# HACKATON.md — EXCALIBUR build spec (Agents vs Wall Street, 16 Aug 2026)

Single source of truth for the team. Read this, then build your lane.
Owner: Viktor (team lead). Updated for the REAL challenge brief (not the earlier estimate).

========================================================================
0. THE DECISION (one paragraph, agreed)
========================================================================
We anchor on Wall Street consensus and add a SMALL, NAMED, BOUNDED adjustment —
never forecast from scratch. Consensus is nearly unbeatable on information at a
one-quarter horizon; the scoring is literally "be closer than consensus." A
ground-up model (DCF/segments) is more work and LESS likely to win, because
analysts already have better information. So: consensus = the thing to beat by
inches; guidance = how we beat it; the beat-prior = a small signed seasoning.
The number is COMPUTED, never hallucinated. LLMs only read documents into
typed signals; plain code does the arithmetic.

========================================================================
1. THE CHALLENGE (from the official repo)
========================================================================
4 companies, 12 measures (3 each). Each metric equal weight (company = 25%).

  HD   FY2026 Q2   Net sales (USDm) | Adjusted diluted EPS | Comparable sales %
  ADI  FY2026 Q3   Revenue (USDm)   | Adjusted diluted EPS | Adjusted gross margin %
  HAS  FY2026 FY   Net fees (GBPm)  | Pre-exceptional basic EPS (pence) | Pre-exceptional op profit (GBPm)
  DE   FY2026 Q3   Net sales (USDm) | Diluted EPS (GAAP)   | Production & Precision Ag op profit (USDm)

SCORING (accuracy prize, decided after companies report):
  metric score = min(5.0, |team − actual| / max(|WS − actual|, floor))
  floor: money/EPS = 0.5% of |actual|; % metrics = 0.5 percentage points.
  < 1.0 = beat Wall Street.  1.0 = tied.  > 1.0 = lost that metric.
  WS benchmark = frozen consensus, NOT given to teams. We reconstruct it.

SUBMISSION: 4 xlsx files, fill 3 yellow cells each (numbers only).
  % in percentage points (4.5 = 4.5%). Hays EPS in pence.
  Files: HD-FY2026Q2.xlsx, ADI-FY2026Q3.xlsx, HAS-FY2026.xlsx, DE-FY2026Q3.xlsx.

DATA: frozen 1,139-doc corpus in challenge/offline-data/ (filings, transcripts,
  slides, 2012→2026, Markdown) + official search helper (starter/search.py).
  No scraping needed. Only consensus must be sourced live (yfinance/Primer).

TIMELINE: build 11:15 → first judging 16:00 (5 min, most important) →
  HTML lock + final run 17:15–18:00 → uploads by 18:00.

========================================================================
2. THE FRAMEWORK (four families, two arithmetic modes)
========================================================================
Every forecast = consensus, moved toward guidance by a named bounded amount.
TWO MODES ONLY:
  LEVELS (money, EPS):  forecast = consensus × (1 + adjustment)   [multiplicative]
  RATES  (%):           forecast = consensus + adjustment          [additive, in pp]

FOUR FAMILIES (the 12 measures map 1:1):
  1. TOP-LINE LEVEL  (HD sales, ADI revenue, DE sales, HAS net fees):
       forecast = consensus × (1 + [0.8 × guidance_gap + small_beat_prior] × damp)
       guidance_gap = (guided midpoint − consensus)/consensus. Guidance = workhorse.
  2. PROFIT LEVEL    (HAS op profit, DE P&P Ag op profit):
       DERIVED, not guessed: op profit = forecast revenue × forecast op margin.
       (Segment: segment sales × segment margin.) Keeps cross-checks consistent.
  3. EPS             (HD adj, ADI adj, DE GAAP, HAS pre-except):
       forecast = consensus × (1 + [beat_prior + guidance_gap + buyback] × damp).
       Beat prior carries weight here (walk-down is an EPS game) but is signed.
  4. RATE            (HD comp %, ADI gross margin %):
       forecast = consensus + 0.8 × (guided midpoint − consensus).  [additive, pp]
       Guidance only; NO beat prior (no walk-down game on rates).

Adjustment terms (shared):
  guidance_gap  = fraction × (guided midpoint − consensus), SIGNED both ways
                  (a guide-down must pull the forecast DOWN — U1 rule).
  beat_prior    = λ·firm_med·reliability + (1−λ)·sector_med, small, signed.
  reliability   = 1/(1 + firm_std/ref_std), floored 0.25. λ default 0.8.
  damp          = multiplier in (0,1] when estimates revised up sharply or after
                  a monster beat (mean-reversion).

CROSS-CHECKS (auditor's ammunition — now 8 identities, not 1):
  EPS ⟺ net income ÷ shares · op profit ⟺ revenue × margin ·
  comp % ⟺ sales growth − new-store contribution · net fees ⟺ revenue − temp costs.

========================================================================
3. GUIDANCE MAP (what management actually commits to, per measure)
========================================================================
ADI (the ONE clean upcycle name — record quarter, revenue +37%):
  Revenue: GUIDED "$3.9bn ± $100m".  Adj EPS: GUIDED "$3.30 ± $0.15".
  Adj GROSS margin: NOT guided (they guide OP margin 49%±100bps) →
    consensus-anchored + trend. Q2 actual adj GM = 73.0%.
HD (soft, Q1 EPS DOWN YoY on +4.8% sales — margin compression):
  Net sales + comp: GUIDED at FULL-YEAR only (sales +2.5–4.5%, comp flat–+2.0%).
    → phase FY guide to Q2 + anchor Q2 consensus. No quarterly guide.
HAYS (staffing downturn, net fees −5% LFL):
  Pre-except op profit: GUIDED on the exact measure — "top of £37–46m consensus
    range"; they even publish consensus £43.5m (10 analysts). A gift.
  Net fees: Q4 −5% LFL; FY absolute derived. EPS: derive (op profit ÷ shares × (1−tax)).
DEERE (severe ag downcycle; P&P Ag sales −14%, op profit −39%):
  P&P Ag: GUIDED at segment level — net sales "down 5–10%" FY + segment op margin.
    → segment op profit DERIVED (segment sales × segment margin).

MACRO READ (drives the weighting): 3 of 4 names in downcycles (HD/Hays/Deere),
only ADI beating. So the beat-prior is a LIABILITY on 3 names — keep it SMALL,
SIGNED, and let guidance lead. Guidance-led: 8 of 12 measures. Prior-led: 4
(ADI gross margin, Hays EPS, HD quarter-specific, Deere EPS).

========================================================================
4. ARCHITECTURE (3 layers + auditor; "few agents, sharp contracts")
========================================================================
LAYER 1 — DATA-CoT (Evidence): read the corpus + consensus. Output a typed
  JSON contract per company: {actuals, consensus (12 anchors), guidance spec,
  revision history, share count, segment data}.
LAYER 2 — CONCEPT-CoT (Forecast engine): pure deterministic code. Runs the
  ledger (section 2), derives profit, produces {forecast, rows, interval,
  P(beat), call} per measure. NO LLM in the arithmetic.
LAYER 3 — QUALITY/AUDIT (Auditor): checks drivers-sum, margin-vs-history,
  rationale-vs-deviation, + contrary-evidence. Mechanical hooks: halve contested
  row, widen interval, redraw. Soft clamp: outside-range needs 2nd critic pass.

LLM is used ONLY to: (a) extract guidance → typed spec (kind/period/low/high),
(b) extract qualitative evidence → capped ±2% signal, (c) classify consensus-
alignment, (d) run the critic. Never computes a number.

========================================================================
5. WORK SPLIT (4 people — clean lanes, sharp hand-offs)
========================================================================
VIKTOR (analytical lead / financials): the engine formulas + 12 recipes +
  calibration (λ, damp, reliability, ref_std) + the backtest mechanics +
  final sign-off on all 12 numbers + the architecture story / pitch.
  Decides: λ, damp thresholds, reference_std, backtest window, soft-clamp bounds.

JAYESH (systems / data): the deterministic pipe. Corpus reader + search +
  extraction of actuals; consensus fetch (yfinance/Primer) + cache; the typed
  contract; the xlsx output writer. Owns data→number plumbing, no LLM.

DAVID (AI / LLM): the LLM edges. Guidance-extraction prompt → typed spec;
  evidence signals (Row 5, ±2%); consensus-alignment classifier; the critic
  call. Owns strict-JSON contracts + robust JSON parsing. Same lane as Jayesh's
  LLM pieces — pair up, don't overlap.

LARISSA (verifier / auditor / UI): auditor checklist + mechanical hook spec +
  "what we don't know" surface; data-quality & units checks; the architecture
  HTML (self-contained, <2MB); the demo narrative; the auditor-fires moment.

HAND-OFF CONTRACTS (the typed JSON between layers — this IS the showcase):
  Viktor spec's the engine's input schema → Jayesh fills it → David's LLM
  outputs slot into typed fields → Larissa's auditor consumes the forecast.
  One contract format end-to-end; nothing messy crosses a boundary.

========================================================================
6. BUILD ORDER (roughly sequential; each is stop-early-safe)
========================================================================
 1. Jayesh: read corpus, extract latest actuals + fiscal labels per company.
 2. Jayesh: fetch 12 consensus anchors (yfinance/Primer) + cache. Hays op profit
    consensus is in their own release (£43.5m).
 3. Viktor: lock the 12 recipes (which row is guidance-led vs prior-led per §3).
 4. David: guidance-extraction LLM → typed specs for the 8 guidance-led measures.
 5. Viktor+Jayesh: engine (ledger) code — deterministic, unit-tested.
 6. David+Larissa: auditor checklist + critic call + mechanical hooks.
 7. Larissa: backtest/validation (units, basis, fiscal labels) + architecture HTML.
 8. Viktor: final 12 numbers sign-off. Jayesh: write the 4 xlsx files.
 9. All: clear run at 17:15, upload by 18:00.

========================================================================
7. TRAPS THAT WILL SILENTLY LOSE A METRIC (memorise)
========================================================================
 1. BASIS: Deere EPS is GAAP+diluted (no adjustment). Hays EPS is pre-exceptional
    (UK "adjusted") AND basic (not diluted). ADI is non-GAAP adjusted. HD adj EPS.
    Forecast the EXACT basis the metric names.
 2. UNITS: rates in percentage POINTS (0.5pp is the whole floor). Hays in pence.
 3. Hays "net fees" ≠ revenue — it's revenue minus temp-worker costs (gross-
    profit proxy). Do not use turnover.
 4. FISCAL LABELS: off-cycle quarters (HD Q2 ends ~Aug 3; ADI/DE Q3 ~Aug). Verify
    period-end dates by hand.
 5. LOOKAHEAD: no post-cutoff info in any backtest (use point-in-time consensus).
 6. DOWN-CYCLE BEAT PRIOR: do not apply a positive beat-prior to HD/Hays/Deere
    by reflex — it goes negative where guidance points down.

========================================================================
8. DISCLOSURE (read once, decide once, then move on)
========================================================================
RULES.md: the entry must be built during the event; pre-built challenge-specific
code/prompts/research can disqualify the WHOLE entry. We have substantial prior
work (earnings_agent, revenue_prior, the brief). Decision: rebuild the specific
system TODAY on the actual 4 companies, and disclose in entry.json's
"pre-existing components" that we drew on general prior earnings-forecasting
research. Be honest, keep repo history + run logs. This protects the entry.

========================================================================
9. THE PITCH (30 seconds, for the 16:00 judging)
========================================================================
"Most agents read documents and ask an LLM for a number. That loses to a linear
model. EXCALIBUR treats consensus as the thing to beat by inches: every forecast
— all 12 numbers — is consensus plus a ledger of named, bounded, evidence-cited
adjustments. The number is computed, never hallucinated. For the non-EPS
measures we go guidance-first: management's own range, converted by code. An
epistemic auditor checks the 12 numbers against each other — implied margin,
op-profit identity — and when they disagree you watch the number move. Click any
dollar and see why it's there."
