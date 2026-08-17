# Deere Dealer Network Structure and Consolidation Dynamics

**Prepared 16 August 2026.** Deere has **not** reported FY2026 Q3; the Q3 earnings call is 09:00 US Central,
Thursday 20 August 2026. Nothing in this document is a Q3 FY2026 actual. Corpus frozen 2026-08-14;
non-corpus facts carry full URLs and publication dates.

Data: `dealer_network.csv` (111 rows, 37 series).
Scripts: `/Users/cor/Documents/projects/agents-vs-wall-street-starter/scripts/data/parse_deere_dealer_network.py`
(extraction + reconciliation proof) and `build_deere_dealer_network_csv.py` (CSV assembly).

---

## 1. Headline: the network is not shrinking. The *ownership* of it is concentrating.

This is the single most important correction this workstream produces. The intuitive story —
"Deere consolidated its dealers, so there are fewer of them" — is **wrong at the location level**.
Deere's 10-K Item 1 distribution paragraph gives an eleven-year run of US-and-Canada dealer counts:

| FY | Ag locations | C&F locations | **Ag + C&F (comparable)** | Turf-only | Roadbuilding-only | As-reported total |
|---|---|---|---|---|---|---|
| 2015 | 1,522 | 427 | **1,949** | 432 | — | 2,381 |
| 2016 | 1,522 | 424 | **1,946** | 419 | — | 2,365 |
| 2017 | 1,532 | 424 | **1,956** | 403 | — | 2,359 |
| 2018 | 1,539 | 430 | **1,969** | 392 | — | 1,981 |
| 2019 | 1,541 | 436 | **1,977** | 375 | — | 1,977 |
| 2020 | 1,544 | 437 | **1,981** | 358 | — | 1,981 |
| 2021 | 1,545 | 445 | **1,990** | 340 | 125 | 1,990 |
| 2022 | 1,552 | 455 | **2,007** | 321 | 114 | 2,007 |
| 2023 | 1,600 | 450 | **2,050** | 280 | 90 | 2,050 |
| 2024 | 1,600 | 450 | **2,050** | 280 | 100 | 2,050 |
| 2025 | 1,600 | 450 | **2,050** | 260 | 100 | 2,050 |

Source: FY2015–FY2025 10-Ks, e.g. `filings/2025-11-26__de-us-20251126-q4-10k__469216.md`.

Over a decade in which Deere pursued explicit dealer consolidation, **ag locations rose 1,522 → 1,600
(+5.1%)** and the comparable ag+C&F total rose **1,949 → 2,050 (+5.2%)**. Deere did not close stores.
It changed who owns them.

### A definitional trap in the raw series — do not report the as-reported total as a trend

The as-reported headline appears to collapse from 2,359 (FY2017) to 1,981 (FY2018), a fake ‑16% drop.
It is a definition change, and the parser proves it by exact arithmetic:

- FY2017: 1,532 ag + 424 C&F + 403 turf-only = **2,359 = reported total** (turf-only *included*)
- FY2018: 1,539 ag + 430 C&F = 1,969 ≈ **1,981 reported** (turf-only *excluded*; 392 turf-only sit outside)

Every year FY2015–FY2017 reconciles to zero against ag+C&F+turf; every year FY2019–FY2025 reconciles to
zero against ag+C&F alone. Anyone plotting the as-reported column straight through will manufacture a
2018 dealer collapse that did not happen. The CSV therefore carries both the as-reported figure (flagged
non-comparable) and a derived `deere_dealer_loc_us_ca_core_ag_cf` series that is clean end-to-end.

**The one genuine contraction is turf: 432 → 260 locations, ‑39.8%.** That is a real channel exit, but it
sits in Small Ag & Turf's low-margin consumer end, not in the large-ag channel that drives PPA.

## 2. Where the consolidation actually shows up: groups, not rooftops

Deere does **not** disclose a dealer *group* count in any filing in the corpus. Three partial reads exist:

- **~170 US Deere ag dealer groups (early 2022, derived, order-of-magnitude).** U.S. PIRG Education Fund,
  *Deere in the Headlights II*, Feb 2022, counted 1,357 US Deere ag dealership locations from Deere's own
  locator and reported one Deere chain per 12,018 farms and per 5.3m acres of farmland. Three independent
  routes converge: 2.0m US farms ÷ 12,018 ≈ 166; ~897m acres ÷ 5.3m ≈ 169; 1,357 locations ÷ ~8 sites per
  chain ≈ 170. Treat as ~170, not exact.
  <https://publicinterestnetwork.org/wp-content/uploads/2022/02/Deere-In-The-Headlights-II.pdf>
- **82% of US Deere ag locations sit in chains of 7+ stores**; average Deere chain ~8 sites; largest chain
  67 locations. Deere is the most consolidated of the four majors — comparators: largest Case IH chain 57,
  AGCO 31, Kubota 6. Eighteen of the twenty largest US ag dealer chains carry Deere. (Same source.)
- **1,500 dealers financed globally by John Deere Financial** — JDF investor day, 8 Dec 2025
  (`call-transcripts/2025-12-08__de-us-20251208-call-pres-2__384036.md`): "about a million customers who we
  serve through 1,500 dealers", across 50+ countries with a $65bn portfolio. This counts dealer *entities*,
  not locations, and is the best available proxy for a global dealer-group count.

**Concentration among the largest groups (derived).** Farm Equipment / Ag Equipment Intelligence's ranking
of North America's largest machinery dealers (June 2024) lists eight Deere groups in the top ten, holding
97 + 84 + 48 + 33 + 32 + 30 + 28 + 26 = **378 ag stores ≈ 23.6% of Deere's ~1,600 US+Canada ag locations**.
That understates true concentration, because RDO Equipment — widely described as the largest Deere dealer
overall — is not in that ag-ranked top ten (its footprint is heavily construction/forestry).
<https://www.nationalbeefwire.com/farm-equipment-magazine-reports-the-10-largest-machinery-dealers>

**The top-100 groups are now shrinking their store count slightly.** Farm Equipment's 2026 update (4th
annual, ~May 2026) puts the 100 largest dealer groups at **2,001 ag stores, down 11 vs the 2025 report**,
about one-third of all North American ag rooftops (all brands).
<https://www.farm-equipment.com/articles/25326-2026-update-shows-numerous-shifts-among-north-americas-largest-dealer-groups>

### Largest Deere dealer groups — what is genuinely public

Every one of these is **private**. Store counts come from trade-press rankings; revenue is *banded* by the
trade press, not disclosed by the companies, and is recorded in the CSV as commentary rather than as a
financial fact. Data-broker "revenue" figures (RocketReach, Growjo, ZoomInfo, PitchBook estimates) were
found during research and are **deliberately excluded** — they are unverified model output.

| Group | Deere? | Ag stores | HQ | Public financials |
|---|---|---|---|---|
| United Ag & Turf | Yes | 97 | Waco, TX | None |
| Ag-Pro Companies | Yes | 84 | Boston, GA | None |
| Papé / Pape Machinery | Yes | 48 | Eugene, OR | None |
| RDO Equipment Co. | Yes | 42 ag (>85 total, 12 states) | Fargo, ND | None |
| Van Wall Equipment | Yes | 33 | Perry, IA | None |
| AgriVision / PrairieLand | Yes | 32 | Winterset, IA | None |
| Hutson Inc. | Yes | 30 | Murray, KY | None |
| James River Equipment | Yes | 28 | Ashland, VA | None |
| Sloan Implement | Yes | 26 | Assumption, IL | None |
| Sydenstricker Nobbe Partners | Yes | not disclosed | MO/IL | None |
| Ziegler Companies | Partly (primarily Caterpillar) | not disclosed | Bloomington, MN | None |
| Brandt (Canada) | Yes | not disclosed | Regina, SK | None |
| *Titan Machinery (TITN)* | **No — CNH** | 71 | West Fargo, ND | Public (CNH signal, not Deere) |
| *Rocky Mountain Equipment* | **No — CNH** | 42 | Calgary, AB | — |

**There is no listed pure-play North American Deere dealer.** Brandt acquired Cervus Equipment in 2021,
retiring the last one; Cervus filings are useful only pre-2021. Titan Machinery is a Case IH / New Holland
dealer and is a valid ag-*channel* proxy but **not a Deere signal**. Deere's own disclosures remain the
best quantitative source on its dealers.

## 3. Dealer M&A, distress and the new antitrust ceiling (2025–2026)

| Date | Event | Locations | Character |
|---|---|---|---|
| 7 Jul 2026 (close targeted 3 Aug 2026) | RDO Equipment acquires True North Equipment's Deere ag locations (ND/MN), ~200 employees; subject to Deere approval | 8 transferred; RDO to 42 ag | Strategic, **not distressed** |
| Announced mid-Jan 2026; **abandoned**, file closed 1 May 2026 | Enns Bros. / Greenvalley Equipment merger, Manitoba — Competition Bureau review opened 23 Jan 2026, parties withdrew after "considerable roadblocks and delays" | 13 combined | **Blocked in effect** |
| Effective 30 Nov 2026 | Horizon Ag & Turf / Battle River Implements, Alberta; Battle River rebrands to Horizon | 17 combined | Strategic, neither distressed |

Sources: <https://www.realagriculture.com/2026/07/rdo-announces-deal-to-acquire-true-north-john-deere-dealerships/>;
<https://www.manitobacooperator.ca/news-opinion/news/john-deere-dealer-chains-enns-bros-greenvalley-equipment-call-off-merger-competition-bureau/>;
<https://www.tractorzoompro.com/podcasts/market-insights-for-july-2026>

Two things matter here. First, **every completed 2026 deal is described by trade press as strategic scale-
building, not a rescue.** Consolidation continuing in a downturn *without* distress sales is a sign of a
network with capital, not one liquidating. Second, the **Enns/Greenvalley collapse is the first evidence in
this dataset of a regulatory ceiling on Deere dealer consolidation** — Canada's Competition Bureau
effectively stopped a 13-store Deere combination. Deere's decades-long consolidation lever now has a limit.

**Dealer bankruptcies: none found, recorded as blank rather than zero.** Targeted searches surfaced no
reported Deere dealer bankruptcy, liquidation or involuntary closure in 2025–2026. Private dealer
insolvencies are frequently unreported, so this is absence of evidence, not evidence of absence.

**Dealer lawsuits against Deere: none found.** The live litigation runs the other way — farmers and the
FTC suing Deere, with Deere's **affiliated dealerships named as co-defendants** in the class action.

## 4. Right to repair: the real question is who pays for the service bay

Two separate matters, both now resolved, neither hitting Q3 FY2026 earnings:

- **$99m class-action settlement** (proposed 6 Apr 2026, MDL filed Oct 2022, N.D. Ill.). Defendants are
  Deere **and its affiliated dealerships**. Class = purchasers of repair services for Deere large ag
  equipment from Deere or authorised dealers, 10 Jan 2018 → preliminary approval; plus interest at 3.95%/yr
  from 15 Jan 2026. **Accrued in Q4 FY2025** — already in the P&L, not a Q3 FY2026 charge.
  <https://nationalaglawcenter.org/john-deere-agrees-to-settle-antitrust-lawsuit/>
- **FTC + five state AGs settlement, 8 Jul 2026**, 10-year order with a four-year post-expiration
  enforcement window. Deere must supply farmers and independent repair providers the same repair
  resources — including software — as authorised dealers, on "fair and reasonable terms". Payment to states
  for litigation costs: **$1m**. The cost is behavioural, not monetary.
  <https://www.ftc.gov/news-events/news/press-releases/2026/07/ftc-states-secure-settlement-deere-company-advancing-farmers-right-repair>;
  <https://www.freshfields.com/en/our-thinking/blogs/a-fresh-take/ftcs-john-deere-settlement-signals-scrutiny-of-aftermarket-repair-restrictions-102nbqo>

Deere's Q2 FY2026 10-Q carries **$175m total accrued legal losses** at 3 May 2026, unchanged from Q1, and
explicitly says it is "unable to estimate the potential impact" of the FTC matter
(`filings/2026-05-21__de-us-20260521-q2-10q__1055929.md`). The $99m sits inside that $175m.

### Does this change dealer economics?

Parts and service is the most profitable line in a dealership and, as Deere's own management put it in 2017,
dealers "utilize parts and service to really cover a significant portion of their fixed costs, which help
them as they go through leaner complete goods years"
(`call-transcripts/2017-02-17__de-us-20170217-call-qna__1480475.md`). Anything that erodes that erodes the
shock absorber the whole consolidated-dealer thesis rests on. Three specific mechanisms:

1. **Loss of tooling exclusivity, on a rolling basis.** Once a repair resource reaches **more than 50% of
   Deere dealer locations**, equivalent access must be extended to farmers and independent providers. This
   is not a one-off unlock — every *future* dealer tool becomes a channel-wide obligation as it rolls out.
2. **Dealers are directly constrained, not just Deere.** Authorised dealers must *promote* the availability
   of repair resources and cannot "discriminate or retaliate in any way, including in the sales, financing,
   or servicing" against customers who self-repair. Dealers lose the soft levers that historically kept
   service work in-house.
3. **Dealers were co-defendants and the class period reaches back to Jan 2018**, so the reputational and
   pricing reset lands on the dealership, not only on Deere.

**But the magnitude is likely modest, and here is why.** The settlement mandates *access on fair and
reasonable terms* — explicitly priced with reference to dealer costs and competitor pricing — not free
access, and it does not touch parts distribution, warranty work, or the connected-machine service model
Deere has been building (Operations Center, connected solution centres). The bulk of dealer service revenue
is routine and warranty work on machines under finance, which farmers overwhelmingly still take to the
dealer. Expect **gradual margin pressure on out-of-warranty diagnostic and reprogramming work**, not a step
change. It is a slow leak in the shock absorber, not a puncture — and it operates over the 10-year order,
not over the next quarter.

## 5. Does consolidation change how a dealer-health signal should be read?

Yes, decisively, and in Deere's favour.

A network of ~170 groups averaging ~8 sites — with 82% of locations inside chains of 7+ — absorbs a
downturn very differently from a fragmented one. Large groups run pooled treasury, centralised used-
equipment desks, and multi-region diversification, so a bad year in one crop belt is netted against a
better one elsewhere. Crucially, **the observable stress indicators shift**: a fragmented network produces
bankruptcies and abrupt closures; a consolidated network produces *order deferral* and *floorplan
discipline* instead. The absence of dealer failures in 2025–2026 is therefore **weak evidence of health**,
because a consolidated network would not be expected to show failures even under real strain. The stronger
tells are inventory behaviour and wholesale receivable ageing.

On that, the evidence points to a de-levering, not a stressed, channel:

- **JDF trade wholesale — used-equipment financing sitting on dealer lots — is down over 15% y/y** as of
  Q2 FY2026 (21 May 2026 call): "That's less on their balance sheets that they've freed up and making more
  opportunity for new sales." (`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md`)
- Management on the same call: dealers "have also managed the cycle and the high interest rate environment
  very well and very profitably, supported by strong owner equity."
- Combine dealer inventories destocked to 12% of trailing-12-month retail (LY 17%); 100+hp 2WD tractors
  30% (LY 31%).

Against that, the channel-wide condition is genuinely poor:

- Dealer profitability at a **five-year low, ~30% below peak**; new machinery sales down 15–20% at most
  OEMs (Tractor Zoom Pro, July 2026).
- **72.5% of dealers forecast a profitable 2025 — "the lowest over the last 5 years by a significant
  margin"** (Ag Equipment Intelligence 2026 Dealer Business Outlook, 10 Jan 2026).
- **Nearly 50% of dealers said conditions worsened in Q2 2026**; 57% expect no change over the next twelve
  months (Sandhills Global / Bloomberg Intelligence Q2 2026 dealer survey, July 2026; sample size not
  published). This is the most recent dealer-sentiment read before Deere's Q3 print.
  <https://www.tractorhouse.com/blog/sandhills-news/2026/07/2026-q2-dealer-survey-farm-equipment-sentiment-weakens>

## 6. What this implies for Q3 FY2026

The forecast-relevant number in this workstream is not a location count. It is this:

> **Deere's own dealers forecast 2026 revenue down 7% — the largest decline of any brand's dealers,
> against ‑4% for the all-brand channel.**
> (Ag Equipment Intelligence / Farm Equipment 2026 Dealer Business Outlook, published Jan 2026:
> <https://www.farm-equipment.com/articles/25370-dealers-forecasting-2026-sales-revenue-down-4>)

Deere's reported revenue is *shipments to dealers*. A dealer planning for ‑7% retail, already destocked on
combines to 12% of trailing retail, sitting on 15%-lighter used-equipment floorplan and reporting worsening
conditions through Q2 2026, orders conservatively. Consolidation reinforces this rather than offsetting it:
large, well-capitalised, professionally-managed groups **do not panic-restock on the first sign of a
bottom** — they wait for confirmed retail traction. The same balance-sheet strength that prevents dealer
failure also makes dealers patient buyers.

Net read for Q3 FY2026 (quarter ending ~2 Aug 2026, reporting 20 Aug 2026): dealer network structure is
**mildly negative for the wholesale-shipment line and clearly positive for credit quality**. It supports
the low end of guided PPA (‑5% to ‑10% FY sales) rather than the high end, while arguing against any
dealer-driven credit deterioration in Financial Services. Right-to-repair is a non-event for the quarter:
the $99m was accrued in Q4 FY2025, the FTC order costs $1m plus compliance, and neither should move Q3 EPS.

The upside risk to watch is restocking timing. Combines at 12% of trailing retail are destocked well below
normal; when Deere and its dealers agree the bottom is in, a large consolidated network can rebuild
inventory faster than a fragmented one could. Management's Q2 language — "our baseline is we expect to see
some level of recovery in the next year" — puts that in FY2027, not in Q3 FY2026.

---

## Data quality and known gaps

- **Strong**: the FY2015–FY2025 dealer location series is from Deere's own 10-Ks, machine-extracted, and
  the definitional break is proven by exact arithmetic rather than asserted.
- **Derived, flagged**: the ~170 US dealer-group count, the 23.6% top-8 concentration share, and the 2025
  top-100 store count (2,012 = 2,001 + 11) are computed, not disclosed. All three are labelled
  `source_type=derived` in the CSV.
- **Not obtainable**: Deere publishes **no** dealer-group count, no dealer revenue, no dealer balance-sheet
  data, and no dealer-satisfaction survey. Every large Deere dealer group is private; none files with the
  SEC. Nine CSV rows carry blank values with explicit "NOT DISCLOSED" / "NOT ESTABLISHED" notes rather than
  zeros or estimates.
- **Weak / caveated**: private-group store counts and revenue bands are trade-press estimates (Farm
  Equipment / Ag Equipment Intelligence, June 2024) and may be stale by 1–2 years. The ScrapeHero US count
  of 2,240 Deere-branded locations (10 Aug 2026) is a scraped storefront census on a different definition
  from the 10-K and is a directional cross-check only. Dealer sentiment surveys do not publish sample sizes.
- **No correlations reported.** With eleven annual location observations and no matching dealer-financial
  series, any correlation between network structure and Deere revenue would be n≈11 against a strongly
  trending variable — spurious by construction. Not computed rather than reported with caveats.
- Several trade-press URLs (farm-equipment.com, pirg.org, tractorhouse.com) return HTTP 403 to automated
  fetches; those facts were taken from search-result extracts and, for PIRG, from the primary PDF
  downloaded directly. Figures sourced only from search extracts are noted as such in the CSV.
