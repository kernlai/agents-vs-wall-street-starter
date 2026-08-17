# Deere dealer credit quality — wholesale (dealer) vs retail (customer) receivables

**Companion to** `dealer_credit_quality.csv` (1,384 rows, 51 series, 51 period-ends, FY2014 Q1 → FY2026 Q2).
**Built:** 16 August 2026. **Latest reported period:** Q2 FY2026, ended 3 May 2026.
**Deere has NOT reported FY2026 Q3.** The Q3 call is 20 August 2026. Nothing below is a Q3 FY2026 actual.

---

## 1. Why this is the best dealer-health measure available

There is no listed pure-play North American Deere dealer. Cervus was acquired by Brandt in 2021; RDO,
Ag-Pro, Van Wall, Sydenstricker Nobbe, Hutson and Ziegler are private. Titan Machinery (TITN) is a
**CNH / Case IH–New Holland dealer**, a channel proxy only, not a Deere signal.

Deere's own filings therefore carry the quantitative load, and they are unusually good for this purpose
because John Deere Financial splits its financing-receivable credit-quality footnote by **portfolio
segment**:

| Portfolio segment | Who owes the money | CSV `entity` |
|---|---|---|
| **Wholesale receivables** | independent **dealers** (floor-plan / new & used inventory finance) | `dealer` |
| Retail customer receivables (retail notes, financing leases, revolving charge) | **end customers** — farmers, contractors | `customer` |

Separately, **trade accounts and notes receivable** is direct trade credit Deere's equipment operations
extend to those same dealers — the 10-Q states plainly that these "arise from sales of goods to
independent dealers" (`filings/2015-02-20__de-us-20150220-q1-10q__469211.md`, and the same language
persists to Q2 FY2026).

### Structural break you must respect
The wholesale-vs-retail split **only exists from CECL adoption in FY2021** (first disclosed in the
Q1 **FY2021** 10-Q, with restated FY2020 comparatives back to 2 February 2020). Before that
Deere disclosed **"Retail Notes"** vs **"Other"**, where "Other" bundles dealer wholesale notes with
revolving charge accounts, operating loans and financing leases. Those pre-CECL series are in the CSV as
`de_prececl_*` and carry `entity = mixed`. **Do not read `de_prececl_other_*` as a clean dealer series.**

A second break: pre-CECL, "non-performing" generally meant **120 days** delinquent; post-CECL it generally
means **90 days**. Post-2021 non-performing balances are therefore structurally higher than pre-2021 ones.
Levels across the 2021 boundary are not directly comparable; **directions within each regime are**.

---

## 2. The headline answer

**Deere's dealer channel is in good financial shape and improving. The stress in this cycle sits with the
end farmer, not with the dealer.** Three independent measures say the same thing.

### 2.1 Dealer (wholesale) credit quality — pristine, and it never cracked

`de_wholesale_stress_pct` = (30+ days past due + non-performing) ÷ total wholesale receivables.

| Period end | FY/Q | Wholesale receivables $m | Non-performing $m | 30+ past due $m | Stress % |
|---|---|---|---|---|---|
| 2020-02-02 | FY20 Q1 | 4,499 | 78 | 1 | **1.76** ← COVID-era high |
| 2020-11-01 | FY20 Q4 | 3,529 | 47 | 0 | 1.33 |
| 2021-10-31 | FY21 Q4 | 2,566 | 12 | 2 | 0.55 |
| 2022-10-30 | FY22 Q4 | 3,273 | 1 | 0 | 0.03 |
| 2023-10-29 | FY23 Q4 | 6,922 | 1 | 0 | 0.01 |
| 2024-07-28 | FY24 Q3 | 9,473 | 1 | 4 | 0.05 ← cycle peak balance |
| 2025-04-27 | FY25 Q2 | 8,921 | 1 | 1 | 0.02 |
| 2025-11-02 | FY25 Q4 | 8,255 | 0 | 0 | **0.00** |
| 2026-02-01 | FY26 Q1 | 7,545 | 9 | 1 | 0.13 |
| **2026-05-03** | **FY26 Q2** | **7,426** | **4** | **0** | **0.05** |

Read that again: through the sharpest ag-equipment downturn since 2015-16 — PPA sales −16% in Q3 FY2025,
AEM US tractor retail −18.4% y/y in June 2026 — **the dealers owed John Deere Financial essentially nothing
past due.** $4m non-performing on a $7,426m book. The allowance against the whole wholesale portfolio is
**$2m** (`de_wholesale_allowance`), unchanged for eight quarters, and there have been **no wholesale
write-offs disclosed in any quarter since FY2021** (blank in every filing; the CSV therefore has no
`de_wholesale_writeoffs` rows rather than fabricated zeros).

The small Q1 FY2026 uptick to $9m (3 ag + 6 construction & forestry) is the only visible blemish in five
years and it half-reversed by Q2 FY2026 (4 ag, 0 C&F). It is not a trend.

### 2.2 Dealer trade credit — stress spiked, then fully normalised

The most sensitive dealer signal Deere publishes is the share of worldwide trade receivables outstanding
**longer than 12 months** (`de_trade_receivables_pct_over_12m`). It is a direct read on how long dealers are
sitting on unsold Deere product bought on Deere's own trade credit.

```
FY2015-FY2019 (normal)   1–2%
FY2020-FY2021 (COVID)    3%
FY2022-FY2023 (boom)     1%   dealers flush, inventory turning
2024-04-28  FY24 Q2      2%
2024-07-28  FY24 Q3      3%
2024-10-27  FY24 Q4      6%   <- 10-K: "caused by increased dealer inventory levels"
2025-01-26  FY25 Q1      6%
2025-04-27  FY25 Q2      7%   <- PEAK dealer trade-credit stress, worst in the corpus
2025-07-27  FY25 Q3      3%
2025-11-02  FY25 Q4      3%   <- 10-K: "reflecting a decrease from the prior year"
2026-02-01  FY26 Q1      2%
2026-05-03  FY26 Q2      1%   <- back to the 2015-19 / boom-era baseline
```

Deere itself named the cause in the FY2024 10-K: aged trade receivables built *because dealer inventory
built*. The collapse from 7% to 1% in four quarters is the cleanest quantitative evidence that the
destocking programme worked and that dealers have cleared the aged product off their lots.
Sources: `filings/2024-11-21__de-us-20241121-q4-10k__105810.md`,
`filings/2025-05-15__de-us-20250515-q2-10q__105831.md`,
`filings/2026-05-28__de-us-20260528-q2-10q__1055932.md`.

### 2.3 Management corroborates the series

Q2 FY2026 earnings call, 21 May 2026
(`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`, line 137):

> "year-over-year on our JDF … our trade wholesale, so that used equipment that's giving finance on the
> lots of dealers, is down over 15% … That's less on their balance sheets that they've freed up and making
> more opportunity for new sales."

My independently-built series gives wholesale receivables **−16.8% y/y** at 3 May 2026 ($7,426m vs $8,921m).
The match validates the extraction. And in the prepared remarks
(`call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md`, line 105):

> dealers "have also managed the cycle and the high interest rate environment very well and very
> profitably, supported by strong owner equity."

That is a qualitative claim, but the wholesale credit data is the hard evidence behind it.

---

## 3. Key question 2 — dealer vs customer credit: a wide and widening divergence

This is the single most important analytical finding in the dataset.

| Period end | Dealer stress % | **Customer** stress % | Customer non-performing % |
|---|---|---|---|
| 2022-10-30 | 0.031 | 2.047 | 0.891 ← cycle best |
| 2023-10-29 | 0.014 | 2.240 | 1.059 |
| 2024-10-27 | 0.011 | 2.655 | 1.209 |
| 2025-01-26 | 0.012 | 3.481 | 1.474 |
| 2025-04-27 | 0.022 | 3.470 | 1.737 |
| 2025-07-27 | 0.011 | 3.294 | 1.590 |
| 2025-11-02 | 0.000 | 2.843 | 1.460 |
| 2026-02-01 | 0.132 | **3.654** ← worst in the CECL series | 1.651 |
| **2026-05-03** | **0.054** | **3.476** | **1.773** ← worst in the CECL series |

**Dealer credit is improving; end-customer credit is deteriorating, and is at its worst level since CECL
adoption.** Customer non-performing balances are $742m on $41,857m (1.77%), up from $732m/1.74% a year ago
and from 0.89% at the FY2022 trough — a doubling in three and a half years. Deere's own Q2 FY2026 10-Q
attributes the higher allowance to "higher expected losses on construction retail accounts."

Retail-notes write-offs are running at $55m/quarter (Q2 FY2026) against $56m a year earlier, and $202m for
FY2025 as a whole vs $186m in FY2024 — deterioration, but orderly, not a cliff. The FY2025 retail-notes
provision of $217m was actually *below* FY2024's $262m, so Deere is not yet building reserve aggressively.

**Why the direction matters for the forecast.** The two stories have opposite implications:

- Stress *in the channel* (dealer) → dealers cut orders below end demand regardless of retail → shipments
  undershoot → bad for Deere revenue.
- Stress *at the end customer* → retail demand is weak, but a healthy dealer with a clean lot and a
  financing partner willing to keep floor-planning **will still restock** once inventory is right-sized.

Deere is unambiguously in the second regime. The channel is not the constraint on Q3 FY2026 shipments —
end demand is.

Cross-check against the corpus dealer-inventory disclosure: US & Canada combines at **12% of trailing-12m
retail (April 2026) vs 17% LY**, 100+hp 2WD tractors at 30% vs 31%. Combines have been destocked hard; the
inventory correction is largely done in the product line that was most over-stocked, and that is exactly
what the trade-receivable ageing collapse (7% → 1%) independently confirms.

---

## 4. Key question 3 — does dealer stress LEAD shipments?

Cross-correlations of each dealer-stress series against Deere's worldwide net sales & revenues y/y growth.
"L" = the number of quarters the stress variable is shifted *forward*, i.e. X at t−L vs sales growth at t.
Coefficient and sample size reported for every lag; see §6 for the spurious-result flags.

| X (stress measure) | L0 | L1 | L2 | L3 | L4 | L5 | L6 | best |
|---|---|---|---|---|---|---|---|---|
| trade receivables >12m % | **−0.52** (43) | −0.35 | −0.12 | +0.09 | +0.24 | +0.32 | +0.34 | **L0, r=−0.52, n=43** |
| customer (retail) stress % | **−0.58** (22) | −0.45 | −0.34 | −0.21 | −0.15 | −0.01 | +0.24 | **L0, r=−0.58, n=22** |
| customer non-performing % | −0.56 (22) | −0.47 | −0.37 | −0.27 | −0.20 | −0.05 | +0.28 | L0, r=−0.56, n=22 |
| **wholesale receivables y/y %** | −0.10 (23) | −0.41 | −0.64 | −0.81 | **−0.885** (19) | −0.87 | −0.78 | **L4, r=−0.885, n=19** |
| dealer (wholesale) stress % | −0.07 (26) | +0.03 | +0.23 | +0.42 | +0.56 | +0.61 | +0.61 (20) | *spurious — see §6* |
| pre-CECL "Other" stress % | −0.37 (21) | −0.31 | −0.10 | +0.20 | +0.43 | +0.32 | +0.23 | L4, r=+0.43, n=25 |

**Result 1 — dealer past-dues do NOT lead shipments; they lag them.**
Running the trade-receivable ageing test in reverse, *sales growth leads the ageing metric* by one quarter
with r = **−0.639 (n=42)** — a stronger and better-signed relationship than any forward lag. Aged dealer
trade credit is a **consequence** of falling shipments (unsold inventory ages on the lot), not a warning of
them. The same is true of customer stress: peak contemporaneous correlation, decaying monotonically with
lag. So the direct answer to "does a rise in dealer past-dues lead a fall in shipments, and by how many
quarters?" is: **no measurable lead; the relationship is coincident-to-lagging, and the ageing metric is
best read as a confirmation that a downturn has already bitten.**

**Result 2 — the dealer floor-plan *balance* does lead, by 4 quarters, and inversely.**
`de_wholesale_receivables_total` y/y growth at t−4 vs sales growth at t: **r = −0.885, n = 19**, and it
survives dropping the FY2025-26 downturn entirely (r = −0.871, n = 13). This is the dealer-inventory cycle
made visible: when dealers' Deere-financed inventory balloons, shipments fall about a year later; when it
is drawn down, shipments recover about a year later. It is causally sensible — Deere explicitly
underproduces retail to burn off that inventory (117 "underproduction" mentions in the corpus).

Fitting `sales_yoy(t) = a + b · wholesale_yoy(t−4)` gives slope −0.308, intercept +12.6, residual SD 9.3pp.

| Lag used | Predictor value | Implied Q3 FY2026 sales y/y | Implied Q3 FY2026 revenue (on $12,018m base) |
|---|---|---|---|
| L=3 (2025-11-02, −7.5%) | −7.53% | +15.2% ±11.9 | $13.8bn (range $12.4–15.3bn) |
| L=4 (2025-07-27, −3.1%) | −3.12% | +13.6% ±9.3 | $13.7bn (range $12.5–14.8bn) |
| L=5 (2025-04-27, +3.9%) | +3.85% | +11.0% ±10.2 | $13.3bn (range $12.1–14.6bn) |

**Treat these point estimates with heavy scepticism.** The ±1sd band is ±$1.1–1.4bn, the fit spans one
inventory cycle (n=19), and the regression's slope is inflated by the extreme amplitude of the 2023 build /
2024-25 bust. What the model supports is a **sign and a floor**, not a level: every specification puts
Q3 FY2026 revenue growth comfortably positive, with the low end of the ±1sd band still at +4% (≈$12.5bn).
It does not support a $13.7bn point forecast.

---

## 5. What this implies for Q3 FY2026 (quarter ending ~2 August 2026, reporting 20 August 2026)

1. **The channel will not be the binding constraint.** Dealer balance sheets are clean by every measure
   Deere publishes: $4m non-performing on $7.4bn wholesale, $2m allowance, zero write-offs, aged trade
   credit back to 1%. A financially stressed dealer under-orders; these dealers can order.
2. **Dealer inventory has been drawn down hard and is now a tailwind, not a headwind.** Wholesale
   receivables −16.8% y/y (−$1,495m) and −$2,047m from the FY2024 Q3 peak of $9,473m; combines at 12% of trailing retail vs 17%
   LY; management explicitly framing the −15% used floor-plan as "making more opportunity for new sales."
   The wholesale-to-quarterly-sales ratio has fallen from 97.5% (Q1 FY2025) to 55.6% (Q2 FY2026).
3. **The risk has migrated to the end customer.** Customer non-performing at 1.77% is the worst of the CECL
   era and still rising. That caps how fast retail can recover and is the reason to discount the +13%
   regression output. It also raises the odds of a higher Financial Services provision in Q3 FY2026 (retail-notes
   provision $62m in Q2 FY2026 vs $55m LY; FY2025 retail-notes write-offs $202m vs $186m in FY2024).
4. **Directionally**, dealer health argues for Q3 FY2026 shipments *at or above* the trend already visible
   in H1 FY2026 (+8% revenue, Q2 +5%) rather than a relapse toward the Q3 FY2025 trough of $12,018m. The
   one measure with genuine predictive content puts the low end of its range at roughly +4% y/y.
5. **Watch on the call:** whether the >12-month trade-receivable percentage stays at 1%, whether wholesale
   non-performing stays ≤$10m, and whether the retail-customer non-performing ratio breaks above 1.80%.
   The first two would confirm dealer normalisation; the third would say the end-customer problem is
   getting worse faster than the channel is healing.

---

## 6. Data quality, caveats and flagged results

**Sources.** Every number is from Deere's own 10-Q/10-K. Values were extracted programmatically from the
SEC EDGAR XBRL "R" financial-report renderings of the *same* filings held in the offline corpus (CIK
315189, 47 filings, FY2015 Q1 → FY2026 Q2), because the corpus markdown conversion mangles multi-column
tables (merged row labels, dropped minus signs). Each CSV row cites the corresponding corpus file path.
16 spot checks against corpus text passed 16/16.

**Verified against the corpus:** wholesale total 7,426 / 8,255 / 8,921; wholesale non-performing 9 at
Q1 FY2026; retail total 41,857 / 43,409; retail non-performing 742; trade receivables net 7,571 / 5,317;
net sales & revenues 12,018 (Q3 FY2025) and 13,369 (Q2 FY2026); wholesale allowance 2; retail-notes
allowance 257; dealer incentive set-off 2,012.

**What is NOT in the data, and why:**
- **No wholesale write-off series.** Deere's allowance roll-forward shows blank in the wholesale column in
  every quarter since FY2021. Blank means nil-or-immaterial, not zero-measured; no rows were fabricated.
- **No wholesale aging finer than 30+ days after FY2021 Q4.** Deere collapsed 30-59 / 60-89 / 90+ into a
  single "30+ days past due" line for wholesale from FY2022. FY2021's three buckets are preserved as
  `de_wholesale_past_due_30_59/60_89/90plus` (8 observations each).
- **No dealer-level data of any kind.** Deere discloses the wholesale portfolio in aggregate. There is no
  way to see dispersion — a handful of stressed dealers inside a $7.4bn book with $4m non-performing is
  arithmetically impossible to hide, but regional concentration is invisible.
- **No FY2015–FY2020 dealer-only series** (see §1). `de_prececl_other_*` is a mixed portfolio.
- **Wholesale provision/recoveries are sparse** (5 and 1 observations) because Deere only reports them when
  non-zero, and only in the column that happens to carry them; rows shown only in a 6- or 9-month column
  were excluded rather than mislabelled as quarterly.
- **Q4 net sales & revenues are derived** (FY less nine-month), flagged `source_type = derived`.
- **Segment-level (PPA / SAT / CF) net sales are not in this file.** The lead/lag test uses total worldwide
  net sales & revenues. A PPA-specific test would be sharper and is the obvious extension.

**Flagged as likely spurious:** `de_wholesale_stress_pct` → sales growth, r = +0.61 at L5–L6, n = 20–21.
The wholesale stress series is a near-constant 0.01–0.13% from FY2022 onward with a handful of $1m
observations; the "correlation" is driven by the 2020–21 decay from 1.76% to 0.5% lining up with the
post-COVID revenue boom. There is no real information in it. Do not use it as a predictor. Similarly the
pre-CECL "Other" result (r = +0.43 at L4) mixes dealer and non-dealer exposures and should not be read as
a dealer signal.

**Definitional break at FY2021** (non-performing 120 days → 90 days) means the FY2026 customer
non-performing ratio of 1.77% is **not** directly comparable with the pre-CECL retail-notes stress of 3.99%
at the 2020 shock or 3.19% in the 2016 trough — different portfolios, different definitions. Compare
directions within each regime only.

**Confidence:** high on the dealer-health read (multiple independent, cleanly-extracted, management-
corroborated measures all agree). Medium-low on the quantitative Q3 FY2026 revenue mapping (one cycle,
n≈19, wide residuals).

---

## 7. Series index

`entity = dealer` (wholesale / trade credit owed by independent dealers)
`de_wholesale_receivables_total`, `de_wholesale_current`, `de_wholesale_current_ag`, `de_wholesale_current_cf`,
`de_wholesale_nonperforming`, `de_wholesale_nonperforming_ag`, `de_wholesale_nonperforming_cf`,
`de_wholesale_past_due_30plus`, `de_wholesale_past_due_30_59`, `de_wholesale_past_due_60_89`,
`de_wholesale_past_due_90plus`, `de_wholesale_allowance`, `de_wholesale_provision`, `de_wholesale_recoveries`,
`de_wholesale_stress_pct`, `de_wholesale_nonperforming_pct`, `de_wholesale_receivables_to_qtr_sales_pct`,
`de_trade_receivables_net`, `de_trade_receivables_pct_over_12m`, `de_trade_receivables_to_ttm_sales_pct`,
`de_dealer_sales_incentives_setoff`

`entity = customer` (retail / end-customer)
`de_retail_receivables_total`, `de_retail_current`, `de_retail_past_due_30_59`, `de_retail_past_due_60_89`,
`de_retail_past_due_90plus`, `de_retail_past_due_total`, `de_retail_nonperforming`, `de_retail_stress_pct`,
`de_retail_nonperforming_pct`, `de_retail_notes_allowance/provision/writeoffs/recoveries`,
`de_revolving_allowance/provision/writeoffs/recoveries`, `de_prececl_retailnotes_*`

`entity = mixed` (pre-CECL, dealer wholesale bundled with other products)
`de_prececl_other_total`, `de_prececl_other_past_due_total`, `de_prececl_other_nonperforming`,
`de_prececl_other_stress_pct`, `de_other_allowance/provision/writeoffs/recoveries`

`entity = company`
`de_net_sales_and_revenues`

## 8. Scripts

- `scripts/data/fetch_edgar_credit_reports.py`, `fetch_edgar_credit_reports2.py` — pull the FilingSummary
  and the credit-quality R-reports for all 47 DE 10-Q/10-K filings FY2015 Q1 → FY2026 Q2.
- `scripts/data/rfile_parse.py` — R-report HTML table parser (preserves empty cells, so column/date
  alignment survives sparse tables; strips XBRL element names appended in pre-2016 renderings).
- `scripts/data/extract_facts.py` — flattens every report into (filing, report, segment-context, row,
  column-date, value) facts.
- `scripts/data/build_dealer_credit_csv.py` — maps facts to the wholesale / retail / pre-CECL / allowance
  series, preferring the as-reported filing for each period end.
- `scripts/data/build_dealer_trade_and_sales.py` — trade-receivable narrative metrics from the corpus,
  trade receivable balances and quarterly net sales & revenues from EDGAR companyfacts.
- `scripts/data/finalize_dealer_credit.py` — merge, fiscal-calendar normalisation, derived ratios.
- `scripts/data/leadlag_dealer_stress.py` — cross-correlation table in §4.
