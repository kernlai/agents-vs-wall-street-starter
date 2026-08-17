#!/usr/bin/env python3
"""Kubota Corporation (TSE 6326) financials -- scripted extraction.

Kubota is NOT an SEC reporting company: it filed Form 15F-12B on 2013-07-16 and
deregistered, so EDGAR XBRL stops at the 20-F for FY ended 2013-03-31. The
recent history therefore has to come from Kubota's own IR PDF releases, which
live at a predictable URL:

    https://www.kubota.com/ir/financial/release/data/<term>q<n>e.pdf

where <term> is Kubota's "business term" number (term = fiscal_year - 1889;
term 137 = FY2026) and <n> is 1..4. The releases are CUMULATIVE (q2 = six
months, q3 = nine months, q4 = full year), so standalone quarters are obtained
by differencing. Figures are IFRS, in millions of yen.

Emits tidy long rows (same header as the peer CSV) on stdout as CSV, or to
--out. Requires `pdftotext` (poppler) on PATH.
"""
from __future__ import annotations

import argparse
import calendar
import os
import re
import subprocess
import sys
import urllib.request

UA = "AgentsVsWallStreet cor@salomo.io"
URL = "https://www.kubota.com/ir/financial/release/data/{term}q{q}e.pdf"

# "FOR THE SIX MONTHS ENDED JUNE 30, 2026" / "FOR THE YEAR ENDED DECEMBER 31, 2025"
HDR = re.compile(
    r"FOR\s+THE\s+(THREE|SIX|NINE|TWELVE|YEAR)\s*(?:MONTHS?)?\s+ENDED\s+"
    r"([A-Z]+)\.?\s+(\d{1,2}),?\s+(\d{4})", re.I)
MONTHS = {m.upper(): i for i, m in enumerate(calendar.month_name) if m}
MONTHS.update({m.upper(): i for i, m in enumerate(calendar.month_abbr) if m})

NUM = r"\(?¥?\s*\(?\s*([\d,]+(?:\.\d+)?)\s*\)?"


def money(line):
    """First yen amount on the line, negative if parenthesised."""
    m = re.search(r"(\()?\s*¥\s*(\()?\s*([\d,]+(?:\.\d+)?)\s*(\))?", line)
    if not m:
        return None
    v = float(m.group(3).replace(",", ""))
    if m.group(1) or m.group(2):
        v = -v
    return v


def grab(text, label):
    for line in text.splitlines():
        s = line.strip()
        if s.lower().startswith(label.lower()):
            v = money(s)
            if v is not None:
                return v
    return None


def fetch(term, q, cache):
    path = os.path.join(cache, "kubota_%dq%d.pdf" % (term, q))
    if not os.path.exists(path):
        req = urllib.request.Request(URL.format(term=term, q=q), headers={"User-Agent": UA})
        try:
            data = urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:
            return None, str(e)
        if not data.startswith(b"%PDF"):
            return None, "not a pdf"
        os.makedirs(cache, exist_ok=True)
        open(path, "wb").write(data)
    return path, None


def parse(path):
    txt = subprocess.run(["pdftotext", "-layout", "-f", "1", "-l", "2", path, "-"],
                         capture_output=True, text=True).stdout
    m = HDR.search(txt)
    if not m:
        return None
    words, mon, day, yr = m.group(1).upper(), m.group(2).upper(), int(m.group(3)), int(m.group(4))
    nmonths = {"THREE": 3, "SIX": 6, "NINE": 9, "TWELVE": 12, "YEAR": 12}[words]
    mon = MONTHS.get(mon[:3].title().upper()) or MONTHS.get(mon)
    if not mon:
        return None
    end = "%04d-%02d-%02d" % (yr, mon, day)
    rev = grab(txt, "Revenue")
    op = grab(txt, "Operating profit")
    eps = None
    lines = txt.splitlines()
    for i, line in enumerate(lines):
        if "Earnings per share" in line:
            for j in range(i + 1, min(i + 4, len(lines))):
                if re.search(r"\bBasic\b", lines[j]):
                    eps = money(lines[j])
                    break
            break
    return dict(end=end, nmonths=nmonths, rev=rev, op=op, eps=eps)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="kubota_pdf")
    ap.add_argument("--out", required=True)
    ap.add_argument("--first-term", type=int, default=127)   # FY2016, first clean Dec FY
    ap.add_argument("--last-term", type=int, default=137)    # FY2026
    ap.add_argument("--sec-facts", default=None,
                    help="path to cached SEC companyfacts JSON for CIK 109821")
    args = ap.parse_args()

    ytd = {}   # (fy, nmonths) -> record
    misses = []
    for term in range(args.first_term, args.last_term + 1):
        fy = term + 1889
        for q in (1, 2, 3, 4):
            path, err = fetch(term, q, args.cache)
            if path is None:
                misses.append("%dq%d (%s)" % (term, q, err))
                continue
            rec = parse(path)
            if rec is None:
                misses.append("%dq%d (unparsed header)" % (term, q))
                continue
            rec["term"] = term
            ytd[(fy, rec["nmonths"])] = rec
            print("  term %d q%d -> %s %dm rev=%s op=%s eps=%s"
                  % (term, q, rec["end"], rec["nmonths"], rec["rev"], rec["op"], rec["eps"]),
                  file=sys.stderr)

    rows = []
    for (fy, nm), rec in sorted(ytd.items()):
        src = URL.format(term=rec["term"], q=nm // 3)
        base = ("Kubota is not an SEC filer (deregistered 2013-07-16, Form 15F-12B); "
                "figures from Kubota's own IFRS results release. Currency JPY, NOT "
                "converted to USD. Kubota's fiscal year ends 31 December (it ended "
                "31 March up to and including FY2015, with a 9-month transition "
                "period Apr-Dec 2015) -- this is a different calendar again from "
                "Deere's late-October year end")
        prior = ytd.get((fy, nm - 3))
        qlabel = "Q%d" % (nm // 3)
        if nm == 12:
            for sid, val, units in (("kubota_revenue", rec["rev"], "JPYm"),
                                    ("kubota_operating_profit", rec["op"], "JPYm"),
                                    ("kubota_eps_basic", rec["eps"], "JPY/share")):
                if val is not None:
                    rows.append([sid, rec["end"], fy, "FY", val, units, "filing", src,
                                 base + "; annual (12-month) figure as reported"])
            if rec["rev"] and rec["op"]:
                rows.append(["kubota_operating_margin", rec["end"], fy, "FY",
                             round(100.0 * rec["op"] / rec["rev"], 4), "percent",
                             "filing", src, base + "; = operating profit / revenue, IFRS"])
        # standalone quarter
        if nm == 3:
            qrev, qop, qeps = rec["rev"], rec["op"], rec["eps"]
            derived = False
        elif prior:
            qrev = None if (rec["rev"] is None or prior["rev"] is None) else rec["rev"] - prior["rev"]
            qop = None if (rec["op"] is None or prior["op"] is None) else rec["op"] - prior["op"]
            qeps = None if (rec["eps"] is None or prior["eps"] is None) else round(rec["eps"] - prior["eps"], 2)
            derived = True
        else:
            continue
        dnote = ("; standalone quarter DERIVED by differencing consecutive cumulative "
                 "year-to-date releases (Kubota reports YTD, not discrete quarters)"
                 if derived else "; three-month release, as reported")
        st = "inference" if derived else "filing"
        for sid, val, units in (("kubota_revenue", qrev, "JPYm"),
                                ("kubota_operating_profit", qop, "JPYm"),
                                ("kubota_eps_basic", qeps, "JPY/share")):
            if val is not None:
                rows.append([sid, rec["end"], fy, qlabel, val, units, st, src, base + dnote])
        if qrev and qop is not None:
            rows.append(["kubota_operating_margin", rec["end"], fy, qlabel,
                         round(100.0 * qop / qrev, 4), "percent", st, src,
                         base + dnote + "; = operating profit / revenue, IFRS"])

    # ---- legacy SEC 20-F era (US GAAP, FY ended 31 MARCH) ---------------------
    # Kept under DISTINCT series_ids. Merging it into kubota_revenue would splice
    # a US-GAAP March-year-end series onto an IFRS December-year-end series across
    # an unlabelled 3-year gap (the Apr-Dec 2015 transition period) -- exactly the
    # kind of silent structural break that ruins a fitted model.
    if args.sec_facts and os.path.exists(args.sec_facts):
        import json as _json
        from datetime import date as _date

        def _d(s):
            y, m, dd = s.split("-")
            return _date(int(y), int(m), int(dd))

        g = _json.load(open(args.sec_facts))["facts"]["us-gaap"]
        legacy = {}
        for tag, sid, units in (("Revenues", "kubota_revenue_legacy_usgaap_mar", "JPYm"),
                                ("OperatingIncomeLoss",
                                 "kubota_operating_profit_legacy_usgaap_mar", "JPYm")):
            node = g.get(tag)
            if not node:
                continue
            for f in node["units"].get("JPY", []):
                if "start" not in f:
                    continue
                n = (_d(f["end"]) - _d(f["start"])).days + 1
                if not (350 <= n <= 380):
                    continue
                key = (sid, f["end"])
                if key not in legacy or f["filed"] < legacy[key][0]:
                    legacy[key] = (f["filed"], f["val"], f.get("form", ""))
        lnote = ("LEGACY BASIS -- DO NOT SPLICE ONTO kubota_revenue. US GAAP, fiscal "
                 "year ended 31 MARCH, from Kubota's SEC Form 20-F XBRL. Kubota "
                 "deregistered from the SEC on 2013-07-16 (Form 15F-12B), so this "
                 "series stops at FY ended 2013-03-31. Kubota later moved to IFRS and "
                 "to a 31 December year end via a 9-month transition period "
                 "(Apr-Dec 2015); there is no comparable data for FY2014-FY2015")
        for (sid, end), (filed, val, form) in sorted(legacy.items()):
            rows.append([sid, end, int(end[:4]), "FY", val / 1e6, "JPYm", "api",
                         "https://data.sec.gov/api/xbrl/companyfacts/CIK0000109821.json",
                         lnote + "; as-first-reported in %s filed %s" % (form, filed)])
        rmap = {e: v for (s, e), (_, v, _f) in legacy.items() if s.endswith("revenue_legacy_usgaap_mar")}
        omap = {e: v for (s, e), (_, v, _f) in legacy.items() if s.startswith("kubota_operating_profit_legacy")}
        for end in sorted(set(rmap) & set(omap)):
            if rmap[end]:
                rows.append(["kubota_operating_margin_legacy_usgaap_mar", end,
                             int(end[:4]), "FY", round(100.0 * omap[end] / rmap[end], 4),
                             "percent", "api",
                             "https://data.sec.gov/api/xbrl/companyfacts/CIK0000109821.json",
                             lnote + "; = OperatingIncomeLoss / Revenues"])

    with open(args.out, "w") as f:
        f.write("series_id,period_end,fiscal_year,fiscal_quarter,value,units,"
                "source_type,source,notes\n")
        for r in sorted(rows, key=lambda r: (r[0], r[1], r[3])):
            cells = []
            for c in r:
                c = "" if c is None else str(c)
                if any(ch in c for ch in ',"\n'):
                    c = '"' + c.replace('"', '""') + '"'
                cells.append(c)
            f.write(",".join(cells) + "\n")
    print("kubota: %d rows -> %s" % (len(rows), args.out))
    print("kubota misses: %d -> %s" % (len(misses), ", ".join(misses[:40])), file=sys.stderr)


if __name__ == "__main__":
    main()
