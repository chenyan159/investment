import json,datetime,concurrent.futures,time
from pathlib import Path
import requests
ROOT=Path(__file__).parent
inv=json.loads((ROOT/'report_inventory.json').read_text(encoding='utf-8'))
universe={c['symbol']:c for c in inv['companies']}
start=datetime.date(2026,9,18);end=datetime.date(2026,9,30)
dates=[str(start+datetime.timedelta(days=i)) for i in range((end-start).days+1)]

def scan(day):
    path=ROOT/f'nasdaq_calendar_{day.replace("-","")}.json'
    url=f'https://api.nasdaq.com/api/calendar/earnings?date={day}'
    try:
        if path.exists():j=json.loads(path.read_text(encoding='utf-8'))
        else:
            time.sleep(.3)
            r=requests.get(url,headers={'User-Agent':'Mozilla/5.0','Accept':'application/json','Origin':'https://www.nasdaq.com'},timeout=25);r.raise_for_status();j=r.json()
            path.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8')
        data=j.get('data') or {};rows=data.get('rows') or []
        found=[{**r,'calendar_date':day,'report_date':universe[r['symbol']]['report_date'],'after_report':day>universe[r['symbol']]['report_date'],'source':url} for r in rows if r['symbol'] in universe]
        return {'day':day,'rows_count':len(rows),'matches':found,'source':url,'error':None}
    except Exception as e:return {'day':day,'error':str(e),'source':url,'matches':[]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(scan,dates))
(ROOT/'calendar_scan.json').write_text(json.dumps({'method':'Nasdaq calendar is discovery only; actual release must be confirmed with issuer source','days':rows},ensure_ascii=False,indent=2),encoding='utf-8')
for r in rows:print(r['day'],r.get('rows_count'),r['error'],[(x['symbol'],x['after_report']) for x in r['matches']])
