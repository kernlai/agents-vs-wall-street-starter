# Deere employment → shipment volume: does the indicator actually work?

Built 2026-08-16. **Deere has not reported FY2026 Q3.** The quarter ran ~2026-05-04 to
2026-08-02 and is closed; the earnings call is 2026-08-20, after this file. No Q3 FY2026
actuals exist here or anywhere else.

Companion footprint file: `PLANT_MAP.md`.
Reproduce every number below with `python3 scripts/data/de_employment_indicator_backtest.py`
(raw output saved to `employment_indicator_backtest.txt`).

---

## 0. The answer, first

**The employment data is a genuine COINCIDENT proxy for Deere's shipment volumes. It is not a
demonstrated leading indicator, and the quarterly plant-event data is too sparse to establish
one either way.**

Three findings, in descending order of how much they are supported:

| | Finding | Support |
|---|---|---|
| 1 | Annual UAW-covered production headcount tracks equipment net sales almost one-for-one, **contemporaneously**. r = +0.89, slope 1.02. | n = 10 annual observations, filing-grade on both sides. The strongest thing here. |
| 2 | Quarterly plant labour events **do not beat naive persistence** of the revenue series itself, and their directional hit rate on next-quarter acceleration is **below 50%**. | n = 8–10 quarters, one cycle turn. Weak, but the direction of the result is clear. |
| 3 | The *composition* of events — which plants, which segments — carried real information where the aggregate did not. | Two clean episodes. Anecdotal, but the mechanism is sound. |

So: the user's premise ("headcount at a plant is a direct observable proxy for the production
rate at that plant") is **correct and validated**. The inference the premise invites ("therefore
it predicts next quarter's revenue") is **not validated**, and the data says the opposite of what
you would hope.

That is not a reason to discard it. It relocates the value. A coincident indicator on a quarter
that has **already closed but not yet been reported** is exactly what use case (A) needs — it is a
nowcast, and a nowcast does not require a lead. Section 4 uses it that way.

---

## 1. TEST 1 — annual: does headcount track shipments at all? (n = 10)

Series: `de_uaw_covered_employees` — active US production and maintenance workers under the UAW
master agreement, disclosed in Item 1 of every 10-K FY2015–FY2025. This is the right series
because **laid-off workers drop out of it**: it counts people actually on the line, not people on
the payroll. Verified verbatim against the FY2025 10-K
(`filings/2025-11-26__de-us-20251126-q4-10k__469216.md`: "Approximately 7,600 of our active U.S.
production and maintenance workers are covered by a collective bargaining agreement with the
United Auto Workers").

| FY | equipment net sales YoY | UAW-covered heads YoY | gap (heads − sales) |
|---|---:|---:|---:|
| 2016 | −9.3% | −24.0% | −14.7pp *(definitional break)* |
| 2017 | +10.7% | +14.5% | +3.8pp |
| 2018 | +28.8% | +10.3% | −18.5pp |
| 2019 | +4.6% | −3.1% | −7.7pp |
| 2020 | −10.4% | −6.0% | +4.3pp |
| 2021 | +27.1% | +20.1% | −6.9pp |
| 2022 | +20.6% | +9.5% | −11.1pp |
| 2023 | +16.0% | 0.0% | −16.0pp |
| 2024 | −19.4% | −22.6% | −3.2pp |
| 2025 | −13.1% | −14.6% | −1.6pp |

**n = 10, r = +0.891, slope = 1.02** sales-pp per head-pp. Excluding the FY2016 definitional break
(the word "active" enters the disclosure in FY2016): **n = 9, r = +0.902, slope = 1.15**.

### The asymmetry is the whole story

- **Down years (n = 4): mean gap −3.8pp.** Headcount falls *slightly more* than sales. This is
  precisely the deliberate-underproduction mechanism — Deere cuts plant activity below retail
  demand to drain inventory, so the labour cut runs a little ahead of the revenue cut. FY2024:
  −22.6% heads vs −19.4% sales. FY2025: −14.6% vs −13.1%. **In a downturn the indicator is sharp
  and close to unbiased.**
- **Up years (n = 6): mean gap −9.4pp.** Headcount badly *understates* growth. FY2023 is the
  extreme: sales +16.0% on **exactly zero** change in heads. Deere absorbs upside with overtime,
  added shifts and productivity, not bodies.

**Practical rule: you can scale a layoff number into a revenue number. You cannot scale a hiring
number.** Any attempt to read the 2026 recalls as proportional revenue upside is reading the
indicator through its weakest axis.

### What this test does not establish

Both sides of this regression are the **same fiscal year**. It is a coincidence relationship by
construction. It tells you employment is a valid proxy for the production rate. It tells you
nothing about lead time.

---

## 2. TEST 2 — quarterly: do layoff and recall events lead reported segment revenue?

Layoffs bucketed by **effective date** (when capacity actually leaves the plant), recalls and new
hires by **announcement date**.

**Non-production rows are excluded**, because they are headcount and not build rate: World
Headquarters 298, Intelligent Solutions Group 59, John Deere Financial 67, the 2018 Eurest
Services notice (79 food-service contractors at Deere Quad Cities sites, not Deere payroll), and
— easily missed — **four WARN rows at production sites that the notes explicitly flag as salaried
reduction waves**: Waterloo 49 and 69, Des Moines 16, Dubuque 34, all in mid-2024.

**This is why the quarterly totals below are lower than a naive sum over `warn_layoffs.csv`.**
FY2024 Q3 is **303 production workers here versus 895 in the raw file**; the entire 592 difference
is salaried, corporate, financial-services or contractor. Anyone summing that CSV without the
filter will overstate the 2024 production cut by roughly a factor of three in that quarter.

| Fiscal Q | Layoffs effective | Recalls/hires announced | Net | PPA y/y | SAT y/y | CF y/y |
|---|---:|---:|---:|---:|---:|---:|
| FY2024 Q1 | 0 | 0 | 0 | −6.7% | −19.2% | +0.3% |
| FY2024 Q2 | 368 | 0 | −368 | −15.9% | −23.2% | −6.5% |
| FY2024 Q3 | 303 | 0 | −303 | −25.1% | −18.3% | −13.5% |
| FY2024 Q4 | 934 | 0 | −934 | **−38.2%** | −25.5% | −28.8% |
| FY2025 Q1 | 192 | 0 | −192 | −36.7% | **−27.9%** | **−37.9%** |
| FY2025 Q2 | 122 | 0 | −122 | −20.5% | −6.0% | −23.3% |
| FY2025 Q3 | 72 | 0 | −72 | −16.2% | −0.9% | −5.4% |
| FY2025 Q4 | 339 | 0 | −339 | **+10.1%** | +6.5% | +27.0% |
| FY2026 Q1 | 40 | 99 | +59 | +3.1% | +24.0% | +33.9% |
| FY2026 Q2 | 0 | 222 | +222 | −13.9% | +16.4% | +28.6% |
| **FY2026 Q3** | **0** | **50** | **+50** | ? | ? | ? |

### Raw correlations, with sample sizes

Segment-matched (only that segment's own plants contribute to its labour delta):

| Segment | lag 0Q | lag +1Q | lag +2Q |
|---|---|---|---|
| PPA | r = +0.31 (n=10) | r = +0.49 (n=9) | r = +0.46 (n=8) |
| SAT | r = −0.03 (n=10) | r = −0.10 (n=9) | r = −0.22 (n=8) |
| CF | r = +0.67 (n=10) | r = +0.65 (n=9) | r = +0.31 (n=8) |

Read naively, CF looks good. **Do not read it naively.** Every one of these series moves
monotonically through a single V-shaped cycle — labour deltas are negative for eight straight
quarters and then positive for three, and revenue YoY does the same thing on the same schedule. A
positive correlation between two series that each trace one V is nearly guaranteed and carries
almost no information.

### TEST 3 — the test that actually decides it

Compare the labour signal against the cheapest possible alternative: **the revenue series
predicting itself**.

| Segment | persistence: revYoY(t) → revYoY(t+1) | labour(t) → revYoY(t+1) | labour(t) → *acceleration* in revYoY |
|---|---|---|---|
| PPA | **r = +0.61** | r = +0.52 | r = **+0.00** |
| SAT | **r = +0.84** | r = +0.45 | r = **−0.00** |
| CF | **r = +0.81** | r = +0.57 | r = +0.35 |

All n = 9.

**The labour signal loses to persistence in all three segments.** And on the only form of the
question that matters for a forecast — does labour tell you whether revenue growth is about to
*accelerate or decelerate* relative to where it already is — the correlation is **+0.001 for PPA
and −0.003 for SAT**. Not "small". Zero.

Directional hit rate, sign of net labour delta vs sign of next-quarter revenue-YoY acceleration:

| Segment | correct | rate |
|---|---|---|
| PPA | 3 / 8 | 38% |
| SAT | 2 / 8 | 25% |
| CF | 3 / 8 | 38% |

All three are **below a coin flip** on n = 8. With eight observations the confidence band on 38%
comfortably spans 50%, so this is not evidence that the signal is *inverted* — it is evidence that
there is **no detectable directional skill**, which is the honest conclusion.

### The two episodes that show why

**FY2025 Q4 — the aggregate was flatly wrong.** 339 workers were laid off effective in the very
quarter all three segments turned positive year-on-year (PPA +10.1%, CF +27.0%, SAT +6.5%). A
tracker reading total headcount would have called that quarter a continued decline.

**But the plant list was right.** Those 339 were Harvester Works 115 (combines), Moline Seeding 52
(planters), Waterloo Foundry 71 and Waterloo 101 — **entirely PPA, and concentrated in the
crop-harvesting and seeding end of it.** Nothing was cut at Dubuque or Davenport. Two quarters
later PPA printed −13.9% while CF printed +28.6%. The composition of the cut called the segment
divergence correctly when the total called it wrong.

**FY2026 Q2 — the mirror image.** +222 recalls announced, and PPA still printed −13.9%. The
recalls were 146 to Waterloo (large tractors) and 76 to Dubuque/Davenport/Coffeyville (C&F); none
to Harvester Works. Combines stayed off. PPA stayed down.

**Conclusion: the count is noise; the plant mix is signal.** That is a qualitative finding from two
episodes, not a fitted relationship, and it is stated as such.

### Why n is irreducibly small, and will stay small

- Iowa's WARN database only begins **2021-08-18**. Illinois goes back to 1999 but its threshold
  (33% of site workforce, or 250+) is so high that Deere's real August-2025 cut of **115 at
  Harvester Works produced no Illinois WARN record at all** — verified absent from the August,
  September and October 2025 monthly reports.
- The clearest measure of how much Illinois misses: **Moline Seeding & Cylinder Works fell from
  890 employees (690 production) in June 2024 to 625 (427 production) in October 2024** — a
  265-person, 30% reduction reported in local news — and generated **zero Illinois WARN records
  in 2024**. The WARN-based series for that plant shows only 52 (an August-2025 news event). The
  true 2024–25 cut there is roughly six times what the notice record contains.
- The federal six-month exemption excludes short furloughs, and scheduled shutdown weeks are never
  WARN-reportable.
- Kansas, Georgia, Louisiana, North Dakota, Michigan and Minnesota WARN databases refused scripted
  access, so Coffeyville, Augusta, Thibodaux, Valley City and Fargo contribute **nothing in either
  direction**.
- There are **no non-US plant events at all** in this dataset, against 46% of Q2 FY2026 revenue
  being non-US. Mannheim, Zweibrücken, Horizontina, Indaiatuba are all dark.

Twelve years of history would give a usable sample. What exists is roughly two and a half years
containing exactly one trough and one recovery. **No amount of care extracts a validated lead-lag
coefficient from that, and this file does not pretend otherwise.**

---

## 3. Where the indicator does have real, independent support

Two things survive scrutiny and are worth more than the failed lead-lag test.

**(a) An absence of negative events inside a closed quarter is informative, and it is a different
statistical object from a forecast.** WARN is high-precision and low-recall: when a notice appears,
something large and durable is happening; when none appears, it is weak evidence. But a *verified*
zero across complete state databases, **corroborated by positive announcements pointing the other
way**, is a much stronger joint reading than either alone. That is the situation in Q3 FY2026.

**(b) An independent series agrees.** US ag-machinery export flows (HS 8432+8433, whole industry,
not Deere-only) track Deere PPA revenue YoY at **r = +0.928 (n = 17)** — and, tellingly, explain
Deere's **US** revenue better (r = +0.880) than its non-US revenue (r = +0.722). That ordering is
the tell: this is a *sector production* measure, not a trade-flow measure, because US exports and
Deere's US shipments come off the same lines on the same schedules. It passed one clean
out-of-sample test: for Q2 FY2026 it implied PPA −15.4% against a reported −14.0%.

Two independent proxies for the same underlying thing — plant labour and sector export volume —
both derived from production schedules rather than from Deere's own guidance. When they agree, the
joint reading is meaningfully stronger than either.

---

## 4. CURRENT READING — what May–August 2026 says about Q3 FY2026

**The quarter is closed. This is evidence, not prediction.**

### Everything found inside 2026-05-04 → 2026-08-02

| Date | Site | Event | People | Segment |
|---|---|---|---|---|
| 2026-06-11 | Dubuque Works | **New external hires** — callback list exhausted | +30 | CF |
| 2026-06-11 | Davenport Works | Recall | +20 | CF |
| 2026-06-11 | — | Deere-stated cumulative since 1 Jan 2026 | 400 returned/hired | — |
| 2026-07-29 | Waterloo (UAW Local 838) | Union counters Deere's 2-year extension offer; Deere rejects | — | PPA |
| whole quarter | Iowa / Illinois / Wisconsin | Deere WARN notices filed | **0** | — |

The Iowa zero is a **hard zero, not a data gap**: the state database is current to notice date
2026-08-13 (past the quarter end) and contains 77 CY2026 notices from other employers, including
CNH Industrial closing lines in Burlington and Whirlpool cutting 288 at Amana. Deere is simply not
in it. Last Deere filing in either Iowa or Illinois: **2025-09-17**.

The strongest single datapoint is the Dubuque one: a plant that cut 133 people by WARN in 2024 had
recalled everyone with recall rights (24 in January, 27 in March, 21 in April) and moved to hiring
off the street. **A plant does not hire externally while producing below plan.**

### Reading it by segment — the composition matters more than the total

| Segment | Labour evidence in/around Q3 | Guidance | Read |
|---|---|---|---|
| **CF** | All 2026 activity: Dubuque, Davenport, Coffeyville. External hiring by June. Order book "up more than 60% since November … over 80% of production slots filled". | +~20% | **Corroborated.** The clearest of the three. |
| **PPA** | 146 recalled to Waterloo (8R tractors) in February — **but Harvester Works, the sole NA combine plant, received nothing in 2026**, after 415 cuts in 2024–25 (279 + 21 by WARN, plus a 115-worker action in Aug-2025 that fell below the Illinois threshold and was never filed). | −5% to −10% | **Mildly better than plan on tractors, no improvement on combines.** |
| **SAT** | **No plant events either way** in 2026. Ottumwa and Horicon silent. | +~15% | **No information.** Do not infer support from silence here. |

### Verdict on the revenue range

**The employment evidence argues against the low end, not for the high end.**

It removes the downside tail — the scenario that produced the FY2024–25 negative surprises was
Deere cutting *into* a quarter, and that demonstrably did not happen: no WARN, no shift
elimination, no extended shutdown, no reversal of the February–June recalls, and net additions
right through June. What it does **not** do is argue for upside, for four reasons that all cut the
same way:

1. **The signal is damped on the upside.** Down years the gap is −3.8pp; up years −9.4pp. You
   cannot scale +400 recalls into revenue.
2. **Management said Q3 is the weaker back-half quarter.** CFO Brent Norwood, 2026-05-21: "a
   little bit better absorption in the fourth quarter as **production rates are significantly
   higher**"; and "more Waterloo large tractor shipments shipping to North America in the back half
   than the front half of the year — that's abnormal for us." Waterloo order books run "well into
   the fourth quarter." **The February Waterloo recalls feed Q4 more than Q3.** SAT was guided to
   "a little bit of a step down in Q3."
3. **Callback announcements decelerated inside the quarter**: 222 announced in FY2026 Q2 versus 50
   in Q3. Part of that is a ceiling effect (Dubuque ran out of recall-eligible people), but it is a
   deceleration.
4. **Management was still calling demand down at the very end of the quarter.** Rejecting the UAW
   counter on 2026-07-29, Deere said it was contrary to providing "continuity and certainty **when
   equipment demand is down**." *(The day is reported; the year 2026 is inferred from search
   context — medium confidence.)*

### The one gap that could invalidate the positive read

**The summer shutdown comparison could not be built, and no substitute was invented.** Deere's
routine shutdown weeks are negotiated into the UAW master agreement, are not WARN-reportable, are
not in the 10-K and are in no traceable press release. Neither the normal baseline nor the 2026
schedule is public.

This matters specifically because of a **fiscal calendar artefact**: FY2025 Q3 ended 2025-07-27 but
FY2026 Q3 ended **2026-08-02**. A late-July/early-August shutdown straddles that boundary
differently in the two years. A shutdown that fell partly into FY2025 Q4 could sit **wholly inside
FY2026 Q3**, depressing Q3 FY2026 production days year-on-year **with no change whatsoever in the
underlying schedule**. This is unquantified and it cuts directly against the positive callback
reading.

### A trap that was caught — do not re-import it

Web search repeatedly asserts that Deere moved the Waterloo summer shutdown to the last two weeks
of June "effective in 2026", citing a Waterloo–Cedar Falls Courier article. Fetching that page with
a crawler user-agent returns `datePublished 2006-08-04`. **The article is from 2006**; the "2026"
is a search-summary artefact. It names "Pat Pinkston, general manager of Deere's Waterloo
Operations", while the incumbent as of February 2026 is Fabio Castro. It was excluded and no
conclusion depends on it. **Always confirm publication date before using a search summary.**

### Corroboration from the independent proxy

US ag-machinery exports (HS 8432+8433) for **May + June 2026** — two of the quarter's three
calendar months, published data — were **$861m, +21.2% YoY**, the first positive print since 2023,
against −32.6% in the same window of 2025. Direction agrees with the labour evidence.

**Magnitude does not, and should be discarded.** The naive regression implies PPA +24% YoY, which
cannot be reconciled with Deere's own guidance of PPA −5 to −10%; residual sd is 10.7pp; July is
unpublished, and at export +0% the implied PPA is only +1%. Levels remain 18% below 2024. **Use the
sign, not the number.** Note also that the construction proxy (HS 8429) has decoupled from Deere CF
in FY2026 — CF +28% against exports −7% — because Deere's CF growth is European roadbuilding
(Wirtgen), which a US export series cannot see. Do not use it for CF.

### Net

**Q3 FY2026 shipments in line with the plan management set in May, with C&F the strongest leg,
PPA sequentially soft versus Q2's 4,503 and below a naive seasonal projection, and a materially
reduced probability of a negative shipment shock.** The labour record says the plants were staffed
to run the plan; it does not say they beat it.

---

## 5. Operating this as an ongoing tracker (use case B)

Roughly 20 minutes a week, no paid data.

### 5.1 What to poll, and how often

| Source | Cadence | Method | Why |
|---|---|---|---|
| **Iowa WARN** | weekly | Download `https://public.tableau.com/workbooks/IowaWARNNotifications.twb`, unzip, read the `.hyper` extracts with `tableauhyperapi`, filter `Company LIKE '%Deere%'` | **Highest value.** 25-employee threshold catches Deere events Illinois misses; covers Waterloo, Dubuque, Davenport, Ankeny, Ottumwa |
| **Illinois WARN** | monthly | Newest monthly XLSX from the DCEO archive; grep `xl/sharedStrings.xml` for "Deere" | Covers Harvester Works, Moline, Silvis — but see the threshold caveat below |
| **Wisconsin WARN** | monthly | Public Google Sheet behind the DWD page, `gviz` CSV endpoint | Horicon. Has never contained a Deere record |
| **Local plant-town news** | 2–3×/week | Deere newsroom, KCRG, KWQC, WQAD, Telegraph Herald, Waterloo–Cedar Falls Courier, quadcitiesbusiness.com | **Callbacks never appear in WARN.** This is the entire positive half of the signal |
| **UAW Locals 838 / 865** | weekly | Local communications | Lead the press by days on recall and shift notices |
| **Deere careers board** | weekly | `scripts/data/fetch_deere_jobs.py` (Eightfold PCSX endpoint; `robots.txt` explicitly allows `/api/pcsx`) | Builds the postings time series that does not yet exist |
| **10-K Item 1 "Employees"** | annually, ~Nov | Corpus filing | The only filing-grade calibration point |
| **10-K Item 2 "Properties"** | annually, ~Nov | Corpus filing | Segment reassignments, factory counts |
| **Deere worldwide locations PDF** | annually, ~Dec | `deere.com/assets/pdfs/common/our-company/about/jd-world-locations.pdf` | Openings, closures, product moves |
| **UN Comtrade HS 8432/8433** | monthly (~6-week lag) | `scripts/data/de_fetch_comtrade_machinery.py` | The independent production proxy |

### 5.2 Thresholds — what counts as a signal

Sized against the FY2025 10-K denominator of **~11,600 full-time US production employees**
(~7,600 of them UAW-covered). Do not use total company headcount as the denominator; it includes
~35,000 non-production people worldwide who do not move with the build schedule.

| Level | Trigger | Interpretation |
|---|---|---|
| **Noise — ignore** | Any single event under ~50 people at one plant; any salaried, corporate or IT reduction; any Financial Services action | Normal churn, or not build rate at all |
| **Watch** | 50–150 at one plant, or two plants in the same segment inside one month | Log it, wait for confirmation. Roughly 0.4–1.3% of US production base |
| **Signal** | >150 at one plant, or >300 across one segment inside a quarter (≈2.5%+ of the US production base), **or** any recall list declared exhausted with external hiring beginning | Act on it, at the segment level only |
| **Strong signal** | Any *extended* or "inventory adjustment" shutdown announced outside the normal seasonal window; any shift eliminated; any WARN notice at Harvester Works | These are the events that preceded the FY2024–25 collapse |
| **Ignore entirely** | Routine July/December shutdown weeks; anything with no plant named; aggregate US headcount changes | See 5.3 |

### 5.3 Avoiding the two false positives that will otherwise ruin this

**(a) Seasonal shutdowns.** Deere shuts plants every July and again around the December holidays.
**Only a deviation from the seasonal norm carries information**, and the deviation is what must be
encoded — never the raw presence of a shutdown.

The problem is that the seasonal baseline **is not publicly available**. Routine shutdown weeks are
negotiated into the UAW master agreement, never disclosed, never WARN-reportable. So the tracker
must not attempt to compare week counts. Use the observable proxy instead:

> **Rule: the tracked variable is the presence or absence of an *extended* or explicitly
> "inventory adjustment" shutdown — one that generates press coverage or a WARN filing precisely
> because it is not routine.** A routine shutdown generates neither. The December-2024 Ottumwa
> four-week inventory-adjustment shutdown is the template of a real signal; a July week of
> silence at every plant is the template of nothing.

Two mechanical guards on top of that:
- **Compare like windows, not like quarters.** Deere's fiscal quarter ends drift by up to a week
  (FY2025 Q3 ended 2025-07-27; FY2026 Q3 ended 2026-08-02). A shutdown can move between quarters
  with no change in the schedule. Always check the two fiscal calendars before reading a July or
  August event.
- **Never treat news silence in July as an observation.** Plant-level coverage thins in mid-summer
  and the search index lags. Absence of stories in the most recent 4–6 weeks is unverified, not
  zero.

**(b) Reading the aggregate instead of the plant list.** This is the error the backtest caught,
and it is worth more than any threshold: **FY2025 Q4 showed 339 layoffs effective in the exact
quarter all three segments turned positive.** Enforce it as a hard rule:

> **Every event must be mapped to a plant, then to a segment and geo cell via `PLANT_MAP.md`,
> before any conclusion is drawn. Never sum across segments.**
> Waterloo / East Moline / Moline / Ankeny / Valley City → PPA · Dubuque / Davenport /
> Kernersville / Coffeyville → CF · Ottumwa / Horicon / Augusta / Greeneville → SAT.

Two further de-duplication traps in the current data:
- **Ramos Arizpe hiring and Waterloo cab-line layoffs are partly the same event** — the large-
  tractor cab line moved from Waterloo to Mexico. Do not count both.
- `production_events.csv` rows for 2024–25 **overlap** `warn_layoffs.csv`. Deduplicate before
  combining.

### 5.4 What to build next, in priority order

1. **Direct state WARN pulls for Kansas, Georgia, Louisiana, North Dakota, Michigan, Minnesota and
   Tennessee.** These blocked scripted access. Coffeyville, Augusta, Thibodaux, Valley City and
   Fargo are currently invisible in both directions.
2. **Any non-US plant labour source at all.** Germany (Mannheim, Zweibrücken, Bruchsal) has
   *Kurzarbeit* short-time-working registrations that are semi-public; Brazil has *férias
   coletivas* collective-vacation announcements that local press covers. **46% of revenue is non-US
   and this indicator currently sees none of it** — the single largest structural weakness.
3. **A weekly cron on `fetch_deere_jobs.py`.** The 2026-08-16 census (201 postings, 83 US) is a
   baseline with no history behind it and **says nothing about Q3** — it was taken two weeks after
   the quarter closed. Its value begins with the second observation. Note the two halves are
   different instruments: all 8 Production/Maintenance postings are in Germany and France; zero in
   the US, because Deere fills US hourly from the UAW recall list and those requisitions never hit
   the external board (proof: the 30 new Dubuque hires announced 11 June never appeared on it).
4. **Plant-level headcount denominators** for the 41 sites that have none, starting with Davenport.
   Without a denominator, "308 laid off at Waterloo" cannot be expressed as a share of capacity.

### 5.5 What to expect this tracker to deliver

Be realistic about it, or it will be over-trusted:

- **It will reliably tell you a quarter did not go badly wrong**, from inside the quarter. That is
  worth real money three days before a print.
- **It will tell you which segment is diverging**, via composition, before the segment tables do.
- **It will not give you a revenue number.** There is no plant-level output or revenue disclosure
  anywhere in Deere's reporting, so no plant-share-of-segment weight exists and none can be
  constructed. Any conversion from headcount to dollars is invention.
- **It will not predict a turn.** The backtest says so plainly: 38%, 25% and 38% directional hit
  rates on n = 8, losing to naive persistence in all three segments.

---

## 6. Honest limits

- FY2026 Q3 is **unreported**. Nothing here is an actual. The call is 2026-08-20.
- **n is small everywhere.** Ten annual observations for the calibration; eight to ten quarterly
  observations spanning one cycle turn for the lead-lag test. Nothing here would survive a
  demanding significance test, and the quarterly correlations are largely a shared trend through a
  single V.
- The **summer-shutdown comparison could not be built** and was not estimated. This is the largest
  single hole in the Q3 read, and the fiscal-calendar boundary shift makes it worse.
- **No non-US plant events exist** in this dataset, against 46% of revenue.
- **Plant headcount is not a panel.** Each figure is an independently sourced point estimate,
  mostly from stories written *because* of a layoff. Differencing two rows for the same plant is
  only valid where scopes match — Waterloo Mar-2024 vs Oct-2024 is comparable; Horizontina Feb-2024
  vs Feb-2025 is not.
- Deere's own cumulative recall counter reached **400** by 2026-06-11 while individually traceable
  events sum to **371**. The ~29 gap is recorded, not reconciled by inventing a row. The 400 is the
  company's rounded number quoted in local press with inconsistent scope ("across the United
  States" vs "across Iowa and Illinois") and is treated as a floor. It also ignores attrition,
  which is unobservable.
- The **2026-07-29 UAW Local 838 event year is inferred**, not confirmed on the page.
- **Export series are whole-industry**, not Deere-only: AGCO, CNH, Caterpillar, Kubota, Claas and
  others are inside them and cannot be separated out. HS 8701 additionally includes highway truck
  tractors and is not an agriculture signal at all.
