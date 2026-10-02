from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests,json,sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).parent
source=json.loads((OUT/'最新行情及IV.json').read_text(encoding='utf-8'))
by={r['ticker']:r for r in source['results']}
TARGETS={'3m':'2026-06-09','6m':'2026-03-09','1y':'2025-09-09'}
def get(t):
    url='https://query1.finance.yahoo.com/v8/finance/chart/'+t
    params={'period1':int(datetime(2025,9,1,tzinfo=timezone.utc).timestamp()),'period2':int(datetime(2026,9,10,tzinfo=timezone.utc).timestamp()),'interval':'1d','events':'div,splits','includeAdjustedClose':'true'}
    resp=requests.get(url,params=params,headers={'User-Agent':'Mozilla/5.0'},timeout=25)
    resp.raise_for_status()
    payload=resp.json()
    (OUT/'原始行情与期权'/(t+'_history.json')).write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
    d=payload['chart']['result'][0]
    tz=ZoneInfo(d['meta'].get('exchangeTimezoneName','America/New_York'))
    q=d['indicators']['quote'][0]
    dates={datetime.fromtimestamp(ts,tz).strftime('%Y-%m-%d'):q['close'][i] for i,ts in enumerate(d['timestamp']) if q['close'][i] is not None}
    spot=by[t]['quote']['regularMarketPrice']
    out={'ticker':t,'endpoint':spot,'endpoint_date':'2026-09-09','source_url':resp.url,'anchors':{},'events':d.get('events',{})}
    for key,target in TARGETS.items():
        dt=max(x for x in dates if x<=target)
        assert (datetime.fromisoformat(target)-datetime.fromisoformat(dt)).days<=7
        out['anchors'][key]={'target':target,'date':dt,'close':dates[dt],'return':100*(spot/dates[dt]-1)}
    return out
rows={}
with ThreadPoolExecutor(max_workers=4) as pool:
    futures={pool.submit(get,t):t for t in source['selected']}
    for f in as_completed(futures):
        t=futures[f]
        try:rows[t]=f.result()
        except Exception as ex:rows[t]={'ticker':t,'error':str(ex)}
        print(t,{k:round(v['return'],2) for k,v in rows[t].get('anchors',{}).items()},rows[t].get('error',''),flush=True)
(OUT/'历史涨幅复核.json').write_text(json.dumps({'asof':'2026-09-09','results':[rows[t] for t in source['selected']]},ensure_ascii=False,indent=2),encoding='utf-8')
