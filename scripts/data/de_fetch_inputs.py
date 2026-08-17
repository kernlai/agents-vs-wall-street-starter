#!/usr/bin/env python3
"""
Fetch the macro input-cost series for the Deere Q3 FY2026 cost build, and map
them onto Deere's fiscal quarters.

Keyless FRED CSV endpoint. Missing observations stay missing (FRED writes "."),
they are never zero-filled.
"""
import csv, io, json, os, sys, urllib.request, datetime, argparse

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
UA = {"User-Agent": "deere-q3-cost-research/1.0 (cor@salomo.io)"}

SERIES = {
    # id: (label, units, family)
    "WPU101707": ("PPI: hot rolled steel sheet and strip", "index_1982_100", "steel"),
    "WPU1012":   ("PPI: steel mill products", "index_1982_100", "steel"),
    "WPU101211": ("PPI: iron and steel scrap", "index_1982_100", "scrap"),
    "PIORECRUSDM": ("Global price of iron ore", "usd_per_tonne", "iron_ore"),
    "PALUMUSDM": ("Global price of aluminum", "usd_per_tonne", "aluminium"),
    "PCOPPUSDM": ("Global price of copper", "usd_per_tonne", "copper"),
    "PRUBBUSDM": ("Global price of rubber", "us_cents_per_pound", "rubber"),
    "WPU057303": ("PPI: no. 2 diesel fuel", "index_1982_100", "diesel"),
    "GASDESW":   ("US no.2 diesel retail price, all types", "usd_per_gallon", "diesel"),
    "PCU484121484121": ("PPI: general freight trucking, long-distance TL",
                        "index_dec2003_100", "freight"),
    "WPU111":    ("PPI: agricultural machinery and equipment", "index_1982_100", "farm_machinery_ppi"),
    "PCU333111333111": ("PPI: farm machinery and equipment manufacturing",
                        "index_dec1984_100", "farm_machinery_ppi"),
    "CUSR0000SETA02": ("CPI: used cars and trucks (unrelated placebo control)",
                       "index_1982_84_100", "control"),
    "PPIACO": ("PPI: all commodities (broad inflation control)", "index_1982_100", "control"),
    "CPIAUCSL": ("CPI: all urban consumers, all items (broad inflation control)",
                 "index_1982_84_100", "control"),
}


def fetch(sid):
    req = urllib.request.Request(FRED.format(sid), headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        txt = r.read().decode("utf-8", "replace")
    out = []
    rdr = csv.reader(io.StringIO(txt))
    head = next(rdr, None)
    if not head or len(head) < 2:
        raise RuntimeError(f"{sid}: unexpected CSV head {head!r}")
    for row in rdr:
        if len(row) < 2:
            continue
        d, v = row[0].strip(), row[1].strip()
        if v in (".", "", "NA"):
            continue          # missing stays missing
        try:
            out.append((d, float(v)))
        except ValueError:
            continue
    if not out:
        raise RuntimeError(f"{sid}: no observations parsed")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = {}
    for sid, (lab, units, fam) in SERIES.items():
        try:
            obs = fetch(sid)
            data[sid] = {"label": lab, "units": units, "family": fam, "obs": obs}
            print(f"{sid:22} n={len(obs):5} {obs[0][0]} .. {obs[-1][0]} last={obs[-1][1]}",
                  file=sys.stderr)
        except Exception as e:
            print(f"{sid:22} FAILED {e}", file=sys.stderr)
    open(a.out, "w").write(json.dumps(data))


if __name__ == "__main__":
    main()
