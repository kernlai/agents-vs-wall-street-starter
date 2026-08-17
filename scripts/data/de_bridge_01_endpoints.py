#!/usr/bin/env python3
"""
Step 1 of the Deere operating-profit-bridge pipeline.

Build the INDEPENDENT ground-truth table of segment operating profit by quarter
from the 8-K / 10-K earnings-release segment tables.  These endpoints are what
the (OCR-scrambled) slide bridges must reconcile TO.

Output: <scratch>/de_segment_op_profit.json
        { "2026Q2": {"PPA": {"cur":706,"pri":1148}, ...}, ... }
where cur = the reported quarter, pri = the same quarter one year earlier
(as printed in the same release, so restatements are handled consistently).

stdlib only.
"""
import json
import os
import re
import sys

FILINGS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"
OUT = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/de_segment_op_profit.json"

# Row label -> canonical segment key.  Deere reorganised segments effective
# FY2021 (PPA / SAT / CF).  Before that it was Agriculture & Turf / C&F.
SEG_PATTERNS = [
    (re.compile(r"^production\s*&\s*precision\s*ag", re.I), "PPA"),
    (re.compile(r"^small\s*ag\s*&\s*turf", re.I), "SAT"),
    (re.compile(r"^construction\s*&\s*forestry", re.I), "CF"),
    (re.compile(r"^agriculture\s*&\s*turf", re.I), "AT"),
]


def cells(line):
    return [c.strip().replace("​", "").strip() for c in line.strip().strip("|").split("|")]


NUM = re.compile(r"^\(?-?\$?\s*([\d,]+)\)?$")


def parse_num(tok):
    tok = tok.replace("$", "").strip()
    if not tok or tok in {"-", "—"}:
        return None
    neg = tok.startswith("(") and tok.endswith(")")
    m = NUM.match(tok)
    if not m:
        return None
    try:
        v = int(m.group(1).replace(",", ""))
    except ValueError:
        return None
    return -v if neg else v


def fiscal_from_filename(fn):
    """Return (fiscal_year, fiscal_quarter) of the period being REPORTED."""
    m = re.search(r"-(q[1-4]|fy)-", fn)
    date = fn[:10]
    year = int(date[:4])
    if not m:
        return None
    tag = m.group(1)
    if tag == "fy":
        return None
    q = int(tag[1])
    # Deere FY ends late Oct/early Nov.  A Q4/FY release published in Nov of
    # calendar year Y reports fiscal year Y.  Q1 published Feb of year Y is
    # fiscal Y.  So fiscal year == calendar year of publication in all cases.
    return (year, q)


def main():
    out = {}
    prov = {}
    for fn in sorted(os.listdir(FILINGS)):
        fq = fiscal_from_filename(fn)
        if not fq:
            continue
        fy, q = fq
        key = f"{fy}Q{q}"
        path = os.path.join(FILINGS, fn)
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")

        # Find the consolidated "Operating profit:" summary table row block.
        idxs = [i for i, ln in enumerate(lines)
                if re.match(r"^\|\s*(\*\*)?Operating profit:?\s*\*?", ln.strip(), re.I)
                and "|" in ln]
        found = {}
        for i in idxs:
            for j in range(i + 1, min(i + 10, len(lines))):
                ln = lines[j]
                if not ln.strip().startswith("|"):
                    break
                c = cells(ln)
                if not c:
                    break
                label = c[0].replace("*", "").strip()
                seg = None
                for pat, k in SEG_PATTERNS:
                    if pat.match(label):
                        seg = k
                        break
                if seg is None:
                    if re.match(r"^(total|financial services)", label, re.I):
                        continue
                    break
                nums = [parse_num(x) for x in c[1:]]
                nums = [n for n in nums if n is not None]
                # Layout: cur_qtr, pri_qtr, %chg, [cur_ytd, pri_ytd, %chg]
                if len(nums) >= 2:
                    found[seg] = {"cur": nums[0], "pri": nums[1]}
                    if len(nums) >= 6:
                        found[seg]["cur_ytd"] = nums[3]
                        found[seg]["pri_ytd"] = nums[4]
            if found:
                break

        # Fallback / supplement: the per-segment mini-tables, which are the only
        # form used in the pre-FY2021 releases (segments "Agriculture & Turf" and
        # "Construction & Forestry").  Header row is the segment name; a later row
        # begins "Operating profit" with cur, prior, %chg.
        for i, ln in enumerate(lines):
            if not ln.strip().startswith("|"):
                continue
            c = cells(ln)
            if not c:
                continue
            label = c[0].replace("&amp;", "&").replace("*", "").strip()
            seg = None
            for pat, k in SEG_PATTERNS:
                if pat.match(label):
                    seg = k
                    break
            if seg is None:
                continue
            if not any(re.search(r"quarter|month", x, re.I) for x in c[1:]):
                continue
            for j in range(i + 1, min(i + 8, len(lines))):
                c2 = cells(lines[j]) if lines[j].strip().startswith("|") else None
                if not c2:
                    break
                lab2 = c2[0].replace("*", "").strip()
                if re.match(r"^net sales\s*$", lab2, re.I):
                    nums = [parse_num(x) for x in c2[1:]]
                    nums = [n for n in nums if n is not None]
                    if len(nums) >= 2:
                        found.setdefault(seg, {})
                        found[seg]["sales_cur"] = nums[0]
                        found[seg]["sales_pri"] = nums[1]
                if re.match(r"^operating profit\s*$", lab2, re.I):
                    nums = [parse_num(x) for x in c2[1:]]
                    nums = [n for n in nums if n is not None]
                    if len(nums) >= 2:
                        found.setdefault(seg, {})
                        found[seg]["cur"] = nums[0]
                        found[seg]["pri"] = nums[1]
                    break

        # Consolidated "<Segment> net sales" rows fill any remaining sales gaps.
        for ln in lines:
            if not ln.strip().startswith("|"):
                continue
            c = cells(ln)
            if not c:
                continue
            label = c[0].replace("&amp;", "&").replace("*", "").strip()
            m2 = re.match(r"^(.*?)\s+net sales$", label, re.I)
            if not m2:
                continue
            seg = None
            for pat, k in SEG_PATTERNS:
                if pat.match(m2.group(1)):
                    seg = k
                    break
            if seg is None or seg not in found or "sales_cur" in found[seg]:
                continue
            nums = [parse_num(x) for x in c[1:]]
            nums = [n for n in nums if n is not None]
            if len(nums) >= 2:
                found[seg]["sales_cur"] = nums[0]
                found[seg]["sales_pri"] = nums[1]

        if not found:
            continue
        # Prefer 8-K over 10-K/10-Q for a given quarter (both may exist).
        rank = 0 if "8k" in fn else 1
        if key not in out or rank < prov.get(key, 9):
            out[key] = found
            prov[key] = rank
            out[key]["_source"] = fn

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(f"quarters with segment operating profit: {len(out)}")
    for k in sorted(out):
        segs = {s: v for s, v in out[k].items() if not s.startswith("_")}
        print(k, {s: (v["cur"], v["pri"]) for s, v in segs.items()}, out[k]["_source"][:24])


if __name__ == "__main__":
    sys.exit(main())
