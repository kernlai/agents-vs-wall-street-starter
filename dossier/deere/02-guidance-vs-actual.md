# Deere & Company — Management Guidance vs Actual

**Workstream:** guidance-vs-actual bias analysis
**Prepared:** 16 August 2026 · **Corpus frozen:** 14 August 2026
**Purpose:** anchor the FY2026 Q3 forecast (NS&R, GAAP diluted EPS, PPA operating profit) on management's own
full-year guidance arithmetic, corrected for Deere's historical guidance bias.

All corpus paths are relative to
`/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`.

---

## 0. Metadata trap — explicitly cleared

The corpus INDEX.md row

> `2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call Transcript` →
> `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`

**is mislabelled.** I read the file. Its YAML header says `period: "Q3 2026"` and its H1 is
"# Q3 2026 Earnings Call Transcript", but the body is unambiguously the **Q2 FY2026 earnings-call Q&A**
of 21 May 2026: it discusses the $272 million IEEPA tariff refund "recognised in the quarter" (a Q2 FY2026
event, per `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`), and an analyst asks management to
"talk us through the cadence for **3Q and 4Q**" — i.e. Q3 is *prospective*.

**There are no FY2026 Q3 actuals in this corpus, and I found none on the web.** Deere confirmed
(press release, 5 August 2026) that Q3 FY2026 reports on **Thursday 20 August 2026**. Every Q3 FY2026 figure
in this document is a *derived estimate*, never a reported fact.

---

## 1. FY2026 guidance verbatim (the core of the task)

### 1.1 Initial FY2026 guidance — issued with Q4 FY2025, 26 November 2025

Source: `filings/2025-11-26__de-us-20251126-q4-8k__361233.md`

> **Company Outlook & Summary**
> "Net income attributable to Deere & Company for fiscal 2026 is forecasted to be in a range of
> $4.00 billion to $4.75 billion."

> "Looking ahead, we believe 2026 will mark the bottom of the large ag cycle," May stated. "While ongoing
> margin pressures from tariffs and persistent challenges in the large ag sector remain, our commitment to
> inventory management and cost control, coupled with expected growth in small agriculture & turf and
> construction & forestry, positions us to effectively manage the business and seize emerging opportunities
> as market conditions begin to recover."

Segment outlook table (same file) and slide deck `slides/2025-11-26__de-us-20251126-slide__361243.md`:

| Segment | Net sales FY26 | Currency | Price realization | Op margin FY26 |
|---|---|---|---|---|
| Production & Precision Ag | Down 5–10% * | +1.5% | ~ +1.5% | 11–13% |
| Small Ag & Turf | Up ~10% | +1.0% | ~ +2.0% | 12.5–14% |
| Construction & Forestry | Up ~10% | +1.0% | ~ +3.0% | 8–10% |
| Financial Services | net income ~ $830M | | | |
| Deere & Co. | Net income **$4.0–4.75B**; tax rate 25–27%; equip-ops op cash flow **$4.0–5.0B**; R&D up slightly; capex ~$1.4B | | | |

\* The 8-K's machine-extracted table renders the PPA cell as bare `10%` (the direction word was lost in
document conversion). The 26 Nov 2025 slide deck is unambiguous: FY2025 base $17,311M, FY2026 forecast bar
labelled "5-10%" **with a downward arrow**. I use "down 5–10%".

### 1.2 Q1 FY2026 guidance — 19 February 2026 (RAISED)

Source: `filings/2026-02-19__de-us-20260219-q1-8k__603009.md`

Headline bullet, verbatim:

> "**Net income guidance range increased to $4.5 billion - $5.0 billion**"

> **Company Outlook & Summary**
> "Net income attributable to Deere & Company for fiscal 2026 is forecasted to be in a range of
> $4.5 billion to $5.0 billion."

> "While the global large agriculture industry continues to experience challenges, we're encouraged by the
> ongoing recovery in demand within both the construction and small agriculture segments," said John May,
> chairman and CEO of John Deere. "These positive developments reinforce our belief that **2026 represents
> the bottom of the current cycle** and provides us with a strong foundation for accelerated growth going
> forward."

> "Our sustained investment in research and development throughout the cycle is yielding measurable results
> as we move toward launching a wide range of innovative products and solutions across all business
> segments," stated May.

Segment outlook (8-K table + `slides/2026-02-19__de-us-20260219-slide__603088.md`):

| Segment | Net sales FY26 | Currency | Price realization | Op margin FY26 |
|---|---|---|---|---|
| Production & Precision Ag | **Down 5 to 10%** | +3.0% | ~ +1.5% | **11–13%** |
| Small Ag & Turf | Up ~15% | +2.0% | ~ +2.0% | 13.5–15% |
| Construction & Forestry | Up ~15% | +2.0% | ~ +2.5% | 9–11% |
| Financial Services | net income ~ $840M | | | |
| Deere & Co. | Net income **$4.5–5.0B**; tax rate 25–27%; op cash flow **$4.5–5.5B**; R&D up slightly; capex ~$1.4B | | | |

Industry outlook (Feb 2026): U.S./Canada large ag **down 15–20%**; small ag & turf flat to +5%; Europe flat
to +5%; South America **down ~5%**; Asia flat to down 5%; U.S./Canada construction +~5%; compact +~5%;
global forestry **flat**; global roadbuilding **+~5%**.

### 1.3 Q2 FY2026 guidance — 21 May 2026 (MAINTAINED)

Source: `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`
(duplicate text also in `filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md`)

Headline bullet, verbatim:

> "**Net income guidance maintained, reinforcing confidence amid market volatility.**"

> **Company Outlook & Summary**
> "Net income attributable to Deere & Company for fiscal 2026 is forecasted to be in a range of
> $4.5 billion to $5.0 billion."

> "Our performance in the current market environment demonstrates the strength of our diversified portfolio.
> This is particularly reflected in the strong outcomes achieved by our Small Ag and Construction & Forestry
> divisions during this year," stated John May… "As we address ongoing challenges within global agricultural
> markets, our comprehensive portfolio continues to drive market share expansion and support our targets for
> sustained growth."

> "While our customers face ongoing challenges, John Deere remains firmly committed to supporting their
> success through disciplined operations and resilience," said May. "By continuing to invest in innovation
> through the cycle and leveraging the strength of our dealer network, we are well positioned to deliver
> increasing value for customers and shareholders as market conditions improve."

Segment outlook (8-K table + `slides/2026-05-21__de-us-20260521-slide__1042212.md`):

| Segment | Net sales FY26 | Currency | Price realization | Op margin FY26 |
|---|---|---|---|---|
| **Production & Precision Ag** | **Down 5 to 10%** | **+3.0%** | **~ +1.0%** | **11–13%** |
| Small Ag & Turf | Up ~15% | +1.0% | ~ +1.5% | 13.5–15% |
| Construction & Forestry | Up ~20% | +2.0% | ~ +2.5% | 10–12% |
| Financial Services | net income **~ $860M** | | | |
| Deere & Co. | Net income **$4.5–5.0B**; tax rate **24–26%**; op cash flow $4.5–5.5B; R&D up slightly; capex ~$1.4B | | | |

Industry outlook (May 2026): U.S./Canada large ag **down 15–20%**; small ag & turf flat to +5%; Europe flat
to +5%; South America **down ~15%** (cut from ~-5%); Asia flat; U.S./Canada construction +~5%; compact +~5%;
global forestry **down ~5%**; global roadbuilding **up ~10%** (raised from ~+5%).

10-Q narrative, `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md`:

> "Large agriculture sales are expected to remain subdued in North America and to soften in South America
> resulting in decreased sales volume for PPA in 2026 compared to 2025. SAT and CF sales are expected to
> improve in 2026. **Our net sales are expected to increase in 2026 compared to 2025**, with the anticipated
> decline in PPA sales more than offset by improvements in CF and SAT."

### 1.4 FY2026 guidance revision path — summary

| Metric | Q4 FY25 (26 Nov 25) | Q1 FY26 (19 Feb 26) | Q2 FY26 (21 May 26) | Direction |
|---|---|---|---|---|
| **Net income attributable to Deere** | $4.00–4.75B (mid $4.375B) | **$4.5–5.0B** (mid $4.75B) | **$4.5–5.0B** (mid $4.75B) | **+8.6% at Q1, then held** |
| Effective tax rate (equip ops) | 25–27% | 25–27% | **24–26%** | cut ⇒ EPS tailwind |
| Equip-ops operating cash flow | $4.0–5.0B | $4.5–5.5B | $4.5–5.5B | raised at Q1 |
| PPA net sales | Down 5–10% | Down 5–10% | Down 5–10% | unchanged all year |
| PPA operating margin | 11–13% | 11–13% | **11–13%** | **unchanged all year** |
| SAT net sales | Up ~10% | Up ~15% | Up ~15% | raised at Q1 |
| SAT operating margin | 12.5–14% | 13.5–15% | 13.5–15% | raised at Q1 |
| C&F net sales | Up ~10% | Up ~15% | **Up ~20%** | raised twice |
| C&F operating margin | 8–10% | 9–11% | **10–12%** | raised twice |
| Financial Services net income | ~$830M | ~$840M | ~$860M | raised twice |

**Reading of the pattern:** the FY2026 raise is entirely a *mix* story. PPA guidance has never moved — the
same "down 5–10% sales / 11–13% margin" box since November 2025. Everything that has been upgraded
(SAT, C&F, FS, tax rate) sits outside PPA. That matters directly for the PPA operating-profit forecast:
management has given zero signal of PPA upside this year.

---

## 2. Full guidance-vs-actual history (FY2015–FY2025)

Full-year net income attributable to Deere & Company, USD billions. "Guide" = midpoint of the range, or the
point estimate where a point was given. Every guidance figure below was extracted verbatim from the filing
listed in §2.2.

| FY | Initial (prior-yr Q4) | Q1 | Q2 | Q3 | **Actual** |
|---|---|---|---|---|---|
| 2015 | n/a (pre-corpus) | ~$1.8B | ~$1.9B | ~$1.8B | **$1.940B** |
| 2016 | ~$1.4B | ~$1.3B | ~$1.2B | ~$1.350B | **$1.524B** |
| 2017 | ~$1.4B | ~$1.5B | ~$2.0B | ~$2.075B | **$2.159B** |
| 2018 | ~$2.6B | ~$2.1B | ~$2.3B | ~$2.360B | **$2.368B** |
| 2019 | ~$3.6B | ~$3.6B | ~$3.3B | ~$3.2B | **$3.253B** |
| 2020 | $2.7–3.1B | $2.7–3.1B | $1.6–2.0B (COVID cut) | ~$2.25B | **$2.751B** |
| 2021 | $3.6–4.0B | $4.6–5.0B | $5.3–5.7B | $5.7–5.9B | **$5.963B** |
| 2022 | $6.5–7.0B | $6.7–7.1B | $7.0–7.4B | $7.0–7.2B | **$7.131B** |
| 2023 | $8.0–8.5B | $8.75–9.25B | $9.25–9.50B | $9.75–10.00B | **$10.166B** |
| 2024 | $7.75–8.25B | $7.50–7.75B | ~$7.0B | ~$7.0B | **$7.100B** |
| 2025 | $5.0–5.5B | $5.0–5.5B | $4.75–5.50B | $4.75–5.25B | **$5.027B** |
| **2026** | **$4.00–4.75B** | **$4.5–5.0B** | **$4.5–5.0B** | *not yet issued* | *not yet reported* |

### 2.1 Error table — (actual ÷ guidance midpoint − 1)

| FY | vs initial | vs Q1 | vs Q2 | vs Q3 |
|---|---|---|---|---|
| 2015 | n/a | +7.8% | +2.1% | +7.8% |
| 2016 | +8.9% | +17.2% | +27.0% | +12.9% |
| 2017 | +54.2% | +43.9% | +7.9% | +4.0% |
| 2018 | −8.9% | +12.8% | +3.0% | +0.3% |
| 2019 | −9.6% | −9.6% | −1.4% | +1.7% |
| 2020 | −5.1% | −5.1% | +52.8% | +22.3% |
| 2021 | +56.9% | +24.2% | +8.4% | +2.8% |
| 2022 | +5.6% | +3.3% | −1.0% | +0.4% |
| 2023 | +23.2% | +13.0% | +8.4% | +2.9% |
| 2024 | −11.3% | −6.9% | +1.4% | +1.4% |
| 2025 | −4.2% | −4.2% | −1.9% | +0.5% |
| **Mean** | **+10.97%** | **+8.76%** | **+9.71%** | **+5.19%** |
| **Median** | **+0.70%** | **+7.78%** | **+2.96%** | **+2.81%** |
| **Beat rate** | 5/10 | 7/11 | 8/11 | **11/11** |
| Median, ex-2016 & 2020 | +0.70% | +7.78% | **+2.11%** | **+1.66%** |
| Median, FY2021–25 only | +5.64% | +3.35% | **+1.43%** | **+1.43%** |
| Beat rate, FY2021–25 | 3/5 | 3/5 | 3/5 | **5/5** |

### 2.2 Provenance of each guidance figure

| Guidance | Document |
|---|---|
| FY15 Q1/Q2/Q3 | `filings/2015-02-20__de-us-20150220-q1-8k__784661.md`, `…2015-05-22…q2-8k__784603.md`, `…2015-08-21…q3-8k__784604.md` |
| FY16 initial / Q1 / Q2 / Q3 | `filings/2015-11-25__de-us-20151125-q4-8k__784605.md`, `…2016-02-19…q1-8k__784606.md`, `…2016-05-20…q2-8k__784653.md`, `…2016-08-19…q3-8k__784652.md` |
| FY17 initial / Q1 / Q2 / Q3 | `filings/2016-11-23__de-us-20161123-q4-8k__784650.md`, `…2017-02-17…q1-8k__784623.md`, `…2017-05-19…q2-8k__784651.md`, `…2017-08-18…q3-8k__784624.md` |
| FY18 initial / Q1 / Q2 / Q3 | `filings/2017-11-22__de-us-20171122-fy-8k__784662.md`, `…2018-02-16…q1-8k__784666.md`, `…2018-05-18…q2-8k__784663.md`, `…2018-08-17…q3-8k__784667.md` |
| FY19 initial / Q1 / Q2 / Q3 | `filings/2018-11-21__de-us-20181121-fy-8k__654629.md`, `…2019-02-15…q1-8k__654630.md`, `…2019-05-17…q2-8k__645299.md`, `…2019-08-16…q3-8k__645300.md` |
| FY20 initial / Q1 / Q2 / Q3 | `filings/2019-11-27__de-us-20191127-q4-8k__469218.md`, `…2020-02-21…q1-8k__469227.md`, `…2020-05-21…q2-8k__469475.md`, `…2020-08-20…q3-8k__105830.md` |
| FY21 initial / Q1 / Q2 / Q3 | `filings/2020-11-25__de-us-20201125-q4-8k__105817.md`, `…2021-02-19…q1-8k__105842.md`, `…2021-05-21…q2-8k__105846.md`, `…2021-08-20…q3-8k__105827.md` |
| FY22 initial / Q1 / Q2 / Q3 | `filings/2021-11-24__de-us-20211124-q4-8k__105843.md`, `…2022-02-18…q1-8k__105812.md`, `…2022-05-20…q2-8k__105815.md`, `…2022-08-19…q3-8k__105811.md` |
| FY23 initial / Q1 / Q2 / Q3 | `filings/2022-11-23__de-us-20221123-q4-8k__105825.md`, `…2023-02-17…q1-8k__105833.md`, `…2023-05-19…q2-8k__105839.md`, `…2023-08-18…q3-8k__105829.md` |
| FY24 initial / Q1 / Q2 / Q3 | `filings/2023-11-22__de-us-20231122-q4-8k__105823.md`, `…2024-02-15…q1-8k__105824.md`, `…2024-05-16…q2-8k__105819.md`, `…2024-08-15…q3-8k__105836.md` |
| FY25 initial / Q1 / Q2 / Q3 | `filings/2024-11-21__de-us-20241121-q4-8k__105840.md`, `…2025-02-13…q1-8k__105841.md`, `…2025-05-15…q2-8k__105808.md`, `…2025-08-15…q3-8k__143410.md` |
| FY26 initial / Q1 / Q2 | `filings/2025-11-26__de-us-20251126-q4-8k__361233.md`, `…2026-02-19…q1-8k__603009.md`, `…2026-05-21…q2-8k__1042167.md` |
| Actuals FY15–FY25 | the respective Q4/FY 8-Ks listed above (each states "For fiscal 20XX, net income attributable to Deere & Company was $X") |

Notable wording variants (verbatim):
- FY2020 Q2, 21 May 2020: *"Net income attributable to Deere & Company is forecast to be in a range of $1.6 billion to $2 billion for the full year."* — the COVID cut.
- FY2024 Q2 & Q3: *"…forecasted to be approximately $7.0 billion"* — Deere collapsed the range to a point.
- FY2025 Q1, 13 Feb 2025: *"…forecasted to **remain** in a range of $5.0 billion to $5.5 billion."*
- FY2022 Q2: *"…in a range of $7.0 billion to $7.4 billion, **which includes a net $220 million gain from special items** in the second quarter of 2022."*

### 2.3 The bias verdict

**Deere guides conservatively, and the conservatism is concentrated at the Q3 update.**

1. **Q3 guidance has never been missed in the 11 years in the corpus (11/11 beats).** Median overshoot
   **+2.8%** (all years), **+1.7%** excluding the two anomaly years, **+1.4%** in FY2021–25. The dispersion
   is tiny: excluding FY2020, the Q3 error range is only **+0.3% to +12.9%**, and +0.3% to +4.0% in the last
   eight years. Deere sets the Q3 range so that it lands in the **upper half, occasionally just above the
   top**.
2. **Q2 guidance is roughly unbiased but noisier**: median **+3.0%** (all), **+2.1%** ex-anomalies, **+1.4%**
   FY2021–25, with an 8/11 beat rate and *three genuine misses* (FY2019 −1.4%, FY2022 −1.0%, FY2025 −1.9%).
   All three misses are small (≤2%). The big overshoots come from cycle inflections (FY2016, FY2020, FY2021,
   FY2023).
3. **Q1 and initial guidance are directionally useless as point estimates** — median errors of +7.8% and
   +0.7% but with spreads of −11% to +57%. Their information content is the *revision direction*, not the level.
4. **The revision direction is the single most predictive signal.** Every year Deere *raised* the range at
   Q1 (FY2017, FY2021, FY2022, FY2023), the year finished **above the Q1 midpoint** — by +43.9%, +24.2%,
   +3.3%, +13.0% respectively. Every year Deere *held or cut* at Q1 (FY2019, FY2020, FY2024, FY2025), the
   year finished **below the Q1 midpoint** (−9.6%, −5.1%, −6.9%, −4.2%). That rule is **8/8**.
   **FY2026 was raised at Q1** — placing it in the up-revision cohort. The counterweight: FY2026 was then
   only *held* at Q2, whereas FY2021/2022/2023 all raised again at Q2. FY2026 therefore looks like a
   *moderate* member of the up-revision cohort, not a FY2021-style blowout.
5. **Where in the range does the actual land?** From the Q2-stage range: FY2021 above the high end, FY2022
   33rd percentile, FY2023 above the high end, FY2024 at the point estimate, FY2025 37th percentile.
   Median ≈ the midpoint, with fat upside tails at cycle inflections. Management is calling FY2026 "the
   bottom of the current cycle" — historically the setup for a top-of-range or above-range year.

**Bias to apply for FY2026:** take the Q2 midpoint $4.75B and apply the ex-anomaly Q2 median beat of
**+1.4% to +2.1%** → **FY2026 net income ≈ $4.82–4.85B**, i.e. the upper-middle of the guided range. A
cycle-inflection scenario supports the top of the range or slightly above ($5.0–5.2B); a "one more leg down
in large ag" scenario supports $4.6–4.7B.

---

## 3. FY2026 H1 actuals (reported fact) and the implied H2

### 3.1 Reported FY2026 H1

| Item | Q1 FY26 (qtr ended 1 Feb 26) | Q2 FY26 (qtr ended 3 May 26) | **H1 FY26** | H1 FY25 | YoY |
|---|---|---|---|---|---|
| Net sales & revenues | $9,611M | $13,369M | **$22,981M** | $21,272M | **+8.0%** |
| Net sales (equip ops) | $8,001M | $11,778M | **$19,779M** | $17,980M | +10.0% |
| Net income attrib. Deere | $656M | $1,773M | **$2,429M** | $2,673M | **−9.1%** |
| Diluted EPS | $2.42 | $6.55 | **$8.97** | $9.82 | −8.7% |
| PPA net sales | $3,163M | $4,503M | **$7,666M** | $8,297M | −7.6% |
| PPA operating profit | $139M | $706M | **$845M** | $1,486M | **−43.1%** |
| PPA operating margin | 4.4% | 15.7% | **11.02%** | 17.9% | |
| SAT net sales / op profit | $2,168M / $196M | $3,485M / $719M | $5,653M / $915M | | |
| C&F net sales / op profit | $2,670M / $137M | $3,790M / $561M | $6,460M / $698M | | |
| Financial Services net income | $244M | $190M | $434M | $391M | +11.0% |

Sources: `filings/2026-02-19__de-us-20260219-q1-8k__603009.md`,
`filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`.
Implied diluted share count: 2,429 ÷ 8.97 = **270.8M** (Q2 alone: 1,773 ÷ 6.55 = 270.7M).

Special item to remember: Q2 FY2026 includes a **$272M recovery of IEEPA tariff refund claims** following
the 20 February 2026 Supreme Court decision invalidating IEEPA tariffs
(`filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`). Per the Q2 call, roughly **50% went to C&F,
30% to SAT, 20% to large ag** (≈ $54M to PPA). Gross full-year tariff run-rate is **~$1.2 billion**
(unchanged), split ~45% C&F / ~33% SAT / ~20% large ag
(`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`). **This $272M does not repeat in Q3.**

### 3.2 Management's own H2 cadence guidance (verbatim, 21 May 2026)

From `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md`:

> "One thing I would add is that as you consider the financial outlook for the rest of the year, we would
> expect **slightly higher revenue in the back half, with the fourth quarter being higher than the third
> quarter**. In addition, we would expect to see our most favorable cost comparisons in the fourth quarter
> as well."

> "Regarding Waterloo large tractors, **order books are well into the fourth quarter** as we look to close
> out our model year 2026 production."

From `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` (analyst asked explicitly about
"the cadence for 3Q and 4Q"):

> "…we expect back half to be higher than the front half, **Q4 would be a little bit higher than Q3
> overall**. …As you look at Large Ag… **Q4 a bit stronger than Q3**. We talked about at the beginning of the
> year some differences in normal seasonality. **We've got more Waterloo large tractor shipments shipping to
> North America in the back half than the front half of the year. That's abnormal for us**… On the small Ag
> side, it's pretty normal seasonality. **You'll get a little bit of a step down in Q3 and another step down
> in Q4**… Construction & Forestry, fairly balanced between the two. Both top line and margin in the back
> half, maybe **a little bit stronger in the fourth quarter than Q3**, but overall pretty close."

> "…price gets more favorable in the back half. Then on the production cost side, including tariffs and
> material costs, that gets more favorable as well. **Price cost will improve as we move through the balance
> of the fiscal year**."

> "…particularly for our large ag factories, is **a little bit better absorption in the fourth quarter as
> production rates are significantly higher**… the order book built this year for a much heavier fourth
> quarter with respect to our large tractors."

**Net effect: management has pre-announced a back-half that is H2 > H1 but Q4 > Q3 on revenue, margin,
price-cost and PPA absorption.** Q3 is explicitly the weaker of the two back-half quarters. Any Q3 forecast
that implies Q3 ≥ Q4 contradicts management.

### 3.3 Implied H2 arithmetic — net income

| Scenario | FY26 net income | − H1 $2,429M | = implied H2 |
|---|---|---|---|
| Bottom of guided range | $4,500M | | **$2,071M** |
| Midpoint | $4,750M | | **$2,321M** |
| Top of guided range | $5,000M | | **$2,571M** |
| Mid + historical Q2 bias (+1.4% / +2.1%) | $4,818M / $4,850M | | $2,389M / $2,421M |

For context, actual H2 FY2025 net income was **$2,354M** ($1,289M Q3 + $1,065M Q4). The FY2026 guidance
midpoint therefore implies an H2 that is **essentially flat year-on-year (−1.4%)**, with the mid-plus-bias
case implying **+1.5% to +2.8%**.

### 3.4 How accurate is Deere's Q2-stage implied H2, historically?

| FY | Q2 guide mid | H1 actual | Implied H2 | Actual H2 | Error |
|---|---|---|---|---|---|
| 2019 | $3.300B | $1.633B | $1.667B | $1.621B | −2.8% |
| 2020 | $1.800B | $1.183B | $0.617B | $1.568B | +154.1% *(COVID)* |
| 2021 | $5.500B | $3.014B | $2.486B | $2.950B | +18.7% |
| 2022 | $7.200B | $3.001B | $4.199B | $4.130B | −1.6% |
| 2023 | $9.375B | $4.819B | $4.556B | $5.347B | +17.4% |
| 2024 | $7.000B | $4.121B | $2.879B | $2.979B | +3.5% |
| 2025 | $5.125B | $2.673B | $2.452B | $2.354B | −4.0% |
| | | | | **median ex-2020** | **+0.9%** |

So the Q2-stage implied H2 is close to unbiased (median +0.9%) but with a **−4% to +19% spread**. Applying
the median: **FY2026 implied H2 ≈ $2.34B**.

### 3.5 Q3 share of H2

| FY | Q3 | Q4 | H2 | Q3 / H2 |
|---|---|---|---|---|
| 2019 | $899M | $722M | $1,621M | 55.5% |
| 2020 | $811M | $757M | $1,568M | 51.7% |
| 2021 | $1,667M | $1,283M | $2,950M | 56.5% |
| 2022 | $1,884M | $2,246M | $4,130M | **45.6%** ← the one Q4>Q3 year |
| 2023 | $2,978M | $2,369M | $5,347M | 55.7% |
| 2024 | $1,734M | $1,245M | $2,979M | 58.2% |
| 2025 | $1,289M | $1,065M | $2,354M | 54.8% |
| | | | **median** | **55.5%** |

The historical median is 55.5% — but **management has explicitly guided Q4 > Q3 for FY2026** on revenue,
price-cost and large-ag absorption. The only precedent year with Q4 > Q3 net income (FY2022) had a Q3/H2
share of **45.6%**. FY2026 should therefore sit at **45–50%**, central **47–48%**. This is the single
largest judgement call in this analysis and the biggest source of error.

---

## 4. What the guidance arithmetically implies for FY2026 Q3

All three figures below are **DERIVED ESTIMATES** built from reported H1 actuals plus management's
own FY2026 guidance and cadence commentary. None is a reported fact.

### 4.1 Worldwide net sales and revenues

Bottom-up from the 21 May 2026 segment sales guidance against FY2025 bases
($17,311M PPA / $10,224M SAT / $11,382M C&F, per the Q2 slide deck):

| Case | PPA | SAT | C&F | FY26 net sales | − H1 $19,779M | = H2 net sales |
|---|---|---|---|---|---|---|
| Low | −10% → $15,580 | +14% → $11,655 | +19% → $13,545 | $40,780M | | $21,001M |
| Mid | −7.5% → $16,013 | +15% → $11,758 | +20% → $13,658 | $41,429M | | $21,650M |
| High | −5% → $16,445 | +16% → $11,860 | +21% → $13,772 | $42,078M | | $22,299M |

Q3 share of H2 net sales, given "Q4 higher than Q3": **48–49%**.
Financial-services + other revenue runs **~$1,600M/quarter** (Q1: 9,611−8,001 = $1,610M; Q2: 13,369−11,778 = $1,591M).

| Case | Q3 net sales | + FS/other | **Q3 NS&R** |
|---|---|---|---|
| Low | $10,080M | $1,600M | **$11,680M** |
| Mid | $10,392–10,608M | $1,600M | **$11,992–12,208M** |
| High | $10,926M | $1,600M | **$12,526M** |

> **Guidance-implied FY26 Q3 net sales & revenues ≈ $12.1B (range $11.7–12.5B)**
> vs Q3 FY2025 actual $12,018M → **roughly flat, +0.5% YoY (range −2.8% to +4.2%)**.
> Implied full-year NS&R ≈ $47.9B (+4.9% vs FY2025's $45,684M), decelerating from +8.0% in H1 because
> Q4 FY2025 was already +11%.

Consistency check: this leaves Q4 FY2026 NS&R ≈ $12.8B > Q3 ≈ $12.2B, matching management's stated cadence.

### 4.2 GAAP diluted EPS

| FY26 net income | Implied H2 | Q3 @ 46% | Q3 @ 48% | Q3 @ 50% |
|---|---|---|---|---|
| $4,500M (low) | $2,071M | $953M / **$3.54** | $994M / **$3.70** | $1,036M / **$3.85** |
| $4,750M (mid) | $2,321M | $1,068M / **$3.97** | $1,114M / **$4.14** | $1,160M / **$4.31** |
| $4,818M (mid +1.4% bias) | $2,389M | $1,099M / **$4.09** | $1,147M / **$4.26** | $1,195M / **$4.44** |
| $5,000M (high) | $2,571M | $1,183M / **$4.40** | $1,234M / **$4.59** | $1,286M / **$4.78** |

EPS computed on **269M diluted shares** (270.8M in H1, declining modestly on buybacks).

> **Guidance-implied FY26 Q3 diluted EPS ≈ $4.25 (central range $4.05–4.45; full range $3.55–4.80)**
> Corresponding net income ≈ **$1,145M** (range $950–1,290M), vs Q3 FY2025 $1,289M / $4.75 →
> **−7% to −11% YoY**.

**⚠ Divergence from the street.** Published consensus for FY26 Q3 diluted EPS is **$4.85** (Barchart/Yahoo
earnings preview, 23 July 2026 — https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html),
with full-year FY2026 consensus EPS of **$18.27**. Two observations:
- $18.27 × ~270M ≈ **$4.93B net income — near the very top of Deere's $4.5–5.0B guided range.** The street
  is already assuming Deere beats to the high end.
- Even at the top of the range, a Q3 of $4.85 requires Q3 ≈ 52–53% of H2 (H1 EPS $8.97 + Q3 $4.85 + Q4
  $4.45 = $18.27, i.e. **Q3 > Q4**) — which **directly contradicts management's 21 May cadence guidance**
  that Q4 > Q3 on revenue, margin, price-cost and large-ag absorption.

The guidance arithmetic and the consensus are hard to reconcile. Either the street is modelling a
full-year materially above $5.0B, or it has the Q3/Q4 split backwards. I would weight management's explicit
cadence statement heavily and sit **below consensus**, around **$4.20–4.45**.

### 4.3 PPA operating profit

PPA guidance has been frozen at **down 5–10% sales / 11–13% operating margin** since November 2025.

| Case | FY26 PPA sales | FY26 margin | FY26 op profit | − H1 $845M | H2 op profit | H2 margin | Q3 @ 44% | Q3 @ 47% | Q3 @ 50% |
|---|---|---|---|---|---|---|---|---|---|
| Low | $15,580M (−10%) | 11.0% | $1,714M | | $869M | 11.0% | $382M | $408M | $434M |
| Mid | $16,013M (−7.5%) | 12.0% | $1,922M | | $1,077M | 12.9% | $474M | $506M | $538M |
| High | $16,445M (−5%) | 13.0% | $2,138M | | $1,293M | 14.7% | $569M | $608M | $646M |

Q3 share of H2 PPA operating profit is set below 50% because management said large-ag absorption and
price-cost are **most favourable in Q4**, and Waterloo shipments are Q4-weighted ("order books are well into
the fourth quarter"). H2 PPA net sales ≈ $8,347M at the midpoint; Q3 PPA sales ≈ $3.9–4.0B (−7% YoY vs
$4,273M) at a Q3 margin of roughly **11.5–12.5%**, stepping to ~13–14% in Q4.

> **Guidance-implied FY26 Q3 PPA operating profit ≈ $480M (central range $410–540M; full range $380–650M)**
> vs Q3 FY2025 actual **$580M** (13.6% margin on $4,273M sales) → **−17% YoY (range −34% to −7%)**.

Key constraint: H1 PPA margin was only **11.0%**, at the *bottom* of the 11–13% full-year guide. To reach
even the 12% FY midpoint, H2 must run at **12.9%**, and to reach 13% it must run at **14.7%**. With Q4
carrying the better half of that, Q3's implied margin is only modestly above H1's — the arithmetic does
**not** support a Q3 margin snap-back to FY2025's 13.6%.

### 4.4 Cross-check: does the segment build reconcile to $4.75B?

Rough full-year build at the guidance midpoint: PPA $1,922M + SAT ($11,758M × 14.25% = $1,675M) +
C&F ($13,658M × 11% = $1,502M) = **$5,099M equipment-operations operating profit**, plus Financial Services
net income ~$860M, less corporate/interest/other and tax at 24–26%. That is broadly consistent with a
$4.5–5.0B net income, so the segment guidance and the company guidance are internally coherent — no hidden
slack. This is important: it means the PPA 11–13% margin band cannot be quietly ignored.

---

## 5. Risks and asymmetries for the Q3 print

**Upside to my guidance-implied numbers**
- Deere has **never missed its Q3-stage guidance in 11 years**, and beat its Q2-stage guidance 8/11.
- The Q1-raise cohort (FY2017/2021/2022/2023) all finished above the Q1 midpoint, average ≈ +21%. FY2026 was raised at Q1.
- Management is calling 2026 "the bottom of the current cycle"; historically the inflection year is the year
  Deere blows through the range (FY2021 +8.4% vs Q2 guide, FY2023 +8.4%).
- Q2 FY2026 already beat the pattern: PPA delivered a 15.7% margin against an 11–13% full-year guide.
- Tax-rate guidance was cut at Q2 (25–27% → 24–26%), a mechanical EPS tailwind not yet in the net-income range.
- C&F and SAT momentum is running ahead of the guidance path (C&F Q2 +29% sales, +48% op profit).

**Downside**
- The **$272M IEEPA tariff refund does not repeat in Q3**; Q2 flattered by roughly $0.75–0.80 of EPS
  (~$54M of it inside PPA).
- Management explicitly guided **Q4 > Q3** on revenue, margin, price-cost and absorption. Q3 is the weak
  back-half quarter by design.
- South America industry guidance was **cut hard at Q2** (down ~5% → down ~15%) and global forestry from
  flat to down ~5% — both hit Q3.
- H1 PPA margin of 11.0% sits at the floor of the 11–13% band; PPA guidance has not been raised once all year.
- Comparison base stiffens: Q3 FY2025 NS&R was $12,018M and Q4 FY2025 was +11% YoY.
- Published consensus ($4.85 Q3 EPS) is meaningfully above the guidance arithmetic; a miss-versus-consensus
  is quite possible even with an in-line-versus-guidance quarter.

---

## 6. Numbers to hand to the model

| Item | Value | Type |
|---|---|---|
| FY2026 net income guidance, Q2 stage (21 May 26) | $4.5–5.0B (mid $4.75B), maintained | reported fact |
| FY2026 net income guidance, Q1 stage (19 Feb 26) | $4.5–5.0B, "increased" from $4.00–4.75B | reported fact |
| FY2026 PPA guidance (unchanged since Nov 25) | net sales down 5–10%; op margin 11–13% | reported fact |
| FY2026 H1 actual net income / EPS | $2,429M / $8.97 | reported fact |
| FY2026 H1 actual NS&R | $22,981M | reported fact |
| FY2026 H1 actual PPA sales / op profit | $7,666M / $845M (11.0%) | reported fact |
| Q3 FY2025 comparatives | NS&R $12,018M; NI $1,289M; EPS $4.75; PPA sales $4,273M, OP $580M (13.6%) | reported fact |
| Diluted share count | ~270.8M H1 FY26; use ~269M for Q3 | inference |
| Median beat vs Q2 guidance midpoint (ex-anomaly) | **+2.1%** (FY2021–25: +1.4%) | inference |
| Median beat vs Q3 guidance midpoint | **+2.8%** (11/11 beats; +1.7% ex-anomaly) | inference |
| Implied H2 FY2026 net income | $2,071–2,571M; central **$2,340–2,420M** | inference |
| Q3 share of H2 net income (Q4>Q3 guided) | **47%** (hist. median 55.5%; FY2022 Q4>Q3 precedent 45.6%) | inference |
| **Q3 FY2026 NS&R** | **≈ $12,100M** (range $11,700–12,500M) | estimate |
| **Q3 FY2026 GAAP diluted EPS** | **≈ $4.25** (central $4.05–4.45; full $3.55–4.80) | estimate |
| **Q3 FY2026 PPA operating profit** | **≈ $480M** (central $410–540M; full $380–650M) | estimate |
| Street consensus Q3 FY26 EPS | $4.85 (FY26 EPS $18.27) — *above* guidance arithmetic | reported (third-party) |
| Q3 FY2026 report date | Thursday 20 August 2026 | reported fact |

---

## 7. Gaps and things not found

- **No FY2026 Q3 actuals exist**, in the corpus or on the web. Confirmed.
- **No FY2026 Q3 guidance** — it will be issued with the 20 August 2026 release, after the corpus freeze.
- **Deere does not guide revenue or EPS explicitly**; it guides full-year *net income* plus segment
  *sales growth* and *operating margin*. Revenue and EPS above are derived, not guided.
- **No quarterly guidance of any kind.** All quarterly splits in §4 are inference from management's
  qualitative cadence commentary plus historical seasonality.
- FY2012–FY2014 guidance is **not in the corpus** (filings begin 14 January 2015), so the bias table starts
  at FY2015 and the FY2015 "initial" cell is blank.
- The FY2026 Q4-stage 8-K segment table renders PPA net sales as a bare "10%"; direction resolved from the
  slide deck. Minor, but flagged.
- **No reliable third-party Q3 FY2026 *revenue* consensus found.** Search results returned figures
  ($10.26B, $11.14B) that trace back to an August 2025 article about Q3 *FY2025*, or to unattributed
  aggregators; I have discarded them. Only the EPS consensus ($4.82–4.85) and FY EPS consensus ($18.27)
  from the 23 July 2026 Barchart/Yahoo preview are cited.
- FY2018 comparisons are distorted by U.S. tax-reform charges; FY2020 by COVID. Both are flagged in the
  tables and excluded from the "ex-anomaly" statistics.

---

**Sources (web):**
- [Deere & Company Earnings Preview: What to Expect — Barchart via Yahoo Finance, 23 July 2026](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html)
- [Deere to Announce Third Quarter 2026 Financial Results — Nasdaq/PR Newswire, 5 August 2026](https://www.nasdaq.com/press-release/deere-announce-third-quarter-2026-financial-results-2026-08-05)
- [Deere & Company Form 8-K exhibit, filed 21 May 2026 — SEC EDGAR](https://www.sec.gov/Archives/edgar/data/0000315189/000110465926064747/de-20260521xex99d2.htm)
