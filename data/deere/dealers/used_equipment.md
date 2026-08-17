# Used equipment values & inventory — Deere dealer channel

**Prepared 16 August 2026. Deere has NOT reported FY2026 Q3; the Q3 call is 20 August 2026.
Nothing below is a Q3 FY2026 actual.**

Companion data: `/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/used_equipment.csv` (677 rows)
Build script: `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/build_used_equipment.py`

---

## 1. Why this series is the one to watch

Deere books revenue on **shipments to independent dealers**. A dealer only orders a new machine if
it can clear the trade-in. Used values and used inventory therefore sit one step upstream of the
revenue line:

```
used values ↓ → dealer's trade-in worth less than carried → dealer refuses the trade or eats a loss
            → the NEW sale dies → dealer orders less → Deere shipments ↓
```

Management says this in their own words. Q2 FY2026 call, 21 May 2026
(`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`):

> "structurally, we've seen the used inventory market, which has really been a governor slowing
> down replacement demand, get a lot healthier"

Q4 FY2025, 26 Nov 2025 (`call-transcripts/2025-11-26__de-us-20251126-call-q4-pres-2__361265.md`):

> "the continued reductions that we're seeing in used inventory levels are freeing up the market
> as the trade ladder gets healthier"

And the mechanism, quantified, from Q3 FY2023 (18 Aug 2023):

> "For every combine or tractor we sell, a dealer will typically facilitate 3-4 additional
> transactions as used equipment works its way down the trade ladder."

---

## 2. Headline: the used glut is over, and it broke in Deere's favour

Sandhills Global publishes a monthly US used-farm-equipment market report (inventory, asking values,
auction values, % M/M and % Y/Y). The turn is unambiguous.

**US used tractors 100+ hp**

| Data month | Inventory Y/Y | Asking Y/Y | Auction Y/Y | Auction M/M |
|---|---|---|---|---|
| Apr 2024 | **+58.3%** | +5.2% | −2.0% | −2.2% |
| Aug 2024 (trough) | +37.1% | −2.6% | **−13.1%** | −1.8% |
| Feb 2025 | +6.1% | −4.6% | −6.3% | −0.1% |
| Apr 2025 | +1.7% | −4.9% | −4.5% | −0.0% |
| Jul 2025 | −4.2% | −6.3% | −2.8% | −1.4% |
| Nov 2025 | −14.6% | −5.5% | −3.8% | +0.1% |
| Jan 2026 | −17.0% | −1.1% | **+1.9%** | +2.7% |
| Apr 2026 | −18.4% | −1.6% | +2.8% | +1.7% |
| **May 2026** | **−16.2%** | −1.8% | **+2.4%** | −0.9% |
| **Jun 2026** | **−16.7%** | −0.6% | **+3.7%** | +0.6% |
| **Jul 2026** | **−16.8%** | **−0.0%** | **+3.0%** | −1.6% |

Sources: monthly Sandhills reports, URLs in the CSV `source` column. July 2026 data published
2026-08-11 (https://www.monitordaily.com/sandhills-global-used-ag-equipment-inventories-continue-to-tighten-as-values-hold-steady/);
June 2026 data published 2026-07-06 (https://www.sandhills.com/news/article/250047595);
May 2026 data published 2026-06-04 (https://www.sandhills.com/news/article/250047334).

Read: high-horsepower used tractor inventory has fallen y/y for **14 consecutive months**; auction
values crossed into positive y/y in January 2026 and have stayed there; asking values have closed
almost the whole gap (from −6.3% y/y in mid-2025 to −0.04% y/y in July 2026). The 2024 glut — the
thing that was killing trade-ins — has cleared.

**US used combines** (the softer half of the story)

| Data month | Inventory Y/Y | Asking Y/Y | Auction Y/Y |
|---|---|---|---|
| Apr 2024 | +17.6% | +8.3% | −0.6% |
| Aug 2024 | +10.4% | +3.8% | −4.8% |
| Jul 2025 | −7.2% | +2.0% | **+9.6%** |
| Nov 2025 | −11.0% | −0.6% | +6.3% |
| Jan 2026 | −11.4% | −3.8% | +2.4% |
| Apr 2026 | −11.9% | +1.3% | +2.2% |
| **May 2026** | −10.1% | −1.2% | **+0.8%** |
| **Jun 2026** | −10.2% | −1.3% | **+0.7%** |
| **Jul 2026** | −11.8% | −1.7% | **+0.4%** |

Combine used inventory is down ~11% y/y, but the **auction-value tailwind has decayed from +9.6%
y/y (Jul 2025) to +0.4% y/y (Jul 2026)** — three consecutive months of negative M/M auction prints
in the May–July window. Combines are the used category where the pricing improvement has run out.

**Category spread, July 2026 data (the most recent print anywhere):**

| Category | Inventory M/M | Inventory Y/Y | Auction M/M | Auction Y/Y |
|---|---|---|---|---|
| Tractors 100+ hp | −2.04% | −16.75% | −1.55% | +2.97% |
| Combines | −3.29% | −11.79% | −0.49% | +0.38% |
| **Sprayers** | **+2.63%** | −19.29% | **−3.97%** | **−5.14%** |
| Planters | +9.11% | −15.88% | −1.12% | **+12.45%** |
| Compact & utility tractors | −1.34% | −25.47% | +0.41% | +2.02% |
| SP forage harvesters | +0.60% | −5.11% | −0.16% | +1.36% |

**Sprayers are the visible weak spot** — the only major category with both rising month-over-month
inventory and falling auction values on both bases. Sprayers sit inside Production & Precision Ag.

**Asking-vs-auction spread (Sandhills EVI): 32% in June 2026**, one point wider than May. Sellers'
asks still sit well above auction clearing levels. Below the 2015 cycle peak, but not a "cleared
market" signal.

---

## 3. Deere's own read: management's used-inventory commentary, dated

A qualitative time series built by searching every call transcript in the corpus for used-equipment
statements. The arc is a complete cycle.

| Date | Fiscal | What management said |
|---|---|---|
| 2019-11-27 | Q4 FY19 | "the overall used equipment market continues to be quite stable, our lease return rates remain at elevated levels" |
| 2020-02-21 | Q1 FY20 | "large ag used inventory levels are in their healthiest position in years" |
| 2020-11-25 | Q4 FY20 | "new and used inventory positions at multi-year lows" |
| 2021-05-21 | Q2 FY21 | "Current global inventory levels for both new and used equipment remain at historic lows" |
| 2021-08-20 | Q3 FY21 | "we've seen gains on the lease book the last few quarters … the upward price pressure we're seeing really across all categories of used equipment" |
| 2022-08-19 | Q3 FY22 | "Our new and used inventories for all large tractors are sitting at multi-year lows" |
| 2023-02-17 | Q1 FY23 | "used equipment inventories are at low levels and used equipment prices continue to be strong" — **the top** |
| 2023-08-18 | Q3 FY23 | "used inventories … rise pretty significantly year-over-year from their historic lows last year" |
| 2023-11-22 | Q4 FY23 | analyst: "used inventories are at absolute low level, but rising rapidly off the bottom"; Deere: "in the back half of 2023, we did increase our incentive spend on used" |
| 2024-05-16 | Q2 FY24 | "increases in used inventory levels, particularly late model year machines, are having an impact on purchase decisions" |
| 2024-08-15 | Q3 FY24 | "reduction in used inventories was our **number one priority** right now" — **the bottom** |
| 2024-11-21 | Q4 FY24 | "a significant concern heading into next year is North American used inventories"; "used inventory to new sales ratios starting to plateau just above the long term average" |
| 2025-02-13 | Q1 FY25 | "high horsepower tractor used inventory **peaked in November** [2024]"; combines "down over 10% from the recent peak in spring 2024 … around 60% of the prior cycle peak" |
| 2025-05-15 | Q2 FY25 | "a higher-than-normal mix of late-model year tractors continues to persist" |
| 2025-08-15 | Q3 FY25 | "**incremental pool funds we accrued during the quarter**"; "the negative price that you saw in the quarter was primarily driven by actions taken to address used inventory in North America" |
| 2025-11-26 | Q4 FY25 | MY22/MY23 8R used inventory "around 25% below the peak in March 2025"; Deere used combines "nearly 25% decrease from their spring 2024 peak"; model-year distribution "returned to a nearly normal level" |
| 2026-02-19 | Q1 FY26 | "improving used inventory market is providing a better environment for machine replacement"; MY22/23 8Rs "down more than 40%" from March 2025, "−20% sequentially in the quarter"; "**We've seen stability in used prices**" |
| 2026-05-21 | Q2 FY26 | used tractors "down mid-teens from this cycle's peak and **down low single digits sequentially** … a period that we typically see seasonal inventory builds"; MY22/23 8Rs "down around 45% from their peak levels last year"; sprayers −30%, planters −50% from recent peaks; JDF **trade wholesale portfolio "down over 15%"** y/y |

Source files are listed per-row in the CSV.

### The one place Deere's own numbers stopped improving

| Metric | Q4 FY25 (26 Nov 2025) | Q1 FY26 (19 Feb 2026) | Q2 FY26 (21 May 2026) |
|---|---|---|---|
| Deere used **combine** inventory vs Mar-2024 peak | −25% ("nearly 25%") | −15% ("about 15%") | −15% ("mid-teens") |
| Deere used **HHP tractor** inventory vs cycle peak | — | −10%+ vs Mar-2025 | −15% ("mid-teens") |
| MY22/23 **8R** vs peak | −25% vs Mar-2025 | −40%+ vs Mar-2025 | −45% vs peak a year ago |

Combine used inventory gave back ~10 points between Q4 FY2025 and Q1 FY2026 (seasonal rebuild) and
then **did not improve at all in Q2 FY2026**. Tractors kept destocking; combines stalled. That is
consistent with Sandhills combine auction values decaying to +0.4% y/y.

---

## 4. Lease residual exposure — real, disclosed, and small

Deere's financial services arm carries residual risk on operating leases. The 10-K discloses the
sensitivity directly.

**"If future market values for this equipment were to decrease 10% … the total unfavourable impact
after consideration of dealer residual value guarantees would be approximately $X":**

| FY | Sensitivity ($m) | Equipment on operating leases – net ($m) | Sensitivity as % of lease book |
|---|---|---|---|
| 2015 | 175 * | 4,970 | 3.5% |
| 2016 | 200 * | 5,902 | 3.4% |
| 2017 | 200 * | 6,594 | 3.0% |
| 2018 | 185 * | 7,165 | 2.6% |
| 2019 | 175 * | 7,567 | 2.3% |
| 2020 | 175 * | 7,298 | 2.4% |
| 2021 | **80** | 6,988 | 1.1% |
| 2022 | 40 | 6,623 | 0.6% |
| 2023 | 90 | 6,917 | 1.3% |
| 2024 | 75 | 7,451 | 1.0% |
| 2025 | **65** | 7,600 | 0.9% |

\* **Definition break at FY2021.** FY2015–FY2020 figures are stated as an increase in annual
depreciation *before* dealer residual value guarantees. From FY2021 the disclosure is stated *after*
dealer residual guarantees and assumes every unit is returned for remarketing. Do not read the
2020→2021 fall from $175m to $80m as a genuine 54% de-risking; most of it is the definition.
FY2021–FY2025 are internally comparable.

Source: `filings/2025-11-26__de-us-20251126-q4-10k__469216.md` and the corresponding prior 10-Ks.

**Sizing it against the FY2026 guide.** Financial services net income is guided to ~$860m. A
hypothetical 10% across-the-board fall in used values, with every leased unit returned, costs ~$65m
— **7.6% of the FS net income guide**, spread as higher depreciation over remaining lease terms
rather than as a single-quarter hit. That is the *tail* scenario. What is actually happening is the
opposite: used auction values are **up** 3.0% y/y on 100+hp tractors.

Two structural reasons the exposure is contained:
1. **Dealer residual value guarantees.** The dealer, not Deere, absorbs a first slice. This is also
   why residual risk is genuinely a *dealer*-health item, not just a Deere-P&L item.
2. **Deere shortened lease terms deliberately.** Q4 FY2023 call: "we've decreased the size of our
   leasing portfolio and limited leasing options to three to five year terms, eliminating short-term
   leases, which drove higher used inventory levels in the 2014-2016 period."

Related residual disclosures (FY2025 10-K): sales-type & direct financing leases carry **$867m
guaranteed** residual values (FY24: $921m) and only **$40m unguaranteed** (FY24: $55m). The
unguaranteed slice — the piece with no backstop at all — is trivially small and shrinking.

**Lease book is still growing but has plateaued.** Equipment on operating leases – net:
$7,157m (Q1 FY25) → $7,336m (Q2 FY25) → $7,512m (Q3 FY25) → $7,600m (FY25) → $7,512m (Q1 FY26) →
**$7,514m (Q2 FY26)**. Flat sequentially in Q2 FY2026. Six-month remarketing proceeds from lease
dispositions were $1,019m vs $1,001m a year earlier — no sign of distressed disposal.

**No residual impairment or write-down is disclosed in the Q2 FY2026 10-Q.** I searched
`filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` for "residual" and "impairment" in the lease
context and found no charge.

---

## 5. Dealer-health read

**Direction: improving on the balance sheet, still stressed on the income statement.**

Improving:
- Dealers are carrying materially less used iron. JDF **trade wholesale** (used equipment floorplanned
  on dealer lots) is **down over 15% y/y** as of Q2 FY2026 — the single hardest dealer-level number
  in the corpus on this topic.
- Used values are firm to rising: 100+hp tractor auction values +3.0% y/y (Jul 2026), asking values
  back to flat. Trade-ins are worth roughly what dealers carried them at. The write-down risk that
  dominated 2024 has gone.
- Late-model overhang cleared: MY2022/2023 8Rs down ~45% from peak. This was the specific cohort
  blocking trades, because a 2-year-old machine competes directly with a new one.
- Deere's pool-fund subsidy pressure should ease. In Q3 FY2025 Deere explicitly took **negative
  price realization in large ag** to fund used-inventory clearance; by Q1 FY2026 it was "still
  positive price for North America," and Q2 FY2026 PPA price realization was +1 point.

Not improving:
- Sandhills/Bloomberg Intelligence **Q2 2026 dealer survey** (published July 2026): dealer sentiment
  "took another leg down"; **nearly 50% of dealers reported conditions worsened** vs the prior
  quarter; 57% expect no change over the next 12 months.
  (https://www.tractorhouse.com/blog/sandhills-news/2026/07/2026-q2-dealer-survey-farm-equipment-sentiment-weakens)
- AEM US ag retail: tractors −18.4% y/y in June 2026, −17.3% across May–Jul. Dealers are selling far
  fewer units. Falling used inventory is *partly* an artefact of that: **fewer new sales means fewer
  trade-ins arriving**, so used inventory falls without any retail strength. Do not read the entire
  16% used-inventory decline as demand.
- Sprayer used values falling (−5.1% y/y auction, −4.0% M/M in July 2026) with inventory building
  M/M — a live pocket of trade-ladder friction inside PPA.

---

## 6. What this implies for Q3 FY2026 (quarter ended ~2 Aug 2026, reporting 20 Aug)

1. **No residual write-down should appear.** Used values rose through the quarter on the dominant
   category. The ~$860m financial-services net income guide is not at risk from this channel.
   The only categories with falling used values (sprayers, marginally combines) are too small to
   move a $65m/10% sensitivity.
2. **Large-ag price realization should be less bad than Q3 FY2025.** Q3 FY2025's negative large-ag
   price was explicitly attributed to used-inventory clearance actions (incremental pool funds).
   With used inventory down ~16% y/y and values firm, that spend has less work to do. Directionally
   supportive of the PPA margin holding in the 11–13% guided band despite volume declines.
3. **It does NOT rescue Q3 shipments.** Q3 volumes were locked by order books months ago — Waterloo
   large-tractor order books were already "well into the fourth quarter" as of 21 May 2026, and
   model-year 2026 seasonal production was set by closed early-order programs. Used-market health is
   an order-intake and FY2027 story; management said so explicitly ("our expectation still as a
   baseline … is that we see recovery in 2027").
4. **Watch the combine line on the call.** Deere's used combine inventory has been stuck at ~−15%
   vs the March 2024 peak for two consecutive quarters, and combine auction values have decelerated
   from +9.6% to +0.4% y/y. Combined with Brazilian combine underproduction in Q2 *and Q3*, combines
   are the segment most likely to disappoint within PPA.
5. **The asymmetry is in commentary, not numbers.** If management repeats the used-market improvement
   framing with fresh quantification (8R cohort down further, trade wholesale down more), it
   strengthens the FY2027 recovery case that supports the multiple, without changing FY2026 revenue.

---

## 7. Data quality, gaps, and traps handled

**Coverage achieved:** monthly Sandhills used-equipment data for 14 data months spanning Apr 2024 –
Jul 2026, plus a Sept 2022 cycle-peak anchor; six categories; three measures each (inventory, asking,
auction) on both M/M and Y/Y. Deere lease-residual sensitivity annually FY2015–FY2025. Equipment on
operating leases annually FY2014–FY2025 and quarterly FY2024 Q1 – FY2026 Q2. Eleven quantified
management used-inventory disclosures Q1 FY2025 – Q2 FY2026. FRED WPU111 monthly Dec 2018 – Jul 2026.

**Gaps — stated, not filled:**
- **2019–2021 used-value indices are missing.** Sandhills' public monthly report archive that I could
  reach starts effectively in 2022; the task asked for 2019–2026 coverage and I have quantitative
  index data only from Sept 2022 forward, with the dense run beginning Apr 2024. The 2019–2021 period
  is covered **qualitatively only**, from Deere transcripts (section 3). I did not interpolate.
- **March 2026 Sandhills data is absent** — the TractorHouse and Sandhills pages for that report
  returned HTTP 403. A blank, not a guess.
- **Tractor Zoom's Used Farm Equipment Index has no retrievable dated levels.** I found the index
  description and a January 2026 reference (used high-hp tractors +1.5% M/M, −9.22% y/y) but could
  not verify the source page directly, so it is **not** in the CSV.
- **Machinery Pete figures are excluded from the CSV.** Search results surfaced specific values
  (e.g. used John Deere X9 combines averaging ~$522,400 at auction vs "well under $500,000" a year
  earlier; a 2022 Case IH 9250 at $280,000 in late June 2026) but the AgWeb source pages returned
  HTTP 403 and I could not confirm publication dates. They are directionally consistent with
  Sandhills and are recorded here as **unverified colour only**.
- **No public pure-play North American Deere dealer exists.** Cervus was acquired by Brandt in 2021.
  RDO, Ag-Pro, Van Wall, Sydenstricker Nobbe, Hutson and Ziegler are private and I fabricated nothing
  for them. Titan Machinery (TITN) is a **CNH** dealer, not a Deere dealer, and is not used here.
- **No Q3 FY2026 Deere actuals exist and none are reported.**

**Traps handled:**
- INDEX.md's row labelled "2026-05-21 | Call Transcript | Q3 2026" is mislabelled **Q2 FY2026**
  material. Treated as Q2 throughout.
- **A search engine returned July-2025 Sandhills figures as though they were July 2026.** The
  snippet gave 100+hp tractor asking −1.37% M/M / −6.28% Y/Y and auction −1.35% M/M / −2.83% Y/Y
  "in July" — those are byte-identical to the **August 2025** publication covering July 2025 data.
  I discarded them and used the verified 2026-08-11 publication instead (asking −0.44% / −0.04%,
  auction −1.55% / **+2.97%**). This matters enormously: the bogus figures say used tractor values
  are falling; the real July 2026 figures say they are up ~3% y/y. Anyone reading the snippet would
  reach the opposite conclusion about residual risk.

**No correlations reported.** With 14 monthly Sandhills observations against 8–9 usable Deere
quarters, any correlation between used-value indices and PPA sales would rest on n < 10 with heavy
serial correlation in both series. Computing one would be spurious precision. The relationship is
asserted here on the disclosed causal mechanism (trade ladder, pool funds, management's own
statements), not on a regression.

**Fiscal mapping convention:** monthly observations carry `period_end` = last day of the data month
and are assigned to the Deere fiscal quarter containing the month's midpoint. May, June and July 2026
therefore all map to **FY2026 Q3** — the quarter being forecast.
