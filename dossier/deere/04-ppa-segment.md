# Deere & Company — Production & Precision Agriculture (PPA) segment deep-dive

**Prepared:** 16 August 2026 · **Purpose:** convert a PPA net-sales forecast into a PPA operating-profit forecast for FY2026 Q3 (quarter ending ~2 Aug 2026, reporting 20 Aug 2026).

**Corpus root** (all relative paths below are relative to this):
`/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`

> **No FY2026 Q3 actuals exist.** I found none, and I did not construct any. The corpus `INDEX.md` row
> "2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call Transcript" →
> `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` is **mislabelled**. Its content is the
> analyst Q&A of the **Q2 FY2026** call (21 May 2026): it discusses Q2 results, the $272m IEEPA refund, and
> forward cadence "for 3Q and 4Q". It is legitimate Q2-dated evidence and I cite it as such, never as Q3 actuals.

---

## 1. What PPA is

**Definition (REPORTED FACT).** From the FY2025 Form 10-K (`filings/2025-12-18__de-us-20251218-fy-10k__393777.md`):

> "PPA segment defines, develops, and delivers global equipment and technology solutions to unlock customer value for production-scale growers of large grains, small grains, cotton, and sugarcane."

**Products in the segment** (same 10-K):

| Category | Products |
|---|---|
| Tractors | Four-wheel-drive (4WD), track, and row-crop tractors (8R/8RX, 9R series; Waterloo, Iowa is the large-tractor plant) |
| Harvest | Combines/harvesters, corn heads and harvesting front-end equipment, cotton pickers and strippers, sugarcane harvesters and loaders |
| Crop care | Tillage, seeding/planting, application (sprayers), nutrient management, soil preparation |
| Aftermarket | Related attachments and service parts |
| Technology | Precision-ag stack: GNSS guidance, See & Spray, ExactShot, ExactRate, ExactDepth, FurrowVision, JDLink/JDLink Boost, John Deere Operations Center |

**Not in PPA:** compact/utility/specialty tractors, hay & forage, turf, mowers, utility vehicles (all in SAT); construction, forestry, roadbuilding (CF); the finance book (FS). Sales/marketing for PPA is organised in four regions: (1) Africa/Asia/Middle East; (2) Europe & CIS; (3) Latin & South America; (4) U.S., Canada & Australia — with the majority of sales in the U.S. and Canada (FY2025 10-K, Item 1).

**Size (REPORTED FACT).** FY2025: PPA net sales **$17,311m = 45% of equipment-operations net sales** (FY2025 10-K). SAT $10,224m (26%), CF $11,382m (29%).

**Definition of segment operating profit (REPORTED FACT).** Per the Q2 FY2026 release footnote (`filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`): *"income from continuing operations before corporate expenses, certain external interest expenses, certain foreign exchange gains and losses, and income taxes."* Because of integrated manufacturing and shared marketing/admin, **a substantial number of allocations** are required to produce segment data (FY2025 10-K, segment note) — this is why segment profit is noisier than consolidated profit.

**Fiscal-calendar note (REPORTED FACT, important).** FY2025 contained **53 weeks; the extra week sat in Q4 FY2025** (FY end 2 Nov 2025 vs 27 Oct 2024). Q1–Q3 of FY2025 and FY2026 are each 13 weeks, so **Q3 FY2026 vs Q3 FY2025 is a clean 13-vs-13-week comparison**; Q4 FY2026 (13w) faces a 14-week Q4 FY2025 comp.

---

## 2. PPA quarterly history: net sales, operating profit, operating margin

Source for every row: the quarter's earnings release (Exhibit 99.x to the 8-K) in `filings/`. FY2020 figures are the prior-year columns of the FY2021 releases (segment structure was created in FY2020 and prior periods restated). **All REPORTED FACT.**

| Fiscal Qtr | Net sales ($m) | Op profit ($m) | Op margin | YoY Δsales | YoY Δprofit | Δprofit ÷ Δsales | Source file (`filings/`) |
|---|---:|---:|---:|---:|---:|---:|---|
| Q1 FY20 | 2,507 | 218 | 8.7% | | | | 2021-02-19…q1-8k__105842 (PY col) |
| Q2 FY20 | 3,365 | 568 | 16.9% | | | | 2021-05-21…q2-8k__105846 (PY col) |
| Q3 FY20 | 3,289 | 605 | 18.4% | | | | 2021-08-20…q3-8k__105827 (PY col) |
| Q4 FY20 | 3,801 | 578 | 15.2% | | | | 2021-11-24…q4-8k__105843 (PY col) |
| Q1 FY21 | 3,069 | 643 | 21.0% | +562 | +425 | 75.6% | 2021-02-19…q1-8k__105842 |
| Q2 FY21 | 4,529 | 1,007 | 22.2% | +1,164 | +439 | 37.7% | 2021-05-21…q2-8k__105846 |
| Q3 FY21 | 4,250 | 906 | 21.3% | +961 | +301 | 31.3% | 2021-08-20…q3-8k__105827 |
| Q4 FY21 | 4,661 | 777 | 16.7% | +860 | +199 | 23.1% | 2021-11-24…q4-8k__105843 |
| Q1 FY22 | 3,356 | 296 | 8.8% | +287 | −347 | n.m. (UAW bonus) | 2022-02-18…q1-8k__105812 |
| Q2 FY22 | 5,117 | 1,057 | 20.7% | +588 | +50 | 8.5% | 2022-05-20…q2-8k__105815 |
| Q3 FY22 | 6,096 | 1,293 | 21.2% | +1,846 | +387 | 21.0% | 2022-08-19…q3-8k__105811 |
| Q4 FY22 | 7,434 | 1,740 | 23.4% | +2,773 | +963 | 34.7% | 2022-11-23…q4-8k__105825 |
| Q1 FY23 | 5,198 | 1,208 | 23.2% | +1,842 | +912 | 49.5% | 2023-02-17…q1-8k__105833 |
| Q2 FY23 | 7,822 | 2,170 | 27.7% | +2,705 | +1,113 | 41.1% | 2023-05-19…q2-8k__105839 |
| Q3 FY23 | 6,806 | 1,782 | 26.2% | +710 | +489 | 68.9% | 2023-08-18…q3-8k__105829 |
| Q4 FY23 | 6,965 | 1,836 | 26.4% | −469 | +96 | n.m. | 2023-11-22…q4-8k__105823 |
| Q1 FY24 | 4,849 | 1,045 | 21.6% | −349 | −163 | 46.7% | 2024-02-15…q1-8k__105824 |
| Q2 FY24 | 6,581 | 1,650 | 25.1% | −1,241 | −520 | 41.9% | 2024-05-16…q2-8k__105819 |
| Q3 FY24 | 5,099 | 1,162 | 22.8% | −1,707 | −620 | 36.3% | 2024-08-15…q3-8k__105836 |
| Q4 FY24 | 4,305 | 657 | 15.3% | −2,660 | −1,179 | 44.3% | 2024-11-21…q4-8k__105840 |
| Q1 FY25 | 3,067 | 338 | 11.0% | −1,782 | −707 | 39.7% | 2025-02-13…q1-8k__105841 |
| Q2 FY25 | 5,230 | 1,148 | 22.0% | −1,351 | −502 | 37.2% | 2025-05-15…q2-8k__105808 |
| Q3 FY25 | 4,273 | 580 | 13.6% | −826 | −582 | 70.5% | 2025-08-15…q3-8k__143410 |
| Q4 FY25 * | 4,740 | 604 | 12.7% | +435 | −53 | n.m. | 2025-11-26…q4-8k__361233 |
| Q1 FY26 | 3,163 | 139 | 4.4% | +96 | −199 | n.m. | 2026-02-19…q1-8k__603009 |
| **Q2 FY26** | **4,503** | **706** | **15.7%** | −727 | −442 | 60.8% | 2026-05-21…q2-8k-2__1042168 |
| Q3 FY26 | **not reported** | **not reported** | — | | | | reports 20 Aug 2026 |

\* Q4 FY2025 contains a 14th week.

### Fiscal-year totals (derived by summing the quarters above; cross-checked to company disclosure)

| FY | Net sales ($m) | Op profit ($m) | Op margin | Cross-check |
|---|---:|---:|---:|---|
| FY2020 | 12,962 | 1,969 | 15.2% | derived |
| FY2021 | 16,509 | 3,333 | 20.2% | derived |
| FY2022 | 22,003 | 4,386 | 19.9% | derived |
| FY2023 | 26,791 | 6,996 | 26.1% | co. states $26,790 sales / 26.1% margin (`slides/2024-08-15…46457`) |
| FY2024 | 20,834 | 4,514 | 21.7% | co. states $20,834 (`slides/2025-08-15…143404`); $4,514 op profit (`filings/2025-11-26…q4-8k__361233`) |
| FY2025 | 17,310 | 2,670 | 15.4% | co. states $17,311 / 15.4% (`slides/2026-05-21…1042212`); $2,671 op profit (`filings/2025-11-26…q4-8k__361233`) |
| FY2026 H1 | 7,666 | 845 | 11.0% | `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` |

Rounding differences of $1m come from company rounding, not from an error here.

---

## 3. The drivers management uses — and the actual bridge numbers

Deere publishes an eight-bucket PPA operating-profit waterfall each quarter in the earnings deck:
**Volume/Mix · Price · Currency · Warranty · Production Costs · SA&G/R&D · Special Items · Other.**
The 10-Q adds: *"The tariff impact was primarily included in the 'Production Costs' category"* (`filings/2026-05-28…q2-10q__1055932.md`).

Below are the bridges I could extract **and arithmetically verify** (each row sums exactly from the prior-year to the current-year profit). Source: the quarter's deck in `slides/`. **REPORTED FACT.**

| Bridge (YoY) | Start | Vol/Mix | Price | Currency | Warranty | Prod. costs | SA&G/R&D | Special | Other | End |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Q3'21→Q3'22 | 906 | +492 | +646 | −47 | −2 | −535 | −140 | +1 | −28 | 1,293 |
| Q3'22→Q3'23 | 1,293 | +27 | +723 | −41 | +4 | −77 | −74 | −1 | −72 | 1,782 |
| Q4'22→Q4'23 | 1,740 | −622 | +729 | −14 | +18 | +40 | −58 | +70 | −67 | 1,836 |
| Q1'23→Q1'24 | 1,208 | −273 | +202 | −1 | −20 | +15 | −89 | 0 | +3 | 1,045 |
| Q3'23→Q3'24 | 1,782 | −847 | +177 | +24 | +48 | −5 | +10 | −62 | +35 | 1,162 |
| Q4'23→Q4'24 | 1,836 | −1,204 | +2 | −60 | −70 | +105 | +7 | +2 | +39 | 657 |
| Q1'24→Q1'25 | 1,045 | −896 | +52 | +13 | −32 | +62 | +81 | 0 | +13 | 338 |
| Q2'24→Q2'25 | 1,650 | −610 | +46 | −92 | +32 | +73 | −8 | 0 | +57 | 1,148 |
| **Q3'24→Q3'25** | 1,162 | −494 | −40 | −52 | −45 | +69 | −17 | +34 | −37 | **580** |
| Q4'24→Q4'25 | 657 | +69 | +122 | −12 | +23 | −147 | −43 | −49 | −16 | 604 |
| Q1'25→Q1'26 | 338 | −61 | −4 | −39 | −48 | −74 | +6 | +21 | 0 | 139 |
| **Q2'25→Q2'26** | 1,148 | −402 | +49 | +75 | −51 | −77 | −4 | 0 | −32 | **706** |

Deck sources in order: `slides/2022-08-19…46460`, `2023-08-18…46427`, `2023-11-22…46466`, `2024-02-15…46430`, `2024-08-15…46457`, `2024-11-21…46477`, `2025-02-13…46456`, `2025-05-15…46462`, `2025-08-15…143404`, `2025-11-26…361243`, `2026-02-19…603088`, `2026-05-21…1042212`.
(Bucket labels in a few OCR'd decks are shifted by one position; I assigned them to Deere's fixed eight-bucket order and verified each row's arithmetic and its consistency with the release narrative. Where I could not make a row sum exactly — Q1 FY23, Q2 FY23, Q2 FY24, Q4 FY22 — I have **omitted** it rather than guess. INFERENCE flag on the labels; the values are reported.)

### What the bridges say about each driver

1. **Volume/Mix is the whole story in a downturn.** In the eight declining quarters FY2024–Q2 FY2026, Volume/Mix accounts for a median ~90% of the total YoY profit change. Everything else nets to small.
2. **Price is nearly pure margin.** Price bridge $ ≈ price-realisation % × prior-year sales, dropping through ~1-for-1. Q2 FY26: +1% on $5,230m = $52m expected vs **+$49m** actual. FY2026 PPA price guide is **~+1.0%** for the year, cut ~0.5pt at Q2 "primarily reflecting slightly lower expectations for overseas markets" (`call-transcripts/2026-05-21…call-pres__1042774.md`).
3. **Currency is two-sided and unreliable.** +3% translation on PPA sales in both Q1 and Q2 FY26, yet the *profit* effect was **−$39m in Q1** and **+$75m in Q2** — translation gain net of transaction losses and hedges. Do not assume translation tailwind ⇒ profit tailwind.
4. **Production costs = tariffs + material/freight.** FY2025 direct tariffs ≈ **$600m** enterprise, "beginning in the third quarter of 2025" (FY2025 10-K; Q1 FY26 10-Q). Q1 FY26 alone was **$361m**; H1 FY26 **$644m gross / $372m net** of the IEEPA recovery (Q2 FY26 10-Q). FY2026 direct exposure **~$1.2bn gross (~3pt enterprise margin headwind), ~$900m net of refunds** (Q2 FY26 call).
5. **Warranty is a live, recurring PPA headwind:** −$48m (Q1 FY26), −$51m (Q2 FY26), −$45m (Q3 FY25).
6. **SA&G/R&D is small at segment level** (−$4m to +$81m); enterprise R&D is still rising (+6% YoY in Q2 FY26) but Deere protects it "through the cycle".
7. **Special items** are episodic: UAW ratification bonus (Q1 FY22, $53m of the $90m hit PPA — `filings/2023-02-17…q1-8k__105833`), Russia reserves (FY22), employee-separation programmes (Q3 FY24, −$62m).

### The IEEPA tariff refund — critical, and PPA got the small slice

**REPORTED FACT** (`filings/2026-05-28__de-us-20260528-q2-10q__1055932.md`): after the **20 Feb 2026 Supreme Court decision invalidating IEEPA tariffs**, Deere filed and CBP accepted a **$272m** refund claim, recognised in Q2 FY2026 as a reduction of cost of sales, **"allocated 20%, 30%, and 50% to PPA, SAT, and CF, respectively."**

⇒ **PPA's share = ~$54m.** So PPA's Q2 FY26 Production Costs bucket of **−$77m** is **≈ −$131m excluding the refund**. **This does not repeat in Q3.** (INFERENCE: the same 20% key is a reasonable proxy for PPA's share of ongoing tariff *cost*, and it back-tests well — Q1 FY26 enterprise tariffs of $361m vs ~$45m a year earlier is a ~$316m YoY step-up; 20% = ~$63m, against a PPA Production Costs bucket of −$74m.)

---

## 4. The sales→profit conversion (the core deliverable)

### 4a. Levels regression: PPA operating profit on PPA net sales

Ordinary least squares on the quarterly table in §2. **This is my calculation (INFERENCE), from reported inputs.**

| Sample | n | Fitted relationship | R² | Resid. SE | Implied contribution margin | Implied quarterly fixed cost | Break-even sales |
|---|---:|---|---:|---:|---:|---:|---:|
| FY2020–Q2 FY26 (all) | 26 | OP = **0.358 × Sales − 756** | 0.921 | $155m | 35.8% | $756m | $2,115m |
| FY2022–Q2 FY26 | 18 | OP = **0.404 × Sales − 1,043** | 0.955 | $129m | 40.4% | $1,043m | $2,583m |
| FY2024–Q2 FY26 (downcycle) | 10 | OP = **0.421 × Sales − 1,125** | 0.911 | $142m | 42.1% | $1,125m | $2,673m |
| FY2025–Q2 FY26 (tariff era) | 6 | OP = **0.360 × Sales − 914** | 0.833 | $157m | 36.0% | $914m | $2,536m |

**Read:** PPA behaves like a business with a **~36–42% contribution margin** and **~$0.9–1.1bn of quarterly fixed/period cost**. The relationship is remarkably tight (R² 0.83–0.96) across a peak-to-trough range of $2.5bn–$7.8bn quarterly sales. Fixed cost has ratcheted up ~$300–400m/quarter since FY2020 (R&D, technology, tariffs, inflation), which is why the FY2026 margin at ~$4bn of quarterly sales is far below FY2020's margin at ~$3.5bn.

Fit quality on the last six quarters (FY2025–Q2 FY26 model): Q1'25 +147, Q2'25 +178, Q3'25 −46, Q4'25 −190, Q1'26 −87, Q2'26 −2. **Mean residual over the last four quarters is −$81m** — the model has been running hot in the tariff era.

### 4b. Delta ("incremental / decremental margin") regression

ΔOP regressed on ΔSales, both YoY:

| Sample | n | Fitted relationship | R² | SE |
|---|---:|---|---:|---:|
| FY2024–FY2025 (8 qtrs, pre-tariff-step) | 8 | ΔOP = **0.344 × ΔSales − 133** | 0.904 | $115m |
| FY2024–Q2 FY2026 (10 qtrs) | 10 | ΔOP = **0.328 × ΔSales − 165** | 0.905 | $105m |

**Read:** the **decremental margin on a sales change is ~33–34%**, plus a **structural YoY drag of $130–165m per quarter** that is independent of sales (tariffs + material/freight + warranty + R&D creep). The bigger negative intercept in the 10-quarter sample is driven by Q1/Q2 FY2026, the two quarters that absorbed the tariff step-up. **Q3 FY2026 has a much easier tariff comparison than Q1/Q2 FY2026 did, because tariffs first hit in Q3 FY2025** — so the −165 intercept overstates the Q3 FY26 drag; the −133 version is more appropriate.

### 4c. Volume/Mix decremental (the cleanest structural number)

Strip currency translation and price out of the sales change, then divide the Volume/Mix bridge bucket by the residual volume-driven sales change. **INFERENCE** (uses reported bridge $ and reported price/currency percentages):

| Quarter | Δsales | less currency | less price | ⇒ volume-driven Δsales | Vol/Mix bridge $ | Decremental |
|---|---:|---:|---:|---:|---:|---:|
| Q3 FY24 | −1,707 | ~0 | +102 | −1,809 | −847 | 46.8% |
| Q4 FY24 | −2,660 | −35 | +70 | −2,695 | −1,204 | 44.7% |
| Q1 FY25 | −1,782 | −121 | +48 | −1,709 | −896 | 52.4% |
| Q2 FY25 | −1,351 | −99 | +66 | −1,318 | −610 | 46.3% |
| Q3 FY25 | −826 | −76 | −40 | −710 | −494 | 69.6% (mix-heavy) |
| Q2 FY26 | −727 | +157 | +52 | −936 | −402 | 42.9% |

**Median ≈ 47%, mean ≈ 50%.** Use **45–50% as the volume/mix decremental** on a *volume-driven* change in PPA sales. Q3 FY25's 70% is the warning case: a quarter where the *mix* deteriorated (fewer high-horsepower Waterloo tractors and combines, more parts/small machines) converts far worse than the headline decremental.

### 4d. Recommended conversion recipe

```
PPA_OpProfit(Q) = PPA_OpProfit(Q-4)
                + 0.47 × [ ΔSales − currency_translation_$ − price_realisation_$ ]   # volume/mix
                + price_realisation_$                                                # ~100% flow-through
                + currency_profit_effect                                             # ±, NOT = translation_$
                + warranty_Δ                                                         # −40 to −50 recently
                + production_cost_Δ                                                  # tariffs + material/freight
                + SA&G/R&D_Δ + special_items + other
```
Cross-check against **OP = 0.42 × Sales − 1,125** (levels) and **ΔOP = 0.344 × ΔSales − 133** (delta). Where the three disagree, the levels model tends to be the optimistic bound and the delta model the pessimistic bound.

---

## 5. FY2026 guidance and what it implies for Q3

**REPORTED FACT — FY2026 PPA guidance, reaffirmed at Q2 on 21 May 2026** (`filings/2026-05-21…q2-8k__1042167.md`; `slides/2026-05-21…1042212.md`; `call-transcripts/2026-05-21…call-pres__1042774.md`):

| Item | FY2026 guide |
|---|---|
| PPA net sales | **Down 5% to 10%** (unchanged since Q1) |
| — currency translation | **+3.0%** ("just under 3 points") |
| — price realisation | **~+1.0%** (cut ~0.5pt at Q2) |
| PPA operating margin | **11% to 13%** (unchanged) |
| U.S. & Canada Large Ag industry | **Down 15–20%** |
| South America tractors & combines | **Down ~15%** (cut from down ~5% at Q1) |
| Europe | Flat to up 5% · Asia: Flat |
| Enterprise net income | $4.5bn–$5.0bn |

**Guidance arithmetic (INFERENCE, my calculation):**

| | Low end | Mid | High end |
|---|---:|---:|---:|
| FY26 PPA net sales (vs FY25 $17,311m) | 15,580 (−10%) | 16,013 (−7.5%) | 16,445 (−5%) |
| FY26 PPA op profit (at 11% / 12% / 13%) | 1,714 | 1,922 | 2,138 |
| less H1 FY26 actual sales / profit | 7,666 / 845 | 7,666 / 845 | 7,666 / 845 |
| **⇒ H2 FY26 implied sales** | **7,914** | **8,347** | **8,779** |
| **⇒ H2 FY26 implied op profit** | **869** | **1,077** | **1,293** |
| H2 implied margin | 11.0% | 12.9% | 14.7% |

### The Q3/Q4 split — management gave unusually explicit direction

**REPORTED FACT**, all from the 21 May 2026 call:

- *"we would expect slightly higher revenue in the back half, with the fourth quarter being higher than the third quarter. In addition, we would expect to see our most favorable cost comparisons in the fourth quarter as well."* (`call-transcripts/2026-05-21…call-pres__1042774.md`)
- *"As you look at Large Ag … **Q4 a bit stronger than Q3**. … We've got **more Waterloo large tractor shipments shipping to North America in the back half than the front half** of the year. That's **abnormal** for us, but reflected how the order book built for the course of the year."* (`call-transcripts/2026-05-21…call-qna__1042775.md` — the mislabelled "Q3 2026" file)
- *"particularly for our large ag factories … **a little bit better absorption in the fourth quarter as production rates are significantly higher**."* (same file)
- *"Regarding Waterloo large tractors, **order books are well into the fourth quarter** as we look to close out our model year 2026 production."* (`call-transcripts/2026-05-21…call-pres__1042774.md`)
- Europe/Brazil: *"Order visibility in both regions now extends through the third quarter and into the fourth."* Brazil: *"we expect to underproduce retail demand, most notably in combines."*

**Historical Q3 share of H2 (REPORTED FACT, derived):**

| FY | Q3 share of H2 sales | Q3 share of H2 op profit | Q3 margin vs FY margin |
|---|---:|---:|---:|
| FY2020 | 46.4% | 51.1% | +3.2pp |
| FY2021 | 47.7% | 53.8% | +1.1pp |
| FY2022 | 45.1% | 42.6% | +1.3pp |
| FY2023 | 49.4% | 49.3% | +0.1pp |
| FY2024 | 54.2% | 63.9% | +1.1pp |
| FY2025 | 47.4% | 49.0% | −1.9pp |
| **Median** | **47.6%** | **50.1%** | **+1.1pp** |

Because FY2026 is explicitly **back-half-of-the-back-half weighted** (Waterloo shipments and better Q4 absorption), Q3's share should sit **below** the historical median: I use **44–47% of H2 sales** and **40–48% of H2 operating profit**.

---

## 6. Putting it together — Q3 FY2026 PPA estimate

### Net sales

| Method | Q3 FY26 PPA net sales |
|---|---:|
| FY guide (−5% to −10%) applied directly to Q3 FY25 $4,273m | 3,846 – 4,059 |
| 44–47% of guidance-implied H2 sales ($7,914–$8,779m) | 3,482 – 4,126 |
| **Central estimate (ESTIMATE)** | **~$3,900m (−8.7% YoY); range $3,700–$4,150m** |

### Operating profit — every method, at $3,900m of sales

| Method | Q3 FY26 PPA op profit | Implied margin |
|---|---:|---:|
| Levels: OP = 0.421×S − 1,125 (FY24–Q2'26) | 517 | 13.3% |
| Levels: OP = 0.404×S − 1,043 (FY22–Q2'26) | 533 | 13.7% |
| Levels: OP = 0.360×S − 914 (FY25–Q2'26, tariff era) | 490 | 12.6% |
| ... tariff-era levels less mean recent residual (−81) | 409 | 10.5% |
| Delta: ΔOP = 0.344×ΔSales − 133 (FY24–FY25) | 319 | 8.2% |
| Delta: ΔOP = 0.328×ΔSales − 165 (FY24–Q2'26) | 293 | 7.5% |
| Bottom-up eight-bucket bridge (below) | 330 – 430 | 8.5–11.0% |
| Guidance top-down: 40–48% of H2 OP $869–$1,293m | 365 – 620 (mid ~480) | 9.4–15.9% |
| FY guide midpoint margin 12% ± 1pt seasonal | 429 – 507 | 11.0–13.0% |
| **Blended central (ESTIMATE)** | **~$430–470m; point $450m** | **~11.5%** |
| **80% range (ESTIMATE)** | **$330 – $580m** | **8.5–14.5%** |

**Bottom-up bridge from Q3 FY25's $580m (INFERENCE, my construction):**

| Bucket | $m | Reasoning |
|---|---:|---|
| Q3 FY2025 actual | 580 | reported |
| Volume/Mix | −256 | Δsales −373; less currency +3% (+128) and price +1% (+43) ⇒ volume-driven −544; × 47% decremental |
| Price | +43 | +1.0% guided on $4,273m prior-year base |
| Currency | +30 | mid-point of Q1 FY26 (−39) and Q2 FY26 (+75) |
| Warranty | −15 | recurring headwind, but Q3 FY25 base already carried −45 |
| Production costs | −55 | PPA ~20% of an ~$78m enterprise YoY tariff step (Q3 FY26 ~$278m vs Q3 FY25 ~$200m) ≈ −$16m, plus material/freight |
| SA&G/R&D · Special · Other | +10 | Q3 FY25 carried −$37m "Other"; assume partial non-repeat |
| **⇒ Q3 FY2026** | **~337** | 8.6% margin |

**The tension is real and the model team should see it.** The bottom-up bridge and the delta regression both land at **$290–$430m**; the levels regression and the reaffirmed FY guidance both point to **$450–$550m**. The reconciling variable is Q4: if Q3 comes in near $350m, FY2026 PPA margin lands at the **bottom** of the 11–13% guide (≈11.1%); reaching the 12% midpoint requires a Q4 PPA margin of ~15.6%, the strongest since Q2 FY2025. Deere reaffirmed the range on 21 May with H1 already booked, which argues against the very bottom. **I weight the guidance and levels methods ~60/40 against the delta methods, giving $450m.**

**Sanity note on tariff timing (the single best reason Q3 FY26 should be better YoY than Q1/Q2 FY26 were):** tariffs first hit in Q3 FY2025 and were ~$600m across FY2025 with almost none in H1. So the brutal YoY tariff step-up that crushed Q1 FY26 (−$316m enterprise) largely annualises out from Q3 FY26 onward. Q4 FY26 should actually see a *favourable* YoY tariff comparison — exactly what management means by "most favorable cost comparisons in the fourth quarter".

---

## 7. Precision-ag technology adoption, SaaS, and engaged acres

**Engaged Acres in John Deere Operations Center (REPORTED FACT, company-stated):**

| As of | Engaged acres | YoY | Highly engaged | Source |
|---|---:|---|---|---|
| Q4 FY2024 (Nov 2024) | 455m | +~20% (S. America +~30%) | >25% of total; +>30% YoY | `call-transcripts/2024-11-21…call-q4-pres__46452.md` |
| Q2 FY2025 (May 2025) | just over 475m | +~15% | +>25% YoY; ~30% of total | `call-transcripts/2025-05-15…call-pres__46417.md` |
| Q3 FY2025 (Aug 2025) | surpassed 485m | — | +~50% for Precision Essentials adopters | `call-transcripts/2025-08-15…call-q3-pres__143406.md` |
| Q4 FY2025 (Nov 2025) | **over 500m** | **+10%** | **147m (+17% YoY)** | `call-transcripts/2025-11-26…call-q4-pres-2__361265.md` |
| Investor Day (8 Dec 2025) | 500m — 2026 LEAP target hit a year early | — | 30% of total | `call-transcripts/2025-12-08…call-pres-2__384036.md` |
| Q1 FY2026 (Feb 2026) | 500m | +>10% | +~25%; "nearly a third" highly engaged | `call-transcripts/2026-02-19…call-qna__605077.md` |
| **Q2 FY2026 (May 2026)** | **+~10% YoY** | — | "grown at an even stronger pace" | `call-transcripts/2026-05-21…call-pres__1042774.md` |

**2030 targets (Investor Day, 8 Dec 2025):** 600m engaged acres; 50% highly engaged; **1m unique active monthly digital users** (vs ~400,000 then, **~440,000 at Q2 FY2026**); >1m connected machines already achieved; **10% net-sales CAGR FY2025→FY2030**; 20% through-cycle OROA.

**Solutions-as-a-Service (SaaS) — REPORTED FACT and a downgrade worth noting:**
- The original LEAP ambition of **10% of revenue from recurring sources by 2030 has been pushed out beyond 2030**. Stated reasons: *"a softer ag market, the time required to build the infrastructure to support a SaaS model, and more disruptive solutions taking longer to adopt."* Deere still believes the level is attainable "in the long term." (`call-transcripts/2025-12-08…call-pres-2__384036.md`)
- FY2025 groundwork: global license-management infrastructure, utilisation programmes; a pay-only-when-it-saves-you-money model; an **unlimited annual licence for high-use operations introduced for 2026**. John Deere Financial finances **nearly half of all See & Spray licences in the U.S. to date**.
- **Practical implication:** SaaS/recurring revenue is *not yet* a material stabiliser of PPA quarterly operating profit. Do not model it as damping the Q3 decremental.

**Product/technology momentum cited in Q2 FY2026** (`call-transcripts/2026-05-21…call-pres__1042774.md`): six new 8R/8RX models at 440/490/540hp on the JD14 engine, autonomy-ready; ExactDepth and FurrowVision downforce automation; ExactShot + ExactRate; **See & Spray extended to wheat, barley and canola**, plus new **See & Scout**; **JDLink Boost >12,500 kits sold since H2 2024, +25% in the quarter alone**.

**Inventory/order position going into Q3 (REPORTED FACT, Q2 FY2026 call):** North America large-ag new inventory for high-horsepower tractors and combines **down >50% from the mid-2024 peak**, inventory-to-sales ratios in line with historical averages; used MY22–MY23 8R tractors **down ~45%** from last year's peak; used sprayers **−30%**, planters **−50%**. Europe production aligned to retail; Brazil underproducing retail, most notably combines. This is the classic setup for volume to stop falling — but it is a FY2027 story, not a Q3 FY2026 one.

---

## 8. External / non-corpus context (web, found 16 Aug 2026)

| Item | Value | Source |
|---|---|---|
| Q3 FY2026 report date | **Thursday 20 August 2026**, call 9:00 a.m. | [Nasdaq, 5 Aug 2026](https://www.nasdaq.com/press-release/deere-announce-third-quarter-2026-financial-results-2026-08-05) |
| Consensus diluted EPS, Q3 FY2026 | **$4.85** (vs $4.75 a year ago, +2.1%) | [Yahoo Finance / Barchart earnings preview](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html) |
| Segment-level (PPA) consensus | **not found** — no public PPA sales/profit consensus located | searched Yahoo, StockTitan, Simply Wall St, Quartr |

I did not find any post-corpus (June–August 2026) company announcement that changes the FY2026 PPA guidance.

---

## 9. Gaps, caveats and where I looked

- **PPA-level consensus (sales, profit, margin) not found.** Searched web for segment estimates; only enterprise EPS consensus is public.
- **Q1 FY23, Q2 FY23, Q2 FY24 and Q4 FY22 operating-profit bridges could not be reconstructed** to an exact sum from the OCR'd decks. Values omitted rather than guessed. Located in `slides/2023-02-17…46447`, `2023-05-19…46428`, `2024-05-16…46443`, `2022-11-23…46423`.
- **PPA net sales by geography (U.S./Canada vs rest) is not disclosed at segment level** in the corpus — the 10-K gives geography for the consolidated enterprise, not for PPA. This limits precision on the currency-translation estimate.
- **PPA's exact share of tariff cost is not disclosed.** I used the disclosed 20% refund-allocation key as a proxy and back-tested it against the Q1 FY26 bridge; it is an inference, not a fact.
- **Quarterly split of FY2025's $600m tariff cost is not disclosed.** I inferred ~$200m Q3 / ~$305m Q4 from "$95m in H1 FY2025" (Q2 FY26 10-Q) and "beginning in the third quarter of 2025" (Q1 FY26 10-Q). This drives the size of the Q3 FY26 production-cost comp.
- **Pre-FY2020 PPA history does not exist.** The three-segment structure was created with the Smart Industrial reorganisation; the corpus restates only back to FY2020.
- **PPA-level R&D and SA&G dollars are not separately disclosed** — only the combined SA&G/R&D bridge bucket.
