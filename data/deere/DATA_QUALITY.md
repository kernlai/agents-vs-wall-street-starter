# DATA QUALITY — Deere quarterly panel

An honest audit of `data/deere/panel_quarterly.csv` (73 rows × 343 columns,
FY2008 Q3 → FY2026 Q3). Read `SCHEMA.md` first for definitions.

**Bottom line up front.** The two headline targets (revenue, diluted EPS) have
71 clean quarterly observations and are well supported. The third target, PPA
operating profit, has **26 observations, of which only 22 are as-reported**, and
almost nothing in this file can be responsibly *fitted* on it. Roughly 300 of the
337 driver columns are noise for any given target; the multiple-testing arithmetic
in §4 shows why the top of a naive correlation ranking is mostly artefact. Sections
§5 and §6 say what should actually be done.

---

## 1. Verification performed

`scripts/data/validate_panel.py`, 8 checks. Each re-derives values from a source
the panel builder did **not** use for that column, so a shared bug cannot make a
check pass.

| # | check | result |
|---|---|---|
| 1 | Structural integrity: shape, unique keys, strictly increasing `period_end`, forecast-row targets empty, no zeros standing in for missing | **PASS** |
| 2 | Targets vs `de_predictability.csv` — a **different extraction agent's** independent read | **140 / 142** — 2 diffs, both resolved below |
| 3 | Targets vs the **live SEC EDGAR XBRL** `companyconcept` API (CIK 315189, fetched at build time) | **132 / 132 exact** |
| 4 | `de_ppa_operating_profit` vs `de_segments_legacy.csv`'s independently extracted restated PPA series over the FY2020 overlap | **4 / 4** |
| 5 | `de_ppa_net_sales + de_sat_net_sales + de_cf_net_sales` vs `de_net_sales_equipment` | **26 / 26**, max residual **0 USDm** |
| 6 | Every mapped peer print within 46 days of its assigned Deere quarter end | **565 / 565** |
| 7 | Guidance vintage issued strictly before the row's `period_end` (no look-ahead) | **57 / 57** |
| 7b | Forecast row uses the 2026-05-21 vintage — the newest a forecaster on 2026-08-16 has | **PASS** |

### 1.1 Discrepancies found, and which value was kept

Nothing here was silently resolved.

**(a) Q4 diluted EPS — a real error, found and fixed.** Deere files no Q4 10-Q,
so SEC XBRL carries **zero** standalone three-month Q4 facts for either target
(verified directly against the API). The upstream `drv_peers.csv` derives Q4 as
*FY minus Q1+Q2+Q3*. For revenue that is accurate to ~1 USDm. For diluted EPS it is
**arithmetically invalid**, because the diluted share count differs every quarter.

| quarter | XBRL-derived | corpus 8-K as-reported | kept |
|---|---|---|---|
| FY2022 Q4 EPS | 7.39 | **7.44** | 8-K |
| FY2023 Q4 EPS | 8.23 | **8.26** | 8-K |
| FY2024 Q4 EPS | 4.57 | **4.55** | 8-K |
| FY2025 Q4 EPS | 3.92 | **3.93** | 8-K |
| FY2023 Q4 revenue | 15,411 | **15,412** | 8-K |
| FY2024 Q4 revenue | 11,144 | **11,143** | 8-K |
| FY2025 Q4 revenue | 12,395 | **12,394** | 8-K |

Corrected by `scripts/data/extract_q4_targets.py`, which parses the nine Q4 8-Ks
in the corpus. **FY2017 and FY2018 Q4 are still derived** — those 8-Ks are not in
the corpus. Their EPS is therefore accurate to roughly ±0.05.

> That extractor itself shipped a bug on its first run: Deere's older releases
> print sub-dollar EPS with no leading zero (`$ .90`), which failed the number
> regex, so the parser skipped the current-year cell and returned the **prior-year
> comparative** — FY2016 Q4 came out as 1.08 instead of 0.90. Caught by reading the
> release. Fixed and re-run. Mentioned because it is exactly the class of silent
> corruption that hand-transcription produces at scale.

**(b) FY2017 Q1 / Q2 diluted EPS — a genuine two-value case.** SEC XBRL carries
**both** 0.61 and 0.62 for Q1, and both 2.49 and 2.50 for Q2 (Deere's ASU 2017-07
restatement). `de_predictability.csv` carries the restated 0.62 / 2.50. The
authoritative corpus 8-Ks state *"$0.61 per share, for the first quarter ended
January 29"* and *"$2.49 per share, for the second quarter ended April 30, 2017"*.
**Kept the as-first-reported 0.61 / 2.49** — consistent with the panel's
no-look-ahead convention. These are the only 2 remaining diffs in check 2.

**(c) Peer alignment — a real defect caught during build.** Mapping peer prints to
the Deere quarter whose *window contains* them shifted Toro and Titan Machinery by
a full quarter (Toro's quarters end days after Deere's; Titan's Jan-31 year end
lands 2 days after Deere's Q1 end). Rewritten to nearest-quarter-end matching.
Both `build_panel.py` and check 6 now guard it.

**(d) CAT 2011 Q1** is tagged with two period ends (2011-03-30 and 2011-03-31) —
an issuer date drift. The nearer print is kept; logged as a build warning.

---

## 2. Coverage

### 2.1 Targets

| target | n | span | missing |
|---|---|---|---|
| `de_net_sales_revenues_total` | **71 / 73** | FY2008 Q3 → FY2026 Q2 | FY2008 Q4; FY2026 Q3 *(the forecast row)* |
| `de_eps_diluted_gaap` | **71 / 73** | FY2008 Q3 → FY2026 Q2 | FY2008 Q4; FY2026 Q3 |
| `de_ppa_operating_profit` | **26 / 73** | FY2020 Q1 → FY2026 Q2, contiguous | everything before FY2020 Q1 |

**FY2008 Q4** is absent from every extraction file, including the two independent
Deere-financials extractions. It is a genuine hole, not a merge failure. Practical
effect: the usable continuous history starts **FY2009 Q1**, giving **70 quarters**.

### 2.2 Drivers, by coverage band

| band | driver columns |
|---|---|
| 60–73 quarters (full) | 219 |
| 30–59 (partial) | 69 |
| 16–29 (thin) | 36 |
| 1–15 (**not modellable**) | 13 |
| 0 (empty) | 0 |

The 13 unmodellable columns are the Sandhills used-equipment series (8–13 quarters
each, starting FY2023–FY2024) and `de_guidance_fy_net_sales_revenues_growth`
(12 quarters, FY2017–FY2019, then Deere stopped publishing the line). **Do not fit
on any of them.** They are retained because they are the only used-equipment signal
in existence and are informative to *look at* on the forecast row.

### 2.3 The AEM unit-sales series is not contiguous — read this before using it

`us_tractor_unit_sales_large_total` spans FY2011 Q2 → FY2026 Q3 but holds only
**37 of the 62 quarters in that span — 25 are missing inside the span**, across 15
separate gaps. Causes, compounding:

1. The Internet Archive holds **no AEM US ag report between 2006-03 and 2010-11**,
   so 2007–2009 are entirely absent upstream and 2006/2010 nearly so.
2. Coverage between 2011 and 2022 is patchy at the monthly level.
3. The builder requires **all 3 months** inside a fiscal window before summing a
   flow — a 2-of-3 sum understates the quarter and reads as a demand collapse. Any
   single missing month therefore voids the quarter.

**The last 12 quarters (FY2023 Q4 → FY2026 Q3) are complete.** So AEM units are a
recent-window indicator, not a long-history regressor. Every correlation reported
for these columns rests on *n* ≈ 13–22, mostly post-2021 — one cycle. Same caveat
applies to `us_dealer_new_inventory_months_*` (30 quarters over a 15-year span).

---

## 3. Structural breaks

### 3.1 The FY2021 segment reorganisation — the one that matters most

Before FY2021 Deere reported **one** segment, Agriculture & Turf. From Q1 FY2021
(filings dated 2021-02-19) it reports **Production & Precision Ag**, **Small Ag &
Turf** and **Construction & Forestry**. Deere recast FY2019 (annual only) and
FY2020 (quarterly) onto the new basis and **never went further back**.

Consequences that a modeller must accept rather than engineer around:

- `de_ppa_operating_profit` **cannot** exist before FY2020 Q1. There is no
  extraction failure here; the number was never computed by anyone.
- The panel never merges the eras. Legacy columns carry `_legacy` in the name and
  stop at FY2020 Q4; modern columns start FY2020 Q1. No column spans both.
- **Back-casting PPA into the legacy era does not work.** The upstream bridge
  agent tested it out of sample: applying the FY2019/FY2020 split ratio to FY2021+
  actuals gives net-sales MAPE 7.8% quarterly with a systematic −6.5% understatement,
  and **operating-profit MAPE 15.9% with a worst quarter of +57.5%**. The PPA share
  of A&T operating profit ranged **0.415 → 0.960** over FY2021–FY2026 Q2 (sd 0.124)
  and is pro-cyclical, so a fixed ratio breaks hardest exactly at the turning points
  you would want a longer history for. A quarterly PPA operating-profit back-cast is
  **not usable**. That is why none is in this panel.
- The reorganisation *was* a clean partition — A&T net sales 23,666 = PPA 13,364 +
  SAT 10,302 and A&T operating profit 2,506 = PPA 1,729 + SAT 777 at FY2019, with
  C&F unchanged. So the *legacy* series remain internally consistent; it is only the
  PPA/SAT split that cannot be projected backwards.

### 3.2 Other breaks, in rough order of danger

| break | date | effect |
|---|---|---|
| **ASU 2017-07** | FY2018 | Changed the *definition* of operating profit (only pension/OPEB service cost stays in). Deere restated FY2016–FY2017 upward but never FY2015 or earlier. `de_at_operating_profit_legacy` is **not definitionally comparable across FY2017/FY2018**. |
| **Wirtgen acquisition** | 2017-12-01 | Roughly doubles C&F net sales between FY2017 (5,718) and FY2018 (10,160). That is acquisition, not organic growth. |
| **Dealer reporting-lag change** | FY2021 Q1 | Elimination of the one-month lag added a one-off **+$270m** to C&F net sales; prior periods were not restated. |
| **53-week fiscal years** | FY2019, FY2025 | One 98-day Q4 in each. Use `days_in_quarter` to normalise flows. |
| **Fiscal-calendar switch** | FY2017 | Calendar month-ends → 52/53-week. EDGAR holds two competing FY2016 quarter-end sets; the panel joins on (year, quarter) and stamps as-originally-reported dates. A one-day seam remains at the FY2016 Q4 / FY2017 Q1 join. |
| **ASU 2023-07** | FY2025 | Restructured the segment footnote. Net sales and operating profit values are unchanged (verified 12/12), but surrounding line items and XBRL tagging change at FY2025 Q1. |
| **US tax reform** | FY2018 Q1–Q3 | GAAP EPS embeds 750–803 USDm of provisional tax expense — a genuine GAAP figure but not an operating signal. |
| **`px_potash` definition** | 2020-01 | FOB Vancouver → Brazil CFR granular. Level shift, not a market move. |
| **`px_urea` definition** | 2022-03 | FOB Black Sea → FOB Middle East, coinciding with the Russia/Ukraine nitrogen shock. Break and genuine spike are **confounded and inseparable**. |
| **`px_steel_hrc_sheet` discontinued** | Feb 2022 | series stops at FY2022 Q1 |
| **`de_operating_margin` / `cnh_operating_margin` stop** | FY2023 Q3 / 2017 | issuers stopped tagging `OperatingIncomeLoss`. **Do not interpolate.** |

### 3.3 Look-ahead risk that is *not* fixed

`us_cpi`, `us_gdp_growth`, `us_industrial_production`, `us_housing_starts` and
`us_consumer_sentiment` are **current-vintage, not point-in-time**. Past-quarter
values are what the agencies say *today*, not what was known when Deere reported.
The `_lag1` variants fix the publication lag but **not** the revision problem. Only
ALFRED real-time vintages would, and those were out of scope. The same applies, more
severely, to the 2025–2026 USDA farm-economy rows, which are **forecasts** that USDA
revises heavily (the 2025 net farm income forecast was cut 14% between Sep-2025 and
Feb-2026). Use `farm_economy_lag1` where possible.

---

## 4. Preliminary driver analysis

### 4.1 The multiple-testing problem, quantified first

The full scan in the build report covers **316 ex-ante-safe driver columns × 5 lags
× 3 targets × 3 transforms ≈ 14,200 correlations**.

At *n* = 70 the 5% two-sided critical value is **|r| ≈ 0.235**. Across 14,200 tests,
roughly **710 hits at that threshold are expected by pure chance**. A Bonferroni-style
threshold is **|r| ≈ 0.49**.

Worse, the naive ranking is dominated by two artefacts:

- **Common trend.** Deere revenue, steel prices, freight indices, farm asset values
  and CPI all rise together over 2009–2026. `idx_freight` correlates with revenue at
  **r = +0.845 (n = 70)** in levels. There is no mechanism by which the Baltic-style
  freight index drives Deere's top line at a one-quarter lag; both are riding the same
  global industrial cycle. Ignore level correlations on trending series.
- **Seasonality.** In the QoQ-difference scan, `de_guidance_vintage_seq` reaches
  **r = −0.873**. That column is literally a counter of which quarter of the fiscal
  year you are in. It is a quarter dummy in disguise, and its "significance" measures
  only that Deere revenue is seasonal. `tsco_operating_margin` at r = −0.919 (n = 33)
  is the same artefact with a company name on it.

**Treat every table below as a hypothesis list, not a finding list.** Prefer a driver
with a mechanism over one that merely fits.

### 4.2 Target 1 — `de_net_sales_revenues_total`

Economically motivated candidates, best lag 0–4:

| driver | transform | lag | r | n | reading |
|---|---|---|---|---|---|
| `de_net_sales_equipment_lag1` | YoY | 0 | **+0.856** | 65 | Deere's own prior-quarter equipment sales. Strongest honest predictor; it is momentum, not information. |
| `de_guidance_fy_net_income_mid` | level | 0 | **+0.863** | 56 | point-in-time management guidance. Genuine information, and available on the forecast row. |
| `agco_revenue` | YoY | 0 | **+0.829** | 63 | closest read-across. Coincident-to-slightly-lagging, *not* leading (see 4.5). |
| `us_crop_cash_receipts_lag1` | level | 0 | +0.773 | 71 | farmer cash flow → ag capex. Clear mechanism; but annual data on a quarterly grid, so effective *n* ≈ 18. |
| `us_net_farm_income_lag1` | level | 0 | +0.775 | 71 | same caveat |
| `cat_revenue` | YoY | 0 | +0.727 | 66 | construction read-across; C&F is ~20% of Deere |
| `us_ag_constr_mining_machinery_ip` | YoY | 0 | +0.654 | 67 | Fed production volume index — complete history, no revision-free guarantee |
| `px_soybean_avg_fq` | YoY | 0 | +0.611 | 67 | crop price → farmer income → equipment demand. Mechanism is real but two steps removed. |
| `px_corn_avg_fq` | YoY | 0 | +0.581 | 67 | as above |
| `us_tractor_unit_sales_large_total` | YoY | 0 | +0.540 | **22** | correct mechanism (retail demand), but see §2.3 — one cycle only |
| `fx_usd_brl_dfq` | YoY | 0 | −0.429 | 67 | stronger BRL-per-USD → translation drag. Correct sign, modest. |
| `ppi_ag_machinery` | YoY | 1 | +0.387 | 66 | Deere's own realised pricing, weak at quarterly frequency |
| `us_dealer_new_inventory_months_100hp_plus` | level | 2 | −0.352 | **27** | correct sign (destocking → weaker wholesale) but thin |

**Likely spurious, despite topping the naive ranking:** `idx_freight` (+0.845, level,
n = 70), `us_farm_debt_total` (+0.79, QoQ), `br_soybean_area_harvested` (+0.79, QoQ),
`eu_ag_output` (+0.826, level), `px_steel_hrc` (+0.812, level). All are common-trend
or seasonal artefacts. None has a defensible one-to-three-quarter causal channel into
Deere's reported top line.

### 4.3 Target 2 — `de_eps_diluted_gaap`

| driver | transform | lag | r | n | reading |
|---|---|---|---|---|---|
| `de_guidance_fy_net_income_mid` | level | 0 | **+0.880** | 56 | the strongest driver in the file, and the only one that is genuine forward information |
| `us_crop_cash_receipts_lag1` | level | 0 | +0.781 | 71 | effective *n* ≈ 18 |
| `de_gross_margin_equipment_lag1` | level | 0 | +0.628 | 69 | margin persistence |
| `us_tractor_unit_sales_large_total` | YoY | 0 | +0.590 | **22** | thin |
| `agco_revenue` | YoY | 1 | +0.312 | 62 | **note the collapse** — AGCO tracks Deere's *revenue* well (+0.83) but its *EPS* barely at all |
| `agco_eps_diluted` | YoY | 3 | +0.298 | 60 | peer EPS carries almost no information about Deere EPS |
| `px_corn_avg_fq` | YoY | 1 | +0.282 | 66 | weak |

**The important negative result:** EPS is materially harder than revenue. Peer EPS
read-across is near-useless (r ≈ 0.3), because EPS is revenue × margin × tax ×
buyback, and the last three are company-specific. Deere has **never guided EPS**, so
Target 2 must be reached through net income plus a share-count assumption. EPS is also
the noisiest target — the seasonal-naive benchmark has **MAPE 46.3%** against 14.8% for
revenue (§6.1).

### 4.4 Target 3 — `de_ppa_operating_profit`: what can and cannot be fitted

**26 observations. 22 as-reported. 4 restated FY2020 comparatives.** After a YoY
transform, 22. After a YoY transform and a 4-quarter lag, 18.

State this plainly: **you cannot fit a multivariate model on this series.** With 22
usable points, a regression with more than **two** free parameters is over-fitting by
any standard. Cross-validation will not save you — every fold is drawn from a single
2021–2026 cycle that contains one enormous boom (FY2022–FY2023) and one sharp
downturn (FY2025–FY2026). There is no second cycle to validate against.

What the scan returns, and why most of it is noise:

| driver | transform | lag | r | n | verdict |
|---|---|---|---|---|---|
| `de_guidance_fy_segment_sales_growth_ppa_mid` | level | 4 | +0.752 | 17 | **usable, with a mechanism** — point-in-time and on the forecast row |
| `de_guidance_fy_segment_operating_margin_ppa_mid` | level | 0 | +0.708 | 21 | **usable** — management's own margin view, same vintage discipline |
| `us_dealer_new_inventory_months_100hp_plus` | level | 4 | −0.652 | 17 | correct sign and mechanism, but *n* = 17 |
| `de_ppa_net_sales_lag1` | level | 1 | +0.570 | 24 | momentum |
| `us_tractor_unit_sales_large_total` | YoY | 0 | +0.719 | **13** | right mechanism, unusable *n* |
| `us_crop_cash_receipts_lag1` | level | 0 | +0.593 | 26 | effective *n* ≈ 7 (annual series) |
| `agco_operating_margin` | level | 1 | +0.508 | 19 | margin definitions differ by issuer — levels not comparable |
| **`px_potash_avg_fq`** | **level** | **4** | **+0.815** | **26** | **spurious. Do not use.** |
| **`px_wheat_avg_fq`** | **level** | **4** | **+0.810** | **26** | **spurious. Do not use.** |

> **Why the wheat and potash correlations are traps.** They top the raw ranking for
> this target and they are artefacts. The whole 26-quarter PPA window (FY2020 Q1 →
> FY2026 Q2) contains exactly one commodity inflation surge and one deflation, and PPA
> operating profit followed the same arc. Any series with that shape scores ~0.8 — the
> fertiliser and grain price columns, `us_cpi_yoy`, and `titn_operating_margin` all do.
> Wheat is not even Deere's main crop exposure (corn and soybeans are), and
> `px_corn_avg_fq` only reaches +0.36. A driver that beats the economically correct
> version of itself by 0.45 is measuring the cycle, not the mechanism. Compounding it,
> `px_potash` has a **definition break in 2020-01**, one quarter into this window.

### 4.5 Peer lead/lag — the widely assumed relationship is backwards

AGCO is the best read-across on every window (contemporaneous r = +0.829, n = 63;
+0.861 at k = −1; non-overlapping annual r = +0.931, n = 17). But its lag profile
**peaks at k = −1 and decays monotonically on both sides**, as do CAT's and CNH's —
meaning **Deere moves first and AGCO follows**. AGCO is not a leading indicator.

The only genuinely leading peers are weak: Lindsay at +3 quarters (r = +0.603, n = 55)
and Tractor Supply at +2 (r = +0.415, n = 61, annual p = 0.40 — indistinguishable from
zero). Titan's apparent k = −3 peak sits on a flat profile (+0.59 to +0.64 across
k = −4…0) and carries no information.

The practical value is timing, not lead: AGCO's calendar-Q2-2026 print lands about
three weeks *before* Deere's FY2026 Q3 report, and **it is already on the forecast
row**. For that quarter AGCO implies roughly flat Deere growth while CAT implies
mid-teens — a **−3% to +21% spread across peers**, which is itself the main finding.

### 4.6 Effective sample sizes — apply these, not the nominal `n`

| series family | nominal n | effective n | why |
|---|---|---|---|
| YoY transforms | ~65 | **~16** | overlapping 4-quarter windows; residuals are serially correlated and nominal p-values are roughly 2× too optimistic |
| `farm_economy` (annual) | 73 | **~18** | one annual value repeated across four quarters |
| `farm_economy` in YoY | ~65 | **~17** | as above |
| AEM units / dealer inventory | 22–41 | **as shown, mostly post-2021** | gap-riddled; see §2.3 |
| `de_ppa_operating_profit` | 26 | **22 as-reported, one cycle** | see §4.4 |
| `guidance` | 22–57 | 4 vintages per fiscal year, highly autocorrelated within a year | |

---

## 5. Series too short or too sparse to model on

**Never fit:** all 13 Sandhills used-equipment columns (8–13 quarters);
`de_guidance_fy_net_sales_revenues_growth` (12).

**Fit only with an explicit small-sample method, never in a multivariate
regression:** `de_ppa_operating_profit` and all `de_ppa_*` / `de_sat_*` /
`de_cf_*` modern-segment columns (26); all modern segment guidance columns (21–22);
`us_dealer_new_inventory_months_*` (30); `us_tractor_unit_sales_*` and
`us_combine_unit_sales` (37, gap-riddled).

**Do not interpolate across the hard stops:** `de_operating_margin` (ends FY2023 Q3
and has no Q4 in any year), `cnh_operating_margin` (ends 2017), `px_steel_hrc_sheet`
(ends FY2022 Q1), all fertiliser USD/mt levels and `_wb_` mirrors (end 2025-12-31).

**Do not use at all as a PPA proxy:** `us_tractor_unit_sales_total` — it is a
compact-tractor series in disguise (sub-40 HP is 50–69% of units) and that share is
*counter-cyclical* to large ag. It will actively mislead.

---

## 6. RECOMMENDATION — how to model this, given what is actually here

### 6.1 Benchmarks the model must beat

Computed on this panel, seasonal-naive (ŷₜ = yₜ₋₄):

| target | n | MAE | MAPE | median APE |
|---|---|---|---|---|
| revenue | 67 | 1,374 USDm | **14.8%** | 13.5% |
| diluted EPS | 67 | 1.04 USD | **46.3%** | 24.5% |
| PPA operating profit | 22 | 486 USDm | **64.9%** | 46.2% |

If a fitted model does not beat these out of sample, it is not adding value.

### 6.2 The strongest structural fact in the data

Deere's revenue seasonality is extremely stable. Share of fiscal-year revenue,
FY2010–FY2025 (n = 16):

| quarter | mean share | sd |
|---|---|---|
| Q1 | 20.1% | 1.54 pp |
| Q2 | 28.0% | 1.11 pp |
| **Q3** | **26.2%** | **0.62 pp** |
| Q4 | 25.8% | 1.92 pp |

**Q3 is the most stable quarter Deere has** — a 0.62 pp standard deviation on its
share of the year. And the Q3/Q2 sequential ratio over FY2010–FY2025 is **0.937 with
sd 0.047** (last five years: 0.945), ranging 0.854–1.055.

That single ratio, applied to the known FY2026 Q2 revenue of 13,369 USDm, brackets
FY2026 Q3 revenue at roughly **11,900–13,150 USDm** with no model at all. Any
regression should be judged against that anchor, not against zero.

### 6.3 Recommended approach, per target

**Revenue.** A *ratio-to-prior-quarter* or *share-of-fiscal-year* model, not a level
regression. Specifically: model log(Q3 / Q2) with **at most 2–3 regressors** chosen
for mechanism — point-in-time guidance (`de_guidance_fy_segment_sales_growth_ppa_mid`
plus the SAT and CF equivalents, which together *are* the company's own revenue
bridge), a peer read-across (`agco_revenue` YoY, on the forecast row), and a
farmer-cash-flow term (`us_crop_cash_receipts_lag1`). This respects the seasonality,
sidesteps the common-trend problem, and keeps parameters ≈ 4 against ~65 usable
quarters — a defensible 16:1 ratio.

**Diluted EPS.** Do **not** model EPS directly. Model it as a composition:
(i) revenue from the above, (ii) equipment gross margin, which is persistent
(`de_gross_margin_equipment_lag1`, r = +0.628), (iii) a share count taken from the
most recent 10-Q rather than estimated. Then reconcile against the **point-in-time
FY2026 net income guidance minus reported H1 actuals** — the upstream guidance agent
supplies exactly this construct (`fy_h2_net_income_implied_by_q2_guidance` in
`de_guidance_vs_actual.csv`), with historical realised errors on the same inference
back to FY2013. A direct EPS regression will chase the FY2018 tax-reform quarters and
the noisy derived Q4s.

**PPA operating profit.** With 22 as-reported quarters spanning one cycle, the honest
answer is a **margin-on-sales identity, not a regression**: forecast PPA net sales
(the guidance gives segment sales growth directly), apply a PPA operating margin
anchored on management's own point-in-time margin guidance and the trailing
four-quarter realised margin, and publish a wide interval. At most **one** free
parameter should be estimated from the data. Note that the upstream agent measured
the FY-level error of the guidance-implied PPA operating profit construct — median
−56 USDm, mean +51 USDm — which is a usable prior for the interval width.

### 6.4 What would definitely be over-fitting

- Any regression with **more than ~4 regressors** on revenue or EPS (~65–70 usable
  quarters, and effective *n* ≈ 16 after a YoY transform).
- Any regression with **more than 2 parameters** on PPA operating profit.
- **Any** use of the 337-column panel as an undifferentiated feature matrix — LASSO,
  random forest, gradient boosting, PCA on all columns. With p ≫ n and ~14,200
  candidate correlations, these will select `idx_freight`, `px_potash`,
  `de_guidance_vintage_seq` and `tsco_operating_margin`, all of which are artefacts
  documented above, and will produce a confidently wrong forecast.
- **Any** contemporaneous Deere-internal column (`deere_internal_*` groups). Those
  are published in the same press release as the target; a model using them is
  reporting, not forecasting. They are empty on the forecast row precisely because
  they are unknowable there.
- Stepwise or best-subset selection over the full column set. The multiple-testing
  arithmetic in §4.1 guarantees it finds artefacts.
- Fitting `de_ppa_operating_profit` on anything back-cast into the legacy-AT era. The
  out-of-sample back-cast error is 15.9% MAPE quarterly with a worst quarter of
  +57.5%; it is not usable and none is supplied.

### 6.5 Residual uncertainty a forecaster should carry

- **FY2026 Q3 ag-commodity `_qe` values rest on a July-2026 nowcast** (IMF data stops
  June 2026; July was index-spliced from BLS PPI ratios). They are the weakest numbers
  on the forecast row.
- **Fertiliser price levels do not exist for calendar 2026** at all.
- **Lindsay, Titan and Toro have not reported** the overlapping quarter, so the peer
  read-across on the forecast row rests on AGCO, CAT, CNH, TSCO, Valmont and Kubota.
- **AEM's July 2026 print covers the month Deere's Q3 ended**, so it is a partial
  overlap with the unreported quarter — informative, but not a read on it.
- **The corpus `INDEX.md` row labelled `2026-05-21 | Call Transcript | Q3 2026` is
  mislabelled Q2 FY2026 material.** It was not used as a Q3 source anywhere in this
  panel, and no FY2026 Q3 Deere actual exists in the corpus, on EDGAR, or in this file.
