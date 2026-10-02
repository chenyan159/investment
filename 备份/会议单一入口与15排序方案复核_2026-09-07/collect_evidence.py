from pathlib import Path
from decimal import Decimal
import csv,hashlib,json,math,statistics,shutil

ROOT=Path('D:/drive/Investment');OUT=Path(__file__).parent;SORT=ROOT/'分析报告/公司排序';BASE=ROOT/'基本面/行业调研/研究方法'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
plans=[r for r in read(SORT/'00_待运行研究方案注册表.csv') if r['prompt_file']]
assert len(plans)==15
historical=read(SORT/'00_运行与榜单注册表.csv')
metrics={r['list_id']:r for r in read(ROOT/'备份/流程审计与研究方案改进_2026-09-05/data/sorting_top30_metrics.csv')}
co=read(ROOT/'备份/项目反思_2026-09-04/data/company_returns.csv')
prices={(r['symbol'],r['date']):r for r in read(ROOT/'备份/项目反思_2026-09-04/data/daily_prices.csv')}
companies={r['ticker']:r for r in co}
def ret(t,opening=False):
    d='2026-07-14' if opening else '2026-07-13';r=prices[t,d]
    a=Decimal(r['adj_close'])
    if opening:a*=Decimal(r['open'])/Decimal(r['close'])
    e=prices[t,companies.get(t,{}).get('end_date','2026-09-04')]
    return Decimal(e['adj_close'])/a-1
def corr(a,b):
    ax=statistics.mean(a);bx=statistics.mean(b)
    return sum((x-ax)*(y-bx) for x,y in zip(a,b))/math.sqrt(sum((x-ax)**2 for x in a)*sum((y-bx)**2 for y in b))
sets={k:set(v['top30_tickers'].split(',')) for k,v in metrics.items()}
winners={r['ticker'] for r in sorted(co,key=lambda x:float(x['ret_0713']),reverse=True)[:30]}
pairs=[]
for a,b in [('01','N01'),('01','04'),('04','N01'),('07','N04'),('03','05'),('03','N02'),('05','N02'),('08','N02'),('09','06G'),('09','06E'),('N03','06E'),('N05','01'),('N05','04'),('N06','06G')]:
    x=[float(r['rank_'+a]) for r in co];y=[float(r['rank_'+b]) for r in co]
    pairs.append({'a':a,'b':b,'rank_correlation':corr(x,y),'top30_overlap':len(sets[a]&sets[b]),'union_size':len(sets[a]|sets[b]),
        'a_unique_winners':sorted((sets[a]-sets[b])&winners),'b_unique_winners':sorted((sets[b]-sets[a])&winners)})
rows=[]
for r in plans:
    p=ROOT/r['prompt_file'];assert sha(p)==r['sha256'],p
    assert not (ROOT/r['expected_output_file']).exists(),f'New result exists: {r["method_id"]}'
    old=[x for x in historical if x['method_id']==r['method_id']]
    for o in old:
        m=metrics[o['list_id']]
        for field,opening in [('top30_return',False),('top30_next_open_return',True)]:
            v=sum((ret(t,opening) for t in sets[o['list_id']]),Decimal(0))/30
            assert abs(v-Decimal(m[field]))<Decimal('1e-12')
        rows.append({**r,**{k:m[k] for k in ['list_id','top30_return','top30_next_open_return','rank_ic','top30_actual_winner30','top30_positive','top30_median']},
            'old_plan':(SORT/o['plan_path']).as_posix(),'old_result':(SORT/o['result_path']).as_posix(),'old_version':o['run_id']})
qualified=['MU','PENG','TSLA','TT','ASX','APLD','BWXT','BDC']
evidence={'window':'2026-07-13 close / 2026-07-14 adjusted open to 2026-09-04 latest available adjusted close',
    'ranking_views':rows,'pairs':pairs,'benchmarks':{t:{'close':str(ret(t)),'open':str(ret(t,True))} for t in ['SPY','QQQ','SOXX']},
    'pool':{'close':str(sum((ret(t) for t in companies),Decimal(0))/len(companies)),'open':str(sum((ret(t,True) for t in companies),Decimal(0))/len(companies))},
    'N03_qualified8':{'tickers':qualified,'close':str(sum((ret(t) for t in qualified),Decimal(0))/8),'open':str(sum((ret(t,True) for t in qualified),Decimal(0))/8)},
    'new_versions_have_results':False,'company_count':len(companies),'stale_endpoint':[{'ticker':r['ticker'],'date':r['end_date']} for r in co if r['end_date']!='2026-09-04']}
(OUT/'排序证据.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')

manifest=OUT/'修改前快照.json'
if not manifest.exists():
    editable=[BASE/'会议调研方案.md',BASE/'00_背景与会议研究入口.md',ROOT/'基本面/行业调研/AGENTS.md']
    for p in editable:
        d=OUT/'原文件'/p.relative_to(ROOT);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
    protected=[ROOT/r['prompt_file'] for r in plans]
    protected += [SORT/n for n in ['00_待运行研究方案注册表.csv','00_运行与榜单注册表.csv','00_站点发布策略.csv','00_方案状态总表.csv','00_当前评估.json','站点数据/current.json']]
    protected += [p for p in (ROOT/'备份/24家公司最新投资价值多情景评估_2026-08-19').rglob('*') if p.is_file()]
    withdrawn=[p for p in (BASE/'会议').rglob('*') if p.is_file()]
    payload={k:[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in ps] for k,ps in [('editable',editable),('protected',protected),('withdrawn',withdrawn)]}
    manifest.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'plans':len(plans),'views':len(rows),'pairs':pairs,'benchmarks':evidence['benchmarks'],'pool':evidence['pool'],'N03_qualified8':evidence['N03_qualified8']},ensure_ascii=False,indent=2))
