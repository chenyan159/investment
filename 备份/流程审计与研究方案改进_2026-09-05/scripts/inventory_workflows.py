from pathlib import Path
import json, csv, hashlib, re, collections, datetime, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('D:/drive/Investment')
OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05/data'
def txt(p): return p.read_text(encoding='utf-8-sig',errors='replace')
def rel(p): return p.relative_to(ROOT).as_posix()
def save(name,rows):
    (OUT/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    if isinstance(rows,list) and rows:
        keys=list(dict.fromkeys(k for r in rows for k in r))
        with (OUT/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
queues=[ROOT/'tools/queue.jsonl',ROOT/'tools/queue.done.jsonl']
tasks=[]; snapshots=[]
for p in queues:
    raw=p.read_bytes(); lines=raw.decode('utf-8-sig').splitlines()
    snapshots.append({'path':rel(p),'sha256':hashlib.sha256(raw).hexdigest(),'lines':len(lines),'read_at':datetime.datetime.now().astimezone().isoformat()})
    for line in lines:
        if not line.strip(): continue
        r=json.loads(line)
        tasks.append({k:r.get(k,'') for k in ['id','domain','subject','sourceDate','status','promptFile','expectedOutputFile','outputFile','startedAt','finishedAt']}|{'queue':rel(p)})
save('queue_tasks_snapshot',tasks);save('queue_snapshot_meta',snapshots)
groups=collections.defaultdict(list)
for r in tasks:
    if r['domain']=='file-run':groups[r['promptFile']].append(r)
historical={r['id']:r for r in tasks}
for qp in sorted((ROOT/'tools/research-runner/queue-backups').glob('*.jsonl')):
    for line in txt(qp).splitlines():
        if not line.strip():continue
        r=json.loads(line)
        if r.get('domain')=='file-run':historical.setdefault(r['id'],{k:r.get(k,'') for k in ['id','domain','subject','sourceDate','status','promptFile','expectedOutputFile','outputFile']}|{'queue':rel(qp)})
hist_tasks=[r for r in historical.values() if r['domain']=='file-run']
save('file_run_historical_tasks',hist_tasks)
for r in hist_tasks:
    if r['promptFile'] and not any(x['id']==r['id'] for x in groups[r['promptFile']]):groups[r['promptFile']].append(r)
prompts=[]
for pf,rs in sorted(groups.items()):
    p=ROOT/pf;t=txt(p) if p.is_file() else ''
    prompts.append({'promptFile':pf,'exists':p.is_file(),'runs':len(rs),'dates':','.join(sorted(set(r['sourceDate'] for r in rs))),'statuses':dict(collections.Counter(r['status'] for r in rs)),'subjects':[r['subject'] for r in rs],'outputFiles':sorted(set(r['expectedOutputFile'] or r['outputFile'] for r in rs)),'chars':len(t),'headings':re.findall(r'^#{1,4}\s+(.+)',t,re.M)[:25],'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ''})
save('file_run_prompt_inventory',prompts)
files=[]
exclude={'备份','_work','tmp','node_modules','.git','历史管理资料','_重复运行','公司评估_淘汰'}
for base in ['基本面','分析报告','金融资料','tools/research-runner/domains','tools/research-runner/prompts']:
    for folder,dirs,names in os.walk(ROOT/base,followlinks=False):
        dirs[:]=[d for d in dirs if d not in exclude and not os.path.isjunction(Path(folder)/d) and not (Path(folder)/d).is_symlink()]
        for name in names:
            p=Path(folder)/name
            if p.suffix=='.mjs' or (p.suffix=='.md' and (any(x in p.name for x in ['方案','方法']) or p.name in ['AGENTS.md','README.md'])):
                t=txt(p);files.append({'path':rel(p),'chars':len(t),'lines':len(t.splitlines()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'headings':re.findall(r'^#{1,4}\s+(.+)',t,re.M)[:30]})
save('source_plan_code_inventory',files)
summary={'queue_domains':dict(collections.Counter(r['domain'] for r in tasks)),'queue_statuses':dict(collections.Counter(r['status'] for r in tasks)),'file_run_current_distinct_prompts':len(set(r['promptFile'] for r in tasks if r['domain']=='file-run')),'file_run_current_and_backup_distinct_prompts':len(prompts),'file_run_historical_unique_tasks':len(hist_tasks),'discovered_plan_code_files':len(files)}
save('inventory_summary',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
for p in prompts: print(p['runs'],p['promptFile'],str(p['outputFiles'])[:180])
