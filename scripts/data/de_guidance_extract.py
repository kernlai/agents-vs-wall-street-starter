#!/usr/bin/env python3
"""Extract Deere & Company forward guidance from the frozen offline corpus.

Scripted extraction only -- every number in the output CSV is parsed out of a
corpus document by regex, never transcribed by hand.

Outputs (written by de_build_guidance.py, which imports this module):
  de_guidance.csv            tidy-long guidance panel
  de_guidance_vs_actual.csv  guidance vintage paired with the eventual actual

Corpus: challenge/offline-data/deere (310 docs, frozen 2026-08-14)
"""
import os
import re

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"

# ---------------------------------------------------------------- fiscal calendar
# Deere fiscal-year end dates. FY2012-FY2025 confirmed against SEC XBRL
# (CIK 315189) annual NetIncomeLoss period ends. FY2026 is projected from the
# FY2026 Q1/Q2 period ends (2026-02-01, 2026-05-03) on a 13-week cadence.
FY_END = {
    2012: "2012-10-31", 2013: "2013-10-31", 2014: "2014-10-31", 2015: "2015-11-01",
    2016: "2016-10-30", 2017: "2017-10-29", 2018: "2018-10-28", 2019: "2019-11-03",
    2020: "2020-11-01", 2021: "2021-10-31", 2022: "2022-10-30", 2023: "2023-10-29",
    2024: "2024-10-27", 2025: "2025-11-02", 2026: "2026-11-01",
}
FY2026_END_IS_ESTIMATE = True

# ---------------------------------------------------------------- guidance events
# (issue_date, release_fq, target_fy, primary_source, slide_source)
# release_fq = the fiscal quarter whose earnings release carried the guidance.
# A Q4 release carries the FIRST guidance for the NEXT fiscal year.
EVENTS = [
    # FY2012 (partial - corpus starts 2012-05-16)
    ("2012-05-16", "Q2", 2012, "call-transcripts/2012-05-16__de-us-20120516-call-pres__1534116.md", None),
    ("2012-08-15", "Q3", 2012, "call-transcripts/2012-08-15__de-us-20120815-call-pres__1533564.md", None),
    # FY2013
    ("2012-11-21", "Q4", 2013, "call-transcripts/2012-11-21__de-us-20121121-call-pres__1532984.md", None),
    ("2013-02-13", "Q1", 2013, "call-transcripts/2013-02-13__de-us-20130213-call-pres__1532730.md", None),
    ("2013-05-15", "Q2", 2013, "call-transcripts/2013-05-15__de-us-20130515-call-pres__1530346.md", None),
    ("2013-08-14", "Q3", 2013, "call-transcripts/2013-08-14__de-us-20130814-call-pres__1529031.md", None),
    # FY2014
    ("2013-11-20", "Q4", 2014, "call-transcripts/2013-11-20__de-us-20131120-call-pres__1527987.md", None),
    ("2014-02-12", "Q1", 2014, "call-transcripts/2014-02-12__de-us-20140212-call-pres__1527290.md", None),
    ("2014-05-14", "Q2", 2014, "call-transcripts/2014-05-14__de-us-20140514-call-pres__1526775.md", None),
    ("2014-08-13", "Q3", 2014, "call-transcripts/2014-08-13__de-us-20140813-call-pres__1524329.md", None),
    # FY2015
    ("2014-11-26", "Q4", 2015, "call-transcripts/2014-11-26__de-us-20141126-call-pres__1523103.md", None),
    ("2015-02-20", "Q1", 2015, "filings/2015-02-20__de-us-20150220-q1-8k__784661.md", None),
    ("2015-05-22", "Q2", 2015, "filings/2015-05-22__de-us-20150522-q2-8k__784603.md", None),
    ("2015-08-21", "Q3", 2015, "filings/2015-08-21__de-us-20150821-q3-8k__784604.md", None),
    # FY2016
    ("2015-11-25", "Q4", 2016, "filings/2015-11-25__de-us-20151125-q4-8k__784605.md", None),
    ("2016-02-19", "Q1", 2016, "filings/2016-02-19__de-us-20160219-q1-8k__784606.md", None),
    ("2016-05-20", "Q2", 2016, "filings/2016-05-20__de-us-20160520-q2-8k__784653.md", None),
    ("2016-08-19", "Q3", 2016, "filings/2016-08-19__de-us-20160819-q3-8k__784652.md", None),
    # FY2017
    ("2016-11-23", "Q4", 2017, "filings/2016-11-23__de-us-20161123-q4-8k__784650.md", None),
    ("2017-02-17", "Q1", 2017, "filings/2017-02-17__de-us-20170217-q1-8k__784623.md", None),
    ("2017-05-19", "Q2", 2017, "filings/2017-05-19__de-us-20170519-q2-8k__784651.md", None),
    ("2017-08-18", "Q3", 2017, "filings/2017-08-18__de-us-20170818-q3-8k__784624.md", None),
    # FY2018
    ("2017-11-22", "Q4", 2018, "filings/2017-11-22__de-us-20171122-fy-8k__784662.md", None),
    ("2018-02-16", "Q1", 2018, "filings/2018-02-16__de-us-20180216-q1-8k__784666.md", None),
    ("2018-05-18", "Q2", 2018, "filings/2018-05-18__de-us-20180518-q2-8k__784663.md", None),
    ("2018-08-17", "Q3", 2018, "filings/2018-08-17__de-us-20180817-q3-8k__784667.md", None),
    # FY2019
    ("2018-11-21", "Q4", 2019, "filings/2018-11-21__de-us-20181121-fy-8k__654629.md", None),
    ("2019-02-15", "Q1", 2019, "filings/2019-02-15__de-us-20190215-q1-8k__654630.md", None),
    ("2019-05-17", "Q2", 2019, "filings/2019-05-17__de-us-20190517-q2-8k__645299.md", None),
    ("2019-08-16", "Q3", 2019, "filings/2019-08-16__de-us-20190816-q3-8k__645300.md", None),
    # FY2020
    ("2019-11-27", "Q4", 2020, "filings/2019-11-27__de-us-20191127-q4-8k__469218.md", None),
    ("2020-02-21", "Q1", 2020, "filings/2020-02-21__de-us-20200221-q1-8k__469227.md", None),
    ("2020-05-21", "Q2", 2020, "filings/2020-05-21__de-us-20200521-q2-8k__469475.md", None),
    ("2020-08-20", "Q3", 2020, "filings/2020-08-20__de-us-20200820-q3-8k__105830.md", None),
    # FY2021  (first year on the modern PPA / SAT / CF segment basis)
    ("2020-11-25", "Q4", 2021, "filings/2020-11-25__de-us-20201125-q4-8k__105817.md", None),
    ("2021-02-19", "Q1", 2021, "filings/2021-02-19__de-us-20210219-q1-8k__105842.md", None),
    ("2021-05-21", "Q2", 2021, "filings/2021-05-21__de-us-20210521-q2-8k__105846.md", None),
    ("2021-08-20", "Q3", 2021, "filings/2021-08-20__de-us-20210820-q3-8k__105827.md", None),
    # FY2022
    ("2021-11-24", "Q4", 2022, "filings/2021-11-24__de-us-20211124-q4-8k__105843.md", None),
    ("2022-02-18", "Q1", 2022, "filings/2022-02-18__de-us-20220218-q1-8k__105812.md", None),
    ("2022-05-20", "Q2", 2022, "filings/2022-05-20__de-us-20220520-q2-8k__105815.md", None),
    ("2022-08-19", "Q3", 2022, "filings/2022-08-19__de-us-20220819-q3-8k__105811.md", None),
    # FY2023
    ("2022-11-23", "Q4", 2023, "filings/2022-11-23__de-us-20221123-q4-8k__105825.md", None),
    ("2023-02-17", "Q1", 2023, "filings/2023-02-17__de-us-20230217-q1-8k__105833.md", None),
    ("2023-05-19", "Q2", 2023, "filings/2023-05-19__de-us-20230519-q2-8k__105839.md", None),
    ("2023-08-18", "Q3", 2023, "filings/2023-08-18__de-us-20230818-q3-8k__105829.md", None),
    # FY2024
    ("2023-11-22", "Q4", 2024, "filings/2023-11-22__de-us-20231122-q4-8k__105823.md", None),
    ("2024-02-15", "Q1", 2024, "filings/2024-02-15__de-us-20240215-q1-8k__105824.md", None),
    ("2024-05-16", "Q2", 2024, "filings/2024-05-16__de-us-20240516-q2-8k__105819.md", None),
    ("2024-08-15", "Q3", 2024, "filings/2024-08-15__de-us-20240815-q3-8k__105836.md", None),
    # FY2025
    ("2024-11-21", "Q4", 2025, "filings/2024-11-21__de-us-20241121-q4-8k__105840.md", None),
    ("2025-02-13", "Q1", 2025, "filings/2025-02-13__de-us-20250213-q1-8k__105841.md", None),
    ("2025-05-15", "Q2", 2025, "filings/2025-05-15__de-us-20250515-q2-8k__105808.md", None),
    ("2025-08-15", "Q3", 2025, "filings/2025-08-15__de-us-20250815-q3-8k__143410.md", None),
    # FY2026 (in progress -- Q3 FY2026 has NOT been reported as of 2026-08-16)
    ("2025-11-26", "Q4", 2026, "filings/2025-11-26__de-us-20251126-q4-8k__361233.md", None),
    ("2026-02-19", "Q1", 2026, "filings/2026-02-19__de-us-20260219-q1-8k__603009.md", None),
    ("2026-05-21", "Q2", 2026, "filings/2026-05-21__de-us-20260521-q2-8k-2__1042168.md", None),
]


def docs_for(issue_date, kinds=("q1-10q", "q2-10q", "q3-10q", "q4-10k", "fy-10k")):
    """All filing docs published on a date whose filename matches one of `kinds`."""
    d = os.path.join(CORPUS, "filings")
    return ["filings/" + f for f in sorted(os.listdir(d))
            if f.startswith(issue_date) and any(k in f for k in kinds)]


def transcript_for(issue_date):
    """The prepared-remarks ('call-pres') transcript published on a date."""
    d = os.path.join(CORPUS, "call-transcripts")
    cands = [f for f in sorted(os.listdir(d)) if f.startswith(issue_date) and "pres" in f]
    return "call-transcripts/" + cands[0] if cands else None


def transcripts_for(issue_date):
    d = os.path.join(CORPUS, "call-transcripts")
    return ["call-transcripts/" + f for f in sorted(os.listdir(d)) if f.startswith(issue_date)]


def slide_for(issue_date):
    """Resolve the earnings-call slide deck published on a given date."""
    d = os.path.join(CORPUS, "slides")
    for fn in sorted(os.listdir(d)):
        if fn.startswith(issue_date):
            return "slides/" + fn
    return None


def read(rel):
    with open(os.path.join(CORPUS, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read().replace("&amp;", "&").replace("’", "'").replace("–", "-")


def flat(rel):
    return " ".join(read(rel).split())


# ---------------------------------------------------------------- number helpers
def bn(x):
    """'$4.5 billion' style token -> USD millions."""
    return round(float(x) * 1000.0, 1)


# ---------------------------------------------------------------- net income guidance
RANGE_PATS = [
    # "...for fiscal 2026 is forecasted to be in a range of $4.00 billion to $4.75 billion"
    r"net income attributable to Deere & Company(?: for fiscal (?:19|20)\d\d)? is forecast(?:ed)? to (?:be |remain )?in a range of \$\s?([\d.]+) billion to \$\s?([\d.]+) billion",
    r"net income attributable to Deere & Company is forecast to be in a range of \$\s?([\d.]+) billion to \$\s?([\d.]+) billion",
]
POINT_PATS = [
    r"net income attributable to Deere & Company(?: for fiscal (?:19|20)\d\d)? is forecast(?:ed)? to be (?:about|approximately) \$\s?([\d.]+) billion",
    r"net income attributable to Deere & Company is (?:anticipated|forecast|forecasted|expected) to be (?:about|approximately) \$\s?([\d.]+) billion",
    r"net income attributable to Deere & Company (?:of|forecast to be) about \$\s?([\d.]+) billion",
    r"net income attributable to Deere & Company is forecast to be about \$\s?([\d.]+) billion",
    # transcript wording, e.g. "our full year 2014 net income forecast is about $3.3 billion"
    r"full[ -]year(?: 20\d\d)? net income (?:forecast|is now forecast)[^.$]{0,60}\$\s?([\d.]+) billion",
    r"(?:20\d\d )?full year net income forecast[^.$]{0,40}\$\s?([\d.]+) billion",
    r"net income attributable to Deere & Company to be about \$\s?([\d.]+) billion for the full year",
]
ADJ_PATS = [
    r"[Aa]djusted net income (?:attributable to Deere & Company[, ]*)?(?:which excludes[^.]{0,90}, )?is forecast(?:ed)? to be (?:about )?\$\s?([\d.]+) billion",
    r"adjusted net income without the impact of the tax-reform adjustments is expected to be about \$\s?([\d.]+) billion",
]
FS_PATS = [
    r"[Ff]iscal[- ]year (?:19|20)\d\d net income attributable to Deere & Company for the financial services operations is (?:expected|forecast|forecasted) to be (?:approximately |about )?\$\s?([\d,]+) million",
    r"net income attributable to Deere & Company for the financial services operations is forecast(?:ed)? to be (?:approximately |about )?\$\s?([\d,]+) million",
    r"[Ff]iscal-year (?:19|20)\d\d net income attributable to Deere & Company for the financial services operations is forecast to be \$\s?([\d,]+) million",
    r"[Ff]iscal[- ]year (?:19|20)\d\d net income attributable to Deere & Company for the financial services operations is projected to be (?:approximately |about )?\$\s?([\d,]+) million",
    r"financial services (?:segment|operations)[^.]{0,90}(?:is|are) (?:expected|forecast|forecasted|projected) to be (?:approximately |about )?\$\s?([\d,]+) million",
    r"[Ff]inancial [Ss]ervices\.? [Ff]iscal[- ]year (?:19|20)\d\d[^.]{0,80}\$\s?([\d,]+) million",
    r"net income attributable to Deere & Company of (?:about |approximately |~ ?)?\$\s?([\d,]+) million in (?:19|20)\d\d",
]


def extract_net_income(txt):
    """-> (low, high, kind) in USDm, or None."""
    for p in RANGE_PATS:
        m = re.search(p, txt, re.I)
        if m:
            return bn(m.group(1)), bn(m.group(2)), "range"
    for p in POINT_PATS:
        m = re.search(p, txt, re.I)
        if m:
            v = bn(m.group(1))
            return v, v, "point"
    return None


def extract_adj_net_income(txt):
    for p in ADJ_PATS:
        m = re.search(p, txt, re.I)
        if m:
            return bn(m.group(1))
    return None


def extract_fs_net_income(txt):
    for p in FS_PATS:
        m = re.search(p, txt, re.I)
        if m:
            return float(m.group(1).replace(",", ""))
    return None


# --------------------------------------------------- consolidated / equip-ops growth
def extract_total_rev_growth(txt):
    m = re.search(r"[Nn]et sales and revenues are (?:projected|expected|forecast) to "
                  r"(increase|decrease) (?:by )?about (\d+) percent", txt)
    if m:
        v = float(m.group(2))
        return -v if m.group(1) == "decrease" else v
    return None


# ------------------------------------------------------------- legacy A&T / C&F
LEGACY_PATS = {
    "ag_turf": r"Deere'?s? worldwide sales of agriculture and turf equipment are (?:forecast|anticipated|expected) to (be )?(up|down|increase|decrease|decline|be up|be down)(?: by)? (?:about )?(\d+)(?: to (\d+))? percent",
    "cf": r"Deere'?s? worldwide sales of construction and forestry equipment are (?:forecast|anticipated|expected) to (be )?(up|down|increase|decrease|decline|be up|be down)(?: by)? (?:about )?(\d+)(?: to (\d+))? percent",
}


def extract_legacy_growth(txt, seg):
    m = re.search(LEGACY_PATS[seg], txt, re.I)
    if not m:
        return None
    direction = m.group(2).lower()
    sign = -1.0 if any(w in direction for w in ("down", "decrease", "decline")) else 1.0
    a = float(m.group(3))
    b = float(m.group(4)) if m.group(4) else a
    lo, hi = sorted([sign * a, sign * b])
    return lo, hi


# ------------------------------------------------------ modern segment outlook table
SEG_LABEL = {
    "ppa": r"Production ?& ?Precision ?Ag(?:riculture)?",
    "sat": r"Small Ag ?& ?Turf",
    "cf": r"Construction ?& ?Forestry",
}
VALUE_RX = (r"(?:Flat to Up|Up to|Down|Up)\s*~?\s*\d+(?:\.\d+)?%?"
            r"(?:\s*(?:to|-)\s*~?\s*\d+(?:\.\d+)?%?)?|~?\s*Flat")


def parse_growth_token(tok):
    """'Down 15 to 20%' -> (-20.0, -15.0). Returns (low, high) percent or None."""
    t = " ".join(tok.split())
    if re.fullmatch(r"~?\s*Flat", t, re.I):
        return 0.0, 0.0
    m = re.match(r"Flat to Up\s*~?\s*(\d+(?:\.\d+)?)%?", t, re.I)
    if m:
        return 0.0, float(m.group(1))
    m = re.match(r"(Up|Down)\s*~?\s*(\d+(?:\.\d+)?)%?(?:\s*(?:to|-)\s*~?\s*(\d+(?:\.\d+)?)%?)?", t, re.I)
    if not m:
        return None
    sign = -1.0 if m.group(1).lower() == "down" else 1.0
    a = float(m.group(2))
    b = float(m.group(3)) if m.group(3) else a
    return tuple(sorted([sign * a, sign * b]))


def segment_outlook_block(txt):
    """Return the text of the 'Deere Segment Outlook' block."""
    m = re.search(r"(?:##\s*)?(?:Deere )?Segment Outlook(?: \(|for )?[^\n]*", txt)
    if not m:
        return None
    start = m.start()
    tail = txt[start:start + 4000]
    stop = re.search(r"FORWARD-LOOKING|Safe Harbor|John Deere Capital Corporation", tail)
    if stop:
        tail = tail[:stop.start()]
    return tail


def extract_modern_segment_growth(txt):
    """-> {seg: (low, high)} percent, from the release's segment-outlook table."""
    blk = segment_outlook_block(txt)
    out = {}
    if not blk:
        return out
    # form 1/3: markdown table rows carrying the segment name
    for seg, lab in SEG_LABEL.items():
        m = re.search(r"\|[^|\n]*" + lab + r"[^|\n]*\|([^|\n]+)\|", blk, re.I)
        if m:
            g = parse_growth_token(m.group(1))
            if g:
                out[seg] = g
    if len(out) == 3:
        return out
    # form 2: column-major flattened text between 'Net Sales' and 'Net Income'
    m = re.search(r"\bNet Sales\b(.*?)\bNet Income\b", blk, re.S)
    if m:
        joined = " ".join(m.group(1).split())
        toks = re.findall(VALUE_RX, joined, re.I)
        if len(toks) >= 3:
            for seg, tok in zip(("ppa", "sat", "cf"), toks[:3]):
                g = parse_growth_token(tok)
                if g and seg not in out:
                    out[seg] = g
    return out


def extract_modern_segment_driver(txt, col):
    """col = 2 (currency translation) or 3 (price realization). -> {seg: pct}"""
    blk = segment_outlook_block(txt)
    out = {}
    if not blk:
        return out
    for seg, lab in SEG_LABEL.items():
        m = re.search(r"\|[^|\n]*" + lab + r"[^|\n]*\|([^|\n]+)\|([^|\n]+)\|([^|\n]+)\|", blk, re.I)
        if not m:
            continue
        cell = " ".join(m.group(col).split())
        if re.search(r"flat", cell, re.I):
            out[seg] = 0.0
            continue
        v = re.search(r"(Down|Up|\+|-)?\s*~?\s*(\d+(?:\.\d+)?)%", cell, re.I)
        if v:
            sign = -1.0 if (v.group(1) or "").lower() in ("down", "-") else 1.0
            out[seg] = sign * float(v.group(2))
    return out


# ------------------------------------------------------ slide-deck operating margin
SEG_NAMES = [("ppa", r"Production (?:&|and) Precision Ag"),
             ("sat", r"Small Ag (?:&|and) Turf"),
             ("cf", r"Construction (?:&|and) Forestry")]


def _last_seg(head):
    """Which segment heading appears last in the text preceding a slide block."""
    best, found = -1, None
    for key, pat in SEG_NAMES:
        ms = list(re.finditer(pat, head, re.I))
        if ms and ms[-1].start() > best:
            best, found = ms[-1].start(), key
    return found, best


def extract_slide_segment_outlook(rel):
    """-> {seg: {'margin': (lo,hi)}} operating-margin outlook from an earnings slide deck.

    Slide decks describe two charts per segment: FY net sales and FY operating
    margin. Net-sales guidance is taken from the 8-K table instead (cleaner);
    the slides are the only source for the segment operating-margin outlook.
    """
    txt = read(rel)
    res = {}
    marks = [m.start() for m in re.finditer(r"Business Segment Outlook", txt)]
    for i, st in enumerate(marks):
        end = marks[i + 1] if i + 1 < len(marks) else len(txt)
        end = min(end, st + 2500)
        head = txt[max(0, st - 1500):st]
        seg, _ = _last_seg(head)
        if seg is None:
            continue
        blk = txt[st:end]
        val = _margin_from_block(blk)
        if val and seg not in res:
            res[seg] = {"margin": val}
    return res


def _margin_from_block(blk):
    """First percent range that follows an 'Operating Margin' chart label.

    Skips 'Operating Margin' mentions that are part of a combined caption
    ("comparing Net Sales and Operating Margin ..."), detected by a 'Net Sales'
    mention appearing before the first percentage in the look-ahead window.
    """
    for m in re.finditer(r"[Oo]perating [Mm]argin", blk):
        win = blk[m.end():m.end() + 600]
        rng = re.search(r"(\d+(?:\.\d+)?)%?\s*(?:-|to)\s*(\d+(?:\.\d+)?)%", win)
        apx = re.search(r"~\s*(\d+(?:\.\d+)?)%", win)
        hit = rng or apx
        if not hit:
            continue
        ns = re.search(r"[Nn]et [Ss]ales", win[:130])
        if ns and ns.start() < hit.start():
            continue
        if rng and (not apx or rng.start() <= apx.start()):
            return float(rng.group(1)), float(rng.group(2))
        return float(apx.group(1)), float(apx.group(1))
    return None


def _first_pct_range(s):
    """First forward-looking percent range/approx in a slide image caption.
    Bare single values like '26.1%' are prior-year actuals and are skipped."""
    m = re.search(r"(\d+(?:\.\d+)?)%?\s*(?:-|to)\s*(\d+(?:\.\d+)?)%", s)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"~\s*(\d+(?:\.\d+)?)%", s)
    if m:
        v = float(m.group(1))
        return v, v
    return None


# ------------------------------------------------- transcript (prepared remarks) forms
TRANSCRIPT_SEG_SALES = {
    "ag_turf": r"(?:sales of worldwide|Deere sales of worldwide|worldwide) (?:Ag(?:riculture)?)\s*(?:and|&)\s*Turf equipment (?:are|is|continue to be) (?:now |still )?forecast(?:ed)? to be (up|down)(?: between)? (?:about |approximately |roughly )?(\d+(?:\.\d+)?)%(?:\s*(?:and|to|-)\s*(\d+(?:\.\d+)?)%)?",
    "cf": r"Construction\s*(?:and|&)\s*Forestry(?: \d{4})?(?: net)? sales (?:are|is)? ?(?:now |still )?forecast(?:ed)? to be (up|down)(?: between)? (?:about |approximately |roughly )?(\d+(?:\.\d+)?)%(?:\s*(?:and|to|-)\s*(\d+(?:\.\d+)?)%)?",
}
TRANSCRIPT_SEG_SALES_ALT = {
    "cf": r"[Nn]et sales in Construction\s*(?:and|&)\s*Forestry are (?:now )?forecast to be (up|down) about (\d+(?:\.\d+)?)%",
}


def extract_transcript_seg_sales(txt, seg):
    pats = [TRANSCRIPT_SEG_SALES[seg]] + ([TRANSCRIPT_SEG_SALES_ALT[seg]] if seg in TRANSCRIPT_SEG_SALES_ALT else [])
    for p in pats:
        m = re.search(p, txt, re.I)
        if not m:
            continue
        sign = -1.0 if m.group(1).lower() == "down" else 1.0
        a = float(m.group(2))
        b = float(m.group(3)) if (m.lastindex or 0) >= 3 and m.group(3) else a
        return tuple(sorted([sign * a, sign * b]))
    return None


AT_MARGIN_PATS = [
    r"(?:20\d\d )?operating margin for the Ag(?:riculture)?\s*(?:and|&)\s*Turf division is forecast(?:ed)? (?:at|to be) (?:about|approximately) (\d+(?:\.\d+)?)%",
    r"Ag(?:riculture)?\s*(?:and|&)\s*Turf [Dd]ivision'?s? (?:operating )?margins? is (?:now )?forecast(?:ed)? to be (?:about|approximately|up approximately) (\d+(?:\.\d+)?)%",
    r"Ag(?:riculture)?\s*(?:and|&)\s*Turf [Dd]ivision (?:operating )?margins? is (?:now )?forecast(?:ed)? to be (?:about|approximately|up approximately) (\d+(?:\.\d+)?)%",
    r"forecast for the Ag(?:riculture)?\s*(?:and|&)\s*Turf division'?s? operating margin (?:continues to be|is now) (?:approximately|about) (\d+(?:\.\d+)?)%",
    r"Ag(?:riculture)?\s*(?:and|&)\s*Turf [Dd]ivision operating margin forecast is about (\d+(?:\.\d+)?)%",
]


def extract_at_operating_margin(txt):
    for p in AT_MARGIN_PATS:
        m = re.search(p, txt, re.I)
        if m:
            return float(m.group(1))
    return None


CF_MARGIN_PATS = [
    r"C ?& ?F'?s? full year operating margin is (?:projected|forecast(?:ed)?) to be (?:about|approximately) (\d+(?:\.\d+)?)%",
]


def extract_cf_operating_margin(txt):
    for p in CF_MARGIN_PATS:
        m = re.search(p, txt, re.I)
        if m:
            return float(m.group(1))
    return None


def extract_ppa_absolute_sales(txt):
    """FY2021 Q1 gave PPA/SAT/CF net sales as absolute dollar ranges."""
    blk = segment_outlook_block(txt)
    out = {}
    if not blk:
        return out
    for seg, lab in SEG_LABEL.items():
        m = re.search(r"\|[^|\n]*" + lab + r"[^|\n]*\|\s*\$?([\d,]+) to ([\d,]+)\s*\|", blk, re.I)
        if m:
            out[seg] = (float(m.group(1).replace(",", "")), float(m.group(2).replace(",", "")))
    return out


def slide_sales_direction(rel, seg):
    """Sign of a slide's segment net-sales forecast: -1 down, +1 up, None unknown."""
    txt = read(rel)
    marks = [m.start() for m in re.finditer(r"Business Segment Outlook", txt)]
    for i, st in enumerate(marks):
        end = marks[i + 1] if i + 1 < len(marks) else min(len(txt), st + 4000)
        head = txt[max(0, st - 1500):st]
        found, _best = _last_seg(head)
        if found != seg:
            continue
        blk = txt[st:end]
        _om = list(re.finditer(r"[Oo]perating [Mm]argin", blk))
        cut = _om[-1].start() if _om else -1
        part = blk[:cut] if cut > 0 else blk
        if re.search(r"downward|pointing down|points? down|decrease|decline|negative", part, re.I):
            return -1
        if re.search(r"upward|pointing up|increase", part, re.I):
            return 1
    return None
