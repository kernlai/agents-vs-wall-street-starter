# Home Depot (HD) — FY2026 Q2 Fundamentals Dossier

**Target period:** Fiscal 2026 second quarter — 13 weeks ending **Sunday 2 August 2026**
**CIK:** 0000354950 · NYSE: HD · ISIN US4370761029
**Corpus:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/home-depot/` (frozen 2026-08-14; newest document 2026-05-21)
**Dossier date:** 16 August 2026

---

## 0. HAS IT REPORTED? — NO.

**Home Depot has NOT reported FY2026 Q2. It reports on Tuesday 18 August 2026, 9:00 a.m. ET** (14:00 UK) — i.e. **two days after** the 16 August 18:00 UK cut-off.

> "The Home Depot announced today that it will hold its Second Quarter Earnings Conference Call on Tuesday, August 18, at 9 a.m. ET."
> — [Home Depot IR press release, 4 August 2026](https://ir.homedepot.com/news-releases/2026/08-04-2026-130209919)

The newest document of any kind in the corpus is dated **2026-05-21** (AGM transcript). The newest *financial* disclosure is the **Q1 FY2026 8-K/10-Q of 2026-05-19**. There is **no** FY2026 Q2 data anywhere in the corpus or on the open web. Anything presented as a Q2 FY2026 "actual" would be fabricated.

### Corpus defects found (period labels)
The corpus INDEX mislabels several documents' fiscal periods. These are labelling errors only — the document bodies are correct and internally consistent:

| File | INDEX label | Actual content |
|---|---|---|
| `call-transcripts/2026-05-19__hd-us-20260519-call-qna__1039119.md` | "Q1 2027" | Q1 **FY2026** earnings-call Q&A (19 May 2026) |
| `call-transcripts/2026-05-21__hd-us-20260521-call-agm-qna__1042692.md` | "Q2 2027" | AGM Q&A, 21 May 2026 |
| `call-transcripts/2026-04-09__hd-us-20260409-call-conf-*` | "Q1 2027" | April 2026 Retail Round Up conference |
| `call-transcripts/2025-09-04__hd-us-20250904-call-conf-pres__144641.md` | "Q3 2026" | Sept 2025 fireside chat (post-Q2 FY2025) |
| `filings/2026-04-07__hd-us-20260407-filing__904273.md` | "FY 2026" | FY2025 proxy material |

No minus-sign stripping was detected in the HD 8-K/10-Q tables I used — negatives appear correctly as `(0.3)%`, `(1.3)%`, `(3.0)` etc. The one HD slide deck in the recent window (2025-12-09 Investor Conference) is almost entirely OCR'd image captions and contains no usable financial tables.

---

## 1. PRIOR-YEAR ACTUALS — the validation baseline (must be exact)

**FY2025 Q2: 13 weeks ended 3 August 2025** (reported 19 August 2025)

| Metric | Value | Source |
|---|---|---|
| **Net sales** | **$45,277 m** (USD 45.277 bn) | `filings/2025-08-19__hd-us-20250819-q2-8k__143666.md`, Condensed Consolidated Statements of Earnings; independently confirmed via SEC XBRL `RevenueFromContractWithCustomerExcludingAssessedTax`, period 2025-05-05→2025-08-03 = 45,277,000,000 |
| **Adjusted diluted EPS** | **$4.68** | Same 8-K, "Reconciliation of Adjusted Diluted Earnings Per Share": GAAP $4.58 + $0.14 acquired-intangible amortisation − $0.04 tax effect = **$4.68** |
| **Comparable sales, total company** | **+1.0 %** (POSITIVE) | Same 8-K, Selected sales data. U.S. comps +1.4 %. FX **negatively** impacted total-company comps by ~40 bps. |

Supporting Q2 FY2025 detail (all same 8-K / `call-transcripts/2025-08-19__hd-us-20250819-call-pres__143686.md`):

- Gross profit $15,125 m (33.41 %); total opex $8,570 m (18.93 %); operating income $6,555 m (14.48 %); adjusted operating income $6,694 m (14.78 %)
- Interest & other, net $550 m; tax rate 24.2 %; net earnings $4,551 m; diluted shares 994 m; GAAP EPS $4.58
- Acquired-intangible amortisation $139 m pre-tax (of which $87 m SRS)
- Comp transactions **−0.4 %**, comp average ticket **+1.4 %**; total transactions 446.8 m (−0.9 %), average ticket $90.01 (+1.2 %)
- Big-ticket comp transactions (>$1,000) **+2.6 %**; 12 of 16 merch departments positive
- Monthly comps: **May −0.3 %, June 0.0 %, July +3.1 %** (U.S.: +0.3 / +0.5 / +3.3)
- Pro and DIY comps both positive and "relatively in line with one another"; online comp +~12 %
- Management: "the performance across the business was the strongest we've seen in over two years"

> ⚠️ **This is the hardest quarterly compare of FY2026.** Q2 FY2025 (+1.0 %) is the highest comp HD printed in the prior nine quarters, and July 2025 alone was +3.1 %.

---

## 2. QUARTERLY HISTORY OF THE THREE TARGET METRICS

All from HD 8-K earnings releases in the corpus (`filings/*q2-8k*`, `*q1-8k*`, `*q3-8k*`, `*q4-8k*`). Adjusted EPS only exists from Q2 FY2024 onward (the non-GAAP measure was introduced with the SRS acquisition, June 2024).

| Fiscal period | Net sales (USDm) | Total-company comp % | GAAP dil. EPS | Adj. dil. EPS |
|---|---|---|---|---|
| FY2022 Q2 (ended 31-Jul-22) | 43,792 | +5.8 | 5.05 | n/a |
| FY2022 Q4 | 35,831 | −0.3 | 3.30 | n/a |
| FY2023 Q1 (30-Apr-23) | 37,257 | −4.5 | 3.82 | n/a |
| **FY2023 Q2 (30-Jul-23)** | **42,916** | **−2.0** | 4.65 | n/a |
| FY2023 Q3 (29-Oct-23) | 37,710 | −3.1 | 3.81 | n/a |
| FY2023 Q4 (28-Jan-24) | 34,786 | −3.5 | 2.82 | n/a |
| FY2024 Q1 (28-Apr-24) | 36,418 | −2.8 | 3.63 | n/a |
| **FY2024 Q2 (28-Jul-24)** | **43,175** | **−3.3** | 4.60 | **4.67** |
| FY2024 Q3 (27-Oct-24) | 40,217 | −1.3 | 3.67 | 3.78 |
| FY2024 Q4 (2-Feb-25, **14 wks**) | 39,704 | +0.8 | 3.02 | 3.13 |
| **FY2024 full year (53 wks)** | **159,514** | **−1.8** | 14.91 | 15.24 |
| FY2025 Q1 (4-May-25) | 39,856 | −0.3 | 3.45 | 3.56 |
| **FY2025 Q2 (3-Aug-25)** | **45,277** | **+1.0** | **4.58** | **4.68** |
| FY2025 Q3 (2-Nov-25) | 41,352 | +0.2 | 3.62 | 3.74 |
| FY2025 Q4 (1-Feb-26, 13 wks) | 38,198 | +0.4 | 2.58 | 2.72 |
| **FY2025 full year (52 wks)** | **164,683** | **+0.3** | 14.23 | 14.69 |
| FY2026 Q1 (3-May-26) | 41,765 | +0.6 | 3.30 | 3.43 |
| **FY2026 Q2 (2-Aug-26)** | **TARGET** | **TARGET** | — | **TARGET** |

### Monthly comp cadence (total company) — from earnings-call prepared remarks
| Quarter | M1 | M2 | M3 | Qtr | FX effect on comp |
|---|---|---|---|---|---|
| FY2025 Q1 | Feb −3.6 | Mar +0.6 | Apr +1.1 | −0.3 | −70 bp |
| FY2025 Q2 | May −0.3 | Jun 0.0 | **Jul +3.1** | +1.0 | −40 bp |
| FY2025 Q3 | Aug +2.0 | Sep +0.5 | Oct −1.5 | +0.2 | n/d |
| FY2025 Q4 | Nov −0.2 | Dec +0.1 | Jan +1.3 | +0.4 | n/d |
| FY2026 Q1 | Feb +0.7 | Mar +2.0 | Apr −0.5 | +0.6 | **+55 bp** |

### Ticket vs transaction split
| Quarter | Comp transactions % | Comp avg ticket % | Total transactions (m) | Avg ticket $ |
|---|---|---|---|---|
| FY2024 Q2 | −2.2 | −1.3 | 451.0 | 88.90 |
| FY2025 Q2 | **−0.4** | **+1.4** | **446.8** | **90.01** |
| FY2025 Q3 | −1.6 | +1.8 | 393.5 | 90.39 |
| FY2025 Q4 | −1.6 | +2.4 | 366.5 | 91.28 |
| FY2026 Q1 | −1.3 | +2.2 | 391.1 | 92.76 |

Transactions have been negative for eleven straight quarters; the entire comp is now ticket, driven by ~3 % of tariff-related price in the market plus mix. Note: transaction/ticket metrics **exclude HD Supply and SRS (incl. GMS)**, so they describe the store business only.

---

## 3. SEASONALITY OF Q2 (the biggest quarter)

| Fiscal year | Q2 / FY sales | Q2 / Q1 sales |
|---|---|---|
| FY2023 | 28.1 % | 1.152 |
| FY2024 | 27.1 % (53-wk yr) | 1.186 (1.150 ex-SRS) |
| FY2025 | 27.5 % | 1.136 |

Applying the FY2023–25 Q2/Q1 ratio (~1.14) to Q1 FY2026's $41,765 m gives **~$47.6 bn** before adding the incremental Mingledorff's contribution — a clean independent cross-check on the sales estimate below.

Q2 is also the highest-margin quarter (op margin 14.5 % in FY2025 vs 12.9 % in Q1 and 10.1 % in Q4) because of maximum fixed-cost leverage on spring/summer volume. Adjusted EPS in Q2 has been ~1.22–1.32× the same year's Q1.

---

## 4. WHAT THE COMPANY HAS GUIDED, AND ITS TRACK RECORD

### FY2026 guidance (given 24 Feb 2026, **reaffirmed unchanged** 19 May 2026)
- Total sales growth **+2.5 % to +4.5 %** → $168.8–172.1 bn (mid $170.5 bn)
- **Comparable sales growth approximately flat to +2.0 %**
- ~15 new stores; 40–50 new SRS locations
- Gross margin ~33.1 % (vs 33.32 % FY2025)
- Operating margin 12.4–12.6 %; **adjusted** operating margin 12.8–13.0 %
- Effective tax rate ~24.3 %; net interest expense ~$2.3 bn
- Diluted EPS and **adjusted** diluted EPS both **flat to +4.0 %** (from $14.23 GAAP / **$14.69 adjusted**) → adj EPS $14.69–15.28
- Capex ~2.5 % of sales
- Adjusted EPS guidance excludes **~$0.50 after-tax** of acquired-intangible amortisation for the year (~$0.125/quarter)
- SRS expected to deliver **mid-single-digit % organic** sales growth for the year

### Shape-of-year guidance — critical for Q2
- Richard McPhail (CFO), Q1 FY2026 Q&A: *"We are **not** looking at a marked improvement in underlying demand. We are looking at a higher comp in the second half of the year, and that is **solely driven by a return to normal storm activity**."*
- On gross margin: *"you're still gonna see pressure on a year-over-year basis in **Q2**, **not quite the degree that you saw in Q1**, and then improving significantly, more really sort of flattish year-over-year when you get into Q3 and Q4."* (Q1 GM was −77 bp YoY.)
- On costs: *"cost on the horizon … have at least moved towards a bias towards an increase"* (fuel, new tariffs), partly offset by unquantified tariff refunds.

### Guidance accuracy history
HD guides conservatively and has hit its own plan in 4 of the last 5 quarters ("in line with our expectations" language in Q1 FY2026, Q2 FY2025, Q4 FY2025 "largely in-line"). The one clear miss was **Q3 FY2025** ("Our results missed our expectations primarily due to the lack of storms"), which forced the only FY2025 guidance cut (comp from "+1.0 %" to "slightly positive"). FY2025 finished at +0.3 % comp — i.e. the original +1.0 % comp guide proved ~0.7 pp too high, and the initial adj-EPS guide (−2 %) landed at −3.6 %.

**Versus sell-side, HD has NOT been a reliable beat machine recently:** Q1 FY2026 adj EPS $3.43 vs ~$3.41 consensus (+0.6 %); Q2 FY2025 $4.68 vs ~$4.71 (small miss); Q3 FY2025 $3.74 was a clear miss. Do not apply a large "HD always beats" tilt.

---

## 5. CONSENSUS FOR FY2026 Q2

| Metric | Consensus | Source |
|---|---|---|
| **Net sales** | **$47.5 bn** (+4.9 % YoY) | Zacks, via [Yahoo Finance, 13 Aug 2026](https://finance.yahoo.com/markets/stocks/articles/ahead-home-depot-hd-q2-131502062.html) |
| **Adjusted diluted EPS** | **$4.71** (+0.6 % YoY); revised down 0.1 % over trailing 30 days | Same |
| Alternate read | Revenue ~$47 bn, adj EPS ~$4.73 | [TIKR, 9 Aug 2026](https://www.tikr.com/blog/home-depot-reports-q2-2026-earnings-on-august-18-can-it-finally-break-out) |
| Store count | 2,365 | Zacks / Yahoo, 13 Aug 2026 |
| Customer transactions | **439.99 m** (−1.5 % vs 446.8 m) | Zacks / Yahoo, 13 Aug 2026 |
| Average ticket | **$92.48** (+2.74 % vs $90.01) | Zacks / Yahoo, 13 Aug 2026 |
| **Comparable sales** | **No published consensus figure found.** | — |

### Deriving the implied consensus comp (two independent routes)
1. **From the Zacks store metrics.** Transactions −1.52 % × ticket +2.74 % → store (ex-SRS/HD Supply) sales +1.18 %. Backing out ~12 net new stores (~+0.3–0.4 pp of non-comp) gives comp store sales ≈ **+0.8 %**. SRS ex-GMS (≈6 % of company sales) is in the comp base with easing compares → total-company comp ≈ **+0.7 % to +0.9 %**.
2. **From the revenue line.** $47.5 bn − $45.277 bn = $2,223 m of growth. Non-comp build: GMS ~$1.40–1.50 bn + Mingledorff's ~$0.15–0.25 bn + new stores/SRS branches/tuck-ins ~$0.35–0.40 bn ≈ $1.95–2.10 bn, leaving ~$0.12–0.27 bn from comp = **+0.3 % to +0.6 %**.

**Working assumption: consensus comp ≈ +0.7 %** (range of reasonable reads +0.3 % to +0.9 %). Treat this as the number to be scored against.

---

## 6. THE DRIVERS

### 6.1 SRS / GMS / Mingledorff's — the inorganic bridge (biggest single sales swing factor)
- **SRS** acquired 18 Jun 2024; entered the comp base **late June 2025**. In Q1 FY2026 SRS (the "Other" reportable grouping) did **$4,002 m** of net sales vs $2,569 m a year earlier, with operating income of only **$16 m** (after $119 m of intangible amortisation) vs $87 m [`filings/2026-05-19__hd-us-20260519-q1-10q__1053121.md`, segment note].
- **GMS Inc.** acquired **4 Sep 2025** for **$5.1 bn** total consideration. Contribution history:
  - Q3 FY2025: **~$900 m** over ~8 weeks (~$112.5 m/wk)
  - Q4 FY2025: ~$1.1 bn implied (FY guide "GMS ~$2.0 bn incremental")  (~$85 m/wk, seasonal trough)
  - **Q1 FY2026: $1.3 bn** over 13 weeks (~$100 m/wk) — *explicitly stated* in the 10-Q MD&A
  - **Q2 FY2026 estimate: $1.40–1.55 bn**, since May–July is the seasonal peak for interior building products; use **~$1.45 bn**. GMS enters the comp base only in **September 2026**, so 100 % of it is non-comp in Q2.
- **Mingledorff's** (HVAC distributor, 42 branches, 5 SE states, Carrier-focused) closed **11 May 2026** — *eight days into fiscal Q2* and after the FY2026 guide was set. Terms and revenue **not disclosed**. Estimate **~$0.15–0.25 bn** of Q2 sales (peak HVAC season, ~12 of 13 weeks owned). **Many sell-side models will not carry this** — a small upward bias to the reported sales line vs consensus.
- Gross-margin consequence: GMS/SRS are lower-gross-margin distribution businesses. Richard McPhail attributed "the vast majority" of Q1's 77 bp GM decline to the GMS mix, and guided Q2 pressure to be smaller than Q1's.
- Cross-sell: **~$400 m run-rate this year**, expected to double next year (Ted Decker, Q1 FY2026 Q&A).
- SRS comps were **slightly negative** in Q1 FY2026 (low-single-digit negative in roofing). CFO: Q2 and Q3 of FY2025 "had some of the lowest recorded hail and hurricane storms in history", so SRS compares get materially easier from Q2 — supports a **positive SRS comp swing of maybe +0.1 to +0.3 pp** to total-company comp in Q2.

### 6.2 Comparable-sales trend and the compare problem
Two-year stacked comps (sum of current + year-ago):

| Quarter | Comp | Year-ago comp | 2-yr stack |
|---|---|---|---|
| FY2025 Q2 | +1.0 | −3.3 | −2.3 |
| FY2025 Q3 | +0.2 | −1.3 | −1.1 |
| FY2025 Q4 | +0.4 | +0.8 | +1.2 |
| FY2026 Q1 | +0.6 | −0.3 | **+0.3** |
| FY2026 Q2 | **?** | **+1.0** | ? |

Holding the Q1 FY2026 two-year stack flat implies a Q2 comp of **−0.7 %**. That is the bear case and it is a direct consequence of lapping the strongest quarter in two years.

### 6.3 External category data — the bull case (all three Q2 months now published)
FRED `RSBMGESD` — *Retail Sales: Building Material and Garden Equipment and Supplies Dealers*, seasonally adjusted, $m:

| Month | 2026 | YoY % | 2-yr % |
|---|---|---|---|
| Feb | 41,290 | +4.05 | +2.67 |
| Mar | 41,828 | +3.36 | +4.00 |
| Apr | 41,853 | +2.81 | +4.82 |
| **May** | **41,956** | **+5.73** | +4.44 |
| **Jun** | **42,456** | **+5.48** | +5.12 |
| **Jul** | **42,583** | **+6.69** | +4.05 |

- Category Q1 FY2026 (Feb–Apr): **+3.40 % YoY / +3.83 % 2-yr**
- Category Q2 FY2026 (May–Jul): **+5.97 % YoY / +4.54 % 2-yr**

So the category **accelerated ~2.6 pp on a 1-yr basis but only ~0.7 pp on a 2-yr basis**. The 2-yr read is the honest one because HD's own Q2 compare hardened by 1.3 pp. Applying the +0.71 pp two-year improvement to HD's Q1 two-year stack of +0.3 gives a Q2 stack of ~+1.0, i.e. a Q2 comp of **~0.0 %**. Applying the raw +2.6 pp one-year acceleration gives ~+3.2 %, which is not credible. The truth is in between, and closer to the 2-yr read.

Caveat: NAICS 444 includes pro lumber/building-material dealers who absorb more tariff-driven price inflation than HD, which is why HD *under*-performed the category by 2.8 pp in Q1 FY2026 after *out*-performing by 2.4 pp in Q2 FY2025. The spread is noisy; use the *direction of change*, not the level.

For reference, total retail ex-food-services (`RSXFS`) actually **fell** sequentially in July 2026 (660,047 vs 665,054 in June) — building materials outperformed broad retail in July.

### 6.4 Housing turnover, mortgage rates, big-ticket discretionary
| Series | Reading |
|---|---|
| 30-yr fixed mortgage (`MORTGAGE30US`) | 30-Apr-26 **6.30 %** → 30-Jul-26 **6.66 %** → 13-Aug-26 **6.67 %**. Rates **rose ~35 bp through the quarter**. |
| Existing home sales SAAR (`EXHOSLUSM495S`) | May 4.19 m, Jun 4.13 m, **Jul 4.06 m** — decelerating; still near 40-year lows |
| Housing starts (`HOUST`) | May 1,199 k (very weak), Jun 1,427 k — volatile; new construction "trending down" per management |

Management framing (Q1 FY2026, 19 May 2026):
- Ted Decker: *"housing turnovers remain low. Industry's not expecting a lot of growth in housing turnover this year, and new construction starts and sales are also trending down."*
- Billy Bastek: *"larger discretionary projects remain under pressure"* — the recurring drag is the **large cross-category project** funded by financing (kitchens, baths, flooring remodels). Big-ticket comp transactions (>$1,000) were only **+0.8 %** in Q1 FY2026, versus **+2.6 %** in Q2 FY2025.
- Michael Lasser (UBS) explicitly asked whether guidance should come down given "the rise in interest rates as well as the rise in energy prices"; management declined but conceded *"the environment is different than it was three months ago."*

### 6.5 Pro vs DIY
- Q1 FY2026: **Pro posted positive comps and outperformed DIY**; the highest-comping part of Pro was the "complex purchase occasion".
- Q2 FY2025 (the base): Pro and DIY both positive and *"relatively in line with one another"*.
- Pro initiatives compounding: Pro Trade Credit (30-day terms on shipment, expanding online and into e-procurement "within the second quarter"), Pro digital workspace, outside sales force >5,000, ~16,000 delivery assets, 1,300+ SRS branches.
- Online/digital comp: **+10 %** in Q1 FY2026 (fourth straight double-digit quarter); +12 % in Q2 FY2025.

### 6.6 Storms and weather
- Q1 FY2026 carried a **56 bp headwind** from lapping prior-year hurricane-recovery demand (Helene/Milton, autumn 2024). Billy Bastek: *"we did have 56 basis points of impact in Q1, but that'll dissipate throughout the balance of the year."* Estimate **~20–40 bp residual headwind in Q2**, going to a tailwind in H2.
- Weather in-quarter: management said May's first two weeks showed engagement *"very similar to the beginning of both February and March"* (i.e. roughly +0.7 % to +2.0 % comp territory) after a soft last-two-weeks-of-April. That is a genuinely encouraging real-time datapoint, but it covers only ~15 % of the quarter.

### 6.7 FX
| | Q1 FY2026 | Q2 FY2026 (est.) |
|---|---|---|
| CAD (USD/CAD avg YoY) | −3.4 % (CAD stronger) | **+1.6 % (CAD weaker)** |
| MXN (USD/MXN avg YoY) | −13.5 % (peso much stronger) | **−8.7 % (peso stronger)** |
| Reported/estimated FX effect on comp | **+55 bp (actual)** | **~+15 bp (estimate)** |

Calibrating my weightings to the reported +55 bp in Q1, Q2 FY2026 FX works out to roughly **+15 bp** — still a tailwind, but ~40 bp less helpful than Q1, and against a −40 bp FX drag in the year-ago Q2.

### 6.8 What "adjusted" means for HD
The **only** adjustment is **amortisation of acquired intangible assets**, including its tax effect. Nothing else — no restructuring, no acquisition costs, no one-offs. Definition (verbatim, Q1 FY2026 8-K):

> "The Company excludes the impact of amortization expense from acquired intangible assets from adjusted operating income and adjusted operating margin, and the impact of amortization expense from acquired intangible assets, including the related tax effects, from adjusted diluted earnings per share."

Amortisation run-rate: Q2 FY2025 $139 m pre-tax ($87 m SRS) → Q3 FY2025 $158 m → Q1 FY2026 **$171 m** ($119 m SRS/GMS, $52 m Primary). With Mingledorff's added, **~$175–185 m pre-tax in Q2 FY2026**, ≈ **$0.13–0.14 per share after tax**. FY2026 guidance assumes ~$0.50 after-tax for the year.
So: **Adjusted EPS ≈ GAAP EPS + ~$0.13.**

---

## 7. BUILD-UP TO THE FORECAST

### 7.1 Net sales
```
Q2 FY2025 base                                    45,277
+ GMS (100% non-comp; seasonal peak quarter)      ~1,450
+ Mingledorff's (~12 of 13 weeks owned)             ~200
+ new stores / new SRS branches / tuck-ins          ~380   (Q1 residual was ~370)
+ comparable-sales effect @ +0.6%                   ~272
--------------------------------------------------------
= Net sales                                       ~47,580
```
Cross-check A (seasonality): Q1 $41,765 × 1.14 Q2/Q1 ratio = $47.6 bn, plus Mingledorff's ≈ $47.6–47.8 bn.
Cross-check B (consensus): $47.5 bn.
Cross-check C (FY guide): FY2026 sales of $170.5 bn × 27.8 % Q2 share = $47.4 bn.

**Recommended: $47,600 m** — 0.2 % above consensus, the tilt coming from Mingledorff's (closed after guidance and after most models were set) and GMS's seasonal peak, partly offset by a slightly-below-consensus comp.

### 7.2 Comparable sales, total company
| Approach | Result |
|---|---|
| Two-year stack held flat from Q1 | **−0.7 %** |
| Two-year stack + category's +0.71 pp 2-yr improvement | **~0.0 %** |
| Q1 run-rate ex-February anomaly (Mar+Apr 2-yr avg +1.6) − LY +1.0 | **+0.6 %** |
| Implied sell-side consensus | **+0.7 % to +0.9 %** |
| Raw category YoY acceleration applied to HD | +3.2 % (not credible) |

Additive check: Q1 comp +0.6 %; adjustments to Q2 = FX −0.4 pp, storm-lap ~+0.2 pp (headwind shrinks), SRS comp swing +0.2 pp, harder underlying compare −0.3 to −0.6 pp, category momentum +0.3 to +0.5 pp → **+0.4 % to +0.9 %**.

**Recommended: +0.6 %** (POSITIVE — same as Q1, ~0.1–0.3 pp below implied consensus). Rationale: management explicitly said underlying demand is not improving before H2's storm normalisation, the compare is the hardest of the year, and the FX tailwind halves — but genuinely strong category prints for May/June/July and management's positive May commentary rule out anything materially negative. **Plausible range −0.5 % to +1.8 %.** U.S. comp will likely be within ~30 bp of total (FX makes total slightly higher than U.S. this year).

### 7.3 Adjusted diluted EPS
```
Net sales                                         47,600
Gross margin 32.9% (−50 bp YoY; Q1 was −77 bp)    15,660
Opex 19.0% of sales (+~10 bp YoY)                 (9,058)
Operating income                                   6,602   (13.87%, −61 bp)
Interest & other, net                               (580)
Pre-tax                                            6,022
Tax @ 24.3%                                       (1,463)
Net earnings                                       4,559
Diluted shares (no buybacks)                         996
GAAP diluted EPS                                   $4.58
+ intangible amortisation, after tax               $0.13
--------------------------------------------------------
Adjusted diluted EPS                               $4.71
```
Sensitivity: **each 10 bp of gross margin = ~$0.036 of EPS.** GM drag of −40 bp → $4.75; −65 bp → $4.66; −77 bp (same as Q1) → $4.62.

**Recommended: $4.70** — effectively consensus ($4.71), a hair below, reflecting (a) management's explicit warning that input costs "have moved towards a bias towards an increase" (fuel, new tariffs) with tariff refunds still "immaterial to date", (b) rising interest expense on a larger debt load, (c) HD's recent record of small misses rather than beats. **Plausible range $4.60 to $4.80.**

---

## 8. RECOMMENDED FORECASTS (units as specified)

| Metric | Unit | Prior-year actual | Consensus | **Recommendation** |
|---|---|---|---|---|
| Net sales | USDm | 45,277 | 47,500 | **47,600** |
| Adjusted diluted EPS | USD/share | 4.68 | 4.71 | **4.70** |
| Comparable sales, total company | percentage points | +1.0 | ~+0.7 (derived) | **+0.6** |

Units discipline: comp is **+0.6** meaning +0.6 %, not 0.006 and not 60. Sales in **millions** of USD. EPS in dollars per share, **adjusted** (GAAP + ~$0.13 of after-tax intangible amortisation).

---

## 9. RISKS TO THE FORECAST

1. **Comp sign risk.** The two-year-stack method points to 0.0 % or slightly negative. If July 2026 comp lapped the +3.1 % of July 2025 poorly, total comp could print negative and the whole street would be wrong in the same direction (which limits the scoring damage, but a below-consensus posture helps).
2. **Mingledorff's is an unmodelled sales wildcard.** Revenue undisclosed; my $200 m could be off by ±$100 m in either direction. It closed 8 days into the quarter and after the FY guide, so both HD's own guidance and most models exclude it.
3. **GMS seasonal shape is inferred, not disclosed.** I have three data points ($900 m/8 wks, ~$1.1 bn implied, $1.3 bn/13 wks) and I am extrapolating a summer peak. Wallboard/steel-framing price deflation and weak new-residential starts could hold GMS flat sequentially, costing ~$150 m of sales.
4. **Gross-margin uncertainty is the dominant EPS swing.** "Not quite the degree of Q1" is a soft guide spanning −40 to −70 bp; that is a $0.11 EPS range.
5. **Guidance-cut risk on 18 August.** Rising mortgage rates (6.30 → 6.67 %), softening existing-home sales (4.06 m in July), higher energy costs and new tariffs mean HD could trim the FY2026 comp guide to the low end. That does not change the Q2 print but will dominate the headlines.
6. **The corpus contains no post-May-2026 company data.** Everything about the June–July trading period comes from macro series, not from HD. Weight the FRED building-materials series accordingly — it is the single best in-quarter read available.

---

## Source index

**Corpus (all paths relative to `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/home-depot/`)**
- `filings/2026-05-19__hd-us-20260519-q1-8k__1038584.md` — Q1 FY2026 release, non-GAAP reconciliations, FY2026 guidance
- `filings/2026-05-19__hd-us-20260519-q1-10q__1053121.md` — GMS $1.3 bn contribution; segment detail; GMS purchase price $5.1 bn
- `call-transcripts/2026-05-19__hd-us-20260519-call-pres__1039117.md` — Q1 monthly comps, SRS/GMS commentary, FY outlook
- `call-transcripts/2026-05-19__hd-us-20260519-call-qna__1039119.md` — H2 storm-driven comp, Q2 GM guidance, SRS $4 bn, May trading, cross-sell $400 m
- `filings/2026-02-24__hd-us-20260224-q4-8k__615609.md` — FY2025 results and initial FY2026 guidance
- `filings/2025-11-18__hd-us-20251118-q3-8k__359994.md` — GMS ~$900 m/8 weeks; FY2025 guidance cut
- `filings/2025-08-19__hd-us-20250819-q2-8k__143666.md` — **prior-year actuals**
- `call-transcripts/2025-08-19__hd-us-20250819-call-pres__143686.md` — Q2 FY2025 monthly comps, ticket/transaction, Pro vs DIY
- `filings/2024-08-13__hd-us-20240813-q2-8k__101849.md`, `filings/2023-08-15__hd-us-20230815-q2-8k__101814.md` and earlier `*q2-8k*` — Q2 history

**External**
- SEC XBRL: `https://data.sec.gov/api/xbrl/companyconcept/CIK0000354950/us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax.json` (accessed 16 Aug 2026) — confirms Q2 FY2025 net sales $45,277 m
- [Home Depot IR, 4 Aug 2026 — Q2 earnings call set for 18 Aug 2026](https://ir.homedepot.com/news-releases/2026/08-04-2026-130209919)
- [Yahoo Finance / Zacks, 13 Aug 2026 — Q2 FY2026 consensus metrics](https://finance.yahoo.com/markets/stocks/articles/ahead-home-depot-hd-q2-131502062.html)
- [TIKR, 9 Aug 2026 — Q2 FY2026 preview](https://www.tikr.com/blog/home-depot-reports-q2-2026-earnings-on-august-18-can-it-finally-break-out)
- [Home Depot IR, 11 May 2026 — SRS completes Mingledorff's acquisition](https://ir.homedepot.com/news-releases/2026/05-11-2026-133053552) (terms undisclosed)
- FRED (accessed 16 Aug 2026): `RSBMGESD` / `MRTSSM444USS` (building-material retail sales, July 2026 available), `MORTGAGE30US`, `EXHOSLUSM495S`, `HOUST`, `RSXFS`, `DEXCAUS`, `DEXMXUS` — `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES_ID>`
