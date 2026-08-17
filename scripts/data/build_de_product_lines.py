#!/usr/bin/env python3
"""
Build the tidy-long product-line / timing-of-revenue CSV for Deere & Company
from the parsed ASC-606 revenue-recognition tables.

Depends on parse_de_product_lines.py (same directory) for the parsing itself.
Standard library only.
"""
import sys, os, csv, json, datetime as dt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parse_de_product_lines as P

OUT_CSV = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_product_lines.csv"

FY_END = {2019: "2019-11-03", 2020: "2020-11-01", 2021: "2021-10-31", 2022: "2022-10-30",
          2023: "2023-10-29", 2024: "2024-10-27", 2025: "2025-11-02"}
# fiscal quarter ends, from the filings themselves
QEND = {}

TAX_OLD = ("Agriculture and Turf", "Construction and Forestry", "Financial Services", "Total")
TAX_NEW = ("PPA", "SAT", "CF", "FS", "Total")
TAX_LABEL = {TAX_OLD: "AT/CF (pre-2021 segment structure)",
             TAX_NEW: "PPA/SAT/CF (2021 Smart Industrial structure)"}

def norm_period(per):
    """-> (kind, period_end ISO, duration_months)"""
    if per is None:
        return None
    if per[0] == "PE":
        _, dur, m, d, y = per
        return ("PE", f"{y:04d}-{m:02d}-{d:02d}", dur)
    if per[0] == "FY":
        y = per[1]
        if y not in FY_END:
            return None
        return ("FY", FY_END[y], 12)
    if per[0] == "QTXT":
        # only occurrence: "In the first quarter of 2019" -> 3 months ended 2019-01-27
        if per[1] == "first" and per[2] == 2019:
            return ("PE", "2019-01-27", 3)
    return None


def fy_of(period_end, dur=None):
    """Deere fiscal year of a period ending on period_end.

    Deere's fiscal year ends on the last Sunday of October or the first days of
    November, so the calendar year of the period end IS the fiscal year for
    every quarter and for the full year alike."""
    return int(period_end[:4])


def main():
    tables = []
    import glob
    for f in sorted(glob.glob(P.CORPUS + "/*.md")):
        tables.extend(P.parse_file(f))

    clean, flagged = [], []
    for t in tables:
        rows, tot, errs = P.validate(t)
        t["_rows"], t["_tot"], t["_errs"] = rows, tot, errs
        (clean if not errs else flagged).append(t)

    # ---- collect: key = (taxonomy, period_end, duration) -> section -> label -> vals
    store = {}
    conflicts = []
    provenance = defaultdict(set)
    for t in clean:
        np_ = norm_period(t["period"])
        if np_ is None:
            conflicts.append(f"{t['file']}:{t['line']} unresolved period {t['period']}")
            continue
        _, pe, dur = np_
        tax = tuple(t["cols"])
        key = (tax, pe, dur)
        provenance[key].add(t["file"])
        cur = store.setdefault(key, {"pl": {}, "timing": {}, "geo": {}})
        for sec in ("pl", "timing", "geo"):
            for lbl, vals in t["_rows"][sec].items():
                prev = cur[sec].get(lbl)
                if prev is not None and prev != vals:
                    conflicts.append(f"CONFLICT {key[1]} {dur}m {sec}/{lbl}: {prev} vs {vals} ({t['file']})")
                cur[sec][lbl] = vals

    print(f"parsed tables={len(tables)} clean={len(clean)} flagged={len(flagged)}")
    print(f"distinct (taxonomy, period_end, duration) keys = {len(store)}")
    for c in conflicts:
        print("  !", c)

    # ---- derive discrete quarters -------------------------------------------
    # index by taxonomy -> fiscal year -> duration -> key
    byfy = defaultdict(dict)
    for (tax, pe, dur) in store:
        byfy[(tax, fy_of(pe, dur))][dur] = (tax, pe, dur)

    derived = {}
    notes_derived = {}
    for (tax, fy), durs in sorted(byfy.items(), key=lambda x: (str(x[0][0]), x[0][1])):
        def sub(a, b, sec):
            """a - b elementwise over labels present in a."""
            out = {}
            A, B = store.get(a) or derived.get(a), store.get(b) or derived.get(b)
            if not A or not B:
                return None
            for lbl, av in A[sec].items():
                bv = B[sec].get(lbl)
                if bv is None:
                    return None
                out[lbl] = {c: av[c] - bv.get(c, 0) for c in av}
            return out
        # Q4 = FY - 9M
        if 12 in durs and 9 in durs:
            k12, k9 = durs[12], durs[9]
            res = {s: sub(k12, k9, s) for s in ("pl", "timing", "geo")}
            if res["pl"]:
                pe4 = k12[1]
                derived[(tax, pe4, "Q4")] = res
                notes_derived[(tax, pe4, "Q4")] = (
                    f"derived: 12 months ended {k12[1]} minus 9 months ended {k9[1]}")
        # Q3 discrete = 9M - 6M  (only if the 3M table is unavailable)
        if 9 in durs and 6 in durs and 3 not in [d for d in durs if store.get(durs[d]) and _is_q3(durs[d])]:
            pass
    # simpler: handle Q3/Q1 gaps explicitly below
    json.dump({}, open(os.devnull, "w"))

    # discrete 3-month tables available, keyed by (tax, period_end)
    three = {(tax, pe): (tax, pe, dur) for (tax, pe, dur) in store if dur == 3}
    six   = {(tax, fy_of(pe, 6)): (tax, pe, dur) for (tax, pe, dur) in store if dur == 6}
    nine  = {(tax, fy_of(pe, 9)): (tax, pe, dur) for (tax, pe, dur) in store if dur == 9}
    twelve= {(tax, fy_of(pe,12)): (tax, pe, dur) for (tax, pe, dur) in store if dur == 12}

    def diff(kA, kB, srcA, srcB):
        out = {}
        A = srcA.get(kA); B = srcB.get(kB)
        if not A or not B:
            return None
        for sec in ("pl", "timing", "geo"):
            o = {}
            for lbl, av in A[sec].items():
                bv = B[sec].get(lbl)
                if bv is None:
                    o = None; break
                o[lbl] = {c: av[c] - bv.get(c, 0) for c in av}
            out[sec] = o
        return out

    # Q1 gap: 6M - Q2(3M)  ;  Q3 gap: 9M - 6M ; Q4: 12M - 9M (or 12M-6M-Q3)
    quarters = {}   # (tax, fy, q) -> (period_end, sections, note, source)
    for (tax, pe, dur), sec in store.items():
        if dur != 3:
            continue
        fy = fy_of(pe, 3)
        m = int(pe[5:7])
        q = {1: "Q1", 2: "Q1", 4: "Q2", 5: "Q2", 7: "Q3", 8: "Q3", 10: "Q4", 11: "Q4"}.get(m)
        if q is None:
            print("  ! unmapped quarter month", pe); continue
        quarters[(tax, fy, q)] = (pe, sec, "", sorted(provenance[(tax, pe, dur)]))

    for (tax, fy), k6 in six.items():
        if (tax, fy, "Q1") in quarters:
            continue
        k3q2 = (tax, k6[1], 3)
        if k3q2 in store:
            d = diff(k6, k3q2, store, store)
            if d and d["pl"]:
                # Q1 period end unknown from this route -> take it from the Q1 10-Q filing text
                quarters[(tax, fy, "Q1")] = (None, d,
                    f"derived: 6 months ended {k6[1]} minus 3 months ended {k6[1]}", [])
    for (tax, fy), k9 in nine.items():
        if (tax, fy, "Q3") in quarters:
            continue
        k6 = six.get((tax, fy))
        if k6:
            d = diff(k9, k6, store, store)
            if d and d["pl"]:
                quarters[(tax, fy, "Q3")] = (k9[1], d,
                    f"derived: 9 months ended {k9[1]} minus 6 months ended {k6[1]}", [])
    for (tax, fy), k12 in twelve.items():
        if (tax, fy, "Q4") in quarters:
            continue
        k9 = nine.get((tax, fy))
        if k9:
            d = diff(k12, k9, store, store)
            if d and d["pl"]:
                quarters[(tax, fy, "Q4")] = (k12[1], d,
                    f"derived: 12 months ended {k12[1]} minus 9 months ended {k9[1]}", [])
        else:
            k6 = six.get((tax, fy)); q3 = quarters.get((tax, fy, "Q3"))
            if k6 and q3:
                nine_syn = {s: {l: {c: store[k6][s][l][c] + q3[1][s][l].get(c, 0) for c in store[k6][s][l]}
                                for l in store[k6][s] if l in q3[1][s]} for s in ("pl", "timing", "geo")}
                d = {}
                for s in ("pl", "timing", "geo"):
                    o = {}
                    for l, av in store[k12][s].items():
                        bv = nine_syn[s].get(l)
                        if bv is None: o = None; break
                        o[l] = {c: av[c] - bv.get(c, 0) for c in av}
                    d[s] = o
                if d["pl"]:
                    quarters[(tax, fy, "Q4")] = (k12[1], d,
                        f"derived: 12 months ended {k12[1]} minus (6 months ended {k6[1]} + Q3)", [])

    print("\ndiscrete quarters built:")
    for k in sorted(quarters, key=lambda x: (x[1], x[2], str(x[0][0]))):
        pe, sec, note, src = quarters[k]
        print("  ", TAX_LABEL[k[0]][:8], k[1], k[2], pe, ("DERIVED " + note) if note else "as-disclosed")

    # ---- validate every quarter (rows sum to total, columns cross-foot) -----
    val_report = []
    def check(tag, cols, sections):
        errs = []
        for sec in ("pl", "timing"):
            rs = sections[sec]
            if not rs:
                errs.append(f"{sec}: empty"); continue
            colsum = {c: sum(v.get(c, 0) for v in rs.values()) for c in cols}
            for lbl, v in rs.items():
                rowsum = sum(v.get(c, 0) for c in cols if c != "Total")
                if "Total" in v and rowsum != v["Total"]:
                    errs.append(f"{sec}:{lbl} crossfoot {rowsum} vs {v['Total']}")
            if colsum.get("Total") != sum(colsum[c] for c in cols if c != "Total"):
                errs.append(f"{sec}: grand total mismatch {colsum}")
        # pl total must equal timing total, column by column
        if sections["pl"] and sections["timing"]:
            a = {c: sum(v.get(c, 0) for v in sections["pl"].values()) for c in cols}
            b = {c: sum(v.get(c, 0) for v in sections["timing"].values()) for c in cols}
            if a != b:
                errs.append(f"pl vs timing totals differ: {a} / {b}")
        if errs:
            val_report.append((tag, errs))
        return not errs

    for k in sorted(quarters, key=lambda x: (x[1], x[2])):
        tax, fy, q = k
        pe, sec, note, src = quarters[k]
        check(f"{fy}{q} {TAX_LABEL[tax][:6]}", list(tax), sec)
    for key in sorted(store, key=lambda x: (x[1], x[2])):
        tax, pe, dur = key
        check(f"{pe} {dur}m {TAX_LABEL[tax][:6]}", list(tax), store[key])

    print("\nvalidation failures:", len(val_report))
    for tag, errs in val_report:
        print("  X", tag, "|", "; ".join(errs[:4]))

    # ---- quarter end dates for derived-Q1 rows -----------------------------
    # Q1 end = the 3M period end reported in that year's Q1 10-Q; recover from
    # the 6M/3M pair only if the corpus states it. Use known Deere quarter ends.
    Q1END = {}
    for (tax, pe, dur) in store:
        if dur == 3 and int(pe[5:7]) in (1, 2):
            Q1END[fy_of(pe, 3)] = pe
    # Deere states its quarter ends in the basis-of-presentation note; harvest them
    import re as _re
    _MN = {m: i + 1 for i, m in enumerate(
        "January February March April May June July August September October November December".split())}
    _pat = _re.compile(r"first quarter ends? for fiscal years? (\d{4}) and (\d{4}) were "
                       r"([A-Z][a-z]+) (\d{1,2}), (\d{4}),? and ([A-Z][a-z]+) (\d{1,2}), (\d{4})")
    for f in glob.glob(P.CORPUS + "/*.md"):
        for m in _pat.finditer(open(f, encoding="utf-8").read()):
            for fy, mon, day, yr in ((m.group(1), m.group(3), m.group(4), m.group(5)),
                                     (m.group(2), m.group(6), m.group(7), m.group(8))):
                Q1END.setdefault(int(fy), f"{int(yr):04d}-{_MN[mon]:02d}-{int(day):02d}")

    # ---- emit --------------------------------------------------------------
    rows = []
    def emit(series, pe, fy, fq, segment, product_line, value, basis, source, notes):
        rows.append(dict(series_id=series, period_end=pe, fiscal_year=fy, fiscal_quarter=fq,
                         segment=segment, geography="", product_line=product_line,
                         value=value, units="USDm", basis=basis, source=source, notes=notes))

    def dump(sections, cols, pe, fy, fq, note, src):
        source = "; ".join(src) if src else "derived"
        for sec, series in (("pl", "de_revrec_product_line"), ("timing", "de_revrec_timing")):
            for lbl in sorted(sections[sec]):
                v = sections[sec][lbl]
                for c in cols:
                    if c not in v:
                        continue
                    seg = "" if c == "Total" else c
                    n = note
                    if c == "Total":
                        n = (note + "; " if note else "") + "all segments"
                    emit(series, pe, fy, fq, seg, lbl, v[c], "rev-rec", source, n)

    for k in sorted(quarters, key=lambda x: (x[1], x[2], str(x[0]))):
        tax, fy, q = k
        pe, sec, note, src = quarters[k]
        if pe is None:
            pe = Q1END.get(fy, "")
            note = (note + "; period end from that year's Q1 10-Q") if pe else note
        tn = "taxonomy=" + TAX_LABEL[tax]
        dump(sec, list(tax), pe, fy, q, (note + "; " if note else "") + tn, src)

    # cumulative as-disclosed periods
    for key in sorted(store, key=lambda x: (x[1], x[2], str(x[0]))):
        tax, pe, dur = key
        if dur == 3:
            continue
        fy = fy_of(pe, dur)
        fq = {6: "H1", 9: "9M", 12: "FY"}[dur]
        tn = f"as disclosed, {dur} months ended {pe}; taxonomy=" + TAX_LABEL[tax]
        dump(store[key], list(tax), pe, fy, fq, tn, sorted(provenance[key]))

    # ---- contract-liability / RPO series (precision-ag subscription proxy) ---
    import extract_de_deferred_revenue as DR
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        DR.main()
    dd = json.load(open("/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/de_deferred.json"))
    QMAP = {}
    for k in list(quarters):
        pe = quarters[k][0] or Q1END.get(k[1], "")
        if pe:
            QMAP[pe] = (k[1], k[2])
    MQ = {1: "Q1", 2: "Q1", 4: "Q2", 5: "Q2", 7: "Q3", 8: "Q3", 10: "Q4", 11: "Q4"}
    def bs_q(d):
        return QMAP.get(d, (fy_of(d), MQ.get(int(d[5:7]), "")))
    for d, (v, src) in sorted(dd["deferred"].items()):
        fy, fq = bs_q(d)
        emit("de_revrec_deferred_revenue", d, fy, fq, "", "", v, "rev-rec", src,
             "contract liability: invoiced-but-unrecognised extended warranty, advance "
             "equipment payments and precision-guidance / telematics / information-enabled "
             "solutions subscription revenue; balance at period end")
    for d, (v, src) in sorted(dd["upo"].items()):
        fy, fq = bs_q(d)
        emit("de_revrec_rpo_gt1yr", d, fy, fq, "", "", v, "rev-rec", src,
             "remaining (unsatisfied) performance obligations on contracts with an original "
             "duration greater than one year; balance at period end")

    hdr = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "segment", "geography",
           "product_line", "value", "units", "basis", "source", "notes"]
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=hdr)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nwrote {len(rows)} rows -> {OUT_CSV}")


def _is_q3(k):
    return int(k[1][5:7]) in (7, 8)


if __name__ == "__main__":
    main()
