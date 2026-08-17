#!/usr/bin/env python3
"""
Build the tidy-long regional dataset for Deere's ASIA / AFRICA / OCEANIA /
MIDDLE EAST desk.

Sources
  1. Deere ASC 606 revenue-recognition footnote, 'Asia, Africa, Oceania, and
     Middle East' geography row, quarterly by segment. Extracted from the
     offline corpus by extract_deere_geo_aaome.py and transcribed here with
     the originating filing path recorded per row. Q4 of each year is derived
     (FY minus nine months) because Deere never publishes a standalone Q4.
  2. FRED daily FX, averaged over Deere fiscal quarters (network fetch).
  3. Country data (India tractor retails, monsoon, kharif, Australian crop,
     China excavators) transcribed from cited public sources.

Output: data/deere/regional/asia_africa_oceania_me.csv
Header: series_id,period_end,fiscal_year,fiscal_quarter,geography,country,
        segment,value,units,source_type,source,notes
"""
import csv
import io
import os
import statistics
import urllib.request

OUT = ("/Users/cor/Documents/projects/agents-vs-wall-street-starter/"
       "data/deere/regional/asia_africa_oceania_me.csv")

GEO = "Asia, Africa, Oceania, and Middle East"
CORPUS = "challenge/offline-data/deere/filings/"

HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter",
          "geography", "country", "segment", "value", "units",
          "source_type", "source", "notes"]

# ---------------------------------------------------------------- fiscal cal
# Deere fiscal quarter end dates (period ends as printed in the filings).
QEND = {
    (2019, 1): "2019-01-27", (2019, 2): "2019-04-28",
    (2019, 3): "2019-07-28", (2019, 4): "2019-11-03",
    (2020, 1): "2020-02-02", (2020, 2): "2020-05-03",
    (2020, 3): "2020-08-02", (2020, 4): "2020-11-01",
    (2021, 1): "2021-01-31", (2021, 2): "2021-05-02",
    (2021, 3): "2021-08-01", (2021, 4): "2021-10-31",
    (2022, 1): "2022-01-30", (2022, 2): "2022-05-01",
    (2022, 3): "2022-07-31", (2022, 4): "2022-10-30",
    (2023, 1): "2023-01-29", (2023, 2): "2023-04-30",
    (2023, 3): "2023-07-30", (2023, 4): "2023-10-29",
    (2024, 1): "2024-01-28", (2024, 2): "2024-04-28",
    (2024, 3): "2024-07-28", (2024, 4): "2024-10-27",
    (2025, 1): "2025-01-26", (2025, 2): "2025-04-27",
    (2025, 3): "2025-07-27", (2025, 4): "2025-11-02",
    (2026, 1): "2026-02-01", (2026, 2): "2026-05-03",
    (2026, 3): "2026-08-02",
}

# ------------------------------------------------- 1. revenue-recognition matrix
# (fy, q): {segment: value}. 'derived' marks Q4 = FY total minus nine months.
# FY2019 quarters predate the FY2020 re-segmentation, so they carry the legacy
# 'Agriculture and Turf' / 'Construction and Forestry' split (AT_legacy).
REV = {
    (2019, 1): dict(AT_legacy=453, CF_legacy=263, FS=30, Total=746),
    (2019, 2): dict(AT_legacy=647, CF_legacy=328, FS=30, Total=1005),
    (2019, 3): dict(AT_legacy=684, CF_legacy=375, FS=32, Total=1091),
    (2019, 4): dict(AT_legacy=704, CF_legacy=299, FS=34, Total=1037),
    (2020, 1): dict(PPA=189, SAT=315, CF=256, FS=34, Total=794),
    (2020, 2): dict(PPA=221, SAT=290, CF=251, FS=30, Total=792),
    (2020, 3): dict(PPA=312, SAT=319, CF=318, FS=32, Total=981),
    (2020, 4): dict(PPA=397, SAT=398, CF=328, FS=36, Total=1159),
    (2021, 1): dict(PPA=304, SAT=401, CF=353, FS=40, Total=1098),
    (2021, 2): dict(PPA=319, SAT=444, CF=393, FS=36, Total=1192),
    (2021, 3): dict(PPA=368, SAT=385, CF=308, FS=38, Total=1099),
    (2021, 4): dict(PPA=426, SAT=449, CF=277, FS=39, Total=1191),
    (2022, 1): dict(PPA=241, SAT=352, CF=219, FS=40, Total=852),
    (2022, 2): dict(PPA=367, SAT=399, CF=318, FS=37, Total=1121),
    (2022, 3): dict(PPA=510, SAT=419, CF=296, FS=36, Total=1261),
    (2022, 4): dict(PPA=452, SAT=438, CF=303, FS=38, Total=1231),
    (2023, 1): dict(PPA=375, SAT=400, CF=300, FS=41, Total=1116),
    (2023, 2): dict(PPA=614, SAT=469, CF=335, FS=43, Total=1461),
    (2023, 3): dict(PPA=720, SAT=422, CF=271, FS=45, Total=1458),
    (2023, 4): dict(PPA=457, SAT=388, CF=277, FS=47, Total=1169),
    (2024, 1): dict(PPA=435, SAT=341, CF=258, FS=56, Total=1090),
    (2024, 2): dict(PPA=414, SAT=373, CF=271, FS=54, Total=1112),
    (2024, 3): dict(PPA=350, SAT=360, CF=300, FS=52, Total=1062),
    (2024, 4): dict(PPA=331, SAT=406, CF=299, FS=59, Total=1095),
    (2025, 1): dict(PPA=205, SAT=308, CF=224, FS=55, Total=792),
    (2025, 2): dict(PPA=312, SAT=385, CF=277, FS=53, Total=1027),
    (2025, 3): dict(PPA=332, SAT=393, CF=313, FS=53, Total=1091),
    (2025, 4): dict(PPA=489, SAT=448, CF=340, FS=56, Total=1333),
    (2026, 1): dict(PPA=325, SAT=376, CF=288, FS=54, Total=1043),
    (2026, 2): dict(PPA=329, SAT=446, CF=369, FS=54, Total=1198),
}
DERIVED_Q4 = {2019, 2020, 2021, 2022, 2023, 2024, 2025}

# filing each quarter's three-month column was read from
SRC = {
    (2019, 1): CORPUS + "2019-02-15__de-us-20190215-q1-10q__469204.md",
    (2019, 2): CORPUS + "2019-05-17__de-us-20190517-q2-10q__469675.md",
    (2019, 3): CORPUS + "2019-08-16__de-us-20190816-q3-10q__469206.md",
    (2019, 4): CORPUS + "2019-11-27__de-us-20191127-q4-10k__469283.md",
    (2020, 1): CORPUS + "2021-02-19__de-us-20210219-q1-10q__105814.md",
    (2020, 2): CORPUS + "2021-05-21__de-us-20210521-q2-10q__105821.md",
    (2020, 3): CORPUS + "2021-08-20__de-us-20210820-q3-10q__105837.md",
    (2020, 4): CORPUS + "2022-11-23__de-us-20221123-q4-10k__105816.md",
    (2021, 1): CORPUS + "2021-02-19__de-us-20210219-q1-10q__105814.md",
    (2021, 2): CORPUS + "2021-05-21__de-us-20210521-q2-10q__105821.md",
    (2021, 3): CORPUS + "2021-08-20__de-us-20210820-q3-10q__105837.md",
    (2021, 4): CORPUS + "2023-11-22__de-us-20231122-q4-10k__105844.md",
    (2022, 1): CORPUS + "2022-02-18__de-us-20220218-q1-10q__105834.md",
    (2022, 2): CORPUS + "2022-05-20__de-us-20220520-q2-10q__105838.md",
    (2022, 3): CORPUS + "2022-08-19__de-us-20220819-q3-10q__105818.md",
    (2022, 4): CORPUS + "2024-11-21__de-us-20241121-q4-10k__105810.md",
    (2023, 1): CORPUS + "2023-02-17__de-us-20230217-q1-10q__105813.md",
    (2023, 2): CORPUS + "2023-05-19__de-us-20230519-q2-10q__105852.md",
    (2023, 3): CORPUS + "2023-08-18__de-us-20230818-q3-10q__105835.md",
    (2023, 4): CORPUS + "2025-11-26__de-us-20251126-q4-10k__469216.md",
    (2024, 1): CORPUS + "2024-02-15__de-us-20240215-q1-10q__105826.md",
    (2024, 2): CORPUS + "2024-05-16__de-us-20240516-q2-10q__105820.md",
    (2024, 3): CORPUS + "2024-08-15__de-us-20240815-q3-10q__105828.md",
    (2024, 4): CORPUS + "2025-11-26__de-us-20251126-q4-10k__469216.md",
    (2025, 1): CORPUS + "2025-02-13__de-us-20250213-q1-10q__105832.md",
    (2025, 2): CORPUS + "2025-05-15__de-us-20250515-q2-10q__105831.md",
    (2025, 3): CORPUS + "2025-08-14__de-us-20250814-q3-10q__155834.md",
    (2025, 4): CORPUS + "2025-11-26__de-us-20251126-q4-10k__469216.md",
    (2026, 1): CORPUS + "2026-02-26__de-us-20260226-q1-10q__636995.md",
    (2026, 2): CORPUS + "2026-05-28__de-us-20260528-q2-10q__1055932.md",
}

# ------------------------------------------------------------------- 2. FX
FRED = {
    "DEXINUS": ("fx_inr_per_usd", "INR per USD", "India"),
    "DEXUSAL": ("fx_usd_per_aud", "USD per AUD", "Australia"),
    "DEXJPUS": ("fx_jpy_per_usd", "JPY per USD", "Japan"),
    "DEXCHUS": ("fx_cny_per_usd", "CNY per USD", "China"),
}


def fred_daily(series_id):
    url = ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s&cosd=2018-01-01"
           % series_id)
    with urllib.request.urlopen(url, timeout=60) as r:
        text = r.read().decode()
    out = []
    for row in csv.DictReader(io.StringIO(text)):
        d = row.get("observation_date") or row.get("DATE")
        v = row[series_id]
        if v in (".", "", None):
            continue
        out.append((d, float(v)))
    return out


def q_window(fy, q):
    """(start, end) for a Deere fiscal quarter, from the prior quarter end."""
    end = QEND[(fy, q)]
    prev = QEND.get((fy, q - 1)) if q > 1 else QEND.get((fy - 1, 4))
    if prev is None:
        return None
    y, m, d = (int(x) for x in prev.split("-"))
    import datetime
    start = (datetime.date(y, m, d) + datetime.timedelta(days=1)).isoformat()
    return start, end


def main():
    rows = []

    def add(**kw):
        r = {h: kw.get(h, "") for h in HEADER}
        rows.append(r)

    # --- segment revenue history -------------------------------------------
    for (fy, q), segs in sorted(REV.items()):
        note = ""
        if q == 4 and fy in DERIVED_Q4:
            note = ("derived: fiscal-year total from 10-K less nine-month "
                    "figure from the Q3 10-Q; Deere does not publish a "
                    "standalone Q4 revenue-recognition table")
        if fy == 2019:
            note = (note + "; " if note else "") + (
                "pre-FY2020 re-segmentation: Agriculture & Turf and "
                "Construction & Forestry basis, not PPA/SAT/CF")
        for seg, val in segs.items():
            add(series_id="deere_revrec_geo_segment_usdm",
                period_end=QEND[(fy, q)], fiscal_year=fy, fiscal_quarter="Q%d" % q,
                geography=GEO, country="", segment=seg, value=val, units="USDm",
                source_type="filing", source=SRC[(fy, q)], notes=note)

    # restated FY2019 five-segment full year (only available at FY level)
    for seg, val in dict(PPA=1039, SAT=1449, CF=1265, FS=126, Total=3879).items():
        add(series_id="deere_revrec_geo_segment_usdm", period_end="2019-11-03",
            fiscal_year=2019, fiscal_quarter="FY", geography=GEO, segment=seg,
            value=val, units="USDm", source_type="filing",
            source=CORPUS + "2021-12-16__de-us-20211216-fy-10k__645298.md",
            notes="FY2019 restated onto the PPA/SAT/CF basis; no quarterly "
                  "restatement was ever published for FY2019")

    # --- FX ------------------------------------------------------------------
    for sid, (name, units, country) in FRED.items():
        try:
            daily = fred_daily(sid)
        except Exception as exc:              # network optional
            print("WARN: FRED %s failed: %s" % (sid, exc))
            continue
        for (fy, q) in sorted(QEND):
            win = q_window(fy, q)
            if not win:
                continue
            a, b = win
            vals = [v for d, v in daily if a <= d <= b]
            if len(vals) < 20:
                continue
            add(series_id=name, period_end=QEND[(fy, q)], fiscal_year=fy,
                fiscal_quarter="Q%d" % q, geography=GEO, country=country,
                segment="", value=round(statistics.mean(vals), 4), units=units,
                source_type="macro",
                source="https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + sid,
                notes="mean of %d daily observations over the Deere fiscal "
                      "quarter %s..%s" % (len(vals), a, b))

    # --- India: tractor retail (FADA) ---------------------------------------
    fada = [
        # month_end, industry units, JD India units, JD share %
        ("2025-05-31", 2025, 74744, 5900, 7.89,
         "https://www.tractorjunction.com/tractor-news/fada-retail-tractor-sales-report-may-2026"),
        ("2026-05-31", 2026, 83092, 6039, 7.27,
         "https://www.tractorjunction.com/tractor-news/fada-retail-tractor-sales-report-may-2026"),
        ("2025-06-30", 2025, 80456, 6178, 7.68,
         "https://www.tractorjunction.com/tractor-news/fada-retail-tractor-sales-report-june-2026"),
        ("2026-06-30", 2026, 100818, 7165, 7.11,
         "https://www.tractorjunction.com/tractor-news/fada-retail-tractor-sales-report-june-2026"),
        ("2025-07-31", 2025, 91604, 6986, 7.63,
         "https://www.tractorjunction.com/tractor-news/fada-jul-2026-retail-tractor-sales-grow-28-13-percent-reach-117349-units"),
        ("2026-07-31", 2026, 117349, 8087, 6.89,
         "https://www.tractorjunction.com/tractor-news/fada-jul-2026-retail-tractor-sales-grow-28-13-percent-reach-117349-units"),
    ]
    for pe, yr, ind, jd, share, src in fada:
        fq = "Q3" if pe[5:7] in ("05", "06", "07") else ""
        add(series_id="india_tractor_retail_industry_units", period_end=pe,
            fiscal_year=(2026 if yr == 2026 else 2025), fiscal_quarter=fq,
            geography=GEO, country="India", segment="SAT", value=ind,
            units="units", source_type="industry", source=src,
            notes="FADA monthly vehicle-registration retail data, all-India; "
                  "calendar month, maps to Deere fiscal Q3 window "
                  "4 May - 2 Aug")
        add(series_id="india_tractor_retail_johndeere_units", period_end=pe,
            fiscal_year=(2026 if yr == 2026 else 2025), fiscal_quarter=fq,
            geography=GEO, country="India", segment="SAT", value=jd,
            units="units", source_type="industry", source=src,
            notes="John Deere India retail registrations (FADA)")
        add(series_id="india_tractor_retail_johndeere_share_pct", period_end=pe,
            fiscal_year=(2026 if yr == 2026 else 2025), fiscal_quarter=fq,
            geography=GEO, country="India", segment="SAT", value=share,
            units="percent", source_type="industry", source=src,
            notes="John Deere India share of FADA-reported tractor retails")

    add(series_id="india_tractor_wholesale_domestic_units", period_end="2026-06-30",
        fiscal_year=2026, fiscal_quarter="Q3", geography=GEO, country="India",
        segment="SAT", value=126112, units="units", source_type="industry",
        source="https://www.tractorjunction.com/tractor-news/domestic-tractor-wholesale-sales-grow-11-92-percent-in-june-2026",
        notes="domestic wholesale (factory dispatches), +11.92% YoY")

    # --- India: monsoon ------------------------------------------------------
    monsoon = [
        ("2026-06-30", "india_monsoon_monthly_pct_lpa", 60,
         "June 2026 all-India southwest monsoon rainfall approx 60% of LPA "
         "(approx 40% deficit); driest June in over a decade, reported as "
         "fifth-lowest June (99.5 mm) since 1901",
         "https://www.downtoearth.org.in/climate-change/daily-weather-tracker-july-2026-forecast-signals-below-normal-rainfall-and-higher-temperatures-across-india"),
        ("2026-07-31", "india_monsoon_monthly_pct_lpa", 104,
         "July 2026 rainfall 290.3 mm vs normal 280.5 mm, approx +4% "
         "(reported elsewhere as 103% of LPA); fifth consecutive "
         "above-normal July",
         "https://www.skymetweather.com/content/monsoon-update/junejuly-2026-contrasting-monsoon-months-high-stakes-for-august"),
        ("2026-07-09", "india_monsoon_cumulative_pct_lpa", 88,
         "1 June - 9 July 2026: 205 mm actual vs 233.1 mm LPA, 14% deficit",
         "https://www.business-standard.com/india-news/india-monsoon-rainfall-deficit-drought-imd-classification-126071000494_1.html"),
        ("2026-07-18", "india_monsoon_cumulative_pct_lpa", 76,
         "deficit widened back to 24% by 18 July 2026 during a monsoon break",
         "https://www.skymetweather.com/content/monsoon-update/junejuly-2026-contrasting-monsoon-months-high-stakes-for-august"),
        ("2026-08-02", "india_monsoon_cumulative_pct_lpa", 88,
         "season-to-date shortfall 12% of LPA as of 2 August 2026 - this is "
         "the Deere FY2026 Q3 quarter-end date",
         "https://www.skymetweather.com/content/monsoon-update/junejuly-2026-contrasting-monsoon-months-high-stakes-for-august"),
        ("2026-08-09", "india_monsoon_cumulative_pct_lpa", 89,
         "deficit narrowed to 11% below LPA as of 9 August 2026",
         "https://www.newsbytesapp.com/news/india/imd-monsoon-deficit-narrows-to-11-but-below-normal-rains-expected/tldr"),
        ("2026-09-30", "india_monsoon_season_forecast_pct_lpa", 90,
         "IMD updated long-range forecast: June-September 2026 seasonal "
         "rainfall likely 90% of LPA (below normal). FORECAST, not actual",
         "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2266479&reg=3&lang=1"),
    ]
    for pe, sid, val, note, src in monsoon:
        add(series_id=sid, period_end=pe, fiscal_year=2026,
            fiscal_quarter="Q3", geography=GEO, country="India", segment="",
            value=val, units="percent_of_LPA", source_type="macro",
            source=src, notes=note)

    kharif = [
        ("2026-06-30", -23.0, "kharif sown area approx 23% below year-ago at "
         "end-June 2026",
         "https://investmentguruindia.com/editorial/uploads/news-pdf/1ef39290_ICRA%20Thematic-%20Mid-Monsoon%20Update%20-%20August%202026.pdf"),
        ("2026-07-31", -3.0, "year-on-year contraction narrowed to approx 3% "
         "at end-July 2026 after surplus July rain; total planted area "
         "trailing by 3.88 m ha in late July",
         "https://www.fas.usda.gov/data/gain/2026/08/india-monsoon-recovery-fails-boost-sluggish-crop-planting"),
    ]
    for pe, val, note, src in kharif:
        add(series_id="india_kharif_sown_area_yoy_pct", period_end=pe,
            fiscal_year=2026, fiscal_quarter="Q3", geography=GEO,
            country="India", segment="", value=val, units="percent_yoy",
            source_type="macro", source=src, notes=note)

    add(series_id="india_msp_common_paddy_inr_per_quintal", period_end="2026-05-13",
        fiscal_year=2026, fiscal_quarter="Q3", geography=GEO, country="India",
        segment="", value=2441, units="INR_per_quintal", source_type="macro",
        source="https://ddnews.gov.in/en/cabinet-approves-higher-msp-for-14-kharif-crops-for-2026-27-marketing-season/",
        notes="kharif marketing season 2026-27 MSP approved 13 May 2026, up "
              "INR 72 (+3.0%) from INR 2,369; falls inside the Q3 window")

    # --- Australia ------------------------------------------------------------
    aus = [
        ("australia_winter_crop_production_mt", 54.5, "Mt",
         "ABARES June 2026 Australian Crop Report: 2026-27 winter crop "
         "forecast 54.5 Mt, down 21% YoY, still 4% above the 10-year average"),
        ("australia_wheat_production_mt", 26.7, "Mt",
         "2026-27 wheat production forecast 26.7 Mt, down 26% YoY and 23% "
         "below the five-year average"),
        ("australia_wheat_area_mha", 10.9, "million_ha",
         "2026-27 wheat area forecast 10.9 m ha, down 12% YoY, smallest "
         "since 2019-20"),
    ]
    for sid, val, units, note in aus:
        add(series_id=sid, period_end="2026-06-02", fiscal_year=2026,
            fiscal_quarter="Q3", geography=GEO, country="Australia",
            segment="PPA", value=val, units=units, source_type="macro",
            source="https://www.agriculture.gov.au/abares/research-topics/agricultural-outlook/australian-crop-report/june-2026",
            notes=note + ". FORECAST published inside the Q3 window")

    # --- China / construction --------------------------------------------------
    china = [
        ("2026-06-30", "china_excavator_sales_total_units", 152320,
         "January-June 2026 total excavator sales in China, +26.4% YoY "
         "(H1 cumulative)"),
        ("2026-06-30", "china_excavator_sales_domestic_units", 79025,
         "H1 2026 domestic excavator sales, +20.4% YoY"),
        ("2026-06-30", "china_excavator_sales_export_units", 73295,
         "H1 2026 excavator exports, +33.5% YoY"),
    ]
    for pe, sid, val, note in china:
        add(series_id=sid, period_end=pe, fiscal_year=2026, fiscal_quarter="Q3",
            geography=GEO, country="China", segment="CF", value=val,
            units="units", source_type="industry",
            source="https://www.steelorbis.com/steel-news/latest-news/chinas-excavator-sales-increase-by-264-percent-in-january-june-2026-1462881.htm",
            notes=note)
    add(series_id="china_excavator_sales_yoy_pct", period_end="2026-07-31",
        fiscal_year=2026, fiscal_quarter="Q3", geography=GEO, country="China",
        segment="CF", value=25.0, units="percent_yoy", source_type="industry",
        source="https://www.mysteel.net/news/5094904-ccma-chinas-excavator-sales-surge-25-yoy-in-july-sustaining-uptrend",
        notes="CCMA: China excavator sales +25% YoY in July 2026, uptrend "
              "sustained; July falls inside the Deere Q3 window")

    # --- Deere's own Asia industry outlook, as guided ---------------------------
    guide = [
        ("2025-11-26", "down ~5%", -5.0,
         CORPUS.replace("filings/", "call-transcripts/") +
         "2025-11-26__de-us-20251126-call-q4-pres-2__361265.md",
         "Q4 FY2025 call: 'Industry sales in Asia are expected to be down 5% "
         "following slight gains in India last year'"),
        ("2026-02-19", "flat to down 5%", -2.5,
         CORPUS.replace("filings/", "call-transcripts/") +
         "2026-02-19__de-us-20260219-call-pres__605076.md",
         "Q1 FY2026 call: Asia flat to down 5%; 'The Indian market is now "
         "expected to only be down slightly from the strong level seen in 2025'"),
        ("2026-05-21", "roughly flat", 0.0,
         CORPUS.replace("filings/", "call-transcripts/") +
         "2026-05-21__de-us-20260521-call-pres__1042774.md",
         "Q2 FY2026 call: 'Industry sales in Asia are now projected to be "
         "roughly flat year-over-year, mainly driven by modest improvements "
         "within the India market' - third consecutive upgrade"),
    ]
    for pe, label, val, src, note in guide:
        add(series_id="deere_asia_ag_industry_outlook_pct", period_end=pe,
            fiscal_year=2026, fiscal_quarter="FY", geography=GEO, country="Asia",
            segment="", value=val, units="percent_yoy_midpoint",
            source_type="filing", source=src,
            notes=note + " [midpoint encoded as '%s']" % label)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("wrote %d rows to %s" % (len(rows), OUT))


if __name__ == "__main__":
    main()
