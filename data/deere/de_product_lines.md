# Deere & Company — ASC 606 major-product-line and timing-of-revenue extract

**Purpose:** bottom-up input for the FY2026 Q3 forecast (worldwide net sales and revenues; diluted GAAP EPS; PPA operating profit).
**Data file:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_product_lines.csv`
**Parser:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/parse_de_product_lines.py`
**Builder:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/build_de_product_lines.py`
**Adjunct extractor:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/extract_de_deferred_revenue.py`
**Corpus:** 310 docs, frozen 2026-08-14. Everything below comes from that corpus only.

> **FY2026 Q3 has not been reported.** Deere's Q3 FY2026 call is 09:00 US Central, Thursday 20 August 2026 — after the corpus freeze and after today (16 August 2026). No FY2026 Q3 actuals exist anywhere in this extract. The most recent actuals are the three and six months ended **3 May 2026** (Q2 FY2026), filed 2026-05-21/2026-05-28.

---

## 1. What is in the CSV

Four series, all on the **rev-rec** basis (revenue from contracts with customers, note 3 / note 4 "Revenue Recognition"):

| series_id | rows | what it is | dimensions used |
|---|---:|---|---|
| `de_revrec_product_line` | 1,245 | major-product-line revenue | `segment` (blank = all-segment total), `product_line` |
| `de_revrec_timing` | 525 | timing of revenue recognition | `segment`; the timing bucket ("At a point in time" / "Over time") is carried in the `product_line` column because the fixed header has no other free dimension |
| `de_revrec_deferred_revenue` | 31 | contract liability (invoiced, not yet recognised) at each balance-sheet date | none |
| `de_revrec_rpo_gt1yr` | 10 | remaining performance obligations on contracts with original duration > 1 year | none |

`geography` is always blank — the segment × geography matrix is a separate extract; geography rows were parsed here **only** as a cross-check and then discarded.

`fiscal_quarter` takes `Q1`–`Q4` for discrete three-month periods and `H1`, `9M`, `FY` for the cumulative periods exactly as Deere discloses them. Both are present: use the `Q*` rows for a quarterly series, the `H1/9M/FY` rows for as-reported cumulatives. Do not add them together.

### Reconciliation warning (restated)

These figures are **revenue from contracts with customers** and do **not** equal segment net sales in the 8-K. For Q2 FY2026 PPA is **4,607** here versus **4,503** in the 8-K segment table — a 104m gap. Never mix the two bases in one series. Section 6 gives the empirical bridge.

---

## 2. Method and validation

1. **A parser, not transcription.** `parse_de_product_lines.py` walks every filing, finds contiguous markdown pipe-table blocks containing a "Major product lines" row, and learns the *numeric column positions* per table from an anchor row that carries a full set of values. This matters: blank cells in the product-line block are meaningful (a product line belongs to exactly one segment), so collapsing empty cells — the obvious approach — silently mis-assigns Small agriculture into the PPA column. Zero-width spaces, non-breaking spaces, empty `$` separator cells, two-line wrapped period captions ("…Ended January 26," / "2025 | PPA | …") and wrapped row labels are all handled.
2. **Every table is validated** three ways: each row must cross-foot to its stated Total column, each column must sum down to its stated Total row, and the product-line section total must equal the timing section total column by column.
3. **91 candidate tables parsed; 76 validate clean; 15 flagged.** Every flagged table is a *rendering* defect in the corpus, not a data defect — cells merged during PDF-to-markdown conversion (e.g. `| Compact construction | … | 303 818 |`, `| Roadbuilding Forestry | … | 3,794 1,429 |`). All 15 are duplicates of periods available cleanly from another filing, so none of them is used. They are listed in section 8.
4. **45 distinct (taxonomy, period-end, duration) tables** survive. Where two filings disclose the same period (current-year table in one 10-Q, comparative in the next year's), the values were compared cell by cell: **zero conflicts**.
5. **Derived quarters** are computed only by subtraction of disclosed cumulative periods and are labelled as such in `notes`. All 26 PPA-era quarters pass the validation checks after derivation (0 failures).

---

## 3. Product-line taxonomy, and how it changed

Deere has used **nine** major product lines throughout the ASC 606 era. There has been **one substantive change and two cosmetic ones**:

| Change | First filing showing it | Detail |
|---|---|---|
| `Large Agriculture` → `Production Agriculture` | 2021-02-19 (Q1 FY2021 10-Q) | Substantive. Accompanies the Smart Industrial segment reorganisation (Agriculture & Turf / Construction & Forestry → PPA / SAT / CF). Certain mid-size tractors moved between the large-ag and small-ag definitions, so **`Large Agriculture` is not a continuation of `Production agriculture`** — do not splice the two into one series. Deere recast FY2019 and FY2020 onto the new basis. |
| `Road Building` → `Roadbuilding` | 2020-02-21 (Q1 FY2020 10-Q) | Cosmetic. |
| Title case → sentence case (`Production Agriculture` → `Production agriculture`) | 2021-05-21 (Q2 FY2021 10-Q) | Cosmetic. Normalised in the CSV to sentence case. |

Timing-section wording also changed: `Timing of revenue recognition: / Revenue recognized at a point in time / Revenue recognized over time` (2019-02-15 → 2021-08-20), then `Revenue recognized: / At a point in time / Over time` (FY2021 10-K onward). Normalised to `At a point in time` / `Over time`.

The geography axis was renamed `Asia, Africa, Australia, New Zealand, and Middle East` → `Asia, Africa, Oceania, and Middle East` from FY2023 (not carried into this CSV, but it is why a naive merge of two vintages double-counts that region).

**Negative finding that matters:** in seven and a half years of ASC 606 disclosure Deere has **never** broken out precision ag, technology, or Solutions-as-a-Service as a product line. There is no disclosed precision-ag revenue line. What exists is described in section 7.

The two catch-all lines, verbatim from the FY2024 10-K:

- **Financial products** — "finance and interest income from retail notes …; wholesale financing to dealers …; revolving charge accounts; lease income from retail leases …; and revenue from extended warranties."
- **Other** — "sales of components to other equipment manufacturers that are included in 'Net sales;' **revenue earned over time from precision guidance, telematics, and other information enabled solutions**; revenue from service performed at company owned dealerships and service centers; gains on disposition of property and businesses; trademark licensing revenue; and other miscellaneous revenue items that are included in 'Other income.'"

---

## 4. Quarterly major product lines, USDm, rev-rec basis, PPA/SAT/CF taxonomy

All-segment totals. `Src`: **A** = as disclosed in a three-month table; **D** = derived by subtraction from disclosed cumulative tables (see section 8).

| FY | Q | Period end | Src | Prod ag | Small ag | Turf | Constr | Compact | Road | Forestry | Fin prod | Other | Total |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2020 | Q1 | 2020-02-02 | D | 2,426 | 1,478 | 468 | 841 | 288 | 605 | 274 | 965 | 286 | 7,631 |
| 2020 | Q2 | 2020-05-03 | A | 3,280 | 1,771 | 806 | 877 | 339 | 723 | 254 | 902 | 301 | 9,253 |
| 2020 | Q3 | 2020-08-02 | D | 3,209 | 1,704 | 651 | 817 | 303 | 818 | 241 | 922 | 260 | 8,925 |
| 2020 | Q4 | 2020-11-01 | D | 3,747 | 1,874 | 465 | 986 | 339 | 778 | 331 | 931 | 280 | 9,731 |
| 2021 | Q1 | 2021-01-31 | D | 3,012 | 1,811 | 651 | 887 | 346 | 910 | 290 | 917 | 288 | 9,112 |
| 2021 | Q2 | 2021-05-02 | A | 4,466 | 2,417 | 898 | 1,232 | 396 | 1,066 | 343 | 919 | 321 | 12,058 |
| 2021 | Q3 | 2021-08-01 | A | 4,179 | 2,355 | 719 | 1,283 | 398 | 948 | 342 | 932 | 371 | 11,527 |
| 2021 | Q4 | 2021-10-31 | D | 4,592 | 2,036 | 585 | 1,282 | 349 | 825 | 305 | 900 | 453 | 11,327 |
| 2022 | Q1 | 2022-01-30 | A | 3,283 | 1,932 | 627 | 1,175 | 321 | 692 | 305 | 898 | 336 | 9,569 |
| 2022 | Q2 | 2022-05-01 | A | 5,032 | 2,668 | 817 | 1,516 | 427 | 1,017 | 325 | 889 | 679 | 13,370 |
| 2022 | Q3 | 2022-07-31 | A | 6,019 | 2,705 | 842 | 1,506 | 460 | 910 | 316 | 941 | 403 | 14,102 |
| 2022 | Q4 | 2022-10-30 | D | 7,352 | 2,722 | 741 | 1,666 | 459 | 822 | 362 | 1,041 | 371 | 15,536 |
| 2023 | Q1 | 2023-01-29 | A | 5,112 | 2,194 | 719 | 1,483 | 473 | 818 | 356 | 1,102 | 395 | 12,652 |
| 2023 | Q2 | 2023-04-30 | A | 7,733 | 2,952 | 1,099 | 1,813 | 663 | 1,134 | 429 | 1,168 | 396 | 17,387 |
| 2023 | Q3 | 2023-07-30 | A | 6,721 | 2,688 | 964 | 1,745 | 614 | 987 | 334 | 1,360 | 388 | 15,801 |
| 2023 | Q4 | 2023-10-29 | D | 6,885 | 2,287 | 723 | 1,802 | 701 | 855 | 310 | 1,464 | 385 | 15,412 |
| 2024 | Q1 | 2024-01-28 | A | 4,791 | 1,718 | 649 | 1,483 | 626 | 763 | 292 | 1,480 | 383 | 12,185 |
| 2024 | Q2 | 2024-04-28 | A | 6,507 | 2,098 | 1,017 | 1,736 | 695 | 1,080 | 271 | 1,483 | 348 | 15,235 |
| 2024 | Q3 | 2024-07-28 | A | 5,038 | 2,168 | 825 | 1,308 | 643 | 961 | 269 | 1,595 | 345 | 13,152 |
| 2024 | Q4 | 2024-10-27 | D | 4,238 | 1,709 | 532 | 995 | 495 | 837 | 276 | 1,663 | 399 | 11,144 |
| 2025 | Q1 | 2025-01-26 | A | 3,002 | 1,234 | 463 | 770 | 361 | 596 | 226 | 1,579 | 277 | 8,508 |
| 2025 | Q2 | 2025-04-27 | A | 5,135 | 1,964 | 957 | 1,182 | 506 | 949 | 254 | 1,482 | 334 | 12,763 |
| 2025 | Q3 | 2025-07-27 | A | 4,183 | 2,189 | 760 | 1,207 | 491 | 1,013 | 292 | 1,544 | 339 | 12,018 |
| 2025 | Q4 | 2025-11-02 | D | 4,639 | 1,828 | 551 | 1,411 | 564 | 994 | 352 | 1,691 | 364 | 12,394 |
| 2026 | Q1 | 2026-02-01 | A | 3,093 | 1,527 | 576 | 1,111 | 468 | 772 | 269 | 1,486 | 309 | 9,611 |
| 2026 | Q2 | 2026-05-03 | A | 4,403 | 2,339 | 1,063 | 1,514 | 653 | 1,270 | 294 | 1,457 | 376 | 13,369 |

FY2019 (Q1–Q3 only) is also in the CSV on the **original Agriculture & Turf / Construction & Forestry taxonomy** (`notes` contains `taxonomy=AT/CF`). Keep it separate from the table above. Deere's recast of FY2019 exists only as a full-year figure, never quarterly, so there are no PPA-basis FY2019 quarters and none were invented.

---

## 5. Timing of revenue recognition — the equipment-operations "over time" line

FS revenue is almost entirely "over time" (finance income) and swamps the signal, so the table below isolates the equipment segments. **PPA + SAT + CF "over time" is the closest disclosed proxy for precision-guidance / telematics / information-enabled-solutions subscription revenue plus extended-warranty amortisation.**

| FY | Q | PPA over time | SAT over time | CF over time | Eq-ops over time | Eq-ops rev-rec | Over-time % | FS over time |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2020 | Q1 | 43 | 12 | 26 | 81 | 6,700 | 1.21% | 905 |
| 2020 | Q2 | 35 | 14 | 26 | 75 | 8,378 | 0.90% | 849 |
| 2020 | Q3 | 39 | 17 | 28 | 84 | 8,032 | 1.05% | 865 |
| 2020 | Q4 | 52 | 13 | 30 | 95 | 8,841 | 1.07% | 864 |
| 2021 | Q1 | 42 | 16 | 30 | 88 | 8,228 | 1.07% | 860 |
| 2021 | Q2 | 40 | 15 | 23 | 78 | 11,166 | 0.70% | 866 |
| 2021 | Q3 | 45 | 21 | 23 | 89 | 10,625 | 0.84% | 875 |
| 2021 | Q4 | 31 | 25 | 15 | 71 | 10,458 | 0.68% | 841 |
| 2022 | Q1 | 37 | 20 | 22 | 79 | 8,699 | 0.91% | 846 |
| 2022 | Q2 | 32 | 13 | 17 | 62 | 12,506 | 0.50% | 838 |
| 2022 | Q3 | 31 | 19 | 20 | 70 | 13,199 | 0.53% | 876 |
| 2022 | Q4 | 40 | 24 | 26 | 90 | 14,548 | 0.62% | 960 |
| 2023 | Q1 | 55 | 25 | 25 | 105 | 11,612 | 0.90% | 1,017 |
| 2023 | Q2 | 51 | 29 | 22 | 102 | 16,280 | 0.63% | 1,080 |
| 2023 | Q3 | 115 | 37 | 28 | 180 | 14,573 | 1.24% | 1,198 |
| 2023 | Q4 | 97 | 40 | 30 | 167 | 14,066 | 1.19% | 1,315 |
| 2024 | Q1 | 88 | 36 | 31 | 155 | 10,809 | 1.43% | 1,348 |
| 2024 | Q2 | 70 | 40 | 26 | 136 | 13,840 | 0.98% | 1,360 |
| 2024 | Q3 | 99 | 44 | 24 | 167 | 11,663 | 1.43% | 1,454 |
| 2024 | Q4 | 110 | 50 | 36 | 196 | 9,621 | 2.04% | 1,487 |
| 2025 | Q1 | 87 | 47 | 30 | 164 | 7,038 | 2.33% | 1,441 |
| 2025 | Q2 | 108 | 49 | 39 | 196 | 11,378 | 1.72% | 1,351 |
| 2025 | Q3 | 114 | 57 | 42 | 213 | 10,600 | 2.01% | 1,382 |
| 2025 | Q4 | 129 | 62 | 45 | 236 | 10,846 | 2.18% | 1,508 |
| 2026 | Q1 | 105 | 50 | 39 | 194 | 8,227 | 2.36% | 1,351 |
| 2026 | Q2 | 105 | 47 | 35 | 187 | 12,003 | 1.56% | 1,329 |

**This is the clearest growth signal in the whole footnote.** Equipment-operations over-time revenue has gone from ~0.5–0.9% of equipment rev-rec revenue in FY2021–FY2022 to **2.0–2.4%** in FY2025–FY2026, and it has grown in absolute terms straight through the ag downturn:

- Eq-ops over-time revenue: FY2022 ~301m → FY2023 ~554m → FY2024 ~654m → FY2025 ~809m (sum of the four quarters above). Roughly **+2.7x in three years** while equipment rev-rec revenue fell ~19% (48,952 → 39,862).
- PPA is where it concentrates: PPA over-time was 0.5–0.6% of PPA revenue in FY2022, **2.28% in Q2 FY2026** and **3.21% in Q1 FY2026** (the ratio rises in low-volume quarters because the subscription base is not volume-linked).
- The mix shift is genuinely counter-cyclical: PPA over-time revenue in Q2 FY2026 (105) is *below* Q2 FY2025 (108) in dollars but the ratio rose because PPA equipment revenue fell 14%.

Treat the ratio, not the dollar amount, as the structural trend, and note that the dollar amount is small relative to the PPA operating-profit target — 105m of over-time revenue per quarter cannot by itself move a PPA operating-profit forecast by more than roughly its own magnitude.

---

## 6. Bridge from this rev-rec basis to 8-K segment net sales

Empirically, **point-in-time rev-rec revenue ≈ segment net sales**, and the gap between rev-rec total and segment net sales is approximately the over-time component (which lands in "Other income", not "Net sales"). Difference = point-in-time minus 8-K segment net sales, USDm:

| FY | Q | PPA | SAT | CF |
|---|---|---:|---:|---:|
| 2024 | Q1 | +106 | +31 | +31 |
| 2024 | Q2 | +28 | +28 | +38 |
| 2024 | Q3 | +44 | +31 | +34 |
| 2025 | Q1 | +19 | +12 | +34 |
| 2025 | Q2 | −12 | +3 | +20 |
| 2025 | Q3 | −3 | +7 | +26 |
| 2026 | Q1 | +1 | +6 | +25 |
| 2026 | Q2 | −1 | +10 | +29 |

For the last four quarters the PPA residual is within ±3m and the SAT residual within ±10m; CF runs a persistent +20 to +30m. So:

**PPA segment net sales ≈ (Production agriculture + Financial products·PPA + Other·PPA) − PPA over-time revenue**, accurate to a few million in recent quarters.

Worked check, Q2 FY2026: 4,403 + 52 + 152 = 4,607 rev-rec; less 105 over-time = 4,502; 8-K PPA net sales 4,503. Q2 FY2025: 5,135 + 56 + 135 = 5,326; less 108 = 5,218; 8-K 5,230 (−12).

One outlier to know about: **Q2 FY2022 CF** shows a +360 residual because the CF `Other` line jumped to 433 (versus ~100 typical) in the quarter of the Deere-Hitachi joint-venture dissolution. It cross-foots correctly; it is a real disclosed spike, not a parse error.

---

## 7. Precision ag, subscriptions and Solutions-as-a-Service — what the filings actually disclose

There is **no disclosed precision-ag revenue figure**. Four quantified proxies exist, all in the CSV or below.

### 7.1 Over-time equipment revenue
Section 5. ~2.0–2.4% of equipment rev-rec revenue and rising; the accounting policy note says the deferred portion of bundled precision guidance / telematics is exactly what is recognised over the service period.

### 7.2 Deferred revenue (contract liability) and remaining performance obligations
Deere states these relate to "extended warranty premiums, advance payments for future equipment sales, and **subscription and service revenue related to precision guidance, telematic services, and other information enabled solutions**."

| Period end | FY | Q | Deferred revenue (contract liability) | RPO > 1 year |
|---|---|---|---:|---:|
| 2018-10-28 | 2018 | Q4 | 915 |  |
| 2019-01-27 | 2019 | Q1 | 956 |  |
| 2019-04-28 | 2019 | Q2 | 1,014 |  |
| 2019-07-28 | 2019 | Q3 | 1,022 |  |
| 2019-11-03 | 2019 | Q4 | 1,010 |  |
| 2020-02-02 | 2020 | Q1 | 1,070 |  |
| 2020-05-03 | 2020 | Q2 | 1,077 |  |
| 2020-08-02 | 2020 | Q3 | 1,115 |  |
| 2020-11-01 | 2020 | Q4 | 1,090 |  |
| 2021-01-31 | 2021 | Q1 | 1,169 |  |
| 2021-05-02 | 2021 | Q2 | 1,249 |  |
| 2021-08-01 | 2021 | Q3 | 1,259 |  |
| 2021-10-31 | 2021 | Q4 | 1,344 |  |
| 2022-01-30 | 2022 | Q1 | 1,348 |  |
| 2022-05-01 | 2022 | Q2 | 1,423 |  |
| 2022-07-31 | 2022 | Q3 | 1,424 |  |
| 2022-10-30 | 2022 | Q4 | 1,423 |  |
| 2023-01-29 | 2023 | Q1 | 1,502 |  |
| 2023-04-30 | 2023 | Q2 | 1,622 | 1,378 |
| 2023-07-30 | 2023 | Q3 | 1,753 | 1,437 |
| 2023-10-29 | 2023 | Q4 | 1,697 |  |
| 2024-01-28 | 2024 | Q1 | 1,747 | 1,531 |
| 2024-04-28 | 2024 | Q2 | 1,911 | 1,633 |
| 2024-07-28 | 2024 | Q3 | 1,895 | 1,677 |
| 2024-10-27 | 2024 | Q4 | 1,923 |  |
| 2025-01-26 | 2025 | Q1 | 2,027 | 1,734 |
| 2025-04-27 | 2025 | Q2 | 2,089 | 1,774 |
| 2025-07-27 | 2025 | Q3 | 2,100 | 1,823 |
| 2025-11-02 | 2025 | Q4 | 2,039 |  |
| 2026-02-01 | 2026 | Q1 | 2,121 | 1,811 |
| 2026-05-03 | 2026 | Q2 | 2,155 | 1,855 |

The contract liability has compounded steadily and, unlike equipment revenue, did **not** fall in the downturn: 915 at FY2018 year end → 1,344 at FY2021 → 1,923 at FY2024 → **2,155 at 3 May 2026** (+3.2% vs 2,089 a year earlier, +5.7% vs the FY2025 year-end 2,039). RPO greater than one year: 1,855 at 3 May 2026 versus 1,774 a year earlier (+4.6%).

Deere also discloses the run-off of the >1-year RPO by fiscal year, at 3 May 2026: remainder of 2026 320; 2027 591; 2028 402; 2029 254; 2030 156; 2031 87; later 45. Revenue recognised in the quarter from deferred revenue that was a contract liability at the start of the fiscal year: 163 in Q2 FY2026 versus 176 in Q2 FY2025 (428 versus 373 for the six months).

### 7.3 Operational metrics (no revenue attached)
From the 8 December 2025 investor day: over 1 million connected machines; John Deere Operations Center at **500 million Engaged Acres**, of which **30% Highly Engaged**; target 600 million engaged acres and 50% highly engaged by 2030; highly engaged acres doubled over three years; monthly active users +33% year on year; ~400,000 unique digital users today, targeting 1 million by 2030.

### 7.4 The SaaS ambition was pushed out — this is the single most important qualitative item
At the same investor day Deere stated that its previous LEAP Ambition of **10% of revenue from recurring sources by 2030** has slipped: "the combination of a softer ag market, the time required to build the infrastructure to support a SaaS model, and more disruptive solutions taking longer to adopt have shifted out the estimated timeframe to reach the 10% threshold… a timeline to achieve the target will extend beyond 2030." Separately, of the 2030 growth drivers, "around $2–$3 billion expected to come from incremental tech utilization via SaaS and additional lifecycle sales."

The extracted over-time series corroborates the pushed-out timeline arithmetically: 2.2% of equipment revenue in FY2025 against a 10% ambition. **Do not model a step-change in precision-ag subscription revenue inside FY2026 Q3.** The margin-accretive component of PPA is real and compounding but at roughly 100–130m per quarter it is a second-order driver of PPA operating profit relative to volume and price.

---

## 8. Gaps, derivations and every quarter that did not reconcile

### 8.1 Derived quarters (subtraction of disclosed cumulatives only)

| Quarter | Derivation | Cross-check against the corrupt but directly-disclosed table |
|---|---|---|
| FY2020 Q1 (PPA basis) | 6M ended 2020-05-03 − 3M ended 2020-05-03 | Total 7,631 = disclosed total 7,631 |
| FY2020 Q3 (both taxonomies) | 9M ended 2020-08-02 − 6M ended 2020-05-03 | Total 8,925 = disclosed 8,925. Production agriculture 3,209 derived vs **3,210 disclosed**; Financial products 922 vs **921**. Compact construction 303 / Roadbuilding 818 / Forestry 241 match the merged raw cells exactly. |
| FY2021 Q1 | 6M ended 2021-05-02 − 3M ended 2021-05-02 | Total 9,112 = disclosed 9,112. Production agriculture 3,012 vs **3,011 disclosed**; Small agriculture 1,811 vs **1,812**. |
| FY2020/21/22/23/25 Q4 | 12M − 9M | FY2025 Q4 total 12,394 = the Q4 FY2025 8-K "Total net sales and revenues" 12,394 |
| FY2024 Q4 | 12M − (6M + Q3) — the FY2024 nine-month table exists only in a corrupt rendering | Total 11,144 vs 11,143 in the Q4 FY2024 8-K (**+1**) |

**The ±1 to ±2 residuals are real.** Deere rounds each column of each cumulative table independently, so a difference of disclosed cumulatives is not always identical to the disclosed discrete quarter. Where a discrete figure was also disclosed, the derived value is within 1 of it. Do not treat derived quarters as exact to the last dollar; treat them as exact to ±2m per product line.

### 8.2 Periods deliberately absent (missing data is an absent row, never a zero)

- **FY2019 Q4 on the AT/CF taxonomy** — would need the FY2019 annual AT/CF table, which survives in the corpus only as an unparseable plain-text rendering (2019-11-27 10-K) and a corrupt pipe rendering (2020-11-25 10-K). Not derived, not guessed.
- **FY2019 quarters on the PPA taxonomy** — Deere recast FY2019 only at the full-year level. No quarterly recast exists.
- **FY2026 Q3 and FY2026 Q4** — not yet reported. Nothing in the corpus, and nothing invented.

### 8.3 The 15 flagged tables (all superseded by a clean rendering of the same period)

`2019-08-16` 9M FY2019 · `2020-11-25` FY2019 · `2021-02-19` Q1 FY2021 and Q1 FY2020 · `2021-08-20` Q3 FY2020 · `2021-11-24` FY2021 and FY2020 · `2022-08-19` 9M FY2022 · `2024-02-15` Q1 FY2023 · `2024-08-15` 9M FY2023 · `2024-11-21` FY2024, FY2023, FY2022 · `2025-08-14` 9M FY2024 · `2025-11-26` FY2023. Cause in every case: cells merged in the markdown conversion. One further table (`2023-08-18` line 587, a Q3 FY2022 comparative) could not be assigned a period and was dropped; that period is available cleanly elsewhere.

### 8.4 Two corpus traps confirmed

- `INDEX.md` labels the 2026-05-21 call transcript "Q3 2026". It is the **Q2 FY2026** call. Confirmed against the transcript and the accompanying 8-K.
- Two renderings of the Q2 FY2026 10-Q exist (`2026-05-21…1055929` and `2026-05-28…1055932`). The 05-28 rendering is complete; the 05-21 rendering drops the six-month product-line Total row and merges `Compact construction Roadbuilding`. Both agree on every cell they share.

### 8.5 53-week years

FY2019 (ended 2019-11-03) and FY2025 (ended 2025-11-02) each contained 53 weeks, with the extra week in Q4. Derived Q4 FY2019 and Q4 FY2025 therefore cover 14 weeks. This does **not** affect Q3 FY2026 versus Q3 FY2025 — both are 13-week quarters.

---

## 9. What this extract says about the three FY2026 Q3 targets

Anchors, all rev-rec basis, all from the extract:

| Product line | FY2025 Q3 actual | FY2026 Q1 YoY | FY2026 Q2 YoY | FY2026 H1 YoY |
|---|---:|---:|---:|---:|
| Production agriculture | 4,183 | +3.0% | −14.3% | −7.9% |
| Small agriculture | 2,189 | +23.7% | +19.1% | +20.9% |
| Turf | 760 | +24.4% | +11.1% | +15.4% |
| Construction | 1,207 | +44.3% | +28.1% | +34.5% |
| Compact construction | 491 | +29.6% | +29.1% | +29.3% |
| Roadbuilding | 1,013 | +29.5% | +33.8% | +32.2% |
| Forestry | 292 | +19.0% | +15.7% | +17.3% |
| Financial products | 1,544 | −5.9% | −1.7% | −3.9% |
| Other | 339 | +11.6% | +12.6% | +12.1% |
| **Total** | **12,018** | | | |

Read-throughs:

1. **Worldwide net sales and revenues.** The rev-rec Total ties exactly to the income-statement "Total net sales and revenues" (verified: Q4 FY2025 12,394 both ways; Q2 FY2026 13,369 both ways). So a product-line build gives the top-line target directly. FY2025 Q3 was 12,018 on this basis.
2. **PPA operating profit.** The product-line detail decomposes PPA revenue into Production agriculture (95.6% of PPA rev-rec in Q2 FY2026), Financial products (1.1%) and Other (3.3%). Production agriculture is the only material driver. Its trajectory is the sharpest divergence in the whole dataset: **+3.0% in Q1 FY2026, then −14.3% in Q2** — the CF and SAT lines are up 20–34% while production ag has turned back down. That divergence, not the company average, is what determines PPA. FY2026 guidance of PPA down 5–10% is consistent with H1 actual −7.9%; the H1-to-guidance arithmetic implies production agriculture roughly flat to down high single digits in H2.
3. **Diluted EPS.** Only indirectly — the extract constrains revenue and mix, not cost. The one direct contribution is the over-time / subscription mix, which is margin-accretive but at ~105m per quarter in PPA is too small to swing EPS materially.
4. **Do not extrapolate the SaaS ramp into Q3.** Deere pushed the 10%-recurring-revenue ambition beyond 2030 in December 2025. The over-time series is compounding at a steady 2.0–2.4% of equipment revenue, with no inflection in the last six quarters.

---

## 10. Reproduce

```
python3 /Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/build_de_product_lines.py
```

Prints the parse counts, every conflict, the discrete-quarter derivation log and the validation report, then writes the CSV. Standard library only; no network.
