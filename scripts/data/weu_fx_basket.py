#!/usr/bin/env python3
"""Western-Europe translation basket for Deere revenue.
Weights approximate Deere's Western Europe geographic revenue by billing currency:
EUR 0.80 (DE/FR/IT/ES/NL/BE/AT/IE/FI/PT), GBP 0.12 (UK/IE-sterling), SEK 0.08 (Sweden - forestry).
Series: DEXUSEU (USD per EUR), DEXUSUK (USD per GBP), DEXSDUS (SEK per USD -> invert).
"""
import csv, datetime as dt, statistics, urllib.request

def fred(sid, cosd="2018-08-01"):
    u = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={cosd}"
    out = {}
    for r in csv.DictReader(urllib.request.urlopen(u).read().decode().splitlines()):
        v = list(r.values())[1]
        if v not in (".", "", None):
            out[dt.date.fromisoformat(r["observation_date"])] = float(v)
    return out

eur, gbp, sek = fred("DEXUSEU"), fred("DEXUSUK"), fred("DEXSDUS")
W = {"EUR": 0.80, "GBP": 0.12, "SEK": 0.08}

QE = {("2024","Q3"):"2024-07-28",("2024","Q4"):"2024-10-27",
      ("2025","Q1"):"2025-01-26",("2025","Q2"):"2025-04-27",("2025","Q3"):"2025-07-27",("2025","Q4"):"2025-11-02",
      ("2026","Q1"):"2026-02-01",("2026","Q2"):"2026-05-03",("2026","Q3"):"2026-08-02"}

def qavg(series, end_iso, invert=False):
    end = dt.date.fromisoformat(end_iso); start = end - dt.timedelta(weeks=13)
    v = [(1/x if invert else x) for d, x in series.items() if start < d <= end]
    return statistics.mean(v), len(v)

basket = {}
for k in sorted(QE, key=lambda k: QE[k]):
    e, ne = qavg(eur, QE[k]); g, ng = qavg(gbp, QE[k]); s, ns = qavg(sek, QE[k], invert=True)
    basket[k] = (e, g, s, min(ne, ng, ns))

print(f"{'FQ':10s} {'EURUSD':>8s} {'GBPUSD':>8s} {'USD/SEK':>8s} {'basket YoY':>11s}  n")
for k in sorted(QE, key=lambda k: QE[k]):
    e, g, s, n = basket[k]
    p = (str(int(k[0])-1), k[1])
    yoy = ""
    if p in basket:
        pe, pg, ps, _ = basket[p]
        r = W["EUR"]*(e/pe) + W["GBP"]*(g/pg) + W["SEK"]*(s/ps)
        yoy = f"{100*(r-1):+.1f}%"
    print(f"FY{k[0]} {k[1]}  {e:8.4f} {g:8.4f} {s:8.5f} {yoy:>11s}  {n}")
