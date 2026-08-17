# Deere & Company — regional driver series and driver→revenue relationships

**Purpose:** supply region-specific economic drivers so each cell of Deere's
six-geography × four-segment revenue matrix can be forecast on its own economics,
and report honestly how much of Deere's regional revenue those drivers actually explain.

**As-of date:** 16 August 2026. Deere has **not** reported FY2026 Q3; the Q3 call is
09:00 US Central on Thursday 20 August 2026. Nothing in this file is a Q3 FY2026 actual.
The offline corpus is frozen at 2026-05-28 and contains no Q3 FY2026 results. The corpus
`INDEX.md` row labelled `2026-05-21 | Call Transcript | Q3 2026` is mislabelled — that
document is the **Q2** FY2026 call.

## Files

| File | Contents |
|---|---|
| `data/deere/drv_regional.csv` | 1,014 rows, tidy long, the driver panel |
| `data/deere/de_geo_matrix.csv` | 684 rows, the parsed rev-rec geography × segment matrix (dependency) |
| `scripts/data/parse_de_geo_matrix.py` | matrix parser + reconciliation |
| `scripts/data/build_de_regional_drivers.py` | driver assembly |
| `scripts/data/de_regional_driver_correlations.py` | the correlation study |

---

## 1. The revenue side: what the matrix actually supports

I parsed the ASC 606 revenue-recognition footnote (note 3) out of the offline 10-Q corpus
with a script. Three distinct markdown formatting eras had to be handled — the FY2019–20
two-segment `Agriculture and Turf / Construction and Forestry` layout, the FY2021–24
space-padded layout, and the FY2025–26 layout riddled with zero-width and non-breaking
characters and bare `$` cells. Two label quirks caused most of the work: the Asia row
wraps across two markdown rows with the figures on the continuation line, and its name
changed from *Asia, Africa, Australia, New Zealand, and Middle East* to
*Asia, Africa, Oceania, and Middle East*.

**Validation: every quarter reconciles.** Rows sum to their stated row total and columns
sum to their column total across all 23 quarters, at a 1.0 USDm tolerance. **Zero
reconciliation failures.** FY2026 Q2 ties exactly to the verified ground-truth matrix
(US 2,012 / 1,833 / 2,317 / 1,036 / 7,198; total 4,607 / 3,542 / 3,854 / 1,366 / 13,369).

**Coverage is 23 quarters, Q1–Q3 only, FY2019 through FY2026 — there is no Q4.**
This is not a parser gap. Deere's footnote discloses a standalone matrix only in the
10-Qs; the 10-K discloses the *annual* matrix, and in this corpus those annual tables are
structurally mangled (adjacent geography rows merged into one, e.g. a single row reading
`United States | $11,741 1,818 | $ 6,249 $ 605 | ...` carrying both the US and Canada
figures). Deriving Q4 as FY minus nine months from tables in that state would inject
errors into every Q4. I left Q4 out rather than fabricate it.

For a **Q3** forecast this is the right sample to have: Q1–Q3 coverage is complete and
gapless. But note the binding constraint — **only 6 usable Q3 year-over-year observations
per region.**

**Independent cross-validation.** A separate parse of the same footnote exists at
`de_geo_segment_matrix.csv`. Comparing only three-month cells (excluding its rows flagged
as cumulative six- and nine-month columns), the two independent parsers agree on **635 of
636 shared cells**. The single exception is US Financial Services for the quarter ended
2020-08-02: 632 here versus 633 there. 632 is the figure disclosed as the FY2020 Q3
comparative in the FY2021 Q3 10-Q and it reconciles exactly against the disclosed US total
(1,617 + 1,228 + 1,048 + 632 = 4,525); the 633 is presumably the as-first-reported value
before a 1m restatement. Immaterial, but recorded rather than silently smoothed.

### Q3 rev-rec revenue by region, all segments (USDm)

| Region | FY19 | FY20 | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| United States | 5,096 | 4,525 | 5,912 | 7,472 | 8,698 | 7,706 | 6,008 |
| Canada | 707 | 635 | 853 | 1,073 | 1,029 | 1,070 | 895 |
| Western Europe | 1,634 | 1,501 | 1,727 | 1,696 | 2,091 | 1,560 | 2,029 |
| Central Europe and CIS | 563 | 506 | 766 | 582 | 491 | 389 | 536 |
| Latin America | 945 | 777 | 1,170 | 2,018 | 2,034 | 1,365 | 1,459 |
| Asia, Africa, Oceania, ME | 1,091 | 981 | 1,099 | 1,261 | 1,458 | 1,062 | 1,091 |

### Q3 revenue YoY by region, with the latest reported quarter for reference

| Region | FY20 | FY21 | FY22 | FY23 | FY24 | FY25 | **FY26 Q2 (reported)** |
|---|---:|---:|---:|---:|---:|---:|---:|
| United States | -11.2% | +30.7% | +26.4% | +16.4% | -11.4% | -22.0% | **+3.9%** |
| Canada | -10.2% | +34.3% | +25.8% | -4.1% | +4.0% | -16.4% | **-12.6%** |
| Western Europe | -8.1% | +15.1% | -1.8% | +23.3% | -25.4% | +30.1% | **+17.6%** |
| Central Europe and CIS | -10.1% | +51.4% | -24.0% | -15.6% | -20.8% | +37.8% | **+22.7%** |
| Latin America | -17.8% | +50.6% | +72.5% | +0.8% | -32.9% | +6.9% | **-7.6%** |
| Asia, Africa, Oceania, ME | -10.1% | +12.0% | +14.7% | +15.6% | -27.2% | +2.7% | **+16.7%** |

**Basis warning.** Everything above is **rev-rec basis** (revenue from contracts with
customers), which does *not* tie to segment net sales. FY2026 Q2 PPA is 4,607 on the
rev-rec basis and 4,503 in the 8-K segment table — a 104m gap. Never mix the two in one
series. Every row of `drv_regional.csv` carries `basis=driver`; the revenue file carries
`basis=rev-rec`.

---

## 2. The driver panel

`drv_regional.csv`, 1,014 rows, all six geographies. Aligned to **Deere fiscal quarters**:
Q1 = Nov–Jan, Q2 = Feb–Apr, Q3 = May–Jul, Q4 = Aug–Oct, with fiscal year = calendar year + 1
for November and December observations. FRED daily and monthly series are averaged within
those windows. Coverage for the machine-readable series is **FY2015 Q1 → FY2026 Q3, 46–47
quarters**, comfortably past the 2015 target.

Three source classes:

1. **FRED keyless CSV** (`fredgraph.csv?id=…`, descriptive User-Agent) — 19 series,
   fully machine-readable, refetchable, cached.
2. **Deere's own regional industry unit outlook**, parsed from the offline 8-K corpus —
   management's regional view, restated each quarter. Range phrases are converted to
   midpoints (`Down 15 to 20%` → -17.5; `Flat to up 5%` → +2.5). FY2021 Q1 → FY2026 Q2,
   20–22 observations per region.
3. **Individually cited point observations** for series with no free machine-readable feed
   — AEM units, CONAB, Plano Safra, ABARES, India tractor registrations, the Argentine
   export-tax schedule, USDA net farm income, StatCan farm cash receipts, CEMA.

**Missing data is an absent row.** No zeros, no interpolation, no carry-forward.
Quarters built from fewer observations than a complete quarter are kept but the note field
begins with the literal string `PARTIAL QUARTER` and they are **excluded from every
correlation**. As of 16 August 2026 the monthly commodity series run through June 2026, so
FY2026 Q3 commodity values are May–June two-month averages and are flagged as such.

### Coverage by region

| Region | Machine-readable drivers | Point observations |
|---|---|---|
| United States | farm proprietors' income (BEA, quarterly SAAR), corn, soybeans, farm-products PPI, ag-machinery PPI ×2, prime rate, fed funds | AEM tractor/combine units and YoY, USDA net farm income, corn/soy acreage and production |
| Canada | USD/CAD | StatCan farm cash receipts, canola area and production, wheat price YoY |
| Western Europe | EUR/USD, wheat | CEMA business-climate index |
| Central Europe and CIS | wheat (proxy), EUR/USD | — |
| Latin America | USD/BRL, soybeans, corn, Brazil short rate | CONAB soy/corn/total grain, Plano Safra 2026/27 envelope and rates, Argentine export taxes |
| Asia, Africa, Oceania, ME | USD/INR, wheat | India tractor registrations (industry and Mahindra), ABARES winter crop |

### Known gaps I did not fill

- **No quarterly US net farm income exists.** USDA ERS publishes it annually. The BEA farm
  proprietors' income series is the only quarterly measure and is a different concept;
  labelled as such.
- **No AEM history.** AEM's monthly unit data is behind a membership wall; only the July
  2026 release is captured. This is the single most valuable missing series for the US cell.
- **No Black Sea FOB wheat.** `drv_ce_wheat_price` uses the IMF global benchmark as an
  explicit proxy and says so in the note.
- **No EU CAP payment series** and **no quantified sanctions/trade-constraint series** for
  Central Europe and CIS. Deere suspended Russian shipments in 2022; that is a structural
  break in the CE&CIS cell, not something a driver regression will capture.
- **No India monsoon index** as a number — the July 2026 monsoon is characterised
  qualitatively in the source (recovered rainfall, improved reservoirs, accelerated kharif
  sowing) and I did not invent a value.

---

## 3. The May–July 2026 window (the quarter being forecast)

FRED-derived drivers, FY2026 Q3 vs FY2025 Q3:

| Region | Driver | FY25 Q3 | FY26 Q3 | YoY | |
|---|---|---:|---:|---:|---|
| United States | ag machinery PPI | 323.86 | 330.73 | +2.1% | |
| United States | farm products PPI | 238.47 | 243.66 | +2.2% | |
| United States | corn, USD/t | 197.66 | 205.70 | +4.1% | partial (May–Jun) |
| United States | soybeans, USD/t | 381.98 | 426.85 | +11.7% | partial (May–Jun) |
| United States | prime rate | 7.50 | 6.75 | -10.0% | |
| United States | fed funds | 4.33 | 3.63 | -16.2% | |
| Canada | USD/CAD | 1.374 | 1.396 | +1.6% | mild translation headwind |
| Western Europe | EUR/USD | 1.149 | 1.154 | +0.4% | translation roughly neutral |
| Central Europe and CIS | wheat, USD/t | 178.43 | 210.27 | +17.8% | partial (May–Jun) |
| Latin America | USD/BRL | 5.582 | 5.074 | -9.1% | **BRL strength, translation tailwind** |
| Latin America | corn, USD/t | 197.66 | 205.70 | +4.1% | partial (May–Jun) |
| Latin America | Brazil short rate | 14.82 | 14.45 | -2.6% | partial (May–Jun) |
| Asia/Africa/Oceania/ME | USD/INR | 85.77 | 95.46 | +11.3% | **sharp INR weakness** |

Non-FRED events landing **inside** the May–July 2026 window:

- **Plano Safra 2026/27 launched July 2026**: BRL 525.1bn commercial envelope (>BRL 608bn
  including family farming), headline commercial costing rate cut **14.0% → 12.5%**,
  Pronamp cut 10.0% → 9.0%. A ~150bp cut in subsidised farm credit at the top of Brazil's
  buying season is a real positive for the Latin America cell.
- **Argentina cut wheat and barley export duties 7.5% → 5.5% effective June 2026**;
  soybeans 24% → 15%, corn at 8.5% on a declining schedule.
- **US demand still contracting**: AEM July 2026 total tractors -10.9% YoY, four-wheel-drive
  **-38.7%**, 100+hp -15.5% calendar YTD, self-propelled combines -10.2% YTD. Nothing here
  says the US large-ag trough is behind Deere.
- **India inflecting hard the other way**: July 2026 industry tractor sales +28.1% YoY
  (117,349 units), Mahindra domestic +21%, on a favourable monsoon and accelerated kharif
  sowing.
- **Brazil harvested a record crop**: CONAB 2025/26 soybeans 180.6 Mt (+5%), corn 141.7 Mt
  (+0.4%), total grain 360.1 Mt (+2.1%).
- **Australia turning down**: ABARES June 2026 puts the 2026/27 winter crop at 54.5 Mt,
  **-21%**, with wheat down ~26%. This bites FY2027 more than FY2026 Q3.
- **Europe softening at the margin**: CEMA business-climate index fell -2 → **-6** in April
  2026, with a third of EU manufacturers expecting fewer orders over six months. This is an
  April reading — inside FY2026 Q2, not Q3 — and is the most recent available.

---

## 4. Driver → revenue relationships, and why most of them are not findings

### Method

Dependent variable: **YoY % change** in a region's rev-rec revenue. Independent variable:
**YoY % change** in the driver, at lags 0–4 quarters. Both sides are year-over-year
differenced deliberately: quarterly equipment revenue is violently seasonal, so a
level-on-level correlation would mostly measure shared trend and shared seasonality rather
than any economic relationship. YoY differencing costs four quarters, leaving **n ≤ 20 per
region** (n ≤ 17 for PPA, which only exists from FY2020).

### The multiple-comparisons problem, stated up front

**230 tests were run.** At p < 0.05, chance alone produces about **12 apparently significant
results**. The Bonferroni threshold for a single honest claim is **p < 0.00022**. Only
**four** results clear it — and two of those are artifacts. Ranking correlations and
reporting the top of the list is exactly how spurious relationships get presented as
findings, so the full lag-0 table for every region is given below, not just the winners.

Twenty observations, six of them Q3, spanning a period containing a pandemic, a
once-in-a-generation grain price spike, a Russian market exit, and a historic ag downcycle,
cannot identify stable regional demand elasticities. Treat everything below as a hypothesis.

### The four results that clear Bonferroni

| Region | Target | Driver | Lag | n | r | p | Verdict |
|---|---|---|---:|---:|---:|---:|---|
| Latin America | PPA | corn price | 1 | 17 | **+0.872** | <0.0001 | **plausibly real** |
| Latin America | Total | corn price | 1 | 20 | **+0.844** | <0.0001 | **plausibly real** |
| United States | PPA | ag machinery PPI | 2 | 17 | +0.839 | <0.0001 | **endogenous — discard** |
| United States | PPA | farm machinery PPI (mfg) | 2 | 17 | +0.814 | 0.0001 | **endogenous — discard** |

**Latin America × corn price, one quarter lagged, is the one relationship I would actually
use.** The sign, the lag and the mechanism all agree: Brazilian grain revenue converts to
equipment orders with roughly a quarter's delay. It is the strongest relationship in the
dataset and it is the only strong one whose economics are not circular. Soybean price at
lag 1 corroborates it (r = +0.714, n = 20).

**The two US PPI results must be discarded.** The BLS agricultural-machinery PPI is
constructed from prices charged by agricultural machinery manufacturers, and Deere is a
dominant constituent of that index. Correlating Deere's US revenue against an index built
partly from Deere's own price realization is close to regressing a variable on itself. The
high r is an accounting relationship, not a demand driver. I am flagging this rather than
reporting +0.84 as the best US driver.

### Results that look strong and are almost certainly spurious

- **US prime rate r = +0.743 (n=17, PPA, lag 0), fed funds r = +0.712.** The sign is
  backwards from theory — higher financing costs should *depress* equipment demand. This is
  the 2021–23 grain boom happening to coincide with the Fed hiking cycle. Do not use;
  certainly do not use it to argue that 2026's rate cuts are bearish for Deere.
- **USD/INR r = +0.66 (lag 2) for Asia/Africa/Oceania/ME.** Sign is backwards for
  translation: a weaker rupee should reduce USD-reported revenue, not raise it. With n = 20
  and one dominant driver of that cell being India's monsoon cycle, this is noise.
- **EUR/USD r = +0.64 (Western Europe, Total, lag 0) and +0.68 (Central Europe and CIS).**
  These are *mechanically* correct but they are largely a **translation identity**, not a
  demand relationship: Deere reports in USD, so a stronger euro raises reported European
  revenue arithmetically. Useful for forecasting the reported number, useless as evidence
  about European farmer demand. Note that EUR/USD is roughly flat YoY in FY2026 Q3 (+0.4%),
  so this identity contributes almost nothing this quarter — a marked change from the large
  FX tailwind in FY2026 Q2.

### Notable *negative* results — these matter more than the winners

- **US farm proprietors' income has essentially zero relationship with Deere's US revenue:
  r = -0.048 (PPA, n=17) and r = -0.071 (Total, n=20).** The most frequently cited driver of
  US ag equipment demand does not explain Deere's US revenue at quarterly frequency in this
  sample at all. Part of this is measurement — BEA farm proprietors' income is not USDA net
  farm income and includes large, lumpy government payments — but a forecaster relying on
  "farm income drives Deere" should know the quarterly panel does not support it.
- **Wheat prices are near-useless for all three wheat-exposed regions**: Western Europe
  r = +0.074, Central Europe and CIS r = +0.266, Asia/Africa/Oceania/ME r = +0.282, all
  p > 0.27. The FY2026 Q3 wheat move is large (+17.8%) but there is no historical basis for
  translating it into revenue.
- **Canada has no usable driver.** The best relationship found anywhere in the Canada cell
  across all drivers and all lags is USD/CAD at r = -0.443 (n=20, p = 0.050) — one test out
  of many, at exactly the significance boundary. Canada should be forecast off Deere's own
  US & Canada large-ag outlook and segment mix, not off a driver regression.
- **Deere's own management regional outlook is a weak contemporaneous predictor.** For
  Latin America it is essentially zero (r = -0.042, n=11). It looks better at lag 1–2
  (Latin America +0.82, Europe +0.79) but n falls to 10–11 there and none survive
  correction.

### Full lag-0 correlation table

| Region | Target | Driver | n | r | p |
|---|---|---|---:|---:|---:|
| Asia/Africa/Oceania/ME | PPA | USD/INR | 17 | +0.447 | 0.072 |
| Asia/Africa/Oceania/ME | PPA | wheat | 17 | +0.282 | 0.272 |
| Asia/Africa/Oceania/ME | Total | wheat | 20 | +0.256 | 0.276 |
| Asia/Africa/Oceania/ME | Total | USD/INR | 20 | +0.173 | 0.467 |
| Canada | PPA | USD/CAD | 17 | +0.288 | 0.262 |
| Canada | Total | USD/CAD | 20 | -0.374 | 0.104 |
| Central Europe and CIS | PPA | EUR/USD | 17 | +0.657 | 0.004 |
| Central Europe and CIS | PPA | wheat | 17 | +0.266 | 0.301 |
| Central Europe and CIS | Total | EUR/USD | 20 | +0.676 | 0.001 |
| Central Europe and CIS | Total | wheat | 20 | +0.295 | 0.207 |
| Latin America | PPA | corn | 17 | +0.737 | 0.001 |
| Latin America | PPA | soybeans | 17 | +0.643 | 0.005 |
| Latin America | PPA | Brazil short rate | 17 | +0.516 | 0.034 |
| Latin America | PPA | USD/BRL | 17 | +0.073 | 0.782 |
| Latin America | PPA | mgmt South America outlook | 11 | -0.042 | 0.902 |
| Latin America | Total | corn | 20 | +0.728 | <0.001 |
| Latin America | Total | soybeans | 20 | +0.661 | 0.002 |
| Latin America | Total | Brazil short rate | 20 | +0.585 | 0.007 |
| Latin America | Total | USD/BRL | 20 | -0.271 | 0.248 |
| Latin America | Total | mgmt South America outlook | 11 | -0.033 | 0.923 |
| United States | PPA | prime rate | 17 | +0.743 | 0.001 |
| United States | PPA | fed funds | 17 | +0.712 | 0.001 |
| United States | PPA | farm machinery PPI (mfg) | 17 | +0.668 | 0.003 |
| United States | PPA | ag machinery PPI | 17 | +0.605 | 0.010 |
| United States | PPA | soybeans | 17 | +0.361 | 0.155 |
| United States | PPA | mgmt large-ag outlook | 13 | -0.273 | 0.367 |
| United States | PPA | farm products PPI | 17 | +0.266 | 0.302 |
| United States | PPA | corn | 17 | +0.213 | 0.412 |
| United States | PPA | mgmt small-ag & turf outlook | 10 | -0.079 | 0.827 |
| United States | PPA | farm proprietors' income | 17 | -0.048 | 0.855 |
| United States | Total | prime rate | 20 | +0.634 | 0.003 |
| United States | Total | farm machinery PPI (mfg) | 20 | +0.628 | 0.003 |
| United States | Total | fed funds | 20 | +0.608 | 0.004 |
| United States | Total | ag machinery PPI | 20 | +0.582 | 0.007 |
| United States | Total | soybeans | 20 | +0.563 | 0.010 |
| United States | Total | corn | 20 | +0.391 | 0.088 |
| United States | Total | farm products PPI | 20 | +0.391 | 0.089 |
| United States | Total | mgmt large-ag outlook | 13 | -0.282 | 0.351 |
| United States | Total | mgmt small-ag & turf outlook | 10 | -0.130 | 0.720 |
| United States | Total | farm proprietors' income | 20 | -0.071 | 0.765 |
| Western Europe | PPA | EUR/USD | 17 | +0.417 | 0.096 |
| Western Europe | PPA | mgmt Europe outlook | 13 | +0.356 | 0.233 |
| Western Europe | PPA | wheat | 17 | +0.074 | 0.779 |
| Western Europe | Total | EUR/USD | 20 | +0.637 | 0.003 |
| Western Europe | Total | mgmt Europe outlook | 13 | +0.400 | 0.175 |
| Western Europe | Total | wheat | 20 | +0.101 | 0.671 |

---

## 5. How much forecasting power is here, honestly

Fitting the single best relationship in the dataset — Latin America revenue on lagged corn
price:

```
LatAm Total YoY = 2.84 + 1.216 × corn YoY(lag 1)    n=20, residual SD = 19.9 pp
LatAm PPA   YoY = 10.38 + 1.281 × corn YoY(lag 1)   n=17, residual SD = 20.2 pp
```

The lag-1 input for FY2026 Q3 is FY2026 Q2 corn, **-0.9% YoY**, giving point estimates of
**+1.7%** (Total) and **+9.2%** (PPA) YoY for the Latin America cell.

**The one-sigma residual is ±20 percentage points.** That is the *best* relationship
available. A ±20pp band on a quarterly YoY revenue change is wide enough that this
regression adds little over a naive "same as last year" baseline. Every other region is
weaker than this one.

**The honest conclusion: these drivers are useful as directional context and as a
narrative cross-check, not as a forecasting engine.** For the FY2026 Q3 numbers the model
should lean on Deere's own segment guidance, order-book commentary and the reported
H1 FY2026 run-rate, and use this driver panel to sanity-check the *direction* of each
regional cell — most usefully:

- **Latin America** — record Brazilian crop, BRL up 9%, Plano Safra rates cut 150bp in July,
  Argentine export duties cut. Every driver points the same way, and this is the region
  where the driver evidence is genuinely strongest. But note the FY2026 Q2 Latin America
  cell was **-7.6%** YoY, so the drivers and the most recent actual currently disagree.
- **United States** — AEM units still deeply negative (4WD -38.7% in July), consistent with
  Deere's own guidance of US & Canada large ag down 15–20%. No sign of an inflection.
- **Asia/Africa/Oceania/ME** — India tractor volumes +28% is a strong positive, offset by a
  11% weaker rupee and a -21% Australian winter crop forecast.
- **Western Europe / Central Europe and CIS** — the large FX tailwind that helped FY2026 Q2
  has gone flat (EUR/USD +0.4% YoY in Q3 vs the Q2 tailwind), so the +17.6% and +22.7% Q2
  growth rates should not be extrapolated into Q3 unchanged.

---

## 6. Reproducing

```bash
python3 scripts/data/parse_de_geo_matrix.py              # matrix + reconciliation report
python3 scripts/data/build_de_regional_drivers.py        # driver panel (FRED fetch, cached)
python3 scripts/data/de_regional_driver_correlations.py  # correlation study
```

All three are standard-library-only Python. FRED responses are cached to the scratchpad; delete
the cache directory to refetch.
