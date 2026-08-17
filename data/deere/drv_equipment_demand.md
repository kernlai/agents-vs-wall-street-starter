# drv-equipment-demand — direct US equipment demand indicators for Deere (DE)

**Data file:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/drv_equipment_demand.csv`
**Rows:** 4,019 · **Series:** 50 · **Span:** 2003-09-30 → 2026-07-31
**Built:** 2026-08-16 · **Today:** 2026-08-16 (Deere has **not** reported FY2026 Q3)

This file contains **no Deere financials**. Every series is an external,
industry-level indicator of end demand for agricultural equipment. There is
therefore no `segment_basis` / `as_reported_or_restated` dimension here — the
PPA vs legacy Agriculture & Turf discontinuity does not apply to any row in
this file. It *does* apply when you join these indicators to Deere segment
results, and the mapping notes below say which series line up with PPA.

---

## 1. The headline answer on coverage

The task asked for 20 years. Here is what actually exists:

| Series family | True coverage | 20-year target met? |
|---|---|---|
| `us_ag_equipment_ppi` (+ 3 companions) | **2005-01 → 2026-07, monthly, complete, zero gaps** | **Yes** (21.6 years) |
| `us_tractor_unit_sales_*`, `us_combine_unit_sales` | 2003-09 → 2026-07, **184 of 275 months present** | Partly — see the hole below |
| `us_dealer_new_inventory_units` / `_months` | 2004-08 → 2026-06, 129 / 100 obs | Partly |
| `us_used_*` value & inventory changes (Sandhills) | 2021-01 → 2026-07 | **No — 5.6 years only** |
| `idx_used_equipment_values` (derived) | 2022-11 → 2026-07, fragmented | **No** |
| `us_dealer_used_inventory_months` | **NOT PRODUCED — no public source exists** | **No** |

### The AEM hole: 2006–2010

AEM monthly unit observations per calendar year (out of 12):

```
2003: 4   2004:10   2005: 7   2006: 2   2007: 0   2008: 0   2009: 0   2010: 1
2011: 9   2012:11   2013: 9   2014: 9   2015: 9   2016:10   2017:10   2018:11
2019: 5   2020:10   2021:12   2022:12   2023:12   2024:12   2025:12   2026: 7
```

**2007, 2008 and 2009 are completely absent, and 2006 and 2010 are nearly
absent.** This is not a parsing failure. AEM's monthly report is a members'
product; the only free copies are the PDFs AEM posted on its own website, and
the Internet Archive holds **no** capture of any AEM US ag report between
2006-03 and 2010-11. I checked every archived path on aem.org
(`/Trends/USAg/PDF/`, `/AllDocuments/AEM/MI/Reports/`,
`/AEM/media/docs/Statistics/`, the modern `getattachment` GUIDs) via the
Wayback CDX API. The 2006–2010 files were never archived.

**Annual (December) totals** exist for 2003, 2004, 2011–2014, 2016–2025.
Missing: **2006, 2007, 2008, 2009, 2010, 2015.**

I did not pad, interpolate or back-cast any of this. Missing periods are
absent rows.

Practical consequence for a modeller: the AEM unit series covers the
**2011→2026 cycle in full** (the 2013 peak, the 2016 trough, the 2021–23
recovery, the 2024–26 downdraft) but **cannot see the 2008 commodity boom or
the 2009 crash**. If you need a demand proxy that spans 2006–2010, use
`us_ag_constr_mining_machinery_ip` (Fed industrial production, complete from
2005) as the bridge, and treat AEM as the high-precision series over
2011–2026.

---

## 2. Series dictionary

### Unit retail sales — AEM (`source_type = vendor`)

The Association of Equipment Manufacturers publishes preliminary monthly
**retail** (dealer-to-end-customer) unit sales for the 50 states + DC,
collected from member manufacturers.

| series_id | Definition | Deere segment read |
|---|---|---|
| `us_tractor_unit_sales_100hp_plus` | AEM "2WD 100+ HP" | **PPA — primary** |
| `us_tractor_unit_sales_4wd` | AEM "4WD Farm Tractors" (articulated) | **PPA** |
| `us_tractor_unit_sales_large_total` | *derived* = 100+ HP 2WD **+** 4WD | **PPA — best single unit proxy** |
| `us_combine_unit_sales` | AEM "Self-Propelled Combines", all sizes | **PPA — primary** |
| `us_tractor_unit_sales_total` | AEM "Total Farm Tractors" (all 2WD classes + 4WD) | mixed |
| `us_tractor_unit_sales_2wd_total` | AEM "Total 2WD Farm Tractors" | mixed |
| `us_tractor_unit_sales_40to100hp` | AEM "2WD 40 < 100 HP" | Small Ag & Turf |
| `us_tractor_unit_sales_under40hp` | AEM "2WD < 40 HP" | Small Ag & Turf |

**Definitional trap you must not miss.** AEM's `100+ HP` bucket is
**2-wheel-drive only**. All 4WD articulated tractors are far above 100 HP but
sit in their own line. `us_tractor_unit_sales_100hp_plus` therefore
*understates* large-tractor demand by the 4WD volume, which ran 2,313–6,933
units a year across the annual observations in this file. Use
`us_tractor_unit_sales_large_total` when you want "large tractors" in the
sense the trade press and sell-side mean it.

**Second trap.** `us_tractor_unit_sales_total` is dominated by sub-40 HP
compact tractors — 50–69% of all units depending on the year (62% in 2024,
63% in 2025), a consumer/housing-driven market. Note the share is itself
strongly cyclical *in the opposite direction*: it falls toward 50% at large-ag
peaks (2011–13) and rises toward ~69% at troughs (2020), so the total series
is not merely noisy about PPA, it is counter-cyclically biased against it. It
is a *poor* proxy for PPA and will mislead a model that treats it as one. It
is included because it is the number the headlines quote.

Rows are monthly (`fiscal_quarter` = calendar quarter, `period_end` = month
end) **plus** annual rows (`fiscal_quarter = FY`, `period_end = YYYY-12-31`)
taken from each December report's year-to-date column.

### Dealer new-equipment inventory — AEM

| series_id | Definition |
|---|---|
| `us_dealer_new_inventory_units[_100hp_plus, _combines]` | AEM "Beginning Inventory" — **new** units in the dealer channel |
| `us_dealer_new_inventory_months[_100hp_plus, _combines]` | *derived* months of supply (`source_type = inference`) |

Two things to know:

1. **Date stamping.** AEM reports this stock as of the *beginning* of the
   report month. I stamp it at the **end of the preceding month**, which is the
   same instant. So the July 2026 report's opening stock appears on
   `2026-06-30`, not `2026-07-31`. If you re-derive this from raw AEM PDFs
   yourself and get a one-month offset against my file, this is why.
2. **Months of supply denominator.** `inventory ÷ (trailing-12-month retail
   sales ÷ 12)`. A trailing-12m denominator is essential because US tractor
   and combine retail is violently seasonal — a current-month denominator
   would produce a series that mostly measures the calendar. The trailing-12m
   total is reconstructed as `YTD(this year) + prior-year annual −
   YTD(prior year)`, all three read off AEM reports (a single monthly report
   prints both years' YTD columns). That identity is why this series has 100
   observations rather than the 57 a naive "needs 12 consecutive monthly
   prints" rule would allow.

Recent values look like this — 100+ HP months of supply drifting up through
2026 (4.06 in Dec-2025 → 4.92 in Jun-2026) while combines sit near 3, which is
consistent with Deere's own commentary that **new** inventory has been
right-sized and the problem has moved to **used**.

### `us_dealer_used_inventory_months` — NOT PRODUCED

There is **no public source for US dealer used-equipment months of supply.**
AEM's report covers new units only. Sandhills publishes used *inventory
levels* as percentage changes, not as months of supply, and not with a
denominator. Deere discusses used inventory qualitatively and in relative
terms on its earnings calls (e.g. FY2025 Q4: "Deere 175 horsepower and greater
tractors in North America have declined by around 7% since they peaked in
March 2025"; FY2025 Q2: "new inventory for tractors above 220 horsepower is
down over 40% year-over-year on a unit basis, while new combines are down
nearly 25%") but never publishes a months-of-supply level.

Rather than invent one, I emitted **no rows** for this series. The nearest
usable substitutes in this file are
`us_used_tractor_inventory_yoy_pct` and `us_used_combine_inventory_yoy_pct`
(Sandhills, 2023-06 onward).

### Used-equipment values — Sandhills (`source_type = vendor`)

Sandhills Global runs TractorHouse / Machinery Trader and publishes the
Sandhills Equipment Value Index (EVI). **The EVI level is a paid product.**
The free monthly press releases quote only month-over-month and
year-over-year percentage *changes*, so that is what this file carries:

`us_used_{tractor, combine, high_hp_tractor, compact_utility_tractor,
farm_equipment}_{auction_value, asking_value, inventory}_{mom_pct, yoy_pct}`

`us_used_tractor_*` is the best-covered farm series (2021-02 → 2026-07); in
these releases it refers to the TractorHouse used tractor market, which is
dominated by high-horsepower row-crop units.
`us_used_high_hp_tractor_*` is an explicitly-named but very short-lived
heading (only 2023-08 → 2023-11) — do not build on it.

**Why this matters for Deere specifically:** falling used auction values both
lead weak new-equipment demand (they compress trade differentials, which is
exactly the mechanism Deere described on the FY2025 Q4 call) and directly
drive lease residual write-downs in Financial Services.

### `idx_used_equipment_values` / `_combines` — derived, handle with care

`source_type = inference`. Built by chain-linking the Sandhills M/M auction
value changes. **The chain restarts at 100.00 after every gap in the source
releases**, and gaps are frequent — the tractor index has 6 separate runs in
27 observations. Every restart row says so in its `notes` field, starting with
`CHAIN RESTART (run N begins here)`. Levels are comparable **only within a
run**; differencing across a restart produces a fictitious jump.

For most modelling purposes the raw `*_auction_value_mom_pct` /
`*_yoy_pct` series are strictly better than this index. It is provided because
the task asked for it.

### Price indices — FRED / BLS (`source_type = api`)

| series_id | FRED id | What it is |
|---|---|---|
| `us_ag_equipment_ppi` | `PCU333111333111` | **Primary.** PPI by Industry: Farm Machinery & Equipment Mfg (NAICS 333111), 1982-06 = 100, NSA |
| `us_ag_equipment_ppi_commodity` | `WPU111` | PPI by Commodity: Agricultural Machinery & Equipment — independent BLS programme |
| `us_ag_equipment_ppi_primary_products` | `PCU333111333111A` | NAICS 333111 primary products only, narrower basket, Dec-1975 = 100 |
| `us_ag_constr_mining_machinery_ip` | `IPG33311S` | **Not a price.** Fed industrial production for NAICS 3331, 2017 = 100, SA — real output volume |

All four are complete monthly 2005-01 → 2026-07 (IP through 2026-06). The
three PPI series have **different base periods** — never compare their levels
to each other, only their growth rates.

`us_ag_constr_mining_machinery_ip` is deliberately included as the one
volume-like series that spans the 2006–2010 AEM hole.

---

## 3. Method

Everything was extracted by script. Nothing was transcribed by hand. The
scripts live in
`/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/`:

| Script | Does |
|---|---|
| `fetch_aem_tractor_combine.py` | Discovers every archived AEM US ag report PDF via the Wayback CDX API, downloads them (+ the current live AEM pre-release), runs `pdftotext -layout`, parses the unit table |
| `fetch_aem_globenewswire_mirror.py` | Fetches the same AEM releases as HTML from the FinancialContent syndication mirror of GlobeNewswire — used for gap-filling **and** as the independent cross-check |
| `fetch_fred_equipment_ppi.py` | Pulls the four price/volume indices from FRED's keyless CSV endpoint |
| `fetch_sandhills_used_values.py` | Crawls all 531 sandhills.com news articles, parses the used-equipment value/inventory sections |
| `build_drv_equipment_demand.py` | De-duplicates, reconciles vintages, derives months of supply and the chained index, writes the tidy CSV |

Two document generations had to be handled. AEM's report changed layout around
2011: the modern one uses `< 40 HP` / `100+ HP` / `Total Farm Tractors` /
`Self-Prop Combines`; the pre-2011 "Flash Report" uses
`Under 40 HP` / `100 HP & Over` / `TOTAL FARM WHEEL TRACTORS` /
`(Self-Propelled)`, and writes negative percentages in parentheses. The parser
reads numbers **only after the matched row label**, so digits inside labels
("40", "100") can never be mistaken for data.

### Revisions

AEM revises. Each monthly report prints the current year and the prior year,
and the prior-year column has been restated by the time it reappears. A given
month is therefore observed 2+ times with different values. **The CSV carries
the latest vintage**, and where vintages disagree the `notes` field records the
first print, the latest vintage, and the spread, e.g.:

> `REVISED: AEM first printed 2773, latest vintage (2023-12 report) is 2759; spread across 3 vintages = 14.`

Revisions are small (typically 0.1–1.0%) but real. If you are backtesting a
real-time forecasting process you want the **first print**, not this file's
latest-vintage values — the raw per-vintage observations are preserved in
`aem_raw_observations.json` in the build scratch directory.

---

## 4. Validation

Four independent cross-checks were run.

**1. AEM PDF vs GlobeNewswire press release — 112 overlapping cells.**
Comparing my PDF extraction against the independently-marked-up HTML release
for 12 months, matched on **first print** vintage:

> **111 of 112 cells agree exactly. 1 disagreement.**

**The single disagreement is an error in the GlobeNewswire HTML, not in my
extraction.** July 2026, 2WD 40 < 100 HP: the PDF says **4,794**, the press
release HTML says **4,974** (a digit transposition). Two internal identities
settle it:

| | implied YoY vs 5,180 | 2WD components sum | reported |
|---|---|---|---|
| PDF 4,794 | −7.45% | 9,717+4,794+1,322 = **15,833** ✓ | −7.5%, total 2WD 15,833 |
| HTML 4,974 | −3.98% ✗ | 16,013 ✗ | |

The PDF is authoritative and is what the CSV carries. Flagging it rather than
silently picking one: **if you source AEM July 2026 from the press release
instead of the PDF, your 40–100 HP figure will be wrong by 180 units.** This
does not touch any priority series.

**2. Internal table identities across all 184 AEM months.**
`<40 + 40–100 + 100+ = Total 2WD` and `Total 2WD + 4WD = Total Farm Tractors`,
checked on every month: **184 months, 0 failures.**

**3. FRED vs BLS public API — 62 overlapping observations.**
`PCU333111333111` and `WPU111` pulled directly from
`api.bls.gov/publicAPI/v2` (the upstream producer, not a redistributor) for
2024–2026 and compared to the FRED CSV values in the file: **62 of 62 agree to
the full published precision, 0 disagreements.**

**4. Trade press vs my AEM extraction, July 2026.** Independent reporting of
the July 2026 AEM release (RFD-TV, KFGO) states total tractor sales 15,985
units (−10.9%), combines 340 (−5.3%), YTD 100+ HP −15.5%, 4WD −38.7%, YTD
self-propelled combines 1,676 (−10.2%). **All five match my extraction
exactly.** A separate check on the December 2021 report: trade press reported
a full-year 2021 gain of 10.3% for tractors and 24.7% for combines — my
extraction gives 10.3% and 24.7%.

**Plausibility.** The extracted annual series reproduce the known ag cycle
without any smoothing: combines 10,753 (2013 peak) → 3,971 (2016 trough) →
7,349 (2023) → 3,579 (2025); 100+ HP 2WD tractors 37,232 (2013) → 17,016
(2017) → 27,708 (2023) → 17,648 (2025). The 2025 collapse is consistent with
Deere's guided "large ag industry sales in the U.S. and Canada down
approximately 30%".

---

## 5. Caveats a modeller must read

1. **2007–2009 are entirely missing from the AEM unit series, and 2006/2010
   nearly so.** Do not fit a model that assumes a continuous monthly panel
   from 2006. Either start the unit series at 2011 or bridge with
   `us_ag_constr_mining_machinery_ip`.
2. **Missing months are absent rows, not zeros.** Any resampling you do must
   treat them as missing, not as zero demand. There are no zero values and no
   blank values anywhere in the file.
3. **`us_tractor_unit_sales_100hp_plus` excludes 4WD.** Use
   `us_tractor_unit_sales_large_total` for the true large-tractor aggregate.
4. **`us_tractor_unit_sales_total` is a compact-tractor series in disguise**
   and is a poor PPA proxy.
5. **AEM is US-only.** Deere's PPA segment is global — North America is
   roughly half of it, with Brazil and Europe material and not covered here.
   AEM also publishes Canada and Brazil reports; those were out of scope for
   this task but are available on the same URL pattern
   (`CAN-Month-Ag-Report-M-YYYY.pdf`) if a later pass needs them.
6. **AEM is retail (dealer→farmer), Deere's revenue is wholesale
   (Deere→dealer).** The two diverge by the change in dealer inventory —
   which is precisely why `us_dealer_new_inventory_units` is in this file.
   In an underproduction year like FY2025 Deere's shipments fell *faster*
   than retail; when the channel restocks the reverse happens. A model
   regressing Deere sales on AEM retail alone will mis-time inflections.
7. **AEM covers "most, but not all" manufacturers** (AEM's own wording) and
   the data are "in part, estimates subject to revision".
8. **AEM is a members' product.** The figures here come from AEM's own freely
   published PDFs, its press releases, and Internet Archive copies of the
   same. Redistribution beyond internal modelling may need AEM's permission;
   AEM asks to be acknowledged as the source.
9. **`fiscal_year` on every row here is the CALENDAR year**, per the spec for
   external series. These are calendar-month observations; Deere's fiscal
   quarters end in late Jan / early May / early Aug / late Oct. You must
   aggregate calendar months onto Deere's fiscal calendar yourself, and a
   Deere fiscal quarter is **not** three calendar months aligned to a quarter
   end (FY2026 Q2 ended 2026-05-03; FY2026 Q3 ends approximately 2026-08-02).
10. **The most recent AEM month is July 2026, released 2026-08-11.** It covers
    the month in which Deere's FY2026 Q3 ended (~2026-08-02), so July AEM data
    is a *partial* overlap with the unreported quarter, not a read on it.
11. **Sandhills sign inference is regex-based.** Direction is taken from the
    nearest directional word ("decreased", "were up", "but increased"). I
    hand-verified 6 randomly selected records against source prose, including
    mixed "up X% M/M but down Y% YOY" constructions; all 6 were correct. This
    is not a proof of zero error across all 374 records.
12. **The three PPI series have different base periods.** Compare growth
    rates, never levels.
13. **No FY2026 Q3 Deere data appears in this file**, and none exists. Note
    that the corpus `INDEX.md` row labelled `2026-05-21 | Call Transcript |
    Q3 2026` is mislabelled Q2 material — it is dated the same day as Q2
    earnings. Nothing in this file derives from it.

---

## 6. What I could not get

- **US dealer used-equipment months of supply** — no public source exists.
- **AEM units 2006-03 → 2010-11** — never archived; not purchasable within
  this task's constraints. AEM sells a 40-year annual history through its
  shop, which would close the annual (not monthly) gap.
- **Sandhills EVI index levels** — paid product; only changes are free.
- **Tractor Zoom / Machinery Pete auction indices** — Tractor Zoom's Used Farm
  Equipment Index and Row Crop Tractor Index sit behind Tractor Zoom Pro with
  no free data endpoint. Neither was usable.
- **A used-equipment value series longer than 5.6 years.** Nothing free spans
  20 years for used ag equipment values.
