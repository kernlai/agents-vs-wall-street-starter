# Deere & Company — master plant inventory

Companion to `plants.csv`. Built 2026-08-16. Deere has **not** reported FY2026 Q3; the Q3
earnings call is 2026-08-20. Nothing in this file is a Q3 actual.

---

## 1. What this dataset is

The spine that every other plant-level signal (WARN notices, callbacks, shutdown weeks,
job postings) hangs on. One row per (plant, metric, date) in tidy long form.

**62 manufacturing / manufacturing-adjacent sites** are enumerated, each mapped to:

- a **segment** (`PPA`, `SAT`, `CF`, or a combination) — from the 10-K where the 10-K says so
- a **geography cell** (`geo_cell=` in `notes`) matching Deere's revenue-by-geography
  disclosure: United States / Canada / Western Europe / Central Europe & CIS /
  Latin America / Asia-Africa-Oceania-Middle East
- an **export orientation** (`orientation=` in `notes`), with its basis stated

That mapping is the point of the dataset: a layoff at Waterloo is evidence about
**PPA / United States**; short-time working at Zweibrücken is evidence about
**PPA+SAT / Western Europe**; collective vacation at Horizontina is evidence about
**PPA / Latin America**. Signals should never be pooled across cells.

### Column semantics

| column | meaning |
|---|---|
| `series_id` | `plant.<slug>.<metric>` or `company.<metric>` |
| `date` | as-of date of the observation, not the publication date of the source |
| `segment` | `;`-separated when a site feeds more than one segment |
| `metric` | `employees`, `employees_production`, `site_area_sqft`, `site_area_acres`, `year_opened`, `products_count` |
| `source_type` | `filing` \| `warn-notice` \| `news` \| `company-site` \| `trade-data` \| `estimate` \| `inference` |
| `notes` | for `products_count` rows: `geo_cell=`, `seg_src=`, `orientation=`, `orientation_basis=`, `products=` (pipe-separated) |

`employees` = total site headcount. `employees_production` = production-and-maintenance
(largely UAW-represented) headcount only. The second is the one that moves with the
build schedule; the first includes engineering and salaried staff that does not.

**Missing data is an absent row.** There are no zeros and no filled-in estimates.

---

## 2. Sources, in priority order

1. **Deere FY2025 Form 10-K, Item 2 "Properties"** (filed 2025-11-26, as of 2025-11-02).
   Authoritative for *segment* attribution but lists only **26 "significant" manufacturing
   properties**. It also gives the structural totals: **23 owned + 4 leased factory
   locations in the US and Canada, and 45 factory locations outside the US and Canada** —
   so ~72 factories exist, of which the 10-K names 26.
   Corpus path: `filings/2025-11-26__de-us-20251126-q4-10k__469216.md`.
2. **"John Deere Worldwide — All locations", December 2025**, Deere & Company Global Brand
   & Communications (`deere.com/assets/pdfs/common/our-company/about/jd-world-locations.pdf`).
   The only public Deere document that enumerates *every* site with its product list. This
   is where the 36 sites absent from the 10-K table come from, and where the `products=`
   strings come from verbatim. It still does not claim to be exhaustive
   ("Maps do not include all locations").
3. **Deere factory microsites** (`deere.com/en-us/our-company/locations/factories/<slug>`) —
   founding years and a handful of site-size facts. Only eight US plants have such a page.
4. **Local news and economic-development agencies** — the only public source of plant
   headcount. Each headcount row carries its own URL and date.

Older 10-Ks (FY2015–FY2020) do **not** contain a plant-level properties table at all; Item 2
just cross-references Item 1 "Manufacturing" and gives aggregate floor space
(e.g. 58.3m sqft owned + 13.9m leased in FY2015; 67.0m + 10.2m in FY2020). No plant-level
history is recoverable from the corpus.

---

## 3. Honest coverage statement

| field | plants covered | of 62 |
|---|---|---|
| name / city / country / products / segment / geo_cell | 62 | 100% |
| segment from a filing (not inferred) | 26 | 42% |
| **at least one headcount observation** | **21** | **34%** |
| headcount dated 2024 or later | 17 | 27% |
| production-only headcount | 6 | 10% |
| year opened | 11 | 18% |
| any site-size figure | 8 | 13% |

**Plant-level headcount is not a disclosed series.** Deere discloses total employees once a
year in the 10-K and nothing below that. Every plant number in this file was reconstructed
from a news story, usually one written *because* of a layoff — which means the sample is
biased toward plants that have been cutting, and toward the moment just before a cut.
Do not treat the headcount column as a panel; treat each cell as a dated point estimate
with its own provenance.

### Plants with NO headcount at all (41 sites)

Davenport IA, Clarion IA, Paton IA, Rock Valley IA, Rock Island IL, Fargo ND,
Springfield MO (reman), Vancouver BC, Altona MB, Catalão, Canoas, Indaiatuba, Porto Alegre,
Rosario, Campana, Las Rosas, Monterrey, Ramos Arizpe, Saltillo, Torreón, Stadtlohn,
Windhagen, Göppingen, Ludwigshafen, Tirschenreuth, Wittlich, Arc-lès-Gray, Largeasse,
Moncoutant, Valencia, Horst, Ravenna, Rainbach, Pune, Dewas, Tianjin, Jiamusi, Langfang,
Beit Hashita, Tokoroa, Fuquay-Varina.

Davenport Works is the most damaging gap: it is a top-five US site by output, it took
299 + 80 + 80 production layoffs across 2024–25, and no public total headcount exists.
The Wirtgen sites are the second gap — Wirtgen Group publishes only a **worldwide** figure
(~8,900), never per plant, so ~5 German road-building plants that together drive a large
share of CF/Western Europe are dark.

### Known conflicts, left unresolved on purpose

- **Horizontina, Brazil**: 1,700 (Feb 2024, combine + planter plant) vs 700 (Feb 2025,
  reported for the combine operation). Both rows are in the CSV with their dates. The
  scopes are probably different, not the same number falling 59% in a year. Do not
  difference them.
- **Waterloo**: 5,500 total / 3,600 production (Mar 2024) vs 4,700 / 2,700 (Oct 2024).
  These *are* comparable and *are* a genuine −15% / −25% in seven months.
- **Ottumwa**: 800 (2022) vs "less than 400" (Nov 2024). The 400 is an upper bound; it is
  recorded as 400 with that caveat in `notes`.
- **Getafe**: 1,114 is the *legal entity* John Deere Ibérica S.A. from the Spanish registry,
  not strictly the Getafe plant. Flagged in `notes`.
- **Coffeyville**: 245 (Jul 2024) vs 236 (2026). Only the sourced 2024 pair is in the CSV.
- **Augusta** (470) and **Valley City** (330+) are 2016 and 2017 vintage. They are the only
  numbers that exist. Treat them as stale.

---

## 4. Company-level anchor series (from the 10-Ks — this one *is* clean)

Total employees at fiscal year end, Item 1 "Employees":

| FY end | worldwide | US | full-time production (WW) |
|---|---|---|---|
| 2015-10-31 | 57,200 | 28,500 | — |
| 2016-10-30 | 56,800 | 27,900 | — |
| 2017-10-29 | 60,500 | 29,000 | — |
| 2018-10-28 | 74,000 | 31,000 | — |
| 2019-11-03 | 73,500 | 30,000 | — |
| 2020-11-01 | 69,600 | 27,500 | — |
| 2021-10-31 | 75,600 | 29,000 | — |
| 2022-10-30 | 82,200 | 32,000 | — |
| 2023-10-29 | 83,000 | 33,800 | — |
| 2024-11-03 | 75,800 | 29,600 | 35,200 |
| 2025-11-02 | 73,100 | 27,000 | 32,500 |

FY2025 additionally: **~11,600 full-time US production employees**; unions represent ~77% of
US production and maintenance staff; **~7,600 active US production workers are under the UAW
agreement expiring 2027-11-01**.

Read the trend: worldwide headcount −11.9% from the FY2023 peak (83,000 → 73,100) and US
headcount −20.1% (33,800 → 27,000) over two years. US shrank roughly twice as fast as the
group. Since PPA is the most US-weighted segment, that asymmetry is itself a segment signal
— and it matches PPA net sales falling from 17,311 in FY2025 with guidance of a further
−5% to −10% in FY2026.

**Caution on the FY2024 break**: the 10-K changed disclosure format in FY2024, adding
"full-time production employees" and dropping the older phrasing. The 2015–2023 and
2024–2025 rows are not perfectly like-for-like on the production sub-series (which is why
the production column starts in FY2024).

---

## 5. The segment × geography matrix, populated

FY2025 segment net sales: PPA 17,311; SAT 10,224; CF 11,382 ($m).
Q2 FY2026 revenue by geography ($m): US 7,198; Canada 1,039; W. Europe 2,141;
C. Europe & CIS 525; Latin America 1,268; Asia/Africa/Oceania/ME 1,198.

| geo_cell | PPA | SAT | CF |
|---|---|---|---|
| **United States** | Waterloo, East Moline, Moline Seeding/Cylinder, Des Moines (Ankeny), Valley City, Clarion, Paton, Thibodaux, Fargo, (+ Mexican component plants: Ramos Arizpe, Saltillo, Torreón, Monterrey) | Augusta, Greeneville, Horicon, Fuquay-Varina, Ottumwa | Dubuque, Davenport, Kernersville, Coffeyville, Waterloo (engines/drivetrain) |
| **Canada** | — | — | Vancouver BC |
| **Western Europe** | Zweibrücken, Bruchsal, Stadtlohn, Largeasse, Moncoutant, Horst, Ravenna, Valencia, Getafe, Saran | Mannheim, Arc-lès-Gray | Windhagen, Göppingen, Ludwigshafen, Tirschenreuth, Wittlich, Joensuu |
| **Central Europe & CIS** | *(none — see Russia below)* | — | — |
| **Latin America** | Horizontina, Montenegro, Catalão, Canoas, Rosario, Campana, Las Rosas | — | Indaiatuba, Porto Alegre |
| **Asia/Africa/Oceania/ME** | Jiamusi, Beit Hashita | Pune, Dewas | Tianjin, Langfang, Tokoroa |

**Cells with no plant of their own are the ones to watch for tariff/FX distortion**, not
production distortion: Central Europe & CIS ($525m in Q2 FY2026) is served entirely by
imports from Western Europe, so a Zweibrücken slowdown reads through to *two* revenue cells.

### The Mexico judgement call

Monterrey, Ramos Arizpe, Saltillo and Torreón are physically in Latin America but their
output is overwhelmingly captive components, cabs and engines feeding US assembly and the
US retail market. They are mapped to `geo_cell=United States` with
`orientation=export` and the reasoning in `notes`. Anyone who prefers a location-based
mapping can re-key on the `country` column instead — both keys are in the file. Ramos Arizpe
specifically absorbed the large-tractor **cab** line moved out of Waterloo, so hiring there
and layoffs at Waterloo are partly the *same* event, not two independent signals. Do not
double count.

### Russia — confirmed exit, not a data gap

Deere suspended shipments to Russia on 2022-02-24, declined to renew Russian dealer
agreements as of 2022-11-01, sold the Russian financial-services business in Q2 FY2023, and
the Orenburg plant was acquired by Koblik Group (2023). **Neither Orenburg nor the
Domodedovo distribution centre appears in Deere's December 2025 worldwide locations list.**
There are therefore no Russia rows in `plants.csv`. Its absence is a fact, not an omission.

---

## 6. How to use this for the FY2026 Q3 read (use case A)

Q3 FY2026 ran roughly 2026-05-04 to 2026-08-02 and is **already over**. To convert a plant
event inside that window into a revenue read:

1. Look the plant up in `plants.csv`, take its `segment` and `geo_cell`.
2. Size the event against the plant's `employees_production` if present, else `employees`,
   else say "unsized" — do not manufacture a denominator.
3. Weight the plant by its share of the segment. **You cannot compute that share from this
   file** — there is no plant-level output or revenue disclosure anywhere. What you can say
   is directional and ordinal: Waterloo and East Moline are the two largest PPA/US sites by
   headcount, Mannheim and Zweibrücken the two largest PPA-SAT/W. Europe sites, Dubuque and
   Davenport the two largest CF/US sites.
4. Remember the **underproduction** wedge. Deere deliberately builds below retail demand in
   downturns (117 mentions in the corpus; CEO John May in the Q3 FY2025 release: Deere had
   "proactively managed inventory" and "matched production to retail demand"). Plant hours
   therefore track **shipments** — the revenue line — more tightly than they track retail
   demand. That is what makes this indicator work for the print, and what makes it *overstate*
   the underlying retail decline.

The most striking thing visible in the enrichment research, which the callback/WARN agent
should own but which belongs on the record here: through H1 CY2026 Deere was **recalling**
production workers to Waterloo (146 across four Waterloo facilities from early March 2026;
another ~41 in April), Dubuque (72 across early-2026 callbacks, plus 30 net new hires) and
Davenport (75 in January, 20 more in June 2026) — the reverse of the 2024–25 direction. That
is a US/PPA and US/CF signal pointing up inside the Q3 window, and it is directly at odds
with FY2026 guidance of PPA sales −5% to −10%. It needs its own dated series before anyone
leans on it; treat the numbers above as leads to verify, not as data.

## 7. How to maintain this for future quarters (use case B)

- Re-pull the worldwide locations PDF each December; Deere re-dates it annually and it is
  the cheapest way to catch openings, closures and product moves.
- Re-read 10-K Item 2 each November for segment reassignments and the owned/leased factory
  counts.
- The headcount rows will always be maintained by hand from news. The realistic cadence is:
  update a plant's headcount only when a WARN notice or a local story restates the base.
  Never carry a headcount forward more than four quarters without re-sourcing it — mark it
  stale instead.
- Rebuild with `python3 scripts/data/build_deere_plants.py`. Every number in the CSV is a
  literal in that script with its source next to it, so provenance survives edits.
