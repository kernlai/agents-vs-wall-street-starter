#!/usr/bin/env python3
"""
Build drv_steel_inputs.csv -- 20 years (2006-2026) of steel / input-cost drivers for
Deere & Company (DE), plus the Deere gross-margin series needed to estimate the
steel -> cost-of-sales pass-through lag.

Sources (all keyless):
  * FRED CSV download      https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>
  * BLS public API v1      https://api.bls.gov/publicAPI/v1/timeseries/data/   (cross-check)
  * SEC EDGAR XBRL         https://data.sec.gov/api/xbrl/companyfacts/CIK0000315189.json
  * Offline Deere corpus   challenge/offline-data/deere/filings/*.md

Standard library only.  Usage:  python3 build_drv_steel_inputs.py
"""
import csv
import datetime as dt
import json
import os
import ssl
import sys
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from de_corpus_income import collect as corpus_collect, month_to_fiscal_qtr, fiscal_qtr_from_end  # noqa: E402

OUT_CSV = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/drv_steel_inputs.csv"
CACHE = os.environ.get("DRV_CACHE", "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad")
UA = "AgentsVsWallStreet cor@salomo.io"
START_YEAR = 2006
CTX = ssl.create_default_context()

HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "value",
          "units", "source_type", "source", "notes"]


# ------------------------------------------------------------------ fetch utils
def http_get(url, binary=False):
    key = os.path.join(CACHE, "cache_" + "".join(c if c.isalnum() else "_" for c in url)[-150:])
    if os.path.exists(key):
        return open(key, "rb").read() if binary else open(key, "r", encoding="utf-8").read()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90, context=CTX) as r:
        data = r.read()
    with open(key, "wb") as fh:
        fh.write(data)
    return data if binary else data.decode("utf-8", "replace")


def fred_monthly(series):
    """Return {(year, month): value} averaging any sub-monthly observations."""
    txt = http_get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + series)
    buckets = {}
    for i, line in enumerate(txt.strip().split("\n")):
        if i == 0:
            continue
        parts = line.split(",")
        if len(parts) < 2:
            continue
        d, v = parts[0], parts[1].strip()
        if v in ("", "."):
            continue
        date = dt.date.fromisoformat(d)
        buckets.setdefault((date.year, date.month), []).append(float(v))
    return {k: sum(v) / len(v) for k, v in buckets.items()}


# ------------------------------------------------------------------ series spec
# series_id, FRED id, units, note
SPEC = [
    ("px_steel_hrc", "WPU101704", "index",
     "BLS PPI commodity WPU101704 Hot rolled steel bars, plates and structural shapes, NSA, 1982=100. "
     "SUBSTITUTION: no keyless USD/ton HRC coil spot price exists; see companion .md. This long/plate "
     "index is the closest continuous hot-rolled series and is arguably the better proxy for Deere's "
     "frame/axle/plate steel buy."),
    ("px_steel_hrc_sheet", "WPU101703", "index",
     "BLS PPI WPU101703 Hot rolled steel SHEET and strip incl tin mill, NSA, 1982=100. "
     "DISCONTINUED by BLS after 2022-02 -- series ends there, do not treat the gap as zero."),
    ("px_steel_cold_rolled", "WPU101707", "index",
     "BLS PPI WPU101707 Cold rolled steel sheet and strip, NSA, 1982=100. Continuous 1982-2026; "
     "use as the flat-rolled proxy after WPU101703 was discontinued."),
    ("px_steel_scrap", "WPU1012", "index",
     "BLS PPI WPU1012 Iron and steel scrap, NSA, 1982=100."),
    ("px_steel_scrap_carbon", "WPU101211", "index",
     "BLS PPI WPU101211 Carbon steel scrap, NSA, 1986-12=100."),
    ("ppi_steel_mill_products", "WPU1017", "index",
     "BLS PPI WPU1017 Steel mill products, NSA, 1982=100."),
    ("ppi_ag_machinery", "WPU111", "index",
     "BLS PPI WPU111 Agricultural machinery and equipment, NSA, 1982=100. Output-price proxy: "
     "Deere's own realised pricing tracks this closely."),
    ("ppi_ag_machinery_industry", "PCU333111333111", "index",
     "BLS PPI NAICS 333111 Farm machinery and equipment manufacturing, NSA, Dec 1983=100. "
     "Independent construction of the same concept as ppi_ag_machinery -- use as a cross-check."),
    ("px_aluminium", "PALUMUSDM", "USD/mt",
     "IMF/World Bank global price of aluminum, LME cash, USD per metric ton, monthly average."),
    ("px_copper", "PCOPPUSDM", "USD/mt",
     "IMF global price of copper, grade A cathode LME, USD per metric ton, monthly average."),
    ("px_rubber", "PRUBBUSDM", "UScents/lb",
     "IMF global price of natural rubber (No.1 RSS, Singapore/Malaysia), US cents per pound. "
     "UNITS ARE CENTS/LB, not USD/ton."),
    ("px_rubber_synthetic_ppi", "WPU071102", "index",
     "BLS PPI WPU071102 Synthetic rubber, NSA, 1982=100. Closer to Deere's actual tyre/seal input "
     "cost basis than the natural-rubber spot price."),
    ("px_diesel", "GASDESW", "USD/gal",
     "EIA US No.2 diesel retail price, all types, USD per gallon; weekly observations averaged to "
     "the month then to the quarter."),
    ("px_diesel_ppi", "WPU057303", "index",
     "BLS PPI WPU057303 No.2 diesel fuel, NSA, 1982=100. Producer-level diesel, better matched to "
     "Deere's freight/plant energy cost than the retail pump price."),
    ("idx_freight", "PCU484121484121", "index",
     "BLS PPI NAICS 484121 General freight trucking, long-distance truckload, NSA, Dec 2003=100. "
     "Primary domestic freight cost index; covers the whole 2006-2026 window."),
    ("idx_freight_drybulk", "IGREA", "index",
     "Kilian Index of Global Real Economic Activity, built from global dry-bulk ocean freight rates. "
     "Deviation-from-trend index: CAN BE NEGATIVE and has no natural zero. Do not log-transform."),
    ("px_iron_ore", "PIORECRUSDM", "USD/dmt",
     "IMF/World Bank global price of iron ore, China import 62% Fe spot, USD per dry metric ton. "
     "Upstream driver that leads the steel PPIs."),
]


# ------------------------------------------------------------------ fiscal calendar
def build_fiscal_calendar(facts, corpus):
    """{(fy, 'Qn'): period_end ISO date} for Deere, 2006 -> 2026.

    Precedence: (1) period end printed on the corpus filing itself, (2) most frequently
    occurring three-month XBRL context end for that slot, (3) pre-2016 calendar month-end
    rule, (4) forward projection for the unreported FY2026 Q3/Q4.
    """
    ends = []
    for concept in ("Revenues", "SalesRevenueGoodsNet", "GrossProfit", "CostOfGoodsSold",
                    "ResearchAndDevelopmentExpense"):
        node = facts["facts"]["us-gaap"].get(concept)
        if not node:
            continue
        for x in node["units"].get("USD", []):
            s = x.get("start")
            if not s:
                continue
            n = (dt.date.fromisoformat(x["end"]) - dt.date.fromisoformat(s)).days
            if 80 <= n <= 100:
                ends.append(x["end"])
    tally = {}
    for e in ends:
        d = dt.date.fromisoformat(e)
        fy, fq = fiscal_qtr_from_end(d)
        if fy and START_YEAR <= fy <= 2026:
            tally.setdefault((fy, fq), {}).setdefault(e, 0)
            tally[(fy, fq)][e] += 1
    cal = {slot: max(c.items(), key=lambda kv: (kv[1], kv[0]))[0] for slot, c in tally.items()}
    # corpus filings win: the period end is printed on the face of the statement
    for (fy, fq), r in corpus.items():
        cal[(fy, fq)] = r["period_end"]
    # Pre-EDGAR years: Deere used calendar month-ends through FY2016.
    for fy in range(START_YEAR, 2010):
        for fq, (m, day) in zip(("Q1", "Q2", "Q3", "Q4"),
                                ((1, 31), (4, 30), (7, 31), (10, 31))):
            cal.setdefault((fy, fq), dt.date(fy, m, day).isoformat())
    # FY2026 Q3/Q4 have NOT been reported (today is 2026-08-16). Project on the 13-week
    # cadence from the corpus-confirmed FY2026 Q2 end of 2026-05-03.
    cal[(2026, "Q3")] = "2026-08-02"
    cal[(2026, "Q4")] = "2026-11-01"
    return cal


def corpus_quarters():
    """{(fy, 'Qn'): record} from the offline corpus, quarterly statements only."""
    out, dupes_ok, dupes_bad = {}, 0, []
    for _key, recs in corpus_collect().items():
        recs = [r for r in recs if r["period_kind"] == "quarter"]
        if not recs:
            continue
        vals = {(r["net_sales"], r["cost_of_sales"]) for r in recs}
        if len(vals) > 1:
            dupes_bad.append((recs[0]["period_end"], sorted(vals)))
        elif len(recs) > 1:
            dupes_ok += 1
        r = recs[0]
        out[(r["fiscal_year"], r["fiscal_quarter"])] = r
    return out, dupes_ok, dupes_bad


def cal_quarter_end(y, q):
    return {1: dt.date(y, 3, 31), 2: dt.date(y, 6, 30),
            3: dt.date(y, 9, 30), 4: dt.date(y, 12, 31)}[q].isoformat()


# ------------------------------------------------------------------ aggregation
def to_quarters(monthly, fiscal, cal):
    """Aggregate {(y,m): v} to quarterly means. Returns {(fy, 'Qn'): (mean, n_months)}."""
    buckets = {}
    for (y, m), v in monthly.items():
        if fiscal:
            fy, fq = month_to_fiscal_qtr(y, m)
        else:
            fy, fq = y, "Q%d" % ((m - 1) // 3 + 1)
        buckets.setdefault((fy, fq), []).append(v)
    return {k: (sum(v) / len(v), len(v)) for k, v in buckets.items()}


# ------------------------------------------------------------------ Deere margin
def deere_margin_rows(facts, cal, corpus):
    """Quarterly Net sales / Cost of sales / Gross profit / Gross margin.

    Corpus filings are authoritative FY2015 Q1 -> FY2026 Q2.
    EDGAR XBRL backfills FY2009 -> FY2014 and independently validates the overlap.
    """
    # --- EDGAR three-month facts
    def q3(concept):
        out = {}
        node = facts["facts"]["us-gaap"].get(concept)
        if not node:
            return out
        for x in node["units"].get("USD", []):
            s = x.get("start")
            if not s:
                continue
            n = (dt.date.fromisoformat(x["end"]) - dt.date.fromisoformat(s)).days
            if 80 <= n <= 100:
                out.setdefault(x["end"], []).append(x["val"])
        # keep the ORIGINAL as-filed value (smallest |restatement| ambiguity is flagged separately)
        return out

    e_ns, e_cs, e_gp = q3("SalesRevenueGoodsNet"), q3("CostOfGoodsSold"), q3("GrossProfit")

    rows, validation = [], []
    for (fy, fq), pe in sorted(cal.items(), key=lambda kv: kv[1]):
        c = corpus.get((fy, fq))
        ns = cs = None
        src, stype, note = None, None, ""
        if c:
            ns, cs = c["net_sales"], c["cost_of_sales"]
            src, stype = c["source"], "filing"
            note = "As reported in the quarterly earnings release / 10-Q consolidated income statement."
        else:
            cand_ns = e_ns.get(pe)
            cand_cs = e_cs.get(pe)
            cand_gp = e_gp.get(pe)
            src = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000315189.json"
            stype = "api"
            if cand_ns and cand_cs:
                ns, cs = min(cand_ns) / 1e6, min(cand_cs) / 1e6
                note = ("SEC XBRL us-gaap:SalesRevenueGoodsNet / us-gaap:CostOfGoodsSold, "
                        "three-month duration context. Pre-corpus backfill.")
            elif cand_ns and cand_gp:
                # Deere did not tag a three-month CostOfGoodsSold for most Q4 periods;
                # reconstruct it from the tagged GrossProfit.
                ns = min(cand_ns) / 1e6
                cs = ns - min(cand_gp) / 1e6
                note = ("SEC XBRL us-gaap:SalesRevenueGoodsNet and us-gaap:GrossProfit, three-month "
                        "duration context. Cost of sales RECONSTRUCTED as net sales - gross profit "
                        "because Deere did not tag a three-month CostOfGoodsSold for this quarter.")
                cand_cs = None
            if ns is not None:
                if (cand_ns and len(set(cand_ns)) > 1) or (cand_cs and len(set(cand_cs)) > 1) \
                        or (cand_gp and len(set(cand_gp)) > 1):
                    note += (" RESTATEMENT: more than one XBRL value exists for this period "
                             "(Deere reclassified non-service pension cost under ASU 2017-07); "
                             "the lower/earliest-filed value is used.")
        if ns is None or cs is None:
            continue
        gp = ns - cs
        gm = 100.0 * gp / ns

        # independent check against separately tagged us-gaap:GrossProfit
        if pe in e_gp:
            xg = min(e_gp[pe]) / 1e6
            validation.append((pe, gp, xg, abs(gp - xg)))

        for sid, val, units in (("de_net_sales_equipment", ns, "USDm"),
                                ("de_cost_of_sales", cs, "USDm"),
                                ("de_gross_profit_equipment", gp, "USDm"),
                                ("de_gross_margin_equipment", gm, "percent")):
            n = note
            if sid == "de_gross_profit_equipment":
                n = "Derived = de_net_sales_equipment - de_cost_of_sales. " + note
            if sid == "de_gross_margin_equipment":
                n = ("Derived = 100 * (net sales - cost of sales) / net sales. Equipment-operations "
                     "basis: excludes Financial Services revenue and Other income. " + note)
            rows.append([sid, pe, fy, fq, round(val, 4), units, stype, src, n])
    return rows, validation


# ------------------------------------------------------------------ BLS cross-check
def bls_check(fred_monthlies):
    """Independently re-pull a handful of PPI series from BLS and compare with FRED."""
    ids = ["WPU101704", "WPU1017", "WPU111", "WPU1012", "WPU101707"]
    body = json.dumps({"seriesid": ids, "startyear": "2016", "endyear": "2025"}).encode()
    req = urllib.request.Request("https://api.bls.gov/publicAPI/v1/timeseries/data/", data=body,
                                 headers={"Content-Type": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=90, context=CTX) as r:
            d = json.loads(r.read())
    except Exception as exc:                                   # pragma: no cover
        return [("BLS API unavailable", str(exc), None, None)]
    out = []
    for s in d.get("Results", {}).get("series", []):
        sid = s["seriesID"]
        fm = fred_monthlies.get(sid, {})
        n = worst = 0
        worst_at = None
        for obs in s["data"]:
            if obs["period"][0] != "M":
                continue
            k = (int(obs["year"]), int(obs["period"][1:]))
            if k in fm:
                diff = abs(float(obs["value"]) - fm[k])
                n += 1
                if diff > worst:
                    worst, worst_at = diff, k
        out.append((sid, n, worst, worst_at))
    return out


# ------------------------------------------------------------------ main
def main():
    facts = json.loads(http_get(
        "https://data.sec.gov/api/xbrl/companyfacts/CIK0000315189.json"))
    corpus, dupes_ok, dupes_bad = corpus_quarters()
    cal = build_fiscal_calendar(facts, corpus)

    rows = []
    monthlies = {}
    coverage = []
    for sid, fred_id, units, note in SPEC:
        m = fred_monthly(fred_id)
        monthlies[fred_id] = m
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + fred_id
        for fiscal in (True, False):
            agg = to_quarters(m, fiscal, cal)
            out_id = sid if fiscal else sid + "_cq"
            basis = ("Deere fiscal quarter (FQ1=Nov-Dec-Jan, FQ2=Feb-Mar-Apr, FQ3=May-Jun-Jul, "
                     "FQ4=Aug-Sep-Oct); period_end is Deere's actual fiscal quarter end."
                     if fiscal else
                     "CALENDAR quarter basis; period_end is the calendar quarter end. Duplicate of "
                     "the fiscal-basis series on a different alignment -- pick one, do not use both.")
            n_out = 0
            for (fy, fq) in sorted(agg):
                if fy < START_YEAR or fy > 2026:
                    continue
                val, nmon = agg[(fy, fq)]
                if fiscal:
                    pe = cal.get((fy, fq))
                    if pe is None:
                        continue
                else:
                    pe = cal_quarter_end(fy, int(fq[1]))
                if pe > "2026-08-14":
                    continue  # corpus freeze date: nothing published after this
                if nmon < 2:
                    continue  # a one-month "quarter" average is not comparable; drop it
                n = note + " " + basis
                if nmon < 3:
                    n += (" PARTIAL QUARTER: mean of %d of 3 monthly observations." % nmon)
                rows.append([out_id, pe, fy, fq, round(val, 4), units, "api", url, n])
                n_out += 1
            if fiscal:
                got = [r for r in rows if r[0] == out_id]
                coverage.append((sid, fred_id, units, got[0][1] if got else None,
                                 got[-1][1] if got else None, len(got)))

    m_rows, validation = deere_margin_rows(facts, cal, corpus)
    rows.extend(m_rows)

    rows.sort(key=lambda r: (r[0], r[1]))
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(rows)

    # ---------------- diagnostics
    print("rows written: %d -> %s" % (len(rows), OUT_CSV))
    print("\n-- fiscal-basis coverage --")
    for c in coverage:
        print("  %-28s %-16s %-12s %s .. %s  n=%d" % c)
    print("\n-- Deere margin series --")
    gm = [r for r in rows if r[0] == "de_gross_margin_equipment"]
    print("  n=%d  %s .. %s   filing=%d api=%d"
          % (len(gm), gm[0][1], gm[-1][1],
             sum(1 for r in gm if r[6] == "filing"), sum(1 for r in gm if r[6] == "api")))
    print("\n-- VALIDATION 1: corpus 8-K vs 10-Q, same quarter --")
    print("  quarters with 2+ independent corpus documents agreeing exactly: %d" % dupes_ok)
    print("  disagreements: %d %s" % (len(dupes_bad), dupes_bad if dupes_bad else ""))
    print("\n-- VALIDATION 2: derived gross profit vs SEC XBRL us-gaap:GrossProfit --")
    if validation:
        mx = max(validation, key=lambda t: t[3])
        big = [v for v in validation if v[3] > 1.0]
        print("  compared n=%d quarters; max abs diff = %.3f USDm at %s (derived %.1f vs XBRL %.1f)"
              % (len(validation), mx[3], mx[0], mx[1], mx[2]))
        print("  quarters differing by > 1.0 USDm: %d %s"
              % (len(big), [(b[0], round(b[3], 2)) for b in big]))
    print("\n-- VALIDATION 3: FRED vs BLS public API (same PPI ids, 2016-2025) --")
    for r in bls_check(monthlies):
        print("   ", r)
    print("\n-- VALIDATION 4: FRED PPI ag-machinery, commodity vs NAICS construction --")
    a = to_quarters(monthlies["WPU111"], True, cal)
    b = to_quarters(monthlies["PCU333111333111"], True, cal)
    common = sorted(set(a) & set(b))
    common = [k for k in common if k[0] >= 2006]
    ga = [a[k][0] for k in common]
    gb = [b[k][0] for k in common]
    print("    n=%d  corr(levels)=%.4f" % (len(common), pearson(ga, gb)))


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / (sxx * syy) ** 0.5 if sxx and syy else float("nan")


if __name__ == "__main__":
    main()
