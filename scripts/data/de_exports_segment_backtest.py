#!/usr/bin/env python3
"""
Backtest: do US machinery export flows track Deere SEGMENT revenue?

The geographic correlation is the wrong test for the export series. US exports
and Deere's US shipments come out of the same factories on the same production
schedules, so the series behaves as a proxy for the US ag-machinery PRODUCTION
CYCLE rather than as a geographic bridge. That is testable against segment
revenue directly:

    HS 8432 + 8433  ->  Production & Precision Ag (PPA)
    HS 8429         ->  Construction & Forestry (CF)

Everything is on year-on-year growth. Both series are strongly seasonal, so
correlations on raw levels mostly measure a shared seasonal shape and overstate
how much information is really there.

Usage:
  python3 de_exports_segment_backtest.py \
      --exports ../../data/deere/footprint/exports_trade.csv \
      --geo-matrix ../../data/deere/de_geo_matrix.csv
"""

import argparse
import collections
import csv
import math


def fiscal_quarter_months(period_end):
    """Three calendar months a Deere fiscal quarter covers. See the note in
    de_build_exports_trade.py: quarters ending in the first half of a month
    (2026-05-03) cover the THREE PRIOR months, not the period-end month."""
    y, m, d = int(period_end[:4]), int(period_end[5:7]), int(period_end[8:10])
    if d <= 15:
        m -= 1
        if m < 1:
            m += 12
            y -= 1
    out = []
    for k in range(3):
        mm, yy = m - k, y
        while mm < 1:
            mm += 12
            yy -= 1
        out.append("%04d-%02d" % (yy, mm))
    return out


def pearson(x, y):
    n = len(x)
    if n < 3:
        return None, n
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx <= 0 or syy <= 0:
        return None, n
    return sxy / math.sqrt(sxx * syy), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exports", required=True)
    ap.add_argument("--geo-matrix", required=True)
    args = ap.parse_args()

    monthly = collections.defaultdict(dict)
    for r in csv.DictReader(open(args.exports)):
        if r["metric"] == "exports_fob_monthly":
            monthly[r["series_id"][-4:]][r["date"][:7]] = float(r["value"])

    seg = collections.defaultdict(float)
    pend = {}
    for r in csv.DictReader(open(args.geo_matrix)):
        if r["segment"] in ("PPA", "SAT", "CF"):
            key = (int(r["fiscal_year"]), r["fiscal_quarter"])
            seg[key + (r["segment"],)] += float(r["value"])
            pend[key] = r["period_end"]

    def exports_for(period_end, codes, months=None):
        want = months or fiscal_quarter_months(period_end)
        tot = 0.0
        for c in codes:
            for mo in want:
                v = monthly.get(c, {}).get(mo)
                if v is None:
                    return None
                tot += v
        return tot

    pairs = {"PPA vs HS8432+8433": ("PPA", ["8432", "8433"]),
             "CF  vs HS8429": ("CF", ["8429"])}

    print("Deere segment revenue YoY vs US HS export YoY (both seasonality-free)")
    print("=" * 74)
    for label, (segment, codes) in pairs.items():
        print("\n%s" % label)
        print("  FY  Q   segment YoY    export YoY")
        xs, ys = [], []
        for (fy, q) in sorted(pend):
            cur, prev = (fy, q), (fy - 1, q)
            if prev not in pend:
                continue
            s1, s0 = seg.get(cur + (segment,)), seg.get(prev + (segment,))
            e1 = exports_for(pend[cur], codes)
            e0 = exports_for(pend[prev], codes)
            if not (s1 and s0 and e1 and e0):
                continue
            sg, eg = 100 * (s1 / s0 - 1), 100 * (e1 / e0 - 1)
            xs.append(sg)
            ys.append(eg)
            print("  %d %s   %+7.1f%%     %+7.1f%%" % (fy, q, sg, eg))
        r, n = pearson(xs, ys)
        print("  --> r = %s   n = %d" % ("%+.3f" % r if r else "n/a", n))

    # ---- live read on the open quarter -----------------------------------
    print("\n" + "=" * 74)
    print("OPEN QUARTER: Deere FY2026 Q3 (approx 4 May - 2 Aug 2026)")
    print("Calendar months May/Jun/Jul 2026. Trade data available through Jun,")
    print("so this is a TWO-THIRDS read on a quarter that has ENDED but NOT REPORTED.")
    for label, codes in (("HS8432+8433 (ag, -> PPA)", ["8432", "8433"]),
                         ("HS8429 (construction, -> CF)", ["8429"]),
                         ("HS8701 (tractors, contaminated)", ["8701"])):
        cur = exports_for(None, codes, months=["2026-05", "2026-06"])
        prev = exports_for(None, codes, months=["2025-05", "2025-06"])
        if cur and prev:
            print("  %-34s May+Jun YoY = %+6.1f%%" % (label, 100 * (cur / prev - 1)))
    print("\nPrior-quarter sanity check (Q2 FY2026, Feb-Apr 2026, ALREADY REPORTED):")
    for label, codes, actual in (("HS8432+8433 -> PPA", ["8432", "8433"], -14.0),
                                 ("HS8429 -> CF", ["8429"], +29.0)):
        cur = exports_for(None, codes, months=["2026-02", "2026-03", "2026-04"])
        prev = exports_for(None, codes, months=["2025-02", "2025-03", "2025-04"])
        if cur and prev:
            print("  %-22s export YoY = %+6.1f%%   vs reported segment %+5.1f%%"
                  % (label, 100 * (cur / prev - 1), actual))


if __name__ == "__main__":
    main()
