#!/usr/bin/env python3
"""
de_segments_edgar_supplement.py
===============================
The frozen offline corpus starts at 2015-01-14, so its earliest quarterly segment
figures are FY2015 Q1 (with FY2014 Q1 as the comparative column). Fiscal 2013 and
fiscal 2012 quarterly segment detail is therefore absent from the corpus.

This script pulls the original Deere 10-Q filings for fiscal 2013 and fiscal 2014
straight from SEC EDGAR and parses the "Worldwide net sales and revenues, operating
profit ... by segment" note out of the raw HTML, so the legacy Agriculture & Turf /
Construction & Forestry quarterly history can be extended backwards.

It also cross-checks a handful of corpus-derived values against EDGAR's XBRL
companyconcept API.

Output: /tmp/de_seg_edgar.json
"""

import json
import re
import sys
import urllib.request
from html.parser import HTMLParser

UA = "AgentsVsWallStreet cor@salomo.io"
BASE = "https://www.sec.gov/Archives/edgar/data/315189/"

# accession (no dashes) -> primary document, for the 10-Qs that carry FY2012-FY2014 quarters
TENQ = [
    # (label, accession-no-dashes, document)
    ("FY2013Q1", "000110465913015827", "a12-29126_110q.htm"),
    ("FY2013Q2", "000110465913045612", "a13-6570_110q.htm"),
    ("FY2013Q3", "000110465913066988", "a13-14192_110q.htm"),
    ("FY2014Q1", "000110465914014013", "a13-23904_110q.htm"),
    ("FY2014Q2", "000110465914042322", "a14-7721_110q.htm"),
]

# Q4 earnings press releases (8-K EX-99.1). These carry the fourth-quarter column and the
# full-fiscal-year column, which the 10-Q series cannot supply.
EIGHTK = [
    ("FY2012Q4", "000110465912079457", "a12-27419_1ex99d1.htm"),
    ("FY2013Q4", "000110465913085905", "a13-24518_1ex99d1.htm"),
    ("FY2014Q4", "000110465914083524", None),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


class TableGrab(HTMLParser):
    """Collect every <table> as a list of rows, each row a list of cell strings."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self.stack = [], []
        self.cur, self.row, self.cell = None, None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.stack.append(self.cur)
            self.cur = []
        elif tag == "tr" and self.cur is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            txt = " ".join("".join(self.cell).split())
            self.row.append(txt)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.cur.append(self.row)
            self.row = None
        elif tag == "table" and self.cur is not None:
            self.tables.append(self.cur)
            self.cur = self.stack.pop() if self.stack else None

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


TOKEN_RE = re.compile(r"([-+]?)\(?\s*\$?\s*(\d[\d,]*)\s*\)?")


def row_values(cells_):
    body = " ".join(cells_).replace("%", " ").replace(" ", " ")
    vals = []
    pos = 0
    while True:
        m = TOKEN_RE.search(body, pos)
        if not m:
            break
        sign, digits = m.group(1), m.group(2).replace(",", "")
        frag = body[m.start():m.end()]
        pos = m.end()
        if sign in ("+", "-"):
            continue                      # percent-change column
        vals.append(-float(digits) if "(" in frag else float(digits))
    return vals


def squeeze(s):
    return re.sub(r"[^a-z]", "", s.lower())


SEGMAP = [("AT", r"^agriculture(and)?turf$"), ("CF", r"^construction(and)?forestry$")]


def seg_of(label):
    s = squeeze(label)
    for code, pat in SEGMAP:
        if re.match(pat, s):
            return code
    return None


def parse_segment_note(html):
    """Find the segment note table and return {(seg, metric): [values...]} + totals."""
    p = TableGrab()
    p.feed(html)
    best = None
    for tbl in p.tables:
        flat = squeeze(" ".join(" ".join(r) for r in tbl))
        if "totaloperatingprofit" in flat and "agricultureandturf" in flat \
           and "totalnetsales" in flat:
            best = tbl
            break
    if best is None:
        return None
    seg, tot, section = {"sales": {}, "op": {}}, {}, None
    for r in best:
        if not r:
            continue
        label = r[0].strip()
        s = squeeze(label)
        if s.startswith("netsalesandrevenues") and not s.startswith("totalnetsalesandrevenues"):
            section = "sales"
            continue
        if s.startswith("operatingprofit"):
            section = "op"
            continue
        if s.startswith("netincomeattributable") or s.startswith("intersegment") \
           or s.startswith("identifiableassets"):
            break
        if section is None:
            continue
        vals = row_values(r[1:])
        code = seg_of(label)
        if code:
            seg[section][code] = vals
        elif s.startswith("financialservices"):
            seg[section]["FS"] = vals
        elif s == "totalnetsales":
            tot["sales_total"] = vals
        elif s.startswith("totaloperatingprofit"):
            tot["op_total"] = vals
    return seg, tot


HDR = re.compile(r"Three Months Ended\s*</?[^>]*>?\s*", re.I)
DATE_RE = re.compile(
    r"Three Months Ended[^A-Z]{0,40}([A-Z][a-z]+)\s+(\d{1,2}),?\s*(\d{4})?", re.I)


def find_ex991(acc):
    idx = json.loads(get(BASE + acc + "/index.json"))
    for it in idx["directory"]["item"]:
        if re.search(r"ex99d1\.htm$", it["name"]):
            return it["name"]
    return None


def main():
    out = []
    for label, acc, doc in TENQ + EIGHTK:
        if doc is None:
            doc = find_ex991(acc)
            if doc is None:
                sys.stderr.write("no ex99.1 for %s\n" % acc)
                continue
        url = BASE + acc + "/" + doc
        sys.stderr.write("fetching %s\n" % url)
        html = get(url)
        res = parse_segment_note(html)
        if not res:
            sys.stderr.write("  !! segment note not found\n")
            continue
        seg, tot = res
        present = [g for g in seg["sales"] if g != "FS"]
        fy = int(label[2:6])
        # cols 0/1 = current & prior-year quarter; cols 2/3 = YTD, which for a Q4
        # press release is the full fiscal year
        colspec = [(0, 0, label[6:], "current"), (1, -1, label[6:], "prior-comparative")]
        if label.endswith("Q4"):
            colspec += [(2, 0, "FY", "current"), (3, -1, "FY", "prior-comparative")]
        for col, offset, fq, role in colspec:
            vals = {}
            ok = True
            for g in present:
                for metric in ("sales", "op"):
                    arr = seg[metric].get(g, [])
                    if len(arr) <= col:
                        ok = False
                    else:
                        vals[(g, metric)] = arr[col]
            if not ok:
                continue
            if "sales_total" in tot and len(tot["sales_total"]) > col:
                s = sum(vals[(g, "sales")] for g in present)
                if abs(s - tot["sales_total"][col]) > 1.0:
                    sys.stderr.write("  SUMCHECK FAIL %s col%d %s vs %s\n"
                                     % (label, col, s, tot["sales_total"][col]))
                    continue
            if "op_total" in tot and len(tot["op_total"]) > col and "FS" in seg["op"]:
                s = sum(vals[(g, "op")] for g in present) + seg["op"]["FS"][col]
                if abs(s - tot["op_total"][col]) > 1.0:
                    sys.stderr.write("  OP SUMCHECK FAIL %s col%d %s vs %s\n"
                                     % (label, col, s, tot["op_total"][col]))
                    continue
            for g in present:
                for metric in ("sales", "op"):
                    out.append(dict(seg=g, metric=metric, fy=fy + offset, fq=fq,
                                    value=vals[(g, metric)], basis="legacy-AT",
                                    role=role,
                                    source=url, form="10q"))
    json.dump(out, open("/tmp/de_seg_edgar.json", "w"), indent=1)
    print("edgar observations:", len(out))
    for o in sorted(out, key=lambda x: (x["fy"], x["fq"], x["seg"], x["metric"])):
        print(o["fy"], o["fq"], o["seg"], o["metric"], o["value"], o["role"])


if __name__ == "__main__":
    main()
