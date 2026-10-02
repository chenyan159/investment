from pathlib import Path
import pandas as pd,numpy as np,hashlib,json
R=Path('D:/drive/Investment');O=R/'备份/company-comparison专项回测_2026-09-05';D=O/'data';OLD=R/'备份/项目反思_2026-09-04/data'
sc=pd.read_csv(OLD/'decisions_historical.csv');resolved=[]
for x in sc.to_dict('records'):
 for kind in ['scenario','evaluation']:
  p=Path(x[kind+'_path'])
  if not p.exists():p=Path(str(p).replace('公司评估_淘汰','备份/公司评估'))
  h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==x[kind+'_sha256'],p
  resolved.append(dict(ticker=x['ticker'],kind=kind,path=p.as_posix(),sha256=h))
pd.DataFrame(resolved).to_csv(D/'historical_source_paths_verified.csv',index=False,encoding='utf-8-sig')
hashes=pd.read_csv(D/'input_hashes.csv');assert all(hashlib.sha256(Path(x.path).read_bytes()).hexdigest()==x.sha256 for x in hashes.itertuples())
raw=pd.read_csv(OLD/'daily_prices.csv');raw.date=pd.to_datetime(raw.date);base=pd.read_csv(OLD/'company_returns.csv').set_index('ticker')
cl=raw.pivot(index='date',columns='symbol',values='adj_close');study=cl.loc['2026-07-15':'2026-09-04',base.vendor_symbol.tolist()]
missing=study.isna().stack();missing=missing[missing].reset_index();missing.to_csv(D/'missing_daily_quotes.csv',index=False,encoding='utf-8-sig')
assert study.ffill().isna().sum().sum()==0
obs=pd.read_csv(D/'price_observations.csv');own=pd.read_csv(D/'192_company_review.csv');assert len(own)==192 and own.return_value.notna().all()
stale=own[own.end_date!='2026-09-04'];assert list(stale.ticker)==['MICLF'] and list(stale.end_date)==['2026-09-03'];stale.to_csv(D/'stale_endpoint.csv',index=False,encoding='utf-8-sig')
evt=[]
for t in ['SMCI','SPY','QQQ']:
 for a,b in [('2026-08-11','2026-08-12'),('2026-07-15','2026-08-11'),('2026-08-11','2026-09-04')]:
  evt.append(dict(ticker=t,start=a,end=b,close_to_close_return=cl.loc[b,t]/cl.loc[a,t]-1))
pd.DataFrame(evt).to_csv(D/'smci_event_windows.csv',index=False,encoding='utf-8-sig')
pm=pd.read_csv(D/'portfolio_metrics.csv');print(pm[(pm.variant=='both')&(pm['mode']=='next_open')&(pm.start_cutoff=='2026-07-18')][['cohort','dimension','top30_return']].to_string(index=False))
print(pd.DataFrame(evt).to_string(index=False))
print(pd.read_csv(D/'dimension_redundancy.csv').sort_values('rank_spearman',ascending=False).head(7).to_string(index=False))
rating=pd.read_csv(D/'scenario_rating_performance.csv');pos=rating[rating.rating.isin(['谨慎建议投资','建议投资','强烈建议投资'])]
out={'verified_comparison_and_input_hashes':len(hashes),'verified_historical_scenario_evaluation_files':len(resolved),'study_price_missing_cells':int(study.isna().sum().sum()),'study_trading_dates':len(study),'endpoints':{'2026-09-04':191,'MICLF_2026-09-03':1},'scenario_positive_37_return':float(np.average(pos.return_0716open,weights=pos.n))}
(D/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(out)
