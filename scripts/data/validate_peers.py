#!/usr/bin/env python3
"""Validation pass over drv_peers.csv.

Check A  arithmetic: sum(Q1..Q4) vs the FY row, per company-year. For companies
         that tag all four quarters this is a genuine independent-of-derivation
         check; for the rest Q4 is derived so the identity is trivially true and
         is skipped.
Check B  monotonic sanity: no negative revenues, no duplicate (series,period,fq).
Check C  cross-source: compares a handful of values against the SEC `frames`
         API, which is assembled by a different EDGAR pipeline than
         companyconcept/companyfacts.
"""
import csv, json, sys, urllib.request, collections

UA = "AgentsVsWallStreet cor@salomo.io"
CSVP = sys.argv[1]

rows = list(csv.DictReader(open(CSVP)))
print("rows:", len(rows))

# ---- B: duplicates -----------------------------------------------------------
seen = collections.Counter((r["series_id"], r["period_end"], r["fiscal_quarter"])
                           for r in rows)
dups = [k for k, v in seen.items() if v > 1]
print("duplicate keys:", len(dups), dups[:5])
neg = [r for r in rows if r["series_id"].endswith("_revenue")
       and r["value"] and float(r["value"]) <= 0]
print("non-positive revenues:", len(neg), [(r["series_id"], r["period_end"]) for r in neg][:5])

# ---- A: sum of quarters vs FY ------------------------------------------------
by = collections.defaultdict(dict)
derived = set()
for r in rows:
    if not r["series_id"].endswith("_revenue") or not r["value"]:
        continue
    by[(r["series_id"], r["fiscal_year"])][r["fiscal_quarter"]] = float(r["value"])
    if r["source_type"] == "inference":
        derived.add((r["series_id"], r["fiscal_year"], r["fiscal_quarter"]))

hard = soft = fails = 0
for (sid, fy), d in sorted(by.items()):
    if "FY" not in d or not all(q in d for q in ("Q1", "Q2", "Q3", "Q4")):
        continue
    s = sum(d[q] for q in ("Q1", "Q2", "Q3", "Q4"))
    err = abs(s - d["FY"]) / max(d["FY"], 1e-9)
    if (sid, fy, "Q4") in derived:
        soft += 1
        continue
    hard += 1
    if err > 0.005:
        fails += 1
        print("  MISMATCH %-16s FY%s sum=%.1f FY=%.1f  err=%.3f%%"
              % (sid, fy, s, d["FY"], err * 100))
print("sum-of-quarters check: %d independent company-years tested, %d failed "
      "(%d skipped because Q4 is derived)" % (hard, fails, soft))

# ---- C: SEC frames API cross-check ------------------------------------------
def frame(tag, unit, cy, cik):
    url = ("https://data.sec.gov/api/xbrl/frames/us-gaap/%s/%s/CY%s.json" % (tag, unit, cy))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=60))
    except Exception as e:
        return None, str(e)
    for x in d["data"]:
        if x["cik"] == cik:
            return x["val"], x["end"]
    return None, "cik not in frame"

CHECKS = [
    ("cat_revenue", "Revenues", "USD", "2024", 18230),
    ("cat_revenue", "Revenues", "USD", "2019", 18230),
    ("tsco_revenue", "Revenues", "USD", "2024", 916365),
    ("cnh_revenue", "Revenues", "USD", "2023", 1567094),
    ("titn_revenue", "Revenues", "USD", "2019", 1409171),
    ("lindsay_revenue", "Revenues", "USD", "2022", 836157),
    ("agco_revenue", "RevenueFromContractWithCustomerExcludingAssessedTax", "USD", "2024", 880266),
    ("valmont_revenue", "RevenueFromContractWithCustomerExcludingAssessedTax", "USD", "2023", 102729),
    ("de_revenue", "Revenues", "USD", "2023", 315189),
]
print("\nframes API cross-check (annual, CY frame):")
ok = bad = miss = 0
for sid, tag, unit, cy, cik in CHECKS:
    val, end = frame(tag, unit, cy, cik)
    if val is None:
        print("  %-16s CY%s  frames: unavailable (%s)" % (sid, cy, end))
        miss += 1
        continue
    mine = [r for r in rows if r["series_id"] == sid and r["fiscal_quarter"] == "FY"
            and r["period_end"] == end]
    if not mine:
        print("  %-16s CY%s  frames=%.1fm end=%s  -> no matching CSV row" % (sid, cy, val/1e6, end))
        miss += 1
        continue
    m = float(mine[0]["value"])
    err = abs(m - val / 1e6) / max(abs(val / 1e6), 1e-9)
    flag = "OK " if err < 0.005 else "DIFF"
    print("  %s %-16s end=%s frames=%.1fm csv=%.1fm err=%.4f%%"
          % (flag, sid, end, val / 1e6, m, err * 100))
    ok += err < 0.005
    bad += err >= 0.005
print("frames check: %d agree, %d differ, %d unavailable" % (ok, bad, miss))
