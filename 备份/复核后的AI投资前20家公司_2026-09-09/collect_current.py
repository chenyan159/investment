from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, date
from zoneinfo import ZoneInfo
import yfinance as yf
import requests, json, math, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).parent
ROOT=OUT.parent.parent
RAW=OUT/'原始行情与期权'
RAW.mkdir(exist_ok=True)
ASOF=date(2026,9,9)
EXPIRY='2026-10-16'
SELECTED=['NVDA','MSFT','MU','META','GOOGL','AMZN','AVGO','TSM','BABA','CRDO','ASML','HTHIY','NVT','EME','ADBE','TEL','APH','JBL','SNDK','ET']
market=json.loads((ROOT/'备份/20家公司投资价值与多维图谱_2026-09-09/market_scenario_data.json').read_text(encoding='utf-8'))
by={c['ticker']:c for c in market['companies']}

def clean_call(row,spot):
    vs=[row.get(k) for k in ('strike','impliedVolatility','bid','ask')]
    if any(v is None or not math.isfinite(v) for v in vs):return False
    k,iv,bid,ask=vs
    if not (.01<=iv<=3 and bid>0 and ask>=bid):return False
    if abs(k/spot-1)>.05:return False
    if (ask-bid)/((bid+ask)/2)>.30:return False
    if (row.get('volume') or 0)+(row.get('openInterest') or 0)<1:return False
    if not row.get('lastTradeDate'):return False
    dt=datetime.fromisoformat(row['lastTradeDate'].replace('Z','+00:00')).astimezone(ZoneInfo('America/New_York')).date()
    return 0<=(ASOF-dt).days<=7

def get(ticker):
    collected=datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()
    old=by[ticker]
    spot=old['quote']['price']
    result={'ticker':ticker,'collected_at':collected,'reference_close':spot,'price_date':str(ASOF),'expiry':EXPIRY}
    obj=yf.Ticker(ticker)
    try:
        info=obj.info
        (RAW/(ticker+'_info.json')).write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
        fields=['symbol','shortName','longName','currency','financialCurrency','quoteType','exchange','regularMarketPrice','regularMarketTime','trailingPE','forwardPE','trailingEps','forwardEps','sharesOutstanding','marketCap']
        result['quote']={k:info.get(k) for k in fields}
    except Exception as ex:result['quote_error']=str(ex)
    try:
        expiries=list(obj.options)
        result['available_expiries']=expiries
        if EXPIRY not in expiries:
            result['iv_percent']=None
            result['iv_missing_reason']='No listed option chain for the common expiry from source.'
        else:
            chain=obj.option_chain(EXPIRY)
            calls=json.loads(chain.calls.to_json(orient='records',date_format='iso'))
            puts=json.loads(chain.puts.to_json(orient='records',date_format='iso'))
            raw={'ticker':ticker,'collected_at':collected,'expiry':EXPIRY,'reference_close':spot,'underlying':chain.underlying,'calls':calls,'puts':puts}
            p=RAW/(ticker+'_options.json')
            p.write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf-8')
            result['raw_option_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
            good=[c for c in calls if clean_call(c,spot)]
            result['clean_call_count']=len(good)
            if good:
                c=min(good,key=lambda x:(abs(x['strike']-spot),-(x.get('openInterest') or 0)-(x.get('volume') or 0)))
                result['call']=c
                result['iv_percent']=100*c['impliedVolatility']
                result['strike_distance_percent']=100*abs(c['strike']/spot-1)
                result['relative_spread_percent']=100*(c['ask']-c['bid'])/((c['ask']+c['bid'])/2)
            else:
                result['iv_percent']=None
                result['iv_missing_reason']='No near-ATM call passes quality filters.'
    except Exception as ex:
        result['iv_percent']=None
        result['iv_missing_reason']=str(ex)
    result['options_source_url']='https://finance.yahoo.com/quote/'+ticker+'/options/?date=1792108800'
    return result

results={}
with ThreadPoolExecutor(max_workers=4) as pool:
    futures={pool.submit(get,t):t for t in SELECTED}
    for f in as_completed(futures):
        ticker=futures[f]
        try:r=f.result()
        except Exception as ex:r={'ticker':ticker,'iv_percent':None,'error':str(ex)}
        results[ticker]=r
        q=r.get('quote',{})
        print(ticker,'close',q.get('regularMarketPrice'),'PE',q.get('trailingPE'),'FPE',q.get('forwardPE'),'IV',r.get('iv_percent'),r.get('iv_missing_reason',''),flush=True)

payload={'asof':str(ASOF),'expiry':EXPIRY,'dte_calendar':(date.fromisoformat(EXPIRY)-ASOF).days,'selected':SELECTED,
 'collected_completed_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),
 'iv_definition':'Same 2026-10-16 expiry, closest eligible near-ATM call source IV, annualized. Not call/put mean. Quote-update timestamps unavailable; collection time and last trade timestamp are distinct.',
 'quality':'strike within 5%; positive valid bid/ask; relative spread <=30%; volume+open interest >=1; source IV 1%-300%; last trade age <=7 calendar days.',
 'results':[results[t] for t in SELECTED]}
(OUT/'最新行情及IV.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',payload['collected_completed_at'],flush=True)
