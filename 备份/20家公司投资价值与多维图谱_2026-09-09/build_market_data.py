from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import requests, json, re, math, hashlib, statistics, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'D:\drive\Investment')
OUT = Path(__file__).parent
RAW = OUT / '原始行情'
RAW.mkdir(exist_ok=True)
ASOF = '2026-09-09'
SELECTED = ['ADBE','ET','MU','MSFT','PNR','BABA','META','GOOGL','SMCI','NVDA','ASML','TSM','AMZN','AVGO','AEP','DKILY','ST','BDC','DOV','FLNC']
source = ROOT / '备份/全部公司情景投资综合分析_2026-09-09/analysis_data.json'
reports = json.loads(source.read_text(encoding='utf-8'))
snapshot = ROOT / '金融资料/每日金融数据/每日金融数据_2026-09-09.md'
fields = ['ticker','name','price_date','price','market_cap','pe','forward_pe','ps','pb','ev_ebitda','eps','call_iv','put_iv','currency','financial_currency','shares','ttm_revenue','ttm_eps','forward_eps','listing_type','adr_ratio','data_source','source_timestamp','valuation_check','note']
snap = {}
def num(v):
    try: return float(str(v).replace(',',''))
    except (ValueError,TypeError): return None
for line in snapshot.read_text(encoding='utf-8-sig').splitlines():
    row = [s.strip() for s in line.strip('|').split('|')]
    if len(row)==25 and re.fullmatch('[A-Z]+',row[0]):
        item=dict(zip(fields,row))
        for k in ['price','pe','forward_pe','eps','ttm_eps','forward_eps','call_iv','put_iv']:
            item[k+'_raw']=item[k]; item[k]=num(item[k])
        snap[row[0]]=item

def download(ticker):
    rawpath=RAW/(ticker+'.json')
    url='https://query1.finance.yahoo.com/v8/finance/chart/'+ticker
    params={'period1':int(datetime(2025,8,29,tzinfo=timezone.utc).timestamp()),'period2':int(datetime(2026,9,10,tzinfo=timezone.utc).timestamp()),'interval':'1d','events':'div,splits','includeAdjustedClose':'true'}
    if rawpath.exists(): payload=json.loads(rawpath.read_text(encoding='utf-8'))
    else:
        response=requests.get(url,params=params,headers={'User-Agent':'Mozilla/5.0'},timeout=35)
        response.raise_for_status()
        payload=response.json()
        rawpath.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
    if not payload['chart']['result']: raise ValueError(str(payload['chart']['error']))
    result=payload['chart']['result'][0]
    meta=result['meta']; quote=result['indicators']['quote'][0]
    tz=ZoneInfo(meta.get('exchangeTimezoneName','America/New_York'))
    adjusted=result['indicators'].get('adjclose',[{}])[0].get('adjclose',[])
    rows=[]
    for i,t in enumerate(result.get('timestamp',[])):
        date=datetime.fromtimestamp(t,tz).strftime('%Y-%m-%d')
        close=quote['close'][i]
        if date<=ASOF and close is not None and close>0:
            rows.append({'date':date,'close':close,'adjclose':adjusted[i] if i<len(adjusted) else None,'volume':quote.get('volume',[None]*len(quote['close']))[i]})
    if not rows: raise ValueError('no valid daily close')
    # Today's chart row can be null even after the regular close. The dated
    # official workspace quote snapshot supplies the SAME security's endpoint.
    q=snap.get(ticker)
    endpoint_source='Yahoo daily chart'
    if q and q['price_date']==ASOF and q['price']:
        rows=[r for r in rows if r['date']!=ASOF]
        rows.append({'date':ASOF,'close':q['price'],'adjclose':None,'volume':None})
        endpoint_source=str(snapshot)
    elif not q and meta.get('regularMarketTime') and datetime.fromtimestamp(meta['regularMarketTime'],tz).strftime('%Y-%m-%d')==ASOF and meta.get('regularMarketPrice'):
        rows=[r for r in rows if r['date']!=ASOF]
        rows.append({'date':ASOF,'close':meta['regularMarketPrice'],'adjclose':None,'volume':None})
        endpoint_source='Yahoo chart metadata regularMarketPrice with same-day regularMarketTime'
    rows.sort(key=lambda x:x['date'])
    last=rows[-1]
    def history_at(target):
        valid=[r for r in rows if r['date']<=target]
        if not valid:return None
        r=valid[-1]
        lag=(datetime.fromisoformat(target)-datetime.fromisoformat(r['date'])).days
        if lag>7:return None
        return {**r,'target':target,'return':100*(last['close']/r['close']-1)}
    anchors={k:history_at(target) for k,target in {'3m':'2026-06-09','6m':'2026-03-09','1y':'2025-09-09'}.items()}
    year=[r for r in rows if r['date']>='2025-09-09']
    peak=year[0]['close']; mdd=0
    for r in year:
        peak=max(peak,r['close']); mdd=min(mdd,100*(r['close']/peak-1))
    dr=[math.log(y['close']/x['close']) for x,y in zip(year,year[1:])]
    full_year=bool(anchors['1y']) and len(year)>=220
    return {'ticker':ticker,'endpoint':last,'endpoint_source':endpoint_source,'meta':{k:meta.get(k) for k in ['symbol','longName','shortName','instrumentType','currency','exchangeName','exchangeTimezoneName','regularMarketPrice','regularMarketTime','firstTradeDate']},'anchors':anchors,'mdd_1y':mdd if full_year else None,'vol_1y':statistics.stdev(dr)*math.sqrt(252)*100 if full_year else None,'gap_from_1y_max':100*(last['close']/max(r['close'] for r in year)-1) if full_year else None,'rows':rows,'events':result.get('events',{}),'source_url':url,'params':params,'raw_sha256':hashlib.sha256(rawpath.read_bytes()).hexdigest()}

histories={}; errors={}
with ThreadPoolExecutor(max_workers=6) as executor:
    futures={executor.submit(download,t):t for t in [d['ticker'] for d in reports]+['SPY','QQQ','SMH']}
    for i,future in enumerate(as_completed(futures),1):
        ticker=futures[future]
        try:histories[ticker]=future.result()
        except Exception as exc:errors[ticker]=str(exc)
        if i%40==0:print('downloaded',i,flush=True)
combined=[]
for d in reports:
    t=d['ticker']
    combined.append({'ticker':t,'name':d['name'],'sector':d['sector'],'file':d['file'],'source_sha256':d['sha256'],'report_date':d['date'],'anchor_price':d['anchor_price'],'quote':snap[t],'history':histories.get(t),'cells':d['cells'],'rank':SELECTED.index(t)+1 if t in SELECTED else None})
dataset={'asof':ASOF,'retrieved_at':datetime.now().astimezone().isoformat(),'selected':SELECTED,'companies':combined,'benchmarks':{t:histories.get(t) for t in ['SPY','QQQ','SMH']},'errors':errors,'snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),'method':'Calendar 3/6/12 months. Latest valid split-adjusted daily Close on/before target (maximum lag 7 days); endpoint same-day local quote snapshot. Excludes dividends and taxes; Adj Close not used. Three-year scenarios are conditional total economic returns, not measured historical returns. No probabilities assigned.'}
(OUT/'market_scenario_data.json').write_text(json.dumps(dataset,ensure_ascii=False,indent=2),encoding='utf-8')
print('ERRORS',errors)
for t in SELECTED:
    d=next(x for x in combined if x['ticker']==t); h=d['history'] or {}; q=d['quote']
    print(t,q['price'],q['pe_raw'],q['forward_pe_raw'],{k:round(v['return'],2) if v else None for k,v in h.get('anchors',{}).items()},'MDD',round(h.get('mdd_1y') or 0,2),'splits',h.get('events',{}).get('splits',{}))
