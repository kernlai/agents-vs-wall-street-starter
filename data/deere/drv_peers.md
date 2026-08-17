# drv_peers — Deere peer financial panel and read-across analysis

Companion to `drv_peers.csv`. Built 2026-08-16. Frozen knowledge date for Deere: **Deere has
not reported FY2026 Q3.** The latest Deere observation in this file is `period_end 2026-05-03`
(FY2026 Q2). Nothing in this file is a Q3 FY2026 actual.

---

## 1. What is in the file

Tidy long CSV, one observation per row:

```
series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes
```

**2,276 rows, 34 series, 10 companies.** `period_end` is always the issuer's own true period
end. `fiscal_year` / `fiscal_quarter` are always the issuer's own fiscal labels.

| series_id | n | first | last | units |
|---|---:|---|---|---|
| `agco_revenue` / `_eps_diluted` / `_operating_margin` | 86 / 86 / 70 | 2008-12-31 | 2026-06-30 | USDm / USD/share / percent |
| `cat_revenue` / `_eps_diluted` / `_operating_margin` | 92 / 92 / 74 | 2007-12-31 | 2026-06-30 | USDm / USD/share / percent |
| `cnh_revenue` / `_eps_diluted` / `_operating_margin` | 69 / 69 / 18 | 2011-12-31 | 2026-06-30 | USDm / USD/share / percent |
| `de_revenue` / `_eps_diluted` / `_operating_margin` | 94 / 94 / 62 | 2007-10-31 | 2026-05-03 | USDm / USD/share / percent |
| `kubota_revenue` / `_operating_profit` / `_operating_margin` / `_eps_basic` | 52 / 43 / 43 / 42 | 2016-03-31 | 2026-06-30 | JPYm / JPYm / percent / JPY/share |
| `kubota_*_legacy_usgaap_mar` (3 series) | 6 each | 2008-03-31 | 2013-03-31 | JPYm / percent |
| `lindsay_revenue` / `_eps_diluted` / `_operating_margin` | 79 / 79 / 64 | 2010-08-31 | 2026-05-31 | USDm / USD/share / percent |
| `titn_revenue` / `_eps_diluted` / `_operating_margin` | 80 / 80 / 65 | 2010-01-31 | 2026-04-30 | USDm / USD/share / percent |
| `toro_revenue` / `_eps_diluted` / `_operating_margin` | 85 / 85 / 69 | 2008-10-31 | 2026-05-01 | USDm / USD/share / percent |
| `tsco_revenue` / `_eps_diluted` / `_operating_margin` | 86 / 86 / 70 | 2008-12-27 | 2026-06-27 | USDm / USD/share / percent |
| `valmont_revenue` / `_eps_diluted` / `_operating_margin` | 87 / 86 / 71 | 2008-12-27 | 2026-06-27 | USDm / USD/share / percent |

`source_type` split: 1,942 `api` (SEC XBRL), 260 `inference` (derived Q4 / derived standalone
quarter), 74 `filing` (Kubota IR releases).

`de_*` is included as the **reference series for the correlation work**, not as the primary
Deere fundamentals extract. It is drawn from SEC XBRL and was validated against the offline
corpus (section 4).

## 2. Coverage vs the 20-year target — honest statement

**Target: 20 years (FY2006–FY2026). Achieved: ~18.5 years at best, ~15–16 years typical.**

The binding constraint is that the SEC's XBRL structured-data mandate phased in for fiscal
periods ending after 15 June 2009. Three years of income-statement comparatives inside the
first XBRL 10-Ks push the annual series back to FY2007 for the largest filers, and no further.
Earliest observation by company:

| company | earliest annual | earliest quarterly | why not earlier |
|---|---|---|---|
| CAT, DE | FY2007 | CY2008Q2 | XBRL mandate + 3yr comparatives |
| AGCO, TSCO, Toro, Valmont | FY2008 | CY2009Q2 | XBRL mandate |
| Lindsay, Titan | FY2010 | CY2010Q2–Q4 | smaller filer, later phase-in |
| CNH Industrial | FY2011 | CY2013Q1 | company formed 2013 (Fiat Industrial / CNH Global merger) |
| Kubota (modern) | FY2016 | CY2016Q1 | see below |

Pre-2007 data would require parsing pre-XBRL HTML 10-Qs for nine companies. I did not do that:
the error rate of unstructured extraction across ~300 old filings would have been higher than
the value of four extra years, and it would have violated the "prefer scripted extraction"
instruction in spirit. **A modeller should treat this panel as starting 2008–2011, not 2006.**

## 3. Method

Three scripts, all in `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/`:

| script | role |
|---|---|
| `peer_diagnose.py` | compares candidate XBRL revenue tags on overlapping periods, per company |
| `build_peers.py` | builds the nine SEC-filer series from the EDGAR XBRL companyfacts API |
| `build_kubota.py` | scrapes and parses Kubota's IFRS results PDFs (Kubota is not an SEC filer) |
| `validate_peers.py` | duplicate / sign / sum-of-quarters / SEC-frames cross-check |
| `analyze_peers.py` | reads the published CSV and produces the correlation study |

Everything is Python standard library. `build_kubota.py` additionally needs `pdftotext`.

### 3.1 Revenue tag selection — the single most important decision

Naively taking "the first `us-gaap` revenue tag that exists" **fabricates a step change**.
`peer_diagnose.py` compared every candidate tag on overlapping periods and found:

* **CAT**: `Revenues` (total sales and revenues, incl. Financial Products) vs `SalesRevenueNet`
  (Machinery/E&T sales only) — **disagree on all 45 overlapping quarters**, e.g. 2008Q2
  13,624 vs 12,797 USDm. Only `Revenues` is used.
* **DE**: same problem — `Revenues` vs `SalesRevenueGoodsNet` (equipment net sales, no financial
  services) disagree on all 43 overlapping quarters. Only `Revenues` is used.
* **CNH**: `Revenues` (total, incl. Financial Services) vs `RevenueFromContractWithCustomer…`
  (net sales of goods only) — disagree on all 27 overlaps. Only `Revenues` is used.
* **Lindsay**: `Revenues` vs `RevenueFromContractWithCustomer…` differ by ~1.5% (the latter
  omits non-contract revenue). Only `Revenues` is used.
* **Valmont**: `SalesRevenueGoodsNet` is a *component*, and the `Revenues` tag (2010–2013 only)
  is a different total again. The chain `SalesRevenueNet` (2009–2018) → `RevenueFromContract…`
  (2018+) agrees on all 5 overlapping quarters and is used.
* **AGCO, Titan, Tractor Supply, Toro**: candidate tags agree exactly on every overlap, so
  chaining across the 2018 ASC 606 boundary is safe.

The chosen tag is recorded in the `notes` column of every row (`xbrl tag=…`), and the excluded
tags plus the reason are also in `notes`. Excluded-tag reasons are per company, not generic.

### 3.2 As-first-reported, not restated

Each value is the **earliest-filed** XBRL fact for that period, so the panel is free of
look-ahead bias. Where a later filing restates the same period by more than 0.5%, the restated
value and its filing date are appended to `notes` (`restated: first reported X in 10-Q filed …;
latest filing 10-K … reports Y`). The `notes` field also carries `as-first-reported in <form>
filed <date>` on every API row, so a modeller can reconstruct a point-in-time vintage.

### 3.3 Keying by period end, not (start, end)

Issuers drift their period start by a day or two between the 10-Q and the later 10-K (CAT tags
2009 Q1 as both 2008-12-30→2009-03-31 and 2009-01-01→2009-03-31). Keying on `(start, end)`
emitted **29 duplicate rows**. Facts are keyed on period end within a duration band
(80–100 days quarterly, 350–380 days annual, which also accommodates 53-week years).

### 3.4 Derived values (`source_type = inference`, 260 rows)

* **Q4 for SEC filers**: most issuers file no Q4 10-Q, so Q4 = FY total − (Q1+Q2+Q3) from exact
  XBRL dollar values. CAT tags all four quarters and needs no derivation.
* **Q4 diluted EPS**: derived the same way but **approximate** — the diluted share count differs
  by quarter, so FY EPS is not exactly the sum of quarterly EPS. Flagged in `notes` on every
  such row. Do not use derived Q4 EPS for anything precision-sensitive.
* **Kubota standalone quarters**: Kubota reports cumulative year-to-date, so discrete quarters
  are obtained by differencing consecutive releases.

### 3.5 Bad-tag guard — a real issuer error caught

Tractor Supply's FY2022 10-K tags **FY2020 total revenue (10,620.352 USDm) with a 91-day Q4
duration**, and SEC even assigns it the `CY2020Q4` frame. Taken at face value this puts a
$10.6bn "quarter" into a company whose real Q4 2020 was ~$2.88bn — a 3.7× error in one cell
that would wreck any fitted model. The build now drops any "quarterly" fact whose value equals
the fiscal-year total for a period ending on the fiscal-year end, and derives Q4 instead
(TSCO FY2020 Q4 = 2,878.265 USDm, `source_type = inference`).

## 4. Validation — what was checked against what

Five independent families of cross-check. **28 individual values cross-checked, 28 agree.**

| # | check | source A | source B (independent) | result |
|---|---|---|---|---|
| 1 | Deere revenue + EPS, 4 quarters | SEC XBRL | offline corpus 8-K earnings releases (authoritative) | **8/8 exact** |
| 2 | Deere derived Q4 revenue | FY − Q1..Q3 from XBRL | Q4 column printed in the FY 8-K | 2/2 agree to $1m rounding — see below |
| 3 | Annual revenue, 9 companies | companyfacts API | SEC **frames** API (different EDGAR pipeline) | **9/9 exact, 0.0000% error** |
| 4 | sum(Q1..Q4) = FY | derived | as-filed FY row | **64 independent company-years, 0 failures** |
| 5 | Kubota, 3 periods | current IFRS release | prior-year release's own figure | **3/3 exact** |
| 6 | duplicates / non-positive revenue | — | — | 0 / 0 |
| 7 | lag sign convention | synthetic 1-quarter-early series | assertion in `analyze_peers.py` | passes |

Check 1 detail (corpus, `challenge/offline-data/deere/filings/`):

| period | metric | corpus | CSV |
|---|---|---|---|
| FY26 Q2 (2026-05-03) | revenue | 13,369 | 13,369 |
| FY26 Q2 | diluted EPS | 6.55 | 6.55 |
| FY26 Q1 (2026-02-01) | revenue | 9,611 | 9,611 |
| FY26 Q1 | diluted EPS | 2.42 | 2.42 |
| FY25 Q2 (2025-04-27) | revenue | 12,763 | 12,763 |
| FY25 Q2 | diluted EPS | 6.64 | 6.64 |
| FY25 Q1 (2025-01-26) | revenue | 8,508 | 8,508 |
| FY25 FY (2025-11-02) | revenue | 45,684 | 45,684 |

Check 2 detail — **a discrepancy worth naming**: Deere's FY2025 8-K prints Q4 revenue of
**12,394** USDm; my derivation gives **12,395**. Same for FY2024: printed 11,143 vs derived
11,144. This is not an error in either place — the press release subtracts *rounded* nine-month
figures, my derivation subtracts *exact* XBRL dollar values. The CSV keeps the exact-arithmetic
value. Magnitude: 1 USDm on ~12,400, i.e. 0.008%.

## 5. Fiscal calendar offsets — read this before joining anything

Peers **do not share Deere's fiscal calendar**, and `drv_peers.csv` does not force them onto it.
Every row keeps the issuer's own `period_end`, `fiscal_year` and `fiscal_quarter`.

| company | FY ends | its Q1 sits in | Q2 | Q3 | Q4 |
|---|---|---|---|---|---|
| **Deere** | late Oct / early Nov | **CQ4 (prior yr)** | **CQ1** | **CQ2** | **CQ3** |
| AGCO, CAT, CNH, Kubota, Tractor Supply, Valmont | Dec | CQ1 | CQ2 | CQ3 | CQ4 |
| Toro, Lindsay | Oct / Aug | CQ4 (prior yr) | CQ1 | CQ2 | CQ3 |
| Titan Machinery | Jan | CQ1 | CQ2 | CQ3 | CQ4 |

("sits in" = the calendar quarter containing the period midpoint.)

Two consequences a modeller must internalise:

1. **Deere's fiscal quarter label leads the calendar by one.** Deere FY2026 Q3 covers roughly
   2026-05-04 → 2026-08-02 and is economically a **calendar Q2 2026** quarter. It overlaps
   AGCO's Q2, CAT's Q2, CNH's Q2.
2. **Titan Machinery's fiscal year is named for the calendar year of its END.** The year ending
   2026-01-31 is Titan's FY2026, so `titn` rows with `period_end 2026-04-30` carry
   `fiscal_year 2027, Q1`. That is Titan's own convention, not an error.

For the correlation study only, each observation is mapped to the calendar quarter containing
its midpoint (approximated as `period_end − 45 days`). This mapping is never written into the
CSV. It agrees with SEC's own `frames` assignment where both exist — e.g. SEC files Deere's
quarter ending 2025-07-27 under `CY2025Q2`, and so does this method.

## 6. Analysis — which peer reads across to Deere, and does it lead or lag?

Setup: YoY revenue growth `g[t] = rev[t]/rev[t−4] − 1` on the calendar-quarter index (YoY
differencing removes the very strong seasonality — Deere Q1 and Titan Q1 are both troughs).
Pearson `r(k) = corr(peer_g[t−k], deere_g[t])`. **`k > 0` means the peer LEADS Deere by k
quarters; `k < 0` means the peer LAGS.** The sign convention is pinned by an assertion in
`analyze_peers.py` against a synthetic series constructed to lead by exactly one quarter.

### 6.1 Headline table

| peer | full: contemp r (n) | full: best r (n) @ k | last 20Q: contemp r (n) | last 20Q: best r @ k | annual non-overlapping r (n, p) |
|---|---|---|---|---|---|
| **AGCO** | **+0.829 (63)** | **+0.861 (64) @ k=−1** | **+0.826 (20)** | **+0.944 (20) @ k=−1** | **+0.931 (17, p<0.0001)** |
| Kubota | +0.794 (37) | +0.794 (37) @ k=0 | +0.905 (20) | +0.905 (20) @ k=0 | +0.797 (9, p=0.008) |
| CAT | +0.727 (66) | +0.767 (67) @ k=−1 | +0.830 (20) | +0.874 (20) @ k=−1 | +0.821 (18, p<0.0001) |
| Valmont | +0.658 (63) | +0.658 (63) @ k=0 | +0.660 (20) | +0.796 (20) @ k=+2 | +0.717 (17, p=0.0008) |
| Titan | +0.611 (59) | +0.645 (59) @ k=−3 | +0.574 (20) | +0.737 (17) @ k=−3 | +0.402 (15, p=0.14) |
| CNH | +0.548 (49) | +0.572 (50) @ k=−1 | +0.332 (20) | +0.452 (20) @ k=−1 | +0.553 (14, p=0.039) |
| Lindsay | +0.340 (58) | +0.603 (55) @ **k=+3** | +0.240 (20) | +0.836 (20) @ **k=+3** | +0.511 (15, p=0.051) |
| Tractor Supply | +0.287 (63) | +0.415 (61) @ **k=+2** | +0.634 (20) | +0.634 (20) @ k=0 | +0.220 (17, p=0.40) |
| Toro | +0.269 (63) | +0.269 (63) @ k=0 | +0.554 (20) | +0.602 (20) @ k=+1 | +0.507 (17, p=0.037) |

Full lag profiles (full history, `r` by `k`; `k>0` = peer leads):

```
peer          -4     -3     -2     -1     +0     +1     +2     +3     +4
agco        +0.29  +0.50  +0.73  +0.86  +0.83  +0.70  +0.53  +0.35  +0.22
cat         +0.19  +0.43  +0.63  +0.77  +0.73  +0.58  +0.39  +0.21  +0.05
cnh         -0.15  +0.12  +0.40  +0.57  +0.55  +0.36  +0.16  +0.09  +0.10
kubota      -0.01  +0.24  +0.54  +0.74  +0.79  +0.57  +0.26  +0.03  -0.13
lindsay     +0.07  +0.12  +0.13  +0.22  +0.34  +0.49  +0.59  +0.60  +0.49
titn        +0.59  +0.64  +0.64  +0.64  +0.61  +0.49  +0.38  +0.19  +0.07
toro        +0.04  +0.04  +0.08  +0.22  +0.27  +0.26  +0.13  +0.07  +0.17
tsco        -0.08  -0.02  +0.03  +0.16  +0.29  +0.38  +0.42  +0.37  +0.28
valmont     +0.25  +0.34  +0.51  +0.58  +0.66  +0.65  +0.59  +0.51  +0.41
```

### 6.2 Answers to the question asked

**Which peer has the strongest read-across? AGCO, unambiguously.** r = +0.83 contemporaneous
(n=63), +0.86 at its peak, +0.94 over the last five years (n=20), and +0.93 on **non-overlapping
annual** growth (n=17, p<0.0001). It wins on every window and on the one test that is immune to
the overlapping-window problem. CAT is a clear second (+0.73 / +0.82 annual, n=18). Kubota
correlates strongly (+0.79 / +0.91 recent) but on a short JPY-denominated history.

**Does it lead or lag? AGCO LAGS Deere, by roughly one quarter — it is not a leading
indicator.** The lag profile peaks at k = −1 (+0.86) and decays monotonically on both sides;
CAT and CNH peak at k = −1 too. Economically this is Deere-first: Deere is the North American
large-ag share leader and turns before the more Europe/South-America-weighted peers.

Two qualifications, both material:

* The k = −1 peak (+0.86) is only marginally above contemporaneous (+0.83). At quarterly
  resolution, with Deere's fiscal quarter straddling calendar quarters by about a third, **the
  honest reading is "coincident to slightly lagging", not a confident one-quarter lag.**
* **Leading and coincident are not the same as useful.** AGCO reports its calendar Q2 in late
  July; Deere reports the overlapping FY Q3 in mid-August. So even a *coincident* AGCO print
  arrives about three weeks before Deere's, which is exactly the window we are in today.

**The only genuine leading indicators are weak ones.** Lindsay leads by three quarters
(r = +0.60 full, n=55; +0.84 over the last 20 quarters) — plausible, since irrigation capex
responds to farm income early — and Tractor Supply leads by two (r = +0.42, n=61). But
Lindsay's contemporaneous r is only +0.34, its annual non-overlapping r is +0.51 at p=0.051, and
its revenue carries a lumpy infrastructure segment. Tractor Supply's annual non-overlapping r is
+0.22 at p=0.40 — **not distinguishable from zero.** Treat both as hypotheses, not signals.

Titan Machinery's k = −3 peak is an artefact of the dealer channel: Titan sells Deere-competitor
(CNH) equipment, and its flat lag profile (+0.59 to +0.64 across k = −4…0) means the peak
location carries no information.

### 6.3 Nowcast inputs for Deere's unreported FY2026 Q3

Deere FY2026 Q3 ≈ 2026-05-04 → 2026-08-02, midpoint mid-June, i.e. **calendar Q2 2026**. Six of
nine peers have already reported an overlapping quarter. Univariate OLS of Deere growth on peer
growth, fitted at the strongest lag for which the peer datum exists today:

| peer | peer quarter used | peer YoY | k | r | n | implied Deere YoY (±1 in-sample se) |
|---|---|---|---|---|---|---|
| AGCO | 2026Q2 | −1.0% | 0 | +0.83 | 63 | **+1.2% ± 9.5%** |
| CAT | 2026Q2 | +24.0% | 0 | +0.73 | 66 | +15.7% ± 11.8% |
| Kubota | 2026Q2 | +18.6% (JPY) | 0 | +0.79 | 37 | +21.4% ± 10.9% |
| Valmont | 2026Q2 | +6.5% | 0 | +0.66 | 63 | +5.9% ± 12.8% |
| CNH | 2026Q2 | +2.0% | 0 | +0.55 | 49 | +6.3% ± 15.0% |
| Lindsay | 2025Q3 | −0.9% | +3 | +0.60 | 55 | +0.8% ± 13.6% |
| Titan | 2026Q1 | −12.1% | +1 | +0.49 | 58 | −3.2% ± 14.6% |
| Tractor Supply | 2025Q4 | +3.3% | +2 | +0.42 | 61 | −1.0% ± 15.3% |
| Toro | 2026Q1 | +8.1% | +1 | +0.26 | 62 | +5.8% ± 16.5% |

Deere's own last reported aligned quarter (2026Q1 = FY26 Q2) grew **+4.7%** YoY.

**The dispersion is the finding.** Single-peer implied readings span −3% to +21%. The two
highest-weight peers disagree violently: AGCO says roughly flat, CAT says mid-teens. CAT's +24%
is not a statistical outlier against its own history (z = +0.83) but CAT's consolidated revenue
is dominated by non-agricultural end markets, so its 2026 acceleration should be discounted
heavily for Deere purposes. **The highest-quality single signal available today is AGCO's
−1.0%, implying Deere FY26 Q3 revenue growth near flat to low-single-digit.** I would weight
AGCO and CNH (the actual ag peers) far above CAT, Kubota and Valmont.

## 7. Caveats

1. **Not 20 years.** ~18.5 years at best, 15–16 typical, and CNH quarterly only from 2013,
   Kubota only from 2016. XBRL does not exist before the 2009 mandate. See section 2.
2. **`_operating_margin` levels are not comparable across companies.** `us-gaap:OperatingIncomeLoss`
   is defined differently by each issuer (what sits above vs below the operating line —
   restructuring, pension, captive-finance results — varies). **Changes** in margin are safer to
   model than levels. This warning is on every margin row's `notes`.
3. **`cnh_operating_margin` covers only 2012–2017** (18 rows). CNH stopped tagging
   `OperatingIncomeLoss` after 2017; it presents "Adjusted EBIT" instead, which is not the same
   concept and is not in this file. **Do not interpolate the gap.**
4. **`de_operating_margin` ends 2024-10-27** for the same reason.
5. **Derived Q4 diluted EPS is approximate** (share-count drift). 260 `inference` rows total.
6. **Kubota is in JPY and is not converted.** Kubota's YoY growth therefore contains a
   translation component that Deere's USD growth does not — a large part of Kubota's +18.6%
   is yen weakness, not volume. Kubota also reports basic EPS only (`kubota_eps_basic`,
   JPY/share); it publishes no diluted figure.
7. **Kubota has two disjoint series and they must not be spliced.** `kubota_revenue` is IFRS,
   December year end, 2016+. `kubota_revenue_legacy_usgaap_mar` is US GAAP, **31 March** year
   end, and stops at FY2013 because Kubota deregistered from the SEC on 2013-07-16 (Form
   15F-12B). Between them sits a 9-month transition period (Apr–Dec 2015) with no comparable
   data. Different series_ids, different notes; joining them would create exactly the kind of
   unmarked structural break this dataset is meant to avoid.
8. **Overlapping-window inflation.** Quarterly YoY growth uses overlapping windows, so the
   residuals are serially correlated and the nominal p-values in section 6 are optimistic. The
   annual non-overlapping column is the robustness check; note that it demotes Tractor Supply
   (p=0.40) and Titan (p=0.14) to insignificance while AGCO and CAT survive comfortably.
9. **Correlation of growth rates is not a forecasting model.** Section 6.3's standard errors are
   in-sample residual sd from a single-regressor fit; true out-of-sample uncertainty is wider.
10. **Regime instability.** CAT's revenue mix has shifted materially toward non-agricultural end
    markets over the sample, so the historical CAT↔DE relationship is probably weakening. The
    last-20-quarter column should be trusted over the full-history column for CAT.
11. **`de_*` series here are for correlation reference only.** They are SEC-XBRL-derived and
    corpus-validated, but the corpus filings remain authoritative for any Deere figure, and
    this file contains no Deere segment (PPA) data at all.
12. **stooq.com CSV endpoints were blocked** by a JavaScript proof-of-work interstitial and were
    not used. SEC EDGAR XBRL (companyfacts, companyconcept, frames), the SEC company-ticker
    file, and kubota.com PDFs all worked.
13. **Two rows carry a genuine value of 0.00 and they are NOT missing data**:
    `titn_eps_diluted` 2015-07-31 (Titan net income that quarter was $6,000, i.e. $0.0003/share,
    tagged as 0.00 in four separate filings) and `toro_eps_diluted` 2012-10-31 (Toro's seasonal
    trough quarter). Both rows say so in `notes` (`ZERO IS REAL, NOT MISSING`). Every other
    absence in this dataset is an absent row, never a zero and never a guess.
14. **The INDEX.md metadata trap was avoided**: the transcript dated 2026-05-21 labelled
    "Q3 2026" is Q2 material. No Q3 FY2026 Deere actuals exist and none are in this file.

## 8. Reproducing

One command rebuilds, validates and re-runs the analysis:

```bash
sh scripts/data/run_peers.sh <work_dir> data/deere/drv_peers.csv
```

Individually:

```bash
python3 scripts/data/peer_diagnose.py <work>/facts                 # tag consistency report
python3 scripts/data/build_peers.py  --cache <work>/facts --out <work>/peers.csv \
                                     --panel <work>/panel.json
python3 scripts/data/build_kubota.py --cache <work>/kubota_pdf --out <work>/kubota.csv \
        --sec-facts <work>/facts/0000109821.json                   # needs pdftotext
python3 scripts/data/validate_peers.py data/deere/drv_peers.csv
python3 scripts/data/analyze_peers.py --csv data/deere/drv_peers.csv
```

`build_peers.py` and `build_kubota.py` cache every downloaded document, so re-runs are offline
and deterministic. All SEC requests send `User-Agent: AgentsVsWallStreet cor@salomo.io`.
