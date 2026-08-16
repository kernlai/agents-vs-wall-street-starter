# Tier 2 — LLM extraction

Automates the Tier 1 manual loop: for each company, an LLM reads the latest
8-Ks/trading updates + call-presentation transcript and emits history.json-format
data — historical values with file citations, plus an `override` when the company
gave explicit guidance for the target period. Everything downstream
(tier1/forecast.py, validation, workbooks) is unchanged.

## Layout

Place in the repo root: `tier2/extract.py` and `run_final.sh` (root, `chmod +x run_final.sh`).

## Setup

```bash
export OPENAI_API_KEY=sk-...     # or put OPENAI_API_KEY=... in .env at the repo root
export OPENAI_MODEL=gpt-5        # optional; this is the default — change if needed
```

## The critical first test: reproduce the ground truth

tier1/history.json was hand-verified against the corpus, so it is a regression
test for the extractor. Run:

```bash
python3 tier2/extract.py --diff
```

Read the diff for each company:
- **MISMATCH** on a value → extraction error; inspect the cited quote, tune the prompt.
- **MISSED GUIDANCE** → the extractor failed to find an override the documents contain
  (ADI revenue/EPS and HAS operating profit are the known ones — it MUST find these).
- "new — not in ground truth" → usually fine (extra periods); spot-check a few.
- "in ground truth but NOT extracted" → fine if the model still has enough periods;
  the forecaster needs same-period-last-year plus one growth pair.

Only after the diff looks clean:

```bash
python3 tier2/extract.py --merge     # backs up history.json first
python3 tier1/forecast.py
npm run check:submission
```

## Final run

```bash
./run_final.sh            # full agent: extract -> merge -> forecast -> validate, logged
./run_final.sh --no-llm   # fallback: Tier 1 only from existing history.json
```

The log lands in logs/ and doubles as the required clear-run log.

## Failure modes

- Invalid model output fails validation loudly and saves the raw response to
  tier2/raw-<TICKER>.txt for inspection; the merge never sees bad data.
- If the API is down at 17:15, run `./run_final.sh --no-llm` — the last good
  history.json still produces a full valid submission.
- Testing without burning credits: OPENAI_MOCK_FILE=<file> makes call_openai
  return that file's contents instead of calling the API.
