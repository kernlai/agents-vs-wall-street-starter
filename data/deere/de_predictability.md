# Deere & Company — one-quarter-ahead predictability: revenue vs. margin

**Purpose.** Empirically test the operator hypothesis that *"the order book for Q3 was already
largely set at the Q2 report, so Q3 revenue is substantially pre-determined; what suppliers and
input costs actually move is profit, not revenue."*

**As-of.** 16 August 2026. Deere has **not** reported FY2026 Q3 (quarter ending ~2 Aug 2026);
the call is 20 August 2026. No Q3 FY2026 actuals exist in this dataset, in the offline corpus, or
on SEC EDGAR (EDGAR's latest Deere quarterly fact ends 2026-05-03). The INDEX.md row labelled
"2026-05-21 | Call Transcript | Q3 2026" is mislabelled Q2 material and was not used as Q3 data.

**Data.** `de_predictability.csv` (tidy long). Scripts:
`/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/de_build_panel.py`,
`.../de_predictability.py` (Python standard library only).

---

## 1. Verdict

| Claim in the hypothesis | Verdict |
|---|---|
| Revenue is more predictable one quarter ahead than margin | **Supported, decisively** |
| Profit/EPS surprise is mostly a margin phenomenon | **Supported** (margin explains ~79% of segment operating-profit surprise variance and ~68% of EPS surprise variance) |
| Therefore: tight range on revenue, wide range on margin/EPS | **Supported in direction, but with two material corrections** |

The two corrections matter enough that acting on the hypothesis naively would misprice the risk:

1. **Revenue and margin errors are positively correlated, not independent.** Regressing margin
   error on revenue error gives β ≈ **+1.15** for the ag segment (n=45, p=0.003) and **+1.31** for
   PPA (n=21, p=0.026). A 1% revenue miss historically comes with an additional ~1.2% relative
   margin miss, so operating profit moves ~**2.1–2.3×** the revenue miss. You cannot draw a tight
   revenue band and a wide margin band and then convolve them as independent — that understates
   the tails of PPA operating profit.
2. **Revenue predictability degrades exactly at cycle turns**, which is the regime FY2026 plausibly
   is in. At turning-point quarters, total-revenue MAE rises from 6.3% to 11.5% (n=52 calm vs
   n=13 turn) and PPA revenue MAE from 9.4% to 25.4% (n=18 vs n=3 — too small to lean on, but
   directionally consistent with the total). The "revenue is locked in" assumption is weakest
   precisely when it is being relied on most.

---

## 2. Data construction and validation

| Item | Result |
|---|---|
| 8-K earnings releases parsed | **46 of 47** (the one skip, `2017-06-01 fy-8k`, is not an earnings release) |
| Quarters in panel | **71**, FY2008 Q3 → FY2026 Q2 |
| Total revenue cross-check vs SEC EDGAR XBRL (CIK 315189) | **45 / 45 match**, 0 mismatches |
| Diluted EPS cross-check vs EDGAR | **45 / 45 match** after one sign repair (Q1 FY2018 was a loss quarter; the press-release text prints "$1.66 per share" unsigned — EDGAR's −1.66 is authoritative) |
| Same-quarter disagreements between two filings | **10**, all in FY2017 Q1/Q2 operating profit and net income, magnitude $2–7m. These are the ASU 2017-07 pension-cost reclassification restatements. As-reported (original) values were kept, since a one-quarter-ahead forecaster only had those. Logged, not averaged. |
| Ground-truth spot checks | FY2025 CF net sales 1,994+2,947+3,059+3,382 = **11,382** ✓; H1 FY2026 PPA 3,163+4,503 = **7,666** ✓; SAT 2,168+3,485 = **5,653** ✓; CF 2,670+3,790 = **6,460** ✓; Q2 FY2026 PPA/SAT/CF = 4,503 / 3,485 / 3,790 ✓ |
| Segment-definition break | Ag & Turf split into PPA + SAT from FY2021 (restated to FY2020 Q1). A spliced `AG` series (A&T before, PPA+SAT after) gives a continuous 50-quarter ag margin history; `PPA` alone has only 26 quarters of level and **21 usable forecast errors**. |

Missing data is an absent row. Nothing was zero-filled or imputed.

**Note on the operating-profit bridge.** This workstream did not require the slide bridges, so no
bridge-reconciliation count is reported here. The one bridge inspected as a spot check — PPA Q2
FY2026 — does reconcile: 1,148 − 402 + 49 + 75 − 51 − 77 − 4 − 32 + 0 = **706**, matching the 8-K
segment table exactly. Bridge reconciliation across all quarters belongs to the bridge workstream.

---

## 3. Method

One-quarter-ahead forecasts use **only information available at the Q(n−1) earnings release**.

| Rule | Level series | Margin series |
|---|---|---|
| `yoy_carry` (primary) | x̂(n) = x(n−4) · [x(n−1)/x(n−5)] | m̂(n) = m(n−4) + [m(n−1) − m(n−5)] |
| `seasonal` (control) | x̂(n) = x(n−4) | m̂(n) = m(n−4) |

Errors are logged so revenue and margin sit on the same scale-free footing:
`e = 100·ln(actual/forecast)`. Margin is additionally reported in bps as requested
(`de_margin_fcst_error_bps`). Because **OP = Revenue × margin**, in logs
`e_op = e_revenue + e_margin` holds *exactly*, which is what makes the variance decomposition
below an identity rather than an approximation.

Variance equality is tested with the **Pitman–Morgan** paired test (correlation of the sum and
difference of the two paired error series), with p-values from a self-contained incomplete beta
function. The paired test is the correct one here because both errors are measured on the same
quarters.

---

## 4. Test 1 — Is revenue more predictable than margin?

`yoy_carry` rule. All figures are one-quarter-ahead errors.

| Series | n | mean | sd | MAE | RMSE |
|---|---:|---:|---:|---:|---:|
| Revenue, total (%) | 65 | +0.17 | **8.96** | **7.37** | 8.89 |
| Revenue, PPA (%) | 21 | −1.68 | 14.97 | 11.67 | 14.71 |
| Revenue, SAT (%) | 21 | −0.42 | 10.57 | 8.48 | 10.32 |
| Revenue, AG spliced (%) | 45 | +0.64 | 10.96 | 8.92 | 10.85 |
| Revenue, C&F (%) | 45 | +0.29 | 14.92 | 12.45 | 14.75 |
| Margin, PPA (% of margin) | 21 | −3.42 | **40.68** | **29.77** | 39.85 |
| Margin, AG (% of margin) | 45 | +5.20 | 29.41 | 22.14 | 29.54 |
| Margin, C&F (% of margin) | 43 | +9.49 | 67.64 | 51.84 | 67.52 |
| Margin, equipment (% of margin) | 45 | +4.22 | 29.34 | 22.37 | 29.32 |
| Margin, PPA (bps) | 21 | −88 | **609** | **484** | 601 |
| Margin, AG (bps) | 45 | +10 | 373 | 287 | 369 |
| Margin, equipment (bps) | 45 | +8 | 344 | 266 | 340 |
| Operating profit, PPA (%) | 21 | −7.47 | 53.38 | 45.19 | 52.63 |
| Operating profit, AG (%) | 45 | +2.00 | 34.16 | 27.51 | 33.83 |
| **Diluted EPS (%)** | 59 | +0.16 | **29.17** | **22.33** | 28.93 |

The `seasonal` control is uniformly worse (total revenue sd 16.66% vs 8.96%; EPS sd 37.57% vs
29.17%), confirming the carry term adds real information and that `yoy_carry` is not a straw man.

### The ratio — the headline result

| Segment | n | sd(revenue err) | sd(margin err) | **ratio** | MAE rev | MAE margin | Pitman–Morgan p |
|---|---:|---:|---:|---:|---:|---:|---:|
| PPA | 21 | 14.97% | 40.68% | **2.72×** | 11.67% | 29.77% | <0.0001 |
| SAT | 20 | 10.20% | 55.06% | 5.40× | 8.15% | 27.92% | <0.0001 |
| AG (spliced) | 45 | 10.96% | 29.41% | **2.68×** | 8.92% | 22.14% | <0.0001 |
| C&F | 43 | 14.86% | 67.64% | 4.55× | 12.48% | 51.84% | <0.0001 |
| Equipment total | 45 | 11.02% | 29.34% | 2.66× | 9.11% | 22.37% | <0.0001 |
| Total revenue vs equipment margin | 45 | 9.62% | 29.34% | 3.05× | 8.14% | 22.37% | <0.0001 |

**Margin is 2.7–5.4× less predictable than revenue one quarter ahead**, and the sample is large
enough (n=45 for the continuous series) that this is not a small-sample artefact. The ratio is
stable across sub-periods, though it narrows in the current down-cycle:

| Window | n | sd(rev) | sd(margin) | ratio | p |
|---|---:|---:|---:|---:|---:|
| FY2015–FY2020 | 23 | 9.21% | 31.26% | 3.39× | <0.0001 |
| FY2021–FY2026 | 22 | 12.65% | 27.16% | 2.15× | 0.0002 |
| FY2023–FY2026 (down-cycle) | 14 | 13.39% | 20.65% | **1.54×** | **0.081** |

**This is the single most important caveat.** In the current down-cycle the ratio falls to 1.54×
and is no longer significant at the 5% level (n=14). Revenue predictability has *deteriorated*
(sd 9.2% → 13.4%) while margin predictability has *improved* (31.3% → 20.7%). The hypothesis was
strongly true in FY2015–FY2020; in the regime FY2026 actually sits in, the gap is roughly half as
wide and the sample is too small to establish it firmly. Read that as: revenue still deserves the
tighter band, but not nearly as tight as the full-history ratio implies.

---

## 5. Test 2 — Decomposing profit and EPS surprise

Exact log identity `e_op = e_revenue + e_margin` ⇒
`Var(e_op) = Cov(e_rev, e_op) + Cov(e_margin, e_op)`, shares summing to 1.

| Segment | n | sd(e_op) | **revenue share** | **margin share** | corr(e_rev, e_margin) |
|---|---:|---:|---:|---:|---:|
| PPA | 21 | 49.7% | 0.210 | **0.790** | +0.48 |
| SAT | 20 | 57.2% | 0.053 | 0.947 | +0.12 |
| AG (spliced) | 45 | 35.5% | 0.205 | **0.795** | +0.43 |
| C&F | 43 | 74.7% | 0.110 | 0.890 | +0.39 |
| Equipment total | 45 | 35.5% | 0.207 | 0.793 | +0.43 |

**EPS surprise** (`e_eps = e_rev + e_margin_equip + e_residual`, residual absorbing financial
services, corporate/reconciling items, tax rate and share count), n = 41, FY2015 Q2 – FY2026 Q2:

| Component | variance share | sd |
|---|---:|---:|
| Revenue | **0.146** | 10.0% |
| Equipment margin | **0.679** | 30.1% |
| Residual (FS, corporate, tax, shares) | **0.175** | 24.7% |
| sd(e_eps) | 1.000 | 32.5% |

**Margin is where the EPS surprise lives — about 68% of it.** Revenue contributes ~15%. Note the
residual at ~18% is *larger than revenue*: financial services, reconciling items and the tax rate
together move EPS more than the revenue miss does. For Q3 FY2026 that argues for explicit
attention to the 24–26% guided tax rate and the ~$860m FS net income guide, not just to PPA margin.

**Independent cross-check using Deere's own guidance** (no naive model involved). At Q(n−1) Deere
publishes FY net income guidance; the implied Q(n) net income is (guidance midpoint − YTD actual)
allocated by the prior-year seasonal share of remaining quarters:

- Net income error: n = 25, mean +21.2%, sd **36.2%**, MAE 28.6%
- Paired against revenue error on the same 25 quarters: sd 36.2% vs **10.0%**, ratio **3.64×**,
  Pitman–Morgan p < 0.0001

So the result survives replacing the naive model with the company's own published guidance:
bottom-line outcomes are ~3.6× harder to hit than revenue. The persistent **+21.2% mean** is also
informative — Deere's FY net income guidance has been biased *low* relative to the quarter that
followed, on average, over this sample.

---

## 6. Test 3 — Does predictability differ by quarter, and at cycle turns?

### By fiscal quarter (`yoy_carry`, n / MAE / sd)

| Series | Q1 | Q2 | **Q3** | Q4 |
|---|---|---|---|---|
| Revenue, total (%) | 16 / 6.8 / 8.8 | 17 / 7.3 / 9.2 | **16 / 6.3 / 7.6** | 16 / 9.0 / 10.7 |
| Revenue, PPA (%) | 5 / 4.7 / 5.4 | 6 / 10.9 / 14.5 | **5 / 15.3 / 20.4** | 5 / 16.0 / 19.7 |
| Revenue, AG (%) | 11 / 7.0 / 8.8 | 12 / 8.0 / 10.9 | **11 / 9.7 / 12.5** | 11 / 11.0 / 12.7 |
| Margin, AG (bps) | 11 / 295 / 431 | 12 / 318 / 396 | **11 / 305 / 380** | 11 / 228 / 312 |
| Margin, PPA (bps) | 5 / 612 / 779 | 6 / 559 / 731 | **5 / 257 / 277** | 5 / 494 / 625 |
| Margin, equipment (bps) | 11 / 292 / 396 | 12 / 307 / 402 | **11 / 253 / 328** | 11 / 208 / 263 |
| EPS (%) | 13 / 27.1 / 38.0 | 15 / 27.3 / 34.7 | **16 / 18.1 / 22.8** | 15 / 17.7 / 22.1 |

**Q3 is the most predictable quarter for total revenue** (MAE 6.3% vs 6.8/7.3/9.0) and is tied
with Q4 as the most predictable for EPS (18.1% vs 27.1/27.3). This is genuine support for the
hypothesis's mechanism: by the Q2 report, Q3 shipments are largely scheduled.

But **PPA revenue is the exception and it is the wrong exception for this forecast**: Q3 is the
*second-worst* quarter for PPA revenue (MAE 15.3%) after Q4. With n = 5 that difference cannot be
distinguished from noise, and the longer 11-quarter AG series shows only a mild Q3 penalty
(9.7% vs 7.0% in Q1). Treat "Q3 PPA revenue is unusually hard" as **unproven but not dismissible** —
the honest position is that Q3 PPA revenue deserves no *tighter* a band than Q1/Q2, and possibly
a wider one.

Individual Q3 errors (`yoy_carry`, sign = actual above/below the naive anchor):

- Total revenue: 2010 +9, 2011 −2, 2012 +2, 2013 −4, 2014 +4, 2015 −3, 2016 −8, 2017 +10, 2018 +2, 2019 −8, 2020 +9, 2021 −1, 2022 +10, 2023 **−15**, 2024 −5, 2025 +9
- PPA revenue: 2021 −4, 2022 +24, 2023 **−31**, 2024 −12, 2025 +5
- PPA margin (bps): 2021 −243, 2022 +147, 2023 −211, 2024 −72, 2025 **−609**
- EPS: 2010 +23, 2011 −34, 2012 −5, 2013 +20, 2014 −5, 2015 −15, 2016 +28, 2017 −23, 2018 −4, 2019 +5, 2020 +42, 2021 −26, 2022 −3, 2023 +16, 2024 −36, 2025 −3

### Cycle turning points

A quarter is flagged "turning" if the sign of total-revenue YoY growth flips versus the prior
quarter, or YoY growth changes by more than 15pp. **13 of 67** quarters qualify:
2010Q2, 2010Q4, 2013Q4, 2014Q1, 2014Q2, 2017Q1, 2019Q3, 2019Q4, 2020Q1, 2021Q1, 2023Q3, 2023Q4,
2025Q4.

| Series | n turn | MAE turn | n calm | MAE calm | ratio |
|---|---:|---:|---:|---:|---:|
| Revenue, total (%) | 13 | 11.5 | 52 | 6.3 | **1.82×** |
| Revenue, PPA (%) | 3 | 25.4 | 18 | 9.4 | 2.71× *(n=3, indicative only)* |
| Revenue, AG (%) | 8 | 13.0 | 37 | 8.0 | **1.61×** |
| Margin, AG (bps) | 8 | 229 | 37 | 300 | 0.76× |
| Margin, PPA (bps) | 3 | 361 | 18 | 505 | 0.72× *(n=3)* |
| Margin, equipment (bps) | 8 | 166 | 37 | 288 | 0.58× |
| EPS (%) | 12 | 17.9 | 47 | 23.5 | 0.76× |

**Revenue predictability breaks down at turns (1.6–1.8× worse); margin predictability does not.**
The margin ratios below 1 should not be over-read — turning quarters here cluster in 2010, 2014,
2020–21 and 2023, and margin errors are largest in absolute terms at cycle *troughs* (2016, 2025)
rather than at *turns*. The defensible statement is: **at turning points the revenue advantage
shrinks or disappears**, which is the same message as the FY2023–FY2026 sub-period split in §4.

FY2026 Q4 is already flagged as a turn (2025Q4), and Q3 FY2026 sits directly after it, in the
middle of a large-ag down-cycle (US&Canada large ag guided down 15–20%) with an offsetting
SAT/CF up-cycle. This is not a calm quarter.

---

## 7. Mechanical anchors for Q3 FY2026 (benchmarks, not forecasts)

`yoy_carry` anchors computed from Q3 FY2025 and the Q2 FY2026 / Q2 FY2025 YoY carry, with the
empirically measured one-quarter-ahead error sd applied as a ±1σ (≈68%) band.

| Target | anchor | error sd | ±1σ band | n |
|---|---:|---:|---|---:|
| **Net sales & revenues** | **$12,589m** | 9.0% | $11,510m – $13,768m | 65 |
| PPA net sales | $3,679m | 15.0% | $3,167m – $4,273m | 21 |
| SAT net sales | $3,521m | 10.6% | $3,168m – $3,914m | 21 |
| C&F net sales | $3,934m | 14.9% | $3,389m – $4,567m | 45 |
| **Diluted EPS** | **$4.69** | 29.2% | $3.50 – $6.27 | 59 |
| **PPA operating margin** | **7.30%** | 609bps | 1.21% – 13.39% | 21 |
| AG operating margin | 11.49% | 373bps | 7.77% – 15.22% | 45 |
| Equipment operating margin | 10.63% | 344bps | 7.19% – 14.06% | 45 |

**These are deliberately unconditioned benchmarks, and the PPA margin anchor is visibly wrong.**
The 7.30% anchor mechanically carries Q2's −632bps YoY margin decline into Q3, but H1 FY2026 PPA
margin was already 845/7,666 = **11.0%** against FY guidance of **11–13%**, which requires H2 PPA
margin of roughly 11–15%. The naive anchor sits ~400bps below the bottom of what guidance implies.
This is a concrete illustration of the ±609bps PPA margin error band, and of why guidance and the
order book must be used to condition the margin forecast rather than a carry rule.

Implied PPA operating profit from the anchors, $3,679m × 7.30% ≈ **$269m**, should therefore be
treated as a low-side scenario, not a central case. A guidance-conditioned central case of
11–13% on $3,679m gives ~$405–478m.

The width relationships, however, are the transferable result: **the revenue band should be
roughly one third the relative width of the margin band, before allowing for the fact that they
are positively correlated.**

---

## 8. Correlation coefficients with sample sizes

| Statistic | value | n | note |
|---|---:|---:|---|
| corr(e_revenue, e_margin), PPA | +0.48 | 21 | p = 0.026 |
| corr(e_revenue, e_margin), AG | +0.43 | 45 | p = 0.003 |
| corr(e_revenue, e_margin), SAT | +0.12 | 20 | p = 0.60 — **not significant** |
| corr(e_revenue, e_margin), C&F | +0.39 | 43 | p = 0.010 |
| corr(e_revenue, e_margin), equipment | +0.43 | 45 | p = 0.003 |
| Operating-leverage β (margin% per revenue%), AG | +1.15 | 45 | ⇒ d(op profit)/d(revenue) ≈ 2.15 |
| Operating-leverage β, PPA | +1.31 | 21 | ⇒ ≈ 2.31 |
| Operating-leverage β, C&F | +1.78 | 43 | ⇒ ≈ 2.78 |

Sample sizes of 20–45 quarters are small. The 45-quarter results (AG, C&F, equipment, total
revenue, EPS) are the ones to lean on. The 20–21 quarter PPA/SAT results are directionally
consistent with them but individually fragile; where PPA and AG disagree, AG is the more reliable
guide because PPA is a strict subset of AG measured over half the history.

---

## 9. Caveats

1. **No sell-side consensus.** The offline corpus contains no analyst estimates, so "surprise" is
   defined against (a) a naive one-quarter-ahead model and (b) Deere's own FY net-income guidance.
   Both give the same answer, but neither is the market's consensus. A genuine consensus-based
   surprise decomposition could differ, most plausibly by shrinking the revenue share further,
   since sell-side revenue models already condition on the order book.
2. **PPA has only 21 usable forecast errors** (FY2021 Q2 – FY2026 Q2, plus FY2020 restated). Every
   PPA-specific number in this note rests on that.
3. **Segment-definition break at FY2021.** The spliced AG series assumes PPA+SAT is comparable to
   the old A&T. Reported net sales aggregate cleanly, but allocation of corporate costs between
   the two new segments has no pre-2020 analogue.
4. **The down-cycle sub-period result (§4) materially qualifies the headline.** In FY2023–FY2026
   the margin/revenue predictability ratio is 1.54× with p = 0.081 (n=14) — the data cannot
   distinguish the two at conventional significance in the current regime.
5. **Turning-point classification is ex-post.** It uses realised YoY growth, so it identifies where
   errors were large but cannot be used to flag a turn in advance.
6. **FY2017 restatement conflicts** (10 fields, $2–7m) were resolved to as-reported values.
7. **The guidance-implied test allocates the residual FY guide by prior-year seasonality**, which
   is itself a naive assumption; its +21.2% mean bias partly reflects Deere's habit of guiding
   conservatively rather than pure forecast error.
8. **No Q3 FY2026 data of any kind is used or implied.** The §7 anchors are constructed purely
   from FY2025 Q3, FY2026 Q2 and FY2025 Q2 actuals.

---

## 10. What this means for the three forecast targets

- **Worldwide net sales & revenues** — the hypothesis holds well enough to justify a tighter band,
  but "tight" empirically means roughly **±7–9% at 1σ**, not ±2–3%. Q3 is the best quarter for this
  (MAE 6.3%), which supports the order-book mechanism; the cycle-turn penalty (1.8×) pushes back
  the other way. A ±6–8% 1σ band around a guidance-and-order-book-conditioned central case is
  defensible; anything tighter is not supported by 65 quarters of history.
- **Diluted EPS** — genuinely wide. sd of one-quarter-ahead error is **29%**, and the surprise is
  68% margin-driven, 18% below-the-line (FS/corporate/tax), only 15% revenue-driven. Concentrate
  forecasting effort on the PPA production-cost/tariff line, the tax rate, and financial services —
  not on refining the revenue estimate.
- **PPA operating profit** — the widest of the three. sd of one-quarter-ahead error on PPA
  operating profit is **53%** (n=21), and 79% of that variance is margin, not volume. Because
  revenue and margin errors are positively correlated (β ≈ 1.3), a downside revenue scenario should
  be paired with a downside margin, giving ~2.3× leverage into operating profit. Model PPA
  operating profit directly with correlated revenue/margin draws rather than multiplying an
  independent tight revenue band by an independent wide margin band.
