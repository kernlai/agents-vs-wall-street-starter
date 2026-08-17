# Deere & Company (NYSE: DE) — FY2026 Q3 Regional Roll-Up

**As of 16 August 2026. Deere has NOT reported FY2026 Q3.** The Q3 earnings call is 09:00 US Central,
Thursday 20 August 2026 — after this document. **No FY2026 Q3 actuals exist**, none were found in the
corpus or on the web by any of the six desks, and every Q3 FY2026 figure below is a forecast. Anything
that looks like a Q3 FY2026 actual is a misreading.

**The quarter:** approximately 4 May 2026 – 2 August 2026 (Q2 FY2026 ended 2026-05-03).

**Basis:** all matrix figures are the **ASC 606 revenue-from-contracts-with-customers footnote**
(the segment × geography disclosure), *not* 8-K segment net sales. Conversions to the 8-K basis are
explicit and labelled. See §2c.

**Reproducibility:** every number in §1–§3 and §5 is produced by
`/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/regional_rollup.py`
(`python3 regional_rollup.py`). It asserts the Q3 FY2025 comparative matrix against the published
column and grand totals before it computes anything, and it re-derives the FY2025 full-year and
H1 FY2026 8-K net sales from the quarterly 8-Ks. It also emits
`data/deere/regional/rollup_matrix_q3fy2026.csv` in the team's tidy-long format.

**Comparative source (actuals, verified line-by-line):**
`challenge/offline-data/deere/filings/2025-08-14__de-us-20250814-q3-10q__155834.md`, three months
ended 27 July 2025, lines 594–606. All 24 Q3 FY2025 comparatives were re-extracted from that table for
this roll-up rather than taken from the desk briefings; all 24 matched what the desks used.

---

## Headline

| | ASC 606 / worldwide net sales & revenues (USDm) |
|---|---|
| Q3 FY2025 actual | **12,018** |
| **Q3 FY2026 bottom-up central** | **12,363  (+2.9% YoY)** |
| Bottom-up band (quadrature over regions) | 11,881 – 12,845 |
| Guidance-implied cross-check | 12,359 (band 11,637 – 13,168) |
| Simple-seasonality cross-check | 12,589 (band 11,541 – 14,101) |

Rolled forward on management's own stated Q3/Q4 cadence, the bottom-up implies FY2026 net sales of
PPA −7.9%, SAT +14.9%, CF +20.4% — **inside all three FY2026 segment guides**, with SAT and CF landing
essentially on the point guide and PPA in the middle-to-weak half of its −5 to −10% band.

The three checks agree to within 230m (1.9%). That closeness is real but partly luck — see §3.

---

## 1. Q3 FY2026 segment × geography matrix forecast (ASC 606, USDm)

Q3 FY2025 column = **actual**, from the 10-Q. Q3 FY2026 column = **forecast**.

| Geography | Segment | Q3 FY2025 actual | Q3 FY2026 central | YoY % | Desk low | Desk high | Desk conf. |
|---|---|---:|---:|---:|---:|---:|---|
| United States | PPA | 1,684 | 1,440 | −14.5% | 1,300 | 1,590 | low |
| United States | SAT | 1,537 | 1,700 | +10.6% | 1,600 | 1,790 | medium |
| United States | CF | 1,687 | 2,050 | +21.5% | 1,900 | 2,180 | medium |
| United States | FS | 1,100 | 1,070 | −2.7% | 1,030 | 1,110 | high |
| Canada | PPA | 335 | 340 | +1.5% | 295 | 390 | low |
| Canada | SAT | 148 | 175 | +18.2% | 158 | 195 | medium |
| Canada | CF | 222 | 200 | −9.9% | 170 | 240 | low |
| Canada | FS | 190 | 196 | +3.2% | 186 | 208 | medium |
| Western Europe | PPA | 677 | 695 | +2.7% | 650 | 745 | medium |
| Western Europe | SAT | 757 | 810 | +7.0% | 765 | 860 | medium |
| Western Europe | CF | 550 | 590 | +7.3% | 555 | 630 | medium |
| Western Europe | FS | 45 | 53 | +17.8% | 49 | 57 | high |
| Central Europe & CIS | PPA | 301 | 308 | +2.3% | 265 | 345 | low |
| Central Europe & CIS | SAT | 130 | 120 | −7.7% | 100 | 140 | low |
| Central Europe & CIS | CF | 103 | 110 | +6.8% | 96 | 124 | medium |
| Central Europe & CIS | FS | 2 | 2 | 0.0% | 1 | 3 | medium |
| Latin America | PPA | 1,055 | 820 | −22.3% | 760 | 900 | medium |
| Latin America | SAT | 124 | 136 | +9.7% | 125 | 148 | medium |
| Latin America | CF | 252 | 285 | +13.1% | 265 | 305 | medium |
| Latin America | FS | 28 | 33 | +17.9% | 30 | 36 | medium |
| Asia/Africa/Oceania/ME | PPA | 332 | 355 | +6.9% | 325 | 390 | low |
| Asia/Africa/Oceania/ME | SAT | 393 | 440 | +12.0% | 415 | 470 | medium |
| Asia/Africa/Oceania/ME | CF | 313 | 380 | +21.4% | 355 | 410 | medium |
| Asia/Africa/Oceania/ME | FS | 53 | 55 | +3.8% | 53 | 57 | high |

**Trailing-trend fallback used on 0 of 24 cells.** Every cell received an explicit, quantified desk view
with a stated low/central/high, and each desk anchored on the correct Q3 FY2025 actual. Nothing here is
a mechanical extrapolation filling a hole. That is unusual and worth stating plainly, because it means
the roll-up inherits the desks' judgement everywhere and cannot hide behind "the trend did it."

Two cells nevertheless deserve the label *effectively trend-based*, because the desk said so itself:

- **Latin America FS (33)** — the desk described it as "purely a run-rate call": a straight extension of
  the post-deconsolidation 28/32/32/32 series after Deere sold 50% of Banco John Deere to Bradesco.
- **Central Europe & CIS FS (2)** — the desk states no inference is possible from the series; it is
  rounding noise on a 540m region.

---

## 2. Totals and basis reconciliation

### 2a. Row totals by geography (ASC 606, USDm)

| Geography | Q3 FY2025 actual | Q3 FY2026 central | YoY % | Low | High | Share of total |
|---|---:|---:|---:|---:|---:|---:|
| United States | 6,008 | 6,260 | +4.2% | 5,830 | 6,670 | 50.6% |
| Canada | 895 | 911 | +1.8% | 809 | 1,033 | 7.4% |
| Western Europe | 2,029 | 2,148 | +5.9% | 2,019 | 2,292 | 17.4% |
| Central Europe & CIS | 536 | 540 | +0.7% | 462 | 612 | 4.4% |
| Latin America | 1,459 | 1,274 | −12.7% | 1,180 | 1,389 | 10.3% |
| Asia/Africa/Oceania/ME | 1,091 | 1,230 | +12.7% | 1,148 | 1,327 | 9.9% |
| **Total** | **12,018** | **12,363** | **+2.9%** | **11,448** | **13,323** | 100.0% |

### 2b. Column totals by segment (ASC 606, USDm)

| Segment | Q3 FY2025 actual | Q3 FY2026 central | YoY % | Low | High |
|---|---:|---:|---:|---:|---:|
| PPA | 4,384 | 3,958 | −9.7% | 3,595 | 4,360 |
| SAT | 3,089 | 3,381 | +9.5% | 3,163 | 3,603 |
| CF | 3,127 | 3,615 | +15.6% | 3,341 | 3,889 |
| FS | 1,418 | 1,409 | −0.6% | 1,349 | 1,471 |
| **Total** | **12,018** | **12,363** | **+2.9%** | **11,448** | **13,323** |

The Low/High columns are the arithmetic sums of the 24 desk lows and 24 desk highs. **They are not a
confidence interval** — they require all 24 cells to miss in the same direction at once. Use the
quadrature band in §3(c) instead.

### 2c. Reconciliation to the "worldwide net sales and revenues" reporting basis — the 104m gap

The reconciliation warning in the brief is real but is narrower than it looks, and the roll-up turns on
getting this right. Two facts, both verified programmatically over the seven quarters where both
disclosures exist (FY2024 Q1/Q3, FY2025 Q1/Q2/Q3, FY2026 Q1/Q2):

**Fact 1 — the grand total ties exactly.** The ASC 606 geographic-matrix *grand total* equals the 8-K
*worldwide net sales and revenues* to the dollar in every quarter tested: Q3 FY2025 12,018 = 12,018;
Q2 FY2026 13,369 = 13,369; Q1 FY2026 9,611 = 9,611; and so on. **So the bottom-up 606 grand total of
12,363 requires no adjustment at all to be a "worldwide net sales and revenues" forecast.** The gap
does not live at the total level.

**Fact 2 — the gap lives in the segment split, and it is a roughly constant number of dollars, not a
percentage.** The 606 segment columns additionally carry the "financial products" and "other" revenue
recorded inside each equipment segment; the 8-K segment "net sales" lines exclude them.

| Quarter | PPA wedge | SAT wedge | CF wedge | Equipment total |
|---|---:|---:|---:|---:|
| FY2024 Q1 | +194 | +67 | +62 | +323 |
| FY2024 Q3 | +143 | +75 | +58 | +276 |
| FY2025 Q1 | +106 | +59 | +64 | +229 |
| FY2025 Q2 | +96 | +52 | +59 | +207 |
| FY2025 Q3 | +111 | +64 | +68 | +243 |
| FY2026 Q1 | +106 | +56 | +64 | +226 |
| FY2026 Q2 | +104 | +57 | +64 | +225 |

Across the last five quarters the PPA wedge sits in a 96–111 band while PPA revenue itself ranges from
3,269 to 5,326. It is a **constant, not a 2.3% ratio**. Applying it as a percentage — which two desks
did (Canada explicitly applied "a ~2.3–2.6% uplift"; Latin America referenced the 2.3% gap) — would
overstate the wedge by ~15m on a large PPA quarter and understate it on a small one. Immaterial at the
cell level, but it is the correct treatment and the script uses median-of-last-five constants:
**PPA +106, SAT +57, CF +64, equipment total +227.**

| Line | Q3 FY2026 forecast (USDm) |
|---|---:|
| 606 PPA column | 3,958 |
| 606 SAT column | 3,381 |
| 606 CF column | 3,615 |
| 606 equipment subtotal | 10,954 |
| less basis wedge | (227) |
| **= Equipment operations NET SALES (8-K basis)** | **10,727** |
| 606 FS column | 1,409 |
| plus wedge, reported as finance and other revenue | 227 |
| **= Finance and other revenues** | **1,636** |
| **= WORLDWIDE NET SALES AND REVENUES** | **12,363** |

### 2d. Implied 8-K segment net sales and the FY2026 guide check

Q4 is implied by holding the Q3 share of H2 that management described on the Q2 call (see §3a).

| Segment | 606 | wedge | 8-K net sales | Q3 FY2025 8-K | YoY % | implied Q4 | implied FY2026 | vs FY2025 | Guide |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PPA | 3,958 | (106) | 3,852 | 4,273 | −9.9% | 4,432 | 15,950 | −7.9% | Down 5–10% ✓ |
| SAT | 3,381 | (57) | 3,324 | 3,025 | +9.9% | 2,775 | 11,752 | +14.9% | Up ~15% ✓ |
| CF | 3,615 | (64) | 3,551 | 3,059 | +16.1% | 3,696 | 13,707 | +20.4% | Up ~20% ✓ |

This is the strongest single validation in the roll-up, and it was not engineered: six desks working
independently on geographies produced a set of numbers that, aggregated by segment and rolled to a full
year on management's own cadence language, sit inside all three guides. SAT (+14.9% vs "~15%") and CF
(+20.4% vs "~20%") are close enough to be coincidence; PPA at −7.9% is the informative one, because it
says the desks collectively believe Deere lands in the weaker half of the large-ag guide.

Also consistent with management's total-company cadence ("slightly higher revenue in the back half,
with the fourth quarter being higher than the third quarter",
`call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` line 143): the bottom-up implies
Q3 net sales 10,727 and Q4 10,903, H2 21,630 against H1 19,779 — back half higher, Q4 higher than Q3. ✓

---

## 3. Three sanity checks, side by side

**Do not average these.** They are shown at full width, with the disagreements named.

| Check | Low | Central | High | YoY | Segment detail |
|---|---:|---:|---:|---:|---|
| **(a) Guidance-implied** | 11,637 | **12,359** | 13,168 | +2.8% | PPA 3,987 / SAT 3,384 / CF 3,591 / FS 1,397 |
| **(b) Simple seasonality** | 11,541 | **12,589** | 14,101 | +4.7% | total level only |
| **(c) Regional bottom-up** | 11,881 | **12,363** | 12,845 | +2.9% | PPA 3,958 / SAT 3,381 / CF 3,615 / FS 1,409 |

Spread between the three centrals: **230m, 1.9%** of the bottom-up total.

### (a) Guidance-implied — 12,359

FY2026 8-K guide applied to FY2025 actuals, less H1 FY2026 actual, split Q3/Q4 on the historical
seasonal pattern **adjusted for management's explicit cadence commentary**, then converted to the 606
basis by adding the wedge back.

Historical Q3 share of H2 net sales (8-K basis), FY2021–FY2025:

| Segment | FY21 | FY22 | FY23 | FY24 | FY25 | median | used | why the adjustment |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| PPA | 47.7% | 45.1% | 49.4% | 54.2% | 47.4% | 47.7% | **46.5%** | "Q4 a bit stronger than Q3… more Waterloo large tractor shipments to North America in the back half… that's abnormal for us" |
| SAT | 52.8% | 50.6% | 54.7% | 57.0% | 55.2% | 54.7% | **54.5%** | "pretty normal seasonality… a little bit of a step down in Q3 and another step down in Q4" |
| CF | 51.8% | 49.2% | 50.0% | 54.8% | 47.5% | 50.0% | **49.0%** | "fairly balanced between the two… maybe a little bit stronger in the fourth quarter than Q3, but overall pretty close" |

Quotes from `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` lines 95–97 and 125.
The mgmt adjustment is small (≈1pt each) but it is the difference between a guidance-implied PPA of
4,088 (naive median) and 3,987 (adjusted) — 100m, and the adjustment is in the direction that *narrows*
the gap to the bottom-up rather than widening it, so it is not a thumb on the scale.

| Segment | FY guide (8-K) | implied H2 | Q3 share | Q3 606 low/central/high |
|---|---|---|---|---|
| PPA | 15,580 – 16,445 | 7,914 – 8,779 | 45.0/46.5/48.0% | 3,667 / **3,987** / 4,320 |
| SAT | 11,553 – 11,962 | 5,900 – 6,309 | 53.0/54.5/57.0% | 3,184 / **3,384** / 3,653 |
| CF | 13,431 – 13,886 | 6,971 – 7,426 | 48.0/49.0/50.0% | 3,410 / **3,591** / 3,777 |
| FS | *no revenue guide* — the guide is FS **net income** ~$860m | | trailing YoY −3.0/−1.5/0.0% | 1,375 / **1,397** / 1,418 |
| **Total** | | | | 11,637 / **12,359** / 13,168 |

**Weakness of this method:** the PPA guide band alone is 865m wide at the FY level and 650m at the Q3
level, so (a) is a wide net, and the fact that (c) lands 4m from its midpoint is coincidence, not
corroboration. What (a) *does* establish, non-trivially, is that (c) is nowhere near the edges of what
management has publicly committed to.

### (b) Simple seasonality — 12,589

Two variants, because the literal reading is biased.

**(b1) Q2→Q3 sequential ratio on the Q2 FY2026 actual of 13,369** *(preferred)*:

| FY | Q2 (606) | Q3 (606) | Q3/Q2 |
|---|---:|---:|---:|
| FY2021 | 12,058 | 11,527 | 0.956 |
| FY2022 | 13,370 | 14,102 | 1.055 |
| FY2023 | 17,387 | 15,801 | 0.909 |
| FY2024 | 15,235 | 13,152 | 0.863 |
| FY2025 | 12,763 | 12,018 | 0.942 |

n=5. Median 0.942 → **12,589**. Mean 0.945 → 12,632. Full observed ratio range → 11,541–14,101.

**(b2) Q3 FY2025 grown at a trend YoY rate** *(the literal brief, flagged as biased)*:

| Trend rate | rate | 12,018 grown at it |
|---|---:|---:|
| Q1 FY2026 YoY | +13.0% | 13,576 |
| Q2 FY2026 YoY | +4.7% | 12,589 |
| H1 FY2026 YoY | +8.0% | 12,984 |

The bias is a comp artefact and it is material: Q1 and Q2 FY2026 grew against FY2025 quarters that were
themselves down 30% and 16% YoY, whereas **Q3 FY2025 was down only 9%**. Applying an H1-derived growth
rate to the Q3 comp silently assumes the Q3 comp is as easy as H1's. It is not. That inflates (b2) by
roughly 400–1,000m. I therefore weight (b1) inside (b), and note that (b1) and the Q2-only variant of
(b2) coincide exactly at 12,589 — not a coincidence, since applying FY2025's own Q2→Q3 ratio to the
current Q2 and applying FY2025's Q2 YoY rate to FY2025's Q3 are the same arithmetic.

**Weakness of this method:** n=5, spanning one boom and one bust, with an observed ratio range of
0.863–1.055 — a 2,560m span. It carries no information about *this* quarter. It is a floor-and-ceiling
check, not a forecast.

### (c) Regional bottom-up — 12,363

Sum of the 24 desk cells. **Band: 11,881 – 12,845 (±3.9%)**, computed by adding the six *regional*
row-ranges in quadrature: within a region cells are strongly correlated (one FX rate, one farm economy,
one order book), so their ranges add arithmetically; across regions they are treated as independent.
That independence assumption is the weak point and is only partly true — US large ag, Brazilian large
ag and global roadbuilding are not orthogonal, so **read ±482m as a floor on the uncertainty, not a
ceiling.** The naive sum-of-lows to sum-of-highs is 11,448–13,323 and is not usable.

### Where they disagree, and which I trust

| Segment | (a) guidance-implied | (c) bottom-up | (c) − (a) | inside (a)'s band? |
|---|---:|---:|---:|---|
| PPA | 3,987 | 3,958 | −29 | yes |
| SAT | 3,384 | 3,381 | −3 | yes |
| CF | 3,591 | 3,615 | +24 | yes |
| FS | 1,397 | 1,409 | +12 | yes |
| **Total** | **12,359** | **12,363** | **+4** | yes |

At the segment level the two methods are within 30m everywhere. **The real disagreement is
(b) versus the other two: +226m.** Its source is identifiable, not mysterious. (b) is a pure
total-level ratio that has no way to know that (i) the Western Europe FX translation tailwind collapses
from +8.2pp in Q2 to +0.3pp in Q3, (ii) Latin America PPA faces its hardest comp of the year against a
quarter that was itself +25.4%, and (iii) Q3 FY2025 was a much less depressed comp than Q1/Q2 FY2025.
All three are Q3-specific and all three push the answer down from a naive seasonal read. **(b) is
therefore biased high here, and its 226m of excess is almost exactly the sum of what the WE and LatAm
desks documented.**

**I trust (c), the bottom-up, most**, for three reasons:

1. It is the only one of the three with *segment × geography resolution*, which is the level at which
   the quarter's actual drivers operate. The two largest YoY movements in the matrix — Latin America
   PPA at −22.3% and US CF at +21.5% — are invisible to (a) and (b) and would be smoothed away.
2. It is the only one built on *observed in-quarter data*: AEM monthly retail through July, FADA India
   registrations for all three months, CEMA April–July, USD/BRL and EUR/USD quarterly averages over a
   **completed** window, CONAB's 13 August survey, ABIMAQ June. (a) is a guide set on 21 May, before
   most of the quarter happened. (b) is history.
3. It survives the guide test in §2d without adjustment, and it is the *lowest* of the three, which is
   the right direction given that each desk independently reported shading conservative.

**But I hold it with a specific asymmetry.** (a)'s midpoint on PPA is 29m above (c), (b) is 226m above
(c), and the single largest identifiable upside error in the file — the US-PPA residual in §4.1 — is
worth roughly +100m. Nothing of comparable size points down. **If the bottom-up is wrong, it is more
likely wrong low than wrong high**, and a print of 12,500–12,600 should not be treated as a surprise.

---

## 4. Divergences

These are where the edge is. Listed most load-bearing first.

### 4.1 Two desks read the same slide with opposite signs — and one of them is wrong

This is the most consequential unresolved conflict in the file, because it inverts the picture of the
largest ag market.

The **US desk** filed a sign correction: the Q2 FY2026 deck's April rolling-3-month retail table
(`slides/2026-05-21__de-us-20260521-slide__1042212.md` lines 186–192) renders the industry column as
bare positives (12%, 4%, 14%, 24%, 5%), but **those figures are negative** — the markdown conversion
stripped the minus signs.

The **Canada desk** took them as positive, and built an argument on it: *"Deere's own April
rolling-3-month slide shows US+Canada industry 4WD +24% and 100+hp +14%, i.e. the US is carrying that
number."* The task brief as circulated also carries the positive reading.

**The US desk is right.** Three independent confirmations:

1. *Internal incoherence of the positive reading.* Deere's own adjacent column reads "Down more than
   the industry" for 100+hp and "Down less than the industry" for 4WD. Those phrases are only coherent
   against a declining industry.
2. *The same table in prior quarters.* The August 2025 deck shows 4WD "42%" with Deere "Less than the
   industry"; the November 2025 deck shows 4WD "50%" with Deere "In-line with the industry". A +50%
   industry 4WD quarter in the FY2025 trough is not possible. The renderer strips minus signs on this
   table every quarter.
3. *External corroboration.* AEM actuals: 100+hp 2WD −10.3% in May and −15.5% YTD-July, 4WD −38.7% in
   July, self-propelled combines −56.1% in May.

**Correct reading: US & Canada ag industry retail DOWN 12% / 4% / 14% / 24% / 5%.**

**What it changes.** Canada's bearish-relative-to-US case weakens: if the blended US+Canada 4WD industry
is −24%, then Canada's −22.6% YTD 4WD is roughly *in line* with the blend, not conspicuously worse. That
argues Canada PPA belongs above 340, toward the upper half of its 295–390 range. I have **not**
overridden the cell — the desk owns it, and its other evidence (Canada PPA −25.8% in Q2, −31.5% in
Q3 FY2025, a 1.6% FX headwind) stands independently — but the team should challenge Canada PPA upward,
not downward. Any other desk that took the column as growth has the US large-ag picture inverted.

### 4.2 The US-PPA residual: the desks collectively imply a *higher* US PPA than the US desk carried

The US desk's bottom-up residual method assumed values for the other five regions. Those desks then
filed different numbers.

| Region | US desk ASSUMED | region desk FILED | diff |
|---|---:|---:|---:|
| Canada | 295 | 340 | +45 |
| Western Europe | 711 | 695 | −16 |
| Central Europe & CIS | 331 | 308 | −23 |
| Latin America | 897 | 820 | **−77** |
| Asia/Africa/Oceania/ME | 359 | 355 | −4 |
| **Sum of other five** | **2,593** | **2,518** | **−75** |

On the US desk's own assumed global 606 PPA of 4,060, its residual for the US was 1,467. **With what the
other five desks actually filed, the same residual is 1,542** — 102m *above* the 1,440 the US desk
carried, though still inside its 1,590 high.

So the roll-up contains a genuine internal tension: either global PPA is ~4,060 and US PPA is ~1,542
(total ~12,465), or US PPA is 1,440 and global PPA is 3,958, which implies FY2026 PPA at −7.9% to −9%,
the weaker half of the guide. **The desks cannot both be right.** I have carried the desks as filed
(giving 3,958) because I trust the LatAm desk's specific, dateable evidence — the Horizontina layoff
running the whole quarter, ABIMAQ June −22.3% — more than I trust the US desk's assumption of LatAm 897.
But this is the single largest known upside risk to the total, and it is the first thing to challenge.

### 4.3 Canada CF: a desk forecasting −9.9% against company guidance of ~+20%

The sharpest desk-versus-company divergence in the file, and one of the sharpest desk-versus-desk ones:
Canada CF −9.9% while the US desk has US CF +21.5% and AAOME has +21.4%, in a segment the company guides
up ~20% for the year with global roadbuilding raised to ~+10%.

The Canada desk's case is specific and evidence-backed, not a hunch: Canada's CF share of global fell
from 5.92% (H1 FY2025) to 4.76% (H1 FY2026), a 20% relative decline; Canadian CF is already down 39%
from FY2023 (1,221) to FY2025 (743) while global CF inflected up; Canadian lumber production was −5.8%
YoY in April and −8.1% in May 2026 against ~35.2% combined AD/CVD plus 10% Section 232 softwood tariffs
unresolved through the quarter; and Deere cut global forestry to −5% at Q2. Canada is over-indexed to
forestry inside CF.

**I carry it.** The share-decline evidence is a two-year trend in Deere's own disclosure, not a
one-quarter blip, and it is corroborated by an independent physical series (StatCan lumber production).
But it is a 35%-of-cell range on a low-confidence call, and the desk's own bull case (Canada
participates in the +60%-since-November North American earthmoving order book) prints 240. **If Canada
CF is wrong it is wrong low, by up to 40m.**

### 4.4 Central Europe & CIS SAT: a desk explicitly overriding the company's +15% SAT guide

CE/CIS SAT −7.7% against a company SAT guide of ~+15%. The desk's reasoning is that the +15% guide is
driven by North American turf and compact utility, not CEE small ag, and that Q3 FY2025's 130 was an
outlier — the highest SAT/Western-Europe-SAT ratio in the entire sample (17.2% vs a trailing-4Q 15.3%
and 14.6% in Q2 FY2026).

**This one is genuinely unresolvable from disclosure**, and the desk says so: if the 130 was a new
run-rate the cell prints 140+; if it was destocking catch-up it prints 100. That is a 40m two-sided
swing on a 120m cell (33%). It is small enough not to matter to the total and honest enough to leave
alone. The company-guide override is legitimate: the guide is global and the geography is not.

### 4.5 Europe: retail up double digits against an industry outlook of flat to +5% — and the desks agree it doesn't help Q3

Deere's April 2026 internal European retail has tractors and combines **both up double digits**
(`slides/2026-05-21__de-us-20260521-slide__1042212.md` lines 208–211), against a published FY2026
industry outlook of **Europe ag flat to +5%**. That is a large, explicit share gain and it is
corroborated independently — UK registrations +22.3% in H1 2026, Ireland +12%, and Deere's own +8.7%
constant-currency Q2 print.

The interesting thing is that **both European desks nonetheless forecast decelerating growth**: Western
Europe +5.9% total and PPA only +2.7%; Central Europe & CIS +0.7%. This is *not* a contradiction, and
the reason is the single most under-appreciated number in the roll-up:

**The European FX translation tailwind collapses from +8.2pp in Q2 FY2026 to +0.3pp in Q3.** Both desks
computed this independently and got the same answer (WE basket +0.3pp; CE +0.4pp), because the euro's
re-rating had already happened by the Q3 FY2025 comparative (EUR/USD averaged 1.1532 in the Q3 FY2026
window vs 1.1488 a year earlier). Roughly eight points of European growth evaporate for reasons that
have nothing to do with demand. Layer on the hardest comp of the year — Q3 FY2025 Western Europe was
+30.1% reported / +22.0% constant currency — and mid-single-digit reported growth is what genuine
double-digit share gain looks like this quarter.

**Where the two European desks quietly disagree:** WE reads the CEMA business-climate collapse
(−6 April, −9 May, **−20 June**, −19 July, "back into recession") as principally a Q4 FY2026 / FY2027
risk because CEMA measures forward order expectations and the Q3 order book was pre-sold. CE/CIS agrees
Q3 shipments were locked but reads its own late-July shock — the collapse of Ukrainian deepwater exports
from 22 July — as *net positive* for EU-CEE farm income, because it removes the Ukrainian grain-inflow
pressure that Deere management explicitly blamed for depressed Polish, Romanian and Hungarian farm
incomes. So the same fortnight is a demand negative in one desk's model and a farm-income positive in
the other's. Both may be right; they concern different countries inside two lines that Deere does not
split.

### 4.6 Latin America: a desk more bearish than the company's own South America unit outlook

Deere guides South America ag (tractors + combines) **down ~15%**. The LatAm desk forecasts PPA
**−22.3% in USD**, and because USD/BRL delivered a **+10.0% translation tailwind**, that is an implied
**ex-FX local-currency decline of about −29%** — roughly double the company's unit outlook.

The desk defends the gap on mix and on a company-specific supply decision, not on a different view of
the market: Deere's Horizontina combine plant was under collective holidays from 12 March and formal
contract suspension from 1 April for two-to-five months with output down ~30%, which is the physical
expression of management's stated plan to "underproduce retail demand, most notably in combines" in
Brazil; the safrinha harvest ran ~4 weeks late (42% complete mid-July vs 74% LY); and ABIMAQ has June
machinery sales −22.3% YoY with buyers explicitly deferring into the 30 June Plano Safra announcement.
Deere's mix skews to the worst-hit categories.

**This is a coherent divergence and I carry it**, but note the shape: it says the *company* underperforms
its own industry outlook by ~14pp on a deliberate supply choice. That is a claim about Deere, not about
Brazil, and it is falsifiable on 20 August. The desk also flags that it could not source Brazilian
tractor/combine retail units for May–July (ANFAVEA returns HTTP 406), which it says is worth 50–70m on
the call.

### 4.7 Asia: management's "Asia roughly flat" was set before the monsoon failed, and the demand data went the other way

Deere upgraded Asia ag three times in six months to "roughly flat" on 21 May — *before* the June
rainfall failure was known (June ~60% of LPA, driest in over a decade; cumulative −12% at the 2 August
quarter-end). Yet Indian tractor retails **accelerated straight through it**: FADA registrations +11.2%
May, +25.3% June, +28.1% July, on the September 2025 GST cut from 12% to 5%.

So the company outlook is wrong in *both* directions at once — too pessimistic on demand, too optimistic
on the weather. The desk's resolution is Deere-specific and is the highest-quality single piece of
evidence any desk produced: **John Deere India's own retail registrations for all three months of the
exact window** (6,039 / 7,165 / 8,087), growing +11.7% against an industry up +22.1%, with share falling
0.65pp to 7.07% because Deere skews higher-horsepower while the surge is affordability-led. Net of a
−10.3% INR translation drag, most of the unit growth disappears in reported dollars.

**The asymmetry to watch on 20 August is commentary, not revenue.** Management will be guiding with a
−12% monsoon and a below-normal El Niño-influenced Aug–Sep forecast in hand.

### 4.8 FX is the largest single non-demand driver in the quarter and it points in six directions

Not a disagreement, but it needs to be on one page because no single desk sees it:

| Region | Q3 FY2026 translation effect | Source desk |
|---|---|---|
| Western Europe | **+0.3%** (from +8.2pp in Q2) | EUR/GBP/SEK basket, 13-week averages |
| Central Europe & CIS | **+0.4%** (from +8.4pp in Q2) | USD/EUR 1.1532 vs 1.1488 |
| Canada | **−1.6%** | DEXCAUS 1.3964 vs 1.3744 |
| Latin America | **+10.0%** | DEXBZUS 5.0756 vs 5.5846, 62 daily obs |
| Asia/Africa/Oceania/ME | **mixed, net negative** | INR −10.3%, JPY −9.6% vs AUD +8.7%, CNY +6.1% |
| United States | n/a | — |

The two largest are **Europe losing eight points** and **Latin America gaining ten**. They roughly
offset at the company level, which is exactly why they are invisible in checks (a) and (b) and exactly
why the bottom-up is the method to trust.

---

## 5. Weakest cells

Ranked by the **absolute dollar width** of the desk's own range, because that is what moves the grand
total. A cell can be wild in percentage terms and irrelevant in dollars (Central Europe FS: 100% range
width, 2m of revenue).

| # | Geography | Segment | Central | Width $m | % of cell | Cell % of total | Width % of total | Conf. |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | United States | PPA | 1,440 | 290 | 20.1% | 11.6% | 2.35% | low |
| 2 | United States | CF | 2,050 | 280 | 13.7% | 16.6% | 2.26% | medium |
| 3 | United States | SAT | 1,700 | 190 | 11.2% | 13.8% | 1.54% | medium |
| 4 | Latin America | PPA | 820 | 140 | 17.1% | 6.6% | 1.13% | medium |
| 5 | Canada | PPA | 340 | 95 | 27.9% | 2.8% | 0.77% | low |
| 6 | Western Europe | PPA | 695 | 95 | 13.7% | 5.6% | 0.77% | medium |
| 7 | Western Europe | SAT | 810 | 95 | 11.7% | 6.6% | 0.77% | medium |
| 8 | United States | FS | 1,070 | 80 | 7.5% | 8.7% | 0.65% | high |
| 9 | Central Europe & CIS | PPA | 308 | 80 | 26.0% | 2.5% | 0.65% | low |
| 10 | Western Europe | CF | 590 | 75 | 12.7% | 4.8% | 0.61% | medium |
| 11 | Canada | CF | 200 | 70 | 35.0% | 1.6% | 0.57% | low |
| 12 | Asia/Africa/Oceania/ME | PPA | 355 | 65 | 18.3% | 2.9% | 0.53% | low |
| 13 | Asia/Africa/Oceania/ME | SAT | 440 | 55 | 12.5% | 3.6% | 0.44% | medium |
| 14 | Asia/Africa/Oceania/ME | CF | 380 | 55 | 14.5% | 3.1% | 0.44% | medium |
| 15 | Central Europe & CIS | SAT | 120 | 40 | 33.3% | 1.0% | 0.32% | low |
| 16 | Latin America | CF | 285 | 40 | 14.0% | 2.3% | 0.32% | medium |
| 17 | Canada | SAT | 175 | 37 | 21.1% | 1.4% | 0.30% | medium |
| 18 | Central Europe & CIS | CF | 110 | 28 | 25.5% | 0.9% | 0.23% | medium |
| 19 | Latin America | SAT | 136 | 23 | 16.9% | 1.1% | 0.19% | medium |
| 20 | Canada | FS | 196 | 22 | 11.2% | 1.6% | 0.18% | medium |
| 21 | Western Europe | FS | 53 | 8 | 15.1% | 0.4% | 0.06% | high |
| 22 | Latin America | FS | 33 | 6 | 18.2% | 0.3% | 0.05% | medium |
| 23 | Asia/Africa/Oceania/ME | FS | 55 | 4 | 7.3% | 0.4% | 0.03% | high |
| 24 | Central Europe & CIS | FS | 2 | 2 | 100.0% | 0.0% | 0.02% | medium |

**Concentration.** The four United States cells are **50.6% of the forecast total and 44.8% of all the
range width in the file** (840m of 1,875m). The bottom six cells together carry 55m — less than one
fifth of US PPA alone. If the team has time to challenge three cells, challenge the three US equipment
cells.

### The five that actually matter

**1. US PPA — 1,440, range 1,300–1,590 (low confidence).** *The entire variance in the roll-up.* The
desk's four methods span 1,283–1,610, ±11% on the largest ag line, and §4.2 shows the team's own filed
numbers imply a residual of 1,542 — above the central. Bear case: AEM 100+hp −15.5% YTD, 4WD −38.7% in
July, Deere still deliberately ceding 100+hp share to protect price, and Q3 is structurally the least-US
quarter for PPA (38.4% share LY). Bull case: Q3 FY2025 was the trough print at −40.7%, inventory is the
cleanest of the cycle (100+hp at 30% of trailing-12m retail vs 31% LY, combines 12% vs 17%), and the
Waterloo H2 North American skew is real. **But management pointed that skew at Q4**, not Q3 — "a much
heavier fourth quarter… production rates significantly higher." That is the pivot: a Q3-weighted
Waterloo build prints near 1,600, a Q4-weighted one near 1,350. *Skew of risk: to the upside.*

**2. US CF — 2,050, range 1,900–2,180 (medium).** Largest cell in the matrix (16.6% of total) and the
comp inflects violently: US CF went −14.2% in Q3 FY2025 to +29.5% in Q4 FY2025. The +21.5% call requires
the restock and share tailwinds to still be running against a US construction market that is genuinely
contracting — **total US construction spending −3.2% YoY, private non-residential −2.1%** — with only
public (+1.7%), highway (+2.9%) and data centres (+46%) growing. Three independent methods converged on
2,062–2,074, which is reassuring, but they are all *Deere-internal* methods (seasonality,
share-of-global, H1-to-H2); none of them can see the end market. A print below +12% says the restock is
already finished and carries straight into a weak Q4. *Skew: to the downside.*

**3. US SAT — 1,700, range 1,600–1,790 (medium).** Third-largest cell. The headline +10.6% understates
the difficulty: Q3 FY2025 SAT was only −15.7% (an easy-ish comp by FY2025 standards) and global SAT rose
*sequentially* Q2→Q3 in FY2025 (ratio 1.014), so management's guided "step down in Q3 and another step
down in Q4" is itself a YoY headwind. The FY guide of ~+15% implies H2 decelerating to +11.5% from H1's
+19%. Supported by turf recovery, strong dairy/livestock margins and clean post-underproduction
inventory — but if turf fades with weak single-family housing, +10.6% is optimistic. *Skew: to the
downside.*

**4. Latin America PPA — 820, range 760–900 (medium).** Hardest comparative in the entire matrix
(Q3 FY2025 was itself +25.4% YoY). Three specific, dateable negatives run through the whole window
(Horizontina −30% output, deliberate combine underproduction, 4-week-late safrinha) against a +10% FX
tailwind. The desk's own risk flag is the right one: a hard reading of "underproduce retail demand, most
notably in combines" implies a *sequential decline* from Q2's 828, not the flat sequential assumed, and
the only thing arguing against that is management's characterisation of the order book — not a
disclosed number. The desk could not source Brazilian retail units for the window at all. *Skew: to the
downside.*

**5. Western Europe SAT — 810, range 765–860 (medium).** The largest cell in Europe and the only
geography where SAT exceeds PPA. The risk here is genuinely under-priced by the market: **EU standard
milk price was EUR 38.20/100kg in June 2026, ~21% below June 2025, with SMP −46% YoY at 23 July.** Deere
has cited robust dairy margins as the support for European SAT on *every call since Q3 FY2025* and said
in February 2026 that milk declines would have no near-term material impact. That judgement is now being
tested, on top of the FX tailwind vanishing and a base that itself grew 39.7%. *Skew: to the downside.*

### Also worth a look, for a different reason

**Canada PPA (340, 27.9% relative width)** and **Canada CF (200, 35% relative width)** are the two
loosest cells in the file in proportional terms, from a low-confidence desk that explicitly flagged
Canada as under-observed in official statistics for July. Together they are only 4.4% of the total, but
§4.1 says Canada PPA should be challenged *upward* and §4.3 says Canada CF is the desk's most
contrarian call. A combined +75m from those two is plausible and would push the total to ~12,440.

**Canada's rescale instruction.** The Canada desk asked that its cells be rescaled on implied shares
(PPA 8.3%, SAT 5.1%, CF 5.6%, FS 14.0%) rather than dollars if the aggregator's global figures differ
from its assumed globals — which they do. Applying that: PPA 329, SAT 172, CF 202, FS 197, region 901
instead of 911. **Total effect on the grand total: −10m (12,363 → 12,353).** Below the rounding
resolution of the disclosure itself. Noted, not applied, so the matrix stays exactly equal to what the
desks filed.

---

## 6. Standing caveats inherited from all six desks

- **No FY2026 Q3 actuals exist.** All six desks searched the corpus and the web and found none.
- **Basis.** ASC 606 revenue-recognition footnote throughout, not 8-K segment net sales. Conversions in
  §2c/§2d are explicit.
- **Q4 rows in every historical year are DERIVED** as (fiscal-year total − nine months). Deere never
  publishes a standalone Q4 geographic matrix. All desks flagged these `source_type=filing_derived` and
  report that they cross-foot to the published FY totals.
- **FY2019 is on the pre-reorganisation three-segment basis** (Ag & Turf / C&F / FS). Only FY2020 was
  restated to four segments. Quarterly FY2019 PPA/SAT splits do not exist and are **blank, not zero**,
  in every desk CSV. No desk fabricated them.
- **Sample sizes are small** — roughly 24–26 usable four-segment quarters, n=5 for every Q2→Q3 seasonal
  ratio in this document. **Five of six desks deliberately reported no correlation coefficients**, on
  the grounds that at n≈24 against strongly trending macro series almost any correlation would be
  spurious. That was the right call and I have not manufactured any here. The one desk that did report
  correlations (Canada, lag-2 crop prices, r=+0.68 to +0.79, n=22) flagged them as suggestive of a lag
  structure rather than estimable, did not use them to size its forecast, and separately flagged its own
  USD/CAD correlation of −0.29 as having the wrong sign and being almost certainly spurious.
- **`INDEX.md` mislabels** `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` as
  "Q3 2026". It is Q2 FY2026 Q&A. All six desks caught this independently and treated it correctly.
- **Known data gaps, left blank rather than estimated:** AEM June 2026 standalone report (US desk,
  fetch failed); Brazilian tractor/combine retail units for May–July (LatAm desk, ANFAVEA HTTP 406);
  country-level H1 2026 registrations for Germany/France/Italy/Spain (WE desk); Southeast Asia and
  Africa entirely (AAOME desk); StatCan data past 2026 Q1 / June / May depending on series (Canada
  desk). July 2026 is close to unobserved in official statistics for Canada.
- **The 20 August call carries more risk in the guidance commentary than in the Q3 number.** Four desks
  said this independently: FY2027 early-order programme results (US), a European Q4 production trim
  validating CEMA (WE), Asia guidance cut on the monsoon (AAOME), and Canada/softwood tariff commentary
  (Canada).
