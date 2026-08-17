#!/usr/bin/env python3
"""
Extract Deere & Company's ASC 606 revenue-recognition geography x segment matrix
(the "primary geographic markets" table) for one geography, from the offline
corpus of 10-Q / 10-K filings.

Two reporting bases appear in the corpus:
  * FY2019 - FY2020 as originally filed: Agriculture & Turf (AT) / CF / FS
  * FY2021 onward (and FY2020 as restated in FY2021 filings):
        PPA / SAT / CF / FS

Cumulative (6/9/12-month) tables are de-cumulated into single quarters using
the same-fiscal-year prior cumulative figure, and 3-month tables are used
directly where the filing provides one.

Usage:  python3 extract_deere_geo_canada.py [GEOGRAPHY]     # default Canada
Writes tidy CSV to stdout.
"""
import os
import re
import sys
import glob
import datetime as dt

CORPUS = ("/Users/cor/Documents/projects/agents-vs-wall-street-starter/"
          "challenge/offline-data/deere/filings")

HDR = re.compile(r"(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+"
                 r"([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})", re.I)
HDR_Y = re.compile(r"Years?\s+Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})",
                   re.I)
MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}
NMONTH = {"three": 3, "six": 6, "nine": 9, "twelve": 12}
NUM = re.compile(r"^\(?\$?\s*([\d,]+)\)?$")
# 10-K revenue note heads each annual table with a bare fiscal-year line
BARE_YEAR = re.compile(r"^\|?[\s|​]*((?:19|20)\d{2})[\s|​]*$")
# Deere fiscal-year end dates (last Sunday of Oct / first Sunday of Nov)
FYEND = {2019: dt.date(2019, 11, 3), 2020: dt.date(2020, 11, 1),
         2021: dt.date(2021, 10, 31), 2022: dt.date(2022, 10, 30),
         2023: dt.date(2023, 10, 29), 2024: dt.date(2024, 10, 27),
         2025: dt.date(2025, 11, 2)}


def parse_nums(line):
    cells = line.split("|") if "|" in line else line.split()
    out = []
    for c in cells:
        c = c.replace("​", "").strip()
        if not c or c in {"$", "-", "--"}:
            continue
        m = NUM.match(c)
        if m:
            out.append(int(m.group(1).replace(",", "")))
    return out


def fq(date):
    """Map a Deere period-end date to (fiscal_year, fiscal_quarter)."""
    q = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3,
         10: 4, 11: 4, 12: 4}[date.month]
    return date.year, q


def scan(path, geo):
    rows = []
    cur = None
    lab = re.compile(r"^\|?\s*" + re.escape(geo) + r"\s*(\||$|\s)", re.I)
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            s = line.replace("​", "").strip()
            m, my = HDR.search(s), HDR_Y.search(s)
            if m:
                mo = MONTHS.get(m.group(2).capitalize())
                if mo:
                    cur = (dt.date(int(m.group(4)), mo, int(m.group(3))),
                           NMONTH[m.group(1).lower()])
                continue
            if my:
                mo = MONTHS.get(my.group(1).capitalize())
                if mo:
                    cur = (dt.date(int(my.group(3)), mo, int(my.group(2))), 12)
                continue
            by = BARE_YEAR.match(s)
            if by and int(by.group(1)) in FYEND:
                cur = (FYEND[int(by.group(1))], 12)
                continue
            if cur and lab.match(s):
                n = parse_nums(s)
                if len(n) == 5 and n[4] == sum(n[:4]):
                    rows.append((cur[0], cur[1], "new", n))
                    cur = None
                elif len(n) == 4 and n[3] == sum(n[:3]):
                    rows.append((cur[0], cur[1], "old", n))
                    cur = None
    return rows


def collect(geo):
    """basis -> (fy, nmonths) -> (period_end, values, source)"""
    data = {"new": {}, "old": {}}
    for path in sorted(glob.glob(os.path.join(CORPUS, "*.md"))):
        for date, n, basis, vals in scan(path, geo):
            fy, _ = fq(date)
            key = (fy, n)
            # prefer the earliest-filed (as-reported) figure; restatements on
            # the "new" basis only ever appear in later filings under 'new'
            if key not in data[basis]:
                data[basis][key] = (date, vals, os.path.basename(path))
    return data


def quarterly(basis_data):
    """De-cumulate into quarters. Returns list of (fy, q, date, vals, src, note)."""
    out = []
    # index 3-month tables by their own period end
    three = {}
    for (fy, n), (date, vals, src) in basis_data.items():
        if n == 3:
            three[fq(date)] = (date, vals, src)
    for (fy, q), (date, vals, src) in sorted(three.items()):
        out.append((fy, q, date, vals, src, "3-month table (as reported)"))
    have = {(fy, q) for (fy, q) in three}
    # de-cumulate the rest
    for (fy, n), (date, vals, src) in sorted(basis_data.items()):
        if n == 3:
            continue
        q = n // 3
        if (fy, q) in have:
            continue
        prior = basis_data.get((fy, n - 3))
        if prior is None:
            continue
        qv = [a - b for a, b in zip(vals, prior[1])]
        out.append((fy, q, date, qv, src,
                    f"{n}mo less {n-3}mo (from {prior[2]})"))
        have.add((fy, q))
    return sorted(out, key=lambda r: (r[0], r[1]))


if __name__ == "__main__":
    geo = sys.argv[1] if len(sys.argv) > 1 else "Canada"
    data = collect(geo)
    print("basis,fiscal_year,fiscal_quarter,period_end,s1,s2,s3,s4,total,source,derivation")
    for basis in ("old", "new"):
        cols = 5 if basis == "new" else 4
        for fy, q, date, vals, src, note in quarterly(data[basis]):
            v = list(vals)
            if basis == "old":       # AT, CF, FS, Total -> pad
                v = [v[0], "", v[1], v[2], v[3]]
            print(f"{basis},{fy},Q{q},{date}," +
                  ",".join(str(x) for x in v) + f",{src},{note}")
