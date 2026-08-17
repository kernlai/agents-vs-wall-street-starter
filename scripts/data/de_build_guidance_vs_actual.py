#!/usr/bin/env python3
"""Pair every Deere guidance vintage with the eventual actual and score the error.

Writes data/deere/de_guidance_vs_actual.csv.

Columns
  metric                 what is being compared
  fiscal_year            Deere fiscal year being guided
  period_end             fiscal-year end (ISO)
  vintage_quarter        Q4 = initial guidance issued with the PRIOR FY's Q4 results,
                         then Q1 / Q2 / Q3 of the guided year
  vintage_seq            0..3, ordering of the vintages within the year
  guidance_issued        date the guidance was published
  guidance_low/mid/high  the guidance itself (mid = midpoint; equal to low/high for
                         point guidance)
  units
  actual                 realised outturn
  error_abs              actual - guidance_mid  (positive = Deere under-promised)
  error_pct              100 * (actual - mid) / |mid|
  actual_vs_range        above | within | below | point_beat | point_miss
  cycle_phase            up_cycle / down_cycle, from the sign of FY y/y change in
                         consolidated net sales and revenues (computed, not asserted)
  source_guidance / source_actual
  notes
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import de_guidance_extract as X          # noqa: E402
import de_build_guidance as B            # noqa: E402

OUT = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_guidance_vs_actual.csv"
HEADER = ["metric", "fiscal_year", "period_end", "vintage_quarter", "vintage_seq",
          "guidance_issued", "guidance_low", "guidance_mid", "guidance_high", "units",
          "actual", "error_abs", "error_pct", "actual_vs_range", "cycle_phase",
          "source_guidance", "source_actual", "notes"]
SEQ = {"Q4": 0, "Q1": 1, "Q2": 2, "Q3": 3}
SEC = ("https://data.sec.gov/api/xbrl/companyconcept/CIK0000315189/us-gaap/%s.json")


def fmt(v, nd=2):
    return "" if v is None else ("%g" % round(v, nd))


def main():
    ni_act = {k: v / 1e6 for k, v in B.annual_actuals("NetIncomeLoss", "USD").items()}
    rev_act = {k: v / 1e6 for k, v in B.annual_actuals("Revenues", "USD").items()}
    eps_act = B.annual_actuals("EarningsPerShareDiluted", "USD/shares")
    h1 = B.h1_actuals()
    seg = B.segment_fy_actuals()
    ppa_op = B.ppa_operating_profit_actuals()

    cycle = {}
    for fy in sorted(rev_act):
        prev = rev_act.get(fy - 1)
        if prev:
            cycle[fy] = "up_cycle" if rev_act[fy] >= prev else "down_cycle"

    rows = []

    def emit(metric, fy, fq, issued, lo, mid, hi, units, actual, src_g, src_a, notes):
        if actual is None or mid is None:
            return
        err = actual - mid
        pct = 100.0 * err / abs(mid) if mid else None
        if lo == hi:
            pos = "point_beat" if actual >= mid else "point_miss"
        elif actual > hi:
            pos = "above"
        elif actual < lo:
            pos = "below"
        else:
            pos = "within"
        rows.append({
            "metric": metric, "fiscal_year": fy, "period_end": X.FY_END[fy],
            "vintage_quarter": fq, "vintage_seq": SEQ[fq], "guidance_issued": issued,
            "guidance_low": fmt(lo), "guidance_mid": fmt(mid), "guidance_high": fmt(hi),
            "units": units, "actual": fmt(actual), "error_abs": fmt(err),
            "error_pct": fmt(pct), "actual_vs_range": pos,
            "cycle_phase": cycle.get(fy, ""), "source_guidance": src_g,
            "source_actual": src_a, "notes": notes,
        })

    SEC_NI = SEC % "NetIncomeLoss"
    SEC_REV = SEC % "Revenues"

    for issue_date, fq, fy, primary, _ in X.EVENTS:
        pflat = X.flat(primary)
        tr = X.transcript_for(issue_date)
        tflat = X.flat(tr) if tr else ""
        praw = X.read(primary)

        # ---- full-year net income -------------------------------------------
        ni = X.extract_net_income(pflat) or (X.extract_net_income(tflat) if tflat else None)
        src = primary if X.extract_net_income(pflat) else tr
        if ni:
            lo, hi, kind = ni
            emit("fy_net_income", fy, fq, issue_date, lo, (lo + hi) / 2, hi, "USDm",
                 ni_act.get(fy), src, SEC_NI,
                 "GAAP net income attributable to Deere & Company; guidance kind=" + kind)

            # ---- H2 implied by the Q2 vintage vs H2 delivered ----------------
            if fq == "Q2" and fy in h1 and fy in ni_act:
                imp_lo, imp_hi = lo - h1[fy], hi - h1[fy]
                emit("fy_h2_net_income_implied_by_q2_guidance", fy, fq, issue_date,
                     imp_lo, (imp_lo + imp_hi) / 2, imp_hi, "USDm",
                     ni_act[fy] - h1[fy], src, SEC_NI,
                     "H2 = full-year guidance minus reported H1 actual (%0.0f USDm). "
                     "This is the exact inference required for FY2026 Q3 today."
                     % h1[fy])

        # ---- consolidated net sales & revenues growth ------------------------
        g = X.extract_total_rev_growth(pflat)
        if g is not None and fy in rev_act and (fy - 1) in rev_act:
            act = 100.0 * (rev_act[fy] / rev_act[fy - 1] - 1.0)
            emit("fy_net_sales_revenues_growth", fy, fq, issue_date, g, g, g, "percent",
                 act, primary, SEC_REV,
                 "worldwide net sales and revenues, y/y percent; point guidance")

        # ---- segment net sales growth ---------------------------------------
        if issue_date <= B.LEGACY_LAST_EVENT:
            pairs = [("ag_turf", "ag_turf"), ("cf_legacy_at", "cf_legacy")]
            gl = {}
            for k, _a in pairs:
                key = "ag_turf" if k == "ag_turf" else "cf"
                gl[k] = (X.extract_legacy_growth(pflat, key) or
                         (X.extract_transcript_seg_sales(tflat, key) if tflat else None))
            basis_note = ("segment_basis=legacy-AT; as_reported_or_restated=as-reported; "
                          "pre-FY2021 basis, not comparable with PPA/SAT/CF")
        else:
            mod = X.extract_modern_segment_growth(praw)
            if issue_date == "2025-11-26":
                mod.setdefault("ppa", (-10.0, -5.0))
            for k2, ab in X.extract_ppa_absolute_sales(praw).items():
                b0 = seg[k2].get(fy - 1)
                if b0 and k2 not in mod:
                    mod[k2] = (100.0 * (ab[0] / b0 - 1.0), 100.0 * (ab[1] / b0 - 1.0))
            pairs = [("ppa", "ppa"), ("sat", "sat"), ("cf", "cf")]
            gl = {k: mod.get(k) for k, _ in pairs}
            basis_note = ("segment_basis=modern-PPA; as_reported_or_restated=as-reported; "
                          "FY2021+ basis")
        for key, actkey in pairs:
            gg = gl.get(key)
            if not gg:
                continue
            cur, prev = seg[actkey].get(fy), seg[actkey].get(fy - 1)
            if cur is None or prev is None:
                continue
            act = 100.0 * (cur / prev - 1.0)
            emit("fy_segment_sales_growth_" + key, fy, fq, issue_date, gg[0],
                 (gg[0] + gg[1]) / 2, gg[1], "percent", act, primary,
                 "corpus 10-K segment table", basis_note)

        # ---- PPA operating margin -------------------------------------------
        slide = X.slide_for(issue_date)
        if slide and issue_date > B.LEGACY_LAST_EVENT:
            so = X.extract_slide_segment_outlook(slide)
            mm = so.get("ppa", {}).get("margin")
            if mm and fy in ppa_op and seg["ppa"].get(fy):
                act = 100.0 * ppa_op[fy] / seg["ppa"][fy]
                emit("fy_ppa_operating_margin", fy, fq, issue_date, mm[0],
                     (mm[0] + mm[1]) / 2, mm[1], "percent", act, slide,
                     "corpus Q4 8-K segment tables",
                     "segment_basis=modern-PPA; as_reported_or_restated=as-reported; "
                     "actual = FY PPA operating profit / FY PPA net sales")
                base = seg["ppa"].get(fy - 1)
                gg = mod.get("ppa")
                if base and gg:
                    lo = base * (1 + gg[0] / 100.0) * mm[0] / 100.0
                    hi = base * (1 + gg[1] / 100.0) * mm[1] / 100.0
                    emit("fy_ppa_operating_profit_implied", fy, fq, issue_date, lo,
                         (lo + hi) / 2, hi, "USDm", ppa_op.get(fy),
                         primary + " + " + slide, "corpus Q4 8-K segment tables",
                         "segment_basis=modern-PPA; INFERENCE -- Deere guides segment sales "
                         "growth and segment operating margin, not segment operating profit "
                         "in dollars; implied = prior-FY PPA net sales x (1+growth) x margin")

    rows.sort(key=lambda r: (r["metric"], r["fiscal_year"], r["vintage_seq"]))
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("de_guidance_vs_actual.csv rows:", len(rows))
    return rows


if __name__ == "__main__":
    main()
