#!/usr/bin/env python3
"""Sanity layer for the 12 forecasts, run BEFORE anything is written to a workbook.

The organisers' own `npm run check:forecasts` only confirms that a cell holds a
finite number. It will happily accept 0.045 where 4.5 was meant, or 12.35 where
12,350 was meant. Those are the errors that actually happen, and each one costs a
full 5.0 on that metric — the same as submitting nothing at all.

Checks applied, in order of how often they catch something real:

  UNITS      percentage metrics must be in POINTS (4.5 == 4.5%), never fractions
             (0.045) and never basis points (450). EPS must be per-share sized;
             Hays EPS is in PENCE, not pounds.
  SCALE      a figure within a plausible multiple of the prior-year actual.
             Catches the thousands/millions slip and the 10x fat finger.
  SIGN       margins and EPS that go negative need an explicit override.
  COHERENCE  the three metrics for a company must be mutually consistent —
             an implied margin outside a sane band means the model disagrees
             with itself.
  COMPLETE   all 12 present. A blank scores 5.0, so a crude number always wins.

Priors live in evaluation/priors.json. A metric with NO prior FAILS rather than
passing silently: an unchecked number is the thing this script exists to prevent.

    python3 scripts/validate_forecasts.py evaluation/forecasts.json
    echo $?     # 0 = clean, 1 = warnings only, 2 = errors present
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPANIES = ROOT / "challenge" / "companies.json"
PRIORS = ROOT / "evaluation" / "priors.json"

# How far from the prior-year actual a forecast may sit before we complain.
# The FAIL threshold hunts SCALE ERRORS (10x, 1000x), not large-but-real moves.
# It was originally 0.60 and produced a false positive on ADI, whose EPS is
# legitimately +66% coming out of a semiconductor downcycle. A genuine unit slip
# is an order of magnitude out, so 3x is the right place to draw the line.
SCALE_WARN = 0.25   # +/-25%  -> warn, look at it
SCALE_FAIL = 2.00   # +/-200% -> error, almost certainly a scale slip

# Below this ratio to the prior, a percentage figure is a fraction (0.005 for 0.5%)
# rather than a small-but-real value (+0.5% against a prior of +1.0%).
FRACTION_RATIO = 0.02
FRACTION_ABS = 0.10  # a percentage-point figure below this is a fraction error

ERR, WARN, OK = "ERROR", "warn", "ok"


class Findings:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, level: str, where: str, msg: str) -> None:
        self.rows.append((level, where, msg))

    @property
    def errors(self) -> int:
        return sum(1 for l, _, _ in self.rows if l == ERR)

    @property
    def warnings(self) -> int:
        return sum(1 for l, _, _ in self.rows if l == WARN)


def is_pct(units: str) -> bool:
    return units.strip().lower() in {"%", "percent", "pp"}


def is_eps(units: str) -> bool:
    u = units.strip().lower()
    return "share" in u or u == "gbp"


def check_units(f: Findings, where: str, value: float, units: str, label: str, prior=None) -> None:
    """The single highest-yield check. Percentage and per-share scale errors are
    silent to the organisers' checker and cost a full 5.0.

    The fraction test is PRIOR-AWARE. A flat |value| < 1 rule wrongly rejected
    Home Depot's +0.5% comparable sales, which is a perfectly ordinary reading
    against a prior of +1.0%. A real fraction error is ~100x too small, so we
    compare against the prior where one exists."""
    if is_pct(units):
        if value != 0:
            if abs(value) < FRACTION_ABS:
                # A percentage-point figure below 0.1 is essentially always a fraction
                # error. Genuine sub-0.1pp readings round to 0.1 in practice.
                f.add(ERR, where, f"{label}: {value} is below {FRACTION_ABS} percentage points. "
                                  f"Almost certainly a FRACTION — percentages go in as points: "
                                  f"4.5 means 4.5%, not 0.045.")
            elif prior not in (None, 0) and abs(value / prior) < FRACTION_RATIO:
                f.add(ERR, where, f"{label}: {value} is {abs(prior/value):.0f}x smaller than the "
                                  f"prior-year {prior}. Looks like a FRACTION.")
        if abs(value) > 100:
            f.add(ERR, where, f"{label}: {value} looks like BASIS POINTS or a "
                              f"mis-scaled percentage. Expected roughly -50..100.")
    elif is_eps(units):
        if units.strip().upper() == "GBP" or "GBp" in units:
            if abs(value) > 200:
                f.add(ERR, where, f"{label}: {value} is too large for pence-per-share.")
            elif 0 < abs(value) < 1:
                f.add(ERR, where, f"{label}: {value} looks like POUNDS. Hays EPS is in PENCE "
                                  f"— 6.2 means 6.2p.")
        elif abs(value) > 100:
            f.add(ERR, where, f"{label}: {value} is implausibly large for EPS per share.")


def check_scale(f: Findings, where: str, value: float, prior, label: str) -> None:
    if prior in (None, 0):
        f.add(ERR, where, f"{label}: NO PRIOR available — cannot range-check. "
                          f"Add the prior-year actual to evaluation/priors.json before submitting.")
        return
    dev = (value - prior) / abs(prior)
    if abs(dev) >= SCALE_FAIL:
        f.add(ERR, where, f"{label}: {value:,.4g} is {dev:+.0%} vs prior-year {prior:,.4g}. "
                          f"Check for a scale error (thousands/millions, or a 10x slip).")
    elif abs(dev) >= SCALE_WARN:
        f.add(WARN, where, f"{label}: {value:,.4g} is {dev:+.0%} vs prior-year {prior:,.4g}. "
                           f"Large but possible — make sure this is intended.")


def check_sign(f: Findings, where: str, value: float, units: str, label: str, allow_neg: bool) -> None:
    if value < 0 and not allow_neg:
        f.add(WARN, where, f"{label}: negative ({value}). Allowed, but flag it explicitly "
                           f"in the run log if intended.")


def check_coherence(f: Findings, ticker: str, vals: dict, priors: dict) -> None:
    """Cross-metric consistency. Catches a model that disagrees with itself —
    e.g. a revenue forecast and a segment-profit forecast implying an absurd margin."""
    if ticker == "DE":
        rev = vals.get("Worldwide net sales and revenues")
        ppa = vals.get("Production & Precision Ag operating profit")
        ppa_sales = priors.get("_ppa_net_sales_estimate")
        if rev and ppa and ppa_sales:
            margin = ppa / ppa_sales * 100
            if not (5 <= margin <= 25):
                f.add(ERR, ticker, f"implied PPA margin {margin:.1f}% on estimated PPA sales "
                                   f"{ppa_sales:,.0f} is outside 5-25%. Revenue and segment "
                                   f"profit forecasts disagree.")
            elif not (9 <= margin <= 17):
                f.add(WARN, ticker, f"implied PPA margin {margin:.1f}% sits outside the "
                                    f"11-13% guided band — justify it.")
    if ticker == "ADI":
        gm = vals.get("Adjusted gross margin")
        if gm is not None and not (50 <= gm <= 80):
            f.add(WARN, ticker, f"adjusted gross margin {gm}% is outside the 50-80% range "
                                f"typical for analog semiconductors.")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    forecasts = json.loads(Path(argv[1]).read_text())
    companies = json.loads(COMPANIES.read_text())["companies"]
    priors = json.loads(PRIORS.read_text()) if PRIORS.exists() else {}

    f = Findings()
    seen = 0
    for c in companies:
        t = c["ticker"].split(":")[-1]
        got = forecasts.get(t, {})
        cp = priors.get(t, {})
        vals: dict[str, float] = {}
        for m in c["metrics"]:
            label, units = m["label"], m["units"]
            where = f"{t}/{label[:28]}"
            v = got.get(label)
            if v is None:
                f.add(ERR, where, "MISSING — an empty cell scores 5.0, the same as the worst "
                                  "possible wrong answer. Always submit a number.")
                continue
            if not isinstance(v, (int, float)):
                f.add(ERR, where, f"not numeric: {v!r}")
                continue
            seen += 1
            vals[label] = float(v)
            check_units(f, where, float(v), units, label, cp.get(label))
            check_scale(f, where, float(v), cp.get(label), label)
            check_sign(f, where, float(v), units, label, allow_neg=is_pct(units))
        check_coherence(f, t, vals, cp)

    width = 100
    print("\n  forecast validation")
    print("  " + "-" * width)
    if not f.rows:
        print("  no findings — all checks clean")
    for level, where, msg in sorted(f.rows, key=lambda r: (r[0] != ERR, r[1])):
        tag = "ERROR" if level == ERR else "warn "
        print(f"  [{tag}] {where}")
        print(f"          {msg}")
    print("  " + "-" * width)
    print(f"  {seen}/12 forecasts present · {f.errors} errors · {f.warnings} warnings\n")
    return 2 if f.errors else (1 if f.warnings else 0)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
