#!/usr/bin/env python3
"""
build_panel.py -- assemble the Deere & Company wide quarterly modelling panel.

Reads the nine tidy-long extraction CSVs in data/deere/ and emits ONE wide table,
one row per Deere fiscal quarter, FY2008 Q3 .. FY2026 Q3.

The final row (FY2026 Q3, period_end 2026-08-02) has all three TARGET columns
EMPTY -- that is the row to be predicted -- and every DRIVER populated wherever
the driver is already observable for that quarter.

Standard library only. Deterministic. Idempotent.

Usage:  python3 build_panel.py [--data DIR] [--out DIR] [--analysis]
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import math
import os
import re
import sys

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.abspath(os.path.join(HERE, "..", "..", "data", "deere"))

PANEL_START = (2008, "Q3")          # earliest quarter with any observed target
FORECAST_ROW = (2026, "Q3")         # the row to be predicted
FORECAST_PERIOD_END = "2026-08-02"  # confirmed in the task brief

TARGETS = [
    "de_net_sales_revenues_total",
    "de_eps_diluted_gaap",
    "de_ppa_operating_profit",
]

QORDER = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}


def qkey(fy: int, q: str) -> int:
    """Monotone integer index for a Deere fiscal quarter."""
    return fy * 4 + QORDER[q] - 1


def unkey(k: int):
    fy, i = divmod(k, 4)
    return fy, "Q%d" % (i + 1)


def d(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def fnum(s):
    s = (s or "").strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def fmt(v):
    """Format a value for CSV. None -> empty string (never zero, never a guess)."""
    if v is None:
        return ""
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return ""
        if abs(v - round(v)) < 1e-9 and abs(v) < 1e15:
            return str(int(round(v)))
        return ("%.6f" % v).rstrip("0").rstrip(".")
    return str(v)


def read_tidy(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("  [warn] " + msg, file=sys.stderr)


# --------------------------------------------------------------------------
# 1. Canonical Deere fiscal calendar
# --------------------------------------------------------------------------

def build_calendar(data_dir):
    """
    Canonical (fiscal_year, fiscal_quarter) -> period_end map.

    Source of truth is drv_macro_fx.csv's `_dfq` grid, which the macro-fx agent
    derived from SEC EDGAR XBRL period contexts and cross-checked against the
    offline filing corpus. It spans FY2006 Q1 .. FY2026 Q3 with no gaps.

    Three of the extraction files disagree by one day on two FY2016 boundaries
    (Deere's switch to a 52/53-week calendar produced two competing sets of
    FY2016 quarter ends). We therefore JOIN ON (fiscal_year, fiscal_quarter),
    never on period_end, and stamp one canonical period_end per quarter.
    """
    rows = read_tidy(os.path.join(data_dir, "drv_macro_fx.csv"))
    cal = {}
    for r in rows:
        if r["series_id"] != "fx_eur_usd_dfq":
            continue
        cal[(int(r["fiscal_year"]), r["fiscal_quarter"])] = d(r["period_end"])
    cal[FORECAST_ROW] = d(FORECAST_PERIOD_END)

    # window start = day after the previous quarter end
    keys = sorted(cal, key=lambda k: qkey(k[0], k[1]))
    windows = {}
    for i, k in enumerate(keys):
        end = cal[k]
        if i == 0:
            start = end - dt.timedelta(days=90)
        else:
            start = cal[keys[i - 1]] + dt.timedelta(days=1)
        windows[k] = (start, end)
    return cal, windows


# --------------------------------------------------------------------------
# 2. Loaders
# --------------------------------------------------------------------------

def load_by_fq(path, want, quarters_only=True, rename=None):
    """
    Load series that are ALREADY aligned to Deere fiscal quarters, keyed on
    (fiscal_year, fiscal_quarter). Used for de_segments_*, drv_macro_fx (_dfq),
    drv_ag_commodities (_fq), drv_steel_inputs (bare ids) and the Deere rows of
    drv_peers.
    """
    out = collections.defaultdict(dict)   # colname -> {(fy,q): value}
    meta = {}
    for r in read_tidy(path):
        sid = r["series_id"]
        if sid not in want:
            continue
        q = r["fiscal_quarter"]
        if quarters_only and q not in QORDER:
            continue          # drops the FY rows that share a period_end with Q4
        try:
            fy = int(r["fiscal_year"])
        except (TypeError, ValueError):
            continue
        v = fnum(r["value"])
        if v is None:
            continue
        col = (rename or {}).get(sid, sid)
        if (fy, q) in out[col] and abs(out[col][(fy, q)] - v) > 1e-9:
            warn("%s: conflicting values for %s %d %s (%s vs %s); kept first"
                 % (os.path.basename(path), col, fy, q, out[col][(fy, q)], v))
            continue
        out[col][(fy, q)] = v
        meta.setdefault(col, {"units": r["units"], "source_file": os.path.basename(path)})
    return out, meta


def load_monthly_to_fq(path, spec, windows):
    """
    Aggregate monthly observations (calendar month-end period_end) onto Deere
    fiscal quarters. `spec` maps series_id -> aggregation rule:
        'sum'  flow (unit sales)
        'mean' index / rate / percent change
        'last' stock (dealer inventory, months of supply)
    A quarter is emitted only if at least 2 months land inside its window;
    'sum' additionally requires 3 months, because a 2-of-3 sum understates a
    flow and would look like a demand collapse.
    """
    buckets = collections.defaultdict(lambda: collections.defaultdict(list))
    meta = {}
    for r in read_tidy(path):
        sid = r["series_id"]
        if sid not in spec:
            continue
        if r["fiscal_quarter"] == "FY":
            continue
        v = fnum(r["value"])
        if v is None or not r["period_end"]:
            continue
        pe = d(r["period_end"])
        for k, (s, e) in windows.items():
            if s <= pe <= e:
                buckets[sid][k].append((pe, v))
                break
        meta.setdefault(sid, {"units": r["units"], "source_file": os.path.basename(path)})

    out = collections.defaultdict(dict)
    for sid, byq in buckets.items():
        rule = spec[sid]
        for k, obs in byq.items():
            obs.sort()
            n = len(obs)
            if n < 2 or (rule == "sum" and n < 3):
                continue
            vals = [v for _, v in obs]
            if rule == "sum":
                out[sid][k] = sum(vals)
            elif rule == "mean":
                out[sid][k] = sum(vals) / n
            elif rule == "last":
                out[sid][k] = vals[-1]
    return out, meta


def load_annual_calendar_to_fq(path, want, windows):
    """
    Broadcast an annual CALENDAR-year series onto Deere fiscal quarters.
    A fiscal quarter is assigned the calendar year of its window MIDPOINT, so
    FY Q1 (Nov-Jan) picks up the prior calendar year, which is the year whose
    harvest and farm income actually drove it.
    Also returns the calendar-year map so the caller can build a clean
    prior-calendar-year (_lag1) variant that is fully observable ex ante.
    """
    byyear = collections.defaultdict(dict)
    meta = {}
    for r in read_tidy(path):
        sid = r["series_id"]
        if sid not in want or r["fiscal_quarter"] != "FY":
            continue
        v = fnum(r["value"])
        if v is None:
            continue
        byyear[sid][int(r["fiscal_year"])] = v
        meta.setdefault(sid, {"units": r["units"], "source_file": os.path.basename(path)})

    out = collections.defaultdict(dict)
    lag = collections.defaultdict(dict)
    for k, (s, e) in windows.items():
        mid = s + (e - s) / 2
        cy = mid.year
        for sid, ys in byyear.items():
            if cy in ys:
                out[sid][k] = ys[cy]
            if (cy - 1) in ys:
                lag[sid + "_lag1"][k] = ys[cy - 1]
    return out, lag, meta


def load_quarterly_calendar_to_fq(path, want, cal, exclude_fy=True, max_days=46):
    """
    Map a quarterly series reported on SOMEONE ELSE'S fiscal calendar (peers,
    BEA quarterly farm income) onto Deere's grid by NEAREST QUARTER END.

    Window containment is the obvious rule and it is wrong. Toro's quarters end
    in early August and early November, a few days AFTER Deere's -- containment
    pushes Toro's Aug-3 print into Deere's Aug-Oct quarter and leaves Deere's
    May-Jul quarter empty, shifting the whole series a quarter. Titan's Jan-31
    year end lands two days after Deere's Q1 end and gets thrown into Q2 the
    same way. Nearest-end matching puts both where they economically belong.

    A match further than `max_days` from a Deere quarter end is discarded rather
    than force-fitted. Where two prints claim the same Deere quarter the closer
    one wins and the collision is reported.

    Deere's fiscal quarter label leads the calendar by one: FY2026 Q3 runs
    2026-05-04..2026-08-02, so a peer print dated 2026-06-30 is the read-across
    for Deere's unreported FY2026 Q3.
    """
    keys = sorted(cal, key=lambda k: qkey(k[0], k[1]))
    out = collections.defaultdict(dict)
    meta = {}
    best = {}          # (sid, deere_key) -> (distance, peer_end, value)
    for r in read_tidy(path):
        sid = r["series_id"]
        if sid not in want:
            continue
        if exclude_fy and r["fiscal_quarter"] == "FY":
            continue
        v = fnum(r["value"])
        if v is None or not r["period_end"]:
            continue
        pe = d(r["period_end"])
        meta.setdefault(sid, {"units": r["units"], "source_file": os.path.basename(path)})
        k = min(keys, key=lambda kk: abs((cal[kk] - pe).days))
        dist = abs((cal[k] - pe).days)
        if dist > max_days:
            continue
        cur = best.get((sid, k))
        if cur is None:
            best[(sid, k)] = (dist, pe, v)
        else:
            warn("%s: %s prints %s and %s both map to Deere %s %s; kept the nearer (%s)"
                 % (os.path.basename(path), sid, cur[1], pe, k[0], k[1],
                    cur[1] if cur[0] <= dist else pe))
            if dist < cur[0]:
                best[(sid, k)] = (dist, pe, v)
    for (sid, k), (_, _, v) in best.items():
        out[sid][k] = v
    return out, meta


ISSUED_RE = re.compile(r"guidance_issued=(\d{4}-\d{2}-\d{2})")
SEQ_RE = re.compile(r"vintage_seq=(\d+)")


def load_guidance_point_in_time(path, want, cal):
    """
    Guidance rows are VINTAGE-encoded: `fiscal_year`/`period_end` identify the
    GUIDED fiscal year, `fiscal_quarter` is the quarter of the earnings release
    the guidance came from, and `notes` carries guidance_issued=YYYY-MM-DD.

    For every panel quarter we take the most recent vintage of the CURRENT
    fiscal year's guidance that was ISSUED STRICTLY BEFORE the quarter's own
    period_end. That is point-in-time correct: no look-ahead. For the FY2026 Q3
    forecast row this resolves to the 2026-05-21 (Q2) vintage, which is exactly
    what a forecaster standing here today has.
    """
    vint = collections.defaultdict(list)   # (sid, guided_fy) -> [(issued, seq, value)]
    meta = {}
    for r in read_tidy(path):
        sid = r["series_id"]
        if sid not in want:
            continue
        m = ISSUED_RE.search(r["notes"] or "")
        if not m:
            continue
        v = fnum(r["value"])
        if v is None:
            continue
        seq = SEQ_RE.search(r["notes"] or "")
        vint[(sid, int(r["fiscal_year"]))].append(
            (d(m.group(1)), int(seq.group(1)) if seq else -1, v))
        meta.setdefault(sid, {"units": r["units"], "source_file": os.path.basename(path)})

    out = collections.defaultdict(dict)
    vmeta = {"de_guidance_vintage_issued": {}, "de_guidance_vintage_seq": {}}
    for k, pe in cal.items():
        fy = k[0]
        best_issued, best_seq = None, None
        for (sid, gfy), obs in vint.items():
            if gfy != fy:
                continue
            avail = [o for o in obs if o[0] < pe]
            if not avail:
                continue
            avail.sort()
            issued, seq, v = avail[-1]
            out[sid][k] = v
            if best_issued is None or issued > best_issued:
                best_issued, best_seq = issued, seq
        if best_issued is not None:
            vmeta["de_guidance_vintage_issued"][k] = best_issued.isoformat()
            vmeta["de_guidance_vintage_seq"][k] = best_seq
    return out, vmeta, meta


# --------------------------------------------------------------------------
# 3. Driver selection
# --------------------------------------------------------------------------

# Group A: Deere's own accounting lines. These are published SIMULTANEOUSLY with
# the targets, so their contemporaneous value is pure look-ahead. Both level and
# _lag1 are emitted; only _lag1 is safe as a regressor.
DEERE_INTERNAL_MODERN = [
    "de_ppa_net_sales", "de_ppa_operating_margin",
    "de_sat_net_sales", "de_sat_operating_profit", "de_sat_operating_margin",
    "de_cf_net_sales", "de_cf_operating_profit", "de_cf_operating_margin",
]
DEERE_INTERNAL_LEGACY = [
    "de_at_net_sales_legacy", "de_at_operating_profit_legacy",
    "de_cf_net_sales_legacy", "de_cf_operating_profit_legacy",
    "de_ppa_share_of_ag_net_sales_modern",
    "de_ppa_share_of_ag_operating_profit_modern",
]
DEERE_INTERNAL_STEEL = [
    "de_net_sales_equipment", "de_cost_of_sales",
    "de_gross_profit_equipment", "de_gross_margin_equipment",
]

# Group B1: macro / FX, Deere-fiscal-quarter aligned (_dfq suffix in source).
MACRO = [
    "fx_eur_usd_dfq", "fx_eur_usd_yoy_dfq",
    "fx_usd_brl_dfq", "fx_usd_brl_yoy_dfq",
    "fx_usd_cad_dfq", "fx_usd_cad_yoy_dfq",
    "fx_usd_inr_dfq", "fx_usd_inr_yoy_dfq",
    "usd_index_dxy_dfq", "usd_index_dxy_yoy_dfq",
    "us_10y_treasury_dfq", "us_10y_treasury_qend_dfq",
    "us_fed_funds_rate_dfq", "us_fed_funds_rate_qend_dfq",
    "us_cpi_dfq", "us_cpi_yoy_dfq",
    "us_gdp_growth_dfq", "us_industrial_production_dfq",
    "us_housing_starts_dfq", "us_consumer_sentiment_dfq",
]
# Revised statistics: first print lands after the quarter closes AND the value
# on file is the current vintage, not what was known at the time.
MACRO_LAGGED = [
    "us_cpi_dfq", "us_cpi_yoy_dfq", "us_gdp_growth_dfq",
    "us_industrial_production_dfq", "us_housing_starts_dfq",
    "us_consumer_sentiment_dfq",
]

# Group B3: input costs (drv_steel_inputs bare ids are fiscal-quarter aligned;
# the _cq mirrors are the same monthly data on a calendar grid and are dropped
# to avoid double counting).
STEEL = [
    "px_steel_hrc", "px_steel_hrc_sheet", "px_steel_cold_rolled",
    "px_steel_scrap", "px_steel_scrap_carbon", "ppi_steel_mill_products",
    "ppi_ag_machinery", "ppi_ag_machinery_industry",
    "px_aluminium", "px_copper", "px_rubber", "px_rubber_synthetic_ppi",
    "px_diesel", "px_diesel_ppi", "idx_freight", "idx_freight_drybulk",
    "px_iron_ore",
]

# Group C: AEM / equipment demand, monthly -> fiscal quarter.
EQUIP_SPEC = {
    "us_tractor_unit_sales_100hp_plus": "sum",
    "us_tractor_unit_sales_4wd": "sum",
    "us_tractor_unit_sales_large_total": "sum",
    "us_tractor_unit_sales_2wd_total": "sum",
    "us_tractor_unit_sales_40to100hp": "sum",
    "us_tractor_unit_sales_under40hp": "sum",
    "us_tractor_unit_sales_total": "sum",
    "us_combine_unit_sales": "sum",
    "us_dealer_new_inventory_units": "last",
    "us_dealer_new_inventory_units_100hp_plus": "last",
    "us_dealer_new_inventory_units_combines": "last",
    "us_dealer_new_inventory_months": "last",
    "us_dealer_new_inventory_months_100hp_plus": "last",
    "us_dealer_new_inventory_months_combines": "last",
    "us_ag_equipment_ppi": "mean",
    "us_ag_equipment_ppi_commodity": "mean",
    "us_ag_equipment_ppi_primary_products": "mean",
    "us_ag_constr_mining_machinery_ip": "mean",
    "us_used_tractor_auction_value_yoy_pct": "mean",
    "us_used_tractor_asking_value_yoy_pct": "mean",
    "us_used_tractor_inventory_yoy_pct": "mean",
    "us_used_combine_auction_value_yoy_pct": "mean",
    "us_used_combine_inventory_yoy_pct": "mean",
    "us_used_compact_utility_tractor_auction_value_yoy_pct": "mean",
}

# Group D: farm economy, annual calendar year.
FARM_ANNUAL = [
    "us_net_farm_income", "us_net_cash_farm_income", "us_gross_cash_farm_income",
    "us_crop_cash_receipts", "us_total_cash_receipts", "us_livestock_cash_receipts",
    "us_corn_cash_receipts", "us_soybean_cash_receipts",
    "us_govt_farm_payments", "us_govt_adhoc_emergency_payments",
    "us_farm_production_expenses", "us_farm_interest_expense",
    "us_farm_fertilizer_expense",
    "us_farm_capital_expenditures", "us_farm_capex_vehicles_machinery",
    "us_farm_debt_to_asset_ratio", "us_farm_debt_total", "us_farm_assets_total",
    "us_farm_equity_total", "us_farm_working_capital",
    "us_farm_rate_of_return_assets",
    "us_farmland_values", "us_cropland_values",
    "us_planted_acres_corn", "us_planted_acres_soybean",
    "us_harvested_acres_corn", "us_harvested_acres_soybean",
    "us_corn_price_received", "us_soybean_price_received",
    "us_corn_production", "us_soybean_production",
    "br_soybean_production", "br_soybean_area_harvested", "br_corn_production",
    "ar_soybean_production", "ar_corn_production",
    "eu_ag_entrepreneurial_income", "eu_ag_output", "brl_usd_fx_rate",
]
FARM_QUARTERLY = ["us_farm_proprietors_income_bea_q"]

# Group E: peers.
PEERS = [
    "agco_revenue", "agco_eps_diluted", "agco_operating_margin",
    "cat_revenue", "cat_eps_diluted", "cat_operating_margin",
    "cnh_revenue", "cnh_eps_diluted",
    "kubota_revenue", "kubota_operating_profit", "kubota_operating_margin",
    "lindsay_revenue", "lindsay_eps_diluted", "lindsay_operating_margin",
    "titn_revenue", "titn_eps_diluted", "titn_operating_margin",
    "toro_revenue", "toro_eps_diluted", "toro_operating_margin",
    "tsco_revenue", "tsco_eps_diluted", "tsco_operating_margin",
    "valmont_revenue", "valmont_eps_diluted", "valmont_operating_margin",
]

# Group F: management guidance, resolved point-in-time.
GUIDANCE = [
    "de_guidance_fy_net_income_low", "de_guidance_fy_net_income_mid",
    "de_guidance_fy_net_income_high", "de_guidance_fy_net_income_range_width",
    "de_guidance_fy_financial_services_net_income",
    "de_guidance_fy_net_sales_revenues_growth",
    "de_guidance_fy_segment_sales_growth_ppa_mid",
    "de_guidance_fy_segment_sales_growth_sat_mid",
    "de_guidance_fy_segment_sales_growth_cf_mid",
    "de_guidance_fy_segment_operating_margin_ppa_mid",
    "de_guidance_fy_segment_operating_margin_sat_mid",
    "de_guidance_fy_segment_operating_margin_cf_mid",
    "de_guidance_fy_implied_ppa_operating_profit_mid",
    "de_guidance_fy_segment_price_realization_ppa",
    "de_guidance_fy_segment_price_realization_sat",
    "de_guidance_fy_segment_price_realization_cf",
    "de_guidance_fy_segment_currency_translation_ppa",
    "de_guidance_fy_segment_currency_translation_cf",
    "de_guidance_fy_segment_sales_growth_ag_turf_mid",
    "de_guidance_fy_segment_sales_growth_cf_legacy_at_mid",
    "de_guidance_fy_segment_operating_margin_ag_turf_mid",
]


# --------------------------------------------------------------------------
# 4. Assemble
# --------------------------------------------------------------------------

def build(data_dir):
    cal, windows = build_calendar(data_dir)

    lo, hi = qkey(*PANEL_START), qkey(*FORECAST_ROW)
    spine = [unkey(k) for k in range(lo, hi + 1)]

    cols = collections.OrderedDict()   # colname -> {(fy,q): value}
    colmeta = {}                       # colname -> dict(units, source_file, group, lag_policy)
    order = []                         # ordered column names

    def add(name, series, group, units=None, srcfile=None, note=""):
        if name in cols:
            warn("duplicate column %s -- second definition ignored" % name)
            return
        cols[name] = series
        colmeta[name] = {"units": units or "", "source_file": srcfile or "",
                         "group": group, "note": note}
        order.append(name)

    def add_many(names, loaded, meta, group, note=""):
        for n in names:
            if n not in loaded:
                warn("requested series %s not found (group %s)" % (n, group))
                continue
            m = meta.get(n, {})
            add(n, loaded[n], group, m.get("units"), m.get("source_file"), note)

    def add_lag1(names, group, note=""):
        for n in names:
            if n not in cols:
                continue
            src = cols[n]
            lagged = {}
            for (fy, q) in spine:
                pk = unkey(qkey(fy, q) - 1)
                if pk in src:
                    lagged[(fy, q)] = src[pk]
            m = colmeta[n]
            add(n + "_lag1", lagged, group, m["units"], m["source_file"], note)

    # ---- ids -------------------------------------------------------------
    # (written directly at emit time)

    # ---- targets ---------------------------------------------------------
    peers_path = os.path.join(data_dir, "drv_peers.csv")
    tgt, tmeta = load_by_fq(peers_path, {"de_revenue", "de_eps_diluted"},
                            rename={"de_revenue": "de_net_sales_revenues_total",
                                    "de_eps_diluted": "de_eps_diluted_gaap"})
    seg_path = os.path.join(data_dir, "de_segments_modern.csv")
    ppa, pmeta = load_by_fq(seg_path, {"de_ppa_operating_profit"})

    add("de_net_sales_revenues_total", tgt["de_net_sales_revenues_total"], "target",
        "USDm", "drv_peers.csv", "TARGET 1: worldwide net sales and revenues")
    add("de_eps_diluted_gaap", tgt["de_eps_diluted_gaap"], "target",
        "USD/share", "drv_peers.csv", "TARGET 2: diluted EPS, GAAP")
    add("de_ppa_operating_profit", ppa["de_ppa_operating_profit"], "target",
        "USDm", "de_segments_modern.csv", "TARGET 3: PPA operating profit, modern-PPA basis")

    # ---- Q4 override from the authoritative corpus 8-Ks -------------------
    # Deere files no Q4 10-Q, so SEC XBRL carries NO standalone three-month Q4
    # fact for either target and drv_peers.csv derives Q4 as FY minus Q1+Q2+Q3.
    # For revenue that is right to ~1 USDm. For diluted EPS it is wrong, because
    # the diluted share count differs every quarter: FY2025 Q4 derives to 3.92
    # against an as-reported 3.93, FY2024 Q4 to 4.57 against 4.55. The Q4 8-K
    # prints both figures and the corpus filings are authoritative, so they win.
    q4_path = os.path.join(data_dir, "de_q4_actuals_from_8k.csv")
    n_over = 0
    if os.path.exists(q4_path):
        for r in read_tidy(q4_path):
            col = {"de_net_sales_revenues_total_q4_asreported": "de_net_sales_revenues_total",
                   "de_eps_diluted_gaap_q4_asreported": "de_eps_diluted_gaap"}.get(r["series_id"])
            v = fnum(r["value"])
            if col is None or v is None:
                continue
            k = (int(r["fiscal_year"]), r["fiscal_quarter"])
            if k[0] > FORECAST_ROW[0] or (k[0] == FORECAST_ROW[0]
                                          and QORDER[k[1]] >= QORDER[FORECAST_ROW[1]]):
                continue        # never let a Q4 override touch the forecast row
            old = cols[col].get(k)
            if old is not None and abs(old - v) > 1e-9:
                n_over += 1
                print("  [q4-override] %s %s %s: XBRL-derived %s -> 8-K as-reported %s"
                      % (col, k[0], k[1], old, v))
            cols[col][k] = v
    else:
        warn("de_q4_actuals_from_8k.csv missing -- Q4 targets remain XBRL-derived. "
             "Run extract_q4_targets.py first.")
    if n_over:
        print("  [q4-override] %d Q4 target values replaced with as-reported 8-K figures" % n_over)

    # The forecast row must be empty on all three targets. Assert it.
    for t in TARGETS:
        if FORECAST_ROW in cols[t]:
            raise SystemExit("FATAL: %s is populated for the forecast row %s -- "
                             "an FY2026 Q3 actual leaked into the panel." % (t, FORECAST_ROW))

    # ---- Group A: Deere internal accounting ------------------------------
    segm, segm_meta = load_by_fq(seg_path, set(DEERE_INTERNAL_MODERN))
    add_many(DEERE_INTERNAL_MODERN, segm, segm_meta, "deere_internal_modern",
             "modern-PPA basis (FY2021+; FY2020 restated). Published WITH the target.")
    segl_path = os.path.join(data_dir, "de_segments_legacy.csv")
    segl, segl_meta = load_by_fq(segl_path, set(DEERE_INTERNAL_LEGACY))
    add_many(DEERE_INTERNAL_LEGACY, segl, segl_meta, "deere_internal_legacy",
             "legacy-AT basis (pre-FY2021) / derived share ratios. Published WITH the target.")
    steel_path = os.path.join(data_dir, "drv_steel_inputs.csv")
    dsi, dsi_meta = load_by_fq(steel_path, set(DEERE_INTERNAL_STEEL))
    add_many(DEERE_INTERNAL_STEEL, dsi, dsi_meta, "deere_internal_pnl",
             "equipment-operations basis. Published WITH the target.")
    peer_de, peer_de_meta = load_by_fq(peers_path, {"de_operating_margin"})
    add_many(["de_operating_margin"], peer_de, peer_de_meta, "deere_internal_pnl",
             "us-gaap:OperatingIncomeLoss / Revenues; tagging stops after FY2024.")

    internal = [c for c in order if colmeta[c]["group"].startswith("deere_internal")]
    add_lag1(internal, "deere_internal_lag1",
             "one-quarter lag of a Deere-reported line: SAFE ex ante.")

    # ---- Group B: macro / FX --------------------------------------------
    mx_path = os.path.join(data_dir, "drv_macro_fx.csv")
    mx, mx_meta = load_by_fq(mx_path, set(MACRO))
    add_many(MACRO, mx, mx_meta, "macro_fx",
             "Deere-fiscal-quarter aligned (_dfq grid).")
    add_lag1(MACRO_LAGGED, "macro_fx_lag1",
             "revised statistic: use the lag to avoid publication-lag look-ahead.")

    # ---- Group B2: ag commodities ---------------------------------------
    ag_path = os.path.join(data_dir, "drv_ag_commodities.csv")
    ag_all = {r["series_id"] for r in read_tidy(ag_path) if r["series_id"].endswith("_fq")}
    ag_names = sorted(ag_all)
    ag, ag_meta = load_by_fq(ag_path, ag_all)
    ag_names = [n for n in ag_names if len(ag.get(n, {})) >= 20]
    add_many(ag_names, ag, ag_meta, "ag_commodities",
             "Deere-fiscal-quarter aligned (_fq grid); nominal USD, not deseasonalised.")

    # ---- Group B3: input costs ------------------------------------------
    st, st_meta = load_by_fq(steel_path, set(STEEL))
    add_many(STEEL, st, st_meta, "input_costs",
             "Deere-fiscal-quarter aligned; the _cq calendar mirrors were dropped.")

    # ---- Group C: equipment demand --------------------------------------
    eq_path = os.path.join(data_dir, "drv_equipment_demand.csv")
    eq, eq_meta = load_monthly_to_fq(eq_path, EQUIP_SPEC, windows)
    eq_names = [n for n in EQUIP_SPEC if n in eq]
    add_many(eq_names, eq, eq_meta, "equipment_demand",
             "monthly AEM/BLS/Fed/Sandhills aggregated onto Deere fiscal quarters.")
    add_lag1(eq_names, "equipment_demand_lag1",
             "AEM revises and publishes ~10 days after month end; the lag is unambiguously safe.")

    # ---- Group D: farm economy ------------------------------------------
    farm_path = os.path.join(data_dir, "drv_farm_economy.csv")
    fa, fa_lag, fa_meta = load_annual_calendar_to_fq(farm_path, set(FARM_ANNUAL), windows)
    fa_names = [n for n in FARM_ANNUAL if n in fa]
    add_many(fa_names, fa, fa_meta, "farm_economy",
             "annual calendar-year value broadcast to every quarter of that calendar year.")
    for n in fa_names:
        ln = n + "_lag1"
        if ln in fa_lag:
            m = fa_meta.get(n, {})
            add(ln, fa_lag[ln], "farm_economy_lag1", m.get("units"), m.get("source_file"),
                "PRIOR calendar year: fully published, no forecast-vintage contamination.")
    fq, fq_meta = load_quarterly_calendar_to_fq(farm_path, set(FARM_QUARTERLY), cal)
    add_many([n for n in FARM_QUARTERLY if n in fq], fq, fq_meta, "farm_economy",
             "BEA quarterly farm proprietors' income, mapped by period_end containment.")
    add_lag1([n for n in FARM_QUARTERLY if n in cols], "farm_economy_lag1",
             "BEA revises; the lag is the safe form.")

    # ---- Group E: peers --------------------------------------------------
    pr, pr_meta = load_quarterly_calendar_to_fq(peers_path, set(PEERS), cal)
    pr_names = [n for n in PEERS if n in pr]
    add_many(pr_names, pr, pr_meta, "peers",
             "peer print mapped to the Deere fiscal quarter whose window contains its period_end.")
    add_lag1(pr_names, "peers_lag1",
             "safe ex ante; the contemporaneous column is only safe for peers that report BEFORE Deere.")

    # ---- Group F: guidance ----------------------------------------------
    gd_path = os.path.join(data_dir, "de_guidance.csv")
    gd, gvm, gd_meta = load_guidance_point_in_time(gd_path, set(GUIDANCE), cal)
    gd_names = [n for n in GUIDANCE if n in gd]
    add_many(gd_names, gd, gd_meta, "guidance",
             "POINT-IN-TIME: most recent vintage of the CURRENT fiscal year's guidance "
             "issued strictly before this quarter's period_end. No look-ahead.")
    add("de_guidance_vintage_issued", gvm["de_guidance_vintage_issued"], "guidance",
        "date", "de_guidance.csv", "issue date of the vintage used in this row's guidance columns")
    add("de_guidance_vintage_seq", gvm["de_guidance_vintage_seq"], "guidance",
        "count", "de_guidance.csv", "0=initial (prior-FY Q4 release), 1=Q1, 2=Q2, 3=Q3 vintage")

    # ---- calendar helpers ------------------------------------------------
    dq = {}
    for k in spine:
        s, e = windows[k]
        dq[k] = (e - s).days + 1
    add("days_in_quarter", dq, "calendar", "count", "derived",
        "fiscal window length; FY2019 and FY2025 were 53-week years (one 98-day Q4).")

    return spine, cal, windows, cols, colmeta, order


# --------------------------------------------------------------------------
# 5. Emit
# --------------------------------------------------------------------------

def emit(out_path, spine, cal, cols, order):
    header = ["fiscal_year", "fiscal_quarter", "period_end"] + order
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for (fy, q) in spine:
            row = [fy, q, cal[(fy, q)].isoformat()]
            for c in order:
                row.append(fmt(cols[c].get((fy, q))))
            w.writerow(row)
    return header


# --------------------------------------------------------------------------
# 6. Analysis (correlations for DATA_QUALITY.md)
# --------------------------------------------------------------------------

def pearson(xs, ys):
    pairs = [(a, b) for a, b in zip(xs, ys) if a is not None and b is not None]
    n = len(pairs)
    if n < 8:
        return None, n
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    sxx = sum((p[0] - mx) ** 2 for p in pairs)
    syy = sum((p[1] - my) ** 2 for p in pairs)
    if sxx <= 0 or syy <= 0:
        return None, n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pairs)
    return sxy / math.sqrt(sxx * syy), n


def yoy(series, spine):
    out = {}
    for k in spine:
        prev = unkey(qkey(*k) - 4)
        a, b = series.get(k), series.get(prev)
        if a is not None and b is not None and b != 0:
            out[k] = (a / b - 1.0) * 100.0
    return out


LOOKAHEAD_GROUPS = {"deere_internal_modern", "deere_internal_legacy",
                    "deere_internal_pnl"}


def crit_r(n, alpha_t=2.0):
    """|r| at which |t| = alpha_t for a sample of n pairs."""
    if n < 4:
        return 1.0
    return alpha_t / math.sqrt(alpha_t ** 2 + (n - 2))


def analyse(spine, cols, colmeta, order, fh):
    p = lambda *a: print(*a, file=fh)

    all_drivers = [c for c in order
                   if colmeta[c]["group"] not in ("target", "calendar")
                   and c != "de_guidance_vintage_issued"]
    # Ex-ante SAFE drivers: everything except Deere's own accounting lines read
    # contemporaneously (those are published in the same press release as the
    # target, so a contemporaneous fit is a tautology, not a forecast).
    safe = [c for c in all_drivers if colmeta[c]["group"] not in LOOKAHEAD_GROUPS]

    p("### Coverage (non-missing quarters out of %d panel rows)" % len(spine))
    p("")
    p("| column | n | % | group |")
    p("|---|---|---|---|")
    for c in order:
        n = sum(1 for k in spine if cols[c].get(k) is not None)
        p("| %s | %d | %.0f%% | %s |" % (c, n, 100.0 * n / len(spine), colmeta[c]["group"]))
    p("")

    n_tests = len(safe) * 5 * 3 * 3
    p("### Multiple-testing context")
    p("")
    p("Candidate ex-ante drivers: %d. Lags scanned: 0-4. Targets: 3. "
      "Transforms: level, YoY, first difference." % len(safe))
    p("Total correlations computed: ~%d." % n_tests)
    p("")
    p("At n=70 the 5%% two-sided critical value is |r| ~ %.3f. Across %d tests "
      "roughly %d spurious hits at that threshold are expected BY CONSTRUCTION. "
      "A Bonferroni-style threshold would be |r| ~ %.3f. Treat anything below "
      "that as a hypothesis, not a finding, and prefer drivers with a mechanism."
      % (crit_r(70, 1.994), n_tests, int(0.05 * n_tests), crit_r(70, 4.6)))
    p("")

    for tgt in TARGETS:
        tser = cols[tgt]
        transforms = [
            ("LEVEL", tser, False),
            ("YoY %", yoy(tser, spine), True),
            ("QoQ diff", {k: tser[k] - tser[unkey(qkey(*k) - 1)]
                          for k in spine
                          if k in tser and unkey(qkey(*k) - 1) in tser}, False),
        ]
        for label, tvals, is_yoy in transforms:
            rows = []
            for c in safe:
                base = cols[c]
                if label == "YoY %":
                    dvals = yoy(base, spine)
                elif label == "QoQ diff":
                    dvals = {k: base[k] - base[unkey(qkey(*k) - 1)]
                             for k in spine
                             if k in base and unkey(qkey(*k) - 1) in base}
                else:
                    dvals = base
                bestrow = None
                for lag in (0, 1, 2, 3, 4):
                    xs, ys = [], []
                    for k in spine:
                        lk = unkey(qkey(*k) - lag)
                        xs.append(dvals.get(lk))
                        ys.append(tvals.get(k))
                    r, n = pearson(xs, ys)
                    if r is None or n < 12:
                        continue
                    if bestrow is None or abs(r) > abs(bestrow[0]):
                        bestrow = (r, n, lag)
                if bestrow:
                    rows.append((abs(bestrow[0]), bestrow[0], bestrow[1], bestrow[2], c))
            rows.sort(reverse=True)
            p("#### %s -- %s  (top 20 ex-ante drivers, best lag 0-4)" % (tgt, label))
            p("")
            p("| driver | best lag (q) | r | n | passes Bonferroni |")
            p("|---|---|---|---|---|")
            for _, r, n, lag, c in rows[:20]:
                bonf = "yes" if abs(r) >= crit_r(n, 4.6) else "no"
                eff = " (overlapping YoY: effective n ~ %d)" % max(4, n // 4) if is_yoy else ""
                p("| %s | %d | %+.3f | %d | %s%s |" % (c, lag, r, n, bonf, eff))
            p("")


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=DEFAULT_DATA)
    ap.add_argument("--out", default=None)
    ap.add_argument("--analysis", default=None,
                    help="write the correlation/coverage report to this path")
    args = ap.parse_args()
    out_dir = args.out or args.data

    print("Building Deere quarterly panel from %s" % args.data)
    spine, cal, windows, cols, colmeta, order = build(args.data)

    out_path = os.path.join(out_dir, "panel_quarterly.csv")
    header = emit(out_path, spine, cal, cols, order)

    print("")
    print("panel rows    : %d  (%s %s .. %s %s)"
          % (len(spine), spine[0][0], spine[0][1], spine[-1][0], spine[-1][1]))
    print("panel columns : %d  (3 identifiers + 3 targets + %d drivers)"
          % (len(header), len(header) - 6))
    print("forecast row  : %s %s  period_end %s  targets empty=%s"
          % (FORECAST_ROW[0], FORECAST_ROW[1], cal[FORECAST_ROW].isoformat(),
             all(cols[t].get(FORECAST_ROW) is None for t in TARGETS)))
    nfilled = sum(1 for c in order
                  if colmeta[c]["group"] not in ("target",)
                  and cols[c].get(FORECAST_ROW) is not None)
    ndriv = sum(1 for c in order if colmeta[c]["group"] != "target")
    print("forecast row  : %d of %d driver columns populated (%.0f%%)"
          % (nfilled, ndriv, 100.0 * nfilled / ndriv))
    print("written       : %s" % out_path)
    print("warnings      : %d" % len(WARNINGS))

    if args.analysis:
        with open(args.analysis, "w", encoding="utf-8") as fh:
            analyse(spine, cols, colmeta, order, fh)
        print("analysis      : %s" % args.analysis)

    # machine-readable column manifest for SCHEMA.md authoring
    man = os.path.join(out_dir, "panel_columns.csv")
    with open(man, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["column", "group", "units", "source_file", "n_obs",
                    "first_quarter", "last_quarter", "forecast_row_populated", "note"])
        for c in order:
            ks = [k for k in spine if cols[c].get(k) is not None]
            w.writerow([c, colmeta[c]["group"], colmeta[c]["units"],
                        colmeta[c]["source_file"], len(ks),
                        "%s %s" % ks[0] if ks else "",
                        "%s %s" % ks[-1] if ks else "",
                        "yes" if cols[c].get(FORECAST_ROW) is not None else "no",
                        colmeta[c]["note"]])
    print("manifest      : %s" % man)


if __name__ == "__main__":
    main()
