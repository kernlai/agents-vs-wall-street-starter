# Deere & Company — segment x geography revenue matrix (ASC 606 footnote)

Companion to `de_geo_segment_matrix.csv`.

- **Built:** 2026-08-16, from the frozen offline corpus
  (`challenge/offline-data/deere`, 310 docs, frozen 2026-08-14).
- **Parser:** `scripts/data/de_parse_revrec_matrix.py` (extraction + validation)
  and `scripts/data/de_build_geo_matrix.py` (cross-source merge, derivation, CSV).
  Standard library only; no figure was transcribed by hand.
- **Rows:** 3,354. **Filings used:** 32 (10-Q and 10-K), plus 495 derived rows.
- **There is no Q3 FY2026 data here, and none exists.** Deere reports Q3 FY2026 on
  20 August 2026. The latest actuals in the corpus are Q2 FY2026 (quarter ended
  2026-05-03). The corpus `INDEX.md` row labelled
  `2026-05-21 | Call Transcript | Q3 2026` is mislabelled — it is the Q2 FY2026 call.

## What the data is

The "Revenue Recognition" note of each 10-Q and 10-K (note 3 in the current
10-Q layout, note 4 in the FY2019–FY2021 10-Qs, note 6 in the 10-K) discloses
*revenue from contracts with customers* disaggregated three ways: by primary
geographic market, by major product line, and by timing of recognition. Only the
first two are captured here.

### BASIS WARNING — read before using any number

`basis = rev-rec` throughout. **This is revenue from contracts with customers and
does not tie to segment net sales in the 8-K / segment tables.** The gap is
persistent and material:

| Period | | rev-rec (this file) | 8-K segment net sales | gap | gap % |
|---|---|--:|--:|--:|--:|
| Q2 FY2026 | PPA | 4,607 | 4,503 | +104 | +2.3% |
| Q2 FY2026 | SAT | 3,542 | 3,485 | +57 | +1.6% |
| Q2 FY2026 | CF | 3,854 | 3,790 | +64 | +1.7% |
| FY2025 | PPA | 17,749 | 17,311 | +438 | +2.5% |
| FY2025 | SAT | 10,464 | 10,224 | +240 | +2.3% |
| FY2025 | CF | 11,650 | 11,382 | +268 | +2.4% |

Never mix the two bases in one series. If a forecast is built on the geographic
mix here, bridge back to segment net sales with a scaling factor of roughly
0.975–0.985 per equipment segment, and state that you did.

## Schema

`series_id,period_end,fiscal_year,fiscal_quarter,segment,geography,product_line,value,units,basis,source,notes`

- `series_id` = `de_revrec_net_sales`, `units` = `USDm`, `basis` = `rev-rec`.
- `fiscal_quarter` is `Q1`–`Q4` for **three-month** figures and `H1` / `9M` / `FY`
  for the cumulative columns as disclosed. **Only `Q1`–`Q4` rows are quarterly.**
  Never sum a `Qn` row with an `H1`/`9M`/`FY` row.
- Geography rows have `geography` set and `product_line` empty; product-line rows
  have `product_line` set and `geography` empty. They are two views of the same
  total, not additive with each other.
- `segment = Total` and `geography = Total` rows are Deere's own disclosed totals.
  They are kept because they are the reconciliation anchors. Do not re-sum them
  with the cells.
- Missing data is an absent row. There are no zeros standing in for unknowns.

## Coverage

The matrix exists only from Deere's ASC 606 adoption in fiscal 2019.

| Segment scheme | Quarters (three-month) | Cumulative columns |
|---|---|---|
| Pre-FY2021 (`A&T` / `C&F` / `FS`) | FY2019 Q1–Q4, FY2020 Q1–Q4 | H1/9M/FY FY2019, FY2020 |
| Current (`PPA` / `SAT` / `CF` / `FS`) | FY2020 Q1–Q4 … FY2025 Q1–Q4, FY2026 Q1–Q2 | H1/9M/FY FY2019(FY only)–FY2025, H1 FY2026 |

**34 distinct quarters** on a three-month basis (26 on the current segment scheme,
8 on the pre-FY2021 scheme), plus 26 cumulative period columns.

Deere restated FY2019 and FY2020 into PPA/SAT/CF when the Smart Industrial
structure took effect in FY2021, so FY2020 appears on **both** schemes and FY2019
appears on the old scheme quarterly plus the new scheme at full-year only. There
are no FY2019 quarters on the current segment scheme — Deere never published them.

Geography labels: the sixth market was "Asia, Africa, Australia, New Zealand, and
Middle East" through FY2022 and "Asia, Africa, Oceania, and Middle East"
afterwards. The CSV uses the current label throughout; it is the same market
definition.

## Reconciliation — the quality gate

Every cell in every retained block was checked twice: each geography row must sum
to its stated row total, and each segment column must sum to its stated column
total. Blocks that failed were rejected outright, never patched into shape.

- **275 candidate tables parsed; 255 reconciled; 20 rejected.**
- **Every one of the 51 disclosed period-columns has at least one fully
  reconciling source. Zero periods failed.**
- **Cross-source conflicts: 0.** Most periods appear in two to five different
  filings (original disclosure plus prior-year comparatives). All 1,825 cells that
  appear in more than one filing agree to the dollar across every filing that
  reports them; 1,034 cells have a single source.
- Re-running the reconciliation on the finished CSV: **60 period-blocks
  (34 quarters + 26 cumulative), 0 failures.**

Per-period detail (`sources` = filings disclosing it, `reconciled` = how many of
those parsed cleanly):

```
  old  FY2019 Q1  2019-01-27   sources=3  reconciled=3  PASS
  old  FY2019 H1  2019-04-28   sources=3  reconciled=3  PASS
  old  FY2019 Q2  2019-04-28   sources=4  reconciled=4  PASS
  old  FY2019 9M  2019-07-28   sources=3  reconciled=3  PASS
  old  FY2019 Q3  2019-07-28   sources=3  reconciled=3  PASS
  new  FY2019 FY  2019-11-03   sources=1  reconciled=1  PASS
  old  FY2019 FY  2019-11-03   sources=3  reconciled=2  PASS
  new  FY2020 Q1  2020-02-02   sources=1  reconciled=1  PASS
  old  FY2020 Q1  2020-02-02   sources=2  reconciled=2  PASS
  new  FY2020 H1  2020-05-03   sources=2  reconciled=2  PASS
  old  FY2020 H1  2020-05-03   sources=2  reconciled=2  PASS
  new  FY2020 Q2  2020-05-03   sources=1  reconciled=1  PASS
  old  FY2020 Q2  2020-05-03   sources=2  reconciled=2  PASS
  new  FY2020 9M  2020-08-02   sources=2  reconciled=2  PASS
  old  FY2020 9M  2020-08-02   sources=1  reconciled=1  PASS
  new  FY2020 Q3  2020-08-02   sources=1  reconciled=1  PASS
  new  FY2020 FY  2020-11-01   sources=3  reconciled=1  PASS
  old  FY2020 FY  2020-11-01   sources=1  reconciled=1  PASS
  new  FY2021 Q1  2021-01-31   sources=2  reconciled=1  PASS
  new  FY2021 H1  2021-05-02   sources=2  reconciled=2  PASS
  new  FY2021 Q2  2021-05-02   sources=3  reconciled=3  PASS
  new  FY2021 9M  2021-08-01   sources=4  reconciled=3  PASS
  new  FY2021 Q3  2021-08-01   sources=3  reconciled=3  PASS
  new  FY2021 FY  2021-10-31   sources=4  reconciled=3  PASS
  new  FY2022 Q1  2022-01-30   sources=2  reconciled=1  PASS
  new  FY2022 H1  2022-05-01   sources=3  reconciled=3  PASS
  new  FY2022 Q2  2022-05-01   sources=4  reconciled=4  PASS
  new  FY2022 9M  2022-07-31   sources=4  reconciled=4  PASS
  new  FY2022 Q3  2022-07-31   sources=4  reconciled=4  PASS
  new  FY2022 FY  2022-10-30   sources=4  reconciled=3  PASS
  new  FY2023 Q1  2023-01-29   sources=3  reconciled=3  PASS
  new  FY2023 H1  2023-04-30   sources=3  reconciled=3  PASS
  new  FY2023 Q2  2023-04-30   sources=2  reconciled=1  PASS
  new  FY2023 9M  2023-07-30   sources=2  reconciled=2  PASS
  new  FY2023 Q3  2023-07-30   sources=2  reconciled=2  PASS
  new  FY2023 FY  2023-10-29   sources=5  reconciled=3  PASS
  new  FY2024 Q1  2024-01-28   sources=4  reconciled=4  PASS
  new  FY2024 H1  2024-04-28   sources=2  reconciled=2  PASS
  new  FY2024 Q2  2024-04-28   sources=4  reconciled=4  PASS
  new  FY2024 9M  2024-07-28   sources=4  reconciled=3  PASS
  new  FY2024 Q3  2024-07-28   sources=4  reconciled=4  PASS
  new  FY2024 FY  2024-10-27   sources=3  reconciled=1  PASS
  new  FY2025 Q1  2025-01-26   sources=4  reconciled=4  PASS
  new  FY2025 H1  2025-04-27   sources=5  reconciled=5  PASS
  new  FY2025 Q2  2025-04-27   sources=5  reconciled=5  PASS
  new  FY2025 9M  2025-07-27   sources=1  reconciled=1  PASS
  new  FY2025 Q3  2025-07-27   sources=1  reconciled=1  PASS
  new  FY2025 FY  2025-11-02   sources=1  reconciled=1  PASS
  new  FY2026 Q1  2026-02-01   sources=2  reconciled=2  PASS
  new  FY2026 H1  2026-05-03   sources=2  reconciled=2  PASS
  new  FY2026 Q2  2026-05-03   sources=2  reconciled=2  PASS
```

Independent check against the task's verified ground truth: all 35 cells of the
Q2 FY2026 matrix (six geographies x four segments plus totals) match exactly.

## Derivations

Nine quarters are not disclosed as a three-month column anywhere in the corpus
and were derived by subtraction. Each derived row carries `source = derived` and
a note naming both columns.

| Scheme | Quarter | Derivation |
|---|---|---|
| current | FY2020 Q4 | fiscal-year column − nine-month column |
| current | FY2021 Q4 | fiscal-year column − nine-month column |
| current | FY2022 Q4 | fiscal-year column − nine-month column |
| current | FY2023 Q4 | fiscal-year column − nine-month column |
| current | FY2024 Q4 | fiscal-year column − nine-month column |
| current | FY2025 Q4 | fiscal-year column − nine-month column |
| pre-FY2021 | FY2019 Q4 | fiscal-year column − nine-month column |
| pre-FY2021 | FY2020 Q3 | nine-month column − six-month column |
| pre-FY2021 | FY2020 Q4 | fiscal-year column − nine-month column |

Deere never discloses a Q4 three-month column, so every Q4 in this file is
derived. FY2020 Q3 on the *pre-FY2021* scheme is derived because the Q3 FY2020
10-Q's three-month table survives the corpus's PDF-to-markdown conversion only as
loose text with labels and numbers on separate lines — it is not machine-readable.
The same quarter **is** available directly on the current scheme (Q3 FY2020,
disclosed as a comparative in the Q3 FY2021 10-Q), so nothing is lost for
forecasting purposes.

All derived quarters were re-validated: their rows sum to their derived row
totals and their columns to their derived column totals, with no exceptions.

## Known quirks

1. **±1 rounding.** Deere rounds each disclosed column independently to whole
   millions, so the sum of rounded quarters can differ from the rounded cumulative
   column by 1. Across 1,298 additivity checks (Q1+Q2 vs H1, Q1+Q2+Q3 vs 9M,
   Q1..Q4 vs FY, cell by cell), 204 differ and **every one differs by exactly 1**
   — except the case in point 2. This is disclosure rounding, not a parse error.

2. **FY2020 PPA/SAT reallocation, up to 12 USDm.** On the current segment scheme,
   FY2020 Q1 (as presented in the Q1 FY2021 10-Q) plus FY2020 Q2 (as presented in
   the Q2 FY2021 10-Q) does not equal the FY2020 H1 column in that same Q2 FY2021
   10-Q. The differences are confined to PPA and SAT and exactly offset each other
   (total PPA +12 / SAT −12; Canada +9 / −9; US +2 / −2; Latin America +1 / −1).
   Deere refined the PPA/SAT boundary between the two filings without restating
   the earlier comparative. Both figures are reproduced as disclosed. Prefer the
   later (H1) presentation if you need internal consistency across FY2020 H1.

3. **17 product-line cells were reconstructed, not read.** In a handful of tables
   the PDF-to-markdown conversion merged two or three product-line rows into one
   cell (e.g. "Forestry Financial Products" carrying seven numbers). Those cells
   were solved from the column residuals: the solution had to be unique as a
   multiset, every multi-segment row total had to appear among the stray numbers,
   and the repaired block then had to pass the full row-and-column reconciliation.
   Each such row is flagged in `notes`. Independent confirmation: for the five
   reconstructed values that can be cross-checked by cumulative arithmetic against
   a *different* filing (FY2021 Q1 Forestry 290 and Financial products 884,
   FY2020 Q1 Compact construction 288 and Roadbuilding 605, FY2020 Q3 Roadbuilding
   818), all five match. **No geography cell was ever reconstructed** — the whole
   geographic matrix is read directly from the filings.

4. **Rejected blocks.** 20 candidate tables were dropped as unreadable renderings.
   All 20 are duplicate renderings of periods covered cleanly by another filing;
   no period lost coverage. The three recurring failure modes are: the plain-text
   dump that precedes some pipe tables putting labels and numbers on separate
   lines; 10-K tables where the conversion merged geography rows; and headers that
   lost their span word ("Months Ended July 31, 2022"). Span-less headers are
   resolved by fingerprint-matching against a dated block for the same date, and
   dropped when no match exists.

## Quarterly series, current segment scheme (rev-rec basis, USDm)

| FY | Q | PPA | SAT | CF | FS | Total | US | Canada | W.Eur | C.Eur/CIS | LatAm | AAO/ME |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 2020 | Q1 | 2,576 | 2,019 | 2,105 | 931 | 7,631 | 4,163 | 466 | 1,139 | 389 | 680 | 794 |
| 2020 | Q2 | 3,431 | 2,634 | 2,313 | 875 | 9,253 | 5,248 | 583 | 1,491 | 486 | 653 | 792 |
| 2020 | Q3 | 3,376 | 2,419 | 2,238 | 892 | 8,925 | 4,525 | 635 | 1,501 | 506 | 777 | 981 |
| 2020 | Q4 | 3,881 | 2,435 | 2,525 | 890 | 9,731 | 5,060 | 706 | 1,202 | 691 | 913 | 1,159 |
| 2021 | Q1 | 3,147 | 2,551 | 2,530 | 884 | 9,112 | 4,832 | 533 | 1,398 | 432 | 819 | 1,098 |
| 2021 | Q2 | 4,602 | 3,427 | 3,137 | 892 | 12,058 | 6,138 | 869 | 1,867 | 909 | 1,083 | 1,192 |
| 2021 | Q3 | 4,338 | 3,212 | 3,075 | 902 | 11,527 | 5,912 | 853 | 1,727 | 766 | 1,170 | 1,099 |
| 2021 | Q4 | 4,730 | 2,857 | 2,871 | 869 | 11,327 | 5,932 | 760 | 1,437 | 557 | 1,450 | 1,191 |
| 2022 | Q1 | 3,433 | 2,674 | 2,592 | 870 | 9,569 | 4,879 | 745 | 1,383 | 534 | 1,176 | 852 |
| 2022 | Q2 | 5,176 | 3,606 | 3,724 | 864 | 13,370 | 7,214 | 974 | 1,683 | 712 | 1,666 | 1,121 |
| 2022 | Q3 | 6,185 | 3,691 | 3,323 | 903 | 14,102 | 7,472 | 1,073 | 1,696 | 582 | 2,018 | 1,261 |
| 2022 | Q4 | 7,524 | 3,598 | 3,426 | 988 | 15,536 | 8,673 | 1,110 | 1,582 | 461 | 2,479 | 1,231 |
| 2023 | Q1 | 5,303 | 3,054 | 3,255 | 1,040 | 12,652 | 6,907 | 931 | 1,459 | 412 | 1,827 | 1,116 |
| 2023 | Q2 | 7,912 | 4,200 | 4,168 | 1,107 | 17,387 | 9,626 | 1,190 | 2,169 | 703 | 2,238 | 1,461 |
| 2023 | Q3 | 6,972 | 3,806 | 3,795 | 1,228 | 15,801 | 8,698 | 1,029 | 2,091 | 491 | 2,034 | 1,458 |
| 2023 | Q4 | 7,101 | 3,162 | 3,803 | 1,346 | 15,412 | 8,875 | 1,137 | 1,602 | 531 | 2,098 | 1,169 |
| 2024 | Q1 | 5,043 | 2,492 | 3,274 | 1,376 | 12,185 | 7,131 | 886 | 1,421 | 354 | 1,303 | 1,090 |
| 2024 | Q2 | 6,679 | 3,253 | 3,908 | 1,395 | 15,235 | 9,219 | 1,184 | 1,857 | 454 | 1,409 | 1,112 |
| 2024 | Q3 | 5,242 | 3,128 | 3,293 | 1,489 | 13,152 | 7,706 | 1,070 | 1,560 | 389 | 1,365 | 1,062 |
| 2024 | Q4 | 4,462 | 2,381 | 2,778 | 1,523 | 11,144 | 6,186 | 760 | 1,351 | 291 | 1,461 | 1,095 |
| 2025 | Q1 | 3,173 | 1,807 | 2,058 | 1,470 | 8,508 | 4,702 | 721 | 1,016 | 181 | 1,096 | 792 |
| 2025 | Q2 | 5,326 | 3,046 | 3,006 | 1,385 | 12,763 | 6,927 | 1,189 | 1,820 | 428 | 1,372 | 1,027 |
| 2025 | Q3 | 4,384 | 3,089 | 3,127 | 1,418 | 12,018 | 6,008 | 895 | 2,029 | 536 | 1,459 | 1,091 |
| 2025 | Q4 | 4,865 | 2,522 | 3,459 | 1,548 | 12,394 | 6,336 | 930 | 1,685 | 430 | 1,680 | 1,333 |
| 2026 | Q1 | 3,269 | 2,224 | 2,734 | 1,384 | 9,611 | 4,960 | 826 | 1,430 | 310 | 1,042 | 1,043 |
| 2026 | Q2 | 4,607 | 3,542 | 3,854 | 1,366 | 13,369 | 7,198 | 1,039 | 2,141 | 525 | 1,268 | 1,198 |

Q4 rows are derived (see above); all others are disclosed three-month columns.

### Q3 history for the PPA build-up

The forecast target quarter is Q3 FY2026 (quarter ending ~2026-08-02). Six prior
Q3s of PPA by geography, on this basis:

| FY Q3 | US | Canada | W.Eur | C.Eur/CIS | LatAm | AAO/ME | PPA total |
|---|--:|--:|--:|--:|--:|--:|--:|
| FY2020 | 1,617 | 199 | 517 | 219 | 512 | 312 | 3,376 |
| FY2021 | 1,995 | 253 | 566 | 398 | 758 | 368 | 4,338 |
| FY2022 | 2,904 | 451 | 645 | 348 | 1,327 | 510 | 6,185 |
| FY2023 | 3,394 | 397 | 833 | 302 | 1,326 | 720 | 6,972 |
| FY2024 | 2,839 | 489 | 522 | 201 | 841 | 350 | 5,242 |
| FY2025 | 1,684 | 335 | 677 | 301 | 1,055 | 332 | 4,384 |

Two features a bottom-up Q3 model has to respect. First, Q3 is not a stable share
of the year: Q3 PPA has run between 24.5% and 27.7% of the fiscal-year PPA total over
FY2020–FY2025, and the Q3/Q2 ratio has ranged from 0.78 (FY2024) to 1.19
(FY2022). Second, the geographic mix is not stable either — US PPA fell from 49%
of PPA in Q3 FY2023 to 38% in Q3 FY2025 while Latin America rose from 19% to 24%.
Applying a single company-level growth rate to the Q2 FY2026 matrix will not
reproduce either pattern.
