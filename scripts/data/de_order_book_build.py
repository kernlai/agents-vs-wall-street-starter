#!/usr/bin/env python3
"""
Stage 3: build the tidy long CSV /data/deere/de_order_book.csv

Every row is hand-adjudicated from a verbatim transcript sentence (the exact
words are carried in `notes` together with the transcript path). Nothing is
imputed: where management did not say something, there is no row.

Coverage-month figures are DERIVED from the wording plus the call date and the
Deere fiscal calendar (Q1 ends ~early Feb, Q2 ~early May, Q3 ~early Aug,
Q4 ~late Oct/early Nov). The derivation is written into the notes so a reader
can disagree with it. Where the wording is qualitative only ("healthy",
"strong") no month value is recorded.
"""
import csv, os, json, statistics as st

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_order_book.csv"
CORPUS_REL = "challenge/offline-data/deere/"
HDR = ["series_id","period_end","fiscal_year","fiscal_quarter","segment","component",
       "value","units","source","notes"]

rows = []

def _units_for(series_id, component):
    if series_id.endswith("_pct") or "pct" in component:
        return "pct"
    if series_id.endswith("_flag") or "flag" in component or "rank" in series_id:
        return "flag_1_yes"
    if "month" in series_id or "month" in component:
        return "months"
    return "count"

def add(series_id, period_end, fy, fq, segment, *rest):
    """Two accepted shapes:
       (component, value, units, source, notes)   -- fully explicit
       (value, component, source, notes)          -- units inferred from names
    """
    if len(rest) == 5:
        component, value, units, source, notes = rest
    elif len(rest) == 4:
        value, component, source, notes = rest
        units = _units_for(series_id, component)
    else:
        raise TypeError(f"bad arity {len(rest)} for {series_id}")
    rows.append(dict(series_id=series_id, period_end=period_end, fiscal_year=fy,
                     fiscal_quarter=fq, segment=segment, component=component,
                     value=value, units=units, source=source, notes=notes))

T = "call-transcripts/"

# ---------------------------------------------------------------------------
# A. FORWARD ORDER COVERAGE STATED AT EACH Q2 CALL  (the core series)
#    "at the Q2 call, what did management say about the following Q3?"
#    coverage_months = months from call date to the stated far edge of the book.
# ---------------------------------------------------------------------------
# (call_date, fy, seg, months_or_None, covers_q3_flag, quote, file)
Q2CALLS = [
 ("2013-05-15", 2013, "PPA_large_ag_NA", None, 1,
  "The order book does remain pretty strong... As you look at the tractor, certainly the order book on eights and nines are further out.",
  T+"2013-05-15__de-us-20130515-call-qna__1530347.md",
  "qualitative only; EOP for the U.S. described as 'for all practical purposes, sold out'"),
 ("2014-05-14", 2014, "PPA_large_ag_NA", 5.0, 1,
  "Our order book, we often talk about where we're at from an availability perspective, and we would tell you on 8Rs, our order availability is into October.",
  T+"2014-05-14__de-us-20140514-call-qna__1526780.md",
  "'into October' from 2014-05-14 = ~5.0 months forward; FY2014 ended 2014-11-02, so book covers all of Q3 and most of Q4"),
 ("2015-05-22", 2015, "PPA_large_ag_NA", None, 1,
  "Certainly combines at this point in the year with the early order program, we're well over 90% covered, and the bigger question tends to be things like large tractors.",
  T+"2015-05-22__de-us-20150522-call-qna__1521782.md",
  "combines >90% covered at Q2 call; large tractors explicitly the looser element"),
 ("2017-05-19", 2017, "PPA_large_ag_NA", None, 1,
  "We talked about in the first quarter, our order books are really quite strong, and they continued to be strong through the second quarter... That order book actually has strengthened pretty significantly over the quarter.",
  T+"2017-05-19__de-us-20170519-call-qna__1479659.md",
  "qualitative; same call: 'Our early order program accounts for over 90% of that in any given year'"),
 ("2018-05-18", 2018, "PPA_large_ag_NA", 5.0, 1,
  "Similarly, our large tractor order book now extends into October.",
  T+"2018-05-18__de-us-20180518-call-pres-2__1475345.md",
  "'into October' from 2018-05-18 = ~4.9 months; FY2018 ended 2018-10-28"),
 ("2019-05-17", 2019, "PPA_large_ag_NA", 3.0, 1,
  "With order books extending into the fourth quarter, the division is on track for a solid finish to the year.",
  T+"2019-05-17__de-us-20190517-call-pres-2__1392890.md",
  "'into the fourth quarter'; FY2019 Q4 began ~2019-07-29, so >=2.4 months forward and all of Q3 covered"),
 ("2020-05-21", 2020, "PPA_large_ag_NA", 3.0, 1,
  "Specifically, order programs for combines and crop care are completed, while large tractor order books extend into the fourth quarter, roughly 90% full.",
  T+"2020-05-21__de-us-20200521-call-pres-2__1143269.md",
  "COVID year; same call: 'the remainder of our 2020 production schedule is largely backed by customer orders through either our early order programs or rolling order books'"),
 ("2021-05-21", 2021, "PPA_large_ag_NA", 5.3, 1,
  "Given the positive environmental backdrop, order activity is up significantly and all of our Large Ag order banks are now complete through the end of the fiscal year.",
  T+"2021-05-21__de-us-20210521-call-pres__46476.md",
  "'complete through the end of the fiscal year' from 2021-05-21; FY2021 ended 2021-10-31 = 5.3 months. 4WD/8R already taking FY2022 orders with visibility through H1 FY22"),
 ("2022-05-20", 2022, "PPA_large_ag_NA", 5.4, 1,
  "At this time, our order book extends through the duration of fiscal 2022 and even into early fiscal 2023 for some product lines.",
  T+"2022-05-20__de-us-20220520-call-pres__46444.md",
  "FY2022 ended 2022-10-30 = 5.4 months; some lines beyond"),
 ("2023-05-19", 2023, "PPA_large_ag_NA", 5.4, 1,
  "As we look ahead to the rest of 2023, we see robust demand with our order books providing excellent visibility through the end of the year.",
  T+"2023-05-19__de-us-20230519-call-pres__46451.md",
  "FY2023 ended 2023-10-29 = 5.4 months"),
 ("2024-05-16", 2024, "PPA_large_ag_NA", None, 1,
  "Demand shifts, coupled with proactive inventory management, are reflected in our production schedules for the balance of the fiscal year, with many product lines anticipating retail demand under production to close out 2024.",
  T+"2024-05-16__de-us-20240516-call-pres__46458.md",
  "no explicit months for large ag; H2 production plan explicitly SET at the Q2 call (deliberate underproduction), i.e. shipments pre-determined by Deere's own decision"),
 ("2025-05-15", 2025, "PPA_large_ag_NA", 5.0, 1,
  "Turning to order books, availability for both North American-produced large tractors and European-produced mid-sized tractors is into October.",
  T+"2025-05-15__de-us-20250515-call-pres__46417.md",
  "'into October' from 2025-05-15 = ~5.0 months; FY2025 ended 2025-11-02"),
 ("2026-05-21", 2026, "PPA_large_ag_NA", 4.0, 1,
  "Regarding Waterloo large tractors, order books are well into the fourth quarter as we look to close out our model year 2026 production.",
  T+"2026-05-21__de-us-20260521-call-pres__1042774.md",
  "'well into the fourth quarter' from 2026-05-21; FY2026 Q4 begins ~2026-08-03 and ends ~2026-11-01, so ~4 months forward. Q3 FY2026 (ends ~2026-08-02) is fully inside the book"),
]
for date, fy, seg, months, covq3, quote, path, note in Q2CALLS:
    if months is not None:
        add("de_order_coverage_months", date, fy, 2, seg, "forward_order_coverage",
            months, "months", path,
            f'"{quote}" | derivation: {note}')
    add("de_q2call_covers_next_q3_flag", date, fy, 2, seg, "q3_covered_by_order_book",
        covq3, "flag_1_yes", path, f'"{quote}"')

# --- other segments at the Q2 call (segment differentiation) ---
add("de_order_coverage_months","2025-05-15",2025,2,"PPA_south_america",2.5,"months",
    T+"2025-05-15__de-us-20250515-call-pres__46417.md",
    '"In Brazil, our order books are full through the third quarter." | Q3 FY2025 ended 2025-07-27 = ~2.4 months forward from the call')
add("de_order_coverage_months","2026-05-21",2026,2,"PPA_europe",3.0,"months",
    T+"2026-05-21__de-us-20260521-call-pres__1042774.md",
    '"Order visibility in both regions now extends through the third quarter and into the fourth." (Europe and South America) | Q3 FY2026 ends ~2026-08-02; "into the fourth" implies ~3 months forward')
add("de_order_coverage_months","2026-05-21",2026,2,"PPA_south_america",3.0,"months",
    T+"2026-05-21__de-us-20260521-call-pres__1042774.md",
    '"Order visibility in both regions now extends through the third quarter and into the fourth."')
add("de_order_coverage_months","2024-05-16",2024,2,"CF_earthmoving",4.0,"months",
    T+"2024-05-16__de-us-20240516-call-pres__46458.md",
    '"Our guide is also supported by an order book for earthmoving equipment that extends out approximately four months into the fourth quarter." | explicit 4 months')
add("de_order_coverage_months","2024-08-15",2024,3,"CF_earthmoving",2.0,"months",
    T+"2024-08-15__de-us-20240815-call-pres__46429.md",
    '"With roughly two months of order visibility in this segment, we are confident in our ability to execute our plan." | explicit ~2 months for North American construction')
add("de_order_coverage_pct_slots","2026-05-21",2026,2,"CF_NA",80.0,"pct_of_fy_production_slots_filled",
    T+"2026-05-21__de-us-20260521-call-pres__1042774.md",
    '"our order book continues to strengthen, up more than 60% since November, now at its highest level since April of 2024, with over 80% of production slots filled for the year."')
add("de_order_book_yoy_pct","2026-05-21",2026,2,"CF_NA",60.0,"pct_increase_since_november",
    T+"2026-05-21__de-us-20260521-call-pres__1042774.md",
    '"our order book continues to strengthen, up more than 60% since November" | NOT year-over-year: growth since the start of FY2026')
add("de_order_coverage_months","2026-02-19",2026,1,"PPA_europe",4.5,"months",
    T+"2026-02-19__de-us-20260219-call-pres__605076.md",
    '"European tractor order books are currently 4-5 months out, while South American orders are full through our second quarter." | midpoint of 4-5')
add("de_order_coverage_months","2026-02-19",2026,1,"PPA_south_america",2.5,"months",
    T+"2026-02-19__de-us-20260219-call-pres__605076.md",
    '"South American orders are full through our second quarter." | Q2 FY2026 ended ~2026-05-03')
add("de_order_coverage_months","2026-02-19",2026,1,"PPA_large_ag_NA",5.5,"months",
    T+"2026-02-19__de-us-20260219-call-pres__605076.md",
    '"large tractor order velocity for the North American market has picked up, and our rolling order books now provide visibility into the fourth quarter." | at the Q1 call (2026-02-19) the NA rolling book ALREADY reached past Q3 into Q4 FY2026')
add("de_order_coverage_months","2024-02-15",2024,1,"CF_compact",5.5,"months",
    T+"2024-02-15__de-us-20240215-call-pres__46480.md",
    '"our order books, which for construction and forestry are full through the second quarter across most product lines, with compact construction equipment notably full through the end of the third quarter."')
add("de_order_coverage_months","2024-02-15",2024,1,"CF_NA",2.5,"months",
    T+"2024-02-15__de-us-20240215-call-pres__46480.md",
    '"order books ... for construction and forestry are full through the second quarter across most product lines"')

# --- explicit statements that SAT / turf / compact have the LEAST visibility ---
add("de_order_visibility_rank","2014-05-14",2014,2,"SAT",0,"flag_1_less_visibility_than_large_ag",
    T+"2014-05-14__de-us-20140514-call-qna__1526780.md",
    '"On small ag versus large, just as a broad statement, our order book would not be as far out and never, rarely would be versus the large." | value 0 = materially shorter visibility than PPA large ag')
add("de_order_visibility_rank","2017-08-18",2017,3,"SAT",0,"flag_1_less_visibility_than_large_ag",
    T+"2017-08-18__de-us-20170818-call-qna__1478901.md",
    '"We don\'t tend to get that kind of visibility on small Ag."')
add("de_order_visibility_rank","2025-05-15",2025,2,"SAT_turf_compact",0,"flag_1_less_visibility_than_large_ag",
    T+"2025-05-15__de-us-20250515-call-pres__46417.md",
    '"It\'s worth noting that we have less order visibility in turf equipment and compact utility tractors."')
add("de_order_visibility_rank","2020-05-21",2020,2,"CF",0,"flag_1_less_visibility_than_large_ag",
    T+"2020-05-21__de-us-20200521-call-pres-2__1143269.md",
    '"Other products have lower levels of visibility as they do not operate off early order programs and tend to be driven to a larger extent by general economic trends such as housing starts, the price of oil, levels of GDP"')
add("de_order_visibility_rank","2020-05-21",2020,2,"PPA",1,"flag_1_less_visibility_than_large_ag",
    T+"2020-05-21__de-us-20200521-call-pres-2__1143269.md",
    '"certain products, like those subject to our early order programs, operate on more of a sold-ahead basis, and we have higher visibility to demand in those areas." | value 1 = high visibility')

# ---------------------------------------------------------------------------
# B. EARLY ORDER PROGRAM MECHANICS -- how far ahead orders are placed
# ---------------------------------------------------------------------------
# EOP share of annual production for the seasonal lines
for date, fy, fq, v, quote, path in [
 ("2017-02-17",2017,1,90.0,"Certainly, that combine early order program, in most years is 90-plus % of our annual production.",T+"2017-02-17__de-us-20170217-call-qna__1480475.md"),
 ("2017-05-19",2017,2,90.0,"Our early order program accounts for over 90% of that in any given year.",T+"2017-05-19__de-us-20170519-call-qna__1479659.md"),
 ("2023-05-19",2023,2,90.0,"Typically, we source about 90% of model year 2024 planters and sprayers through the early order program.",T+"2023-05-19__de-us-20230519-call-qna__46469.md"),
 ("2024-02-15",2024,1,90.0,"With nearly 90% of orders sourced through our combine, sprayer, and planter early order programs, we have significant visibility into the balance of the year for those product lines.",T+"2024-02-15__de-us-20240215-call-pres__46480.md"),
 ("2015-05-22",2015,2,90.0,"Certainly combines at this point in the year with the early order program, we're well over 90% covered.",T+"2015-05-22__de-us-20150522-call-qna__1521782.md"),
]:
    add("de_eop_share_of_production_pct", date, fy, fq, "PPA_seasonal", "eop_share_of_annual_production",
        v, "pct", path, f'"{quote}" | value is a floor: management says "over"/"nearly" 90%')

# EOP calendar -> lead time to delivery. Anchored on the most explicit statements.
EOPCAL = [
 ("sprayers","2025-08-15",2025,3,"open_month",5,
  "The EOP for sprayers opened in mid May and actually closes today.",T+"2025-08-15__de-us-20250815-call-q3-pres__143406.md"),
 ("sprayers","2025-08-15",2025,3,"close_month",8,
  "The EOP for sprayers opened in mid May and actually closes today.",T+"2025-08-15__de-us-20250815-call-q3-pres__143406.md"),
 ("planters","2025-08-15",2025,3,"open_month",6,
  "Planner EOP opened at the June and will close at the September.",T+"2025-08-15__de-us-20250815-call-q3-pres__143406.md"),
 ("planters","2025-08-15",2025,3,"close_month",9,
  "Planner EOP opened at the June and will close at the September.",T+"2025-08-15__de-us-20250815-call-q3-pres__143406.md"),
 ("combines","2025-08-15",2025,3,"open_month",8,
  "Lastly, Combine EOP just opened at the August and will run through the December.",T+"2025-08-15__de-us-20250815-call-q3-pres__143406.md"),
 ("combines","2025-08-15",2025,3,"close_month",12,
  "Lastly, Combine EOP just opened at the August and will run through the December.",T+"2025-08-15__de-us-20250815-call-q3-pres__143406.md"),
 ("sprayers","2026-05-21",2026,2,"open_month",5,
  "We opened up at the beginning of May. It'll run through the end of August.",T+"2026-05-21__de-us-20260521-call-qna__1042775.md"),
 ("sprayers","2026-05-21",2026,2,"close_month",8,
  "We opened up at the beginning of May. It'll run through the end of August.",T+"2026-05-21__de-us-20260521-call-qna__1042775.md"),
 ("planters","2026-05-21",2026,2,"open_month",6,
  "Planters will be kind of a one month lag of that, opening up at the beginning of June and running through the end of September.",T+"2026-05-21__de-us-20260521-call-qna__1042775.md"),
 ("planters","2026-05-21",2026,2,"close_month",9,
  "Planters will be kind of a one month lag of that, opening up at the beginning of June and running through the end of September.",T+"2026-05-21__de-us-20260521-call-qna__1042775.md"),
 ("combines","2025-11-26",2025,4,"close_month",12,
  "our combine EOP, which closes in Mid-December, is projected to fall within our guided range for the industry.",T+"2025-11-26__de-us-20251126-call-q4-pres-2__361265.md"),
 ("combines","2022-11-23",2022,4,"open_month",8,
  "We opened North American Combine EOP back in August.",T+"2022-11-23__de-us-20221123-call-pres__46446.md"),
 ("combines","2023-08-18",2023,3,"open_month",8,
  "Our combine early order program just opened at the beginning of this month and has gotten off to a nice start, but it remains too early to extrapolate any data points for 2024 as the program will continue through the end of November.",T+"2023-08-18__de-us-20230818-call-pres__46455.md"),
 ("combines","2023-08-18",2023,3,"close_month",11,
  "the program will continue through the end of November",T+"2023-08-18__de-us-20230818-call-pres__46455.md"),
 ("crop_care","2022-05-20",2022,2,"open_month",6,
  "we will have our early order programs open up for crop care in early June, which is fairly typical for our planters and sprayers.",T+"2022-05-20__de-us-20220520-call-qna__46464.md"),
 ("crop_care","2021-05-21",2021,2,"open_month",6,
  "We'll open our early order program for planters and sprayers in June, which will yield some additional data points on demand for 2022.",T+"2021-05-21__de-us-20210521-call-pres__46476.md"),
 ("crop_care","2019-11-27",2019,4,"close_month",10,
  "the final phase of the planter and sprayer EOP concluded in October with mixed results on a unit basis.",T+"2019-11-27__de-us-20191127-call-pres-2__1347447.md"),
 ("crop_care","2018-11-21",2018,4,"close_month",9,
  "In September, the final phase of the planter and sprayer early order program concluded, with orders up mid-single digits over 2018.",T+"2018-11-21__de-us-20181121-call-pres-2__1441802.md"),
 ("combines","2017-11-22",2017,4,"close_month",1,
  "Our combine early order program, it will end in January",T+"2017-11-22__de-us-20171122-call-qna__1478009.md"),
 ("combines","2025-02-13",2025,1,"close_month",1,
  "Our combine early order program closed a couple of weeks ago and compared to last year's EOP was down more than our industry guide.",T+"2025-02-13__de-us-20250213-call-q1-pres__46459.md"),
]
for line, date, fy, fq, comp, v, quote, path in EOPCAL:
    add("de_eop_calendar_month", date, fy, fq, "PPA_"+line, comp, v, "calendar_month_1_12",
        path, f'"{quote}"')

# EOP duration and derived lead time to the use season
add("de_eop_duration_months","2022-11-23",2022,4,"PPA_combines",5.5,"normal_eop_open_duration",
    T+"2022-11-23__de-us-20221123-call-pres__46446.md",
    '"That\'s noteworthy because we normally have the EOP open for five to six months." | midpoint of 5-6 months')
add("de_eop_lead_months_order_to_delivery","2026-05-21",2026,2,"PPA_sprayers",9.5,"months_eop_open_to_use_season",
    T+"2026-05-21__de-us-20260521-call-qna__1042775.md",
    'DERIVED: MY2027 sprayer EOP opens May 2026 and closes end-Aug 2026 ("We opened up at the beginning of May. It\'ll run through the end of August."); production runs "in the last few months of the fiscal year" (Aug-Oct 2026); delivery ahead of the spring 2027 use season (Mar-May 2027). May-2026 order to ~Apr-2027 use = ~11 months; Aug-2026 close to ~Apr-2027 = ~8 months. Value = midpoint of the open-to-use and close-to-use interval, 9.5 months')
add("de_eop_lead_months_order_to_delivery","2026-05-21",2026,2,"PPA_planters",9.0,"months_eop_open_to_use_season",
    T+"2026-05-21__de-us-20260521-call-qna__1042775.md",
    'DERIVED: MY2027 planter EOP opens Jun-2026, closes end-Sep-2026; planting season Apr-May 2027. Open-to-use ~10 months, close-to-use ~7 months; midpoint 9.0')
add("de_eop_lead_months_order_to_delivery","2025-08-15",2025,3,"PPA_combines",11.0,"months_eop_open_to_use_season",
    T+"2025-08-15__de-us-20250815-call-q3-pres__143406.md",
    'DERIVED: MY2026 combine EOP opens Aug-2025 and runs to Dec-2025 ("Combine EOP just opened at the August and will run through the December"); combines are delivered for the following autumn harvest (Aug-Oct 2026). Open-to-use ~12-14 months, close-to-use ~8-10 months; value = 11.0 as the central estimate')
add("de_eop_lead_months_order_to_production_start","2026-05-21",2026,2,"PPA_seasonal",3.0,"months_eop_open_to_production_start",
    T+"2026-05-21__de-us-20260521-call-pres__1042774.md",
    '"We\'re just launching EOPs for model year 2027 spring products, which will begin production in the last few months of the fiscal year." | EOP opened early May 2026, production begins ~Aug-2026 = ~3 months')

# EOP results, year-over-year, where quantified
EOPRES = [
 ("2014-02-12",2014,1,"PPA_combines",None,"They were down year-over-year on the combine early order program.",T+"2014-02-12__de-us-20140212-call-qna__1527306.md"),
 ("2014-11-26",2014,4,"PPA_seasonal",-40.0,"Given that, as we look at early November, most programs are down 40% or more on the early order program.",T+"2014-11-26__de-us-20141126-call-qna__1523108.md"),
 ("2018-02-16",2018,1,"PPA_combines",12.0,"If you think about the combine EOP, it did come in strong, up double digits.",T+"2018-02-16__de-us-20180216-call-qna__1477401.md"),
 ("2018-05-18",2018,2,"PPA_combines",12.0,"Replacement demand is reflected in the results of our 2018 Combine Early Order program, which increased by double digits from the previous year.",T+"2018-05-18__de-us-20180518-call-pres-2__1475345.md"),
 ("2018-11-21",2018,4,"PPA_crop_care",5.0,"In September, the final phase of the planter and sprayer early order program concluded, with orders up mid-single digits over 2018.",T+"2018-11-21__de-us-20181121-call-pres-2__1441802.md"),
 ("2021-02-19",2021,1,"PPA_crop_care",12.0,"Our Crop Care early order program, which ended in October, finished with unit orders up double digits compared to the prior year.",T+"2021-02-19__de-us-20210219-call-pres__46420.md"),
 ("2021-02-19",2021,1,"PPA_combines",12.0,"we completed our Combine early order program in January, with results also up double digits and outpacing the results of our Crop Care program.",T+"2021-02-19__de-us-20210219-call-pres__46420.md"),
 ("2023-11-22",2023,4,"PPA_planters",0.0,"our model year 2024 sprayer early order program ended strong, up year-over-year, and planters were flat year-over-year",T+"2023-11-22__de-us-20231122-call-pres__46470.md"),
 ("2023-11-22",2023,4,"PPA_combines",-12.0,"While our combine early order program does not finish until the end of November, we expect volumes to be down double digits when compared to 2023.",T+"2023-11-22__de-us-20231122-call-pres__46470.md"),
 ("2025-08-15",2025,3,"PPA_sprayers",-20.0,"Based on the results of the EOP and expected order intake post EOP, which is based on historical activity, we project model year '26 sprayers to be down roughly 20% year over year.",T+"2025-08-15__de-us-20250815-call-q3-pres__143406.md"),
 ("2025-11-26",2025,4,"PPA_sprayers",-20.0,"We mentioned in last quarter's call that based on the results of the early order program, Deere sprayer shipments would be down around 20% this coming year.",T+"2025-11-26__de-us-20251126-call-q4-pres-2__361265.md"),
]
for date, fy, fq, seg, v, quote, path in EOPRES:
    if v is None:
        continue
    note = f'"{quote}"'
    if abs(v) == 12.0:
        note += ' | "double digits" coded as 12% as a nominal midpoint, direction is the reliable part'
    if v == 5.0:
        note += ' | "mid-single digits" coded as 5%'
    add("de_eop_orders_yoy_pct", date, fy, fq, seg, "eop_orders_yoy", v, "pct_yoy", path, note)

# EOP outcome vs realised shipments -- the accuracy check that matters
add("de_eop_forecast_accuracy_flag","2026-02-19",2026,1,"PPA_combines",1,"flag_1_eop_guided_outcome_held",
    T+"2026-02-19__de-us-20260219-call-pres__605076.md",
    '"our combined Early Order Program finished better than expected, and large tractor order activity has increased" -> Deere RAISED its NA large-ag net sales forecast on the strength of a closed EOP. Evidence that the closed EOP is used directly as the shipment forecast.')
add("de_eop_forecast_accuracy_flag","2025-11-26",2025,4,"PPA_sprayers",1,"flag_1_eop_guided_outcome_held",
    T+"2025-11-26__de-us-20251126-call-q4-pres-2__361265.md",
    '"We mentioned in last quarter\'s call that based on the results of the early order program, Deere sprayer shipments would be down around 20% this coming year." -> the Q3 FY2025 EOP read was carried straight into the FY2026 shipment plan one quarter later, unchanged.')

# ---------------------------------------------------------------------------
# C. UNDERPRODUCTION FLAGS (the mechanism that DOES move revenue)
# ---------------------------------------------------------------------------
UP = [
 ("2015-05-22",2015,2,"AT",1,"We have underproduced year-to-date, and we would continue, especially as we go into the back half of the year, we'll be underproducing the retail environment and continuing to bring those field inventories down",T+"2015-05-22__de-us-20150522-call-qna__1521782.md"),
 ("2017-05-19",2017,2,"PPA",0,"If you think about large ag, for example, certainly versus last year where we were underproducing retail, this year we would be at or pretty much at retail.",T+"2017-05-19__de-us-20170519-call-qna__1479659.md"),
 ("2019-05-17",2019,2,"PPA",1,"The reduction from previous guidance relates to recent softness in the North American large ag and dairy markets, as well as our decision to underproduce retail for the remainder of the year.",T+"2019-05-17__de-us-20190517-call-pres-2__1392890.md"),
 ("2020-05-21",2020,2,"AT",1,"The incremental decline relative to the industry guidance reflects plans to underproduce retail sales as we take further actions to reduce field inventory.",T+"2020-05-21__de-us-20200521-call-pres-2__1143269.md"),
 ("2021-05-21",2021,2,"PPA",0,"At this point, we anticipate producing in line with retail demand for the year, keeping inventory levels relatively tight heading into fiscal year 2022.",T+"2021-05-21__de-us-20210521-call-pres__46476.md"),
 ("2023-05-19",2023,2,"SAT",1,"we've seen inventory rise, and we will cut production and have cut and will produce below retail in the back half of the year to try to manage that inventory.",T+"2023-05-19__de-us-20230519-call-qna__46469.md"),
 ("2024-05-16",2024,2,"PPA",1,"This is probably best exemplified by our decision to underproduce large tractor retail demand in North America in the back half of the year.",T+"2024-05-16__de-us-20240516-call-pres__46458.md"),
 ("2026-05-21",2026,2,"PPA_NA",0,"With these improvements, our plan for the year is to continue to manage production in line with retail demand.",T+"2026-05-21__de-us-20260521-call-pres__1042774.md"),
 ("2026-05-21",2026,2,"SAT_NA",0,"we continue to execute against our plan to build in line with retail demand this fiscal year.",T+"2026-05-21__de-us-20260521-call-pres__1042774.md"),
 ("2026-05-21",2026,2,"PPA_europe",0,"In Europe, 2026 production is largely aligned with retail demand",T+"2026-05-21__de-us-20260521-call-pres__1042774.md"),
 ("2026-05-21",2026,2,"PPA_brazil",1,"while in Brazil we expect to underproduce retail demand, most notably in combines.",T+"2026-05-21__de-us-20260521-call-pres__1042774.md"),
 ("2026-02-19",2026,1,"PPA_brazil",1,"We'll underproduce retail for Brazilian combines in our second and third quarters to bring those inventory levels down.",T+"2026-02-19__de-us-20260219-call-pres__605076.md"),
]
for date, fy, fq, seg, v, quote, path in UP:
    add("de_underproduction_flag", date, fy, fq, seg, "planned_underproduction_vs_retail",
        v, "flag_1_underproducing", path,
        f'"{quote}" | 1 = management states it will produce BELOW retail demand; 0 = explicitly in line with retail')

# magnitude, where given
add("de_underproduction_magnitude_pct","2024-05-16",2024,2,"PPA",9.0,"underproduction_vs_retail_sales",
    T+"2024-05-16__de-us-20240516-call-qna__46474.md",
    '"if you look at Production and Precision Ag, you know, it\'s about high single digit underproduction." | "high single digit" coded as 9%; worldwide, complete-goods basis, full fiscal year')

# ---------------------------------------------------------------------------
# D. WHAT WAS SAID AT EACH Q2 CALL ABOUT THE H2 / Q3 REVENUE CADENCE,
#    and what actually happened. This is the direct test.
# ---------------------------------------------------------------------------
CADENCE = [
 ("2022-05-20",2022,"back_half_weighted",
  "We also expect shipments to be more back-half weighted than we've seen historically as we work through a backlog of partially built inventory waiting for supplied parts",
  T+"2022-05-20__de-us-20220520-call-pres__46444.md"),
 ("2023-05-19",2023,"q3_down_sequentially_10_15pct",
  "We'd expect revenue to be down sequentially by a bit over 10% in the third quarter.",
  T+"2023-05-19__de-us-20230519-call-pres__46451.md"),
 ("2024-05-16",2024,"h2_underproduction_lower_volumes",
  "Demand shifts, coupled with proactive inventory management, are reflected in our production schedules for the balance of the fiscal year, with many product lines anticipating retail demand under production to close out 2024.",
  T+"2024-05-16__de-us-20240516-call-pres__46458.md"),
 ("2025-05-15",2025,"h2_margins_back_end_loaded",
  "Again, being so back-end loaded in the back half margins, that's 2 to 2 and a half points in the back half.",
  T+"2025-05-15__de-us-20250515-call-qna__46440.md"),
 ("2026-05-21",2026,"q4_higher_than_q3",
  "we would expect slightly higher revenue in the back half, with the fourth quarter being higher than the third quarter. In addition, we would expect to see our most favorable cost comparisons in the fourth quarter as well.",
  T+"2026-05-21__de-us-20260521-call-pres__1042774.md"),
]
for date, fy, code, quote, path in CADENCE:
    add("de_q2call_h2_cadence_statement", date, fy, 2, "enterprise", code, 1, "flag_statement_made",
        path, f'"{quote}" | component field carries the coded content of the statement')

# the FY2026 segment-level cadence detail -- highest-value rows for the Q3 FY2026 call
for seg, code, quote in [
 ("PPA","q4_stronger_than_q3","As you look at Large Ag ... Q4 a bit stronger than Q3. We talked about at the beginning of the year some differences in normal seasonality. We've got more Waterloo large tractor shipments shipping to North America in the back half than the front half of the year. That's abnormal for us, but reflected how the order book built for the course of the year."),
 ("SAT","step_down_q3_then_q4","On the small Ag side, it's pretty normal seasonality. You'll get a little bit of a step down in Q3 and another step down in Q4, just on a normal seasonal basis."),
 ("CF","balanced_q3_q4","Construction & Forestry, fairly balanced between the two. Both top line and margin in the back half, maybe a little bit stronger in the fourth quarter than Q3, but overall pretty close."),
]:
    add("de_q2call_h2_cadence_by_segment","2026-05-21",2026,2,seg,code,1,"flag_statement_made",
        T+"2026-05-21__de-us-20260521-call-qna__1042775.md", f'"{quote}"')

add("de_q2call_h2_cadence_by_segment","2026-05-21",2026,2,"PPA_absorption","q4_better_overhead_absorption",1,
    "flag_statement_made", T+"2026-05-21__de-us-20260521-call-qna__1042775.md",
    '"The other thing that we\'ll see, particularly for our large ag factories, is a little bit better absorption in the fourth quarter as production rates are significantly higher." | implies Q3 FY2026 PPA carries WEAKER absorption than Q4')
add("de_q2call_h2_cadence_by_segment","2026-05-21",2026,2,"enterprise_price_cost","price_cost_improves_through_h2",1,
    "flag_statement_made", T+"2026-05-21__de-us-20260521-call-qna__1042775.md",
    '"Price cost will improve as we move through the balance of the fiscal year." with "most favorable cost comparisons in the fourth quarter" -> Q3 sits between H1 and the favourable Q4')

# ---------------------------------------------------------------------------
# E. EVIDENCE AGAINST THE HYPOTHESIS -- order book != shipped revenue
# ---------------------------------------------------------------------------
add("de_orderbook_to_revenue_break_flag","2012-08-15",2012,3,"AT",1,"orders_cancellable",
    T+"2012-08-15__de-us-20120815-call-pres__1533564.md",
    '"Consequently, some machines will be shipped too late for harvest, we have allowed dealers to cancel orders." | a booked order is not an unconditional shipment')
add("de_orderbook_to_revenue_break_flag","2022-05-20",2022,2,"enterprise",1,"supply_constrained_shipment",
    T+"2022-05-20__de-us-20220520-call-qna__46464.md",
    '"Really, the biggest challenge, though, as we noted in the Q2, was the number of partially completed machines that you referenced" | FY2022 order books were FULL yet revenue timing was set by parts availability, not by the order book')
add("de_orderbook_to_revenue_break_flag","2022-08-19",2022,3,"CF_compact",1,"supply_constrained_shipment",
    T+"2022-08-19__de-us-20220819-call-pres__46475.md",
    '"Though demand remains strong for compact construction products, the downward revision reflects extremely low levels of inventory and supply challenges constraining shipments." | full demand, revised-down revenue')
add("de_orderbook_to_revenue_break_flag","2019-05-17",2019,2,"PPA",1,"deere_cut_its_own_schedule_at_q2",
    T+"2019-05-17__de-us-20190517-call-pres-2__1392890.md",
    '"our decision to underproduce retail for the remainder of the year" announced AT the Q2 call -> the H2 revenue change was a Deere decision, disclosed at the Q2 call, not an unforecastable shock')

# ---------------------------------------------------------------------------
# F. REALISED SEASONALITY / DISPERSION  (computed from the 8-K corpus)
# ---------------------------------------------------------------------------
EIGHTK = json.load(open("/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/de_8k_quarters.json"))
QEND = {  # fiscal quarter end dates used only as the period_end label
 (2020,3):"2020-08-02",(2021,3):"2021-08-01",(2022,3):"2022-07-31",(2023,3):"2023-07-30",
 (2024,3):"2024-07-28",(2025,3):"2025-07-27",
}
for fy in range(2020, 2026):
    a = EIGHTK.get(f"{fy}Q2",{}).get("nsr_cur"); b = EIGHTK.get(f"{fy}Q3",{}).get("nsr_cur")
    if a and b:
        add("de_q3_over_q2_nsr_ratio", QEND[(fy,3)], fy, 3, "enterprise", "realised_q3_div_q2_net_sales_and_revenues",
            round(b/a,4), "ratio", "filings/ 8-K earnings releases (Q2 and Q3 of each FY)",
            f"Q3 NSR {b:.0f} / Q2 NSR {a:.0f}. Tests whether Q3 revenue is mechanically implied by Q2. n=6 across FY2020-FY2025.")
    a = EIGHTK.get(f"{fy}Q2",{}).get("ppa_sales_cur"); b = EIGHTK.get(f"{fy}Q3",{}).get("ppa_sales_cur")
    if a and b:
        add("de_ppa_q3_over_q2_sales_ratio", QEND[(fy,3)], fy, 3, "PPA", "realised_q3_div_q2_segment_net_sales",
            round(b/a,4), "ratio", "filings/ 8-K earnings releases (Q2 and Q3 of each FY)",
            f"PPA Q3 sales {b:.0f} / Q2 sales {a:.0f}. Segment tables only exist from FY2021 (new segment structure), so n=5.")
    s2 = EIGHTK.get(f"{fy}Q2",{}).get("ppa_sales_cur"); o2 = EIGHTK.get(f"{fy}Q2",{}).get("ppa_op_cur")
    s3 = EIGHTK.get(f"{fy}Q3",{}).get("ppa_sales_cur"); o3 = EIGHTK.get(f"{fy}Q3",{}).get("ppa_op_cur")
    if s2 and o2 and s3 and o3:
        add("de_ppa_margin_q3_minus_q2_pp", QEND[(fy,3)], fy, 3, "PPA", "realised_q3_minus_q2_operating_margin",
            round(o3/s3*100 - o2/s2*100, 2), "percentage_points",
            "filings/ 8-K earnings releases (Q2 and Q3 of each FY)",
            f"Q3 margin {o3/s3*100:.2f}% minus Q2 margin {o2/s2*100:.2f}%. n=5.")

# ---------------------------------------------------------------------------
# G. AMPLIFICATION TEST: in H2, how much does PPA revenue move vs PPA profit?
#    The hypothesis predicts a small revenue move and a large profit move.
# ---------------------------------------------------------------------------
for fy in range(2022, 2026):
    def h2(tag, y):
        a = EIGHTK.get(f"{y}Q3",{}).get(tag); b = EIGHTK.get(f"{y}Q4",{}).get(tag)
        return (a+b) if (a and b) else None
    s_now, s_pri = h2("ppa_sales_cur", fy), h2("ppa_sales_cur", fy-1)
    o_now, o_pri = h2("ppa_op_cur", fy),   h2("ppa_op_cur", fy-1)
    if s_now and s_pri and o_now and o_pri:
        ds = (s_now/s_pri - 1)*100
        do = (o_now/o_pri - 1)*100
        add("de_ppa_h2_sales_yoy_pct", QEND[(fy,3)].replace("-08-","-10-"), fy, 4, "PPA",
            "h2_q3_plus_q4_segment_sales_yoy", round(ds,1), "pct_yoy",
            "filings/ 8-K earnings releases (Q3 and Q4 of each FY)",
            f"H2 FY{fy} PPA sales {s_now:.0f} vs H2 FY{fy-1} {s_pri:.0f}. Paired with de_ppa_h2_op_yoy_pct to show revenue-vs-profit amplification. n=4 (FY2022-FY2025), segment tables begin FY2021.")
        add("de_ppa_h2_op_yoy_pct", QEND[(fy,3)].replace("-08-","-10-"), fy, 4, "PPA",
            "h2_q3_plus_q4_segment_operating_profit_yoy", round(do,1), "pct_yoy",
            "filings/ 8-K earnings releases (Q3 and Q4 of each FY)",
            f"H2 FY{fy} PPA operating profit {o_now:.0f} vs H2 FY{fy-1} {o_pri:.0f}. Amplification vs sales = {do/ds if ds else float('nan'):.1f}x.")

add("de_q2call_h2_revenue_call_accuracy","2025-05-15",2025,2,"enterprise",
    "q2call_said_h2_sales_change_small_actual_yoy_pct", 0.5, "pct_yoy",
    T+"2025-05-15__de-us-20250515-call-qna__46440.md",
    '"The decremental math, candidly, gets a little bit funny just because the change in sales is relatively small year-over-year as you look at the second half of 2025 versus the second half of 2024." Actual: H2 FY2025 enterprise net sales and revenues 12,018 + 12,394 = 24,412 vs H2 FY2024 13,152 + 11,143 = 24,295, i.e. +0.5%. The Q2-call revenue characterisation was right; the whole Q&A that day was analysts disputing the MARGIN, not the revenue.')

# ---- the one directly checkable Q2-call Q3 revenue guide in the corpus ----
_a = EIGHTK["2023Q2"]["nsr_cur"]; _b = EIGHTK["2023Q3"]["nsr_cur"]
add("de_q2call_q3_revenue_guide_pct","2023-05-19",2023,2,"enterprise",
    "q2call_guided_q3_sequential_change", -12.5, "pct_sequential",
    T+"2023-05-19__de-us-20230519-call-pres__46451.md",
    '"We\'d expect revenue to be down sequentially by a bit over 10% in the third quarter." and, in Q&A, "a sequential decline anywhere from, you know, 10%-15% in revenue as we go into the third quarter." Value = midpoint of the 10-15% range.')
add("de_q3_revenue_actual_vs_q2call_guide_pp","2023-07-30",2023,3,"enterprise",
    "actual_minus_guided_sequential_change", round((_b/_a-1)*100 - (-12.5), 1), "percentage_points",
    "filings/2023-08-18__de-us-20230818-q3-8k__105829.md and filings/2023-05-19__de-us-20230519-q2-8k__105839.md",
    f"Actual Q3 FY2023 sequential change {(_b/_a-1)*100:.1f}% ({_b:.0f} vs {_a:.0f}) versus the -12.5% midpoint guided at the Q2 call. n=1: this is the ONLY quarter in the corpus where management put an explicit number on the Q3 sequential revenue move at the Q2 call, so it is an anecdote, not a distribution.")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=HDR)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(f"wrote {len(rows)} rows -> {OUT}")
from collections import Counter
c = Counter(r["series_id"] for r in rows)
for k, v in sorted(c.items()):
    print(f"  {v:3d}  {k}")
