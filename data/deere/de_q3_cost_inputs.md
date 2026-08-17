# Deere Q3 FY2026 cost inputs — supply, tariffs, warranty and the lag structure

Companion to `de_q3_cost_inputs.csv` (1,942 rows).
Assembled 16 August 2026. **Deere has not reported FY2026 Q3.** The quarter ends
2026-08-02 and the call is 09:00 US Central, Thursday 20 August 2026. No Q3 FY2026
actuals appear in this file, and the validation script asserts their absence.

The offline corpus is frozen at 2026-05-28. FRED and news sources are live and were
queried on 2026-08-16, which is how the May–July 2026 input-cost window is covered at all.

> **Corpus mislabel.** `INDEX.md` lists `2026-05-21 | Call Transcript | Q3 2026 | Q3 2026
> Earnings Call Transcript` → `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`.
> It is dated the same day as the Q2 earnings release and its contents are the **Q2 FY2026
> Q&A** (it discusses the Q2 $272m refund, Q2 margins, and forward guidance for the back
> half). It is cited throughout this document as Q2 material and contains no Q3 results.

---

## 1. Headline findings

1. **The lag exists, but the sample cannot prove it is a *steel* lag.** Hot-rolled coil
   steel PPI peaks against Deere's PPA production-cost bridge component at **lag 3
   quarters, r = −0.75, n = 18** (AR(1)-adjusted effective n = 11.5). Broader steel mill
   products and scrap peak at lag 4 (r = −0.76 / −0.75); aluminium at lag 2 (r = −0.76);
   diesel and freight at lags 1–2. The pattern is coherent with a 2–4 quarter
   procure-to-COGS lag. **But a deliberately unrelated placebo — CPI used cars and
   trucks — scores r = −0.92 at lag 3, beating every genuine input.** The whole
   FY2021–FY2026 window is a single inflation up-and-down cycle, so anything
   inflation-correlated fits. Treat the lag as a *prior about physical timing*, not as
   an identified statistical relationship.
2. **The cost impulse hitting Q3 is materially worse than the one that hit Q2.** At each
   series' best-fit lag: HRC steel **+10.0% YoY** feeding Q3 versus **+2.5%** feeding Q2;
   diesel PPI **+70.1%** versus **−6.2%**; aluminium **+17.9%** versus **+10.0%**. Freight,
   scrap and copper move the other way but by far smaller amounts.
3. **Deere's own output prices are not moving.** PPI farm machinery is **+2.2% YoY** in the
   Q3 window and has been flat near +2% all year, matching management's 1.5–2.0% price
   guide. With inputs at +10% to +70%, the Q3 price/cost scissor opens further.
4. **Q2's margin beat was a one-off cost item, not a revenue event.** A $272m IEEPA tariff
   refund was booked *into production cost* and lifted equipment-operations margin by
   ~2.5 points, while revenue "came in largely in line with expectations." That single
   line item is worth more than the entire plausible range of Q3 revenue surprise.
5. **No extended summer shutdown found.** Searched specifically. The only PPA production
   news inside or adjacent to the window is *expansionary* (146 Waterloo callbacks for
   8R tractors from early March 2026) plus ~120 Ankeny layoffs completed 28 April, i.e.
   inside Q2. This is evidence **against** a shipment-side shock to Q3 revenue.
6. **Warranty is loading up.** Consolidated new product warranty accruals: 342 in Q1 FY2026
   (+34% YoY) and 318 in Q2 (+40% YoY), while claims paid fell (−299, −294 versus −310,
   −308). Deere is provisioning ahead of payout. PPA's warranty bridge line has been
   negative for two straight quarters (−48, −51).

---

## 2. The operating-profit bridge: what reconciled, what was rejected

The slide decks are OCR'd and the waterfall labels and values do **not** reliably align.
Every bridge was therefore reconstructed and then arithmetically reconciled, with both
endpoints independently verified against the 8-K segment tables (`de_segment_panel.py`,
which double-sources 299 segment values from current-year and prior-year 8-K columns and
reports 4 conflicts, all pre-2018 Financial Services rows).

| | count |
|---|---|
| Segment-quarters reconciled (FY2021 Q1 – FY2026 Q2, 3 segments = 66 slots) | **55** |
| Rejected: bridge would not reconcile, or endpoints disagreed with the 8-K | **11** |
| Rejected: OCR emitted the label row out of Deere's fixed waterfall order | **2** |
| Chunks parsed but discarded as duplicates/unusable | 22 |

PPA specifically: **18 of 22 quarters**. Missing PPA quarters: 2Q2022, 3Q2022, 1Q2023,
2Q2023. Missing CF: 3Q2021, 2Q2022, 3Q2022, 2Q2023, 4Q2023, 2Q2024, 2Q2026. Missing SAT:
1Q2025. All rejected slots are written to the CSV as `de_op_bridge_rejected` rows with
blank values and the rejection reason, so the gaps are visible rather than silent.

### The trap that arithmetic alone does not catch

Reconciliation is necessary but **not sufficient**: every permutation of the components
sums to the same total, so a bridge can reconcile perfectly while every label is wrong.
Two real examples from this corpus:

- **2Q FY2024 PPA.** The narrative reads `"Volume/Mix" ($137) ... A gray bar with a value
  of "($627)" is positioned between the "2Q 2023" bar and the "Volume/Mix" bar.` A naive
  parse reconciles at 2,170 → 1,650 with Volume/Mix = +137 and Other = −627. That is
  wrong on its face — PPA sales fell 16% that quarter, and the 8-K says operating profit
  fell "due to lower shipment volumes." The correct reading puts the orphan −627 in the
  first (Volume/Mix) slot and shifts every label back one.
- **2Q FY2022 PPA/CF.** The OCR label array is `["2Q 2021", "Price", "Volume/Mix",
  "Currency", ...]` — Price and Volume/Mix transposed. Nothing in the arithmetic
  distinguishes Price = +502 / Volume-Mix = +212 from the reverse. **These two quarters
  are rejected, not guessed.**

The parser therefore binds labels to values using the *connector text* between them
("($61)" **for** "Volume/Mix" binds backwards; "Price**:** $2" binds forwards), falls back
to Deere's fixed waterfall order when the full set of 8 bars is present, and refuses the
quarter when the label sequence itself is scrambled. Twelve PPA quarters were then
hand-checked against the raw narrative; all twelve match.

### PPA production-cost bridge component (USDm, YoY delta)

| | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| FY2021 | −38 | −139 | −248 | −391 |
| FY2022 | −407 | *rejected* | *rejected* | −586 |
| FY2023 | *rejected* | *rejected* | −77 | +40 |
| FY2024 | +15 | −41 | −5 | +105 |
| FY2025 | +62 | +73 | +69 | −147 |
| FY2026 | −74 | −77 | **forecast target** | |

### PPA warranty bridge component (USDm, YoY delta)

| | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| FY2024 | −20 | +27 | +48 | −70 |
| FY2025 | −32 | +32 | −45 | +23 |
| FY2026 | −48 | −51 | **forecast target** | |

Warranty flips sign quarter to quarter with a range of roughly ±50 on PPA alone. This is
why it belongs in the width of the band, not in the point estimate.

---

## 3. Lag structure: method and result

Deere's real 52/53-week fiscal calendar was reconstructed from the 8-K period headers
(44 quarter-end dates, `de_fiscal_calendar.py`), because a calendar-quarter approximation
would smear precisely the lag being measured. Q3 FY2026 is therefore **2026-05-04 to
2026-08-02** — the end date derived as 13 weeks after the reported Q2 end, flagged as
derived in the CSV.

Each macro series is averaged over the real fiscal quarter, converted to YoY %, and
cross-correlated against the PPA production-cost bridge component at lags 0–6.

| Series | best lag | r | n | n_eff | partial r vs PPI-all-commodities | first-differenced r |
|---|---|---|---|---|---|---|
| PPI hot-rolled steel sheet & strip (WPU101707) | **3** | −0.75 | 18 | 11.5 | −0.56 | −0.78 |
| PPI steel mill products (WPU1012) | 4 | −0.76 | 18 | 8.8 | −0.73 | −0.79 |
| PPI iron & steel scrap (WPU101211) | 4 | −0.75 | 18 | 8.9 | −0.72 | −0.78 |
| Aluminium (PALUMUSDM) | 2 | −0.76 | 18 | 7.4 | −0.16 | −0.74 |
| Copper (PCOPPUSDM) | 4 | −0.69 | 18 | 9.4 | −0.69 | −0.70 |
| Iron ore (PIORECRUSDM) | 5 | −0.65 | 17 | 12.4 | −0.66 | −0.75 |
| Rubber (PRUBBUSDM) | 0 | **+0.46** | 18 | 7.1 | +0.56 | +0.23 |
| PPI no. 2 diesel (WPU057303) | 1 | −0.86 | 18 | 7.2 | −0.14 | −0.66 |
| Retail diesel (GASDESW) | 1 | −0.90 | 18 | 8.7 | −0.47 | −0.83 |
| PPI TL freight (PCU484121484121) | 2 | −0.94 | 18 | 7.5 | −0.74 | −0.89 |
| PPI farm machinery (WPU111) | 0 | −0.94 | 18 | 6.4 | −0.89 | −0.87 |
| **PLACEBO: CPI used cars (CUSR0000SETA02)** | 3 | **−0.92** | 18 | 8.0 | −0.86 | −0.81 |
| Control: PPI all commodities (PPIACO) | 1 | −0.89 | 18 | 6.6 | — | −0.77 |
| Control: CPI all items (CPIAUCSL) | 0 | −0.91 | 18 | 8.2 | −0.79 | −0.83 |

Full lag-by-lag correlograms for PPA, SAT and CF are in the CSV as `lag_correlation` rows
(315 of them).

**How to read this honestly.** The signs are right — rising input prices, more negative
production-cost contribution — and the peak lags cluster at 1–4 quarters in a sensible
order (energy and freight fast, steel slower, iron ore slowest). But:

- n is 18 nominal and 6–12 effective once AR(1) persistence in both series is removed.
- 7 lags × 15 series × 3 segments = 315 tests. At that count, |r| ≈ 0.5 at n_eff ≈ 8 is
  not evidence of anything on its own.
- The placebo out-scores hot-rolled coil at the *same* lag. The rubber result is
  positively signed, which is economically backwards and is the honest signature of noise.
- The farm-machinery PPI result at lag 0 (r = −0.94) is close to mechanical — it is the
  industry's own output price index moving with the same cycle.

So: **use lag 2–3 for steel as a planning convention with the physical rationale behind
it, and do not present the correlation as the reason.** The statistically strongest thing
in this whole exercise is not a correlation at all — it is Deere's own MD&A, which
attributes the Q2 production-cost move to "higher material costs" and quantifies it at
$157m pretax, and management's "$200 million of the headwind" from direct tariffs.

---

## 4. The actual input data for the Q3 FY2026 window

Fiscal-quarter averages on Deere's calendar. Q3 FY2026 = 2026-05-04 to 2026-08-02.

| Series | 2025Q3 | 2025Q4 | 2026Q1 | 2026Q2 | **2026Q3** | Q3 YoY |
|---|---|---|---|---|---|---|
| PPI HRC steel sheet/strip | 382.8 | 364.4 | 393.9 | 416.6 | **439.8** | **+14.9%** |
| PPI steel mill products | 532.9 | 523.7 | 565.2 | 603.8 | **593.5** | **+11.4%** |
| PPI iron & steel scrap | 493.7 | 485.6 | 528.7 | 560.9 | **546.6** | **+10.7%** |
| Aluminium, $/t | 2,526.6 | 2,716.3 | 3,025.0 | 3,541.9 | *(Jun only)* | +38.4% at Q2 |
| Copper, $/t | 9,712.3 | 10,304.6 | 12,576.3 | 12,977.2 | *(Jun only)* | +37.9% at Q2 |
| Rubber, ¢/lb | 101.1 | 95.0 | 98.4 | 118.1 | *(Jun only)* | +11.5% at Q2 |
| PPI no. 2 diesel | 297.4 | 312.9 | 285.2 | 505.1 | **467.1** | **+57.1%** |
| Retail diesel, $/gal | 3.6 | 3.7 | 3.7 | 4.7 | **5.2** | **+43.8%** |
| PPI TL freight | 175.9 | 185.6 | 181.9 | 198.7 | **196.8** | **+11.9%** |
| **PPI farm machinery** | 323.9 | 325.4 | 328.5 | 330.2 | **330.9** | **+2.2%** |

Monthly detail (all in the CSV as `macro_*_monthly`):

- **HRC steel rises monotonically and is still rising at quarter end**: 358.1 (Oct-25) →
  407.0 (Mar-26) → 423.8 (May) → 433.1 (Jun) → **446.6 (Jul)**. Up 25% in nine months.
- **Steel mill products and scrap peaked in March 2026** (614.8 / 574.3) and are easing
  (588.9 / 542.3 in July). The narrow HRC index and the broad mill index have diverged;
  which one matters depends on Deere's contract mix, which is not disclosed.
- **Diesel is a genuine shock**: PPI 266.6 (Jan-26) → 437.3 (Mar) → 582.8 (May) → 457.1
  (Jul). Retail diesel peaked ~$5.60 in early May, troughed ~$4.60 mid-July, back to
  $5.30 by 10 August. Deere's Q2 10-Q flags "the availability and price of fertilizers as
  a result of the conflict in the Middle East" among its concerns.
- **Freight peaked in May 2026** (203.9) and eased to 195.6 by July.
- **Copper, aluminium and rubber only run to June 2026** on the IMF series — the July
  observation is genuinely absent, and is left absent rather than extrapolated.

---

## 5. Tariffs in force during the Q3 window

| Date | Event | Rate |
|---|---|---|
| 2026-02-20 | Supreme Court rules 6–3 that IEEPA does not authorise presidential tariffs | — |
| 2026-02-20 | Section 122 (Trade Act 1974) proclamation, flat surcharge on all imports | 10% |
| 2026-02-22 | Section 122 surcharge raised | 15% |
| 2026-04-06 | Section 232 proclamation: steel primary metals; tiered derivative structure (50% on certain primary metal products) | 25% |
| 2026-04-06 | Section 232 aluminium primary metals; tiered derivatives | 10% |
| 2026-04-06 | Copper and derivatives brought under Section 232 (~25% on certain articles); Section 232 goods are exempt from the Section 122 surcharge | — |
| **2026-05-07** | **Court of International Trade invalidates the global Section 122 tariffs — four days into Deere's Q3** | — |

### Deere's own quantifications (Q2 FY2026 call, 21 May 2026)

- **$272m** IEEPA refund recognised in Q2, "benefited our production cost this quarter and
  lifted margins by nearly 2.5 points." One-off.
- **~$200m** year-on-year direct tariff expense headwind in Q2 excluding the refund, "with
  the remainder largely driven by higher material and freight costs."
- **$1.2bn** full-year FY2026 direct tariff exposure, ~3 points of margin, described as
  "essentially unchanged" after the IEEPA invalidation, Section 122 introduction and
  Section 232 adjustments. **~$900m** net of the refund.
- Segment split of exposure: **~50% C&F, ~33% SAT, ~20% large ag (PPA)**; the refund split
  was "pretty close to the tariff exposure as well" → **PPA's share of the refund ≈ $54m**
  (derived, not disclosed). That implies **PPA's Q2 production-cost line was about −131
  excluding the refund, versus the −77 reported.**
- No surcharging: price guide 1.5–2.0% for the year, against general inflation ex-tariffs
  of "also about 1.5%–2%." Mitigation is resourcing, reshoring, exemptions, USMCA compliance.
- ~80% of US complete-good sales are US-built; ~75% of components at those plants are
  US-sourced. This caps direct tariff exposure but does not cap the *indirect* inflation
  that domestic steel prices carry.

**The Q3-specific tariff point:** the CIT struck down Section 122 on **7 May 2026**, inside
the quarter. The Q2 refund shows that a favourable ruling can produce a discrete,
unforecastable nine-figure credit *booked into production cost*. Another such credit in Q3
is possible and is the single largest identifiable upside risk to Q3 margin. Deere's
21 May guidance did not assume one.

**Comparison base matters.** Q3 FY2025 already carried roughly **$200m** of tariff cost
("Tariff costs in the quarter were approximately $200,000,000 which brings us to roughly
$300,000,000 in tariff [costs year to date]"). At a $1.2bn FY2026 run rate (~$300m/quarter)
the year-on-year tariff *step* in Q3 FY2026 is around +$100m enterprise, roughly half the
~$200m step Deere reported in Q2. Management's "back-half comps become more favorable" is
therefore right in direction — but for PPA it lands mostly in **Q4**, because PPA's
production-cost bridge was still **+69 (favourable) in Q3 FY2025** and only collapsed to
**−147 in Q4 FY2025**.

---

## 6. Production announcements, May–August 2026 — searched specifically

The hypothesis predicts revenue is locked; an extended summer shutdown would break that.
I looked for one and did not find one.

| Date | Event | Direction |
|---|---|---|
| 2026-02-06 | 146 workers recalled to four Waterloo facilities (Drivetrain, Tractor Operations, Engine Works, Foundry) from early March, "increased customer demand" for 8R tractors | **Expansionary, PPA large ag** |
| 2026-03-28 / 04-04 / 04-28 | ~120 layoffs at Des Moines Works, Ankeny IA in three tranches | Contractionary, but **all inside Q2 FY2026** |
| 2026-05-04 → 2026-08-02 | **Nothing found**: no extended shutdown, additional seasonal layoff, or production-rate cut announced in the Q3 window. The WARN aggregator shows no John Deere filings in calendar 2026 | **No shipment shock identified** |

This is absence of evidence in public reporting, not a company statement that nothing
happened. Deere takes routine summer shutdown weeks every year; the question is whether
FY2026's were *extended*, and nothing indicates they were. Deere's own framing points the
other way — Q3 is the *lighter* of the two back-half quarters by design, not by disruption:

> "a little bit better absorption in the fourth quarter as production rates are
> significantly higher … that's just the way the order book built this year for a much
> heavier fourth quarter with respect to our large tractors that are going to be settled
> here in the U.S."

That is a *scheduled* Q4 weighting, disclosed on 21 May, not a Q3 surprise.

---

## 7. Warranty

| Fiscal quarter | New product warranty accruals | Claims paid | YoY accruals |
|---|---|---|---|
| FY2024 Q1 | 281 | −309 | |
| FY2024 Q2 | 310 *(derived: 9M 871 − Q1 281 − Q3 280)* | | |
| FY2024 Q3 | 280 | −325 | |
| FY2024 Q4 | 286 *(derived: FY 1,157 − 9M 871)* | | |
| FY2025 Q1 | 256 | −310 | −9% |
| FY2025 Q2 | 227 | −308 | −27% |
| FY2025 Q3 | 303 | −336 | +8% |
| FY2025 Q4 | 362 *(derived: FY 1,148 − 9M 786)* | | +27% |
| FY2026 Q1 | **342** | −299 | **+34%** |
| FY2026 Q2 | **318** | −294 | **+40%** |

Accruals up 34–40% while claims paid fall. That gap is the P&L charge: Deere is booking
expected future claims, not paying more today. The Q2 10-Q MD&A puts consolidated warranty
at **$82m pretax** of headwind in the quarter. Liability balance $1,336m at 3 May 2026
versus $1,297m a year earlier.

For Q3: the FY2025 Q3 base is 303 — the *highest* of FY2025's first three quarters, so a
slightly easier comp than Q1/Q2 offered. A repeat of the +30–40% pace implies roughly
+$90m to +$120m of enterprise headwind.

---

## 8. Derived Q3 FY2026 scenario inputs (CSV series `q3_cost_build`)

These are **my scenario values, not Deere figures.**

| Component | Low | Central | High |
|---|---|---|---|
| PPA production costs (bridge, USDm YoY) | −180 | **−115** | −50 |
| PPA warranty (bridge, USDm YoY) | −70 | **−45** | −20 |

Construction of the central production-cost figure: start from the Q2 ex-refund run rate
of about −131; add roughly **+20** for the smaller year-on-year direct tariff step
(≈$100m enterprise in Q3 versus ≈$200m in Q2, at PPA's 20% share); subtract for the
worsening lagged material and energy impulse (HRC steel +10.0% vs +2.5%, diesel PPI +70%
vs −6%, aluminium +17.9% vs +10.0%) and for weaker Q3 overhead absorption given the
disclosed Q4-weighted build.

The **high** case is driven almost entirely by the possibility of a further tariff refund
following the 7 May CIT ruling — the same mechanism that delivered $272m unannounced in Q2.

---

## 9. Verdict on the hypothesis

**The evidence partially supports the hypothesis, and supports the modelling consequence
more strongly than it supports the stated reasoning.**

**Supported — revenue is largely pre-set.** As of the Q2 report on 21 May 2026, 18 days
into Q3:

- "Model year 2026 production of seasonal products is largely set by our early order
  programs, which have been closed for several months now."
- "Regarding Waterloo large tractors, order books are well into the fourth quarter."
- Europe and South America: "Order visibility in both regions now extends through the
  third quarter and into the fourth."
- MY2027 early order programmes were only just launching and "will begin production in the
  last few months of the fiscal year" — they do not touch Q3.
- No extended shutdown or production cut found in the window.

**Supported — profit is where the variance lives, and Q2 demonstrated it.** A single
$272m tariff-refund line moved equipment-operations margin ~2.5 points while revenue was
"largely in line with expectations." Nothing on the revenue side of Q3 has that
magnitude of dispersion.

**Qualified — the operator's stated *mechanism* is only half right.** The claim is that
"suppliers and input costs" are what move profit. In FY2026 the dominant swing factors in
Deere's production-cost line are **policy and accounting**, not procurement: a $1.2bn
tariff run rate, a $272m refund whose timing depended on a court ruling, and a warranty
provisioning step-up of 34–40%. Raw materials matter — steel at +10–15% and diesel at
+57% are real — but they are the *second* largest source of variance, behind tariff
adjudication. A forecaster who widened the margin band only for commodity risk would have
missed the Q2 surprise entirely.

**Qualified — "pre-determined" is not the same as "flat".** Q3 revenue is pre-set but
pre-set *low*: management disclosed that the order book is built for a "much heavier
fourth quarter." A tight range is justified; centring that tight range on naive
seasonality is not.

**Practical consequence:** forecast Q3 revenue tightly, anchored on the order book and on
the disclosed Q4-weighted large-ag build. Put the width on PPA operating profit and EPS,
and make the dominant term in that width **tariff adjudication**, with material/energy
inflation second and warranty third.

---

## 10. Caveats

1. The lag correlations are not identified. A placebo beats the real inputs at the same
   lag. n_eff is 6–12. Do not quote these r values as evidence of causation.
2. Eleven of 66 segment-quarter bridges could not be recovered, including four PPA
   quarters (2Q22, 3Q22, 1Q23, 2Q23), which removes most of the FY2022–23 inflation peak
   from the PPA series and biases the sample toward the disinflation phase.
3. The PPA share of the $272m refund ($54m) is derived from the stated exposure split, not
   disclosed. Management said the refund split was only "pretty close" to the exposure split.
4. Q3 FY2026's quarter-end date (2026-08-02) is derived as 13 weeks after the reported Q2
   end. Deere has not published it.
5. Copper, aluminium and rubber have no July 2026 observation; their Q3 fiscal-quarter
   averages cover May–June only, and the corresponding "Q3 YoY" cells are left blank.
6. The absence of an extended summer shutdown is based on public news and a WARN
   aggregator that may lag. It is not a company statement.
7. FY2025 PPA net sales sum to 17,310 from the quarterly 8-K columns versus the 17,311
   stated full-year figure — a 1m rounding difference, not resolved.
8. Bridge components are year-on-year deltas, not levels. Deere does not disclose absolute
   segment cost of sales, so the elasticity of the bridge line to a given steel move
   cannot be computed from disclosure alone.

---

## Reproduction

```
scripts/data/de_segment_panel.py        # 8-K segment panel, 299 values, double-sourced
scripts/data/de_fiscal_calendar.py      # 44 real fiscal quarter-end dates
scripts/data/de_extract_bridges.py      # OCR bridge recovery + reconciliation + rejection
scripts/data/de_warranty.py             # warranty liability rollforward
scripts/data/de_fetch_inputs.py         # FRED keyless CSV, 15 series
scripts/data/de_lag_analysis.py         # cross-correlograms, partial r, n_eff, placebos
scripts/data/de_build_q3_cost_csv.py    # assembles de_q3_cost_inputs.csv
scripts/data/de_validate_q3_cost_csv.py # ground-truth assertions (all pass)
```

Validation output: 14/14 checks pass, including all six verified Q2 FY2026 segment
figures, the three FY2025 full-year segment sales totals, the three H1 FY2026 totals,
"every bridge row reconciles against its 8-K endpoints", and "no reported Q3 FY2026 Deere
financials in file".
