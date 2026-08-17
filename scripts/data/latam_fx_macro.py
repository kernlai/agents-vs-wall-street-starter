#!/usr/bin/env python3
"""Fetch FRED series and average them over Deere fiscal quarters (LatAm desk)."""
import csv, io, urllib.request, datetime as dt, statistics, sys

FQ = {  # Deere fiscal quarter -> (start, end) inclusive
 "FY2024Q3": ("2024-04-29","2024-07-28"), "FY2024Q4": ("2024-07-29","2024-10-27"),
 "FY2025Q1": ("2024-10-28","2025-01-26"), "FY2025Q2": ("2025-01-27","2025-04-27"),
 "FY2025Q3": ("2025-04-28","2025-07-27"), "FY2025Q4": ("2025-07-28","2025-11-02"),
 "FY2026Q1": ("2025-11-03","2026-02-01"), "FY2026Q2": ("2026-02-02","2026-05-03"),
 "FY2026Q3": ("2026-05-04","2026-08-02"),
}

def fred(sid):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
    req = urllib.request.Request(url, headers={"User-Agent":"deere-latam-desk research cor@salomo.io"})
    txt = urllib.request.urlopen(req, timeout=60).read().decode()
    out = {}
    for row in csv.DictReader(io.StringIO(txt)):
        d = row.get("observation_date") or row.get("DATE") or list(row.values())[0]
        v = list(row.values())[1]
        try: out[d] = float(v)
        except ValueError: pass
    return out

for sid in sys.argv[1:]:
    s = fred(sid)
    print("###", sid, "n=", len(s), "last=", max(s))
    for q,(a,b) in FQ.items():
        vals = [v for d,v in s.items() if a <= d <= b]
        if vals:
            print(f"  {q} n={len(vals):3d} mean={statistics.mean(vals):9.4f} last={vals[-1] if vals else '':}")
