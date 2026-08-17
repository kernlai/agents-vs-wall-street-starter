#!/usr/bin/env python3
"""
Establish the LAG between input-cost moves and Deere's reported
production-cost bridge component.

Deere buys steel and components ahead of build, and build precedes shipment,
so the input prices sitting in a given fiscal quarter's cost of sales were
mostly paid one or two quarters earlier. This measures that lag rather than
assuming it: for each macro series, the fiscal-quarter average is computed on
Deere's real 52/53-week calendar, converted to a year-on-year percentage
change, and cross-correlated against the bridge's production-cost component
(itself a year-on-year dollar delta) at lags of 0 to 6 quarters.

Reported with sample sizes. n is 16-18 per segment, which is small: an r of
0.5 at n=17 is roughly p=0.04 two-sided with ONE test, and this runs 7 lags x
several series, so the multiple-comparisons burden is real and is flagged in
the output rather than papered over.
"""
import json, math, argparse, datetime, sys
from statistics import mean

MONTHS_BACK = None


def qkey(lab):
    return (int(lab[2:]), int(lab[0])) if lab[1] == "Q" else None


def parse_date(s):
    return datetime.date(*map(int, s.split("-")))


def quarter_windows(cal):
    """(fy, q) -> (start_date, end_date) using consecutive fiscal quarter ends."""
    items = sorted(((int(k[:4]), int(k[-1]), parse_date(v)) for k, v in cal.items()))
    out = {}
    for i, (fy, q, end) in enumerate(items):
        if i == 0:
            start = end - datetime.timedelta(days=90)
        else:
            start = items[i - 1][2] + datetime.timedelta(days=1)
        out[(fy, q)] = (start, end)
    return out


def monthly_to_quarter(obs, windows):
    """Average the monthly (or weekly) observations falling inside each quarter."""
    pts = [(parse_date(d), v) for d, v in obs]
    out = {}
    for key, (s, e) in windows.items():
        vals = [v for d, v in pts if s <= d <= e]
        if len(vals) >= 2:          # need real coverage, else leave missing
            out[key] = mean(vals)
    return out


def yoy(series):
    out = {}
    for (fy, q), v in series.items():
        p = series.get((fy - 1, q))
        if p and p != 0:
            out[(fy, q)] = 100.0 * (v / p - 1.0)
    return out


def pearson(xs, ys):
    n = len(xs)
    if n < 4:
        return None, n
    mx, my = mean(xs), mean(ys)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None, n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy), n


def shift(key, lags):
    fy, q = key
    idx = fy * 4 + (q - 1) - lags
    return (idx // 4, idx % 4 + 1)


def ar1(xs):
    if len(xs) < 4:
        return 0.0
    m = mean(xs)
    num = sum((xs[i] - m) * (xs[i - 1] - m) for i in range(1, len(xs)))
    den = sum((x - m) ** 2 for x in xs)
    return num / den if den else 0.0


def n_eff(xs, ys):
    """Sample size deflated for AR(1) persistence in both series (Dawdy-Matalas).
    Quarterly YoY changes are heavily autocorrelated by construction, so the
    nominal n badly overstates the independent information available."""
    rx, ry = ar1(xs), ar1(ys)
    f = (1 - rx * ry) / (1 + rx * ry) if (1 + rx * ry) else 0
    return max(3.0, len(xs) * f)


def partial(xs, ys, zs):
    """r(x,y | z) -- how much of the association survives removing the common
    inflation cycle."""
    rxy, _ = pearson(xs, ys)
    rxz, _ = pearson(xs, zs)
    ryz, _ = pearson(ys, zs)
    if None in (rxy, rxz, ryz):
        return None
    den = math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))
    return rxy if den == 0 else (rxy - rxz * ryz) / den


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bridges", required=True)
    ap.add_argument("--fred", required=True)
    ap.add_argument("--calendar", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    cal = json.load(open(a.calendar))
    windows = quarter_windows(cal)
    fred = json.load(open(a.fred))
    bridges = json.load(open(a.bridges))

    # dependent variables: bridge production-cost component, by segment
    dep = {}
    for r in bridges["reconciled"]:
        seg = r.get("segment")
        if not seg:
            continue
        k = qkey(r["end_label"])
        for comp in ("production_costs", "warranty", "price", "volume_mix"):
            v = r["components"].get(comp)
            if v is not None:
                dep.setdefault((seg, comp), {})[k] = v

    # independent variables: YoY % change of quarter-averaged macro series
    macro_q, macro_yoy = {}, {}
    for sid, d in fred.items():
        mq = monthly_to_quarter(d["obs"], windows)
        macro_q[sid] = mq
        macro_yoy[sid] = yoy(mq)

    results = []
    for (seg, comp), dv in sorted(dep.items()):
        for sid in fred:
            for lag in range(7):
                xs, ys = [], []
                for k, y in sorted(dv.items()):
                    x = macro_yoy[sid].get(shift(k, lag))
                    if x is None:
                        continue
                    xs.append(x)
                    ys.append(y)
                r, n = pearson(xs, ys)
                if r is None:
                    continue
                row = {"segment": seg, "component": comp, "series": sid,
                       "lag_quarters": lag, "r": round(r, 4), "n": n,
                       "n_eff": round(n_eff(xs, ys), 1)}
                # partial correlation controlling for broad producer inflation
                zs = []
                ok = True
                for k, _y in sorted(dv.items()):
                    if macro_yoy[sid].get(shift(k, lag)) is None:
                        continue
                    z = macro_yoy.get("PPIACO", {}).get(shift(k, lag))
                    if z is None:
                        ok = False
                        break
                    zs.append(z)
                if ok and len(zs) == len(xs) and sid != "PPIACO":
                    pr = partial(xs, ys, zs)
                    if pr is not None:
                        row["r_partial_vs_PPIACO"] = round(pr, 4)
                # first-differenced dependent variable removes the level trend
                dxs = [xs[i] - xs[i - 1] for i in range(1, len(xs))]
                dys = [ys[i] - ys[i - 1] for i in range(1, len(ys))]
                rd, nd = pearson(dxs, dys)
                if rd is not None:
                    row["r_first_diff"] = round(rd, 4)
                    row["n_first_diff"] = nd
                results.append(row)

    out = {"correlations": results,
           "macro_quarterly": {sid: {f"{fy}Q{q}": round(v, 4) for (fy, q), v in mq.items()}
                               for sid, mq in macro_q.items()},
           "macro_yoy_pct": {sid: {f"{fy}Q{q}": round(v, 4) for (fy, q), v in my.items()}
                             for sid, my in macro_yoy.items()},
           "dependent": {f"{seg}|{comp}": {f"{fy}Q{q}": v for (fy, q), v in dv.items()}
                         for (seg, comp), dv in dep.items()},
           "windows": {f"{fy}Q{q}": [s.isoformat(), e.isoformat()]
                       for (fy, q), (s, e) in sorted(windows.items())}}
    open(a.out, "w").write(json.dumps(out, indent=1))

    # headline: best lag per series for PPA production costs
    print("PPA production_costs vs macro YoY -- r by lag (n in brackets)", file=sys.stderr)
    for sid in fred:
        row = [x for x in results if x["segment"] == "PPA"
               and x["component"] == "production_costs" and x["series"] == sid]
        if not row:
            continue
        row.sort(key=lambda x: x["lag_quarters"])
        cells = " ".join(f"L{x['lag_quarters']}:{x['r']:+.2f}" for x in row)
        best = max(row, key=lambda x: abs(x["r"]))
        print(f"{sid:18} {cells} | BEST L{best['lag_quarters']} r={best['r']:+.3f} "
              f"n={best['n']} n_eff={best['n_eff']} "
              f"partial={best.get('r_partial_vs_PPIACO')} "
              f"dif={best.get('r_first_diff')}", file=sys.stderr)


if __name__ == "__main__":
    main()
