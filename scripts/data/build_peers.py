#!/usr/bin/env python3
"""Build a tidy long peer-financials panel for Deere (DE) read-across.

Source: SEC EDGAR XBRL companyfacts API (keyless; descriptive User-Agent required).
Output: tidy long CSV
    series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes

Design decisions (all deliberate -- see drv_peers.md)
----------------------------------------------------
1. Per-company revenue tag priority is HARD-CODED, chosen by peer_diagnose.py,
   which compares every candidate tag on overlapping periods. For CAT/DE/CNH
   `Revenues` is total sales AND revenues (includes captive finance) whereas
   `SalesRevenueNet` / `RevenueFromContractWithCustomer*` is an equipment-only
   subtotal -- naively chaining them by "first tag that exists" fabricates a
   step change of 5-10% right at the 2018 ASC 606 boundary.
2. Values are AS FIRST REPORTED (earliest `filed` for the period) to avoid
   look-ahead bias. If a later filing restates the period by >0.5% the restated
   value and its filing date go into `notes`.
3. Facts are keyed by PERIOD END, not (start,end): issuers drift their period
   start by a day or two between the 10-Q and the later 10-K, which would
   otherwise emit the same quarter twice.
4. Bad-tag guard: a "quarterly" fact whose value equals the fiscal-year total
   for a period ending on the fiscal-year end is a known issuer tagging error
   (Tractor Supply FY2020, tagged in the FY2022 10-K and even framed CY2020Q4).
   Such facts are dropped and Q4 is derived instead.
5. Q4 is derived (FY minus Q1+Q2+Q3) wherever the issuer tags no usable
   standalone Q4 duration. Those rows carry source_type=inference.
6. Peers run DIFFERENT fiscal calendars. period_end is always each company's own
   true period end. A calendar-quarter alignment key is computed from the period
   MIDPOINT, used ONLY for the correlation study, never to relabel data.

Usage:
    python3 build_peers.py --cache facts --out .../drv_peers.csv --panel panel.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import date, timedelta

UA = "AgentsVsWallStreet cor@salomo.io"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

# key -> (cik10, display name, revenue tag priority, fiscal calendar description)
COMPANIES = {
    "de": ("0000315189", "Deere & Company",
           ["Revenues"], "FY ends late Oct / early Nov (52/53-week)"),
    "agco": ("0000880266", "AGCO Corporation",
             ["RevenueFromContractWithCustomerExcludingAssessedTax",
              "RevenueFromContractWithCustomerIncludingAssessedTax",
              "SalesRevenueGoodsNet"], "FY ends 31 Dec (calendar)"),
    "cnh": ("0001567094", "CNH Industrial N.V.",
            ["Revenues"], "FY ends 31 Dec (calendar)"),
    "cat": ("0000018230", "Caterpillar Inc.",
            ["Revenues"], "FY ends 31 Dec (calendar)"),
    "titn": ("0001409171", "Titan Machinery Inc.",
             ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"],
             "FY ends 31 Jan (fiscal year named for the calendar year of its END)"),
    "tsco": ("0000916365", "Tractor Supply Company",
             ["Revenues", "SalesRevenueGoodsNet"],
             "52/53-week FY ending last Saturday of December"),
    "toro": ("0000737758", "The Toro Company",
             ["RevenueFromContractWithCustomerExcludingAssessedTax",
              "Revenues", "SalesRevenueNet"], "FY ends 31 Oct"),
    "lindsay": ("0000836157", "Lindsay Corporation",
                ["Revenues"], "FY ends 31 Aug"),
    "valmont": ("0000102729", "Valmont Industries, Inc.",
                ["RevenueFromContractWithCustomerExcludingAssessedTax",
                 "SalesRevenueNet"],
                "52/53-week FY ending last Saturday of December"),
}

EXCLUDED = {
    "de": "excluded tags SalesRevenueGoodsNet/SalesRevenueNet = equipment net sales "
          "only (no financial services); Revenues = total net sales and revenues",
    "cat": "excluded tag SalesRevenueNet = Machinery/E&T sales only; Revenues = "
           "total sales and revenues incl. Financial Products",
    "cnh": "excluded tags RevenueFromContractWithCustomer* = net sales of goods only; "
           "Revenues = total revenues incl. Financial Services",
    "lindsay": "excluded tag RevenueFromContractWithCustomer* omits non-contract "
               "revenue; Revenues = total revenues as presented",
    "valmont": "excluded tags `Revenues` (2010-2013 only) and SalesRevenueGoodsNet "
               "are narrower than headline Net sales; SalesRevenueNet used pre-2018",
}

EPS_TAG = "EarningsPerShareDiluted"
OPINC_TAG = "OperatingIncomeLoss"
Q_LO, Q_HI = 80, 100
A_LO, A_HI = 350, 380


def dt(s):
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


def fetch_facts(cik, cache):
    path = os.path.join(cache, cik + ".json")
    if not os.path.exists(path) or os.path.getsize(path) < 1000:
        os.makedirs(cache, exist_ok=True)
        req = urllib.request.Request(FACTS_URL.format(cik=cik), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
            f.write(r.read())
    return json.load(open(path))


def by_end(facts, tag, unit, lo, hi):
    """{end_str: [(filed, val, form, start)]} sorted by filed, for durations in band."""
    out = defaultdict(list)
    node = facts.get(tag)
    if not node:
        return out
    for u, arr in node["units"].items():
        if u != unit:
            continue
        for f in arr:
            if "start" not in f:
                continue
            n = (dt(f["end"]) - dt(f["start"])).days + 1
            if lo <= n <= hi:
                out[f["end"]].append((f["filed"], f["val"], f.get("form", ""), f["start"]))
    for k in out:
        out[k].sort()
    return out


def chain(facts, tags, unit, lo, hi, rel_tol=0.005):
    """Merge tags by priority -> {end: dict(val, filed, form, tag, start, note)}."""
    merged = {}
    for tag in tags:
        for end, entries in by_end(facts, tag, unit, lo, hi).items():
            if end in merged:
                continue
            filed0, val0, form0, start0 = entries[0]
            denom = max(abs(val0), 1e-9)
            later = [(f, v, fm) for f, v, fm, _ in entries[1:]
                     if abs(v - val0) / denom > rel_tol]
            note = ""
            if later:
                f, v, fm = later[-1]
                note = ("restated: first reported %g in %s filed %s; latest filing "
                        "%s %s reports %g" % (val0, form0, filed0, fm, f, v))
            merged[end] = dict(val=val0, filed=filed0, form=form0, tag=tag,
                               start=start0, note=note)
    return merged


def drop_bad_quarters(q, a, rel_tol=1e-6):
    """Remove 'quarterly' facts that are actually the FY total mis-tagged."""
    dropped = []
    for end in list(q):
        if end in a and abs(q[end]["val"] - a[end]["val"]) <= rel_tol * max(abs(a[end]["val"]), 1):
            dropped.append(end)
            del q[end]
    return dropped


def build_fy_ends(annual_ends, quarterly_ends):
    ends = sorted({dt(e) for e in annual_ends})
    if not ends:
        return []
    qe = sorted({dt(e) for e in quarterly_ends})
    if qe:
        while ends[0] > qe[0]:
            ends.insert(0, ends[0] - timedelta(days=364))
        while ends[-1] < qe[-1]:
            ends.append(ends[-1] + timedelta(days=364))
    ends.append(ends[-1] + timedelta(days=364))
    return ends


def fy_of(end, fy_ends):
    for i, fe in enumerate(fy_ends):
        if fe >= end - timedelta(days=5):
            return i, fe
    return None, None


def fiscal_label(end, fy_ends):
    i, fe = fy_of(end, fy_ends)
    if i is None:
        return None, None
    fy_start = (fy_ends[i - 1] + timedelta(days=1)) if i > 0 else fe - timedelta(days=363)
    q = int(round(((end - fy_start).days + 1) / 91.3125))
    return fe.year, "Q%d" % max(1, min(4, q))


def cal_quarter(start, end):
    mid = start + (end - start) // 2
    return mid.year, (mid.month - 1) // 3 + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="facts")
    ap.add_argument("--out", required=True)
    ap.add_argument("--panel", default=None)
    args = ap.parse_args()

    rows, panel = [], {}

    for key, (cik, name, rev_tags, fycal) in COMPANIES.items():
        facts = fetch_facts(cik, args.cache)["facts"]["us-gaap"]
        src = FACTS_URL.format(cik=cik)

        rev_q = chain(facts, rev_tags, "USD", Q_LO, Q_HI)
        rev_a = chain(facts, rev_tags, "USD", A_LO, A_HI)
        eps_q = chain(facts, [EPS_TAG], "USD/shares", Q_LO, Q_HI)
        eps_a = chain(facts, [EPS_TAG], "USD/shares", A_LO, A_HI)
        op_q = chain(facts, [OPINC_TAG], "USD", Q_LO, Q_HI)
        op_a = chain(facts, [OPINC_TAG], "USD", A_LO, A_HI)

        bad = {"revenue": drop_bad_quarters(rev_q, rev_a),
               "eps": drop_bad_quarters(eps_q, eps_a),
               "opinc": drop_bad_quarters(op_q, op_a)}
        for what, ends in bad.items():
            for e in ends:
                print("  [%s] dropped mis-tagged quarterly %s at %s (equals FY total)"
                      % (key, what, e), file=sys.stderr)

        fy_ends = build_fy_ends(list(rev_a) + list(eps_a),
                                list(rev_q) + list(eps_q))
        if not fy_ends:
            print("!! no annual anchor for", key, file=sys.stderr)
            continue

        calnote = "fiscal calendar: %s" % fycal
        exnote = EXCLUDED.get(key)

        def emit(store, sid, units, scale, freq):
            for end in sorted(store):
                rec = store[end]
                ed = dt(end)
                if freq == "FY":
                    _, fe = fy_of(ed, fy_ends)
                    if fe is None:
                        continue
                    fy, fq = fe.year, "FY"
                else:
                    fy, fq = fiscal_label(ed, fy_ends)
                    if fy is None:
                        continue
                notes = [calnote, "xbrl tag=%s" % rec["tag"],
                         "period %s..%s" % (rec["start"], end),
                         "as-first-reported in %s filed %s" % (rec["form"], rec["filed"])]
                if exnote:
                    notes.append(exnote)
                if rec["note"]:
                    notes.append(rec["note"])
                if rec["val"] == 0:
                    notes.append("ZERO IS REAL, NOT MISSING: the issuer tagged exactly 0 "
                                 "for this period (a rounded-to-zero breakeven quarter). "
                                 "Do not treat as a gap")
                rows.append([sid, end, fy, fq, round(rec["val"] * scale, 6), units,
                             "api", src, "; ".join(notes)])

        emit(rev_q, "%s_revenue" % key, "USDm", 1e-6, "Q")
        emit(rev_a, "%s_revenue" % key, "USDm", 1e-6, "FY")
        emit(eps_q, "%s_eps_diluted" % key, "USD/share", 1.0, "Q")
        emit(eps_a, "%s_eps_diluted" % key, "USD/share", 1.0, "FY")

        def derive_q4(store_q, store_a, sid, units, scale, eps=False):
            byfy = defaultdict(dict)
            for end, rec in store_q.items():
                fy, fq = fiscal_label(dt(end), fy_ends)
                if fy:
                    byfy[fy][fq] = (end, rec["val"], rec["start"])
            for end, rec in sorted(store_a.items()):
                ed = dt(end)
                _, fe = fy_of(ed, fy_ends)
                if fe is None:
                    continue
                fy = fe.year
                got = byfy.get(fy, {})
                if "Q4" in got or not all(q in got for q in ("Q1", "Q2", "Q3")):
                    continue
                q4 = rec["val"] - sum(got[q][1] for q in ("Q1", "Q2", "Q3"))
                extra = ("; EPS subtraction is APPROXIMATE: the diluted share count "
                         "differs quarter to quarter, so FY EPS is not exactly the "
                         "sum of quarterly EPS" if eps else "")
                rows.append([sid, end, fy, "Q4", round(q4 * scale, 6), units,
                             "inference", src,
                             "%s; DERIVED Q4 = FY total minus reported Q1+Q2+Q3 "
                             "(issuer tags no usable standalone Q4 duration in XBRL)%s"
                             % (calnote, extra)])
                byfy[fy]["Q4"] = (end, q4, None)
            return byfy

        rev_byfy = derive_q4(rev_q, rev_a, "%s_revenue" % key, "USDm", 1e-6)
        derive_q4(eps_q, eps_a, "%s_eps_diluted" % key, "USD/share", 1.0, eps=True)

        for store_op, store_rev, freq in ((op_q, rev_q, "Q"), (op_a, rev_a, "FY")):
            for end in sorted(store_op):
                if end not in store_rev:
                    continue
                rv = store_rev[end]["val"]
                if not rv:
                    continue
                ed = dt(end)
                if freq == "FY":
                    _, fe = fy_of(ed, fy_ends)
                    if fe is None:
                        continue
                    fy, fq = fe.year, "FY"
                else:
                    fy, fq = fiscal_label(ed, fy_ends)
                    if fy is None:
                        continue
                rows.append(["%s_operating_margin" % key, end, fy, fq,
                             round(100.0 * store_op[end]["val"] / rv, 4), "percent",
                             "api", src,
                             "%s; = us-gaap:OperatingIncomeLoss / revenue (tag %s), same "
                             "period, both as-first-reported; NOTE issuer definitions of "
                             "'operating income' are NOT uniform across these companies -- "
                             "compare levels with care, changes are safer"
                             % (calnote, store_rev[end]["tag"])])

        pk = {}
        for end, rec in rev_q.items():
            pk[cal_quarter(dt(rec["start"]), dt(end))] = rec["val"] * 1e-6
        for fy, qs in rev_byfy.items():
            if "Q4" in qs and qs["Q4"][2] is None:
                end, v, _ = qs["Q4"]
                ed = dt(end)
                pk.setdefault(cal_quarter(ed - timedelta(days=90), ed), v * 1e-6)
        panel[key] = {"%d-Q%d" % k: round(v, 3) for k, v in sorted(pk.items())}

    rows.sort(key=lambda r: (r[0], r[1], r[3]))
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        f.write("series_id,period_end,fiscal_year,fiscal_quarter,value,units,"
                "source_type,source,notes\n")
        for r in rows:
            cells = []
            for c in r:
                c = "" if c is None else str(c)
                if any(ch in c for ch in ',"\n'):
                    c = '"' + c.replace('"', '""') + '"'
                cells.append(c)
            f.write(",".join(cells) + "\n")
    print("wrote %d rows -> %s" % (len(rows), args.out))
    if args.panel:
        json.dump(panel, open(args.panel, "w"), indent=1)
        print("wrote panel -> %s" % args.panel)


if __name__ == "__main__":
    main()
