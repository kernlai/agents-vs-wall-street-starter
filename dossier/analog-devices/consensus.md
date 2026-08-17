# Analog Devices (ADI) — FY2026 Q3 consensus & post-freeze news dossier

Prepared 16 August 2026. Corpus freeze 14 August 2026.
Target period: **fiscal Q3 2026, the three months ending Saturday 1 August 2026** (FY end ~31 Oct 2026).
Target metrics: Revenue (USDm) · Adjusted diluted EPS (USD/share) · Adjusted gross margin (%).

> **NOT YET REPORTED.** ADI has not published Q3 FY2026 results as of 16 Aug 2026. Anything that looks
> like a Q3 FY2026 "actual" is a mislabelled document — see the "Corpus and web defects" section at the
> bottom, which lists two concrete traps I hit while researching this.

---

## 1. Confirmed report date and time — REPORTED FACT

**Wednesday, 19 August 2026.** Press release at **07:00 ET**; conference call at **10:00 ET**
(webcast at investor.analog.com). Speakers: Vincent Roche (CEO & Chair), Richard Puccio (EVP & CFO),
Jeff Ambrosi (Head of IR).

- Company announcement, 23 July 2026: https://investor.analog.com/news-releases/news-release-details/analog-devices-report-third-quarter-fiscal-year-2026-financial
- Morningstar/PR Newswire mirror, 23 July 2026: https://www.morningstar.com/news/pr-newswire/20260723ne10537/analog-devices-to-report-third-quarter-fiscal-year-2026-financial-results-on-wednesday-august-19-2026
- StockTitan, 23 July 2026: https://www.stocktitan.net/news/ADI/analog-devices-to-report-third-quarter-fiscal-year-2026-financial-w62xxxgy6eag.html

That is **three days after today**, i.e. the print lands before any further material news window.

---

## 2. THE ANCHOR — Q3 FY2026 guidance, verbatim — REPORTED FACT

Issued with the Q2 FY2026 results on **20 May 2026** (8-K Ex-99.1):

> "For the third quarter of fiscal 2026, we are forecasting revenue of **$3.9 billion, +/- $100 million**.
> At the midpoint of this revenue outlook, we expect reported operating margin of approximately
> **39.0%, +/-150 bps**, and adjusted operating margin of approximately **49.0%, +/-100 bps**.
> We are planning for reported EPS to be **$2.60, +/-$0.15**, and adjusted EPS to be **$3.30, +/-$0.15**."

Source (corpus): `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/filings/2026-05-20__adi-us-20260520-q2-8k__1040581.md` (line 71)
Original: https://www.sec.gov/Archives/edgar/data/6281/000000628126000050/adi2q26exhibit991earnings.htm

CFO Puccio restated it on the call and added the **tax rate** input:

> "Revenue is expected to be $3.9 billion, +-$100 million. Operating margin at the midpoint is expected
> to be 49%, +-100 basis points. … Our tax rate is expected to be **12%-14%**, and based on these inputs,
> adjusted EPS is expected to be $3.30, +-$0.15."

Source: `.../call-transcripts/2026-05-20__adi-us-20260520-call-pres__1041157.md` (lines 44, 47)

### 2a. Gross margin — ADI does NOT guide GM explicitly, but gave a number in Q&A — REPORTED FACT

This is the single most useful line in the whole corpus for the GM metric. Asked directly what is implied
for fiscal Q3 gross margin, Puccio answered:

> "Obviously, starting with the 73% gross margin, which was even a little higher than we expected based on
> some better mix and utilization. As I mentioned, the pricing impact was pretty much as expected.
> **For Q3, we are assuming about a 50 basis points decline in gross margin**, largely driven by the absence
> of that one-time benefit we got from repricing the channel during the prior quarter, obviously. From a mix
> perspective, we do expect it's likely to be a **slight tailwind** based on our outlook. While, as I mentioned
> previously, **utilization is expected to be fairly neutral**, … we don't see a ton of future upside on gross
> margin from utilization given where we're running the factories today."

Source: `.../call-transcripts/2026-05-20__adi-us-20260520-call-qna__1041159.md` (line 61)

→ **Company-implied Q3 FY2026 adjusted gross margin ≈ 72.5%** (73.0% − 50 bps).

Follow-up exchange (line 83) confirms management treats this as a near-term ceiling: asked whether ~72.5%
is "the local peak on gross margins … on the current revenue trajectory," Puccio: *"Yeah, I actually think
that's the right way to think about it… any more significant mix shift from a growth perspective could
change that."* The caveat matters: revenue above the high end has, in practice, come with mix upside.

**Basis warning.** ADI's adjusted GM excludes acquisition-related amortisation (Linear, Maxim, and now
Empower). The gap is very wide: Q2 FY2026 GAAP GM was **67.3%** vs adjusted **73.0%** (570 bps).
The target metric is the **adjusted** figure (~72–74% range). A number near 67–68% is the GAAP line.

---

## 3. Last reported quarter — Q2 FY2026 (ended 2 May 2026) — REPORTED FACT

| Metric | Q2 FY26 | Q2 FY25 | Change |
|---|---|---|---|
| Revenue | **$3,623m** | $2,640m | +37% |
| GAAP gross margin % | 67.3% | 61.0% | +630 bps |
| **Adjusted gross margin %** | **73.0%** | 69.4% | +360 bps |
| Adjusted operating margin | 49.0% | 41.2% | +780 bps |
| GAAP diluted EPS | $2.40 | $1.14 | +111% |
| **Adjusted diluted EPS** | **$3.09** | $1.85 | +67% |
| Tax rate (adj) | 11.8% | — | — |
| Adjusted OpEx | $872m (24.1% of rev) | — | — |

Revenue and EPS were **above the high end** of guidance ($3.5bn ± $0.1bn; $2.88 ± $0.15).
Source: `.../filings/2026-05-20__adi-us-20260520-q2-8k__1040581.md`

Q2 end-market mix (from the call, line 39/41):
- **Industrial 50%** of revenue, +20% q/q, +56% y/y — led by aerospace & defense, ATE, ETM, broad market.
- **Automotive 24%**, +8% q/q, +2% y/y; BMS for EVs back to y/y growth for the first time in two years.
- **Communications 15%**, +22% q/q, **+79% y/y**; data center is now **>75% of comms**, +>90% y/y
  (optical *and* power roughly equally); wireless +>35% y/y.
- **Consumer 11%**, flat q/q, +23% y/y.

---

## 4. PRIOR-YEAR ACTUALS — the validation baseline — REPORTED FACT

Q3 FY2025, quarter ended 2 August 2025, reported 20 August 2025:

| Metric | Q3 FY2025 |
|---|---|
| Revenue | **$2,880m** |
| GAAP gross margin % | 62.1% |
| **Adjusted gross margin %** | **69.2%** |
| Adjusted operating margin | 42.2% |
| GAAP diluted EPS | $1.04 |
| **Adjusted diluted EPS** | **$2.05** |

Source: `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/filings/2025-08-20__adi-us-20250820-q3-8k__155976.md`

Cross-check on the consensus growth rates: $2,880m × 1.363 = $3,926m (Zacks' "+36.3%" → $3.92bn ✓);
$2.05 × 1.624 = $3.33 (Zacks' "+62.4%" ✓). The consensus figures below are internally consistent with
these prior-year bases.

**Full recent sequence (all adjusted, corpus-sourced):**

| Quarter | Revenue | Adj GM % | Adj OM % | Adj EPS |
|---|---|---|---|---|
| Q3 FY25 (Aug-25) | $2,880m | 69.2% | 42.2% | $2.05 |
| Q4 FY25 (Nov-25) | $3,076m | 69.8% | 43.5% | $2.26 |
| FY2025 total | $11,020m | 69.3% | 41.9% | $7.79 |
| Q1 FY26 (Feb-26) | $3,160m | 71.2% | 45.5% | $2.46 |
| Q2 FY26 (May-26) | $3,623m | 73.0% | 49.0% | $3.09 |
| **Q3 FY26 (guide)** | **$3,900m ±100** | **~72.5% (implied)** | **49.0% ±100bps** | **$3.30 ±0.15** |

---

## 5. SELL-SIDE CONSENSUS — the scoring benchmark

### Revenue

| Source | Estimate | Date | Note |
|---|---|---|---|
| **Zacks Consensus** | **$3.92bn** (+36.3% y/y) | 14 Aug 2026 | Zacks preview "Should You Buy, Sell or Hold ADI Stock Before Q3 Earnings?" |
| **Benzinga / MarketBeat aggregate** | **$3.93bn** | ~11–13 Aug 2026 | "Analysts expect ADI to report $3.33 EPS and $3.93B revenue" |
| Company guidance midpoint | $3.90bn | 20 May 2026 | Not a consensus, but the gravity well |

**Spread: $3.92bn – $3.93bn.** Very tight. Consensus sits ~0.5–0.8% above the guidance midpoint —
the normal sell-side habit of modelling a small beat. **Use $3,925m as the consensus point.**

- Zacks (Globe & Mail mirror, 14 Aug 2026): https://www.theglobeandmail.com/investing/markets/stocks/ADI/pressreleases/3853356/should-you-buy-sell-or-hold-adi-stock-before-q3-earnings/
- Zacks (TradingView mirror): https://www.tradingview.com/news/zacks:cd40d67ee094b:0-should-you-buy-sell-or-hold-adi-stock-before-q3-earnings/
- Benzinga, Aug 2026: https://www.benzinga.com/trading-ideas/dividends/26/08/61205809/how-to-earn-500-a-month-from-analog-devices-stock-ahead-of-q3-earnings

### Adjusted diluted EPS

| Source | Estimate | Date |
|---|---|---|
| **Zacks Consensus** | **$3.33** (+62.4% y/y) | 14 Aug 2026 |
| Zacks "Most Accurate Estimate" | $3.41 | 14 Aug 2026 (Earnings ESP +2.37%) |
| Benzinga / MarketBeat aggregate | $3.33 | ~11–13 Aug 2026 |
| Barchart (consensus of 31 analysts) | $3.33 | 24 July 2026 |
| Company guidance midpoint | $3.30 ±0.15 | 20 May 2026 |

**Consensus is unusually well-corroborated at $3.33** across three independent aggregators and three
separate dates. The buy-side/whisper number is nearer **$3.41** (Zacks' Most Accurate, i.e. the most
recently-revised estimates).

- Barchart preview, 24 July 2026: https://www.barchart.com/story/news/3446493/here-s-what-to-expect-from-analog-devices-next-earnings-report

### Adjusted gross margin (%)

**No published sell-side GM consensus number could be found.** Aggregators (Zacks, MarketBeat, Barchart,
StockAnalysis, Simply Wall St) publish revenue/EPS only; the GM consensus lives behind Visible Alpha /
StreetAccount paywalls, which I could not reach.

**Best available proxies, in descending order of reliability:**

1. **Management's own stated Q3 assumption: ~72.5%** (73.0% less "about a 50 basis points decline").
   Sell-side models are built off this sentence, so the street GM consensus is almost certainly
   **72.4%–72.6%**. **Use 72.5% as the consensus point.**
2. **Bottom-up from the guided operating margin.** Adj OM guided at 49.0% on $3.9bn ⇒ adj operating
   income $1,911m. Q2 adj OpEx was $872m; ADI's OpEx scales with revenue and variable comp, so Q3 OpEx
   of ~$900–940m implies adj GM of 72.1%–73.1%. Midpoint ≈ 72.6%. Consistent with (1).
3. Trajectory: 69.2% → 69.8% → 71.2% → 73.0%. Four straight quarters of expansion; management is
   explicitly calling a pause, not a reversal.

### Full-year consensus (context / cross-check)

| Metric | FY2026 consensus | FY2027 consensus | Source |
|---|---|---|---|
| Revenue | $14.81bn (+34.4%) | — | StockAnalysis, 28 analysts, 14 Aug 2026 |
| Adjusted EPS | $12.42–12.43 (+59%) | $14.63 (+17.8%) | Barchart 24 Jul 2026 / StockAnalysis 14 Aug 2026 |

Cross-check: FY26 revenue $14.81bn − Q1 $3.160bn − Q2 $3.623bn − Q3 cons $3.925bn ⇒ **Q4 FY26 consensus
≈ $4.10bn** (+~4–5% q/q, vs management's reminder that "the fourth quarter for us is usually up in the low
single digits"). FY26 EPS $12.43 − $2.46 − $3.09 − $3.33 ⇒ **Q4 adj EPS ≈ $3.55**. Both internally coherent.
Useful mainly because a Q4 guide well above $4.1bn / $3.55 is what the market will trade on, not the Q3 print.

- StockAnalysis forecast page: https://stockanalysis.com/stocks/adi/forecast/

---

## 6. Guidance updates, pre-announcements, trading statements since the freeze — NONE FOUND

- **No** ADI guidance update, pre-announcement, profit warning or trading statement between 20 May 2026
  and 16 August 2026. The only company press releases in the window are the Empower closing (7 Jul) and
  the earnings-date notice (23 Jul).
- **No** 8-K with revised outlook on EDGAR in the window.
- **No** post-freeze (14–16 Aug 2026) material news. The 14 Aug Zacks preview is the last substantive item.

### The one real corporate event inside the quarter — REPORTED FACT

**ADI completed its acquisition of Empower Semiconductor on 7 July 2026 for $1.5bn all-cash.**
Empower makes integrated voltage regulators (IVR) and silicon capacitors for AI processor power delivery;
ADI frames it as making it a "grid-to-core" power partner for the AI ecosystem.

- https://investor.analog.com/news-releases/news-release-details/analog-devices-completes-acquisition-empower-semiconductor
- https://www.prnewswire.com/news-releases/analog-devices-completes-acquisition-of-empower-semiconductor-302819437.html (7 Jul 2026)
- https://evertiq.com/news/2026-07-08-analog-devices-completes-acquisition-of-empower-semiconductor

**Why this matters for the three target metrics (INFERENCE):**
- It closed on 7 July, i.e. **~26 days inside** a quarter that ended 1 August — roughly 28% of the period.
- Empower is a private, pre-scale company. Revenue contribution is immaterial (low single-digit $m).
  It does **not** meaningfully move the $3.9bn revenue line.
- It was **not** in the 20 May guidance. Its purchase-price amortisation is excluded from adjusted figures,
  but its **operating expenses are not**, and $1.5bn of cash out raises net non-operating expense.
  Net effect on Q3 adjusted EPS: a small drag, order of **$0.02–0.04**. Small enough to be inside noise,
  but it argues against assuming the *full* historical EPS beat repeats.
- Empower's product line is early-stage and likely below corporate gross margin; at its scale the GM
  effect is <10 bps. Ignore for GM.

### Announced price increase — REPORTED FACT, but lands AFTER the quarter

A broad ADI price increase takes effect **13 September 2026** — i.e. in Q4 FY2026, not Q3.
It is evidence of a tight supply/strong-demand environment but has **zero** effect on the Q3 print.
Source: https://www.aetrixelec.com/blog/analog-devices-price-increase-september-2026 (distributor notice)

---

## 7. ADI's record vs its own guidance and vs consensus — REPORTED FACT

ADI has landed **above the midpoint every quarter** in the recent run, and above the high end twice.

| Quarter | Rev guide mid | Rev actual | Beat | EPS guide mid | EPS actual | Beat |
|---|---|---|---|---|---|---|
| Q3 FY25 | $2,750m | $2,880m | **+4.7%** | $1.92 | $2.05 | +$0.13 |
| Q4 FY25 | $3,000m | $3,076m | **+2.5%** | $2.22 | $2.26 | +$0.04 |
| Q1 FY26 | $3,100m | $3,160m | **+1.9%** | $2.29 | $2.46 | +$0.17 |
| Q2 FY26 | $3,500m | $3,623m | **+3.5%** | $2.88 | $3.09 | +$0.21 |
| **Mean** | | | **+3.2%** | | | **+$0.14** |

Guidance sources: `.../filings/2025-05-22__adi-us-20250522-q2-8k__102679.md`,
`.../filings/2025-08-20__adi-us-20250820-q3-8k__155976.md`,
`.../filings/2025-11-25__adi-us-20251125-q4-8k__361005.md`,
`.../filings/2026-02-18__adi-us-20260218-q1-8k-2__602115.md`.

Zacks: ADI "beat the Zacks Consensus Estimate in each of the trailing four quarters, with an
**average surprise of 5.48%**" (EPS basis).

**Applying the mean beat mechanically:** revenue $3,900m × 1.032 = **$4,025m**; EPS $3.30 + $0.14 = **$3.44**.
Note the +3.2% mean revenue beat maps to $4,025m, which is **above the top of the guided band** ($4,000m).
ADI has exceeded the *high end* in two of the last four quarters, so this is not absurd — but it is an
aggressive read, and the trend in the revenue beat is not monotonic.

---

## 8. Analyst revisions, last 90 days — REPORTED FACT

Direction is decisively **positive on price targets, flat-to-fractionally-negative on the Q3 EPS number**.

| Date | Firm / analyst | Action | Rating | PT |
|---|---|---|---|---|
| 28 Jul 2026 | Weiss Ratings | Downgrade | Buy (B−) → Hold (C+) | — |
| 14 Jul 2026 | KeyBanc — John Vinh | Raise PT | Overweight | $500 → **$525** |
| 13 Jul 2026 | TD Cowen — Joshua Buchalter | Raise PT | Buy | $450 → $460 |
| 29 Jun 2026 | Cantor Fitzgerald — Matthew Prisco | Raise PT | Overweight | $510 → **$550** |
| 29 Jun 2026 | Fundamental Research | Initiate/Set PT | — | $550 |
| 24 Jun 2026 | Stifel — Tore Svanberg | Raise PT | Buy | $450 → $498 |
| ~11 Aug 2026 | (unnamed) | New Buy rating | Buy | — |
| — | Wells Fargo — Joseph Quatrochi | Reiterate | Overweight | $515 (unchanged) |
| 14 Jul 2026 (earlier ref) | Truist | Raise PT | — | $230 → $248 (older vintage; treat with care) |

Source: https://www.marketbeat.com/stocks/NASDAQ/ADI/forecast/ ; https://www.tipranks.com/news/the-fly/analog-devices-price-target-raised-to-248-from-230-at-truist

**Estimate revisions on the Q3 number itself:** Zacks reports the Q3 EPS consensus was
**revised DOWN by one cent over the past 30 days** (14 Aug 2026). An earlier Zacks note (22 Jun 2026)
said FY consensus had "remained unchanged in the past 30 days."

**Read: the Q3 quarter estimate has been essentially frozen at guidance+3c since May, while multi-year
numbers and price targets have been marked up hard.** That is a classic set-up where the street is
underwriting the guide for the quarter and paying for the FY27 story. It implies the *quarter* consensus
carries limited information beyond the guide — which is exactly why deviating far from $3.92bn / $3.33 is
a risk rather than an edge.

**Ratings distribution:** 31–33 covering analysts; 23 Strong Buy, 4 Moderate Buy, 4 Hold, 0 Sell.
Average price target **$441.00** (MarketBeat) to **$457.73** (StockAnalysis, 33 analysts) to **$452.96**
(Barchart, 31 analysts). Spread of ~$16 across aggregators.

---

## 9. Share price path — REPORTED FACT

| Item | Value | Date |
|---|---|---|
| Last close | **$389.39** (+$8.22, +2.16%) | 14 Aug 2026, 4:00 pm ET |
| After hours | $389.20 | 14 Aug 2026 |
| 52-week range | $223.47 – $445.91 | as of 14 Aug 2026 |
| Market cap | $189.67bn | 14 Aug 2026 |
| Trailing P/E | 57.97 | |
| Forward P/E | 27.77 | |
| 52-week total return | +66.7% (vs S&P 500 +16.5%) | 24 Jul 2026 |
| YTD return | +44.5% | 13 Jul 2026 |
| Dividend | $4.40 annual (1.13% yield); $1.10/qtr declared 20 May 2026 | |

Source: https://stockanalysis.com/stocks/adi/ ; https://www.barchart.com/story/news/3446493/here-s-what-to-expect-from-analog-devices-next-earnings-report

Notable intra-quarter moves: +4.82% on 4 Aug 2026 and +3.26% on 7 Aug 2026 (tradingkey.com market-mover
notes; no ADI-specific catalyst identified — read as sector/AI-complex beta).

The stock is ~13% off its 52-week high and ~12–18% below the average price target. It has **not** run into
the print, which slightly reduces the risk that a modest beat is sold — but it is priced at 58x trailing,
so the Q4 guide, not the Q3 print, is the swing factor.

---

## 10. Cycle, bookings, channel inventory and end markets — REPORTED FACT unless flagged

### Cycle position
ADI is in a **strong, broad, mid-cycle analog upturn**, not a late-cycle blow-off. CEO Roche, 20 May 2026,
on the non-ATE/non-A&D industrial businesses (automation, ETM, sustainable energy, healthcare, broad market):

> "Collectively, these markets have grown more than 40% in the first half of fiscal 2026. … From a cyclical
> perspective, these businesses are **still well below their prior cycle highs with lean channel inventories**."

Source: `.../call-transcripts/2026-05-20__adi-us-20260520-call-pres__1041157.md` (line 23)

### Bookings and book-to-bill
- Q2 FY26 press release: **"record bookings across our B2B markets of Industrial, Automotive, and Communications."**
- Q1 FY26 press release (18 Feb 2026): "bookings growth continued, driven by broad strength in Industrial
  and **record orders for our Data Center segment**." (`.../filings/2026-02-18__adi-us-20260218-q1-8k-2__602115.md` line 47)
- On automotive specifically (Q&A line 135): *"As we look out at Q3, we have **record bookings, positive
  book-to-bill**, and so we do expect to see above-seasonal growth sort of in that mid-high single digits."*
- Q2 close: *"We continue to see constructive demand signals in our order book and backlog, particularly in
  industrial, AI-related applications, and automotive."*

ADI does not publish a numeric book-to-bill. The qualitative signal is **>1.0 and rising**.

### Inventory — own and channel
- Own inventory **+$81m q/q**, deliberate: *"we continue to build strategic die bank and finished goods
  buffers to support growing demand."* Days of inventory **168**.
- **Channel inventory weeks DECLINED in Q2 and remain inside the 6–7 week target range.** (Call, line 43.)
  Note the corpus renders this as "six to seven-week range" in words, so it is not exposed to the
  minus-sign-stripping defect.
- Guidance assumption: *"baked into that outlook is also a **flat channel inventory weeks**."* (Q&A line 73.)
  So the guide does NOT assume channel restocking — any restock is upside.
- Automotive customer inventory: *"we're not seeing that [buildup] yet … automotive customers are fairly
  lean on inventory."* (Q&A line 135.)
- Lead times "in pretty good shape"; general customer atmosphere "one of general calmness," with the one
  named supply-chain choke point being **memory**, biting hardest on consumer customers. (Q&A line 17.)

### Guided Q3 end-market shape — REPORTED FACT (CFO, Q&A lines 71–73)

> "If we look at what we think at the midpoint of the guide, what we expect to see in Q3 is **continued
> above seasonal growth across industrial, automotive, and communication**. From an industrial and
> automotive perspective, we'd expect to grow sort of **mid to high single digits sequentially**. …
> From a comms perspective, we expect to be our fastest grower, **up low to mid-teens sequentially**.
> **Consumer is expected to be down single digits sequentially**… I would just remind you from a seasonality
> perspective, **the fourth quarter for us is usually up in the low single digits**."

**Bridge check (INFERENCE).** Applying those rates to the Q2 dollar bases:

| End market | Q2 FY26 $m | Guided q/q | Q3 implied $m |
|---|---|---|---|
| Industrial | 1,812 | +7% (mid–high SD) | 1,939 |
| Automotive | 870 | +7% (mid–high SD) | 931 |
| Communications | 543 | +13% (low–mid teens) | 614 |
| Consumer | 399 | −5% (down SD) | 379 |
| **Total** | **3,624** | | **3,863** |

At the top of each stated band (+9%/+9%/+15%/−3%) the bridge gives **$3,948m**. So the guided commentary
brackets roughly **$3.86bn–$3.95bn**, straddling the $3.9bn midpoint and sitting slightly *below* the
$3.92–3.93bn consensus at the middle of the bands. The guidance was internally consistent, not
sandbagged in the segment commentary — the sandbag, if any, is in ADI's habitual conservatism.

### Data center — the swing factor
- >75% of Communications; **+>90% y/y** in Q2; power and optical growing at similar rates.
- CFO: *"Given the momentum we're seeing, we really do expect this to continue to increase and be
  **the fastest grower sequentially** for us as we look out into the next quarter."* (Q&A line 51.)
- Data center is the mix-tailwind that could push adjusted GM above the 72.5% assumption — but note
  the analyst on line 85 pressed on exactly whether data center carries industrial-like margin, and
  management did not confirm a clear positive. Treat the mix tailwind as real but modest.

### Constraint
- Utilization is effectively **maxed**: *"we don't see a ton of future upside on gross margin from
  utilization given where we're running the factories today."* Incremental revenue above plan increasingly
  goes to **external foundry/OSAT**, which is GM-dilutive at the margin. **This is the key asymmetry:
  revenue upside above the high end tends to come with LESS-than-proportional GM upside.**

---

## 11. Working view for the forecaster — clearly labelled ESTIMATE / INFERENCE

Not instructions — inputs. Scoring is relative to consensus, so the default is to sit close to it and
deviate only where there is an articulable reason.

| Metric | Consensus (benchmark) | Guidance | Suggested lean | Reasoning |
|---|---|---|---|---|
| **Revenue (USDm)** | **3,925** (spread 3,920–3,930) | 3,900 ±100 | **3,980** (range 3,950–4,020) | ADI has beaten the midpoint by +3.2% on average over four quarters and exceeded the high end twice. But the segment bridge only supports $3.86–3.95bn at stated growth rates, and Empower adds nothing material. A +2.0% beat to $3,980m is the balanced read; the full +3.2% (to $4,025m) would push above the guided high end. Deviating ~+1.4% above consensus. |
| **Adjusted diluted EPS (USD)** | **3.33** (whisper 3.41) | 3.30 ±0.15 | **3.45** (range 3.40–3.52) | Mean beat vs midpoint is +$0.14 → $3.44. Revenue upside at ~72.7% GM and OpEx roughly flat as a % of sales drops through hard; tax guided 12–14% vs 11.8% actual in Q2 (a slight headwind — Q2's low rate flattered EPS). Empower is a ~$0.02–0.04 drag not in the guide. Net: $3.45, i.e. +$0.12 vs consensus, matching the Most-Accurate estimate direction. |
| **Adjusted gross margin (%)** | **72.5** (derived, no published street number) | ~72.5 implied | **72.8** (range 72.4–73.2) | Management explicitly modelled 73.0% − 50 bps. They also called mix a "slight tailwind" and beat their own GM assumption last quarter. Offsetting: utilization is maxed and revenue upside routes to external supply, which is dilutive; and the channel-repricing benefit genuinely does not repeat. Lean fractionally above the guide, not aggressively. **Report in POINTS: 72.8, not 0.728.** |

**Units check.** Revenue in **USDm** (≈3,980, not 3.98). EPS in **USD/share** (3.45). Gross margin in
**percentage points** (72.8). Adjusted, not GAAP — GAAP GM would be ~67–68% and GAAP EPS ~$2.75.

**Scoring floors for reference:** revenue floor = 0.5% of reported ≈ ±$20m; EPS floor ≈ ±$0.017;
GM floor = 0.5 percentage points. The GM floor is generous relative to the plausible dispersion
(72.4–73.2), so GM is the lowest-variance of the three metrics — do not get clever there.

---

## 12. Risks to this view

1. **The consensus GM number is derived, not observed.** If the street actually models 73.0%+ (carrying
   Q2 forward and ignoring the 50 bps commentary), our 72.8% would sit *below* consensus rather than
   above it. The 0.5-point floor limits the damage either way.
2. **Utilization ceiling / external supply mix.** Beating revenue by 3%+ could compress GM below 72.5%
   if the incremental units are outsourced. Revenue upside and GM upside are partly mutually exclusive.
3. **Empower Semiconductor is not in the guide.** Closed 7 July 2026 for $1.5bn cash — adds OpEx and
   non-operating expense inside the quarter with negligible offsetting revenue. Straight application of
   the historical EPS beat over-counts by ~$0.02–0.04.
4. **Consumer is guided down and memory is a named choke point.** Consumer was 11% of revenue and is the
   one segment where management flagged deterioration ("we do expect to see some impact there").
5. **Tax rate.** Q2 came in at 11.8%; Q3 is guided 12–14%. Assuming Q2's rate persists would overstate
   EPS by roughly $0.05–0.08.
6. **The beat has been decelerating on revenue** (+4.7% → +2.5% → +1.9% → +3.5%) — the pattern is noisy,
   not a reliable +3.2%.
7. **Stock at 58x trailing, ~13% off highs.** The Q4 guide, not the Q3 print, drives the reaction. Not a
   scoring risk but relevant to any read-through from post-print price action.

---

## 13. Corpus and web defects encountered — READ THIS

Two live traps, both of the kind the brief warned about:

1. **Mislabelled corpus index row.** `INDEX.md` lists
   `2026-05-20 | Filing | Q3 2026 | Quarterly Report on Form 10-Q →
   filings/2026-05-20__adi-us-20260520-q2-10q__1040607.md`.
   The **period column says "Q3 2026" but the document is the Q2 FY2026 10-Q** (filename says `q2-10q`,
   filed 20 May 2026 for the quarter ended 2 May 2026). There is no Q3 FY2026 10-Q in existence.
   Do not read this as Q3 data.

2. **Web aggregator presenting FY2025 results as August-2026 news.** A search result
   (itiger.com, "US Stock Alert: Analog Devices Surges 6.26% as Earnings Beat Expectations") is surfaced
   with an August 2026 framing but reports **"revenue of $2.88 billion (up 24.7% y/y, exceeding
   expectations of $2.77 billion) and adjusted EPS of $2.05 (vs $1.95 expected)."** Those are the
   **Q3 FY2025** actuals from **20 August 2025**. This is *not* a Q3 FY2026 result. Anyone anchoring on it
   would forecast ~$2.88bn / $2.05 — a catastrophic ~26% / ~38% error.
   *(Incidentally it does give a useful datum: the Q3 FY2025 street numbers were $2.77bn rev / $1.95 EPS,
   i.e. ADI beat consensus by +4.0% on revenue and +$0.10 on EPS that quarter.)*

3. **Truist "$230 → $248" price target** surfaced in search alongside 2026 items is an **older vintage**
   (pre-2026 split of the rating cycle); it is inconsistent with the $440–550 target cluster of every
   other 2026 note. Ignore it as a current data point.

No minus-sign-stripping defects were identified in the ADI documents I read — the margin and growth
tables in the 8-Ks carry explicit "bps" and "%" labels and reconcile against the narrative.

---

## Source index

**Corpus (absolute paths):**
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/filings/2026-05-20__adi-us-20260520-q2-8k__1040581.md` — Q2 FY26 results + Q3 FY26 guidance
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/call-transcripts/2026-05-20__adi-us-20260520-call-pres__1041157.md` — Q2 FY26 prepared remarks
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/call-transcripts/2026-05-20__adi-us-20260520-call-qna__1041159.md` — Q2 FY26 Q&A (gross margin, segment guide, bookings)
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/filings/2026-02-18__adi-us-20260218-q1-8k-2__602115.md` — Q1 FY26 results + Q2 guidance
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/filings/2025-11-25__adi-us-20251125-q4-8k__361005.md` — Q4/FY25 results + Q1 FY26 guidance
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/filings/2025-08-20__adi-us-20250820-q3-8k__155976.md` — **Q3 FY2025 prior-year actuals**
- `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/analog-devices/filings/2025-05-22__adi-us-20250522-q2-8k__102679.md` — Q3 FY25 guidance

**Web:**
- https://investor.analog.com/news-releases/news-release-details/analog-devices-report-third-quarter-fiscal-year-2026-financial (23 Jul 2026)
- https://www.sec.gov/Archives/edgar/data/6281/000000628126000050/adi2q26exhibit991earnings.htm (20 May 2026)
- https://www.theglobeandmail.com/investing/markets/stocks/ADI/pressreleases/3853356/should-you-buy-sell-or-hold-adi-stock-before-q3-earnings/ (14 Aug 2026, Zacks)
- https://www.benzinga.com/trading-ideas/dividends/26/08/61205809/how-to-earn-500-a-month-from-analog-devices-stock-ahead-of-q3-earnings (Aug 2026)
- https://www.barchart.com/story/news/3446493/here-s-what-to-expect-from-analog-devices-next-earnings-report (24 Jul 2026)
- https://stockanalysis.com/stocks/adi/forecast/ (14 Aug 2026)
- https://stockanalysis.com/stocks/adi/ (14 Aug 2026 close)
- https://www.marketbeat.com/stocks/NASDAQ/ADI/forecast/ (14 Aug 2026)
- https://investor.analog.com/news-releases/news-release-details/analog-devices-completes-acquisition-empower-semiconductor (7 Jul 2026)
- https://www.prnewswire.com/news-releases/analog-devices-completes-acquisition-of-empower-semiconductor-302819437.html (7 Jul 2026)
- https://simplywall.st/stocks/us/semiconductors/nasdaq-adi/analog-devices/news/will-lofty-q3-2026-earnings-expectations-reshape-analog-devi (25 Jul 2026)
- https://simplywall.st/stocks/us/semiconductors/nasdaq-adi/analog-devices/news/is-analog-devices-adi-undervalued-as-data-center-demand-and (13 Jul 2026)
- https://www.theglobeandmail.com/investing/markets/stocks/ADI/pressreleases/2581743/can-analog-devices-sustain-margin-expansion-throughout-2026/ (22 Jun 2026, Zacks)
- https://www.aetrixelec.com/blog/analog-devices-price-increase-september-2026 (price increase eff. 13 Sep 2026)
