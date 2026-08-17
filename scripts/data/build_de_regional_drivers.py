#!/usr/bin/env python3
"""
Build region-specific driver series for a bottom-up geographic model of
Deere & Company, aligned to Deere FISCAL quarters.

Deere fiscal calendar: FY ends the Sunday nearest 31 October.
  Q1 = Nov, Dec, Jan     Q2 = Feb, Mar, Apr
  Q3 = May, Jun, Jul     Q4 = Aug, Sep, Oct
Fiscal year = calendar year + 1 for November and December observations.

Sources
  FRED keyless CSV endpoint (no API key needed), fetched with a descriptive UA.
  Deere's own regional industry-unit outlook, parsed out of the offline 8-K corpus.
  Hand-entered, individually cited point observations for series that have no
  free machine-readable feed (AEM units, CONAB, Plano Safra, ABARES, India
  tractor registrations, Argentine export-tax schedule, USDA net farm income).

Missing data is an ABSENT ROW. Never zero, never a guess.

Standard library only.
"""

import csv
import datetime as dt
import os
import re
import statistics
import sys
import urllib.request
from collections import defaultdict, OrderedDict

CACHE = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/fred"
OUT_CSV = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/drv_regional.csv"
MATRIX = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_geo_matrix.csv"
CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
UA = "deere-geo-model-research cor@salomo.io"

START_FY = 2015

# ---------------------------------------------------------- fiscal mapping ---

MONTH_TO_FQ = {
    11: "Q1", 12: "Q1", 1: "Q1",
    2: "Q2", 3: "Q2", 4: "Q2",
    5: "Q3", 6: "Q3", 7: "Q3",
    8: "Q4", 9: "Q4", 10: "Q4",
}


def fiscal(y, m):
    """Calendar (year, month) -> (fiscal_year, fiscal_quarter)."""
    return (y + 1 if m >= 11 else y), MONTH_TO_FQ[m]


# Representative period_end for each Deere fiscal quarter. The exact 52/53-week
# end dates for quarters we hold in the matrix are read from the matrix file;
# everything else uses the last day of the quarter's final calendar month, which
# is accurate to within a week and is flagged in the notes.
QTR_LAST_MONTH = {"Q1": 1, "Q2": 4, "Q3": 7, "Q4": 10}


def nominal_period_end(fy, fq):
    m = QTR_LAST_MONTH[fq]
    y = fy
    import calendar

    return "%04d-%02d-%02d" % (y, m, calendar.monthrange(y, m)[1])


# ------------------------------------------------------------- FRED loader ---


def fred(series_id):
    """Fetch a FRED series as [(date, float)], cached on disk."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, series_id + ".csv")
    if not os.path.exists(path):
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + series_id
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8", "replace")
        if not body.lstrip().lower().startswith("observation_date"):
            raise RuntimeError("FRED returned non-CSV for " + series_id)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
    out = []
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            d = row["observation_date"]
            v = row[series_id].strip()
            if v in ("", "."):
                continue  # genuine missing observation -- drop the row
            out.append((d, float(v)))
    return out


def to_fiscal_quarters(obs, how="mean"):
    """Aggregate dated observations into Deere fiscal quarters."""
    buckets = defaultdict(list)
    for d, v in obs:
        y, m, _ = (int(x) for x in d.split("-"))
        buckets[fiscal(y, m)].append(v)
    out = {}
    for k, vs in buckets.items():
        out[k] = statistics.fmean(vs) if how == "mean" else sum(vs)
    return out


# ---------------------------------------------------------- driver catalog ---

# (series_id, FRED id, geography, units, how, notes)
FRED_DRIVERS = [
    # ---- United States / Canada
    ("drv_us_farm_proprietors_income", "B042RC1Q027SBEA", "United States", "USDbn_saar", "mean",
     "BEA farm proprietors' income w/ IVA and CCAdj, quarterly SAAR; the only "
     "quarterly US farm-income measure -- USDA ERS net farm income is annual only"),
    ("drv_us_corn_price", "PMAIZMTUSDM", "United States", "USD_per_tonne", "mean",
     "IMF global price of corn, monthly, US No.2 Yellow FOB Gulf"),
    ("drv_us_soybean_price", "PSOYBUSDM", "United States", "USD_per_tonne", "mean",
     "IMF global price of soybeans, monthly, CIF Rotterdam"),
    ("drv_us_farm_products_ppi", "WPU01", "United States", "index_1982_100", "mean",
     "BLS PPI farm products -- proxy for US crop receipts per unit"),
    ("drv_us_ag_machinery_ppi", "WPU111", "United States", "index_1982_100", "mean",
     "BLS PPI agricultural machinery and equipment -- Deere's own price realization proxy"),
    ("drv_us_farm_machinery_ppi_mfg", "PCU333111333111", "United States", "index_dec2003_100", "mean",
     "BLS PPI farm machinery and equipment manufacturing"),
    ("drv_us_prime_rate", "MPRIME", "United States", "percent", "mean",
     "Bank prime loan rate -- farm operating-credit cost proxy"),
    ("drv_us_fed_funds", "DFF", "United States", "percent", "mean",
     "Effective federal funds rate, daily, averaged over the fiscal quarter"),
    ("drv_ca_usdcad", "DEXCAUS", "Canada", "CAD_per_USD", "mean",
     "Daily noon USD/CAD averaged over the fiscal quarter; a HIGHER value is a "
     "weaker CAD and a translation headwind to Deere's Canadian revenue"),
    # ---- Western Europe
    ("drv_we_eurusd", "DEXUSEU", "Western Europe", "USD_per_EUR", "mean",
     "Daily USD per EUR averaged over the fiscal quarter; a HIGHER value is a "
     "stronger EUR and a translation TAILWIND to Deere's European revenue"),
    ("drv_we_wheat_price", "PWHEAMTUSDM", "Western Europe", "USD_per_tonne", "mean",
     "IMF global price of wheat, monthly, No.1 Hard Red Winter FOB Gulf"),
    # ---- Central Europe and CIS
    ("drv_ce_wheat_price", "PWHEAMTUSDM", "Central Europe and CIS", "USD_per_tonne", "mean",
     "IMF global wheat price; Black Sea wheat is the dominant CE/CIS crop economic "
     "driver and tracks this benchmark closely. No free quarterly Black Sea "
     "FOB series is available keyless, so this is a PROXY, not the regional price"),
    ("drv_ce_eurusd", "DEXUSEU", "Central Europe and CIS", "USD_per_EUR", "mean",
     "EUR/USD -- much of Central Europe invoices in or pegs to EUR"),
    # ---- Latin America
    ("drv_la_usdbrl", "DEXBZUS", "Latin America", "BRL_per_USD", "mean",
     "Daily BRL per USD averaged over the fiscal quarter; a HIGHER value is a "
     "weaker BRL -- raises the local-currency cost of imported equipment AND is a "
     "translation headwind, but improves Brazilian soy farmers' BRL revenue"),
    ("drv_la_soybean_price", "PSOYBUSDM", "Latin America", "USD_per_tonne", "mean",
     "IMF global soybean price -- Brazil is the world's largest soybean exporter"),
    ("drv_la_corn_price", "PMAIZMTUSDM", "Latin America", "USD_per_tonne", "mean",
     "IMF global corn price -- drives Brazilian safrinha corn economics"),
    ("drv_la_brazil_short_rate", "IRSTCI01BRM156N", "Latin America", "percent", "mean",
     "Brazil immediate interbank rate (SELIC proxy), monthly; sets the cost of "
     "non-subsidised farm credit and caps how far Plano Safra can subsidise"),
    # ---- Asia, Africa, Oceania, Middle East
    ("drv_aaom_usdinr", "DEXINUS", "Asia, Africa, Oceania, and Middle East", "INR_per_USD", "mean",
     "Daily INR per USD averaged over the fiscal quarter; India is the largest "
     "unit-volume market in this geography"),
    ("drv_aaom_wheat_price", "PWHEAMTUSDM", "Asia, Africa, Oceania, and Middle East",
     "USD_per_tonne", "mean",
     "IMF global wheat price -- Australian wheat is the main Oceania driver"),
]


# ---------------------------------------------------- hand-entered points ----
# Every row here carries its own source URL. These are series with no free
# machine-readable feed. They are point observations, not full histories --
# stated as such rather than padded out with guesses.

POINTS = [
    # series_id, fy, fq, geography, value, units, source, notes
    # ---------- AEM US retail units, the single best US large-ag read-through
    ("drv_us_aem_total_tractors_units", 2026, "Q3", "United States", 15985, "units_month",
     "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html",
     "AEM US retail sales, JULY 2026 MONTH ONLY (not the quarter); 17,938 in July 2025, -10.9% YoY"),
    ("drv_us_aem_total_tractors_yoy", 2026, "Q3", "United States", -10.9, "percent_yoy",
     "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html",
     "AEM US total tractor retail units, July 2026 vs July 2025"),
    ("drv_us_aem_4wd_tractors_yoy", 2026, "Q3", "United States", -38.7, "percent_yoy",
     "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html",
     "AEM US four-wheel-drive tractor retail units, July 2026 YoY -- the closest "
     "public proxy for Deere large-ag (PPA) US demand"),
    ("drv_us_aem_2wd_tractors_yoy", 2026, "Q3", "United States", -10.5, "percent_yoy",
     "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html",
     "AEM US two-wheel-drive tractor retail units, July 2026 YoY"),
    ("drv_us_aem_100hp_plus_ytd_yoy", 2026, "Q3", "United States", -15.5, "percent_yoy_ytd",
     "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html",
     "AEM US tractors above 100 horsepower, calendar year to date through July 2026"),
    ("drv_us_aem_combines_ytd_units", 2026, "Q3", "United States", 1676, "units_ytd",
     "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html",
     "AEM US self-propelled combine retail units, calendar YTD through July 2026, -10.2% YoY"),
    ("drv_us_aem_combines_ytd_yoy", 2026, "Q3", "United States", -10.2, "percent_yoy_ytd",
     "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html",
     "AEM US self-propelled combines, calendar YTD through July 2026"),
    ("drv_us_aem_combines_jul_yoy", 2026, "Q3", "United States", -5.3, "percent_yoy",
     "https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html",
     "AEM US self-propelled combine retail units, July 2026 vs July 2025"),
    # ---------- USDA farm income (calendar year, annual only)
    ("drv_us_net_farm_income_cy", 2026, "", "United States", 153.4, "USDbn_cy",
     "https://www.ers.usda.gov/topics/farm-economy/farm-sector-income-finances/highlights-from-the-farm-income-forecast",
     "USDA ERS net farm income forecast for CALENDAR 2026, -$1.2bn (-0.7%) vs 2025. "
     "Annual, not quarterly; fiscal_quarter deliberately blank"),
    ("drv_us_soybean_planted_acres_cy", 2026, "", "United States", 85.0, "million_acres",
     "https://www.profarmer.com/news/agriculture-news/heres-usdas-preliminary-look-2026-corn-soybean-wheat-acres-and-balance-sheets",
     "USDA Ag Outlook Forum Feb 2026 projection for calendar 2026 soybean plantings"),
    ("drv_us_corn_production_cy", 2026, "", "United States", 15.8, "billion_bushels",
     "https://www.profarmer.com/news/agriculture-news/heres-usdas-preliminary-look-2026-corn-soybean-wheat-acres-and-balance-sheets",
     "USDA projected 2026 corn crop at 183 bu/ac, down ~7% from 2025; corn "
     "plantings down ~5 million acres"),
    ("drv_us_soybean_production_cy", 2026, "", "United States", 4.45, "billion_bushels",
     "https://www.profarmer.com/news/agriculture-news/heres-usdas-preliminary-look-2026-corn-soybean-wheat-acres-and-balance-sheets",
     "USDA projected 2026 soybean crop at 53.0 bu/ac"),
    # ---------- Canada
    ("drv_ca_farm_cash_receipts_cy", 2025, "", "Canada", 102.2, "CADbn_cy",
     "https://www150.statcan.gc.ca/n1/daily-quotidien/251126/dq251126c-eng.htm",
     "Statistics Canada farm cash receipts, calendar 2025, +4.7% YoY"),
    ("drv_ca_canola_area_cy", 2026, "", "Canada", 23.4, "million_acres",
     "https://www.fcc-fac.ca/en/knowledge/2026-crop-outlook",
     "Canadian canola planted area 2026, +8.4% YoY"),
    ("drv_ca_canola_production_cy", 2025, "", "Canada", 21.8, "million_tonnes",
     "https://www.fcc-fac.ca/en/knowledge/2026-crop-outlook",
     "Canadian canola production calendar 2025, +13.3% YoY"),
    ("drv_ca_wheat_price_yoy_q1fy26", 2026, "Q2", "Canada", -8.6, "percent_yoy",
     "https://www150.statcan.gc.ca/n1/daily-quotidien/260527/dq260527d-eng.htm",
     "StatCan: Canadian wheat (excl. durum) PRICE change, Jan-Mar 2026 vs Jan-Mar "
     "2025; marketings also -6.0%. Calendar Q1 2026 maps to Deere FY2026 Q2"),
    # ---------- Western Europe
    ("drv_we_cema_business_climate", 2026, "Q3", "Western Europe", -6.0, "index_-100_to_100",
     "https://www.cema-agri.org/market-trends/24-business-barometer/1126-april-2026-business-climate-deteriorating-again",
     "CEMA European ag-machinery business climate index, APRIL 2026 reading, "
     "down from -2; one third of EU manufacturers expect fewer orders over the "
     "next six months. April 2026 sits in Deere FY2026 Q2 but is the most recent "
     "reading available before the Q3 window -- treat as a leading indicator"),
    # ---------- Latin America
    ("drv_la_brazil_soybean_production", 2026, "", "Latin America", 180.6, "million_tonnes",
     "https://www.world-grain.com/articles/22984-brazil-wraps-up-record-soybean-harvest",
     "CONAB: Brazil 2025/26 soybean crop, record, +5% YoY on +2.7% area. Harvested "
     "Jan-May 2026, so the cash lands in Deere FY2026 Q2-Q3"),
    ("drv_la_brazil_corn_production", 2026, "", "Latin America", 141.7, "million_tonnes",
     "https://www.world-grain.com/articles/22984-brazil-wraps-up-record-soybean-harvest",
     "CONAB: Brazil 2025/26 corn across all three harvests, +0.4% YoY"),
    ("drv_la_brazil_total_grain_production", 2026, "", "Latin America", 360.1, "million_tonnes",
     "https://www.world-grain.com/articles/22984-brazil-wraps-up-record-soybean-harvest",
     "CONAB: Brazil total 2025/26 grain output, record, +2.1% YoY"),
    ("drv_la_plano_safra_commercial", 2027, "", "Latin America", 525.1, "BRLbn",
     "https://agenciabrasil.ebc.com.br/en/economia/noticia/2026-07/brazil-launches-brl-5251b-crop-plan-20262027",
     "Plano Safra 2026/27 commercial-agriculture credit envelope, announced JULY "
     "2026 -- i.e. inside the Deere FY2026 Q3 window. Total package >BRL 608bn "
     "including ~BRL 85bn family farming. Labelled fiscal_year 2027 because it "
     "funds the 2026/27 crop year"),
    ("drv_la_plano_safra_costing_rate", 2027, "", "Latin America", 12.5, "percent_per_year",
     "https://www.riotimesonline.com/brazil-plano-safra-2026-27-farm-credit-rates-2026/",
     "Plano Safra 2026/27 headline commercial costing rate, cut from 14.0% in "
     "2025/26. A ~150bp cut in subsidised farm credit is a genuine Q3-window "
     "positive for Brazilian equipment demand"),
    ("drv_la_plano_safra_pronamp_rate", 2027, "", "Latin America", 9.0, "percent_per_year",
     "https://www.riotimesonline.com/brazil-plano-safra-2026-27-farm-credit-rates-2026/",
     "Plano Safra 2026/27 Pronamp (medium producers) maximum rate, cut from 10.0%; "
     "Pronamp envelope ~BRL 72.6bn"),
    ("drv_la_argentina_soybean_export_tax", 2026, "Q3", "Latin America", 15.0, "percent",
     "https://www.fas.usda.gov/data/gain/2026/06/argentina-argentina-further-cuts-agricultural-export-taxes",
     "Argentine soybean export duty (retenciones) cut from 24% to 15% under the "
     "2026 schedule; further 0.25pp monthly cuts from 2027, 0.5pp from 2028"),
    ("drv_la_argentina_corn_export_tax", 2026, "Q3", "Latin America", 8.5, "percent",
     "https://www.fas.usda.gov/data/gain/2026/06/argentina-argentina-further-cuts-agricultural-export-taxes",
     "Argentine corn export duty as of mid-2026; scheduled quarterly cuts of "
     "0.25pp through 2027 to 7.5%, then 0.5pp quarterly to 5.5% by end-2028"),
    ("drv_la_argentina_wheat_export_tax", 2026, "Q3", "Latin America", 5.5, "percent",
     "https://buenosairesherald.com/business/agro/argentina-announces-fresh-cut-to-grains-export-duties",
     "Argentine wheat and barley export duty cut from 7.5% to 5.5% effective June "
     "2026 -- inside the Deere FY2026 Q3 window"),
    # ---------- Asia, Africa, Oceania, Middle East
    ("drv_aaom_india_tractor_retail_units", 2026, "Q3", "Asia, Africa, Oceania, and Middle East",
     117349, "units_month",
     "https://www.whalesbook.com/news/English/auto/India-Tractor-Sales-Surge-28percent-in-July-to-117349-Units/6a783db173b576501a06369a",
     "India tractor sales, JULY 2026 MONTH ONLY, +28.1% YoY. A separate retail-only "
     "count (FADA-style) puts July at 107,329 units, +27.82% YoY -- the two counts "
     "differ in scope, both are reported"),
    ("drv_aaom_india_tractor_retail_yoy", 2026, "Q3", "Asia, Africa, Oceania, and Middle East",
     28.1, "percent_yoy",
     "https://www.whalesbook.com/news/English/auto/India-Tractor-Sales-Surge-28percent-in-July-to-117349-Units/6a783db173b576501a06369a",
     "India tractor market July 2026 YoY; driven by favourable monsoon, recovered "
     "reservoir levels and accelerated kharif sowing"),
    ("drv_aaom_india_mahindra_tractor_units", 2026, "Q3", "Asia, Africa, Oceania, and Middle East",
     32643, "units_month",
     "https://www.mahindra.com/news-room/press-release/en/mahindra-farm-equipment-business-sells-32643-tractors-in-july-2026-registering-a-growth-of-21-percent",
     "Mahindra domestic tractor sales July 2026, +21% YoY vs 26,990. Market-leader "
     "read-through for the Indian small-ag market Deere competes in"),
    ("drv_aaom_australia_winter_crop", 2027, "", "Asia, Africa, Oceania, and Middle East",
     54.5, "million_tonnes",
     "https://www.agriculture.gov.au/abares/research-topics/agricultural-outlook/australian-crop-report/june-2026",
     "ABARES June 2026 crop report: Australian 2026/27 winter crop forecast, -21% "
     "YoY on lower planted area and yields. Wheat specifically forecast down ~26%. "
     "A clear negative for Deere's Oceania ag demand into FY2027"),
    ("drv_aaom_australia_winter_crop_yoy", 2027, "", "Asia, Africa, Oceania, and Middle East",
     -21.0, "percent_yoy",
     "https://www.agriculture.gov.au/abares/research-topics/agricultural-outlook/australian-crop-report/june-2026",
     "ABARES June 2026: Australian 2026/27 winter crop production YoY"),
]


# -------------------------------- Deere's own regional industry outlook ------

OUTLOOK_ROWS = OrderedDict(
    [
        ("Large Ag", ("drv_mgmt_outlook_us_canada_large_ag", "United States")),
        ("Small Ag & Turf", ("drv_mgmt_outlook_us_canada_small_ag_turf", "United States")),
        ("Europe", ("drv_mgmt_outlook_europe_ag", "Western Europe")),
        ("South America (Tractors & Combines)",
         ("drv_mgmt_outlook_south_america_ag", "Latin America")),
        ("Asia", ("drv_mgmt_outlook_asia_ag", "Asia, Africa, Oceania, and Middle East")),
    ]
)

NUMWORD = re.compile(
    r"(down|up|flat)\s*(?:to\s*(down|up)\s*)?~?\s*(\d+)?\s*(?:%|)"
    r"(?:\s*to\s*~?\s*(\d+)\s*%?)?",
    re.I,
)


def parse_outlook_phrase(txt):
    """'Down 15 to 20%' -> -17.5 ; 'Flat to up 5%' -> +2.5 ; 'Up ~10%' -> +10.
    Returns (midpoint_percent, is_truncated) or (None, ...) if unparseable."""
    t = re.sub(r"\s+", " ", txt).strip().lower().replace("~", "")
    t = t.replace("–", "-").replace("—", "-")
    if not t:
        return None, False
    truncated = t.endswith(" to") or t.endswith("-")
    nums = [int(x) for x in re.findall(r"(\d+)", t)]
    # direction words in order of appearance
    dirs = re.findall(r"\b(down|up|flat)\b", t)
    if not dirs:
        return None, truncated
    if dirs == ["flat"] and not nums:
        return 0.0, truncated
    if not nums:
        # e.g. "down moderately" / "down slightly" -- qualitative, no number
        return None, truncated

    def signed(d, v):
        return -v if d == "down" else v

    if len(dirs) == 1:
        d = dirs[0]
        if d == "flat":
            return 0.0, truncated
        vals = [signed(d, n) for n in nums]
        return statistics.fmean(vals), truncated
    # two directions, e.g. "flat to down 5%" / "flat to up 5%" / "down 15 to 20"
    lo_d, hi_d = dirs[0], dirs[1]
    if lo_d == "flat":
        return statistics.fmean([0.0, signed(hi_d, nums[0])]), truncated
    if hi_d == "flat":
        return statistics.fmean([signed(lo_d, nums[0]), 0.0]), truncated
    vals = [signed(lo_d, n) for n in nums]
    return statistics.fmean(vals), truncated


FQ_FROM_NAME = re.compile(r"-(q[1-4])-8k", re.I)
DATE_FROM_NAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})__")


def parse_outlooks():
    """Deere's fiscal-year regional industry unit outlook, as restated at each
    quarterly release. This is management's own regional driver view."""
    d = os.path.join(CORPUS, "filings")
    rows = []
    for fn in sorted(os.listdir(d)):
        if "8k" not in fn:
            continue
        m = DATE_FROM_NAME.match(fn)
        q = FQ_FROM_NAME.search(fn)
        if not (m and q):
            continue
        pub = "%s-%s-%s" % m.groups()
        fq = q.group(1).upper()
        # An 8-K reports the fiscal quarter named in its filename, and Deere's
        # Q4 release lands in November of the SAME calendar year the fiscal year
        # closed in -- so the reporting fiscal year is simply the publication
        # year. The OUTLOOK stated at a Q4 release, however, targets the NEXT
        # fiscal year; at Q1-Q3 it targets the current one.
        py = int(m.group(1))
        fy = py
        target_fy = py + 1 if fq == "Q4" else py
        with open(os.path.join(d, fn), encoding="utf-8") as fh:
            text = fh.read()
        if "Industry Outlook" not in text and "Large Ag" not in text:
            continue
        for line in text.split("\n"):
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            label = re.sub(r"\s+", " ", cells[0]).strip()
            if label not in OUTLOOK_ROWS:
                continue
            vals = [c for c in cells[1:] if c.strip()]
            if not vals:
                continue
            phrase = vals[-1]
            # skip the segment-results tables that reuse these labels
            if re.search(r"\d{3,}", phrase) or "net sales" in label.lower():
                continue
            val, trunc = parse_outlook_phrase(phrase)
            if val is None:
                continue
            sid, geo = OUTLOOK_ROWS[label]
            rows.append(
                (sid, fy, fq, geo, val, "percent_fy_units",
                 "filings/" + fn,
                 'Deere management industry UNIT outlook for FY%d, as stated at '
                 'the FY%d %s release (%s): "%s" -> range midpoint. This is a '
                 'full-year outlook restated each quarter, not a quarterly '
                 'actual%s' % (target_fy, fy, fq, pub, phrase,
                               "; PHRASE TRUNCATED IN SOURCE TABLE" if trunc else ""))
            )
    # keep the last occurrence per (series, fy, fq) -- the outlook table, not a
    # stray earlier match
    dedup = OrderedDict()
    for r in rows:
        dedup[(r[0], r[1], r[2])] = r
    return list(dedup.values())


# ------------------------------------------------------------------- main ---


def main():
    out = []

    # exact fiscal quarter end dates where we know them from the 10-Q matrix
    exact_end = {}
    if os.path.exists(MATRIX):
        with open(MATRIX, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                exact_end[(int(r["fiscal_year"]), r["fiscal_quarter"])] = r["period_end"]

    def pend(fy, fq):
        if not fq:
            return ""
        if (fy, fq) in exact_end:
            return exact_end[(fy, fq)], "exact"
        return nominal_period_end(fy, fq), "nominal"

    # ---- FRED drivers
    for sid, fid, geo, units, how, note in FRED_DRIVERS:
        try:
            obs = fred(fid)
        except Exception as e:
            print("SKIP %s (%s): %s" % (sid, fid, e), file=sys.stderr)
            continue
        q = to_fiscal_quarters(obs, how)
        n_raw = defaultdict(int)
        for d, _ in obs:
            y, m, _x = (int(x) for x in d.split("-"))
            n_raw[fiscal(y, m)] += 1
        for (fy, fq), v in sorted(q.items()):
            if fy < START_FY or fy > 2026:
                continue
            # A quarter built from fewer observations than a full quarter is
            # kept but LOUDLY FLAGGED -- for the FY2026 Q3 forecast window a
            # two-month average is real information, but it is not the quarter.
            n = n_raw[(fy, fq)]
            daily = fid.startswith("DEX") or fid == "DFF"
            if daily:
                if n < 20:
                    continue  # too thin to be a quarter average at all
                partial = n < 50
            elif fid.endswith("SBEA"):
                partial = False  # natively quarterly, one observation
            else:
                partial = n < 3  # monthly series, expect 3 per fiscal quarter
            pe, kind = pend(fy, fq)
            flag = "PARTIAL QUARTER -- " if partial else ""
            out.append(
                [sid, pe, fy, fq, "", geo, "", "%.4f" % v, units, "driver",
                 "FRED:" + fid,
                 flag + note
                 + "; fiscal-quarter %s of %d raw observations%s; period_end=%s"
                 % (how, n,
                    " (incomplete quarter, not comparable to full quarters)"
                    if partial else "",
                    kind)]
            )

    # ---- Deere management regional outlook
    for sid, fy, fq, geo, v, units, src, note in parse_outlooks():
        if fy < START_FY:
            continue
        pe, kind = pend(fy, fq)
        out.append([sid, pe, fy, fq, "", geo, "", "%.4f" % v, units, "driver", src, note])

    # ---- hand-entered point observations
    for sid, fy, fq, geo, v, units, src, note in POINTS:
        if fq:
            pe, kind = pend(fy, fq)
        else:
            pe, kind = "", "n/a"
        out.append([sid, pe, fy, fq, "", geo, "", "%g" % v, units, "driver", src, note])

    out.sort(key=lambda r: (r[0], r[2], r[3]))

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(
            "series_id,period_end,fiscal_year,fiscal_quarter,segment,geography,"
            "product_line,value,units,basis,source,notes".split(",")
        )
        w.writerows(out)

    print("wrote %d rows to %s" % (len(out), OUT_CSV))
    bys = defaultdict(int)
    for r in out:
        bys[(r[5], r[0])] += 1
    for (geo, sid), n in sorted(bys.items()):
        print("  %-40s %-42s %3d" % (geo, sid, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
