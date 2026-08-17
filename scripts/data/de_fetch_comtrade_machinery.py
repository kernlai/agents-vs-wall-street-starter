#!/usr/bin/env python3
"""
Fetch agricultural / construction machinery trade flows from the UN Comtrade
public preview API, for the Deere (NYSE: DE) manufacturing-footprint work.

HS codes:
  8432  agricultural / horticultural / forestry soil-prep machinery (planters, seeders, tillage)
  8433  harvesting & threshing machinery (combines, forage harvesters, mowers)
  8701  tractors
  8429  self-propelled construction equipment (dozers, graders, scrapers, excavators, loaders)

Reporters: USA (842), Brazil (76), India (699).

The public preview endpoint accepts exactly ONE period per request and is
intermittently rate limited, so every request is retried with backoff and the
raw JSON is cached on disk. Re-running the script is cheap and idempotent.

Output: newline-delimited JSON of flattened records to --out.
No API key required (public preview tier).
"""

import argparse
import hashlib
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor

BASE = "https://comtradeapi.un.org/public/v1/preview/C"

# The public tier enforces an hourly CALL VOLUME quota, and a rejected 429 still
# spends quota. So the winning strategy is to never trigger a 429: pace requests
# globally rather than racing and retrying. _PACER serialises the spacing.
_PACE_LOCK = threading.Lock()
_LAST_CALL = [0.0]


def pace(min_interval):
    if min_interval <= 0:
        return
    with _PACE_LOCK:
        wait = _LAST_CALL[0] + min_interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _LAST_CALL[0] = time.monotonic()
UA = "deere-footprint-research/1.0 (contact: cor@salomo.io)"

HS_CODES = ["8432", "8433", "8701", "8429"]

# Comtrade M49 reporter/partner codes
REPORTERS = {"USA": 842, "Brazil": 76, "India": 699}
WORLD = 0


class QuotaExhausted(Exception):
    def __init__(self, retry_after=None):
        super().__init__("comtrade hourly call quota exhausted")
        self.retry_after = retry_after


def cache_path(cache_dir, url):
    h = hashlib.sha1(url.encode()).hexdigest()[:20]
    return os.path.join(cache_dir, h + ".json")


def fetch(url, cache_dir, tries=25, cache_only=False, min_interval=0.0):
    """GET with disk cache + retry. Returns parsed dict or None.

    The public preview tier throttles hard (HTTP 429) but the window clears in
    about a second, so retry with a short, near-flat sleep rather than
    exponential backoff -- exponential backoff turns a 1s limit into minutes of
    idle waiting and drags the whole run out by an order of magnitude.
    """
    cp = cache_path(cache_dir, url)
    if os.path.exists(cp):
        try:
            with open(cp) as f:
                return json.load(f)
        except Exception:
            pass  # corrupt cache entry, refetch

    if cache_only:
        return None

    for attempt in range(tries):
        pace(min_interval)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8")
            data = json.loads(body)
            # A successful preview response always carries a "data" list.
            if isinstance(data, dict) and isinstance(data.get("data"), list):
                with open(cp, "w") as f:
                    json.dump(data, f)
                return data
            # Structured error (e.g. "Maximum number of periods for preview is 1")
            if isinstance(data, dict) and data.get("error"):
                sys.stderr.write("ERR %s :: %s\n" % (data["error"], url))
                return None
        except urllib.error.HTTPError as e:
            if e.code == 403:
                # "Out of call volume quota" - retrying only wastes wall clock.
                retry_after = e.headers.get("Retry-After") if e.headers else None
                sys.stderr.write("QUOTA EXHAUSTED (403), Retry-After=%s :: %s\n"
                                 % (retry_after, url))
                raise QuotaExhausted(retry_after)
            if e.code == 429:
                time.sleep(0.8 + 0.8 * random.random())
                continue
            time.sleep(1.5 + random.random())
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
            time.sleep(1.5 + random.random())
    sys.stderr.write("FAIL after %d tries :: %s\n" % (tries, url))
    return None


def build_urls(args):
    """Yield (meta, url) jobs, HIGHEST VALUE FIRST.

    The public tier throttles to roughly 15 successful requests a minute, so job
    order is the real budget decision: if the run is cut short, whatever ran
    first is what we keep. Annual partner detail is one request per year per
    code and carries the destination breakdown, so it goes first; the monthly
    world series is the bulk of the calls and goes second, newest years first so
    the quarters that matter for the current forecast land early.
    """
    jobs = []
    only = args.only

    # --- 1. US annual, full partner breakdown: destination detail (cheap) ---
    for code in (HS_CODES if only in ("all", "annual") else []):
        for year in args.years:
            jobs.append((
                {"reporter": "USA", "freq": "A", "hs": code, "period": str(year), "scope": "partners"},
                f"{BASE}/A/HS?reporterCode=842&period={year}&cmdCode={code}&flowCode=X",
            ))

    # --- 2. US monthly, world total: the high-frequency series -------------
    # Newest first: the recent quarters drive the live forecast.
    for period in (sorted(args.months, reverse=True) if only in ("all", "monthly") else []):
        for code in HS_CODES:
            jobs.append((
                {"reporter": "USA", "freq": "M", "hs": code, "period": period, "scope": "world"},
                f"{BASE}/M/HS?reporterCode=842&period={period}&partnerCode={WORLD}"
                f"&cmdCode={code}&flowCode=X",
            ))

    # --- 3. Brazil & India annual, world total, both directions ------------
    # Shorter window than the US series: these are context, not the core signal.
    for name, rc in ((("Brazil", 76), ("India", 699)) if only in ("all", "foreign") else ()):
        for code in HS_CODES:
            for year in [y for y in args.years if y >= args.foreign_start_year]:
                for flow in ("X", "M"):
                    jobs.append((
                        {"reporter": name, "freq": "A", "hs": code, "period": str(year),
                         "scope": "world", "flow": flow},
                        f"{BASE}/A/HS?reporterCode={rc}&period={year}&partnerCode={WORLD}"
                        f"&cmdCode={code}&flowCode={flow}",
                    ))

    return jobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--start-year", type=int, default=2012)
    ap.add_argument("--end-year", type=int, default=2026)
    ap.add_argument("--foreign-start-year", type=int, default=2016,
                    help="first year for the Brazil/India annual series")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", choices=["all", "annual", "monthly", "foreign"], default="all",
                    help="restrict which block of series to fetch, so a limited quota "
                         "window can be spent deliberately")
    ap.add_argument("--min-interval", type=float, default=0.0,
                    help="minimum seconds between requests, globally across workers; "
                         "set this at or below the hourly quota rate to avoid 429s, "
                         "which themselves consume quota")
    ap.add_argument("--cache-only", action="store_true",
                    help="build output from the disk cache only, make no network calls "
                         "(the Comtrade public tier has a hard hourly call quota)")
    args = ap.parse_args()

    os.makedirs(args.cache, exist_ok=True)
    args.years = list(range(args.start_year, args.end_year + 1))
    args.months = [
        f"{y}{m:02d}"
        for y in range(args.start_year, args.end_year + 1)
        for m in range(1, 13)
    ]

    jobs = build_urls(args)
    sys.stderr.write("jobs: %d\n" % len(jobs))

    rows = []
    done = [0]

    def run(job):
        meta, url = job
        try:
            data = fetch(url, args.cache, cache_only=args.cache_only,
                         min_interval=args.min_interval)
        except QuotaExhausted:
            return []
        done[0] += 1
        if done[0] % 100 == 0:
            sys.stderr.write("  %d/%d\n" % (done[0], len(jobs)))
        if not data:
            return []
        out = []
        for r in data.get("data", []):
            out.append({
                "reporter": meta["reporter"],
                "reporterCode": r.get("reporterCode"),
                "freq": r.get("freqCode"),
                "period": r.get("period"),
                "flow": r.get("flowCode"),
                "hs": r.get("cmdCode"),
                "partnerCode": r.get("partnerCode"),
                "value_usd": r.get("primaryValue"),
                "netWgt_kg": r.get("netWgt"),
                "isReported": r.get("isReported"),
                "isAggregate": r.get("isAggregate"),
                # Discriminators. Some reporters (Brazil, India) return the same
                # reporter/partner/period/commodity several times, split by customs
                # procedure, mode of transport and second partner. Dropping these
                # fields silently multiplies rows and lets a partial breakdown be
                # mistaken for the total, so they must be carried through and the
                # true aggregate selected downstream (C00 / mot 0 / mos 0 / p2 0).
                "customsCode": r.get("customsCode"),
                "motCode": r.get("motCode"),
                "mosCode": r.get("mosCode"),
                "partner2Code": r.get("partner2Code"),
                "scope": meta["scope"],
            })
        return out

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for res in ex.map(run, jobs):
            rows.extend(res)

    with open(args.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    sys.stderr.write("wrote %d rows -> %s\n" % (len(rows), args.out))


if __name__ == "__main__":
    main()
