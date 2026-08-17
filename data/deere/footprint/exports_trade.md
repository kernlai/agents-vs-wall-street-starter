# Deere: export flows, cross-border production, and a live read on FY2026 Q3

Companion to `exports_trade.csv`. Built 2026-08-16, before Deere reports FY2026 Q3 on
2026-08-20. **No Q3 FY2026 actuals exist and none are used here.** Everything below is built
from trade data published through June 2026 and from Deere filings through the Q2 FY2026 10-Q.

The brief was to map export flows so that plant-level activity in one country can be tied to
revenue booked in another. The mapping work produced a more useful result than the mapping
itself, so the headline is stated first.

---

## 1. The main finding

**US machinery export flows are not a geographic bridge. They are a production-cycle
thermometer — and a good one.**

The intuitive test (do US exports explain Deere's *non-US* revenue?) mostly fails. The
non-intuitive one works far better: US exports track Deere's **segment** revenue, because US
exports and Deere's US shipments come off the same assembly lines on the same production
schedules.

Year-on-year growth, seasonality removed, Deere fiscal quarters:

| Test | n | r |
|---|---|---|
| **HS 8432+8433 vs Deere PPA revenue** | **17** | **+0.928** |
| HS 8429 vs Deere CF revenue | 19 | +0.765 |
| HS 8432+8433 vs Deere **US** revenue | 19 | +0.880 |
| HS 8432+8433 vs Deere **non-US** revenue | 19 | +0.722 |
| HS 8429 vs Deere non-US revenue | 19 | +0.629 |

Note the ordering: the export series explains Deere's **US** revenue *better* than its non-US
revenue, in every code and every transform. That is the opposite of what an export-channel story
predicts, and it is the tell — this is a **sector production** measure, not a trade-flow measure.

Use levels correlations with care. On raw quarterly levels every pair looks strong
(r = +0.69 to +0.94), but both series share a heavy planting/harvest seasonality, so most of that
is a shared calendar shape rather than shared information. The YoY figures above are the only
ones worth acting on. All three transforms are in `corr_diag.txt`.

### Out-of-sample check on the last reported quarter

| Q2 FY2026 (Feb–Apr 2026) | Export proxy YoY | Reported segment YoY |
|---|---|---|
| HS 8432+8433 → **PPA** | **−15.4%** | **−14.0%** |
| HS 8429 → CF | −6.6% | **+29.0%** |

The PPA call was nearly exact. **The CF relationship has broken down** — it held from FY2020 to
FY2025 and then decoupled hard in FY2026 Q1 (CF +32.8% vs export −6.7%) and Q2 (+28.2% vs
−6.6%). Deere's CF growth is coming from roadbuilding and Europe, which a US export series
cannot see. **Do not use HS 8429 to forecast CF right now.**

---

## 2. Live read on FY2026 Q3 (use case A)

Deere's Q3 FY2026 covers roughly **4 May – 2 Aug 2026** — calendar May, June and July. US trade
data is published through **June 2026**, so this is a genuine **two-thirds read on a quarter that
has already ended but has not been reported.**

**US ag machinery exports (HS 8432+8433), May+June, USD m:**

| 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | **2026** |
|---|---|---|---|---|---|---|---|
| 806 | 669 | 921 | 1,092 | 1,326 | 1,053 | 710 | **861** |

**+21.2% YoY** — the first positive print since 2023, after −32.6% in the same window of 2025.
HS 8429 (construction) is +3.8% and HS 8701 +4.9%.

**Read this as a trough turning, not a recovery.** At 861 the level is still 18% below 2024 and
35% below 2023. The move is a rebound off a deeply depressed base, not a return to cycle-average
volume.

**Do not take the naive regression literally.** Feeding +21.2% into the fitted relationship
(PPA_YoY = 1.15 + 1.098 × export_YoY, R²=0.86) implies PPA **+24%** YoY in Q3. That is almost
certainly too strong, for four reasons worth stating plainly:

1. **It contradicts guidance.** Deere guided FY2026 PPA to −5 to −10% on 2026-05-21, and H1 PPA
   was already tracking well below that. A +24% Q3 is not reconcilable with the full-year frame.
2. **The fit was estimated across the 2021–2023 boom**, so the slope (1.098) is calibrated on a
   period with far more upside variance than today.
3. **The residuals are large**: residual sd 10.7pp, mean absolute error 8.5pp, worst historical
   miss 19.6pp. Even in-sample this indicator is accurate to roughly ±10pp, not ±2pp.
4. **Two of three months.** July 2026 is unpublished and could revert. At export +0% the implied
   PPA is +1%; at +10% it is +12%. The answer is highly sensitive to the missing month.

**What I would actually take from this:** the direction of travel in the Q3 window was
**up, not down**, for the first time in two years, and the sharp sequential improvement from
Q2's −15.4% to +21.2% is a real change in the data rather than noise at the margin. That is a
point *against* a further deterioration in PPA shipments in Q3 and *for* the underproduction
phase having bottomed. It is not a basis for a specific PPA number.

**Tariffs point the same way** (section 5): the Section 122 baseline died three days into the
quarter, the ag machinery Section 232 rate halved from 8 June, and CAPE refund phases 2 and 3
opened inside the quarter. Deere's *net* tariff cost in Q3 was very likely far below Q1's $361m,
with a real chance of a further recovery credit.

---

## 3. Where Deere builds versus where it sells (use case B)

Deere's own framing, FY2025 10-K Item 1:

> Our global manufacturing footprint allows us whenever possible to produce our products close to
> the markets where they are sold. For example, most of our large agricultural equipment is
> assembled in the U.S. for our U.S. customers.

| Measure | Value |
|---|---|
| Owned factory locations, US & Canada | 23 (+4 leased) |
| Factory locations outside US & Canada | 45 |
| Countries hosting those 45 | Argentina, Austria, Brazil, China, Finland, France, Germany, India, Israel, Italy, Mexico, Netherlands, New Zealand, Spain |
| Property & equipment, US / Germany / other | $4,198m / $1,435m / $2,446m |

The property-by-country series (FY2013–FY2025, in the CSV) carries one structural break:
**Germany roughly doubled from $598m (FY2017) to $1,164m (FY2018)** on the Wirtgen acquisition.
That is why roadbuilding revenue is booked heavily in Europe, why CF is the most import-exposed
segment, why CF absorbed **50%** of the IEEPA tariff refund — and, most likely, why the HS 8429
export proxy has stopped tracking CF.

### The geographic bridge is real but narrow: it is Canada

US machinery exports send **47–60% of every dollar to Canada**, across all four codes. Deere has
no meaningful ag or construction *assembly* in Canada, so Canadian revenue is almost purely
machines built in US plants and shipped north. That structural claim makes a prediction, and it
holds:

| Deere revenue line | vs US HS exports | n | r |
|---|---|---|---|
| **Canada** | exports **to Canada**, HS 8432+8433 | 7 | **+0.987** |
| **Canada** | exports **to Canada**, HS 8429 | 7 | +0.936 |
| Outside US & Canada | exports to world, HS 8432+8433 | 9 | +0.253 |
| Outside US & Canada | exports to world, HS 8429 | 9 | +0.117 |

Read the *contrast*, not the levels — with n=7 an r of +0.99 is one or two points doing the work.
What matters is that the same series is strongly related to Canadian revenue and essentially
unrelated to rest-of-world revenue, exactly as the footprint predicts.

**Consequence for the employment-signal thesis:** US plant headcount maps to **US + Canada**
shipments, about 61% of Deere revenue (FY2025: US $23,974m + Canada $3,735m of $45,684m). It does
**not** map to Western Europe, Latin America or Asia. Reading those requires headcount at the
German, Brazilian and Indian plants.

### Brazil confirms the same logic from the other side

Brazil is a **net exporter** of construction machinery and tractors (2024: HS 8429 exports
$2,667m vs imports $1,050m; HS 8701 $1,332m vs $381m). Latin American demand is served from
Brazilian plants, not from US exports — total *industry* US exports of all four codes to Brazil
were about $0.55bn in 2024, against Deere Latin America revenue of $5,607m in FY2025.

### Deere's own import dependence, a trackable series

| Date | "…of our domestic sales are assembled in the U.S." |
|---|---|
| 2025-05-15 → 2025-11-26 | nearly **80%** (unchanged across three filings) |
| 2026-02-19 | nearly **75%** |
| 2026-05-28 | *sentence removed* |

A 5-point drop, then the disclosure disappearing. Consistent with a higher imported share of US
sales (Deere names Europe, Mexico, India, Japan) and higher tariff exposure per dollar of US
revenue. Withdrawal of a voluntary sentence has innocent explanations; it is flagged, not
concluded.

---

## 4. This is a sector proxy, not a Deere measure

**These HS codes cover the whole US industry and Deere cannot be separated out.**

- **HS 8432** (soil prep, planters, seeders) — AGCO (White, Sunflower), CNH (Case IH Early
  Riser), Kinze, Great Plains/Landoll, Vermeer.
- **HS 8433** (harvesting, threshing, mowers) — AGCO (Gleaner, Massey), CNH (Axial-Flow, New
  Holland), Claas of America (Omaha-built combines), Kubota and Toro in the mower lines. Also
  contains **lawn mowers** (8433.11/8433.19), which belong to Deere's Small Ag & Turf segment,
  not PPA — so the code straddles two Deere segments.
- **HS 8701 — largest contamination risk.** This heading includes **road tractors for
  semi-trailers** (8701.21–8701.29), i.e. highway trucks, alongside agricultural tractors
  (8701.91–8701.95). Freightliner, Peterbilt, Kenworth and Mack sit inside the $6.59bn 2024
  figure. **Do not read HS 8701 at 4-digit level as an agriculture signal.** It is included for
  completeness and deliberately excluded from the PPA backtest.
- **HS 8429** (dozers, graders, excavators, loaders) — **Caterpillar dominates**, plus Komatsu,
  Volvo CE, Terex, Bobcat/Doosan. Deere CF is a minority of the flow, which is part of why the
  CF relationship decoupled once Deere's own mix shifted toward European roadbuilding.

Kubota mainly *imports* into the US from Japan and Thailand, so it contaminates the import side
more than the export side.

That the PPA correlation is +0.93 *despite* all this contamination is itself informative: the US
ag-machinery production cycle is highly synchronised across manufacturers, which is what makes an
industry-wide series usable as a Deere proxy at all.

---

## 5. Tariffs and trade policy, 2025–2026

Several events land **inside the Q3 FY2026 window (4 May – 2 Aug 2026)**. Deere's own filings
corroborate the key ones.

| Date | Event | In Q3 window? |
|---|---|---|
| 2025-08-18 | Steel/aluminium derivative duty scope expanded to more HTS codes | no |
| 2026-02-20 | **Supreme Court invalidates IEEPA tariffs** (6–3) | no |
| 2026-02-24 | Section 122: 10% additional ad valorem on all imports, as IEEPA replacement | no |
| 2026-03-04 | CIT orders CBP to liquidate/reliquidate without IEEPA duties | no |
| 2026-04-06 | **Section 232 derivative duty extended to ag machinery (HS 8432, 8433) at 25%** (Proc. 11021) | no |
| 2026-04-20 | CBP opens CAPE refund process, phase 1 | no |
| **2026-05-07** | **CIT strikes down the Section 122 10% baseline as ultra vires** | **yes (day 4)** |
| **2026-06-08** | **Section 232 ag machinery rate cut 25% → 15%**, through 2027-12-31 | **yes** |
| **2026-06-29** | CAPE phase 2 opens (reconciliation, AD/CVD, finally-liquidated entries) | **yes** |
| **2026-07-31** | CBP: 17.69m entries liquidated, ~$128.68bn refunds accepted for processing | **yes** |

### Deere's disclosed tariff economics

| Period | Direct incremental tariff cost |
|---|---|
| Q2 FY2025 | ~$95m |
| 9M FY2025 | ~$300m (implies ~$205m in Q3 FY2025) |
| FY2025 | ~$600m (implies ~$300m in Q4 FY2025) |
| Q1 FY2026 | $361m gross |
| H1 FY2026 | **$372m net** of a **$272m** IEEPA recovery |

Backing out Q2 FY2026: gross H1 = 372 + 272 = $644m, so **gross Q2 ≈ $283m**, **net Q2 ≈ $11m**.
The $272m recovery was allocated **20% PPA / 30% SAT / 50% CF**, and Deere described it as a
first-phase claim.

**Q3 implication — direction, not magnitude.** Three forces compound favourably: the Section 122
baseline died on day 4 of the quarter; the ag machinery Section 232 rate halved from 8 June
(roughly the last eight weeks); and CAPE phases 2 and 3 opened inside the quarter, so a further
recovery credit is plausible. Against a Q3 FY2025 comparative of roughly $205m of tariff cost,
the year-on-year cost comparison should be favourable. **I am deliberately not putting a number
on it**: the refund depends on Deere's entry-level filings, which are not public, and the
government has appealed the CIT refund order to the Federal Circuit, so recognised recoveries
carry reversal risk.

**Retaliation side.** Deere is "a net exporter of agriculture and turf equipment from the U.S.",
so foreign retaliation hits export prices and margins rather than input costs. Through 2026 the
retaliation picture eased — notably China suspended retaliatory tariffs and resumed US soybean
purchases, supporting farm income and equipment demand with a lag. That is an FY2027 demand
tailwind, not a Q3 FY2026 shipment effect.

---

## 6. Coverage, gaps and honesty

**1,203 rows, 73 series**, dates 2012-01-01 to 2026-07-31. By `source_type`: 1,100 trade-data,
93 filing, 8 news, 2 company-site.

| Series | Coverage |
|---|---|
| `us_exports_hs{8432,8433,8701,8429}` annual, world | 2012–2025, 14 years each, complete |
| `us_exports_hs*` **monthly** | 8432: 2012-01→2026-06 (173 obs); 8433/8701/8429: 2019-01→2026-06 (90 each) |
| `us_exports_hs*_{canada,mexico,brazil,germany,eu27,australia,argentina,uk,china}` | annual by destination, 2012–2025 |
| `br_{exports,imports}_hs*` | 2016–2025, 10 years × 4 codes × 2 directions, complete |
| `in_{exports,imports}_hs*` | **sparse — 8432 only (8 years), plus one 8433 import year** |
| `de_property_equipment_*` | FY2013–FY2025 |
| `de_net_sales_{us_canada,outside_us_canada}` | FY2013–FY2021 (Deere discontinued this split) |
| `de_net_sales_canada` | FY2019–FY2025 |
| `de_tariff_*`, `de_domestic_assembly_share`, `de_factory_count_*` | as disclosed |
| `us_sec232_*`, `us_sec122_*`, `us_cape_*`, `us_ieepa_*` | dated policy events |

### Real gaps — not filled with estimates

- **India is materially incomplete.** Only HS 8432 has a usable series. The Comtrade hourly call
  quota ran out partway through the India block. Requested by the brief; substantially not
  delivered.
- **No HS6 detail.** HS 8701 at 4 digits is contaminated by highway truck tractors and could not
  be narrowed to 8701.91–8701.95. This is the most important remaining gap.
- **July 2026 trade data is unpublished**, so the Q3 read is two months of three.
- **Monthly history for 8433/8701/8429 starts 2019**, not 2012, so the quarterly backtest is
  n=17–19 rather than the ~50 a full history would give.
- **Deere never discloses plant-to-market assignment.** The mapping in section 3 is inferred from
  the 10-K's "produce close to the markets" language plus the factory country list. Directionally
  sound, specifically unproven.
- **Fiscal/calendar alignment is approximate.** Deere's 13-week quarters end in the last days of
  Jan/Apr/Jul/Oct in some years and the first days of Feb/May/Aug/Nov in others; quarters ending
  in the first half of a month are mapped to the three prior calendar months. Residual mismatch
  is up to about a week at each end.
- **Missing values are absent rows, never zeros.** The single `0` in the file is the Section 122
  rate after the CIT struck it down — a real measured rate, documented in its own note.

### On the sample sizes

The quarterly correlations rest on **n=17–19**; the Canada and annual ones on **n=7–9**. None of
these would survive a demanding significance test. They are reported because the *pattern* across
them is coherent and matches independently-known structure, and because the Q2 FY2026
out-of-sample PPA check (−15.4% predicted vs −14.0% reported) is a genuine test the indicator
passed. One good out-of-sample hit is not a track record either.

---

## 7. How to refresh (durable tracker)

Three scripts in `scripts/data/`:

```bash
# 1. Fetch. Caches every response, so re-runs are free.
#    --only {annual,monthly,foreign} spends a limited quota window deliberately.
python3 de_fetch_comtrade_machinery.py --cache ./ctcache --out ./comtrade_raw.jsonl \
    --start-year 2012 --end-year 2026 --only monthly --workers 3 --min-interval 1.1

# 2. Build the CSV and re-run the geographic correlations.
python3 de_build_exports_trade.py --comtrade ./comtrade_raw.jsonl \
    --partners ./partnerAreas.json --corpus-rows ./de_exports_trade_corpus_rows.csv \
    --geo-matrix ../../data/deere/de_geo_matrix.csv \
    --out ../../data/deere/footprint/exports_trade.csv --diag ./corr_diag.txt

# 3. The segment backtest and the live read on the open quarter.
python3 de_exports_segment_backtest.py \
    --exports ../../data/deere/footprint/exports_trade.csv \
    --geo-matrix ../../data/deere/de_geo_matrix.csv
```

**Monthly cadence.** US data for month *M* appears in Comtrade around the first week of *M+2*.
For a quarter ending in early August, two of three months are readable before the earnings date —
which is exactly the edge this indicator provides.

Operational notes, learned the hard way:

- The public tier returns **429** under burst and **403 "Out of call volume quota"** when the
  hourly budget is gone. **A rejected 429 still spends quota**, so aggressive retrying is
  self-defeating — pace with `--min-interval` rather than racing. `Retry-After` on the 403 gives
  the exact resume time (~40 min).
- **Exponential backoff is wrong here.** The 429 window clears in about a second; exponential
  backoff turned that into minutes of idle waiting and cost a ~4x slowdown before it was fixed.
- **Some reporters return several rows per query**, split by customs procedure and mode of
  transport. The true total carries `customsCode=C00, motCode=0, mosCode="0", partner2Code=0`.
  Brazil and India do this; the US does not. Missing this silently multiplies rows and can pass a
  partial breakdown off as the total — the builder filters explicitly.
- A **Census API key** (free, `api.census.gov/data/key_signup.html`) would remove all of this:
  the Census timeseries endpoint returns many months and all destinations per call. It was
  unavailable in this run.

Priorities for the next refresh:

1. **July 2026 data** (publishes early September) — completes the Q3 read and lets it be scored
   against the actual result. Scoring this call is the single most valuable next step.
2. **HS6 breakout of 8701.91–8701.95** to de-contaminate the tractor series.
3. **India flows**, and extend 8433/8701/8429 monthly back to 2012 to lift the backtest n.
4. **Diagnose the CF/HS8429 decoupling** — split Deere CF into roadbuilding vs construction and
   test against European rather than US flows.

### Sources

- UN Comtrade public preview API — <https://comtradeapi.un.org>
- Deere filings corpus, `challenge/offline-data/deere/filings/` (10-Ks FY2015–FY2025, 10-Qs
  through Q2 FY2026)
- [NDSU ARPC, temporary tariff relief for agricultural machinery](https://www.arpc-ndsu.com/post/temporary-tariff-relief-for-agricultural-machinery)
- [White & Case, Section 122 tariff](https://www.whitecase.com/insight-alert/trump-administration-imposes-10-section-122-tariff-plan-replace-ieepa-tariffs)
- [Miller Nash, IEEPA and Section 122 struck down](https://www.millernash.com/firm-news/news/tariffs-in-flux-ieepa-and-section-122-struck-down-section-232-duties-expand)
- [Skadden, tariff refund mechanism](https://www.skadden.com/insights/publications/2026/03/tariff-refund-mechanism-takes-shape)
- [Cato, IEEPA refunds update](https://www.cato.org/blog/ieepa-refunds-update-good-progress-still-ways-go)
