import json,re,statistics,hashlib,csv
from pathlib import Path
from datetime import datetime
R=Path('D:/drive/Investment'); OUT=Path(__file__).parent
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
allq=jl(R/'tools/queue.done.jsonl'); q=[x for x in allq if x.get('createdAt','').startswith('2026-09-06T00:11:')]
logs=jl(R/'tools/research-runner/logs/current.jsonl')
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
stats=[]; pairs=[]; prompts=[]
names=['HBM与高带宽内存','云厂自研AI ASIC','AI云算力外包和NeoCloud与AI数据中心运营商','商用AI加速芯片','数据中心电力接入与高压变电','数据中心直液冷系统']
for x in q:
 p=R/x['outputFile']; s=p.read_text(encoding='utf-8-sig'); claims=[l for l in logs if l.get('id')==x['id'] and l['event'].startswith('Claimed ')]
 vals=[l for l in logs if l.get('id')==x['id'] and l['event'].startswith('Local output validation passed')]
 attempts=x.get('tokenUsage',{}).get('attempts',[])
 row=dict(subject=x['subject'],domain=x['domain'],status=x['status'],attempts=x['attempts'],claims=len(claims),start=x['startedAt'],finish=x['finishedAt'],minutes=(dt(x['finishedAt'])-dt(x['startedAt'])).total_seconds()/60,wall_minutes=(dt(vals[-1]['timestamp'])-dt(claims[0]['timestamp'])).total_seconds()/60,output=x['outputFile'],bytes=p.stat().st_size,chars=len(s),lines=len(s.splitlines()),h1=len(re.findall(r'^# ',s,re.M)),replacement=s.count('\ufffd'),nul=s.count('\0'),validated=len(vals),thread=attempts[-1]['formal']['threadId'],model=attempts[-1]['formal']['model'],reasoning=attempts[-1]['formal']['reasoningEffort'])
 stats.append(row)
 plan=(R/('基本面/行业调研/研究方法/行业调研方案.md' if x['domain']=='industry' else '基本面/公司调研/研究方法/调研方案.md')).read_text(encoding='utf-8-sig').replace('【行业名称】',x['subject']).replace('【公司股票代号】',x['subject']).strip()
 for c in claims:
  pp=Path(c['promptDebug']); ps=pp.read_text(encoding='utf-8-sig'); prompts.append(dict(subject=x['subject'],path=str(pp),chars=len(ps),logged_chars=c['promptCharacters'],full_current_plan=plan in ps,bytes=pp.stat().st_size,placeholder=bool(re.search('【行业名称】|【公司股票代号】',ps))))
 if x['domain']=='company' or x['subject'] in names:
  prep=[l for l in logs if l['event']==f"Prepared {x['domain']}/{x['subject']} formal run." and l.get('files')]
  old=next((f['to'] for pr in prep for f in pr['files'] if (R/f['to']).exists()),None)
  previous=[a for a in allq if a['domain']==x['domain'] and a['subject']==x['subject'] and a['id']!=x['id'] and a.get('finishedAt','')<x['startedAt']]
  prev=max(previous,key=lambda a:a.get('finishedAt','')) if previous else None
  pair=dict(row,old=old,oldRun=prev,newRun=x);pairs.append(pair)
  if old:
   os=(R/old).read_text(encoding='utf-8-sig');pair.update(oldchars=len(os),oldbytes=(R/old).stat().st_size)
  for v,path in [('new',p),('old',R/old if old else None)]:
   if path:
    text=path.read_text(encoding='utf-8-sig'); safe=re.sub(r'[/\\ ]','_',x['subject']);(OUT/f'{safe}_{v}_提要.txt').write_text('\n'.join(f'{i}: {l}' for i,l in enumerate(text.splitlines(),1) if i<=65 or l.startswith('#')),encoding='utf-8')
for fn,obj in [('运行清单.json',stats),('对照清单.json',pairs),('输入提示检查.json',prompts)]: (OUT/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'逐项耗时.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=stats[0].keys());w.writeheader();w.writerows(stats)
for domain in ['industry','company']:
 a=[r for r in stats if r['domain']==domain];print(domain,json.dumps(dict(count=len(a),min_minutes=min(r['wall_minutes'] for r in a),median_minutes=statistics.median(r['wall_minutes'] for r in a),mean_minutes=statistics.mean(r['wall_minutes'] for r in a),max_minutes=max(r['wall_minutes'] for r in a),sum_minutes=sum(r['wall_minutes'] for r in a),min_bytes=min(r['bytes'] for r in a),max_bytes=max(r['bytes'] for r in a),median_bytes=statistics.median(r['bytes'] for r in a)),ensure_ascii=False))
print('retries',[(r['subject'],r['claims'],r['wall_minutes']) for r in stats if r['claims']>1]);print('prompt checks',len(prompts),sum(p['full_current_plan'] for p in prompts));print('output problems',[s for s in stats if s['h1']!=1 or s['replacement'] or s['nul'] or not s['validated']]);print('pairs',[(p['subject'],p.get('oldchars'),p['chars'],p['oldRun']['finishedAt'] if p['oldRun'] else None) for p in pairs])
