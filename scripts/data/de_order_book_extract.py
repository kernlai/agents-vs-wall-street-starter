#!/usr/bin/env python3
"""
Stage 1: scan all Deere call transcripts for order-book / lead-time / EOP /
underproduction / dealer-inventory language and dump sentence-level hits with
provenance so they can be read and hand-adjudicated.

Standard library only. Output: a JSON + a readable text dump in the scratch dir.
"""
import os, re, json, sys

CORPUS = "/Users/cor/Documents/projects/agents-vs-wall-street-starter/challenge/offline-data/deere"
TDIR = os.path.join(CORPUS, "call-transcripts")
OUT = "/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"
os.makedirs(OUT, exist_ok=True)

# Deere fiscal year ends ~last Sunday of October. Earnings calls:
# Feb -> Q1, May -> Q2, Aug -> Q3, Nov -> Q4 (of the FY that just ended).
def call_period(datestr):
    y, m, d = (int(x) for x in datestr.split("-"))
    if m == 2:
        return y, 1
    if m in (5, 6):
        return y, 2
    if m == 8:
        return y, 3
    if m in (11, 12):
        return y + 1, 4  # Q4 of FY y reported in Nov of calendar y; FY label = y
    return None

def fy_q(datestr):
    y, m, d = (int(x) for x in datestr.split("-"))
    if m == 2:  return (y, 1)
    if m in (5,6): return (y, 2)
    if m == 8:  return (y, 3)
    if m in (11,12): return (y, 4)   # FY y Q4, reported Nov of calendar y
    return (y, None)

PATTERNS = {
    "order_book":      r"\border book|\border books|\border bank|\bbacklog",
    "eop":             r"early order program|early-order program|early order programme|\bEOP\b|\bEOPs\b|early order",
    "lead_time":       r"lead time|lead-time|leadtime",
    "order_coverage":  r"sold out|order (?:book|books)?\s*(?:is|are|remain|extend|extends|extending|run|runs|go|goes|filled|full|through|into|well into)|production slots|slots (?:are )?(?:filled|full|spoken)|order visibility|visibility (?:extends|through|into)|covered through|booked (?:through|into)",
    "underproduction": r"underproduc|under-produc|under produc|overproduc|over-produc|produc\w* (?:in line with|below|above|ahead of) retail|retail[- ]driven production|production in line with retail",
    "dealer_inv":      r"dealer inventor|field inventor|inventory[- ]to[- ]sales|used inventor|new inventor|inventory levels",
    "order_pct":       r"orders? (?:are |were |is |was )?(?:up|down)\s+[\d]|order (?:intake|entry|velocity|activity|rates?)",
    "production_sched":r"production schedule|production plan|production slot|build schedule|shipment schedule|production rates?",
    "next_q_guide":    r"(?:third|fourth|second|first) quarter|\bQ3\b|\bQ4\b|\b3Q\b|\b4Q\b|back half|second half|balance of the (?:year|fiscal)|remainder of the (?:year|fiscal)",
}
COMP = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}

# core = only pull sentences hitting one of these; next_q_guide is a co-tag
CORE = ["order_book","eop","lead_time","order_coverage","underproduction","order_pct","production_sched"]

SENT = re.compile(r"(?<=[.!?])\s+")

def sentences(text):
    # split paragraphs first (transcripts are one speaker-turn per line)
    for para in text.split("\n"):
        para = para.strip()
        if not para or para.startswith("#") or para.startswith("---"):
            continue
        para = re.sub(r"^Unknown speaker:\s*", "", para)
        parts = SENT.split(para)
        for i, s in enumerate(parts):
            yield s.strip(), parts, i

def main():
    files = sorted(f for f in os.listdir(TDIR) if f.endswith(".md"))
    records = []
    for fn in files:
        m = re.match(r"(\d{4}-\d{2}-\d{2})__", fn)
        if not m:
            continue
        date = m.group(1)
        fy, q = fy_q(date)
        path = os.path.join(TDIR, fn)
        text = open(path, encoding="utf-8", errors="replace").read()
        kind = "qna" if "qna" in fn else ("agm" if "agm" in fn else "pres")
        for s, parts, i in sentences(text):
            tags = [k for k in CORE if COMP[k].search(s)]
            if not tags:
                continue
            if COMP["next_q_guide"].search(s):
                tags.append("next_q_guide")
            if COMP["dealer_inv"].search(s):
                tags.append("dealer_inv")
            ctx = " ".join(parts[max(0,i-1):i+2])
            records.append({
                "date": date, "fy": fy, "q": q, "kind": kind,
                "file": os.path.join("call-transcripts", fn),
                "tags": tags, "sentence": s, "context": ctx[:1200],
            })
    json.dump(records, open(os.path.join(OUT,"order_hits.json"),"w"), indent=1)
    # readable dump grouped by date
    with open(os.path.join(OUT,"order_hits.txt"),"w") as fh:
        cur = None
        for r in records:
            key = (r["date"], r["kind"])
            if key != cur:
                cur = key
                fh.write(f"\n\n===== {r['date']}  FY{r['fy']}Q{r['q']}  [{r['kind']}]  {r['file']}\n")
            fh.write(f"  [{'|'.join(r['tags'])}] {r['sentence']}\n")
    # counts per date
    from collections import Counter, defaultdict
    bydate = defaultdict(Counter)
    for r in records:
        for t in r["tags"]:
            bydate[r["date"]][t]+=1
    print(f"files scanned: {len(files)}, hit sentences: {len(records)}, dates with hits: {len(bydate)}")
    for d in sorted(bydate):
        print(d, dict(bydate[d]))

if __name__ == "__main__":
    main()
