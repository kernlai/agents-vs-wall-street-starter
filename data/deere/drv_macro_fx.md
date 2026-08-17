# drv-macro-fx — Macro, rates and FX driver panel for Deere & Company (NYSE: DE)

**Data file:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/drv_macro_fx.csv`
**Build script:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/build_drv_macro_fx.py`
**Validation script:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/validate_drv_macro_fx.py`
**Validation log:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/validation_report_drv_macro_fx.txt`

Built 2026-08-16. 3,268 rows, 40 distinct `series_id`, no missing values encoded as zero.
All figures sourced by script from keyless public APIs — nothing in this file was transcribed by hand.

---

## 1. The one thing to read before using this file

**Every series is published on TWO calendars, and you must pick one deliberately.**

| suffix | grid | `fiscal_year` / `fiscal_quarter` mean | n periods |
|---|---|---|---|
| *(none)* | **Calendar** quarters (Jan–Mar, Apr–Jun, …) | calendar year, calendar quarter | 83 |
| `_dfq` | **Deere fiscal** quarters | Deere's own FY and FQ | 83 |

Deere's fiscal quarters do **not** line up with calendar quarters. Deere's FY2026 Q3 runs
**2026-05-04 → 2026-08-02**. A calendar-Q2 macro average (Apr–Jun) and a calendar-Q3 average
(Jul–Sep) each capture only part of it.

If you are regressing a Deere fiscal-quarter target — net sales, diluted EPS, PPA operating profit —
**use the `_dfq` series.** The unsuffixed calendar series are provided for joining to external
calendar-dated data and for sanity-checking against published macro commentary.

Mixing the two grids in one regression will silently mis-time every driver by roughly one month.

---

## 2. Series inventory

### Levels — the 12 requested series

| series_id | units | FRED id | aggregation | notes |
|---|---|---|---|---|
| `us_fed_funds_rate` | percent | `DFF` | period **average** of daily | effective fed funds |
| `us_10y_treasury` | percent | `DGS10` | period **average** of daily | 10y CMT yield |
| `us_cpi` | index | `CPIAUCSL` | period **average** of monthly | CPI-U all items, SA, 1982-84=100 |
| `us_gdp_growth` | percent | `A191RL1Q225SBEA` | **none** (already quarterly) | real GDP % chg, SAAR |
| `usd_index_dxy` | index | `DTWEXBGS` | period **average** of daily | **not ICE DXY** — see §5.1 |
| `fx_eur_usd` | ratio | `DEXUSEU` | period **average** of daily | **USD per 1 EUR** |
| `fx_usd_brl` | ratio | `DEXBZUS` | period **average** of daily | **BRL per 1 USD** |
| `fx_usd_inr` | ratio | `DEXINUS` | period **average** of daily | **INR per 1 USD** |
| `fx_usd_cad` | ratio | `DEXCAUS` | period **average** of daily | **CAD per 1 USD** |
| `us_housing_starts` | count | `HOUST` | period **average** of monthly | thousands of units, SAAR |
| `us_industrial_production` | index | `INDPRO` | period **average** of monthly | total IP, 2017=100, SA |
| `us_consumer_sentiment` | index | `UMCSENT` | period **average** of monthly | U. Michigan, 1966Q1=100 |

### Derived and additional series

| series_id | units | what it is |
|---|---|---|
| `fx_eur_usd_yoy`, `fx_usd_brl_yoy`, `fx_usd_inr_yoy`, `fx_usd_cad_yoy` | percent | YoY % change of the quarterly average FX level |
| `usd_index_dxy_yoy` | percent | YoY % change of the quarterly average dollar index |
| `us_cpi_yoy` | percent | YoY % change of the quarterly average CPI index = the inflation rate |
| `us_fed_funds_rate_qend`, `us_10y_treasury_qend` | percent | **period END**, not average — last daily observation in the window |

Each of the 20 series above also exists with a `_dfq` suffix on the Deere fiscal grid.
`20 × 2 = 40` series total.

**Sign convention warning.** `fx_eur_usd` is quoted **USD per EUR** (rises when the dollar weakens).
The other three are quoted **foreign currency per USD** (rise when the dollar *strengthens*).
`fx_eur_usd_yoy` therefore has the **opposite** sign relationship to dollar strength than
`fx_usd_brl_yoy` / `fx_usd_inr_yoy` / `fx_usd_cad_yoy`. Do not pool them without sign-correcting.

---

## 3. Why average vs period-end, and why it matters

The task asked for this choice to be recorded explicitly. Every row states its convention in `notes`.

- **Period average** is the default for everything. Deere's reported revenue and segment profit are
  flows accumulated across a quarter, and non-USD revenue is translated at rates approximating the
  average over the period. An average-rate driver is the like-for-like match to a flow target.
- **Period end** is provided *additionally* for the two policy/market rates
  (`*_qend`). John Deere Capital's balance sheet reprices off the rate level prevailing at the
  reporting date, and the spot level at quarter end is the better predictor of the *next* quarter's
  net interest margin than the average of the quarter just gone. Use `_qend` for balance-sheet and
  NIM-flavoured questions; use the average for income-statement flows.

For monthly and quarterly source series mapped onto Deere's fiscal windows (which straddle calendar
month boundaries), the value is a **day-overlap-weighted mean**: each monthly observation is treated
as covering its whole calendar month, and months are weighted by how many days they contribute to
the fiscal window. This is an interpolation, not an observation — flagged in `notes` on every row.

**YoY series** are computed on the aggregated quarterly averages as
`(level_t / level_{t-4} - 1) × 100`, comparing the same fiscal quarter one year earlier.
The two levels used are printed in the `notes` of every YoY row so the arithmetic is auditable.

---

## 4. The Deere fiscal calendar used

Fiscal windows were **derived programmatically**, not typed in. Source: SEC XBRL
`companyconcept/CIK0000315189/us-gaap/EarningsPerShareDiluted`, taking every tagged ~91-day duration,
assigning each to its own fiscal year by end date, and deriving Q4 as the gap between Q3 end and the
next year's Q1 start.

Audit result: **83 quarters, zero gaps, zero overlaps, all lengths 84–98 days.**

Recent windows:

| FY | FQ | start | end | days |
|---|---|---|---|---|
| FY2025 | Q1 | 2024-10-28 | 2025-01-26 | 91 |
| FY2025 | Q2 | 2025-01-27 | 2025-04-27 | 91 |
| FY2025 | Q3 | 2025-04-28 | 2025-07-27 | 91 |
| FY2025 | Q4 | 2025-07-28 | 2025-11-02 | 98 (53-week year) |
| FY2026 | Q1 | 2025-11-03 | 2026-02-01 | 91 |
| FY2026 | Q2 | 2026-02-02 | 2026-05-03 | 91 |
| FY2026 | Q3 | 2026-05-04 | 2026-08-02 | 91 — **PROJECTED, see §5.3** |

Three fiscal-calendar caveats a modeller must know:

1. **FY2006–FY2008 windows are INFERRED** (140 rows). SEC XBRL does not reach back that far.
   They are set to calendar month-end quarters (Jan 31 / Apr 30 / Jul 31 / Oct 31), which is the
   convention visible in every XBRL-tagged Deere period through FY2016. Rows carry
   `fiscal window INFERRED` in `notes`.
2. **Deere changed fiscal calendars in FY2017**, from calendar month-ends to a 52/53-week calendar.
   XBRL therefore contains *two competing* sets of FY2016 boundaries — as-reported (Q2 ends
   2016-04-30) and as-restated-in-FY2017-comparatives (Q2 ends 2016-05-01). The build deterministically
   prefers **as-originally-reported**. A one-day seam remains at the FY2016 Q4 / FY2017 Q1 join
   (FY2016 Q4 ends 2016-10-30; as-reported FY2016 ended 2016-10-31). This is an artefact of the
   calendar transition itself, not an error, and its effect on a quarterly average is negligible.
3. **FY2025 Q4 is 98 days** — FY2025 was a 53-week year. Flow-like drivers are averages so they are
   not distorted, but any level-vs-flow comparison across that quarter should account for it.

---

## 5. Caveats, limitations and things that are NOT what they look like

### 5.1 `usd_index_dxy` is not the DXY
The series is FRED `DTWEXBGS`, the **Federal Reserve Nominal Broad U.S. Dollar Index** (Jan 2006 = 100),
trade-weighted across ~26 economies. It is **not** the ICE U.S. Dollar Index (DXY), which is a fixed
basket of six developed-market currencies. They differ materially in level, in volatility, and
especially in emerging-market sensitivity — which is precisely the exposure that matters for Deere's
Brazil and India business. The `series_id` was kept as specified in the task brief, but the underlying
series is the Fed broad index. Do not compare its level to a quoted DXY print.

`DTWEXBGS` begins **2006-01-02**, which is what sets the panel's start date. There is no earlier
history for this index; the predecessor major-currencies index `DTWEXM` was discontinued in 2020 and
is not spliced in (splicing two differently-weighted indices would create a structural break).

### 5.2 Partial periods — 15 rows
A period is flagged `PARTIAL PERIOD` in `notes` only when the **source series stops inside the
window**. Weekend and holiday gaps in daily series are *not* partiality — a quarter of business-day
quotes is a complete quarter. (An earlier build conflated the two and false-flagged 983 rows; fixed.)

The 15 genuinely partial rows are all at the data frontier:

- **Calendar 2026 Q3** (`period_end` 2026-09-30) — quarter still in progress. 10 rows.
- **Deere FY2026 Q3** (`period_end` 2026-08-02) — 5 rows, all from *monthly/quarterly* sources whose
  latest observation predates 2026-08-02: `us_cpi_dfq`, `us_gdp_growth_dfq`, `us_housing_starts_dfq`,
  `us_industrial_production_dfq`, `us_consumer_sentiment_dfq`.

**Important and useful:** every *daily* driver — all four FX pairs, the dollar index, fed funds and
the 10-year — is **complete** through Deere's FY2026 Q3 window. The FX and rates inputs to a FY2026 Q3
forecast are fully observed, not estimated. Only the slower macro aggregates are incomplete, and
`us_gdp_growth_dfq` for that quarter is effectively carrying calendar-2026-Q2 GDP forward across the
64% of the window it covers, since Q3 GDP does not exist yet.

Rows below 25% window coverage are omitted entirely rather than published thin.

### 5.3 FY2026 Q3 window is projected, not confirmed
Deere has not reported FY2026 Q3 as of 2026-08-16, so its exact period end is not in any filing.
The window `2026-05-04 → 2026-08-02` is a 13-week roll forward from the confirmed Q2 end of
2026-05-03, consistent with Deere's 52/53-week calendar. It matches the task brief's stated
approximate end date. All 14 affected rows carry `fiscal window PROJECTED` in `notes`.
If the actual reported period end differs by a few days, quarterly *averages* will shift only
marginally — but re-run the build once the 10-Q lands.

### 5.4 Series NOT independently validated
Four series rest on a single source with no keyless independent cross-check available:
`usd_index_dxy` (Fed G.5/H.10), `us_housing_starts` (Census/HUD), `us_industrial_production`
(Fed G.17), `us_consumer_sentiment` (University of Michigan). Each is the sole official publisher of
its own statistic, so "independent" confirmation does not really exist for them. They were
plausibility-checked against known historical episodes (e.g. housing starts ≈ 524k in 2009 Q1;
sentiment ≈ 57.7 in 2008 Q4) and passed.

### 5.5 Revisions
`us_cpi`, `us_gdp_growth`, `us_industrial_production` and `us_housing_starts` are all **revised** after
first publication, and several are seasonally adjusted with periodically re-estimated factors. This
file is a **current-vintage** snapshot as of 2026-08-16 — it is *not* point-in-time. Values for past
quarters are what BEA/BLS/Fed/Census say *today*, not what was known to the market when Deere reported
that quarter. For a genuine backtest of forecast skill this introduces look-ahead bias. Real-time
vintages would require ALFRED/FRED-MD, which was out of scope here.

FX and interest-rate series are **not** revised, so `fx_*`, `us_fed_funds_rate`, `us_10y_treasury` and
`usd_index_dxy` are free of this problem.

### 5.6 Fixing conventions differ slightly between sources
FRED's H.10 FX rates are noon-New-York fixings; the ECB reference rates used for validation are
14:15 CET. This produces an irreducible ~0.05–0.35% difference on quarterly averages. It is a
time-of-day artefact, not an error in either source, and it bounds how precisely any FX figure here
should be read.

### 5.7 Blocked source
**stooq.com CSV endpoints are unusable** — they now sit behind a JavaScript proof-of-work bot
challenge that returns an HTML interstitial instead of CSV. This was not circumvented. All FX
validation was rerouted to central-bank primary sources (ECB, Bank of Canada, Banco Central do
Brasil), which are better sources anyway.

---

## 6. Validation

Nine cross-checks. Each recomputes a series from a source **other than FRED** and compares quarterly
values across the shared history. Full log in `validation_report_drv_macro_fx.txt`.

| # | series | independent source | n | mean abs diff | max abs diff | verdict |
|---|---|---|---|---|---|---|
| 1 | `fx_eur_usd` | ECB Data Portal reference rate USD/EUR | 82 | 0.0599% | 0.2541% | **AGREE** |
| 2 | `fx_usd_inr` | ECB cross (INR/EUR) ÷ (USD/EUR) | 82 | 0.0714% | 0.3444% | **AGREE** |
| 3 | `fx_usd_cad` | Bank of Canada Valet `FXUSDCAD` | 38 | 0.0230% | 0.0759% | **AGREE** |
| 4 | `fx_usd_brl` | Banco Central do Brasil SGS series 1 (PTAX sell) | 82 | 0.0840% | 0.2832% | **AGREE** |
| 5 | `us_cpi` | BLS bulk file `cu.data.0.Current`, `CUSR0000SA0` | 82 | 0.0017% | 0.0091% | **AGREE** |
| 6 | `us_fed_funds_rate` | FRED `FEDFUNDS` monthly, re-aggregated | 82 | 0.0016pp | 0.0071pp | **AGREE** |
| 7 | `us_10y_treasury` | FRED `GS10` monthly, re-aggregated | 82 | 0.0039pp | 0.0192pp | **AGREE** |
| 8 | `us_gdp_growth` | rebuilt from `GDPC1` level: ((L_t/L_t-1)^4−1)×100 | 81 | 0.0251pp | 0.0521pp | **AGREE** |
| 9 | Deere fiscal calendar | offline filing corpus (311 docs) | 6/6 | — | — | **AGREE** |

**No discrepancy survived investigation.** Notes on the individual results:

- **Checks 1–4 (FX).** Residual differences of 0.02–0.34% are the noon-NY vs 14:15-CET fixing
  difference described in §5.6, not extraction error. Check 3 has n=38 because Bank of Canada's
  `FXUSDCAD` series begins in 2017 after a methodology change; the pre-2017 legacy series is a
  different construct and was not spliced.
- **Checks 6–7 (rates)** are measured in **absolute percentage points**, not relative %. A relative
  metric is meaningless at the zero lower bound: a 0.003pp gap on a 0.077% ZIRP-era policy rate reads
  as a 3.9% "discrepancy" while being economically nil. The first run of this validator made exactly
  that mistake and false-flagged fed funds; the metric was corrected. The tiny residual is expected —
  a day-weighted average of daily rates is not identical to the unweighted mean of three monthly
  averages, because months differ in length. That is the aggregation-convention question the task
  asked to be documented, and 0.007pp is its full magnitude.
- **Check 8 (GDP)** also validates the **quarter mapping**. FRED dates quarterly observations at the
  quarter *start*; an off-by-one would shift every GDP observation by a full quarter and would show
  up here as a large mismatch. It does not. The residual ≤0.052pp is BEA's rounding of the published
  growth rate to one decimal.
- **Check 9** confirms the SEC-XBRL-derived fiscal calendar against a completely separate artefact —
  the offline filing corpus. All six recent period-end dates (2025-01-26, 2025-04-27, 2025-07-27,
  2025-11-02, 2026-02-01, 2026-05-03) appear as literal text in 2–9 corpus documents each.

Structural QA on the CSV also passed: exact required header, 3,268 rows, zero duplicate
`(series_id, period_end)` keys, zero literal-zero values, zero blank values, all `period_end` values
parse as ISO dates, all `fiscal_quarter` values in `{Q1,Q2,Q3,Q4}`. Eight independent plausibility
spot-checks against known historical episodes all landed in range.

---

## 7. Reproducing

```bash
python3 /Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/build_drv_macro_fx.py
python3 /Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/validate_drv_macro_fx.py
```

Standard library only, no API keys. Both scripts cache raw downloads in
`scripts/data/.cache_macro_fx/` — delete that directory to force a clean refetch. The build is
deterministic given the same cache.

**Sources used:** FRED CSV (`fred.stlouisfed.org/graph/fredgraph.csv`), SEC EDGAR XBRL companyconcept
API, ECB Data Portal (`data-api.ecb.europa.eu`), Bank of Canada Valet API, Banco Central do Brasil
SGS API, BLS bulk time-series files, and the offline Deere filing corpus.
