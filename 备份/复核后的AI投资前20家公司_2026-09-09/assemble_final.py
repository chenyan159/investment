from pathlib import Path
from datetime import datetime,date
from zoneinfo import ZoneInfo
import hashlib,json,math,re,sys

sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).parent
ROOT=OUT.parent.parent
MARKET=ROOT/'备份/20家公司投资价值与多维图谱_2026-09-09/market_scenario_data.json'
market=json.loads(MARKET.read_text(encoding='utf-8'))
quotes=json.loads((OUT/'最新行情及IV.json').read_text(encoding='utf-8'))
ivs=json.loads((OUT/'可用IV核查.json').read_text(encoding='utf-8'))
history=json.loads((OUT/'历史涨幅复核.json').read_text(encoding='utf-8'))
cs={c['ticker']:c for c in market['companies']}
qs={r['ticker']:r for r in quotes['results']}
vi={r['ticker']:r for r in ivs['results']}
hs={r['ticker']:r for r in history['results']}
selected=quotes['selected']
names={'NVDA':'英伟达','MSFT':'微软','MU':'美光','META':'Meta','GOOGL':'Alphabet','AMZN':'亚马逊','AVGO':'博通','TSM':'台积电','BABA':'阿里巴巴','CRDO':'Credo','ASML':'阿斯麦','HTHIY':'日立','NVT':'nVent','EME':'EMCOR','ADBE':'Adobe','TEL':'TE Connectivity','APH':'安费诺','JBL':'捷普','SNDK':'闪迪','ET':'Energy Transfer'}
reasons={
 'NVDA':'AI计算、CUDA、网络与系统价值捕获直接，已有现金盈利；风险在客户支出、ASIC竞争与集中度。',
 'MSFT':'企业软件、云与订阅现金基础；Azure AI及Copilot提供增长，需核查资本投入与折旧。',
 'MU':'HBM和存储盈利弹性及现价；周期较强，低Forward PE不自动形成永久保护。',
 'META':'广告现金流与AI推荐/广告转化形成较直接的价值回收；资本开支、广告周期及监管是风险。',
 'GOOGL':'搜索、YouTube、云与TPU协同；需要证明AI搜索仍有经济利润，TTM利润有投资估值影响。',
 'AMZN':'AWS、广告和履约基础，AI算力及自研芯片增长；投入与承诺影响股东现金。',
 'AVGO':'定制AI芯片、网络及软件现金流；客户集中、负债和项目周期需控制。',
 'TSM':'先进制程与先进封装地位；持续投资与地缘尾部风险不能忽略。',
 'BABA':'电商现金基础、估值及云AI弹性；竞争补贴、资本分配和地缘风险仍显著。',
 'CRDO':'AEC和高速连接增长已有利润支持，跨代资格及光学机会扩大空间；客户集中和技术路线风险高。',
 'ASML':'EUV与设备服务地位；扩产需求、估值及出口政策影响回报。',
 'HTHIY':'电网设备、服务和日本IT基础，补足原名单的电力平台敞口；集团结构、预付、汇率与ADR需区分。',
 'NVT':'配电与机房设备增长、现金基础及平台扩展；并购出资、整合与估值要求提高。',
 'EME':'工程交付与现实经营盈利，现金转换比仅有订单更重要；工程成本、用工和项目延期仍可冲击。',
 'ADBE':'低估值、创意与文档订阅基础；因AI对原付费模式的替代风险降低优先级，保留价值修复可能。',
 'TEL':'连接、电力与工业客户基础，业务相对分散；汽车工业周期与AI实际收入占比是约束。',
 'APH':'连接器设计导入、制造能力和客户基础；AI内容量增长，同时面对高估值及并购回报要求。',
 'JBL':'AI服务器、机柜、电力和散热交付能力；薄利润率、营运资本及客户集中削弱保护。',
 'SNDK':'AI存储、企业SSD和NAND盈利弹性；与MU共享周期，保留低于核心平台的优先级。',
 'ET':'管网、合同及现金分配提供不同收入结构；AI传导间接，项目、杠杆及税务影响回报。'
}
cases=[('基准',12),('基准',36),('乐观',12),('乐观',36),('突破',12),('突破',36)]
def fmtp(x):
    if x is None:return '—'
    if abs(x)<.05:x=0
    return f'{x:+.1f}%'
def sh(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
headers=['公司','PE','Forward PE','近3个月','近半年','近一年','基准一年','基准三年','乐观一年','乐观三年','突破一年','突破三年','最新IV¹']
table=['|'+'|'.join(headers)+'|','|:--|'+'--:|'*12]
rows=[];checks=[];historical_changes=[];quote_changes=[]
for rank,t in enumerate(selected,1):
    c=cs[t];q=qs[t]['quote'];h=hs[t];iv=vi[t]
    assert 'error' not in h and q.get('regularMarketPrice'),t
    spot=q['regularMarketPrice']
    dt=datetime.fromtimestamp(q['regularMarketTime'],ZoneInfo('America/New_York')).date()
    assert str(dt)=='2026-09-09',(t,dt)
    assert q['currency']=='USD'
    assert sh(c['file']).lower()==c['source_sha256'].lower(),(t,'formal report changed')
    for pefield,epsfield in [('trailingPE','trailingEps'),('forwardPE','forwardEps')]:
        assert q[pefield]>0 and q[epsfield]>0
        assert abs(spot/q[epsfield]/q[pefield]-1)<.01,(t,pefield,'EPS scale')
    assert len(h['anchors'])==3
    for k,a in h['anchors'].items():
        assert abs(a['return']-100*(spot/a['close']-1))<1e-8
        prior=c['history']['anchors'][k]
        if abs(a['close']-prior['close'])>.0001:
            historical_changes.append({'ticker':t,'period':k,'old_anchor_close':prior['close'],'refreshed_anchor_close':a['close']})
    if any(abs(q[new]-c['quote'][old])>.005 for new,old in [('trailingPE','pe'),('forwardPE','forward_pe')]):
        quote_changes.append({'ticker':t,'old_pe':c['quote']['pe'],'new_pe':q['trailingPE'],'old_forward_pe':c['quote']['forward_pe'],'new_forward_pe':q['forwardPE']})
    scenarios={}
    for case,months in cases:
        z=next(v for v in c['cells'] if v['scenario']==case and v['months']==months)
        lo=(1+z['low']/100)*c['anchor_price']/spot*100-100
        hi=(1+z['high']/100)*c['anchor_price']/spot*100-100
        mid=(lo+hi)/2
        alternate=((1+(z['low']+z['high'])/200)*c['anchor_price']/spot-1)*100
        assert abs(mid-alternate)<1e-8 and lo<=mid<=hi
        scenarios[f'{case}_{months}m']={'low':lo,'high':hi,'midpoint':mid,'source_line':z['source_line'],'source_label':z['label']}
    if iv['iv_percent'] is not None:
        a=iv['call'];bid,ask=a['bid'],a['ask']
        assert iv['expiry']=='2026-10-16'
        assert 0<bid<=ask and (ask-bid)/((bid+ask)/2)<=.30
        assert abs(a['strike']/spot-1)<=.05
        assert 0<=(date(2026,9,9)-date.fromisoformat(a['last_trade_time'][:10])).days<=7
        assert 1<=iv['iv_percent']<=300
    else:assert t=='HTHIY',(t,'unexpected missing IV')
    row={'rank':rank,'ticker':t,'name':names[t],'price':spot,'price_date':str(dt),'pe':q['trailingPE'],'forward_pe':q['forwardPE'],
       'history':h['anchors'],'scenarios':scenarios,'iv':iv,'selection_reason':reasons[t],
       'market_collected_at':qs[t]['collected_at'],'report_path':c['file'],'report_date':c['report_date'],'report_anchor_price':c['anchor_price'],
       'report_sha256':c['source_sha256'],'quote_source_url':'https://finance.yahoo.com/quote/'+t+'/key-statistics/','history_source_url':h['source_url']}
    rows.append(row)
    values=[f'{rank}. **{t}** {names[t]}',f'{q["trailingPE"]:.2f}',f'{q["forwardPE"]:.2f}']
    values.extend(fmtp(h['anchors'][k]['return']) for k in ['3m','6m','1y'])
    values.extend(fmtp(scenarios[f'{case}_{months}m']['midpoint']) for case,months in cases)
    values.append('—' if iv['iv_percent'] is None else f'{iv["iv_percent"]:.1f}%')
    assert len(values)==13
    table.append('|'+'|'.join(values)+'|')
    checks.append({'ticker':t,'dated_quote_ok':True,'pe_eps_scale_ok':True,'formal_hash_ok':True,'history_recalculated':3,'scenario_midpoints_checked':6,'iv_valid_or_documented_missing':True})

assert len(rows)==len(set(selected))==20
table_md='\n'.join(table)
(OUT/'仅总表.md').write_text(table_md+'\n',encoding='utf-8')
old_selected=json.loads((ROOT/'备份/AI乐观情景_增长与下行保护20家公司_2026-09-09/20家公司合并数据.json').read_text(encoding='utf-8'))
old_tickers=[r['ticker'] for r in old_selected['rows']]
added=[t for t in selected if t not in old_tickers];removed=[t for t in old_tickers if t not in selected]
assert set(added)=={'CRDO','HTHIY','NVT','EME'} and set(removed)=={'NTAP','IBM','SMCI','BDC'}
intro='''# 复核后的AI投资前20家公司

这份名单以AI产业乐观发展为前提，综合考虑已形成的现金流、融资承压能力、AI价值捕获、现价要求及成长空间；顺序为主观综合配置优先级，不按突破情景中点机械排序，不代表唯一数学最优解或仓位比例。

相对上一版，新增CRDO、HTHIY、NVT、EME，移出BDC、IBM、NTAP、SMCI。CRDO提高AI连接成长敞口；HTHIY补充电网和多业务现金基础；NVT补配电设备；EME补工程交付和现金盈利。Adobe因AI替代风险降低优先级，仍保留估值修复机会。CRWV/IREN等仍具有投资可能，但本名单优先兼顾融资和现金保护，没有把突破上行自动视为高胜率。

价格为2026年9月9日美股常规时段收盘，PE/Forward PE于当日23:35 PDT前后刷新，期权于23:37 PDT前后核查Cboe最新可取得的延迟数据。HTHIY收盘端点由33.33更新为33.35美元，相关涨幅及情景回报同步重算。

PE以倍计，其余数值为百分比。基准、乐观、突破列均为原模型区间上下限的算术平均；三年列为累计回报，不是年化，也不是概率加权预期收益。

'''
notes='''

**口径与来源**

1. 最新IV¹：统一采用2026年10月16日到期、最接近收盘价且通过质量筛选的看涨期权，显示Cboe来源年化隐含波动率，按9月9日计算剩余37个日历日。它不是IV Rank、历史波动率、IV30或Call/Put均值。本次统一改用Cboe，与前版Yahoo来源IV有方法和合约筛选差异，差值不能当成当日IV涨跌。HTHIY为OTC ADR，未取得同一证券的可比期权链，以“—”表示；未使用日本普通股的期权或历史波动率代替。
2. IV筛选：执行价距收盘不超过5%；有效正买卖价；相对价差不超过30%；成交量与未平仓量之和大于零；最近成交不超过7个日历日；来源IV处于1%至300%。采集时间不是合约报价时间，来源文件时间和最近成交时间分别保留。TEL使用200美元执行价，距现价约2.3%，因为更近的合约未通过全部筛选。
3. 夜间Yahoo期权刷新返回了零买卖价和异常小的IV，该批数据仅保留在原始核查文件中，未用于主表。Cboe主表所选19份合约全部通过上述筛选。
4. 历史涨跌按2026-06-09、2026-03-09、2025-09-09的拆股调整收盘价与当前收盘价计算，不含分红、税费；本次重新拉取了全部20家的价格历史并重算。估值字段已刷新；与前版展示的差异以本次逐行数据为准。
5. 六个情景列使用9月8—9日原报告的条件回报，先按同一收盘买价换算，再取上下限平均。没有重新估计经营或终值。目标日期保留原报告起点最多一天的差异；原模型中的现金分配处理沿用原报告。
6. PE/Forward PE为Yahoo最新来源值，已核对与来源EPS及股价的数量关系。Forward EPS的预测年度、GAAP/调整后口径及底层更新时间不完全统一。HTHIY是美元ADR口径，并非日立能源子公司；不能把表中PE直接与未经换汇的日元EPS拼接。

'''
detail=['**入选理由与主要约束**\n']
for r in rows:
    p=Path(r['report_path']).as_posix()
    detail.append(f'- **{r["ticker"]}**：{r["selection_reason"]} [原情景报告](/{p})')
sources=['\n**逐行资料来源**\n','|公司|行情与历史|期权合约|IV%|执行价|最后成交时间（来源原文）|','|---|---|---|---:|---:|---|']
for r in rows:
    t=r['ticker'];v=r['iv']
    urls=f'[Yahoo估值]({r["quote_source_url"]})、[日线]({r["history_source_url"]})'
    if v['iv_percent'] is None:
        sources.append(f'|{t}|{urls}|未取得可比链|—|—|—|')
    else:
        a=v['call']
        sources.append(f'|{t}|{urls}|[{a["option"]}]({v["source_url"]})|{v["iv_percent"]:.2f}|{a["strike"]:g}|{a["last_trade_time"]}|')
sources.append('\n[完整数据与计算边界](./前20家公司完整数据.json)保存区间上下限、单点计算、价格锚点、原报告路径与哈希；展示主表仅显示单点。')
(OUT/'前20家公司总表.md').write_text(intro+table_md+notes+'\n'.join(detail)+'\n'+'\n'.join(sources)+'\n',encoding='utf-8')
payload={'asof':'2026-09-09','created_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'selection':'AI乐观下兼顾增长和下行保护的主观组合优先级','added':added,'removed':removed,
 'midpoint_definition':'After rebasing original conditional return endpoints to refreshed close, arithmetic mean (low+high)/2. Not probability weighted expected return.',
 'rows':rows}
(OUT/'前20家公司完整数据.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
validation={'companies':20,'columns':13,'history_points':60,'scenario_midpoints':120,'source_iv_valid':19,'iv_missing':['HTHIY'],'checks':checks,
 'added':added,'removed':removed,'historical_source_changes':historical_changes,'updated_pe_fields':quote_changes,'no_displayed_ranges':not re.search(r'[～—].*[+−-]?\d.*%',table_md.replace('|—|','||'))}
(OUT/'校验记录.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(table_md)
print('VALIDATION',json.dumps({k:v for k,v in validation.items() if k not in ['checks','historical_source_changes','updated_pe_fields']},ensure_ascii=False))
print('HISTORY_SOURCE_CHANGES',historical_changes)
