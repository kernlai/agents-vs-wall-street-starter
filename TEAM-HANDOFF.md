# Legacy v1 pipeline handoff

This document describes the earlier five-worker `forecast_input.v1` path retained
for comparison. The canonical evidence-gated design uses Tavily, company profiles,
an independent look-ahead review and `forecast_input.v2`; see `ARCHITECTURE.md`.
The downstream `forecasting.cli`, aggregation and `workbook_generator.cli` adapters
are now implemented. This file otherwise documents the retained v1 comparison path.

## Setup

```bash
npm install
export OPENAI_API_KEY="..."
npm run test:signals
```

Run only the completed stages:

```bash
python3 -m pipeline.run --through inputs
```

This creates `forecast_inputs/<company>.json` using the `forecast_input.v1` contract. Each input contains confirmed facts, chronological metric series, observations, sources, confidence and unresolved conflicts.

## Forecasting team contract

Implement `forecasting/cli.py` so this command works:

```bash
python3 -m forecasting.cli \
  --company HAS \
  --input forecast_inputs/HAS.json \
  --output forecasts/HAS.json
```

The output must be JSON:

```json
{
  "schema_version": "company_forecast.v1",
  "company_id": "HAS",
  "signal_run_id": "source-run-id",
  "forecasts": [
    {
      "metric": "Net fees",
      "value": 904.0,
      "unit": "GBPm",
      "scenario": "base",
      "confidence": 0.78,
      "rationale": "Short explanation",
      "input_fact_ids": []
    }
  ],
  "scenarios": {},
  "checks": [],
  "warnings": []
}
```

There must be exactly three numeric forecasts matching `challenge/companies.json`. Keep model judgement in this stage and arithmetic checks deterministic.

## Workbook team contract

Implement `workbook_generator/cli.py` so this command works:

```bash
python3 -m workbook_generator.cli \
  --company HAS \
  --forecast forecasts/HAS.json \
  --template challenge/templates/HAS-FY2026.xlsx \
  --output submission/HAS-FY2026.xlsx
```

It must copy the supplied template, fill only the three yellow forecast cells, preserve the `Summary` sheet, labels, units and period, and write the requested output path.

## Final commands

For a clean live research-to-workbook run with both keys in `.env`:

```bash
python3 -m pipeline.run --max-minutes 45
```

Once four validated `forecast_input.v2.1` files exist, rerun without paid APIs:

```bash
python3 -m pipeline.run --skip-research
```

The command runs four isolated company lanes concurrently. Within each lane, research feeds the handoff, forecasting and workbook stages in order. It then runs `npm run check:forecasts` and saves a timestamped log under `logs/`. Each web researcher also receives a bounded, metric-relevant selection from the supplied frozen corpus and verifies it against current official web sources.

Useful development modes:

```bash
python3 -m pipeline.run --through signals
python3 -m pipeline.run --through inputs --skip-research
python3 -m pipeline.run --through forecasts --skip-research
python3 -m pipeline.run --companies HAS --skip-research
python3 -m pipeline.run --parallel-companies 2
```

Do not commit `.env`, API keys, `data/signals.db`, generated signals, forecast inputs or private `entry.json`. Commit the source, prompts, configurations, tests and interface documentation.
