# Deere & Company — Supply Chain Map & Production Signal (FY2026 Q3 forecast input)

**Prepared:** 16 August 2026 · **Agent:** supply-chain-map · **Forecast target:** DE FY2026 Q3 (fiscal quarter ended ~2 Aug 2026), reporting **Thursday 20 August 2026**.

**Corpus root (relative paths below are relative to this root):**
`/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`

## 0. Metadata trap — explicit statement

The corpus `INDEX.md` line 16 lists:

> `| 2026-05-21 | Call Transcript | Q3 2026 | Q3 2026 Earnings Call Transcript | call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md |`

I opened this file. Its YAML header carries `period: "Q3 2026"` and `published_at: "2026-05-21"`, but the **body is unambiguously the Q2 FY2026 earnings-call Q&A**: it discusses the $272M IEEPA tariff refund recognised "in the quarter" (recorded in Q2 per the 21 May 8-K), sprayer Early Order Programs that "opened up at the beginning of May", and asks management to "talk us through the cadence for 3Q and 4Q" as *future* periods. It is **mislabelled Q2 material**. I found **no FY2026 Q3 actuals anywhere in the corpus or on the web** — nothing in this document is a Q3 FY2026 reported result.

---

## 1. Executive read-through (the part that moves the forecast)

| Signal | Direction for Q3 FY2026 | Confidence |
|---|---|---|
| **No Deere WARN layoff filings anywhere in 2026 YTD** (most recent: 17 Sep 2025). Instead ~245 workers *recalled* Jan–Mar 2026 across Waterloo/Davenport/Dubuque, explicitly "driven by increased customer demand". | **Positive** — no production cut announced into or during the May–Jul window | High |
| Management guided Q3 < Q4 on both revenue and margin; Waterloo large-tractor NA shipments deliberately **back-half and Q4-weighted**, with "production rates significantly higher" in Q4 and better overhead absorption *in Q4, not Q3* | **Caps Q3 PPA upside** — Q3 is the weaker of the two back-half quarters | High (company guidance) |
| **Brazil combines: explicit plan to underproduce retail demand in fiscal Q2 *and Q3*** | **Negative for PPA Q3 volume** — a named, quantifiable production cut inside the window | High (company statement) |
| SAT guided to a **sequential step-down in Q3** and again in Q4 (normal seasonality); C&F "fairly balanced" Q3 vs Q4 | Mixed | High |
| Freight cost shock from the 2026 Iran war / Strait of Hormuz closure hit hardest **in the Q3 window** (Asia–US container spot +19–22% m/m by late April; Hormuz effectively closed as at 30 Jul 2026) | **Negative for production costs / PPA margin** | Medium |
| Tariff run-rate unchanged at ~$1.2bn gross FY26 (~$900m net of the $272m refund), ~3 margin points full-year; but Q3/Q4 comps *improve* because H2 FY2025 already carried tariffs and tariff-driven indirect inflation | **Mildly positive vs. H1 price/cost** | High (company statement) |
| **UAW: zero strike risk in the quarter.** Master agreement runs to 1 Nov 2027; the contract-*extension* ratification vote is 23 Aug 2026 — three days *after* the Q3 print | **Neutral for Q3; a headline risk for the print week** | High |
| No semiconductor, rare-earth or supplier-insolvency disruption attributable to Deere found in the window | Neutral | Medium (absence of evidence) |

**Net inference (mine, not company-stated):** the supply chain was a **cost** problem in Q3 FY2026, not a **volume** problem. There is no evidence of a Deere-specific production interruption in May–July 2026, and the labour data points the other way (recalls, not layoffs). The volume constraint on PPA in Q3 is *self-imposed and demand-driven* — Brazilian combine underproduction plus the deliberate Q4-weighting of Waterloo large tractors — not supply-side.

---

## 2. The supply chain map

### 2.1 What Deere itself says it buys (REPORTED FACT)

From `filings/2025-12-18__de-us-20251218-fy-10k__393777.md` (FY2025 Form 10-K, "Raw Materials", lines 369–377):

> Deere sources "a variety of steel products, metal castings, forgings, plastics, hydraulics, electronics, and ready-to-assemble components made to certain specifications" from "leading suppliers globally."

Stated mitigation playbook (same source, line 377): prioritised allocations with the supply base, **multi-sourcing selected parts**, **long-term contracts for some critical components**, and **alternative freight carriers to expedite delivery**.

Named supply-chain risk vectors monitored (line 375): supplier financial viability, capacity, business continuity, labour availability, quality, delivery, cybersecurity, weather, natural disasters, geopolitical instability, trade policies.

**Rare earths — the one named single-geography dependency:** 10-K line 657 states that "certain of our products, including motors, batteries, and other components, rely on rare earth minerals for their manufacturing, of which a significant majority are sourced from China. The inability to obtain export permits for rare earth minerals could have a detrimental effect on our business."

**Import geography:** "Nearly 80% of our domestic sales are assembled in the U.S., with the remaining products imported primarily from **Europe, Mexico, India, and Japan**" (10-K line 559 / line 1350). Deere told reporters at Q2 that roughly **80% of products are made at U.S. facilities and ~75% of components are sourced domestically** ([Supply Chain Dive, 4 Jun 2026](https://www.supplychaindive.com/news/deere-recovers-272m-in-tariff-refunds/821818/)).

### 2.2 Vertical integration — what Deere makes itself (REPORTED FACT)

This matters: Deere is unusually vertically integrated for engines, drivetrain, castings, control electronics and GNSS, which materially *reduces* its exposure to the classic third-party bottlenecks.

| Sub-system | In-house asset | Source |
|---|---|---|
| **Diesel engines** | John Deere Engine Works (Waterloo IA); Saran Engine Factory (France); Torreón Engine Factory (Mexico); Pune Works (India) | 10-K Item 2 Properties, `filings/2025-12-18…10k` lines 1006–1035 |
| **Drivetrain / powertrain** | Waterloo Drive Train Operations (named in the Feb 2026 recall notice); Deere also **sells** engines, power trains and electronic components to third-party OEMs | 10-K lines 335, 365; [CBS2 Iowa, 6 Feb 2026](https://cbs2iowa.com/news/local/john-deere-announces-146-waterloo-worker-callbacks-citing-increased-production-demand) |
| **Castings** | John Deere Waterloo Foundry (a separately-listed significant property) | 10-K Item 2 Properties |
| **Cylinders / seeding** | John Deere Seeding & Cylinder, Moline IL | [The Gazette / WARN reporting, Aug 2025](https://www.thegazette.com/business/john-deere-to-lay-off-more-than-200-employees-across-three-factories/article_25d409a4-afc3-5232-8ef1-3026452fb46a.html) |
| **Control electronics** | Phoenix International (acquired 1999) — John Deere Electronic Solutions | `call-transcripts/2020-11-25__de-us-20201125-call-pres__46441.md` line 49 |
| **GNSS / precision guidance** | NavCom Technology (acquired 1999) — "a foundational element to our tech stack… AutoTrac… AutoPath" | `call-transcripts/2020-11-25__de-us-20201125-call-pres__46441.md` line 47 |
| **Computer vision / See & Spray** | Blue River Technology (acquired 2017) | `call-transcripts/2020-11-25…` line 49; `2020-01-08…call-pres-2__1340209.md` lines 49–53 |
| **Autonomy** | Bear Flag Robotics (acquired 2021) | `call-transcripts/2021-11-24__de-us-20211124-call-qna__46439.md` line 47 |
| **Batteries / electrification** | Kreisel Electric (2022; put/call on remaining minority interest exercisable **2027**) | `filings/2025-12-18…10k` line 3078 |
| **Excavators (was a JV)** | Deere bought out Hitachi Construction Machinery from the Deere-Hitachi JV in 2022; a clean-sheet Deere excavator launched at CONEXPO in FY2026, and excavator production started at Kernersville NC in Q2 FY2026 | `call-transcripts/2023-02-17…call-qna__46468.md` line 99; `call-transcripts/2026-02-19…call-qna__605077.md` line 147 |

### 2.3 Named external suppliers and partners — verified

| Category | Supplier | Evidence | Grade |
|---|---|---|---|
| **Tyres / wheels** | **Titan International (TWI)** — Deere is/was Titan's single largest customer. Titan's SEC filings disclose Deere at **22% (FY2004), 20% (FY2005), 17% (FY2006), 26% (FY2010)** of Titan consolidated revenue; agricultural was ~52% of Titan net sales in FY2025, serving "John Deere, CNH Industrial and AGCO" | [Titan 10-K FY2006](https://www.sec.gov/Archives/edgar/data/0000899751/000089975107000020/form10k.htm), [Titan 10-K FY2010](https://www.sec.gov/Archives/edgar/data/0000899751/000089975111000007/form10k.htm), [Titan FY2025 results, 28 Feb 2026](https://www.prnewswire.com/news-releases/titan-international-inc-reports-fourth-quarter-and-fiscal-year-2025-financial-performance-302697570.html) | Reported fact (Titan's own filings); the FY2025 Deere-specific % is **not found** |
| **Hydraulics / fluid power** | **Helios Technologies** (Sun Hydraulics / Enovation Controls) — recipient of a John Deere Supplier Innovation Award | [Helios Technologies press release](https://www.heliostechnologies.com/news/press-releases/detail/186/helios-technologies-subsidiary-receives-john-deere-supplier) | Reported fact (supplier's own release) |
| **Satellite connectivity (precision ag)** | **SpaceX / Starlink** — powers JDLink Boost; 12,500+ kits sold since H2 2024, +25% in Q2 FY2026 alone | `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` line 163; `call-transcripts/2025-02-13__de-us-20250213-call-q1-qna__46478.md` line 45 | Reported fact |
| **Excavator products (legacy)** | **Hitachi Construction Machinery** — "long-standing relationship with Hitachi, with good products", now being displaced by Deere's own machine | `call-transcripts/2026-02-19__de-us-20260219-call-qna__605077.md` line 147 | Reported fact |
| **Coatings** | **Sherwin-Williams General Industrial** — 2026 John Deere Partner-level supplier and Indirect Global Supplier of the Year | [PR Newswire / farm-equipment.com, May 2026](https://www.farm-equipment.com/articles/25337-sherwin-williams-recognized-as-a-john-deere-partner-level-supplier-and-supplier-of-the-year) | Reported fact |
| **Metalworking fluids** | **Quaker Houghton** — 2026 Partner-level supplier | [The Fabricator](https://www.thefabricator.com/thefabricator/news/consumables/quaker-houghton-recognized-as-a-john-deere-partner-level-supplier) | Reported fact |
| **Freight / logistics (3PL)** | **Ascent Global Logistics** — John Deere Partner-level supplier for the **11th consecutive year** (announced 7 May 2026, i.e. inside the Q3 window) | [ChartMill/PR, 7 May 2026](https://www.chartmill.com/news/DE/prnews-2026-5-7-ascent-global-logistics-earns-recognition-as-a-john-deere-partner-level-supplier-for-the-11th-consecutive-year) | Reported fact |
| **IT / software engineering** | **Thoughtworks** — 2026 Partner-level supplier | [PR Newswire, 2026](https://www.prnewswire.com/news-releases/thoughtworks-recognized-as-john-deere-partner-level-supplier-in-2026-achieving-excellence-program-302782477.html) | Reported fact |

Deere runs a public supplier portal, **John Deere Supply Network (JDSN)**, at `https://jdsn.deere.com` — access is gated to registered suppliers, so no bill-of-materials-level supplier roster is publicly extractable.

### 2.4 Categories where I could NOT verify a named supplier — flagged as gaps

I deliberately do **not** assert the following, because I could not source them in this research window. Widely repeated trade-press attributions exist for hydraulics (Bosch Rexroth, Parker Hannifin, Danfoss Power Solutions, HUSCO), axles/transmissions (ZF, Dana, Carraro, Comer), tyres (Bridgestone/Firestone, Michelin, Trelleborg), semiconductors (NXP, Infineon, TI, Renesas, STMicro) and steel (Nucor, Cleveland-Cliffs, SSAB) — **none of these were confirmed by a primary source during this research and should be treated as unverified.** See §7.

---

## 3. Deere's manufacturing footprint

**Scale (REPORTED FACT, FY2025 10-K Item 2, `filings/2025-12-18…10k` line 997):** in the U.S. and Canada, equipment operations own/operate **23 factory locations** plus 4 leased manufacturing sites and 12 distribution facilities. Outside the U.S. and Canada, **45 factory locations** and 13 distribution facilities.

**Significant manufacturing properties as of 2 November 2025** (verbatim from the 10-K Item 2 table):

| Location | Facility | Segment |
|---|---|---|
| Augusta, Georgia | John Deere Augusta Works | SAT |
| Catalão, Brazil | John Deere Brasil Ltda (Catalão) | **PPA** |
| Davenport, Iowa | John Deere Davenport Works | CF |
| Des Moines, Iowa | John Deere Des Moines Works | **PPA** |
| Dubuque, Iowa | John Deere Dubuque Works | CF |
| East Moline, Illinois | John Deere Harvester Works | **PPA** |
| Joensuu, Finland | Finland Forestry Factory | CF |
| Fuquay, North Carolina | John Deere Turf Care | SAT |
| Getafe, Spain | John Deere Ibérica, S.A. | PPA, CF, SAT |
| Göppingen, Germany | Kleemann GmbH | CF |
| Greeneville, Tennessee | John Deere Greeneville | SAT |
| Horicon, Wisconsin | John Deere Horicon Works | SAT |
| Horizontina, Brazil | John Deere Brazil SA | **PPA** |
| Indaiatuba, Brazil | Brazil Construction Factory | CF |
| Kernersville, North Carolina | John Deere Kernersville | CF |
| Ludwigshafen, Germany | Vögele AG | CF |
| Mannheim, Germany | John Deere Werke Mannheim | SAT, **PPA** |
| Montenegro, Brazil | John Deere Brazil Ltda | **PPA** |
| Monterrey, Mexico | Industrias John Deere SA de CV | SAT, **PPA**, CF |
| Pune, India | John Deere Pune Works | SAT |
| Saran, France | Saran Engine Factory | SAT, **PPA**, CF |
| Tirschenreuth, Germany | Hamm AG | CF |
| Torreón, Mexico | Torreón Engine Factory | **PPA**, SAT, CF |
| Waterloo, Iowa | John Deere Engine Works; Waterloo Foundry; Waterloo Works | **PPA**, CF |
| Windhagen, Germany | Wirtgen GmbH | CF |
| Zweibrücken, Germany | John Deere Werke Zweibrücken | **PPA**, SAT |

**PPA-critical nodes:** Waterloo IA (large tractors, engines, foundry, drivetrain), East Moline IL (Harvester Works — combines), Des Moines IA (sprayers/cotton), Horizontina + Montenegro + Catalão Brazil (South American ag), Mannheim & Zweibrücken Germany (Europe).

**Announced footprint changes (2026):**
- Mid-frame skid steer & compact track loader production moving **Dubuque Works → Ramos Arizpe, Mexico**, operational by end-2026 (CF, not PPA). New **$55m plant in Nuevo León** for mini track/wheel loaders. ([Food Tank, 27 Apr 2026](https://foodtank.com/news/2026/04/can-new-deere-jobs-and-facilities-offset-years-of-layoffs/); [Equipment Insider, 13 Mar 2026](https://www.equipmentinsiderhq.com/posts/2026-03-13-john-deere-610-layoffs-mexico/))
- **Hebron, Indiana** $125m / 1.2m sq ft distribution centre, 150 jobs. **Kernersville, NC** $70m excavator manufacturing expansion, 150 jobs — **excavator production began there in Q2 FY2026**. ([Food Tank, 27 Apr 2026](https://foodtank.com/news/2026/04/can-new-deere-jobs-and-facilities-offset-years-of-layoffs/); [Supply Chain Dive, 4 Jun 2026](https://www.supplychaindive.com/news/deere-recovers-272m-in-tariff-refunds/821818/))
- Deere has pledged **$20bn of U.S. manufacturing investment over 10 years** — framed explicitly as tariff mitigation. (same sources)

---

## 4. Supply-chain PERFORMANCE, May–July 2026

### 4.1 Deere's own quantification of the cost hit (REPORTED FACT)

From the Q2 FY2026 earnings call, `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` line 81:

> "we did see higher year-over-year production costs in the second quarter, excluding the impact from tariff refunds. Without accounting for tariff refunds, year-over-year direct tariff expense was approximately **$200 million** of the headwind, with the remainder largely driven by **higher material and freight costs**."

From `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` line 1878: direct incremental tariff impact was **$372m in H1 FY2026 net of the recovery**, vs **~$95m in H1 FY2025**.

From `filings/2026-05-28…q2-10q` line 2011 — the PPA-specific attribution:

> "Operating profit decreased primarily due to lower shipment volumes and higher production costs from an increase in **material and freight costs**, partially offset by the favorable effects of foreign currency exchange."

Tariff run-rate and allocation (Q2 Q&A, `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` lines 21–23): gross **~$1.2bn for the full year, unchanged**, despite IEEPA going away, Section 122 coming in and Section 232 adjustments; split ~45% C&F, ~⅓ SAT, ~20% large ag; ~3 points of full-year margin. The $272m refund split ~50% C&F / 30% SAT / 20% large ag. Net FY2026 tariff cost ≈ **$900m** ([Supply Chain Dive, 4 Jun 2026](https://www.supplychaindive.com/news/deere-recovers-272m-in-tariff-refunds/821818/)).

Mitigation actions named by CFO Brent Norwood (Q2 Q&A line 35): "**resourcing, reshoring, exemption submissions, ensuring USMCA compliance**" — explicitly **no tariff surcharge to customers**.

**Management's forward statement on the Q3/Q4 cost line** (Q2 Q&A lines 39–41):
> "on the production cost side, including tariffs and material costs, that gets more favorable as well. Price cost will improve as we move through the balance of the fiscal year."

But also, same call, line 123: "I would agree with you that we are seeing **some high levels of inflation over the last two or three months**." That "last two or three months" window is Feb–May 2026 — i.e. the run-up into Q3.

### 4.2 The macro shock inside the window: the 2026 Iran war and the Strait of Hormuz

Deere named it directly on 21 May 2026 (`call-transcripts/2026-05-21…call-pres` line 67): "a lot has transpired over the past quarter in the global economy, **most notably the conflict in Iran and the associated impacts**", and line 109: "input costs, particularly **fuel and fertilizer**, have increased globally".

External timeline (all secondary/commentary — treat as ESTIMATE-grade context):

| Date | Event | Source |
|---|---|---|
| Late Feb 2026 | U.S./Israeli operations against Iran begin; Strait of Hormuz effectively closed within 48 hours | [Wikipedia: 2026 Strait of Hormuz crisis](https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis) |
| 12 Apr 2026 | Daily Hormuz vessel crossings down **>95%** vs pre-war | [SeaVantage crisis timeline](https://www.seavantage.com/blog/strait-of-hormuz-crisis-2026-shipping-disruption-timeline) |
| 23 Apr 2026 | Container spot: Far East→USWC **$2,857/FEU, +22% m/m**; Far East→USEC **$3,871/FEU, +19% m/m**; N. Europe→USEC **+46% m/m** | [FreightWaves, 27 Apr 2026](https://www.freightwaves.com/news/the-iran-conflict-sent-asia-us-shipping-rates-soaring-thousands-of-miles-away-heres-why) |
| Apr 2026 | Ceasefire agreed | [Al Jazeera, 23 Jul 2026](https://www.aljazeera.com/economy/2026/7/23/how-shipping-insurance-rates-are-rising-as-hormuz-bab-al-mandeb-shut-down) |
| Jun 2026 | Memorandum of understanding signed | as above |
| **Jul 2026** | **Conflict resumes**; attacks on commercial shipping; war-risk insurance rates rising; Bab al-Mandeb also shut | [Al Jazeera, 23 Jul 2026](https://www.aljazeera.com/economy/2026/7/23/how-shipping-insurance-rates-are-rising-as-hormuz-bab-al-mandeb-shut-down) |
| **30 Jul 2026** | Hormuz **effectively closed** to routine commercial shipping; ~10 vessels/day vs pre-crisis 88–130 | [SeaVantage](https://www.seavantage.com/blog/strait-of-hormuz-crisis-2026-shipping-disruption-timeline) |

**INFERENCE (mine):** Deere ships very little through Hormuz directly, but the second-order effects land squarely on its P&L in fiscal Q3 — (a) transpacific and transatlantic ocean freight on the ~25% of components and ~20% of finished goods it imports from Europe/Mexico/India/Japan; (b) bunker-fuel-linked inbound and outbound domestic freight; (c) fertiliser and diesel cost inflation depressing customer margins, especially in Brazil ahead of the September planting window — which Deere itself linked to its decision to cut the Brazil guide. This argues the "material and freight" line stayed a **headwind in Q3**, partly offsetting the favourable tariff/price comps management promised.

### 4.3 Semiconductors and electronics — no Deere-specific disruption found

Industry commentary (secondary, low-to-medium confidence) describes mid-2026 as a **selective, structural** shortage rather than a 2021-style broad crisis: 8-bit MCUs back to 2–10 week lead times, but 32-bit industrial MCUs and power-management ICs stretching toward 52 weeks as AI infrastructure absorbs mature-node foundry capacity ([IC Online Q3 2026 market report](https://www.ic-online.com/pt/blog/post/market-report-q3-2026-semiconductor-lead-time-pricing-and-supply-chain-risk-analysis-for-oem-buyers); [Utmel power semiconductor outlook 2026](https://www.utmel.com/blog/categories/semiconductor/power-semiconductors-shortage-outlook-2026-supply-lead-times-and-sourcing-options)).

**Deere itself did not mention semiconductors, chip allocation or electronics shortages once in the Q1 or Q2 FY2026 calls or in the Q2 10-Q.** Given that Deere designs and builds its own controllers (Phoenix International / John Deere Electronic Solutions) and its own GNSS receivers (NavCom lineage), it sits one step removed from merchant-MCU allocation. **Not found:** any 2026 report of a Deere line stoppage caused by chip availability.

### 4.4 Rare earths — dormant risk, suspended not resolved

Deere flags China-sourced rare earths as a named dependency for motors and batteries (10-K line 657). China **suspended** the October 2025 export-control expansion for one year until **10 November 2026** as part of a US–China trade agreement ([China Briefing](https://www.china-briefing.com/news/chinas-rare-earth-export-controls-impacts-on-businesses/); [S&P Global, 27 Jan 2026](https://www.spglobal.com/energy/en/news-research/latest-news/metals/012726-rare-earth-supply-bottlenecks-set-to-persist-in-2026)). **INFERENCE:** immaterial to Q3 FY2026; a live risk for FY2027 guidance commentary on the 20 Aug call.

### 4.5 Steel and raw materials

Section 232 steel/aluminium tariffs were doubled 25%→50% on 4 June 2025. Secondary sources put US hot-rolled coil around **$947/short ton mid-2026** ([Bomis Steel 2026 guide](https://www.bomissteel.com/steel-coil-prices-market-trends-2026/); [Cato, "Steel Prices Rise (Again)"](https://www.cato.org/blog/steel-prices-rise-again-amid-persistent-us-tariffs)) versus a pre-232 $560–620 range. **Grade: estimate — these are trade-blog figures, not CRU/Platts primary data.** Deere's own framing is consistent: general inflation ex-tariffs of ~1.5–2% against price realisation of ~1.5–2% (Q2 Q&A line 35), i.e. tariffs are the margin-dilutive increment, not base material inflation.

### 4.6 Supplier financial distress — nothing found

**Not found.** I searched for 2026 insolvency, bankruptcy or delivery failure at Deere suppliers and found no reported event. Deere's Q2 10-Q carries only the boilerplate risk-factor language. Titan International — the one Deere-dependent supplier whose financials are public — reported FY2025 results on 28 Feb 2026 with no going-concern flag. **Where I looked:** corpus full-text search for `supplier|supply chain|shortage`, plus web searches on supplier bankruptcy and farm-equipment parts shortages.

### 4.7 Port / freight / logistics constraints, US domestic

**Not found** for anything Deere-specific: no US port strike, rail disruption or Mississippi/Illinois River logistics event reported in May–July 2026 in the sources searched. Ascent Global Logistics — a Deere Partner-level 3PL — was recognised on **7 May 2026**, i.e. Deere's outbound logistics network was operating normally enough to run its awards programme mid-window.

---

## 5. Production announcements, layoffs and plant idling — the direct shipment signal

Deere's stated policy is that "production schedules at each John Deere factory vary to align with seasonal farming needs", with seasonal and inventory-adjustment shutdowns used as the lever. The FY2025 10-K (line 339) confirms: "Our manufacturing, logistics, and scheduling systems are dependent on forecasts of industry volumes… we can adjust our assembly lines to accommodate a wide product mix."

### 5.1 Layoff / recall timeline

| Date | Action | Plants | Workers | Source |
|---|---|---|---|---|
| Oct 2023 | Layoff | East Moline | 225 | [Food Tank, 27 Apr 2026](https://foodtank.com/news/2026/04/can-new-deere-jobs-and-facilities-offset-years-of-layoffs/) |
| Jun 2024 | Layoff | East Moline 280, Davenport 230, Dubuque 100 | 610 | [Equipment Insider, 13 Mar 2026](https://www.equipmentinsiderhq.com/posts/2026-03-13-john-deere-610-layoffs-mexico/) |
| CY2024 total | Layoff | Waterloo ~1,000 + Davenport, Dubuque, Ankeny, Ottumwa, Moline, East Moline | 2,167 | [Food Tank](https://foodtank.com/news/2026/04/can-new-deere-jobs-and-facilities-offset-years-of-layoffs/) |
| 15 Aug 2025 | Layoff (notified) | Harvester Works E. Moline 115 (last day 29 Aug), Seeding & Cylinder Moline 52 (26 Sep), Waterloo Foundry 71 (19 Sep) | 238 | [The Gazette](https://www.thegazette.com/business/john-deere-to-lay-off-more-than-200-employees-across-three-factories/article_25d409a4-afc3-5232-8ef1-3026452fb46a.html) |
| 17 Sep 2025 | Layoff (WARN) | Waterloo 101 (eff. 20 Oct), Ankeny 40 (eff. 3 Nov) | 141 | [WARNact](https://warnact.io/company-john-deere) |
| Oct 2023–Sep 2025 cumulative | Layoff | all | **>3,500** | [Food Tank](https://foodtank.com/news/2026/04/can-new-deere-jobs-and-facilities-offset-years-of-layoffs/) |
| **28 Jan 2026** | **RECALL** | Davenport Works 75, Dubuque Works 24 | **99** | [CBS2 Iowa, 6 Feb 2026](https://cbs2iowa.com/news/local/john-deere-announces-146-waterloo-worker-callbacks-citing-increased-production-demand) |
| **6 Feb 2026** | **RECALL**, starting early March | Waterloo Tractor Operations, Drive Train Operations, Engine Works, Foundry — supporting **8R tractor** assembly, machining, logistics, foundry | **146** | [CBS2 Iowa, 6 Feb 2026](https://cbs2iowa.com/news/local/john-deere-announces-146-waterloo-worker-callbacks-citing-increased-production-demand) |
| **Apr 2026** | Recalls confirmed: Waterloo 146, Dubuque 24, Davenport 75 | | **245** | [Food Tank, 27 Apr 2026](https://foodtank.com/news/2026/04/can-new-deere-jobs-and-facilities-offset-years-of-layoffs/) |
| **Jan–Aug 2026** | **NO Deere WARN filings — zero YTD 2026** (most recent on file: 17 Sep 2025) | — | **0** | [WARNact John Deere page](https://warnact.io/company-john-deere) |

Deere's stated reason for the February recall (Fabio Castro, VP Waterloo Works): the callbacks "reflect the production needs driven by increased customer demand."

**This is the single most important supply-chain-side finding for the forecast.** Deere's well-documented pattern is to WARN-notice production cuts weeks before they bite. There is no such notice anywhere in calendar 2026 — and the only workforce news is inbound. **I searched specifically for Deere layoffs, furloughs, idling and shutdowns in June/July/August 2026 and found none.**

### 5.2 Deliberate production plan by region (REPORTED FACT — company statements)

From `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` lines 123–133:

- **NA large ag:** HHP tractor and combine field inventories **down >50% from the mid-2024 peak**, inventory-to-sales in line with historical averages. "Our plan for the year is to continue to **manage production in line with retail demand**."
- **NA used:** combines down mid-teens from Mar-2024 peak; used HHP tractors down mid-teens and down low-single-digits *sequentially in a seasonal-build quarter*; MY2022–23 8Rs **down ~45%** from last year's peak; used sprayers **-30%**, planters **-50%** from recent peaks.
- **Waterloo:** "order books are **well into the fourth quarter** as we look to close out our model year 2026 production."
- **NA SAT:** building in line with retail after last year's underproduction.
- **Europe:** "2026 production is largely aligned with retail demand."
- **Brazil:** "**we expect to underproduce retail demand, most notably in combines**." Order visibility in Europe and South America "extends through the third quarter and into the fourth."

Reaffirming the Q1 call (`call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md` line 67): "We'll **underproduce retail for Brazilian combines in our second and third quarters** to bring those inventory levels down."

Seasonal products are locked: "Demand and that production plan for 2026 is **set at this point**. Our EOPs for this year have closed, and we know where we're going to build in combines, sprayers, and planters" (Q2 Q&A line 65). Sprayer EOP opened early May, runs to end-August; planter EOP opens early June, runs to end-September — these set **FY2027**, not FY2026, volumes.

### 5.3 The explicit Q3-vs-Q4 cadence guidance (REPORTED FACT — the key modelling constraint)

`call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` line 143:
> "we would expect **slightly higher revenue in the back half, with the fourth quarter being higher than the third quarter**. In addition, we would expect to see our **most favorable cost comparisons in the fourth quarter** as well."

`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` lines 95–97:
> "As you look at Large Ag… **Q4 a bit stronger than Q3**. We've got **more Waterloo large tractor shipments shipping to North America in the back half than the front half** of the year. That's abnormal for us… On the small Ag side, it's pretty normal seasonality. You'll get **a little bit of a step down in Q3 and another step down in Q4**… Construction & Forestry, fairly balanced between the two… maybe a little bit stronger in the fourth quarter than Q3."

`call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` line 125 (Norwood):
> "particularly for our large ag factories, [we'll see] **a little bit better absorption in the fourth quarter as production rates are significantly higher**… That's going to help on the overhead absorption as we move a little bit later in the year."

**INFERENCE (mine):** overhead absorption in PPA improves in **Q4**, not Q3. PPA Q3 operating margin therefore likely lands between the Q2 FY2026 15.7% and the Q4 exit rate, and closer to the Q2 level than to a Q4 peak — the deliberately Q4-loaded Waterloo build means Q3 does *not* get the absorption benefit while still carrying the freight/material headwind.

---

## 6. UAW and labour relations

### 6.1 Contract status (REPORTED FACT)

From `filings/2025-12-18__de-us-20251218-fy-10k__393777.md` lines 441–447:
> Unions are certified bargaining agents for **~77% of U.S. production and maintenance employees**. Approximately **7,600 active U.S. production and maintenance workers are covered by a collective bargaining agreement with the UAW, with an expiration date of 1 November 2027.** A small number are represented by the IAM. U.S. collective bargaining agreements expire **between 2025 and 2027**. Unions also represent the majority of employees at non-U.S. manufacturing facilities.

Headcount context (10-K line 439): **~73,100 employees** at 2 Nov 2025, of which ~32,500 full-time production; **27,000 in the U.S.**, ~11,600 full-time production.

### 6.2 The 2026 contract-extension fight (live, but post-quarter)

| Date | Event | Source |
|---|---|---|
| Mid-2026 | Deere offers to extend the six-year 2021 agreement (expiring 31 Oct / 1 Nov 2027) by two years to **eight years**, locking terms through 2029. Covers **~10,000 workers at nine Midwestern plants** per press reporting | [Jacobin, 12 Aug 2026](https://jacobin.com/2026/08/uaw-john-deere-contract-workers) |
| Jul–Aug 2026 | UAW pushes back; counteroffer roughly **half a billion dollars** above Deere's. Deere proposes replacing the 2026 3% annual lump sum with a **4% general wage increase**, moving the lump sum to 2028; UAW wants a **5% GWI in 2026 plus** the 3% lump sum | [Manufacturing.net](https://www.manufacturing.net/automotive/news/22971894/john-deere-uaw-half-a-billion-dollars-apart-in-contract-extension-clash); [OurQuadCities](https://www.ourquadcities.com/news/local-news/john-deere-will-not-increase-proposed-contract-extension-for-uaw-workers/) |
| 1 Aug 2026 | Deere holds firm; will not improve the offer. UAW Local 838 (Waterloo) leading opposition | [KTIV, 1 Aug 2026](https://www.ktiv.com/2026/08/01/deere-uaw-still-debating-contract-extension-proposal-ahead-union-vote/); [KWWL](https://www.kwwl.com/news/deere-holds-firm-as-uaw-local-838-pushes-back-on-proposed-contract-extension/article_e762fff0-f556-4243-acc3-a4063a6feef3.html) |
| **23 Aug 2026** | **Member ratification vote on the extension** | [Jacobin, 12 Aug 2026](https://jacobin.com/2026/08/uaw-john-deere-contract-workers) |

Historical benchmark: the 2021 UAW-Deere strike ran **34 days** and produced a 20% wage increase over six years plus COLA and three lump sums.

### 6.3 Assessment

**INFERENCE (mine, high confidence):** **strike risk inside FY2026 Q3 was zero.** The master agreement does not expire until November 2027; the current dispute is over an *early, voluntary* extension, which the union can simply reject without any lawful work stoppage. A "no" vote on 23 Aug 2026 leaves the existing contract fully in force. **Nothing in the labour picture reduced Q3 shipments.**

Two live but *post-quarter* considerations for the 20 August print: (i) the vote falls three days after earnings, so management will likely be asked about it and may decline to comment; (ii) UAW rhetoric this year has fixed on Mexico offshoring and buybacks — 2024–25 layoffs alongside a reported $43.6bn of buybacks and dividends over two decades ([Common Dreams](https://www.commondreams.org/news/uaw-john-deere-layoffs); [UAW statement](https://uaw.org/uaw-statement-on-corporate-greed-at-john-deere/)) — so a rejection would raise FY2027–28 labour-cost risk, not FY2026.

---

## 7. Gaps, negative findings, and where I looked

1. **No FY2026 Q3 actuals exist.** The corpus ends 28 May 2026 (frozen 14 Aug 2026); Q3 reports 20 Aug 2026. Confirmed by reading the mislabelled "Q3 2026" transcript in full.
2. **Component-level supplier roster: not found.** Deere does not publish a bill-of-materials supplier list; JDSN is gated. Hydraulics, drivetrain, tyre and semiconductor supplier names commonly attributed to Deere in trade press were **not verifiable** from primary sources in this window — I have listed them in §2.4 as explicitly unconfirmed rather than assert them.
3. **Titan International's FY2025 Deere-specific revenue share: not found.** Only the 2004–2010 disclosures (17–26%) and the FY2025 statement that agriculture ≈52% of net sales serving Deere/CNH/AGCO. Would require pulling Titan's FY2025 10-K directly.
4. **CNH Industrial's 10-Q for the quarter ended 30 June 2026** — the closest overlapping-period peer disclosure on component availability — returned HTTP 403 from SEC EDGAR via WebFetch. Not read. This is the best available cross-check on industry-wide supply conditions in the exact window and is worth retrieving by other means.
5. **No quantified freight-cost pass-through for Deere.** Deere gives "material and freight" as a combined bucket and does not split it. The container spot moves in §4.2 are directional context, not a Deere cost input.
6. **Steel price figures are trade-blog grade**, not CRU/Platts/AMM primary data.
7. **No Deere-specific May–July 2026 supply-chain incident found.** Searched: Deere layoffs/furloughs/idling Jun–Aug 2026; farm-equipment parts shortages and plant shutdowns Jul 2026; supplier bankruptcy; semiconductor availability; Iowa/Illinois WARN filings. All negative for Deere.
8. **Q3 consensus** (context, secondary): EPS **$4.85** vs $4.75 a year ago ([Barchart preview](https://www.barchart.com/story/news/3425260/deere-company-earnings-preview-what-to-expect)). Revenue consensus **not found**.

---

## 8. Baselines the forecasting model should anchor on

| Metric | Q3 FY2025 (actual) | Q2 FY2026 (actual) | Source |
|---|---|---|---|
| Worldwide net sales & revenues | **$12,018m** | **$13,369m** | `filings/2025-08-15__de-us-20250815-q3-8k__143410.md` L80; `filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md` L85 |
| Diluted EPS (GAAP) | **$4.75** | **$6.55** | same, L266 / L275 |
| PPA net sales | **$4,273m** | **$4,503m** | same, L86-90 / L220 |
| **PPA operating profit** | **$580m** (13.6% margin) | **$706m** (15.7% margin) | same |
| Diluted share count | 271.4m | 270.8m | same |

**FY2026 full-year guidance as of 21 May 2026** (`filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md` L74, L163):
- Net income attributable to Deere: **$4.5bn–$5.0bn** (maintained)
- PPA net sales: **down 5–10%** (currency +3.0%, price ~+1.0%)
- SAT: up ~15% · C&F: up ~20% · Financial Services net income ~$860m
- Industry: US/Canada large ag **down 15–20%**; SAT flat to +5%; Europe flat to +5%; South America tractors & combines **down ~15%**

**H1 FY2026 actuals for the residual arithmetic:** NS&R $22,981m, net income $2,429m, diluted EPS $8.97, PPA net sales $7,666m, PPA operating profit $845m.

---

## 9. Source list

**Corpus (relative to `/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/`)**
- `filings/2025-12-18__de-us-20251218-fy-10k__393777.md` — FY2025 Form 10-K (raw materials, supply chain risk, properties, UAW, employees, tariffs)
- `filings/2025-11-26__de-us-20251126-q4-10k__469216.md` — FY2025 Annual Report (properties, footprint counts)
- `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md` — Q2 FY2026 Form 10-Q (tariff quantification, PPA cost attribution, inventories)
- `filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md` — Q2 FY2026 earnings release + FY26 outlook
- `filings/2026-05-21__de-us-20260521-q2-8k__1042167.md` — Q2 FY2026 8-K with call presentation
- `filings/2025-08-15__de-us-20250815-q3-8k__143410.md` — Q3 FY2025 earnings release (baseline)
- `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` — Q2 FY2026 prepared remarks
- `call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md` — Q2 FY2026 Q&A (**mislabelled "Q3 2026" in INDEX.md**)
- `call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md` and `…call-qna__605077.md` — Q1 FY2026 call
- `call-transcripts/2020-11-25__de-us-20201125-call-pres__46441.md` — technology-acquisition history (NavCom, Phoenix International, Blue River)
- `call-transcripts/2023-02-17__de-us-20230217-call-qna__46468.md` — Deere-Hitachi JV buyout
- `call-transcripts/2025-02-13__de-us-20250213-call-q1-qna__46478.md` — Starlink / JDLink Boost in Brazil

**Web**
- Supply Chain Dive, "Deere recovers $272M in tariff refunds", 4 Jun 2026 — https://www.supplychaindive.com/news/deere-recovers-272m-in-tariff-refunds/821818/
- CBS2 Iowa, "John Deere announces 146 Waterloo worker callbacks", 6 Feb 2026 — https://cbs2iowa.com/news/local/john-deere-announces-146-waterloo-worker-callbacks-citing-increased-production-demand
- Food Tank, "Can New Deere Jobs and Facilities Offset Years of Layoffs?", 27 Apr 2026 — https://foodtank.com/news/2026/04/can-new-deere-jobs-and-facilities-offset-years-of-layoffs/
- Equipment Insider, "John Deere Lays Off 610 Midwest Workers as Production Moves to Mexico", 13 Mar 2026 — https://www.equipmentinsiderhq.com/posts/2026-03-13-john-deere-610-layoffs-mexico/
- WARNact, John Deere WARN filings (0 filings YTD 2026; most recent 17 Sep 2025) — https://warnact.io/company-john-deere
- The Gazette, Deere Aug 2025 layoffs at three factories — https://www.thegazette.com/business/john-deere-to-lay-off-more-than-200-employees-across-three-factories/article_25d409a4-afc3-5232-8ef1-3026452fb46a.html
- Jacobin, "John Deere Is Testing Its Workers' Resolve", 12 Aug 2026 — https://jacobin.com/2026/08/uaw-john-deere-contract-workers
- KTIV, "Deere, UAW still debating contract extension proposal ahead of union vote", 1 Aug 2026 — https://www.ktiv.com/2026/08/01/deere-uaw-still-debating-contract-extension-proposal-ahead-union-vote/
- KWWL, "Deere holds firm as UAW Local 838 pushes back" — https://www.kwwl.com/news/deere-holds-firm-as-uaw-local-838-pushes-back-on-proposed-contract-extension/article_e762fff0-f556-4243-acc3-a4063a6feef3.html
- Manufacturing.net, "John Deere, UAW 'Half a Billion Dollars' Apart" — https://www.manufacturing.net/automotive/news/22971894/john-deere-uaw-half-a-billion-dollars-apart-in-contract-extension-clash
- OurQuadCities, "John Deere will not increase proposed contract extension for UAW workers" — https://www.ourquadcities.com/news/local-news/john-deere-will-not-increase-proposed-contract-extension-for-uaw-workers/
- UAW, "Statement on John Deere Contract Extension Offer by UAW VP Laura Dickerson" — https://uaw.org/statement-on-john-deere-contract-extension-offer-by-uaw-vice-president-laura-dickerson-director-of-the-agricultural-implement-department/
- Common Dreams, "UAW Rips 'Corporate Greed' of John Deere" — https://www.commondreams.org/news/uaw-john-deere-layoffs
- FreightWaves, "The Iran conflict sent Asia-US shipping rates soaring", 27 Apr 2026 — https://www.freightwaves.com/news/the-iran-conflict-sent-asia-us-shipping-rates-soaring-thousands-of-miles-away-heres-why
- Al Jazeera, "How shipping insurance rates are rising, as Hormuz, Bab al-Mandeb shut down", 23 Jul 2026 — https://www.aljazeera.com/economy/2026/7/23/how-shipping-insurance-rates-are-rising-as-hormuz-bab-al-mandeb-shut-down
- SeaVantage, "Strait of Hormuz Crisis 2026: Full Timeline & Ocean Freight Impact" — https://www.seavantage.com/blog/strait-of-hormuz-crisis-2026-shipping-disruption-timeline
- Wikipedia, "2026 Strait of Hormuz crisis" — https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis
- IC Online, "Market Report Q3 2026: Semiconductor Lead Time, Pricing, and Supply Chain Risk" — https://www.ic-online.com/pt/blog/post/market-report-q3-2026-semiconductor-lead-time-pricing-and-supply-chain-risk-analysis-for-oem-buyers
- Utmel, "Power Semiconductors Shortage Outlook 2026" — https://www.utmel.com/blog/categories/semiconductor/power-semiconductors-shortage-outlook-2026-supply-lead-times-and-sourcing-options
- China Briefing, "China's Rare Earth Export Controls" — https://www.china-briefing.com/news/chinas-rare-earth-export-controls-impacts-on-businesses/
- S&P Global, "Rare earth supply bottlenecks set to persist in 2026", 27 Jan 2026 — https://www.spglobal.com/energy/en/news-research/latest-news/metals/012726-rare-earth-supply-bottlenecks-set-to-persist-in-2026
- Cato Institute, "Steel Prices Rise (Again) Amid Persistent US Tariffs" — https://www.cato.org/blog/steel-prices-rise-again-amid-persistent-us-tariffs
- Bomis Steel, "What Influences Steel Coil Prices & Market Trends (2026 Guide)" — https://www.bomissteel.com/steel-coil-prices-market-trends-2026/
- Titan International 10-K FY2006 (Deere 17%/20%/22% of revenue 2006/2005/2004) — https://www.sec.gov/Archives/edgar/data/0000899751/000089975107000020/form10k.htm
- Titan International 10-K FY2010 (Deere 26% of revenue) — https://www.sec.gov/Archives/edgar/data/0000899751/000089975111000007/form10k.htm
- Titan International FY2025 results, 28 Feb 2026 — https://www.prnewswire.com/news-releases/titan-international-inc-reports-fourth-quarter-and-fiscal-year-2025-financial-performance-302697570.html
- Helios Technologies, "Subsidiary Receives John Deere Supplier Innovation Award" — https://www.heliostechnologies.com/news/press-releases/detail/186/helios-technologies-subsidiary-receives-john-deere-supplier
- Farm Equipment, "Sherwin-Williams Recognized as a John Deere Partner-Level Supplier and Supplier of the Year", May 2026 — https://www.farm-equipment.com/articles/25337-sherwin-williams-recognized-as-a-john-deere-partner-level-supplier-and-supplier-of-the-year
- The Fabricator, "Quaker Houghton recognized as a John Deere Partner-level supplier" — https://www.thefabricator.com/thefabricator/news/consumables/quaker-houghton-recognized-as-a-john-deere-partner-level-supplier
- PR Newswire, "Thoughtworks Recognized as John Deere Partner-Level Supplier in 2026" — https://www.prnewswire.com/news-releases/thoughtworks-recognized-as-john-deere-partner-level-supplier-in-2026-achieving-excellence-program-302782477.html
- ChartMill/PR, "Ascent Global Logistics Earns Recognition as a John Deere Partner-Level Supplier for the 11th Consecutive Year", 7 May 2026 — https://www.chartmill.com/news/DE/prnews-2026-5-7-ascent-global-logistics-earns-recognition-as-a-john-deere-partner-level-supplier-for-the-11th-consecutive-year
- John Deere Supply Network (gated supplier portal) — https://jdsn.deere.com
- StockTitan, "Deere Sets Q3 2026 Earnings Call for Aug. 20" — https://www.stocktitan.net/news/DE/deere-to-announce-third-quarter-2026-financial-ws5vrthl5ifm.html
- Barchart, "Deere & Company Earnings Preview: What to Expect" (consensus EPS $4.85) — https://www.barchart.com/story/news/3425260/deere-company-earnings-preview-what-to-expect
