#!/usr/bin/env python3
"""
Average FRED daily FX rates over Deere fiscal-quarter windows and compute the
year-over-year translation move for each currency.

All rates are converted to a common orientation: USD PER UNIT OF FOREIGN
CURRENCY.  A positive yoy % therefore means the foreign currency APPRECIATED
against the dollar, which TRANSLATES DEERE'S FOREIGN REVENUE UP.

Standard library only.  Reads the fred_*.csv files already downloaded.
"""
import csv
import json
import os
import sys

SCRATCH = ("/private/tmp/claude-501/-Users-cor/"
           "c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad")

# series -> (currency, orientation)
#   "usd_per_fx"  : quoted as USD per 1 unit of the foreign currency
#   "fx_per_usd"  : quoted as foreign-currency units per 1 USD (needs inverting)
SERIES = {
    "DEXUSEU": ("EUR", "usd_per_fx"),
    "DEXUSUK": ("GBP", "usd_per_fx"),
    "DEXUSAL": ("AUD", "usd_per_fx"),
    "DEXBZUS": ("BRL", "fx_per_usd"),
    "DEXINUS": ("INR", "fx_per_usd"),
    "DEXCAUS": ("CAD", "fx_per_usd"),
    "DEXMXUS": ("MXN", "fx_per_usd"),
    "DEXCHUS": ("CNY", "fx_per_usd"),
    "DEXJPUS": ("JPY", "fx_per_usd"),
    "DEXSDUS": ("SEK", "fx_per_usd"),
    "DEXSZUS": ("CHF", "fx_per_usd"),
    "DEXKOUS": ("KRW", "fx_per_usd"),
    "DEXSFUS": ("ZAR", "fx_per_usd"),
}

# Deere fiscal-quarter windows, (start, end) inclusive.  Every period end is a
# date stated in the corresponding 10-Q/10-K in the corpus; each start is the
# day after the preceding quarter's stated end.
WINDOWS = {
    "FY2021Q1": ("2020-11-02", "2021-01-31"),
    "FY2021Q2": ("2021-02-01", "2021-05-02"),
    "FY2021Q3": ("2021-05-03", "2021-08-01"),
    "FY2022Q1": ("2021-11-01", "2022-01-30"),
    "FY2022Q2": ("2022-01-31", "2022-05-01"),
    "FY2022Q3": ("2022-05-02", "2022-07-31"),
    "FY2023Q1": ("2022-10-31", "2023-01-29"),
    "FY2023Q2": ("2023-01-30", "2023-04-30"),
    "FY2023Q3": ("2023-05-01", "2023-07-30"),
    "FY2024Q1": ("2023-10-30", "2024-01-28"),
    "FY2024Q2": ("2024-01-29", "2024-04-28"),
    "FY2024Q3": ("2024-04-29", "2024-07-28"),
    "FY2025Q1": ("2024-10-28", "2025-01-26"),
    "FY2025Q2": ("2025-01-27", "2025-04-27"),
    "FY2025Q3": ("2025-04-28", "2025-07-27"),
    "FY2026Q1": ("2025-11-03", "2026-02-01"),
    "FY2026Q2": ("2026-02-02", "2026-05-03"),
    "FY2026Q3": ("2026-05-04", "2026-08-02"),
}

# (target fiscal quarter) -> (prior-year fiscal quarter) for the yoy move
YOY_PAIRS = [("FY%dQ%d" % (y, q), "FY%dQ%d" % (y - 1, q))
             for y in range(2022, 2027) for q in (1, 2, 3)]


def load(series):
    path = os.path.join(SCRATCH, "fred_%s.csv" % series)
    obs = {}
    with open(path, newline="") as fh:
        r = csv.reader(fh)
        header = next(r)
        for row in r:
            if len(row) < 2:
                continue
            d, v = row[0], row[1].strip()
            if v in ("", "."):
                continue          # FRED holiday / no-quote day: skipped, not zeroed
            try:
                obs[d] = float(v)
            except ValueError:
                continue
    return obs


def window_avg(obs, lo, hi, orientation):
    vals = [v for d, v in obs.items() if lo <= d <= hi]
    if not vals:
        return None, 0
    if orientation == "fx_per_usd":
        vals = [1.0 / v for v in vals]
    return sum(vals) / len(vals), len(vals)


def main():
    out = {}
    for series, (ccy, orient) in SERIES.items():
        obs = load(series)
        rec = {"series": series, "currency": ccy, "orientation_native": orient,
               "windows": {}}
        for name, (lo, hi) in WINDOWS.items():
            avg, n = window_avg(obs, lo, hi, orient)
            rec["windows"][name] = {"avg_usd_per_fx": avg, "n_obs": n,
                                    "start": lo, "end": hi}
        rec["yoy_pct"] = {}
        for tgt, base in YOY_PAIRS:
            cur = rec["windows"].get(tgt, {}).get("avg_usd_per_fx")
            pri = rec["windows"].get(base, {}).get("avg_usd_per_fx")
            rec["yoy_pct"][tgt] = (
                None if (cur is None or pri is None or pri == 0)
                else 100.0 * (cur / pri - 1.0))
        # convenience aliases for the current fiscal year
        for q in ("Q1", "Q2", "Q3"):
            rec["yoy_pct"][q] = rec["yoy_pct"].get("FY2026" + q)
        out[ccy] = rec
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
