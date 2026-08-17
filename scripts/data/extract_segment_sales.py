import re,os,json,sys,csv
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from rfile_parse import parse_rfile,num
SC="/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"
man=json.load(open(os.path.join(SC,'manifest_seg.json')))
MON={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
def pdte(s):
    m=re.search(r'([A-Z][a-z]{2})\.?\s+(\d{1,2}),\s+(\d{4})',s)
    return None if not m else "%04d-%02d-%02d"%(int(m.group(3)),MON[m.group(1)],int(m.group(2)))
out=[]
for pe,info in man.items():
    for name,fn in info['reports']:
        if 'Operations by Operating Segment' not in name and 'Operating Segment (Details)' not in name: continue
        path=os.path.join(SC,'rfiles',f"{pe}_{fn}")
        if not os.path.exists(path): continue
        _,_,rows=parse_rfile(path)
        if not rows: continue
        hdr=rows[0]; dates=[pdte(c) for c in hdr[1:]]; body=rows[1:]
        if sum(1 for d in dates if d)==0 and len(rows)>1:
            dates=[pdte(c) for c in rows[1]]; body=rows[2:]
        ctx=''
        for r in body:
            if not r: continue
            lab=r[0]; vals=r[1:]
            if not [v for v in vals if v.strip()]:
                if lab.strip() not in ('Net Sales and Revenues','Segment Reporting Information'): ctx=lab
                continue
            for i,v in enumerate(vals):
                x=num(v)
                if x is None: continue
                out.append(dict(filing_period=pe,form=info['form'],report=name,context=ctx,row=lab,
                                col_index=i,col_date=dates[i] if i<len(dates) else None,value=x))
with open(os.path.join(SC,'segfacts.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(len(out))
