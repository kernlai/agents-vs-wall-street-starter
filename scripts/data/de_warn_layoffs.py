#!/usr/bin/env python3
"""
Build the Deere layoff / furlough / recall timeline (series de_warn_layoff, de_recall_callback).

Primary sources actually pulled (2026-08-16):
  IOWA   : Iowa Workforce Development WARN dashboard. The public page embeds a Tableau Public viz
           (IowaWARNNotifications/WARNNotifications). The workbook is downloadable as a .twb (a zip
           containing .hyper extracts) at https://public.tableau.com/workbooks/IowaWARNNotifications.twb
           -> 553 notice rows, notice dates 2021-08-18 .. 2026-08-13. Deere rows transcribed below.
           Reproduce with: fetch_iowa_warn() in this file.
  ILLINOIS: DCEO monthly WARN reports (1999-2026) listed at
           https://www.illinoisworknet.com/LayoffRecovery/Pages/ArchivedWARNReports.aspx
           331 monthly files downloaded (PDF pre-2020, XLSX 2020+), through July 2026.
           Only 4 Deere-related records exist in the whole 1999-2026 archive (see below).
           Reproduce with: fetch_illinois_warn() in this file.
  WISCONSIN: DWD layoff notices. 2020-2026 data is a public Google Sheet behind the page; pulled via
           https://docs.google.com/spreadsheets/d/1cyZiHZcepBI7ShB3dMcRprUFRG24lbwEnEDRBMhAqsA/gviz/tq?tqx=out:csv
           (635 rows, 2020-01-02 .. 2026-08-12). 2016-2019 pulled as static HTML. Zero Deere rows.

Everything else is news / company press release and is tagged as such in source_type.
No value in this file is estimated or interpolated. Rows that would need a guess are simply absent.
"""
import csv
import os
import sys

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/footprint/warn_layoffs.csv"

HEADER = ["series_id", "date", "plant", "city", "state_or_region", "country", "segment",
          "metric", "value", "units", "source_type", "source", "notes"]

IA_SRC = ("Iowa Workforce Development WARN notice database "
          "(https://workforce.iowa.gov/employers/resources/warn/notices ; data extract from "
          "https://public.tableau.com/workbooks/IowaWARNNotifications.twb, retrieved 2026-08-16)")
IL_SRC_T = ("Illinois DCEO monthly WARN report, {m} "
            "(https://www.illinoisworknet.com/LayoffRecovery/Pages/ArchivedWARNReports.aspx, retrieved 2026-08-16)")
WI_SRC = ("Wisconsin DWD layoff notices (https://dwd.wisconsin.gov/dislocatedworker/warn/ ; "
          "underlying public sheet 1cyZiHZcepBI7ShB3dMcRprUFRG24lbwEnEDRBMhAqsA, retrieved 2026-08-16)")

# plant -> (city, state, segment)
PLANT = {
    "Waterloo Works - Tractor Operations":      ("Waterloo", "IA", "PPA"),
    "Waterloo Works - Engine Works":            ("Waterloo", "IA", "PPA/multi"),
    "Waterloo Works - Drivetrain Operations":   ("Waterloo", "IA", "PPA"),
    "Waterloo Works - Foundry":                 ("Waterloo", "IA", "PPA"),
    "Waterloo Works":                           ("Waterloo", "IA", "PPA"),
    "Des Moines Works":                         ("Ankeny", "IA", "PPA"),
    "Davenport Works":                          ("Davenport", "IA", "CF"),
    "Dubuque Works":                            ("Dubuque", "IA", "CF"),
    "Ottumwa Works":                            ("Ottumwa", "IA", "SAT"),
    "Intelligent Solutions Group":              ("Urbandale", "IA", "PPA"),
    "John Deere Financial":                     ("Johnston", "IA", "Financial Services"),
    "Harvester Works":                          ("East Moline", "IL", "PPA"),
    "Seeding and Cylinder":                     ("Moline", "IL", "PPA"),
    "World Headquarters":                       ("Moline", "IL", "Corporate"),
    "Coffeyville Works":                        ("Coffeyville", "KS", "components/multi"),
    "Horicon Works":                            ("Horicon", "WI", "SAT"),
    "Multiple US factories":                    ("", "US", "multi"),
    "Multiple Quad Cities sites":               ("Moline/East Moline/Silvis", "IL", "multi"),
}

rows = []


def add(series, date, plant, metric, value, units, stype, source, notes):
    city, state, seg = PLANT.get(plant, ("", "", ""))
    rows.append([series, date, plant, city, state, "US", seg, metric,
                 "" if value is None else value, units, stype, source, notes])


# ---------------------------------------------------------------------------
# 1. IOWA WARN -- verbatim from the state database (notice_date, plant, n, effective_date)
#    "Notice Type" in the IA database is Mass Layoff unless noted.
# ---------------------------------------------------------------------------
IA = [
    # notice,     plant,                      n,   effective,   type,          extra note
    ("2024-03-12", "Des Moines Works",        30,  "2024-04-08", "Mass Layoff", "one of five staged tranches filed on the same notice date"),
    ("2024-03-12", "Des Moines Works",        30,  "2024-04-15", "Mass Layoff", "one of five staged tranches filed on the same notice date"),
    ("2024-03-12", "Des Moines Works",        30,  "2024-04-29", "Mass Layoff", "one of five staged tranches filed on the same notice date"),
    ("2024-03-12", "Des Moines Works",        30,  "2024-05-06", "Mass Layoff", "one of five staged tranches filed on the same notice date"),
    ("2024-03-12", "Des Moines Works",        30,  "2024-05-20", "Mass Layoff", "one of five staged tranches filed on the same notice date"),
    ("2024-03-26", "Waterloo Works",          308, "2024-04-26", "Mass Layoff", "site 3500 E Donald St (Tractor/Drivetrain complex)"),
    ("2024-05-20", "Waterloo Works",          192, "2024-06-21", "Mass Layoff", "site 3500 E Donald St"),
    ("2024-06-03", "Des Moines Works",        16,  "2024-06-06", "Mass Layoff", "salaried reduction wave, same-week effective date"),
    ("2024-06-03", "Intelligent Solutions Group", 58, "2024-06-06", "Mass Layoff", "salaried/technology roles, Urbandale"),
    ("2024-06-03", "Waterloo Works",          49,  "2024-06-06", "Mass Layoff", "salaried reduction wave, site 3500 E Donald St"),
    ("2024-06-07", "Intelligent Solutions Group", 1, "2024-06-07", "Amendment",  "amendment to the 2024-06-03 notice (+1 worker)"),
    ("2024-06-28", "Davenport Works",         211, "2024-08-30", "Mass Layoff", "same-day filing as Dubuque and (in IL) Harvester Works"),
    ("2024-06-28", "Dubuque Works",           99,  "2024-08-30", "Mass Layoff", "same-day filing as Davenport and (in IL) Harvester Works"),
    ("2024-07-11", "Waterloo Works",          191, "2024-09-20", "Mass Layoff", "site 3500 E Donald St; part of the 345-worker Waterloo action effective 2024-09-20"),
    ("2024-07-11", "Waterloo Works",          89,  "2024-09-20", "Mass Layoff", "site 300 Commercial St; part of the 345-worker Waterloo action effective 2024-09-20"),
    ("2024-07-11", "Waterloo Works",          65,  "2024-09-20", "Mass Layoff", "site 3801 W Ridgeway Ave; part of the 345-worker Waterloo action effective 2024-09-20"),
    ("2024-07-24", "Dubuque Works",           34,  "2024-07-24", "Mass Layoff", "salaried; notice and effective date the same day"),
    ("2024-07-24", "John Deere Financial",    67,  "2024-07-24", "Mass Layoff", "salaried; financial services, not a production site"),
    ("2024-07-24", "Waterloo Works",          69,  "2024-07-24", "Mass Layoff", "salaried; notice and effective date the same day"),
    ("2024-10-16", "Davenport Works",         80,  "2025-01-03", "Mass Layoff", "indefinite production layoff"),
    ("2024-12-03", "Waterloo Works",          112, "2025-01-06", "Mass Layoff", "indefinite production layoff, site 3500 E Donald St"),
    ("2025-01-06", "Ottumwa Works",           75,  "2025-02-07", "Mass Layoff", "hay and forage / balers"),
    ("2025-02-21", "Des Moines Works",        9,   "2025-03-31", "Mass Layoff", "one of three staged tranches filed on the same notice date"),
    ("2025-02-21", "Des Moines Works",        38,  "2025-04-07", "Mass Layoff", "one of three staged tranches filed on the same notice date"),
    ("2025-02-21", "Des Moines Works",        72,  "2025-04-28", "Mass Layoff", "one of three staged tranches filed on the same notice date"),
    ("2025-08-15", "Waterloo Works",          71,  "2025-09-22", "Mass Layoff", "site 2000 Westfield Ave = John Deere Foundry; part of the 238-worker three-plant action announced Aug 2025"),
    ("2025-09-17", "Des Moines Works",        40,  "2025-11-03", "Mass Layoff", "last Deere WARN filing in Iowa to date"),
    ("2025-09-17", "Waterloo Works",          101, "2025-10-20", "Mass Layoff", "site 3500 E Donald St; last Deere Waterloo WARN filing to date"),
]
for notice, plant, n, eff, ntype, extra in IA:
    add("de_warn_layoff", notice, plant, "employees_affected", n, "employees", "warn-notice", IA_SRC,
        f"notice_date={notice}; effective_date={eff}; notice_type={ntype}; "
        f"permanent_or_temporary=not stated in IA database (IA records only 'Mass Layoff'/'Closing'); "
        f"rescinded_or_recalled=no rescission recorded; {extra}")

# ---------------------------------------------------------------------------
# 2. ILLINOIS WARN -- the ONLY Deere-related records in the full 1999-2026 monthly archive
# ---------------------------------------------------------------------------
add("de_warn_layoff", "2014-08-20", "Harvester Works", "employees_affected", 425, "employees",
    "warn-notice", IL_SRC_T.format(m="August 2014"),
    "notice_date=2014-08-20; effective_date=2014-10-20 (first=ending layoff date); type=Layoff; "
    "permanent_or_temporary=Permanent; union=UAW Local 865; bumping rights=Yes; NAICS 333111; "
    "rescinded_or_recalled=not recorded. Largest single Deere WARN event found in either state; the 2014-15 ag downturn.")
add("de_warn_layoff", "2024-06-28", "Harvester Works", "employees_affected", 279, "employees",
    "warn-notice", IL_SRC_T.format(m="June 2024"),
    "notice_date=2024-06-28; effective_date=2024-08-30; type=Mass Layoff; permanent_or_temporary=Permanent; "
    "union=Yes; bumping rights=Yes; NAICS 333111; rescinded_or_recalled=no; filed the same day as the "
    "Davenport (211) and Dubuque (99) Iowa notices -- a single co-ordinated 589-worker action.")
add("de_warn_layoff", "2024-07-25", "Harvester Works", "employees_affected", 21, "employees",
    "warn-notice", IL_SRC_T.format(m="July 2024"),
    "supplemental notice to the 2024-06-28 filing; notice_date=2024-07-25; workers laid off 2024-07-24; "
    "permanent_or_temporary=not restated; rescinded_or_recalled=no. Increases the June action to 300 at Harvester Works.")
add("de_warn_layoff", "2024-07-25", "World Headquarters", "employees_affected", 298, "employees",
    "warn-notice", IL_SRC_T.format(m="July 2024"),
    "notice_date=2024-07-25; effective_date=2024-07-24 (notice filed after the fact); type=Layoff; "
    "permanent_or_temporary=Permanent; union=No; salaried head-office reduction, NOT production; "
    "rescinded_or_recalled=no.")
add("de_warn_layoff", "2018-09-07", "Multiple Quad Cities sites", "employees_affected", 79, "employees",
    "warn-notice", IL_SRC_T.format(m="September 2018"),
    "CONTRACTOR, NOT DEERE PAYROLL. Filed by Eurest Services (food service) for its operations at One John "
    "Deere Place + 1515 5th Ave Moline (58), 1100 13th Ave East Moline (16), 1800 158th St Silvis (5). "
    "notice_date=2018-09-07; effective 2018-09-30 to 2018-12-31; permanent; type=Closing. Included because it "
    "is a Deere-site event, but it must NOT be added to Deere headcount reductions.")

# ---------------------------------------------------------------------------
# 3. VERIFIED ZEROES IN THE CRITICAL WINDOW (FY2026 Q3 = 2026-05-04 .. 2026-08-02)
#    These are affirmative findings from complete databases, not missing data.
# ---------------------------------------------------------------------------
add("de_warn_layoff", "2026-08-02", "Multiple US factories", "warn_notices_filed", 0, "notices",
    "warn-notice", IA_SRC,
    "VERIFIED ZERO, not missing. Iowa WARN database is current to notice date 2026-08-13 (77 notices from other "
    "employers in CY2026, incl. CNH Industrial Burlington closings). It contains NO John Deere notice anywhere in "
    "calendar 2026. Last Deere Iowa filing: 2025-09-17. Covers Waterloo, Dubuque, Davenport, Ankeny, Ottumwa.")
add("de_warn_layoff", "2026-08-02", "Multiple Quad Cities sites", "warn_notices_filed", 0, "notices",
    "warn-notice", IL_SRC_T.format(m="Jan-Jul 2026"),
    "VERIFIED ZERO, not missing. All Illinois DCEO monthly WARN reports through July 2026 downloaded and scanned; "
    "no Deere record in calendar 2026. Note Illinois' higher trigger (33%% of site workforce or 250+) means "
    "sub-scale cuts at Harvester Works are invisible here -- the Aug-2025 115-worker cut was never IL-WARN-filed.")
add("de_warn_layoff", "2026-08-02", "Horicon Works", "warn_notices_filed", 0, "notices",
    "warn-notice", WI_SRC,
    "VERIFIED ZERO, not missing. Wisconsin DWD notices 2020-01-02..2026-08-12 (635 rows) plus static 2016-2019 "
    "pages contain no Deere record at all. Horicon has never triggered a WI WARN in the available record.")

# ---------------------------------------------------------------------------
# 4. NEWS / PRESS-RELEASE LAYOFFS THAT DID NOT PRODUCE A WARN FILING
# ---------------------------------------------------------------------------
add("de_warn_layoff", "2015-11-30", "Seeding and Cylinder", "employees_affected", 220, "employees",
    "filing", "Deere & Company press release 'Deere Announces Factory Workforce Adjustments', 2015-11-30 "
    "(https://www.prnewswire.com/news-releases/deere-announces-factory-workforce-adjustments-300185176.html)",
    "notice_date=2015-11-30; effective_date=2016-02-15; permanent_or_temporary=INDEFINITE layoff, company states "
    "'no specific call-back date' and explicitly distinguishes it from the site's past seasonal layoffs; "
    "rescinded_or_recalled=not recorded. No corresponding Illinois WARN record exists.")
add("de_warn_layoff", "2025-08-15", "Harvester Works", "employees_affected", 115, "employees",
    "news", "AgWeb / Manufacturing Dive / WQAD coverage of Deere's Aug-2025 three-plant announcement "
    "(https://www.manufacturingdive.com/news/deere-lay-off-238-workers-tractor-market-tariff-struggles-harvester-works/757892/)",
    "announced mid-Aug 2025; last day of work 2025-08-29; indefinite production layoff; recall rights equal to "
    "length of service; NOT WARN-filed in Illinois (below the IL trigger). Part of the 238-worker action "
    "(115 East Moline + 52 Moline + 71 Waterloo Foundry).")
add("de_warn_layoff", "2025-08-15", "Seeding and Cylinder", "employees_affected", 52, "employees",
    "news", "AgWeb / WQAD coverage of Deere's Aug-2025 three-plant announcement "
    "(https://www.wqad.com/article/money/business/john-deere/john-deere-lay-off-240-workers-iowa-illinois/526-59d0bc17-00e6-4725-b390-369f2d2dab49)",
    "announced mid-Aug 2025; indefinite production layoff; NOT WARN-filed in Illinois (below trigger). "
    "Part of the 238-worker action.")

# ---------------------------------------------------------------------------
# 5. RECALLS AND NEW HIRING -- the positive signal. 2026 only; this is the live cycle turn.
# ---------------------------------------------------------------------------
add("de_recall_callback", "2026-01-28", "Davenport Works", "employees_recalled", 75, "employees",
    "news", "CBS2 Iowa / KWWL, reporting Deere's 2026-01-28 announcement "
    "(https://cbs2iowa.com/news/local/john-deere-announces-146-waterloo-worker-callbacks-citing-increased-production-demand)",
    "announced 2026-01-28; workers return from indefinite layoff beginning mid-February 2026; assembly and "
    "material handling; construction & forestry demand. First recall of the cycle.")
add("de_recall_callback", "2026-01-28", "Dubuque Works", "employees_recalled", 24, "employees",
    "news", "CBS2 Iowa / KWWL, reporting Deere's 2026-01-28 announcement "
    "(https://cbs2iowa.com/news/local/john-deere-announces-146-waterloo-worker-callbacks-citing-increased-production-demand)",
    "announced 2026-01-28; return begins mid-February 2026; dozer assembly and general factory needs.")
add("de_recall_callback", "2026-02-06", "Waterloo Works", "employees_recalled", 146, "employees",
    "news", "CBS2 Iowa 2026-02-06 / KCRG 2026-02-06 / Deere newsroom 'Nearly 150 Employees Set to Return to Work "
    "at Waterloo Factories' (https://www.kcrg.com/2026/02/06/john-deere-waterloo-recalling-about-150-workers/)",
    "announced 2026-02-06; across four facilities -- Drivetrain Operations, Tractor Operations, Engine Works and "
    "the Foundry; supports 8R tractor assembly, machining, logistics and foundry; workers return early March 2026, "
    "callbacks continuing to end-February. Quote, Fabio Castro, Waterloo Works VP/factory manager: 'These callbacks "
    "at Waterloo Tractor Operations reflect the production needs driven by increased customer demand.' "
    "This is the large-ag (PPA) plant turning back on.")
add("de_recall_callback", "2026-03-01", "Dubuque Works", "employees_recalled", 27, "employees",
    "news", "Telegraph Herald / KIMT / KWWL, March 2026 ('Dubuque recalls 27 more workers, over 50 since January'); "
    "Deere newsroom 'Demand Grows, Jobs Return: 27 More Employees Return to Dubuque Works'",
    "DATE APPROXIMATE TO MONTH -- reported March 2026, exact announcement day not confirmed. Construction & "
    "forestry operations. Quote, Alex Fernandez, Dubuque Works factory manager: 'Customer demand has continued to "
    "strengthen, driving increased production that makes these callbacks possible.'")
add("de_recall_callback", "2026-04-13", "Dubuque Works", "employees_recalled", 21, "employees",
    "news", "Construction Equipment 2026-04-16 "
    "(https://www.constructionequipment.com/industry-news/news/55371187/john-deere-recalls-nearly-50-workers-as-production-demand-ticks-up)",
    "announced 2026-04-13; return during April 2026; fabrication, assembly, material handling.")
add("de_recall_callback", "2026-04-13", "Davenport Works", "employees_recalled", 20, "employees",
    "news", "Construction Equipment 2026-04-16 "
    "(https://www.constructionequipment.com/industry-news/news/55371187/john-deere-recalls-nearly-50-workers-as-production-demand-ticks-up)",
    "announced 2026-04-13; return during April 2026; fabrication, assembly, material handling.")
add("de_recall_callback", "2026-04-13", "Coffeyville Works", "employees_recalled", 8, "employees",
    "news", "Construction Equipment 2026-04-16 "
    "(https://www.constructionequipment.com/industry-news/news/55371187/john-deere-recalls-nearly-50-workers-as-production-demand-ticks-up)",
    "announced 2026-04-13; return during April 2026. Only non-Iowa/Illinois site in the 2026 recall record. "
    "CEO John May in the same release: 'While the global large agriculture industry continues to experience "
    "challenges, we're encouraged by the ongoing recovery in demand within both the construction and small "
    "agriculture segments.'")
add("de_recall_callback", "2026-06-11", "Davenport Works", "employees_recalled", 20, "employees",
    "news", "KWQC 2026-06-11 (https://www.kwqc.com/2026/06/11/john-deere-bringing-back-20-workers-davenport-works/); "
    "WQAD 2026-06-11; Telegraph Herald 2026-06-11",
    "INSIDE FY2026 Q3 (quarter runs 2026-05-04 to 2026-08-02). Announced 2026-06-11; return during June 2026; "
    "supports increased construction & forestry demand.")
add("de_recall_callback", "2026-06-11", "Dubuque Works", "employees_hired_new", 30, "employees",
    "news", "KCRG 2026-06-11 (https://www.kcrg.com/2026/06/11/dubuque-john-deere-facility-hiring-30-new-postitions/); "
    "Telegraph Herald 2026-06-11 'John Deere to hire 30 more employees in Dubuque'",
    "INSIDE FY2026 Q3. NOT a recall -- Deere states the Dubuque Works CALLBACK LIST IS EXHAUSTED and it is now "
    "hiring 30 NEW employees. This is the strongest single employment datapoint in the quarter: a plant that cut "
    "133 people via WARN in 2024 has re-absorbed everyone with recall rights and moved to external hiring.")
add("de_recall_callback", "2026-06-11", "Multiple US factories", "employees_recalled_cumulative", 400, "employees",
    "news", "KCRG / WQAD / Telegraph Herald, 2026-06-11, quoting Deere",
    "Company-stated cumulative: 400 US employees have returned to work or been hired since January 2026. "
    "Prior milestones on the same counter: ~275 (Feb 2026), 324 (Mar 2026), 'more than 300' (Apr 2026).")

# ---------------------------------------------------------------------------
# 6. OTHER Q3-WINDOW LABOUR EVENTS (no headcount attached)
# ---------------------------------------------------------------------------
add("de_warn_layoff", "2026-07-29", "Waterloo Works", "labor_event", 1, "event",
    "news", "KWWL, 'Deere holds firm as UAW Local 838 pushes back on proposed contract extension' "
    "(https://www.kwwl.com/news/deere-holds-firm-as-uaw-local-838-pushes-back-on-proposed-contract-extension/article_e762fff0-f556-4243-acc3-a4063a6feef3.html)",
    "INSIDE FY2026 Q3. UAW Local 838 bargaining committee met 2026-07-29 and countered Deere's offer of a two-year "
    "contract extension; Deere rejected the counter, saying it exceeds its own proposal by roughly half a billion "
    "dollars and is contrary to providing 'continuity and certainty when equipment demand is down'. "
    "YEAR NOT INDEPENDENTLY CONFIRMED -- the article is undated in the retrievable text; the July-29 day is "
    "reported, 2026 is inferred from search context. Treat as medium confidence. Directionally a caution: "
    "management was still describing large-ag demand as down while recalling workers.")
add("de_warn_layoff", "2025-10-15", "Ottumwa Works", "restructuring_announcement", 1, "event",
    "news", "AGDAILY, 'John Deere to relocate more Iowa jobs amid restructuring' "
    "(https://www.agdaily.com/news/john-deere-to-relocate-more-iowa-jobs-amid-restructuring/)",
    "DATE APPROXIMATE (article published mid-October 2025; exact day not on page). Product verification and "
    "validation testing moves out of Ottumwa Works and Des Moines Works to other Deere sites in IA and IL, "
    "to complete during fiscal 2026. HEADCOUNT NOT DISCLOSED -- Deere says the number depends on production "
    "needs and turnover and that some staff can relocate. Do not treat as a layoff count.")

# ---------------------------------------------------------------------------
# 7. DERIVED QUARTERLY AGGREGATES (fiscal quarters, bucketed by EFFECTIVE date for
#    layoffs and by ANNOUNCEMENT date for recalls). These are sums of rows already in
#    this file -- do not add them to the event rows.
# ---------------------------------------------------------------------------
FQ = [("FY2024Q1", "2023-10-30", "2024-01-28"), ("FY2024Q2", "2024-01-29", "2024-04-28"),
      ("FY2024Q3", "2024-04-29", "2024-07-28"), ("FY2024Q4", "2024-07-29", "2024-10-27"),
      ("FY2025Q1", "2024-10-28", "2025-01-26"), ("FY2025Q2", "2025-01-27", "2025-04-27"),
      ("FY2025Q3", "2025-04-28", "2025-07-27"), ("FY2025Q4", "2025-07-28", "2025-11-02"),
      ("FY2026Q1", "2025-11-03", "2026-02-01"), ("FY2026Q2", "2026-02-02", "2026-05-03"),
      ("FY2026Q3", "2026-05-04", "2026-08-02")]


def fq(d):
    for n, a, b in FQ:
        if a <= d <= b:
            return n, b
    return None, None


lay_q, rec_q = {}, {}
for r in list(rows):
    if r[7] == "employees_affected" and "CONTRACTOR" not in r[12]:
        eff = r[1]
        for tok in r[12].split(";"):
            if "effective_date=" in tok:
                eff = tok.split("effective_date=")[1].strip()[:10]
        n, _ = fq(eff)
        if n:
            lay_q[n] = lay_q.get(n, 0) + int(r[8])
    if r[7] in ("employees_recalled", "employees_hired_new"):
        n, _ = fq(r[1])
        if n:
            rec_q[n] = rec_q.get(n, 0) + int(r[8])

for n, a, b in FQ:
    if n in lay_q:
        add("de_warn_layoff_fq", b, "Multiple US factories", "employees_affected", lay_q[n], "employees",
            "inference", "derived aggregate of the event rows in this file",
            f"fiscal_quarter={n}; DERIVED, do not double-count. Sum of WARN/news layoff headcounts whose "
            f"EFFECTIVE date falls in {n} ({a}..{b}). Contractor row excluded.")
    if n in rec_q:
        add("de_recall_callback_fq", b, "Multiple US factories", "employees_recalled", rec_q[n], "employees",
            "inference", "derived aggregate of the event rows in this file",
            f"fiscal_quarter={n}; DERIVED, do not double-count. Sum of recall + new-hire headcounts ANNOUNCED "
            f"in {n} ({a}..{b}). Deere's own cumulative counter reached 400 by 2026-06-11 vs 371 summed here, "
            f"so this understates by ~29 -- some smaller callbacks were not individually reported.")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(HEADER)
    for r in sorted(rows, key=lambda x: (x[1], x[0], x[2])):
        w.writerow(r)

# quick console summary
warn_ia = [r for r in rows if r[10] == "warn-notice" and r[4] == "IA" and r[7] == "employees_affected"]
print(f"rows written: {len(rows)} -> {OUT}")
for y in ("2014", "2015", "2018", "2024", "2025", "2026"):
    ev = [r for r in rows if not r[0].endswith("_fq")]
    tot = sum(int(r[8]) for r in ev if r[1].startswith(y) and r[7] == "employees_affected" and r[2] != "Multiple Quad Cities sites")
    rec = sum(int(r[8]) for r in ev if r[1].startswith(y) and r[7] in ("employees_recalled", "employees_hired_new"))
    print(f"  {y}: layoffs {tot:>5}   recalls+hires {rec:>4}")
