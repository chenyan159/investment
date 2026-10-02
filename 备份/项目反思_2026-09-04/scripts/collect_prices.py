from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json, time, hashlib, requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parents[1] / '分析报告/公司排序/90_有效性评估/2026-07-13_26方案3月6月生成前历史回看/03_192家公司独立复权价3月6月收益.csv'
RAW = ROOT/'data/price_raw'; RAW.mkdir(exist_ok=True)
universe = pd.read_csv(SOURCE)[['ticker','company','category','vendor_symbol']]
universe.to_csv(ROOT/'data/universe.csv',index=False,encoding='utf-8-sig')
symbols = universe.vendor_symbol.tolist() + ['SPY','QQQ','SOXX','SMH','IWM','RSP','IGV','XLU','XLI','XLE','TLT','HYG','USO','^VIX','^GSPC','^TNX']
p1=int(datetime(2026,1,1,tzinfo=timezone.utc).timestamp())
p2=int(datetime(2026,9,5,tzinfo=timezone.utc).timestamp())

def get(symbol):
    path=RAW/(symbol.replace('^','INDEX_')+'.json')
    url=f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={p1}&period2={p2}&interval=1d&events=div%2Csplits'
    if path.exists():
        payload=json.loads(path.read_text(encoding='utf-8'))
    else:
        for attempt in range(3):
            try:
                r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=35);r.raise_for_status()
                payload={'fetched_at':datetime.now(timezone.utc).isoformat(),'url':url,'data':r.json()}
                if not payload['data']['chart']['result']: raise ValueError(str(payload['data']))
                path.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8');break
            except Exception as e:
                if attempt==2:return [],{'symbol':symbol,'status':'error','error':str(e),'url':url}
                time.sleep(1+attempt)
    j=payload['data']['chart']['result'][0];m=j['meta'];q=j['indicators']['quote'][0]
    adj=j['indicators'].get('adjclose',[{}])[0].get('adjclose',[])
    rows=[]
    for i,ts in enumerate(j.get('timestamp',[])):
        d=datetime.fromtimestamp(ts,ZoneInfo(m['exchangeTimezoneName'])).date().isoformat()
        if d>'2026-09-04':continue
        row={'symbol':symbol,'date':d,'timestamp':ts}
        for key in ['open','high','low','close','volume']:row[key]=q.get(key,[None]*len(j['timestamp']))[i]
        row['adj_close']=adj[i] if i<len(adj) else None
        rows.append(row)
    meta={key:m.get(key) for key in ['symbol','longName','shortName','currency','exchangeName','exchangeTimezoneName','regularMarketTime','regularMarketPrice','firstTradeDate']}
    meta.update(status='ok',requested_symbol=symbol,first_date=rows[0]['date'] if rows else None,last_date=rows[-1]['date'] if rows else None,row_count=len(rows),events=json.dumps(j.get('events',{})),url=url,raw_path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return rows,meta

rows=[];metadata=[]
with ThreadPoolExecutor(max_workers=8) as ex:
    fs={ex.submit(get,s):s for s in symbols}
    for n,f in enumerate(as_completed(fs),1):
        rr,mm=f.result();rows.extend(rr);metadata.append(mm)
        if n%20==0 or mm['status']!='ok':print(n,fs[f],mm['status'],flush=True)
pd.DataFrame(rows).sort_values(['symbol','date']).to_csv(ROOT/'data/daily_prices.csv',index=False,encoding='utf-8-sig')
pd.DataFrame(metadata).sort_values('symbol').to_csv(ROOT/'data/price_manifest.csv',index=False,encoding='utf-8-sig')
print('DONE',len(metadata),len(rows),flush=True)
