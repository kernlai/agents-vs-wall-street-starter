# Public-company dealer proxies for Deere's FY2026 Q3

**Prepared 16 August 2026. Deere has not reported FY2026 Q3 — the call is 09:00 US Central,
Thursday 20 August 2026. Nothing below is a Q3 FY2026 actual for Deere.**

Companion dataset: `dealer_proxies.csv` (1,090 rows, tidy long, 2011-01-31 → 2027-01-31).
Build scripts: `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/`
(`titn_xbrl_extract.py`, `titn_fetch_releases.py`, `titn_parse_releases.py`,
`tsco_fetch_comps.py`, `tsco_parse_comps.py`, `build_dealer_proxies.py`, `proxy_correlations.py`).

---

## 1. What each proxy measures — and what it does not

| Proxy | What it actually is | What it measures | What it does **not** measure |
|---|---|---|---|
| **Titan Machinery (Nasdaq: TITN)** | Full-service dealer for **CNH Industrial** — Case IH, New Holland, Case/New Holland Construction. 4 segments: Agriculture (US), Construction (US), Europe (Bulgaria/Romania/Ukraine), Australia. FY ends **31 January**. | US ag-**dealership economics**: equipment vs parts/service margin structure, floorplan carrying cost, equipment inventory turns, same-store retail demand, used-equipment overhang. | **Deere's own dealers.** TITN buys from CNH, is financed by CNH Industrial Capital, and takes CNH allocation decisions. Its inventory glut is evidence about the *industry channel*, not about Deere's dealer network. Its mix (≈13% Construction, ≈21% Europe+Australia in Q1 FY2027) is also not Deere's mix. |
| **Cervus Equipment (TSX: CERV)** | A **genuine John Deere dealer** — the largest Deere dealer group in Canada, plus Deere branches in Australia and New Zealand. Acquired by Brandt, delisted 2021. | The only public pure-ish **Deere-dealer** P&L that has ever existed. Calibrates what stressed vs healthy Deere-dealer economics look like: gross margin, used-equipment turnover, impairment intensity, finance cost. | **Anything current.** Last reported FY2020. Also not pure Deere-ag: the group carried Peterbilt (Transportation) and Bobcat/JCB (Industrial) alongside Deere agriculture. |
| **Tractor Supply (Nasdaq: TSCO)** | Rural-lifestyle **retailer** — feed, animal health, apparel, small tools, consumables. | Farmer/rural **discretionary spending** and rural household traffic. | Equipment demand, dealer inventory, floorplan, used values, or Deere shipments. TSCO carries no combines or high-hp tractors and has **no floorplan exposure at all**. Treat as sentiment colour only. |
| **Deere & Company (corpus)** | One quantitative datapoint from Deere's own Q2 FY2026 call. | Used equipment sitting on **Deere** dealer lots, via the John Deere Financial trade-wholesale portfolio. | Precision — management said "down over 15%", a floor, not a point estimate. |

### Listed dealers outside North America — searched, none usable
There is **no listed pure-play Deere dealer anywhere today**, and I did not find a usable one abroad.
Candidates checked and rejected, with the reason:

- **AFGRI Equipment** (South Africa + Western Australia) — a real and large Deere dealer, but AFGRI
  delisted from the JSE in 2014 and is private. No public financials.
- **Senwes Equipment** (South Africa) — a real Deere dealer; parent Senwes Ltd is only thinly
  traded off-JSE and I could not retrieve segment financials. No data extracted.
- **BayWa AG** (Xetra: BYW6) — large German ag-machinery dealer, but its machinery affiliation is
  principally **Claas/Fendt**, it is a diversified agri-conglomerate, and it has been in
  restructuring. Not a Deere read.
- **Vamos (B3: VAMO3)** — Brazilian dealership/leasing group; its ag dealerships are **Valtra
  (AGCO)** plus VW/MAN trucks and Komatsu. Not Deere; also predominantly a leasing business.
- **Seven Group Holdings (ASX: SVW)** — WesTrac is a **Caterpillar** dealer. Not Deere, not ag.

No financials are reported here for RDO Equipment, Ag-Pro, Van Wall, Sydenstricker Nobbe, Hutson,
Ziegler or Brandt. They are private and I have no data on them — deliberately blank rather than guessed.

---

## 2. Titan Machinery — the ag-dealership cycle, 28 quarters

All figures USD millions unless noted. Period ends are TITN's true fiscal quarter ends.
`P+S %GP` = share of total gross profit contributed by parts and service.
`turns` = TTM equipment cost of revenue ÷ period-end equipment inventory.

| Period end | FY/Q | Revenue | y/y | Equip rev | P+S rev | P+S %GP | Equip GM% | Turns | Floorplan payable | FP int %rev | Ag SSS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023-04-30 | FY24 Q1 | 570 | +23.6% | 429 | 132 | 45.6% | 14.2% | 2.26 | 443 | 0.22% | |
| 2023-07-31 | FY24 Q2 | 643 | +29.4% | 480 | 151 | 47.7% | 13.6% | 2.05 | 596 | 0.38% | |
| 2023-10-31 | FY24 Q3 | 694 | +3.8% | 522 | 160 | 48.3% | 12.9% | 1.84 | 706 | 0.58% | |
| 2024-01-31 | FY24 Q4 | 852 | +46.2% | 714 | 126 | 35.3% | 12.2% | 1.71 | 894 | 0.71% | |
| 2024-04-30 | FY25 Q1 | 629 | +10.4% | 468 | 153 | 52.1% | 11.9% | 1.56 | 1,025 | 1.12% | |
| **2024-07-31** | FY25 Q2 | 634 | −1.4% | 465 | 157 | 59.3% | 9.2% | **1.45** | **1,168** | 1.45% | −11.2% |
| 2024-10-31 | FY25 Q3 | 680 | −2.1% | 495 | 172 | 64.1% | 7.4% | 1.58 | 1,048 | 1.47% | −10.8% |
| **2025-01-31** | FY25 Q4 | 760 | −10.8% | 622 | 126 | **91.4%** | **0.3%** | 2.07 | 756 | 1.11% | −15.5% |
| 2025-04-30 | FY26 Q1 | 594 | −5.5% | 437 | 150 | 65.9% | 6.8% | 2.09 | 770 | 1.10% | −14.1% |
| 2025-07-31 | FY26 Q2 | 546 | −13.8% | 376 | 158 | 70.4% | 6.6% | 1.93 | 852 | 1.25% | −18.7% |
| 2025-10-31 | FY26 Q3 | 645 | −5.2% | 460 | 171 | 63.1% | 8.1% | 2.17 | 740 | 0.96% | −12.3% |
| 2026-01-31 | FY26 Q4 | 642 | −15.5% | 502 | 127 | 52.9% | 7.5% | 2.27 | 554 | 0.71% | −22.8% |
| **2026-04-30** | **FY27 Q1** | **522** | **−12.1%** | **365** | **148** | **64.8%** | **7.8%** | **2.14** | **589** | **0.68%** | **−8.2%** |

Full history back to FY2019 (revenue, gross profit, inventory, receivables, equity, total assets from
SEC XBRL) is in the CSV; product-line and floorplan detail begins FY2020 Q2, when the press-release
format stabilised.

### The destock is essentially finished
- Total inventory peaked at **$1,527.8m** (2024-07-31) and stands at **$914.8m** (2026-04-30):
  **−$613m, −40%**. Management's own framing on 19 March 2026: inventory "peaked in the second
  quarter of fiscal 2025, and over the next 18 months we reduced total inventory by $625 million."
- Floorplan payable halved: **$1,168m → $589m (−50%)**.
- Floorplan interest expense fell from **$10.0m** in the Sep–Nov 2024 quarter to **$3.55m** in
  Feb–Apr 2026 (−64%), and from **1.47% of revenue to 0.68%** — a fall in the carrying cost of
  channel inventory as large as the fall in the inventory itself.
- Equipment inventory turns bottomed at **1.45x** (Jul 2024) and have recovered to **2.14–2.27x**.
- Management explicitly stopped targeting further reduction: they "do not have further targeted
  reductions from an overall inventory level perspective as we head into fiscal 2027", shifting to
  **mix optimisation** instead.

### But the dealer P&L is still negative
- Q1 FY2027 net loss **$(12.6)m**; Agriculture segment pre-tax loss **$(6.2)m** (improved from
  $(12.8)m). Adjusted EBITDA **$1.0m** on $522m of revenue.
- FY2027 guidance, reaffirmed 9 June 2026: Agriculture revenue **down 15–20%**, adjusted net loss
  **$(28)–(40)m**, adjusted diluted LPS **$(1.25)–(1.75)**.
- Equipment gross margin recovered off a 0.3% floor (the Q4 FY2025 impairment quarter) to 7.8%,
  guided to ~8.4% for FY2027 vs 7.3% in FY2026 — better, but nowhere near the 12–14% of FY2023–24.

### Parts and service are carrying the dealer
Equipment revenue fell **16.5%** y/y in Q1 FY2027 while parts + service fell **1.4%**
($147.5m vs $149.6m). Parts margin has held in a tight **28.4–33.6%** band for six years and service
in the **53.9–68.0%** band, versus equipment swinging **0.3%–14.3%**. In the worst quarter
(Q4 FY2025) parts and service produced **91.4%** of all gross profit. Management's phrase for the
customer behaviour behind this is a **"fix-as-fail mentality"**.

### The one genuine inflection: used-equipment values have stopped falling
CEO Bryan Knutson, Q1 FY2027 earnings call, 9 June 2026:

> "We've seen stability in the used equipment prices after about 18 months of ... almost going on
> 2 years of sequentially falling used equipment values."

Aged inventory "continued to decline each month" through the quarter and is described as the
"critical leading indicator" of margin recovery. Used values are the trade-in currency for new
equipment sales, so this matters more than the headline revenue decline. It is corroborated on
Deere's own side: in the Q2 FY2026 call, management said the John Deere Financial trade-wholesale
portfolio — used equipment financed on **Deere** dealer lots — is "down over 15%" year on year.

---

## 3. Cervus Equipment — what a Deere dealer looks like stressed vs healthy

The only public pure-play Deere dealer that ever existed. CAD, calendar fiscal years.
Use these as **thresholds**, not as a current signal.

| Metric | FY2018 (peak) | FY2019 (**stressed**) | FY2020 (**recovered**) |
|---|---|---|---|
| Revenue | 1,350.0 | 1,139.0 (−16%) | 1,227.9 (+8%) |
| Equipment revenue | 1,041.8 | 813.4 (−22%) | 891.9 (+10%) |
| Product support (parts+service) | 308.2 | 325.6 (+6%) | 336.0 (+3%) |
| Gross margin | 15.5% | **14.9%** | **16.5%** |
| Inventory impairment | 11.5 | **24.0** (2.1% of revenue) | (−$20m y/y) |
| Income before tax | +34.1 | **−10.4** | +27.7 (adjusted) |
| Net income | +24.8 | −8.6 | +25.1 |
| EPS (basic) | +1.58 | −0.56 | +1.62 |
| Net finance costs | 5.5 | 12.4 (+125%) | −17% y/y |
| **Ag used-equipment turnover (TTM)** | | **1.78x** (1.62x at Jun-2019) | **2.87x** (target 2.50x) |
| Ag used-equipment inventory | | 114 (from a 181 peak at Jun-2019, −37%) | −58 y/y |

**The calibration:** a Deere dealer in distress runs gross margin **below ~15%**, negative pre-tax
income, used-equipment turnover **below 2x**, and takes impairments worth **~2% of revenue**. A
healthy one runs **16.5%+** gross margin and **~2.9x** used turns. Cervus stated an internal target
of **2.50x**.

Caveat on comparing to TITN: Cervus's 1.78x/2.87x is **used equipment only**. TITN's 2.14x in the
table above is **all equipment, new and used**. They are not the same ratio and should not be read
as directly comparable levels — only as within-company trajectories.

---

## 4. Tractor Supply — rural discretionary, labelled as such

| Quarter end | Comp store sales |
|---|---|
| 2022-12-31 | +8.6% |
| 2023-12-30 | −4.2% |
| 2024-09-28 | −0.2% |
| 2024-12-28 | +0.6% |
| 2025-03-29 | −0.9% |
| 2025-06-28 | +1.5% |
| 2025-09-27 | +3.9% |
| 2025-12-27 | +0.3% |
| 2026-03-28 | +0.5% |
| **2026-06-27** | **−1.5%** |

The Apr–Jun 2026 quarter is the **only public proxy datapoint that actually falls inside Deere's
FY2026 Q3 window**. Comps were −1.5%, with transactions −1.7% and average ticket +0.2%; management
attributed the decline to adverse May weather and said April and June were positive. Read: rural
discretionary is **flat, not collapsing**. That is weak evidence and it is not equipment demand.

---

## 5. How much do these proxies actually track Deere? (Pearson r, with n)

Proxy y/y growth vs Deere total net sales & revenues y/y growth (SEC XBRL, CIK 315189), paired on
nearest fiscal-quarter end within 45 days. Deere's Q4 (October) quarters are absent from XBRL
quarterly-duration facts because the 10-K reports annually, so those pairings drop out.

| Relationship | Lag | n | r | Verdict |
|---|---|---|---|---|
| TITN total revenue y/y | 0 | **44** | **0.63** | Best-supported relationship in the set. **Coincident, not leading** — r falls to 0.54 at +1q and 0.44 at +2q. |
| TITN Agriculture segment revenue y/y | 0 | 18 | 0.62 | Consistent with the above; shorter history. |
| TITN equipment revenue y/y | 0 | 18 | 0.53 | Weaker than total. |
| TITN total inventory y/y | 0 | 52 | **0.22** | **Essentially no relationship.** Channel inventory cycles are brand- and allocation-specific. Do not use TITN inventory to infer Deere dealer inventory. |
| TITN equipment turns (level) | +2q | 15 | 0.80 | **Likely spurious.** n=15 spans a single cycle, so this is ~1 independent observation of one downturn, not 15. |
| TITN Ag same-store sales | 0 | **6** | −0.26 | **Too few points. Anecdote only.** Sign is unstable across lags (−0.26 / −0.42 / −0.72). |
| TSCO comparable store sales | +1q | 10 | 0.75 | **Likely spurious** — small n over a single trending window. |
| TSCO revenue y/y | 0 | **7** | 0.94 | **Almost certainly a trend artifact.** TSCO revenue grows steadily 4–7%; Deere swings ±20%. A 0.94 on 7 overlapping points sharing one downtrend is not information. Do not use. |

**Two limitations that bound all of the above.** First, the Deere series is **total** net sales and
revenues — it includes Construction & Forestry and Financial Services, so this is not a clean test
against Production & Precision Ag. TITN's Q1 FY2027 (Feb–Apr 2026, −12.1%) overlaps Deere's Q2 FY2026,
which Deere reported at **+5% total but −14% PPA**; the proxy plainly maps to PPA, not to the total.
Second, **overlapping y/y windows are autocorrelated**, so the effective sample is materially smaller
than n and no p-value is quoted.

---

## 6. Read for Deere FY2026 Q3

**Timing problem, stated plainly.** TITN's most recent quarter (Feb–Apr 2026) overlaps Deere's
**Q2** FY2026, not Q3. TITN's Q2 FY2027 covers May–Jul 2026 and will be reported in late August 2026 —
**after** Deere's 20 August call. **No equipment-dealer proxy covers Deere's Q3 FY2026 quarter.** The
only in-window public datapoint is TSCO's −1.5% comp, which is rural retail, not equipment.

Subject to that, the channel evidence points three ways:

1. **The destock headwind is largely spent — this removes downside, it does not add upside.** TITN
   inventory −40% from peak, floorplan −50%, turns back to ~2.2x, and management has publicly
   stopped targeting further reduction. Deere's own disclosures agree: combines at **12%** of
   trailing-12-month retail (vs 17% LY) and 100+hp tractors at **30%** (vs 31%). A channel this lean
   cannot absorb much more underproduction, so Q3 shipments should sit closer to retail than in the
   quarters when Deere was actively destocking. Expect less negative wedge between shipments and
   retail than in FY2025 — but note Deere flagged continued Brazilian combine underproduction
   specifically into Q3.

2. **Dealers remain unprofitable, so there is no restocking impulse in Q3.** TITN lost money at the
   consolidated and Ag-segment level again in Feb–Apr 2026 and guides to a full-year FY2027 adjusted
   net loss with Ag revenue **down 15–20%**. Against the Cervus calibration, this is squarely a
   stressed-dealer configuration: negative pre-tax income, equipment margin at 7.8% versus 12–14% in
   the good years. Loss-making dealers order to replace what they sell, not to build position. Any
   forecast that assumes Deere Q3 shipments are lifted by channel refill is unsupported by this data.

3. **The one forward-positive is used-equipment price stabilisation, and it lands too late for Q3.**
   Used values stopped falling around the turn of 2026 after ~18–24 months of sequential decline, and
   Deere's JDF trade-wholesale used portfolio is down over 15% y/y. Stabilised trade-in values unlock
   new-equipment transactions, which is why both Deere and TITN management talk about recovery "next
   year." That supports the FY2027 setup and Deere's own baseline of "some level of recovery in the
   next year" — it does not move Q3 FY2026 shipments.

**Where the channel data creates tension with guidance.** Deere's FY2026 PPA guidance is **−5% to
−10%** with H1 actuals at −16% (Q1) and −14% (Q2). Getting to the guided range requires a materially
better H2. Nothing in the dealer channel supports a demand-driven H2 improvement: AEM US tractor
retail is −18.4% y/y in June and −17.3% across May–Jul, and TITN guides Ag down 15–20% for a fiscal
year running to January 2027. If Deere's H2 does improve, the channel evidence says it will be
**comparison-driven and mix/underproduction-driven, not demand-driven** — Q3 FY2025 was already a
−16% PPA quarter. That distinction matters for how durable any Q3 beat would be.

**Practical guidance for the forecast.** Use TITN as a **coincident read on PPA-type revenue
direction** (r≈0.63, n=44), never on Deere's dealer inventory (r≈0.22, n=52). Use the parts-and-
service resilience — TITN P&S −1.4% y/y against equipment −16.5% — as support for the aftermarket
component of Deere revenue holding far better than whole goods. Use Cervus's thresholds (15% gross
margin, 2x used turns) to judge stress, and treat TSCO as sentiment only.

---

## 7. Data quality and gaps

**Complete and machine-extracted.** TITN's XBRL series (revenue, gross profit, operating income,
net income, inventories, receivables, equity, assets) runs 2011-01-31 → 2026-04-30 from SEC
companyfacts. Product-line revenue/COGS, floorplan payable, floorplan interest and segment revenue
were parsed from 27 8-K EX-99.1 earnings releases covering FY2020 Q2 → FY2027 Q1. Line-item revenue
sums were cross-checked against the XBRL totals and tie exactly for every quarter tested.

**Known gaps, left blank rather than filled.**
- TITN product-line detail before FY2020 Q2: the pre-2019 press releases use a one-cell-per-line
  HTML layout the parser does not read. XBRL totals cover the period; the equipment/parts/service
  split does not.
- Two TITN Q4 press releases (FY2019, FY2020) had no matching EX-99.1 at the expected path.
- TITN same-store sales exists for only **8 Agriculture and 10 Construction** quarters — the company
  only began disclosing it per segment consistently from FY2025. Earlier quarters were genuinely not
  disclosed; they are absent rows, not zeros.
- TITN discloses no same-store sales for Europe or Australia at all.
- Cervus: annual figures only, FY2018–FY2020, transcribed from two dated press releases (SEDAR
  filings were not retrievable). No quarterly Cervus series was built. Cervus balance-sheet detail
  beyond used-equipment inventory and turnover was not recovered.
- No financials for any private Deere dealer group, and none for AFGRI or Senwes.
- TSCO comps: 15 quarters recovered; three quarters (including Q3 CY2023 and Q1 CY2024's transaction
  and ticket splits) were not parsed cleanly and are absent.
- Deere quarterly revenue used for correlations omits every fiscal Q4, because the 10-K carries only
  annual duration facts.

**One value that is directional, not exact.** Deere's JDF trade-wholesale used portfolio is recorded
at −15.0% because management said "down over 15%". It is a floor.

**Sources.** All corpus citations are relative paths under
`challenge/offline-data/deere/`. All web citations carry full URLs with publication dates in the
CSV's `source` column. SEC data is cited by CIK, concept, form and filing date.
