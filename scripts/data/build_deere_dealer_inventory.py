#!/usr/bin/env python3
"""
Build the Deere dealer-inventory time series (US & Canada Ag, units as a % of
trailing-12-month retail sales) from the offline corpus of earnings-call slide
decks, plus management commentary from the call transcripts.

Sources: challenge/offline-data/deere/slides/*.md and call-transcripts/*.md

Two-stage design:
  1. CURATED  - the observation table below, each row carrying the corpus file it
     was read from. Curation is necessary because the markdown conversion of the
     older decks (2015-2016, and the 2020-2023 decks that render the inventory
     block as loose lines rather than a table) scrambles character order inside
     the dealer-inventory table.
  2. VERIFY   - for every deck whose dealer-inventory block survived conversion as
     a clean markdown table, re-parse it from disk and assert the curated value
     matches. Any mismatch is a hard failure. This covers 30 of the 46 decks.

Output: tidy long CSV.
"""

import csv
import os
import re
import sys
from collections import defaultdict

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/dealer_inventory.csv"

HEADER = [
    "series_id", "period_end", "fiscal_year", "fiscal_quarter", "entity",
    "metric", "value", "units", "source_type", "source", "notes",
]

# Deere fiscal year ends late Oct / early Nov. The retail-sales month shown on each
# deck maps to the fiscal quarter the deck reports.
MONTH_TO_FQ = {1: ("Q1", 0), 4: ("Q2", 0), 7: ("Q3", 0), 10: ("Q4", 0)}
MONTH_END = {1: "01-31", 4: "04-30", 7: "07-31", 10: "10-31"}

DECK = {  # retail month -> corpus slide path (the deck that first printed it)
    (2015, 1): "slides/2015-02-20__de-us-20150220-slide__469336.md",
    (2015, 4): "slides/2015-05-22__de-us-20150522-slide__469418.md",
    (2015, 7): "slides/2015-08-21__de-us-20150821-slide__469412.md",
    (2015, 10): "slides/2015-11-25__de-us-20151125-slide__468542.md",
    (2016, 1): "slides/2016-02-19__de-us-20160219-slide__469335.md",
    (2016, 4): "slides/2016-05-20__de-us-20160520-slide__469364.md",
    (2016, 7): "slides/2016-08-19__de-us-20160819-slide__469401.md",
    (2016, 10): "slides/2016-11-23__de-us-20161123-slide__468519.md",
    (2017, 1): "slides/2017-02-17__de-us-20170217-slide__469324.md",
    (2017, 4): "slides/2017-05-19__de-us-20170519-slide__469652.md",
    (2017, 7): "slides/2017-08-18__de-us-20170818-slide__469828.md",
    (2017, 10): "slides/2017-11-22__de-us-20171122-slide__469640.md",
    (2018, 1): "slides/2018-02-16__de-us-20180216-slide__468566.md",
    (2018, 4): "slides/2018-05-18__de-us-20180518-slide__469458.md",
    (2018, 7): "slides/2018-08-17__de-us-20180817-slide__468505.md",
    (2018, 10): "slides/2018-11-21__de-us-20181121-slide__469934.md",
    (2019, 1): "slides/2019-02-15__de-us-20190215-slide__469639.md",
    (2019, 4): "slides/2019-05-17__de-us-20190517-slide__469810.md",
    (2019, 7): "slides/2019-08-16__de-us-20190816-slide__469630.md",
    (2019, 10): "slides/2019-11-27__de-us-20191127-slide__469403.md",
    (2020, 1): "slides/2020-02-21__de-us-20200221-slide__469359.md",
    (2020, 4): "slides/2020-05-21__de-us-20200521-slide__469383.md",
    (2020, 7): "slides/2020-08-20__de-us-20200820-slide__46433.md",
    (2020, 10): "slides/2020-11-25__de-us-20201125-slide__46418.md",
    (2021, 1): "slides/2021-02-19__de-us-20210219-slide__46421.md",
    (2021, 4): "slides/2021-05-21__de-us-20210521-slide__46479.md",
    (2021, 7): "slides/2021-08-20__de-us-20210820-slide__46481.md",
    (2021, 10): "slides/2021-11-24__de-us-20211124-slide__46437.md",
    (2022, 1): "slides/2022-02-18__de-us-20220218-slide__46449.md",
    (2022, 4): "slides/2022-05-20__de-us-20220520-slide__46463.md",
    (2022, 7): "slides/2022-08-19__de-us-20220819-slide__46460.md",
    (2022, 10): "slides/2022-11-23__de-us-20221123-slide__46423.md",
    (2023, 1): "slides/2023-02-17__de-us-20230217-slide__46447.md",
    (2023, 4): "slides/2023-05-19__de-us-20230519-slide__46428.md",
    (2023, 7): "slides/2023-08-18__de-us-20230818-slide__46427.md",
    (2023, 10): "slides/2023-11-22__de-us-20231122-slide__46466.md",
    (2024, 1): "slides/2024-02-15__de-us-20240215-slide__46430.md",
    (2024, 4): "slides/2024-05-16__de-us-20240516-slide__46443.md",
    (2024, 7): "slides/2024-08-15__de-us-20240815-slide__46457.md",
    (2024, 10): "slides/2024-11-21__de-us-20241121-slide__46477.md",
    (2025, 1): "slides/2025-02-13__de-us-20250213-slide__46456.md",
    (2025, 4): "slides/2025-05-15__de-us-20250515-slide__46462.md",
    (2025, 7): "slides/2025-08-15__de-us-20250815-slide__143404.md",
    (2025, 10): "slides/2025-11-26__de-us-20251126-slide__361243.md",
    (2026, 1): "slides/2026-02-19__de-us-20260219-slide__603088.md",
    (2026, 4): "slides/2026-05-21__de-us-20260521-slide__1042212.md",
}

CAT = {
    "2wd_100hp": "de_dealer_inv_pct_ttm_2wd_100hp",
    "4wd": "de_dealer_inv_pct_ttm_4wd",
    "combines": "de_dealer_inv_pct_ttm_combines",
}

# ---------------------------------------------------------------------------
# CURATED OBSERVATIONS
# (year, month, category, value, source_key, note)
#   source_key "own"  -> the contemporaneous deck printed it as the current year
#   source_key (y, m) -> read from a LATER deck's prior-year comparative column
# ---------------------------------------------------------------------------
OBS = [
    # ---- 2WD tractors 100+ PTO hp (labelled "Row-Crop Tractors" before 3Q2015) ----
    (2013, 1, "2wd_100hp", 18, (2015, 1), "two-years-prior column of the Jan-2015 deck's 3-year table; labelled Row-Crop Tractors"),
    (2014, 1, "2wd_100hp", 19, (2015, 1), "prior-year column; labelled Row-Crop Tractors"),
    (2014, 4, "2wd_100hp", 18, (2015, 4), "prior-year column; labelled Row-Crop Tractors"),
    (2014, 7, "2wd_100hp", 25, (2015, 7), "prior-year column"),
    (2015, 1, "2wd_100hp", 24, "own", "labelled Row-Crop Tractors"),
    (2015, 4, "2wd_100hp", 23, "own", "deck table OCR-scrambled; value corroborated by prior-year column of the Apr-2016 deck"),
    (2015, 7, "2wd_100hp", 25, "own", "deck table OCR-scrambled; corroborated by prior-year column of the Jul-2016 deck"),
    (2015, 10, "2wd_100hp", 24, (2016, 10), "Oct-2015 deck table unreadable after conversion; taken from the Oct-2016 deck prior-year column"),
    (2016, 1, "2wd_100hp", 29, "own", "deck table OCR-scrambled; prior-year cell 24% matches the Jan-2015 print"),
    (2016, 4, "2wd_100hp", 37, "own", "deck table OCR-scrambled; prior-year cell 23% matches the Apr-2015 print"),
    (2016, 7, "2wd_100hp", 37, "own", "deck table OCR-scrambled; prior-year cell 25% matches the Jul-2015 print"),
    (2016, 10, "2wd_100hp", 31, "own", "deck table OCR-scrambled; prior-year cell 24% is the Oct-2015 value"),
    (2017, 1, "2wd_100hp", 38, "own", ""),
    (2017, 4, "2wd_100hp", 32, "own", ""),
    (2017, 7, "2wd_100hp", 31, "own", ""),
    (2017, 10, "2wd_100hp", 25, "own", ""),
    (2018, 1, "2wd_100hp", 33, "own", ""),
    (2018, 4, "2wd_100hp", 39, "own", ""),
    (2018, 7, "2wd_100hp", 37, "own", ""),
    (2018, 10, "2wd_100hp", 32, "own", ""),
    (2019, 1, "2wd_100hp", 38, "own", ""),
    (2019, 4, "2wd_100hp", 44, "own", "cycle peak for this series in the corpus"),
    (2019, 7, "2wd_100hp", 41, "own", "Jul-2020 deck later shows this comparative as 42%"),
    (2019, 10, "2wd_100hp", 27, "own", ""),
    (2020, 1, "2wd_100hp", 31, "own", "Jan-2021 deck later shows this comparative as 32%"),
    (2020, 4, "2wd_100hp", 33, "own", ""),
    (2020, 7, "2wd_100hp", 32, "own", ""),
    (2020, 10, "2wd_100hp", 21, "own", ""),
    (2021, 1, "2wd_100hp", 28, "own", ""),
    (2021, 4, "2wd_100hp", 25, "own", ""),
    (2021, 7, "2wd_100hp", 21, "own", ""),
    (2021, 10, "2wd_100hp", 12, "own", "corpus low; post-COVID supply constraint"),
    (2022, 1, "2wd_100hp", 15, "own", ""),
    (2022, 4, "2wd_100hp", 22, "own", ""),
    (2022, 7, "2wd_100hp", 24, "own", ""),
    (2022, 10, "2wd_100hp", 18, "own", ""),
    (2023, 1, "2wd_100hp", 25, "own", ""),
    (2023, 4, "2wd_100hp", 29, "own", ""),
    (2023, 7, "2wd_100hp", 30, "own", ""),
    (2023, 10, "2wd_100hp", 23, "own", ""),
    (2024, 1, "2wd_100hp", 30, "own", ""),
    (2024, 4, "2wd_100hp", 31, "own", ""),
    (2024, 7, "2wd_100hp", 31, "own", "management on the 3Q24 call: 'if you look at 100+, we're around 30%-31% inventory-to-sales ratio'"),
    (2024, 10, "2wd_100hp", 24, "own", ""),
    (2025, 1, "2wd_100hp", 34, "own", ""),
    (2025, 4, "2wd_100hp", 31, "own", ""),
    (2025, 7, "2wd_100hp", 31, "own", ""),
    (2025, 10, "2wd_100hp", 23, "own", ""),
    (2026, 1, "2wd_100hp", 27, "own", ""),
    (2026, 4, "2wd_100hp", 30, "own", "VERIFIED ANCHOR; prior-year comparative on the same deck is 31%"),

    # ---- Combines ----
    (2013, 1, "combines", 10, (2015, 1), "two-years-prior column of the Jan-2015 deck's 3-year table"),
    (2014, 1, "combines", 10, (2015, 1), "prior-year column"),
    (2014, 4, "combines", 14, (2015, 4), "prior-year column"),
    (2014, 7, "combines", 18, (2015, 7), "prior-year column; rendered '81%' by the OCR, digits transposed"),
    (2014, 10, "combines", 6, (2015, 10), "prior-year column of a badly scrambled table; LOW CONFIDENCE"),
    (2015, 1, "combines", 10, "own", ""),
    (2015, 4, "combines", 17, "own", "corroborated by prior-year column of the Apr-2016 deck"),
    (2015, 7, "combines", 19, "own", "rendered '91%' by the OCR; 19% confirmed by prior-year column of the Jul-2016 deck"),
    (2015, 10, "combines", 6, "own", "scrambled table; the Oct-2016 deck's comparative is ambiguous between 5% and 6%. LOW CONFIDENCE"),
    (2016, 1, "combines", 10, "own", "scrambled table; prior-year cell 10% matches the Jan-2015 print"),
    (2016, 4, "combines", 13, "own", "scrambled table; prior-year cell 17% matches the Apr-2015 print"),
    (2016, 7, "combines", 20, "own", "scrambled table; prior-year cell 19% is the Jul-2015 value"),
    (2016, 10, "combines", 5, (2017, 10), "Oct-2016 deck cell scrambled; 5% taken from the clean Oct-2017 deck prior-year column"),
    (2017, 1, "combines", 14, "own", ""),
    (2017, 4, "combines", 21, "own", ""),
    (2017, 7, "combines", 26, "own", ""),
    (2017, 10, "combines", 5, "own", ""),
    (2018, 1, "combines", 16, "own", ""),
    (2018, 4, "combines", 23, "own", ""),
    (2018, 7, "combines", 25, "own", ""),
    (2018, 10, "combines", 8, "own", ""),
    (2019, 1, "combines", 19, "own", ""),
    (2019, 4, "combines", 23, "own", ""),
    (2019, 7, "combines", 36, "own", "cycle peak for combines in the corpus"),
    (2019, 10, "combines", 9, "own", ""),
    (2020, 1, "combines", 15, "own", ""),
    (2020, 4, "combines", 22, "own", ""),
    (2020, 7, "combines", 28, "own", ""),
    (2020, 10, "combines", 4, "own", ""),
    (2021, 1, "combines", 12, "own", ""),
    (2021, 4, "combines", 22, "own", ""),
    (2021, 7, "combines", 23, "own", ""),
    (2021, 10, "combines", 3, "own", "corpus low"),
    (2022, 1, "combines", 7, "own", ""),
    (2022, 4, "combines", 17, "own", ""),
    (2022, 7, "combines", 25, "own", ""),
    (2022, 10, "combines", 6, "own", ""),
    (2023, 1, "combines", 16, "own", ""),
    (2023, 4, "combines", 23, "own", ""),
    (2023, 7, "combines", 17, "own", ""),
    (2023, 10, "combines", 4, "own", ""),
    (2024, 1, "combines", 16, "own", ""),
    (2024, 4, "combines", 15, "own", ""),
    (2024, 7, "combines", 22, "own", ""),
    (2024, 10, "combines", 4, "own", "management 4Q24 call confirms 'finished the year at 4% inventory to sales'"),
    (2025, 1, "combines", 11, "own", "management 1Q25 call: '11% inventory to sales for combines ... a little lower than normal'"),
    (2025, 4, "combines", 17, "own", ""),
    (2025, 7, "combines", 26, "own", ""),
    (2025, 10, "combines", 8, "own", "management 4Q25 call confirms combines closed the year at 8%"),
    (2026, 1, "combines", 18, "own", ""),
    (2026, 4, "combines", 12, "own", "VERIFIED ANCHOR; prior-year comparative on the same deck is 17%"),

    # ---- 4WD tractors (disclosed only intermittently on the slide) ----
    (2016, 1, "4wd", 23, (2017, 1), "prior-year column"),
    (2016, 7, "4wd", 27, (2017, 7), "prior-year column"),
    (2017, 1, "4wd", 27, "own", ""),
    (2017, 7, "4wd", 24, "own", ""),
    (2017, 10, "4wd", 21, (2018, 10), "prior-year column"),
    (2018, 4, "4wd", 25, (2019, 4), "prior-year column"),
    (2018, 10, "4wd", 27, "own", "the Oct-2019 deck later shows this comparative as 22% - unreconciled restatement"),
    (2019, 4, "4wd", 26, "own", ""),
    (2019, 10, "4wd", 20, "own", ""),
    (2022, 10, "4wd", 19, (2023, 10), "prior-year column"),
    (2023, 10, "4wd", 21, "own", ""),
]

# Management-stated inventory-to-sales ratios from the call transcripts.
# NOTE: the "220 hp and above" series is a NARROWER, Deere-internal cut than the
# AEM-based "100+ PTO hp" slide series and runs materially lower. Kept separate.
MGMT = [
    ("de_dealer_inv_pct_ttm_220hp_plus", "2023-10-31", 2023, "Q4", 15,
     "call-transcripts/2024-05-16__de-us-20240516-call-qna__46474.md",
     "'row crop tractors were about 15% inventory to sales as we close out 2023'; 4Q24 call repeats 15%"),
    ("de_dealer_inv_pct_ttm_220hp_plus", "2024-10-31", 2024, "Q4", 10,
     "call-transcripts/2024-11-21__de-us-20241121-call-q4-pres__46452.md",
     "'year end inventory to sales ratio of 10%, a 500 basis point reduction year over year'; only twice this low in 10 yrs (Apr-2014, Jan-2022)"),
    ("de_dealer_inv_pct_ttm_220hp_plus", "2025-07-31", 2025, "Q3", 20,
     "call-transcripts/2025-08-15__de-us-20250815-call-q3-qna__143409.md",
     "'right around 20% inventory to sales ... exactly the same year over year'; APPROXIMATE ('right around')"),
    ("de_dealer_inv_pct_ttm_220hp_plus", "2025-10-31", 2025, "Q4", 12,
     "call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md",
     "'220 horsepower and above tractors were at 12%'; absolute units the lowest in over 17 years"),
    ("de_dealer_inv_pct_ttm_4wd", "2025-10-31", 2025, "Q4", 8,
     "call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md",
     "'inventory-to-sales ratios for combines and four-wheel drive tractors both closed the year at 8%'; 4WD absent from the Oct-2025 slide table"),
    ("de_dealer_inv_pct_ttm_2wd_100hp", "2024-07-31", 2024, "Q3", 70,
     "call-transcripts/2024-08-15__de-us-20240815-call-qna__46445.md",
     "INDUSTRY EX-DEERE comparator: 'if you look at 100+, we're around 30%-31% ... I think the industry ex Deere is closer to 70%'; APPROXIMATE"),
]

# New-equipment field inventory, absolute units, y/y or vs peak. Different metric.
UNITS = [
    ("de_field_inv_units_yoy_pct", "2025-07-31", 2025, "Q3", -45, "Deere NA Ag 220+hp tractors",
     "call-transcripts/2025-08-15__de-us-20250815-call-q3-pres__143406.md",
     "'220 horsepower and above tractor inventories are 45% lower year over year'"),
    ("de_field_inv_units_yoy_pct", "2025-07-31", 2025, "Q3", -25, "Deere NA Ag combines",
     "call-transcripts/2025-08-15__de-us-20250815-call-q3-pres__143406.md",
     "'combine inventories are down 25%'"),
    ("de_field_inv_units_yoy_pct", "2025-07-31", 2025, "Q3", -30, "Deere NA Small Ag tractors <100hp",
     "call-transcripts/2025-08-15__de-us-20250815-call-q3-pres__143406.md",
     "'less than 100 horsepower tractor inventory in North America is down 30% year over year'"),
    ("de_field_inv_units_vs_peak_pct", "2026-04-30", 2026, "Q2", -50, "Deere NA Ag high-hp tractors and combines",
     "call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md",
     "'down more than 50% from their mid-2024 peak, with inventory to sales ratios in line with historical averages'; at-least magnitude"),
    ("de_field_inv_units_yoy_pct", "2026-01-31", 2026, "Q1", -40, "Deere NA Small Ag tractors (<100hp and 100-220hp)",
     "call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md",
     "'each about 40% lower year-over-year'"),
    ("de_used_inv_vs_peak_pct", "2026-01-31", 2026, "Q1", -15, "Deere NA used combines",
     "call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md",
     "'about 15% below their peak in March 2024'"),
    ("de_used_inv_vs_peak_pct", "2026-04-30", 2026, "Q2", -45, "Deere NA used MY2022-23 8R tractors",
     "call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md",
     "'down around 45% from their peak levels last year'"),
    ("de_used_inv_vs_peak_pct", "2026-04-30", 2026, "Q2", -30, "Deere NA used sprayers",
     "call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md",
     "'sprayer inventory down approximately 30%'"),
    ("de_used_inv_vs_peak_pct", "2026-04-30", 2026, "Q2", -50, "Deere NA used planters",
     "call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md",
     "'planter inventory is down roughly 50% from recent peak levels'"),
]


def fiscal_year(y, m):
    """Deere FY ends late Oct. Jan/Apr/Jul/Oct retail month -> FY of the deck."""
    return y  # Jan-2026 deck is 1Q FY2026; Oct-2025 deck is 4Q FY2025.


# ---------------------------------------------------------------------------
# VERIFICATION: re-parse decks whose block survived as a clean markdown table
# ---------------------------------------------------------------------------
ROW_PATTERNS = [
    (re.compile(r"2WD\s*Tractors.*?100\+\s*PTO\s*hp", re.I | re.S), "2wd_100hp"),
    (re.compile(r"Row-Crop\s*Tractors", re.I), "2wd_100hp"),
    (re.compile(r"4WD\s*Tractors", re.I), "4wd"),
    (re.compile(r"Combines", re.I), "combines"),
]


def verify():
    """Re-parse clean tables from disk; assert curated values match."""
    curated = {(y, m, c): v for (y, m, c, v, s, n) in OBS}
    checked, failed = 0, []
    for (y, m), rel in sorted(DECK.items()):
        path = os.path.join(CORPUS, rel)
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        # locate the "Deere Dealer Inventories" anchor
        anchor = None
        for i, ln in enumerate(lines):
            if re.search(r"Deere Dealer Inventories", ln, re.I):
                anchor = i
                break
        if anchor is None:
            continue
        for ln in lines[anchor:anchor + 8]:
            if not ln.strip().startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            label = cells[0]
            cat = None
            for pat, c in ROW_PATTERNS:
                if pat.search(label):
                    cat = c
                    break
            if cat is None:
                continue
            # first numeric percent cell after the label = current-year value
            nums = []
            for c in cells[1:]:
                mm = re.fullmatch(r"\$?(\d{1,2})%\$?", c.replace(" ", ""))
                if mm:
                    nums.append(int(mm.group(1)))
            if not nums:
                continue
            got = nums[0]
            key = (y, m, cat)
            if key not in curated:
                failed.append(f"{rel}: parsed {cat}={got}% for {y}-{m:02d} but no curated row")
                continue
            checked += 1
            if curated[key] != got:
                failed.append(
                    f"{rel}: {cat} {y}-{m:02d} parsed {got}% != curated {curated[key]}%")
    return checked, failed


def main():
    checked, failed = verify()
    print(f"verify: {checked} slide-table values re-parsed and matched")
    if failed:
        print("VERIFY FAILURES:", file=sys.stderr)
        for f in failed:
            print("  " + f, file=sys.stderr)
        sys.exit(1)

    rows = []
    for (y, m, cat, val, src, note) in OBS:
        fq, _ = MONTH_TO_FQ[m]
        if src == "own":
            key = (y, m)
        else:
            key = src
        rel = DECK[key]
        rows.append({
            "series_id": CAT[cat],
            "period_end": f"{y}-{MONTH_END[m]}",
            "fiscal_year": fiscal_year(y, m),
            "fiscal_quarter": fq,
            "entity": "Deere US & Canada Ag dealers",
            "metric": "dealer_inventory_units_pct_of_ttm_retail",
            "value": val,
            "units": "percent",
            "source_type": "slide",
            "source": rel,
            "notes": note,
        })

    for (sid, pe, fy, fq, val, src, note) in MGMT:
        entity = ("Industry ex-Deere US & Canada Ag dealers"
                  if "INDUSTRY EX-DEERE" in note else "Deere US & Canada Ag dealers")
        rows.append({
            "series_id": sid, "period_end": pe, "fiscal_year": fy,
            "fiscal_quarter": fq, "entity": entity,
            "metric": "dealer_inventory_units_pct_of_ttm_retail",
            "value": val, "units": "percent", "source_type": "call-transcript",
            "source": src, "notes": note,
        })

    for (sid, pe, fy, fq, val, entity, src, note) in UNITS:
        rows.append({
            "series_id": sid, "period_end": pe, "fiscal_year": fy,
            "fiscal_quarter": fq, "entity": entity,
            "metric": ("used_field_inventory_units_change" if "used" in sid
                       else "new_field_inventory_units_change"),
            "value": val, "units": "percent", "source_type": "call-transcript",
            "source": src, "notes": note,
        })

    rows.sort(key=lambda r: (r["series_id"], r["period_end"], r["entity"]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {OUT}")

    by = defaultdict(int)
    for r in rows:
        by[r["series_id"]] += 1
    for k, v in sorted(by.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
