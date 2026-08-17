#!/usr/bin/env python3
"""Average EUR/USD (FRED DEXUSEU) over Deere fiscal quarters + YoY translation effect."""
import csv, datetime as dt, statistics, urllib.request

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU&cosd=2018-08-01"
rows = []
for r in csv.DictReader(urllib.request.urlopen(URL).read().decode().splitlines()):
    v = r.get("DEXUSEU") or r.get("observation_value")
    if v not in (".", "", None):
        rows.append((dt.date.fromisoformat(r["observation_date"]), float(v)))

# Deere fiscal quarter end dates (Sunday-ending 13-week quarters)
QE = {
 ("2019","Q3"):"2019-07-28",("2019","Q4"):"2019-11-03",
 ("2020","Q1"):"2020-02-02",("2020","Q2"):"2020-05-03",("2020","Q3"):"2020-08-02",("2020","Q4"):"2020-11-01",
 ("2021","Q1"):"2021-01-31",("2021","Q2"):"2021-05-02",("2021","Q3"):"2021-08-01",("2021","Q4"):"2021-10-31",
 ("2022","Q1"):"2022-01-30",("2022","Q2"):"2022-05-01",("2022","Q3"):"2022-07-31",("2022","Q4"):"2022-10-30",
 ("2023","Q1"):"2023-01-29",("2023","Q2"):"2023-04-30",("2023","Q3"):"2023-07-30",("2023","Q4"):"2023-10-29",
 ("2024","Q1"):"2024-01-28",("2024","Q2"):"2024-04-28",("2024","Q3"):"2024-07-28",("2024","Q4"):"2024-10-27",
 ("2025","Q1"):"2025-01-26",("2025","Q2"):"2025-04-27",("2025","Q3"):"2025-07-27",("2025","Q4"):"2025-11-02",
 ("2026","Q1"):"2026-02-01",("2026","Q2"):"2026-05-03",("2026","Q3"):"2026-08-02",
}
def avg(end_iso, weeks=13):
    end = dt.date.fromisoformat(end_iso); start = end - dt.timedelta(weeks=weeks)
    vals = [v for d, v in rows if start < d <= end]
    return statistics.mean(vals), len(vals)

res = {}
for k in sorted(QE, key=lambda k: QE[k]):
    m, n = avg(QE[k]); res[k] = m
    print(f"FY{k[0]} {k[1]}  end {QE[k]}  avg EURUSD {m:.4f}  (n={n} obs)")
print("\nYoY translation tailwind/headwind on EUR-denominated revenue:")
for k in sorted(QE, key=lambda k: QE[k]):
    p = (str(int(k[0])-1), k[1])
    if p in res:
        print(f"  FY{k[0]} {k[1]}: {100*(res[k]/res[p]-1):+.1f}%")
