#!/usr/bin/env python3
"""Implements the official Agents vs Wall Street accuracy formula (JUDGING.md).

    metric score = min(5.0, team_miss / max(wall_street_miss, floor))
    final score  = mean of the 12 metric scores      (lower is better)

Floors, per JUDGING.md:
    percentage metric  -> 0.5 percentage points
    money / EPS metric -> 0.5% of |reported result|, with a fixed fallback at zero
    missing forecast   -> 5.0 (not a disqualification)

Use it two ways:
  1. Backtest: score a candidate forecast for a HISTORICAL quarter, where the
     reported result is known and a consensus figure stands in for the Wall
     Street benchmark. This is the only way to evaluate the agent before the
     companies report.
  2. Post-mortem: after 20 Aug, score the real submission.

The real Wall Street benchmark is frozen internally at 18:00 and never given to
teams, so any score produced here is an ESTIMATE whose quality depends entirely
on the consensus proxy supplied.

    python3 scripts/score.py evaluation/backtests/de-fy2025q3.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CAP = 5.0
PCT_FLOOR = 0.5           # percentage points
MONEY_FLOOR_FRAC = 0.005  # 0.5% of the reported result
ZERO_FALLBACK = 0.01      # used only when the reported result is 0


def is_percentage(units: str) -> bool:
    return units.strip().lower() in {"%", "percent", "pp", "percentage points"}


def floor_for(units: str, reported: float) -> float:
    """Denominator floor. Stops a near-perfect consensus making every score huge."""
    if is_percentage(units):
        return PCT_FLOOR
    if reported == 0:
        return ZERO_FALLBACK
    return abs(reported) * MONEY_FLOOR_FRAC


def score_metric(forecast, reported: float, benchmark, units: str) -> dict:
    if forecast is None:
        return {
            "score": CAP, "team_miss": None, "ws_miss": None,
            "denominator": None, "beat_ws": False, "note": "missing forecast -> 5.0",
        }
    team_miss = abs(forecast - reported)
    if benchmark is None:
        return {
            "score": None, "team_miss": team_miss, "ws_miss": None,
            "denominator": None, "beat_ws": None,
            "note": "no benchmark supplied - miss reported, score not computable",
        }
    ws_miss = abs(benchmark - reported)
    denom = max(ws_miss, floor_for(units, reported))
    raw = team_miss / denom
    return {
        "score": min(CAP, raw), "team_miss": team_miss, "ws_miss": ws_miss,
        "denominator": denom, "beat_ws": team_miss < ws_miss,
        "note": "capped at 5.0" if raw > CAP else "",
    }


def run(case: dict) -> dict:
    rows, scores = [], []
    for m in case["metrics"]:
        r = score_metric(m.get("forecast"), m["reported"], m.get("benchmark"), m.get("units", ""))
        r["label"] = m["label"]
        r["units"] = m.get("units", "")
        r["forecast"] = m.get("forecast")
        r["reported"] = m["reported"]
        r["benchmark"] = m.get("benchmark")
        rows.append(r)
        if r["score"] is not None:
            scores.append(r["score"])
    return {
        "case": case.get("name", "unnamed"),
        "rows": rows,
        "final": (sum(scores) / len(scores)) if scores else None,
        "n_scored": len(scores),
        "n_beat_ws": sum(1 for r in rows if r["beat_ws"]),
    }


def fmt(v, nd=2):
    return "—" if v is None else f"{v:,.{nd}f}"


def report(res: dict) -> None:
    print(f"\n  {res['case']}")
    print("  " + "-" * 96)
    print(f"  {'metric':<42}{'fcst':>10}{'actual':>10}{'street':>10}{'miss':>9}{'score':>8}{'':>5}")
    print("  " + "-" * 96)
    for r in res["rows"]:
        flag = "beat" if r["beat_ws"] else ("" if r["beat_ws"] is None else "    ")
        print(
            f"  {r['label'][:41]:<42}{fmt(r['forecast']):>10}{fmt(r['reported']):>10}"
            f"{fmt(r['benchmark']):>10}{fmt(r['team_miss']):>9}{fmt(r['score']):>8}  {flag}"
        )
        if r["note"]:
            print(f"  {'':<42}{r['note']}")
    print("  " + "-" * 96)
    if res["final"] is not None:
        verdict = "beats Wall Street on average" if res["final"] < 1.0 else "Wall Street closer on average"
        print(f"  final score {res['final']:.3f} over {res['n_scored']} metrics "
              f"({res['n_beat_ws']} beat street) — {verdict}")
    else:
        print("  final score not computable — no benchmarks supplied")
    print()


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    finals = []
    for p in argv[1:]:
        case = json.loads(Path(p).read_text())
        res = run(case)
        report(res)
        if res["final"] is not None:
            finals.append(res["final"])
    if len(finals) > 1:
        print(f"  ACROSS {len(finals)} CASES: mean final score {sum(finals)/len(finals):.3f}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
