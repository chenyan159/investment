import csv, hashlib, json, re, shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('D:/investment')
OUT = ROOT/'实验室/2026-10-12_20家公司多角色实验'
for d in ['00_control','01_inputs/frozen','01_inputs/dossiers','02_round1','03_round2','04_verification','05_chair','06_final','07_logs','scripts','tmp']:
    (OUT/d).mkdir(parents=True,exist_ok=True)
assert OUT.resolve().is_relative_to((ROOT/'实验室').resolve())

def dump(p, v):
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')

roots = ['基本面/公司调研/结果','基本面/行业调研/结果','基本面/产业背景/结果','分析报告/公司情景投资决策/结果','分析报告/公司对比/结果']
files = [ROOT/'基本面/公司调研/公司索引.md', ROOT/'基本面/行业调研/行业索引.md',ROOT/'金融资料/每日金融数据/每日金融数据_2026-10-12.md',ROOT/'金融资料/每日金融数据/每日金融数据_2026-10-09.md']
for r in roots:
    files += [p for p in (ROOT/r).rglob('*') if p.is_file() and p.suffix in ['.md','.json']]
for r in ['','基本面','基本面/公司调研','基本面/行业调研','基本面/产业背景','分析报告','分析报告/公司情景投资决策','分析报告/公司对比','金融资料']:
    for n in ['AGENTS.md','README.md']:
        p=ROOT/r/n
        if p.is_file(): files.append(p)
for r in ['基本面/公司调研','基本面/行业调研','分析报告/公司情景投资决策','分析报告/公司对比']:
    files += list((ROOT/r/'研究方案').glob('研究方案_*.md'))
    p=ROOT/r/'研究方案/README.md'
    if p.exists(): files.append(p)
manifest=[]
for p in sorted(set(files)):
    rel=p.relative_to(ROOT)
    dest=OUT/'01_inputs/frozen'/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    data=p.read_bytes()
    dest.write_bytes(data)
    manifest.append(dict(path=str(rel).replace('\\','/'),size=len(data),sha256=hashlib.sha256(data).hexdigest(),mtime_utc=datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat()))
dump(OUT/'00_control/input_manifest.json',manifest)

frozen=OUT/'01_inputs/frozen'
index=(frozen/'基本面/公司调研/公司索引.md').read_text(encoding='utf-8-sig')
rows=[]
for line in index.splitlines():
    parts=[x.strip() for x in line.strip().strip('|').split('|')]
    if len(parts)==6 and re.fullmatch(r'[A-Z][A-Z0-9.\-]*',parts[0]):
        rows.append(dict(ticker=parts[0],name=parts[1],category=parts[2].strip('`/'),business_tags=parts[3],industry_tags=parts[4],security_notes=parts[5]))
assert len(rows)==245 and len({r['ticker'] for r in rows})==245
snapshot=(frozen/'金融资料/每日金融数据/每日金融数据_2026-10-12.md').read_text(encoding='utf-8-sig')
headers=None; finance={}
for lineno,line in enumerate(snapshot.splitlines(),1):
    if not line.startswith('|'): continue
    parts=[x.strip() for x in line.strip().strip('|').split('|')]
    if parts[0]=='股票代号': headers=parts;continue
    if headers and len(parts)==len(headers) and parts[0] in {r['ticker'] for r in rows}:
        finance[parts[0]]=dict(zip(headers,parts)); finance[parts[0]]['source_line']=lineno
assert len(finance)==245
counts={}
for row in rows:
    t=row['ticker']; row['finance']=finance[t]; row['sources']={}
    sections=[f'# {t} {row["name"]}',f'Category: {row["category"]}', '## 冻结金融数据',json.dumps(finance[t],ensure_ascii=False,indent=2)]
    for label,rel,limit in [('company','基本面/公司调研/结果',75),('scenario','分析报告/公司情景投资决策/结果',100),('comparison','分析报告/公司对比/结果',95)]:
        matches=sorted((frozen/rel).rglob(f'{t}_*.md'))
        row['sources'][label]=[str(p.relative_to(OUT)).replace('\\','/') for p in matches]
        counts[label]=counts.get(label,0)+bool(matches)
        if matches:
            p=matches[-1];lines=p.read_text(encoding='utf-8-sig').splitlines()
            sections += [f'## {label} 开头摘录（非完整报告；请继续按目录深读）',f'文件: {p}', '\n'.join(f'{i+1}: {v}' for i,v in enumerate(lines[:limit])), '### 全文小节索引', '\n'.join(f'{i}: {v}' for i,v in enumerate(lines,1) if v.startswith('#'))]
        else: sections.append(f'## {label}: 无冻结正式MD，不能当作已研究')
    (OUT/f'01_inputs/dossiers/{t}.md').write_text('\n\n'.join(sections),encoding='utf-8')
dump(OUT/'01_inputs/universe.json',rows)
dump(OUT/'01_inputs/financial_snapshot.json',finance)
with (OUT/'01_inputs/universe_screen.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ticker','name','category','price','price_date','market_cap','forward_pe','forward_eps','ps','currency','financial_currency','validation','company_md','scenario_md','comparison_md'])
    for r in rows:
        q=r['finance'];w.writerow([r['ticker'],r['name'],r['category'],q['最新价格'],q['价格日期'],q['市值'],q['Forward PE'],q['forward_eps'],q['P/S'],q['currency'],q['financial_currency'],q['估值校验'],bool(r['sources']['company']),bool(r['sources']['scenario']),bool(r['sources']['comparison'])])
summary={'frozen_files':len(manifest),'bytes':sum(m['size'] for m in manifest),'companies':len(rows),'categories':len(set(r['category'] for r in rows)),'coverage':counts,'frozen_utc':datetime.now(timezone.utc).isoformat()}
dump(OUT/'00_control/freeze_summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
