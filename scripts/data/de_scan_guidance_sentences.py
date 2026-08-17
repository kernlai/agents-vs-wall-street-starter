#!/usr/bin/env python3
"""Scan the Deere offline corpus for guidance sentences (net income / EPS / segment
sales outlook) so they can be inspected before structured extraction.

Usage: python3 de_scan_guidance_sentences.py [outfile]
"""
import os, re, sys

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"

PATTERNS = [
    r"net income attributable to deere",
    r"net income .{0,40}forecast",
    r"forecast(?:ed)? .{0,60}net income",
    r"is (?:now )?(?:forecast|projected|expected|anticipated) to",
    r"are (?:now )?(?:forecast|projected|expected) to",
    r"full[- ]year net income",
    r"outlook",
]
RX = re.compile("|".join(PATTERNS), re.I)


def sentences(text):
    # split on sentence enders and on markdown table rows / newlines
    parts = re.split(r"(?<=[.!?])\s+|\n", text)
    return [p.strip() for p in parts if p.strip()]


def main():
    out = open(sys.argv[1], "w") if len(sys.argv) > 1 else sys.stdout
    for sub in ("filings", "slides", "call-transcripts"):
        d = os.path.join(CORPUS, sub)
        for fn in sorted(os.listdir(d)):
            path = os.path.join(d, fn)
            text = open(path, encoding="utf-8", errors="replace").read()
            hits = [s for s in sentences(text) if RX.search(s)]
            if not hits:
                continue
            print(f"\n===== {sub}/{fn}", file=out)
            for h in hits:
                print("  |", h[:600], file=out)
    if out is not sys.stdout:
        out.close()


if __name__ == "__main__":
    main()
