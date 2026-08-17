# Deere & Company (NYSE: DE) — FY2026 Q3 Consolidated Research Dossier

**Prepared:** 16 August 2026 · **Synthesis of 14 agent dossiers** (`01-…` through `14-…` in this directory)
**Corpus root for all relative paths:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`
**Corpus frozen:** 14 August 2026 · **Latest document in corpus:** Q2 FY2026 10-Q, 28 May 2026

---

## ⚠️ STATUS OF FY2026 Q3 — READ FIRST

**Deere has NOT reported FY2026 Q3. No FY2026 Q3 actuals exist in the corpus or anywhere on the public web
as of 16 August 2026. Every Q3 FY2026 figure in this document is a derived estimate or inference — never a
reported fact.**

Deere reports FY2026 Q3 on **Thursday 20 August 2026**, conference call 9:00 a.m. Central
(Deere press release 5 Aug 2026, reproduced at
https://www.stocktitan.net/news/DE/deere-to-announce-third-quarter-2026-financial-ws5vrthl5ifm.html and
https://www.nasdaq.com/press-release/deere-announce-third-quarter-2026-financial-results-2026-08-05).
The print lands **four days after this dossier**, so this is a genuine out-of-sample forecast.

**The metadata trap is confirmed and cleared — independently, by all fourteen agents.** The corpus
`INDEX.md` row `2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call Transcript` →
`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` is **mislabelled Q2 FY2026 material**.
Proof (strongest first):

1. Its **first line is verbatim identical to the last line** of the Q2 prepared-remarks file
   `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` ("…Our first question comes from
   Paddy Bogart from Melius Research"). It is the Q&A continuation of the 21 May Q2 call, split into a
   second file.
2. It discusses the **$272M IEEPA tariff refund recognised in the quarter** — a Q2 FY2026 event disclosed
   in `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` and the Q2 10-Q.
3. An analyst asks management to "talk us through **the cadence for 3Q and 4Q**" — Q3 is prospective.

This file is **legitimate, high-value Q2-dated evidence** (it carries the segment cadence guidance and the
tariff split) and is cited throughout as such. It is never cited as Q3 actuals.

---

## 1. EXECUTIVE SUMMARY

Deere enters FY2026 Q3 (≈4 May – 2 Aug 2026, a clean 13-week quarter against a clean 13-week comp) as a
company whose consolidated line has already turned while its largest segment has not. In Q2 FY2026 total
net sales and revenues rose 5% to **$13,369M** and diluted GAAP EPS was **$6.55**, yet Production &
Precision Ag net sales fell 14% and PPA operating profit fell 39% to **$706M**. Small Ag & Turf (+16% sales,
20.6% margin) and Construction & Forestry (+29% sales, 14.8% margin) are carrying the company. Management
calls FY2026 "the bottom of the ag cycle" with recovery in FY2027, and states that Large Ag is "operating
below trough levels" while C&F is "slightly above mid-cycle."

Four facts dominate the Q3 forecast.

**First, management pre-announced the H2 shape and it is unusual.** On 21 May the CFO said Deere expects
"slightly higher revenue in the back half, with the **fourth quarter being higher than the third quarter**"
and "our **most favorable cost comparisons in the fourth quarter**." For Large Ag, "Q4 a bit stronger than
Q3," because "more Waterloo large tractor shipments [are] shipping to North America in the back half than
the front half — **that's abnormal for us**." Q3 has beaten Q4 in FY2023, FY2024 and FY2025; FY2026 breaks
that pattern by design. Anyone applying normal seasonality will over-estimate Q3.

**Second, Q2 was flattered by a one-off.** A **$272M IEEPA tariff refund** (Supreme Court invalidated IEEPA
tariffs on 20 Feb 2026) was booked to cost of sales, **allocated 20% PPA / 30% SAT / 50% C&F**. PPA's clean
Q2 operating profit was ~$652M / 14.5%, not $706M / 15.7%. Guidance embeds **no further refund**, so any Q3
tranche is un-modelled upside — the single largest right-tail on the print.

**Third, guidance is unchanged and PPA guidance has never moved.** FY2026 net income $4.5–5.0bn (raised at
Q1, maintained at Q2). PPA has been guided "net sales down 5–10%, operating margin 11–13%" since November
2025 — every upgrade this year (SAT, C&F, Financial Services, tax rate) sat **outside** large ag.

**Fourth, guidance arithmetic and consensus disagree, materially.** FY guidance less H1 actuals implies H2
net income of $2,071–2,571M; with Q4 > Q3 that maps to Q3 EPS of roughly **$4.10–4.40**. Street consensus is
**$4.85–4.86**, which arithmetically requires either FY net income above the $5.0bn guidance ceiling or
Q4 < Q3 — directly contradicting management. Our central estimates sit deliberately between the two.

Macro during the window was "better crop prices, worse grower margins": corn +19.6% / soybeans +15.2% /
wheat +33.2% YoY, but AEM US ag tractor retail was **−17.3% across May–July** with 4WD −38.7% in July, the
Purdue Farm Capital Investment Index at cycle lows (41/40/50), and an Iran/Hormuz energy-and-fertiliser
shock. FX, which added ~2.7 points to Q2 sales, essentially vanishes in Q3 (+0.2% modelled).

---

## 2. THE THREE TARGETS

> **These are PRELIMINARY, evidence-based estimates, not final forecasts.** They are built from a single
> internally consistent chain: segment sales → total sales → segment operating profit → below-the-line
> items → EPS. Where the evidence does not support a tight range we have given a wide one and said so.

### 2.0 The build-up in one table

| Line ($M unless noted) | Q3 FY2025 actual | **Q3 FY2026 central** | YoY | Derivation |
|---|---:|---:|---:|---|
| PPA net sales | 4,273 | **3,880** | −9.2% | FY guide −5/−10% off $17,311M → H2 $7,914–8,779M; Q3 at 46–47% of H2 (below the 47.6% median because Waterloo is Q4-loaded) |
| Small Ag & Turf net sales | 3,025 | **3,350** | +10.7% | FY guide +15% → $11,758M; less H1 $5,653M = H2 $6,105M; Q3 at 55% (4-yr mean 54.4%; mgmt: "step down in Q3 and another step down in Q4") |
| Construction & Forestry net sales | 3,059 | **3,480** | +13.8% | FY guide +20% → $13,658M; less H1 $6,460M = H2 $7,198M; Q3 at 48.3% (4-yr mean 50.4%, cut for mgmt "a little stronger in Q4") |
| **Equipment operations net sales** | **10,357** | **10,710** | **+3.4%** | sum |
| Financial Services revenues | 1,418 | **1,400** | −1.3% | avg portfolio ~−1%, interest income −1.5% in Q2; FS revenue has run 1,384 / 1,366 in FY26 |
| Other revenues | 243 | **235** | −3.3% | FY26 running 226 / 225 |
| **(a) WORLDWIDE NET SALES AND REVENUES** | **12,018** | **≈ 12,350** | **+2.8%** | sum ($12,345M before rounding) |
| | | | | |
| PPA operating profit | 580 | **450** | −22.4% | see §2.3 — margin 11.6% |
| SAT operating profit | 485 | **490** | +1.0% | FY margin mid 14.25% → FY $1,676M; less H1 $916M = H2 $760M; Q3 at ~64% (Q4 is SAT's seasonally weakest margin quarter). Margin 14.6% vs 16.0% LY — no refund, ~⅓ of the $1.2bn tariff run-rate sits in SAT |
| C&F operating profit | 237 | **380** | +60.3% | FY margin mid 11% → FY $1,502M; less H1 $698M = H2 $804M; Q3 at ~47%. Margin 10.9% — cross-checks to Q2's **clean** 11.2% ex-refund |
| Financial Services operating profit | 266 | **265** | −0.4% | spread +7% on −71bp funding, offset by op-lease depreciation +10% |
| **Total operating profit** | **1,568** | **1,585** | **+1.1%** | sum |
| Reconciling items (corporate, certain interest, FX) | ~+84 (derived) | **+55** | | H1 FY26 +132; Q2 FY26 +54 |
| **Income before taxes** | ~1,652 | **1,640** | | |
| Effective tax rate | ~22% | **25.0%** | | FY guide 24–26%; H1 actual 22.8% ⇒ H2 must run 25–28%. Do **not** roll H1 forward |
| **Net income attributable to Deere** | **1,289** | **≈ 1,230** | **−4.6%** | |
| Diluted shares (M) | 271.4 | **270.0** | −0.5% | 270.8 in Q2 FY26; buyback ran only $193M / 326k shares in Q2 |
| **(b) DILUTED EPS (GAAP)** | **$4.75** | **≈ $4.55** | **−4.2%** | 1,230 ÷ 270.0 |

**Consistency check:** total operating profit is 12.8% of revenue vs 13.0% in Q3 FY2025 — margin down
slightly on *higher* revenue, which is exactly what the mix shift (PPA down, lower-margin C&F/SAT up) plus
the absence of the tariff refund should produce. Net margin falls from 10.7% to 10.0%, almost all of it the
tax rate. The three targets are one model, not three guesses.

---

### 2.1 (a) Worldwide net sales and revenues

| | Value | vs Q3 FY2025 ($12,018M) |
|---|---:|---:|
| **Low** | **$11,900M** | −1.0% |
| **CENTRAL** | **$12,350M** | **+2.8%** |
| **High** | **$12,800M** | +6.5% |

**Confidence: medium-high.** Revenue is the best-behaved of the three targets. Consensus revenue error has
a mean absolute error of ~3–4% (n=9), roughly a quarter of the EPS error, and segment net-sales consensus
was near-perfect last year (PPA $4.28bn estimated vs $4.273bn actual, −0.2%).

**Cross-checks on the central:**

| Method | Implied Q3 NSR | Note |
|---|---:|---|
| Bottom-up segment build (above) | $12,345M | primary |
| Q2 × 12-yr mean Q3÷Q2 ratio (0.935) | $12,500M | |
| Q2 × down-cycle mean (0.906) | $12,116M | FY2026 is a down-cycle year for PPA only |
| Q2 × last-3-yr mean (0.905) | $12,094M | |
| Implied ratio of our central | **0.924** | sits between down-cycle and all-year means ✓ |
| 26.08% of guidance-implied FY NSR (~$48.0bn) | $12,518M | the %-of-FY method points ~1.4% higher |
| Implied consensus (equipment $10.87bn + FS/other ~$1.62bn) | $12,400–12,500M | our central is ~1% below |

**Why we sit slightly below the implied consensus:** (i) the **FX translation tailwind collapses** — a
revenue-weighted model calibrated to within 0.1pt on Q2's actual +2.70pt gives **+0.18pt for Q3**, because
the euro laps the weakest-dollar months of 2025 (EUR +0.3% YoY vs +8.2% in Q2), the rupee is −10.2% and the
CAD flipped to −1.6%; only the real still helps. Deere's own +3.0% PPA FX guide was struck at ~20 May spot
(EUR ≈1.17) before the euro fell to a 1.1419 July average, so the company's H2 currency assumption looks
~2 points too high. (ii) AEM US retail was **−17.3% across the exact May–July window**, capping PPA volume.

**Basis warning (critical):** the widely quoted **$10.87bn Q3 "revenue consensus" is EQUIPMENT OPERATIONS
NET SALES, not worldwide net sales and revenues.** Arithmetically proven: $10,357M × 1.0495 = $10,870M
exactly, and Zacks' FY2026 $41.51bn at +6.66% implies an FY2025 base of $38.92bn = FY2025 *net sales*, not
the $45.68bn total. The gap has run $1,591–1,868M per quarter. Quoting a $12.4bn forecast against a
$10.87bn "consensus" would look like a 15% beat that never happened. **No named consensus for worldwide net
sales and revenues is published anywhere; the ~$12.5bn figure is our own bridge.**

---

### 2.2 (b) Diluted EPS (GAAP)

| | Value | vs Q3 FY2025 ($4.75) | Implied net income |
|---|---:|---:|---:|
| **Low** | **$3.70** | −22% | ~$1,000M |
| **CENTRAL** | **$4.55** | **−4.2%** | **~$1,230M** |
| **High** | **$5.40** | +14% | ~$1,460M |

**Confidence: medium.** Deere reports no adjusted EPS, so consensus EPS *is* GAAP — no bridge needed. But
the method dispersion here is the widest of the three targets and the range is genuinely wide.

**Every method, laid side by side:**

| Method | Implied Q3 EPS | Respects mgmt's "Q4 > Q3"? |
|---|---:|---|
| Guidance mid ($4.75bn) − H1, Q3 at 47% of H2 | $4.14 | yes |
| Guidance mid + historical Q2-stage beat (+2.1% ⇒ $4.85bn), Q3 at 47% | $4.26 | yes |
| **Bottom-up segment build (§2.0)** | **$4.55** | yes (implies Q4 op profit +2.5% over Q3) |
| Guidance top ($5.0bn), Q3 at 49% | $4.66 | yes |
| Consensus (Zacks/Barchart, Jul 2026) | $4.85–4.86 | **no** — implies Q4 < Q3 |
| Q2-ratio: **clean** Q2 NI ($1,568M ex-refund) × last-3-yr Q3÷Q2 NI ratio 0.829 | $4.81 | no |
| Consensus + Q3-only median historical beat (+$0.13) | $4.98 | no |
| Q2-ratio: clean Q2 NI × 12-yr Q3÷Q2 NI ratio 0.873 | $5.07 | no |
| Q2-ratio: **reported** Q2 NI ($1,773M) × 0.873 | $5.72 | no — double-counts the refund |

Median of the nine ≈ $4.66; mean ≈ $4.63. **We sit at $4.55, below both** — because the methods above the
central all rely on normal seasonality, and management explicitly and repeatedly told the market that
FY2026 H2 is *not* normally seasonal. That statement is the single most load-bearing piece of forward
evidence in the corpus, and it is worth more than a twelve-year ratio.

**Below-the-line sensitivities (the swing factors):**

| Input | Central | Sensitivity |
|---|---|---|
| Effective tax rate | 25.0% | at H1's 22.8% ⇒ **$4.69**; at 27% ⇒ **$4.43**. Worth ±$0.13 per point |
| Diluted shares | 270.0M | ±1M ⇒ ∓$0.02. **Not a swing factor** — buyback slowed to $193M in Q2 |
| Reconciling items | +$55M | ±$40M ⇒ ±$0.11 |
| Second IEEPA refund tranche | **$0 assumed** | a $200M tranche ⇒ **+$0.55**; a $272M repeat ⇒ **+$0.75** |
| Q3 share of H2 net income | 49.3% | 45% ⇒ $4.15; 53% ⇒ $4.89. **The largest single judgement** |

**Reconciling to the full year:** our Q3 of $1,230M plus H1's $2,429M plus a Q4 of ~$1,250M (respecting
Q4 > Q3 at the operating-profit line) gives **FY2026 net income ≈ $4.91bn** — upper-middle of the
$4.5–5.0bn guide, essentially on top of the Street's $4.88bn and the historical Q2-stage beat of +2.1%
($4.85bn). The chain is coherent from segment to full year.

---

### 2.3 (c) PPA operating profit

| | Value | Margin on $3,880M sales | vs Q3 FY2025 ($580M) |
|---|---:|---:|---:|
| **Low** | **$340M** | 8.8% | −41% |
| **CENTRAL** | **$450M** | **11.6%** | **−22%** |
| **High** | **$610M** | 15.7% | +5% |

**Confidence: medium-low, and the range is deliberately wide.** There is **no published PPA
operating-profit consensus anywhere** — six agents independently searched Zacks, Yahoo, AlphaQuery,
StockStory, TipRanks, Investing.com, MarketScreener, Visible Alpha, Simply Wall St, Quartr, Nasdaq and WSJ.
Segment operating-profit consensus is paywalled institutional data. There is no anchor to lean on or fade.
The number must be built bottom-up, and the methods disagree by nearly 2×.

**Every method at PPA net sales of ~$3,900M:**

| Method | Implied Q3 PPA OP | Character |
|---|---:|---|
| Delta regression ΔOP = 0.328×ΔSales − 165 (FY24–Q2'26) | $293M | most pessimistic |
| Delta regression ΔOP = 0.344×ΔSales − 133 (FY24–FY25, R²=0.90) | $319M | |
| Bottom-up eight-bucket bridge (below) | ~$355M | |
| Tariff-era levels model less mean recent residual (−$81M) | $409M | |
| FY guide midpoint margin 12% ± 1pt seasonal | $429–507M | |
| **Blend / CENTRAL** | **$450M** | |
| Guidance top-down: 40–48% of implied H2 OP $869–1,293M | $365–620M (mid ~$480M) | |
| Levels model OP = 0.360×S − 914 (FY25–Q2'26, tariff era) | $490M | |
| Levels model OP = 0.421×S − 1,125 (FY24–Q2'26, R²=0.91, SE $142M) | $517M | most optimistic |
| Q2 ratio: **clean** Q2 OP ($652M) × 6-yr mean Q3÷Q2 of 0.870 | $567M | |

**Our own bottom-up bridge from Q3 FY2025's $580M** (MY INFERENCE, using the reported eight-bucket format):

| Bucket | $M | Reasoning |
|---|---:|---|
| Q3 FY2025 actual | 580 | reported |
| Volume / Mix | −216 | Δsales −393; strip FX (+1% = +$43M) and price (+1% = +$43M) ⇒ volume-driven −$479M; × 45–47% decremental (median of six observed quarters: 47%) |
| Price | +43 | +1.0% guided, on the $4,273M prior-year base; price flows ~1-for-1 |
| Currency (profit bar) | 0 | the bar swung −$39M → +$75M between Q1 and Q2 FY26 on a *smaller* translation number, so it is export-transaction margin, not translation. With the broad dollar +1.2% YoY it evaporates. **Straight-lining Q2's +$75M is ~$75M too high** |
| Warranty | −15 | recurring: −$45M (Q3'25), −$48M (Q1'26), −$51M (Q2'26) — but the Q3'25 base already carried a drag |
| Production costs | −45 | PPA carries ~20% of tariffs; Q3 YoY enterprise tariff step is only ~$78M (vs ~$200M in Q2) ⇒ ~−$16M in PPA, possibly better after the 8 June 25%→15% equipment-tariff cut; plus ~$20–40M of lagged steel/material. Q3'25's bucket was a *favourable* +$69M, so the comp is hard |
| SA&G/R&D · Special · Other | +10 | Q3'25 carried Special +$34M and Other −$37M; assume partial non-repeat |
| **⇒ Q3 FY2026** | **~355** | 9.1% margin |

**The tension is real and we are not smoothing it.** The bottom-up bridge and the delta regressions land at
**$290–400M**; the levels regression and the reaffirmed FY guidance land at **$450–550M**. The reconciling
variable is Q4:

| If Q3 PPA OP = | then Q4 must be, for FY margin of… | FY2026 PPA margin |
|---|---|---|
| $355M | $512M (12.5% on ~$4.1bn) | **10.9% — below the 11% guidance floor** |
| $450M | $560M (13.7%) | 11.7% — inside |
| $490M | $590M (14.4%) | 12.2% — near the guide midpoint |

Deere **reaffirmed the 11–13% band on 21 May 2026 with H1 (11.0%) already booked**. That is a real
constraint and argues against the bottom-up bridge being right. We therefore weight guidance and the levels
model ~65% against the bridge/delta methods ~35%, which yields ~$450M. The honest read is that the true
distribution is bimodal-ish and wide.

**PPA-specific swing factors, in order of size:**
1. **A second IEEPA refund tranche.** CBP Phase 2 opened 29 June and Phase 3 late July 2026 — both *inside*
   Deere's fiscal Q3. Deere's Q2 language was narrow: "eligibility parameters established by the CBP for
   the **initial phase**." 20% of any tranche lands in PPA. Probability estimated at 30–40%; not in the base case.
2. **Mix.** Q3 FY2025 converted at a 70% volume/mix decremental (vs a 47% median) because the mix
   deteriorated — fewer Waterloo high-hp tractors and combines, more parts. Waterloo being Q4-loaded this
   year risks repeating that.
3. **The absent $54M.** Q2's 15.7% margin is ~1.2pts flattered. Extrapolating it extrapolates a one-off.

---

## 3. SEASONALITY AND GUIDANCE ANCHORS

### 3.1 Q3 as a share of the year and of Q2 — total net sales and revenues (FY2014–FY2025, n=12)

| Statistic | Mean | Median | Min | Max | Std dev |
|---|---:|---:|---:|---:|---:|
| **Q3 as % of full-year NSR** | **26.08%** | **26.22%** | 25.11% (FY2020) | 27.59% (FY2018) | 0.68 pp |
| **Q3 ÷ Q2 NSR** | **0.935** | **0.942** | 0.854 (FY2016) | 1.055 (FY2022) | 0.052 |
| Q3 ÷ Q1 | 1.286 | 1.253 | 1.079 | 1.491 | 0.122 |

Sub-samples of Q3 ÷ Q2: last 5 years **0.945**; last 3 years **0.905**; down-cycle years (FY2015/16/19/20/24/25)
**0.906**; up-cycle years 0.963.

**Q3 has been 25.1%–27.6% of the full fiscal year in every one of the last twelve years** — the tightest
ratio in the whole dataset. Applied to a guidance-implied FY2026 NSR of ~$48.0bn it gives $12.0–13.2bn,
centre $12.5bn. Applied to Q2's $13,369M, the Q3÷Q2 ratio gives $12.1–12.6bn. **Our central of $12,350M
implies a 0.924 ratio and a 25.7% share of a $48.0bn year — both inside the historical band, in the lower
half, which is where the guided Q4-weighting should put them.**

### 3.2 Segment-level Q3 seasonality (FY2020–FY2025)

| Segment / metric | Q3 ÷ Q2 mean / median / range | Last-3-yr mean | Q3 as % of H2 (median) |
|---|---|---:|---:|
| **PPA net sales** | 0.928 / 0.904 / 0.775–1.191 | **0.821** | 47.6% |
| **PPA operating profit** | 0.870 / 0.861 / 0.505–1.223 | **0.677** | 50.1% |
| SAT net sales | 0.956 / 0.943 / 0.902–1.018 | 0.957 | 54.4% (4-yr) |
| SAT operating profit | 1.005 / 0.884 / 0.845–1.491 | 0.859 | — |
| C&F net sales | 0.952 / 0.973 / 0.842–1.038 | 0.930 | 50.4% (4-yr) |
| C&F operating profit | 0.977 / 0.763 / 0.625–2.135 | 0.717 | — |
| Net income attributable to Deere | 0.873 / 0.834 / 0.715–1.218 | 0.829 | **55.6% mean / 55.7% median** |

**PPA is the most Q3-negative line in the business,** and getting worse: its Q3÷Q2 operating-profit ratio
has fallen every year since FY2022 (1.223 → 0.821 → 0.704 → 0.505). Our central implies 450 ÷ 706 = **0.637**
reported, or 450 ÷ 652 = **0.690** against the clean ex-refund Q2 base — between the FY2025 actual (0.505)
and the last-3-year mean (0.677).

### 3.3 What FY2026 guidance arithmetically implies for Q3

**Guidance in force (REPORTED FACT, `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`, 21 May 2026):**
net income **$4.5–5.0bn** (raised from $4.0–4.75bn at Q1, maintained at Q2); PPA net sales **down 5–10%**,
FX +3.0%, price ~+1.0%, margin **11–13%**; SAT **up ~15%**, margin 13.5–15%; C&F **up ~20%**, margin 10–12%;
Financial Services net income **~$860M**; effective tax rate **24–26%**; equipment-ops operating cash flow
$4.5–5.5bn; capex ~$1.4bn.

| Derived line | Low | Mid | High |
|---|---:|---:|---:|
| FY2026 PPA net sales (off $17,311M) | 15,580 | 16,013 | 16,445 |
| FY2026 PPA operating profit (11 / 12 / 13%) | 1,714 | 1,922 | 2,138 |
| less H1 FY2026 actual $845M ⇒ **H2 PPA OP** | **869** | **1,077** | **1,293** |
| ⇒ Q3 PPA OP at 40–48% of H2 | 365 | 480 | 620 |
| FY2026 total NSR (segment guides + FS ~$5.6bn + other ~$0.95bn) | 47.6bn | 48.0bn | 48.5bn |
| less H1 $22,981M ⇒ **H2 NSR** | 24.6bn | 25.0bn | 25.5bn |
| ⇒ Q3 NSR at 47–49.5% of H2 | 11.7bn | 12.2bn | 12.5bn |
| FY2026 net income guide | 4,500 | 4,750 | 5,000 |
| less H1 $2,429M ⇒ **H2 net income** | **2,071** | **2,321** | **2,571** |
| ⇒ Q3 net income at 46–50% of H2 | 953 | 1,114 | 1,286 |
| ⇒ Q3 diluted EPS at 270.0M shares | **$3.53** | **$4.13** | **$4.76** |

### 3.4 The Q3-share-of-H2 judgement — the single biggest error source

Historical Q3 share of H2 net income: FY2019 55.5%, FY2020 51.7%, FY2021 56.5%, **FY2022 45.6%**, FY2023
55.7%, FY2024 58.2%, FY2025 54.8% — **median 55.5%**. But **FY2022 is the only precedent year in which Q4 >
Q3, and it ran 45.6%.** Management has explicitly guided Q4 > Q3 for FY2026 on revenue, margin, price-cost
and large-ag absorption. A 45% vs 53% assumption swings Q3 EPS by ~$0.70. We use **49.3%**, which is above
the FY2022 precedent (because Deere's FY2026 Q4 loses a week — see below) and well below the median.

**The 53rd-week mechanic strengthens the Q4>Q3 signal.** FY2025 was a 53-week year with the extra week in
**Q4** (10-Q: "Fiscal year 2025 contained 53 weeks, with the additional week occurring in the fourth
quarter"). So:
- **Q3 FY2026 vs Q3 FY2025 is a clean 13-vs-13-week comparison** — no adjustment needed.
- Q4 FY2026 (13 weeks) faces a 14-week Q4 FY2025 — a ~7% week-count headwind on the Q4 YoY comp.
- FY2025's Q3 share of H2 revenue (49.2%) is *understated*; normalising FY2025 Q4 to 13 weeks lifts it to
  ~51%. Management's "Q4 higher than Q3" therefore has to overcome a lost week — **it is a stronger
  statement about Q4 volumes than it first appears, and a firmer signal that Q3 sits below 50% of H2.**

### 3.5 Guidance bias — how conservative is Deere, really?

Actual full-year net income vs the guidance midpoint at each stage, FY2015–FY2025 (n=11, all from corpus 8-Ks):

| Stage | Mean error | Median | Beat rate | Median ex-2016/2020 | Median FY2021–25 |
|---|---:|---:|---:|---:|---:|
| Initial (prior-yr Q4) | +11.0% | +0.7% | 5/10 | +0.7% | +5.6% |
| Q1 | +8.8% | +7.8% | 7/11 | +7.8% | +3.4% |
| **Q2 (the stage FY2026 is at)** | **+9.7%** | **+3.0%** | **8/11** | **+2.1%** | **+1.4%** |
| Q3 | +5.2% | +2.8% | **11/11** | +1.7% | +1.4% |

Deere is **reliably but only mildly conservative**, and the conservatism is concentrated at the Q3 update
(11/11 beats, +0.3% to +4.0% error in the last eight years). At the Q2 stage it is roughly unbiased with
three genuine small misses (FY2019 −1.4%, FY2022 −1.0%, FY2025 −1.9%). Applying the ex-anomaly Q2 median
beat of +1.4% to +2.1% to the $4.75bn midpoint gives **FY2026 net income ≈ $4.82–4.85bn** — which is where
our bottom-up chain lands ($4.91bn), and where consensus sits ($4.88bn).

**One 8/8 predictive rule worth knowing:** every year Deere *raised* the range at Q1 (FY2017/2021/2022/2023)
finished above the Q1 midpoint (+43.9 / +24.2 / +3.3 / +13.0%); every year it *held or cut* at Q1
(FY2019/2020/2024/2025) finished below (−9.6 / −5.1 / −6.9 / −4.2%). **FY2026 was raised at Q1** — up-revision
cohort. Counterweight: FY2021/22/23 all raised *again* at Q2, whereas FY2026 only held. FY2026 is a
**moderate** member of the up-revision cohort.

---

## 4. THE BULL CASE AND THE BEAR CASE

### 4.1 Bull case — what has to be true to reach the high end
**(NSR ~$12,800M · EPS ~$5.40 · PPA OP ~$610M)**

1. **A second IEEPA refund tranche is recognised in Q3.** This is the single largest lever and the cleanest
   path to the high end. CBP's CAPE Phase 2 opened 29 June and Phase 3 late July — both inside Deere's
   fiscal Q3. By 31 July, >75,000 declarations had been submitted and ~$128.68bn accepted for processing;
   $86.3bn had been repaid by 10 July. Deere called its $272M "this initial amount." Peers were still
   recognising refunds *after* Deere's 3 May close (AGCO $22M, Caterpillar ~$300M, Kubota, Amazon $640M).
   A $272M repeat is worth **~$0.75/share**, with ~$54M landing in PPA.
2. **C&F over-delivers again, as it has all year.** The order book is **up >60% since November 2025**,
   highest since April 2024, with **>80% of FY production slots filled**. Caterpillar's Construction
   Industries — the closest overlapping read-across, Apr–Jun 2026 — printed sales **+35%**, North America
   **+50%**, segment profit **+57%** at a 23.3% margin. United Rentals set a revenue record and **raised**
   FY guidance; Astec's backlog was +57.9%; the Dodge Momentum Index was +11.7% YoY in July. Deere has
   raised the C&F sales guide twice (10% → 15% → 20%) and the margin guide twice (8–10% → 9–11% → 10–12%).
   A third raise on 20 August is more likely than not.
3. **The 8 June equipment-tariff cut helps more than modelled.** Section 232 on select ag and construction
   equipment was cut **25% → 15%** effective 8 June 2026 through 31 Dec 2027, with a **10% preferential
   rate for ≥85% US-metal content** — and ~80% of Deere's US complete-good sales are US-built from ~75%
   US-sourced components. Deere's stock rose 4.3% on 3 June on the news. One third-party preview puts the
   benefit at $0.10–0.15 of FY2026 EPS; Deere has not quantified it. Combined with the tariff comp
   annualising (Q3 YoY step-up only ~$78M vs ~$200M in Q2), price-cost could turn positive earlier than Q4.
4. **The consensus-beat machine keeps running.** Deere beat GAAP EPS in **20 of the last 22 quarters**
   (median +$0.67), and the last two prints beat by +26.0% and +12.7% as analysts mis-modelled the
   C&F/SAT-strong, PPA-weak mix. Management is calling FY2026 the cycle bottom, and inflection years are
   historically when Deere blows through its range (FY2021 +8.4% vs the Q2 guide, FY2023 +8.4%).
5. **Deere's own tax guide is a free EPS tailwind** that the net-income range may not fully reflect: the
   effective rate was cut from 25–27% to 24–26% at Q2, and H1 actually ran 22.8%.
6. **The FY2016 rhyme.** FY2026 maps almost exactly onto FY2016 of the last downturn — identical "large ag
   down 15–20%" guide after an identical ~30% down-year. FY2016 Q3 delivered revenue −11% but **EPS $1.55
   vs $1.53, the first positive YoY EPS comp of that downturn**, on cost actions and easier comps.

### 4.2 Bear case — what has to be true to reach the low end
**(NSR ~$11,900M · EPS ~$3.70 · PPA OP ~$340M)**

1. **Take management literally.** "Q4 higher than Q3." "Most favorable cost comparisons in the fourth
   quarter." "Q4 a bit stronger than Q3" for Large Ag. "More Waterloo large tractor shipments in the back
   half — that's abnormal for us." "A little bit better absorption in the fourth quarter as production
   rates are significantly higher." At a 45–46% Q3 share of H2 net income and the guidance midpoint, Q3 EPS
   is **$3.97–4.06**; at the bottom of the range, **$3.53–3.62**.
2. **The PPA bridge, not the guidance, is right.** Two independent regressions (ΔOP = 0.344×ΔSales − 133,
   R²=0.90; and the tariff-era levels model less its −$81M mean residual) and a hand-built eight-bucket
   bridge all land PPA at **$290–410M**. The levels model has run **hot by a mean $81M over the last four
   quarters**. H1 PPA margin was 11.0% — at the *floor* of the 11–13% guide — and that guide has not been
   raised once all year while every other segment's has.
3. **Retail demand deteriorated inside the window.** AEM US total farm tractors: **May −21.6%, June −18.4%,
   July −10.9%; aggregated May–Jul −17.3%.** 4WD −38.7% in July, −24.6% YTD. 100+hp 2WD −15.5% YTD.
   Combines −10.2% YTD. Purdue Farm Capital Investment Index 41 / 40 / 50 — June was the lowest since
   September 2024. Tractor Supply and AEM independently flagged May as a rural air-pocket.
4. **Grower liquidity was in an air-pocket exactly during May–July.** The $11–12bn Farmer Bridge payment
   landed by 28 Feb 2026; the +$13.1bn ARC/PLC tranche does not pay until **October 2026**. Meanwhile the
   Iran/Hormuz shock pushed Brent from ~$76 to ~$126, diesel to $5.31/gal in late July, and the World Bank
   fertiliser index to its highest since October 2022 (urea +80% since February). Southern Ag Today's
   May-2026 analysis found 2026 breakeven yields exceed projected national average yields for **both** corn
   and soybeans despite the better price deck.
5. **South America was cut hard, and global forestry too.** South America tractors & combines went from
   "down ~5%" to **"down ~15%"** at Q2 — the largest negative revision of the year — and Deere is
   deliberately **underproducing Brazilian combines in Q2 and Q3**. Global forestry was cut from flat to
   down ~5%.
6. **CNH's warning is the sharpest peer signal.** CNH's North America agriculture sales were +10% in
   Apr–Jun 2026 **but with "unfavorable product mix with weaker large tractor sales relative to smaller
   models,"** and its Ag adjusted EBIT margin collapsed to **5.2% from 8.1%**. The NA recovery is small and
   mid horsepower — Deere SAT, not Deere PPA. Do not let AGCO's headline NA +19.7% pull PPA up.
7. **The tax rate bites.** H1 ran 22.8%; the FY guide of 24–26% requires H2 at ~25–28%. At 27%, EPS is
   $4.43 before anything else goes wrong.
8. **FX stops helping.** Q2's ~+2.7pt / ~$300M translation tailwind falls to ~+0.2pt / ~$20M, and the PPA
   operating-profit "Currency" bar goes from **+$75M to ~$0M**.

---

## 5. CONTRADICTIONS AND OPEN QUESTIONS

**Flagging weak spots honestly is more useful than papering over them. Here are ours.**

### 5.1 The central contradiction: guidance arithmetic vs consensus (~$0.60–0.70 of EPS)

Guidance less H1 actuals, with Q4 > Q3, gives Q3 EPS of **$4.10–4.40**. Consensus is **$4.85–4.86**. Three
agents showed independently that $4.85 × 270.8M = ~$1.31bn of Q3 net income leaves only $0.76–1.26bn for
Q4 against a $4.5–5.0bn FY guide — **i.e. consensus implicitly requires Q4 < Q3, contradicting management's
explicit statement**, or a full-year outcome of ~$5.1bn, above the guidance ceiling. Either the Street is
underwriting a beat-and-raise (the gap of ~$190M of net income is suspiciously close to a second IEEPA
tranche after tax), or it has the Q3/Q4 split backwards. **We cannot resolve this from available evidence.**
We split the difference at $4.55, closer to the guidance camp. This is the largest single source of error in
the whole dossier.

### 5.2 The PPA method split (~$200M, i.e. ~45% of the central)

- Bridge + delta regressions: **$290–410M**
- Levels regression + guidance top-down: **$450–550M**

The reconciling variable is Q4. If Q3 = $355M, FY2026 PPA margin lands at ~10.9% — *below* the 11% floor
Deere reaffirmed on 21 May with H1 already in hand. That is the strongest argument the bridge is too
pessimistic. But the levels model has run hot by $81M/quarter recently, and PPA guidance is the one guide
Deere has never raised. **Genuine ambiguity; the wide $340–610M range is the honest expression of it.**

### 5.3 Agent-level disagreements, itemised

| Question | Positions taken | Our resolution |
|---|---|---|
| Q3 GAAP EPS central | 02: $4.25 · 05: $4.10 · 12: $3.65–4.65 · 03: $4.29 · 13: $4.87 · 07: $5.15–5.30 · 01: $4.50–5.30 | **$4.55.** Agents 02/05/12 weight management's cadence; 07 weights the beat history; 13 builds from segment margins at guidance midpoints. All are defensible |
| Q3 PPA operating profit | 04: $450M · 02: $480M · 05: $490M · 13: ~$495M · 06: $500M · 09: $460–540M · 03: $480–540M | **$450M** — the low end of the cluster, because agent 04's bridge and delta work is the most granular and is the most pessimistic |
| Q3 total NSR | 02: $12.1bn · 03: $12.1–12.3bn · 05: $12.3bn · 13: $12.4bn · 01: $12.4bn · 06/07/12: $12.4–12.9bn (consensus-anchored) | **$12.35bn** |
| Should the historical beat be applied to consensus? | 07 says yes at half strength (+$0.30–0.45 ⇒ $5.15–5.30); 02/05/12 say the guidance ceiling voids it | **Mostly no.** Agent 07's own data shows Q3 is Deere's *weakest* beat quarter (median +$0.13 across 11 Q3s, vs +$0.67 all-quarter), all three clean-comparison misses of the decade were Q3s, and consensus already sits at the top of the guide |
| Do peers point PPA up? | 09's regressions imply PPA sales of $4.3–4.7bn, $300–700M **above** the guide-implied path | **Discount heavily.** Residual σ is 12–21pp on a 15-quarter sample spanning one violent drawdown; and CNH explicitly said the NA recovery is *small* horsepower. Use only as evidence the low end of the guide is unlikely |

### 5.4 Evidence that is thin, unverified or internally inconsistent

- **No PPA (or any segment) operating-profit consensus exists publicly.** Nothing to calibrate against.
- **No published worldwide-net-sales-and-revenues consensus.** The ~$12.5bn figure is our own bridge from an
  equipment-net-sales consensus. Consensus dispersion (high/low, analyst count) could not be retrieved for
  any Q3 FY2026 metric — Zacks, Yahoo analysis, TipRanks, MarketScreener, Seeking Alpha, WSJ all bot-blocked
  or paywalled. Only one individual broker datapoint was recovered ($5.03, Zacks Research M. Das, 24 Jun 2026).
- **AEM YTD unit counts are internally inconsistent** between the June report (103,123 YTD) and the July
  report (105,185 YTD, implying only ~2,062 July units against a stated 15,985). Use monthly YoY
  percentages, not YTD levels. July category-level month units for 40–100hp and 100+hp were unobtainable
  (globenewswire and aem.org returned 403/timeout).
- **Deere's used-combine inventory data contradicts itself:** Nov 2025 said "nearly 25% decrease from their
  spring 2024 peak," May 2026 said "down by mid-teens from their March 2024 peak." Direction of travel
  conflicts. The tractor / sprayer / planter figures are internally consistent; the combine figure is not.
- **PPA's share of ongoing tariff cost is not disclosed.** We use the disclosed 20% refund-allocation key as
  a proxy. It back-tests acceptably against the Q1 FY26 bridge, but it is an inference.
- **The quarterly split of FY2025's ~$600M tariff cost is not disclosed** — inferred as ~$200M Q3 / ~$305M
  Q4 from "$95M in H1 FY2025" plus "beginning in the third quarter of 2025." This drives the size of the
  Q3 FY2026 production-cost comp.
- **Deere has never disclosed steel tonnage or spend.** The 10%-HRC sensitivity ($150–250M/yr enterprise) is
  a back-solve from the 2018 and 2022 episodes, not a company figure. The Nov-2024→Apr-2025 HRC average
  (the lagged base) is the weakest data point in the whole dossier: published quotes range $690–$904, and
  using $860 instead of $800 cuts the lagged YoY steel inflation from ~+18% to ~+10%.
- **PPA net sales by geography is not disclosed at segment level** anywhere, limiting FX precision.
- **The Q2 slide's April-2026 AEM retail table lost its up/down direction markers in conversion.**
- **The Nov-2025 8-K rendered PPA net-sales guidance as a bare "10%"** with the direction word lost;
  resolved as "down 5–10%" from the slide deck, but the primary-text ambiguity is unresolved.
- **Four PPA operating-profit waterfalls (Q4 FY22, Q1 FY23, Q2 FY23, Q2 FY24) could not be reconstructed**
  from the OCR'd decks and were omitted rather than guessed. Bucket *labels* on the 12 extracted bridges are
  inferred from Deere's fixed eight-bucket order; the values are reported and each row's arithmetic verified.
- **FY24/FY25 10-K full-year PPA operating-profit rows ($1,532M / $1,673M) do not reconcile** to the sum of
  the quarterly segment tables (~$2,670M for FY25) and appear to be a different line item. Not used.
- **PPA history begins in FY2020** (Smart Industrial reorganisation), so PPA seasonality rests on only six
  observations and **no PPA series covers the 2013–2016 downturn** — cross-cycle PPA comparison is
  structurally impossible.
- **Search contamination hazard.** An 11 Aug 2025 Yahoo article ("Curious about Deere Q3 Performance…")
  ranks highly for FY2026 queries but contains **FY2025** estimates ($4.62 EPS, $10.26bn revenue, PPA net
  sales $4.28bn). MarketBeat's "$4.75" Q3 consensus is a stale copy of the year-ago actual. StockAnalysis's
  "FY2026 revenue $41.42B, down 9.23%" has the growth sign wrong (basis mismatch). A "$5.71 next-quarter
  EPS, range $5.33–6.20" figure matches no Q3 source and is probably Q4. **All discarded.**

### 5.5 Genuinely unknowable before the print

1. **Whether a second IEEPA refund tranche was booked in Q3.** No Deere disclosure either way. ~30–40% odds.
   Worth ~$0.75/share and ~$54M of PPA operating profit per $272M.
2. **Q3-to-date order book, retail settlements and May–July dealer inventory.** The most recent Deere-published
   figures anywhere are as of the Q2 close (3 May 2026).
3. **Zero management commentary between 21 May and 16 August 2026.** Verified against the complete EDGAR
   filing list (CIK 315189) and the newsroom: no guidance update, pre-announcement, Reg FD 8-K, or investor
   conference. Post-freeze filings are all non-financial (director not standing for re-election, routine
   S-3ASR shelf, a $300M Deere Funding Canada note, one Form 144). **This is a confirmed information vacuum,
   not a search failure.** A 26 Jun 2026 Simply Wall St piece claiming a June guidance raise is unsupported
   and recycles the February Q1 raise — refuted.
4. **MY2027 spring early-order-programme take rates.** Sprayer EOPs opened early May and close end-August;
   planters opened early June. Q3 will be the first quarter carrying real MY2027 data — the highest-information
   *forward* item to expect from the 20 August call, but not knowable now.

---

## 6. EVIDENCE LEDGER

Corpus paths are relative to `challenge/offline-data/deere/`. Web sources carry full URL and publication date.

### 6.1 Reported facts — the anchors

| # | Figure | Value | Source |
|---|---|---|---|
| 1 | Q3 FY2025 worldwide net sales and revenues | **$12,018M** | `filings/2025-08-15__de-us-20250815-q3-8k__143410.md` |
| 2 | Q3 FY2025 equipment net sales | $10,357M (PPA 4,273 / SAT 3,025 / C&F 3,059) | same |
| 3 | Q3 FY2025 diluted GAAP EPS / net income / diluted shares | **$4.75** / $1,289M / 271.4M | same |
| 4 | Q3 FY2025 PPA net sales / operating profit / margin | **$4,273M / $580M / 13.6%** | same |
| 5 | Q3 FY2025 SAT / C&F / FS operating profit | $485M / $237M / $266M | same |
| 6 | Q3 FY2025 FS revenues / other revenues | $1,418M / $243M | same |
| 7 | Q2 FY2026 worldwide net sales and revenues | **$13,369M (+5%)** | `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` |
| 8 | Q2 FY2026 diluted GAAP EPS / net income / diluted shares | **$6.55 (−1%)** / $1,773M / 270.8M | same |
| 9 | Q2 FY2026 PPA net sales / operating profit / margin | **$4,503M (−14%) / $706M (−39%) / 15.7%** | same |
| 10 | Q2 FY2026 SAT / C&F / FS operating profit | $719M / $561M / $251M; total OP $2,237M | same |
| 11 | H1 FY2026 NS&R / net income / EPS | $22,981M (+8.0%) / $2,429M (−9.1%) / $8.97 | same |
| 12 | H1 FY2026 PPA net sales / operating profit / margin | $7,666M / $845M / **11.0%** | same + Q1 8-K |
| 13 | FY2026 net income guidance, maintained 21 May 2026 | **$4.5–5.0bn** (raised from $4.0–4.75bn at Q1) | same, verbatim "Net income guidance maintained" |
| 14 | FY2026 PPA guidance, **unchanged since Nov 2025** | net sales **down 5–10%**; FX +3.0%; price ~+1.0%; **margin 11–13%** | same + `slides/2026-05-21__de-us-20260521-slide__1042212.md` |
| 15 | FY2026 SAT / C&F guidance | SAT up ~15%, margin 13.5–15%; C&F up ~20%, margin 10–12% | same |
| 16 | FY2026 FS net income / tax rate guidance | ~$860M (raised from $830M→$840M); tax **24–26%** (cut from 25–27%) | same |
| 17 | FY2025 actual bases | Total NSR $45,684M; PPA $17,311M / $2,671M (15.4%); SAT $10,224M / $1,207M; C&F $11,382M / $1,028M; FY EPS $18.50 | `filings/2025-11-26__de-us-20251126-q4-8k__361233.md` |
| 18 | **$272M IEEPA tariff refund**, allocated **20% PPA / 30% SAT / 50% C&F**, decreasing cost of sales | $272M (~$54M PPA, ~$82M SAT, ~$136M C&F); lifted equipment-ops margin ~2.5 pts | `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` L1880; `call-transcripts/2026-05-21__…call-qna__1042775.md` L29 |
| 19 | FY2026 tariff run-rate | **~$1.2bn gross (~3 pts of margin), ~$900M net** of the refund; split ~45% C&F / ~33% SAT / **~20% large ag** | `call-transcripts/2026-05-21__…call-pres__1042774.md` L85; `…call-qna__1042775.md` L27 |
| 20 | Tariff cost series | FY2025 ~$600M (~$200M in Q3 FY25, started Q3 FY25, ~$95M in H1 FY25); H1 FY26 $372M net / ~$644M gross | `filings/2026-05-28__…q2-10q__1055932.md` L1878; FY25 10-K |
| 21 | Q2 FY2026 YoY direct tariff headwind, ex-refund | ~$200M | `call-transcripts/2026-05-21__…call-pres__1042774.md` L81 |
| 22 | **Fiscal calendar:** FY2025 had 53 weeks, extra week in **Q4**; Q3 FY26 vs Q3 FY25 both 13 weeks | clean Q3 comp; Q4 FY26 faces a week-count headwind | `filings/2026-05-28__…q2-10q__1055932.md` L400 |
| 23 | **H2 cadence, verbatim** | "slightly higher revenue in the back half, with the **fourth quarter being higher than the third quarter**… **most favorable cost comparisons in the fourth quarter**" | `call-transcripts/2026-05-21__…call-pres__1042774.md` L143 |
| 24 | **Segment cadence, verbatim** | Large Ag "**Q4 a bit stronger than Q3**… more Waterloo large tractor shipments… **abnormal for us**"; SAT "step down in Q3 and another step down in Q4"; C&F "fairly balanced… maybe a little bit stronger in Q4" | `call-transcripts/2026-05-21__…call-qna__1042775.md` L95–97 |
| 25 | Q4 absorption | "large ag factories… **better absorption in the fourth quarter as production rates are significantly higher**" | same, L125 |
| 26 | Cycle position | "2026 will represent the **bottom of the ag cycle**"; "Large Ag is operating **below trough levels**, Small Ag & Turf is progressing towards mid-cycle, and Construction & Forestry is **slightly above mid-cycle**" | `call-transcripts/2026-05-21__…call-pres__1042774.md` |
| 27 | C&F order book | **up >60% since November 2025**, highest since April 2024; **>80% of FY production slots filled** | same, L115 |
| 28 | New field inventory, NA large ag | HHP tractors and combines **down >50% from the mid-2024 peak**; inventory-to-sales in line with historical averages | same, L123 |
| 29 | Used inventory | MY22–23 8R tractors **−45%** from last year's peak; sprayers −30%; planters −50%; JDF trade-wholesale portfolio **−15%+** | same, L125–127; `…call-qna__1042775.md` L137 |
| 30 | Dealer inventory (Deere, US&C ag, % of trailing-12m retail) | 2WD 100+ PTO hp: 30% (31% LY); combines: **12% (17% LY)** | `slides/2026-05-21__…slide__1042212.md` L193–198 |
| 31 | Brazil / Europe production plan | Brazil: **underproduce retail, most notably combines** (Q2 and Q3); Europe aligned with retail; order visibility "through the third quarter and into the fourth" | `call-transcripts/2026-05-21__…call-pres__1042774.md` L133; Q1 call L67 |
| 32 | Industry outlook cuts at Q2 | **South America tractors & combines: down ~5% → down ~15%**; global forestry: flat → down ~5%; global roadbuilding: +5% → +10% | `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` |
| 33 | Buyback / shares outstanding | Q2 FY26 repurchases only $193M / 326k shares; H1 $496M; $7.4bn left of $18bn; 269,937,425 shares outstanding at 3 May 2026 | `filings/2026-05-28__…q2-10q__1055932.md` L94, L2634–2641 |
| 34 | Q2 FY2026 effective tax rate | **22.6%** (H1 22.8%) — below the 24–26% FY guide | `filings/2026-05-28__…q2-10q__1055932.md` L1982 |
| 35 | FS credit quality (3 May 2026 vs 27 Apr 2025) | 30+ past due **1.70% vs 1.73%**; past-due + non-performing 3.48% vs 3.47%; H1 provision $127M vs $163M | `filings/2026-05-21__de-us-20260521-q2-10q__1055929.md` |
| 36 | Q3 FY2026 earnings date | **Thursday 20 August 2026, 9:00 a.m. CT**, before US market open | Deere PR 5 Aug 2026 — https://www.stocktitan.net/news/DE/deere-to-announce-third-quarter-2026-financial-ws5vrthl5ifm.html ; https://www.nasdaq.com/press-release/deere-announce-third-quarter-2026-financial-results-2026-08-05 |
| 37 | Deere WARN layoff notices filed in calendar 2026 | **zero** (most recent 17 Sep 2025); instead **~245 workers recalled** Jan–Feb 2026 (Davenport 75, Dubuque 24, Waterloo 146) for 8R production | https://warnact.io/company-john-deere ; https://cbs2iowa.com (6 Feb 2026) |
| 38 | UAW contract | master agreement (~7,600 workers) runs to **1 Nov 2027**; the live extension dispute votes **23 Aug 2026** — after the print. **Zero Q3 strike risk** | `filings/2025-11-26__…q4-10k__469216.md` L441; Jacobin 12 Aug 2026; KTIV 1 Aug 2026 |
| 39 | FTC right-to-repair suit **settled 8 July 2026** | 10-year dealer-equivalent repair obligation; only $1m to states' legal costs. The separate $99m class settlement was **already accrued in Q4 FY2025**. **Neither produces a Q3 charge** | https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-states-secure-settlement-deere-company-advancing-farmers-right-repair ; Q2 10-Q L1459 |
| 40 | Section 232 on ag/construction equipment cut **25% → 15%**, effective 8 Jun 2026 – 31 Dec 2027; 10% rate for ≥85% US-metal content. DE +4.3% on 3 Jun 2026 | not quantified by Deere | https://www.aem.org/news/section-232-tariff-changes-what-manufacturers-need-to-know ; https://www.investing.com/news/stock-market-news/deere-stock-jumps-on-tariff-cut-for-farm-equipment-93CH-4722460 (3 Jun 2026) |
| 41 | CBP IEEPA refund **Phase 2 opened 29 Jun 2026**, Phase 3 late July; >75,000 declarations, ~$128.68bn accepted by 31 Jul; $86.3bn repaid by 10 Jul | both phases fall inside Deere's fiscal Q3 | https://www.thompsonhinesmartrade.com/2026/06/cbp-confirms-june-29-2026-ieepa-tariff-refund-process-phase-2-launch/ ; https://www.cato.org/blog/ieepa-refunds-update-good-progress-still-ways-go |

### 6.2 External estimates and third-party data

| # | Figure | Value | Source (URL, date) |
|---|---|---|---|
| 42 | Q3 FY2026 consensus GAAP diluted EPS | **$4.85–$4.86** (+2.1–2.3% YoY) | Barchart via Yahoo, 23 Jul 2026 — https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html ; Zacks via Yahoo, 28 Jul 2026 — https://finance.yahoo.com/markets/stocks/articles/know-beyond-why-deere-company-130006540.html |
| 43 | Q3 FY2026 consensus revenue — **EQUIPMENT NET SALES basis** | **$10.87bn** (+4.95%) | Zacks via Yahoo, 28 Jul 2026 |
| 44 | Consensus EPS revision | Q3 FY26 EPS **$5.13 on 21 May → $4.85 by 23 Jul (−5.3%)**, then +0.9% over the 30 days to 28 Jul | Zacks via Yahoo (21 May 2026 Q2 recap; 28 Jul 2026) |
| 45 | FY2026 consensus | EPS $18.26–18.28 (StockAnalysis 15-analyst panel: $18.05); net income **$4.88bn** | https://stockanalysis.com/stocks/de/forecast/ (16 Aug 2026); Zacks via Yahoo (28 Jul 2026) |
| 46 | Q2 FY2026 surprise (calibration) | EPS $6.55 vs $5.70–5.81 consensus = **+12.7% to +14.9%**; total-revenue basis $13.369bn vs $13.05bn = **+2.4%** | MarketBeat; StockStory 21 May 2026 |
| 47 | EPS surprise history, last 22 quarters (FY21Q1–FY26Q2) | **20 beats / 22**; median **+12.65% / +$0.665**; σ $0.575 | AlphaQuery https://www.alphaquery.com/stock/DE/earnings-history × corpus 8-K actuals, computed 16 Aug 2026 |
| 48 | **Q3-only** EPS surprise, 11 Q3s FY2015–FY2025 | 8 beats / 11; mean +$0.43 but **median only +$0.13 (+4.1%)**; σ $0.735. All three clean-comparison misses of the decade were Q3s | same |
| 49 | Revenue surprise history (n=9) | 8 beats / 1 miss; mean +1.8%, median +3.0%, **MAE 4.9%** (3.8% ex-outlier) — 3–4× more accurate than EPS | Zacks / MarketBeat / StockStory × corpus |
| 50 | **AEM US ag retail, Deere's exact FQ3 window** | May 2026 total tractors **−21.6%**; June **−18.4%**; July **−10.9%** (15,985 units). **Aggregated May–Jul −17.3%.** 4WD −38.7% in July, −24.6% YTD; 100+hp 2WD −15.5% YTD; combines −10.2% YTD | AEM May 2026 PDF (aem.org); AEM June report GlobeNewswire 10 Jul 2026; AEM July report GlobeNewswire 11 Aug 2026 via https://www.rfdtv.com/farm-equipment-sales-remain-weak-through-july-2026 |
| 51 | Canada 100+hp 2WD, July 2026 | **+4.9% in month, +6.2% YTD** — the only positive large-tractor retail series in North America | same |
| 52 | Purdue/CME Farm Capital Investment Index | **41 (May), 40 (Jun — lowest since Sep 2024), 50 (Jul)**; Barometer 119/113/126 vs 158/146 a year earlier | https://ag.purdue.edu/commercialag/ageconomybarometer/after-3-months-of-decline-farmer-sentiment-rebounds-in-july/ (4 Aug 2026) |
| 53 | Crop prices, 14 Aug 2026 | Corn 459.00 ¢/bu **+19.6% YoY**; soybeans 1,177.75 **+15.2%**; wheat 674.75 **+33.2%** | https://tradingeconomics.com/commodity/corn (and /soybeans, /wheat), accessed 16 Aug 2026 |
| 54 | US net farm income 2026F | $153.4bn (−0.7% nominal) but **$44.3bn (29%) is government payments**; ex-payments $109.1bn, ~−12%. USDA cut its 2025 estimate from $179.8bn to $154.6bn (−14%) in Feb 2026 | USDA ERS 5 Feb 2026 via https://www.ers.usda.gov/topics/farm-economy/farm-sector-income-finances/highlights-from-the-farm-income-forecast ; https://www.dtnpf.com/…/2026/02/05/adjusted-inflation-usda-projects-net |
| 55 | Payment timing | $11–12bn Farmer Bridge paid by 28 Feb 2026; **+$13.1bn ARC/PLC does not pay until October 2026** — May–July was a liquidity air-pocket | USDA ERS / DTN, Feb 2026 |
| 56 | Input costs in the window | Diesel **$5.313/gal** w/e 27 Jul 2026 (+$1.54 YoY); urea $864/t mid-May easing to $714–718/t in July; World Bank fertiliser index highest since Oct 2022 in April | https://weeklydiesel.com/ ; DTN retail fertiliser, May–Jul 2026 ; https://blogs.worldbank.org/en/opendata/fertilizer-prices-surge-as-strait-of-hormuz-disruptions-tighten- |
| 57 | US HRC steel | **$1,220/short ton on 14 Aug 2026, +46.6% YoY**; May–Jul 2026 avg ~$1,120 vs ~$860. BLS PPI steel mill products +22.5% YoY in July 2026 | https://tradingeconomics.com/commodity/hrc-steel ; Steel Market Update; BLS 13 Aug 2026 release (secondary) |
| 58 | **AGCO** Q2 CY2026 (Apr–Jun) | Net sales $2,609M (−1.0%) but **North America +19.7% to $471.5M**; guidance **cut** on Europe, not North America; still models NA large ag −15% for 2026 | https://news.agcocorp.com/2026-07-30-AGCO-REPORTS-SECOND-QUARTER-RESULTS (30 Jul 2026) |
| 59 | **CNH** Q2 CY2026 | Ag net sales $3,277M (+1%); **NA ag +10% BUT "unfavorable product mix with weaker large tractor sales relative to smaller models"**; Ag adj EBIT **$170M / 5.2% vs $263M / 8.1%**; guidance raised/narrowed | https://www.stocktitan.net/news/CNH/cnh-industrial-n-v-reports-second-quarter-2026-o0p5uumfykau.html (3 Aug 2026) |
| 60 | **Caterpillar** Q2 CY2026 Construction Industries | Sales **$8.346B (+35%)**, North America **$5.065B (+50%)**, segment profit **$1.947B (+57%)**, margin 23.3% vs 20.1% | https://www.prnewswire.com/news-releases/caterpillar-reports-second-quarter-2026-results-302841940.html (4 Aug 2026) |
| 61 | Peer IEEPA refunds recognised **after** Deere's 3 May close | AGCO $22M; Caterpillar ~$300M; Kubota (cited); Amazon $640M | AGCO 30 Jul 2026; CAT Q2 call; roic.ai 31 Jul 2026 |
| 62 | US construction put-in-place, June 2026 | $2,166.5B SAAR, **−3.2% YoY**; private nonres −4.7% YoY, **−7.9% ex-data-centres** — the counter-evidence to the C&F bull case | https://www.census.gov/construction/c30/pdf/release.pdf ; https://www.constructiondive.com/news/construction-spending-june-2026-drop-data-centers/826936/ (4 Aug 2026) |
| 63 | Fed funds, May–Jul 2026 vs 2025 | 3.50–3.75% vs 4.25–4.50% (**−71bp** on EFFR); held 9–3 on 29 Jul 2026 with **three dissents for a hike** | https://www.federalreserve.gov/newsevents/pressreleases/monetary20260617a.htm ; https://www.cnbc.com/2026/07/29/fed-rate-decision-july-2026.html |
| 64 | Used-equipment values, June 2026 | High-HP tractors **+3.74% YoY** (inventory −16.7%, 13 months down); 175–299hp +4.21%; combines +0.72%; planters +13.3% — **lease residuals are a non-risk** | Sandhills/TractorHouse June-2026 report; https://www.morningstar.com/news/pr-newswire/20260706cg98367/… (6 Jul 2026) |
| 65 | FX, May–Jul 2026 vs 2025 | EUR **+0.3%** (vs +8.2% in Q2 FY26); BRL +9.8%; INR **−10.2%**; CAD **−1.6%**; Fed broad dollar index ~120 in July, **+1.2% YoY** | https://www.x-rates.com/average/ (2025, 2026), accessed 16 Aug 2026; https://tradingeconomics.com/united-states/trade-weighted-us-dollar-index-broad-goods-and-services-fed-data.html |

### 6.3 Our inferences and calculations — the load-bearing ones

| # | Inference | Value | Basis |
|---|---|---|---|
| 66 | Q3 ÷ Q2 total NSR ratio, 12-yr | mean 0.935, median 0.942, range 0.854–1.055; down-cycle 0.906 | computed from FY2014–FY2025 8-K tables |
| 67 | Q3 as % of full-year NSR, 12-yr | mean 26.08%, median 26.22%, range 25.11–27.59% | same |
| 68 | Q3 share of H2 net income | median **55.5%**; but the only Q4>Q3 precedent (FY2022) ran **45.6%** | same |
| 69 | PPA levels regression (FY2024–Q2 FY26, n=10) | **OP = 0.421 × Sales − 1,125**, R²=0.911, SE $142M; recent mean residual **−$81M** | OLS on the quarterly PPA series |
| 70 | PPA delta regression (FY2024–FY2025) | **ΔOP = 0.344 × ΔSales − 133**, R²=0.904, SE $115M | same |
| 71 | PPA volume/mix decremental | median **47%** (range 43–52%; 70% in the mix-heavy Q3 FY25) | reported bridge $ ÷ volume-driven sales change |
| 72 | PPA clean Q2 FY26 operating profit ex-refund | **~$652M / 14.5%** (not $706M / 15.7%) | $706M − 20% × $272M |
| 73 | Q3 FY2026 gross tariff, implied | ~$278M vs ~$200M in Q3 FY25 ⇒ **only ~$78M incremental YoY** (vs ~$200M in Q2), before the 8 June cut | ($1,200M − $644M) ÷ 2 |
| 74 | Company FX translation on Q3 FY26 net sales | **+0.2%** (0% to +1.0%), ~+$20M — vs +2.70% / ~$300M in Q2 | revenue-weighted model on FY2025 sales-by-customer-location; **calibrated to within 0.1pt on Q2's actual** |
| 75 | PPA operating-profit "Currency" bar, Q3 FY26 | **~$0M** (−$40M to +$40M), vs +$75M in Q2 FY26 and −$52M in Q3 FY25 | the bar is export-transaction margin, not translation |
| 76 | Consensus worldwide NS&R (bridged) | **~$12.4–12.6bn** = $10.87bn + the $1.59–1.66bn FS/other gap | corpus quarterly gaps |
| 77 | Diluted share count for Q3 FY2026 | **~270.0M** (269.5–270.8M) | 270.8M in Q2; buyback slowed to 326k shares |
| 78 | Required H2 FY2026 effective tax rate | **~25–28%** to land inside the 24–26% FY guide, given H1 at 22.8% | arithmetic |
| 79 | **Q3 FY2026 worldwide net sales and revenues** | **$12,350M** (low $11,900M / high $12,800M) | §2.1 |
| 80 | **Q3 FY2026 diluted GAAP EPS** | **$4.55** (low $3.70 / high $5.40); net income ~$1,230M | §2.2 |
| 81 | **Q3 FY2026 PPA operating profit** | **$450M** (low $340M / high $610M) on PPA net sales ~$3,880M, margin ~11.6% | §2.3 |

---

## 7. WHAT TO DO NEXT — ranked by value per unit of effort

1. **Hunt for evidence of a second IEEPA refund tranche.** This is the largest single unresolved variable
   (~$0.75/share, ~$54M of PPA operating profit per $272M) and the one most likely to be resolvable from
   public sources. Try: CBP CAPE Phase 2/3 filer or claimant disclosures; trade-press coverage naming
   large manufacturers; peer Q2/Q3 CY2026 10-Qs (AGCO, CNH, Caterpillar) for refund-timing language that
   would bracket Deere's fiscal Q3; any Deere 8-K between 28 May and 20 Aug (already checked — none, but
   re-check EDGAR on the morning of the print). Even a probability refinement from 30–40% to 15% or 60%
   would move the EPS central by ~$0.15–0.25.

2. **Resolve the Q3-share-of-H2 assumption with better evidence than a single precedent year.** Our 49.3%
   vs the agents' 45–48% vs the historical 55.5% is worth ~$0.70 of EPS. Highest-value approach: rebuild
   the H2 split at *segment* level for FY2022 (the only Q4>Q3 year) and see whether the 45.6% was driven by
   the same mechanism (a Q4-loaded large-tractor build) or by something idiosyncratic. Second: re-read the
   FY2022 Q2 call for cadence language and compare its specificity to the 21 May 2026 language.

3. **Pin down the PPA volume/mix decremental for a Q4-loaded quarter.** The single largest driver of the
   $290M–$550M PPA spread. Q3 FY2025 converted at 70% because mix deteriorated; Q2 FY2026 at 43%. If
   Waterloo shipments are Q4-loaded, Q3 FY2026 mix should be *worse* than normal, arguing for the high
   decremental and the low PPA number. Test: reconstruct the four missing waterfalls (Q4 FY22, Q1 FY23,
   Q2 FY23, Q2 FY24) from the raw slide files in `slides/` — agent 04 omitted them rather than guess, but
   recovering them would raise n from 12 to 16 and let the decremental be conditioned on mix.

4. **Verify the C&F and SAT Q3 estimates against the one perfectly aligned public dataset that exists.**
   Titan Machinery's FQ2 covers **May–July 2026 exactly** — but reports 27 August, a week after Deere. Not
   usable. Instead: check whether AGCO's or CNH's 10-Q (quarter ended 30 June 2026) discloses North
   American *monthly* shipment or dealer-inventory detail. CNH's Ex-99.1 returned 403 from SEC EDGAR;
   retrieve it by another route. This is the best remaining test of the C&F/SAT strength that carries ~60%
   of our total operating profit.

5. **Re-verify the two weakest quantitative inputs.** (a) The Nov-2024→Apr-2025 HRC average, which swings
   the lagged steel inflation between +10% and +18% — published quotes range $690–$904. (b) The BLS PPI
   steel-mill-products +22.5% figure, taken from secondary reporting because bls.gov returned 403 twice;
   the primary release is https://www.bls.gov/news.release/archives/ppi_08132026.htm.

6. **Retrieve consensus dispersion.** Every agent was bot-blocked on Zacks detailed-estimates, Yahoo's
   analysis tab, TipRanks and MarketScreener. A high/low bracket and analyst count for the Q3 FY2026 EPS
   estimate would let us judge whether $4.85 is a tight cluster or a wide distribution with a low tail near
   our $4.55. Try Investing.com's mobile endpoints, Quartr, Koyfin free tier, or a broker terminal.

7. **Check for post-corpus AEM August partial data and the 18 August housing-starts print.** July housing
   starts (18 Aug) and Home Depot/Lowe's Q2 (18–19 Aug) land two days before Deere and would refine the
   SAT/turf leg. Marginal, but free.

8. **Lowest priority — do not spend time on:** further peer regressions (residual σ of 12–21pp makes them
   directionally useful only); PPA cross-cycle comparison (structurally impossible, no PPA data before
   FY2020); or hunting for a published PPA operating-profit consensus (seven agents searched; it is
   Visible Alpha / LSEG paywalled and does not exist in free sources).

---

## 8. AGENT DOSSIER INDEX

| File | Workstream | Confidence | Headline contribution |
|---|---|---|---|
| `01-financial-history.md` | Quarterly history & seasonality | high | The Q3÷Q2 and Q3-as-%-of-FY ratio tables; the full FY2014–FY2026 quarterly series |
| `02-guidance-vs-actual.md` | Guidance bias | medium | 11-year guidance-vs-actual error table; the Q3/H2 = 47% argument |
| `03-q2-fy2026-deep-read.md` | Most recent reported quarter | high | Every verbatim forward-looking statement; the 53rd-week and tax-rate traps |
| `04-ppa-segment.md` | PPA conversion model | medium | The levels/delta regressions and the eight-bucket bridge library |
| `05-cycle-history.md` | Cycle positioning | high | The FY2016-Q3 equivalent-stage analogue and where it breaks |
| `06-analyst-consensus.md` | Consensus | medium | The $4.85–4.86 consensus and the equipment-vs-total revenue basis proof |
| `07-analyst-accuracy-history.md` | Consensus calibration | high | Q3 is Deere's weakest beat quarter (median +$0.13); the guidance ceiling |
| `08-ag-commodity-macro.md` | Farm economy | medium | "Better prices, worse margins"; the May–July grower-liquidity air-pocket |
| `09-adjacent-companies.md` | Peer read-across | medium | CNH's "weaker large tractor sales relative to smaller models" warning |
| `10-steel-input-costs.md` | Input costs & tariffs | medium | The Q3 tariff arithmetic (~$78M incremental vs ~$200M in Q2); the 8 June cut |
| `11-supply-chain-map.md` | Production signal | high | Zero 2026 WARN filings, ~245 recalls; no supply disruption; no UAW risk |
| `12-deere-news-may-aug-2026.md` | News window | high | Confirmed information vacuum 21 May – 16 Aug; FTC settlement is not a Q3 charge |
| `13-construction-forestry.md` | C&F and SAT | medium | The clean ex-refund Q2 segment margins; C&F and SAT Q3 estimates |
| `14-financial-services-fx.md` | FS and currency | medium | The FX tailwind collapsing from +2.7pt to +0.2pt; FS credit quality flat |
