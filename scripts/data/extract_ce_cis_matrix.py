#!/usr/bin/env python3
"""
Extract the "Central Europe and CIS" row of Deere's ASC 606 revenue-recognition
footnote (net sales & revenues by primary geographic market x segment) from the
offline corpus of 10-Q / 10-K filings.

Output: a raw dump of every (filing, period-header, CE&CIS row) triple, which the
caller then reconciles into a quarterly series.

Usage: python3 extract_ce_cis_matrix.py [--csv]
"""
import os
import re
import sys
import glob

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"

PERIOD_RE = re.compile(
    r"(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+([A-Z][a-z]+\.?\s+\d{1,2},?\s+\d{4})",
    re.I,
)
# 10-K annual blocks are headed by a bare fiscal year on its own table row
FY_RE = re.compile(r"^\|?\s*(20\d\d)\s*\|")
CE_RE = re.compile(r"Central\s*\|?\s*$|Central\s+Europe|Europe\s+and\s+CIS", re.I)
NUM_RE = re.compile(r"\(?\$?\s*-?[\d,]+\)?")


def numbers(s):
    out = []
    for tok in re.findall(r"\(?\$?\s?(-?[\d][\d,]*)\)?", s):
        t = tok.replace(",", "")
        try:
            out.append(int(t))
        except ValueError:
            pass
    return out


def scan(path):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    cur_period = None
    for i, line in enumerate(lines):
        m = PERIOD_RE.search(line)
        if m:
            cur_period = f"{m.group(1).title()} Months Ended {m.group(2)}"
        fy = FY_RE.match(line.strip())
        if fy and "Central" not in line:
            cur_period = f"FY{fy.group(1)}"
        if "Central" in line and ("Europe" in line or "Europe" in "".join(lines[i:i + 2])):
            blob = line
            if "Europe and CIS" not in line and i + 1 < len(lines):
                blob = line + " " + lines[i + 1]
            if "Europe and CIS" not in blob:
                continue
            nums = numbers(blob.split("CIS", 1)[1])
            rows.append((os.path.basename(path), cur_period, nums, blob.strip()[:160]))
    return rows


def main():
    files = sorted(glob.glob(os.path.join(CORPUS, "*10q*.md"))) + sorted(
        glob.glob(os.path.join(CORPUS, "*10k*.md"))
    )
    for f in files:
        for fname, period, nums, raw in scan(f):
            print(f"{fname}\t{period}\t{nums}\t{raw}")


if __name__ == "__main__":
    main()
