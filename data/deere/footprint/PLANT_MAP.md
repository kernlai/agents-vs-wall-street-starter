# Deere & Company — consolidated manufacturing footprint (PLANT_MAP)

Built 2026-08-16 from five independent collection passes. **Deere has not reported
FY2026 Q3** — the earnings call is 2026-08-20, after this file was written. Nothing
here is a Q3 FY2026 actual.

Regenerate with `python3 scripts/data/de_build_plant_map.py`.
Companion indicator file: `HIRING_TRACKER.md`.

---

## 1. Coverage, stated before the data

| | count | of 62 |
|---|---:|---:|
| Sites enumerated (name, city, country, products, segment, geography) | 62 | 100% |
| Segment attribution from a filing rather than inferred | 26 | 41% |
| **Any site headcount at all** | **21** | **33%** |
| Headcount dated 2024 or later | 15 | 24% |
| Production-only headcount | 5 | 8% |

**Deere does not disclose plant-level headcount anywhere.** The 10-K gives one worldwide
total, one US total, and (since FY2024) a production sub-total. Every site number below was
reconstructed from local news or an economic-development announcement, which biases the
sample hard: most of these stories exist *because* a plant was cutting, so the figures
cluster on shrinking plants and are usually snapshots taken immediately before a cut.
Treat each as a dated point estimate with its own provenance, **not** as a panel.

**Two corrections applied during consolidation**, both found by recomputing from the raw
CSV rather than trusting the collecting agent's own summary:

- The source file tags **27** sites as filing-sourced on segment. The FY2025 10-K Item 2 table
  actually lists exactly **26 locations** (28 named facilities — Waterloo bundles Engine
  Works, the Foundry and Waterloo Works under one row). **Moline Seeding & Cylinder Works is
  not in it.** Its PPA assignment is almost certainly right but it is inferred, and it is
  re-tagged `i` below.
- Distinct-plant counts corrected: **15** plants (not 17) have a headcount observation dated
  2024 or later, and **5** plants (not 6) have a production-only figure — the higher numbers
  counted rows, and Waterloo and Moline each contribute two.

Deere's own FY2025 10-K Item 2 discloses the structural totals: **23 owned + 4 leased**
factory locations in the US and Canada and **45** outside — roughly **72 factories**. This
file names 62. **About ten factories are therefore missing entirely and cannot be named.**

---

## 2. The plant table

`seg src` = `F` where the FY2025 10-K Item 2 table names the site and its segment, `i` where
segment is inferred from the product list. `geo cell` maps the site to the revenue-by-geography
disclosure used elsewhere in this project, and is an analytical judgement, not a disclosed fact.

| # | Plant | City | Country | Segment | seg src | Geo cell | Employees | as of | Headcount source | Products |
|---:|---|---|---|---|:---:|---|---:|---|---|---|
| 1 | John Deere Waterloo Works / Engine Works / Foundry / Drivetrain | Waterloo | United States | PPA;CF | F | United States | 4,700<br><sub>2,700 prod</sub> | 2024-10-01 | aol.com | large ag tractors (7/8/9 Series) , diesel engines , drivetrain components , foundry castings , product engineering |
| 2 | John Deere Dubuque Works | Dubuque | United States | CF | F | United States | 3,000 | 2024-01-01 | biztimes.biz | backhoe loaders , compact track loaders , crawler dozers , high-speed dozers , knuckleboom loaders , skid-steer loaders , tracked feller bunchers , tracked harvesters |
| 3 | John Deere Harvester Works | East Moline | United States | PPA | F | United States | 2,300<br><sub>1,975 prod</sub> | 2023-01-01 | farm-equipment.com | combine harvesters (S/X Series) , corn heads , draper platforms , combine product engineering |
| 4 | John Deere Des Moines Works | Ankeny (Des Moines) | United States | PPA | F | United States | 1,500<br><sub>1,136 prod</sub> | 2025-03-01 | yahoo.com | seeding equipment , sprayers , tillage equipment , cotton harvesters |
| 5 | John Deere Horicon Works | Horicon | United States | SAT | F | United States | 1,200 | 2024-01-01 | co.dodge.wi.gov | Gator utility vehicles , lawn and garden tractors (X300/500/700/900) , golf and turf reel mowers , walk-behind greens mowers |
| 6 | John Deere Seeding Group / Cylinder Works (Moline) | Moline | United States | PPA | i | United States | 625<br><sub>427 prod</sub> | 2024-10-01 | wqad.com | planters and seeding equipment , hydraulic cylinders , performance upgrade kits |
| 7 | John Deere Greeneville (John Deere Power Products) | Greeneville | United States | SAT | F | United States | 600 | 2024-08-08 | tn.gov | riding lawn equipment , residential mowers |
| 8 | John Deere Kernersville Campus | Kernersville | United States | CF | F | United States | 600 | 2024-05-01 | journalnow.com | mid-size hydraulic excavators , small excavators (west campus, from 2026) , Kreisel battery packs |
| 9 | John Deere Augusta Works (North and South factories) | Augusta / Grovetown | United States | SAT | F | United States | 470 | 2016-01-01 | machinefinder.com | compact utility tractors (1/2/3/4 Family) , utility tractors |
| 10 | John Deere Ottumwa Works | Ottumwa | United States | SAT | i | United States | 400 | 2024-11-01 | kcrg.com | hay and forage equipment , large square balers , round balers , self-propelled windrowers |
| 11 | John Deere Seeding Group Valley City | Valley City | United States | PPA | i | United States | 330 | 2017-01-01 | inforum.com | air seeders , commodity carts , tillage equipment |
| 12 | John Deere Thibodaux | Thibodaux | United States | PPA;CF | i | United States | 284 | 2022-01-01 | opportunitylouisiana.gov | sugarcane harvesters , cotton stripper heads , scrapers , cane loaders , airbooms |
| 13 | John Deere Coffeyville Works (Funk Manufacturing) | Coffeyville | United States | CF;PPA | i | United States | 245<br><sub>145 prod</sub> | 2024-07-01 | ourquadcities.com | power transmission equipment , drivetrain and power-system components |
| 14 | Industrias John Deere SA de CV (Monterrey) | Monterrey | Mexico | SAT;PPA;CF | F | United States | unknown | — | — | components , planters , small skid-steer loaders , mower conditioners , rotary cutters |
| 15 | John Deere Clarion (Hagie) | Clarion | United States | PPA | i | United States | unknown | — | — | self-propelled sprayers , detasselers |
| 16 | John Deere Davenport Works | Davenport | United States | CF | F | United States | unknown | — | — | articulated dump trucks , cabs , felling heads , 4WD loaders , motor graders , skidders , wheeled feller bunchers |
| 17 | John Deere Electronic Solutions | Fargo | United States | PPA;SAT;CF | i | United States | unknown | — | — | electronic controllers , displays , precision-ag electronics |
| 18 | John Deere Paton | Paton | United States | PPA | i | United States | unknown | — | — | planting equipment , tillage equipment |
| 19 | John Deere Ramos Arizpe | Ramos Arizpe | Mexico | PPA;SAT | i | United States | unknown | — | — | tractor-mounted loaders , operator stations , cabs , hydraulic cylinders , components |
| 20 | John Deere Reman Springfield | Springfield | United States | PPA;SAT;CF | i | United States | unknown | — | — | remanufactured engines , remanufactured transmissions , axles and components |
| 21 | John Deere Rock Island (all-makes parts) | Rock Island | United States | unknown | i | United States | unknown | — | — | all-makes replacement parts |
| 22 | John Deere Rock Valley (all-makes parts) | Rock Valley | United States | unknown | i | United States | unknown | — | — | all-makes replacement parts manufacturing and distribution |
| 23 | John Deere Saltillo | Saltillo | Mexico | SAT;PPA | i | United States | unknown | — | — | ag tractors , transmissions , axles , electronics , components |
| 24 | John Deere Turf Care | Fuquay-Varina | United States | SAT | F | United States | unknown | — | — | commercial mowers , golf course mowers , turf utility vehicles |
| 25 | Torreon Engine Factory | Torreon | Mexico | PPA;SAT;CF | F | United States | unknown | — | — | diesel engines , electronics , axles |
| 26 | John Deere Altona (aftermarket ag parts) | Altona | Canada | unknown | i | Canada | unknown | — | — | aftermarket agricultural parts |
| 27 | John Deere Forestry Vancouver | Vancouver | Canada | CF | i | Canada | unknown | — | — | forestry swing machines , tracked feller bunchers , tracked harvesters |
| 28 | John Deere Werke Mannheim | Mannheim | Germany | SAT;PPA | F | Western Europe | 3,600 | 2025-01-01 | zukunftsindustrie.de | mid-size ag tractors (5R/6M/6R) , European headquarters |
| 29 | John Deere Iberica S.A. (Getafe) | Getafe | Spain | PPA;CF;SAT | F | Western Europe | 1,114 | 2026-01-01 | einforma.com | transmissions , final drives and gearboxes , gears and shafts |
| 30 | John Deere Werke Zweibruecken | Zweibruecken | Germany | PPA;SAT | F | Western Europe | 1,000 | 2025-01-01 | wiwo.de | combine harvesters , self-propelled forage harvesters |
| 31 | Saran Engine Factory (John Deere Power Systems) | Saran | France | SAT;PPA;CF | F | Western Europe | 850 | 2023-01-01 | terre-net.fr | diesel engines 2.9L/4.5L/6.8L , engine product engineering |
| 32 | John Deere Bruchsal | Bruchsal | Germany | PPA;SAT | i | Western Europe | 800 | 2025-01-01 | wiwo.de | operator cabs for tractors, combines, foragers and sprayers , European parts distribution centre |
| 33 | John Deere Forestry Oy Joensuu | Joensuu | Finland | CF | F | Western Europe | 800 | 2022-01-01 | businessjoensuu.fi | cut-to-length forestry harvesters , forwarders , harvesting heads |
| 34 | Benninghoven (Wittlich / Muelheim an der Mosel) | Wittlich | Germany | CF | i | Western Europe | unknown | — | — | stationary asphalt mixing plants , mobile asphalt plants , granulators |
| 35 | Hamm AG | Tirschenreuth | Germany | CF | F | Western Europe | unknown | — | — | compactors , rollers |
| 36 | John Deere (Kreisel) Rainbach | Rainbach im Muehlkreis | Austria | PPA;SAT;CF | i | Western Europe | unknown | — | — | electric battery development , battery packs |
| 37 | John Deere Arc-les-Gray | Arc-les-Gray | France | SAT;PPA | i | Western Europe | unknown | — | — | balers , mower conditioners , front loaders , feederhouses |
| 38 | John Deere Horst (Douven) | Horst | Netherlands | PPA | i | Western Europe | unknown | — | — | trailed and mounted spraying equipment |
| 39 | John Deere Kemper Stadtlohn | Stadtlohn | Germany | PPA | i | Western Europe | unknown | — | — | forage harvester headers , pickups , tractor-mounted choppers |
| 40 | John Deere Ravenna | Ravenna | Italy | PPA | i | Western Europe | unknown | — | — | sprayers |
| 41 | John Deere Valencia | Valencia | Spain | PPA | i | Western Europe | unknown | — | — | sprayer booms |
| 42 | Joseph Voegele AG | Ludwigshafen am Rhein | Germany | CF | F | Western Europe | unknown | — | — | asphalt pavers |
| 43 | Kleemann GmbH | Goeppingen | Germany | CF | F | Western Europe | unknown | — | — | mobile crushers , screening plants |
| 44 | Monosem Largeasse | Largeasse | France | PPA | i | Western Europe | unknown | — | — | precision planters |
| 45 | Monosem Moncoutant | Moncoutant | France | PPA | i | Western Europe | unknown | — | — | precision planters |
| 46 | Wirtgen GmbH | Windhagen | Germany | CF | F | Western Europe | unknown | — | — | cold milling machines , recyclers , slipform pavers , surface miners , Wirtgen Group headquarters |
| 47 | John Deere Brasil Ltda Montenegro | Montenegro | Brazil | PPA | F | Latin America | 900 | 2024-01-01 | revistacultivar.com.br | ag tractors |
| 48 | John Deere Brasil Ltda Horizontina | Horizontina | Brazil | PPA | F | Latin America | 700 | 2025-02-01 | agfeed.com.br | combine harvesters , headers , planting equipment |
| 49 | Industrias John Deere Argentina (Rosario/Granadero Baigorria) | Rosario | Argentina | PPA | i | Latin America | unknown | — | — | diesel engines and components , ag tractors , combine harvesters |
| 50 | John Deere Brasil Ltda Catalao | Catalao | Brazil | PPA | F | Latin America | unknown | — | — | sugarcane harvesters , self-propelled sprayers |
| 51 | John Deere Brazil Construction Factory (Indaiatuba) | Indaiatuba | Brazil | CF | F | Latin America | unknown | — | — | backhoe loaders , 4WD loaders , hydraulic excavators , crawler dozers , motor graders |
| 52 | John Deere Campana | Campana | Argentina | PPA | i | Latin America | unknown | — | — | sprayer booms |
| 53 | John Deere Canoas | Canoas | Brazil | PPA | i | Latin America | unknown | — | — | self-propelled sprayers |
| 54 | John Deere Las Rosas | Las Rosas | Argentina | PPA | i | Latin America | unknown | — | — | sprayers , planters |
| 55 | Wirtgen Group Porto Alegre (Ciber) | Porto Alegre | Brazil | CF | i | Latin America | unknown | — | — | milling machines , pavers , rollers , mobile asphalt mixing plants |
| 56 | John Deere Beit Hashita | Beit Hashita | Israel | PPA | i | Asia/Africa/Oceania/Middle East | unknown | — | — | cotton picker repair parts , cotton picker row units |
| 57 | John Deere Dewas | Dewas | India | SAT | i | Asia/Africa/Oceania/Middle East | unknown | — | — | small ag tractors |
| 58 | John Deere Jiamusi | Jiamusi | China | PPA | i | Asia/Africa/Oceania/Middle East | unknown | — | — | combine harvesters , cotton harvesting equipment |
| 59 | John Deere Pune Works | Pune (Sanaswadi) | India | SAT;CF | F | Asia/Africa/Oceania/Middle East | unknown | — | — | ag tractors , engines , transmissions , electronics , road rollers, screens, pavers and stackers (Wirtgen India) |
| 60 | John Deere Tianjin Works | Tianjin | China | PPA;CF | i | Asia/Africa/Oceania/Middle East | unknown | — | — | ag tractors , 4WD loaders , hydraulic excavators , transmissions |
| 61 | Waratah Forestry Equipment Tokoroa | Tokoroa | New Zealand | CF | i | Asia/Africa/Oceania/Middle East | unknown | — | — | forestry harvesting heads |
| 62 | Wirtgen China (Langfang) | Langfang | China | CF | i | Asia/Africa/Oceania/Middle East | unknown | — | — | milling machines , pavers , rollers |

### Sites with no headcount at all

**41 of 62 sites.** Listed so the hole is explicit rather than hidden:

> Industrias John Deere SA de CV (Monterrey) (Mexico); John Deere Clarion (Hagie) (United States); John Deere Davenport Works (United States); John Deere Electronic Solutions (United States); John Deere Paton (United States); John Deere Ramos Arizpe (Mexico); John Deere Reman Springfield (United States); John Deere Rock Island (all-makes parts) (United States); John Deere Rock Valley (all-makes parts) (United States); John Deere Saltillo (Mexico); John Deere Turf Care (United States); Torreon Engine Factory (Mexico); John Deere Altona (aftermarket ag parts) (Canada); John Deere Forestry Vancouver (Canada); Benninghoven (Wittlich / Muelheim an der Mosel) (Germany); Hamm AG (Germany); John Deere (Kreisel) Rainbach (Austria); John Deere Arc-les-Gray (France); John Deere Horst (Douven) (Netherlands); John Deere Kemper Stadtlohn (Germany); John Deere Ravenna (Italy); John Deere Valencia (Spain); Joseph Voegele AG (Germany); Kleemann GmbH (Germany); Monosem Largeasse (France); Monosem Moncoutant (France); Wirtgen GmbH (Germany); Industrias John Deere Argentina (Rosario/Granadero Baigorria) (Argentina); John Deere Brasil Ltda Catalao (Brazil); John Deere Brazil Construction Factory (Indaiatuba) (Brazil); John Deere Campana (Argentina); John Deere Canoas (Brazil); John Deere Las Rosas (Argentina); Wirtgen Group Porto Alegre (Ciber) (Brazil); John Deere Beit Hashita (Israel); John Deere Dewas (India); John Deere Jiamusi (China); John Deere Pune Works (India); John Deere Tianjin Works (China); Waratah Forestry Equipment Tokoroa (New Zealand); Wirtgen China (Langfang) (China)

The two that matter most:

- **Davenport Works (CF, Iowa)** — a top-five US site that absorbed 291 WARN-recorded layoffs
  across 2024–25 and 115 recalls across 2026, and for which no public total headcount exists.
  Every Davenport event is therefore unsizable against its own base.
- **The Wirtgen road-building plants** (Windhagen, Göppingen, Ludwigshafen, Tirschenreuth,
  Wittlich, Langfang, Porto Alegre). Wirtgen Group publishes a single ~8,900 worldwide figure
  and never a per-plant one. These plants drive the CF/Western Europe growth that the Q2 FY2026
  call attributes to roadbuilding, and they are completely dark to this indicator.

---

## 3. Segment × geography aggregation

This is the join that makes a plant event readable as a revenue signal: a Waterloo layoff is
evidence about **PPA / United States**; short-time working at Zweibrücken is evidence about
**PPA+SAT / Western Europe**; collective vacation at Horizontina is **PPA / Latin America**.
Never pool a signal across cells.

Reference magnitudes — FY2025 segment net sales ($m): PPA 17,311 · SAT 10,224 · CF 11,382.
Q2 FY2026 revenue by geography ($m): US 7,198 · Canada 1,039 · W. Europe 2,141 ·
C. Europe & CIS 525 · Latin America 1,268 · Asia/Africa/Oceania/ME 1,198.

### 3a. By geography

`known headcount` sums only the sites that have a number, so it is a **floor**, and `blank`
says how many sites in that cell contribute nothing to it. A cell with a small known total and
many blanks is not a small cell — Asia/Africa/Oceania/ME booked $1,198m in Q2 FY2026 and has
**nine plants and not one headcount**.

| Geo cell | Plants | Sites w/ headcount | Known headcount (floor) | Blank |
|---|---:|---:|---:|---:|
| United States | 25 | 13 | 16,254 | 12 |
| Canada | 2 | 0 | — | 2 |
| Western Europe | 19 | 6 | 8,164 | 13 |
| Central Europe & CIS | 0 | 0 | — | — |
| Latin America | 9 | 2 | 1,600 | 7 |
| Asia/Africa/Oceania/Middle East | 7 | 0 | — | 7 |

### 3b. By segment — plant counts only

**Headcount is deliberately not totalled by segment.** Sixteen sites serve more than one
segment (Waterloo is PPA+CF; Mannheim is SAT+PPA; Getafe, Saran, Monterrey and Torreón are
all three) and Deere publishes no basis for apportioning a site's people between segments.
Any segment headcount total would be an invented split. Plant counts are given instead, and
a multi-segment site is counted once in each segment it serves, so these sum to more than 62.

| Segment | Plants | of which with a headcount | FY2025 net sales ($m) |
|---|---:|---:|---:|
| PPA | 38 | 14 | 17,311 |
| SAT | 20 | 9 | 10,224 |
| CF | 26 | 8 | 11,382 |
| (no segment — all-makes parts depots) | 3 | 0 | n/a |

Mexico is mapped to `geo_cell = United States` on functional grounds — see §4.

### 3c. The matrix, by name

| geo cell | PPA | SAT | CF |
|---|---|---|---|
| **United States** | Ankeny (Des Moines), Clarion*, Coffeyville, East Moline, Fargo*, Moline, Monterrey*, Paton*, Ramos Arizpe*, Saltillo*, Springfield*, Thibodaux, Torreon*, Valley City, Waterloo | Augusta / Grovetown, Fargo*, Fuquay-Varina*, Greeneville, Horicon, Monterrey*, Ottumwa, Ramos Arizpe*, Saltillo*, Springfield*, Torreon* | Coffeyville, Davenport*, Dubuque, Fargo*, Kernersville, Monterrey*, Springfield*, Thibodaux, Torreon*, Waterloo |
| **Canada** | — | — | Vancouver* |
| **Western Europe** | Arc-les-Gray*, Bruchsal, Getafe, Horst*, Largeasse*, Mannheim, Moncoutant*, Rainbach im Muehlkreis*, Ravenna*, Saran, Stadtlohn*, Valencia*, Zweibruecken | Arc-les-Gray*, Bruchsal, Getafe, Mannheim, Rainbach im Muehlkreis*, Saran, Zweibruecken | Getafe, Goeppingen*, Joensuu, Ludwigshafen am Rhein*, Rainbach im Muehlkreis*, Saran, Tirschenreuth*, Windhagen*, Wittlich* |
| **Central Europe & CIS** | — | — | — |
| **Latin America** | Campana*, Canoas*, Catalao*, Horizontina, Las Rosas*, Montenegro, Rosario* | — | Indaiatuba*, Porto Alegre* |
| **Asia/Africa/Oceania/Middle East** | Beit Hashita*, Jiamusi*, Tianjin* | Dewas*, Pune (Sanaswadi)* | Langfang*, Pune (Sanaswadi)*, Tianjin*, Tokoroa* |

`*` = no headcount known for that site.

**The empty cell is the informative one.** Central Europe & CIS booked $525m in Q2 FY2026 and
has **no Deere plant of its own** — it is supplied entirely from Western Europe. A Zweibrücken
or Mannheim slowdown therefore reads into two revenue cells at once, and no plant-level signal
will ever originate inside Central Europe & CIS. Russia is a confirmed exit, not a gap:
shipments suspended 2022-02-24, dealer agreements not renewed from 2022-11-01, financial
services sold in Q2 FY2023, Orenburg acquired by Koblik Group in 2023, and neither Orenburg nor
Domodedovo appears in Deere's December 2025 locations list.

---

## 4. Three mapping judgements you may want to reverse

1. **Mexico → United States.** Monterrey, Ramos Arizpe, Saltillo and Torreón are physically in
   Latin America, but their output is captive components, cabs and engines feeding US assembly
   and the US retail market, so they are keyed to `geo_cell = United States`. The `country`
   column is preserved so anyone can re-key on location instead. **Ramos Arizpe absorbed the
   large-tractor cab line moved out of Waterloo**, so Waterloo layoffs and Ramos Arizpe hiring
   are partly the *same* event. Do not count them twice.
2. **Ottumwa → SAT.** Not in the 10-K Item 2 table. Assigned SAT because hay and forage sits in
   Small Ag & Turf. If you disagree, the Ottumwa events (75 laid off Jan-2025, a four-week
   inventory-adjustment shutdown Dec-2024) move to PPA and change the segment read materially.
3. **Coffeyville → CF.** A drivetrain component plant feeding several assembly plants. Its
   April-2026 recall of 8 is tagged CF here but genuinely serves more than one segment.

---

## 5. Company-level anchor series — the part that *is* filing grade

From Item 1 'Employees' of each 10-K in the corpus. Verified verbatim against
`filings/2025-11-26__de-us-20251126-q4-10k__469216.md` for FY2025.

| FY end | Worldwide | US (+Canada to FY2023) | Full-time production WW | UAW-covered active US |
|---|---:|---:|---:|---:|
| 2015-10-31 | 57,200 | 28,500 | — | 10,000 |
| 2016-10-30 | 56,800 | 27,900 | — | 7,600 |
| 2017-10-29 | 60,500 | 29,000 | — | 8,700 |
| 2018-10-28 | 74,000 | 31,000 | — | 9,600 |
| 2019-11-03 | 73,500 | 30,000 | — | 9,300 |
| 2020-11-01 | 69,600 | 27,500 | — | 8,740 |
| 2021-10-31 | 75,600 | 29,000 | — | 10,500 |
| 2022-10-30 | 82,200 | 32,000 | — | 11,500 |
| 2023-10-29 | 83,000 | 33,800 | — | 11,500 |
| 2024-11-03 | 75,800 | 29,600 (US only) | 35,200 | 8,900 |
| 2025-11-02 | 73,100 | 27,000 (US only) | 32,500 | 7,600 |

FY2025 additionally: **~11,600 full-time US production employees**, unions certified for **77%**
of US production and maintenance staff, **~7,600 active US production workers under the UAW
agreement expiring 2027-11-01**. That 11,600 is the practical denominator for sizing any US
WARN or callback event; the 7,600 is the denominator for the union-covered subset.

Worldwide headcount is **−11.9%** from the FY2023 peak and US headcount **−20.1%**. US shrank
about twice as fast as the group. PPA is the most US-weighted segment, so that asymmetry is
itself a segment signal, and it lines up with FY2026 guidance of PPA −5% to −10%.

**Two breaks that must not be smoothed.** FY2015–FY2023 disclose 'US *and Canada*'; FY2024–FY2025
disclose 'US' only — never join them. And the FY2018 jump 60,500 → 74,000 is the Wirtgen
acquisition (~8,200 people), not a production signal. The UAW series also gains the word
'active' from FY2016, so the FY2015→FY2016 −24% is partly definitional.

---

## 6. What each site contributes to the indicator

Sites with at least one dated 2024–2026 labour event, which is the set the tracker actually
watches. Everything else in the table above is structural context.

Layoffs are bucketed by **effective date**, recalls and new hires by announcement date.

| Plant | Segment | pre-2024 layoffs | 2024–25 layoffs | 2026 recalls + new hires | 2024→2026 net |
|---|---|---:|---:|---:|---:|
| John Deere Waterloo Works / Engine Works / Foundry / Drivetrain | PPA;CF | — | 1,247 | 146 | -1,101 |
| John Deere Harvester Works | PPA | 425 | 415 | 0 | -415 |
| John Deere Davenport Works | CF | — | 291 | 115 | -176 |
| John Deere Des Moines Works | PPA | — | 325 | 0 | -325 |
| John Deere Dubuque Works | CF | — | 133 | 102 | -31 |
| John Deere Ottumwa Works | SAT | — | 75 | 0 | -75 |
| John Deere Seeding Group / Cylinder Works (Moline) | PPA | 220 | 52 | 0 | -52 |
| John Deere Coffeyville Works (Funk Manufacturing) | CF;PPA | — | 0 | 8 | +8 |

The pre-2024 column holds only the two events the archives reach: **425 at Harvester Works**
(notice 2014-08-20, effective 2014-10-20, permanent, UAW Local 865 — the largest single Deere
WARN event in the entire 1999–2026 Illinois archive) and **220 at Moline Seeding & Cylinder**
(Deere press release 2015-11-30, no corresponding Illinois WARN record). Iowa's WARN database
does not start until 2021-08-18, so pre-2021 Iowa is invisible and those columns are not
comparable across plants.

Salaried, corporate and financial-services WARN rows (World Headquarters 298, Intelligent
Solutions Group 59, John Deere Financial 67) are **excluded** — they are headcount, not build
rate. So is the 2018 Eurest Services notice (79 food-service contractors at three Deere Quad
Cities sites), which is not Deere payroll at all.

Note what is **absent** from that table: Harvester Works in East Moline — the sole North
American combine plant and the core of PPA — took 415 cuts across 2024–25 (279 + 21 by WARN,
plus a 115-worker action in August 2025 that fell below the Illinois WARN threshold and was
never filed) and received **nothing** in 2026. Read alongside PPA guidance of −5% to −10%,
that silence is the single most informative row in the whole footprint.

---

## 7. Maintaining this

- Re-pull `deere.com/assets/pdfs/common/our-company/about/jd-world-locations.pdf` each
  December; Deere re-dates it annually and it is the cheapest way to catch openings, closures
  and product moves.
- Re-read 10-K Item 2 each November for segment reassignments and the owned/leased counts.
- Headcount rows will always be hand-maintained from news. Update a plant only when a WARN
  notice or a local story restates the base. **Never carry a headcount forward more than four
  quarters without re-sourcing it** — mark it stale instead. Augusta (470, 2016) and Valley City
  (330, 2017) are already stale and are kept only because they are the only numbers that exist.
- Known conflicts left unreconciled on purpose: Horizontina 1,700 (Feb-2024, combine + planter)
  vs 700 (Feb-2025, combine operation only) — different scopes, do not difference them; Ottumwa
  800 (2022) vs 'less than 400' (Nov-2024), recorded as an upper bound; Getafe 1,114 is the legal
  entity John Deere Ibérica S.A. from the Spanish registry, not strictly the plant.
