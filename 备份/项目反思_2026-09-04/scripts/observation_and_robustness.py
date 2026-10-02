from pathlib import Path
import pandas as pd,numpy as np,json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';p=pd.read_csv(D/'daily_prices.csv').dropna(subset=['adj_close','close']);co=pd.read_csv(D/'company_returns.csv');dec=pd.read_csv(D/'decisions_historical.csv');comp=pd.read_csv(D/'company_comparison_historical_sources.csv')
rows=[]
for _,x in co.iterrows():
    s=p[p.symbol==x.ticker].sort_values('date');end=s.iloc[-1]
    dd=dec[dec.ticker==x.ticker].iloc[0]
    for layer,date,source in [('排序','2026-07-13','历史28榜见historical_rankings.csv'),('公司对比','2026-07-14','公司对比历史原文见company_comparison_historical_sources.csv'),('情景决策',dd.scenario_report_date,dd.scenario_path),('经营评估',dd.evaluation_report_date,dd.evaluation_path)]:
        a=s[s.date>=date].iloc[0]; nxt=s[s.date>date].iloc[0]
        open_adj=nxt.open*nxt.adj_close/nxt.close
        rows.append(dict(ticker=x.ticker,company=x.company,layer=layer,report_date=date,observation_start_date=a.date,observation_start_close=a.close,observation_start_adj_close=a.adj_close,last_date=end.date,last_close=end.close,last_adj_close=end.adj_close,adjusted_return=end.adj_close/a.adj_close-1,price_return=end.close/a.close-1,next_session=nxt.date,next_session_open=nxt.open,next_open_return=end.adj_close/open_adj-1,next_close_return=end.adj_close/nxt.adj_close-1,source_path=source,price_url=x.price_url))
obs=pd.DataFrame(rows);obs.to_csv(D/'company_observations_by_source_date.csv',index=False,encoding='utf-8-sig')
top=co.nsmallest(20,'consensus_rank');series=p.pivot(index='date',columns='symbol',values='adj_close').sort_index().loc['2026-07-13':].ffill()
port=series[top.ticker]/series.loc['2026-07-13',top.ticker];eq=port.mean(axis=1)
paths=pd.DataFrame({'consensus20':eq,'universe192':(series[co.ticker]/series.loc['2026-07-13',co.ticker]).mean(axis=1)})
for b in ['SPY','QQQ','SOXX']:paths[b]=series[b]/series.loc['2026-07-13',b]
paths.to_csv(D/'portfolio_paths.csv',encoding='utf-8-sig')
summary={'observation_days':int(co.n_0713.median()),'universe_positive':int((co.ret_0713>0).sum()),'universe_negative':int((co.ret_0713<0).sum()),'universe_winner20_average':co.nlargest(20,'ret_0713').ret_0713.mean(),'consensus20_mean':top.ret_0713.mean(),'consensus20_median':top.ret_0713.median(),'consensus20_drawdown':float((eq/eq.cummax()-1).min()),'consensus20_top3_contribution':float(top.nlargest(3,'ret_0713').ret_0713.sum()/20),'consensus20_excluding_top3_mean':top.nsmallest(17,'ret_0713').ret_0713.mean(),'consensus20_bottom3_contribution':float(top.nsmallest(3,'ret_0713').ret_0713.sum()/20),'consensus20_next_open_return':obs[(obs.layer=='排序')&obs.ticker.isin(top.ticker)].next_open_return.mean(),'universe_next_open_return':obs[obs.layer=='排序'].next_open_return.mean(),'consensus20_next_close_return':obs[(obs.layer=='排序')&obs.ticker.isin(top.ticker)].next_close_return.mean(),'return_signs_strict':{'positive20':int((co.ret_0713>.2).sum()),'negative20':int((co.ret_0713<-.2).sum())}}
for b in ['SPY','QQQ','SOXX']:summary[b+'_mdd']=float((paths[b]/paths[b].cummax()-1).min())
for excl,name in [(co.exchange!='PNK','exclude_OTC_PNK'),(~co.ticker.isin(['SOMMY','MICLF','ATKR']),'exclude_thin_and_takeover')]:summary[name+'_universe_mean']=co[excl].ret_0713.mean()
n03=['MU','PENG','TSLA','TT','ASX','APLD','BWXT','BDC'];summary['N03_eligible8_mean']=co[co.ticker.isin(n03)].ret_0713.mean()
summary['N03_eligible8_negative']=int((co[co.ticker.isin(n03)].ret_0713<0).sum())
(D/'robustness_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
ev=[('ATKR','2026-08-03'),('AEHR','2026-07-15'),('AEHR','2026-07-21'),('P','2026-08-10'),('P','2026-08-11'),('P','2026-08-27'),('SMCI','2026-07-22'),('SMCI','2026-08-12'),('WDC','2026-08-06'),('MOD','2026-07-29'),('MOD','2026-07-30'),('PENG','2026-07-08')]
er=[]
for sym,date in ev:
    s=p[p.symbol==sym].sort_values('date');a=s[s.date==date].iloc[0];b=s[s.date<date].iloc[-1];er.append(dict(ticker=sym,date=date,previous_close=b.close,close=a.close,adjusted_return=a.adj_close/b.adj_close-1))
pd.DataFrame(er).to_csv(D/'key_event_day_returns.csv',index=False,encoding='utf-8-sig')
print(json.dumps(summary,ensure_ascii=False,indent=2))
