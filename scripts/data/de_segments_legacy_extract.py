#!/usr/bin/env python3
"""
de_segments_legacy_extract.py
=============================
Build the Deere & Company LEGACY segment panel (Agriculture & Turf, Construction & Forestry,
pre-FY2021 basis) plus the RESTATED modern-basis segment figures (Production & Precision Ag,
Small Ag & Turf, Construction & Forestry), and compute the legacy -> modern BRIDGE ratios.

Every number is parsed out of the frozen offline corpus markdown tables. Nothing is
transcribed by hand.

Table shapes handled
--------------------
(A) Press-release (8-K EX-99.1) / 10-Q segment table
        "| Net sales and revenues: | ..."   then    "| Operating profit: * | ..."
    Value columns, after separating explicitly-signed percent-change tokens:
        [current quarter, prior-year quarter]                                (Q1 filings)
        [current quarter, prior-year quarter, YTD current, YTD prior]        (Q2/Q3/Q4)
    For Q4 filings the YTD pair is the full fiscal year.

(B) 10-K annual "OPERATING SEGMENTS" table: three fiscal years side by side.

Validation performed
--------------------
  1. segment net sales must sum to the printed "Total net sales"
  2. segment operating profit + financial services must sum to "Total operating profit"
  3. annual tables: segment sales + FS revenues + other revenues == printed Total
  4. every value seen in more than one document is compared across documents; genuine
     restatements are kept as separate flagged rows, parse mismatches are reported
  5. consolidated totals are cross-checked against the SEC EDGAR XBRL API (separate script)

Usage:  python3 de_segments_legacy_extract.py
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict, OrderedDict

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
FILINGS = os.path.join(CORPUS, "filings")
OUTDIR = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere"
OUT_CSV = os.path.join(OUTDIR, "de_segments_legacy.csv")

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}


def iso(month, day, year):
    return "%04d-%02d-%02d" % (int(year), MONTHS[month], int(day))


def clean(s):
    return s.replace("​", "").replace("&amp;", "&").strip()


def cells(line):
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [clean(c) for c in raw.split("|")]


TOKEN_RE = re.compile(r"([-+]?)\(?\s*\$?\s*(\d[\d,]*)\s*\)?")


def row_tokens(line):
    """(label, values, pcts). Percent-change tokens carry an explicit +/- sign in these
    tables; data values are unsigned, or negative inside parentheses."""
    cs = cells(line)
    if not cs:
        return "", [], []
    label = clean(cs[0])
    body = " ".join(cs[1:]).replace("%", " ")
    values, pcts, pos = [], [], 0
    while True:
        m = TOKEN_RE.search(body, pos)
        if not m:
            break
        sign, digits = m.group(1), m.group(2).replace(",", "")
        frag = body[m.start():m.end()]
        pos = m.end()
        if sign in ("+", "-"):
            pcts.append(float(sign + digits))
        elif "(" in frag:
            values.append(-float(digits))
        else:
            values.append(float(digits))
    return label, values, pcts


def norm(lbl):
    l = clean(lbl).lower()
    l = l.replace("&", " & ")
    l = re.sub(r"[*:]+\s*$", "", l).strip()
    l = re.sub(r"\s+", " ", l).strip()
    l = re.sub(r"[*:]+\s*$", "", l).strip()
    return l


# Labels are matched on a "squeezed" key (lowercase, letters only) so that the many
# typographic variants in the corpus -- "Production &precision ag",
# "Production &PrecisionAg net sales", "Production & Precision Agriculture" -- all collapse
# onto one code. Order matters: SAT must be tested before AT.
SEG_ALIASES = [
    ("PPA", (r"^production(and)?precisionag(riculture)?(netsales)?$",)),
    ("SAT", (r"^smallag(riculture)?(and)?turf(netsales)?$",)),
    ("AT", (r"^agriculture(and)?turf(netsales)?$",)),
    ("CF", (r"^construction(and)?forestry(netsales)?$",)),
]


def squeeze(nl):
    return re.sub(r"[^a-z]", "", nl.lower())


def seg_of(nl):
    s = squeeze(nl)
    for code, pats in SEG_ALIASES:
        for pat in pats:
            if re.match(pat, s):
                return code
    return None


# ------------------------------------------------------------------ period ends

HDR_FULL = re.compile(
    r"For the Three Months Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})\s+and\s+([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})")
HDR_SHORT = re.compile(
    r"For the Three Months Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})\s+and\s+(\d{4})")


def period_ends(text):
    m = HDR_FULL.search(text)
    if m:
        return iso(m.group(1), m.group(2), m.group(3)), iso(m.group(4), m.group(5), m.group(6))
    m = HDR_SHORT.search(text)
    if m:
        return iso(m.group(1), m.group(2), m.group(3)), iso(m.group(1), m.group(2), m.group(4))
    return None, None


def fy_quarter(pend):
    y, mth, d = [int(x) for x in pend.split("-")]
    if mth in (10, 11):
        return y, "Q4"
    if mth in (1, 2):
        return y, "Q1"
    if mth in (4, 5):
        return y, "Q2"
    if mth in (7, 8):
        return y, "Q3"
    raise ValueError(pend)


# ------------------------------------------------------------------ shape (A)

STOP_A = ("intersegment", "identifiable assets", "equipment operations outside")


def parse_segment_table(text):
    lines = text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^\|\s*Net sales and revenues:", ln):
            start = i
            break
    if start is None:
        return None
    seg = {"sales": OrderedDict(), "op": OrderedDict()}
    tot = {}
    section = None
    for ln in lines[start:start + 45]:
        if not ln.strip().startswith("|"):
            if seg["op"]:
                break
            continue
        label, vals, pcts = row_tokens(ln)
        nl = norm(label)
        if any(nl.startswith(s) for s in STOP_A):
            break
        if nl.startswith("net sales and revenues") and not vals:
            section = "sales"
            continue
        if nl.startswith("operating profit") and not vals:
            section = "op"
            continue
        if nl.startswith("net income attributable"):
            break
        if section is None:
            continue
        code = seg_of(nl)
        if code:
            seg[section][code] = vals
        elif squeeze(nl).startswith("financialservices"):
            seg[section]["FS"] = vals
        elif nl == "total net sales":
            tot["sales_total"] = vals
        elif nl.startswith("total operating profit"):
            tot["op_total"] = vals
        elif nl.startswith("total net sales and revenues"):
            tot["rev_total"] = vals
    if not seg["sales"]:
        return None
    return seg, tot


def inventory():
    out = []
    for f in sorted(os.listdir(FILINGS)):
        m = re.match(r"(\d{4}-\d{2}-\d{2})__de-us-\d{8}-(q[1-4]|fy)-(8k|10q|10k)", f)
        if m:
            out.append((m.group(1), m.group(2), m.group(3), os.path.join(FILINGS, f), f))
    return out


# ------------------------------------------------------------------ shape (B)

def parse_annual_tables(text, rel, problems):
    """Parse 10-K 'OPERATING SEGMENTS' three-year tables."""
    out = []
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if not re.match(r"^\|\s*OPERATING SEGMENTS", ln):
            continue
        years = [int(y) for y in re.findall(r"\b(20\d\d)\b", ln)]
        if len(years) != 3:
            continue
        section = None
        found = {}
        totals = {}
        for bl in lines[i + 1:i + 55]:
            if not bl.strip().startswith("|"):
                continue
            label, vals, pcts = row_tokens(bl)
            nl = norm(label)
            if nl.startswith("net income"):
                break
            if nl.startswith("interest income") or nl.startswith("interest expense") \
               or nl.startswith("depreciation") or nl.startswith("identifiable assets") \
               or nl.startswith("capital additions"):
                break
            # section markers, possibly fused with the first data row
            if nl.startswith("net sales and revenues"):
                section = "sales"
                nl = norm(nl[len("net sales and revenues"):])
                if not nl:
                    continue
            if nl.startswith("unaffiliated customers"):
                section = "sales"
                nl = norm(re.sub(r"^unaffiliated customers[:.]?", "", nl))
                if not nl:
                    continue
            if nl.startswith("operating profit"):
                if nl.startswith("total operating profit"):
                    if len(vals) >= 3:
                        totals["op_total"] = vals[:3]
                    continue
                section = "op"
                nl = norm(nl[len("operating profit"):])
                if not nl:
                    continue
            if section is None:
                continue
            code = seg_of(nl)
            if code and len(vals) >= 3:
                found[(code, section)] = vals[:3]
            elif nl.startswith("financial services") and len(vals) >= 3:
                found[("FS", section)] = vals[:3]
            elif nl.startswith("other revenues") and len(vals) >= 3:
                totals["other_rev"] = vals[:3]
            elif nl == "total" and len(vals) >= 3 and section == "sales":
                totals["rev_total"] = vals[:3]
        segs = sorted({k[0] for k in found if k[0] != "FS"})
        if not segs:
            continue
        basis = "modern-PPA" if "PPA" in segs else "legacy-AT"
        # validation 3
        if "rev_total" in totals and "other_rev" in totals and ("FS", "sales") in found:
            for yi in range(3):
                s = sum(found[(g, "sales")][yi] for g in segs if (g, "sales") in found)
                s += found[("FS", "sales")][yi] + totals["other_rev"][yi]
                if abs(s - totals["rev_total"][yi]) > 1.0:
                    problems.append("ANNUAL REV SUMCHECK FAIL %s %s %s vs %s"
                                    % (rel, years[yi], s, totals["rev_total"][yi]))
                    return out
        if "op_total" in totals and ("FS", "op") in found:
            for yi in range(3):
                s = sum(found[(g, "op")][yi] for g in segs if (g, "op") in found)
                s += found[("FS", "op")][yi]
                if abs(s - totals["op_total"][yi]) > 1.0:
                    problems.append("ANNUAL OP SUMCHECK FAIL %s %s %s vs %s"
                                    % (rel, years[yi], s, totals["op_total"][yi]))
                    return out
        for (g, metric), vals in found.items():
            if g == "FS":
                continue
            for yi, yr in enumerate(years):
                out.append(dict(seg=g, metric=metric, fy=yr, fq="FY", value=vals[yi],
                                basis=basis, role="current" if yr == max(years) else "prior-comparative",
                                source=rel, form="10k"))
    return out


# ------------------------------------------------------------------ extraction

def extract():
    obs, problems = [], []
    for pub, qtag, form, path, fname in inventory():
        text = open(path, encoding="utf-8").read()
        rel = os.path.relpath(path, CORPUS)
        if form == "10k":
            for o in parse_annual_tables(text, rel, problems):
                o["pub"] = pub
                obs.append(o)
            continue

        parsed = parse_segment_table(text)
        if not parsed:
            continue
        seg, tot = parsed
        cur_end, prior_end = period_ends(text)
        if cur_end is None:
            problems.append("no period header: " + fname)
            continue
        present = [k for k in seg["sales"] if k != "FS"]
        basis = "modern-PPA" if "PPA" in present else "legacy-AT"

        colsets = [(0, cur_end, "Q"), (1, prior_end, "Q")]
        if qtag in ("q4", "fy"):
            colsets += [(2, cur_end, "FY"), (3, prior_end, "FY")]

        for col, pend, freq in colsets:
            vals, complete = {}, True
            for g in present:
                for metric in ("sales", "op"):
                    arr = seg[metric].get(g, [])
                    if len(arr) <= col:
                        complete = False
                    else:
                        vals[(g, metric)] = arr[col]
            if not complete:
                problems.append("incomplete columns %s col%d" % (fname, col))
                continue
            if "sales_total" in tot and len(tot["sales_total"]) > col:
                s = sum(vals[(g, "sales")] for g in present)
                if abs(s - tot["sales_total"][col]) > 1.0:
                    problems.append("SALES SUMCHECK FAIL %s col%d %s vs %s"
                                    % (fname, col, s, tot["sales_total"][col]))
                    continue
            if "op_total" in tot and len(tot["op_total"]) > col and "FS" in seg["op"] \
               and len(seg["op"]["FS"]) > col:
                s = sum(vals[(g, "op")] for g in present) + seg["op"]["FS"][col]
                if abs(s - tot["op_total"][col]) > 1.0:
                    problems.append("OP SUMCHECK FAIL %s col%d %s vs %s"
                                    % (fname, col, s, tot["op_total"][col]))
                    continue
            fy, fq = fy_quarter(pend)
            if freq == "FY":
                fq = "FY"
            role = "current" if col in (0, 2) else "prior-comparative"
            for g in present:
                for metric in ("sales", "op"):
                    obs.append(dict(seg=g, metric=metric, fy=fy, fq=fq, value=vals[(g, metric)],
                                    basis=basis, role=role, source=rel, form=form,
                                    pub=pub, period_end=pend))
    return obs, problems


# ------------------------------------------------------------------ canonical calendar

def canonical_calendar(obs):
    """(fy, fq) -> canonical period end, taken from the ORIGINAL as-reported filing.
    Also records any alternate date a later filing used for the same period."""
    cand = defaultdict(list)
    for o in obs:
        if "period_end" not in o or o["fq"] == "FY":
            continue
        cand[(o["fy"], o["fq"])].append((o["pub"], o["role"], o["period_end"]))
    cal, alt = {}, {}
    for k, lst in cand.items():
        cur = sorted([x for x in lst if x[1] == "current"]) or sorted(lst)
        cal[k] = cur[0][2]
        others = sorted({x[2] for x in lst} - {cal[k]})
        if others:
            alt[k] = others
    # FY rows end on the Q4 date
    for (fy, fq), pend in list(cal.items()):
        if fq == "Q4":
            cal[(fy, "FY")] = pend
            if (fy, "Q4") in alt:
                alt[(fy, "FY")] = alt[(fy, "Q4")]
    return cal, alt


# ------------------------------------------------------------------ reconcile

def reconcile(obs):
    groups = defaultdict(list)
    for o in obs:
        groups[(o["seg"], o["metric"], o["fy"], o["fq"], o["basis"])].append(o)

    primary, restatements, agreements, unresolved = {}, [], [], []
    for key, lst in groups.items():
        cur = sorted([o for o in lst if o["role"] == "current"], key=lambda o: o["pub"])
        comp = [o for o in lst if o["role"] == "prior-comparative"]
        if cur:
            base = cur[0]
            flag = "as_reported"
            # do the original as-reported filings agree among themselves (8-K vs 10-Q)?
            same_pub = [o for o in cur if o["pub"] == base["pub"]]
            if len({o["value"] for o in same_pub}) > 1:
                unresolved.append((key, sorted({o["value"] for o in same_pub}),
                                   sorted({o["source"] for o in same_pub})))
                continue
            if len(same_pub) > 1:
                agreements.append((key, base["value"], sorted({o["source"] for o in same_pub})))
            # later filings restating the same period?
            later_vals = defaultdict(list)
            for o in cur[1:] + comp:
                if abs(o["value"] - base["value"]) > 0.5:
                    later_vals[o["value"]].append(o)
                else:
                    agreements.append((key, base["value"], [o["source"]]))
            for v, olist in later_vals.items():
                restatements.append((key, base["value"], v,
                                     sorted({o["source"] for o in olist}),
                                     min(o["pub"] for o in olist)))
        else:
            # only ever seen as a prior-year comparative
            vals = {o["value"] for o in comp}
            base = sorted(comp, key=lambda o: o["pub"])[0]
            flag = "as_reported_comparative"
            if len(vals) > 1:
                unresolved.append((key, sorted(vals), sorted({o["source"] for o in comp})))
                continue
            if len({o["source"] for o in comp}) > 1:
                agreements.append((key, base["value"], sorted({o["source"] for o in comp})))
        b = dict(base)
        b["flag"] = flag
        primary[key] = b
    return primary, restatements, agreements, unresolved


if __name__ == "__main__":
    obs, problems = extract()
    cal, alt = canonical_calendar(obs)
    primary, restatements, agreements, unresolved = reconcile(obs)
    print("raw observations      :", len(obs))
    print("primary series points :", len(primary))
    print("cross-doc agreements  :", len(agreements))
    print("genuine restatements  :", len(restatements))
    print("UNRESOLVED conflicts  :", len(unresolved))
    for u in unresolved:
        print("   !!", u)
    print("parse problems        :", len(problems))
    for p in problems:
        print("   ", p)
    print("\nalternate period-end labels:", json.dumps({str(k): v for k, v in sorted(alt.items())}, indent=0))
    json.dump({"obs": obs, "cal": {"%s|%s" % k: v for k, v in cal.items()},
               "alt": {"%s|%s" % k: v for k, v in alt.items()},
               "restatements": [[list(k), a, b, s, p] for k, a, b, s, p in restatements],
               "primary": {"|".join(str(x) for x in k): v for k, v in primary.items()},
               "n_agreements": len(agreements),
               "agreements": [["|".join(str(x) for x in k), v, s] for k, v, s in agreements]},
              open("/tmp/de_seg_raw.json", "w"))
