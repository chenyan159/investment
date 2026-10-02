from pathlib import Path
import json,hashlib,re
ROOT=Path('D:/drive/Investment');OUT=Path(__file__).resolve().parent
R=ROOT/'备份/排序八单元与BCDE对照实施_2026-09-08'
a=json.loads((R/'其余13份入队回执_2026-09-09.json').read_text(encoding='utf-8'))['items']
b=[x for x in json.loads((R/'16份方案入队回执.json').read_text(encoding='utf-8'))['items'] if x['variant']=='BCDE']
queue=[]
for p in [ROOT/'tools/queue.jsonl',ROOT/'tools/queue.done.jsonl']:
 queue.extend(json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip())
data={}
for x in a+b:
 key=x['method']+('-B' if x.get('variant')=='BCDE' else ('-A' if x['method'].startswith('E') else ''))
 q=next((y for y in queue if y['id']==x['queue_id']),{})
 p=ROOT/x['result'];t=p.read_text(encoding='utf-8') if p.exists() else '';lines=t.splitlines()
 data[key]={'id':key,'method':x['method'],'input':'BCDE' if key.endswith('-B') else 'ABCDE','queue_id':x['queue_id'],'status':q.get('status'),'start':q.get('startedAt'),'finish':q.get('finishedAt'),'attempts':q.get('attempts'),'report':p.as_posix(),'prompt':(ROOT/x['prompt']).as_posix(),'bytes':p.stat().st_size if p.exists() else 0,'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else '', 'lines':len(lines),'headings':[{'line':i+1,'text':l} for i,l in enumerate(lines) if l.startswith('## ')]}
(OUT/'16份结果清单.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for k,v in data.items(): print(json.dumps({key:v[key] for key in ['id','status','start','finish','attempts','bytes','lines']},ensure_ascii=False))
