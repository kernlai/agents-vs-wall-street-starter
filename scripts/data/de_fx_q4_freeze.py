#!/usr/bin/env python3
"""
Sensitivity: what does Q4 FY2026 currency translation look like if spot rates
freeze at their latest observed level (FRED runs to 2026-08-07, Deere's Q4
window is 2026-08-03..2026-11-01), and does the resulting full-year figure
match the +3.0% / +1.0% / +2.0% currency-translation guidance Deere issued for
FY2026 on 2026-05-21?
"""
import csv
import json
import os

SCRATCH = ("/private/tmp/claude-501/-Users-cor/"
           "c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad")

SERIES = {
    "DEXUSEU": ("EUR", "usd_per_fx"), "DEXUSUK": ("GBP", "usd_per_fx"),
    "DEXUSAL": ("AUD", "usd_per_fx"), "DEXBZUS": ("BRL", "fx_per_usd"),
    "DEXINUS": ("INR", "fx_per_usd"), "DEXCAUS": ("CAD", "fx_per_usd"),
    "DEXMXUS": ("MXN", "fx_per_usd"), "DEXCHUS": ("CNY", "fx_per_usd"),
    "DEXJPUS": ("JPY", "fx_per_usd"), "DEXSDUS": ("SEK", "fx_per_usd"),
    "DEXSZUS": ("CHF", "fx_per_usd"), "DEXKOUS": ("KRW", "fx_per_usd"),
    "DEXSFUS": ("ZAR", "fx_per_usd"),
}
BASKET = {
    "United States": {"USD": 1.00},
    "Canada": {"CAD": 1.00},
    "Western Europe": {"EUR": 0.80, "GBP": 0.12, "SEK": 0.05, "CHF": 0.03},
    "Central Europe and CIS": {"EUR": 1.00},
    "Latin America": {"BRL": 0.72, "MXN": 0.13, "USD": 0.15},
    "Asia, Africa, Oceania, and Middle East": {
        "INR": 0.32, "AUD": 0.20, "CNY": 0.12, "ZAR": 0.06, "JPY": 0.05,
        "KRW": 0.04, "USD": 0.21},
}
# Q4 FY2025 base-quarter geographic mix is not separately disclosed (the 10-K
# gives the full year only), so Q4 FY2025 = FY2025 minus the three published
# quarters, computed here from the quarterly matrices.
Q_ENDS_FY25 = ["2025-01-26", "2025-04-27", "2025-07-27"]


def load_series(s, orient):
    obs = {}
    with open(os.path.join(SCRATCH, "fred_%s.csv" % s), newline="") as fh:
        r = csv.reader(fh)
        next(r)
        for row in r:
            if len(row) < 2 or row[1].strip() in ("", "."):
                continue
            v = float(row[1])
            obs[row[0]] = (1.0 / v) if orient == "fx_per_usd" else v
    return obs


def avg(obs, lo, hi):
    v = [x for d, x in obs.items() if lo <= d <= hi]
    return (sum(v) / len(v)) if v else None


def latest_avg(obs, n=5):
    ds = sorted(obs)[-n:]
    return sum(obs[d] for d in ds) / len(ds)


def main():
    mx = json.load(open(os.path.join(SCRATCH, "matrix.json")))

    def three(end):
        for m in mx:
            if (not m["validation"] and m["period"]
                    and m["period"]["months"] == "Three"
                    and m["period"]["end"] == end):
                return m
        return None

    # Q4 FY2025 regional mix, by subtraction from the FY2025 nine-month matrix
    nine = None
    for m in mx:
        if (not m["validation"] and m["period"]
                and m["period"]["months"] == "Nine"
                and m["period"]["end"] == "2025-07-27"):
            nine = m
    fy_seg = {"PPA": 17311.0, "SAT": 10224.0, "CF": 11382.0}

    moves = {}
    for s, (ccy, orient) in SERIES.items():
        obs = load_series(s, orient)
        base = avg(obs, "2025-07-28", "2025-11-02")
        partial = avg(obs, "2026-08-03", "2026-08-07")
        froz = partial if partial is not None else latest_avg(obs)
        moves[ccy] = 100.0 * (froz / base - 1.0)
    moves["USD"] = 0.0

    def region_move(region):
        return sum(sh * moves[c] for c, sh in BASKET[region].items())

    print("Q4 FY2026 yoy FX move if spot freezes at the 2026-08-03..07 level:")
    for c in sorted(moves, key=lambda x: -abs(moves[x])):
        print("   %-4s %+7.2f%%" % (c, moves[c]))
    print()
    for r in BASKET:
        print("   region %-40s %+7.2f%%" % (r, region_move(r)))

    # Q4 FY2025 mix = nine-month matrix subtracted from the full year is not
    # available on a comparable rev-rec basis for the geography split, so the
    # Q3 FY2025 mix is used as the Q4 proxy and that is stated as a limitation.
    q3 = three("2025-07-27")
    rows = {}
    for lab, v in q3["geo"].items():
        for canon in BASKET:
            if canon.lower() in lab.lower() or (
                    canon.startswith("Asia") and lab.lower().startswith("asia")):
                rows[canon] = v
    idx = {"PPA": 0, "SAT": 1, "CF": 2, "TOTAL": 4}
    print()
    K = 0.9260123233019592
    out = {}
    for seg, i in idx.items():
        tot = sum(rows[c][i] for c in BASKET)
        eff = sum(rows[c][i] / tot * region_move(c) for c in BASKET)
        out[seg] = {"naive_pp": eff, "calibrated_pp": eff * K}
        print("Q4 FY2026 %-6s naive %+6.2fpp  calibrated %+6.2fpp"
              % (seg, eff, eff * K))

    # full-year check against guidance
    print()
    ly = {"PPA": [3067, 5230, 4273], "SAT": [1748, 2994, 3025],
          "CF": [1994, 2947, 3059]}
    est_q3 = {"PPA": 1.7819, "SAT": 0.2135, "CF": 0.4999}
    disc = {"PPA": [4, 3], "SAT": [2, 2], "CF": [4, 3]}
    guide = {"PPA": 3.0, "SAT": 1.0, "CF": 2.0}
    for seg in ("PPA", "SAT", "CF"):
        q4_ly = fy_seg[seg] - sum(ly[seg])
        usd = (disc[seg][0] / 100.0 * ly[seg][0] + disc[seg][1] / 100.0 * ly[seg][1]
               + est_q3[seg] / 100.0 * ly[seg][2]
               + out[seg]["calibrated_pp"] / 100.0 * q4_ly)
        pct = 100.0 * usd / fy_seg[seg]
        print("%-4s FY2026 implied currency %+5.2f%% (%+.0f USDm) vs guidance %+.1f%%"
              % (seg, pct, usd, guide[seg]))


if __name__ == "__main__":
    main()
