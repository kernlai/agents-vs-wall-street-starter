#!/usr/bin/env python3
"""
Assemble data/deere/footprint/PLANT_MAP.md from the five agent CSVs.

Consolidates:
  plants.csv           - site spine, products, segment, geo_cell, headcount
  warn_layoffs.csv     - dated layoff / recall events per site
  production_events.csv- line starts, offshoring, capex, shutdowns
  headcount_hiring.csv - company-level 10-K backbone

Emits the plant table, the coverage statement, and the segment x geography
aggregation. Every unknown stays "unknown" -- nothing is imputed.

Usage: python3 scripts/data/de_build_plant_map.py > /dev/null   (writes PLANT_MAP.md)
"""

from __future__ import annotations

import csv
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FOOT = os.path.join(ROOT, "data", "deere", "footprint")
OUT = os.path.join(FOOT, "PLANT_MAP.md")


def read(name):
    with open(os.path.join(FOOT, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def kv(notes, key):
    m = re.search(rf"{key}=([^;]+)", notes or "")
    return m.group(1).strip() if m else None


def short_src(s):
    s = (s or "").strip().strip('"')
    if "jd-world-locations" in s:
        return "Deere worldwide locations PDF, Dec-2025"
    if "10-K Item 2" in s or "Form 10-K Item 2" in s:
        return "FY2025 10-K Item 2"
    if "10-K" in s:
        return "10-K Item 1"
    m = re.search(r"https?://(?:www\.)?([^/]+)", s)
    return m.group(1) if m else s[:60]


# --- validation corrections applied during consolidation -----------------------
# plants.csv tags 27 sites seg_src=filing, but the FY2025 10-K Item 2 table lists exactly
# 26 locations (28 named facilities; Waterloo bundles Engine Works, Foundry and Waterloo
# Works under one location row). Moline Seeding & Cylinder Works does NOT appear in that
# table -- verified against filings/2025-11-26__de-us-20251126-q4-10k__469216.md. Its
# segment (PPA) is almost certainly right, but it is inferred, not disclosed.
SEG_SRC_OVERRIDE = {"moline-seeding-cylinder": "inference"}

ITEM2_LOCATIONS = 26  # verified count of location rows in FY2025 10-K Item 2


def main():
    plants = read("plants.csv")
    warn = read("warn_layoffs.csv")
    prod = read("production_events.csv")

    # ---- spine: one entry per plant, from the products_count rows
    sites = {}
    for r in plants:
        if r["metric"] != "products_count" or not r["series_id"].startswith("plant."):
            continue
        slug = r["series_id"].split(".")[1]
        sites[slug] = {
            "slug": slug,
            "name": r["plant"],
            "city": r["city"],
            "region": r["state_or_region"],
            "country": r["country"],
            "segment": r["segment"] or "unknown",
            "geo": kv(r["notes"], "geo_cell") or "unknown",
            "seg_src": SEG_SRC_OVERRIDE.get(slug, kv(r["notes"], "seg_src") or "unknown"),
            "orientation": kv(r["notes"], "orientation") or "unknown",
            "products": (kv(r["notes"], "products") or "unknown"),
            "hc": None,
            "hc_date": None,
            "hc_src": None,
            "hc_note": None,
            "hc_prod": None,
            "hc_prod_date": None,
            "opened": None,
        }

    # ---- headcount: keep the MOST RECENT observation per plant, and record its date
    for r in plants:
        if not r["series_id"].startswith("plant."):
            continue
        slug = r["series_id"].split(".")[1]
        if slug not in sites:
            continue
        s = sites[slug]
        if r["metric"] == "employees":
            if s["hc_date"] is None or r["date"] > s["hc_date"]:
                s["hc"] = int(float(r["value"]))
                s["hc_date"] = r["date"]
                s["hc_src"] = short_src(r["source"])
                s["hc_note"] = r["notes"]
        elif r["metric"] == "employees_production":
            if s["hc_prod_date"] is None or r["date"] > s["hc_prod_date"]:
                s["hc_prod"] = int(float(r["value"]))
                s["hc_prod_date"] = r["date"]
        elif r["metric"] == "year_opened":
            s["opened"] = int(float(r["value"]))

    # ---- events per site, from WARN + production events
    NAME_TO_SLUG = {
        "Waterloo Works": "waterloo",
        "Waterloo Foundry": "waterloo",
        "Harvester Works": "east-moline",
        "Seeding and Cylinder": "moline-seeding-cylinder",
        "Des Moines Works": "des-moines",
        "Ottumwa Works": "ottumwa",
        "Dubuque Works": "dubuque",
        "Davenport Works": "davenport",
        "Coffeyville Works": "coffeyville",
        "Horicon Works": "horicon",
        "Kernersville excavator factory": "kernersville",
        "Ramos Arizpe plant": "ramos-arizpe",
    }
    ev_lay = defaultdict(int)      # layoffs with an effective date in 2024-2025
    ev_rec = defaultdict(int)      # recalls + new hires announced in 2026
    ev_old = defaultdict(int)      # pre-2024 layoffs, kept separate
    for r in warn:
        if r["series_id"].endswith("_fq"):
            continue
        slug = NAME_TO_SLUG.get(r["plant"])
        if not slug:
            continue
        try:
            v = float(r["value"])
        except ValueError:
            continue
        if r["metric"] == "employees_affected":
            eff = kv(r["notes"], "effective_date") or r["date"]
            (ev_lay if eff >= "2024-01-01" else ev_old)[slug] += v
        elif r["metric"] in ("employees_recalled", "employees_hired_new"):
            ev_rec[slug] += v
    for r in prod:
        slug = NAME_TO_SLUG.get(r["plant"])
        if not slug or r["metric"] != "shift_change" or not r["value"]:
            continue
        # production_events overlaps WARN for 2024-25 comparators -- only take the
        # 2026 recall rows that WARN also has, to avoid double counting: skip entirely.
        continue

    # ---- render
    L = []
    A = L.append
    A("# Deere & Company — consolidated manufacturing footprint (PLANT_MAP)")
    A("")
    A("Built 2026-08-16 from five independent collection passes. **Deere has not reported")
    A("FY2026 Q3** — the earnings call is 2026-08-20, after this file was written. Nothing")
    A("here is a Q3 FY2026 actual.")
    A("")
    A("Regenerate with `python3 scripts/data/de_build_plant_map.py`.")
    A("Companion indicator file: `HIRING_TRACKER.md`.")
    A("")
    A("---")
    A("")

    # coverage block
    n = len(sites)
    n_hc = sum(1 for s in sites.values() if s["hc"] is not None)
    n_hc_recent = sum(1 for s in sites.values() if s["hc_date"] and s["hc_date"] >= "2024-01-01")
    n_prod = sum(1 for s in sites.values() if s["hc_prod"] is not None)
    n_filing_seg = sum(1 for s in sites.values() if s["seg_src"] == "filing")

    A("## 1. Coverage, stated before the data")
    A("")
    A("| | count | of 62 |")
    A("|---|---:|---:|")
    A(f"| Sites enumerated (name, city, country, products, segment, geography) | {n} | 100% |")
    A(f"| Segment attribution from a filing rather than inferred | {n_filing_seg} | {100*n_filing_seg//n}% |")
    A(f"| **Any site headcount at all** | **{n_hc}** | **{100*n_hc//n}%** |")
    A(f"| Headcount dated 2024 or later | {n_hc_recent} | {100*n_hc_recent//n}% |")
    A(f"| Production-only headcount | {n_prod} | {100*n_prod//n}% |")
    A("")
    A("**Deere does not disclose plant-level headcount anywhere.** The 10-K gives one worldwide")
    A("total, one US total, and (since FY2024) a production sub-total. Every site number below was")
    A("reconstructed from local news or an economic-development announcement, which biases the")
    A("sample hard: most of these stories exist *because* a plant was cutting, so the figures")
    A("cluster on shrinking plants and are usually snapshots taken immediately before a cut.")
    A("Treat each as a dated point estimate with its own provenance, **not** as a panel.")
    A("")
    A("**Two corrections applied during consolidation**, both found by recomputing from the raw")
    A("CSV rather than trusting the collecting agent's own summary:")
    A("")
    A("- The source file tags **27** sites as filing-sourced on segment. The FY2025 10-K Item 2 table")
    A(f"  actually lists exactly **{ITEM2_LOCATIONS} locations** (28 named facilities — Waterloo bundles Engine")
    A("  Works, the Foundry and Waterloo Works under one row). **Moline Seeding & Cylinder Works is")
    A("  not in it.** Its PPA assignment is almost certainly right but it is inferred, and it is")
    A("  re-tagged `i` below.")
    A("- Distinct-plant counts corrected: **15** plants (not 17) have a headcount observation dated")
    A("  2024 or later, and **5** plants (not 6) have a production-only figure — the higher numbers")
    A("  counted rows, and Waterloo and Moline each contribute two.")
    A("")
    A("Deere's own FY2025 10-K Item 2 discloses the structural totals: **23 owned + 4 leased**")
    A("factory locations in the US and Canada and **45** outside — roughly **72 factories**. This")
    A(f"file names {n}. **About ten factories are therefore missing entirely and cannot be named.**")
    A("")
    A("---")
    A("")

    # main table
    A("## 2. The plant table")
    A("")
    A("`seg src` = `F` where the FY2025 10-K Item 2 table names the site and its segment, `i` where")
    A("segment is inferred from the product list. `geo cell` maps the site to the revenue-by-geography")
    A("disclosure used elsewhere in this project, and is an analytical judgement, not a disclosed fact.")
    A("")
    A("| # | Plant | City | Country | Segment | seg src | Geo cell | Employees | as of | Headcount source | Products |")
    A("|---:|---|---|---|---|:---:|---|---:|---|---|---|")
    order = sorted(
        sites.values(),
        key=lambda s: (
            {"United States": 0, "Canada": 1, "Western Europe": 2, "Central Europe & CIS": 3,
             "Latin America": 4}.get(s["geo"], 5),
            -(s["hc"] or 0),
            s["name"],
        ),
    )
    for i, s in enumerate(order, 1):
        hc = f"{s['hc']:,}" if s["hc"] is not None else "unknown"
        if s["hc_prod"] is not None:
            hc += f"<br><sub>{s['hc_prod']:,} prod</sub>"
        A(
            f"| {i} | {s['name']} | {s['city']} | {s['country']} | {s['segment'] or 'unknown'} | "
            f"{'F' if s['seg_src']=='filing' else 'i'} | {s['geo']} | {hc} | "
            f"{s['hc_date'] or '—'} | {s['hc_src'] or '—'} | {s['products'].replace('|', ',')} |"
        )
    A("")

    # gaps
    A("### Sites with no headcount at all")
    A("")
    blanks = [s for s in order if s["hc"] is None]
    A(f"**{len(blanks)} of {n} sites.** Listed so the hole is explicit rather than hidden:")
    A("")
    A("> " + "; ".join(f"{s['name']} ({s['country']})" for s in blanks))
    A("")
    A("The two that matter most:")
    A("")
    A("- **Davenport Works (CF, Iowa)** — a top-five US site that absorbed 291 WARN-recorded layoffs")
    A("  across 2024–25 and 115 recalls across 2026, and for which no public total headcount exists.")
    A("  Every Davenport event is therefore unsizable against its own base.")
    A("- **The Wirtgen road-building plants** (Windhagen, Göppingen, Ludwigshafen, Tirschenreuth,")
    A("  Wittlich, Langfang, Porto Alegre). Wirtgen Group publishes a single ~8,900 worldwide figure")
    A("  and never a per-plant one. These plants drive the CF/Western Europe growth that the Q2 FY2026")
    A("  call attributes to roadbuilding, and they are completely dark to this indicator.")
    A("")
    A("---")
    A("")

    # segment x geography
    A("## 3. Segment × geography aggregation")
    A("")
    A("This is the join that makes a plant event readable as a revenue signal: a Waterloo layoff is")
    A("evidence about **PPA / United States**; short-time working at Zweibrücken is evidence about")
    A("**PPA+SAT / Western Europe**; collective vacation at Horizontina is **PPA / Latin America**.")
    A("Never pool a signal across cells.")
    A("")
    A("Reference magnitudes — FY2025 segment net sales ($m): PPA 17,311 · SAT 10,224 · CF 11,382.")
    A("Q2 FY2026 revenue by geography ($m): US 7,198 · Canada 1,039 · W. Europe 2,141 ·")
    A("C. Europe & CIS 525 · Latin America 1,268 · Asia/Africa/Oceania/ME 1,198.")
    A("")

    cells = defaultdict(list)
    geo_order = ["United States", "Canada", "Western Europe", "Central Europe & CIS",
                 "Latin America", "Asia/Africa/Oceania/Middle East"]
    for s in order:
        segs = [x.strip() for x in (s["segment"] or "").split(";") if x.strip()]
        if not segs:
            segs = ["(unassigned)"]
        for seg in segs:
            cells[(s["geo"], seg)].append(s)

    A("### 3a. By geography")
    A("")
    A("`known headcount` sums only the sites that have a number, so it is a **floor**, and `blank`")
    A("says how many sites in that cell contribute nothing to it. A cell with a small known total and")
    A("many blanks is not a small cell — Asia/Africa/Oceania/ME booked $1,198m in Q2 FY2026 and has")
    A("**nine plants and not one headcount**.")
    A("")
    A("| Geo cell | Plants | Sites w/ headcount | Known headcount (floor) | Blank |")
    A("|---|---:|---:|---:|---:|")
    for geo in geo_order:
        grp = [s for s in order if s["geo"] == geo]
        if not grp:
            A(f"| {geo} | 0 | 0 | — | — |")
            continue
        known = [g for g in grp if g["hc"] is not None]
        tot = sum(g["hc"] for g in known)
        A(f"| {geo} | {len(grp)} | {len(known)} | "
          f"{format(tot, ',') if known else '—'} | {len(grp)-len(known)} |")
    A("")
    A("### 3b. By segment — plant counts only")
    A("")
    A("**Headcount is deliberately not totalled by segment.** Sixteen sites serve more than one")
    A("segment (Waterloo is PPA+CF; Mannheim is SAT+PPA; Getafe, Saran, Monterrey and Torreón are")
    A("all three) and Deere publishes no basis for apportioning a site's people between segments.")
    A("Any segment headcount total would be an invented split. Plant counts are given instead, and")
    A("a multi-segment site is counted once in each segment it serves, so these sum to more than 62.")
    A("")
    A("| Segment | Plants | of which with a headcount | FY2025 net sales ($m) |")
    A("|---|---:|---:|---:|")
    for seg, sales_fy25 in (("PPA", "17,311"), ("SAT", "10,224"), ("CF", "11,382")):
        grp = [s for s in order if seg in (s["segment"] or "")]
        known = [g for g in grp if g["hc"] is not None]
        A(f"| {seg} | {len(grp)} | {len(known)} | {sales_fy25} |")
    unass = [s for s in order if not (s["segment"] or "").strip() or s["segment"] == "unknown"]
    A(f"| (no segment — all-makes parts depots) | {len(unass)} | "
      f"{len([g for g in unass if g['hc'] is not None])} | n/a |")
    A("")
    A("Mexico is mapped to `geo_cell = United States` on functional grounds — see §4.")
    A("")

    A("### 3c. The matrix, by name")
    A("")
    A("| geo cell | PPA | SAT | CF |")
    A("|---|---|---|---|")
    def names(geo, seg):
        grp = cells.get((geo, seg))
        if not grp:
            return "—"
        return ", ".join(
            g["city"] + ("*" if g["hc"] is None else "") for g in sorted(grp, key=lambda x: x["city"])
        )
    for geo in geo_order:
        A(f"| **{geo}** | {names(geo,'PPA')} | {names(geo,'SAT')} | {names(geo,'CF')} |")
    A("")
    A("`*` = no headcount known for that site.")
    A("")
    A("**The empty cell is the informative one.** Central Europe & CIS booked $525m in Q2 FY2026 and")
    A("has **no Deere plant of its own** — it is supplied entirely from Western Europe. A Zweibrücken")
    A("or Mannheim slowdown therefore reads into two revenue cells at once, and no plant-level signal")
    A("will ever originate inside Central Europe & CIS. Russia is a confirmed exit, not a gap:")
    A("shipments suspended 2022-02-24, dealer agreements not renewed from 2022-11-01, financial")
    A("services sold in Q2 FY2023, Orenburg acquired by Koblik Group in 2023, and neither Orenburg nor")
    A("Domodedovo appears in Deere's December 2025 locations list.")
    A("")
    A("---")
    A("")

    A("## 4. Three mapping judgements you may want to reverse")
    A("")
    A("1. **Mexico → United States.** Monterrey, Ramos Arizpe, Saltillo and Torreón are physically in")
    A("   Latin America, but their output is captive components, cabs and engines feeding US assembly")
    A("   and the US retail market, so they are keyed to `geo_cell = United States`. The `country`")
    A("   column is preserved so anyone can re-key on location instead. **Ramos Arizpe absorbed the")
    A("   large-tractor cab line moved out of Waterloo**, so Waterloo layoffs and Ramos Arizpe hiring")
    A("   are partly the *same* event. Do not count them twice.")
    A("2. **Ottumwa → SAT.** Not in the 10-K Item 2 table. Assigned SAT because hay and forage sits in")
    A("   Small Ag & Turf. If you disagree, the Ottumwa events (75 laid off Jan-2025, a four-week")
    A("   inventory-adjustment shutdown Dec-2024) move to PPA and change the segment read materially.")
    A("3. **Coffeyville → CF.** A drivetrain component plant feeding several assembly plants. Its")
    A("   April-2026 recall of 8 is tagged CF here but genuinely serves more than one segment.")
    A("")
    A("---")
    A("")

    A("## 5. Company-level anchor series — the part that *is* filing grade")
    A("")
    A("From Item 1 'Employees' of each 10-K in the corpus. Verified verbatim against")
    A("`filings/2025-11-26__de-us-20251126-q4-10k__469216.md` for FY2025.")
    A("")
    A("| FY end | Worldwide | US (+Canada to FY2023) | Full-time production WW | UAW-covered active US |")
    A("|---|---:|---:|---:|---:|")
    for row in [
        ("2015-10-31", "57,200", "28,500", "—", "10,000"),
        ("2016-10-30", "56,800", "27,900", "—", "7,600"),
        ("2017-10-29", "60,500", "29,000", "—", "8,700"),
        ("2018-10-28", "74,000", "31,000", "—", "9,600"),
        ("2019-11-03", "73,500", "30,000", "—", "9,300"),
        ("2020-11-01", "69,600", "27,500", "—", "8,740"),
        ("2021-10-31", "75,600", "29,000", "—", "10,500"),
        ("2022-10-30", "82,200", "32,000", "—", "11,500"),
        ("2023-10-29", "83,000", "33,800", "—", "11,500"),
        ("2024-11-03", "75,800", "29,600 (US only)", "35,200", "8,900"),
        ("2025-11-02", "73,100", "27,000 (US only)", "32,500", "7,600"),
    ]:
        A("| " + " | ".join(row) + " |")
    A("")
    A("FY2025 additionally: **~11,600 full-time US production employees**, unions certified for **77%**")
    A("of US production and maintenance staff, **~7,600 active US production workers under the UAW")
    A("agreement expiring 2027-11-01**. That 11,600 is the practical denominator for sizing any US")
    A("WARN or callback event; the 7,600 is the denominator for the union-covered subset.")
    A("")
    A("Worldwide headcount is **−11.9%** from the FY2023 peak and US headcount **−20.1%**. US shrank")
    A("about twice as fast as the group. PPA is the most US-weighted segment, so that asymmetry is")
    A("itself a segment signal, and it lines up with FY2026 guidance of PPA −5% to −10%.")
    A("")
    A("**Two breaks that must not be smoothed.** FY2015–FY2023 disclose 'US *and Canada*'; FY2024–FY2025")
    A("disclose 'US' only — never join them. And the FY2018 jump 60,500 → 74,000 is the Wirtgen")
    A("acquisition (~8,200 people), not a production signal. The UAW series also gains the word")
    A("'active' from FY2016, so the FY2015→FY2016 −24% is partly definitional.")
    A("")
    A("---")
    A("")
    A("## 6. What each site contributes to the indicator")
    A("")
    A("Sites with at least one dated 2024–2026 labour event, which is the set the tracker actually")
    A("watches. Everything else in the table above is structural context.")
    A("")
    A("Layoffs are bucketed by **effective date**, recalls and new hires by announcement date.")
    A("")
    A("| Plant | Segment | pre-2024 layoffs | 2024–25 layoffs | 2026 recalls + new hires | 2024→2026 net |")
    A("|---|---|---:|---:|---:|---:|")
    allslugs = set(list(ev_lay) + list(ev_rec) + list(ev_old))
    for slug in sorted(allslugs, key=lambda k: -(ev_lay[k] + ev_rec[k])):
        s = sites.get(slug)
        nm = s["name"] if s else slug
        old = f"{ev_old[slug]:,.0f}" if ev_old[slug] else "—"
        A(f"| {nm} | {s['segment'] if s else '?'} | {old} | {ev_lay[slug]:,.0f} | "
          f"{ev_rec[slug]:,.0f} | {ev_rec[slug]-ev_lay[slug]:+,.0f} |")
    A("")
    A("The pre-2024 column holds only the two events the archives reach: **425 at Harvester Works**")
    A("(notice 2014-08-20, effective 2014-10-20, permanent, UAW Local 865 — the largest single Deere")
    A("WARN event in the entire 1999–2026 Illinois archive) and **220 at Moline Seeding & Cylinder**")
    A("(Deere press release 2015-11-30, no corresponding Illinois WARN record). Iowa's WARN database")
    A("does not start until 2021-08-18, so pre-2021 Iowa is invisible and those columns are not")
    A("comparable across plants.")
    A("")
    A("Salaried, corporate and financial-services WARN rows (World Headquarters 298, Intelligent")
    A("Solutions Group 59, John Deere Financial 67) are **excluded** — they are headcount, not build")
    A("rate. So is the 2018 Eurest Services notice (79 food-service contractors at three Deere Quad")
    A("Cities sites), which is not Deere payroll at all.")
    A("")
    A("Note what is **absent** from that table: Harvester Works in East Moline — the sole North")
    A("American combine plant and the core of PPA — took 415 cuts across 2024–25 (279 + 21 by WARN,")
    A("plus a 115-worker action in August 2025 that fell below the Illinois WARN threshold and was")
    A("never filed) and received **nothing** in 2026. Read alongside PPA guidance of −5% to −10%,")
    A("that silence is the single most informative row in the whole footprint.")
    A("")
    A("---")
    A("")
    A("## 7. Maintaining this")
    A("")
    A("- Re-pull `deere.com/assets/pdfs/common/our-company/about/jd-world-locations.pdf` each")
    A("  December; Deere re-dates it annually and it is the cheapest way to catch openings, closures")
    A("  and product moves.")
    A("- Re-read 10-K Item 2 each November for segment reassignments and the owned/leased counts.")
    A("- Headcount rows will always be hand-maintained from news. Update a plant only when a WARN")
    A("  notice or a local story restates the base. **Never carry a headcount forward more than four")
    A("  quarters without re-sourcing it** — mark it stale instead. Augusta (470, 2016) and Valley City")
    A("  (330, 2017) are already stale and are kept only because they are the only numbers that exist.")
    A("- Known conflicts left unreconciled on purpose: Horizontina 1,700 (Feb-2024, combine + planter)")
    A("  vs 700 (Feb-2025, combine operation only) — different scopes, do not difference them; Ottumwa")
    A("  800 (2022) vs 'less than 400' (Nov-2024), recorded as an upper bound; Getafe 1,114 is the legal")
    A("  entity John Deere Ibérica S.A. from the Spanish registry, not strictly the plant.")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"wrote {OUT}  ({len(sites)} sites, {n_hc} with headcount)")


if __name__ == "__main__":
    main()
