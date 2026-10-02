from pathlib import Path
from datetime import datetime, date, timezone
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, math, sys, time
import yfinance as yf
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
OUT.joinpath('市场原始核验').mkdir(exist_ok=True)
local=json.loads((OUT/'候选公司本地证据.json').read_text(encoding='utf-8'))
symbols=sys.argv[1:] or list(local)
cutoff=date(2026,9,9)
capture=datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()
def clean(v):
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,list):return [clean(x) for x in v]
    if isinstance(v,tuple):return [clean(x) for x in v]
    if hasattr(v,'isoformat'):return v.isoformat()
    if hasattr(v,'item'):return clean(v.item())
    if isinstance(v,float) and not math.isfinite(v):return None
    return v
def fetch(sym):
    p=OUT/'市场原始核验'/f'{sym}.json'
    if p.exists():return json.loads(p.read_text(encoding='utf-8'))
    t=yf.Ticker(sym)
    r={'ticker':sym,'retrieved_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),
       'price_cutoff':str(cutoff),'history_url':f'https://finance.yahoo.com/quote/{sym}/history/',
       'statistics_url':f'https://finance.yahoo.com/quote/{sym}/key-statistics/',
       'options_url':f'https://finance.yahoo.com/quote/{sym}/options/','errors':[]}
    try:
        h=t.history(start='2026-06-02',end='2026-09-10',auto_adjust=False,actions=True,raise_errors=True)
        r['history']=[clean(dict(date=idx,**row.to_dict())) for idx,row in h.iterrows()]
        start=h[[x.date()<=date(2026,6,9) for x in h.index]].iloc[-1]
        end=h[[x.date()<=cutoff for x in h.index]].iloc[-1]
        r['return_3m']={'start':str(start.name.date()),'end':str(end.name.date()),
            'start_close':float(start.Close),'end_close':float(end.Close),
            'start_adjclose':float(start['Adj Close']),'end_adjclose':float(end['Adj Close']),
            'price_change_pct':(float(end.Close)/float(start.Close)-1)*100,
            'adjusted_change_pct':(float(end['Adj Close'])/float(start['Adj Close'])-1)*100}
    except Exception as e:r['errors'].append('history: '+str(e))
    try:
        info=t.info
        r['quote']={k:clean(info.get(k)) for k in ['symbol','shortName','currency','financialCurrency','regularMarketPrice','regularMarketTime','currentPrice','marketCap','sharesOutstanding','trailingPE','forwardPE','trailingEps','forwardEps','targetMeanPrice','targetHighPrice','numberOfAnalystOpinions']}
    except Exception as e:r['errors'].append('info: '+str(e))
    try:
        expiries=t.options
        r['available_expirations']=list(expiries)
        ranked=sorted([(abs((date.fromisoformat(e)-cutoff).days-30),e) for e in expiries if 20 <= (date.fromisoformat(e)-cutoff).days <=45])
        spot=r.get('return_3m',{}).get('end_close') or r.get('quote',{}).get('regularMarketPrice')
        r['option_chains']=[]
        best=None
        for _,expiry in ranked[:3]:
            chain=t.option_chain(expiry)
            raw={'expiry':expiry,'underlying':clean(chain.underlying),'calls':clean(chain.calls.to_dict('records')),'puts':clean(chain.puts.to_dict('records'))}
            r['option_chains'].append(raw)
            chosen={}
            for side in ['calls','puts']:
                viable=[]
                for row in raw[side]:
                    bid,ask,iv,k=[row.get(f) for f in ['bid','ask','impliedVolatility','strike']]
                    if not all(isinstance(v,(int,float)) for v in [bid,ask,iv,k]):continue
                    if not (bid>0 and ask>=bid and .01<iv<5 and abs(k/spot-1)<=.05):continue
                    mid=(bid+ask)/2
                    if (ask-bid)/mid>.40:continue
                    if (row.get('openInterest') or 0)+(row.get('volume') or 0)<=0:continue
                    viable.append(row|{'moneyness_distance':abs(k/spot-1),'relative_spread':(ask-bid)/mid})
                if viable:
                    chosen[side]=sorted(viable,key=lambda x:(x['moneyness_distance'],x['relative_spread']))[0]
            if len(chosen)==2:
                best={'expiration':expiry,'dte_from_close':(date.fromisoformat(expiry)-cutoff).days,'spot':spot,**chosen,
                    'mean_iv_pct':50*(chosen['calls']['impliedVolatility']+chosen['puts']['impliedVolatility'])}
                break
        r['selected_iv']=best
        if not best:r['errors'].append('No clean call-and-put ATM pair within 20-45 DTE and 5% moneyness; not set to zero.')
    except Exception as e:r['errors'].append('options: '+str(e))
    p.write_text(json.dumps(clean(r),ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    return r
results={}
with ThreadPoolExecutor(max_workers=4) as pool:
    jobs={pool.submit(fetch,s):s for s in symbols}
    for f in as_completed(jobs):
        sym=jobs[f]
        try:
            r=f.result();results[sym]=r
            print(sym,'price',r.get('return_3m',{}).get('end_close'),'3m',round(r.get('return_3m',{}).get('price_change_pct',float('nan')),2),'IV',round((r.get('selected_iv') or {}).get('mean_iv_pct',float('nan')),2),'errors',r['errors'],flush=True)
        except Exception as e:print(sym,'FAILED',repr(e),flush=True)
(OUT/'最新市场数据汇总.json').write_text(json.dumps(clean(results),ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
print('COMPLETE',len(results),flush=True)
