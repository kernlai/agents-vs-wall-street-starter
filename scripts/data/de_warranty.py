#!/usr/bin/env python3
"""
Extract Deere's product-warranty liability rollforward from every 10-Q/10-K in
the corpus.

The bridge shows warranty as a separate, volatile line of segment profit, but
the bridge is a year-on-year DELTA. The rollforward gives the level: new
product warranty accruals (the P&L charge as booked at point of sale) and
claims paid. New accruals are the leading indicator -- they move before the
bridge delta does.

Each filing carries the current AND prior-year period, so most quarters are
double-sourced; disagreements are reported, not averaged.
"""
import re, os, glob, json, sys, argparse

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
ROWS = {
    "warranty_beginning_balance": r"Beginning of period balance",
    "warranty_claims_paid":       r"Warranty claims paid",
    "warranty_new_accruals":      r"(?:New product warranty accruals|Provision for warranties)",
    "warranty_fx":                r"Foreign exchange",
    "warranty_ending_balance":    r"End of period balance",
}


def nums(line):
    out = []
    for tok in re.findall(r"\(?\$?\s?-?[\d,]+\)?", line):
        neg = tok.strip().startswith("(")
        t = tok.replace("(", "").replace(")", "").replace("$", "").replace(",", "").strip()
        if not re.fullmatch(r"-?\d+", t):
            continue
        v = int(t)
        out.append(-v if neg else v)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out"); a = ap.parse_args()
    recs = []
    for path in sorted(glob.glob(os.path.join(CORPUS, "filings", "*.md"))):
        fn = os.path.basename(path)
        m = re.search(r"-(q[1-4]|fy)-(10q|10k)", fn)
        if not m:
            continue
        txt = open(path, encoding="utf-8").read().replace("​", "")
        i = txt.find("changes in the warranty liability")
        if i < 0:
            continue
        block = txt[i: i + 2500]
        # period-end labels sit in the header rows of the table
        hdr = re.findall(r"(January|February|March|April|May|June|July|August|"
                         r"September|October|November|December)\s+(\d{1,2})[ ,|]+(20\d\d)", block)
        got = {}
        for key, pat in ROWS.items():
            mm = re.search(r"^\|\s*" + pat + r".*$", block, re.M | re.I)
            if mm:
                got[key] = nums(mm.group(0))
        if not got:
            continue
        recs.append({"file": fn, "published": fn[:10],
                     "period_labels": [f"{h[0]} {h[1]} {h[2]}" for h in hdr[:6]],
                     "values": got})
    if a.out:
        open(a.out, "w").write(json.dumps(recs, indent=1))
    for r in recs:
        print(r["published"], r["period_labels"][:4],
              {k: v[:4] for k, v in r["values"].items()}, file=sys.stderr)
    print(f"filings_with_warranty_table={len(recs)}", file=sys.stderr)


if __name__ == "__main__":
    main()
