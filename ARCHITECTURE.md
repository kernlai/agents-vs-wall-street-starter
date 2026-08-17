# Evidence-to-forecast compiler

> Central development reference — updated 16 August 2026. Keep this file and
> `architecture/index.html` synchronized with the command used for the final run.

## Integrated system map

The merged repository contains three complementary contributions:

- `COMPANY_PROFILE_SKILL.md` defines the lightweight, repository-first company
  orientation contract and claim-level provenance policy;
- `signal_agent/company_research.py`, `tavily.py`, `research_validation.py` and
  `lookahead.py` implement bounded Tavily discovery, immutable source freezing,
  deterministic evidence gates and independent look-ahead review; and
- `pipeline/`, the legacy five-worker report collector and `forecast_input.v1`
  remain available as the earlier financial-report consensus path and comparison
  baseline.

The target architecture is:

```text
four concurrent company lanes: HAS · HD · ADI · DE
                   │
        lightweight company profile
                   │
       approved metric-specific signal map
                   │
    bounded Tavily search/extract + supplied corpus
                   │
 immutable sources + manifest + cutoff decisions
                   │
 deterministic audit + independent no-web reviewer
                   │
             forecast_input.v2
                   │
      Decimal forecast compiler + challenge
                   │
      exactly three figures per company
                   │
 validate → preserve templates → four workbooks
```

### Current implementation status

| Area | State | Primary interface |
| --- | --- | --- |
| Company-profile contract | Implemented | `COMPANY_PROFILE_SKILL.md` |
| Four-company Tavily candidate research | Implemented | `python3 -m signal_agent.company_research --stage profile` |
| Approved-signal candidate research | Implemented | `python3 -m signal_agent.company_research --stage signals` |
| Source freezing, cutoff and manifests | Implemented | `signal_agent/tavily.py` |
| Profile/signal-map/evidence gates | Implemented library | `signal_agent/research_validation.py` |
| Independent look-ahead review | Implemented library | `signal_agent/lookahead.py` |
| Fail-closed v2 construction | Implemented library | `build_forecast_input_v2(...)` |
| Deterministic compiler | Implemented | `forecasting/` |
| Final forecast validation and workbook writing | Implemented | `scripts/run.sh` |
| Deterministic v2.1 handoff assembly | Implemented | `python3 -m signal_agent.handoff_cli` |
| Autonomous profile and observation proposal | Implemented | `python3 -m signal_agent.research_pipeline` |
| Offline corpus plus current web evidence | Implemented | concurrent company lanes in `research_pipeline.py` |
| v2.1-to-compiler adapter for all 12 figures | Implemented | `python3 -m forecasting.cli` and `forecasting.aggregate` |
| Per-company workbook adapter | Implemented | `python3 -m workbook_generator.cli` |

`python3 -m pipeline.run --max-minutes 45` is the single-command live path. It runs
four isolated research lanes concurrently, combines Tavily evidence with the
supplied offline corpus, creates audited v2.1 handoffs, compiles all twelve figures,
validates them and writes the four workbooks. `--skip-research` reuses validated
handoffs for a fast deterministic rerun.

Research consensus confidence is useful for report discovery and extraction
triage, but it is not forecast authority. Only evidence that passes the v2 source,
cutoff, audit and look-ahead gates may enter the deterministic compiler.

## Architecture statement

The worker first builds a source-backed company profile, then creates a metric-specific signal map. Each signal defines what evidence is required, how it affects the metric and how it may enter the forecast. Reusable resolver tools collect and normalize those signals before deterministic code combines them into an auditable forecast.

The LLM may propose structured observations. It may not invent sources, choose arbitrary weights, perform forecast arithmetic or write submission values. A signal changes a forecast only when its evidence and declared transformation pass deterministic validation.

## Worker workflow

```text
1. Build company profile                 Team Red + Team Blue
             ↓
2. Define metric-specific signal map     Team Red
             ↓
3. Collect evidence for those signals    Team Blue
             ↓
4. Measure and combine the signals       Team Red
             ↓
5. Produce scenarios and forecast        Team Red
             ↓
6. Challenge and validate                Independent challenger
```

### 1. Build the company profile

The JSON profile records the company's business model, products and customers, segments and geographies, fiscal calendar, revenue and cost drivers, accounting definitions, guidance style, cyclicality, seasonality, and material macroeconomic, political and industry exposures.

Profile claims are source-backed. Every claim cites one or more source IDs. Every source preserves its publisher, title, document type, publication time, URL, local corpus path and SHA-256 content hash.

### 2. Define the signal map

Each target metric gets approximately three to seven material signals. A signal must declare:

- what is measured;
- why it should affect the target metric;
- expected direction and target period;
- units and importance;
- resolver and required evidence;
- combination method;
- freshness requirement;
- correlation group, so related evidence is not double-counted.

Signals have one of five roles:

- `constraint`: an accounting identity or invariant that is enforced, never weighted;
- `anchor`: direct guidance or another defensible starting range;
- `driver`: a quantified effect applied through an explicit formula;
- `modifier`: qualitative evidence used to explain range selection, never assigned false precision;
- `scenario_trigger`: a conditional risk kept out of the base forecast unless the condition occurs.

Weights are forbidden unless the signal map identifies the backtest or historical analysis that justifies them.

### 3. Resolve the signals

Resolvers search only for approved signals and return typed observations. The Tavily query planner includes the declared signal hypothesis, target metric and period, evidence requirement, units and freshness rule. Search results are leads until selected pages are extracted, frozen locally and assigned immutable source records. Every observation carries the source ID, exact quotation, publication time, target period, units and normalized value. The compiler verifies the quotation against the frozen source text and verifies the source hash before accepting it.

A reusable signal has three levels:

1. template, such as management guidance;
2. company-specific instance, such as ADI FY2026Q3 revenue guidance;
3. current evidence-backed observation.

### 4. Combine signals

The visible calculation is:

```text
anchor
+ approved quantitative driver adjustments
= base forecast
```

Modifiers are displayed beside the range but do not receive invented numerical weights. Scenario triggers create explicit conditional scenarios. Constraints are checked after calculation.

### 5. Produce scenarios

Every target has a base forecast and may have upside or downside scenarios. A scenario records the triggering condition, explicit adjustment, source evidence and formula. A proposed but untriggered event never silently changes the base forecast.

### 6. Challenge and validate

The challenger checks:

- omitted material signals;
- period, unit, currency and accounting-basis mismatches;
- stale or post-cutoff evidence;
- unsupported quotations or changed source content;
- duplicated or correlated drivers;
- illogical direction or transmission mechanism;
- coincident evidence presented as leading evidence;
- qualitative evidence given false numerical precision;
- revenue evidence incorrectly applied to margin or EPS;
- missing reconciliation constraints.

A failed signal is rejected with a reason. The forecast retains its declared baseline or anchor rather than inventing an adjustment.

An independent no-web reviewer receives only the frozen-source manifest, supplied excerpts, cutoff, prompt hash, research audit and proposal. It reports unsupported claims and suspected look-ahead using a fixed issue vocabulary. Error findings or an unavailable reviewer block `forecast_input.v2`; deterministic provenance failures block it regardless of the model verdict. The reviewer detects evidence that cannot be reconstructed from supplied sources—it cannot prove what came from model training data.

## Provenance chain

Every forecast-driving value must preserve this chain:

```text
source URL + frozen file + SHA-256
        ↓
exact quotation + locator
        ↓
typed observation
        ↓
approved signal definition
        ↓
validation decision
        ↓
explicit Decimal formula
        ↓
forecast component and final value
```

Run artifacts are written as JSON next to the forecasts. Submission workbooks remain structurally unchanged except for the required value cells.

## First-version scope

Implemented now:

- strict JSON company profiles and signal maps;
- bounded Tavily search/extract with secret-safe configuration and concurrent company lanes;
- nine-section profile and approved-signal-only query planning;
- immutable web source snapshots, canonical manifests, hashes, publication cutoff decisions and exact-quote checks;
- three-to-seven signal cardinality, one-anchor, role/formula, unit and accounting-basis gates;
- structured research audits and an independent OpenAI no-web look-ahead reviewer;
- `forecast_input.v2` blocking on incomplete review, unsupported provenance or non-decimal JSON numbers;
- source hashes, URLs, exact quotations and cutoff checks;
- reusable management-guidance and explicit-driver resolvers;
- deterministic anchor-plus-driver combination using `Decimal`;
- qualitative modifiers and conditional scenarios without arbitrary weights;
- challenge checks for unsupported evidence, mismatches and double-counting;
- replayable JSON run receipts;
- an end-to-end ADI example using the supplied frozen SEC filing.

Deliberately excluded from the deterministic critical path:

- generic news sentiment;
- automatic supplier-network inference;
- arbitrary model-generated weights;
- unrestricted LLM arithmetic;
- a universal financial ontology;
- an unrestricted or self-modifying agent swarm.

The older five-worker report-consensus collector remains available for comparison, but agreement and confidence from that path are not forecast authority and do not satisfy the `forecast_input.v2` evidence gates.

## Guarantees and limits

The system does not guarantee that an LLM finds every economically relevant fact or that a forecast is accurate. It does guarantee that accepted inputs replay to the same output, rejected evidence cannot move a number, post-cutoff evidence is excluded, and every applied component has an inspectable source-to-formula receipt.
