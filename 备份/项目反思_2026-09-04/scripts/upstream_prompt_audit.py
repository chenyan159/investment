from pathlib import Path
import re,csv,json,collections
root=Path(r'D:\drive\Investment'); out=root/'备份/项目反思_2026-09-04'
rows=[]
for p in (root/'tools/research-runner/prompt-debug').glob('2026-07-*.md'):
    m=re.match(r'(2026-07-\d\d)T.*?_(industry|company)_([^/]+)_prompt.md$',p.name)
    if not m or m[1]>'2026-07-12': continue
    text=p.read_text(encoding='utf-8-sig')
    phrases=['对于找不到的直接数据可以做大胆乐观的假设','按基准，乐观，极度乐观三种口径','非AI方面低增速不重要的产品和业务可以跳过']
    row={'domain':m[2],'subject':m[3],'prompt_date':m[1],'path':str(p)}
    for n,s in enumerate(phrases):row['instruction_'+str(n)]=int(s in text)
    rows.append(row)
latest={}
for r in rows:
    key=(r['domain'],r['subject'])
    if key not in latest or r['path']>latest[key]['path']:latest[key]=r
rr=list(latest.values())
with (out/'data/upstream_prompt_contract_audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rr[0].keys());w.writeheader();w.writerows(rr)
print(json.dumps({'all_prompt_files':len(rows),'latest_per_subject':dict(collections.Counter(r['domain'] for r in rr)),'counts':{d:{'n':sum(r['domain']==d for r in rr),**{f'instruction_{i}':sum(r[f'instruction_{i}'] for r in rr if r['domain']==d) for i in range(3)}} for d in ['company','industry']}},ensure_ascii=False))
