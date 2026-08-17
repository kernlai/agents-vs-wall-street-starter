# Research payload schemas

## Profile claim

```json
{
  "claimId": "unique-id",
  "claim": "Concise claim",
  "sourceIds": ["src-id"],
  "exactQuotes": ["Exact text present in the frozen source"]
}
```

Populate every required section: `businessModel`, `productsAndCustomers`, `segmentsAndGeographies`, `fiscalCalendar`, `revenueAndCostDrivers`, `accountingDefinitions`, `guidanceStyle`, `cyclicalityAndSeasonality`, and `externalExposures`.

## Signal definition

Use roles and deterministic behaviors only in these combinations:

| role | resolver | combinationMethod |
| --- | --- | --- |
| `anchor` | `extract_management_guidance` | `forecast_starting_range` |
| `driver` | `extract_explicit_driver` | `additive_adjustment` |
| `modifier` | `extract_qualitative_modifier` | `qualitative_only` |
| `scenario_trigger` | `extract_scenario_trigger` | `conditional_adjustment` |
| `constraint` | `evaluate_constraint` | `constraint_check` |

Include `id`, `signal`, `targetMetric`, `role`, `hypothesis`, `expectedDirection`, `targetPeriod`, `units`, `importance`, `resolver`, non-empty `evidenceRequired`, `combinationMethod`, `freshnessRequirement`, `correlationGroup`, `accountingBasis`, and `status`. Use `approved` only after review. Do not add `weight` or `numericWeight`.

## Typed observation

```json
{
  "observationId": "obs-id",
  "signalId": "approved-signal-id",
  "targetMetricId": "metric-id",
  "period": "FY2026Q3",
  "units": "USDm",
  "accountingBasis": "reported",
  "value": {"low": "3800", "high": "4000"},
  "sourceId": "src-id",
  "exactQuote": "Exact frozen-source quote",
  "deterministicStatus": "accepted"
}
```

All forecast arithmetic numbers cross JSON boundaries as decimal strings.

## Audit and review

`research_audit.v1` must record provider, model, declared knowledge cutoff, request ID, prompt SHA-256, canonical input-manifest SHA-256, supplied source IDs, concise claims, rejected evidence, a reasoning summary, and creation time. It is an evidence-selection summary, not hidden chain of thought.

`lookahead_review.v1` has status `passed`, `blocked_for_lookahead`, or `incomplete`. Error findings block handoff. Supported codes are defined by `signal_agent.research_validation.SUPPORTED_LOOKAHEAD_ISSUES`.
