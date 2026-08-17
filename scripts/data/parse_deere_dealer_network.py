#!/usr/bin/env python3
"""
Extract Deere & Company dealer-network structure metrics from the offline corpus.

Primary source: the Item 1 "Business / Distribution" paragraph of each 10-K, which
states the approximate number of independent dealer LOCATIONS in the U.S. and Canada,
split by ag / construction-and-forestry / roadbuilding-only / turf-only.

IMPORTANT DEFINITIONAL BREAK: FY2015-FY2017 10-Ks report a TOTAL that INCLUDES
turf-only locations (e.g. FY2017: 1,532 ag + 424 C&F + 403 turf-only = 2,359).
From FY2018 the headline total EXCLUDES turf-only locations (and from FY2021 also
excludes roadbuilding-only). The raw totals are therefore NOT comparable across the
FY2017/FY2018 boundary. We emit both the as-reported total and a restated
"core (ag + C&F)" total that IS comparable across the whole period.

Usage: python3 parse_deere_dealer_network.py
Writes a summary table to stdout; the CSV is assembled by hand from this output
plus non-corpus sources.
"""

import os
import re
import glob

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"

# The distribution paragraph, in its several phrasings across years.
PARA_RE = re.compile(
    r"(?:Through (?:these )?(?:the )?U\.S\.(?: and)? (?:and )?Canad(?:a|ian)[^.]*?"
    r"markets? products to approximately[^\n]{0,2500})",
    re.IGNORECASE,
)

TOTAL_RE = re.compile(r"approximately ([\d,]+) (?:independent )?dealer locations", re.I)
AG_RE = re.compile(r"approximately ([\d,]+) sell agricultural equipment", re.I)
CF_RE = re.compile(r"approximately ([\d,]+) sell construction", re.I)
RB_RE = re.compile(r"approximately ([\d,]+) roadbuilding-only locations", re.I)
TURF_RE = re.compile(r"about ([\d,]+) turf-only locations", re.I)


def n(s):
    return int(s.replace(",", "")) if s else None


def fiscal_year_from_path(p):
    """10-K filed in Nov/Dec of calendar year Y reports fiscal year Y."""
    base = os.path.basename(p)
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})__", base)
    y, mo = int(m.group(1)), int(m.group(2))
    # Deere FY ends late Oct/early Nov; 10-K filed Nov/Dec same calendar year.
    return y if mo >= 11 else y - 1


def main():
    rows = {}
    files = sorted(glob.glob(os.path.join(CORPUS, "filings", "*10k*.md")))
    for path in files:
        txt = open(path, encoding="utf-8", errors="replace").read()
        # Use the LAST (fullest) occurrence: the corpus repeats the paragraph, and
        # early occurrences are sometimes line-wrapped/truncated by the conversion.
        best = None
        for m in PARA_RE.finditer(txt):
            chunk = txt[m.start(): m.start() + 2500]
            cand = dict(
                total=n(TOTAL_RE.search(chunk).group(1)) if TOTAL_RE.search(chunk) else None,
                ag=n(AG_RE.search(chunk).group(1)) if AG_RE.search(chunk) else None,
                cf=n(CF_RE.search(chunk).group(1)) if CF_RE.search(chunk) else None,
                rb=n(RB_RE.search(chunk).group(1)) if RB_RE.search(chunk) else None,
                turf=n(TURF_RE.search(chunk).group(1)) if TURF_RE.search(chunk) else None,
            )
            score = sum(1 for v in cand.values() if v is not None)
            if best is None or score > best[0]:
                best = (score, cand)
        if best is None:
            continue
        fy = fiscal_year_from_path(path)
        c = best[1]
        # Prefer the record with the most fields if a FY appears twice (10-K + FY 10-K).
        if fy in rows and sum(1 for v in rows[fy][1].values() if v is not None) >= best[0]:
            continue
        rows[fy] = (os.path.relpath(path, CORPUS), c)

    hdr = f"{'FY':<6}{'total_rep':>10}{'ag':>7}{'cf':>7}{'rb_only':>9}{'turf_only':>11}{'core_ag_cf':>12}  source"
    print(hdr)
    print("-" * len(hdr))
    for fy in sorted(rows):
        src, c = rows[fy]
        core = (c["ag"] + c["cf"]) if (c["ag"] and c["cf"]) else None
        print(
            f"{fy:<6}{c['total'] if c['total'] else '':>10}{c['ag'] or '':>7}"
            f"{c['cf'] or '':>7}{c['rb'] or '':>9}{c['turf'] or '':>11}"
            f"{core or '':>12}  {src}"
        )

    # Reconciliation check: does reported total == ag+cf(+rb)(+turf)?
    print("\nReconciliation (reported total minus component sums):")
    for fy in sorted(rows):
        src, c = rows[fy]
        if not c["total"]:
            continue
        core = (c["ag"] or 0) + (c["cf"] or 0)
        with_turf = core + (c["turf"] or 0)
        with_all = with_turf + (c["rb"] or 0)
        print(
            f"  FY{fy}: reported {c['total']:>5} | ag+cf {core:>5} (diff {c['total']-core:>5})"
            f" | +turf {with_turf:>5} (diff {c['total']-with_turf:>5})"
            f" | +turf+rb {with_all:>5} (diff {c['total']-with_all:>5})"
        )


if __name__ == "__main__":
    main()
