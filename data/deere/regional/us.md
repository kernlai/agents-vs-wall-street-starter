# Regional desk: UNITED STATES — Deere & Company FY2026 Q3

**Desk:** desk-united-states · **As of:** 16 August 2026 · **Corpus frozen:** 14 August 2026
**Quarter under analysis:** FY2026 Q3, approximately 4 May – 2 August 2026
**Status:** Deere has **not** reported FY2026 Q3. The earnings call is 09:00 US Central, Thursday 20 August 2026. No FY2026 Q3 actuals exist and none are reported below.

**Data files**
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/regional/us.csv` (1,340 rows)
- Extractor: `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/extract_de_geo_matrix.py`
- Builder: `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/build_us_regional_csv.py`

**Basis warning.** Everything in the revenue tables below is the **ASC 606 revenue-recognition footnote** (revenue from contracts with customers, segment × primary geographic market). It does **not** tie to 8-K segment net sales. Q2 FY2026 PPA is 4,607 on this basis versus 4,503 in the 8-K segment table — a 104m gap. Where I use guidance (which is stated on the 8-K net-sales basis) to constrain a 606 figure, I say so.

---

## 1. The seven-year US history

Deere's ASC 606 geographic disclosure begins at adoption in fiscal 2019. FY2019 is presented on the **old three-segment structure** (Ag & Turf / C&F / FS); the four-segment PPA/SAT/CF/FS split was introduced in FY2020 and prior-year comparatives were restated in the FY2021 10-Qs, which is where the FY2020 four-segment quarters below come from.

**Q1–Q3 are reported figures lifted from the 10-Qs. Q4 is derived** as (fiscal-year total − nine months); Deere never publishes a Q4-only matrix. Every Q4 row in the CSV carries `source_type = filing_derived`. Reconciliation of the four quarters back to the published fiscal-year total is exact to ±1 (rounding) in all six years.

### US revenue by segment, ASC 606 basis, USDm

| FY | PPA Q1 | Q2 | Q3 | Q4* | SAT Q1 | Q2 | Q3 | Q4* | CF Q1 | Q2 | Q3 | Q4* | FS Q1 | Q2 | Q3 | Q4* | **US total** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2020 | 1,433 | 1,841 | 1,617 | 1,997 | 1,067 | 1,540 | 1,228 | 1,226 | 1,020 | 1,263 | 1,048 | 1,217 | 643 | 604 | 632 | 620 | 18,996 |
| 2021 | 1,608 | 2,211 | 1,995 | 2,409 | 1,424 | 1,838 | 1,753 | 1,491 | 1,202 | 1,481 | 1,559 | 1,455 | 598 | 608 | 605 | 577 | 22,814 |
| 2022 | 1,608 | 2,434 | 2,904 | 4,029 | 1,438 | 2,103 | 2,177 | 2,023 | 1,260 | 2,108 | 1,789 | 1,946 | 573 | 569 | 602 | 675 | 28,238 |
| 2023 | 2,628 | 4,058 | 3,394 | 3,838 | 1,665 | 2,241 | 2,098 | 1,791 | 1,901 | 2,561 | 2,346 | 2,302 | 713 | 766 | 860 | 944 | 34,105 |
| 2024 | 2,721 | 3,881 | 2,839 | 2,300 | 1,345 | 1,842 | 1,824 | 1,238 | 2,095 | 2,500 | 1,967 | 1,523 | 970 | 996 | 1,076 | 1,125 | 30,242 |
| 2025 | 1,555 | 2,512 | **1,684** | 2,001 | 949 | 1,626 | **1,537** | 1,170 | 1,113 | 1,717 | **1,687** | 1,972 | 1,085 | 1,072 | **1,100** | 1,193 | 23,974 |
| 2026 | 1,226 | 2,012 | — | — | 1,106 | 1,833 | — | — | 1,577 | 2,317 | — | — | 1,051 | 1,036 | — | — | — |

\* Q4 derived. **Bold = the Q3 FY2025 comparatives everything below is anchored on: PPA 1,684 / SAT 1,537 / CF 1,687 / FS 1,100 / total 6,008.**

FY2019 (three-segment): Q1 A&T 2,628, C&F 1,163, FS 575; Q2 3,912 / 1,738 / 604; Q3 2,870 / 1,594 / 632; Q4 (derived) 2,951 / 1,587 / 672. FY2019 US total 20,926.

### YoY, US, by segment and quarter

| Segment | FY2024 Q3 | FY2025 Q1 | Q2 | Q3 | Q4 | FY2026 Q1 | Q2 |
|---|---|---|---|---|---|---|---|
| PPA | −16.4% | −42.9% | −35.3% | **−40.7%** | −13.0% | −21.2% | −19.9% |
| SAT | −13.1% | −29.4% | −11.7% | **−15.7%** | −5.5% | +16.5% | +12.7% |
| CF | −16.2% | −46.9% | −31.3% | **−14.2%** | +29.5% | +41.7% | +34.9% |
| FS | +25.1% | +11.9% | +7.6% | **+2.2%** | +6.0% | −3.1% | −3.4% |
| Total | −11.4% | −34.1% | −24.9% | −22.0% | +2.4% | +5.5% | +3.9% |

The single most important structural fact for the Q3 forecast: **the three equipment segments' comparatives move in opposite directions in H2.** Q3 FY2025 was the *trough* for US PPA (−40.7%) and a *moderate* quarter for SAT (−15.7%), but US CF had already begun recovering by Q3 FY2025 (only −14.2%, then +29.5% in Q4). So the CF comp hardens sharply while the PPA comp gets easier. Deere said exactly this on the Q1 FY2026 call: *"PPA … you're probably the toughest comp is 2Q, and then get easier when you get to the back half of the year from a top-line perspective."* (`call-transcripts/2026-02-19__de-us-20260219-call-qna__605077.md`)

### US seasonality (sequential ratios)

| Segment | Q3/Q2 FY20 | FY21 | FY22 | FY23 | FY24 | FY25 | mean | last-3 mean |
|---|---|---|---|---|---|---|---|---|
| PPA | 0.878 | 0.902 | 1.193 | 0.836 | 0.732 | 0.670 | 0.869 | 0.746 |
| SAT | 0.797 | 0.954 | 1.035 | 0.936 | 0.990 | 0.945 | 0.943 | 0.957 |
| CF | 0.830 | 1.053 | 0.849 | 0.916 | 0.787 | 0.983 | 0.903 | 0.895 |
| FS | 1.046 | 0.995 | 1.058 | 1.123 | 1.080 | 1.026 | 1.055 | 1.076 |

n = 6 fiscal years. That is a small sample and I treat it as a sanity band, not a model. SAT's Q3/Q2 ratio is the only genuinely tight one (0.94–0.99 in five of six years); PPA's has been falling monotonically since FY2022 as Deere cut large-ag production, so a naive extrapolation of the FY2025 ratio would embed a fourth consecutive production cut that management has explicitly said is not happening.

### US share of Deere's global segment revenue (606 basis)

| | PPA | SAT | CF | FS | Total |
|---|---|---|---|---|---|
| FY2025 Q2 | 47.2% | 53.4% | 57.1% | 77.4% | 54.3% |
| FY2025 Q3 | **38.4%** | **49.8%** | **53.9%** | **77.6%** | **50.0%** |
| FY2026 Q1 | 37.5% | 49.7% | 57.7% | 75.9% | 51.6% |
| FY2026 Q2 | 43.7% | 51.8% | 60.1% | 75.8% | 53.8% |

Q3 is structurally the least-US quarter for PPA (Brazil's safrinha and Southern-Hemisphere shipments land there). The US has *lost* PPA share within Deere's own mix (H1 FY2026 41.1% vs H1 FY2025 47.9%) and *gained* CF share (+3.2pp H1-on-H1). FS is a stable ~76–78% US.

---

## 2. What actually happened in the US during May–July 2026

### 2a. Large ag retail collapsed further — and this is the biggest single risk to the PPA line

**Correction to the brief the desk was issued.** The Q2 FY2026 deck's "April 2026 Retail Sales (Rolling 3 Months)" table appears in the corpus markdown with the industry column rendered as bare positive numbers (12%, 4%, 14%, 24%, 5%). Those are **negative**. Two independent checks confirm it: (i) Deere's own adjacent column reads "Down more than the industry" / "Down less than the industry", which is incoherent against a positive industry; (ii) the magnitudes match AEM's actual negative YTD prints almost exactly (4WD −24% on the slide vs −23.6% AEM YTD-May). The corpus rendering has dropped the minus signs. Source: `slides/2026-05-21__de-us-20260521-slide__1042212.md`, lines 184–204.

Corrected reading, US & Canada ag industry retail, rolling 3 months to April 2026: **<40hp −12%, 40–100hp −4%, 100+hp −14%, 4WD −24%, combines −5%.** Deere: better than industry in <40hp, 40–100hp and 4WD; **worse than industry in 100+hp**; flat in combines.

Now the actual May–July window, from AEM's US reports:

| US retail units | May-26 | May-25 | %Chg | YTD-May 26 | YTD-May 25 | %Chg |
|---|---|---|---|---|---|---|
| 2WD <40 HP | 11,415 | 15,155 | −24.7% | 46,288 | 53,908 | −14.1% |
| 2WD 40–100 HP | 3,986 | 4,714 | −15.4% | 17,844 | 18,768 | −4.9% |
| 2WD 100+ HP | 1,270 | 1,416 | −10.3% | 5,881 | 7,161 | −17.9% |
| 4WD | 144 | 176 | −18.2% | 766 | 1,002 | −23.6% |
| Total tractors | 16,815 | 21,461 | −21.6% | 70,779 | 80,839 | −12.4% |
| Self-propelled combines | 138 | 314 | −56.1% | 1,066 | 1,248 | −14.6% |

July 2026: total tractors 15,985 vs 17,938, **−10.9%**; 2WD −10.5%; **4WD −38.7%**; combines −5.3%. YTD-July: tractors 105,185 (−13.1%), combines 1,676 (−10.2%), <40hp −15.1%, **100+hp −15.5%**.

Two readings, both true:
1. **Level:** US large-ag retail through the whole Q3 window ran down double digits. There was no spring recovery.
2. **Direction:** the 100+hp YTD decline *improved* from −17.9% (through May) to −15.5% (through July), implying the June–July months were better than the Jan–May average (July 2WD 100+hp roughly −7%). 4WD, by contrast, fell off a cliff in July (−38.7%). 4WD is a small unit category but a high-ASP one for Deere.

**Why Deere is underperforming the industry in 100+hp.** Management gave the answer directly on the Q1 FY2026 call: *"large ag in North America, over the last 12-18 months, we've ceded a little bit of share. I think as we've been leaner on the new inventory side, more focused on driving used down."* It is a deliberate trade: Deere refused to chase retail with new-machine discounting while it cleared the used book. The Q3 FY2025 8-K confirms the cost of the alternative — that quarter's PPA had *unfavourable* price realization "primarily driven by actions taken to address used inventory in North America." Deere is now lapping those incentives and has told the street price gets *better* in H2 FY2026 — which mechanically means it is still not buying share. Management's stated expectation is *"we've got some opportunity to gain some share as we move through the course of the year"*, but the April rolling-3-month data says the gap had not closed as of the start of the quarter, and nothing in the AEM series through July suggests it closed inside it.

**Inventory is the offsetting positive.** Deere dealer inventory as a % of trailing-12m retail: 100+hp 2WD **30%** (LY 31%), combines **12%** (LY 17%). Deere says new field inventory for both high-horsepower tractors and combines is down more than 50% from the mid-2024 peak with inventory-to-sales ratios in line with historical averages, and that used has finally broken: used combines down mid-teens from the March 2024 peak, used high-hp tractors down mid-teens from peak and down low single digits *sequentially in Q2 — a quarter that normally builds*, MY2022–23 8R tractors down ~45% from last year's peak, used sprayers −30%, used planters −50%. The JDF trade-wholesale portfolio (used on dealer lots) is down over 15% YoY. A 12% combine inventory ratio against 17% a year ago is the leanest combine position in the cycle and is a genuine restock argument for H2 builds.

### 2b. The 2026 crop year, farm economics and policy

- **Acreage** (USDA NASS, 30 June 2026): corn **95.3m acres, −3%**; soybeans **85.4m, +5%**; combined corn+soy+wheat 223.4m vs 225.3m for 2025/26.
- **Crop conditions deteriorated through the window.** Corn good/excellent **63% at 26 July** vs **73%** a year earlier, with poor/very-poor at 12% vs 7%; by 2 August corn had slipped to **61%**, soybeans 63%. Wide regional dispersion — Iowa 80%, Minnesota 77%, Wisconsin 74% against Nebraska and Ohio at 60%.
- **Drought.** 7 July 2026: 67.0% of the US abnormally dry or worse, **47.2% at D1+**; 19% of corn acres and 19% of soybean acres in D1–D4.
- **August WASDE (12 Aug 2026)** cut corn yield to **180.7 bu/ac** from 183.0 and soybeans to **52.7** from 53.0, but raised harvested area — soybean production 4.519bn bu would be the **largest US crop on record**. Season-average farm price raised to **$4.50/bu** corn; soybeans held at **$11.40/bu**.
- **Prices.** Global corn ran 215.6 $/mt in May 2026 (+5.3% YoY) then fell to 195.8 in June (flat YoY). Soybeans 439.1 $/mt in May (+13.3% YoY), 414.5 in June (+8.1%). Deere's framing on the Q2 call — *"commodity prices since August, both for soybeans and corn, they've been up like 20%"* — is measured off the August 2025 low, and the June pullback took some of that back inside the quarter.
- **Input costs went the wrong way.** WTI spiked from $64.51 (Feb) to **$100.32 April / $102.13 May** on the Iran conflict before easing to $84.81 June and $80.46 July; the IMF energy index went 159 → 242 → 232 → 199 over the same months. Fertilizer followed. Deere's mitigant — *"our customers in North America and Europe largely purchased these inputs ahead of the spring planting season when costs were lower"* — protects the 2026 crop's margin but not the 2027 planning that drives the spring early-order programs opening in May–September 2026.
- **Farm income.** USDA ERS (February 2026 vintage, the current one) forecasts CY2026 net farm income at **$153.4bn**, −0.7% nominal / −2.6% real vs 2025 but still above the 2005–24 real average; net cash farm income **$158.5bn**, +3.0%. **The September 3 2026 update lands after Deere's Q3 print** — so no new vintage will have moved sentiment inside the quarter.
- **Credit and land.** Kansas City Fed Q2 2026 ag credit survey: credit conditions continued to deteriorate gradually but financial stress remained **modest**; cropland values strong and ranchland at record highs; farm income subdued but the *pace* of decline slowed as corn, soybean and wheat prices rose; commercial-bank farm lending declined for nearly all non-real-estate purposes. Fed funds sat at 3.63% all quarter with the 10-year at 4.63–4.72% in mid-August — financing costs are not improving.
- **Government support.** The $12bn Farmer Bridge Assistance Program (announced Dec 2025, soybeans $30.88/acre) was targeted for release by 28 February 2026 and provided liquidity into the buying season. Deere flagged the **supplemental disaster relief payment factor rising from 35% to 70%** during the quarter.
- **Biofuel policy turned positive.** EPA's final RFS rule (27 March 2026) set record volumes — 25.82bn RINs for 2026, 25.98bn for 2027 — and held the conventional (corn ethanol) requirement at 15bn gallons; the House passed year-round E15 during the quarter. Deere's own view: *"we don't expect these developments to meaningfully adjust demand levels this fiscal year"* — real, but a FY2027 story.
- **Farm bill.** The 2018 Farm Bill remains extended at existing funding through **30 September 2026**, with the One Big Beautiful Bill Act (2025) updating some programmes. Unresolved through the quarter; a source of planning uncertainty rather than an active driver.

### 2c. Tariffs and trade — the quarter's largest single P&L event was a US policy event

The Supreme Court struck down the IEEPA tariffs on **20 February 2026** (one day after Deere's Q1 call). Section 122 10% surcharges were imposed within hours; Section 232 was adjusted. Deere recognised a **$272m IEEPA refund in Q2 FY2026** — c.2.5pts of equipment-operations margin, split ~50% CF / ~30% SAT / ~20% large ag. Full-year gross tariff exposure is unchanged at **~$1.2bn (~3pts of margin)**, ~$900m net of the refund. Deere is not surcharging; net price realization for equipment ops is guided 1.5–2.0% for the year against ~1.5–2.0% ex-tariff inflation.

Two live items inside the Q3 window: the **US Court of International Trade struck down the Section 122 tariffs in May 2026** (under appeal), and the Section 122 tariffs were **set to expire 24 July 2026**. Either could produce a further refund or a further regime change. I would not model a second $272m windfall — but the tail is not zero, and it is a revenue-neutral, margin-only item in any case.

Structurally the US is insulated: ~80% of Deere's US complete-good sales are built in US plants, and ~75% of components at those plants are US-sourced. Deere started building US-designed excavators at Kernersville, NC in the quarter (a $70m expansion) and reaffirmed $20bn of US manufacturing investment over ten years.

### 2d. Construction & forestry — the US end market is more mixed than the segment result

The official spending data is soft:

| US construction spending, $m SAAR | Jun-25 | Jun-26 | YoY |
|---|---|---|---|
| Total | 2,237,719 | 2,166,539 | **−3.2%** |
| Private total | 1,702,574 | 1,622,458 | −4.7% |
| Private non-residential | 1,304,452 | 1,277,174 | −2.1% |
| Public | 535,146 | 544,081 | **+1.7%** |
| Highway & street | 147,730 | 152,065 | **+2.9%** |

Housing starts: 1,199k SAAR in May (−7.0% YoY), 1,427k in June (+3.5%); single-family stuck at 895–917k and drifting down. Residential is a drag and Deere's own **global forestry guide is −5%** on weak residential and low log/lumber prices.

The offsets are concentrated and large: highway/street +2.9% supports Wirtgen roadbuilding (guide raised to **~+10% globally** during the quarter); data-centre construction spending is up ~46% YoY with YTD-April at $49.5bn against $13.6bn a year earlier; the ABC Construction Backlog Indicator hit a 10-month high around 8.2 months, with data-centre-tied contractors at 11.0 months versus 7.8 for everyone else. Deere: *"our order book continues to strengthen, up more than 60% since November, now at its highest level since April of 2024, with over 80% of production slots filled for the year"*, plus CONEXPO 2026 with 140,000 contractors and nearly all new-excavator production slots spoken for.

**So the CF revenue story is not an end-market volume story.** It is (i) lapping severe H1 FY2025 underproduction, (ii) share gain after pricing adjustments at the end of FY2025 — management confirmed *"we have seen some pickup in share over the past 12 months, particularly in the last six"*, and (iii) roadbuilding and infrastructure. Deere itself sized the gap: industry earthmoving +5% against segment sales +29%. That distinction matters for how durable the Q3 number is.

---

## 3. Q3 FY2026 US forecast

### Constraints I am forecasting inside

- FY2026 guidance (21 May 2026, 8-K net-sales basis): PPA −5 to −10%, SAT ~+15%, CF ~+20%.
- Implied H2: PPA 7,914–8,779 (mid 8,347) vs 8,978 LY, **−7.0%**; SAT 6,105 vs 5,474, **+11.5%**; CF 7,198 vs 6,451, **+11.6%**. All three decelerate hard from H1 (PPA −8%, SAT +19%, CF +31%).
- Management cadence, verbatim: *"back half to be higher than the front half, Q4 would be a little bit higher than Q3."* Large Ag: *"Q4 a bit stronger than Q3 … we've got more Waterloo large tractor shipments shipping to North America in the back half than the front half of the year. That's abnormal for us"*, and *"a much heavier fourth quarter with respect to our large tractors that are going to be settled here in the U.S."* Small Ag: *"a little bit of a step down in Q3 and another step down in Q4, just on a normal seasonal basis."* C&F: *"fairly balanced between the two … maybe a little bit stronger in the fourth quarter than Q3, but overall pretty close."*
- Q3 FY2025 comparatives (8-K): PPA 4,273, SAT 3,025, CF 3,059 = 10,357 equipment-ops net sales; total NS&R 12,018.
- Street consensus for Q3 FY2026: equipment-ops net sales ~$10.87bn (+4.95%), EPS $4.85. **Global, not US.** I use it only as a cross-check on my implied global totals.

### Triangulation, by segment

**PPA — central 1,440, −14.5%.** Four methods:
| Method | Result |
|---|---|
| Q3/Q2 seasonality at FY2025's 0.670 / last-3 0.746 / 0.80 (NA back-half skew) | 1,348 / 1,501 / 1,610 |
| US share of global PPA (global Q3 606 ≈ 4,060; LY US share 38.4%; H1 gap −6.8pp, narrowing to −3pp) | 1,283 – 1,437 |
| Bottom-up residual: global 4,060 less my estimates for Canada 295, W.Europe 711, C.Europe/CIS 331, LatAm 897, AAOME 359 | **1,467** |
| Straight continuation of H1's −20.4% | 1,340 |

The bear case is the AEM data (100+hp −15.5% YTD, 4WD −38.7% in July, Deere still ceding share) plus Q3 being structurally the least-US quarter for PPA. The bull case is that Q3 FY2025 was the trough print (−40.7%), inventory is finally clean, Deere told the street the PPA comp *gets easier* in H2, and the Waterloo large-tractor build is skewed to North America in H2 — although management pointed that at **Q4**, not Q3 ("production rates are significantly higher" in Q4). I land just below the bottom-up residual at **1,440**, and I would rather the team treated the 1,300–1,590 band as real than the point estimate as precise.

**SAT — central 1,700, +10.6%.** Seasonality (0.945–0.957 × 2,012… i.e. × 1,833) gives 1,732–1,754; share-of-global gives 1,595–1,693; relative-YoY (US ran 3.6pp below global in Q2, gap narrowing) gives 1,614–1,675. The comp hardens materially: Q3 FY2025 SAT was only −15.7% and global SAT was seasonally *up* Q2→Q3 in FY2025 (1.014), so "normal seasonality" in FY2026 is itself a headwind. Turf and compact are the genuine bright spot — AEM <40hp is down at industry level but Deere is outperforming, dairy/livestock margins are strong, and last year's underproduction left clean inventory.

**CF — central 2,050, +21.5%.** Unusually, all three methods converge: seasonality 2,317 × 0.895 = 2,074; share-of-global (global Q3 606 ≈ 3,612 at +15.5%, US share 53.9% + 3.2pp) = 2,062; H1→H2 with Q3≈Q4 = 2,062. I shade fractionally below to respect the soft aggregate construction spending. This is the segment where my number is furthest above the segment's *guided* H2 growth (+11.6% globally) — justified because the US has outrun global CF by 6–7pp every quarter this year (Q2: US +34.9% vs global +28.2%).

**FS — central 1,070, −2.7%.** The most stable line in the file: three consecutive quarters within ±3.5%, driven by a shrinking average portfolio (JDF trade wholesale −15% YoY) against a flat rate environment (fed funds 3.63% all quarter). Seasonality (Q3/Q2 last-3 mean 1.076) argues 1,115; YoY continuation argues 1,064. I sit near the YoY read because the portfolio is still contracting.

### Summary

| Segment | Q3 FY2025 actual | Q3 FY2026 central | YoY | Range | Confidence |
|---|---|---|---|---|---|
| PPA | 1,684 | **1,440** | −14.5% | 1,300–1,590 | low |
| SAT | 1,537 | **1,700** | +10.6% | 1,600–1,790 | medium |
| CF | 1,687 | **2,050** | +21.5% | 1,900–2,180 | medium |
| FS | 1,100 | **1,070** | −2.7% | 1,030–1,110 | high |
| **US total** | **6,008** | **6,260** | **+4.2%** | 5,830–6,670 | medium |

Implied US share of Deere global 606 revenue in Q3 FY2026 ≈ 51.1% (LY 50.0%), on a global Q3 606 total of roughly 12,240 (+1.8%) derived from consensus equipment-ops net sales plus ~1,370 of FS revenue. That is internally consistent: the US gains mix share on CF strength and loses it on PPA weakness, netting slightly positive.

---

## 4. Risks to this call

1. **PPA is the whole variance.** The four methods span 1,283–1,610 — a ±11% band on the largest ag line. If Deere pushed more of the Waterloo North America build into Q3 than the "much heavier Q4" language implies, PPA prints near 1,600 and the US total beats. If the July 4WD collapse (−38.7%) is a leading indicator of order-book cancellations rather than a small-category monthly artefact, PPA prints near 1,300.
2. **CF's comp inflection.** US CF went from −14.2% in Q3 FY2025 to +29.5% in Q4 FY2025. My +21.5% for Q3 requires the restock and share tailwinds to still be running. Total US construction spending is −3.2% YoY and private non-residential is −2.1%; only public (+1.7%), highway (+2.9%) and data centres are growing. A Q3 CF print below +12% would suggest the restock is already done and would carry straight into a weak Q4.
3. **A second tariff windfall.** The CIT struck down Section 122 in May 2026 and the tariffs were set to expire 24 July 2026. A further refund would inflate margin, not revenue, but it would obscure the underlying read for everyone modelling this quarter — and it would be recognised in the US.
4. **Crop deterioration is a two-sided risk.** Corn G/E at 61–63% against 73% LY with 19% of corn acres in D1+ drought supports prices (bullish for 2027 farmer cash) while cutting 2026 bushels for affected growers (bearish for immediate liquidity). The August WASDE resolved it toward "smaller yield, bigger acreage, higher price" — mildly net positive.
5. **The FY2027 early-order programmes are being written inside and just after this window** (sprayers opened early May, close end-August; planters opened early June, close end-September). Deere would only say results *"thus far would support our view that 2026 still marks the bottom."* Commentary on the 20 August call about EOP take-rates will move FY2027 far more than the Q3 revenue number itself.
6. **Share.** Deere has ceded 100+hp share for 12–18 months by choice and has not yet demonstrably won it back. The disciplined-price strategy improves H2 price realization but caps volume.

## 5. Caveats on the data

- Q4 rows in every fiscal year are **derived** (FY total − nine months), not reported.
- FY2019 is on the pre-reorganisation three-segment basis and is not comparable to FY2020+ without the FY2021 restatement, which only covers FY2020.
- The 606 footnote does not reconcile to 8-K segment net sales; all guidance is on the 8-K basis and I convert explicitly where I use it.
- The Q2 FY2026 slide's retail-sales percentages are **sign-corrupted in the corpus markdown**; I have restored the signs from AEM's published actuals and from Deere's own adjacent commentary column, and flagged the correction on every affected CSV row.
- The USDA ERS farm income figures are the **February 2026 vintage**; the September 3 2026 update post-dates Deere's Q3 report.
- The AEM June 2026 report could not be retrieved in full (GlobeNewswire and the AEM PDF endpoint both failed); June is therefore represented only through the YTD-July aggregates rather than as a standalone month. That is a gap, not a zero.
- INDEX.md labels `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` as "Q3 2026". It is **Q2 FY2026 Q&A** — the file's own header line says "Q3 2026 Earnings Call Transcript" but its content is the 21 May 2026 Q2 call. I have treated it as Q2 material throughout.
- Sample sizes are small: six fiscal years of four-segment quarterly US data (24 usable quarters, 22 with a prior-year comparative). I have deliberately not reported correlation coefficients between US drivers and US revenue, because at n≈24 with strongly trending series almost any such correlation would be spurious.

## Sources

Corpus (all paths relative to `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`):
`filings/2026-05-21__de-us-20260521-q2-10q__1055929.md`, `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md`, `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`, `filings/2026-02-26__de-us-20260226-q1-10q__636995.md`, `filings/2025-08-14__de-us-20250814-q3-10q__155834.md`, `filings/2025-08-15__de-us-20250815-q3-8k__143410.md`, `filings/2025-12-18__de-us-20251218-fy-10k__393777.md`, `filings/2023-12-15__de-us-20231215-fy-10k__645297.md`, `filings/2021-12-16__de-us-20211216-fy-10k__645298.md`, plus the FY2015–FY2026 10-Q/10-K series enumerated by the extractor; `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md`, `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`, `call-transcripts/2026-02-19__de-us-20260219-call-qna__605077.md`, `call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md`, `call-transcripts/2025-08-15__de-us-20250815-call-q3-pres__143406.md`; `slides/2026-05-21__de-us-20260521-slide__1042212.md`.

Web (accessed 16 August 2026):
- [AEM United States Ag Tractor and Combine Report, May 2026 (released 10 Jun 2026)](https://www.aem.org/getattachment/a717c93d-4798-4bfb-8daf-555dda8cd403/May-2026-Farm_Flash_Trade_Press_With_Chart_PreRelease-United-States.pdf)
- [AEM United States Ag Tractor and Combine Report, July 2026 (released 11 Aug 2026)](https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html)
- [RFD-TV, "Farm Equipment Sales Remain Weak Through July 2026", 13 Aug 2026](https://www.rfdtv.com/farm-equipment-sales-remain-weak-through-july-2026)
- [USDA NASS Acreage, 30 June 2026](https://www.nass.usda.gov/Newsroom/2026/06-30-2026.php)
- [DTN/PF, USDA Crop Progress, 27 July 2026](https://www.dtnpf.com/agriculture/web/ag/news/article/2026/07/27/usda-crop-progress-corn-rated-63-63)
- [DTN/PF, USDA Crop Progress, 3 August 2026](https://www.dtnpf.com/agriculture/web/ag/news/article/2026/08/03/usda-crop-progress-corn-rated-61-63)
- [DTN/PF, August 2026 Crop Production / WASDE, 12 Aug 2026](https://www.dtnpf.com/agriculture/web/ag/news/article/2026/08/12/usda-releases-august-crop-production-4)
- [Pro Farmer, US Drought Monitor, July 2026](https://www.profarmer.com/news/drought-monitor-shows-little-change-overall-u-s-conditions)
- [USDA ERS, Highlights from the Farm Income Forecast (February 2026 vintage)](https://www.ers.usda.gov/topics/farm-economy/farm-sector-income-finances/highlights-from-the-farm-income-forecast)
- [Kansas City Fed, Ag Credit Survey Q2 2026 / New Farm Loan Originations Ease Slightly](https://www.kansascityfed.org/center-for-agriculture-and-the-economy/agricultural-finance/new-farm-loan-originations-ease-slightly/)
- [EPA, Final Renewable Fuel Standards for 2026 and 2027 (27 Mar 2026)](https://www.epa.gov/renewable-fuel-standard/final-renewable-fuel-standards-2026-and-2027)
- [USDA, $12bn Farmer Bridge Payments (8 Dec 2025)](https://www.usda.gov/about-usda/news/press-releases/2025/12/08/trump-administration-announces-12-billion-farmer-bridge-payments-american-farmers-impacted-unfair)
- [CRS, Supreme Court Rules Against IEEPA Tariffs](https://www.congress.gov/crs-product/LSB11398)
- [Skadden, US Trade Court Strikes Down Section 122 Tariffs (May 2026)](https://www.skadden.com/insights/publications/2026/05/us-trade-court-strikes-down-section-122-tariffs)
- [CRS R48918, The 2026 Farm Bill: Comparison of the House and Senate Bills with Current Law](https://www.congress.gov/crs-product/R48918)
- [Construction Equipment, 2026 Construction Overview: Data Centers, Highways, Housing, and Jobs](https://www.constructionequipment.com/industry-news/article/55397202/2026-construction-overview-data-centers-highways-housing-and-jobs)
- [Yahoo Finance, Deere & Company Earnings Preview](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html)
- FRED keyless CSV endpoint, series HOUST, HOUST1F, TTLCONS, TLPRVCONS, TLNRESCONS, TLPBLCONS, TLHWYCONS, PMAIZMTUSDM, PSOYBUSDM, MCOILWTICO, PNRGINDEXM, FEDFUNDS — `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>`
