#!/usr/bin/env python3
"""
validate_drv_macro_fx.py -- independent cross-validation of drv_macro_fx.csv.

Each check recomputes a calendar-quarter series from a source that is NOT FRED
and compares it to the panel. Sources used:

  ECB Data Portal (data-api.ecb.europa.eu)  -> EUR/USD, and USD/INR as a cross
  Bank of Canada Valet API                  -> USD/CAD
  Banco Central do Brasil SGS API           -> USD/BRL (PTAX sell)
  US Bureau of Labor Statistics public API  -> CPI-U (CUSR0000SA0)
  FRED monthly aggregates FEDFUNDS / GS10   -> aggregation-convention check
  Deere SEC XBRL + offline filing corpus    -> fiscal calendar boundaries

Standard library only. No API keys.
"""

import csv
import datetime as dt
import json
import os
import re
import ssl
import subprocess
import time
import urllib.request

UA = "AgentsVsWallStreet cor@salomo.io"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache_macro_fx")
PANEL = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/drv_macro_fx.csv"
CORPUS = ("/Users/cor/Documents/projects/agents-vs-wall-street-starter/"
          "challenge/offline-data/deere")

os.makedirs(CACHE, exist_ok=True)
_SSL = ssl.create_default_context()
RESULTS = []


def fetch(url, fname, tries=3):
    path = os.path.join(CACHE, fname)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return open(path, "rb").read()
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90, context=_SSL) as r:
                data = r.read()
            open(path, "wb").write(data)
            return data
        except Exception as e:                                    # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise last


def add_months(d, n):
    y, m = divmod((d.year * 12 + d.month - 1) + n, 12)
    return dt.date(y, m + 1, 1)


def load_panel():
    """series_id -> {(fy,fq): value}, calendar-grid rows only, full periods only."""
    out = {}
    with open(PANEL) as fh:
        for r in csv.DictReader(fh):
            if r["series_id"].endswith("_dfq") or "_dfq" in r["series_id"]:
                continue
            if "PARTIAL PERIOD" in r["notes"]:
                continue
            if r["value"] == "":
                continue
            out.setdefault(r["series_id"], {})[(int(r["fiscal_year"]),
                                                r["fiscal_quarter"])] = float(r["value"])
    return out


def to_quarters(daily):
    """[(date,value)] -> {(year,'Qn'): mean}."""
    buckets = {}
    for d, v in daily:
        key = (d.year, "Q%d" % ((d.month - 1) // 3 + 1))
        buckets.setdefault(key, []).append(v)
    return {k: sum(v) / len(v) for k, v in buckets.items()}


def compare(name, panel_series, ref, src_label, tol, mode="pct"):
    """Compare two {(y,q):value} dicts on their shared keys.

    mode="pct" -> relative % difference (levels: FX, index numbers)
    mode="abs" -> absolute difference in the series' own units. Required for
                  interest rates: a 0.003pp gap on a 0.077% ZIRP-era policy rate
                  is a 3.9% *relative* gap but is economically nil.
    """
    keys = sorted(set(panel_series) & set(ref))
    if not keys:
        RESULTS.append((name, src_label, 0, None, None, "NO OVERLAP", [], mode))
        return
    diffs = []
    for k in keys:
        a, b = panel_series[k], ref[k]
        if mode == "abs":
            diffs.append((abs(a - b), k, a, b))
        else:
            if b == 0:
                continue
            diffs.append((abs(a - b) / abs(b) * 100.0, k, a, b))
    diffs.sort(reverse=True)
    mean_d = sum(d[0] for d in diffs) / len(diffs)
    max_d = diffs[0][0]
    verdict = "AGREE" if max_d <= tol else "DISCREPANCY"
    RESULTS.append((name, src_label, len(diffs), mean_d, max_d, verdict,
                    diffs[:3], mode))


# ------------------------------------------------------------------ 1. ECB FX

def ecb(series_key, tag):
    """Fetch in 4-year chunks -- a single 20-year request times out on the ECB API."""
    out = []
    for lo in range(2006, 2027, 4):
        hi = min(lo + 3, 2026)
        url = ("https://data-api.ecb.europa.eu/service/data/EXR/%s?format=csvdata"
               "&startPeriod=%d-01-01&endPeriod=%d-12-31" % (series_key, lo, hi))
        try:
            raw = fetch(url, "ecb_%s_%d.csv" % (tag, lo)).decode("utf-8")
        except Exception as e:                                    # noqa: BLE001
            print("  [ecb %s %d] %s" % (tag, lo, e))
            continue
        for r in csv.DictReader(raw.strip().splitlines()):
            v = (r.get("OBS_VALUE") or "").strip()
            if not v or v == "NaN":
                continue
            out.append((dt.date.fromisoformat(r["TIME_PERIOD"]), float(v)))
    out.sort()
    return out


def check_ecb_eurusd(panel):
    d = ecb("D.USD.EUR.SP00.A", "usd_eur")
    compare("fx_eur_usd", panel["fx_eur_usd"], to_quarters(d),
            "ECB reference rate USD/EUR (data-api.ecb.europa.eu)", 0.5)
    return d


def check_ecb_usdinr(panel, usd_eur):
    """ECB publishes INR/EUR; USD/INR = (INR per EUR) / (USD per EUR)."""
    inr_eur = dict(ecb("D.INR.EUR.SP00.A", "inr_eur"))
    ue = dict(usd_eur)
    cross = [(d, inr_eur[d] / ue[d]) for d in sorted(set(inr_eur) & set(ue)) if ue[d]]
    compare("fx_usd_inr", panel["fx_usd_inr"], to_quarters(cross),
            "ECB cross: (INR/EUR)/(USD/EUR), independent of Fed H.10", 0.6)


# ------------------------------------------------------- 2. Bank of Canada CAD

def check_boc(panel):
    url = ("https://www.bankofcanada.ca/valet/observations/FXUSDCAD/csv"
           "?start_date=2006-01-01&end_date=2026-08-16")
    raw = fetch(url, "boc_usdcad.csv").decode("utf-8")
    lines = raw.splitlines()
    try:
        i = next(n for n, l in enumerate(lines) if l.strip().strip('"') == "OBSERVATIONS")
    except StopIteration:
        RESULTS.append(("fx_usd_cad", "Bank of Canada Valet", 0, None, None,
                        "SOURCE FORMAT UNRECOGNISED", [], "pct"))
        return
    out = []
    for r in csv.DictReader(lines[i + 1:]):
        v = (r.get("FXUSDCAD") or "").strip()
        if not v:
            continue
        try:
            out.append((dt.date.fromisoformat(r["date"].strip()), float(v)))
        except ValueError:
            continue
    compare("fx_usd_cad", panel["fx_usd_cad"], to_quarters(out),
            "Bank of Canada Valet FXUSDCAD daily average", 0.5)


# ------------------------------------------------------------- 3. BCB BRL PTAX

def check_bcb(panel):
    out = []
    for yr in range(2006, 2027):
        url = ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json"
               "&dataInicial=01/01/%d&dataFinal=31/12/%d" % (yr, yr))
        try:
            raw = fetch(url, "bcb_usdbrl_%d.json" % yr).decode("utf-8")
            for rec in json.loads(raw):
                d = dt.datetime.strptime(rec["data"], "%d/%m/%Y").date()
                out.append((d, float(rec["valor"])))
        except Exception as e:                                    # noqa: BLE001
            print("  [bcb %d] %s" % (yr, e))
    if not out:
        RESULTS.append(("fx_usd_brl", "BCB SGS", 0, None, None,
                        "FETCH FAILED", [], "pct"))
        return
    compare("fx_usd_brl", panel["fx_usd_brl"], to_quarters(out),
            "Banco Central do Brasil SGS series 1 (PTAX sell)", 0.6)


# ----------------------------------------------------------------- 4. BLS CPI

def check_bls(panel):
    """BLS bulk flat file -- the full published CPI history.

    NOTE: the public API v1 endpoint silently returns only the most recent ~3
    years for unregistered callers, ignoring startyear/endyear, which is why the
    bulk file is used instead.
    """
    raw = fetch("https://download.bls.gov/pub/time.series/cu/cu.data.0.Current",
                "bls_cu_current.txt").decode("utf-8", "replace")
    obs = []
    for line in raw.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) < 4 or parts[0].strip() != "CUSR0000SA0":
            continue
        per = parts[2].strip()
        if not per.startswith("M") or per == "M13":
            continue
        try:
            obs.append((dt.date(int(parts[1]), int(per[1:]), 1),
                        float(parts[3].strip())))
        except ValueError:
            continue
    if not obs:
        RESULTS.append(("us_cpi", "BLS bulk flat file", 0, None, None,
                        "FETCH FAILED", [], "pct"))
        return
    compare("us_cpi", panel["us_cpi"], to_quarters(obs),
            "BLS bulk file cu.data.0.Current, series CUSR0000SA0 (CPI-U SA)", 0.1)


# ------------------------------------- 5/6. FRED monthly aggregation convention

def fred_monthly(sid):
    url = ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s"
           "&cosd=2006-01-01&coed=2026-08-16" % sid)
    raw = fetch(url, "fred_%s.csv" % sid).decode("utf-8")
    out = []
    for r in list(csv.reader(raw.strip().splitlines()))[1:]:
        if len(r) < 2 or r[1].strip() in (".", "", "NA"):
            continue
        out.append((dt.date.fromisoformat(r[0].strip()), float(r[1])))
    return out


def check_monthly_agg(panel):
    # FEDFUNDS / GS10 are FRED's own monthly averages of the same daily data.
    # Averaging them to quarters should reproduce our daily-average quarters.
    compare("us_fed_funds_rate", panel["us_fed_funds_rate"],
            to_quarters(fred_monthly("FEDFUNDS")),
            "FRED FEDFUNDS monthly average, re-aggregated to quarters",
            0.05, mode="abs")
    compare("us_10y_treasury", panel["us_10y_treasury"],
            to_quarters(fred_monthly("GS10")),
            "FRED GS10 monthly average, re-aggregated to quarters",
            0.05, mode="abs")


# --------------------------------- 6b. GDP growth rebuilt from the level series

def check_gdp(panel):
    """A191RL1Q225SBEA is BEA's published growth rate. Rebuild it independently
    from the real GDP LEVEL series (GDPC1) as ((L_t/L_t-1)^4 - 1)*100 and check
    the two agree. This validates that the panel's quarter mapping is right --
    FRED dates quarterly observations at the quarter START, and an off-by-one
    here would silently shift every GDP observation by a quarter."""
    lv = fred_monthly("GDPC1")            # quarterly, dated at quarter start
    ref = {}
    for (d0, v0), (d1, v1) in zip(lv, lv[1:]):
        if v0 <= 0:
            continue
        ref[(d1.year, "Q%d" % ((d1.month - 1) // 3 + 1))] = ((v1 / v0) ** 4 - 1) * 100
    compare("us_gdp_growth", panel["us_gdp_growth"], ref,
            "rebuilt from FRED GDPC1 real GDP level: ((L_t/L_t-1)^4-1)*100",
            0.15, mode="abs")


# ------------------------------------------- 7. Deere fiscal calendar vs corpus

def check_fiscal_calendar():
    """The fiscal grid came from SEC XBRL. Confirm the recent period-end dates
    independently against the offline filing corpus."""
    expect = ["May 3, 2026", "February 1, 2026", "November 2, 2025",
              "July 27, 2025", "April 27, 2025", "January 26, 2025"]
    corpus_text = []
    for root, _dirs, files in os.walk(CORPUS):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                    corpus_text.append((fp, fh.read()))
            except (OSError, UnicodeError):
                continue
    found, missing = [], []
    for phrase in expect:
        hits = [fp for fp, t in corpus_text if phrase in t]
        (found if hits else missing).append((phrase, len(hits)))
    verdict = "AGREE" if not missing else "PARTIAL"
    RESULTS.append(("deere_fiscal_calendar",
                    "offline filing corpus (%d docs, literal date match)"
                    % len(corpus_text),
                    len(found), None, None, verdict,
                    [(0, p, n, "files") for p, n in found], "cal"))
    return found, missing


def main():
    panel = load_panel()
    print("panel: %d calendar series loaded\n" % len(panel))

    def guard(label, fn, *a):
        try:
            return fn(*a)
        except Exception as e:                                    # noqa: BLE001
            print("  [%s] FAILED: %s" % (label, e))
            RESULTS.append((label, "source unreachable", 0, None, None,
                            "SOURCE UNAVAILABLE: %s" % e, [], "pct"))
            return None

    usd_eur = guard("fx_eur_usd", check_ecb_eurusd, panel) or []
    if usd_eur:
        guard("fx_usd_inr", check_ecb_usdinr, panel, usd_eur)
    guard("fx_usd_cad", check_boc, panel)
    guard("fx_usd_brl", check_bcb, panel)
    guard("us_cpi", check_bls, panel)
    guard("rates_agg", check_monthly_agg, panel)
    guard("us_gdp_growth", check_gdp, panel)
    fc = guard("deere_fiscal_calendar", check_fiscal_calendar)
    found, missing = fc if fc else ([], [])

    print("\n" + "=" * 100)
    print("CROSS-VALIDATION: panel vs independent source (calendar quarters, full periods only)")
    print("=" * 100)
    for name, src, n, mean_d, max_d, verdict, worst, mode in RESULTS:
        unit = "pp" if mode == "abs" else "%"
        md = "n/a" if mean_d is None else "%.4f%s" % (mean_d, unit)
        xd = "n/a" if max_d is None else "%.4f%s" % (max_d, unit)
        print("\n%-22s %s\n  source : %s\n  n=%-4d mean|diff|=%-10s max|diff|=%-10s -> %s"
              % (name, "", src, n, md, xd, verdict))
        for w in worst:
            if name == "deere_fiscal_calendar":
                print("      %s matched in %d %s" % (w[1], w[2], w[3]))
            else:
                print("      worst %s%s: panel=%.6f ref=%.6f (%.4f%s)"
                      % (w[1][0], w[1][1], w[2], w[3], w[0], unit))
    if missing:
        print("\n  fiscal dates NOT found in corpus: %s" % [m[0] for m in missing])
    print()


if __name__ == "__main__":
    main()
