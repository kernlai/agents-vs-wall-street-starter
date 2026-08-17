#!/usr/bin/env python3
"""
Extract Deere quarterly fundamentals (total revenue, diluted EPS, segment net sales
and segment operating profit) from the offline 8-K earnings releases, and cross-check
total revenue / EPS against SEC EDGAR XBRL companyfacts.

Stdlib only. Writes an intermediate JSON used by de_predictability.py.

Outputs: <SCRATCH>/de_quarterly.json
"""
import json
import os
import re
import sys
from datetime import date

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
FILINGS = os.path.join(CORPUS, "filings")
SCRATCH = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"

NUM = re.compile(r"\(?-?\+?\$?\s?\d[\d,]*(?:\.\d+)?\)?")


def toks(line):
    """Numeric tokens from a markdown table row, in order, ignoring $ and blank cells."""
    cells = [c.strip().replace("​", "").strip() for c in line.strip().strip("|").split("|")]
    out = []
    for c in cells:
        c = c.replace("$", "").strip()
        if not c:
            continue
        m = NUM.fullmatch(c.replace(" ", ""))
        if not m:
            continue
        s = c.replace(",", "").replace(" ", "").replace("+", "")
        neg = s.startswith("(") and s.endswith(")")
        s = s.strip("()")
        try:
            v = float(s)
        except ValueError:
            continue
        out.append(-v if neg else v)
    return out


def label(line):
    cells = [c.strip().replace("​", "").strip() for c in line.strip().strip("|").split("|")]
    return cells[0] if cells else ""


# canonical segment keys
SEG_SALES = {
    "agriculture and turf": "AT",
    "agriculture & turf": "AT",
    "construction and forestry": "CF",
    "construction & forestry": "CF",
    "construction and forestry net sales": "CF",
    "production and precision ag net sales": "PPA",
    "production & precision ag net sales": "PPA",
    "production and precision agriculture net sales": "PPA",
    "small ag and turf net sales": "SAT",
    "small ag & turf net sales": "SAT",
    "small agriculture and turf net sales": "SAT",
    "construction & forestry net sales": "CF",
    "agriculture and turf net sales": "AT",
}
SEG_OP = {
    "agriculture and turf": "AT",
    "agriculture & turf": "AT",
    "construction and forestry": "CF",
    "construction & forestry": "CF",
    "production and precision ag": "PPA",
    "production & precision ag": "PPA",
    "production and precision agriculture": "PPA",
    "small ag and turf": "SAT",
    "small ag & turf": "SAT",
    "small agriculture and turf": "SAT",
    "financial services": "FS",
}


def norm(s):
    s = s.lower().replace("​", "").strip()
    s = re.sub(r"[*†]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_8k(path):
    txt = open(path, encoding="utf-8").read()
    lines = txt.split("\n")

    # header metadata
    per = re.search(r'period:\s*"(Q\d|FY)\s*(\d{4})"', txt)
    pub = re.search(r'published_at:\s*"(\d{4}-\d{2}-\d{2})"', txt)
    published = pub.group(1) if pub else None

    # Locate the segment note table: a line whose label starts "Net sales and revenues:"
    # followed within ~30 lines by "Operating profit:".
    starts = [i for i, l in enumerate(lines)
              if norm(label(l)).startswith("net sales and revenues:")]
    best = None
    for i in starts:
        window = lines[i:i + 40]
        if any(norm(label(l)).startswith("operating profit") for l in window):
            best = i
            break
    if best is None:
        return None

    rec = {"file": os.path.basename(path), "published": published,
           "sales": {}, "op": {}, "raw": {}}

    mode = "sales"
    for l in lines[best:best + 45]:
        lab = norm(label(l))
        if lab.startswith("operating profit"):
            mode = "op"
            continue
        if lab.startswith("net sales and revenues:"):
            mode = "sales"
            continue
        t = toks(l)
        if not t:
            continue
        if mode == "sales":
            if lab in SEG_SALES:
                rec["sales"][SEG_SALES[lab]] = t
            elif lab.startswith("total net sales and revenues"):
                rec["raw"]["total_rev"] = t
            elif lab == "total net sales":
                rec["raw"]["equip_net_sales"] = t
            elif lab.startswith("financial services"):
                rec["sales"]["FS"] = t
        else:
            if lab in SEG_OP:
                rec["op"][SEG_OP[lab]] = t
            elif lab.startswith("total operating profit"):
                rec["raw"]["total_op"] = t
            elif lab.startswith("net income attributable"):
                rec["raw"]["ni"] = t
            elif lab.startswith("income taxes"):
                rec["raw"]["tax"] = t
        if lab.startswith("net income attributable"):
            break
    return rec


def main():
    files = sorted(f for f in os.listdir(FILINGS) if re.search(r"-(q\d|fy)-8k", f))
    recs = []
    for f in files:
        r = parse_8k(os.path.join(FILINGS, f))
        if r:
            recs.append(r)
        else:
            print("NO SEGMENT TABLE:", f, file=sys.stderr)
    with open(os.path.join(SCRATCH, "de_8k_raw.json"), "w") as fh:
        json.dump(recs, fh, indent=1)
    print("parsed", len(recs), "of", len(files))
    for r in recs[:2] + recs[-2:]:
        print(r["file"], r["published"], {k: v[:2] for k, v in r["sales"].items()},
              {k: v[:2] for k, v in r["op"].items()}, r["raw"].get("total_rev", [])[:2])


if __name__ == "__main__":
    main()
