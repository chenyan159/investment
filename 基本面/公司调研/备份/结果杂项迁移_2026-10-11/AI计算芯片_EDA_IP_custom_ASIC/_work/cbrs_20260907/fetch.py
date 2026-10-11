from pathlib import Path
import requests,bs4,concurrent.futures
root=Path(__file__).parent
sources={
'q2':'https://investors.cerebras.ai/node/7301/html',
'q1':'https://www.sec.gov/Archives/edgar/data/2021728/000162828026044981/cbrs-20260331.htm',
'release2':'https://cerebras.gcs-web.com/news-releases/news-release-details/cerebras-systems-fast-inference-cloud-business-nearly-quadruples',
'release1':'https://investors.cerebras.ai/news-releases/news-release-details/cerebras-systems-announces-strong-first-quarter-2026-results',
'ipo':'https://investors.cerebras.ai/static-files/0264993f-99b7-4dfb-9e7a-2a7a4fbddd46',
}
def fetch(k,u):
 r=requests.get(u,timeout=60);r.raise_for_status()
 if r.content.startswith(b'%PDF'):
  import pymupdf
  d=pymupdf.open(stream=r.content,filetype='pdf');t='\n'.join('PAGE '+str(i+1)+'\n'+p.get_text() for i,p in enumerate(d))
 else:
  s=bs4.BeautifulSoup(r.text,'html.parser')
  for e in s.find_all(['script','style','ix:header','ix:hidden']):e.decompose()
  t=s.get_text(' ',strip=True)
  # Preserve table structure separately.
  tables='\n\n'.join('TABLE '+str(i)+'\n'+'\n'.join(' | '.join(c.get_text(' ',strip=True) for c in row.find_all(['td','th'])) for row in tab.find_all('tr')) for i,tab in enumerate(s.find_all('table')))
  (root/(k+'_tables.txt')).write_text(tables,encoding='utf-8')
 (root/(k+'.txt')).write_text(t,encoding='utf-8')
 return k,len(t)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for f in [ex.submit(fetch,k,u) for k,u in sources.items()]:
  try:print(f.result())
  except Exception as e:print(type(e).__name__,str(e))
