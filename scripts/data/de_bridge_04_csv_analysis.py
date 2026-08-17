#!/usr/bin/env python3
"""
Step 3 of the Deere operating-profit-bridge pipeline.

Writes the tidy-long CSV of reconciled bridges and runs the variance
decomposition that the lead-time / order-book hypothesis actually turns on:

    across quarters, how much of the variation in the YEAR-OVER-YEAR CHANGE in
    segment operating profit is carried by volume/mix, and how much by the cost
    lines (production costs + warranty)?

Because the bridge is an exact identity,

    dOP = sum_i c_i        =>      Var(dOP) = sum_i Cov(c_i, dOP)

so Cov(c_i, dOP) / Var(dOP) is an exact, additive share of variance for each
component.  Shares sum to 1.0 and may be negative (a component that moves
against the total is a stabiliser).  Raw Var(c_i) is reported alongside, since a
volatile component that is uncorrelated with the total contributes little.

stdlib only.
"""
import csv
import json
import os
import sys
from collections import defaultdict

SCRATCH = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"
PARSED = os.path.join(SCRATCH, "de_bridge_parsed.json")
ENDPOINTS = os.path.join(SCRATCH, "de_segment_op_profit.json")
OUTDIR = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere"
CSV_PATH = os.path.join(OUTDIR, "de_operating_profit_bridge.csv")

# Deere fiscal period ends, from SEC XBRL (CIK 315189) dei/us-gaap contexts.
PERIOD_END = {
    (2019, 1): "2019-01-27", (2019, 2): "2019-04-28", (2019, 3): "2019-07-28", (2019, 4): "2019-11-03",
    (2020, 1): "2020-02-02", (2020, 2): "2020-05-03", (2020, 3): "2020-08-02", (2020, 4): "2020-11-01",
    (2021, 1): "2021-01-31", (2021, 2): "2021-05-02", (2021, 3): "2021-08-01", (2021, 4): "2021-10-31",
    (2022, 1): "2022-01-30", (2022, 2): "2022-05-01", (2022, 3): "2022-07-31", (2022, 4): "2022-10-30",
    (2023, 1): "2023-01-29", (2023, 2): "2023-04-30", (2023, 3): "2023-07-30", (2023, 4): "2023-10-29",
    (2024, 1): "2024-01-28", (2024, 2): "2024-04-28", (2024, 3): "2024-07-28", (2024, 4): "2024-10-27",
    (2025, 1): "2025-01-26", (2025, 2): "2025-04-27", (2025, 3): "2025-07-27", (2025, 4): "2025-11-02",
    (2026, 1): "2026-02-01", (2026, 2): "2026-05-03",
}
EXTRA = ["voluntary_separation", "impairment"]
# FY2020 decks used "Voluntary Separation" / "Impairment" where later decks use
# "Special Items"; fold them in so the shares still sum to 100%.
CANON = ["volume_mix", "price", "currency", "warranty", "production_costs",
         "sag_rd", "special_items", "other"]
CANON_CSV = list(CANON)
SEGS = ["PPA", "SAT", "CF"]


def mean(xs):
    return sum(xs) / len(xs)


def var(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def cov(xs, ys):
    if len(xs) < 2:
        return 0.0
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def corr(xs, ys):
    d = (var(xs) * var(ys)) ** 0.5
    return cov(xs, ys) / d if d else float("nan")


def main():
    data = json.load(open(PARSED))
    eps = json.load(open(ENDPOINTS))
    br = [b for b in data["bridges"] if b["segment"] in SEGS]
    br.sort(key=lambda b: (b["segment"], b["fiscal_year"], b["fiscal_quarter"]))
    for b in br:
        b["stat_components"] = dict(b["components"])
        for k in EXTRA:                       # FY2020 wording of "special items"
            if k in b["stat_components"]:
                b["stat_components"]["special_items"] = \
                    b["stat_components"].get("special_items", 0) + b["stat_components"].pop(k)

    os.makedirs(OUTDIR, exist_ok=True)
    rows = []
    for b in br:
        fy, fq, seg = b["fiscal_year"], b["fiscal_quarter"], b["segment"]
        pe = PERIOD_END.get((fy, fq), "")
        src = f"slides/{b['file']}"
        base_note = f"parse={b['method']}"
        if b["recovered_component"]:
            base_note += f"; {b['recovered_component']} recovered as arithmetic residual"
        if b["note"]:
            base_note += f"; {b['note']}"
        if fy == 2020:
            base_note += "; pre-FY2021 segment basis (as reported at the time)"

        def add(component, value, note):
            rows.append({
                "series_id": "de_op_bridge", "period_end": pe,
                "fiscal_year": fy, "fiscal_quarter": fq, "segment": seg,
                "component": component, "value": value, "units": "USDm",
                "source": src, "notes": note})

        add("opening_operating_profit", b["opening"],
            "prior-year same quarter, per 8-K segment table: "
            + eps[f"{fy}Q{fq}"]["_source"])
        for k in CANON_CSV + EXTRA:
            if k in b["components"]:
                add(k, b["components"][k], base_note)
        add("closing_operating_profit", b["closing"],
            "reported quarter, per 8-K segment table: "
            + eps[f"{fy}Q{fq}"]["_source"])

    with open(CSV_PATH, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["series_id", "period_end", "fiscal_year",
                                           "fiscal_quarter", "segment", "component",
                                           "value", "units", "source", "notes"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {CSV_PATH}: {len(rows)} rows, {len(br)} segment-quarters")

    # ------------------------------------------------------------- analysis
    print("\n" + "=" * 78)
    print("VARIANCE DECOMPOSITION OF THE YoY CHANGE IN SEGMENT OPERATING PROFIT")
    print("=" * 78)
    summary = {}
    for seg in SEGS:
        rs = [b for b in br if b["segment"] == seg]
        d = [b["closing"] - b["opening"] for b in rs]
        n = len(rs)
        vd = var(d)
        comp = {k: [b["stat_components"].get(k, 0) for b in rs] for k in CANON}
        print(f"\n--- {seg}   n = {n} quarters "
              f"({rs[0]['fiscal_year']}Q{rs[0]['fiscal_quarter']}"
              f"-{rs[-1]['fiscal_year']}Q{rs[-1]['fiscal_quarter']})")
        print(f"    sd of YoY change in operating profit: {vd ** 0.5:,.0f} USDm")
        print(f"    {'component':20} {'sd':>8} {'cov-share':>10} {'corr w/ dOP':>12}")
        shares = {}
        for k in CANON:
            sh = cov(comp[k], d) / vd if vd else float("nan")
            shares[k] = sh
            print(f"    {k:20} {var(comp[k]) ** 0.5:8,.0f} {sh:10.1%} "
                  f"{corr(comp[k], d):12.2f}")
        print(f"    {'SUM OF SHARES':20} {'':8} {sum(shares.values()):10.1%}")
        cost = shares["production_costs"] + shares["warranty"]
        rev = shares["volume_mix"] + shares["price"] + shares["currency"]
        print(f"    grouped: volume/mix                 {shares['volume_mix']:6.1%}")
        print(f"             production costs + warranty{cost:6.1%}")
        print(f"             all revenue-linked "
              f"(vol/mix+price+currency) {rev:6.1%}")
        # count statistic, robust to outliers
        wins = sum(1 for b in rs
                   if abs(b["stat_components"].get("volume_mix", 0)) >
                   abs(b["stat_components"].get("production_costs", 0) +
                       b["stat_components"].get("warranty", 0)))
        print(f"    quarters where |volume/mix| > |production costs + warranty|: "
              f"{wins}/{n} ({wins / n:.0%})")
        # link back to revenue
        ds = [(b["sales_cur"] - b["sales_pri"]) for b in rs
              if b.get("sales_cur") and b.get("sales_pri")]
        dv = [b["stat_components"].get("volume_mix", 0) for b in rs
              if b.get("sales_cur") and b.get("sales_pri")]
        dd = [(b["closing"] - b["opening"]) for b in rs
              if b.get("sales_cur") and b.get("sales_pri")]
        print(f"    corr(YoY change in segment net sales, volume/mix bar) = "
              f"{corr(ds, dv):.2f}  (n={len(ds)})")
        print(f"    corr(YoY change in segment net sales, YoY change in op profit) = "
              f"{corr(ds, dd):.2f}  (n={len(ds)})")
        # How much operating-profit uncertainty is LEFT once the revenue-side
        # bars (volume/mix, price, currency) are known?  This is the direct
        # test of "put the wide range on margin, not on revenue".
        resid = [dd - b["stat_components"].get("volume_mix", 0)
                 - b["stat_components"].get("price", 0)
                 - b["stat_components"].get("currency", 0)
                 for dd, b in zip(d, rs)]
        resid_v = [dd - b["stat_components"].get("volume_mix", 0) for dd, b in zip(d, rs)]
        print(f"    sd of dOP                                    {vd ** 0.5:7,.0f}")
        print(f"    sd of dOP after removing volume/mix          {var(resid_v) ** 0.5:7,.0f}"
              f"   ({var(resid_v) / vd:.0%} of variance remains)")
        print(f"    sd of dOP after removing vol/mix+price+ccy   {var(resid) ** 0.5:7,.0f}"
              f"   ({var(resid) / vd:.0%} of variance remains)")
        # flow-through: profit contribution per $1 of segment sales change
        slope = cov(ds, dv) / var(ds) if var(ds) else float("nan")
        slope_op = cov(ds, dd) / var(ds) if var(ds) else float("nan")
        print(f"    flow-through: d(volume/mix bar) per $1 d(net sales) = {slope:.3f}")
        print(f"    flow-through: d(operating profit) per $1 d(net sales) = {slope_op:.3f}")
        summary[seg] = {"n": n, "sd_dOP": vd ** 0.5, "shares": shares,
                        "cost_share": cost, "rev_share": rev,
                        "wins": wins,
                        "corr_sales_vol": corr(ds, dv),
                        "corr_sales_dop": corr(ds, dd),
                        "first": f"{rs[0]['fiscal_year']}Q{rs[0]['fiscal_quarter']}",
                        "last": f"{rs[-1]['fiscal_year']}Q{rs[-1]['fiscal_quarter']}",
                        "sd_resid_after_volmix": var(resid_v) ** 0.5,
                        "sd_resid_after_rev": var(resid) ** 0.5,
                        "flowthrough_volmix": slope, "flowthrough_op": slope_op}

    # pooled
    print("\n--- POOLED (all three segments, standardised by nothing; raw USDm)")
    rs = br
    d = [b["closing"] - b["opening"] for b in rs]
    vd = var(d)
    print(f"    n = {len(rs)}; sd of YoY change in operating profit {vd ** 0.5:,.0f}")
    pooled = {}
    for k in CANON:
        c = [b["stat_components"].get(k, 0) for b in rs]
        pooled[k] = cov(c, d) / vd
        print(f"    {k:20} sd {var(c) ** 0.5:8,.0f}  cov-share {pooled[k]:8.1%}")
    print(f"    volume/mix {pooled['volume_mix']:.1%} | "
          f"production costs + warranty "
          f"{pooled['production_costs'] + pooled['warranty']:.1%} | "
          f"price {pooled['price']:.1%}")
    summary["POOLED"] = {"n": len(rs), "shares": pooled, "sd_dOP": vd ** 0.5}

    json.dump(summary, open(os.path.join(SCRATCH, "de_bridge_summary.json"), "w"),
              indent=1, default=float)

    # -------- PPA component distribution, for the Q3 FY2026 prior
    print("\n--- PPA bridge components: distribution (USDm), all quarters and Q3s only")
    ppa = [b for b in br if b["segment"] == "PPA"]
    q3 = [b for b in ppa if b["fiscal_quarter"] == 3]
    print(f"    {'component':20} {'mean':>8} {'sd':>8} {'min':>8} {'max':>8} | "
          f"{'Q3 mean':>8} {'Q3 vals':>28}")
    for k in CANON:
        v = [b["stat_components"].get(k, 0) for b in ppa]
        v3 = [b["stat_components"].get(k, 0) for b in q3]
        print(f"    {k:20} {mean(v):8,.0f} {var(v) ** 0.5:8,.0f} {min(v):8,.0f} "
              f"{max(v):8,.0f} | {mean(v3):8,.0f} {str(v3):>28}")
    print(f"    PPA Q3 openings (prior-year Q3 op profit): "
          f"{[(b['fiscal_year'], b['opening']) for b in q3]}")

    # -------- recent-era subsample: the downturn Deere is actually in now
    print("\n--- RECENT ERA ONLY (FY2024Q1 onward: the down-cycle)")
    for seg in SEGS:
        rs = [b for b in br if b["segment"] == seg and b["fiscal_year"] >= 2024]
        if len(rs) < 4:
            continue
        d = [b["closing"] - b["opening"] for b in rs]
        vd = var(d)
        sh = {k: cov([b["stat_components"].get(k, 0) for b in rs], d) / vd for k in CANON}
        print(f"    {seg} n={len(rs)} sd={vd ** 0.5:,.0f} | vol/mix {sh['volume_mix']:6.1%}"
              f" | prod+warr {sh['production_costs'] + sh['warranty']:6.1%}"
              f" | price {sh['price']:6.1%}")


if __name__ == "__main__":
    sys.exit(main())
