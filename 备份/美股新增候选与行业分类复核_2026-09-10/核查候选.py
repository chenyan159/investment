from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from zoneinfo import ZoneInfo
import re,json,hashlib,math
import yfinance as yf

ROOT=Path(r'D:\drive\Investment')
OUT=Path(__file__).parent
SYMBOLS=['SYM','CGNX','ROK','EMR','AMBA','ALGM','TTMI','ITT','SPXC','CW','ASTS','PL','RDW','CCJ','LEU','NET','PANW','SNOW','DDOG','NOW','PLTR','SBGSY','FANUY','YASKY','SMCAY']
FIELDS=['symbol','shortName','longName','quoteType','exchange','fullExchangeName','currency','regularMarketPrice','regularMarketTime','marketCap','trailingPE','forwardPE','trailingEps','forwardEps','volume','averageVolume','website','longBusinessSummary']

def clean(v):
    if isinstance(v,float) and not math.isfinite(v):return None
    if isinstance(v,list):return [clean(x) for x in v]
    if isinstance(v,dict):return {k:clean(x) for k,x in v.items()}
    return v

def fetch(s):
    r={'symbol':s,'retrieved_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()}
    try:
        q=yf.Ticker(s).info
        r['quote']={k:q.get(k) for k in FIELDS}
    except Exception as e:r['error']=str(e)
    return clean(r)

if __name__=='__main__':
    index=ROOT/'基本面/公司调研/公司索引.md'
    text=index.read_text(encoding='utf-8')
    companies=[]
    for line in text.splitlines():
        if line.startswith('| ') and '`' in line:
            cells=[v.strip().strip('`').rstrip('/') for v in line.strip('|').split('|')]
            companies.append(dict(zip(['symbol','name','category'],cells)))
    existing={x['symbol'] for x in companies}
    assert len(existing)==193
    assert not existing.intersection(SYMBOLS),existing.intersection(SYMBOLS)
    reports=[p for c in (ROOT/'基本面/公司调研').iterdir() if c.is_dir() and c.name in {x['category'] for x in companies} for p in c.glob('*.md')]
    collisions=[str(p) for p in reports if p.name.split('_')[0] in SYMBOLS]
    assert not collisions,collisions
    industry_index=ROOT/'基本面/行业调研/行业索引.md'
    industries=[]
    for line in industry_index.read_text(encoding='utf-8').splitlines():
        if line.startswith('| ') and '`' in line:
            cells=[v.strip().strip('`').rstrip('/') for v in line.strip('|').split('|')]
            industries.append({'name':cells[0],'category':cells[1],'scope_note':cells[2] if len(cells)>2 else ''})
    industry_files=[p for c in (ROOT/'基本面/行业调研').iterdir() if c.is_dir() and c.name in {x['category'] for x in industries} for p in c.glob('行业调研_*.md')]
    audit={'checked_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'company_index':str(index),'company_index_sha256':hashlib.sha256(index.read_bytes()).hexdigest(),'existing_companies':companies,'new_candidates':SYMBOLS,'active_report_collision_count':len(collisions),'industry_index':str(industry_index),'industry_index_sha256':hashlib.sha256(industry_index.read_bytes()).hexdigest(),'industry_index_count':len(industries),'industries':industries,'industry_files':[{'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':len(p.read_text(encoding='utf-8').splitlines())} for p in industry_files]}
    (OUT/'项目覆盖核验.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    rows=[]
    with ThreadPoolExecutor(max_workers=6) as pool:
        for f in as_completed([pool.submit(fetch,s) for s in SYMBOLS]):
            r=f.result();rows.append(r);q=r.get('quote',{});print(json.dumps({'symbol':r['symbol'],'name':q.get('longName'),'exchange':q.get('exchange'),'currency':q.get('currency'),'price':q.get('regularMarketPrice'),'error':r.get('error')},ensure_ascii=False),flush=True)
    rows.sort(key=lambda r:SYMBOLS.index(r['symbol']))
    (OUT/'美股交易身份与行情核查.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    print('SAVED',len(rows),flush=True)
