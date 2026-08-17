#!/usr/bin/env python3
"""Western Europe (Deere) quarterly revenue history, seasonality, FX decomposition.
Inputs: /tmp/geo_matrix.json (from extract_geo_matrix.py) + FRED FX.
"""
import json, statistics as st, csv, datetime as dt, urllib.request

M = {(r["span"], r["period"]): r for r in json.load(open("/tmp/geo_matrix.json"))
     if r["geography"] == "Western Europe"}

FQ = {  # fiscal (year, qtr) -> (quarter_end, cumulative_span_label, cumulative_end)
 (2019,1):("2019-01-27",None,None),(2019,2):("2019-04-28","Three","2019-04-28"),
 (2019,3):("2019-07-28","Three","2019-07-28"),(2019,4):("2019-11-03","FY","2019"),
 (2020,1):("2020-02-02",None,None),(2020,2):("2020-05-03","Three","2020-05-03"),
 (2020,3):("2020-08-02","Three","2020-08-02"),(2020,4):("2020-11-01","FY","2020"),
 (2021,1):("2021-01-31",None,None),(2021,2):("2021-05-02","Three","2021-05-02"),
 (2021,3):("2021-08-01","Three","2021-08-01"),(2021,4):("2021-10-31","FY","2021"),
 (2022,1):("2022-01-30",None,None),(2022,2):("2022-05-01","Three","2022-05-01"),
 (2022,3):("2022-07-31","Three","2022-07-31"),(2022,4):("2022-10-30","FY","2022"),
 (2023,1):("2023-01-29",None,None),(2023,2):("2023-04-30","Three","2023-04-30"),
 (2023,3):("2023-07-30","Three","2023-07-30"),(2023,4):("2023-10-29","FY","2023"),
 (2024,1):("2024-01-28",None,None),(2024,2):("2024-04-28","Three","2024-04-28"),
 (2024,3):("2024-07-28","Three","2024-07-28"),(2024,4):("2024-10-27","FY","2024"),
 (2025,1):("2025-01-26",None,None),(2025,2):("2025-04-27","Three","2025-04-27"),
 (2025,3):("2025-07-27","Three","2025-07-27"),(2025,4):("2025-11-02","FY","2025"),
 (2026,1):("2026-02-01",None,None),(2026,2):("2026-05-03","Three","2026-05-03"),
}
NINE = {2019:"2019-07-28",2020:"2020-08-02",2021:"2021-08-01",2022:"2022-07-31",
        2023:"2023-07-30",2024:"2024-07-28",2025:"2025-07-27"}
SEGS4 = ["PPA","SAT","CF","FS"]

def get(span, per): return M.get((span, per))

q = {}   # (fy, fq) -> {seg: val}
for (fy, fq), (qe, _, _) in FQ.items():
    r = get("Three", qe)
    if r:
        q[(fy, fq)] = {k: r.get(k) for k in SEGS4 + ["AT", "Total"]}
# Q4 = FY - nine months  (derived, flagged as such)
derived = set()
for fy, nine_end in NINE.items():
    a, b = get("FY", str(fy)), get("Nine", nine_end)
    if a and b:
        q[(fy, 4)] = {k: (a.get(k) - b.get(k) if a.get(k) is not None and b.get(k) is not None else None)
                      for k in SEGS4 + ["AT", "Total"]}
        derived.add((fy, 4))

print("Deere WESTERN EUROPE quarterly revenue (ASC 606 rev-rec basis, USDm)")
print(f"{'FQ':10s} {'PPA':>6s} {'SAT':>6s} {'A&T':>6s} {'CF':>6s} {'FS':>5s} {'Total':>7s} {'YoY':>8s}  src")
for k in sorted(q):
    v = q[k]; p = q.get((k[0]-1, k[1]))
    yoy = f"{100*(v['Total']/p['Total']-1):+.1f}%" if p and p.get("Total") and v.get("Total") else ""
    f = lambda x: f"{x:6d}" if x else "      "
    print(f"FY{k[0]} Q{k[1]}  {f(v.get('PPA'))} {f(v.get('SAT'))} {f(v.get('AT'))} {f(v.get('CF'))} "
          f"{v.get('FS') or '':>5} {v.get('Total') or '':>7} {yoy:>8s}  {'derived' if k in derived else 'filing'}")

print("\n--- Q2 -> Q3 sequential ratios (seasonality), Western Europe")
print(f"{'FY':6s} " + " ".join(f"{s:>7s}" for s in SEGS4 + ["Total"]))
ratios = {s: [] for s in SEGS4 + ["Total"]}
for fy in range(2021, 2026):
    row = []
    for s in SEGS4 + ["Total"]:
        a, b = q.get((fy, 2), {}).get(s), q.get((fy, 3), {}).get(s)
        if a and b:
            ratios[s].append(b/a); row.append(f"{b/a:7.3f}")
        else: row.append("      -")
    print(f"FY{fy}  " + " ".join(row))
print("mean  " + " ".join(f"{st.mean(ratios[s]):7.3f}" for s in SEGS4 + ["Total"]))
print("med   " + " ".join(f"{st.median(ratios[s]):7.3f}" for s in SEGS4 + ["Total"]))
print("n     " + " ".join(f"{len(ratios[s]):7d}" for s in SEGS4 + ["Total"]))

# ---- FX decomposition
def fred(sid):
    u = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd=2018-08-01"
    d = {}
    for r in csv.DictReader(urllib.request.urlopen(u).read().decode().splitlines()):
        v = list(r.values())[1]
        if v not in (".", "", None): d[dt.date.fromisoformat(r["observation_date"])] = float(v)
    return d
eur, gbp, sek = fred("DEXUSEU"), fred("DEXUSUK"), fred("DEXSDUS")
W = {"EUR":0.80, "GBP":0.12, "SEK":0.08}
def qavg(s, end, inv=False):
    e = dt.date.fromisoformat(end); s0 = e - dt.timedelta(weeks=13)
    return st.mean([(1/x if inv else x) for d, x in s.items() if s0 < d <= e])
QEND = {k: v[0] for k, v in FQ.items()}
QEND[(2026,3)] = "2026-08-02"
for fy in NINE: QEND[(fy,4)] = FQ[(fy,4)][0]
bask = {k: (qavg(eur,e), qavg(gbp,e), qavg(sek,e,True)) for k,e in QEND.items() if e >= "2018-11-01"}

print("\n--- YoY decomposition: reported vs FX-basket translation vs implied constant currency")
print(f"{'FQ':10s} {'reported':>9s} {'FX':>7s} {'implied CC':>11s}")
pairs = []
for k in sorted(bask):
    p = (k[0]-1, k[1])
    if p not in bask or k not in q or p not in q: continue
    if not (q[k].get("Total") and q[p].get("Total")): continue
    fx = sum(W[c]*(bask[k][i]/bask[p][i]) for i,c in enumerate(["EUR","GBP","SEK"])) - 1
    rep = q[k]["Total"]/q[p]["Total"] - 1
    print(f"FY{k[0]} Q{k[1]}  {100*rep:+8.1f}% {100*fx:+6.1f}% {100*((1+rep)/(1+fx)-1):+10.1f}%")
    pairs.append((fx, rep))
# forward-looking cell
k = (2026,3); p = (2025,3)
fx = sum(W[c]*(bask[k][i]/bask[p][i]) for i,c in enumerate(["EUR","GBP","SEK"])) - 1
print(f"FY2026 Q3  {'n/a (unreported)':>9s} {100*fx:+6.1f}%   <-- FX tailwind essentially GONE")

n = len(pairs)
mx, my = st.mean([a for a,_ in pairs]), st.mean([b for _,b in pairs])
cov = sum((a-mx)*(b-my) for a,b in pairs)
den = (sum((a-mx)**2 for a,_ in pairs) * sum((b-my)**2 for _,b in pairs))**0.5
print(f"\nCorrelation(FX basket YoY, reported WEu total YoY) = {cov/den:+.2f}  (n={n} quarters)")
print("  -> small sample; FX and demand cycles overlap, treat as indicative not causal.")

json.dump({f"FY{k[0]}Q{k[1]}": v for k, v in q.items()}, open("/tmp/weu_q.json","w"), indent=1)
