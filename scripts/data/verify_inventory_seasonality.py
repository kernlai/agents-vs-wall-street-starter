"""Re-derive dealer-inventory seasonal norms and the Apr->Jul transition.
NOTE: (series_id, period_end) is NOT unique in dealer_inventory.csv -- the same
series_id carries Deere rows AND an 'Industry ex-Deere' comparator row. Must
filter on entity or the industry 70% contaminates the Deere series."""
import csv, collections, statistics as st
P="/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/dealer_inventory.csv"
S=collections.defaultdict(dict); OTHER=collections.defaultdict(dict)
for r in csv.DictReader(open(P)):
    if not r["value"]: continue
    (S if r["entity"].startswith("Deere") else OTHER)[r["series_id"]][r["period_end"]]=float(r["value"])
print("non-Deere comparator rows held under the same series_ids:")
for sid,d in OTHER.items():
    for k,v in sorted(d.items()): print(f"   {sid} {k} = {v:.0f}")
for sid,lab in [("de_dealer_inv_pct_ttm_2wd_100hp","2WD 100+hp"),("de_dealer_inv_pct_ttm_combines","Combines")]:
    s=S[sid]
    print(f"\n{lab}: n={len(s)}  {min(s)} .. {max(s)}")
    print("  month means 2013-2025:", {m:round(st.mean([v for k,v in s.items() if k[5:7]==m and k<'2026']),1) for m in ['01','04','07','10']})
    tr=[]
    for k in sorted(s):
        if k[5:7]=="04":
            j=[x for x in s if x[:4]==k[:4] and x[5:7]=="07"]
            if j: tr.append(s[j[0]]-s[k])
    print(f"  Apr->Jul move: n={len(tr)} median {st.median(tr):+.1f} mean {st.mean(tr):+.1f} range {min(tr):+.0f}..{max(tr):+.0f}")
    apr26=[v for k,v in s.items() if k.startswith("2026-04")][0]
    ly=[v for k,v in s.items() if k.startswith("2025-07")][0]
    print(f"  Apr26 {apr26:.0f} -> implied Jul26 {apr26+st.median(tr):.1f} (median) vs Jul25 actual {ly:.0f}  => y/y {100*((apr26+st.median(tr))/ly-1):+.0f}%")
    print("  recent seasonal deviations:")
    for k in sorted(s)[-8:]:
        mm=st.mean([v for j,v in s.items() if j[5:7]==k[5:7] and j<'2026'])
        print(f"    {k} {s[k]:5.0f}  dev {s[k]-mm:+.1f}")
