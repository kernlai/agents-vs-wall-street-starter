import re,glob,os,json
CORPUS="/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"
out=[]
for f in sorted(glob.glob(os.path.join(CORPUS,"*.md"))):
    t=open(f,encoding="utf-8").read().replace("​","")
    t=re.sub(r"\s+"," ",t)
    for m in re.finditer(r"[^.]*exceeding 12 months[^.]*\.",t):
        out.append((os.path.basename(f),m.group(0).strip()))
    for m in re.finditer(r"[^.]*ratios? of worldwide trade accounts and notes receivable[^.]*\.",t):
        out.append((os.path.basename(f),m.group(0).strip()))
seen=set()
for f,s in out:
    k=(f,s[:80])
    if k in seen: continue
    seen.add(k)
    print(f,"||",s)
