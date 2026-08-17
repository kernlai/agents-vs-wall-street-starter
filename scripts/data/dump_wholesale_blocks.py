import re,glob,os
CORPUS="/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere/filings"
out=[]
for f in sorted(glob.glob(os.path.join(CORPUS,"*.md"))):
    t=open(f,encoding="utf-8").read()
    if "Wholesale receivables:" not in t: continue
    lines=t.split("\n")
    idxs=[i for i,l in enumerate(lines) if "wholesale receivables" in l.lower() and ("credit quality" in l.lower() or "Wholesale receivables:" in l)]
    if not idxs: continue
    start=max(0,min(idxs)-3); end=min(len(lines),max(idxs)+40)
    out.append("\n\n########## %s\n"%os.path.basename(f))
    out.append("\n".join(lines[start:end]))
print("\n".join(out))
