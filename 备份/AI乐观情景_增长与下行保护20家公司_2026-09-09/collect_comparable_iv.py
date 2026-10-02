from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from zoneinfo import ZoneInfo
import yfinance as yf
import json, math, sys

sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).parent
ROOT=Path(r'D:\drive\Investment')
RAW=OUT/'原始期权链'
RAW.mkdir(exist_ok=True)
ASOF=date(2026,9,9)
EXPIRY='2026-10-16'
SELECTED=['MU','ADBE','MSFT','NVDA','META','BABA','GOOGL','AMZN','ASML','TSM','AVGO','ET','SNDK','APH','TEL','JBL','NTAP','IBM','SMCI','BDC']
market=json.loads((ROOT/'备份/20家公司投资价值与多维图谱_2026-09-09/market_scenario_data.json').read_text(encoding='utf-8'))
by_ticker={d['ticker']:d for d in market['companies']}

def get(ticker):
    retrieved=datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()
    t=yf.Ticker(ticker)
    expiries=list(t.options)
    if EXPIRY not in expiries:raise ValueError('common expiry unavailable: '+str(expiries))
    chain=t.option_chain(EXPIRY)
    calls=json.loads(chain.calls.to_json(orient='records',date_format='iso'))
    puts=json.loads(chain.puts.to_json(orient='records',date_format='iso'))
    price=by_ticker[ticker]['quote']['price']
    raw={'ticker':ticker,'expiry':EXPIRY,'collected_at':retrieved,'underlying_reference_close':price,'underlying':chain.underlying,'calls':calls,'puts':puts}
    (RAW/(ticker+'.json')).write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf-8')
    def quality(r):
        k=r.get('strike');iv=r.get('impliedVolatility');bid=r.get('bid');ask=r.get('ask')
        if any(v is None or not math.isfinite(v) for v in [k,iv,bid,ask]):return False
        if not (0.01<=iv<=3 and bid>0 and ask>=bid):return False
        if abs(k/price-1)>.05:return False
        if (ask-bid)/((bid+ask)/2)>.30:return False
        if (r.get('openInterest') or 0)+(r.get('volume') or 0)<1:return False
        trade=r.get('lastTradeDate')
        if not trade:return False
        trade_date=datetime.fromisoformat(trade.replace('Z','+00:00')).astimezone(ZoneInfo('America/New_York')).date()
        return 0<=(ASOF-trade_date).days<=7
    clean_calls={r['strike']:r for r in calls if quality(r)}
    clean_puts={r['strike']:r for r in puts if quality(r)}
    paired=set(clean_calls)&set(clean_puts)
    if not paired:
        return {'ticker':ticker,'expiry':EXPIRY,'collected_at':retrieved,'iv_percent':None,'reason':'No same-strike call/put pair within 5% of close passes positive bid/ask, <=30% spread, positive volume/OI and <=7-day trade freshness.','clean_call_strikes':list(clean_calls),'clean_put_strikes':list(clean_puts)}
    strike=min(paired,key=lambda k:(abs(k-price),-sum((r.get('openInterest') or 0)+(r.get('volume') or 0) for r in [clean_calls[k],clean_puts[k]])))
    c,p=clean_calls[strike],clean_puts[strike]
    return {'ticker':ticker,'expiry':EXPIRY,'dte_calendar':(date.fromisoformat(EXPIRY)-ASOF).days,'collected_at':retrieved,'reference_close':price,'strike':strike,'moneyness_distance_percent':100*abs(strike/price-1),'iv_percent':50*(c['impliedVolatility']+p['impliedVolatility']),'call_iv_percent':100*c['impliedVolatility'],'put_iv_percent':100*p['impliedVolatility'],'call':c,'put':p,'source':'Yahoo Finance options source impliedVolatility via yfinance; arithmetic mean of same-strike call/put source IV, not an option price or a VIX-style index.','source_url':'https://finance.yahoo.com/quote/'+ticker+'/options/?date=1792108800','bid_ask_timestamp':'not supplied; lastTradeDate is a trade timestamp, not quote timestamp'}

result={}
with ThreadPoolExecutor(max_workers=4) as executor:
    futures={executor.submit(get,t):t for t in SELECTED}
    for f in as_completed(futures):
        ticker=futures[f]
        try:result[ticker]=f.result()
        except Exception as exc:result[ticker]={'ticker':ticker,'iv_percent':None,'reason':str(exc)}
        r=result[ticker]
        print(ticker, None if r['iv_percent'] is None else round(r['iv_percent'],2),'K',r.get('strike'),'call',r.get('call_iv_percent'),'put',r.get('put_iv_percent'),r.get('reason',''),flush=True)
payload={'asof_market_date':str(ASOF),'expiry':EXPIRY,'dte_calendar':(date.fromisoformat(EXPIRY)-ASOF).days,'selected':SELECTED,'collected_completed_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'method':'Source IV, annualized. Same expiry and strike; closest clean ATM pair within 5% of underlying close, bid/ask positive, relative spread <=30%, volume+OI >=1, trade age <=7 calendar days. Arithmetic mean of call and put IV. No historical-volatility substitution or stale-snapshot fallback. Bid/ask update timestamps not supplied by provider.','results':[result[t] for t in SELECTED]}
(OUT/'latest_comparable_iv.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
