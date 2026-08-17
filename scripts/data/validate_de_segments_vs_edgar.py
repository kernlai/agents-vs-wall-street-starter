#!/usr/bin/env python3
"""
Independent validation of data/deere/de_segments_modern.csv against SEC EDGAR.

The offline corpus is the primary source. This script re-derives the same segment
figures from a genuinely independent channel -- the XBRL "Financial Report" R-files
that EDGAR renders from each 10-Q/10-K instance document -- and reports agreement.

Note: data.sec.gov's companyconcept/companyfacts APIs expose only NON-dimensional
facts, so segment-dimensioned values are not retrievable there. The R-files are the
keyless way to reach dimensioned segment facts.

Standard library only.
"""

import csv
import html
import json
import os
import re
import sys
import time
import urllib.request

UA = "AgentsVsWallStreet cor@salomo.io"
CIK = "0000315189"
CSV_PATH = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_segments_modern.csv"

SEGS = {
    # post-ASU 2023-07 axis member labels
    "Production & Precision Agriculture (PPA)": "de_ppa",
    "Small Agriculture & Turf (SAT)": "de_sat",
    "Construction & Forestry (CF)": "de_cf",
    # pre-ASU axis member labels
    "Production & Precision Ag (PPA)": "de_ppa",
    "Small Ag & Turf (SAT)": "de_sat",
    "Production and precision agriculture": "de_ppa",
    "Small agriculture and turf": "de_sat",
    "Construction and forestry": "de_cf",
    # FY2021-FY2022 axis member labels
    "Production & Precision Ag": "de_ppa",
    "Small Ag & Turf": "de_sat",
    "Construction & Forestry": "de_cf",
}


def ctx_segment(line):
    """A dimension context is ' | '-joined axis members in arbitrary order.
    Return (segment_key, frozenset(other members)) or (None, None)."""
    parts = [p.strip() for p in line.split(" | ")]
    hits = [p for p in parts if p in SEGS]
    if len(hits) != 1:
        return None, None
    return SEGS[hits[0]], frozenset(p for p in parts if p != hits[0])

# Lines that may appear INSIDE a segment block without ending it.
SUBHEADERS = {"Net Sales and Revenues", "Operating Profit", "Identifiable Assets",
              "Net Sales and Revenues:", "Operating Profit:", "Operating Profit (Loss)",
              "Net Sales", "Operating Segment"}
PCT_CELL = re.compile(r"^\(?-?[\d,.]+\s*%\)?$")
ROW_LABEL = re.compile(
    r"^(%|Total Assets|Total operating profit|Segment operating profit|Operating profit"
    r"|Net sales|External |Intersegment|Cost of sales|Interest expense|Other segment items"
    r"|Depreciation|Net income|Total segment)")

OP_LABELS = {"Segment operating profit", "Total operating profit", "Operating profit"}
NS_LABELS = {"External net sales", "Net sales", "Net sales and revenues"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
    time.sleep(0.2)
    return b.decode("utf-8", "replace")


def rfile_text(html_text):
    t = re.sub(r"<[^>]+>", "\n", html_text)
    t = html.unescape(t)
    return [x.strip().replace("\xa0", " ") for x in t.split("\n") if x.strip()]


def to_num(s):
    s = s.replace("$", "").replace(",", "").strip()
    if s.endswith("%"):
        return None
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def parse_r_segment(lines):
    """Return [(segment, metric, context, [column values])] for segment-dimensioned rows."""
    cur_seg = None
    cur_ctx = None
    res = []
    i = 0
    while i < len(lines):
        s = lines[i]
        seg, dims = ctx_segment(s)
        if seg is not None:
            cur_seg, cur_ctx = seg, (seg, dims)
            i += 1
            continue
        if cur_seg and s in SUBHEADERS:
            i += 1
            continue
        metric = None
        if cur_seg and s in OP_LABELS:
            metric = "operating_profit"
        elif cur_seg and s in NS_LABELS:
            metric = "net_sales"
        if metric:
            vals, j = [], i + 1
            while j < len(lines) and to_num(lines[j]) is not None:
                vals.append(to_num(lines[j]))
                j += 1
            if vals:
                res.append((cur_seg, metric, cur_ctx, vals))
            i = j
            continue
        # anything else that is neither a numeric cell nor a recognised row label
        # is a new (non-segment) dimension context and ends the block
        if to_num(s) is None and not ROW_LABEL.match(s) and not PCT_CELL.match(s):
            cur_seg = None
        i += 1
    return res


MONTHS = {m[:3]: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}


def parse_col_dates(lines):
    """Column header dates, in order, from the R-file preamble."""
    dates = []
    for s in lines[:60]:
        m = re.fullmatch(r"([A-Z][a-z]{2})\.?\s+(\d{1,2}),\s+(\d{4})", s)
        if m:
            dates.append(f"{m.group(3)}-{MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}")
    return dates


def n_three_month_cols(lines, ndates):
    """R-files list every '<N> Months Ended' group label first, then all the column
    dates. Returns how many leading date columns belong to the 3-month group."""
    groups = [s for s in lines[:60] if re.fullmatch(r"\d+ Months Ended", s)]
    if not groups or groups[0] != "3 Months Ended":
        return 0
    # Deere's quarterly reports always present exactly two 3-month columns
    # (current quarter and prior-year quarter) before any YTD or instant columns.
    return min(2, ndates)


def main():
    subs = json.loads(get(f"https://data.sec.gov/submissions/CIK{CIK}.json"))
    r = subs["filings"]["recent"]
    targets = []
    for form, fdate, acc, rep in zip(r["form"], r["filingDate"],
                                     r["accessionNumber"], r["reportDate"]):
        if form in ("10-Q", "10-K"):
            targets.append((form, fdate, acc.replace("-", ""), rep))

    # load our CSV
    ours = {}
    with open(CSV_PATH) as fh:
        for row in csv.DictReader(fh):
            if row["units"] != "USDm" or row["fiscal_quarter"] == "FY":
                continue
            ours[(row["series_id"], row["period_end"])] = float(row["value"])

    checked = agree = n_filings = 0
    mismatches = []
    covered = set()

    for form, fdate, acc, rep in targets:
        base = f"https://www.sec.gov/Archives/edgar/data/315189/{acc}"
        try:
            fsx = get(base + "/FilingSummary.xml")
        except Exception as e:
            print(f"  skip {form} {fdate}: {e}", file=sys.stderr)
            continue
        cands = []
        for m in re.finditer(r"<Report[^>]*>(.*?)</Report>", fsx, re.S):
            b = m.group(1)
            sn = re.search(r"<ShortName>(.*?)</ShortName>", b)
            fn = re.search(r"<HtmlFileName>(.*?)</HtmlFileName>", b)
            if not sn or not fn:
                continue
            name = html.unescape(sn.group(1))
            if not re.search(r"segment", name, re.I) or "(Details)" not in name:
                continue
            if re.search(r"number of|other disclosur|additional|asset|geograph", name, re.I):
                continue
            cands.append(fn.group(1))
        chosen = None
        for rfile in cands:
            try:
                lines = rfile_text(get(f"{base}/{rfile}"))
            except Exception as e:
                print(f"  skip {form} {fdate} {rfile}: {e}", file=sys.stderr)
                continue
            dates = parse_col_dates(lines)
            n3 = n_three_month_cols(lines, len(dates))
            if not dates or n3 == 0:
                continue
            rows = parse_r_segment(lines)
            if len({r[0] for r in rows if r[1] == "operating_profit"}) >= 3:
                chosen = rfile
                break
        if chosen is None:
            print(f"  no usable 3-month segment R-file: {form} {fdate}", file=sys.stderr)
            continue
        print(f"  {form} {fdate} -> {chosen}", file=sys.stderr)
        # Pick, per (segment, metric), the single correct dimension context.
        #   post-ASU 2023-07: external net sales = '<Seg> | Net Sales | Operating Segment'
        #                     operating profit   = '<Seg> | Operating Segment'
        #   pre-ASU:          both live on the bare '<Seg>' context
        # The BARE '<Segment>' context carries TOTAL segment revenues (external net
        # sales + finance/interest + other + intersegment income), which is NOT the
        # 'segment net sales' line of the earnings release -- accept net sales only
        # from a context that also carries the 'Net Sales' axis member. Operating
        # profit is unambiguous and is accepted from the plain segment context too.
        PREF = {"net_sales": [frozenset({"Net Sales", "Operating Segment"}),
                              frozenset({"Net Sales"})],
                "operating_profit": [frozenset({"Operating Segment"}), frozenset()]}
        best = {}
        for seg, metric, ctx, vals in rows:
            dims = ctx[1]
            pref = PREF[metric]
            if dims not in pref:
                continue
            rank = pref.index(dims)
            k = (seg, metric)
            if k not in best or rank < best[k][0]:
                best[k] = (rank, vals)
        n_filings += 1
        for (seg, metric), (_, vals) in sorted(best.items()):
            for k in range(min(n3, len(vals), len(dates))):
                pe = dates[k]
                sid = f"{seg}_{metric}"
                if (sid, pe) not in ours:
                    continue
                checked += 1
                covered.add((sid, pe))
                if abs(ours[(sid, pe)] - vals[k]) < 0.5:
                    agree += 1
                else:
                    mismatches.append((form, fdate, sid, pe, ours[(sid, pe)], vals[k]))

    print(f"filings with a usable 3-month segment R-file: {n_filings}")
    print(f"EDGAR R-file cross-check: {agree}/{checked} values agree "
          f"({len(covered)} distinct series-period cells covered)")
    for m in mismatches:
        print("  MISMATCH:", m)
    per = {}
    for sid, pe in covered:
        per.setdefault(sid, []).append(pe)
    for sid in sorted(per):
        d = sorted(per[sid])
        print(f"  {sid}: {len(d)} periods {d[0]} .. {d[-1]}")


if __name__ == "__main__":
    main()
