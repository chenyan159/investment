import json, os, collections
from pathlib import Path
root = Path(r'D:\investment')
out = Path(__file__).parent
groups = collections.Counter()
files = {}
with open(Path(os.environ['TEMP'])/'junction-hits.jsonl', encoding='utf-8-sig') as f:
    for line in f:
        obj=json.loads(line)
        if obj['type'] != 'match': continue
        d=obj['data']; p=d['path']['text']; rel=os.path.relpath(p,root).replace('\\','/')
        if rel.startswith('备份/Junction依赖审计与图标清理_2026-09-19/'): continue
        parts=rel.split('/')
        if any(x in parts for x in ['备份','queue-backups','prompt-debug','logs','历史管理资料','评估备份']): category='history'
        elif any(x in parts for x in ['tmp','_work','__pycache__']): category='temporary'
        elif rel.startswith(('tools/site/docs/','tools/site/dist/','tools/site/public/')) or '/站点数据/' in rel: category='generated'
        elif Path(p).suffix in ['.py','.mjs','.js','.ts','.ps1','.cmd','.bat','.sh','.jsx','.tsx']: category='code-review'
        else: category='document-or-config'
        groups[category]+=1
        entry=files.setdefault(rel,dict(category=category,count=0,samples=[]))
        entry['count']+=1
        if len(entry['samples'])<5: entry['samples'].append({'line':d['line_number'],'text':d['lines']['text'][:700]})
(out/'reference-file-summary.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'matching_lines':groups,'matching_files':collections.Counter(x['category'] for x in files.values())},ensure_ascii=False))
for p,v in files.items():
    if v['category']=='code-review': print(p, json.dumps(v,ensure_ascii=False))
