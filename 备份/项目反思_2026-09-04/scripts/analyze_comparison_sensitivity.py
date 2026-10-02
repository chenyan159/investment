from pathlib import Path
from collections import Counter
import json
import numpy as np
import pandas as pd

OUT=Path('D:/drive/Investment/备份/项目反思_2026-09-04'); DATA=OUT/'data'
pairs=pd.read_csv(DATA/'company_comparison_historical_pairs.csv').fillna('')
summary=pd.read_csv(DATA/'company_comparison_historical.csv')
prices=pd.read_csv(DATA/'all_returns_and_benchmarks.csv').set_index('ticker')
retcol='ret_0714'
merged=summary.join(prices[[retcol]],on='ticker')
dimensions=['near','long','odds','defense','explosion','mispricing','overall']
tickers=sorted(summary.ticker); pairmap={(r.ticker,r.opponent):r for r in pairs.itertuples(index=False)}
metrics=[]; ranks=[]; reciprocal_accuracy=[]
for d in dimensions:
    stats={v:{t:Counter(wins=0,losses=0,close=0) for t in tickers} for v in ['self_reports','opponent_reports','same_winner_only']}
    for row in pairs.to_dict('records'):
        a,b=row['ticker'],row['opponent'];winner=row[d+'_winner'];status=row[d+'_status']
        if status=='winner':
            stats['self_reports'][a]['wins' if winner==a else 'losses']+=1
            stats['opponent_reports'][b]['wins' if winner==b else 'losses']+=1
    for i,a in enumerate(tickers):
        for b in tickers[i+1:]:
            x,y=pairmap[a,b],pairmap[b,a]
            sx,sy=getattr(x,d+'_status'),getattr(y,d+'_status');wx,wy=getattr(x,d+'_winner'),getattr(y,d+'_winner')
            if sx==sy=='winner' and wx==wy:
                stats['same_winner_only'][wx]['wins']+=1;stats['same_winner_only'][b if wx==a else a]['losses']+=1
    variations={'all_directions':merged[['ticker',d+'_rank',retcol]].rename(columns={d+'_rank':'rank'}).copy()}
    for variant,st in stats.items():
        ordered=sorted(tickers,key=lambda t:(-(st[t]['wins']-st[t]['losses']),-st[t]['wins'],st[t]['losses'],t))
        df=pd.DataFrame([dict(ticker=t,rank=i+1,wins=st[t]['wins'],losses=st[t]['losses'],net=st[t]['wins']-st[t]['losses']) for i,t in enumerate(ordered)])
        variations[variant]=df.join(prices[[retcol]],on='ticker')
    base_top=set(variations['all_directions'].nsmallest(20,'rank').ticker)
    for variant,df in variations.items():
        top=df.nsmallest(20,'rank');bottom=df.nlargest(20,'rank');valid=df.dropna(subset=[retcol]); rankic=valid['rank'].rank().corr(valid[retcol].rank())*-1
        metrics.append(dict(dimension=d,variant=variant,start_date='2026-07-14',n=len(valid),top20_n=top[retcol].notna().sum(),rank_ic=rankic,top20_return=top[retcol].mean(),bottom20_return=bottom[retcol].mean(),top20_bottom20=top[retcol].mean()-bottom[retcol].mean(),top20_positive_share=(top[retcol]>0).mean(),top20_overlap_original=len(base_top & set(top.ticker)),top20_tickers=','.join(top.sort_values('rank').ticker)))
        for _,r in df.iterrows():ranks.append(dict(dimension=d,variant=variant,**r.to_dict()))
    s=variations['self_reports'].set_index('ticker');o=variations['opponent_reports'].set_index('ticker')
    print(d,'direction_rank_correlation',s['rank'].rank().corr(o['rank'].rank()),'top20overlap',len(set(s.nsmallest(20,'rank').index)&set(o.nsmallest(20,'rank').index)))
pd.DataFrame(metrics).to_csv(DATA/'company_comparison_forward_metrics.csv',index=False,encoding='utf-8-sig')
pd.DataFrame(ranks).to_csv(DATA/'company_comparison_sensitivity_rankings.csv',index=False,encoding='utf-8-sig')

# Conflict examples with performance dispersion, relation and strength retained.
conf=pd.read_csv(DATA/'company_comparison_reciprocal_conflicts.csv')
conf=conf.join(prices[[retcol]],on='ticker_a').rename(columns={retcol:'a_return'}).join(prices[[retcol]],on='ticker_b').rename(columns={retcol:'b_return'})
conf['return_gap']=(conf.a_return-conf.b_return).abs()
conf['overall_a_rank']=conf.ticker_a.map(merged.set_index('ticker').overall_rank)
conf['overall_b_rank']=conf.ticker_b.map(merged.set_index('ticker').overall_rank)
conf['relation']=conf.apply(lambda r:pairmap[r.ticker_a,r.ticker_b].relation,axis=1)
conf['reverse_relation']=conf.apply(lambda r:pairmap[r.ticker_b,r.ticker_a].relation,axis=1)
conf.to_csv(DATA/'company_comparison_conflicts_with_returns.csv',index=False,encoding='utf-8-sig')
focus=conf[(conf.dimension=='overall') & ((conf.overall_a_rank<=20)|(conf.overall_b_rank<=20))].nlargest(25,'return_gap')
focus.to_csv(DATA/'company_comparison_focus_conflicts.csv',index=False,encoding='utf-8-sig')
print(pd.DataFrame(metrics).query("variant in ['all_directions','same_winner_only']")[['dimension','variant','rank_ic','top20_return','top20_bottom20','top20_overlap_original']].to_string(index=False))
print(focus[['ticker_a','ticker_b','conflict','a_text','b_text','a_return','b_return','relation']].head(12).to_string(index=False))
