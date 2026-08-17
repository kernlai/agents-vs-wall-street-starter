#!/usr/bin/env python3
"""
build_drv_equipment_demand.py

Assembles the DIRECT EQUIPMENT DEMAND panel for the Deere (DE) forecasting
dataset from three upstream extractions:

  1. AEM US Ag Tractor and Combine Report  (unit retail sales + field
     inventory)                       -> fetch_aem_tractor_combine.py
  2. FRED / BLS farm-machinery price indices
                                      -> fetch_fred_equipment_ppi.py
  3. Sandhills Global market reports (used-equipment value trends)
                                      -> fetch_sandhills_used_values.py

Emits the tidy-long CSV required by the project spec:
  series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes

All external (non-Deere) series use the CALENDAR year in fiscal_year, per
spec.  Monthly observations carry the calendar quarter in fiscal_quarter;
period_end always identifies the month unambiguously.

Standard library only.
"""

import calendar
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict

HDR = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "value",
       "units", "source_type", "source", "notes"]

AEM_BOILERPLATE = (
    "AEM US Ag Tractor and Combine Report; preliminary retail unit sales "
    "reported by AEM member manufacturers, 50 states + DC. AEM states the "
    "data are partly estimates subject to revision and cover most but not "
    "all manufacturers.")


def eom(y, m):
    return dt.date(y, m, calendar.monthrange(y, m)[1]).isoformat()


def cq(m):
    return "Q%d" % ((m - 1) // 3 + 1)


# --------------------------------------------------------------- AEM series

# AEM table row -> (series_id for MONTHLY/ANNUAL units, extra note)
UNIT_SERIES = {
    "tractor_2wd_100hp_plus": (
        "us_tractor_unit_sales_100hp_plus",
        "AEM category '2WD 100+ HP'. EXCLUDES 4WD (articulated) tractors, "
        "which are all high-horsepower -- see us_tractor_unit_sales_4wd and "
        "us_tractor_unit_sales_large_total for the combined large-tractor "
        "aggregate. This is the single best public proxy for Deere "
        "Production & Precision Ag end demand."),
    "tractor_total": (
        "us_tractor_unit_sales_total",
        "AEM 'Total Farm Tractors' = all 2WD horsepower classes + 4WD. "
        "Dominated by sub-40 HP units, which map to Small Ag & Turf, not "
        "Production & Precision Ag."),
    "combine_sp": (
        "us_combine_unit_sales",
        "AEM 'Self-Propelled Combines', all sizes. Maps directly to Deere "
        "Production & Precision Ag harvesting."),
    "tractor_4wd": (
        "us_tractor_unit_sales_4wd",
        "AEM '4WD Farm Tractors' (articulated). Low volume, high value; all "
        "units are well above 100 HP."),
    "tractor_2wd_lt40hp": (
        "us_tractor_unit_sales_under40hp",
        "AEM '2WD < 40 HP'. Compact tractors -- Small Ag & Turf read, and a "
        "consumer/housing-sensitive series rather than a row-crop one."),
    "tractor_2wd_40to100hp": (
        "us_tractor_unit_sales_40to100hp",
        "AEM '2WD 40 < 100 HP'. Utility tractors, mostly Small Ag & Turf."),
    "tractor_2wd_total": (
        "us_tractor_unit_sales_2wd_total",
        "AEM 'Total 2WD Farm Tractors' (all horsepower classes, excl. 4WD)."),
}

# categories used for the derived months-of-supply series
MOS_SERIES = {
    "tractor_2wd_100hp_plus": "us_dealer_new_inventory_months_100hp_plus",
    "tractor_total": "us_dealer_new_inventory_months",
    "combine_sp": "us_dealer_new_inventory_months_combines",
}


def load_aem(path):
    """Collapse duplicate observations of the same period into one value.

    A given (key, year, month) is reported many times: once as the
    current-year column of that month's own report, and again as the
    prior-year comparative in the following year's report (by which point AEM
    has revised it).  We keep the LATEST-VINTAGE value -- the revised figure,
    which is what a model fitted on history should see -- and record the
    first-print value in the notes when the two differ.
    """
    raw = json.load(open(path))
    buckets = defaultdict(list)
    for o in raw:
        buckets[(o["key"], o["kind"], o["year"], o["month"])].append(o)

    out = {}
    for k, obs in buckets.items():
        # report vintage "YYYY-MM"; higher == later publication
        obs = sorted(obs, key=lambda o: o["report"])
        first, last = obs[0], obs[-1]
        vals = {round(o["value"], 3) for o in obs}
        note = ""
        if len(vals) > 1:
            note = ("REVISED: AEM first printed %s, latest vintage (%s report) "
                    "is %s; spread across %d vintages = %s."
                    % (fmt(first["value"]), last["report"], fmt(last["value"]),
                       len(obs), fmt(max(vals) - min(vals))))
        out[k] = dict(value=last["value"], source=last["source"],
                      vintage=last["report"], note=note, n=len(obs))
    return out


def merge_globenewswire(aem, path):
    """Add months that survive only as a GlobeNewswire press release.

    The FinancialContent mirror of the AEM release carries the same table as
    the PDF.  Cross-checking 112 overlapping cells against the PDFs gave 111
    exact matches and one typo in the HTML (see the companion .md), so the PDF
    is always preferred where both exist; the mirror is used only to fill
    months with no surviving PDF.
    """
    if not os.path.exists(path):
        return aem, []
    gnw = json.load(open(path))
    added = []
    for ym, rec in sorted(gnw.items()):
        y, m = int(ym[:4]), int(ym[5:])
        for key, nums in rec["table"].items():
            for idx, kind in ((0, "month"), (3, "ytd"), (6, "inventory")):
                if idx >= len(nums):
                    continue
                k = (key, kind, y, m)
                if k in aem:
                    continue
                aem[k] = dict(value=nums[idx], source=rec["source"],
                              vintage=ym, n=1,
                              note="Source: AEM press release as syndicated by "
                                   "FinancialContent (GlobeNewswire); used "
                                   "because no AEM PDF for this month survives "
                                   "in the Internet Archive.")
                if kind == "month":
                    added.append((key, y, m))
    return aem, added


def validate(aem):
    """Internal consistency checks on the extracted AEM table."""
    probs = []
    months = sorted({(y, m) for (_, kind, y, m) in aem if kind == "month"})
    for (y, m) in months:
        def g(k):
            r = aem.get((k, "month", y, m))
            return r["value"] if r else None
        a, b, c = (g("tractor_2wd_lt40hp"), g("tractor_2wd_40to100hp"),
                   g("tractor_2wd_100hp_plus"))
        t2, t4, tt = g("tractor_2wd_total"), g("tractor_4wd"), g("tractor_total")
        if None not in (a, b, c, t2) and abs(a + b + c - t2) > 1:
            probs.append("%04d-%02d 2WD components %g+%g+%g=%g != total %g"
                         % (y, m, a, b, c, a + b + c, t2))
        if None not in (t2, t4, tt) and abs(t2 + t4 - tt) > 1:
            probs.append("%04d-%02d 2WD %g + 4WD %g != total %g"
                         % (y, m, t2, t4, tt))
    return probs, len(months)


def fmt(v):
    if v is None:
        return ""
    if abs(v - round(v)) < 1e-9:
        return "%d" % round(v)
    return ("%.3f" % v).rstrip("0").rstrip(".")


def build_aem_rows(aem):
    rows = []
    # ---- monthly unit sales
    monthly = defaultdict(dict)   # key -> {(y,m): rec}
    for (key, kind, y, m), rec in aem.items():
        if kind == "month":
            monthly[key][(y, m)] = rec

    for key, (sid, extra) in UNIT_SERIES.items():
        for (y, m), rec in sorted(monthly.get(key, {}).items()):
            notes = AEM_BOILERPLATE + " " + extra
            if rec["note"]:
                notes += " " + rec["note"]
            rows.append([sid, eom(y, m), y, cq(m), fmt(rec["value"]), "count",
                         "vendor", rec["source"], notes])

    # ---- derived: combined large tractors (2WD 100+ HP plus 4WD)
    a, b = monthly.get("tractor_2wd_100hp_plus", {}), monthly.get("tractor_4wd", {})
    for ym in sorted(set(a) & set(b)):
        y, m = ym
        v = a[ym]["value"] + b[ym]["value"]
        rows.append(["us_tractor_unit_sales_large_total", eom(y, m), y, cq(m),
                     fmt(v), "count", "inference", a[ym]["source"],
                     AEM_BOILERPLATE + " DERIVED = AEM 2WD 100+ HP + AEM 4WD "
                     "farm tractors. This is the 'large tractor' aggregate the "
                     "trade press and sell-side normally quote and is the "
                     "closest unit-level analogue to Deere's North American "
                     "large-ag franchise."])

    # ---- annual totals: the December report's YTD column
    for key, (sid, extra) in UNIT_SERIES.items():
        for (k2, kind, y, m), rec in sorted(aem.items()):
            if k2 != key or kind != "ytd" or m != 12:
                continue
            notes = (AEM_BOILERPLATE + " " + extra +
                     " Full calendar-year total, from the December report's "
                     "year-to-date column.")
            if rec["note"]:
                notes += " " + rec["note"]
            rows.append([sid, "%d-12-31" % y, y, "FY", fmt(rec["value"]),
                         "count", "vendor", rec["source"], notes])

    # ---- field / dealer inventory in units, and months of supply
    inv = defaultdict(dict)
    for (key, kind, y, m), rec in aem.items():
        if kind == "inventory":
            inv[key][(y, m)] = rec

    # Annual (December YTD) totals, needed for the trailing-12m identity below
    annual = {}
    for (key, kind, y, m), rec in aem.items():
        if kind == "ytd" and m == 12:
            annual[(key, y)] = rec["value"]
    ytd = {}
    for (key, kind, y, m), rec in aem.items():
        if kind == "ytd":
            ytd[(key, y, m)] = rec["value"]

    for key, sid in MOS_SERIES.items():
        iv = inv.get(key, {})
        # ---- raw inventory level in units.
        # AEM measures this at the BEGINNING of the report month, so it is
        # stamped at the end of the PRECEDING month, not the report month.
        for (y, m), rec in sorted(iv.items()):
            py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
            rows.append([sid.replace("_months", "_units"), eom(py, pm), py,
                         cq(pm), fmt(rec["value"]), "count", "vendor",
                         rec["source"],
                         AEM_BOILERPLATE + " NEW-equipment dealer/field "
                         "inventory in units. AEM reports this as 'Beginning "
                         "Inventory' of the report month (the pre-2011 Flash "
                         "Reports label the same column 'U.S. Field "
                         "Inventory'); beginning-of-month stock is stamped "
                         "here at the END of the PRECEDING month, so this row "
                         "is the %04d-%02d report's opening stock. Covers NEW "
                         "machines in the dealer channel only -- used "
                         "inventory is NOT included and is not published."
                         % (y, m)])

        # ---- months of supply.
        # Denominator = trailing-12-month retail sales through the same date,
        # recovered with the identity
        #     T12(y,m-1) = YTD(y,m-1) + Annual(y-1) - YTD(y-1,m-1)
        # which needs only the report for month m-1 (it prints BOTH years'
        # year-to-date columns) plus the prior year's December total.  That is
        # far better covered than requiring 12 consecutive monthly prints.
        for (y, m) in sorted(iv):
            py, pm = (y, m - 1) if m > 1 else (y - 1, 12)
            if pm == 12:
                t12 = annual.get((key, py))
            else:
                a = ytd.get((key, py, pm))
                b = ytd.get((key, py - 1, pm))
                c = annual.get((key, py - 1))
                t12 = (a + c - b) if None not in (a, b, c) else None
            if not t12 or t12 <= 0:
                continue
            rows.append([sid, eom(py, pm), py, cq(pm),
                         "%.2f" % (iv[(y, m)]["value"] / (t12 / 12.0)),
                         "ratio", "inference", iv[(y, m)]["source"],
                         "DERIVED months of supply = AEM new-unit dealer field "
                         "inventory at this date divided by average monthly "
                         "retail unit sales over the trailing 12 months ending "
                         "the same date. A trailing-12m denominator is used "
                         "because US tractor and combine retail sales are "
                         "strongly seasonal, so a current-month denominator "
                         "would swing wildly. The trailing-12m total is "
                         "reconstructed as YTD(this year) + prior-year annual "
                         "- YTD(prior year), all read off the same AEM "
                         "reports. NEW equipment only. " + AEM_BOILERPLATE])
    return rows


# ---------------------------------------------------------- Sandhills series

SH_CAT = {
    "high_hp_tractors": ("high-horsepower (100+ hp row-crop and 4WD) "
                         "tractors", "us_used_high_hp_tractor"),
    "combines": ("self-propelled combines", "us_used_combine"),
    "tractors_all": ("the used tractor market as a whole on TractorHouse "
                     "(dominated by high-horsepower row-crop units)",
                     "us_used_tractor"),
    "compact_utility_tractors": ("compact and utility tractors",
                                 "us_used_compact_utility_tractor"),
    "farm_equipment_all": ("used farm equipment overall",
                           "us_used_farm_equipment"),
}
SH_METRIC = {"auction": "auction_value", "asking": "asking_value",
             "inventory": "inventory"}


def build_sandhills_rows(path):
    if not os.path.exists(path):
        return []
    recs = json.load(open(path))
    rows = []
    base_note = ("Sandhills Global monthly market report (TractorHouse / "
                 "Machinery Trader), the Sandhills Equipment Value Index "
                 "family. Sandhills publishes only PERCENTAGE CHANGES free of "
                 "charge -- the EVI level itself is a paid product -- so these "
                 "are changes, not levels. Extracted from the press-release "
                 "prose by regex; sign inferred from the surrounding "
                 "directional wording.")
    for r in recs:
        cat_desc, cat_sid = SH_CAT[r["category"]]
        met = SH_METRIC[r["metric"]]
        for suffix, val, kind in (("mom_pct", r["mom_pct"], "month over month"),
                                  ("yoy_pct", r["yoy_pct"], "year over year")):
            if val is None:
                continue
            sid = "%s_%s_%s" % (cat_sid, met, suffix)
            rows.append([sid, eom(r["year"], r["month"]), r["year"],
                         cq(r["month"]), fmt(val), "percent", "vendor",
                         r["source"],
                         "%s change in Sandhills %s for %s. %s"
                         % (kind.capitalize(), met.replace("_", " "),
                            cat_desc, base_note)])
    return rows


def build_used_index(sh_rows):
    """Chain the used-tractor and used-combine auction M/M changes into an
    index level (first available month = 100).  Explicitly an inference."""
    out = []
    for cat_sid, label in (("us_used_tractor", "used high-horsepower tractors"),
                           ("us_used_combine", "used self-propelled combines")):
        sid_in = "%s_auction_value_mom_pct" % cat_sid
        pts = sorted((r[1], float(r[4]), r[7]) for r in sh_rows
                     if r[0] == sid_in)
        if len(pts) < 6:
            continue
        # only chain across CONSECUTIVE months; a gap breaks the chain
        lvl, prev, run = 100.0, None, 0
        for period_end, pct, src in pts:
            y, m, _ = (int(x) for x in period_end.split("-"))
            gap = None if prev is None else (y - prev[0]) * 12 + (m - prev[1])
            restart = gap != 1
            if restart:
                lvl, run = 100.0, run + 1   # never interpolate across a gap
            else:
                lvl *= (1.0 + pct / 100.0)
            prev = (y, m)
            suffix = "" if cat_sid == "us_used_tractor" else "_combines"
            flag = ("CHAIN RESTART (run %d begins here): the source releases "
                    "skip at least one month before this date, so this 100.00 "
                    "is a NEW base, NOT a move in value. Do not difference "
                    "this row against the row before it. " % run) if restart \
                else "Run %d. " % run
            out.append(["idx_used_equipment_values" + suffix, period_end, y,
                        cq(m), "%.2f" % lvl, "index", "inference", src,
                        flag +
                        "DERIVED index of %s auction values, built by chain-"
                        "linking the month-over-month percentage changes "
                        "Sandhills publishes. Base = 100.00 at the first month "
                        "of each unbroken run of consecutive monthly "
                        "observations, so levels are comparable ONLY within a "
                        "run. Not a Sandhills-published index level; the "
                        "underlying observables are the "
                        "us_used_*_auction_value_mom_pct / _yoy_pct series, "
                        "which are preferable for modelling."
                        % label])
    return out


# --------------------------------------------------------------------- main

def main():
    scratch = os.environ.get("BUILD_SCRATCH", ".")
    out_csv = sys.argv[1]

    rows = []

    aem_json = os.path.join(scratch, "aem_raw_observations.json")
    if os.path.exists(aem_json):
        aem = load_aem(aem_json)
        aem, added = merge_globenewswire(aem, os.path.join(scratch, "gnw.json"))
        if added:
            print("gap-filled %d category-months from the GlobeNewswire "
                  "mirror: %s" % (len(added),
                                  sorted({(y, m) for _, y, m in added})),
                  file=sys.stderr)
        probs, nmonths = validate(aem)
        print("internal consistency: %d months checked, %d failures"
              % (nmonths, len(probs)), file=sys.stderr)
        for p in probs[:20]:
            print("  !! " + p, file=sys.stderr)
        rows += build_aem_rows(aem)
    else:
        print("WARNING: no AEM extraction at %s" % aem_json, file=sys.stderr)

    fred_csv = os.path.join(scratch, "fred_ppi.csv")
    if os.path.exists(fred_csv):
        with open(fred_csv) as fh:
            rd = csv.reader(fh)
            next(rd)
            rows += [r for r in rd]
    else:
        print("WARNING: no FRED extraction at %s" % fred_csv, file=sys.stderr)

    sh_rows = build_sandhills_rows(os.path.join(scratch, "sandhills.json"))
    rows += sh_rows
    rows += build_used_index(sh_rows)

    def sort_key(r):
        return (r[0], r[1], r[3] != "FY")
    rows.sort(key=sort_key)

    # drop exact duplicates
    seen, dedup = set(), []
    for r in rows:
        k = (r[0], r[1], r[3])
        if k in seen:
            continue
        seen.add(k)
        dedup.append(r)

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HDR)
        w.writerows(dedup)

    print("wrote %d rows -> %s" % (len(dedup), out_csv))
    per = defaultdict(list)
    for r in dedup:
        per[r[0]].append(r[1])
    for sid in sorted(per):
        d = sorted(per[sid])
        print("  %-46s n=%4d  %s .. %s" % (sid, len(d), d[0], d[-1]))


if __name__ == "__main__":
    main()
