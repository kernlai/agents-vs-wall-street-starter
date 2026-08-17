#!/usr/bin/env python3
"""
Build data/deere/de_geo_segment_matrix.csv from the parsed ASC 606
revenue-recognition footnote blocks.

- keeps only blocks that reconcile (rows -> row total, columns -> column total)
- cross-validates every cell across all filings that disclose it
- derives Q4 as (fiscal year - nine months) and documents the derivation
- emits a per-quarter reconciliation report to stdout
"""

import csv
import os
import sys
from collections import OrderedDict, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import de_parse_revrec_matrix as M  # noqa: E402

OUT_CSV = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_geo_segment_matrix.csv"

SEG_OF_SCHEME = {"old": M.SEG_OLD, "new": M.SEG_NEW}
SPAN_Q = {"Three": None, "Six": "H1", "Nine": "9M", "Twelve": "FY"}
# three-month period end -> fiscal quarter
QEND = {}


def collect():
    blocks = []
    for f in sorted(os.listdir(M.FILINGS)):
        if not f.endswith(".md"):
            continue
        p = os.path.join(M.FILINGS, f)
        if "Central Europe" not in open(p, encoding="utf-8").read():
            continue
        for b in M.parse_file(p):
            b["src"] = f
            b["pubdate"] = f[:10]
            b["problems"] = (M.validate_geo(b) if b["kind"] == "geo"
                             else M.validate_pl(b))
            if b["problems"] and b["kind"] == "pl" and M.repair_pl(b):
                b["problems"] = M.validate_pl(b)
                if b["problems"]:
                    b.pop("repaired", None)
            blocks.append(b)
    return blocks


def resolve_unknown_spans(blocks):
    """Some headers lose the span word ("Months Ended July 31, 2022").

    Resolve by matching the block's fingerprint against blocks of the same
    date whose span IS known. Unresolvable blocks are dropped.
    """
    def fp(b):
        if b["kind"] == "geo":
            return tuple(tuple(v) for v in b["rows"].values())
        return tuple(tuple(v) for _, v in b["rows"].values())

    known = defaultdict(dict)
    for b in blocks:
        p = b["period"]
        if p["span"] != "Unknown" and not b["problems"]:
            known[(b["kind"], b["scheme"], p["period_end"])][fp(b)] = p["span"]
    dropped = []
    for b in blocks:
        p = b["period"]
        if p["span"] != "Unknown":
            continue
        span = known.get((b["kind"], b["scheme"], p["period_end"]), {}).get(fp(b))
        if span:
            p["span"] = span
            p["cum_q"] = M.MONTHS_TO_Q[span]
            b["span_resolved"] = True
        else:
            b["problems"] = (b["problems"] or []) + [
                "header lost its span word and could not be matched to a "
                "known three/six/nine/twelve-month block"]
            dropped.append(b)
    return dropped


def infer_quarters(blocks):
    """Map each three-month period_end to its fiscal quarter."""
    ends = defaultdict(set)
    for b in blocks:
        p = b["period"]
        if p["period_end"]:
            ends[p["fy"]].add((p["period_end"], p["span"]))
    for fy, s in ends.items():
        threes = sorted(d for d, sp in s if sp == "Three")
        # cumulative spans tell us the ordinal directly
        for d, sp in s:
            if sp == "Six":
                QEND[d] = (fy, 2)
            elif sp == "Nine":
                QEND[d] = (fy, 3)
        for d in threes:
            if d in QEND:
                continue
            QEND[d] = (fy, None)
    # resolve remaining three-month ends by ordering within the fiscal year
    for fy in ends:
        threes = sorted(d for d, sp in ends[fy] if sp == "Three")
        for i, d in enumerate(threes):
            known = QEND.get(d)
            if known and known[1]:
                continue
            QEND[d] = (fy, i + 1)
    # FY2019 Q1 (no dated header in the Q1 FY2019 10-Q) is pinned by the
    # Q1 FY2020 10-Q comparative "Three Months Ended January 27, 2019"
    return QEND


def main():
    blocks = collect()
    unresolved = resolve_unknown_spans(blocks)
    infer_quarters(blocks)

    # The Q1 FY2019 10-Q labels its table only in prose ("In the first quarter
    # of 2019..."), with no period-end date. Pin the date from the dated
    # three-month columns of the same quarter elsewhere in the corpus.
    qdate = {}
    for pe, (fy, q) in QEND.items():
        if q:
            qdate[(fy, q)] = pe
    for b in blocks:
        p = b["period"]
        if p["period_end"] is None and p.get("explicit_q"):
            p["period_end"] = qdate.get((p["fy"], p["explicit_q"]))

    bad = [b for b in blocks if b["problems"]]
    good = [b for b in blocks if not b["problems"]]

    # ---- cross-source cell store -------------------------------------------
    # geo cells: (scheme, span, period_end, fy, segment, geography) -> {value: [srcs]}
    cells = defaultdict(lambda: defaultdict(list))
    for b in good:
        p, sch = b["period"], b["scheme"]
        segs = SEG_OF_SCHEME[sch]
        pe = p["period_end"]
        if pe is None:
            continue  # undated prose block; the same figures are dated elsewhere
        key0 = (sch, p["span"], pe, p["fy"])
        if b["kind"] == "geo":
            for g, v in b["rows"].items():
                for i, s in enumerate(segs):
                    cells[key0 + (s, g, "")][v[i]].append(b["src"])
                cells[key0 + ("Total", g, "")][v[len(segs)]].append(b["src"])
            t = b["totals"]
            for i, s in enumerate(segs):
                cells[key0 + (s, "Total", "")][t[i]].append(b["src"])
            cells[key0 + ("Total", "Total", "")][t[len(segs)]].append(b["src"])
        else:
            rep = set(b.get("repaired") or [])
            for name, (spans, v) in b["rows"].items():
                tag = b["src"] + ("|reconstructed" if name in rep else "")
                for i, s in enumerate(spans):
                    cells[key0 + (s, "", name)][v[i]].append(tag)
                cells[key0 + ("Total", "", name)][v[-1]].append(tag)

    conflicts = [(k, dict(vv)) for k, vv in cells.items() if len(vv) > 1]

    # ---- derive quarters that are only disclosed cumulatively --------------
    # Q2 = six - three, Q3 = nine - six, Q4 = twelve - nine.  Only used where
    # the three-month column itself is absent from every filing.
    derived = {}
    by_span = defaultdict(dict)
    three_by_q = defaultdict(dict)   # (scheme, fy, quarter) -> disclosed cells
    for k, vv in cells.items():
        sch, span, pe, fy, seg, geo, pl = k
        val = sorted(vv, key=lambda v: -len(vv[v]))[0]
        by_span[(sch, span, fy)][(seg, geo, pl)] = (val, pe)
        if span == "Three":
            three_by_q[(sch, fy, QEND[pe][1])][(seg, geo, pl)] = val

    LADDER = [(2, "Six", "Three"), (3, "Nine", "Six"), (4, "Twelve", "Nine")]
    for (sch, span, fy) in sorted(by_span):
        for q, big, small in LADDER:
            if span != big:
                continue
            if three_by_q.get((sch, fy, q)):
                continue  # the quarter is disclosed directly, no need to derive
            top = by_span.get((sch, big, fy))
            base = by_span.get((sch, small, fy))
            if not top or not base:
                continue
            out = {kk: val - base[kk][0] for kk, (val, pe) in top.items()
                   if kk in base}
            if out:
                derived[(sch, fy, q)] = (
                    out, top[list(top)[0]][1], base[list(base)[0]][1], big, small)

    # ---- write csv ----------------------------------------------------------
    rows = []
    src_of = {}
    for k, vv in cells.items():
        sch, span, pe, fy, seg, geo, pl = k
        val = sorted(vv, key=lambda v: -len(vv[v]))[0]
        tags = sorted(set(vv[val]))
        srcs = sorted({t.split("|")[0] for t in tags})
        reconstructed = all("|reconstructed" in t for t in tags)
        src_of[k] = srcs
        if span == "Three":
            fq = "Q%d" % QEND[pe][1]
            note = ""
        else:
            fq = SPAN_Q[span]
            note = "cumulative %s-month column as disclosed; not a quarter" % {
                "Six": "six", "Nine": "nine", "Twelve": "twelve"}[span]
        if sch == "old":
            note = (note + "; " if note else "") + \
                "pre-FY2021 reportable segments (Agriculture & Turf / Construction & Forestry)"
        if geo == "Total" or seg == "Total":
            note = (note + "; " if note else "") + "disclosed total, do not re-sum with cells"
        if reconstructed:
            note = (note + "; " if note else "") + (
                "cell reconstructed from the column residual: the source table "
                "cell was merged by the pdf-to-markdown conversion")
        if len(srcs) > 1:
            note = (note + "; " if note else "") + "confirmed in %d filings" % len(srcs)
        rows.append(dict(
            series_id="de_revrec_net_sales", period_end=pe, fiscal_year=fy,
            fiscal_quarter=fq, segment=seg, geography=geo, product_line=pl,
            value=val, units="USDm", basis="rev-rec",
            source="filings/" + srcs[0], notes=note))

    SPANWORD = {"Six": "six-month", "Nine": "nine-month", "Twelve": "fiscal-year"}
    for (sch, fy, q), (out, top_pe, base_pe, big, small) in sorted(derived.items()):
        for (seg, geo, pl), val in out.items():
            rows.append(dict(
                series_id="de_revrec_net_sales", period_end=top_pe, fiscal_year=fy,
                fiscal_quarter="Q%d" % q, segment=seg, geography=geo,
                product_line=pl, value=val, units="USDm", basis="rev-rec",
                source="derived",
                notes=("derived: %s column ended %s minus %s column ended %s "
                       "(the three-month column is not disclosed for this quarter)"
                       % (SPANWORD[big], top_pe, SPANWORD[small], base_pe)) +
                      ("; pre-FY2021 reportable segments" if sch == "old" else "") +
                      ("; disclosed total, do not re-sum with cells"
                       if (geo == "Total" or seg == "Total") else "")))

    def sortkey(r):
        return (r["fiscal_year"], {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4,
                                   "H1": 5, "9M": 6, "FY": 7}[r["fiscal_quarter"]],
                0 if r["product_line"] == "" else 1,
                M.GEO_ORDER.index(r["geography"]) if r["geography"] in M.GEO_ORDER
                else 99,
                r["product_line"], r["segment"])

    rows.sort(key=sortkey)
    hdr = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "segment",
           "geography", "product_line", "value", "units", "basis", "source", "notes"]
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=hdr)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ---- reconciliation report ---------------------------------------------
    print("== parsed blocks: %d  clean: %d  rejected: %d" %
          (len(blocks), len(good), len(bad)))
    print("== cross-source conflicts: %d" % len(conflicts))
    for k, vv in conflicts:
        print("   CONFLICT", k, vv)

    print("\n== per-period reconciliation (geographic matrix) ==")
    seen = OrderedDict()
    for b in blocks:
        if b["kind"] != "geo":
            continue
        p = b["period"]
        k = (b["scheme"], p["fy"], p["span"], p["period_end"])
        seen.setdefault(k, []).append(b)
    for k in sorted(seen, key=lambda x: (x[1], str(x[3]), x[2], x[0])):
        bs = seen[k]
        ok = [b for b in bs if not b["problems"]]
        print("  %-4s FY%d %-7s %-11s  sources=%d  reconciled=%d  %s" %
              (k[0], k[1], k[2], k[3] or "n/a", len(bs), len(ok),
               "PASS" if ok else "FAIL"))

    print("\n== quarters derived from cumulative columns ==")
    for (sch, fy, q) in sorted(derived):
        _, _, _, big, small = derived[(sch, fy, q)]
        print("  %-4s FY%d Q%d = %s column - %s column" % (sch, fy, q, big, small))

    print("\n== rejected blocks (not used) ==")
    for b in bad:
        p = b["period"]
        print("  %s/%s FY%s %s %s  %s line %d :: %s" %
              (b["kind"], b["scheme"], p["fy"], p["span"], p["period_end"],
               b["src"], b["line"], b["problems"][0]))

    print("\nwrote %d rows -> %s" % (len(rows), OUT_CSV))


if __name__ == "__main__":
    main()
