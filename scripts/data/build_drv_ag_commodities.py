#!/usr/bin/env python3
"""
Build 20 years (2006-2026) of agricultural commodity price and crop-input-cost
drivers for Deere & Company (NYSE: DE) forecasting, at quarterly frequency,
aligned BOTH to calendar quarters (_cq) and to Deere's fiscal quarters (_fq).

Standard library only. Network sources (all keyless):
  * FRED CSV download    https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>
      - IMF global commodity price series (monthly) - PRIMARY price source
      - BLS PPI fertiliser / diesel indices (monthly)
      - EIA retail diesel (weekly), WTI (daily)
  * World Bank "Pink Sheet" CMO-Historical-Data-Monthly.xlsx  - CROSS-CHECK
      source + the only USD/mt fertiliser levels (urea, potash, DAP, TSP,
      phosphate rock). Parsed from the raw xlsx with zipfile + ElementTree.
  * SEC EDGAR XBRL companyconcept (CIK 315189) - used ONLY to derive Deere's
      exact fiscal period boundaries (see FISCAL_QUARTER_ENDS below, which was
      produced from that API and cross-checked against the offline filings
      corpus).

NOT used: stooq.com. Its CSV endpoint is behind a JavaScript proof-of-work
bot check; solving it would be circumventing bot detection, so it was skipped.
NOT used: USDA NASS QuickStats. Its API returned {"error":["unauthorized"]} -
it requires an API key which is not available in this environment.

Outputs:
  data/deere/drv_ag_commodities.csv   tidy long panel
"""

import csv
import io
import os
import sys
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from collections import defaultdict

UA = "AgentsVsWallStreet cor@salomo.io"
ROOT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter"
OUT_CSV = os.path.join(ROOT, "data/deere/drv_ag_commodities.csv")
CACHE = os.environ.get(
    "AG_CACHE",
    "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/ag",
)

# Panel window. 2006Q1 calendar start; Deere FY2006 Q1 begins 2005-11-01.
PANEL_START = date(2005, 11, 1)
PANEL_END = date(2026, 8, 2)  # Deere FY2026 Q3 end (quarter not yet reported)

# ---------------------------------------------------------------------------
# Unit conversion constants
# ---------------------------------------------------------------------------
LB_KG = 0.45359237
# US bushel test weights: corn 56 lb, soybeans & wheat 60 lb.
BU_PER_MT_CORN = 1000.0 / (56 * LB_KG)      # 39.36825...
BU_PER_MT_SOY = 1000.0 / (60 * LB_KG)       # 36.74371...
BU_PER_MT_WHEAT = BU_PER_MT_SOY

# ---------------------------------------------------------------------------
# Deere fiscal calendar.
#
# Source: SEC EDGAR XBRL companyconcept us-gaap/Revenues for CIK 0000315189,
# from which the distinct ~91-day and ~364-day (start,end) periods were
# extracted; cross-checked against "Three Months Ended <date>" strings in the
# offline filings corpus. Both agree.
#
# Through FY2016 Deere reported on calendar month-ends (Jan 31 / Apr 30 /
# Jul 31 / Oct 31). From FY2017 Deere reports on a 52/53-week fiscal calendar
# ending on the Sunday nearest 31 October, so quarter-ends drift.
#
# FY2006 (2005-11-01 .. 2006-10-31) predates EDGAR XBRL coverage and is
# assigned by the pre-FY2017 calendar-month-end rule -> flagged inferred.
# FY2026 Q3 end (2026-08-02) is the scheduled period end; Deere has NOT
# reported that quarter as of the 2026-08-16 build date.
# ---------------------------------------------------------------------------
FISCAL_QUARTER_ENDS = {
    2006: ["2006-01-31", "2006-04-30", "2006-07-31", "2006-10-31"],
    2007: ["2007-01-31", "2007-04-30", "2007-07-31", "2007-10-31"],
    2008: ["2008-01-31", "2008-04-30", "2008-07-31", "2008-10-31"],
    2009: ["2009-01-31", "2009-04-30", "2009-07-31", "2009-10-31"],
    2010: ["2010-01-31", "2010-04-30", "2010-07-31", "2010-10-31"],
    2011: ["2011-01-31", "2011-04-30", "2011-07-31", "2011-10-31"],
    2012: ["2012-01-31", "2012-04-30", "2012-07-31", "2012-10-31"],
    2013: ["2013-01-31", "2013-04-30", "2013-07-31", "2013-10-31"],
    2014: ["2014-01-31", "2014-04-30", "2014-07-31", "2014-10-31"],
    2015: ["2015-01-31", "2015-04-30", "2015-07-31", "2015-10-31"],
    2016: ["2016-01-31", "2016-04-30", "2016-07-31", "2016-10-31"],
    2017: ["2017-01-29", "2017-04-30", "2017-07-30", "2017-10-29"],
    2018: ["2018-01-28", "2018-04-29", "2018-07-29", "2018-10-28"],
    2019: ["2019-01-27", "2019-04-28", "2019-07-28", "2019-11-03"],
    2020: ["2020-02-02", "2020-05-03", "2020-08-02", "2020-11-01"],
    2021: ["2021-01-31", "2021-05-02", "2021-08-01", "2021-10-31"],
    2022: ["2022-01-30", "2022-05-01", "2022-07-31", "2022-10-30"],
    2023: ["2023-01-29", "2023-04-30", "2023-07-30", "2023-10-29"],
    2024: ["2024-01-28", "2024-04-28", "2024-07-28", "2024-10-27"],
    2025: ["2025-01-26", "2025-04-27", "2025-07-27", "2025-11-02"],
    2026: ["2026-02-01", "2026-05-03", "2026-08-02"],  # Q4 not yet defined/ended
}
INFERRED_FY = {2006}          # calendar-month-end rule applied, not XBRL-confirmed
UNREPORTED_END = date(2026, 8, 2)   # FY2026 Q3: period ends but is unreported


def fiscal_windows():
    """[(fy, 'Q1'..'Q4', start_date, end_date)] for Deere fiscal quarters."""
    out = []
    prev_end = PANEL_START - timedelta(days=1)
    for fy in sorted(FISCAL_QUARTER_ENDS):
        for i, ds in enumerate(FISCAL_QUARTER_ENDS[fy]):
            end = date.fromisoformat(ds)
            start = prev_end + timedelta(days=1)
            out.append((fy, "Q%d" % (i + 1), start, end))
            prev_end = end
    return out


def calendar_windows():
    """[(year, 'Q1'..'Q4', start_date, end_date)] for calendar quarters."""
    out = []
    for y in range(2006, 2027):
        for q, (m0, m1) in enumerate([(1, 3), (4, 6), (7, 9), (10, 12)], start=1):
            start = date(y, m0, 1)
            end = date(y, m1 + 1, 1) - timedelta(days=1) if m1 < 12 else date(y, 12, 31)
            if start > PANEL_END:
                continue
            out.append((y, "Q%d" % q, start, end))
    return out


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------
def fetch(url, cache_name, binary=False):
    path = os.path.join(CACHE, cache_name)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        mode = "rb" if binary else "r"
        with open(path, mode) as fh:
            return fh.read()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(raw)
    return raw if binary else raw.decode("utf-8", "replace")


def fred_series(series_id):
    """-> dict[date] = float. Handles FRED's '.' missing marker."""
    txt = fetch(
        "https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + series_id,
        "fred_%s.csv" % series_id,
    )
    rd = csv.reader(io.StringIO(txt))
    hdr = next(rd)
    if not hdr or "observation_date" not in hdr[0]:
        raise RuntimeError("FRED %s: unexpected payload" % series_id)
    out = {}
    for row in rd:
        if len(row) < 2 or row[1].strip() in (".", ""):
            continue
        out[date.fromisoformat(row[0])] = float(row[1])
    return out


# ---------------------------------------------------------------------------
# World Bank Pink Sheet
# ---------------------------------------------------------------------------
WB_URL = ("https://thedocs.worldbank.org/en/doc/"
          "18675f1d1639c7a34d463f59263ba0a2-0050012025/related/"
          "CMO-Historical-Data-Monthly.xlsx")
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def worldbank_monthly():
    """-> (dict[column_label] = dict[(y,m)] = float, units_by_label)."""
    raw = fetch(WB_URL, "wb_pinksheet.xlsx", binary=True)
    z = zipfile.ZipFile(io.BytesIO(raw))
    shared = [
        "".join(t.text or "" for t in si.iter(NS + "t"))
        for si in ET.fromstring(z.read("xl/sharedStrings.xml"))
    ]
    sheet = ET.fromstring(z.read("xl/worksheets/sheet2.xml"))  # "Monthly Prices"

    def cellval(c):
        v = c.find(NS + "v")
        if v is None:
            return None
        return shared[int(v.text)] if c.get("t") == "s" else v.text

    def colof(ref):
        return "".join(ch for ch in ref if ch.isalpha())

    names, units, data = {}, {}, defaultdict(dict)
    for r in sheet.iter(NS + "row"):
        n = int(r.get("r"))
        cells = {colof(c.get("r")): cellval(c) for c in r.iter(NS + "c")}
        if n == 5:
            names = {k: (v or "").strip() for k, v in cells.items() if v}
        elif n == 6:
            units = {k: (v or "").strip() for k, v in cells.items() if v}
        elif n >= 7:
            per = cells.get("A")
            if not per or "M" not in str(per):
                continue
            y, m = str(per).split("M")
            key = (int(y), int(m))
            for col, val in cells.items():
                if col == "A" or val in (None, "", "…", ".."):
                    continue
                lab = names.get(col)
                if not lab:
                    continue
                try:
                    data[lab][key] = float(val)
                except ValueError:
                    continue
    return data, {names[k]: v for k, v in units.items() if k in names}


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
def month_key(d):
    return (d.year, d.month)


def monthly_to_window(monthly, start, end):
    """Day-weighted average of a monthly series over [start, end].

    Every calendar day in the window takes the value of the month it falls in.
    This is what makes a Deere fiscal quarter (which starts/ends mid-month,
    e.g. 2026-02-02..2026-05-03) aggregate correctly rather than being forced
    onto whole calendar months.

    Returns (avg, coverage_fraction) or (None, cov) if <95% of days covered.
    """
    total, hit, acc = 0, 0, 0.0
    d = start
    while d <= end:
        total += 1
        v = monthly.get(month_key(d))
        if v is not None:
            acc += v
            hit += 1
        d += timedelta(days=1)
    if total == 0:
        return None, 0.0
    cov = hit / total
    return (acc / hit if hit and cov >= 0.95 else None), cov


def months_in_window(start, end):
    """-> [( (y,m), days_in_window )] ordered."""
    counts = defaultdict(int)
    d = start
    while d <= end:
        counts[month_key(d)] += 1
        d += timedelta(days=1)
    return sorted(counts.items())


def monthly_quarter_end(monthly, start, end):
    """Quarter-end proxy for a monthly source.

    Defined as: the value of the LAST calendar month that has at least 15 days
    inside the quarter window. Deere fiscal quarters end mid-month (e.g.
    2026-05-03), so 'the month containing the end date' would return a month
    the quarter barely touched. The >=15-day rule returns the last month the
    quarter was genuinely exposed to.

    Returns (value, "YYYY-MM") or (None, None).
    """
    cand = [mk for mk, n in months_in_window(start, end) if n >= 15]
    if not cand:
        return None, None
    mk = cand[-1]
    return monthly.get(mk), "%04d-%02d" % mk


def daily_to_window(obs, start, end):
    """Mean of all observations dated within [start, end]."""
    vals = [v for d, v in obs.items() if start <= d <= end]
    return (sum(vals) / len(vals)) if vals else None, len(vals)


def daily_quarter_end(obs, end, max_back=14):
    """Last observation on or before `end`, within max_back days."""
    best = None
    for d, v in obs.items():
        if d <= end and (end - d).days <= max_back:
            if best is None or d > best[0]:
                best = (d, v)
    return best  # (date, value) or None


# ---------------------------------------------------------------------------
# Series definitions
# ---------------------------------------------------------------------------
# (base_id, fred_id, units_out, scale_fn, description, freq)
IMF_PRICES = [
    ("px_corn", "PMAIZMTUSDM", "USD/bushel", lambda v: v / BU_PER_MT_CORN,
     "IMF global corn price: US No.2 Yellow, prompt shipment, FOB US Gulf of "
     "Mexico ports, USD/metric ton converted at 56 lb/bushel (39.36825 bu/mt)"),
    ("px_soybean", "PSOYBUSDM", "USD/bushel", lambda v: v / BU_PER_MT_SOY,
     "IMF global soybean price: US soybeans, CBOT nearest forward contract, "
     "No.2 yellow and par, USD/metric ton converted at 60 lb/bushel "
     "(36.74371 bu/mt)"),
    ("px_wheat", "PWHEAMTUSDM", "USD/bushel", lambda v: v / BU_PER_MT_WHEAT,
     "IMF global wheat price: US No.1 Hard Red Winter, ordinary protein, "
     "KANSAS CITY (an interior rail-terminal quote, NOT a Gulf export price), "
     "USD/metric ton converted at 60 lb/bushel (36.74371 bu/mt)"),
    ("px_cotton", "PCOTTINDUSDM", "USD/lb", lambda v: v / 100.0,
     "IMF global cotton price (Cotlook A Index), US cents/lb -> USD/lb"),
    ("px_sugar", "PSUGAISAUSDM", "USD/lb", lambda v: v / 100.0,
     "IMF global sugar price (ISA daily price, world), US cents/lb -> USD/lb"),
]

# World Bank Pink Sheet cross-check + fertiliser levels.
# Every definition below is quoted from the workbook's own "Description" sheet,
# including the definition BREAKS it discloses. Those breaks are level shifts
# inside the series and a modeller must treat them as structural.
WB_SERIES = [
    ("px_corn_wb", "Maize", "USD/bushel", lambda v: v / BU_PER_MT_CORN,
     "World Bank Pink Sheet: 'Maize (U.S.), no. 2, yellow, f.o.b. US Gulf ports'. "
     "USD/mt -> USD/bu (56 lb/bu). SAME quote as px_corn (IMF) - true "
     "independent cross-check, agrees to ~0.1%."),
    ("px_soybean_wb", "Soybeans", "USD/bushel", lambda v: v / BU_PER_MT_SOY,
     "World Bank Pink Sheet soybeans. DEFINITION BREAKS disclosed by the "
     "source: from Jan-2025 'U.S. Soybeans, FOB U.S. Gulf'; Jan-2021..Dec-2024 "
     "'U.S. Gulf Yellow Soybean #2, CIF Rotterdam'; Dec-2007..Dec-2020 'U.S. "
     "No.2 yellow MEAL, CIF Rotterdam'; previously US origin nearest forward. "
     "USD/mt -> USD/bu (60 lb/bu). NOT a like-for-like cross-check on "
     "px_soybean before 2025 - the Dec-2007..Dec-2020 stretch is a MEAL quote, "
     "not whole beans. Use for shape, not level."),
    ("px_wheat_hrw_wb", "Wheat, US HRW", "USD/bushel", lambda v: v / BU_PER_MT_WHEAT,
     "World Bank Pink Sheet: 'Wheat (U.S.), no. 2 hard red winter GULF EXPORT "
     "price; June-2020 backwards, no.1 hard red winter ordinary protein, export "
     "price delivered at the US Gulf port'. USD/mt -> USD/bu (60 lb/bu). This "
     "is a GULF FOB export quote, whereas px_wheat (IMF) is a KANSAS CITY "
     "interior quote: WB runs 12-32% higher and the wedge widens over the "
     "sample with rail freight. DO NOT splice the two."),
    ("px_wheat_srw_wb", "Wheat, US SRW", "USD/bushel", lambda v: v / BU_PER_MT_WHEAT,
     "World Bank Pink Sheet: 'Wheat (U.S.), no. 2, soft red winter, export "
     "price delivered at the US Gulf port'. USD/mt -> USD/bu (60 lb/bu)."),
    ("px_cotton_wb", "Cotton, A Index", "USD/lb", lambda v: v * LB_KG,
     "World Bank Pink Sheet: Cotton Outlook 'Cotlook A index', middling "
     "1-3/32 inch, traded Far East C/F from 2006 (previously N. Europe CIF). "
     "USD/kg -> USD/lb. SAME quote as px_cotton (IMF) - agrees to ~0.2%."),
    ("px_sugar_wb", "Sugar, world", "USD/lb", lambda v: v * LB_KG,
     "World Bank Pink Sheet: 'Sugar (World), International Sugar Agreement "
     "(ISA) daily price, raw, f.o.b. and stowed at greater Caribbean ports'. "
     "USD/kg -> USD/lb. SAME quote as px_sugar (IMF) - agrees to ~2%."),
]

WB_INPUTS = [
    ("px_urea", "Urea", "USD/mt", lambda v: v,
     "World Bank Pink Sheet: 'Urea, prill spot f.o.b. MIDDLE EAST beginning "
     "March-2022; previously f.o.b. BLACK SEA'. DEFINITION BREAK at 2022-03 - "
     "coincides with the Russia/Ukraine nitrogen shock, so the break and a "
     "genuine price spike are confounded. Key crop input cost."),
    ("px_potash", "Potassium chloride **", "USD/mt", lambda v: v,
     "World Bank Pink Sheet: 'Potassium chloride (muriate of potash), BRAZIL "
     "CFR granular spot price from January-2020; previously f.o.b. VANCOUVER'. "
     "DEFINITION BREAK at 2020-01 - CFR Brazil embeds freight that FOB "
     "Vancouver does not, so there is a level shift at that date that is NOT a "
     "market move. Key crop input cost."),
    ("px_dap", "DAP", "USD/mt", lambda v: v,
     "World Bank Pink Sheet: 'DAP (diammonium phosphate), spot, f.o.b. US "
     "Gulf'. Key crop input cost."),
    ("px_tsp", "TSP", "USD/mt", lambda v: v,
     "World Bank Pink Sheet: 'TSP (triple superphosphate), spot, IMPORT US "
     "Gulf'. Crop input cost."),
    ("px_phosphate_rock", "Phosphate rock", "USD/mt", lambda v: v,
     "World Bank Pink Sheet: 'Phosphate rock, f.o.b. NORTH AFRICA'. "
     "Upstream crop input cost."),
]

# ---------------------------------------------------------------------------
# BLS PPI farm-product price indices. Series titles were confirmed against the
# BLS flat file https://download.bls.gov/pub/time.series/wp/wp.series (field
# series_title), not guessed. These publish ~6 weeks faster than the IMF
# monthly commodity series, so they alone give full coverage of Deere's
# FY2026 Q3 window (2026-05-04 .. 2026-08-02).
# ---------------------------------------------------------------------------
PPI_FARM = [
    ("ppi_corn", "WPU01220205",
     "BLS PPI Farm products - Corn, NSA (1982=100). Index, not a price level."),
    ("ppi_soybean", "WPU01830131",
     "BLS PPI Farm products - Soybeans, NSA (1982=100). Index, not a price level."),
    ("ppi_wheat_hrw", "WPU01210101",
     "BLS PPI Farm products - Hard red winter wheat, NSA (1982=100). Index."),
    ("ppi_wheat_all", "WPU0121",
     "BLS PPI Farm products - Wheat, NSA (1982=100). Index, not a price level."),
    ("ppi_cotton_raw", "WPU0151",
     "BLS PPI Farm products - Raw cotton, NSA (1982=100). Index, not a price level."),
]

# Index-splice nowcast: price_base is carried forward past its last observed
# month using the month-over-month ratio of the matched PPI index.
#   base_id -> (ppi_fred_id, ppi_human_name, max_months_to_extend)
# Matched on definition: IMF wheat is No.1 Hard Red Winter (Kansas City), so
# the HRW wheat PPI is the right index. US raw sugar is price-supported and
# decoupled from the world ISA price, so sugar is deliberately NOT nowcast.
NOWCAST = {
    "px_corn": ("WPU01220205", "BLS PPI Farm products - Corn", 2),
    "px_soybean": ("WPU01830131", "BLS PPI Farm products - Soybeans", 2),
    "px_wheat": ("WPU01210101", "BLS PPI Farm products - Hard red winter wheat", 2),
    "px_cotton": ("WPU0151", "BLS PPI Farm products - Raw cotton", 2),
}


def add_months(mk, k):
    y, m = mk
    n = (y * 12 + (m - 1)) + k
    return (n // 12, n % 12 + 1)


def extend_by_index(monthly, index_monthly, max_months):
    """Carry `monthly` forward past its last observation using MoM ratios of
    `index_monthly`. Returns (extended_dict, set_of_nowcast_month_keys)."""
    out = dict(monthly)
    nowcast = set()
    if not out or not index_monthly:
        return out, nowcast
    last = max(out)
    for k in range(1, max_months + 1):
        mk = add_months(last, k)
        prev = add_months(last, k - 1)
        i_now, i_prev = index_monthly.get(mk), index_monthly.get(prev)
        if i_now is None or i_prev is None or not i_prev:
            break
        out[mk] = out[prev] * (i_now / i_prev)
        nowcast.add(mk)
    return out, nowcast


# FRED monthly index series (crop inputs; extend past the Pink Sheet vintage)
FRED_INDEX = [
    ("ppi_fertilizer_materials", "WPU0652", "index",
     "BLS PPI by commodity: chemicals & allied products - fertilizer materials "
     "(1982=100). Index, not a price level. Extends fertiliser coverage past "
     "the Pink Sheet vintage end."),
    ("ppi_nitrogenous_fertilizer_mfg", "PCU325311325311", "index",
     "BLS PPI industry: nitrogenous fertilizer manufacturing (Dec 1975=100). "
     "Index, not a price level."),
    ("ppi_diesel_no2", "WPU057303", "index",
     "BLS PPI by commodity: No.2 diesel fuel (1973=100). Index, not a price level."),
]

# FRED higher-frequency series (crop input / energy cost)
FRED_HIFREQ = [
    ("px_diesel_retail_us", "GASDESW", "USD/gallon", "weekly",
     "EIA US No.2 diesel retail price, all types, weekly (Monday-dated). "
     "Primary on-farm fuel cost proxy."),
    ("px_wti_crude", "DCOILWTICO", "USD/barrel", "daily",
     "EIA WTI spot crude, daily. Upstream driver of diesel and nitrogen "
     "fertiliser cost."),
]

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s"


def qlabel_note(kind, cal, fy_inferred, unreported):
    bits = []
    if cal == "fq":
        bits.append("Deere fiscal quarter window")
        if fy_inferred:
            bits.append("fiscal dates INFERRED from pre-FY2017 calendar-month-end "
                        "rule (predates EDGAR XBRL coverage)")
        if unreported:
            bits.append("Deere has NOT reported this quarter as of 2026-08-16; "
                        "driver data only, no company actuals exist")
    else:
        bits.append("calendar quarter window")
    bits.append("quarterly average = day-weighted mean of the monthly source "
                "over the window" if kind == "avg" else None)
    return bits


def _corr(a, b):
    n = len(a)
    if n < 3:
        return float("nan")
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a) ** 0.5
    vb = sum((x - mb) ** 2 for x in b) ** 0.5
    if va == 0 or vb == 0:
        return float("nan")
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (va * vb)


# (label, series_a, series_b, expectation)
CROSSCHECKS = [
    ("corn USD/bu", "px_corn_avg_cq", "px_corn_wb_avg_cq",
     "same underlying quote (US No.2 Yellow FOB Gulf) via two publishers"),
    ("soybeans USD/bu", "px_soybean_avg_cq", "px_soybean_wb_avg_cq",
     "DIFFERENT quotes: IMF=CBOT nearest-forward; WB=CIF Rotterdam and a MEAL "
     "quote 2007-2020. Level gap EXPECTED; correlation is the real test"),
    ("wheat HRW USD/bu", "px_wheat_avg_cq", "px_wheat_hrw_wb_avg_cq",
     "DIFFERENT delivery points: IMF=Kansas City interior; WB=US Gulf FOB "
     "export. Rail-freight wedge EXPECTED and widening; correlation is the test"),
    ("cotton USD/lb", "px_cotton_avg_cq", "px_cotton_wb_avg_cq",
     "same underlying quote (Cotlook A Index) via two publishers"),
    ("sugar USD/lb", "px_sugar_avg_cq", "px_sugar_wb_avg_cq",
     "same underlying quote (world/ISA raw sugar) via two publishers"),
    ("corn: price vs PPI index", "px_corn_avg_cq", "ppi_corn_avg_cq",
     "different units; correlation only"),
    ("diesel: retail USD/gal vs PPI index", "px_diesel_retail_us_avg_cq",
     "ppi_diesel_no2_avg_cq", "different units; correlation only"),
    ("urea USD/mt vs nitrogen-fertiliser PPI", "px_urea_avg_cq",
     "ppi_nitrogenous_fertilizer_mfg_avg_cq", "different units; correlation only"),
]


def validate(rows):
    idx = defaultdict(dict)
    for r in rows:
        idx[r["series_id"]][r["period_end"]] = float(r["value"])
    lines = ["", "=" * 78, "CROSS-SOURCE VALIDATION", "=" * 78]
    for label, sa, sb, expect in CROSSCHECKS:
        A, B = idx.get(sa, {}), idx.get(sb, {})
        common = sorted(set(A) & set(B))
        if len(common) < 8:
            lines.append("%-38s NO OVERLAP (n=%d)" % (label, len(common)))
            continue
        a = [A[d] for d in common]
        b = [B[d] for d in common]
        r = _corr(a, b)
        pdiff = [abs(x - y) / ((abs(x) + abs(y)) / 2) * 100 for x, y in zip(a, b)]
        mad = sum(pdiff) / len(pdiff)
        worst = max(range(len(pdiff)), key=lambda i: pdiff[i])
        lines.append(
            "%-38s n=%3d  corr=%+.4f  mean|%%diff|=%6.2f%%  worst=%s "
            "(%.4f vs %.4f = %.1f%%)"
            % (label, len(common), r, mad, common[worst], a[worst], b[worst],
               pdiff[worst]))
        lines.append("      %s vs %s -- %s" % (sa, sb, expect))
    # Spot checks: raw source values must round-trip through the unit maths.
    lines += ["", "SPOT CHECKS (unit conversion round-trip)"]
    spots = [
        ("px_corn_qe_cq", "2026-06-30", 195.78187899659861 / BU_PER_MT_CORN,
         "FRED PMAIZMTUSDM 2026-06-01 = 195.7819 USD/mt / 39.36825 bu/mt"),
        ("px_soybean_qe_cq", "2026-06-30", 414.5423329603930 / BU_PER_MT_SOY,
         "FRED PSOYBUSDM 2026-06-01 = 414.5423 USD/mt / 36.74371 bu/mt"),
        ("px_wheat_qe_cq", "2026-06-30", 199.64828756190479 / BU_PER_MT_WHEAT,
         "FRED PWHEAMTUSDM 2026-06-01 = 199.6483 USD/mt / 36.74371 bu/mt"),
        ("px_cotton_qe_cq", "2026-06-30", 86.29318181818182 / 100.0,
         "FRED PCOTTINDUSDM 2026-06-01 = 86.2932 US cents/lb / 100"),
        ("px_sugar_qe_cq", "2026-06-30", 13.90772727272727 / 100.0,
         "FRED PSUGAISAUSDM 2026-06-01 = 13.9077 US cents/lb / 100"),
        ("px_diesel_retail_us_qe_cq", "2026-06-30", None,
         "EIA GASDESW last weekly obs on/before 2026-06-30"),
    ]
    for sid, pe, expected, why in spots:
        got = idx.get(sid, {}).get(pe)
        if got is None:
            lines.append("  %-28s %s  MISSING" % (sid, pe))
        elif expected is None:
            lines.append("  %-28s %s  value=%.4f  (%s)" % (sid, pe, got, why))
        else:
            ok = abs(got - expected) < 1e-4
            lines.append("  %-28s %s  got=%.6f expected=%.6f  %s  [%s]"
                         % (sid, pe, got, expected, "OK" if ok else "MISMATCH", why))
    out = "\n".join(lines)
    print(out, file=sys.stderr)
    with open(os.path.join(CACHE, "validation.txt"), "w") as fh:
        fh.write(out + "\n")


def main():
    rows = []
    fq = fiscal_windows()
    cq = calendar_windows()
    windows = [("fq", fy, q, s, e) for (fy, q, s, e) in fq] + \
              [("cq", y, q, s, e) for (y, q, s, e) in cq]

    def emit(sid, end, yr, q, val, units, stype, src, note):
        if val is None:
            return
        rows.append({
            "series_id": sid,
            "period_end": end.isoformat(),
            "fiscal_year": yr,
            "fiscal_quarter": q,
            "value": ("%.6f" % val).rstrip("0").rstrip(".") if isinstance(val, float) else val,
            "units": units,
            "source_type": stype,
            "source": src,
            "notes": note,
        })

    # ---------------- monthly sources ----------------
    # (base, monthly, units, desc, src, stype, nowcast_months)
    monthly_sources = []
    ppi_cache = {}
    for _b, fid, _d in PPI_FARM:
        ppi_cache[fid] = {month_key(d): v for d, v in fred_series(fid).items()}
    for _b, fid, _u, _d in FRED_INDEX:
        ppi_cache.setdefault(fid, {month_key(d): v for d, v in fred_series(fid).items()})

    for base, fid, units, fn, desc in IMF_PRICES:
        raw = fred_series(fid)
        m = {month_key(d): fn(v) for d, v in raw.items()}
        nc = set()
        if base in NOWCAST:
            nfid, nname, nmax = NOWCAST[base]
            idx = ppi_cache.get(nfid) or {
                month_key(d): v for d, v in fred_series(nfid).items()}
            ppi_cache[nfid] = idx
            m, nc = extend_by_index(m, idx, nmax)
            if nc:
                desc = (desc + "; series carried past its last observed month "
                        "(%s) by index splice on %s (%s)"
                        % ("-".join("%02d" % x for x in max(set(m) - nc)),
                           nname, nfid))
        monthly_sources.append((base, m, units, desc, FRED_URL % fid, "api", nc))

    wb, wbunits = worldbank_monthly()
    for base, lab, units, fn, desc in WB_SERIES + WB_INPUTS:
        if lab not in wb:
            print("WARN: pink sheet column missing: %r" % lab, file=sys.stderr)
            continue
        m = {k: fn(v) for k, v in wb[lab].items()}
        monthly_sources.append((base, m, units, desc, WB_URL, "vendor", set()))

    for base, fid, desc in PPI_FARM:
        monthly_sources.append((base, ppi_cache[fid], "index", desc,
                                FRED_URL % fid, "api", set()))

    for base, fid, units, desc in FRED_INDEX:
        monthly_sources.append((base, ppi_cache[fid], units, desc,
                                FRED_URL % fid, "api", set()))

    for base, m, units, desc, src, stype, ncmonths in monthly_sources:
        for cal, yr, q, s, e in windows:
            if e > PANEL_END:
                continue
            tail = []
            if cal == "fq":
                tail.append("Deere fiscal quarter FY%s-%s (%s..%s)"
                            % (yr, q, s.isoformat(), e.isoformat()))
                if yr in INFERRED_FY:
                    tail.append("fiscal quarter dates INFERRED via the pre-FY2017 "
                                "calendar-month-end rule (predates EDGAR XBRL "
                                "coverage)")
                if e == UNREPORTED_END:
                    tail.append("Deere has NOT reported this quarter as of "
                                "2026-08-16; driver data only")
            else:
                tail.append("calendar quarter %s-%s" % (yr, q))

            wmonths = {mk for mk, _n in months_in_window(s, e)}
            hit_nc = sorted(wmonths & ncmonths)
            nc_note = []
            st = stype
            if hit_nc:
                st = "estimate"
                nc_note = ["CONTAINS NOWCAST: month(s) %s are index-spliced "
                           "estimates, not observed source data"
                           % ",".join("%04d-%02d" % x for x in hit_nc)]

            avg, cov = monthly_to_window(m, s, e)
            emit(base + "_avg_" + cal, e, yr, q, avg, units, st, src,
                 "; ".join([desc,
                            "quarterly average = day-weighted mean of the monthly "
                            "source over the quarter window (each calendar day "
                            "carries its month's value); day coverage %.2f" % cov]
                           + nc_note + tail))

            qe, qem = monthly_quarter_end(m, s, e)
            qe_st = st
            if qem and tuple(int(x) for x in qem.split("-")) in ncmonths:
                qe_st = "estimate"
            elif qem and tuple(int(x) for x in qem.split("-")) not in ncmonths:
                qe_st = stype
            emit(base + "_qe_" + cal, e, yr, q, qe, units, qe_st, src,
                 "; ".join([desc,
                            "quarter-end PROXY from a MONTHLY source: value of "
                            "the last calendar month with >=15 days inside the "
                            "quarter window (month %s). This is a monthly "
                            "average, NOT a spot close on %s"
                            % (qem, e.isoformat())]
                           + (nc_note if qe_st == "estimate" else []) + tail))

    # ---------------- higher-frequency sources ----------------
    for base, fid, units, freq, desc in FRED_HIFREQ:
        obs = fred_series(fid)
        for cal, yr, q, s, e in windows:
            if e > PANEL_END:
                continue
            inf = (cal == "fq" and yr in INFERRED_FY)
            unrep = (cal == "fq" and e == UNREPORTED_END)
            tail = []
            if cal == "fq":
                tail.append("Deere fiscal quarter %s-%s (%s..%s)"
                            % (yr, q, s.isoformat(), e.isoformat()))
                if inf:
                    tail.append("fiscal dates inferred via pre-FY2017 "
                                "calendar-month-end rule")
                if unrep:
                    tail.append("Deere has NOT reported this quarter as of 2026-08-16")
            else:
                tail.append("calendar quarter %s-%s" % (yr, q))

            avg, n = daily_to_window(obs, s, e)
            # require a plausible number of observations in the window
            need = 8 if freq == "weekly" else 40
            if n < need:
                avg = None
            emit(base + "_avg_" + cal, e, yr, q, avg, units, "api", FRED_URL % fid,
                 "; ".join([desc,
                            "quarterly average = simple mean of the %s "
                            "observations dated inside the quarter window "
                            "(n=%d)" % (freq, n)] + tail))

            last = daily_quarter_end(obs, e)
            emit(base + "_qe_" + cal, e, yr, q, (last[1] if last else None), units,
                 "api", FRED_URL % fid,
                 "; ".join([desc,
                            "quarter-end = last %s observation on or before the "
                            "quarter end%s" % (
                                freq,
                                " (obs dated %s)" % last[0].isoformat() if last else "")]
                           + tail))

    rows.sort(key=lambda r: (r["series_id"], r["period_end"]))
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "series_id", "period_end", "fiscal_year", "fiscal_quarter",
            "value", "units", "source_type", "source", "notes"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ---------------- validation ----------------
    validate(rows)

    # ---------------- summary to stderr ----------------
    per = defaultdict(list)
    for r in rows:
        per[r["series_id"]].append(r["period_end"])
    print("rows=%d series=%d" % (len(rows), len(per)))
    for sid in sorted(per):
        ds = sorted(per[sid])
        print("%-42s n=%3d %s..%s" % (sid, len(ds), ds[0], ds[-1]))


if __name__ == "__main__":
    main()
