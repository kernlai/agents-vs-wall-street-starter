#!/usr/bin/env python3
"""
validate_panel.py -- independent audit of data/deere/panel_quarterly.csv.

Nothing here reuses build_panel.py's loaders: every check re-derives the value
from a source the panel builder did not use for that column, so a shared bug
cannot make a check pass.

  CHECK 1  structural integrity (shape, key uniqueness, forecast-row emptiness,
           no zeros standing in for missing data)
  CHECK 2  targets vs de_predictability.csv -- a DIFFERENT extraction agent's
           independent read of Deere revenue and diluted EPS
  CHECK 3  targets vs the LIVE SEC EDGAR XBRL companyconcept API (network)
  CHECK 4  de_ppa_operating_profit vs de_segments_legacy.csv's independently
           extracted restated PPA series, over the FY2020 overlap
  CHECK 5  panel de_ppa_net_sales + de_sat_net_sales + de_cf_net_sales against
           de_net_sales_equipment (the equipment-operations total)
  CHECK 6  peer alignment sanity -- every mapped peer print is within 46 days
           of the Deere quarter end it was assigned to
  CHECK 7  guidance point-in-time discipline: the vintage used in each row was
           issued strictly before that row's period_end

Usage: python3 validate_panel.py [--data DIR] [--offline]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.abspath(os.path.join(HERE, "..", "..", "data", "deere"))
UA = "AgentsVsWallStreet cor@salomo.io"

RESULTS = []


def record(name, checked, agree, detail=""):
    RESULTS.append((name, checked, agree, detail))
    status = "PASS" if checked and agree == checked else ("EMPTY" if not checked else "DIFFS")
    print("[%s] %-46s %3d/%-3d agree  %s" % (status, name, agree, checked, detail))


def rd(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(s):
    s = (s or "").strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def close(a, b, tol_abs, tol_rel):
    if a is None or b is None:
        return False
    return abs(a - b) <= max(tol_abs, tol_rel * max(abs(a), abs(b)))


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=DEFAULT_DATA)
    ap.add_argument("--offline", action="store_true", help="skip the live SEC check")
    args = ap.parse_args()
    D = args.data

    panel = rd(os.path.join(D, "panel_quarterly.csv"))
    by = {(int(r["fiscal_year"]), r["fiscal_quarter"]): r for r in panel}
    print("panel: %d rows x %d columns\n" % (len(panel), len(panel[0])))

    # ---------------- CHECK 1: structure --------------------------------
    problems = []
    if len(by) != len(panel):
        problems.append("duplicate (fiscal_year, fiscal_quarter) keys")
    last = panel[-1]
    if last["period_end"] != "2026-08-02" or last["fiscal_quarter"] != "Q3":
        problems.append("last row is not FY2026 Q3 / 2026-08-02")
    for t in ("de_net_sales_revenues_total", "de_eps_diluted_gaap", "de_ppa_operating_profit"):
        if last[t] != "":
            problems.append("forecast row target %s is populated" % t)
    # period_end must be strictly increasing
    pes = [dt.date.fromisoformat(r["period_end"]) for r in panel]
    if any(b <= a for a, b in zip(pes, pes[1:])):
        problems.append("period_end is not strictly increasing")
    # a literal 0 in a target or a price column would mean 'missing' encoded as zero
    zerocols = set()
    for r in panel:
        for c, v in r.items():
            if c.startswith(("px_", "de_net_sales", "de_eps", "de_ppa_net", "agco_", "cat_")) \
               and v.strip() == "0":
                zerocols.add(c)
    if zerocols:
        problems.append("zero used where missing is likely: %s" % sorted(zerocols))
    record("1 structural integrity", 1, 0 if problems else 1, "; ".join(problems) or "clean")

    # ---------------- CHECK 2: vs de_predictability.csv -----------------
    pred = {}
    for r in rd(os.path.join(D, "de_predictability.csv")):
        if r["series_id"] in ("de_eps_actual_usd", "de_revenue_actual_usdm"):
            k = (int(r["fiscal_year"]), "Q" + r["fiscal_quarter"])
            pred[(r["series_id"], k)] = num(r["value"])
    n = a = 0
    diffs = []
    for (sid, k), v in pred.items():
        col = "de_eps_diluted_gaap" if sid == "de_eps_actual_usd" else "de_net_sales_revenues_total"
        if k not in by:
            continue
        p = num(by[k][col])
        if p is None or v is None:
            continue
        n += 1
        # de_predictability carries sub-million precision; the panel is XBRL exact
        if close(p, v, 0.005 if "eps" in col else 1.0, 0.0011):
            a += 1
        else:
            diffs.append("%s %s%s panel=%s pred=%s" % (col, k[0], k[1], p, v))
    record("2 targets vs de_predictability.csv", n, a, diffs[0] if diffs else "independent agent")
    for x in diffs[:6]:
        print("       %s" % x)

    # ---------------- CHECK 3: live SEC EDGAR XBRL ----------------------
    if args.offline:
        record("3 targets vs live SEC EDGAR XBRL", 0, 0, "skipped (--offline)")
    else:
        try:
            base = "https://data.sec.gov/api/xbrl/companyconcept/CIK0000315189/us-gaap/%s.json"
            eps = fetch(base % "EarningsPerShareDiluted")
            rev = fetch(base % "Revenues")

            def quarterly(doc, unit):
                out = {}
                for f in doc["units"][unit]:
                    if not f.get("start") or not f.get("end"):
                        continue
                    s = dt.date.fromisoformat(f["start"])
                    e = dt.date.fromisoformat(f["end"])
                    if not (80 <= (e - s).days <= 100):
                        continue
                    out.setdefault(e, set()).add(f["val"])
                return out

            eq = quarterly(eps, "USD/shares")
            rq = quarterly(rev, "USD")
            n = a = 0
            diffs = []
            for r in panel:
                pe = dt.date.fromisoformat(r["period_end"])
                for col, src, scale, ta, tr in (
                        ("de_eps_diluted_gaap", eq, 1.0, 0.005, 0.0),
                        ("de_net_sales_revenues_total", rq, 1e-6, 1.0, 0.0)):
                    p = num(r[col])
                    if p is None:
                        continue
                    # SEC period ends can differ from the panel's canonical date
                    # by a day or two around the FY2016 calendar change
                    cand = [v for e, vs in src.items() if abs((e - pe).days) <= 3 for v in vs]
                    if not cand:
                        continue
                    n += 1
                    if any(close(p, v * scale, ta, tr) for v in cand):
                        a += 1
                    else:
                        diffs.append("%s %s%s panel=%s sec=%s"
                                     % (col, r["fiscal_year"], r["fiscal_quarter"], p,
                                        sorted(v * scale for v in cand)))
            record("3 targets vs live SEC EDGAR XBRL", n, a,
                   "companyconcept, CIK 315189")
            for x in diffs[:8]:
                print("       %s" % x)
        except Exception as exc:                      # noqa: BLE001
            record("3 targets vs live SEC EDGAR XBRL", 0, 0, "network error: %s" % exc)

    # ---------------- CHECK 4: PPA vs legacy-file restated PPA ----------
    leg = {}
    for r in rd(os.path.join(D, "de_segments_legacy.csv")):
        if r["series_id"] == "de_ppa_operating_profit_restated" and r["fiscal_quarter"] != "FY":
            leg[(int(r["fiscal_year"]), r["fiscal_quarter"])] = num(r["value"])
    n = a = 0
    diffs = []
    for k, v in leg.items():
        if k not in by:
            continue
        p = num(by[k]["de_ppa_operating_profit"])
        if p is None:
            continue
        n += 1
        if close(p, v, 0.5, 0.0):
            a += 1
        else:
            diffs.append("%s%s panel=%s legacy=%s" % (k[0], k[1], p, v))
    record("4 PPA op profit vs legacy-file restated", n, a, "; ".join(diffs) or "FY2020 overlap")

    # ---------------- CHECK 5: segment sales sum vs equipment sales -----
    n = a = 0
    worst = 0.0
    for r in panel:
        parts = [num(r["de_ppa_net_sales"]), num(r["de_sat_net_sales"]), num(r["de_cf_net_sales"])]
        tot = num(r["de_net_sales_equipment"])
        if tot is None or any(p is None for p in parts):
            continue
        n += 1
        gap = abs(sum(parts) - tot)
        worst = max(worst, gap)
        if gap <= max(3.0, 0.004 * tot):
            a += 1
    record("5 PPA+SAT+CF vs equipment net sales", n, a,
           "max residual %.0f USDm (Deere rounds each line independently)" % worst)

    # ---------------- CHECK 6: peer alignment distance ------------------
    cal = {(int(r["fiscal_year"]), r["fiscal_quarter"]): dt.date.fromisoformat(r["period_end"])
           for r in panel}
    peers = rd(os.path.join(D, "drv_peers.csv"))
    pv = {}
    for r in peers:
        if r["fiscal_quarter"] == "FY" or not r["period_end"]:
            continue
        pv.setdefault(r["series_id"], {})[dt.date.fromisoformat(r["period_end"])] = num(r["value"])
    n = a = 0
    far = []
    for col in ("agco_revenue", "cat_revenue", "cnh_revenue", "toro_revenue",
                "titn_revenue", "tsco_revenue", "lindsay_revenue", "valmont_revenue",
                "kubota_revenue"):
        src = pv.get(col, {})
        for r in panel:
            p = num(r[col])
            if p is None:
                continue
            k = (int(r["fiscal_year"]), r["fiscal_quarter"])
            hits = [e for e, v in src.items() if v is not None and abs(v - p) < 1e-6]
            if not hits:
                continue
            n += 1
            dist = min(abs((e - cal[k]).days) for e in hits)
            if dist <= 46:
                a += 1
            else:
                far.append("%s %s%s off by %dd" % (col, k[0], k[1], dist))
    record("6 peer alignment within 46 days", n, a, "; ".join(far[:3]) or "nearest-quarter-end rule")

    # ---------------- CHECK 7: guidance is point-in-time ----------------
    n = a = 0
    bad = []
    for r in panel:
        iss = r.get("de_guidance_vintage_issued", "").strip()
        if not iss:
            continue
        n += 1
        if dt.date.fromisoformat(iss) < dt.date.fromisoformat(r["period_end"]):
            a += 1
        else:
            bad.append("%s%s vintage %s >= period_end %s"
                       % (r["fiscal_year"], r["fiscal_quarter"], iss, r["period_end"]))
    record("7 guidance vintage precedes period_end", n, a, "; ".join(bad[:3]) or "no look-ahead")

    # forecast row must use the 2026-05-21 vintage -- the newest thing a
    # forecaster standing on 2026-08-16 actually has
    fr = panel[-1]
    ok = fr.get("de_guidance_vintage_issued") == "2026-05-21"
    record("7b forecast row uses 2026-05-21 vintage", 1, 1 if ok else 0,
           "got %r" % fr.get("de_guidance_vintage_issued"))

    print("")
    bad = [r for r in RESULTS if r[1] and r[2] != r[1]]
    print("SUMMARY: %d checks run, %d with disagreements" % (len(RESULTS), len(bad)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
