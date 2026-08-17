#!/usr/bin/env python3
"""
Build /data/deere/dealers/used_equipment.csv

Task: used equipment values & inventory as a leading indicator of Deere dealer
profitability and new-equipment shipments, plus Deere's lease-residual exposure.

Sources
-------
A) Sandhills Global monthly market reports (US used farm equipment): inventory,
   asking values, auction values, % M/M and % Y/Y, by category.
   Each report is published ~5th-11th of month M+1 and covers data month M.
   Figures transcribed from the cited article URLs (see `source` column).
B) Deere corpus (frozen 2026-08-14) at challenge/offline-data/deere:
   - 10-K critical-accounting-estimate residual-value sensitivity ($m impact of a
     10% decline in future market values of leased equipment)
   - Equipment on operating leases - net (balance sheet), annual + quarterly
   - Lease revenues, guaranteed/unguaranteed residual values
   - Management's own quantified used-inventory disclosures from earnings calls
C) FRED WPU111 - PPI, farm machinery & equipment (NEW equipment list prices).
   Used as the new-vs-used price wedge reference.

Missing data is omitted, never zeroed.
"""

import csv
import os
import calendar
import datetime as dt

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/used_equipment.csv"
FRED_CSV = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/wpu111.csv"

HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "entity",
          "metric", "value", "units", "source_type", "source", "notes"]

rows = []


def add(series_id, period_end, fy, fq, entity, metric, value, units,
        source_type, source, notes=""):
    if value is None or value == "":
        return  # missing data -> absent row
    rows.append([series_id, period_end, fy, fq, entity, metric, value, units,
                 source_type, source, notes])


# ---------------------------------------------------------------------------
# Deere fiscal calendar. FY ends the Sunday closest to 31 Oct; Q1/Q2/Q3 end
# ~late Jan / late Apr / late Jul. Boundaries used to map calendar months.
# ---------------------------------------------------------------------------
FY_Q_END = {
    (2024, 1): "2024-01-28", (2024, 2): "2024-04-28", (2024, 3): "2024-07-28", (2024, 4): "2024-10-27",
    (2025, 1): "2025-01-26", (2025, 2): "2025-04-27", (2025, 3): "2025-07-27", (2025, 4): "2025-11-02",
    (2026, 1): "2026-02-01", (2026, 2): "2026-05-03", (2026, 3): "2026-08-02", (2026, 4): "2026-11-01",
}


def fiscal_of(date_str):
    """Map a calendar date to (fiscal_year, fiscal_quarter) for Deere."""
    d = dt.date.fromisoformat(date_str)
    # Approximate FY start: first Monday-ish of November of prior calendar year.
    for fy in range(2012, 2028):
        starts = dt.date(fy - 1, 11, 1)
        ends = dt.date(fy, 10, 31)
        if starts <= d <= ends + dt.timedelta(days=4):
            # find quarter
            for q in (1, 2, 3, 4):
                qe = FY_Q_END.get((fy, q))
                if qe is None:
                    # fall back to nominal boundaries
                    nominal = {1: dt.date(fy, 1, 31), 2: dt.date(fy, 4, 30),
                               3: dt.date(fy, 7, 31), 4: dt.date(fy, 10, 31)}[q]
                else:
                    nominal = dt.date.fromisoformat(qe)
                if d <= nominal + dt.timedelta(days=3):
                    return fy, q
            return fy, 4
    return "", ""


def eom(y, m):
    return f"{y:04d}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"


def fiscal_of_month(y, m):
    """Fiscal mapping for a monthly observation: use the month's midpoint so a
    data month is assigned to the fiscal quarter it mostly sits in."""
    return fiscal_of(f"{y:04d}-{m:02d}-15")


# ---------------------------------------------------------------------------
# A) SANDHILLS GLOBAL monthly used-equipment market reports
#    dict: (data_year, data_month) -> (publication_date, source_url, {category: (inv_mm, inv_yy, ask_mm, ask_yy, auc_mm, auc_yy)})
#    None = not disclosed in that report.
# ---------------------------------------------------------------------------
CATS = {
    "tractor_100hp_plus": "US used tractors 100+ hp",
    "tractor_175_299hp": "US used tractors 175-299 hp",
    "tractor_300hp_plus": "US used tractors 300+ hp",
    "combine": "US used combines",
    "sprayer": "US used self-propelled sprayers",
    "planter": "US used planters",
    "compact_utility_tractor": "US used compact & utility tractors",
    "sp_forage_harvester": "US used self-propelled forage harvesters",
}

SANDHILLS = {
    # ---- cycle peak / stress phase -----------------------------------------
    (2022, 9): ("2022-10-14", "https://www.sandhills.com/news/article/250037243", {
        "tractor_175_299hp": (7.4, -32.0, 1.4, 11.9, 1.6, 10.3),
        "compact_utility_tractor": (7.4, 48.0, -1.1, 6.8, -3.1, 0.0),
    }),
    (2024, 4): ("2024-05-07", "https://www.sandhills.com/news/article/250041954", {
        "tractor_100hp_plus": (2.54, 58.30, -0.22, 5.18, -2.23, -2.02),
        "tractor_300hp_plus": (None, 106.93, None, None, None, None),
        "combine": (1.49, 17.63, 1.65, 8.27, -0.15, -0.56),
        "planter": (-0.29, 41.59, 1.01, 7.73, 1.87, -11.42),
        "compact_utility_tractor": (-3.63, 15.60, 0.44, -1.79, -0.05, -3.79),
    }),
    (2024, 8): ("2024-09-05", "https://www.sandhills.com/news/article/250042680", {
        "tractor_100hp_plus": (2.90, 37.09, -1.28, -2.62, -1.79, -13.14),
        "tractor_300hp_plus": (4.17, 62.48, None, None, None, None),
        "combine": (-2.58, 10.44, -0.56, 3.83, -2.03, -4.83),
        "sprayer": (4.39, 38.39, 0.60, -0.67, -2.85, -12.82),
        "planter": (4.06, 8.19, 4.94, -6.84, 5.96, -21.99),
        "compact_utility_tractor": (-1.03, -11.50, 0.36, -4.47, 0.65, -6.89),
    }),
    # ---- destock phase ------------------------------------------------------
    (2025, 2): ("2025-03-05", "https://www.sandhills.com/news/article/250044728", {
        "tractor_100hp_plus": (0.83, 6.09, -0.11, -4.60, -0.13, -6.27),
        "tractor_300hp_plus": (None, 12.65, None, -4.60, None, -6.27),
        "combine": (1.61, -5.82, -0.30, -0.44, 1.23, 1.10),
        "sprayer": (-2.56, 2.63, 3.12, -2.65, 2.56, -5.44),
        "planter": (-5.55, -8.63, 0.94, -3.67, 0.82, -1.14),
        "compact_utility_tractor": (-1.96, -24.10, 0.13, -3.40, 1.77, -2.89),
    }),
    (2025, 4): ("2025-05-06", "https://www.sandhills.com/news/article/250044995", {
        "tractor_100hp_plus": (-2.30, 1.73, 0.73, -4.86, -0.02, -4.52),
        "combine": (0.53, -5.43, 0.22, -2.06, 1.31, 2.21),
        "sprayer": (-3.69, -1.81, -1.88, -4.41, -3.71, -2.91),
        "planter": (-4.22, -13.15, -0.28, -1.36, 1.20, 10.51),
        "compact_utility_tractor": (-4.09, -23.71, -0.19, -1.66, -0.34, -0.35),
    }),
    (2025, 7): ("2025-08-06", "https://www.sandhills.com/news/article/250045354", {
        "tractor_100hp_plus": (-1.42, -4.17, -1.37, -6.28, -1.35, -2.83),
        "combine": (-2.29, -7.21, 0.93, 1.98, 1.53, 9.64),
        "sprayer": (-1.59, -7.97, -0.97, -4.98, -0.95, 0.07),
        "planter": (4.67, -18.19, 1.41, -0.75, 2.53, 10.73),
        "compact_utility_tractor": (-3.48, -23.77, -0.08, 0.63, 0.30, 2.24),
    }),
    (2025, 8): ("2025-09-05", "https://www.sandhills.com/news/article/250045479", {
        "tractor_100hp_plus": (-1.85, -7.52, -0.11, -6.22, -0.47, -2.95),
        "combine": (-6.62, -11.86, -5.84, -2.82, -5.02, 6.17),
        "sprayer": (1.17, -10.13, -0.16, -3.75, 1.29, 4.39),
        "planter": (-1.04, -21.22, 4.57, 0.48, 3.34, 7.78),
        "compact_utility_tractor": (-2.78, -24.32, 0.65, 0.97, 0.40, 2.06),
    }),
    (2025, 11): ("2025-12-04", "https://www.sandhills.com/news/article/250046010", {
        "tractor_100hp_plus": (-3.37, -14.64, -1.33, -5.50, 0.11, -3.78),
        "combine": (0.71, -11.01, 2.57, -0.57, 5.01, 6.34),
        "sprayer": (0.36, -13.70, -2.32, -6.94, -2.61, -4.94),
        "planter": (-2.28, -19.85, 0.56, 1.44, 3.74, 7.88),
        "compact_utility_tractor": (-2.47, -22.29, 0.45, 1.92, 0.64, 2.59),
    }),
    (2025, 12): ("2026-01-07", "https://www.sandhills.com/news/article/250046195", {
        "tractor_100hp_plus": (-1.90, -15.46, -0.07, -5.85, 2.39, -2.54),
        "combine": (4.66, -9.50, 4.66, -0.37, 6.11, 7.47),
        "sprayer": (-1.89, -14.52, -1.59, -8.05, -1.28, -6.38),
        "planter": (-6.35, -22.23, -2.66, 0.48, -1.00, 4.39),
        "compact_utility_tractor": (1.07, -19.85, -0.52, 2.50, -1.12, 2.55),
    }),
    (2026, 1): ("2026-02-04", "https://www.sandhills.com/news/article/250046401", {
        "tractor_100hp_plus": (-1.12, -16.99, 2.06, -1.12, 2.67, 1.89),
        "combine": (0.92, -11.43, 1.54, -3.82, 1.92, 2.35),
        "sprayer": (-3.11, -15.30, 0.57, -3.62, -0.16, -3.19),
        "planter": (-5.34, -22.92, 7.43, 1.65, 11.68, 8.05),
        "compact_utility_tractor": (-3.10, -22.59, 1.36, 1.05, 1.75, 1.54),
    }),
    (2026, 2): ("2026-03-06", "https://www.sandhills.com/news/article/250046662", {
        "tractor_100hp_plus": (0.02, -16.84, -0.88, -2.21, -1.05, 0.80),
        "combine": (1.87, -9.95, 1.16, -1.09, 0.68, 3.92),
        "sprayer": (-4.58, -15.13, -0.38, -3.12, 0.76, -2.02),
        "planter": (-6.22, -22.76, -1.10, 2.07, -2.44, 6.10),
        "compact_utility_tractor": (-5.76, -25.86, 0.97, 1.82, 3.23, 4.22),
    }),
    (2026, 4): ("2026-05-07", "https://www.sandhills.com/news/article/250047072", {
        "tractor_100hp_plus": (-2.01, -18.40, 0.55, -1.60, 1.67, 2.78),
        "combine": (-0.55, -11.89, 1.24, 1.32, -0.99, 2.16),
        "sprayer": (-2.43, -21.28, -0.45, -0.07, 1.37, 2.87),
        "planter": (-5.29, -25.97, -2.09, 2.25, -1.30, 7.53),
        "compact_utility_tractor": (-5.35, -28.64, 0.32, 1.79, 0.76, 3.13),
    }),
    # ---- THE MAY-JULY 2026 WINDOW = Deere fiscal Q3 2026 --------------------
    (2026, 5): ("2026-06-04", "https://www.sandhills.com/news/article/250047334", {
        "tractor_100hp_plus": (-0.81, -16.23, -0.51, -1.75, -0.90, 2.36),
        "combine": (0.60, -10.09, -2.61, -1.22, -1.52, 0.76),
        "sprayer": (-0.80, -19.18, -2.84, -2.59, -5.94, -2.90),
        "planter": (-5.33, -26.36, -0.15, 2.57, -3.26, 5.01),
        "compact_utility_tractor": (-2.91, -28.25, 0.02, 1.63, -0.16, 2.76),
    }),
    (2026, 6): ("2026-07-06", "https://www.sandhills.com/news/article/250047595", {
        "tractor_100hp_plus": (-1.26, -16.71, 0.63, -0.56, 0.56, 3.74),
        "tractor_175_299hp": (None, None, None, None, 1.10, 4.21),
        "combine": (-1.55, -10.19, -0.51, -1.28, -0.51, 0.72),
        "sprayer": (-4.73, -21.91, -0.74, -4.65, 1.83, -2.69),
        "planter": (8.19, -21.01, 3.60, 7.41, 6.86, 13.32),
        "compact_utility_tractor": (-0.25, -27.87, -0.70, 0.97, -1.75, 1.26),
        "sp_forage_harvester": (-2.92, -4.05, -3.53, -2.65, -3.75, 1.34),
    }),
    (2026, 7): ("2026-08-11", "https://www.monitordaily.com/sandhills-global-used-ag-equipment-inventories-continue-to-tighten-as-values-hold-steady/", {
        "tractor_100hp_plus": (-2.04, -16.75, -0.44, -0.04, -1.55, 2.97),
        "combine": (-3.29, -11.79, -0.55, -1.69, -0.49, 0.38),
        "sprayer": (2.63, -19.29, -1.90, -5.36, -3.97, -5.14),
        "planter": (9.11, -15.88, -2.98, 4.46, -1.12, 12.45),
        "compact_utility_tractor": (-1.34, -25.47, 0.20, 1.49, 0.41, 2.02),
        "sp_forage_harvester": (0.60, -5.11, 2.72, 0.08, -0.16, 1.36),
    }),
}

MEASURES = [
    ("inventory", "mom_pct", 0), ("inventory", "yoy_pct", 1),
    ("asking_value", "mom_pct", 2), ("asking_value", "yoy_pct", 3),
    ("auction_value", "mom_pct", 4), ("auction_value", "yoy_pct", 5),
]

for (y, m), (pub, url, cats) in sorted(SANDHILLS.items()):
    pe = eom(y, m)
    fy, fq = fiscal_of_month(y, m)
    for cat, tup in cats.items():
        for meas, stat, idx in MEASURES:
            v = tup[idx]
            if v is None:
                continue
            add(f"sandhills_{cat}_{meas}_{stat}", pe, fy, fq, "US used ag equipment market",
                f"{CATS[cat]} {meas.replace('_',' ')} {stat.replace('_',' ')}",
                v, "percent", "web",
                url,
                f"Sandhills Global market report published {pub}; data month {y}-{m:02d}. "
                f"Deere fiscal mapping FY{fy} Q{fq}.")

# Sandhills EVI (Equipment Value Index) asking-vs-auction spread
add("sandhills_evi_spread_pct", "2026-06-30", 2026, 3, "US used ag equipment market",
    "Sandhills EVI spread (asking vs auction value)", 32.0, "percent", "web",
    "https://www.sandhills.com/news/article/250047595",
    "June 2026 data, published 2026-07-06. Up 1pt vs May 2026; still below the 2015 cycle peak. "
    "A wide spread means sellers' asks have not yet met auction clearing levels.")

# ---------------------------------------------------------------------------
# B) DEERE OWN DISCLOSURES
# ---------------------------------------------------------------------------
CORP = "challenge/offline-data/deere"

# B1. 10-K critical accounting estimate: $m unfavourable impact if future market
#     values of leased equipment fall 10%.  NOTE the definition changed in FY2021:
#     from FY2021 onward the figure is stated AFTER dealer residual value
#     guarantees and assumes all equipment is returned for remarketing.
RESID_SENS = [
    (2015, "2015-11-01", 175, f"{CORP}/filings/2015-11-25__de-us-20151125-q4-10k__469104.md", "pre-FY2021 basis (annual depreciation increase, before dealer residual guarantees)"),
    (2016, "2016-10-30", 200, f"{CORP}/filings/2016-11-23__de-us-20161123-q4-10k__469184.md", "pre-FY2021 basis"),
    (2017, "2017-10-29", 200, f"{CORP}/filings/2017-11-22__de-us-20171122-q4-10k__468364.md", "pre-FY2021 basis"),
    (2018, "2018-10-28", 185, f"{CORP}/filings/2018-11-21__de-us-20181121-q4-10k__469201.md", "pre-FY2021 basis"),
    (2019, "2019-11-03", 175, f"{CORP}/filings/2019-11-27__de-us-20191127-q4-10k__469283.md", "pre-FY2021 basis"),
    (2020, "2020-11-01", 175, f"{CORP}/filings/2020-11-25__de-us-20201125-q4-10k__105845.md", "pre-FY2021 basis"),
    (2021, "2021-10-31", 80, f"{CORP}/filings/2021-11-24__de-us-20211124-q4-10k__131650.md", "FY2021 basis: after dealer residual value guarantees, assumes all units returned for remarketing. NOT comparable with FY2015-FY2020."),
    (2022, "2022-10-30", 40, f"{CORP}/filings/2022-11-23__de-us-20221123-q4-10k__105816.md", "after dealer residual value guarantees; trough of exposure - used values were at cycle highs"),
    (2023, "2023-10-29", 90, f"{CORP}/filings/2023-11-22__de-us-20231122-q4-10k__105844.md", "after dealer residual value guarantees"),
    (2024, "2024-10-27", 75, f"{CORP}/filings/2024-11-21__de-us-20241121-q4-10k__105810.md", "after dealer residual value guarantees"),
    (2025, "2025-11-02", 65, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md", "after dealer residual value guarantees; latest disclosed. Recognised as higher depreciation over remaining lease term or as impairment."),
]
for fy, pe, v, src, note in RESID_SENS:
    add("de_oplease_residual_sensitivity_10pct_usdm", pe, fy, 4, "Deere & Company",
        "Unfavourable impact of a 10% decline in future market values of equipment on operating leases",
        v, "USD_millions", "corpus", src, note)

# B2. Equipment on operating leases - net (the asset carrying the residual risk)
OPLEASE_FY = [
    (2014, "2014-11-02", 4016, f"{CORP}/filings/2015-11-25__de-us-20151125-q4-10k__469104.md"),
    (2015, "2015-11-01", 4970, f"{CORP}/filings/2015-11-25__de-us-20151125-q4-10k__469104.md"),
    (2016, "2016-10-30", 5902, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2017, "2017-10-29", 6594, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2018, "2018-10-28", 7165, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2019, "2019-11-03", 7567, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2020, "2020-11-01", 7298, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2021, "2021-10-31", 6988, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2022, "2022-10-30", 6623, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2023, "2023-10-29", 6917, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2024, "2024-10-27", 7451, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
    (2025, "2025-11-02", 7600, f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"),
]
for fy, pe, v, src in OPLEASE_FY:
    add("de_equipment_on_operating_leases_net_usdm", pe, fy, 4, "Deere & Company",
        "Equipment on operating leases - net (fiscal year end)", v, "USD_millions",
        "corpus", src, "10-year selected financial data / balance sheet")

OPLEASE_Q = [
    (2024, 1, "2024-01-28", 6751, f"{CORP}/filings/2024-02-15__de-us-20240215-q1-10q__105826.md"),
    (2024, 2, "2024-04-28", 6965, f"{CORP}/filings/2024-05-16__de-us-20240516-q2-10q__105820.md"),
    (2024, 3, "2024-07-28", 7118, f"{CORP}/filings/2024-08-15__de-us-20240815-q3-10q__105828.md"),
    (2025, 1, "2025-01-26", 7157, f"{CORP}/filings/2025-02-13__de-us-20250213-q1-10q__105832.md"),
    (2025, 2, "2025-04-27", 7336, f"{CORP}/filings/2025-05-15__de-us-20250515-q2-10q__105831.md"),
    (2025, 3, "2025-07-27", 7512, f"{CORP}/filings/2025-08-14__de-us-20250814-q3-10q__155834.md"),
    (2026, 1, "2026-02-01", 7512, f"{CORP}/filings/2026-02-26__de-us-20260226-q1-10q__636995.md"),
    (2026, 2, "2026-05-03", 7514, f"{CORP}/filings/2026-05-28__de-us-20260528-q2-10q__1055932.md"),
]
for fy, fq, pe, v, src in OPLEASE_Q:
    add("de_equipment_on_operating_leases_net_q_usdm", pe, fy, fq, "Deere & Company",
        "Equipment on operating leases - net (quarter end)", v, "USD_millions",
        "corpus", src, "Balance sheet; residual-risk-bearing asset base")

# B3. Lease revenues and sales-type / direct-finance lease residuals
K25 = f"{CORP}/filings/2025-11-26__de-us-20251126-q4-10k__469216.md"
for fy, pe, opv, tot in [(2023, "2023-10-29", 1312, 1493), (2024, "2024-10-27", 1403, 1610),
                         (2025, "2025-11-02", 1472, 1676)]:
    add("de_operating_lease_revenues_usdm", pe, fy, 4, "Deere & Company",
        "Operating lease revenues", opv, "USD_millions", "corpus", K25, "10-K lease note")
    add("de_total_lease_revenues_usdm", pe, fy, 4, "Deere & Company",
        "Total lease revenues", tot, "USD_millions", "corpus", K25, "10-K lease note")

for fy, pe, g, u in [(2024, "2024-10-27", 921, 55), (2025, "2025-11-02", 867, 40)]:
    add("de_salestype_lease_guaranteed_residual_usdm", pe, fy, 4, "Deere & Company",
        "Guaranteed residual values, sales-type & direct financing leases", g,
        "USD_millions", "corpus", K25, "10-K lease note")
    add("de_salestype_lease_unguaranteed_residual_usdm", pe, fy, 4, "Deere & Company",
        "Unguaranteed residual values, sales-type & direct financing leases", u,
        "USD_millions", "corpus", K25,
        "10-K lease note. Unguaranteed portion is the piece fully exposed to used-value declines.")

add("de_operating_lease_revenues_6m_usdm", "2026-05-03", 2026, 2, "Deere & Company",
    "Operating lease revenues, six months ended", 748, "USD_millions", "corpus",
    f"{CORP}/filings/2026-05-28__de-us-20260528-q2-10q__1055932.md",
    "vs 717 in the six months ended 2025-04-27 (+4.3% y/y)")
add("de_proceeds_from_sales_of_oplease_equipment_6m_usdm", "2026-05-03", 2026, 2, "Deere & Company",
    "Proceeds from sales of equipment on operating leases, six months ended", 1019,
    "USD_millions", "corpus", f"{CORP}/filings/2026-05-28__de-us-20260528-q2-10q__1055932.md",
    "vs 1,001 prior-year six months. Remarketing proceeds on lease returns - the direct "
    "channel through which used values hit Financial Services earnings.")
add("de_cost_of_oplease_equipment_acquired_6m_usdm", "2026-05-03", 2026, 2, "Deere & Company",
    "Cost of equipment on operating leases acquired, six months ended", 1295,
    "USD_millions", "corpus", f"{CORP}/filings/2026-05-28__de-us-20260528-q2-10q__1055932.md",
    "vs 1,254 prior-year six months")

# B4. Deere management's OWN quantified used-inventory disclosures (earnings calls)
#     value = percent change vs the stated reference point.
MGMT = [
    # (period_end, fy, fq, metric, value, notes, source)
    ("2025-01-26", 2025, 1, "Deere used combine inventory vs spring-2024 peak", -10.0,
     "'down over 10% from the recent peak in spring 2024 and is currently sitting at around 60% "
     "of the prior cycle peak'. Stated as 'over 10%' - recorded as -10.0 (a floor, not a point estimate).",
     f"{CORP}/call-transcripts/2025-02-13__de-us-20250213-call-q1-pres__46459.md"),
    ("2025-11-02", 2025, 4, "Deere MY2022-MY2023 8R used inventory vs Mar-2025 peak", -25.0,
     "'around 25% below the peak in March 2025'; also -mid-teens% sequentially in Q4 FY2025",
     f"{CORP}/call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md"),
    ("2025-11-02", 2025, 4, "Deere used combine inventory vs spring-2024 peak", -25.0,
     "'declined over 10% sequentially in our fourth quarter, resulting in a nearly 25% decrease "
     "from their spring 2024 peak'. Model-year distribution described as 'nearly normal'.",
     f"{CORP}/call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md"),
    ("2026-02-01", 2026, 1, "Deere used combine inventory vs Mar-2024 peak", -15.0,
     "'remain about 15% below their peak in March 2024, with model year distribution at a normal mix'. "
     "Note this is WORSE than the -25% reported for Q4 FY2025: a seasonal Q1 rebuild gave back ~10 pts.",
     f"{CORP}/call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md"),
    ("2026-02-01", 2026, 1, "Deere used high-horsepower tractor inventory vs Mar-2025 peak", -10.0,
     "'declined by over 10% from their March 2025 peak'; down mid-single digits sequentially in Q1 FY2026",
     f"{CORP}/call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md"),
    ("2026-02-01", 2026, 1, "Deere MY2022-MY2023 8R used inventory vs Mar-2025 peak", -40.0,
     "'down more than 40% in that same time period'; -20%+ sequentially in Q1 FY2026 alone. "
     "MY2024 8Rs down over 10% sequentially.",
     f"{CORP}/call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md"),
    ("2026-05-03", 2026, 2, "Deere used combine inventory vs Mar-2024 peak", -15.0,
     "'down by mid-teens from their March 2024 peak' - unchanged vs Q1 FY2026, i.e. combine used "
     "destock stalled during Q2 FY2026",
     f"{CORP}/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md"),
    ("2026-05-03", 2026, 2, "Deere used high-horsepower tractor inventory vs cycle peak", -15.0,
     "'down mid-teens from this cycle's peak and down low single digits sequentially during the "
     "quarter, which is a period that we typically see seasonal inventory builds'",
     f"{CORP}/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md"),
    ("2026-05-03", 2026, 2, "Deere MY2022-MY2023 8R used inventory vs peak a year earlier", -45.0,
     "'now down around 45% from their peak levels last year'",
     f"{CORP}/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md"),
    ("2026-05-03", 2026, 2, "Deere used sprayer inventory vs recent peak", -30.0,
     "'sprayer inventory down approximately 30% ... from recent peak levels'",
     f"{CORP}/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md"),
    ("2026-05-03", 2026, 2, "Deere used planter inventory vs recent peak", -50.0,
     "'planter inventory is down roughly 50% from recent peak levels'",
     f"{CORP}/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md"),
]
for pe, fy, fq, metric, v, note, src in MGMT:
    add("de_mgmt_used_inventory_vs_peak_pct", pe, fy, fq, "Deere & Company",
        metric, v, "percent", "corpus", src, note)

# B5. John Deere Financial "trade wholesale" - used equipment financed on dealer lots
add("de_jdf_trade_wholesale_portfolio_yoy_pct", "2026-05-03", 2026, 2, "John Deere Financial",
    "Trade wholesale portfolio (used equipment financed on dealer lots), y/y change", -15.0,
    "percent", "corpus", f"{CORP}/call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md",
    "'our trade wholesale, so that used equipment that's giving finance on the lots of dealers, "
    "is down over 15%, just in terms of the portfolio size'. Stated as 'over 15%' - recorded as "
    "-15.0, a floor. Direct measure of dealers' used-equipment carrying burden.")

# B6. Deere-disclosed US/Canada ag dealer NEW inventory as % of trailing-12m retail (context)
for pe, fy, fq, metric, v, note in [
    ("2026-04-30", 2026, 3, "US & Canada dealer new inventory, 100+hp 2WD tractors, % of trailing-12m retail", 30.0,
     "April 2026; prior-year April 2025 was 31%"),
    ("2026-04-30", 2026, 3, "US & Canada dealer new inventory, combines, % of trailing-12m retail", 12.0,
     "April 2026; prior-year April 2025 was 17% - combines destocked hard"),
]:
    add("de_dealer_new_inventory_pct_ttm_retail", pe, fy, fq, "Deere & Company",
        metric, v, "percent", "corpus",
        f"{CORP}/slides/2026-05-21__de-us-20260521-slide__1042212.md",
        note + ". NEW inventory - included as the counterpart to the used series.")

# ---------------------------------------------------------------------------
# C) FRED WPU111 - PPI new farm machinery & equipment (new-vs-used wedge)
# ---------------------------------------------------------------------------
if os.path.exists(FRED_CSV):
    with open(FRED_CSV) as fh:
        rdr = csv.DictReader(fh)
        hist = {}
        for r in rdr:
            d = r["observation_date"]
            try:
                val = float(r["WPU111"])
            except (ValueError, KeyError):
                continue
            hist[d] = val
        for d in sorted(hist):
            y, m, _ = (int(x) for x in d.split("-"))
            pe = eom(y, m)
            fy, fq = fiscal_of_month(y, m)
            add("fred_wpu111_ppi_farm_machinery", pe, fy, fq, "US PPI",
                "PPI: farm machinery & equipment (NEW equipment, index 1982=100)",
                round(hist[d], 3), "index", "web",
                "https://fred.stlouisfed.org/graph/fredgraph.csv?id=WPU111",
                "New-equipment producer prices. Contrast with used asking/auction values "
                "to size the new-vs-used price wedge.")
            prev = f"{y-1:04d}-{m:02d}-01"
            if prev in hist:
                add("fred_wpu111_ppi_farm_machinery_yoy_pct", pe, fy, fq, "US PPI",
                    "PPI: farm machinery & equipment, y/y change", round((hist[d] / hist[prev] - 1) * 100, 2),
                    "percent", "web",
                    "https://fred.stlouisfed.org/graph/fredgraph.csv?id=WPU111",
                    "Computed from WPU111 monthly index.")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(HEADER)
    w.writerows(rows)

print(f"wrote {len(rows)} rows to {OUT}")
