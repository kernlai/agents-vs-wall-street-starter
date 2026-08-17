#!/usr/bin/env python3
"""
Extract Deere & Company quarterly income-statement lines (Net sales, Cost of sales)
from the offline document corpus.

The corpus 8-K earnings releases and 10-Q quarterly reports both contain a markdown
table headed "STATEMENTS OF CONSOLIDATED INCOME".  Column 1 of the numeric block is
always the CURRENT three-month period; later columns are prior-year and year-to-date.

Output: list of dicts {period_end, fiscal_year, fiscal_quarter, net_sales, cost_of_sales,
                       source, doc_kind}

Standard library only.  Run directly to dump a TSV to stdout.
"""
import os
import re
import sys
import datetime as dt

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
FILINGS = os.path.join(CORPUS, "filings")

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}


# ---------------------------------------------------------------- fiscal helpers
def fiscal_qtr_from_end(d):
    """Map a Deere period-end date to (fiscal_year, 'Q1'..'Q4').

    Deere's FY ends late Oct / early Nov.  Quarter ends fall in tight windows:
      Q1 late Jan-early Feb | Q2 late Apr-early May
      Q3 late Jul-early Aug | Q4 late Oct-early Nov
    """
    m, day, y = d.month, d.day, d.year
    if m == 1 or (m == 2 and day <= 10):
        return y, "Q1"
    if (m == 4 and day >= 20) or (m == 5 and day <= 10):
        return y, "Q2"
    if (m == 7 and day >= 20) or (m == 8 and day <= 10):
        return y, "Q3"
    if (m == 10 and day >= 20) or (m == 11 and day <= 10):
        return y, "Q4"
    return None, None


def month_to_fiscal_qtr(year, month):
    """Bucket a calendar month into the Deere fiscal quarter that contains it.

    FQ1 = Nov, Dec, Jan   FQ2 = Feb, Mar, Apr
    FQ3 = May, Jun, Jul   FQ4 = Aug, Sep, Oct
    (Deere quarter ends drift by a few days under the 52/53-week calendar; the
    month bucket is correct to within a few days and is the standard convention.)
    """
    if month in (11, 12):
        return year + 1, "Q1"
    if month == 1:
        return year, "Q1"
    if month in (2, 3, 4):
        return year, "Q2"
    if month in (5, 6, 7):
        return year, "Q3"
    return year, "Q4"  # 8, 9, 10


# ---------------------------------------------------------------- parsing
NUM = re.compile(r"^\(?\$?\s*(-?[\d,]+(?:\.\d+)?)\)?$")


def cells(line):
    return [c.strip().replace("​", "").strip() for c in line.strip().strip("|").split("|")]


def first_numbers(cs, n=4):
    """Pull the leading numeric cells out of a markdown table row."""
    out = []
    for c in cs[1:]:
        c = c.strip()
        if not c or c in ("$", "-", "—"):
            continue
        mo = NUM.match(c)
        if mo:
            v = float(mo.group(1).replace(",", ""))
            if c.startswith("(") or c.startswith("$ ("):
                v = -v
            out.append(v)
            if len(out) >= n:
                break
        else:
            # a non-numeric, non-filler cell means we have left the number block
            if re.search(r"[A-Za-z]{2}", c):
                break
    return out


PERIOD_RE = re.compile(
    r"(?:Three|Six|Nine|Twelve)\s+Months?\s+Ended\s+(?:and\s+)?", re.I)
DATE_RE = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})[,\s]+(\d{4})",
    re.I)


def parse_doc(path):
    """Return (period_end, net_sales, cost_of_sales, header_kind) or None."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    lines = text.split("\n")

    # locate the consolidated income statement header
    idxs = [i for i, ln in enumerate(lines)
            if re.search(r"STATEMENTS? OF CONSOLIDATED INCOME", ln, re.I)]
    if not idxs:
        return None

    for start in idxs:
        window = lines[start:start + 90]
        # the "For the Three and Six Months Ended May 3, 2026 and April 27, 2025" line
        end_date = None
        kind = None
        for ln in window[:8]:
            if re.search(r"Months? Ended|Years? Ended", ln, re.I):
                dm = DATE_RE.search(ln)
                if dm:
                    end_date = dt.date(int(dm.group(3)), MONTHS[dm.group(1).title()], int(dm.group(2)))
                # Q4 releases are headed "For the Three Months and Years Ended Oct 30, 2022 ...";
                # 10-K statements are headed "For the Years Ended ...".  The presence of
                # "Three ... Months" is what tells us column 1 is a three-month figure.
                kind = "quarter" if re.search(r"Three\s+(?:and\s+\w+\s+)?Months?", ln, re.I) else "annual"
                break
        if end_date is None:
            continue

        ns = cos = None
        for ln in window:
            if not ln.lstrip().startswith("|"):
                continue
            cs = cells(ln)
            label = cs[0].lower().rstrip(" .:*")
            if ns is None and label == "net sales":
                v = first_numbers(cs, 1)
                if v:
                    ns = v[0]
            elif cos is None and label == "cost of sales":
                v = first_numbers(cs, 1)
                if v:
                    cos = v[0]
            if ns is not None and cos is not None:
                break
        if ns is not None and cos is not None:
            return end_date, ns, cos, kind
    return None


def collect():
    rows = {}
    for name in sorted(os.listdir(FILINGS)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(FILINGS, name)
        got = parse_doc(path)
        if not got:
            continue
        end_date, ns, cos, kind = got
        fy, fq = fiscal_qtr_from_end(end_date)
        if fy is None:
            continue
        rel = os.path.join("filings", name)
        is_8k = "-8k" in name
        rec = dict(period_end=end_date.isoformat(), fiscal_year=fy, fiscal_quarter=fq,
                   net_sales=ns, cost_of_sales=cos, source=rel,
                   doc_kind="8-K" if is_8k else "10-Q/10-K", period_kind=kind)
        key = (end_date.isoformat(),)
        # prefer the 8-K earnings release (three-month column is unambiguous there),
        # but keep both for cross-validation
        rows.setdefault(key, []).append(rec)
    return rows


if __name__ == "__main__":
    rows = collect()
    print("period_end\tfy\tfq\tnet_sales\tcost_of_sales\tdoc\tsource")
    for k in sorted(rows):
        for r in rows[k]:
            print(f"{r['period_end']}\t{r['fiscal_year']}\t{r['fiscal_quarter']}\t"
                  f"{r['net_sales']}\t{r['cost_of_sales']}\t{r['doc_kind']}\t{r['source']}")
