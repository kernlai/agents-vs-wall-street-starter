# drv_farm_economy — US, South American and EU farm-economy drivers for Deere (DE)

**Build date:** 2026-08-16 · **Rows:** 1,432 · **Series:** 75 · **Coverage:** 2006-01-01 → 2026-12-31
**Data file:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/drv_farm_economy.csv`
**Build script:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/build_drv_farm_economy.py`
(standard library only; `python3 scripts/data/build_drv_farm_economy.py` reproduces the CSV byte-for-byte
from a cache at `~/.cache/avws-farm-economy`, re-downloading anything missing)

Every number in the CSV was extracted by that script. Nothing was transcribed by hand.

---

## 1. What is in here

All eight series named in the task brief are present for the full 20 years, plus 67 supporting series.

| Requested series | series_id | Units | Coverage | n |
|---|---|---|---|---|
| US net farm income | `us_net_farm_income` | USD billions | 2006–2026 | 21 |
| US net cash farm income | `us_net_cash_farm_income` | USD billions | 2006–2026 | 21 |
| US crop cash receipts | `us_crop_cash_receipts` | USD billions | 2006–2026 | 21 |
| Farm debt-to-asset ratio | `us_farm_debt_to_asset_ratio` | percent | 2006–2026 | 21 |
| Farmland values | `us_farmland_values` | USD/acre | 2006–2026 | 21 |
| Corn planted acres | `us_planted_acres_corn` | million acres | 2006–2026 | 21 |
| Soybean planted acres | `us_planted_acres_soybean` | million acres | 2006–2025 | 20 |
| Government farm payments | `us_govt_farm_payments` | USD billions | 2006–2026 | 21 |

**Supporting US series (USDA ERS, 2006–2026 unless noted):**
`us_total_cash_receipts`, `us_livestock_cash_receipts`, `us_corn_cash_receipts`,
`us_soybean_cash_receipts` (2008–), `us_gross_cash_farm_income`, `us_farm_production_expenses`,
`us_farm_interest_expense`, `us_farm_fertilizer_expense`, `us_farm_assets_total`,
`us_farm_debt_total`, `us_farm_equity_total`, `us_farm_real_estate_assets`,
`us_farm_working_capital` (2009–), `us_farm_rate_of_return_assets`,
`us_govt_adhoc_emergency_payments`.

**Deere-specific supporting series — farm machinery capex.** These are the closest public
proxy for Deere's addressable US market and are worth more than most of the macro series:
`us_farm_capital_expenditures`, `us_farm_capex_vehicles_machinery` (2006–2026),
`us_farm_capex_tractors` and `us_farm_capex_other_machinery` (2006–2024; ERS does not forecast
the components, only the aggregate).

**Other US:** `us_cropland_values`, `us_pasture_values`, `us_harvested_acres_corn`,
`us_harvested_acres_soybean`, `us_corn_price_received`, `us_soybean_price_received`,
`us_farm_proprietors_income_bea` (annual) and **`us_farm_proprietors_income_bea_q` (quarterly,
82 obs, 2006Q1–2026Q2)** — the only *quarterly* farm-income indicator in the file.

**USDA forecast vintages** (see §4): `us_net_farm_income_fcst_v2024_02`,
`…_v2025_02`, `…_v2025_09`, `…_v2026_02` and the matching `us_net_cash_farm_income_fcst_*`.

**South America / EU:** `br_*` and `ar_*` soybean and corn area harvested + production
(2006–2026, USDA FAS PSD), agriculture value added in USD and as % of GDP, World Bank crop
production index, `brl_usd_fx_rate`, and for the EU `eu_ag_entrepreneurial_income`,
`eu_ag_factor_income`, `eu_ag_output` (Eurostat, 2006–2025) plus `eu_*` PSD and World Bank rows.

---

## 2. Sources

| # | Source | Access | Used for |
|---|---|---|---|
| 1 | USDA ERS **Farm Income and Wealth Statistics**, bulk CSV, 4 release vintages (Feb-2024, Feb-2025, Sep-2025, **Feb-2026**) | keyless HTTP zip | all US income / balance-sheet / capex series |
| 2 | USDA NASS **Land Values** annual summaries, 12 PDFs 2010–2026 | keyless HTTP PDF → `pdftotext -layout` → parser | farmland, cropland, pasture $/acre |
| 3 | USDA ERS **Feed Grains Yearbook** (all-years CSV) | keyless | corn planted/harvested acres, corn price |
| 4 | USDA ERS **Oil Crops Yearbook** (all-tables CSV) | keyless | soybean planted/harvested acres, soybean price |
| 5 | USDA FAS **PSD Online** bulk CSV (grains, oilseeds), Aug-2026 vintage | keyless zip | BR / AR / EU / US area and production |
| 6 | **World Bank** indicators API | keyless | ag value added, crop production index |
| 7 | **Eurostat** `aact_eaa01` dissemination API | keyless | EU agricultural income and output |
| 8 | **FRED** CSV (`B042RC1A027NBEA`, `B042RC1Q027SBEA`, `DEXBZUS`) | keyless | BEA farm proprietors' income (independent cross-check), BRL |
| 9 | **Offline Deere corpus** — Q1 FY2026 earnings call, 2026-02-19 | local | validation of the 2026 USDA forecast figures |

Endpoints that did **not** work and what I did instead:

* **USDA NASS Quick Stats API** returns `{"error":["unauthorized"]}` without a registered key.
  Acreage therefore comes from the ERS Feed Grains / Oil Crops yearbooks (which republish the
  same NASS estimates) and land values from the NASS PDF summaries.
* **USDA ESMIS / Cornell** (`usda.library.cornell.edu`, `esmis.nal.usda.gov`) — the old catalog
  and JSON API now return 404/410. Land Values PDFs were pulled from
  `nass.usda.gov/Publications/Todays_Reports/reports/` directly. The **August-2013 through
  August-2016 and August-2023 summaries are no longer hosted there** (404); coverage is
  unaffected because each summary carries a 15-year trend chart.
* **ERS "Farmland Value" topic page** carries only 1950s–1990s spreadsheets; not useful.
* No keyless Argentine peso FX series was found on FRED, so `ar` has no FX row.

---

## 3. Conventions a modeller must know

* **Header is exactly** `series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes`.
* **`fiscal_year` is the CALENDAR year** for every row in this file — these are external drivers,
  not Deere fiscal periods. **Deere's fiscal year ends late Oct / early Nov**, so Deere FY(n)
  spans roughly calendar Nov(n-1)…Oct(n). Deere FY2026 Q3 ended **2026-08-02**. Do not join
  `fiscal_year` in this file to Deere's `fiscal_year` without an explicit offset.
* **Annual rows use `fiscal_quarter=FY` and `period_end = YYYY-12-31`**, even when the real
  reference date differs. The true reference date is always in `notes`:
  * NASS land values are surveyed **as of June 1** and published late July / early August.
    (Through the 2010 summary the reference date was January 1 — a genuine definition change.)
  * ERS balance-sheet items are **Dec-31** values; income items are calendar-year flows.
  * Corn/soybean acreage is labelled by the **planting year** (corn marketing year Sep–Aug,
    soybean Sep–Aug); PSD market year `Y` means `Y/Y+1`.
* **Missing data is an absent row.** There are zero blank values and zero zeros in the file.
* `source_type=estimate` marks the 58 rows that are USDA forecasts or preliminary estimates
  (2025 and 2026 ERS years, plus all the vintage series). Everything else is `api`.
* **Southern-hemisphere timing:** Brazilian/Argentine market year `Y/Y+1` is planted Sep–Dec of
  `Y` and harvested Jan–Jun of `Y+1`, i.e. it falls in Deere fiscal Q1–Q3 of **FY(Y+1)**. This is
  noted on every `br_*`/`ar_*` row.

---

## 4. USDA forecast vintages for 2026 — and why they matter

The current USDA vintage is the **February 5, 2026** release. It is the *only* 2026 vintage that
exists: ERS publishes three times a year (Feb / Sep / Dec) and the next release was still due
when this dataset was frozen on 2026-08-16.

| Year | Feb-2024 | Feb-2025 | Sep-2025 | **Feb-2026** |
|---|---|---|---|---|
| Net farm income 2024 | 116.1 | 139.1 | 127.8 | **127.5** |
| Net farm income 2025 | — | 180.1 | 179.8 | **154.5** |
| Net farm income 2026 | — | — | — | **153.4** |

**The 2025 forecast was cut by 14 percent between September 2025 and February 2026** (179.8 →
154.5), and the 2024 forecast moved across a 19.8 percent range across four vintages. Any model
that treats USDA farm-income forecasts as precise inputs is mis-specified: the forecast error
is large, and it is *biased upward in the vintages published before large ad-hoc payment
programmes are settled*. The `*_fcst_v*` series exist so a model can estimate that revision
process rather than assume it away.

**What USDA currently projects for 2026** (the quarter being forecast):

| Series | 2025 | 2026 forecast | Change |
|---|---|---|---|
| Net farm income | 154.54 | 153.38 | −0.7% |
| Net cash farm income | 153.90 | 158.50 | **+3.0%** |
| Crop cash receipts | 238.05 | 240.82 | +1.2% |
| Government payments | 30.54 | **44.34** | **+45.2%** |
| Farmland value ($/acre) | 4,350 | 4,500 | +3.4% |
| Debt-to-asset ratio (%) | 13.49 | 13.75 | +0.26pp |

The read-through for Deere is unflattering: the 2026 improvement in cash income is essentially
*all* government transfer payments, not crop revenue. Farmers do not buy combines on ad-hoc
disaster payments the way they buy them on high crop receipts.

---

## 5. Validation

Every check below is produced by the build script itself (`===== VALIDATION =====` block) so it
re-runs with the data.

### 5.1 Cross-source agreement (the required ≥5 checks)

| # | Check | Result |
|---|---|---|
| 1 | **Deere's own Q1 FY2026 call (offline corpus, authoritative) vs my extraction.** Management said the USDA forecast 2026 net cash farm income "up around 3%", "driven by more government payments", with crop cash receipts "up slightly". | **+2.99%**, govt payments **+45.2%**, crop receipts **+1.16%**. Exact match on all three. |
| 2 | **USDA ERS net farm income vs BEA farm proprietors' income** (Commerce Dept, genuinely independent agency and independent methodology) | YoY *direction* agrees in 2023 (−19.2% vs −24.9%), 2024 (−13.3% vs −19.0%) and 2025 (+21.2% vs +31.0%). Level correlation r = 0.888 over 2006–2025. |
| 3 | **US corn harvested acres: ERS Feed Grains vs FAS PSD**, 2023/24/25/26 | 0.00% difference on all four |
| 4 | **US soybean harvested acres: ERS Oil Crops vs FAS PSD**, 2023/24/25 | 0.00% difference on all three |
| 5 | **NASS land values read from two different annual summaries' charts** | 60 year-values appear in ≥2 summaries; **34 agree exactly**, 26 differ and every one of those is a documented NASS revision (see 5.2) |
| 6 | **ERS internal identity**: crop + livestock cash receipts = all-commodity cash receipts, 2015/2020/2024 | 0.00% |
| 7 | **Brazil: FAS PSD soybean production vs World Bank crop production index** (two unrelated producers) | r = 0.931, n = 17 |
| 8 | **EU: Eurostat ag output (EUR) vs World Bank EU ag value added (USD)** | r = 0.869, n = 20 |
| 9 | **NASS farmland $/acre vs ERS farm real estate asset value** (two agencies, two units) | r = 0.996, n = 21 |
| 10 | Plausibility: US net farm income vs US farm machinery capex | r = 0.847, n = 21 |

**Honesty note on checks 3 and 4.** ERS and FAS agree to the last digit because both republish the
same underlying NASS/WAOB estimates. They confirm my *parsing* is correct; they are **not**
evidence that USDA's acreage estimate is correct. The genuinely independent checks are #1, #2,
#7 and #8.

### 5.2 Discrepancies found and how they were handled

* **NASS revises farmland values, sometimes a lot.** The 5-year regional tables inside each
  Land Values summary are frozen at the values published that year, while the 15-year trend
  chart at the front of the *same* PDF carries the current revised history. 18 of 63 year-values
  disagree between the two. The largest:
  * `us_cropland_values` 2012: as-published table **3,550** → currently **3,350** (5.97%)
  * `us_farmland_values` 2012: **2,650** → **2,520** (5.16%)
  * `us_cropland_values` 2011: **3,100** → **2,980** (4.03%)
  These are the 2012 Census-of-Agriculture benchmark revisions. **The build takes the chart value
  from the newest summary covering each year**, so the series is on the current revised basis end
  to end. A naive "latest table wins" extraction would have put a 5% level break into 2011–2012.
  The 2020–2022 revisions (~2%) are handled the same way.
* **ERS vintage revisions** — quantified in §4, and exposed as explicit `*_fcst_v*` series rather
  than being smoothed over.
* **ERS 2015 farm-income restatement is *not* present** — I take the whole history from a single
  Feb-2026 vintage, so `us_net_farm_income` is internally consistent across all 21 years.

---

## 6. Caveats

1. **2025 and 2026 are not actuals.** 58 rows are `source_type=estimate`. USDA's 2025 figure is a
   preliminary estimate and 2026 is a forecast; both will move (§4 shows by how much historically).
2. **`us_planted_acres_soybean` and `us_harvested_acres_soybean` stop at 2025.** The ERS Oil Crops
   Yearbook had not published 2026/27 acreage at the 2026-08 data cut. A substitute exists in the
   file: `us_soybean_area_harvested` (FAS PSD) has a 2026 value of 34.71 Mha ≈ 85.8 M acres.
   Corn planted acreage *is* available for 2026 (96.73 M acres, down from the record 98.79 M in 2025).
3. **`us_farm_capex_tractors` / `us_farm_capex_other_machinery` stop at 2024.** ERS forecasts the
   capex aggregate but not its components. Use `us_farm_capex_vehicles_machinery` for 2025–2026.
4. **World Bank series lag badly.** `us_ag_value_added_*` stops at 2021, `eu_crop_production_index`
   at 2020, the other crop indices at 2022. They are context, not nowcast inputs.
5. **Annual frequency is a real limitation.** Deere reports quarterly; almost everything here is
   annual. `us_farm_proprietors_income_bea_q` (quarterly, through 2026Q2) is the only high-frequency
   farm-income signal in the file, and it is a *different measure* from USDA net farm income (BEA
   excludes corporate farms and imputes differently) — use it for turning points, not levels.
6. **`us_farm_debt_to_asset_ratio` is in percent, not a 0–1 ratio** (2026 = 13.75). Do not mix it
   with a decimal ratio.
7. **NASS reference-date change**: land values ≤2010 are as of January 1, ≥2011 as of June 1.
   Flagged per row. If you difference the series, the 2010→2011 change spans 17 months, not 12.
8. **Land values ≤2010 come from the "48 States" total** (excludes Alaska and Hawaii) because that
   is how NASS labelled it then. Verified identical to the later "United States" label in every
   overlapping year.
9. **`brl_usd_fx_rate` 2026 is a partial-year average** (observations through the 2026-08 cut).
10. **Argentina has no FX series** here — no keyless source found. Argentine ag economics are
    heavily distorted by export taxes (*retenciones*) and multiple exchange rates, so
    `ar_ag_value_added_usd` in particular should be treated as low-quality.
11. **PSD later market years are USDA forecasts**, not actuals — 2025/26 and 2026/27 rows for all
    countries will be revised.
12. **The `Q3 2026` row in the corpus `INDEX.md` is mislabelled** (it is dated 2026-05-21, the day
    of Q2 earnings, and is Q2 material). No Q3 FY2026 data exists anywhere and none is used here.
    The only corpus document used in this task is the Q1 FY2026 call of 2026-02-19, for validation.
