#!/usr/bin/env python3
"""
Build data/deere/footprint/exports_trade.csv for the Deere (NYSE: DE)
manufacturing-footprint work.

Inputs
  1. comtrade_raw.jsonl  -- output of de_fetch_comtrade_machinery.py
  2. partnerAreas.json   -- Comtrade partner reference (code -> name)
  3. corpus_rows.csv     -- hand-extracted rows from the Deere filing corpus and
                            from dated public trade-policy sources, each already
                            carrying its own source string
  4. de_geo_matrix.csv   -- Deere quarterly revenue by geography (built upstream),
                            used only for the correlation diagnostic, not copied
                            into the output

Output: tidy long CSV with the fixed 13-column header.

IMPORTANT INTERPRETATION NOTE, carried into the notes column of every HS row:
these HS codes measure the WHOLE US industry, not Deere. AGCO, CNH, Caterpillar,
Kubota, Vermeer, Great Plains and every other US-based exporter sit in the same
series. Treat it as a sector proxy.
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict

HEADER = [
    "series_id", "date", "plant", "city", "state_or_region", "country", "segment",
    "metric", "value", "units", "source_type", "source", "notes",
]

HS_LABEL = {
    "8432": "agricultural/horticultural/forestry soil preparation machinery",
    "8433": "harvesting and threshing machinery",
    "8701": "tractors",
    "8429": "self-propelled construction machinery",
}

SECTOR_CAVEAT = ("whole-industry HS flow, NOT Deere-only; includes AGCO, CNH, "
                 "Caterpillar, Kubota and all other US exporters")

COMTRADE_SRC = "UN Comtrade public preview API (comtradeapi.un.org), reporter=USA(842)"

# EU-27 M49 codes. Comtrade reports France as 251 and sometimes 250
# (Metropolitan France); both are included and de-duplicated by summation.
EU27 = {
    40, 56, 100, 191, 196, 203, 208, 233, 246, 250, 251, 276, 300, 348, 372,
    380, 428, 440, 442, 470, 528, 616, 620, 642, 703, 705, 724, 752,
}

# Destinations broken out individually in the output.
FOCUS_PARTNERS = {
    124: ("Canada", "Canada"),
    484: ("Mexico", "Mexico"),
    76: ("Brazil", "Brazil"),
    276: ("Germany", "Germany"),
    36: ("Australia", "Australia"),
    32: ("Argentina", "Argentina"),
    826: ("United Kingdom", "United Kingdom"),
    156: ("China", "China"),
}


def month_to_date(period):
    """'202405' -> '2024-05-31'-ish; we use the first day for a stable key."""
    y, m = int(period[:4]), int(period[4:6])
    return "%04d-%02d-01" % (y, m)


def load_partner_names(path):
    names = {}
    if not os.path.exists(path):
        return names
    for x in json.load(open(path)).get("results", []):
        names[x["PartnerCode"]] = x["PartnerDesc"]
    return names


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None, n
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0 or syy <= 0:
        return None, n
    return sxy / math.sqrt(sxx * syy), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comtrade", required=True)
    ap.add_argument("--partners", required=True)
    ap.add_argument("--corpus-rows", required=True)
    ap.add_argument("--geo-matrix", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--diag", required=True, help="where to write correlation diagnostics")
    args = ap.parse_args()

    pnames = load_partner_names(args.partners)
    raw = [json.loads(l) for l in open(args.comtrade) if l.strip()]

    # Keep only the true aggregate row. Some reporters (Brazil, India) return the
    # same reporter/partner/period/commodity several times, split by customs
    # procedure (customsCode), mode of transport (motCode), mode of supply
    # (mosCode) and second partner. The total carries C00 / 0 / "0" / 0; the rest
    # are partial breakdowns that would otherwise be double counted and, worse,
    # could be silently mistaken for the total. US responses only ever contain the
    # aggregate, so this filter is a no-op there.
    recs = [r for r in raw
            if (r.get("customsCode") in (None, "C00")
                and r.get("motCode") in (None, 0)
                and r.get("mosCode") in (None, "0")
                and r.get("partner2Code") in (None, 0))]
    sys.stderr.write("comtrade records: %d raw -> %d aggregate-only\n"
                     % (len(raw), len(recs)))

    rows = []

    # ---------- 1. US monthly world totals -------------------------------
    monthly = defaultdict(dict)  # hs -> period -> value
    for r in recs:
        if r["reporter"] == "USA" and r["freq"] == "M" and r["scope"] == "world" \
                and r["flow"] == "X" and r["partnerCode"] == 0:
            if r["value_usd"] is not None:
                monthly[r["hs"]][r["period"]] = r["value_usd"]

    for hs in sorted(monthly):
        for period in sorted(monthly[hs]):
            rows.append({
                "series_id": "us_exports_hs%s" % hs,
                "date": month_to_date(period),
                "plant": "", "city": "", "state_or_region": "",
                "country": "United States",
                "segment": "",
                "metric": "exports_fob_monthly",
                "value": "%.0f" % monthly[hs][period],
                "units": "USD",
                "source_type": "trade-data",
                "source": COMTRADE_SRC,
                "notes": "HS %s (%s); destination=World; %s" % (hs, HS_LABEL[hs], SECTOR_CAVEAT),
            })

    # ---------- 2. US annual by destination -------------------------------
    annual = defaultdict(lambda: defaultdict(dict))  # hs -> year -> partner -> value
    for r in recs:
        if r["reporter"] == "USA" and r["freq"] == "A" and r["scope"] == "partners" \
                and r["flow"] == "X":
            if r["value_usd"] is not None:
                annual[r["hs"]][r["period"]][r["partnerCode"]] = r["value_usd"]

    for hs in sorted(annual):
        for year in sorted(annual[hs]):
            pmap = annual[hs][year]
            date = "%s-12-31" % year

            world = pmap.get(0)
            if world is not None:
                rows.append({
                    "series_id": "us_exports_hs%s" % hs, "date": date,
                    "plant": "", "city": "", "state_or_region": "",
                    "country": "United States", "segment": "",
                    "metric": "exports_fob_annual", "value": "%.0f" % world, "units": "USD",
                    "source_type": "trade-data", "source": COMTRADE_SRC,
                    "notes": "HS %s (%s); destination=World; %s" % (hs, HS_LABEL[hs], SECTOR_CAVEAT),
                })

            for pc, (label, country) in sorted(FOCUS_PARTNERS.items()):
                v = pmap.get(pc)
                if v is None:
                    continue  # genuinely not reported -> no row, never a zero
                rows.append({
                    "series_id": "us_exports_hs%s_%s" % (hs, label.lower().replace(" ", "_")),
                    "date": date,
                    "plant": "", "city": "", "state_or_region": label,
                    "country": "United States", "segment": "",
                    "metric": "exports_fob_annual_by_destination",
                    "value": "%.0f" % v, "units": "USD",
                    "source_type": "trade-data", "source": COMTRADE_SRC,
                    "notes": "HS %s (%s); destination=%s; %s"
                             % (hs, HS_LABEL[hs], country, SECTOR_CAVEAT),
                })

            # EU-27 aggregate, summed from member states actually reported
            eu_codes = [c for c in pmap if c in EU27]
            if eu_codes:
                eu_val = sum(pmap[c] for c in eu_codes)
                rows.append({
                    "series_id": "us_exports_hs%s_eu27" % hs, "date": date,
                    "plant": "", "city": "", "state_or_region": "EU-27",
                    "country": "United States", "segment": "",
                    "metric": "exports_fob_annual_by_destination",
                    "value": "%.0f" % eu_val, "units": "USD",
                    "source_type": "trade-data", "source": COMTRADE_SRC,
                    "notes": "HS %s (%s); destination=EU-27 aggregate summed from %d reported "
                             "member states; %s" % (hs, HS_LABEL[hs], len(eu_codes), SECTOR_CAVEAT),
                })

    # ---------- 3. Brazil / India annual world totals ---------------------
    for r in recs:
        if r["reporter"] in ("Brazil", "India") and r["freq"] == "A" \
                and r["scope"] == "world" and r["partnerCode"] == 0:
            if r["value_usd"] is None:
                continue
            direction = "exports" if r["flow"] == "X" else "imports"
            iso = "br" if r["reporter"] == "Brazil" else "in"
            rows.append({
                "series_id": "%s_%s_hs%s" % (iso, direction, r["hs"]),
                "date": "%s-12-31" % r["period"],
                "plant": "", "city": "", "state_or_region": "",
                "country": r["reporter"], "segment": "",
                "metric": "%s_annual" % direction,
                "value": "%.0f" % r["value_usd"], "units": "USD",
                "source_type": "trade-data",
                "source": "UN Comtrade public preview API, reporter=%s" % r["reporter"],
                "notes": "HS %s (%s); partner=World; whole-industry HS flow, NOT "
                         "Deere-only -- every manufacturer shipping from %s is in it"
                         % (r["hs"], HS_LABEL[r["hs"]], r["reporter"]),
            })

    # ---------- 4. corpus / policy rows -----------------------------------
    n_corpus = 0
    with open(args.corpus_rows) as f:
        for r in csv.DictReader(f):
            if not r.get("series_id"):
                continue
            rows.append({k: (r.get(k) or "") for k in HEADER})
            n_corpus += 1
    sys.stderr.write("corpus/policy rows: %d\n" % n_corpus)

    # ---------- write -----------------------------------------------------
    rows.sort(key=lambda r: (r["series_id"], r["date"]))
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)
    sys.stderr.write("wrote %d rows -> %s\n" % (len(rows), args.out))

    # ---------- correlation diagnostic ------------------------------------
    annual_world = defaultdict(dict)  # hs -> year -> world total
    for hs in annual:
        for year in annual[hs]:
            if 0 in annual[hs][year]:
                annual_world[hs][year] = annual[hs][year][0]
    diagnostics(monthly, annual_world, annual, args.corpus_rows, args.geo_matrix, args.diag)


def fiscal_quarter_months(period_end):
    """The three calendar months a Deere fiscal quarter actually covers.

    Deere's 13-week quarters do not end on a month boundary. In some years they
    end in the last week of Jan/Apr/Jul/Oct (e.g. 2025-07-27) and in others in
    the first days of Feb/May/Aug/Nov (e.g. 2026-05-03, 2026-02-01). Naively
    taking the three months ending in the period-end MONTH is therefore off by a
    full month for the early-in-month cases: Q2 FY2026 ended 2026-05-03 and
    covers Feb/Mar/Apr, not Mar/Apr/May.

    Rule: if the quarter ended in the first half of a month, essentially none of
    that month is in the quarter, so step back one month first.
    """
    y, m, d = int(period_end[:4]), int(period_end[5:7]), int(period_end[8:10])
    if d <= 15:
        m -= 1
        if m < 1:
            m += 12
            y -= 1
    out = []
    for k in range(3):
        mm = m - k
        yy = y
        while mm < 1:
            mm += 12
            yy -= 1
        out.append("%04d%02d" % (yy, mm))
    return out


def annual_correlation(annual_world, corpus_path, lines):
    """Annual US HS exports vs Deere 'Outside U.S. and Canada' net sales.

    Deere's fiscal year ends late October, so a fiscal year is matched to the
    calendar year it mostly overlaps. The mismatch is about two months and is
    the main reason not to read too much into the level of r here.
    """
    outside = {}
    for r in csv.DictReader(open(corpus_path)):
        if r["series_id"] == "de_net_sales_outside_us_canada":
            outside[int(r["date"][:4])] = float(r["value"])

    if len(outside) < 3:
        lines.append("annual: Deere outside-US series too short, skipped")
        return

    lines.append("ANNUAL: US HS exports (calendar year) vs Deere net sales and revenues")
    lines.append("        OUTSIDE U.S. and Canada (fiscal year, 10-K GEOGRAPHIC AREAS note)")
    lines.append("-" * 72)

    combos = {
        "hs8432+8433 (ag ex-tractors)": ["8432", "8433"],
        "hs8701 (tractors)": ["8701"],
        "hs8429 (construction)": ["8429"],
        "hs8432+8433+8701 (all ag)": ["8432", "8433", "8701"],
        "all four codes": ["8432", "8433", "8701", "8429"],
    }
    for label, codes in combos.items():
        xs, ys, yrs = [], [], []
        for fy in sorted(outside):
            tot, ok = 0.0, True
            for c in codes:
                v = annual_world.get(c, {}).get(str(fy))
                if v is None:
                    ok = False
                    break
                tot += v
            if ok:
                xs.append(tot)
                ys.append(outside[fy])
                yrs.append(fy)
        r, n = pearson(xs, ys)
        span = "%d-%d" % (yrs[0], yrs[-1]) if yrs else "n/a"
        lines.append("%-32s n=%2d (%s)  r=%s"
                     % (label, n, span, "%+.3f" % r if r is not None else " n/a"))
    lines.append("")


def canada_correlation(annual_partner, corpus_path, lines):
    """US machinery exports TO CANADA vs Deere revenue booked IN CANADA.

    This is the sharpest available test of the whole export thesis. Deere has no
    meaningful ag or construction ASSEMBLY in Canada, so Canadian revenue is
    almost entirely machines built elsewhere -- overwhelmingly in US plants --
    and shipped across the border. If US plant output drives any non-US revenue
    line, it is this one. Every other region has local Deere plants muddying it.
    """
    canada = {}
    for r in csv.DictReader(open(corpus_path)):
        if r["series_id"] == "de_net_sales_canada":
            canada[int(r["date"][:4])] = float(r["value"])
    if len(canada) < 3:
        return

    lines.append("CANADA: US HS exports to Canada vs Deere revenue booked in Canada")
    lines.append("-" * 72)
    combos = {
        "hs8432+8433 (ag ex-tractors)": ["8432", "8433"],
        "hs8701 (tractors, incl. road tractors)": ["8701"],
        "hs8429 (construction)": ["8429"],
        "all four codes": ["8432", "8433", "8701", "8429"],
    }
    for label, codes in combos.items():
        xs, ys, yrs = [], [], []
        for fy in sorted(canada):
            tot, ok = 0.0, True
            for c in codes:
                v = annual_partner.get(c, {}).get(str(fy), {}).get(124)
                if v is None:
                    ok = False
                    break
                tot += v
            if ok:
                xs.append(tot)
                ys.append(canada[fy])
                yrs.append(fy)
        r, n = pearson(xs, ys)
        span = "%d-%d" % (yrs[0], yrs[-1]) if yrs else "n/a"
        lines.append("%-40s n=%2d (%s)  r=%s"
                     % (label, n, span, "%+.3f" % r if r is not None else " n/a"))
    lines.append("  NOTE: n is tiny. With n<8 an r above +0.9 is not evidence of a")
    lines.append("  reliable relationship -- it is one or two points doing all the work.")
    lines.append("")


def diagnostics(monthly, annual_world, annual_partner, corpus_path, geo_path, diag_path):
    """Correlate US HS export totals against Deere revenue, annually and quarterly."""
    lines = []
    annual_correlation(annual_world, corpus_path, lines)
    canada_correlation(annual_partner, corpus_path, lines)

    if not os.path.exists(geo_path):
        sys.stderr.write("no geo matrix at %s, skipping quarterly correlation\n" % geo_path)
        open(diag_path, "w").write("\n".join(lines) + "\n")
        sys.stderr.write("\n".join(lines) + "\n")
        return

    grows = list(csv.DictReader(open(geo_path)))
    # Deere total revenue by geography, per fiscal period end
    nonus = defaultdict(float)
    us = defaultdict(float)
    seen = set()
    for r in grows:
        if r["segment"] != "Total":
            continue
        key = (r["period_end"], r["geography"])
        if key in seen:
            continue
        seen.add(key)
        try:
            v = float(r["value"])
        except (TypeError, ValueError):
            continue
        if r["geography"] == "United States":
            us[r["period_end"]] += v
        else:
            nonus[r["period_end"]] += v

    lines.append("QUARTERLY: US HS machinery exports vs Deere revenue")
    lines.append("=" * 68)
    lines.append("Each Deere 13-week fiscal quarter is mapped to the 3 calendar months it")
    lines.append("actually covers: quarters ending in the first half of a month (2026-05-03")
    lines.append("-> Feb/Mar/Apr) step back one month first. Residual mismatch ~1 week each end.")
    lines.append("r(level) and r(qoq) are inflated by seasonality shared between the two")
    lines.append("series; r(YoY) removes it and is the only one worth acting on.")
    lines.append("")

    combos = {
        "hs8432+8433 (ag machinery ex-tractors)": ["8432", "8433"],
        "hs8701 (tractors)": ["8701"],
        "hs8429 (construction)": ["8429"],
        "hs8432+8433+8701 (all ag)": ["8432", "8433", "8701"],
    }

    # Map each period end to its (fiscal_year, fiscal_quarter) so year-on-year
    # pairs the SAME quarter a year earlier. The 10-Q geography matrix only
    # carries Q1-Q3 of each year, so positional lags are wrong: index i-4 in this
    # sequence is not the same quarter one year back, it is one year and one
    # quarter back. Matching on the label is the only correct way.
    fq = {}
    for r in grows:
        fq[r["period_end"]] = (int(r["fiscal_year"]), r["fiscal_quarter"])

    for label, codes in combos.items():
        series = {}  # (fy, q) -> (exports, nonus, us)
        for pe in sorted(nonus):
            months = fiscal_quarter_months(pe)
            tot = 0.0
            ok = True
            for c in codes:
                for mo in months:
                    v = monthly.get(c, {}).get(mo)
                    if v is None:
                        ok = False
                        break
                    tot += v
                if not ok:
                    break
            if not ok or pe not in fq:
                continue
            series[fq[pe]] = (tot, nonus[pe], us[pe])

        keys = sorted(series)
        for idx, name in ((1, "Deere NON-US revenue"), (2, "Deere US revenue")):
            if len(keys) < 3:
                lines.append("%-42s vs %-22s  n=%d  (too few)" % (label, name, len(keys)))
                continue
            xs = [series[k][0] for k in keys]
            ys = [series[k][idx] for k in keys]
            r, n = pearson(xs, ys)
            # q/q first difference, in sequence order
            dx = [xs[i] - xs[i - 1] for i in range(1, len(xs))]
            dy = [ys[i] - ys[i - 1] for i in range(1, len(ys))]
            rd, nd = pearson(dx, dy)
            # YEAR-ON-YEAR growth, matched on the same fiscal quarter one year
            # earlier. Both series are strongly seasonal (planting and harvest
            # drive shipments and exports in the same months), so r on raw levels
            # and on q/q differences mostly measures a shared seasonal shape, not
            # shared information. This is the only one of the three worth acting on.
            yx, yy = [], []
            for (fyr, q) in keys:
                prev = (fyr - 1, q)
                if prev in series and series[prev][0] and series[prev][idx]:
                    yx.append(series[(fyr, q)][0] / series[prev][0] - 1)
                    yy.append(series[(fyr, q)][idx] / series[prev][idx] - 1)
            ry, ny = pearson(yx, yy)
            lines.append("%-42s vs %-22s  n=%2d  r(level)=%s  r(qoq)=%s  r(YoY)=%s [n=%d]"
                         % (label, name, n,
                            "%+.3f" % r if r is not None else "  n/a",
                            "%+.3f" % rd if rd is not None else "  n/a",
                            "%+.3f" % ry if ry is not None else "  n/a", ny))
        lines.append("")

    txt = "\n".join(lines)
    open(diag_path, "w").write(txt + "\n")
    sys.stderr.write(txt + "\n")


if __name__ == "__main__":
    main()
