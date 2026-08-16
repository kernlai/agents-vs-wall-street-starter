# Tier 1 — seasonal naive with drift

Drop this folder into the repo root as `tier1/`. Workflow:

```bash
python3 tier1/find_history.py        # 1. surface candidate figures with citations
# 2. confirm real values into tier1/history.json (fill value + source)
python3 tier1/forecast.py            # 3. compute forecasts, write submission/*.xlsx
npm run check:submission             # 4. official validation
```

## What it does

- **`find_history.py`** greps the most recent filings/transcripts/slides per
  company for metric-keyword lines and writes `research/tier1-candidates-<T>.md`
  with `path:line` citations. It never auto-fills history — a wrong historical
  poisons every forecast, so a human (or a Tier 2 LLM step) confirms each value.
- **`history.json`** is the confirmed-figures store. Minimum per metric: same
  period last year + two years back. Adding the most recent reported period and
  its prior-year twin sharpens the growth estimate. Units follow the workbook
  conventions: millions, dollars/pence per share, percentage points.
- **`forecast.py`** computes, per metric:
  - `growth` (amounts, EPS): same-period-last-year × (1 + g), g = 0.7 × most
    recent YoY + 0.3 × same-period seasonal YoY. For the annual Hays target,
    the FY2026H1 vs FY2025H1 interim pair drives the recent component.
  - `pct_blend` (margins, comp sales): 0.6 × latest reported + 0.4 × same
    period last year — mean-reverting metrics are never extrapolated
    multiplicatively.

  It then writes the three numbers into `Summary!C7:C9` of a fresh template
  copy (after verifying labels/units, mirroring the official validator), saves
  to `submission/`, and tees the full reasoning trail to `logs/` — which doubles
  as the timestamped run log the submission requires.

Missing history fails loudly with a named list of gaps; nothing is written
for that company.

## Tier 2 hook

Replace the human-confirmation step: have an LLM read the latest 8-K and call
transcript, extract guidance, and either write `history.json` itself or
override the drift `g` with guidance-anchored growth. Everything downstream
stays the same.
