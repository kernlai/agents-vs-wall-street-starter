# Deere Dealer Network — Financial Health Verdict

**Prepared 16 August 2026.** Deere has **not** reported FY2026 Q3. The Q3 earnings call is 09:00 US
Central, Thursday 20 August 2026. **No Q3 FY2026 actuals exist in this analysis or anywhere else.**
Last reported Deere period: Q2 FY2026, ended 3 May 2026. Corpus frozen 2026-08-14.

Synthesis of five workstreams in `data/deere/dealers/`: `dealer_credit_quality`, `dealer_inventory`,
`dealer_proxies`, `used_equipment`, `dealer_network`. Every load-bearing number below was re-derived
from the underlying CSVs or the corpus, not taken from the agents' summaries. Verification scripts:
`scripts/data/verify_dealer_leadlag.py`, `verify_leadlag_effn.py`, `verify_inventory_seasonality.py`,
`q3_segment_bridge.py`.

---

## 1. VERDICT

> **Deere's dealers are IMPROVING FROM STRESS — a two-speed channel: balance sheets are repaired and
> still healing fast; income statements are still at cycle trough. They are not impaired, and they are
> not the binding constraint on Q3 FY2026 shipments.**

The distinction the task demands — dealer stress versus end-customer stress — resolves cleanly and it
resolves in Deere's favour:

| | Dealer (channel) | End customer (farmer/contractor) |
|---|---|---|
| Credit stress, Q2 FY2026 | **0.05%** of wholesale receivables | **3.48%** of retail receivables |
| Non-performing | $4m on a $7,426m book | $742m on $41,857m = **1.77%** |
| Direction | improving, near-zero for four years | **deteriorating — worst of the CECL era** |
| Trend vs FY2022 trough | flat at ~nil | non-performing has **doubled** (0.89% → 1.77%) |

Source: `dealer_credit_quality.csv`, from Deere's own 10-Q/10-K credit-quality footnote.

This is the second regime described in the task framing, not the first. **Farmers are stressed; dealers
are well-capitalised and destocked. Deere can keep shipping.** A financially impaired channel would
under-order regardless of end demand — that is not what the data shows. What constrains Q3 is end
demand and Deere's own production plan, not dealer solvency.

The counterweight, and it is real: dealers are *solvent but unprofitable*. Dealer profitability sits at
a five-year low, ~30% below peak; only 72.5% of dealers forecast a profitable 2025, "the lowest over
the last 5 years by a significant margin"; nearly 50% reported worsening conditions in Q2 2026. A
solvent-but-unprofitable dealer replaces what it sells. It does not build position. **That removes
downside from Q3; it does not create upside.**

---

## 2. DIRECTION OF TRAVEL

**Improving, and fast on the balance sheet — roughly two years into a repair that is now largely
complete. Flat-to-still-deteriorating on the P&L and on sentiment.**

### Improving quickly (balance sheet, inventory, collateral)

| Measure | Peak / worst | Q2 FY2026 | Move |
|---|---|---|---|
| Trade receivables aged >12 months | **7%** (27 Apr 2025) | **1%** | −6pp in 4 quarters, back to 2015-19 baseline |
| Wholesale (floor-plan) receivables | $9,473m (28 Jul 2024) | **$7,426m** | −$2,047m; **−16.8% y/y** |
| Wholesale receivables ÷ quarterly sales | 97.5% (Q1 FY2025) | **55.6%** | −42pp |
| JDF trade-wholesale (used on dealer lots) | — | **"down over 15%" y/y** | management, 21 May 2026 |
| Used 100+hp tractor auction values | −13.1% y/y (Aug 2024) | **+3.0% y/y** (Jul 2026) | +16pp; positive every month since Jan 2026 |
| MY2022/23 8R used inventory | peak Mar 2025 | **−45%** | the specific cohort that blocked trades |
| Combine dealer inventory | 26% of TTM retail (Jul 2025) | **12%** (Apr 2026) | destocked through normal |

The single cleanest series is the aged trade receivable. Deere's FY2024 10-K named the cause of the 6%
reading explicitly — "increased dealer inventory levels" — so the collapse 7% → 3% → 3% → 2% → 1% is a
direct, Deere-authored read that dealer lots have cleared. It is not a proxy or an inference.

### Not improving (P&L, sentiment, and the customer behind the dealer)

- **Dealer P&L at trough.** In the CNH channel (Titan Machinery — *industry evidence, not Deere*),
  Q1 FY2027 net loss $(12.6)m, Ag segment pre-tax loss $(6.2)m, equipment gross margin 7.8% against
  12–14% in FY2023-24, FY2027 guided to a full-year adjusted net loss with Ag revenue down 15–20%.
- **Sentiment took another leg down.** Sandhills/Bloomberg Intelligence Q2 2026 dealer survey (July
  2026): ~50% report worsening conditions, 57% expect no change over twelve months.
- **Deere's own dealers plan for less.** Ag Equipment Intelligence 2026 Dealer Business Outlook
  (Jan 2026): Deere dealers forecast 2026 revenue **−7%**, the largest decline of any brand's dealers,
  against −4% for the all-brand channel.
- **The end customer is getting worse, not better.** Customer non-performing 1.77% and rising; Deere's
  Q2 FY2026 10-Q attributes the higher allowance to "higher expected losses on construction retail
  accounts."

**Speed read:** the balance-sheet repair is ~90% done and decelerating (there is little left to
de-stock). The P&L recovery has not started and management puts it in FY2027. The customer
deterioration is ongoing and is the live risk — but it sits in Financial Services, not in the
equipment shipment line.

---

## 3. QUANTIFIED EVIDENCE

### 3.1 Wholesale (dealer) receivable credit quality — Deere's own filings

`dealer_credit_quality.csv`; extracted from SEC EDGAR XBRL R-reports of the same 10-Q/10-K filings held
in the corpus, 16/16 spot checks against corpus text passed.

| Period end | FY/Q | Wholesale $m | Non-perf $m | 30+ past due $m | Stress % |
|---|---|---|---|---|---|
| 2020-02-02 | FY20 Q1 | 4,499 | 78 | 1 | **1.76** (COVID high) |
| 2021-10-31 | FY21 Q4 | 2,566 | 12 | 2 | 0.55 |
| 2022-10-30 | FY22 Q4 | 3,273 | 1 | 0 | 0.03 |
| 2023-10-29 | FY23 Q4 | 6,922 | 1 | 0 | 0.01 |
| 2024-07-28 | FY24 Q3 | **9,473** (peak) | 1 | 4 | 0.05 |
| 2025-04-27 | FY25 Q2 | 8,921 | 1 | 1 | 0.02 |
| 2025-07-27 | FY25 Q3 | 9,177 | 1 | 0 | 0.01 |
| 2025-11-02 | FY25 Q4 | 8,255 | 0 | 0 | **0.00** |
| 2026-02-01 | FY26 Q1 | 7,545 | 9 | 1 | 0.13 |
| **2026-05-03** | **FY26 Q2** | **7,426** | **4** | **0** | **0.05** |

Allowance against the entire $7.4bn wholesale book: **$2m**, unchanged for eight quarters. **No
wholesale write-offs disclosed in any quarter since FY2021** (blank in every roll-forward — recorded as
absent rows, not fabricated zeros). Through a downturn that cut PPA sales 17% in FY2025, dealers never
missed a payment to John Deere Financial at any material scale.

### 3.2 Dealer inventory as % of trailing-12-month retail — and why the headline misleads

`dealer_inventory.csv`, 51 observations per category, Jan 2013 – Apr 2026. **Caution when re-using this
file: `(series_id, period_end)` is not unique — `de_dealer_inv_pct_ttm_2wd_100hp` at 2024-07-31 carries
both Deere (31%) and an "Industry ex-Deere" comparator (70%). Filter on `entity` or the industry figure
contaminates the Deere series and corrupts every seasonal statistic.** I hit this and corrected it.

Seasonal means by month, 2013–2025 (re-derived independently):

| | Jan | Apr | Jul | Oct |
|---|---|---|---|---|
| 2WD 100+ hp | 27.8 | 30.3 | 30.4 | 23.6 |
| Combines | 12.8 | **18.9** | 23.8 | 5.7 |

Combines swing ~18 points a year because ~90% of volume is locked through the Early Order Program —
build-to-order, one delivery window, flushed to near-zero at fiscal year end. Row-crop tractors run a
rolling order book and anchor the dealer's trade ladder. **The two are not comparable at face value.**

Deviation from own-month norm, last eight quarters:

| Period | 2WD 100+hp | dev | Combines | dev |
|---|---|---|---|---|
| 2025-04 | 31 | +0.7 | 17 | −1.9 |
| 2025-07 | 31 | +0.6 | 26 | +2.2 |
| 2025-10 | 23 | −0.6 | 8 | +2.3 |
| 2026-01 | 27 | −0.8 | 18 | **+5.2** |
| **2026-04** | **30** | **−0.3** | **12** | **−6.9** |

### 3.3 Used values — the only hard data that falls *inside* the forecast quarter

Sandhills Global monthly US used-farm-equipment reports. May, June and July 2026 all map to Deere
FY2026 Q3. The July print was published **2026-08-11** — the freshest dealer-channel data available.

| Category (Jul 2026) | Inventory M/M | Inventory Y/Y | Auction M/M | Auction Y/Y |
|---|---|---|---|---|
| Tractors 100+ hp | −2.04% | **−16.75%** | −1.55% | **+2.97%** |
| Combines | −3.29% | −11.79% | −0.49% | **+0.38%** |
| **Sprayers** | **+2.63%** | −19.29% | **−3.97%** | **−5.14%** |
| Planters | +9.11% | −15.88% | −1.12% | +12.45% |
| Compact & utility tractors | −1.34% | −25.47% | +0.41% | +2.02% |

100+hp tractor auction values ran **+2.36% / +3.74% / +2.97% y/y** through May/June/July 2026 — firm
and positive for the whole quarter. Combine auction support decayed from +9.6% y/y (Jul 2025) to
**+0.38%**. Sprayers are the one actively deteriorating category, and they sit inside PPA.

**A trap worth recording:** the used-equipment agent caught a search engine serving July-**2025**
Sandhills figures as July 2026 (asking −6.28% y/y, auction −2.83%), byte-identical to the August 2025
publication. The verified 2026-08-11 print gives asking −0.04% and auction **+2.97%**. The bogus figures
say used values are falling; the real ones say they are up ~3% y/y. That flips the sign on residual risk.

### 3.4 Residual exposure — disclosed, small, shrinking

FY2025 10-K: a 10% fall in future market values of leased equipment, every unit returned, costs
**~$65m after dealer residual value guarantees** — 7.6% of the ~$860m FY2026 financial-services net
income guide, recognised as higher depreciation over remaining lease terms, not a one-quarter hit.
Series: $80m (FY21) → $40m → $90m → $75m → **$65m (FY25)** against a lease book that grew to $7,600m.
Unguaranteed residuals on sales-type/direct-finance leases are just $40m vs $867m guaranteed.
Equipment on operating leases was **flat sequentially at $7,514m** in Q2 FY2026; six-month remarketing
proceeds $1,019m vs $1,001m — no distressed disposal. **No residual impairment in the Q2 FY2026 10-Q.**

*Definition break:* FY2015–FY2020 sensitivities ($175–200m) are stated *before* dealer guarantees; from
FY2021 *after*. The 2020→2021 drop is mostly definitional, not de-risking.

### 3.5 Proxy financials — labelled correctly

**Titan Machinery (TITN) is a CNH Industrial / Case IH–New Holland dealer. It is ag-equipment CHANNEL
evidence, not a Deere signal.** Its balance-sheet cycle is informative about industry dealer economics;
its inventory is *not* informative about Deere dealer inventory (r=0.22, n=52 — essentially nothing).

- Inventory $1,527.8m (Jul 2024) → $914.8m (Apr 2026), **−40%**; floorplan payable $1,168m → $589m
  (**−50%**); floorplan interest $10.0m → $3.55m per quarter (−64%, 1.47% → 0.68% of revenue);
  equipment turns 1.45x → 2.14–2.27x. Management has **stopped targeting further reduction**.
- Still loss-making: Q1 FY2027 net loss $(12.6)m; FY2027 guided Ag revenue −15 to −20%.
- Parts & service carrying the dealer: P&S revenue −1.4% y/y vs equipment −16.5%; in the worst quarter
  P&S produced **91.4%** of all gross profit.

**Cervus Equipment (TSX:CERV)** — the only public pure-play Deere dealer that ever existed, acquired by
Brandt 2021, last reported FY2020 — calibrates the thresholds: *stressed* = gross margin <15%, negative
pre-tax, used turns <2x, impairments ~2% of revenue (FY2019: 14.9%, −CAD10.4m, 1.78x, CAD24.0m).
*Healthy* = 16.5% margin, 2.87x used turns (FY2020). TITN today sits in the stressed configuration.
**This is six-year-old data on a company that no longer exists — a yardstick, not a signal.**

No financials exist for any private Deere group (RDO, Ag-Pro, Van Wall, Sydenstricker Nobbe, Hutson,
Ziegler, Papé, Brandt). None were fabricated. Deere's own disclosures carry the quantitative load.

### 3.6 Network structure

US+Canada ag locations **rose** 1,522 (FY2015) → 1,600 (FY2025), +5.1%; comparable ag+C&F 1,949 →
2,050. The network is not shrinking — ownership is concentrating (~170 US groups, 82% of locations in
chains of 7+). *A definitional trap: the as-reported total appears to collapse 2,359 → 1,981 at FY2018;
that is turf-only locations leaving the definition, proven by exact reconciliation. Plotting it straight
manufactures a dealer collapse that never happened.* Zero dealer bankruptcies found in 2025-26, and all
2026 M&A is strategic, not distressed — **but a consolidated network would not show failures even under
real strain**, so absence of bankruptcy is weak evidence. The stronger tells are the inventory and
receivable-ageing series above, and they agree.

---

## 4. LEAD/LAG — the sample cannot establish it

**Direct answer: no. Dealer stress does not reliably lead Deere shipments at any lag that this sample
can establish, and the one relationship that looks predictive fails every robustness test.**

### 4.1 Dealer past-dues LAG shipments — they do not lead them

Cross-correlations against Deere worldwide net sales y/y (`verify_dealer_leadlag.py`):

| X (stress measure) | best lag | r | n |
|---|---|---|---|
| Trade receivables >12m % | **L0** | −0.52 | 43 |
| Customer (retail) stress % | **L0** | −0.58 | 22 |
| Customer non-performing % | **L0** | −0.56 | 22 |

All three peak contemporaneously and decay monotonically at every forward lag. Run in reverse, **sales
growth leads the ageing metric by one quarter, r = −0.639, n = 42** — stronger and better-signed than
any forward lag. Aged dealer trade credit is a *consequence* of falling shipments, not a warning of
them. It confirms a downturn has bitten; it does not predict one.

### 4.2 The floor-plan balance "lead" is one cycle, not nineteen observations

The headline claim in the credit workstream is that wholesale-receivable y/y leads net-sales y/y by four
quarters at **r = −0.885, n = 19**. I reproduced it exactly (slope −0.308, intercept +12.64, residual SD
9.3pp). **It cannot bear weight.** Three tests:

| Test | Result |
|---|---|
| AR(1) of predictor / target | **+0.927 / +0.854** — overlapping y/y windows, heavily autocorrelated |
| **Bartlett-adjusted effective n** | **≈ 2.2** — roughly *two* independent observations, not 19 |
| Drop the 2023-26 cycle (obs before 2024) | r falls to **−0.523, n=9** |
| Keep only 2023+ | r = −0.922, n=14 — the entire result lives here |
| Reverse direction: sales(t−4) → wholesale(t) | **r = +0.565, n=23** — the causality runs both ways |

The credit agent's own robustness check (r=−0.871 on n=13) drops FY2025-26 but *retains the 2023 build*,
so it does not remove the cycle that generates the correlation. The honest out-of-cycle number is −0.52
on nine points.

The reverse-direction result is the tell: shipments mechanically create dealer floor-plan receivables
with a lag (Deere ships → dealer floor-plans it → the receivable sits until retailed). So "wholesale
balance leads sales" and "sales lead wholesale balance" are the same inventory identity observed from
two ends of **one** build-and-bust. Fitting a slope to it and extrapolating is curve-fitting.

**Consequence for the forecast: I reject the regression's output.** That fit implies Q3 FY2026 revenue
growth of **+13.6% ±9.3pp → ~$13.7bn**, i.e. above the top of our $11,900–12,800m range. Leave-one-out
gives +12.1% to +15.3%, so it is stable — *stably wrong*, because it is stably fitted to two effective
observations of a single cycle whose extreme amplitude inflates the slope. **No dealer series in this
dataset supports a $13.7bn Q3.** The credit agent flagged scepticism about the point estimate but still
carried "a sign and a floor" forward; on an effective n of 2.2, even the sign is not established.

**What survives:** the *mechanism* — dealer inventory build precedes shipment decline and drawdown
precedes recovery — is causally sound, disclosed by Deere, and corroborated by 117 corpus mentions of
"underproduction". Use it as a **narrative constraint** (the channel is no longer a source of downside),
never as a **numerical predictor**.

**Also flagged and not used:** `de_wholesale_stress_pct` vs sales, r=+0.61 at L5-6 — the series is a
near-constant 0.01–0.13% since FY2022; the "correlation" is the 2020-21 decay lining up with the
post-COVID boom. TSCO revenue r=0.94 on n=7 is a shared-downtrend artifact. TITN equipment turns r=0.80
on n=15 spans one cycle ≈ one independent observation.

---

## 5. Q3 FY2026 REVENUE IMPLICATION

### 5.1 The answer

> **Neither the high end nor the low end — the dealer evidence argues for the MIDDLE, and its main
> contribution is to COMPRESS the range rather than shift the centre. It rules out both tails.**
>
> **Keep the central case at ~$12,350m. Narrow the range from $11,900–12,800m to roughly
> $12,150–12,600m, with a slight tilt to the upper half (~$12,400m).**

### 5.2 Why — the segment bridge (`scripts/data/q3_segment_bridge.py`)

Deere's FY2026 guidance has been unchanged since 21 May 2026. Running it against actuals:

| Segment | FY2025 | H1 FY2026 actual | FY2026 guide | Implied H2 y/y | Implied Q3 FY2026 |
|---|---|---|---|---|---|
| PPA | 17,311 | 7,666 (**−7.6%**) | −5% to −10% | **−2.6% to −12.2%** | 3,752 – 4,162 |
| SAT | 10,224 | 5,653 (+19.2%) | +~15% | +11.4% | 3,369 |
| CF | 11,382 | 6,460 (+30.7%) | +~20% | +11.8% | 3,419 |
| FS + other | — | — | FS NI ~$860m | ~flat | ~1,611 – 1,661 |
| **Total** | | | | | **$12,150 – 12,610m** |

The guidance arithmetic alone brackets **$12.15–12.6bn**. Our $12,350m central case sits near its
midpoint and implies PPA **−8.7%** y/y — comfortably inside the guide-implied H2 PPA band. The stated
range's tails are the problem:

- **$11,900 (low end) requires PPA −19.2%** — *worse* than Q3 FY2025's −16%. That demands an
  incremental destock. **The dealer inventory data says there is nothing left to destock in North
  America**, and Q3 is structurally the ratio *peak*, not the cut (Deere concentrates the flush in
  Jul→Oct: mean −18.1 points for combines, −7.3 for 2WD). The low end is close to excluded.
- **$12,800 (high end) requires PPA +1.8%** — PPA *growth* against a −15% to −20% NA large-ag industry.
  That demands channel refill. **Loss-making dealers planning −7% revenue do not restock**; management
  puts recovery in FY2027. The high end is close to excluded.

### 5.3 An independent cross-check that lands in the same place

The base-year destock cushions the y/y decline. Q3 FY2025 shipments = retail − destock; Q3 FY2026
shipments ≈ retail (wedge now ~zero). With NA large-ag retail down ~17%:

- if the Q3 FY2025 destock was ~5% of retail → PPA y/y = 0.83/0.95 = **−12.6%**
- if it was ~10% of retail → PPA y/y = 0.83/0.90 = **−7.8%**

Add currency (+3 points in Q2 FY2026) and price (+1) and volume-driven PPA of −12% to −16% maps to
reported PPA of roughly **−8% to −12%** → total revenue **$12,209 – 12,401m**. Two independent routes
converge on the same place.

### 5.4 The critical sub-question: is combine destocking finished while large tractors run on?

**Half right, and the half that is wrong is the expensive half.**

**Combines: destocking is finished AND has overshot.** April 2026 at 12% is **−6.9 points below its
April seasonal norm of 18.9** — the lowest April combine reading anywhere in the corpus (prior low 13%,
April 2016). And the y/y "17 → 12" *understates* it, because April 2025 was itself −1.9 below normal.
The cut was violent and recent: deviations ran +2.3 (Oct-25), **+5.2 (Jan-26)**, then **−6.9 (Apr-26)** —
a ~12-point seasonally-adjusted reduction in a single quarter, against a season that normally *builds*.
**That destock is already inside the reported Q2 FY2026 numbers, not still ahead.** Correct: the
combine shipment headwind is removed for Q3.

**Large tractors: the premise is wrong. 30% is not incomplete destocking — 30% IS the target.**
The April norm is 30.3; April 2026 printed 30.0, a deviation of **−0.3**. Seven of the last eight
quarters sit within ±1.0 point of the seasonal norm. That is the fingerprint of a company running the
line to a target, not of a destock with further to run. The ratio "barely moved" because **the ratio is
the control variable**. The absolute units moved enormously: management says high-hp tractor and combine
units are "down more than 50% from their mid-2024 peak," and 220+hp units at FY2025 close were the
lowest in over 17 years.

The mechanism matters for the money: **TTM retail — the denominator — is falling ~15–18%.** Holding the
ratio flat at 30% while the denominator falls 17% means absolute dealer tractor inventory fell ~17%.
That is precisely "produce in line with retail demand," repeated on three consecutive calls. So
large tractors are **neither a drag nor a tailwind** in Q3 — shipments track retail down, no incremental
destock, no restock.

**Net for the PPA line:** the destock wedge that produced Q3 FY2025's −16% PPA has closed to
approximately zero in North America. Both categories are done. Neither generates a restock impulse.
So PPA should be down y/y in Q3 — but **materially less than −16%** — which is exactly the −8% to −12%
the bridge and the cross-check both produce. Trading the low end for the middle on PPA is worth roughly
**$300–450m of revenue**, which is the practical value of this distinction.

### 5.5 What is NOT supported, and residual Q3 risks

- **No $13.7bn.** The wholesale-receivable regression that implies it fails on effective n ≈ 2.2 (§4.2).
- **No residual write-down.** Used values rose through the entire quarter on the dominant category;
  disclosed sensitivity is ~$65m for a full 10% decline; lease book flat; no Q2 impairment. The ~$860m
  FS net income guide is not at risk *from this channel*.
- **Less-bad PPA price realization.** Q3 FY2025's negative large-ag price was explicitly attributed to
  "actions taken to address used inventory in North America" (incremental pool funds). Used inventory
  is now −16% y/y with firm values, so that subsidy has less work to do. Q2 FY2026 PPA price was +1.
  Directionally supportive of the 11–13% guided PPA margin band.
- **Residual negatives, both specific:** (a) **Brazilian combines** — Deere pre-announced
  underproduction in "our second and third quarters," a known, quantified, Q3-specific negative inside
  PPA; (b) **sprayers**, the one used category actively deteriorating (auction −5.14% y/y, inventory
  building M/M), also inside PPA; (c) **Financial Services provision** — customer non-performing 1.77%
  and rising raises the odds of a larger Q3 provision (retail-notes provision $62m in Q2 FY2026 vs $55m
  LY). Note this hits FS net income, **not** the revenue line we are forecasting.
- **Timing caveat, stated plainly:** no equipment-dealer proxy covers Deere's Q3 FY2026. TITN's latest
  quarter overlaps Deere's **Q2**; TITN's May–Jul quarter reports *after* the 20 August call. The only
  in-window public data are Sandhills used values (May/Jun/Jul 2026) and Tractor Supply's −1.5% comp for
  the quarter ended 2026-06-27 — rural discretionary, not equipment demand.

---

## 6. DIVERGENCES

**6.1 An arithmetic error carried by two agents — corrected.** Both `public-dealer-proxies` and
`dealer-inventory-series` state H1 FY2026 PPA ran "−16% (Q1) and −14% (Q2)". **Q1 FY2026 PPA was
+3%** — $3,163m vs $3,067m (`filings/2026-02-26__de-us-20260226-q1-10q__636995.md`). H1 PPA is **−7.6%**,
not ~−15%. Both agents then concluded the unchanged guide "requires H2 PPA roughly flat to only modestly
down." It does not: from a −7.6% H1, the guide requires H2 PPA of **−2.6% to −12.2%**. The error made
the guide look far easier than it is, and made the proxies agent's "tension with guidance" argument look
sharper than it is. The corrected bridge is §5.2.

**6.2 Deere's own disclosures vs the channel proxy — and the proxy loses.** TITN's balance-sheet destock
(−40% inventory) looks like Deere's (combines 17% → 12%), but the correlation between TITN inventory and
Deere revenue is **r=0.22, n=52 — essentially nothing**. Channel inventory cycles are brand- and
allocation-specific. The agreement is coincidence of cycle phase, not evidence. **TITN is a CNH dealer;
its destock is industry evidence, its P&L is industry evidence, and neither is a Deere dealer signal.**
Where the two conflict, Deere's own filings win.

**6.3 Dealer credit improving vs end-customer credit at its worst.** The widest divergence in the data:
dealer stress 0.05% against customer stress 3.48% — a ratio of ~64x. These have **opposite** forecast
implications and must not be netted. Channel health supports shipments; customer deterioration caps
retail recovery and pressures FS provisions.

**6.4 Balance sheet vs income statement.** Every balance-sheet measure says improving; every P&L and
sentiment measure says trough. Both are true. Solvency governs whether dealers *can* order; profitability
governs whether they order *ahead of* retail. They can; they won't.

**6.5 Falling used inventory is partly mechanical, not demand.** With new retail down ~18%, fewer
trade-ins arrive on lots, so used inventory falls without any retail strength. Do not read the full
−16.75% used-tractor inventory decline as sell-through.

**6.6 Combines: Deere's own used-inventory destock stalled while new-inventory destock completed.**
Deere's used combine inventory has been stuck at ~−15% vs the March 2024 peak for two consecutive
quarters (−25% → −15% → "mid-teens"), and combine auction values decayed from +9.6% to +0.38% y/y —
while *new* combine dealer inventory cut through its seasonal norm to a corpus low. New combines are
clean; used combines are not. Combines are the likeliest disappointment inside PPA.

**6.7 Zero bankruptcies vs worsening sentiment.** Not a contradiction — a consequence of structure. A
consolidated network (82% of locations in chains of 7+, pooled treasury, multi-region) expresses strain
as **order deferral and floorplan discipline**, not as failures. Absence of bankruptcy is therefore weak
evidence of health, and the sentiment survey is not evidence of impending failure.

**6.8 A slide-deck trap that inverts a reading.** The Q2 FY2026 deck's April retail table has stripped
minus signs — industry figures rendered "12% / 4% / 14% / 24% / 5%" are **negative**. Deere's adjacent
column reading "Down more than the industry" against a supposed +14% is incoherent, and −24% 4WD matches
AEM's independent −24.6% YTD. Treated as negative throughout.

---

## 7. ONGOING TRACKER

### 7.1 Tier 1 — Deere's own disclosures (highest signal, quarterly, free)

| Series | Where | Freq | Real signal | Noise |
|---|---|---|---|---|
| **Trade receivables aged >12 months** | 10-Q/10-K receivables note | Q | **≥3% for two consecutive quarters** = inventory re-building on dealer lots. Deere names the cause itself. | 1–2% is the 2015-19 baseline; ±1pt is nothing |
| **Wholesale receivables, total + y/y** | credit-quality footnote | Q | **y/y turning positive** = channel restocking → the FY2027 recovery is real | seasonal: Q2/Q3 build, Q4 flush |
| **Wholesale non-performing + 30+ past due** | same | Q | **>$25m, or any 30+ past due >$10m** = genuine dealer impairment, first since COVID | $1–9m is noise on a $7.4bn book |
| **Dealer inventory % of TTM retail, by category** | earnings slide deck | Q | **compare to the month norm, never y/y or cross-category**: 2WD Apr 30.3 / Jul 30.4 / Oct 23.6; combines Apr 18.9 / Jul 23.8 / Oct 5.7. **Deviation >±3 points** = policy change | ±2 points is normal management |
| **Customer non-performing %** | credit-quality footnote | Q | **>1.80% and rising** = end-demand recovery is capped; FS provision risk | quarterly wiggle of ±0.10pp |

### 7.2 Tier 2 — external, monthly

| Series | Source | Freq | Real signal |
|---|---|---|---|
| Sandhills used values, tractors 100+hp | monthly report | M | **auction y/y back below 0% for 2+ months** = trade ladder re-blocking. Currently +3.0% |
| Sandhills used inventory, 100+hp | same | M | **y/y turning positive** ends the 14-month destock |
| Sandhills sprayers & combines | same | M | already the weak categories — watch for spread to tractors |
| AEM US ag tractor retail | AEM | M | the demand denominator; **improvement to better than −10% y/y** would precede restocking |
| Ag Equipment Intelligence dealer outlook | annual, Jan | A | Deere-dealer revenue plan; −7% for 2026. **A 2027 plan better than −2%** signals restock |

### 7.3 Tier 3 — proxies, correctly labelled

TITN (**CNH channel, not Deere**): use as a *coincident* read on PPA-type revenue direction (r=0.63,
n=44; decays to 0.54 at +1q — it is not leading). **Never** use TITN inventory to infer Deere dealer
inventory (r=0.22, n=52). Watch TITN equipment gross margin recovering through **10%** and Ag same-store
sales turning positive as industry-level confirmation. TSCO is sentiment colour only.

### 7.4 Specific, falsifiable checks for the 20 August 2026 call

From the seasonal transition (median Apr→Jul move: **0.0** points for 2WD, **+5.5** for combines):

| Check | Prediction | Reading |
|---|---|---|
| 2WD 100+hp, July 2026 slide | **~30%** (vs 31% LY) | >33% = shipped ahead of retail; <27% = further destock, PPA disappoints |
| Combines, July 2026 slide | **~17–18%** (vs 26% LY) | **>18% = shipped into the channel** — better Q3, worse Q4. **<15% = destock continued, Q3 PPA disappoints** |
| Trade receivables >12m | holds at **1%** | ≥3% = re-building |
| Wholesale non-performing | **≤$10m** | >$25m = first real dealer impairment |
| Customer non-performing | ~1.77% | **>1.80%** = customer problem outrunning channel repair |
| PPA price realization | positive | negative again = pool funds back, used problem returned |

---

## 8. LIMITATIONS

1. **No Q3 FY2026 actuals exist.** Everything here is an ex-ante read on data ending 3 May 2026 (Deere)
   and 31 July 2026 (Sandhills).
2. **No public pure-play North American Deere dealer exists.** Cervus was acquired by Brandt in 2021;
   RDO, Ag-Pro, Van Wall, Sydenstricker Nobbe, Hutson, Ziegler, Papé and Brandt are private and file
   nothing. **Titan Machinery is CNH, not Deere.** No financials were fabricated for any private group.
3. **No dealer-level or regional dispersion data exists anywhere.** Deere reports the wholesale
   portfolio only in aggregate. A pocket of stressed dealers would be invisible — though $4m
   non-performing on $7,426m bounds the aggregate problem tightly.
4. **The lead/lag question is not answerable from this sample.** Effective n ≈ 2.2 after autocorrelation
   adjustment. Reported as a mechanism, not a coefficient. See §4.2.
5. **No dealer/wholesale credit split exists before CECL adoption (FY2021).** Pre-2021, Deere disclosed
   only "Retail Notes" vs "Other", and "Other" bundles dealer wholesale with revolving/operating loans.
   Those rows carry `entity='mixed'` and are **not** a dealer series.
6. **Definitional break at FY2021** — non-performing moved from 120 days to 90 days. Compare directions
   within each regime only; cross-regime level comparisons are invalid.
7. **Segment-level (PPA/SAT/CF) quarterly sales are absent from the credit CSV**, so the lead/lag test
   used total worldwide revenue — which includes C&F and Financial Services and is therefore not a clean
   test against PPA. The §5.2 bridge uses segment data read directly from the filings instead.
8. **2019–2021 used-value indices are missing** (Sandhills' reachable archive starts ~2022); March 2026
   is absent (HTTP 403). Machinery Pete and Tractor Zoom figures were excluded as unverifiable — blanks,
   not guesses. Dealer sentiment surveys publish no sample sizes.
