#!/usr/bin/env python3
"""
de_segments_legacy_build.py
===========================
Combine the corpus extraction (de_segments_legacy_extract.py) with the EDGAR
supplement (de_segments_edgar_supplement.py), compute the legacy -> modern segment
BRIDGE, run an independent XBRL cross-check, and emit the tidy long CSV.

Output CSV header (fixed by the task spec):
  series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes

Because the header is fixed at nine columns, the two mandatory segment attributes are
carried in `notes` as machine-readable key=value pairs, always first and always in this
order:
    segment_basis=legacy-AT|modern-PPA; as_reported_or_restated=<flag>; ...
and they are also encoded in the series_id suffix.

Usage:
    python3 de_segments_legacy_extract.py      # writes /tmp/de_seg_raw.json
    python3 de_segments_edgar_supplement.py    # writes /tmp/de_seg_edgar.json
    python3 de_segments_legacy_build.py
"""

import csv
import json
import os
import re
import statistics
import sys
import urllib.request
from collections import defaultdict

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
OUTDIR = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere"
OUT_CSV = os.path.join(OUTDIR, "de_segments_legacy.csv")
UA = "AgentsVsWallStreet cor@salomo.io"

HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "value",
          "units", "source_type", "source", "notes"]

# Deere used fixed calendar month-ends before the 52/53-week fiscal year was adopted;
# these fill in the pre-FY2014 periods that the corpus does not cover.
LEGACY_CAL = {}
for _y in (2011, 2012, 2013):
    LEGACY_CAL[(_y, "Q1")] = "%d-01-31" % _y
    LEGACY_CAL[(_y, "Q2")] = "%d-04-30" % _y
    LEGACY_CAL[(_y, "Q3")] = "%d-07-31" % _y
    LEGACY_CAL[(_y, "Q4")] = "%d-10-31" % _y
    LEGACY_CAL[(_y, "FY")] = "%d-10-31" % _y

SERIES = {
    ("AT", "sales"): "de_at_net_sales_legacy",
    ("AT", "op"): "de_at_operating_profit_legacy",
    ("CF", "sales"): "de_cf_net_sales_legacy",
    ("CF", "op"): "de_cf_operating_profit_legacy",
}
SERIES_MODERN = {
    ("PPA", "sales"): "de_ppa_net_sales_restated",
    ("PPA", "op"): "de_ppa_operating_profit_restated",
    ("SAT", "sales"): "de_sat_net_sales_restated",
    ("SAT", "op"): "de_sat_operating_profit_restated",
    ("CF", "sales"): "de_cf_net_sales_restated",
    ("CF", "op"): "de_cf_operating_profit_restated",
}

QORDER = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4, "FY": 5}


def load():
    raw = json.load(open("/tmp/de_seg_raw.json"))
    edgar = json.load(open("/tmp/de_seg_edgar.json"))
    return raw, edgar


def build_calendar(raw, edgar):
    cal = {}
    for k, v in raw["cal"].items():
        fy, fq = k.split("|")
        cal[(int(fy), fq)] = v
    for k, v in LEGACY_CAL.items():
        cal.setdefault(k, v)
    # every FY row sits on its Q4 date
    for (fy, fq), v in list(cal.items()):
        if fq == "Q4":
            cal.setdefault((fy, "FY"), v)
    return cal


def merge(raw, edgar):
    """Merge corpus primaries with EDGAR observations. Report agreement / conflict."""
    prim = {}
    for k, v in raw["primary"].items():
        seg, metric, fy, fq, basis = k.split("|")
        prim[(seg, metric, int(fy), fq, basis)] = dict(
            value=v["value"], flag=v["flag"], source=v["source"], stype="filing",
            origin="corpus")

    xcheck_hits, xcheck_conflicts, added = [], [], 0
    for o in edgar:
        key = (o["seg"], o["metric"], o["fy"], o["fq"], o["basis"])
        if key in prim:
            if abs(prim[key]["value"] - o["value"]) < 0.5:
                xcheck_hits.append((key, o["value"], o["source"]))
            else:
                xcheck_conflicts.append((key, prim[key]["value"], o["value"], o["source"]))
        else:
            if o["role"] == "current":
                flag = "as_reported"
            else:
                flag = "as_reported_comparative"
            cur = prim.get(key)
            if cur is None:
                prim[key] = dict(value=o["value"], flag=flag, source=o["source"],
                                 stype="filing", origin="edgar")
                added += 1
            elif cur["origin"] == "edgar" and cur["flag"] == "as_reported_comparative" \
                    and flag == "as_reported":
                prim[key] = dict(value=o["value"], flag=flag, source=o["source"],
                                 stype="filing", origin="edgar")
    return prim, xcheck_hits, xcheck_conflicts, added


# ------------------------------------------------------------------ XBRL cross-check

def xbrl_revenues():
    url = ("https://data.sec.gov/api/xbrl/companyconcept/CIK0000315189/"
           "us-gaap/Revenues.json")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode())
    out = {}
    for f in d["units"]["USD"]:
        if "start" not in f or "end" not in f:
            continue
        out.setdefault((f["start"], f["end"]), set()).add(f["val"])
    return out


TOTAL_RE = re.compile(r"^\|\s*Total net sales and revenues", re.M)


def corpus_total_revenues():
    """Re-read 'Total net sales and revenues' from the legacy-era 8-K press releases,
    independently of the segment extraction, for the XBRL cross-check."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import de_segments_legacy_extract as ex
    out = {}
    for pub, qtag, form, path, fname in ex.inventory():
        if form != "8k":
            continue
        text = open(path, encoding="utf-8").read()
        parsed = ex.parse_segment_table(text)
        if not parsed:
            continue
        seg, tot = parsed
        if "rev_total" not in tot:
            continue
        cur_end, prior_end = ex.period_ends(text)
        if not cur_end:
            continue
        out[cur_end] = (tot["rev_total"][0], os.path.relpath(path, CORPUS))
    return out


def prev_quarter_start(end_iso, all_ends):
    """The XBRL quarterly fact for a period ending `end_iso` starts the day after the
    previous quarter end."""
    import datetime
    ends = sorted(all_ends)
    i = ends.index(end_iso)
    if i == 0:
        return None
    prev = datetime.date(*[int(x) for x in ends[i - 1].split("-")])
    return (prev + datetime.timedelta(days=1)).isoformat()


# ------------------------------------------------------------------ main

def main():
    raw, edgar = load()
    cal = build_calendar(raw, edgar)
    prim, hits, conflicts, added = merge(raw, edgar)

    print("=" * 78)
    print("MERGE")
    print("  corpus primary points        :", len(raw["primary"]))
    print("  EDGAR observations           :", len(edgar))
    print("  EDGAR values matching corpus :", len(hits))
    print("  EDGAR/corpus CONFLICTS       :", len(conflicts))
    for c in conflicts:
        print("     !!", c)
    print("  new points added from EDGAR  :", added)

    # ---------------- bridge ----------------
    bridge = []
    for (fy, fq) in sorted({(k[2], k[3]) for k in prim}, key=lambda x: (x[0], QORDER[x[1]])):
        legacy_s = prim.get(("AT", "sales", fy, fq, "legacy-AT"))
        legacy_o = prim.get(("AT", "op", fy, fq, "legacy-AT"))
        ppa_s = prim.get(("PPA", "sales", fy, fq, "modern-PPA"))
        sat_s = prim.get(("SAT", "sales", fy, fq, "modern-PPA"))
        ppa_o = prim.get(("PPA", "op", fy, fq, "modern-PPA"))
        sat_o = prim.get(("SAT", "op", fy, fq, "modern-PPA"))
        if not (legacy_s and ppa_s and sat_s and legacy_o and ppa_o and sat_o):
            continue
        rec_s = ppa_s["value"] + sat_s["value"] - legacy_s["value"]
        rec_o = ppa_o["value"] + sat_o["value"] - legacy_o["value"]
        bridge.append(dict(fy=fy, fq=fq, period_end=cal[(fy, fq)],
                           at_sales=legacy_s["value"], ppa_sales=ppa_s["value"],
                           sat_sales=sat_s["value"], recon_sales=rec_s,
                           at_op=legacy_o["value"], ppa_op=ppa_o["value"],
                           sat_op=sat_o["value"], recon_op=rec_o,
                           share_sales=ppa_s["value"] / legacy_s["value"],
                           share_op=ppa_o["value"] / legacy_o["value"],
                           src_legacy=legacy_s["source"], src_modern=ppa_s["source"]))

    print("\n" + "=" * 78)
    print("BRIDGE: periods disclosed on BOTH bases")
    print("%-9s %-11s %9s %9s %9s %8s | %8s %8s %8s %7s | %7s %7s" %
          ("period", "period_end", "A&T sls", "PPA sls", "SAT sls", "recon",
           "A&T op", "PPA op", "SAT op", "recon", "s_share", "o_share"))
    for b in bridge:
        print("%-9s %-11s %9.0f %9.0f %9.0f %8.0f | %8.0f %8.0f %8.0f %7.0f | %7.4f %7.4f" %
              ("%dFY%s" % (b["fy"], b["fq"]) if b["fq"] == "FY" else "%d%s" % (b["fy"], b["fq"]),
               b["period_end"], b["at_sales"], b["ppa_sales"], b["sat_sales"], b["recon_sales"],
               b["at_op"], b["ppa_op"], b["sat_op"], b["recon_op"],
               b["share_sales"], b["share_op"]))

    q = [b for b in bridge if b["fq"] != "FY"]
    a = [b for b in bridge if b["fq"] == "FY"]
    for name, grp in (("quarterly", q), ("annual", a)):
        if len(grp) < 2:
            continue
        ss = [b["share_sales"] for b in grp]
        so = [b["share_op"] for b in grp]
        print("\n  %s PPA share of A&T net sales      n=%d mean=%.4f sd=%.4f min=%.4f max=%.4f cv=%.1f%%"
              % (name, len(ss), statistics.mean(ss), statistics.stdev(ss), min(ss), max(ss),
                 100 * statistics.stdev(ss) / statistics.mean(ss)))
        print("  %s PPA share of A&T operating profit n=%d mean=%.4f sd=%.4f min=%.4f max=%.4f cv=%.1f%%"
              % (name, len(so), statistics.mean(so), statistics.stdev(so), min(so), max(so),
                 100 * statistics.stdev(so) / statistics.mean(so)))

    # ---------------- forward stability: PPA share within ag&turf, FY2021+ ----------
    forward = []
    for (fy, fq) in sorted({(k[2], k[3]) for k in prim if k[4] == "modern-PPA"},
                           key=lambda x: (x[0], QORDER[x[1]])):
        if fy < 2021:
            continue
        ps = prim.get(("PPA", "sales", fy, fq, "modern-PPA"))
        ss = prim.get(("SAT", "sales", fy, fq, "modern-PPA"))
        po = prim.get(("PPA", "op", fy, fq, "modern-PPA"))
        so = prim.get(("SAT", "op", fy, fq, "modern-PPA"))
        if not (ps and ss and po and so):
            continue
        denom_o = po["value"] + so["value"]
        forward.append(dict(fy=fy, fq=fq, period_end=cal.get((fy, fq)),
                            share_sales=ps["value"] / (ps["value"] + ss["value"]),
                            share_op=(po["value"] / denom_o) if denom_o else None,
                            src=ps["source"]))
    print("\n" + "=" * 78)
    print("FORWARD STABILITY: PPA share of (PPA+SAT), FY2021 onward -- the ratio a")
    print("back-cast would have to assume is constant")
    for f in forward:
        print("  %d%-3s %-11s sales %.4f   op %s" %
              (f["fy"], f["fq"], f["period_end"], f["share_sales"],
               ("%.4f" % f["share_op"]) if f["share_op"] is not None else "n/a"))
    # is the ratio cyclical? correlate it with the level of ag&turf sales
    lvl, shr, shro = [], [], []
    for (fy, fq) in sorted({(k[2], k[3]) for k in prim if k[4] == "modern-PPA"},
                           key=lambda x: (x[0], QORDER[x[1]])):
        if fy < 2021 or fq == "FY":
            continue
        ps = prim.get(("PPA", "sales", fy, fq, "modern-PPA"))
        ss = prim.get(("SAT", "sales", fy, fq, "modern-PPA"))
        po = prim.get(("PPA", "op", fy, fq, "modern-PPA"))
        so = prim.get(("SAT", "op", fy, fq, "modern-PPA"))
        if not (ps and ss and po and so):
            continue
        lvl.append(ps["value"] + ss["value"])
        shr.append(ps["value"] / (ps["value"] + ss["value"]))
        shro.append(po["value"] / (po["value"] + so["value"]))
    if len(lvl) > 3:
        print("\n  correlation(PPA sales share, A&T sales level) FY2021+ quarters r=%.3f n=%d"
              % (statistics.correlation(shr, lvl), len(lvl)))
        print("  correlation(PPA op share,    A&T sales level) FY2021+ quarters r=%.3f n=%d"
              % (statistics.correlation(shro, lvl), len(lvl)))

    fq_ = [f for f in forward if f["fq"] != "FY"]
    if fq_:
        ss = [f["share_sales"] for f in fq_]
        so = [f["share_op"] for f in fq_ if f["share_op"] is not None]
        print("\n  FY2021+ quarterly sales share  n=%d mean=%.4f sd=%.4f min=%.4f max=%.4f"
              % (len(ss), statistics.mean(ss), statistics.stdev(ss), min(ss), max(ss)))
        print("  FY2021+ quarterly op share     n=%d mean=%.4f sd=%.4f min=%.4f max=%.4f"
              % (len(so), statistics.mean(so), statistics.stdev(so), min(so), max(so)))

    # ---------------- out-of-sample back-cast test ----------------
    # Apply the ratio measured on the FY2019/FY2020 overlap window to FY2021+ periods,
    # where the true PPA split is observed. This is the honest test of whether a
    # back-cast of PPA off the long A&T history would have worked.
    print("\n" + "=" * 78)
    print("OUT-OF-SAMPLE BACK-CAST TEST: FY2019/FY2020 ratio applied to FY2021+ actuals")
    if q and a:
        rs = statistics.mean(b["share_sales"] for b in q)
        ro = statistics.mean(b["share_op"] for b in q)
        rs_a = statistics.mean(b["share_sales"] for b in a)
        ro_a = statistics.mean(b["share_op"] for b in a)
        for freq, ratio_s, ratio_o, want_fy in (("quarterly", rs, ro, False),
                                                ("annual", rs_a, ro_a, True)):
            es, eo = [], []
            for (fy, fq) in sorted({(k[2], k[3]) for k in prim if k[4] == "modern-PPA"},
                                   key=lambda x: (x[0], QORDER[x[1]])):
                if fy < 2021 or ((fq == "FY") != want_fy):
                    continue
                ps = prim.get(("PPA", "sales", fy, fq, "modern-PPA"))
                ss = prim.get(("SAT", "sales", fy, fq, "modern-PPA"))
                po = prim.get(("PPA", "op", fy, fq, "modern-PPA"))
                so = prim.get(("SAT", "op", fy, fq, "modern-PPA"))
                if not (ps and ss and po and so) or po["value"] == 0:
                    continue
                es.append((ratio_s * (ps["value"] + ss["value"]) - ps["value"]) / ps["value"])
                eo.append((ratio_o * (po["value"] + so["value"]) - po["value"]) / po["value"])
            if not es:
                continue
            print("  %-9s net sales   ratio=%.4f n=%2d mean err %+.1f%%  MAPE %.1f%%  worst %.1f%%"
                  % (freq, ratio_s, len(es), 100 * statistics.mean(es),
                     100 * statistics.mean(abs(e) for e in es),
                     100 * max(abs(e) for e in es)))
            print("  %-9s op profit   ratio=%.4f n=%2d mean err %+.1f%%  MAPE %.1f%%  worst %.1f%%"
                  % (freq, ratio_o, len(eo), 100 * statistics.mean(eo),
                     100 * statistics.mean(abs(e) for e in eo),
                     100 * max(abs(e) for e in eo)))

    # ---------------- XBRL cross-check ----------------
    print("\n" + "=" * 78)
    print("INDEPENDENT CROSS-CHECK: corpus press-release 'Total net sales and revenues'")
    print("vs SEC EDGAR XBRL us-gaap:Revenues (companyconcept API)")
    xb = xbrl_revenues()
    corp = corpus_total_revenues()
    ends = sorted(corp)
    checked = ok = 0
    xrows = []
    for e in ends:
        start = prev_quarter_start(e, ends)
        if start is None:
            continue
        cand = xb.get((start, e))
        if not cand:
            continue
        val_m = corp[e][0]
        best = min(cand, key=lambda v: abs(v / 1e6 - val_m))
        diff = best / 1e6 - val_m
        checked += 1
        good = abs(diff) < 1.0
        ok += good
        xrows.append((e, val_m, best / 1e6, diff, good))
    for r in xrows:
        print("   %s  press release %9.1f   XBRL %9.1f   diff %+6.1f  %s"
              % (r[0], r[1], r[2], r[3], "OK" if r[4] else "MISMATCH"))
    print("   -> %d/%d quarters agree to within USD 1m" % (ok, checked))

    # ---------------- CSV ----------------
    rows = []

    def add(series_id, fy, fq, value, units, stype, source, notes):
        pend = cal.get((fy, fq))
        if pend is None:
            return
        rows.append([series_id, pend, fy, fq,
                     ("%g" % value) if value is not None else "",
                     units, stype, source, notes])

    basis_note = "segment_basis=%s; as_reported_or_restated=%s; "

    for (seg, metric, fy, fq, basis), v in sorted(
            prim.items(), key=lambda kv: (kv[0][4], kv[0][0], kv[0][1], kv[0][2], QORDER[kv[0][3]])):
        if basis == "legacy-AT":
            sid = SERIES.get((seg, metric))
            if not sid:
                continue
            n = basis_note % (basis, v["flag"])
            n += ("pre-FY2021 Agriculture & Turf reporting basis; "
                  "A&T was split into Production & Precision Ag and Small Ag & Turf in FY2021. ")
            if metric == "op":
                if fy <= 2016:
                    n += ("operating profit on the pre-ASU-2017-07 definition (full pension/OPEB "
                          "cost inside operating profit); not comparable with FY2018+ without the "
                          "restated series. ")
                elif fy == 2017:
                    n += ("as originally reported; Deere later restated FY2017 operating profit "
                          "upward on adoption of ASU 2017-07 - see de_*_operating_profit_legacy_asu201707. ")
                else:
                    n += "operating profit on the post-ASU-2017-07 definition (service cost only). "
            if fy == 2019 and fq in ("Q4", "FY"):
                n += "FY2019 was a 53-week year; Q4 FY2019 contained 14 weeks. "
            if fy <= 2016:
                n += ("period_end is the calendar month-end label used in the filing itself; "
                      "Deere's FY2017 10-K later restated the fiscal-year ends onto a 52/53-week "
                      "basis (FY2016 ended 2016-10-30, FY2015 ended 2015-11-01) but never "
                      "republished 52/53-week quarter ends for those years. ")
            if seg == "CF" and fy >= 2018:
                n += ("construction & forestry includes Wirtgen from 2017-12-01 (acquired, "
                      "consolidated with a one-month reporting lag until FY2021 Q1). ")
            if v["flag"] == "as_reported_comparative":
                n += "taken from the prior-year comparative column of a later filing. "
            add(sid, fy, fq, v["value"], "USDm", "filing", v["source"], n.strip())
        else:
            if fy > 2020:
                continue          # modern-era series belong to the modern-basis task
            sid = SERIES_MODERN.get((seg, metric))
            if not sid:
                continue
            n = basis_note % (basis, "restated")
            n += ("prior-year comparative recast by Deere onto the FY2021 four-segment basis; "
                  "this is the restated view of a pre-reorganisation period and is the only "
                  "PPA/SAT data that exists before FY2021. ")
            add(sid, fy, fq, v["value"], "USDm", "filing", v["source"], n.strip())

    # ASU 2017-07 restated legacy operating profit, kept as its own series so that
    # (series_id, period_end) stays unique
    for k, orig, new, srcs, pub in raw["restatements"]:
        seg, metric, fy, fq, basis = k
        if metric != "op" or basis != "legacy-AT":
            continue
        sid = {"AT": "de_at_operating_profit_legacy_asu201707",
               "CF": "de_cf_operating_profit_legacy_asu201707"}[seg]
        n = (basis_note % (basis, "restated"))
        n += ("restated on adoption of ASU 2017-07 (only the service-cost component of "
              "pension/OPEB stays in operating profit); originally reported %g, restated to %g "
              "in filings published %s. Use this series, not the as-reported one, when "
              "comparing FY2016-FY2017 operating profit with FY2018 onward." % (orig, new, pub))
        add(sid, fy, fq, new, "USDm", "filing", "; ".join(srcs), n)

    # bridge ratio series
    for b in bridge:
        n = ("segment_basis=bridge; as_reported_or_restated=derived; "
             "PPA net sales / legacy Agriculture & Turf net sales for a period Deere "
             "disclosed on both bases. legacy source: %s ; restated source: %s ; "
             "reconciliation residual PPA+SAT-A&T = %g USDm"
             % (b["src_legacy"], b["src_modern"], b["recon_sales"]))
        add("de_bridge_ppa_share_of_at_net_sales", b["fy"], b["fq"], round(b["share_sales"], 6),
            "ratio", "inference", b["src_legacy"] + " + " + b["src_modern"], n)
        n = ("segment_basis=bridge; as_reported_or_restated=derived; "
             "PPA operating profit / legacy Agriculture & Turf operating profit for a period "
             "Deere disclosed on both bases. legacy source: %s ; restated source: %s ; "
             "reconciliation residual PPA+SAT-A&T = %g USDm"
             % (b["src_legacy"], b["src_modern"], b["recon_op"]))
        add("de_bridge_ppa_share_of_at_operating_profit", b["fy"], b["fq"],
            round(b["share_op"], 6), "ratio", "inference",
            b["src_legacy"] + " + " + b["src_modern"], n)

    # forward stability series
    for f in forward:
        n = ("segment_basis=modern-PPA; as_reported_or_restated=derived; "
             "PPA / (PPA + Small Ag & Turf) on the modern basis. Included so a modeller can "
             "see how far the FY2019-FY2020 bridge ratio drifts after the reorganisation; "
             "a back-cast implicitly assumes this ratio is stationary.")
        add("de_ppa_share_of_ag_net_sales_modern", f["fy"], f["fq"],
            round(f["share_sales"], 6), "ratio", "inference", f["src"], n)
        if f["share_op"] is not None:
            add("de_ppa_share_of_ag_operating_profit_modern", f["fy"], f["fq"],
                round(f["share_op"], 6), "ratio", "inference", f["src"], n)

    rows.sort(key=lambda r: (r[0], r[1], QORDER.get(r[3], 9)))
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(rows)

    print("\n" + "=" * 78)
    print("wrote", OUT_CSV, len(rows), "rows")
    bys = defaultdict(list)
    for r in rows:
        bys[r[0]].append(r[1])
    for s in sorted(bys):
        print("  %-52s n=%3d  %s .. %s" % (s, len(bys[s]), min(bys[s]), max(bys[s])))

    json.dump({"bridge": bridge, "forward": forward,
               "xbrl_check": xrows, "edgar_hits": len(hits),
               "edgar_conflicts": conflicts},
              open("/tmp/de_bridge.json", "w"), indent=1)


if __name__ == "__main__":
    main()
