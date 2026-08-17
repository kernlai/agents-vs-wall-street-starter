#!/usr/bin/env python3
"""Build the tidy-long Western Europe regional dataset for the Deere FY2026 Q3 bottom-up forecast.
Depends on extract_geo_matrix.py having written /tmp/geo_matrix.json.
"""
import json, csv, os, statistics as st, datetime as dt, urllib.request

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/regional/western_europe.csv"
CORPUS = "challenge/offline-data/deere/filings"
HDR = ["series_id","period_end","fiscal_year","fiscal_quarter","geography","country",
       "segment","value","units","source_type","source","notes"]
rows = []
def add(**k):
    r = {h: k.get(h, "") for h in HDR}
    rows.append(r)

GEO = "Western Europe"
M = {(r["span"], r["period"]): r for r in json.load(open("/tmp/geo_matrix.json"))
     if r["geography"] == GEO}

# fiscal quarter -> (period_end, source filing basename)
QE = {(2019,1):"2019-01-27",(2019,2):"2019-04-28",(2019,3):"2019-07-28",(2019,4):"2019-11-03",
      (2020,1):"2020-02-02",(2020,2):"2020-05-03",(2020,3):"2020-08-02",(2020,4):"2020-11-01",
      (2021,1):"2021-01-31",(2021,2):"2021-05-02",(2021,3):"2021-08-01",(2021,4):"2021-10-31",
      (2022,1):"2022-01-30",(2022,2):"2022-05-01",(2022,3):"2022-07-31",(2022,4):"2022-10-30",
      (2023,1):"2023-01-29",(2023,2):"2023-04-30",(2023,3):"2023-07-30",(2023,4):"2023-10-29",
      (2024,1):"2024-01-28",(2024,2):"2024-04-28",(2024,3):"2024-07-28",(2024,4):"2024-10-27",
      (2025,1):"2025-01-26",(2025,2):"2025-04-27",(2025,3):"2025-07-27",(2025,4):"2025-11-02",
      (2026,1):"2026-02-01",(2026,2):"2026-05-03",(2026,3):"2026-08-02"}
NINE = {2019:"2019-07-28",2020:"2020-08-02",2021:"2021-08-01",2022:"2022-07-31",
        2023:"2023-07-30",2024:"2024-07-28",2025:"2025-07-27"}
SEGS = ["PPA","SAT","AT","CF","FS","Total"]

q = {}
for (fy, fq), pe in QE.items():
    r = M.get(("Three", pe))
    if r:
        q[(fy,fq)] = ({s: r.get(s) for s in SEGS}, r["source"], "10-Q/10-K revenue-recognition footnote")
for fy, ne in NINE.items():
    a, b = M.get(("FY", str(fy))), M.get(("Nine", ne))
    if a and b:
        q[(fy,4)] = ({s: (a[s]-b[s] if a.get(s) is not None and b.get(s) is not None else None) for s in SEGS},
                     a["source"], "DERIVED: fiscal year total minus nine-month total (Q4 is not separately disclosed)")

for (fy, fq) in sorted(q):
    vals, src, note = q[(fy,fq)]
    for seg in SEGS:
        v = vals.get(seg)
        if v is None:
            continue     # missing = absent row, never zero
        add(series_id="revenue_by_geo_segment", period_end=QE[(fy,fq)], fiscal_year=fy,
            fiscal_quarter=f"Q{fq}", geography=GEO, segment=seg, value=v, units="USDm",
            source_type="filing", source=f"{CORPUS}/{src}", notes=note)

# ---------------- FX ----------------
def fred(sid):
    u = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd=2018-08-01"
    d = {}
    for r in csv.DictReader(urllib.request.urlopen(u).read().decode().splitlines()):
        v = list(r.values())[1]
        if v not in (".","",None): d[dt.date.fromisoformat(r["observation_date"])] = float(v)
    return d
eur, gbp, sek = fred("DEXUSEU"), fred("DEXUSUK"), fred("DEXSDUS")
W = [("EUR",0.80), ("GBP",0.12), ("SEK",0.08)]
def qavg(s, end, inv=False):
    e = dt.date.fromisoformat(end); s0 = e - dt.timedelta(weeks=13)
    return st.mean([(1/x if inv else x) for d,x in s.items() if s0 < d <= e])

bask = {}
for (fy,fq), pe in sorted(QE.items()):
    if pe < "2018-11-01": continue
    e, g, k = qavg(eur,pe), qavg(gbp,pe), qavg(sek,pe,True)
    bask[(fy,fq)] = (e,g,k)
    add(series_id="fx_eurusd_qtr_avg", period_end=pe, fiscal_year=fy, fiscal_quarter=f"Q{fq}",
        geography=GEO, country="Euro area", segment="", value=round(e,4), units="USD per EUR",
        source_type="official_statistics",
        source="https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU (FRED/H.10, accessed 2026-08-16)",
        notes="mean of daily noon rates over the 13 weeks ending on Deere's fiscal quarter end")
    add(series_id="fx_gbpusd_qtr_avg", period_end=pe, fiscal_year=fy, fiscal_quarter=f"Q{fq}",
        geography=GEO, country="United Kingdom", segment="", value=round(g,4), units="USD per GBP",
        source_type="official_statistics",
        source="https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSUK (FRED/H.10, accessed 2026-08-16)",
        notes="13-week average to Deere fiscal quarter end")
for (fy,fq) in sorted(bask):
    p = (fy-1, fq)
    if p not in bask: continue
    r = sum(w*(bask[(fy,fq)][i]/bask[p][i]) for i,(c,w) in enumerate(W)) - 1
    add(series_id="fx_weu_basket_yoy", period_end=QE[(fy,fq)], fiscal_year=fy, fiscal_quarter=f"Q{fq}",
        geography=GEO, segment="", value=round(100*r,1), units="pct_yoy",
        source_type="derived",
        source="scripts/data/weu_fx_basket.py (FRED DEXUSEU/DEXUSUK/DEXSDUS)",
        notes="translation effect on WEu revenue; weights EUR 0.80 / GBP 0.12 / SEK 0.08 (assumption, not disclosed by Deere)")

# ---------------- CEMA business barometer ----------------
CEMA = [("2026-01-31",2026,"Q2",2,"January 2026 - Upturn still not fully materializing in business",
         "https://www.cema-agri.org/market-trends/24-business-barometer/1117-january-2026-upturn-still-not-fully-materializing-in-business"),
        ("2026-04-30",2026,"Q2",-6,"April 2026 - Business climate deteriorating again; 1/3 of makers expect fewer orders in next 6m, only 20% expect more; arable equipment worst, livestock best",
         "https://www.cema-agri.org/market-trends/24-business-barometer/1126-april-2026-business-climate-deteriorating-again"),
        ("2026-05-31",2026,"Q3",-9,"May 2026 - Business climate on the brink of recession (published 2026-05-13)",
         "https://www.cema-agri.org/market-trends/24-business-barometer/1128-may-2026-business-climate-on-the-brink-of-recession"),
        ("2026-06-30",2026,"Q3",-20,"June 2026 - Business climate slips back into recession; indices fell across all segments; arable worst, livestock above average; members still expect low-single-digit turnover growth for FY2026",
         "https://www.cema-agri.org/market-trends/24-business-barometer/1129-june-2026-business-climate-slips-back-into-recession"),
        ("2026-07-31",2026,"Q3",-19,"July 2026 - Business climate stabilizes in recessionary territory; sentiment stable in Germany, UK, Ireland, Scandinavia, Alpine region; weak in France, Italy, Poland",
         "https://www.cema-agri.org/market-trends/24-business-barometer/1131-july-2026-business-climate-stabilizes-in-recessionary-territory")]
for pe, fy, fq, v, note, url in CEMA:
    add(series_id="cema_business_climate_index", period_end=pe, fiscal_year=fy, fiscal_quarter=fq,
        geography=GEO, segment="", value=v, units="index_-100_to_+100", source_type="industry_association",
        source=f"{url} (accessed 2026-08-16)", notes=note)

# ---------------- EU dairy / crop / construction / registrations ----------------
add(series_id="eu_standard_milk_price", period_end="2026-06-30", fiscal_year=2026, fiscal_quarter="Q3",
    geography=GEO, country="EU", segment="SAT", value=38.20, units="EUR per 100kg",
    source_type="industry_press",
    source="https://en.edairynews.com/european-milk-prices-fluctuate-as-global-butter-values-decline/ (accessed 2026-08-16)",
    notes="European average base price, standard milk 4.2% fat / 3.4% protein, before bonuses; EUR 10.31/100kg BELOW June 2025 (approx -21% YoY). Dairy margin is the stated pillar of Deere's European SAT strength.")
add(series_id="eu_smp_price", period_end="2026-07-23", fiscal_year=2026, fiscal_quarter="Q3",
    geography=GEO, country="EU", segment="SAT", value=274, units="EUR per 100kg",
    source_type="industry_press",
    source="https://www.indexbox.io/blog/eu-dairy-commodity-prices-butter-up-15-smp-down-46-as-of-july-2026/ (accessed 2026-08-16)",
    notes="skimmed milk powder, -46% YoY as of 2026-07-23")
add(series_id="eu_butter_price", period_end="2026-07-23", fiscal_year=2026, fiscal_quarter="Q3",
    geography=GEO, country="EU", segment="SAT", value=396, units="EUR per 100kg",
    source_type="industry_press",
    source="https://www.indexbox.io/blog/eu-dairy-commodity-prices-butter-up-15-smp-down-46-as-of-july-2026/ (accessed 2026-08-16)",
    notes="butter +15% YoY as of 2026-07-23; dairy commodity signals are mixed, but farmgate milk is sharply lower")

wheat = {"2025-05-01":None}
def fredm(sid):
    u = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd=2023-01-01"
    d = {}
    for r in csv.DictReader(urllib.request.urlopen(u).read().decode().splitlines()):
        v = list(r.values())[1]
        if v not in (".","",None): d[r["observation_date"]] = float(v)
    return d
for sid, name, seg in [("PWHEAMTUSDM","global_wheat_price","PPA"), ("PMAIZMTUSDM","global_maize_price","PPA")]:
    s = fredm(sid)
    for k, v in sorted(s.items()):
        if k < "2025-01-01": continue
        add(series_id=name, period_end=k, fiscal_year=(2026 if k >= "2025-11-01" else 2025),
            fiscal_quarter="", geography=GEO, country="", segment=seg, value=round(v,1),
            units="USD per metric ton", source_type="official_statistics",
            source=f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid} (IMF via FRED, accessed 2026-08-16)",
            notes="global benchmark, proxy for EU arable revenue; monthly average")

add(series_id="euro_area_construction_output_yoy", period_end="2026-05-31", fiscal_year=2026,
    fiscal_quarter="Q3", geography=GEO, country="Euro area", segment="CF", value=1.2, units="pct_yoy",
    source_type="official_statistics",
    source="https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/4-20072026-ap (Eurostat, published 2026-07-20)",
    notes="production in construction, euro area, May 2026 vs May 2025; +0.4% MoM. EU +1.8% YoY.")
add(series_id="uk_tractor_registrations", period_end="2026-06-30", fiscal_year=2026, fiscal_quarter="Q3",
    geography=GEO, country="United Kingdom", segment="PPA", value=5955, units="units_H1",
    source_type="industry_association",
    source="https://www.farmersguardian.com/news/4533027/tractor-registrations-22-half-2026 (AEA data, accessed 2026-08-16)",
    notes="H1 2026 total, +22.3% vs H1 2025; June 2026 alone 999 units +17% YoY but still ~8% below the 5-year seasonal average; avg power 173hp unchanged; growth concentrated in 241-320hp, declines in 51-100hp and >320hp")
add(series_id="ireland_tractor_registrations", period_end="2026-06-30", fiscal_year=2026, fiscal_quarter="Q3",
    geography=GEO, country="Ireland", segment="PPA", value=1487, units="units_H1",
    source_type="industry_association",
    source="https://www.agriland.ie/farming-news/ftmta-1487-new-tractors-registered-in-first-half-of-2026/ (FTMTA, accessed 2026-08-16)",
    notes="H1 2026, +12% vs H1 2025")
add(series_id="france_agequipment_revenue_outlook", period_end="2026-12-31", fiscal_year=2026,
    fiscal_quarter="", geography=GEO, country="France", segment="", value=-2.5, units="pct_yoy_midpoint",
    source_type="industry_association",
    source="https://www.entraid.com/articles/marche-de-la-machine-agricole-2026 (Axema 2026 economic report, accessed 2026-08-16)",
    notes="Axema guides French ag-equipment revenue 0 to -5% in 2026 (~EUR 7.15bn) after -9% in 2025; French tractor registrations -15% in 2025 to 33,446, a 10-year low; recovery pushed to 2027")

# ---------------- Deere qualitative markers ----------------
QUAL = [("2026-05-21","Europe industry demand relatively stable, flat to up 5%; elevated interest rates still affecting purchases; arable sector 'a bit muted'; favourable dairy margins support the outlook",
         "challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md"),
        ("2026-05-21","Inventory levels in Europe in good shape after FY2024/FY2025 reductions; 2026 European production LARGELY ALIGNED WITH RETAIL DEMAND; order visibility extends through Q3 and into Q4",
         "challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-pres__1042774.md"),
        ("2026-02-19","European tractor order books 4-5 months out (i.e. covering roughly Feb-Jul 2026); Deere comfortable with European field inventory",
         "challenge/offline-data/deere/call-transcripts/2026-02-19__de-us-20260219-call-pres__605076.md"),
        ("2026-02-19","Q1 FY2026 large-ag volume flat YoY overall but mix was Europe UP, Asia up, North and South America down - unfavourable margin mix",
         "challenge/offline-data/deere/call-transcripts/2026-02-19__de-us-20260219-call-qna__605077.md"),
        ("2026-02-19","Global roadbuilding raised to up ~5% driven by North America AND Europe; Wirtgen strength 'not just concentrated in North America... Europe as well'",
         "challenge/offline-data/deere/call-transcripts/2026-02-19__de-us-20260219-call-qna__605077.md"),
        ("2025-08-15","Europe tractor and combine inventories down 10-15% over the prior twelve months",
         "challenge/offline-data/deere/call-transcripts/2025-08-15__de-us-20250815-call-q3-pres__143406.md")]
for d, note, src in QUAL:
    add(series_id="mgmt_commentary_europe", period_end=d, fiscal_year=2026, fiscal_quarter="",
        geography=GEO, segment="", value="", units="qualitative", source_type="call_transcript",
        source=src, notes=note)

add(series_id="deere_retail_europe_ag", period_end="2026-04-30", fiscal_year=2026, fiscal_quarter="Q2",
    geography=GEO, segment="PPA", value="", units="qualitative",
    source_type="slide", source="challenge/offline-data/deere/slides/2026-05-21__de-us-20260521-slide__1042212.md",
    notes="April 2026 rolling-3-month Deere internal retail sales, Europe Ag: tractors UP DOUBLE DIGITS, combines UP DOUBLE DIGITS, against an industry outlook of flat to up 5% -> implies share gain")

# ---------------- Forecast ----------------
FC = [("PPA", 695, 677, 2.7, 650, 745, "medium"),
      ("SAT", 810, 757, 7.0, 765, 860, "medium"),
      ("CF",  590, 550, 7.3, 555, 630, "medium"),
      ("FS",   53,  45, 17.8, 49,  57, "high"),
      ("Total",2148,2029, 5.9, 2020, 2290, "medium")]
for seg, c, base, yoy, lo, hi, conf in FC:
    add(series_id="forecast_q3fy2026", period_end="2026-08-02", fiscal_year=2026, fiscal_quarter="Q3",
        geography=GEO, segment=seg, value=c, units="USDm", source_type="forecast",
        source="scripts/data/weu_analysis.py + scripts/data/build_western_europe_csv.py",
        notes=(f"CENTRAL estimate. Q3 FY2025 base {base} (10-Q rev-rec basis). Implied YoY {yoy:+.1f}%. "
               f"Range {lo}-{hi}. Confidence {conf}. NOT AN ACTUAL - Deere reports FY2026 Q3 on 2026-08-20."))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=HDR); w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows -> {OUT}")
