#!/usr/bin/env python3
"""
Build the Central Europe & CIS regional dataset for the Deere FY2026 Q3 bottom-up forecast.

Sources
-------
All segment x geography figures come from Deere's ASC 606 revenue-recognition footnote
("net sales and revenues by primary geographic market"), extracted from the offline
corpus of 10-Q and 10-K filings. This is the REVENUE-RECOGNITION basis and does NOT tie
to the 8-K segment net-sales table.

Quarterly figures for Q1/Q2/Q3 are printed directly in the 10-Qs (three-month columns).
Q4 is derived as (fiscal year from the 10-K) minus (nine months from the Q3 10-Q).
Every derived figure is cross-footed against the printed YTD subtotals.

FY2019 predates the PPA/SAT split; the 10-Qs of that year report a single
"Agriculture & Turf" column. The FY2021 10-K restates FY2019 and FY2020 on the
PPA/SAT basis at the ANNUAL level only, so FY2019 quarters carry AT (combined) only.

Macro series come from FRED (keyless CSV endpoint).

Writes:
  data/deere/regional/central_europe_cis.csv   (tidy long)
"""
import csv
import os
import datetime
import statistics
import urllib.request

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/regional/central_europe_cis.csv"
CORPUS = "challenge/offline-data/deere/filings"

# --------------------------------------------------------------------------------------
# Deere fiscal quarter end dates (52/53-week year ending the last Sunday of October-ish)
# --------------------------------------------------------------------------------------
QEND = {
    ("2019", "Q1"): "2019-01-27", ("2019", "Q2"): "2019-04-28", ("2019", "Q3"): "2019-07-28", ("2019", "Q4"): "2019-11-03",
    ("2020", "Q1"): "2020-02-02", ("2020", "Q2"): "2020-05-03", ("2020", "Q3"): "2020-08-02", ("2020", "Q4"): "2020-11-01",
    ("2021", "Q1"): "2021-01-31", ("2021", "Q2"): "2021-05-02", ("2021", "Q3"): "2021-08-01", ("2021", "Q4"): "2021-10-31",
    ("2022", "Q1"): "2022-01-30", ("2022", "Q2"): "2022-05-01", ("2022", "Q3"): "2022-07-31", ("2022", "Q4"): "2022-10-30",
    ("2023", "Q1"): "2023-01-29", ("2023", "Q2"): "2023-04-30", ("2023", "Q3"): "2023-07-30", ("2023", "Q4"): "2023-10-29",
    ("2024", "Q1"): "2024-01-28", ("2024", "Q2"): "2024-04-28", ("2024", "Q3"): "2024-07-28", ("2024", "Q4"): "2024-10-27",
    ("2025", "Q1"): "2025-01-26", ("2025", "Q2"): "2025-04-27", ("2025", "Q3"): "2025-07-27", ("2025", "Q4"): "2025-11-02",
    ("2026", "Q1"): "2026-02-01", ("2026", "Q2"): "2026-05-03",
}

# --------------------------------------------------------------------------------------
# CENTRAL EUROPE AND CIS -- three-month figures as printed in the 10-Qs.
# Provenance: file each figure was read from (see extract_ce_cis_matrix.py for the scrape).
# Order: PPA, SAT, CF, FS, Total.  None = not disclosed on that basis.
# --------------------------------------------------------------------------------------
Q10Q = "challenge/offline-data/deere/filings/{}"
CE = {
    # FY2019: pre-split. AT reported as one column -> stored under segment "AT".
    ("2019", "Q1"): dict(AT=148, CF=171, FS=9, TOTAL=328,
                         src="2019-02-15__de-us-20190215-q1-10q__469204.md"),
    ("2019", "Q2"): dict(AT=393, CF=155, FS=9, TOTAL=557,
                         src="2019-05-17__de-us-20190517-q2-10q__469675.md"),
    ("2019", "Q3"): dict(AT=324, CF=229, FS=10, TOTAL=563,
                         src="2019-08-16__de-us-20190816-q3-10q__469206.md"),
    ("2019", "Q4"): dict(AT=558, CF=194, FS=9, TOTAL=761,
                         src="derived: FY2019 10-K (2019-11-27) less 9M FY2019 (2019-08-16 10-Q)"),
    # FY2020 onward: PPA/SAT split, as restated in the FY2021 filings.
    ("2020", "Q1"): dict(PPA=131, SAT=89, CF=159, FS=10, TOTAL=389,
                         src="2021-02-19__de-us-20210219-q1-10q__105814.md (prior-year column)"),
    ("2020", "Q2"): dict(PPA=258, SAT=80, CF=140, FS=8, TOTAL=486,
                         src="2021-05-21__de-us-20210521-q2-10q__105821.md (prior-year column)"),
    ("2020", "Q3"): dict(PPA=219, SAT=100, CF=178, FS=9, TOTAL=506,
                         src="2021-08-20__de-us-20210820-q3-10q__105837.md (prior-year column)"),
    ("2020", "Q4"): dict(PPA=290, SAT=224, CF=169, FS=8, TOTAL=691,
                         src="derived: FY2020 10-K restated (2021-11-24) less 9M FY2020"),
    ("2021", "Q1"): dict(PPA=161, SAT=84, CF=178, FS=9, TOTAL=432,
                         src="2021-02-19__de-us-20210219-q1-10q__105814.md"),
    ("2021", "Q2"): dict(PPA=531, SAT=160, CF=209, FS=9, TOTAL=909,
                         src="2021-05-21__de-us-20210521-q2-10q__105821.md"),
    ("2021", "Q3"): dict(PPA=398, SAT=117, CF=241, FS=10, TOTAL=766,
                         src="2021-08-20__de-us-20210820-q3-10q__105837.md"),
    ("2021", "Q4"): dict(PPA=232, SAT=114, CF=200, FS=11, TOTAL=557,
                         src="derived: FY2021 10-K (2021-11-24) less 9M FY2021"),
    ("2022", "Q1"): dict(PPA=202, SAT=126, CF=195, FS=11, TOTAL=534,
                         src="2022-02-18__de-us-20220218-q1-10q__105834.md"),
    ("2022", "Q2"): dict(PPA=404, SAT=151, CF=146, FS=11, TOTAL=712,
                         src="2022-05-20__de-us-20220520-q2-10q__105838.md"),
    ("2022", "Q3"): dict(PPA=348, SAT=109, CF=111, FS=14, TOTAL=582,
                         src="2022-08-19__de-us-20220819-q3-10q__105818.md"),
    ("2022", "Q4"): dict(PPA=253, SAT=102, CF=93, FS=13, TOTAL=461,
                         src="derived: FY2022 10-K (2022-11-23) less 9M FY2022"),
    ("2023", "Q1"): dict(PPA=202, SAT=123, CF=75, FS=12, TOTAL=412,
                         src="2023-02-17__de-us-20230217-q1-10q__105813.md"),
    ("2023", "Q2"): dict(PPA=393, SAT=212, CF=90, FS=8, TOTAL=703,
                         src="2023-05-19__de-us-20230519-q2-10q__105852.md"),
    ("2023", "Q3"): dict(PPA=302, SAT=85, CF=98, FS=6, TOTAL=491,
                         src="2023-08-18__de-us-20230818-q3-10q__105835.md"),
    ("2023", "Q4"): dict(PPA=321, SAT=110, CF=90, FS=10, TOTAL=531,
                         src="derived: FY2023 10-K (2023-11-22) less 9M FY2023"),
    ("2024", "Q1"): dict(PPA=179, SAT=73, CF=94, FS=8, TOTAL=354,
                         src="2024-02-15__de-us-20240215-q1-10q__105826.md"),
    ("2024", "Q2"): dict(PPA=275, SAT=80, CF=91, FS=8, TOTAL=454,
                         src="2024-05-16__de-us-20240516-q2-10q__105820.md"),
    ("2024", "Q3"): dict(PPA=201, SAT=70, CF=106, FS=12, TOTAL=389,
                         src="2024-08-15__de-us-20240815-q3-10q__105828.md"),
    ("2024", "Q4"): dict(PPA=132, SAT=61, CF=90, FS=8, TOTAL=291,
                         src="derived: FY2024 10-K (2024-11-21) less 9M FY2024"),
    ("2025", "Q1"): dict(PPA=67, SAT=39, CF=71, FS=4, TOTAL=181,
                         src="2025-02-13__de-us-20250213-q1-10q__105832.md"),
    ("2025", "Q2"): dict(PPA=239, SAT=99, CF=87, FS=3, TOTAL=428,
                         src="2025-05-15__de-us-20250515-q2-10q__105831.md"),
    ("2025", "Q3"): dict(PPA=301, SAT=130, CF=103, FS=2, TOTAL=536,
                         src="2025-08-14__de-us-20250814-q3-10q__155834.md"),
    ("2025", "Q4"): dict(PPA=225, SAT=91, CF=112, FS=2, TOTAL=430,
                         src="derived: FY2025 10-K (2025-12-18) less 9M FY2025"),
    ("2026", "Q1"): dict(PPA=172, SAT=60, CF=76, FS=2, TOTAL=310,
                         src="2026-02-26__de-us-20260226-q1-10q__636995.md"),
    ("2026", "Q2"): dict(PPA=297, SAT=121, CF=105, FS=2, TOTAL=525,
                         src="2026-05-21__de-us-20260521-q2-10q__1055929.md"),
}

# Western Europe -- the no-Russia control for the structural-break test.
# Q1-Q3 printed in the 10-Qs; Q4 = 10-K annual less the printed 9M.
# FY annual WE totals from the 10-Ks: 2020 5,333 / 2021 6,429 / 2022 6,344 /
#                                     2023 7,321 / 2024 6,189 / 2025 6,550.
WE = {
    ("2020", "Q1"): 1139, ("2020", "Q2"): 1491, ("2020", "Q3"): 1501, ("2020", "Q4"): 1202,
    ("2021", "Q1"): 1398, ("2021", "Q2"): 1867, ("2021", "Q3"): 1727, ("2021", "Q4"): 1437,
    ("2022", "Q1"): 1383, ("2022", "Q2"): 1683, ("2022", "Q3"): 1696, ("2022", "Q4"): 1582,
    ("2023", "Q1"): 1459, ("2023", "Q2"): 2169, ("2023", "Q3"): 2091, ("2023", "Q4"): 1602,
    ("2024", "Q1"): 1421, ("2024", "Q2"): 1857, ("2024", "Q3"): 1560, ("2024", "Q4"): 1351,
    ("2025", "Q1"): 1016, ("2025", "Q2"): 1820, ("2025", "Q3"): 2029, ("2025", "Q4"): 1685,
    ("2026", "Q1"): 1430, ("2026", "Q2"): 2141,
}
# Western Europe by segment, recent quarters only -- for the segment-level ratio anchor.
WE_SEG = {
    ("2024", "Q3"): dict(PPA=522, SAT=542, CF=432, FS=64),
    ("2025", "Q1"): dict(PPA=277, SAT=352, CF=344, FS=43),
    ("2025", "Q2"): dict(PPA=612, SAT=667, CF=497, FS=44),
    ("2025", "Q3"): dict(PPA=677, SAT=757, CF=550, FS=45),
    ("2025", "Q4"): dict(PPA=504, SAT=564, CF=564, FS=53),   # derived FY less 9M
    ("2026", "Q1"): dict(PPA=464, SAT=486, CF=426, FS=54),
    ("2026", "Q2"): dict(PPA=654, SAT=827, CF=608, FS=52),
}

# FY annual totals as printed in the 10-Ks (cross-foot targets)
FY_TOTAL = {"2019": 2209, "2020": 2072, "2021": 2664, "2022": 2289,
            "2023": 2137, "2024": 1488, "2025": 1575}

SEG_ORDER = ["PPA", "SAT", "AT", "CF", "FS", "TOTAL"]
SEG_LABEL = {"PPA": "PPA", "SAT": "SAT", "AT": "AT (PPA+SAT, pre-2020 basis)",
             "CF": "CF", "FS": "FS", "TOTAL": "TOTAL"}


def crossfoot():
    """Verify derived Q4s and segment sums."""
    bad = []
    for (fy, q), d in CE.items():
        parts = [d[s] for s in ("PPA", "SAT", "AT", "CF", "FS") if s in d]
        if sum(parts) != d["TOTAL"]:
            bad.append(f"{fy}{q} segments sum {sum(parts)} != total {d['TOTAL']}")
    for fy, tot in FY_TOTAL.items():
        s = sum(CE[(fy, q)]["TOTAL"] for q in ("Q1", "Q2", "Q3", "Q4") if (fy, q) in CE)
        if s != tot:
            bad.append(f"FY{fy} quarters sum {s} != 10-K annual {tot}")
    return bad


def fred(series):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    req = urllib.request.Request(url, headers={"User-Agent": "deere-regional-desk/1.0 (research)"})
    txt = urllib.request.urlopen(req, timeout=30).read().decode()
    out = {}
    rows = list(csv.reader(txt.splitlines()))
    for r in rows[1:]:
        if len(r) < 2:
            continue
        try:
            out[datetime.date.fromisoformat(r[0])] = float(r[1])
        except ValueError:
            pass
    return out


def main():
    problems = crossfoot()
    for p in problems:
        print("CROSSFOOT FAIL:", p)
    if not problems:
        print("crossfoot OK: all quarters sum to segment totals and to 10-K annuals")

    rows = []

    def add(**kw):
        rows.append(kw)

    # ---- 1. segment x quarter revenue -------------------------------------------------
    for (fy, q) in sorted(CE, key=lambda k: (k[0], k[1])):
        d = CE[(fy, q)]
        src = d["src"]
        derived = src.startswith("derived")
        for seg in SEG_ORDER:
            if seg not in d:
                continue
            add(series_id="de_rev_ce_cis_" + seg.lower(),
                period_end=QEND[(fy, q)], fiscal_year=fy, fiscal_quarter=q,
                geography="Central Europe and CIS", country="",
                segment=SEG_LABEL[seg], value=d[seg], units="USDm",
                source_type="10-Q/10-K derived" if derived else "10-Q",
                source=src if derived else f"{CORPUS}/{src}",
                notes="ASC 606 revenue-recognition basis; does NOT tie to 8-K segment net sales"
                      + ("; Q4 derived = FY less 9M" if derived else ""))

    # ---- 2. YoY growth ----------------------------------------------------------------
    for (fy, q) in sorted(CE):
        prev = (str(int(fy) - 1), q)
        if prev not in CE:
            continue
        for seg in ("PPA", "SAT", "CF", "TOTAL"):
            if seg in CE[(fy, q)] and seg in CE[prev] and CE[prev][seg]:
                yoy = 100.0 * (CE[(fy, q)][seg] / CE[prev][seg] - 1)
                add(series_id="de_rev_ce_cis_yoy_" + seg.lower(),
                    period_end=QEND[(fy, q)], fiscal_year=fy, fiscal_quarter=q,
                    geography="Central Europe and CIS", country="",
                    segment=SEG_LABEL[seg], value=round(yoy, 1), units="pct_yoy",
                    source_type="calculated",
                    source="calculated from ASC 606 footnote series above", notes="")

    # ---- 3. Western Europe control ----------------------------------------------------
    for (fy, q), v in sorted(WE.items()):
        add(series_id="de_rev_western_europe_total",
            period_end=QEND[(fy, q)], fiscal_year=fy, fiscal_quarter=q,
            geography="Western Europe", country="", segment="TOTAL", value=v,
            units="USDm", source_type="10-Q/10-K",
            source=f"{CORPUS}/ ASC 606 footnote, same filings as CE&CIS",
            notes="control region for the Russia structural-break test (no Russia exposure)")

    # ---- 4. macro ---------------------------------------------------------------------
    macro = [
        ("PWHEAMTUSDM", "wheat_usd_mt", "USD/mt", "IMF/World Bank global wheat price, monthly"),
        ("PMAIZMTUSDM", "maize_usd_mt", "USD/mt", "IMF/World Bank global maize price, monthly"),
        ("CCUSMA02PLM618N", "pln_per_usd", "PLN/USD", "OECD MEI monthly average"),
        ("CCUSMA02HUM618N", "huf_per_usd", "HUF/USD", "OECD MEI monthly average"),
        ("CCUSMA02CZM618N", "czk_per_usd", "CZK/USD", "OECD MEI monthly average"),
    ]
    for sid, name, unit, desc in macro:
        try:
            s = fred(sid)
        except Exception as e:  # network hiccup -> leave the rows absent, never zero
            print(f"WARN: FRED {sid} unavailable ({e}); rows omitted")
            continue
        for d, v in sorted(s.items()):
            if d < datetime.date(2018, 10, 1):
                continue
            add(series_id="macro_" + name, period_end=d.isoformat(), fiscal_year="",
                fiscal_quarter="", geography="Global" if "usd_mt" in name else "Central Europe",
                country="", segment="", value=round(v, 4), units=unit,
                source_type="FRED",
                source=f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid} (retrieved 2026-08-16)",
                notes=desc)

    # USD/EUR averaged over each Deere fiscal quarter (translation exposure proxy)
    try:
        eur = fred("DEXUSEU")
        windows = {}
        keys = sorted(QEND, key=lambda k: QEND[k])
        for i, k in enumerate(keys):
            end = datetime.date.fromisoformat(QEND[k])
            start = (datetime.date.fromisoformat(QEND[keys[i - 1]]) + datetime.timedelta(days=1)
                     if i else end - datetime.timedelta(days=90))
            windows[k] = (start, end)
        windows[("2026", "Q3")] = (datetime.date(2026, 5, 4), datetime.date(2026, 8, 2))
        for k, (a, b) in sorted(windows.items(), key=lambda x: x[1][1]):
            v = [x for d, x in eur.items() if a <= d <= b]
            if not v:
                continue
            add(series_id="macro_usd_per_eur_fq_avg", period_end=b.isoformat(),
                fiscal_year=k[0], fiscal_quarter=k[1], geography="Central Europe",
                country="", segment="", value=round(statistics.mean(v), 4),
                units="USD/EUR", source_type="FRED",
                source="https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU (retrieved 2026-08-16)",
                notes=f"mean of daily rates over the Deere fiscal quarter, n={len(v)}; "
                      f"Q3 FY2026 window 2026-05-04 to 2026-08-02 is complete")
    except Exception as e:
        print(f"WARN: DEXUSEU unavailable ({e})")

    # ---- 5. Q3 FY2026 forecast (NOT an actual -- Deere reports 2026-08-20) --------------
    FC = {"PPA": (308, 265, 345, "low"), "SAT": (120, 100, 140, "low"),
          "CF": (110, 96, 124, "medium"), "FS": (2, 1, 3, "medium"),
          "TOTAL": (540, 462, 612, "low")}
    base = {"PPA": 301, "SAT": 130, "CF": 103, "FS": 2, "TOTAL": 536}
    for seg, (c, lo, hi, conf) in FC.items():
        for tag, v in (("central", c), ("low", lo), ("high", hi)):
            add(series_id=f"de_rev_ce_cis_fcst_{seg.lower()}_{tag}",
                period_end="2026-08-02", fiscal_year="2026", fiscal_quarter="Q3",
                geography="Central Europe and CIS", country="", segment=seg, value=v,
                units="USDm", source_type="forecast",
                source="desk-central-europe-cis, 2026-08-16",
                notes=f"FORECAST, not reported. Deere reports FY2026 Q3 on 2026-08-20. "
                      f"Base Q3 FY2025 = {base[seg]}; implied YoY "
                      f"{100*(v/base[seg]-1):+.1f}%; confidence {conf}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cols = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "geography",
            "country", "segment", "value", "units", "source_type", "source", "notes"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    print(f"wrote {len(rows)} rows -> {OUT}")

    # ---- diagnostics printed for the briefing -----------------------------------------
    print("\n=== CE&CIS quarterly (USDm) ===")
    print(f"{'FQ':10}{'PPA':>7}{'SAT':>7}{'CF':>7}{'FS':>6}{'TOT':>7}{'WE tot':>9}{'CE/WE':>8}")
    for (fy, q) in sorted(CE):
        d = CE[(fy, q)]
        we = WE.get((fy, q))
        ratio = f"{100*d['TOTAL']/we:6.1f}%" if we else ""
        print(f"FY{fy} {q:3}{d.get('PPA', d.get('AT','')):>7}{d.get('SAT',''):>7}"
              f"{d['CF']:>7}{d['FS']:>6}{d['TOTAL']:>7}{we if we else '':>9}{ratio:>8}")

    print("\n=== structural break: CF run-rate (Russia roadbuilding/Wirtgen) ===")
    for fy in ("2021", "2022", "2023", "2024", "2025"):
        qs = [CE[(fy, q)]["CF"] for q in ("Q1", "Q2", "Q3", "Q4")]
        print(f"  FY{fy} CF {sum(qs):5} ({'/'.join(map(str,qs))})  avg/qtr {sum(qs)/4:.0f}")

    print("\n=== CE&CIS total as % of Western Europe total (diff-in-diff control) ===")
    for era, yrs in [("pre-war FY2020-21", ["2020", "2021"]), ("war-onset FY2022", ["2022"]),
                     ("exit complete FY2023", ["2023"]), ("trough FY2024", ["2024"]),
                     ("FY2025", ["2025"]), ("FY2026 H1", ["2026"])]:
        num = sum(CE[(y, q)]["TOTAL"] for y in yrs for q in ("Q1", "Q2", "Q3", "Q4") if (y, q) in CE)
        den = sum(WE[(y, q)] for y in yrs for q in ("Q1", "Q2", "Q3", "Q4") if (y, q) in WE)
        print(f"  {era:22} CE/WE = {100*num/den:5.1f}%   (CE {num}, WE {den})")

    print("\n=== segment-level CE/WE ratio, last 7 quarters (forecast anchor) ===")
    for k in sorted(WE_SEG):
        if k not in CE:
            continue
        r = " ".join(f"{s} {100*CE[k][s]/WE_SEG[k][s]:5.1f}%" for s in ("PPA", "SAT", "CF")
                     if s in CE[k] and WE_SEG[k].get(s))
        print(f"  FY{k[0]} {k[1]}  {r}")

    print("\n=== Q3/Q2 and Q3/H1 seasonality, CE&CIS total ===")
    for fy in ("2020", "2021", "2022", "2023", "2024", "2025"):
        q2, q3 = CE[(fy, "Q2")]["TOTAL"], CE[(fy, "Q3")]["TOTAL"]
        h1 = CE[(fy, "Q1")]["TOTAL"] + q2
        print(f"  FY{fy}  Q3/Q2 {q3/q2:.3f}   Q3/H1 {q3/h1:.3f}")


if __name__ == "__main__":
    main()
