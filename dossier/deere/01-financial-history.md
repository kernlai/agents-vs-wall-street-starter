# Deere & Company (NYSE: DE) — Quarterly Financial History and Q3 Seasonality

**Prepared:** 16 August 2026 · **Agent:** financial-history · **Purpose:** numeric backbone for the FY2026 Q3 forecast
**Corpus root:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`
(All relative paths below are relative to that root.)

---

## 0. Status of FY2026 Q3 — READ FIRST

**No FY2026 Q3 actuals exist anywhere in this corpus. Nothing in this document is a reported Q3 FY2026 result.**

- The most recent **reported** quarter is **FY2026 Q2**, quarter ended **3 May 2026**, released **21 May 2026**, 10-Q filed **28 May 2026**.
- `INDEX.md` contains a row `2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call Transcript` →
  `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`. **This is mislabelled.** Its `period:` header says
  "Q3 2026" but it was published on the Q2 earnings date and its content is unambiguously the Q2 FY2026 call: it discusses the
  **$272 million IEEPA tariff recovery** that appears in the Q2 FY2026 press release, and the full-year 2026 tariff run-rate.
  Treat it as **Q2 FY2026 Q&A**. (Verified by reading the file directly.)
- Everything in §5 labelled "mechanical implication" is **MY INFERENCE** from historical ratios, not a reported figure.

### Fiscal calendar (matters for the Q3 comparison)
| Period | Quarter end | Weeks | Source |
|---|---|---|---|
| FY2025 Q3 | 27 Jul 2025 | 13 | `filings/2025-08-14__de-us-20250814-q3-10q__155834.md` ("quarterly period ended July 27, 2025") |
| FY2025 Q4 / FY2025 | 2 Nov 2025 | 14 / **53-week year** | `filings/2025-11-26__de-us-20251126-q4-8k__361233.md` (table header "November 2 2025") |
| FY2026 Q1 | 1 Feb 2026 | 13 | `filings/2026-02-19__de-us-20260219-q1-8k__603009.md` ("quarter ended February 1, 2026") |
| FY2026 Q2 | 3 May 2026 | 13 | `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` ("quarterly period ended May 3, 2026") |
| FY2026 Q3 | **~2 Aug 2026 (inferred)** | 13 (inferred) | MY INFERENCE from the 4-4-5 pattern above |

**Implication:** FY2026 Q3 (≈4 May – 2 Aug 2026) is a clean 13-week quarter versus a clean 13-week FY2025 Q3.
The extra 53rd week sat in **Q4 FY2025**, so it does **not** distort the Q3-vs-Q3 comparison, but it **does** inflate the
FY2025 full-year base used in any "% of full year" seasonality calculation (see §4 caveat).

---

## 1. Source documents by fiscal year

All figures below are REPORTED FACT taken from these documents unless explicitly flagged otherwise.

| Fiscal year | Primary source documents (relative paths) |
|---|---|
| FY2013 | Quarterly detail only from transcripts: `call-transcripts/2013-02-13__de-us-20130213-call-pres__1532730.md`, `…2013-05-15…call-pres__1530346.md`, `…2013-08-14…call-pres__1529031.md`, `…2013-11-20…call-pres__1527987.md`. FY total from `filings/2015-11-25__de-us-20151125-q4-10k__469104.md` (3-year income statement) |
| FY2014 | Prior-year comparative columns in the FY2015 releases: `filings/2015-02-20__…q1-8k__784661.md`, `…2015-05-22…q2-8k__784603.md`, `…2015-08-21…q3-8k__784604.md`, `…2015-11-25…q4-8k__784605.md` |
| FY2015 | `filings/2015-02-20__de-us-20150220-q1-8k__784661.md`, `2015-05-22__…q2-8k__784603.md`, `2015-08-21__…q3-8k__784604.md`, `2015-11-25__…q4-8k__784605.md` (+ 10-K `2015-11-25__…q4-10k__469104.md`) |
| FY2016 | `filings/2016-02-19__…q1-8k__784606.md`, `2016-05-20__…q2-8k__784653.md`, `2016-08-19__…q3-8k__784652.md`, `2016-11-23__…q4-8k__784650.md` |
| FY2017 | `filings/2017-02-17__…q1-8k__784623.md`, `2017-05-19__…q2-8k__784651.md`, `2017-08-18__…q3-8k__784624.md`, **Q4:** `filings/2017-11-22__de-us-20171122-fy-8k__784662.md` |
| FY2018 | `filings/2018-02-16__…q1-8k__784666.md`, `2018-05-18__…q2-8k__784663.md`, `2018-08-17__…q3-8k__784667.md`. **Q4 FY2018** from prior-year column of `filings/2019-11-27__de-us-20191127-q4-8k__469218.md` (no FY2018 Q4 8-K in corpus) |
| FY2019 | `filings/2019-02-15__…q1-8k__654630.md`, `2019-05-17__…q2-8k__645299.md`, `2019-08-16__…q3-8k__645300.md`, `2019-11-27__…q4-8k__469218.md` |
| FY2020 | `filings/2020-02-21__…q1-8k__469227.md`, `2020-05-21__…q2-8k__469475.md`, `2020-08-20__…q3-8k__105830.md`, `2020-11-25__…q4-8k__105817.md`. **Restated PPA/SAT split** from prior-year columns of the FY2021 8-Ks |
| FY2021 | `filings/2021-02-19__…q1-8k__105842.md`, `2021-05-21__…q2-8k__105846.md`, `2021-08-20__…q3-8k__105827.md`, `2021-11-24__…q4-8k__105843.md` |
| FY2022 | `filings/2022-02-18__…q1-8k__105812.md`, `2022-05-20__…q2-8k__105815.md`, `2022-08-19__…q3-8k__105811.md`, `2022-11-23__…q4-8k__105825.md` |
| FY2023 | `filings/2023-02-17__…q1-8k__105833.md`, `2023-05-19__…q2-8k__105839.md`, `2023-08-18__…q3-8k__105829.md`, `2023-11-22__…q4-8k__105823.md` |
| FY2024 | `filings/2024-02-15__…q1-8k__105824.md`, `2024-05-16__…q2-8k__105819.md`, `2024-08-15__…q3-8k__105836.md`, `2024-11-21__…q4-8k__105840.md` |
| FY2025 | `filings/2025-02-13__…q1-8k__105841.md`, `2025-05-15__…q2-8k__105808.md`, `2025-08-15__…q3-8k__143410.md`, `2025-11-26__…q4-8k__361233.md` |
| FY2026 (Q1–Q2 only) | `filings/2026-02-19__de-us-20260219-q1-8k__603009.md`; `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` (identical content in `…q2-8k-2__1042168.md`); 10-Q `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` |

**Segment-reporting break:** Deere moved from **Agriculture & Turf / Construction & Forestry** to
**Production & Precision Ag (PPA) / Small Ag & Turf (SAT) / Construction & Forestry (C&F)** effective **FY2021 Q1**,
with FY2020 restated. **PPA data therefore begins in FY2020.** Pre-FY2021 A&T ≈ PPA + SAT.

---

## 2. Consolidated quarterly time series (USD millions, except EPS)

"Net sales" = net sales of the equipment operations. From FY2021 the releases dropped the "Total net sales" subtotal;
for those years net sales = PPA + SAT + C&F (arithmetic check, MY CALCULATION, verified against the FY2026 Q2 release text
"Net sales were $11.778 billion" = 4,503 + 3,485 + 3,790 ✓).

| FY | Qtr | Total net sales & revenues | Equipment net sales | Financial Services revenues | Other revenues | Net income attrib. to Deere | Diluted EPS (GAAP) |
|---|---|---|---|---|---|---|---|
| 2013 | Q1 | ~7,400 | n/f | n/f | n/f | n/f | n/f |
| 2013 | Q2 | ~10,900 | n/f | n/f | n/f | n/f | n/f |
| 2013 | Q3 | ~10,000 | ~9,300 | n/f | n/f | 997 | n/f |
| 2013 | Q4 | ~9,500 | ~8,600 | n/f | n/f | 807 | 2.11 |
| **2013 FY** | | **37,795** | **34,998** | — | — | **3,537** | n/f |
| 2014 | Q1 | 7,654 | 6,949 | 587 | 118 | 681 | 1.81 |
| 2014 | Q2 | 9,948 | 9,246 | 572 | 130 | 981 | 2.65 |
| 2014 | Q3 | 9,500 | 8,723 | 656 | 121 | 851 | 2.33 |
| 2014 | Q4 | 8,965 | 8,043 | 762 | 160 | 649 | 1.83 |
| **2014 FY** | | **36,067** | **32,961** | 2,577 | 529 | **3,162** | **8.63** |
| 2015 | Q1 | 6,383 | 5,605 | 648 | 130 | 387 | 1.12 |
| 2015 | Q2 | 8,171 | 7,399 | 653 | 119 | 690 | 2.03 |
| 2015 | Q3 | 7,594 | 6,840 | 636 | 118 | 512 | 1.53 |
| 2015 | Q4 | 6,715 | 5,932 | 654 | 129 | 351 | 1.08 |
| **2015 FY** | | **28,863** | **25,775** | 2,591 | 497 | **1,940** | **5.77** |
| 2016 | Q1 | 5,525 | 4,769 | 636 | 120 | 254 | 0.80 |
| 2016 | Q2 | 7,875 | 7,107 | 651 | 117 | 495 | 1.56 |
| 2016 | Q3 | 6,724 | 5,861 | 667 | 196 | 489 | 1.55 |
| 2016 | Q4 | 6,520 | 5,650 | 740 | 130 | 285 | 0.90 |
| **2016 FY** | | **26,644** | **23,387** | 2,694 | 563 | **1,524** | **4.81** |
| 2017 | Q1 | 5,625 | 4,698 | 696 | 231 | 194 | 0.61 |
| 2017 | Q2 | 8,287 | 7,260 | 716 | 311 | 802 | 2.49 |
| 2017 | Q3 | 7,808 | 6,833 | 741 | 234 | 642 | 1.97 |
| 2017 | Q4 | 8,018 | 7,094 | 782 | 142 | 510 | 1.57 |
| **2017 FY** | | **29,738** | **25,885** | 2,935 | 918 | **2,159** | **6.68** |
| 2018 | Q1 | 6,913 | 5,974 | 776 | 163 | **−535** | **−1.66** |
| 2018 | Q2 | 10,720 | 9,747 | 795 | 178 | 1,208 | 3.67 |
| 2018 | Q3 | 10,308 | 9,286 | 830 | 192 | 910 | 2.78 |
| 2018 | Q4 | 9,416 | 8,343 | 851 | 222 | 785 | 2.42 |
| **2018 FY** | | **37,358** | **33,351** | 3,252 | 755 | **2,368** | **7.24** |
| 2019 | Q1 | 7,984 | 6,941 | 855 | 188 | 499 | 1.54 |
| 2019 | Q2 | 11,342 | 10,273 | 886 | 183 | 1,135 | 3.52 |
| 2019 | Q3 | 10,036 | 8,969 | 910 | 157 | 899 | 2.81 |
| 2019 | Q4 | 9,896 | 8,703 | 971 | 222 | 722 | 2.27 |
| **2019 FY** (53wk) | | **39,258** | **34,886** | 3,621 | 751 | **3,253** | **10.15** |
| 2020 | Q1 | 7,631 | 6,530 | 931 | 170 | 517 | 1.63 |
| 2020 | Q2 | 9,253 | 8,224 | 875 | 154 | 666 | 2.11 |
| 2020 | Q3 | 8,925 | 7,859 | 892 | 174 | 811 | 2.57 |
| 2020 | Q4 | 9,731 | 8,659 | 891 | 181 | 757 | 2.39 |
| **2020 FY** | | **35,540** | **31,272** | 3,589 | 679 | **2,751** | **8.69** |
| 2021 | Q1 | 9,112 | 8,051 | 884 | 177 | 1,224 | 3.87 |
| 2021 | Q2 | 12,058 | 10,998 | 892 | 168 | 1,790 | 5.68 |
| 2021 | Q3 | 11,527 | 10,413 | 902 | 212 | 1,667 | 5.32 |
| 2021 | Q4 | 11,327 | 10,276 | 869 | 182 | 1,283 | 4.12 |
| **2021 FY** | | **44,024** | **39,737** | 3,548 | 739 | **5,963** | **18.99** |
| 2022 | Q1 | 9,569 | 8,531 | 870 | 168 | 903 | 2.92 |
| 2022 | Q2 | 13,370 | 12,034 | 864 | 472 | 2,098 | 6.81 |
| 2022 | Q3 | 14,102 | 13,000 | 903 | 199 | 1,884 | 6.16 |
| 2022 | Q4 | 15,536 | 14,351 | 988 | 197 | 2,246 | 7.44 |
| **2022 FY** | | **52,577** | **47,917** | 3,625 | 1,035 | **7,131** | **23.28** |
| 2023 | Q1 | 12,652 | 11,402 | 1,040 | 210 | 1,959 | 6.55 |
| 2023 | Q2 | 17,387 | 16,079 | 1,107 | 201 | 2,860 | 9.65 |
| 2023 | Q3 | 15,801 | 14,284 | 1,228 | 289 | 2,978 | 10.20 |
| 2023 | Q4 | 15,412 | 13,801 | 1,347 | 264 | 2,369 | 8.26 |
| **2023 FY** | | **61,251** | **55,565** | 4,721 | 965 | **10,166** | **34.63** |
| 2024 | Q1 | 12,185 | 10,486 | 1,376 | 323 | 1,751 | 6.23 |
| 2024 | Q2 | 15,235 | 13,610 | 1,395 | 230 | 2,370 | 8.53 |
| 2024 | Q3 | 13,152 | 11,387 | 1,489 | 276 | 1,734 | 6.29 |
| 2024 | Q4 | 11,143 | 9,275 | 1,522 | 346 | 1,245 | 4.55 |
| **2024 FY** | | **51,716** | **44,759** | 5,782 | 1,175 | **7,100** | **25.62** |
| 2025 | Q1 | 8,508 | 6,809 | 1,470 | 229 | 869 | 3.19 |
| 2025 | Q2 | 12,763 | 11,171 | 1,385 | 207 | 1,804 | 6.64 |
| 2025 | Q3 | 12,018 | 10,357 | 1,418 | 243 | 1,289 | 4.75 |
| 2025 | Q4 (14wk) | 12,394 | 10,579 | 1,548 | 267 | 1,065 | 3.93 |
| **2025 FY** (53wk) | | **45,684** | **38,917** | 5,821 | 946 | **5,027** | **18.50** |
| 2026 | Q1 | 9,611 | 8,001 | 1,384 | 226 | 656 | 2.42 |
| 2026 | **Q2 (latest reported)** | **13,369** | **11,778** | 1,366 | 225 | **1,773** | **6.55** |
| 2026 | **Q3** | **NOT YET REPORTED** | — | — | — | — | — |
| **2026 H1** | | **22,981** | **19,779** | 2,751 | 451 | **2,429** | **8.97** |

`n/f` = not found in corpus. `~` = transcript figure, rounded by the speaker.

**Notes / data-integrity flags**
1. **FY2013 quarterly** figures come from earnings-call remarks ("Net sales and revenues were up 10% to $7.4 billion" etc.),
   not filings — filings coverage in this corpus starts January 2015. Their sum (7.4 + 10.9 + 10.0 + 9.5 = 37.8) reconciles
   with the audited FY2013 total of $37,795.4M in the FY2015 10-K, so they are reliable to ±$0.05bn.
2. **FY2017 Q1** was later restated from $193.8M / $0.61 to $199.0M / $0.62 (pension/OPEB presentation standard) — the
   restated figures appear as the prior-year column in `filings/2018-02-16__de-us-20180216-q1-8k__784666.md`. Table shows as-first-reported.
3. **FY2018 Q1** was a GAAP **net loss** of $535.1M / −$1.66 driven by US tax-reform charges (non-GAAP net income would have
   been $442.1M / $1.35). This is a genuine GAAP outlier — exclude it from EPS-ratio seasonality.
4. **FY2019 and FY2025 were 53-week years**, with the extra week in Q4.
5. FY2026 Q2 GAAP results include a **$272M recovery of IEEPA tariffs** following the 20 Feb 2026 Supreme Court decision
   (`filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`). This is inside GAAP net income and is largely non-recurring.

### Average diluted shares outstanding (millions)
| FY | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| 2023 | 299.1 | 296.5 | 292.1 | 286.9 |
| 2024 | 281.1 | 277.9 | 275.6 | 273.6 |
| 2025 | 272.3 | 271.8 | 271.4 | 271.1 |
| 2026 | 270.9 | **270.8** | — | — |

Source: "Average Shares Outstanding / Diluted" rows in each 8-K / 10-Q. Buyback pace has slowed sharply — the Q1→Q2 FY2026
decline was only 0.1M shares, so a **~270.5–271.0M** diluted count for Q3 FY2026 is a safe working assumption (MY INFERENCE).

---

## 3. Segment quarterly time series (USD millions)

### 3a. Production & Precision Ag (PPA) — the forecast target
| FY | Qtr | PPA net sales | PPA operating profit | PPA operating margin |
|---|---|---|---|---|
| 2020 | Q1 | 2,507 | 218 | 8.7% |
| 2020 | Q2 | 3,365 | 568 | 16.9% |
| 2020 | Q3 | 3,289 | 605 | 18.4% |
| 2020 | Q4 | 3,801 | 578 | 15.2% |
| **2020 FY** | | **12,962** | **1,969** | 15.2% |
| 2021 | Q1 | 3,069 | 643 | 21.0% |
| 2021 | Q2 | 4,529 | 1,007 | 22.2% |
| 2021 | Q3 | 4,250 | 906 | 21.3% |
| 2021 | Q4 | 4,661 | 777 | 16.7% |
| **2021 FY** | | **16,509** | **3,334** | 20.2% |
| 2022 | Q1 | 3,356 | 296 | 8.8% |
| 2022 | Q2 | 5,117 | 1,057 | 20.7% |
| 2022 | Q3 | 6,096 | 1,293 | 21.2% |
| 2022 | Q4 | 7,434 | 1,740 | 23.4% |
| **2022 FY** | | **22,002** | **4,386** | 19.9% |
| 2023 | Q1 | 5,198 | 1,208 | 23.2% |
| 2023 | Q2 | 7,822 | 2,170 | 27.7% |
| 2023 | Q3 | 6,806 | 1,782 | 26.2% |
| 2023 | Q4 | 6,965 | 1,836 | 26.4% |
| **2023 FY** | | **26,790** | **6,996** | 26.1% |
| 2024 | Q1 | 4,849 | 1,045 | 21.6% |
| 2024 | Q2 | 6,581 | 1,650 | 25.1% |
| 2024 | Q3 | 5,099 | 1,162 | 22.8% |
| 2024 | Q4 | 4,305 | 657 | 15.3% |
| **2024 FY** | | **20,834** | **4,514** | 21.7% |
| 2025 | Q1 | 3,067 | 338 | 11.0% |
| 2025 | Q2 | 5,230 | 1,148 | 22.0% |
| 2025 | Q3 | 4,273 | 580 | 13.6% |
| 2025 | Q4 | 4,740 | 604 | 12.7% |
| **2025 FY** | | **17,311** | **2,671** | 15.4% |
| 2026 | Q1 | 3,163 | 139 | 4.4% |
| 2026 | **Q2** | **4,503** | **706** | **15.7%** |
| **2026 H1** | | **7,666** | **845** | 11.0% |

### 3b. Small Ag & Turf (SAT)
| FY | Q1 sales / op | Q2 sales / op | Q3 sales / op | Q4 sales / op | FY sales / op |
|---|---|---|---|---|---|
| 2020 | 1,979 / 155 | 2,603 / 226 | 2,383 / 337 | 2,397 / 282 | 9,363 / 1,000 |
| 2021 | 2,515 / 469 | 3,390 / 648 | 3,147 / 583 | 2,809 / 346 | 11,860 / 2,045 |
| 2022 | 2,631 / 371 | 3,570 / 520 | 3,635 / 552 | 3,544 / 506 | 13,381 / 1,949 |
| 2023 | 3,001 / 447 | 4,145 / 849 | 3,739 / 732 | 3,094 / 444 | 13,980 / 2,472 |
| 2024 | 2,425 / 326 | 3,185 / 571 | 3,053 / 496 | 2,306 / 234 | 10,969 / 1,627 |
| 2025 | 1,748 / 124 | 2,994 / 574 | 3,025 / 485 | 2,457 / 25 | 10,224 / 1,207 |
| 2026 | 2,168 / 196 | **3,485 / 719** | — | — | H1 5,653 / 916 |

### 3c. Construction & Forestry (C&F)
| FY | Q1 sales / op | Q2 sales / op | Q3 sales / op | Q4 sales / op | FY sales / op |
|---|---|---|---|---|---|
| 2020 | 2,044 / 93 | 2,256 / 96 | 2,187 / 205 | 2,461 / 196 | 8,947 / 590 |
| 2021 | 2,467 / 268 | 3,079 / 489 | 3,016 / 463 | 2,806 / 270 | 11,368 / 1,489 |
| 2022 | 2,544 / 272 | 3,347 / 814 | 3,269 / 514 | 3,373 / 414 | 12,534 / 2,014 |
| 2023 | 3,203 / 625 | 4,112 / 838 | 3,739 / 716 | 3,742 / 516 | 14,795 / 2,695 |
| 2024 | 3,212 / 566 | 3,844 / 668 | 3,235 / 448 | 2,664 / 328 | 12,956 / 2,009 |
| 2025 | 1,994 / 65 | 2,947 / 379 | 3,059 / 237 | 3,382 / 348 | 11,382 / 1,028 |
| 2026 | 2,670 / 137 | **3,790 / 561** | — | — | H1 6,460 / 698 |

### 3d. Financial Services operating profit and total operating profit
| FY | Q1 | Q2 | Q3 | Q4 | FY |
|---|---|---|---|---|---|
| FS op 2023 | 238 | 41 | 286 | 229 | 795 |
| FS op 2024 | 257 | 209 | 191 | 231 | 889 |
| FS op 2025 | 266 | 207 | 266 | 374 | 1,114 |
| FS op 2026 | 301 | **251** | — | — | H1 552 |
| Total op profit 2025 | 793 | 2,308 | 1,568 | 1,351 | 6,020 |
| Total op profit 2026 | 773 | **2,237** | — | — | H1 3,011 |

### 3e. Legacy Agriculture & Turf (pre-FY2021 reporting basis)
| FY | Q1 sales / op | Q2 sales / op | Q3 sales / op | Q4 sales / op |
|---|---|---|---|---|
| 2014 | 5,596 / 797 | 7,646 / 1,229 | 6,969 / 941 | 6,169 / 682 |
| 2015 | 4,081 / 268 | 5,766 / 639 | 5,308 / 472 | 4,656 / 271 |
| 2016 | 3,600 / 144 | 5,742 / 614 | 4,704 / 571 | 4,441 / 371 |
| 2017 | 3,598 / 213 | 5,794 / 1,003 | 5,338 / 685 | 5,437 / 584 |
| 2018 | 4,243 / 387 | 7,049 / 1,056 | 6,293 / 806 | 5,605 / 567 |
| 2019 | 4,681 / 348 | 7,282 / 1,019 | 5,946 / 612 | 5,756 / 527 |
| 2020 | 4,486 / 373 | 5,968 / 794 | 5,672 / 942 | 6,198 / 860 |
| (C&F 2014–20) | see below | | | |
| C&F 2014 | 1,353 / 94 | 1,600 / 132 | 1,754 / 194 | 1,874 / 228 |
| C&F 2015 | 1,524 / 146 | 1,633 / 189 | 1,532 / 129 | 1,276 / 64 |
| C&F 2016 | 1,169 / 70 | 1,365 / 74 | 1,157 / 54 | 1,209 / −17 |
| C&F 2017 | 1,100 / 34 | 1,466 / 108 | 1,495 / 110 | 1,657 / 85 |
| C&F 2018 | 1,731 / 32 | 2,698 / 259 | 2,993 / 281 | 2,738 / 295 |
| C&F 2019 | 2,260 / 229 | 2,991 / 347 | 3,023 / 378 | 2,947 / 261 |
| C&F 2020 | 2,044 / 93 | 2,256 / 96 | 2,187 / 205 | 2,461 / 196 |

---

## 4. Q3 SEASONALITY — the core output

### 4a. Total net sales and revenues: Q3 as % of full year, and Q3 ÷ Q2

| FY | Q1 | Q2 | Q3 | Q4 | FY total | **Q3 % of FY** | **Q3 ÷ Q2** | Q3 ÷ Q1 | H2 ÷ H1 |
|---|---|---|---|---|---|---|---|---|---|
| 2014 | 7,654 | 9,948 | 9,500 | 8,965 | 36,067 | 26.3% | **0.955** | 1.241 | 1.049 |
| 2015 | 6,383 | 8,171 | 7,594 | 6,715 | 28,863 | 26.3% | **0.929** | 1.190 | 0.983 |
| 2016 | 5,525 | 7,875 | 6,724 | 6,520 | 26,644 | 25.2% | **0.854** | 1.217 | 0.988 |
| 2017 | 5,625 | 8,287 | 7,808 | 8,018 | 29,738 | 26.3% | **0.942** | 1.388 | 1.138 |
| 2018 | 6,913 | 10,720 | 10,308 | 9,416 | 37,357 | 27.6% | **0.962** | 1.491 | 1.119 |
| 2019 | 7,984 | 11,342 | 10,036 | 9,896 | 39,258 | 25.6% | **0.885** | 1.257 | 1.031 |
| 2020 | 7,631 | 9,253 | 8,925 | 9,731 | 35,540 | 25.1% | **0.965** | 1.170 | 1.105 |
| 2021 | 9,112 | 12,058 | 11,527 | 11,327 | 44,024 | 26.2% | **0.956** | 1.265 | 1.080 |
| 2022 | 9,569 | 13,370 | 14,102 | 15,536 | 52,577 | 26.8% | **1.055** | 1.474 | 1.292 |
| 2023 | 12,652 | 17,387 | 15,801 | 15,412 | 61,252 | 25.8% | **0.909** | 1.249 | 1.039 |
| 2024 | 12,185 | 15,235 | 13,152 | 11,143 | 51,715 | 25.4% | **0.863** | 1.079 | 0.886 |
| 2025 | 8,508 | 12,763 | 12,018 | 12,394 | 45,683 | 26.3% | **0.942** | 1.413 | 1.148 |

**Summary statistics (n = 12, FY2014–FY2025)**

| Metric | Mean | Median | Min | Max | Std dev (pop.) |
|---|---|---|---|---|---|
| **Q3 as % of full-year net sales & revenues** | **26.08%** | **26.22%** | 25.11% (FY2020) | 27.59% (FY2018) | 0.68 pp |
| **Q3 ÷ Q2 net sales & revenues** | **0.935** | **0.942** | 0.854 (FY2016) | 1.055 (FY2022) | 0.052 |
| Q3 ÷ Q1 | 1.286 | 1.253 | 1.079 | 1.491 | 0.122 |
| H2 ÷ H1 | 1.071 | 1.064 | 0.886 | 1.292 | 0.098 |

**Sub-samples of the Q3 ÷ Q2 ratio**

| Sample | Mean | Median | Range |
|---|---|---|---|
| All 12 years (FY2014–25) | 0.935 | 0.942 | 0.854 – 1.055 |
| Last 5 years (FY2021–25) | 0.945 | 0.942 | 0.863 – 1.055 |
| Last 3 years (FY2023–25) | 0.905 | 0.909 | 0.863 – 0.942 |
| **Down-cycle years only** (FY2015, 16, 19, 20, 24, 25) | **0.906** | **0.907** | 0.854 – 0.965 |
| Up-cycle years only (FY2014, 17, 18, 21, 22, 23) | 0.963 | 0.955 | 0.909 – 1.055 |

> **The single most useful number:** Q3 total net sales & revenues has run at **0.94× Q2** on average over 12 years
> (median 0.94), tightening to **0.91×** in the last three years and **0.91×** across down-cycle years. It has **never**
> fallen below 0.85× and has exceeded 1.0× only once (FY2022, a supply-chain catch-up year with an unusually weak Q2 base).
> Q3 has been **25.1%–27.6% of the full fiscal year in every one of the last twelve years** — a remarkably tight band.

**Caveat on the "% of FY" metric:** FY2019 and FY2025 were 53-week years with the extra week in Q4, which mechanically
depresses their Q3 share by roughly 0.3–0.4 pp. FY2026 is expected to be a 52-week year, so the ratio for FY2026 should
sit at or slightly above the historical mean rather than below it (MY INFERENCE).

### 4b. Equipment net sales only (excludes Financial Services and Other)

| FY | Q3 % of FY | Q3 ÷ Q2 |
|---|---|---|
| 2014 | 26.5% | 0.943 |
| 2015 | 26.5% | 0.924 |
| 2016 | 25.1% | 0.825 |
| 2017 | 26.4% | 0.941 |
| 2018 | 27.8% | 0.953 |
| 2019 | 25.7% | 0.873 |
| 2020 | 25.1% | 0.956 |
| 2021 | 26.2% | 0.947 |
| 2022 | 27.1% | 1.080 |
| 2023 | 25.7% | 0.888 |
| 2024 | 25.4% | 0.837 |
| 2025 | 26.6% | 0.927 |
| **Mean / Median** | **26.2% / 26.3%** | **0.925 / 0.934** |
| **Range** | 25.1% – 27.8% | 0.825 – 1.080 |
| Last 3y mean | 25.9% | 0.884 |

Equipment sales are slightly *more* Q3-seasonal-negative than the consolidated line, because Financial Services revenue is
near-flat quarter to quarter (FY2026 Q1 1,384 → Q2 1,366) and therefore damps the consolidated ratio.

### 4c. Segment-level Q3 seasonality

| Segment / metric | Years | Q3 % of FY (mean / median / range) | **Q3 ÷ Q2** (mean / median / range) | Last-3y Q3 ÷ Q2 mean |
|---|---|---|---|---|
| **PPA net sales** | FY2020–25 | 25.6% / 25.4% / 24.5–27.7% | **0.928 / 0.904 / 0.775–1.191** | **0.821** |
| **PPA operating profit** | FY2020–25 | 26.7% / 26.5% / 21.7–30.7% | **0.870 / 0.861 / 0.505–1.223** | **0.677** |
| SAT net sales | FY2020–25 | 27.2% / 27.0% / 25.5–29.6% | 0.956 / 0.943 / 0.902–1.018 | 0.957 |
| SAT operating profit | FY2020–25 | 31.8% / 30.1% / 28.3–40.2% | 1.005 / 0.884 / 0.845–1.491 | 0.859 |
| C&F net sales | FY2020–25 | 25.7% / 25.7% / 24.4–26.9% | 0.952 / 0.973 / 0.842–1.038 | 0.930 |
| C&F operating profit | FY2020–25 | 27.2% / 26.0% / 22.3–34.7% | 0.977 / 0.763 / 0.625–2.135 | 0.717 |
| Net income attrib. to Deere | FY2014–25 | 28.7% / 27.8% / 24.4–38.4% | **0.873 / 0.834 / 0.715–1.218** | 0.829 |
| Q3 as % of **H2** net income | FY2014–25 | **55.6% / 55.7% / 45.6–63.2%** | — | — |

**PPA is the most Q3-negative line in the business.** Its Q3 ÷ Q2 operating-profit ratio has averaged 0.87× over six years
but has fallen every year since FY2022 (1.223 → 0.821 → 0.704 → 0.505). The driver is structural: Deere front-loads
large-ag combine and high-horsepower tractor shipments into Q2, then under-produces in Q3 to manage dealer inventory in a
down cycle. Q3 PPA operating margin has compressed to 13.6% (FY2025) from 26.2% (FY2023) while Q2 margin held at 22.0%.

**Note on SAT operating profit:** the FY2025 Q4 figure of just $25M (0.6% margin) is an outlier — it drags the FY2025
"Q3 % of FY" for SAT op profit to 40.2%. Use the median, not the mean, for that row.

---

## 5. Mechanical implications for FY2026 Q3 (MY INFERENCE — not reported, not a forecast)

These are arithmetic consequences of the ratios above applied to reported FY2026 Q2 actuals. A forecast must overlay
company guidance, order-book, industry and FX judgement — that is other agents' work.

**Anchors (REPORTED FACT):** FY2026 Q2 net sales & revenues $13,369M; Q2 PPA operating profit $706M; H1 net income $2,429M;
H1 diluted EPS $8.97; Q2 diluted shares 270.8M.
**Guidance (REPORTED, forward-looking):** FY2026 net income attributable to Deere forecast **$4.5bn to $5.0bn**, maintained
at Q2 (`filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`). FY2026 segment outlook: PPA net sales **down 5–10%**,
SAT **up ~15%**, C&F **up ~20%**; Financial Services net income **~$860M**.

### 5a. Total net sales and revenues
| Method | Ratio | Implied FY2026 Q3 NSR (USDm) |
|---|---|---|
| Q2 × 12-year mean Q3÷Q2 | 0.935 | **12,495** |
| Q2 × 12-year median | 0.942 | **12,592** |
| Q2 × last-5-year mean | 0.945 | 12,632 |
| Q2 × last-3-year mean | 0.905 | 12,094 |
| Q2 × down-cycle mean | 0.906 | 12,116 |
| Q2 × historical minimum | 0.854 | 11,414 (floor) |
| Q2 × historical maximum | 1.055 | 14,100 (ceiling) |

**Central mechanical range: ~$12.1bn – $12.6bn; point ≈ $12.4bn.** That would be **+3% to +5% YoY** versus FY2025 Q3's
$12,018M — directionally consistent with H1 FY2026 running +8% YoY, decelerating as the C&F/SAT comparison base hardens.
Cross-check: at 26.1% of FY (the 12-year mean Q3 share), Q3 = $12.4bn implies FY2026 revenue of ~$47.6bn (+4% on FY2025's
53-week $45.7bn), which is broadly consistent with the segment guidance mix (PPA −5/−10%, SAT +15%, C&F +20%).

### 5b. Diluted EPS (GAAP) and net income
- Guidance implies **H2 FY2026 net income of $2,071M – $2,571M** ($4.5–5.0bn less H1's $2,429M).
- Q3 has averaged **55.6%** of H2 net income (median 55.7%; last-5-year mean 54.2%; range 45.6%–63.2%).
- ⇒ Q3 net income ≈ **$1,150M – $1,430M** at the mean split; at 270.8M diluted shares that is **EPS ≈ $4.25 – $5.27**.
- Alternative anchor: Q2 net income $1,773M × 12-year mean Q3÷Q2 NI of 0.873 = **$1,548M → EPS ≈ $5.72**; × last-3-year
  mean 0.829 = $1,470M → EPS ≈ $5.43. The Q2-ratio method sits **above** the guidance-implied range, which says either
  (a) guidance is conservative, or (b) H2 is expected to be weaker than the normal seasonal pattern. Flagging this tension
  as the single biggest judgement call for the EPS forecast.
- Note the Q2 base is flattered by the **$272M IEEPA tariff recovery**; excluding it, Q2 net income would be roughly
  $1.55bn and the Q2-ratio method would produce ≈$1.35bn / ~$5.00 EPS for Q3, much closer to the guidance-implied range.
  **MY INFERENCE: the $272M is the reconciling item; a Q3 GAAP EPS in the $4.50–$5.30 band is the seasonally coherent zone.**

### 5c. PPA operating profit
| Method | Ratio applied to Q2'26 = $706M | Implied FY2026 Q3 PPA op profit |
|---|---|---|
| 6-year mean Q3÷Q2 | 0.870 | **614** |
| 6-year median | 0.861 | **608** |
| Last-3-year mean | 0.677 | **478** |
| FY2025 actual ratio (worst) | 0.505 | 357 (floor) |
| FY2022 (best) | 1.223 | 863 (ceiling) |

Cross-check via margin: if Q3 PPA net sales follow the last-3-year Q3÷Q2 sales ratio of 0.821 → $3,697M; at FY2025 Q3's
13.6% margin that is $503M, at a modest recovery to 15% it is $555M. FY2025 Q3 actual was **$580M** on 13.6% margin.
**Central mechanical zone: ~$480M – $615M**, i.e. roughly flat to modestly down YoY. The declining trend in the PPA Q3÷Q2
ratio (1.22 → 0.82 → 0.70 → 0.51 across FY2022–25) argues for the lower half of that zone unless the order book has
genuinely inflected.

---

## 6. Gaps and things not found

- **FY2012 Q1 and all of FY2012 quarterly detail** — corpus begins 16 May 2012 (Q2 FY2012 call). Not found.
- **FY2013 and FY2014 segment operating-profit detail at the A&T/C&F level for FY2013** — not found; FY2013 exists only as
  transcript commentary plus the audited FY total in the FY2015 10-K.
- **PPA/SAT split before FY2020** — does not exist; Deere did not report on that basis. Reconstructing it from A&T is not
  possible from this corpus.
- **FY2018 Q4 standalone 8-K** — absent; figures taken from the prior-year column of the FY2019 Q4 release.
- **Any FY2026 Q3 actual** — does not exist. Confirmed by reading every 2026-dated document in the corpus.
- **Consensus/sell-side estimates for FY2026 Q3** — outside this corpus; assigned to another agent.
