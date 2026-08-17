# Deere & Company — Ag Equipment Cycle History and FY2026 Positioning

**Prepared:** 16 August 2026 | **Analyst role:** cycle-history
**Corpus:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere` (310 docs, frozen 14 Aug 2026)
**Purpose:** position FY2026 Q3 (May–Jul 2026, reports 20 Aug 2026) against 14 years of Deere cycle history.

---

## 0. Metadata trap — confirmed and resolved

The corpus `INDEX.md` lists:

> `| 2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call Transcript | call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md |`

**This is mislabelled Q2 FY2026 material.** I read the file in full. Evidence:

- Its first line is `"Our first question comes from Paddy Bogart from Melius Research"` — the exact sentence that **ends** the Q2 prepared-remarks file `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md`. The two files are one call, split into prepared remarks and Q&A.
- Its content discusses "the second quarter", the $272M Q2 IEEPA refund, and forward guidance for "3Q and 4Q" as *future* quarters.
- It is dated 21 May 2026, the Q2 earnings release date.

**There are no FY2026 Q3 actuals anywhere in the corpus or (as of 16 Aug 2026) in public sources.** Deere reports FY2026 Q3 on **20 August 2026** ([StockTitan, Aug 2026](https://www.stocktitan.net/news/DE/deere-to-announce-third-quarter-2026-financial-ws5vrthl5ifm.html)). Every FY2026 Q3 number in this document is an estimate or inference and is labelled as such.

---

## 1. Headline positioning

**Deere says FY2026 is the bottom of the ag cycle, and the fiscal-year that most closely rhymes with FY2026 in the prior downturn is FY2016 — the trough year of the 2013–2016 cycle.** But there is a critical structural difference: in 2016 *every* Deere segment was contracting, whereas in FY2026 only large ag (PPA) is down while Construction & Forestry (+~20%) and Small Ag & Turf (+~15%) are growing. Company revenue and EPS have therefore already inflected up; **PPA has not.**

| Question | Answer |
|---|---|
| What phase does Deere say it is in? | **Bottom.** "Our baseline view remains that 2026 will represent the bottom of the ag cycle" — CFO Brent Norwood, Q2 FY26 call, 21 May 2026 |
| Where within the cycle by segment? | "Large Ag is operating **below trough levels**, Small Ag & Turf is progressing towards **mid-cycle**, and Construction & Forestry is **slightly above mid-cycle**" — same call |
| When does recovery start? | "Our expectation still as a baseline… is that we see **recovery in 2027**" — Q2 FY26 Q&A |
| Prior-cycle analogue Deere itself uses | FY2025 margins were *"over 450 basis points better than 2016, the last time we were at this point in the cycle"* — Q4 FY25 call, 26 Nov 2025 |

---

## 2. Fiscal-year cycle chronology (REPORTED FACT unless noted)

| FY | Net sales & revenues ($M) | YoY | Diluted EPS (GAAP) | YoY | Cycle phase |
|---|---:|---:|---:|---:|---|
| 2013 | 37,795 | +5% | 9.09 | +15% | **Peak (cycle 1)** |
| 2014 | 36,067 | −5% | 8.63 | −5% | Downturn yr 1 |
| 2015 | 28,863 | −20% | 5.77 | −33% | Downturn yr 2 (steepest) |
| 2016 | 26,644 | −8% | 4.81 | −17% | **Trough (cycle 1)** |
| 2017 | 29,738 | +12% | 6.68 | +39% | Recovery yr 1 |
| 2018 | 37,358 | +26% | 7.24 | +8% | Recovery yr 2 (Wirtgen) |
| 2019 | 39,258 | +5% | 10.15 | +40% | Late expansion |
| 2020 | 35,540 | −9% | 8.69 | −14% | COVID air-pocket |
| 2021 | 44,024 | +24% | 18.99 | +119% | Upcycle yr 1 |
| 2022 | 52,577 | +19% | 23.28 | +23% | Upcycle yr 2 |
| 2023 | 61,251 | +16% | 34.63 | +49% | **Peak (cycle 2)** |
| 2024 | 51,716 | −16% | 25.62 | −26% | Downturn yr 1 |
| 2025 | 45,684 | −12% | 18.50 | −28% | Downturn yr 2 (revenue trough) |
| 2026E | ~47.6–48.5k *(inference, §7)* | ~+5% | ~16.7–18.6 *(guide-implied)* | ~−10% to 0% | **Company inflects up; PPA still bottoming** |

Sources: FY2013 — [Deere FY2013 Q4 release, 20 Nov 2013](https://www.sec.gov/Archives/edgar/data/0000315189/000110465913085905/a13-24518_1ex99d1.htm). FY2014–FY2015 — `filings/2015-11-25__de-us-20151125-q4-8k__784605.md`. FY2016–FY2025 — the corresponding Q4/FY 8-K in `filings/` (see §3–§5 quarterly tables for exact files). FY2026E — my arithmetic on the Q2 FY26 guide in `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`.

### Peak-to-trough magnitude, the two downturns side by side

| Metric | 2013→2016 downturn | 2023→2025/26 downturn |
|---|---|---|
| Peak FY revenue | $37,795M (FY2013) | $61,251M (FY2023) |
| Trough FY revenue | $26,644M (FY2016) | $45,684M (FY2025) |
| **FY revenue peak-to-trough** | **−29.5% over 3 fiscal years** | **−25.4% over 2 fiscal years** |
| Peak FY diluted EPS | $9.09 (FY2013) | $34.63 (FY2023) |
| Trough FY diluted EPS | $4.81 (FY2016) | $18.50 (FY2025); FY2026 guide-implied ~$17.7 |
| **FY EPS peak-to-trough** | **−47.1% over 3 years** | **−46.6% in 2 yrs; ~−49% by FY2026** |
| Peak *quarter* revenue | ~$10,930M (FY13 Q2, inferred) | $17,387M (FY23 Q2) |
| Trough *quarter* revenue | $5,525M (FY16 Q1) | $8,508M (FY25 Q1) |
| **Quarterly peak-to-trough** | **−49.5% over 11 quarters** | **−51.1% over 7 quarters** |
| Consecutive quarters of YoY revenue decline | **11** (FY14 Q2 → FY16 Q4) | **8** (FY23 Q4 → FY25 Q3) |
| Deepest single-quarter YoY revenue decline | −25% (FY15 Q4) | **−30% (FY25 Q1)** |

**Inference:** the current downturn is of *near-identical depth* to 2013–2016 but was compressed into roughly two-thirds the time. On an EPS basis the two are almost the same: ~−47% peak-to-trough both times.

---

## 3. Downturn 1 (FY2014–FY2016): quarterly path and management language

### Quarterly data

| Quarter | NSR ($M) | YoY | Diluted EPS | YoY |
|---|---:|---:|---:|---:|
| FY13 Q1 | ~7,430 † | +10% | — | — |
| FY13 Q2 | ~10,930 † | +9% | — | — |
| FY13 Q3 | ~10,000 † | +4% | — | — |
| FY13 Q4 | ~9,437 † | — | 2.11 | +21% |
| FY14 Q1 | 7,654 | +3% | 1.81 | +10% |
| FY14 Q2 | 9,948 | −9% | 2.65 | — |
| FY14 Q3 | 9,500 | −5% | 2.33 | — |
| FY14 Q4 | 8,965 | −5% | 1.83 | −13% |
| FY15 Q1 | 6,383 | −17% | 1.12 | −38% |
| FY15 Q2 | 8,171 | −18% | 2.03 | −23% |
| FY15 Q3 | 7,594 | −20% | 1.53 | −34% |
| FY15 Q4 | 6,715 | −25% | 1.08 | −41% |
| FY16 Q1 | **5,525** | −13% | 0.80 | −29% |
| FY16 Q2 | 7,875 | −4% | 1.56 | −23% |
| **FY16 Q3** | **6,724** | **−11%** | **1.55** | **+1%** ← first positive EPS comp |
| FY16 Q4 | 6,520 | −3% | 0.90 | −17% |
| FY17 Q1 | 5,625 | +2% | 0.61 | −24% |
| FY17 Q2 | 8,287 | +5% | 2.49 | +60% |
| FY17 Q3 | 7,808 | +16% | 1.97 | +27% |
| FY17 Q4 | 8,018 | +23% | 1.57 | +74% |

† FY2013 quarterly revenue is **MY INFERENCE**, back-solved from the YoY percentages quoted in the FY2014 quarterly calls (`call-transcripts/2014-02-12…-call-pres__1527290.md`, `2014-05-14…__1526775.md`, `2014-08-13…__1524329.md`, `2014-11-26…__1523103.md`). The four inferred quarters sum to $37,797M vs the reported FY2013 total of $37,795M, which validates the method. FY2015–FY2017 data: `filings/2015-*`–`filings/2017-*` quarterly 8-Ks.

### US & Canada large-ag industry guides through the downturn

| Fiscal year | Deere's US & Canada ag industry guide | Source |
|---|---|---|
| FY2014 | Down 5–10% | `call-transcripts/2013-11-20__de-us-20131120-call-pres__1527987.md` |
| FY2015 | **Down 25–30%** | `call-transcripts/2014-11-26__de-us-20141126-call-pres__1523103.md` |
| FY2016 | **Down 15–20%** | `filings/2015-11-25__de-us-20151125-q4-8k__784605.md` |
| FY2017 | Down 5–10% | `filings/2016-11-23__de-us-20161123-q4-8k__784650.md` |

### Management language, by cycle stage

**Stage 1 — Denial / "solid execution despite" (Nov 2013, FY2014 guide).** The peak had passed but the framing was mix and one-offs, not cycle:

> "we expect an industry decline of 5%-10%, mainly reflecting lower sales of large equipment such as high-horsepower tractors and combines… fiscal year 2014 Deere sales of worldwide Ag and Turf equipment are forecast to be down about 6%."
> — `call-transcripts/2013-11-20__de-us-20131120-call-pres__1527987.md`

**Stage 2 — Explicit acknowledgement plus aggressive self-help (Nov 2014, FY2015 guide).** The tell is the phrase "we moved aggressively" and the arrival of a resilience narrative:

> "we moved aggressively. We restrained costs, we reduced assets, and we realized the benefit of having a broad-based business line-up… there is no question John Deere faces challenging conditions in 2015… Our earnings forecast reflects the aggressive actions we are taking to control costs and assets and make deep cuts in factory production."
> — `call-transcripts/2014-11-26__de-us-20141126-call-pres__1523103.md`

**Stage 3 — Trough vocabulary (FY2015–FY2016).** Management begins naming the trough as a *planning scenario*, and talks about structural cost programs and decremental margins:

> "each of our units plan for the mid-cycle trough and peak scenarios… You will have noted our incremental margin performance in the last three years show how well we've executed in this downturn."
> — `call-transcripts/2016-08-19__de-us-20160819-call-qna__1481604.md`

> "changes to our variable pay structure, especially under **trough conditions**… Overall, our teams are making good progress towards the $500-plus million goal"
> — `call-transcripts/2016-11-23__de-us-20161123-call-pres-2__1480827.md`

> "when you think about where we are as a percent of mid-cycle in those products, you'd be at **50% or less** in some of those facilities."
> — `call-transcripts/2016-02-19__de-us-20160219-call-pres-2__1517041.md`

**Stage 4 — "Nearing bottom" (Nov 2016 → Feb 2017).** The exact turning-point formulation, and note the *test* they used: second derivative of the industry decline.

> "there are signs the large ag market is **nearing bottom**, as indicated by the fact that the decline expected in 2017 is less than we saw in 2016."
> — `call-transcripts/2016-11-23__de-us-20161123-call-pres-2__1480827.md`

> "we are seeing encouraging signs that after several years of steep declines, our key agricultural markets **may be stabilizing**… there are signs the large ag market is nearing bottom… Also, the used equipment environment is stabilizing. On the other hand, **used inventory for the industry remains above normal levels** and rental rates are still soft."
> — `call-transcripts/2017-02-17__de-us-20170217-call-pres-2__1480472.md`

**Stage 5 — Confirmed turn (May–Aug 2017).** Three named criteria — a smaller rate of decline, a supportive used market, and rising seasonal-product demand:

> "it does appear the large ag market is **stabilizing**. Signs supporting the stabilization include a considerably lower rate of industry sales decline in 2017 versus the past two years, a used equipment environment that is supportive of sales, and increased demand for spring seasonal products… **traditional farmer capital purchase patterns are returning now that used equipment inventories are approaching more traditional levels.**"
> — `call-transcripts/2017-08-18__de-us-20170818-call-pres-3__1478898.md`

Caution flag from the same era, useful for calibrating how noisy the turn is: in May 2017, with revenue already up 5% YoY, management said **"I would not say we've turned the corner"** (`call-transcripts/2017-05-19__de-us-20170519-call-qna__1479659.md`).

---

## 4. Upcycle FY2020–FY2023 (for amplitude reference)

| Quarter | NSR ($M) | YoY | Diluted EPS | PPA net sales ($M) | PPA op profit ($M) | PPA margin |
|---|---:|---:|---:|---:|---:|---:|
| FY21 Q1 | 9,112 | +19% | 3.87 | 3,069 | 643 | 21.0% |
| FY21 Q2 | 12,058 | +30% | 5.68 | 4,529 | 1,007 | 22.2% |
| FY21 Q3 | 11,527 | +29% | 5.32 | 4,250 | 906 | 21.3% |
| FY21 Q4 | 11,327 | +16% | 4.12 | 4,661 | 777 | 16.7% |
| FY22 Q1 | 9,569 | +5% | 2.92 | 3,356 | 296 | 8.8% |
| FY22 Q2 | 13,370 | +11% | 6.81 | 5,117 | 1,057 | 20.7% |
| FY22 Q3 | 14,102 | +22% | 6.16 | 6,096 | 1,293 | 21.2% |
| FY22 Q4 | 15,536 | +37% | 7.44 | 7,434 | 1,740 | 23.4% |
| FY23 Q1 | 12,652 | +32% | 6.55 | 5,198 | 1,208 | 23.2% |
| **FY23 Q2** | **17,387** | +30% | 9.65 | **7,822** | **2,170** | **27.7%** ← cycle peak |
| FY23 Q3 | 15,801 | +12% | 10.20 | 6,806 | 1,782 | 26.2% |
| FY23 Q4 | 15,412 | −1% | 8.26 | 6,965 | 1,836 | 26.4% |

Sources: the corresponding quarterly 8-Ks in `filings/` (e.g. `2023-05-19__de-us-20230519-q2-8k__105839.md`).

Cycle amplitude in EPS is the striking number: **$4.81 (FY2016) → $34.63 (FY2023) → ~$17.7 (FY2026E)**. Deere's own framing is that each cycle resets the floor higher — see §6.

---

## 5. Downturn 2 (FY2024–FY2026): quarterly path, and the PPA series

### Company level

| Quarter | NSR ($M) | YoY | Diluted EPS | YoY |
|---|---:|---:|---:|---:|
| FY23 Q4 | 15,412 | −1% | 8.26 | +11% |
| FY24 Q1 | 12,185 | −4% | 6.23 | −5% |
| FY24 Q2 | 15,235 | −12% | 8.53 | −12% |
| FY24 Q3 | 13,152 | −17% | 6.29 | −38% |
| FY24 Q4 | 11,143 | −28% | 4.55 | −45% |
| FY25 Q1 | **8,508** | **−30%** | 3.19 | −49% |
| FY25 Q2 | 12,763 | −16% | 6.64 | −22% |
| FY25 Q3 | 12,018 | −9% | 4.75 | −24% |
| FY25 Q4 | 12,394 | **+11%** | 3.93 | −14% |
| FY26 Q1 | 9,611 | **+13%** | 2.42 | −24% |
| FY26 Q2 | 13,369 | **+5%** | 6.55 | −1% |
| FY26 Q3 | *not yet reported* | — | — | — |

### Production & Precision Ag (the segment that is still in the downturn)

| Quarter | PPA net sales ($M) | YoY | PPA op profit ($M) | YoY | Margin |
|---|---:|---:|---:|---:|---:|
| FY23 Q2 (peak) | 7,822 | +53% | 2,170 | +105% | 27.7% |
| FY24 Q1 | 4,849 | −7% | 1,045 | −13% | 21.6% |
| FY24 Q2 | 6,581 | −16% | 1,650 | −24% | 25.1% |
| FY24 Q3 | 5,099 | −25% | 1,162 | −35% | 22.8% |
| FY24 Q4 | 4,305 | −38% | 657 | −64% | 15.3% |
| FY25 Q1 | 3,067 | −37% | 338 | −68% | 11.0% |
| FY25 Q2 | 5,230 | −21% | 1,148 | −30% | 22.0% |
| FY25 Q3 | 4,273 | −16% | 580 | −50% | 13.6% |
| FY25 Q4 | 4,740 | +10% | 604 | −8% | 12.7% |
| FY26 Q1 | 3,163 | +3% | **139** | −59% | **4.4%** ← lowest PPA margin on record |
| FY26 Q2 | 4,503 | −14% | 706 | −39% | 15.7% *(incl. ~$54M tariff refund)* |
| FY26 Q3 | *not yet reported* | — | — | — | — |

PPA fiscal-year operating profit: **FY2023 $6,996M → FY2024 $4,514M → FY2025 $2,671M → FY2026 guide 11–13% margin on sales down 5–10% ≈ $1,714–2,138M.** That is a **−69% to −76% peak-to-trough collapse in PPA operating profit over three years**, materially deeper than the company aggregate.

Sources: `filings/2024-11-21__de-us-20241121-q4-8k__105840.md`, `filings/2025-11-26__de-us-20251126-q4-8k__361233.md`, `filings/2026-02-19__de-us-20260219-q1-8k__603009.md`, `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md`.

### Management language, by cycle stage (this downturn)

**Stage 1 — the guide-down (Nov 2023).** No cycle language yet; framed as segment-level guidance:

> "we anticipate Production and Precision Ag net sales to be **down between 15% and 20%** in fiscal year 2024."
> — `call-transcripts/2023-11-22__de-us-20231122-call-pres__46470.md`

**Stage 2 — deep-cut / "controllables" phase (Aug 2025, the year-ago comparable quarter).** Note the tonal fingerprint: *uncertainty*, *lean factories*, *used inventory is priority one*.

> "Global uncertainty and difficult fundamentals continue to weigh on customer sentiment… we currently have **more uncertainty than ever in the North American ag market**, which translates to the broadest range of outcomes for a following year than we've had in a long time… Our focus and alignment with our dealers right now is on the **controllables. Priority number one is jointly addressing used inventory levels**… we will continue to run our factories lean… positions us well **as this cycle turns**."
> — `call-transcripts/2025-08-15__de-us-20250815-call-q3-pres__143406.md`

**Stage 3 — "below trough", "this coming year will mark the bottom" (Nov 2025).** This is the turning-point statement of the current cycle:

> "our implied midpoint guidance of approximately **$16 in earnings per share reflects sub-trough conditions in PPA**, with projected fiscal year 2026 sales at **less than 80% of mid-cycle levels**."
> "In a year where we saw industry declines in a majority of major markets that we serve, **placing the business below trough levels**… Even with the North American large Ag industry declining this year by around 30%, we delivered margins **over 450 basis points better than 2016, the last time we were at this point in the cycle**."
> "For large Ag in North America, while we see the industry declining in 2026, we also see a number of positive factors that lead us to believe **this coming year will mark the bottom of the cycle**."
> — `call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md`

**Stage 4 — bottom confirmed, recovery deferred to FY2027 (Feb and May 2026).**

> "The developments over the course of the past three months have **strengthened our belief that 2026 marks the bottom of the current cycle**, as we project mid-single-digit net sales growth for the equipment operations this fiscal year."
> — `call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md` (Q1 FY26)

> "we're still **below trough levels for production precision ag** overall, and North America below that… it's **not a bounce, it's not inflecting hard**. It's just… we're seeing some positive progress and momentum."
> — `call-transcripts/2026-02-19__de-us-20260219-call-qna__605077.md` (Q1 FY26 Q&A)

> "our business segments are performing at different points in the cycle. While **Large Ag is operating below trough levels**, Small Ag & Turf is progressing towards mid-cycle, and Construction & Forestry is slightly above mid-cycle… our baseline view remains that **2026 will represent the bottom of the ag cycle**."
> — `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` (Q2 FY26)

> "our expectation still as a baseline… is that we see **recovery in 2027**… everything we've seen thus far [in early order programs] would support our view that **2026 still marks the bottom of the ag cycle**."
> — `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` (Q2 FY26 Q&A — the mislabelled file)

**Language contrast worth noting.** In the 2016 trough Deere used *hedged, second-derivative* language ("signs the large ag market is nearing bottom"). In FY2026 the language is *declarative* ("2026 will represent the bottom"), reiterated across three consecutive calls (Nov 2025, Feb 2026, May 2026) and *strengthened* rather than walked back. That is a more confident posture than at the equivalent point in 2016.

---

## 6. Where FY2026 sits — the equivalent-stage comparison

### Mapping by industry-decline sequence (the cleanest alignment)

| Downturn 1 | US&C large-ag industry | | Downturn 2 | US&C large-ag industry |
|---|---|---|---|---|
| FY2014 | Down 5–10% | ≈ | FY2024 | Down ~15% |
| FY2015 | **Down 25–30%** | ≈ | FY2025 | **Down ~30%** |
| FY2016 (trough) | **Down 15–20%** | ≈ | **FY2026** | **Down 15–20%** |
| FY2017 (recovery yr 1) | Down 5–10%, then FY2018 +9% | ≈ | FY2027 (Deere's baseline recovery year) | — |

**The FY2026 industry guide (down 15–20%) is numerically identical to the FY2016 guide, and follows an equally severe ~30% down-year. FY2026 Q3 therefore maps most cleanly to FY2016 Q3 (reported 19 Aug 2016).**

### What happened at the equivalent quarter — FY2016 Q3

| FY2016 Q3 (19 Aug 2016) | Value |
|---|---|
| Net sales & revenues | $6,724M, **−11% YoY** |
| Diluted EPS | **$1.55 vs $1.53 — the first positive YoY EPS comparison of the entire downturn** |
| Driver | Cost/structural actions and easier comps, not volume |
| Management tone | Still cautious: "Low commodity prices, weakening farm incomes, and elevated used equipment levels" (`call-transcripts/2016-08-19__de-us-20160819-call-pres-2__1481603.md`) |

**Inference — the closest historical rhyme.** FY2026 Q2 already produced a near-flat EPS comp (−1%, $6.55 vs $6.64) with revenue *up* 5%. FY2026 Q3 is, on the FY2016 analogue, the quarter where the YoY EPS comparison plausibly flips positive for the first time in this downturn. Sell-side consensus for FY26 Q3 is $4.85 vs $4.75 a year ago — i.e. **+2.1%**, essentially the same shape as FY16 Q3's +1% ([Yahoo Finance earnings preview, Aug 2026](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html)).

### Where the analogy breaks — three material differences

1. **Segment breadth.** In FY2016 construction & forestry was *also* contracting ("the market demand for construction equipment continues to soften", Aug 2016). In FY2026, C&F is guided **up ~20%** and Small Ag & Turf **up ~15%**. Company revenue and EPS are therefore decoupled from the ag trough in a way they were not in 2016. Company-level FY2026 looks like a recovery year; PPA looks like 2016.
2. **Speed.** The current downturn took 8 quarters of YoY decline (vs 11) and 7 quarters peak-quarter to trough-quarter (vs 11) to fall a comparable ~50%. Deere reacted faster: field inventories of HHP tractors and combines are **down more than 50% from their mid-2024 peak**, versus 2016 when field inventory-to-sales ratios were merely held "in line with 2015 year-end levels".
3. **Structurally higher trough profitability, plus a tariff overlay.** Deere states FY2025 equipment-ops margins were **>450bp better than 2016** (>600bp excluding tariffs) at a comparable industry point. Offsetting that, FY2026 carries **~$1.2bn of direct tariff expense (~3 points of margin)**, an exposure with no 2016 analogue.

### The cyclical *decline* at the equivalent stage — magnitude and duration

| At the trough year (FY2016 vs FY2026) | FY2016 | FY2026 (guide/inference) |
|---|---|---|
| Years since peak revenue | 3 | 3 |
| Cumulative company revenue decline from peak | −29.5% | −21% (FY2026E ~48.0k vs 61.3k peak) |
| Cumulative GAAP EPS decline from peak | −47.1% | ~−49% |
| Company revenue YoY in trough year | −8% | **+5%** (differs) |
| Large-ag industry YoY, US&C | −15 to −20% | −15 to −20% (same) |
| Quarters of consecutive YoY revenue decline before the turn | 11 | 8 (already ended, FY25 Q4) |

---

## 7. Leading indicators — what the corpus says about each

### (a) Large-ag replacement demand and fleet age — **positive, slow-building**

| Evidence | Source |
|---|---|
| "the U.S. **fleet age is high and continues to get older** as customers put more hours on their equipment. With the stabilization that we're seeing in U.S. ag fundamentals, along with an improving used market, our expectation is that we'll start to see **some replacement demand return**." | `call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md` |
| "we are seeing a little bit of pickup from a replacement demand. **Not a massive inflection**… replacement does come back over time" | `call-transcripts/2026-02-19__de-us-20260219-call-qna__605077.md` |
| "**machine hours continue to accrue, aging out the fleet** and driving a base-level need for replacement" | `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` |
| "We're a couple of years into the downturn. We've seen less replacement. We're seeing age of fleets continue to grow… we're at **very elevated levels for high horsepower tractors. Very elevated levels in terms of fleet age for combines** as well." | `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` |
| **Prior-cycle analogue:** the turn was declared only once used normalised — "traditional farmer capital purchase patterns are returning **now that used equipment inventories are approaching more traditional levels**" (Aug 2017, four quarters *after* the FY2016 revenue trough) | `call-transcripts/2017-08-18__de-us-20170818-call-pres-3__1478898.md` |

### (b) Used inventory — **the governor, and it is clearing fast**

Q2 FY2026 (`call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md`), REPORTED FACT as stated by management:

| Category | Position at Q2 FY2026 |
|---|---|
| **New** field inventory, NA HHP tractors and combines | **Down >50% from mid-2024 peak**; inventory-to-sales ratios in line with historical averages |
| Used combines | Down **mid-teens %** from March 2024 peak |
| Used HHP tractors | Down **mid-teens %** from cycle peak; **down low single digits sequentially in Q2 — a quarter that normally builds** |
| Used model-year 2022–2023 8R tractors (the problem cohort) | **Down ~45% from peak levels a year ago** |
| Used sprayers | Down ~30% from recent peak |
| Used planters | Down ~50% from recent peak |
| John Deere Financial trade-wholesale portfolio (used on dealer lots) | **Down >15% YoY** |

Trajectory of the 8R cohort across three calls — a clean destocking curve:
- Nov 2025: "reduced by a mid-teens % in Q4 and is now **around 25% below the peak in March 2025**" (`call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md`)
- Feb 2026: "model year 2022, 2023, 8R's **down 20% sequentially in the quarter**" (`…2026-02-19…-call-qna__605077.md`)
- May 2026: "**down around 45%** from their peak levels last year" (`…2026-05-21…-call-pres__1042774.md`)

**Discrepancy flagged:** the Nov 2025 call described used combines as "nearly 25% decrease from their spring 2024 peak", while the May 2026 call says "down by mid-teens from their March 2024 peak". These are inconsistent in direction of travel. Likely a transcription/definition difference (Deere-branded vs all-brand, or a re-based peak). Treat the used-combine figure as low-confidence; the tractor, sprayer and planter figures are internally consistent.

**Prior-cycle comparison:** in 2016–2017 used inventory was described as *"elevated"* (Aug 2016) → *"stabilizing"* but *"above normal levels"* (Feb 2017) → *"has come down in the past quarter"* (May 2017) → *"approaching more traditional levels"* (Aug 2017). **Deere is currently at a materially better used-inventory position at the trough than it was in 2016**, and Deere itself attributes this to proactive pool-fund deployment beginning Q3 FY2025.

### (c) Farmer sentiment — **muted; the weakest of the three indicators**

| Evidence | Source |
|---|---|
| "**customer sentiment remains muted** despite recent grain price increases as growers' margins face headwinds from elevated and volatile input costs and high interest rates." | Q2 FY26 prepared remarks |
| Iran conflict → fuel and fertiliser inflation. "The situation in Iran is affecting **Brazilian growers at a particularly sensitive point**… Brazilians have more exposure to current spot prices." US/EU growers "largely purchased these inputs ahead of the spring planting season when costs were lower." | Q2 FY26 |
| South America industry guide **cut from down ~5% to down ~15%** during Q2 FY2026 — the single largest negative revision of the year | `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` |
| Offsetting positives: US corn and soybean prices "**up like 20%**" since August; RVO approved; House passed year-round E15; disaster-relief payment factors raised **35% → 70%**; US government farm support >$40bn in 2025; farmland values keeping debt ratios low | Q2 FY26 Q&A; Q4 FY25 call |
| Dealer sentiment **bifurcated**: "dealers who took action early on used… are most optimistic… we have a couple of dealers who are actually looking to **add** in select cases to their used fleet." | Q2 FY26 Q&A |
| **Prior-cycle analogue:** Nov 2014 — "crop receipts for 2015 are forecast to be down about 17% lower than 2012's crop receipt record"; Aug 2016 — "Low commodity prices, weakening farm incomes" | `2014-11-26…-call-pres__1523103.md`; `2016-08-19…-call-pres-2__1481603.md` |

### (d) External corroboration for the Q3 FY2026 window (May–Jul 2026) — post-corpus

| Indicator | Value | Source |
|---|---|---|
| US ag tractor unit sales, **July 2026** | **15,985 units, −10.9% YoY** (from 17,938) | [RFD-TV, Aug 2026](https://www.rfdtv.com/farm-equipment-sales-remain-weak-through-july-2026) |
| US 4WD tractors, July 2026 | **−38.7% YoY** | same |
| US tractors 100+ hp, YTD through July 2026 | **−15.5%** | same |
| US self-propelled combines, YTD through July 2026 | 1,676 units, **−10.2%** | same |
| US ag tractors, **June 2026** | **−18% YoY**; combines **+4% YoY** | [AEM June 2026 report via Yahoo Finance / DRG News, Jul 2026](https://drgnews.com/2026/07/23/u-s-and-canadian-sales-of-combines-see-slight-increase-in-june-2026/) |
| Canada tractors, July 2026 | −7.8%; but **100+hp 2WD +4.9% in July, +6.2% YTD** | RFD-TV, above |
| USDA 2026 net farm income forecast | **$153.4bn, −0.7% nominal / −2.6% real** vs 2025; net cash farm income $158.5bn, **+3.0%** | [USDA ERS Farm Income Forecast](https://www-tx.ers.usda.gov/topics/farm-economy/farm-sector-income-finances/highlights-from-the-farm-income-forecast) |

**Inference:** the AEM data through July 2026 is consistent with Deere's "large ag US&C down 15–20%" guide holding — no deterioration, no acceleration. The Canadian 100+hp 2WD figure turning positive, and US combines turning positive in June, are the first genuinely green data points in this indicator set and are consistent with a bottoming, not a recovery.

---

## 8. Guide-implied arithmetic for FY2026 Q3 (MY INFERENCE — not company guidance)

Deere does **not** guide quarterly. The following is arithmetic on the FY2026 full-year guide from the Q2 8-K and the explicit shaping comments on the Q2 call.

**Guide anchors (REPORTED FACT, `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` and the Q2 call):**
- FY26 net income attributable to Deere: **$4.5bn–$5.0bn** (unchanged)
- PPA net sales **down 5–10%**; PPA operating margin **11–13%**
- SAT net sales **up ~15%**; margin 13.5–15%
- C&F net sales **up ~20%**; margin 10–12%
- Financial Services net income **~$860M**; effective tax rate **24–26%**
- "we would expect **slightly higher revenue in the back half, with the fourth quarter being higher than the third quarter**… our **most favorable cost comparisons in the fourth quarter** as well" — CFO Norwood
- Large Ag: "**Q4 a bit stronger than Q3**… more Waterloo large tractor shipments shipping to North America in the back half… That's **abnormal** for us"
- Small Ag & Turf: "pretty normal seasonality… a little bit of a **step down in Q3 and another step down in Q4**"
- C&F: "fairly balanced between the two… maybe a little bit stronger in the fourth quarter"
- **The $272M IEEPA tariff refund is a Q2-only item** (~2.5 points of equipment-ops margin, ~$0.75/share after tax). It does not repeat in Q3.
- Price/cost improves in H2 (lapping H2-FY25 tariff onset and H2-FY25 incentives); better Waterloo overhead absorption in Q4

**FY2025 actual segment base (`filings/2025-11-26__de-us-20251126-q4-8k__361233.md`):** PPA $17,311M; SAT $10,224M; C&F $11,382M; FS revenues $5,821M; Other $946M; **Total $45,684M**. H1 FY2026 actual: $22,981M.

| Derived line | Range | Central |
|---|---|---|
| FY2026 total net sales & revenues | $47.6bn–$48.5bn | ~$48.0bn (+5%) |
| H2 FY2026 total NSR | $24.65bn–$25.50bn | ~$25.05bn |
| **FY26 Q3 total NSR** | **$12.05bn–$12.50bn** | **~$12.3bn (≈ +2% YoY vs $12,018M)** |
| FY26 Q4 total NSR | $12.6bn–$13.0bn | ~$12.75bn |
| FY2026 PPA operating profit (full year) | $1,714M–$2,138M | ~$1,920M |
| H2 FY2026 PPA operating profit (FY less H1 $845M) | $869M–$1,293M | ~$1,075M |
| **FY26 Q3 PPA operating profit** | **~$400M–$600M** | **~$490M** (vs $580M LY, ≈ −15%) |
| FY26 Q3 PPA net sales | ~$3.75bn–$4.20bn | ~$3.98bn (vs $4,273M LY, ≈ −7%) |
| H2 FY2026 net income (FY guide less H1 $2.429bn) | $2.07bn–$2.57bn | ~$2.32bn |
| **FY26 Q3 net income** (Q3 ≈ 45–49% of H2 given Q4 > Q3) | **$0.95bn–$1.24bn** | **~$1.10bn** |
| **FY26 Q3 diluted EPS** (at ~269M diluted shares) | **~$3.55–$4.60** | **~$4.10** |

**⚠ Tension worth flagging to the modelling team.** Sell-side consensus of **$4.85** for FY26 Q3 sits *above* the top of my guide-implied range. Reconciling them requires FY2026 net income of roughly **$5.1bn**, i.e. above the top of Deere's own $4.5–5.0bn guide. Either (a) consensus assumes the usual Deere conservatism and a Q4 guide-raise, (b) consensus assumes a Q3-weighted rather than Q4-weighted H2 despite management's explicit statement, or (c) the reported consensus figure is unreliable. Historically Q3 > Q4 for Deere (FY25: $4.75 vs $3.93; FY24: $6.29 vs $4.55; FY23: $10.20 vs $8.26) — **FY2026 is the first year in the series where management has explicitly said Q4 > Q3**, so anyone anchoring on normal seasonality will over-estimate Q3.

**Second flag:** Q2 FY2026's $6.55 EPS included ~$0.75/share of one-time IEEPA refund. Underlying Q2 EPS was ~$5.80. A naive sequential model off $6.55 will over-estimate Q3.

---

## 9. Not found / gaps

- **FY2013 quarterly net sales & revenues** are not in the corpus (filings begin Feb 2015; the FY2013 transcripts truncate the figures at the decimal point in this corpus's sentence splitting). I inferred them from FY2014 YoY percentages and validated against the reported FY2013 total. Searched: `filings/` (all), `call-transcripts/2013-*`, `call-transcripts/2014-*`.
- **FY2013/FY2014 quarterly diluted EPS for Q1–Q3 FY2013** — only Q4 FY2013 ($2.11) is in the corpus. FY2014 quarterly EPS is complete via the FY2015 8-K comparatives.
- **Segment-level PPA data before FY2021** does not exist — Deere reorganised from Agriculture & Turf / Construction & Forestry into PPA / SAT / C&F effective FY2021. No PPA series covers the 2013–2016 downturn. Any cross-cycle PPA comparison is therefore structurally impossible; use company-level and A&T-level series instead.
- **Deere's own quarterly guidance** — Deere stopped guiding quarterly revenue after ~FY2020. The Q3 estimates in §8 are derived, not given.
- **AEM YTD tractor unit counts are internally inconsistent** between the June report (103,123 YTD) and the July report (105,185 YTD, which implies only ~2,062 July units against a stated 15,985). Monthly YoY percentages are the reliable series; treat YTD unit levels with caution.
- **No FY2026 Q3 actuals exist.** Confirmed by document-level inspection of every 2026-dated file in the corpus and by the fact that Deere's Q3 FY2026 release is scheduled for 20 August 2026, four days after this analysis.

---

## 10. Source index

**Corpus (relative to `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`):**

| File | Used for |
|---|---|
| `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` | Q2 FY26 results, FY26 segment guide, industry outlook |
| `filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md` | Q2 FY26 segment tables (duplicate exhibit) |
| `filings/2026-02-19__de-us-20260219-q1-8k__603009.md` | Q1 FY26 results, raised guide to $4.5–5.0bn |
| `filings/2025-11-26__de-us-20251126-q4-8k__361233.md` | FY2025 full-year segment actuals |
| `filings/2025-08-15__de-us-20250815-q3-8k__143410.md` | FY25 Q3 (the year-ago comparable) |
| `filings/2024-11-21…`, `2024-08-15…`, `2024-05-16…`, `2024-02-15…` 8-Ks | FY2024 quarterly series |
| `filings/2021-*` through `2023-*` quarterly 8-Ks | PPA series and upcycle |
| `filings/2015-11-25__de-us-20151125-q4-8k__784605.md` | FY2014/FY2015 full-year, FY2016 industry guide |
| `filings/2016-11-23__de-us-20161123-q4-8k__784650.md` | FY2016 actuals, FY2017 industry guide |
| `filings/2015-*` and `2016-*` and `2017-*` quarterly 8-Ks | Downturn-1 quarterly revenue and EPS |
| `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` | Q2 FY26 prepared remarks — cycle phase, inventory, H2 shaping |
| `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` | Q2 FY26 Q&A (**mislabelled "Q3 2026" in INDEX.md**) — tariffs, EOPs, dealers |
| `call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md` / `…-call-qna__605077.md` | Q1 FY26 — "2026 marks the bottom" |
| `call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md` | FY25 Q4 — "below trough levels", 450bp vs 2016, $16 EPS midpoint |
| `call-transcripts/2025-08-15__de-us-20250815-call-q3-pres__143406.md` | FY25 Q3 — used-inventory pool funds, "as this cycle turns" |
| `call-transcripts/2023-11-22__de-us-20231122-call-pres__46470.md` | FY24 guide-down |
| `call-transcripts/2017-08-18__de-us-20170818-call-pres-3__1478898.md` | Confirmed-turn language, 2017 |
| `call-transcripts/2017-05-19__de-us-20170519-call-qna__1479659.md` | "I would not say we've turned the corner" |
| `call-transcripts/2017-02-17__de-us-20170217-call-pres-2__1480472.md` | "nearing bottom", used inventory still above normal |
| `call-transcripts/2016-11-23__de-us-20161123-call-pres-2__1480827.md` | "nearing bottom" formulation, trough cost programme |
| `call-transcripts/2016-08-19__de-us-20160819-call-pres-2__1481603.md` / `…-call-qna__1481604.md` | Equivalent-stage quarter, trough planning |
| `call-transcripts/2016-02-19__de-us-20160219-call-pres-2__1517041.md` | "50% or less of mid-cycle" |
| `call-transcripts/2015-11-25__de-us-20151125-call-pres-2__1515778.md` | FY2016 guide, "further weakness" |
| `call-transcripts/2014-11-26__de-us-20141126-call-pres__1523103.md` | FY2015 guide, "down 25–30%", "no question… challenging conditions" |
| `call-transcripts/2013-11-20__de-us-20131120-call-pres__1527987.md` | FY2014 guide, downturn onset |

**Web (accessed 16 August 2026):**

- [Deere FY2013 Q4 earnings release, SEC EDGAR, 20 Nov 2013](https://www.sec.gov/Archives/edgar/data/0000315189/000110465913085905/a13-24518_1ex99d1.htm) — FY2013 $37.795bn / $9.09
- [Deere to Announce Third Quarter 2026 Financial Results — StockTitan, Aug 2026](https://www.stocktitan.net/news/DE/deere-to-announce-third-quarter-2026-financial-ws5vrthl5ifm.html) — Q3 FY26 reports 20 Aug 2026
- [Deere & Company Earnings Preview — Yahoo Finance, Aug 2026](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html) — consensus Q3 EPS $4.85; FY26 $18.27
- [Farm Equipment Sales Remain Weak Through July 2026 — RFD-TV, Aug 2026](https://www.rfdtv.com/farm-equipment-sales-remain-weak-through-july-2026) — AEM July 2026 US/Canada tractor and combine data
- [U.S. and Canadian Sales of Combines See Slight Increase in June 2026 — DRG News, 23 Jul 2026](https://drgnews.com/2026/07/23/u-s-and-canadian-sales-of-combines-see-slight-increase-in-june-2026/) — AEM June 2026 data
- [USDA ERS, Highlights from the Farm Income Forecast](https://www-tx.ers.usda.gov/topics/farm-economy/farm-sector-income-finances/highlights-from-the-farm-income-forecast) — 2026 net farm income $153.4bn
- [AEM US Ag Tractor and Combine Reports](https://www.aem.org/market-share-statistics/us-ag-tractor-and-combine-reports) — primary AEM index page
