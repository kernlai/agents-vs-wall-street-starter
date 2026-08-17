#!/usr/bin/env python3
"""
fetch_aem_globenewswire_mirror.py

Second, INDEPENDENT rendering of the AEM US Ag Tractor and Combine Report.

AEM distributes each monthly report as a GlobeNewswire press release whose
body contains the same table as the PDF, marked up as HTML.  globenewswire.com
itself refuses non-browser clients, but the FinancialContent syndication
mirror serves the identical release and is fetchable:

  https://markets.financialcontent.com/pennwell.bioopticsworld/article/
      gnwcq-<YYYY>-<M>-<D>-aem-united-states-ag-tractor-and-combine-report-<month>-<year>

The release day varies (usually the 8th-14th of the following month), so the
script probes a small day window.

Used for two things:
  1. filling months where no PDF survives in the Wayback archive
  2. cross-checking values already extracted from the PDFs

Standard library only.
"""

import html
import json
import os
import re
import subprocess
import sys
import time

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
BASE = ("https://markets.financialcontent.com/pennwell.bioopticsworld/article/"
        "gnwcq-%d-%d-%d-aem-united-states-ag-tractor-and-combine-report-%s-%d")
CACHE = os.environ.get("GNW_CACHE", "/tmp/gnw_cache")
os.makedirs(CACHE, exist_ok=True)

MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]

ROWS = [
    (r"&lt;\s*40\s*HP|<\s*40\s*HP", "tractor_2wd_lt40hp"),
    (r"40\s*&lt;\s*100\s*HP|40\s*<\s*100\s*HP", "tractor_2wd_40to100hp"),
    (r"100\+\s*HP", "tractor_2wd_100hp_plus"),
    (r"Total\s+2WD\s+Farm\s+Tractors", "tractor_2wd_total"),
    (r"4WD\s+Farm\s+Tractors", "tractor_4wd"),
    (r"Total\s+Farm\s+Tractors", "tractor_total"),
    (r"Self[- ]?Prop\.?\s*Combines", "combine_sp"),
]


def fetch(url, name):
    p = os.path.join(CACHE, name)
    if os.path.exists(p):
        return open(p, encoding="utf-8", errors="replace").read()
    r = subprocess.run(["curl", "-sSL", "--max-time", "40", "-A", UA, url],
                       capture_output=True)
    body = r.stdout.decode("utf-8", "replace")
    open(p, "w", encoding="utf-8").write(body)
    return body


def parse(hbody):
    """Pull the unit table out of the release HTML."""
    out = {}
    # the release is a <table>; work row by row on the raw markup
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", hbody, re.S | re.I):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr,
                                     re.S | re.I)]
        if not cells:
            continue
        joined = " ".join(cells[:3])
        key = None
        for pat, k in ROWS:
            if re.search(pat, joined, re.I):
                key = k
                break
        if key is None or key in out:
            continue
        nums = []
        for c in cells:
            c = c.replace(",", "").replace("%", "").strip()
            if re.fullmatch(r"-?\d+(\.\d+)?", c):
                nums.append(float(c))
        if len(nums) >= 6:
            out[key] = nums
    return out


def get_month(year, month, probe_days=range(6, 18)):
    """Return {key: [nums]} for report month `month` of `year`."""
    ry, rm = (year, month + 1) if month < 12 else (year + 1, 1)
    for d in probe_days:
        url = BASE % (ry, rm, d, MONTHS[month - 1], year)
        name = "gnw_%04d%02d_%02d.html" % (year, month, d)
        body = fetch(url, name)
        if "Total Farm Tractors" not in body:
            continue
        tbl = parse(body)
        if len(tbl) >= 6:
            return tbl, url
        time.sleep(0.3)
    return None, None


def main(out_json, targets):
    res = {}
    for (y, m) in targets:
        tbl, url = get_month(y, m)
        if tbl:
            res["%04d-%02d" % (y, m)] = dict(table=tbl, source=url)
            print("  OK   %04d-%02d  %s" % (y, m, url), file=sys.stderr)
        else:
            print("  MISS %04d-%02d" % (y, m), file=sys.stderr)
    with open(out_json, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote %d months -> %s" % (len(res), out_json))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/gnw.json"
    if len(sys.argv) > 2:
        tg = [tuple(int(x) for x in a.split("-")) for a in sys.argv[2:]]
    else:
        # gap-fill months + cross-check months
        tg = [(2025, 9), (2026, 3), (2026, 5), (2026, 6),
              (2026, 7), (2026, 4), (2025, 12), (2024, 12), (2023, 6),
              (2022, 12), (2023, 12), (2024, 6)]
    main(out, tg)
