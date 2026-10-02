from pathlib import Path
from datetime import datetime, date
from zoneinfo import ZoneInfo
import hashlib, json, math, sys

sys.stdout.reconfigure(encoding='utf-8')
OUT = Path(__file__).parent
ROOT = Path(r'D:\drive\Investment')
SOURCE = ROOT/'备份/20家公司投资价值与多维图谱_2026-09-09/market_scenario_data.json'
SNAPSHOT = ROOT/'金融资料/每日金融数据/每日金融数据_2026-09-09.md'
market = json.loads(SOURCE.read_text(encoding='utf-8'))
paired = json.loads((OUT/'latest_comparable_iv.json').read_text(encoding='utf-8'))
selected = paired['selected']
companies = {c['ticker']: c for c in market['companies']}
pairs = {c['ticker']: c for c in paired['results']}
ASOF = date(2026,9,9)
EXPIRY = '2026-10-16'

NAMES = {'MU':'美光','ADBE':'Adobe','MSFT':'微软','NVDA':'英伟达','META':'Meta',
         'BABA':'阿里巴巴','GOOGL':'Alphabet','AMZN':'亚马逊','ASML':'阿斯麦','TSM':'台积电',
         'AVGO':'博通','ET':'Energy Transfer','SNDK':'闪迪','APH':'安费诺','TEL':'TE Connectivity',
         'JBL':'捷普','NTAP':'NetApp','IBM':'IBM','SMCI':'超微电脑','BDC':'Belden'}
REASONS = {
 'MU':('HBM、DRAM及存储制造技术；现有利润和现金积累','HBM扩容、DRAM定价、AI服务器内存含量提升','周期、资本开支和价格回落；低Forward PE可能是高景气利润的倒数'),
 'ADBE':('创意和文档订阅、专业工作流与客户续费；当前估值较低','Firefly商业化、企业内容自动化、Acrobat AI和付费升级','AI工具替代与定价权下降；AI行业增长不自动等于Adobe增长'),
 'MSFT':('企业合同、Office/身份/安全/云平台和经常性收入','Azure AI、Copilot、代理及企业AI预算转为可持续利润','巨额资本开支、折旧、模型及能源成本'),
 'NVDA':('CUDA生态、系统与网络能力、已实现盈利和现金','训练与推理计算、整机系统、网络，以及平台租金持续','客户资本开支周期、定制芯片、集中度；强业务护城河不等于股价有底'),
 'META':('广告现金流、用户网络和推荐分发规模','AI广告转化率、商业消息、应用使用和变现效率','广告周期、监管及AI资本开支'),
 'BABA':('电商存量业务、客户及商家生态、回购分配能力','阿里云AI、模型与企业服务增长转为现金利润','竞争补贴、资本开支、监管与股东价值传导'),
 'GOOGL':('搜索、YouTube与广告现金流，云平台和分发入口','Gemini、Google Cloud、TPU及AI搜索的收入与成本效率','搜索被替代、监管、资本开支；TTM利润含投资公允价值影响'),
 'AMZN':('AWS、广告和零售履约基础，业务组合多样','AWS AI、Trainium、广告及零售效率改善','建设和投资承诺、资本开支及利润到现金的差异；TTM含投资估值影响'),
 'ASML':('EUV设备技术地位、服务安装基数与切换成本','EUV/High-NA及先进节点投入','估值、晶圆厂资本开支周期和出口限制'),
 'TSM':('先进制程制造能力、客户与良率积累','先进节点、CoWoS和AI芯片制造需求','再投资强度、客户集中、地缘尾部风险'),
 'AVGO':('定制芯片和网络客户关系、软件现金流','AI ASIC、以太网及软件效率','客户集中、项目周期、负债与资本分配'),
 'ET':('管网基础设施、合同及现金分配','数据中心电力需求带来的天然气运输和基础设施需求','AI传导间接、杠杆和项目资本开支；分配不保证且税后回报因账户而异'),
 'SNDK':('已兑现存储利润、现金流及NBM相关合同','AI存储需求、NAND景气、企业SSD与利润率','高度周期性；不能只因6倍Forward PE就认定有强下行保护'),
 'APH':('连接器制造、客户设计导入、多终端市场与切换成本','高速互连、AI服务器单机价值量及网络升级','并购负债、生命周期与ROIC、客户压价及高估值'),
 'TEL':('汽车、工业、电力及连接业务分散，既有现金利润','数据中心连接、电力及AI互连内容量','汽车/工业周期，新增收入的净利润和现金转化可能下降'),
 'JBL':('客户交付与工程能力、非AI业务及既有产能','AI服务器、机柜、电力与散热配套工程','薄利润率、营运资本、资本开支和股权薪酬侵蚀股东现金'),
 'NTAP':('ONTAP、企业续费、安装基数和多云渠道','企业AI数据管理、混合云和存储需求','AI需求未必转成超额利润，存储周期、再投资及SBC'),
 'IBM':('混合云、Red Hat、主机与企业软件的延续收入','企业AI、软件增长和咨询效率带来的可持续现金','有机增长、咨询工时替代、现金流正常化；量子计算不是主要估值支柱'),
 'SMCI':('客户交付和规模形成一定业务价值，估值较低','AI服务器、整机机柜与液冷交付','利润与经营现金流明显分离，营运资本和融资需求；仅适合小权重'),
 'BDC':('工业连接和客户设计导入','Ruckus、网络/数据中心业务整合与现金转化','收购后净负债和整合风险大，原报告悲观情景损失很深；仅适合小权重'),
}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def good_call(row, spot):
    values = [row.get(k) for k in ('strike','impliedVolatility','bid','ask')]
    if any(v is None or not math.isfinite(v) for v in values): return False
    strike, iv, bid, ask = values
    if not (.01 <= iv <= 3 and bid > 0 and ask >= bid): return False
    if abs(strike/spot-1) > .05: return False
    if (ask-bid)/((ask+bid)/2) > .30: return False
    if (row.get('volume') or 0)+(row.get('openInterest') or 0) < 1: return False
    dt = row.get('lastTradeDate')
    if not dt: return False
    trade_date = datetime.fromisoformat(dt.replace('Z','+00:00')).astimezone(ZoneInfo('America/New_York')).date()
    return 0 <= (ASOF-trade_date).days <= 7

def number(v, signed=True):
    if abs(v) < .05: v = 0.0
    return f'{v:+.1f}' if signed else f'{v:.1f}'

def pct(v):
    return number(v)+'%'

def band(row):
    return pct(row['rebased_low'])+'～'+pct(row['rebased_high'])

rows=[]
checks=[]
header='|顺位·公司|PE|Forward PE|近3月|近半年|近1年|基准1年|基准3年|突破1年|突破3年|最新IV¹|'
table=[header,'|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|']
for rank,ticker in enumerate(selected,1):
    c=companies[ticker]
    q,h=c['quote'],c['history']
    assert q['price_date']==str(ASOF), (ticker,'quote date')
    assert h['endpoint']['date']==str(ASOF), (ticker,'endpoint date')
    assert abs(q['price']-h['endpoint']['close']) < 1e-8, (ticker,'close')
    assert c['source_sha256'].lower()==sha(Path(c['file'])), (ticker,'report changed')
    for period,target in [('3m','2026-06-09'),('6m','2026-03-09'),('1y','2025-09-09')]:
        a=h['anchors'][period]
        assert a['date']==target, (ticker,period,'anchor date')
        assert abs((q['price']/a['close']-1)*100-a['return']) < 1e-8, (ticker,period,'return')
    scen={f'{x[0]}_{x[1]}m':next(z for z in c['cells'] if z['scenario']==x[0] and z['months']==x[1]) for x in [('基准',12),('基准',36),('突破',12),('突破',36),('乐观',36),('悲观',36)]}
    for k,v in scen.items():
        assert v['rebased_low'] <= v['rebased_high'], (ticker,k,'band')
        for side in ['low','high']:
            calculated=((1+v[side]/100)*c['anchor_price']/q['price']-1)*100
            assert abs(calculated-v['rebased_'+side]) < 1e-7, (ticker,k,side,'rebase')
    rawpath=OUT/'原始期权链'/f'{ticker}.json'
    raw=json.loads(rawpath.read_text(encoding='utf-8'))
    assert raw['expiry']==EXPIRY
    choices=[r for r in raw['calls'] if good_call(r,q['price'])]
    assert choices, (ticker,'no clean call')
    call=min(choices,key=lambda r:(abs(r['strike']-q['price']),-(r.get('openInterest') or 0)-(r.get('volume') or 0)))
    iv=call['impliedVolatility']*100
    relative_spread=(call['ask']-call['bid'])/((call['ask']+call['bid'])/2)*100
    distance=abs(call['strike']/q['price']-1)*100
    assert q['pe'] > 0 and q['forward_pe'] > 0
    row={'rank':rank,'ticker':ticker,'name':NAMES[ticker],'sector':c['sector'],
         'price':q['price'],'price_date':q['price_date'],'pe':q['pe'],'forward_pe':q['forward_pe'],
         'returns':{k:h['anchors'][k] for k in ('3m','6m','1y')},
         'scenarios':scen,'report_file':c['file'],'report_sha256':c['source_sha256'],
         'report_date':c['report_date'],'report_anchor_price':c['anchor_price'],
         'iv_percent':iv,'iv_type':'near-ATM call source impliedVolatility, annualized',
         'iv_expiry':EXPIRY,'iv_dte_calendar':37,'iv_collected_at':raw['collected_at'],
         'iv_contract':call,'iv_strike_distance_percent':distance,'iv_relative_bid_ask_spread_percent':relative_spread,
         'iv_quote_timestamp':None,'iv_source_url':f'https://finance.yahoo.com/quote/{ticker}/options/?date=1792108800',
         'option_raw_sha256':sha(rawpath),'optional_paired_call_put_iv_percent':pairs[ticker]['iv_percent'],
         'defense_basis':REASONS[ticker][0],'growth_business':REASONS[ticker][1],'failure_mechanism':REASONS[ticker][2]}
    rows.append(row)
    vals=[f'{rank}. **{ticker}** {NAMES[ticker]}',f'{q["pe"]:.2f}',f'{q["forward_pe"]:.2f}']
    vals += [pct(h['anchors'][k]['return']) for k in ('3m','6m','1y')]
    vals += [band(scen[k]) for k in ('基准_12m','基准_36m','突破_12m','突破_36m')]
    vals += [f'{iv:.1f}%'+('†' if ticker in ('TEL','BDC') else '')]
    table.append('|'+ '|'.join(vals)+'|')
    checks.append({'ticker':ticker,'report_hash_matches':True,'close_date_matches':True,'history_anchors_and_returns_pass':True,'scenario_rebase_pass':True,'clean_call_pass':True})

assert len(rows)==len(set(selected))==20
table_md='\n'.join(table)
intro='''# AI乐观情景下：增长与下行保护兼顾的20家公司

数据截至2026年9月9日美股常规交易时段收盘；期权链于当日18:22 PDT重新采集。此文件为本次对话的一次性研究成品，不覆盖正式公司报告。

这份名单基于“AI需求持续增长”的组合配置判断，依次考虑已形成的现金流、AI增量能否转成股东现金、当前估值、基准与悲观情景承压，以及突破空间。顺位代表综合配置优先级，未给各情景虚构概率，也不是可证明的唯一最优解。AI乐观不等于每家公司均能兑现突破。

主表PE以倍计，其余数字均为百分比。历史列为过去的股价变动；情景列为条件累计回报区间，三年列不是年化收益。

'''
notes='''

## 取值口径

1. **最新IV**：统一采用2026年10月16日到期、距9月9日收盘价最近且通过报价质量筛选的Call（看涨期权）来源年化IV，剩余37个日历日。不是IV Rank、历史波动率或上涨概率。没有把Call/Put平均值混入主表；19家可配对的平均值另存在`latest_comparable_iv.json`中供核对。
2. IV筛选条件：执行价距现价不超过5%；买卖价为正且有效；相对买卖价差不超过30%；成交量与未平仓量之和大于零；最近成交距行情日不超过7个日历日；来源IV处于1%至300%。数据商未提供买卖报价更新时间，采集时间和最后成交时间不等同于报价时间。
3. **TEL/BDC†**：TEL使用执行价200的Call，IV 42.0%，相对买卖价差23.5%，最后成交为9月3日；BDC使用执行价115的Call，IV 55.1%，距收盘价约2.4%，相对买卖价差29.9%，最后成交为9月8日。二者交易较不活跃、价差较宽，估值精度低于活跃期权；最后成交时间也不能证明买卖报价在哪一刻更新。BDC没有合格的同执行价Call/Put配对，但本表20家都使用Call口径。
4. **历史涨幅**：以9月9日收盘价对2026年6月9日、3月9日和2025年9月9日的拆股调整收盘价计算；不含分红再投资、税费和交易成本。SNDK的一年+2402.0%来自70.51至1764.17的来源价格变化，不是误把半年涨幅作为一年。
5. **情景回报**：取当前正式报告的四种经营情景中“基准”和“突破”的一年、三年单元，保持原报告终值与现金分配假设，用9月9日价格换算：`(1 + 原回报) × 报告锚价 / 当前价 − 1`。没有重新预测终值，没有把报告价值区间改成统计置信区间或保底回报。期限沿用原报告9月8日/9月9日建模起点，相差最多一天。
6. **PE与Forward PE**：取9月9日金融快照的TTM与来源预测EPS口径。各公司Forward EPS预测期、GAAP/调整口径未被数据商完整披露，因此不能将横向差异全部解释为便宜程度。GOOGL、AMZN的TTM利润含投资估值影响；MU、SNDK的Forward PE高度依赖存储景气假设。

## 如何使用这份名单

优先研究和分批建立的核心是MU、MSFT、NVDA、ADBE、META；但MU的周期风险、NVDA的资本开支周期与ADBE的AI替代风险分别要单独控制。BABA以估值与AI云弹性补充，不能忽略股东价值传导。

ET承担现金分配和业务分散角色，AI增长传导较间接。ASML/TSM/AVGO提供先进制造与定制芯片敞口；APH/TEL/JBL/NTAP/IBM分散到连接、交付和企业数据软件。其业务延续性不代表现价便宜：TSM、AVGO、NTAP的基准三年区间仍包含亏损。

SNDK与MU共享存储景气，组合中要合并看风险；不能将两只股票视为充分分散。SMCI与BDC只保留为小权重高弹性部分，原因是现金转化或收购负债削弱了保护。均等分配20家公司不会自动实现这个目标。

IV提供短期期权价格中的不确定性尺度，低IV不保证本金安全，高IV也不保证高回报。期限一致有助于比较，但不同公司财报日期、事件和报价质量仍然不同。[Cboe对按到期日与固定期限波动率的说明](https://datashop.cboe.com/volatility-surfaces)

## 每家公司保护与增长来自哪里

'''
details=[]
for r in rows:
    details.append(f"- **{r['ticker']}**：保护依据为{r['defense_basis']}；高增长来自{r['growth_business']}；主要失效因素为{r['failure_mechanism']}。[正式报告]({Path(r['report_file']).as_posix()})")
sources=f'''

## 来源与校验

- [2026年9月9日金融快照]({SNAPSHOT.as_posix()})：价格、TTM PE和Forward PE。
- [193家公司市场与情景数据]({SOURCE.as_posix()})：历史价格锚点、正式报告路径/哈希、原始及换算后的情景单元。
- [本表完整数据和逐行合约]({(OUT/'20家公司合并数据.json').as_posix()})：20条行数据，包括执行价、Call/Put原始IV、最后成交时间、价差和文件哈希。
- [校验记录]({(OUT/'validation.json').as_posix()})：20份正式报告哈希一致、60个历史锚点/涨幅一致、120个情景单元重算一致、20个Call筛选通过。

个股期权来源为Yahoo Finance options，经yfinance读取。完整原始期权链保存在本目录`原始期权链`中；每条来源URL及采集时间附在完整数据中。本报告只重组已有研究并补充最新可取得的期权数据，未修改正式报告或金融快照。
'''
(OUT/'20家公司合并总表.md').write_text(intro+table_md+notes+'\n'.join(details)+sources,encoding='utf-8')
payload={'asof':str(ASOF),'selection':'AI乐观发展下兼顾已形成的现金流、估值与增长的主观组合优先级；非概率模型或唯一数学最优解',
         'iv_definition':'same-expiry clean near-ATM call source annualized implied volatility',
         'snapshot_path':str(SNAPSHOT),'snapshot_sha256':sha(SNAPSHOT),
         'scenario_source_path':str(SOURCE),'scenario_source_sha256':sha(SOURCE),'rows':rows}
(OUT/'20家公司合并数据.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'validation.json').write_text(json.dumps({'asof':str(ASOF),'companies':20,'history_anchors_checked':60,'scenario_cells_checked':120,'common_expiry':EXPIRY,'calls_with_clean_iv':20,'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(table_md)
print('\nIV audit:')
for r in rows:
    print(r['ticker'],f"IV={r['iv_percent']:.4f}", 'K='+str(r['iv_contract']['strike']),f"spread={r['iv_relative_bid_ask_spread_percent']:.2f}%",r['iv_contract']['lastTradeDate'])
print('\nVALIDATED: 20 report hashes, 60 history anchors, 120 rebased scenario cells, 20 same-expiry clean calls.')
