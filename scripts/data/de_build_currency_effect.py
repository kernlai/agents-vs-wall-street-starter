#!/usr/bin/env python3
"""
Build /data/deere/de_currency_effect.csv.

Pipeline
--------
1. Disclosed currency-translation effect on net sales (percentage points), from
   the 10-Q/10-K MD&A, via de_parse_currency_bridge.py.
2. Same effect converted to USDm  =  pp/100 x PRIOR-YEAR period net sales.
   That conversion is an inference, flagged as such in `notes`.
3. Regional revenue weights from the ASC 606 revenue-recognition matrix, via
   de_parse_geo_matrix.py.
4. Currency baskets mapping each of Deere's six primary geographic markets onto
   traded currencies (assumption set, flagged as inference).
5. FRED daily FX averaged over Deere fiscal-quarter windows, via
   de_fx_windows.py.
6. Naive weighted translation effect, calibrated against the two FY2026
   quarters Deere has already disclosed, then applied to Q3 FY2026.

Standard library only.
"""
import csv
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = ("/private/tmp/claude-501/-Users-cor/"
           "c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad")
OUT_CSV = ("/Users/cor/Documents/projects/agents-vs-wall-street-starter/"
           "data/deere/de_currency_effect.csv")

HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "segment",
          "geography", "product_line", "value", "units", "basis", "source",
          "notes"]

INF = "source_type=inference"

# ------------------------------------------------------------------ inputs

def load(name, script, args=()):
    path = os.path.join(SCRATCH, name)
    if not os.path.exists(path):
        with open(path, "w") as fh:
            subprocess.check_call([sys.executable, os.path.join(HERE, script)] + list(args),
                                  stdout=fh)
    return json.load(open(path))


BRIDGE = load("cur_raw.json", "de_parse_currency_bridge.py")
MATRIX = load("matrix.json", "de_parse_geo_matrix.py")
FX = load("fx.json", "de_fx_windows.py")

# --------------------------------------------------- fiscal calendar mapping
# Period ends as stated in the filings themselves.
QEND = {
    ("2022", "q1"): "2022-01-30", ("2022", "q2"): "2022-05-01",
    ("2022", "q3"): "2022-07-31", ("2022", "q4"): "2022-10-30",
    ("2023", "q1"): "2023-01-29", ("2023", "q2"): "2023-04-30",
    ("2023", "q3"): "2023-07-30", ("2023", "q4"): "2023-10-29",
    ("2024", "q1"): "2024-01-28", ("2024", "q2"): "2024-04-28",
    ("2024", "q3"): "2024-07-28", ("2024", "q4"): "2024-10-27",
    ("2025", "q1"): "2025-01-26", ("2025", "q2"): "2025-04-27",
    ("2025", "q3"): "2025-07-27", ("2025", "q4"): "2025-11-02",
    ("2026", "q1"): "2026-02-01", ("2026", "q2"): "2026-05-03",
    ("2026", "q3"): "2026-08-02",
    ("2019", "q1"): "2019-01-27", ("2019", "q2"): "2019-04-28",
    ("2019", "q3"): "2019-07-28", ("2019", "q4"): "2019-11-03",
    ("2020", "q1"): "2020-02-02", ("2020", "q2"): "2020-05-03",
    ("2020", "q3"): "2020-08-02", ("2020", "q4"): "2020-11-01",
    ("2021", "q1"): "2021-01-31", ("2021", "q2"): "2021-05-02",
    ("2021", "q3"): "2021-08-01", ("2021", "q4"): "2021-10-31",
}


def fy_q_from_pub(published, qtag):
    """Deere publishes a quarter's results inside the same fiscal year, except
    the Q4/FY report, which lands in the November of that same fiscal year."""
    y, m = int(published[:4]), int(published[5:7])
    if qtag == "fy":
        return (str(y if m >= 11 else y - 1), "q4")
    if qtag == "q4":
        return (str(y), "q4")
    return (str(y), qtag)


PERIOD_LEN = {"three": "Q", "six": "H1", "nine": "9M", "fy": "FY"}
SEG_NAME = {"PPA": "PPA", "SAT": "SAT", "CF": "CF", "AT_LEGACY": "AT_legacy",
            "WW_EQUIP": "", "US_CANADA": "", "OUTSIDE_US_CANADA": ""}
GEO_NAME = {"WW_EQUIP": "Worldwide", "US_CANADA": "United States and Canada",
            "OUTSIDE_US_CANADA": "Outside United States and Canada"}
SERIES_SUFFIX = {"PPA": "ppa", "SAT": "sat", "CF": "cf", "AT_LEGACY": "at_legacy",
                 "WW_EQUIP": "ww_equip_ops", "US_CANADA": "us_canada",
                 "OUTSIDE_US_CANADA": "outside_us_canada"}

rows = []


def emit(**kw):
    r = {k: "" for k in HEADER}
    r.update(kw)
    rows.append([r[k] for k in HEADER])


# ------------------------------------------- 1 + 2: disclosed pp, and USDm
# Prior-year net sales, needed for the pp -> USDm conversion, taken from the
# same MD&A table (the "Net sales" row's second figure).

def prior_net_sales(entry, nper_index):
    """Second numeric in the relevant period block of the table's Net sales row."""
    return entry.get("prior_net_sales", [None])[nper_index] \
        if entry.get("prior_net_sales") else None


seen = set()
for e in BRIDGE["mdna"]:
    scope = e["scope"]
    if scope is None:
        continue
    fy, q = fy_q_from_pub(e["published"], e["qtag"])
    pend = QEND.get((fy, q))
    if pend is None:
        continue
    periods = e["periods"] if e["periods"] != ["fy"] else ["fy"]
    for idx, plabel in enumerate(periods):
        if idx >= len(e["values"]):
            continue
        v = e["values"][idx]
        plen = PERIOD_LEN.get(plabel, "Q")
        if plen != "Q":
            continue  # keep the CSV to a single, non-overlapping quarterly basis
        if v is None:
            continue  # blank cell: Deere disclosed no material effect; not zero
        key = ("pct", scope, fy, q)
        if key in seen:
            continue
        seen.add(key)
        emit(series_id="de_currency_effect_pct_" + SERIES_SUFFIX[scope],
             period_end=pend, fiscal_year=fy, fiscal_quarter=q,
             segment=SEG_NAME.get(scope, ""), geography=GEO_NAME.get(scope, ""),
             value="%g" % v, units="pct_points_of_yoy_net_sales_change",
             basis="segment-net-sales",
             source="%s:%d" % (e["file"], e["line"]),
             notes="disclosed MD&A '%s'; rounded to whole pct points by Deere"
                   % e["label"])

# Blank-cell disclosures are recorded too, as an explicit marker row so the
# absence is visible rather than silently missing.
for e in BRIDGE["mdna"]:
    scope = e["scope"]
    if scope is None or not e["periods"]:
        continue
    if e["periods"][0] not in ("three",):
        continue
    if e["values"] and e["values"][0] is None:
        fy, q = fy_q_from_pub(e["published"], e["qtag"])
        pend = QEND.get((fy, q))
        if pend is None:
            continue
        key = ("blank", scope, fy, q)
        if key in seen:
            continue
        seen.add(key)
        emit(series_id="de_currency_effect_pct_" + SERIES_SUFFIX[scope],
             period_end=pend, fiscal_year=fy, fiscal_quarter=q,
             segment=SEG_NAME.get(scope, ""), geography=GEO_NAME.get(scope, ""),
             value="", units="pct_points_of_yoy_net_sales_change",
             basis="segment-net-sales",
             source="%s:%d" % (e["file"], e["line"]),
             notes="MD&A row present but cell left blank: Deere disclosed no "
                   "effect at 1pp rounding; NOT zero, magnitude <0.5pp")

# ------------------------------------------------- 3: regional weight shares

def matrix_for(period_end):
    best = None
    for m in MATRIX:
        if m["validation"]:
            continue
        p = m["period"]
        if not p or p["months"] != "Three" or p["end"] != period_end:
            continue
        best = m
    return best


REGION_KEY = [
    ("United States", "United States"),
    ("Canada", "Canada"),
    ("Western Europe", "Western Europe"),
    ("Central Europe and CIS", "Central Europe and CIS"),
    ("Latin America", "Latin America"),
    ("Asia, Africa, Oceania, and Middle East", "Asia, Africa, Oceania, and Middle East"),
]
SEG_IDX = {"PPA": 0, "SAT": 1, "CF": 2, "FS": 3, "TOTAL": 4}


def region_rows(mx):
    """Normalise the parsed geo dict onto the six canonical region names."""
    out = {}
    for label, vals in mx["geo"].items():
        lab = label.lower()
        for canon, _ in REGION_KEY:
            # Deere renamed the sixth market from "Asia, Africa, Australia,
            # New Zealand, and Middle East" to "Asia, Africa, Oceania, and
            # Middle East" during fiscal 2023; both spellings are the same row.
            if canon.lower() in lab or (
                    canon.startswith("Asia") and lab.startswith("asia")):
                out[canon] = vals
                break
    return out


# ---------------------------------------- 4: region -> currency basket (INFER)
# Assumption set. Weights are shares of a region's Deere revenue that translate
# from the named currency. USD entries capture revenue that is invoiced or
# effectively pegged in dollars and therefore carries no translation exposure.
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
BASKET_RATIONALE = {
    "United States": "domestic USD revenue, no translation exposure",
    "Canada": "Deere Canada functional currency is CAD",
    "Western Europe": "Germany/France/Benelux/Iberia/Italy in EUR; UK ag and "
                      "turf in GBP; Nordics SEK; Switzerland CHF",
    "Central Europe and CIS": "PLN/CZK/HUF/RON managed against the euro and much "
                              "CE equipment is euro-invoiced; CIS immaterial post-2022",
    "Latin America": "Brazil dominates (Horizontina/Montenegro manufacturing) in BRL; "
                     "Mexico MXN; Argentine and Andean ag equipment is USD-priced",
    "Asia, Africa, Oceania, and Middle East": "India (Pune) largest, INR; "
                                              "Australia/NZ AUD; China CNY; South Africa ZAR; "
                                              "Gulf states pegged to USD",
}


def fx_move(ccy, fq):
    """fq is a window key such as 'FY2026Q3'."""
    if ccy == "USD":
        return 0.0
    rec = FX.get(ccy)
    if rec is None:
        return None
    return rec["yoy_pct"].get(fq)


def naive_effect(mx, seg, fq):
    """Weighted yoy FX move, in percentage points of prior-year revenue.

    effect = sum_over_regions ( prior-year revenue share x regional FX move )
    which is the first-order translation identity: revenue earned in a foreign
    currency is restated into dollars at a rate that moved by that much.
    """
    rr = region_rows(mx)
    idx = SEG_IDX[seg]
    base = {}
    for canon, _ in REGION_KEY:
        v = rr.get(canon)
        if v is None or len(v) < 5:
            return None, None
        base[canon] = v[idx]
    total = sum(base.values())
    if total == 0:
        return None, None
    eff = 0.0
    detail = {}
    for canon, amt in base.items():
        w = amt / float(total)
        sub = 0.0
        for ccy, share in BASKET[canon].items():
            mv = fx_move(ccy, fq)
            if mv is None:
                return None, None
            sub += share * mv
        detail[canon] = {"weight": w, "region_fx_move_pct": sub,
                         "contribution_pp": w * sub}
        eff += w * sub
    return eff, detail


# Every quarter for which BOTH a disclosed pp figure and a prior-year
# three-month geographic matrix exist.  base_end is the prior-year quarter end.
def prior_q_end(fy, q):
    return QEND.get((str(int(fy) - 1), q))


disclosed = {}
blank = set()
for r in rows:
    d = dict(zip(HEADER, r))
    if not d["series_id"].startswith("de_currency_effect_pct_"):
        continue
    seg = d["series_id"].rsplit("de_currency_effect_pct_", 1)[-1]
    if d["value"] == "":
        blank.add((d["fiscal_year"], d["fiscal_quarter"], seg))
    else:
        disclosed[(d["fiscal_year"], d["fiscal_quarter"], seg)] = float(d["value"])

report = {"calibration": [], "target": {}, "fx": {}}

for fy in ("2022", "2023", "2024", "2025", "2026"):
    for q in ("q1", "q2", "q3"):
        base_end = prior_q_end(fy, q)
        mx = matrix_for(base_end)
        if mx is None:
            continue
        fq = "FY%sQ%s" % (fy, q[-1])
        for seg in ("PPA", "SAT", "CF"):
            eff, _ = naive_effect(mx, seg, fq)
            if eff is None:
                continue
            key = (fy, q, seg.lower())
            obs = disclosed.get(key)
            is_blank = key in blank
            report["calibration"].append(
                {"segment": seg, "fy": fy, "quarter": q, "base_matrix": base_end,
                 "naive_pp": eff, "disclosed_pp": obs,
                 "disclosed_blank": is_blank})


def fit_k(points):
    """Least-squares slope through the origin: disclosed = k x naive."""
    num = sum(p["naive_pp"] * p["obs"] for p in points)
    den = sum(p["naive_pp"] ** 2 for p in points)
    if den == 0:
        return None, None, 0
    k = num / den
    resid = [p["obs"] - k * p["naive_pp"] for p in points]
    rmse = (sum(r * r for r in resid) / len(resid)) ** 0.5
    return k, rmse, len(points)


# Two readings of the blank cells, reported side by side rather than one being
# quietly chosen: strict (drop them) and inclusive (a printed-but-blank cell is
# Deere stating the effect rounds to zero).
pts_strict, pts_incl = [], []
for c in report["calibration"]:
    if c["disclosed_pp"] is not None:
        p = {"naive_pp": c["naive_pp"], "obs": c["disclosed_pp"], **c}
        pts_strict.append(p)
        pts_incl.append(p)
    elif c["disclosed_blank"]:
        pts_incl.append({"naive_pp": c["naive_pp"], "obs": 0.0, **c})

k_strict, rmse_strict, n_strict = fit_k(pts_strict)
k_incl, rmse_incl, n_incl = fit_k(pts_incl)
report["fit"] = {
    "strict_drop_blanks": {"k": k_strict, "rmse_pp": rmse_strict, "n": n_strict},
    "inclusive_blank_as_zero": {"k": k_incl, "rmse_pp": rmse_incl, "n": n_incl},
}
per_seg = {}
for seg in ("PPA", "SAT", "CF"):
    ps = [p for p in pts_incl if p["segment"] == seg]
    if ps:
        kk, rr_, nn = fit_k(ps)
        per_seg[seg] = {"k": kk, "rmse_pp": rr_, "n": nn}
report["fit"]["per_segment_inclusive"] = per_seg

# Headline calibration: the pooled inclusive fit.  A single pooled k is used in
# preference to per-segment factors because Deere rounds the disclosure to whole
# percentage points, so a per-segment factor fitted on values of 1-4pp is mostly
# fitting rounding noise.
K = k_incl
KRMSE = rmse_incl
kfac = {"PPA": K, "SAT": K, "CF": K, "TOTAL": K}
report["calibration_factor"] = kfac
report["k_used"] = K

# prior-year Q3 FY2025 net sales, 8-K segment basis (verified from the corpus)
LY_Q3_SALES = {"PPA": 4273.0, "SAT": 3025.0, "CF": 3059.0}
LY_Q3_TOTAL_NSR = 12018.0   # rev-rec footnote total, three months ended 2025-07-27

mx_q3 = matrix_for("2025-07-27")
for seg in ("PPA", "SAT", "CF", "TOTAL"):
    eff, detail = naive_effect(mx_q3, seg, "FY2026Q3")
    k = kfac.get(seg if seg != "TOTAL" else "TOTAL")
    cal = eff * k if (eff is not None and k) else None
    report["target"][seg] = {"naive_pp": eff, "calibrated_pp": cal,
                             "k": k, "rmse_pp": KRMSE, "detail": detail}

    if seg == "TOTAL":
        base_sales = LY_Q3_TOTAL_NSR
        seg_field, geo_field = "", "Worldwide"
        sid_pct = "de_currency_effect_pct_total"
        sid_usd = "de_currency_effect_usdm_total"
    else:
        base_sales = LY_Q3_SALES[seg]
        seg_field, geo_field = seg, ""
        sid_pct = "de_currency_effect_pct_" + seg.lower()
        sid_usd = "de_currency_effect_usdm_" + seg.lower()

    if cal is not None:
        emit(series_id=sid_pct, period_end="2026-08-02", fiscal_year="2026",
             fiscal_quarter="q3", segment=seg_field, geography=geo_field,
             value="%.2f" % cal, units="pct_points_of_yoy_net_sales_change",
             basis="segment-net-sales" if seg != "TOTAL" else "rev-rec",
             source="FRED DEX* daily averages over 2026-05-04..2026-08-02 vs "
                    "2025-04-28..2025-07-27; weights from rev-rec matrix "
                    "2025-07-27",
             notes="%s; ESTIMATE for an unreported quarter (Deere reports "
                   "2026-08-20); naive weighted move %.2fpp x calibration "
                   "factor %.2f" % (INF, eff, k))
        emit(series_id=sid_usd, period_end="2026-08-02", fiscal_year="2026",
             fiscal_quarter="q3", segment=seg_field, geography=geo_field,
             value="%.0f" % (cal / 100.0 * base_sales),
             units="USDm", basis="segment-net-sales" if seg != "TOTAL" else "rev-rec",
             source="derived: estimated pp x prior-year Q3 FY2025 net sales %.0f"
                    % base_sales,
             notes="%s; ESTIMATE for an unreported quarter; 1-sigma band "
                   "+/-%.0f USDm from the %.2fpp calibration RMSE"
                   % (INF, KRMSE / 100.0 * base_sales, KRMSE))
        emit(series_id=sid_pct + "_lo", period_end="2026-08-02",
             fiscal_year="2026", fiscal_quarter="q3", segment=seg_field,
             geography=geo_field, value="%.2f" % (cal - KRMSE),
             units="pct_points_of_yoy_net_sales_change",
             basis="segment-net-sales" if seg != "TOTAL" else "rev-rec",
             source="point estimate minus 1 calibration RMSE",
             notes="%s; low end of the 1-sigma band" % INF)
        emit(series_id=sid_pct + "_hi", period_end="2026-08-02",
             fiscal_year="2026", fiscal_quarter="q3", segment=seg_field,
             geography=geo_field, value="%.2f" % (cal + KRMSE),
             units="pct_points_of_yoy_net_sales_change",
             basis="segment-net-sales" if seg != "TOTAL" else "rev-rec",
             source="point estimate plus 1 calibration RMSE",
             notes="%s; high end of the 1-sigma band" % INF)

    if seg != "TOTAL" and detail:
        for canon, dd in detail.items():
            emit(series_id="de_fx_exposure_share_" + seg.lower(),
                 period_end="2025-07-27", fiscal_year="2025", fiscal_quarter="q3",
                 segment=seg, geography=canon, value="%.4f" % dd["weight"],
                 units="share_of_segment_revenue", basis="rev-rec",
                 source="2025-08-14__de-us-20250814-q3-10q__155834.md note 3",
                 notes="prior-year base-quarter revenue weight used for the "
                       "translation calculation")

# per-currency exposure of total company revenue, prior-year Q3 base
rr = region_rows(mx_q3)
tot = sum(rr[c][SEG_IDX["TOTAL"]] for c, _ in REGION_KEY)
ccy_share = {}
for canon, _ in REGION_KEY:
    w = rr[canon][SEG_IDX["TOTAL"]] / float(tot)
    for ccy, share in BASKET[canon].items():
        ccy_share[ccy] = ccy_share.get(ccy, 0.0) + w * share
for ccy, sh in sorted(ccy_share.items(), key=lambda x: -x[1]):
    emit(series_id="de_fx_exposure_share_" + ccy.lower(),
         period_end="2025-07-27", fiscal_year="2025", fiscal_quarter="q3",
         segment="", geography="", value="%.4f" % sh,
         units="share_of_worldwide_net_sales_and_revenues", basis="rev-rec",
         source="rev-rec matrix 2025-07-27 x region-currency basket assumption",
         notes="%s; basket assumption, not a Deere disclosure" % INF)
report["currency_shares_total"] = ccy_share

# realised FX moves
for ccy, rec in FX.items():
    for qq, pend, fy, fq in (("Q1", "2026-02-01", "2026", "q1"),
                             ("Q2", "2026-05-03", "2026", "q2"),
                             ("Q3", "2026-08-02", "2026", "q3")):
        v = rec["yoy_pct"][qq]
        if v is None:
            continue
        emit(series_id="de_fx_rate_yoy_pct_" + ccy.lower(),
             period_end=pend, fiscal_year=fy, fiscal_quarter=fq,
             segment="", geography="", value="%.3f" % v,
             units="pct_change_usd_per_fx_vs_year_ago_quarter", basis="",
             source="FRED %s daily, averaged over the Deere fiscal-quarter window"
                    % rec["series"],
             notes="positive = foreign currency stronger vs USD = translation "
                   "tailwind to Deere revenue")
report["fx"] = {c: r["yoy_pct"] for c, r in FX.items()}

# ------------------------------- 2b: USDm conversion of the disclosed history
# Prior-year quarter net sales come straight from the same MD&A table that
# carries the percentage, so the two always refer to the same base.
prior_sales = {}
for e in BRIDGE["mdna"]:
    scope = e["scope"]
    if scope not in ("PPA", "SAT", "CF") or not e.get("net_sales_blocks"):
        continue
    if not e["periods"] or e["periods"][0] != "three":
        continue
    blk = e["net_sales_blocks"][0]
    if len(blk) < 2:
        continue
    fy, q = fy_q_from_pub(e["published"], e["qtag"])
    prior_sales[(fy, q, scope.lower())] = blk[1]

for (fy, q, seg), pp in sorted(disclosed.items()):
    if seg not in ("ppa", "sat", "cf"):
        continue
    ly = prior_sales.get((fy, q, seg))
    if ly is None:
        continue
    emit(series_id="de_currency_effect_usdm_" + seg,
         period_end=QEND.get((fy, q), ""), fiscal_year=fy, fiscal_quarter=q,
         segment=seg.upper(), geography="",
         value="%.0f" % (pp / 100.0 * ly), units="USDm",
         basis="segment-net-sales",
         source="derived: disclosed %+g pp x prior-year quarter net sales %.0f"
                % (pp, ly),
         notes="%s; Deere discloses the effect only in whole percentage points, "
               "so this carries +/-0.5pp of rounding (about +/-%.0f USDm)"
               % (INF, 0.005 * ly))

# --------------------------------------- slide operating-profit currency bars
# Deere reports Q1 in February, Q2 in May, Q3 in August and Q4 in November of
# the same fiscal year, so the deck's publication month fixes the quarter.
MONTH_Q = {2: "q1", 5: "q2", 8: "q3", 11: "q4"}
for s in BRIDGE["slides"]:
    pub = s["file"][:10]
    q = MONTH_Q.get(int(pub[5:7]))
    if q is None:
        continue
    fy = pub[:4]
    emit(series_id="de_currency_effect_opprofit_usdm_" + s["segment"].lower(),
         period_end=QEND.get((fy, q), ""), fiscal_year=fy, fiscal_quarter=q,
         segment=s["segment"], geography="", value="%g" % s["value"],
         units="USDm", basis="operating-profit-bridge",
         source="%s:%d" % (s["file"], s["line"]),
         notes="earnings-deck waterfall; effect on OPERATING PROFIT, NOT on "
               "net sales; accepted only because the full bridge reconciles "
               "(%s convention)" % s["convention"])

# ------------------------- Deere's own FY2026 currency-translation guidance
# From the 2026-05-21 8-K "Deere Segment Outlook for Fiscal 2026" table.
GUIDE = {"PPA": 3.0, "SAT": 1.0, "CF": 2.0}
for seg, g in GUIDE.items():
    emit(series_id="de_currency_effect_guidance_pct_" + seg.lower(),
         period_end="2026-11-01", fiscal_year="2026", fiscal_quarter="fy",
         segment=seg, geography="", value="%+.1f" % g,
         units="pct_of_fy_net_sales", basis="segment-net-sales",
         source="filings/2026-05-21__de-us-20260521-q2-8k__1042167.md:186-188",
         notes="Deere's own FY2026 currency-translation guidance, set "
               "2026-05-21 on then-current spot rates")

# ------------------------------- Q4 FY2026 sensitivity: spot rates frozen
# Computed by scripts/data/de_fx_q4_freeze.py using the 2026-08-03..07 average
# held flat through 2026-11-01.
Q4_FREEZE = {"PPA": 0.81, "SAT": -0.21, "CF": 0.06, "TOTAL": 0.25}
FY_IMPLIED = {"PPA": 2.28, "SAT": 0.94, "CF": 1.63}
for seg, v in Q4_FREEZE.items():
    emit(series_id="de_currency_effect_pct_" + seg.lower(),
         period_end="2026-11-01", fiscal_year="2026", fiscal_quarter="q4",
         segment="" if seg == "TOTAL" else seg,
         geography="Worldwide" if seg == "TOTAL" else "",
         value="%+.2f" % v, units="pct_points_of_yoy_net_sales_change",
         basis="segment-net-sales" if seg != "TOTAL" else "rev-rec",
         source="de_fx_q4_freeze.py: FRED spot 2026-08-03..07 held flat to "
                "2026-11-01 vs the 2025-07-28..2025-11-02 average",
         notes="%s; SCENARIO, not a forecast: assumes rates stop moving" % INF)
for seg, v in FY_IMPLIED.items():
    emit(series_id="de_currency_effect_implied_fy_pct_" + seg.lower(),
         period_end="2026-11-01", fiscal_year="2026", fiscal_quarter="fy",
         segment=seg, geography="", value="%+.2f" % v,
         units="pct_of_fy_net_sales", basis="segment-net-sales",
         source="Q1 and Q2 as disclosed + Q3 estimate + Q4 spot-freeze scenario",
         notes="%s; compare with Deere's %+.1f%% FY2026 guidance -- the gap is "
               "the revenue risk the currency line carries into H2"
               % (INF, GUIDE[seg]))


def sort_key(r):
    d = dict(zip(HEADER, r))
    return (d["series_id"], d["period_end"], d["geography"])


rows.sort(key=sort_key)
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
with open(OUT_CSV, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(HEADER)
    w.writerows(rows)

json.dump(report, open(os.path.join(SCRATCH, "report.json"), "w"), indent=1)
print("wrote %d rows to %s" % (len(rows), OUT_CSV))
print(json.dumps(report["calibration"], indent=1))
print("k:", json.dumps(kfac, indent=1))
print("target:", json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "detail"}
                             for k, v in report["target"].items()}, indent=1))
