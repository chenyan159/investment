from pathlib import Path
from datetime import datetime
import json, re, hashlib, statistics, collections, math

ROOT=Path(r'D:\drive\Investment')
OUT=Path(__file__).parent
VIZ=Path(r'C:\Users\cheny\.codex\visualizations\2026\09\09\01a08863-4bd3-72f1-9e37-058d18265914')
dataset=json.loads((OUT/'market_scenario_data.json').read_text(encoding='utf-8'))
judgments=json.loads((OUT/'investment_judgments.json').read_text(encoding='utf-8'))
positive={'谨慎建议投资','建议投资','强烈建议投资'}
scenarios=['悲观','基准','乐观','突破']
sector_names={
 'AI计算芯片_EDA_IP_custom_ASIC':'芯片/EDA',
 '云算力_IDC_AI软件平台':'云/平台',
 'AI服务器_存储_EMS':'服务器/存储',
 'AI网络_光互联_连接器':'网络/光互联',
 '晶圆制造_前道设备':'晶圆/前道',
 '封测_检测_计量_光罩':'封测/检测',
 '半导体材料_化学品_基板':'材料/基板',
 '机电_冷却_工程_水处理_边缘工业AI':'机电/冷却',
 '配电_电源_功率器件':'配电/功率',
 '电力_发电_能源_储能':'发电/储能'
}
def cell(d,s,m=36):return next(c for c in d['cells'] if c['scenario']==s and c['months']==m)
def rng(c):return [c.get('rebased_low',c['low']),c.get('rebased_high',c['high'])]
def fm(v):return f'{v:+.1f}%'
def fr(v):return fm(v[0])+'～'+fm(v[1])
def fpe(v):return '缺失' if v is None else f'{v:.2f}'
def slink(d):return f"[{d['ticker']}](<{Path(d['file']).as_posix()}>)"
def upclass(d):
    o=rng(cell(d,'乐观'));u=rng(cell(d,'突破'))
    if o[0]>=100:return '很强'
    if u[0]>=100:return '强'
    if u[1]>=100:return '中等'
    return '较弱'

companies=[]
for d in dataset['companies']:
    h=d['history'];q=d['quote'];t=d['ticker']
    g=next((i for i,s in enumerate(['基准','乐观','突破']) if any(c['positive'] for c in d['cells'] if c['scenario']==s)),3)
    obj={'t':t,'n':d['name'],'s':d['sector'],'g':g,'k':d['rank'],'q':[q['price'],q['pe'],q['forward_pe']],
         'quoteDate':q['price_date'],'sameDay':q['price_date']=='2026-09-09' and 'rebased_low' in cell(d,'基准'),
         'p':[h['anchors'][x]['return'] if h and h['anchors'][x] else None for x in ['3m','6m','1y']],
         'mdd':h['mdd_1y'] if h else None,'vol':h['vol_1y'] if h else None,
         'd36':rng(cell(d,'悲观')),'b6':rng(cell(d,'基准',6)),'b12':rng(cell(d,'基准',12)),
         'b36':rng(cell(d,'基准')),'o36':rng(cell(d,'乐观')),'u36':rng(cell(d,'突破'))}
    if t in judgments:
        j=judgments[t];obj.update(defense=j['defense'],priceDefense=j['price_defense'],upside=j['upside_business'],upsideClass=upclass(d))
    companies.append(obj)
def compact(v):
    if isinstance(v,float):return round(v,4)
    if isinstance(v,dict):return {k:compact(x) for k,x in v.items()}
    if isinstance(v,list):return [compact(x) for x in v]
    return v
chartdata=compact({'asof':dataset['asof'],'selected':dataset['selected'],'companies':companies,
   'sectors':[{'name':name,'short':short} for name,short in sector_names.items()],
   'benchmarks':[{'t':t,'k':None,'p':[h['anchors'][x]['return'] for x in ['3m','6m','1y']]} for t,h in dataset['benchmarks'].items()]})
(OUT/'chart_data.json').write_text(json.dumps(chartdata,ensure_ascii=False,indent=2),encoding='utf-8')
runtime=(OUT/'chart-runtime.js').read_text(encoding='utf-8')
visuals=['market-momentum-opportunity','earnings-valuation-mirror','sector-time-horizons','top20-price-performance','defense-and-upside']
for name in visuals:
    file=VIZ/(name+'.html');text=file.read_text(encoding='utf-8')
    payload=json.dumps(chartdata,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    text=re.sub(r'(<script type="application/json">)[\s\S]*?(</script>)',lambda m:m[1]+payload+m[2],text,count=1)
    text=re.sub(r'/\*RUNTIME_START\*/[\s\S]*?/\*RUNTIME_END\*/',lambda m:'/*RUNTIME_START*/\n'+runtime+'\n/*RUNTIME_END*/',text,count=1)
    file.write_text(text,encoding='utf-8')

selected=sorted([d for d in dataset['companies'] if d['rank']],key=lambda d:d['rank'])
market=['# 20家公司估值和历史涨跌幅','','数据截止：2026-09-09美国常规收盘。价格与PE来自当天13:32:32 PDT采集的正式金融快照；3/6/12个月按2026-06-09、2026-03-09、2025-09-09同证券日线Close重新计算。价格包含历史拆股调整，不含现金分配、税费及再投资；不用Adj Close冒充价格涨跌幅。',
 '', '前瞻PE为供应商显示值，预测期与会计调整未统一，不能直接视为精确NTM或同口径增长率。序号是本次综合投资研究优先顺序，并非按历史涨幅或突破回报的单指标排序。',
 '', '| 顺序 | 公司 | 9/9价格 USD | TTM PE | Forward PE | 近3个月 | 近半年 | 近一年 | 一年最大收盘回撤 |', '|---:|---|---:|---:|---:|---:|---:|---:|---:|']
for d in selected:
    q=d['quote'];h=d['history'];values=[d['rank'],slink(d)+' '+d['name'],f"{q['price']:.2f}",fpe(q['pe']) if q['pe'] else '亏损，不适用',fpe(q['forward_pe'])]+[fm(h['anchors'][k]['return']) for k in ['3m','6m','1y']]+[fm(h['mdd_1y'])]
    market.append('| '+' | '.join(map(str,values))+' |')
market+=['','- DKILY无供应商forward EPS/PE，本次保留缺失，不以管理层指引或日本普通股未核对数据代填。','- FLNC为TTM亏损，前瞻PE约79倍建立在很小的预测盈利分母上。','- SMCI使用FY2026稀释EPS 3.26美元：38.93/3.26=11.94倍；不沿用尚未更新的旧EPS 2.08。其未来优先股/转债稀释不会自动全部进入这一个历史PE。','- GOOGL和AMZN存在投资资产重估对利润的影响；ST历史减值和调整口径使TTM与forward差别大。PE差距并不全部代表盈利增长。','- 原始快照的ASML/BABA/TSM汇率相关P/S、GOOGL市值/股数、FLNC经济单位告警不用于本次PE之外的估值推断。快照PE已做价格/EPS算术勾稽，底层财报期并非逐字段重新审计。','',f"[正式金融快照](<{(ROOT/'金融资料/每日金融数据/每日金融数据_2026-09-09.md').as_posix()}>)；[原始行情与逐日数据](<{(OUT/'market_scenario_data.json').as_posix()}>)。"]
(OUT/'20家公司估值与涨跌幅.md').write_text('\n'.join(market)+'\n',encoding='utf-8')

review=['# 20家公司：防御、超高回报业务与行动条件','','本名单用于未来1—3年的新增资金研究排序。先看基准现金价值和买价，再看可更新的业务/客户关系、财务与稀释、增长的可归属现金、不同公司的共同风险，最后比较高回报经营路径；没有给193家伪造统一概率，也没有把20家都列为立即买入。不同风险偏好可以改变次序，前后相邻名次不代表可证明的收益差距。',
 '', '经营防御为本次定性判断：较强=持续收费/受监管需求相对可靠；中等=客户/产品优势存在但有周期、替代或再投资压力；偏弱=利润/现金/融资对不利环境敏感。现价防御单独考虑价值余量与资本结构，均不表示最大损失。历史最大回撤只描述2025-09-09至2026-09-09的日收盘路径。',
 '', '超高回报统一定义为三年累计至少+100%（本金达到2倍，等价年化约25.99%）。空间分级：很强=乐观情景下沿已达+100%；强=需到突破情景下沿才达+100%；中等=只有较强情景区间的一部分达到+100%；较弱=突破上沿仍未达+100%。这是条件空间及所需路径的描述，不是成功概率/置信度，更不等于应配置的仓位。',
 '', '所有三年区间保持原报告的经营、资本、稀释和目标日假设，仅把投资起点换成9月9日报价：新回报=(1+原回报)×原买价/新买价−1。原文目标日期相差一日的期限没有重建；原评级不随这项机械重算自动升级。原报告的悲观行不是灾难下限，尤其TSM、SMCI、FLNC可能出现更深损失。',
 '', '| 公司 | 经营/现价防御 | 超高回报空间 | 悲观三年 | 基准三年 | 乐观三年 | 突破三年 |', '|---|---|---|---:|---:|---:|---:|']
for d in selected:
    j=judgments[d['ticker']]
    review.append('| '+' | '.join([slink(d),j['defense']+' / '+j['price_defense'],upclass(d)]+[fr(rng(cell(d,s))) for s in scenarios])+' |')
for d in selected:
    t=d['ticker'];j=judgments[t];q=d['quote'];h=d['history']
    review += ['',f"## {d['rank']}. {t} — {d['name']}",'',j['action'],'',f"**防御：经营{j['defense']}，现价{j['price_defense']}。** {j['defense_basis']}",'',f"历史一年最大收盘回撤{fm(h['mdd_1y'])}；模型悲观三年{fr(rng(cell(d,'悲观')))}。两者分别是历史事实和经营条件实验，不能互相替代。",'',f"**超高回报空间：{upclass(d)}。关键业务：{j['upside_business']}。** {j['upside_condition']}",'',f"乐观三年{fr(rng(cell(d,'乐观')))}；突破三年{fr(rng(cell(d,'突破')))}。这个上行范围不自带成功概率。",'','**最少验证项：** '+j['watch'],'',f"依据：{slink(d)}正式报告，日期{d['report_date']}；源文件SHA256 `{d['source_sha256']}`。",'']
review+=['## 配置与实施判断','','- 优先建立分批研究仓的现价候选：ADBE、ET、MU、SMCI。MU和SMCI按风险约束更小；SMCI偏一年现金兑现，不能把三年突破上沿用作核心仓依据。','- 长期平台质量候选：MSFT、META、GOOGL、AMZN、NVDA、ASML、TSM、AVGO。企业质量支持持续跟踪，当前多数仍需降价或现金持续性的新证据。','- 估值/经营修复：PNR、BABA、ST、BDC；分散化与收入：AEP、DKILY、DOV。不同组之间仍可能共同暴露于利率和企业资本开支，不能只数股票数量。','- FLNC只留高风险卫星席位。对不能承受极端亏损的资金，直接不配置；保留研究权并不产生持仓义务。','- 三年本金翻倍要求年化25.99%，不能拿三年+40%—60%称作同一层次的高回报。ET和AEP的分配/稳定性、MU和FLNC的弹性，承担的是不同任务。',
 '', '## 没有入选但值得解释的公司','','- SKHY：HBM业务有吸引力；截至原报告9/8的异步可比收盘换算，美国ADS相对韩国普通股等价权益约溢价39%，且ADS转换有约束。这是特定日期的报告计算，不冒充9/9同步套利价。7/10才开始美股历史，不能用韩国原股收益代替该ADS的一年收益。','- SNDK：本次日线计算近一年约+2402%，但9/9价格下基准三年约−8.6%至+14.7%；虽有很大的突破空间，与MU的存储供给周期相关，优先保留MU。','- IREN/CRWV：突破情景非常大，但基准和融资/稀释风险弱，不因为上沿大就替代有现金核心的公司。','- VRT：有真实冷却/电源优势，最近一次价格下跌不足以自动消除基准估值缺口。',
 '', '## 图表范围与统计限制','','- 动量—价值图187家：未混入MICLF的9/8报价，也未补造CBRS、Q、SKHY、WOLF不足一年及SPACEX研究代码缺失的价格。','- PE镜像图143家：只画TTM和forward PE都为正且可得者；其余50家为缺失/亏损/非正值，未当作零。MICLF保留快照显示的9/8报价日期。','- 行业期限图191家：全部有9/9报价且可机械重算者。每家公司先对条件区间中点做年化，再展示行业分布；中点不是期望值，横向分位不是统计置信区间。半年机械年化不能理解为重复相同半年回报的承诺。','- 股价涨幅与未来条件回报存在共享价格分母造成的机械关系，横截面的负相关不能证明反转策略有效。没有把今天挑出的20家历史收益当作选股回测。','- 日线Close按提供方拆股处理；不使用Adj Close，排除现金分配、税费、再投资。涉及分拆、特殊分红、ADR和流动性差异时，纯价格涨跌不等于完整股东财富变化。']
(OUT/'20家公司防御与高回报业务详解.md').write_text('\n'.join(review)+'\n',encoding='utf-8')

anchors=['# 20家公司历史价格锚点与复算','','公式：9/9价格 ÷ 对应日期Close − 1。三个目标日期均为交易日，20家均有原日期有效价格。Yahoo日线9/9部分Close为空，以同日正式快照的常规收盘价补终点，没有退用9/8终点。', '', '| 公司 | 2025-09-09 | 2026-03-09 | 2026-06-09 | 2026-09-09 | 数据源 |','|---|---:|---:|---:|---:|---|']
for d in selected:
    h=d['history'];q=d['quote'];
    anchors.append('| '+' | '.join([d['ticker']]+[f"{h['anchors'][k]['close']:.4f}" for k in ['1y','6m','3m']]+[f"{q['price']:.4f}",f"[Yahoo原始日线]({h['source_url']})"])+' |')
(OUT/'价格锚点与数据口径.md').write_text('\n'.join(anchors)+'\n',encoding='utf-8')

stats={}
for m in [6,12,36]:
    valid=[d for d in companies if d['sameDay']]
    annuals=[100*((1+sum(d[f'b{m}'])/200)**(12/m)-1) for d in valid]
    stats[str(m)]={'n':len(valid),'median_midpoint_annual':statistics.median(annuals),'lower_at_least_12pct_annual':[d['t'] for d in valid if 100*((1+d[f'b{m}'][0]/100)**(12/m)-1)>=12]}
stats['by_sector']={s:{str(m):statistics.median(100*((1+sum(d[f'b{m}'])/200)**(12/m)-1) for d in companies if d['sameDay'] and d['s']==s) for m in [6,12,36]} for s in sector_names}
stats['selected_upside_class']=dict(collections.Counter(upclass(d) for d in selected))
stats['selected_historical_1y_median']=statistics.median(d['history']['anchors']['1y']['return'] for d in selected)
stats['selected_outperformed_spy_1y']=[d['ticker'] for d in selected if d['history']['anchors']['1y']['return']>dataset['benchmarks']['SPY']['anchors']['1y']['return']]
(OUT/'statistics.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')

assert len(selected)==20 and len(judgments)==20
assert len(set(d['ticker'] for d in selected))==20
assert len(companies)==193
hash_mismatch=[d['ticker'] for d in dataset['companies'] if hashlib.sha256(Path(d['file']).read_bytes()).hexdigest()!=d['source_sha256']]
assert not hash_mismatch,hash_mismatch
for d in selected:
    assert d['quote']['price_date']=='2026-09-09'
    assert d['history']['endpoint']['date']=='2026-09-09'
    for k,date in [('3m','2026-06-09'),('6m','2026-03-09'),('1y','2025-09-09')]:
        a=d['history']['anchors'][k]
        assert a['date']==date
        assert abs(a['return']-100*(d['quote']['price']/a['close']-1))<1e-9
for h in dataset['benchmarks'].values():assert h['endpoint']['date']=='2026-09-09'
checks={'checked_at':datetime.now().astimezone().isoformat(),'companies':193,'selected':20,'selected_price_anchors':60,'selected_pe_available':sum(bool(d['quote']['pe']) for d in selected),'selected_forward_pe_available':sum(bool(d['quote']['forward_pe']) for d in selected),'source_hash_mismatches':hash_mismatch,'momentum_points':sum(d['sameDay'] and d['p'][2] is not None for d in companies),'valuation_points':sum(d['q'][1] is not None and d['q'][1]>0 and d['q'][2] is not None and d['q'][2]>0 for d in companies),'same_day_scenario_companies':sum(d['sameDay'] for d in companies),'visuals':{v:(VIZ/(v+'.html')).stat().st_size for v in visuals}}
for v in visuals:
    content=(VIZ/(v+'.html')).read_text(encoding='utf-8')
    assert '__DATA__' not in content and '__RUNTIME__' not in content
    assert len(content.encode('utf-8'))<1_000_000
(OUT/'verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
print(json.dumps(stats,ensure_ascii=False,indent=2))
