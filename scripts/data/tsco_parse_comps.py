#!/usr/bin/env python3
"""Parse TSCO quarterly comparable-store-sales, transactions and ticket from 8-K text."""
import re, glob, os, sys, csv, datetime as dt
M = {m:i for i,m in enumerate(['January','February','March','April','May','June','July',
     'August','September','October','November','December'],1)}

def parse(p):
    t = open(p).read()
    m = re.search(r'(?:first|second|third|fourth) quarter (?:and (?:fiscal )?year )?ended (\w+) (\d{1,2}), (\d{4})', t)
    if not m: return None
    pe = dt.date(int(m.group(3)), M[m.group(1)], int(m.group(2))).isoformat()
    r = {'period_end': pe, 'source': os.path.basename(p)}
    m = re.search(r'Comparable store sales (increase|decrease)d? ([\d.]+)%', t)
    if m: r['comp_sales_pct'] = float(m.group(2)) * (-1 if m.group(1)=='decrease' else 1)
    m = re.search(r'[Cc]omparable (?:average )?transactions? (increase|decrease) of ([\d.]+)%', t) or \
        re.search(r'comparable transaction count (increase|decrease) of ([\d.]+)%', t) or \
        re.search(r'transaction count (?:decline|increase|decrease) of ([\d.]+)%', t)
    if m:
        g = m.groups()
        if len(g)==2: r['comp_transactions_pct'] = float(g[1])*(-1 if g[0]=='decrease' else 1)
    m = re.search(r'comparable average ticket (increase|decrease) of ([\d.]+)%', t)
    if m: r['comp_ticket_pct'] = float(m.group(2))*(-1 if m.group(1)=='decrease' else 1)
    m = re.search(r'[Nn]et sales (?:increased|decreased) [\d.]+% to \$([\d.]+) billion', t)
    if m: r['net_sales_busd'] = float(m.group(1))
    return r

def main(indir, out):
    recs = [x for x in (parse(p) for p in sorted(glob.glob(os.path.join(indir,'tsco_2*.txt')))) if x]
    recs.sort(key=lambda x: x['period_end'])
    cols = []
    for r in recs:
        for k in r:
            if k not in cols: cols.append(k)
    with open(out,'w',newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for r in recs: w.writerow(r)
    for r in recs: print(r)
    print(len(recs),'->',out)

if __name__=='__main__': main(sys.argv[1], sys.argv[2])
