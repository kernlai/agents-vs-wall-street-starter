#!/usr/bin/env python3
"""Snapshot Deere's external careers board (Eightfold PCSX) by location + department.

Endpoint discovered 2026-08-16: https://careers.deere.com/api/pcsx/search?domain=johndeere.com
robots.txt explicitly Allows /api/pcsx. Output: raw JSON + a tidy summary.
Re-run this on a schedule to build the time series the one-off snapshot lacks.
"""
import json, subprocess, sys, time, collections, datetime, os

BASE = "https://careers.deere.com/api/pcsx/search?domain=johndeere.com&start={start}&num={num}&sort_by=timestamp"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/private/tmp/deere_jobs.json"

def get(url):
    r = subprocess.run(["curl","-s","-m","60",url,
        "-H","User-Agent: Mozilla/5.0","-H","Referer: https://careers.deere.com/careers"],
        capture_output=True, text=True)
    return json.loads(r.stdout)

positions, start, num = [], 0, 10  # API caps page size at 10
while True:
    d = get(BASE.format(start=start, num=num))
    data = d["data"]
    total = data["count"]
    batch = data["positions"]
    if not batch: break
    positions.extend(batch)
    start += num
    if start >= total: break
    time.sleep(1)

json.dump({"fetched_utc": datetime.datetime.utcnow().isoformat()+"Z",
           "total": total, "positions": positions}, open(OUT,"w"), ensure_ascii=False, indent=1)
print("total reported:", total, "fetched:", len(positions), "->", OUT)
