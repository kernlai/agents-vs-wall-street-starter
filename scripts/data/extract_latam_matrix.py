#!/usr/bin/env python3
"""Extract Deere's ASC 606 primary-geographic-market revenue matrix rows for
Latin America (and totals) from the offline corpus 10-Q / 10-K filings.

Output: tidy long CSV fragment on stdout.
Source of truth: /challenge/offline-data/deere/filings/*.md
"""
import re, os, sys, glob, json

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"

# period header regex, e.g. "Three Months Ended July 27, 2025" / "Nine Months Ended ..."
PERIOD_RE = re.compile(
    r"(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})", re.I)
YEAR_RE = re.compile(r"^\s*(?:\|\s*)?(?:Year[s]?\s+Ended\s+)?(October|November)\s+(\d{1,2}),?\s+(\d{4})", re.I)

GEO_ROWS = [
    "United States", "Canada", "Western Europe", "Central Europe and CIS",
    "Latin America", "Asia, Africa, Oceania, and Middle",
]

MONTHS = {m: i+1 for i, m in enumerate(
    ["January","February","March","April","May","June","July","August","September","October","November","December"])}

def nums(line):
    """pull numeric cells out of a table/text line"""
    # strip the label part
    vals = re.findall(r"\(?\$?\s*-?([\d,]+)\s*\)?", line)
    out = []
    for v in vals:
        v = v.replace(",", "")
        if v == "":
            continue
        out.append(int(v))
    return out

def parse_file(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    lines = txt.split("\n")
    # locate revenue recognition section
    try:
        start = next(i for i,l in enumerate(lines) if re.search(r"^#{0,4}\s*\(\d+\)\s*Revenue Recognition", l.strip(), re.I))
    except StopIteration:
        return []
    # end of section: next numbered footnote header
    end = len(lines)
    for i in range(start+3, len(lines)):
        if re.match(r"^#{0,4}\s*\(\d+\)\s+[A-Z]", lines[i]) and not re.search(r"REVENUE RECOG", lines[i], re.I):
            end = i; break
    seg = lines[start:end]

    results = []
    cur = None
    for i, l in enumerate(seg):
        m = PERIOD_RE.search(l)
        if m:
            months = {"three":3,"six":6,"nine":9,"twelve":12}[m.group(1).lower()]
            mon = MONTHS[m.group(2).capitalize()]
            cur = (months, f"{m.group(4)}-{mon:02d}-{int(m.group(3)):02d}")
            continue
        for g in GEO_ROWS:
            # match label at start of the row (allow leading | and spaces)
            lab = re.sub(r"^\|?\s*", "", l).strip()
            if lab.startswith(g):
                rest = lab[len(g):]
                v = nums(rest)
                if g == "Asia, Africa, Oceania, and Middle" and len(v) < 4:
                    # continuation line "East  332 393 ..."
                    v = nums(re.sub(r"^\|?\s*East", "", seg[i+1].strip())) if i+1 < len(seg) else v
                if len(v) >= 4 and cur:
                    results.append((cur[0], cur[1], g, v[:5] if len(v)>=5 else v[:4]))
                break
    return results

def main():
    rows = {}
    for path in sorted(glob.glob(os.path.join(CORPUS, "*.md"))):
        for months, pend, geo, v in parse_file(path):
            key = (months, pend, geo)
            if key not in rows:
                rows[key] = (v, os.path.basename(path))
    out = []
    for (months, pend, geo), (v, src) in sorted(rows.items(), key=lambda x: (x[0][1], x[0][0], x[0][2])):
        out.append(dict(months=months, period_end=pend, geography=geo,
                        cols=len(v), vals=v, source=src))
    json.dump(out, sys.stdout, indent=0)

main()
