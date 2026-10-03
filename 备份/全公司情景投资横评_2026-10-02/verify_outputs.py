from pathlib import Path
from datetime import datetime, timezone
import json, csv, re, math, hashlib, collections

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
a=json.loads((OUT/'analysis.json').read_text(encoding='utf-8'))
ex=json.loads((OUT/'extracted.json').read_text(encoding='utf-8'))
selected=json.loads((OUT/'重点20家判断.json').read_text(encoding='utf-8'))
companies=a['companies']; cs={c['ticker']:c for c in companies}
assert len(cs)==len(companies)==ex['index_count']==221
assert not ex['missing'] and not ex['extra']
assert len(selected)==len({m['ticker'] for m in selected})==20
assert set(m['ticker'] for m in selected).issubset(cs)
assert not a['stats']['validation_issues']

changed=[]; numeric_errors=[]; max_publication_error=0; source_rows=0
for c in companies:
 data=(ROOT/c['path']).read_bytes()
 if hashlib.sha256(data).hexdigest()!=c['sha256']:changed.append(c['ticker'])
 lines=data.decode('utf-8-sig').splitlines()
 assert set(c['scenarios'])=={'悲观','基准','乐观','突破'}
 assert c['quote']>0 and 2<c['years']<6.5
 for k,s in c['scenarios'].items():
  assert lines[s['line']-1]==s['raw'],(c['ticker'],k,'source row')
  assert len(s['price'])==len(s['return_published'])==2
  assert 0<=s['price'][0]<=s['price'][1]
  pts=re.findall(r'\d[\d,]*(?:\.\d+)?',s['price_text'])
  rts=re.findall(r'(\d+(?:\.\d+)?)\s*%',s['return_text'])
  if len(pts)==1:pts*=2
  if len(rts)==1:rts*=2
  assert len(pts)>=2 and len(rts)>=2
  for j in range(2):
   expected=(s['price'][j]/c['quote']-1)*100
   annual=((s['price'][j]/c['quote'])**(1/c['years'])-1)*100 if s['price'][j]>0 else -100
   assert abs(expected-s['return_calculated'][j])<1e-9
   assert abs(annual-s['annual_report'][j])<1e-9
   pd=len(pts[j].split('.')[1]) if '.' in pts[j] else 0
   rd=len(rts[j].split('.')[1]) if '.' in rts[j] else 0
   tolerance=.5*10**(-pd)/c['quote']*100+.5*10**(-rd)+1e-8
   err=abs(expected-s['return_published'][j])
   max_publication_error=max(max_publication_error,err)
   if err>tolerance:numeric_errors.append([c['ticker'],k,j,err,tolerance])
  source_rows+=1
assert not changed and not numeric_errors
assert source_rows==884

snap=ROOT/'金融资料/每日金融数据/每日金融数据_2026-10-02.md'
assert hashlib.sha256(snap.read_bytes()).hexdigest()==a['stats']['snapshot_hash']
assert cs['TOELY']['snapshot_compatible'] is False
assert all(cs['TOELY']['scenarios'][s]['return_snapshot'] is None for s in cs['TOELY']['scenarios'])

counts={}
for name,expected_rows,expected_tickers in [('全公司四情景复算.csv',884,221),('重点20家公司比较.csv',80,20)]:
 rows=list(csv.DictReader((OUT/name).open(encoding='utf-8-sig')))
 assert len(rows)==expected_rows
 assert len({r['ticker'] for r in rows})==expected_tickers
 per=collections.Counter(r['ticker'] for r in rows)
 assert all(n==4 for n in per.values())
 counts[name]={'rows':len(rows),'unique_tickers':len(per)}

allrows=list(csv.DictReader((OUT/'全公司四情景复算.csv').open(encoding='utf-8-sig')))
for r in allrows:
 c=cs[r['ticker']];s=c['scenarios'][r['scenario']]
 assert abs(float(r['annual_report_low'])-s['annual_report'][0])<=.000051
 assert abs(float(r['return_report_high'])-s['return_calculated'][1])<=.000051
 if r['ticker']=='TOELY':assert not r['snapshot_price'] and not r['return_snapshot_low']

broken_links=[]; checked_links=0
for name in ['综合分析与20家公司对比.md','全公司逐项明细.md']:
 text=(OUT/name).read_text(encoding='utf-8')
 assert '{{' not in text
 for raw in re.findall(r'\]\((/D:/[^\)]+)\)',text):
  raw=raw[1:];match=re.search(r':(\d+)$',raw);line=int(match.group(1)) if match else None
  target=Path(raw[:match.start()] if match else raw)
  if target.name=='复核记录.json':continue
  if not target.exists():broken_links.append(str(target))
  elif line:assert 1<=line<=len(target.read_text(encoding='utf-8-sig').splitlines())
  checked_links+=1
assert not broken_links
detail=(OUT/'全公司逐项明细.md').read_text(encoding='utf-8')
headtickers=re.findall(r'^### ([A-Z0-9.\-]+) — ',detail,re.M)
assert len(headtickers)==len(set(headtickers))==221 and set(headtickers)==set(cs)
main=(OUT/'综合分析与20家公司对比.md').read_text(encoding='utf-8')
deeptickers=re.findall(r'^### \d+\. ([A-Z0-9.\-]+) — ',main,re.M)
assert deeptickers==[m['ticker'] for m in selected]

result={
 'verified_at_utc':datetime.now(timezone.utc).isoformat(),
 'research_baseline':'2026-10-02',
 'index_companies':221,'source_reports':221,'scenario_rows':884,
 'selected_companies':20,'selected_scenario_rows':80,
 'missing_companies':[],'extra_companies':[],'source_reports_changed':changed,
 'price_return_formula_checks':'884 rows / 1768 endpoints passed',
 'annual_return_formula_checks':'884 rows / 1768 endpoints passed',
 'published_return_rounding_checks':'passed using displayed price and percentage precision',
 'max_published_return_difference_percentage_points':max_publication_error,
 'csv_counts':counts,'checked_local_links':checked_links,'broken_local_links':[],
 'snapshot_security_incompatibility':['TOELY'],
 'input_hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [ROOT/'基本面/公司调研/公司索引.md',snap,ROOT/'分析报告/公司情景投资决策/研究方案/研究方案_20261002_002635.md']},
 'scope_limit':'No independent full audit of all source-model operating, capital or terminal assumptions; primary-source checks are selective.'
}
(OUT/'复核记录.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
