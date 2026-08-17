# drv_steel_inputs — steel and input-cost drivers for Deere & Company (DE)

Companion to `drv_steel_inputs.csv`. Built 2026-08-16. Corpus frozen 2026-08-14.

**Contents:** 3,050 rows / 38 series. Input-cost drivers 2006-01-31 → 2026-08-02 (83 Deere
fiscal quarters, the full 20-year target). Deere gross-margin series FY2009 Q1 → FY2026 Q2
(70 quarters, no gaps).

**No FY2026 Q3 Deere actuals are present and none exist.** The Deere series stop at the
FY2026 Q2 period end of 2026-05-03. The *input-cost* series do extend to the FY2026 Q3 slot
(period end 2026-08-02) because the underlying BLS/IMF/EIA monthly data for May–July 2026 is
published — that is the point of the file, those are the leading indicators available now.

## Reproducing

```
python3 scripts/data/build_drv_steel_inputs.py     # writes the CSV + prints validation
python3 scripts/data/analyse_steel_lag.py          # the lag analysis below
```

`scripts/data/de_corpus_income.py` is the corpus income-statement parser used by both.
Standard library only. Full analysis output is saved at `drv_steel_inputs_lag_output.txt`.

---

## 1. Series

Every input-cost series appears twice: once aligned to **Deere fiscal quarters** (bare
`series_id`) and once to **calendar quarters** (`_cq` suffix). They are the same underlying
monthly data on two alignments — pick one, never both.

Fiscal bucketing: FQ1 = Nov+Dec+Jan, FQ2 = Feb+Mar+Apr, FQ3 = May+Jun+Jul, FQ4 = Aug+Sep+Oct.
Quarterly value = simple mean of the monthly observations in the bucket. `period_end` is
Deere's actual reported fiscal quarter end (from the filings where available, from SEC XBRL
contexts otherwise, from the pre-2016 calendar-month-end rule before that).

| series_id | source id | units | what it is |
|---|---|---|---|
| `px_steel_hrc` | FRED/BLS `WPU101704` | index | PPI hot rolled steel **bars, plates and structural shapes**, NSA, 1982=100 |
| `px_steel_hrc_sheet` | `WPU101703` | index | PPI hot rolled **sheet and strip**. **Discontinued by BLS after Feb 2022** |
| `px_steel_cold_rolled` | `WPU101707` | index | PPI cold rolled sheet and strip — continuous flat-rolled proxy |
| `px_steel_scrap` | `WPU1012` | index | PPI iron and steel scrap |
| `px_steel_scrap_carbon` | `WPU101211` | index | PPI carbon steel scrap, 1986-12=100 |
| `ppi_steel_mill_products` | `WPU1017` | index | PPI steel mill products (the aggregate) |
| `ppi_ag_machinery` | `WPU111` | index | PPI agricultural machinery and equipment — Deere's **output** price proxy |
| `ppi_ag_machinery_industry` | `PCU333111333111` | index | PPI NAICS 333111 farm machinery mfg — cross-check on the above |
| `px_aluminium` | `PALUMUSDM` | USD/mt | IMF global aluminum, LME cash |
| `px_copper` | `PCOPPUSDM` | USD/mt | IMF global copper, LME grade A |
| `px_rubber` | `PRUBBUSDM` | **UScents/lb** | IMF natural rubber. Note the unit |
| `px_rubber_synthetic_ppi` | `WPU071102` | index | PPI synthetic rubber |
| `px_diesel` | `GASDESW` | USD/gal | EIA US No.2 diesel retail, weekly → monthly → quarterly |
| `px_diesel_ppi` | `WPU057303` | index | PPI No.2 diesel — producer level |
| `idx_freight` | `PCU484121484121` | index | PPI long-distance truckload trucking, Dec 2003=100 |
| `idx_freight_drybulk` | `IGREA` | index | Kilian global real activity index (dry-bulk ocean freight). **Can be negative** |
| `px_iron_ore` | `PIORECRUSDM` | USD/dmt | IMF iron ore, China import 62% Fe |
| `de_net_sales_equipment` | corpus / SEC XBRL | USDm | Deere **Net sales** (equipment operations) |
| `de_cost_of_sales` | corpus / SEC XBRL | USDm | Deere **Cost of sales** |
| `de_gross_profit_equipment` | derived | USDm | net sales − cost of sales |
| `de_gross_margin_equipment` | derived | percent | 100 × gross profit / net sales |

### The one substitution a modeller must know about

**`px_steel_hrc` is an index, not USD/ton, and it is not coil.** There is no keyless public
source for US hot-rolled **coil** spot in USD/ton. CRU and Platts HRC assessments — the series
everyone quotes — are commercial and paywalled. Stooq's CSV endpoint, which would have given
CME HRC futures, is behind a JavaScript proof-of-work challenge and returns no data.

So `px_steel_hrc` carries BLS `WPU101704`, hot rolled bars/plates/structural shapes. Two
reasons that is defensible rather than a fudge: it is continuous over the whole 2006–2026
window, and for Deere specifically — frames, axles, plate, heavy weldments — long products and
plate are closer to the actual steel buy than coil is. The genuine hot-rolled *sheet* index
(`px_steel_hrc_sheet`) is provided but BLS discontinued it after February 2022, which is why it
cannot be the backbone. `px_steel_cold_rolled` is the continuous flat-rolled alternative.

If you need real USD/ton HRC you must buy it. Do not rescale an index to look like a price.

### Deere series definition

`de_net_sales_equipment` is the **Net sales** line of the consolidated income statement:
equipment operations only. It excludes Finance and interest income and Other income, so it is
*not* "worldwide net sales and revenues" (the forecast target). For FY2026 Q2: net sales 11,778
vs total net sales and revenues 13,369. Gross margin is defined against net sales because cost
of sales is an equipment-operations cost — pairing it with the total would understate the ratio.

There is no PPA segment content in this file, so the segment-basis break does not bite here.
Gross margin is consolidated and continuous across the FY2021 reorganisation.

---

## 2. Validation

Six independent checks, all clean.

| # | Check | Result |
|---|---|---|
| A | FRED CSV vs **BLS public API v1**, same 5 PPI ids, 120 monthly obs each (600 comparisons) | max abs diff **0.000** |
| B | Corpus **8-K earnings release vs 10-Q**, same quarter, net sales + cost of sales | **35 quarters, 0 disagreements** |
| C | Derived gross profit vs separately tagged **SEC XBRL `us-gaap:GrossProfit`** | 48 quarters, max diff **1.0 USDm** (a rounding artefact at FY2020 Q1) |
| D | `ppi_ag_machinery` (WPU111, commodity basis) vs `ppi_ag_machinery_industry` (NAICS 333111) | corr 0.9995 over 83 quarters |
| E | Deere FY2022 Q4 net sales: 8-K three-month column = **14,351**; 10-K FY total 47,917 minus the three 10-Q quarters (8,531+12,034+13,000) = **14,352** | agree to 1 USDm rounding |
| F | All 24 XBRL-backfilled margin quarters | **24 of 24** independently confirmed by `us-gaap:GrossProfit` |

Also checked: SEC XBRL `Revenues` FY2026 Q2 = 13,369,000,000 exactly matches the "Total" line on
the 10-Q face; `px_steel_hrc` FY2026 Q3 recomputed from the BLS API rather than FRED reproduces
the CSV value to 3e-5.

The one real discrepancy found: SEC XBRL carries **two** values for FY2017 Q1–Q3 cost of sales
(e.g. FY2017 Q2: 5,444.7 and 5,427.7). This is Deere's ASU 2017-07 restatement moving
non-service pension cost out of cost of sales. The corpus as-filed figure is used for those
quarters and the affected rows carry a RESTATEMENT note. It shifts gross margin by roughly
0.2pp in FY2017 — small, but do not treat FY2017 as clean.

---

## 3. The steel → cost-of-sales lag

**Short answer: 2 quarters, partial r = +0.66 (HAC t = +7.4, n = 66) — but only once you
control for Deere's own pricing. The naive cross-correlation the brief asks for is unstable and
sign-flips between subsamples, and I am not reporting it as an answer.**

### 3.1 Setup

Levels are useless here: `px_steel_hrc` and Deere's gross margin both trend, and their level
correlation is +0.617 — that number measures a shared trend, not pass-through. Deere's margin is
also strongly seasonal (Q1 mean 24.04%, Q2 26.75%, a 2.7pp spread). So:

- target = **year-over-year change** in the log cost-of-sales ratio (COGS/net sales), which kills
  the seasonal without fitting a seasonal model on 70 points
- driver = **year-over-year log change** in the steel index, at lags k = 0…6 fiscal quarters
- YoY differences overlap → residuals are MA(3) by construction → all t-statistics are
  **Newey–West HAC with truncation 4**. The naive OLS t-stats were roughly double.

### 3.2 What the naive bivariate cross-correlation says (and why it is not the answer)

YoY change in gross margin (pp) vs YoY log steel, full sample n = 66:

| driver | L0 | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|---|
| `px_steel_hrc` | −0.075 | −0.080 | −0.061 | −0.004 | +0.101 | +0.253 | **+0.421** |
| `ppi_steel_mill_products` | −0.204 | −0.266 | −0.221 | −0.076 | +0.149 | +0.367 | **+0.533** |

The largest |r| is at lag 6 — **with the wrong sign**. Read literally it says a steel spike six
quarters ago makes Deere *more* profitable. And it does not survive splitting the sample:

| driver | FY2010 Q1–FY2017 Q4 | FY2018 Q1–FY2026 Q2 |
|---|---|---|
| `px_steel_hrc` | peak lag 4, r = **−0.618** | peak lag 6, r = **+0.649** |
| `ppi_steel_mill_products` | peak lag 4, r = **−0.605** | peak lag 6, r = **+0.720** |

Same series, same transform, opposite sign in the two halves. **A bivariate steel-vs-margin
cross-correlation on this data is not a stable estimate of anything and should not be put in a
model.** Reporting "lag 6, r = +0.53" would have been a fabricated finding.

The reason is straightforward: steel prices are procyclical with ag-equipment demand. A steel
spike arrives *with* a demand boom that lets Deere raise list prices, and Deere's realised
pricing follows several quarters later. The bivariate correlation is measuring the pricing
cycle, not the cost channel. `ppi_ag_machinery` (Deere's own output price) correlates +0.546
with margin at lag 3 — larger than anything steel manages unconditionally.

### 3.3 The controlled estimate

Isolate the cost channel by conditioning on the two things that also move the cost ratio:

```
Δ₄ log(COGS/net sales)_t = a + b·Δ₄ log(steel)_{t−k}
                             + c·Δ₄ log(PPI ag machinery)_t     [output price]
                             + d·Δ₄ log(net sales)_t            [volume / absorption]
```

Expected sign on b is **positive** (steel up → cost ratio up → margin down). Partial correlation
of steel with the cost ratio, conditional on price and volume, n = 66:

| driver | L0 | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|---|
| `ppi_steel_mill_products` | +0.495 | +0.641 | **+0.663** | +0.410 | −0.040 | −0.367 | −0.571 |
| `px_steel_hrc` | +0.531 | **+0.556** | +0.438 | +0.212 | −0.057 | −0.317 | −0.548 |
| `px_steel_cold_rolled` | +0.432 | +0.568 | **+0.595** | +0.432 | +0.045 | −0.251 | −0.416 |
| `px_steel_scrap` | +0.037 | +0.253 | +0.476 | **+0.520** | +0.490 | +0.286 | −0.061 |

HAC t on the steel coefficient at the peak: steel mill products **+7.36**, HRC **+3.65**,
cold rolled **+6.66**, scrap **+3.87**.

**Peak lag = 2 quarters.** The mass sits in lags 1–3 for every flat/long steel series; scrap
peaks one quarter later at 3, which is what you would expect from a series that sits further
upstream. Lags 5–6 turn negative — that is the pricing channel arriving, not a cost effect, so
the peak is taken over economically-admissible (positive) coefficients only.

### 3.4 Stability of the controlled estimate

| driver | full | FY2010–17 | FY2018–26 | excl. FY2021–22 |
|---|---|---|---|---|
| `ppi_steel_mill_products` | **2** (+0.663) | 3 (+0.703) | 1 (+0.777) | **2** (+0.527) |
| `px_steel_hrc` | 1 (+0.556) | 3 (+0.677) | 0 (+0.728) | **2** (+0.490) |
| `px_steel_cold_rolled` | 2 (+0.595) | 4 (+0.708) | 1 (+0.717) | 3 (+0.435) |
| `px_steel_scrap` | 3 (+0.520) | 4 (+0.700) | 2 (+0.712) | 4 (+0.587) |

Honest reading:

- The **sign is stable** — positive in every subsample, every series, at lags 0–3. That is the
  robust part, and it is the part the naive spec got wrong.
- The **exact peak lag is not stable**: it moves by 1–3 quarters between halves, consistently
  *shorter* in the recent half (0–2) than in the earlier half (3–4). Plausibly real — Deere's
  inventory turns have shortened and surcharge-linked steel contracts pass through faster now —
  but with 32–34 observations per half I cannot distinguish that from noise.
- Dropping FY2021–FY2022 (the steel spike, which is the single most informative episode in the
  sample) **keeps the peak at lag 2–3** and keeps partial r near +0.5. So this is not one
  episode driving everything.

**Use lag 2 as the point estimate, treat 1–3 as the credible band, and prefer a distributed lag
over a single lag if the model allows it.** A flat 0–3 quarter average of Δ₄ log steel is nearly
as correlated as the best single lag and is far more stable across subsamples.

### 3.5 Magnitude

At lag 2 with `ppi_steel_mill_products`, b = **+0.157**. A 10% YoY rise in the steel PPI raises
the cost-of-sales ratio by about 1.5% relative — from a 74.7% base that is **+1.1pp on the cost
ratio, i.e. −1.1pp on gross margin**, showing up two quarters later.

Sanity check on that elasticity: 0.157 implies steel-linked inputs behave like ~16% of COGS.
That is at the high end of any plausible direct steel share for Deere. The steel PPI is almost
certainly proxying broader industrial input inflation (freight, castings, components, energy all
move with it), so **treat b as a composite input-cost loading, not a pure steel bill-of-materials
coefficient.** If you also put freight or diesel in the model, expect b to shrink.

### 3.6 What this implies is already on the books

The lag-2 driver for the quarters being forecast is already observed:

| driver quarter | Δ₄ log steel mill products | feeds | implied gross-margin effect |
|---|---|---|---|
| FY2026 Q1 | +13.1% | **FY2026 Q3** | **−1.5pp** |
| FY2026 Q2 | +14.9% | **FY2026 Q4** | **−1.7pp** |

For context, FY2026 Q3 steel is running +14.1% YoY and scrap has accelerated to +10.9%, copper
+33.2%, freight +12.4%, while `ppi_ag_machinery` — the output-price side — is up only **+2.1%**.
Input costs are rising roughly seven times faster than Deere's realised pricing proxy. That
spread is the single most forecast-relevant number in this file. Deere's gross margin has
already printed YoY declines in each of the last five quarters (−5.3, −0.8, −4.2, −4.3, −4.5,
−2.1pp), which is consistent with it.

Do not read the −1.5pp as a margin forecast on its own. It is one term in a model that also
needs volume, mix, pricing and the FY2026 tariff environment.

---

## 4. Caveats

1. **`px_steel_hrc` is a PPI index in index units, and it is bars/plates/structural, not coil.**
   No keyless USD/ton HRC exists. See §1. This is the biggest single compromise in the file.
2. **`px_steel_hrc_sheet` ends FY2022 Q1 (period end 2022-01-30) on the fiscal basis, 2022-03-31
   on the calendar basis** — BLS discontinued the underlying index after Feb 2022. Quarters with
   only one of three monthly observations are dropped rather than published as a misleading
   "quarterly average". Absent afterwards, never zero.
3. **`idx_freight_drybulk` (IGREA) is a deviation-from-trend index. It goes negative and has no
   natural zero.** Do not log it.
4. **`px_rubber` is US cents per pound**, not dollars per ton. Every other price series is
   dollars.
5. **Every `_cq` series duplicates a fiscal-basis series** on calendar-quarter alignment. Using
   both double-counts.
6. **Gross margin is equipment-operations, not total-company.** Denominator is Net sales, not
   Net sales and revenues.
7. **Two provenance regimes in the Deere series.** FY2015 Q1 → FY2026 Q2 comes from the corpus
   filings (`source_type=filing`). FY2009 Q1 → FY2014 Q4 comes from SEC XBRL
   (`source_type=api`). Within the XBRL block, most Q4s have no tagged three-month
   `CostOfGoodsSold`, so cost of sales is reconstructed as net sales − `GrossProfit`; those rows
   say so in `notes`. All 24 are independently confirmed (validation F).
8. **FY2017 is affected by the ASU 2017-07 pension restatement** — two XBRL values exist. The
   as-filed corpus figure is used. Roughly 0.2pp on gross margin.
9. **Deere's fiscal calendar switched from calendar month-ends to a 52/53-week calendar around
   FY2017.** Month-bucketed averaging is correct to within a few days either way; a fiscal
   quarter is occasionally 14 weeks. Immaterial for quarterly averages of monthly data.
10. **FY2026 Q3 and Q4 period ends (2026-08-02, 2026-11-01) are projections** off the confirmed
    FY2026 Q2 end of 2026-05-03 on a 13-week cadence. Deere has not reported them.
11. **The FY2026 Q3 input-cost rows are real published data, not forecasts** — May/June/July 2026
    BLS and EIA releases. Where a monthly source only runs to June (the IMF commodity series),
    the FY2026 Q3 value is a two-month mean and the row says PARTIAL QUARTER in `notes`.
    One-month partials are dropped entirely rather than published.
12. **PPI indices are not seasonally adjusted** and are transaction-price indices, not spot
    prices. They lag spot by weeks and are smoothed by contract pricing. That smoothing is one
    reason the estimated lag should be read as a band, not a point.
13. **The lag estimate is conditional on the control set.** Unconditionally, steel's correlation
    with Deere's margin is near zero at short lags and perversely positive at long ones. If your
    model omits an output-price control, do not expect the lag-2 relationship to appear.
14. **n = 66 with overlapping YoY windows.** HAC-corrected, but the effective sample is closer to
    15–20 independent observations. Treat every correlation here as indicative, not precise.
15. **`ppi_ag_machinery` is an industry price index, not Deere's realised pricing.** It misses
    mix, discounting and the finance-subsidy channel Deere uses to move equipment.

---

## 5. Sources

- FRED CSV download (keyless): `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>` —
  worked for every series tried. The FRED **HTML** series pages return 403 to both curl and
  WebFetch, so series titles were verified against BLS instead.
- BLS `wp.series` metadata file and BLS **public API v1** (keyless) — used to verify every PPI
  series title and as the independent cross-check in validation A. This caught a real error:
  `WPU101707` is **cold** rolled, not hot rolled, despite being an obvious-looking pick for an
  HRC proxy.
- SEC EDGAR XBRL `companyfacts` for CIK 0000315189.
- The offline Deere corpus, `filings/*.md` — authoritative for everything it contains.
- **Blocked:** stooq.com CSV (JavaScript proof-of-work challenge, no data returned) and
  `download.bls.gov` for two of the bulk `wp.data.*` files (rate-limited; the API was used
  instead).

## 6. Note on the corpus metadata trap

`INDEX.md` labels `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` as
"Q3 2026". It is dated 2026-05-21, the same day as Q2 earnings, and is Q2 material. Nothing in
this build reads that file — the Deere figures come from the income-statement tables in the 10-Q
and 8-K filings, keyed on the period end printed on the face of the statement rather than on any
INDEX.md label — so the mislabelling cannot have propagated. The latest Deere period in the CSV
is 2026-05-03, FY2026 Q2.
