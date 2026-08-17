#!/usr/bin/env python3
"""Peer read-across analysis: does any peer's revenue growth lead Deere's?

Reads the published tidy CSV (so the analysis is reproducible from the
deliverable itself, not from an intermediate).

Method
------
* Peers run different fiscal calendars, so each quarterly observation is mapped
  to the CALENDAR quarter containing the period MIDPOINT (approximated as
  period_end - 45 days; every observation here is a ~91-day quarter). This is an
  alignment key for the correlation only -- the CSV keeps each issuer's true
  period_end and its own fiscal labels.
* Growth is YoY: g[t] = rev[t]/rev[t-4] - 1, on the calendar-quarter index. YoY
  differencing removes seasonality, which matters enormously here (Deere Q1 and
  Titan Q1 are both seasonal troughs).
* r(k) = Pearson corr( peer_g[t-k], deere_g[t] ). k > 0 means the peer's number
  from k quarters EARLIER lines up with Deere now, i.e. the peer LEADS.
* Two windows: full common history, and the last 20 calendar quarters.
* Overlapping YoY windows are serially correlated, so nominal p-values are
  optimistic. A non-overlapping annual-growth correlation is reported as a
  robustness check.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from datetime import date, timedelta

QS = ("Q1", "Q2", "Q3", "Q4")


def dt(s):
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def cq_index(period_end):
    """Calendar-quarter index from the period midpoint (end - 45 days)."""
    mid = dt(period_end) - timedelta(days=45)
    return mid.year * 4 + (mid.month - 1) // 3


def cq_name(i):
    return "%dQ%d" % (i // 4, i % 4 + 1)


def pearson(xs, ys):
    n = len(xs)
    if n < 4:
        return None, n, None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0 or syy <= 0:
        return None, n, None
    r = sxy / math.sqrt(sxx * syy)
    r = max(-0.999999, min(0.999999, r))
    p = None
    if n > 3:
        z = 0.5 * math.log((1 + r) / (1 - r)) * math.sqrt(n - 3)
        p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return r, n, p


def yoy(series):
    """{idx: value} -> {idx: growth}"""
    return {t: series[t] / series[t - 4] - 1
            for t in series if (t - 4) in series and series[t - 4]}


def selftest():
    """Pin the sign convention: construct a peer that genuinely leads by 1 quarter
    and assert the search recovers k=+1."""
    import random
    random.seed(7)
    shock = {t: random.gauss(0, 1) for t in range(8000, 8100)}
    de_g = {t: shock[t] for t in shock}
    peer_g = {t: shock[t + 1] for t in shock if (t + 1) in shock}   # peer moves 1q EARLY
    best = None
    for k in range(-4, 5):
        xs = [peer_g[t - k] for t in sorted(de_g) if (t - k) in peer_g]
        ys = [de_g[t] for t in sorted(de_g) if (t - k) in peer_g]
        r, n, _ = pearson(xs, ys)
        if r is not None and (best is None or r > best[0]):
            best = (r, k)
    assert best[1] == 1 and best[0] > 0.99, "sign convention broken: %r" % (best,)
    return "sign-convention self-test PASSED (synthetic 1q-early peer recovered as k=+1)"


def ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((a - mx) ** 2 for a in xs)
    if sxx <= 0:
        return None
    b = sum((a - mx) * (c - my) for a, c in zip(xs, ys)) / sxx
    a0 = my - b * mx
    resid = [c - (a0 + b * a) for a, c in zip(xs, ys)]
    se = math.sqrt(sum(e * e for e in resid) / max(n - 2, 1))
    return a0, b, se, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--base", default="de")
    ap.add_argument("--recent", type=int, default=20)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.csv)))

    q = defaultdict(dict)     # company -> {cq_idx: revenue}
    a = defaultdict(dict)     # company -> {fiscal_year: revenue}
    for r in rows:
        if not r["series_id"].endswith("_revenue") or not r["value"]:
            continue
        comp = r["series_id"][: -len("_revenue")]
        v = float(r["value"])
        if r["fiscal_quarter"] in QS:
            q[comp][cq_index(r["period_end"])] = v
        elif r["fiscal_quarter"] == "FY":
            a[comp][int(r["fiscal_year"])] = v

    # Kubota is reported in JPY; growth rates are still comparable (unit-free),
    # but the caveat matters and is flagged in the output.
    base = args.base
    gq = {c: yoy(s) for c, s in q.items()}
    ga = {c: {y: s[y] / s[y - 1] - 1 for y in s if (y - 1) in s and s[y - 1]}
          for c, s in a.items()}

    latest = max(gq[base])
    cut = latest - args.recent + 1

    print(selftest())
    print("=" * 96)
    print("DEERE PEER READ-ACROSS -- YoY quarterly revenue growth, calendar-quarter aligned")
    print("base = %s ; latest aligned calendar quarter for base = %s" % (base, cq_name(latest)))
    print("r(k) = corr(peer_g[t-k], deere_g[t]);  k>0 => peer LEADS Deere by k quarters")
    print("=" * 96)

    hdr = ("%-9s | %-28s | %-28s | %s" %
           ("peer", "FULL: contemporaneous r (n)", "FULL: best lag  r (n) [k]",
            "LAST %d Q: contemp r (n) | best lag" % args.recent))
    print(hdr)
    print("-" * len(hdr))

    results = {}
    for comp in sorted(gq):
        if comp == base:
            continue
        row = {"peer": comp}
        for label, lo in (("full", None), ("recent", cut)):
            dg = {t: v for t, v in gq[base].items() if lo is None or t >= lo}
            best = None
            contemp = None
            for k in range(-4, 5):
                xs, ys = [], []
                for t in sorted(dg):
                    if (t - k) in gq[comp]:
                        xs.append(gq[comp][t - k])
                        ys.append(dg[t])
                r, n, p = pearson(xs, ys)
                if r is None:
                    continue
                if k == 0:
                    contemp = (r, n, p)
                if n >= (8 if label == "full" else 6) and (best is None or abs(r) > abs(best[0])):
                    best = (r, n, p, k)
            row[label] = {"contemp": contemp, "best": best}
        # annual, non-overlapping robustness check
        yrs = sorted(set(ga.get(comp, {})) & set(ga.get(base, {})))
        xs = [ga[comp][y] for y in yrs]
        ys = [ga[base][y] for y in yrs]
        row["annual"] = pearson(xs, ys)
        results[comp] = row

        def fmt(d):
            c = d["contemp"]
            b = d["best"]
            cs = "r=%+.3f (n=%d)%s" % (c[0], c[1], "*" if c[2] is not None and c[2] < 0.05 else " ") if c else "n/a"
            bs = "r=%+.3f (n=%d) k=%+d" % (b[0], b[1], b[3]) if b else "n/a"
            return cs, bs
        cf, bf = fmt(row["full"])
        cr, br = fmt(row["recent"])
        print("%-9s | %-28s | %-28s | %-22s | %s" % (comp, cf, bf, cr, br))

    print()
    print("Annual (non-overlapping) FY revenue growth correlation vs Deere FY growth:")
    print("  NOTE: each company's own fiscal year; Deere FY ends late Oct, so a Deere FY")
    print("        is roughly the calendar year ending one quarter earlier than a Dec filer's.")
    for comp in sorted(results):
        r, n, p = results[comp]["annual"]
        if r is None:
            print("    %-9s  n=%d  (too few overlapping years)" % (comp, n))
        else:
            print("    %-9s  r=%+.3f  n=%2d  p=%.4f" % (comp, r, n, p))

    print()
    print("Full lag profiles (r by k, full history) -- k>0 = peer leads:")
    ks = list(range(-4, 5))
    print("    %-9s %s" % ("peer", " ".join("%+d".rjust(7) % k for k in ks)))
    for comp in sorted(gq):
        if comp == base:
            continue
        cells = []
        for k in ks:
            xs, ys = [], []
            for t in sorted(gq[base]):
                if (t - k) in gq[comp]:
                    xs.append(gq[comp][t - k])
                    ys.append(gq[base][t])
            r, n, _ = pearson(xs, ys)
            cells.append("%+.2f" % r if r is not None else "  .  ")
        print("    %-9s %s" % (comp, " ".join(c.rjust(7) for c in cells)))

    print()
    print("Data availability right now (2026-08-16): latest aligned calendar quarter per company")
    for comp in sorted(q):
        print("    %-9s %s   (n quarters = %d)" % (comp, cq_name(max(q[comp])), len(q[comp])))

    # ------------------------------------------------------------------ nowcast
    target = latest + 1   # the calendar quarter Deere has not yet reported
    print()
    print("=" * 96)
    print("NOWCAST INPUTS for Deere's unreported quarter (aligned calendar quarter %s)"
          % cq_name(target))
    print("Deere FY2026 Q3 runs approx 2026-05-04..2026-08-02, midpoint mid-June -> %s."
          % cq_name(target))
    print("Peers that have ALREADY reported an overlapping quarter, with their YoY growth,")
    print("and the Deere growth each one implies via a univariate OLS fitted at its best lag:")
    print("%-9s %-9s %-10s %-9s %-8s %-9s %s"
          % ("peer", "cq", "peer YoY", "best k", "r", "n", "implied DE YoY (+/-1 se)"))
    for comp in sorted(gq):
        if comp == base:
            continue
        # rank candidate lags by |r|, then use the strongest one for which the
        # peer observation actually EXISTS today. A peer whose best lag is -1
        # (it trails Deere) cannot nowcast Deere at all -- fall back to k=0.
        ranked = []
        for k in range(-4, 5):
            xs, ys = [], []
            for t in sorted(gq[base]):
                if (t - k) in gq[comp]:
                    xs.append(gq[comp][t - k])
                    ys.append(gq[base][t])
            r, n, _ = pearson(xs, ys)
            if r is not None and n >= 8:
                ranked.append((abs(r), r, k, n))
        ranked.sort(reverse=True)
        pick = next(((r, k, n) for _a, r, k, n in ranked if (target - k) in gq[comp]), None)
        if pick is None:
            continue
        rr, k, nn = pick
        b = (rr, nn, None, k)
        src_t = target - k          # peer observation that maps onto Deere at `target`
        xs, ys = [], []
        for t in sorted(gq[base]):
            if (t - k) in gq[comp]:
                xs.append(gq[comp][t - k])
                ys.append(gq[base][t])
        fit = ols(xs, ys)
        if not fit:
            continue
        a0, bb, se, n = fit
        x = gq[comp][src_t]
        yhat = a0 + bb * x
        print("%-9s %-9s %+9.1f%% %+9d %+8.3f %-9d %+.1f%%  +/- %.1f%%"
              % (comp, cq_name(src_t), 100 * x, k, b[0], n, 100 * yhat, 100 * se))
    print()
    print("CAVEATS on the nowcast block: single-regressor OLS on overlapping YoY windows;")
    print("standard errors are in-sample residual sd and understate true uncertainty.")
    print("Kubota growth is in JPY and carries a translation component Deere does not.")


if __name__ == "__main__":
    main()
