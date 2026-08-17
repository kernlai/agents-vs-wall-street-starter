#!/usr/bin/env python3
"""
Build dealer_network.csv: Deere dealer-network STRUCTURE and consolidation dynamics.

Corpus rows are parsed from the 10-K Item 1 distribution paragraph
(see parse_deere_dealer_network.py for the extraction + reconciliation proof).
Non-corpus rows are transcribed from the cited public sources.

Missing / undisclosed values are emitted as BLANK, never zero, never a guess.
Private dealer groups that do not publish financials get an explicit
"not disclosed" row so the absence is on the record rather than inferred.
"""

import csv
import os
import re
import glob

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/dealer_network.csv"

HEADER = [
    "series_id", "period_end", "fiscal_year", "fiscal_quarter", "entity",
    "metric", "value", "units", "source_type", "source", "notes",
]

# Deere fiscal year-end dates (52/53-week year ending late Oct / early Nov).
FYE = {
    2015: "2015-11-01", 2016: "2016-10-30", 2017: "2017-10-29", 2018: "2018-10-28",
    2019: "2019-11-03", 2020: "2020-11-01", 2021: "2021-10-31", 2022: "2022-10-30",
    2023: "2023-10-29", 2024: "2024-10-27", 2025: "2025-11-02",
}

PARA_RE = re.compile(
    r"(?:Through (?:these )?(?:the )?U\.S\.(?: and)? (?:and )?Canad(?:a|ian)[^.]*?"
    r"markets? products to approximately[^\n]{0,2500})", re.IGNORECASE)
FIELDS = {
    "total": re.compile(r"approximately ([\d,]+) (?:independent )?dealer locations", re.I),
    "ag": re.compile(r"approximately ([\d,]+) sell agricultural equipment", re.I),
    "cf": re.compile(r"approximately ([\d,]+) sell construction", re.I),
    "rb": re.compile(r"approximately ([\d,]+) roadbuilding-only locations", re.I),
    "turf": re.compile(r"about ([\d,]+) turf-only locations", re.I),
}


def parse_10k_series():
    out = {}
    for path in sorted(glob.glob(os.path.join(CORPUS, "filings", "*10k*.md"))):
        txt = open(path, encoding="utf-8", errors="replace").read()
        base = os.path.basename(path)
        y, mo = int(base[:4]), int(base[5:7])
        fy = y if mo >= 11 else y - 1
        best = None
        for m in PARA_RE.finditer(txt):
            chunk = txt[m.start(): m.start() + 2500]
            cand = {}
            for k, rx in FIELDS.items():
                mm = rx.search(chunk)
                cand[k] = int(mm.group(1).replace(",", "")) if mm else None
            score = sum(1 for v in cand.values() if v is not None)
            if best is None or score > best[0]:
                best = (score, cand)
        if best is None:
            continue
        if fy in out and sum(1 for v in out[fy][1].values() if v is not None) >= best[0]:
            continue
        out[fy] = (os.path.relpath(path, CORPUS), best[1])
    return out


def corpus_rows():
    rows = []
    series = parse_10k_series()
    # FY2015-FY2017 headline total INCLUDES turf-only locations; FY2018+ excludes them.
    # Proven by exact reconciliation: FY2017 1,532+424+403 = 2,359 = reported total.
    for fy in sorted(series):
        src, c = series[fy]
        pe = FYE[fy]
        basis = ("includes turf-only locations (pre-FY2018 definition)"
                 if fy <= 2017 else "excludes turf-only and roadbuilding-only locations")
        specs = [
            ("deere_dealer_loc_us_ca_total_reported", c["total"],
             "dealer_locations_us_canada_total_as_reported",
             f"As-reported headline count; definition {basis}. NOT comparable across FY2017/FY2018 break."),
            ("deere_dealer_loc_us_ca_ag", c["ag"],
             "dealer_locations_us_canada_selling_ag_equipment",
             "Locations selling agricultural equipment."),
            ("deere_dealer_loc_us_ca_cf", c["cf"],
             "dealer_locations_us_canada_selling_construction_forestry",
             "Locations selling construction/earthmoving/material handling/roadbuilding/forestry."),
            ("deere_dealer_loc_us_ca_turf_only", c["turf"],
             "dealer_locations_us_canada_turf_only",
             "Turf-only locations; many also carry non-Deere lines."),
            ("deere_dealer_loc_us_ca_roadbuilding_only", c["rb"],
             "dealer_locations_us_canada_roadbuilding_only",
             "First disclosed FY2021 (post-Wirtgen channel build-out)."),
        ]
        for sid, val, metric, note in specs:
            if val is None:
                continue
            rows.append([sid, pe, fy, "FY", "Deere & Company", metric, val,
                         "count", "filing", src, note])
        if c["ag"] is not None and c["cf"] is not None:
            rows.append([
                "deere_dealer_loc_us_ca_core_ag_cf", pe, fy, "FY", "Deere & Company",
                "dealer_locations_us_canada_ag_plus_cf_restated", c["ag"] + c["cf"],
                "count", "derived", src,
                "DERIVED = ag + C&F locations. The only consistently-defined total across "
                "FY2015-FY2025; strips the FY2018 turf-only definitional break."])
    return rows


# ---------------------------------------------------------------------------
# Non-10-K rows. Each carries its own full citation.
# ---------------------------------------------------------------------------
T_BR = "call-transcripts/2025-06-10__de-us-20250610-call-pres-2__469351.md"
T_JDF = "call-transcripts/2025-12-08__de-us-20251208-call-pres-2__384036.md"
T_Q2 = "call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md"
Q2_10Q = "filings/2026-05-21__de-us-20260521-q2-10q__1055929.md"
Q1_10Q = "filings/2026-02-19__de-us-20260219-q1-10q__648937.md"
K25 = "filings/2025-11-26__de-us-20251126-q4-10k__469216.md"

PIRG = "https://publicinterestnetwork.org/wp-content/uploads/2022/02/Deere-In-The-Headlights-II.pdf"
FE100 = "https://www.farm-equipment.com/articles/25326-2026-update-shows-numerous-shifts-among-north-americas-largest-dealer-groups"
FE10 = "https://www.nationalbeefwire.com/farm-equipment-magazine-reports-the-10-largest-machinery-dealers"
RDO_TN = "https://www.realagriculture.com/2026/07/rdo-announces-deal-to-acquire-true-north-john-deere-dealerships/"
TZP = "https://www.tractorzoompro.com/podcasts/market-insights-for-july-2026"
MBCO = "https://www.manitobacooperator.ca/news-opinion/news/john-deere-dealer-chains-enns-bros-greenvalley-equipment-call-off-merger-competition-bureau/"
FTC = "https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-states-secure-settlement-deere-company-advancing-farmers-right-repair"
FRESH = "https://www.freshfields.com/en/our-thinking/blogs/a-fresh-take/ftcs-john-deere-settlement-signals-scrutiny-of-aftermarket-repair-restrictions-102nbqo"
NALC = "https://nationalaglawcenter.org/john-deere-agrees-to-settle-antitrust-lawsuit/"
UPS = "https://upstream.ag/p/2026-ag-equipment-dealer-business-outlook-trends-report-highlights-and-analysis"
FE26 = "https://www.farm-equipment.com/articles/25370-dealers-forecasting-2026-sales-revenue-down-4"
SAND = "https://www.tractorhouse.com/blog/sandhills-news/2026/07/2026-q2-dealer-survey-farm-equipment-sentiment-weakens"
SCRAPE = "https://www.scrapehero.com/location-reports/John%20Deere-USA/"

EXTRA = [
    # ---- non-US/Canada network scale -------------------------------------
    ["deere_dealer_loc_brazil", "2025-06-10", 2025, "Q2", "Deere & Company",
     "dealer_locations_brazil", 275, "count", "transcript", T_BR,
     "'over 275 unique locations'; floor value, stated at Brazil investor day 10 Jun 2026-fiscal-2025. "
     "Deere says this 'nearly tripled over the past 20 years' (slide: 2.7x, 2004-2024)."],
    ["deere_dealer_loc_brazil_growth_multiple", "2025-06-10", 2025, "Q2", "Deere & Company",
     "dealer_location_growth_multiple_brazil_2004_2024", 2.7, "ratio", "slide",
     "slides/2025-06-10__de-us-20250610-slide__46442.md",
     "Deere Brazil dealer locations 2004-2024. Companion slide metric: avg dealer revenue 12.8x 2014-2024 "
     "(>11%/yr). Absolute 2004 base NOT disclosed - do not back-solve as exact."],
    ["deere_jdf_dealers_served_global", "2025-12-08", 2026, "Q1", "John Deere Financial",
     "dealers_served_by_john_deere_financial_global", 1500, "count", "transcript", T_JDF,
     "'about a million customers who we serve through 1,500 dealers', JDF investor day 8 Dec 2025. "
     "Counts dealer ENTITIES/organisations financed by JDF globally, not locations. "
     "Best available proxy for global dealer-group count; Deere does not disclose a group count in filings."],

    # ---- US consolidation structure (third-party census) ------------------
    ["deere_us_ag_dealer_locations_pirg", "2022-02-01", "", "", "Deere & Company",
     "us_ag_dealership_locations_third_party_census", 1357, "count", "web", PIRG,
     "U.S. PIRG Education Fund, 'Deere in the Headlights II', Feb 2022. US ONLY (10-K figure is US+Canada). "
     "Collected from Deere's own dealer locator."],
    ["deere_us_ag_loc_share_in_chains_7plus", "2022-02-01", "", "", "Deere & Company",
     "share_of_us_ag_locations_in_chains_of_7plus_stores", 82, "percent", "web", PIRG,
     "Most consolidated of the four majors studied (Deere, Case IH, AGCO, Kubota). "
     "18 of the 20 largest chains in the US service Deere equipment."],
    ["deere_us_ag_avg_chain_size", "2022-02-01", "", "", "Deere & Company",
     "average_sites_per_us_deere_dealer_chain", 8, "count", "web", PIRG,
     "'The average Deere chain has about 8 sites'; largest chain network 67 locations. "
     "Comparators: largest Case IH chain 57, AGCO 31, Kubota 6."],
    ["deere_us_ag_largest_chain_size", "2022-02-01", "", "", "Deere & Company",
     "locations_in_largest_us_deere_dealer_chain", 67, "count", "web", PIRG, ""],
    ["deere_us_ag_dealer_groups_derived", "2022-02-01", "", "", "Deere & Company",
     "implied_number_of_us_deere_ag_dealer_groups", 170, "count", "derived", PIRG,
     "DERIVED, APPROXIMATE. PIRG states one Deere chain per 12,018 farms and per 5.3m acres of US farmland; "
     "~2.0m US farms/12,018 = ~166 and ~897m acres/5.3m = ~169. Also 1,357 locations / ~8 sites = ~170. "
     "Three independent routes converge on ~170 US Deere ag dealer GROUPS in early 2022. "
     "Deere itself never publishes a group count - treat as order-of-magnitude, not exact."],
    ["deere_us_all_locations_scraped", "2026-08-10", "", "", "Deere & Company",
     "us_deere_branded_dealer_locations_scraped", 2240, "count", "web", SCRAPE,
     "ScrapeHero location census, collected 10 Aug 2026, US only, 51 states/territories, 1,679 cities. "
     "NOT comparable to the 10-K count: scrapes every Deere-branded storefront incl. turf-only and "
     "small-format outlets. Directional cross-check only."],

    # ---- largest dealer groups (trade press; private companies) -----------
    ["top100_dealer_groups_ag_stores", "2026-05-01", "", "", "North America ag dealer channel",
     "ag_stores_operated_by_100_largest_dealer_groups", 2001, "count", "web", FE100,
     "Farm Equipment / Ag Equipment Intelligence 2026 update (4th annual), published ~May 2026. "
     "DOWN 11 stores vs the 2025 report; ~1/3 of all ag equipment rooftops in North America. "
     "All brands, not Deere-only."],
    ["top100_dealer_groups_ag_stores", "2025-05-01", "", "", "North America ag dealer channel",
     "ag_stores_operated_by_100_largest_dealer_groups", 2012, "count", "derived", FE100,
     "DERIVED = 2,001 + 11, from the 2026 update's stated year-over-year change of -11 stores. "
     "The 2025 report's own figure was not independently retrieved."],
    ["dealer_group_locations", "2024-06-01", "", "", "United Ag & Turf",
     "ag_store_locations", 97, "count", "web", FE10,
     "Deere dealer. Farm Equipment 'Largest Machinery Dealers', June 2024. Rank 1 in NA by ag store count. "
     "HQ Waco, TX. Revenue banded '>$2B' by the trade press - PRIVATE company, not an audited disclosure."],
    ["dealer_group_locations", "2024-06-01", "", "", "Ag-Pro Companies",
     "ag_store_locations", 84, "count", "web", FE10,
     "Deere dealer. Rank 2. HQ Boston, GA. Revenue banded '>$2B' by trade press; PRIVATE, unaudited."],
    ["dealer_group_locations", "2024-06-01", "", "", "Pape Machinery (Pape)",
     "ag_store_locations", 48, "count", "web", FE10,
     "Deere dealer. Rank 5. HQ Eugene, OR. Revenue banded '$1-1.5B' by trade press; PRIVATE, unaudited. "
     "Ag stores only - the wider Pape group also runs Deere construction/forestry outlets."],
    ["dealer_group_locations", "2024-06-01", "", "", "Van Wall Equipment",
     "ag_store_locations", 33, "count", "web", FE10,
     "Deere dealer. Rank 10. HQ Perry, IA. Revenue banded '$1-1.5B' by trade press; PRIVATE, unaudited."],
    ["dealer_group_locations", "2024-06-01", "", "", "AgriVision / PrairieLand",
     "ag_store_locations", 32, "count", "web", FE10,
     "Deere dealer. Rank 8. HQ Winterset, IA. Revenue banded '$1-1.5B'; PRIVATE, unaudited."],
    ["dealer_group_locations", "2024-06-01", "", "", "Hutson Inc.",
     "ag_store_locations", 30, "count", "web", FE10,
     "Deere dealer. Rank 4. HQ Murray, KY. Revenue banded '$1-1.5B'; PRIVATE, unaudited."],
    ["dealer_group_locations", "2024-06-01", "", "", "James River Equipment",
     "ag_store_locations", 28, "count", "web", FE10,
     "Deere dealer. Rank 7. HQ Ashland, VA. Revenue banded '$1-1.5B'; PRIVATE, unaudited."],
    ["dealer_group_locations", "2024-06-01", "", "", "Sloan Implement",
     "ag_store_locations", 26, "count", "web", FE10,
     "Deere dealer. Rank 9. HQ Assumption, IL. Revenue banded '$1-1.5B'; PRIVATE, unaudited."],
    ["dealer_group_locations", "2024-06-01", "", "", "Titan Machinery (TITN)",
     "ag_store_locations", 71, "count", "web", FE10,
     "CNH Industrial (Case IH / New Holland) dealer - NOT a Deere dealer. Rank 3. Included ONLY as the "
     "single listed ag-channel comparator; its results are a CNH signal, not a Deere signal."],
    ["dealer_group_locations", "2024-06-01", "", "", "Rocky Mountain Equipment",
     "ag_store_locations", 42, "count", "web", FE10,
     "CNH (Case IH / New Holland) dealer, Calgary AB - NOT a Deere dealer. Rank 6."],
    ["dealer_group_locations", "2026-07-07", 2026, "Q3", "RDO Equipment Co.",
     "ag_store_locations_post_true_north", 42, "count", "web", RDO_TN,
     "Deere dealer. Ag locations after the True North acquisition (8 added). RDO runs >85 total "
     "locations across 12 states incl. construction/forestry. PRIVATE - no audited financials. "
     "Revenue figures circulating on data-broker sites are unverified estimates and are NOT recorded here."],
    ["deere_top8_group_share_of_ag_locations", "2024-06-01", "", "", "Deere & Company",
     "share_of_deere_us_ca_ag_locations_held_by_8_largest_deere_groups", 23.6, "percent", "derived", FE10,
     "DERIVED = (97+84+48+33+32+30+28+26) = 378 ag stores held by the 8 Deere groups in Farm Equipment's "
     "NA top 10, over the FY2024 10-K's ~1,600 US+Canada Deere ag locations. Understates true "
     "concentration: RDO and other large Deere groups sit outside that top-10 ag ranking."],

    # ---- private groups with genuinely no public financials ---------------
    ["dealer_group_financials_disclosed", "2026-08-16", 2026, "Q3", "RDO Equipment Co.",
     "audited_financial_statements_public", "", "boolean", "derived", "",
     "NOT DISCLOSED. Private company; no SEC filings. Do not attribute revenue/headcount."],
    ["dealer_group_financials_disclosed", "2026-08-16", 2026, "Q3", "Ag-Pro Companies",
     "audited_financial_statements_public", "", "boolean", "derived", "",
     "NOT DISCLOSED. Private company; no SEC filings."],
    ["dealer_group_financials_disclosed", "2026-08-16", 2026, "Q3", "Van Wall Equipment",
     "audited_financial_statements_public", "", "boolean", "derived", "",
     "NOT DISCLOSED. Private company; no SEC filings."],
    ["dealer_group_financials_disclosed", "2026-08-16", 2026, "Q3", "Sydenstricker Nobbe Partners",
     "audited_financial_statements_public", "", "boolean", "derived", "",
     "NOT DISCLOSED. Private Deere dealer group (MO/IL). No public location count retrieved either; "
     "did not appear in the Farm Equipment NA top-10 ag ranking."],
    ["dealer_group_financials_disclosed", "2026-08-16", 2026, "Q3", "Hutson Inc.",
     "audited_financial_statements_public", "", "boolean", "derived", "",
     "NOT DISCLOSED. Private company; no SEC filings."],
    ["dealer_group_financials_disclosed", "2026-08-16", 2026, "Q3", "Ziegler Companies",
     "audited_financial_statements_public", "", "boolean", "derived", "",
     "NOT DISCLOSED. Private; primarily a CATERPILLAR dealer, also Deere ag in parts of the upper Midwest. "
     "No location count verified for its Deere ag operations."],
    ["dealer_group_financials_disclosed", "2026-08-16", 2026, "Q3", "Papé Group",
     "audited_financial_statements_public", "", "boolean", "derived", "",
     "NOT DISCLOSED. Private company; no SEC filings."],
    ["dealer_group_financials_disclosed", "2026-08-16", 2026, "Q3", "Brandt Tractor / Brandt Group (Canada)",
     "audited_financial_statements_public", "", "boolean", "derived", "",
     "NOT DISCLOSED. Private. Acquired Cervus Equipment in 2021, removing the last listed pure-play "
     "Deere dealer; Cervus filings remain useful only for the pre-2021 period."],
    ["listed_pureplay_deere_dealer_exists", "2026-08-16", 2026, "Q3", "North America",
     "public_pureplay_deere_dealer_count", 0, "count", "derived", "",
     "Structural constraint, not missing data: there is genuinely NO listed pure-play North American "
     "Deere dealer after Brandt acquired Cervus Equipment in 2021. Titan Machinery is CNH, not Deere."],

    # ---- 2025-2026 dealer M&A / distress events --------------------------
    ["dealer_ma_locations_transferred", "2026-08-03", 2026, "Q3", "RDO Equipment / True North Equipment",
     "deere_ag_locations_changing_ownership", 8, "count", "web", RDO_TN,
     "Announced 7 Jul 2026, targeted close 3 Aug 2026, subject to Deere approval. ~200 employees. "
     "Locations: Grand Forks/Grafton/Northwood ND; Thief River Falls/Warren/Kennedy/Mahnomen/Baudette MN. "
     "Trade press characterises True North as an established, NOT distressed, group."],
    ["dealer_ma_locations_transferred", "2026-11-30", 2026, "Q4", "Horizon Ag & Turf / Battle River Implements",
     "deere_locations_in_combined_entity", 17, "count", "web", TZP,
     "Alberta, Canada. Merger effective 30 Nov 2026; Battle River locations rebrand to Horizon. "
     "Described as strategic (footprint + back-office scale), neither party distressed."],
    ["dealer_ma_abandoned_locations", "2026-05-01", 2026, "Q2", "Enns Bros. / Greenvalley Equipment",
     "deere_locations_in_abandoned_merger", 13, "count", "web", MBCO,
     "Manitoba, Canada. Announced mid-Jan 2026; Competition Bureau review opened 23 Jan 2026; file closed "
     "1 May 2026 as ABANDONED by the parties after 'considerable roadblocks and delays'. "
     "First evidence in this dataset of an antitrust ceiling on Deere dealer consolidation."],
    ["deere_dealer_bankruptcies_identified", "2026-08-16", 2026, "Q3", "Deere dealer network (North America)",
     "publicly_reported_deere_dealer_bankruptcies_2025_2026", "", "count", "derived", "",
     "NOT ESTABLISHED. Targeted searches surfaced NO reported Deere dealer bankruptcy, liquidation or "
     "involuntary closure in 2025-2026. Absence of evidence, not evidence of absence: private dealer "
     "insolvencies are frequently unreported. Recorded as blank, not zero."],

    # ---- dealer economics / sentiment (channel condition) ----------------
    ["dealer_profitability_vs_peak", "2026-07-01", 2026, "Q3", "North America ag dealer channel",
     "dealer_profitability_decline_from_peak", -30, "percent", "web", TZP,
     "Tractor Zoom Pro market insights, July 2026: dealer profitability at a five-year low, ~30% below peak; "
     "new machinery sales down 15-20% at most OEMs. All-brand channel estimate, not a Deere disclosure."],
    ["dealer_share_forecasting_profit", "2026-01-10", 2026, "Q1", "North America ag dealer channel",
     "share_of_dealers_forecasting_a_profitable_year", 72.5, "percent", "web", UPS,
     "Ag Equipment Intelligence 2026 Dealer Business Outlook (pub. 10 Jan 2026), for calendar 2025: "
     "'the lowest over the last 5 years by a significant margin'. All brands."],
    ["dealer_revenue_forecast_2026", "2026-01-10", 2026, "Q1", "North America ag dealer channel",
     "forecast_2026_dealer_sales_revenue_change", -4, "percent", "web", FE26,
     "Ag Equipment Intelligence / Farm Equipment 2026 Dealer Business Outlook. All brands."],
    ["dealer_revenue_forecast_2026_deere", "2026-01-10", 2026, "Q1", "Deere dealers (North America)",
     "forecast_2026_dealer_sales_revenue_change_deere_dealers", -7, "percent", "web", FE26,
     "DEERE DEALERS SPECIFICALLY forecast the LARGEST decline of any brand's dealers (-7% vs -4% all-brand). "
     "Directly upstream of Deere wholesale shipments; a dealer planning -7% orders less."],
    ["dealer_net_saying_new_inventory_too_high", "2026-01-10", 2026, "Q1", "North America ag dealer channel",
     "net_share_of_dealers_reporting_new_equipment_inventory_too_high", 42, "percent", "web", UPS,
     "Used-equipment equivalent 27%. All brands, survey taken around Jan 2026."],
    ["dealer_share_expecting_price_increases", "2026-01-10", 2026, "Q1", "North America ag dealer channel",
     "share_of_dealers_expecting_oem_price_increases_in_2026", 98.6, "percent", "web", UPS,
     "Majority expect +1% to +6%."],
    ["dealer_share_conditions_worsened_qoq", "2026-07-01", 2026, "Q3", "North America ag dealer channel",
     "share_of_dealers_reporting_worsening_market_conditions_qoq", 50, "percent", "web", SAND,
     "Sandhills Global / Bloomberg Intelligence Q2 2026 dealer survey, published July 2026: 'nearly 50%'. "
     "Sentiment took another leg down in Q2 2026; 57% expect conditions unchanged over the next 12 months. "
     "Sample size not published. This is the most recent dealer-sentiment read before Deere's Q3 print."],
    ["jdf_trade_wholesale_portfolio_change", "2026-05-03", 2026, "Q2", "John Deere Financial",
     "used_equipment_wholesale_financing_portfolio_yoy_change", -15, "percent", "transcript", T_Q2,
     "Q2 FY2026 call, 21 May 2026: 'our trade wholesale, so that used equipment that's giving finance on the "
     "lots of dealers, is down over 15%... That's less on their balance sheets that they've freed up.' "
     "Floor value ('over 15%'). Direct evidence dealer balance sheets are DE-levering, not stressing."],

    # ---- right to repair -------------------------------------------------
    ["deere_legal_accrual_total", "2026-02-01", 2026, "Q1", "Deere & Company",
     "total_accrued_losses_unresolved_legal_matters", 175, "USD_millions", "filing", Q1_10Q,
     "Includes the multidistrict class action antitrust settlement accrued in Q4 FY2025."],
    ["deere_legal_accrual_total", "2026-05-03", 2026, "Q2", "Deere & Company",
     "total_accrued_losses_unresolved_legal_matters", 175, "USD_millions", "filing", Q2_10Q,
     "Unchanged from Q1 FY2026. The $99m class-action settlement sits inside this $175m. "
     "Q2 FY2026 10-Q gives no separate FTC accrual: 'unable to estimate the potential impact'."],
    ["deere_rtr_class_action_settlement", "2026-04-06", 2026, "Q2", "Deere & Company",
     "right_to_repair_class_action_settlement_amount", 99, "USD_millions", "web", NALC,
     "Proposed settlement 6 Apr 2026 of the consolidated MDL filed Oct 2022. Defendants are Deere AND ITS "
     "AFFILIATED DEALERSHIPS. Plus interest at 3.95%/yr from 15 Jan 2026. Class = purchasers of repair "
     "services for Deere large ag equipment from Deere or authorised dealers, 10 Jan 2018 to preliminary "
     "approval. Accrued by Deere in Q4 FY2025, so it does NOT hit Q3 FY2026 earnings."],
    ["deere_ftc_settlement_term", "2026-07-08", 2026, "Q3", "Deere & Company",
     "ftc_right_to_repair_order_duration", 10, "years", "web", FTC,
     "FTC + AGs of AZ, IL, MI, MN, WI, announced 8 Jul 2026, N.D. Ill. Deere must give farmers and "
     "independent repair providers the SAME repair resources (incl. software) as authorised dealers, on "
     "'fair and reasonable terms'. Four-year post-expiration enforcement window (Freshfields, 13 Jul 2026: "
     + FRESH + ")."],
    ["deere_ftc_settlement_dealer_rollout_trigger", "2026-07-08", 2026, "Q3", "Deere & Company",
     "dealer_network_penetration_triggering_mandatory_ird_access", 50, "percent", "web", FRESH,
     "Once a repair resource reaches MORE THAN 50% of Deere dealer locations, equivalent access must be "
     "extended to farmers and independent repair providers. Compounding: every future dealer tool becomes "
     "a channel-wide obligation, so dealers lose exclusivity on tooling on a rolling basis."],
    ["deere_ftc_settlement_payment_to_states", "2026-07-08", 2026, "Q3", "Deere & Company",
     "payment_to_plaintiff_states_for_litigation_costs", 1, "USD_millions", "web", FTC,
     "De minimis relative to the $99m class settlement. The FTC order's cost to Deere is behavioural, "
     "not monetary."],
    ["deere_ftc_settlement_dealer_nonretaliation", "2026-07-08", 2026, "Q3", "Deere dealer network",
     "dealers_barred_from_retaliating_against_self_repair_customers", 1, "boolean", "web", FRESH,
     "Authorised dealers must PROMOTE the availability of repair resources and cannot 'discriminate or "
     "retaliate in any way, including in the sales, financing, or servicing' against customers who "
     "self-repair or use an independent provider. This is an obligation placed on DEALERS, not just Deere."],
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = corpus_rows() + EXTRA
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for r in rows:
            assert len(r) == len(HEADER), r
            w.writerow(r)
    print(f"wrote {len(rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
