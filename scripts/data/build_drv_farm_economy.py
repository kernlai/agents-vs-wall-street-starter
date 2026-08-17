#!/usr/bin/env python3
"""
build_drv_farm_economy.py
=========================
Builds  data/deere/drv_farm_economy.csv  -- a tidy-long panel of US, South American
and EU farm-economy driver series for forecasting Deere & Company (NYSE: DE).

Standard library only.  Network access required on first run; everything is cached
under --cache so re-runs are deterministic and offline.

Sources (all keyless):
  1. USDA ERS  Farm Income and Wealth Statistics  (bulk CSV releases, several vintages)
     https://www.ers.usda.gov/data-products/farm-income-and-wealth-statistics/...
  2. USDA NASS Land Values annual summaries (PDF -> pdftotext -layout -> table parse)
     https://www.nass.usda.gov/Publications/Todays_Reports/reports/landMMYY.pdf
  3. USDA ERS  Feed Grains Yearbook (corn planted/harvested acres, price)
  4. USDA ERS  Oil Crops Yearbook  (soybean planted/harvested acres, price)
  5. USDA FAS  PSD Online bulk CSV (Brazil / Argentina / US corn+soybean area & production)
  6. World Bank API (agriculture value added, BRA/ARG/EUU/USA)
  7. Eurostat  aact_eaa01 (EU agricultural entrepreneurial income & output)
  8. FRED CSV  B042RC1A027NBEA / B042RC1Q027SBEA (BEA farm proprietors' income --
     an INDEPENDENT (Commerce Dept) cross-check on USDA farm income)

Output header (fixed):
  series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes

Conventions
-----------
* All annual rows use fiscal_quarter=FY and period_end = <year>-12-31, even when the
  underlying survey reference date differs (e.g. NASS land values are as-of June 1).
  The real reference date is always stated in `notes`.
* fiscal_year is the CALENDAR year for every series in this file (these are external
  drivers, not Deere fiscal periods).  Deere's FY ends late Oct/early Nov, so Deere
  FY(n) overlaps roughly calendar Nov(n-1)..Oct(n) -- documented in the companion .md.
* Missing data is an ABSENT ROW.  Never zero, never a guess.
* USDA forecast/preliminary years are source_type=estimate.
"""

import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
import urllib.request
import zipfile
from collections import defaultdict

UA = "AgentsVsWallStreet cor@salomo.io"
HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "value",
          "units", "source_type", "source", "notes"]

YEAR_MIN, YEAR_MAX = 2006, 2026

# ERS release currently on the ERS site as of the 2026-08-16 build date.
# ERS publishes 3x/year (Feb, Sep, Dec).  Feb-2026 is the newest available on
# 2026-08-16; the next release (~Sep 2026) had not happened yet.
ERS_VINTAGES = [
    # (vintage tag, url, name inside zip prefix, first forecast year)
    ("2026-02", "https://www.ers.usda.gov/media/20808/february-5-2026-release.zip", 2025),
    ("2025-09", "https://www.ers.usda.gov/media/4866/september-3-2025-release.zip", 2025),
    ("2025-02", "https://www.ers.usda.gov/media/4532/farmincomewealthstatisticsdata2025-02.zip", 2024),
    ("2024-02", "https://www.ers.usda.gov/sites/default/files/images/farmincome_wealthstatisticsdata_february2024.zip", 2023),
]
CURRENT_VINTAGE = "2026-02"

# artificialKey -> (series_id, units, scale, note)
# ERS money variables are published in $1,000; scale 1e-6 converts to USD billions.
K = 1e-6
ERS_SERIES = {
    "FIAUSNTFI--P": ("us_net_farm_income", "USD billions", K,
                     "USDA ERS net farm income, US total, calendar year. Accrual measure."),
    "FIAUSNTCI--P": ("us_net_cash_farm_income", "USD billions", K,
                     "USDA ERS net cash farm income, US total, calendar year. Cash-basis measure."),
    "CRAUSCO--VAP": ("us_crop_cash_receipts", "USD billions", K,
                     "USDA ERS cash receipts, all crops."),
    "CRAUSLV--VAP": ("us_livestock_cash_receipts", "USD billions", K,
                     "USDA ERS cash receipts, livestock and products."),
    "CRAUSAC--VAP": ("us_total_cash_receipts", "USD billions", K,
                     "USDA ERS cash receipts, all commodities (= crops + livestock)."),
    "CRAUSCR--VAP": ("us_corn_cash_receipts", "USD billions", K, "USDA ERS cash receipts, corn."),
    "CRAUSSY--VAP": ("us_soybean_cash_receipts", "USD billions", K, "USDA ERS cash receipts, soybeans."),
    "GPAUSGPTLVAP": ("us_govt_farm_payments", "USD billions", K,
                     "USDA ERS total direct government payments to farms."),
    "GPAUSAE--VAP": ("us_govt_adhoc_emergency_payments", "USD billions", K,
                     "Ad hoc and emergency program payments -- the volatile component of govt payments."),
    "RTAUSSODAEXP": ("us_farm_debt_to_asset_ratio", "percent", 1.0,
                     "USDA ERS farm sector debt-to-asset ratio, excl. operator dwellings. Percent, not a 0-1 ratio."),
    "FAAUSRE--EXP": ("us_farm_real_estate_assets", "USD billions", K,
                     "Dec-31 value of farm real estate assets, excl. operator dwellings. Total-dollar farmland wealth."),
    "FAAUSFA--EXP": ("us_farm_assets_total", "USD billions", K, "Dec-31 value of farm assets, excl. operator dwellings."),
    "FDAUSFD--EXP": ("us_farm_debt_total", "USD billions", K, "Dec-31 value of farm debt, excl. operator dwellings."),
    "FEAUSFE--EXP": ("us_farm_equity_total", "USD billions", K, "Dec-31 value of farm equity, excl. operator dwellings."),
    "EXAUSPE--EXP": ("us_farm_production_expenses", "USD billions", K,
                     "Total farm production expenses, excl. operator dwellings."),
    "EXAUSIN--EXP": ("us_farm_interest_expense", "USD billions", K,
                     "Farm sector interest expense, excl. operator dwellings."),
    "EXAUSIPFL--P": ("us_farm_fertilizer_expense", "USD billions", K,
                     "Fertilizer, lime and soil conditioner expense."),
    "EXAUSCE--EXP": ("us_farm_capital_expenditures", "USD billions", K,
                     "Total farm capital expenditures, excl. operator dwellings."),
    "EXAUSCEVM--P": ("us_farm_capex_vehicles_machinery", "USD billions", K,
                     "Capital expenditures on vehicles and machinery -- closest ERS analogue to Deere's addressable US ag equipment spend."),
    "EXAUSCEVTTRP": ("us_farm_capex_tractors", "USD billions", K,
                     "Capital expenditures on farm tractors. Directly Deere-relevant."),
    "EXAUSCEFM--P": ("us_farm_capex_other_machinery", "USD billions", K,
                     "Capital expenditures on other farm machinery (combines, planters, sprayers etc)."),
    "FIAUSGRCI--P": ("us_gross_cash_farm_income", "USD billions", K, "USDA ERS gross cash farm income."),
    "RTAUSPRRA--P": ("us_farm_rate_of_return_assets", "percent", 1.0,
                     "Total rate of return on farm assets (current income + capital gains)."),
    "RTAUSLIWC--P": ("us_farm_working_capital", "USD billions", K, "Farm sector working capital."),
}

# Vintage tracking is applied only to the two headline income measures.
VINTAGE_KEYS = {
    "FIAUSNTFI--P": "us_net_farm_income",
    "FIAUSNTCI--P": "us_net_cash_farm_income",
}

NASS_LAND_REPORTS = [
    # (file stem, publication date, reference-date note)
    ("land0810", "2010-08-04"), ("land0811", "2011-08-05"), ("land0812", "2012-08-03"),
    ("land0817", "2017-08-03"), ("land0818", "2018-08-03"), ("land0819", "2019-08-06"),
    ("land0820", "2020-08-06"), ("land0821", "2021-08-05"), ("land0822", "2022-08-05"),
    ("land0824", "2024-08-02"), ("land0825", "2025-08-01"), ("land0726", "2026-07-31"),
]
LAND_SERIES = {
    "farm real estate": ("us_farmland_values", "farm real estate (land + buildings)"),
    "cropland": ("us_cropland_values", "cropland"),
    "pasture": ("us_pasture_values", "pasture"),
}

WB_COUNTRIES = {"BRA": "br", "ARG": "ar", "EUU": "eu", "USA": "us"}
WB_INDICATORS = {
    "NV.AGR.TOTL.CD": ("ag_value_added_usd", "USD billions", 1e-9,
                       "World Bank / national accounts: agriculture, forestry and fishing value added, current US$."),
    "NV.AGR.TOTL.ZS": ("ag_value_added_pct_gdp", "percent", 1.0,
                       "Agriculture, forestry and fishing value added as % of GDP."),
    "AG.PRD.CROP.XD": ("crop_production_index", "index", 1.0,
                       "World Bank crop production index (2014-2016 = 100)."),
}

PSD_TARGETS = {
    # (file, commodity description) -> commodity slug
    ("grains", "Corn"): "corn",
    ("oilseeds", "Oilseed, Soybean"): "soybean",
}
PSD_COUNTRIES = {"Brazil": "br", "Argentina": "ar", "United States": "us",
                 "European Union": "eu"}
PSD_ATTRS = {
    "Area Harvested": ("area_harvested", "million hectares", 1e-3),
    "Production": ("production", "million tonnes", 1e-3),
}


# --------------------------------------------------------------------------- utils
def fetch(url, path, binary=True):
    """Download url -> path unless already cached. Returns path."""
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    sys.stderr.write("  fetch %s\n" % url)
    with urllib.request.urlopen(req, timeout=180) as r, open(path, "wb") as f:
        f.write(r.read())
    return path


def num(s):
    s = (s or "").strip().replace(",", "").replace("$", "")
    if s in ("", "(D)", "(X)", "(NA)", "-", "--", "(S)", "(Z)", "NA"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def fmt(v):
    if v is None:
        return ""
    if abs(v - round(v)) < 1e-9 and abs(v) < 1e15:
        return str(int(round(v)))
    return ("%.6f" % v).rstrip("0").rstrip(".")


def row(series_id, year, value, units, source_type, source, notes,
        period_end=None, quarter="FY"):
    return {
        "series_id": series_id,
        "period_end": period_end or ("%d-12-31" % year),
        "fiscal_year": year,
        "fiscal_quarter": quarter,
        "value": fmt(value),
        "units": units,
        "source_type": source_type,
        "source": source,
        "notes": notes,
    }


# --------------------------------------------------------------------------- 1. ERS
def ers_extract(cache):
    """Returns (rows, raw) where raw[(vintage, key, year)] = value in native units."""
    rows = []
    raw = {}
    for tag, url, first_fcst in ERS_VINTAGES:
        zp = os.path.join(cache, "ers", "ers_%s.zip" % tag)
        fetch(url, zp)
        with zipfile.ZipFile(zp) as z:
            name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
            with z.open(name) as fh:
                text = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
                rdr = csv.DictReader(text)
                for r in rdr:
                    if r.get("State") != "US":
                        continue
                    key = r.get("artificialKey")
                    if key not in ERS_SERIES:
                        continue
                    try:
                        y = int(r["Year"])
                    except (TypeError, ValueError):
                        continue
                    if not (YEAR_MIN <= y <= YEAR_MAX):
                        continue
                    v = num(r.get("Amount"))
                    if v is None:
                        continue
                    raw[(tag, key, y)] = v

        pub = {"2026-02": "February 5, 2026", "2025-09": "September 3, 2025",
               "2025-02": "February 6, 2025", "2024-02": "February 7, 2024"}[tag]

        if tag == CURRENT_VINTAGE:
            for key, (sid, units, scale, note) in ERS_SERIES.items():
                for y in range(YEAR_MIN, YEAR_MAX + 1):
                    v = raw.get((tag, key, y))
                    if v is None:
                        continue
                    est = y >= first_fcst
                    n = note
                    if est:
                        n += (" USDA FORECAST/preliminary as of %s -- not an actual. "
                              "%d is the current-year forecast." % (pub, YEAR_MAX)) \
                             if y == YEAR_MAX else \
                             (" USDA preliminary estimate as of %s; still subject to "
                              "large revision (see vintage series)." % pub)
                    rows.append(row(sid, y, v * scale, units,
                                    "estimate" if est else "api", url, n))
        # vintage series for the two headline measures
        for key, base in VINTAGE_KEYS.items():
            for y in range(YEAR_MIN, YEAR_MAX + 1):
                v = raw.get((tag, key, y))
                if v is None or y < first_fcst:
                    continue
                sid = "%s_fcst_v%s" % (base, tag.replace("-", "_"))
                rows.append(row(sid, y, v * K, "USD billions", "estimate", url,
                                "Forecast VINTAGE: what USDA ERS published for %d in the "
                                "%s release. Use with the same-year value in %s to measure "
                                "USDA forecast revision behaviour." % (y, pub, base)))
    return rows, raw


# --------------------------------------------------------------------- 2. NASS land
CHART_KINDS = {r"Farm\s+Real\s+Estate\s+Value": "us_farmland_values",
               r"Cropland\s+Value": "us_cropland_values",
               r"Pasture\s+Value": "us_pasture_values"}


def _parse_land_charts(lines):
    """
    Each NASS Land Values summary opens with a 15-year US trend chart whose data
    labels are printed on the page.  Those charts carry NASS's CURRENT (revised)
    history, whereas the 5-year regional tables later in the same PDF are frozen
    at the values published in the covering years.  The 2012 Census of Agriculture
    benchmarking revised the pre-2013 series materially (e.g. 2012 farm real estate
    2,650 -> 2,520 USD/acre), so the charts are the correct primary source.

    Layout trick: pdftotext -layout preserves horizontal position, so sorting the
    data labels by column reproduces year order.  The x-axis line (>=5 consecutive
    years) supplies the year vector and the left cut-off that excludes y-axis labels.
    """
    out = {}
    for i, ln in enumerate(lines):
        if "...." in ln:                       # table of contents
            continue
        sid = None
        for pat, s in CHART_KINDS.items():
            if re.search(r"Average\s+" + pat + r"\s*[-–—]\s*United\s+States", ln):
                sid = s
                break
        if sid is None or sid in out:
            continue
        blk = lines[i + 1:i + 34]
        axis = None
        for j, b in enumerate(blk):
            toks = [(m.start(), int(m.group())) for m in re.finditer(r"\b(?:19|20)\d{2}\b", b)]
            if len(toks) >= 5 and all(toks[k + 1][1] - toks[k][1] == 1
                                      for k in range(len(toks) - 1)):
                axis = (j, toks)
                break
        if not axis:
            continue
        j, toks = axis
        years = [t[1] for t in toks]
        c0 = toks[0][0]
        pts = []
        for b in blk[:j]:
            for m in re.finditer(r"\b\d{1,2},\d{3}\b|\b\d{3,5}\b", b):
                if m.start() < c0 - 4:          # y-axis scale labels
                    continue
                pts.append((m.start(), int(m.group().replace(",", ""))))
        pts.sort()
        if len(pts) == len(years):              # refuse to guess on any mismatch
            out[sid] = dict(zip(years, [p[1] for p in pts]))
    return out


def nass_land_extract(cache):
    chart_best = {}     # (sid, year) -> (pubdate, value, stem)
    table_best = {}     # (sid, year) -> (pubdate, value, stem)
    all_obs = []        # (sid, year, value, stem, 'chart'|'table') for validation
    hdr_re = re.compile(
        r"(Farm Real Estate|Cropland|Pasture)[ ,]*Average Value per Acre.*?"
        r"(\d{4})\s*[-–—]\s*(\d{4})", re.I)

    for stem, pubdate in NASS_LAND_REPORTS:
        url = "https://www.nass.usda.gov/Publications/Todays_Reports/reports/%s.pdf" % stem
        pdf = os.path.join(cache, "lv", "%s.pdf" % stem)
        fetch(url, pdf)
        txt = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                             capture_output=True, text=True, check=True).stdout
        lines = txt.splitlines()

        # ---- charts (primary)
        for sid, series in _parse_land_charts(lines).items():
            for y, v in series.items():
                if not (YEAR_MIN <= y <= YEAR_MAX):
                    continue
                all_obs.append((sid, y, float(v), stem, "chart"))
                prev = chart_best.get((sid, y))
                if prev is None or pubdate > prev[0]:
                    chart_best[(sid, y)] = (pubdate, float(v), stem)

        # ---- 5-year regional tables (cross-check / fallback)
        i = 0
        while i < len(lines):
            ln = lines[i]
            m = hdr_re.search(ln)
            if not m or "...." in ln or "Irrigated" in ln:
                i += 1
                continue
            kind = m.group(1).lower()
            y0, y1 = int(m.group(2)), int(m.group(3))
            if kind not in LAND_SERIES or y1 - y0 != 4:
                i += 1
                continue
            sid = LAND_SERIES[kind][0]
            # NASS labelled the national total "48 States" through the 2010
            # summary and "United States" from 2011; both exclude AK and HI.
            for j in range(i + 1, min(i + 130, len(lines))):
                s = lines[j].strip()
                if not (s.startswith("United States") or s.startswith("48 States")):
                    continue
                vals = [num(t) for t in re.findall(r"[\d,]+(?:\.\d+)?", s.split("...")[-1])]
                vals = [v for v in vals if v is not None and v >= 100][:5]
                if len(vals) < 5:
                    continue
                for off, v in enumerate(vals):
                    y = y0 + off
                    if not (YEAR_MIN <= y <= YEAR_MAX):
                        continue
                    all_obs.append((sid, y, v, stem, "table"))
                    prev = table_best.get((sid, y))
                    if prev is None or pubdate > prev[0]:
                        table_best[(sid, y)] = (pubdate, v, stem)
                break
            i += 1

    label_by_sid = {v[0]: v[1] for v in LAND_SERIES.values()}
    rows = []
    for key in sorted(set(chart_best) | set(table_best)):
        sid, y = key
        if key in chart_best:
            pubdate, v, stem = chart_best[key]
            origin = ("Taken from the US trend chart of the newest summary covering this "
                      "year, which carries NASS's revised history; the frozen 5-year "
                      "regional tables in older summaries can be up to ~5 percent higher "
                      "for pre-2013 years because of 2012-Census benchmarking.")
        else:
            pubdate, v, stem = table_best[key]
            origin = ("Taken from the 5-year regional table (no parseable trend chart "
                      "covers this year). May predate later NASS revisions.")
        refnote = ("Survey reference date January 1 of the year (NASS moved the reference "
                   "date to June 1 from the 2011 summary onward -- a definition change, "
                   "not a data error)." if y <= 2010 else
                   "Survey reference date June 1 of the year.")
        rows.append(row(sid, y, v, "USD/acre", "api",
                        "https://www.nass.usda.gov/Publications/Todays_Reports/reports/%s.pdf" % stem,
                        "USDA NASS Land Values summary, US average %s value per acre. "
                        "%s %s Published %s. period_end set to Dec-31 for panel consistency."
                        % (label_by_sid[sid], refnote, origin, pubdate)))
    return rows, all_obs


# ------------------------------------------------------- 3/4. ERS crop yearbooks
def crop_acreage_extract(cache):
    rows = []
    xchk = {}
    fg = fetch("https://www.ers.usda.gov/media/5766/feed-grains-yearbook-tables-all-years.csv?v=71123",
               os.path.join(cache, "feedgrains.csv"))
    oc = fetch("https://www.ers.usda.gov/media/5218/all-tables-oil-crops-yearbook.csv?v=24957",
               os.path.join(cache, "oilcrops.csv"))

    # --- corn (Million acres, marketing year Sep-Aug; 'year' = crop/plant year)
    corn_map = {"Area planted": ("us_planted_acres_corn", "planted"),
                "Area harvested for grain": ("us_harvested_acres_corn", "harvested for grain")}
    with open(fg, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            if r["commodity"] != "Corn" or r["geography"] != "United States":
                continue
            if r["frequency"] != "Annual" or r["unit"] != "Million acres":
                continue
            a = r["attribute"]
            if a not in corn_map:
                continue
            y = int(r["year"])
            if not (YEAR_MIN <= y <= YEAR_MAX):
                continue
            v = num(r["amount"])
            if v is None:
                continue
            sid, lab = corn_map[a]
            rows.append(row(sid, y, v, "million acres", "api",
                            "https://www.ers.usda.gov/data-products/feed-grains-database/feed-grains-yearbook-tables",
                            "USDA ERS Feed Grains Yearbook Table 1: US corn area %s, crop year %d. "
                            "Acreage is decided in Feb-Apr and is the strongest single-season "
                            "signal for large-row-crop equipment demand." % (lab, y)))
            xchk[(sid, y)] = v

    # --- soybeans (Thousand acres -> million acres)
    soy_map = {"Planted acres": ("us_planted_acres_soybean", "planted"),
               "Harvested acres": ("us_harvested_acres_soybean", "harvested")}
    with open(oc, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            if r["Commodity_Desc"] != "Soybeans" or r["Geography_Desc"] != "United States":
                continue
            if r["Unit_Desc"] != "Thousand acres":
                continue
            a = r["Attribute_Desc"]
            if a not in soy_map:
                continue
            my = r["Marketing_Year"]           # e.g. "2024/25"
            m = re.match(r"^(\d{4})", my or "")
            if not m:
                continue
            y = int(m.group(1))
            if not (YEAR_MIN <= y <= YEAR_MAX):
                continue
            v = num(r["Amount"])
            if v is None:
                continue
            sid, lab = soy_map[a]
            rows.append(row(sid, y, v / 1000.0, "million acres", "api",
                            "https://www.ers.usda.gov/data-products/oil-crops-yearbook",
                            "USDA ERS Oil Crops Yearbook: US soybean acres %s, marketing year %s "
                            "(labelled by the planting year). Converted from thousand acres."
                            % (lab, my)))
            xchk[(sid, y)] = v / 1000.0

    # --- season-average farm prices (drive cash receipts)
    with open(fg, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            if (r["commodity"] == "Corn" and r["geography"] == "United States"
                    and r["frequency"] == "Annual"
                    and r["attribute"] == "Price received by farmers"
                    and r["unit"] == "Dollars per bushel"):
                y = int(r["year"])
                v = num(r["amount"])
                if YEAR_MIN <= y <= YEAR_MAX and v is not None:
                    rows.append(row("us_corn_price_received", y, v, "USD/bushel", "api",
                                    "https://www.ers.usda.gov/data-products/feed-grains-database/feed-grains-yearbook-tables",
                                    "US season-average corn price received by farmers, marketing "
                                    "year Sep-Aug beginning in %d." % y))
    with open(oc, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            if (r["Commodity_Desc"] == "Soybeans" and r["Geography_Desc"] == "United States"
                    and r["Attribute_Desc"] == "Season-average price received by farmers"
                    and r["Unit_Desc"] == "Dollars/bushel"):
                m = re.match(r"^(\d{4})", r["Marketing_Year"] or "")
                v = num(r["Amount"])
                if m and v is not None and YEAR_MIN <= int(m.group(1)) <= YEAR_MAX:
                    rows.append(row("us_soybean_price_received", int(m.group(1)), v,
                                    "USD/bushel", "api",
                                    "https://www.ers.usda.gov/data-products/oil-crops-yearbook",
                                    "US season-average soybean price received by farmers, "
                                    "marketing year %s." % r["Marketing_Year"]))
    return rows, xchk


# -------------------------------------------------------------------- 5. FAS PSD
def psd_extract(cache):
    rows = []
    xchk = {}
    urls = {"grains": "https://apps.fas.usda.gov/psdonline/downloads/psd_grains_pulses_csv.zip",
            "oilseeds": "https://apps.fas.usda.gov/psdonline/downloads/psd_oilseeds_csv.zip"}
    for tag, url in urls.items():
        zp = fetch(url, os.path.join(cache, "psd_%s.zip" % tag))
        with zipfile.ZipFile(zp) as z:
            name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
            with z.open(name) as fh:
                text = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
                for r in csv.DictReader(text):
                    key = (tag, r["Commodity_Description"])
                    if key not in PSD_TARGETS:
                        continue
                    ctry = PSD_COUNTRIES.get(r["Country_Name"])
                    if not ctry:
                        continue
                    attr = PSD_ATTRS.get(r["Attribute_Description"])
                    if not attr:
                        continue
                    try:
                        y = int(r["Market_Year"])
                    except (TypeError, ValueError):
                        continue
                    if not (YEAR_MIN <= y <= YEAR_MAX):
                        continue
                    v = num(r["Value"])
                    if v is None:
                        continue
                    crop = PSD_TARGETS[key]
                    aslug, units, scale = attr
                    sid = "%s_%s_%s" % (ctry, crop, aslug)
                    sa_note = ("Southern-hemisphere crop: market year %d/%d is planted "
                               "Sep-Dec %d and harvested Jan-Jun %d, i.e. it lands in "
                               "Deere fiscal Q1-Q3 of FY%d. " % (y, (y + 1) % 100, y, y + 1, y + 1)
                               if ctry in ("br", "ar") else "")
                    rows.append(row(sid, y, v * scale, units, "api", url,
                                    "USDA FAS PSD Online (bulk CSV, Aug-2026 vintage): %s %s %s, "
                                    "market year %d/%d. %sLater market years are USDA forecasts."
                                    % (r["Country_Name"], crop, aslug.replace("_", " "),
                                       y, (y + 1) % 100, sa_note)))
                    xchk[(sid, y)] = v * scale
    return rows, xchk


# ----------------------------------------------------------------- 6. World Bank
def worldbank_extract(cache):
    rows = []
    for ind, (slug, units, scale, note) in WB_INDICATORS.items():
        url = ("https://api.worldbank.org/v2/country/%s/indicator/%s?format=json"
               "&per_page=2000&date=%d:%d" % (";".join(WB_COUNTRIES), ind, YEAR_MIN, YEAR_MAX))
        p = fetch(url, os.path.join(cache, "wb_%s.json" % ind.replace(".", "_")))
        with open(p, encoding="utf-8") as f:
            doc = json.load(f)
        if not isinstance(doc, list) or len(doc) < 2 or doc[1] is None:
            continue
        for rec in doc[1]:
            iso = rec.get("countryiso3code")
            pre = WB_COUNTRIES.get(iso)
            if not pre or rec.get("value") is None:
                continue
            y = int(rec["date"])
            rows.append(row("%s_%s" % (pre, slug), y, rec["value"] * scale, units, "api", url,
                            "%s Country=%s. EUU=European Union aggregate. World Bank data lag "
                            "1-2 years, so recent years may be absent." % (note, iso)))
    return rows


# -------------------------------------------------------------------- 7. Eurostat
def eurostat_extract(cache):
    rows = []
    items = {"AM370000": ("eu_ag_entrepreneurial_income", "Net entrepreneurial income of the EU "
                          "agricultural industry -- the EU analogue of US net farm income."),
             "AM180000": ("eu_ag_output", "Output of the EU agricultural 'industry' at basic prices."),
             "AM320000": ("eu_ag_factor_income", "EU agricultural factor income.")}
    for code, (sid, note) in items.items():
        url = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/aact_eaa01"
               "?format=JSON&lang=EN&geo=EU27_2020&unit=MIO_EUR&indic_agr=PRD_BP&am_item=%s" % code)
        try:
            p = fetch(url, os.path.join(cache, "eurostat_%s.json" % code))
            with open(p, encoding="utf-8") as f:
                doc = json.load(f)
            tidx = doc["dimension"]["time"]["category"]["index"]
            vals = doc["value"]
            size = doc["size"]
            n_time = size[doc["id"].index("time")]
            for tlabel, ti in tidx.items():
                y = int(tlabel)
                if not (YEAR_MIN <= y <= YEAR_MAX):
                    continue
                # all other dims are length-1 so the flat index == time index
                v = vals.get(str(ti)) if isinstance(vals, dict) else None
                if v is None:
                    continue
                rows.append(row(sid, y, v, "EUR millions", "api", url,
                                "%s Eurostat aact_eaa01, geo=EU27_2020, current prices." % note))
            assert n_time >= 1
        except Exception as e:                      # noqa: BLE001 - source is best-effort
            sys.stderr.write("  WARN eurostat %s failed: %s\n" % (code, e))
    return rows


# ------------------------------------------------------------------------ 8. FRED
def fred_extract(cache):
    rows, annual = [], {}
    # annual
    url_a = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=B042RC1A027NBEA"
    p = fetch(url_a, os.path.join(cache, "fred_B042RC1A027NBEA.csv"))
    with open(p, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            d = r["observation_date"]
            v = num(list(r.values())[1])
            y = int(d[:4])
            if v is None or not (YEAR_MIN <= y <= YEAR_MAX):
                continue
            annual[y] = v
            rows.append(row("us_farm_proprietors_income_bea", y, v, "USD billions", "api", url_a,
                            "BEA (Dept of Commerce) farm proprietors' income with IVA and CCAdj, "
                            "NIPA basis. INDEPENDENT of USDA. Level differs from USDA net farm "
                            "income by definition (BEA excludes corporate farms and uses different "
                            "imputations) -- use for direction/turning points, not levels."))
    # quarterly (SAAR) -- the only quarterly farm-income indicator available
    url_q = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=B042RC1Q027SBEA"
    p = fetch(url_q, os.path.join(cache, "fred_B042RC1Q027SBEA.csv"))
    qend = {1: ("03-31", "Q1"), 4: ("06-30", "Q2"), 7: ("09-30", "Q3"), 10: ("12-31", "Q4")}
    with open(p, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            d = r["observation_date"]
            v = num(list(r.values())[1])
            y, m = int(d[:4]), int(d[5:7])
            if v is None or not (YEAR_MIN <= y <= YEAR_MAX) or m not in qend:
                continue
            suf, q = qend[m]
            rows.append(row("us_farm_proprietors_income_bea_q", y, v, "USD billions", "api", url_q,
                            "BEA farm proprietors' income, QUARTERLY, seasonally adjusted annual "
                            "rate. Calendar quarter. Deere's fiscal quarters end ~late Jan / early "
                            "May / early Aug / late Oct, so lag/lead this against Deere quarters "
                            "rather than matching Q labels.",
                            period_end="%d-%s" % (y, suf), quarter=q))
    # BRL and ARS -- Brazilian/Argentine farmer purchasing power for USD-priced equipment
    for fid, sid, note in [
        ("DEXBZUS", "brl_usd_fx_rate", "Brazilian reais per USD, daily -> calendar-year average. "
                                       "A weaker BRL raises the local-currency cost of imported "
                                       "equipment but also raises soybean revenue in BRL."),
    ]:
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s" % fid
        try:
            p = fetch(url, os.path.join(cache, "fred_%s.csv" % fid))
            buckets = defaultdict(list)
            with open(p, encoding="utf-8", errors="replace") as f:
                for r in csv.DictReader(f):
                    d = r["observation_date"]
                    v = num(list(r.values())[1])
                    if v is None:
                        continue
                    y = int(d[:4])
                    if YEAR_MIN <= y <= YEAR_MAX:
                        buckets[y].append(v)
            for y in sorted(buckets):
                partial = " Partial year: average of observations through the 2026-08 data cut." \
                    if y == YEAR_MAX else ""
                rows.append(row(sid, y, sum(buckets[y]) / len(buckets[y]), "ratio", "api", url,
                                note + partial))
        except Exception as e:                      # noqa: BLE001
            sys.stderr.write("  WARN fred %s failed: %s\n" % (fid, e))
    return rows, annual


# --------------------------------------------------------------------- validation
def _corr(pairs):
    n = len(pairs)
    if n < 5:
        return None
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pairs)
    sxx = sum((p[0] - mx) ** 2 for p in pairs)
    syy = sum((p[1] - my) ** 2 for p in pairs)
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / (sxx * syy) ** 0.5


def validate(ers_raw, land_obs, crop_x, psd_x, bea_annual, all_rows):
    out = []
    byser = defaultdict(dict)
    for r in all_rows:
        if r["value"] != "":
            byser[r["series_id"]][int(r["fiscal_year"])] = float(r["value"])

    def add(name, a, b, la, lb, tol_pct):
        if a is None or b is None:
            out.append("SKIP  %-52s (missing input)" % name)
            return
        d = abs(a - b) / abs(b) * 100 if b else float("inf")
        out.append("%-5s %-52s %s=%.4g  %s=%.4g  diff=%.2f%%"
                   % ("OK" if d <= tol_pct else "FLAG", name, la, a, lb, b, d))

    # 1-2. corn acreage: ERS Feed Grains vs USDA FAS PSD (different USDA agencies/systems,
    #      but note both ultimately trace back to NASS/WAOB -- see companion .md)
    for y in (2023, 2024, 2025, 2026):
        ers_h = crop_x.get(("us_harvested_acres_corn", y))
        psd_h = psd_x.get(("us_corn_area_harvested", y))
        add("US corn harvested acres %d  ERS-FeedGrains vs FAS-PSD" % y,
            ers_h, (psd_h * 1000 * 2.4710538) / 1000 if psd_h else None,
            "ERS(Macre)", "PSD(Macre)", 1.5)
    # 3. soybean acreage cross-check
    for y in (2023, 2024, 2025):
        ers_h = crop_x.get(("us_harvested_acres_soybean", y))
        psd_h = psd_x.get(("us_soybean_area_harvested", y))
        add("US soybean harvested acres %d  ERS-OilCrops vs FAS-PSD" % y,
            ers_h, (psd_h * 2.4710538) if psd_h else None, "ERS(Macre)", "PSD(Macre)", 1.5)
    # 4a. NASS land values: same year read from the CHART of two different annual
    #     summaries -- these should agree exactly once NASS has settled a year.
    charts = defaultdict(dict)
    tables = defaultdict(dict)
    for sid, y, v, stem, kind in land_obs:
        (charts if kind == "chart" else tables)[(sid, y)][stem] = v
    disagree = []
    npairs = 0
    for (sid, y), d in sorted(charts.items()):
        if len(d) < 2:
            continue
        npairs += 1
        smin = min(d, key=lambda s: d[s])
        smax = max(d, key=lambda s: d[s])
        if d[smax] != d[smin]:
            disagree.append((abs(d[smax] - d[smin]) / d[smin] * 100, sid, y,
                             smin, smax, d[smin], d[smax]))
    out.append("INFO  %-52s %d year-values appear in >=2 summaries' charts; %d differ "
               "(all are NASS revisions -- newest chart is used)"
               % ("NASS chart-vs-chart across separate summaries", npairs, len(disagree)))
    for pct, sid, y, s0, s1, a, b in sorted(disagree, reverse=True)[:3]:
        add("%s %d  chart(%s) vs chart(%s)" % (sid, y, s0, s1), a, b, s0, s1, 1.0)
    same = npairs - len(disagree)
    out.append("OK    %-52s %d of %d chart year-values agree EXACTLY across summaries"
               % ("NASS chart reproducibility", same, npairs))
    # 4b. chart (revised) vs 5-year table (as-published) -- quantifies NASS revisions
    revs = []
    for (sid, y), d in sorted(tables.items()):
        c = charts.get((sid, y))
        if not c:
            continue
        newest_tbl = d[sorted(d)[-1]]
        newest_cht = c[sorted(c)[-1]]
        if newest_tbl != newest_cht:
            revs.append((abs(newest_tbl - newest_cht) / newest_cht * 100, sid, y,
                         newest_tbl, newest_cht))
    out.append("INFO  %-52s %d of %d year-values revised by NASS after first publication"
               % ("NASS revised-chart vs as-published-table", len(revs), len(tables)))
    for pct, sid, y, t, c in sorted(revs, reverse=True)[:3]:
        out.append("INFO  %-52s table=%.0f chart=%.0f  revision=%.2f%% (chart used)"
                   % ("%s %d NASS revision" % (sid, y), t, c, pct))
    # 5. ERS internal identity: crops + livestock == all commodities
    for y in (2015, 2020, 2024):
        c = ers_raw.get((CURRENT_VINTAGE, "CRAUSCO--VAP", y))
        l = ers_raw.get((CURRENT_VINTAGE, "CRAUSLV--VAP", y))
        t = ers_raw.get((CURRENT_VINTAGE, "CRAUSAC--VAP", y))
        add("ERS identity %d crops+livestock vs all commodities" % y,
            (c + l) if (c and l) else None, t, "sum", "reported", 0.5)
    # 6. ERS vs BEA (genuinely independent agency) -- direction of YoY change
    for y in (2023, 2024, 2025):
        u0 = ers_raw.get((CURRENT_VINTAGE, "FIAUSNTFI--P", y - 1))
        u1 = ers_raw.get((CURRENT_VINTAGE, "FIAUSNTFI--P", y))
        b0, b1 = bea_annual.get(y - 1), bea_annual.get(y)
        if all(x is not None for x in (u0, u1, b0, b1)):
            du, db = (u1 / u0 - 1) * 100, (b1 / b0 - 1) * 100
            same = (du > 0) == (db > 0)
            out.append("%-5s %-52s USDA=%+.1f%%  BEA=%+.1f%%  (independent agencies)"
                       % ("OK" if same else "FLAG",
                          "US farm income YoY sign %d USDA-ERS vs BEA" % y, du, db))
    # 7. Cross-source correlation checks between genuinely different data producers
    for a_sid, b_sid, label in [
        ("br_soybean_production", "br_crop_production_index",
         "Brazil: FAS-PSD soybean output vs World Bank crop index"),
        ("eu_ag_output", "eu_ag_value_added_usd",
         "EU: Eurostat ag output (EUR) vs World Bank ag value added (USD)"),
        ("us_net_farm_income", "us_farm_proprietors_income_bea",
         "US: USDA-ERS net farm income vs BEA farm proprietors' income"),
        ("us_net_farm_income", "us_farm_capex_vehicles_machinery",
         "US: net farm income vs farm machinery capex (driver plausibility)"),
        ("us_farmland_values", "us_farm_real_estate_assets",
         "US: NASS farmland $/acre vs ERS farm real estate assets"),
    ]:
        yrs = sorted(set(byser.get(a_sid, {})) & set(byser.get(b_sid, {})))
        pairs = [(byser[a_sid][y], byser[b_sid][y]) for y in yrs]
        c = _corr(pairs)
        out.append("%-5s %-52s r=%s over n=%d (%s)"
                   % ("OK" if (c is not None and c > 0.5) else
                      ("FLAG" if c is not None else "SKIP"),
                      label, ("%.3f" % c) if c is not None else "n/a", len(pairs),
                      "%d-%d" % (yrs[0], yrs[-1]) if yrs else "-"))

    # 8. CORPUS cross-check.  Deere's own Q1 FY2026 earnings call (2026-02-19) reads the
    #    same USDA Feb-2026 release out loud.  The corpus is authoritative, so this is
    #    the single strongest validation of the headline forecast numbers.
    def pct(sid, y0, y1):
        a, b = byser.get(sid, {}).get(y0), byser.get(sid, {}).get(y1)
        return None if (a in (None, 0) or b is None) else (b / a - 1) * 100

    for sid, y0, y1, claim, lo, hi in [
        ("us_net_cash_farm_income", 2025, 2026,
         "Deere Q1FY26 call: 2026 US net cash farm income 'up around 3%'", 2.0, 4.0),
        ("us_govt_farm_payments", 2025, 2026,
         "Deere Q1FY26 call: increase 'driven by more government payments'", 5.0, 1e9),
        ("us_crop_cash_receipts", 2025, 2026,
         "Deere Q1FY26 call: crop cash receipts 'up slightly'", 0.0, 5.0),
    ]:
        p = pct(sid, y0, y1)
        out.append("%-5s %-52s extracted=%+.2f%%  (expected %s)"
                   % ("OK" if (p is not None and lo <= p <= hi) else "FLAG",
                      claim[:52], p if p is not None else float("nan"),
                      "%.0f..%.0f%%" % (lo, min(hi, 999))))

    # 9. ERS vintage revision magnitudes (informational, always reported)
    for y in (2024, 2025):
        vals = [(t, ers_raw.get((t, "FIAUSNTFI--P", y)) )
                for t, _, _ in ERS_VINTAGES]
        vals = [(t, v * K) for t, v in vals if v is not None]
        if len(vals) >= 2:
            lo, hi = min(v for _, v in vals), max(v for _, v in vals)
            out.append("INFO  %-52s vintages %s  spread=%.1f%%"
                       % ("US net farm income %d forecast revisions" % y,
                          ", ".join("%s=%.1f" % (t, v) for t, v in vals),
                          (hi - lo) / lo * 100))
    return out


# ------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    default_cache = os.path.expanduser("~/.cache/avws-farm-economy")
    ap.add_argument("--cache", default=default_cache)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..",
        "data", "deere", "drv_farm_economy.csv"))
    a = ap.parse_args()
    cache = os.path.abspath(a.cache)
    os.makedirs(cache, exist_ok=True)

    rows = []
    sys.stderr.write("[1/7] USDA ERS farm income and wealth statistics\n")
    r, ers_raw = ers_extract(cache); rows += r
    sys.stderr.write("[2/7] USDA NASS land values\n")
    r, land_obs = nass_land_extract(cache); rows += r
    sys.stderr.write("[3/7] USDA ERS crop yearbooks (acreage, prices)\n")
    r, crop_x = crop_acreage_extract(cache); rows += r
    sys.stderr.write("[4/7] USDA FAS PSD (Brazil / Argentina / US)\n")
    r, psd_x = psd_extract(cache); rows += r
    sys.stderr.write("[5/7] World Bank\n")
    rows += worldbank_extract(cache)
    sys.stderr.write("[6/7] Eurostat\n")
    rows += eurostat_extract(cache)
    sys.stderr.write("[7/7] FRED / BEA\n")
    r, bea_annual = fred_extract(cache); rows += r

    # de-duplicate on (series_id, period_end) keeping the first occurrence
    seen, dedup, dups = set(), [], 0
    for r in rows:
        k = (r["series_id"], r["period_end"])
        if k in seen:
            dups += 1
            continue
        seen.add(k)
        dedup.append(r)
    rows = sorted(dedup, key=lambda r: (r["series_id"], r["period_end"]))

    out = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    sids = sorted({r["series_id"] for r in rows})
    sys.stderr.write("\nwrote %s  rows=%d series=%d (dropped %d dupes)\n"
                     % (out, len(rows), len(sids), dups))

    print("\n===== SERIES INVENTORY =====")
    agg = defaultdict(list)
    for r in rows:
        agg[r["series_id"]].append(r)
    for sid in sids:
        rs = sorted(agg[sid], key=lambda x: x["period_end"])
        print("%-42s n=%-4d %s .. %s  %s"
              % (sid, len(rs), rs[0]["period_end"], rs[-1]["period_end"], rs[0]["units"]))

    print("\n===== VALIDATION =====")
    for line in validate(ers_raw, land_obs, crop_x, psd_x, bea_annual, rows):
        print(line)


if __name__ == "__main__":
    main()
