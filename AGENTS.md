# Repository worker rules

Read `ARCHITECTURE.md`, `RULES.md`, `JUDGING.md` and `SUBMISSION.md` before changing the forecasting system.

## Required workflow

1. Build or update the source-backed company profile.
2. Define a metric-specific signal map with three to seven material signals per metric.
3. Resolve only those signals against admissible evidence.
4. Let deterministic code validate, normalize and combine accepted observations.
5. Produce an explicit base forecast and conditional scenarios.
6. Challenge cutoff, provenance, units, periods, accounting basis, correlation and reconciliation.

## Authority split

- An LLM may find passages and propose typed observations.
- Source records own facts, dates, URLs and hashes.
- Signal maps own permitted causal relationships and formulas.
- Deterministic code owns validation, conflict handling, arithmetic, scenarios, workbook values and provenance receipts.
- Qualitative modifiers never receive invented numerical weights.
- Missing or invalid evidence means reject the adjustment and retain the declared anchor/baseline.

## Development discipline

- Build one public behavior at a time with a failing test, minimum implementation and green suite.
- Commit every coherent green vertical slice.
- Use `Decimal`, not binary floating point, for forecast arithmetic.
- Do not copy challenge-specific code committed before the official build window.
- Never commit secrets, private data, Bloomberg data or confidential employer/client information.
- Do not change template structure beyond the required submission value cells.
