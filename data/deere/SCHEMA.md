# SCHEMA — `panel_quarterly.csv`

The wide modelling table for forecasting Deere & Company (NYSE: DE).

| | |
|---|---|
| File | `data/deere/panel_quarterly.csv` |
| Shape | **73 rows × 343 columns** (3 identifiers + 3 targets + 337 drivers) |
| Grain | one row per **Deere fiscal quarter**, FY2008 Q3 → FY2026 Q3 |
| Forecast row | last row: FY2026 Q3, `period_end` = 2026-08-02, all three targets **empty** |
| Built by | `scripts/data/build_panel.py` (stdlib only, deterministic, idempotent) |
| Audited by | `scripts/data/validate_panel.py` (8 checks, incl. a live SEC EDGAR call) |
| Machine-readable manifest | `data/deere/panel_columns.csv` — one row per column with group, units, source file, n, first/last quarter, forecast-row availability |
| Data as of | 2026-08-16. Deere has **not** reported FY2026 Q3. |

Missing data is always an **empty cell**. There are no zeros standing in for
missing, and nothing is imputed, interpolated or forward-filled.

---

## 1. How to read this file before you model on it

Four things will silently ruin a model fitted on this panel if you skip them.

**1. Join grain is `(fiscal_year, fiscal_quarter)`, not `period_end`.** Deere
switched from calendar month-ends to a 52/53-week fiscal calendar in FY2017, so
EDGAR holds two competing sets of FY2016 quarter-end dates. Three of the source
files disagree by one day on two FY2016 boundaries. The builder joins on the
(year, quarter) key and stamps one canonical `period_end` per row.

**2. Deere's fiscal quarter label leads the calendar by roughly one quarter.**
FY2026 Q3 runs 2026-05-04 → 2026-08-02, i.e. economically calendar Q2 2026. Any
external series you add yourself must be aligned the same way or every driver is
mis-timed by about a month.

**3. The `_lag1` columns exist because the un-lagged ones are not always
knowable.** See §4 — this is the look-ahead map, and it is the single most
important section in this document.

**4. `de_ppa_operating_profit` has 26 observations, not 73.** The segment did not
exist before the FY2021 reorganisation. See §3.3 and `DATA_QUALITY.md` §3.

---

## 2. Identifier columns

| column | definition | units | notes |
|---|---|---|---|
| `fiscal_year` | Deere fiscal year (ends late Oct / early Nov) | integer | FY2026 Q3 carries 2026 |
| `fiscal_quarter` | `Q1`…`Q4` | string | no `FY` rows — annual rows were filtered out at load, so Q4 is never double-counted against a fiscal-year total |
| `period_end` | canonical Deere fiscal period end | ISO date | strictly increasing; FY2026 Q3 = 2026-08-02 |
| `days_in_quarter` | length of the fiscal window | count | 84–98. FY2019 and FY2025 were 53-week years and carry one 98-day Q4. Use it to normalise flow variables. |

---

## 3. Target columns

All three are **empty on the FY2026 Q3 row by construction**; `build_panel.py`
raises a fatal error if any of them is populated there.

### 3.1 `de_net_sales_revenues_total` — TARGET 1

| | |
|---|---|
| Definition | Worldwide net sales and revenues (equipment operations + financial services), the headline top line |
| Units | USDm |
| Frequency | quarterly, 3-month figure |
| Coverage | 71 of 73 rows. FY2008 Q3 → FY2026 Q2. **FY2008 Q4 is missing.** |
| Source | `drv_peers.csv` (SEC XBRL `us-gaap:Revenues`, as-first-reported) for Q1–Q3; **Q4 overridden with the as-reported figure from the corpus Q4 8-K** |
| Transformation | none — raw reported values |
| Breaks | ASC 606 adoption (FY2019) changed revenue presentation modestly. No restatement was applied. |
| Look-ahead | This is the target. Never use its contemporaneous value as a feature. |

### 3.2 `de_eps_diluted_gaap` — TARGET 2

| | |
|---|---|
| Definition | Diluted earnings per share attributable to Deere & Company, **GAAP** |
| Units | USD/share |
| Frequency | quarterly, 3-month figure |
| Coverage | 71 of 73 rows. FY2008 Q3 → FY2026 Q2. **FY2008 Q4 is missing.** |
| Source | SEC XBRL `us-gaap:EarningsPerShareDiluted` (as-first-reported) for Q1–Q3; **Q4 from the corpus Q4 8-K** |
| Transformation | none |
| Breaks | FY2018 Q1–Q3 GAAP EPS embeds 750–803 USDm of provisional US tax-reform expense. It is a genuine GAAP figure, but it is not comparable to surrounding quarters as an operating signal. |
| Look-ahead | target |

> **Why Q4 is sourced differently.** Deere files no fourth-quarter 10-Q, so SEC
> XBRL carries **no** standalone three-month Q4 fact for either target (verified:
> zero `EarningsPerShareDiluted` facts with an 80–100 day duration ending on any
> Deere Q4 date). Every XBRL-only pipeline must derive Q4 as *fiscal year minus
> Q1+Q2+Q3*. For revenue that is right to ~1 USDm. For diluted EPS it is **wrong**,
> because the diluted share count differs every quarter: FY2025 Q4 derives to
> 3.92 against an as-reported **3.93**, FY2024 Q4 to 4.57 against **4.55**.
> `scripts/data/extract_q4_targets.py` parses the as-reported figures out of the
> nine Q4 8-Ks in the corpus and `build_panel.py` layers them on top. Seven values
> were corrected this way (FY2022–FY2025). **FY2017 and FY2018 Q4 remain derived**
> — those Q4 8-Ks are not in the corpus.

### 3.3 `de_ppa_operating_profit` — TARGET 3

| | |
|---|---|
| Definition | Production & Precision Ag segment operating profit |
| Units | USDm |
| Frequency | quarterly, 3-month figure |
| Coverage | **26 of 73 rows**, contiguous FY2020 Q1 → FY2026 Q2 (verified). Rows before FY2020 Q1 are empty. |
| Composition | **22 as-reported quarters** (FY2021 Q1 → FY2026 Q2) + **4 restated FY2020 quarters** recovered from prior-year comparative columns of the FY2021 releases |
| Source | `de_segments_modern.csv` (corpus 8-K segment tables, cross-checked against 10-Q/10-K footnotes and EDGAR XBRL R-files) |
| Segment basis | **`modern-PPA` only.** Every row is on the FY2021+ three-segment basis. |
| Look-ahead | target |

**The structural break, stated plainly.** "Production and Precision Ag" first
appears in filings dated 2021-02-19 (Q1 FY2021). Before the FY2021 reorganisation
Deere reported **one** segment, "Agriculture and Turf" (A&T). Deere recast FY2019
(annual only) and FY2020 (quarterly) onto the new basis and never went further
back. This panel therefore contains **no PPA observation before FY2020 Q1, and
none is recoverable**. The legacy A&T series is supplied separately (§4.2) and is
tagged `_legacy` in its column name — the two eras never share a column.

---

## 4. Look-ahead map — which columns are safe for which quarter

This is the section that decides whether your backtest means anything.

### 4.1 Safety tiers

| tier | groups | safe to use contemporaneously? |
|---|---|---|
| **A — safe** | `macro_fx` (market-priced), `ag_commodities`, `input_costs`, `guidance` | **Yes.** FX, rates, futures-derived prices and BLS PPIs are observable inside or within days of the quarter. Guidance is resolved point-in-time (§4.5). |
| **B — safe with care** | `equipment_demand`, `peers`, `farm_economy` | Observable **after** the quarter ends but **before** Deere reports (~3 weeks later). Fine for a "forecast on the eve of the print" exercise; not fine if you claim to forecast at quarter end. `_lag1` variants are unambiguously safe. |
| **C — NOT safe** | `deere_internal_modern`, `deere_internal_legacy`, `deere_internal_pnl` | **No.** These are Deere's own accounting lines, published in the *same press release* as the target. A contemporaneous fit is a tautology, not a forecast. |
| **D — safe** | `*_lag1` of any of the above, `macro_fx_lag1`, `farm_economy_lag1`, `calendar` | **Yes** by construction. |

`build_panel.py`'s correlation analysis excludes tier C entirely. So should your
feature set.

### 4.2 Group C in detail — Deere's own lines

Present as levels **and** `_lag1`. Only the `_lag1` form belongs in a model.

| columns | basis | coverage |
|---|---|---|
| `de_ppa_net_sales`, `de_ppa_operating_margin`, `de_sat_net_sales`, `de_sat_operating_profit`, `de_sat_operating_margin`, `de_cf_net_sales`, `de_cf_operating_profit`, `de_cf_operating_margin` | `modern-PPA` | 26 quarters, FY2020 Q1+ |
| `de_at_net_sales_legacy`, `de_at_operating_profit_legacy`, `de_cf_net_sales_legacy`, `de_cf_operating_profit_legacy` | `legacy-AT` | 37 quarters, FY2012 Q1 → FY2020 Q4 |
| `de_ppa_share_of_ag_net_sales_modern`, `de_ppa_share_of_ag_operating_profit_modern` | derived ratio | 22 quarters, FY2021+ |
| `de_net_sales_equipment`, `de_cost_of_sales`, `de_gross_profit_equipment`, `de_gross_margin_equipment` | equipment operations | 70 quarters, FY2009 Q1+ |
| `de_operating_margin` | consolidated | 42 quarters, **stops FY2023 Q3**, and is *not contiguous* — Deere tags no Q4 `OperatingIncomeLoss` in most years, so Q4 is absent throughout, and the series stops entirely after FY2023 Q3 |

**Never merge `de_at_*_legacy` with `de_ppa_*`.** They are different segments
under different definitions. A model trained across an unmarked break is
worthless. The two eras do not overlap in any column: legacy ends FY2020 Q4,
modern begins FY2020 Q1, and they carry different column names throughout.

`de_gross_margin_equipment` is on an **equipment-operations** denominator (net
sales), not the "net sales and revenues" total that is Target 1 — FY2026 Q2:
11,778 vs 13,369. Do not pair it with the total.

### 4.3 `_lag1` semantics

`x_lag1` for panel row *t* = the value of `x` at fiscal quarter *t−1*, taken on
the Deere fiscal grid. For `farm_economy` the `_lag1` variant means something
slightly different and better: it is the **prior calendar year's** annual value,
which is fully published and free of USDA forecast-vintage contamination (§4.4).

### 4.4 `farm_economy` — annual data on a quarterly grid

40 annual USDA/ERS/NASS/FAS series broadcast onto quarters. A fiscal quarter takes
the calendar year of its **window midpoint**, so FY Q1 (Nov–Jan) picks up the
prior calendar year — the year whose harvest actually drove it.

Two traps:

- **The 2025 and 2026 values are USDA forecasts, not actuals**, and USDA revises
  them heavily (the 2025 net farm income forecast was cut 14% between Sep-2025 and
  Feb-2026). Contemporaneous `farm_economy` columns on recent rows are therefore
  *a forecast of a driver*, not an observation. `*_lag1` is the clean version.
- The same annual value repeats across four consecutive quarters. That inflates
  apparent significance: 73 quarterly observations of an annual series carry at
  most ~18 independent data points. Every correlation on these series should be
  read against an effective *n* of roughly 18, not 73.

`us_farm_proprietors_income_bea_q` is the one genuinely quarterly farm-income
series (BEA). It is a **different measure** from USDA net farm income — BEA
excludes corporate farms. Use it for turning points, not levels.

### 4.5 `guidance` — point-in-time by construction

Guidance rows in the source file are vintage-encoded, and getting this wrong is
the easiest way to leak the future into the panel. The builder resolves, for each
panel quarter, **the most recent vintage of that fiscal year's guidance issued
strictly before that quarter's `period_end`**.

`validate_panel.py` check 7 verifies this on all 57 populated rows.

| column | meaning |
|---|---|
| `de_guidance_vintage_issued` | ISO date of the earnings release the guidance in this row came from |
| `de_guidance_vintage_seq` | 0 = initial (issued with the *prior* FY's Q4 results), 1 = Q1 vintage, 2 = Q2, 3 = Q3 |

On the **FY2026 Q3 forecast row this resolves to the 2026-05-21 vintage
(`vintage_seq` = 2)** — exactly what a forecaster standing on 2026-08-16 has, and
no more. This is the single most informative driver on that row.

Three cautions:

- **Deere has never guided EPS**, and consolidated revenue-growth guidance exists
  only for FY2017–FY2019 (`de_guidance_fy_net_sales_revenues_growth`, 12 rows).
  Target 2 must be reached via net income and a share-count assumption; Target 1
  bottom-up from segment sales growth.
- `de_guidance_fy_implied_ppa_operating_profit_mid` is **`source_type=inference`,
  not guidance**. Deere never guides segment operating profit in dollars. It
  compounds three error sources (prior-FY sales × guided growth × guided margin);
  historical full-year error median −56 USDm, mean +51 USDm.
- Segment operating-margin guidance comes from earnings-call **slide decks**,
  whose corpus text is an OCR/vision transcription of chart images — weaker
  provenance than filing prose.
- `de_guidance_fy_segment_*_ag_turf_*` / `_cf_legacy_at_*` are **legacy-AT basis**
  and stop at FY2021 Q4. The modern `_ppa_`/`_sat_`/`_cf_` guidance starts
  2021-02-19. FY2021 has **no** modern-basis initial vintage — the first FY2021
  guidance (2020-11-25) was still framed on the legacy A&T basis.

### 4.6 `peers` — 26 columns, nearest-quarter-end alignment

Peers run their own fiscal calendars and were **not** forced onto Deere's.
Each peer print is mapped to the Deere fiscal quarter whose **end date is
nearest**, discarding anything more than 46 days away.

Window *containment* — the obvious rule — is wrong here and was a real defect
caught in build: Toro's quarters end in early August and early November, a few
days *after* Deere's, so containment pushed Toro's Aug-3 print into Deere's
Aug–Oct quarter and left Deere's May–Jul quarter empty, shifting the whole series
by a quarter. Titan's Jan-31 year end landed two days after Deere's Q1 end and was
thrown into Q2 the same way. `validate_panel.py` check 6 confirms all 565 mapped
peer values sit within 46 days of their assigned quarter end.

| caution | detail |
|---|---|
| Margin **levels** are not comparable across companies | `us-gaap:OperatingIncomeLoss` is defined differently by each issuer. Model changes, not levels. |
| Kubota is in **JPY**, not USD | `kubota_revenue`, `kubota_operating_profit` carry a yen-translation component Deere's do not. |
| Peer Q4s are derived | most issuers file no Q4 10-Q; those values are FY minus Q1+Q2+Q3 (`source_type=inference` upstream) |
| `cnh_operating_margin`, `de_operating_margin` have hard stops | CNH stopped tagging `OperatingIncomeLoss` after 2017; Deere after FY2023 Q3. Do not interpolate. |
| Forecast-row availability | AGCO, CAT, CNH, TSCO, Valmont, Kubota **have** reported the overlapping calendar Q2 2026 quarter and are populated. **Lindsay, Titan and Toro have not** — their columns are empty on the forecast row and only their `_lag1` is available. |

### 4.7 `equipment_demand` — monthly → fiscal quarter

24 columns aggregated from monthly AEM / BLS / Fed / Sandhills data onto Deere
fiscal windows by the builder:

| rule | applied to | requirement |
|---|---|---|
| `sum` | unit-sales flows (`us_tractor_unit_sales_*`, `us_combine_unit_sales`) | **3 months must land in the window**, else the cell is left empty — a 2-of-3 sum understates a flow and reads as a demand collapse |
| `last` | stocks (`us_dealer_new_inventory_units*`, `us_dealer_new_inventory_months*`) | ≥2 months |
| `mean` | indices and percent-change series (`us_ag_equipment_ppi*`, `us_ag_constr_mining_machinery_ip`, `us_used_*_yoy_pct`) | ≥2 months |

Definitional traps carried forward from the source:

- **`us_tractor_unit_sales_100hp_plus` is 2-wheel-drive only.** All 4WD
  articulated tractors are well above 100 HP but sit on their own line. Use
  `us_tractor_unit_sales_large_total` for the aggregate the trade press means.
- **`us_tractor_unit_sales_total` is a compact-tractor series in disguise**
  (sub-40 HP is 50–69% of units) and that share is *counter-cyclical* to large ag.
  It is a poor PPA proxy that will actively mislead.
- **AEM measures retail** (dealer→farmer); **Deere books revenue wholesale**
  (Deere→dealer). The two diverge by the change in dealer inventory — which is why
  the inventory columns are here. Regressing Deere sales on AEM retail alone will
  mis-time inflections.
- AEM is **US-only**; PPA is global (North America roughly half).
- The three PPI series have **different base periods** (1982-06=100, 1982=100,
  Dec-1975=100). Compare growth rates, never levels.
- `us_ag_constr_mining_machinery_ip` is a **volume** index, not a price.

### 4.8 `macro_fx` — 20 columns, already on Deere's fiscal grid

Sourced from the `_dfq` grid, which is derived from SEC XBRL period contexts.

- **FX sign conventions are mixed.** `fx_eur_usd` is USD per EUR (rises as the
  dollar *weakens*). `fx_usd_brl` / `fx_usd_inr` / `fx_usd_cad` are foreign
  currency per USD (rise as the dollar *strengthens*). Do not pool without
  sign-correcting.
- **`usd_index_dxy_dfq` is not the DXY.** It is FRED `DTWEXBGS`, the Fed Nominal
  Broad Dollar Index (Jan 2006 = 100, ~26 economies). Its EM sensitivity is exactly
  the Brazil/India exposure that matters for Deere — but it is not the 6-currency
  ICE index and levels differ materially.
- `_qend` variants are quarter-end reads; unsuffixed are period averages.
- **`us_cpi`, `us_gdp_growth`, `us_industrial_production`, `us_housing_starts`,
  `us_consumer_sentiment` are current-vintage, not point-in-time.** They are what
  BEA/BLS/Fed/Census say *today*, not what was known when Deere reported. This is
  look-ahead in any backtest of forecast skill. `_lag1` variants are provided for
  all six; they fix the publication lag but **not** the revision problem — only
  ALFRED real-time vintages would, and those were out of scope.

### 4.9 `ag_commodities` (52) and `input_costs` (17)

Both are already on Deere's fiscal grid (`_fq` and bare ids respectively); the
calendar-quarter mirrors in the source files were dropped to avoid double
counting. Naming: `_avg_fq` = fiscal-quarter average, `_qe_fq` = quarter-end read,
`_wb_` = World Bank Pink Sheet cross-check duplicate of an IMF series.

| trap | detail |
|---|---|
| USD/bushel is **derived**, not native | converted from USD/metric-tonne export/terminal quotes. These sit *above* farm-gate prices by the local basis. USDA NASS QuickStats (native $/bu) is API-key-gated and was unavailable. |
| `px_wheat_*` (IMF) is a **Kansas City interior** quote | runs 12–32% below `px_wheat_hrw_wb` (US Gulf FOB) and the wedge *widens* with rail freight. Pick one; never splice. |
| `px_potash` has a definition break at 2020-01 | FOB Vancouver → Brazil CFR granular: a level shift that is **not** a market move |
| `px_urea` has a definition break at 2022-03 | FOB Black Sea → FOB Middle East, coinciding with the Russia/Ukraine nitrogen shock — break and genuine spike are **confounded and inseparable** from this data |
| `px_soybean_wb` is a soybean **meal** quote Dec-2007→Dec-2020 | not a like-for-like bean price over that stretch |
| `ppi_*` are **indices**, not price levels, and NSA | never place in the same regressor as a USD series untransformed |
| `px_steel_hrc` is an **index** (BLS WPU101704), not USD/ton and not coil | no keyless public source for US HRC coil spot exists |
| `px_steel_hrc_sheet` **stops FY2022 Q1** | BLS discontinued the index |
| `idx_freight_drybulk` (Kilian IGREA) goes **negative** | it is a deviation-from-trend index — must not be log-transformed |
| `px_rubber` is US cents per **pound** | not USD/tonne |
| Everything is **nominal** and **seasonal** | nothing is deflated; crop prices are strongly seasonal — deseasonalise before fitting |

**Fertiliser USD/mt levels and all `_wb_` cross-check series stop 2025-12-31** (the
Jan-2026 World Bank Pink Sheet vintage carries data only through Dec-2025), so
they are **empty on the forecast row**. Bridge with
`ppi_fertilizer_materials_avg_fq` / `ppi_nitrogenous_fertilizer_mfg_avg_fq`, which
are current through July 2026.

**FY2026 Q3 contains a nowcast.** IMF monthly data stops at June 2026, so July 2026
was index-spliced forward using matched BLS PPI month-over-month ratios for corn,
soybeans, HRW wheat and cotton. The FY2026 Q3 `_qe_fq` values rest entirely on that
spliced July figure and are the weakest numbers on the forecast row. August 2026 was
not extrapolated (the window averages 89 of 91 days).

---

## 5. Forecast-row availability (FY2026 Q3)

**269 of 337 driver columns are populated.** What is missing and why:

| missing | count | reason |
|---|---|---|
| Deere's own contemporaneous lines (`de_ppa_net_sales`, `de_cost_of_sales`, all segment columns…) | 19 | Deere has not reported. **Their `_lag1` forms are populated** and carry FY2026 Q2 — which is what a forecaster actually has. |
| Legacy-AT columns and their lags | 5 | segment ceased to exist in FY2021 |
| Fertiliser levels + World Bank `_wb_` mirrors + `px_sugar` | ~22 | source vintage stops 2025-12-31 (sugar 2026-06-30) |
| `px_steel_hrc_sheet` | 1 | BLS discontinued after Feb 2022 |
| Lindsay / Titan / Toro | 9 | have not yet reported the overlapping quarter; `_lag1` available |
| Soybean acreage, `us_soybean_price_received`, EU ag income/output | 5 | ERS/Eurostat had not published at the data cut |
| Legacy and lapsed guidance lines | 5 | series discontinued (`de_guidance_fy_net_sales_revenues_growth` ends FY2019; FS net income ends FY2024) |

---

## 6. Reproducing

```bash
python3 scripts/data/extract_q4_targets.py   # corpus Q4 8-K → de_q4_actuals_from_8k.csv
python3 scripts/data/build_panel.py \
        --analysis /tmp/analysis.md          # → panel_quarterly.csv + panel_columns.csv
python3 scripts/data/validate_panel.py       # 8 checks (needs network for check 3)
```

`build_panel.py` is idempotent and prints every Q4 override, every column it was
asked for but could not find, and every peer-alignment collision.

---

## 7. Complete column list

The exhaustive, machine-readable column dictionary is **`panel_columns.csv`**:
one row per column with `column, group, units, source_file, n_obs,
first_quarter, last_quarter, forecast_row_populated, note`.

Column counts by group:

| group | columns | median n | populated on forecast row |
|---|---|---|---|
| `target` | 3 | 71 | 0 / 3 *(by design)* |
| `deere_internal_modern` | 8 | 26 | 0 / 8 |
| `deere_internal_legacy` | 6 | 37 | 0 / 6 |
| `deere_internal_pnl` | 5 | 70 | 0 / 5 |
| `deere_internal_lag1` | 19 | 26 | 14 / 19 |
| `macro_fx` | 20 | 73 | 20 / 20 |
| `macro_fx_lag1` | 6 | 73 | 6 / 6 |
| `ag_commodities` | 52 | 73 | 28 / 52 |
| `input_costs` | 17 | 73 | 16 / 17 |
| `equipment_demand` | 24 | 37 | 24 / 24 |
| `equipment_demand_lag1` | 24 | 36 | 24 / 24 |
| `farm_economy` | 40 | 73 | 35 / 40 |
| `farm_economy_lag1` | 40 | 73 | 40 / 40 |
| `peers` | 26 | 63 | 17 / 26 |
| `peers_lag1` | 26 | 63 | 26 / 26 |
| `guidance` | 23 | 22 | 18 / 23 |
| `calendar` | 1 | 73 | 1 / 1 |

---

## 8. Recommended core driver set

343 columns against 73 rows is a superset, not a feature set. If you fit on more
than ~6 of these simultaneously you are over-fitting (see `DATA_QUALITY.md` §6).
Start here:

**For revenue and EPS**

1. `de_net_sales_revenues_total` at lag 4 (seasonal naive — the benchmark to beat)
2. `de_guidance_fy_net_income_mid` — point-in-time, `r` ≈ +0.86/+0.88, n = 56
3. `agco_revenue` — closest read-across, reports before Deere, populated on the forecast row
4. `us_crop_cash_receipts_lag1` — farm cash flow, the economic driver of ag capex
5. `us_tractor_unit_sales_large_total` — retail demand, correctly defined
6. `us_dealer_new_inventory_months_100hp_plus` — the wholesale/retail wedge
7. `fx_usd_brl_dfq`, `fx_eur_usd_dfq` — translation exposure
8. `days_in_quarter` — the 53-week years are real

**Additionally for PPA operating profit** (and read §5 of `DATA_QUALITY.md` first —
22 as-reported quarters will not support much)

9. `de_ppa_net_sales_lag1`
10. `de_guidance_fy_segment_sales_growth_ppa_mid` and
    `de_guidance_fy_segment_operating_margin_ppa_mid` (point-in-time, and the
    2026-05-21 vintage is on the forecast row)
