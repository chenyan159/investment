import json, re, csv, statistics
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

ROOT = Path('D:/drive/Investment')
OUT = Path(__file__).parent
def rows(p):
    return [json.loads(l) for l in p.read_text(encoding='utf-8-sig').splitlines() if l.strip()]
current = rows(ROOT/'tools/queue.done.jsonl')
historical = rows(ROOT/'tools/research-runner/queue-backups/queue.done.before_company_investment_decision_all_v4_20260715_012607.jsonl')
new = [r for r in current if r.get('runId','').endswith('_20260905')]
oldconf = [r for r in current if r.get('domain')=='file-run' and '2026-08-18' in r.get('startedAt','') and 'conference' in r['id']]
oldbg = [r for r in historical if any(x in r['id'] for x in ['reasoning-test-ai-chain-t02-', 'reasoning-test-datacenter-t05-', 'background-global-ai-token-framework-20260710-', 'background-head-ai-chips-20260710-', 'background-ai-chain-bottlenecks-20260710-'])]
result=[]
rate_details=[]
for cohort, items in [('astra_new',new),('sol_conference',oldconf),('sol_background',oldbg)]:
 for r in items:
    formal=r['tokenUsage']['attempts'][-1]['formal']
    d={k:formal.get(k) for k in ['model','reasoningEffort','threadId','inputTokens','cachedInputTokens','uncachedInputTokens','outputTokens','reasoningOutputTokens','totalTokens']}
    if d['uncachedInputTokens'] is None: d['uncachedInputTokens']=d['inputTokens']-d['cachedInputTokens']
    d.update(cohort=cohort, id=r['id'], name=r.get('displayName',r.get('subject')), outputFile=r['outputFile'], start=r['startedAt'], end=r['finishedAt'], attempts=r['attempts'])
    d['minutes']=(datetime.fromisoformat(d['end'])-datetime.fromisoformat(d['start'])).total_seconds()/60
    p=ROOT/r['outputFile']
    if p.exists():
      s=p.read_text(encoding='utf-8-sig'); urls=set(re.findall(r'https?://[^\s<>\]）)"`]+',s))
      d.update(bytes=p.stat().st_size, chars=len(s), lines=len(s.splitlines()), uniqueUrls=len(urls), uniqueHosts=len(set(urlparse(u).netloc for u in urls)))
    date=d['start'][:10].split('-'); folder=Path('C:/Users/cheny/.codex/sessions').joinpath(*date)
    session=next(folder.glob('*'+d['threadId']+'.jsonl'),None)
    if session:
      rates=[]; gaps=[]; prev=None; first_ts=None; last_ts=None; last_usage=None; commands=[]
      for l in session.open(encoding='utf-8'):
       try: e=json.loads(l)
       except Exception: continue
       ts=e.get('timestamp'); payload=e.get('payload',{})
       if ts:
        dt=datetime.fromisoformat(ts.replace('Z','+00:00'))
        if prev: gaps.append(((dt-prev).total_seconds(),ts,e.get('type'),payload.get('type'),payload.get('name')))
        prev=dt
       if e.get('type')=='event_msg' and payload.get('type')=='token_count':
        if first_ts is None: first_ts=ts
        last_ts=ts
        info=payload.get('info') or {};last_usage=info.get('total_token_usage') or last_usage
        rl=payload.get('rate_limits') or {}
        for win in ['primary','secondary']:
         pr=rl.get(win) or {}
         if rl.get('limit_id')!='codex' or pr.get('window_minutes')!=10080: continue
         val=(pr.get('used_percent'),pr.get('resets_at'),pr.get('window_minutes'))
         if val[0] is not None and (not rates or rates[-1]['value']!=val): rates.append({'time':ts,'value':val})
       if e.get('type')=='response_item' and payload.get('type')=='function_call':
        commands.append({'time':ts,'name':payload.get('name'),'args':payload.get('arguments','')})
      d['formalSessionFirstUsage']=first_ts;d['formalSessionLastUsage']=last_ts
      rate_details.append({'id':r['id'],'threadId':d['threadId'],'session':str(session),'rates':rates,'largestGaps':sorted(gaps,reverse=True)[:5],'lastSessionUsage':last_usage})
    result.append(d)
summary={}
for c in ['astra_new','astra_conference','astra_background','sol_conference','sol_background','sol_all']:
 group=[d for d in result if d['cohort']==c or (c=='sol_all' and d['cohort'].startswith('sol_')) or (c=='astra_conference' and d['cohort']=='astra_new' and 'conference' in d['id']) or (c=='astra_background' and d['cohort']=='astra_new' and 'background' in d['id'])]
 summary[c]={'n':len(group), **{k:sum(d[k] for d in group) for k in ['inputTokens','cachedInputTokens','uncachedInputTokens','outputTokens','reasoningOutputTokens','totalTokens','minutes']}, 'meanMinutes':statistics.mean(d['minutes'] for d in group),'medianMinutes':statistics.median(d['minutes'] for d in group)}
 summary[c]['cacheRatio']=summary[c]['cachedInputTokens']/summary[c]['inputTokens']
(OUT/'metrics.json').write_text(json.dumps({'tasks':result,'summary':summary,'rateDetails':rate_details},ensure_ascii=False,indent=2),encoding='utf-8')
keys=list(dict.fromkeys(k for r in result for k in r))
with (OUT/'逐任务资源明细.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(result)
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('RATES', json.dumps([{'id':r['id'],'first':r['rates'][:1],'last':r['rates'][-1:]} for r in rate_details],ensure_ascii=False,indent=2))
