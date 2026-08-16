#!/usr/bin/env python3
"""Surface candidate historical figures from the offline corpus, with citations.

Run from the repo root:

    python3 tier1/find_history.py            # all four companies
    python3 tier1/find_history.py HD ADI     # a subset

Writes research/tier1-candidates-<TICKER>.md containing, for each metric,
matching lines from the most recent filings (8-Ks first — they carry the
actuals) with file paths and line numbers. You confirm real values into
tier1/history.json; this script deliberately does NOT auto-fill it, because
a wrong historical poisons every forecast downstream.

Dependency-free (stdlib only).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "challenge" / "offline-data"
OUT_DIR = ROOT / "research"

COMPANY_DIRS = {
    "HD": "home-depot",
    "ADI": "analog-devices",
    "DE": "deere",
    "HAS": "hays",
}

# Case-insensitive search patterns per metric. Keep them loose: the goal is
# recall with citations, not precision. Numbers are matched nearby on the line.
METRIC_PATTERNS: dict[str, dict[str, list[str]]] = {
    "HD": {
        "Net sales": [r"\bnet sales\b", r"\bsales of \$"],
        "Adjusted diluted EPS": [r"adjusted diluted (earnings per share|eps)"],
        "Comparable sales, total company": [r"\bcomparable sales\b", r"\bcomp sales\b"],
    },
    "ADI": {
        "Revenue": [r"\brevenue of\b", r"\brevenue was\b", r"^\s*\|?\s*revenue\b"],
        "Adjusted diluted EPS": [r"adjusted (diluted )?(eps|earnings per share)"],
        "Adjusted gross margin": [r"adjusted gross margin"],
    },
    "DE": {
        "Worldwide net sales and revenues": [r"net sales and revenues"],
        "Diluted EPS (GAAP)": [r"\bper share\b.*diluted", r"diluted.*\bper share\b"],
        "Production & Precision Ag operating profit": [
            r"production (&|and) precision ag",
        ],
    },
    "HAS": {
        "Net fees": [r"\bnet fees\b"],
        "Pre-exceptional basic EPS": [r"basic (earnings per share|eps)", r"pre-exceptional.*eps"],
        "Pre-exceptional operating profit": [r"operating profit"],
    },
}

HAS_NUMBER = re.compile(r"\d")
DATE_PREFIX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})__")
MAX_FILES_PER_KIND = 16  # 8 was too few: it cut off the Aug-2025 same-quarter actuals
MAX_HITS_PER_METRIC = 40


def recent_files(company_dir: Path) -> list[Path]:
    """Most recent filings first, then transcripts, then slides."""
    picked: list[Path] = []
    for kind in ("filings", "call-transcripts", "slides"):
        folder = company_dir / kind
        if not folder.is_dir():
            continue
        dated = [p for p in folder.glob("*.md") if DATE_PREFIX.match(p.name)]
        dated.sort(key=lambda p: p.name, reverse=True)  # date prefix sorts lexically
        picked.extend(dated[:MAX_FILES_PER_KIND])
    return picked


def scan(ticker: str) -> str:
    company_dir = CORPUS / COMPANY_DIRS[ticker]
    if not company_dir.is_dir():
        return f"# {ticker}\n\nCorpus folder not found: {company_dir}\n"

    lines_out = [f"# {ticker} — candidate historical figures\n"]
    files = recent_files(company_dir)
    lines_out.append(f"Scanned {len(files)} most-recent documents.\n")

    for metric, patterns in METRIC_PATTERNS[ticker].items():
        regexes = [re.compile(p, re.IGNORECASE) for p in patterns]
        lines_out.append(f"\n## {metric}\n")
        hits = 0
        for path in files:
            try:
                text = path.read_text(errors="replace")
            except OSError:
                continue
            for n, line in enumerate(text.splitlines(), 1):
                if hits >= MAX_HITS_PER_METRIC:
                    break
                stripped = line.strip()
                if not stripped or not HAS_NUMBER.search(stripped):
                    continue
                if any(rx.search(stripped) for rx in regexes):
                    rel = path.relative_to(ROOT)
                    snippet = stripped if len(stripped) <= 240 else stripped[:237] + "..."
                    lines_out.append(f"- `{rel}:{n}` — {snippet}")
                    hits += 1
            if hits >= MAX_HITS_PER_METRIC:
                lines_out.append(f"- ... capped at {MAX_HITS_PER_METRIC} hits")
                break
        if hits == 0:
            lines_out.append("- (no matching lines — widen METRIC_PATTERNS for this one)")
    return "\n".join(lines_out) + "\n"


def main() -> int:
    tickers = [t.upper() for t in sys.argv[1:]] or list(COMPANY_DIRS)
    unknown = [t for t in tickers if t not in COMPANY_DIRS]
    if unknown:
        print(f"Unknown ticker(s): {', '.join(unknown)}. Use: {', '.join(COMPANY_DIRS)}")
        return 1
    OUT_DIR.mkdir(exist_ok=True)
    for ticker in tickers:
        out = OUT_DIR / f"tier1-candidates-{ticker}.md"
        out.write_text(scan(ticker))
        print(f"wrote {out.relative_to(ROOT)}")
    print("\nConfirm real values into tier1/history.json (with sources), "
          "then run: python3 tier1/forecast.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())