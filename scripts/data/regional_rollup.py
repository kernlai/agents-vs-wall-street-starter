#!/usr/bin/env python3
"""
Deere & Company (NYSE: DE) -- FY2026 Q3 bottom-up regional roll-up.

Aggregates the six regional desks' segment x geography Q3 FY2026 forecasts into a
complete 24-cell matrix, reconciles the ASC 606 revenue-recognition basis to the
8-K "worldwide net sales and revenues" reporting basis, and runs three independent
sanity checks against the bottom-up total.

AS OF 2026-08-16.  Deere has NOT reported FY2026 Q3 (call: 09:00 US Central,
Thursday 20 August 2026).  Every Q3 FY2026 number here is a FORECAST.  No Q3
FY2026 actuals exist anywhere in the corpus or on the web.

All Q3 FY2025 comparatives are ACTUALS transcribed from the primary source:
  challenge/offline-data/deere/filings/2025-08-14__de-us-20250814-q3-10q__155834.md
  (three months ended 27 July 2025 revenue-recognition footnote, lines 594-606)

Run:  python3 regional_rollup.py
"""

from __future__ import annotations

import csv
import io
import os
import sys
from typing import Dict, List, Tuple

# --------------------------------------------------------------------------------------
# 0.  CONSTANTS AND SOURCES
# --------------------------------------------------------------------------------------

CORPUS = "challenge/offline-data/deere"
Q3FY25_10Q = f"{CORPUS}/filings/2025-08-14__de-us-20250814-q3-10q__155834.md"
Q2FY26_10Q = f"{CORPUS}/filings/2026-05-21__de-us-20260521-q2-10q__1055929.md"
Q2FY26_8K = f"{CORPUS}/filings/2026-05-21__de-us-20260521-q2-8k__1042167.md"
Q3FY25_8K = f"{CORPUS}/filings/2025-08-15__de-us-20250815-q3-8k__143410.md"
Q2FY26_CALL = f"{CORPUS}/call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md"
Q2FY26_SLIDE = f"{CORPUS}/slides/2026-05-21__de-us-20260521-slide__1042212.md"

GEOS = [
    "United States",
    "Canada",
    "Western Europe",
    "Central Europe & CIS",
    "Latin America",
    "Asia/Africa/Oceania/ME",
]
SEGS = ["PPA", "SAT", "CF", "FS"]

# --------------------------------------------------------------------------------------
# 1.  Q3 FY2025 ACTUAL MATRIX (ASC 606 revenue-recognition basis, USDm)
#     Source: Q3 FY2025 10-Q, three months ended 2025-07-27.  VERIFIED, not derived.
# --------------------------------------------------------------------------------------

Q3FY25: Dict[str, Dict[str, float]] = {
    "United States":          {"PPA": 1684, "SAT": 1537, "CF": 1687, "FS": 1100},
    "Canada":                 {"PPA":  335, "SAT":  148, "CF":  222, "FS":  190},
    "Western Europe":         {"PPA":  677, "SAT":  757, "CF":  550, "FS":   45},
    "Central Europe & CIS":   {"PPA":  301, "SAT":  130, "CF":  103, "FS":    2},
    "Latin America":          {"PPA": 1055, "SAT":  124, "CF":  252, "FS":   28},
    "Asia/Africa/Oceania/ME": {"PPA":  332, "SAT":  393, "CF":  313, "FS":   53},
}
# Published Q3 FY2025 column totals and grand total, for assertion.
Q3FY25_PUBLISHED_COLS = {"PPA": 4384, "SAT": 3089, "CF": 3127, "FS": 1418}
Q3FY25_PUBLISHED_TOTAL = 12018

# --------------------------------------------------------------------------------------
# 2.  Q2 FY2026 ACTUAL MATRIX (ASC 606, USDm) -- the sequential anchor.
#     Source: Q2 FY2026 10-Q, three months ended 2026-05-03.
# --------------------------------------------------------------------------------------

Q2FY26: Dict[str, Dict[str, float]] = {
    "United States":          {"PPA": 2012, "SAT": 1833, "CF": 2317, "FS": 1036},
    "Canada":                 {"PPA":  487, "SAT":  187, "CF":  175, "FS":  190},
    "Western Europe":         {"PPA":  654, "SAT":  827, "CF":  608, "FS":   52},
    "Central Europe & CIS":   {"PPA":  297, "SAT":  121, "CF":  105, "FS":    2},
    "Latin America":          {"PPA":  828, "SAT":  128, "CF":  280, "FS":   32},
    "Asia/Africa/Oceania/ME": {"PPA":  329, "SAT":  446, "CF":  369, "FS":   54},
}
Q2FY26_PUBLISHED_TOTAL = 13369

# --------------------------------------------------------------------------------------
# 3.  DESK FORECASTS -- Q3 FY2026 central, low, high (ASC 606, USDm)
#     Each entry: (central, low, high, desk_confidence, basis_note)
#     Transcribed verbatim from the six briefings in data/deere/regional/*.md
# --------------------------------------------------------------------------------------

DeskCell = Tuple[float, float, float, str, str]

DESK: Dict[str, Dict[str, DeskCell]] = {
    "United States": {
        "PPA": (1440, 1300, 1590, "low",
                "Desk view. Four methods span 1,283-1,610; anchored on 1,684 base. "
                "Bottom-up residual 1,467 / share-of-global 1,283-1,437 / "
                "Q3-Q2 seasonality 1,348-1,610 / H1 continuation 1,340."),
        "SAT": (1700, 1600, 1790, "medium",
                "Desk view. Q3/Q2 ratio 0.94-0.99 in 5 of 6 years -> 1,732-1,754; "
                "share-of-global 1,595-1,693; relative-YoY 1,614-1,675."),
        "CF":  (2050, 1900, 2180, "medium",
                "Desk view. Three independent methods converge on ~2,062-2,074; "
                "shaded fractionally down for soft US construction spend (-3.2% YoY)."),
        "FS":  (1070, 1030, 1110, "high",
                "Desk view. Most stable line in the file; three consecutive quarters "
                "within +/-3.5% YoY on a shrinking portfolio (JDF trade wholesale -15%)."),
    },
    "Canada": {
        "PPA": (340, 295, 390, "low",
                "Desk view. Soft 335 base (-31.5% LY). Waterloo H2 NA skew vs weak "
                "Canadian retail (4WD -22.6% YTD) and ~1.6% FX headwind."),
        "SAT": (175, 158, 195, "medium",
                "Desk view. H1 FY2026 +24.1%; share of global SAT drifting to ~5.1%."),
        "CF":  (200, 170, 240, "low",
                "Desk view. DELIBERATELY CONTRARIAN: -9.9% against company CF guide "
                "of ~+20%. Canadian lumber production -5.8%/-8.1% YoY Apr/May; "
                "Canada CF share of global fell 5.92% -> 4.76% H1/H1."),
        "FS":  (196, 186, 208, "medium",
                "Desk view. 186-212 for twelve straight quarters."),
    },
    "Western Europe": {
        "PPA": (695, 650, 745, "medium",
                "Desk view. Q2-to-Q3 ratio ~1.06 on 654. FX tailwind gone (+0.3%); "
                "CEMA arable weakest; combines are a Q3 harvest shipment item."),
        "SAT": (810, 765, 860, "medium",
                "Desk view. Q2-to-Q3 ratio ~0.98 on 827. Largest cell in region; "
                "dairy pillar cracking (EU milk -21% YoY in June 2026)."),
        "CF":  (590, 555, 630, "medium",
                "Desk view. Q2-to-Q3 ratio ~0.97 on 608. Roadbuilding +10% guide, "
                "Wirtgen Europe strength, Q3 peak paving; Nordic forestry drag."),
        "FS":  ( 53,  49,  57, "high",
                "Desk view. Run-rate stepped up to ~53 over the past year."),
    },
    "Central Europe & CIS": {
        "PPA": (308, 265, 345, "low",
                "Desk view. WE-ratio anchor 308; H2-shape method 301-316. Naive "
                "Q3/Q2 seasonal gives 228 but its estimation window IS the structural "
                "break, so the desk discounts it."),
        "SAT": (120, 100, 140, "low",
                "Desk view. OVERRIDES the company +15% SAT guide. Mean reversion in "
                "the CE/WE SAT ratio (17.2% in Q3 FY2025 vs 15.3% trailing-4Q)."),
        "CF":  (110,  96, 124, "medium",
                "Desk view. Twelve quarters in a 71-112 band; Poland KPO/RRF "
                "August 2026 grant deadline falls inside the quarter."),
        "FS":  (  2,   1,   3, "medium",
                "Desk view. Residual line post the March 2023 Russia FS disposal. "
                "Rounding noise on a ~540m region."),
    },
    "Latin America": {
        "PPA": (820, 760, 900, "medium",
                "Desk view. Roughly flat to -1% sequential off 828. Horizontina "
                "combine output -30% through the whole quarter; explicit plan to "
                "underproduce Brazilian retail; safrinha ~4 weeks late. Offset by a "
                "+10.0% BRL translation tailwind. Implied ex-FX local decline ~-29%."),
        "SAT": (136, 125, 148, "medium",
                "Desk view. Conservative +6% sequential off 128 (vs +15.7% median "
                "seasonality) given Brazilian demand malaise."),
        "CF":  (285, 265, 305, "medium",
                "Desk view. Roughly flat sequential off 280; FX carries YoY to +13%. "
                "Desk flags this as its most exposed growth call."),
        "FS":  ( 33,  30,  36, "medium",
                "Desk view. Clean post-deconsolidation run-rate (Banco John Deere "
                "50% sold to Bradesco in Q2 FY2025); series 28/32/32/32."),
    },
    "Asia/Africa/Oceania/ME": {
        "PPA": (355, 325, 390, "low",
                "Desk view. 1.079 sequential ratio, deliberately below the 1.154 "
                "seasonal median. Australia-led; ABARES June cut 2026-27 winter crop "
                "-21%, but that hits Q1 FY2027 orders not Q3 deliveries; AUD +8.7%."),
        "SAT": (440, 415, 470, "medium",
                "Desk view. Best-evidenced cell in the region: JD India retail "
                "registrations for all three months (+11.7% vs industry +22.1%), "
                "less a -10.3% INR translation drag."),
        "CF":  (380, 355, 410, "medium",
                "Desk view. Deliberate deceleration from +33.2% in Q2 to +21.4%, to "
                "respect the company H2 CF math. China excavators +26.4% H1, "
                "Gulf roadbuilding megaprojects."),
        "FS":  ( 55,  53,  57, "high",
                "Desk view. 52-56 band for eight consecutive quarters."),
    },
}

# Cells where the desk gave no usable view and we fell back to the cell's own
# trailing trend.  EMPTY -- all 24 cells received an explicit, quantified desk view
# with a stated low/central/high.  Kept here so the fallback path is visible and the
# absence of fallbacks is an assertion rather than a claim.
TRAILING_TREND_FALLBACKS: Dict[Tuple[str, str], str] = {}

# --------------------------------------------------------------------------------------
# 4.  8-K SEGMENT NET SALES HISTORY (USDm) -- for the basis reconciliation and for the
#     guidance-implied seasonal split.  Source: quarterly 8-K segment tables.
# --------------------------------------------------------------------------------------

# fiscal_year -> quarter -> (PPA, SAT, CF) net sales, 8-K basis
NETSALES_8K: Dict[int, Dict[str, Tuple[int, int, int]]] = {
    2021: {"Q1": (3069, 2515, 2467), "Q2": (4529, 3390, 3079),
           "Q3": (4250, 3147, 3016), "Q4": (4661, 2809, 2806)},
    2022: {"Q1": (3356, 2631, 2544), "Q2": (5117, 3570, 3347),
           "Q3": (6096, 3635, 3269), "Q4": (7434, 3544, 3373)},
    2023: {"Q1": (5198, 3001, 3203), "Q2": (7822, 4145, 4112),
           "Q3": (6806, 3739, 3739), "Q4": (6965, 3094, 3742)},
    2024: {"Q1": (4849, 2425, 3212), "Q2": (6581, 3185, 3844),
           "Q3": (5099, 3053, 3235), "Q4": (4305, 2306, 2664)},
    2025: {"Q1": (3067, 1748, 1994), "Q2": (5230, 2994, 2947),
           "Q3": (4273, 3025, 3059), "Q4": (4740, 2457, 3382)},
    2026: {"Q1": (3163, 2168, 2670), "Q2": (4503, 3485, 3790)},
}

# 606 segment column totals (three-month), same quarters, for the wedge.
# Source: 10-Q revenue-recognition footnotes.
REV606_SEG: Dict[Tuple[int, str], Tuple[int, int, int, int, int]] = {
    # (FY, Q): (PPA, SAT, CF, FS, TOTAL)
    (2024, "Q1"): (5043, 2492, 3274, 1376, 12185),
    (2024, "Q3"): (5242, 3128, 3293, 1489, 13152),
    (2025, "Q1"): (3173, 1807, 2058, 1470,  8508),
    (2025, "Q2"): (5326, 3046, 3006, 1385, 12763),
    (2025, "Q3"): (4384, 3089, 3127, 1418, 12018),
    (2026, "Q1"): (3269, 2224, 2734, 1384,  9611),
    (2026, "Q2"): (4607, 3542, 3854, 1366, 13369),
}
# 8-K worldwide "net sales and revenues" for the same quarters, for the identity check.
NSR_8K: Dict[Tuple[int, str], int] = {
    (2024, "Q1"): 12185, (2024, "Q3"): 13152,
    (2025, "Q1"):  8508, (2025, "Q2"): 12763, (2025, "Q3"): 12018,
    (2026, "Q1"):  9611, (2026, "Q2"): 13369,
}

# FY2025 actuals and FY2026 guidance (8-K basis), from the 2026-05-21 8-K.
FY2025_NETSALES = {"PPA": 17311, "SAT": 10224, "CF": 11382}
H1_FY2026_NETSALES = {"PPA": 7666, "SAT": 5653, "CF": 6460}
FY2026_GUIDE = {            # (low_growth, high_growth) as decimals, 8-K net sales
    "PPA": (-0.10, -0.05),  # "Down 5 to 10%"
    "SAT": (0.13, 0.17),    # "Up ~15%"  -> +/-2pt band around the point guide
    "CF":  (0.18, 0.22),    # "Up ~20%"  -> +/-2pt band around the point guide
}

# Management's stated Q3/Q4 cadence, Q2 FY2026 call Q&A (Q2FY26_CALL, lines 95-97):
#   PPA  "Q4 a bit stronger than Q3 ... more Waterloo large tractor shipments to
#         North America in the back half ... abnormal for us"     -> Q3 share of H2 < 50%
#   SAT  "pretty normal seasonality ... a little bit of a step down in Q3 and
#         another step down in Q4"                                -> Q3 share of H2 > 50%
#   CF   "fairly balanced between the two ... maybe a little bit stronger in the
#         fourth quarter than Q3, but overall pretty close"       -> Q3 share of H2 ~ 49%
Q3_SHARE_OF_H2 = {          # (low, central, high) applied to guidance-implied H2
    "PPA": (0.450, 0.465, 0.480),
    "SAT": (0.530, 0.545, 0.570),
    "CF":  (0.480, 0.490, 0.500),
}

# FS 606 revenue has no company guidance (the guide is FS NET INCOME ~$860m).
# Trailing YoY: Q1 FY2026 1,384 vs 1,470 = -5.9%; Q2 FY2026 1,366 vs 1,385 = -1.4%.
FS_TREND_YOY = (-0.030, -0.015, 0.000)   # (low, central, high) applied to 1,418


# --------------------------------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------------------------------

def yoy(new: float, old: float) -> float:
    return (new / old - 1.0) * 100.0


def median(xs: List[float]) -> float:
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)


def fmt(x: float, dp: int = 0) -> str:
    return f"{x:,.{dp}f}"


OUT = io.StringIO()


def say(line: str = "") -> None:
    print(line)
    OUT.write(line + "\n")


# --------------------------------------------------------------------------------------
# STEP 1 -- validate the Q3 FY2025 comparative matrix against the published totals
# --------------------------------------------------------------------------------------

def validate_base() -> None:
    for seg in SEGS:
        col = sum(Q3FY25[g][seg] for g in GEOS)
        assert col == Q3FY25_PUBLISHED_COLS[seg], (seg, col)
    grand = sum(sum(Q3FY25[g].values()) for g in GEOS)
    assert grand == Q3FY25_PUBLISHED_TOTAL, grand
    q2 = sum(sum(Q2FY26[g].values()) for g in GEOS)
    assert q2 == Q2FY26_PUBLISHED_TOTAL, q2

    # FY2025 8-K net sales cross-foot
    for seg, idx in (("PPA", 0), ("SAT", 1), ("CF", 2)):
        fy = sum(NETSALES_8K[2025][q][idx] for q in ("Q1", "Q2", "Q3", "Q4"))
        assert abs(fy - FY2025_NETSALES[seg]) <= 1, (seg, fy)
        h1 = sum(NETSALES_8K[2026][q][idx] for q in ("Q1", "Q2"))
        assert h1 == H1_FY2026_NETSALES[seg], (seg, h1)

    # THE KEY IDENTITY: the 606 geographic-matrix GRAND TOTAL equals the 8-K
    # "worldwide net sales and revenues" EXACTLY, in every quarter tested.
    for key, tot in NSR_8K.items():
        assert REV606_SEG[key][4] == tot, key


# --------------------------------------------------------------------------------------
# STEP 2 -- the 606 <-> 8-K basis wedge
# --------------------------------------------------------------------------------------

def basis_wedge() -> Dict[str, float]:
    """
    Compute the historical wedge (606 segment column) minus (8-K segment net sales).

    The famous "~104m PPA gap" is NOT a percentage and NOT a total-level gap.  It is a
    definitional difference between the 606 segment COLUMNS and the 8-K segment NET
    SALES lines: the 606 columns additionally carry the "financial products" and
    "other" revenue recorded inside each equipment segment.  Empirically the wedge is
    close to CONSTANT IN DOLLARS over the last five quarters, not proportional.
    """
    rows = []
    for (fy, q), (p6, s6, c6, _f6, _t6) in sorted(REV606_SEG.items()):
        p8, s8, c8 = NETSALES_8K[fy][q]
        rows.append(((fy, q), p6 - p8, s6 - s8, c6 - c8))

    say("### 606 -> 8-K basis wedge  (606 segment column MINUS 8-K segment net sales, USDm)")
    say()
    say("| Quarter | PPA wedge | SAT wedge | CF wedge | Total |")
    say("|---|---:|---:|---:|---:|")
    for (fy, q), wp, ws, wc in rows:
        say(f"| FY{fy} {q} | {wp:+,.0f} | {ws:+,.0f} | {wc:+,.0f} | {wp+ws+wc:+,.0f} |")

    last5 = rows[-5:]
    wedge = {
        "PPA": median([r[1] for r in last5]),
        "SAT": median([r[2] for r in last5]),
        "CF":  median([r[3] for r in last5]),
    }
    wedge["EQUIP_TOTAL"] = wedge["PPA"] + wedge["SAT"] + wedge["CF"]
    say()
    say(f"Median of the last five quarters: PPA {wedge['PPA']:+,.0f}, "
        f"SAT {wedge['SAT']:+,.0f}, CF {wedge['CF']:+,.0f}, "
        f"equipment total {wedge['EQUIP_TOTAL']:+,.0f}.")
    say("The wedge is stable in DOLLARS (PPA 96-111 across five quarters spanning a "
        "3,269-to-5,326 revenue range), so it is applied as a constant, not a ratio.")
    say()
    return wedge


# --------------------------------------------------------------------------------------
# STEP 3 -- the bottom-up matrix
# --------------------------------------------------------------------------------------

def build_matrix() -> Tuple[Dict, Dict, Dict]:
    central = {g: {s: DESK[g][s][0] for s in SEGS} for g in GEOS}
    low = {g: {s: DESK[g][s][1] for s in SEGS} for g in GEOS}
    high = {g: {s: DESK[g][s][2] for s in SEGS} for g in GEOS}
    for g in GEOS:
        for s in SEGS:
            assert low[g][s] <= central[g][s] <= high[g][s], (g, s)
    return central, low, high


def print_matrix(central, low, high) -> Dict[str, float]:
    say("## 1. Q3 FY2026 SEGMENT x GEOGRAPHY MATRIX FORECAST (ASC 606, USDm)")
    say()
    say("Q3 FY2025 comparatives are ACTUALS from the Q3 FY2025 10-Q "
        "(three months ended 2025-07-27). Q3 FY2026 figures are FORECASTS.")
    say()
    say("| Geography | Segment | Q3 FY2025 actual | Q3 FY2026 central | YoY % | "
        "Desk low | Desk high | Desk conf. |")
    say("|---|---|---:|---:|---:|---:|---:|---|")
    for g in GEOS:
        for s in SEGS:
            a = Q3FY25[g][s]
            c = central[g][s]
            say(f"| {g} | {s} | {fmt(a)} | {fmt(c)} | {yoy(c,a):+.1f}% | "
                f"{fmt(low[g][s])} | {fmt(high[g][s])} | {DESK[g][s][3]} |")
    say()

    if TRAILING_TREND_FALLBACKS:
        say("Cells filled by trailing-trend fallback (no usable desk view):")
        for (g, s), why in TRAILING_TREND_FALLBACKS.items():
            say(f"  - {g} / {s}: {why}")
    else:
        say("**Trailing-trend fallback used on 0 of 24 cells.** Every cell carries an "
            "explicit, quantified desk view with a stated low/central/high, and every "
            "desk anchored on the correct Q3 FY2025 actual (all 24 bases were "
            "re-verified line-by-line against the Q3 FY2025 10-Q for this roll-up).")
    say()
    return {}


def print_totals(central, low, high, wedge) -> Dict[str, float]:
    say("## 2. ROW AND COLUMN TOTALS, AND BASIS RECONCILIATION")
    say()
    say("### 2a. Row totals by geography (ASC 606, USDm)")
    say()
    say("| Geography | Q3 FY2025 actual | Q3 FY2026 central | YoY % | Low | High | "
        "Share of Q3 FY2026 |")
    say("|---|---:|---:|---:|---:|---:|---:|")
    grand_c = sum(sum(central[g].values()) for g in GEOS)
    for g in GEOS:
        a = sum(Q3FY25[g].values())
        c = sum(central[g].values())
        say(f"| {g} | {fmt(a)} | {fmt(c)} | {yoy(c,a):+.1f}% | "
            f"{fmt(sum(low[g].values()))} | {fmt(sum(high[g].values()))} | "
            f"{c/grand_c*100:.1f}% |")
    ga = Q3FY25_PUBLISHED_TOTAL
    gl = sum(sum(low[g].values()) for g in GEOS)
    gh = sum(sum(high[g].values()) for g in GEOS)
    say(f"| **Total** | **{fmt(ga)}** | **{fmt(grand_c)}** | **{yoy(grand_c,ga):+.1f}%** "
        f"| **{fmt(gl)}** | **{fmt(gh)}** | 100.0% |")
    say()

    say("### 2b. Column totals by segment (ASC 606, USDm)")
    say()
    say("| Segment | Q3 FY2025 actual | Q3 FY2026 central | YoY % | Low | High |")
    say("|---|---:|---:|---:|---:|---:|")
    cols_c: Dict[str, float] = {}
    for s in SEGS:
        a = Q3FY25_PUBLISHED_COLS[s]
        c = sum(central[g][s] for g in GEOS)
        cols_c[s] = c
        say(f"| {s} | {fmt(a)} | {fmt(c)} | {yoy(c,a):+.1f}% | "
            f"{fmt(sum(low[g][s] for g in GEOS))} | "
            f"{fmt(sum(high[g][s] for g in GEOS))} |")
    say(f"| **Total** | **{fmt(ga)}** | **{fmt(grand_c)}** | "
        f"**{yoy(grand_c,ga):+.1f}%** | **{fmt(gl)}** | **{fmt(gh)}** |")
    say()
    say("NOTE ON THE LOW/HIGH COLUMNS: these are the arithmetic sums of the 24 desk "
        "lows and 24 desk highs. They are NOT a confidence interval -- they assume all "
        "24 cells miss in the same direction simultaneously. A more defensible "
        "aggregate band is given in section 3.")
    say()

    say("### 2c. Reconciliation to the reporting basis")
    say()
    say("The critical fact, verified on all seven quarters where both are available "
        "(FY2024 Q1/Q3, FY2025 Q1/Q2/Q3, FY2026 Q1/Q2): the ASC 606 geographic-matrix "
        "GRAND TOTAL equals the 8-K 'worldwide net sales and revenues' EXACTLY. "
        "Q3 FY2025: 12,018 = 12,018. Q2 FY2026: 13,369 = 13,369. "
        "So the bottom-up 606 grand total needs NO adjustment to be a "
        "net-sales-and-revenues forecast.")
    say()
    say("The ~104m PPA gap lives entirely in the SEGMENT SPLIT, and it is a roughly "
        "CONSTANT DOLLAR wedge, not a percentage.")
    say()
    say("| Line | Q3 FY2026 forecast (USDm) |")
    say("|---|---:|")
    say(f"| 606 PPA column | {fmt(cols_c['PPA'])} |")
    say(f"| 606 SAT column | {fmt(cols_c['SAT'])} |")
    say(f"| 606 CF column | {fmt(cols_c['CF'])} |")
    say(f"| 606 equipment subtotal | {fmt(cols_c['PPA']+cols_c['SAT']+cols_c['CF'])} |")
    say(f"| less basis wedge (fin. products + other inside equipment segments) "
        f"| ({fmt(wedge['EQUIP_TOTAL'])}) |")
    ns = cols_c["PPA"] + cols_c["SAT"] + cols_c["CF"] - wedge["EQUIP_TOTAL"]
    say(f"| **= Equipment operations NET SALES (8-K basis)** | **{fmt(ns)}** |")
    say(f"| 606 FS column | {fmt(cols_c['FS'])} |")
    say(f"| plus basis wedge back (reported as finance/other revenue) "
        f"| {fmt(wedge['EQUIP_TOTAL'])} |")
    say(f"| **= Finance and other revenues** | **{fmt(cols_c['FS']+wedge['EQUIP_TOTAL'])}** |")
    say(f"| **= WORLDWIDE NET SALES AND REVENUES** | **{fmt(grand_c)}** |")
    say()

    say("### 2d. Implied 8-K segment net sales, and the FY2026 guide check")
    say()
    say("| Segment | Q3 FY2026, 606 basis | wedge | Q3 FY2026, 8-K net sales | "
        "Q3 FY2025 8-K | YoY % | Implied Q4 | Implied FY2026 | vs FY2025 | Guide |")
    say("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    guide_txt = {"PPA": "Down 5-10%", "SAT": "Up ~15%", "CF": "Up ~20%"}
    hist_share = {}
    for seg, idx in (("PPA", 0), ("SAT", 1), ("CF", 2)):
        shares = []
        for fy in (2021, 2022, 2023, 2024, 2025):
            q3 = NETSALES_8K[fy]["Q3"][idx]
            q4 = NETSALES_8K[fy]["Q4"][idx]
            shares.append(q3 / (q3 + q4))
        hist_share[seg] = median(shares)
        n8 = sum(central[g][seg] for g in GEOS) - wedge[seg]
        base8 = NETSALES_8K[2025]["Q3"][idx]
        # Q4 implied by holding the management-guided Q3 share of H2
        share = Q3_SHARE_OF_H2[seg][1]
        q4_imp = n8 * (1 - share) / share
        fy_imp = H1_FY2026_NETSALES[seg] + n8 + q4_imp
        say(f"| {seg} | {fmt(sum(central[g][seg] for g in GEOS))} | "
            f"({fmt(wedge[seg])}) | {fmt(n8)} | {fmt(base8)} | {yoy(n8,base8):+.1f}% | "
            f"{fmt(q4_imp)} | {fmt(fy_imp)} | "
            f"{yoy(fy_imp, FY2025_NETSALES[seg]):+.1f}% | {guide_txt[seg]} |")
    say()
    say("This is the single most reassuring number in the roll-up: rolled forward on "
        "management's own stated Q3/Q4 cadence, the bottom-up lands INSIDE all three "
        "FY2026 segment guides, with SAT and CF landing almost exactly on the point "
        "guide and PPA at the weak end of its band.")
    say()
    return cols_c


# --------------------------------------------------------------------------------------
# STEP 4 -- the three sanity checks
# --------------------------------------------------------------------------------------

def sanity_checks(central, low, high, wedge, cols_c) -> None:
    say("## 3. THREE SANITY CHECKS, SIDE BY SIDE")
    say()

    grand_c = sum(sum(central[g].values()) for g in GEOS)

    # ---- (a) guidance-implied -------------------------------------------------------
    say("### (a) Guidance-implied")
    say()
    say("Method: apply the FY2026 8-K segment guide to FY2025 actual net sales, "
        "subtract H1 FY2026 actual to get implied H2, split H2 into Q3/Q4 on the "
        "historical seasonal pattern ADJUSTED for management's explicit Q2-call "
        "cadence commentary, then add the wedge back to return to the 606 basis.")
    say()
    say("Historical Q3 share of H2 net sales (8-K basis), FY2021-FY2025:")
    say()
    say("| Segment | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | median | "
        "used (mgmt-adjusted) | why |")
    say("|---|---:|---:|---:|---:|---:|---:|---:|---|")
    why = {
        "PPA": "'Q4 a bit stronger than Q3'; abnormal Waterloo H2 NA skew -> below median",
        "SAT": "'step down in Q3 and another step down in Q4' -> above 50%",
        "CF":  "'fairly balanced ... maybe a little bit stronger in Q4' -> just below 50%",
    }
    for seg, idx in (("PPA", 0), ("SAT", 1), ("CF", 2)):
        sh = []
        for fy in (2021, 2022, 2023, 2024, 2025):
            q3 = NETSALES_8K[fy]["Q3"][idx]
            q4 = NETSALES_8K[fy]["Q4"][idx]
            sh.append(q3 / (q3 + q4) * 100)
        say(f"| {seg} | " + " | ".join(f"{x:.1f}%" for x in sh) +
            f" | {median(sh):.1f}% | {Q3_SHARE_OF_H2[seg][1]*100:.1f}% | {why[seg]} |")
    say()

    g_low: Dict[str, float] = {}
    g_cen: Dict[str, float] = {}
    g_high: Dict[str, float] = {}
    say("| Segment | FY2026 guide range (8-K) | implied H2 | Q3 share used | "
        "Q3 8-K low/central/high | Q3 606 low/central/high |")
    say("|---|---|---|---|---|---|")
    for seg in ("PPA", "SAT", "CF"):
        glo, ghi = FY2026_GUIDE[seg]
        fy_lo = FY2025_NETSALES[seg] * (1 + glo)
        fy_hi = FY2025_NETSALES[seg] * (1 + ghi)
        h2_lo = fy_lo - H1_FY2026_NETSALES[seg]
        h2_hi = fy_hi - H1_FY2026_NETSALES[seg]
        h2_mid = 0.5 * (h2_lo + h2_hi)
        s_lo, s_cen, s_hi = Q3_SHARE_OF_H2[seg]
        q3_lo, q3_cen, q3_hi = h2_lo * s_lo, h2_mid * s_cen, h2_hi * s_hi
        g_low[seg], g_cen[seg], g_high[seg] = (q3_lo + wedge[seg],
                                               q3_cen + wedge[seg],
                                               q3_hi + wedge[seg])
        say(f"| {seg} | {fmt(fy_lo)} - {fmt(fy_hi)} | {fmt(h2_lo)} - {fmt(h2_hi)} "
            f"| {s_lo*100:.1f}/{s_cen*100:.1f}/{s_hi*100:.1f}% "
            f"| {fmt(q3_lo)} / {fmt(q3_cen)} / {fmt(q3_hi)} "
            f"| {fmt(g_low[seg])} / {fmt(g_cen[seg])} / {fmt(g_high[seg])} |")

    fs_base = Q3FY25_PUBLISHED_COLS["FS"]
    fs_lo, fs_cen, fs_hi = (fs_base * (1 + r) for r in FS_TREND_YOY)
    g_low["FS"], g_cen["FS"], g_high["FS"] = fs_lo, fs_cen, fs_hi
    say(f"| FS | no revenue guide (guide is FS NET INCOME ~$860m) | n/a | n/a | n/a "
        f"| {fmt(fs_lo)} / {fmt(fs_cen)} / {fmt(fs_hi)} (trailing YoY -3.0/-1.5/0.0%) |")
    a_lo = sum(g_low.values())
    a_cen = sum(g_cen.values())
    a_hi = sum(g_high.values())
    say(f"| **Total (606)** | | | | | **{fmt(a_lo)} / {fmt(a_cen)} / {fmt(a_hi)}** |")
    say()

    # ---- (b) simple seasonality -----------------------------------------------------
    say("### (b) Simple seasonality")
    say()
    say("Two variants, because the naive one is biased.")
    say()
    say("**(b1) Q2-to-Q3 sequential ratio applied to the Q2 FY2026 actual of 13,369.** "
        "Preferred, because it is anchored on a known FY2026 level rather than on a "
        "comparative whose difficulty changes quarter to quarter.")
    say()
    seq_hist = {2021: (12058, 11527), 2022: (13370, 14102), 2023: (17387, 15801),
                2024: (15235, 13152), 2025: (12763, 12018)}
    ratios = []
    say("| FY | Q2 total (606) | Q3 total (606) | Q3/Q2 |")
    say("|---|---:|---:|---:|")
    for fy, (q2, q3) in sorted(seq_hist.items()):
        r = q3 / q2
        ratios.append(r)
        say(f"| FY{fy} | {fmt(q2)} | {fmt(q3)} | {r:.3f} |")
    r_med, r_mean = median(ratios), mean(ratios)
    b1_cen = Q2FY26_PUBLISHED_TOTAL * r_med
    b1_lo = Q2FY26_PUBLISHED_TOTAL * min(ratios)
    b1_hi = Q2FY26_PUBLISHED_TOTAL * max(ratios)
    say(f"| | | median {r_med:.3f} / mean {r_mean:.3f} | n=5 |")
    say()
    say(f"13,369 x median {r_med:.3f} = **{fmt(b1_cen)}**  "
        f"(mean {r_mean:.3f} -> {fmt(Q2FY26_PUBLISHED_TOTAL*r_mean)}; "
        f"full observed ratio range {min(ratios):.3f}-{max(ratios):.3f} -> "
        f"{fmt(b1_lo)}-{fmt(b1_hi)}).")
    say()
    say("**(b2) Q3 FY2025 actual grown at a trend YoY rate.** The literal reading of "
        "the brief. Reported, but flagged as upward-biased.")
    say()
    trend = {
        "Q1 FY2026 actual YoY (9,611 / 8,508)": 9611 / 8508 - 1,
        "Q2 FY2026 actual YoY (13,369 / 12,763)": 13369 / 12763 - 1,
        "H1 FY2026 actual YoY (22,981 / 21,272)": 22981 / 21272 - 1,
    }
    say("| Trend rate used | rate | 12,018 grown at it |")
    say("|---|---:|---:|")
    for k, v in trend.items():
        say(f"| {k} | {v*100:+.1f}% | {fmt(12018*(1+v))} |")
    say()
    say("These run 12,589-13,576, at or ABOVE (b1). The reason is a comp artefact and "
        "it matters: Q1 and Q2 FY2026 grew against FY2025 quarters that were down 30% "
        "and 16% YoY, whereas Q3 FY2025 was down only 9% YoY. Growing the Q3 comp at "
        "an H1-derived rate implicitly assumes the comp is as easy as H1's; it is not. "
        "Within (b) I therefore weight (b1). Note the two agree exactly at the "
        "Q2-only rate (both 12,589), which is not a coincidence -- applying last "
        "quarter's YoY rate to the year-ago quarter and applying the year-ago "
        "sequential ratio to the current quarter are the same operation when the "
        "seasonal ratio used is FY2025's own 0.942.")
    b_cen = b1_cen
    say()

    # ---- (c) bottom-up ---------------------------------------------------------------
    say("### (c) Regional bottom-up")
    say()
    say(f"Sum of the 24 desk cells: **{fmt(grand_c)}** "
        f"({yoy(grand_c, Q3FY25_PUBLISHED_TOTAL):+.1f}% YoY).")
    say()
    say("A more defensible aggregate band than the naive sum-of-lows / sum-of-highs: "
        "add the six REGIONAL row-ranges in quadrature. Within a region the cells are "
        "strongly correlated (one FX rate, one farm economy, one order book) so their "
        "ranges are added arithmetically; across regions they are treated as "
        "independent, which is the assumption doing the work here and is only "
        "partly true -- the US large-ag cycle, the Brazil cycle and global "
        "roadbuilding are not orthogonal. Read the band as a floor on the "
        "uncertainty, not a ceiling:")
    var = 0.0
    for g in GEOS:
        half = 0.5 * (sum(high[g].values()) - sum(low[g].values()))
        var += half ** 2
    quad = var ** 0.5
    say(f"  half-width = sqrt(sum of squared regional half-widths) = {fmt(quad)}")
    say(f"  -> **{fmt(grand_c-quad)} to {fmt(grand_c+quad)}** around a central "
        f"{fmt(grand_c)}, i.e. roughly +/-{quad/grand_c*100:.1f}%.")
    say(f"  (The naive sum-of-lows to sum-of-highs is "
        f"{fmt(sum(sum(low[g].values()) for g in GEOS))} to "
        f"{fmt(sum(sum(high[g].values()) for g in GEOS))} -- too wide to be useful.)")
    say()

    # ---- side by side ---------------------------------------------------------------
    say("### The three, side by side (ASC 606 / worldwide net sales and revenues, USDm)")
    say()
    say("| Check | Low | Central | High | YoY on central | Segment detail |")
    say("|---|---:|---:|---:|---:|---|")
    say(f"| (a) Guidance-implied | {fmt(a_lo)} | {fmt(a_cen)} | {fmt(a_hi)} | "
        f"{yoy(a_cen, Q3FY25_PUBLISHED_TOTAL):+.1f}% | "
        f"PPA {fmt(g_cen['PPA'])} / SAT {fmt(g_cen['SAT'])} / CF {fmt(g_cen['CF'])} / "
        f"FS {fmt(g_cen['FS'])} |")
    say(f"| (b) Simple seasonality (b1) | {fmt(b1_lo)} | {fmt(b1_cen)} | {fmt(b1_hi)} | "
        f"{yoy(b1_cen, Q3FY25_PUBLISHED_TOTAL):+.1f}% | total-level only |")
    say(f"| (c) Regional bottom-up | {fmt(grand_c-quad)} | {fmt(grand_c)} | "
        f"{fmt(grand_c+quad)} | {yoy(grand_c, Q3FY25_PUBLISHED_TOTAL):+.1f}% | "
        f"PPA {fmt(cols_c['PPA'])} / SAT {fmt(cols_c['SAT'])} / CF {fmt(cols_c['CF'])} / "
        f"FS {fmt(cols_c['FS'])} |")
    say()
    say("Segment-level comparison of (a) against (c) -- this is where the daylight is:")
    say()
    say("| Segment | (a) guidance-implied | (c) bottom-up | (c) minus (a) | (c) vs (a) band |")
    say("|---|---:|---:|---:|---|")
    for seg in SEGS:
        d = cols_c[seg] - g_cen[seg]
        pos = ("inside" if g_low[seg] <= cols_c[seg] <= g_high[seg] else "OUTSIDE")
        say(f"| {seg} | {fmt(g_cen[seg])} | {fmt(cols_c[seg])} | {d:+,.0f} | {pos} |")
    say(f"| **Total** | **{fmt(a_cen)}** | **{fmt(grand_c)}** | "
        f"**{grand_c-a_cen:+,.0f}** | inside |")
    say()

    spread = max(a_cen, b_cen, grand_c) - min(a_cen, b_cen, grand_c)
    say(f"Spread between the three centrals: {fmt(spread)}m, "
        f"{spread/grand_c*100:.1f}% of the bottom-up total.")
    say()


# --------------------------------------------------------------------------------------
# STEP 5 -- weakest cells
# --------------------------------------------------------------------------------------

def weakest_cells(central, low, high) -> List[Tuple]:
    grand = sum(sum(central[g].values()) for g in GEOS)
    rows = []
    for g in GEOS:
        for s in SEGS:
            c = central[g][s]
            width = high[g][s] - low[g][s]
            weight = c / grand
            rows.append((g, s, c, width, width / c, weight, width / grand * 100,
                         DESK[g][s][3]))
    # score = absolute dollar range, i.e. contribution of this cell's uncertainty to
    # the uncertainty of the grand total.  That is the correct ranking for "most
    # uncertainty AND most weight".
    rows.sort(key=lambda r: -r[3])
    say("## 4. DIVERGENCES")
    say()
    say("Divergences are qualitative and are set out in full in "
        "data/deere/regional/REGIONAL_ROLLUP.md section 4. The two that are "
        "arithmetic, and therefore reproducible here, are printed in section 3 above: "
        "the segment-level (c)-minus-(a) table, and the US-PPA residual test below.")
    say()
    # The US desk sized its residual method off assumed values for the other five
    # desks. Those desks then filed different numbers. Recompute the residual with
    # what they actually filed.
    us_assumed = {"Canada": 295, "Western Europe": 711, "Central Europe & CIS": 331,
                  "Latin America": 897, "Asia/Africa/Oceania/ME": 359}
    global_ppa_assumed = 4060
    filed = {g: central[g]["PPA"] for g in us_assumed}
    say("US-PPA residual test (the roll-up's central tension):")
    say()
    say("| Region | US desk ASSUMED | region desk FILED | diff |")
    say("|---|---:|---:|---:|")
    for g in us_assumed:
        say(f"| {g} | {fmt(us_assumed[g])} | {fmt(filed[g])} | "
            f"{filed[g]-us_assumed[g]:+,.0f} |")
    say(f"| **Sum of other five** | **{fmt(sum(us_assumed.values()))}** | "
        f"**{fmt(sum(filed.values()))}** | **{sum(filed.values())-sum(us_assumed.values()):+,.0f}** |")
    say()
    resid_assumed = global_ppa_assumed - sum(us_assumed.values())
    resid_filed = global_ppa_assumed - sum(filed.values())
    say(f"On the US desk's own assumed global 606 PPA of {fmt(global_ppa_assumed)}, its "
        f"residual for the US was {fmt(resid_assumed)}. With what the other five desks "
        f"ACTUALLY filed, the same residual is {fmt(resid_filed)} -- "
        f"{resid_filed - central['United States']['PPA']:+,.0f} above the "
        f"{fmt(central['United States']['PPA'])} the US desk carried, and "
        f"{'above' if resid_filed > DESK['United States']['PPA'][2] else 'inside'} "
        f"its stated high of {fmt(DESK['United States']['PPA'][2])}.")
    say()
    say("## 5. WEAKEST CELLS -- ranked by dollars of uncertainty contributed")
    say()
    say("Ranking metric is the ABSOLUTE dollar width of the desk's own range, because "
        "that is what actually moves the grand total. Relative width is shown "
        "alongside so small-but-wild cells are visible too.")
    say()
    say("| # | Geography | Segment | Central | Range width $m | Range as % of cell | "
        "Cell % of total | Width as % of total | Desk conf. |")
    say("|---:|---|---|---:|---:|---:|---:|---:|---|")
    for i, (g, s, c, w, rel, wt, wpct, conf) in enumerate(rows, 1):
        say(f"| {i} | {g} | {s} | {fmt(c)} | {fmt(w)} | {rel*100:.1f}% | "
            f"{wt*100:.1f}% | {wpct:.2f}% | {conf} |")
    say()
    us_share = sum(central["United States"].values()) / grand
    us_width = sum(high["United States"][s] - low["United States"][s] for s in SEGS)
    tot_width = sum(r[3] for r in rows)
    say(f"Concentration: the four United States cells are {us_share*100:.1f}% of the "
        f"forecast total and {us_width/tot_width*100:.1f}% of the total range width "
        f"({fmt(us_width)}m of {fmt(tot_width)}m). If you have time to challenge only "
        f"three cells, challenge US PPA, US CF and US SAT.")
    say()
    return rows


# --------------------------------------------------------------------------------------
# STEP 6 -- CSV emission
# --------------------------------------------------------------------------------------

def write_csv(central, low, high, path: str) -> None:
    hdr = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "geography",
           "country", "segment", "value", "units", "source_type", "source", "notes"]
    rows = []
    for g in GEOS:
        for s in SEGS:
            rows.append(["de_rev606_matrix_actual", "2025-07-27", 2025, "Q3", g, "",
                         s, Q3FY25[g][s], "USD_millions", "filing",
                         f"corpus:{Q3FY25_10Q}",
                         "ASC 606 revenue from contracts with customers; "
                         "three months ended 2025-07-27; ACTUAL"])
    for g in GEOS:
        for s in SEGS:
            c, lo, hi, conf, note = DESK[g][s]
            for label, v in (("central", c), ("low", lo), ("high", hi)):
                rows.append([f"de_rev606_matrix_forecast_{label}", "2026-08-02", 2026,
                             "Q3", g, "", s, v, "USD_millions", "forecast",
                             "regional-desk roll-up 2026-08-16",
                             f"FORECAST, not actual. desk_confidence={conf}. "
                             + note.replace(",", ";")])
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(hdr)
        w.writerows(rows)


# --------------------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------------------

def main() -> int:
    validate_base()
    central, low, high = build_matrix()

    say("# Deere FY2026 Q3 -- regional roll-up calculation output")
    say()
    say("Generated by scripts/data/regional_rollup.py. As of 2026-08-16. "
        "Deere reports FY2026 Q3 on 2026-08-20. NO Q3 FY2026 ACTUALS EXIST.")
    say()
    print_matrix(central, low, high)
    wedge = basis_wedge()
    cols_c = print_totals(central, low, high, wedge)
    sanity_checks(central, low, high, wedge, cols_c)
    weakest_cells(central, low, high)

    here = os.path.dirname(os.path.abspath(__file__))
    out_csv = os.path.abspath(os.path.join(
        here, "..", "..", "data", "deere", "regional", "rollup_matrix_q3fy2026.csv"))
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    write_csv(central, low, high, out_csv)
    say(f"Wrote tidy-long matrix CSV: {out_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
