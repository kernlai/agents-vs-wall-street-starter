"""Effective sample size + direction-of-causality checks on the L4 wholesale->sales result."""
import csv, collections
from datetime import date
P="/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/dealer_credit_quality.csv"
S=collections.defaultdict(dict)
for r in csv.DictReader(open(P)):
    if r["value"]: S[r["series_id"]][r["period_end"]]=float(r["value"])
def yoy(s):
    ks=sorted(s); o={}
    for k in ks:
        d=date.fromisoformat(k)
        c=[(abs((d-date.fromisoformat(p)).days-365),p) for p in ks if 330<=(d-date.fromisoformat(p)).days<=400]
        if c: _,p=min(c); o[k]=100*(s[k]/s[p]-1) if s[p] else None
    return {k:v for k,v in o.items() if v is not None}
def pear(a,b):
    n=len(a); ma,mb=sum(a)/n,sum(b)/n
    va=sum((x-ma)**2 for x in a); vb=sum((y-mb)**2 for y in b)
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/(va*vb)**.5 if va and vb else float('nan')
wy,sy=yoy(S["de_wholesale_receivables_total"]),yoy(S["de_net_sales_and_revenues"])
wk,sk=sorted(wy),sorted(sy)
def pair(lag,lead_series,targ_series):
    lk,tk=sorted(lead_series),sorted(targ_series); out=[]
    for k in tk:
        prior=[w for w in lk if w<=k]
        if len(prior)<=lag: continue
        w=prior[-1-lag]
        gap=(date.fromisoformat(k)-date.fromisoformat(w)).days
        if not (lag*91-50<=gap<=lag*91+50): continue
        out.append((k,lead_series[w],targ_series[k]))
    return out

p=pair(4,wy,sy); x=[q[1] for q in p]; y=[q[2] for q in p]
r1=pear(x[:-1],x[1:]); r2=pear(y[:-1],y[1:])
n=len(p); neff=n*(1-r1*r2)/(1+r1*r2)
print(f"L4 wholesale->sales: n={n} r={pear(x,y):+.3f}")
print(f"  AR(1) predictor={r1:+.3f} target={r2:+.3f}")
print(f"  Bartlett-adjusted EFFECTIVE n = {neff:.1f}  (critical |r| at 5% with n~{neff:.0f} is ~{0.95 if neff<5 else 0.7:.2f})")

print("\nSUBSAMPLES (does it survive removing the 2023-26 cycle?)")
for lab,f in [("all",lambda k:True),("<=2024-12",lambda k:k<"2025-01-01"),("<=2024-06",lambda k:k<"2024-07-01"),
              ("<=2023-12",lambda k:k<"2024-01-01"),(">=2023-01",lambda k:k>="2023-01-01")]:
    s=[q for q in p if f(q[0])]
    if len(s)>=6:
        print(f"  {lab:12s} n={len(s):2d} r={pear([q[1] for q in s],[q[2] for q in s]):+.3f}")

print("\nREVERSE DIRECTION: does sales y/y lead wholesale y/y?")
for lag in range(0,5):
    q=pair(lag,sy,wy)
    if len(q)>=8: print(f"  sales(t-{lag}) -> wholesale(t): n={len(q):2d} r={pear([z[1] for z in q],[z[2] for z in q]):+.3f}")
