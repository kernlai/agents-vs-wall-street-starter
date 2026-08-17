#!/usr/bin/env python3
"""
Build the tidy long CSV for the Deere CANADA regional desk.

Sources
  1. Deere 10-Q / 10-K ASC 606 "primary geographic markets" matrix, Canada row
     -> extract_deere_geo_canada.py (same directory)
  2. FRED DEXCAUS (CAD per USD, daily) -> Deere-fiscal-quarter averages
  3. Statistics Canada 32-10-0077 Farm product prices (canola / wheat / barley /
     durum, Prairie provinces, monthly)
  4. Statistics Canada 32-10-0046 Farm cash receipts, quarterly
  5. Statistics Canada 32-10-0359 Seeded area, principal field crops
  6. Hand-entered figures from Deere filings / AEM press coverage (each row
     carries its own source string)

Run:
  python3 build_canada_dataset.py            # writes the CSV + prints analysis
"""
import csv
import os
import subprocess
import sys
import datetime as dt
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = ("/private/tmp/claude-501/-Users-cor/"
           "c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad")
OUT = ("/Users/cor/Documents/projects/agents-vs-wall-street-starter/"
       "data/deere/regional/canada.csv")

HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter",
          "geography", "country", "segment", "value", "units",
          "source_type", "source", "notes"]

# Deere fiscal quarter end dates (from the filings themselves)
QEND = {
    (2019, 1): "2019-01-27", (2019, 2): "2019-04-28", (2019, 3): "2019-07-28",
    (2019, 4): "2019-11-03",
    (2020, 1): "2020-02-02", (2020, 2): "2020-05-03", (2020, 3): "2020-08-02",
    (2020, 4): "2020-11-01",
    (2021, 1): "2021-01-31", (2021, 2): "2021-05-02", (2021, 3): "2021-08-01",
    (2021, 4): "2021-10-31",
    (2022, 1): "2022-01-30", (2022, 2): "2022-05-01", (2022, 3): "2022-07-31",
    (2022, 4): "2022-10-30",
    (2023, 1): "2023-01-29", (2023, 2): "2023-04-30", (2023, 3): "2023-07-30",
    (2023, 4): "2023-10-29",
    (2024, 1): "2024-01-28", (2024, 2): "2024-04-28", (2024, 3): "2024-07-28",
    (2024, 4): "2024-10-27",
    (2025, 1): "2025-01-26", (2025, 2): "2025-04-27", (2025, 3): "2025-07-27",
    (2025, 4): "2025-11-02",
    (2026, 1): "2026-02-01", (2026, 2): "2026-05-03", (2026, 3): "2026-08-02",
}
CORPUS = ("challenge/offline-data/deere/filings/")

rows = []


def add(series_id, period_end, fy, fq, segment, value, units,
        source_type, source, notes="", geography="Canada", country="Canada"):
    rows.append({
        "series_id": series_id, "period_end": period_end,
        "fiscal_year": fy, "fiscal_quarter": fq, "geography": geography,
        "country": country, "segment": segment, "value": value,
        "units": units, "source_type": source_type, "source": source,
        "notes": notes})


# ---------------------------------------------------------------- 1. Deere
def deere_matrix():
    out = subprocess.run(
        [sys.executable, os.path.join(HERE, "extract_deere_geo_canada.py"),
         "Canada"], capture_output=True, text=True, check=True).stdout
    rd = csv.DictReader(out.splitlines())
    segmap_new = ["PPA", "SAT", "CF", "FS", "TOTAL"]
    segmap_old = ["AT", None, "CF", "FS", "TOTAL"]
    for r in rd:
        basis = r["basis"]
        segs = segmap_new if basis == "new" else segmap_old
        vals = [r["s1"], r["s2"], r["s3"], r["s4"], r["total"]]
        note = ("segment basis: PPA/SAT/CF/FS (post-2021 reporting structure)"
                if basis == "new" else
                "segment basis: Agriculture & Turf / CF / FS (pre-2021 "
                "structure, as originally filed)")
        note += "; " + r["derivation"]
        for seg, v in zip(segs, vals):
            if seg is None or v == "":
                continue
            add("de_revrec_canada", r["period_end"], r["fiscal_year"],
                r["fiscal_quarter"], seg, v, "USDm", "filing",
                CORPUS + r["source"],
                note + "; ASC 606 revenue from contracts with customers "
                       "(NOT the 8-K segment net sales basis)")


# ---------------------------------------------------------------- 2. FX
def fx():
    path = os.path.join(SCRATCH, "DEXCAUS.csv")
    if not os.path.exists(path):
        return
    obs = []
    for r in csv.reader(open(path)):
        if not r or r[0].startswith("observation") or r[1] in (".", ""):
            continue
        obs.append((dt.date.fromisoformat(r[0]), float(r[1])))
    prev = dt.date(2018, 10, 29)
    for k in sorted(QEND):
        e = dt.date.fromisoformat(QEND[k])
        vals = [v for d, v in obs if prev < d <= e]
        prev = e
        if not vals:
            continue
        m = statistics.mean(vals)
        add("fx_cadusd_avg", QEND[k], k[0], f"Q{k[1]}", "", round(m, 4),
            "CAD per USD", "official_stat",
            "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXCAUS",
            "mean of daily noon rates over the Deere fiscal quarter; "
            "retrieved 2026-08-16, series runs to 2026-08-07 so FY2026 Q3 "
            "covers 4 May - 7 Aug 2026")
        add("fx_usdcad_avg", QEND[k], k[0], f"Q{k[1]}", "", round(1 / m, 4),
            "USD per CAD", "official_stat",
            "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXCAUS",
            "inverse of fx_cadusd_avg; a fall = translation headwind for "
            "CAD-denominated Deere revenue")


# ------------------------------------------------- 3. StatCan farm prices
PRICE_MAP = {"Canola (including rapeseed) [113111]": "canola",
             "Wheat (except durum wheat) [1121111]": "wheat_ex_durum",
             "Durum wheat [112111211]": "durum",
             "Barley [1151141]": "barley"}
PRAIRIE = ["Saskatchewan", "Alberta", "Manitoba"]


def statcan_prices():
    path = os.path.join(SCRATCH, "32100077", "32100077.csv")
    if not os.path.exists(path):
        return
    monthly = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        p = PRICE_MAP.get(r["Farm products"])
        if not p or r["GEO"] not in PRAIRIE or r["REF_DATE"] < "2018-11":
            continue
        if not r["VALUE"]:
            continue
        monthly.setdefault((r["REF_DATE"], p), {})[r["GEO"]] = float(r["VALUE"])
    # monthly prairie-average price
    for (ref, p), d in sorted(monthly.items()):
        y, m = ref.split("-")
        pe = (dt.date(int(y), int(m), 28)
              .replace(day=28))
        add(f"ca_farmprice_{p}_prairie", ref, "", "", "",
            round(statistics.mean(d.values()), 2), "CAD per tonne",
            "official_stat",
            "Statistics Canada Table 32-10-0077 (Farm product prices, crops "
            "and livestock), downloaded 2026-08-16",
            "simple mean of Saskatchewan, Alberta and Manitoba monthly "
            "average farm prices; last observation 2026-06",
            geography="Prairie provinces")
    # Deere-fiscal-quarter averages
    def to_date(ref):
        y, m = ref.split("-")
        return dt.date(int(y), int(m), 15)
    for p in set(PRICE_MAP.values()):
        series = [(to_date(ref), statistics.mean(d.values()))
                  for (ref, pp), d in monthly.items() if pp == p]
        prev = dt.date(2018, 10, 29)
        for k in sorted(QEND):
            e = dt.date.fromisoformat(QEND[k])
            vals = [v for dd, v in series if prev < dd <= e]
            prev = e
            if not vals:
                continue
            add(f"ca_farmprice_{p}_prairie_fq", QEND[k], k[0], f"Q{k[1]}", "",
                round(statistics.mean(vals), 2), "CAD per tonne",
                "official_stat",
                "Statistics Canada Table 32-10-0077, downloaded 2026-08-16",
                "mean of prairie monthly average farm prices whose mid-month "
                "falls inside the Deere fiscal quarter; FY2026 Q3 uses May "
                "and June 2026 only (July not yet published)",
                geography="Prairie provinces")


# ------------------------------------------- 4. StatCan farm cash receipts
def statcan_fcr():
    path = os.path.join(SCRATCH, "32100046", "32100046.csv")
    if not os.path.exists(path):
        return
    keep = {"Total farm cash receipts": "total",
            "Total crop receipts": "crop",
            "Total receipts from direct payments": "direct_payments"}
    geos = {"Canada", "Saskatchewan", "Alberta", "Manitoba"}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        k = keep.get(r["Type of cash receipts"])
        if not k or r["GEO"] not in geos or r["REF_DATE"] < "2018" or not r["VALUE"]:
            continue
        add(f"ca_farmcashreceipts_{k}", r["REF_DATE"], "", "", "",
            round(float(r["VALUE"]) / 1000.0, 1), "CADm", "official_stat",
            "Statistics Canada Table 32-10-0046 (Farm cash receipts, "
            "quarterly), downloaded 2026-08-16",
            "calendar quarter, unadjusted; latest published quarter is "
            "2026-Q1 (Jan-Mar 2026) - no Q2 2026 data exists yet",
            geography=r["GEO"], country="Canada")


# --------------------------------------------------- 5. StatCan seeded area
def statcan_area():
    path = os.path.join(SCRATCH, "32100359", "32100359.csv")
    if not os.path.exists(path):
        return
    crops = {"Canola (rapeseed)": "canola", "Wheat, all": "wheat_all",
             "Wheat, spring": "wheat_spring", "Wheat, durum": "durum",
             "Barley": "barley"}
    geos = {"Canada", "Saskatchewan", "Alberta", "Manitoba"}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        c = crops.get(r["Type of crop"])
        if (not c or r["GEO"] not in geos or r["REF_DATE"] < "2019"
                or r["Harvest disposition"] != "Seeded area (acres)"
                or not r["VALUE"]):
            continue
        add(f"ca_seededarea_{c}", r["REF_DATE"], "", "", "",
            round(float(r["VALUE"]) / 1e6, 3), "million acres",
            "official_stat",
            "Statistics Canada Table 32-10-0359 (Estimated areas, yield, "
            "production of principal field crops), downloaded 2026-08-16",
            "crop year = calendar year; 2026 is the June 2026 seeding survey "
            "estimate", geography=r["GEO"], country="Canada")


# ------------------------------------------------- 6. hand-entered context
MANUAL = [
    # (series_id, period_end, fy, fq, segment, value, units, stype, source, notes, geo)
    ("aem_canada_retail_yoy", "2026-06-30", 2026, "Q3", "ag_tractors_all",
     -12.5, "percent YoY", "trade_press",
     "https://drgnews.com/2026/07/23/u-s-and-canadian-sales-of-combines-see-slight-increase-in-june-2026/ (23 Jul 2026), reporting AEM Canada Ag Tractor and Combine Report",
     "Canadian ag tractor unit retail sales, June 2026 vs June 2025"),
    ("aem_canada_retail_yoy", "2026-06-30", 2026, "Q3", "combines",
     14.2, "percent YoY", "trade_press",
     "https://drgnews.com/2026/07/23/u-s-and-canadian-sales-of-combines-see-slight-increase-in-june-2026/ (23 Jul 2026), reporting AEM",
     "Canadian combine unit retail sales, June 2026 vs June 2025"),
    ("aem_canada_retail_yoy", "2026-07-31", 2026, "Q3", "ag_tractors_all",
     -8.0, "percent YoY", "trade_press",
     "https://kxel.com/2026/08/14/sales-of-agricultural-tractors-and-combines-decline/ (14 Aug 2026), reporting AEM",
     "Canadian ag tractor unit retail sales, July 2026 vs July 2025 ('fell nearly 8%')"),
    ("aem_canada_retail_yoy", "2026-07-31", 2026, "Q3", "combines",
     -11.0, "percent YoY", "trade_press",
     "https://kxel.com/2026/08/14/sales-of-agricultural-tractors-and-combines-decline/ (14 Aug 2026), reporting AEM",
     "Canadian combine unit retail sales, July 2026 vs July 2025 ('declined almost 11%')"),
    ("aem_canada_retail_ytd_yoy", "2026-07-31", 2026, "Q3", "tractors_4wd",
     -22.6, "percent YoY", "trade_press",
     "https://www.realagriculture.com/2026/08/new-4wd-tractor-sales-continue-to-struggle-through-august (Aug 2026), reporting AEM",
     "Canada year-to-date through July 2026 vs same period 2025"),
    ("aem_canada_retail_ytd_yoy", "2026-07-31", 2026, "Q3", "tractors_2wd",
     -8.9, "percent YoY", "trade_press",
     "https://www.realagriculture.com/2026/08/new-4wd-tractor-sales-continue-to-struggle-through-august (Aug 2026), reporting AEM",
     "Canada year-to-date through July 2026 vs same period 2025"),
    ("aem_canada_retail_ytd_yoy", "2026-07-31", 2026, "Q3", "combines",
     -1.9, "percent YoY", "trade_press",
     "https://www.realagriculture.com/2026/08/new-4wd-tractor-sales-continue-to-struggle-through-august (Aug 2026), reporting AEM",
     "Canada year-to-date through July 2026 vs same period 2025"),
    ("china_ad_duty_canola_seed", "2026-03-01", 2026, "Q2", "canola_seed",
     5.9, "percent", "official_stat",
     "https://www.canolacouncil.org/china-update/ ; MOFCOM final determination 28 Feb 2026, effective 1 Mar 2026",
     "cut from the 75.8% preliminary rate imposed Aug 2025; stacks on the 9% MFN duty for 14.9% all-in"),
    ("china_duty_canola_meal", "2026-03-01", 2026, "Q2", "canola_meal",
     0.0, "percent", "official_stat",
     "https://www.canolacouncil.org/china-update/ ; MOFCOM/MoF 27 Feb 2026",
     "100% tariff suspended to 0% for 1 Mar 2026 - 31 Dec 2026 only"),
    ("us_tariff_ag_equipment", "2026-06-08", 2026, "Q3", "ag_equipment",
     15.0, "percent", "official_stat",
     "https://www.pwc.com/ca/en/services/tax/publications/tax-insights/us-tariffs-steel-aluminum-copper-imports-update-2026.html (June 2026 update); US proclamation of 1 Jun 2026",
     "US Sec.232 derivative rate on agricultural equipment cut from 25% to "
     "15% effective 8 Jun 2026 through 31 Dec 2027; CUSMA-qualifying mobile "
     "industrial equipment taxed on non-US content with a 15% floor",
     "Canada-US"),
    ("us_softwood_lumber_duty", "2025-08-31", 2025, "Q4", "softwood_lumber",
     35.2, "percent", "trade_press",
     "https://www.rbc.com/en/economics/canadian-analysis/featured-analysis/insights/decades-of-trade-disputes-reshape-canadas-softwood-lumber-sector/ (Feb 2026)",
     "combined AD/CVD rate on Canadian softwood lumber set summer 2025; plus "
     "a 10% Sec.232 tariff on softwood and 25% on derivative wood products "
     "from mid-Oct 2025 - the key pressure on Canadian forestry equipment demand",
     "Canada"),
]


def manual():
    for (sid, pe, fy, fq, seg, val, units, st, src, note, *geo) in MANUAL:
        add(sid, pe, fy, fq, seg, val, units, st, src, note,
            geography=(geo[0] if geo else "Canada"))


# --------------------------------------------------------------- forecast
FORECAST = [
    ("PPA", 340, 295, 390, 1.5),
    ("SAT", 175, 158, 195, 18.2),
    ("CF", 200, 170, 240, -9.9),
    ("FS", 196, 186, 208, 3.2),
    ("TOTAL", 911, 809, 1033, 1.8),
]


# ------------------------------------------------ 7. Canadian lumber output
def lumber():
    path = os.path.join(SCRATCH, "16100017", "16100017.csv")
    if not os.path.exists(path):
        return
    tot = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        p = r["North American Product Classification System (NAPCS)"]
        if (r["GEO"] != "Canada" or r["UOM"] != "Cubic metres"
                or "production" not in p or not r["VALUE"]
                or r["REF_DATE"] < "2019-01"):
            continue
        tot[r["REF_DATE"]] = tot.get(r["REF_DATE"], 0.0) + float(r["VALUE"])
    for ref, v in sorted(tot.items()):
        add("ca_lumber_production", ref, "", "", "sawn_lumber",
            round(v / 1000.0, 1), "thousand cubic metres", "official_stat",
            "Statistics Canada Table 16-10-0017 (Lumber production, shipments "
            "and stocks by species, monthly), downloaded 2026-08-16",
            "sum of all species' production; proxy for Canadian forestry "
            "activity feeding Deere's CF segment; last observation 2026-05")


def forecast():
    for seg, c, lo, hi, yoy in FORECAST:
        add("de_revrec_canada_forecast_q3fy2026", "2026-08-02", 2026, "Q3",
            seg, c, "USDm", "estimate",
            "desk-canada bottom-up estimate, 16 Aug 2026 (pre-announcement)",
            f"central case; low {lo} / high {hi}; implied YoY {yoy:+.1f}% on "
            f"the Q3 FY2025 Canada comparative; NOT an actual - Deere reports "
            f"Q3 FY2026 on 20 Aug 2026")


def main():
    deere_matrix()
    fx()
    statcan_prices()
    statcan_fcr()
    statcan_area()
    lumber()
    manual()
    forecast()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
