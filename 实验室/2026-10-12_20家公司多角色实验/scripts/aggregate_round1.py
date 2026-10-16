import csv,json,hashlib
from pathlib import Path
from collections import defaultdict
OUT=Path(__file__).resolve().parents[1]
universe={r['ticker']:r for r in json.loads((OUT/'01_inputs/universe.json').read_text(encoding='utf-8'))}
pool=defaultdict(list);reports=[];issues=[]
for p in sorted((OUT/'02_round1').glob('R[1-5]_*.json')):
    data=json.loads(p.read_text(encoding='utf-8-sig'))
    if 'nominations' not in data:continue
    nominations=data['nominations']
    tickers=[r['ticker'] for r in nominations]
    if len(tickers)!=20:issues.append(f'{p.name}: nominations={len(tickers)}')
    if len(tickers)!=len(set(tickers)):issues.append(f'{p.name}: duplicate tickers')
    for n in nominations:
        if n['ticker'] not in universe:issues.append(f'{p.name}: out of universe {n["ticker"]}');continue
        pool[n['ticker']].append(dict(researcher=p.stem,**n))
    reports.append(dict(file=p.name,role=data.get('role'),nominations=len(nominations),screened_count=data.get('screened_count'),deep_read_tickers=data.get('deep_read_tickers'),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
combined=[]
for t,views in pool.items():
    r=universe[t];combined.append(dict(ticker=t,name=r['name'],category=r['category'],reference_price=float(r['finance']['最新价格'].replace(',','')),nominations=len(views),ranks={v['researcher']:v.get('rank') for v in views},views=views))
combined.sort(key=lambda r:(-r['nominations'],r['ticker']))
result=dict(reports=reports,union_count=len(combined),issues=issues,candidates=combined,note='票数仅用于显示分歧和安排审计；同一底层来源不产生独立证据，不能直接当投资排名。')
(OUT/'03_round2/round1_union.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'03_round2/round1_union.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ticker','name','category','price','nominations','ranks'])
    for r in combined:w.writerow([r['ticker'],r['name'],r['category'],r['reference_price'],r['nominations'],json.dumps(r['ranks'],ensure_ascii=False)])
print(json.dumps({'reports':[{k:v for k,v in r.items() if k!='deep_read_tickers'} for r in reports],'union_count':len(combined),'issues':issues,'candidates':[{k:v for k,v in r.items() if k not in ['views','name','category']} for r in combined]},ensure_ascii=False,indent=2))
