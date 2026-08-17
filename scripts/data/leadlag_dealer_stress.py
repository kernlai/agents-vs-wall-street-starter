import pandas as pd,numpy as np,os,itertools
CSV="/Users/cor/Documents/projects/agents-vs-wall-street-starter/data/deere/dealers/dealer_credit_quality.csv"
df=pd.read_csv(CSV)
p=df.pivot_table(index='period_end',columns='series_id',values='value').sort_index()
p.index=pd.to_datetime(p.index)
p['sales_yoy']=p['de_net_sales_and_revenues'].pct_change(4)*100
p['trade_yoy']=p['de_trade_receivables_net'].pct_change(4)*100
p['wh_yoy']=p['de_wholesale_receivables_total'].pct_change(4)*100
def xcorr(x,y,maxlag=6):
    out=[]
    for L in range(0,maxlag+1):
        a=x.shift(L); s=pd.concat([a,y],axis=1).dropna()
        if len(s)<8: out.append((L,np.nan,len(s))); continue
        r=np.corrcoef(s.iloc[:,0],s.iloc[:,1])[0,1]
        out.append((L,round(r,3),len(s)))
    return out
print("Cross-correlation: X leads Y by L quarters (X shifted forward L). r, n\n")
tests=[('de_trade_receivables_pct_over_12m','sales_yoy'),
       ('de_trade_receivables_pct_over_12m','de_net_sales_and_revenues'),
       ('de_retail_stress_pct','sales_yoy'),
       ('de_retail_nonperforming_pct','sales_yoy'),
       ('de_wholesale_stress_pct','sales_yoy'),
       ('wh_yoy','sales_yoy'),
       ('de_prececl_other_stress_pct','sales_yoy'),
       ('de_prececl_retailnotes_stress_pct','sales_yoy')]
for x,y in tests:
    if x not in p or y not in p: print('missing',x,y); continue
    res=xcorr(p[x],p[y])
    best=max([r for r in res if not np.isnan(r[1])],key=lambda r:abs(r[1]),default=None)
    print(f"{x:42s} -> {y:12s} " + " ".join(f"L{L}:{r}(n={n})" for L,r,n in res) + (f"  | best L={best[0]} r={best[1]} n={best[2]}" if best else ""))
print()
# same-quarter relationships of interest
sub=p[['de_trade_receivables_pct_over_12m','de_wholesale_receivables_total','de_retail_stress_pct','de_net_sales_and_revenues','sales_yoy']].dropna()
print("n overlapping quarters for the joint frame:",len(sub))
