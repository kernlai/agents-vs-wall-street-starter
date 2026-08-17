#!/usr/bin/env python3
"""Diagnostic: which XBRL revenue tags are mutually consistent per company.

Reads cached SEC companyfacts JSON and, for every pair of candidate revenue
tags, prints overlapping periods and whether the values agree. Used to decide
the per-company tag priority list in build_peers.py.
"""
import json, os, sys
from collections import defaultdict
from datetime import date

CACHE = sys.argv[1] if len(sys.argv) > 1 else "facts"

TAGS = [
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "SalesRevenueNet",
    "SalesRevenueGoodsNet",
]

COMPANIES = {
    "0000315189": "DE", "0000880266": "AGCO", "0001567094": "CNH",
    "0000018230": "CAT", "0001409171": "TITN", "0000916365": "TSCO",
    "0000737758": "TTC", "0000836157": "LNN", "0000102729": "VMI",
}


def d(s):
    y, m, dd = s.split("-")
    return date(int(y), int(m), int(dd))


def collect(facts, tag, lo, hi):
    """Return {(start,end): [(filed, val)]} for durations in [lo,hi] days."""
    out = defaultdict(list)
    node = facts.get(tag)
    if not node:
        return out
    for unit, arr in node["units"].items():
        if unit != "USD":
            continue
        for f in arr:
            if "start" not in f:
                continue
            n = (d(f["end"]) - d(f["start"])).days + 1
            if lo <= n <= hi:
                out[(f["start"], f["end"])].append((f["filed"], f["val"], f.get("form", "")))
    return out


for cik, tic in COMPANIES.items():
    facts = json.load(open(os.path.join(CACHE, cik + ".json")))["facts"]["us-gaap"]
    print("=" * 70)
    print(tic, cik)
    per = {}
    for t in TAGS:
        q = collect(facts, t, 80, 100)
        a = collect(facts, t, 350, 380)
        per[t] = (q, a)
        if q or a:
            qe = sorted(k[1] for k in q)
            ae = sorted(k[1] for k in a)
            print(f"  {t:60s} Q:{len(q):3d} {qe[0] if qe else '-'}..{qe[-1] if qe else '-'}"
                  f"  A:{len(a):3d} {ae[0] if ae else '-'}..{ae[-1] if ae else '-'}")
    # pairwise overlap agreement on quarterly periods
    ts = [t for t in TAGS if per[t][0]]
    for i in range(len(ts)):
        for j in range(i + 1, len(ts)):
            a, b = per[ts[i]][0], per[ts[j]][0]
            common = set(a) & set(b)
            if not common:
                continue
            agree = dis = 0
            ex = None
            for k in sorted(common):
                va = min(a[k])[1]
                vb = min(b[k])[1]
                if va == 0 or abs(va - vb) / max(abs(va), 1) < 0.005:
                    agree += 1
                else:
                    dis += 1
                    if ex is None:
                        ex = (k, va, vb)
            print(f"    overlap {ts[i][:34]:34s} vs {ts[j][:34]:34s} n={len(common):3d} agree={agree} disagree={dis} ex={ex}")
