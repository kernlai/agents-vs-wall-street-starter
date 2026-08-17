---
name: researching-company-signals
description: Build source-backed company profiles and resolve approved metric-specific forecasting signals with the repository's Tavily research pipeline. Use for company research, profile enrichment, forecast evidence collection, signal-map creation or validation, provenance auditing, cutoff checks, and forecast-input handoff in this repository.
---

# Research Company Signals

Use models to discover and propose. Let repository code own admissibility, arithmetic, and forecast acceptance.

## Workflow

1. Read `ARCHITECTURE.md`, `RULES.md`, `JUDGING.md`, `SUBMISSION.md`, `challenge/companies.json`, and the company seed in `signal_agent/config/companies.json`.
2. Run `npm run research:profiles` (or add `-- --company ADI`) to search all nine required profile sections. Never expose `TAVILY_API_KEY`; load it from the process or ignored `.env`.
3. Inspect `research/<run>/<company>/profile-candidates.json`. Use only sources whose `cutoffDecision` is `accepted`. Every proposed claim must cite source IDs and exact quotations from frozen files.
4. Create a metric-specific signal map. Give each challenge metric three to seven material approved signals and exactly one anchor. Declare role, hypothesis, direction, period, units, importance, resolver, evidence requirements, combination method, freshness, correlation group, accounting basis, and status.
5. Validate the profile and signal map with `signal_agent.research_validation`. Stop on missing sections, bad quotes, unknown sources, invalid role/formula combinations, unit or basis mismatch, arbitrary weights, or bad cardinality.
6. Save maps as `signal_maps/<company>.json`, then run `npm run research:signals` (or add `-- --company ADI`). The planner searches only approved signals.
7. Propose typed observations using exact quotations and decimal strings. Do not convert qualitative modifiers into numeric weights. Keep untriggered risks as conditional scenarios.
8. Create `research_audit.v1`, run the independent no-web reviewer in `signal_agent.lookahead`, and build `forecast_input.v2`. An incomplete/error review or deterministic provenance failure blocks handoff.
9. Pass accepted observations to `forecasting`; let `Decimal` formulas combine the anchor and approved drivers. Run the challenger and retain rejected-signal reasons in the receipt.

Read [references/schemas.md](references/schemas.md) when constructing profile claims, signal definitions, audits, reviews, or observations.

## Non-negotiable boundaries

- Treat URLs and model agreement as leads, not proof.
- Freeze selected content before citing it; preserve URL, publication time, local path, and SHA-256.
- Reject missing/uncertain publication dates for forecast-driving evidence.
- Never use post-cutoff facts, later actuals, or model memory to fill evidence gaps.
- Never invent numerical weights. Missing evidence retains the declared anchor or baseline.
- Do not alter workbook structure or submit automatically.
