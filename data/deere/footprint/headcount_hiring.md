# Deere & Company — headcount and hiring series

Companion to `headcount_hiring.csv` (161 rows). Built 2026-08-16. Deere has **not** reported FY2026 Q3
(quarter ended ~2 August 2026; earnings call 20 August 2026, 09:00 US Central). Nothing below is a Q3
actual.

---

## 1. What this file is for

Two questions, kept separate throughout:

- **(A) Immediate — what already happened in Q3 FY2026 (4 May – 2 Aug 2026).** Answered by *dated events
  inside that window*: recall/hire announcements, WARN filings, shutdown changes. Those are near-direct
  evidence, not forecasts.
- **(B) Ongoing — a reusable tracker.** Answered by the annual filing backbone plus a reproducible
  scraper for the careers board, so the snapshot below becomes a time series from now on.

---

## 2. The reliable backbone: 10-K employee disclosures, FY2015–FY2025

Every figure below is verbatim from the Item 1 "Employees" paragraph of the corresponding 10-K in
`challenge/offline-data/deere/filings/`. Deere writes "approximately" for all of them.

| FY | as of | Total | US (+Canada) | Full-time production, WW | US production | UAW-covered (active) | % US prod/maint unionised |
|---|---|---|---|---|---|---|---|
| 2015 | 2015-10-31 | 57,200 | 28,500 (US+CA) | — | — | 10,000 | 82 |
| 2016 | 2016-10-31 | 56,800 | 27,900 (US+CA) | — | — | 7,600 | 84 |
| 2017 | 2017-10-29 | 60,500 | 29,000 (US+CA) | — | — | 8,700 | 84 |
| 2018 | 2018-10-28 | 74,000 | 31,000 (US+CA) | — | — | 9,600 | 85 |
| 2019 | 2019-11-03 | 73,500 | 30,000 (US+CA) | — | — | 9,300 | 84 |
| 2020 | 2020-11-01 | 69,600 | 27,500 (US+CA) | — | — | 8,740 | 84 |
| 2021 | 2021-10-31 | 75,600 | 29,000 (US+CA) | — | — | 10,500 | 83 |
| 2022 | 2022-10-30 | 82,200 | 32,000 (US+CA) | — | — | 11,500 | 81 |
| 2023 | 2023-10-29 | 83,000 | 33,800 (US+CA) | — | — | 11,500 | 80 |
| 2024 | 2024-10-27 | 75,800 | 29,600 (US only) | 35,200 | 13,300 | 8,900 | 77 |
| 2025 | 2025-11-02 | 73,100 | 27,000 (US only) | 32,500 | 11,600 | 7,600 | 77 |

**Two breaks you must not smooth over.**

1. **Geographic definition changed in FY2024.** FY2015–FY2023 disclose "US **and Canada**"; FY2024–FY2025
   disclose "**US**" only. The CSV keeps these as two different series (`de_us_canada_employees`,
   `de_us_employees`) and never joins them. The apparent 33,800 → 29,600 drop is partly Canada leaving
   the numerator. `de_non_us_employees` inherits the same break and is flagged row-by-row.
2. **The FY2018 jump (60,500 → 74,000) is the Wirtgen acquisition**, ~8,200 employees at the acquisition
   date (Dec 2017), plus organic growth. Not a production-rate signal.

Also: the UAW figure gains the word "**active**" from FY2016 onward. The FY2015 → FY2016 −24% is
therefore partly definitional and is excluded from the calibration below.

### The single best series in this file

`de_uaw_covered_employees` — active US production and maintenance workers under the UAW master
agreement, disclosed every year since FY2015. It is superior to total headcount for this purpose
because **laid-off workers fall out of it**: it counts people actually on the line. It excludes
salaried, non-union US plants (e.g. Grovetown GA, Kernersville NC) and everything outside the US.

**It tracks shipments.** Regressing YoY change in UAW-covered heads on YoY change in worldwide equipment
operations net sales (PPA+SAT+CF), FY2016→FY2025:

- n = 10, **correlation 0.89**, slope 0.78
- excluding the FY2016 definitional break: n = 9, **correlation 0.90**, slope 0.71

| FY | equip. net sales YoY | UAW-covered YoY | gap (heads − sales) |
|---|---|---|---|
| 2016 | −9.3% | −24.0% | −14.7pp *(definition change)* |
| 2017 | +10.7% | +14.5% | +3.8pp |
| 2018 | +28.8% | +10.3% | −18.5pp |
| 2019 | +4.6% | −3.1% | −7.7pp |
| 2020 | −10.4% | −6.0% | +4.3pp |
| 2021 | +27.1% | +20.1% | −6.9pp |
| 2022 | +20.6% | +9.5% | −11.1pp |
| 2023 | +16.0% | 0.0% | −16.0pp |
| 2024 | −19.4% | −22.6% | −3.2pp |
| 2025 | −13.1% | −14.6% | −1.6pp |

Read the asymmetry carefully, because it is the crux of whether the user's idea works:

- **On the way up, headcount badly understates shipments** (2018, 2022, 2023: sales +16 to +29% on flat
  or single-digit headcount). Deere absorbs upside with overtime, extra shifts and productivity, not
  bodies. Slope < 1.
- **On the way down, headcount slightly overstates the fall in shipments** (2024: −22.6% heads vs −19.4%
  sales; 2025: −14.6% vs −13.1%). That is exactly the underproduction mechanism the brief describes —
  Deere cuts plant activity below retail demand to drain inventory, so the labour cut runs a little
  ahead of the revenue cut.

Practical rule: **the indicator is sharp and near-unbiased in downturns, and heavily damped in
upturns.** Do not scale a hiring number up into a revenue number the way you can scale a layoff number.

### Productivity / capacity-utilisation check

`de_revenue_per_employee` (total net sales and revenues ÷ total employees):

| FY | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $k/employee | 505 | 469 | 492 | 505 | 534 | 511 | 582 | 640 | **738** | 682 | 625 |

Peak FY2023 at $738k, then −7.5% and −8.4% in the two down years. The ratio has fallen 15% from peak
while headcount fell only 12% — i.e. Deere has *not* cut people as fast as revenue has fallen. That is
the fixed-cost drag management describes as "higher overhead costs from production inefficiencies
associated with lower volumes" (FY2025 10-K, cost-of-sales bridge).

Tighter version, available only for FY2024–FY2025 because production headcount was first disclosed in
the FY2024 10-K — `de_equipment_sales_per_production_employee`:

- FY2024: $44,759m / 35,200 = **$1.272m** per production employee
- FY2025: $38,917m / 32,500 = **$1.197m** (−5.8%)

Equipment sales −13.1%, production heads −7.7%. Deere retained roughly half the labour it "should" have
shed on a pure volume basis. Consistent with the recalls that followed in FY2026: management held the
workforce for a recovery it expected.

---

## 3. (A) IMMEDIATE — what the employment record says about Q3 FY2026

The Q3 window is 4 May – 2 August 2026. Everything here is dated.

### Dated events inside or bearing on the window

| Date | Site | Action | People | Segment |
|---|---|---|---|---|
| 2026-01-28 | Davenport Works, IA | recall | 75 | C&F |
| 2026-01-28 | Dubuque Works, IA | recall | 24 | C&F |
| 2026-02-06 | Waterloo Works, IA (Tractor Ops, Drivetrain, Engine Works, Foundry) | recall | 146 | PPA — 8R tractors |
| 2026-02-19 | Dubuque Works, IA | recall | 27 | C&F |
| 2026-04-16 | Dubuque / Davenport / Coffeyville | recall | 21 / 20 / 8 | C&F |
| **2026-06-11** | **Dubuque Works, IA** | **new external hires** | **30** | **C&F — inside Q3** |
| **2026-06-11** | **Davenport Works, IA** | **recall** | **20** | **C&F — inside Q3** |

Company-reported cumulative US recalls + hires since 1 Jan 2026: ~275 (as of 19 Feb) → 324 (16 Apr) →
**400+ (11 Jun)**.

**Layoffs: none found in calendar 2026.** WARN aggregators covering Deere show the most recent Iowa
filing dated 2025-09-17; the 2024–2025 wave (2,167 cut in 2024, 500+ in Iowa in 2025) has stopped. A
full FY2026 Q3 with zero WARN filings, against a company that filed 21 Iowa notices in the preceding
15 months, is a dated, public, negative-signal-absent observation. *Caveat: I read this off aggregator
sites, not the state WARN pages directly — verify before leaning on it.*

**One qualitative item to check, not to trust yet:** search results surfaced an article describing
Waterloo's traditional late-July/early-August shutdown moving to the last two weeks of June. I could not
establish that article's publication year (paywall redirect), and this change is plausibly a much older
one. If the shutdown genuinely sat in June rather than late July in 2026, it shifts *which* weeks of Q3
were dark without changing the total. Flagged as unverified; not in the CSV.

### What this implies for Q3

1. **Direction is unambiguously positive and it is evidence, not forecast.** Deere added US production
   labour in every month of the fiscal year through June, including inside the Q3 window, and cut none.
   A company underproducing into a demand shortfall does not recall 400 people and then hire 30 more
   externally because the recall list is exhausted at that plant.
2. **The mix maps onto guidance.** Six of the seven events are Construction & Forestry (Dubuque,
   Davenport, Coffeyville). FY2026 guidance is CF +~20% and SAT +~15% against PPA −5 to −10%. The
   recalls corroborate the C&F leg of that guide directly.
3. **The Waterloo 146 is the interesting one.** Waterloo is 8R large tractors — PPA, the segment
   guided *down*. Recalling 146 into 8R assembly, machining, logistics and foundry in March, with no
   subsequent reversal, is mildly *better* than a −5 to −10% PPA build plan would imply. Consistent with
   the Q2 call statement that "order books are well into the fourth quarter as we look to close out our
   model year 2026 production" at Waterloo.
4. **Magnitude, quantified honestly.** 400 net additions on a FY2025-end base of 7,600 active
   UAW-covered workers is **+5.3%** (upper bound — attrition is unobservable and would offset). Applying
   the FY2016–FY2025 slope of 0.78 implies **≈ +6.8% worldwide equipment net sales for FY2026**.
   Deere's own guidance (PPA −7.5% midpoint, SAT +15%, CF +20%) implies **+6.5%**. Those agree to within
   0.3pp.

   That agreement is the headline. The employment record does **not** predict a Q3 beat or miss; it says
   the plants were staffed to run the plan management set in May, and nothing in the labour record
   between May and August suggests they deviated from it. **Base case for Q3: shipments in line with the
   FY2026 guide, with C&F the strongest leg.**

5. **What would have shown up here if Q3 were going badly, and did not:** a WARN filing, an extended or
   added shutdown week, a shift elimination, or a reversal of the February–June recalls. None of these
   appeared.

---

## 4. (B) ONGOING — job-postings snapshot, and why it says nothing about Q3

### Read this before using section 4 for anything

**This snapshot was taken on 16 August 2026 — two weeks after Q3 closed. It is a contemporaneous
reading with no history behind it. It cannot inform Q3.** Job postings describe labour Deere intends to
add *next*, and Deere's own careers board does not archive; there is no retrievable back-series. Its
value is for Q4 FY2026 and beyond, and it only becomes a real indicator once
`scripts/data/fetch_deere_jobs.py` has been run repeatedly. Today it is a baseline, nothing more.

### The snapshot

Source: `https://careers.deere.com/api/pcsx/search?domain=johndeere.com` (Eightfold; `robots.txt`
explicitly allows `/api/pcsx`). **201 open external postings worldwide, 83 in the US.**

By function (worldwide):

| Department | n |
|---|---|
| Technology | 36 |
| Factory Engineering | 34 |
| Product Engineering | 29 |
| Other | 24 |
| Supply Chain Management | 17 |
| Marketing and Sales | 13 |
| Operations | 9 |
| **Production/Maintenance** | **8** |
| Data and Analytics | 7 |
| Product & Process Mgmt | 6 |
| Accounting and Finance | 6 |
| Customer Experience | 5 |
| Financial Services | 3 |
| People and Culture | 2 |
| User Experience | 1 |
| Law / Gov't Affairs | 1 |

US plant towns, all 83 US postings:

| Location | Postings | of which Production/Maintenance |
|---|---|---|
| Waterloo, IA | 18 | 0 |
| Moline, IL | 12 | 0 |
| Dubuque, IA | 11 | 0 |
| East Moline, IL | 8 | 0 |
| Johnston, IA | 4 | 0 |
| Grovetown, GA | 4 | 0 |
| Kernersville, NC | 3 | 0 |
| Davenport, IA / Milan, IL / Fargo, ND | 2 each | 0 |
| Ottumwa, Valley City, Thibodaux, Silvis, Coal Valley, Ames, Champaign, Urbandale, Chicago, St Paul, Santa Clara, Austin, Orlando, Harrisburg, E. Dubuque | 1 each | 0 |

### The important caveat, stated plainly

**All 8 Production/Maintenance postings are outside the US** — Mannheim and Bruchsal (Germany:
*Montagewerker*, *Schweißer*, *Elektroniker Instandhaltung*, *Staplerfahrer*, *Fachkräfte für
Lagerlogistik*) plus one French maintenance-engineering internship. Zero in the US.

**Do not read that zero as a US hiring freeze.** Deere fills US hourly roles from the UAW recall list
first, and its US "Production Assembler" requisitions do not appear to route through this external
board at all: the 30 *new external hires* announced for Dubuque on 11 June 2026 are nowhere in this
snapshot. The board is, in practice, a **salaried and engineering** hiring signal in the US and a
**direct production** signal in Germany. Treat those two halves as different instruments.

Further limits: 25 of the 83 US postings are part-time student/intern roles, which say nothing about
production volume. And 82 of the 201 postings were posted inside the Q3 window and are *still open* —
that is a survivorship-biased view, since anything posted and filled during the quarter has already
disappeared from the board.

### What the snapshot *is* good for

- **Baseline for a differenced series.** Re-run the fetcher weekly; the change in
  `Production/Maintenance` count at Mannheim/Bruchsal and the change in `Factory Engineering` count at
  Waterloo/Dubuque/East Moline are the two cells to watch.
- **Factory Engineering as a leading proxy.** 34 postings worldwide, 28 of them US, concentrated in
  Waterloo (several), East Moline (3 weld manufacturing engineers, two of them 3rd shift) and Dubuque.
  Third-shift weld manufacturing engineering roles at Harvester Works are consistent with a plant
  running or planning to run three shifts — a genuine capacity signal, if a soft one.
- **Kernersville, NC** shows 3 postings (Buyer, Planner, Facilities & Maintenance Engineer, all posted
  10–14 Aug 2026) — a new $70m, 150-job small-excavator plant taking over production previously made in
  Japan. Staffing-up activity, and a structural addition to US C&F capacity rather than a cyclical one.

---

## 5. Coverage and honesty statement

**What is well sourced**
- Total, US(+Canada), production and UAW-covered headcount: 11 fiscal years, all from 10-K primary text.
- Equipment operations net sales, 11 fiscal years, from 10-K MD&A — included so every ratio is
  reproducible.
- Seven dated FY2026 recall/hire events with named facilities and headcounts, each from a named
  publication with a verified publication date.
- A complete, timestamped census of Deere's external job board (201/201 postings retrieved).

**What is missing, and left blank rather than guessed**
- **Plant-level headcount is not disclosed anywhere.** There is no row in this CSV giving "how many
  people work at Waterloo Works". Deere does not publish it, and I found no credible primary figure. The
  only plant-level numbers here are *changes* (recalls and hires), which is a different quantity.
- **No non-US site headcount at all**, and no non-US recall/layoff events. Mannheim, Bruchsal, Zweibrücken,
  Horizontina, Indaiatuba, Monterrey — all blank. Given Q2 FY2026 revenue was 46% non-US, this is a
  material hole in the indicator.
- **No FY2012–FY2014 headcount**: the corpus's earliest 10-K is FY2015.
- **No FY2026 headcount**: the next disclosure is the FY2026 10-K in ~Nov/Dec 2026.
- **No historical job-postings series.** Stated repeatedly above because it is the single most likely
  thing to be misread.
- **No monthly or quarterly headcount** of any kind. The recall events are the only intra-year
  observations, and they are announcements, not confirmed payroll counts.
- **Salaried vs hourly split** exists only from FY2024 (production vs total), so the productivity ratio
  in section 2 has two data points.

**Where I may be wrong**
- The WARN "zero for 2026" comes from third-party aggregators, not the state agencies. If a 2026 filing
  exists and the aggregators missed it, the central conclusion of section 3 weakens considerably.
- The "400+ recalled or hired" figure is the company's own rounded number quoted in local press, and
  different outlets describe its scope differently ("across the United States" vs "across Iowa and
  Illinois"). Treated as a floor.
- The 0.78 slope rests on 10 annual observations of a cyclical business. It is a calibration, not a
  model, and it should not be pushed to more than one significant figure.

---

## 6. Reproducing / extending

- `scripts/data/fetch_deere_jobs.py <out.json>` — full census of the careers board. Page size is capped
  at 10 server-side; the script paginates. Run on a schedule to create the missing time series.
- `scripts/data/build_headcount_hiring.py` — regenerates the CSV. All 10-K figures are hard-coded with
  their source file path so they can be re-verified line by line.
- Next highest-value additions, in order: (1) direct state WARN database pulls for IA/IL/WI/KS/ND/GA/TN/LA,
  (2) a weekly cron on the job fetcher, (3) UAW Local 838 / 865 communications for recall and shift
  notices, which lead the press by days.
