from pathlib import Path
import csv,json,re,hashlib,statistics,math
ROOT=Path('D:/drive/Investment'); OUT=Path(__file__).parent; (OUT/'data').mkdir(exist_ok=True)
OLD=ROOT/'备份/项目反思_2026-09-04/data'; AUD=ROOT/'备份/流程审计与研究方案改进_2026-09-05/data'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (OUT/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
prices={}
for r in read(OLD/'daily_prices.csv'):
    prices.setdefault(r['symbol'],{})[r['date']]={k:float(r[k]) if r[k] else None for k in ['open','high','low','close','adj_close']}
co=read(OLD/'company_returns.csv'); companies={r['ticker']:r for r in co}
master=ROOT/'备份/24家公司最新投资价值多情景评估_2026-08-19/05_24家公司综合排名与配置_2026-08-19.md'
txt=master.read_text(encoding='utf-8-sig'); sections={}; title=''
for n,l in enumerate(txt.splitlines(),1):
    if l.startswith('### '): title=l.strip('# ');sections[title]=[]
    m=re.match(r'^\|\s*(\d+)\s*\|\s*([A-Z][A-Z0-9.]*)\s*\|',l)
    if m and title:sections[title].append((int(m[1]),m[2],n))
rankings={k:v for k,v in sections.items() if len(v)==24 and (k.startswith('3.1') or k.startswith('4.'))}
assert len(rankings)==7,[(k,len(v)) for k,v in sections.items()]
mainrank=next(v for k,v in rankings.items() if k.startswith('3.1')); tickers=[t for _,t,_ in mainrank]
tiers={'核心候选':['EME','TEL','META'],'分批候选':['AMKR','NVT','HPE','MKSI'],'等待回撤或证据':['NVDA','CARR','CMI','AVGO','TSM','GEV','ANET','MU'],'仅投机小仓位':['CRDO','POWL','NBIS','BE'],'暂不投入新资金':['CRWV','STX','ALAB','LITE','WDC']}
assert set(sum(tiers.values(),[]))==set(tickers)
groups={'半导体计算制造':['AVGO','AMKR','NVDA','TSM','MKSI','MU','ALAB'],'网络互连连接器':['TEL','CRDO','LITE','ANET'],'云服务器存储':['HPE','META','STX','WDC','NBIS','CRWV'],'电力冷却工业':['CMI','CARR','EME','POWL','NVT','GEV','BE']}
thresholds={'EME':755,'TEL':194,'META':516.4,'AMKR':62.9,'HPE':49.5,'NVT':148,'MKSI':277.5}
def ret(t,date,opening=False):
    p=prices[t];s=p[date];e=p['2026-09-04'];start=s['open']*s['adj_close']/s['close'] if opening else s['adj_close'];return e['adj_close']/start-1
def corr(x,y):
    mx=statistics.mean(x);my=statistics.mean(y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
rows=[]
for rank,t,line in mainrank:
    p=prices[t]; dates=sorted(d for d in p if '2026-08-20'<=d<='2026-09-04')
    low=min(p[d]['low'] for d in dates);th=thresholds.get(t)
    rows.append({'ticker':t,'rank':rank,'source_line':line,'tier':next(k for k,v in tiers.items() if t in v),'group':next(k for k,v in groups.items() if t in v),'close_0819':p['2026-08-19']['close'],'open_0820':p['2026-08-20']['open'],'close_0904':p['2026-09-04']['close'],'ret_0819_close':ret(t,'2026-08-19'),'ret_0820_open':ret(t,'2026-08-20',True),'subsequent_sessions':len(dates),'min_low_after':low,'price_only_threshold':th,'first_daily_low_touch':next((d for d in dates if th and p[d]['low']<=th),''),'touch_is_trade':False})
write('专项24公司逐股回测.csv',rows)
agg=[]
for kind,sets in [('tier',tiers),('group',groups),('main_topk',{f'Top{k}':tickers[:k] for k in [3,5,7,10,24]})]:
    for name,ts in sets.items():
        agg.append({'type':kind,'name':name,'n':len(ts),'ret_0819_close':statistics.mean(ret(t,'2026-08-19') for t in ts),'ret_0820_open':statistics.mean(ret(t,'2026-08-20',True) for t in ts),'tickers':','.join(ts),'is_executable_portfolio':False})
for t in ['SPY','QQQ','SOXX']:
    agg.append({'type':'benchmark','name':t,'n':1,'ret_0819_close':ret(t,'2026-08-19'),'ret_0820_open':ret(t,'2026-08-20',True),'tickers':t,'is_executable_portfolio':False})
write('专项分层与分组回测.csv',agg)
method=[]
actual=sorted(tickers,key=lambda t:ret(t,'2026-08-20',True),reverse=True)
for name,rs in rankings.items():
    ts=[t for _,t,_ in rs];ys=[actual.index(t)+1 for t in ts]
    for k in [3,5,7,10,24]:
        method.append({'view':name,'k':k,'ret_0819_close':statistics.mean(ret(t,'2026-08-19') for t in ts[:k]),'ret_0820_open':statistics.mean(ret(t,'2026-08-20',True) for t in ts[:k]),'rank_ic_0820_open':corr(list(range(1,25)),ys),'tickers':','.join(ts[:k])})
write('专项七种视图回测.csv',method)
# Rankings: actual winners and losses within each frozen Top30; no re-optimized weight.
mt=read(AUD/'sorting_top30_metrics.csv'); contrib=[]
for r in mt:
    ts=r['top30_tickers'].split(',')
    for t in ts:
        v=float(companies[t]['ret_0713']);contrib.append({'list_id':r['list_id'],'ticker':t,'ret_0713':v,'equal_weight_contribution_pp':v/30*100,'original_rank':companies[t]['rank_'+r['list_id']]})
write('排序Top30逐股贡献.csv',contrib)
cs=[]
for r in mt:
    rr=sorted((z for z in contrib if z['list_id']==r['list_id']),key=lambda z:z['ret_0713'],reverse=True)
    cs.append({'list_id':r['list_id'],'best3':','.join(z['ticker'] for z in rr[:3]),'best3_contribution_pp':sum(z['equal_weight_contribution_pp'] for z in rr[:3]),'worst3':','.join(z['ticker'] for z in rr[-3:]),'worst3_contribution_pp':sum(z['equal_weight_contribution_pp'] for z in rr[-3:]),'top30_return':float(r['top30_return']),'return_excluding_best':statistics.mean(z['ret_0713'] for z in rr[1:])})
write('排序Top30收益集中度诊断.csv',cs)
focus=['P','SMCI','PENG','MOD','AEHR','SOMMY','MSFT','DELL','WDC','MU','STX','LITE','CRDO','HPE','EME','TEL','AMKR','META']
write('关键公司七月回测与28榜位置.csv',[{k:r[k] for k in ['ticker','company','ret_0713','ret_0715','consensus_rank']+[f'rank_{z["list_id"]}' for z in mt]} for t in focus if (r:=companies.get(t))])
conference_examples={'DAC':['ATEYY','TER','KLAC','ONTO','LITE'],'FMS':['MU','SNDK','ALAB','DELL','HPE'],'RSS':['TER','NVDA'],'Farnborough':['ETN','PH','RYCEY']}
ce=[]
for name,ts in conference_examples.items():
    for t in ts:
        ok=t in prices and '2026-08-19' in prices[t]
        ce.append({'conference':name,'ticker':t,'entry_date':'2026-08-19','entry':'open','end_date':'2026-09-04','ret':ret(t,'2026-08-19',True) if ok else None,'status':'mapped_example_not_recommendation_basket' if ok else 'not_in_cached_universe','selection':'purposive examples of original company mapping, not exhaustive or a performance ranking'})
write('会议映射公司后续观察_非建议回测.csv',ce)
fp=[OLD/'daily_prices.csv',OLD/'company_returns.csv',AUD/'sorting_top30_metrics.csv',master]
(OUT/'data/来源快照.json').write_text(json.dumps([{'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in fp],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'conference_examples':ce,'core_without_META':statistics.mean(ret(t,'2026-08-20',True) for t in ['EME','TEL']),'sources':len(fp),'special_companies':len(rows),'views':len(rankings)},ensure_ascii=False,indent=2))
