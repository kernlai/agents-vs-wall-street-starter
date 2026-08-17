# Deere segment operating-profit bridge — extraction, reconciliation, variance decomposition

**Companion to** `de_operating_profit_bridge.csv` (688 rows, 69 segment-quarters, `series_id = de_op_bridge`).
**Corpus** `challenge/offline-data/deere` (310 docs, frozen 2026-08-14). **Run date** 2026-08-16.
**Scripts** (stdlib only, reproducible in order):

| step | script |
|---|---|
| 1 | `scripts/data/de_bridge_01_endpoints.py` — segment operating profit + net sales from the 8-K tables |
| 2 | `scripts/data/de_bridge_02_dump.py` — raw dump of every bridge block, used to classify OCR shapes |
| 2b | `scripts/data/de_bridge_narrative.py` — independent driver-sign expectations from 8-K MD&A prose |
| 3 | `scripts/data/de_bridge_03_extract.py` — shape-aware parse + arithmetic reconciliation |
| 4 | `scripts/data/de_bridge_04_csv_analysis.py` — CSV writer + variance decomposition |

**Q3 FY2026 has not been reported.** Nothing in this file is Q3 FY2026 actuals. The latest bridge is
Q2 FY2026 (quarter ended 2026-05-03, reported 2026-05-21). The `INDEX.md` row labelled
"2026-05-21 | Call Transcript | Q3 2026" is mislabelled Q2 material and was not used as Q3 data.

---

## 1. Coverage and reconciliation result

### How many decks actually carry a bridge

The brief anticipated 44 decks with an operating-profit bridge. **In this corpus there are 26.**
Of 51 slide documents, only 26 contain a quantified waterfall; the 2015–2019 decks (21 documents)
give the drivers as unquantified bullets only ("+ Shipment volumes + Price realization − Production
costs"), and four documents are investor-day / investor-presentation decks with no bridge. The
quantified bridge starts with the 1Q FY2020 deck (2020-02-21) and runs to 2Q FY2026.

### Reconciled vs rejected, per segment

A bridge is accepted only when `opening + Σ components == closing` **exactly**, with both endpoints
taken from the 8-K segment table, never from the slide.

| segment | quarters reconciled | rejected | span |
|---|---|---|---|
| PPA | **21** | **1** (2023 Q2) | 2021 Q1 – 2026 Q2 |
| SAT | **22** | 0 | 2021 Q1 – 2026 Q2 |
| CF  | **26** | 0 | 2020 Q1 – 2026 Q2 |
| **total in CSV** | **69** | **1** | |
| *Agriculture & Turf (pre-FY2021 segment)* | *4* | *0* | *2020 Q1 – 2020 Q4* |

PPA and SAT do not exist before FY2021 — Deere reorganised into PPA / SAT / CF effective FY2021, so
the four FY2020 decks carry an **Agriculture & Turf** bridge instead. Those four reconcile cleanly but
are **excluded from the CSV**, which is restricted to `PPA|SAT|CF` as specified; they are reported here
for completeness. The FY2020 **CF** bridges are in the CSV, flagged in `notes` as being on the
as-reported pre-FY2021 basis (Deere restated FY2020 CF when it reorganised, so those four quarters are
not perfectly comparable with FY2021+).

**The single rejection — 2023 Q2 PPA — is an honest failure, not a parsing shortfall.** The OCR of that
chart states an opening bar of "$1,043" where the 8-K says 2Q FY2022 PPA operating profit was $1,057,
lists only six of the eight bars, and folds the closing bar ($2,170) into the "Other" label. No
assignment of the transcribed numbers reconciles 1,057 → 2,170. Rather than force it, it is dropped.
Earlier drafts of the parser *did* force it, producing a bridge with `other = +2,170` and
`currency = −483`; a guard now rejects any candidate in which a component equals an endpoint.

### Quality flags carried in the CSV `notes` column

| flag | count | detail |
|---|---|---|
| exact parse, nothing inferred | 66 / 69 | |
| one component recovered as the arithmetic residual | 3 / 69 | 2024 Q3 PPA `other`, 2024 Q2 SAT `other`, 2026 Q2 CF `other` — in each case the OCR merged the "Other" label into the closing bar or dropped its small value |
| slide's own endpoint bars disagree with the 8-K | 3 / 69 | 2024 Q1 SAT, 2024 Q2 SAT, 2024 Q3 PPA — in all three the slide simply omits or garbles one endpoint label; the 8-K value was used |
| needed a documented tie-break | 29 / 69 | see §2 |

---

## 2. The OCR trap, and how it was defused

The brief warned that values appear "in scrambled order relative to their labels" and that positional
matching is unsafe. That is correct, but in this corpus the corruption takes **six** distinct forms,
and only some of them are fixable by arithmetic. Being precise about which is the point of this
section, because **the sum test is invariant to a permutation of the components** — an assignment that
swaps Price and Volume/Mix still reconciles perfectly. Arithmetic alone cannot catch a label swap.

| # | failure mode | example | fix |
|---|---|---|---|
| a | four different OCR shapes across 2020-2026: keyed JSON, parallel label/value **arrays**, `{category,value}` object lists, and English prose | 2022 Q3 PPA is keyed JSON; 2022 Q2 SAT is object list; 2026 Q2 is prose | shape detection, then pair *inside* the shape |
| b | in the array shape every label is emitted before every value, and the two arrays appear in **either** order | 2021 Q1 PPA lists 10 labels then 10 values; a proximity read pairs the last label with the first value, reversing the whole bridge | index pairing, never character position |
| c | in the array shape the label order is itself permuted | 2022 Q2 PPA lists `Price` before `Volume/Mix` | index pairing preserves the OCR's own label↔value pairing; validated against the 8-K narrative ("Operating profit rose primarily due to **price realization** and higher shipment volumes" → Price 502 > Volume/Mix 212 ✓) |
| d | in prose, a short label sits closer to the *previous* bar's number than to its own | `Special Items: $0` / `Other: +$8` — "Other" is nearer the `$0` | order-preserving alignment (i-th slot owns the i-th number), with a sliding window so a preceding net-sales chart cannot shift it |
| e | **the sign convention flips between blocks.** In most, `($90)` = −90. In some, parentheses are mere delimiters and negatives are written `-$46`, so `($741)` = **+741** | 2023 Q1 PPA: `"Price" ($741) ... "Currency" (-$46)`. Read as −741 the bridge misses by 1,482 | both conventions are tried; only one reconciles (296 + 613 + 741 − 46 − 15 − 256 − 127 + 53 − 51 = 1,208 ✓). 2 quarters resolved this way |
| f | bars go missing, or the label row is offset by one because the OCR transcribes the first bar as an **unlabelled stray** | 2024 Q2 PPA: seven labelled bars plus "a gray bar with a value of ($627) positioned between the 2Q 2023 bar and the Volume/Mix bar" | two candidates generated (stray = Volume/Mix with labels shifted right, vs. stray = Other); both reconcile; the 8-K narrative decides |

### The independent check that catches what arithmetic cannot

Because permutations survive the sum test, a second, **non-numeric** source was used: the 8-K MD&A
sentence for the same segment and quarter. *"Operating profit decreased due to lower shipment volumes
and higher production costs, partially offset by price realization"* pins the **sign** of several bridge
components without touching any of the slide's numbers. Drivers in the main clause take the sign of the
verb; drivers after "partially offset by" take the opposite sign.

Result: **132 driver signs across 56 segment-quarters, 132 agree, 0 conflict (100%).**

This check also arbitrated the ambiguous cases. 31 blocks admitted more than one reconciling
assignment; tie-breaks were applied in this order and their use is recorded per row:

1. **8-K narrative driver signs** — decided 19 of the 69 CSV rows (21 including the AT bridges).
2. **Most explicit parse wins** (a shape parser or order-preserving alignment reads a stated pairing;
   greedy and positional reads *infer* one) — decided 10 of the 69 (11 including AT).
3. Volume/Mix must move with the segment's own net-sales direction — needed for 0 blocks in the end.
4. Otherwise: reject. No block reached this step.

Two cases are worth naming because the narrative overturned the literal OCR pairing:
**2023 Q4 CF** and **2024 Q1 CF**. The prose pairs `Volume/Mix → $214` and `Price → ($28)`
(4Q23), but the 8-K says profit *"improved primarily due to price realization"* and separately cites
*"higher production costs"*, *"less-favorable sales mix"* and *"unfavorable currency"*. The one-slot
shift (Price +214, Volume/Mix −8, production costs −84, currency −28, special items +32) matches the
narrative on five independent counts; the literal read matches on none and contradicts it on price.
It also passes an economic sanity check: CF sales rose $369m that quarter, and a $214m *volume* profit
contribution would imply a 58% incremental margin, while a $214m *price* contribution is ordinary.
**These two rows are the least certain in the file.**

---

## 3. Variance decomposition — the test the hypothesis turns on

The bridge is an exact identity, `ΔOP = Σ c_i`, so `Var(ΔOP) = Σ Cov(c_i, ΔOP)`. Each component's
`Cov(c_i, ΔOP) / Var(ΔOP)` is therefore an **exact, additive share of variance** that sums to 100%.
Shares can be negative: a component that moves against the total is a *stabiliser*, not a driver.
ΔOP here is the year-over-year change in segment operating profit — precisely what the bridge measures.

### Production & Precision Ag — n = 21 quarters (2021 Q1 – 2026 Q2)

sd of ΔOP = **554 USDm**

| component | sd (USDm) | variance share | corr with ΔOP |
|---|---:|---:|---:|
| **volume/mix** | 544 | **89.9%** | 0.92 |
| price | 286 | 40.9% | 0.79 |
| currency | 49 | 0.1% | 0.01 |
| warranty | 33 | 1.7% | 0.28 |
| **production costs** | 228 | **−24.3%** | −0.59 |
| SA&G / R&D | 56 | −6.6% | −0.65 |
| special items | 49 | 1.6% | 0.18 |
| other | 36 | −3.4% | −0.51 |
| **sum** | | **100.0%** | |

### Small Ag & Turf — n = 22 quarters (2021 Q1 – 2026 Q2)

sd of ΔOP = **200 USDm**

| component | sd (USDm) | variance share | corr with ΔOP |
|---|---:|---:|---:|
| **volume/mix** | 187 | **77.1%** | 0.82 |
| price | 129 | 25.4% | 0.39 |
| currency | 20 | 1.6% | 0.17 |
| warranty | 27 | 3.4% | 0.25 |
| **production costs** | 120 | **−8.1%** | −0.13 |
| SA&G / R&D | 24 | −2.0% | −0.17 |
| special items | 26 | 5.0% | 0.38 |
| other | 26 | −2.5% | −0.19 |
| **sum** | | **100.0%** | |

### Construction & Forestry — n = 26 quarters (2020 Q1 – 2026 Q2)

sd of ΔOP = **222 USDm**

| component | sd (USDm) | variance share | corr with ΔOP |
|---|---:|---:|---:|
| **volume/mix** | 181 | **64.9%** | 0.80 |
| price | 151 | 42.2% | 0.62 |
| currency | 16 | 1.7% | 0.24 |
| warranty | 20 | −1.0% | −0.11 |
| **production costs** | 92 | **−20.7%** | −0.50 |
| SA&G / R&D | 23 | −1.7% | −0.16 |
| special items | 88 | 12.0% | 0.30 |
| other | 33 | 2.5% | 0.17 |
| **sum** | | **100.0%** | |

### Grouped answer to the question as posed

| grouping | PPA (n=21) | SAT (n=22) | CF (n=26) | pooled (n=69) |
|---|---:|---:|---:|---:|
| volume/mix | **+89.9%** | **+77.1%** | **+64.9%** | **+85.6%** |
| production costs + warranty | **−22.6%** | **−4.7%** | **−21.7%** | **−19.7%** |
| price | +40.9% | +25.4% | +42.2% | +37.6% |
| all revenue-linked (volume/mix + price + currency) | +131.0% | +104.2% | +108.9% | +123.8% |
| quarters where \|volume/mix\| > \|production costs + warranty\| | 14/21 (67%) | 13/22 (59%) | 15/26 (58%) | 42/69 (61%) |

Restricting to the current down-cycle (FY2024 Q1 onward, n = 10 per segment) makes it starker, not
weaker: volume/mix carries 115% (PPA), 101% (SAT), 100% (CF) of the variance, with production costs +
warranty at −15%, +0%, −19%.

### Volume/mix *is* the revenue line

| segment | corr(Δ segment net sales, volume/mix bar) | corr(Δ net sales, ΔOP) | flow-through: ΔOP per $1 Δ net sales |
|---|---:|---:|---:|
| PPA (n=21) | **0.99** | 0.94 | 0.383 |
| SAT (n=22) | **0.98** | 0.82 | 0.299 |
| CF (n=26) | **0.96** | 0.86 | 0.297 |

The volume/mix bar is essentially a linear transform of the segment's revenue change. Whatever moves
revenue moves the single largest term in the profit bridge, at roughly **30–38 cents of operating
profit per dollar of sales**.

---

## 4. Verdict on the hypothesis

The hypothesis has two clauses. This work can test the second directly and speaks to the modelling
consequence; it cannot test the first (whether Q3's order book was already set at the time of the Q2
report) — that requires the order-book / early-order-program evidence, not the margin bridge.

**Clause tested: *"The thing suppliers and input costs actually move is PROFIT, not revenue."***
**CONTRADICTED, clearly and in every segment.** Production costs plus warranty do not drive
quarter-to-quarter variation in operating profit — their combined variance share is **negative**
(−22.6% PPA, −4.7% SAT, −21.7% CF). They are counter-cyclical stabilisers: production costs improve
when volumes collapse and worsen when volumes surge (corr with ΔOP of −0.59 / −0.13 / −0.50).
Volume/mix carries **65–90%** of the variance on its own. The answer to the question as posed —
volume/mix, or production costs plus warranty? — is **volume/mix, by a wide margin, in all three
segments and in the pooled sample.**

**Where the hypothesis nonetheless earns something.** Its *modelling consequence* — a tighter relative
range on revenue than on profit — is supported, but for a different reason than stated. It is
operating leverage, not cost volatility:

| segment | sd(Δ net sales) as % of mean sales | sd(ΔOP) as % of mean operating profit |
|---|---:|---:|
| PPA | 27.6% | **56.5%** |
| SAT | 18.2% | **43.0%** |
| CF | 21.4% | **54.9%** |

Profit swings about twice as hard as revenue in percentage terms. So a wider *relative* band on
operating profit and EPS than on revenue is right — but it follows from the ~0.30–0.38 flow-through
applied to a smaller profit base, **not** from suppliers and input costs being the dominant source of
surprise.

**And a genuine caveat in the hypothesis's favour, in absolute terms.** Knowing revenue exactly does
not make profit known. Removing volume/mix from PPA's ΔOP leaves sd = **226 USDm** (17% of the
variance, but a large absolute number against a segment earning $580m–$1.1bn a quarter); removing the
whole revenue-linked block (volume/mix + price + currency) leaves sd = **291 USDm**. For SAT and CF the
residuals are 116 and 135 USDm. So: if a revenue forecast is accurate to, say, ±5% of PPA's ~$5bn
quarter (±$250m, ≈ ±$96m of profit at 0.383 flow-through), the *remaining* cost-and-other uncertainty
of roughly ±$220m is in fact the larger of the two. **Conditional on a good revenue forecast, the cost
lines are the bigger residual — but unconditionally, and as a driver of realised variation, they are
not.** The hypothesis is right about where the *residual* uncertainty sits and wrong about what
*drives* the variation.

**Net: PARTIALLY SUPPORTS, with the central claim contradicted.** Do not model PPA operating profit as
"revenue anchored tight, margin wide and independent." Model it as revenue × a ~0.30–0.38 incremental
flow-through, and then add a cost-side band of roughly ±$220m (PPA) around that, which is what the
bridge residual actually looks like.

### Forecast-relevant priors for Q3 FY2026 PPA (a target of the wider task)

Opening for the Q3 FY2026 PPA bridge is fixed and known: **3Q FY2025 PPA operating profit = $580m**
(8-K 2025-08-15). The historical Q3 distribution of each bar (FY2021–FY2025, n = 5, a very small
sample — treat as orientation, not as a distribution):

| component | Q3 values FY21→FY25 (USDm) | Q3 mean | all-quarter mean | all-quarter sd |
|---|---|---:|---:|---:|
| volume/mix | 325, 492, 27, −847, −494 | −99 | −138 | 544 |
| price | 257, 646, 723, 177, −40 | 353 | 297 | 286 |
| currency | 85, −47, −41, 24, −52 | −6 | −5 | 49 |
| warranty | −31, −2, 4, 48, −45 | −5 | −3 | 33 |
| production costs | −248, −535, −77, −5, 69 | −159 | −156 | 228 |
| SA&G / R&D | −44, −140, −74, 10, −17 | −53 | −36 | 56 |
| special items | 0, 1, −1, −62, 34 | −6 | 1 | 49 |
| other | −43, −28, −72, 35, −37 | −29 | −10 | 36 |

Note the regime break: price realization, worth +$177m to +$723m in FY2021–FY2024, turned **negative**
(−$40m) in 3Q FY2025 and was −$4m in 1Q FY2026 and +$49m in 2Q FY2026. The FY2021–FY2023 price bars
should not be pooled with the current cycle.

---

## 5. Caveats

1. **Small samples throughout.** n = 21 / 22 / 26 per segment; the FY2024+ subsample is n = 10. The
   correlations of 0.96–0.99 between Δ net sales and the volume/mix bar are near-mechanical (the bar is
   constructed from the volume and mix of the same shipments) and should not be read as a discovered
   empirical regularity. The variance shares are exact decompositions of *this* sample, not population
   estimates; with n ≈ 20 the standard error on a share of this size is easily ±10pp.
2. **The sample straddles two very different regimes** — the 2021–2023 price-and-volume boom and the
   2024–2026 down-cycle. Volume/mix dominance holds in both, and is stronger in the recent one, which
   is reassuring; but the *level* of every bar differs sharply between them.
3. **Two CF rows (2023 Q4, 2024 Q1) rest on the 8-K narrative overriding the literal OCR pairing.**
   Reversing that choice moves ~$220m and ~$95m between the volume/mix and price bars in those two
   quarters. This was re-run: with the literal OCR reading, CF's volume/mix share goes 64.9% → 66.2%,
   price 42.2% → 40.9%, production costs −20.7% → −20.2%. The individual rows would be wrong but the
   decomposition and the verdict are unaffected.
4. **FY2020 CF is on the pre-reorganisation basis.** Those four quarters are flagged in `notes`.
   Excluding them leaves CF at n = 22 and does not materially change the shares.
5. **The four Agriculture & Turf bridges (FY2020) are not in the CSV**, per the `PPA|SAT|CF` spec.
6. **The narrative sign check covers 56 of 69 segment-quarters**, because the 8-K only names two to
   four drivers per segment per quarter. 13 segment-quarters have no narrative coverage and rest on the
   arithmetic and the shape parse alone.
7. **This file contains no Q3 FY2026 data.** Deere reports Q3 FY2026 on 2026-08-20.
