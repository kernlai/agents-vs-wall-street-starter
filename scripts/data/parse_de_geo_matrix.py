#!/usr/bin/env python3
"""
Parse Deere's ASC 606 revenue-recognition footnote geography x segment matrix
out of the offline 10-Q / 10-K corpus.

Handles three formatting eras:
  era A (FY2019-FY2020): "| | Agriculture and Turf | Construction and Forestry | Financial Services | Total |"
  era B (FY2021-FY2024): header row of segment names, values padded with spaces
  era C (FY2025-FY2026): heavy zero-width / non-breaking whitespace, "$" in its own cell

Output: tidy long CSV of region x segment revenue on the rev-rec basis,
plus a reconciliation report (rows must sum to the row total, columns to the
column total).

Standard library only.
"""

import csv
import os
import re
import sys
from collections import OrderedDict

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
FILINGS = os.path.join(CORPUS, "filings")

# ---------------------------------------------------------------- cleaning ---

# zero-width space, zero-width non-joiner/joiner, BOM, non-breaking space,
# narrow nbsp, figure space, thin space, en/em space
JUNK = dict.fromkeys(
    map(ord, "​‌‍﻿      ⁠"),
    " ",
)


def clean(s):
    s = s.translate(JUNK)
    s = s.replace("–", "-").replace("—", "-").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip()


def cells(line):
    """Split a markdown table row into cleaned cells."""
    if "|" not in line:
        return None
    parts = line.split("|")
    # drop the empty artifacts of leading/trailing pipes
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [clean(p) for p in parts]


NUM_RE = re.compile(r"^\(?\$?\s*-?[\d,]+(?:\.\d+)?\)?$")


def to_num(tok):
    """Return float for a numeric cell, else None. Handles $ and (negatives)."""
    t = tok.replace("$", "").strip()
    if t in ("", "-", "--"):
        return None
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()").replace(",", "")
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def row_numbers(cs):
    """Extract the ordered numeric values from a table row's cells,
    ignoring pure-'$' cells and empty separator cells."""
    out = []
    for c in cs:
        if c in ("", "$"):
            continue
        v = to_num(c)
        if v is not None:
            out.append(v)
    return out


# ------------------------------------------------------------- vocabulary ---

GEOS = OrderedDict(
    [
        ("United States", "United States"),
        ("Canada", "Canada"),
        ("Western Europe", "Western Europe"),
        ("Central Europe and CIS", "Central Europe and CIS"),
        ("Latin America", "Latin America"),
        ("Asia, Africa, Oceania, and Middle East", "Asia, Africa, Oceania, and Middle East"),
    ]
)

# tolerant matching of the geography label appearing in the first cell
GEO_PATTERNS = [
    ("United States", re.compile(r"^(?:primary\s+geograph\w*\s*)?(?:markets?:?\s*)?united states\b", re.I)),
    ("Canada", re.compile(r"^canada\b", re.I)),
    ("Western Europe", re.compile(r"^western europe\b", re.I)),
    ("Central Europe and CIS", re.compile(r"^central europe\s*(?:and|&)\s*cis\b", re.I)),
    ("Latin America", re.compile(r"^latin america\b", re.I)),
    # label text changed over time (Australia/New Zealand -> Oceania) and often
    # wraps across two markdown rows; match the stem and pull numbers forward
    ("Asia, Africa, Oceania, and Middle East", re.compile(r"^asia,?\s*africa", re.I)),
]


def match_geo(first_cell):
    for name, pat in GEO_PATTERNS:
        if pat.match(first_cell):
            return name
    return None


SEG_PATTERNS = [
    ("PPA", re.compile(r"production\s*&?\s*precision\s*ag|^ppa$", re.I)),
    ("SAT", re.compile(r"small\s*ag\s*&?\s*(and)?\s*turf|^sat$", re.I)),
    ("AT", re.compile(r"agriculture\s*(and)?\s*&?\s*turf", re.I)),
    ("CF", re.compile(r"construction\s*(and|&)\s*forestry|^cf$", re.I)),
    ("FS", re.compile(r"financial\s*services|^fs$", re.I)),
    ("Total", re.compile(r"^total$", re.I)),
]


def parse_segment_header(cs):
    """Given a candidate header row, return the ordered segment codes, or None."""
    segs = []
    for c in cs:
        if not c:
            continue
        for code, pat in SEG_PATTERNS:
            if pat.search(c):
                if not segs or segs[-1] != code:
                    segs.append(code)
                break
    # a valid header ends with Total and has >= 3 segments
    if len(segs) >= 3 and segs[-1] == "Total":
        # de-dup consecutive repeats (era-B repeats the same header cell)
        return segs
    return None


# -------------------------------------------------------------- period id ---

MONTHS = {
    m: i + 1
    for i, m in enumerate(
        [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december",
        ]
    )
}

DATE_RE = re.compile(
    r"(?:three|six|nine|twelve)\s+months\s+ended\s+"
    r"([a-z]+)\s+(\d{1,2}),?\s*(\d{4})",
    re.I,
)
PERIOD_LEN_RE = re.compile(r"(three|six|nine|twelve)\s+months\s+ended", re.I)
QTR_TEXT_RE = re.compile(
    r"in the (first|second|third|fourth) quarter of (\d{4})", re.I
)
QTR_ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4}
LEN_MONTHS = {"three": 3, "six": 6, "nine": 9, "twelve": 12}


def parse_period(text):
    """Return (period_end_iso, n_months) or (None, None)."""
    m = DATE_RE.search(text)
    if m:
        mon = MONTHS.get(m.group(1).lower())
        if mon:
            lm = PERIOD_LEN_RE.search(text)
            n = LEN_MONTHS[lm.group(1).lower()] if lm else 3
            return "%04d-%02d-%02d" % (int(m.group(3)), mon, int(m.group(2))), n
    return None, None


# Deere fiscal year ends late Oct/early Nov; Q1 ends late Jan/early Feb.
def fiscal_qtr(period_end):
    y, m, d = (int(x) for x in period_end.split("-"))
    # quarter by month of the period end
    if m in (1, 2):
        return y, "Q1"
    if m in (4, 5):
        return y, "Q2"
    if m in (7, 8):
        return y, "Q3"
    if m in (10, 11):
        # fiscal year end -- if end-Oct/early-Nov it closes FY y
        return y, "Q4"
    raise ValueError("unexpected period end " + period_end)


# ------------------------------------------------------------------ parse ---


def parse_file(path):
    """Yield dict blocks: {period_end, n_months, segs, data{geo:{seg:val}}, total_row}"""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    blocks = []
    cur_segs = None
    cur_segs_line = -10**9
    cur_period = None
    cur_nmonths = None
    cur_period_line = -10**9
    pending_qtr_text = None
    pending_qtr_line = -10**9

    # proximity guards: a period / segment header only applies to a block that
    # starts within this many lines of it. Without this the annual 10-K tables
    # inherit a stale "Three Months Ended" from elsewhere in the document.
    PERIOD_WINDOW = 30
    SEG_WINDOW = 30

    i = 0
    while i < len(lines):
        raw = lines[i]
        line = clean(raw)

        p, n = parse_period(line)
        if p:
            cur_period, cur_nmonths, cur_period_line = p, n, i

        qt = QTR_TEXT_RE.search(line)
        if qt:
            pending_qtr_text = (QTR_ORD[qt.group(1).lower()], int(qt.group(2)))
            pending_qtr_line = i

        cs = cells(raw)
        if cs:
            hdr = parse_segment_header(cs)
            if hdr:
                cur_segs, cur_segs_line = hdr, i
            # also pick up a period embedded in a table header cell
            for c in cs:
                p2, n2 = parse_period(c)
                if p2:
                    cur_period, cur_nmonths, cur_period_line = p2, n2, i

            geo = match_geo(cs[0]) if cs else None
            in_seg_window = (i - cur_segs_line) <= SEG_WINDOW
            if geo == "United States" and cur_segs and in_seg_window:
                nseg = len(cur_segs)
                data = OrderedDict()
                total_row = None
                j = i
                seen = set()
                while j < len(lines) and j < i + 40:
                    cj = cells(lines[j])
                    if cj is None:
                        j += 1
                        continue
                    g = match_geo(cj[0])
                    if g and g not in seen:
                        nums = row_numbers(cj)
                        if len(nums) != nseg:
                            # the label wrapped onto the next markdown row and
                            # the figures live there (e.g. "Asia, Africa, ..." /
                            # "East  332  393  313  53  1,091")
                            ck = cells(lines[j + 1]) if j + 1 < len(lines) else None
                            if ck is not None and not match_geo(ck[0]):
                                nums2 = row_numbers(ck)
                                if len(nums2) == nseg:
                                    nums = nums2
                                    j += 1
                        if len(nums) == nseg:
                            data[g] = OrderedDict(zip(cur_segs, nums))
                            seen.add(g)
                    elif re.match(r"^total$", cj[0], re.I) and len(seen) >= 4:
                        nums = row_numbers(cj)
                        if len(nums) == nseg:
                            total_row = OrderedDict(zip(cur_segs, nums))
                        break
                    j += 1

                if len(data) == 6:
                    period = cur_period if (i - cur_period_line) <= PERIOD_WINDOW else None
                    nm = cur_nmonths if period else None
                    qtxt = (
                        pending_qtr_text
                        if (i - pending_qtr_line) <= PERIOD_WINDOW
                        else None
                    )
                    blocks.append(
                        dict(
                            period_end=period,
                            n_months=nm,
                            qtr_text=qtxt,
                            segs=list(cur_segs),
                            data=data,
                            total_row=total_row,
                            line=i + 1,
                        )
                    )
                i = j
        i += 1
    return blocks


# ------------------------------------------------------------------- main ---

# Deere fiscal quarter end dates (period ends) for the era-A filings whose
# footnote says only "in the first quarter of 2019".
FALLBACK_QTR_END = {
    (2019, 1): "2019-01-27", (2019, 2): "2019-04-28", (2019, 3): "2019-07-28", (2019, 4): "2019-11-03",
    (2020, 1): "2020-02-02", (2020, 2): "2020-05-03", (2020, 3): "2020-08-02", (2020, 4): "2020-11-01",
}


def main():
    paths = sorted(
        os.path.join(FILINGS, f)
        for f in os.listdir(FILINGS)
        if f.endswith(".md")
    )

    records = {}  # (period_end, geo, seg) -> (value, source)
    recon = []
    seen_blocks = 0

    for path in paths:
        with open(path, encoding="utf-8") as fh:
            if "Central Europe" not in fh.read():
                continue
        for b in parse_file(path):
            if b["n_months"] not in (3, None):
                continue  # only three-month (quarterly) blocks
            pe = b["period_end"]
            if pe is None and b["qtr_text"]:
                pe = FALLBACK_QTR_END.get(b["qtr_text"])
            if pe is None:
                continue
            if b["n_months"] is None and b["qtr_text"] is None:
                continue
            seen_blocks += 1

            # ---- validation
            segs = [s for s in b["segs"] if s != "Total"]
            row_ok, col_ok = True, True
            for g, row in b["data"].items():
                if "Total" in row:
                    s = sum(row[s] for s in segs if s in row)
                    if abs(s - row["Total"]) > 1.0:
                        row_ok = False
                        recon.append((pe, "row", g, s, row["Total"], os.path.basename(path)))
            if b["total_row"]:
                for s in b["segs"]:
                    csum = sum(r[s] for r in b["data"].values() if s in r)
                    if abs(csum - b["total_row"][s]) > 1.0:
                        col_ok = False
                        recon.append((pe, "col", s, csum, b["total_row"][s], os.path.basename(path)))

            for g, row in b["data"].items():
                for s, v in row.items():
                    key = (pe, g, s)
                    # prefer the earliest (as-first-reported) filing; comparatives
                    # in later filings should agree, and do
                    if key not in records:
                        records[key] = (v, os.path.basename(path), row_ok and col_ok)

    # ---- write
    out = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_geo_matrix.csv"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(
            "series_id,period_end,fiscal_year,fiscal_quarter,segment,geography,"
            "product_line,value,units,basis,source,notes".split(",")
        )
        for (pe, g, s), (v, src, ok) in sorted(records.items()):
            fy, fq = fiscal_qtr(pe)
            w.writerow(
                [
                    "de_revrec_%s_%s"
                    % (s.lower(), re.sub(r"[^a-z]+", "_", g.lower()).strip("_")),
                    pe, fy, fq, s, g, "", "%g" % v, "USDm", "rev-rec",
                    "filings/" + src,
                    "reconciles=%s" % ("yes" if ok else "NO"),
                ]
            )

    periods = sorted({k[0] for k in records})
    print("blocks parsed:", seen_blocks)
    print("quarters:", len(periods), periods[0], "->", periods[-1])
    print("rows:", len(records))
    print("\nreconciliation failures:", len(recon))
    for r in recon[:40]:
        print("  ", r)
    print("\nper-quarter geographies present:")
    for p in periods:
        gs = {k[1] for k in records if k[0] == p}
        ss = {k[2] for k in records if k[0] == p}
        print("  ", p, len(gs), "geos", sorted(ss))
    return 0


if __name__ == "__main__":
    sys.exit(main())
