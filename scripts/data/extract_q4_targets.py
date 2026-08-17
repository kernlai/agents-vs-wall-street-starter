#!/usr/bin/env python3
"""
extract_q4_targets.py -- recover Deere's AS-REPORTED fourth-quarter net sales &
revenues and diluted EPS from the offline corpus Q4 8-K earnings releases.

Why this exists
---------------
Deere files no fourth-quarter 10-Q, so SEC XBRL carries no standalone three-month
Q4 fact for either target (verified: zero EarningsPerShareDiluted facts with an
80-100 day duration ending on any Deere Q4 date). Every XBRL-only pipeline has to
DERIVE Q4 as "fiscal year minus Q1+Q2+Q3".

For revenue that subtraction is right to about 1 USDm. For diluted EPS it is
simply wrong: the diluted share count differs every quarter, so full-year EPS is
not the sum of the four quarterly EPS figures. FY2025 Q4 derives to 3.92 against
an as-reported 3.93; FY2024 Q4 derives to 4.57 against an as-reported 4.55.

The Q4 8-K prints both figures directly and, per the task brief, the corpus
filings are authoritative. This script parses them and writes a small override
table that build_panel.py layers on top of the XBRL-derived values.

Output: data/deere/de_q4_actuals_from_8k.csv  (tidy long, standard 9-column header)
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.abspath(os.path.join(
    HERE, "..", "..", "challenge", "offline-data", "deere"))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "data", "deere"))

# Each Q4 8-K prints the three-month column first, then the twelve-month column.
# "Total net sales and revenues | $ 12,394 | $ 11,143 | +11 | $ 45,684 | ..."
#   -> [0] Q4 this year, [1] Q4 prior year, (pct), [3] FY this year, [4] FY prior
REV_ROW = re.compile(
    r"^\|\s*Total net sales and revenues\s*\|(.+)$", re.I | re.M)
# "| Diluted | 3.93 | 4.55 | 18.50 | 25.62 |"  (Per Share Data block)
EPS_ROW = re.compile(r"^\|\s*Diluted\s*\|(.+)$", re.I | re.M)
# "| Fully diluted EPS | $ 3.93 | $ 4.55 | | $ 18.50 | $ 25.62 | |"
EPS_HEADLINE = re.compile(r"^\|\s*Fully diluted EPS\s*\|(.+)$", re.I | re.M)

# Deere's older releases print sub-dollar EPS with no leading zero ("$ .90"),
# so the leading-dot form must be accepted. Without it the parser skips the
# current-year cell and silently reports the prior-year comparative instead --
# which is exactly the failure this regex was first written with.
NUMBER = re.compile(r"-?(?:\d[\d,]*(?:\.\d+)?|\.\d+)")

# fiscal year -> (period_end, filing) for every Q4 8-K in the corpus
Q4_FILES = {}


def cells(line):
    out = []
    for c in line.split("|"):
        c = c.strip().replace("$", "").replace("&nbsp;", "").strip()
        m = NUMBER.fullmatch(c)
        out.append(float(m.group(0).replace(",", "")) if m else None)
    return out


def first_numbers(line, k):
    """The first k numeric cells of a markdown table row."""
    return [c for c in cells(line) if c is not None][:k]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=CORPUS)
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    fdir = os.path.join(args.corpus, "filings")
    files = sorted(f for f in os.listdir(fdir) if re.search(r"q4-8k", f))
    if not files:
        sys.exit("no Q4 8-K files found in %s" % fdir)

    rows = []
    for fn in files:
        path = os.path.join(fdir, fn)
        text = open(path, encoding="utf-8", errors="replace").read()
        fy_filed = int(fn[:4])           # the 8-K is filed in Nov of the FY it reports

        # period end: "for the fourth quarter ended November 2, 2025".
        # The FY2015 and FY2016 releases drop the year ("ended October 31,"),
        # which is unambiguous because the release is filed weeks later.
        import datetime as dt
        pe = None
        m = re.search(r"fourth quarter ended (\w+ \d{1,2}, \d{4})", text, re.I)
        if m:
            pe = dt.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()
        else:
            m = re.search(r"fourth quarter ended (\w+ \d{1,2})\b", text, re.I)
            if m:
                pe = dt.datetime.strptime("%s, %d" % (m.group(1), fy_filed),
                                          "%B %d, %Y").date().isoformat()

        rev = eps = None
        mm = REV_ROW.search(text)
        if mm:
            n = first_numbers(mm.group(1), 1)
            if n:
                rev = n[0]

        mm = EPS_HEADLINE.search(text) or EPS_ROW.search(text)
        if mm:
            n = first_numbers(mm.group(1), 1)
            if n:
                eps = n[0]

        # Prose fallback for the older releases, which carry no Per Share Data
        # markdown table: "...was $351.2 million, or $1.08 per share, for the
        # fourth quarter ended October 31..." and "Worldwide net sales and
        # revenues decreased 25 percent, to $6.715 billion, for the fourth
        # quarter".
        if eps is None:
            m = re.search(r"or \$([\d.]+) per share, for the fourth quarter", text, re.I)
            if m:
                eps = float(m.group(1))
        if rev is None:
            m = re.search(r"Worldwide net sales and revenues [^.]*?to \$([\d.]+) billion, "
                          r"for the fourth quarter", text, re.I)
            if m:
                rev = round(float(m.group(1)) * 1000.0, 3)

        # cross-check the two EPS presentations against each other where both exist
        a, b = EPS_HEADLINE.search(text), EPS_ROW.search(text)
        note_eps = "as-reported three-month diluted EPS from the Q4 8-K"
        if a and b:
            va = first_numbers(a.group(1), 1)
            vb = first_numbers(b.group(1), 1)
            if va and vb:
                if abs(va[0] - vb[0]) < 1e-9:
                    note_eps += "; headline table and Per Share Data block agree (%.2f)" % va[0]
                else:
                    note_eps += "; DISAGREEMENT headline=%s per-share-block=%s, kept headline" \
                                % (va[0], vb[0])

        if pe is None:
            print("  [skip] %s: no 'fourth quarter ended' date" % fn, file=sys.stderr)
            continue
        fy = fy_filed
        if rev is not None:
            rows.append(["de_net_sales_revenues_total_q4_asreported", pe, fy, "Q4",
                         rev, "USDm", "filing", "filings/" + fn,
                         "as-reported three-month total net sales and revenues from the Q4 8-K; "
                         "authoritative over the XBRL FY-minus-nine-months derivation"])
        if eps is not None:
            rows.append(["de_eps_diluted_gaap_q4_asreported", pe, fy, "Q4",
                         eps, "USD/share", "filing", "filings/" + fn, note_eps])
        print("FY%d Q4 (%s): revenue=%s  diluted EPS=%s" % (fy, pe, rev, eps))

    out_path = os.path.join(args.out, "de_q4_actuals_from_8k.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["series_id", "period_end", "fiscal_year", "fiscal_quarter",
                    "value", "units", "source_type", "source", "notes"])
        w.writerows(rows)
    print("\nwrote %d rows -> %s" % (len(rows), out_path))


if __name__ == "__main__":
    main()
