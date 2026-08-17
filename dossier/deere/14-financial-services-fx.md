# Deere FY2026 Q3 — John Deere Financial Services & Currency

**Workstream:** financial-services-fx
**Prepared:** 16 August 2026 (Deere reports FY2026 Q3 on **20 August 2026**)
**Corpus:** `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere` (frozen 14 Aug 2026)

---

## 0. Metadata-trap check (mandatory)

The corpus `INDEX.md` row `2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call Transcript` →
`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` is **mislabelled**. Its header carries
`published_at: "2026-05-21"` and `period: "Q3 2026"`, but the body is the **Q2 FY2026 earnings-call Q&A**: it
discusses the C&F industry guide "up 5%" (the 21-May-2026 Q2 outlook) and forward-looking half-year cadence
("we expect back half to be higher than the front half, Q4 would be a little bit higher than Q3").

**There are no FY2026 Q3 actuals anywhere in the corpus or in any source I found online.** Every Q3 FY2026 figure
below is my estimate or inference, labelled as such.

---

## 1. Why this workstream matters to the three forecast targets

| Target | Financial Services / FX linkage |
|---|---|
| Worldwide net sales and revenues | "Financial Services revenues" is an explicit line in the revenue build — $1,418M of the $12,018M reported in Q3 FY2025 (**11.8%**). FX translation moves the equipment lines. |
| Diluted EPS (GAAP) | FS net income flows straight into consolidated net income — $205M of $1,289M in Q3 FY2025 (**15.9%**, ≈ **$0.76/share**). |
| PPA operating profit | FS operating profit is a **separate** segment and is *not* in PPA. But the **"Currency" bar in the PPA operating-profit waterfall** is one of the largest and most volatile swing factors: −$39M in Q1 FY2026, **+$75M in Q2 FY2026**, −$52M in Q3 FY2025. |

Source for the revenue/profit split: `filings/2025-08-15__de-us-20250815-q3-8k__143410.md` (Q3 FY2025 press release);
`filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` (Q2 FY2026 press release).

---

## 2. Financial Services quarterly history (REPORTED FACT)

All figures $ millions, from the segment tables in each quarter's 8-K earnings release.

### 2a. "Financial Services revenues" (as reported in the net-sales-and-revenues build)

| FY | Q1 | Q2 | Q3 | Q4 | FY total |
|---|---|---|---|---|---|
| 2021 | 884 | 892 | 902 | 869 | 3,548 |
| 2022 | 870 | 864 | 903 | 988 | 3,625 |
| 2023 | 1,040 | 1,107 | 1,228 | 1,347 | 4,721 |
| 2024 | 1,376 | 1,395 | 1,489 | 1,522 | 5,782 |
| 2025 | 1,470 | 1,385 | 1,418 | **1,548*** | 5,821 |
| 2026 | 1,384 | 1,366 | **est. 1,400** | est. 1,455 | guide n/a |

\* FY2025 Q4 was a **14-week quarter** (FY2025 ran 27 Oct 2024 → 2 Nov 2025 = 53 weeks). FY2026 quarters are all 13 weeks
(Q1 ended 1 Feb 2026, Q2 ended 3 May 2026, Q3 ends ~2 Aug 2026). *(inference from period-end dates on the filings.)*

Sources by row: `filings/2022-02-18__de-us-20220218-q1-8k__105812.md`, `.../2022-05-20…q2-8k__105815.md`,
`.../2022-08-19…q3-8k__105811.md`, `.../2022-11-23…q4-8k__105825.md`, `.../2023-02-17…q1-8k__105833.md`,
`.../2023-05-19…q2-8k__105839.md`, `.../2023-08-18…q3-8k__105829.md`, `.../2023-11-22…q4-8k__105823.md`,
`.../2024-02-15…q1-8k__105824.md`, `.../2024-05-16…q2-8k__105819.md`, `.../2024-08-15…q3-8k__105836.md`,
`.../2024-11-21…q4-8k__105840.md`, `.../2025-02-13…q1-8k__105841.md`, `.../2025-05-15…q2-8k__105808.md`,
`.../2025-08-15…q3-8k__143410.md`, `.../2025-11-26…q4-8k__361233.md`, `.../2026-02-19…q1-8k__603009.md`,
`.../2026-05-21…q2-8k__1042167.md`.

### 2b. FS net income attributable to Deere & Co.

| FY | Q1 | Q2 | Q3 | Q4 | FY total | FY guide at Q2 |
|---|---|---|---|---|---|---|
| 2022 | 231 | 208 | 209 | 232 | 880 | — |
| 2023 | 185 | 28† | 216 | 190 | 619 | — |
| 2024 | 207 | 162 | 153 | 173 | 695 | — |
| 2025 | 230 | 161 | 205 | 293 | **889 (~$890)** | ~$750 |
| 2026 | 244 | 190 | **est. 200** | est. 230 | **guide ~$860** | ~$860 |

† Q2 FY2023 included a **$135M after-tax** correction of accounting for dealer financing incentives
(`filings/2023-05-19__de-us-20230519-q2-8k__105839.md`).

### 2c. FS **operating profit** (segment line; includes interest expense and FX gains/losses)

| FY | Q1 | Q2 | Q3 | Q4 | FY total |
|---|---|---|---|---|---|
| 2022 | 296 | 279 | 287 | 297 | 1,159 |
| 2023 | 238 | 41 | 286 | 229 | 795 |
| 2024 | 257 | 209 | 191 | 231 | 889 |
| 2025 | 266 | 207 | 266 | 374 | 1,114 |
| 2026 | 301 | 251 | **est. 265** | est. 300 | — |

### 2d. FY guidance track record for FS net income (REPORTED FACT — shows Deere's bias)

| Guide issued | For FY | Guide | Actual | Delta |
|---|---|---|---|---|
| 22 Nov 2023 (Q4'23) | FY2024 | ~$770 | 695 | **−75** |
| 21 Nov 2024 (Q4'24) | FY2025 | ~$750 | 889 | **+139** |
| 15 May 2025 (Q2'25) | FY2025 | ~$750 | 889 | **+139** |
| 15 Aug 2025 (Q3'25) | FY2025 | ~$770 | 889 | **+119** |
| 26 Nov 2025 (Q4'25) | FY2026 | ~$830 | — | — |
| 19 Feb 2026 (Q1'26) | FY2026 | ~$840 | — | — |
| 21 May 2026 (Q2'26) | FY2026 | **~$860** | — | — |

**Inference:** Deere has raised the FY2026 FS guide at each of the last two prints (830 → 840 → 860) and under-guided
FY2025 by ~$120–140M all year. The ~$860M guide implies H2 FY2026 = **$426M** (FY $860 − H1 actual $434). That is
−14% vs H2 FY2025's $498M — but H2 FY2025 contained the **extra 14th week** in Q4. On a like-for-like week count the
guide is roughly flat, and Deere's revealed conservatism argues for the upper half of any range.

---

## 3. What actually drives FS earnings — Q2 FY2026 detail (REPORTED FACT)

From the supplemental consolidating income statement, `filings/2026-05-21__de-us-20260521-q2-10q__1055929.md`
(Q2 10-Q, filed 21 May 2026) — Financial Services column, three months ended 3 May 2026 vs 27 Apr 2025:

| $M | Q2 FY2026 | Q2 FY2025 | Δ |
|---|---|---|---|
| Finance and interest income | 1,359 | 1,380 | −1.5% |
| Other income | 150 | 121 | +24% |
| **Revenue (incl. intercompany)** | **1,509** | **1,501** | **+1%** |
| Interest expense | 649 | 721 | **−10%** |
| *Net revenue after interest ("spread")* | *860* | *780* | *+10.3%* |
| SA&G | 231 | 238 | −3% |
| Other operating expenses (mainly op-lease depreciation) | 369 | 335 | +10% |
| Pre-tax income | 260 | 207 | +26% |
| Tax | 66 | 49 | (25.4% rate) |
| Equity in income (loss) of unconsolidated affiliates (BJD 50%) | (4) | 3 | — |
| **Net income** | **190** | **161** | **+18%** |

Comparable Q3 FY2025 figures (`filings/2025-08-14__de-us-20250814-q3-10q__155834.md`):
revenue incl. intercompany **$1,544M**, interest expense **$720M**, net income **$205M**; average portfolio **−6%** YoY
"primarily due to the deconsolidation of BJD."

### Driver 1 — Portfolio size (shrinking, but decelerating)

| Metric ($M) | 3 May 2026 | 2 Nov 2025 | 27 Apr 2025 | YoY |
|---|---|---|---|---|
| Retail notes & financing leases | 37,291 | — | 37,991 | −1.8% |
| Revolving charge accounts | 4,566 | 4,801 | 4,140 | **+10.3%** |
| Wholesale receivables | 7,426 | 8,255 | 8,921 | **−16.8%** |
| **Total financing receivables** | **49,283** | — | **51,052** | **−3.5%** |

Deere states the **average** balance of receivables and leases financed was **−1% in Q2 FY2026** and **−2% in H1 FY2026**
(vs −6% in Q3 FY2025) — i.e. the portfolio drag is fading fast as the BJD deconsolidation (Feb 2025) laps.
On the Q2 call: *"year-over-year on our JDF … trade wholesale, so that used equipment that's giving finance on the lots
of dealers, is down over 15% just in terms of the portfolio size"*
(`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`).

Note: `filings/2026-05-21__de-us-20260521-q2-10q__1055929.md` also shows FS **ratio of interest-bearing debt to
stockholder's equity of 8.7 to 1** at 3 May 2026 (8.4:1 at FY-end 2025, 8.7:1 a year ago).

### Driver 2 — Net interest margin (the swing factor, and it is favourable)

Interest expense is down **−10% YoY in Q2 FY2026** and **−12% in H1**, "as a result of lower average borrowing rates and
lower average borrowings." Deere attributes the net-income increase to **"favourable financing spreads and favourable
derivative valuation adjustments"** in Q2 and, for H1, additionally a **lower provision for credit losses**.

The asset side is dominated by **fixed-rate retail notes** with multi-year lives; the liability side (commercial paper,
short term-debt, securitisations) reprices far faster. With the Fed 71bp lower in May–Jul 2026 than in May–Jul 2025
(§5), the same favourable-spread dynamic that produced Q2's +10.3% spread growth should persist into Q3.

### Driver 3 — Provisions and credit quality (benign — the "rising delinquency" thesis does NOT hold in Deere's book)

Allowance rollforward, `filings/2026-05-21__de-us-20260521-q2-10q__1055929.md`:

| $M | Q2 FY2026 | Q2 FY2025 | H1 FY2026 | H1 FY2025 |
|---|---|---|---|---|
| Provision | 89 | 94 | **127** | **163** |
| Gross write-offs | (93) | (96) | (150) | (157) |
| Recoveries | 17 | 11 | 32 | 23 |
| *Net write-offs* | *76* | *85* | *118* | *134* |
| Ending allowance | **267** | **258** | 267 | 258 |
| Allowance / financing receivables | **0.54%** | **0.51%** | — | — |

Retail-customer-receivable credit quality (my computation from the aging tables in the same 10-Q):

| | 3 May 2026 | 27 Apr 2025 |
|---|---|---|
| Total retail customer receivables | $41,857M | $42,131M |
| 30+ days past due | $713M (**1.70%**) | $730M (**1.73%**) |
| Non-performing | $742M (**1.77%**) | $732M (**1.74%**) |
| **Past due + non-performing** | **3.48%** | **3.47%** |

**Inference:** essentially flat YoY. Deere's own narrative pins the small allowance build on **"higher expected losses on
construction retail accounts"** — not agriculture. Wholesale receivables are near-pristine (30+ past due ≈ $0 on
$7,426M). A provision-driven Q3 miss is a low-probability risk.

### Driver 4 — Lease residuals (currently a tailwind, not a risk)

`filings/2025-11-26__de-us-20251126-q4-10k__469216.md` (FY2025 10-K) sensitivity: *"if (a) future market values for this
equipment were to decrease 10% from our present estimates, and (b) all the equipment on operating leases were returned …
the total unfavorable impact after consideration of dealer residual value guarantees would be approximately **$65**"*
(recognised over remaining lease terms, i.e. **well under $20M in any single quarter**). Residuals are a second-order
item at current used-equipment prices (§6).

---

## 4. FS forecast for Q3 FY2026 (ESTIMATE)

Bottom-up build, three months ending ~2 Aug 2026:

| $M | Q3 FY2025 (actual) | Q3 FY2026 (my estimate) | Basis |
|---|---|---|---|
| Revenue incl. intercompany | 1,544 | **1,545** (1,520–1,585) | avg portfolio ~−1%, offset by higher revolving balances (+10%) and fee/other income (+24% in Q2) |
| Interest expense | 720 | **660** (645–685) | −8% YoY; Q2 ran −10%, funding base rate −71bp YoY |
| Spread | 824 | **885** (+7%) | |
| SA&G | ~235 | **235** | Q2 = 231, trending flat/down |
| Other operating expenses | ~350 | **385** | op-lease depreciation running +10% YoY |
| Pre-tax | ~270 | **265** | |
| Tax @ ~25% | | (66) | Q2 effective 25.4% |
| Equity in loss of unconsol. affiliates (BJD) | | (4) | Q2 = −4 |
| **FS net income** | **205** | **≈ 200** | range **175–230** |

**Cross-checks:**
- Guidance-implied: FY ~$860 − H1 $434 = H2 $426; at FY2025's 41/59 Q3/Q4 split → Q3 ≈ **$188M**; at 50/50 → **$213M**.
- Deere's persistent under-guiding of FS (+$120–140M on FY2025) skews the distribution upward.
- Q4 FY2026 is a 13-week quarter vs FY2025 Q4's 14 weeks, so more of H2's dollars must land in Q3 than the raw FY2025
  seasonal split implies — another upward nudge on Q3.

### Numbers to feed the model

| Line | Q3 FY2025 actual | **Q3 FY2026 estimate** | Range |
|---|---|---|---|
| Financial Services **revenues** (revenue-build line) | 1,418 | **1,400** | 1,370–1,440 |
| Financial Services **operating profit** | 266 | **265** | 235–300 |
| Financial Services **net income** | 205 | **200** | 175–230 |
| FS contribution to **diluted EPS** | $0.76 | **≈ $0.74** | $0.65–$0.85 |
| "Other revenues" (non-FS, non-equipment) | 243 | **≈ 235** | 220–250 |

Diluted average shares: **270.1M** in Q2 FY2026 vs 271.1M a year earlier (`…q2-10q__1055929.md`) — only −0.4% YoY, so
buybacks add ~$0.02–0.03 to Q3 EPS at most. Assume **~269.5–270.0M** for Q3 FY2026.

---

## 5. Interest-rate environment, May–July 2026 (REPORTED FACT, external)

| Date | Fed funds target range | Note |
|---|---|---|
| through 16 Sep 2025 | 4.25–4.50% | the Q3 FY2025 comparison base |
| 17 Sep 2025 | 4.00–4.25% | cut |
| 29 Oct 2025 | 3.75–4.00% | cut |
| 10 Dec 2025 | 3.50–3.75% | cut |
| 17 Jun 2026 | **3.50–3.75%** | **held** |
| 29 Jul 2026 | **3.50–3.75%** | **held, 9–3** — Hammack, Kashkari, Logan dissented in favour of a **25bp HIKE** |

Sources: [Federal Reserve FOMC statement, 17 June 2026](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260617a.htm);
[Fed rate decision July 2026 — CNBC, 29 July 2026](https://www.cnbc.com/2026/07/29/fed-rate-decision-july-2026.html);
[Fed Funds Target Rate History, fedprimerate.com (accessed 16 Aug 2026)](https://www.fedprimerate.com/fedfundsrate/federal_funds_rate_history.htm);
[Implementation Note, 29 July 2026](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a1.htm).

**Implications (inference):**
1. Policy rate in Deere's Q3 FY2026 (May–Jul 2026) averaged **~3.62% EFFR** vs **~4.33%** in Q3 FY2025 — a **−71bp** YoY
   funding tailwind, essentially the same YoY delta JDCC enjoyed in Q2 FY2026 (Feb–Apr: −75bp). The −8% to −10% YoY
   decline in FS interest expense should repeat.
2. **The direction of risk flipped hawkish during the quarter.** Three dissents for a hike in July, and markets pricing
   two 2026 hikes, mean the spread tailwind is a FY2026 story that fades in FY2027 — relevant to Deere's Q4/FY2027
   commentary on 20 August, not to the Q3 print itself.
3. Farm-borrower rates stayed high: KC Fed reports the average rate on farm loans >$100,000 at **slightly under 7%** in
   Q2 2026, "nearly unchanged from the previous quarter." High customer financing costs are a demand headwind Deere
   management repeatedly cites (Q2 call: *"elevated interest rates continue to affect purchasing decisions"*).

---

## 6. US farm credit quality and used-equipment values (REPORTED FACT, external)

### Farm credit
- **Delinquency rates remain low but are edging up.** About **1.3% of farm loans** at both agricultural and
  non-agricultural banks were delinquent in **Q2 2026**; credit conditions "continued to deteriorate gradually … but the
  level of financial stress was modest, and farmland values remained strong."
  ([KC Fed, Agricultural Finance Updates](https://www.kansascityfed.org/agriculture/agfinance-updates/), Q2 2026 releases;
  [KC Fed, New Farm Loan Originations Ease Slightly](https://www.kansascityfed.org/center-for-agriculture-and-the-economy/agricultural-finance/new-farm-loan-originations-ease-slightly/))
- **Q1 2026:** farm loan delinquency rates "nearly unchanged from a year ago"; the ag-loan charge-off rate at the largest
  banks **declined slightly** in Q1 2026 after rising to ~**0.25%** in mid-2025.
  ([KC Fed, Farm Debt Grows and Delinquencies Rise Modestly](https://www.kansascityfed.org/agriculture/agfinance-updates/farm-debt-grows-and-delinquencies-rise-modestly/))
- **Regional surveys** (Dallas, Minneapolis, Chicago Fed districts) report softer loan repayment rates, more renewals and
  extensions, and tighter credit standards in Q2 2026 — but "most loan repayment issues remained minor."
  ([Dallas Fed Agricultural Survey Q2 2026](https://www.dallasfed.org/research/surveys/agsurvey/2026/ag2602);
  [KC Fed, Steady Tightening of Agricultural Credit Conditions Persists](https://www.kansascityfed.org/agriculture/ag-credit-survey/steady-tightening-of-agricultural-credit-conditions-persists/);
  [Minneapolis Fed, higher input costs pressure district farmers, 2026](https://www.minneapolisfed.org/article/2026/higher-input-costs-pressure-district-farmers))
- **Notably**, farm **machinery and equipment loan** originations rose **more than 50%** from recent years in Q2 2026 even
  as other non-real-estate purposes declined — a positive read for equipment demand financing.

**Inference:** industry-wide deterioration is real but gradual and from a very low base, and it is running well behind
what would be needed to force a Deere provision spike within one quarter. It is consistent with Deere's own flat
delinquency ratios (§3, Driver 3). **I do not forecast a provision-driven FS earnings hit in Q3 FY2026.**

### Used-equipment values → lease residuals
[Sandhills Global / TractorHouse market report, June 2026 data (published July 2026)](https://www.tractorhouse.com/blog/sandhills-news/2026/07/used-planter-values-surge-as-farm-equipment-inventory-declines);
[Sandhills market reports, 6 July 2026](https://www.morningstar.com/news/pr-newswire/20260706cg98367/sandhills-market-reports-show-continued-inventory-declines-across-used-equipment-and-truck-markets):

| Category (June 2026) | Inventory YoY | Auction value M/M | Auction value **YoY** |
|---|---|---|---|
| High-HP tractors | **−16.7%** (13 straight months down) | +0.56% | **+3.74%** |
| 175–299 HP tractors | — | +1.1% | **+4.21%** |
| Combines | −10.2% | −0.51% | **+0.72%** |
| Planters | — | +6.9% | **+13.3%** |

Corroborated inside Deere: on the Q2 FY2026 call management said used inventories are *"down like 45% from their peak a
year ago"* (`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`).

**Inference:** used values are **rising** YoY and inventories are shrinking. Residual write-downs are therefore a
**non-event** for Q3 FY2026; the tail risk sits on the upside (gains on operating-lease dispositions). Note the FS
"Other operating expenses" line (op-lease depreciation) is nevertheless running **+10% YoY** on a growing operating-lease
book, which is a volume effect, not an impairment effect.

---

## 7. Currency

### 7a. How Deere quantifies currency (REPORTED FACT — three distinct disclosures)

1. **Percentage-point translation effect on segment net sales**, a line in each segment's quarterly table in the 10-Q
   and press release: *"Currency translation impact on Net sales."*
2. **A "Currency Translation" percentage column** in the *Deere Segment Outlook* table in each earnings release.
3. **A dollar "Currency" bar** in the operating-profit waterfall on the earnings-call slides. This bar mixes
   *translation* and *transaction* effects (margin on US-manufactured exports) and can have the **opposite sign** to the
   sales-translation line. Management on the Q2 FY2026 call: *"Foreign currency was also a tailwind in the quarter versus
   last year, largely driven by a weaker U.S. dollar, which favorably impacts the margins on U.S. products exported to
   overseas markets."*

Observed values:

| Quarter | PPA sales translation | SAT | C&F | PPA op-profit "Currency" bar | SAT bar | C&F bar |
|---|---|---|---|---|---|---|
| Q2 FY2025 | (not disclosed as +/−) | — | — | **−$92M** | +$7M | −$14M |
| Q3 FY2025 | ~0 (9M: −1) | +1% | +1% | **−$52M** | +$9M | −$1M |
| Q4 FY2025 | — | — | — | **−$12M** | +$2M | +$4M |
| Q1 FY2026 | **+4%** | +2% | +4% | **−$39M** | −$14M | — |
| **Q2 FY2026** | **+3%** | **+2%** | **+3%** | **+$75M** | **+$27M** | **−$9M** |

Sources: `filings/2026-05-21__de-us-20260521-q2-10q__1055929.md`, `filings/2026-02-26__de-us-20260226-q1-10q__636995.md`,
`filings/2025-08-14__de-us-20250814-q3-10q__155834.md`, `slides/2026-05-21__de-us-20260521-slide__1042212.md`,
`slides/2026-02-19__de-us-20260219-slide__603088.md`, `slides/2025-08-15__de-us-20250815-slide__143404.md`,
`slides/2025-11-26__de-us-20251126-slide__361243.md`, `slides/2025-05-15__de-us-20250515-slide__46462.md`.

**Deere's FY2026 currency-translation guidance has been raised all year** (the dollar weakened through FY2026 H1):

| Guide date | PPA | SAT | C&F |
|---|---|---|---|
| 26 Nov 2025 (Q4'25) | +1.5% | +1.0% | +1.0% |
| 19 Feb 2026 (Q1'26) | +3.0% | +2.0% | +2.0% |
| **21 May 2026 (Q2'26)** | **+3.0%** | **+1.0%** | **+2.0%** |

### 7b. Actual FX moves, Deere's Q3 FY2026 window (May–July 2026) vs prior year (REPORTED FACT)

Monthly averages from [x-rates.com monthly average tables, 2025](https://www.x-rates.com/average/?from=USD&to=EUR&amount=1&year=2025)
and [2026](https://www.x-rates.com/average/?from=USD&to=EUR&amount=1&year=2026) (accessed 16 Aug 2026; same source for
BRL, INR, CAD). Values expressed as **USD strength of the foreign currency**, i.e. the direction of the translation effect.

| Pair | May–Jul **2025** avg | May–Jul **2026** avg | **Q3 FY26 YoY** | (memo) Q2 FY26 YoY (Feb–Apr) |
|---|---|---|---|---|
| **EUR** (USD per EUR) | 1.1497 | 1.1536 | **+0.3%** | **+8.2%** |
| **BRL** (reals per USD; ↓ = stronger real) | 5.5818 | 5.0844 | **+9.8%** | **+11.8%** |
| **INR** (rupees per USD; ↑ = weaker rupee) | 85.73 | 95.45 | **−10.2%** | **−6.5%** |
| **CAD** (CAD per USD) | 1.3740 | 1.3959 | **−1.6%** | **+3.7%** |

Broad measure: the Fed's **Nominal Broad U.S. Dollar Index was ~119.7–120.7 in July 2026, up ~1.2% YoY**
([Trading Economics / Fed data, Aug 2026](https://tradingeconomics.com/united-states/trade-weighted-us-dollar-index-broad-goods-and-services-fed-data.html)) —
i.e. on a trade-weighted basis the dollar was **stronger**, not weaker, than a year earlier.

### 7c. My translation estimate for Q3 FY2026 (INFERENCE — this is the key finding)

Weights from Deere's FY2025 net sales and revenues **by customer location**
(`filings/2025-11-26__de-us-20251126-q4-10k__469216.md`, Note 5, total $45,684M):

| Region | FY2025 $M | Weight | Proxy currency |
|---|---|---|---|
| United States | 23,974 | 52.5% | USD |
| Canada | 3,735 | 8.2% | CAD |
| Western Europe | 6,550 | 14.3% | EUR |
| Central Europe & CIS | 1,575 | 3.4% | EUR-linked |
| Latin America | 5,607 | 12.3% | BRL |
| Asia, Africa, Oceania, Middle East | 4,243 | 9.3% | INR |

**Model calibration on Q2 FY2026 (known answer):**
`0.177×(+8.22%) + 0.123×(+11.76%) + 0.093×(−6.45%) + 0.082×(+3.69%) = **+2.61 pts**`
Actual revenue-weighted segment disclosure = `(4,503×3 + 3,485×2 + 3,790×3) / 11,778` = **+2.70 pts**. Model error 0.1pt.

**Applying the same model to Q3 FY2026 (May–Jul 2026):**
`0.177×(+0.34%) + 0.123×(+9.78%) + 0.093×(−10.18%) + 0.082×(−1.57%) = **+0.18 pts**`

> **The FX translation tailwind essentially disappears in Q3 FY2026.** Central estimate **+0.2%**, plausible range
> **0% to +1.0%**, versus **+2.7%** in Q2 FY2026. In dollars on ~$10.4bn of equipment net sales this is **~+$20M**
> (range $0–$105M) versus **~+$300M** in Q2 FY2026 — a **~$280M quarter-on-quarter collapse in the FX contribution to
> YoY sales growth**.

Why: the euro comparison base is the *weakest-dollar months of 2025* (EUR averaged 1.17 in July 2025), so EUR is flat
YoY; and the INR headwind widened from −6.5% to −10.2% while the CAD flipped from +3.7% to −1.6%. Only Brazil still
helps.

**Tension with Deere's own guide, and how to resolve it:** the 21-May-2026 FY guide of **PPA +3.0%** currency, against
H1 actuals of +4% (Q1) and +3% (Q2), arithmetically implies roughly **+2.5–2.7% in H2**. That guide was struck at
~20 May 2026 spot (EUR ≈ 1.17); the euro then fell to a **1.1419 July average** before recovering to ~1.157 by
14 Aug 2026. My read is that **Deere's H2 currency assumption was set too high by roughly 2 points**, which is a
downside risk to reported sales versus the company's own May framework — though not necessarily versus sell-side
models, which mark to spot.

Sensitivity check on the load-bearing input: even if the July 2026 EUR average were 1.15 rather than 1.1419, the
May–Jul 2026 EUR average becomes 1.1564, i.e. **+0.6% YoY** — the conclusion is unchanged.

### 7d. FX effect on Financial Services specifically (small)

FS revenues by customer location, FY2025 (same Note 5): US $4,450M (**76.4%**), Canada $761M (13.1%), Western Europe
$185M, Central Europe/CIS $11M, Latin America $197M, Asia/Africa/Oceania/ME $217M. With Brazil now equity-method (BJD
deconsolidated Feb 2025), **FS is ~90% USD/CAD**. Applying §7c rates: **FX effect on FS revenue in Q3 FY2026 ≈ −0.2% to
0%** — negligible, and slightly negative. Do **not** add an FX tailwind to the FS revenue line.

### 7e. FX effect on **PPA operating profit** (the volatile one)

The PPA op-profit "Currency" bar is a YoY *delta* and mixes translation with transaction/hedge effects. It swung
**−$39M → +$75M** between Q1 and Q2 FY2026 (a $114M swing) on a *smaller* sales-translation number (+4% → +3%),
which shows the bar is driven mainly by **export transaction margin and hedge marks, not translation**.

With the broad dollar **+1.2% YoY** in July 2026 and EUR flat, the export-margin tailwind that produced Q2's +$75M
largely evaporates. Against a Q3 FY2025 base of **−$52M**:

> **Estimate: PPA op-profit "Currency" contribution in Q3 FY2026 ≈ $0M, range −$40M to +$40M** (vs +$75M in Q2 FY2026).
> Anyone who straight-lines Q2's +$75M currency benefit into their Q3 PPA operating-profit model is **~$75M too high**.

---

## 8. Consensus context (for calibration, not a source of truth)

Street consensus for Q3 FY2026 as of mid-August 2026: **diluted EPS ~$4.85–4.86** (vs $4.75 in Q3 FY2025, +2.1–2.3%) and
**net sales ~$10.87bn** (equipment only, +4.95% vs $10.357bn). Adding my FS revenue estimate ($1,400M) and Other revenues
(~$235M) implies **total net sales and revenues ≈ $12.5bn** at consensus equipment sales.
Earnings date confirmed as **20 August 2026**.
Sources: [Deere to Announce Third Quarter 2026 Financial Results, 5 Aug 2026](https://www.nasdaq.com/press-release/deere-announce-third-quarter-2026-financial-results-2026-08-05);
[Deere Sets Q3 2026 Earnings Call for Aug. 20 — StockTitan](https://www.stocktitan.net/news/DE/deere-to-announce-third-quarter-2026-financial-ws5vrthl5ifm.html);
[Deere & Company Earnings Preview: What to Expect — Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/deere-company-earnings-preview-expect-122951821.html).

---

## 9. Summary of numbers to hand to the forecasting model

| # | Item | Value | Type |
|---|---|---|---|
| 1 | Financial Services revenues, Q3 FY2026 | **$1,400M** (1,370–1,440) | estimate |
| 2 | Financial Services revenues, Q3 FY2025 | $1,418M | reported fact |
| 3 | Other revenues, Q3 FY2026 | **~$235M** | estimate |
| 4 | FS net income, Q3 FY2026 | **$200M** (175–230) | estimate |
| 5 | FS operating profit, Q3 FY2026 | **$265M** (235–300) | estimate |
| 6 | FS EPS contribution, Q3 FY2026 | **~$0.74** | inference |
| 7 | Diluted share count, Q3 FY2026 | **~269.5–270.0M** | inference (270.1M in Q2) |
| 8 | Company FX translation on net sales, Q3 FY2026 | **+0.2%** (0% to +1.0%) | inference |
| 9 | …in dollars on equipment net sales | **~+$20M** (0 to +$105M) | inference |
| 10 | …versus Q2 FY2026 | +2.7% / ~+$300M | reported fact + inference |
| 11 | PPA op-profit "Currency" bar, Q3 FY2026 | **~$0M** (−$40M to +$40M) | inference |
| 12 | FS FY2026 guidance (21 May 2026) | **~$860M** net income | reported fact |
| 13 | Fed funds, May–Jul 2026 vs 2025 | 3.50–3.75% vs 4.25–4.50% (−71bp) | reported fact |

---

## 10. Gaps and things I could not find

- **No FY2026 Q3 actuals exist** in the corpus or online — confirmed. The `Q3 2026` transcript label is wrong (§0).
- **John Deere Capital Corporation's separate 10-Q** (JDCC files its own reports with the SEC) is **not in the corpus**,
  and I did not locate a filed FY2026 Q2 JDCC 10-Q online. That would give a cleaner NIM and delinquency series than the
  consolidated segment view.
- **No monthly Deere-specific used-equipment index.** Sandhills is the best public proxy; I could not fetch the
  July-2026 report directly (`tractorhouse.com` returned HTTP 403) and relied on the June-2026 data plus the 6 July 2026
  Sandhills press summary.
- **kansascityfed.org and dallasfed.org returned HTTP 403** to direct fetches; the Q2-2026 delinquency figure (1.3%) and
  rate figure (<7%) come from search-engine extracts of those pages, not from a page I rendered myself. Treat as
  medium-confidence and re-verify if it becomes decision-critical.
- **Currency weights are by customer location, not invoicing currency.** Some Brazilian and Middle-East sales are
  USD-invoiced, which would make my Q3 FX estimate of +0.2% **too high** (i.e. FX could be a small net negative).
  My model calibrated to within 0.1pt on Q2, which limits but does not eliminate this bias.
- **No FRED access** (`fred.stlouisfed.org` CSV endpoint returned HTTP 403); FX monthly averages come from x-rates.com.
- **I could not decompose the PPA op-profit "Currency" bar** into translation vs transaction vs hedge; Deere does not
  disclose it. That is why the range on item 11 is wide.
