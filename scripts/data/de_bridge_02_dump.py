#!/usr/bin/env python3
"""Step 2a: locate every operating-profit-bridge block in the slide decks and
dump it raw, so the OCR format variants can be classified before parsing."""
import os
import re
import sys

SLIDES = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/slides"

SEG_HINTS = [
    (re.compile(r"production\s*(&|and)\s*precision\s*ag", re.I), "PPA"),
    (re.compile(r"small\s*ag(riculture)?\s*(&|and)\s*turf", re.I), "SAT"),
    (re.compile(r"construction\s*(&|and)\s*forestry", re.I), "CF"),
    (re.compile(r"agriculture\s*(&|and)\s*turf", re.I), "AT"),
]
MARK = re.compile(r"operating\s*profit\s*comparison", re.I)


def blocks(text):
    """Yield (char_index, block_text) for each bridge chart region."""
    out = []
    for m in MARK.finditer(text):
        start = m.start()
        # widen to the enclosing paragraph / fenced json block
        lo = text.rfind("\n\n", 0, start)
        lo = 0 if lo < 0 else lo + 2
        hi = text.find("\n\n", m.end())
        hi = len(text) if hi < 0 else hi
        # json code fences can contain blank lines; extend while unbalanced
        seg = text[lo:hi]
        while seg.count("```") % 2 == 1 and hi < len(text):
            nxt = text.find("\n\n", hi + 2)
            hi = len(text) if nxt < 0 else nxt
            seg = text[lo:hi]
        out.append((start, lo, hi, seg))
    return out


def segment_for(text, pos):
    best = None
    for pat, key in SEG_HINTS:
        for m in pat.finditer(text, 0, pos):
            if best is None or m.start() > best[0]:
                best = (m.start(), key)
    return best[1] if best else None


def main():
    for fn in sorted(os.listdir(SLIDES)):
        path = os.path.join(SLIDES, fn)
        text = open(path, encoding="utf-8").read()
        bs = blocks(text)
        if not bs:
            continue
        print("#" * 100)
        print("FILE", fn, "blocks:", len(bs))
        for (pos, lo, hi, seg) in bs:
            print("-" * 80, "SEGMENT GUESS:", segment_for(text, pos))
            print(seg[:2500])


if __name__ == "__main__":
    sys.exit(main())
