"""Adds (a) dealer TRADE receivable series, (b) quarterly net sales & revenues,
to the dealer-credit-quality dataset, and computes lead/lag correlations."""
import json,re,os,datetime,csv
import pandas as pd
SC="/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"
CORPUSDIR="/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"
CORPUSREL="challenge/offline-data/deere/filings/"
FIXDATE={'2016-10-31':'2016-10-30','2015-11-01':'2015-10-31','2016-05-01':'2016-04-30',
         '2017-10-30':'2017-10-29','2020-11-02':'2020-11-01'}
recs=[]
def fiscal(dt):
    y,m,dd=[int(x) for x in dt.split('-')]
    if m in (1,2): return (y,1)
    if m in (4,5): return (y,2)
    if m in (7,8): return (y,3)
    if m in (10,11): return (y+1,4)
    return (None,None)
def add(sid,pe,entity,metric,value,units,stype,src,notes=''):
    pe=FIXDATE.get(pe,pe)
    fy,fq=fiscal(pe)
    recs.append(dict(series_id=sid,period_end=pe,fiscal_year=fy,fiscal_quarter=fq,entity=entity,metric=metric,
                     value=value,units=units,source_type=stype,source=src,notes=notes))

# ---------- 1. trade accounts & notes receivable - net (owed mostly by dealers) ----------
cf=json.load(open(os.path.join(SC,'cf.json')))['facts']['us-gaap']
tr={}
for tag in ('AccountsAndNotesReceivableNet','AccountsReceivableNet'):
    for x in cf.get(tag,{}).get('units',{}).get('USD',[]):
        if 'start' in x: continue
        if x['form'] not in ('10-Q','10-K'): continue
        tr.setdefault(x['end'],[]).append((x['filed'],x['val'],tag,x['accn']))
for end,v in sorted(tr.items()):
    if end<'2014-10-01': continue
    filed,val,tag,accn=sorted(v)[0]
    add('de_trade_receivables_net',end,'dealer','trade accounts and notes receivable - net (equipment ops; arise from sales of goods to independent dealers)',
        round(val/1e6,1),'USD_millions','filing',f'SEC EDGAR XBRL companyfacts us-gaap:{tag}, DE CIK 315189, accn {accn}',
        '10-Q verified language: "Trade accounts and notes receivable primarily arise from sales of goods to independent dealers."')

# ---------- 2. % of trade receivables outstanding > 12 months ----------
MON={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
pat=re.compile(r'(?:percentage of (?:total worldwide )?trade receivables outstanding for (?:a )?periods? exceeding 12 months was )(.{0,400}?)\.',re.I)
val_at=re.compile(r'(\d+)\s*(?:percent|%)(.{0,120}?)(?=(?:\d+\s*(?:percent|%))|$)',re.I)
date_re=re.compile(r'([A-Z][a-z]+)\s+(\d{1,2}),\s*(\d{4})')
found={}
for fn in sorted(os.listdir(CORPUSDIR)):
    t=open(os.path.join(CORPUSDIR,fn),encoding='utf-8').read().replace('​','')
    t=re.sub(r'<!--.*?-->',' ',t); t=re.sub(r'\s+',' ',t)
    for m in pat.finditer(t):
        seg=m.group(1)
        # "1 percent at A, B and C" -> same value for all listed dates
        chunks=[]
        for vm in val_at.finditer(seg): chunks.append((int(vm.group(1)),vm.group(2)))
        if not chunks: continue
        if 'respectively' in seg.lower():
            # form: "was 1 percent, 1 percent, and 3 percent at A, B, and C, respectively"
            vals=[int(x) for x in re.findall(r'(\d+)\s*(?:percent|%)',seg)]
            dts=[]
            for dm in date_re.finditer(seg):
                mo=MON.get(dm.group(1))
                if mo: dts.append("%s-%02d-%02d"%(dm.group(3),mo,int(dm.group(2))))
            if len(vals)==len(dts) and vals:
                for v,dt in zip(vals,dts): found.setdefault(dt,(v,fn))
                continue
        if len(chunks)==1:
            v,tail=chunks[0]
            for dm in date_re.finditer(tail):
                mo=MON.get(dm.group(1));
                if mo: found.setdefault("%s-%02d-%02d"%(dm.group(3),mo,int(dm.group(2))),(v,fn))
        else:
            for v,tail in chunks:
                dm=date_re.search(tail)
                if not dm: continue
                mo=MON.get(dm.group(1))
                if mo: found.setdefault("%s-%02d-%02d"%(dm.group(3),mo,int(dm.group(2))),(v,fn))
# 10-K bullet form ("6 percent of receivables were outstanding for periods exceeding 12 months")
KBUL={'2024-10-27':(6,'2024-11-21__de-us-20241121-q4-10k__105810.md'),
      '2025-11-02':(3,'2025-12-18__de-us-20251218-fy-10k__393777.md')}
for k,v in KBUL.items(): found.setdefault(k,v)
for dt,(v,fn) in sorted(found.items()):
    if dt<'2014-10-01': continue
    add('de_trade_receivables_pct_over_12m',dt,'dealer','% of worldwide trade receivables outstanding longer than 12 months',
        float(v),'percent','filing',CORPUSREL+fn,'direct aging of trade credit Deere extends to its own dealers')

# ---------- 3. trade receivables / trailing-12m net sales (disclosed through FY2021) ----------
pat2=re.compile(r'ratios? of worldwide trade accounts and notes receivable to the last 12 months.{0,3} net sales were (.{0,300}?)\.',re.I)
f2={}
for fn in sorted(os.listdir(CORPUSDIR)):
    t=open(os.path.join(CORPUSDIR,fn),encoding='utf-8').read().replace('​','')
    t=re.sub(r'\s+',' ',t)
    for m in pat2.finditer(t):
        seg=m.group(1)
        for vm in val_at.finditer(seg):
            v=int(vm.group(1)); dm=date_re.search(vm.group(2))
            if not dm: continue
            mo=MON.get(dm.group(1))
            if mo: f2.setdefault("%s-%02d-%02d"%(dm.group(3),mo,int(dm.group(2))),(v,fn))
for dt,(v,fn) in sorted(f2.items()):
    if dt<'2014-10-01': continue
    add('de_trade_receivables_to_ttm_sales_pct',dt,'dealer','worldwide trade accounts & notes receivable / last-12-months net sales',
        float(v),'percent','filing',CORPUSREL+fn,'disclosure discontinued after FY2021')

# ---------- 4. quarterly net sales & revenues ----------
rev={}
for x in cf['Revenues']['units']['USD']:
    if 'start' not in x: continue
    d0=datetime.date.fromisoformat(x['start']); d1=datetime.date.fromisoformat(x['end'])
    n=(d1-d0).days
    key=(x['end'],'Q' if n<110 else ('FY' if n>330 else ('H1' if n<200 else '9M')))
    rev.setdefault(key,[]).append((x['filed'],x['val'],x['accn']))
qs={}
for (end,kind),v in rev.items():
    filed,val,accn=sorted(v)[0]
    qs[(end,kind)]=(val,accn)
for (end,kind),(val,accn) in sorted(qs.items()):
    if kind!='Q' or end<'2014-10-01': continue
    add('de_net_sales_and_revenues',end,'company','worldwide net sales and revenues (fiscal quarter)',round(val/1e6,1),
        'USD_millions','filing',f'SEC EDGAR XBRL companyfacts us-gaap:Revenues, accn {accn}')
# Q4 = FY minus 9M
fy={e:v for (e,k),v in qs.items() if k=='FY'}
nm={e:v for (e,k),v in qs.items() if k=='9M'}
def prior_9m(end):
    y=int(end[:4]); cands=[e for e in nm if e[:4]==str(y) and e<end]
    return max(cands) if cands else None
for e,(val,accn) in sorted(fy.items()):
    if e<'2014-10-01': continue
    p=prior_9m(e)
    if not p: continue
    q4=val-nm[p][0]
    add('de_net_sales_and_revenues',e,'company','worldwide net sales and revenues (fiscal Q4, derived FY minus 9M)',
        round(q4/1e6,1),'USD_millions','derived',f'SEC EDGAR XBRL companyfacts us-gaap:Revenues, accn {accn}','FY less nine-month figure')

pd.DataFrame(recs).drop_duplicates(['series_id','period_end'],keep='first').to_csv(os.path.join(SC,'stage2.csv'),index=False)
print(len(recs))

# ---------- 5. dealer sales incentives with right of set-off against trade receivables ----------
import re as _re
recs2=[]
pat3=_re.compile(r'dealer sales incentives with a right of set-?off against trade receivables of (.{0,340}?)\.',_re.I)
amt=_re.compile(r'\$\s?([\d,]+)(?:\s*million)?\s*(?:at\s*)?(.{0,70}?)(?=(?:\$)|$)',_re.I)
seen={}
for fn in sorted(os.listdir(CORPUSDIR)):
    t=_re.sub(r'\s+',' ',open(os.path.join(CORPUSDIR,fn),encoding='utf-8').read().replace('​',''))
    t=_re.sub(r'<!--.*?-->',' ',t)
    for m in pat3.finditer(t):
        for am in amt.finditer(m.group(1)):
            v=float(am.group(1).replace(',',''))
            dm=date_re.search(am.group(2))
            if not dm: continue
            mo=MON.get(dm.group(1))
            if not mo: continue
            k="%s-%02d-%02d"%(dm.group(3),mo,int(dm.group(2)))
            seen.setdefault(FIXDATE.get(k,k),(v,fn))
for dt,(v,fn) in sorted(seen.items()):
    add('de_dealer_sales_incentives_setoff',dt,'dealer','dealer sales incentives with a right of set-off against trade receivables',
        v,'USD_millions','filing',CORPUSREL+fn,'unpaid incentives Deere owes dealers, netted against what dealers owe Deere')
pd.DataFrame(recs).drop_duplicates(['series_id','period_end'],keep='first').to_csv(os.path.join(SC,'stage2.csv'),index=False)
print('with incentives:',len(recs))
