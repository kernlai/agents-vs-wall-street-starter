# Deere & Company — structured guidance dataset

Built 2026-08-16. Source of record: the frozen offline corpus
`challenge/offline-data/deere` (310 documents, 2012-05-16 → 2026-05-28, frozen
2026-08-14), plus the SEC XBRL company-concept API (CIK 315189) for actuals.

**Today is 2026-08-16. Deere has NOT reported FY2026 Q3.** Nothing in either file
is an FY2026 Q3 actual. The most recent guidance vintage is the FY2026 Q2 release
of 2026-05-21.

## Files

| File | Rows | Shape |
|---|---|---|
| `de_guidance.csv` | 1,068 | tidy long, 48 series, standard 9-column header |
| `de_guidance_vs_actual.csv` | 229 | analysis table, one row per (metric × fiscal year × vintage) |

Reproducible build (standard library only, `python3`):

```
scripts/data/de_guidance_extract.py        extraction library: event table + regex parsers
scripts/data/de_build_guidance.py          writes de_guidance.csv
scripts/data/de_build_guidance_vs_actual.py writes de_guidance_vs_actual.csv
scripts/data/de_validate_guidance.py       112 cross-source checks
scripts/data/de_scan_guidance_sentences.py corpus reconnaissance helper
```

Every number in both CSVs was parsed out of a source document by regex. Nothing
was transcribed by hand.

---

## READ THIS FIRST: how the vintage dimension is encoded

Guidance is a two-dimensional object — *what period is being guided* × *when the
guidance was issued*. The mandated header has no vintage column, so:

* `period_end` / `fiscal_year` = **the fiscal year being guided** (the target).
* `fiscal_quarter` = **the vintage quarter — which earnings release the guidance
  came from. It is NOT a quarter of the guided period.**
* `notes` on every guidance row carries `guidance_issued=YYYY-MM-DD`,
  `guidance_vintage=FY<year> <quarter> earnings release`, and `vintage_seq`.

`vintage_seq` orders the four vintages of each fiscal year:

| vintage_seq | fiscal_quarter | meaning |
|---|---|---|
| 0 | `Q4` | **initial** guidance, issued with the *prior* fiscal year's Q4/full-year results, i.e. before the guided year began |
| 1 | `Q1` | first update, with Q1 results |
| 2 | `Q2` | second update, with Q2 results |
| 3 | `Q3` | final update, with Q3 results |

So `series_id=de_guidance_fy_net_income_mid, period_end=2026-11-01,
fiscal_quarter=Q4` is the FY2026 guidance issued on **2025-11-26** with FY2025 Q4
results. The key `(series_id, period_end, fiscal_quarter)` is unique — verified.

Ranges are stored as three rows (`_low`, `_mid`, `_high`). For point guidance
("about $7.0 billion") low = mid = high, and `notes` says
`point estimate`. `de_guidance_fy_net_income_range_width` (= high − low, 0 for a
point) lets a model condition on how much uncertainty management admitted to.

## THE SEGMENT DISCONTINUITY — do not merge across it

Deere reorganised for FY2021. Before: one **Agriculture & Turf** segment. After:
**Production & Precision Ag (PPA)**, **Small Ag & Turf (SAT)**, **Construction &
Forestry (CF)**. Every segment row carries `segment_basis=legacy-AT` or
`segment_basis=modern-PPA` and `as_reported_or_restated=` in `notes`, and the two
eras never share a `series_id`:

| era | series |
|---|---|
| legacy-AT | `..._segment_sales_growth_ag_turf_{low,mid,high}`, `..._segment_sales_growth_cf_legacy_at_{low,mid,high}`, `..._segment_operating_margin_ag_turf_mid`, `..._segment_operating_margin_cf_legacy_at_mid` |
| modern-PPA | `..._segment_sales_growth_{ppa,sat,cf}_{low,mid,high}`, `..._segment_operating_margin_{ppa,sat,cf}_{low,mid,high}`, `..._segment_{price_realization,currency_translation}_{ppa,sat,cf}`, `..._implied_ppa_operating_profit_*` |

**Critical boundary detail:** the *first* FY2021 guidance — issued 2025-11-25… no,
issued **2020-11-25** with FY2020 Q4 results — was still framed on the **legacy
A&T basis** ("worldwide sales of agriculture and turf equipment forecast to
increase 10 to 15 percent for fiscal-year 2021"). PPA/SAT/CF guidance first
appears on **2021-02-19**. So FY2021 has only three modern-basis vintages
(Q1/Q2/Q3), and its `vintage_seq=0` row lives in the legacy-AT series. A model
that assumes four modern PPA vintages per year will silently mis-align FY2021.

All guidance rows are **as-reported at the vintage date** — guidance is never
restated. The *actuals* used in `de_guidance_vs_actual.csv` for PPA/SAT/CF FY2019
and FY2020 are Deere's **restated** modern-basis comparatives (from the FY2021
10-K three-year table); they are only used as growth denominators, never as
guidance.

## Series inventory (48)

Consolidated
* `de_guidance_fy_net_income_{low,mid,high}` — USDm, 57 vintages, FY2012 Q2 → FY2026 Q2. The core series; Deere's only consistently guided bottom line.
* `de_guidance_fy_net_income_range_width` — USDm.
* `de_guidance_fy_adjusted_net_income_mid` — USDm, FY2018 only (non-GAAP, excludes US tax-reform provisional items; **not** comparable to the GAAP series).
* `de_guidance_fy_financial_services_net_income` — USDm, 34 vintages FY2012–FY2025.
* `de_guidance_fy_net_sales_revenues_growth` — percent, 12 vintages, FY2017–FY2019 only. Deere published an explicit consolidated revenue-growth line only in those three years.

Segment — legacy-AT (FY2012–FY2021 initial)
* `..._segment_sales_growth_ag_turf_{low,mid,high}` — 33 vintages.
* `..._segment_sales_growth_cf_legacy_at_{low,mid,high}` — 33 vintages.
* `..._segment_operating_margin_ag_turf_mid` — 23 vintages FY2013–FY2019, from prepared remarks.
* `..._segment_operating_margin_cf_legacy_at_mid` — 4 vintages.

Segment — modern-PPA (FY2021 Q1 onward)
* `..._segment_sales_growth_{ppa,sat,cf}_{low,mid,high}` — 22 vintages each.
* `..._segment_sales_{ppa,sat,cf}_usdm_{low,high}` — the FY2021 Q1 vintage alone guided segment net sales in **absolute dollars** ($15,500–16,500m for PPA); growth-equivalent rows for that vintage are `source_type=inference`.
* `..._segment_operating_margin_{ppa,sat,cf}_{low,mid,high}` — 22 vintages each, from the earnings-call slide decks (the only place Deere publishes segment margin outlook).
* `..._segment_price_realization_{ppa,sat,cf}`, `..._segment_currency_translation_{ppa,sat,cf}` — 17 vintages each, the drivers Deere breaks out beside the sales outlook.
* `de_guidance_fy_implied_ppa_operating_profit_{low,mid,high}` — USDm, 21 vintages, **`source_type=inference`**: prior-FY actual PPA net sales × (1 + guided sales growth) × guided operating margin. Deere never guides segment operating profit in dollars; this is the closest thing to guidance on forecast target #3.

## `de_guidance_vs_actual.csv`

One row per (metric, fiscal year, vintage). Columns: `metric, fiscal_year,
period_end, vintage_quarter, vintage_seq, guidance_issued, guidance_low,
guidance_mid, guidance_high, units, actual, error_abs, error_pct,
actual_vs_range, cycle_phase, source_guidance, source_actual, notes`.

* `error_abs = actual − guidance_mid`; **positive = Deere under-promised**.
* `error_pct = 100 × error_abs / |guidance_mid|`.
* `actual_vs_range ∈ {above, within, below, point_beat, point_miss}`.
* `cycle_phase` is computed, not asserted: `up_cycle` if FY consolidated net sales
  and revenues rose y/y, `down_cycle` if they fell. This is an **ex-post**
  classification — see caveats.

Metrics: `fy_net_income` (54), `fy_segment_sales_growth_cf_legacy_at` (28),
`fy_segment_sales_growth_ag_turf` (27), `fy_ppa_operating_margin` (19),
`fy_ppa_operating_profit_implied` (19), `fy_segment_sales_growth_{ppa,sat,cf}`
(19/19/19), `fy_h2_net_income_implied_by_q2_guidance` (13),
`fy_net_sales_revenues_growth` (12). FY2026 has no actual and therefore no rows.

---

# The analytical answer

## 1. Is Deere's guidance systematically conservative? Yes — measurably.

Full-year net income, 13 completed fiscal years (FY2013–FY2025), 52 vintages:

| vintage | n | mean error % | median error % | sd | beat rate | mean abs error (USDm) |
|---|---|---|---|---|---|---|
| Q4 (initial) | 13 | **+9.08** | +2.11 | 21.9 | 54% | 593 |
| Q1 | 13 | **+7.64** | +7.19 | 14.4 | 62% | 421 |
| Q2 | 13 | **+8.45** | +2.96 | 14.9 | 69% | 268 |
| Q3 | 13 | **+4.74** | +2.53 | 6.1 | **100%** | 132 |
| all | 52 | **+7.48** | +2.88 | — | 71% | — |

The mean error is positive at every vintage, the beat rate rises monotonically
with vintage, and the Q3 vintage has **never once been missed in 13 years** (13/13
beats, mean +4.7%). Dispersion collapses as the year progresses (sd 21.9 → 6.1;
MAE 593 → 132 USDm). Read plainly: Deere guides low and walks the number up.

The mean is dragged by a few very large up-cycle beats (FY2017 Q4 +54%, FY2021 Q4
+57%). The median (+2.9% overall, +2.5% at Q3) is the number a modeller should
anchor on; the mean is the number a modeller should use to size the right tail.

## 2. Does the bias differ between up-cycle and down-cycle years? Yes, and the shape differs too.

`cycle_phase` from realised FY revenue direction. Up-cycle years: FY2013, 2017,
2018, 2019, 2021, 2022, 2023. Down-cycle: FY2014, 2015, 2016, 2020, 2024, 2025.

| | n | mean error % | median error % | beat rate |
|---|---|---|---|---|
| up-cycle | 28 | **+9.79** | +4.84 | 82% |
| down-cycle | 24 | **+4.78** | +1.43 | 58% |

By vintage:

| vintage | up-cycle mean % | down-cycle mean % |
|---|---|---|
| Q4 (initial) | **+18.85** | **−2.31** |
| Q1 | +13.54 | +0.75 |
| Q2 | +4.65 | +12.88 |
| Q3 | +2.11 | +7.82 |

The bias is **not a constant conservatism premium — it rotates within the year
depending on the cycle**:

* **In up-cycles the error is front-loaded.** Deere's *initial* (Q4-vintage)
  guidance badly under-calls an upturn (+18.9% mean), then catches up: by Q3 the
  residual beat is only +2.1%. Management does not extrapolate an inflection it
  has not yet seen.
* **In down-cycles the error is back-loaded and flips sign.** The initial guidance
  is roughly unbiased or even slightly *optimistic* (−2.3%), and the conservatism
  only appears mid-year (+12.9% at Q2, +7.8% at Q3) — Deere cuts the range harder
  than the eventual outturn requires. FY2016 (Q2 mid $1.2bn vs $1.524bn actual,
  +27%), FY2020 (Q2 mid $1.8bn vs $2.751bn, +53%) and FY2024 (Q2 $7.0bn vs
  $7.100bn, +1.4% after a −11% initial *over*-call) are the pattern.

Practical rule: **the direction of the guidance bias depends on where you are in
the year, and the size depends on the cycle.** At a Q2 vintage in a down-cycle
year the historical mean beat is +12.9% (median smaller); at a Q3 vintage in a
down-cycle year, +7.8%.

FY2026 is a down-cycle year on this definition so far (H1 net sales and revenues
+8% y/y, but PPA sales −7% and the FY guidance implies FY revenue roughly flat to
up); treat the classification for FY2026 as **not yet determinable**.

## 3. Q2-vintage implied H2 versus H2 delivered — the FY2026 Q3 analogue

For each year: `implied H2 = FY guidance (Q2 vintage) − reported H1 actual`, versus
`actual H2 = FY actual − H1 actual`. This is exactly the inference required now.

| FY | cycle | implied H2 mid (USDm) | actual H2 (USDm) | error (USDm) | error % |
|---|---|---|---|---|---|
| 2013 | up | 1,566 | 1,803 | +237 | +15.2% |
| 2014 | down | 1,638 | 1,500 | −138 | −8.4% |
| 2015 | down | 823 | 863 | +40 | +4.9% |
| 2016 | down | 450 | 774 | +324 | +72.0% |
| 2017 | up | 993 | 1,152 | +159 | +16.0% |
| 2018 | up | 1,627 | 1,695 | +68 | +4.2% |
| 2019 | up | 1,667 | 1,620 | −47 | −2.8% |
| 2020 | down | 618 | 1,569 | +951 | +153.9% |
| 2021 | up | 2,487 | 2,950 | +463 | +18.6% |
| 2022 | up | 4,199 | 4,130 | −69 | −1.6% |
| 2023 | up | 4,556 | 5,347 | +791 | +17.4% |
| 2024 | down | 2,879 | 2,979 | +100 | +3.5% |
| 2025 | down | 2,452 | 2,354 | −98 | −4.0% |

Summary (n = 13): mean **+22.2%**, median **+4.9%**, beat rate **69%**, mean
absolute-dollar error **+214 USDm**, median **+100 USDm**.
Excluding FY2020 (COVID; the Q2-2020 guidance was cut to $1.6–2.0bn and the
outturn was $2.751bn): mean **+11.2%**, median **+4.5%**, mean error **+152 USDm**.
Up-cycle mean +9.6%; down-cycle mean +37.0% (+13.6% excluding FY2020).

The H2 error is roughly **twice** the full-year error in percentage terms, because
H1 is already banked — the whole full-year error is concentrated in the unguided
half. A model should apply the bias to the *residual*, not to the full year.

**Live application to FY2026.** Q2-vintage FY2026 guidance (issued 2026-05-21):
$4.5–5.0bn, mid $4.75bn. Reported H1 FY2026 net income: $2,429m. Implied H2:
**$2,071–2,571m, mid $2,321m**. Applying the historical Q2-vintage H2 bias:
median +4.5% → ≈ $2,426m; median +100 USDm → ≈ $2,421m; mean ex-FY2020 +11.2% →
≈ $2,581m. In FY2025, Q3 was the larger of the two H2 quarters (net income $1,289m in Q3
vs $1,065m in Q4, from SEC XBRL); this file does not carry a general quarterly
split — take that from the quarterly panel dataset.

## 4. Segment guidance accuracy (for forecast targets #1 and #3)

Errors here are in **percentage points** (guidance and actual are both growth
rates or margins), `actual − guidance_mid`.

| metric | n | mean err | median err | Q2-vintage mean err |
|---|---|---|---|---|
| `fy_segment_sales_growth_ppa` (modern) | 19 | +1.83 pp | +0.59 pp | +1.65 pp |
| `fy_segment_sales_growth_ag_turf` (legacy) | 27 | +0.99 pp | +0.10 pp | — |
| `fy_ppa_operating_margin` | 19 | **−0.18 pp** | −0.33 pp | −0.28 pp |
| `fy_net_sales_revenues_growth` | 12 | +2.19 pp | +0.35 pp | — |
| `fy_ppa_operating_profit_implied` | 19 | +51 USDm | −56 USDm | +18 USDm |

Two findings that matter for the PPA operating-profit target:

1. **Deere's segment *sales* guidance is very accurate and mildly conservative**
   (median +0.1 to +0.6 pp). It is a far tighter constraint than the net income
   guidance.
2. **Deere's segment *margin* guidance is essentially unbiased and, if anything,
   slightly optimistic** (mean −0.18 pp, median −0.33 pp) — the opposite sign to
   the net income conservatism. The consolidated net income beat therefore does
   **not** come from segment margins running hot; it comes from below-segment
   items (tax rate, financial services, corporate/other) and from the range being
   set wide.

**Live application to FY2026 PPA.** Q2-vintage FY2026 guidance: PPA net sales
down 5–10% off FY2025 actual $17,311m → $15,580–16,445m; PPA operating margin
11–13%. Implied FY2026 PPA operating profit **$1,714–2,138m, mid $1,926m**
(`de_guidance_fy_implied_ppa_operating_profit_*`, FY2026 Q2 vintage). Reported H1
FY2026 PPA operating profit is **$845m** ($139m Q1 + $706m Q2, −43% y/y), so the
implied H2 is **$869–1,293m**. Historically the implied-profit construction has a
median error of −56 USDm (mean +51 USDm) at the full-year level, i.e. close to
unbiased with wide dispersion.

---

## Validation

`scripts/data/de_validate_guidance.py` runs **112 independent cross-checks and
reports 0 disagreements**:

* **A — guidance, 8-K vs 10-Q/10-K (10 checks).** The same full-year net income
  guidance appears in the earnings-release 8-K and in the quarterly report filed
  the same day. All agree exactly (FY2016, FY2017, FY2018, FY2019, FY2020
  vintages).
* **B — guidance, 8-K prose vs prepared-remarks transcript (78 checks).** Legacy
  Agriculture & Turf and Construction & Forestry full-year sales-growth guidance,
  every vintage FY2015–FY2021, extracted independently from the press release and
  from the earnings-call script. All agree.
* **C — actuals, SEC XBRL vs corpus filings (22 checks).** FY2015–FY2025
  consolidated net sales and revenues, and net income attributable to Deere & Co,
  from `data.sec.gov` XBRL versus the Q4 8-K headline tables. All agree to within
  rounding (largest gap $0.2m, on FY2015 revenue: 28,862.8 vs 28,863).
* **D — segment actuals, 10-K three-year table vs Q4 8-K full-year column
  (2 checks).** Construction & Forestry FY2019 ($11,220m) and FY2020 ($8,947m)
  reconcile across the segment break, confirming the C&F segment was not
  redefined by the FY2021 reorganisation.

A fifth, informal check (not counted in the 112): for every modern-era vintage
the segment net-sales guidance parsed from the 8-K markdown table (62 cells
across PPA/SAT/CF, FY2021 Q2 → FY2026 Q2) was compared against the magnitude
described in the same day's earnings-call slide deck. Every cell that both
sources carried agreed on magnitude. The one cell where they disagreed — the
FY2025 Q4 PPA net-sales cell — is the extraction defect documented in caveat 3;
this comparison is how it was found.

## Caveats a modeller must know

1. **`fiscal_quarter` is the vintage quarter, not a quarter of the guided period.**
   A `Q4` row is the *initial* guidance issued with the **prior** fiscal year's
   results. Getting this wrong shifts every initial-guidance observation forward
   by a year.
2. **FY2026 Q3 does not exist in this dataset.** The most recent vintage is
   2026-05-21. `period_end` for FY2026 is `2026-11-01`, which is an **estimate**
   (Deere's 52/53-week calendar; derived from the confirmed FY2026 Q1 end
   2026-02-01 and Q2 end 2026-05-03). All other FY end dates are confirmed against
   SEC XBRL.
3. **One documented extraction defect and its repair.** In the FY2025 Q4 8-K
   (2025-11-26) the markdown segment-outlook table renders the PPA net-sales cell
   as `10%`; the correct guidance, confirmed by the same day's slide deck
   ("5-10%" with a downward arrow) and by the two subsequent vintages that
   maintained "Down 5 to 10%", is **down 5 to 10%**. That single cell is sourced to
   the slide deck and flagged in `notes`. No other cell was overridden.
4. **`cycle_phase` is ex-post.** It is computed from realised FY revenue direction,
   which was not knowable at the vintage date. Using it as a regression feature
   leaks information. Use it for descriptive stratification, or replace it with an
   ex-ante proxy (e.g. the sign of the guided segment sales growth in the same
   row).
5. **The FY2018 GAAP net income guidance is contaminated by US tax reform.** The
   Q1/Q2/Q3 FY2018 GAAP figures embed $750–803m of provisional tax expense.
   `de_guidance_fy_adjusted_net_income_mid` carries the company's non-GAAP
   alternative ($2.85bn at Q1, $3.1bn at Q3). Do not mix the two series.
6. **`de_guidance_fy_implied_ppa_operating_profit_*` is an inference, not
   guidance.** Deere never guides segment operating profit in dollars. The
   construction multiplies three guided/actual quantities and compounds their
   errors. `source_type=inference`; treat as a derived feature.
7. **Segment operating-margin guidance is only in the slide decks**, whose text in
   this corpus is an OCR/vision transcription of chart images. Values were
   sanity-checked for smoothness across vintages within each year and against the
   subsequent actual; they are nonetheless a weaker provenance than filing prose.
8. **FY2012 is partial** (only Q2 and Q3 vintages; the corpus begins 2012-05-16)
   and has no `cycle_phase` (no FY2011 revenue). FY2013 A&T sales growth has no
   guidance-vs-actual row because FY2012 A&T segment sales are not in the corpus
   (the earliest 10-K present is FY2015, which reaches back only to FY2013).
9. **Missing by construction, not by omission:**
   * Consolidated revenue-growth guidance exists only for FY2017–FY2019 (12 rows).
     Deere stopped publishing it. There is **no** guided revenue number for
     FY2020–FY2026 — for forecast target #1 you must build revenue bottom-up from
     the segment sales-growth guidance.
   * **Deere has never guided EPS.** There is no EPS guidance series here and none
     exists in the corpus. For forecast target #2, derive it from the net income
     guidance and a share-count assumption.
   * Financial-services net income guidance is absent for the FY2020 Q2/Q3
     vintages (withdrawn during COVID) and for FY2025/FY2026 (the figure moved into
     a slide-only chart in those decks).
   * FY2021 has no `vintage_seq=0` modern-PPA row — see the segment-break note.
10. **Missing data is an absent row or a blank `value`. There are no zeros used as
    "unknown" and no imputed values** anywhere in either file. The only zeros are
    genuine ("~Flat" guidance = 0.0 percent, and `range_width` = 0 for point
    guidance).
11. **`source_type=filing` covers every corpus document**, including
    call-transcript and slide-deck sources, because the mandated vocabulary has no
    transcript/slide value. Check the `source` path to see which kind of document
    a row came from: `filings/` (8-K, 10-Q, 10-K), `call-transcripts/` (prepared
    remarks), `slides/` (earnings-call deck). `inference` marks the three derived
    families (`implied_ppa_operating_profit_*`, `net_income_range_width`, and the
    FY2021 Q1 absolute-to-growth conversion); `api` is not used in
    `de_guidance.csv` because it contains no actuals.
12. **The corpus is the authority.** Where the SEC XBRL API and the corpus could
    both supply a figure, the corpus was used for anything Deere-specific and the
    API only for consolidated actuals — and the two were reconciled (check C).
