#!/usr/bin/env python3
"""
de_thesis_verdict.py -- adjudication script for the LEAD-TIME / ORDER-BOOK hypothesis.

Reconciles the four evidence workstreams and measures the ONE thing that determines
the recommended range widths: how accurate is the inference a forecaster must actually
make today -- "take Deere's Q2-vintage FY guidance, subtract reported H1, get H2".

Stdlib only. Reads only files under data/deere/. Writes nothing but stdout.
No FY2026 Q3 actuals exist; none are used.
"""
import csv, math, os, statistics as st
from collections import defaultdict

D = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere"


def rows(fn):
    with open(os.path.join(D, fn)) as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def desc(xs, label, unit=""):
    xs = [x for x in xs if x is not None]
    n = len(xs)
    if n == 0:
        print(f"  {label:<46} n=0 (no data)")
        return None
    m = st.mean(xs)
    sd = st.stdev(xs) if n > 1 else float("nan")
    mae = st.mean([abs(x) for x in xs])
    mx = max(xs, key=abs)
    print(f"  {label:<46} n={n:<3} mean={m:+7.2f} sd={sd:6.2f} MAE={mae:6.2f} worst={mx:+7.2f} {unit}")
    return dict(n=n, mean=m, sd=sd, mae=mae, worst=mx, vals=xs)


print("=" * 100)
print("PART 1 -- RECONCILING THE APPARENT CONTRADICTION BETWEEN WORKSTREAMS")
print("=" * 100)
print("""
The bridge workstream says volume/mix carries 65-90% of variance in the REALISED YoY change
in operating profit, and concludes the hypothesis is contradicted.
The predictability workstream says margin carries ~79% of variance in the one-quarter-ahead
operating-profit SURPRISE, and concludes the hypothesis is supported.

These are not in conflict. They decompose different quantities: realised variation vs
unforecastable variation. The hypothesis is a claim about FORECASTABILITY. The test that
separates them is: how much of each bridge component is predictable ex ante?
""")

# --- PPA bridge components, wide form -------------------------------------------------
br = [r for r in rows("de_operating_profit_bridge.csv") if r["series_id"] == "de_op_bridge"]
bq = defaultdict(dict)
for r in br:
    key = (r["segment"], int(r["fiscal_year"]), int(r["fiscal_quarter"]))
    bq[key][r["component"]] = num(r["value"])

COST = ["production_costs", "warranty", "sag_rd", "other"]
REVLINKED = ["volume_mix", "price", "currency"]

for seg in ("PPA", "SAT", "CF"):
    ks = sorted(k for k in bq if k[0] == seg)
    dop, vm, cost, rev = [], [], [], []
    for k in ks:
        b = bq[k]
        if "opening_operating_profit" not in b or "closing_operating_profit" not in b:
            continue
        dop.append(b["closing_operating_profit"] - b["opening_operating_profit"])
        vm.append(b.get("volume_mix", 0.0))
        cost.append(sum(b.get(c, 0.0) for c in COST))
        rev.append(sum(b.get(c, 0.0) for c in REVLINKED))
    n = len(dop)
    print(f"\n{seg}  n={n} segment-quarters (bridge, YoY deltas, USDm)")
    print(f"  sd(delta OP)               = {st.stdev(dop):7.1f}")
    print(f"  sd(volume/mix bar)         = {st.stdev(vm):7.1f}")
    print(f"  sd(revenue-linked block)   = {st.stdev(rev):7.1f}   [volume_mix+price+currency]")
    print(f"  sd(cost block)             = {st.stdev(cost):7.1f}   [prod costs+warranty+SA&G/R&D+other]")
    # exact additive variance shares
    mo = st.mean(dop)
    var = sum((d - mo) ** 2 for d in dop) / (n - 1)
    for nm, ser in (("volume/mix", vm), ("revenue-linked", rev), ("cost block", cost)):
        ms = st.mean(ser)
        cov = sum((a - ms) * (b - mo) for a, b in zip(ser, dop)) / (n - 1)
        print(f"    variance share {nm:<16} = {100*cov/var:+7.1f}%")

print("""
READ: the cost block has a small or negative share of REALISED variance. That is the bridge
workstream's finding and it is correct. But sd(cost block) is 150-300 USDm in absolute terms,
and -- crucially -- almost none of it is forecastable, whereas most of the volume/mix bar is.
""")

# --- how forecastable is each block? --------------------------------------------------
print("-" * 100)
print("PART 1b -- FORECASTABILITY OF EACH BLOCK (persistence test, PPA)")
print("-" * 100)
print("""A component that is forecastable should be autocorrelated / persistent: last quarter's
bridge value should carry information about this quarter's. Volume/mix tracks a revenue path
management guides to; cost surprises should look closer to white noise.""")

for seg in ("PPA", "SAT", "CF"):
    ks = sorted(k for k in bq if k[0] == seg)
    series = {"volume_mix": [], "cost_block": [], "production_costs": [], "price": []}
    for k in ks:
        b = bq[k]
        series["volume_mix"].append(b.get("volume_mix", 0.0))
        series["price"].append(b.get("price", 0.0))
        series["production_costs"].append(b.get("production_costs", 0.0))
        series["cost_block"].append(sum(b.get(c, 0.0) for c in COST))
    print(f"\n{seg}:")
    for nm, s in series.items():
        a, b_ = s[:-1], s[1:]
        n = len(a)
        ma, mb = st.mean(a), st.mean(b_)
        cov = sum((x - ma) * (y - mb) for x, y in zip(a, b_))
        va = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b_))
        r = cov / va if va else float("nan")
        print(f"  lag-1 autocorrelation  {nm:<20} r={r:+.3f}  (n={n} pairs)")

print("""
READ: volume/mix is strongly persistent (it follows the multi-quarter revenue cycle Deere
guides to). The cost block is far less persistent -- closer to a sequence of one-off shocks
(tariff rulings, warranty true-ups, absorption). Persistence is forecastability. This is the
mechanism that reconciles the two workstreams and it is the hypothesis's real content.
""")

print("=" * 100)
print("PART 2 -- THE TEST THAT SETS THE RANGE WIDTHS")
print("Q2-vintage FY guidance, minus reported H1, versus realised H2. This is EXACTLY the")
print("inference required for Q3 FY2026 today.")
print("=" * 100)

gva = rows("de_guidance_vs_actual.csv")

# segment quarterly sales from the predictability panel
pred = rows("de_predictability.csv")
seg_sales = {}
for r in pred:
    if r["series_id"] == "de_segment_sales_usdm":
        seg_sales[(r["segment"], int(r["fiscal_year"]), int(r["fiscal_quarter"]))] = num(r["value"])
seg_op = {}
for r in pred:
    if r["series_id"] == "de_segment_op_usdm":
        seg_op[(r["segment"], int(r["fiscal_year"]), int(r["fiscal_quarter"]))] = num(r["value"])
rev_act = {}
for r in pred:
    if r["series_id"] == "de_revenue_actual_usdm":
        rev_act[(int(r["fiscal_year"]), int(r["fiscal_quarter"]))] = num(r["value"])

print("\n[2a] ENTERPRISE H2 NET SALES & REVENUES implied by Q2-vintage FY guidance")
print("     (uses fy_net_sales_revenues_growth where available)")
sub = [r for r in gva if r["metric"] == "fy_net_sales_revenues_growth" and r["vintage_quarter"] == "Q2"]
for r in sub:
    print(f"     FY{r['fiscal_year']}: guide mid {r['guidance_mid']}% actual {r['actual']}% err {r['error_pct']}")

print("\n[2b] SEGMENT FY SALES GROWTH GUIDANCE ISSUED AT Q2 vs ACTUAL FY OUTCOME (pp error)")
res = {}
for metric, lab in (("fy_segment_sales_growth_ppa", "PPA"),
                    ("fy_segment_sales_growth_sat", "SAT"),
                    ("fy_segment_sales_growth_cf", "CF"),
                    ("fy_segment_sales_growth_ag_turf", "AG&TURF (legacy)")):
    sub = [r for r in gva if r["metric"] == metric and r["vintage_quarter"] == "Q2"]
    errs = []
    detail = []
    for r in sub:
        gm, ac = num(r["guidance_mid"]), num(r["actual"])
        if gm is None or ac is None:
            continue
        errs.append(ac - gm)
        detail.append(f"FY{r['fiscal_year']} guide{gm:+.1f}% act{ac:+.1f}% err{ac-gm:+.1f}pp")
    res[lab] = desc(errs, f"FY sales growth guide err @Q2, {lab}", "pp")
    for d in detail:
        print(f"      {d}")

print("\n[2c] THE DECISIVE ONE -- implied H2 SEGMENT SALES error, in %")
print("     H2_implied = FY_sales_guide(from Q2) - H1_actual ; compared with realised H2.")
h2res = {}
for metric, seg in (("fy_segment_sales_growth_ppa", "PPA"),
                    ("fy_segment_sales_growth_sat", "SAT"),
                    ("fy_segment_sales_growth_cf", "CF")):
    sub = [r for r in gva if r["metric"] == metric and r["vintage_quarter"] == "Q2"]
    errs, det = [], []
    for r in sub:
        fy = int(r["fiscal_year"])
        gm = num(r["guidance_mid"])
        if gm is None:
            continue
        prior = [seg_sales.get((seg, fy - 1, q)) for q in (1, 2, 3, 4)]
        cur_h1 = [seg_sales.get((seg, fy, q)) for q in (1, 2)]
        cur_h2 = [seg_sales.get((seg, fy, q)) for q in (3, 4)]
        if any(v is None for v in prior + cur_h1 + cur_h2):
            continue
        fy_implied = sum(prior) * (1 + gm / 100.0)
        h2_implied = fy_implied - sum(cur_h1)
        h2_actual = sum(cur_h2)
        e = 100.0 * (h2_actual / h2_implied - 1.0)
        errs.append(e)
        det.append(f"FY{fy} H2 implied {h2_implied:8.0f} actual {h2_actual:8.0f} err {e:+6.1f}%")
    h2res[seg] = desc(errs, f"implied-H2 sales error @Q2 guidance, {seg}", "%")
    for d in det:
        print(f"      {d}")

print("\n[2d] SAME INFERENCE FOR PPA OPERATING PROFIT (the margin side)")
sub = [r for r in gva if r["metric"] == "fy_ppa_operating_margin" and r["vintage_quarter"] == "Q2"]
errs, det = [], []
for r in sub:
    fy = int(r["fiscal_year"])
    gm, ac = num(r["guidance_mid"]), num(r["actual"])
    if gm is None or ac is None:
        continue
    errs.append(100 * (ac - gm))  # pp -> bps
    det.append(f"FY{fy} PPA margin guide {gm:.2f}% actual {ac:.2f}% err {100*(ac-gm):+5.0f}bps")
ppa_m = desc(errs, "FY PPA operating-margin guide err @Q2", "bps")
for d in det:
    print(f"      {d}")

sub = [r for r in gva if r["metric"] == "fy_ppa_operating_profit_implied" and r["vintage_quarter"] == "Q2"]
errs, det = [], []
for r in sub:
    ep = num(r["error_pct"])
    if ep is None:
        continue
    errs.append(ep)
    det.append(f"FY{r['fiscal_year']} PPA OP guide-implied err {ep:+.1f}%")
ppa_op = desc(errs, "FY PPA operating-profit guide err @Q2", "%")
for d in det:
    print(f"      {d}")

print("\n[2e] H2 NET INCOME implied by Q2 guidance -- the bottom-line analogue (longest sample)")
sub = [r for r in gva if r["metric"] == "fy_h2_net_income_implied_by_q2_guidance"]
errs, det = [], []
for r in sub:
    ep = num(r["error_pct"])
    if ep is None:
        continue
    errs.append(ep)
    det.append(f"FY{r['fiscal_year']} H2 NI implied err {ep:+7.1f}%  ({r['cycle_phase']}, {r['actual_vs_range']})")
h2ni = desc(errs, "implied-H2 net income error @Q2 guidance", "%")
for d in det:
    print(f"      {d}")
# down-cycle only
errs_dc = [num(r["error_pct"]) for r in sub if r["cycle_phase"] == "down_cycle" and num(r["error_pct"]) is not None]
desc(errs_dc, "  ... restricted to down_cycle years", "%")

print("\n" + "=" * 100)
print("PART 3 -- ASYMMETRY RATIO: revenue vs bottom line, on the SAME inference and years")
print("=" * 100)
byfy_rev = {}
for seg in ("PPA", "SAT", "CF"):
    pass
sub_ni = {int(r["fiscal_year"]): num(r["error_pct"])
          for r in gva if r["metric"] == "fy_h2_net_income_implied_by_q2_guidance"}
# enterprise implied-H2 revenue from segment guides, matched years
match_years, rev_errs, ni_errs = [], [], []
guides = defaultdict(dict)
for metric, seg in (("fy_segment_sales_growth_ppa", "PPA"),
                    ("fy_segment_sales_growth_sat", "SAT"),
                    ("fy_segment_sales_growth_cf", "CF")):
    for r in gva:
        if r["metric"] == metric and r["vintage_quarter"] == "Q2":
            guides[int(r["fiscal_year"])][seg] = num(r["guidance_mid"])
for fy, g in sorted(guides.items()):
    if len(g) < 3 or any(v is None for v in g.values()):
        continue
    imp, act = 0.0, 0.0
    ok = True
    for seg, gm in g.items():
        prior = [seg_sales.get((seg, fy - 1, q)) for q in (1, 2, 3, 4)]
        h1 = [seg_sales.get((seg, fy, q)) for q in (1, 2)]
        h2 = [seg_sales.get((seg, fy, q)) for q in (3, 4)]
        if any(v is None for v in prior + h1 + h2):
            ok = False
            break
        imp += sum(prior) * (1 + gm / 100.0) - sum(h1)
        act += sum(h2)
    if not ok or fy not in sub_ni:
        continue
    e = 100.0 * (act / imp - 1.0)
    match_years.append(fy)
    rev_errs.append(e)
    ni_errs.append(sub_ni[fy])
    print(f"  FY{fy}: H2 equip sales err {e:+6.1f}%   H2 net income err {sub_ni[fy]:+7.1f}%")
r1 = desc(rev_errs, "H2 equipment-sales error @Q2 guidance", "%")
r2 = desc(ni_errs, "H2 net-income error @Q2 guidance", "%")
if r1 and r2 and r1["n"] > 1:
    print(f"\n  ==> ASYMMETRY RATIO sd(bottom line)/sd(revenue) = {r2['sd']/r1['sd']:.2f}x on n={r1['n']} matched years")
    print(f"  ==> MAE ratio = {r2['mae']/r1['mae']:.2f}x")

print("\n" + "=" * 100)
print("PART 4 -- CONVERTING MEASURED ERROR INTO RECOMMENDED Q3 RANGE WIDTHS")
print("=" * 100)

# Deere's own FY2026 guidance arithmetic, verified ground truth
H1 = {"PPA": 7666.0, "SAT": 5653.0, "CF": 6460.0}
FY25 = {"PPA": 17311.0, "SAT": 10224.0, "CF": 11382.0}
G = {"PPA": (-10.0, -5.0), "SAT": (14.0, 16.0), "CF": (19.0, 21.0)}
print("\nH2 FY2026 equipment sales implied by the 21-May-2026 segment guidance:")
tot_lo = tot_hi = 0.0
for s in ("PPA", "SAT", "CF"):
    lo = FY25[s] * (1 + G[s][0] / 100) - H1[s]
    hi = FY25[s] * (1 + G[s][1] / 100) - H1[s]
    tot_lo += lo
    tot_hi += hi
    print(f"  {s}: FY25 {FY25[s]:.0f} x guide {G[s]} -> H2 {lo:.0f} to {hi:.0f}  (H1 was {H1[s]:.0f})")
print(f"  TOTAL H2 equipment sales implied: {tot_lo:.0f} to {tot_hi:.0f}  (mid {0.5*(tot_lo+tot_hi):.0f})")
mid = 0.5 * (tot_lo + tot_hi)
print(f"  Guidance range alone spans {100*(tot_hi-tot_lo)/mid:.1f}% of the midpoint -- BEFORE any forecast error.")

print("""
  Note this is an H2 number. Splitting H2 into Q3 and Q4 adds a second, independent
  uncertainty that the guidance does NOT pin down -- management gave only qualitative
  cadence ("Q4 a bit stronger than Q3"). Quantify that split risk from history:""")
for seg in ("PPA", "SAT", "CF"):
    ratios = []
    for fy in range(2021, 2026):
        q3 = seg_sales.get((seg, fy, 3))
        q4 = seg_sales.get((seg, fy, 4))
        if q3 and q4:
            ratios.append(q3 / (q3 + q4))
    if len(ratios) > 1:
        print(f"    {seg}: Q3 share of H2 sales, n={len(ratios)} mean={st.mean(ratios):.3f} "
              f"sd={st.stdev(ratios):.3f} range {min(ratios):.3f}-{max(ratios):.3f}")
# enterprise
ratios = []
for fy in range(2013, 2026):
    q3 = rev_act.get((fy, 3))
    q4 = rev_act.get((fy, 4))
    if q3 and q4:
        ratios.append(q3 / (q3 + q4))
print(f"    ENTERPRISE NSR: Q3 share of H2, n={len(ratios)} mean={st.mean(ratios):.3f} "
      f"sd={st.stdev(ratios):.3f} range {min(ratios):.3f}-{max(ratios):.3f}")

print("""
  A sd of ~1.5-3pp on the Q3-share-of-H2 translates, at a ~50% share, into roughly
  3-6% of additional Q3-level revenue uncertainty that is ORTHOGONAL to the H2 guidance
  error. Total Q3 revenue uncertainty = sqrt(H2 guide error^2 + split error^2).""")

print("\n" + "=" * 100)
print("PART 5 -- Q3-SPECIFIC MARGIN/COST RESIDUAL, PPA")
print("=" * 100)
ks = sorted(k for k in bq if k[0] == "PPA")
print("  PPA Q3 bridge history (USDm):")
print(f"  {'FY':<6}{'open':>7}{'vol/mix':>9}{'price':>7}{'ccy':>6}{'warr':>7}{'prodcost':>10}{'SA&G':>7}{'spec':>6}{'other':>7}{'close':>8}{'costblk':>9}")
q3cost = []
for k in ks:
    if k[2] != 3:
        continue
    b = bq[k]
    cb = sum(b.get(c, 0.0) for c in COST)
    q3cost.append(cb)
    print(f"  {k[1]:<6}{b.get('opening_operating_profit',0):>7.0f}{b.get('volume_mix',0):>9.0f}"
          f"{b.get('price',0):>7.0f}{b.get('currency',0):>6.0f}{b.get('warranty',0):>7.0f}"
          f"{b.get('production_costs',0):>10.0f}{b.get('sag_rd',0):>7.0f}{b.get('special_items',0):>6.0f}"
          f"{b.get('other',0):>7.0f}{b.get('closing_operating_profit',0):>8.0f}{cb:>9.0f}")
desc(q3cost, "PPA Q3 cost block (prodcost+warr+SA&G+other)", "USDm")
allcost = [sum(bq[k].get(c, 0.0) for c in COST) for k in ks]
desc(allcost, "PPA all-quarter cost block", "USDm")

print("\nDone. No Q3 FY2026 actuals were read or produced.")


print("\n" + "=" * 100)
print("PART 6 -- Q3-LEVEL UNCERTAINTY FOR THE THREE TARGETS, BUILT FROM MEASURED ERROR")
print("=" * 100)

# --- 6a implied-H2 PPA OPERATING PROFIT error at Q2 guidance --------------------------
print("\n[6a] implied-H2 PPA OPERATING PROFIT error @Q2 guidance")
print("     FY OP implied = (FY sales guide) x (FY margin guide); H2 = that minus H1 actual OP")
gm_sales = {int(r["fiscal_year"]): num(r["guidance_mid"]) for r in gva
            if r["metric"] == "fy_segment_sales_growth_ppa" and r["vintage_quarter"] == "Q2"}
gm_marg = {int(r["fiscal_year"]): num(r["guidance_mid"]) for r in gva
           if r["metric"] == "fy_ppa_operating_margin" and r["vintage_quarter"] == "Q2"}
errs, det = [], []
for fy in sorted(set(gm_sales) & set(gm_marg)):
    prior = [seg_sales.get(("PPA", fy - 1, q)) for q in (1, 2, 3, 4)]
    h1s = [seg_sales.get(("PPA", fy, q)) for q in (1, 2)]
    h1o = [seg_op.get(("PPA", fy, q)) for q in (1, 2)]
    h2o = [seg_op.get(("PPA", fy, q)) for q in (3, 4)]
    if any(v is None for v in prior + h1s + h1o + h2o):
        continue
    fy_sales = sum(prior) * (1 + gm_sales[fy] / 100.0)
    fy_op = fy_sales * gm_marg[fy] / 100.0
    h2_imp = fy_op - sum(h1o)
    h2_act = sum(h2o)
    e = 100.0 * (h2_act / h2_imp - 1.0)
    errs.append(e)
    det.append(f"FY{fy} H2 PPA OP implied {h2_imp:7.0f} actual {h2_act:7.0f} err {e:+7.1f}%")
ppa_h2op = desc(errs, "implied-H2 PPA operating-profit error @Q2", "%")
for d in det:
    print(f"      {d}")

# --- 6b Q3 share of H2, for the profit lines ------------------------------------------
print("\n[6b] Q3 share of H2 for the PROFIT lines (the split risk guidance does not pin down)")


def q3share(getter, key_seg, years):
    out = []
    for fy in years:
        a = getter(key_seg, fy, 3)
        b = getter(key_seg, fy, 4)
        if a is None or b is None or (a + b) == 0:
            continue
        out.append(a / (a + b))
    return out


g_op = lambda s, fy, q: seg_op.get((s, fy, q))
for seg in ("PPA", "SAT", "CF"):
    sh = q3share(g_op, seg, range(2021, 2026))
    if len(sh) > 1:
        print(f"    {seg} operating profit: n={len(sh)} mean={st.mean(sh):.3f} sd={st.stdev(sh):.3f} "
              f"range {min(sh):.3f}-{max(sh):.3f}  -> relative sd on Q3 = {100*st.stdev(sh)/st.mean(sh):.1f}%")

eps_act = {}
for r in pred:
    if r["series_id"] == "de_eps_actual_usd":
        eps_act[(int(r["fiscal_year"]), int(r["fiscal_quarter"]))] = num(r["value"])
sh = []
for fy in range(2013, 2026):
    a, b = eps_act.get((fy, 3)), eps_act.get((fy, 4))
    if a is None or b is None or (a + b) == 0:
        continue
    sh.append(a / (a + b))
print(f"    DILUTED EPS: n={len(sh)} mean={st.mean(sh):.3f} sd={st.stdev(sh):.3f} "
      f"range {min(sh):.3f}-{max(sh):.3f}  -> relative sd on Q3 = {100*st.stdev(sh)/st.mean(sh):.1f}%")
eps_sh = (st.mean(sh), st.stdev(sh))

# --- 6c combine ------------------------------------------------------------------------
print("\n[6c] COMBINED Q3 uncertainty = sqrt( H2-guidance error^2 + Q3/H2-split error^2 )")
print("     (the two are measured on different information and are treated as independent;")
print("      that assumption is stated, not proven)")


def comb(h2sd, splitsd, splitmean, label):
    rel = 100.0 * splitsd / splitmean
    tot = math.sqrt(h2sd ** 2 + rel ** 2)
    print(f"    {label:<34} H2err={h2sd:5.2f}%  split={rel:5.2f}%  -> Q3 1sigma = {tot:5.2f}%")
    return tot


rev_tot = comb(2.40, 0.019, 0.507, "Enterprise revenue")
ppa_rev_tot = comb(3.07, 0.034, 0.488, "PPA net sales")
ppa_op_tot = comb(ppa_h2op["sd"] if ppa_h2op else float("nan"), 0.0, 1.0, "PPA operating profit (H2 only)")
sh_ppa_op = q3share(g_op, "PPA", range(2021, 2026))
ppa_op_tot = comb(ppa_h2op["sd"], st.stdev(sh_ppa_op), st.mean(sh_ppa_op), "PPA operating profit (combined)")

ni_recent = [num(r["error_pct"]) for r in gva
             if r["metric"] == "fy_h2_net_income_implied_by_q2_guidance" and int(r["fiscal_year"]) >= 2021]
ni_ex = [num(r["error_pct"]) for r in gva
         if r["metric"] == "fy_h2_net_income_implied_by_q2_guidance"
         and int(r["fiscal_year"]) not in (2016, 2020)]
desc(ni_recent, "H2 net-income err, FY2021-25 only", "%")
desc(ni_ex, "H2 net-income err, ex FY2016 & FY2020 outliers", "%")
eps_tot = comb(st.stdev(ni_ex), eps_sh[1], eps_sh[0], "Diluted EPS (ex-outlier NI err)")
eps_tot_r = comb(st.stdev(ni_recent), eps_sh[1], eps_sh[0], "Diluted EPS (FY2021-25 NI err)")

# --- 6d small-sample honesty -----------------------------------------------------------
print("\n[6d] SMALL-SAMPLE INFLATION. n=5 sd estimates are badly under-determined.")
print("     Upper 90% confidence bound on sigma = s * sqrt((n-1)/chi2_{0.05,n-1}).")
CHI2_05 = {4: 0.7107, 5: 1.1455, 10: 3.9403, 12: 5.2260}
for lab, s, n in (("H2 equip sales err", 2.40, 5), ("H2 PPA sales err", 3.07, 5),
                  ("H2 PPA OP err", ppa_h2op["sd"], 5), ("H2 NI err (ex-outlier)", st.stdev(ni_ex), 11)):
    k = 4 if n == 5 else 10
    print(f"    {lab:<26} s={s:6.2f}%  90% upper bound on sigma = {s*math.sqrt(k/CHI2_05[k]):6.2f}%")

print("\n[6e] CENTRAL-CASE ARITHMETIC (guidance only -- NOT a forecast)")
q3share_ent = 0.49
fs_other = 1591.0
for nm, share in (("Q4>Q3 as guided (0.49)", 0.49), ("historical mean (0.507)", 0.507)):
    q3_equip = mid * share
    print(f"    {nm:<26} Q3 equipment {q3_equip:8.0f} + FS/other {fs_other:.0f} = NSR {q3_equip+fs_other:8.0f}")
print("    +/-1sigma at the measured combined error:")
base = mid * 0.49 + fs_other
for s in (rev_tot, rev_tot * 1.5):
    print(f"      +/-{s:4.2f}%  ->  {base*(1-s/100):8.0f} to {base*(1+s/100):8.0f}  (+/- {base*s/100:5.0f})")
