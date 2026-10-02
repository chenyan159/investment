from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from io import StringIO
import requests,pandas as pd,json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';RAW=D/'secondary_price_raw';RAW.mkdir(exist_ok=True)
c=pd.read_csv(D/'company_returns.csv');p=pd.read_csv(D/'daily_prices.csv').set_index(['symbol','date'])
symbols=sorted(set(c.nlargest(20,'ret_0713').ticker)|set(c.nsmallest(20,'consensus_rank').ticker)|set(c.nsmallest(20,'ret_0713').ticker))
def check(sym):
    exchange=c.loc[c.ticker==sym,'exchange'].iloc[0]
    url=f'https://stockanalysis.com/quote/otc/{sym}/history/' if exchange in ['PNK','OQX','OQB'] else f'https://stockanalysis.com/stocks/{sym.lower()}/history/'
    path=RAW/f'{sym}.html'
    try:
        if not path.exists():
            r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=30);r.raise_for_status();path.write_text(r.text,encoding='utf-8')
        t=pd.read_html(StringIO(path.read_text(encoding='utf-8')))[0];rows=[]
        for _,x in t.iterrows():
            try:date=pd.to_datetime(x['Date']).date().isoformat();v=float(x['Close'])
            except:continue
            if '2026-07-13'<=date<='2026-09-04' and (sym,date) in p.index:
                y=float(p.loc[(sym,date),'close']);rows.append(dict(ticker=sym,date=date,secondary_close=v,yahoo_close=y,relative_difference=v/y-1,url=url,raw_path=str(path)))
        return rows,dict(ticker=sym,status='ok',rows=len(rows),url=url)
    except Exception as e:return [],dict(ticker=sym,status='error',error=str(e),url=url)
rows=[];meta=[]
with ThreadPoolExecutor(max_workers=6) as ex:
    for f in as_completed([ex.submit(check,s) for s in symbols]):
        rr,mm=f.result();rows.extend(rr);meta.append(mm)
df=pd.DataFrame(rows);df.to_csv(D/'secondary_price_crosscheck.csv',index=False,encoding='utf-8-sig');pd.DataFrame(meta).to_csv(D/'secondary_price_manifest.csv',index=False,encoding='utf-8-sig')
print('DONE',len(symbols),'SYMBOLS',len(df),'ROWS',len([m for m in meta if m['status']=='error']),'ERRORS')
print('EXCEPTIONS',df[df.relative_difference.abs()>.001].to_string(index=False))
print('META_ERRORS',[m for m in meta if m['status']=='error'])
