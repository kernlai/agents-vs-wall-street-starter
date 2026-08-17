#!/usr/bin/env python3
"""
Extract Deere & Company's ASC 606 revenue-recognition geographic x segment matrix
from the offline corpus of 10-Q / 10-K filings.

Handles both the markdown-table and the plain-text renderings that appear in the
corpus, and both the pre-FY2020 (Ag & Turf / C&F / FS) and post-FY2020
(PPA / SAT / CF / FS) segment structures.

Outputs a tidy long CSV to stdout.
"""
import re
import os
import sys
import glob
import csv
from datetime import date

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"

GEOS = [
    ("United States", "united_states"),
    ("Canada", "canada"),
    ("Western Europe", "western_europe"),
    ("Central Europe and CIS", "central_europe_cis"),
    ("Latin America", "latin_america"),
    ("Asia, Africa, Oceania, and Middle East", "asia_africa_oceania_me"),
]

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}

# Deere fiscal year ends late Oct / early Nov. FY quarter ends:
# Q1 ~ late Jan/early Feb, Q2 ~ late Apr/early May, Q3 ~ late Jul/early Aug, Q4 ~ late Oct/early Nov.
def fiscal_qtr(d):
    """Map a period-end date to (fiscal_year, fiscal_quarter)."""
    m = d.month
    if m in (1, 2):
        return d.year, 1
    if m in (4, 5):
        return d.year, 2
    if m in (7, 8):
        return d.year, 3
    if m in (10, 11):
        # FY ends here; fiscal year == calendar year of the Oct/Nov end
        return d.year, 4
    raise ValueError(f"unexpected period end {d}")


HEADER_RE = re.compile(
    r"(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+"
    r"([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})", re.I)
YEAR_RE = re.compile(
    r"Years?\s+Ended\s+([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})", re.I)

NUM_RE = re.compile(r"\(?\$?\s*-?[\d,]+\)?")


def clean_line(ln):
    # strip zero-width / non-breaking marks used as empty table cells
    ln = ln.replace("​", " ").replace(" ", " ")
    ln = ln.replace("|", " ")
    return ln


def nums_after(label, line):
    """Return the list of integers appearing after `label` on `line`."""
    idx = line.lower().find(label.lower())
    if idx < 0:
        return []
    rest = line[idx + len(label):]
    out = []
    for tok in re.findall(r"\(?\$?\s*([\d,]+)\)?", rest):
        t = tok.replace(",", "")
        if t == "":
            continue
        out.append(int(t))
    return out


def parse_file(path):
    """Yield dicts: period_end, months, segments->{geo: value}."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        raw = fh.read()

    # Only work inside the REVENUE RECOGNITION note (geographic matrix lives there).
    # Some 10-Ks repeat it; take everything from the first occurrence onward,
    # but bound it so we don't wander into unrelated tables.
    lines = raw.split("\n")

    blocks = []  # (line_idx, months, period_end)
    for i, ln in enumerate(lines):
        c = clean_line(ln)
        m = HEADER_RE.search(c)
        if m:
            word, mon, day, yr = m.groups()
            months = {"three": 3, "six": 6, "nine": 9, "twelve": 12}[word.lower()]
            if mon.capitalize() not in MONTHS:
                continue
            blocks.append((i, months,
                           date(int(yr), MONTHS[mon.capitalize()], int(day))))
            continue
        m = YEAR_RE.search(c)
        if m:
            mon, day, yr = m.groups()
            if mon.capitalize() not in MONTHS:
                continue
            blocks.append((i, 12,
                           date(int(yr), MONTHS[mon.capitalize()], int(day))))

    results = []
    for bi, (start, months, pend) in enumerate(blocks):
        end = blocks[bi + 1][0] if bi + 1 < len(blocks) else min(start + 60, len(lines))
        window = lines[start:min(end, start + 60)]
        # must look like the geographic-markets table
        joined = "\n".join(clean_line(x) for x in window)
        if not re.search(r"Primary geograph", joined):
            continue
        geo_vals = {}
        ncols = None
        for ln in window:
            c = clean_line(ln)
            for label, key in GEOS:
                if key in geo_vals:
                    continue
                # anchor at line start (after whitespace) to avoid narrative text
                stripped = c.strip()
                stripped = re.sub(r"^(Primary\s+geograph\w*\s*)?markets:\s*", "",
                                  stripped, flags=re.I)
                if not stripped.lower().startswith(label.lower()):
                    continue
                c = stripped
                v = nums_after(label, c)
                if len(v) >= 4:
                    geo_vals[key] = v
                    ncols = ncols or len(v)
        if len(geo_vals) >= 5:
            results.append(dict(period_end=pend, months=months,
                                geo=geo_vals, src=os.path.basename(path)))
    return results


def main():
    files = sorted(glob.glob(os.path.join(CORPUS, "*10q*.md")) +
                   glob.glob(os.path.join(CORPUS, "*10k*.md")))
    # period_end -> months -> {geo: [vals]}  (dedupe; prefer richest parse)
    store = {}
    for f in files:
        for r in parse_file(f):
            k = (r["period_end"], r["months"])
            def score(x):
                return (max((len(v) for v in x["geo"].values()), default=0),
                        len(x["geo"]))
            if k not in store or score(r) > score(store[k]):
                store[k] = r

    w = csv.writer(sys.stdout)
    w.writerow(["period_end", "months", "geography", "cols", "values", "source"])
    for (pend, months), r in sorted(store.items()):
        for geo, vals in r["geo"].items():
            w.writerow([pend.isoformat(), months, geo, len(vals),
                        "|".join(str(x) for x in vals), r["src"]])


if __name__ == "__main__":
    main()
