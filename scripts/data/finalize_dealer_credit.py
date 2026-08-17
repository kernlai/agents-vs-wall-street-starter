import pandas as pd,os,itertools,math
SC="/private/tmp/claude-501/-Users-cor/c1ddf24f-b1cc-482f-9e47-45cae42bbce1/scratchpad"
OUT="/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/dealer_credit_quality.csv"
FIX={'2016-10-31':'2016-10-30','2015-11-01':'2015-10-31','2016-05-01':'2016-04-30','2017-10-30':'2017-10-29','2020-11-02':'2020-11-01'}
a=pd.read_csv(os.path.join(SC,'stage1.csv')); b=pd.read_csv(os.path.join(SC,'stage2.csv'))
df=pd.concat([a,b],ignore_index=True)
df['period_end']=df.period_end.replace(FIX)
def fiscal(dt):
    y,m,dd=[int(x) for x in dt.split('-')]
    if m in (1,2): return (y,1)
    if m in (4,5): return (y,2)
    if m in (7,8): return (y,3)
    return (y+1,4)
df[['fiscal_year','fiscal_quarter']]=df.period_end.apply(lambda d: pd.Series(fiscal(d)))
df=df.drop_duplicates(['series_id','period_end'],keep='first')
# derived: wholesale receivables as % of quarterly net sales (dealer-financed inventory intensity)
piv=df.pivot_table(index='period_end',columns='series_id',values='value')
extra=[]
for dt,r in piv.iterrows():
    if pd.notna(r.get('de_wholesale_receivables_total')) and pd.notna(r.get('de_net_sales_and_revenues')):
        fy,fq=fiscal(dt)
        extra.append(dict(series_id='de_wholesale_receivables_to_qtr_sales_pct',period_end=dt,fiscal_year=fy,fiscal_quarter=fq,
            entity='dealer',metric='wholesale (dealer) financing receivables / quarterly net sales & revenues',
            value=round(100*r['de_wholesale_receivables_total']/r['de_net_sales_and_revenues'],2),units='percent',
            source_type='derived',source='derived from de_wholesale_receivables_total and de_net_sales_and_revenues',notes=''))
df=pd.concat([df,pd.DataFrame(extra)],ignore_index=True)
cols=['series_id','period_end','fiscal_year','fiscal_quarter','entity','metric','value','units','source_type','source','notes']
df=df[cols].sort_values(['series_id','period_end'])
df.to_csv(OUT,index=False)
print('rows',len(df),'series',df.series_id.nunique(),'dates',df.period_end.nunique())
print(df.series_id.value_counts().to_string())
