#!/usr/bin/env python3
"""Cross-validate the Deere guidance dataset against independent sources.

Three families of check:
  A. guidance value in the 8-K earnings release vs the same value in the 10-Q/10-K
  B. guidance value in the 8-K vs the prepared-remarks transcript / slide deck
  C. actuals from the SEC XBRL API vs the same actuals in the corpus filings
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import de_guidance_extract as X       # noqa: E402
import de_build_guidance as B         # noqa: E402

ok = bad = 0


def chk(name, a, b, tol):
    global ok, bad
    if a is None or b is None:
        print("  SKIP %-52s (missing)" % name)
        return
    good = abs(a - b) <= tol
    globals().__setitem__("ok", ok + 1) if good else globals().__setitem__("bad", bad + 1)
    print("  %-5s %-52s %s vs %s" % ("AGREE" if good else "DIFFER", name, a, b))


def main():
    print("A. guidance: 8-K earnings release vs 10-Q / 10-K")
    for issue, fq, fy, primary, _ in X.EVENTS:
        docs = X.docs_for(issue)
        if not docs:
            continue
        a = X.extract_net_income(X.flat(primary))
        b = X.extract_net_income(" ".join(X.flat(f) for f in docs))
        if a and b:
            chk("FY%d %s net income low" % (fy, fq), a[0], b[0], 60)
            chk("FY%d %s net income high" % (fy, fq), a[1], b[1], 60)

    print("\nB. guidance: 8-K vs prepared-remarks transcript (legacy segment sales)")
    for issue, fq, fy, primary, _ in X.EVENTS:
        if issue > B.LEGACY_LAST_EVENT:
            continue
        tr = X.transcript_for(issue)
        if not tr:
            continue
        tf = X.flat(tr)
        pf = X.flat(primary)
        for seg in ("ag_turf", "cf"):
            a = X.extract_legacy_growth(pf, seg)
            b = X.extract_transcript_seg_sales(tf, seg)
            if a and b:
                chk("FY%d %s %s growth low" % (fy, fq, seg), a[0], b[0], 1.01)
                chk("FY%d %s %s growth high" % (fy, fq, seg), a[1], b[1], 1.01)

    print("\nC. actuals: SEC XBRL vs corpus filings")
    ni = {k: v / 1e6 for k, v in B.annual_actuals("NetIncomeLoss", "USD").items()}
    rev = {k: v / 1e6 for k, v in B.annual_actuals("Revenues", "USD").items()}
    eps = B.annual_actuals("EarningsPerShareDiluted", "USD/shares")
    corpus_rev, corpus_ni, corpus_eps = {}, {}, {}
    d = os.path.join(X.CORPUS, "filings")
    for fn in sorted(os.listdir(d)):
        if not re.search(r"(q4-8k|fy-8k)", fn):
            continue
        cand = [y for y, e in X.FY_END.items() if e <= fn[:10]]
        if not cand:
            continue
        fy0 = max(cand)
        txt = open(os.path.join(d, fn), encoding="utf-8", errors="replace").read().replace("&amp;", "&")
        for line in txt.split("\n"):
            l = line.strip()
            if not l.startswith("|"):
                continue
            v = B._nums(l)
            if re.search(r"Total net sales and revenues", l, re.I) and len(v) >= 5:
                corpus_rev.setdefault(fy0, v[3])
            # the headline summary table is the only one with exactly
            # [Q, Q, %chg, FY, FY, %chg]; the supplemental consolidating
            # statements and the JDCC statements have different shapes
            if re.match(r"\|\s*Net [Ii]ncome", l) and len(v) == 6:
                corpus_ni.setdefault(fy0, v[3])
    for fy in sorted(set(corpus_rev) & set(rev)):
        chk("FY%d net sales & revenues" % fy, rev[fy], corpus_rev[fy], 2.0)
    for fy in sorted(set(corpus_ni) & set(ni)):
        chk("FY%d net income" % fy, ni[fy], corpus_ni[fy], 2.0)

    print("\nD. segment FY net sales: 10-K three-year table vs Q4 8-K full-year column")
    seg = B.segment_fy_actuals()
    chk("C&F FY2019 legacy vs modern label", seg["cf_legacy"].get(2019), seg["cf"].get(2019), 1.0)
    chk("C&F FY2020 legacy vs modern label", seg["cf_legacy"].get(2020), seg["cf"].get(2020), 1.0)

    print("\nTOTAL agree=%d differ=%d" % (ok, bad))


if __name__ == "__main__":
    main()
