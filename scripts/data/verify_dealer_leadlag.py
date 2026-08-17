"""Independent re-check of the wholesale-receivable -> net-sales lead/lag claim
(dealer-credit-quality agent: r=-0.885 at L4, n=19) before it is allowed to
carry weight in DEALER_HEALTH.md."""
import csv, collections, statistics as st
from datetime import date

P = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/dealer_credit_quality.csv"
rows = list(csv.DictReader(open(P)))
S = collections.defaultdict(dict)
for r in rows:
    if r["value"] not in ("", None):
        S[r["series_id"]][r["period_end"]] = float(r["value"])

def yoy(series):
    """y/y % using the observation ~4 quarters back (nearest period end 330-400d)."""
    ks = sorted(series)
    out = {}
    for k in ks:
        d = date.fromisoformat(k)
        cands = [(abs((d - date.fromisoformat(p)).days - 365), p) for p in ks
                 if 330 <= (d - date.fromisoformat(p)).days <= 400]
        if cands:
            _, p = min(cands)
            if series[p]:
                out[k] = 100.0 * (series[k] / series[p] - 1)
    return out

def pearson(a, b):
    n = len(a)
    ma, mb = sum(a)/n, sum(b)/n
    va = sum((x-ma)**2 for x in a); vb = sum((y-mb)**2 for y in b)
    if va == 0 or vb == 0: return float("nan")
    return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / (va*vb)**0.5

wy = yoy(S["de_wholesale_receivables_total"])
sy = yoy(S["de_net_sales_and_revenues"])
wk, sk = sorted(wy), sorted(sy)

def pair(lag):
    """wholesale y/y at t-lag quarters vs sales y/y at t."""
    out = []
    for i, k in enumerate(sk):
        # find wholesale obs 'lag' quarters before k
        target = [w for w in wk if w < k] if lag else [w for w in wk if w == k]
        if lag:
            prior = [w for w in wk if w <= k]
            if len(prior) <= lag: continue
            w = prior[-1-lag]
            # guard: must actually be ~lag*91 days earlier
            gap = (date.fromisoformat(k) - date.fromisoformat(w)).days
            if not (lag*91 - 50 <= gap <= lag*91 + 50): continue
        else:
            if k not in wy: continue
            w = k
        out.append((k, wy[w], sy[k]))
    return out

print("lag |  n  |    r    | slope | note")
fits = {}
for lag in range(0, 7):
    p = pair(lag)
    if len(p) < 6: continue
    x = [q[1] for q in p]; y = [q[2] for q in p]
    r = pearson(x, y)
    mx, my = sum(x)/len(x), sum(y)/len(y)
    b = sum((a-mx)*(c-my) for a, c in zip(x, y)) / sum((a-mx)**2 for a in x)
    a0 = my - b*mx
    fits[lag] = (a0, b, p, r)
    print(f" L{lag} | {len(p):3d} | {r:+.3f} | {b:+.3f} | a={a0:+.2f}")

# --- robustness: does the relationship survive dropping the 2023 build / 2024-25 bust? ---
print("\nROBUSTNESS at L4")
a0, b, p, r = fits[4]
print(f"  full: n={len(p)} r={r:+.3f}")
sub = [q for q in p if q[0] < "2024-01-01"]
if len(sub) >= 6:
    x=[q[1] for q in sub]; y=[q[2] for q in sub]
    print(f"  pre-2024 only: n={len(sub)} r={pearson(x,y):+.3f}")
sub2 = [q for q in p if q[0] >= "2023-01-01"]
if len(sub2) >= 6:
    x=[q[1] for q in sub2]; y=[q[2] for q in sub2]
    print(f"  2023+ only:    n={len(sub2)} r={pearson(x,y):+.3f}")

# leave-one-out on the L4 fit's Q3 FY2026 prediction
pred_x = wy.get("2025-07-27")
print(f"\n  L4 predictor for Q3 FY2026 = wholesale y/y at 2025-07-27 = {pred_x:+.2f}%")
preds = []
for i in range(len(p)):
    q = p[:i] + p[i+1:]
    x=[z[1] for z in q]; y=[z[2] for z in q]
    mx,my=sum(x)/len(x),sum(y)/len(y)
    bb=sum((a-mx)*(c-my) for a,c in zip(x,y))/sum((a-mx)**2 for a in x)
    preds.append((my-bb*mx)+bb*pred_x)
print(f"  LOO predicted Q3 FY26 sales y/y: min {min(preds):+.1f}%  max {max(preds):+.1f}%  full-fit {a0+b*pred_x:+.1f}%")
resid = [q[2]-(a0+b*q[1]) for q in p]
sd = (sum(e*e for e in resid)/(len(resid)-2))**0.5
print(f"  residual SD = {sd:.1f}pp -> on 12,018 base: 1sd band ${12018*(1+(a0+b*pred_x-sd)/100)/1000:.2f}-{12018*(1+(a0+b*pred_x+sd)/100)/1000:.2f}bn")

# --- effective sample size: how autocorrelated is the predictor? ---
xs = [q[1] for q in p]
lag1 = pearson(xs[:-1], xs[1:])
print(f"\n  AR(1) of predictor series: {lag1:+.3f}  -> overlapping y/y windows; effective n well below {len(p)}")
ys = [q[2] for q in p]
print(f"  AR(1) of target series:    {pearson(ys[:-1], ys[1:]):+.3f}")

# --- what does the naive alternative say? ---
print("\nNAIVE BENCHMARKS for Q3 FY2026 total revenue (base Q3 FY25 = 12,018):")
for g,lab in [(0.05,'Q2 FY26 y/y +5%'),(0.08,'H1 FY26 y/y +8%'),(0.0,'flat y/y')]:
    print(f"  {lab:22s} -> ${12018*(1+g)/1000:.2f}bn")
