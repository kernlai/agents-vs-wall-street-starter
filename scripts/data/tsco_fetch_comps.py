#!/usr/bin/env python3
"""Pull Tractor Supply (TSCO) comparable-store-sales and transaction/ticket metrics
from quarterly earnings 8-K exhibits. TSCO is a RURAL-LIFESTYLE RETAILER, not an
equipment dealer -- farmer/rural discretionary spending proxy only.
"""
import json, re, html, os, sys, time, urllib.request
UA = 'Deere-dealer-research cor@salomo.io'
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'

def get(u):
    return urllib.request.urlopen(
        urllib.request.Request(u, headers={'User-Agent': UA})).read().decode('utf-8','replace')

def to_text(t):
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>','',t,flags=re.S|re.I)
    t = re.sub(r'</t[dh]>','\t',t,flags=re.I); t = re.sub(r'</tr>','\n',t,flags=re.I)
    t = re.sub(r'<(p|div|br|h\d)[^>]*>','\n',t,flags=re.I)
    t = re.sub(r'<[^>]+>','',t); t = html.unescape(t)
    t = re.sub(r'[ \xa0]+',' ',t); return re.sub(r'\n\s*\n+','\n',t)

sub = json.load(open(os.path.join(OUT,'tsco_sub.json')))
r = sub['filings']['recent']
accs = [(a,d) for f,d,a in zip(r['form'],r['filingDate'],r['accessionNumber'])
        if f=='8-K' and d >= '2023-01-01']
for acc, filed in accs:
    dest = os.path.join(OUT, f'tsco_{filed}_{acc}.txt')
    if os.path.exists(dest): continue
    n = acc.replace('-','')
    idx = get(f'https://www.sec.gov/Archives/edgar/data/916365/{n}/')
    pick = [c for c in re.findall(r'href="(/Archives/edgar/data/916365/[^"]*\.htm)"', idx)
            if re.search(r'(ex99|ex-99)', c, re.I)]
    if not pick: time.sleep(0.2); continue
    body = to_text(get('https://www.sec.gov'+pick[0]))
    if 'omparable store sales' not in body: time.sleep(0.2); continue
    open(dest,'w').write(body); print('saved', dest); time.sleep(0.25)
