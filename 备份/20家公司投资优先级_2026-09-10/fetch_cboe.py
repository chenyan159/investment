from pathlib import Path
from datetime import datetime,date
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor,as_completed
import requests,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
market=json.loads((OUT/'最新市场数据汇总.json').read_text(encoding='utf-8'))
symbols=sys.argv[1:] or 'ADBE MU ET MSFT PNR BABA SMCI ST TEL DOV ASML META DKILY AEP ALLE BDC NVDA SNDK TSM AVGO'.split()
end=date(2026,9,9)
def run(sym):
    url=f'https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json'
    rawp=OUT/'市场原始核验'/f'{sym}_cboe.json'
    retrieved=datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()
    if rawp.exists():x=json.loads(rawp.read_text(encoding='utf-8'))
    else:
        res=requests.get(url,timeout=30)
        if not res.ok:return {'ticker':sym,'url':url,'retrieved_at':retrieved,'error':str(res.status_code)}
        x=res.json();rawp.write_text(json.dumps(x,ensure_ascii=False),encoding='utf-8')
    spot=market[sym]['return_3m']['end_close']
    options=x['data']['options']; viable={}
    for o in options:
        m=re.search(r'(\d{6})([CP])(\d{8})$',o['option'])
        if not m:continue
        e=datetime.strptime(m[1],'%y%m%d').date();dte=(e-end).days;k=int(m[3])/1000
        bid,ask,iv=[o.get(z) for z in ['bid','ask','iv']]
        if not (20<=dte<=45 and abs(k/spot-1)<=.05):continue
        if not all(isinstance(z,(int,float)) for z in [bid,ask,iv]):continue
        if not (bid>0 and ask>=bid and .01<iv<5):continue
        spread=(ask-bid)/((ask+bid)/2)
        if spread>.4 or o.get('open_interest',0)+o.get('volume',0)<=0:continue
        viable.setdefault(str(e),{}).setdefault(m[2],[]).append(o|{'strike':k,'distance':abs(k/spot-1),'spread':spread})
    selected=None
    for expiry in sorted(viable,key=lambda e:abs((date.fromisoformat(e)-end).days-30)):
        sides=viable[expiry]
        if not('C' in sides and 'P' in sides):continue
        c=min(sides['C'],key=lambda o:(o['distance'],o['spread']))
        p=min(sides['P'],key=lambda o:(o['distance'],o['spread']))
        selected={'expiry':expiry,'dte':(date.fromisoformat(expiry)-end).days,'call':c,'put':p,'iv_mean_pct':50*(c['iv']+p['iv'])}
        break
    return {'ticker':sym,'url':url,'retrieved_at':retrieved,'provider_timestamp_unzoned':x.get('timestamp'),'underlying':{k:v for k,v in x['data'].items() if k!='options'},'selected':selected,'number_of_contracts':len(options),'spot_for_selection':spot}
out={}
with ThreadPoolExecutor(max_workers=4) as pool:
    jobs={pool.submit(run,s):s for s in symbols}
    for f in as_completed(jobs):
        s=jobs[f]
        try:r=f.result()
        except Exception as e:r={'ticker':s,'error':str(e)}
        out[s]=r
        v=r.get('selected') or {}
        print(s,'IV',v.get('iv_mean_pct'),'expiry',v.get('expiry'),'asof',r.get('provider_timestamp_unzoned'),'error',r.get('error'),flush=True)
(OUT/'Cboe期权IV核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
