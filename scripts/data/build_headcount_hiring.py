#!/usr/bin/env python3
"""Build headcount_hiring.csv for Deere (DE).

Backbone  : 10-K Item 1 "Employees" disclosures, FY2015-FY2025 (corpus, verbatim).
Derived   : non-US headcount, revenue per employee, equipment sales per production employee.
Events    : FY2026 recall / hire announcements (dated local + trade news).
Snapshot  : careers.deere.com external job board, counted by location and department,
            fetched 2026-08-16 by scripts/data/fetch_deere_jobs.py.
Missing data is an ABSENT ROW. No estimates, no zero-filling.
"""
import csv, json, os, datetime, collections

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/footprint/headcount_hiring.csv"
JOBS = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/deere_jobs.json"
CORPUS = "challenge/offline-data/deere/filings/"
HDR = ["series_id","date","plant","city","state_or_region","country","segment","metric",
       "value","units","source_type","source","notes"]
rows = []
def r(**kw):
    row = {h: kw.get(h, "") for h in HDR}
    rows.append(row)

# ---------------------------------------------------------------- 1. 10-K backbone
TENK = {
 2015: dict(d="2015-10-31", f="2015-11-25__de-us-20151125-q4-10k__469104.md", tot=57200, usca=28500, uaw=10000, pct=82),
 2016: dict(d="2016-10-31", f="2016-11-23__de-us-20161123-q4-10k__469184.md", tot=56800, usca=27900, uaw=7600,  pct=84),
 2017: dict(d="2017-10-29", f="2017-11-22__de-us-20171122-q4-10k__468364.md", tot=60500, usca=29000, uaw=8700,  pct=84),
 2018: dict(d="2018-10-28", f="2018-11-21__de-us-20181121-q4-10k__469201.md", tot=74000, usca=31000, uaw=9600,  pct=85),
 2019: dict(d="2019-11-03", f="2019-11-27__de-us-20191127-q4-10k__469283.md", tot=73500, usca=30000, uaw=9300,  pct=84),
 2020: dict(d="2020-11-01", f="2020-11-25__de-us-20201125-q4-10k__105845.md", tot=69600, usca=27500, uaw=8740,  pct=84),
 2021: dict(d="2021-10-31", f="2021-11-24__de-us-20211124-q4-10k__131650.md", tot=75600, usca=29000, uaw=10500, pct=83),
 2022: dict(d="2022-10-30", f="2022-11-23__de-us-20221123-q4-10k__105816.md", tot=82200, usca=32000, uaw=11500, pct=81),
 2023: dict(d="2023-10-29", f="2023-11-22__de-us-20231122-q4-10k__105844.md", tot=83000, usca=33800, uaw=11500, pct=80),
 2024: dict(d="2024-10-27", f="2024-11-21__de-us-20241121-q4-10k__105810.md", tot=75800, us=29600,
            prod=35200, usprod=13300, uaw=8900, pct=77),
 2025: dict(d="2025-11-02", f="2025-11-26__de-us-20251126-q4-10k__469216.md", tot=73100, us=27000,
            prod=32500, usprod=11600, uaw=7600, pct=77),
}
# Total net sales and revenues (USDm), 10-K selected financial data / income statement
REV = {2015:28863,2016:26644,2017:29738,2018:37358,2019:39258,2020:35540,
       2021:44024,2022:52577,2023:61251,2024:51716,2025:45684}
# Equipment operations net sales = PPA + SAT + CF (USDm), FY2024/FY2025 10-K Item 1
EQSALES = {2015:25775,2016:23387,2017:25885,2018:33351,2019:34886,2020:31272,
           2021:39737,2022:47917,2023:55565,2024:44759,2025:38917}

for fy, v in sorted(TENK.items()):
    src = CORPUS + v["f"]
    r(series_id="de_total_employees", date=v["d"], country="Worldwide", metric="total_employees",
      value=v["tot"], units="employees", source_type="filing", source=src,
      notes=f"FY{fy} 10-K Item 1 Employees; company states 'approximately'")
    if "usca" in v:
        r(series_id="de_us_canada_employees", date=v["d"], country="US+Canada",
          metric="employees_us_and_canada", value=v["usca"], units="employees",
          source_type="filing", source=src,
          notes=f"FY{fy} 10-K; US AND CANADA combined - definition changed to US-only from FY2024, series NOT continuous with de_us_employees")
        r(series_id="de_non_us_employees", date=v["d"], country="Ex-US+Canada",
          metric="employees_outside_us_and_canada", value=v["tot"]-v["usca"], units="employees",
          source_type="inference", source=src,
          notes=f"derived: total minus US+Canada; FY{fy}; excludes Canada so not comparable to FY2024-25 rows")
    if "us" in v:
        r(series_id="de_us_employees", date=v["d"], country="United States", metric="employees_us",
          value=v["us"], units="employees", source_type="filing", source=src,
          notes=f"FY{fy} 10-K; US ONLY (Canada excluded from FY2024 disclosure onward)")
        r(series_id="de_non_us_employees", date=v["d"], country="Ex-US", metric="employees_outside_us",
          value=v["tot"]-v["us"], units="employees", source_type="inference", source=src,
          notes=f"derived: total minus US; FY{fy}; includes Canada, unlike FY2015-23 rows")
    if "prod" in v:
        r(series_id="de_production_employees", date=v["d"], country="Worldwide",
          metric="full_time_production_employees", value=v["prod"], units="employees",
          source_type="filing", source=src,
          notes=f"FY{fy} 10-K; first disclosed FY2024. Closest filing-grade proxy for plant activity")
        r(series_id="de_us_production_employees", date=v["d"], country="United States",
          metric="full_time_production_employees_us", value=v["usprod"], units="employees",
          source_type="filing", source=src, notes=f"FY{fy} 10-K; first disclosed FY2024")
    r(series_id="de_uaw_covered_employees", date=v["d"], country="United States",
      metric="uaw_collective_bargaining_covered_workers", value=v["uaw"], units="employees",
      source_type="filing", source=src,
      notes=f"FY{fy} 10-K; ACTIVE US production and maintenance workers under the UAW master agreement. Laid-off workers drop out, so this is the highest-signal filing-grade production-labour series")
    r(series_id="de_us_union_coverage_pct", date=v["d"], country="United States",
      metric="pct_us_production_maintenance_unionised", value=v["pct"], units="percent",
      source_type="filing", source=src, notes=f"FY{fy} 10-K")

# ---------------------------------------------------------------- 2. productivity ratios
for fy, v in sorted(TENK.items()):
    r(series_id="de_revenue_per_employee", date=v["d"], country="Worldwide",
      metric="net_sales_and_revenues_per_employee", value=round(REV[fy]*1e6/v["tot"]),
      units="usd_per_employee", source_type="inference",
      source=CORPUS + v["f"],
      notes=f"FY{fy} worldwide net sales and revenues ${REV[fy]}m / {v['tot']} employees")
for fy, v in sorted(TENK.items()):
    r(series_id="de_equipment_net_sales", date=v["d"], country="Worldwide",
      segment="Equipment Operations (PPA+SAT+CF)", metric="net_sales_equipment_operations",
      value=EQSALES[fy], units="usd_millions", source_type="filing", source=CORPUS + v["f"],
      notes=f"FY{fy} 10-K MD&A; reference series so the per-employee ratios are reproducible")
    r(series_id="de_equipment_sales_per_uaw_covered_worker", date=v["d"], country="Worldwide/US mix",
      segment="Equipment Operations (PPA+SAT+CF)",
      metric="worldwide_equipment_net_sales_per_uaw_covered_us_worker",
      value=round(EQSALES[fy]*1e6/v["uaw"]), units="usd_per_employee", source_type="inference",
      source=CORPUS + v["f"],
      notes=f"FY{fy}. CROSS-BASIS INDEX, not a true productivity figure: numerator is worldwide equipment "
            f"net sales, denominator is US UAW-covered heads only. Useful only for its YoY direction and "
            f"for testing whether union headcount tracks shipments")

for fy in (2024, 2025):
    v = TENK[fy]
    r(series_id="de_equipment_sales_per_production_employee", date=v["d"], country="Worldwide",
      segment="Equipment Operations (PPA+SAT+CF)",
      metric="equipment_net_sales_per_full_time_production_employee",
      value=round(EQSALES[fy]*1e6/v["prod"]), units="usd_per_employee", source_type="inference",
      source=CORPUS + TENK[fy]["f"],
      notes=f"FY{fy} equipment ops net sales ${EQSALES[fy]}m / {v['prod']} production employees; capacity-utilisation check")

# ---------------------------------------------------------------- 3. FY2026 recall / hire events
EV = [
 # date, plant, city, state, n, kind, segment, source_type, source, notes
 ("2026-01-28","Davenport Works","Davenport","IA",75,"recall","Construction & Forestry","news",
  "https://www.brownfieldagnews.com/news/john-deere-brings-back-nearly-250-iowa-employees/",
  "announced late Jan 2026, employees back mid-Feb; assembly, fabrication, machining, material handling"),
 ("2026-01-28","Dubuque Works","Dubuque","IA",24,"recall","Construction & Forestry","news",
  "https://www.brownfieldagnews.com/news/john-deere-brings-back-nearly-250-iowa-employees/",
  "same announcement as Davenport 75; 99 combined"),
 ("2026-02-06","Waterloo Works","Waterloo","IA",146,"recall","Production & Precision Ag","news",
  "https://www.kcrg.com/2026/02/06/john-deere-waterloo-recalling-about-150-workers/",
  "Tractor Operations, Drivetrain, Engine Works and Foundry; supports 8R tractor build; back at work early March 2026 (Q2 FY2026)"),
 ("2026-02-19","Dubuque Works","Dubuque","IA",27,"recall","Construction & Forestry","news",
  "https://cbs2iowa.com/news/local/john-deere-recalls-27-more-workers-to-dubuque-works-as-production-ramps-up",
  "fabrication, assembly, material handling; factory manager Alex Fernandez cites strengthening customer demand"),
 ("2026-04-16","Dubuque Works","Dubuque","IA",21,"recall","Construction & Forestry","news",
  "https://www.constructionequipment.com/industry-news/news/55371187/john-deere-recalls-nearly-50-workers-as-production-demand-ticks-up",
  "April 2026 tranche; 49 across three plants"),
 ("2026-04-16","Davenport Works","Davenport","IA",20,"recall","Construction & Forestry","news",
  "https://www.constructionequipment.com/industry-news/news/55371187/john-deere-recalls-nearly-50-workers-as-production-demand-ticks-up",
  "April 2026 tranche"),
 ("2026-04-16","Coffeyville Works","Coffeyville","KS",8,"recall","Construction & Forestry","news",
  "https://www.constructionequipment.com/industry-news/news/55371187/john-deere-recalls-nearly-50-workers-as-production-demand-ticks-up",
  "April 2026 tranche; drivetrain/axles"),
 ("2026-06-11","Dubuque Works","Dubuque","IA",30,"new_hire","Construction & Forestry","news",
  "https://www.kcrg.com/2026/06/11/dubuque-john-deere-facility-hiring-30-new-postitions/",
  "NEW external hires, not recalls - recall list at Dubuque exhausted. INSIDE Deere FY2026 Q3 window (4 May - 2 Aug 2026). Crawler dozers, skid steers, backhoes, forestry machines"),
 ("2026-06-11","Davenport Works","Davenport","IA",20,"recall","Construction & Forestry","news",
  "https://www.kwqc.com/2026/06/11/john-deere-bringing-back-20-workers-davenport-works/",
  "INSIDE FY2026 Q3 window. 4WD loaders, dump trucks, motor graders, skidders"),
]
for d, plant, city, st, n, kind, seg, sty, src, note in EV:
    r(series_id=f"de_plant_{kind}_announced", date=d, plant=plant, city=city, state_or_region=st,
      country="United States", segment=seg, metric=f"workers_{kind}_announced", value=n,
      units="employees", source_type=sty, source=src, notes=note)

# cumulative US recall/hire counter as reported by the company through the press
CUM = [("2026-02-19",275,"https://cbs2iowa.com/news/local/john-deere-recalls-27-more-workers-to-dubuque-works-as-production-ramps-up","'approximately 275 US employees called back since the beginning of 2026'"),
       ("2026-04-16",324,"https://www.constructionequipment.com/industry-news/news/55371187/john-deere-recalls-nearly-50-workers-as-production-demand-ticks-up","'more than 300' / 324 recalled since January"),
       ("2026-06-11",400,"https://www.kcrg.com/2026/06/11/dubuque-john-deere-facility-hiring-30-new-postitions/","'400 employees rehired across the United States' since January 2026; other outlets say 'more than 400 across Iowa and Illinois'. Treat as a floor, rounded by the company")]
for d, n, src, note in CUM:
    r(series_id="de_us_cumulative_recalls_hires_fy2026", date=d, country="United States",
      metric="cumulative_workers_recalled_or_hired_since_2026_01_01", value=n, units="employees",
      source_type="news", source=src, notes=note)

# ---------------------------------------------------------------- 4. careers-site snapshot
SNAP = "2026-08-16"
SRC_JOBS = "https://careers.deere.com/api/pcsx/search?domain=johndeere.com (Eightfold; robots.txt allows /api/pcsx)"
NOTE_SNAP = ("CONTEMPORANEOUS SNAPSHOT taken 2026-08-16 - no history behind it. Informs FY2026 Q4+, "
             "NOT Q3 which closed 2026-08-02.")
jobs = json.load(open(JOBS))["positions"]
def loc(p): return (p.get("standardizedLocations") or p.get("locations") or ["unknown"])[0]
US = [p for p in jobs if loc(p).endswith("US") or loc(p).endswith(", US")]

r(series_id="de_open_job_postings_total", date=SNAP, country="Worldwide",
  metric="open_external_job_postings", value=len(jobs), units="postings",
  source_type="company-site", source=SRC_JOBS,
  notes=NOTE_SNAP + " Whole external board, all countries, all functions.")
r(series_id="de_open_job_postings_total", date=SNAP, country="United States",
  metric="open_external_job_postings", value=len(US), units="postings",
  source_type="company-site", source=SRC_JOBS, notes=NOTE_SNAP)

bydep = collections.Counter(p.get("department") for p in jobs)
for dep, n in bydep.most_common():
    r(series_id="de_open_job_postings_by_function", date=SNAP, country="Worldwide",
      metric=f"open_external_job_postings|{dep}", value=n, units="postings",
      source_type="company-site", source=SRC_JOBS,
      notes=NOTE_SNAP + " Deere's own department taxonomy. 'Production/Maintenance' = direct plant labour.")

# US city breakdown (only cities that are Deere plant/engineering towns get a plant label)
PLANT = {
 "Waterloo, IA, US":("Waterloo Works","Waterloo","IA","Production & Precision Ag"),
 "Dubuque, IA, US":("Dubuque Works","Dubuque","IA","Construction & Forestry"),
 "Moline, IL, US":("Moline (HQ / Cylinder / Seeding)","Moline","IL","Corporate & multiple"),
 "East Moline, IL, US":("Harvester Works","East Moline","IL","Production & Precision Ag"),
 "Davenport, IA, US":("Davenport Works","Davenport","IA","Construction & Forestry"),
 "Milan, IL, US":("Milan Parts Distribution","Milan","IL","Parts"),
 "Ottumwa, IA, US":("Ottumwa Works","Ottumwa","IA","Small Ag & Turf"),
 "Grovetown, GA, US":("Grovetown / Augusta","Grovetown","GA","Small Ag & Turf"),
 "Valley City, ND, US":("Valley City Works","Valley City","ND","Production & Precision Ag"),
 "Thibodaux, LA, US":("Thibodaux Works","Thibodaux","LA","Production & Precision Ag"),
 "Kernersville, NC, US":("Kernersville (new excavator plant)","Kernersville","NC","Construction & Forestry"),
 "Johnston, IA, US":("Johnston (Financial/IT)","Johnston","IA","Financial Services"),
 "Fargo, ND, US":("Fargo (engineering)","Fargo","ND","Production & Precision Ag"),
 "Silvis, IL, US":("Silvis (Seeding/Cylinder)","Silvis","IL","Production & Precision Ag"),
 "Coal Valley, IL, US":("Coal Valley","Coal Valley","IL","Construction & Forestry"),
 "Urbandale, IA, US":("Urbandale (ISG)","Urbandale","IA","Technology"),
 "Ames, IL, US":("Ames","Ames","IA","Production & Precision Ag"),
}
byloc = collections.Counter(loc(p) for p in US)
for l, n in byloc.most_common():
    p_, c_, s_, seg_ = PLANT.get(l, ("", l.split(",")[0].strip(), (l.split(",")[1].strip() if l.count(",")>=2 else ""), ""))
    prod = sum(1 for p in US if loc(p)==l and p.get("department")=="Production/Maintenance")
    r(series_id="de_open_job_postings_by_location", date=SNAP, plant=p_, city=c_, state_or_region=s_,
      country="United States", segment=seg_, metric="open_external_job_postings", value=n,
      units="postings", source_type="company-site", source=SRC_JOBS,
      notes=NOTE_SNAP + f" Of these, {prod} are department='Production/Maintenance'.")

# non-US locations with >=4 postings, for the export-side picture
byloc_all = collections.Counter(loc(p) for p in jobs if p not in US)
NONUS = {"Indaiatuba, SP, BR":("Indaiatuba","Indaiatuba","Sao Paulo","Brazil"),
         "MA, BW, DE":("Mannheim Works","Mannheim","Baden-Wurttemberg","Germany"),
         "Bruchsal, BW, DE":("Bruchsal (parts/cab)","Bruchsal","Baden-Wurttemberg","Germany"),
         "Poznań, Greater Poland Voivodeship, PL":("Poznan (shared services)","Poznan","Greater Poland","Poland"),
         "San Pedro Garza García, N.L., MX":("Monterrey area","San Pedro Garza Garcia","Nuevo Leon","Mexico"),
         "Walldorf, BW, DE":("Walldorf (Europe HQ)","Walldorf","Baden-Wurttemberg","Germany"),
         "Fleury-les-Aubrais, Centre-Val de Loire, FR":("Fleury-les-Aubrais","Fleury-les-Aubrais","Centre-Val de Loire","France"),
         "Stadtlohn, NRW, DE":("Stadtlohn","Stadtlohn","North Rhine-Westphalia","Germany")}
for l, n in byloc_all.most_common():
    if n < 4: continue
    p_, c_, s_, ctry = NONUS.get(l, ("", l.split(",")[0].strip(), "", l.split(",")[-1].strip()))
    prod = sum(1 for p in jobs if loc(p)==l and p.get("department")=="Production/Maintenance")
    r(series_id="de_open_job_postings_by_location", date=SNAP, plant=p_, city=c_, state_or_region=s_,
      country=ctry, metric="open_external_job_postings", value=n, units="postings",
      source_type="company-site", source=SRC_JOBS,
      notes=NOTE_SNAP + f" Of these, {prod} are department='Production/Maintenance'.")

r(series_id="de_open_production_postings_us", date=SNAP, country="United States",
  metric="open_external_postings_department_production_maintenance", value=0, units="postings",
  source_type="company-site", source=SRC_JOBS,
  notes="ZERO is an OBSERVED COUNT here, not missing data: all 8 Production/Maintenance postings on the "
        "board sit in Germany (Mannheim, Bruchsal) and France. CAVEAT: Deere fills US hourly roles from the "
        "UAW recall list first and does not appear to route US 'Production Assembler' requisitions through "
        "this external board - the 30 new Dubuque hires announced 2026-06-11 never appeared here. "
        "So the zero is NOT by itself evidence of a US hiring freeze.")

# ---------------------------------------------------------------- 5. WARN-derived context
r(series_id="de_us_warn_notices_fy2026", date="2026-08-16", country="United States",
  metric="warn_notices_filed_by_deere_in_calendar_2026", value=0, units="notices",
  source_type="warn-notice", source="https://warnact.io/company-john-deere ; https://warnfirehose.com/data/layoffs/company/john-deere",
  notes="OBSERVED ZERO. Aggregators covering Deere WARN filings show the most recent Iowa filing dated "
        "2025-09-17; none in calendar 2026 as of this snapshot. Verify against the state WARN pages before "
        "relying on it. Absence of WARN filings across the whole FY2026 Q3 window is a real, dated negative signal for layoffs.")

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=HDR)
    w.writeheader()
    for row in sorted(rows, key=lambda x: (x["series_id"], x["date"])):
        w.writerow(row)
print("wrote", OUT, len(rows), "rows")
