from pathlib import Path
import pandas as pd,re,json,hashlib
R=Path('D:/drive/Investment');O=R/'备份/company-comparison专项回测_2026-09-05';D=O/'data';OLD=R/'备份/项目反思_2026-09-04/data'
links=[];bad=[]
for p in O.glob('*.md'):
 for match in re.finditer(r'\]\(<(D:/[^>]+)>\)',p.read_text(encoding='utf-8')):
  dest=match[1];m=re.match(r'^(.*):(\d+)$',dest);target=Path(m[1] if m else dest)
  if not target.exists():bad.append([p.name,dest,'missing'])
  elif m and int(m[2])>len(target.read_text(encoding='utf-8-sig').splitlines()):bad.append([p.name,dest,'badline'])
  links.append(dest)
assert not bad,bad
historical=pd.read_csv(OLD/'historical_rankings.csv',keep_default_na=False);checks=[]
for x in historical.itertuples():
 p=Path(x.source_path);ls=p.read_text(encoding='utf-8-sig').splitlines();line=ls[int(x.source_line)-1]
 # Source lines must still contain both the security and exact integer rank, allowing Markdown markup.
 assert re.search(r'(?<![A-Z0-9])'+re.escape(x.ticker)+r'(?![A-Z0-9])',line),(p,x.ticker,line)
 rank_match=re.match(r'^\|\s*(?:\*\*)?(\d+)',line.strip());assert rank_match and int(rank_match[1])==int(x.rank),(p,x.rank,line)
 checks.append((p.as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()))
pd.DataFrame(sorted(set(checks)),columns=['path','sha256']).to_csv(D/'ranking_source_hashes_verified.csv',index=False,encoding='utf-8-sig')
q=pd.read_csv(D/'qcom_net_cash_claim_screen.csv');assert len(q)==42 and q.report_ticker.nunique()==38
pm=pd.read_csv(D/'portfolio_metrics.csv');z=pm[(pm.cohort=='original_0714')&(pm.variant=='both')&(pm.start_cutoff=='2026-07-14')&(pm['mode']=='next_open')]
own=pd.read_csv(D/'192_company_review.csv').set_index('ticker');errs=[]
for x in z.itertuples():
 ts=x.top30_tickers.split(',');manual=own.loc[ts,'return_original_0715open'].mean();assert abs(manual-x.top30_return)<1e-12
rec=pd.read_csv(D/'reciprocal_metrics.csv');rec=rec[(rec.cohort=='original_0714')&(rec.dimension=='overall')];assert rec.pairs.sum()==18336
conf=int(rec[rec.status.isin(['each_self','each_other'])].pairs.sum());assert conf==3344,conf
price=pd.read_csv(D/'price_observations.csv');spy=price[(price.ticker=='SPY')&(price.report_date=='2026-07-14')&(price['mode']=='next_open')].iloc[0].return_value
assert abs(spy-0.0211471314350155)<1e-10
out=dict(local_links_checked=len(links),unique_link_targets=len(set(links)),broken_links=bad,ranking_rows_source_ticker_checked=len(checks),ranking_source_files=len(set(checks)),qcom_claims=len(q),qcom_report_count=q.report_ticker.nunique(),seven_top30_return_recomputations='passed',strict_overall_conflicts=conf,spy_return=float(spy))
(D/'final_qa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False,indent=2))
