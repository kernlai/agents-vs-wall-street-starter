# Deere (DE) driver dataset — agricultural commodity prices & crop input costs

**File:** `data/deere/drv_ag_commodities.csv`
**Builder:** `scripts/data/build_drv_ag_commodities.py` (stdlib-only Python, fully re-runnable)
**Built:** 2026-08-16
**Rows:** 8,454 · **Series:** 104 (26 base series × 4 variants) · **Span:** 2006-01-31 → 2026-08-02

Crop prices drive farm cash income, which drives equipment demand. This file is the
commodity-price and input-cost driver block. It contains **no Deere financials** — no
segment data, so the PPA / legacy-Agriculture-&-Turf segment discontinuity does not
arise here. It does, however, respect Deere's fiscal calendar (see below).

---

## 1. Series naming

Every series follows `<base>_<stat>_<calendar>`:

| part | values | meaning |
|---|---|---|
| `<stat>` | `avg` | quarterly **average** |
| | `qe` | quarterly **quarter-end** reading |
| `<calendar>` | `_cq` | **calendar** quarter (Mar/Jun/Sep/Dec ends) |
| | `_fq` | **Deere fiscal** quarter |

So `px_corn_avg_fq` = corn, quarterly average, Deere fiscal quarters.
All four variants exist for all 26 base series.

**`fiscal_year` / `fiscal_quarter` semantics differ by calendar suffix:**

- `_cq` rows: `fiscal_year` = **calendar** year, `fiscal_quarter` = calendar quarter.
- `_fq` rows: `fiscal_year` = **Deere fiscal year**, `fiscal_quarter` = Deere's quarter.

`_cq` and `_fq` rows never collide on `period_end`, so `(series_id, period_end)` is a
unique key (verified: 0 duplicates).

---

## 2. Series inventory

### Primary crop prices — IMF via FRED (the headline series)

| base series | units | variants | n | coverage |
|---|---|---|---|---|
| `px_corn` | USD/bushel | 4 | 82–83 | 2006-01-31..2026-08-02 |
| `px_soybean` | USD/bushel | 4 | 82–83 | 2006-01-31..2026-08-02 |
| `px_wheat` | USD/bushel | 4 | 82–83 | 2006-01-31..2026-08-02 |
| `px_cotton` | USD/lb | 4 | 82–83 | 2006-01-31..2026-08-02 |
| `px_sugar` | USD/lb | 4 | 82 | 2006-01-31..2026-06-30 |

Exact quote definitions (confirmed, not assumed):

- **corn** `PMAIZMTUSDM` — US No.2 Yellow, prompt shipment, **FOB US Gulf**.
- **soybean** `PSOYBUSDM` — US soybeans, **CBOT nearest forward**, No.2 yellow and par.
- **wheat** `PWHEAMTUSDM` — US No.1 Hard Red Winter, ordinary protein, **Kansas City**
  (an *interior rail-terminal* quote, **not** a Gulf export price — this matters, see §5).
- **cotton** `PCOTTINDUSDM` — Cotlook A Index, US cents/lb → USD/lb.
- **sugar** `PSUGAISAUSDM` — ISA daily price, raw, world, US cents/lb → USD/lb.

### Crop input costs — World Bank Pink Sheet (USD/mt price *levels*)

| base series | units | n | coverage |
|---|---|---|---|
| `px_urea` | USD/mt | 80 | 2006-01-31..2025-12-31 |
| `px_potash` | USD/mt | 80 | 2006-01-31..2025-12-31 |
| `px_dap` | USD/mt | 80 | 2006-01-31..2025-12-31 |
| `px_tsp` | USD/mt | 80 | 2006-01-31..2025-12-31 |
| `px_phosphate_rock` | USD/mt | 79–80 | 2006-01-31..2025-12-31 |

### Crop input costs — energy (full coverage through FY2026 Q3)

| base series | units | n | coverage |
|---|---|---|---|
| `px_diesel_retail_us` | USD/gallon | 82–83 | 2006-01-31..2026-08-02 |
| `px_wti_crude` | USD/barrel | 82–83 | 2006-01-31..2026-08-02 |

### BLS PPI indices (index units — full coverage through FY2026 Q3)

`ppi_corn`, `ppi_soybean`, `ppi_wheat_hrw`, `ppi_wheat_all`, `ppi_cotton_raw`,
`ppi_fertilizer_materials`, `ppi_nitrogenous_fertilizer_mfg`, `ppi_diesel_no2`
— all 4 variants, n=82–83, 2006-01-31..2026-08-02.

These publish ~6 weeks faster than the IMF and World Bank series and are the reason
FY2026 Q3 is populated at all. **They are indices, not price levels** — do not mix
them into a regressor with a USD/bushel series.

### Cross-check duplicates — World Bank Pink Sheet

`px_corn_wb`, `px_soybean_wb`, `px_wheat_hrw_wb`, `px_wheat_srw_wb`, `px_cotton_wb`,
`px_sugar_wb` — n=76–80, ending 2025-12-31. Present so a modeller can audit the
primary series; **not intended as model inputs alongside their IMF twins** (collinear).

---

## 3. Aggregation method

Deere fiscal quarters start and end mid-month (FY2026 Q2 = 2026-02-02..2026-05-03), so
whole-calendar-month aggregation would be wrong. Both aggregations therefore use:

- **`avg` from a monthly source** — *day-weighted mean*: every calendar day in the
  quarter window carries its month's value, then average over the window. A month
  contributes in proportion to how many of its days fall inside the quarter. Each row's
  `notes` records the realised **day coverage**; rows below 0.95 coverage are **omitted
  entirely** rather than emitted partial.
- **`qe` from a monthly source** — the value of the **last calendar month with ≥15 days
  inside the quarter window**. This is a *proxy*: it is a monthly average, **not a spot
  close** on the quarter-end date. Chosen over "the month containing the end date"
  because a quarter ending 2026-05-03 barely touches May.
- **`avg` from daily/weekly sources** (`px_wti_crude`, `px_diesel_retail_us`) — simple
  mean of observations dated inside the window; minimum 40 (daily) / 8 (weekly) obs.
- **`qe` from daily/weekly sources** — the genuine last observation on or before the
  quarter end (within 14 days). These are true quarter-end reads.

---

## 4. Deere fiscal calendar

Quarter boundaries came from the **SEC EDGAR XBRL** API
(`companyconcept/CIK0000315189/us-gaap/Revenues.json`), extracting distinct ~91-day and
~364-day `(start, end)` periods, then **cross-checked against the offline filings corpus**
by grepping `"Three Months Ended <date>"`. The two agree on every overlapping date.

Two regimes:

- **Through FY2016** — calendar month-ends (Jan 31 / Apr 30 / Jul 31 / Oct 31).
- **FY2017 onward** — a 52/53-week fiscal calendar ending the Sunday nearest 31 October,
  so quarter-ends drift (FY2024 Q4 ended 2024-10-27; FY2025 Q4 ended 2025-11-02).

Caveats:

- **FY2006 is inferred.** It predates EDGAR XBRL coverage, so the pre-FY2017
  calendar-month-end rule was applied. Every affected row says so in `notes`.
- **FY2016 restatement.** When Deere adopted the 52/53-week calendar it restated FY2016
  comparatives (e.g. Q2 shown as ending 2016-05-01 rather than 2016-04-30). This file
  uses the **as-originally-reported** month-end dates. Maximum discrepancy is one day —
  immaterial for a monthly-sourced commodity average, but noted for completeness.
- **FY2026 Q3 (`period_end` 2026-08-02) is a scheduled period end. Deere has NOT
  reported that quarter as of 2026-08-16.** These rows are *driver data only*; no Deere
  actuals exist for them. Every such row carries that warning in `notes`.
- FY2026 Q4 is not in the file — its end date is not yet determinable.

---

## 5. Validation

Cross-checks run automatically at the end of every build (see `validate()` in the script;
raw output also written to the scratchpad as `validation.txt`).

### Two-publisher agreement on identical quotes

| pair | n | corr | mean abs % diff | verdict |
|---|---|---|---|---|
| corn: IMF vs World Bank | 80 | **+0.9999** | **0.14 %** | agree — same quote |
| cotton: IMF vs World Bank | 80 | **+0.9989** | **0.23 %** | agree — same quote |
| sugar: IMF vs World Bank | 80 | **+0.9944** | **2.00 %** | agree — same quote |

Corn agreeing to 0.14 % across two independent publishers is the strongest evidence
that the USD/mt → USD/bushel conversion and the quarterly aggregation are both correct.

### Discrepancies — investigated, explained, NOT silently resolved

| pair | n | corr | mean abs % diff | finding |
|---|---|---|---|---|
| wheat: IMF vs WB HRW | 80 | +0.9745 | **16.88 %** | **Different delivery points.** IMF = Kansas City *interior*; World Bank = *US Gulf FOB export*. The wedge is the rail freight from the plains to the Gulf, and it widened from ~12 % (2006-10) to ~32 % (2025) as rail rates rose. Both series hold a comparably stable ratio to the BLS HRW-wheat PPI (cv 0.052 vs 0.056, versus 0.055 for the corn control), so **neither is broken** — they are genuinely different quotes. **Do not splice them.** |
| soybeans: IMF vs WB | 80 | +0.9761 | **12.88 %** | **World Bank changed the definition three times.** Its own Description sheet states: from Jan-2025 FOB US Gulf; Jan-2021–Dec-2024 CIF Rotterdam; **Dec-2007–Dec-2020 US No.2 yellow *meal*, CIF Rotterdam** (soybean *meal*, not whole beans); earlier, US origin nearest forward. `px_soybean_wb` is therefore **not** a like-for-like check on `px_soybean` before 2025. Use `px_soybean` (IMF, definitionally stable). |

### Unit-conversion round-trips (all pass)

Five conversions were recomputed from the raw endpoint values and matched to <1e-4:
corn, soybean, wheat (USD/mt ÷ bushels-per-tonne) and cotton, sugar (US cents/lb ÷ 100).
The FY2026 Q3 corn nowcast and its day-weighted quarterly average were also
independently recomputed from a clean second script and reproduced the pipeline value.

### Correlation-only checks (different units, sanity direction)

corn price vs corn PPI **+0.9919**; retail diesel vs diesel PPI **+0.9683**;
urea USD/mt vs nitrogenous-fertiliser PPI **+0.8518**.

---

## 6. The FY2026 Q3 nowcast — read this before modelling

Deere's FY2026 Q3 window is **2026-05-04 .. 2026-08-02**. The IMF monthly commodity
series stop at **June 2026**, which would have left the single most decision-relevant
quarter in the file empty.

Rather than drop it or guess, July 2026 was **index-spliced**: the last observed monthly
price is carried forward by the month-over-month ratio of the matched BLS PPI index,
which *is* published through July 2026.

```
price_July2026 = price_June2026 × (PPI_July2026 / PPI_June2026)
```

| series | index used | BLS series (title verified against `wp.series`) |
|---|---|---|
| `px_corn` | corn PPI | `WPU01220205` Farm products — Corn |
| `px_soybean` | soybean PPI | `WPU01830131` Farm products — Soybeans |
| `px_wheat` | HRW wheat PPI | `WPU01210101` Farm products — Hard red winter wheat |
| `px_cotton` | raw cotton PPI | `WPU0151` Farm products — Raw cotton |

**`px_sugar` is deliberately NOT nowcast** — US raw sugar is price-supported and
decoupled from the world ISA price, so a US PPI would be an invalid bridge. Sugar simply
ends at 2026-06-30.

Consequences a modeller must respect:

- Exactly **8 rows** in the file are affected. All carry `source_type = estimate` and a
  `CONTAINS NOWCAST` note naming the spliced month. **Filter on
  `source_type == 'estimate'` to find or exclude every one of them.**
- The FY2026 Q3 averages are still ~2/3 observed data (May and June are actual; only
  July is spliced; day coverage 0.98).
- The FY2026 Q3 `qe` values rest **entirely** on the spliced July figure — they are the
  weakest numbers in the file.
- August 2026 was **not** extrapolated (no August PPI exists), so the FY2026 Q3 window is
  averaged over 89 of its 91 days.

---

## 7. What could not be obtained

- **USDA NASS QuickStats** (US season-average and monthly prices received, in USD/bushel
  natively) — the API returned `{"error":["unauthorized"]}`. It requires an API key that
  is not available in this environment. **This is the main gap:** all USD/bushel figures
  here are *derived* from USD/metric-ton export/terminal quotes via standard bushel test
  weights, not USDA farm-gate prices received. Export/terminal quotes sit **above**
  farm-gate prices by the local basis. If you need the price a farmer actually received
  (arguably the truer driver of equipment demand), an NASS key is required.
- **stooq.com CSV** (would have given daily futures, hence true quarter-end closes and
  exact fiscal-quarter alignment) — the endpoint is behind a JavaScript proof-of-work bot
  check. Circumventing bot detection was out of bounds, so it was not used. **This is why
  every `qe` value from a monthly source is a proxy rather than a spot close.**
- **FRED series metadata endpoints** (`/data/<ID>.txt`, `/series/<ID>`) returned empty or
  HTTP 403. Series identities were instead confirmed from the **BLS flat file**
  `https://download.bls.gov/pub/time.series/wp/wp.series` (`series_title` field) for all
  PPI series, and from IMF documentation for the IMF quotes. No series identity in this
  file is a guess.
- **World Bank Pink Sheet vintage** — the January 2026 release, with data through
  **December 2025**. All fertiliser levels therefore stop at 2025-12-31 and there is **no
  USD/mt fertiliser price for calendar 2026 or for Deere FY2026 Q1–Q3**. Use
  `ppi_fertilizer_materials` / `ppi_nitrogenous_fertilizer_mfg` (index units, current
  through July 2026) to cover the gap.

---

## 8. Caveats summary

1. **USD/bushel here is derived, not native.** USD/mt ÷ bushels-per-tonne, using US test
   weights: corn 56 lb/bu (39.36825 bu/mt), soybeans and wheat 60 lb/bu (36.74371 bu/mt).
   These are export/terminal quotes, **above** farm-gate prices received by the basis.
2. **`px_wheat` is a Kansas City interior quote**, not a Gulf export price. It is
   12–32 % below `px_wheat_hrw_wb`, and the gap widens over the sample. Pick one; never
   splice.
3. **`px_potash` has a definition break at 2020-01** (FOB Vancouver → Brazil CFR
   granular). CFR embeds freight; there is a level shift at that date that is **not** a
   market move.
4. **`px_urea` has a definition break at 2022-03** (FOB Black Sea → FOB Middle East),
   which coincides with the Russia/Ukraine nitrogen shock — **the definition break and a
   real price spike are confounded** and cannot be separated from this data alone.
5. **`px_soybean_wb` is a soybean *meal* quote from Dec-2007 to Dec-2020.** Do not use it
   as a bean price over that stretch.
6. **`px_wheat_hrw_wb` has a definition break around June-2020** (No.1 → No.2 HRW).
7. **`qe` from monthly sources is a monthly average, not a spot close.** Only
   `px_wti_crude_qe_*` and `px_diesel_retail_us_qe_*` are true quarter-end reads.
8. **`ppi_*` series are indices** (mostly 1982=100), not price levels. Never place them
   in the same regressor as a USD series without transforming.
9. **FY2006 fiscal dates are inferred** from the pre-FY2017 rule.
10. **FY2026 Q3 rows are driver data for an unreported quarter.** Deere has not reported
    it as of 2026-08-16.
11. **Nominal USD throughout.** Nothing is deflated or seasonally adjusted; the PPI
    series are explicitly NSA. Crop prices are strongly seasonal — deseasonalise before
    fitting.
12. **Missing data is an absent row.** There are zero blank values and zero zero-values
    in the file; a zero would be a real zero, and none occur.

---

## 9. Reproducing

```bash
python3 scripts/data/build_drv_ag_commodities.py
```

Network sources are cached to the scratchpad on first fetch; delete the cache to force a
refresh. The script re-runs the full validation suite and prints it to stderr on every
build. All sources are keyless.
