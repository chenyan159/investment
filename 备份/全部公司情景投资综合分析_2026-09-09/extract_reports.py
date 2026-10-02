from pathlib import Path
import re, json, hashlib, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'D:\drive\Investment')
SRC = ROOT / '分析报告/公司情景投资决策/结果'
OUT = Path(__file__).parent
WORK = OUT / 'tmp'
WORK.mkdir(parents=True, exist_ok=True)
SCENARIOS = ['悲观','基准','乐观','突破']
LABELS = ['强烈不建议投资','强烈建议投资','谨慎建议投资','不建议投资','建议投资','中性','不可判定','不适用']
def clean(s):
    return re.sub(r'[*`]', '', s).replace('<br>', '；').strip()
def splitrow(s):
    return [clean(c.replace('\\|','｜')) for c in re.split(r'(?<!\\)\|',s.strip().strip('|'))]
def get_tables(lines):
    tables=[]; i=0
    while i<len(lines):
        if lines[i].lstrip().startswith('|'):
            start=i; rows=[]
            while i<len(lines) and lines[i].lstrip().startswith('|'):
                r=splitrow(lines[i])
                if not all(re.fullmatch(r'[:\-\s]+',x) for x in r): rows.append(r)
                i+=1
            if rows: tables.append({'line':start+1,'header':rows[0],'rows':rows[1:]})
        else: i+=1
    return tables
def scenario(s):
    return next((x for x in SCENARIOS if x in s),'悲观' if '受损' in s else None)
def label(s):
    return next((x for x in LABELS if x in s),None)
def percents(s):
    s=s.replace('−','-').replace('－','-').replace('％','%').replace(',','')
    return [float(n) for n in re.findall(r'([+\-]?\d+(?:\.\d+)?)\s*%',s)]
data=[]; failures=[]
for f in sorted(SRC.glob('*.md')):
    raw=f.read_bytes(); text=raw.decode('utf-8-sig'); lines=text.splitlines(); tables=get_tables(lines)
    matrices=[]
    for t in tables:
        h=' '.join(t['header'])
        if len(t['header'])==4 and any(scenario(r[0]) for r in t['rows']) and (('短期' in h and ('长期' in h or '三年' in h)) or ('6个月' in h and '36' in h)):
            score=sum(len(r)>=4 and all(label(c) for c in r[1:4]) for r in t['rows'] if scenario(r[0]))
            matrices.append((score,t))
    matrices.sort(key=lambda x:x[0],reverse=True)
    matrix=matrices[0][1] if matrices and matrices[0][0]>=4 else None
    cells=[]
    if matrix:
        for r in matrix['rows']:
            sc=scenario(r[0])
            if sc and len(r)==4:
                for m,c in zip([6,12,36],r[1:]):
                    nums=percents(c)
                    cells.append({'scenario':sc,'months':m,'label':label(c),'text':c,'percent_values':nums,'source_line':matrix['line']})
    else: failures.append(f.name)
    majors=[i for i,s in enumerate(lines) if s.startswith('## ')]
    section2=majors[1] if len(majors)>1 else min(90,len(lines))
    intro='\n'.join(lines[:section2])
    detail=[]
    for t in tables:
        h=' '.join(t['header'])
        if len(t['header'])>=7 and ('回报' in h or '收益' in h) and any('建议' in ' '.join(r) for r in t['rows']):
            detail.append(t)
    current_tables=[t for t in tables if t['line']<=section2 and ('判断' in ' '.join(t['header']) or '期限' in ' '.join(t['header']))]
    data.append({'ticker':f.name.split('_')[0],'file':str(f),'date':re.search(r'2026-\d\d-\d\d',f.name)[0],'sha256':hashlib.sha256(raw).hexdigest(),'title':clean(lines[0].lstrip('# ')), 'intro':intro,'current_tables':current_tables,'matrix':matrix,'cells':cells,'details':detail,'tables':tables})
(WORK/'extracted_reports.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(WORK/'current_judgments.txt').write_text('\n\n'.join('===== '+d['ticker']+' =====\n'+d['intro'] for d in data),encoding='utf-8')
print('REPORTS',len(data),'MATRICES',sum(d['matrix'] is not None for d in data),'CELLS',sum(len(d['cells']) for d in data))
print('FAILURES',failures)
for d in data:
    if not d['matrix']:
        cand=[(t['line'],t['header']) for t in d['tables'] if any('短期' in x or '36个月' in x or '建议' in x for x in t['header'])]
        print(d['ticker'],json.dumps(cand,ensure_ascii=False))
for m in [6,12,36]:
    print('HORIZON',m)
    for s in SCENARIOS:
        c=[c for d in data for c in d['cells'] if c['months']==m and c['scenario']==s]
        print(s,dict(collections.Counter(c['label'] for c in c)))
