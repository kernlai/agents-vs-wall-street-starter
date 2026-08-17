import csv, collections
P='/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/de_q3_cost_inputs.csv'
rows=list(csv.DictReader(open(P)))
def get(sid,fy,q,seg,comp):
    for r in rows:
        if (r['series_id']==sid and r['fiscal_year']==str(fy) and r['fiscal_quarter']==str(q)
            and r['segment']==seg and r['component']==comp): return float(r['value'])
    return None
checks=[]
GT={('PPA','net_sales'):4503,('SAT','net_sales'):3485,('CF','net_sales'):3790,
    ('PPA','operating_profit'):706,('SAT','operating_profit'):719,('CF','operating_profit'):561}
for (seg,comp),v in GT.items():
    got=get('de_segment_8k',2026,2,seg,comp)
    checks.append((f'2026Q2 {seg} {comp}',got,v,got==v))
# FY2025 full-year segment sales
for seg,tot in [('PPA',17311),('SAT',10224),('CF',11382)]:
    s=sum(get('de_segment_8k',2025,q,seg,'net_sales') or 0 for q in (1,2,3,4))
    checks.append((f'FY2025 {seg} sales sum',s,tot,abs(s-tot)<=1))
# H1 FY2026
for seg,tot in [('PPA',7666),('SAT',5653),('CF',6460)]:
    s=sum(get('de_segment_8k',2026,q,seg,'net_sales') or 0 for q in (1,2))
    checks.append((f'H1 FY2026 {seg} sales',s,tot,s==tot))
# bridges reconcile
br=collections.defaultdict(dict)
for r in rows:
    if r['series_id']=='de_op_bridge':
        br[(r['fiscal_year'],r['fiscal_quarter'],r['segment'])][r['component']]=float(r['value'])
bad=0
for k,c in br.items():
    comps=sum(v for n,v in c.items() if n.startswith('bridge_'))
    end=c.get('operating_profit')
    prev=get('de_segment_8k',int(k[0])-1,int(k[1]),k[2],'operating_profit')
    if end is None or prev is None: continue
    if abs(prev+comps-end)>1: bad+=1; print('BRIDGE FAIL',k,prev,comps,end)
checks.append(('all bridge rows reconcile vs 8-K endpoints',bad,0,bad==0))
# no Q3 FY2026 actuals
q3act=[r for r in rows if r['fiscal_year']=='2026' and r['fiscal_quarter']=='3'
       and r['series_id'] in ('de_op_bridge','de_segment_8k','de_warranty')]
checks.append(('no reported Q3 FY2026 Deere financials in file',len(q3act),0,len(q3act)==0))
for name,got,exp,ok in checks:
    print(('PASS' if ok else 'FAIL'),f'{name:48}',got,'vs',exp)
print('bridge quarters in file:',len(br))
