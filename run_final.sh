#!/usr/bin/env bash
# Final run: corpus -> LLM extraction -> forecasts -> four workbooks, one command.
#   ./run_final.sh            full agent run (Tier 2 + Tier 1)
#   ./run_final.sh --no-llm   Tier 1 only, from the existing tier1/history.json
# Logs everything to logs/final-run-<timestamp>.log (the required clear-run log).
set -euo pipefail
cd "$(dirname "$0")"

STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="logs/final-run-${STAMP}.log"
mkdir -p logs

{
  echo "=== Agents vs Wall Street — final run ${STAMP} ==="
  echo "commit: $(git rev-parse HEAD 2>/dev/null || echo 'not a git repo')"

  if [[ "${1:-}" != "--no-llm" ]]; then
    echo "--- Tier 2: LLM extraction + merge ---"
    python3 tier2/extract.py --diff --merge
  else
    echo "--- Tier 2 skipped (--no-llm): using existing tier1/history.json ---"
  fi

  echo "--- Tier 1: forecast + write workbooks ---"
  python3 tier1/forecast.py

  echo "--- Validation ---"
  npm run check:forecasts

  echo "=== done: workbooks in submission/ — upload manually to openstocks.com ==="
} 2>&1 | tee "${LOG}"

echo
echo "Clear-run log saved: ${LOG}"