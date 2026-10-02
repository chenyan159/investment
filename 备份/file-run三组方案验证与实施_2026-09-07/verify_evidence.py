from pathlib import Path
import csv, hashlib, json, statistics
from decimal import Decimal

ROOT = Path('D:/drive/Investment')
OUT = Path(__file__).parent
OLD = ROOT/'备份/项目反思_2026-09-04/data'
AUD = ROOT/'备份/流程审计与研究方案改进_2026-09-05/data'
def rows(p):
    return list(csv.DictReader(p.open(encoding='utf-8-sig')))
prices = {(r['symbol'],r['date']):r for r in rows(OLD/'daily_prices.csv')}
co = {r['ticker']:r for r in rows(OLD/'company_returns.csv')}
def ret(t,d,opening=False):
    s=prices[t,d]; e=prices[t,co.get(t,{}).get('end_date','2026-09-04')]
    a=Decimal(s['adj_close'])
    if opening: a*=Decimal(s['open'])/Decimal(s['close'])
    return Decimal(e['adj_close'])/a-1

check=[]
for t in co:
    a=ret(t,'2026-07-13')
    assert abs(a-Decimal(co[t]['ret_0713']))<Decimal('0.000000000001')
    check.append({'ticker':t,'return':str(a)})
metrics=[]
for m in rows(AUD/'sorting_top30_metrics.csv'):
    ts=m['top30_tickers'].split(','); assert len(ts)==len(set(ts))==30
    for field,day,opening in [('top30_return','2026-07-13',False),('top30_next_open_return','2026-07-14',True)]:
        value=sum((ret(t,day,opening) for t in ts),Decimal(0))/30
        assert abs(value-Decimal(m[field]))<Decimal('0.000000000001')
    metrics.append({'list':m['list_id'],'close_return':m['top30_return'],'next_open_return':m['top30_next_open_return']})
sha=[]
for r in rows(AUD/'sorting_current_inventory.csv'):
    p=Path(r['plan_path']); v=hashlib.sha256(p.read_bytes()).hexdigest()
    assert v==r['plan_sha256'], str(p)
    sha.append({'method':r['method_id'],'unchanged_since_audit':True})
conference=[]
for r in rows(ROOT/'备份/file-run两类流程改造讨论_2026-09-05/data/会议映射公司后续观察_非建议回测.csv'):
    if r['ret']:
        v=ret(r['ticker'],'2026-08-19',True)
        assert abs(v-Decimal(r['ret']))<Decimal('0.000000000001')
        conference.append({'conference':r['conference'],'ticker':r['ticker'],'return':str(v)})
out={'date':'2026-09-07','price_cutoff':'2026-09-04','universe_checks':len(check),'ranking_metric_checks':len(metrics)*2,
     'unchanged_sorting_plans':sha,'focus':{t:{'return':str(ret(t,'2026-07-13')),'rank03':co[t]['rank_03'],'rank05':co[t]['rank_05'],'rank15':co[t]['rank_15']} for t in ['PENG','SMCI','MOD','P','SOMMY','DELL','HPE']},
     'metrics':metrics,'conference_checks':conference,
     'calendar_source':'https://www.nasdaqtrader.com/TraderNews.aspx?id=ETS2026-47',
     'limitations':['July window is 39 return intervals, below 3 months.','Same frozen vendor history was recomputed, not newly acquired independent prices.','Conference mappings are purposive observations, not recommendation or causal backtests.']}
sort=ROOT/'分析报告/公司排序'
current=rows(sort/'00_运行与榜单注册表.csv')
def ranking(mid):
    r=next(x for x in current if x['method_id']==mid); p=sort/r['result_path']; found={}
    for line,text in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
        v=[c.strip() for c in text.strip().strip('|').split('|')]
        if len(v)>4 and v[0].isdigit() and v[1] in co:
            found[v[1]]={'line':line,'fields':v,'path':p.relative_to(ROOT).as_posix()}
    return found
peng=ranking('03')['PENG'];v=peng['fields']
assert v[0]=='1' and Decimal(v[3])==Decimal('83.9')
assert Decimal(v[3])==Decimal(50)+Decimal(v[6])+Decimal(v[7])-sum((Decimal(z) for z in v[8:13]),Decimal(0))
mod=ranking('02')['MOD'];v=mod['fields'];assert v[0]=='17' and v[7]=='95' and v[8]=='25'
n03=ranking('N03');same52=[t for t,r in n03.items() if Decimal(r['fields'][3])==52]
assert len(n03)==192 and len(same52)==148
out['original_report_checks']={'PENG03':peng,'MOD02':mod,'N03_same52_count':len(same52),'N03_qualified_count':8}
out['stale_endpoints']=[{'ticker':t,'actual_end_date':r['end_date']} for t,r in co.items() if r['end_date']!='2026-09-04']
(OUT/'回测重新核验.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print({'company_returns':len(check),'ranking_metrics':len(metrics)*2,'plan_hashes':len(sha),'conference_returns':len(conference)})
