# The lead-time / order-book hypothesis: verdict

**Question tested.** *"Deere needs longer than a month to build a tractor. Sales and supply-chain impacts lag.
So the order book for Q3 was already largely set at the time of the Q2 report, and Q3 REVENUE is therefore
substantially pre-determined. The thing suppliers and input costs actually move is PROFIT, not revenue."*

**As of 16 August 2026, Deere has not reported FY2026 Q3.** The quarter ends ~2 August 2026 and the call is
09:00 US Central, Thursday 20 August 2026. No Q3 FY2026 actuals exist in the corpus, in any of the four
evidence CSVs, or on SEC EDGAR (latest Deere quarterly fact ends 2026-05-03). The `INDEX.md` row labelled
`2026-05-21 | Call Transcript | Q3 2026` is mislabelled Q2 material; all four workstreams independently
confirmed this and treated it as Q2.

**Adjudication script:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/de_thesis_verdict.py`
(stdlib only, reads only the four evidence CSVs plus `de_guidance_vs_actual.csv`).

---

## 1. Verdict

# PARTIALLY SUPPORTED

The hypothesis gets the **modelling conclusion right** and the **stated mechanism wrong**, and it misidentifies
*which* uncertainty binds. Specifically:

| Clause | Verdict | Why |
|---|---|---|
| Q3 demand was already booked at the Q2 report | **Supported, strongly, for PPA and C&F** | 13/13 Q2 calls since 2013 state order coverage reaching past Q3; at Q2 FY2026 management said the MY2026 production plan "is set at this point" |
| The mechanism is manufacturing lead time ("longer than a month to build a tractor") | **Contradicted** | Deere never once cites build time as the constraint in 310 documents. Order-to-*production-start* is ~3 months; what fixes the quarter is **commercial** lead time — early order programs closing 8–14 months before the use season |
| Therefore Q3 revenue is tight | **Supported, and now measured: 4.45% 1σ vs 8.96% for a naive model** | Conditioning on Q2 guidance roughly **halves** revenue error. This is the hypothesis's real payoff and it is large |
| The thing input costs move is profit, not revenue | **Supported as a forecasting claim; contradicted as a statement about realised variation** | Costs contribute a **negative** share of realised ΔOP variance (−22.6% PPA) — volume/mix carries 65–90%. But conditional on guidance, profit error is **2.65×** revenue error on the same five years and the two are **uncorrelated** (r = −0.16) |
| Put the width on margin, not revenue | **Supported. Measured factor: 4× for PPA operating profit, 3× for EPS** | See §5 |

### The two corrections that change what you do

**(a) The order book pins the HALF-YEAR, not the QUARTER.** This is the sharpest finding in the whole
workflow and no single evidence agent surfaced it. Decomposing the measured Q3 revenue error:

| Target | error from H2 guidance being wrong | error from the Q3/Q4 **split** | combined Q3 1σ |
|---|---:|---:|---:|
| Enterprise net sales & revenues | 2.40% (n=5) | **3.75%** (n=13) | 4.45% |
| PPA net sales | 3.07% (n=5) | **6.97%** (n=5) | 7.61% |
| PPA operating profit | 8.14% (n=5) | **15.24%** (n=5) | 17.28% |

For every target, the **larger** term is the Q3-versus-Q4 allocation — which the order book does *not*
determine. Deere reallocates shipments between Q3 and Q4 most years. The order book guarantees the sale;
it does not guarantee the quarter. So the correct formulation is not "Q3 revenue is pre-determined" but
**"H2 revenue is pre-determined; Q3 revenue is pre-*disclosed*"** — tight only because management narrates
the intended cadence at the Q2 call, not because the backlog mechanically fixes it.

**(b) At the guidance-conditioned horizon, revenue error and profit error are uncorrelated.** The
predictability workstream measured corr(revenue error, margin error) = +0.43 to +0.48 and warned against
treating the two bands as independent. That correlation is an artefact of the *naive* model, in which both
errors share a common "the cycle turned" component. Re-measured on the information set we will actually use
— Q2-vintage guidance — the correlation vanishes: **r = −0.16 for PPA (n=5), −0.01 for enterprise (n=5)**.
The volume path is already inside the guidance, so what is left on the profit line is close to pure cost
noise. Do **not** apply the β = +1.31 leverage amplifier to a guidance-anchored forecast; it would
double-count. (n=5 cannot establish independence either — treat as weakly correlated, not as β = 1.31.)

### Where it holds and where it breaks

- **Holds:** PPA large ag and PPA seasonal (combines, planters, sprayers) — ~90% of seasonal volume locked
  by early order programs closed months before the Q2 call.
- **Holds moderately:** C&F — "over 80% of production slots filled for the year" at 21 May 2026, but only
  2–4 months of order visibility historically.
- **Breaks:** SAT turf and compact utility. Deere has **never quantified** order visibility for this segment
  in 14 years of transcripts and explicitly says *"we have less order visibility in turf equipment and
  compact utility tractors"* (2025-05). SAT is ~29% of equipment sales and is the segment where the
  hypothesis simply does not apply — it is a retail-driven, short-cycle business.
- **Also breaks at cycle turns.** The revenue-predictability advantage falls from 3.39× (FY2015–20) to
  **1.54× and non-significant (p = 0.081, n=14)** in the FY2023–FY2026 down-cycle, and revenue MAE rises
  1.6–1.8× at turning-point quarters. FY2026 is a turning cycle (US&Canada large ag guided −15–20% against
  SAT +15% and C&F +20%). The hypothesis is weakest exactly where we are relying on it.

---

## 2. Quantified lead time

**Deere has never stated a lead time anywhere in the 310-document corpus.** Every figure below is derived
from programme calendars, coverage statements and the fiscal calendar. Manufacturing cycle time is *not* the
binding constraint and is never cited as one.

| Business | Binding lead time | Type | Evidence |
|---|---|---|---|
| PPA seasonal — combines, planters, sprayers (~90% of those lines via EOP) | **8–14 months** order → use season | Commercial (EOP) | Sprayers open early-May, close end-August; planters open June, close September; combines open August, run to Nov/Dec/Jan. *"we normally have the EOP open for five to six months"* (2022-11-23) |
| PPA large tractors (Waterloo, Mannheim) | **3.0–5.4 months** forward coverage at each Q2 call; mean **4.57** (n=9 quantified across 13 Q2 calls 2013–2026) | Commercial (rolling book) | 2026-05-21: *"Waterloo large tractors, order books are well into the fourth quarter"* |
| PPA Europe / South America | **2.5–4.5 months** | Commercial | 2026-05-21: *"Order visibility in both regions now extends through the third quarter and into the fourth"* |
| C&F earthmoving | **2–4 months** | Commercial | 2024-08: *"roughly two months of order visibility"* |
| SAT turf / compact utility | **Never quantified in 14 years** | — | 2017-08: *"We don't tend to get that kind of visibility on small Ag"* |
| *Order → production start (any line)* | *~3 months* | *Manufacturing + scheduling* | MY2027 spring product opened EOP early May 2026, production begins *"in the last few months of the fiscal year"* |

**In no Q2 call in the corpus does PPA large-ag coverage fall short of the following Q3.** 13 out of 13.

### How much of Q3 FY2026 was committed at the 21 May 2026 Q2 call?

Q3 FY2026 runs 2026-05-04 to 2026-08-02 (13 weeks, end-date derived — Deere has not published it). The Q2
report landed on 21 May, **18 days / ~20% of the way into the quarter already physically elapsed.**

| Evidence at that date | Implication for Q3 |
|---|---|
| *"Model year 2026 production of seasonal products is largely set by our early order programs, which have been closed for several months now"* | Seasonal PPA: effectively 100% committed |
| *"Demand and that production plan for 2026 is set at this point. Our EOPs for this year have closed, and we know where we're going to build in combines, sprayers, and planters"* | Explicit management statement that the plan is fixed |
| *"order books are well into the fourth quarter"* (Waterloo large tractors) | Coverage ≥ 4 months forward = through ~late September, i.e. all of Q3 plus ~2 months of Q4 |
| *"Order visibility in both regions now extends through the third quarter and into the fourth"* (Europe, South America) | All of Q3 |
| *"over 80% of production slots filled for the year"*, order book up >60% since November (C&F NA) | Most of Q3 |
| MY2027 EOPs only just launching; production *"in the last few months of the fiscal year"* | MY2027 does not touch Q3 |
| SAT turf/compact | No visibility statement given, in any year |

**Best estimate:** at the Q2 call, essentially **100% of Q3 PPA orders and ~80%+ of Q3 C&F orders were in
hand**, covering roughly **70% of equipment revenue** (H1 weights: PPA 39%, C&F 33%, SAT 29%). The residual
uncertainty on Q3 revenue is therefore almost entirely **shipment timing and cancellation**, not demand
arrival — which is precisely why the Q3/Q4 split term in §1(a) dominates the guidance term.

Four documented ways the order book fails to determine revenue: orders are cancellable (2012-08); FY2022
revenue timing was set by parts availability, not demand (*"the biggest challenge … was the number of
partially completed machines"*); Deere cut H2 production below the order book in FY2019 and FY2024; and
Brazil is on planned combine underproduction through Q3 FY2026 right now.

---

## 3. Variance split: volume/mix versus production costs, warranty and price

Two decompositions answer two different questions. Both are correct. Reporting only one is how this
hypothesis gets mis-adjudicated.

### 3a. Realised variation — exact additive decomposition of YoY ΔOP (bridge, 69 segment-quarters)

`Var(ΔOP) = Σ Cov(cᵢ, ΔOP)`, shares sum to 100%. Negative share = counter-cyclical stabiliser.

| Component group | PPA (n=21) | SAT (n=22) | CF (n=26) | Pooled (n=69) |
|---|---:|---:|---:|---:|
| **volume/mix** | **+89.9%** | **+77.1%** | **+64.9%** | **+85.6%** |
| price | +40.9% | +25.4% | +42.2% | +37.6% |
| **production costs + warranty** | **−22.6%** | **−4.7%** | **−21.7%** | **−19.7%** |
| all revenue-linked (vol/mix + price + FX) | +131.0% | +104.2% | +108.9% | +123.8% |
| cost block (prod costs + warranty + SA&G/R&D + other) | **−32.6%** | −9.2% | −20.9% | — |

**On realised variation the hypothesis is contradicted.** Production costs correlate *negatively* with ΔOP
(−0.59 PPA, −0.50 CF): they improve when volumes collapse and worsen when volumes surge. Restricting to the
FY2024+ down-cycle (n=10 per segment) makes it starker, not weaker — volume/mix rises to 115% for PPA.
Bridge reconciliation: **69 reconciled, 1 rejected** (FY2023 Q2 PPA), with a 132/132 independent sign check
against 8-K MD&A prose that catches the label permutations arithmetic cannot.

### 3b. Unforecastable variation — decomposition of *surprise*

| Decomposition | Revenue share | Margin share | n |
|---|---:|---:|---:|
| PPA operating-profit surprise | 0.210 | **0.790** | 21 |
| Ag (spliced) operating-profit surprise | 0.205 | **0.795** | 45 |
| EPS surprise | 0.146 | **0.679** (+0.175 below-the-line: FS, corporate, tax, shares) | 41 |

**On unforecastable variation the hypothesis is supported.**

### 3c. Reconciling the two — and a failed test reported honestly

The two results are consistent if and only if volume/mix is *forecastable* and the cost block is not.
I tested this first via persistence (lag-1 autocorrelation of each bridge component) and **the test failed
to discriminate**: PPA volume/mix r = +0.80 but the cost block r = +0.87 — the cost block is *more*
persistent, not less. Persistence is not the mechanism. Reporting this because it is a negative result that
constrains the story.

The test that *does* discriminate is the guidance test, on identical years and an identical information set:

| Measured on the Q2-vintage guidance information set, FY2021–FY2025 | sd | n |
|---|---:|---:|
| Implied-H2 **PPA net sales** error | **3.07%** | 5 |
| Implied-H2 **PPA operating profit** error | **8.14%** | 5 |
| Ratio | **2.65×** | 5 |
| Implied-H2 **equipment sales** error | **2.40%** | 5 |
| Implied-H2 **net income** error | **10.61%** | 5 |
| Ratio | **4.42×** | 5 |
| corr(H2 sales error, H2 profit error), PPA | **−0.16** | 5 |

**Answer to the question as posed.** Volume/mix drives the realised swing, by a wide margin, in every
segment. But volume/mix is the part management tells you about; the cost block is the part it cannot. Once
the volume path is conditioned on, the residual profit uncertainty is roughly **2.7× (PPA operating profit) to 4.4×
(enterprise net income) larger than the residual revenue uncertainty**, and it is essentially orthogonal to
it. That is the hypothesis's genuine content, arrived at by a different route than the one it proposes.

---

## 4. Predictability: revenue versus margin, measured

| Model / information set | Revenue error sd | Margin or profit error sd | Ratio | n |
|---|---:|---:|---:|---:|
| Naive `yoy_carry`, total revenue vs equipment margin | 9.62% | 29.34% | **3.05×** | 45 |
| Naive, PPA | 14.97% | 40.68% (609bps) | **2.72×** | 21 |
| Naive, Ag spliced | 10.96% | 29.41% | 2.68× | 45 |
| Naive, FY2023–26 down-cycle only | 13.39% | 20.65% | **1.54× (p = 0.081, n.s.)** | 14 |
| Deere's own FY net-income guidance, seasonally allocated | 10.0% | 36.2% | **3.64×** | 25 |
| **Q2-vintage guidance → implied H2 (our actual method)** | **2.40%** | **10.61%** | **4.42×** | **5** |

**Yes — revenue is genuinely the tighter of the two, by a factor of roughly 2.7× to 4.4×** depending on
method, with Pitman–Morgan p < 0.0001 on the large-sample versions. Three qualifications:

1. **The advantage halves in the current regime** (1.54×, n=14, not significant at 5%). This is the single
   most important caveat in the whole workflow.
2. **Conditioning on guidance shrinks revenue error far more than profit error** — from 9.6% to 2.4% for
   revenue (4×) but only from ~36% to ~10.6% for the bottom line (3.4×), and profit's *residual* is what
   remains after all the information Deere has released. The hypothesis's directional advice survives
   every method tried.
3. **Q3 is empirically the most predictable quarter for enterprise revenue** (MAE 6.3% vs 6.8/7.3/9.0 for
   Q1/Q2/Q4, n=16), which is real support for the order-book mechanism. But **Q3 is the second-worst quarter
   for PPA revenue** (MAE 15.3%, n=5) — unproven at n=5, but it argues against tightening the *segment*
   band below the enterprise band. Segment errors offset at the enterprise level; the hypothesis holds
   considerably better for the consolidated top line than for PPA alone (4.45% vs 7.61% Q3 1σ).

---

## 5. Forecasting implication — recommended range widths

All widths below are derived from the **measured** error distributions above, not from intuition. Central
cases are guidance arithmetic shown only to convert percentages into dollars — **they are not forecasts.**

### Central-case arithmetic (guidance only)

H1 FY2026 actuals: PPA 7,666 / SAT 5,653 / C&F 6,460 = 19,779 equipment; NSR 22,980; PPA operating profit 845.
Applying the 21 May 2026 FY guidance: H2 equipment sales **21,001–22,299** (mid 21,650) — note the *guidance
range alone* spans 6.0% of its own midpoint before any forecast error. Management's stated cadence is Q4 >
Q3, so a Q3 share of H2 below the 0.507 historical mean (~0.49) gives Q3 equipment ~10,600, plus ~1,590 of
financial services and other revenue → **NSR ≈ $12.2bn**. PPA: FY sales ~16,013 × 12% margin = 1,922 FY
operating profit, less 845 H1 = 1,077 H2, × ~0.48 Q3 share → **PPA operating profit ≈ $515m**. FY net income
guide $4,750m mid, less ~$2,430m H1, × 0.553 Q3 share of H2 EPS, ÷ ~270m diluted shares → **EPS ≈ $4.75**.

### Recommended widths

| Target | Measured Q3 1σ | Small-sample upper bound | **Recommended 1σ** | **Recommended ~80% range** | vs naive model |
|---|---:|---:|---:|---:|---:|
| **Worldwide net sales & revenues** | 4.45% | 6.8% | **±5%  (≈ ±$610m)** | **±7%  (≈ ±$850m)** | naive was ±9.0% |
| **Diluted EPS (GAAP)** | 12.1–12.9% | ~17% | **±15%  (≈ ±$0.71)** | **±20%  (≈ ±$0.95)** | naive was ±29.2% |
| **PPA operating profit** | 17.3% | ~24.6% | **±20%  (≈ ±$105m)** | **±29%  (≈ ±$150m)** | naive was ±53.4% |
| *(supporting) PPA net sales* | 7.6% | ~10% | *±8% (≈ ±$310m)* | *±11%* | *naive was ±15.0%* |

**The actionable ratio: the PPA operating-profit band should be 4× the relative width of the revenue band,
and the EPS band 3×.** That is the hypothesis's core modelling advice, and it is confirmed — with the
revenue band roughly *half* what an unconditioned model would give you, which is where the value is.

Five things to do with these numbers:

1. **Skew the EPS and revenue ranges upward.** Deere's Q2-vintage guidance has been biased *low*: implied-H2
   net income error mean **+22.2% across 13 years**, **+5.7% excluding the FY2016 and FY2020 outliers**;
   implied-H2 PPA sales error mean **+2.48%** (5 of 5 years above or at guidance). A symmetric band around
   pure guidance arithmetic will sit too low. Prefer e.g. EPS $4.15–5.60 over a symmetric $4.04–5.46.
2. **Do not apply the naive-model leverage amplifier (β = +1.31).** Conditional on guidance the revenue and
   profit errors are uncorrelated (r = −0.16, n=5). Applying β to a guidance-anchored revenue forecast
   double-counts the volume effect. Sample the cost band as a largely independent draw.
3. **Spend the forecasting effort on the Q3/Q4 split, not on the order book.** The split term is the larger
   contributor to Q3 error for all three targets. The order book question is essentially settled; the
   allocation question is not. Management's cadence language is the only real evidence: *"Q4 a bit stronger
   than Q3"*, *"more Waterloo large tractor shipments … in the back half than the front half — that's
   abnormal for us"*, SAT *"a little bit of a step down in Q3 and another step down in Q4"*, C&F *"fairly
   balanced … maybe a little bit stronger in the fourth quarter"*.
4. **Make tariff adjudication the largest single term in the margin band, ahead of commodities.** The Q2
   beat was a $272m IEEPA refund booked into production cost, worth ~2.5 points of equipment margin, while
   revenue "came in largely in line." The Court of International Trade invalidated the Section 122 tariffs
   on **2026-05-07, four days into Q3** — the same mechanism, live, unmodelled in the 21 May guidance. PPA's
   share would be ~$54m, ~10% of a $515m central case, and it is a **one-sided upside** tail. Rank the
   margin risks: tariff adjudication > material/energy inflation > warranty.
5. **Two known Q3-specific margin headwinds are already identifiable and belong in the central case, not the
   band.** (a) The favourable back-half cost comp lands in **Q4, not Q3** — PPA's production-cost bridge was
   still +69 (favourable) in Q3 FY2025 and only collapsed to −147 in Q4 FY2025, so Q3 faces the hard comp.
   (b) Management flagged *"better absorption in the fourth quarter as production rates are significantly
   higher"* — Q3 is the weaker-absorption H2 quarter by design. Also note Q2's reported 15.7% PPA margin was
   ~14.5% ex-refund; do not carry the reported figure forward.

---

## 6. What would change the answer

**An extended summer production shutdown in the May–July 2026 window would undercut the
revenue-is-pre-determined claim. It was searched for specifically and none was found.**

| Date | Event | Direction |
|---|---|---|
| 2026-02-06 | 146 workers recalled to four Waterloo facilities (Drivetrain, Tractor Operations, Engine Works, Foundry) from early March, citing increased demand for 8R tractors | **Expansionary, PPA large ag** |
| 2026-03-28 / 04-04 / 04-28 | ~120 layoffs at Des Moines Works, Ankeny IA, in three tranches | Contractionary — but **entirely inside Q2 FY2026** |
| 2026-05-04 → 2026-08-02 | **Nothing found.** No extended shutdown, additional seasonal layoff, or production-rate cut announced in the Q3 window. No John Deere WARN filings in calendar 2026 | **No shipment shock identified** |

This is recorded in `de_q3_cost_inputs.csv` as a `production_event` row with a **blank value** and the search
documented — an absent observation, not a zero. It is absence of evidence in public reporting and a WARN
aggregator that may lag, **not** a company statement that nothing happened. Deere takes routine summer
shutdown weeks every year; the question is whether FY2026's were extended, and nothing indicates they were.
Management's own framing points the other way: Q3 is the lighter back-half quarter *by schedule*
(*"that's just the way the order book built this year for a much heavier fourth quarter"*), disclosed on
21 May — a planned weighting, not a disruption.

### Other evidence that would move the verdict

| Finding | Effect |
|---|---|
| Q3 revenue lands outside ±7% of the guidance-implied central case | Falsifies the tight-revenue conclusion; would mean the Q3/Q4 split risk is materially larger than 3.75% |
| A second tariff refund appears in Q3 | Confirms the margin-width recommendation and the tariff-first ranking; would make the ±20% PPA band look too narrow on the upside |
| PPA Q3 revenue misses badly while SAT/C&F are in line | Confirms that segment-level offsetting is what makes the enterprise number tight, and that PPA alone deserves the wider ±8% |
| Dealer order cancellations disclosed | Directly attacks the order-book-equals-revenue link — the 2012-08 precedent exists |
| Sell-side consensus obtained | Would replace the naive/guidance benchmarks with the market's own. Likely **shrinks the revenue share of surprise further**, since sell-side revenue models already condition on the order book — i.e. would strengthen the hypothesis |

---

## 7. Principal caveats

1. **The guidance test that sets the range widths rests on n = 5** (FY2021–FY2025, the life of the current
   segment structure). The 90% upper confidence bounds on σ are roughly 2.4× the point estimates
   (H2 equipment sales 2.40% → 5.69%; H2 PPA operating profit 8.14% → 19.30%). The recommended widths in §5
   deliberately sit **above** the point estimates for this reason. The correlation results (r = −0.16,
   −0.01) at n=5 are close to uninformative — they refute the assumption that β = +1.31 carries over, but
   they do not establish independence.
2. **None of the five guidance-test years contained a tariff-adjudication regime resembling FY2026.** The
   measured error distribution has no observation like the Q2 FY2026 $272m refund. The recommended bands may
   understate the true FY2026 tail, which is why §5 asks for an explicit upside skew on margin.
3. **The Q3/Q4 split term and the H2 guidance term are combined in quadrature, i.e. treated as independent.**
   That assumption is stated, not proven.
4. **Q3 FY2026's quarter-end date (2026-08-02) is derived** as 13 weeks after the reported Q2 end. Deere has
   not published it.
5. **Segment financials begin FY2021**, so every PPA/SAT/CF dispersion statistic rests on n = 5 (annual) or
   n = 21–26 (quarterly). Where PPA and the 45-quarter spliced-Ag series disagree, prefer Ag.
6. **No sell-side consensus exists in the corpus.** "Surprise" is defined against a naive model, Deere's own
   guidance, and the guidance-implied-H2 inference. All three agree on direction.
7. **Lag correlations between input costs and the production-cost bridge are not identified** — a placebo
   (CPI used cars, r = −0.92) beats every genuine input at the same lag, effective n is 6–12, and 315 tests
   were run. Steel lag 2–3 is used as a physical planning convention only, never quoted as a measured effect.
8. **Bridge coverage gaps.** The margin-bridge workstream recovered 21 of 22 PPA quarters; the cost
   workstream recovered 18 of 22 with a stricter parser, losing 2Q22, 3Q22, 1Q23, 2Q23 and thereby most of
   the FY2022–23 inflation peak. The two disagree on how many quarters are safely recoverable; §3a uses the
   69-quarter reconciled set, which carries the independent 132/132 MD&A sign check.
9. **Transcripts are speaker-unattributed** ("Unknown speaker"), so no quote can be assigned to a named
   executive, and some OCR corruption is present.
10. **Coverage-in-months figures are derived** from wording plus call date plus the fiscal calendar, with
    each derivation written into the CSV `notes` so it can be disputed. Deere has never quantified lead time
    directly.

---

## Sources

| Workstream | CSV | Doc |
|---|---|---|
| Order book / lead time | `de_order_book.csv` (135 rows) | `de_order_book.md` |
| Margin bridge | `de_operating_profit_bridge.csv` (688 rows, 69 reconciled / 1 rejected) | `de_operating_profit_bridge.md` |
| Predictability | `de_predictability.csv` (3,019 rows) | `de_predictability.md` |
| Supply / cost / Q3 window | `de_q3_cost_inputs.csv` (1,942 rows) | `de_q3_cost_inputs.md` |
| Guidance vs actual (used for the §5 range widths) | `de_guidance_vs_actual.csv`, `de_guidance.csv` | `de_guidance.md` |

Adjudication: `scripts/data/de_thesis_verdict.py`. All paths relative to
`/Users/cor/Documents/projects/agents-vs-wall-street-starter/`.
