#!/usr/bin/env python3
"""
Stage 2: quantitative adjudication of the lead-time / order-book hypothesis.

The hypothesis says Q3 REVENUE is largely pre-determined at the Q2 call while
MARGIN is not. The falsifiable implication tested here:

  (a) Q3 revenue expressed relative to information already in hand at the Q2 call
      (i.e. Q3 / Q2 and Q3 / H1 ratios) should be TIGHT across years.
  (b) Q3 margin (PPA operating margin, enterprise EPS conversion) should be
      MUCH LOOSER on any comparable normalised basis.

Data source: the 8-K earnings releases in the offline corpus (headline table +
segment tables). No guesses; a missing quarter is simply absent.
"""
import os, re, json, statistics as st

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
FDIR = os.path.join(CORPUS, "filings")

NUM = r"\$?\s*\(?\s*([\d,]+(?:\.\d+)?)\s*\)?"

QMAP = {"q1":1,"q2":2,"q3":3,"q4":4,"fy":4}

def money(s):
    s = s.replace(",", "").replace("$","").strip()
    try: return float(s)
    except: return None

def parse_file(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    out = {}
    # headline table row: | Net sales and revenues | $12,018 | $13,152 | -9% | ...
    m = re.search(r"\|\s*Net sales and revenues\s*\|\s*\$?\s*([\d,]+)\s*\|\s*\$?\s*([\d,]+)\s*\|", txt)
    if m:
        out["nsr_cur"] = money(m.group(1)); out["nsr_py"] = money(m.group(2))
    m = re.search(r"\|\s*Fully diluted EPS\s*\|\s*\$?\s*([\d.,]+)\s*\|\s*\$?\s*([\d.,]+)\s*\|", txt)
    if m:
        out["eps_cur"] = money(m.group(1)); out["eps_py"] = money(m.group(2))
    # segment blocks
    for seg, key in [("Production & Precision Ag", "ppa"),
                     ("Small Ag & Turf", "sat"),
                     ("Construction & Forestry", "cf")]:
        # find the table header line for this segment then the following ~8 lines
        pat = re.escape(seg) + r"(?:riculture|)\s*\|[^\n]*\n(?:[^\n]*\n){0,8}"
        for mm in re.finditer(pat, txt):
            blk = mm.group(0)
            if "Net sales" not in blk:
                continue
            s = re.search(r"\|\s*Net sales\s*\|\s*\$?\s*([\d,]+)\s*\|\s*\$?\s*([\d,]+)\s*\|", blk)
            p = re.search(r"\|\s*Operating profit\s*\|\s*\$?\s*\(?([\d,]+)\)?\s*\|\s*\$?\s*\(?([\d,]+)\)?\s*\|", blk)
            if s:
                out[key+"_sales_cur"] = money(s.group(1)); out[key+"_sales_py"] = money(s.group(2))
            if p:
                out[key+"_op_cur"] = money(p.group(1)); out[key+"_op_py"] = money(p.group(2))
            break
    return out

def main():
    rows = {}
    for fn in sorted(os.listdir(FDIR)):
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})__de-us-\d+-(q[1-4]|fy)-8k", fn)
        if not m:
            continue
        y, mo, d, qs = m.group(1), m.group(2), m.group(3), m.group(4)
        q = QMAP[qs]
        fy = int(y)
        rec = parse_file(os.path.join(FDIR, fn))
        if not rec:
            continue
        rec["_file"] = fn
        rows[(fy, q)] = rec

    print(f"8-K earnings releases parsed: {len(rows)}")
    keys = sorted(rows)
    print("\nfy q  NSR      EPS    PPAsales PPAop  file")
    for k in keys:
        r = rows[k]
        print(f"{k[0]} {k[1]}  {r.get('nsr_cur','-'):>8} {r.get('eps_cur','-'):>6} "
              f"{r.get('ppa_sales_cur','-'):>8} {r.get('ppa_op_cur','-'):>6}  {r['_file'][:34]}")

    # ---- test (a): Q3 revenue relative to Q2 revenue, same FY
    print("\n=== TEST A: Q3 total NSR / Q2 total NSR (revenue seasonality stability) ===")
    ratios = []
    for fy in range(2012, 2027):
        q2 = rows.get((fy,2),{}).get("nsr_cur")
        q3 = rows.get((fy,3),{}).get("nsr_cur")
        # a Q3 filing also carries the prior-year Q3; use direct where possible
        if q2 and q3:
            ratios.append((fy, q3/q2))
    for fy, r in ratios:
        print(f"  FY{fy}: Q3/Q2 = {r:.4f}")
    vals = [r for _, r in ratios]
    if len(vals) > 2:
        print(f"  n={len(vals)} mean={st.mean(vals):.4f} sd={st.pstdev(vals):.4f} "
              f"CV={st.pstdev(vals)/st.mean(vals)*100:.2f}%")

    print("\n=== TEST A2: PPA Q3 sales / PPA Q2 sales ===")
    pr = []
    for fy in range(2012, 2027):
        a = rows.get((fy,2),{}).get("ppa_sales_cur"); b = rows.get((fy,3),{}).get("ppa_sales_cur")
        if a and b: pr.append((fy, b/a))
    for fy, r in pr: print(f"  FY{fy}: {r:.4f}")
    v = [r for _, r in pr]
    if len(v) > 2:
        print(f"  n={len(v)} mean={st.mean(v):.4f} sd={st.pstdev(v):.4f} CV={st.pstdev(v)/st.mean(v)*100:.2f}%")

    # ---- test (b): PPA Q3 operating margin, and Q3 margin minus Q2 margin
    print("\n=== TEST B: PPA operating margin, Q2 vs Q3 same FY (margin stability) ===")
    deltas = []
    for fy in range(2012, 2027):
        s2 = rows.get((fy,2),{}).get("ppa_sales_cur"); o2 = rows.get((fy,2),{}).get("ppa_op_cur")
        s3 = rows.get((fy,3),{}).get("ppa_sales_cur"); o3 = rows.get((fy,3),{}).get("ppa_op_cur")
        if s2 and o2 and s3 and o3:
            m2, m3 = o2/s2*100, o3/s3*100
            deltas.append((fy, m2, m3, m3-m2))
    for fy, m2, m3, dm in deltas:
        print(f"  FY{fy}: Q2 margin {m2:5.2f}%  Q3 margin {m3:5.2f}%  delta {dm:+6.2f}pp")
    dv = [d for *_ , d in deltas]
    if len(dv) > 2:
        print(f"  n={len(dv)} mean delta={st.mean(dv):+.2f}pp sd={st.pstdev(dv):.2f}pp")

    # ---- combined: how much of Q3 OP variance comes from sales vs margin
    print("\n=== TEST C: decomposition of Q3 PPA operating-profit error if you knew Q2 ===")
    print("  Naive model: Q3 sales = Q2 sales * mean(Q3/Q2); Q3 margin = Q2 margin + mean(delta)")
    if len(dv) > 2 and len(v) > 2:
        mr, mdm = st.mean(v), st.mean(dv)
        errs_s, errs_m, errs_op = [], [], []
        for fy, m2, m3, dm in deltas:
            s2 = rows[(fy,2)]["ppa_sales_cur"]; s3 = rows[(fy,3)]["ppa_sales_cur"]
            o3 = rows[(fy,3)]["ppa_op_cur"]
            s3h = s2*mr
            m3h = m2 + mdm
            o3h = s3h*m3h/100
            errs_s.append((s3h-s3)/s3*100)
            errs_m.append(m3h-m3)
            errs_op.append((o3h-o3)/o3*100)
        print(f"  n={len(errs_s)}")
        print(f"  Q3 PPA SALES  pct error: mean {st.mean(errs_s):+.1f}%  sd {st.pstdev(errs_s):.1f}%  "
              f"MAPE {st.mean([abs(e) for e in errs_s]):.1f}%")
        print(f"  Q3 PPA MARGIN pp  error: mean {st.mean(errs_m):+.2f}pp sd {st.pstdev(errs_m):.2f}pp "
              f"MAE {st.mean([abs(e) for e in errs_m]):.2f}pp")
        print(f"  Q3 PPA OP     pct error: mean {st.mean(errs_op):+.1f}%  sd {st.pstdev(errs_op):.1f}%  "
              f"MAPE {st.mean([abs(e) for e in errs_op]):.1f}%")

    json.dump({f"{k[0]}Q{k[1]}": v for k, v in rows.items()},
              open("/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/de_8k_quarters.json","w"), indent=1)

if __name__ == "__main__":
    main()
