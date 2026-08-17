#!/usr/bin/env python3
"""How much do the public dealer proxies actually track Deere's reported revenue?
Pairs each proxy's y/y growth with Deere's y/y total net sales & revenues growth for
the nearest-ending fiscal quarter (within 45 days), then reports Pearson r WITH n.
Small n and overlapping-window autocorrelation are flagged in the output.
"""
import json, csv, sys, datetime as dt, math
from collections import defaultdict

SCRATCH = sys.argv[1]

def load_de():
    d = json.load(open(f'{SCRATCH}/de_rev2.json'))
    out = {}
    for x in d['units']['USD']:
        if not x.get('start'): continue
        n = (dt.date.fromisoformat(x['end']) - dt.date.fromisoformat(x['start'])).days
        if not 80 <= n <= 100: continue
        if x['end'] not in out or x['filed'] > out[x['end']]['filed']:
            out[x['end']] = x
    return {k: v['val'] for k, v in out.items()}

def yoy(series):
    """y/y % change, matching each period end to the one ~365 days earlier."""
    ends = sorted(series)
    out = {}
    for e in ends:
        d = dt.date.fromisoformat(e)
        cand = [p for p in ends if 340 <= (d - dt.date.fromisoformat(p)).days <= 390]
        if cand:
            prev = series[cand[-1]]
            if prev: out[e] = 100.0 * (series[e] - prev) / prev
    return out

def pearson(xs, ys):
    n = len(xs)
    if n < 3: return None
    mx, my = sum(xs)/n, sum(ys)/n
    sxy = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
    sxx = sum((a-mx)**2 for a in xs); syy = sum((b-my)**2 for b in ys)
    if sxx == 0 or syy == 0: return None
    return sxy / math.sqrt(sxx*syy)

def align(a, b, lag_q=0, tol=45):
    """Pair a[t] with b at the period end nearest t shifted by lag_q quarters.
    lag_q>0 means the proxy LEADS Deere (proxy at t vs Deere at t+lag)."""
    xs, ys, pairs = [], [], []
    for ea, va in sorted(a.items()):
        target = dt.date.fromisoformat(ea) + dt.timedelta(days=91*lag_q)
        best = min(b, key=lambda eb: abs((dt.date.fromisoformat(eb)-target).days), default=None)
        if best is None: continue
        if abs((dt.date.fromisoformat(best)-target).days) > tol: continue
        xs.append(va); ys.append(b[best]); pairs.append((ea, best))
    return xs, ys, pairs

de = load_de(); de_y = yoy(de)

rows = list(csv.DictReader(open('/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/dealer_proxies.csv')))
S = defaultdict(dict)
for r in rows:
    S[(r['entity'].split(' (')[0], r['metric'])][r['period_end']] = float(r['value'])

tests = [
 ('TITN total revenue y/y',        yoy(S[('Titan Machinery','revenue')])),
 ('TITN Agriculture segment revenue y/y', yoy(S[('Titan Machinery','segment_revenue_agriculture')])),
 ('TITN equipment revenue y/y',    yoy(S[('Titan Machinery','revenue_equipment')])),
 ('TITN parts revenue y/y',        yoy(S[('Titan Machinery','revenue_parts')])),
 ('TITN total inventory y/y',      yoy(S[('Titan Machinery','inventory_total')])),
 ('TITN equipment inv turns TTM (level)', S[('Titan Machinery','equipment_inventory_turns_ttm')]),
 ('TITN equipment gross margin % (level)', S[('Titan Machinery','gross_margin_equipment_pct')]),
 ('TITN Ag same-store sales %',    S[('Titan Machinery','same_store_sales_agriculture_pct')]),
 ('TSCO comparable store sales %', S[('Tractor Supply','comparable_store_sales_pct')]),
 ('TSCO revenue y/y',              yoy(S[('Tractor Supply','revenue')])),
]

print(f'{"proxy":<42} {"lag":>4} {"n":>4} {"r":>7}   window')
print('-'*95)
for name, ser in tests:
    for lag in (0, 1, 2):
        xs, ys, pr = align(ser, de_y, lag)
        r = pearson(xs, ys)
        if r is None:
            print(f'{name:<42} {lag:>4} {len(xs):>4} {"n/a":>7}   insufficient overlap'); continue
        w = f'{pr[0][0]}..{pr[-1][0]}'
        flag = '  <-- n<8, treat as anecdote' if len(xs) < 8 else ''
        print(f'{name:<42} {lag:>4} {len(xs):>4} {r:>7.2f}   {w}{flag}')
    print()
