from pathlib import Path
import pandas as pd,numpy as np,json,re,hashlib
R=Path('D:/drive/Investment');O=R/'备份/company-comparison专项回测_2026-09-05';D=O/'data';OLD=R/'备份/项目反思_2026-09-04/data'
DIMS=['near','long','odds','defense','explosion','mispricing','overall']
def read(n,**kw):return pd.read_csv(D/n,**kw)
def save(n,x):pd.DataFrame(x).to_csv(D/n,index=False,encoding='utf-8-sig')
rank=read('derived_rankings.csv');prices=read('price_observations.csv');p=prices[prices['mode']=='next_open'].set_index(['ticker','report_date'])
base=pd.read_csv(OLD/'company_returns.csv').set_index('ticker');tickers=sorted(base.index);cats=base.category.to_dict()
def ret(t,date):return float(p.loc[(t,date),'return_value'])
e=read('comparison_pair_outcomes_next_open.csv',usecols=['cohort','ticker','opponent','dimension','status','winner','confidence','strength','a_return','b_return','edge','correct','relation','source_line'])
orig=e[e.cohort=='original_0714'];calls=orig[orig.status=='winner'];rr=rank[(rank.cohort=='original_0714')&(rank.variant=='both')].pivot(index='ticker',columns='dimension',values='rank')
sc=read('scenario_and_evaluation_comparison.csv');rating_order={'强烈不建议投资':-2,'不建议投资':-1,'中性 / 等待':0,'谨慎建议投资':0.5,'建议投资':1,'强烈建议投资':2};sc.score=sc.rating.map(rating_order);assert sc.score.notna().all();save('scenario_and_evaluation_comparison.csv',sc)
others=pd.read_csv(OLD/'historical_rankings.csv',dtype={'list_id':str});rmap={k:g.set_index('ticker')['rank'].to_dict() for k,g in others.groupby('list_id')}
rmap['scenario_rating']=(-sc.set_index('ticker').score).to_dict()
for col,asc in [('pre_momentum_63',False),('pre_beta_SPY',True),('pre_momentum_20',False)]:
 rmap['simple_'+col]=pd.to_numeric(base[col]).rank(ascending=asc).to_dict()
inc=[]
for d in DIMS:
 q=calls[calls.dimension==d];a=q.ticker.to_numpy();b=q.opponent.to_numpy();w=q.winner.to_numpy();gap=np.array([ret(t,'2026-07-15') for t in a])-np.array([ret(t,'2026-07-15') for t in b]);ce=np.where(w==a,gap,-gap)
 for lid,rm in rmap.items():
  ar=np.array([rm.get(t,np.nan) for t in a]);br=np.array([rm.get(t,np.nan) for t in b]);valid=np.isfinite(ar)&np.isfinite(br)&(ar!=br);bw=np.where(ar<br,a,b);be=np.where(bw==a,gap,-gap)
  for st,mask in [('all',valid),('agree',valid&(w==bw)),('disagree',valid&(w!=bw))]:
   inc.append(dict(dimension=d,baseline=lid,subset=st,n=int(mask.sum()),comparison_accuracy=np.mean(ce[mask]>0),baseline_accuracy=np.mean(be[mask]>0),comparison_edge=np.mean(ce[mask]),baseline_edge=np.mean(be[mask]),difference=np.mean(ce[mask]-be[mask])))
save('incremental_disagreement.csv',inc)

# Current versus original updates with paired old/new calls, same post-update horizon.
u=read('updated_calls.csv');updates=[]
for d,g in u.groupby('dimension'):
 flip=g[(g.old_status=='winner')&(g.new_status=='winner')];updates.append(dict(dimension=d,changed_cells=len(g),strict_reversals=len(flip),new_correct=float((flip.new_edge>0).mean()),old_correct=float((flip.old_edge>0).mean()),new_edge=float(flip.new_edge.mean()),old_edge=float(flip.old_edge.mean()),became_decisive=int(((g.old_status!='winner')&(g.new_status=='winner')).sum()),became_close=int(((g.old_status=='winner')&(g.new_status!='winner')).sum())))
save('update_summary.csv',updates)

# Good/bad call lists, automatic selection rules declared in the report.
focus=['PENG','P','MOD','WDC','SMCI','MSFT','DELL','ADBE','MU','DHR','AEHR','AAOI','VST','QCOM','ET','SOMMY','HPE']
cr=read('192_company_review.csv').set_index('ticker');save('focus_company_review.csv',cr.loc[focus].reset_index())
rc=read('reciprocal_pairs.csv');conf=rc[(rc.cohort=='original_0714')&(rc.dimension=='overall')&(rc.status.isin(['each_self','each_other']))]
save('largest_conflicts.csv',conf.nlargest(30,'gap_abs'))
agreed=rc[(rc.cohort=='original_0714')&(rc.dimension.isin(['overall','odds','explosion']))&(rc.status=='agreement')].copy();save('largest_agreed_errors.csv',agreed.nsmallest(30,'edge'));save('largest_agreed_successes.csv',agreed.nlargest(30,'edge'))

# Redundancy measured from decisions, not assumed from long text or labels.
red=[]
for d in DIMS:
 for other in DIMS:
  if other<=d:continue
  x=orig[orig.dimension==d].set_index(['ticker','opponent']);y=orig[orig.dimension==other].set_index(['ticker','opponent']);valid=(x.status=='winner')&(y.status=='winner')
  red.append(dict(dimension_a=d,dimension_b=other,both_decisive=int(valid.sum()),same_winner_share=float((x.loc[valid,'winner']==y.loc[valid,'winner']).mean()),rank_spearman=float(rr[d].rank().corr(rr[other].rank()))))
save('dimension_redundancy.csv',red)

# Equal-weight paths and category neutral diagnostics. No fitting to this realized window.
raw=pd.read_csv(OLD/'daily_prices.csv');raw.date=pd.to_datetime(raw.date);raw=raw[raw.date<='2026-09-04'];close=raw.pivot(index='date',columns='symbol',values='adj_close');dates=close.index[close.index>='2026-07-15'];paths=[];exposure=[];rob=[]
for d in DIMS:
 order=rr[d].sort_values().index;top=list(order[:30]);series=[]
 for t in top:
  entry=float(p.loc[(t,'2026-07-14'),'start_adjusted_price']);series.append(close.loc[dates,base.loc[t,'vendor_symbol']]/entry)
 nav=pd.concat(series,axis=1).ffill().mean(axis=1)
 for date,value in nav.items():paths.append(dict(dimension=d,date=str(date.date()),nav=value))
 for cat in sorted(set(cats.values())):
  ts=[t for t in top if cats[t]==cat];pool=[t for t in tickers if cats[t]==cat]
  exposure.append(dict(dimension=d,category=cat,top30_n=len(ts),pool_n=len(pool),top30_weight=len(ts)/30,pool_weight=len(pool)/192,selected_return=np.mean([ret(t,'2026-07-14') for t in ts]) if ts else np.nan,pool_return=np.mean([ret(t,'2026-07-14') for t in pool])))
  # Each category equal weight conditional ranking: report separate, never substitute for original.
 actual=np.array([ret(t,'2026-07-14') for t in tickers]);sector=pd.Series({t:np.mean([ret(s,'2026-07-14') for s in tickers if cats[s]==cats[t]]) for t in tickers});residual=pd.Series(actual,index=tickers)-sector
 usable=[t for t in tickers if base.loc[t,'exchange'] not in ['PNK','OTC'] and p.loc[(t,'2026-07-14'),'zero_volume_days']==0]
 q=calls[(calls.dimension==d)&calls.ticker.isin(usable)&calls.opponent.isin(usable)]
 rob.append(dict(dimension=d,rank_ic_sector_residual=float((-rr.reindex(tickers)[d]).rank().corr(residual.rank())),top30_sector_excess=float(residual.loc[top].mean()),liquid_filter_companies=len(usable),liquid_pair_n=len(q),liquid_pair_accuracy=float(q.correct.mean()),liquid_pair_edge=float(q.edge.mean())))
for t in ['SPY','QQQ','SOXX']:
 nav=close.loc[dates,t]/p.loc[(t,'2026-07-14'),'start_adjusted_price']
 for date,value in nav.items():paths.append(dict(dimension=t,date=str(date.date()),nav=value))
save('portfolio_paths.csv',paths);save('category_exposure.csv',exposure);save('sector_liquidity_robustness.csv',rob)

# Confidence strata within each relationship type; no numerical probability assigned to verbal confidence.
cf=[]
for (d,c,rel),g in calls.groupby(['dimension','confidence','relation']):cf.append(dict(dimension=d,confidence=c,relation=rel,n=len(g),accuracy=g.correct.mean(),mean_edge=g.edge.mean()))
save('confidence_by_relation.csv',cf)

# Every report has its own dated stock observation; compare recommendations on that same cutoff.
score=read('report_performance.csv'); own=score[(score.cohort=='latest_0718')&(score.dimension=='overall')&(score['mode']=='next_open')];save('192_report_accuracy_ranked.csv',own.sort_values('accuracy',ascending=False))
change=rank[(rank.variant=='both')&(rank.dimension=='overall')].pivot(index='ticker',columns='cohort',values='rank');change['rank_change']=change.original_0714-change.latest_0718;save('update_rank_changes.csv',change.reset_index().sort_values('rank_change',ascending=False))
summary={'price_origin':'Frozen raw daily prices collected 2026-09-04, no later trading session by 2026-09-05. Adjusted open = raw open * adjusted close / raw close.','peer_observations':'Repeated stock pairs are dependent; no binomial significance or 256k independent trials claim.','rank_method':'Both directions net wins; ties by wins then losses then ticker, fixed before inspecting this backtest. Other views are sensitivity only.','scenario_cautious_rating_included':int((sc.rating=='谨慎建议投资').sum()),'liquid_filter':'Diagnostic exclusion of PNK/OTC exchange or any zero-volume days; does not certify tradability of remaining names.','omitted_price_rows':'Six raw records lacked usable open/close/adj_close or positive prices; not fill-zero returns.'}
(D/'extended_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(pd.DataFrame(updates).to_string(index=False));print(pd.DataFrame(rob).to_string(index=False));print(pd.DataFrame(red).query("dimension_a=='odds' or dimension_b=='overall'").to_string(index=False))
