#!/usr/bin/env python3
"""Build the Deere guidance panel and the guidance-vs-actual comparison.

  data/deere/de_guidance.csv            tidy-long guidance panel
  data/deere/de_guidance_vs_actual.csv  vintage-vs-outturn errors

Guidance is extracted from the frozen offline corpus by de_guidance_extract.py.
Actuals come from the SEC XBRL company-concept API (CIK 315189) for the
consolidated figures and from the corpus 10-K / Q4 8-K segment tables for the
segment figures.

Run:  python3 de_build_guidance.py
"""
import csv
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import de_guidance_extract as X  # noqa: E402

OUTDIR = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere"
CACHE = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad/sec"
UA = "AgentsVsWallStreet cor@salomo.io"
HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "value",
          "units", "source_type", "source", "notes"]

# Fiscal years whose guidance was framed on the legacy Agriculture & Turf
# segment basis. The FY2021 reorganisation into PPA / SAT / CF first appears in
# reporting on 2021-02-19 (Q1 FY2021); the Q4 FY2020 release (2020-11-25) that
# issued the FIRST FY2021 guidance was still on the legacy A&T basis.
LEGACY_LAST_EVENT = "2020-11-25"


# ------------------------------------------------------------------ SEC actuals
def sec_concept(tag):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, tag + ".json")
    if not os.path.exists(path):
        url = ("https://data.sec.gov/api/xbrl/companyconcept/CIK0000315189/us-gaap/%s.json" % tag)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            open(path, "wb").write(r.read())
    return json.load(open(path))


def _rows(tag, unit):
    return sec_concept(tag)["units"][unit]


def _days(r):
    from datetime import date
    a = date.fromisoformat(r["start"])
    b = date.fromisoformat(r["end"])
    return (b - a).days


END_TO_FY = {v: k for k, v in X.FY_END.items()}


def annual_actuals(tag, unit):
    """{fiscal_year: value} for full-year facts whose end date is a Deere FY end."""
    out = {}
    for r in _rows(tag, unit):
        if 330 < _days(r) < 400 and r["end"] in END_TO_FY:
            out[END_TO_FY[r["end"]]] = r["val"]
    return out


def h1_actuals():
    """{fiscal_year: H1 net income USDm} -- 6-month facts starting at an FY start."""
    starts = {}
    for fy, end in X.FY_END.items():
        prev = X.FY_END.get(fy - 1)
        if prev:
            from datetime import date, timedelta
            starts[(date.fromisoformat(prev) + timedelta(days=1)).isoformat()] = fy
    out = {}
    for r in _rows("NetIncomeLoss", "USD"):
        if 170 < _days(r) < 200 and r["start"] in starts:
            out[starts[r["start"]]] = r["val"] / 1e6
    return out


# ------------------------------------------------- corpus segment / FY actuals
def _nums(line):
    out = []
    for tok in re.findall(r"[-+(]?\$?\s?[\d,]+(?:\.\d+)?\)?", line):
        t = tok.replace("$", "").replace(",", "").replace(" ", "")
        neg = t.startswith("(") or t.startswith("-")
        t = t.strip("()+-")
        if not t:
            continue
        try:
            v = float(t)
        except ValueError:
            continue
        out.append(-v if neg else v)
    return out


SEG_ROW = {
    "ag_turf": r"Agriculture and turf net sales",
    "cf_legacy": r"Construction and forestry net sales",
    "ppa": r"Production ?& ?ecision ?ag net sales|Production ?&ecisionAg net sales|Production ?& ?[Pp]recision ?[Aa]g net sales",
    "sat": r"Small ag ?& ?turf net sales",
    "cf": r"Construction ?& ?forestry net sales",
}


def segment_fy_actuals():
    """{seg: {fy: net sales USDm}} -- 10-K three-year segment tables first, then
    the Q4 8-K full-year column as a fallback for any year the 10-K text
    extraction did not carry."""
    out = {k: {} for k in SEG_ROW}
    d = os.path.join(X.CORPUS, "filings")
    for fn in sorted(os.listdir(d)):
        if not re.search(r"(q4-10k|fy-10k)", fn):
            continue
        pub = fn[:10]
        cand = [fy for fy, e2 in X.FY_END.items() if e2 <= pub]
        if not cand:
            continue
        fy0 = max(cand)
        txt = open(os.path.join(d, fn), encoding="utf-8", errors="replace").read().replace("&amp;", "&")
        for line in txt.split("\n"):
            l = line.strip()
            if not l.startswith("|"):
                continue
            for seg, pat in SEG_ROW.items():
                if re.search(pat, l, re.I):
                    vals = _nums(l)
                    for k, v in enumerate(vals[:3]):
                        out[seg].setdefault(fy0 - k, v)
    # fallback: Q4 8-K full-year column (numbers 3 and 4 = current FY, prior FY)
    for fn in sorted(os.listdir(d)):
        if not re.search(r"(q4-8k|fy-8k)", fn):
            continue
        pub = fn[:10]
        cand = [fy for fy, e2 in X.FY_END.items() if e2 <= pub]
        if not cand:
            continue
        fy0 = max(cand)
        txt = open(os.path.join(d, fn), encoding="utf-8", errors="replace").read().replace("&amp;", "&")
        for line in txt.split("\n"):
            l = line.strip()
            if not l.startswith("|"):
                continue
            for seg, pat in SEG_ROW.items():
                if re.search(pat.replace(" net sales", r" ?net sales"), l, re.I):
                    v = _nums(l)
                    if len(v) >= 5:
                        out[seg].setdefault(fy0, v[3])
                        out[seg].setdefault(fy0 - 1, v[4])
    return out


def ppa_operating_profit_actuals():
    """{fy: PPA operating profit USDm} from Q4 8-K full-year segment tables."""
    out = {}
    d = os.path.join(X.CORPUS, "filings")
    for fn in sorted(os.listdir(d)):
        if not re.search(r"(q4-8k|fy-8k)", fn):
            continue
        pub = fn[:10]
        cand = [fy for fy, e2 in X.FY_END.items() if e2 <= pub]
        if not cand:
            continue
        fy0 = max(cand)
        txt = open(os.path.join(d, fn), encoding="utf-8", errors="replace").read().replace("&amp;", "&")
        seen_op = False
        for line in txt.split("\n"):
            l = line.strip()
            if re.search(r"Operating profit:", l, re.I):
                seen_op = True
            if not seen_op or not l.startswith("|"):
                continue
            if re.search(r"Production ?& ?Precision Ag\s*\|", l, re.I) and "net sales" not in l.lower():
                v = _nums(l)
                if len(v) >= 6:
                    out[fy0] = v[3]
                break
    return out


# ------------------------------------------------------------------ row builder
ROWS = []
CUR_FQ = ["FY"]


def add(series, fy, value, units, stype, source, notes, fq=None, period_end=None):
    if value is None:
        return
    fq = fq or CUR_FQ[0]
    ROWS.append({
        "series_id": series,
        "period_end": period_end or X.FY_END[fy],
        "fiscal_year": fy,
        "fiscal_quarter": fq,
        "value": ("%g" % round(float(value), 4)),
        "units": units,
        "source_type": stype,
        "source": source,
        "notes": notes,
    })


def basis(issue_date):
    return "legacy-AT" if issue_date <= LEGACY_LAST_EVENT else "modern-PPA"


VINTAGE_SEQ = {"Q4": 0, "Q1": 1, "Q2": 2, "Q3": 3}


def vintage_note(issue_date, fq, fy, extra=""):
    """Every guidance row must say when the guidance was issued and from which release."""
    src_fy = fy - 1 if fq == "Q4" else fy
    n = ("guidance_issued=%s; guidance_vintage=FY%d %s earnings release; vintage_seq=%d; "
         "guides FY%d (period_end column)"
         % (issue_date, src_fy, fq, VINTAGE_SEQ[fq], fy))
    if fq == "Q4":
        n += ("; INITIAL guidance for the year -- issued with the PRIOR fiscal year's "
              "Q4/full-year results, i.e. before FY%d began" % fy)
    n += ("; the fiscal_quarter column on guidance rows is the VINTAGE quarter (which "
          "release the guidance came from), NOT a quarter of the guided period")
    return n + ("; " + extra if extra else "")


def main():
    seg_fy = segment_fy_actuals()
    ppa_op = ppa_operating_profit_actuals()
    log = []

    for issue_date, fq, fy, primary, _ in X.EVENTS:
        pflat = X.flat(primary)
        praw = X.read(primary)
        tr = X.transcript_for(issue_date)
        tflat = X.flat(tr) if tr else ""
        tenq = X.docs_for(issue_date)
        qflat = " ".join(X.flat(f) for f in tenq)
        slide = X.slide_for(issue_date)
        CUR_FQ[0] = fq
        vn = vintage_note(issue_date, fq, fy)

        # ---- consolidated net income guidance -------------------------------
        ni = X.extract_net_income(pflat) or (X.extract_net_income(tflat) if tflat else None)
        nisrc = primary if X.extract_net_income(pflat) else tr
        if ni:
            lo, hi, kind = ni
            kindnote = ("point estimate ('about $Xbn') -- low/mid/high identical"
                        if kind == "point" else "explicit guidance range")
            add("de_guidance_fy_net_income_low", fy, lo, "USDm", "filing", nisrc,
                vn + "; " + kindnote)
            add("de_guidance_fy_net_income_mid", fy, (lo + hi) / 2, "USDm", "filing", nisrc,
                vn + "; " + kindnote + "; mid = midpoint of low and high")
            add("de_guidance_fy_net_income_high", fy, hi, "USDm", "filing", nisrc,
                vn + "; " + kindnote)
            add("de_guidance_fy_net_income_range_width", fy, hi - lo, "USDm", "inference", nisrc,
                vn + "; high minus low; 0 for point guidance")
            # cross-check the same number in the 10-Q / 10-K where available
            if qflat:
                q = X.extract_net_income(qflat)
                if q:
                    agree = abs(q[0] - lo) < 60 and abs(q[1] - hi) < 60
                    log.append(("net_income", issue_date, "8K=%s/%s 10Q=%s/%s %s"
                                % (lo, hi, q[0], q[1], "AGREE" if agree else "DISAGREE")))
        else:
            log.append(("net_income", issue_date, "NOT FOUND"))

        # ---- adjusted net income (FY2018 tax-reform years) ------------------
        adj = X.extract_adj_net_income(pflat)
        add("de_guidance_fy_adjusted_net_income_mid", fy, adj, "USDm", "filing", primary,
            vn + "; non-GAAP adjusted net income excluding US tax-reform "
                 "provisional items; not comparable to the GAAP series")

        # ---- financial services net income ----------------------------------
        fs = X.extract_fs_net_income(pflat) or (X.extract_fs_net_income(qflat) if qflat else None)
        fssrc = primary if X.extract_fs_net_income(pflat) else (tenq[0] if tenq else primary)
        add("de_guidance_fy_financial_services_net_income", fy, fs, "USDm", "filing", fssrc,
            vn + "; net income attributable to Deere & Co for the financial services segment")

        # ---- consolidated net sales & revenues growth ------------------------
        rev = X.extract_total_rev_growth(pflat)
        add("de_guidance_fy_net_sales_revenues_growth", fy, rev, "percent", "filing", primary,
            vn + "; worldwide net sales AND revenues, y/y percent; Deere only published "
                 "this line FY2017-FY2019")

        # ---- segment net sales growth ---------------------------------------
        if issue_date <= LEGACY_LAST_EVENT:
            for seg, sid in (("ag_turf", "ag_turf"), ("cf", "cf")):
                g = X.extract_legacy_growth(pflat, seg)
                src, stype = primary, "filing"
                gt = X.extract_transcript_seg_sales(tflat, seg) if tflat else None
                if g and gt:
                    ok = abs(g[0] - gt[0]) < 1.01 and abs(g[1] - gt[1]) < 1.01
                    log.append(("seg_%s" % seg, issue_date,
                                "8K=%s transcript=%s %s" % (g, gt, "AGREE" if ok else "DISAGREE")))
                if g is None and gt:
                    g, src, stype = gt, tr, "filing"
                if g is None:
                    continue
                # never share a series_id across the FY2021 segment break
                name = "ag_turf" if seg == "ag_turf" else "cf_legacy_at"
                nt = (vn + "; segment_basis=legacy-AT; as_reported_or_restated=as-reported; "
                           "pre-FY2021 Agriculture & Turf reporting basis -- NOT comparable to "
                           "the modern PPA/SAT/CF segments")
                if seg == "cf":
                    nt = (vn + "; segment_basis=legacy-AT; as_reported_or_restated=as-reported; "
                               "Construction & Forestry as reported pre-FY2021")
                add("de_guidance_fy_segment_sales_growth_%s_low" % name, fy, g[0], "percent", stype, src, nt)
                add("de_guidance_fy_segment_sales_growth_%s_mid" % name, fy,
                    (g[0] + g[1]) / 2, "percent", stype, src, nt + "; mid = midpoint")
                add("de_guidance_fy_segment_sales_growth_%s_high" % name, fy, g[1], "percent", stype, src, nt)
            m = X.extract_at_operating_margin(tflat) if tflat else None
            add("de_guidance_fy_segment_operating_margin_ag_turf_mid", fy, m, "percent", "filing", tr,
                vn + "; segment_basis=legacy-AT; as_reported_or_restated=as-reported; "
                     "Agriculture & Turf division operating margin outlook from prepared remarks")
            mc = X.extract_cf_operating_margin(tflat) if tflat else None
            add("de_guidance_fy_segment_operating_margin_cf_legacy_at_mid", fy, mc, "percent", "filing", tr,
                vn + "; segment_basis=legacy-AT; as_reported_or_restated=as-reported")
        else:
            mod = X.extract_modern_segment_growth(praw)
            absol = X.extract_ppa_absolute_sales(praw)
            for seg in ("ppa", "sat", "cf"):
                nt = (vn + "; segment_basis=modern-PPA; as_reported_or_restated=as-reported; "
                           "FY2021+ Production & Precision Ag / Small Ag & Turf / "
                           "Construction & Forestry basis")
                g = mod.get(seg)
                src, stype = primary, "filing"
                if g is None and slide:
                    sd = X.slide_sales_direction(slide, seg)
                    so = X.extract_slide_segment_outlook(slide)
                    # slide sales range is only used as a documented fallback
                    if seg == "ppa" and issue_date == "2025-11-26" and sd == -1:
                        g, src = (-10.0, -5.0), slide
                        nt += ("; net-sales guidance recovered from the earnings-call slide "
                               "(FY2026 Fcst 5-10% with a downward arrow) because the 8-K "
                               "markdown table cell lost the 'Down 5 to' prefix in extraction")
                if g:
                    add("de_guidance_fy_segment_sales_growth_%s_low" % seg, fy, g[0], "percent", stype, src, nt)
                    add("de_guidance_fy_segment_sales_growth_%s_mid" % seg, fy,
                        (g[0] + g[1]) / 2, "percent", stype, src, nt + "; mid = midpoint")
                    add("de_guidance_fy_segment_sales_growth_%s_high" % seg, fy, g[1], "percent", stype, src, nt)
                if seg in absol:
                    a = absol[seg]
                    base0 = seg_fy[seg].get(fy - 1)
                    if base0 and not g:
                        glo = 100.0 * (a[0] / base0 - 1.0)
                        ghi = 100.0 * (a[1] / base0 - 1.0)
                        nt3 = (nt + "; INFERENCE -- FY2021 Q1 guided segment net sales in "
                                    "absolute dollars; growth derived against FY%d actual "
                                    "segment net sales of %.0f USDm" % (fy - 1, base0))
                        add("de_guidance_fy_segment_sales_growth_%s_low" % seg, fy, glo,
                            "percent", "inference", primary, nt3)
                        add("de_guidance_fy_segment_sales_growth_%s_mid" % seg, fy,
                            (glo + ghi) / 2, "percent", "inference", primary, nt3)
                        add("de_guidance_fy_segment_sales_growth_%s_high" % seg, fy, ghi,
                            "percent", "inference", primary, nt3)
                    add("de_guidance_fy_segment_sales_%s_usdm_low" % seg, fy, a[0], "USDm", "filing", primary,
                        nt + "; FY2021 Q1 guided segment net sales in absolute dollars, not growth")
                    add("de_guidance_fy_segment_sales_%s_usdm_high" % seg, fy, a[1], "USDm", "filing", primary,
                        nt + "; FY2021 Q1 guided segment net sales in absolute dollars, not growth")
            # currency / price drivers from the same 8-K table
            for col, label in ((2, "currency_translation"), (3, "price_realization")):
                dd = X.extract_modern_segment_driver(praw, col)
                for seg, v in dd.items():
                    add("de_guidance_fy_segment_%s_%s" % (label, seg), fy, v, "percent", "filing", primary,
                        vn + "; segment_basis=modern-PPA; as_reported_or_restated=as-reported; "
                             "component of the segment net-sales outlook")
            # operating margin outlook from the earnings-call slide deck
            if slide:
                so = X.extract_slide_segment_outlook(slide)
                for seg in ("ppa", "sat", "cf"):
                    mm = so.get(seg, {}).get("margin")
                    if not mm:
                        continue
                    nt = (vn + "; segment_basis=modern-PPA; as_reported_or_restated=as-reported; "
                               "segment operating-margin outlook, from the earnings-call slide deck")
                    add("de_guidance_fy_segment_operating_margin_%s_low" % seg, fy, mm[0], "percent", "filing", slide, nt)
                    add("de_guidance_fy_segment_operating_margin_%s_mid" % seg, fy,
                        (mm[0] + mm[1]) / 2, "percent", "filing", slide, nt + "; mid = midpoint")
                    add("de_guidance_fy_segment_operating_margin_%s_high" % seg, fy, mm[1], "percent", "filing", slide, nt)
                    # implied PPA operating profit -- the FY2026 Q3 forecast target
                    if seg == "ppa":
                        base = seg_fy["ppa"].get(fy - 1)
                        gg = mod.get("ppa") or ((-10.0, -5.0) if issue_date == "2025-11-26" else None)
                        if base and gg:
                            lo = base * (1 + gg[0] / 100.0) * mm[0] / 100.0
                            hi = base * (1 + gg[1] / 100.0) * mm[1] / 100.0
                            nt2 = (vn + "; segment_basis=modern-PPA; INFERENCE = FY%d actual PPA net "
                                        "sales (%.0f USDm) x (1 + guided sales growth) x guided operating "
                                        "margin. Deere does not guide segment operating profit in dollars."
                                   % (fy - 1, base))
                            add("de_guidance_fy_implied_ppa_operating_profit_low", fy, lo, "USDm",
                                "inference", primary + " + " + slide, nt2)
                            add("de_guidance_fy_implied_ppa_operating_profit_mid", fy, (lo + hi) / 2, "USDm",
                                "inference", primary + " + " + slide, nt2)
                            add("de_guidance_fy_implied_ppa_operating_profit_high", fy, hi, "USDm",
                                "inference", primary + " + " + slide, nt2)

    ROWS.sort(key=lambda r: (r["series_id"], r["period_end"], r["notes"]))
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, "de_guidance.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in ROWS:
            w.writerow(r)

    print("de_guidance.csv rows:", len(ROWS))
    for l in log:
        print("VALIDATE", l)
    return seg_fy, ppa_op


if __name__ == "__main__":
    main()
