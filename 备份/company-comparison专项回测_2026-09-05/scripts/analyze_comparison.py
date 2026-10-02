from pathlib import Path
from collections import defaultdict,Counter
import pandas as pd,numpy as np,json,re,hashlib
ROOT=Path('D:/drive/Investment'); OUT=ROOT/'备份/company-comparison专项回测_2026-09-05'; OLD=ROOT/'备份/项目反思_2026-09-04/data'
for d in ['data','evidence','scripts','figures']: (OUT/d).mkdir(parents=True,exist_ok=True)
DIMS=['near','long','odds','defense','explosion','mispricing','overall']
NAMES=dict(zip(DIMS,['近端兑现','长期复利','价格赔率','防守保全','爆发突破','定价错位','总体判断']))
snapshots={};warnings=[]
def snap(p):
 p=Path(p);snapshots[p.as_posix()]={'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def csvout(n,x):
 pd.DataFrame(x).to_csv(OUT/'data'/n,index=False,encoding='utf-8-sig')
def readcsv(n):
 p=OLD/n;snap(p);return pd.read_csv(p,keep_default_na=False)
def clean(s):return re.sub(r'<br\s*/?>',' ',re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s)).replace('**','').replace('`','').strip()
def outcome(raw,a,b):
 s=clean(raw);conf=re.search(r'(中高|中低|高|中|低)置信',s) or re.search(r'[（(](中高|中低|高|中|低)[）)]',s)
 if re.match('接近|难分|大致平衡|基本平衡',s):return 'close','',conf[1] if conf else '',0,s
 if re.match('资料不足|信息不足|无法判断|不可判断',s):return 'unavailable','','',0,s
 m=re.match(r'^([A-Z0-9.-]+)\s*(?=明显更优|略优|更优|：|:|（|\(|$)',s)
 w=m[1] if m else ''; w={'A':a,'B':b,'PSTG':'P','AGC':'ASGLY'}.get(w,w)
 return 'winner' if w in [a,b] else 'invalid',w,conf[1] if conf else '',2 if '明显更优' in s else 1,s
def parse(p,a,date,cohort):
 snap(p);rows=[];ls=p.read_text(encoding='utf-8-sig').splitlines()
 for i,l in enumerate(ls,1):
  if not re.match(r'^\|\s*\d+\s*\|',l.strip()):continue
  cells=[c.strip() for c in re.split(r'(?<!\\)\|',l.strip().strip('|'))]
  if len(cells)!=12:continue
  m=re.match(r'^([A-Z][A-Z0-9.-]*)',clean(cells[1]))
  if not m:continue
  b={'PSTG':'P'}.get(m[1],m[1]);r=dict(cohort=cohort,ticker=a,opponent=b,report_date=date,source_path=p.as_posix(),source_line=i,relation=clean(cells[3]),reason=clean(cells[11]))
  for d,raw in zip(DIMS,cells[4:11]):
   st,w,c,strength,txt=outcome(raw,a,b)
   r.update({d+'_status':st,d+'_winner':w,d+'_confidence':c,d+'_strength':strength,d+'_text':txt})
   if st=='invalid':warnings.append(dict(cohort=cohort,ticker=a,opponent=b,dimension=d,text=txt))
  rows.append(r)
 assert len(rows)==191 and len({r['opponent'] for r in rows})==191,(p,len(rows))
 return rows
historical=readcsv('company_comparison_historical_sources.csv'); allrows=[];source_rows=[]
for r in historical.to_dict('records'):
 p=Path(r['source_path']); assert hashlib.sha256(p.read_bytes()).hexdigest()==r['source_sha256']
 allrows+=parse(p,r['ticker'],r['run_date'],'original_0714')
 source_rows.append(dict(cohort='original_0714',ticker=r['ticker'],report_date=r['run_date'],path=p.as_posix(),sha256=snapshots[p.as_posix()]['sha256']))
for p in sorted((ROOT/'分析报告/公司对比/结果').glob('*_逐家公司投资思路对比_*.md')):
 m=re.match(r'^(.+)_逐家公司投资思路对比_(\d{4}-\d{2}-\d{2})\.md$',p.name)
 if not m:continue
 a,date=m.groups();allrows+=parse(p,a,date,'latest_0718')
 source_rows.append(dict(cohort='latest_0718',ticker=a,report_date=date,path=p.as_posix(),sha256=snapshots[p.as_posix()]['sha256']))
pairs=pd.DataFrame(allrows);assert len(pairs)==2*192*191
csvout('source_reports.csv',source_rows);csvout('parse_warnings.csv',warnings)
tickers=sorted(historical.ticker);ix={t:i for i,t in enumerate(tickers)}
base=readcsv('company_returns.csv').set_index('ticker'); cats=base.category.to_dict()
raw=readcsv('daily_prices.csv');raw.date=pd.to_datetime(raw.date)
for col in ['open','high','low','close','volume','adj_close']:raw[col]=pd.to_numeric(raw[col],errors='coerce')
raw=raw.dropna(subset=['open','close','adj_close']);raw=raw[(raw.open>0)&(raw.close>0)&(raw.adj_close>0)]
raw['adj_open']=raw.open*(raw.adj_close/raw.close)
raw=raw[raw.date<=pd.Timestamp('2026-09-04')]
price={s:x.sort_values('date').set_index('date') for s,x in raw.groupby('symbol')}
symbols={t:base.loc[t,'vendor_symbol'] for t in tickers}; symbols.update({t:t for t in ['SPY','QQQ','SOXX']})
cache={}
def obs(t,date,mode):
 key=(t,date,mode)
 if key in cache:return cache[key]
 x=price[symbols[t]];target=pd.Timestamp(date)
 # Report-close sensitivity uses prior close for a weekend; that is not executable after publication.
 start=x[x.index<=target].iloc[-1] if mode=='report_close' else x[x.index>target].iloc[0]
 dt=start.name;end=x.iloc[-1];field='adj_close' if mode=='report_close' else 'adj_open';entry=float(start[field])
 path=x[x.index>=dt].adj_close/entry;path=np.r_[1.,path.to_numpy()]
 mdd=float(np.min(path/np.maximum.accumulate(path)-1))
 val=dict(ticker=t,report_date=date,mode=mode,start_date=dt.strftime('%Y-%m-%d'),end_date=end.name.strftime('%Y-%m-%d'),start_raw_price=float(start['close' if mode=='report_close' else 'open']),start_adjusted_price=entry,end_raw_close=float(end.close),end_adjusted_close=float(end.adj_close),return_value=float(end.adj_close/entry-1),mdd=mdd,trading_closes=len(path)-1,zero_volume_days=int((x.loc[dt:].volume==0).sum()),currency=base.loc[t,'currency'] if t in base.index else 'USD',exchange=base.loc[t,'exchange'] if t in base.index else '',source_url=base.loc[t,'price_url'] if t in base.index else '')
 cache[key]=val;return val
dates=['2026-07-12','2026-07-13','2026-07-14','2026-07-15','2026-07-18']
for t in symbols:
 for date in dates:
  for mode in ['next_open','report_close']:obs(t,date,mode)
csvout('price_observations.csv',cache.values())
rankrows=[];rankmetrics=[];groupmetrics=[];recips=[];pair_metrics=[];matrixmetrics=[];perreport=[];update_rows=[];panel_edges=[]
def portfolio(ts,date,mode):
 ts=list(ts);os=[obs(t,date,mode) for t in ts];start=os[0]['start_date']
 series=[]
 for t,o in zip(ts,os): series.append(price[symbols[t]].loc[pd.Timestamp(start):,'adj_close']/o['start_adjusted_price'])
 nav=pd.concat(series,axis=1).ffill().mean(axis=1);arr=np.r_[1.,nav.to_numpy()];mdd=np.min(arr/np.maximum.accumulate(arr)-1)
 return float(np.mean([o['return_value'] for o in os])),float(mdd)
def metric_rank(df,date,mode,**meta):
 rets=df.ticker.map(lambda t:obs(t,date,mode)['return_value']); top=df.nsmallest(30,'rank');bot=df.nlargest(30,'rank')
 top_ret,mdd=portfolio(top.ticker,date,mode);bottom,_=portfolio(bot.ticker,date,mode)
 real=set(sorted(tickers,key=lambda t:obs(t,date,mode)['return_value'],reverse=True)[:30]);bench=obs('SPY',date,mode)['return_value']
 return dict(**meta,start_cutoff=date,mode=mode,n=len(df),top30_return=top_ret,bottom30_return=bottom,spread=top_ret-bottom,top30_mdd=mdd,top30_excess_spy=top_ret-bench,top30_excess_pool=top_ret-np.mean([obs(t,date,mode)['return_value'] for t in tickers]),rank_ic=float(pd.Series(-df['rank'].to_numpy()).rank().corr(pd.Series(rets.to_numpy()).rank())),winner30_capture=len(set(top.ticker)&real),top30_positive=int(sum(obs(t,date,mode)['return_value']>0 for t in top.ticker)),top30_tickers=','.join(top.ticker),bottom30_tickers=','.join(bot.ticker))
for cohort,frame in pairs.groupby('cohort'):
 cutoff='2026-07-14' if cohort=='original_0714' else '2026-07-18';pm={(r['ticker'],r['opponent']):r for r in frame.to_dict('records')}
 for d in DIMS:
  for mode in ['next_open','report_close']:
   z=frame.copy();z['winner']=z[d+'_winner'];z['status']=z[d+'_status'];z['confidence']=z[d+'_confidence'];z['strength']=z[d+'_strength']
   z['a_return']=[obs(a,dt,mode)['return_value'] for a,dt in zip(z.ticker,z.report_date)]
   z['b_return']=[obs(b,dt,mode)['return_value'] for b,dt in zip(z.opponent,z.report_date)]
   z['edge']=np.where(z.winner==z.ticker,z.a_return-z.b_return,z.b_return-z.a_return)
   z['correct']=z.edge>0;z['abs_gap']=abs(z.a_return-z.b_return)
   def summarise(q,typ,label):
    v=q[q.status=='winner'];pair_metrics.append(dict(cohort=cohort,dimension=d,mode=mode,group_type=typ,group=label,all_rows=len(q),decisive=len(v),accuracy=float(v.correct.mean()) if len(v) else np.nan,mean_edge=float(v.edge.mean()) if len(v) else np.nan,median_edge=float(v.edge.median()) if len(v) else np.nan,selection_coverage=len(v)/len(q) if len(q) else np.nan))
   summarise(z,'all','all')
   for key in ['confidence','strength','relation','report_date']:
    for val,q in z.groupby(key):summarise(q,key,str(val))
   for a,q in z.groupby('ticker'):
    v=q[q.status=='winner'];perreport.append(dict(cohort=cohort,ticker=a,dimension=d,mode=mode,report_date=q.report_date.iloc[0],own_return=obs(a,q.report_date.iloc[0],mode)['return_value'],decisive=len(v),accuracy=float(v.correct.mean()),mean_edge=float(v.edge.mean()),self_wins=int((v.winner==a).sum()),opponent_wins=int((v.winner!=a).sum())))
   if mode=='next_open':
    cols=['cohort','ticker','opponent','report_date','source_path','source_line','relation','reason']
    zz=z[cols+['winner','status','confidence','strength','a_return','b_return','edge','correct']].copy();zz['dimension']=d
    panel_edges+=zz.to_dict('records')
  scores={v:{t:Counter(wins=0,losses=0,points=0) for t in tickers} for v in ['both','self_only','other_only','agreement_only','high_only','strength_weighted']}
  for r in frame.to_dict('records'):
   a,b=r['ticker'],r['opponent'];w=r[d+'_winner']
   if r[d+'_status']!='winner':continue
   loser=b if w==a else a
   for v in ['both','high_only','strength_weighted']:
    if v=='high_only' and r[d+'_confidence']!='高':continue
    wt=r[d+'_strength'] if v=='strength_weighted' else 1
    scores[v][w]['wins']+=1;scores[v][loser]['losses']+=1;scores[v][w]['points']+=wt;scores[v][loser]['points']-=wt
   for v,t in [('self_only',a),('other_only',b)]:
    iswin=w==t;scores[v][t]['wins' if iswin else 'losses']+=1;scores[v][t]['points']+=1 if iswin else -1
  adjacency=np.zeros((192,192),dtype=np.int64);recgroup=defaultdict(list)
  for i,a in enumerate(tickers):
   for b in tickers[i+1:]:
    x,y=pm[a,b],pm[b,a];sx,sy=x[d+'_status'],y[d+'_status'];wx,wy=x[d+'_winner'],y[d+'_winner']
    if 'unavailable' in [sx,sy] or 'invalid' in [sx,sy]:st='unavailable'
    elif sx==sy=='close':st='both_close'
    elif 'close' in [sx,sy]:st='one_close'
    elif wx==wy:st='agreement'
    elif wx==a and wy==b:st='each_self'
    else:st='each_other'
    oa,ob=obs(a,cutoff,'next_open'),obs(b,cutoff,'next_open');gap=oa['return_value']-ob['return_value']
    edge=gap if wx==a else -gap
    recgroup[st].append((edge,abs(gap)))
    recips.append(dict(cohort=cohort,dimension=d,a=a,b=b,status=st,a_date=x['report_date'],b_date=y['report_date'],a_text=x[d+'_text'],b_text=y[d+'_text'],a_source=x['source_path'],a_line=x['source_line'],b_source=y['source_path'],b_line=y['source_line'],a_return=oa['return_value'],b_return=ob['return_value'],gap_abs=abs(gap),winner=wx if st=='agreement' else '',correct=edge>0 if st=='agreement' else '',edge=edge if st=='agreement' else '',relation=x['relation'],reverse_relation=y['relation']))
    if st=='agreement':
     loser=b if wx==a else a;scores['agreement_only'][wx]['wins']+=1;scores['agreement_only'][loser]['losses']+=1;scores['agreement_only'][wx]['points']+=1;scores['agreement_only'][loser]['points']-=1
     adjacency[ix[wx],ix[loser]]=1
  cycle=int(np.trace(adjacency@adjacency@adjacency)//3);und=adjacency+adjacency.T;complete=int(np.trace(und@und@und)//6)
  matrixmetrics.append(dict(cohort=cohort,dimension=d,agreed_edges=int(adjacency.sum()),complete_triplets=complete,cycles=cycle,cycle_share=cycle/complete if complete else 0))
  for st,vs in recgroup.items():groupmetrics.append(dict(cohort=cohort,dimension=d,status=st,pairs=len(vs),accuracy=np.mean([e>0 for e,g in vs]) if st=='agreement' else np.nan,mean_edge=np.mean([e for e,g in vs]) if st=='agreement' else np.nan,mean_absolute_gap=np.mean([g for e,g in vs])))
  for v,sc in scores.items():
   order=sorted(tickers,key=lambda t:(-sc[t]['points'],-sc[t]['wins'],sc[t]['losses'],t));rr=pd.DataFrame([dict(cohort=cohort,dimension=d,variant=v,ticker=t,rank=i+1,**sc[t]) for i,t in enumerate(order)])
   rankrows+=rr.to_dict('records')
   for date in sorted(set([cutoff,'2026-07-15','2026-07-18'])):
    # July18 updates are never tested from before the full current cohort became available.
    if date<cutoff:continue
    for mode in ['next_open','report_close']:rankmetrics.append(metric_rank(rr,date,mode,cohort=cohort,dimension=d,variant=v))
csvout('comparison_pairs_parsed.csv',pairs);csvout('comparison_pair_outcomes_next_open.csv',panel_edges)
csvout('pair_accuracy.csv',pair_metrics);csvout('report_performance.csv',perreport);csvout('reciprocal_pairs.csv',recips);csvout('reciprocal_metrics.csv',groupmetrics);csvout('preference_cycles.csv',matrixmetrics);csvout('derived_rankings.csv',rankrows);csvout('portfolio_metrics.csv',rankmetrics)
rankdf=pd.DataFrame(rankrows);perf=pd.DataFrame(rankmetrics);edges=pd.DataFrame(panel_edges)

# Other ranking methods on precisely the same investment windows; no optimization of weights.
others=readcsv('historical_rankings.csv');other_metrics=[];rankmap={}
for lid,df in others.groupby('list_id'):
 df=df.copy();df['rank']=pd.to_numeric(df['rank']);rankmap[str(lid)]=df.set_index('ticker')['rank'].to_dict()
 for date in ['2026-07-14','2026-07-15','2026-07-18']:
  other_metrics.append(metric_rank(df,date,'next_open',family='ranking',method=str(lid),name=df.method_name.iloc[0]))
csvout('other_ranking_metrics.csv',other_metrics)

# Scenario labels are conditional advice. Preserve original scope and separate unclassified reports.
dec=readcsv('decisions_historical.csv');rating_order={'强烈不建议投资':-2,'不建议投资':-1,'中性':0,'中性 / 等待':0,'谨慎建议投资':0.5,'建议投资':1,'强烈建议投资':2}
scenario_rows=[]
for r in dec.to_dict('records'):
 rating=r['current_condition_rating_reviewed'];val=rating_order.get(rating,np.nan)
 scenario_rows.append(dict(ticker=r['ticker'],rating=rating,score=val,scenario_date=r['scenario_report_date'],source_path=r['scenario_path'],summary_line=r['summary_line'],summary_text=r['summary_text'],return_0716open=obs(r['ticker'],'2026-07-15','next_open')['return_value'],return_0720open=obs(r['ticker'],'2026-07-18','next_open')['return_value'],evaluation_path=r['evaluation_path'],evaluation_boundary=r['evaluation_scope_text'],evaluation_baseline=r['evaluation_baseline_revenue_text']))
scen=pd.DataFrame(scenario_rows);csvout('scenario_and_evaluation_comparison.csv',scen)
sg=[]
for label,q in scen.groupby('rating'):
 sg.append(dict(rating=label,n=len(q),return_0716open=q.return_0716open.mean(),return_0720open=q.return_0720open.mean(),tickers=','.join(q.ticker)))
csvout('scenario_rating_performance.csv',sg)

# Disagreement comparisons use common July16 open and original July14 comparison only.
inc=[];ranksignals=rankmap.copy();ranksignals['scenario_rating']={r.ticker:-r.score for r in scen.itertuples() if np.isfinite(r.score)}
original=edges[(edges.cohort=='original_0714') & (edges.status=='winner')].copy()
for d in DIMS:
 e=original[original.dimension==d].copy();a=e.ticker.to_numpy();b=e.opponent.to_numpy();w=e.winner.to_numpy()
 ra=np.array([obs(t,'2026-07-15','next_open')['return_value'] for t in a]);rb=np.array([obs(t,'2026-07-15','next_open')['return_value'] for t in b]);c_edge=np.where(w==a,ra-rb,rb-ra)
 for lid,rmap in ranksignals.items():
  ar=np.array([rmap.get(t,np.nan) for t in a]);br=np.array([rmap.get(t,np.nan) for t in b]);valid=np.isfinite(ar)&np.isfinite(br)&(ar!=br);ow=np.where(ar<br,a,b);be=np.where(ow==a,ra-rb,rb-ra)
  for subset,mask in [('all',valid),('agree',valid&(w==ow)),('disagree',valid&(w!=ow))]:
   inc.append(dict(dimension=d,baseline=lid,subset=subset,n=int(mask.sum()),comparison_accuracy=float(np.mean(c_edge[mask]>0)),baseline_accuracy=float(np.mean(be[mask]>0)),comparison_edge=float(np.mean(c_edge[mask])),baseline_edge=float(np.mean(be[mask])),difference=float(np.mean(c_edge[mask]-be[mask]))))
csvout('incremental_disagreement.csv',inc)

# Fifteen/July18 updates: identical securities, identical later window for old vs new calls.
update=[]
oldpm={(r['ticker'],r['opponent']):r for r in pairs[pairs.cohort=='original_0714'].to_dict('records')}
updated=pairs[(pairs.cohort=='latest_0718')&(pairs.report_date=='2026-07-18')]
for r in updated.to_dict('records'):
 o=oldpm[r['ticker'],r['opponent']];a,b=r['ticker'],r['opponent'];gap=obs(a,'2026-07-18','next_open')['return_value']-obs(b,'2026-07-18','next_open')['return_value']
 for d in DIMS:
  if r[d+'_winner']!=o[d+'_winner'] or r[d+'_status']!=o[d+'_status']:
   oldedge=(gap if o[d+'_winner']==a else -gap) if o[d+'_status']=='winner' else np.nan;newedge=(gap if r[d+'_winner']==a else -gap) if r[d+'_status']=='winner' else np.nan
   update.append(dict(ticker=a,opponent=b,dimension=d,old_status=o[d+'_status'],new_status=r[d+'_status'],old_winner=o[d+'_winner'],new_winner=r[d+'_winner'],old_text=o[d+'_text'],new_text=r[d+'_text'],old_edge=oldedge,new_edge=newedge,old_source=o['source_path'],old_line=o['source_line'],new_source=r['source_path'],new_line=r['source_line']))
csvout('updated_calls.csv',update)

# Robustness: leave one company out in pair evaluation, and market/sector exposure in rank evaluation.
rob=[]
for d in DIMS:
 e=original[original.dimension==d];acc=e.correct.astype(float).to_numpy();edge=e.edge.to_numpy();vals=[]
 for t in tickers:
  q=e[(e.ticker!=t)&(e.opponent!=t)];vals.append((t,q.correct.mean(),q.edge.mean()))
 worst=min(vals,key=lambda x:x[1]);best=max(vals,key=lambda x:x[1]);rob.append(dict(dimension=d,accuracy=acc.mean(),mean_edge=edge.mean(),leave_one_min_accuracy=worst[1],leave_one_min_ticker=worst[0],leave_one_max_accuracy=best[1],leave_one_max_ticker=best[0]))
csvout('leave_one_company_out.csv',rob)
diag=[]
for d in DIMS:
 q=rankdf[(rankdf.cohort=='original_0714')&(rankdf.dimension==d)&(rankdf.variant=='both')].set_index('ticker').reindex(tickers)
 for factor in ['pre_momentum_20','pre_momentum_63','pre_beta_SPY','pre_beta_QQQ']:
  diag.append(dict(dimension=d,measure=factor,spearman=float(pd.Series(-q['rank'].to_numpy()).rank().corr(pd.Series(pd.to_numeric(base.reindex(tickers)[factor]).to_numpy()).rank()))))
 csvout('rank_factor_diagnostics.csv',diag)
for cohort in ['original_0714','latest_0718']:
 q=rankdf[(rankdf.cohort==cohort)&(rankdf.variant=='both')].pivot(index='ticker',columns='dimension',values='rank');q.rank().corr().to_csv(OUT/'data'/f'dimension_correlation_{cohort}.csv',encoding='utf-8-sig')

# A company-level workbook table: own last report returns plus all seven derived ranks, original and updated.
company=[];sr=pd.DataFrame(source_rows);currentdates=sr[sr.cohort=='latest_0718'].set_index('ticker').report_date.to_dict()
for t in tickers:
 r=dict(ticker=t,company=base.loc[t,'company'],category=cats[t],last_report_date=currentdates[t],**{k:v for k,v in obs(t,currentdates[t],'next_open').items() if k not in ['ticker','report_date']})
 for cohort in ['original_0714','latest_0718']:
  for d in DIMS:r[cohort+'_'+d+'_rank']=int(rankdf[(rankdf.cohort==cohort)&(rankdf.variant=='both')&(rankdf.dimension==d)&(rankdf.ticker==t)]['rank'].iloc[0])
 r['return_original_0715open']=obs(t,'2026-07-14','next_open')['return_value'];r['return_latest_common_0720open']=obs(t,'2026-07-18','next_open')['return_value'];r['scenario_rating']=scen.set_index('ticker').loc[t,'rating'];r['ranking_consensus_rank']=base.loc[t,'consensus_rank'];company.append(r)
csvout('192_company_review.csv',company)
for p in [ROOT/'分析报告/公司对比/研究方案.md',ROOT/'tools/research-runner/domains/company-comparison.mjs',ROOT/'tools/research-runner/prompts/company-comparison.mjs']:snap(p)
csvout('input_hashes.csv',snapshots.values())
summary=dict(reports_by_cohort={c:dict(g.report_date.value_counts()) for c,g in sr.groupby('cohort')},unique_comparison_files=sr.path.nunique(),rows=len(pairs),parse_warnings=len(warnings),updated_company_count=updated.ticker.nunique(),updated_tickers=sorted(updated.ticker.unique()),end_date='2026-09-04',prices_rows=len(raw),source_hashes=len(snapshots))
(OUT/'data/summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=int),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2,default=int))
print(perf.query("cohort=='original_0714' and variant=='both' and start_cutoff=='2026-07-14' and mode=='next_open'")[['dimension','top30_return','top30_mdd','rank_ic','winner30_capture']].to_string(index=False))
print(pd.DataFrame(pair_metrics).query("cohort=='original_0714' and mode=='next_open' and group_type=='all'")[['dimension','decisive','accuracy','mean_edge']].to_string(index=False))

