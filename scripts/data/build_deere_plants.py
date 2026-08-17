#!/usr/bin/env python3
"""
Build the Deere & Company master plant inventory (tidy long CSV).

Spine sources (authoritative, in priority order):
  1. Deere FY2025 Form 10-K, Item 2 "Properties" -- table of *significant* manufacturing
     properties with the business segment each feeds, as of 2025-11-02.
     File: challenge/offline-data/deere/filings/2025-11-26__de-us-20251126-q4-10k__469216.md
  2. "John Deere Worldwide -- All locations" PDF, dated December 2025, published by
     Deere & Company Global Brand & Communications.
     https://www.deere.com/assets/pdfs/common/our-company/about/jd-world-locations.pdf
     This is the only public Deere source that enumerates every site with its products.
  3. Deere factory microsites (www.deere.com/en-us/our-company/locations/factories/<slug>)
     for founding years and a few site-size facts.
  4. Local news / economic-development bodies for plant-level headcount. Plant headcount is
     NOT systematically disclosed by Deere; every headcount row carries its own source+date.

Rules:
  - Missing data => no row. Never zero, never an invented estimate.
  - source_type in {filing, warn-notice, news, company-site, trade-data, estimate, inference}
  - notes carries the segment x geography attribution tags:
        geo_cell=<Deere revenue geography this plant's output primarily serves>
        seg_src=filing|inference
        orientation=domestic|export|mixed|unknown  (+ orientation_basis)

Output: data/deere/footprint/plants.csv
"""

import csv
import os

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/footprint/plants.csv"

TENK = ("Deere FY2025 Form 10-K Item 2 Properties (filed 2025-11-26), "
        "offline-data/deere/filings/2025-11-26__de-us-20251126-q4-10k__469216.md")
WWPDF = ("Deere & Company, 'John Deere Worldwide - All locations', December 2025, "
         "https://www.deere.com/assets/pdfs/common/our-company/about/jd-world-locations.pdf")

rows = []


def add(series_id, date, plant, city, region, country, segment, metric, value,
        units, source_type, source, notes=""):
    rows.append(dict(series_id=series_id, date=date, plant=plant, city=city,
                     state_or_region=region, country=country, segment=segment,
                     metric=metric, value=value, units=units,
                     source_type=source_type, source=source, notes=notes))


# ---------------------------------------------------------------------------
# PLANT SPINE
# key: slug
# fields: plant, city, region, country, segment, seg_src, geo_cell, products (list),
#         orientation, orientation_basis
# ---------------------------------------------------------------------------
P = {}


def plant(slug, name, city, region, country, segment, seg_src, geo_cell, products,
          orientation="unknown", orientation_basis=""):
    P[slug] = dict(name=name, city=city, region=region, country=country,
                   segment=segment, seg_src=seg_src, geo_cell=geo_cell,
                   products=products, orientation=orientation,
                   orientation_basis=orientation_basis)


# ---- UNITED STATES ---------------------------------------------------------
plant("waterloo", "John Deere Waterloo Works / Engine Works / Foundry / Drivetrain",
      "Waterloo", "Iowa", "United States", "PPA;CF", "filing", "United States",
      ["large ag tractors (7/8/9 Series)", "diesel engines", "drivetrain components",
       "foundry castings", "product engineering"],
      "mixed", "largest Deere tractor complex; 7/8/9R tractors sold in NA and exported")
plant("east-moline", "John Deere Harvester Works", "East Moline", "Illinois",
      "United States", "PPA", "filing", "United States",
      ["combine harvesters (S/X Series)", "corn heads", "draper platforms",
       "combine product engineering"],
      "mixed", "sole NA combine plant; supplies NA plus export")
plant("moline-seeding-cylinder", "John Deere Seeding Group / Cylinder Works (Moline)",
      "Moline", "Illinois", "United States", "PPA", "filing", "United States",
      ["planters and seeding equipment", "hydraulic cylinders",
       "performance upgrade kits"],
      "domestic", "row-crop planters primarily for NA row-crop market")
plant("des-moines", "John Deere Des Moines Works", "Ankeny (Des Moines)", "Iowa",
      "United States", "PPA", "filing", "United States",
      ["seeding equipment", "sprayers", "tillage equipment", "cotton harvesters"],
      "mixed", "cotton harvesters exported; seeding/tillage mainly NA")
plant("dubuque", "John Deere Dubuque Works", "Dubuque", "Iowa", "United States",
      "CF", "filing", "United States",
      ["backhoe loaders", "compact track loaders", "crawler dozers", "high-speed dozers",
       "knuckleboom loaders", "skid-steer loaders", "tracked feller bunchers",
       "tracked harvesters"],
      "mixed", "")
plant("davenport", "John Deere Davenport Works", "Davenport", "Iowa", "United States",
      "CF", "filing", "United States",
      ["articulated dump trucks", "cabs", "felling heads", "4WD loaders",
       "motor graders", "skidders", "wheeled feller bunchers"],
      "mixed", "")
plant("ottumwa", "John Deere Ottumwa Works", "Ottumwa", "Iowa", "United States",
      "SAT", "inference", "United States",
      ["hay and forage equipment", "large square balers", "round balers",
       "self-propelled windrowers"],
      "mixed", "hay & forage sits in Small Ag & Turf; segment not in 10-K Item 2 table")
plant("clarion", "John Deere Clarion (Hagie)", "Clarion", "Iowa", "United States",
      "PPA", "inference", "United States",
      ["self-propelled sprayers", "detasselers"], "domestic", "")
plant("paton", "John Deere Paton", "Paton", "Iowa", "United States",
      "PPA", "inference", "United States",
      ["planting equipment", "tillage equipment"], "domestic", "")
plant("rock-valley", "John Deere Rock Valley (all-makes parts)", "Rock Valley", "Iowa",
      "United States", "", "inference", "United States",
      ["all-makes replacement parts manufacturing and distribution"], "domestic", "")
plant("augusta", "John Deere Augusta Works (North and South factories)",
      "Augusta / Grovetown", "Georgia", "United States", "SAT", "filing",
      "United States",
      ["compact utility tractors (1/2/3/4 Family)", "utility tractors"],
      "export", "Deere: 27 models distributed across North America and exported to 40+ countries")
plant("greeneville", "John Deere Greeneville (John Deere Power Products)", "Greeneville",
      "Tennessee", "United States", "SAT", "filing", "United States",
      ["riding lawn equipment", "residential mowers"], "domestic", "")
plant("horicon", "John Deere Horicon Works", "Horicon", "Wisconsin", "United States",
      "SAT", "filing", "United States",
      ["Gator utility vehicles", "lawn and garden tractors (X300/500/700/900)",
       "golf and turf reel mowers", "walk-behind greens mowers"],
      "mixed", "")
plant("fuquay-varina", "John Deere Turf Care", "Fuquay-Varina", "North Carolina",
      "United States", "SAT", "filing", "United States",
      ["commercial mowers", "golf course mowers", "turf utility vehicles"],
      "mixed", "")
plant("kernersville", "John Deere Kernersville Campus", "Kernersville", "North Carolina",
      "United States", "CF", "filing", "United States",
      ["mid-size hydraulic excavators", "small excavators (west campus, from 2026)",
       "Kreisel battery packs"],
      "domestic", "built to replace excavators previously imported from Japan (Hitachi JV exit)")
plant("coffeyville", "John Deere Coffeyville Works (Funk Manufacturing)", "Coffeyville",
      "Kansas", "United States", "CF;PPA", "inference", "United States",
      ["power transmission equipment", "drivetrain and power-system components"],
      "domestic", "component plant feeding Deere assembly plants; not in 10-K Item 2 table")
plant("thibodaux", "John Deere Thibodaux", "Thibodaux", "Louisiana", "United States",
      "PPA;CF", "inference", "United States",
      ["sugarcane harvesters", "cotton stripper heads", "scrapers", "cane loaders",
       "airbooms"],
      "export", "world's largest sugarcane-equipment producer; sugarcane demand is Brazil/Asia-weighted")
plant("valley-city", "John Deere Seeding Group Valley City", "Valley City",
      "North Dakota", "United States", "PPA", "inference", "United States",
      ["air seeders", "commodity carts", "tillage equipment"], "domestic", "")
plant("fargo", "John Deere Electronic Solutions", "Fargo", "North Dakota",
      "United States", "PPA;SAT;CF", "inference", "United States",
      ["electronic controllers", "displays", "precision-ag electronics"],
      "mixed", "components feed all three equipment segments")
plant("springfield-mo", "John Deere Reman Springfield", "Springfield", "Missouri",
      "United States", "PPA;SAT;CF", "inference", "United States",
      ["remanufactured engines", "remanufactured transmissions", "axles and components"],
      "domestic", "")
plant("rock-island", "John Deere Rock Island (all-makes parts)", "Rock Island",
      "Illinois", "United States", "", "inference", "United States",
      ["all-makes replacement parts"], "domestic", "")

# ---- CANADA ----------------------------------------------------------------
plant("vancouver-ca", "John Deere Forestry Vancouver", "Vancouver", "British Columbia",
      "Canada", "CF", "inference", "Canada",
      ["forestry swing machines", "tracked feller bunchers", "tracked harvesters"],
      "mixed", "")
plant("altona", "John Deere Altona (aftermarket ag parts)", "Altona", "Manitoba",
      "Canada", "", "inference", "Canada", ["aftermarket agricultural parts"],
      "domestic", "")

# ---- LATIN AMERICA ---------------------------------------------------------
plant("horizontina", "John Deere Brasil Ltda Horizontina", "Horizontina",
      "Rio Grande do Sul", "Brazil", "PPA", "filing", "Latin America",
      ["combine harvesters", "headers", "planting equipment"],
      "mixed", "principal Brazilian combine plant; serves Brazil and LatAm export")
plant("montenegro", "John Deere Brasil Ltda Montenegro", "Montenegro",
      "Rio Grande do Sul", "Brazil", "PPA", "filing", "Latin America",
      ["ag tractors"], "domestic", "")
plant("catalao", "John Deere Brasil Ltda Catalao", "Catalao", "Goias", "Brazil",
      "PPA", "filing", "Latin America",
      ["sugarcane harvesters", "self-propelled sprayers"], "mixed", "")
plant("canoas", "John Deere Canoas", "Canoas", "Rio Grande do Sul", "Brazil",
      "PPA", "inference", "Latin America", ["self-propelled sprayers"], "domestic", "")
plant("indaiatuba", "John Deere Brazil Construction Factory (Indaiatuba)", "Indaiatuba",
      "Sao Paulo", "Brazil", "CF", "filing", "Latin America",
      ["backhoe loaders", "4WD loaders", "hydraulic excavators", "crawler dozers",
       "motor graders"], "mixed", "")
plant("porto-alegre", "Wirtgen Group Porto Alegre (Ciber)", "Porto Alegre",
      "Rio Grande do Sul", "Brazil", "CF", "inference", "Latin America",
      ["milling machines", "pavers", "rollers", "mobile asphalt mixing plants"],
      "mixed", "")
plant("rosario", "Industrias John Deere Argentina (Rosario/Granadero Baigorria)",
      "Rosario", "Santa Fe", "Argentina", "PPA", "inference", "Latin America",
      ["diesel engines and components", "ag tractors", "combine harvesters"],
      "domestic", "")
plant("campana", "John Deere Campana", "Campana", "Buenos Aires", "Argentina",
      "PPA", "inference", "Latin America", ["sprayer booms"], "domestic", "")
plant("las-rosas", "John Deere Las Rosas", "Las Rosas", "Santa Fe", "Argentina",
      "PPA", "inference", "Latin America", ["sprayers", "planters"], "domestic", "")
plant("monterrey", "Industrias John Deere SA de CV (Monterrey)", "Monterrey",
      "Nuevo Leon", "Mexico", "SAT;PPA;CF", "filing", "United States",
      ["components", "planters", "small skid-steer loaders", "mower conditioners",
       "rotary cutters"],
      "export", "Mexican plants feed US/global assembly and the US retail market; located in LatAm")
plant("ramos-arizpe", "John Deere Ramos Arizpe", "Ramos Arizpe", "Coahuila", "Mexico",
      "PPA;SAT", "inference", "United States",
      ["tractor-mounted loaders", "operator stations", "cabs", "hydraulic cylinders",
       "components"],
      "export", "took over large-tractor cab production moved from Waterloo, Iowa")
plant("saltillo", "John Deere Saltillo", "Saltillo", "Coahuila", "Mexico",
      "SAT;PPA", "inference", "United States",
      ["ag tractors", "transmissions", "axles", "electronics", "components"],
      "export", "")
plant("torreon", "Torreon Engine Factory", "Torreon", "Coahuila", "Mexico",
      "PPA;SAT;CF", "filing", "United States",
      ["diesel engines", "electronics", "axles"], "export", "")

# ---- WESTERN EUROPE --------------------------------------------------------
plant("mannheim", "John Deere Werke Mannheim", "Mannheim", "Baden-Wuerttemberg",
      "Germany", "SAT;PPA", "filing", "Western Europe",
      ["mid-size ag tractors (5R/6M/6R)", "European headquarters"],
      "export", "largest Deere plant in Europe; tractors exported worldwide")
plant("zweibruecken", "John Deere Werke Zweibruecken", "Zweibruecken", "Rhineland-Palatinate",
      "Germany", "PPA;SAT", "filing", "Western Europe",
      ["combine harvesters", "self-propelled forage harvesters"],
      "export", "sole European combine/forager plant; serves EMEA and export")
plant("bruchsal", "John Deere Bruchsal", "Bruchsal", "Baden-Wuerttemberg", "Germany",
      "PPA;SAT", "inference", "Western Europe",
      ["operator cabs for tractors, combines, foragers and sprayers",
       "European parts distribution centre"],
      "domestic", "captive cab supplier to Mannheim and Zweibruecken")
plant("stadtlohn", "John Deere Kemper Stadtlohn", "Stadtlohn", "North Rhine-Westphalia",
      "Germany", "PPA", "inference", "Western Europe",
      ["forage harvester headers", "pickups", "tractor-mounted choppers"],
      "export", "")
plant("windhagen", "Wirtgen GmbH", "Windhagen", "Rhineland-Palatinate", "Germany",
      "CF", "filing", "Western Europe",
      ["cold milling machines", "recyclers", "slipform pavers", "surface miners",
       "Wirtgen Group headquarters"], "export", "")
plant("goeppingen", "Kleemann GmbH", "Goeppingen", "Baden-Wuerttemberg", "Germany",
      "CF", "filing", "Western Europe", ["mobile crushers", "screening plants"],
      "export", "")
plant("ludwigshafen", "Joseph Voegele AG", "Ludwigshafen am Rhein", "Rhineland-Palatinate",
      "Germany", "CF", "filing", "Western Europe", ["asphalt pavers"], "export", "")
plant("tirschenreuth", "Hamm AG", "Tirschenreuth", "Bavaria", "Germany", "CF", "filing",
      "Western Europe", ["compactors", "rollers"], "export", "")
plant("wittlich", "Benninghoven (Wittlich / Muelheim an der Mosel)", "Wittlich",
      "Rhineland-Palatinate", "Germany", "CF", "inference", "Western Europe",
      ["stationary asphalt mixing plants", "mobile asphalt plants", "granulators"],
      "export", "")
plant("saran", "Saran Engine Factory (John Deere Power Systems)", "Saran", "Centre-Val de Loire",
      "France", "SAT;PPA;CF", "filing", "Western Europe",
      ["diesel engines 2.9L/4.5L/6.8L", "engine product engineering"],
      "mixed", "majority of output is captive to Deere equipment plants; remainder sold to third-party OEMs")
plant("arc-les-gray", "John Deere Arc-les-Gray", "Arc-les-Gray", "Bourgogne-Franche-Comte",
      "France", "SAT;PPA", "inference", "Western Europe",
      ["balers", "mower conditioners", "front loaders", "feederhouses"], "export", "")
plant("largeasse", "Monosem Largeasse", "Largeasse", "Nouvelle-Aquitaine", "France",
      "PPA", "inference", "Western Europe", ["precision planters"], "export", "")
plant("moncoutant", "Monosem Moncoutant", "Moncoutant", "Nouvelle-Aquitaine", "France",
      "PPA", "inference", "Western Europe", ["precision planters"], "export", "")
plant("getafe", "John Deere Iberica S.A. (Getafe)", "Getafe", "Madrid", "Spain",
      "PPA;CF;SAT", "filing", "Western Europe",
      ["transmissions", "final drives and gearboxes", "gears and shafts"],
      "export", "captive component plant supplying Deere assembly plants worldwide")
plant("valencia", "John Deere Valencia", "Valencia", "Valencia", "Spain", "PPA",
      "inference", "Western Europe", ["sprayer booms"], "export", "")
plant("joensuu", "John Deere Forestry Oy Joensuu", "Joensuu", "North Karelia", "Finland",
      "CF", "filing", "Western Europe",
      ["cut-to-length forestry harvesters", "forwarders", "harvesting heads"],
      "export", "Deere: world's largest forest machine factory; output overwhelmingly exported")
plant("horst", "John Deere Horst (Douven)", "Horst", "Limburg", "Netherlands", "PPA",
      "inference", "Western Europe", ["trailed and mounted spraying equipment"],
      "export", "")
plant("ravenna", "John Deere Ravenna", "Ravenna", "Emilia-Romagna", "Italy", "PPA",
      "inference", "Western Europe", ["sprayers"], "export", "")
plant("rainbach", "John Deere (Kreisel) Rainbach", "Rainbach im Muehlkreis", "Upper Austria",
      "Austria", "PPA;SAT;CF", "inference", "Western Europe",
      ["electric battery development", "battery packs"],
      "domestic", "primarily development/innovation site per Deere locations list")

# ---- ASIA / AFRICA / OCEANIA / MIDDLE EAST ---------------------------------
plant("pune", "John Deere Pune Works", "Pune (Sanaswadi)", "Maharashtra", "India",
      "SAT;CF", "filing", "Asia/Africa/Oceania/Middle East",
      ["ag tractors", "engines", "transmissions", "electronics",
       "road rollers, screens, pavers and stackers (Wirtgen India)"],
      "export", "India tractor exports are a material share of Deere small-tractor volume")
plant("dewas", "John Deere Dewas", "Dewas", "Madhya Pradesh", "India", "SAT",
      "inference", "Asia/Africa/Oceania/Middle East",
      ["small ag tractors"], "mixed", "Deere: builds small tractors for India and export to nearby markets")
plant("tianjin", "John Deere Tianjin Works", "Tianjin", "Tianjin", "China", "PPA;CF",
      "inference", "Asia/Africa/Oceania/Middle East",
      ["ag tractors", "4WD loaders", "hydraulic excavators", "transmissions"],
      "domestic", "China plants primarily serve the domestic Chinese market")
plant("jiamusi", "John Deere Jiamusi", "Jiamusi", "Heilongjiang", "China", "PPA",
      "inference", "Asia/Africa/Oceania/Middle East",
      ["combine harvesters", "cotton harvesting equipment"], "domestic", "")
plant("langfang", "Wirtgen China (Langfang)", "Langfang", "Hebei", "China", "CF",
      "inference", "Asia/Africa/Oceania/Middle East",
      ["milling machines", "pavers", "rollers"], "domestic", "")
plant("beit-hashita", "John Deere Beit Hashita", "Beit Hashita", "Northern District",
      "Israel", "PPA", "inference", "Asia/Africa/Oceania/Middle East",
      ["cotton picker repair parts", "cotton picker row units"], "export", "")
plant("tokoroa", "Waratah Forestry Equipment Tokoroa", "Tokoroa", "Waikato",
      "New Zealand", "CF", "inference", "Asia/Africa/Oceania/Middle East",
      ["forestry harvesting heads"], "export", "")

# ---------------------------------------------------------------------------
# Emit one products_count row per plant -- this is the spine.
# ---------------------------------------------------------------------------
for slug, d in P.items():
    notes = (f"geo_cell={d['geo_cell']}; seg_src={d['seg_src']}; "
             f"orientation={d['orientation']}"
             + (f"; orientation_basis={d['orientation_basis']}" if d['orientation_basis'] else "")
             + "; products=" + " | ".join(d["products"]))
    add(f"plant.{slug}.products_count", "2025-12-01", d["name"], d["city"], d["region"],
        d["country"], d["segment"], "products_count", len(d["products"]), "count",
        "company-site", WWPDF, notes)


def fact(slug, date, metric, value, units, stype, source, note=""):
    d = P[slug]
    add(f"plant.{slug}.{metric}", date, d["name"], d["city"], d["region"], d["country"],
        d["segment"], metric, value, units, stype, source, note)


# ---------------------------------------------------------------------------
# YEAR OPENED (Deere factory microsites unless noted)
# ---------------------------------------------------------------------------
FS = "https://www.deere.com/en-us/our-company/locations/factories/"
fact("east-moline", "1912-01-01", "year_opened", 1912, "year", "company-site",
     FS + "harvester-works", "Deere factory timeline: factory opened 1912")
fact("dubuque", "1946-05-01", "year_opened", 1946, "year", "company-site",
     FS + "dubuque-works", "opened May 1946")
fact("davenport", "1974-01-01", "year_opened", 1974, "year", "company-site",
     FS + "davenport-works", "first 4WD loader production 1974; 50th anniversary 2024")
fact("des-moines", "1947-01-01", "year_opened", 1947, "year", "company-site",
     FS + "des-moines-works", "Deere bought the WWII ordnance plant from DoD in 1947; first machine 1948")
fact("horicon", "1911-01-01", "year_opened", 1911, "year", "company-site",
     FS + "horicon-works", "site founded 1861 by Van Brunt; John Deere purchased it in 1911")
fact("thibodaux", "1965-01-01", "year_opened", 1965, "year", "company-site",
     FS + "thibodaux", "first cane loaders 1965 (Cameco lineage; Deere partnership from 1987)")
fact("waterloo", "1918-01-01", "year_opened", 1918, "year", "company-site",
     FS + "waterloo", "Deere purchased the Waterloo Gasoline Engine Company in 1918")
fact("kernersville", "1988-01-01", "year_opened", 1988, "year", "company-site",
     FS + "kernersville", "excavator production begins 1988")
fact("fuquay-varina", "1997-01-01", "year_opened", 1997, "year", "news",
     "https://www.lawnandlandscape.com/news/ll-072717-john-deere-turf-care-anniversary/",
     "Turf Care facility opened 1997 (20th anniversary reported 2017)")
fact("saran", "1963-01-01", "year_opened", 1963, "year", "news",
     "https://www.terre-net.fr/john-deere/article/116939/john-deere-power-system-le-made-in-france-de-l-americain",
     "engine plant at Saran since 1963")
fact("joensuu", "1972-01-01", "year_opened", 1972, "year", "news",
     "https://forestmachinemagazine.com/50-years-of-joensuu-forest-machine-factory/",
     "Rauma-Repola machine shop established Joensuu 1972; Deere acquired Timberjack lineage")

# ---------------------------------------------------------------------------
# SITE SIZE
# ---------------------------------------------------------------------------
fact("kernersville", "2024-05-01", "site_area_sqft", 1700000, "sqft", "company-site",
     FS + "kernersville", "campus floor space ~1.7m sqft")
fact("kernersville", "2024-05-01", "site_area_acres", 111, "acres", "company-site",
     FS + "kernersville", "expanded from 52 to 111 acres")
fact("des-moines", "2025-01-01", "site_area_acres", 450, "acres", "company-site",
     FS + "des-moines-works", "Deere: 'spans more than 450 acres'")
fact("augusta", "2016-01-01", "site_area_sqft", 400000, "sqft", "company-site",
     "https://www.machinefinder.com/ww/en-US/articles/one-millionth-john-deere-tractor-built-at-augusta-factory-2608",
     "'more than 400,000 square feet'; lower bound")
fact("augusta", "2016-01-01", "site_area_acres", 175, "acres", "company-site",
     "https://www.machinefinder.com/ww/en-US/articles/one-millionth-john-deere-tractor-built-at-augusta-factory-2608",
     "'more than 175 acres'; lower bound")
fact("fuquay-varina", "2017-07-01", "site_area_sqft", 335000, "sqft", "news",
     "https://www.lawnandlandscape.com/news/ll-072717-john-deere-turf-care-anniversary/", "")
fact("horicon", "2020-01-01", "site_area_sqft", 800000, "sqft", "news",
     "https://www.co.dodge.wi.gov/workforce/industries",
     "downtown plant only; south-side operations additional")
fact("pune", "2020-01-01", "site_area_acres", 112, "acres", "company-site",
     "https://www.deere.co.in/en/john-deere-technology-center/",
     "112 acres with ~50,000 sqm (538,000 sqft) covered area, Sanaswadi")
fact("dubuque", "1946-05-01", "site_area_acres", 742, "acres", "company-site",
     FS + "dubuque-works", "1946 figure: 600,000 sqft on 742 acres; floor space much larger today")

# ---------------------------------------------------------------------------
# EMPLOYEES -- plant level. Every row dated and sourced. Coverage is partial.
# metric 'employees' = total site headcount; 'employees_production' = production
# and maintenance (UAW-represented) headcount only.
# ---------------------------------------------------------------------------
fact("waterloo", "2024-03-01", "employees", 5500, "persons", "news",
     "https://www.wsws.org/en/articles/2024/03/30/deer-m30.html",
     "Waterloo-area Deere operations; 3,600 of them production")
fact("waterloo", "2024-03-01", "employees_production", 3600, "persons", "news",
     "https://www.wsws.org/en/articles/2024/03/30/deer-m30.html", "")
fact("waterloo", "2024-10-01", "employees", 4700, "persons", "news",
     "https://www.aol.com/john-deere-continues-2024-layoffs-153602564.html",
     "after 2024 layoff rounds; ~2,700 production and maintenance")
fact("waterloo", "2024-10-01", "employees_production", 2700, "persons", "news",
     "https://www.aol.com/john-deere-continues-2024-layoffs-153602564.html", "")

fact("east-moline", "2023-01-01", "employees", 2300, "persons", "news",
     "https://www.farm-equipment.com/articles/21752-deere-announces-layoffs-at-east-moline-harvester-works",
     "~1,975 in production and maintenance; figure predates 2024-25 layoffs")
fact("east-moline", "2023-01-01", "employees_production", 1975, "persons", "news",
     "https://www.farm-equipment.com/articles/21752-deere-announces-layoffs-at-east-moline-harvester-works", "")

fact("moline-seeding-cylinder", "2024-06-01", "employees", 890, "persons", "news",
     "https://www.wqad.com/article/news/local/john-deere-lay-off-120-employees-seeding-cylinder-plant/526-6bf560b4-d2b6-4a21-90db-935a53ffc92f",
     "~690 production and maintenance")
fact("moline-seeding-cylinder", "2024-06-01", "employees_production", 690, "persons", "news",
     "https://www.wqad.com/article/news/local/john-deere-lay-off-120-employees-seeding-cylinder-plant/526-6bf560b4-d2b6-4a21-90db-935a53ffc92f", "")
fact("moline-seeding-cylinder", "2024-10-01", "employees", 625, "persons", "news",
     "https://www.wqad.com/article/news/local/john-deere-additional-layoffs-moline-cylinder-works/526-48fe43bf-8d71-4830-b5d8-96b92489e267",
     "~427 production and maintenance after October 2024 cuts")
fact("moline-seeding-cylinder", "2024-10-01", "employees_production", 427, "persons", "news",
     "https://www.wqad.com/article/news/local/john-deere-additional-layoffs-moline-cylinder-works/526-48fe43bf-8d71-4830-b5d8-96b92489e267", "")

fact("des-moines", "2024-03-01", "employees", 1700, "persons", "news",
     "https://www.weareiowa.com/article/money/business/john-deere-des-moines-works-ankeny-location-layoffs-production/524-8dda4a34-b9b2-428a-8b3b-a149d798674a",
     "1,136 production and maintenance")
fact("des-moines", "2024-03-01", "employees_production", 1136, "persons", "news",
     "https://www.weareiowa.com/article/money/business/john-deere-des-moines-works-ankeny-location-layoffs-production/524-8dda4a34-b9b2-428a-8b3b-a149d798674a", "")
fact("des-moines", "2025-03-01", "employees", 1500, "persons", "news",
     "https://www.yahoo.com/news/ankeny-john-deere-facility-lay-193925445.html",
     "'nearly 1,500' at the time of the March/April 2025 layoff of 119")

fact("dubuque", "2024-01-01", "employees", 3000, "persons", "news",
     "https://biztimes.biz/john-deere-dubuque-works-marks-75-years-of-growth-innovation/",
     "'about 3,000'; largest employer in Dubuque County. Approximate, rounded by source")

fact("ottumwa", "2022-07-01", "employees", 800, "persons", "news",
     "https://blog.machinefinder.com/27887/john-deere-ottumwa-works", "")
fact("ottumwa", "2024-11-01", "employees", 400, "persons", "news",
     "https://www.kcrg.com/2024/11/15/ottumwa-john-deere-facility-shut-down-temporarily-again-amid-reduced-demand/",
     "reported as 'less than 400'; treat as an upper bound, not a point estimate")

fact("horicon", "2024-01-01", "employees", 1200, "persons", "news",
     "https://www.co.dodge.wi.gov/workforce/industries",
     "sources range ~1,000-1,200 across downtown (~700) and south-side (~500) operations")

fact("greeneville", "2024-08-08", "employees", 600, "persons", "news",
     "https://www.tn.gov/ecd/news/2024/8/8/john-deere-power-products-to-expand-manufacturing-presence-in-greene-county.html",
     "'slightly more than 600'; +25 jobs committed with a $15m expansion through 2025")

fact("augusta", "2016-01-01", "employees", 470, "persons", "news",
     "https://www.machinefinder.com/ww/en-US/articles/one-millionth-john-deere-tractor-built-at-augusta-factory-2608",
     "dated figure - 2016 vintage; no newer public headcount found")

fact("coffeyville", "2024-07-01", "employees", 245, "persons", "news",
     "https://www.ourquadcities.com/news/local-news/deere-announces-layoffs-at-waterloo-and-coffeyville/",
     "~145 in production")
fact("coffeyville", "2024-07-01", "employees_production", 145, "persons", "news",
     "https://www.ourquadcities.com/news/local-news/deere-announces-layoffs-at-waterloo-and-coffeyville/", "")

fact("valley-city", "2017-01-01", "employees", 330, "persons", "news",
     "https://www.inforum.com/business/john-deeres-20-million-expansion-in-valley-city-could-add-100-jobs",
     "'more than 330 full-time'; dated 2017, largest employer in Valley City")

fact("thibodaux", "2022-01-01", "employees", 284, "persons", "company-site",
     "https://www.opportunitylouisiana.gov/news/john-deere-thibodaux-plant-expansion-to-create-70-bayou-region-jobs",
     "284 jobs retained under the 2022 expansion agreement; +70 new direct jobs committed")

fact("kernersville", "2024-05-01", "employees", 600, "persons", "news",
     "https://journalnow.com/news/local/business/development/article_b204fb94-5ff2-4618-9eba-6aee803fc2dc.html",
     "~600 salaried and production; expected to rise toward ~840 with the $70m excavator plant")

fact("mannheim", "2025-01-01", "employees", 3600, "persons", "company-site",
     "https://www.zukunftsindustrie.de/m-e-erleben/stellen-mehr/john-deere-werk-mannheim-mannheim-30998",
     "largest Deere plant in Europe; figure includes the European HQ campus")
fact("zweibruecken", "2025-01-01", "employees", 1000, "persons", "news",
     "https://www.wiwo.de/erfolg/management/john-deere-in-zweibruecken-oftmals-werden-stellen-einfach-abgebaut-das-war-fuer-uns-keine-loesung/30208762.html",
     "~1,000; Deere used a paid qualification sabbatical and a 35->32h week instead of layoffs")
fact("bruchsal", "2025-01-01", "employees", 800, "persons", "news",
     "https://www.wiwo.de/erfolg/management/john-deere-in-zweibruecken-oftmals-werden-stellen-einfach-abgebaut-das-war-fuer-uns-keine-loesung/30208762.html",
     "cab plant supplying Mannheim and Zweibruecken")
fact("saran", "2023-01-01", "employees", 850, "persons", "news",
     "https://www.terre-net.fr/john-deere/article/116939/john-deere-power-system-le-made-in-france-de-l-americain",
     "850 permanent staff on six covered hectares; a second source says ~800")
fact("joensuu", "2022-01-01", "employees", 800, "persons", "news",
     "https://businessjoensuu.fi/en/10-facts-about-joensuu", "")
fact("getafe", "2026-01-01", "employees", 1114, "persons", "company-site",
     "https://www.einforma.com/informacion-empresa/john-deere-iberica",
     "John Deere Iberica S.A. legal-entity headcount from the Spanish commercial registry; "
     "entity is dominated by the Getafe plant but is not strictly plant-level")
fact("montenegro", "2024-01-01", "employees", 900, "persons", "news",
     "https://revistacultivar.com.br/noticias/john-deere-comemora-uma-decada-de-producao-de-tratores-em-montenegro-rs",
     "'more than 900 direct'; ~100 indirect additional")
fact("horizontina", "2024-02-01", "employees", 1700, "persons", "news",
     "https://agfeed.com.br/negocios/a-espera-da-recuperacao-john-deere-da-ferias-coletivas-e-layoff-a-trabalhadores-e-reduz-producao-no-rs/",
     "combine + planter plant, Feb 2024; CONFLICTS with a Feb-2025 report of 700 - see plants.md")
fact("horizontina", "2025-02-01", "employees", 700, "persons", "news",
     "https://agfeed.com.br/economia/com-vendas-em-queda-fabrica-da-john-deere-no-rs-opera-com-capacidade-reduzida/",
     "reported for the combine operation specifically; may be a narrower scope than the 2024 figure")

# ---------------------------------------------------------------------------
# COMPANY-LEVEL EMPLOYEE TIME SERIES (Deere 10-K Item 1, 'Employees') --
# the calibration anchor for the plant-level signal.
# ---------------------------------------------------------------------------
CORP = [
    ("2015-10-31", 57200, 28500, None, "2015-11-25__de-us-20151125-q4-10k__469104.md"),
    ("2016-10-30", 56800, 27900, None, "2016-11-23__de-us-20161123-q4-10k__469184.md"),
    ("2017-10-29", 60500, 29000, None, "2017-11-22__de-us-20171122-q4-10k__468364.md"),
    ("2018-10-28", 74000, 31000, None, "2018-11-21__de-us-20181121-q4-10k__469201.md"),
    ("2019-11-03", 73500, 30000, None, "2019-11-27__de-us-20191127-q4-10k__469283.md"),
    ("2020-11-01", 69600, 27500, None, "2020-11-25__de-us-20201125-q4-10k__105845.md"),
    ("2021-10-31", 75600, 29000, None, "2021-11-24__de-us-20211124-q4-10k__131650.md"),
    ("2022-10-30", 82200, 32000, None, "2022-11-23__de-us-20221123-q4-10k__105816.md"),
    ("2023-10-29", 83000, 33800, None, "2023-11-22__de-us-20231122-q4-10k__105844.md"),
    ("2024-11-03", 75800, 29600, 35200, "2024-11-21__de-us-20241121-q4-10k__105810.md"),
    ("2025-11-02", 73100, 27000, 32500, "2025-11-26__de-us-20251126-q4-10k__469216.md"),
]
for date, tot, us, prod, src in CORP:
    s = "Deere FY10-K Item 1 'Employees', offline-data/deere/filings/" + src
    add("company.employees_total", date, "ALL - Deere & Company (worldwide)", "", "",
        "Worldwide", "PPA;SAT;CF;FS", "employees", tot, "persons", "filing", s,
        "10-K disclosed total employees at fiscal year end")
    add("company.employees_us", date, "ALL - Deere & Company (United States)", "",
        "", "United States", "PPA;SAT;CF;FS", "employees", us, "persons", "filing", s,
        "US employees at fiscal year end")
    if prod:
        add("company.employees_production_ww", date,
            "ALL - Deere & Company (worldwide)", "", "", "Worldwide",
            "PPA;SAT;CF", "employees_production", prod, "persons", "filing", s,
            "full-time production employees worldwide; disclosure format changed in FY2024")

# FY2025 also discloses US full-time production employees explicitly
add("company.employees_production_us", "2025-11-02",
    "ALL - Deere & Company (United States)", "", "", "United States", "PPA;SAT;CF",
    "employees_production", 11600, "persons", "filing",
    "Deere FY2025 10-K Item 1 'Employees', offline-data/deere/filings/2025-11-26__de-us-20251126-q4-10k__469216.md",
    "approximately 11,600 full-time US production employees; 77% of US production and "
    "maintenance employees unionised; ~7,600 covered by the UAW agreement expiring 2027-11-01")

# Structural counts from 10-K Item 2
add("company.factory_count_us_canada", "2025-11-02", "ALL - Deere & Company (US/Canada)",
    "", "", "United States;Canada", "PPA;SAT;CF", "products_count", 27, "count",
    "filing", TENK,
    "23 owned + 4 leased equipment-operations factory locations in the US and Canada")
add("company.factory_count_intl", "2025-11-02", "ALL - Deere & Company (ex-US/Canada)",
    "", "", "Worldwide", "PPA;SAT;CF", "products_count", 45, "count", "filing", TENK,
    "45 owned or leased factory locations outside the US and Canada")

# ---------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT), exist_ok=True)
cols = ["series_id", "date", "plant", "city", "state_or_region", "country", "segment",
        "metric", "value", "units", "source_type", "source", "notes"]
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow(r)
print(f"wrote {len(rows)} rows to {OUT}")
print(f"plants in spine: {len(P)}")
emp = {r['plant'] for r in rows if r['metric'] in ('employees', 'employees_production')
       and not r['plant'].startswith('ALL')}
print(f"plants with a headcount observation: {len(emp)}")
