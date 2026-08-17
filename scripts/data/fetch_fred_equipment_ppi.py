#!/usr/bin/env python3
"""
fetch_fred_equipment_ppi.py

Pulls farm-machinery price indices from FRED's keyless CSV endpoint and writes
them as tidy-long rows.  Two independent BLS programmes are pulled so they can
be cross-checked against each other:

  PCU333111333111  PPI by Industry: Farm Machinery and Equipment Manufacturing
                   (NAICS 333111, industry-net-output basis, 1982-06 = 100)
  WPU111           PPI by Commodity: Machinery and Equipment:
                   Agricultural Machinery and Equipment (commodity basis)
  PCU333111333111A PPI by Industry 333111: primary products
  IPG33311S        Industrial Production: Agriculture, Construction and Mining
                   Machinery (NAICS 3331) -- a real-volume cross-check

Standard library only.
"""

import csv
import io
import os
import sys
import urllib.request

UA = "AgentsVsWallStreet cor@salomo.io"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s"

SERIES = {
    "PCU333111333111": dict(
        series_id="us_ag_equipment_ppi", units="index",
        note="PPI by Industry: Farm Machinery and Equipment Manufacturing "
             "(NAICS 333111), index 1982-06=100, NSA, monthly. PRIMARY."),
    "WPU111": dict(
        series_id="us_ag_equipment_ppi_commodity", units="index",
        note="PPI by Commodity: Agricultural Machinery and Equipment "
             "(WPU111), index 1982=100, NSA, monthly. Independent "
             "cross-check on the industry-basis series."),
    "PCU333111333111A": dict(
        series_id="us_ag_equipment_ppi_primary_products", units="index",
        note="PPI by Industry 333111: primary products only, index "
             "Dec-1975=100. Narrower basket than the headline industry index."),
    "IPG33311S": dict(
        series_id="us_ag_constr_mining_machinery_ip", units="index",
        note="Industrial Production: Agriculture, Construction and Mining "
             "Machinery (NAICS 3331), index 2017=100, SA, monthly. Real "
             "output volume cross-check; NOT price."),
}

START = "2005-01-01"


def fetch(sid):
    req = urllib.request.Request(FRED % sid, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def main(out_path):
    rows = []
    for sid, meta in SERIES.items():
        try:
            txt = fetch(sid)
        except Exception as e:  # noqa: BLE001
            print("FAILED %s: %s" % (sid, e), file=sys.stderr)
            continue
        rdr = csv.reader(io.StringIO(txt))
        hdr = next(rdr)
        if hdr[0] != "observation_date":
            print("unexpected header for %s: %r" % (sid, hdr), file=sys.stderr)
            continue
        n = 0
        for r in rdr:
            if len(r) < 2 or not r[1].strip() or r[1].strip() == ".":
                continue
            d = r[0]
            if d < START:
                continue
            # FRED stamps monthly obs on the 1st; convert to period END
            y, m, _ = (int(x) for x in d.split("-"))
            if m == 12:
                nxt = "%04d-01-01" % (y + 1)
            else:
                nxt = "%04d-%02d-01" % (y, m + 1)
            import datetime as dt
            end = (dt.date(*[int(x) for x in nxt.split("-")]) -
                   dt.timedelta(days=1)).isoformat()
            q = "Q%d" % ((m - 1) // 3 + 1)
            rows.append([meta["series_id"], end, y, q, r[1].strip(),
                         meta["units"], "api", FRED % sid, meta["note"]])
            n += 1
        print("%-18s %5d obs from %s" % (sid, n, START), file=sys.stderr)

    rows.sort(key=lambda r: (r[0], r[1]))
    with open(out_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["series_id", "period_end", "fiscal_year", "fiscal_quarter",
                    "value", "units", "source_type", "source", "notes"])
        w.writerows(rows)
    print("wrote %d rows -> %s" % (len(rows), out_path))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/fred_ppi.csv")
