#!/usr/bin/env bash
# The final command. Processes all four companies and produces the four workbooks,
# writing a timestamped log to logs/ as the rules require.
#
#   ./scripts/run.sh
#
# Stages:
#   1. validate   sanity-check the twelve forecasts (units, scale, sign, coherence)
#   2. write      render the four workbooks from the supplied templates
#   3. check      run the organisers' own entry and forecast checks
#
# Validation WARNINGS do not stop the run; validation ERRORS do, because an error
# means a number is wrong in a way that passes the organisers' checker silently and
# costs a full 5.0 on that metric.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="logs/run-${RUN_ID}.log"
mkdir -p logs submission

# tee everything, and timestamp each line
exec > >(while IFS= read -r line; do printf '%s  %s\n' "$(date -u +%H:%M:%SZ)" "$line"; done | tee "$LOG") 2>&1

echo "=== Agents vs Wall Street — final run ${RUN_ID} ==="
echo "commit:  $(git rev-parse HEAD 2>/dev/null || echo 'not a git repo')"
echo "branch:  $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '-')"
echo "dirty:   $(if [ -n "$(git status --porcelain 2>/dev/null)" ]; then echo yes; else echo no; fi)"
echo "python:  $(python3 --version 2>&1)"
echo "node:    $(node --version 2>&1)"
echo

echo "--- stage 1/3: validate forecasts ---"
python3 scripts/validate_forecasts.py evaluation/forecasts.json
VALIDATE=$?
if [ $VALIDATE -ge 2 ]; then
  echo
  echo "ABORTED: validation errors. No workbooks written."
  echo "Every blocked metric would otherwise score 5.0 — the same as submitting nothing."
  exit 1
fi
[ $VALIDATE -eq 1 ] && echo "(warnings only — continuing)"
echo

echo "--- stage 2/3: write workbooks ---"
python3 scripts/write_workbooks.py
WRITE=$?
echo

echo "--- stage 3/3: organisers' checks ---"
npm run --silent check:submission
CHECK=$?
echo

echo "=== summary ==="
echo "validate: $([ $VALIDATE -eq 0 ] && echo clean || echo warnings)"
echo "write:    $([ $WRITE -eq 0 ] && echo 'all four' || echo incomplete)"
echo "check:    $([ $CHECK -eq 0 ] && echo pass || echo FAIL)"
ls -la submission/*.xlsx 2>/dev/null || echo "no workbooks present"
echo
echo "log written to ${LOG}"
[ $WRITE -eq 0 ] && [ $CHECK -eq 0 ] && echo "READY TO UPLOAD" || echo "NOT READY"
exit $(( WRITE != 0 || CHECK != 0 ))
