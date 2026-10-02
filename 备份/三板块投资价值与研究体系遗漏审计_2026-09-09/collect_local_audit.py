from pathlib import Path
import json, hashlib, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(r'D:\drive\Investment'); OUT=Path(__file__).parent
MFILE=ROOT/'备份/20家公司投资价值与多维图谱_2026-09-09/market_scenario_data.json'
market=json.loads(MFILE.read_text(encoding='utf-8'))
by={c['ticker']:c for c in market['companies']}
groups={
 '通信':['CRDO','LITE','COHR','FN','ANET','CIEN','GLW','ALAB','MRVL','MTSI','AAOI','POET','AXTI','SMTC','CSCO'],
 'NeoCloud':['CRWV','IREN','NBIS','APLD','ORCL','DLR','EQIX'],
 '电力设备及工程':['ETN','NVT','HUBB','POWL','VRT','GEV','PWR','FIX','EME','IESC','MOD','AAON','MPWR','VICR','NVTS','ABBNY','MIELY','HTHIY','BE','GNRC','CAT','CMI','ATKR'],
}
old=json.loads((ROOT/'备份/AI乐观情景_增长与下行保护20家公司_2026-09-09/20家公司合并数据.json').read_text(encoding='utf-8'))
old20=[c['ticker'] for c in old['rows']]
targets=list(dict.fromkeys(sum(groups.values(),[])+old20))
rows=[]; manifest=[]; intros=[]
for t in targets:
 c=by[t]; p=Path(c['file']); txt=p.read_text(encoding='utf-8')
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 row={'ticker':t,'name':c['name'],'sector':c['sector'],'in_prior20':t in old20,'price':c['quote']['price'],'pe':c['quote']['pe'],'forward_pe':c['quote']['forward_pe'],
      'history_returns':{k:c['history'].get('anchors',{}).get(k,{}).get('return') for k in ['3m','6m','1y']},
      'scenarios':{f"{v['scenario']}_{v['months']}m":{'low':v.get('rebased_low'),'high':v.get('rebased_high'),'label':v['label'],'source_line':v['source_line']} for v in c['cells']},
      'report_path':str(p),'report_date':c['report_date'],'source_hash_matches':digest==c['source_sha256'],'current_sha256':digest,
      'company_report_paths':[str(q) for q in (ROOT/'基本面/公司调研').rglob(t+'_*.md') if not any(x in q.parts for x in ['tmp','备份','评估备份'])]}
 rows.append(row)
 lines=txt.splitlines()
 intros.append('\n## '+t+'\n来源：'+str(p)+'\n'+ '\n'.join(f'{i+1}: {s}' for i,s in enumerate(lines[:95])))
 manifest.append({'path':str(p),'sha256':digest,'same_as_prior_analysis':row['source_hash_matches']})
def val(v):return 'NA' if v is None else f'{v:.1f}'
def band(c,s):
 v=c['scenarios'].get(s+'_36m',{})
 return val(v.get('low'))+'..'+val(v.get('high'))
lookup={r['ticker']:r for r in rows}
tables=[]
for group,tickers in groups.items():
 tables.append('\n### '+group+'\n|公司|现价|PE|FPE|基准3年%|乐观3年%|突破3年%|悲观3年%|原20|\n|---|---:|---:|---:|---:|---:|---:|---:|---|')
 for t in tickers:
  c=lookup[t]
  tables.append('|'+ '|'.join([t,val(c['price']),val(c['pe']),val(c['forward_pe']),band(c,'基准'),band(c,'乐观'),band(c,'突破'),band(c,'悲观'),'是' if c['in_prior20'] else ''])+'|')
plans=[ROOT/'基本面/行业调研/研究方法/行业调研方案.md',ROOT/'基本面/公司调研/研究方法/调研方案.md',ROOT/'分析报告/公司情景投资决策/研究方案.md']
for p in plans:manifest.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':len(p.read_text(encoding='utf-8').splitlines())})
(OUT/'本地情景与比较数据.json').write_text(json.dumps({'asof':'2026-09-09','groups':groups,'prior20':old20,'rows':rows,'manifest':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'本地报告开头摘录.md').write_text('\n'.join(intros),encoding='utf-8')
(OUT/'现有模型横向对照.md').write_text('\n'.join(tables),encoding='utf-8')
print('\n'.join(tables))
print('hash mismatches:',[r['ticker'] for r in rows if not r['source_hash_matches']])
print('company report gaps:',[r['ticker'] for r in rows if not r['company_report_paths']])
print('universe gaps:',[t for t in ['CORZ','HUT','WULF','CIFR','RIOT','MARA','CLSK','BTDR','BTBT','BITF','SU.PA','STRL','TLN','VST'] if t not in by])
