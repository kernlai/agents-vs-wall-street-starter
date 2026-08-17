#!/usr/bin/env python3
"""
fetch_aem_tractor_combine.py

Downloads the AEM (Association of Equipment Manufacturers) monthly
"United States Ag Tractor and Combine Report" PDFs and parses the unit
retail-sales table out of them.

Sources, in order of preference:
  1. live www.aem.org (current month only, plus a handful of legacy paths)
  2. the Internet Archive Wayback Machine copies of aem.org statistics PDFs
     (discovered via the CDX API -- see discover_wayback())

Each monthly PDF contains, for one report month M of year Y:
    <category>  month_Y  month_(Y-1)  %chg   ytd_Y  ytd_(Y-1)  %chg   [beginning_inventory]
so one PDF yields observations for BOTH Y and Y-1.  A December PDF therefore
yields two full calendar years of annual totals.

Outputs a raw tidy JSON/CSV of every observation with full provenance so the
downstream builder can de-duplicate and reconcile.

Standard library only.  Requires the `pdftotext` binary (poppler) on PATH.
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

SCRATCH = os.environ.get("AEM_CACHE", "/tmp/aem_cache")
PDF_DIR = os.path.join(SCRATCH, "pdf")
os.makedirs(PDF_DIR, exist_ok=True)

MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]
MON_IDX = {m: i + 1 for i, m in enumerate(MONTHS)}
MON_IDX.update({m[:3]: i + 1 for i, m in enumerate(MONTHS)})

# Canonical row labels -> series key.
# Two document generations exist:
#   modern (2011-12 onward):  "< 40 HP" / "40 < 100 HP" / "100+ HP" /
#                             "Total 2WD Farm Tractors" / "4WD Farm Tractors" /
#                             "Total Farm Tractors" / "Self-Prop Combines"
#   legacy (2004-2011 Flash): "Under 40 HP" / "40 & Under 100 HP" /
#                             "100 HP & Over" / "2 Wheel Drive" /
#                             "4 Wheel Drive" / "WHEEL TRACTORS" /
#                             "(Self-Propelled)"
# Order matters: the more specific modern labels are tested first.
ROW_PATTERNS = [
    (re.compile(r"^\s*<\s*40\s*HP", re.I), "tractor_2wd_lt40hp"),
    (re.compile(r"^\s*Under\s*40\s*HP", re.I), "tractor_2wd_lt40hp"),
    (re.compile(r"^\s*40\s*<\s*100\s*HP", re.I), "tractor_2wd_40to100hp"),
    (re.compile(r"^\s*40\s*&\s*Under\s*100\s*HP", re.I), "tractor_2wd_40to100hp"),
    (re.compile(r"^\s*100\+\s*HP", re.I), "tractor_2wd_100hp_plus"),
    (re.compile(r"^\s*100\s*HP\s*&\s*Over", re.I), "tractor_2wd_100hp_plus"),
    (re.compile(r"^\s*Total\s+2WD\s+Farm\s+Tractors", re.I), "tractor_2wd_total"),
    (re.compile(r"^\s*2\s*Wheel\s*Drive\b", re.I), "tractor_2wd_total"),
    (re.compile(r"^\s*4WD\s+Farm\s+Tractors", re.I), "tractor_4wd"),
    (re.compile(r"^\s*4\s*Wheel\s*Drive\b", re.I), "tractor_4wd"),
    (re.compile(r"^\s*Total\s+Farm\s+Tractors", re.I), "tractor_total"),
    (re.compile(r"^\s*WHEEL\s+TRACTORS\b", re.I), "tractor_total"),
    (re.compile(r"^\s*Self[- ]?Prop(elled)?\.?\s+Combines", re.I), "combine_sp"),
    (re.compile(r"^\s*\(\s*Self[- ]?Propelled\s*\)", re.I), "combine_sp"),
]

NUM = re.compile(r"-?[\d,]+\.?\d*")


# ----------------------------------------------------------------- fetching

def http_get(url, timeout=45, tries=3):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "*/*",
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            # 404/410 are definitive -- never retry them
            if e.code in (400, 403, 404, 410):
                raise
            last = e
            time.sleep(1.5 * (attempt + 1))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise last


def discover_wayback():
    """Ask the Wayback CDX API for every archived aem.org ag-report PDF."""
    rows = []
    patterns = ["usag", "us-month-ag-report", "us-monthly-ag-report",
                "farm_flash", "ag-report"]
    for pat in patterns:
        url = ("http://web.archive.org/cdx/search/cdx?url=aem.org&matchType=domain"
               "&output=json&fl=original,timestamp&filter=statuscode:200"
               "&collapse=urlkey&limit=5000"
               "&filter=urlkey:.*%s.*" % pat)
        try:
            body, _ = http_get(url, timeout=120)
            data = json.loads(body.decode("utf-8", "replace"))
        except Exception as e:  # noqa: BLE001
            print("  CDX %-24s FAILED %s" % (pat, e), file=sys.stderr)
            continue
        for orig, ts in data[1:]:
            rows.append((orig, ts))
    # keep US ag reports only
    out = {}
    for orig, ts in rows:
        low = orig.lower()
        if ".pdf" not in low:
            continue
        if any(k in low for k in ("/can", "can-month", "can%20", "canada",
                                  "russia", "subscription", "brazil", "arc-flash")):
            continue
        if not any(k in low for k in ("usag", "us-month-ag", "us-monthly-ag",
                                      "united-states", "usa-")):
            continue
        base = orig.split("?")[0]
        # prefer the shortest (query-free) form of each file
        out.setdefault(base, ts)
    return sorted(out.items())


def fetch_pdf(url, wayback_ts=None):
    """Download a PDF (via Wayback id_ raw form when a timestamp is given)."""
    key = re.sub(r"[^A-Za-z0-9._-]", "_", url.split("/")[-1].split("?")[0])
    if wayback_ts:
        key = wayback_ts + "_" + key
    path = os.path.join(PDF_DIR, key)
    if os.path.exists(path) and os.path.getsize(path) > 4000:
        return path
    target = url
    if wayback_ts:
        target = "https://web.archive.org/web/%sid_/%s" % (wayback_ts, url)
    # curl is markedly more reliable than urllib against archive.org, which
    # refuses urllib connections under even light concurrency.
    tmp = path + ".part"
    for attempt in range(4):
        subprocess.run(["curl", "-sSL", "--max-time", "90",
                        "--retry", "2", "--retry-delay", "3",
                        "-A", UA, "-o", tmp, target],
                       capture_output=True)
        if os.path.exists(tmp):
            with open(tmp, "rb") as fh:
                head = fh.read(5)
            if head.startswith(b"%PDF"):
                os.replace(tmp, path)
                return path
            os.remove(tmp)
        time.sleep(2 + 3 * attempt)
    print("  DL FAIL %s" % url, file=sys.stderr)
    return None


# ------------------------------------------------------------------ parsing

def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"],
                              capture_output=True, timeout=60).stdout.decode(
                                  "utf-8", "replace")
    except Exception:  # noqa: BLE001
        return ""


def parse_header_period(text, fallback_name=""):
    """Find the report month/year, e.g. 'December 2021'."""
    # legacy Flash Reports write "September, 2004 Flash Report"; modern ones
    # write "December 2021" -- allow the optional comma, but never let
    # "October 11, 2004" (the cover-letter date) match.
    pat = r"\b(%s),?\s+((?:19|20)\d{2})\b" % "|".join(MONTHS)
    head = "\n".join(text.splitlines()[:16])
    for hay in (head, text):
        for m in re.finditer(pat, hay, re.I):
            return MON_IDX[m.group(1).lower()], int(m.group(2))
    # filename fallbacks: US-Month-Ag-Report-12-2021 / 18-05-USAG / 12_12_USAG
    fn = fallback_name
    m = re.search(r"Report-(\d{1,2})-(\d{4})", fn, re.I)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"Report-(\d{4})-(\d{1,2})", fn, re.I)
    if m:
        return int(m.group(2)), int(m.group(1))
    m = re.search(r"\b(\d{2})[-_](\d{1,2})[-_]USAG", fn, re.I)
    if m:
        return int(m.group(2)), 2000 + int(m.group(1))
    return None, None


def parse_years(text):
    """The two column-header years, e.g. (2021, 2020)."""
    for line in text.splitlines()[:20]:
        yrs = re.findall(r"\b(19|20)\d{2}\b", line)
        full = re.findall(r"\b((?:19|20)\d{2})\b", line)
        if len(full) >= 2:
            a, b = int(full[0]), int(full[1])
            if a - b == 1:
                return a, b
    return None, None


def parse_table(text):
    """Return {series_key: [numbers...]} from the report body."""
    out = {}
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        for pat, key in ROW_PATTERNS:
            if key in out:
                continue
            m = pat.match(line) or pat.match(line.lstrip())
            if not m:
                continue
            # Numbers are read only AFTER the label so that digits inside the
            # label itself ("40", "100") can never be mistaken for data.
            tail = (line if pat.match(line) else line.lstrip())[m.end():]
            vals = []
            for n in NUM.findall(tail):
                try:
                    vals.append(float(n.replace(",", "")))
                except ValueError:
                    pass
            if len(vals) >= 6:
                out[key] = vals
            break
    return out


def observations_from_pdf(path, url, wayback_ts):
    text = pdf_text(path)
    # modern reports say "Total Farm Tractors"; the pre-2011 Flash Reports say
    # "TOTAL FARM / WHEEL TRACTORS" across two lines.
    low = text.lower()
    if "farm tractors" not in low and "wheel tractors" not in low:
        return []
    mon, yr = parse_header_period(text, os.path.basename(path))
    y_cur, y_prev = parse_years(text)
    if y_cur is None and yr is not None:
        y_cur, y_prev = yr, yr - 1
    if mon is None or y_cur is None:
        return []
    if yr is not None and yr != y_cur:
        # header year wins for the report period
        y_cur, y_prev = yr, yr - 1
    table = parse_table(text)
    src = url if not wayback_ts else \
        "https://web.archive.org/web/%sid_/%s" % (wayback_ts, url)
    obs = []
    for key, vals in table.items():
        # canonical layout: m_cur, m_prev, pct, ytd_cur, ytd_prev, pct, [inv]
        m_cur, m_prev = vals[0], vals[1]
        ytd_cur, ytd_prev = (vals[3], vals[4]) if len(vals) >= 5 else (None, None)
        inv = vals[6] if len(vals) >= 7 else None
        obs.append(dict(key=key, kind="month", year=y_cur, month=mon,
                        value=m_cur, source=src, report="%04d-%02d" % (y_cur, mon)))
        obs.append(dict(key=key, kind="month", year=y_prev, month=mon,
                        value=m_prev, source=src, report="%04d-%02d" % (y_cur, mon)))
        if ytd_cur is not None:
            obs.append(dict(key=key, kind="ytd", year=y_cur, month=mon,
                            value=ytd_cur, source=src,
                            report="%04d-%02d" % (y_cur, mon)))
            obs.append(dict(key=key, kind="ytd", year=y_prev, month=mon,
                            value=ytd_prev, source=src,
                            report="%04d-%02d" % (y_cur, mon)))
        if inv is not None:
            obs.append(dict(key=key, kind="inventory", year=y_cur, month=mon,
                            value=inv, source=src,
                            report="%04d-%02d" % (y_cur, mon)))
    return obs


# --------------------------------------------------------------------- main

LIVE_EXTRA = [
    # current-month pre-release published on the AEM statistics landing page
    "https://www.aem.org/getattachment/6ac05a97-bb18-435f-b0bf-852ab21dc71f/"
    "July2026-Farm_Flash_Trade_Press_With_Chart_PreRelease-United-States.pdf",
]


def main():
    print("discovering Wayback captures ...", file=sys.stderr)
    wb = discover_wayback()
    print("  %d candidate archived PDFs" % len(wb), file=sys.stderr)

    jobs = [(u, ts) for u, ts in wb]
    for u in LIVE_EXTRA:
        jobs.append((u, None))
    # Live aem.org direct paths. Wayback already holds everything up to
    # 2025, so only the current year is worth guessing here -- probing the
    # whole 2021-2026 grid costs ~140 dead requests for no extra data.
    for y in (2026,):
        for m in range(1, 13):
            jobs.append(("https://www.aem.org/AEM/media/docs/Statistics/"
                         "US-Month-Ag-Report-%d-%d.pdf" % (m, y), None))
            jobs.append(("https://www.aem.org/AEM/media/docs/Statistics/"
                         "US-Month-Ag-Report-%02d-%d.pdf" % (m, y), None))

    uniq, seen_files = [], set()
    for url, ts in jobs:
        if (url, ts) in seen_files:
            continue
        seen_files.add((url, ts))
        uniq.append((url, ts))

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as ex:
        paths = list(ex.map(lambda j: (fetch_pdf(j[0], j[1]), j[0], j[1]), uniq))

    all_obs = []
    ok = 0
    for p, url, ts in paths:
        if not p:
            continue
        obs = observations_from_pdf(p, url, ts)
        if obs:
            ok += 1
            all_obs.extend(obs)
            print("  parsed %-70s -> %d obs" % (os.path.basename(p), len(obs)),
                  file=sys.stderr)

    print("parsed %d PDFs, %d raw observations" % (ok, len(all_obs)),
          file=sys.stderr)

    out = os.path.join(SCRATCH, "aem_raw_observations.json")
    with open(out, "w") as fh:
        json.dump(all_obs, fh, indent=1)
    print("wrote %s" % out)

    # quick coverage report
    cov = defaultdict(set)
    for o in all_obs:
        if o["kind"] == "month":
            cov[o["key"]].add((o["year"], o["month"]))
    for k in sorted(cov):
        ys = sorted({y for y, _ in cov[k]})
        print("  %-24s %d month-obs  %s..%s" % (k, len(cov[k]), ys[0], ys[-1]))


if __name__ == "__main__":
    main()
