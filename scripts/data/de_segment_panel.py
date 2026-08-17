#!/usr/bin/env python3
"""
Build Deere's quarterly segment net-sales / operating-profit panel from the
8-K press-release SEGMENT DATA tables in the offline corpus.

Each 8-K carries current-quarter AND prior-year-quarter values, so the panel is
double-sourced for every period: any disagreement is reported, never averaged.
This panel is the independent check on the slide-deck bridge endpoints.
"""
import re, os, glob, json, sys, argparse

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"

SEGROWS = {
    "PPA_sales": r"Production\s*&\s*Precision\s*Ag(?:riculture)?\s*net sales",
    "SAT_sales": r"Small\s*Ag(?:riculture)?\s*&\s*Turf\s*net sales",
    "CF_sales":  r"Construction\s*&\s*Forestry\s*net sales",
    "TOTAL_rev": r"Total net sales and revenues",
    "PPA_op":    r"Production\s*&\s*Precision\s*Ag(?:riculture)?\s*\|",
    "SAT_op":    r"Small\s*Ag(?:riculture)?\s*&\s*Turf\s*\|",
    "CF_op":     r"Construction\s*&\s*Forestry\s*\|",
    "FS_op":     r"Financial Services\s*\|",
    "NI":        r"Net income attributable to Deere",
}


def norm(s):
    for a, b in [("&amp;", "&"), ("​", ""), ("​", ""), ("&nbsp;", " ")]:
        s = s.replace(a, b)
    return s


def nums(line):
    out = []
    for tok in re.findall(r"\(?-?[\d,]+\.?\d*\)?%?", line):
        if tok.endswith("%"):
            continue
        neg = tok.startswith("(")
        t = tok.strip("()").replace(",", "")
        if not re.fullmatch(r"-?\d+", t):
            continue
        v = int(t)
        out.append(-v if neg else v)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out"); a = ap.parse_args()
    panel = {}          # (fy, q, key) -> list of (value, source)
    for path in sorted(glob.glob(os.path.join(CORPUS, "filings", "*8k*.md"))):
        fn = os.path.basename(path)
        m = re.search(r"-(q[1-4])-8k", fn)
        if not m:
            continue
        q = int(m.group(1)[1])
        pub = fn[:10]
        pubyear = int(pub[:4])
        # Deere FY ends late Oct/early Nov: Q1 8-K in Feb, Q2 in May, Q3 in Aug,
        # Q4 in Nov of the SAME fiscal year.
        fy = pubyear
        txt = norm(open(path, encoding="utf-8").read())
        # locate the SEGMENT DATA / press-release table
        idx = txt.find("Operating profit:")
        if idx < 0:
            continue
        sales_block = txt[max(0, idx - 4000): idx]
        op_block = txt[idx: idx + 4000]
        for key, pat in SEGROWS.items():
            # operating-profit rows must come from BELOW the "Operating profit:"
            # header, otherwise the identically-named net-sales row is matched
            block = op_block if key.endswith("_op") or key == "NI" else sales_block
            mm = re.search(r"^\|\s*" + pat + r".*$", block, re.M | re.I)
            if not mm:
                continue
            v = nums(mm.group(0))
            # expect [cur_qtr, prior_qtr, %chg, cur_ytd, prior_ytd, %chg]
            # % changes are stripped only when suffixed with %; Deere writes
            # them bare, so filter by position using length heuristics
            if len(v) >= 2:
                panel.setdefault((fy, q, key), []).append((v[0], pub + " current"))
                panel.setdefault((fy - 1, q, key), []).append((v[1] if len(v) < 3 else v[1],
                                                               pub + " prior-year"))
    # collapse + conflict report
    rows, conflicts = [], []
    for (fy, q, key), vals in sorted(panel.items()):
        uniq = sorted(set(v for v, _ in vals))
        if len(uniq) > 1:
            conflicts.append({"fy": fy, "q": q, "key": key, "values": vals})
        rows.append({"fy": fy, "q": q, "key": key, "value": uniq[0],
                     "n_sources": len(vals), "conflict": len(uniq) > 1,
                     "sources": [s for _, s in vals]})
    out = {"rows": rows, "conflicts": conflicts}
    if a.out:
        open(a.out, "w").write(json.dumps(out, indent=1))
    print(f"rows={len(rows)} conflicts={len(conflicts)}", file=sys.stderr)
    for r in rows:
        if r["key"].endswith("_op"):
            print(f"{r['fy']} Q{r['q']} {r['key']:>10} {r['value']:>8} "
                  f"n={r['n_sources']}{' CONFLICT' if r['conflict'] else ''}", file=sys.stderr)


if __name__ == "__main__":
    main()
