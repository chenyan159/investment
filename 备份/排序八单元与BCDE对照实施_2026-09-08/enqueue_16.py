from pathlib import Path
import csv,json,subprocess,hashlib,shutil,datetime
ROOT=Path('D:/drive/Investment'); OUT=Path(__file__).resolve().parent
CLI=ROOT/'tools/research-runner/queue-tools.mjs'
rows=list(csv.DictReader((ROOT/'分析报告/公司排序/00_待运行研究方案注册表.csv').open(encoding='utf-8-sig',newline='')))
items=[]
for mode in ['routine','paired_experiment','experiment']:
 for r in rows:
  if r['execution_mode']!=mode:continue
  variants=[('BCDE',r['prompt_file'],r['expected_output_file'],r['sha256'])] if mode=='paired_experiment' else [('ABCDE',r['prompt_file'],r['expected_output_file'],r['sha256'])]
  if mode=='paired_experiment':variants.insert(0,('ABCDE',r['control_prompt_file'],r['control_expected_output_file'],r['control_sha256']))
  for variant,prompt,result,digest in variants:
   assert hashlib.sha256((ROOT/prompt).read_bytes()).hexdigest()==digest,prompt
   assert not (ROOT/result).exists(),result
   items.append({'method':r['method_id'],'variant':variant,'mode':mode,'prompt':prompt,'result':result,'name':r['method_name']+' '+variant})
assert len(items)==16 and len({x['result'] for x in items})==16
queue=ROOT/'tools/queue.jsonl';done=ROOT/'tools/queue.done.jsonl'
def read(p):return [json.loads(l) for l in p.read_text(encoding='utf-8-sig').splitlines() if l.strip()]
def matches(x):return [r for r in read(queue)+read(done) if r.get('domain')=='file-run' and (r.get('promptFile')==x['prompt'] or r.get('expectedOutputFile')==x['result'])]
for x in items:
 found=matches(x);assert len(found)<=1,found
 if found:assert found[0]['promptFile']==x['prompt'] and found[0]['expectedOutputFile']==x['result']
 x['existing_id']=found[0]['id'] if found else None
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
backup=ROOT/'tools/research-runner/queue-backups'/('sorting-16-'+stamp);backup.mkdir(parents=True,exist_ok=False)
shutil.copy2(queue,backup/'queue.jsonl');shutil.copy2(done,backup/'queue.done.jsonl')
for x in items:
 x['args']=['node',str(CLI),'add-file-run','--run-id=sorting-'+x['method']+'-'+x['variant']+'-2026-09-08','--prompt-file='+x['prompt'],'--expected-output-dir='+str(Path(x['result']).parent).replace('\\','/'),'--expected-output-file='+x['result'],'--display-name='+x['name'],'--status=pending']
 if not x['existing_id']:
  check=subprocess.run(x['args']+['--dry-run'],cwd=ROOT,capture_output=True,encoding='utf-8',check=True)
  proposed=json.loads(check.stdout);x['reasoning']=proposed['reasoningEffort']
for x in items:
 if not x['existing_id']:
  subprocess.run(x['args'],cwd=ROOT,capture_output=True,encoding='utf-8',check=True)
 found=matches(x);assert len(found)==1
 x['queue_id']=found[0]['id'];x['status']=found[0]['status'];x['reasoning']=found[0]['reasoningEffort'];del x['args']
assert len({x['queue_id'] for x in items})==16
validation=subprocess.run(['node',str(CLI),'validate'],cwd=ROOT,capture_output=True,encoding='utf-8',check=True)
report={'added':sum(not x['existing_id'] for x in items),'already_present':sum(bool(x['existing_id']) for x in items),'verified':len(items),'backup':backup.as_posix(),'validation':validation.stdout.strip(),'items':items}
(OUT/'16份方案入队回执.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='items'},ensure_ascii=False))
print(json.dumps({'statuses':{s:sum(x['status']==s for x in items) for s in set(x['status'] for x in items)},'reasoning':sorted(set(x['reasoning'] for x in items))},ensure_ascii=False))
