#!/usr/bin/env python3
"""Download every Titan Machinery (TITN) earnings press release (8-K EX-99.1)
since 2018 and convert to plain text. TITN = CNH Industrial dealer, channel proxy.
"""
import json, re, html, os, sys, time, urllib.request

UA = 'Deere-dealer-research cor@salomo.io'
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'

def get(url, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req).read().decode('utf-8', 'replace')

def to_text(t):
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', t, flags=re.S | re.I)
    t = re.sub(r'</t[dh]>', '\t', t, flags=re.I)
    t = re.sub(r'</tr>', '\n', t, flags=re.I)
    t = re.sub(r'<(p|div|br|h\d)[^>]*>', '\n', t, flags=re.I)
    t = re.sub(r'<[^>]+>', '', t)
    t = html.unescape(t)
    t = re.sub(r'[ \xa0]+', ' ', t)
    return re.sub(r'\n\s*\n+', '\n', t)

sub = json.load(open(os.path.join(OUT, 'titn_sub.json')))
r = sub['filings']['recent']
accs = [(a, d) for f, d, a in zip(r['form'], r['filingDate'], r['accessionNumber'])
        if f == '8-K' and d >= '2018-01-01']

for acc, filed in accs:
    dest = os.path.join(OUT, f'rel_{filed}_{acc}.txt')
    if os.path.exists(dest):
        continue
    n = acc.replace('-', '')
    idx = get(f'https://www.sec.gov/Archives/edgar/data/1409171/{n}/')
    # earnings releases are EX-99.1 documents containing "earningsrelease"/"release" in the name
    cands = re.findall(r'href="(/Archives/edgar/data/1409171/[^"]*\.htm)"', idx)
    pick = [c for c in cands if re.search(r'(ex99|ex-99)', c, re.I)]
    if not pick:
        print('skip (no ex99):', acc, filed); time.sleep(0.2); continue
    body = to_text(get('https://www.sec.gov' + pick[0]))
    if 'Announces Results' not in body and 'Reports' not in body:
        print('skip (not earnings):', acc, filed, pick[0]); time.sleep(0.2); continue
    open(dest, 'w').write(body)
    print('saved', dest, len(body))
    time.sleep(0.25)
