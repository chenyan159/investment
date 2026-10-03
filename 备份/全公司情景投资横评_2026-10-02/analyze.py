from pathlib import Path
from datetime import date
import json,csv,re,statistics,collections,hashlib
from extract import clean,cells,nums,ROOT,OUT

obj=json.loads((OUT/'extracted.json').read_text(encoding='utf-8'))
rs=obj['companies']
snap={};heads=None
sp=ROOT/'金融资料/每日金融数据/每日金融数据_2026-10-02.md'
for l in sp.read_text(encoding='utf-8-sig').splitlines():
    if not l.startswith('|'):continue
    cs=cells(l)
    if cs[0]=='股票代号':heads=cs
    elif heads and re.fullmatch(r'[A-Z][A-Z0-9.-]*',cs[0]):snap[cs[0]]=dict(zip(heads,cs))

issues=[]
for r in rs:
    r['years']=(date.fromisoformat(r['target'])-date(2026,10,2)).days/365.25
    r['snapshot']=snap.get(r['ticker'],{})
    r['snapshot_price']=float(r['snapshot']['最新价格'])
    r['snapshot_compatible']=r['ticker'] not in ['TOELY']
    r['security_note']='JPY东京8035拆股后普通股；旧TOELY不可直接比价' if r['ticker']=='TOELY' else '报告证券口径'
    r['quote_change']=(r['snapshot_price']/r['quote']-1)*100 if r['snapshot_compatible'] else None
    for k,sc in r['scenarios'].items():
        ps=sc['price'];sc['return_snapshot']=[(v/r['snapshot_price']-1)*100 for v in ps] if r['snapshot_compatible'] else None
        sc['annual_report']=[((v/r['quote'])**(1/r['years'])-1)*100 if v>0 else -100 for v in ps]
        sc['annual_snapshot']=[((v/r['snapshot_price'])**(1/r['years'])-1)*100 if v>0 else -100 for v in ps] if r['snapshot_compatible'] else None
        sc['fixed_returns']=[float(x) for x in re.findall(r'([+\-−]?\d+(?:\.\d+)?)\s*%',sc['fixed_text'].replace('−','-'))] if sc['fixed_text'] else []
        rp=sc['return_published'];rr=sc['return_calculated']
        if len(rp)!=2 or len(rr)!=2:issues.append([r['ticker'],k,'parse',rp,rr])
        elif max(abs(x-y) for x,y in zip(rp,rr))>.7:issues.append([r['ticker'],k,'arithmetic',rp,rr])
    sc=r['scenarios'];b=sc['基准']['annual_report'];bl=sc['基准']['return_calculated'][0];bh=sc['基准']['return_calculated'][1]
    if r['ticker']=='ATKR':r['bucket']='事件对价约束'
    elif bh<0:r['bucket']='基准全区间亏损'
    elif bl<0:r['bucket']='基准跨零或回报偏低'
    elif b[0]<8:r['bucket']='基准正回报但年化下沿不足8%'
    else:r['bucket']='基准年化下沿至少8%'
    r['base_mid_annual_report']=((sum(sc['基准']['price'])/2/r['quote'])**(1/r['years'])-1)*100
    r['base_mid_annual_snapshot']=((sum(sc['基准']['price'])/2/r['snapshot_price'])**(1/r['years'])-1)*100 if r['snapshot_compatible'] else None
    r['base_mid_annual_delay']=((sum(sc['基准']['price'])/2/r['quote'])**(1/(r['years']+1))-1)*100
    r['base_mid_price20cut']=((sum(sc['基准']['price'])/2*.8/r['quote'])**(1/r['years'])-1)*100
    r['base_pess_ratio']=max(0,sum(sc['基准']['return_calculated'])/2)/abs(sc['悲观']['return_calculated'][0])
    vals=[sc[k]['price'] for k in ['悲观','基准','乐观','突破']]
    if any(vals[i][j]>vals[i+1][j] for i in range(3) for j in [0,1]):issues.append([r['ticker'],'scenario-order',vals])

stats={
 'index_count':obj['index_count'],'report_count':len(rs),'scenario_count':len(rs)*4,
 'buckets':dict(collections.Counter(r['bucket'] for r in rs)),
 'evidence':{k:dict(collections.Counter(r['scenarios'][k]['evidence'] for r in rs)) for k in ['悲观','基准','乐观','突破']},
 'median_base_mid_total':statistics.median(sum(r['scenarios']['基准']['return_calculated'])/2 for r in rs),
 'median_base_mid_annual':statistics.median(r['base_mid_annual_report'] for r in rs),
 'median_pess_low':statistics.median(r['scenarios']['悲观']['return_calculated'][0] for r in rs),
 'pess_low_below50':sum(r['scenarios']['悲观']['return_calculated'][0]<=-50 for r in rs),
 'base_low_above0':sum(r['scenarios']['基准']['return_calculated'][0]>=0 for r in rs),
 'base_high_below0':sum(r['scenarios']['基准']['return_calculated'][1]<0 for r in rs),
 'break_high_nonpositive':sum(r['scenarios']['突破']['return_calculated'][1]<=0 for r in rs),
 'target_years_range':[min(r['years'] for r in rs),max(r['years'] for r in rs)],
 'snapshot_hash':hashlib.sha256(sp.read_bytes()).hexdigest(),
 'categories':[], 'validation_issues':issues
}
for cat in dict.fromkeys(r['category'] for r in rs):
    group=[r for r in rs if r['category']==cat]
    stats['categories'].append({'category':cat,'count':len(group),'base_positive_low':sum(r['scenarios']['基准']['return_calculated'][0]>=0 for r in group),'base_negative_high':sum(r['scenarios']['基准']['return_calculated'][1]<0 for r in group),'median_base_total':statistics.median(sum(r['scenarios']['基准']['return_calculated'])/2 for r in group),'median_base_annual':statistics.median(r['base_mid_annual_report'] for r in group),'median_pess_low':statistics.median(r['scenarios']['悲观']['return_calculated'][0] for r in group)})
(OUT/'analysis.json').write_text(json.dumps({'stats':stats,'companies':rs},ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'全公司四情景复算.csv').open('w',encoding='utf-8-sig',newline='') as f:
    fields=['ticker','name','category','report_quote','snapshot_price','quote_change_pct','target','years','scenario','target_low','target_high','return_report_low','return_report_high','annual_report_low','annual_report_high','return_snapshot_low','return_snapshot_high','evidence','fixed_text','bucket','source_path','source_line','source_sha256']
    w=csv.DictWriter(f,fields);w.writeheader()
    for r in rs:
        for k,sc in r['scenarios'].items():
            def rnd(v):return round(v,4) if isinstance(v,(float,int)) else v
            w.writerow(dict(zip(fields,map(rnd,[r['ticker'],r['name'],r['category'],r['quote'],r['snapshot_price'] if r['snapshot_compatible'] else None,r['quote_change'],r['target'],r['years'],k,*sc['price'],*sc['return_calculated'],*sc['annual_report'],*(sc['return_snapshot'] or [None,None]),sc['evidence'],sc['fixed_text'],r['bucket'],r['path'],sc['line'],r['sha256']]))))
print(json.dumps(stats,ensure_ascii=False,indent=2))
print('RISK_REWARD_CANDIDATES')
for r in sorted(rs,key=lambda r:r['base_pess_ratio'],reverse=True)[:35]:
 print(r['ticker'],round(r['base_pess_ratio'],2),round(r['base_mid_annual_report'],1),round(r['base_mid_annual_snapshot'] or 0,1),r['bucket'])
