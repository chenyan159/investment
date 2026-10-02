import csv, json, os, re, collections, ntpath
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(r'D:\investment'); OUT=Path(__file__).parent
INV=json.loads((OUT/'inventory-before.json').read_text(encoding='utf-8-sig'))
LINKS=INV['Links']; RANK=ROOT/'分析报告/公司排序'
def norm(s): return re.sub(r'/+', '/',unquote(str(s)).replace('\\','/'))
def matched(s):
    s=norm(s); found=[]
    for i,l in enumerate(LINKS):
        alias=norm(os.path.relpath(l['Path'],ROOT))
        if i<2:
            if alias in s or (i==1 and '日度资料' in s): found.append(i)
        else:
            leaf=Path(l['Path']).name
            # Include old relative-path names as candidates; these may also be historical identifiers.
            if leaf in s: found.append(i)
    return found
def category(p):
    parts=p.split('/')
    if any(x in parts for x in ['备份','queue-backups','prompt-debug','logs','历史管理资料','评估备份']) or p.endswith(('.log','queue.done.jsonl')): return '历史备份日志'
    if any(x in parts for x in ['tmp','_work','__pycache__']) or any(x.startswith('.站点数据-') for x in parts): return '临时产物'
    if p.startswith(('tools/site/docs/','tools/site/dist/','tools/site/public/')) or '/站点数据/' in p: return '派生展示数据'
    if Path(p).suffix in ['.py','.mjs','.js','.ts','.ps1','.cmd','.bat','.sh','.jsx','.tsx']: return '脚本待复核'
    return '正文或管理文件'

refs={}; total=0
with open(Path(os.environ['TEMP'])/'junction-hits.jsonl',encoding='utf-8-sig') as f:
    for line in f:
        o=json.loads(line)
        if o['type']!='match': continue
        d=o['data']; p=norm(os.path.relpath(d['path']['text'],ROOT))
        if p.startswith(norm(os.path.relpath(OUT,ROOT))+'/'): continue
        text=d['lines']['text']; ids=matched(text)
        for i in ids:
            key=(i,p); v=refs.setdefault(key,{'count':0,'samples':[],'category':category(p)})
            v['count']+=1
            if len(v['samples'])<2:
                needle='日度资料' if i==1 else ('基本面' if i==0 else Path(LINKS[i]['Path']).name)
                start=max(0,text.find(needle)-80)
                v['samples'].append({'line':d['line_number'],'text':text[start:start+400].strip()})
with (OUT/'junction-reference-files.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['junction','file','category','matched_lines','samples'])
    for (i,p),v in sorted(refs.items()): w.writerow([os.path.relpath(LINKS[i]['Path'],ROOT),p,v['category'],v['count'],json.dumps(v['samples'],ensure_ascii=False)])

checks=[]; active_files=set(); path_checks=[]
def check_path(source,field,value,base):
    if not value or not isinstance(value,str): return
    p=Path(ntpath.normpath(ntpath.join(str(base),value)))
    aliases=[]
    for l in LINKS:
        if str(p).lower()==l['Path'].lower() or str(p).lower().startswith(l['Path'].lower()+'\\'): aliases.append(l['Path'])
    path_checks.append({'source':str(source.relative_to(ROOT)),'field':field,'value':value,'exists':p.exists(),'junctions':aliases})
    if p.is_file() and p.suffix=='.md': active_files.add(p)
def walk_values(obj,field=''):
    if isinstance(obj,dict):
        for k,v in obj.items(): yield from walk_values(v,field+'.'+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): yield from walk_values(v,field+f'[{i}]')
    elif isinstance(obj,str): yield field,obj

for filename,base in [('00_待运行研究方案注册表.csv',ROOT),('00_运行与榜单注册表.csv',RANK),('00_方案状态总表.csv',RANK),('00_站点发布策略.csv',RANK)]:
    p=RANK/filename; rows=list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
    hits=[]
    for n,row in enumerate(rows,2):
        for k,v in row.items():
            if matched(v or ''): hits.append({'line':n,'field':k,'value':v})
            if k and (k.endswith(('_path','_file','_dir')) or k in ['prompt_file','control_prompt_file']): check_path(p,f'{n}:{k}',v,base)
    checks.append({'file':str(p.relative_to(ROOT)),'rows':len(rows),'alias_mentions':hits})

p=RANK/'00_当前评估.json'; obj=json.loads(p.read_text(encoding='utf-8-sig'))
for k,v in obj.items():
    if k.endswith('_path'):check_path(p,k,v,RANK)
p=ROOT/'tools/research-runner/research-plans.json'; plans=json.loads(p.read_text(encoding='utf-8-sig'))
for plan in plans:
    check_path(p,plan['id']+'.directory',plan['directory'],ROOT)
    active_files.update((ROOT/plan['directory']).glob('研究方案_*.md'))
checks.append({'file':str(p.relative_to(ROOT)),'rows':len(plans),'alias_mentions':[{'field':k,'value':v} for k,v in walk_values(plans) if matched(v)]})
p=ROOT/'tools/queue.jsonl'; states=collections.Counter(); qhits=[]; n=0
for n,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
    if not line.strip():continue
    obj=json.loads(line);states[obj.get('status','unknown')]+=1
    for k,v in walk_values(obj):
        if matched(v): qhits.append({'line':n,'field':k,'value':v[:400]})
        if k.split('.')[-1] in ['promptFile','planEntryFile','planSnapshotFile','actualPromptFile','outputFile','outputDir']:check_path(p,f'{n}:{k}',v,ROOT)
checks.append({'file':'tools/queue.jsonl','rows':n,'states':states,'alias_mentions':qhits})
# Other current independent-plan families.
active_files.update((ROOT/'基本面/特征量化/研究方案').glob('*.md'))
active_files.update((ROOT/'技术面/研究方案').glob('*.md'))
plan_hits=[]
for p in sorted(active_files):
    for n,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
        if matched(line):plan_hits.append({'file':str(p.relative_to(ROOT)),'line':n,'text':line[:500]})
summary={'inventory_links':len(LINKS),'checks':checks,'path_checks':path_checks,'current_and_bound_md_files':len(active_files),'plan_alias_mentions':plan_hits,
         'link_references':[{'path':l['Path'],'target':l['Target'][0],'files':sum(i==idx for i,p in refs),'categories':dict(collections.Counter(v['category'] for (i,p),v in refs.items() if i==idx))} for idx,l in enumerate(LINKS)]}
(OUT/'dependency-checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks':checks,'path_checks':len(path_checks),'junction_path_checks':[x for x in path_checks if x['junctions']],'missing_paths':[x for x in path_checks if not x['exists']][:10],'current_and_bound_md_files':len(active_files),'plan_alias_mentions':plan_hits[:15]},ensure_ascii=False,indent=2))
for x in summary['link_references']:print(json.dumps(x,ensure_ascii=False))
