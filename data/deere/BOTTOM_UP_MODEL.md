# Deere & Company (NYSE: DE) — Bottom-Up Geographic Model, FY2026 Q3

**Model date: 16 August 2026. Deere reports Q3 FY2026 at 09:00 US Central on Thursday 20 August 2026.**

**There are no Q3 FY2026 actuals in existence.** The offline corpus is frozen at 2026-08-14 and its
last reported quarter is Q2 FY2026 (three months ended 2026-05-03). Every Q3 FY2026 figure in this
document is a forecast. The `INDEX.md` row labelled `2026-05-21 | Call Transcript | Q3 2026` is
mislabelled — it is the Q2 FY2026 call and was treated as such throughout.

Runnable model: `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/bottom_up_model.py`
(stdlib only; reads `de_geo_segment_matrix.csv` and `de_predictability.csv`; prints every table below).

---

## 0. The answer

| Target | Low | **Central** | High | YoY (central) |
|---|---:|---:|---:|---:|
| **1. Worldwide net sales and revenues** (USDm) | 11,786 | **12,437** | 13,088 | **+3.5%** (Q3 FY2025: 12,018) |
| **2. Diluted EPS, GAAP** (USD) | 3.66 | **4.63** | 5.70 | **−2.6%** (Q3 FY2025: $4.75) |
| **3. PPA operating profit** (USDm) | 357 | **459** | 573 | **−20.8%** (Q3 FY2025: 580) |

Supporting lines (central): PPA net sales 3,893 (−8.9%) · SAT 3,334 (+10.2%) · CF 3,560 (+16.4%) ·
FS revenues 1,413 (−0.4%) · PPA operating margin 11.8% · net income $1,251m · diluted shares 270.4m.

Low/high are **~80% bounds** (z = 1.28), not extremes. There is roughly a one-in-five chance the print
falls outside them, and a one-in-ten chance on either side.

The three numbers come from **one connected model**: the same 24 cells produce the revenue line; the
PPA block of those cells, bridged off "Other revenues," produces the PPA operating-profit denominator;
and all four segment operating profits plus reconciling items and tax produce the EPS. Change one cell
and all three move.

---

## 1. Data foundation and validation

The model is anchored on Deere's ASC 606 revenue-recognition footnote matrix (six primary geographic
markets × four segments). Before use, every quarter FY2020 Q1 – FY2026 Q2 was re-validated from the
CSV: each geography row must sum to Deere's stated row total **and** each segment column to its stated
column total. **Zero failures.** Cumulative H1/9M/FY columns were filtered out before any quarterly
series was built.

Two anchors verified externally:

- Q3 FY2025 grid total = **12,018**, exactly the income-statement "Total net sales and revenues."
- Q2 FY2026 grid reproduces the supplied ground truth cell for cell.

### The Q3 FY2025 base (rev-rec, USDm) — the comparator for every cell

| | PPA | SAT | CF | FS | Total |
|---|---:|---:|---:|---:|---:|
| United States | 1,684 | 1,537 | 1,687 | 1,100 | 6,008 |
| Canada | 335 | 148 | 222 | 190 | 895 |
| Western Europe | 677 | 757 | 550 | 45 | 2,029 |
| Central Europe and CIS | 301 | 130 | 103 | 2 | 536 |
| Latin America | 1,055 | 124 | 252 | 28 | 1,459 |
| Asia, Africa, Oceania, ME | 332 | 393 | 313 | 53 | 1,091 |
| **Total** | **4,384** | **3,089** | **3,127** | **1,418** | **12,018** |

---

## 2. Cell-level forecast — 24 segment × geography cells

Basis = rev-rec, USDm. Q1/Q2 columns are actual YoY growth for context.

| Seg | Geography | Q3 FY25 | Q1 FY26 | Q2 FY26 | Low | **Central** | High | **YoY** |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| PPA | US | 1,684 | −21.2% | −19.9% | 1,347 | **1,480** | 1,633 | **−12.1%** |
| PPA | Canada | 335 | +12.4% | −25.8% | 302 | **340** | 375 | **+1.5%** |
| PPA | W. Europe | 677 | +67.5% | +6.9% | 596 | **650** | 704 | **−4.0%** |
| PPA | C. Eur + CIS | 301 | +156.7% | +24.3% | 241 | **285** | 331 | **−5.3%** |
| PPA | Latin America | 1,055 | −4.3% | −16.8% | 791 | **890** | 1,002 | **−15.6%** |
| PPA | AAO-ME | 332 | +58.5% | +5.4% | 315 | **355** | 392 | **+6.9%** |
| **PPA** | **Total** | **4,384** | +3.0% | −13.5% | 3,681 | **4,001** | 4,320 | **−8.7%** |
| SAT | US | 1,537 | +16.5% | +12.7% | 1,614 | **1,740** | 1,844 | **+13.2%** |
| SAT | Canada | 148 | +27.8% | +22.2% | 155 | **178** | 197 | **+20.3%** |
| SAT | W. Europe | 757 | +38.1% | +24.0% | 734 | **800** | 863 | **+5.7%** |
| SAT | C. Eur + CIS | 130 | +53.8% | +22.2% | 98 | **115** | 136 | **−11.5%** |
| SAT | Latin America | 124 | +18.8% | +10.3% | 124 | **138** | 151 | **+11.3%** |
| SAT | AAO-ME | 393 | +22.1% | +15.8% | 393 | **425** | 456 | **+8.1%** |
| **SAT** | **Total** | **3,089** | +23.1% | +16.3% | 3,190 | **3,396** | 3,602 | **+9.9%** |
| CF | US | 1,687 | +41.7% | +34.9% | 1,889 | **2,080** | 2,244 | **+23.3%** |
| CF | Canada | 222 | +34.7% | −15.9% | 182 | **210** | 240 | **−5.4%** |
| CF | W. Europe | 550 | +23.8% | +22.3% | 534 | **585** | 632 | **+6.4%** |
| CF | C. Eur + CIS | 103 | +7.0% | +20.7% | 98 | **113** | 129 | **+9.7%** |
| CF | Latin America | 252 | +12.7% | +27.3% | 260 | **290** | 320 | **+15.1%** |
| CF | AAO-ME | 313 | +28.6% | +33.2% | 319 | **350** | 382 | **+11.8%** |
| **CF** | **Total** | **3,127** | +32.8% | +28.2% | 3,364 | **3,628** | 3,893 | **+16.0%** |
| FS | US | 1,100 | −3.1% | −3.4% | 1,034 | **1,075** | 1,111 | **−2.3%** |
| FS | Canada | 190 | +2.1% | +10.5% | 184 | **198** | 211 | **+4.2%** |
| FS | W. Europe | 45 | +25.6% | +18.2% | 47 | **53** | 58 | **+17.8%** |
| FS | C. Eur + CIS | 2 | −50.0% | −33.3% | 1 | **2** | 3 | **0.0%** |
| FS | Latin America | 28 | −66.7% | −22.0% | 22 | **30** | 36 | **+7.1%** |
| FS | AAO-ME | 53 | −1.8% | +1.9% | 50 | **55** | 60 | **+3.8%** |
| **FS** | **Total** | **1,418** | −5.9% | −1.4% | 1,356 | **1,413** | 1,469 | **−0.4%** |

### Rationales

**PPA / United States, −12.1%.** Base 1,684 is the **cycle-trough cell** (−40.7% YoY in Q3 FY2025), the
easiest comp in the grid. Running YoY is −21.2% (Q1) / −19.9% (Q2); the base effect alone buys ~8pp.
AEM July 2026 retail is still contracting with no inflection (total tractors −10.9%; 4WD −38.7%;
100+hp −15.5% YTD; combines −10.2% YTD) and industry large ag is guided down 15–20%. Held **below** a
normal seasonal read because management flagged an abnormal shipment skew: *"more Waterloo large
tractor shipments shipping to North America in the back half than the front half of the year. That's
abnormal for us"* and *"order books are well into the fourth quarter."* Implied Q3/Q2 ratio 0.736 — in
line with FY2024's 0.732 and above FY2025's 0.670, but well short of a mid-cycle 0.85–0.90.

**PPA / Canada, +1.5%.** Base 335 also depressed (−31.5%). Q1 +12.4%, Q2 −25.8% — the two average
−12%, and the cell is chronically lumpy (Q3/Q2 has run 0.51–1.46). Same large-ag industry guide as the
US, same trough comp. USD/CAD −1.6% YoY is a small translation headwind.

**PPA / Western Europe, −4.0%.** Base 677 is a hard comp (+29.7%). Q1 +67.5%, Q2 +6.9% — decelerating
fast. The decisive point is FX: **EUR/USD averaged 1.15324 over Deere's Q3 window vs 1.14882 a year
earlier = +0.38%, against +8.40% in Q2.** The Q2 growth rate is mostly translation and must not be
rolled forward; this is a base effect invisible in spot rates. Europe ag industry flat to +5%; 2026
European production "largely aligned with retail demand."

**PPA / Central Europe and CIS, −5.3%.** Smallest PPA cell, most erratic (post-Russia-exit structural
break). Base 301 was +49.8%. Q1 +156.7%, Q2 +24.3% off tiny FY2025 bases. Momentum faded hard against
the toughest of the four European comps; widest proportional band in the grid.

**PPA / Latin America, −15.6%.** Base 1,055 is the hardest comp in PPA (+25.4%), and LatAm is 24.1% of
Q3 PPA versus 18.0% in Q2 — the seasonal mix amplifies it. Trend is negative (Q1 −4.3%, Q2 −16.8%),
South America industry is guided down ~15%, and management said *"in Brazil we expect to underproduce
retail demand, most notably in combines."* Drivers pull the other way: record 180.6Mt CONAB soy,
BRL +10.0% YoY (the single largest FX contributor to PPA at +1.74pp on its own), Plano Safra costing
rate cut 14.0%→12.5% in July, and the one correlation that survives Bonferroni (LatAm revenue on corn
price lagged one quarter, r = +0.87). **Drivers and the last two actuals disagree.** I weight the
actuals and the explicit underproduction statement more heavily, and let FX and crop economics stop
the decline short of Q2's rate.

**PPA / Asia, Africa, Oceania, ME, +6.9%.** Q1 +58.5%, Q2 +5.4% on an ordinary base. India tractor
registrations +28.1% but INR −10.3% eats most of it in translation; Asia ag industry flat. The ABARES
−21% Australian winter crop is a 2026/27 harvest event and hits FY2027, not this quarter. Q3/Q2 > 1.0
in four of five years (mean 1.11).

**SAT / United States, +13.2%.** The cleanest cell in the model. Q1 +16.5%, Q2 +12.7%; segment guided
up ~15%; US/Canada small ag and turf industry flat to +5% with Deere restocking after last year's
underproduction. Management: SAT is *"pretty normal seasonality… a little bit of a step down in Q3 and
another step down in Q4."* Q3/Q2 applied 0.949, against a five-year mean of 0.972.

**SAT / Canada, +20.3%.** Q1 +27.8%, Q2 +22.2% off a small base. No usable Canada driver exists (the
best correlate across all drivers and lags is USD/CAD at r = −0.44, one test among many at the
significance boundary), so this is momentum plus seasonality with a deliberately wide band.

**SAT / Western Europe, +5.7%.** Largest non-US SAT cell and the hardest comp (+39.7%). SAT is 24.5%
Western Europe by revenue — the most euro-levered segment — and the euro tailwind goes from +8.4% to
+0.4%. Strip ~8pp of translation out of Q2's +24.0% and the underlying is mid-teens; the comp takes
the reported rate to mid single digits.

**SAT / Central Europe and CIS, −11.5%.** Base 130 was +85.7% — the single hardest comp in the grid.
Q1 +53.8%, Q2 +22.2%. Q3/Q2 has run 0.40–1.31. A decline against that base is the central case; the
band is nearly ±20pp because the cell is ~1% of revenue and noise-dominated.

**SAT / Latin America, +11.3%.** Small and consistently positive (Q1 +18.8%, Q2 +10.3%; Q3/Q2 > 1.05 in
all five years). BRL helps translation. Brazilian underproduction is a combine and large-tractor
story, i.e. PPA, not SAT.

**SAT / Asia, Africa, Oceania, ME, +8.1%.** Q1 +22.1%, Q2 +15.8%. India tractor volumes are the driver
and this is where they land, but INR −10.3% roughly halves the reported rate.

**CF / United States, +23.3%.** The strongest cell in the model. Q1 +41.7%, Q2 +34.9%; segment guided
up ~20% (raised at Q2). Management: US/Canada order book *"up more than 60% since November, now at its
highest level since April of 2024, with over 80% of production slots filled for the year"*, demand
*"supported by infrastructure spending, rental activity, and accelerating data center investments"*,
plus share gains and the roll-off of last year's earthmoving underproduction. Decelerating from Q2
because the comp hardens (Q3 FY2025 US CF −14.2%) and management called H2 "fairly balanced" Q3 vs Q4.

**CF / Canada, −5.4%.** The one CF cell going backwards: Q1 +34.7% then Q2 −15.9%. H1 in total is
+0.6%, so the swing looks like shipment timing rather than demand. Base 222 was +21.3% — the hardest CF
comp.

**CF / Western Europe, +6.4%.** Roadbuilding (Wirtgen) sits here; global roadbuilding guided up ~10%.
Q1 +23.8%, Q2 +22.3% — but again roughly 8pp of Q2 was euro translation that does not repeat, and the
base was +27.3%.

**CF / Central Europe and CIS, +9.7%.** Tiny, and the only C. Eur + CIS cell with a soft comp (−2.8%).
Q1 +7.0%, Q2 +20.7%; Q3/Q2 > 1.08 in four of five years.

**CF / Latin America, +15.1%.** Q1 +12.7%, Q2 +27.3% against a base that was −17.4%, so the comp is
easy. BRL +10% translation tailwind. Brazilian underproduction is an ag decision and does not bind
construction.

**CF / Asia, Africa, Oceania, ME, +11.8%.** Q1 +28.6%, Q2 +33.2% on a base that was +4.3%. Global
forestry guided down ~5% is the offset and lands disproportionately here and in Nordic Western Europe;
INR −10.3% is a translation drag.

**FS (all six cells).** FS revenue tracks average portfolio × yield, not equipment shipments. US −2.3%
(Q1 −3.1%, Q2 −3.4%; portfolio shrinking after two years of lower equipment sales, partly offset by
higher earning-asset yields). LatAm +7.1% only because Q3 laps a −70.2% step down in the Brazilian
book — the sign flip is mechanical, not a recovery. C. Eur + CIS is a 2 USDm cell carried at base so
the grid stays complete; it is never treated as signal.

### FX summary for the quarter (the most under-appreciated input)

The FX tailwind collapses in Q3. Deere reported +4/+2/+4pp (PPA/SAT/CF) in Q1 FY2026 and +3/+2/+3pp in
Q2; the estimate for Q3 is **+1.78 / +0.21 / +0.50pp, worldwide +0.83pp (~+$99m)**, versus **+$305m in
Q2**. Roughly **$210m of revenue** would be wrongly assumed by rolling Q2's currency run-rate forward.
The euro is the entire cause (base effect, not a spot move). Brazil is what keeps PPA positive
(BRL +10.0%, LatAm 24.1% of Q3 PPA). This is why PPA and SAT diverge on FX: **PPA is a Brazil story,
SAT is a Europe story.**

---

## 3. Aggregation and basis reconciliation

### 3.1 Correlation-aware aggregation

Summing the 24 cell extremes gives 11,331–13,512, which assumes every region misses in the same
direction at once. That is not what the history shows: in Q2 FY2026, PPA was −13.5% while CF was
+28.2%. The band is therefore aggregated with an explicit correlation structure — ρ = 0.45 between
cells of the same segment (shared production plan and order book), ρ = 0.25 across segments (shared FX
and macro, shared Deere-wide execution). Aggregate 1σ = **$508m**.

**Worldwide net sales and revenues: low 11,786 | central 12,437 | high 13,088.**

### 3.2 The rev-rec → reporting-basis bridge, resolved exactly

**At company level there is no gap.** The rev-rec grid total *is* the income-statement "Total net sales
and revenues" (Q3 FY2025 both 12,018; Q2 FY2026 both 13,369). So the geographic build gives the
revenue target directly, with no adjustment.

**At segment level the ~104m PPA gap is not a residual and not rounding — it is the segment's share of
the 8-K line "Other revenues."** This closes to the dollar on every quarter tested:

| Quarter | PPA gap | SAT gap | CF gap | Sum | 8-K "Other revenues" | Residual |
|---|---:|---:|---:|---:|---:|---:|
| Q3 FY2025 | 111 | 64 | 68 | 243 | 243 | **0** |
| Q1 FY2026 | 106 | 56 | 64 | 226 | 226 | **0** |
| Q2 FY2026 | 104 | 57 | 64 | 225 | 225 | **0** |

Financial Services is identical on both bases. Economically, "Other revenues" is close to the
*over-time* revenue-recognition bucket (precision-guidance, telematics and information-enabled
subscriptions), which lands in Other income rather than Net sales.

Q3 FY2026 assumption: **Other revenues 238** (Q3'25 243, Q4'25 267, Q1'26 226, Q2'26 225 — flat to
slightly down), split PPA 108 / SAT 62 / CF 68 on the five-quarter average shares.

| Segment net sales, 8-K basis | Q3 FY25 | Low | **Central** | High | YoY |
|---|---:|---:|---:|---:|---:|
| PPA | 4,273 | 3,573 | **3,893** | 4,212 | **−8.9%** |
| SAT | 3,025 | 3,128 | **3,334** | 3,540 | **+10.2%** |
| CF | 3,059 | 3,296 | **3,560** | 3,825 | **+16.4%** |
| FS revenues | 1,418 | 1,356 | **1,413** | 1,469 | **−0.4%** |

No figure in this document mixes the two bases in one series.

---

## 4. PPA operating profit

Two independent methods, run side by side.

### (a) Operating-profit bridge from the year-earlier quarter

Sales change on the 8-K basis: 4,273 → 3,893, i.e. **−$381m**, decomposed as FX +$76m (+1.78pp),
price +$64m (+1.5%), volume/mix **−$521m**.

| Step | USDm | Basis |
|---|---:|---|
| Q3 FY2025 PPA operating profit | **580** | 8-K, margin 13.57% |
| Volume/mix | −167 | −$521m × 32% decremental (historical range 25–35%) |
| Price realisation | +64 | +1.5% on 4,273; H2 laps last year's incentives — *"price gets more favorable in the back half"* |
| Production cost incl. tariffs | −20 | PPA still carries ~$60m/qtr of the $1.2bn FY tariff run-rate (large ag = 20% of it); Q3 FY2025 had only its first weeks. H2 laps most but not all, and material/freight inflation re-accelerated Feb–May |
| Currency on operating profit | +15 | vs +$75m in Q2 FY2026; BRL-driven, and the Brazilian cost base offsets part of it |
| R&D / SA&G | −15 | R&D guided "up slightly"; no volume relief |
| **= Q3 FY2026 PPA operating profit** | **458** | **margin 11.75%** |

### (b) Guidance- and seasonality-anchored margin

Reference points: FY2026 guide **11–13%**; H1 FY2026 actual **11.02%**; Q3 FY2025 actual **13.57%**;
Q2 FY2026 **ex the one-off $272m IEEPA tariff refund** (20% of which went to large ag) **14.48%** vs
15.68% reported. **The refund does not repeat in Q3** — on its own that is −1.4pp for PPA, −2.4pp for
SAT and −3.6pp for CF versus the reported Q2 margins.

Q3 margins used: **low 10.0% | central 11.8% | high 13.6%.**

> Calibration note: Deere's Q2-vintage PPA margin guidance has landed **below** the guided range in
> both recent difficult years (FY2022 −7.3%, FY2025 −5.1% vs the midpoint; FY2025 guided 15.5–17%,
> actual 15.43%). That is why the central sits in the lower half of 11–13% rather than at the midpoint.

### Result

| PPA operating profit (USDm) | Low | **Central** | High |
|---|---:|---:|---:|
| | 357 | **459** | 573 |
| implied margin | 10.0% | **11.8%** | 13.6% |

The bridge (458) and the guidance-anchored margin (459) **agree to $2m** and are constructed
independently — one from a volume/price/cost walk, the other from the FY margin guide and the H1
actual. That agreement is the main reason to have some confidence in this line.

---

## 5. EPS build-up

Built through the 8-K segment identity, which holds to the dollar on every quarter tested:

> Net income attributable to Deere = Total segment operating profit + Reconciling items − Income taxes
>
> Q2 FY2026: 2,237 + 54 − 518 = **1,773** ✓  ·  Q3 FY2025: 1,568 + 60 − 339 = **1,289** ✓

| USDm unless stated | Low | **Central** | High |
|---|---:|---:|---:|
| PPA net sales (8-K) | 3,573 | **3,893** | 4,212 |
| SAT net sales (8-K) | 3,128 | **3,334** | 3,540 |
| CF net sales (8-K) | 3,296 | **3,560** | 3,825 |
| Financial Services revenues | 1,356 | **1,413** | 1,469 |
| Other revenues | 238 | **238** | 238 |
| **Total net sales and revenues** | **11,591** | **12,437** | **13,284** |
| | | | |
| PPA operating profit (10.0 / 11.8 / 13.6%) | 357 | **459** | 573 |
| SAT operating profit (12.2 / 14.1 / 16.0%) | 382 | **470** | 566 |
| CF operating profit (9.1 / 10.5 / 11.9%) | 300 | **374** | 455 |
| FS operating profit | 250 | **270** | 292 |
| **Total operating profit** | **1,289** | **1,573** | **1,886** |
| Reconciling items (added) | 40 | **62** | 84 |
| **Pre-tax income** | **1,329** | **1,635** | **1,970** |
| Income taxes (25.5 / 23.5 / 21.8%) | −339 | **−384** | −430 |
| **Net income attributable to Deere** | **990** | **1,251** | **1,541** |
| *memo: implied FS net income* | *198* | *213* | *231* |
| Diluted shares (m) | 270.6 | **270.4** | 270.2 |
| **DILUTED EPS, GAAP (USD)** | **3.66** | **4.63** | **5.70** |

Note the low-case total (11,591) sits below the correlation-aware revenue low (11,786) because the
P&L scenarios stack worst-case cells *and* worst-case margins *and* worst-case tax; the revenue
headline in §0 uses the correlation-aware band, which is the honest one for the revenue target alone.

### Line-by-line justification

**Segment margins.** SAT central 14.1%: FY guide 13.5–15% against an H1 actual of 16.2%, so the guide
demands a materially weaker H2; Q3 is seasonally the strong half of H2 (Q3 margins 19.6% / 16.3% /
16.0% in FY2023-25 versus Q4 at 14.4% / 10.2% / 1.0%), and Q3 loses the 30% share of the tariff refund
booked in Q2. CF central 10.5%: FY guide 10–12%, H1 actual 10.8%, Q2 ex-refund 11.2%, Q3 FY2025 7.75%
— volume leverage on +16% sales offset by losing the 50% share of the refund.

**Financial Services.** FS operating profit 270 central (Q3 FY2025: 266), implying FS net income ~213
at the historical 0.79 conversion (FY2025: 890 / 1,114). Combined with H1 actual 434 and a Q4 of ~209,
FY FS net income is **857** against the guided **~$860m** — the FS block is pinned to guidance.

**Reconciling items, +62.** Deere's residual (corporate expense, certain interest, FX, non-service
pension, NCI) has been **positive** for eight straight quarters: +62, +43, +103, +35, +60, +68, +79,
+54. Q3s specifically: +98 (FY23), +62 (FY24), +60 (FY25).

**Tax rate, 23.5%.** Deere's guided **24–26% is footnoted "*Equipment Operations"** — it is not the
consolidated rate. Realised **consolidated** effective rates: FY2023 22.1% (2,871/13,019), FY2024 22.7%
(2,094/9,206), FY2025 **20.1%** (1,259/6,257), H1 FY2026 **22.8%** (714/3,129). The central case sits
just above the H1 run-rate and below the guided floor; the low case uses 25.5% to respect the guide.

**Diluted shares, 270.4m.** Q3 FY2025 271.4 → Q4 271.0 → Q1 FY2026 271.1 → Q2 FY2026 270.8. Net
buyback is light (−1.0m YoY), roughly −0.2m/quarter.

---

## 6. Full-year consistency of the model

The Q3 forecast is only credible if the Q4 it implies is also credible. Rolling forward on Deere's
guided FY segment sales (PPA −7.5% midpoint, SAT +15%, CF +20%):

| Segment | FY guide mid | H1 actual | Q3 model | Q4 plug | FY margin | FY margin guide |
|---|---:|---:|---:|---:|---:|---:|
| PPA | 16,013 | 7,666 | 3,893 | 4,454 | **11.7%** | 11–13% ✓ |
| SAT | 11,758 | 5,653 | 3,334 | 2,771 | **13.9%** | 13.5–15% ✓ |
| CF | 13,658 | 6,460 | 3,560 | 3,638 | **10.8%** | 10–12% ✓ |

**Equipment net sales: Q3 10,787 vs Q4 10,863 — Q4 exceeds Q3 by $76m.** This satisfies management's
explicit constraint of 2026-05-21: *"we would expect slightly higher revenue in the back half, with
the fourth quarter being higher than the third quarter."* **This constraint is what caps the Q3 PPA
cell block.** A larger Q3 PPA — which a naive Q3/Q2 seasonal ratio would produce — would violate it,
because SAT steps down ~$560m from Q3 to Q4 and only PPA can offset that.

Implied Q4 FY2026 net income **1,176** → **FY2026 net income 4,856**, inside the guided
**$4.5–5.0bn** (+2.2% vs the midpoint). Implied FY FS net income 857 vs ~860 guided.

*(Note: Q4 FY2026 faces a 13-week quarter against FY2025 Q4's 14 weeks — FY2025 was a 53-week year with
the extra week in Q4. Q3 FY2026 vs Q3 FY2025 is 13 vs 13, so the Q3 forecast is unaffected; the Q4
plug is flattered on a like-for-like basis.)*

---

## 7. Top-down cross-check

FY2026 net income guidance less H1 actual (2,429), split into Q3/Q4 on the seasonal pattern.

Historical Q3 share of H2 GAAP EPS: FY2015 58.6% · FY2016 63.3% · FY2017 55.6% · FY2018 53.5% ·
FY2019 55.3% · FY2020 51.8% · FY2021 56.4% · FY2022 45.3% · FY2023 55.3% · FY2024 58.0% · FY2025 54.7%
— **mean 55.3%**. FY2026 uses **51%**, below the mean, because management flagged an abnormally
Q4-weighted large-tractor build and *"the most favorable cost comparisons in the fourth quarter."*

| FY NI guide | H2 implied | Q3 NI | **Q3 EPS** |
|---|---:|---:|---:|
| low 4,500 | 2,071 | 1,056 | **$3.91** |
| mid 4,750 | 2,321 | 1,184 | **$4.38** |
| high 5,000 | 2,571 | 1,311 | **$4.85** |

**Bottom-up central $4.63 vs top-down at guide midpoint $4.38 — a gap of $0.25 (+6%).** I do not
average them. Decomposition:

1. **The tax line, $0.09 (36% of the gap).** Rerun the bottom-up at the guided 25% rather than 23.5%
   and EPS falls to $4.54. The guided rate is an *equipment-operations* rate and has been above the
   realised consolidated rate every year since FY2023. The bottom-up is right on this line; the
   top-down inherits the conservative rate embedded in the NI range.
2. **The remaining $0.16 is inside the top-down's own seasonal-split uncertainty.** At the guidance
   midpoint alone, the Q3/Q4 split assumption spans:

   | Q3 share of H2 | 45% | 51% | 55% | 58% | 63% |
   |---|---:|---:|---:|---:|---:|
   | Q3 EPS | $3.86 | $4.38 | $4.72 | $4.98 | $5.41 |

   The observed historical range is 45.3%–63.3%, i.e. the top-down spans **$3.89–$5.43 before forming
   any view on the FY number at all** — roughly four times the gap being reconciled. At the historical
   mean split of 55.3% the top-down reads **$4.75**, *above* my central. **The two methods bracket each
   other; they are not in material conflict.**
3. **Guidance bias is not the explanation.** Q2-vintage FY NI guidance vs actual: FY18 +3.0%,
   FY19 −1.4%, FY20 +52.8% (COVID), FY21 +8.4%, FY22 −1.0%, FY23 +8.4%, FY24 +1.4%, FY25 −1.9%. In the
   two recent down-cycle years the guide was essentially unbiased, so the FY midpoint is a fair anchor.

**I take the bottom-up ($4.63) as the central case** because it is the only one of the two that is
tied cell-by-cell to disclosed geographic revenue, uses Deere's realised tax rate rather than a
different-basis guided one, and produces an FY net income (4,856) that sits inside the guided range
without anything having to be assumed away.

---

## 8. Weakest links

Ranked by contribution to forecast risk.

1. **PPA / United States (1,480 central, band 1,347–1,633).** The largest single swing factor in the
   whole model. It hinges entirely on *when* the Waterloo large-tractor build lands — management said
   the back half is abnormally Q4-weighted, but "back half" is not a quarter. A one-month shift in that
   schedule is worth ±$150–200m of revenue and, at a ~32% decremental, ±$50–65m of PPA operating
   profit and ~±$0.15 of EPS. The historical Q3/Q2 ratio for this cell alone spans 0.670–1.193.
2. **PPA / Latin America (890 central, band 791–1,002).** The one cell where the driver evidence and
   the reported actuals point in opposite directions. Record 180.6Mt CONAB soy, BRL +10%, cheaper
   Plano Safra credit and the only Bonferroni-surviving correlation (corn lag-1, r = +0.87) all say
   up; Q1 −4.3%, Q2 −16.8%, a −15% industry guide and an explicit statement that Deere will
   underproduce Brazilian retail all say down. I chose the actuals. If the drivers are right the cell
   is 150m light. Note also that the best-fitting LatAm regression has a residual SD of **±19.9pp** —
   it is directional context, not a forecasting engine.
3. **PPA operating margin (11.8% central).** The FY guide spans 11–13% on ~16.0bn of sales, so the
   guidance alone leaves ±$320m of FY operating profit undetermined. The naive one-quarter-ahead
   benchmark MAE for Q3 PPA margin is **257bp** — my ±180bp band at 80% is tighter than that and is
   only justified by having the FY guide and the H1 actual. The tariff line inside it is the softest
   assumption in the model: the $1.2bn FY run-rate is management's own number, but the *timing* of the
   lap and the offsetting material inflation are estimates, and Q2 already showed a $272m one-off
   moving 2.5 points of enterprise margin in a single quarter.
4. **The effective tax rate.** A 23.5% vs 26% assumption is worth **$0.15/share**. It is also the
   largest identified component of the bottom-up/top-down gap. Deere's guided rate is on a different
   basis (equipment operations) and has been wrong in the same direction three years running, but
   nothing guarantees a fourth.
5. **Assuming the Q2 currency run-rate does not repeat.** If I am wrong about the euro base effect —
   for example if the region-to-currency baskets (my assumption, not a Deere disclosure) are
   mis-specified — worldwide revenue moves ±$77m at 1σ. The Latin America basket is the weakest part:
   assumed BRL 72% / MXN 13% / USD 15%; at BRL 60% the PPA effect falls ~0.27pp, at 85% it rises about
   the same.
6. **Reconciling items (+62).** An unmodelled residual line with no forecastable driver. It moves EPS
   ~$0.12 across the +40 to +84 range used here, but it has swung from −111 to +103 within the sample
   — a $0.60 spread — and I am leaning on eight consecutive positive quarters to narrow it.
7. **Central Europe/CIS and Canada cells.** Individually small (each ~1–4% of revenue) but jointly
   ~$800m and essentially unforecastable: Canada has no usable driver at all (best result across every
   driver and lag is r = −0.44 at p = 0.050), and C. Eur/CIS carries a structural break from Deere's
   Russian exit. Bands of ±15–25% on these cells are not conservatism; they are the honest width.
8. **Only six usable Q3 year-over-year observations exist per region** on the current segment scheme,
   across a window containing a pandemic, a grain-price spike, a Russian market exit and a historic ag
   downcycle. No seasonal or elasticity parameter estimated here should be treated as stable. This is
   why the model leans on management's own forward statements and guidance arithmetic wherever they
   exist, and on cell history only where they do not.

---

## 9. Reproducibility

```
python3 /Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/bottom_up_model.py
```

Inputs: `data/deere/de_geo_segment_matrix.csv` (rev-rec matrix, revalidated at runtime — all quarters
FY2020 Q1–FY2026 Q2 reconcile both ways, zero failures) and `data/deere/de_predictability.csv` (GAAP
EPS history for the seasonal cross-check). Corroborating extracts read during construction but not
required at runtime: `de_currency_effect.csv`, `drv_regional.csv`, `de_product_lines.csv`,
`de_guidance_vs_actual.csv`, `de_segments_modern.csv`. Filings cited are in
`challenge/offline-data/deere/{filings,call-transcripts,slides}`, principally the 2026-05-21 Q2 FY2026
8-K and call, the 2026-05-28 Q2 FY2026 10-Q, the 2025-08-15 Q3 FY2025 8-K and the 2025-12-18 FY2025
10-K. Standard library only; no network access required.
