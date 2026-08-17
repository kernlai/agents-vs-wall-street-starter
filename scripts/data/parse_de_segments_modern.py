#!/usr/bin/env python3
"""
Extract Deere & Company MODERN-BASIS segment series (FY2021 reorganisation basis:
Production & Precision Ag / Small Ag & Turf / Construction & Forestry) from the
offline corpus of 8-K quarterly earnings releases and 10-Q segment footnotes.

Standard library only.

Output: tidy long CSV
  series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes

Design notes
------------
* The 8-K "<Quarter> PRESS RELEASE" table is the primary source. It carries, for each
  segment, three-month net sales and three-month operating profit for the CURRENT quarter
  and the PRIOR-YEAR quarter, plus year-to-date columns (except Q1).
* Prior-year columns in the FY2021 releases are the RESTATED FY2020 comparatives on the
  modern PPA basis -- Deere never published FY2020 quarters on this basis contemporaneously.
  These are captured and flagged as_reported_or_restated=restated.
* The 10-Q / 10-K segment footnote ("SEGMENT DATA") is parsed independently and used as a
  cross-check, never merged blindly.
* Percent-change columns printed in the filing are used as an internal arithmetic check.
"""

import csv
import os
import re
import sys
from collections import defaultdict
from datetime import date

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
FILINGS = os.path.join(CORPUS, "filings")
OUT_CSV = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_segments_modern.csv"

ZW = "​"

SEG_KEYS = {
    "ppa": "de_ppa",
    "sat": "de_sat",
    "cf": "de_cf",
}

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}


# --------------------------------------------------------------------------- helpers

def norm_label(s):
    s = s.replace("&amp;", "&").replace(ZW, "")
    s = s.lower()
    s = re.sub(r"[^a-z ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def seg_of(label):
    """Map a normalised row label to a segment key, or None."""
    l = label
    if l.startswith("production") and ("precision" in l):
        return "ppa"
    if l.startswith("ppa"):
        return "ppa"
    if l.startswith("small ag"):
        return "sat"
    if l.startswith("sat"):
        return "sat"
    if l.startswith("construction") and "forestry" in l:
        return "cf"
    if l.startswith("cf"):
        return "cf"
    return None


NUM_RE = re.compile(r"^\(?\$?\s*-?\+?[\d,]+\)?$")


def cells(line):
    parts = line.split("|")
    out = []
    for p in parts:
        t = p.replace(ZW, "").replace("&amp;", "&").strip()
        t = t.replace("\xa0", " ").strip()
        if t in ("", "$", "-", "--", "—", "*", "**"):
            continue
        out.append(t)
    return out


def to_num(tok):
    t = tok.replace("$", "").replace(",", "").replace(" ", "").strip()
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    t = t.lstrip("+")
    if t in ("", "-"):
        return None
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def parse_dates(text):
    """Return (current_period_end, prior_period_end) as ISO strings."""
    pat = re.compile(
        r"[Ff]or the [Tt]hree(?:\s+and\s+(?:Six|Nine))?\s*(?:Months?)?"
        r"(?:\s+and\s+(?:Years|Fiscal Years|Year))?\s+[Ee]nded\s+"
        r"([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4}),?\s+and\s+"
        r"([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})")
    m = pat.search(text)
    if not m:
        return None, None
    a = date(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2)))
    b = date(int(m.group(6)), MONTHS[m.group(4)], int(m.group(5)))
    return a.isoformat(), b.isoformat()


def fiscal_of(period_end_iso):
    """Deere FY ends late Oct/early Nov. FY = calendar year of the FY end."""
    y, m, d = (int(x) for x in period_end_iso.split("-"))
    # A period end in Nov or Dec belongs to the fiscal year that just ended in that Nov,
    # i.e. FY == that calendar year. Period ends Jan..Oct belong to FY == calendar year.
    return y


def quarter_of(period_end_iso):
    m = int(period_end_iso.split("-")[1])
    d = int(period_end_iso.split("-")[2])
    if m in (1, 2):
        return "Q1"
    if m in (4, 5):
        return "Q2"
    if m in (7, 8):
        return "Q3"
    if m in (10, 11):
        return "Q4"
    if m == 3:
        return "Q2"
    return None


# ---------------------------------------------------------------- 8-K press-release table

def parse_8k_segment_table(path):
    """Parse the '<QUARTER> PRESS RELEASE' segment table from an 8-K.

    Returns dict with keys:
      cur_end, prior_end, rows -> {(seg, metric): (cur_q, prior_q, pct, cur_ytd, prior_ytd, pct_ytd)}
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()

    cur_end, prior_end = parse_dates(text)

    # find start of segment table
    start = None
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("|") and "net sales and revenues:" in ln.lower():
            start = i
            break
    if start is None:
        return None

    section = None
    rows = {}
    for ln in lines[start:start + 40]:
        if not ln.lstrip().startswith("|"):
            if rows:
                break
            continue
        c = cells(ln)
        if not c:
            continue
        lab = norm_label(c[0])
        if lab.startswith("net sales and revenues"):
            section = "net_sales"
            continue
        if lab.startswith("operating profit"):
            section = "operating_profit"
            continue
        if lab.startswith("net income attributable"):
            break
        seg = seg_of(lab)
        if seg is None or section is None:
            continue
        nums = [to_num(t) for t in c[1:] if NUM_RE.match(t)]
        nums = [n for n in nums if n is not None]
        rows[(seg, section)] = nums

    return {"cur_end": cur_end, "prior_end": prior_end, "rows": rows,
            "src": os.path.relpath(path, CORPUS)}


# ------------------------------------------------------------------- 10-Q segment footnote

def parse_legacy_segment_footnote(path):
    """FY2021-FY2024 10-Q/10-K segment note: same markdown layout as the 8-K table.

    Returns {(period_end, seg, metric): value} for the three-month current column.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    cur_end, prior_end = parse_dates(text)
    out = {}
    if cur_end is None:
        return out

    for i, ln in enumerate(lines):
        if not ln.lstrip().startswith("|"):
            continue
        c = cells(ln)
        if not c:
            continue
        if norm_label(c[0]) not in ("net sales and revenues", "net sales and revenues "):
            continue
        # candidate segment-note table; walk it
        section = "net_sales"
        block = {}
        for ln2 in lines[i + 1:i + 30]:
            if not ln2.lstrip().startswith("|"):
                break
            c2 = cells(ln2)
            if not c2:
                continue
            lab = norm_label(c2[0])
            if lab.startswith("intersegment") or lab.startswith("outside the u s"):
                break
            if lab.startswith("operating profit"):
                section = "operating_profit"
                continue
            if lab.startswith("total") or lab.startswith("net income") or \
               lab.startswith("reconciling") or lab.startswith("income taxes"):
                continue
            seg = seg_of(lab)
            if seg is None:
                continue
            nums = [to_num(t) for t in c2[1:] if NUM_RE.match(t)]
            nums = [n for n in nums if n is not None]
            if nums:
                block[(cur_end, seg, section)] = nums[0]
                if len(nums) > 1:
                    block[(prior_end, seg, section)] = nums[1]
        if len([k for k in block if k[2] == "operating_profit"]) >= 3:
            out.update(block)
            break
    return out


ASU_HDR = re.compile(
    r"(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})\s+PPA")


def parse_asu_segment_footnote(path):
    """FY2025+ 10-Q/10-K segment note (post ASU 2023-07): transposed plain-text blocks
    'Three Months Ended <date>  PPA SAT CF FS Total' followed by
    'External net sales ...' and 'Segment operating profit ...'.

    Returns {(period_end, seg, metric): value} for THREE-MONTH blocks only.
    """
    def flat(s):
        s = s.replace(ZW, "").replace("&amp;", "&").replace("|", " ")
        return re.sub(r"\s+", " ", s).strip()

    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = [flat(x) for x in text.splitlines()]
    out = {}
    for i, ln in enumerate(lines):
        m = ASU_HDR.search(ln)
        if not m:
            continue
        if m.group(1) != "Three":
            continue
        pe = date(int(m.group(4)), MONTHS[m.group(2)], int(m.group(3))).isoformat()
        for s in lines[i + 1:i + 14]:
            if re.search(r"Months\s+Ended\s+[A-Z][a-z]+\s+\d{1,2},\s*\d{4}", s):
                break  # next transposed block starts here
            metric = None
            if s.startswith("External net sales"):
                metric = "net_sales"
                rest = s[len("External net sales"):]
            elif s.startswith("Segment operating profit"):
                metric = "operating_profit"
                rest = s[len("Segment operating profit"):]
            if metric is None:
                continue
            toks = re.findall(r"\(?\$?\s*-?[\d,]+\)?", rest)
            vals = [to_num(t) for t in toks]
            vals = [v for v in vals if v is not None]
            # PPA SAT CF [FS] Total -- first three are the equipment segments
            if len(vals) >= 4:
                for seg, v in zip(("ppa", "sat", "cf"), vals[:3]):
                    out[(pe, seg, metric)] = v
    return out


# ------------------------------------------------------------------------------- driver

MODERN_8K = [
    ("2021-02-19__de-us-20210219-q1-8k__105842.md", "Q1", 2021),
    ("2021-05-21__de-us-20210521-q2-8k__105846.md", "Q2", 2021),
    ("2021-08-20__de-us-20210820-q3-8k__105827.md", "Q3", 2021),
    ("2021-11-24__de-us-20211124-q4-8k__105843.md", "Q4", 2021),
    ("2022-02-18__de-us-20220218-q1-8k__105812.md", "Q1", 2022),
    ("2022-05-20__de-us-20220520-q2-8k__105815.md", "Q2", 2022),
    ("2022-08-19__de-us-20220819-q3-8k__105811.md", "Q3", 2022),
    ("2022-11-23__de-us-20221123-q4-8k__105825.md", "Q4", 2022),
    ("2023-02-17__de-us-20230217-q1-8k__105833.md", "Q1", 2023),
    ("2023-05-19__de-us-20230519-q2-8k__105839.md", "Q2", 2023),
    ("2023-08-18__de-us-20230818-q3-8k__105829.md", "Q3", 2023),
    ("2023-11-22__de-us-20231122-q4-8k__105823.md", "Q4", 2023),
    ("2024-02-15__de-us-20240215-q1-8k__105824.md", "Q1", 2024),
    ("2024-05-16__de-us-20240516-q2-8k__105819.md", "Q2", 2024),
    ("2024-08-15__de-us-20240815-q3-8k__105836.md", "Q3", 2024),
    ("2024-11-21__de-us-20241121-q4-8k__105840.md", "Q4", 2024),
    ("2025-02-13__de-us-20250213-q1-8k__105841.md", "Q1", 2025),
    ("2025-05-15__de-us-20250515-q2-8k__105808.md", "Q2", 2025),
    ("2025-08-15__de-us-20250815-q3-8k__143410.md", "Q3", 2025),
    ("2025-11-26__de-us-20251126-q4-8k__361233.md", "Q4", 2025),
    ("2026-02-19__de-us-20260219-q1-8k__603009.md", "Q1", 2026),
    ("2026-05-21__de-us-20260521-q2-8k__1042167.md", "Q2", 2026),
]

CROSSCHECK_10Q = [
    "2021-02-19__de-us-20210219-q1-10q__105814.md",
    "2021-05-21__de-us-20210521-q2-10q__105821.md",
    "2021-08-20__de-us-20210820-q3-10q__105837.md",
    "2022-02-18__de-us-20220218-q1-10q__105834.md",
    "2022-05-20__de-us-20220520-q2-10q__105838.md",
    "2022-08-19__de-us-20220819-q3-10q__105818.md",
    "2023-02-17__de-us-20230217-q1-10q__105813.md",
    "2023-05-19__de-us-20230519-q2-10q__105852.md",
    "2023-08-18__de-us-20230818-q3-10q__105835.md",
    "2024-02-15__de-us-20240215-q1-10q__105826.md",
    "2024-05-16__de-us-20240516-q2-10q__105820.md",
    "2024-08-15__de-us-20240815-q3-10q__105828.md",
    "2025-02-13__de-us-20250213-q1-10q__105832.md",
    "2025-05-15__de-us-20250515-q2-10q__105831.md",
    "2025-08-14__de-us-20250814-q3-10q__155834.md",
    "2026-02-19__de-us-20260219-q1-10q__648937.md",
    "2026-05-21__de-us-20260521-q2-10q__1055929.md",
    "2026-05-28__de-us-20260528-q2-10q__1055932.md",
    "2021-11-24__de-us-20211124-q4-10k__131650.md",
    "2022-11-23__de-us-20221123-q4-10k__105816.md",
    "2023-11-22__de-us-20231122-q4-10k__105844.md",
    "2024-11-21__de-us-20241121-q4-10k__105810.md",
    "2025-11-26__de-us-20251126-q4-10k__469216.md",
]


def parse_asu_10k_annual(path):
    """FY2025 10-K (post ASU 2023-07) annual segment table: a transposed table with
    '| PPA | SAT | CF | FS | Total' header and per-year sub-header rows.
    Returns {(fy, seg, metric): value}."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    out = {}
    year = None
    active = False
    for ln in lines:
        c = cells(ln)
        if not c:
            continue
        head = [t.strip() for t in c[:5]]
        if head[:4] == ["PPA", "SAT", "CF", "FS"]:
            active = True
            continue
        if not active:
            continue
        lab = norm_label(c[0])
        if re.fullmatch(r"\d{4}", c[0].strip()) and len(c) <= 2:
            year = int(c[0].strip())
            continue
        metric = None
        if lab == "external net sales":
            metric = "net_sales"
        elif lab == "segment operating profit":
            metric = "operating profit".replace(" ", "_")
        if metric is None or year is None:
            continue
        nums = [to_num(t) for t in c[1:] if NUM_RE.match(t)]
        nums = [n for n in nums if n is not None]
        if len(nums) >= 4:
            for seg, v in zip(("ppa", "sat", "cf"), nums[:3]):
                out[(year, seg, metric)] = v
    return out


FY2021_10K = "2021-11-24__de-us-20211124-q4-10k__131650.md"
FY_END = {2019: "2019-11-03", 2020: "2020-11-01", 2021: "2021-10-31"}


def parse_fy2021_10k_annual():
    """FY2021 10-K OPERATING SEGMENTS tables: annual FY2021 / FY2020 / FY2019 on the
    modern three-segment basis. FY2019 and FY2020 are RESTATED (recast) comparatives."""
    path = os.path.join(FILINGS, FY2021_10K)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    out = {}
    for i, ln in enumerate(lines):
        c = cells(ln)
        if not c or norm_label(c[0]) != "operating segments":
            continue
        if [t.strip() for t in c[1:4]] != ["2021", "2020", "2019"]:
            continue
        section = None
        for ln2 in lines[i + 1:i + 20]:
            if not ln2.lstrip().startswith("|"):
                break
            c2 = cells(ln2)
            if not c2:
                continue
            lab = norm_label(c2[0])
            if lab == "operating profit":
                section = "operating_profit"
                continue
            if lab.startswith("net sales and revenues"):
                section = "net_sales"
                continue
            seg = seg_of(lab)
            if seg is None or section is None:
                continue
            nums = [to_num(t) for t in c2[1:] if NUM_RE.match(t)]
            nums = [n for n in nums if n is not None]
            if len(nums) >= 3:
                for fy, v in zip((2021, 2020, 2019), nums[:3]):
                    out[(fy, seg, section)] = v
    return out


def main():
    # obs[(series_id, period_end)] = dict(value, source, notes, restated, kind)
    primary = {}      # as-reported current-quarter values (authoritative)
    comparative = {}  # prior-year-quarter values pulled from the same releases
    annual = {}       # (series_id, period_end) -> record, fiscal_quarter = FY
    audit = []

    for fname, q, fy in MODERN_8K:
        path = os.path.join(FILINGS, fname)
        res = parse_8k_segment_table(path)
        if res is None:
            print(f"WARN: no segment table in {fname}", file=sys.stderr)
            continue
        cur_end, prior_end = res["cur_end"], res["prior_end"]
        if cur_end is None:
            print(f"WARN: no dates in {fname}", file=sys.stderr)
            continue
        for (seg, metric), nums in sorted(res["rows"].items()):
            if len(nums) not in (3, 6):
                print(f"WARN: {fname} {seg}/{metric} unexpected cell count {len(nums)}: {nums}",
                      file=sys.stderr)
            if len(nums) < 3:
                continue
            cur, prior, pct = nums[0], nums[1], nums[2]
            # arithmetic check against the filing's own % change column
            if prior:
                calc = round((cur - prior) / abs(prior) * 100)
                audit.append((fname, seg, metric, cur, prior, pct, calc,
                              abs(calc - pct) <= 1))
            sid = f"{SEG_KEYS[seg]}_{metric}"
            primary[(sid, cur_end)] = {
                "value": cur, "fy": fy, "q": q,
                "source": res["src"],
                "restated": "as-reported",
            }
            pq = quarter_of(prior_end)
            pfy = fiscal_of(prior_end)
            comparative.setdefault((sid, prior_end), []).append({
                "value": prior, "fy": pfy, "q": pq, "source": res["src"],
            })
            # Q4 releases carry "Years Ended" columns -> annual observations
            if q == "Q4" and len(nums) == 6:
                annual[(sid, cur_end)] = {
                    "value": nums[3], "fy": fy, "q": "FY", "source": res["src"],
                    "restated": "as-reported",
                }
                pfy_end = prior_end
                if (sid, pfy_end) not in annual:
                    annual[(sid, pfy_end)] = {
                        "value": nums[4], "fy": fiscal_of(prior_end), "q": "FY",
                        "source": res["src"],
                        "restated": "restated" if fy == 2021 else "as-reported",
                    }

    # ---- restated FY2020 comparatives: keep only those with no as-reported modern value
    restated_rows = {}
    for (sid, pe), lst in comparative.items():
        if (sid, pe) in primary:
            continue
        vals = sorted({x["value"] for x in lst})
        restated_rows[(sid, pe)] = {
            "value": vals[0], "fy": lst[0]["fy"], "q": lst[0]["q"],
            "source": lst[0]["source"], "restated": "restated",
            "conflict": len(vals) > 1, "allvals": vals,
        }

    # ---- consistency of comparatives against the as-reported value one year earlier
    disagreements = []
    for (sid, pe), lst in comparative.items():
        if (sid, pe) in primary:
            p = primary[(sid, pe)]["value"]
            for x in lst:
                if abs(x["value"] - p) > 0.5:
                    disagreements.append((sid, pe, p, x["value"], x["source"]))

    # ---- restated FY2019/FY2020 annuals from the FY2021 10-K
    tenk = parse_fy2021_10k_annual()
    tenk_src = os.path.join("filings", FY2021_10K)
    for (fy, seg, metric), v in sorted(tenk.items()):
        sid = f"{SEG_KEYS[seg]}_{metric}"
        pe = FY_END[fy]
        if (sid, pe) in annual:
            continue
        annual[(sid, pe)] = {
            "value": v, "fy": fy, "q": "FY", "source": tenk_src,
            "restated": "as-reported" if fy == 2021 else "restated",
        }

    # cross-check the 10-K annuals against the Q4 8-K annuals
    tenk_x = []
    for (fy, seg, metric), v in sorted(tenk.items()):
        sid = f"{SEG_KEYS[seg]}_{metric}"
        pe = FY_END[fy]
        if (sid, pe) in annual and annual[(sid, pe)]["source"] != tenk_src:
            tenk_x.append((fy, sid, annual[(sid, pe)]["value"], v,
                           abs(annual[(sid, pe)]["value"] - v) < 0.5))

    # ---- 10-Q / 10-K segment-footnote cross-check (independent of the 8-K tables)
    xcheck = []
    for fname in CROSSCHECK_10Q:
        path = os.path.join(FILINGS, fname)
        if not os.path.exists(path):
            continue
        got = parse_legacy_segment_footnote(path)
        got.update(parse_asu_segment_footnote(path))
        if not got:
            xcheck.append((fname, "NO-TABLE", None, None, None, None))
            continue
        for (pe, seg, metric), v in sorted(got.items()):
            sid = f"{SEG_KEYS[seg]}_{metric}"
            key = (sid, pe)
            ref = primary.get(key) or restated_rows.get(key)
            if ref is None:
                continue
            xcheck.append((fname, sid, pe, ref["value"], v,
                           abs(v - ref["value"]) < 0.5))

    # ------------------------------------------------------------------ assemble records
    SEGNAME = {"de_ppa": "Production & Precision Ag",
               "de_sat": "Small Agriculture & Turf",
               "de_cf": "Construction & Forestry"}

    def prefix_of(sid):
        return sid[:6] if sid.startswith("de_ppa") or sid.startswith("de_sat") else "de_cf"

    recs = []  # (series_id, period_end, fy, q, value, units, source_type, source, notes)

    def add(sid, pe, fy, q, value, units, stype, src, notes):
        recs.append({"series_id": sid, "period_end": pe, "fiscal_year": fy,
                     "fiscal_quarter": q,
                     "value": (f"{value:.0f}" if units == "USDm" else f"{value:.2f}"),
                     "units": units, "source_type": stype, "source": src,
                     "notes": notes})

    combined = {}
    for k, v in restated_rows.items():
        combined[(k[0], k[1], v["q"])] = v
    for k, v in primary.items():
        combined[(k[0], k[1], v["q"])] = v
    for (sid, pe), v in annual.items():
        combined[(sid, pe, "FY")] = v

    for (sid, pe, q) in sorted(combined, key=lambda k: (k[1], k[2], k[0])):
        rec = combined[(sid, pe, q)]
        pfx = prefix_of(sid)
        metric = "net sales" if sid.endswith("net_sales") else "operating profit"
        if rec["restated"] == "restated":
            note = (f"segment_basis=modern-PPA; as_reported_or_restated=restated; "
                    f"{SEGNAME[pfx]} {metric}; comparative recast onto the FY2021 "
                    f"three-segment basis (PPA/SAT/CF); originally reported under the "
                    f"legacy-AT single Agriculture & Turf segment")
        else:
            note = (f"segment_basis=modern-PPA; as_reported_or_restated=as-reported; "
                    f"{SEGNAME[pfx]} {metric}")
        if q == "FY":
            note += "; annual (four-quarter) figure, not a quarter"
        add(sid, pe, rec["fy"], q, rec["value"], "USDm", "filing", rec["source"], note)

    # derived operating margin
    for (sid, pe, q) in sorted(combined, key=lambda k: (k[1], k[2], k[0])):
        if not sid.endswith("operating_profit"):
            continue
        pfx = prefix_of(sid)
        skey = (pfx + "_net_sales", pe, q)
        if skey not in combined:
            continue
        rec = combined[(sid, pe, q)]
        sales = combined[skey]["value"]
        if not sales:
            continue
        note = (f"segment_basis=modern-PPA; as_reported_or_restated={rec['restated']}; "
                f"{SEGNAME[pfx]} operating margin; derived = {pfx}_operating_profit / "
                f"{pfx}_net_sales * 100 (denominator is external segment net sales as "
                f"presented in the earnings-release segment table)")
        if q == "FY":
            note += "; annual figure, not a quarter"
        add(pfx + "_operating_margin", pe, rec["fy"], q,
            rec["value"] / sales * 100.0, "percent", "inference", rec["source"], note)

    recs.sort(key=lambda r: (r["period_end"], r["fiscal_quarter"], r["series_id"]))

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["series_id", "period_end", "fiscal_year",
                                           "fiscal_quarter", "value", "units",
                                           "source_type", "source", "notes"])
        w.writeheader()
        for r in recs:
            w.writerow(r)

    # ------------------------------------------------------------------ validation report
    print(f"rows written: {len(recs)} -> {OUT_CSV}\n")

    n_ok = sum(1 for a in audit if a[7])
    print(f"[1] internal %-change check (filing's own % column vs recomputed): "
          f"{n_ok}/{len(audit)} agree within 1pp")
    for a in audit:
        if not a[7]:
            print("    MISMATCH:", a)

    print(f"\n[2] prior-year comparative column vs the as-reported value one year "
          f"earlier: {len(disagreements)} disagreement(s)")
    for d in disagreements:
        print("   ", d)

    ok = sum(1 for x in xcheck if x[-1] is True)
    bad = [x for x in xcheck if x[-1] is not True]
    print(f"\n[3] 10-Q / 10-K segment-footnote cross-check vs 8-K press release: "
          f"{ok} agree, {len(bad)} disagree/absent")
    for b in bad:
        print("   ", b)

    ok3 = sum(1 for x in tenk_x if x[-1])
    print(f"\n[4] FY2021 10-K annual segment table vs Q4 8-K 'Years Ended' columns: "
          f"{ok3}/{len(tenk_x)} agree")
    for x in tenk_x:
        if not x[-1]:
            print("    MISMATCH:", x)

    # [4b] FY2025 10-K (post ASU 2023-07) annual table vs Q4 8-K annual columns
    fy25 = parse_asu_10k_annual(os.path.join(FILINGS, "2025-11-26__de-us-20251126-q4-10k__469216.md"))
    FYEND25 = {2023: "2023-10-29", 2024: "2024-10-27", 2025: "2025-11-02"}
    x4b = []
    for (fy, seg, metric), v in sorted(fy25.items()):
        sid = f"{SEG_KEYS[seg]}_{metric}"
        pe = FYEND25.get(fy)
        if pe and (sid, pe) in annual:
            a = annual[(sid, pe)]["value"]
            x4b.append((fy, sid, a, v, abs(a - v) < 0.5))
    print(f"\n[4b] FY2025 10-K annual segment table (ASU 2023-07 presentation) vs Q4 8-K "
          f"annual columns: {sum(1 for x in x4b if x[-1])}/{len(x4b)} agree")
    for x in x4b:
        if not x[-1]:
            print("    MISMATCH:", x)

    # [5] quarters must sum to the fiscal year
    print("\n[5] four-quarter sum vs reported annual "
          "(ROUND = 1 USDm apart, i.e. rounding of independently rounded quarters):")
    nb = []
    qmap = defaultdict(dict)
    for (sid, pe, q) in combined:
        if q == "FY":
            continue
        qmap[(sid, fiscal_of_fy(pe))][q] = combined[(sid, pe, q)]["value"]
    for (sid, pe, q) in sorted(combined):
        if q != "FY":
            continue
        fy = combined[(sid, pe, q)]["fy"]
        qs = qmap.get((sid, fy), {})
        if len(qs) == 4:
            s = sum(qs.values())
            a = combined[(sid, pe, q)]["value"]
            d = abs(s - a)
            mark = "OK  " if d < 0.5 else ("ROUND" if d <= 1.5 else "DIFF")
            nb.append((mark, sid, fy, s, a))
            print(f"    {mark} {sid} FY{fy}: sum(Q1..Q4)={s:.0f} reported={a:.0f}")

    print(f"    -> exact={sum(1 for x in nb if x[0]=='OK  ')}, "
          f"off-by-one(rounding)={sum(1 for x in nb if x[0]=='ROUND')}, "
          f"real differences={sum(1 for x in nb if x[0]=='DIFF')}")

    # [6] basis-bridge: legacy-AT FY2019 (as reported in the FY2019 Q4 8-K) must equal
    # restated PPA + SAT, and legacy CF must equal restated CF, if the FY2021 split was a
    # clean partition of Agriculture & Turf with no reallocation.
    LEGACY_FY2019 = {  # from filings/2019-11-27__de-us-20191127-q4-8k__469218.md
        ("at", "net_sales"): 23666.0, ("at", "operating_profit"): 2506.0,
        ("cf", "net_sales"): 11220.0, ("cf", "operating_profit"): 1215.0,
    }
    print("\n[6] legacy-AT -> modern-PPA basis bridge at FY2019 (annual):")
    pe19 = FY_END[2019]
    for metric in ("net_sales", "operating_profit"):
        ppa = annual.get((f"de_ppa_{metric}", pe19), {}).get("value")
        sat = annual.get((f"de_sat_{metric}", pe19), {}).get("value")
        cf = annual.get((f"de_cf_{metric}", pe19), {}).get("value")
        if None in (ppa, sat, cf):
            continue
        la = LEGACY_FY2019[("at", metric)]
        lc = LEGACY_FY2019[("cf", metric)]
        print(f"    {metric}: legacy A&T {la:.0f} vs restated PPA+SAT {ppa + sat:.0f} "
              f"-> {'OK' if abs(la - ppa - sat) < 0.5 else 'DIFF'};  "
              f"legacy CF {lc:.0f} vs restated CF {cf:.0f} "
              f"-> {'OK' if abs(lc - cf) < 0.5 else 'DIFF'}")

    per_series = defaultdict(list)
    for r in recs:
        per_series[r["series_id"]].append((r["period_end"], r["fiscal_quarter"]))
    print("\n[7] series coverage:")
    for s in sorted(per_series):
        pe = sorted(per_series[s])
        nq = sum(1 for x in pe if x[1] != "FY")
        print(f"    {s}: n={len(pe)} (quarterly={nq}, annual={len(pe)-nq}) "
              f"{pe[0][0]} .. {pe[-1][0]}")


def fiscal_of_fy(period_end_iso):
    """Fiscal year a QUARTER end belongs to. Deere FY ends late Oct / early Nov, so a
    period ending in November belongs to the fiscal year of that same calendar year."""
    return int(period_end_iso.split("-")[0])


if __name__ == "__main__":
    main()
