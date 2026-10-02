from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from zoneinfo import ZoneInfo
import requests, json, re, math, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).parent
RAW=OUT/'原始行情与期权'
source=json.loads((OUT/'最新行情及IV.json').read_text(encoding='utf-8'))
by={r['ticker']:r for r in source['results']}
ASOF=date(2026,9,9)
EXPIRY='2026-10-16'

def get(t):
    stamp=datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()
    path=RAW/(t+'_cboe.json')
    url='https://cdn.cboe.com/api/global/delayed_quotes/options/'+t+'.json'
    if path.exists():
        payload=json.loads(path.read_text(encoding='utf-8'))
    else:
        response=requests.get(url,timeout=25)
        response.raise_for_status()
        payload=response.json()
        path.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
    data=payload['data']
    spot=by[t]['quote']['regularMarketPrice']
    selected=[]
    for o in data['options']:
        match=re.fullmatch(re.escape(t)+r'(\d{6})([CP])(\d{8})',o['option'])
        if not match or match[1]!='261016' or match[2]!='C':continue
        k=int(match[3])/1000
        iv,bid,ask=o.get('iv'),o.get('bid'),o.get('ask')
        if any(v is None or not math.isfinite(v) for v in [iv,bid,ask]):continue
        if not (.01<=iv<=3 and bid>0 and ask>=bid):continue
        if abs(k/spot-1)>.05:continue
        if (ask-bid)/((bid+ask)/2)>.30:continue
        if (o.get('volume') or 0)+(o.get('open_interest') or 0)<1:continue
        if not o.get('last_trade_time'):continue
        dt=date.fromisoformat(o['last_trade_time'][:10])
        if not (0<=(ASOF-dt).days<=7):continue
        selected.append({**o,'strike':k})
    result={'ticker':t,'collected_at':stamp,'source_timestamp_raw':payload['timestamp'],'source_timestamp_timezone':'not specified in response',
       'source_underlying_last_trade_time':data.get('last_trade_time'),'source_underlying_close':data.get('close'),'source_underlying_current_price':data.get('current_price'),
       'reference_close':spot,'expiry':EXPIRY,'dte_calendar':37,'source_url':url,'source_display_url':'https://www.cboe.com/delayed_quotes/'+t.lower()+'/quote_table/',
       'source':'Cboe delayed quotes: single near-ATM call source implied volatility; no IV30 substitution.',
       'clean_call_count':len(selected),'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if selected:
        row=min(selected,key=lambda o:(abs(o['strike']-spot),-(o.get('open_interest') or 0)-(o.get('volume') or 0)))
        result.update({'iv_percent':row['iv']*100,'call':row,'strike_distance_percent':abs(row['strike']/spot-1)*100,'relative_spread_percent':100*(row['ask']-row['bid'])/((row['bid']+row['ask'])/2)})
    else:result.update({'iv_percent':None,'missing_reason':'No eligible call passed fixed filters.'})
    return result

results={'HTHIY':{'ticker':'HTHIY','iv_percent':None,'missing_reason':'No same-security US option chain from Yahoo; OTC ADR. No Tokyo-security or historical volatility proxy substituted.'}}
with ThreadPoolExecutor(max_workers=3) as pool:
    futures={pool.submit(get,t):t for t in source['selected'] if t!='HTHIY'}
    for f in as_completed(futures):
        t=futures[f]
        try:results[t]=f.result()
        except Exception as exc:results[t]={'ticker':t,'iv_percent':None,'missing_reason':str(exc)}
        r=results[t]
        print(t,'IV',r['iv_percent'],'K',r.get('call',{}).get('strike'),'quote_asof',r.get('source_timestamp_raw'),r.get('missing_reason',''),flush=True)
payload={'asof':str(ASOF),'expiry':EXPIRY,'dte_calendar':37,'collected_completed_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),
 'method':'Cboe delayed option data, same expiry nearest eligible near-ATM call source IV annualized. Quote timestamp per-contract unavailable; trade and file timestamps are not interchangeable.',
 'selected':source['selected'],'results':[results[t] for t in source['selected']]}
(OUT/'可用IV核查.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',payload['collected_completed_at'])
