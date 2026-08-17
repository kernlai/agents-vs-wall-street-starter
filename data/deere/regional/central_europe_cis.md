# Regional briefing — Central Europe and CIS

**Desk:** desk-central-europe-cis · **Date:** 16 August 2026
**Quarter under analysis:** Deere FY2026 Q3, ~4 May – 2 August 2026
**Status:** Deere has **not** reported FY2026 Q3. The earnings call is 09:00 US Central, Thursday 20 August 2026. Nothing in this note is an actual. Every FY2026 Q3 figure here is a forecast and is labelled as such.

**Data file:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/regional/central_europe_cis.csv` (779 rows)
**Build script:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/build_central_europe_cis.py`
**Scrape helper:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/extract_ce_cis_matrix.py`

**Basis warning.** All segment × geography figures are from the ASC 606 revenue-recognition footnote ("net sales and revenues by primary geographic market"). This basis does **not** tie to the 8-K segment net-sales table (Q2 FY2026 PPA: 4,607 footnote vs 4,503 8-K, a 104m gap). Do not mix the two when aggregating.

---

## 1. The seven-year quarterly history

Central Europe and CIS, USDm, revenue-recognition basis. Q1–Q3 are printed three-month columns in the 10-Qs. **Q4 is derived** as (10-K fiscal year) less (10-Q nine months). Every quarter cross-foots to its segment total and every fiscal year's four quarters cross-foot to the 10-K annual — the build script asserts this and passes.

| Fiscal quarter | PPA | SAT | CF | FS | **Total** | W. Europe | CE/WE |
|---|---:|---:|---:|---:|---:|---:|---:|
| FY2019 Q1 | 148¹ | — | 171 | 9 | **328** | 1,205 | 27.2% |
| FY2019 Q2 | 393¹ | — | 155 | 9 | **557** | 1,760 | 31.6% |
| FY2019 Q3 | 324¹ | — | 229 | 10 | **563** | 1,634 | 34.5% |
| FY2019 Q4 *(der.)* | 558¹ | — | 194 | 9 | **761** | 940 | — |
| FY2020 Q1 | 131 | 89 | 159 | 10 | **389** | 1,139 | 34.2% |
| FY2020 Q2 | 258 | 80 | 140 | 8 | **486** | 1,491 | 32.6% |
| FY2020 Q3 | 219 | 100 | 178 | 9 | **506** | 1,501 | 33.7% |
| FY2020 Q4 *(der.)* | 290 | 224 | 169 | 8 | **691** | 1,202 | 57.5%² |
| FY2021 Q1 | 161 | 84 | 178 | 9 | **432** | 1,398 | 30.9% |
| FY2021 Q2 | 531 | 160 | 209 | 9 | **909** | 1,867 | 48.7% |
| FY2021 Q3 | 398 | 117 | 241 | 10 | **766** | 1,727 | 44.4% |
| FY2021 Q4 *(der.)* | 232 | 114 | 200 | 11 | **557** | 1,437 | 38.8% |
| FY2022 Q1 | 202 | 126 | 195 | 11 | **534** | 1,383 | 38.6% |
| **FY2022 Q2** ← break | 404 | 151 | **146** | 11 | **712** | 1,683 | 42.3% |
| FY2022 Q3 | 348 | 109 | **111** | 14 | **582** | 1,696 | 34.3% |
| FY2022 Q4 *(der.)* | 253 | 102 | 93 | 13 | **461** | 1,582 | 29.1% |
| FY2023 Q1 | 202 | 123 | 75 | 12 | **412** | 1,459 | 28.2% |
| FY2023 Q2 | 393 | 212 | 90 | 8 | **703** | 2,169 | 32.4% |
| FY2023 Q3 | 302 | 85 | 98 | 6 | **491** | 2,091 | 23.5% |
| FY2023 Q4 *(der.)* | 321 | 110 | 90 | 10 | **531** | 1,602 | 33.1% |
| FY2024 Q1 | 179 | 73 | 94 | 8 | **354** | 1,421 | 24.9% |
| FY2024 Q2 | 275 | 80 | 91 | 8 | **454** | 1,857 | 24.4% |
| FY2024 Q3 | 201 | 70 | 106 | 12 | **389** | 1,560 | 24.9% |
| FY2024 Q4 *(der.)* | 132 | 61 | 90 | 8 | **291** | 1,351 | 21.5% |
| **FY2025 Q1** ← trough | 67 | 39 | 71 | 4 | **181** | 1,016 | 17.8% |
| FY2025 Q2 | 239 | 99 | 87 | 3 | **428** | 1,820 | 23.5% |
| FY2025 Q3 | **301** | **130** | **103** | **2** | **536** | 2,029 | 26.4% |
| FY2025 Q4 *(der.)* | 225 | 91 | 112 | 2 | **430** | 1,685 | 25.5% |
| FY2026 Q1 | 172 | 60 | 76 | 2 | **310** | 1,430 | 21.7% |
| FY2026 Q2 | 297 | 121 | 105 | 2 | **525** | 2,141 | 24.5% |
| **FY2026 Q3** | *308* | *120* | *110* | *2* | ***540*** | — | — |

¹ FY2019 predates the PPA/SAT split; the 10-Qs report a single Agriculture & Turf column. The FY2021 10-K restates FY2019 at the annual level only (PPA 859 / SAT 564), so no quarterly split exists. Missing, not zero.
² FY2020 Q4 is a derived-residual outlier on both numerator and denominator (SAT 224 vs ~90 in the other three quarters). Arithmetically correct against the disclosures but I would exclude it from any regression.
*Italics = forecast.*

**Fiscal-year totals (10-K, cross-foot targets):** FY2019 2,209 · FY2020 2,072 · FY2021 2,664 · FY2022 2,289 · FY2023 2,137 · FY2024 1,488 · FY2025 1,575.

This region is ~3.9% of company revenue (Q2 FY2026: 525 of 13,369) and the smallest of the six. It is PPA-dominated (57% of the region in Q2 FY2026 vs 34% company-wide) and it is the region where Deere's segment mix is most concentrated in large ag.

---

## 2. The structural break: Russia, and what it actually did

### 2.1 The timeline, from the filings

| Date | Event | Source |
|---|---|---|
| Feb–Mar 2022 | Invasion; Deere suspends shipments of machines and service parts to Russia | Q2 FY2022 10-Q, Note 20 |
| Q2 FY2022 (qtr end 1 May 2022) | Net Russia/Ukraine exposure ~$454m. **$120m pretax / $106m after-tax** charge: long-lived asset impairments (PPA 46, SAT 1, CF 47), credit-loss allowance (FS 26), contingent liabilities. "Net sales from the Company's Russian operations represented 2 percent of consolidated annual net sales from 2017 to 2021." Ukraine operations not material. | Q2 FY2022 10-Q |
| Q3 FY2022 | Voluntary separation programme for Russia employees | FY2023 10-K |
| During FY2022 | Russian manufacturing facility shut down | FY2023 10-K, Item 2 |
| **1 Nov 2022** | Dealer agreements in Russia **not renewed** | FY2023 10-K |
| **7 Mar 2023** (Q2 FY2023) | Financial services business in Russia **sold** to Insight Investment Group; net proceeds $36m, assets $31m, cumulative translation loss $10m | Q2 FY2023 10-Q, Note 20 |
| Q2 FY2023 | Eurasian parts distribution centre in Russia closed, premises returned | FY2023 10-K |
| **Oct 2023** (Q4 FY2023) | Wirtgen **roadbuilding business in Russia sold**. "Consequently, we no longer sell equipment in Russia." | FY2023 10-K |

The wind-down is complete as of the end of FY2023. Russia has contributed nothing since.

### 2.2 Where it shows in the data — and where it does not

**It shows almost entirely in Construction & Forestry, and it is a clean step, not a trend.**

| | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|---:|---:|
| CF, fiscal year | 828 | 545 | 353 | 381 | 373 |
| CF, avg per quarter | **207** | 136 | **88** | 95 | 93 |

CF quarters run 178/209/241/200 through FY2021, then 195/**146**/**111**/93 through FY2022, then settle in a band of **71–112 for twelve consecutive quarters** (FY2023 Q1 – FY2026 Q2). The break begins in FY2022 Q2 — the exact quarter of the shipment suspension — and completes by FY2023 Q1.

**Quantum: the CF step is ~115m per quarter, ~460m per year.** That is the Wirtgen roadbuilding franchise in Russia (Wirtgen operated a company-owned Russian sales and service subsidiary; the FY2023 10-K's subsidiary list drops Russia, Georgia, Belgium, Bulgaria and Serbia relative to FY2022). It is consistent in size with "Russia = 2% of consolidated net sales", of which roadbuilding was disproportionate.

**It does NOT show cleanly in PPA or SAT — and this is the trap.**

PPA ran 1,322 → 1,207 → **1,218** across FY2021→FY2023, essentially flat despite losing an entire country. SAT ran 475 → 488 → **530**, up. The Russia loss in ag was masked by two offsets that peaked in exactly the same window: the 2022–23 Black Sea grain price spike lifting Polish, Romanian, Hungarian and Kazakh farm incomes, and Deere's own price realisation (+12% outside the US and Canada in FY2022, per the FY2023 10-K MD&A).

**Then a completely separate shock hit PPA and SAT one to two years later.** PPA 1,218 → **787** (-35%) in FY2024; SAT 530 → **284** (-46%). Management named the cause on the record and it is not Russia:

> "Eastern Europe continues to be impacted by grain inflows from Ukraine, driving down commodity prices" — Q4 FY2023 earnings call, 22 Nov 2023
> "Demand is expected to be softest in Central and Eastern Europe, as local commodity markets remain disrupted by the ongoing conflict in Ukraine" — Q1 FY2024 call, 15 Feb 2024
> "In Central and Eastern Europe, reduced pressure from Ukrainian grain imports is supporting better than expected farm net incomes" — Q1 FY2025 call, 13 Feb 2025 ← *the inflection*

### 2.3 The control: difference-in-differences against Western Europe

Western Europe is the right control — same continent, same CAP, same ag cycle, same euro, **no Russia exposure**. The ratio of CE&CIS to Western Europe revenue:

| Era | CE/WE |
|---|---:|
| Pre-war, FY2020–21 | **40.3%** |
| War onset, FY2022 | 36.1% |
| Exit complete, FY2023 | 29.2% |
| Trough, FY2024 | **24.0%** |
| FY2025 | **24.0%** |
| FY2026 H1 | **23.4%** |

Two distinct legs, then a floor:

1. **FY2021 → FY2023: −11.1pts.** The Russia exit. Concentrated in CF.
2. **FY2023 → FY2024: −5.2pts.** The Ukrainian-grain-inflow shock to EU-CEE farm incomes. Concentrated in PPA and SAT.
3. **FY2024 → present: flat at 24%.** The region now moves *with* Western Europe. Three fiscal years of stability.

**Total permanent de-rating: ~16pts of relative scale, i.e. the region is ~40% smaller relative to Western Europe than it was pre-war.** Against FY2021's Western Europe base that is roughly **$1.0–1.1B of annualised revenue** never recovered.

### 2.4 Modelling instruction for the team

> **Do not fit a trend, level model, or YoY-momentum model across FY2021–FY2026 for this region.** A linear trend over that window is dominated by two discrete regime shifts and will extrapolate a decline that structurally ended in FY2024. Any regression must either start at FY2024 Q1, or carry a Russia-exit dummy (FY2022 Q2 through FY2023 Q1, phased) plus a separate CEE-farm-income dummy (FY2024).
>
> **The robust specification is a ratio to Western Europe.** CE/WE has been 24.0%, 24.0%, 23.4% for three consecutive periods. Quarterly it is noisier (21.7%–26.4% over the last four quarters, trailing-4Q 24.7%), but at segment level it is tighter than anything else available: PPA 43.3%, SAT 15.3%, CF 18.4% on a trailing-four-quarter basis.
>
> A second trap: **the FY2020–FY2024 seasonal shape is itself contaminated.** The Q3/Q2 ratio for the region was 0.70–0.86 across FY2021–FY2024 — but that period *is* the two shocks. FY2025 printed 1.25. Seasonal-ratio methods give answers 15–25% below every other method here (see §5) and I discount them heavily.

---

## 3. Current conditions in the region

### 3.1 What is actually in this region now

Post-Russia, the revenue is: **Poland** (the anchor — Deere ag sales/admin office, Wirtgen subsidiary), **Romania**, **Hungary**, **Czechia**, **Slovakia**, the **Baltics**, **Bulgaria**, **Ukraine**, and the non-sanctioned **CIS** — principally **Kazakhstan** (a genuinely large grain and large-ag market) plus Uzbekistan, Georgia, Armenia, Azerbaijan, Moldova. Belarus is embargoed. Ukraine is a real market but a modest one for Deere specifically: German manufacturers hold roughly half the Ukrainian combine market and US manufacturers under 10%.

### 3.2 Grain: the single most important variable, and it turned positive

Global wheat (IMF/World Bank monthly, FRED `PWHEAMTUSDM`, USD/mt):

| | Feb 26 | Mar 26 | Apr 26 | May 26 | Jun 26 |
|---|---:|---:|---:|---:|---:|
| 2026 | 174.8 | 193.9 | 202.6 | **220.9** | 199.6 |
| 2025 comparator (May/Jun/Jul) | | | | 196.8 / 173.2 / 165.3 | |

**May–Jun 2026 average $210/mt vs the full Q3 FY2025 window (May–Jul 2025) average of $178/mt — up ~18% year over year.** Wheat has risen in five of the last seven months and May 2026 was the highest monthly print since early 2023. Maize is roughly flat YoY ($206 vs $198). Wheat is what matters for Poland, Romania, Hungary, Ukraine and Kazakhstan.

MATIF milling wheat was €201/t (Sep contract) in late June 2026 and firmed into the **low €220s/t by mid-July 2026**, with a risk premium building on Black Sea disruption and a **summer heatwave cutting the EU 2026 grain harvest**. Romania has a record wheat crop (13.86 Mt, 5.9 t/ha) but is price-taking; Polish wheat area is down 2% to 2.4m ha with output possibly ~1 Mt lower YoY, cushioned by large carryover; Hungary shifted acreage toward barley.

Net: **rising prices on softer EU volumes — a farm-income tailwind for EU-CEE in the May–July window**, and the opposite of the 2023–24 conditions that broke this region.

### 3.3 The Black Sea, May–July 2026 — the defining event of the quarter

Ukraine's 2026 harvest is **large**: the Ukrainian Grain Association raised its grain-and-oilseed forecast to **84.6 Mt**. By 28 July farmers had cut 2.6m ha (22% of area) for 10.65 Mt; wheat specifically 1.532m ha (30%) for 6.61 Mt at **4.32 t/ha**, a strong yield. Early-season Black Sea export volumes ran well above July 2025.

Then the corridor was attacked, hard, inside this quarter:

- **20 June – 20 July 2026:** Russia attacked **28 civilian vessels** in Greater Odesa ports; 21 killed, 34 injured.
- **July 2026 in total:** **124 attacks** on Ukrainian port infrastructure, ships in port and vessels in the sea corridor.
- **Freight cost roughly doubled in one week**, ~$24 → ~$47/t; total added logistics cost cited at ~$50/t.
- **Since 22 July 2026** — peak wheat harvest — commercial vessel arrivals at the deepwater ports effectively stopped; 30–40% of scheduled July–August calls cancelled. Roughly **one-third of Ukraine's grain export capacity** lost.
- Ukraine's Agriculture Ministry cut its 2026/27 agricultural export forecast by **54%**, to 29.6 Mt from 64.4 Mt.
- Danube and rail are the fallback and cannot match the corridor's throughput or cost.

The May 2026 truce (9–11 May, around Victory Day) was a three-day humanitarian pause with a prisoner exchange; it did not hold and covered no port or shipping provisions. Talks in the UAE and Switzerland in Jan–Feb 2026 produced no breakthrough; further talks were set for Istanbul on 23 July 2026. **There is no ceasefire and no reconstruction dividend in this quarter.** Agriculture-sector reconstruction need is put at $55.5B through 2035, of which under 2% ($873m) has been funded — donor-funded equipment demand is real but not yet a revenue line for Deere at scale.

**The two-sided read, which matters for the forecast:**

- **Negative for Ukraine.** A big crop that cannot be shipped, plus +$50/t logistics, crushes Ukrainian farmgate realisations and cash flow. The Ukrainian Agribusiness Club expects near-term earnings declines for producers. But this bites from late July onward, i.e. the last ten days of the quarter, and it hits *orders*, not shipments already in the book.
- **Positive for EU-CEE.** Ukrainian grain that cannot reach the world market also cannot flood Poland, Romania and Hungary. That is precisely the mechanism Deere management credited in February 2025 for better-than-expected CEE farm incomes, and it is now amplified. Combined with the EU heatwave, it is what is holding MATIF in the low €220s.

Since Poland, Romania, Hungary and Kazakhstan almost certainly outweigh Ukraine in Deere's revenue mix here, the net effect on Q3 FY2026 *shipments* is mildly positive to neutral. The damage is a **FY2027 order-book risk**, not a Q3 revenue risk.

### 3.4 Sanctions and export control

Agricultural machinery is **not** subject to an EU export ban per se. But the perimeter tightened inside the quarter:

- **EU 20th package, adopted 23 April 2026** (just before the quarter): 120 new listings; new prohibitions on commercial goods worth >€365m including agricultural and industrial machinery categories, and specifically **industrial tractors above 130 kW**. First-ever use of the **anti-circumvention tool** (introduced in the 11th package, June 2023) restricting exports to named *third* countries.
- **EU 21st package, ~3 August 2026** — at the quarter boundary.

The anti-circumvention tool is the item to watch for this desk, because the "CIS" half of the region is exactly where circumvention scrutiny lands: Kazakhstan, Georgia, Armenia, Uzbekistan. Tighter end-use diligence raises friction and lead times on CIS-destined large ag. Deere itself has no Russia exposure left to lose, so the exposure is second-order — compliance drag on legitimate Central Asian shipments, not a revenue cliff.

### 3.5 Farm support and EU funding

- **CAP 2023–27** runs unchanged through this quarter; direct payments are the income floor for Polish, Romanian and Hungarian arable farms.
- **The 2028–34 MFF proposal cuts CAP's share** (CAP + cohesion drop from ~70% to ~45% of the EU budget; ~20% real cut to agriculture) and has triggered farmer protests across the bloc. Poland is the loudest opponent and also the largest beneficiary of the proposed €1.8–2.0tn budget. This is **sentiment risk now, cash risk from 2028** — it can suppress large-ticket ordering confidence ahead of the cash impact.
- **Poland's RRF/KPO deadline is August 2026 — inside this quarter.** Poland must complete the grant portion of its €29bn national recovery plan by August 2026 (final payment requests to end-September); the Commission approved a €7.9bn payment request on 10 August 2026. Poland receives a record ~€43bn of EU funding in 2026 in total. A material share is transport infrastructure, with added emphasis on dual-use/military-mobility corridors. **This is a genuine, deadline-driven pull-forward of road-building procurement in Deere's largest market in this region, landing exactly in Q3 FY2026.** It is the strongest single argument for CF upside here.

### 3.6 Currency

| Pair (local per USD; lower = stronger local) | May–Jul 2025 | May–Jun 2026 | Change |
|---|---:|---:|---|
| PLN/USD | 3.704 | 3.665 | PLN +1.1% |
| HUF/USD | 349.6 | 307.3 | HUF **+13.8%** |
| CZK/USD | 21.57 | 20.92 | CZK +3.1% |
| USD/EUR (fiscal-quarter mean of dailies) | 1.1488 (Q3 FY25) | **1.1532 (Q3 FY26)** | **+0.4%** |

RON is EUR-managed and tracks EUR/USD, so effectively flat YoY. UAH is down ~5.5% YoY vs USD (~43.8–44/USD) and is not on FRED — treated as a blank, not a zero.

**The critical FX point: the euro tailwind evaporates in Q3.** Q2 FY2026 enjoyed USD/EUR 1.1688 against a Q2 FY2025 comparator of 1.0782 — an **8.4-point translation tailwind**, which is a large part of why Q2 printed +22.7% YoY. Q3 FY2025 already had a weak dollar (1.1488), so the Q3 FY2026 tailwind is **+0.4 points — essentially nil**. Any forecast that carries H1's YoY momentum into Q3 without stripping FX will be too high by roughly 8 points. Deere guided ~3 points of favourable currency for full-year PPA; almost all of that was earned in H1.

### 3.7 What Deere management has said that bears on this region

From the Q2 FY2026 call and 10-Q (21 and 28 May 2026):

- Europe ag industry **flat to up 5%**; elevated rates still weighing, customer profitability and replacement activity "relatively stable", arable "a bit muted", dairy margins supportive.
- Deere-internal European ag retail (April 2026): **tractors up double digits, combines up double digits** — Deere is outrunning a flat-to-+5% industry.
- **"Inventory levels in Europe and South America are in good shape following significant reductions in FY2024 and FY2025. In Europe, 2026 production is largely aligned with retail demand… Order visibility in both regions now extends through the third quarter and into the fourth."**
- Global roadbuilding **up ~10%**; global forestry **down ~5%**.
- PPA sales guide down 5–10%; SAT up ~15%; CF up ~20%.

Two things follow. First, **Q3 FY2026 shipments were substantially locked before the late-July Odesa escalation** — the order book covered Q3 and into Q4. Second, **"production aligned with retail demand" means no restocking kicker**; the region grows only as fast as retail does.

---

## 4. Correlations — reported with sample sizes, and mostly discarded

With ~30 quarters total and only **10 clean post-structural-break quarters** (FY2024 Q1 – FY2026 Q2), formal correlation work on this region is not worth much and I will not dress it up.

- CE&CIS total vs Western Europe total, FY2024 Q1 – FY2026 Q2: **n = 10.** The two co-move closely (CE/WE in a 21.5–26.4% band), which is the basis for the ratio method, but with n=10 I quote the ratio and its dispersion, not a correlation coefficient.
- CE&CIS PPA vs lagged global wheat price: **n = 30 across the full history, but the series spans two regime shifts**, so any coefficient is picking up the Russia exit and the grain-inflow shock rather than a price elasticity. Post-break, n = 10. **I regard any such correlation as spurious and am not reporting a number.**
- CE&CIS FS vs anything: the series is 2–4 USDm per quarter after the March 2023 disposal. Rounding noise. No inference possible.

The honest statement is that this region has ~10 usable observations under its current structure, and the forecast below is triangulation across three explicit methods, not a fitted model.

---

## 5. Q3 FY2026 forecast

**Comparative base — Q3 FY2025, extracted from the 10-Q filed 14 Aug 2025** (`filings/2025-08-14__de-us-20250814-q3-10q__155834.md`), three months ended 27 July 2025:

**PPA 301 · SAT 130 · CF 103 · FS 2 · Total 536.**

Note this base is itself a hard comp: Q3 FY2025 was +37.8% YoY over Q3 FY2024's 389, the quarter in which the region inflected out of its trough.

### Three methods

| Method | PPA | SAT | CF | Total | Comment |
|---|---:|---:|---:|---:|---|
| **A. Ratio to Western Europe** (trailing-4Q segment ratios 43.3/15.3/18.4%, applied to WE Q3 at +5%) | 308 | 121 | 107 | 537 | Most robust; needs a WE Q3 assumption |
| **B. Seasonal Q3/Q2** (median FY2020–24, ex-FY2025) | 228 | 88 | 121 | ~439 | **Discounted** — the seasonal shape was set during the two shocks |
| **C. H2 shape** (Q3's FY2025 share of H2, H2 flat to +5%) | 301–316 | 130–136 | 103–108 | 536–562 | Assumes FY2026 H2 repeats FY2025's split |

Method B is the bearish outlier by 15–25%. Its estimation window *is* the structural break — exactly the error this brief warns against — so I weight A and C.

### Adjustments applied on top

- **PPA:** favour the middle of A and C. Wheat +18% YoY, EU-CEE farm income improving, Deere European retail up double digits, no restock kicker, **FX tailwind gone**, comp already +50%. → **308, +2.3%.**
- **SAT:** the hardest comp in the region. Q3 FY2025 SAT/WE-SAT hit 17.2%, the highest ratio in the sample, against a trailing-4Q 15.3% and 14.6% in Q2 FY2026. Mean reversion in the ratio dominates the +15% segment guide. → **120, −7.7%.**
- **CF:** the most stable series here (71–112 for twelve quarters) and the one with a specific, dateable catalyst — Poland's August 2026 RRF/KPO completion deadline pulling road procurement into this quarter, on top of a +10% global roadbuilding guide. Q3 has exceeded Q2 in each of the last three years. Nudged above method A. → **110, +6.8%.**
- **FS:** residual after the March 2023 Russia disposal; 4/3/2/2/2/2 over the last six quarters. → **2, flat.**

### Result

| Segment | Q3 FY25 base | **Q3 FY26 central** | **YoY** | Range | Confidence |
|---|---:|---:|---:|---:|---|
| PPA | 301 | **308** | **+2.3%** | 265–345 | low |
| SAT | 130 | **120** | **−7.7%** | 100–140 | low |
| CF | 103 | **110** | **+6.8%** | 96–124 | medium |
| FS | 2 | **2** | **0.0%** | 1–3 | medium |
| **Total** | **536** | **540** | **+0.7%** | **462–612** | **low** |

Revenue-recognition basis. This is a forecast; Deere reports on 20 August 2026.

The shape of the call: **the region's YoY growth decelerates sharply from +71% (Q1) and +23% (Q2) to roughly flat, almost entirely on comp and FX, not on deterioration.** In level terms 540 would be the second-highest quarter since FY2023 Q2. If the team's aggregate shows this region still growing 15–20% in Q3, the FX tailwind has not been stripped.

---

## 6. Risks

1. **Ukraine port collapse bleeds into Q3 shipments.** Base case is that it hits FY2027 orders, because the order book covered Q3. If Ukrainian dealers cancelled or deferred inside the quarter, PPA lands nearer 265.
2. **SAT comp risk is two-sided.** Q3 FY2025's 130 may reflect a shipment-timing catch-up rather than a new run-rate. If it was structural and the +15% segment guide holds regionally, SAT prints 140+; if it was catch-up, 100.
3. **FX reversal.** The whole forecast assumes USD/EUR ~1.153, which is now a *complete* observed quarter (4 May – 2 Aug 2026, n=62 daily) — so this risk is small for Q3 and large for Q4.
4. **Anti-circumvention friction on CIS shipments.** The EU's 20th (23 Apr) and 21st (~3 Aug) packages tighten third-country diligence over Kazakhstan and the Caucasus. Slower clearance defers, rather than destroys, CIS revenue.
5. **Poland RRF cliff.** The August 2026 deadline is a pull-forward. Whatever CF gains in Q3 FY2026 it gives back in FY2027 unless the successor cohesion programmes ramp cleanly.
6. **CAP 2028–34 sentiment.** A proposed ~20% real cut plus centralisation is already driving protests; it can chill large-ticket ordering confidence in Poland and Romania well before the money changes.

## 7. Caveats

1. **Basis.** Everything here is ASC 606 revenue-recognition, not 8-K segment net sales. The two differ by ~100m at PPA level company-wide. Do not mix.
2. **Q4s are derived**, not printed — (10-K fiscal year) less (10-Q nine months). They cross-foot, but any 10-K restatement propagates into the Q4 residual. FY2020 Q4 in particular (SAT 224 vs ~90 elsewhere) looks like a restatement-allocation artifact and should be excluded from regressions.
3. **FY2019 has no PPA/SAT split at quarterly level.** The 10-Qs of that year report combined Agriculture & Turf; the restatement is annual only. Those cells are blank in the CSV, not zero.
4. **Ten usable post-break observations.** Any model of this region is fitted on n≈10. Treat all point estimates accordingly; the ±14% range on the total is not decoration.
5. **No country-level split exists.** Deere discloses one line for the whole of Central Europe and CIS. The Poland-vs-Ukraine-vs-Kazakhstan weighting in §3 is inference from the 10-K subsidiary and sales-office lists plus market structure, not disclosure. If the true Ukraine weight is much higher than I assume, risk 1 gets much worse.
6. **The wheat, MATIF, harvest and port figures in §3.2–3.3 are third-party press and trade sources**, not audited statistics, and several were published within days of the freeze. FRED series are official and cited with retrieval date.

---

## Sources

**Corpus** (`/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`):
`filings/2019-02-15…q1-10q__469204.md` · `2019-05-17…q2-10q__469675.md` · `2019-08-16…q3-10q__469206.md` · `2019-11-27…q4-10k__469283.md` · `2021-02-19…q1-10q__105814.md` · `2021-05-21…q2-10q__105821.md` · `2021-08-20…q3-10q__105837.md` · `2021-11-24…q4-10k__131650.md` · `2021-12-16…fy-10k__645298.md` · `2022-02-18…q1-10q__105834.md` · `2022-05-20…q2-10q__105838.md` · `2022-08-19…q3-10q__105818.md` · `2022-11-23…q4-10k__105816.md` · `2023-02-17…q1-10q__105813.md` · `2023-05-19…q2-10q__105852.md` · `2023-08-18…q3-10q__105835.md` · `2023-12-15…fy-10k__645297.md` · `2024-02-15…q1-10q__105826.md` · `2024-05-16…q2-10q__105820.md` · `2024-08-15…q3-10q__105828.md` · `2024-11-21…q4-10k__105810.md` · `2025-02-13…q1-10q__105832.md` · `2025-05-15…q2-10q__105831.md` · `2025-08-14…q3-10q__155834.md` · `2025-12-18…fy-10k__393777.md` · `2026-02-19…q1-10q__648937.md` · `2026-02-26…q1-10q__636995.md` · `2026-05-21…q2-10q__1055929.md` · `2026-05-28…q2-10q__1055932.md`
`call-transcripts/2023-11-22…call-pres__46470.md` · `2024-02-15…call-pres__46480.md` · `2024-02-15…call-qna__46498.md` · `2025-02-13…call-q1-pres__46459.md` · `2026-05-21…call-pres__1042774.md` · `2026-05-21…call-qna__1042775.md`

*(INDEX.md labels `call-transcripts/2026-05-21__…call-qna__1042775.md` as "Q3 2026". It is Q2 FY2026 material — the label is wrong and I have treated it as Q2.)*

**FRED** (all retrieved 2026-08-16):
[DEXUSEU](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU) · [PWHEAMTUSDM](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PWHEAMTUSDM) · [PMAIZMTUSDM](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PMAIZMTUSDM) · [CCUSMA02PLM618N](https://fred.stlouisfed.org/graph/fredgraph.csv?id=CCUSMA02PLM618N) · [CCUSMA02HUM618N](https://fred.stlouisfed.org/graph/fredgraph.csv?id=CCUSMA02HUM618N) · [CCUSMA02CZM618N](https://fred.stlouisfed.org/graph/fredgraph.csv?id=CCUSMA02CZM618N). No RON or UAH series is published on FRED; omitted rather than estimated.

**Web** (retrieved 2026-08-16):
- [Ukraine's 2026 grain harvest exceeds 10.6 mln tons — UkrAgroConsult](https://ukragroconsult.com/en/news/ukraines-2026-grain-harvest-exceeds-10-6-mln-tons/) (harvest progress to 28 Jul 2026)
- [Russia's escalating port attacks choke Ukraine's grain exports — Kyiv Independent, 24 Jul 2026](https://kyivindependent.com/russias-escalating-port-attacks-choke-ukraines-grain-exports-as-industry-nears-crisis/)
- [Russia's Odesa strikes halve Ukraine's grain export forecast — Euromaidan Press, 11 Aug 2026](https://euromaidanpress.com/2026/08/11/russia-port-strikes-ukraine-farm-export-forecast/)
- [Odesa Pounded, Straits Squeezed: Black Sea Grain Trade Nears a Standstill — Ag Bull Trading](https://www.agbull.com/odesa-pounded-straits-squeezed-black-sea-grain-trade-nears-a-standstill/)
- [Wheat market July 2026: Prices steady as Black Sea risks rise — Commodity Board](https://commodity-board.com/wheat-prices-steady-but-risk-premium-builds-on-black-sea-disruption)
- [Romania grain market 2026: record wheat output and low prices — Logos Press](https://logos-pres.md/en/news/outlook-for-the-grain-market-in-romania-record-production-low-prices/)
- [A summer heatwave is cutting Europe's 2026 grain harvest — Wikifarmer](https://wikifarmer.com/library/en/article/heatwave-cuts-europe-2026-grain-harvest)
- [May 2026 Russo-Ukrainian truce — Wikipedia](https://en.wikipedia.org/wiki/May_2026_Russo-Ukrainian_truce)
- [Ceasefire Talks: What's at Stake for Ukraine's Agriculture Sector — CSIS](https://www.csis.org/analysis/ceasefire-talks-whats-stake-ukraines-agriculture-sector-and-global-food-security)
- [EU's 20th Russia Sanctions Package: Key Changes — Greenberg Traurig, May 2026](https://www.gtlaw.com/en/insights/2026/5/eus-20th-russia-sanctions-package-key-changes-and-compliance-implications)
- [EU adopts its 20th package of sanctions against Russia — Lexology](https://www.lexology.com/library/detail.aspx?g=c709fe61-5bc3-4265-98b7-c1cee4d70ad4)
- [EU Adopts 21st Sanctions Package Against Russia — Global Trade & Sanctions Law, 3 Aug 2026](https://www.globaltradeandsanctionslaw.com/eu-21st-sanctions-package-russia/)
- [European Commission Approves Poland's KPO Payment Request of €7.9 Billion — 10 Aug 2026](https://knews.media/2026/08/10/european-commission-approves-polands-kpo-payment-request-of-e7-9-billion/)
- [CEE countries face a race against time as RRF deadline approaches — ING Think](https://think.ing.com/articles/cee-faces-race-against-time-eu-funds-absorption-lags-as-2026-rrf-deadline-approaches/)
- [Poland to receive record €43 bln in EU funds in 2026 — TVP World](https://tvpworld.com/90868791/record-eu-funds-for-poland-in-2026)
- [New CAP 2028–2034: farmers' protests erupt — FoodTimes](https://www.foodtimes.eu/planet/new-cap-farmers-protests/)
- [Common agricultural policy 2028-2034 — European Parliament Legislative Train](https://www.europarl.europa.eu/legislative-train/spotlight-MFF/file-common-agricultural-policy-2028-2034)
