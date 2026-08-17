#!/usr/bin/env python3
"""
Deere & Company -- variance decomposition test of the "order book pre-determines
revenue, inputs move margin" hypothesis.

Reads  <SCRATCH>/de_panel.json   (built by de_build_panel.py)
Writes /Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_predictability.csv

Method
------
One-quarter-ahead NAIVE forecasts using ONLY information available at the Q(n-1)
earnings release:

  yoy_carry   (primary)  x_hat(n) = x(n-4) * [ x(n-1) / x(n-5) ]      (levels, logs)
                         m_hat(n) = m(n-4) + [ m(n-1) - m(n-5) ]      (margin, bps)
  seasonal    (control)  x_hat(n) = x(n-4);  m_hat(n) = m(n-4)

Errors
------
  revenue   e_rev  = 100 * ln( Rev(n) / Rev_hat(n) )        (~ % error)
  margin    e_bps  = 100 * ( m(n) - m_hat(n) )              (bps, m in %)
            e_mlog = 100 * ln( m(n) / m_hat(n) )            (~ % error, comparable to e_rev)
  eps       e_eps  = 100 * ln( EPS(n) / EPS_hat(n) )        (positive-EPS quarters only)

Because  OP = Rev * m  exactly,  e_op = e_rev + e_mlog  exactly (in logs).  That
gives an exact covariance decomposition of profit/EPS surprise into a revenue
component and a margin component:

  Var(e_op) = Cov(e_rev, e_op) + Cov(e_mlog, e_op)

Statistics
----------
Variance equality on PAIRED samples is tested with the Pitman-Morgan test
(correlation of sum and difference).  p-values from a self-contained incomplete
beta function -- no third-party libraries.
"""
import csv
import json
import math
import os
import statistics as st

SCRATCH = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"
OUTDIR = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere"
CSVPATH = os.path.join(OUTDIR, "de_predictability.csv")

SRC_8K = "Deere 8-K earnings releases (offline corpus), segment tables"
SRC_MIX = "Deere 8-K earnings releases + SEC EDGAR XBRL companyfacts CIK 315189"


# ------------------------------------------------------------------ statistics
def betacf(a, b, x):
    MAXIT, EPS, FPMIN = 200, 3e-16, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
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


def betai(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return math.exp(lbeta) * betacf(a, b, x) / a
    return 1.0 - math.exp(lbeta) * betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t, df):
    if df <= 0:
        return float("nan")
    return betai(df / 2.0, 0.5, df / (df + t * t))


def pearson(x, y):
    n = len(x)
    if n < 3:
        return float("nan")
    mx, my = st.fmean(x), st.fmean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx <= 0 or syy <= 0:
        return float("nan")
    return sxy / math.sqrt(sxx * syy)


def pitman_morgan(x, y):
    """Paired test of H0: Var(x) == Var(y).  Returns (F=s2x/s2y, r, t, df, p)."""
    n = len(x)
    if n < 4:
        return (float("nan"),) * 5
    s = [a + b for a, b in zip(x, y)]
    d = [a - b for a, b in zip(x, y)]
    r = pearson(s, d)
    df = n - 2
    t = r * math.sqrt(df / max(1e-12, 1 - r * r))
    return (st.variance(x) / st.variance(y), r, t, df, t_two_sided_p(t, df))


def cov(x, y):
    n = len(x)
    mx, my = st.fmean(x), st.fmean(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (n - 1)


def desc(v):
    n = len(v)
    return {"n": n,
            "mean": st.fmean(v) if n else float("nan"),
            "sd": st.stdev(v) if n > 1 else float("nan"),
            "mae": st.fmean([abs(a) for a in v]) if n else float("nan"),
            "rmse": math.sqrt(st.fmean([a * a for a in v])) if n else float("nan")}


# ------------------------------------------------------------------ data
panel = json.load(open(os.path.join(SCRATCH, "de_panel.json")))["panel"]
KEYS = sorted(panel, key=lambda k: (int(k[:4]), int(k[-1])))
IDX = {k: i for i, k in enumerate(KEYS)}


def key_of(fy, fq):
    return f"{fy}Q{fq}"


def lag(k, n):
    """n quarters before k on Deere's fiscal calendar (independent of gaps in data)."""
    fy, fq = int(k[:4]), int(k[-1])
    t = fy * 4 + (fq - 1) - n
    return key_of(t // 4, t % 4 + 1)


def get(k, field):
    e = panel.get(k)
    if e is None:
        return None
    v = e.get(field)
    return v


ROWS = []


def emit(series_id, k, segment, component, value, units, source, notes=""):
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return
    e = panel.get(k, {})
    ROWS.append({"series_id": series_id,
                 "period_end": e.get("period_end") or "",
                 "fiscal_year": int(k[:4]), "fiscal_quarter": int(k[-1]),
                 "segment": segment, "component": component,
                 "value": round(value, 4), "units": units,
                 "source": source, "notes": notes})


# ------------------------------------------------------------------ forecasts
SEGMENTS = ["PPA", "SAT", "AG", "CF", "EQUIP"]

err = {}          # (kind, seg, rule) -> {quarter: error}
fcst = {}         # for auditability


def build_level_errors(field, kind, seg, source, unit_note):
    for k in KEYS:
        x0, x4, x1, x5 = (get(k, field), get(lag(k, 4), field),
                          get(lag(k, 1), field), get(lag(k, 5), field))
        if x0 is None or x4 is None or x0 <= 0 or x4 <= 0:
            continue
        # seasonal naive
        e_s = 100.0 * math.log(x0 / x4)
        err.setdefault((kind, seg, "seasonal"), {})[k] = e_s
        fcst.setdefault((kind, seg, "seasonal"), {})[k] = x4
        # yoy carry
        if x1 is None or x5 is None or x1 <= 0 or x5 <= 0:
            continue
        f = x4 * (x1 / x5)
        err.setdefault((kind, seg, "yoy_carry"), {})[k] = 100.0 * math.log(x0 / f)
        fcst.setdefault((kind, seg, "yoy_carry"), {})[k] = f


def build_margin_errors(seg, source):
    field = f"margin_{seg}"
    for k in KEYS:
        m0, m4, m1, m5 = (get(k, field), get(lag(k, 4), field),
                          get(lag(k, 1), field), get(lag(k, 5), field))
        if m0 is None or m4 is None:
            continue
        err.setdefault(("margin_bps", seg, "seasonal"), {})[k] = 100.0 * (m0 - m4)
        fcst.setdefault(("margin", seg, "seasonal"), {})[k] = m4
        if m0 > 0 and m4 > 0:
            err.setdefault(("margin_log", seg, "seasonal"), {})[k] = 100.0 * math.log(m0 / m4)
        if m1 is None or m5 is None:
            continue
        f = m4 + (m1 - m5)
        err.setdefault(("margin_bps", seg, "yoy_carry"), {})[k] = 100.0 * (m0 - f)
        fcst.setdefault(("margin", seg, "yoy_carry"), {})[k] = f
        if m0 > 0 and f > 0:
            err.setdefault(("margin_log", seg, "yoy_carry"), {})[k] = 100.0 * math.log(m0 / f)


build_level_errors("total_rev", "revenue", "TOTAL", SRC_MIX, "USDm")
build_level_errors("eps_diluted", "eps", "TOTAL", SRC_MIX, "USD")
for s in SEGMENTS:
    build_level_errors(f"sales_{s}", "revenue", s, SRC_8K, "USDm")
    build_level_errors(f"op_{s}", "op", s, SRC_8K, "USDm")
    build_margin_errors(s, SRC_8K)


# ------------------------------------------------------------------ emit series
for k in KEYS:
    e = panel[k]
    src = SRC_MIX if "EDGAR XBRL" in e.get("sources", []) else SRC_8K
    emit("de_revenue_actual_usdm", k, "TOTAL", "net_sales_and_revenues",
         e.get("total_rev"), "USDm", src)
    emit("de_eps_actual_usd", k, "TOTAL", "diluted_eps_gaap",
         e.get("eps_diluted"), "USD", src,
         "; ".join(e.get("notes", [])))
    for s in SEGMENTS:
        emit("de_segment_sales_usdm", k, s, "net_sales", e.get(f"sales_{s}"), "USDm", SRC_8K,
             "AG = A&T pre-FY2021, PPA+SAT thereafter" if s == "AG" else
             ("EQUIP = AG + CF" if s == "EQUIP" else ""))
        emit("de_segment_op_usdm", k, s, "operating_profit", e.get(f"op_{s}"), "USDm", SRC_8K)
        emit("de_segment_margin_pct", k, s, "operating_margin", e.get(f"margin_{s}"),
             "percent", SRC_8K)

for rule in ("yoy_carry", "seasonal"):
    for k, v in sorted(err.get(("revenue", "TOTAL", rule), {}).items(),
                       key=lambda kv: IDX.get(kv[0], 0)):
        emit("de_revenue_fcst_error_pct", k, "TOTAL", rule, v, "percent_log", SRC_MIX,
             "100*ln(actual/forecast); forecast uses only data through Q(n-1)")
        emit("de_revenue_fcst_usdm", k, "TOTAL", rule,
             fcst[("revenue", "TOTAL", rule)][k], "USDm", SRC_MIX)
    for k, v in sorted(err.get(("eps", "TOTAL", rule), {}).items(),
                       key=lambda kv: IDX.get(kv[0], 0)):
        emit("de_eps_fcst_error_pct", k, "TOTAL", rule, v, "percent_log", SRC_MIX,
             "positive-EPS quarters only; loss quarters excluded, not zeroed")
        emit("de_eps_fcst_usd", k, "TOTAL", rule,
             fcst[("eps", "TOTAL", rule)][k], "USD", SRC_MIX)
    for s in SEGMENTS:
        for k, v in sorted(err.get(("margin_bps", s, rule), {}).items(),
                           key=lambda kv: IDX.get(kv[0], 0)):
            emit("de_margin_fcst_error_bps", k, s, rule, v, "bps", SRC_8K,
                 "actual minus forecast operating margin")
        for k, v in sorted(err.get(("margin_log", s, rule), {}).items(),
                           key=lambda kv: IDX.get(kv[0], 0)):
            emit("de_margin_fcst_error_pct", k, s, rule, v, "percent_log", SRC_8K,
                 "100*ln(actual/forecast margin) - scale-free, comparable to revenue error")
        for k, v in sorted(err.get(("revenue", s, rule), {}).items(),
                           key=lambda kv: IDX.get(kv[0], 0)):
            emit("de_segment_sales_fcst_error_pct", k, s, rule, v, "percent_log", SRC_8K)
        for k, v in sorted(err.get(("op", s, rule), {}).items(),
                           key=lambda kv: IDX.get(kv[0], 0)):
            emit("de_segment_op_fcst_error_pct", k, s, rule, v, "percent_log", SRC_8K)


# ------------------------------------------------------------------ analysis
REPORT = []


def P(*a):
    line = " ".join(str(x) for x in a)
    REPORT.append(line)
    print(line)


def paired(a, b):
    ks = sorted(set(a) & set(b), key=lambda k: IDX.get(k, 0))
    return ks, [a[k] for k in ks], [b[k] for k in ks]


P("=" * 78)
P("TEST 1  --  IS REVENUE MORE PREDICTABLE ONE QUARTER AHEAD THAN MARGIN?")
P("=" * 78)
P("All errors are 100*ln(actual/forecast) so revenue and margin are on the same")
P("scale-free footing.  Forecast rule 'yoy_carry' is the primary; 'seasonal' is a")
P("control.  n = number of quarters with a computable forecast.")
P("")

summary_rows = []
for rule in ("yoy_carry", "seasonal"):
    P(f"--- rule = {rule} ---")
    P(f"{'series':34s} {'n':>3s} {'mean':>8s} {'sd':>8s} {'MAE':>8s} {'RMSE':>8s}")
    items = [("revenue TOTAL (%)", ("revenue", "TOTAL", rule))]
    for s in SEGMENTS:
        items.append((f"revenue {s} (%)", ("revenue", s, rule)))
    for s in SEGMENTS:
        items.append((f"margin {s} (% of margin)", ("margin_log", s, rule)))
    for s in SEGMENTS:
        items.append((f"margin {s} (bps)", ("margin_bps", s, rule)))
    for s in SEGMENTS:
        items.append((f"op profit {s} (%)", ("op", s, rule)))
    items.append(("EPS TOTAL (%)", ("eps", "TOTAL", rule)))
    for lab, key in items:
        d = err.get(key)
        if not d:
            continue
        st_ = desc(list(d.values()))
        P(f"{lab:34s} {st_['n']:3d} {st_['mean']:8.2f} {st_['sd']:8.2f} "
          f"{st_['mae']:8.2f} {st_['rmse']:8.2f}")
        summary_rows.append((rule, lab, key, st_))
    P("")

P("--- RATIO of margin unpredictability to revenue unpredictability (paired) ---")
P("Pitman-Morgan paired test of equal variance.  ratio = sd(margin)/sd(revenue)")
P(f"{'segment':10s} {'n':>3s} {'sd_rev':>7s} {'sd_mgn':>7s} {'ratio':>6s} "
  f"{'MAE_rev':>8s} {'MAE_mgn':>8s} {'r_pm':>6s} {'p':>7s}")
ratio_tbl = {}
for s in SEGMENTS:
    a = err.get(("revenue", s, "yoy_carry"), {})
    b = err.get(("margin_log", s, "yoy_carry"), {})
    ks, x, y = paired(a, b)
    if len(ks) < 6:
        continue
    F, r, t, df, p = pitman_morgan(y, x)
    ratio = st.stdev(y) / st.stdev(x)
    ratio_tbl[s] = (len(ks), st.stdev(x), st.stdev(y), ratio,
                    st.fmean([abs(v) for v in x]), st.fmean([abs(v) for v in y]), r, p,
                    ks[0], ks[-1])
    P(f"{s:10s} {len(ks):3d} {st.stdev(x):7.2f} {st.stdev(y):7.2f} {ratio:6.2f} "
      f"{st.fmean([abs(v) for v in x]):8.2f} {st.fmean([abs(v) for v in y]):8.2f} "
      f"{r:6.2f} {p:7.4f}   [{ks[0]}..{ks[-1]}]")

# enterprise-level: total revenue vs equipment margin
a = err.get(("revenue", "TOTAL", "yoy_carry"), {})
b = err.get(("margin_log", "EQUIP", "yoy_carry"), {})
ks, x, y = paired(a, b)
F, r, t, df, p = pitman_morgan(y, x)
P(f"{'TOTALrev/':10s} {len(ks):3d} {st.stdev(x):7.2f} {st.stdev(y):7.2f} "
  f"{st.stdev(y)/st.stdev(x):6.2f} {st.fmean([abs(v) for v in x]):8.2f} "
  f"{st.fmean([abs(v) for v in y]):8.2f} {r:6.2f} {p:7.4f}   "
  f"[{ks[0]}..{ks[-1]}]  (EQUIP margin)")
ent = (len(ks), st.stdev(x), st.stdev(y), st.stdev(y) / st.stdev(x), p)
P("")

P("=" * 78)
P("TEST 2  --  DECOMPOSITION OF PROFIT / EPS SURPRISE")
P("=" * 78)
P("Exact identity in logs:  e_op = e_revenue + e_margin.")
P("Variance shares from  Var(e_op) = Cov(e_rev,e_op) + Cov(e_mgn,e_op)  (sums to 1).")
P("")
P(f"{'segment':10s} {'n':>3s} {'sd(e_op)':>9s} {'rev share':>10s} {'mgn share':>10s} "
  f"{'corr(rev,mgn)':>14s}")
decomp = {}
for s in SEGMENTS:
    a = err.get(("revenue", s, "yoy_carry"), {})
    b = err.get(("margin_log", s, "yoy_carry"), {})
    ks, x, y = paired(a, b)
    if len(ks) < 6:
        continue
    op = [p_ + q_ for p_, q_ in zip(x, y)]
    vop = st.variance(op)
    sr, sm = cov(x, op) / vop, cov(y, op) / vop
    decomp[s] = (len(ks), math.sqrt(vop), sr, sm, pearson(x, y), ks[0], ks[-1])
    P(f"{s:10s} {len(ks):3d} {math.sqrt(vop):9.2f} {sr:10.3f} {sm:10.3f} "
      f"{pearson(x, y):14.2f}   [{ks[0]}..{ks[-1]}]")
P("")
P("EPS surprise decomposition (enterprise): e_eps = e_rev + e_marginEQUIP + e_residual")
P("where residual absorbs financial services, corporate/reconciling items, tax rate")
P("and share count.  Shares are Cov(component, e_eps)/Var(e_eps) and sum to 1.")
ar = err.get(("revenue", "TOTAL", "yoy_carry"), {})
am = err.get(("margin_log", "EQUIP", "yoy_carry"), {})
ae = err.get(("eps", "TOTAL", "yoy_carry"), {})
ks = sorted(set(ar) & set(am) & set(ae), key=lambda k: IDX.get(k, 0))
xr = [ar[k] for k in ks]
xm = [am[k] for k in ks]
xe = [ae[k] for k in ks]
xres = [e - r_ - m_ for e, r_, m_ in zip(xe, xr, xm)]
ve = st.variance(xe)
eps_shares = (len(ks), math.sqrt(ve), cov(xr, xe) / ve, cov(xm, xe) / ve, cov(xres, xe) / ve)
P(f"  n={len(ks)}  sd(e_eps)={math.sqrt(ve):.1f}%   "
  f"revenue share={cov(xr, xe)/ve:.3f}   margin share={cov(xm, xe)/ve:.3f}   "
  f"residual share={cov(xres, xe)/ve:.3f}   [{ks[0]}..{ks[-1]}]")
P(f"  sd(e_rev)={st.stdev(xr):.1f}%  sd(e_margin)={st.stdev(xm):.1f}%  "
  f"sd(e_residual)={st.stdev(xres):.1f}%")
P("")

# ---- guidance-implied check (independent of the naive model)
P("Guidance-implied cross-check: at Q(n-1) Deere publishes FY net-income guidance.")
P("Implied Q(n) net income = (guidance midpoint - YTD actual) allocated by the")
P("prior-year seasonal share of the remaining quarters.")
gerr = {}
for k in KEYS:
    fy, fq = int(k[:4]), int(k[-1])
    if fq == 1:
        continue
    prev = lag(k, 1)
    g_lo, g_hi = get(prev, "guidance_fy_ni_lo"), get(prev, "guidance_fy_ni_hi")
    if g_lo is None:
        continue
    ytd = []
    ok = True
    for q in range(1, fq):
        v = get(key_of(fy, q), "net_income")
        if v is None:
            ok = False
            break
        ytd.append(v)
    if not ok:
        continue
    remain_now = (g_lo + g_hi) / 2.0 - sum(ytd)
    py = [get(key_of(fy - 1, q), "net_income") for q in range(fq, 5)]
    if any(v is None for v in py) or sum(py) == 0:
        continue
    share = py[0] / sum(py)
    f = remain_now * share
    act = get(k, "net_income")
    if act is None or f <= 0 or act <= 0:
        continue
    gerr[k] = 100.0 * math.log(act / f)
    emit("de_ni_guidance_fcst_error_pct", k, "TOTAL", "guidance_implied", gerr[k],
         "percent_log", SRC_8K,
         "FY NI guidance midpoint at Q(n-1) less YTD, split by prior-year seasonal share")
gd = desc(list(gerr.values()))
P(f"  net income: n={gd['n']}  mean={gd['mean']:.1f}%  sd={gd['sd']:.1f}%  "
  f"MAE={gd['mae']:.1f}%")
# compare with revenue predictability on the same quarters
ks2 = sorted(set(gerr) & set(ar), key=lambda k: IDX.get(k, 0))
if len(ks2) >= 6:
    xg = [gerr[k] for k in ks2]
    xr2 = [ar[k] for k in ks2]
    F, r, t, df, p = pitman_morgan(xg, xr2)
    P(f"  paired vs revenue error on the same {len(ks2)} quarters: "
      f"sd(NI)={st.stdev(xg):.1f}% vs sd(rev)={st.stdev(xr2):.1f}%  "
      f"ratio={st.stdev(xg)/st.stdev(xr2):.2f}  Pitman-Morgan p={p:.4f}")
    guid_cmp = (len(ks2), st.stdev(xg), st.stdev(xr2), st.stdev(xg) / st.stdev(xr2), p)
else:
    guid_cmp = None
P("")

P("=" * 78)
P("TEST 3  --  DOES PREDICTABILITY DIFFER BY QUARTER, AND AT TURNING POINTS?")
P("=" * 78)
byq = {}
P("(a) by fiscal quarter, yoy_carry rule")
P(f"{'series':26s} {'Q1 n/MAE/sd':>20s} {'Q2 n/MAE/sd':>20s} "
  f"{'Q3 n/MAE/sd':>20s} {'Q4 n/MAE/sd':>20s}")
for lab, key in (("revenue TOTAL (%)", ("revenue", "TOTAL", "yoy_carry")),
                 ("revenue PPA (%)", ("revenue", "PPA", "yoy_carry")),
                 ("revenue AG (%)", ("revenue", "AG", "yoy_carry")),
                 ("margin AG (bps)", ("margin_bps", "AG", "yoy_carry")),
                 ("margin PPA (bps)", ("margin_bps", "PPA", "yoy_carry")),
                 ("margin EQUIP (bps)", ("margin_bps", "EQUIP", "yoy_carry")),
                 ("EPS TOTAL (%)", ("eps", "TOTAL", "yoy_carry"))):
    d = err.get(key)
    if not d:
        continue
    parts = []
    for q in (1, 2, 3, 4):
        v = [val for k, val in d.items() if int(k[-1]) == q]
        byq[(lab, q)] = desc(v) if v else None
        if len(v) >= 2:
            parts.append(f"{len(v):2d}/{st.fmean([abs(a) for a in v]):6.1f}/"
                         f"{st.stdev(v):6.1f}")
        else:
            parts.append(f"{len(v):2d}/     ./     .")
    P(f"{lab:26s} " + " ".join(f"{p_:>20s}" for p_ in parts))
P("")

P("(b) turning points.  A quarter is 'turning' if the sign of total-revenue YoY")
P("    growth differs from the prior quarter's sign, or if YoY growth changes by")
P("    more than 15pp versus the prior quarter.")
yoy = {}
for k in KEYS:
    a_, b_ = get(k, "total_rev"), get(lag(k, 4), "total_rev")
    if a_ and b_:
        yoy[k] = 100.0 * (a_ / b_ - 1.0)
turn = set()
for k in KEYS:
    p_ = lag(k, 1)
    if k in yoy and p_ in yoy:
        flip = (yoy[k] > 0) != (yoy[p_] > 0)
        jump = abs(yoy[k] - yoy[p_]) > 15.0
        if flip or jump:
            turn.add(k)
P(f"    turning quarters identified: {len(turn)} of {len(yoy)} with YoY growth")
P(f"{'series':26s} {'turn n':>7s} {'turn MAE':>9s} {'calm n':>7s} {'calm MAE':>9s} "
  f"{'ratio':>6s}")
tp_tbl = {}
for lab, key in (("revenue TOTAL (%)", ("revenue", "TOTAL", "yoy_carry")),
                 ("revenue PPA (%)", ("revenue", "PPA", "yoy_carry")),
                 ("revenue AG (%)", ("revenue", "AG", "yoy_carry")),
                 ("margin AG (bps)", ("margin_bps", "AG", "yoy_carry")),
                 ("margin PPA (bps)", ("margin_bps", "PPA", "yoy_carry")),
                 ("margin EQUIP (bps)", ("margin_bps", "EQUIP", "yoy_carry")),
                 ("EPS TOTAL (%)", ("eps", "TOTAL", "yoy_carry"))):
    d = err.get(key)
    if not d:
        continue
    t_ = [v for k, v in d.items() if k in turn]
    c_ = [v for k, v in d.items() if k not in turn]
    if len(t_) < 3 or len(c_) < 3:
        continue
    mt, mc = st.fmean([abs(a) for a in t_]), st.fmean([abs(a) for a in c_])
    tp_tbl[lab] = (len(t_), mt, len(c_), mc, mt / mc)
    P(f"{lab:26s} {len(t_):7d} {mt:9.1f} {len(c_):7d} {mc:9.1f} {mt/mc:6.2f}")
P("")

# ---- Q3-specific detail
P("(c) Q3 detail, all available Q3s (yoy_carry):")
for lab, key, unit in (("revenue TOTAL", ("revenue", "TOTAL", "yoy_carry"), "%"),
                       ("revenue PPA", ("revenue", "PPA", "yoy_carry"), "%"),
                       ("margin PPA", ("margin_bps", "PPA", "yoy_carry"), "bps"),
                       ("margin AG", ("margin_bps", "AG", "yoy_carry"), "bps"),
                       ("EPS", ("eps", "TOTAL", "yoy_carry"), "%")):
    d = err.get(key, {})
    v = sorted(((k, val) for k, val in d.items() if int(k[-1]) == 3),
               key=lambda kv: IDX.get(kv[0], 0))
    P(f"  {lab:14s} ({unit}): " + "  ".join(f"{k[:4]}:{val:+.0f}" for k, val in v))
P("")

P("=" * 78)
P("TEST 4  --  ROBUSTNESS: SUB-PERIODS, OPERATING LEVERAGE, AND THE Q3 FY2026 ANCHOR")
P("=" * 78)
P("(a) sub-period stability of the ratio sd(margin)/sd(revenue), AG segment")
P(f"{'window':18s} {'n':>3s} {'sd_rev':>7s} {'sd_mgn':>7s} {'ratio':>6s} {'p':>7s}")
subper = {}
for name, lo, hi in (("FY2015-FY2020", 2015, 2020), ("FY2021-FY2026", 2021, 2026),
                     ("FY2023-FY2026 (down-cycle)", 2023, 2026)):
    a = err.get(("revenue", "AG", "yoy_carry"), {})
    b = err.get(("margin_log", "AG", "yoy_carry"), {})
    ks_, x_, y_ = paired(a, b)
    sel = [i for i, k in enumerate(ks_) if lo <= int(k[:4]) <= hi]
    if len(sel) < 6:
        continue
    xx = [x_[i] for i in sel]
    yy = [y_[i] for i in sel]
    F, r, t, df, pv = pitman_morgan(yy, xx)
    subper[name] = (len(sel), st.stdev(xx), st.stdev(yy), st.stdev(yy) / st.stdev(xx), pv)
    P(f"{name:18s} {len(sel):3d} {st.stdev(xx):7.2f} {st.stdev(yy):7.2f} "
      f"{st.stdev(yy)/st.stdev(xx):6.2f} {pv:7.4f}")
P("")

P("(b) operating leverage: regression of margin error on revenue error")
P("    e_margin(%) = alpha + beta * e_revenue(%).  beta > 0 means a revenue miss")
P("    MECHANICALLY drags margin with it, so the two ranges are NOT independent.")
P(f"{'segment':10s} {'n':>3s} {'corr':>6s} {'beta':>6s} {'t':>6s} {'p':>7s} "
  f"{'implied d(OP)/d(Rev)':>21s}")
lev = {}
for s_ in SEGMENTS:
    a = err.get(("revenue", s_, "yoy_carry"), {})
    b = err.get(("margin_log", s_, "yoy_carry"), {})
    ks_, x_, y_ = paired(a, b)
    if len(ks_) < 8:
        continue
    r = pearson(x_, y_)
    beta = r * st.stdev(y_) / st.stdev(x_)
    dfree = len(ks_) - 2
    tt = r * math.sqrt(dfree / max(1e-12, 1 - r * r))
    pv = t_two_sided_p(tt, dfree)
    lev[s_] = (len(ks_), r, beta, pv)
    P(f"{s_:10s} {len(ks_):3d} {r:6.2f} {beta:6.2f} {tt:6.2f} {pv:7.4f} "
      f"{1 + beta:21.2f}")
P("")

P("(c) Naive yoy_carry anchors for Q3 FY2026 (NOT a forecast -- the mechanical")
P("    benchmark, plus the empirically measured one-quarter-ahead error band).")
K = "2026Q3"
anchors = {}
for lab, field, kind, seg in (("net sales & revenues (USDm)", "total_rev", "revenue", "TOTAL"),
                              ("PPA net sales (USDm)", "sales_PPA", "revenue", "PPA"),
                              ("SAT net sales (USDm)", "sales_SAT", "revenue", "SAT"),
                              ("CF net sales (USDm)", "sales_CF", "revenue", "CF"),
                              ("diluted EPS (USD)", "eps_diluted", "eps", "TOTAL")):
    x4, x1, x5 = get(lag(K, 4), field), get(lag(K, 1), field), get(lag(K, 5), field)
    if None in (x4, x1, x5) or min(x4, x1, x5) <= 0:
        continue
    f = x4 * (x1 / x5)
    d = desc(list(err.get((kind, seg, "yoy_carry"), {}).values()))
    lo68, hi68 = f * math.exp(-d["sd"] / 100), f * math.exp(d["sd"] / 100)
    anchors[lab] = (f, d["sd"], d["mae"], lo68, hi68, d["n"])
    P(f"  {lab:30s} anchor {f:9.2f}   sd {d['sd']:5.1f}%  MAE {d['mae']:5.1f}%  "
      f"68% band [{lo68:8.2f}, {hi68:8.2f}]  (n={d['n']})")
for seg in ("PPA", "SAT", "CF", "AG", "EQUIP"):
    m4, m1, m5 = (get(lag(K, 4), f"margin_{seg}"), get(lag(K, 1), f"margin_{seg}"),
                  get(lag(K, 5), f"margin_{seg}"))
    if None in (m4, m1, m5):
        continue
    f = m4 + (m1 - m5)
    d = desc(list(err.get(("margin_bps", seg, "yoy_carry"), {}).values()))
    anchors[f"{seg} operating margin (%)"] = (f, d["sd"], d["mae"],
                                              f - d["sd"] / 100, f + d["sd"] / 100, d["n"])
    P(f"  {seg + ' operating margin (%)':30s} anchor {f:9.2f}   sd {d['sd']:5.0f}bps "
      f"MAE {d['mae']:5.0f}bps  68% band [{f - d['sd']/100:8.2f}, "
      f"{f + d['sd']/100:8.2f}]  (n={d['n']})")
P("")

# ------------------------------------------------------------------ summary rows in CSV
def emit_stat(series_id, segment, component, value, units, notes):
    if value is None or (isinstance(value, float) and not math.isfinite(value)):
        return
    ROWS.append({"series_id": series_id, "period_end": "", "fiscal_year": "",
                 "fiscal_quarter": "", "segment": segment, "component": component,
                 "value": round(value, 4), "units": units,
                 "source": "computed", "notes": notes})


for rule, lab, key, st_ in summary_rows:
    kind, seg, _ = key
    for stat in ("n", "mean", "sd", "mae", "rmse"):
        unit = "count" if stat == "n" else (
            "bps" if "bps" in lab else "percent_log")
        emit_stat("de_predictability_summary", seg, f"{rule}|{kind}|{stat}",
                  float(st_[stat]), unit, lab)

for s, (n, sdr, sdm, ratio, maer, maem, r, p, k0, k1) in ratio_tbl.items():
    emit_stat("de_predictability_ratio", s, "sd_margin_over_sd_revenue", ratio, "ratio",
              f"n={n} sd_rev={sdr:.2f}% sd_margin={sdm:.2f}% "
              f"PitmanMorgan_p={p:.4f} window {k0}-{k1}")
for s, (n, sdop, sr, sm, rcorr, k0, k1) in decomp.items():
    emit_stat("de_op_surprise_variance_share", s, "revenue_component", sr, "share",
              f"n={n} sd_e_op={sdop:.2f}% corr(rev,margin)={rcorr:.2f} window {k0}-{k1}")
    emit_stat("de_op_surprise_variance_share", s, "margin_component", sm, "share",
              f"n={n} sd_e_op={sdop:.2f}% corr(rev,margin)={rcorr:.2f} window {k0}-{k1}")
n_, sde, s_r, s_m, s_res = eps_shares
for cname, val in (("revenue_component", s_r), ("margin_component", s_m),
                   ("residual_component", s_res)):
    emit_stat("de_eps_surprise_variance_share", "TOTAL", cname, val, "share",
              f"n={n_} sd_e_eps={sde:.2f}%")
for (lab, q), st_ in byq.items():
    if st_ is None:
        continue
    emit_stat("de_predictability_by_quarter", lab.split()[1], f"Q{q}|{lab}|mae",
              st_["mae"], "bps" if "bps" in lab else "percent_log", f"n={st_['n']}")
for lab, (nt, mt, nc, mc, rt) in tp_tbl.items():
    emit_stat("de_predictability_turning_point", lab.split()[1],
              f"{lab}|mae_ratio_turn_vs_calm", rt, "ratio",
              f"n_turn={nt} MAE_turn={mt:.1f} n_calm={nc} MAE_calm={mc:.1f}")

for nm, (n_s, sdr, sdm, rt, pv) in subper.items():
    emit_stat("de_predictability_ratio_subperiod", "AG", nm, rt, "ratio",
              f"n={n_s} sd_rev={sdr:.2f}% sd_margin={sdm:.2f}% PitmanMorgan_p={pv:.4f}")
for s_, (n_s, r, beta, pv) in lev.items():
    emit_stat("de_operating_leverage_beta", s_, "d_margin_pct_per_d_revenue_pct", beta,
              "ratio", f"n={n_s} corr={r:.2f} p={pv:.4f}; "
                       f"implied d(op profit)%/d(revenue)% = {1+beta:.2f}")
for lab, (f, sd_, mae_, lo_, hi_, n_) in anchors.items():
    unit = "percent" if "margin" in lab else ("USD" if "EPS" in lab else "USDm")
    seg_ = lab.split()[0] if lab.split()[0] in SEGMENTS else "TOTAL"
    metric = ("operating_margin" if "margin" in lab else
              ("diluted_eps" if "EPS" in lab else "net_sales"))
    emit_stat("de_q3fy2026_naive_anchor", seg_, f"{metric}|yoy_carry_anchor", f, unit,
              f"mechanical benchmark, not a forecast; historical sd={sd_:.2f} "
              f"MAE={mae_:.2f} n={n_}")
    emit_stat("de_q3fy2026_naive_anchor", seg_, f"{metric}|band_68_low", lo_, unit,
              "anchor +/- one historical one-quarter-ahead error sd; NOT a forecast")
    emit_stat("de_q3fy2026_naive_anchor", seg_, f"{metric}|band_68_high", hi_, unit,
              "anchor +/- one historical one-quarter-ahead error sd; NOT a forecast")

os.makedirs(OUTDIR, exist_ok=True)
FIELDS = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "segment",
          "component", "value", "units", "source", "notes"]
ROWS.sort(key=lambda r: (r["series_id"], r["segment"], r["component"],
                         str(r["fiscal_year"]), str(r["fiscal_quarter"])))
with open(CSVPATH, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(ROWS)
P(f"wrote {len(ROWS)} rows -> {CSVPATH}")

json.dump({"subper": subper, "lev": lev, "anchors": anchors, "ratio_tbl": ratio_tbl, "decomp": decomp, "eps_shares": eps_shares,
           "tp_tbl": tp_tbl, "ent": ent, "guid": guid_cmp,
           "byq": {f"{a}|{b}": v for (a, b), v in byq.items()},
           "turn": sorted(turn)},
          open(os.path.join(SCRATCH, "de_pred_results.json"), "w"), indent=1)
open(os.path.join(SCRATCH, "de_pred_report.txt"), "w").write("\n".join(REPORT))
