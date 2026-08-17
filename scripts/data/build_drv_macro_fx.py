#!/usr/bin/env python3
"""
build_drv_macro_fx.py -- Deere (DE) forecasting panel: macro, rates and FX drivers.

Builds 20 years (2006-2026) of quarterly macro/rates/FX series from FRED's keyless
CSV endpoint, aggregated on TWO calendars:

  1. CALENDAR quarters (Q1=Jan-Mar ... Q4=Oct-Dec)          -> series_id as given
  2. DEERE FISCAL quarters (FY ends late Oct/early Nov)     -> series_id + "_dfq"

The fiscal-quarter grid is derived from authoritative SEC XBRL period boundaries
(CIK 0000315189) for FY2009+ and inferred as calendar month-ends for FY2006-FY2008,
which is what Deere used until it moved to a 52/53-week calendar in FY2017.

Standard library only. No API keys.

Output: tidy long CSV
  series_id,period_end,fiscal_year,fiscal_quarter,value,units,source_type,source,notes
"""

import csv
import datetime as dt
import json
import os
import ssl
import urllib.request

UA = "AgentsVsWallStreet cor@salomo.io"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache_macro_fx")
OUT_CSV = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/drv_macro_fx.csv"

START = dt.date(2005, 1, 1)   # 1yr of runway before 2006 so 2006 YoY is computable
END = dt.date(2026, 8, 16)    # "today"
PANEL_START = dt.date(2006, 1, 1)

# Minimum fraction of a quarter's days that must be covered by data to emit a row.
MIN_COVERAGE = 0.25

os.makedirs(CACHE, exist_ok=True)
_SSL = ssl.create_default_context()


def fetch(url, fname):
    """Download to cache once; return bytes."""
    path = os.path.join(CACHE, fname)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return open(path, "rb").read()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90, context=_SSL) as r:
        data = r.read()
    open(path, "wb").write(data)
    return data


# ---------------------------------------------------------------- FRED loading

def fred(series_id):
    """Return list of (date, float) from FRED CSV. FRED marks gaps with '.'."""
    url = ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s&cosd=%s&coed=%s"
           % (series_id, START.isoformat(), END.isoformat()))
    raw = fetch(url, "fred_%s.csv" % series_id).decode("utf-8")
    rows = list(csv.reader(raw.strip().splitlines()))
    out = []
    for r in rows[1:]:
        if len(r) < 2:
            continue
        v = r[1].strip()
        if v in (".", "", "NA"):
            continue
        out.append((dt.date.fromisoformat(r[0].strip()), float(v)))
    out.sort()
    if not out:
        raise RuntimeError("FRED series %s returned no usable observations" % series_id)
    return out


# ------------------------------------------------------- observation intervals
# Every observation is expanded into the [start, end] day-interval it *covers*.
# Daily series cover one day; monthly cover their calendar month; quarterly cover
# their three months. Aggregation is then a single day-overlap-weighted mean,
# identical for all frequencies.

def add_months(d, n):
    y, m = divmod((d.year * 12 + d.month - 1) + n, 12)
    return dt.date(y, m + 1, 1)


def intervals(obs, freq):
    """[(cover_start, cover_end, value)] -- FRED dates monthly/quarterly obs at
    the FIRST day of the period they cover."""
    out = []
    for d, v in obs:
        if freq == "D":
            out.append((d, d, v))
        elif freq == "M":
            out.append((d, add_months(d, 1) - dt.timedelta(days=1), v))
        elif freq == "Q":
            out.append((d, add_months(d, 3) - dt.timedelta(days=1), v))
        else:
            raise ValueError(freq)
    return out


def overlap_days(a0, a1, b0, b1):
    lo, hi = max(a0, b0), min(a1, b1)
    return 0 if hi < lo else (hi - lo).days + 1


def agg_mean(ivals, w0, w1, data_end):
    """Day-overlap-weighted mean over window [w0,w1].

    Coverage semantics: a window is COMPLETE when the source has published
    through its end (data_end >= w1). It is PARTIAL only when the source series
    stops inside the window. Weekend/holiday gaps in daily series are NOT
    partiality -- a quarter of business-day quotes is a complete quarter.

    Returns (value, coverage_fraction).
    """
    win_days = (w1 - w0).days + 1
    num = den = 0.0
    for s, e, v in ivals:
        w = overlap_days(s, e, w0, w1)
        if w == 0:
            continue
        num += v * w
        den += w
    if den == 0:
        return None, 0.0
    if data_end >= w1:
        frac = 1.0
    else:
        frac = max(0.0, ((data_end - w0).days + 1) / win_days)
    return num / den, frac


def agg_last(obs, w0, w1):
    """Last available observation at-or-before window end, if inside window."""
    sel = [(d, v) for d, v in obs if w0 <= d <= w1]
    if not sel:
        return None, None
    return sel[-1][1], sel[-1][0]


# ------------------------------------------------------ Deere fiscal calendar

def deere_fiscal_quarters():
    """Return sorted list of dicts: {fy, fq, start, end} for Deere fiscal quarters.

    FY2009+ boundaries come from SEC XBRL EarningsPerShareDiluted period tags
    (authoritative). FY2006-FY2008 are INFERRED as calendar month-ends
    (Jan31/Apr30/Jul31/Oct31), which is the convention visible in every SEC-tagged
    Deere period through FY2016.
    """
    url = ("https://data.sec.gov/api/xbrl/companyconcept/CIK0000315189/"
           "us-gaap/EarningsPerShareDiluted.json")
    doc = json.loads(fetch(url, "sec_de_eps.json").decode("utf-8"))
    facts = doc["units"]["USD/shares"]

    # (a) explicit ~quarterly durations -> Q1/Q2/Q3 boundaries
    # Collect every candidate boundary for each (period fiscal year, fiscal period).
    # Deere moved from calendar month-end quarters to a 52/53-week calendar in
    # FY2017 and RESTATED the FY2016 comparatives onto the new basis, so FY2016
    # has two competing sets of boundaries in XBRL (e.g. Q2 ends 2016-04-30
    # as-reported vs 2016-05-01 as-restated). Prefer the AS-ORIGINALLY-REPORTED
    # boundary: the fact whose own `fy` tag equals the period's fiscal year.
    # A fact tagged fy=2017 describing a 2016 period is a restated comparative.
    cands = {}
    for f in facts:
        s, e = f.get("start"), f.get("end")
        if not s:
            continue
        s, e = dt.date.fromisoformat(s), dt.date.fromisoformat(e)
        fp = f.get("fp")
        if not (70 <= (e - s).days <= 110) or fp not in ("Q1", "Q2", "Q3"):
            continue
        # The `fy` tag is the FILING fiscal year, not always the period's own FY.
        # Deere's FY ends late Oct / early Nov, so a period ending Nov or Dec
        # belongs to the NEXT fiscal year's Q1.
        pfy = e.year + 1 if e.month >= 11 else e.year
        cands.setdefault((pfy, fp), []).append((s, e, f.get("fy")))

    byfy = {}
    for (pfy, fp), lst in cands.items():
        # rank: as-reported first (fy tag == period FY), then earliest end date
        lst.sort(key=lambda t: (0 if t[2] == pfy else 1, t[1]))
        s, e, _ = lst[0]
        byfy.setdefault(pfy, {})[fp] = (s, e)

    quarters = []
    all_fys = sorted(byfy)
    for fy in all_fys:
        d = byfy[fy]
        for fp in ("Q1", "Q2", "Q3"):
            if fp in d:
                quarters.append({"fy": fy, "fq": fp, "start": d[fp][0], "end": d[fp][1]})
        # Q4: from Q3end+1 to (next FY's Q1 start - 1)
        nxt = byfy.get(fy + 1, {}).get("Q1")
        if "Q3" in d and nxt:
            q4s = d["Q3"][1] + dt.timedelta(days=1)
            q4e = nxt[0] - dt.timedelta(days=1)
            if 70 <= (q4e - q4s).days <= 110:
                quarters.append({"fy": fy, "fq": "Q4", "start": q4s, "end": q4e})

    # FY2006-FY2008: inferred calendar month-end quarters.
    inferred = []
    for fy in (2006, 2007, 2008):
        ends = [dt.date(fy - 1, 11, 1), dt.date(fy, 2, 1), dt.date(fy, 5, 1), dt.date(fy, 8, 1)]
        for i, fp in enumerate(("Q1", "Q2", "Q3", "Q4")):
            s = ends[i]
            e = add_months(s, 3) - dt.timedelta(days=1)
            inferred.append({"fy": fy, "fq": fp, "start": s, "end": e, "inferred": True})
    have = {(q["fy"], q["fq"]) for q in quarters}
    quarters += [q for q in inferred if (q["fy"], q["fq"]) not in have]

    # FY2026 Q3: not yet reported (today = 2026-08-16, Deere reports late August).
    # Deere's 52/53-week calendar makes Q3 exactly 13 weeks after Q2 end.
    q2_26 = next((q for q in quarters if q["fy"] == 2026 and q["fq"] == "Q2"), None)
    if q2_26 and not any(q["fy"] == 2026 and q["fq"] == "Q3" for q in quarters):
        s = q2_26["end"] + dt.timedelta(days=1)
        quarters.append({"fy": 2026, "fq": "Q3", "start": s,
                         "end": s + dt.timedelta(days=90), "projected": True})

    quarters.sort(key=lambda q: q["end"])
    return quarters


def calendar_quarters():
    out = []
    for y in range(2005, 2027):
        for i, fq in enumerate(("Q1", "Q2", "Q3", "Q4")):
            s = dt.date(y, 1 + 3 * i, 1)
            e = add_months(s, 3) - dt.timedelta(days=1)
            if e < dt.date(2005, 1, 1) or s > END:
                continue
            out.append({"fy": y, "fq": fq, "start": s, "end": e})
    return out


# ------------------------------------------------------------------ the series

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s"

SERIES = [
    # series_id,               fred_id,            freq, units,   convention, description
    ("us_fed_funds_rate",      "DFF",              "D", "percent", "avg",
     "Effective federal funds rate"),
    ("us_10y_treasury",        "DGS10",            "D", "percent", "avg",
     "10-Year Treasury constant maturity yield"),
    ("us_cpi",                 "CPIAUCSL",         "M", "index",   "avg",
     "CPI-U all items, seasonally adjusted, 1982-84=100"),
    ("us_gdp_growth",          "A191RL1Q225SBEA",  "Q", "percent", "asis",
     "Real GDP, % change from preceding quarter, seasonally adjusted annual rate"),
    ("usd_index_dxy",          "DTWEXBGS",         "D", "index",   "avg",
     "Fed Nominal Broad U.S. Dollar Index, Jan-2006=100"),
    ("fx_eur_usd",             "DEXUSEU",          "D", "ratio",   "avg",
     "USD per 1 EUR"),
    ("fx_usd_brl",             "DEXBZUS",          "D", "ratio",   "avg",
     "BRL per 1 USD"),
    ("fx_usd_inr",             "DEXINUS",          "D", "ratio",   "avg",
     "INR per 1 USD"),
    ("fx_usd_cad",             "DEXCAUS",          "D", "ratio",   "avg",
     "CAD per 1 USD"),
    ("us_housing_starts",      "HOUST",            "M", "count",   "avg",
     "Privately-owned housing units started, thousands of units, SAAR"),
    ("us_industrial_production", "INDPRO",         "M", "index",   "avg",
     "Industrial Production total index, 2017=100, seasonally adjusted"),
    ("us_consumer_sentiment",  "UMCSENT",          "M", "index",   "avg",
     "University of Michigan Consumer Sentiment, 1966Q1=100"),
]

# Quarter-END (not average) variants -- level at the balance-sheet date matters
# for John Deere Capital's repricing, distinct from the period average.
QEND_SERIES = [("us_fed_funds_rate_qend", "DFF", "percent",
                "Effective federal funds rate"),
               ("us_10y_treasury_qend", "DGS10", "percent",
                "10-Year Treasury constant maturity yield")]

# Year-over-year % change series. Translation effect on Deere's reported sales
# depends on the CHANGE in FX, not the level.
YOY_OF = ["fx_eur_usd", "fx_usd_brl", "fx_usd_inr", "fx_usd_cad",
          "usd_index_dxy", "us_cpi"]


def main():
    rows = []
    data = {}      # fred_id -> (obs, ivals)
    for _, fid, freq, _, _, _ in SERIES:
        obs = fred(fid)
        data[fid] = (obs, intervals(obs, freq))

    grids = [
        ("cal", calendar_quarters(), ""),
        ("fis", deere_fiscal_quarters(), "_dfq"),
    ]

    # values[(grid, series_id, fy, fq)] = (value, period_end, partial_note)
    values = {}

    for gname, grid, suffix in grids:
        for q in grid:
            if q["end"] < PANEL_START:
                continue

            gnote = []
            if gname == "fis":
                gnote.append("Deere fiscal %s FY%d, window %s..%s"
                             % (q["fq"], q["fy"], q["start"], q["end"]))
                if q.get("inferred"):
                    gnote.append("fiscal window INFERRED (pre-XBRL; Deere used "
                                 "calendar month-end quarters through FY2016)")
                if q.get("projected"):
                    gnote.append("fiscal window PROJECTED: FY2026 Q3 not yet "
                                 "reported as of 2026-08-16; 13-week roll from "
                                 "Q2 end 2026-05-03")

            for sid, fid, freq, units, conv, desc in SERIES:
                obs, ivals = data[fid]
                data_end = max(e for _, e, _ in ivals)
                val, frac = agg_mean(ivals, q["start"], q["end"], data_end)
                if val is None or frac < MIN_COVERAGE:
                    continue

                notes = list(gnote)
                notes.append(desc)
                if conv == "asis":
                    notes.append("AGGREGATION: none -- source is already quarterly; "
                                 "mapped to this window by day-overlap weighting")
                else:
                    notes.append("AGGREGATION: period AVERAGE (day-overlap weighted "
                                 "mean of %s observations)"
                                 % {"D": "daily", "M": "monthly", "Q": "quarterly"}[freq])
                partial = frac < 1.0
                if partial:
                    notes.append("PARTIAL PERIOD: source data ends %s, before "
                                 "window end %s; only %.0f%% of the window is "
                                 "covered -- NOT comparable to full quarters"
                                 % (data_end, q["end"], frac * 100))

                values[(gname, sid + suffix, q["fy"], q["fq"])] = (val, q["end"], partial)
                rows.append([sid + suffix, q["end"].isoformat(), q["fy"], q["fq"],
                             round(val, 6), units, "api",
                             FRED_URL % fid, "; ".join(notes)])

            # quarter-end rate levels
            for sid, fid, units, desc in QEND_SERIES:
                obs, _ = data[fid]
                val, on = agg_last(obs, q["start"], q["end"])
                if val is None:
                    continue
                notes = list(gnote)
                notes.append(desc)
                notes.append("AGGREGATION: period END (last daily observation in "
                             "window, %s)" % on)
                if on < q["end"] - dt.timedelta(days=7):
                    notes.append("PARTIAL PERIOD: last observation %s is well "
                                 "before window end %s" % (on, q["end"]))
                rows.append([sid + suffix, q["end"].isoformat(), q["fy"], q["fq"],
                             round(val, 6), units, "api",
                             FRED_URL % fid, "; ".join(notes)])

        # ---- YoY % change, computed on the aggregated quarterly levels ----
        order = [q for q in grid if q["end"] >= PANEL_START]
        for base in YOY_OF:
            sid = base + suffix
            for i, q in enumerate(order):
                cur = values.get((gname, sid, q["fy"], q["fq"]))
                prev = values.get((gname, sid, q["fy"] - 1, q["fq"]))
                if cur is None or prev is None or prev[0] == 0:
                    continue
                yoy = (cur[0] / prev[0] - 1.0) * 100.0
                src = next(s for s in SERIES if s[0] == base)
                notes = []
                if suffix:
                    notes.append("Deere fiscal %s FY%d" % (q["fq"], q["fy"]))
                notes.append("COMPUTED: year-over-year %% change of %s, "
                             "(this quarter avg / same quarter prior year avg - 1) "
                             "x 100" % sid)
                notes.append("levels used: %.6f vs %.6f" % (cur[0], prev[0]))
                if cur[2] or prev[2]:
                    notes.append("WARNING: one or both endpoints is a PARTIAL "
                                 "period -- YoY is not like-for-like, do not use "
                                 "without adjustment")
                rows.append([base + "_yoy" + suffix,
                             q["end"].isoformat(), q["fy"], q["fq"],
                             round(yoy, 6), "percent", "api",
                             FRED_URL % src[1], "; ".join(notes)])

    rows.sort(key=lambda r: (r[0], r[1]))
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["series_id", "period_end", "fiscal_year", "fiscal_quarter",
                    "value", "units", "source_type", "source", "notes"])
        w.writerows(rows)

    # ------------------------------------------------------------- run summary
    print("wrote %d rows -> %s" % (len(rows), OUT_CSV))
    ids = {}
    for r in rows:
        ids.setdefault(r[0], []).append(r[1])
    print("%d distinct series_id" % len(ids))
    for k in sorted(ids):
        print("  %-34s n=%3d  %s .. %s" % (k, len(ids[k]), min(ids[k]), max(ids[k])))

    print("\nDeere fiscal quarters derived:")
    for q in deere_fiscal_quarters():
        if q["end"] >= dt.date(2025, 1, 1):
            flag = " [INFERRED]" if q.get("inferred") else ""
            flag += " [PROJECTED]" if q.get("projected") else ""
            print("  FY%d %s  %s .. %s%s" % (q["fy"], q["fq"], q["start"], q["end"], flag))


if __name__ == "__main__":
    main()
