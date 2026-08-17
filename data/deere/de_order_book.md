# Deere order book, lead time and order visibility — evidence for the Q3 FY2026 forecast

**Companion to** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_order_book.csv` (135 rows)
**Scripts** (reproducible, stdlib only):
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/de_order_book_extract.py` — keyword scan over all 131 transcripts
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/de_seasonality_test.py` — 8-K parse + dispersion tests
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/de_order_book_build.py` — builds the CSV

**As of 16 August 2026, Deere has not reported FY2026 Q3.** Nothing in this file is a Q3 FY2026 actual. The
INDEX.md row labelled `2026-05-21 | Call Transcript | Q3 2026` is the Q2 FY2026 Q&A transcript, mislabelled;
it is used here as Q2 material only.

---

## 1. Verdict on the hypothesis

> "The order book for Q3 was already largely set at the time of the Q2 report, so Q3 REVENUE is
> substantially pre-determined. What suppliers and input costs move is PROFIT, not revenue."

**PARTIALLY SUPPORTED — and the part that is wrong matters.**

| Claim | Verdict | Evidence |
|---|---|---|
| Q3 demand is booked before the Q2 call | **Supported, strongly, for PPA** | 13/13 Q2 calls with an order-book statement (2013–2026) say coverage reaches *at minimum* through Q3. 9 quantified: 3.0–5.4 months forward, mean 4.6. ~90% of combine/planter/sprayer volume is locked by EOP, closed months before the Q2 call. |
| Therefore Q3 *revenue* is tight | **Only conditionally** | Realised PPA Q3/Q2 sales ratio has CV **16.0%** (n=5) — not tight at all on a naive basis. It is tight only once you use the production-cadence statements management makes *at the Q2 call*. |
| Profit is where the uncertainty lives | **Supported** | PPA H2 operating profit moved **1.6× to 10.7×** as much as PPA H2 sales, every year, n=4. Q3-minus-Q2 PPA margin has sd **3.08pp** on a −2.5pp mean (n=5), i.e. the sign of the surprise is unstable. |
| "Deere needs longer than a month to build a tractor" as the *mechanism* | **Wrong mechanism, right conclusion** | Manufacturing cycle time is not what fixes the quarter. What fixes it is the **commercial** lead time — EOPs that close 7–11 months before the use season and rolling order books that run 3–5 months out. Deere itself never cites build time as the constraint. |

**The precise correct statement is not "revenue is pre-determined" but "revenue is pre-disclosed."**
The order book fixes *demand*, not *shipment timing*. Deere reallocates shipments between Q3 and Q4 freely
and does so most years — but it **announces the reallocation at the Q2 call**. In every one of the four
years where the PPA Q3/Q2 ratio deviated materially from its mean, the deviation was flagged in the Q2 call
script:

| FY | PPA Q3/Q2 | Deviation pre-announced at the Q2 call? |
|---|---|---|
| 2021 | 0.938 | n/a (near mean) |
| 2022 | **1.191** | Yes — "shipments to be more back-half weighted than we've seen historically" |
| 2023 | 0.870 | Yes — "revenue to be down sequentially by a bit over 10% in the third quarter" |
| 2024 | **0.775** | Yes — "our decision to underproduce large tractor retail demand in North America in the back half" |
| 2025 | 0.817 | Yes — H2 guide framed as "the change in sales is relatively small year-over-year"; enterprise H2 came in **+0.5% YoY**, i.e. exactly right |

**Modelling consequence.** A tight revenue range is justified — but anchor it on the Q2-call cadence
language, not on historical seasonality. Anchoring on the naive Q3/Q2 ratio would have been off by
−22% (FY2024) and +27% (FY2022). Widen the range on margin: that is where the realised dispersion is,
and it is where the FY2025 Q2 call shows the sell side actually disagreeing with management.

---

## 2. How far ahead is Deere sold? Quantified, by segment

### 2a. PPA large ag — the long-lead business

Statements at each **Q2 call** about forward order coverage (`de_order_coverage_months`, `segment=PPA_large_ag_NA`):

| Q2 call | Coverage stated | Months forward | Covers all of Q3? |
|---|---|---|---|
| 2014-05-14 | "on 8Rs, our order availability is into October" | 5.0 | yes |
| 2018-05-18 | "our large tractor order book now extends into October" | 5.0 | yes |
| 2019-05-17 | "order books extending into the fourth quarter" | 3.0 | yes |
| 2020-05-21 | "large tractor order books extend into the fourth quarter, roughly 90% full" | 3.0 | yes |
| 2021-05-21 | "all of our Large Ag order banks are now complete through the end of the fiscal year" | 5.3 | yes |
| 2022-05-20 | "our order book extends through the duration of fiscal 2022 and even into early fiscal 2023" | 5.4 | yes |
| 2023-05-19 | "excellent visibility through the end of the year" | 5.4 | yes |
| 2025-05-15 | "availability for … North American-produced large tractors … is into October" | 5.0 | yes |
| **2026-05-21** | **"Waterloo large tractors, order books are well into the fourth quarter"** | **4.0** | **yes** |

n=9 quantified, range 3.0–5.4, mean 4.57 months. Three further Q2 calls (2013, 2015, 2017) make the same
statement qualitatively; 2024 states the H2 production plan directly instead. **In no Q2 call in the corpus
does PPA large-ag coverage fall short of the following Q3.**

Corroborating leading indicator: at the **Q1 FY2026** call (2026-02-19), six months before Q3-end, the NA
rolling book already reached past Q3 — *"our rolling order books now provide visibility into the fourth
quarter."*

### 2b. Early order programs — how far in advance large-ag orders are actually placed

EOP share of annual production for the seasonal lines: **~90%**, stated five separate times
(2015-05, 2017-02, 2017-05, 2023-05, 2024-02). E.g. *"Typically, we source about 90% of model year 2024
planters and sprayers through the early order program."*

Programme calendar (`de_eop_calendar_month`, most explicit statement 2025-08-15 and 2026-05-21):

| Line | Opens | Closes | Duration | Delivery / use season | **Order → use interval** |
|---|---|---|---|---|---|
| Sprayers | early–mid **May** | end **August** | ~4 mo | spring (Mar–May) of the *next* calendar year | **~8–11 months** |
| Planters | early **June** | end **September** | ~4 mo | spring (Apr–May) next year | **~7–10 months** |
| Combines | **August** | Nov / mid-Dec / Jan | ~4–6 mo | autumn harvest (Aug–Oct) *next* year | **~8–14 months** |

Normal EOP duration: *"we normally have the EOP open for five to six months"* (2022-11-23).
Order-to-**production-start** is shorter: MY2027 spring products opened EOP in early May 2026 and
*"will begin production in the last few months of the fiscal year"* — roughly **3 months**.

Large tractors (Waterloo) are **not** on an EOP; they run a *rolling* order book, which is why coverage is
3–5 months rather than 8–14.

### 2c. The segment gradient — the hypothesis does **not** apply uniformly

| Segment | Forward visibility | Source |
|---|---|---|
| PPA seasonal (combine/planter/sprayer) | 8–14 months at order; ~90% of the year locked before the year starts | EOP statements above |
| PPA large tractors (Waterloo, Mannheim) | 3–5.4 months at the Q2 call | table 2a |
| PPA Europe / South America | 2.5–4.5 months | 2026-02-19: Europe "4-5 months out", SA "full through our second quarter" |
| C&F earthmoving | **2–4 months** | 2024-05: "approximately four months into the fourth quarter"; 2024-08: "roughly two months of order visibility" |
| SAT turf & compact utility | **least of all — never quantified in 14 years of transcripts** | 2025-05: *"we have less order visibility in turf equipment and compact utility tractors"*; 2017-08: *"We don't tend to get that kind of visibility on small Ag"*; 2014-05: *"our order book would not be as far out … versus the large"* |

Deere states the principle itself (2020-05-21): *"certain products, like those subject to our early order
programs, operate on more of a sold-ahead basis, and we have higher visibility to demand in those areas.
Other products have lower levels of visibility as they do not operate off early order programs and tend to
be driven to a larger extent by general economic trends."*

**Implication for the three targets.** The "revenue is pre-determined" argument is strongest for PPA
(~35% of FY2026 equipment sales), weaker for C&F, and weakest for SAT. But note the arithmetic runs the
other way from intuition: SAT is the segment where management gave the *most* mechanical Q3 guidance this
quarter ("normal seasonality… a little bit of a step down in Q3"), because normal seasonality is exactly
what a retail-driven business follows.

---

## 3. Where the order book does **not** determine revenue (counter-evidence)

Four documented breaks (`de_orderbook_to_revenue_break_flag`):

1. **Orders are cancellable.** 2012-08-15: *"Consequently, some machines will be shipped too late for
   harvest, we have allowed dealers to cancel orders."*
2. **Supply, not demand, set FY2022 revenue.** Order books were full all year, yet revenue timing was
   governed by parts: *"the biggest challenge … was the number of partially completed machines"* (2022-05),
   and C&F compact was guided *down* on *"supply challenges constraining shipments"* despite strong demand
   (2022-08). A full order book guarantees the sale, not the quarter it lands in.
3. **Deere cuts its own schedule mid-year.** FY2019 and FY2024 both saw H2 production cut below the order
   book to drain dealer inventory. Both were announced at the Q2 call — so they are forecastable, but only
   if you read the Q2 call rather than the order book.
4. **Underproduction is a live lever right now.** For FY2026, Brazil is explicitly on underproduction
   *"most notably in combines"* through Q3 (stated at both the Q1 and Q2 calls).

---

## 4. Realised dispersion: revenue vs profit (the quantitative test)

Parsed 27 8-K earnings releases. Segment tables begin FY2021 (new segment structure), so segment-level
samples are **n=4–5 — far too small for inference; treat as illustration, not estimation.**

| Statistic | n | Mean | sd | CV |
|---|---|---|---|---|
| Enterprise Q3/Q2 net sales & revenues | 6 | 0.948 | 0.058 | **6.2%** |
| PPA Q3/Q2 segment sales | 5 | 0.918 | 0.147 | **16.0%** |
| PPA Q3 margin − Q2 margin | 5 | −2.52pp | 3.08pp | — |

Naive "know Q2, predict Q3" model errors for PPA (n=5): sales MAPE **12.3%**, margin MAE **2.34pp**,
operating profit MAPE **24.7%**. Profit error is 2× the sales error, and the margin term is what does it.

**H2 amplification** (`de_ppa_h2_sales_yoy_pct` vs `de_ppa_h2_op_yoy_pct`, n=4):

| FY | PPA H2 sales YoY | PPA H2 op profit YoY | Amplification |
|---|---|---|---|
| 2022 | +51.8% | +80.2% | 1.5× |
| 2023 | +1.8% | +19.3% | **10.7×** |
| 2024 | −31.7% | −49.7% | 1.6× |
| 2025 | −4.2% | −34.9% | **8.3×** |

In the two years where H2 revenue barely moved, profit moved 19% and 35%. That is the hypothesis's core
claim, and the data does support it.

**The one auditable Q2-call Q3 revenue guide in 14 years:** FY2023, *"revenue to be down sequentially by a
bit over 10% in the third quarter"* / *"anywhere from 10%-15%"*. Actual: **−9.1%**, i.e. **+3.4pp** better
than the midpoint. One observation — an anecdote, not a distribution — but it is the right sign of
accuracy for a revenue call made 11 weeks before quarter-end.

---

## 5. What the Q2 FY2026 call (2026-05-21) said about Q3 FY2026 — in full

All quotes: `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` and
`…-call-qna__1042775.md`.

### Order book / production status
- **Waterloo large tractors:** *"order books are well into the fourth quarter as we look to close out our
  model year 2026 production."*
- **Seasonal PPA:** *"Model year 2026 production of seasonal products is largely set by our early order
  programs, which have been closed for several months now."* / *"Demand and that production plan for 2026
  is set at this point. Our EOPs for this year have closed, and we know where we're going to build in
  combines, sprayers, and planters."*
- **Europe & South America:** *"Order visibility in both regions now extends through the third quarter and
  into the fourth."*
- **C&F North America:** *"our order book continues to strengthen, up more than 60% since November, now at
  its highest level since April of 2024, with over 80% of production slots filled for the year."* Plus:
  *"nearly all of the production slots for the new John Deere excavator are spoken for."*
- **Production posture:** PPA NA and SAT NA both *"in line with retail demand"*; Europe *"largely aligned
  with retail"*; **Brazil underproducing, "most notably in combines."**
- **MY2027 EOPs (do not affect Q3 revenue):** sprayers opened early May, run to end-August; planters open
  early June to end-September. Production of MY2027 spring product begins *"in the last few months of the
  fiscal year"* — i.e. Q4 FY2026, not Q3.

### Explicit Q3-vs-Q4 cadence — the single most important passage
- Enterprise: *"we would expect slightly higher revenue in the back half, with **the fourth quarter being
  higher than the third quarter**. In addition, we would expect to see our **most favorable cost
  comparisons in the fourth quarter** as well."*
- PPA: *"**Q4 a bit stronger than Q3.** … We've got more Waterloo large tractor shipments shipping to North
  America in the back half than the front half of the year. **That's abnormal for us**, but reflected how
  the order book built for the course of the year."*
- SAT: *"pretty normal seasonality. You'll get a little bit of a **step down in Q3** and another step down
  in Q4."*
- C&F: *"fairly balanced between the two. Both top line and margin in the back half, maybe a little bit
  stronger in the fourth quarter than Q3, but overall pretty close."*
- PPA cost: *"a little bit **better absorption in the fourth quarter** as production rates are
  significantly higher"* — i.e. **Q3 FY2026 PPA carries the weaker absorption of the two H2 quarters.**
- Price/cost: *"Price cost will improve as we move through the balance of the fiscal year"*, with the
  favourable tariff and material comps landing hardest in Q4.

### Margin caution that belongs in the Q3 range, not the revenue range
Q2 FY2026 PPA operating profit of $706m **includes a one-time IEEPA tariff refund**. Management gave the
split: $272m total refund, *"the remaining 20% went to the large ag business"* ≈ **$54m to PPA**. Ex-refund
Q2 PPA margin was ≈ **14.5%**, not the reported 15.7%. The refund does not recur in Q3. Full-year direct
tariff expense is unchanged at ~$1.2bn gross / ~$900m net.

---

## 6. Arithmetic implications for Q3 FY2026 (derived, not a forecast)

Combining H1 FY2026 actuals with the FY2026 segment guidance reaffirmed on 2026-05-21 and the stated
Q3/Q4 cadence. These are the bounds management's own words imply; they are **not** my forecast and they
carry all the guidance-range width.

H1 FY2026 segment sales: PPA 7,666 / SAT 5,653 / CF 6,460 (= 19,779). H1 NSR 22,980.

| Segment | FY guide | H2 implied | Q3/Q4 split stated | **Q3 implied (USDm)** |
|---|---|---|---|---|
| PPA | −5% to −10% | 7,914 – 8,779 | Q4 a bit stronger (assume Q4/Q3 1.05–1.15) | **3,680 – 4,280** |
| SAT | ≈ +15% | 6,002 – 6,207 | step down Q3 then Q4 (Q4/Q3 0.88–0.95) | **3,080 – 3,300** |
| C&F | ≈ +20% | 7,085 – 7,312 | balanced, Q4 marginally higher (1.00–1.06) | **3,440 – 3,660** |
| Equipment ops | — | 21,001 – 22,299 | — | **10,200 – 11,240** |

Adding financial services + other revenue (Q2 FY2026: NSR 13,369 − equipment net sales 11,778 = 1,591) gives
an implied **Q3 FY2026 worldwide net sales and revenues of roughly 11.8 – 12.8 USDbn**.

Note a genuine tension to flag to the forecaster: *"slightly higher revenue in the back half"* reads as a
small H1→H2 step, but the segment guide midpoints imply H2 equipment sales **+7% to +12%** over H1. The
segment guide is the harder number; the "slightly" is loose language.

---

## 7. Caveats

- Segment-level financial series start FY2021 — n=4–5. Every dispersion statistic here is illustrative.
  No correlation coefficients are quoted because no pairing in this dataset reaches a sample size where
  one would be honest.
- Coverage-in-months values are **derived** from wording ("into October", "into the fourth quarter") plus
  the call date and Deere's fiscal calendar. Each derivation is written into the CSV `notes` so it can be
  disputed. Where wording was purely qualitative, no number was recorded.
- "Double digits" / "mid-single digits" in EOP results are coded as 12% / 5% nominal midpoints; the
  direction is reliable, the magnitude is not.
- EOP order→use-season intervals are derived from the programme calendar plus the known agronomic use
  season, not from a management statement of "lead time". Deere has never quantified lead time directly in
  this corpus.
- Transcripts are speaker-unattributed ("Unknown speaker") throughout, so quotes cannot be assigned to a
  named executive.
- Coverage: 131 transcripts scanned, 1,179 matching sentences across **59 distinct call dates**
  (2012-05-16 → 2026-05-21). 27 8-K earnings releases parsed.
