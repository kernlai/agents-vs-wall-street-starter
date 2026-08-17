#!/usr/bin/env python3
"""
Parse Deere & Company ASC-606 revenue-recognition disaggregation tables
(the "Revenue Recognition" note) out of the offline filings corpus.

Three sections per table:
  Primary geographic markets  |  Major product lines  |  Timing of revenue recognition

Only markdown pipe-tables are parsed.  Column positions are LEARNED per table
from an anchor row that carries a full set of numbers, so blank cells stay
blank (a product line belongs to exactly one segment; collapsing blanks would
silently mis-assign it).

Every table is validated: section rows must sum to the stated section Total row
and each column must sum down to it.  Tables that fail are kept but flagged;
where the same period is available from a second (clean) rendering the clean
one wins.

Standard library only.
"""
import re, os, glob, json, sys
from collections import defaultdict

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"
SCRATCH = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"

ZW = ["​", "‌", "‍", "﻿", " ", " ", " "]

def clean(s):
    for z in ZW:
        s = s.replace(z, " ")
    return s.replace("–", "-").replace("—", "-").replace("’", "'")

NUM = re.compile(r"^\(?\$?\s*-?[\d,]+\)?$")

def to_num(c):
    c = (c or "").strip()
    if not c or c in ("$", "-", "--"):
        return None
    if not NUM.match(c):
        return None
    neg = c.startswith("(")
    c = c.strip("()").replace("$", "").replace(",", "").strip()
    if not re.fullmatch(r"-?\d+", c):
        return None
    return -int(c) if neg else int(c)

MONTHS = ("January February March April May June July August September "
          "October November December").split()
MON_NUM = {m: i + 1 for i, m in enumerate(MONTHS)}
PERIOD_RE = re.compile(r"(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+(%s)\s+(\d{1,2}),?\s+(\d{4})"
                       % "|".join(MONTHS), re.I)
DUR = {"three": 3, "six": 6, "nine": 9, "twelve": 12}
# a period caption wrapped over two physical lines: "...Ended January 26," / "2025 | PPA | ..."
PARTIAL_RE = re.compile(r"(Three|Six|Nine|Twelve)\s+Months\s+Ended\s+(%s)\s+(\d{1,2}),\s*$"
                        % "|".join(MONTHS), re.I)

def wrapped_period(prev_joined, joined):
    mp = PARTIAL_RE.search(prev_joined or "")
    if not mp:
        return None
    my = re.match(r"^\s*(20\d\d)\b", joined or "")
    if not my:
        return None
    return ("PE", DUR[mp.group(1).lower()], MON_NUM[mp.group(2).capitalize()],
            int(mp.group(3)), int(my.group(1)))

SEC_GEO = re.compile(r"^primary geograph", re.I)
SEC_PL  = re.compile(r"^major product lines", re.I)
SEC_TIM = re.compile(r"^(revenue\s+recognized\s*:|timing of revenue recognition)", re.I)

def norm(s):
    return re.sub(r"[^a-z]", "", (s or "").lower())

SEG_SETS = {
    ("ppa", "sat", "cf", "fs", "total"): ["PPA", "SAT", "CF", "FS", "Total"],
    ("productionprecisionag", "smallagturf", "constructionforestry", "financialservices", "total"):
        ["PPA", "SAT", "CF", "FS", "Total"],
    ("agricultureandturf", "constructionandforestry", "financialservices", "total"):
        ["Agriculture and Turf", "Construction and Forestry", "Financial Services", "Total"],
}

# as-disclosed product-line label -> canonical label + owning segment
PL_CANON = {
    "largeagriculture": ("Large agriculture", "AT"),
    "productionagriculture": ("Production agriculture", "PPA"),
    "smallagriculture": ("Small agriculture", "SATorAT"),
    "turf": ("Turf", "SATorAT"),
    "construction": ("Construction", "CF"),
    "compactconstruction": ("Compact construction", "CF"),
    "roadbuilding": ("Roadbuilding", "CF"),
    "forestry": ("Forestry", "CF"),
    "financialproducts": ("Financial products", "*"),
    "other": ("Other", "*"),
}
TIM_CANON = {
    "revenuerecognizedatapointintime": "At a point in time",
    "atapointintime": "At a point in time",
    "revenuerecognizedovertime": "Over time",
    "overtime": "Over time",
    "pointintime": "At a point in time",
    "revenuerecognizedatapointin": "At a point in time",
    "revenuerecognizedatapointintimetime": "At a point in time",
    "time": "At a point in time",
}
GEO_CANON = {
    "unitedstates": "United States",
    "marketsunitedstates": "United States",
    "canada": "Canada",
    "westerneurope": "Western Europe",
    "centraleuropeandcis": "Central Europe and CIS",
    "latinamerica": "Latin America",
    "asiaafricaoceaniaandmiddleeast": "Asia, Africa, Oceania, and Middle East",
    "asiaafricaaustralianewzealandandmiddleeast": "Asia, Africa, Australia, New Zealand, and Middle East",
    "newzealandandmiddleeast": "Asia, Africa, Australia, New Zealand, and Middle East",
    "zealandandmiddleeast": "Asia, Africa, Australia, New Zealand, and Middle East",
}

def split_cells(line):
    s = line.strip()
    if s.startswith("|"): s = s[1:]
    if s.endswith("|"):   s = s[:-1]
    return [re.sub(r"\s+", " ", c).strip() for c in s.split("|")]

def is_sep(cells):
    joined = "".join(cells)
    return bool(joined) and set(joined) <= set("-: ")

def header_cols(cells):
    vals = [norm(c) for c in cells if c.strip()]
    uniq = []
    for v in vals:
        if v and (not uniq or uniq[-1] != v):
            uniq.append(v)
    for key, cols in SEG_SETS.items():
        if tuple(u for u in uniq if u in key) == key and len(set(uniq) & set(key)) == len(key):
            return cols
    return None

def pipe_blocks(lines):
    i, n = 0, len(lines)
    while i < n:
        if lines[i].lstrip().startswith("|"):
            j = i
            while j < n and lines[j].lstrip().startswith("|"):
                j += 1
            yield i, lines[i:j]
            i = j
        else:
            i += 1

def prose_period(lines, upto):
    for k in range(upto - 1, max(-1, upto - 15), -1):
        m = PERIOD_RE.search(lines[k])
        if m:
            return ("PE", DUR[m.group(1).lower()], MON_NUM[m.group(2).capitalize()],
                    int(m.group(3)), int(m.group(4)))
        mm = re.search(r"In the (first|second|third|fourth) quarter of (\d{4}), "
                       r"the Company's revenue by primary geograph", lines[k], re.I)
        if mm:
            return ("QTXT", mm.group(1).lower(), int(mm.group(2)))
    return None


def parse_file(path):
    raw = [clean(l.rstrip("\n")) for l in open(path, encoding="utf-8")]
    fname = os.path.basename(path)
    tables = []

    for start, blk in pipe_blocks(raw):
        rows = [split_cells(l) for l in blk]
        if not any(SEC_PL.match(c.strip()) for r in rows for c in r):
            continue

        cols = None; period = None; section = None
        anchor_len = None; col_idx = None; pending_label = ""; prev_joined = ""
        cur = None
        default_period = prose_period(raw, start)

        def flush():
            nonlocal cur
            if cur and cur["recs"]:
                tables.append(cur)
            cur = None

        def open_table():
            nonlocal cur, section, anchor_len, col_idx, pending_label
            flush()
            pending_label = ""
            section = None; anchor_len = None; col_idx = None
            cur = {"file": fname, "line": start, "cols": list(cols),
                   "period": period, "recs": []}

        prev_list = [""] + [" ".join(c for c in rr if c.strip()) for rr in rows[:-1]]
        for ri, r in enumerate(rows):
            prev_joined = prev_list[ri]
            if is_sep(r):
                continue
            hc = header_cols(r)
            if hc:
                cols = hc
                mh = PERIOD_RE.search(" ".join(r))
                if mh:
                    period = ("PE", DUR[mh.group(1).lower()],
                              MON_NUM[mh.group(2).capitalize()],
                              int(mh.group(3)), int(mh.group(4)))
                else:
                    wp = wrapped_period(prev_joined, " ".join(c for c in r if c.strip()))
                    if wp:
                        period = wp
                        mh = True
                if cur is None or cur["recs"] or mh:
                    period = period or default_period
                    open_table()
                else:
                    cur["cols"] = list(cols)
                continue
            joined = " ".join(c for c in r if c.strip())
            m = PERIOD_RE.search(joined)
            wp = None if m else wrapped_period(prev_joined, joined)
            if m or wp:
                period = wp or ("PE", DUR[m.group(1).lower()], MON_NUM[m.group(2).capitalize()],
                                int(m.group(3)), int(m.group(4)))
                if cols:
                    open_table()
                continue
            # bare fiscal-year row inside a 10-K annual table
            nz = [c for c in r if c.strip()]
            if len(nz) == 1 and re.fullmatch(r"20\d\d", nz[0]):
                period = ("FY", int(nz[0]))
                if cols:
                    open_table()
                continue
            if cols is None:
                continue
            if cur is None:
                period = period or default_period
                open_table()

            label = ""
            for c in r:
                if c.strip() and to_num(c) is None and c.strip() != "$":
                    label = c.strip(); break
            ls = label.strip()
            if SEC_GEO.match(ls):  section = "geo"; continue
            if SEC_PL.match(ls):   section = "pl";  continue
            if SEC_TIM.match(ls):  section = "timing"; continue
            if section is None:
                continue

            nums_all = [(i, to_num(c)) for i, c in enumerate(r) if to_num(c) is not None]
            if not nums_all:
                if ls:
                    pending_label = (pending_label + " " + ls).strip()
                continue
            if pending_label:
                label = (pending_label + " " + label).strip()
                pending_label = ""
            ncol = len(cols)
            if col_idx is None and len(nums_all) == ncol:
                anchor_len, col_idx = len(r), [i for i, _ in nums_all]

            vals, ok = None, True
            if col_idx is not None and len(r) == anchor_len:
                cand = {}
                for ci, cn in zip(col_idx, cols):
                    v = to_num(r[ci]) if ci < len(r) else None
                    if v is not None:
                        cand[cn] = v
                stray = [i for i, _ in nums_all if i not in col_idx]
                if not stray:
                    vals = cand
            if vals is None:
                if len(nums_all) == ncol:
                    vals = dict(zip(cols, [v for _, v in nums_all]))
                else:
                    ok = False
            cur["recs"].append({"label": label, "section": section,
                                "vals": vals, "ok": ok,
                                "raw": [v for _, v in nums_all]})
        flush()
    return tables


# ---------------------------------------------------------------- validation
def canon_rows(tbl):
    """Return dict section -> {canon_label: vals} plus the section Total rows."""
    out = {"geo": {}, "pl": {}, "timing": {}}
    tot = {}
    bad = []
    for rec in tbl["recs"]:
        s = rec["section"]
        n = norm(rec["label"])
        if n == "total":
            if rec["ok"] and rec["vals"]:
                tot[s] = rec["vals"]
            continue
        if not rec["ok"] or not rec["vals"]:
            bad.append((s, rec["label"], rec["raw"]))
            continue
        if s == "pl":
            c = PL_CANON.get(n)
            if not c:
                bad.append((s, rec["label"], rec["raw"])); continue
            out["pl"][c[0]] = rec["vals"]
        elif s == "geo":
            c = GEO_CANON.get(n)
            if not c:
                bad.append((s, rec["label"], rec["raw"])); continue
            out["geo"][c] = rec["vals"]
        else:
            c = TIM_CANON.get(n)
            if not c:
                bad.append((s, rec["label"], rec["raw"])); continue
            out["timing"][c] = rec["vals"]
    return out, tot, bad


def validate(tbl):
    rowsets, tot, bad = canon_rows(tbl)
    errs = ["unparsed row %s/%s %s" % b for b in bad]
    cols = tbl["cols"]
    for sec in ("geo", "pl", "timing"):
        rs = rowsets[sec]
        if not rs:
            errs.append(f"{sec}: no rows"); continue
        if sec not in tot:
            errs.append(f"{sec}: no Total row"); continue
        for c in cols:
            got = sum(v.get(c, 0) for v in rs.values())
            want = tot[sec].get(c)
            if want is None:
                errs.append(f"{sec}: Total row missing column {c}")
            elif got != want:
                errs.append(f"{sec}: column {c} sums to {got}, Total row says {want}")
        # row cross-foot
        for lbl, v in rs.items():
            rowsum = sum(v.get(c, 0) for c in cols if c != "Total")
            if "Total" in v and rowsum != v["Total"]:
                errs.append(f"{sec}: row {lbl} crossfoots to {rowsum}, states {v['Total']}")
    return rowsets, tot, errs


def main():
    all_t = []
    for f in sorted(glob.glob(CORPUS + "/*.md")):
        all_t.extend(parse_file(f))
    print("candidate tables:", len(all_t))
    good, bad = [], []
    for t in all_t:
        rowsets, tot, errs = validate(t)
        t["_rows"], t["_tot"], t["_errs"] = rowsets, tot, errs
        (good if not errs else bad).append(t)
    print("clean:", len(good), " flagged:", len(bad))
    print("\n--- periods (clean) ---")
    seen = defaultdict(list)
    for t in good:
        seen[tuple(t["period"]) if t["period"] else None].append(t["file"])
    for k in sorted(seen, key=str):
        print(" ", k, len(seen[k]), seen[k][0])
    print("\n--- flagged ---")
    for t in bad:
        print(" ", t["file"], t["line"], t["period"], "|", "; ".join(t["_errs"][:3]))
    json.dump({"good": [{k: v for k, v in t.items() if not k.startswith("_")} | {"rows": t["_rows"], "tot": t["_tot"]} for t in good]},
              open(SCRATCH + "/de_pl_good.json", "w"), indent=1)


if __name__ == "__main__":
    main()
