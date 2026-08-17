"""Deere & Company dealer-credit-quality time series builder.

Primary source: SEC EDGAR XBRL 'R' financial-report renderings of DE 10-Q / 10-K
(CIK 315189) - the machine-readable form of the SAME filings held in the offline
corpus at challenge/offline-data/deere/filings/. Corpus paths are attached where
the figure is also visible in the corpus markdown.

Deere splits financing receivables into WHOLESALE receivables (owed by independent
DEALERS) and RETAIL/CUSTOMER receivables (owed by END CUSTOMERS). The wholesale
split only exists from CECL adoption (FY2021, first reported Q1 FY2021, with
restated FY2020 comparatives). Before that Deere disclosed 'Retail Notes' vs
'Other' financing receivables, where 'Other' bundles dealer wholesale notes with
revolving charge accounts, operating loans and financing leases - a mixed series,
labelled entity='mixed'.
"""
import pandas as pd, re, os, json
SC="/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"
OUTDIR="/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers"
os.makedirs(OUTDIR,exist_ok=True)
d=pd.read_csv(os.path.join(SC,'facts.csv'))
for c in ('row','context','sub','report'): d[c]=d[c].fillna('').str.strip()
# canonical period ends: FY2016 year-end appears as both 2016-10-30 and 2016-10-31
FIXDATE={'2016-10-31':'2016-10-30','2015-11-01':'2015-10-31','2016-05-01':'2016-04-30'}
d['col_date']=d.col_date.replace(FIXDATE)
d['filing_period']=d.filing_period.replace(FIXDATE)

CORPUS="challenge/offline-data/deere/filings/"
# map period_end -> corpus filing markdown (the same 10-Q/10-K)
CMAP={
 '2015-01-31':'2015-02-20__de-us-20150220-q1-10q__469211.md','2015-04-30':'2015-05-22__de-us-20150522-q2-10q__468391.md',
 '2015-07-31':'2015-08-21__de-us-20150821-q3-10q__469127.md','2015-10-31':'2015-11-25__de-us-20151125-q4-10k__469104.md',
 '2016-01-31':'2016-02-19__de-us-20160219-q1-10q__469699.md','2016-04-30':'2016-05-20__de-us-20160520-q2-10q__469677.md',
 '2016-07-31':'2016-08-19__de-us-20160819-q3-10q__469698.md','2016-10-31':'2016-11-23__de-us-20161123-q4-10k__469184.md',
 '2017-01-29':'2017-02-17__de-us-20170217-q1-10q__469116.md','2017-04-30':'2017-05-19__de-us-20170519-q2-10q__469480.md',
 '2017-07-30':'2017-08-18__de-us-20170818-q3-10q__469477.md','2017-10-29':'2017-11-22__de-us-20171122-q4-10k__468364.md',
 '2018-01-28':'2018-02-16__de-us-20180216-q1-10q__469205.md','2018-04-29':'2018-05-18__de-us-20180518-q2-10q__468389.md',
 '2018-07-29':'2018-08-17__de-us-20180817-q3-10q__469474.md','2018-10-28':'2018-11-21__de-us-20181121-q4-10k__469201.md',
 '2019-01-27':'2019-02-15__de-us-20190215-q1-10q__469204.md','2019-04-28':'2019-05-17__de-us-20190517-q2-10q__469675.md',
 '2019-07-28':'2019-08-16__de-us-20190816-q3-10q__469206.md','2019-11-03':'2019-11-27__de-us-20191127-q4-10k__469283.md',
 '2020-02-02':'2020-02-21__de-us-20200221-q1-10q__468373.md','2020-05-03':'2020-05-21__de-us-20200521-q2-10q__469470.md',
 '2020-08-02':'2020-08-20__de-us-20200820-q3-10q__105822.md','2020-11-01':'2020-11-25__de-us-20201125-q4-10k__105845.md',
 '2021-01-31':'2021-02-19__de-us-20210219-q1-10q__105814.md','2021-05-02':'2021-05-21__de-us-20210521-q2-10q__105821.md',
 '2021-08-01':'2021-08-20__de-us-20210820-q3-10q__105837.md','2021-10-31':'2021-12-16__de-us-20211216-fy-10k__645298.md',
 '2022-01-30':'2022-02-18__de-us-20220218-q1-10q__105834.md','2022-05-01':'2022-05-20__de-us-20220520-q2-10q__105838.md',
 '2022-07-31':'2022-08-19__de-us-20220819-q3-10q__105818.md','2022-10-30':'2022-11-23__de-us-20221123-q4-10k__105816.md',
 '2023-01-29':'2023-02-17__de-us-20230217-q1-10q__105813.md','2023-04-30':'2023-05-19__de-us-20230519-q2-10q__105852.md',
 '2023-07-30':'2023-08-18__de-us-20230818-q3-10q__105835.md','2023-10-29':'2023-12-15__de-us-20231215-fy-10k__645297.md',
 '2024-01-28':'2024-02-15__de-us-20240215-q1-10q__105826.md','2024-04-28':'2024-05-16__de-us-20240516-q2-10q__105820.md',
 '2024-07-28':'2024-08-15__de-us-20240815-q3-10q__105828.md','2024-10-27':'2024-11-21__de-us-20241121-q4-10k__105810.md',
 '2025-01-26':'2025-02-13__de-us-20250213-q1-10q__105832.md','2025-04-27':'2025-05-15__de-us-20250515-q2-10q__105831.md',
 '2025-07-27':'2025-08-14__de-us-20250814-q3-10q__155834.md','2025-11-02':'2025-12-18__de-us-20251218-fy-10k__393777.md',
 '2026-02-01':'2026-02-26__de-us-20260226-q1-10q__636995.md','2026-05-03':'2026-05-28__de-us-20260528-q2-10q__1055932.md',
}
def fiscal(dt):
    y,m,dd=[int(x) for x in dt.split('-')]
    if m in (1,2): return (y,1)
    if m in (4,5): return (y,2)
    if m in (7,8): return (y,3)
    if m in (10,11): return (y+1,4)
    return (None,None)
recs=[]
def add(sid,pe,entity,metric,value,units,stype,src,notes=''):
    fy,fq=fiscal(pe)
    recs.append(dict(series_id=sid,period_end=pe,fiscal_year=fy,fiscal_quarter=fq,entity=entity,metric=metric,
                     value=value,units=units,source_type=stype,source=src,notes=notes))
def csrc(pe,extra=''):
    f=CMAP.get(pe)
    return (CORPUS+f if f else 'SEC EDGAR XBRL R-report, DE 10-Q/10-K, CIK 315189')+(' ; '+extra if extra else '')

def seg_of(c):
    return 'ag' if 'Agriculture' in c else ('cf' if 'Construction' in c else None)
def buck_of(c):
    cl=c.lower()
    if 'non-performing' in cl or 'nonperforming' in cl: return 'nonperforming'
    if '30-59' in cl: return 'pd_30_59'
    if '60-89' in cl: return 'pd_60_89'
    if '90+' in cl or '90 days' in cl: return 'pd_90plus'
    if '30+' in cl: return 'pd_30plus'
    if 'current' in cl: return 'current'
    return None

# ================= 1. WHOLESALE (dealer) =================
wh=d[d.report.str.contains('Wholesale',case=False)&
     d.row.isin(['Total wholesale receivables','Current','Non-performing','30+ days past due',
                 '30-59 days past due','60-89 days past due','90+ days past due','Past due'])].copy()
wh['key']=wh.apply(lambda r: r.context if r.row in ('Total wholesale receivables','Past due') else r.context+' | '+r.row,axis=1)
wh['seg']=wh.key.apply(seg_of); wh['buck']=wh.key.apply(buck_of)
wh=wh[wh.key.str.contains('Wholesale|Agriculture|Construction',case=False)]
wh['asrep']=(wh.filing_period==wh.col_date)
wh=wh.sort_values(['col_date','asrep','filing_period']).drop_duplicates(['col_date','seg','buck'],keep='last')
W={}
for _,r in wh.iterrows(): W[(r.col_date,r.seg if r.seg else 'all',r.buck if r.buck else 'total')]=r.value
wdates=sorted(set(k[0] for k in W))
for dt in wdates:
    has_table = W.get((dt,'ag','current')) is not None
    tot=W.get((dt,'all','total'))
    if tot is None and has_table:
        tot=sum(v for k,v in W.items() if k[0]==dt and k[1] in ('ag','cf'))
    if tot is not None:
        add('de_wholesale_receivables_total',dt,'dealer','wholesale financing receivables owed by dealers, total',tot,
            'USD_millions','filing',csrc(dt))
    if not has_table: continue
    for seg,nm in (('ag','agriculture & turf'),('cf','construction & forestry')):
        for b,sid in (('current','de_wholesale_current'),('nonperforming','de_wholesale_nonperforming')):
            v=W.get((dt,seg,b))
            if b=='current' and v is None: continue
            add(sid+'_'+seg,dt,'dealer',f'wholesale {b} - {nm}',v if v is not None else 0.0,'USD_millions','filing',csrc(dt))
    agg={}
    for b in ('current','nonperforming','pd_30plus','pd_30_59','pd_60_89','pd_90plus'):
        vals=[W.get((dt,s,b)) for s in ('ag','cf')]
        agg[b]=sum(v for v in vals if v is not None) if any(v is not None for v in vals) else 0.0
    add('de_wholesale_current',dt,'dealer','wholesale receivables current',agg['current'],'USD_millions','filing',csrc(dt))
    add('de_wholesale_nonperforming',dt,'dealer','wholesale receivables non-performing',agg['nonperforming'],'USD_millions','filing',csrc(dt),
        'zero = no non-performing wholesale balance disclosed')
    pd30=agg['pd_30plus']+agg['pd_30_59']+agg['pd_60_89']+agg['pd_90plus']
    add('de_wholesale_past_due_30plus',dt,'dealer','wholesale receivables 30+ days past due',pd30,'USD_millions','filing',csrc(dt),
        'FY2021 disclosed 30-59/60-89/90+ separately; summed here')
    if dt <= '2021-10-31':
        for b,sid in (('pd_30_59','de_wholesale_past_due_30_59'),('pd_60_89','de_wholesale_past_due_60_89'),('pd_90plus','de_wholesale_past_due_90plus')):
            add(sid,dt,'dealer','wholesale '+sid.split('past_due_')[-1]+' days past due',agg[b],'USD_millions','filing',csrc(dt))
    if tot:
        add('de_wholesale_stress_pct',dt,'dealer','(30+ past due + non-performing) / total wholesale receivables',
            round(100*(pd30+agg['nonperforming'])/tot,4),'percent','derived','derived: '+csrc(dt))
        add('de_wholesale_nonperforming_pct',dt,'dealer','non-performing / total wholesale receivables',
            round(100*agg['nonperforming']/tot,4),'percent','derived','derived: '+csrc(dt))

# ================= 2. RETAIL CUSTOMER (CECL era) =================
rt=d[d.report.str.contains('Retail Notes',case=False)&
     d.row.isin(['Total retail customer receivables','Total customer receivables'])].copy()
rt=rt[rt.context.str.contains('Agriculture|Construction',case=False)]
rt['seg']=rt.context.apply(seg_of); rt['buck']=rt.context.apply(buck_of)
rt=rt[rt.buck.notna()]
rt=rt[rt.col_date>='2021-01-31']
rt['asrep']=(rt.filing_period==rt.col_date)
rt=rt.sort_values(['col_date','asrep','filing_period']).drop_duplicates(['col_date','seg','buck'],keep='last')
R={}
for _,r in rt.iterrows(): R[(r.col_date,r.seg,r.buck)]=r.value
rdates=sorted(set(k[0] for k in R))
for dt in rdates:
    agg={b:sum(R.get((dt,s,b),0.0) for s in ('ag','cf')) for b in ('current','nonperforming','pd_30_59','pd_60_89','pd_90plus')}
    total=sum(agg.values())
    add('de_retail_receivables_total',dt,'customer','retail customer financing receivables, total',total,'USD_millions','filing',csrc(dt),
        'sum of current + past due buckets + non-performing (ag&turf + c&f)')
    for b,sid in (('current','de_retail_current'),('nonperforming','de_retail_nonperforming'),
                  ('pd_30_59','de_retail_past_due_30_59'),('pd_60_89','de_retail_past_due_60_89'),
                  ('pd_90plus','de_retail_past_due_90plus')):
        add(sid,dt,'customer','retail customer '+b.replace('pd_','').replace('_','-')+(' days past due' if b.startswith('pd') else ''),
            agg[b],'USD_millions','filing',csrc(dt))
    pdtot=agg['pd_30_59']+agg['pd_60_89']+agg['pd_90plus']
    add('de_retail_past_due_total',dt,'customer','retail customer total past due (30+ days)',pdtot,'USD_millions','filing',csrc(dt))
    add('de_retail_stress_pct',dt,'customer','(past due + non-performing) / total retail customer receivables',
        round(100*(pdtot+agg['nonperforming'])/total,4),'percent','derived','derived: '+csrc(dt))
    add('de_retail_nonperforming_pct',dt,'customer','non-performing / total retail customer receivables',
        round(100*agg['nonperforming']/total,4),'percent','derived','derived: '+csrc(dt))

# ================= 3. PRE-CECL age analysis (FY2015-FY2020) =================
pc=d[d.report.str.contains(r'Past Due Age Analysis|Financing Receivables Past Due|RECEIVABLES \(Details',case=False,regex=True)&
     d.row.isin(['Total Past Due','Total Non-Performing','Current','Total Financing Receivables'])].copy()
pc=pc[pc.context.str.contains('Retail Notes|Other Financing Receivables',case=False)]
pc['fam']='retailnotes' if False else pc.context.apply(lambda c:'retailnotes' if 'Retail Notes' in c else 'other')
pc['seg']=pc.context.apply(seg_of); pc['sub2']=pc.context.apply(buck_of)
pc=pc[pc.sub2.isna() & pc.seg.notna()]      # segment-level rows only, not bucket-level
pc['asrep']=(pc.filing_period==pc.col_date)
pc=pc.sort_values(['col_date','asrep','filing_period']).drop_duplicates(['col_date','fam','seg','row'],keep='last')
P={}
for _,r in pc.iterrows(): P[(r.col_date,r.fam,r.seg,r.row)]=r.value
pdates=sorted(set(k[0] for k in P))
LBL={'retailnotes':('customer','retail notes (end customers)'),
     'other':('mixed','"Other" financing receivables - bundles DEALER wholesale notes with revolving charge accounts, operating loans and financing leases')}
for dt in pdates:
    if dt>='2021-01-31': continue
    for fam,(ent,desc) in LBL.items():
        vals={r:sum(P.get((dt,fam,s,r),0.0) for s in ('ag','cf')) for r in
              ('Total Past Due','Total Non-Performing','Current','Total Financing Receivables')}
        if vals['Total Financing Receivables']==0: continue
        pref='de_prececl_'+fam
        add(pref+'_total',dt,ent,desc+' - total financing receivables',vals['Total Financing Receivables'],'USD_millions','filing',csrc(dt),
            'pre-CECL presentation; no separate wholesale/dealer split existed')
        add(pref+'_past_due_total',dt,ent,desc+' - total past due (30+ days, still accruing)',vals['Total Past Due'],'USD_millions','filing',csrc(dt))
        add(pref+'_nonperforming',dt,ent,desc+' - non-performing',vals['Total Non-Performing'],'USD_millions','filing',csrc(dt))
        add(pref+'_stress_pct',dt,ent,desc+' - (past due + non-performing) / total',
            round(100*(vals['Total Past Due']+vals['Total Non-Performing'])/vals['Total Financing Receivables'],4),
            'percent','derived','derived: '+csrc(dt))

# ================= 4. ALLOWANCE / PROVISION / WRITE-OFFS =================
al=d[d.report.str.contains(r'Allowance for Credit Losses|RECEIVABLES \(Details 2\)|FINANCING RECEIVABLES \(Details 2\)',case=False,regex=True)].copy()
CTXMAP={'Wholesale Receivables':('wholesale','dealer'),
        'Retail Notes & Financing Leases':('retail_notes','customer'),
        'Retail Notes and Financing Leases':('retail_notes','customer'),
        'Retail Notes':('retail_notes','customer'),
        'Revolving Charge Accounts':('revolving','customer'),
        'Other Financing Receivables':('other','mixed')}
ROWMAP={'End of period balance':'allowance','End of year balance':'allowance','End of year balance*':'allowance',
        'Provision':'provision','Provision (credit)':'provision','Provision (credit) subtotal':'provision','Provision subtotal':'provision',
        'Write-offs':'writeoffs','Recoveries':'recoveries',
        'Deposits primarily withheld from dealers and merchants available for potential credit losses':'dealer_withholding'}
al=al[al.context.isin(CTXMAP)&al.row.isin(ROWMAP)]
al=al[~((al.row.str.startswith('End of'))&(al['sub'].str.contains('Financing receivable',case=False)))]
for _,r in al.iterrows():
    pass
# take, per (col_date, context, row), the value from the AS-REPORTED filing and the FIRST matching column
al['asrep']=(al.filing_period==al.col_date)
# only the primary column (col_index 0) of the as-reported filing: that is the
# fiscal-quarter flow in a 10-Q and the fiscal-year flow in a 10-K. Flows shown
# only in a 6/9-month column are NOT quarterly and are excluded.
allw=al[al.asrep & (al.col_index==0)].drop_duplicates(['col_date','context','row'],keep='first')
for _,r in allw.iterrows():
    fam,ent=CTXMAP[r.context]; met=ROWMAP[r.row]
    if met=='allowance':
        note='balance at period end'
    elif met=='dealer_withholding':
        note='dealer/merchant deposits withheld, available to absorb credit losses'
    else:
        note='fiscal-quarter flow (10-Q) or full fiscal year (10-K)'
    add(f'de_{fam}_{met}',r.col_date,ent,f'{fam} {met}',r.value,'USD_millions','filing',csrc(r.col_date),note)

out=pd.DataFrame(recs)
out=out.drop_duplicates(['series_id','period_end'],keep='first')
out=out.sort_values(['series_id','period_end'])
out.to_csv(os.path.join(SC,'stage1.csv'),index=False)
print(len(out), out.series_id.nunique())
