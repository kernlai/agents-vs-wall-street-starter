# Deere & Company — legacy segment panel and the legacy→modern segment bridge

**Task:** `de-segments-legacy`
**Data file:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_segments_legacy.csv`
**Built:** 2026-08-16 (corpus frozen 2026-08-14; Deere has **not** reported FY2026 Q3)
**Scripts (reproducible, stdlib-only Python 3):**

| script | purpose |
|---|---|
| `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/de_segments_legacy_extract.py` | parse every segment table in the offline corpus (8-K press releases, 10-Qs, 10-Ks) |
| `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/de_segments_edgar_supplement.py` | pull FY2012–FY2014 original filings from SEC EDGAR (corpus starts 2015-01-14) and parse their segment notes |
| `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/de_segments_legacy_build.py` | merge, cross-validate, compute the bridge, emit the CSV |

Run order: `extract` → `edgar_supplement` → `build`.

---

## 1. What is in the CSV

302 rows, 16 series, tidy long format with the mandated header
`series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes`.

| series_id | n | coverage | units |
|---|---:|---|---|
| `de_at_net_sales_legacy` | 47 | 2011-10-31 … 2020-11-01 | USDm |
| `de_at_operating_profit_legacy` | 47 | 2011-10-31 … 2020-11-01 | USDm |
| `de_cf_net_sales_legacy` | 47 | 2011-10-31 … 2020-11-01 | USDm |
| `de_cf_operating_profit_legacy` | 47 | 2011-10-31 … 2020-11-01 | USDm |
| `de_at_operating_profit_legacy_asu201707` | 6 | 2016-10-31 … 2017-10-29 | USDm |
| `de_cf_operating_profit_legacy_asu201707` | 6 | 2016-10-31 … 2017-10-29 | USDm |
| `de_ppa_net_sales_restated` | 6 | 2019-11-03 … 2020-11-01 | USDm |
| `de_ppa_operating_profit_restated` | 6 | 2019-11-03 … 2020-11-01 | USDm |
| `de_sat_net_sales_restated` | 6 | 2019-11-03 … 2020-11-01 | USDm |
| `de_sat_operating_profit_restated` | 6 | 2019-11-03 … 2020-11-01 | USDm |
| `de_cf_net_sales_restated` | 6 | 2019-11-03 … 2020-11-01 | USDm |
| `de_cf_operating_profit_restated` | 6 | 2019-11-03 … 2020-11-01 | USDm |
| `de_bridge_ppa_share_of_at_net_sales` | 6 | 2019-11-03 … 2020-11-01 | ratio |
| `de_bridge_ppa_share_of_at_operating_profit` | 6 | 2019-11-03 … 2020-11-01 | ratio |
| `de_ppa_share_of_ag_net_sales_modern` | 27 | 2021-01-31 … 2026-05-03 | ratio |
| `de_ppa_share_of_ag_operating_profit_modern` | 27 | 2021-01-31 … 2026-05-03 | ratio |

Each of the four legacy series carries **37 quarterly observations (FY2011 Q4, then FY2012 Q1
through FY2020 Q4 with no gaps) plus 10 fiscal-year observations (FY2011–FY2020)**.

### Reading the file

* **`segment_basis` and `as_reported_or_restated` are in `notes`**, not in their own columns —
  the nine-column header is fixed by the task spec. They are always the first two
  `key=value;` pairs of every segment row, so they are trivially machine-parsable:
  `segment_basis=legacy-AT|modern-PPA|bridge; as_reported_or_restated=as_reported|as_reported_comparative|restated|derived; …`
  The basis is *also* encoded in the `series_id` suffix (`_legacy`, `_restated`, `_asu201707`,
  `_modern`) so a model can never silently pool the two eras.
* **Quarterly and annual observations share a `series_id`.** Filter `fiscal_quarter != 'FY'`
  for a quarterly panel. Q4 and FY rows share a `period_end` (they end on the same day) and are
  distinguished only by `fiscal_quarter`. The unique key is
  `(series_id, period_end, fiscal_quarter)` — verified to have no duplicates.
* `as_reported_comparative` means the value was only ever printed as a prior-year comparative
  column in a later filing, never as an "as reported this quarter" figure in the corpus/EDGAR
  documents pulled. It is still the company's own number, just captured one filing downstream.

---

## 2. The bridge — the central result

Deere reorganised in fiscal 2021: the single **Agriculture & Turf** segment was split into
**Production & Precision Ag (PPA)** and **Small Ag & Turf (SAT)**. Construction & Forestry and
Financial Services were unchanged. Deere recast prior periods "for a consistent presentation"
(FY2021 Q1 10-Q, Note 1).

Deere disclosed **exactly six periods on both bases**. Nothing else exists.

| period | period_end | A&T sales | PPA sales | SAT sales | resid | A&T op | PPA op | SAT op | resid | PPA sales share | PPA op share |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FY2019 | 2019-11-03 | 23,666 | 13,364 | 10,302 | **0** | 2,506 | 1,729 | 777 | **0** | 0.5647 | 0.6899 |
| FY2020 Q1 | 2020-02-02 | 4,486 | 2,507 | 1,979 | **0** | 373 | 218 | 155 | **0** | 0.5588 | 0.5845 |
| FY2020 Q2 | 2020-05-03 | 5,968 | 3,365 | 2,603 | **0** | 794 | 568 | 226 | **0** | 0.5638 | 0.7154 |
| FY2020 Q3 | 2020-08-02 | 5,672 | 3,289 | 2,383 | **0** | 942 | 605 | 337 | **0** | 0.5799 | 0.6423 |
| FY2020 Q4 | 2020-11-01 | 6,198 | 3,801 | 2,397 | **0** | 860 | 578 | 282 | **0** | 0.6133 | 0.6721 |
| FY2020 | 2020-11-01 | 22,325 | 12,962 | 9,363 | **0** | 2,969 | 1,969 | 1,000 | **0** | 0.5806 | 0.6632 |

`resid = PPA + SAT − A&T`. **It is exactly zero in all six periods, for both sales and operating
profit.** The split is a pure partition — no reallocation to or from Construction & Forestry,
no residual "other". Restated C&F equals legacy C&F to the dollar in every overlap period
(e.g. FY2020 8,947 both ways; FY2020 Q4 2,461 both ways). So the mapping is a clean one-to-two
decomposition and the only unknown is **the split fraction**.

**Sources** (corpus-relative; the filing chosen per period is the earliest as-reported one, and
every value below was also confirmed against at least one other document in the corpus):

| period | legacy A&T source | restated PPA/SAT source |
|---|---|---|
| FY2019 | `filings/2019-11-27__de-us-20191127-q4-8k__469218.md` | `filings/2021-11-24__de-us-20211124-q4-10k__131650.md` |
| FY2020 Q1 | `filings/2020-02-21__de-us-20200221-q1-10q__468373.md` | `filings/2021-02-19__de-us-20210219-q1-10q__105814.md` |
| FY2020 Q2 | `filings/2020-05-21__de-us-20200521-q2-10q__469470.md` | `filings/2021-05-21__de-us-20210521-q2-10q__105821.md` |
| FY2020 Q3 | `filings/2020-08-20__de-us-20200820-q3-10q__105822.md` | `filings/2021-08-20__de-us-20210820-q3-10q__105837.md` |
| FY2020 Q4 | `filings/2020-11-25__de-us-20201125-q4-8k__105817.md` | `filings/2021-11-24__de-us-20211124-q4-8k__105843.md` |
| FY2020 | `filings/2020-11-25__de-us-20201125-q4-8k__105817.md` | `filings/2021-11-24__de-us-20211124-q4-10k__131650.md` |

The FY2019/FY2020 restated annual figures also appear, identically, in the three-year
`OPERATING SEGMENTS` table of `filings/2021-12-16__de-us-20211216-fy-10k__645298.md`.
Every CSV bridge row names both of its source documents.

### Is the fraction stable?

Inside the six-period window it looks stable — deceptively so.

| | n | mean | sd | min | max | CV |
|---|---:|---:|---:|---:|---:|---:|
| PPA share of A&T **net sales**, quarterly (FY2020 Q1–Q4) | 4 | 0.5790 | 0.0246 | 0.5588 | 0.6133 | 4.2% |
| PPA share of A&T **operating profit**, quarterly | 4 | 0.6535 | 0.0550 | 0.5845 | 0.7154 | 8.4% |
| PPA share of A&T net sales, annual (FY2019, FY2020) | 2 | 0.5726 | 0.0113 | 0.5647 | 0.5806 | 2.0% |
| PPA share of A&T operating profit, annual | 2 | 0.6766 | 0.0189 | 0.6632 | 0.6899 | 2.8% |

Four quarterly observations, all inside a single fiscal year, is not enough to establish
stationarity. So I tested the fraction forward, on FY2021–FY2026 Q2 where the true PPA/SAT split
is observed (`de_ppa_share_of_ag_*_modern` in the CSV):

* Net sales share: **mean 0.6223, sd 0.0422, range 0.5496 → 0.6924** over 22 quarters.
* Operating profit share: **mean 0.6726, sd 0.1242, range 0.4149 → 0.9603** over 22 quarters.

The sales share rose from ~0.55 in FY2021 to ~0.69 at the FY2023 peak and fell back to ~0.56 by
FY2026 Q2. That is **not noise — it is the large-ag cycle**. PPA is the big-iron business
(large tractors, combines, sprayers); SAT is dairy/livestock/turf, which is structurally less
cyclical. Correlation of the share with the level of A&T (PPA+SAT) sales across FY2021+
quarters: **r = 0.52 for the sales share, r = 0.40 for the operating-profit share**. The ratio is
pro-cyclical, and the FY2019–FY2020 window happens to sit near a cyclical trough, so the
measured ratio is biased low relative to the full cycle.

### How reliable would a back-cast be? (out-of-sample test)

Apply the bridge ratios measured in the FY2019–FY2020 window to the FY2021–FY2026 periods where
true PPA is known:

| back-cast | mean error | MAPE | worst quarter |
|---|---:|---:|---:|
| PPA net sales, quarterly (ratio 0.5790) | −6.5% | **7.8%** | −16.4% (FY2023 Q4) |
| PPA operating profit, quarterly (ratio 0.6535) | +0.9% | **15.9%** | +57.5% (FY2026 Q1) |
| PPA net sales, annual (ratio 0.5726) | −8.8% | **8.8%** | −12.9% (FY2023) |
| PPA operating profit, annual (ratio 0.6766) | −2.3% | **5.9%** | +9.2% (FY2021) |

**Verdict.**

* A **net-sales back-cast is usable with care.** ~8% MAPE and a systematic ~6–9% *understatement*
  in strong years. Good enough to establish the shape and cyclical amplitude of a synthetic
  pre-2021 PPA revenue series; not good enough to treat any single back-cast quarter as an
  observation. If you use it, use `0.58` and expect to be low in booms and high in busts, or make
  the ratio a function of the ag cycle rather than a constant.
* An **operating-profit back-cast is not usable at the quarterly level.** 16% MAPE, errors up to
  +58%, and a share that ranged 0.41–0.96 in the observed era. Operating margin dispersion between
  PPA and SAT is much wider than revenue dispersion, and it inverts: in weak quarters (FY2022 Q1,
  FY2026 Q1) SAT can out-earn its revenue weight and the constant-ratio back-cast blows up.
  At the annual level it degrades more gracefully (~6% MAPE), so an annual synthetic PPA operating
  profit is defensible as a covariate, never as a target.

**Where the back-cast breaks, concretely:**

1. **Cyclical turning points.** The ratio moves with the large-ag cycle (r≈0.5). At peaks and
   troughs the constant ratio is worst.
2. **Any quarter where SAT operating profit approaches zero or goes negative.** The share becomes
   unstable or undefined; FY2025 Q4 (share 0.96) and FY2026 Q1 (0.41) are live examples.
3. **Pre-FY2018 periods.** The legacy A&T operating profit definition changed in FY2018
   (see §4). Applying a FY2019/FY2020 ratio to pre-FY2018 A&T operating profit mixes a
   definitional break into a structural break.
4. **FY2013 and earlier.** A&T then included businesses and a geographic mix that Deere never
   mapped onto PPA/SAT. The recast Deere published only reaches back to FY2019. Anything before
   that is extrapolation of an extrapolation.
5. **Seasonality.** Q1 and Q4 shares differ systematically from Q2/Q3 (Q4 FY2020 0.6133 vs Q1
   FY2020 0.5588). A single annual ratio applied to quarters imports a seasonal error.

If a synthetic pre-2021 PPA series is needed, my recommendation is: back-cast **net sales only**,
at **annual** frequency, with ratio 0.573, carry an explicit ±10% uncertainty band, mark every
such row `source_type=estimate`, and never mix it into the same series_id as observed PPA.

---

## 3. Method

**Scripted, not transcribed.** No number in the CSV was typed by hand. Two parsers:

1. *Corpus parser.* Locates the `| Net sales and revenues:` … `| Operating profit: *` block in
   each 8-K press release and 10-Q, and the three-year `| OPERATING SEGMENTS` table in each 10-K.
   Numeric tokens are separated from percent-change tokens by sign (Deere always signs the
   %-change column, `+22` / `−25`, and never signs a value; negative values appear in
   parentheses). Segment labels are matched on a "squeezed" alphabetic key so the ~8 typographic
   variants in the corpus (`Agriculture and turf`, `Production &precision ag`,
   `Production &PrecisionAg net sales`, …) collapse onto one code.
   Column positions: `[current quarter, prior-year quarter]` for Q1 filings, plus
   `[YTD current, YTD prior]` for Q2/Q3/Q4 — the Q4 YTD pair is the full fiscal year.
2. *EDGAR parser.* The offline corpus begins 2015-01-14, so its earliest quarterly segment
   figures are FY2015 Q1 with FY2014 Q1 as the comparative. FY2011–FY2013 quarterly detail was
   pulled from the original filings on SEC EDGAR (three FY2013 10-Qs, two FY2014 10-Qs, and the
   FY2012/FY2013/FY2014 Q4 8-K EX-99.1 press releases) and parsed with an `html.parser`-based
   table extractor. This added 44 observations that the corpus cannot supply.

**Prior-year comparative columns were mined deliberately.** Each filing carries the same period
twice — once as "current" and once, a year later, as "comparative". That gives free redundancy
and it is how the pre-corpus periods and the restated FY2020 quarters were obtained.

---

## 4. Validation

Every check below is executed by the scripts and printed on each run.

| check | result |
|---|---|
| Segment net sales sum to the printed "Total net sales", every parsed column | **0 failures** |
| Segment + Financial Services operating profit sums to "Total operating profit", every parsed column | **0 failures** |
| 10-K annual tables: segments + FS revenues + other revenues = printed Total | **0 failures** |
| Same value parsed from ≥2 corpus documents (8-K vs 10-Q vs later comparative) | **857 agreements, 0 unresolved conflicts** |
| Corpus values re-derived independently from original EDGAR HTML filings | **44 values, 0 conflicts** (incl. all of FY2014 Q1/Q2/Q4, FY2013 FY, FY2014 FY) |
| Press-release "Total net sales and revenues" vs SEC XBRL `us-gaap:Revenues` (companyconcept API, CIK 315189) | **39/39 quarters agree exactly** (2015-04-30 … 2026-05-03) |
| Sum of four quarters vs the fiscal-year row, all four legacy series, FY2012–FY2020 | **agrees within ±2 USDm** (Deere rounds each period to $1m independently) |
| Bridge reconciliation PPA+SAT−A&T | **exactly 0 in all 6 overlap periods, sales and operating profit** |
| Duplicate `(series_id, period_end, fiscal_quarter)` keys | **none** |
| Zero values used as a stand-in for missing data | **none** (missing data is an absent row) |

The independent sources are genuinely independent: the XBRL API serves tagged facts from
Deere's own XBRL exhibits, while the corpus rows come from the narrative HTML/markdown of the
same filings, and the EDGAR supplement re-parses raw 1990s-style HTML tables that were never in
the corpus at all.

### Discrepancies found (none silently resolved)

1. **ASU 2017-07 restatement of operating profit — 12 values.** Deere adopted ASU 2017-07 in
   FY2018 Q1, retrospectively for the presentation of operating profit: only the *service cost*
   component of pension/OPEB stays in operating profit. FY2016 and FY2017 operating profit were
   restated **upward**:

   | period | as originally reported | restated | restated in |
   |---|---:|---:|---|
   | FY2016 FY, A&T | 1,700 | 1,719 | FY2018 10-K |
   | FY2016 FY, C&F | 180 | 189 | FY2018 10-K |
   | FY2017 Q1, A&T / C&F | 213 / 34 | 218 / 37 | FY2018 Q1 8-K & 10-Q |
   | FY2017 Q2, A&T / C&F | 1,003 / 108 | 1,009 / 111 | FY2018 Q2 8-K & 10-Q |
   | FY2017 Q3, A&T / C&F | 685 / 110 | 693 / 111 | FY2018 Q3 8-K & 10-Q |
   | FY2017 Q4, A&T / C&F | 584 / 85 | 594 / 86 | FY2018 Q4 8-K |
   | FY2017 FY, A&T / C&F | 2,484 / 337 | 2,513 / 346 | FY2018 Q4 8-K & 10-K |

   Both versions are in the CSV: the as-reported value in
   `de_{at,cf}_operating_profit_legacy`, the restated value in
   `de_{at,cf}_operating_profit_legacy_asu201707`. **Deere never restated FY2015 or earlier.**
   That means the legacy operating-profit series has a *definitional* break at FY2018 that is
   independent of the FY2021 *structural* break, and it cannot be repaired for FY2011–FY2015 from
   any disclosure in the corpus or on EDGAR.

2. **Fiscal-calendar relabelling.** Deere moved to a 52/53-week fiscal year ending the last
   Sunday of the period, effective fiscal 2017, and retroactively restated the *dates*: the
   FY2017 10-K states FY2016 ended 2016-10-30 and FY2015 ended 2015-11-01, although the FY2015
   and FY2016 filings themselves are headed "October 31". `period_end` in the CSV uses the label
   printed in the original filing (so FY2016 Q4 is `2016-10-31`); the alternative date is flagged
   in `notes`. Deere never republished 52/53-week *quarter* ends for FY2016 and earlier, so no
   better mapping exists. Affects FY2016 and earlier only.

---

## 5. What could not be obtained

* **No PPA/SAT figures before FY2019.** Deere recast FY2019 and FY2020 only. There is no
  quarterly recast for FY2019 (only the fiscal-year total), so the quarterly bridge rests on
  **four observations, all in FY2020**. This is the single biggest limitation of the bridge.
* **No FY2011 Q1–Q3.** The FY2012 Q4 press release supplies FY2011 Q4 and FY2011 FY as
  comparatives; the FY2012 10-Qs were not fetched, so FY2011 Q1–Q3 are absent rows, not zeros.
* **No FY2013 Q3 comparative confirmation.** FY2013 Q3 is single-sourced (its own 10-Q on
  EDGAR); the FY2014 Q3 10-Q was not fetched. All other quarters FY2012–FY2020 are at least
  double-sourced.
* **No sub-segment (geographic or product-line) split** of A&T. Deere disclosed
  "outside the U.S. and Canada" equipment sales and operating profit but never a segment ×
  geography grid, so the A&T→PPA split cannot be modelled from geographic mix.
* **Pre-FY2016 operating profit on the modern (ASU 2017-07) definition** — never published.
* **Segment data is not in the XBRL companyconcept/companyfacts API.** Those endpoints return
  only non-dimensional facts, so the segment figures had to come from filing text. XBRL was used
  for consolidated cross-checks only.

## 6. Caveats a modeller must carry

1. **Never pool `*_legacy` with `*_restated` or with modern PPA/SAT series.** They measure
   different things. The `series_id` suffix and `notes` `segment_basis=` key both mark this.
2. **Two breaks, not one.** FY2021 structural (A&T → PPA + SAT) *and* FY2018 definitional
   (ASU 2017-07 pension presentation, operating profit only). A dummy at FY2021 alone is not
   enough.
3. **Wirtgen.** Acquired 2017-12-01 and consolidated into Construction & Forestry, initially with
   a one-month reporting lag. C&F net sales roughly double between FY2017 (5,718) and FY2018
   (10,160); that is acquisition, not organic growth. The lag was eliminated in FY2021 Q1, adding
   a one-off $270m to C&F net sales in that quarter (FY2021 Q1 10-Q); prior periods were not
   restated. Flagged in the notes of every FY2018+ C&F row.
4. **FY2019 was a 53-week year** (ended 2019-11-03); Q4 FY2019 contained 14 weeks. Do not treat
   it as a normal quarter in a seasonal model.
5. **Q4 and FY rows share a `period_end`.** Filter on `fiscal_quarter`.
6. **Bridge ratios are `source_type=inference`**, derived by the build script — they are not
   figures Deere published. The inputs are, and both source documents are named per row.
7. **FY2011–FY2013 rows use calendar month-end `period_end` labels**, which is what the filings
   of the day used.
8. **Metadata trap avoided.** `INDEX.md` lists a row "2026-05-21 | Call Transcript | Q3 2026"
   (`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`). It is dated the same day
   as the Q2 FY2026 earnings release and is Q2 material, mislabelled. No transcript was used as a
   data source for this file in any case — every value comes from a filing table.
9. **Nothing in this file is FY2026 Q3 data.** The latest observation of any kind is
   2026-05-03 (FY2026 Q2), from the FY2026 Q2 filings.
