from pathlib import Path
import pandas as pd, numpy as np, json
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data'; PROJ=ROOT.parents[1]
p=pd.read_csv(D/'daily_prices.csv'); u=pd.read_csv(D/'universe.csv'); m=pd.read_csv(D/'price_manifest.csv')
r=pd.read_csv(PROJ/'分析报告/公司排序/90_有效性评估/2026-07-13_26方案3月6月生成前历史回看/02_28张榜全部名次.csv',dtype={'method_id':str,'list_id':str})
reg=pd.read_csv(PROJ/'分析报告/公司排序/00_运行与榜单注册表.csv',dtype={'method_id':str,'list_id':str})
p=p.dropna(subset=['close','adj_close']).drop_duplicates(['symbol','date'])
panel=p.pivot(index='date',columns='symbol',values='adj_close').sort_index()
daily=panel.pct_change(fill_method=None)
rows=[]
for sym in u.ticker.tolist()+['SPY','QQQ','SOXX','SMH','IWM','RSP','IGV','XLU','XLI','XLE','TLT','HYG','USO','^VIX','^GSPC','^TNX']:
    s=p[p.symbol==sym].sort_values('date');end=s.iloc[-1]
    row={'ticker':sym,'end_date':end.date,'end_close':end.close,'end_adj_close':end.adj_close,'last_volume':end.volume}
    mm=m[m.symbol==sym].iloc[0]; row.update(currency=mm.currency,exchange=mm.exchangeName,price_url=mm.url)
    for start in ['2026-07-10','2026-07-13','2026-07-14','2026-07-15','2026-07-17']:
        ss=s[s.date>=start]; key=start[5:].replace('-','')
        if not len(ss):continue
        a=ss.iloc[0];v=ss.adj_close
        row.update({f'start_{key}':a.date,f'close_{key}':a.close,f'adj_{key}':a.adj_close,f'ret_{key}':end.adj_close/a.adj_close-1,f'price_ret_{key}':end.close/a.close-1,f'n_{key}':len(ss)-1,f'mdd_{key}':(v/v.cummax()-1).min(),f'best_close_ret_{key}':v.max()/a.adj_close-1,f'worst_close_ret_{key}':v.min()/a.adj_close-1,f'zero_volume_{key}':int((ss.volume==0).sum())})
    pre=s[s.date<='2026-07-10'];
    for n in [20,63]:
        row[f'pre_momentum_{n}']=pre.iloc[-1].adj_close/pre.iloc[-n-1].adj_close-1 if len(pre)>n else np.nan
    for b in ['SPY','QQQ','SOXX']:
        rr=daily.loc[:'2026-07-10',[sym,b]].dropna() if sym!=b else pd.DataFrame()
        if len(rr)>=60:
            beta=np.cov(rr.iloc[:,0],rr.iloc[:,1],ddof=1)[0,1]/rr.iloc[:,1].var()
            row[f'pre_beta_{b}']=beta
    rows.append(row)
ret=pd.DataFrame(rows);ret.to_csv(D/'all_returns_and_benchmarks.csv',index=False,encoding='utf-8-sig')
co=u.merge(ret,on='ticker',validate='one_to_one'); co['actual_rank']=co.ret_0713.rank(ascending=False,method='min')
co['category_mean']=co.groupby('category').ret_0713.transform('mean');co['category_median']=co.groupby('category').ret_0713.transform('median');co['category_excess']=co.ret_0713-co.category_mean
for b in ['SPY','QQQ','SOXX']:
    br=float(ret.loc[ret.ticker==b,'ret_0713'].iloc[0]);co[f'excess_{b}']=co.ret_0713-br;co[f'beta_adjusted_excess_{b}']=co.ret_0713-co[f'pre_beta_{b}']*br
family=r[r.method_id.isin(['01','02','03','04','05','06','07'])].groupby(['method_id','ticker'])['rank'].mean().reset_index()
cons=family.groupby('ticker')['rank'].mean().rename('active_family_mean_rank').reset_index();cons['consensus_rank']=cons.active_family_mean_rank.rank(method='min')
co=co.merge(cons,on='ticker');wide=r.pivot(index='ticker',columns='list_id',values='rank').add_prefix('rank_').reset_index();co=co.merge(wide,on='ticker')
co.to_csv(D/'company_returns.csv',index=False,encoding='utf-8-sig')
joined=r.merge(co,on='ticker',suffixes=('','_company')).merge(reg[['list_id','list_name','lifecycle']],on='list_id')
joined.to_csv(D/'ranking_returns_long.csv',index=False,encoding='utf-8-sig')
def score(name,x):
    x=x.sort_values('rank');t=x.head(20); bot=x.tail(20); row={'list_id':name,'n':len(x),'top20_mean':t.ret_0713.mean(),'top20_median':t.ret_0713.median(),'universe_mean':x.ret_0713.mean(),'top20_excess_universe':t.ret_0713.mean()-x.ret_0713.mean(),'bottom20_mean':bot.ret_0713.mean(),'top_bottom_spread':t.ret_0713.mean()-bot.ret_0713.mean(),'rank_ic':(-x['rank']).corr(x.ret_0713.rank()),'sector_neutral_rank_ic':(-x['rank']).corr(x.category_excess.rank()),'top20_category_excess':t.category_excess.mean(),'top20_negative':int((t.ret_0713<0).sum()),'winner20_captured':int((t.actual_rank<=20).sum()),'winner20_capture_fraction':float((t.actual_rank<=20).mean()),'top20_avg_mdd':t.mdd_0713.mean(),'top20_tickers':','.join(t.ticker)}
    for k in ['0710','0714','0715','0717']: row[f'top20_ret_{k}']=t[f'ret_{k}'].mean();row[f'top20_excess_{k}']=t[f'ret_{k}'].mean()-x[f'ret_{k}'].mean()
    for b in ['SPY','QQQ','SOXX']:row[f'top20_excess_{b}']=t[f'excess_{b}'].mean();row[f'top20_beta_adjusted_{b}']=t[f'beta_adjusted_excess_{b}'].mean()
    for k in [10,40]:row[f'top{k}_mean']=x.head(k).ret_0713.mean()
    return row
metrics=[]
for lid,x in joined.groupby('list_id',sort=False):metrics.append(score(lid,x))
c=co.copy();c['rank']=c.consensus_rank;metrics.append(score('ACTIVE_CONSENSUS',c))
for n in [20,63]:
    c=co.copy();c['rank']=c[f'pre_momentum_{n}'].rank(ascending=False);metrics.append(score(f'PRE_MOMENTUM_{n}',c))
metrics=pd.DataFrame(metrics).merge(reg[['list_id','method_id','list_name','lifecycle']],on='list_id',how='left')
rng=np.random.default_rng(20260904); vals=co.ret_0713.to_numpy(); rand=np.array([rng.choice(vals,20,replace=False).mean() for _ in range(20000)])
metrics['random20_percentile']=[float((rand<=v).mean()) for v in metrics.top20_mean]
metrics.to_csv(D/'method_metrics.csv',index=False,encoding='utf-8-sig')
corr=r.pivot(index='ticker',columns='list_id',values='rank').corr();corr.to_csv(D/'ranking_correlation.csv',encoding='utf-8-sig')
co.groupby('category').agg(n=('ticker','size'),mean_return=('ret_0713','mean'),median_return=('ret_0713','median'),min_return=('ret_0713','min'),max_return=('ret_0713','max')).to_csv(D/'category_returns.csv',encoding='utf-8-sig')
print('UNIVERSE',co.ret_0713.describe().to_string());print('\nBENCHMARKS',ret.tail(16)[['ticker','ret_0713','end_date']].to_string(index=False))
print('\nWINNERS',co.sort_values('ret_0713',ascending=False).head(25)[['ticker','ret_0713','consensus_rank','rank_01','rank_02','rank_06G','rank_07']].to_string(index=False))
print('\nTOP PICKS',co.sort_values('consensus_rank').head(25)[['ticker','ret_0713','actual_rank','consensus_rank']].to_string(index=False))
print('\nMETHODS',metrics[['list_id','list_name','top20_mean','top20_excess_universe','rank_ic','top20_negative','winner20_captured']].to_string(index=False))
