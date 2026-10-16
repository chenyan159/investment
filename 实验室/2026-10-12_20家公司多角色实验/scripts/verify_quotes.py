import concurrent.futures, datetime, json, sys, urllib.request
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp/quote_pages';OUT.mkdir(parents=True,exist_ok=True)
class Rows(HTMLParser):
    def __init__(self): super().__init__();self.rows=[];self.row=None;self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr':self.row=[]
        if tag in ('td','th') and self.row is not None:self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ('td','th') and self.cell is not None:
            self.row.append(''.join(self.cell).strip());self.cell=None
        if tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
def check(t):
    url=f'https://stockanalysis.com/stocks/{t.lower()}/history/'
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        raw=urllib.request.urlopen(req,timeout=12).read().decode('utf-8')
        (OUT/f'{t}.html').write_text(raw,encoding='utf-8')
        parser=Rows();parser.feed(raw)
        matches=[r for r in parser.rows if r and ('Oct 12, 2026' in r[0] or '2026-10-12' in r[0])]
        if not matches:return {'ticker':t,'url':url,'status':'date_not_found','sample_rows':parser.rows[:3]}
        row=matches[0]
        return {'ticker':t,'url':url,'status':'historical_close_row_read','price_date':'2026-10-12','currency':'USD','close':float(row[4].replace(',','')),'raw_row':row}
    except Exception as e:return {'ticker':t,'url':url,'status':'fetch_failed','error':str(e)}
symbols=sys.argv[1:] or ['ADBE','NVDA','PNR','MU']
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:records=list(ex.map(check,symbols))
path=ROOT/'04_verification/controller_quote_checks.json'
if path.exists():
    previous=json.loads(path.read_text(encoding='utf-8'))['records'];current={r['ticker']:r for r in previous}
else:current={}
for row in records:current[row['ticker']]=row
obj={'accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Public historical table, unadjusted close; no averaging with after-hours or differing ticks. HTTP failures are not successful checks.','records':list(current.values())}
path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
