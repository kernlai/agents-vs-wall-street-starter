# Deere & Company — layoff, furlough and recall timeline from WARN notices and news

Companion to `warn_layoffs.csv`. Built 2026-08-16. Deere has **not** reported FY2026 Q3
(quarter runs ~2026-05-04 to 2026-08-02; earnings call 2026-08-20 09:00 US Central).
Nothing in this file is a Q3 FY2026 actual.

Rebuild with `scripts/data/de_warn_layoffs.py`.

---

## 1. Headline finding

**Deere filed zero WARN notices anywhere in Iowa or Illinois in calendar 2026, and announced
callbacks or new hiring on at least six separate dates instead. The last Deere layoff notice in
either state was 2025-09-17. By 2026-06-11 — mid-Q3 — Deere said 400 US employees had returned
to work or been hired since January, and Dubuque Works had exhausted its recall list and moved to
hiring 30 net-new people.**

This is not a forecast. FY2026 Q3 is over. The employment record inside the quarter is one of net
addition at every Deere plant that reported anything at all.

Three qualifications that matter, developed below:

1. The recalls are **segment-selective**. Every 2026 callback landed at Dubuque and Davenport
   (Construction & Forestry), Coffeyville (components) or Waterloo (large ag tractors).
   **Harvester Works in East Moline — combines, the core of Production & Precision Ag — received
   nothing.** That matches PPA guidance of -5 to -10% and PPA's -14% in Q2 FY2026.
2. Management told the Q2 call (2026-05-21) that large-ag production is **back-half and
   specifically Q4-weighted**: "a little bit better absorption in the fourth quarter as production
   rates are significantly higher … that's just the way the order book built this year for a much
   heavier fourth quarter with respect to our large tractors." The Waterloo February callbacks feed
   Q4 more than Q3.
3. The rate of new callback announcements **decelerated** inside Q3 (222 announced in FY2026 Q2,
   50 in FY2026 Q3). Part of that is a ceiling effect — Dubuque ran out of people with recall
   rights — but it is a deceleration nonetheless.

---

## 2. What was actually searched, and what was found

| Source | Coverage obtained | Deere records | Method |
|---|---|---|---|
| **Iowa Workforce Development WARN** | 553 notices, **2021-08-18 → 2026-08-13** (all employers) | **28** | Page embeds a Tableau Public viz; pulled the workbook `.twb` (a zip of `.hyper` extracts) and read it with `tableauhyperapi` |
| **Illinois DCEO monthly WARN reports** | **331 monthly reports, 1999 → July 2026** (PDF pre-2020, XLSX after) | **4 Deere + 1 Deere-site contractor** | Downloaded the full archive, scanned XLSX shared-strings and `pdftotext` output |
| **Wisconsin DWD layoff notices** | 635 notices **2020-01-02 → 2026-08-12**, plus static 2016–2019 pages | **0** | Data lives in a public Google Sheet behind the page; pulled via the `gviz` CSV endpoint |
| Kansas, Georgia, Louisiana, Michigan, Minnesota, N. Dakota, Tennessee | **not obtained** (403 / dead endpoints), except Tennessee's PDF index which shows no Deere filename | — | See gaps, §7 |
| News, trade press, Deere press releases, UAW | 2014 → Aug 2026, targeted | 12 events | Web search + fetch |

Iowa's WARN dataset only begins 2021-08-18, so the 2013–2021 target window is covered for Illinois
(back to 1999) but **not** for Iowa. Everything before 2021 in Iowa is therefore invisible to this
build, and any "Deere Iowa layoffs in 2015" number circulating in secondary coverage could not be
verified against a primary state record here.

---

## 3. Why WARN systematically undercounts Deere

Three structural reasons, all confirmed by cases in this dataset. They matter more than any single
number, because they determine when the indicator will and will not fire.

1. **Site-size thresholds.** Illinois requires notice at 33% of the site workforce or 250+ workers.
   Harvester Works employs roughly 2,000. Deere's August 2025 cut of **115** workers there was
   real, announced, and produced **no Illinois WARN record at all** — I verified its absence in the
   August, September and October 2025 monthly reports. Iowa's threshold is lower (25), which is why
   Iowa captures 28 Deere notices and Illinois only 4.
2. **The federal six-month rule.** Layoffs expected to last under six months are exempt. Deere's
   ag-cycle actions are frequently framed as recallable, with employees retaining recall rights
   "for a period equal to their length of service". Indefinite layoffs do get filed; short furloughs
   and shutdown weeks never do.
3. **Shutdown weeks are invisible.** Deere's summer and holiday shutdowns are scheduled downtime,
   not layoffs. **No WARN notice will ever exist for them.** See §6.

Practical consequence for the tracker: **WARN is a high-precision, low-recall signal.** When a
notice appears, something large and durable is happening. When none appears, it does not follow
that nothing happened — but in 2026 the *absence* of notices is corroborated by the *presence* of
recall announcements pointing the other way, which is a much stronger joint reading than either
alone.

---

## 4. The critical window: FY2026 Q3 (2026-05-04 → 2026-08-02)

Everything found inside the quarter:

| Date | Site | Event | People |
|---|---|---|---|
| 2026-06-11 | Dubuque Works (CF) | **New hiring** — callback list exhausted | +30 |
| 2026-06-11 | Davenport Works (CF) | Recall | +20 |
| 2026-06-11 | — | Deere states cumulative since January | 400 returned/hired |
| 2026-07-29 | Waterloo (UAW Local 838) | Union counters Deere's two-year contract-extension offer; Deere rejects | — |
| whole quarter | Iowa | WARN notices filed by Deere | **0** |
| whole quarter | Illinois | WARN notices filed by Deere | **0** |
| whole quarter | Wisconsin | WARN notices filed by Deere | **0** |

The Iowa zero is a hard zero, not a data gap: the state database contains 77 CY2026 notices from
other employers — including CNH Industrial closing lines in Burlington and Whirlpool cutting 288 at
Amana in June — and is current to 2026-08-13, past the end of Deere's quarter. Deere is simply not
in it.

The 2026-06-11 Dubuque hiring event is the single most informative datapoint. Dubuque cut 133
people by WARN in 2024 (99 on 2024-06-28, 34 on 2024-07-24). By mid-Q3 FY2026 it had recalled
everyone with recall rights (24 in January, 27 in March, 21 in April) and moved to external
hiring. A plant does not hire off the street while producing below plan.

**Counter-signal to keep on the page:** Deere's own words on 2026-07-29, rejecting the UAW counter,
were that it is contrary to providing "continuity and certainty **when equipment demand is down**."
Management was still characterising large-ag demand as down at the very end of the quarter. Note
the year on this item is inferred from search context, not confirmed on the page — treat as medium
confidence.

---

## 5. Historical pattern: layoff waves against reported segment volumes

Layoffs bucketed into Deere fiscal quarters by **effective date** (the date production capacity
actually comes out), recalls by announcement date, against reported segment net sales (USDm) and
y/y change from `data/deere/de_segments_modern.csv`.

| Fiscal Q | Layoffs effective | Recalls announced | PPA | PPA y/y | CF | CF y/y | SAT | SAT y/y |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| FY2024 Q1 | 0 | 0 | 4,849 | -6.7% | 3,212 | +0.3% | 2,425 | -19.2% |
| FY2024 Q2 | 368 | 0 | 6,581 | -15.9% | 3,844 | -6.5% | 3,185 | -23.2% |
| FY2024 Q3 | 895 | 0 | 5,099 | -25.1% | 3,235 | -13.5% | 3,053 | -18.3% |
| FY2024 Q4 | 934 | 0 | 4,305 | **-38.2%** | 2,664 | -28.8% | 2,306 | -25.5% |
| FY2025 Q1 | 192 | 0 | 3,067 | -36.7% | 1,994 | **-37.9%** | 1,748 | **-27.9%** |
| FY2025 Q2 | 122 | 0 | 5,230 | -20.5% | 2,947 | -23.3% | 2,994 | -6.0% |
| FY2025 Q3 | 72 | 0 | 4,273 | -16.2% | 3,059 | -5.4% | 3,025 | -0.9% |
| FY2025 Q4 | 339 | 0 | 4,740 | **+10.1%** | 3,382 | +27.0% | 2,457 | +6.5% |
| FY2026 Q1 | 40 | 99 | 3,163 | +3.1% | 2,670 | +33.9% | 2,168 | +24.0% |
| FY2026 Q2 | 0 | 222 | 4,503 | -13.9% | 3,790 | +28.6% | 3,485 | +16.4% |
| **FY2026 Q3** | **0** | **50** | ? | ? | ? | ? | ? | ? |

What this actually shows, stated conservatively:

- **The layoff peak and the volume trough are close to coincident, with the layoff running one
  quarter early at most.** Layoffs effective peaked in FY2024 Q3–Q4 (895, then 934). PPA's y/y
  trough is FY2024 Q4 (-38.2%); CF's and SAT's are FY2025 Q1 (-37.9%, -27.9%). This is exactly what
  the underproduction disclosure predicts: Deere pulls capacity out *as* shipments fall, not before,
  because the schedule is already set months ahead and the layoff is the schedule cut being
  executed.
- **The layoff run-down led the y/y inflection by about two quarters.** Layoffs effective collapsed
  from 934 (FY2024 Q4) to 192 → 122 → 72 across FY2025 Q1–Q3. All three segments turned positive
  y/y in FY2025 Q4. A two-quarter lead from "layoffs stop" to "y/y goes positive" is the single
  most usable regularity in this table.
- **The signal is asymmetric and plant-specific.** The FY2025 Q4 bucket shows 339 layoffs effective
  *in the same quarter that all three segments turned positive y/y*. Those 339 were the August–
  September 2025 combine and foundry cuts (Harvester Works 115, Moline Seeding 52, Waterloo Foundry
  71, Des Moines 40, Waterloo 101). Aggregate headcount said "still cutting"; the plant mix said
  "cutting combines, not construction". Two quarters later PPA printed -13.9% while CF printed
  +28.6%. **Reading the aggregate would have been wrong. Reading the plant list was right.**
- **n is small.** Eleven quarters, one cycle turn. Treat these as regularities in a single episode,
  not as estimated coefficients.

The 2014 comparison anchors the amplitude. The single largest Deere WARN event in the whole
1999–2026 Illinois archive is **425 workers at Harvester Works, notice 2014-08-20, effective
2014-10-20, permanent, UAW Local 865**. The 2024 wave is larger in total (2,167 in Iowa+Illinois per
WARN-based reporting) but more fragmented — 20+ notices across seven sites rather than one.

---

## 6. Summer shutdown weeks: the question I could not answer, and a trap

The brief asks whether 2026's summer shutdowns were longer or shorter than normal. **I could not
establish either the baseline or the 2026 figure from public sources, and I am not going to
estimate them.**

Deere schedules shutdown weeks plant by plant through the UAW locals. They are not WARN-reportable,
not in the 10-K, and not in any press release I could find. Local coverage of shutdown *scheduling*
(as opposed to layoffs) has largely disappeared behind paywalls.

**Trap, flagged explicitly.** Web search repeatedly surfaced a Waterloo–Cedar Falls Courier article,
"Deere changes summer shutdown", and asserted that Deere moved the Waterloo summer shutdown from
late July/early August to the last two weeks of June "effective in 2026". Fetching the page with a
crawler user-agent returns
`<time datetime="2006-08-04T00:00:00-05:00">Aug 4, 2006</time>`. **The article is from 2006.** The
"2026" was a search-summary artefact — almost certainly the article says 2007. I have not used it.

If someone does establish the real 2026 schedule, the thing to test is this: FY2025 Q3 ended
2025-07-27 and FY2026 Q3 ended 2026-08-02. A late-July/early-August shutdown straddles that
boundary differently in the two years. A shutdown that sat partly in FY2025 Q4 but wholly inside
FY2026 Q3 would depress Q3 FY2026 production days y/y *without any change in the underlying
schedule*. That is a live, unquantified risk to the read in §4, and it cuts against the positive
callback signal.

---

## 7. Coverage, gaps and honest limits

**Well covered:** Iowa 2021-08→2026-08 (complete state database); Illinois 1999→2026-07 (complete
monthly archive); Wisconsin 2016→2026-08. These three states hold Waterloo, Dubuque, Davenport,
Des Moines/Ankeny, Ottumwa, East Moline, Moline, Silvis and Horicon — the large-ag and C&F core.

**Not covered — acknowledged blanks, no substitute numbers invented:**

- **Kansas (Coffeyville)** — kansasworks.com returns 403 to scripted requests. Coffeyville appears
  in this file only via the 2026-04-13 news-sourced recall of 8 workers.
- **Georgia (Augusta/Grovetown), Louisiana (Thibodaux), North Dakota (Valley City, Fargo),
  Michigan, Minnesota** — endpoints 403'd or moved. No Deere data from these states, in either
  direction. Augusta and Thibodaux are meaningful turf/C&F sites; their absence is a real hole.
- **Tennessee (Greeneville)** — the state's WARN PDF index was retrieved and contains no Deere
  filename, but I did not open every PDF, so this is a weak negative.
- **Iowa before 2021-08-18** — outside the state database.
- **Shutdown weeks, shift eliminations, overtime changes** — no public series exists.
- **Plant-level headcount** — not in this file; Deere discloses only a total. Without denominators,
  "308 laid off at Waterloo" cannot be turned into a percentage of that plant's capacity.
- **Recall completeness** — Deere's own counter reached 400 by 2026-06-11; the individually
  reported events in this file sum to 371. Roughly 29 recalls were announced too quietly to trace.
  The CSV records both, and does not reconcile them by inventing a row.

**Non-Deere row retained deliberately:** the 2018-09-07 Eurest Services notice (79 workers, food
service at three Deere Quad Cities sites). It is a Deere-site event and useful context, and it is
labelled `CONTRACTOR, NOT DEERE PAYROLL` in its notes and excluded from every aggregate.

---

## 8. How to run this forward (use case B)

Weekly, ~15 minutes, no paid data:

1. **Iowa** — re-download `https://public.tableau.com/workbooks/IowaWARNNotifications.twb`, unzip,
   read the `.hyper`, filter `Company LIKE '%Deere%'`. Fully structured, updated daily, and the
   most sensitive of the three because of the low 25-employee threshold.
2. **Illinois** — pull the newest monthly XLSX from the DCEO archive page and grep
   `xl/sharedStrings.xml` for "Deere". One file a month.
3. **Wisconsin** — refetch the public sheet CSV.
4. **News** — the callback announcements are the leading half of the signal and never appear in
   WARN. Deere puts them on its own newsroom; KCRG, KWQC, WQAD, Telegraph Herald and
   quadcitiesbusiness.com carry them within a day.
5. **Read the plant list, not the total.** The 2025 Q4 row in §5 is the proof: aggregate headcount
   and segment direction disagreed, and the plant mix resolved it. Map every event to its segment
   (Waterloo/East Moline/Moline/Ankeny → PPA; Dubuque/Davenport → CF; Ottumwa/Horicon → SAT) before
   drawing any conclusion.

**Note for whoever runs this:** several state sites and local papers block scripted requests. A
crawler user-agent gets the page and, usefully, the JSON-LD `datePublished` — which is how the 2006
article in §6 was caught. **Always confirm the publication date before using a search summary.**
