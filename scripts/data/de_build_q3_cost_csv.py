#!/usr/bin/env python3
"""
Assemble de_q3_cost_inputs.csv -- the cost inputs that hit Deere's Q3 FY2026
(4 May - 2 Aug 2026) profit, plus the lag evidence linking them to the reported
production-cost bridge.

Tidy long format, one observation per row. Anything not established is simply
absent: no zero fills, no interpolation, no placeholder rows.
"""
import csv, json, datetime, argparse, os, re

HEADER = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "segment",
          "component", "value", "units", "source", "notes"]

SLIDE = "offline-corpus/slides/{}"
CALL_PRES = ("offline-corpus/call-transcripts/"
             "2026-05-21__de-us-20260521-call-pres__1042774.md")
CALL_QNA = ("offline-corpus/call-transcripts/"
            "2026-05-21__de-us-20260521-call-qna__1042775.md")
TENQ = ("offline-corpus/filings/2026-05-21__de-us-20260521-q2-10q__1055929.md")
EIGHTK = ("offline-corpus/filings/2026-05-21__de-us-20260521-q2-8k__1042167.md")
FREDSRC = "FRED https://fred.stlouisfed.org/series/{}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bridges", required=True)
    ap.add_argument("--panel", required=True)
    ap.add_argument("--fred", required=True)
    ap.add_argument("--lag", required=True)
    ap.add_argument("--warranty", required=True)
    ap.add_argument("--calendar", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    bridges = json.load(open(a.bridges))
    panel = json.load(open(a.panel))
    fred = json.load(open(a.fred))
    lag = json.load(open(a.lag))
    warr = json.load(open(a.warranty))
    cal = json.load(open(a.calendar))

    rows = []

    def add(sid, pend, fy, fq, seg, comp, val, units, src, note=""):
        rows.append({"series_id": sid, "period_end": pend, "fiscal_year": fy,
                     "fiscal_quarter": fq, "segment": seg, "component": comp,
                     "value": val, "units": units, "source": src, "notes": note})

    # ---------------------------------------------------------------- A. bridge
    for r in bridges["reconciled"]:
        seg = r.get("segment")
        if not seg:
            continue
        fy, q = int(r["end_label"][2:]), int(r["end_label"][0])
        pend = cal.get(f"{fy}Q{q}", "")
        note = (f"reconciles {r['start']}+components={r['end']}; "
                f"endpoints cross-checked vs 8-K segment table; "
                f"parse={r['style']}; status={r['status']}")
        for comp, v in r["components"].items():
            if v is None:
                continue
            add("de_op_bridge", pend, fy, q, seg, f"bridge_{comp}", v,
                "usd_millions_yoy_delta", SLIDE.format(r["file"]), note)
        add("de_op_bridge", pend, fy, q, seg, "operating_profit", r["end"],
            "usd_millions", SLIDE.format(r["file"]), "bridge endpoint = 8-K value")

    # rejected bridges recorded so the gaps are auditable
    for r in bridges["rejected"] + bridges["scrambled_label_order"]:
        el = r.get("end_label")
        if not el or not r.get("segment"):
            continue
        fy, q = int(el[2:]), int(el[0])
        add("de_op_bridge_rejected", cal.get(f"{fy}Q{q}", ""), fy, q, r["segment"],
            "bridge_rejected", "", "", SLIDE.format(r["file"]),
            f"REJECTED: {r.get('status')}; residual={r.get('residual')}; "
            f"no trustworthy label-to-value mapping recoverable")

    # ------------------------------------------------- B. segment panel context
    for r in panel["rows"]:
        if not r["key"].endswith("_op") and not r["key"].endswith("_sales"):
            continue
        if r["fy"] < 2021:
            continue
        seg, kind = r["key"].split("_")
        if seg == "FS":
            continue
        add("de_segment_8k", cal.get(f"{r['fy']}Q{r['q']}", ""), r["fy"], r["q"], seg,
            "net_sales" if kind == "sales" else "operating_profit", r["value"],
            "usd_millions", EIGHTK,
            f"8-K segment table, {r['n_sources']} independent source(s)"
            + ("; SOURCES DISAGREE" if r["conflict"] else ""))

    # -------------------------------------------------------- C. warranty level
    # quarterly new accruals / claims paid, reconstructed from cumulative
    # year-to-date disclosures where the quarter is not stated directly
    wq = {
        (2024, 1): (281, -309), (2024, 3): (280, -325),
        (2025, 1): (256, -310), (2025, 2): (227, -308), (2025, 3): (303, -336),
        (2026, 1): (342, -299), (2026, 2): (318, -294),
    }
    derived = {
        (2024, 2): (310, None, "9M FY24 accruals 871 less Q1 281 less Q3 280"),
        (2024, 4): (286, None, "FY24 accruals 1,157 less 9M 871"),
        (2025, 4): (362, None, "FY25 accruals 1,148 less 9M 786"),
    }
    for (fy, q), (acc, paid) in sorted(wq.items()):
        pend = cal.get(f"{fy}Q{q}", "")
        add("de_warranty", pend, fy, q, "CONSOLIDATED", "warranty_new_accruals",
            acc, "usd_millions", TENQ, "10-Q/10-K warranty liability rollforward")
        if paid is not None:
            add("de_warranty", pend, fy, q, "CONSOLIDATED", "warranty_claims_paid",
                paid, "usd_millions", TENQ, "10-Q/10-K warranty liability rollforward")
    for (fy, q), (acc, _p, note) in sorted(derived.items()):
        add("de_warranty", cal.get(f"{fy}Q{q}", ""), fy, q, "CONSOLIDATED",
            "warranty_new_accruals", acc, "usd_millions", TENQ,
            "derived by subtraction: " + note)
    for fy, q, val, comp in [(2026, 2, 1336, "warranty_liability_balance"),
                             (2025, 2, 1297, "warranty_liability_balance"),
                             (2026, 1, 1311, "warranty_liability_balance"),
                             (2025, 4, 1259, "warranty_liability_balance")]:
        add("de_warranty", cal.get(f"{fy}Q{q}", ""), fy, q, "CONSOLIDATED", comp,
            val, "usd_millions", TENQ, "end of period balance")

    # ------------------------------------------------- D. macro, fiscal-quarter
    for sid, d in fred.items():
        lv = lag["macro_quarterly"].get(sid, {})
        yy = lag["macro_yoy_pct"].get(sid, {})
        for k in sorted(lv):
            fy, q = int(k[:4]), int(k[-1])
            if fy < 2021:
                continue
            pend = cal.get(k, "")
            note = d["label"]
            if k == "2026Q3":
                note += ("; PARTIAL/CURRENT fiscal quarter 2026-05-04..2026-08-02, "
                         "quarter-end date derived as 13 weeks after the reported "
                         "Q2 end (2026-05-03), not yet reported by Deere")
            add(f"macro_{d['family']}", pend, fy, q, "MACRO",
                f"{sid}_level_qtr_avg", round(lv[k], 3), d["units"],
                FREDSRC.format(sid), note)
            if k in yy:
                add(f"macro_{d['family']}", pend, fy, q, "MACRO",
                    f"{sid}_yoy_pct", round(yy[k], 2), "percent_yoy",
                    FREDSRC.format(sid), note)

    # ------------------------------------------------------- E. macro, monthly
    for sid, d in fred.items():
        for dt, v in d["obs"]:
            if dt < "2025-08-01":
                continue
            add(f"macro_{d['family']}_monthly", dt, "", "", "MACRO",
                f"{sid}_observation", v, d["units"], FREDSRC.format(sid),
                d["label"] + "; observation date as published by FRED")

    # ---------------------------------------------------------- F. lag evidence
    for c in lag["correlations"]:
        if c["component"] != "production_costs":
            continue
        note = (f"Pearson r, YoY% of quarter-averaged input vs bridge "
                f"production-cost component; n={c['n']}, "
                f"AR(1)-adjusted effective n={c['n_eff']}")
        if "r_partial_vs_PPIACO" in c:
            note += f"; partial r controlling PPI-all-commodities={c['r_partial_vs_PPIACO']}"
        if "r_first_diff" in c:
            note += f"; first-differenced r={c['r_first_diff']} (n={c['n_first_diff']})"
        add("lag_correlation", "", "", "", c["segment"],
            f"corr_prodcost_vs_{c['series']}_lag{c['lag_quarters']}q", c["r"],
            "pearson_r", "derived: de_lag_analysis.py", note)

    # -------------------------------------------- G. Deere quantified statements
    S = [
        (272, "usd_millions", "tariff_refund_recognised_q2fy26", CALL_PRES,
         "IEEPA refund claims filed and accepted by US Customs, recognised in "
         "Q2 FY2026; 'benefited our production cost this quarter and lifted "
         "margins by nearly 2.5 points'; ONE-OFF, no equivalent assumed in Q3"),
        (2.5, "percentage_points", "tariff_refund_margin_lift_q2fy26", CALL_PRES,
         "equipment operations margin lift from the $272m refund"),
        (200, "usd_millions", "tariff_direct_expense_yoy_headwind_q2fy26", CALL_PRES,
         "'year-over-year direct tariff expense was approximately $200 million "
         "of the headwind, with the remainder largely driven by higher material "
         "and freight costs' (excluding the refund)"),
        (1200, "usd_millions", "tariff_direct_exposure_fy2026_gross", CALL_PRES,
         "full-year direct tariff exposure, unchanged after IEEPA invalidation, "
         "Section 122 introduction and Section 232 adjustments; ~3% margin headwind"),
        (900, "usd_millions", "tariff_cost_fy2026_net_of_refunds", CALL_QNA,
         "$1.2bn gross run-rate less the $272m refund"),
        (3.0, "percentage_points", "tariff_margin_headwind_fy2026", CALL_QNA,
         "full-year tariff expense worth about 3 points of margin"),
        (20, "percent", "tariff_exposure_share_large_ag", CALL_QNA,
         "segment split of tariff exposure: ~50% Construction & Forestry, "
         "~33% Small Ag & Turf, ~20% large ag (PPA); refund split described as "
         "'pretty close to the tariff exposure as well'"),
        (50, "percent", "tariff_exposure_share_construction_forestry", CALL_QNA, ""),
        (33, "percent", "tariff_exposure_share_small_ag_turf", CALL_QNA, ""),
        (54, "usd_millions", "tariff_refund_ppa_share_estimate", CALL_QNA,
         "DERIVED, not disclosed: 20% of the $272m refund on the stated exposure "
         "split; implies PPA Q2 FY2026 production-cost bridge of about -131 "
         "excluding the refund, versus the reported -77"),
        (1.75, "percent", "price_realization_guide_fy2026_midpoint", CALL_QNA,
         "'implied net price realization for the equipment operations is between "
         "1.5% and 2% for the year'; Deere explicitly is NOT surcharging tariffs"),
        (1.75, "percent", "general_inflation_ex_tariffs_fy2026_midpoint", CALL_QNA,
         "'our general inflation rates, excluding tariffs, of also about 1.5%-2%'"),
        (80, "percent", "us_complete_goods_made_in_us", CALL_PRES,
         "'approximately 80% of John Deere's U.S. complete good sales are produced "
         "at our U.S. manufacturing facilities'"),
        (75, "percent", "us_components_sourced_domestically", CALL_PRES,
         "'roughly 75% of those components used at those facilities are sourced "
         "from U.S.-based suppliers'"),
        (157, "usd_millions", "consolidated_production_cost_headwind_q2fy26_pretax", TENQ,
         "MD&A: 'increased production costs of $122 ($157 pretax) from higher "
         "material costs'"),
        (82, "usd_millions", "consolidated_warranty_headwind_q2fy26_pretax", TENQ,
         "MD&A: 'higher warranty expenses of $64 ($82 pretax)'"),
    ]
    for val, units, comp, src, note in S:
        add("de_statement", "2026-05-21", 2026, 2, "COMPANY", comp, val, units,
            src, note)

    for comp, note, src in [
        ("order_book_visibility_q3_q4",
         "'Model year 2026 production of seasonal products is largely set by our "
         "early order programs, which have been closed for several months now.'",
         CALL_PRES),
        ("order_book_large_tractors",
         "'Regarding Waterloo large tractors, order books are well into the fourth "
         "quarter as we look to close out our model year 2026 production.'",
         CALL_PRES),
        ("order_book_europe_south_america",
         "'Order visibility in both regions now extends through the third quarter "
         "and into the fourth.'", CALL_PRES),
        ("production_shape_q4_weighted",
         "'a little bit better absorption in the fourth quarter as production rates "
         "are significantly higher... that's just the way the order book built this "
         "year for a much heavier fourth quarter with respect to our large tractors' "
         "-- implies Q3 FY2026 PPA build is the lighter of the two back-half quarters",
         CALL_QNA),
        ("my2027_production_starts_q4",
         "'We're just launching EOPs for model year 2027 spring products, which will "
         "begin production in the last few months of the fiscal year' -- MY2027 build "
         "does not contribute to Q3", CALL_PRES),
        ("inflation_last_two_three_months",
         "'we are seeing some high levels of inflation over the last two or three "
         "months' (i.e. roughly March-May 2026)", CALL_QNA),
        ("back_half_comps_more_favourable",
         "'we're lapping tariffs that we started to see come into business last year, "
         "and we're starting to lap the indirect inflation... The comps become more "
         "favorable.' NOTE: the PPA bridge shows tariffs hit hardest in 4Q FY2025 "
         "(production costs -147) while 3Q FY2025 was +69, so the lapping benefit "
         "lands mainly in Q4 FY2026, not Q3", CALL_QNA),
        ("no_tariff_surcharge_policy",
         "'we are not surcharging our customers on tariffs... focusing on reducing "
         "our tariff exposure through cost actions'", CALL_QNA),
    ]:
        add("de_statement", "2026-05-21", 2026, 2, "COMPANY", comp, "", "text",
            src, note)

    # ------------------------------------------------------- H. tariff regime
    T = [
        ("2026-02-20", "scotus_ieepa_struck_down", "",
         "Supreme Court rules 6-3 that IEEPA does not authorise the president to "
         "impose tariffs; basis for Deere's $272m refund claim",
         "https://www.millerchevalier.com/publication/supreme-court-finds-ieepa-tariffs-unlawful-what-you-need-know"),
        ("2026-02-20", "section_122_surcharge_rate_initial", 10,
         "Section 122 Trade Act 1974 proclamation: flat 10% ad valorem surcharge "
         "on all imports, replacing IEEPA tariffs",
         "https://www.troutman.com/insights/supreme-court-strikes-down-ieepa-tariffs-trump-responds-with-section-122-global-surcharge/"),
        ("2026-02-22", "section_122_surcharge_rate_raised", 15,
         "surcharge raised from 10 to 15 percentage points",
         "https://globaltradealert.org/reports/S122-US-Tariff-Estimates"),
        ("2026-05-07", "section_122_invalidated_by_cit", "",
         "Court of International Trade invalidates the global Section 122 tariffs -- "
         "four days INTO Deere's Q3 FY2026; a live source of further refund or "
         "expense revision inside the quarter",
         "https://www.millernash.com/firm-news/news/tariffs-in-flux-ieepa-and-section-122-struck-down-section-232-duties-expand"),
        ("2026-04-06", "section_232_steel_primary_rate", 25,
         "Section 232 steel primary metals rate under the April 2026 proclamation; "
         "tiered derivative-product structure, 50% on certain primary metal products",
         "https://www.millernash.com/firm-news/news/tariffs-in-flux-ieepa-and-section-122-struck-down-section-232-duties-expand"),
        ("2026-04-06", "section_232_aluminium_primary_rate", 10,
         "Section 232 aluminium primary metals rate; tiered derivative structure",
         "https://www.millernash.com/firm-news/news/tariffs-in-flux-ieepa-and-section-122-struck-down-section-232-duties-expand"),
        ("2026-04-06", "section_232_copper_added", "",
         "copper and derivatives brought under Section 232, ~25% for certain "
         "copper articles; Section 232 goods are exempt from the Section 122 surcharge",
         "https://www.millernash.com/firm-news/news/tariffs-in-flux-ieepa-and-section-122-struck-down-section-232-duties-expand"),
    ]
    for d, comp, val, note, src in T:
        add("tariff_regime", d, 2026, 3 if d >= "2026-05-04" else 2, "POLICY",
            comp, val, "percent" if isinstance(val, int) else "event", src, note)

    # -------------------------------------------- I. production announcements
    P = [
        ("2026-02-06", "waterloo_worker_callbacks", 146,
         "Deere recalls 146 workers to four Waterloo facilities (Drivetrain, Tractor "
         "Operations, Engine Works, Foundry) starting early March 2026, citing "
         "'increased customer demand' for 8R tractor production. EXPANSIONARY for "
         "PPA large ag inside the Q2/Q3 FY2026 build window -- evidence AGAINST an "
         "extended summer shutdown",
         "https://cbs2iowa.com/news/local/john-deere-announces-146-waterloo-worker-callbacks-citing-increased-production-demand"),
        ("2026-04-28", "ankeny_des_moines_works_layoffs", 120,
         "~120 workers laid off at Des Moines Works, Ankeny IA in three groups on "
         "28 Mar, 4 Apr and 28 Apr 2026. Ankeny builds sprayers/cotton -- PPA "
         "adjacent. All three dates fall in Q2 FY2026, before the Q3 window opens",
         "https://www.yahoo.com/news/ankeny-john-deere-facility-lay-193925445.html"),
        ("2026-08-14", "no_extended_summer_shutdown_found", "",
         "SEARCHED AND NOT FOUND: no announcement of an extended or additional "
         "summer shutdown, seasonal layoff or production-rate cut in the "
         "4 May - 2 Aug 2026 window. WARN aggregator shows no John Deere filings "
         "in calendar 2026. Absence of evidence in public news, not a company "
         "statement that none occurred",
         "https://warnact.io/company-john-deere"),
    ]
    for d, comp, val, note, src in P:
        add("production_event", d, 2026, 3 if d >= "2026-05-04" else 2, "PPA",
            comp, val, "workers" if isinstance(val, int) else "event", src, note)

    # ------------------------- J. Q3 cost impulse at each series' best-fit lag
    def shiftq(k, l):
        fy, q = int(k[:4]), int(k[-1])
        i = fy * 4 + (q - 1) - l
        return f"{i // 4}Q{i % 4 + 1}"

    best = {}
    for c in lag["correlations"]:
        if c["segment"] != "PPA" or c["component"] != "production_costs":
            continue
        b = best.get(c["series"])
        if b is None or abs(c["r"]) > abs(b["r"]):
            best[c["series"]] = c
    for sid, c in best.items():
        L = c["lag_quarters"]
        my = lag["macro_yoy_pct"][sid]
        w2, w3 = shiftq("2026Q2", L), shiftq("2026Q3", L)
        y2, y3 = my.get(w2), my.get(w3)
        lbl = fred[sid]["label"]
        if y3 is not None:
            add("q3_cost_impulse", cal.get("2026Q3", ""), 2026, 3, "PPA",
                f"{sid}_yoy_at_best_lag{L}q", round(y3, 2), "percent_yoy",
                FREDSRC.format(sid),
                f"{lbl}; input window feeding Q3 FY2026 at the lag that maximises "
                f"|r| vs the PPA production-cost bridge (r={c['r']}, n={c['n']}, "
                f"n_eff={c['n_eff']}); window={w3}")
        if y2 is not None and y3 is not None:
            add("q3_cost_impulse", cal.get("2026Q3", ""), 2026, 3, "PPA",
                f"{sid}_impulse_change_q2_to_q3", round(y3 - y2, 2),
                "percentage_points", FREDSRC.format(sid),
                f"{lbl}; change in the lagged YoY cost impulse between the window "
                f"feeding Q2 FY2026 ({w2}, {y2:+.1f}%) and the window feeding "
                f"Q3 FY2026 ({w3}, {y3:+.1f}%). Positive = cost headwind worsens "
                f"sequentially into Q3")

    # ------------------------------------- K. derived Q3 bridge-component build
    B = [
        ("ppa_production_costs_q2fy26_reported", -77, "usd_millions_yoy_delta",
         "reconciled 2Q FY2026 PPA bridge, endpoints 1,148 -> 706 verified vs 8-K"),
        ("ppa_production_costs_q2fy26_ex_refund", -131, "usd_millions_yoy_delta",
         "DERIVED: reported -77 less the estimated $54m PPA share (20% of $272m) "
         "of the one-off IEEPA refund that Deere said benefited production cost"),
        ("ppa_production_costs_q3fy25_prior_year_comp", 69, "usd_millions_yoy_delta",
         "3Q FY2025 PPA bridge production-cost component (a FAVOURABLE +69). The "
         "prior-year quarter was NOT yet carrying the full tariff run rate, so the "
         "Q3 FY2026 comparison base is a hard one -- the lapping relief management "
         "described lands mainly in Q4, where 4Q FY2025 was -147"),
        ("ppa_production_costs_q3fy26_central_estimate", -115,
         "usd_millions_yoy_delta",
         "DERIVED SCENARIO, not a company figure. Builds from the Q2 ex-refund run "
         "rate of about -131, adds roughly +20 for a smaller year-on-year direct "
         "tariff step (Q3 FY2025 already carried early tariff expense; PPA share of "
         "the ~$200m Q2 enterprise tariff headwind is about $40m on the 20% split), "
         "and subtracts for the worsening lagged material and energy impulse "
         "(HRC steel +10.0% vs +2.5%, diesel PPI +70% vs -6%, aluminium +17.9% vs "
         "+10.0%) plus weaker Q3 overhead absorption given the Q4-weighted build"),
        ("ppa_production_costs_q3fy26_low", -180, "usd_millions_yoy_delta",
         "DERIVED SCENARIO low end: full material/energy pass-through, no new "
         "tariff refund, absorption drag from the light Q3 build"),
        ("ppa_production_costs_q3fy26_high", -50, "usd_millions_yoy_delta",
         "DERIVED SCENARIO high end: cost actions bite, and/or a further tariff "
         "refund lands following the 7 May 2026 Court of International Trade ruling "
         "invalidating Section 122 -- the same mechanism that produced the $272m "
         "Q2 item, which arrived unannounced and moved equipment margin 2.5 points"),
        ("ppa_warranty_q3fy26_central_estimate", -45, "usd_millions_yoy_delta",
         "DERIVED SCENARIO. Consolidated new product warranty accruals are running "
         "342 in Q1 FY2026 (+34% YoY) and 318 in Q2 (+40% YoY) while claims paid are "
         "flat to lower, so the step-up is provisioning, not payout. Q3 FY2025 "
         "accruals were 303; a repeat of the +30-40% pace implies roughly +90 to "
         "+120 of enterprise headwind, of which PPA has taken 33-100% in recent "
         "quarters (PPA warranty bridge -48 in Q1 FY2026, -51 in Q2)"),
        ("ppa_warranty_q3fy26_range_low", -70, "usd_millions_yoy_delta",
         "DERIVED SCENARIO low end"),
        ("ppa_warranty_q3fy26_range_high", -20, "usd_millions_yoy_delta",
         "DERIVED SCENARIO high end; warranty has flipped sign quarter to quarter "
         "in this series (PPA +32 in 2Q FY2025, -45 in 3Q FY2025, +23 in 4Q FY2025), "
         "which is why it belongs in the uncertainty band and not the point estimate"),
    ]
    for comp, val, units, note in B:
        add("q3_cost_build", cal.get("2026Q3", ""), 2026, 3, "PPA", comp, val,
            units, "derived: de_build_q3_cost_csv.py", note)

    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"rows={len(rows)} -> {a.out}")


if __name__ == "__main__":
    main()
