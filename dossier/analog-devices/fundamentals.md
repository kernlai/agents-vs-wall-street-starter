# Analog Devices (ADI) — FY2026 Q3 Fundamentals Dossier

**Prepared:** 2026-08-16 · **Corpus frozen:** 2026-08-14
**Target period:** Fiscal 2026 third quarter, the 13 weeks ending **Saturday 1 August 2026**
**Target metrics:** Revenue (USDm) · Adjusted diluted EPS (USD/share) · Adjusted gross margin (%)

> **NOT-YET-REPORTED WARNING.** ADI has **not** reported FY2026 Q3. The most recent reported
> period in the corpus and on SEC EDGAR is **FY2026 Q2, ended 2 May 2026** (filed 20 May 2026).
> SEC XBRL for CIK 0000006281 (`RevenueFromContractWithCustomerExcludingAssessedTax`) has **no**
> fact with `end` on/after 2026-05-03, confirming Q3 FY2026 is unreported. Any document that
> appears to contain Q3 FY2026 *actuals* is mislabelled or is prior-year material.
>
> **One corpus labelling defect found:** `filings/2026-05-20__adi-us-20260520-q2-10q__1040607.md`
> carries front-matter `period: "Q3 2026"` and the INDEX.md row lists it as "Q3 2026", but it is
> the **Q2 FY2026 10-Q** for the quarter ended 2 May 2026. Do not read it as Q3 data.

---

## 1. Report date — CONFIRMED

**Wednesday 19 August 2026**, results at 07:00 ET, conference call 10:00 ET.
- PR Newswire via Morningstar, published 2026-07-23: <https://www.morningstar.com/news/pr-newswire/20260723ne10537/analog-devices-to-report-third-quarter-fiscal-year-2026-financial-results-on-wednesday-august-19-2026>
- StockTitan: <https://www.stocktitan.net/news/ADI/analog-devices-to-report-third-quarter-fiscal-year-2026-financial-w62xxxgy6eag.html>

That is **3 days after today**. The quarter closed 1 August 2026; the books are effectively shut.

---

## 2. PRIOR-YEAR ACTUALS — the validation baseline (FY2025 Q3, 13 weeks ended 2 Aug 2025)

REPORTED FACT. Source: `filings/2025-08-20__adi-us-20250820-q3-8k__155976.md` (8-K/EX-99.1,
published 2025-08-20), Results Summary table.

| Metric | FY2025 Q3 actual |
|---|---|
| **Revenue** | **$2,880m** (exactly $2,880,348 thousand) |
| **Adjusted diluted EPS** | **$2.05** |
| **Adjusted gross margin** | **69.2%** (adjusted gross margin $1,995m) |

Cross-checks:
- Revenue independently confirmed at **$2,880,348,000** via SEC XBRL
  `https://data.sec.gov/api/xbrl/companyconcept/CIK0000006281/us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax.json`
  (start 2025-05-04, end 2025-08-02, frame CY2025Q2, form 10-Q).
- Revenue also appears as $2,880,348 in the TTM table of the Q2 FY2026 8-K
  (`filings/2026-05-20__adi-us-20260520-q2-8k__1040581.md`, three months ended Aug. 2, 2025).
- GAAP comparatives for the same quarter: gross margin 62.1%, operating margin 28.4%,
  GAAP diluted EPS $1.04, diluted shares 496.7m.

**Implied YoY growth at my forecast:** revenue +38.0%, adj EPS +66.8%, adj GM +350bps.

⚠️ **Basis discipline.** The GAAP-to-adjusted gap is very wide for ADI because Linear/Maxim
purchase-accounting amortisation is excluded. In FY2026 Q2 the gap was **5.7pp on gross margin**
(67.3% GAAP → 73.0% adjusted; $205m of acquisition-related expense in COGS) and **$0.69 on EPS**
($2.40 GAAP → $3.09 adjusted). All three target metrics here are the **adjusted/non-GAAP** basis,
except revenue which is identical on both bases.

---

## 3. THE GUIDANCE — verbatim, the single most important anchor

Issued with Q2 FY2026 results on **20 May 2026**.
Source: `filings/2026-05-20__adi-us-20260520-q2-8k__1040581.md`, "Outlook for the Third Quarter
of Fiscal Year 2026" (SEC URL:
`https://www.sec.gov/Archives/edgar/data/6281/000000628126000050/adi2q26exhibit991earnings.htm`):

> "For the third quarter of fiscal 2026, we are forecasting revenue of **$3.9 billion, +/- $100
> million**. At the midpoint of this revenue outlook, we expect reported operating margin of
> approximately **39.0%, +/-150 bps**, and adjusted operating margin of approximately **49.0%,
> +/-100 bps**. We are planning for reported EPS to be **$2.60, +/-$0.15**, and adjusted EPS to be
> **$3.30, +/-$0.15**."

Guidance reconciliation table (same file), "Three Months Ending August 1, 2026":
tax rate **12%–14%** (both bases); the adjusted line includes **$391 million** of acquisition-related
add-backs and **$51 million** of associated tax effects, i.e. **$0.70** of EPS.

**Gross margin is not formally guided, but management quantified it on the call.**
CFO Richard Puccio, Q2 FY2026 Q&A (`call-transcripts/2026-05-20__adi-us-20260520-call-qna__1041159.md`),
answering Josh on what is implied for fiscal Q3 gross margin:

> "…starting with the 73% gross margin, which was even a little higher than we expected based on
> some better mix and utilization… **For Q3, we are assuming about a 50 basis points decline in
> gross margin**, largely driven by the absence of that one-time benefit we got from repricing the
> channel during the prior quarter… From a mix perspective, we do expect it's likely to be a slight
> tailwind based on our outlook. While… **utilization is expected to be fairly neutral**… we don't
> see a ton of future upside on gross margin from utilization given where we're running the
> factories today."

⇒ **Implied Q3 FY2026 adjusted gross margin guidance ≈ 72.5%.**

Independently corroborated two weeks later. At the 2 June 2026 conference
(`call-transcripts/2026-06-02__adi-us-20260602-call-conf-qna__1135033.md`) the interviewer states
gross margin "held on to the **72.5%**, which is the best in the industry" and Puccio does not
dispute it; he adds that further accretion will come from **mix and revenue growth, not utilisation**.

Stacy Rasgon asked whether guided Q3 GM is a near-term ceiling because utilisations are maxed and
incremental revenue needs outsourcing. Puccio: *"Yeah, I actually think that's the right way to
think about it."* — a mild cap on gross-margin upside.

Segment guidance embedded in the $3.9bn midpoint (same Q&A, Puccio):
- **Industrial and Automotive: up mid-to-high single digits sequentially** ("above seasonal")
- **Communications: fastest grower, up low-to-mid teens sequentially**
- **Consumer: down single digits sequentially**
- **Channel inventory weeks assumed flat** in the guide
- Reminder that "the fourth quarter for us is usually up in the low single digits"

Adjusted opex implied by the guide: 72.5% GM − 49.0% adj op margin ⇒ **~23.5% of revenue ≈ $917m**
at the $3.9bn midpoint (vs $871.5m in Q2 FY2026, +5.2% q/q). Rich has repeatedly said FY2026 opex
growth will trail revenue growth "by roughly half."

---

## 4. Quarterly history of the three target metrics

REPORTED FACT throughout. Source for each row: the corresponding quarterly 8-K/EX-99.1 in
`offline-data/analog-devices/filings/` (Results Summary and GAAP→non-GAAP reconciliation tables).
Revenue in USDm; adj GM in %; adj EPS in USD.

| Fiscal qtr | Revenue | Adj GM % | Adj EPS |
|---|---|---|---|
| FY19 Q1 | 1,541 | 70.3 | 1.33 |
| FY19 Q2 | 1,527 | 70.6 | 1.36 |
| **FY19 Q3** | **1,480** | **70.4** | **1.26** |
| FY19 Q4 | 1,443 | 68.4 | 1.19 |
| FY20 Q1 | 1,304 | 68.5 | 1.03 |
| FY20 Q2 | 1,317 | 67.7 | 1.08 |
| **FY20 Q3** | **1,456** | **69.9** | **1.36** |
| FY20 Q4 | 1,526 | 70.0 | 1.44 |
| FY21 Q1 | 1,558 | 70.0 | 1.44 |
| FY21 Q2 | 1,661 | 70.9 | 1.54 |
| **FY21 Q3** | **1,759** | **71.6** | **1.72** |
| FY21 Q4 | 2,340 | 70.9 | 1.73 |
| FY22 Q1 | 2,684 | 71.9 | 1.94 |
| FY22 Q2 | 2,972 | 74.2 | 2.40 |
| **FY22 Q3** | **3,110** | **74.1** | **2.52** |
| FY22 Q4 | 3,248 | 74.0 | 2.73 |
| FY23 Q1 | 3,250 | 73.6 | 2.75 |
| FY23 Q2 | 3,263 | 73.7 | 2.83 |
| **FY23 Q3** | **3,076** | **72.2** | **2.49** |
| FY23 Q4 | 2,716 | 70.2 | 2.01 |
| FY24 Q1 (14 wks) | 2,513 | 69.0 | 1.73 |
| FY24 Q2 | 2,159 | 66.7 | 1.40 |
| **FY24 Q3** | **2,312** | **67.9** | **1.58** |
| FY24 Q4 | 2,443 | 67.9 | 1.67 |
| FY25 Q1 | 2,423 | 68.8 | 1.63 |
| FY25 Q2 | 2,640 | 69.4 | 1.85 |
| **FY25 Q3** | **2,880** | **69.2** | **2.05** |
| FY25 Q4 | 3,076 | 69.8 | 2.26 |
| FY26 Q1 | 3,160 | 71.2 | 2.46 |
| FY26 Q2 | **3,623** | **73.0** | **3.09** |
| **FY26 Q3** | *guide $3,900 ±100* | *guide ~72.5* | *guide $3.30 ±0.15* |

Full-year: FY22 $12,014m / 73.6% / $9.57 · FY23 $12,306m / 72.5% / $10.09 ·
FY24 $9,427m / 67.9% / $6.38 · FY25 $11,020m / 69.3% / $7.79.

**FY2026 Q3 is a clean 13-week quarter** (Q1 ended 31 Jan, Q2 2 May, Q3 1 Aug, Q4 31 Oct 2026 —
52-week year). No 14th-week distortion of the sort that inflated FY24 Q1.

---

## 5. Seasonality of the target period (Q2 → Q3 sequential)

| Year | Rev q/q | Adj GM q/q (bps) | Adj EPS q/q |
|---|---|---|---|
| FY2019 | −3.1% | −20 | −7.4% |
| FY2020 | +10.6% | +220 | +25.9% |
| FY2021 | +5.9% | +70 | +11.7% |
| FY2022 | +4.6% | −10 | +5.0% |
| FY2023 | −5.7% | −150 | −12.0% |
| FY2024 | +7.1% | +120 | +12.9% |
| FY2025 | +9.1% | −20 | +10.8% |
| **7-yr mean** | **+4.1%** | **+33** | **+6.7%** |
| **Up-cycle mean (FY20/21/24/25)** | **+8.2%** | **+98** | **+15.3%** |
| FY2026 **guide** | +7.6% | −50 | +6.8% |

Q3 is a *seasonally solid* quarter for ADI — it is Q4/Q1 that are the soft ones. The guide's
+7.6% sequential is below the up-cycle mean, and its −50bps gross-margin step is
entirely explained by a specific, disclosed one-off (Q2's channel-repricing benefit) rather
than by seasonality.

---

## 6. Guidance accuracy — ADI's track record (this is the edge)

Guidance midpoint vs. actual, from the 8-K of the guiding quarter vs. the 8-K of the reported
quarter. All REPORTED FACT.

| Guided quarter | Rev guide mid | Rev actual | Δ ($m) | Δ as × of ±band | EPS guide mid | EPS actual | Δ ($) |
|---|---|---|---|---|---|---|---|
| FY22 Q1 | 2,600 | 2,684 | **+84** | 0.84 | 1.78 | 1.94 | +0.16 |
| FY22 Q2 | 2,800 | 2,972 | **+172** | 1.72 | 2.07 | 2.40 | +0.33 |
| FY22 Q3 | 3,050 | 3,110 | **+60** | 0.60 | 2.42 | 2.52 | +0.10 |
| FY22 Q4 | 3,150 | 3,248 | **+98** | 0.98 | 2.57 | 2.73 | +0.16 |
| FY23 Q1 | 3,150 | 3,250 | **+100** | 1.00 | 2.60 | 2.75 | +0.15 |
| FY23 Q2 | 3,200 | 3,263 | **+63** | 0.63 | 2.75 | 2.83 | +0.08 |
| FY23 Q3 | 3,100 | 3,076 | **−24** | −0.24 | 2.52 | 2.49 | −0.03 |
| FY23 Q4 | 2,700 | 2,716 | **+16** | 0.16 | 2.00 | 2.01 | +0.01 |
| FY24 Q1 | 2,500 | 2,513 | **+13** | 0.13 | 1.70 | 1.73 | +0.03 |
| FY24 Q2 | 2,100 | 2,159 | **+59** | 0.59 | 1.26 | 1.40 | +0.14 |
| FY24 Q3 | 2,270 | 2,312 | **+42** | 0.42 | 1.50 | 1.58 | +0.08 |
| FY24 Q4 | 2,400 | 2,443 | **+43** | 0.43 | 1.63 | 1.67 | +0.04 |
| FY25 Q1 | 2,350 | 2,423 | **+73** | 0.73 | 1.53 | 1.63 | +0.10 |
| FY25 Q2 | 2,500 | 2,640 | **+140** | 1.40 | 1.68 | 1.85 | +0.17 |
| FY25 Q3 | 2,750 | 2,880 | **+130** | 1.30 | 1.92 | 2.05 | +0.13 |
| FY25 Q4 | 3,000 | 3,076 | **+76** | 0.76 | 2.22 | 2.26 | +0.04 |
| FY26 Q1 | 3,100 | 3,160 | **+60** | 0.60 | 2.29 | 2.46 | +0.17 |
| FY26 Q2 | 3,500 | 3,623 | **+123** | 1.23 | 2.88 | 3.09 | +0.21 |

- **17 of the last 18 quarters beat the revenue midpoint.** The single miss (FY23 Q3, −$24m) was
  the down-cycle inflection.
- Mean beat, all 18: **+$72m** (0.68× the band). Mean beat, **last 6 quarters: +$100m**
  (1.00× the band) — i.e. in the current up-cycle ADI lands, on average, **exactly at the high end**.
- Last 6 quarters: **3 of 6 finished at or above the stated high end** (FY25 Q2 $2,640 vs $2,600;
  FY25 Q3 $2,880 vs $2,850; FY26 Q2 $3,623 vs $3,600).
- Adjusted EPS beat the midpoint in 17 of 18. Mean beat last 6: **+$0.137**.

**Gross margin vs. its (verbal) guide** — a noisier record, worth respecting:
- FY25 Q3: guided "around 70%" (`call-transcripts/2025-05-22__adi-us-20250522-call-qna__40024.md`)
  → **actual 69.2%, a ~80bps MISS**, caused by an unplanned utilisation disruption at a European fab
  (`call-transcripts/2025-08-20__adi-us-20250820-call-qna__143762.md`).
- FY25 Q4: guided "get back to a 70% margin" → actual **69.8%**, ~20bps short.
- FY26 Q2: guided +100bps on Q1's 71.2%, i.e. ~72.2%
  (`call-transcripts/2026-02-18__adi-us-20260218-call-qna__602365.md`) → actual **73.0%, +80bps BEAT**
  on "better mix and utilization."

Net: revenue/EPS guidance is systematically conservative; gross-margin guidance is roughly
unbiased with ±80bps dispersion driven by fab utilisation events and mix.

---

## 7. Cycle, bookings, channel inventory, end markets

**Where we are in the analog cycle.** ADI is in the steep part of an up-cycle. Revenue has gone
$2,423 → $2,640 → $2,880 → $3,076 → $3,160 → $3,623m over six quarters (+50%). Q2 FY2026 was a
record on revenue, gross margin, operating margin and EPS. Vince Roche: *"we're currently seeing
record demand for our products and solutions."*

**Bookings / book-to-bill.** Puccio, Q2 FY2026 press release: *"We continued to see growing demand
in the second quarter with **record bookings across our B2B markets** of Industrial, Automotive, and
Communications."* On the auto question in the same Q&A: *"As we look out at Q3, we have **record
bookings, positive book-to-bill**, and so we do expect to see above-seasonal growth."* ADI does not
publish a numeric book-to-bill; "positive" (>1) is the disclosure.

**Backlog quality / double-ordering.** Puccio at the 2 June 2026 conference is unusually explicit:
lead times are *"pretty well in check… the vast majority of our product goes out inside normal
lead times"* with *"some minor stretch in the real high mover areas."* Because lead times are
normal, there is little incentive to place phantom orders. He says orders are now arriving *"a
quarter beyond where we would historically have had them as things appear to be getting tighter
broadly across Analog."* This is a genuine visibility improvement, not panic buying.

**Channel inventory — lean and disciplined.** Q2 FY2026: *"channel inventory weeks declined,
remaining within our six to seven-week range."* The Q3 guide *"baked into that outlook is also a
flat channel inventory weeks."* At the June conference: *"we're very lean in the channel. We're
running a leaner channel than we've run historically… and the channel is predominantly an
industrial business."* This removes the classic sell-in/sell-through risk that would normally cap
a Q3 beat.

**ADI's own inventory.** Q2 FY2026 balance-sheet inventories $1,848m (up $81m q/q, up from $1,656m
at FY25 year-end); days of inventory 168 (up from 159 at Q4 FY25). Deliberate: *"strategic die bank
and finished goods buffers to support growing demand."* Not a demand warning.

**End markets** (Q2 FY2026 actuals, FY2026 classification; source: Q2 FY2026 8-K end-market table):

| End market | Q2 FY26 rev | % of total | q/q | y/y | Guided Q3 q/q |
|---|---|---|---|---|---|
| Industrial | $1,799m | 50% | +20% | +56% | mid-to-high single digits |
| Automotive | $872m | 24% | +8% | +2% | mid-to-high single digits |
| Communications | $555m | 15% | +22% | +79% | low-to-mid teens |
| Consumer | $398m | 11% | flat | +23% | down single digits |

- **Industrial** is the profit engine (highest gross margin, 15–20 year product lives). Led by
  aerospace & defense (record), ATE, ETM and the broad market. Roche: the non-ATE/non-A&D
  industrial businesses *"have grown more than 40% in the first half of fiscal 2026"* and are
  *"still well below their prior cycle highs with lean channel inventories."* Puccio: ~40% of
  industrial is A&D + infrastructure; the other 60% is *"still approximately 20% below its prior
  peaks."* Mix target: peak margins occur at **53–54% industrial**; currently ~50%.
- **Communications / data center.** Data centre is now **>75% of communications** and grew **>90%
  y/y** in Q2 on optical and power. Wireless +35% y/y. Comms is described as an
  **above-corporate-average gross margin** business — so its outperformance is GM-accretive.
- **Automotive.** BMS for EVs returned to y/y growth for the first time in two years. ⚠️ **Read
  this carefully:** Puccio, 2 June 2026 — *"we saw an acceleration literally in the last month of
  the quarter in auto demand **that we were expecting to come in Q3**."* Some Q3 automotive revenue
  was pulled into Q2. He judges it real content demand, not a pre-buy, but it mechanically thins
  the Q3 automotive beat.
- **Consumer.** Guided down; memory shortages are the constraint — Roche: *"choke points in the
  semiconductor supply chain, memory being one of those. That's… having most effect on consumer
  customers who've got to make choices."*

**Pricing.** FY2026 price actions add *"a couple points to our growth rate in 2026"*; Q2's beat
above midpoint was *"due to volume, not incremental price."* The 50bps channel-repricing benefit
is a Q2-only item and is already removed from the Q3 bridge.

**Supply.** Internal capacity more than doubled vs. pre-COVID; capacity in place to support the
**$20bn 2030 vision**; *"we have not yet been unable to get the capacity we've needed"* externally.
But utilisation is at/near optimal, so incremental upside increasingly comes from **external
foundry**, which is gross-margin-dilutive at the margin.

**Empower Semiconductor** acquisition announced with Q2, pending regulatory approval. Puccio: if
it closes, *"there'll be some amount of revenue upon closing in the back half of our year. It will
certainly not be material."* Treat as ~$0 for Q3 revenue; any purchase-accounting amortisation is
excluded from the adjusted metrics anyway.

---

## 8. Consensus (ESTIMATE — third-party, dated)

| Metric | Consensus | Source |
|---|---|---|
| Revenue | **$3.92bn** (Zacks; +36.3% y/y) | Zacks via TradingView, "Should You Buy, Sell or Hold ADI Stock Before Q3 Earnings?" <https://www.tradingview.com/news/zacks:cd40d67ee094b:0-should-you-buy-sell-or-hold-adi-stock-before-q3-earnings/> (Aug 2026) |
| Revenue | **$3.93bn** (alt. compile) | Yahoo Finance / Insider Monkey compile, Aug 2026 |
| Adj. EPS | **$3.33** (Zacks; +62.4% y/y). "Most Accurate Estimate" **$3.41**, Earnings ESP +2.37% | same Zacks article |
| Adj. EPS | **$3.34** | TipRanks <https://www.tipranks.com/stocks/adi/earnings> |
| Adj. gross margin | **no published consensus found**; the street is anchored on management's ~**72.5%** | inferred from §3 |
| FY2026 full year | revenue **$14.81bn**, EPS **$12.43** | stockanalysis.com <https://stockanalysis.com/stocks/adi/forecast/> |

Consistency check on the FY consensus: H1 FY26 actual is $6,784m revenue / $5.54 adj EPS, so the
street implies H2 of $8,026m / $6.89 — i.e. Q3 ~$3.92bn and Q4 ~$4.11bn, EPS ~$3.33 and ~$3.56.
Internally coherent.

**Zacks notes ADI has beaten consensus in each of the trailing four quarters, average surprise
+5.48%.** Consensus revenue sits only **+$20–30m above the guidance midpoint**, versus a trailing
six-quarter average beat of **+$100m**. Consensus EPS sits only **+$0.03 above the midpoint** versus
a trailing six-quarter average beat of **+$0.137**. **The street is anchoring on the guide and
under-weighting ADI's own beat record.** That is where the relative-scoring points are.

---

## 9. FORECAST (INFERENCE)

| Metric | Forecast | Guide mid | Consensus | vs consensus |
|---|---|---|---|---|
| **Revenue** | **$3,975m** | $3,900m | ~$3,920m | +$55m (+1.4%) |
| **Adjusted diluted EPS** | **$3.42** | $3.30 | $3.33 | +$0.09 |
| **Adjusted gross margin** | **72.7%** | ~72.5% | ~72.5% | +20bps |

### Revenue — $3,975m (+$75m over midpoint, +38.0% y/y, +9.7% q/q)
Build-up from the guided segment deltas, applied at the upper end of each stated range (which is
what ADI has actually delivered in each of the last six quarters):

| Segment | Q2 FY26 | Applied q/q | Q3 FY26E |
|---|---|---|---|
| Industrial | 1,799 | +10% | 1,979 |
| Automotive | 872 | +8% | 942 |
| Communications | 555 | +17% | 649 |
| Consumer | 398 | −5% | 378 |
| **Total** | **3,623** | **+9.7%** | **3,948–4,000 → 3,975** |

Reasons to sit **above** consensus: 17/18 midpoint beats; a +$100m mean absolute beat over the last
six quarters (= 1.00× the guidance band, i.e. the high end); record bookings and positive
book-to-bill going into the quarter; flat-to-declining channel weeks so no sell-in overhang;
data-centre revenue compounding at >90% y/y with the hyperscaler capex cycle still accelerating;
the guide's +7.6% sequential is *below* ADI's own up-cycle Q2→Q3 mean of +8.2%.

Reasons **not** to go all the way to the $4,000m high end: some Q3 automotive demand was pulled
into Q2 by the late-quarter order surge; consumer is guided down and is memory-constrained;
internal utilisation is at optimum so unplanned upside must be sourced externally with lead time;
and Q1 FY2026 (+$60m) showed the beat can compress when the base gets large. $3,975m splits the
difference between the pure historical extrapolation ($4,000m) and the street ($3,920m), leaning
to history.

### Adjusted diluted EPS — $3.42 (+$0.12 over midpoint, +66.8% y/y)
Bottom-up at $3,975m revenue:

| Line | Q3 FY26E |
|---|---|
| Revenue | $3,975m |
| Adj. gross margin @ 72.7% | $2,890m |
| Adj. operating expenses (23.0% of rev; +5.1% q/q from $871.5m) | $916m |
| Adj. operating income → **49.6% adj op margin** (guide 49.0% ±100bps) | $1,974m |
| Adj. nonoperating expense (Q2: $57m) | $57m |
| Adj. pre-tax income | $1,917m |
| Adj. tax @ 12.8% (guide 12–14%; actual run-rate 11.8–12.7%) | $245m |
| Adj. net income | $1,672m |
| Diluted shares (Q2 490.5m less ~2.5m from continued ~$0.8bn/qtr buyback) | ~488m |
| **Adjusted diluted EPS** | **$3.43 → call it $3.42** |

Sensitivities: ±$25m revenue ≈ ±$0.04; ±20bps gross margin ≈ ±$0.014; ±100bps tax rate ≈ ∓$0.04.
The cross-check from history (mean +$0.137 beat over the last six quarters ⇒ $3.44) and the Zacks
"Most Accurate Estimate" ($3.41) both bracket $3.42.

### Adjusted gross margin — 72.7% (−30bps q/q, +350bps y/y)
Bridge from Q2's 73.0%: **−50bps** for the non-repeating channel-repricing benefit (explicitly
disclosed), **+0 to +10bps** utilisation (management says neutral), **+20 to +30bps** mix
(communications guided to grow low-to-mid teens and is above corporate average; consumer, a
below-average business, guided down; industrial mix roughly holds at ~50%), **+10bps** volume
leverage on fixed manufacturing cost from the assumed revenue beat, **−10bps** drag from the extra
external-foundry content needed to service that beat.

I deviate only **+20bps** from the guided ~72.5% because: (a) ADI beat its implied GM guide by
80bps last quarter on exactly the mix dynamic that persists into Q3; but (b) Puccio explicitly
endorsed Rasgon's framing that the guided level is a near-term **ceiling** while utilisation is
maxed, and (c) FY25 Q3 shows a single fab utilisation event can cost 80bps to the downside. The
0.5pp scoring floor on percentage metrics makes a 20bps deviation cheap insurance; a larger one
is not justified by the evidence.

**Sanity check:** 72.7% is comfortably inside ADI's high-60s-to-low-70s historical band (FY22 peak
74.2%, FY24 trough 66.7%) and far from the 55–80% error bounds.

---

## 10. Risks to the forecast

1. **Automotive pull-forward.** Late-Q2 auto orders that management expected in Q3 were shipped in
   Q2. If that borrowing is larger than the ~1pp of segment growth I have assumed, revenue lands
   nearer $3,920–3,940m and my +$55m gap to consensus becomes a penalty.
2. **A single fab utilisation event.** Precisely this cost ADI ~80bps of gross margin in FY25 Q3
   (European fab disruption) and turned a "get to 70%" guide into 69.2%. Q3 is the quarter that
   contains ADI's summer shutdowns.
3. **Memory/substrate shortage bleeding beyond consumer.** Roche flagged memory as a supply-chain
   choke point already forcing consumer customers to make choices; a spread into industrial or
   auto build plans would cap the revenue beat.
4. **Utilisation ceiling forces outsourcing.** Incremental revenue above ~$3.9bn increasingly comes
   from external foundry, which is margin-dilutive — so an unusually large *revenue* beat could
   coincide with a gross-margin *miss*. My forecast pair is deliberately modest on GM for this reason.
5. **Opex step-up.** Q3 adj. opex is the least-visible line: variable comp ratchets with y/y growth
   and operating margin, both of which are running far above plan, and headcount is being added in
   "strategic investment areas." $30m of extra opex is $0.05 of EPS.
6. **Tariffs / export controls / China.** China auto is ~30% of ADI's automotive business and the
   guide is explicitly conditioned on a "dynamic macro and geopolitical environment."

---

## 11. Confidence

**HIGH.** This is close to the best-case setup for a corpus-fundamentals forecast: the target
quarter closed on 1 August 2026, results land 19 August 2026, and the company published an
explicit ±band on both revenue and adjusted EPS plus a quantified verbal bridge on gross margin —
all of it verbatim in the corpus, corroborated by a post-quarter-guide conference appearance on
2 June 2026. The prior-year baseline is triple-sourced (8-K, TTM table in a later 8-K, SEC XBRL).
The residual uncertainty is only *how far above* the guide ADI lands, and that distribution is
well characterised by 18 quarters of guidance-vs-actual history.
