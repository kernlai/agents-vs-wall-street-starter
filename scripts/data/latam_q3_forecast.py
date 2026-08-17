#!/usr/bin/env python3
"""Seasonality / FX / YoY diagnostics for the Deere Latin America Q3 FY2026 forecast."""
import csv, statistics, collections
P="/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/regional/latin_america.csv"
rows=[r for r in csv.DictReader(open(P))]
q={}
for r in rows:
    if r["series_id"]=="de_rev606_latam":
        q.setdefault((int(r["fiscal_year"]),r["fiscal_quarter"]),{})[r["segment"]]=float(r["value"])
fx={}
for r in rows:
    if r["series_id"]=="fx_usdbrl_avg": fx[(int(r["fiscal_year"]),r["fiscal_quarter"])]=float(r["value"])

def g(fy,fq,seg): return q.get((fy,fq),{}).get(seg)

print("### LatAm quarterly, USDm (ASC 606)")
print(f"{'FQ':10}{'PPA':>7}{'SAT':>7}{'CF':>7}{'FS':>7}{'TOT':>8}   PPA YoY  TOT YoY")
for fy in range(2020,2027):
    for fq in ("Q1","Q2","Q3","Q4"):
        if (fy,fq) not in q: continue
        d=q[(fy,fq)]; p=d.get("PPA"); t=d.get("TOTAL")
        pp=g(fy-1,fq,"PPA"); tp=g(fy-1,fq,"TOTAL")
        py=f"{(p/pp-1)*100:+7.1f}%" if p and pp else "       ."
        ty=f"{(t/tp-1)*100:+7.1f}%" if t and tp else "       ."
        print(f"FY{fy}{fq:4}{p or 0:7.0f}{d.get('SAT',0):7.0f}{d.get('CF',0):7.0f}{d.get('FS',0):7.0f}{t:8.0f}   {py} {ty}")

print("\n### Q2 -> Q3 sequential, LatAm")
for seg in ("PPA","SAT","CF","TOTAL"):
    seq=[]
    for fy in range(2021,2026):
        a,b=g(fy,"Q2",seg),g(fy,"Q3",seg)
        if a and b: seq.append((fy,b/a-1))
    s=[x[1] for x in seq]
    print(f" {seg:6} n={len(s)} " + " ".join(f"FY{fy}{v*100:+6.1f}%" for fy,v in seq) +
          f"  | median {statistics.median(s)*100:+5.1f}%  mean {statistics.mean(s)*100:+5.1f}%")

print("\n### Q3 share of fiscal-year LatAm revenue")
for seg in ("PPA","SAT","CF","TOTAL"):
    sh=[]
    for fy in range(2021,2026):
        y=sum(g(fy,x,seg) or 0 for x in ("Q1","Q2","Q3","Q4"))
        v=g(fy,"Q3",seg)
        if y and v: sh.append((fy,v/y))
    print(f" {seg:6} " + " ".join(f"FY{fy}{v*100:5.1f}%" for fy,v in sh) +
          f" | median {statistics.median([x[1] for x in sh])*100:5.1f}%")

print("\n### USD/BRL and LatAm PPA YoY (n small -- read with caution)")
pairs=[]
for fy in range(2025,2027):
    for fq in ("Q1","Q2","Q3","Q4"):
        f0,f1=fx.get((fy,fq)),fx.get((fy-1,fq))
        p0,p1=g(fy,fq,"PPA"),g(fy-1,fq,"PPA")
        if f0 and f1 and p0 and p1:
            brl=(f1/f0-1)*100; ppa=(p0/p1-1)*100
            pairs.append((fy,fq,brl,ppa))
            print(f" FY{fy}{fq}  BRL translation {brl:+6.1f}%   LatAm PPA USD {ppa:+6.1f}%   implied ex-FX {ppa-brl:+6.1f}%")
print(f" FY2026Q3 BRL translation {(fx[(2025,'Q3')]/fx[(2026,'Q3')]-1)*100:+6.1f}% (avg {fx[(2026,'Q3')]:.4f} vs {fx[(2025,'Q3')]:.4f})")

print("\n### Q3 FY2026 scenarios, LatAm PPA (Q3 FY2025 base = 1055; Q2 FY2026 = 828)")
base, q2 = 1055.0, 828.0
for label, seq in (("bear: Q2->Q3 -10% (combine underbuild + delayed safrinha)",-0.10),
                   ("low : Q2->Q3  -5%",-0.05),
                   ("central: Q2->Q3 flat", 0.00),
                   ("high: Q2->Q3 +6% (5yr median seasonality)", 0.06),
                   ("bull: Q2->Q3 +12%", 0.12)):
    v=q2*(1+seq); print(f"  {label:58} -> {v:6.0f}  ({(v/base-1)*100:+5.1f}% YoY)")
