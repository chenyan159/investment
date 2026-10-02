from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import re,json,pandas as pd,numpy as np
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';PROJ=ROOT.parents[1]
p=pd.read_csv(D/'daily_prices.csv').set_index(['symbol','date']);u=pd.read_csv(D/'universe.csv');rows=[]
events={}
for sym in u.ticker:
    j=json.loads((D/'price_raw'/f'{sym}.json').read_text(encoding='utf-8'))['data']['chart']['result'][0]
    events[sym]=[(datetime.fromtimestamp(e['date'],ZoneInfo(j['meta']['exchangeTimezoneName'])).date().isoformat(),e['numerator']/e['denominator']) for e in j.get('events',{}).get('splits',{}).values()]
for f in sorted((PROJ/'金融资料/每日金融数据').glob('每日金融数据_2026-*.md')):
    fd=f.stem[-10:]
    if not '2026-07-10'<=fd<='2026-09-04':continue
    for ln,line in enumerate(f.read_text(encoding='utf-8-sig').splitlines(),1):
        z=[s.strip() for s in line.strip().strip('|').split('|')]
        if len(z)<4 or z[0] not in set(u.ticker) or not re.fullmatch(r'2026-\d\d-\d\d',z[2]):continue
        sym,date=z[0],z[2]
        try:nominal=float(z[3].replace(',','').replace('$',''))
        except:continue
        factor=np.prod([r for d,r in events[sym] if date<d<='2026-09-04'])
        split_close=nominal/factor
        try:vendor=float(p.loc[(sym,date),'close'])
        except:vendor=np.nan
        rel=split_close/vendor-1 if vendor>0 else np.nan
        rows.append(dict(ticker=sym,snapshot_date=fd,price_date=date,snapshot_nominal_close=nominal,subsequent_split_factor=factor,snapshot_split_adjusted_close=split_close,yahoo_historical_close=vendor,relative_difference=rel,source_path=str(f),source_line=ln))
df=pd.DataFrame(rows);df.to_csv(D/'price_snapshot_crosscheck.csv',index=False,encoding='utf-8-sig')
end=df[df.snapshot_date=='2026-09-04'];print('ALL',len(df),'matched',df.relative_difference.notna().sum(),'over1pct',(df.relative_difference.abs()>.01).sum(),'over0.1pct',(df.relative_difference.abs()>.001).sum())
print('END',len(end),'over0.1pct',(end.relative_difference.abs()>.001).sum());print(df[df.relative_difference.abs()>.01].head(35).to_string(index=False))
print('END EXCEPTIONS',end[end.relative_difference.abs()>.001].to_string(index=False))
