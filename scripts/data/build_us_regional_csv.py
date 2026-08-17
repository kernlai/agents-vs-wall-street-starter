#!/usr/bin/env python3
"""
Build the United States regional desk CSV for the Deere FY2026 Q3 bottom-up forecast.

Sources
-------
1. Deere ASC 606 revenue-recognition footnote (segment x primary geographic market),
   extracted from the offline corpus by extract_de_geo_matrix.py. Quarterly Q1-Q3 come
   straight from the 10-Qs; Q4 is derived as (fiscal year total - nine months) and is
   flagged as such in `notes`.
2. FRED keyless CSV endpoint (macro / commodity / construction series).
3. AEM US Ag Tractor and Combine Report (retail unit sales) - published PDFs / press
   releases, cited individually.
4. USDA NASS / ERS / EPA / Federal Reserve, cited individually.

Output: tidy long CSV.
"""
import csv
import os
import subprocess
import sys
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/regional/us.csv"

HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "geography",
          "country", "segment", "value", "units", "source_type", "source", "notes"]

# ---------------------------------------------------------------- fiscal calendar
FY_END = {2019: "2019-11-03", 2020: "2020-11-01", 2021: "2021-10-31", 2022: "2022-10-30",
          2023: "2023-10-29", 2024: "2024-10-27", 2025: "2025-11-02"}

# quarter end -> (fy, q); from the filings themselves
QTR = {
    "2019-01-27": (2019, 1), "2019-04-28": (2019, 2), "2019-07-28": (2019, 3),
    "2020-02-02": (2020, 1), "2020-05-03": (2020, 2), "2020-08-02": (2020, 3),
    "2021-01-31": (2021, 1), "2021-05-02": (2021, 2), "2021-08-01": (2021, 3),
    "2022-01-30": (2022, 1), "2022-05-01": (2022, 2), "2022-07-31": (2022, 3),
    "2023-01-29": (2023, 1), "2023-04-30": (2023, 2), "2023-07-30": (2023, 3),
    "2024-01-28": (2024, 1), "2024-04-28": (2024, 2), "2024-07-28": (2024, 3),
    "2025-01-26": (2025, 1), "2025-04-27": (2025, 2), "2025-07-27": (2025, 3),
    "2026-02-01": (2026, 1), "2026-05-03": (2026, 2),
}

SEG4 = ["PPA", "SAT", "CF", "FS"]
SEG3 = ["AT", "CF", "FS"]          # pre-FY2020 presentation: Ag & Turf / C&F / FS

# ---------------------------------------------------------------- 1. matrix rows
def matrix_rows():
    """Run the extractor and emit US quarterly + fiscal-year revenue rows."""
    raw = subprocess.run([sys.executable, os.path.join(HERE, "extract_de_geo_matrix.py")],
                         capture_output=True, text=True, check=True).stdout
    rdr = csv.DictReader(raw.splitlines())
    us = {}   # (period_end, months) -> (values, source)
    for r in rdr:
        if r["geography"] != "united_states":
            continue
        us[(r["period_end"], int(r["months"]))] = (
            [int(x) for x in r["values"].split("|")], r["source"])

    rows = []
    # -- reported three-month quarters
    for (pend, months), (vals, src) in sorted(us.items()):
        if months != 3 or pend not in QTR:
            continue
        fy, q = QTR[pend]
        segs = SEG4 if len(vals) == 5 else SEG3
        for seg, v in zip(segs + ["TOTAL"], vals):
            rows.append(dict(
                series_id="de_rev606_us_quarterly", period_end=pend, fiscal_year=fy,
                fiscal_quarter=f"Q{q}", geography="United States", country="United States",
                segment=seg, value=v, units="USD_millions", source_type="filing",
                source=f"corpus:challenge/offline-data/deere/filings/{src}",
                notes="ASC 606 revenue from contracts with customers; does not tie to 8-K segment net sales"))

    # -- fiscal-year totals (hand-verified from the fy-10k geographic tables)
    fy_tot = {
        2019: dict(PPA=6772, SAT=5590, CF=6082, FS=2482, TOTAL=20926,
                   src="2021-12-16__de-us-20211216-fy-10k__645298.md", note="restated to four-segment structure"),
        2020: dict(PPA=6889, SAT=5059, CF=4548, FS=2500, TOTAL=18996,
                   src="2021-12-16__de-us-20211216-fy-10k__645298.md", note="restated to four-segment structure"),
        2021: dict(PPA=8223, SAT=6505, CF=5697, FS=2389, TOTAL=22814,
                   src="2021-12-16__de-us-20211216-fy-10k__645298.md", note=""),
        2022: dict(PPA=10975, SAT=7741, CF=7103, FS=2419, TOTAL=28238,
                   src="2023-12-15__de-us-20231215-fy-10k__645297.md", note=""),
        2023: dict(PPA=13917, SAT=7796, CF=9109, FS=3283, TOTAL=34105,
                   src="2023-12-15__de-us-20231215-fy-10k__645297.md", note=""),
        2024: dict(PPA=11741, SAT=6249, CF=8086, FS=4166, TOTAL=30242,
                   src="2025-12-18__de-us-20251218-fy-10k__393777.md", note=""),
        2025: dict(PPA=7753, SAT=5282, CF=6489, FS=4450, TOTAL=23974,
                   src="2025-12-18__de-us-20251218-fy-10k__393777.md", note=""),
    }
    for fy, d in sorted(fy_tot.items()):
        for seg in SEG4 + ["TOTAL"]:
            rows.append(dict(
                series_id="de_rev606_us_fiscal_year", period_end=FY_END[fy], fiscal_year=fy,
                fiscal_quarter="FY", geography="United States", country="United States",
                segment=seg, value=d[seg], units="USD_millions", source_type="filing",
                source=f"corpus:challenge/offline-data/deere/filings/{d['src']}",
                notes=("ASC 606 basis " + d["note"]).strip()))

    # -- Q4 derived = fiscal year total minus nine months
    nine = {int(QTR[p][0]): (v, s) for (p, m), (v, s) in us.items()
            if m == 9 and p in QTR}
    for fy, (vals9, src9) in sorted(nine.items()):
        d = fy_tot[fy]
        segs = SEG4 if len(vals9) == 5 else SEG3
        if segs == SEG3:
            q4 = {"AT": d["PPA"] + d["SAT"] - vals9[0], "CF": d["CF"] - vals9[1],
                  "FS": d["FS"] - vals9[2], "TOTAL": d["TOTAL"] - vals9[3]}
        else:
            q4 = {s: d[s] - v for s, v in zip(SEG4, vals9)}
            q4["TOTAL"] = d["TOTAL"] - vals9[4]
        for seg, v in q4.items():
            rows.append(dict(
                series_id="de_rev606_us_quarterly", period_end=FY_END[fy], fiscal_year=fy,
                fiscal_quarter="Q4", geography="United States", country="United States",
                segment=seg, value=v, units="USD_millions", source_type="filing_derived",
                source=(f"corpus:challenge/offline-data/deere/filings/{d['src']} minus "
                        f"corpus:challenge/offline-data/deere/filings/{src9}"),
                notes="DERIVED: fiscal-year total less nine-month figure; Deere does not publish a Q4-only matrix"))
    return rows


# ---------------------------------------------------------------- 2. FRED drivers
FRED = [
    ("HOUST", "US_housing_starts_total", "thousand_units_saar", "monthly"),
    ("HOUST1F", "US_housing_starts_single_family", "thousand_units_saar", "monthly"),
    ("TTLCONS", "US_construction_spending_total", "USD_millions_saar", "monthly"),
    ("TLPRVCONS", "US_construction_spending_private", "USD_millions_saar", "monthly"),
    ("TLNRESCONS", "US_construction_spending_private_nonres", "USD_millions_saar", "monthly"),
    ("TLPBLCONS", "US_construction_spending_public", "USD_millions_saar", "monthly"),
    ("TLHWYCONS", "US_construction_spending_highway_street", "USD_millions_saar", "monthly"),
    ("PMAIZMTUSDM", "corn_price_global", "USD_per_metric_ton", "monthly"),
    ("PSOYBUSDM", "soybean_price_global", "USD_per_metric_ton", "monthly"),
    ("MCOILWTICO", "wti_crude_price", "USD_per_barrel", "monthly"),
    ("PNRGINDEXM", "energy_price_index", "index_2016_100", "monthly"),
    ("FEDFUNDS", "fed_funds_effective_rate", "percent", "monthly"),
]


def fred_rows(start="2018-11-01"):
    rows = []
    for sid, label, units, _freq in FRED:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "deere-regional-research (cor@salomo.io)"})
        try:
            txt = urllib.request.urlopen(req, timeout=45).read().decode()
        except Exception as e:                       # missing data stays missing
            print(f"  ! {sid}: {e}", file=sys.stderr)
            continue
        if "<html" in txt[:200].lower():
            print(f"  ! {sid}: non-CSV response, skipped", file=sys.stderr)
            continue
        for line in txt.strip().split("\n")[1:]:
            parts = line.split(",")
            if len(parts) != 2:
                continue
            d, v = parts
            if v in (".", "") or d < start:
                continue
            rows.append(dict(
                series_id=label, period_end=d, fiscal_year="", fiscal_quarter="",
                geography="United States", country="United States", segment="",
                value=v, units=units, source_type="official_statistics",
                source=url, notes=f"FRED series {sid}; observation date is period start"))
    return rows


# ---------------------------------------------------------------- 3. hand-keyed rows
AEM_MAY = "https://www.aem.org/getattachment/a717c93d-4798-4bfb-8daf-555dda8cd403/May-2026-Farm_Flash_Trade_Press_With_Chart_PreRelease-United-States.pdf"
AEM_JUL = "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html"
RFD_JUL = "https://www.rfdtv.com/farm-equipment-sales-remain-weak-through-july-2026"

MANUAL = [
    # --- AEM US retail units, May 2026 (report released 2026-06-10)
    ("aem_us_retail_units_month", "2026-05-31", "tractor_2wd_lt40hp", 11415, "units", AEM_MAY,
     "May 2026 month; May 2025 = 15,155 (-24.7% YoY)"),
    ("aem_us_retail_units_month", "2026-05-31", "tractor_2wd_40_100hp", 3986, "units", AEM_MAY,
     "May 2026 month; May 2025 = 4,714 (-15.4% YoY)"),
    ("aem_us_retail_units_month", "2026-05-31", "tractor_2wd_100hp_plus", 1270, "units", AEM_MAY,
     "May 2026 month; May 2025 = 1,416 (-10.3% YoY)"),
    ("aem_us_retail_units_month", "2026-05-31", "tractor_4wd", 144, "units", AEM_MAY,
     "May 2026 month; May 2025 = 176 (-18.2% YoY)"),
    ("aem_us_retail_units_month", "2026-05-31", "tractor_total", 16815, "units", AEM_MAY,
     "May 2026 month; May 2025 = 21,461 (-21.6% YoY)"),
    ("aem_us_retail_units_month", "2026-05-31", "combine_self_propelled", 138, "units", AEM_MAY,
     "May 2026 month; May 2025 = 314 (-56.1% YoY)"),
    ("aem_us_retail_units_ytd", "2026-05-31", "tractor_2wd_lt40hp", 46288, "units", AEM_MAY,
     "YTD through May 2026; 2025 = 53,908 (-14.1%)"),
    ("aem_us_retail_units_ytd", "2026-05-31", "tractor_2wd_40_100hp", 17844, "units", AEM_MAY,
     "YTD through May 2026; 2025 = 18,768 (-4.9%)"),
    ("aem_us_retail_units_ytd", "2026-05-31", "tractor_2wd_100hp_plus", 5881, "units", AEM_MAY,
     "YTD through May 2026; 2025 = 7,161 (-17.9%)"),
    ("aem_us_retail_units_ytd", "2026-05-31", "tractor_4wd", 766, "units", AEM_MAY,
     "YTD through May 2026; 2025 = 1,002 (-23.6%)"),
    ("aem_us_retail_units_ytd", "2026-05-31", "tractor_total", 70779, "units", AEM_MAY,
     "YTD through May 2026; 2025 = 80,839 (-12.4%)"),
    ("aem_us_retail_units_ytd", "2026-05-31", "combine_self_propelled", 1066, "units", AEM_MAY,
     "YTD through May 2026; 2025 = 1,248 (-14.6%)"),
    ("aem_us_field_inventory_units", "2026-05-01", "tractor_2wd_lt40hp", 62258, "units", AEM_MAY,
     "AEM beginning-of-May 2026 field inventory"),
    ("aem_us_field_inventory_units", "2026-05-01", "tractor_2wd_40_100hp", 24867, "units", AEM_MAY,
     "AEM beginning-of-May 2026 field inventory"),
    ("aem_us_field_inventory_units", "2026-05-01", "tractor_2wd_100hp_plus", 6553, "units", AEM_MAY,
     "AEM beginning-of-May 2026 field inventory"),
    ("aem_us_field_inventory_units", "2026-05-01", "tractor_4wd", 513, "units", AEM_MAY,
     "AEM beginning-of-May 2026 field inventory"),
    ("aem_us_field_inventory_units", "2026-05-01", "combine_self_propelled", 714, "units", AEM_MAY,
     "AEM beginning-of-May 2026 field inventory"),
    # --- AEM US retail, July 2026 (report released 2026-08-11)
    ("aem_us_retail_units_month", "2026-07-31", "tractor_total", 15985, "units", AEM_JUL,
     "July 2026 month; July 2025 = 17,938 (-10.9% YoY); 2WD -10.5%, 4WD -38.7%, combines -5.3%"),
    ("aem_us_retail_units_ytd", "2026-07-31", "tractor_total", 105185, "units", AEM_JUL,
     "YTD through July 2026, -13.1% YoY"),
    ("aem_us_retail_units_ytd", "2026-07-31", "combine_self_propelled", 1676, "units", AEM_JUL,
     "YTD through July 2026, -10.2% YoY"),
    ("aem_us_retail_pct_yoy_ytd", "2026-07-31", "tractor_2wd_lt40hp", -15.1, "percent", RFD_JUL,
     "YTD through July 2026 YoY change"),
    ("aem_us_retail_pct_yoy_ytd", "2026-07-31", "tractor_2wd_100hp_plus", -15.5, "percent", RFD_JUL,
     "YTD through July 2026 YoY change; July month alone approx -7%"),
    # --- Deere disclosed retail / inventory, rolling 3 months to April 2026 (Q2 FY26 deck)
    ("de_slide_industry_retail_r3m_pct", "2026-04-30", "tractor_2wd_lt40hp", -12, "percent",
     "corpus:challenge/offline-data/deere/slides/2026-05-21__de-us-20260521-slide__1042212.md",
     "US and Canada ag industry, rolling 3 months to April 2026, per AEM. SIGN CORRECTION: the corpus markdown renders these as bare positives; Deere's own column reads 'down more/less than the industry', and the magnitudes match AEM's negative YTD actuals. Deere: down a single digit"),
    ("de_slide_industry_retail_r3m_pct", "2026-04-30", "tractor_2wd_40_100hp", -4, "percent",
     "corpus:challenge/offline-data/deere/slides/2026-05-21__de-us-20260521-slide__1042212.md",
     "US and Canada ag industry rolling 3m to Apr-2026. Deere: down a single digit"),
    ("de_slide_industry_retail_r3m_pct", "2026-04-30", "tractor_2wd_100hp_plus", -14, "percent",
     "corpus:challenge/offline-data/deere/slides/2026-05-21__de-us-20260521-slide__1042212.md",
     "US and Canada ag industry rolling 3m to Apr-2026. Deere: DOWN MORE THAN THE INDUSTRY - share loss"),
    ("de_slide_industry_retail_r3m_pct", "2026-04-30", "tractor_4wd", -24, "percent",
     "corpus:challenge/offline-data/deere/slides/2026-05-21__de-us-20260521-slide__1042212.md",
     "US and Canada ag industry rolling 3m to Apr-2026. Deere: down less than the industry"),
    ("de_slide_industry_retail_r3m_pct", "2026-04-30", "combine", -5, "percent",
     "corpus:challenge/offline-data/deere/slides/2026-05-21__de-us-20260521-slide__1042212.md",
     "US and Canada ag industry rolling 3m to Apr-2026. Deere: flat"),
    ("de_dealer_inventory_pct_ttm_retail", "2026-04-30", "tractor_2wd_100hp_plus", 30, "percent",
     "corpus:challenge/offline-data/deere/slides/2026-05-21__de-us-20260521-slide__1042212.md",
     "Deere US and Canada dealer inventory, units as pct of trailing-12m retail; prior year 31%"),
    ("de_dealer_inventory_pct_ttm_retail", "2026-04-30", "combine", 12, "percent",
     "corpus:challenge/offline-data/deere/slides/2026-05-21__de-us-20260521-slide__1042212.md",
     "Deere US and Canada dealer inventory, units as pct of trailing-12m retail; prior year 17%"),
    # --- USDA crop conditions and acreage
    ("usda_crop_condition_good_excellent", "2026-07-26", "corn", 63, "percent",
     "https://www.dtnpf.com/agriculture/web/ag/news/article/2026/07/27/usda-crop-progress-corn-rated-63-63",
     "USDA Crop Progress week ending 2026-07-26; prior year 73%; poor/very-poor 12% vs 7% LY"),
    ("usda_crop_condition_good_excellent", "2026-07-26", "soybean", 63, "percent",
     "https://www.dtnpf.com/agriculture/web/ag/news/article/2026/07/27/usda-crop-progress-corn-rated-63-63",
     "USDA Crop Progress week ending 2026-07-26"),
    ("usda_crop_condition_good_excellent", "2026-08-02", "corn", 61, "percent",
     "https://www.dtnpf.com/agriculture/web/ag/news/article/2026/08/03/usda-crop-progress-corn-rated-61-63",
     "USDA Crop Progress week ending 2026-08-02; deteriorating through the window"),
    ("usda_crop_condition_good_excellent", "2026-08-02", "soybean", 63, "percent",
     "https://www.dtnpf.com/agriculture/web/ag/news/article/2026/08/03/usda-crop-progress-corn-rated-61-63",
     "USDA Crop Progress week ending 2026-08-02"),
    ("usda_planted_acres", "2026-06-30", "corn", 95.3, "million_acres",
     "https://www.nass.usda.gov/Newsroom/2026/06-30-2026.php",
     "USDA NASS Acreage 2026-06-30; down 3% vs 2025; fourth highest since 1944"),
    ("usda_planted_acres", "2026-06-30", "soybean", 85.4, "million_acres",
     "https://www.nass.usda.gov/Newsroom/2026/06-30-2026.php",
     "USDA NASS Acreage 2026-06-30; up 5% vs 2025"),
    ("usda_yield_forecast", "2026-08-12", "corn", 180.7, "bushels_per_acre",
     "https://www.dtnpf.com/agriculture/web/ag/news/article/2026/08/12/usda-releases-august-crop-production-4",
     "August 2026 WASDE / Crop Production; down from 183.0 in July"),
    ("usda_yield_forecast", "2026-08-12", "soybean", 52.7, "bushels_per_acre",
     "https://www.dtnpf.com/agriculture/web/ag/news/article/2026/08/12/usda-releases-august-crop-production-4",
     "August 2026 WASDE / Crop Production; down from 53.0 in July; 4.519bn bu = largest US soybean crop on record"),
    ("usda_season_avg_farm_price", "2026-08-12", "corn", 4.50, "USD_per_bushel",
     "https://www.dtnpf.com/agriculture/web/ag/news/article/2026/08/12/usda-releases-august-crop-production-4",
     "August 2026 WASDE season-average farm price, 2026/27 marketing year; raised"),
    ("usda_season_avg_farm_price", "2026-08-12", "soybean", 11.40, "USD_per_bushel",
     "https://www.dtnpf.com/agriculture/web/ag/news/article/2026/08/12/usda-releases-august-crop-production-4",
     "August 2026 WASDE season-average farm price, 2026/27 marketing year; unchanged"),
    # --- USDA ERS farm income (February 2026 vintage; next update 2026-09-03, after this event)
    ("usda_ers_net_farm_income", "2026-12-31", "", 153.4, "USD_billions",
     "https://www.ers.usda.gov/topics/farm-economy/farm-sector-income-finances/highlights-from-the-farm-income-forecast",
     "CY2026 forecast, February 2026 vintage: -0.7% nominal / -2.6% real vs 2025, still above the 2005-24 real average. Next vintage 2026-09-03 lands AFTER Deere's Q3 print"),
    ("usda_ers_net_cash_farm_income", "2026-12-31", "", 158.5, "USD_billions",
     "https://www.ers.usda.gov/topics/farm-economy/farm-sector-income-finances/highlights-from-the-farm-income-forecast",
     "CY2026 forecast, February 2026 vintage: +3.0% nominal vs 2025"),
    # --- drought
    ("us_drought_area_d1_plus", "2026-07-07", "", 47.2, "percent_of_area",
     "https://www.profarmer.com/news/drought-monitor-shows-little-change-overall-u-s-conditions",
     "US Drought Monitor 2026-07-07; 67.0% of the US abnormally dry or worse (D0+)"),
    ("us_drought_crop_area_d1_plus", "2026-07-07", "corn", 19, "percent_of_planted_area",
     "https://www.profarmer.com/news/drought-monitor-shows-little-change-overall-u-s-conditions",
     "Share of US corn acres in D1-D4 drought, early July 2026"),
    ("us_drought_crop_area_d1_plus", "2026-07-07", "soybean", 19, "percent_of_planted_area",
     "https://www.profarmer.com/news/drought-monitor-shows-little-change-overall-u-s-conditions",
     "Share of US soybean acres in D1-D4 drought, early July 2026"),
    # --- policy
    ("us_policy_farm_support", "2025-12-08", "", 12.0, "USD_billions",
     "https://www.usda.gov/about-usda/news/press-releases/2025/12/08/trump-administration-announces-12-billion-farmer-bridge-payments-american-farmers-impacted-unfair",
     "Farmer Bridge Assistance Program; row-crop bridge payments, targeted for release by 2026-02-28; soybean rate $30.88/acre. Liquidity support into the FY2026 buying season"),
    ("us_policy_rfs_total_volume", "2026-03-27", "", 25.82, "billion_RINs",
     "https://www.epa.gov/renewable-fuel-standard/final-renewable-fuel-standards-2026-and-2027",
     "EPA final RFS rule 2026-03-27: record 2026 volume, 2027 = 25.98bn RINs; conventional (corn ethanol) held at 15bn gallons"),
    ("us_policy_disaster_payment_factor", "2026-05-21", "", 70, "percent",
     "corpus:challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md",
     "Supplemental disaster relief program payment factor raised from 35% to 70% (Deere Q2 FY2026 call)"),
    ("de_tariff_cost_fy2026_gross", "2026-05-21", "", 1200, "USD_millions",
     "corpus:challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md",
     "Full-year direct tariff exposure, ~3pts of margin; split ~45% CF, ~33% SAT, ~20% large ag"),
    ("de_tariff_refund_q2fy2026", "2026-05-03", "", 272, "USD_millions",
     "corpus:challenge/offline-data/deere/filings/2026-05-21__de-us-20260521-q2-8k__1042167.md",
     "IEEPA refund recognised in Q2 FY2026 after the 2026-02-20 Supreme Court ruling; lifted equipment-ops margin ~2.5pts; one-off, not repeatable in Q3 at this scale"),
    ("de_tariff_cost_fy2026_net", "2026-05-21", "", 900, "USD_millions",
     "corpus:challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md",
     "FY2026 tariff cost net of the IEEPA refund"),
    # --- Deere-disclosed US order book / capacity
    ("de_cf_order_book_change_since_nov", "2026-05-21", "CF", 60, "percent",
     "corpus:challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md",
     "US and Canada C&F order book up more than 60% since November 2025, highest since April 2024; >80% of FY production slots filled"),
    ("de_us_manufacturing_share_of_us_sales", "2026-05-21", "", 80, "percent",
     "corpus:challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md",
     "~80% of Deere US complete-good sales are produced in US plants; ~75% of components at those plants are US-sourced"),
    # --- consensus (context only, not a Deere disclosure)
    ("street_consensus_q3fy2026_net_sales", "2026-08-02", "", 10870, "USD_millions",
     "https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html",
     "Sell-side consensus for Q3 FY2026 equipment-operations net sales, +4.95% vs $10,357m; consensus EPS $4.85 vs $4.75 LY. GLOBAL, not US-only"),
]


def manual_rows():
    out = []
    for sid, pend, seg, val, units, src, note in MANUAL:
        st = "filing" if src.startswith("corpus:") else (
            "official_statistics" if any(k in src for k in ("usda.gov", "epa.gov", "nass")) else "web")
        out.append(dict(series_id=sid, period_end=pend, fiscal_year="", fiscal_quarter="",
                        geography="United States", country="United States", segment=seg,
                        value=val, units=units, source_type=st, source=src, notes=note))
    return out


def main():
    rows = matrix_rows() + manual_rows() + fred_rows()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
