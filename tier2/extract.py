#!/usr/bin/env python3
"""Tier 2 — LLM extraction of historicals + guidance from the corpus.

Automates the manual loop from Tier 1: read each company's latest documents,
extract the historical figures and any explicit guidance for the target period,
and emit history.json-format data with citations. Downstream (tier1/forecast.py)
is unchanged.

Usage, from the repo root:

    export OPENAI_API_KEY=sk-...            # or put it in .env
    python3 tier2/extract.py                 # all four companies
    python3 tier2/extract.py HD ADI          # subset
    python3 tier2/extract.py --diff          # compare vs tier1/history.json (ground truth)
    python3 tier2/extract.py --merge         # write results into tier1/history.json (backs it up first)

Outputs tier2/extracted-<TICKER>.json regardless; --merge is opt-in.

Model: env OPENAI_MODEL (default "gpt-5"). Stdlib only — no pip installs.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "challenge" / "offline-data"
COMPANIES = ROOT / "challenge" / "companies.json"
HISTORY = ROOT / "tier1" / "history.json"
OUT_DIR = Path(__file__).resolve().parent

COMPANY_DIRS = {"HD": "home-depot", "ADI": "analog-devices", "DE": "deere", "HAS": "hays"}

# Document selection. Three layers:
#   1. RECENT: newest events per folder (deduped: q1-8k and q1-8k-2 are one event).
#   2. ANCHOR: the prior-year documents matching the TARGET period — these hold
#      same-period-last-year actuals, which the forecaster cannot run without.
#   3. Slides included (Hays reports absolute figures in results presentations,
#      not in its quarterly trading updates). 10-Qs/10-Ks excluded (too large).
DOC_PICKS = [
    ("filings", r"-(q\d-8k|fy-8k)", 3),
    ("call-transcripts", r"-call(-q\d)?(-h\d)?-pres", 3),
    ("slides", r"-slide", 2),
]
PER_DOC_CHAR_CAP = 45_000
TOTAL_CHAR_CAP = 220_000


def event_key(p: Path) -> str:
    """q1-8k, q1-8k-2 and different ids collapse to one event."""
    stem = re.sub(r"__\d+$", "", p.stem)          # drop trailing id
    stem = re.sub(r"-\d+$", "", stem)             # drop -2/-3 variant suffix
    return stem


def anchor_documents(ticker: str, target: str, already: set[str]) -> list[Path]:
    """Prior-year documents for the target period: the same-quarter-last-year
    actuals (e.g. target FY2026Q3 -> 2025 files tagged q3), or for annual
    targets the prior-year results (files tagged h2/fy or dated Jul-Sep)."""
    base = CORPUS / COMPANY_DIRS[ticker]
    m = re.match(r"FY(\d{4})(?:Q(\d))?$", target)
    if not m:
        return []
    prev_year = int(m.group(1)) - 1
    q = m.group(2)
    tag_rx = re.compile(rf"q{q}" if q else r"(h2|fy|results|slide)", re.IGNORECASE)
    picked = []
    for folder in ("filings", "call-transcripts", "slides"):
        for p in sorted((base / folder).glob(f"{prev_year}-*.md"), reverse=True):
            if "10-q" in p.name or "10q" in p.name or "10-k" in p.name:
                continue
            # annual targets: prior-year results land Jul-Sep for Hays
            month_ok = (not q) and p.name[5:7] in ("07", "08", "09")
            if (tag_rx.search(p.name) or month_ok) and event_key(p) not in already:
                picked.append(p)
                already.add(event_key(p))
            if len(picked) >= 3:
                return picked
    return picked

PERIOD_RE = re.compile(r"^FY\d{4}(?:[QH]\d)?$")

SYSTEM_PROMPT = """You are a meticulous financial-data extractor. You will receive excerpts of a company's recent filings and earnings-call transcripts, each introduced by a line 'FILE: <path>'.

Your job: for each requested metric, extract REPORTED historical values and, separately, any EXPLICIT company guidance for the target period.

Rules:
1. Output STRICT JSON only. No markdown fences, no commentary.
2. Schema (top-level keys are the EXACT metric labels as given, WITHOUT the bracketed units):
{
  "<metric label>": {
    "series": { "<PERIOD>": { "value": <number>, "source": "<file>: <short verbatim quote>" }, ... },
    "override": { "value": <number or null>, "source": "<file>: <short verbatim quote>" }
  }, ...
}
3. PERIOD labels: FY2026Q2 (fiscal quarter), FY2026H1 (fiscal half), FY2026 (fiscal year). Use the COMPANY'S fiscal calendar as the documents do.
4. For each metric, extract at minimum: the same period one year before the target, the same period two years before if present, and the most recent reported period plus its prior-year comparative. More periods are welcome.
5. Units must match exactly what is requested (millions for amounts; per-share in dollars, or PENCE for Hays; percentages as points, e.g. 4.5 for 4.5%). Convert billions to millions.
6. "override" is ONLY for explicit forward guidance FOR THE TARGET PERIOD stated by the company (e.g. 'for the third quarter we are forecasting revenue of $3.9 billion'). Use the midpoint of a range unless the company signals top/bottom (e.g. 'top of the range' means the top). Full-year guidance is NOT an override for a quarterly target. If none exists, set value to null.
7. Transcripts may garble currency symbols ($ appearing as DKK or EUR euro signs). Values for US companies are USD.
8. NEVER invent a number. If a required value is absent from the excerpts, omit that period.
9. Every source must name the file and quote the sentence fragment containing the number."""


def load_env_key() -> str | None:
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            m = re.match(r"\s*OPENAI_API_KEY\s*=\s*(.+)\s*$", line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return None


def pick_documents(ticker: str, target: str) -> list[Path]:
    """ANCHORS FIRST: the prompt is truncated tail-first when it exceeds the
    budget, so document order is priority order. Prior-year anchors (small,
    indispensable) lead; recent filings (guidance) next; transcripts and
    slides last, where truncation can afford to bite."""
    base = CORPUS / COMPANY_DIRS[ticker]
    prev_year = int(re.match(r"FY(\d{4})", target).group(1)) - 1
    recent: list[Path] = []
    seen: set[str] = set()
    for folder, pattern, cap in DOC_PICKS:
        rx = re.compile(pattern)
        n = 0
        for p in sorted((base / folder).glob("*.md"), key=lambda p: p.name, reverse=True):
            if n >= cap:
                break
            if folder == "slides" and p.name < f"{prev_year}-":
                continue  # stale decks waste budget
            if rx.search(p.name) and event_key(p) not in seen:
                recent.append(p)
                seen.add(event_key(p))
                n += 1
    anchors = anchor_documents(ticker, target, seen)
    return anchors + recent


def build_user_prompt(ticker: str, company: dict) -> str:
    docs = pick_documents(ticker, company['period'])
    if not docs:
        raise SystemExit(f"{ticker}: no documents matched — check DOC_PICKS patterns")
    parts = [
        f"Company: {company['company']} ({company['ticker']})",
        f"TARGET PERIOD to forecast (do not extract it as history; it has not been reported): {company['period']}",
        "Metrics and required units:",
    ]
    parts += [f"- {m['label']} [{m['units']}]" for m in company["metrics"]]
    parts.append("\n--- DOCUMENT EXCERPTS ---")
    budget = TOTAL_CHAR_CAP
    for doc in docs:
        text = doc.read_text(errors="replace")[:PER_DOC_CHAR_CAP]
        if len(text) > budget:
            text = text[:budget]
        budget -= len(text)
        parts.append(f"\nFILE: {doc.relative_to(ROOT)}\n{text}")
        if budget <= 0:
            break
    return "\n".join(parts)


def call_openai(system: str, user: str) -> str:
    mock = os.environ.get("OPENAI_MOCK_FILE")  # testing hook: canned response, no API call
    if mock:
        return Path(mock).read_text()
    key = load_env_key()
    if not key:
        raise SystemExit("OPENAI_API_KEY not set (env or .env in repo root)")
    model = os.environ.get("OPENAI_MODEL", "gpt-5")
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


def parse_and_validate(raw: str, company: dict) -> dict:
    """Strict-ish validation so a malformed extraction fails HERE, not at forecast time."""
    text = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    data = json.loads(text)
    # Models sometimes echo the units into the key ("Net sales [USDm]") — normalize.
    data = {re.sub(r"\s*\[[^\]]*\]\s*$", "", k): v for k, v in data.items()}
    problems: list[str] = []
    expected = {m["label"] for m in company["metrics"]}
    for label in expected:
        if label not in data:
            problems.append(f"missing metric: {label}")
            continue
        spec = data[label]
        series = spec.get("series", {})
        if not isinstance(series, dict) or not series:
            problems.append(f"{label}: empty series")
        for period, entry in series.items():
            if not PERIOD_RE.match(period):
                problems.append(f"{label}: bad period label {period!r}")
            if period == company["period"]:
                problems.append(f"{label}: target period {period} extracted as history")
            v = entry.get("value") if isinstance(entry, dict) else None
            if not isinstance(v, (int, float)):
                problems.append(f"{label}/{period}: non-numeric value {v!r}")
            if isinstance(entry, dict) and not str(entry.get("source", "")).strip():
                problems.append(f"{label}/{period}: missing source citation")
        ov = spec.get("override")
        if ov is not None and not isinstance(ov, dict):
            problems.append(f"{label}: override must be an object")
    extras = set(data) - expected
    for e in extras:
        problems.append(f"unexpected metric key: {e!r}")
    if problems:
        raise ValueError("extraction failed validation:\n  " + "\n  ".join(problems))
    return {k: data[k] for k in expected}


def to_history_block(company: dict, extracted: dict) -> dict:
    metrics = {}
    for m in company["metrics"]:
        spec = extracted[m["label"]]
        block = {
            # % metrics mean-revert; everything else extrapolates
            "method": "pct_blend" if m["units"] == "%" else "growth",
            "series": spec["series"],
        }
        ov = spec.get("override") or {}
        if ov.get("value") is not None:
            block["override"] = {"value": ov["value"], "source": ov.get("source", "")}
        metrics[m["label"]] = block
    return {"target": company["period"], "metrics": metrics}


def diff_against(ground: dict, ticker: str, block: dict) -> list[str]:
    """Compare extracted values to tier1/history.json (the hand-verified ground truth)."""
    notes = []
    gt = ground.get(ticker, {}).get("metrics", {})
    for label, spec in block["metrics"].items():
        gt_series = {
            p: e.get("value") for p, e in gt.get(label, {}).get("series", {}).items()
            if isinstance(e, dict) and e.get("value") is not None
        }
        for period, entry in spec["series"].items():
            v = entry["value"]
            if period in gt_series:
                g = gt_series[period]
                if abs(v - g) > 1e-9:
                    sev = "MISMATCH" if abs(v - g) > 0.005 * max(abs(g), 1) else "minor diff"
                    notes.append(f"{ticker}/{label}/{period}: extracted {v} vs ground truth {g}  <-- {sev}")
            else:
                notes.append(f"{ticker}/{label}/{period}: {v} (new — not in ground truth)")
        missing = set(gt_series) - set(spec["series"])
        for p in sorted(missing):
            notes.append(f"{ticker}/{label}/{p}: in ground truth but NOT extracted")
        gt_ov = gt.get(label, {}).get("override", {}).get("value")
        ex_ov = (spec.get("override") or {}).get("value")
        if gt_ov is not None and ex_ov is None:
            notes.append(f"{ticker}/{label}: ground truth has override {gt_ov}, extraction found none  <-- MISSED GUIDANCE")
        elif ex_ov is not None:
            notes.append(f"{ticker}/{label}: extracted override {ex_ov}" + (f" (ground truth {gt_ov})" if gt_ov is not None else " (new)"))
    return notes


def main() -> int:
    args = [a for a in sys.argv[1:]]
    do_diff = "--diff" in args
    do_merge = "--merge" in args
    tickers = [a.upper() for a in args if not a.startswith("--")] or list(COMPANY_DIRS)

    companies = {c["ticker"].split(":")[-1]: c for c in json.loads(COMPANIES.read_text())["companies"]}
    ground = json.loads(HISTORY.read_text()) if HISTORY.exists() else {}

    merged = dict(ground)
    for ticker in tickers:
        company = companies[ticker]
        print(f"\n=== {ticker}: selecting documents ===")
        for d in pick_documents(ticker, company['period']):
            print(f"  {d.relative_to(ROOT)}")
        prompt = build_user_prompt(ticker, company)
        print(f"  prompt: {len(prompt):,} chars — calling model...")
        t0 = time.time()
        raw = call_openai(SYSTEM_PROMPT, prompt)
        print(f"  model replied in {time.time()-t0:.0f}s")
        try:
            extracted = parse_and_validate(raw, company)
        except (ValueError, json.JSONDecodeError) as e:
            raw_path = OUT_DIR / f"raw-{ticker}.txt"
            raw_path.write_text(raw)
            print(f"  EXTRACTION INVALID — raw response saved to {raw_path.relative_to(ROOT)}")
            print(f"  {e}")
            return 1
        block = to_history_block(company, extracted)
        out = OUT_DIR / f"extracted-{ticker}.json"
        out.write_text(json.dumps(block, indent=2))
        print(f"  wrote {out.relative_to(ROOT)}")
        if do_diff and ground:
            print("  --- diff vs tier1/history.json ---")
            for note in diff_against(ground, ticker, block) or ["  (identical)"]:
                print(f"  {note}")
        merged[ticker] = block

    if do_merge:
        backup = HISTORY.with_suffix(f".backup-{time.strftime('%H%M%S')}.json")
        if HISTORY.exists():
            backup.write_text(HISTORY.read_text())
            print(f"\nbacked up history.json -> {backup.name}")
        # preserve the _readme if present
        if "_readme" in ground:
            merged = {"_readme": ground["_readme"], **{k: v for k, v in merged.items() if k != "_readme"}}
        HISTORY.write_text(json.dumps(merged, indent=2))
        print(f"merged into {HISTORY.relative_to(ROOT)} — now run: python3 tier1/forecast.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())