#!/usr/bin/env python3
"""
fetch_sandhills_used_values.py

Crawls sandhills.com/news for the monthly "Sandhills Global market report"
press releases and extracts the USED FARM EQUIPMENT value / inventory trends.

Sandhills operates TractorHouse, Machinery Trader and Truck Paper and
publishes the Sandhills Equipment Value Index (EVI).  The *level* of the EVI
is a paid product; the free press releases quote month-over-month and
year-over-year percentage CHANGES in

    inventory levels, asking values, auction values

for named categories.  The categories relevant to Deere's Production &
Precision Ag franchise are:

    "U.S. Used High-Horsepower Tractors"   (100+ hp row-crop / 4WD)
    "U.S. Used Combines"
    "U.S. Used Compact and Utility Tractors"   (maps to Small Ag & Turf)
    "U.S. Used Farm Equipment" / "U.S. Used Tractors"  (older, broader wording)

Output is a JSON list of {year, month, category, metric, mom_pct, yoy_pct}.
Percentage CHANGES are the observable; no index level is invented here.

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
CACHE = os.environ.get("SH_CACHE", "/tmp/sandhills_cache")
os.makedirs(CACHE, exist_ok=True)

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MON_IDX = {m: i + 1 for i, m in enumerate(MONTHS)}
MONTH_RE = "|".join(MONTHS)

# Section heading -> canonical category. Longest/most specific first.
CATEGORIES = [
    ("U.S. Used High-Horsepower Tractors", "high_hp_tractors"),
    ("U.S. Used High Horsepower Tractors", "high_hp_tractors"),
    ("U.S. Used Combines", "combines"),
    ("U.S. Used Compact and Utility Tractors", "compact_utility_tractors"),
    ("U.S. Used Farm Equipment", "farm_equipment_all"),
    ("U.S. Used Tractors", "tractors_all"),
]

# every heading Sandhills uses, so a section can be terminated correctly
ANY_HEADING = re.compile(r"U\.S\. Used [A-Z]")

METRICS = [("Inventory levels", "inventory"),
           ("inventory levels", "inventory"),
           ("Asking values", "asking"),
           ("asking values", "asking"),
           ("Auction values", "auction"),
           ("auction values", "auction")]

PCT = r"(\d+(?:\.\d+)?)\s*%"
DOWN = ("decreas", "declin", "down", "fell", "fall", "drop", "dip", "slid",
        "lower", "loss", "shrank", "shrunk", "contract")
UP = ("increas", "rose", "rise", "gain", "grew", "grow", "climb", "higher",
      "bump", "jump", "surge", "up ", "rebound")


def get(url, name):
    p = os.path.join(CACHE, name)
    if os.path.exists(p) and os.path.getsize(p) > 2000:
        return open(p, encoding="utf-8", errors="replace").read()
    for attempt in range(3):
        r = subprocess.run(["curl", "-sSL", "--max-time", "45", "-A", UA, url],
                           capture_output=True)
        body = r.stdout.decode("utf-8", "replace")
        if len(body) > 2000:
            open(p, "w", encoding="utf-8").write(body)
            return body
        time.sleep(2 + 2 * attempt)
    return ""


def to_text(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    t = t.replace("—", " -- ").replace("–", "-")
    return re.sub(r"\s+", " ", t)


def sign_from(fragment):
    """Direction implied by the nearest directional word before the number."""
    f = fragment.lower()
    best, sign = -1, None
    for w in DOWN:
        i = f.rfind(w)
        if i > best:
            best, sign = i, -1.0
    for w in UP:
        i = f.rfind(w)
        if i > best:
            best, sign = i, 1.0
    return sign


def parse_section(seg):
    """Extract {metric: (mom, yoy)} from one category's prose block."""
    out = {}
    # locate each metric phrase inside the section
    hits = []
    for phrase, key in METRICS:
        for m in re.finditer(re.escape(phrase), seg):
            hits.append((m.start(), key))
    hits.sort()
    for idx, (pos, key) in enumerate(hits):
        if key in out:
            continue
        end = hits[idx + 1][0] if idx + 1 < len(hits) else len(seg)
        sub = seg[pos:min(end, pos + 500)]
        mom = yoy = None
        m = re.search(PCT + r"\s*(?:month over month|month-over-month|M/M)",
                      sub, re.I)
        if m:
            s = sign_from(sub[:m.start()])
            if s:
                mom = s * float(m.group(1))
        m = re.search(PCT + r"\s*(?:year over year|year-over-year|YOY|Y/Y|"
                      r"compared (?:with|to) (?:the same month |)"
                      r"(?:year-ago|last year|a year ago))", sub, re.I)
        if m:
            s = sign_from(sub[:m.start()]) or sign_from(sub)
            if s:
                yoy = s * float(m.group(1))
        if mom is not None or yoy is not None:
            out[key] = (mom, yoy)
    return out


def article_period(text):
    """(year, month) of the DATA the release covers."""
    pm = re.search(r"(%s)\s+(\d{1,2}),\s+(20\d\d)" % MONTH_RE, text)
    if not pm:
        return None, None
    pub_m, pub_y = MON_IDX[pm.group(1)], int(pm.group(3))
    m = re.search(r"cover(?:ing|s)\s+(%s)\s+data" % MONTH_RE, text)
    if not m:
        m = re.search(r"in\s+(%s)[,.]" % MONTH_RE, text)
    if m:
        dm = MON_IDX[m.group(1)]
    else:
        dm = pub_m - 1 or 12
    y = pub_y
    if dm > pub_m:
        y -= 1
    return y, dm


def parse_article(text, url):
    # The article body starts at the dateline "LINCOLN, Nebraska -- <date>".
    d = text.find("LINCOLN, Nebraska")
    body = text[d:] if d > 0 else text
    y, mo = article_period(body)
    if not y:
        return []
    # index every heading occurrence in the body
    marks = [(m.start(), m.group(0)) for m in
             re.finditer(r"U\.S\. Used [A-Za-z \-]{3,45}", body)]
    recs = []
    for i, (pos, head) in enumerate(marks):
        cat = None
        for label, c in CATEGORIES:
            if head.startswith(label):
                cat = c
                break
        if cat is None:
            continue
        end = marks[i + 1][0] if i + 1 < len(marks) else min(len(body),
                                                             pos + 2000)
        seg = body[pos:end]
        for metric, (mom, yoy) in parse_section(seg).items():
            recs.append(dict(year=y, month=mo, category=cat, metric=metric,
                             mom_pct=mom, yoy_pct=yoy, source=url))
    return recs


def main(out_json):
    ids = []
    for page in range(1, 30):
        h = get("https://www.sandhills.com/news?page=%d" % page,
                "list_%02d.html" % page)
        found = re.findall(r"/news/article/(\d+)", h)
        if not found:
            break
        n0 = len(ids)
        ids = sorted(set(ids) | set(found), key=int)
        if len(ids) == n0:
            break

    print("  %d articles indexed" % len(ids), file=sys.stderr)
    all_recs, seen = [], set()
    for aid in ids:
        url = "https://www.sandhills.com/news/article/%s" % aid
        h = get(url, "a_%s.html" % aid)
        if not h:
            continue
        t = to_text(h)
        if "Auction values" not in t and "auction values" not in t:
            continue
        for r in parse_article(t, url):
            k = (r["year"], r["month"], r["category"], r["metric"])
            if k in seen:
                continue
            seen.add(k)
            all_recs.append(r)

    all_recs.sort(key=lambda r: (r["category"], r["metric"], r["year"],
                                 r["month"]))
    with open(out_json, "w") as fh:
        json.dump(all_recs, fh, indent=1)

    import collections
    c = collections.Counter((r["category"], r["metric"]) for r in all_recs)
    for k, v in sorted(c.items()):
        yrs = sorted({(r["year"], r["month"]) for r in all_recs
                      if (r["category"], r["metric"]) == k})
        print("  %-26s %-10s n=%3d  %s..%s" % (k[0], k[1], v, yrs[0], yrs[-1]))
    print("wrote %d records -> %s" % (len(all_recs), out_json))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/sandhills.json")
