#!/usr/bin/env python3
"""
Deere employment -> shipment-volume indicator: backtest + ongoing tracker engine.

Answers one question: does employment data actually predict Deere's reported volumes?

Two independent tests, both reported WITH sample size:
  TEST 1 (annual, n=10):  YoY change in UAW-covered active US production/maintenance
                          headcount (10-K Item 1) vs YoY change in worldwide equipment
                          operations net sales.
  TEST 2 (quarterly, n=11): net plant labour delta (recalls announced - layoffs effective),
                          bucketed into Deere fiscal quarters, vs segment net sales YoY at
                          lag 0, +1 and +2 quarters. Run in aggregate AND split PPA vs CF.

Inputs (all repo-local, no network):
  data/deere/footprint/headcount_hiring.csv
  data/deere/footprint/warn_layoffs.csv
  data/deere/de_segments_modern.csv

Usage:  python3 scripts/data/de_employment_indicator_backtest.py
"""

from __future__ import annotations

import csv
import datetime as dt
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FOOT = os.path.join(ROOT, "data", "deere", "footprint")
SEG = os.path.join(ROOT, "data", "deere", "de_segments_modern.csv")

# Plant -> segment map. Filing-grade for the 10-K Item 2 sites; see PLANT_MAP.md for
# provenance of the inferred ones. Corporate/financial-services sites are excluded from
# every production aggregate.
PLANT_SEGMENT = {
    "Waterloo Works": "PPA",
    "Waterloo Foundry": "PPA",
    "Harvester Works": "PPA",
    "Seeding and Cylinder": "PPA",
    "Des Moines Works": "PPA",
    "Ottumwa Works": "SAT",
    "Horicon Works": "SAT",
    "Dubuque Works": "CF",
    "Davenport Works": "CF",
    "Coffeyville Works": "CF",
    "Intelligent Solutions Group": "EXCLUDE_SALARIED",
    "World Headquarters": "EXCLUDE_SALARIED",
    "John Deere Financial": "EXCLUDE_FINSVC",
    "Multiple Quad Cities sites": "EXCLUDE_CONTRACTOR",
    "Multiple US factories": "AGG",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None, n
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx == 0 or syy == 0:
        return None, n
    return sxy / math.sqrt(sxx * syy), n


def ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((a - mx) ** 2 for a in xs)
    if sxx == 0:
        return None, None
    slope = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sxx
    return slope, my - slope * mx


def r_pvalue_note(r, n):
    """Two-sided p for Pearson r via t = r*sqrt((n-2)/(1-r^2)), normal approx on t.

    Deliberately crude: with n around 10 this is indicative only, and the point of
    printing it is to show how weak the evidence is, not to certify significance.
    """
    if r is None or n < 4 or abs(r) >= 1:
        return None
    t = r * math.sqrt((n - 2) / (1 - r * r))
    # survival function of standard normal, x2 for two-sided
    p = math.erfc(abs(t) / math.sqrt(2))
    return p


def parse_date(s):
    return dt.date.fromisoformat(s)


# ---------------------------------------------------------------- fiscal calendar
def load_fiscal_quarters():
    """Deere fiscal quarter ends, from the reported segment table. Returns ordered list of
    (fy, q, start_date, end_date). Start = day after the previous quarter end."""
    ends = {}
    for r in read_csv(SEG):
        if r["series_id"] != "de_ppa_net_sales" or r["fiscal_quarter"] == "FY":
            continue
        ends[(int(r["fiscal_year"]), r["fiscal_quarter"])] = parse_date(r["period_end"])
    ordered = sorted(ends.items(), key=lambda kv: kv[1])
    out = []
    prev = None
    for (fy, q), end in ordered:
        start = (prev + dt.timedelta(days=1)) if prev else end - dt.timedelta(days=90)
        out.append((fy, q, start, end))
        prev = end
    # FY2026 Q3 is over (ended 2026-08-02) but unreported, so it is not in the segment
    # file. Append it so labour events inside it can still be bucketed.
    out.append((2026, "Q3", dt.date(2026, 5, 4), dt.date(2026, 8, 2)))
    return out


def bucket(fq, d):
    for fy, q, s, e in fq:
        if s <= d <= e:
            return (fy, q)
    return None


# ---------------------------------------------------------------- segment revenue
def load_segment_sales():
    """{(fy,q): {'PPA':x,'SAT':y,'CF':z}} quarterly net sales, USDm."""
    key = {"de_ppa_net_sales": "PPA", "de_sat_net_sales": "SAT", "de_cf_net_sales": "CF"}
    out = {}
    for r in read_csv(SEG):
        if r["series_id"] not in key or r["fiscal_quarter"] == "FY":
            continue
        k = (int(r["fiscal_year"]), r["fiscal_quarter"])
        out.setdefault(k, {})[key[r["series_id"]]] = float(r["value"])
    return out


def yoy(sales, fy, q, seg):
    cur = sales.get((fy, q), {}).get(seg)
    prv = sales.get((fy - 1, q), {}).get(seg)
    if cur is None or prv is None or prv == 0:
        return None
    return 100.0 * (cur / prv - 1.0)


# ---------------------------------------------------------------- labour events
def load_labour_events(fq):
    """Return per-fiscal-quarter labour deltas, by segment and in aggregate.

    Layoffs are bucketed by EFFECTIVE date (when capacity actually leaves the plant).
    Recalls/new hires are bucketed by ANNOUNCEMENT date (no effective date is published
    for most of them; they are described as beginning within weeks).
    Salaried/corporate/financial-services/contractor rows are excluded from production
    aggregates -- they are headcount, not build rate.
    """
    rows = read_csv(os.path.join(FOOT, "warn_layoffs.csv"))
    delta = {}          # (fy,q) -> {'layoff':n,'recall':n,'net':n}
    seg_delta = {}      # (fy,q) -> {seg: net}
    excluded = []
    for r in rows:
        sid, notes = r["series_id"], r["notes"]
        if sid.endswith("_fq"):
            continue  # derived aggregate rows in the source CSV; recomputed here
        plant = r["plant"]
        seg = PLANT_SEGMENT.get(plant, "UNKNOWN")
        if seg.startswith("EXCLUDE") or seg == "AGG":
            excluded.append((r["date"], plant, r["metric"], r["value"]))
            continue
        # Some WARN rows at production sites are explicitly salaried reduction waves
        # (Waterloo 49 and 69 in 2024, Des Moines 16, Dubuque 34). They are headcount,
        # not build rate, and are excluded from every production aggregate.
        if re.search(r"\bsalaried\b", notes or "", re.I):
            excluded.append((r["date"], plant + " (salaried)", r["metric"], r["value"]))
            continue
        metric, val = r["metric"], r["value"]
        if metric == "employees_affected":
            m = re.search(r"effective_date=(\d{4}-\d{2}-\d{2})", notes)
            d = parse_date(m.group(1)) if m else parse_date(r["date"])
            n = -float(val)
        elif metric in ("employees_recalled", "employees_hired_new"):
            if metric == "employees_recalled" and r["units"] == "employees" and "cumulative" in sid:
                continue
            d = parse_date(r["date"])
            n = float(val)
        else:
            continue  # labour_event / warn_notices_filed markers carry no headcount
        b = bucket(fq, d)
        if b is None:
            continue
        rec = delta.setdefault(b, {"layoff": 0.0, "recall": 0.0, "net": 0.0})
        if n < 0:
            rec["layoff"] += -n
        else:
            rec["recall"] += n
        rec["net"] += n
        sd = seg_delta.setdefault(b, {})
        sd[seg] = sd.get(seg, 0.0) + n
    return delta, seg_delta, excluded


# ---------------------------------------------------------------- TEST 1: annual
def test1_annual():
    rows = read_csv(os.path.join(FOOT, "headcount_hiring.csv"))
    uaw, eq = {}, {}
    for r in rows:
        if r["series_id"] == "de_uaw_covered_employees":
            uaw[int(r["date"][:4]) if r["date"][5:7] < "11" else int(r["date"][:4])] = float(r["value"])
        elif r["series_id"] == "de_equipment_net_sales":
            eq[int(r["date"][:4])] = float(r["value"])
    # key both by the 10-K fiscal-year label carried in the notes where available
    uaw_fy, eq_fy = {}, {}
    for r in rows:
        m = re.search(r"(?:^|[^0-9])FY(20\d\d)", r["notes"] or "")
        fy = int(m.group(1)) if m else None
        if fy is None:
            # dates are fiscal year ends: Oct/Nov of the fiscal year
            d = parse_date(r["date"])
            fy = d.year if d.month >= 10 else d.year - 1
        if r["series_id"] == "de_uaw_covered_employees":
            uaw_fy[fy] = float(r["value"])
        elif r["series_id"] == "de_equipment_net_sales":
            eq_fy[fy] = float(r["value"])

    years = sorted(set(uaw_fy) & set(eq_fy))
    rowsout = []
    for y in years:
        if (y - 1) in uaw_fy and (y - 1) in eq_fy:
            rowsout.append(
                (
                    y,
                    100.0 * (eq_fy[y] / eq_fy[y - 1] - 1),
                    100.0 * (uaw_fy[y] / uaw_fy[y - 1] - 1),
                )
            )
    return rowsout


def main():
    fq = load_fiscal_quarters()
    sales = load_segment_sales()

    print("=" * 78)
    print("TEST 1 -- ANNUAL: UAW-covered active US production heads vs equipment net sales")
    print("=" * 78)
    t1 = test1_annual()
    print(f"{'FY':>6} {'equip sales YoY':>16} {'UAW heads YoY':>14}")
    for y, s, h in t1:
        print(f"{y:>6} {s:>15.1f}% {h:>13.1f}%")
    xs = [h for _, _, h in t1]
    ys = [s for _, s, _ in t1]
    r, n = pearson(xs, ys)
    b, a = ols(xs, ys)
    p = r_pvalue_note(r, n)
    print(f"\n  n={n}  r={r:+.3f}  slope={b:.2f} (sales pp per head pp)  intercept={a:+.1f}")
    print(f"  crude two-sided p ~ {p:.4f}" if p else "")
    # drop FY2016 definitional break
    t1b = [t for t in t1 if t[0] != 2016]
    r2, n2 = pearson([h for _, _, h in t1b], [s for _, s, _ in t1b])
    b2, _ = ols([h for _, _, h in t1b], [s for _, s, _ in t1b])
    print(f"  excluding FY2016 definitional break: n={n2}  r={r2:+.3f}  slope={b2:.2f}")
    # asymmetry
    dn = [t for t in t1 if t[1] < 0]
    up = [t for t in t1 if t[1] >= 0]
    for lab, grp in (("DOWN years", dn), ("UP years", up)):
        if len(grp) >= 2:
            gaps = [h - s for _, s, h in grp]
            print(
                f"  {lab}: n={len(grp)} mean(head YoY - sales YoY)={sum(gaps)/len(gaps):+.1f}pp"
            )

    print()
    print("=" * 78)
    print("TEST 2 -- QUARTERLY: net plant labour delta vs segment net sales YoY")
    print("=" * 78)
    delta, seg_delta, excluded = load_labour_events(fq)
    qs = [(fy, q) for fy, q, _, _ in fq if (fy, q) in sales or (fy, q) == (2026, "Q3")]
    qs = [k for k in qs if k >= (2024, "Q1")]
    print(
        f"{'FiscalQ':>9} {'layoffs eff':>12} {'recalls ann':>12} {'net':>7} "
        f"{'PPA y/y':>9} {'SAT y/y':>9} {'CF y/y':>9}"
    )
    series = []
    for fy, q in qs:
        d = delta.get((fy, q), {"layoff": 0.0, "recall": 0.0, "net": 0.0})
        yy = {s: yoy(sales, fy, q, s) for s in ("PPA", "SAT", "CF")}
        fmt = lambda v: f"{v:8.1f}%" if v is not None else "       ?"
        print(
            f"{fy}{q:>4} {d['layoff']:>12.0f} {d['recall']:>12.0f} {d['net']:>7.0f} "
            f"{fmt(yy['PPA'])} {fmt(yy['SAT'])} {fmt(yy['CF'])}"
        )
        series.append(((fy, q), d, yy))

    def lagcorr(seg, lag):
        xs, ys = [], []
        idx = {k: i for i, (k, _, _) in enumerate(series)}
        for i, (k, d, _) in enumerate(series):
            j = i + lag
            if j >= len(series):
                continue
            tgt = series[j][2][seg]
            if tgt is None:
                continue
            xs.append(d["net"])
            ys.append(tgt)
        return pearson(xs, ys) + (xs, ys)

    print("\n  Aggregate net labour delta (all production plants) vs segment revenue YoY:")
    for seg in ("PPA", "SAT", "CF"):
        for lag in (0, 1, 2):
            r, n, xs, ys = lagcorr(seg, lag)
            p = r_pvalue_note(r, n)
            ptxt = f" p~{p:.3f}" if p else ""
            rtxt = f"{r:+.3f}" if r is not None else "  n/a"
            print(f"    {seg}  lag +{lag}Q:  n={n:>2}  r={rtxt}{ptxt}")

    def seg_lagcorr(seg, lag):
        xs, ys = [], []
        for i, (k, _, _) in enumerate(series):
            j = i + lag
            if j >= len(series):
                continue
            tgt = series[j][2][seg]
            if tgt is None:
                continue
            xs.append(seg_delta.get(k, {}).get(seg, 0.0))
            ys.append(tgt)
        return pearson(xs, ys) + (xs, ys)

    print("\n  SEGMENT-MATCHED labour delta (only that segment's plants) vs its revenue YoY:")
    for seg in ("PPA", "SAT", "CF"):
        for lag in (0, 1, 2):
            r, n, xs, ys = seg_lagcorr(seg, lag)
            p = r_pvalue_note(r, n)
            ptxt = f" p~{p:.3f}" if p else ""
            rtxt = f"{r:+.3f}" if r is not None else "  n/a"
            print(f"    {seg}  lag +{lag}Q:  n={n:>2}  r={rtxt}{ptxt}")

    print("\n  Segment-matched quarterly labour deltas actually observed:")
    for (fy, q) in qs:
        sd = seg_delta.get((fy, q), {})
        if sd:
            print(f"    {fy}{q}: " + ", ".join(f"{k} {v:+.0f}" for k, v in sorted(sd.items())))

    print("\n  Rows excluded from production aggregates (salaried / corporate / contractor):")
    for e in excluded:
        print(f"    {e[0]}  {e[1]:<32} {e[2]}={e[3]}")

    print()
    print("=" * 78)
    print("TEST 3 -- DOES THE LABOUR SIGNAL BEAT PERSISTENCE? (the test that matters)")
    print("=" * 78)
    print(
        "  Both the labour delta and revenue YoY move monotonically through one V-shaped\n"
        "  cycle, so a positive correlation is close to guaranteed and means little. The\n"
        "  real question: does labour tell you anything the revenue series does not already\n"
        "  tell you about itself?\n"
    )
    for seg in ("PPA", "SAT", "CF"):
        # persistence baseline: revenue YoY(t) predicting revenue YoY(t+1)
        px, py = [], []
        for i in range(len(series) - 1):
            a = series[i][2][seg]
            b = series[i + 1][2][seg]
            if a is not None and b is not None:
                px.append(a)
                py.append(b)
        rp, np_ = pearson(px, py)
        # labour delta(t) predicting revenue YoY(t+1)
        rl, nl, _, _ = lagcorr(seg, 1)
        # labour delta(t) predicting the ACCELERATION in revenue YoY, t -> t+1
        ax, ay = [], []
        for i in range(len(series) - 1):
            a = series[i][2][seg]
            b = series[i + 1][2][seg]
            if a is not None and b is not None:
                ax.append(series[i][1]["net"])
                ay.append(b - a)
        ra, na = pearson(ax, ay)
        fmt = lambda v: f"{v:+.3f}" if v is not None else "  n/a"
        print(f"  {seg}:")
        print(f"    persistence   revYoY(t)   -> revYoY(t+1) : n={np_:>2}  r={fmt(rp)}")
        print(f"    labour        labour(t)   -> revYoY(t+1) : n={nl:>2}  r={fmt(rl)}")
        print(f"    labour->accel labour(t)   -> d revYoY     : n={na:>2}  r={fmt(ra)}")

    print("\n  Directional hit rate, sign of net labour delta vs sign of next-quarter")
    print("  revenue YoY acceleration (the only usable form of the signal):")
    for seg in ("PPA", "SAT", "CF"):
        hits = tot = 0
        for i in range(len(series) - 1):
            a = series[i][2][seg]
            b = series[i + 1][2][seg]
            if a is None or b is None:
                continue
            nd = series[i][1]["net"]
            if nd == 0:
                continue
            tot += 1
            if (nd > 0) == (b - a > 0):
                hits += 1
        if tot:
            print(f"    {seg}: {hits}/{tot} correct ({100.0*hits/tot:.0f}%)  -- n={tot}, coin-flip band is wide")

    print(
        "\nNOTE: TEST 2 and TEST 3 span a single cycle turn. n is 8-11 quarterly observations\n"
        "with one trough and one recovery; every correlation is descriptive of that one\n"
        "episode and is NOT an estimated coefficient. Do not quote it as a validated\n"
        "relationship. TEST 1 (n=10 annual) is the only calibration with any real support,\n"
        "and even that is 10 points on a deeply cyclical business."
    )


if __name__ == "__main__":
    sys.exit(main())
