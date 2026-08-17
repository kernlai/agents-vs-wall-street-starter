# Deere FY2026 Q3 — Construction & Forestry and Small Ag & Turf

**Analyst brief · prepared 16 August 2026 · Deere has NOT reported FY2026 Q3**

Deere's FY2026 Q3 covers ~4 May – 2 August 2026. The results are scheduled for release on
**Thursday, 20 August 2026, 9:00 a.m. Central** (REPORTED FACT — stated on the last page of
`slides/2026-05-21__de-us-20260521-slide__1042212.md`, and corroborated by
[stocktitan.net/news/DE/deere-to-announce-third-quarter-2026-financial-ws5vrthl5ifm.html](https://www.stocktitan.net/news/DE/deere-to-announce-third-quarter-2026-financial-ws5vrthl5ifm.html), 5 Aug 2026).

## 0. Metadata trap — resolved

The corpus `INDEX.md` row reading `2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call
Transcript` → `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` is **mislabelled**.
Its YAML header says `period: "Q3 2026"`, but the body is the **Q2 FY2026 earnings-call Q&A of
21 May 2026**: it discusses the $272M IEEPA refund booked in Q2, "our second quarter came in largely
in line", and the *forward* Q3/Q4 cadence. **There are no FY2026 Q3 actuals anywhere in the corpus or
on the public web.** Everything below marked ESTIMATE or INFERENCE is mine.

That mislabelled file is nonetheless the single most valuable document for this task — it contains the
segment-level H2 cadence guidance and the tariff-refund split.

---

## 1. Reported baseline — segment quarterly history

**REPORTED FACT.** Net sales, $M. Sources: quarterly 8-K earnings releases in `filings/`
(FY23 Q1–Q4 from `2024-02-15…q1-8k`, `2024-05-16…q2-8k`, `2023-08-18…q3-8k`, `2023-11-22…q4-8k`;
FY24/FY25 from the matching-year 8-Ks; FY26 Q1 from `2026-02-19__de-us-20260219-q1-8k__603009.md`;
FY26 Q2 from `2026-05-21__de-us-20260521-q2-8k-2__1042168.md`).

| Quarter | PPA | SA&T | C&F | Equip. total |
|---|---|---|---|---|
| FY23 Q1 | 5,198 | 3,001 | 3,203 | 11,402 |
| FY23 Q2 | 7,822 | 4,145 | 4,112 | 16,079 |
| FY23 Q3 | 6,806 | 3,739 | 3,739 | 14,284 |
| FY23 Q4 | 6,965 | 3,094 | 3,742 | 13,801 |
| **FY23** | **26,790** | **13,980** | **14,795** | **55,565** |
| FY24 Q1 | 4,849 | 2,425 | 3,212 | 10,486 |
| FY24 Q2 | 6,581 | 3,185 | 3,844 | 13,610 |
| FY24 Q3 | 5,099 | 3,053 | 3,235 | 11,387 |
| FY24 Q4 | 4,305 | 2,306 | 2,664 | 9,275 |
| **FY24** | **20,834** | **10,969** | **12,956** | **44,759** |
| FY25 Q1 | 3,067 | 1,748 | 1,994 | 6,809 |
| FY25 Q2 | 5,230 | 2,994 | 2,947 | 11,171 |
| FY25 Q3 | 4,273 | 3,025 | 3,059 | 10,357 |
| FY25 Q4 | 4,740 | 2,457 | 3,382 | 10,579 |
| **FY25** | **17,311** | **10,224** | **11,382** | **38,917** |
| FY26 Q1 | 3,163 | 2,168 | 2,670 | 8,001 |
| FY26 Q2 | 4,503 | 3,485 | 3,790 | 11,778 |
| FY26 H1 | 7,666 | 5,653 | 6,460 | 19,779 |
| FY26 Q3 | **not reported** | **not reported** | **not reported** | — |

**REPORTED FACT.** Segment operating profit, $M (same sources).

| Quarter | PPA | SA&T | C&F | C&F margin | SA&T margin |
|---|---|---|---|---|---|
| FY23 Q3 | 1,782 | 732 | 716 | 19.1% | 19.6% |
| FY23 FY | 6,996 | 2,472 | 2,695 | 18.2% | 17.7% |
| FY24 Q3 | 1,162 | 496 | 448 | 13.8% | 16.2% |
| FY24 FY | 4,514 | 1,627 | 2,009 | 15.5% | 14.8% |
| FY25 Q1 | 338 | 124 | 65 | 3.3% | 7.1% |
| FY25 Q2 | 1,148 | 574 | 379 | 12.9% | 19.2% |
| FY25 Q3 | 580 | 485 | 237 | 7.7% | 16.0% |
| FY25 Q4 | 604 | 25 | 348 | 10.3% | 1.0% |
| **FY25 FY** | **2,671** | **1,207** | **1,028** | **9.0%** | **11.8%** |
| FY26 Q1 | 139 | 196 | 137 | 5.1% | 9.0% |
| FY26 Q2 | 706 | 719 | 561 | 14.8% | 20.6% |
| FY26 H1 | 845 | 916 | 698 | 10.8% | 16.2% |

Other Q3 FY25 anchors (REPORTED FACT, `filings/2025-08-15__de-us-20250815-q3-8k__143410.md`):
Financial Services revenues **$1,418M**; Other revenues **$243M**; total net sales & revenues
**$12,018M**; net income **$1,289M**; **diluted EPS $4.75**; diluted shares **271.4M**.
Q2 FY26 diluted shares: **270.8M** (`filings/2026-05-21…q2-8k-2`, line 280).

---

## 2. Company guidance in force (as of 21 May 2026) — the arithmetic spine

**REPORTED FACT** — `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` and
`call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md`.

### FY2026 industry outlook — evolution across the year

| Industry line | Nov 2025 (Q4 guide) | Feb 2026 (Q1 guide) | **May 2026 (Q2 guide)** | Direction |
|---|---|---|---|---|
| US/Canada Construction Equipment | Flat to up 5% | Up ~5% | **Up ~5%** | held |
| US/Canada Compact Construction Equip. | Flat to up 5% | Up ~5% | **Up ~5%** | held |
| Global Forestry | Flat | Flat | **Down ~5%** | **cut** |
| Global Roadbuilding | Flat | Up ~5% | **Up ~10%** | **raised twice** |
| US/Canada Small Ag & Turf | — | Flat to up 5% | **Flat to up 5%** | held |

### FY2026 Deere segment outlook — evolution

| Segment | Nov 2025 | Feb 2026 | **May 2026** | FX | Price |
|---|---|---|---|---|---|
| PPA net sales | Down 10% | Down 5–10% | **Down 5–10%** | +3.0% | ~+1.0% |
| SA&T net sales | Up ~10% | Up ~15% | **Up ~15%** | +1.0% | ~+1.5% |
| C&F net sales | Up ~10% | Up ~15% | **Up ~20%** | +2.0% | ~+2.5% |
| PPA op margin | — | 11–13% | **11–13%** | | |
| SA&T op margin | — | 13.5–15% | **13.5–15%** | | |
| C&F op margin | — | (raised at Q2) | **10–12%** | | |
| FS net income | ~$830 | ~$840 | **~$860** | | |
| Deere net income | — | $4.5–5.0B | **$4.5–5.0B** | | |
| Effective tax rate | — | — | **24–26%** | | |

### Implied H2 FY2026 from the guide (MY INFERENCE, arithmetic only)

| Segment | FY26 guide $M | less H1 actual | = H2 implied $M | vs H2 FY25 |
|---|---|---|---|---|
| PPA (−5% / −10%) | 16,445 / 15,580 | 7,666 | 8,779 / 7,914 | 9,013 → **−3% to −12%** |
| SA&T (+15%) | 11,758 | 5,653 | 6,105 | 5,482 → **+11%** |
| C&F (+20%) | 13,658 | 6,460 | 7,198 | 6,441 → **+12%** |

### Management's explicit H2 cadence (REPORTED FACT — the mislabelled Q&A file, line 97)

> "…**Small Ag** side, it's pretty normal seasonality. You'll get a little bit of a step down in Q3
> and another step down in Q4… **Construction & Forestry, fairly balanced between the two. Both top
> line and margin in the back half, maybe a little bit stronger in the fourth quarter than Q3, but
> overall pretty close.** I wouldn't call out anything specifically abnormal."

Also: "price gets more favorable in the back half… production cost side, including tariffs and
material costs, that gets more favorable as well. **Price cost will improve as we move through the
balance of the fiscal year**" — because Deere laps both the H2-FY25 tariff onset and the H2-FY25 C&F
and large-ag discounting.

### CRITICAL non-repeating item — the $272M IEEPA tariff refund

**REPORTED FACT** (Q2 8-K note + mislabelled Q&A, lines 27–29). On 20 Feb 2026 the US Supreme Court
invalidated IEEPA tariffs; Deere booked a **$272M recovery in Q2 FY26**, sitting inside the
"Production Costs" line of each segment. Management's split of the refund:
**~50% C&F (~$136M), ~30% SA&T (~$82M), ~20% large ag (~$54M).** The ongoing tariff run-rate is
unchanged at **~$1.2B/yr** (~45% C&F, ~⅓ SA&T, ~20% large ag).

**MY INFERENCE — the clean Q2 baseline that Q3 must be built off:**

| Segment | Q2 FY26 reported OP | less refund | = underlying OP | underlying margin |
|---|---|---|---|---|
| C&F | 561 | (136) | **~425** | **~11.2%** (not 14.8%) |
| SA&T | 719 | (82) | **~637** | **~18.3%** (not 20.6%) |
| PPA | 706 | (54) | **~652** | **~14.5%** (not 15.7%) |

This is the biggest single trap in modelling Q3: the reported Q2 margins are ~1.2–3.5pts flattered.

---

## 3. Construction & Forestry — demand evidence, May–July 2026

### 3a. Deere's own order-book and retail data (REPORTED FACT, corpus)

| Datapoint | Value | Source |
|---|---|---|
| C&F order book, US/Canada | **up >60% since November 2025**, highest since April 2024; **>80% of FY production slots filled** | Q2 call Q&A/pres, `call-pres__1042774.md` line 115 |
| Same metric one quarter earlier | up >50% in the quarter, highest since May 2024 | Q1 call, `call-pres__605076.md` line 75 |
| Q1 FY26 retail settlements, CE and compact CE | both **up mid-teens** YoY | Q1 call, line 75 |
| Rolling-3-month retail to April 2026, US/Canada Earthmoving & Forestry (Deere) | **up low double digits** | Q2 slide deck appendix |
| Data-center construction | expected to **top $100B in 2026**, double-digit growth into 2027 | Q2 call, line 119 |
| Deere share | "seen some pickup in share over the past 12 months… particularly in the last six" after end-FY25 pricing adjustments | mislabelled Q&A, line 17 |
| Wirtgen / roadbuilding | "road building performance also remains stellar"; strength in **both North America and Europe** | Q2 call line 119; Q1 Q&A line 39 |

### 3b. External read-across (REPORTED FACT, web)

| Source | Period | Datapoint |
|---|---|---|
| **Caterpillar** Q2 2026 release, 4 Aug 2026 — [prnewswire](https://www.prnewswire.com/news-releases/caterpillar-reports-second-quarter-2026-results-302841940.html) | Apr–Jun 2026 (≈ Deere FQ3) | Construction Industries sales **$8.346B, +35% YoY**; **North America $5.065B, +50%**; LatAm $676M +25%; EAME $1.456B +23%; Asia/Pac $1.064B +3%. CI segment profit **$1.947B, +57%**, margin **23.3% vs 20.1%**. Volume +$1.755B, price +$309M. Total company $20.543B, +24% — first-ever $20B quarter. |
| **United Rentals** Q2 2026, 23 Jul 2026 — [investors.unitedrentals.com](https://investors.unitedrentals.com/press-releases/press-releases-details/2026/United-Rentals-Announces-Record-Second-Quarter-Results-and-Raises-Full-Year-2026-Guidance/default.aspx) | Apr–Jun 2026 | Record revenue **$4.410B**; rental revenue $3.849B; **fleet productivity +3.4%**; adj. EBITDA $2.056B (46.6% margin); **raised FY26 guide to $17.5–17.8B revenue, gross capex $4.85–5.25B**. Cited "tailwinds across large projects, customer backlogs". |
| **Astec Industries** Q2 2026, 5 Aug 2026 — [globenewswire](https://www.globenewswire.com/news-release/2026/08/05/3339170/0/en/astec-reports-second-quarter-2026-results.html) | Apr–Jun 2026 | Record revenue **$408.1M, +23.6%**; adj. EBITDA $42.6M +26%; **backlog +57.9% to $601.1M**. Infrastructure Solutions $228.3M **+11.6%** on concrete/mobile paving/forestry demand. FY EBITDA guide *cut* to $160–175M on asphalt-plant delivery timing. |
| **ARA** rental forecast, updated May 2026 — [ope-plus.com](https://ope-plus.com/2026/05/29/ara-updates-forecast-for-equipment-and-event-rental-markets/26342/) | CY2026 | US CIE + general tool rental **+3.6% to $83.5B** (raised from +2.8%/$82.9B); Canada **+5% to $6.3B**; 2027 +3.8%. |
| **Dodge Momentum Index**, 10 Aug 2026 — [construction.com](https://www.construction.com/dodge-momentum-index-improves-7-in-july/) | July 2026 | DMI **291.7, +6.9% m/m**, **+11.7% YoY**; commercial +4.1% m/m (+13.8% YoY), institutional +13.1% m/m. Data-center planning re-accelerated after a June pause. |

### 3c. The counter-evidence — put-in-place spending and housing are NEGATIVE

| Source | Period | Datapoint |
|---|---|---|
| **Census C30**, 3 Aug 2026 — [census.gov/construction/c30](https://www.census.gov/construction/c30/pdf/release.pdf); summary at [Construction Dive, 4 Aug 2026](https://www.constructiondive.com/news/construction-spending-june-2026-drop-data-centers/826936/) | June 2026 | Total construction spending **$2,166.5B SAAR, −0.1% m/m and −3.2% YoY**. Private nonres **$745.3B, +0.1% m/m but −4.7% YoY**; **ex-data-centres −7.9% YoY**. 8 of 16 categories declining. ABC's Basu: private nonres peaked April 2025 and has fallen >7% since. AGC flags highway risk if Congress does not reauthorise. |
| **Census/HUD New Residential Construction**, 17 Jul 2026 — [census.gov/construction/nrc](https://www.census.gov/construction/nrc/pdf/newresconst.pdf) | June 2026 | Total starts **1,427k SAAR, +19.0% m/m, +3.5% YoY** (vs 1,379k Jun-25) — but the gain is multifamily (5+ units **513k**). **Single-family 895k, −0.2% m/m** and soft. July data releases 18 Aug 2026, i.e. after this brief. |
| **Madison's Lumber Reporter**, Jul–Aug 2026 — [madisonsreport.com](https://madisonsreport.com/limited-supply-keeps-lumber-prices-buoyant/) | Jul 2026 | Western S-P-F 2×4 #2&Btr KD: $500/mfbm w/e 17 Jul, $510 w/e 24 Jul, $516 w/e 31 Jul — **flat YoY** in mid-July. Prices firm only because of **sawmill curtailments and closures**, not demand. |
| **IIJA reauthorisation** — [NACo](https://www.naco.org/news/iija-authorities-expire-september-30-naco-urges-congress-uphold-full-funding-levels-highway) | 30 Sep 2026 | IIJA surface-transportation authorities **expire 30 September 2026** — *after* Deere's Q3 close, so no Q3 impact, but a live FY2027 roadbuilding risk. House BUILD America 250 Act (H.R. 8870, May 2026) proposes +7% highway / +12% bridge funding. |

**MY INFERENCE on the divergence:** dollar put-in-place spending is falling YoY while equipment sales
are up 25–50% YoY. That is not a contradiction — it is a *fleet* story, not an *activity* story:
(i) Deere and Cat both underproduced retail in H1 FY2025, so FY2026 wholesale shipments lap an
artificially low base (Deere management, Q1 call line 49: "we did some pretty strong under-production
last year… close to 10% for the segment"); (ii) rental fleets deferred replacement for two years and
are now repleting (URI capex guide raised; ARA forecast raised); (iii) the mix of activity has shifted
to large, equipment-intensive site-prep work (data centres, utilities) even as total dollars fall.
The corollary is that the C&F upcycle is **restock- and replacement-driven, not demand-driven**, and is
therefore more fragile into FY2027 than the order book alone suggests.

---

## 4. Small Ag & Turf — demand evidence

### 4a. Deere's own data (REPORTED FACT, corpus)

- Q2 FY26 SA&T **+16% to $3,485M**, OP **$719M / 20.6% margin** — the highest segment margin in the
  company that quarter. Drivers: higher shipment volumes, +~1.5pt price, +~2.5pt FX
  (`call-pres__1042774.md`, line 39).
- Rolling-3-month retail to April 2026, US/Canada **Selected Turf and Utility Equipment: up low
  double digits** (Deere internal, Q2 slide appendix).
- "Modest strengthening in the turf markets as demand has expanded **following several years of
  industry decline**"; "dairy and livestock sector also continues to maintain strong margins"
  (Q2 call, line 43).
- Q1 FY26: "order velocity for **North American turf equipment and compact utility tractors has
  increased**" (`call-pres__605076.md`, line 23).
- Field inventory: "current new field inventory for **both** tractor horsepower categories in this
  segment (<100hp and 100–220hp) are each **about 40% lower year-over-year**" (Q1 call, line 69);
  "favorable inventory levels are being maintained following last year's underproduction, and we
  continue to execute against our plan to **build in line with retail demand** this fiscal year"
  (Q2 call, line 131).
- Segment position in the cycle: "Large Ag is operating below trough levels, **Small Ag & Turf is
  progressing towards mid-cycle**, and Construction & Forestry is **slightly above mid-cycle**"
  (Q2 call, line 65).

### 4b. External read-across

| Source | Period | Datapoint |
|---|---|---|
| **Toro** Q2 FY2026 (qtr ended 1 May 2026), reported 4 Jun 2026 — [10-Q](https://www.sec.gov/Archives/edgar/data/0000737758/000073775826000018/ttc-20260501.htm); [Las Vegas Sun, 4 Jun 2026](https://lasvegassun.com/news/2026/jun/04/the-toro-company-reports-strong-second-quarter-res/) | Feb–Apr 2026 | **Residential net sales +4.4%**, driven by price and **higher zero-turn mower shipments**; Residential **EBIT +88.2%, margin 9.8% vs 5.4%**. Consolidated gross margin 33.9% vs 33.1%. "Strong demand across its portfolio", double-digit adj. EPS growth. **Toro's FQ3 (May–Jul 2026) has NOT been reported** — it typically reports in early September, i.e. after Deere. |
| Toro Q1 FY2026 — [businesswire, 5 Mar 2026](https://www.businesswire.com/news/home/20260305236875/en/The-Toro-Company-Reports-Fiscal-2026-First-Quarter-Results-and-Raises-Full-Year-Guidance) | Nov 25–Jan 26 | Professional +7.2%; **raised full-year guidance**. |
| **Home Depot** Q1 FY2026, 19 May 2026 — [ir.homedepot.com](https://ir.homedepot.com/news-releases/2026/05-19-2026-110111934) | Feb–Apr 2026 | Sales $41.8B **+4.8%**; **comps +0.6%, US comps +0.4%**; EPS $3.30 vs $3.45. FY26 guidance **reaffirmed**. Note: HD/Lowe's **Q2 FY2026 report 18–19 Aug 2026** — after this brief. Directionally: low-single-digit comps, DIY discretionary still soft. |
| **Webb Analytics / Grips Intelligence**, 15 Jul 2026 — [webb-analytics.com](https://www.webb-analytics.com/post/what-s-the-value-of-promotion-home-depot-and-lowe-s-mower-sales-show-the-impact) | H1 CY2026 | HD + Lowe's sold **≥$1.05B of mowers and related equipment in H1 2026** ($920.2M in-store, $132.1M online); three promo weeks = 21% of H1 sales. **No YoY comparison given.** |
| **AEM US Ag Tractor & Combine Report**, July 2026 — [globenewswire, 11 Aug 2026](https://www.globenewswire.com/news-release/2026/08/11/3343098/0/en/aem-united-states-ag-tractor-and-combine-report-july-2026.html) | July 2026 | Total US tractors **15,985 units, −11% YoY** (17,938 in Jul-25). **Under-40hp −12%**, 40–<100hp −8%. H1 2026 under-40hp: **58,156 vs 68,992, ≈−16%**. |

**MY INFERENCE — the AEM conflict is important and I flag it rather than smooth it.** AEM's under-40hp
category (small *ag* tractors) is down 12–16% YoY through July 2026, while Deere is guiding SA&T up
~15% and reporting internal turf/utility retail up low double digits. Three reconciling factors:
(1) **AEM counts US ag tractors only** — it excludes turf/mowing equipment, compact utility outside
the ag channel, and all of Europe, which is a large SA&T market where Deere reported tractors and
combines "up double digits" in the April rolling-3; (2) **SA&T net sales are wholesale shipments**,
and Deere underproduced retail in FY2025 by design, so FY2026 shipments rebuild to a normalised
level even on flat retail; (3) FX is a genuine +1 to +2.5pt tailwind. Even so, AEM is the one
independent series pointing the other way, and it argues for the **lower half** of my SA&T range.

---

## 5. How C&F and SA&T behaved in previous downturns relative to PPA (corpus evidence)

**REPORTED FACT — peak-to-trough, the FY2023→FY2025 cycle** (Smart Industrial segments, comparable
since FY2021):

| | Net sales FY23→FY25 | Op profit FY23→FY25 | Op margin FY23 → FY25 |
|---|---|---|---|
| PPA | 26,790 → 17,311 = **−35.4%** | 6,996 → 2,671 = **−61.8%** | 26.1% → **15.4%** |
| SA&T | 13,980 → 10,224 = **−26.9%** | 2,472 → 1,207 = **−51.2%** | 17.7% → **11.8%** |
| C&F | 14,795 → 11,382 = **−23.1%** | 2,695 → 1,028 = **−61.9%** | 18.2% → **9.0%** |

**MY INFERENCE — three patterns that matter for the Q3 forecast:**

1. **C&F falls less on the top line but just as hard on profit, and it falls a year later.** C&F net
   sales fell only 23% peak-to-trough vs PPA's 35%, yet C&F operating profit fell 62% — identical to
   PPA — because C&F has lower gross margin and less pricing power, so decremental margins are
   brutal. C&F held up through FY2024 (op profit −25% vs PPA −35%) then collapsed in FY2025 (−49%,
   with Q1 FY25 at −89% and a 3.3% margin). **C&F is a late-cycle laggard on the way down, which is
   exactly why it is a late-cycle leader on the way back up now.**

2. **SA&T is the shallowest cyclical of the three on both lines** (−27% sales, −51% profit), because
   dairy/livestock and turf are driven by consumer and protein-margin cycles, not row-crop income.
   Its worst quarter in the cycle was FY25 Q4 (op profit $25M, 1.0% margin — depressed by special
   items) and FY25 Q1 (7.1%).

3. **FY2026 is the first year in the entire corpus where the three segments have visibly decoupled.**
   In the 2015–16 downturn and again in 2020 they moved together — e.g. Q3 FY2016 construction &
   forestry net sales $1,157M (−24% YoY) with op profit $54M (−58%)
   (`filings/2016-08-19__de-us-20160819-q3-8k__784652.md`), and Q3 FY2020 C&F $2,187M (−28%) with op
   profit $205M (−46%) (`filings/2020-08-20__de-us-20200820-q3-8k__105830.md`) — both alongside a
   simultaneous ag decline. In FY2026, PPA sales are guided **down 5–10%** while C&F is **up ~20%**
   and SA&T **up ~15%**. Management frames it explicitly (Q2 call, line 65). Practically, this means
   **the historic rule of thumb "C&F tracks PPA with a lag" should NOT be applied to Q3 FY2026.**

**Consequence for segment mix.** In Q3 FY2025, C&F + SA&T were 59% of equipment net sales
($6,084M of $10,357M) and 55% of equipment operating profit ($722M of $1,302M). On my estimates
below they are ~64% of sales and ~70% of equipment operating profit in Q3 FY2026. **PPA is no longer
the swing factor for the total-company line; C&F and SA&T now are.**

---

## 6. My Q3 FY2026 estimates for C&F and SA&T

All figures below are **ESTIMATE / MY INFERENCE**, built from the guidance arithmetic in §2, the
historical Q3-share-of-H2 seasonality below, and the demand evidence in §3–4.

**Q3 as % of H2 net sales (REPORTED FACT, computed from the table in §1):**

| | FY22 | FY23 | FY24 | FY25 | mean |
|---|---|---|---|---|---|
| C&F | 49.2% | 50.0% | 54.8% | 47.5% | **50.4%** |
| SA&T | 50.6% | 54.7% | 57.0% | 55.2% | **54.4%** |

Management said C&F Q4 will be "a little bit stronger" than Q3 → I use **48.5%** for C&F.
Management said SA&T steps down in Q3 then again in Q4 → I use **55%** for SA&T.

### Construction & Forestry — Q3 FY2026

| Line | Low | **Base** | High |
|---|---|---|---|
| Net sales, $M | 3,400 | **3,525** | 3,700 |
| YoY vs $3,059M | +11% | **+15%** | +21% |
| Operating margin | 9.7% | **11.1%** | 12.7% |
| **Operating profit, $M** | **330** | **390** | **470** |
| YoY vs $237M | +39% | **+65%** | +98% |

*Derivation:* FY guide $13,658M − H1 $6,460M = H2 $7,198M; × 48.5% = **$3,491M**, rounded up to
$3,525M for the demonstrated beat pattern (Deere beat its own C&F plan in both Q1 and Q2) and the
Cat NA +50% read-across. Op profit: FY margin midpoint 11% → FY OP ~$1,502M − H1 $698M = H2 $804M;
Q3 at ~48% of H2 (Q4 stronger) = **$386M**. Sanity check against the clean Q2 underlying margin of
**11.2%** ex-refund — consistent. Upside comes from H2 price-cost (lapping FY25 tariffs and FY25 C&F
discounting); downside from the absent $136M refund and from warranty (Q2 carried an **$82M**
warranty drag in the C&F waterfall, per the Q2 slide deck).

**Skew: to the upside.** The C&F FY guide has been raised twice (up ~10% → ~15% → ~20%) and the
order book is up >60% since November with >80% of slots filled. A third raise at the Q3 print is
more likely than not.

### Small Ag & Turf — Q3 FY2026

| Line | Low | **Base** | High |
|---|---|---|---|
| Net sales, $M | 3,225 | **3,375** | 3,525 |
| YoY vs $3,025M | +7% | **+12%** | +17% |
| Operating margin | 13.6% | **15.3%** | 16.6% |
| **Operating profit, $M** | **440** | **515** | **585** |
| YoY vs $485M | −9% | **+6%** | +21% |

*Derivation:* FY guide $11,758M − H1 $5,653M = H2 $6,105M; × 55% = **$3,358M**. Op profit: FY margin
midpoint 14.25% → FY OP ~$1,676M − H1 $916M = H2 $760M; Q3 at ~68% of H2 (Q4 is seasonally the
weakest SA&T margin quarter: 10.1% in FY24 Q4, 1.0% in FY25 Q4) = **$517M**. Note the YoY margin
*compression* from 16.0% to ~15.3% despite +12% sales — SA&T carries ~⅓ of the $1.2B tariff run-rate
(~$100M/qtr) and gets no refund in Q3.

**Skew: mildly to the downside**, on the AEM under-40hp series (−12% in July) and soft US DIY
discretionary at HD/Lowe's.

### Roll-up context for the total-company target (for the modelling agent)

| Line, $M | Q3 FY25 actual | Q3 FY26 estimate | Basis |
|---|---|---|---|
| PPA net sales | 4,273 | ~3,850 | H2 implied $8,347M mid × ~46% (Q4-weighted Waterloo shipments) |
| SA&T net sales | 3,025 | **~3,375** | §6 |
| C&F net sales | 3,059 | **~3,525** | §6 |
| Equipment net sales | 10,357 | **~10,750** | sum |
| Financial Services revenues | 1,418 | ~1,400 | Q2 FY26 ran −1% YoY ($1,366M) |
| Other revenues | 243 | ~250 | Q2 FY26 $225M, +9% YoY |
| **Total net sales & revenues** | **12,018** | **~12,400** (range 12,150–12,750) | **+3.2% YoY** |

Cross-check: **Zacks consensus for the quarter is $10.83B**, which equals Q3 FY25 *equipment* net
sales of $10,357M × 1.046 — i.e. the sell-side is at ~$10.83B equipment / ~$12.48B total. My bottom-up
$10.75B equipment is ~1% below that ([Barchart/Yahoo preview](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html)).

**EPS bridge (illustrative, not my segment's remit):** PPA ~$495M + SA&T ~$515M + C&F ~$390M +
FS ~$250M = total operating profit ~$1,650M; + reconciling items ~$60M; × (1 − 23% effective rate,
the Q2 FY26 realised rate) ≈ **net income ~$1.32B → diluted EPS ~$4.87** on ~270.5M shares.
Consensus is **$4.85** vs $4.75 a year ago. Note this sits **above** the midpoint of the FY guide:
FY $4.5–5.0B less H1 $2.429B leaves H2 of $2.07–2.57B, and $1.32B in Q3 implies the **top** of the
range. That is defensible given Deere beat its own internal plan in both Q1 and Q2, but it is the
single most aggressive assumption in the chain.

---

## 7. Risks specific to these two segments

1. **The $272M refund does not repeat.** ~$136M of C&F's Q2 profit and ~$82M of SA&T's were one-time.
   Anyone anchoring on Q2's 14.8% C&F margin will be ~350bp too high.
2. **Warranty.** C&F's Q2 waterfall carried an **$82M** warranty drag (Q2 slide deck) — the largest
   single negative bar in the segment. If that repeats it is ~230bp of C&F margin.
3. **Put-in-place spending is contracting** (−3.2% YoY total, −7.9% private nonres ex-data-centres).
   The equipment cycle is currently decoupled from it via restock and rental replenishment; that
   decoupling has a finite life.
4. **Global forestry was cut to down ~5%** at Q2 (from flat) on weak residential and low log/lumber
   prices. Lumber is flat YoY only because of curtailments. Forestry is the one clearly negative
   sub-market inside C&F.
5. **Roadbuilding is the fastest-growing sub-market (guide up ~10%)** but IIJA authorities expire
   30 Sep 2026 — no Q3 impact, material FY2027 risk. Astec's backlog +58% is the corroborating bull
   datapoint; its guidance cut on delivery timing is the bear one.
6. **AEM under-40hp US tractor retail is −12% in July 2026** — the only independent series that
   contradicts the SA&T guide.
7. **Competitive price in C&F.** Q1 FY26 C&F price realisation was *negative* ~0.5pt and Deere cut
   its full-year C&F price guide by 0.5pt, citing competitors sitting on field inventory
   (`call-pres__605076.md`, line 47). Q2 recovered to >+2.5pt, but the FY guide of +2.5pt now
   requires H2 price to hold.

## 8. What I could not find

- **Any FY2026 Q3 actuals for Deere.** None exist. Confirmed by absence in the corpus (latest filing
  `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md`, 28 May 2026) and by the 20 Aug 2026
  earnings-date announcement.
- **July 2026 US housing starts** — releases 18 Aug 2026, two days after this brief.
- **Home Depot / Lowe's Q2 FY2026** — report 18–19 Aug 2026.
- **Toro FQ3 2026 (May–Jul)** — reports early September 2026.
- **Caterpillar's Q3 2026 or full-year outlook commentary** — the 4 Aug 2026 release I retrieved
  contained no forward guidance, backlog figure, or residential/data-centre split for CI.
- **AEM turf / compact-utility-tractor retail specifically** — AEM's monthly Flash Report covers ag
  tractors and combines only; no turf series was located.
- **Deere C&F retail settlement data for May–July 2026** — the latest Deere-published retail figures
  in the corpus are the rolling-3-months-to-April 2026 appendix in the Q2 slide deck.
