from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib, math

ROOT = Path(r'D:\drive\Investment')
OUT = Path(__file__).parent

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def clean(v):
    if isinstance(v, float) and not math.isfinite(v):
        return None
    if isinstance(v, list):
        return [clean(x) for x in v]
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items()}
    return v

def norm(s):
    return s.replace('\\|','｜').replace('**','').strip()

def save(name, data):
    (OUT/name).write_text(json.dumps(clean(data), ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')

old = read(ROOT/'备份/20家公司投资价值与多维图谱_2026-09-09/market_scenario_data.json')
raw = {x['ticker']: x for x in old['companies']}
data = read(OUT/'公司行情及情景复核.json')
extra = clean(read(OUT/'补充公司行情.json'))
for x in extra:
    if x.get('endpoint', {}).get('close') is None:
        x['history_quality_note'] = '供应商未返回2026-09-09有效收盘价；不使用盘中价替代统一比较时点。'
        x['returns'] = {k: None for k in ['3m','6m','1y']}
save('补充公司行情.json', extra)
sp = next(x for x in extra if x['symbol'] == 'SPCX')

rows = []
symbols = [x for x in data['selected'] if x != 'SPCX']
if 'SPACEX' not in symbols:
    symbols.append('SPACEX')
for s in ['BWXT','SMR','OKLO']:
    if s not in symbols:
        symbols.append(s)
for ticker in symbols:
    a = raw[ticker]
    live_ticker = 'SPCX' if ticker == 'SPACEX' else ticker
    p = Path(a['file'])
    price = a['quote'].get('price')
    q = dict(a['quote'])
    if ticker == 'SPACEX':
        p = next((ROOT/'分析报告/公司情景投资决策/结果').glob('SPCX*.md'))
        price = sp['endpoint']['close']
        q = {'ticker': 'SPCX', 'name': 'SpaceX', 'price': price, 'price_date': '2026-09-09',
             'pe': None, 'forward_pe': sp['quote']['forwardPE'], 'currency': 'USD',
             'data_source': 'Yahoo Finance/yfinance; issuer IPO announcement verifies ticker',
             'source_timestamp': sp['retrieved_at'],
             'note': 'Forward EPS预测年度/口径未得到独立验证，不用于投资排序；多类别股份口径不直接用A类股数乘价推集团市值。'}
    assert p.exists(), p
    text = p.read_text(encoding='utf-8')
    lines = text.splitlines()
    cur_hash = sha(p)
    original_hash_ok = cur_hash == a['source_sha256']
    assert original_hash_ok or ticker == 'SPACEX', ticker
    scen = {}
    for c in a['cells']:
        if c['months'] not in [12,36]:
            continue
        assert norm(c['text']) in norm(text), (ticker,c['scenario'],c['months'])
        low = (1+c['low']/100)*a['anchor_price']/price*100-100
        high = (1+c['high']/100)*a['anchor_price']/price*100-100
        line = next(i+1 for i,l in enumerate(lines) if norm(c['text']) in norm(l))
        scen[f"{c['scenario']}_{c['months']}"] = {'mid':(low+high)/2, 'low':low, 'high':high,
            'source_line':line,'label':c['label'],'original_text':c['text']}
    assert len(scen) == 8, ticker
    h = (a.get('history') or {}).get('anchors') or {}
    returns = {k:(v.get('return') if isinstance(v,dict) else None) for k,v in h.items()}
    if ticker == 'SPACEX':
        returns = {k:(v.get('percent') if v else None) for k,v in sp['returns'].items()}
    cfiles = sorted((ROOT/'基本面/公司调研').glob(f'*/*{live_ticker}_*公司调研_*.md'))
    # Exact ticker prefix prevents accidental cross-company matches.
    cfiles = [f for f in cfiles if f.name.startswith(live_ticker+'_')]
    rows.append({'ticker': live_ticker, 'name': a['name'], 'sector':a['sector'],
        'file':str(p), 'report_date':a['report_date'], 'anchor_price':a['anchor_price'],
        'source_sha256':a['source_sha256'], 'current_sha256':cur_hash,
        'hash_match':original_hash_ok, 'scenario_cells_verified':True,
        'alias_note':'SPACEX旧索引已对应到SPCX；逐格验证现行报告，补价后重算回报。' if ticker=='SPACEX' else None,
        'quote':q, 'history_returns':returns, 'scenarios':scen,
        'company_files':[str(f) for f in cfiles]})
data.update({'selected':[x['ticker'] for x in rows], 'rows':rows,
    'verified_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),
    'method': '价格涨跌幅为当地挂牌币种、拆股调整后收盘价，不含股息。情景沿用现行报告原回报，按9月9日收盘价换算，保留原模型分红/分拆等假设；三年数为累计条件回报而非年化、概率期望或市价预测。区间显示值为上下限算术平均。',
    'coverage_note':'原193家公司池有SPACEX旧代码；现行正式研究为SPCX。原报告55份全文哈希相符，SPCX更名报告8个一年/三年格逐格核验。'})
save('公司行情及情景复核.json', data)

G = ROOT/'基本面/行业调研'
growth_specs = [
 ('功率半导体','全球功率分立器件与模块',2026,2030,36.7,51.5,'十亿美元','AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-09-06.md','2026报告中心值；2030基准区间均值；不是全体模拟/电源管理IC。'),
 ('功率半导体','广义AI电源半导体',2026,2030,5.5,12,'十亿美元','AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-09-06.md','两端基准区间均值；子市场与全球功率统计口径不同，不可相加。'),
 ('功率半导体','SiC功率器件',2026,2030,4.5,9,'十亿美元','AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-09-06.md','区间均值；汽车/工业需求也重要。'),
 ('功率半导体','GaN功率器件',2026,2030,.8,2.75,'十亿美元','AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-09-06.md','区间均值；低基数、份额和ASP敏感。'),
 ('电力设备发电设备','数据中心开关设备与变压器',2026,2030,17,28.5,'十亿美元','AI园区电力_机电_冷却/行业调研_数据中心开关设备与变压器_2026-09-06.md','基准区间均值；不含全电网、UPS、储能、冷却及工程总包。'),
 ('电力设备发电设备','美国数据中心自备主电源当年净投运',2026,2028,3.2,7.7,'GW','AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-09-06.md','报告工作点；排除仅应急备用，不是订单签署容量。'),
 ('电力设备发电设备','上述投运电站对应资产额',2026,2028,10.8,22.6,'十亿美元','AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-09-06.md','报告工作点；资产额不能直接当成设备制造商收入。'),
 ('电力设备发电设备','800VDC核心设备',2026,2030,.136,4.521,'十亿美元','AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-09-06.md','报告工作点，低基数低置信度；800V不等于必须采用SST。'),
 ('冷却','数据中心直液冷A口径核心系统',2026,2028,3.9,6.2,'十亿美元','AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-09-06.md','报告中心值；不含冷板、室外排热和服务，不能与全口径报告直接比较。'),
 ('冷却','液冷小组件与流体控制核心市场',2026,2030,1.83,2.78,'十亿美元','AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-09-06.md','报告中心值；MW增长快于组件金额增长。'),
 ('材料与基板','完整有机封装基板ABF+BT',2026,2028,19.8,29.6,'十亿美元','AI服务器_存储_芯片/行业调研_封装基板、中介层与RDL_2026-09-06.md','报告中心值；含非AI，不等于ABF树脂材料收入。'),
 ('材料与基板','AI加速器大尺寸基板',2026,2028,3.3,8.2,'十亿美元','AI服务器_存储_芯片/行业调研_封装基板、中介层与RDL_2026-09-06.md','报告中心值；上一行子集。'),
 ('材料与基板','中介层与RDL制造价值',2026,2028,6.3,13.7,'十亿美元','AI服务器_存储_芯片/行业调研_封装基板、中介层与RDL_2026-09-06.md','含内部制造价值，不能等同独立第三方销售。'),
 ('材料与基板','前道材料不含光罩',2026,2028,46,55.5,'十亿美元','晶圆制造_设备_材料_测试/行业调研_硅片、光刻胶与前道材料_2026-09-06.md','基准区间均值；大宗硅片与先进节点配方增速不同。'),
 ('材料与基板','大型AI封装玻璃芯板销售',2026,2030,.0075,.375,'十亿美元','晶圆制造_设备_材料_测试/行业调研_玻璃基板、TGV与玻璃检测_2026-09-06.md','极低基数、低置信度；2028工作点0.075B；不能外推到玻璃集团整体收入。'),
 ('AI计算中心互联','高速铜缆核心市场AEC/DAC等',2026,2028,6.1,11,'十亿美元','AI网络_光互联_铜互联/行业调研_AEC、DAC与高速铜缆_2026-09-06.md','2026中心值，2028基准区间均值；不是AEC单项。'),
 ('AI计算中心互联','400G以上可插拔内EML/CW激光器价值',2026,2028,2.6,4.6,'十亿美元','AI网络_光互联_铜互联/行业调研_激光器、EML与光器件_2026-09-06.md','报告中心值；含内部器件价值，不含CPO外置光源和完整模块。'),
 ('AI计算中心互联','独立800G/1.6T非相干可插拔模块',2026,2028,27.45,34,'十亿美元','AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-09-06.md','报告中心值；2027为33.42B，ASP下降和产品代际迁移压平2028金额。'),
 ('AI计算中心互联','交换侧CPO/NPO光子系统价值',2026,2030,.26,5.8,'十亿美元','AI网络_光互联_铜互联/行业调研_CPO_NPO与交换侧光引擎_2026-09-06.md','区间均值；含内部价值，2028中点2.04B，低置信度。'),
 ('太空经济','低轨卫星运营相关收入含终端',2026,2030,18,36,'十亿美元','商业航天_火箭_卫星/行业调研_商业火箭与商业航天_2026-09-06.md','基准区间均值；不能当成纯订阅或全太空经济。'),
 ('太空经济','西方外部中大型入轨采购',2026,2030,4.55,7.65,'十亿美元','商业航天_火箭_卫星/行业调研_商业火箭与商业航天_2026-09-06.md','基准区间均值；排除自有星座内部发射。'),
 ('太空经济','卫星遥感收入',2025,2030,3.64,6.2,'十亿美元','商业航天_火箭_卫星/行业调研_商业火箭与商业航天_2026-09-06.md','2025历史锚点，2030基准均值；含不同任务和数据模式。'),
 ('机器人','机器人核心硬件交付等价值',2026,2030,27.45,52.6,'十亿美元','机器人_硬件_零部件/行业调研_机器人硬件_2026-09-06.md','基准区间均值；工业本体、特定物流及非玩具具身硬件，非完整自动化系统收入。'),
 ('机器人','具身智能新形态硬件',2026,2028,1.425,4.43,'十亿美元','机器人_硬件_零部件/行业调研_机器人硬件_2026-09-06.md','基准区间均值；含轮式、科研、展示交付，不等于成熟工厂人形劳动力。'),
]
growth=[]
for sector,segment,start,end,a,b,unit,file,note in growth_specs:
    path=G/file
    assert path.exists(),path
    growth.append({'sector':sector,'segment':segment,'start_year':start,'end_year':end,
        'start':a,'end':b,'unit':unit,'cagr_percent':100*((b/a)**(1/(end-start))-1),
        'source':str(path),'source_sha256':sha(path),'note':note})
save('行业增长口径与计算.json',growth)

def link(p,label):
    return f'[{label}](<{str(p).replace(chr(92),"/")}>)'

def n(v, sign=False):
    if v is None or not isinstance(v,(float,int)) or not math.isfinite(v):
        return '—'
    return (f'{v:+.1f}%' if sign else f'{v:.1f}')

top=set(['NVDA','MSFT','MU','META','GOOGL','AMZN','AVGO','TSM','BABA','CRDO','ASML','HTHIY','NVT','EME','ADBE','TEL','APH','JBL','SNDK','ET'])
groups={
 '功率半导体':['MPWR','IFNNY','LFUS','ON','STM','VICR','NVTS','WOLF'],
 '电力设备、发电设备与工程':['HTHIY','NVT','EME','ETN','GEV','CMI','CAT','HUBB','PWR','GNRC','BE','BWXT','OKLO','SMR'],
 '冷却、流体与配套':['VRT','MOD','AAON','TT','JCI','ECL','DOV','FLEX','JBL'],
 '半导体材料和基板':['AJNMY','Q','ENTG','SHECY','ASGLY','HOCPY','LIN','AXTI','ROG'],
 'AI计算中心互联':['CRDO','AVGO','APH','TEL','LITE','COHR','MTSI','ANET','ALAB','GLW','SMTOY'],
 '太空经济与机器人':['SPCX','RKLB','TSLA','TER','ABBNY'],
}
lookup={x['ticker']:x for x in rows}
doc=['# 相关公司行情与情景对照','',
 '价格统一使用2026-09-09收盘；历史涨跌为挂牌币种价格回报，不含分红。估值为该日快照供应商口径，Forward PE预测期未完全统一，适合初筛而非精确估值排名。', '',
 '情景表来自2026-09-08/09正式报告，并按9月9日价格换算。区间均值仅为展示值，不是概率预期；三年为累计回报，不是年化。不同公司情景强度、终值、融资与新业务行内成功权重存在差异，不能按最大数字机械排名。异常高倍数保留原值并单列说明。','']
for group,tickers in groups.items():
    doc += [f'## {group}','', '| 公司 | 原前20 | PE | Forward PE | 近3个月 | 近半年 | 近一年 | 基准一年 | 基准三年 | 乐观一年 | 乐观三年 | 突破一年 | 突破三年 |','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for ticker in tickers:
        if ticker not in lookup:
            continue
        r=lookup[ticker];q=r['quote'];sc=r['scenarios'];hr=r['history_returns']
        vals=[link(r['file'],f"{ticker} {r['name']}"),'是' if ticker in top else '否',n(q.get('pe')),n(q.get('forward_pe'))]
        vals += [n(hr.get(k),True) for k in ['3m','6m','1y']]
        vals += [n(sc[k]['mid'],True) for k in ['基准_12','基准_36','乐观_12','乐观_36','突破_12','突破_36']]
        doc.append('| '+' | '.join(vals)+' |')
    doc += ['']
doc += ['## 原公司池遗漏标的的补充行情','',
 '这些公司尚无当前193家公司矩阵中的完整情景估值，不补造情景回报。日本、台湾、欧洲历史涨跌为当地货币；Forward PE用9月9日有效收盘价除以9月10日取得的供应商Forward EPS，仅作标注明确的补充，预测年度/调整口径仍待核实。','',
 '| 公司 | 代码 | 9月9日收盘/币种 | 近3个月 | 近半年 | 近一年 | 补充Forward PE |','|---|---|---:|---:|---:|---:|---:|']
names={'4062.T':'Ibiden 揖斐电','3037.TW':'Unimicron 欣兴','6954.T':'FANUC 发那科','6506.T':'Yaskawa 安川电机','SYM':'Symbotic','ASTS':'AST SpaceMobile','PL':'Planet Labs','SU.PA':'Schneider Electric 施耐德'}
for e in extra:
    s=e['symbol']
    if s=='SPCX':continue
    price=e.get('endpoint',{}).get('close');q=e.get('quote',{});eps=q.get('forwardEps')
    pe=price/eps if price and eps and eps>0 else None
    disppe='无比较意义（近盈亏平衡）' if pe and pe>500 else n(pe)
    vals=[names[s],s,((f'{price:.2f} {q.get("currency")}') if price else '未取得有效收盘价')]
    vals += [n((e.get('returns',{}).get(k) or {}).get('percent'),True) for k in ['3m','6m','1y']]
    vals += [disppe]
    doc.append('| '+' | '.join(vals)+' |')
doc += ['','说明：SPCX上市时间为2026-06-12，不足完整三个月；Q上市不足一年；WOLF重组前后不能直接拼接一年回报。SPCX Forward EPS预测口径未独立确认，RKLB和PL极高Forward PE主要受接近盈亏平衡的分母影响，不能据此精确比较贵便宜。Schneider未取得有效9月9日历史收盘，保留缺失，经营证据仍可用于覆盖审查。','',
 '## 行业预测完整口径','',
 '以下是项目行业研究的独立条件估算，不是已经实现的收入，也不是统一市场共识。CAGR由列示的中心值/区间均值计算；嵌套、内部制造价值和不同地区口径不相加。','',
 '| 行业 | 口径 | 年份 | 起点 | 终点 | CAGR | 单位 | 限定 |','|---|---|---|---:|---:|---:|---|---|']
for g in growth:
    doc.append('| '+' | '.join([g['sector'],link(g['source'],g['segment']),f"{g['start_year']}→{g['end_year']}",f"{g['start']:g}",f"{g['end']:g}",n(g['cagr_percent'],True),g['unit'],g['note']])+' |')
(OUT/'相关公司行情与情景对照.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')

manifest={'checked_at':data['verified_at'],'market_date':'2026-09-09',
          'scenario_company_count':len(rows),'same_hash_count':sum(r['hash_match'] for r in rows),
          'verified_matrix_cells':sum(len(r['scenarios']) for r in rows),
          'supplemented_universe_count':len(extra)-1,
          'industry_series_count':len(growth),'industry_report_count':len({g['source'] for g in growth}),
          'inputs':[{'file':r['file'],'sha256':r['current_sha256']} for r in rows],
          'industry_inputs':[{'file':p,'sha256':sha(Path(p))} for p in sorted({g['source'] for g in growth})],
          'company_inputs':[{'file':p,'sha256':sha(Path(p))} for p in sorted({p for r in rows for p in r['company_files']})],
          'note':'仅创建一次性备份成品；没有修改正式研究、行情生成器或公司池。SPCX为本次分析内更名映射，正式上下游数据修复另行实施。'}
save('来源核验记录.json',manifest)
print(json.dumps({k:v for k,v in manifest.items() if k not in ['inputs','industry_inputs','company_inputs']},ensure_ascii=False,indent=2))
print('GROWTH',[(g['segment'],round(g['cagr_percent'],1)) for g in growth])
