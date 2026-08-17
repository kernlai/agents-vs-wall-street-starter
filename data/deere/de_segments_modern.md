# Deere & Company — modern-basis segment panel (`de_segments_modern.csv`)

Built 2026-08-16. Corpus frozen 2026-08-14. **Deere has not reported FY2026 Q3; the panel
ends at FY2026 Q2 (period end 2026-05-03).**

## What is in the file

Tidy long CSV, header exactly:

```
series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes
```

297 data rows, 9 series × 33 observations each.

| series_id | units | quarterly obs | annual (FY) obs | range |
|---|---|---|---|---|
| `de_ppa_net_sales` | USDm | 26 | 7 | 2020-02-02 → 2026-05-03 |
| `de_ppa_operating_profit` | USDm | **26** | 7 | 2020-02-02 → 2026-05-03 |
| `de_ppa_operating_margin` | percent | 26 | 7 | 2020-02-02 → 2026-05-03 |
| `de_sat_net_sales` | USDm | 26 | 7 | 2020-02-02 → 2026-05-03 |
| `de_sat_operating_profit` | USDm | 26 | 7 | 2020-02-02 → 2026-05-03 |
| `de_sat_operating_margin` | percent | 26 | 7 | 2020-02-02 → 2026-05-03 |
| `de_cf_net_sales` | USDm | 26 | 7 | 2020-02-02 → 2026-05-03 |
| `de_cf_operating_profit` | USDm | 26 | 7 | 2020-02-02 → 2026-05-03 |
| `de_cf_operating_margin` | percent | 26 | 7 | 2020-02-02 → 2026-05-03 |

`fiscal_quarter` is `Q1|Q2|Q3|Q4` for the three-month observations and `FY` for the
annual ones. **A `Q4` row and an `FY` row share the same `period_end`** (Deere's Q4 and
fiscal-year both end on the same date) — filter on `fiscal_quarter` before doing anything
time-series-like, or you will double-count the fourth quarter.

### `de_ppa_operating_profit` — the forecast target

**26 quarterly observations obtained.**

- 22 as-reported: FY2021 Q1 (period end 2021-01-31) → FY2026 Q2 (2026-05-03). This is the
  full modern-basis history; PPA first appears in the 2021-02-19 Q1 FY2021 filings.
- 4 restated: FY2020 Q1–Q4, recovered from the prior-year comparative columns of the
  FY2021 quarterly earnings releases. These are Deere's own recast of FY2020 onto the
  three-segment basis; they were never reported contemporaneously.
- Plus 7 annual `FY` rows (FY2019 → FY2025). FY2019 and FY2020 annual are restated;
  FY2019 exists **only** at annual frequency — Deere never published restated FY2019
  quarters on the PPA basis, so there is no FY2019 quarterly segment data anywhere.

## Segment basis / structural break

Every row's `notes` field carries `segment_basis=modern-PPA` and
`as_reported_or_restated=as-reported|restated`. 242 rows are as-reported, 55 restated.

- Before FY2021 Deere reported a single **Agriculture & Turf** segment (`legacy-AT`).
  Nothing on that basis is in this file — it belongs in a separate legacy-basis file and
  must not be concatenated with these series without an explicit break dummy.
- The FY2021 reorganisation split Agriculture & Turf into **Production & Precision Ag
  (PPA)** and **Small Agriculture & Turf (SAT)**. **Construction & Forestry (CF) was not
  reorganised**, so CF is in principle continuous across the FY2021 boundary — but Deere
  also moved goodwill out of identifiable segment assets at the start of FY2021 and
  recast prior periods, so CF figures here are still the recast presentation. Treat CF
  continuity as likely-but-unverified rather than given.
- **The restatement is an exact partition, and this is checkable.** At FY2019 the
  legacy-AT figures as originally reported in the FY2019 Q4 8-K reconcile to the recast
  figures with zero residual:

  | FY2019 annual | legacy-AT as reported | restated modern basis | residual |
  |---|---|---|---|
  | A&T net sales vs PPA + SAT | 23,666 | 13,364 + 10,302 = 23,666 | 0 |
  | A&T operating profit vs PPA + SAT | 2,506 | 1,729 + 777 = 2,506 | 0 |
  | CF net sales | 11,220 | 11,220 | 0 |
  | CF operating profit | 1,215 | 1,215 | 0 |

  So the FY2021 reorganisation split Agriculture & Turf cleanly in two with no
  reallocation to or from Construction & Forestry, and no change to the totals. That is
  useful: it means a legacy-AT series can be spliced to `de_ppa + de_sat` as a combined
  "agriculture & turf" aggregate without a level break. It does **not** mean PPA alone
  can be extended backwards — the split of A&T into PPA and SAT is only observable from
  FY2019 onward (annual) and FY2020 onward (quarterly).

## A second, quieter structural break: ASU 2023-07

From FY2025 Deere adopted **ASU 2023-07 (Segment Reporting Topic 280)** and rebuilt the
segment footnote around "External net sales", "Cost of sales", "Other segment items" and
"Segment operating profit". The reported *values* for net sales and operating profit are
unchanged in definition — verified: the FY2025 10-K's ASU-format annual table agrees
12/12 with the Q4 FY2025 8-K's "Years Ended" columns. But the surrounding line items and
the XBRL tagging changed, so anything you build on the footnote's *other* rows breaks at
FY2025 Q1.

## Sources and method

**Primary source: the quarterly 8-K earnings releases in the offline corpus**
(`filings/*-q[1-4]-8k*.md`), which contain a clean "\<QUARTER\> PRESS RELEASE" segment
table with, per segment, three-month net sales and three-month operating profit for the
current and prior-year quarter, plus YTD (and, in Q4, "Years Ended") columns.

Nothing was transcribed by hand. Two scripts, standard library only:

- `scripts/data/parse_de_segments_modern.py` — parses 22 modern 8-Ks, the FY2021 10-K
  annual segment table, and the 10-Q/10-K segment footnotes; writes the CSV; prints the
  full validation report.
- `scripts/data/validate_de_segments_vs_edgar.py` — re-derives the same numbers from
  **SEC EDGAR** and reports agreement.

Source of record per row is in the `source` column as a corpus-relative path.

### Definition of "segment net sales"

`de_*_net_sales` is **external segment net sales** as presented in the earnings-release
segment table. It is *not* "total segment net sales and revenues", which additionally
includes segment finance and interest income, other income and intersegment income (for
PPA in FY2026 Q2: 4,503 external vs 4,612 total). The operating-margin series uses
external net sales as the denominator, matching how Deere quotes segment margin.

## Validation

Six in-corpus checks plus one external check; all pass.

| # | Check | Result |
|---|---|---|
| 1 | Filing's own "% Change" column vs recomputed change, every segment row of every modern 8-K | **131/131** agree within 1pp |
| 2 | Prior-year comparative column vs the as-reported value published a year earlier (detects silent restatement) | **0 disagreements** out of 131 comparisons |
| 3 | 10-Q / 10-K segment footnote (separately filed document, both pre- and post-ASU layouts) vs the 8-K press-release table | **216/216** agree |
| 4 | FY2021 10-K annual segment table vs FY2021 Q4 8-K "Years Ended" columns | **12/12** agree |
| 4b | FY2025 10-K (ASU 2023-07 layout) annual table vs FY2025 Q4 8-K annual columns | **12/12** agree |
| 5 | Sum of Q1..Q4 vs the reported fiscal-year figure, 36 segment-years | 18 exact, 18 off by exactly 1 USDm, **0 real differences** |
| 6 | Basis bridge: legacy-AT FY2019 as originally reported vs restated PPA+SAT and CF | **4/4** reconcile exactly (residual 0) |

**External (out-of-corpus) validation — SEC EDGAR.** `data.sec.gov`'s
`companyconcept` / `companyfacts` APIs return only non-dimensional facts, so segment
values are *not* retrievable there (verified: `us-gaap/OperatingIncomeLoss` for CIK
315189 returns 178 consolidated facts and no segment dimension). Segment-dimensioned
facts were instead read from the XBRL "Financial Report" R-files that EDGAR renders from
each filing's instance document (`FilingSummary.xml` → `R##.htm`).

> **204/204 values agree**, across 17 filings, covering 20 of the 26 quarter-ends for all
> six USDm series (2020-02-02 → 2026-05-03). Zero mismatches.

The 6 uncovered quarter-ends are the Q4s (FY2020–FY2025): Deere files no 10-Q for Q4, and
the 10-K reports twelve-month columns only, so the fourth quarter exists as a discrete
three-month figure **only** in the Q4 8-K press release. Those six are covered indirectly
by check 5 (Q1+Q2+Q3+Q4 reconciles to the independently-validated annual, to the rounding
tolerance).

## Caveats a modeller must know

1. **Never pool `de_ppa_*` or `de_sat_*` with pre-FY2021 Agriculture & Turf data.** The
   `notes` field marks the basis on every row for exactly this reason. The one splice
   that *is* legitimate is legacy-AT ↔ (`de_ppa` + `de_sat`) as a combined aggregate —
   see the basis-bridge table above.
2. **`Q4` and `FY` rows share a `period_end`.** Always filter `fiscal_quarter`.
3. **FY2020 quarters are restated, not as-reported.** They were published as
   comparatives, after the fact, by a company with an incentive to present a clean
   trend. They are internally consistent (they sum to the reported FY2020 annual) but
   they were never subject to a contemporaneous earnings-release news cycle. If your
   model uses surprise-vs-consensus or any reported-at-the-time construct, the four
   FY2020 quarters are not comparable to the 22 as-reported ones. Consider dropping them
   or adding a `restated` dummy.
4. **FY2019 is annual only.** No restated FY2019 quarters exist.
5. **Operating margin is derived, not reported.** `source_type=inference`. It is
   operating profit ÷ external segment net sales × 100, computed from the two rounded
   USDm figures, so it carries their rounding (roughly ±0.02pp at typical magnitudes).
   Deere quotes segment margins in its slides on the same definition, and spot checks
   match (PPA FY2025 15.4% in the 2Q 2026 deck vs 2,671/17,311 = 15.43% here).
6. **All USDm values are rounded to whole millions by Deere.** Four quarters summed can
   miss the reported annual by 1 — 18 of 36 segment-years do. That is the filings'
   rounding, not a parsing error, and the file preserves the filings' figures rather
   than forcing them to reconcile.
7. **No FY2026 Q3 data of any kind is in this file.** `INDEX.md` has a row labelled
   "2026-05-21 | Call Transcript | Q3 2026" — that document is dated the same day as Q2
   FY2026 earnings and is mislabelled Q2 material. It was not used, and nothing in the
   corpus contains FY2026 Q3 actuals.
8. **Financial Services is deliberately excluded.** It is a fourth reportable segment but
   was not requested, and its operating profit is defined differently (it includes
   interest expense and FX).
9. **`period_end` is the fiscal period end, not the filing date.** The Q2 FY2026 quarter
   ends 2026-05-03 but was not public until 2026-05-21. Any backtest must lag by the
   announcement date, which is the date prefix of the `source` file path.
10. **The 2024-02-15 Q1 FY2024 8-K prints no "% Change" for CF net sales** (3,212 vs
    3,203 rounds to 0%). Both values were captured correctly; only check 1 skips that
    single cell, which is why it reports 131 and not 132 comparisons.

## What could not be obtained

- FY2019 and earlier **quarterly** segment data on the modern PPA basis. It does not
  exist — Deere recast FY2019 only at annual frequency, and FY2018 and earlier not at all.
- FY2026 Q3 anything (not yet reported as of today, 2026-08-16).
- Segment data via the SEC XBRL JSON APIs (structurally unavailable — dimensions are not
  exposed; the R-file route was used instead).
- An EDGAR cross-check of the six Q4 three-month figures (no Q4 10-Q exists; covered
  indirectly via the annual reconciliation).

## Reproduce

```bash
python3 scripts/data/parse_de_segments_modern.py          # writes the CSV + checks 1-5
python3 scripts/data/validate_de_segments_vs_edgar.py     # external SEC EDGAR check
```
