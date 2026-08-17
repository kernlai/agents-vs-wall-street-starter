import json,os,re,time,urllib.request
UA={'User-Agent':'Research Analyst cor@salomo.io'}
SC="/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"
rows=json.load(open(os.path.join(SC,'filings.json')))
def get(u):
    for _ in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read().decode('utf-8','ignore')
        except Exception as e:
            time.sleep(2)
    raise RuntimeError(u)
KEY=re.compile(r"(credit quality|aging|past due|allowance for credit loss|financing receivable|^RECEIVABLES)",re.I)
manifest={}
for form,fdate,pend,acc in rows:
    a=acc.replace('-','')
    base=f"https://www.sec.gov/Archives/edgar/data/315189/{a}/"
    fs=get(base+"FilingSummary.xml")
    reps=re.findall(r'<Report[^>]*>(.*?)</Report>',fs,re.S)
    hits=[]
    for r in reps:
        nm=re.search(r'<ShortName>(.*?)</ShortName>',r,re.S)
        fn=re.search(r'<HtmlFileName>(.*?)</HtmlFileName>',r,re.S)
        if not nm or not fn: continue
        n=nm.group(1)
        if KEY.search(n): hits.append((n,fn.group(1)))
    manifest[pend]={'form':form,'acc':acc,'base':base,'reports':hits}
    for n,f in hits:
        out=os.path.join(SC,'rfiles',f"{pend}_{f}")
        if not os.path.exists(out):
            open(out,'w').write(get(base+f))
            time.sleep(0.12)
    print(pend,form,len(hits),flush=True)
    time.sleep(0.15)
json.dump(manifest,open(os.path.join(SC,'manifest2.json'),'w'),indent=1)
