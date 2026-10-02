from pathlib import Path
import csv,json,hashlib,subprocess,datetime,shutil,sys
ROOT=Path('D:/drive/Investment');OUT=Path(__file__).resolve().parent
CLI=ROOT/'tools/research-runner/queue-tools.mjs'
receipt=json.loads((OUT/'16份方案入队回执.json').read_text(encoding='utf-8'))
wanted=[x for x in receipt['items'] if x['variant']=='ABCDE'];assert len(wanted)==13
with (ROOT/'分析报告/公司排序/00_待运行研究方案注册表.csv').open(encoding='utf-8-sig',newline='') as f:registry={r['method_id']:r for r in csv.DictReader(f)}
queue=ROOT/'tools/queue.jsonl';done=ROOT/'tools/queue.done.jsonl'
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def matches(x):return [r for r in read(queue)+read(done) if r.get('domain')=='file-run' and (r.get('promptFile')==x['prompt'] or r.get('expectedOutputFile')==x['result'])]
planned=[]
for x in wanted:
 r=registry[x['method']];control=r['execution_mode']=='paired_experiment'
 prompt=r['control_prompt_file'] if control else r['prompt_file'];result=r['control_expected_output_file'] if control else r['expected_output_file'];digest=r['control_sha256'] if control else r['sha256']
 assert prompt==x['prompt'] and result==x['result'],'Registration changed from original request'
 assert hashlib.sha256((ROOT/prompt).read_bytes()).hexdigest()==digest,prompt
 found=matches(x);assert len(found)<=1,found
 if found:assert found[0]['promptFile']==prompt and found[0]['expectedOutputFile']==result
 else:assert not (ROOT/result).exists(),'Result exists without queue binding: '+result
 args=['node',str(CLI),'add-file-run','--run-id=sorting-'+x['method']+'-ABCDE-2026-09-09','--prompt-file='+prompt,'--expected-output-dir='+Path(result).parent.as_posix(),'--expected-output-file='+result,'--display-name='+x['name'],'--source-date=2026-09-09','--status=pending','--reasoning='+x['reasoning']]
 if not found:subprocess.run(args+['--dry-run'],cwd=ROOT,capture_output=True,encoding='utf-8',check=True)
 planned.append({'method':x['method'],'prompt':prompt,'result':result,'existing':found[0]['id'] if found else None,'args':args})
summary={'tasks':len(planned),'new':sum(not x['existing'] for x in planned),'already_present':sum(bool(x['existing']) for x in planned),'company_decision_unfinished':sum(r.get('domain')=='company-investment-decision' and r.get('status') in ['pending','running','retry_pending'] for r in read(queue))}
if '--apply' not in sys.argv:
 print(json.dumps(summary));sys.exit(0)
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup=ROOT/'tools/research-runner/queue-backups'/('sorting-remaining13-'+stamp)
backup.mkdir(parents=True,exist_ok=False);shutil.copy2(queue,backup/'queue.jsonl');shutil.copy2(done,backup/'queue.done.jsonl')
for x in planned:
 if not x['existing']:subprocess.run(x['args'],cwd=ROOT,capture_output=True,encoding='utf-8',check=True)
 found=matches(x);assert len(found)==1
 x['queue_id']=found[0]['id'];x['status']=found[0]['status'];x['reasoning']=found[0]['reasoningEffort'];del x['args']
assert len({x['queue_id'] for x in planned})==13
validation=subprocess.run(['node',str(CLI),'validate'],cwd=ROOT,capture_output=True,encoding='utf-8',check=True)
report={**summary,'backup':backup.as_posix(),'validation':validation.stdout.strip(),'items':planned}
(OUT/'其余13份入队回执_2026-09-09.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({**summary,'statuses':{s:sum(x['status']==s for x in planned) for s in set(x['status'] for x in planned)},'validation':validation.stdout.strip()},ensure_ascii=False))
