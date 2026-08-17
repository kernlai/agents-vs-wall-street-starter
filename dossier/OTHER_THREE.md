# OTHER_THREE — Final forecasts for Home Depot FY2026Q2, Analog Devices FY2026Q3, Hays plc FY2026

**Prepared 16 August 2026.** Corpus frozen 14 August 2026.
Author: synthesis agent, working from the six research dossiers in
`/Users/cor/Documents/projects/agents-vs-wall-street-starter/dossier/{home-depot,analog-devices,hays}/`
plus direct re-verification of every prior-year actual against the primary corpus documents.

---

## 0. NONE OF THE THREE HAS REPORTED THE TARGET PERIOD

| Company | Target period | Period end | Reports | Status |
|---|---|---|---|---|
| Home Depot | FY2026 Q2 | 2 Aug 2026 | **Tue 18 Aug 2026**, 09:00 ET | NOT REPORTED (2 days after cut-off) |
| Analog Devices | FY2026 Q3 | 1 Aug 2026 | **Wed 19 Aug 2026**, 07:00 ET | NOT REPORTED (3 days after cut-off) |
| Hays plc | FY2026 | 30 Jun 2026 | **Thu 20 Aug 2026**, ~07:00 BST | NOT REPORTED (4 days after cut-off) |

All three fiscal periods are **closed**, but no audited/reported figure for any of the nine metrics
exists in the corpus or on the open web. Every number in the "central/low/high" columns below is a
FORECAST. I found nothing that could be mistaken for a target-period actual except the two documented
traps below, both of which I rejected.

**Corpus/web defects confirmed and handled:**
1. `analog-devices/INDEX.md` labels `filings/2026-05-20__adi-us-20260520-q2-10q__1040607.md` as
   "Q3 2026". It is the **Q2 FY2026 10-Q** (quarter ended 2 May 2026). Not used as Q3 data.
2. Several HD transcripts carry period front-matter off by a year (the 19 May 2026 Q1 FY2026 Q&A is
   tagged "Q1 2027"; a Sept-2025 fireside chat is tagged "Q3 2026"). All HD figures taken from
   document body text with an explicit dateline.
3. A web item (itiger.com) surfaces **ADI's Q3 FY2025 actuals** ($2.88bn revenue / $2.05 adj EPS)
   with an August-2026 framing. Those are the prior year. Anchoring on them would be a ~26%/~38% error.
4. Minus-sign stripping: checked the tables I actually used. HD 8-K tables render negatives as `(3.3)%`
   correctly; the Hays Q4 statement renders them as `(5)%` correctly; ADI margin tables carry explicit
   bps/% labels that reconcile to the narrative. No stripping found in the load-bearing tables.

---

## 1. THE NINE NUMBERS

| # | Ticker | Metric | Units | **Central** | Low | High | Consensus | Δ vs consensus |
|---|---|---|---|---|---|---|---|---|
| 1 | HD | Net sales | USDm | **47,550** | 46,900 | 48,200 | 47,350 (spread 47,240–47,500) | +0.4% |
| 2 | HD | Adjusted diluted EPS | USD/sh | **4.71** | 4.55 | 4.87 | 4.71 (Zacks) / 4.73 (S&P) | at consensus |
| 3 | HD | Comparable sales, total company | % pts | **+0.5** | −0.7 | +1.6 | ~+0.8 (derived, none published) | −0.3pp |
| 4 | ADI | Revenue | USDm | **3,970** | 3,890 | 4,070 | 3,925 (3,920–3,930) | +1.1% |
| 5 | ADI | Adjusted diluted EPS | USD/sh | **3.40** | 3.26 | 3.58 | 3.33 | +$0.07 |
| 6 | ADI | Adjusted gross margin | % pts | **72.7** | 71.9 | 73.4 | ~72.5 (derived from CFO commentary) | +0.2pp |
| 7 | HAS | Net fees | GBPm | **903.5** | 895.0 | 911.0 | 902.4 (894.0–914.0) | +0.1% |
| 8 | HAS | Pre-exceptional basic EPS | GBp (pence) | **1.14** | 1.04 | 1.25 | 1.13 (0.93–1.40) | +0.01p |
| 9 | HAS | Pre-exceptional operating profit | GBPm | **46.2** | 45.4 | 47.2 | 45.3 (40.0–46.1) | +£0.9m |

**Units discipline check.** Percentages are in POINTS (+0.5 = +0.5%, 72.7 = 72.7%). Hays EPS is in
PENCE (1.14 = 1.14p, not £0.0114). Money is in the stated millions (47,550 = $47.55bn; 903.5 = £903.5m).
All EPS/margin metrics are on the **adjusted / pre-exceptional** basis, never GAAP/statutory.

---

## 2. PRIOR-YEAR ACTUALS (validation baseline) — all re-verified against primary documents

| Ticker | Metric | Prior-year actual | Period | Source |
|---|---|---|---|---|
| HD | Net sales | **45,277** USDm | Q2 FY2025, 13 wks ended 3 Aug 2025 | `home-depot/filings/2025-08-19__hd-us-20250819-q2-8k__143666.md` line 99; confirmed via SEC XBRL CIK0000354950 `RevenueFromContractWithCustomerExcludingAssessedTax` 2025-05-05→2025-08-03 = 45,277,000,000 |
| HD | Adjusted diluted EPS | **4.68** USD | same | same 8-K line 246 (GAAP $4.58 + $0.14 intangible amortisation − $0.04 tax) |
| HD | Comparable sales, total company | **+1.0** pp | same | same 8-K line 120 (US comps +1.4%; FX −40bp) |
| ADI | Revenue | **2,880** USDm ($2,880.348m) | Q3 FY2025, 13 wks ended 2 Aug 2025 | `analog-devices/filings/2025-08-20__adi-us-20250820-q3-8k__155976.md` lines 56/164; SEC XBRL CIK0000006281 confirms $2,880,348,000 |
| ADI | Adjusted diluted EPS | **2.05** USD | same | same 8-K lines 67/349 (GAAP $1.04) |
| ADI | Adjusted gross margin | **69.2** pp | same | same 8-K lines 64/320 (GAAP GM 62.1%) |
| HAS | Net fees | **972.4** GBPm | FY2025, yr ended 30 Jun 2025 | `hays/filings/2025-08-21__has-ln-20250821-filing__143845.md` line 33 |
| HAS | Pre-exceptional basic EPS | **1.31** GBp | same | same, lines 39/503/816 (£20.9m / 1,590.2m shares). Statutory basic EPS was (0.49)p |
| HAS | Pre-exceptional operating profit | **45.6** GBPm | same | same, lines 34/496 |

Two of the three research pairs cited slightly different Hays FY25 filenames
(`...20250821-filing__143845.md` vs `...20250821-h2-8k__143890.md`); both contain the same Preliminary
Report figures. I verified against `__143845.md` directly.

---

## 3. HOME DEPOT — FY2026 Q2 (13 weeks ended 2 August 2026)

### 3.1 Net sales — **$47,550m** (consensus benchmark 47,350; Zacks 47,500, S&P Global 47,240)

Two independent builds converge just above consensus.

**Bridge from the prior year (all non-comp items are ESTIMATES except the base):**
```
Q2 FY2025 net sales (FACT)                                        45,277
+ GMS, 100% non-comp until Sept 2026                              +1,450   (Q1 FY26 was $1,300m over 13 wks per 10-Q MD&A;
                                                                            May–Jul is the seasonal peak for interior building products)
+ Mingledorff's (42 HVAC branches, closed 11 May 2026)              +200   (~12 of 13 weeks owned, at HVAC seasonal peak; revenue undisclosed)
+ new stores / new SRS branches / tuck-ins                          +400   (Q1 FY26 residual was ~$379m; Q2 is a ~14% larger quarter)
+ comparable-sales effect @ +0.5%                                   +220
------------------------------------------------------------------------
= net sales                                                       47,547
```
**Seasonality cross-check.** Q2/Q1 sales ratio was 1.136 (FY2025), 1.150 (FY2024 ex-SRS), 1.152 (FY2023).
$41,765m × 1.136 = $47,445m, plus Mingledorff's (not in the Q1 base) ≈ **$47,645m**.

**Why above consensus, and why only modestly.** The articulable edge is entirely inorganic:
Mingledorff's closed eight days into the quarter and *after* the FY2026 guide was set, its revenue was
never disclosed, and most sell-side models will not carry it; GMS sits at its seasonal peak in the
May–July window. Against that, I model a comp *below* the consensus-implied level, which claws most of
the gap back. The published consensus spread (47,240–47,500) is itself ~1.1 scoring floors wide
(floor = 0.5% ≈ $238m), so the choice inside it barely matters; falling outside it is the real risk.
$47,550 sits at the top of the published range rather than beyond it.

### 3.2 Adjusted diluted EPS — **$4.71** (consensus 4.71 Zacks / 4.73 S&P; benchmark 4.72)

**Sit at consensus. I have no edge here and the floor is punishing** (0.5% of result ≈ $0.024).

Bottom-up at $47,550m of sales:
```
Gross margin 32.91% (−50bp YoY; mgmt: Q2 pressure "not quite the degree" of Q1's −77bp)  15,649
Opex 18.98% of sales (Q2 FY25 18.93%; +5bp of deleverage)                               (9,025)
Operating income (13.93%, −55bp YoY)                                                      6,624
Interest and other, net (FY guide ~$2.3bn/yr; Q2 FY25 was $550m)                           (580)
Pre-tax                                                                                   6,044
Tax @ 24.3% (FY guide)                                                                  (1,469)
Net earnings / 996m diluted shares → GAAP diluted EPS                                     $4.59
+ acquired-intangible amortisation, after tax                                             $0.13
------------------------------------------------------------------------------------------------
Adjusted diluted EPS                                                                      $4.72
```
Rounding down to **$4.71** to match the most widely syndicated consensus print and to respect two
specifics: management's warning that costs "have at least moved towards a bias towards an increase"
(fuel, new tariffs, with tariff refunds "immaterial to date"), and HD's recent record of small *misses*
versus the street (Q2 FY2025 $4.68 vs ~$4.71; Q3 FY2025 a clear miss) rather than beats. Gross margin is
the whole swing: each 10bp ≈ $0.036 of EPS, so the guided −40bp to −70bp band alone spans $4.62–$4.76.

**BASIS TRAP — do not submit GAAP.** HD's sole adjustment is amortisation of acquired intangible assets
including its tax effect. Nothing else. Run-rate: $139m pre-tax in Q2 FY2025 → $171m in Q1 FY2026
($119m SRS/GMS + $52m Primary) → ~$175–185m expected in Q2 FY2026 ≈ $0.13/share after tax. FY guidance
assumes ~$0.50 after-tax for the year, of which $0.13 landed in Q1. **Adjusted ≈ GAAP + $0.13.**
Submitting the GAAP number (~$4.58–4.59) would miss by ~13c ≈ 5.5 floors.

### 3.3 Comparable sales, total company — **+0.5 percentage points** (derived consensus ~+0.8)

This is the only genuinely two-sided call in the HD set, and there is **no published headline comp
consensus** in free sources. Five approaches:

| Method | Result |
|---|---|
| Two-year stack held flat from Q1 FY2026 (+0.3) against a +1.0 lap | **−0.7%** |
| Two-year stack plus the building-materials category's +0.71pp two-year improvement | **~0.0%** |
| Additive bridge from Q1's +0.6% (below) | **+0.4% to +0.9%** |
| Implied from Zacks' store metrics (transactions −1.5% × ticket +2.7%, less new stores, plus SRS) | **+0.7% to +0.9%** |
| Implied from the revenue consensus after the non-comp bridge | **+0.3% to +0.6%** |

**Additive bridge:** Q1 FY2026 +0.6%; storm-lap headwind shrinks from −56bp to ~−20bp (**+0.3pp**);
SRS laps a record-low hail/hurricane quarter starting in Q2 (**+0.2pp**); FX tailwind falls from +55bp
to ~+15bp (**−0.4pp**); the underlying compare hardens by 1.3pp — Q2 FY2025's +1.0% is the highest comp
in nine quarters and July 2025 alone was +3.1% (**−0.4pp**); category momentum (**+0.3pp**). Net ≈ +0.6%,
and I shade to **+0.5%** because the two-year-stack family of methods clusters at 0.0% or below.

**The two sides.** Bull: FRED `RSBMGESD` (building materials & garden equipment dealers) ran +5.97% y/y
in May–Jul 2026 vs +3.40% in Feb–Apr, with July the highest print in the series; management said early
May engagement looked "very similar to the beginning of both February and March"; storm and FX
mechanics are net positive sequentially. Bear: the CFO said flatly *"We are not looking at a marked
improvement in underlying demand. We are looking at a higher comp in the second half of the year, and
that is solely driven by a return to normal storm activity"*; the 30-yr mortgage rose 6.30% → 6.67%
through the quarter; existing home sales SAAR fell 4.19m → 4.13m → 4.06m; transactions have been
negative for eleven straight quarters.

**Weighting note on the category data.** The HD-comp-to-category spread has flipped sign quarter to
quarter (−0.7pp, +2.35pt, −2.8pp), the series is nominal (tariff price inflation inflates it) and NAICS
444 includes pro lumber dealers HD does not resemble. I used the *two-year* read (+0.71pp), not the raw
+2.6pp one-year acceleration, which would imply an incredible +3.2% comp.

**Scoring posture.** The 0.5pp floor is generous relative to the plausible dispersion, so a 0.3pp
deviation below the derived consensus is cheap: if the print lands at consensus we score ~0.6; if it
lands at 0.0% or negative — which three of five methods point at — we win materially. Sign risk is real
but a negative print would break five consecutive flat-to-positive quarters, so positive is the base case.

**Post-freeze item worth naming:** on 12 Aug 2026 CEO Ted Decker took a temporary medical leave; Campbell
and McPhail jointly run the office of the CEO. Non-financial, but it lowers the odds of a guidance raise
on 18 Aug and argues for a conservative tone. It does not change the reported quarter.

---

## 4. ANALOG DEVICES — FY2026 Q3 (13 weeks ended 1 August 2026)

Company guidance, not consensus, is the primary anchor here — and the two are only ~0.6% apart.

> "For the third quarter of fiscal 2026, we are forecasting revenue of **$3.9 billion, +/- $100 million**.
> … adjusted operating margin of approximately **49.0%, +/-100 bps** … adjusted EPS to be
> **$3.30, +/-$0.15**." — Q2 FY2026 8-K Ex-99.1, 20 May 2026

Tax guided 12–14%. Segment guide: industrial and automotive up mid-to-high single digits q/q,
communications fastest at low-to-mid teens, consumer down single digits, **flat channel inventory weeks**.

### 4.1 Revenue — **$3,970m** (consensus 3,925; guide midpoint 3,900)

Three methods bracket the answer:

| Method | Result |
|---|---|
| Segment bridge at the *midpoints* of the stated q/q ranges | $3,863m |
| Segment bridge at the *tops* of the stated ranges | $3,948m |
| Historical mean beat vs midpoint applied (+3.2% over 4 qtrs; +$100m over 6 qtrs) | $4,025m (above the guided high end) |

**The edge is ADI's guidance-beat record, and the street is not taking it.** ADI beat its own revenue
midpoint in 17 of the last 18 quarters (only miss: FY23 Q3, −$24m, at the down-cycle inflection); the
mean beat over the last six quarters is +$100m, i.e. **exactly the width of the band** — ADI lands on
average *at the high end* — and it exceeded the high end in two of the last four. Consensus sits only
+$25m above the midpoint. Supporting: record bookings across all three B2B markets, positive
book-to-bill called out in automotive, channel inventory lean at 6–7 weeks and *declining* with flat
weeks assumed in the guide (any restock is unmodelled upside), and data centre >75% of comms growing
>90% y/y.

**Why I stop short of $4,025m.** Puccio at the 2 June 2026 conference: automotive demand accelerated
*"literally in the last month of the quarter … that we were expecting to come in Q3"* — some Q3
automotive revenue was pulled into Q2. Add: consumer guided down with memory named as a choke point;
internal utilisation at optimum so unplanned upside must be sourced externally with lead time; and the
beat has been noisy and non-monotonic (+4.7%, +2.5%, +1.9%, +3.5%). $3,970m sits between the
segment-bridge top ($3,948m) and the historical extrapolation ($4,025m), leaning to history.
That is +1.1% versus consensus and +1.8% versus the midpoint.

### 4.2 Adjusted diluted EPS — **$3.40** (consensus 3.33; guide midpoint 3.30 ± 0.15)

Bottom-up at $3,970m:
```
Revenue                                                                  3,970
Adjusted gross margin @ 72.7%                                            2,886
Adjusted opex (~23.2% of revenue; Q2 was $871.5m, +Empower opex)          (921)
Adjusted operating income → 49.5% adj OM (guide 49.0% ±100bps)            1,965
Adjusted non-operating expense (Q2 $57m; higher after $1.5bn cash out)      (60)
Adjusted pre-tax                                                          1,905
Tax @ 13.2% (guide 12–14%; Q2 actual was 11.8% — a real headwind)          (251)
Adjusted net income / ~488m diluted shares                                $3.39
```
Cross-checks: mean EPS beat of +$0.137 over six quarters implies $3.44; Zacks' "Most Accurate Estimate"
(most recently revised subset) is $3.41; my build gives $3.38–3.42 depending on opex and tax. **Central
$3.40.**

**Why $3.40 rather than the $3.44 the pure beat-history implies.** Three deliberate haircuts:
(a) the **Empower Semiconductor** acquisition closed 7 July 2026 for $1.5bn cash — ~26 days inside the
quarter, revenue immaterial, but its opex runs through *adjusted* results and the cash outflow raises
net non-operating expense: a $0.02–0.04 drag that was not in the 20 May guide and that a straight
historical extrapolation double-counts; (b) the tax rate steps up from Q2's flattering 11.8% to a guided
12–14%; (c) adjusted opex is the least-visible line — variable comp ratchets with y/y growth and
operating margin, both running far above plan, and $30m of extra opex is $0.05 of EPS.

**Scoring note.** The EPS floor here is tiny (0.5% of result ≈ $0.017), so the punishing scenario is
*ADI beating by only $0.03–0.05* — which would put the actual essentially on consensus and make any
deviation expensive. I ran the expected score across a plausible outcome distribution: forecasting
$3.42–3.45 is optimal only if the recent beat cadence persists, while $3.38–3.40 is robust across both
"beats continue" and "beats compress" regimes. $3.40 is the risk-adjusted choice, and it stays
internally consistent with the $3,970m revenue line.

### 4.3 Adjusted gross margin — **72.7 percentage points** (derived consensus ~72.5)

ADI does not guide GM in the release. The usable anchor is Puccio's Q&A answer:

> "For Q3, we are assuming **about a 50 basis points decline** in gross margin, largely driven by the
> absence of that one-time benefit we got from repricing the channel during the prior quarter …
> From a mix perspective, we do expect it's likely to be a **slight tailwind** … **utilization is
> expected to be fairly neutral** … we don't see a ton of future upside on gross margin from
> utilization given where we're running the factories today."

73.0% − 50bp = **72.5% company-implied**, corroborated at the 2 June conference ("held on to the 72.5%",
undisputed). Independent bottom-up off the 49.0% adjusted-OM guide with $900–940m of opex gives
72.1–73.1%, midpoint 72.6%.

**Bridge to 72.7%:** −50bp for the non-repeating channel-repricing benefit (explicit); +20–30bp mix
(communications/data centre guided fastest and is above corporate average; consumer, below average,
guided down); +10bp volume leverage on fixed manufacturing cost from the assumed revenue beat; −10bp
external-foundry dilution required to service that beat; ~0 utilisation.

**Only +0.2pp of deviation, deliberately.** Puccio explicitly endorsed the framing that ~72.5% is the
near-term *ceiling* while utilisation is maxed, and the two forecasts are negatively correlated —
incremental revenue above ~$3.9bn increasingly routes to external foundry/OSAT, which is dilutive. A
single fab utilisation event is the classic killer: exactly that cost ADI ~80bp in FY2025 Q3, and Q3
contains ADI's summer shutdowns. The 0.5pp floor makes +0.2pp near-free insurance; more would be
unjustified.

**BASIS TRAP.** The GAAP-to-adjusted gap is ~570bp (Q2 FY26: GAAP GM 67.3% vs adjusted 73.0%) because
Linear/Maxim/Empower purchase-accounting amortisation is excluded. Report **72.7**, in points, not 0.727,
and not the ~67–68% GAAP line. GAAP diluted EPS would be ~$2.70–2.75 versus adjusted ~$3.40.

---

## 5. HAYS PLC — FY2026 (year ended 30 June 2026)

**The fiscal year is complete and the Q4 trading update of 10 July 2026 already discloses all four
quarters of net-fee growth and pre-guides the profit outcome.** Two of the three metrics are close to
arithmetic. Note carefully: the 10 July document is a **trading update, not results** — it contains no
FY26 net fee, operating profit or EPS figure. No FY26 actual exists.

### 5.1 Net fees — **£903.5m** (company-compiled consensus £902.4m, range £894.0–914.0m, 9 analysts, 11 Aug 2026)

Reported FY26 quarterly net-fee growth on an **actual** basis (the basis that builds to a reported
figure): Q1 (8)%, Q2 (9)%, Q3 (7)%, Q4 (4)%.
Source: `hays/filings/{2025-10-10 Q1, 2026-01-14 Q2, 2026-04-16 Q3, 2026-07-10 Q4}`.

```
H1 FY2026 net fees (REPORTED, 27 Feb 2026)                              453.3
H2 FY2025 base = FY25 972.4 − H1 25 496.0 (both REPORTED)               476.4
H2 FY2026 = 476.4 × blended Q3/Q4 actual growth of ~(5.5)%              450.2
------------------------------------------------------------------------------
FY2026 net fees                                                        ~903.5   (−7.1% actual YoY)
```
**Method validation:** applying the same method to H1 (Q1 −8%, Q2 −9% ⇒ −8.5%) predicts £453.9m against
the reported £453.3m — accurate to 0.1pp. A divisional build (Germany ~£142.7m, UK&I ~£86.7m, ANZ
~£57.7m, RoW ~£164.4m for H2) gives £904.6m. CFO Hilton on the 10 July call: *"they only do GBP 15
million of fees versus a business that does close to GBP 900 million."* Because the disclosed quarterly
rates are integers, the irreducible rounding band is roughly **£901.5–907.2m**.

**Sit at consensus.** £903.5m is +£1.1m (+0.1%) versus the compiled mean — well inside the 0.5% floor
(£4.5m). There is no edge to be had on a number the street computes the same way we do.

**The one 5.0-scoring tail risk: IFRS 5.** Hays sold six European countries (Czech Republic, Denmark,
Hungary, Luxembourg, Romania, Sweden) to Meraki Capital on 16 June 2026, and footnote (1) of the Q4
statement says they "are no longer considered continuing operations following their disposal". If they
are presented as **discontinued operations** in the FY26 P&L, reported net fees fall to ~£888m (and
~£818m if the seven countries under options review followed). I judge this unlikely and have not adopted
it, for four reasons: (i) the same statement says they "contributed **c.£15m to reported group net fees
in FY26**" — the company's own phrasing puts them inside the reported figure; (ii) the actual-basis
growth narrative explicitly describes the divestments as a *drag on the actual rate*, i.e. included;
(iii) six small country subsidiaries are not "a separate major line of business or geographical area of
operations" under IFRS 5; (iv) the tight £894–914m consensus range proves the sell-side is uniformly on
the inclusive basis, so if we are wrong the street is wrong with us and the ratio stays near 1.0.

### 5.2 Pre-exceptional operating profit — **£46.2m** (consensus £45.3m, range £40.0–46.1m)

Guidance, verbatim, 10 July 2026: *"we currently expect FY26 pre-exceptional operating profit will be at
the top of the £37.0-46.0m consensus range."*

Two independent routes converge:
1. **"Top of the range"** ⇒ ~£46.0m.
2. **The CFO's own on-call arithmetic:** *"this second half profit performance is up about 30% versus H2
   last year."* H2 FY25 pre-exceptional operating profit = 45.6 − 25.5 = **£20.1m** ⇒ H2 FY26 ≈ £26.1m
   ⇒ FY26 = 20.1 + 26.1 = **£46.2m**. He was doing that sum from near-final numbers ten days after the
   year end.
3. **Hays habitually beats its own point guidance by 0.5–1.5%:** FY25 pre-close "c.£45m" → £45.6m;
   H1 26 "c.£20m" → £20.1m.

Implied conversion rate 46.2/903.5 = **5.1%** (FY25 4.7%, H1 26 4.4%), consistent with c.£35m of H2
structural cost savings landing against a −5.3% H2 fee decline. c.£50m of annualised savings were
secured in FY26 against a c.£45m-by-FY29 target — three years early.

**Why this deviation is justified, not clever.** The £45.3m compiled mean is depressed by an unrevised
£40.0m low estimate while the compiled *top* sits at £46.1m — exactly where the company steered
everyone. Consensus history shows the drift: £45.2m (15 Apr, 11 analysts) → £43.5m (9 Jul, 10 analysts)
→ £45.3m (11 Aug, 9 analysts). The mean still sits ~£0.8m below the company's own steer. Asymmetry:
if the print is £46.0m our miss is 0.2 against a street miss of 0.7 (score ~0.3); if £46.5m we win
outright; the deviation only hurts if it lands at or below ~£45.5m, which would contradict the explicit
guidance.

### 5.3 Pre-exceptional basic EPS — **1.14 pence** (consensus 1.13p, range 0.93–1.40p)

```
Pre-exceptional operating profit                                46.2
less net finance charge                                        (13.2)   [guided "c.£13 million" at H1; FY25 was 13.4; H1 26 run-rate 6.7]
= Pre-exceptional PBT                                           33.0
less tax @ 45.0%                                               (14.9)   [guided "ETR in FY26 to be c.45%"; H1 26 actual 44.8%]
= Pre-exceptional earnings                                      18.1
÷ weighted average basic shares                              1,592m     [H1 26: 1,595.7m; FY25: 1,590.2m; ~£12m of treasury buybacks, mostly June 2026]
= Pre-exceptional basic EPS                                    1.14p
```

**On the tax rate — I explicitly reject the "ETR falls to ~43.5%" argument** made in one of the source
dossiers. Under IAS 34 the H1 charge is struck at management's forecast *full-year* rate, so H1 26's
44.8% **is** the company's FY26 forecast, and the H1 report restated it as guidance ("c.45%, consistent
with the first half"). The mechanical argument that a fixed unrecognised-loss block spread over higher
H2 profit lowers the rate requires H2 profit to have surprised materially versus the February plan — it
did not (the Q3 update on 16 Apr said "in line with consensus" of £45.2m; the outturn is ~£46.2m).
The FY25 precedent runs the *other* way: the full-year pre-exceptional ETR (35.1%) landed 3.0pts **above**
its H1 rate (32.1%). Directional risk on this metric is therefore to the downside.

Sensitivity: each 1pt of ETR ≈ ∓0.021p; each £0.5m of finance charge ≈ ∓0.017p; each £1.0m of operating
profit ≈ ±0.035p. At 43% ETR EPS is 1.19p; at 47%, 1.10p; at 49%, 1.06p. The consensus range of
0.93–1.40p shows the sell-side itself is widely dispersed on exactly this line.

**Positioning:** 1.14p is +0.01p above consensus — directionally consistent with my above-consensus
operating profit (£46.2m vs £45.3m, worth ~+0.02p mechanically) but haircut for the downside ETR skew.
Consensus scaled for my operating profit (1.13 × 46.2/45.3) gives 1.15p; my own build at guided tax
gives 1.13–1.15p. 1.14p is the honest centre. **This is PENCE: 1.14, not £0.0114 and not 114.**

**Do not confuse the statutory result with a miss.** FY26 exceptionals are flagged at c.£40m
restructuring + c.£30m right-of-use impairment + a modest disposal loss (H1 already booked £8.8m),
so total FY26 exceptionals of c.£70–80m imply a **statutory operating loss of roughly £(25)–(29)m and a
sharply negative statutory EPS**. All three target metrics are pre-exceptional.

---

## 6. WHERE WE SIT VERSUS CONSENSUS, IN ONE VIEW

| Metric | Posture | Reason for the deviation (or for not deviating) |
|---|---|---|
| HD net sales | +0.4% above benchmark, at the top of the published range | Mingledorff's (~$200m, undisclosed, closed after the guide, under-modelled) + GMS at seasonal peak; independently corroborated by the 1.14x Q2/Q1 seasonality ratio |
| HD adjusted EPS | **At consensus** | No edge; floor is only ~$0.024; HD has recently posted small misses, not beats; gross margin alone spans $0.14 of outcomes |
| HD comparable sales | −0.3pp below the derived consensus | Hardest compare of FY2026 (+1.0% lap, July 2025 +3.1%); management explicitly disclaimed a Q2 demand inflection; FX tailwind halves; three of five methods point to 0.0% or below |
| ADI revenue | +1.1% above consensus | 17/18 midpoint beats, mean beat = full band width; record bookings, lean and declining channel inventory, flat-weeks assumption. Capped below the pure extrapolation for the auto pull-forward into Q2 |
| ADI adjusted EPS | +$0.07 above consensus | Same beat record, minus the Empower opex/interest drag, minus the 11.8%→12–14% tax step-up. Deliberately short of the $3.44 that history alone implies because the tiny floor punishes a small-beat outcome severely |
| ADI adjusted gross margin | +0.2pp above the derived consensus | Management's own 73.0% − 50bp bridge plus the mix tailwind they named; capped tight because they called it a ceiling and because revenue upside routes to dilutive external foundry |
| HAS net fees | **At consensus** | Arithmetic from reported quarterly growth rates; consensus computes it the same way |
| HAS pre-exceptional operating profit | +£0.9m above consensus | "Top of the £37.0–46.0m range" plus the CFO's own "H2 up ~30%" sum; the compiled mean is dragged by a stale £40.0m low while the compiled top is £46.1m |
| HAS pre-exceptional EPS | +0.01p above consensus | Follows the operating-profit deviation, haircut for the downside ETR skew (FY25 precedent: FY rate 3pts above H1 rate) |

**Net stance:** three metrics essentially at consensus (HD EPS, HAS net fees, and near-enough HAS EPS),
five modest reasoned deviations, one meaningful contrarian call (HD comparable sales). No metric is more
than ~1.1% (money) or ~0.3pp (percentage) from its consensus benchmark except ADI revenue and EPS, where
an 18-quarter guidance-beat record is the specific, articulable reason.

---

## 7. THE FIVE THINGS MOST LIKELY TO MAKE THIS WRONG

1. **HD comparable sales, sign risk.** The two-year-stack family says 0.0% to −0.7%; the
   consensus-implied read says +0.7% to +0.9%. My +0.5% could be a full point high if July 2026 lapped
   July 2025's +3.1% badly. The 0.5pp floor bounds the damage.
2. **ADI landing on the guide.** If ADI beats its EPS midpoint by only $0.03–0.05 (it did exactly that in
   Q4 FY2025), the actual lands on consensus, the street miss collapses to the floor, and our +$0.07
   deviation scores badly. This is the single largest downside in the set.
3. **Hays ETR.** Guided c.45%, struck at 44.8% in H1, but the FY25 full-year rate came in 3pts above its
   H1 rate. At 48% EPS is ~1.08p against my 1.14p. The consensus range of 0.93–1.40p is the market's own
   admission that this is unforecastable.
4. **Hays IFRS 5 restatement of net fees** — the only true 5.0-scoring tail. Judged unlikely (see §5.1),
   and the street would be wrong with us if it happened.
5. **Mingledorff's and GMS are both estimates, not disclosures.** Together they are ~$1.65bn of my HD
   sales line, and the error band on the pair is comfortably ±$250m — more than one scoring floor.

---

## 8. SOURCE INDEX (load-bearing documents only; all paths absolute)

**Corpus**
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/home-depot/filings/2025-08-19__hd-us-20250819-q2-8k__143666.md` — HD prior-year actuals
- `.../home-depot/filings/2026-05-19__hd-us-20260519-q1-8k__1038584.md` — Q1 FY2026 results, non-GAAP definition, FY2026 guidance reaffirmed
- `.../home-depot/filings/2026-05-19__hd-us-20260519-q1-10q__1053121.md` — GMS $1.3bn Q1 contribution; SRS segment detail
- `.../home-depot/call-transcripts/2026-05-19__hd-us-20260519-call-qna__1039119.md` — H2-weighted comp, Q2 gross-margin steer, May trading
- `.../analog-devices/filings/2026-05-20__adi-us-20260520-q2-8k__1040581.md` — Q2 FY2026 results and Q3 FY2026 guidance (line 71)
- `.../analog-devices/call-transcripts/2026-05-20__adi-us-20260520-call-qna__1041159.md` — the "50 basis points decline" gross-margin bridge (line 61), segment guide (lines 71–73), ceiling (line 83)
- `.../analog-devices/filings/2025-08-20__adi-us-20250820-q3-8k__155976.md` — ADI prior-year actuals
- `.../hays/filings/2026-07-10__has-ln-20260710-q4-8k__1572805.md` — Q4 FY26 trading update: quarterly growth, "top of the £37.0-46.0m range", c.£15m disposed-country fees (line 132)
- `.../hays/call-transcripts/2026-07-10__has-ln-20260710-call-qna__1573114.md` — CFO "H2 up about 30%", "close to GBP 900 million"
- `.../hays/filings/2026-02-27__has-ln-20260227-h1-8k__642921.md` — H1 FY26 actuals; "c.£13 million" finance charge and "c.45%" ETR guidance
- `.../hays/filings/2025-08-21__has-ln-20250821-filing__143845.md` — Hays FY25 prior-year actuals
- `.../hays/filings/2026-08-03__has-ln-20260803-filing__1600192.md` — share count at 31 Jul 2026

**External (dates as fetched by the research agents, 16 Aug 2026)**
- SEC XBRL `https://data.sec.gov/api/xbrl/companyconcept/CIK0000354950/us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax.json` — confirms HD Q2 FY2025 $45,277m
- SEC XBRL `https://data.sec.gov/api/xbrl/companyconcept/CIK0000006281/us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax.json` — confirms ADI Q3 FY2025 $2,880,348,000; no fact ending after 2026-05-02
- `https://ir.homedepot.com/news-releases/2026/08-04-2026-130209919` (4 Aug 2026) — HD reports 18 Aug 2026
- `https://finance.yahoo.com/markets/stocks/articles/ahead-home-depot-hd-q2-131502062.html` (13 Aug 2026, Zacks) — HD consensus $47.5bn / $4.71
- `https://www.ad-hoc-news.de/boerse/news/corporate-news/home-depot-stock-softens-ahead-of-august-earnings-consensus-push/69950012` (14 Aug 2026, S&P Global) — HD consensus $47.24bn / $4.73
- `https://investor.analog.com/news-releases/news-release-details/analog-devices-report-third-quarter-fiscal-year-2026-financial` (23 Jul 2026) — ADI reports 19 Aug 2026
- Zacks via Globe & Mail / TradingView (14 Aug 2026) — ADI consensus $3.92bn / $3.33; Most Accurate $3.41
- `https://www.barchart.com/story/news/3446493/here-s-what-to-expect-from-analog-devices-next-earnings-report` (24 Jul 2026) — ADI consensus $3.33 across 31 analysts
- `https://investor.analog.com/news-releases/news-release-details/analog-devices-completes-acquisition-empower-semiconductor` (7 Jul 2026)
- `https://www.haysplc.com/investors/analysts-consensus` (last updated 11 Aug 2026, 9 analysts) — **primary Hays consensus**: net fees £902.4m, operating profit £45.3m, EPS 1.13p
- `https://www.haysplc.com/investors/events-calendar` — Hays FY26 results 20 Aug 2026
- FRED keyless CSV: `RSBMGESD`, `MORTGAGE30US`, `EXHOSLUSM495S`, `HOUST`, `RSXFS`, `DEXCAUS`, `DEXMXUS`
