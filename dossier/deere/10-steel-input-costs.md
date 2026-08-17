# Deere FY2026 Q3 — Input Costs and the Steel Linkage

**Agent:** steel-input-costs
**Prepared:** 16 August 2026 (Deere FY2026 Q3 not yet reported; scheduled release **20 August 2026**)
**Forecast quarter:** FY2026 Q3 = fiscal 3 May 2026 → ~2 August 2026 (calendar May–July 2026)
**Corpus root:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere` (paths below are relative to this root)

### Metadata-trap check (required)
`INDEX.md` line for `2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call Transcript` →
`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`. **I read the file. It is Q2 FY2026 material, mislabelled.**
Its content discusses the $272M IEEPA refund recognised in the quarter ended 3 May 2026, the 16.9% Q2 equipment-ops margin, and the "back half of 2026" as *future*. **No FY2026 Q3 actuals exist anywhere in this corpus or in any source I found.** Every Q3 FY2026 figure in this document is an estimate or inference and is labelled as such.

---

## 1. Executive summary

| # | Finding | Type |
|---|---|---|
| 1 | US hot-rolled coil (HRC) spot averaged roughly **$1,120/short ton in May–July 2026 vs ~$860 a year earlier (~+30% YoY)** — the sharpest steel inflation Deere has faced since 2021. | Estimate from market data |
| 2 | But Deere buys steel on **3–6 month lagging contracts** (management's own repeated language). The steel actually *flowing into* Q3 FY26 cost of sales was bought roughly **Nov-2025 → Apr-2026 at ~$940/st vs ~$800/st a year earlier ≈ +15–20% YoY** — materially less than spot. | Inference |
| 3 | Cost inflation is **broad, not steel-only**: copper +47.6% YoY, aluminium +24.7%, WTI crude +33.0%, natural rubber +31.6%, US diesel +$1.54/gal YoY, Cass freight expenditures +11.2% YoY. Only natural gas is down (-6.3%). | Reported fact (market data, 14 Aug 2026) |
| 4 | **Sensitivity: a 10% move in US HRC ≈ $100–250M annualised on Deere equipment-ops cost of sales ≈ 0.25–0.55 pt of equipment-ops gross margin**, of which roughly 35–40% lands in PPA. Central estimate ~$175M/yr, ~0.4 pt. Fully phased in over 2–3 quarters. | Inference (two independent back-solves; see §4) |
| 5 | Management explicitly flagged rising material cost on the 21 May call — *"we are seeing some high levels of inflation over the last two or three months"* — while simultaneously guiding **price-cost to improve in H2** because of favourable tariff and inflation comps and lapped H2-FY25 incentives. Both can be true; the swing factor is which dominates. | Reported fact + inference |
| 6 | **Tariff run-rate ≈ $300M/quarter gross, evenly spread**; the *incremental* YoY tariff headwind collapses from ~$200M in Q2 to ~**$70–80M in Q3** as Deere laps the FY25 tariff ramp. This is the single largest mechanical margin tailwind in the quarter. | Inference from disclosed totals |
| 7 | **Post-guidance positive event: on 1 June 2026 Section 232 tariffs on ag & construction equipment were cut 25% → 15% (effective 8 June 2026, through 31 Dec 2027)**, with a 10% preferential rate for equipment ≥85% US steel/aluminium. Deere's shares rose 4.3% on 3 June 2026. This landed **after** the 21 May guide and is **not** in the $1.2B/$900M tariff numbers. | Reported fact |
| 8 | **A second IEEPA refund tranche is plausible in Q3.** CBP launched refund *Phase 2* on **29 June 2026** (~$28.7B in scope) and Phase 3 in late July 2026. Deere's Q2 $272M was explicitly only "the initial phase." A further recovery would be a large, lumpy, non-operating-quality boost to reported PPA profit and EPS. | Reported fact + inference |

**Net read for the model:** the steel/commodity headwind into Q3 FY26 is real but *lagged and partially absorbed*; the tariff line swings from a large YoY headwind to near-neutral; and there are two identifiable upside wildcards (equipment tariff cut from 8 June, possible IEEPA Phase-2/3 refund) that Deere's 21 May guidance does not contain.

---

## 2. Input-cost levels and YoY change

### 2.1 Steel — US hot-rolled coil, the primary linkage

All prices USD per **short ton**, US Midwest, unless noted. The CME/TradingEconomics front-month series is used as the consistent backbone; SMU/Nucor assessments are cross-checks.

| Date | HRC ($/st) | YoY | Source |
|---|---|---|---|
| ~late Jan 2025 | ~736 *(derived)* | — | back-solved from TE 12-mo change below |
| ~mid Aug 2025 | ~832 *(derived)* | — | back-solved from TE +46.63% at $1,220 |
| 16 Sep 2025 | ~810 | — | steelindustry.news / SMU commentary |
| Oct 2025 | ~814 | — | SMU / futures settlements |
| 12 Nov 2025 | ~834 (spot range 830–865) | — | [Steel Market Update, 12 Nov 2025](https://www.steelmarketupdate.com/2025/11/12/hrc-vs-prime-spread-widens-again-in-november/) |
| Dec 2025 | ~850 (contract settle) | — | SMU / futures |
| **28 Jan 2026** | **970** | **+31.83%** | [TradingEconomics, 28 Jan 2026](https://tradingeconomics.com/commodity/hrc-steel/news/520761) — "highest since January 2024" |
| early Mar 2026 | 990 | — | steelindustry.news (2026) |
| w/c 13 Apr 2026 | 1,045 (Nucor CSP; CSI to 1,095) | — | [steelindustry.news](https://steelindustry.news/hrc-hits-1045-raw-materials-rise-manufacturing-employment-strengthens-section-232-adjustments-what-it-means-for-steel-buyers/) |
| 11 May 2026 | 1,080 | — | steelindustry.news (2026) |
| ~26 May 2026 | 1,095 avg (range 1,070–1,120) | — | SMU weekly assessment |
| June 2026 | ~1,105 (Nucor CSP) | — | [IndexBox, June 2026](https://www.indexbox.io/blog/nucor-raises-hot-rolled-coil-spot-price-by-10-per-ton/) |
| 7 & 14 Jul 2026 | 1,160 avg | — | SMU weekly assessments |
| **21 Jul 2026** | **1,165 avg** | — | [Steel Market Update, 21 Jul 2026](https://www.steelmarketupdate.com/data/prices/); Nucor held at $1,135 ([SMU 20 Jul 2026](https://www.steelmarketupdate.com/2026/07/20/nucor-holds-spot-hr-price-at-1135-ton/)) |
| late Jul 2026 | 1,145 (Nucor CSP, +$10) | — | [IndexBox, late Jul 2026](https://www.indexbox.io/blog/nucor-raises-hot-rolled-coil-spot-price-by-10-per-short-tonne/) |
| **14 Aug 2026** | **1,220** | **+46.63%** (1-mo +2.61%) | [TradingEconomics HRC](https://tradingeconomics.com/commodity/hrc-steel), retrieved 16 Aug 2026 |

**Corroborating primary-adjacent source:** BLS PPI for **steel mill products was ~+22.5% YoY in July 2026** ([BLS PPI, July 2026 release, 13 Aug 2026](https://www.bls.gov/news.release/archives/ppi_08132026.htm); series [WPU1017](https://fred.stlouisfed.org/series/WPU1017)). The PPI (contract-weighted, transaction prices) rising +22.5% while spot rose ~+47% is itself direct evidence of the contract lag — **the PPI is closer to what Deere actually pays than the spot index is.**

**Derived quarterly averages (ESTIMATE):**

| Window | Spot HRC avg | Purpose |
|---|---|---|
| May–Jul 2025 (Q3 FY25 calendar) | ~$860 | prior-year spot |
| **May–Jul 2026 (Q3 FY26 calendar)** | **~$1,120** | **current spot, +~30% YoY** |
| Nov-2024 → Apr-2025 | ~$800 *(low confidence)* | prior-year *lagged purchase* window |
| **Nov-2025 → Apr-2026** | **~$944** | **lagged window feeding Q3 FY26 COGS, ~+15–20% YoY** |

*Confidence note:* the Nov-2024→Apr-2025 average is the weakest number in this dossier. Published quotes for that window range from ~$690 (SMU spot lows, Nov–Dec 2024) to $862 (19 Nov 2024, per one 2025 trade source) to $904–967 (Mar–Apr 2025). I use ~$800 and flag ±$60. Using $860 instead would cut the lagged YoY to ~+10%.

**Drivers of the 2026 steel surge:** Section 232 at 50% since June 2025 with no rollback; the 6 April 2026 proclamation extending 232 to the *full customs value* of covered articles (not just metal content); constrained import volumes; and demand from reshoring/infrastructure. HRC prices in the USA rose ~12.7% in Q1 2026 alone.

### 2.2 Other metals, energy, freight, rubber

All as of **14 August 2026** unless noted; source [TradingEconomics commodity pages](https://tradingeconomics.com/commodities), retrieved 16 Aug 2026.

| Input | Level | 1-month | **YoY** | Notes |
|---|---|---|---|---|
| **US HRC steel** | $1,220 /st | +2.6% | **+46.6%** | See §2.1. All-time high $1,945 (Sep 2021). |
| **Copper** | $6.60 /lb | +4.9% | **+47.6%** | All-time high $6.83 set Aug 2026. Codelco cuts, DRC export restrictions, US import-tariff front-running. |
| **Aluminium (LME)** | $3,247.70 /t | +3.2% | **+24.7%** | July 2026 average $3,161/t. Gulf supply disruption (EGA at 18% capacity); Alunorte gas outage. |
| **WTI crude** | $82.40 /bbl | +3.5% | **+33.0%** | US pressure on Iran, naval blockade, Strait of Hormuz risk. Forecast $84.30 end-Q3. |
| **US on-highway diesel** | $5.13/gal (20 Jul); $5.31 (27 Jul); $5.35 (3 Aug) | rising | **+$1.54/gal vs 2025** | [EIA weekly, via IndexBox/WorkTruck July 2026](https://www.worktruckonline.com/news/july-diesel-trends-update-v2). Bottomed $4.58 on 6 Jul then spiked. |
| **Natural gas (Henry Hub)** | $2.73 /MMBtu | −6.5% | **−6.3%** | The one deflationary input. Record L48 output 111.2 Bcf/d; storage +6.6% vs 5-yr avg. |
| **Natural rubber** | 221.30 USc/kg | +1.8% | **+31.6%** | Crude-linked (synthetic substitution); Indonesian acreage shifting to palm. Well below Feb-2025 peak of 815. |
| **Cass Freight expenditures** | — | — | **+11.2% YoY (July 2026)** | Fastest since late 2022; rate- not volume-driven; 8 consecutive seasonally-adjusted monthly gains. [Cass, July 2026](https://www.cassinfo.com/freight-audit-payment/cass-transportation-indexes/freight-index-archives) |
| **Cass Truckload Linehaul** | 149.4 | −0.9% | **+5.5% YoY (July 2026)** | Same source. |

**Reading:** this is a genuinely broad, energy-led cost shock centred on the *exact* May–July 2026 window, kicked off by the Iran conflict that began between Deere's Q1 (19 Feb) and Q2 (21 May) earnings calls. Deere's own Q2 script names it: *"Since our last earnings call, we have seen the start of the conflict in Iran and the associated inflationary impact on products like oil and fertilizer"* (`call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md`, l.95).

---

## 3. The transmission mechanism: how long is the lag?

Deere has been unusually consistent and explicit about this for over a decade. Direct quotations from the corpus:

| Date | Quote (abridged) | File |
|---|---|---|
| 13 Aug 2014 | *"We are significantly impacted by steel prices, so our **steel costs generally follow the market prices with a lag of three to six months**. If you can forecast steel prices, that should give an indication for material costs."* | `call-transcripts/2014-08-13__de-us-20140813-call-qna__1524330.md` l.47 |
| 20 May 2016 | *"The way our contracts are set up, we don't have a lot of risk through third quarter. Going into fourth quarter… For us, the risk is fourth quarter."* (said in May, about a spike that began ~Feb–Mar) | `call-transcripts/2016-05-20__de-us-20160520-call-qna__1482770.md` l.47–49 |
| 15 Feb 2019 | *"With regards to the higher production costs, it's important to note that **our steel contracts operate on a three to six-month lag**."* | `call-transcripts/2019-02-15__de-us-20190215-call-pres-2__1421659.md` l.23 |
| 17 May 2019 | *"With regards to material cost inflation, keep in mind that **our steel contracts operate on a three to six-month lag to spot prices.**"* | `call-transcripts/2019-05-17__de-us-20190517-call-pres-2__1392890.md` l.19 |
| 25 Nov 2020 | *"Our contracts, we tend to **cover a quarter, a little bit more** in terms of the lag time between price movements and when we see those come through… to the extent you see some of that inflation, probably more impactful later in the year."* | `call-transcripts/2020-11-25__de-us-20201125-call-qna__46453.md` l.45 |
| 20 May 2022 | *"**Lagging contracts on steel means we've seen progressively higher costs since Q3 of 2021.**"* (HRC peaked Sep 2021 → cost peak in Deere's Q1–Q2 FY2022) | `call-transcripts/2022-05-20__de-us-20220520-call-pres__46444.md` l.75 |
| 24 Nov 2021 | *"Traditionally we buy, you know, **roughly a quarter ahead**… you've seen steel moderate some from where it was peaking probably a bit a quarter or so ago. We haven't adjusted significantly."* | `call-transcripts/2021-11-24__de-us-20211124-call-qna__46439.md` l.143 |

### 3.1 Case study — the 2018 Section 232 shock (a close analogue)

| Event | Date | What Deere said / did |
|---|---|---|
| Section 232 steel tariffs imposed | Mar 2018 (effective 23 Mar) | *"232 issues related to steel didn't start until the second quarter of 2018"* (`2019-02-15…qna`, l.19) — i.e. **first cost impact ~1 quarter after imposition**. |
| Deere Q2 FY18 call | 18 May 2018 | Cost-of-sales guide raised **75% → 76% of net sales**, *"due largely to inflation in U.S. steel prices and a tight market for logistics providers."* Pricing actions announced for C&F "over the remainder of the year"; A&T pricing deferred to the annual model-year cycle. (`call-transcripts/2018-05-18__de-us-20180518-call-pres-2__1475345.md` l.53, l.65) |
| Peak cost impact | Q4 FY18 (Aug–Oct 2018) | *"As you think about hot rolled coil on the ag side of the business, **our fourth quarter is kind of where we saw the higher level of steel pricing**"* (`2018-11-21…qna`, l.155). HRC spot peaked ~Jul 2018 → **~1–2 quarters to peak COGS**. |
| Relief | Q3–Q4 FY19 | *"As we get to the latter part of the third quarter and into the fourth quarter, we see some of that pricing abate **due to our lags in our contracts**"* (`2019-02-15…qna`, l.19, l.53). |
| Price recovery | FY19 | ~3 points of price realisation guided, explicitly *"to offset both material cost and freight inflation experienced in 2018 as well as any additional increases forecasted in 2019"* (`2018-11-21…call-pres-2`, l.67) — **full price recovery took ~4–6 quarters.** |

### 3.2 Case study — 2021–2022 inflation

| Date | Disclosure | File |
|---|---|---|
| 21 May 2021 | Material + freight cost forecast **$1.0B for FY21, ~75% of it in H2** — up from a $500M forecast one quarter earlier (i.e. it *doubled* in a quarter). | `call-transcripts/2021-05-21__de-us-20210521-call-pres__46476.md` l.57; `…qna__46488.md` l.175 |
| 24 Nov 2021 | FY2022 guide: **~$2.0B material + freight headwind vs FY2021, split ~80% material / ~20% freight** (≈$1.6B material). | `call-transcripts/2021-11-24__de-us-20211124-call-qna__46439.md` l.143 |
| 20 May 2022 | *"We experienced the most difficult material and freight compares in H1 of 2022… commodities such as copper and aluminum, electronics, and even things like labor and energy are increasing. We'll begin to anniversary some of these cost increases in the third and fourth quarter."* | `call-transcripts/2022-05-20__de-us-20220520-call-pres__46444.md` l.75 |
| 23 Nov 2022 | *"Certain raw materials like **hot-rolled coil steel are easing**, as you can see in some of the different indices… On the other hand, labor and energy costs will increase."* | `call-transcripts/2022-11-23__de-us-20221123-call-pres__46446.md` l.87 |

**Lag conclusion (INFERENCE, high confidence):**
- **Contract lag to Deere's purchase price: 3–6 months** (company-stated, unchanged since at least 2014).
- **Purchase price to reported cost of sales: a further ~1 quarter**, because Deere uses standard costing and inventory turns (`Ratio to prior 12 months' cost of sales` for inventory was **27%** at 3 May 2026, i.e. ~3.2 months of inventory — `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` l.2147).
- **Total spot → P&L lag: ~2 quarters, with peak impact 2–3 quarters after the spot move.**

**Direct application to Q3 FY26:** the May–July 2026 spot spike to ~$1,120–1,220/st largely does **not** hit Q3 FY26 COGS. It hits **Q4 FY2026 and Q1 FY2027**. Q3 FY26 COGS reflects roughly Nov-2025→Apr-2026 purchases (~+15–20% YoY). The forward risk is therefore to Q4 FY26 guidance, not to the Q3 print itself.

### 3.3 Deere does *not* hedge commodities
The FY2025 10-K market-risk section discloses FX and interest-rate hedging in detail and quantifies a 10%-USD FX sensitivity (~$100M), but contains **no commodity derivative programme** (`filings/2025-11-26__de-us-20251126-q4-10k__469216.md`, l.4424 ff.). Deere manages steel risk through **contract structure (the 3–6 month lag) and supplier agreements**, not derivatives. Confirmed by the 2021 exchange: *"From a purchasing point of view, we haven't made significant shifts… we haven't locked anything in at this point."*

---

## 4. Quantified sensitivity: what does 10% on steel do to gross margin?

Deere has never disclosed its steel spend. Two independent back-solves:

**Method A — the 2018 tariff episode.**
FY2018 cost-of-sales guidance rose 1.0 pt (75%→76%) on equipment-ops net sales of ~$33B → ~$330M, attributed to *material + freight + incentive comp*. Assigning ~50–65% to material → ~$170–215M. FY2018 average HRC was ~+34% vs FY2017. → **10% HRC ≈ $50–65M/yr ≈ 0.15–0.20 pt of equipment-ops gross margin (on the FY2018 revenue base).**

**Method B — the FY2022 episode.**
FY2022 material headwind ~$1.6B on FY2021 equipment-ops COGS of ~$29B. Deere's *realised* (lagged) steel cost roughly doubled between FY2021 and FY2022. If steel were ~60–70% of that $1.6B (the rest copper, aluminium, electronics, resins, purchased components), the steel base was ~$1.0–1.1B. → **10% HRC ≈ $100–110M/yr on a ~$29B COGS base ≈ 0.25–0.30 pt of gross margin.**

**Scaling to FY2026.** Equipment-ops cost of sales is running ~$30–32B annualised (H1 FY26 actual: $14,568M — `2026-05-28 10-Q` segment note). Deere's steel-linked spend (direct coil/plate/bar plus the steel content embedded in castings, forgings, and purchased components) is plausibly **$1.5–2.5B/yr, i.e. 5–8% of COGS**.

> **INFERENCE — headline sensitivity**
> **A sustained 10% move in US HRC ≈ $150–250M annualised on Deere equipment-ops cost of sales ≈ $40–60M per quarter ≈ 0.35–0.55 pt of equipment-ops gross margin**, phased in over 2–3 quarters and offset over 4–6 quarters by pricing.
> **Central point estimate: ~$175M/yr, ~0.40 pt of gross margin.** Range on the low side (~$100M, 0.25 pt) if Method A is more representative.
>
> **PPA share.** PPA is ~36% of FY2026 equipment-ops sales (FY26 guide: PPA down 5–10% off ~$17.3B → ~$16B; equipment ops ~$44B) and is steel-heavy (large tractors, combines). Allocating **35–40%** of the steel exposure to PPA:
> **10% HRC ≈ $55–90M/yr to PPA operating profit ≈ $14–23M per quarter ≈ ~0.4 pt of PPA operating margin.**

**Applied to Q3 FY2026 specifically:** the lagged, effective steel-cost inflation entering Q3 FY26 COGS is ~+15–20% YoY → **~$60–110M of YoY steel headwind at the enterprise level in the quarter, of which ~$20–40M in PPA.** Add the rest of the basket (copper, aluminium, rubber, resins, energy, freight) and the total material+freight YoY headwind is plausibly **$200–350M enterprise-wide in Q3 FY26** — broadly consistent with Q2's disclosed shape (see §5).

**Offsets the model must not forget:** Deere targets ~2.5%/yr structural direct-material cost reduction (`call-transcripts/2017-08-18…qna__1478901.md` l.39: *"direct material cost reduction of 2.5% per year is what we baked in with structural cost reduction"*), and FY2026 guided price realisation is **+1.5% to +2.0%** for the equipment operations (+1.0% for PPA specifically).

---

## 5. What Deere actually reported and guided (the Q2 FY2026 baseline)

### 5.1 Reported fact — Q2 FY2026 (quarter ended 3 May 2026)

| Metric | Q2 FY26 | Q2 FY25 | Source |
|---|---|---|---|
| Net sales and revenues | $13,369M | $12,763M (+5%) | `filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md` l.85 |
| Diluted EPS (GAAP) | $6.55 | $6.64 | ibid l.66 |
| **PPA net sales** | **$4,503M** | $5,230M (−14%) | ibid l.220 |
| **PPA operating profit** | **$706M (15.7% margin)** | $1,148M (22.0%) | `2026-05-28 10-Q` MD&A |
| PPA cost of sales | $3,100M | $3,398M | `2026-05-28 10-Q` segment note |
| Consolidated cost of sales / net sales | **70.2%** | 68.1% | `2026-05-28 10-Q` l.1964 |
| H1 cost of sales / net sales | 73.5% | 70.3% | ibid |

10-Q attribution of the cost-of-sales ratio move (l.1966–1968): **Material costs — Unfavorable; Tariffs net of recoveries — Favorable (Q2) / Unfavorable (H1); Production efficiencies — Favorable.** *"Increased mostly due to **higher material costs as a result of inflationary pressures**."*

### 5.2 Management commentary on the cost bridge — 21 May 2026

- *"We did see higher year-over-year production costs in the second quarter, excluding the impact from tariff refunds. Without accounting for tariff refunds, **year-over-year direct tariff expense was approximately $200 million of the headwind, with the remainder largely driven by higher material and freight costs.**"* (`…call-pres__1042774.md` l.81)
- *"All three business units benefited from a one-time lift from tariff refunds, which helped **offset ongoing inflationary pressures on materials and freight**."* (l.137)
- Analyst (Mig Dobre, Baird) pushback: *"everything that I'm kind of seeing on the cost side, whether it's raw materials, whether it's components, energy prices, all suggest that things get tougher going forward rather than easier."* Response: *"From a material standpoint, we have seen some inflation come in… **I would agree with you that we are seeing some high levels of inflation over the last two or three months.**"* (`…call-qna__1042775.md` l.119–123)
- But: *"As we get to the back half of 2026 and start to lap not only the tariff expense that came into the organization in the back half of last year, but also the associated inflation… **You start to see more favorable comps from both a tariff standpoint and a material cost standpoint in the back half.** … Actually, price gets more favorable in the back half… **Price cost will improve as we move through the balance of the fiscal year.**"* (l.39–41)
- Overhead absorption: *"a little bit better absorption in the fourth quarter as production rates are significantly higher… that's just the way the order book built this year for a much heavier fourth quarter"* (l.125) — note this is a **Q4**, not Q3, tailwind.

### 5.3 FY2026 guidance in force (as of 21 May 2026)

| Item | Guide |
|---|---|
| Net income attributable to Deere, FY2026 | **$4.5B – $5.0B** (raised from $4.0–4.75B at Q4 FY25) |
| PPA net sales | Down 5–10%; currency +3.0%; price realisation ~+1.0% |
| SAT net sales | Up ~15%; currency +1.0%; price ~+1.5% |
| C&F net sales | Up ~20%; currency +2.0%; price ~+2.5% |
| Financial Services net income | ~$860M |
| Equipment-ops net price realisation | +1.5% to +2.0% (≈ ex-tariff general inflation of 1.5–2.0%) |
| Direct tariff expense (gross) | ~$1.2B pretax (~3 pts of margin); **~$900M net of the $272M refund** |

Source: `filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md` l.74, l.161–166; call transcript l.85–89.

---

## 6. US tariffs in force during FY2026 Q3, and Deere's exposure

### 6.1 The 2026 tariff timeline

| Date | Event | Source |
|---|---|---|
| Jun 2025 | Section 232 steel & aluminium raised **25% → 50%** (UK 25%). | [CRS IN12519](https://www.congress.gov/crs-product/IN12519) |
| 18 Aug 2025 | Scope of steel/aluminium **derivative** duties expanded to more HTS codes. | `filings/2025-08-14__de-us-20250814-q3-10q__155834.md` l.1985 |
| 5 Nov 2025 | Supreme Court hears IEEPA oral argument. | `filings/2025-11-26__de-us-20251126-q4-10k__469216.md` l.1268 |
| **20 Feb 2026** | **Supreme Court invalidates IEEPA tariffs** (*Learning Resources, Inc. v. Trump*). Within hours the White House reimposes a **10% across-the-board tariff under Section 122** of the Trade Act of 1974. | `filings/2026-05-28…q2-10q__1055932.md` l.1880; [Global Trade Alert](https://globaltradealert.org/blog/from-ieepa-to-section-122) |
| **6 Apr 2026** | **Section 232 restructured**: 50% on HS ch. 72/73/74/76 (steel, aluminium, **copper**); derivatives >15% metal content at 25%; US-origin metal used abroad 10%; Russian aluminium 200%. **Critically: duties now apply to the *entire customs value* of covered articles, not just the metal content.** Metal <15% by weight excluded; many derivatives removed (Annex II); certain industrial/grid equipment capped at 15% through 2027 (Annex III). | [C.H. Robinson advisory, 6 Apr 2026](https://www.chrobinson.com/en-us/resources/insights-and-advisories/client-advisories/2026q2/04-06-2026-us-expands-n-increases-sec232-tariffs-on-aluminum-steel-n-copper-effective-apr-6/); [GHY](https://www.ghy.com/trade-compliance/us-adjusts-section-232-tariffs-on-aluminum-steel-and-copper-full-customs-value-now-applies/) |
| **20 Apr 2026** | CBP launches the **IEEPA refund claim system**. Deere files and CBP accepts a **$272M** claim. | `filings/2026-05-28…q2-10q__1055932.md` l.1880 |
| **7 May 2026** | **CIT strikes down the 10% Section 122 tariff** (relief limited to three plaintiff importers). **12 May 2026: Federal Circuit administrative stay** — Section 122 remains collected pending appeal. | [Skadden](https://www.skadden.com/insights/publications/2026/05/us-trade-court-strikes-down-section-122-tariffs); [Gibson Dunn](https://www.gibsondunn.com/section-122-global-tariffs-invalidated-by-the-court-of-international-trade/) |
| **1 Jun 2026 (proclamation), effective 8 Jun 2026 – 31 Dec 2027** | **Section 232 tariffs on select agricultural and construction equipment cut 25% → 15%**; new **10% preferential rate** for imported capital equipment with **≥85% US-produced steel/aluminium** (eligible origins: EU, Japan, S. Korea, UK, Taiwan, Switzerland, Liechtenstein, Argentina, Ecuador, El Salvador, Guatemala). Canada/Mexico: 25% on non-US content, 15% minimum effective. | [AEM](https://www.aem.org/news/section-232-tariff-changes-what-manufacturers-need-to-know); [Farm Progress](https://www.farmprogress.com/farm-policy/u-s-cuts-tariffs-on-farm-and-construction-equipment-to-15-); [AGDAILY](https://www.agdaily.com/news/farm-equipment-tariffs-cut-from-25-to-15/) |
| **3 Jun 2026** | **Deere shares +4.3%** on the equipment tariff cut. Commentary noted Deere could qualify for the 10% rate on some products since ~90% of its raw materials are US-sourced. | [Investing.com, 3 Jun 2026](https://www.investing.com/news/stock-market-news/deere-stock-jumps-on-tariff-cut-for-farm-equipment-93CH-4722460) |
| **29 Jun 2026** | **CBP IEEPA refund Phase 2 opens** (~$28.7B scope; unliquidated entries and entries within 80 days of liquidation). | [Thompson Hine SmarTrade](https://www.thompsonhinesmartrade.com/2026/06/cbp-confirms-june-29-2026-ieepa-tariff-refund-process-phase-2-launch/) |
| late Jul 2026 | **Phase 3** opens (finally-liquidated entries). As of 10 Jul 2026, **$86.3B repaid** to importers (incl. interest) against $121.75B accepted; June alone $49.1B. | [Thompson Hine](https://www.thompsonhinesmartrade.com/2026/06/cbp-announces-phases-2-and-3-of-the-ieepa-tariff-refund-process/); [Cato](https://www.cato.org/blog/ieepa-refunds-update-good-progress-still-ways-go) |

### 6.2 Deere's disclosed tariff exposure — the full series (REPORTED FACT)

| Period | Direct incremental tariff cost | Source |
|---|---|---|
| FY2025 9M (through 27 Jul 2025) | ~$300M | `filings/2025-08-14…q3-10q__155834.md` l.2032 |
| FY2025 Q3 alone | ~$200M ("a couple of 100,000,000 impact in Q3") | `call-transcripts/2025-08-15…q3-qna__143409.md` l.123 |
| FY2025 Q4 (then-forecast) | ~$300M | ibid |
| **FY2025 full year** | **~$600M** | `filings/2025-11-26…q4-10k__469216.md` l.1211, l.2481 |
| FY2025 Q4 margin impact | >3 pts on equipment-ops margin in the quarter | `call-transcripts/2025-11-26…call-q4-pres-2__361265.md` l.57 |
| FY2026 H1 (six months to 3 May 2026) | **$372M net of the $272M recovery** ⇒ **~$644M gross**; vs ~$95M in H1 FY2025 | `filings/2026-05-28…q2-10q__1055932.md` l.1878 |
| FY2026 Q2 YoY headwind, ex-refund | ~$200M | `…call-pres__1042774.md` l.81 |
| **FY2026 full year (guide)** | **~$1.2B gross (~3 pts of margin); ~$900M net of the $272M refund** | `…call-pres__1042774.md` l.85; `…call-qna__1042775.md` l.25 |
| Quarterly run-rate | *"pretty evenly spread, roughly **$300 million per quarter**"* | `call-transcripts/2025-11-26…call-q4-qna__361266.md` l.15 |
| Segment split of the $1.2B | **C&F ~45%, SAT ~1/3, PPA ~20%** | `…call-qna__1042775.md` l.27 |
| Segment split of the $272M refund | **C&F 50%, SAT 30%, PPA 20%** (= **~$54M to PPA**, recorded as a reduction of cost of sales) | `filings/2026-05-28…q2-10q__1055932.md` l.1880; `…call-qna__1042775.md` l.29 |
| PPA-specific tariff margin impact, FY2026 | ~1.5 pts for the full year | `call-transcripts/2025-11-26…call-q4-qna__361266.md` l.23 |
| Composition of the $1.2B (as at Q1 FY26) | IEEPA "a little less than half"; Section 232 "a little bit higher" | `call-transcripts/2026-02-19…call-qna__605077.md` l.105 |
| Q1 FY26 mitigation note | *"mitigation on Section 232 steel tariffs and some relief in India have been offset by volume growth"* | `call-transcripts/2026-02-19…call-pres__605076.md` l.49 |

### 6.3 Deere's stated posture — no surcharges, cost-side mitigation only

- *"We are **not surcharging our customers on tariffs**… Instead, we are focusing on reducing our tariff exposure through cost actions. Things like resourcing, reshoring, exemption submissions, ensuring USMCA compliance. I have full confidence that we will largely counter the negative financial impact of tariffs over the coming periods, largely through cost measures without ever having to rely on any surcharges."* — Brent Norwood, CFO, 21 May 2026 (`…call-qna__1042775.md` l.37)
- *"Approximately **80% of John Deere's U.S. complete good sales are produced at our U.S. manufacturing facilities**, and roughly **75% of those components used at those facilities are sourced from U.S.-based suppliers.**"* (`…call-pres__1042774.md` l.91). The 10-K states it as *"Nearly 80% of our domestic sales are assembled in the U.S., with the remaining products imported primarily from Europe, Mexico, India, and Japan"* (`filings/2025-11-26…q4-10k__469216.md` l.2481).
- Known structural exposure: **small-frame skid steers and compact track loaders were moved to Mexico in 2024** and became tariff-exposed in 2025; USMCA qualification is being pursued (`filings/2025-11-26…q4-10k__469216.md` l.1312).
- Rare-earth dependence on China flagged as a supply-chain risk (l.1328).

### 6.4 The Q3 FY2026 tariff arithmetic (INFERENCE)

| | FY25 | FY26 | YoY |
|---|---|---|---|
| H1 gross tariff | ~$95M | ~$644M | +$549M |
| **Q3 gross tariff** | **~$200M** (stated) | **~$278M** (= ($1,200 − $644) ÷ 2, before the 8 June equipment-tariff cut) | **≈ +$78M** |
| Q4 gross tariff | ~$300M | ~$278M | ≈ −$22M |

**This is the single most important mechanical change in the Q3 P&L bridge:** the incremental YoY tariff drag falls from ~$200M in Q2 to roughly **$70–80M in Q3**, and the 8 June cut (25%→15%, plus a possible 10% rate on high-US-content items) should push the Q3 figure *below* $278M. **The Q3 gross tariff line could plausibly come in at $230–270M, making the YoY tariff comparison close to neutral or even slightly favourable.** PPA carries ~20% of tariff cost, so PPA's YoY tariff delta in Q3 is likely **under $20M** — versus a ~$54M *benefit* in Q2 from the refund allocation, which does **not** repeat unless a new refund tranche is booked.

### 6.5 The refund wildcard
Deere's Q2 language was deliberately narrow: *"Based on the **eligibility parameters established by the CBP for the initial phase** of the refund process, we prepared and filed a refund claim in the amount of $272, which has been accepted."* Phases 2 and 3 opened **within Deere's fiscal Q3** (29 June and late July 2026). Deere's IEEPA-attributable payments were "a little less than half" of an ~$1.2B FY26 run-rate plus a share of FY2025's ~$600M — so the theoretical remaining claim pool is several hundred million dollars.
**INFERENCE:** a second recovery booked in Q3 FY2026 is a genuine possibility. If one lands, it flows through **cost of sales** with a **20% PPA / 30% SAT / 50% C&F** allocation on Q2 precedent, and would be a large, non-recurring boost to reported PPA operating profit and GAAP EPS. **This is the biggest single upside tail on the Q3 print, and the biggest reason a GAAP-EPS forecast should carry a fat right tail.**

---

## 7. Net effect on the three forecast lines — how to use this

*(Directional guidance for the modelling agent, not a forecast. Consensus for Q3 FY26 is EPS $4.85 vs $4.75 a year ago, per [Yahoo/Barchart preview, Aug 2026](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html); Deere reports 20 Aug 2026.)*

**Revenue (net sales and revenues).** Input costs do not directly drive the top line, but two second-order channels matter: (a) **price realisation** is guided at +1.5–2.0% equipment-ops / +1.0% PPA and Deere has repeatedly refused to surcharge, so cost inflation will *not* show up as extra revenue in Q3; (b) **farmer input-cost inflation** (fuel, fertiliser — Deere's own Q2 script names both) is a demand headwind for large ag, already reflected in the "down 15–20%" US/Canada large-ag industry guide. Prior-year base: Q3 FY25 net sales and revenues **$12,018M**.

**Diluted GAAP EPS.** Prior-year base **$4.75**. Cost side: ~$60–110M of lagged steel headwind plus a broader material/freight basket, partly offset by ~$70–80M *less* incremental tariff drag than Q2 carried, the 8 June equipment-tariff cut (in-quarter from ~week 6), production efficiencies from higher SAT/C&F volumes, and structural material-cost reduction. **Skew the distribution right** for a possible IEEPA Phase-2/3 refund.

**PPA operating profit.** Prior-year base **$580M on $4,273M of net sales (13.6% margin)**. PPA-specific factors: ~20% of tariff cost and ~1.5 pts of full-year tariff margin drag; **no repeat of the ~$54M Q2 refund allocation unless a new tranche is booked**; ~$20–40M of lagged steel/material headwind; only +1.0% price; PPA volumes still declining (FY26 guide down 5–10%, though management called Q2 "the toughest comp" with the back half easier on the top line); and the *heavier* Q4 large-tractor build means the **overhead-absorption tailwind is a Q4 story, not a Q3 one**.

---

## 8. Gaps and where I looked

| Gap | Where I looked | Status |
|---|---|---|
| Deere's actual steel tonnage or $ spend | All 10-Ks 2015–2025, all transcripts 2012–2026 (`rg -i "steel"`, `"direct material"`, `"commodity basket"`) | **Not found — never disclosed.** Sensitivity in §4 is a back-solve. |
| Any commodity hedging programme | FY2025 10-K market-risk and derivatives notes | **Not found — Deere hedges FX and rates only.** Confirmed by 2021 management comment. |
| Segment-level cost of sales for Q3 FY2025 | `filings/2025-08-14…q3-10q__155834.md` segment note | **Not disclosed in that filing** (pre-ASU 2023-07 format). FY26 Q2 10-Q *does* disclose it. |
| BLS PPI July 2026 primary release | bls.gov (403 Forbidden to automated fetch, twice) | Steel mill products **+22.5% YoY July 2026** taken from secondary reporting of the [13 Aug 2026 release](https://www.bls.gov/news.release/archives/ppi_08132026.htm). **Verify against the primary release before publishing.** |
| Nov-2024 → Apr-2025 HRC monthly averages | Multiple searches; sources conflict ($690 SMU spot lows vs $862 on 19 Nov 2024 vs $904–967 Mar–Apr 2025) | **Low confidence.** ±$60 on the ~$800 lagged-window average → the lagged YoY could be +10% rather than +18%. |
| Whether Deere has already booked or disclosed an IEEPA Phase-2/3 refund | Corpus (frozen 14 Aug 2026, nothing after 28 May); web searches on CBP phases | **Unknown.** No Deere-specific Phase-2 disclosure found. Treat as an open upside tail. |
| Quantified $ impact on Deere of the 8 June equipment-tariff cut | Deere IR, news coverage, analyst notes | **Not found.** One preview cites a **$0.10–$0.15 FY2026 EPS** benefit for the 25%→15% cut ([Yahoo/Barchart, Aug 2026](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html)) — third-party estimate, not company-sourced. |
| Deere-specific freight cost disclosure for 2026 | Q2 FY26 10-Q and call | Only qualitative ("higher material and freight costs"). No $ split since the FY2022 80/20 disclosure. |

---

## 9. Source list

**Corpus (relative to `challenge/offline-data/deere/`)**
- `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` — Q2 FY26 10-Q (filed 28 May 2026): tariff disclosure l.1876–1880; cost-of-sales ratio l.1955–1968; segment note l.845–900; inventory ratio l.2147
- `filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md` — Q2 FY26 earnings release and FY2026 outlook
- `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` — Q2 FY26 prepared remarks
- `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` — Q2 FY26 Q&A (**mislabelled "Q3 2026" in INDEX.md**)
- `call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md`, `…call-qna__605077.md` — Q1 FY26
- `filings/2025-11-26__de-us-20251126-q4-10k__469216.md` — FY2025 10-K
- `call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md`, `…call-q4-qna__361266.md` — Q4 FY25 / FY26 guide
- `filings/2025-08-14__de-us-20250814-q3-10q__155834.md`, `filings/2025-08-15__de-us-20250815-q3-8k__143410.md`, `call-transcripts/2025-08-15…q3-qna__143409.md` — Q3 FY2025 (the comparison base)
- Historical steel-lag evidence: `call-transcripts/2014-08-13…qna__1524330.md`, `2016-05-20…qna__1482770.md`, `2017-08-18…qna__1478901.md`, `2018-05-18…call-pres-2__1475345.md` & `…qna__1475349.md`, `2018-11-21…qna__1441804.md` & `…call-pres-2__1441802.md`, `2019-02-15…call-pres-2__1421659.md` & `…qna__1421664.md`, `2019-05-17…call-pres-2__1392890.md` & `…qna__1392891.md`, `2019-11-27…qna__1347451.md`, `2020-11-25…qna__46453.md`, `2021-02-19…call-pres__46420.md`, `2021-05-21…call-pres__46476.md` & `…qna__46488.md`, `2021-11-24…qna__46439.md`, `2022-05-20…call-pres__46444.md` & `…qna__46464.md`, `2022-08-19…qna__46489.md`, `2022-11-23…call-pres__46446.md`

**Web (all retrieved 16 August 2026)**
- https://tradingeconomics.com/commodity/hrc-steel — HRC $1,220/st, +46.63% YoY, 14 Aug 2026
- https://tradingeconomics.com/commodity/hrc-steel/news/520761 — HRC $970, +31.83% YoY, 28 Jan 2026
- https://tradingeconomics.com/commodity/copper — $6.60/lb, +47.60% YoY, 14 Aug 2026
- https://tradingeconomics.com/commodity/aluminum — $3,247.70/t, +24.74% YoY, 14 Aug 2026
- https://tradingeconomics.com/commodity/crude-oil — WTI $82.40, +32.95% YoY, 14 Aug 2026
- https://tradingeconomics.com/commodity/natural-gas — $2.73/MMBtu, −6.28% YoY, 14 Aug 2026
- https://tradingeconomics.com/commodity/rubber — 221.30 USc/kg, +31.57% YoY, 14 Aug 2026
- https://www.steelmarketupdate.com/data/prices/ — SMU HRC assessments, 2026
- https://www.steelmarketupdate.com/2026/07/20/nucor-holds-spot-hr-price-at-1135-ton/ — 20 Jul 2026
- https://www.steelmarketupdate.com/2025/11/12/hrc-vs-prime-spread-widens-again-in-november/ — 12 Nov 2025
- https://www.indexbox.io/blog/nucor-raises-hot-rolled-coil-spot-price-by-10-per-short-tonne/ — Nucor $1,145, late Jul 2026
- https://www.indexbox.io/blog/nucor-raises-hot-rolled-coil-spot-price-by-10-per-ton/ — Nucor $1,105, Jun 2026
- https://steelindustry.news/hrc-hits-1045-raw-materials-rise-manufacturing-employment-strengthens-section-232-adjustments-what-it-means-for-steel-buyers/ — HRC $1,045, Apr 2026
- https://www.bls.gov/news.release/archives/ppi_08132026.htm — PPI, July 2026 release (13 Aug 2026); steel mill products +22.5% YoY *(secondary-sourced; verify)*
- https://fred.stlouisfed.org/series/WPU1017 — PPI steel mill products series
- https://www.cassinfo.com/freight-audit-payment/cass-transportation-indexes/freight-index-archives — Cass, July 2026: expenditures +11.2% YoY, truckload linehaul 149.4 (+5.5% YoY)
- https://www.worktruckonline.com/news/july-diesel-trends-update-v2 — EIA diesel, July 2026: $5.13/gal 20 Jul, +$1.54 YoY
- https://www.chrobinson.com/en-us/resources/insights-and-advisories/client-advisories/2026q2/04-06-2026-us-expands-n-increases-sec232-tariffs-on-aluminum-steel-n-copper-effective-apr-6/ — Section 232, effective 6 Apr 2026
- https://www.ghy.com/trade-compliance/us-adjusts-section-232-tariffs-on-aluminum-steel-and-copper-full-customs-value-now-applies/ — full-customs-value change
- https://www.aem.org/news/section-232-tariff-changes-what-manufacturers-need-to-know — 1 Jun 2026 proclamation; effective 8 Jun 2026 – 31 Dec 2027
- https://www.farmprogress.com/farm-policy/u-s-cuts-tariffs-on-farm-and-construction-equipment-to-15- — farm/construction equipment 25% → 15%
- https://www.agdaily.com/news/farm-equipment-tariffs-cut-from-25-to-15/ — same
- https://www.investing.com/news/stock-market-news/deere-stock-jumps-on-tariff-cut-for-farm-equipment-93CH-4722460 — DE +4.3%, 3 Jun 2026
- https://globaltradealert.org/blog/from-ieepa-to-section-122 — 20 Feb 2026 IEEPA → Section 122
- https://www.skadden.com/insights/publications/2026/05/us-trade-court-strikes-down-section-122-tariffs — CIT ruling 7 May 2026; Fed. Cir. stay 12 May 2026
- https://www.gibsondunn.com/section-122-global-tariffs-invalidated-by-the-court-of-international-trade/ — same
- https://www.thompsonhinesmartrade.com/2026/06/cbp-confirms-june-29-2026-ieepa-tariff-refund-process-phase-2-launch/ — Phase 2, 29 Jun 2026
- https://www.thompsonhinesmartrade.com/2026/06/cbp-announces-phases-2-and-3-of-the-ieepa-tariff-refund-process/ — Phases 2 & 3
- https://www.cato.org/blog/ieepa-refunds-update-good-progress-still-ways-go — $86.3B repaid as of 10 Jul 2026
- https://www.congress.gov/crs-product/IN12519 — CRS, Section 232 steel & aluminium
- https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html — Q3 FY26 consensus EPS $4.85; report date 20 Aug 2026
- https://www.deere.com/en-us/john-deere-news/fy2026-q3-announcement — Deere Q3 FY2026 earnings date announcement
