#!/usr/bin/env python3
"""
Estimate the historical relationship between each region's drivers and Deere's
revenue in that region, using the rev-rec geography matrix.

Design decisions that matter for whether the numbers mean anything:

  * The matrix only exists from Deere's ASC 606 adoption (FY2019) and the 10-K
    annual tables in this corpus are too mangled to net a clean standalone Q4,
    so the panel is 23 quarters, Q1-Q3 of FY2019-FY2026. There is NO Q4.
  * Quarterly equipment revenue is violently seasonal, so LEVEL correlations
    between a driver level and a revenue level mostly measure shared trend and
    shared seasonality. The headline estimate here is therefore on YEAR-OVER-YEAR
    PERCENT CHANGE for both sides, which differences out both.
  * YoY differencing costs four quarters, leaving n<=15 per region. Fifteen
    observations is not enough to establish a driver relationship. Everything
    below is reported with its n and screened for multiple comparisons.

Standard library only.
"""

import csv
import math
import os
import sys
from collections import defaultdict, OrderedDict

DATA = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere"
MATRIX = os.path.join(DATA, "de_geo_matrix.csv")
DRIVERS = os.path.join(DATA, "drv_regional.csv")

QORD = {"Q1": 0, "Q2": 1, "Q3": 2, "Q4": 3}


def qkey(fy, fq):
    return int(fy) * 4 + QORD[fq]


# ------------------------------------------------------------------ stats ---


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None, n
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        return None, n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sxx * syy), n


def _betacf(a, b, x):
    MAXIT, EPS, FPMIN = 200, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def betainc(a, b, x):
    """Regularized incomplete beta I_x(a,b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = (
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log1p(-x)
    )
    front = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def pvalue(r, n):
    """Two-tailed p for a Pearson r under the null of zero correlation."""
    if r is None or n < 4:
        return None
    if abs(r) >= 1.0:
        return 0.0
    df = n - 2
    t = r * math.sqrt(df / (1.0 - r * r))
    return betainc(df / 2.0, 0.5, df / (df + t * t))


def yoy(series):
    """{(fy,fq): v} -> {(fy,fq): pct change vs same quarter one year earlier}."""
    out = {}
    for (fy, fq), v in series.items():
        prev = series.get((fy - 1, fq))
        if prev is None or prev == 0:
            continue
        out[(fy, fq)] = (v / prev - 1.0) * 100.0
    return out


# ------------------------------------------------------------------- load ---


def load_matrix():
    """-> revenue[geo][segment or 'Total'][(fy,fq)] = USDm"""
    rev = defaultdict(lambda: defaultdict(dict))
    with open(MATRIX, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rev[r["geography"]][r["segment"]][
                (int(r["fiscal_year"]), r["fiscal_quarter"])
            ] = float(r["value"])
    return rev


def load_drivers():
    """-> drv[geo][series_id][(fy,fq)] = value, excluding partial quarters and
    rows with no fiscal quarter."""
    drv = defaultdict(lambda: defaultdict(dict))
    with open(DRIVERS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if not r["fiscal_quarter"]:
                continue
            if r["notes"].startswith("PARTIAL"):
                continue  # never mix an incomplete quarter into an estimate
            drv[r["geography"]][r["series_id"]][
                (int(r["fiscal_year"]), r["fiscal_quarter"])
            ] = float(r["value"])
    return drv


# ------------------------------------------------------------------- main ---

# Region -> which segment's revenue is the meaningful dependent variable.
# 'Total' is all four segments including financial services; PPA is the
# large-ag line that the ag drivers should actually move.
TARGETS = ["Total", "PPA"]

MAX_LAG = 4  # quarters the driver leads revenue by


def main():
    rev = load_matrix()
    drv = load_drivers()

    geos = [g for g in rev if g]
    results = []
    n_tests = 0

    for geo in sorted(geos):
        for tgt in TARGETS:
            series = rev[geo].get(tgt)
            if not series or len(series) < 8:
                continue
            rev_yoy = yoy(series)
            for sid, dser in sorted(drv.get(geo, {}).items()):
                if len(dser) < 8:
                    continue
                d_yoy = yoy(dser)
                for lag in range(0, MAX_LAG + 1):
                    xs, ys = [], []
                    for (fy, fq), rv in sorted(rev_yoy.items()):
                        k = qkey(fy, fq) - lag
                        dk = (k // 4, ["Q1", "Q2", "Q3", "Q4"][k % 4])
                        if dk in d_yoy:
                            xs.append(d_yoy[dk])
                            ys.append(rv)
                    r, n = pearson(xs, ys)
                    if r is None or n < 8:
                        continue
                    n_tests += 1
                    results.append(
                        dict(geo=geo, target=tgt, sid=sid, lag=lag, r=r, n=n,
                             p=pvalue(r, n))
                    )

    results.sort(key=lambda d: -abs(d["r"]))

    print("Deere regional driver correlations")
    print("dependent variable: YoY %% change in rev-rec revenue for the region")
    print("independent variable: YoY %% change in the driver, lagged 0-4 quarters")
    print("panel: Q1-Q3 of FY2019-FY2026, 23 quarters, no Q4 in the corpus")
    print()
    print("TOTAL TESTS RUN: %d" % n_tests)
    exp_false = n_tests * 0.05
    print("At p<0.05, pure chance alone would produce about %.0f 'significant'"
          % exp_false)
    print("results out of %d tests. Treat any single r below as a hypothesis," % n_tests)
    print("not a finding, unless it survives that arithmetic.")
    bonf = 0.05 / n_tests if n_tests else 1
    print("Bonferroni-corrected threshold for one honest claim: p < %.2g" % bonf)
    print()

    print("=" * 100)
    print("STRONGEST 30 BY |r| (all lags, all regions)")
    print("=" * 100)
    print("%-38s %-6s %-28s %3s %3s %7s %9s %s"
          % ("region", "target", "driver", "lag", "n", "r", "p", "survives Bonferroni"))
    for d in results[:30]:
        print("%-38s %-6s %-28s %3d %3d %+7.3f %9.4f %s"
              % (d["geo"][:38], d["target"], d["sid"][:28], d["lag"], d["n"],
                 d["r"], d["p"], "YES" if d["p"] < bonf else "no"))

    print()
    print("=" * 100)
    print("BEST DRIVER PER REGION x TARGET (by |r|, any lag)")
    print("=" * 100)
    best = OrderedDict()
    for d in results:
        k = (d["geo"], d["target"])
        if k not in best:
            best[k] = d
    for (geo, tgt), d in sorted(best.items()):
        print("%-38s %-6s %-28s lag=%d n=%d r=%+.3f p=%.4f"
              % (geo[:38], tgt, d["sid"], d["lag"], d["n"], d["r"], d["p"]))

    print()
    print("=" * 100)
    print("FULL RESULTS BY REGION (contemporaneous, lag 0, PPA and Total)")
    print("=" * 100)
    for geo in sorted(geos):
        rows = [d for d in results if d["geo"] == geo and d["lag"] == 0]
        if not rows:
            continue
        print("\n--- %s" % geo)
        for d in sorted(rows, key=lambda z: (z["target"], -abs(z["r"]))):
            print("   %-6s %-30s n=%2d r=%+.3f p=%.4f"
                  % (d["target"], d["sid"], d["n"], d["r"], d["p"]))

    # sample-size reality check
    print()
    print("=" * 100)
    print("SAMPLE SIZES BEHIND THE REVENUE SIDE")
    print("=" * 100)
    for geo in sorted(geos):
        s = rev[geo].get("Total", {})
        y = yoy(s)
        q3 = [k for k in y if k[1] == "Q3"]
        print("  %-40s levels n=%2d   YoY n=%2d   of which Q3 n=%d"
              % (geo[:40], len(s), len(y), len(q3)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
