from pathlib import Path
import json,re,collections,csv,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('D:/drive/Investment'); OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05'
allrows=[]; summary=[]; excerpts=[]
for p in sorted((ROOT/'基本面/特征量化/量化评分').glob('*.md')):
 t=p.read_text(encoding='utf-8-sig'); lines=t.splitlines(); fid=p.name[:3]
 header=None;rows=[];tables=[]
 for n,l in enumerate(lines,1):
  if l.startswith('|'):
   cells=[x.strip().strip('`') for x in re.split(r'(?<!\\)\|',l.strip().strip('|'))]
   if 'display_score' in cells:
    if rows:tables.append(rows)
    rows=[];header=cells;continue
   if header and len(cells)==len(header) and not all(re.fullmatch(r'[:\- ]+',x) for x in cells):
    r=dict(zip(header,cells))
    ident=next((r[k] for k in ['ticker','security','symbol','股票代号','公司','company'] if k in r),'')
    m=re.match(r'^([A-Z][A-Z0-9.\-]{0,9})(?:$|\s|（|\()',ident)
    if m:rows.append(r|{'ticker_normalized':m.group(1),'line':n})
   elif header and len(cells)!=len(header):
    if rows:tables.append(rows)
    rows=[];header=None
  elif header and rows:
   tables.append(rows);rows=[];header=None
 if rows:tables.append(rows)
 rows=max(tables,key=len) if tables else []
 if not rows:
  for n,l in enumerate(lines,1):
   if l.strip().startswith('{'):
    try:r=json.loads(l.strip())
    except:continue
    if isinstance(r,dict) and any(k in r for k in ['display_score','gate_status']):rows.append(r|{'line':n})
 for r in rows:allrows.append({'feature_id':fid,'path':p.relative_to(ROOT).as_posix(),**r})
 vals=[r.get('display_score') for r in rows]
 def num(x):
  try:return float(x)
  except:return None
 nums=[num(x) for x in vals if num(x) is not None]
 summary.append({'feature_id':fid,'report':p.relative_to(ROOT).as_posix(),'rows_parsed':len(rows),'numeric_scores_parsed':len(nums),'score_mode':collections.Counter(nums).most_common(3),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 chosen=[]
 for n,l in enumerate(lines,1):
  if n<=100 and not len(l)>950 and re.search(r'结论|192|NA|数据|缺失|覆盖|三|季度|门槛|可评分|有效|计算|约束',l):chosen.append(f'{n}: {l}')
 excerpts.append('## '+p.name+'\n\n[原报告](<'+p.as_posix()+'>)；以下为带原始行号的逐字摘录，内部相对链接保留原文，不作为此审计目录的导航。\n\n```text\n'+'\n'.join(chosen[:18])+'\n```')
(OUT/'data/feature_rows.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'data/feature_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'evidence/特征量化_截面原文摘录.md').write_text('\n\n'.join(excerpts),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
for p in sorted((ROOT/'基本面/特征量化/研究方案').glob('*.md')):
 ls=p.read_text(encoding='utf-8-sig').splitlines(); print('\nPLAN',p.name,'lines',len(ls))
 for n,l in enumerate(ls,1):
  if re.search(r'^##|自由|裁量|公式|权重|前瞻|个月|三桶|1.0|标准化',l) and len(l)<400:print(n,l)
