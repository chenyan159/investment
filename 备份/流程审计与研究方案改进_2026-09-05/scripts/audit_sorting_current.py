from pathlib import Path
import json,re,hashlib
import numpy as np
import pandas as pd
ROOT=Path('D:/drive/Investment');RR=ROOT/'分析报告/公司排序';OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05';OLD=ROOT/'备份/项目反思_2026-09-04/data'
reg=pd.read_csv(RR/'00_运行与榜单注册表.csv',dtype=str)
pol=pd.read_csv(RR/'00_站点发布策略.csv',dtype=str).set_index('method_id')
prior=pd.read_csv(OLD/'historical_rankings.csv',dtype={'method_id':str,'list_id':str})
ret=pd.read_csv(OLD/'company_returns.csv').set_index('ticker')
daily=pd.read_csv(OLD/'daily_prices.csv')
first=daily[daily.date.eq('2026-07-14')].set_index('symbol')
start=first.open*first.adj_close/first.close
ret['ret_next_open']=ret.end_adj_close/ret.vendor_symbol.map(start)-1
winner30=set(ret.nlargest(30,'ret_0713').index)
metrics=[]
for lid,g in prior.groupby('list_id',sort=False):
    f=g.sort_values('rank').join(ret,on='ticker',rsuffix='_return')
    t=f.head(30);b=f.tail(30)
    metrics.append(dict(method_id=g.iloc[0].method_id,list_id=lid,method_name=g.iloc[0].method_name,list_name=g.iloc[0].list_name,n=len(f),top30_return=t.ret_0713.mean(),top30_next_open_return=t.ret_next_open.mean(),top30_excess_universe=t.ret_0713.mean()-ret.ret_0713.mean(),top30_category_excess=t.category_excess.mean(),top30_median=t.ret_0713.median(),top30_positive=int((t.ret_0713>0).sum()),top30_actual_winner30=int(len(set(t.ticker)&winner30)),top30_bottom30_spread=t.ret_0713.mean()-b.ret_0713.mean(),rank_ic=-f['rank'].rank().corr(f.ret_0713.rank()),top30_tickers=','.join(t.ticker)))
pd.DataFrame(metrics).to_csv(OUT/'data/sorting_top30_metrics.csv',index=False,encoding='utf-8-sig')
inventory=[];sections=[]
for method,r in reg.drop_duplicates('method_id').set_index('method_id').iterrows():
    p=RR/r.plan_path;txt=p.read_text(encoding='utf-8');lines=txt.splitlines()
    iterroot=RR/r.method_path/'迭代版本'
    versions=[v.name for v in iterroot.iterdir() if v.is_dir() and re.match(r'R\d+',v.name)]
    versions.sort(key=lambda s:(int(re.match(r'R(\d+)',s)[1]),s))
    inventory.append(dict(method_id=method,method_name=r.method_name,run_id=r.run_id,run_date=r.run_date,lifecycle=r.lifecycle,status=r.status,site_publish=pol.loc[method,'site_publish'],consensus_eligible=pol.loc[method,'consensus_eligible'],plan_path=str(p),plan_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),result_path=str(RR/r.result_path),latest_iteration=versions[-1],registry_is_latest=(p.parent.name==versions[-1]),reads_retired_evaluation=(method!='07' and '公司评估' in txt),reads_merged_decision=('公司情景投资决策' in txt or '经营情景市场状态投资决策' in txt),line_count=len(lines),input_evidence=' | '.join(f'{i}: {l}' for i,l in enumerate(lines,1) if re.search('只能读取|公司评估|公司情景投资决策|公司调研|行业调研',l) and i<40)))
    for i,l in enumerate(lines,1):
        if l.startswith('#') or re.search('权重|公式|×|%|个月|季度|不得|只允许|只能|取50|不低于|≥|≤',l):
            sections.append(dict(method_id=method,source_path=str(p),source_line=i,text=l))
pd.DataFrame(inventory).to_csv(OUT/'data/sorting_current_inventory.csv',index=False,encoding='utf-8-sig')
pd.DataFrame(sections).to_csv(OUT/'data/sorting_plan_clauses.csv',index=False,encoding='utf-8-sig')

queue=[]
for fname in ['queue.jsonl','queue.done.jsonl']:
    path=ROOT/'tools'/fname
    for i,l in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
        if not l.strip():continue
        r=json.loads(l)
        if r.get('domain')!='file-run':continue
        q={k:r.get(k,'') for k in ['subject','runId','status','sourceDate','promptFile','expectedOutputFile','finishedAt']}
        q['queue_path']=str(path);q['queue_line']=i
        raw=q['promptFile'].replace('\\','/');pp=Path(raw) if re.match('[A-Za-z]:',raw) else ROOT/raw
        q['prompt_exists']=pp.exists();q['resolved_prompt']=str(pp.resolve()) if pp.exists() else ''
        queue.append(q)
pd.DataFrame(queue).to_csv(OUT/'data/file_run_live_queue_inventory.csv',index=False,encoding='utf-8-sig')
# Most recent historical queue holding a registry current ranking; no global history claim.
backup=ROOT/'tools/research-runner/queue-backups/queue.done.before-clear_20260717_013356.jsonl'
arch=[]
if backup.exists():
    for i,l in enumerate(backup.read_text(encoding='utf-8-sig').splitlines(),1):
        if not l.strip():continue
        r=json.loads(l)
        if r.get('domain')=='file-run':
            arch.append(dict(subject=r.get('subject',''),status=r.get('status',''),promptFile=r.get('promptFile',''),expectedOutputFile=r.get('expectedOutputFile',''),sourceDate=r.get('sourceDate',''),queue_path=str(backup),queue_line=i))
pd.DataFrame(arch).to_csv(OUT/'data/file_run_july_archive_inventory.csv',index=False,encoding='utf-8-sig')
print('methods',len(inventory),'latest matches',sum(x['registry_is_latest'] for x in inventory),'retired references',sum(x['reads_retired_evaluation'] for x in inventory),'merged refs',sum(x['reads_merged_decision'] for x in inventory),'live/done file-run',len(queue),'historical file-run',len(arch))
print(pd.DataFrame(metrics)[['list_id','top30_return','top30_next_open_return','rank_ic','top30_actual_winner30']].to_string(index=False))
