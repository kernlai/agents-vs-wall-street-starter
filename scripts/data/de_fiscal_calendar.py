#!/usr/bin/env python3
"""
Derive Deere's fiscal quarter-END dates from the 8-K press releases.

Deere runs a 52/53-week fiscal year ending on the Sunday closest to 31 Oct, so
quarter ends drift by up to a week. The dates matter here because the whole
question is which calendar months of raw-material purchasing feed a given
fiscal quarter's cost of sales -- an assumed calendar-quarter mapping would
smear the lag structure being measured.

Where the 8-K text does not yield a date, the quarter is left BLANK, not
interpolated.
"""
import re, os, glob, json, sys, argparse, datetime

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], 1)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out"); a = ap.parse_args()
    ends = {}
    for path in sorted(glob.glob(os.path.join(CORPUS, "filings", "*8k*.md"))):
        fn = os.path.basename(path)
        mq = re.search(r"-(q[1-4])-8k", fn)
        if not mq:
            continue
        q = int(mq.group(1)[1])
        pub = fn[:10]
        fy = int(pub[:4])
        txt = open(path, encoding="utf-8").read()
        idx = txt.find("Operating profit:")
        if idx < 0:
            idx = txt.find("Net sales and revenues")
        head = txt[max(0, idx - 2500): idx]
        # the column header rows carry the two period-end dates, current first
        cand = re.findall(r"\b(" + "|".join(MONTHS) + r")\s+(\d{1,2})\b", head)
        if not cand:
            continue
        mo, day = cand[0]
        # infer the calendar year: Q1 ends Jan/Feb of the fiscal year, Q2 Apr/May,
        # Q3 Jul/Aug, Q4 Oct/Nov -- all inside the same calendar year as the 8-K
        y = int(pub[:4])
        try:
            d = datetime.date(y, MONTHS[mo], int(day))
        except ValueError:
            continue
        pubd = datetime.date(*map(int, pub.split("-")))
        if not (0 < (pubd - d).days < 60):
            continue
        ends[f"{fy}Q{q}"] = d.isoformat()
    rows = dict(sorted(ends.items(), key=lambda kv: (int(kv[0][:4]), int(kv[0][-1]))))
    if a.out:
        open(a.out, "w").write(json.dumps(rows, indent=1))
    for k, v in rows.items():
        print(k, v, file=sys.stderr)
    print(f"n={len(rows)}", file=sys.stderr)


if __name__ == "__main__":
    main()
