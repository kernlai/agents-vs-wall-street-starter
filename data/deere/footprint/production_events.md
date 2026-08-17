# Deere production event log — plant-level production-rate changes

Companion to `production_events.csv` (39 rows). Compiled 2026-08-16, before Deere's FY2026 Q3 earnings call on Thursday 20 August 2026, 09:00 US Central. **No FY2026 Q3 actuals exist.** Everything below is either a dated pre-quarter announcement, a dated in-quarter event, or management's own stated intent.

FY2026 Q3 window: **4 May 2026 – 2 August 2026.**

---

## 1. Lead finding: the July-shutdown comparison cannot be made from public data — but the absence of shutdown news is itself the signal

The task asked for the July 2026 vs July 2025 vs July 2024 shutdown-week comparison as the single most decision-relevant output. **I could not build it, and I am not going to fabricate it.** Here is exactly why, and what replaces it.

**Why it is not buildable.** Deere's *routine* contractual summer shutdown weeks are not publicly disclosed. They are negotiated into the UAW master agreement and communicated internally by plant. They do not generate press releases, WARN filings, or local news coverage, because nothing unusual is happening. What *does* generate coverage is an **extended** or **"inventory adjustment"** shutdown — a shutdown beyond the normal calendar, taken because demand fell. Those are covered obsessively by the Waterloo Courier, Quad-City Times, Telegraph Herald, KCRG, KWQC and the ag trade press, and they are the observable variable.

So the measurable quantity is not "how many weeks" but "was there an extended shutdown". That question I can answer.

**The answer for the FY2026 Q3 window: no. Nothing was announced.**

| Check | Result |
|---|---|
| Deere WARN notices filed anywhere, 2026 YTD | **Zero.** Both independent WARN aggregators (WARNact, WARN Firehose) report no 2026 Deere filings; last notice on record is 2025-09-17 (Waterloo 101, Ankeny 40). |
| Extended / inventory-adjustment shutdown announced May–Aug 2026 | **None found** at Waterloo, Ottumwa, Des Moines Works (Ankeny), Harvester Works, Seeding & Cylinder, Davenport, Dubuque, Coffeyville, or Horicon. |
| Shift eliminations announced May–Aug 2026 | **None found.** |
| Plant closures announced May–Aug 2026 | **None found.** |
| Workforce actions actually announced in the window | **Additions.** 20 recalled at Davenport Works + **30 newly hired** at Dubuque Works, effective June 2026 (KWQC, 2026-06-11). |

Contrast with the same window one and two years earlier: July 2024 brought ~600 production layoffs announced on 1 July; December 2024–January 2025 brought a roughly four-week inventory-adjustment shutdown at Ottumwa Works; August–September 2025 brought 238 layoffs across Harvester Works, Seeding & Cylinder and the Waterloo Foundry, followed by 141 more in September. **The FY2026 Q3 window contains none of that. It contains the opposite.**

**Interpretation.** The employment indicator, read honestly, says Deere did **not** take an extended production cut in its fiscal Q3 2026. It does not say Q3 shipments were strong — see §3, where management said the opposite about the *level*. It says the quarter came in **on plan** rather than being cut into. For a forecaster this is a variance-narrowing finding, not a direction-changing one: it removes the downside tail in which an unannounced deep summer shutdown produces a large negative surprise in PPA.

### A dating trap worth flagging

Search engines repeatedly surface a Waterloo-Cedar Falls Courier article, *"Deere changes summer shutdown"*, summarised as: Waterloo Operations' annual shutdown moves from late July/early August to **the last two weeks of June, effective in 2026**. If real, that would matter — it would pull the whole shutdown inside fiscal Q3 rather than straddling the Q3/Q4 boundary.

**It is almost certainly not a 2026 article.** The piece quotes "Pat Pinkston, general manager of Deere's Waterloo Operations." Waterloo Works' Vice President and Factory Manager as of February 2026 is **Fabio Castro**; the 2019 Courier profile names Dave DeVault as the then-GM. Pinkston does not appear anywhere in the modern record. The article is a Lee Enterprises archival page behind a TollBit paywall, and the "2026" in the search summary is best read as an OCR/paraphrase artefact of an earlier year. **I have excluded it from the CSV and no conclusion here depends on it.** Anyone rerunning this tracker should re-check it rather than inherit my judgement.

---

## 2. What actually happened at the plants during and just before Q3 FY2026

The 2026 signal is a **recall and rehire cycle**, running continuously from January and still running inside the Q3 window.

| Date | Plant(s) | Action | Deere's stated reason |
|---|---|---|---|
| 2026-01-28 | Davenport Works (75), Dubuque Works (24) | Recall, eff. mid-Feb | "increased production demand and ongoing factory needs" |
| 2026-02-06 | Waterloo: Tractor Ops, Drive Train Ops, Engine Works, Foundry (146) | Recall, eff. early March | increased demand, explicitly to support **8R** (and per KIMT, 8R/9R) tractor build |
| 2026-02-19 | Dubuque Works (27) | Recall | "Customer demand has continued to strengthen, driving increased production" — factory manager Alex Fernandez. Cumulative ~275 YTD |
| 2026-04-13 | Dubuque (21), Davenport (20), Coffeyville KS (8) | Recall | rising demand in construction, forestry, drivetrain. Cumulative >300 YTD |
| **2026-06-11** | **Davenport Works (20 recalled), Dubuque Works (30 hired)** | **Recall + external hire, eff. June** | **"increased demand for construction equipment." Cumulative >400 hired-or-recalled since January** |

Two things deserve weight.

**The Waterloo February recall is the highest-value single data point for large ag.** Waterloo is the PPA production heart — 2,734 acres, ~7.2m sq ft across five sites, the largest Deere manufacturing complex. Deere recalled into the **foundry** as well as assembly. Foundry and drive-train activity lead final assembly by weeks, so a February foundry recall is a commitment to a higher tractor build rate in the March-through-August period — precisely the Q3 window. And Deere named the product: 8R.

**The June Dubuque action includes external hires, not just recalls.** That is a stronger signal than a recall. Recalls draw from a pool of laid-off workers with contractual recall rights; hiring from outside means either the pool is exhausted or the required rate exceeds it. This is C&F, the segment already guided to +20% for the year with >80% of production slots filled.

**Caveat on segment attribution.** Most of the 2026 recall activity is **Dubuque, Davenport and Coffeyville — Construction & Forestry**, not large ag. The recall log is much better evidence for C&F strength than for PPA. Waterloo (February, 146) is the only large-ag recall in the set. Do not read a C&F-weighted recall count as a PPA production signal.

---

## 3. What management said on 21 May 2026 about production for exactly this quarter

This is the company's own statement of intent for the period being forecast, from the Q2 FY2026 call (corpus: `call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md` and `…-call-qna__1042775.md`).

**On large-ag production cadence — the most important quote in the corpus for this task.** CFO Brent Norwood, on Q4 margin absorption:

> "…a little bit better absorption in the fourth quarter as production rates are significantly higher."

That is explicit: **Q3 FY2026 large-ag production rates are materially below Q4's.** Reinforced twice more — "we've got more Waterloo large tractor shipments shipping to North America in the back half than the front half of the year, that's abnormal for us"; and "Q4 a bit stronger than Q3" for large ag. Waterloo order books were described as "well into the fourth quarter as we look to close out our model year 2026 production."

**On underproduction, by region:**

| Region / segment | FY2026 production plan as stated 2026-05-21 |
|---|---|
| North America large ag | Build **in line with retail demand**. No incremental underproduction. |
| North America Small Ag & Turf | Build **in line with retail demand**, following last year's underproduction. |
| Europe | "largely aligned with retail demand" |
| **Brazil** | **"we expect to underproduce retail demand, most notably in combines"** — the only region with a stated underproduction plan; South America industry guide cut to −15% from −5% |
| C&F | Building to a strengthening order book; >80% of FY production slots filled |

**On seasonality by segment for Q3:** SAT was guided to "pretty normal seasonality… a little bit of a step down in Q3 and another step down in Q4" from Q2's 3,485. C&F H2 "fairly balanced," Q4 marginally stronger. Enterprise-level: "slightly higher revenue in the back half, with the fourth quarter being higher than the third quarter."

**The crux, stated plainly.** The prompt asks whether employment signals overstate a decline because Deere deliberately underproduces. For FY2026 the answer is that **the deliberate-underproduction lever is largely switched off** — three of four regions are building to retail, and only Brazilian combines are being underbuilt. That means for FY2026 the plant-employment signal should track shipments more faithfully than it did in FY2024–25, when underproduction drove plant activity below retail demand. That makes the indicator *more* reliable this year, not less. It also means the Q3 sequential softness in large ag is a **calendar/order-book artefact** (model-year 2026 close-out weighted to Q4), not evidence of a demand deterioration inside the quarter.

---

## 4. Structural footprint changes in flight during FY2026

| Change | Detail | Segment |
|---|---|---|
| **Dubuque → Ramos Arizpe, Mexico** | Mid-frame skid steer loaders and compact track loaders move out of Dubuque Works. Announced June 2024. Dubuque ramp-down begins **early 2026**; transition complete **by end of 2026**. | CF |
| **Nuevo León, Mexico** | $55m plant for mini track loaders and mini wheel loaders. Timeline undisclosed. | CF |
| **Kernersville, NC** | $70m, 380,000 sq ft small-excavator factory; >150 jobs. Announced 2026-01-27. **Production of Deere-designed excavators started inside Q2 FY2026** and ramps through Q3. Takes over future-generation excavator production previously done in **Japan** — reshoring, opposite direction to the Dubuque move. | CF |
| **Hebron, IN** | New parts/supply-chain distribution centre, ~150 jobs. Announced 2026-01-27. Investment undisclosed. | — |
| **Ottumwa Works / Des Moines Works** | Product verification & validation testing relocated to other Iowa/Illinois sites across FY2026. Overhead reduction; not an assembly-line move. | PPA |
| **$20B / 10 years** | US manufacturing investment commitment reaffirmed on the Q2 FY2026 call. | — |

Note the offsetting pattern: Dubuque loses two loader lines to Mexico during 2026 while simultaneously **recalling and hiring** (24 in Feb, 27 in Feb, 21 in April, 30 hired in June). The recalls are therefore not evidence that the Mexico transition stalled — they are backfilling excavator, forestry and other Dubuque lines whose demand is rising faster than the loader lines are leaving.

---

## 5. Labour context: the UAW contract extension fight, live right now

Not a production event, but it bears on how to read everything above and it lands directly on the earnings date.

Deere offered the UAW a **two-year extension** of the agreement expiring **1 October 2027** — 4% general wage increase effective 2026-11-01, another 4% effective 2027-11-01, $3,000 ratification bonus, existing contract language unchanged. The UAW countered roughly **$500m higher** (5% per year, COLA rolled into base). Deere rejected it and said it will not improve the offer. A **membership vote is expected 2026-08-23**, three days after the earnings call, with a **2026-08-31 deadline**. The agreement covers **>10,000 workers across nine UAW locals**; per the FY2025 10-K, ~7,600 active US production and maintenance workers are under the master contract, out of 11,600 US full-time production employees and 73,100 employees worldwide.

Two readings, and both are worth holding:
- Deere's own framing is defensive — it wants "continuity and certainty for our employees when equipment demand is down and the market outlook remains uncertain."
- But a company planning deep plant cuts does not normally lock in two years of 4% wage increases fifteen months early. Seeking labour peace through the FY2027 ramp is consistent with the recall data and with management's "2026 marks the bottom of the ag cycle" baseline.

---

## 6. Honest assessment of data quality

**What is well sourced.** Every 2026 recall and hire event has a named local outlet, a date, a plant, a headcount, and in most cases a quoted Deere factory manager. The zero-WARN-notices finding is corroborated by two independent aggregators. All management production commentary is quoted verbatim from the frozen corpus with file paths.

**What is missing, and I did not invent it.**
1. **Actual shutdown-week counts for July 2026, July 2025 and July 2024.** Not public. The `shutdown_weeks` metric appears in only 2 of 39 rows, one of which (`prod_evt_036`) is an explicit blank-value "not measured" marker. This is the biggest gap and it is a source limitation, not an effort limitation.
2. **Shift-level detail.** No shift additions or eliminations were announced anywhere in 2026. Recalls are recorded under `shift_change` with `units=employees_recalled` because they are the observable proxy, but Deere did not describe them as shift actions and I have not asserted that they were.
3. **Non-US plants.** Nothing on Mannheim, Bruchsal, Zweibrücken, Horizontina, Montenegro, Catalão, Pune, or Saran. Germany and Brazil have real disclosure regimes but I found no 2026 production events; European works-council notices were not searched. Brazil matters most given it is the one region with stated underproduction.
4. **Paywalls.** Waterloo-Cedar Falls Courier, AgDaily, Quad Cities Business and AgWeb are behind TollBit/Cloudflare and returned 402/403 to both WebFetch and curl. Several conclusions rest on search-engine summaries of those outlets rather than the full text. Where a fact appears in only one paywalled source I have either corroborated it elsewhere or excluded it.
5. **Coverage thins sharply after mid-June 2026.** I found no plant-level Deere news dated July or the first half of August 2026 at all. I read that as "nothing newsworthy happened," which for this indicator is meaningful — but it is also consistent with incomplete search index coverage of the most recent weeks. Treat the July 2026 blank as genuinely uncertain.

**What I did not find and want to state plainly:** no FY2026 Q3 results, no Q3 production statistics, and no post-quarter Deere commentary. None exist yet.

---

## 7. Using this as an ongoing tracker

The reusable mechanic is: **watch for the presence of an extended shutdown announcement, not for a week count.** Concretely, per quarter, check —

1. **State WARN databases** (Iowa Workforce Development, Illinois DCEO, Wisconsin DWD, Kansas, Georgia, Tennessee, North Dakota, Louisiana). Free, dated, structured, and legally compelled. Zero filings is a real observation.
2. **Plant-town local TV and press** for the words *inventory adjustment shutdown*, *extended shutdown*, *temporary suspension*, *callback*, *recall* — KWQC and WQAD (Quad Cities), KCRG and KWWL (Eastern Iowa), CBS2 Iowa, Telegraph Herald (Dubuque), KTVO and Ottumwa Post.
3. **Named factory managers** quoted in callback stories. They state the reason and often the product line — the February 2026 Waterloo story naming 8R is worth more than the headcount.
4. **The earnings call itself** for the four phrases that carry production intent: *underproduce*, *in line with retail demand*, *production slots*, *absorption*.
5. **UAW local channels** (Local 838 Waterloo, Local 865 Moline, Local 74 Ottumwa) — they confirm shutdowns and pay treatment before the company does.

The 2026 rows in the CSV are a clean template: dated, plant-level, segment-tagged, with the stated reason preserved in `notes`.

---

## Sources

Corpus (frozen 2026-08-14): `challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md`, `…__de-us-20260521-call-qna__1042775.md`, `…/2025-08-15__de-us-20250815-call-q3-pres__143406.md`, `…__de-us-20250815-call-q3-qna__143409.md`, `filings/2025-11-26__de-us-20251126-q4-10k__469216.md`, `filings/2026-05-28__de-us-20260528-q2-10q__1055932.md`.

Web: [WARNact — John Deere](https://warnact.io/company-john-deere) · [WARN Firehose — John Deere](https://warnfirehose.com/data/layoffs/company/john-deere) · [KWQC 2026-01-28](https://www.kwqc.com/2026/01/28/nearly-100-employees-set-return-2-john-deere-facilities/) · [KCRG 2026-02-06](https://www.kcrg.com/2026/02/06/john-deere-waterloo-recalling-about-150-workers/) · [CBS2 Iowa — Waterloo callbacks](https://cbs2iowa.com/news/local/john-deere-announces-146-waterloo-worker-callbacks-citing-increased-production-demand) · [CBS2 Iowa 2026-02-19 — Dubuque](https://cbs2iowa.com/news/local/john-deere-recalls-27-more-workers-to-dubuque-works-as-production-ramps-up) · [Construction Equipment 2026-04-16](https://www.constructionequipment.com/industry-news/news/55371187/john-deere-recalls-nearly-50-workers-as-production-demand-ticks-up) · [KWQC 2026-06-11](https://www.kwqc.com/2026/06/11/john-deere-bringing-back-20-workers-davenport-works/) · [KCRG 2026-07-30 — UAW extension](https://www.kcrg.com/2026/07/30/deere-uaw-still-debating-contract-extension-proposal-ahead-union-vote/) · [Equipment Insider 2026-03-13](https://www.equipmentinsiderhq.com/posts/2026-03-13-john-deere-610-layoffs-mexico/) · [PR Newswire — two new US facilities](https://www.prnewswire.com/news-releases/john-deere-announces-major-expansion-with-two-new-us-facilities-coming-302671843.html) · [Supply Chain Dive](https://www.supplychaindive.com/news/deere-open-two-facilities-20b-commitment-us-manufacturing/811055/) · [KCRG 2025-10-16 — Ottumwa/Des Moines](https://www.kcrg.com/2025/10/16/john-deere-moving-some-production-jobs-out-ottumwa-des-moines/) · [KCRG 2024-11-15 — Ottumwa shutdown](https://www.kcrg.com/2024/11/15/ottumwa-john-deere-facility-shut-down-temporarily-again-amid-reduced-demand/) · [AgWeb — 238 layoffs](https://www.agweb.com/news/breaking-john-deere-confirms-238-layoffs-across-3-plants) · [Manufacturing Dive](https://www.manufacturingdive.com/news/deere-lay-off-238-workers-tractor-market-tariff-struggles-harvester-works/757892/) · [Mexico News Daily — $55m](https://mexiconewsdaily.com/business/john-deere-commits-55m-mexico-facility-trump-threats-tariffs/) · [UAW statement — Deere extension](https://uaw.org/statement-on-john-deere-contract-extension-offer-by-uaw-vice-president-laura-dickerson-director-of-the-agricultural-implement-department/) · [Deere — UAW contract update](https://www.deere.com/en-us/john-deere-news/uaw-contract-update) · excluded/unverified: [WCF Courier — "Deere changes summer shutdown"](https://wcfcourier.com/news/metro/deere-changes-summer-shutdown/article_c23b7432-30d3-52f9-b73d-43114e1d8ecb.html) (archival, wrong-era GM named).
