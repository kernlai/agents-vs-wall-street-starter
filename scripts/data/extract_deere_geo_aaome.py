#!/usr/bin/env python3
"""
Extract Deere's ASC 606 revenue-recognition footnote geography rows
(focus: 'Asia, Africa, Oceania, and Middle East', formerly
'Asia, Africa, Australia, New Zealand, and Middle East') from the
offline corpus of 10-Q / 10-K filings.

Output: raw long-format rows (one per period x segment) to stdout as CSV.
The markdown tables come from several different PDF->MD converters, so the
parser is deliberately tolerant: it tracks the most recent period header and
then grabs the numeric cells on (or immediately after) the geography label.

Usage:
  python3 extract_deere_geo_aaome.py > /tmp/aaome_raw.csv
"""
import re
import sys
import glob
import os

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"

PERIOD_RE = re.compile(
    r"(Three|Six|Nine|Twelve)\s+Months?\s+Ended\s+([A-Z][a-z]+\.?\s+\d{1,2},?\s+\d{4})")
YEAR_RE = re.compile(
    r"(?:For the\s+)?Years?\s+Ended\s+([A-Z][a-z]+\.?\s+\d{1,2},?\s+\d{4})"
    r"(?:,?\s+([A-Z][a-z]+\.?\s+\d{1,2},?\s+\d{4}))?"
    r"(?:,?\s+and\s+([A-Z][a-z]+\.?\s+\d{1,2},?\s+\d{4}))?")

# geography labels, in the order they appear in the footnote
GEOS = [
    ("United States", re.compile(r"United\s+States")),
    ("Canada", re.compile(r"^\|?\s*Canada\b")),
    ("Western Europe", re.compile(r"Western\s+Europe")),
    ("Central Europe and CIS", re.compile(r"Central\s+Europe")),
    ("Latin America", re.compile(r"Latin\s*\n?\s*America")),
    ("Asia, Africa, Oceania, and Middle East", re.compile(r"Asia,\s*Africa")),
]

NUM = re.compile(r"\(?\$?\s*(\d[\d,]*)\)?")


def numbers_in(text):
    """Pull integer cells out of a table line, dropping $ and separators."""
    # remove zero-width spaces used as empty cells
    text = text.replace("​", " ")
    out = []
    for m in re.finditer(r"\$?\s*(\d{1,3}(?:,\d{3})+|\d+)", text):
        tok = m.group(1).replace(",", "")
        out.append(int(tok))
    return out


def parse_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")

    rows = []
    period = None
    fname = os.path.basename(path)

    for i, line in enumerate(lines):
        clean = line.replace("​", " ")

        m = PERIOD_RE.search(clean)
        if m:
            # a header line repeated across columns still yields one period
            period = (m.group(1), re.sub(r"\s+", " ", m.group(2)).replace(",", "").strip())
            continue
        y = YEAR_RE.search(clean)
        if y and "Ended" in clean:
            period = ("Twelve", re.sub(r"\s+", " ", y.group(1)).replace(",", "").strip())
            continue

        if re.search(r"Asia,\s*Africa", clean):
            nums = numbers_in(clean)
            # label may wrap; numbers can be on this line or the next 1-2
            j = i
            while len(nums) < 4 and j + 1 < len(lines) and j - i < 3:
                j += 1
                nxt = lines[j].replace("​", " ")
                if re.search(r"Total|Major product|Primary", nxt):
                    break
                nums += numbers_in(nxt)
            if len(nums) >= 4 and period:
                rows.append({
                    "file": fname,
                    "period_type": period[0],
                    "period_end_raw": period[1],
                    "nums": nums,
                })
    return rows


def main():
    w = sys.stdout
    w.write("file,period_type,period_end_raw,n_values,values\n")
    for path in sorted(glob.glob(os.path.join(CORPUS, "*.md"))):
        for r in parse_file(path):
            w.write("%s,%s,%s,%d,%s\n" % (
                r["file"], r["period_type"], r["period_end_raw"],
                len(r["nums"]), "|".join(str(x) for x in r["nums"])))


if __name__ == "__main__":
    main()
