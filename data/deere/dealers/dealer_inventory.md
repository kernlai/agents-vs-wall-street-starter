# Deere dealer inventory — US & Canada Ag, units as % of trailing-12-month retail

**As of 16 August 2026. Deere has NOT reported FY2026 Q3; the Q3 call is 20 August 2026. No Q3 FY2026
actuals exist in this analysis. The last observed data point is April 2026 (2Q FY2026 deck).**

Data: `dealer_inventory.csv` (127 rows). Builder: `scripts/data/build_deere_dealer_inventory.py`.

---

## 1. What the series is, and why it is the right instrument

Deere sells wholesale to independent dealers. Reported revenue is *shipments to dealers*; the wedge
between shipments and end-market retail is the change in dealer field inventory. In the quarterly
earnings-call deck Deere prints, for US & Canada Ag, dealer inventory **in units as a percentage of
trailing-12-month retail sales**, by product category. It is the only quantitative, continuously
disclosed measure of that wedge.

Two properties matter for reading it:

- **The denominator is falling.** TTM retail is shrinking through this downcycle, so a *flat* ratio
  means absolute units are falling. Deere leans on exactly this: Q2 FY2026 management said units for
  high-hp tractors and combines are "down more than 50% from their mid-2024 peak, with inventory to
  sales ratios in line with historical averages."
- **It is not one series, it is three with different physics** (see §3).

## 2. Coverage

| series_id | category | obs | span |
|---|---|---|---|
| `de_dealer_inv_pct_ttm_2wd_100hp` | 2WD tractors 100+ PTO hp (pre-3Q15: "Row-Crop Tractors") | 51 | Jan 2013 – Apr 2026 |
| `de_dealer_inv_pct_ttm_combines` | Combines | 51 | Jan 2013 – Apr 2026 |
| `de_dealer_inv_pct_ttm_4wd` | 4WD tractors | 12 | Jan 2016 – Oct 2025 (intermittent) |
| `de_dealer_inv_pct_ttm_220hp_plus` | 220+ hp tractors (management's narrower internal cut) | 4 | Oct 2023 – Oct 2025 |
| `de_field_inv_units_yoy_pct` / `_vs_peak_pct` | new field inventory, absolute units | 5 | Jul 2025 – Apr 2026 |
| `de_used_inv_vs_peak_pct` | used inventory vs cycle peak | 4 | Jan 2026 – Apr 2026 |

Every one of the 46 slide decks 2015–2026 that carries the dealer-inventory table was read. Prior-year
comparative columns were used to backfill 2013–2014 and the four decks whose table did not survive
markdown conversion. **59 of the slide values were re-parsed from disk by the builder and matched the
curated table exactly; the script fails hard on any mismatch.**

### The series, Jan / Apr / Jul / Oct (percent)

| year | 2WD 100+hp Jan / Apr / Jul / Oct | Combines Jan / Apr / Jul / Oct |
|---|---|---|
| 2013 | 18 / – / – / – | 10 / – / – / – |
| 2014 | 19 / 18 / 25 / – | 10 / 14 / 18 / 6 |
| 2015 | 24 / 23 / 25 / 24 | 10 / 17 / 19 / 6 |
| 2016 | 29 / 37 / 37 / 31 | 10 / 13 / 20 / 5 |
| 2017 | 38 / 32 / 31 / 25 | 14 / 21 / 26 / 5 |
| 2018 | 33 / 39 / 37 / 32 | 16 / 23 / 25 / 8 |
| 2019 | 38 / **44** / 41 / 27 | 19 / 23 / **36** / 9 |
| 2020 | 31 / 33 / 32 / 21 | 15 / 22 / 28 / 4 |
| 2021 | 28 / 25 / 21 / **12** | 12 / 22 / 23 / **3** |
| 2022 | 15 / 22 / 24 / 18 | 7 / 17 / 25 / 6 |
| 2023 | 25 / 29 / 30 / 23 | 16 / 23 / 17 / 4 |
| 2024 | 30 / 31 / 31 / 24 | 16 / 15 / 22 / 4 |
| 2025 | 34 / 31 / 31 / 23 | 11 / 17 / 26 / 8 |
| 2026 | 27 / **30** / – / – | 18 / **12** / – / – |

## 3. The two categories are seasonally different animals — read levels against the month, never against each other

Mean of the ratio by calendar month, 2013–2025:

| | Jan | Apr | Jul | Oct |
|---|---|---|---|---|
| 2WD 100+ hp (n=11–13/month) | 27.8 | 30.3 | 30.4 | 23.6 |
| Combines (n=12–13/month) | 12.8 | 18.9 | 23.8 | 5.7 |

Combines swing ~18 points across the year: they build into harvest and are flushed to near-zero at
fiscal year end (Oct median 5.5%, low 3%). Large tractors are nearly flat, 24–30%. The reason is
channel mechanics, not demand: **~90% of combine volume is locked in through the Early Order Program
before the year starts**, so combines are effectively build-to-order with a single delivery window,
whereas row-crop tractors run on a rolling order book and are the anchor of the dealer's trade ladder
— a dealer must keep tractors on the lot.

Consequence: the headline April 2026 comparison "2WD 30% vs combines 12%" says nothing about relative
health. The right comparison is against each category's own seasonal norm.

## 4. The April 2026 divergence, seasonally adjusted

Deviation from the 2013–2025 mean for that month (points):

| period | 2WD 100+hp | dev | Combines | dev |
|---|---|---|---|---|
| 2024-10 | 24 | +0.4 | 4 | −1.7 |
| 2025-01 | 34 | +6.2 | 11 | −1.8 |
| 2025-04 | 31 | +0.7 | 17 | −1.9 |
| 2025-07 | 31 | +0.6 | 26 | **+2.2** |
| 2025-10 | 23 | −0.6 | 8 | **+2.3** |
| 2026-01 | 27 | −0.8 | 18 | **+5.2** |
| 2026-04 | 30 | **−0.3** | 12 | **−6.9** |

This reframes the "divergence" and is the single most useful thing in this file:

1. **Large tractors are not "barely moved" — they are precisely, deliberately at normal.** Seven of the
   last eight quarters sit within ±1 point of the seasonal norm (2025-01 the only exception). That is
   the signature of a company running the line to a target, not drifting. It corroborates management's
   repeated "produce in line with retail demand" and their Q2 FY2026 phrase "in line with historical
   averages."
2. **Combines did not destock steadily — they were above normal into January 2026 and were cut violently
   in Q2 FY2026.** Oct 2025 +2.3, Jan 2026 +5.2, then Apr 2026 −6.9. That is a ~12-point
   seasonally-adjusted reduction in a single quarter, against a season that normally *builds*. April
   2026's 12% is the lowest April combine reading in the corpus (prior low 13%, April 2016).
3. **So the year-over-year "17 → 12" understates it.** April 2025 was itself −1.9 below normal. The
   destock is deeper than the y/y print implies, and it happened inside 2Q FY2026 — it was a drag on
   the quarter Deere has already reported, not a drag still to come in North America.

### Does the divergence persist across history?

No — and that is the point. Correlation of the two series:

| basis | r | n |
|---|---|---|
| levels | 0.55 | 50 |
| deviation from own month-mean | 0.49 | 50 |
| year-over-year change | **0.23** | 46 |

*Caveat: the 0.55 levels correlation is largely artifactual — both series fall together through the
2021–22 supply-constrained trough, so it is picking up the shared cycle, not a mechanical link. The
honest number is the y/y change correlation, 0.23 on n=46, which is weak.* Deere manages the two lines
independently and they routinely diverge: April y/y moves had opposite signs in 2016, 2017, 2024 and
2026. Combines lead the destock in this cycle (they are the easier line to turn off), but there is no
persistent structural spread. Treat the April 2026 pattern as episodic, not regime.

## 5. Target versus actual, in management's own words

Deere gives few numeric targets, but it gives clear directional ones, and one hard historical anchor.

| date | source | statement |
|---|---|---|
| May 2023 | `call-transcripts/2023-05-19__de-us-20230519-call-pres__46451.md` | 220+ and 4WD ratios "in the teens" at end-April 2023; **"Pre-COVID, both products would have been at least 10 points higher in the second quarter on an inventory to sales ratio basis"** — the clearest normal-level anchor in the corpus |
| Nov 2024 | `call-transcripts/2024-11-21__de-us-20241121-call-q4-pres__46452.md` | FY2024 close: 220+ hp at 10% I/S (−500bp y/y), only twice this low in 10 years; combines 4%. "Given the inventory reductions we've achieved, we expect to produce in line with retail demand in North America in 2025" |
| Nov 2024 | same | Industry I/S ratios "more than double Deere's" for both 100+hp tractors and combines |
| Aug 2024 | `call-transcripts/2024-08-15__de-us-20240815-call-qna__46445.md` | "if you look at 100+, we're around 30%-31% ... the industry ex Deere is closer to 70%" — corroborates the July 2024 slide print of 31% and gives the industry comparator |
| Nov 2025 | `call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md` | FY2025 close: combines 8%, 4WD 8%, 220+hp 12%; **220+hp absolute units "the lowest unit level we've seen in over 17 years"**; produced "roughly in line with retail demand for the full year" |
| Feb 2026 | `call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md` | NA new inventory "in a great position"; hold plan to produce in line with retail in FY2026. **Only exception: "combines in Brazil, where we're a bit higher than we want to be. We'll underproduce retail for Brazilian combines in our second and third quarters."** |
| May 2026 | `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` | "Inventories for both high horsepower tractors and combines are down more than 50% from their mid-2024 peak, with inventory to sales ratios in line with historical averages. With these improvements, our plan for the year is to continue to manage production in line with retail demand." |

**Note the basis difference:** the "220+ hp" figures management quotes are a *narrower internal cut*
than the AEM-based 100+ hp slide series and run ~10 points lower (Oct 2025: 220+hp 12% vs 100+hp 23%).
They are kept as a separate `series_id` in the CSV. Do not splice them.

## 6. Used equipment — the actual binding constraint, and it is clearing

Used inventory is disclosed only qualitatively but is discussed on every call, because in this cycle it,
not new inventory, has been the governor on retail. Q2 FY2026: *"the used inventory market, which has
really been a governor slowing down replacement demand, [has gotten] a lot healthier."*

| period | metric | source |
|---|---|---|
| Q3 FY2025 | Incremental dealer pool funds accrued to attack used; drove PPA price negative in the quarter. Used MY22/MY23 8R tractors and combines each −10%+ over the quarter | `call-transcripts/2025-08-15__de-us-20250815-call-q3-pres__143406.md` |
| Q1 FY2026 | Used combines ~15% below the March 2024 peak, model-year mix normal; used high-hp tractors >10% below their March 2025 peak; MY22/23 8R −20% sequentially | `call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md` |
| Q2 FY2026 | Used combines down mid-teens from March 2024 peak; used high-hp tractors down mid-teens from cycle peak **and down low single digits sequentially in a quarter that normally builds**; MY22/23 8R **−45%** from last year's peak; sprayers −30%; planters −50% | `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` |

The late-model 8R overhang was the specific blockage in the trade ladder. At −45% from peak it is
substantially cleared. This is the mechanism by which new-tractor retail can stabilise even with farm
economics weak — and it is why Deere can hold new-tractor field inventory at normal rather than cutting
further.

## 7. Construction & Forestry / Small Ag & Turf (qualitative only)

- **Small Ag & Turf:** Q1 FY2026 — new field inventory in *both* horsepower bands (<100hp and 100–220hp)
  "each about 40% lower year-over-year"; Q2 FY2026 — "favorable inventory levels are being maintained
  ... build in line with retail demand this fiscal year." Supports the SAT +~15% guide.
- **C&F / earthmoving:** Jul 2025 — NA field inventories 25–30% lower y/y. Q1 FY2026 — *competitors*
  "still have a lot of inventory in the field," which lags competitor price increases into transaction
  price. Deere's own C&F channel is lean; the inventory issue in C&F is a *pricing* headwind from rivals'
  stock, not a Deere volume constraint. Consistent with the CF +~20% guide.
- **Outside North America:** Europe production "largely aligned with retail demand"; Brazil expects to
  underproduce, "most notably in combines" — the one explicit above-target pocket, and Deere said it
  runs through Q3.

## 8. Answer to the key question — the state entering Q3 FY2026, by category

| category | state entering Q3 FY2026 | implication for Q3 shipments |
|---|---|---|
| **2WD/row-crop 100+ hp, NA** | **AT target.** Apr 2026 30% = −0.3 vs seasonal norm; 220+hp units lowest in 17+ years | Produce in line with retail. No incremental destock drag |
| **Combines, NA** | **BELOW target.** Apr 2026 12% = −6.9 vs seasonal norm; lowest April in the corpus | Destock complete and overshot; room to ship at or above retail |
| **4WD, NA** | **Lean.** FY2025 close 8% I/S | No drag |
| **Small Ag & Turf, NA** | **Lean**, −40% y/y both hp bands | Restocking in line with improving retail; supports SAT +~15% |
| **C&F, NA** | **Lean**, −25/−30% y/y as of Jul 2025 | Volume supportive; price pressure from *competitor* inventory |
| **Brazil combines** | **ABOVE target** — the sole exception | Explicit underproduction in Q2 **and Q3** FY2026. A known negative in the quarter |

**Deere enters Q3 FY2026 out of the destock, not in it.** For three consecutive calls management has
said "produce in line with retail demand," and the seasonally-adjusted series now corroborates it
rather than merely repeating it: tractors pinned within a point of normal for seven of eight quarters,
combines cut through normal to a corpus low.

### What that implies for the Q3 revenue line

The shipments-minus-retail wedge that crushed FY2025 (Q3 FY2025 PPA −16% y/y on deliberate
underproduction; 117 corpus mentions of "underproduction") has closed to roughly zero in North America.
Shipments should now track retail rather than fall faster than it.

Retail is still falling: AEM US ag tractor retail −18.4% y/y in June 2026, −17.3% across May–Jul,
−13.6% YTD, 4WD −24.6% YTD; Deere's own NA large-ag industry guide is −15% to −20%. So **PPA revenue
should still be down year over year in Q3 — but by materially less than the −16% of Q3 FY2025**, because
the incremental destock drag is gone. That is arithmetically what the unchanged FY2026 guide requires:
PPA −5% to −10% for the full year against H1 PPA running −14%/−16% implies H2 PPA roughly flat to
modestly down.

Three specific, checkable points for the 20 August print:

1. **Seasonality gives a testable prediction for the Jul-2026 slide.** Median Apr→Jul move is 0.0 points
   for 2WD and +5.5 for combines. Off the April base that implies **2WD ~30% (vs 31% LY) and combines
   ~17–18% (vs 26% LY)**. A combine reading materially above ~18% would mean Deere shipped ahead of
   retail into the channel — better for Q3 revenue, worse for Q4. Below ~15% would mean the destock
   continued and Q3 PPA disappoints.
2. **Q3 is structurally the ratio peak, not the cut.** The big flush is Jul→Oct (mean −18 points for
   combines, −7 for 2WD). Deere concentrates destocking in Q4. This is a reason not to expect a
   surprise Q3 production cut in North America.
3. **The offsets are real.** SAT and CF dealer inventory are lean and their retail is inflecting
   positively (Apr 2026: NA turf/utility and earthmoving both "up low double digits"; Europe ag tractors
   and combines both "up double digits"). Those segments carry the +15%/+20% guides and their channel
   position supports shipping to them.

**Net read: dealer inventory is a support for Q3 FY2026 shipments, not a drag — for the first time in
roughly two years. The residual negatives are Brazilian combines (explicit, quantified as a Q3
underproduction) and the falling retail denominator itself, not dealer destocking in North America.**

## 9. Data quality and what is not here

- **Verified:** 59 slide-table values re-parsed programmatically from the corpus and matched. The two
  anchor values (Apr 2026: 2WD 30% vs 31%, combines 12% vs 17%) reconcile exactly.
- **Reconstructed from prior-year comparative columns** (marked in `notes`): 2013–2014 observations and
  Oct-2015 / Oct-2016. These are Deere's own figures, just read from a later deck.
- **Low confidence, flagged in `notes`:** Oct-2014 and Oct-2015 combines (6%). Both decks' tables were
  scrambled by the markdown conversion and the two available sources disagree between 5% and 6%. Kept
  because they are directionally certain (single-digit October trough) and immaterial to the forecast.
- **OCR repairs, each corroborated by a later deck's comparative column:** Jul-2015 combines rendered as
  "91%" is 19% (confirmed by the Jul-2016 deck); Jul-2014 rendered "81%" is 18%.
- **Unreconciled restatements** (contemporaneous value kept, later value noted): Jul-2019 2WD 41% vs 42%;
  Jan-2020 2WD 31% vs 32%; Oct-2018 4WD 27% vs 22%.
- **Missing, not zero:** 4WD is disclosed on the slide only intermittently (12 observations); there is no
  4WD print for Apr 2026. Oct-2014 2WD 100+hp is absent. No dealer-inventory ratios are disclosed for
  Europe, Brazil, C&F or Small Ag & Turf — those are qualitative only, and are reported as such above.
- **Not fabricated:** no financials for private Deere dealer groups (RDO, Ag-Pro, Van Wall, Sydenstricker
  Nobbe, Hutson, Ziegler). Titan Machinery is a CNH dealer and is not used here as a Deere signal.
- **No Q3 FY2026 actuals.** The last observation in every series is April 2026 or earlier.
