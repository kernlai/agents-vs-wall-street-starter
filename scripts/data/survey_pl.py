import re,os,glob,unicodedata
D="/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"
def clean(s):
    s=s.replace('​',' ').replace(' ',' ').replace('‑','-').replace('–','-').replace('—','-')
    return s
for f in sorted(glob.glob(D+"/*.md")):
    lines=[clean(l.rstrip('\n')) for l in open(f,encoding='utf-8')]
    hits=[i for i,l in enumerate(lines) if re.search(r'major product lines',l,re.I)]
    if not hits: continue
    print("="*100); print(os.path.basename(f), "hits:",hits)
    for i in hits:
        # walk back up to 25 lines to find a header
        ctx=None
        for j in range(i-1,max(-1,i-30),-1):
            l=lines[j]
            if re.search(r'(Three|Six|Nine|Twelve) Months Ended|Agriculture and Turf|quarter of 20|months of 20|PPA',l):
                ctx=(j,l[:200]); break
        print(f"  line {i}: back-> {ctx}")
