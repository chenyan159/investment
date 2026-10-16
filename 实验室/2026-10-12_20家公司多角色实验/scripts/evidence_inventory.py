"""Inventory provenance without treating repeated mentions as independent evidence."""
import csv, json, re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
universe = json.loads((ROOT/'01_inputs/universe.json').read_text(encoding='utf-8'))
if isinstance(universe, dict):
    universe = universe.get('companies', universe.get('universe', []))
tickers = {r['ticker'] for r in universe}
coverage = {t: {'ticker': t, 'blind_nominations': [], 'blind_deep_read': [], 'document_mentions': [], 'source_log_mentions': []} for t in tickers}
reports = []
for path in sorted((ROOT/'02_round1').glob('R[1-5]_*.json')):
    obj=json.loads(path.read_text(encoding='utf-8'))
    role=obj.get('role',path.stem)
    deep=obj.get('deep_read_tickers', [])
    noms=obj.get('nominations', [])
    reports.append({'role':role,'screened':obj.get('screened_count'),'deep_count':len(deep),'nominations':len(noms)})
    for t in deep:
        if t in coverage: coverage[t]['blind_deep_read'].append(role)
    for r in noms:
        if r['ticker'] in coverage: coverage[r['ticker']]['blind_nominations'].append(role)

sources=[]
def walk(x, file, parent_ticker=None):
    if isinstance(x, dict):
        target=x.get('ticker',x.get('tickers',parent_ticker))
        for key,value in x.items():
            if isinstance(value,str) and value.startswith(('https://','http://')):
                u=urlsplit(value)
                canon=urlunsplit((u.scheme,u.netloc.lower(),u.path.rstrip('/'),u.query,''))
                sources.append({'file':file,'url':value,'canonical_url':canon,'ticker':target,'status':x.get('status',x.get('access_status','unspecified')),'event_id':x.get('event_id',x.get('root_event','unassigned')),'date':x.get('date',x.get('published_date',''))})
            elif isinstance(value,(dict,list)):walk(value,file,target)
    elif isinstance(x,list):
        for row in x:walk(row,file,parent_ticker)

for path in sorted((ROOT/'07_logs').glob('*sources*.json')):
    try:
        obj=json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        sources.append({'file':path.name,'parse_error':str(e)}); continue
    walk(obj,str(path.relative_to(ROOT)))
    body=path.read_text(encoding='utf-8')
    for t in tickers:
        if re.search(r'(?<![A-Z0-9])'+re.escape(t)+r'(?![A-Z0-9])',body):coverage[t]['source_log_mentions'].append(path.stem)
for folder in ('03_round2','04_verification','05_chair'):
    for path in (ROOT/folder).glob('*.md'):
        body=path.read_text(encoding='utf-8')
        for t in tickers:
            if re.search(r'(?<![A-Z0-9])'+re.escape(t)+r'(?![A-Z0-9])',body):coverage[t]['document_mentions'].append(str(path.relative_to(ROOT)))
out={'blind_reports':reports,'unique_blind_deep_read':sum(bool(v['blind_deep_read']) for v in coverage.values()),'source_url_records':len([s for s in sources if 'url' in s]),'unique_source_urls':len({s['canonical_url'] for s in sources if 'canonical_url' in s}),'coverage':sorted(coverage.values(),key=lambda x:x['ticker']),'sources':sources,'warning':'Mentions are navigation only, not a completed verification or independent-source count. Same corporate event may have multiple URLs. Inspect each decisive evidence chain manually.'}
(ROOT/'00_control/evidence_inventory.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'00_control/evidence_coverage.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(next(iter(coverage.values())).keys()));writer.writeheader()
    for v in sorted(coverage.values(),key=lambda x:x['ticker']):writer.writerow({k:'; '.join(val) if isinstance(val,list) else val for k,val in v.items()})
print(json.dumps({k:v for k,v in out.items() if k not in ('coverage','sources')},ensure_ascii=False,indent=2))
