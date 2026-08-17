#!/usr/bin/env python3
"""
Parse Deere's revenue-recognition footnote segment x geography matrix
(and the major-product-lines block) out of the offline corpus.

Only the FIRST (three-months) matrix in each 10-Q is taken; the year-to-date
matrix that follows it is captured separately and labelled.

Every matrix is validated: each row must sum to its stated row total and each
column to its stated column total.  Failures are reported, never patched.

Standard library only.
"""
import json
import os
import re
import sys

CORPUS = ("/Users/cor/Documents/projects/agents-vs-wall-street-starter/"
          "challenge/offline-data/deere")

ZW = dict.fromkeys(map(ord, "​‌‍﻿­"), None)

REGIONS = ["United States", "Canada", "Western Europe",
           "Central Europe and CIS", "Latin America",
           "Asia, Africa, Oceania, and Middle East"]


def clean(s):
    s = s.translate(ZW).replace(" ", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", s).strip()


def split_row(line):
    line = line.strip()
    if not line.startswith("|"):
        return None
    cells = line.split("|")
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [clean(c) for c in cells]


def is_sep(cells):
    return bool(cells) and all(
        re.fullmatch(r":?-{2,}:?", c or "") for c in cells if c != "")


def nums(cells):
    out = []
    for c in cells:
        t = c.replace("$", "").replace(",", "").strip()
        if re.fullmatch(r"\(?\d+\)?", t):
            v = int(t.strip("()"))
            out.append(-v if t.startswith("(") else v)
    return out


PERIOD = re.compile(r"(Three|Six|Nine|Twelve) Months Ended ([A-Z][a-z]+ \d{1,2}, \d{4})")
MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}


def iso(s):
    m = re.match(r"([A-Z][a-z]+) (\d{1,2}), (\d{4})", s)
    return "%s-%02d-%02d" % (m.group(3), MONTHS[m.group(1)], int(m.group(2)))


def parse_file(path):
    fn = os.path.basename(path)
    lines = open(path, encoding="utf-8").read().split("\n")
    matrices = []
    i = 0
    while i < len(lines):
        cells = split_row(lines[i])
        if cells is None:
            i += 1
            continue
        start = i
        rows = []
        while i < len(lines):
            c = split_row(lines[i])
            if c is None:
                break
            if not is_sep(c):
                rows.append(c)
            i += 1
        labels = " || ".join(r[0] for r in rows if r)
        if "Primary geographic markets" not in labels:
            continue

        # A single pipe-table region often concatenates the three-month and the
        # year-to-date matrices with no blank line between them.  Start a fresh
        # matrix every time a "<N> Months Ended <date>" header row appears,
        # otherwise the later block silently overwrites the earlier one.
        cur = None
        pending = None
        section = None
        for r in rows:
            m = PERIOD.search(" ".join(r))
            if m:
                if cur is not None:
                    matrices.append(cur)
                cur = {"file": fn, "line": start + 1,
                       "period": {"months": m.group(1), "end": iso(m.group(2))},
                       "geo": {}, "product_lines": {}, "totals": None}
                section = None
                pending = None
                continue
            if cur is None:
                cur = {"file": fn, "line": start + 1, "period": None,
                       "geo": {}, "product_lines": {}, "totals": None}
            geo, prod = cur["geo"], cur["product_lines"]
            lab = r[0]
            if "Primary geographic markets" in lab:
                section = "geo"
                continue
            if "Major product lines" in lab:
                section = "prod"
                continue
            if "Timing of revenue" in lab or "revenue recognition" in lab.lower():
                section = "timing"
                continue
            v = nums(r[1:])
            if lab and not v:
                # a region name wrapped across two table rows
                pending = lab
                continue
            if not lab and pending:
                lab, pending = pending + " " + "", pending
                lab = pending
                pending = None
            elif pending:
                lab = pending + " " + lab
                pending = None
            if not v:
                continue
            if lab.lower().startswith("total"):
                if section == "geo" and cur["totals"] is None:
                    cur["totals"] = v
                continue
            if section == "geo":
                geo[lab] = v
            elif section == "prod":
                prod[lab] = v

        if cur is not None:
            matrices.append(cur)
    return matrices


def validate(mx):
    """Rows must sum to their stated row total; columns to the column total."""
    issues = []
    geo = mx["geo"]
    seg_cols = 4  # PPA SAT CF FS  (+ total)
    col_sums = [0] * seg_cols
    row_total_sum = 0
    for region, v in geo.items():
        if len(v) != seg_cols + 1:
            issues.append("%s: expected %d cells, got %d %r"
                          % (region, seg_cols + 1, len(v), v))
            continue
        if sum(v[:seg_cols]) != v[seg_cols]:
            issues.append("row %s: %d != stated %d" % (region, sum(v[:seg_cols]), v[seg_cols]))
        for k in range(seg_cols):
            col_sums[k] += v[k]
        row_total_sum += v[seg_cols]
    t = mx["totals"]
    if t and len(t) == seg_cols + 1:
        for k in range(seg_cols):
            if col_sums[k] != t[k]:
                issues.append("col %d: %d != stated %d" % (k, col_sums[k], t[k]))
        if row_total_sum != t[seg_cols]:
            issues.append("grand total: %d != stated %d" % (row_total_sum, t[seg_cols]))
    else:
        issues.append("no usable stated totals row")
    return issues


def main():
    want = sys.argv[1:] or None
    fdir = os.path.join(CORPUS, "filings")
    out = []
    for fn in sorted(os.listdir(fdir)):
        if not fn.endswith(".md"):
            continue
        if want and not any(w in fn for w in want):
            continue
        for mx in parse_file(os.path.join(fdir, fn)):
            mx["validation"] = validate(mx)
            out.append(mx)
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
