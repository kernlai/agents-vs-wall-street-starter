# Deere & Company — currency translation effect on revenue

Companion to `de_currency_effect.csv`. Built 2026-08-16, before Deere's Q3 FY2026 report
(Thursday 2026-08-20, 09:00 US Central). **No Q3 FY2026 actuals exist and none are used here.**
Every Q3 FY2026 number in this file is an estimate and is tagged `source_type=inference` in the CSV.

---

## 1. Headline answer

**Estimated FX translation effect on Q3 FY2026 (three months ending 2026-08-02) revenue:**

| Segment | Effect on yoy net sales | USDm on prior-year base | 1σ band (pp) |
|---|---:|---:|---:|
| Production & Precision Ag | **+1.78 pp** | **+$76m** | +1.14 to +2.42 |
| Small Ag & Turf | **+0.21 pp** | **+$6m** | −0.43 to +0.85 |
| Construction & Forestry | **+0.50 pp** | **+$15m** | −0.14 to +1.14 |
| **Worldwide net sales and revenues** | **+0.83 pp** | **+$99m** | +0.19 to +1.47 |

Bases: PPA 4,273 / SAT 3,025 / CF 3,059 (Q3 FY2025 segment net sales, 8-K basis);
worldwide 12,018 (Q3 FY2025 net sales and revenues).

**The point that matters for the forecast: the FX tailwind collapses in Q3.** Deere just posted
+3 pp (PPA), +2 pp (SAT), +3 pp (CF) of currency in Q2 FY2026, and +4/+2/+4 in Q1. Q3 is roughly
+1.8/+0.2/+0.5. That is a **~2 pp sequential deceleration** in the reported-revenue tailwind,
worth roughly **$210m of revenue that Q2's run-rate would have implied and Q3 will not get**
(the Q2 currency uplift was $305m across the three segments; Q3's is $97m).

The euro is the whole story. EUR/USD averaged 1.1532 over Deere's Q3 FY2026 window against
1.1488 a year earlier — **+0.38%**, versus **+8.40%** in Q2. Brazil is still a large tailwind
(BRL +10.03%) and it is what keeps PPA positive, because Latin America is seasonally at its
heaviest weight in Deere's fiscal Q3.

---

## 2. What Deere actually discloses (and what it does not)

Three distinct disclosures exist in the corpus. They are on different bases and the CSV keeps
them in separate series.

| Disclosure | Where | Unit | Series prefix |
|---|---|---|---|
| Currency translation impact on **net sales** | 10-Q / 10-K MD&A segment tables | whole percentage points | `de_currency_effect_pct_*` |
| Currency bar in the **operating-profit** waterfall | quarterly earnings deck | USDm | `de_currency_effect_opprofit_usdm_*` |
| FY currency-translation **guidance** | Q2 8-K segment-outlook table | percent of FY net sales | `de_currency_effect_guidance_pct_*` |

**Deere does not publish a currency effect on net sales in dollars.** The
`de_currency_effect_usdm_*` series is derived: disclosed pp × prior-year-quarter net sales, taken
from the same MD&A table so the two always share a base. Because Deere rounds the percentage to
whole points, each derived dollar figure carries ±0.5 pp of rounding — around ±$25m on a
$5bn segment. That is stated in every row's `notes`.

### Coverage

- Segment-level pp series (PPA / SAT / CF): **FY2022 Q2 through FY2026 Q2** — 13 quarters,
  39 segment-quarters.
  Before FY2022 Q2 the MD&A gave the split only as worldwide / U.S. & Canada / outside
  U.S. & Canada; those are captured as `de_currency_effect_pct_ww_equip_ops`,
  `_us_canada` and `_outside_us_canada` for **FY2019 Q1 through FY2022 Q1**.
- Operating-profit waterfall currency bars: **42 segment-quarters, FY2021 Q2 to FY2026 Q2**.

### Blank cells are not zeros

In 10 of those 39 segment-quarters the MD&A prints the "Currency translation" row but leaves the
cell empty. That is Deere saying the effect rounds to nothing at 1 pp granularity — it is
information, but it is not the number zero. Those rows are in the CSV with an **empty `value`**
and an explanatory note, so the gap is visible rather than silently missing. The calibration
below is run twice, once discarding them and once reading them as 0, and both results are
reported.

---

## 3. Regional exposure: where Deere's revenue is denominated

Weights come from the ASC 606 revenue-recognition matrix in note 3 of the 10-Q, using the
**prior-year quarter** (three months ended 2025-07-27) — the correct base for a translation
calculation, since translation restates a foreign-currency revenue stream that already existed.

Share of segment revenue by primary geographic market, Q3 FY2025 base:

| Market | PPA | SAT | CF | Total co. |
|---|---:|---:|---:|---:|
| United States | 38.4% | 49.8% | 54.0% | 50.0% |
| Canada | 7.6% | 4.8% | 7.1% | 7.5% |
| Western Europe | 15.4% | 24.5% | 17.6% | 16.9% |
| Central Europe & CIS | 6.9% | 4.2% | 3.3% | 4.5% |
| Latin America | 24.1% | 4.0% | 8.1% | 12.1% |
| Asia / Africa / Oceania / ME | 7.6% | 12.7% | 10.0% | 9.1% |

Note how different the segments are: **PPA is a Brazil story, SAT is a Europe story.** And note
the seasonality — Latin America is 24.1% of PPA in fiscal Q3 versus 18.0% in fiscal Q2. Using
Q2 weights for a Q3 estimate would understate the Brazilian contribution by about a fifth.

### Region → currency baskets (assumption, not disclosure)

Deere does not disclose functional-currency mix, so each geographic market is mapped onto traded
currencies. This is the weakest link in the chain and is marked `source_type=inference`:

| Market | Basket | Reasoning |
|---|---|---|
| United States | USD 100% | no translation exposure |
| Canada | CAD 100% | Deere Canada functional currency |
| Western Europe | EUR 80%, GBP 12%, SEK 5%, CHF 3% | Germany/France/Benelux/Iberia/Italy in euro; UK ag and turf in sterling; Nordics; Switzerland |
| Central Europe & CIS | EUR 100% | PLN/CZK/HUF/RON are managed against the euro and much CE equipment is euro-invoiced; CIS immaterial post-2022 |
| Latin America | BRL 72%, MXN 13%, USD 15% | Brazil dominates (Horizontina, Montenegro manufacturing); Argentine and Andean ag equipment is USD-priced |
| Asia / Africa / Oceania / ME | INR 32%, AUD 20%, CNY 12%, ZAR 6%, JPY 5%, KRW 4%, USD 21% | India (Pune) is the largest Asian operation; Australia/NZ; Gulf states pegged to USD |

Implied share of **worldwide** revenue by currency (Q3 FY2025 base):

USD 53.7% · EUR 17.97% · BRL 8.7% · CAD 7.5% · INR 2.9% · GBP 2.0% · AUD 1.8% · MXN 1.6% ·
CNY 1.1% · SEK 0.8% · ZAR 0.5% · CHF 0.5% · JPY 0.5% · KRW 0.4%

So roughly **46% of Deere's revenue translates**, and the euro bloc (EUR + the euro-managed
Central European currencies) is about 18 points of that — nearly twice Brazil.

---

## 4. Realised FX over the quarter

FRED daily rates, averaged over Deere's exact fiscal-quarter windows
(**2026-05-04 → 2026-08-02** against **2025-04-28 → 2025-07-27**), all expressed as
**USD per unit of foreign currency**, so positive = tailwind to Deere revenue. 62 observations
in each window; the FRED series run through 2026-08-07, so the quarter is fully covered.

| Currency | FRED | Q3 FY26 avg | Q3 FY25 avg | yoy | (Q2 FY26 yoy, for contrast) |
|---|---|---:|---:|---:|---:|
| EUR | DEXUSEU | 1.15324 | 1.14882 | **+0.38%** | +8.40% |
| BRL | DEXBZUS | 0.19707 | 0.17910 | **+10.03%** | +12.38% |
| CAD | DEXCAUS | 0.71625 | 0.72763 | **−1.56%** | +3.86% |
| INR | DEXINUS | 0.010480 | 0.011682 | **−10.29%** | −6.51% |
| MXN | DEXMXUS | 0.05753 | 0.05239 | +9.80% | +15.99% |
| AUD | DEXUSAL | 0.70552 | 0.64900 | +8.71% | +12.26% |
| CNY | DEXCHUS | 0.14744 | 0.13899 | +6.07% | +5.74% |
| ZAR | DEXSFUS | 0.06081 | 0.05578 | +9.02% | +12.84% |
| CHF | DEXSZUS | 1.25275 | 1.22792 | +2.02% | +11.86% |
| SEK | DEXSDUS | 0.10524 | 0.10418 | +1.02% | +11.70% |
| GBP | DEXUSUK | 1.34012 | 1.34795 | −0.58% | +4.91% |
| JPY | DEXJPUS | 0.006234 | 0.006894 | −9.57% | −5.67% |
| KRW | DEXKOUS | 0.000671 | 0.000730 | −8.05% | −1.82% |

The euro's yoy move going from +8.4% to +0.4% is the single largest change in Deere's revenue
translation between Q2 and Q3, and it is not visible in spot rates alone — EUR/USD is roughly
where it was in May. It is a **base effect**: the euro's rally happened in the spring of 2026,
so by the May-to-August window the year-ago comparator has caught up.

---

## 5. The calculation, step by step (PPA, Q3 FY2026)

Translation effect = Σ over regions ( prior-year revenue share × regional FX move ).

| Region | Weight | Basket FX move | Contribution |
|---|---:|---:|---:|
| United States | 0.3841 | +0.00% | +0.000 pp |
| Canada | 0.0764 | −1.56% | −0.120 pp |
| Western Europe | 0.1544 | +0.35% | +0.054 pp |
| Central Europe & CIS | 0.0687 | +0.38% | +0.026 pp |
| Latin America | 0.2406 | +8.50% | **+2.045 pp** |
| Asia / Africa / Oceania / ME | 0.0757 | −1.08% | −0.082 pp |
| **Naive total** | | | **+1.924 pp** |
| × calibration factor 0.926 | | | **+1.782 pp** |
| × prior-year net sales 4,273 | | | **+$76m** |

Same arithmetic for the others: SAT naive +0.231 → **+0.214 pp** (+$6m);
CF naive +0.540 → **+0.500 pp** (+$15m); company naive +0.893 → **+0.827 pp** (+$99m).

For PPA the entire result is Latin America (+2.045 pp, of which Brazil alone is +1.74 pp) minus
Canada and Asia (−0.20 pp) — Europe contributes essentially nothing this quarter.

### The calibration factor, and why it is trustworthy

The naive weighted-move calculation was run against **every quarter where Deere has already
published the answer and a prior-year geographic matrix exists**: 36 segment-quarters spanning
FY2022 Q2 to FY2026 Q2. Fitting `disclosed = k × naive` through the origin:

| Fit | k | RMSE | n |
|---|---:|---:|---:|
| Blank cells discarded | 0.910 | 0.63 pp | 26 |
| Blank cells read as 0 | **0.926** | **0.64 pp** | 36 |
| PPA only (inclusive) | 0.915 | 0.63 pp | 12 |
| SAT only (inclusive) | 0.888 | 0.61 pp | 12 |
| CF only (inclusive) | 0.979 | 0.67 pp | 12 |

The pooled inclusive fit (k = 0.926) is used. A per-segment factor was rejected: the disclosures
are whole percentage points on values of 1–4 pp, so a segment-specific factor is mostly fitting
rounding noise — and in any case the three per-segment factors sit within 0.09 of each other,
so the choice moves the Q3 answer by less than 0.1 pp.

**Sign agreement is 26 out of 26** on the non-blank observations. k slightly below 1 is what
theory predicts: some foreign-market revenue is invoiced in dollars, and Deere's hedging and
intercompany structure damp the raw translation.

Nothing here is fitted to Q3 FY2026 — the calibration window ends at Q2 FY2026, the last
reported quarter.

---

## 6. Cross-check against Deere's own guidance

On 2026-05-21 Deere guided FY2026 currency translation to **+3.0% PPA, +1.0% SAT, +2.0% CF**.
Combining the two reported quarters, this Q3 estimate, and a Q4 scenario that freezes spot at
the 2026-08-03…07 average:

| | Q1 (rep.) | Q2 (rep.) | Q3 (est.) | Q4 (frozen-spot) | FY implied | FY guidance | Gap |
|---|---:|---:|---:|---:|---:|---:|---:|
| PPA | +4% | +3% | +1.78% | +0.81% | **+2.28%** | +3.0% | **−0.7 pp** |
| SAT | +2% | +2% | +0.21% | −0.21% | **+0.94%** | +1.0% | −0.1 pp |
| CF | +4% | +3% | +0.50% | +0.06% | **+1.63%** | +2.0% | −0.4 pp |

Deere's May guidance was set on then-current spot, which embedded the spring euro rally
persisting. It has not. The implication for the 20 August report: **currency is likely to be
called out as a smaller tailwind than the FY guide implies**, and PPA's full-year revenue
guidance (down 5–10%) is carrying roughly 0.7 pp less currency help than assumed — about
**$125m of FY PPA revenue** (0.72 pp on FY2025's 17,311). Q4 is a scenario, not a forecast; rates will move.

---

## 7. Method, validation, and what was thrown away

All parsing is done by scripts in `scripts/data/`, standard library only:

- `de_parse_currency_bridge.py` — MD&A currency rows + slide waterfalls
- `de_parse_geo_matrix.py` — ASC 606 segment × geography matrices
- `de_fx_windows.py` — FRED daily averages over Deere fiscal-quarter windows
- `de_build_currency_effect.py` — weights, calibration, estimate, CSV
- `de_fx_q4_freeze.py` — Q4 spot-freeze scenario

**Geographic matrices.** 61 parsed, **56 reconcile exactly** (every row sums to its stated row
total and every column to its stated column total). The Q2 FY2026 matrix reproduces the verified
ground truth to the dollar. Five fail and are excluded rather than patched:

| File | Problem |
|---|---|
| `2023-11-22__…q4-10k__105844.md` | column total mismatch (27,792 vs stated 22,318) |
| `2024-11-21__…q4-10k__105810.md` | two rows with truncated cell counts |
| `2025-11-26__…q4-10k__469216.md` | product-line block truncated |
| `2026-02-19__…q1-10q__648937.md` | column total mismatch — the **2026-02-26** copy of the same Q1 filing parses clean and is used instead |

All five are annual 10-K layouts or a duplicate of a filing available in clean form, so no
quarter used in the model is lost.

Two structural traps worth recording for anyone reusing this code:

1. In several 10-Qs the three-month and year-to-date matrices are **one contiguous markdown
   table with no blank line between them**. Parsing per-table silently lets the YTD block
   overwrite the quarterly block — the Q3 FY2025 US row reads 5,752 instead of 1,684, and the
   result still validates because the YTD matrix is internally consistent. The parser starts a
   fresh matrix at every "N Months Ended" header row.
2. Deere renamed the sixth market from "Asia, Africa, Australia, New Zealand, and Middle East"
   to "Asia, Africa, Oceania, and Middle East" during fiscal 2023. Matching on "Oceania" drops
   every pre-2023 quarter.

**MD&A currency rows.** The tables are ragged — zero-width padding cells vary row to row, so
column indices cannot be trusted. Values are mapped to periods by cutting the row body into
equal blocks, one per reporting period. This matters: on the naive "first number wins" reading,
SAT Q2 FY2025 would be recorded as −1 pp for the quarter when the −1 is actually the six-month
figure and the quarter was left blank.

**Slide waterfalls.** 78 "Operating Profit Comparison" charts exist in the decks. The chart text
is a prose transcription of an image, and the value sits before the label, after the label, or
in a parallel list depending on the deck. Each candidate reading is accepted **only if the whole
bridge reconciles** — opening bar + every component = closing bar, exactly. **42 pass and are in
the CSV; 36 are discarded.** The rejects are not guessed at. An earlier looser pass returned 60
values of which several were plainly the closing bar rather than the currency bar (PPA "+$873"),
which is why the arithmetic check is the gate.

Note these are **operating-profit** effects, not net-sales effects, and they are much larger
relative to their base — Q2 FY2026 PPA currency was +$75m of operating profit on a segment
whose net-sales currency effect was about +$157m.

---

## 8. Uncertainty — stated honestly

The 1σ band of **±0.64 pp** comes from the calibration RMSE across 36 out-of-sample-in-spirit
observations. Applied to Q3 FY2026 that is roughly **±$27m on PPA, ±$19m on SAT, ±$20m on CF,
±$77m on worldwide revenue**.

Ranked by how much they could move the answer:

1. **The Latin America basket dominates the PPA estimate.** +2.045 pp of PPA's +1.92 pp naive
   total comes from Latin America, +1.74 pp of it from Brazil alone. If the BRL share of Latin
   American revenue is 60% rather than the assumed 72%, PPA drops about 0.27 pp (~$11m); if it
   is 85%, PPA gains about the same. Nothing in Deere's disclosure pins this share down.
2. **The RMSE is large relative to a small answer.** The calibration was fitted mostly on
   quarters where the effect was 1–4 pp. Q3 FY2026's estimates are 0.2–1.8 pp, so the relative
   uncertainty on SAT and CF is very high — the honest reading of SAT is "somewhere between a
   small headwind and a small tailwind", not "+0.21".
3. **Rounding.** Deere reports whole percentage points, so the disclosed history the model is
   fitted to is itself quantised at ±0.5 pp. Roughly 0.29 pp of the 0.64 pp RMSE is rounding
   rather than model error.
4. **Revenue geography ≠ currency of denomination.** Revenue booked to a region can be invoiced
   in dollars (exports from US plants, Gulf sales, much of Argentina). The calibration factor
   absorbs the average of this, but not its quarter-to-quarter variation.
5. **Translation ≠ transaction.** This estimates only the restatement of foreign-currency
   revenue into dollars. Deere's operating-profit currency line also contains transaction
   effects and hedge results, which is why the two series must not be added together.
6. **Q3 FY2025 mix as the Q4 proxy.** The Q4 scenario in section 6 borrows the Q3 regional mix
   because Deere does not publish a standalone Q4 geographic matrix. Q4 is seasonally lighter
   in Brazil, so that scenario probably overstates PPA's Q4 currency slightly.

**Confidence: medium-high on direction and on the Q2→Q3 deceleration; medium on the PPA
magnitude; low on SAT and CF individually.** The robust, decision-relevant claim is the first
one: currency stops helping in Q3, and anyone rolling Q2's +3 pp forward will overstate revenue
by roughly $200–250m.
