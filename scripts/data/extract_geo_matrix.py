#!/usr/bin/env python3
"""Extract Deere's ASC 606 revenue-disaggregation geography x segment matrix
from the offline corpus (10-Q / 10-K, fiscal 2019 -> Q2 FY2026).

Handles four distinct layouts in the corpus:
  A. markdown table, period label in the header row ("Three Months Ended May 3, 2026 | PPA | ...")
  B. markdown table, period label repeated across every header cell
  C. plain text block, period label on its own line
  D. 10-K annual table, fiscal year on its own row ("| 2025 |")

Segment count varies: 4 segments (PPA/SAT/CF/FS) from FY2021; 3 (A&T/CF/FS) FY2019-20.

Usage: extract_geo_matrix.py [geography_substring]
"""
import os, re, sys, json, glob, collections

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"

GEOS = ["United States", "Canada", "Western Europe", "Central Europe and CIS",
        "Latin America", "Asia", "Total"]

PERIOD = re.compile(r"(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", re.I)
FYROW  = re.compile(r"^\|?\s*(20\d\d)\s*(\|[\s​|]*)?$")
STOP   = re.compile(r"(Major product line|Timing of revenue|Revenue recognized:)", re.I)

MONTHS = {m: i+1 for i, m in enumerate(
    ["January","February","March","April","May","June","July","August",
     "September","October","November","December"])}

def nums(line):
    parts = re.split(r"\|", line.replace("​", "")) if "|" in line else line.split()
    out = []
    for p in parts:
        p = p.strip().replace("$", "").replace(",", "").strip()
        for tok in p.split():
            tok = tok.replace(",", "")
            if re.fullmatch(r"\(?\d+\)?", tok):
                out.append(-int(tok.strip("()")) if tok.startswith("(") else int(tok))
    return out

def geo_of(line):
    t = line.replace("​", "").lstrip("| ").strip()
    for g in GEOS:
        if t.startswith(g):
            return g
    return None

def parse_file(path):
    txt = open(path, encoding="utf-8").read()
    lines = txt.split("\n")
    cur = None            # (span, iso_date) or ("FY", year)
    for ln in lines:
        if STOP.search(ln):
            cur = None
        m = PERIOD.search(ln)
        if m:
            span = m.group(1).title()
            d = f"{m.group(4)}-{MONTHS[m.group(2).title()]:02d}-{int(m.group(3)):02d}"
            cur = (span, d)
            continue
        fy = FYROW.match(ln.replace("​", "").strip())
        if fy and "Western Europe" in txt:
            cur = ("FY", fy.group(1))
            continue
        if cur is None:
            continue
        g = geo_of(ln)
        if not g:
            continue
        v = nums(ln)
        if len(v) == 5:
            segs = dict(zip(["PPA", "SAT", "CF", "FS", "Total"], v))
        elif len(v) == 4:
            segs = dict(zip(["AT", "CF", "FS", "Total"], v))
        else:
            continue
        if segs["Total"] != sum(x for k, x in segs.items() if k != "Total"):
            continue          # row failed internal cross-foot -> skip, do not guess
        yield cur[0], cur[1], ("Asia/Africa/Oceania/ME" if g == "Asia" else g), segs

def main():
    rows, prov, conflicts = {}, {}, []
    for path in sorted(glob.glob(os.path.join(CORPUS, "*.md"))):
        for span, per, geo, segs in parse_file(path):
            key = (span, per, geo)
            if key in rows and rows[key] != segs:
                conflicts.append((key, rows[key], segs, os.path.basename(path)))
            if key not in rows:
                rows[key], prov[key] = segs, os.path.basename(path)
    out = [{"span": k[0], "period": k[1], "geography": k[2], **v, "source": prov[k]}
           for k, v in rows.items()]
    json.dump(out, open("/tmp/geo_matrix.json", "w"), indent=1)
    filt = sys.argv[1] if len(sys.argv) > 1 else None
    for r in sorted(out, key=lambda r: (r["period"], r["span"])):
        if filt and filt.lower() not in r["geography"].lower():
            continue
        print(f"{r['span']:6s} {r['period']:11s} {r['geography']:24s} "
              f"PPA={r.get('PPA','')} SAT={r.get('SAT','')} AT={r.get('AT','')} "
              f"CF={r.get('CF')} FS={r.get('FS')} T={r.get('Total')}  [{r['source'][:14]}]")
    print(f"\n{len(out)} cells; {len(conflicts)} conflicts", file=sys.stderr)
    for c in conflicts[:10]:
        print("CONFLICT", c, file=sys.stderr)

main()
