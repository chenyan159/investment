import json,re,time,hashlib,concurrent.futures,collections
from pathlib import Path
import requests

ROOT=Path(__file__).parent
inv=json.loads((ROOT/'report_inventory.json').read_text(encoding='utf-8'))
tickers=json.loads((ROOT/'sec_company_tickers.json').read_text(encoding='utf-8'))
mapping={v['ticker'].upper():v for v in tickers.values()}
HEADERS={'User-Agent':'Investment research audit research@example.com','Accept-Encoding':'gzip, deflate'}
cache=ROOT/'sec_submissions';cache.mkdir(exist_ok=True)

def get(cik):
    p=cache/f'{int(cik):010d}.json'
    if p.exists():return json.loads(p.read_text(encoding='utf-8'))
    time.sleep(.3)
    url=f'https://data.sec.gov/submissions/CIK{int(cik):010d}.json'
    resp=requests.get(url,headers=HEADERS,timeout=30)
    resp.raise_for_status()
    p.write_text(resp.text,encoding='utf-8')
    return resp.json()

def scan(c):
    out={k:c[k] for k in ['symbol','name','category','report_date','path','sha256']}
    txt=Path(c['path']).read_text(encoding='utf-8-sig')
    out['characters']=len(txt)
    out['date_header_match']=c['report_date'] in '\n'.join(txt.splitlines()[:12])
    out['short_term_mentions']=len(re.findall(r'下一季|下一季度|未来.?季|季度预测|短期|近期|FY27Q1|FY2027Q1|2027.?Q1',txt,re.I))
    out['forecast_heading_lines']=[{'line':i+1,'text':s} for i,s in enumerate(txt.splitlines()) if s.startswith('#') and re.search('预测|展望|未来|待验证|观察|跟踪',s)]
    try:
        v=mapping.get(c['symbol'])
        if v:
            cik=v['cik_str']; sub=get(cik)
        else:
            sub=None
            for cik0 in c.get('sec_links',[]):
                cand=get(cik0)
                if c['symbol'] in [s.upper() for s in cand.get('tickers',[])]:
                    cik=int(cik0);sub=cand;break
            if sub is None:
                out.update(status='no_verified_sec_ticker_match',filings=[])
                return out
        out['cik']=int(cik);out['sec_name']=sub.get('name');out['sec_tickers']=sub.get('tickers')
        recent=sub['filings']['recent'];rows=[]
        for i,day in enumerate(recent.get('filingDate',[])):
            if day<c['report_date'] or day>'2026-09-30':continue
            row={k:recent[k][i] for k in ['filingDate','reportDate','form','accessionNumber','primaryDocument','items'] if k in recent}
            row['url']=f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{row['accessionNumber'].replace('-','')}/{row['primaryDocument']}"
            row['after_report']=day>c['report_date']
            row['potential_earnings']=row['form'] in ['10-Q','10-K','10-Q/A','10-K/A','20-F','20-F/A','6-K'] or ('2.02' in row.get('items',''))
            rows.append(row)
        out['filings']=rows
        out['earnings_candidates']=[r for r in rows if r['potential_earnings'] and r['after_report']]
        out['same_day_candidates']=[r for r in rows if r['potential_earnings'] and not r['after_report']]
        out['status']='sec_checked'
    except Exception as e:
        out.update(status='error',error=str(e))
    return out

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(scan,inv['companies']))
    result={'cutoff_utc':inv['cutoff_utc'],'cutoff_local':inv['cutoff_local'],'method':'Verified ticker to CIK; recent SEC filings after report date through 2026-09-30; candidates are not automatically new earnings. Company reports read in full by parser.','companies':rows}
    (ROOT/'sec_scan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('STATUS',dict(collections.Counter(r['status'] for r in rows)))
    print('HEADERS',dict(collections.Counter(r['date_header_match'] for r in rows)))
    for r in rows:
        if r.get('earnings_candidates') or r['status']!='sec_checked' or r.get('same_day_candidates'):
            print(r['symbol'],r['report_date'],r['status'],'AFTER',[(x['filingDate'],x['form'],x.get('items'),x['primaryDocument']) for x in r.get('earnings_candidates',[])],'SAME',[(x['filingDate'],x['form']) for x in r.get('same_day_candidates',[])])
