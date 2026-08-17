# Signal research system

> Legacy comparison path: this document describes the five-worker report-consensus
> collector and `forecast_input.v1`. Consensus confidence is not forecast authority.
> The canonical fail-closed evidence contract is `forecast_input.v2`, documented in
> `ARCHITECTURE.md` and implemented by `signal_agent.research_validation`.

This package collects evidence that can later feed forecasting agents. Its first signal type is `financial_reports`.

## Architecture

One orchestrator launches five independent research workers concurrently. Each worker uses a different search strategy: investor relations, regulator, exchange, direct-document verification, or sceptical cross-checking. Every worker receives a deterministic, bounded selection of recent metric-relevant excerpts from the supplied frozen corpus, then uses live web search to verify official and current sources. All workers return the same structured finding schema.

The reconciler groups findings by company, normalised report-event family and reporting period. Quarterly results, trading statements and trading updates share one periodic-update family because issuers use those labels inconsistently; full-year results and annual reports remain distinct events. It does not use a simple majority over URLs because the same report may have several official URLs. Confidence combines:

- agent agreement (40%);
- source authority (25%);
- source-domain independence (15%);
- record completeness (15%); and
- verified official status (5%).

A result below 0.65 is marked `needs_review`; it is not silently promoted to a confirmed signal. When a company defines a report checklist, overall confidence combines leading-report quality (75%) with target coverage (25%). This makes missing reports visible instead of allowing three strong findings to hide incomplete research.

Every saved signal and CLI result includes a short `confidence_explanation`. It reports checklist coverage, evidence quality across the three most recent events, researcher agreement and the number of reports corroborated by multiple source organizations.

## Extracted financial facts

Report discovery is only the first confidence layer. Every researcher also opens accepted reports and returns normalized numerical facts with metric, value, unit, fiscal period, accounting basis, section and evidence. The reconciler groups equivalent facts, votes on the numeric value and records conflicting values instead of silently choosing one.

Facts are organized into financial performance, operating drivers, guidance, capital and cash, and accounting adjustments. Each fact records its company/region scope and whether it is reported, guidance, or derived. Qualitative statements are stored separately as directional observations with scope and horizon, so language such as “Perm activity softened” is useful without inventing a number.

The signal exposes separate `document_confidence`, `extraction_confidence`, and `extraction_coverage` values. Combined confidence is 50% document confidence, 35% reconciled extraction confidence and 15% report-level extraction coverage. A signal cannot be `confirmed` without at least one fact supported above the extraction threshold.

## Persistent memory and self-improvement

SQLite stores companies, runs, raw findings and source memory. Source usefulness is scoped to `(company_id, signal_type, domain)`, so a useful Hays filing source does not automatically become authoritative for Deere or for a different signal.

Sources contributing to confirmed consensus accumulate a bounded reputation score. Rejected findings reduce it. Memory is only a ranking hint: the sceptical fifth worker receives no hints and must explore independently. This avoids a self-reinforcing source monoculture.

Future improvement should use delayed outcome labels: report accessibility, later human acceptance, extraction success and forecast contribution. Those labels are more meaningful than agreement alone.

## Run it

Set `OPENAI_API_KEY`, then run:

```bash
python3 -m signal_agent.cli --company HAS
```

The same reusable collector is configured for all challenge companies:

```bash
python3 -m signal_agent.cli --company HD
python3 -m signal_agent.cli --company ADI
python3 -m signal_agent.cli --company DE
```

Reasoning effort is configurable and recorded in the run metadata:

```bash
python3 -m signal_agent.cli --company DE --reasoning-effort high
```

All company-specific behavior is editable in `signal_agent/config/companies.json`. Change `financial_report_targets` to control required source coverage, `financial_fact_targets` to select numerical fields, and `financial_observation_targets` to select qualitative drivers. No Python change is required when adding or removing a target.

## Forecasting handoff

The forecasting stage should not parse raw researcher output. Build a compact, deterministic handoff from the latest reconciled signal:

```bash
python3 -m signal_agent.forecast_input --company HAS
```

This writes `forecast_inputs/HAS.json` containing confirmed facts, chronological metric series, qualitative observations, source lineage, signal confidence and unresolved conflicts. The next forecasting agent consumes this stable `forecast_input.v1` contract, applies company-specific forecast logic and emits scenario and final-forecast JSON before workbook generation.

Useful options:

```bash
python3 -m signal_agent.cli \
  --company HD \
  --workers 5 \
  --model gpt-5.6-terra \
  --database data/signals.db \
  --output signals
```

The command writes a versioned JSON signal and `latest.json` beneath `signals/<company>/financial_reports/`.

For regular refreshes, invoke the same idempotent command from cron, a CI scheduler or a managed job runner. Schedule the command externally rather than embedding a permanently running scheduler in the agent. Each run remains immutable and `latest.json` is updated only after reconciliation completes.

## Add another signal

Add a prompt, structured finding schema, normalised identity function and reconciler for the new signal type. Reuse the orchestrator, company registry, storage tables, source-memory policy and run artifact conventions. Signal-specific confidence factors should be versioned rather than forcing every signal into the financial-report formula.

## Tests

```bash
npm run test:signals
```

The tests run offline and cover consensus confidence, disagreement handling, concurrent orchestration and company-scoped source memory.
