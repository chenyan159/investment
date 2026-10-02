from pathlib import Path
import json, re, hashlib, sys
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from zoneinfo import ZoneInfo
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('D:/drive/Investment'); OUT=Path(__file__).resolve().parent
PREV=ROOT/'备份/16份排序结果横评_2026-09-09'
local=json.loads((OUT/'候选公司本地证据.json').read_text(encoding='utf-8'))
market=json.loads((OUT/'最新市场数据汇总.json').read_text(encoding='utf-8'))
cboe=json.loads((OUT/'Cboe期权IV核验.json').read_text(encoding='utf-8'))
prior=json.loads((PREV/'交集与选择及历史核验.json').read_text(encoding='utf-8'))
manifest=json.loads((PREV/'16份结果清单.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256(Path(v['report']).read_bytes()).hexdigest()==v['sha256'] for v in manifest.values())

# Manually identified twelve-month base and optimistic rows in the formal
# September 8/9 company models. The breakout scenario is never substituted.
spec=[
('ADBE',[373,490],[514,694],458,461,'首选；关注9月10日财报风险','01、02、04、07现金；E04-B、E05-A/B',
 '现金收益支持修复，多个估值思路交叉支持，现价仍能容纳一部分经营失误。',
 'TTM自由现金流10.280B减SBC2.029B后，经济现金约8.251B，相对约101.3B市值为8.1%；一年基准价值明显高于现价，且不要求全部新AI产品成功。旧N02和02均曾把它排在第1；本轮07现金与输入对照也给现价支持，因此支持跨越了单一算法。',
 '核心风险是专业创作收费权与续约受到生成式AI侵蚀，经济现金的低倍数可能合理。9月10日财报尚未公布，当前预测仍基于Q2；今天的事件风险不能用一年上行空间抹掉。',
 '关注付费续约、有机ARR与单位收费；如果只见免费用户增长、付费与现金走弱，应下调。约220—231美元的较严格研究边界有更多余量，但不是固定买点。'),
('MU',[1096,1374],[2060,2664],532,535,'成长首选；周期风险高','01、02、04、06G/E、07、N03',
 '交付、巨额现金和客户协议同时存在，是成长名单里经营支持最完整的对象。',
 'FY26Q3收入41.456B、GAAP净利28.243B、经营现金25.39B已有正式披露；成长、现金和增量证据三个视角均靠前。旧02曾列第22，本轮升至核心条件组；这是依据新经营更新，而不是宣称它历史上就是所有方法的头部。',
 '6.63倍Forward PE用了约155美元供应商前瞻EPS，不能当中周期利润。高价格、高利润和低PE可以同时意味着周期风险；增产、折旧、续约价格、稀释共同影响价值。',
 '9月30日财报重点看FY27量价、合同覆盖和现金；仅兑现旧季度指引不构成新的超预期。接受显著波动才适合，不能按低PE当防守仓。'),
('ET',[26.09,34.13],[32.97,42.46],381,384,'现金与成长候选；回报较平衡','01双判断、06F；02半年',
 '收费网络、现金分配与已投资项目兑现，比单纯AI概念更能解释普通股回报。',
 '旧01第1、旧N02第7；本轮01半年基准研究仍第1。最近季度分配0.34美元，年化1.36美元，相对21.68美元约6.27%；一年基准价格26.09—34.13尚未把分配加进去。收益来自现有网络收费及扩建兑现，不要求全面科技化重估。',
 '成长CapEx、债务和商品优化利润回落会消耗现金，较弱长期持续性解释仍可能使价值低于现价。ET是LP普通合伙单位，税后分配与普通公司股息不能直接等同。',
 '跟踪2027资本预算、项目起租、正常化后的单位现金；现金分配不构成保本。本文价格与收益均未扣个人税。'),
('MSFT',[433.7,646.4],[665.8,1037.3],410,413,'质量优先；现价回报余量一般','01、02、07现金、E04-B、E05-B半年',
 '成熟软件付费与云业务有相互支持，历史和新结果的交叉证据都较强。',
 '旧N02第6、旧02第7，旧窗口股价回报约28.04%；本轮01三个月基准研究第1，BCDE赔率现价通过。FY26云收入超过214B、近90%来自前沿模型公司之外，比依赖少数AI实验室的需求结构更有支撑。',
 '近三个月已涨21.87%；一年DCF工作值约547，对现价价格回报约11.3%，合理估值下沿仍低于现价。CapEx、融资租赁和设备更新使利润增长快于股东现金；不能称无争议低估。',
 '约10%回报取向可谨慎考虑，追求显著更高超额回报则应要求更低买价或更好的现金转换。440—465美元是01的条件研究带，经营变化时必须更新。'),
('BABA',[128.7,171.3],[231.7,296.5],511,514,'高风险修复候选；尚非确定买入','01赔率、02、06F/E、N05',
 '云增长与电商修复有较大上行，价格相对基准价值有差距。',
 '本轮01赔率、02兑现和06性价比均保留条件候选；一年基准128.7—171.3美元对109.40美元有上行。现金与库务资产可以承担一段投入期，使它与靠持续股权融资维持运营的早期AI项目不同。',
 '6月季度公司FCF为−44.670B人民币；8月配股使现金和股数同时增加。应用亏损、云设备更新和电商补贴可能拖延现金转正；VIE、汇率和资本配置风险也不能用低Forward PE消除。',
 '原单公司研究仍中性，我保留高优先级的风险修复资格，不把它升为核心买入。95—105美元且净CMR、单位云现金回收、应用亏损至少两项改善，是更有依据的复核条件。'),
('PNR',[55.93,76.86],[72.74,99.63],477,480,'修复候选；需承受继续下修','01双判断、02、06F、N05',
 '估值压低后，渠道去库存与正常利润恢复有投资意义。',
 '旧N02第9、旧01第7、旧04第2；本輪01与02再次保留。三个月跌22.87%，Forward PE约11.13倍；一年基准工作值64.71美元，加分配后对现价的回报条件较原研究价58.62美元改善。',
 '下跌包含真实业绩恶化：Q2销售下降17%，公司将约170M美元影响归于泳池渠道去库存；不是所有跌幅都属于误价。Taco约1.4B美元收购及融资增加现金压力。',
 '观察连续补货周期、终端销量、回款与偿债，不只看库存下降。50—51美元且核心经营未进一步受损更有余量；现价只能作为谨慎修复参与，不能当安全边际很厚。'),
('ST',[40.74,51.93],[57.67,73.90],517,520,'边界型现金修复候选','01、02、06F；E05-A现价',
 '存量传感器现金与降债是主要价值来源，AI新产品只作额外机会。',
 '旧01第2；本轮E05-A给现价可考虑，门槛42.3美元，现价42.03美元仅略低。H1自由现金流291M美元、已用400M现金回购约406M债务，说明修复与去杠杆已有实际动作。',
 'H1 FCF增量约72%来自营运资本改善和较低CapEx，不能直接外推。TTM PE67.79与Forward PE10.26差距巨大，所需利润恢复仍应核验；42.3的门槛并无宽价格保护。',
 '正常化年经济现金至少约0.50B且不能靠持续压研发/维护实现。更严格01研究带35—38美元；现价结论仅边界型，不能只凭数据中心定点升级。'),
('SMCI',[51.64,62.71],[82.79,101.69],450,453,'高风险候选；资金条件优先','02、06G、01半年赔率；09/N05辅助',
 '低估值与系统交付有较大上行，但融资和回款决定普通股能否兑现。',
 '旧02第3、旧01第21，旧窗口上涨约43.13%；本轮02和成长视角仍保留。FY26Q4经营现金已转为+747M美元，是全年巨额流出之后的有用变化，一年基准价值也高于38.93美元。',
 'FY26全年CFO仍约−6.810B美元、FCF约−6.972B；不可取消采购和可取消销售不对称，库存、应收、资本稀释可能击穿静态估值。一次季度转正尚不能证明现金问题解决。',
 '先看连续回款、库存变现和实际可提款资金。只有能承受重大损失的策略才考虑，稳健资金不因7.31倍Forward PE买入；不能把它与MSFT的现金质量等量比较。'),
('TEL',[165.5,254.5],[209.5,323.7],422,425,'优先条件候选；现价分歧未解决','E04-B、E05-A/B；01研究',
 '连接器跨代能力和估值受到多种方法支持，但现金模型没有同等支持现价。',
 '旧N02第3、旧04第5、旧02第9；本轮多个输入对照现价通过，属于最强跨方法候选之一。Q3销售增14%、EPS增19%、年初至今经营现金约3.0B美元，经营并非空泛技术故事。',
 '单公司一年现金DCF工作值约201美元，低于现价204.68；E05-A半年盈利倍数价值216—273美元更积极。两者分歧来自现金税、再投资和利润持续性，不能用多数投票裁决，也不应机械平均。',
 '优先等现金转换上修或170—180美元附近且经营保持。若采用盈利倍数参与，必须明确承担更持久成长和较低资本要求的假设，不能宣称已有一致安全边际。'),
('META',[545,751],[828,1198],364,367,'条件候选；AI变现强于现金恢复','07现金、06G研究、E05-A/B',
 '广告已有可量化的AI收益，经营机制比纯模型收入故事更成熟。',
 'Q2广告展示增14%、价格增12%、总收入增28%；AI改善广告效率可以直接转化为既有客户预算。相对只靠新应用收费的公司，更容易检验收入归属，本轮收入/现金研究与独立估值对照均关注。',
 '同季经营利润下降8%，CapEx含融资租赁本金31.08B美元，FCF仅0.784B。低Forward PE没有消除资本强度问题；一年现金工作值633美元仍低于653.69美元。',
 '540—560美元或广告利润与资本效率同时上修，才更有吸引力；新模型发布或免费用户增长不足以翻转。'),
('DOV',[167.7,218.2],[212.6,279.2],419,422,'条件候选；优先核现金与净份额','01、04、E04-A、E05-A',
 '成熟现金业务叠加液冷连接与换热机会，较符合历史有效方法的思路。',
 '旧04第19、旧N02第29；本轮01基准及极简判断均保留，E04-A研究优先靠前。比押注单一液冷新公司更有成熟业务支撑，前瞻倍数也较温和。',
 '液冷总投资不能全部归属Dover；订单定义不扣以前订单取消，CST的订单增长未同步变为利润。并购成本、工厂效率和长期更新仍使一年现金工作值约189美元，未明显高于现价。',
 '165—175美元或交付、利润、现金一起改善时复核。表中已从原权益值扣除0.525美元应收股息，统一为纯股票价格。'),
('ASML',[1480,1964],[2150,2903],548,551,'技术瓶颈候选；需价格或持续性证据','01基准承载；N05关注',
 '稀缺工艺设备与装机服务的收费权清楚，技术优势具有较长验证历史。',
 '本轮01保留基准条件候选。公司Q2销售9.326B欧元、毛利率54%，上调全年收入指引至43—45B欧元；低NA EUV及DUV浸没式设备2027产能计划增加30%，有现实客户投资支撑。',
 '59.89倍TTM PE与28.76倍Forward PE之间要求很大盈利增长；技术采用不等于同年度验收和现金，出口许可、客户CapEx和High-NA经济性仍能改变回报。',
 '约1500—1550美元或客户验收、现金与增长持续性超过基准后复核；现价只有宽区间上行，不能把乐观2150—2903当必然目标。'),
('DKILY',[12.82,15.72],[16.66,20.26],632,635,'全球工业修复候选；数据覆盖弱','01双判断、04半年、06F',
 '商用空调、渠道和服务构成存量基础，利润率修复有验证路径。',
 '本轮01、04与06F交叉保留；经营分散于多地区空调、商用系统、服务和材料，有较成熟的客户和资产基础，不依赖一项AI新业务成功。',
 '美国住宅、价格传导与日元汇率会共同影响美元ADR回报。前瞻PE未取得同口径供应商数据，OTC证券没有取得可用期权IV；原项目部分P/S与EV字段还有跨币种风险，不能据其极低值选股。',
 '约11.7—12.8美元且利润、资本效率未受损时更有研究价值。1普通股=10 ADS，表中目标与现价均为美元DKILY；缺失Forward PE与IV不补造。'),
('BDC',[111.49,137.09],[200.73,244.89],465,468,'小型工业候选；并购现金需核验','06F、E05-A、E04-B',
 '工业连接与数据网络的经营改善有基础，利润兑现存在上行。',
 '旧01第12、旧02第11、旧04第24；本轮性价比与独立估值对照保留。前瞻PE约11.72倍，具备工业连接、数据网络产品及生产订单，不是无收入技术期权。',
 '一年基准工作值123.44美元对117.78美元只有约4.8%价格空间；并购整合、债务和费用消耗现金。乐观200—245需要利润率、复购和降债共同改善，不能只看调整EPS增厚。',
 '约97—108美元或更强现金/持续性证据时复核；现价仍高于有充分补偿的工作买价。'),
('NVDA',[183.07,213.53],[297.62,355.50],624,627,'核心成长观察；现价估值解释分歧大','06G、07、01赔率、02、N03、E05-A/B',
 '生态、系统和网络优势使它仍是高质量成长候选，但高共识不等于便宜。',
 '13份有收益选择功能的报告全部将其列为重点；旧04第9。FY27Q2收入96.221B美元、同比增106%，平台与实际交付很强。独立盈利倍数研究明显比单公司现金模型积极，这一分歧应保留。',
 '同季CFO24.077B对净利59.688B，现金与利润不同步；客户应收、库存、供货承诺及支持安排需要一起看。183—214的现金基准依赖2030后利润租金收敛，275—335的持久平台替代解释也有经济可能，但尚非已证实基准。',
 '优先检验多代复购、ASIC迁移后的净价和现金回收，或等待更低价格。现价不升为现金价值核心买入；不能反过来把低DCF当成一年必跌预测。'),
('SNDK',[1342,1721],[3004,4060],368,371,'高弹性存储候选；不把低PE当防守','07收入/现金、N03、06G、01半年赔率',
 '企业存储、真实利润与NBM协议形成上行机制，合同延续是主要分歧。',
 'Q4收入8.97B美元，环比增51%；公司披露新增NBM协议与最低财务保障框架。它比纯现货周期有更强现金可见性，本轮增长和增量证据视角均靠前。',
 'Q4增长约三分之二来自价格；Forward PE6.66使用峰值附近前瞻利润。基准1342—1721低于现价1764.17，但NBM较持久替代解释1984—2599可以转正；不能把全部未覆盖市场也当保价长约。IV30约75.7%体现很高的不确定性。',
 '合同覆盖、续约价格和合资资本投入后的现金比单季EPS更关键；目前排在MU之后，不以3004—4060乐观范围支持无条件买入。'),
('ALLE',[125.9,170.9],[158.2,217.6],440,443,'优质工业候选；价格尚需余量','04半年、E05-A',
 '建筑规格、维护和电子化构成较持久的需求，现金风险较易检验。',
 '旧N02第16、旧01第25；本轮04及E05-A保留。规格黏性和维护需求支持成熟业务盈利，电子化提供可跟踪的增量，不需要把公司整体变成订阅软件。',
 '正常现金价值工作点未提供充分回报；TTM与前瞻利润的改善不代表所有利润都能分配。国际执行、收购、ERP和回款会影响结果，新增电子收入还可能替代机械收入。',
 '约125—131美元或电子净增量、国际利润及现金同时上修后复核。当前151.73美元仅接近E05-A较宽松的150美元条件，不能视作厚安全边际。'),
('AEP',[116.01,141.53],[135.54,165.78],441,444,'防守性候选；不承担高回报主任务','01基准、04半年',
 '受监管资产增长和股息支持较稳定的回报来源，能减少单一AI预算暴露。',
 '旧04第13、旧01第26；本轮01基准和04保留条件候选。增长通过在运资产、监管回收和每股盈利兑现，比用数据中心意向GW直接估收入更可核验。',
 '大量资本开支需要权益融资；公司规模增长可能被新增股数稀释。现价下正常回报中枢不高，不能因为IV30约19.6%就把它当高赔率股票。',
 '约109—119美元或资本回收、获准收益与融资股数共同改善时更合适。它是组合风格上的防守备选，不能代替项目超高回报目标。'),
('TSM',[304.5,384.1],[452.5,576.6],520,523,'先进制造候选；现价需更强现金','06G、07、N03、02半年、E05-A/B',
 '领先制程和封装是实际产业瓶颈，客户与交付证据强。',
 '本轮成长、收入、现金和增量证据方法都关注，技术护城河与实体产能可核验，1 ADS=5普通股的价格口径已统一。',
 '一年现金基准304.5—384.1低于435.36美元；2027基准FCF约47.2B、核心CapEx约73B，高盈利与重投入并存。海外厂成本、折旧、汇率及地缘约束不能靠19.86倍Forward PE解决。',
 '约269—338美元或可验证的资本效率、净利润持续性显著好于基准后复核；当前仍是优质企业的价格条件候选。'),
('AVGO',[260.7,326.1],[404.2,514.6],373,376,'AI平台候选；客户资本风险压后','06G、07、N03、02半年、E05-A/B',
 '定制计算、网络和软件现金有互补价值，增长来自真实客户项目。',
 '9月2日Q3披露AI半导体收入16.7B美元、同比增221%；下一季度集团收入指引34.8B。收入与经营证据支持继续跟踪，本轮多种成长与现金视角均入选重点。',
 '一年现金基准260.7—326.1低于364.38美元；整机/系统化后毛利结构、客户集中、应收与支持承诺改变资本风险。单一大客户项目成功不等于整股已经便宜。',
 '约257—266美元工作研究带或现金与多年净收费显著上修后再评估；乐观404—515美元也不是无条件目标。'),
]

def filelink(p,label=None,line=None):
    p=Path(p).as_posix();return f'[{label or Path(p).name}](</{p}{":"+str(line) if line else ""}>)'
def n(x):return f'{Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP):,f}'.rstrip('0').rstrip('.')
def band(x):return '—'.join(n(v) for v in x)
def pct(x):return f'{x:+.2f}%'
records=[]
for rank,(s,base,bull,bl,ol,stance,lists,why,pro,con,trigger) in enumerate(spec,1):
    l=local[s];q=market[s]['quote'];r=market[s]['return_3m'];p=r['end_close']
    assert r['start']=='2026-06-09' and r['end']=='2026-09-09'
    assert abs(q['regularMarketPrice']-p)<.02
    assert l['sha256']==hashlib.sha256(Path(l['report']).read_bytes()).hexdigest()
    rawlines=Path(l['report']).read_text(encoding='utf-8').splitlines()
    for ln,label,values in [(bl,'基准',base),(ol,'乐观',bull)]:
        row=rawlines[ln-1];assert label in row and '2027-09' in row,(s,ln)
        cells=[z.strip() for z in row.split('|')]
        expected_values=None
        for cell in cells:
            parts=re.split('[—～~–]',cell.replace(',',''))
            if len(parts)==2:
                try:nums=list(map(float,parts))
                except ValueError:continue
                if nums==values:expected_values=nums
        assert expected_values is not None,(s,ln,values,row)
    target=re.search(r'2027-09-\d\d',rawlines[bl-1]).group()
    adjustment=.525 if s=='DOV' else 0
    stockbase=[float(Decimal(str(v))-Decimal(str(adjustment))) for v in base]
    stockbull=[float(Decimal(str(v))-Decimal(str(adjustment))) for v in bull]
    iv=cboe[s].get('underlying',{}).get('iv30')
    if iv:
        assert 1<iv<300 and abs(cboe[s]['underlying']['close']-p)<.02
    pe=q.get('trailingPE');fpe=q.get('forwardPE')
    if pe:assert abs(pe-p/q['trailingEps'])<.05
    if fpe:assert abs(fpe-p/q['forwardEps'])<.05
    oldranks={x['list_id']:x['old_top30'].index(s)+1 for x in prior['historical'] if x['list_id'] in ['N02','01','02','04'] and s in x['old_top30']}
    current_focus=[k for k,v in prior['focus'].items() if s in v and k not in ['N02','E06-A','E06-B']]
    y_reports=sorted({v['report_id'] for v in prior['views'].values() if s in (v.get('y3') or []) or s in (v.get('y6') or [])})
    records.append({'rank':rank,'ticker':s,'name':l['snapshot']['公司名称'],'stance':stance,'main_list_evidence':lists,
        'short_reason':why,'supporting_case':pro,'countercase':con,'reassessment':trigger,
        'price':p,'price_date':r['end'],'pe_ttm_vendor':pe,'forward_pe_vendor':fpe,
        'quote_retrieved_at':market[s]['retrieved_at'],'ttm_eps_vendor':q.get('trailingEps'),'forward_eps_vendor':q.get('forwardEps'),
        'price_return_3m_pct':r['price_change_pct'],'return_start':r['start'],'start_price':r['start_close'],
        'target_date':target,'base_raw_equity_value':base,'optimistic_raw_equity_value':bull,
        'receivable_dividend_removed':adjustment,'base_stock_price_range':stockbase,'optimistic_stock_price_range':stockbull,
        'base_price_upside_pct':[(v/p-1)*100 for v in stockbase],
        'iv30_pct':iv,'iv_source':'Cboe delayed quotes, data.iv30' if iv else None,
        'iv_provider_timestamp_unzoned':cboe[s].get('provider_timestamp_unzoned'),
        'iv_retrieved_at':cboe[s].get('retrieved_at'),'iv_url':cboe[s]['url'],
        'current_return_report_focus_count':len(current_focus),'current_return_report_focus_lists':current_focus,
        'original_current_price_choice_reports':y_reports,'old_top30_ranks':oldranks,
        'company_report':l['report'],'company_report_sha256':l['sha256'],'base_source_line':bl,'optimistic_source_line':ol,
        'history_url':market[s]['history_url'],'quote_url':market[s]['statistics_url']})
assert len(records)==len({x['ticker'] for x in records})==20
(OUT/'20家公司_数据与证据.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')

text=[]
def add(s=''):text.append(s)
add('**20家公司投资优先级、估值与一年情景预测**')
add()
add('研究时间：2026-09-10（America/Los_Angeles）。最新完整美股交易日为2026-09-09；20家价格统一用该日正常交易收盘。本文是一次性分析，不修改正式研究、方案或队列。')
add()
add('**当前结论：ADBE、MU、ET的现价投资依据最完整；MSFT质量更强，但回报余量较小。BABA、PNR、ST、SMCI是应单独承担风险的修复候选。其余12家保留在前20优先名单中，需要价格或经营证据改善。现有证据不支持把这20家都称为同等强度的现价买入。**')
add()
add('这是一份投资吸引力与后续配置优先级的定性排序，不是等权组合、买卖指令或收益概率模型。前8也不代表同一风险等级：其中BABA仍缺现金回收证据，SMCI仍有资金断点风险；排名不能替代这些条件。关注窗口沿用项目未来3—6个月，但下表估值严格来自一年情景，未将一年价值当成3个月成交预测。')
add()
add('**历史方法怎样影响本次筛选**')
add()
add('历史窗口冻结为2026-07-13收盘或07-14复权开盘，持有至09-04最后可用复权收盘。仅约39个收益间隔，非完整3/6个月验证，也非反复修订后的新版本业绩。按旧次序机械等权截取、未扣成本。')
add()
add('|旧方法|Top20收盘口径|Top20次日开盘口径|Top30收盘口径|本次使用方式|')
add('|---|---:|---:|---:|---|')
histuse={'N02':'优先采用现金、生存与普通不利解释审查；新U08是风险审查，不能当旧质量排名直接继承。','01':'优先看赔率和基准现金承载，保留公司级反证。','04':'偏重普通经营兑现能否支撑价格，避免只靠大幅乐观。','02':'主要相信头部兑现准备度；旧Top10达+6.09%，扩到Top20仅+0.54%，不宜整体高权重。'}
for k in ['N02','01','04','02']:
    h=next(x for x in prior['historical'] if x['list_id']==k)
    add(f'|{k} {h["method_name"]}|{pct(float(h["width_sensitivity"]["20"]["close"])*100)}|{pct(float(h["width_sensitivity"]["20"]["open"])*100)}|{pct(float(h["top30_return"])*100)}|{histuse[k]}|')
add()
add('同期SPY为+2.81%/+2.57%（收盘/次日开盘），QQQ为+1.01%/−0.17%。因此这里的“过去表现好”是相对有限证据：旧N02头部较有力，01/04并未全面胜过宽基。不给四种方法人为赋予精确胜率，也不把这20家公司按今天的名单倒填成旧回测。')
add()
add('16份结果中有3份仅承担风险审查；其余13份也共享不少输入。01/E04、04/E05的对照版本作同一方法族的佐证，07内部收入/现金也不能算两次独立投票。“重点30出现”只代表关注；条件集合不等于现价买入，旧方法名也不证明新模型有效。先用这些证据找候选，再检查现金、资本、价值与反解释。')
add()
add('历史出处：'+filelink(PREV/'00_16份结果横评与迭代方向.md','16份横评与旧回测',85)+'；'+filelink(PREV/'交集与选择及历史核验.json','历史数值与集合')+'。本次再次核对16份报告哈希，均与9月9日横评快照一致。')
add()
add('**20家数据表**')
add()
add('- PE及Forward PE：9月10日凌晨重新读取Yahoo quote/info，采用其TTM/forward字段；逐家公司复算P/EPS，均与字段在0.05倍内一致。供应商未提供逐字段财报期/预测期时间戳，Forward PE不能称为精确研究日起NTM。部分TTM EPS已异于9月9日金融快照，表中采用本次采集值；不擅自把这种变动归因于新财报。')
add('- 三个月：2026-06-09收盘至2026-09-09收盘的价格变动，不含分红。原始日线和复权序列均保留；这20家窗口内未发现拆股事件，价格与总回报不混用。')
add('- 一年：来自最新单公司报告“基准/正常兑现”和“乐观/超预期”的12个月价格区间，目标日为2027-09-08或09。它们是经营路径成立时的条件合理股价，不是概率加权目标、卖方目标或保证成交预测，也不是“突破”情景。所有价格为美元/所列证券；分红不计入股价。DOV原权益值含0.525美元股息应收，本表已扣。')
add('- IV：采用本次获取的Cboe标准30天隐含波动率IV30（年化百分数），不是单一期权、IV Rank或历史波动率。Cboe定义为平值隐波、30天插值期限：[字段说明](https://datashop.cboe.com/Documents/Cboe_OptionSentiment_Specs.pdf)。19家基础收盘价与Yahoo匹配；供应商包时间戳是9月10日但未标时区，原样保留，不宣称是9月10日盘中行情。')
add('- DKILY的Forward PE及IV未取得可核验值，写NA；不能将缺失视作0。DKILY为OTC非保荐ADR，1普通股=10 ADS，币种差异与流动性应另查。')
add()
header='|序|公司|现价$|PE|Forward PE|近3个月|一年基准$|一年乐观$|IV30|'
add(header);add('|---:|---|---:|---:|---:|---:|---:|---:|---:|')
for x in records:
    iv_text=f'{x["iv30_pct"]:.1f}%' if x['iv30_pct'] else 'NA'
    add(f'|{x["rank"]}|{filelink(x["company_report"],x["ticker"],x["base_source_line"])}|{n(x["price"])}|{n(x["pe_ttm_vendor"]) if x["pe_ttm_vendor"] else "NA"}|{n(x["forward_pe_vendor"]) if x["forward_pe_vendor"] else "NA"}|{pct(x["price_return_3m_pct"])}|{band(x["base_stock_price_range"])}|{band(x["optimistic_stock_price_range"])}|{iv_text}|')
add()
add('价格/PE/收益原始抓取：'+filelink(OUT/'最新市场数据汇总.json','Yahoo核验记录')+'；IV字段、时间与链数据：'+filelink(OUT/'Cboe期权IV核验.json','Cboe核验记录')+'。每个公司名链接到对应一年基准原文，乐观原文行与数据源URL保存在'+filelink(OUT/'20家公司_数据与证据.json','结构化明细')+'。')
add()
add('**逐家公司：榜单出处、入选理由与实际判断**')
add()
for x in records:
    add(f'**{x["rank"]}. {x["name"]}（{x["ticker"]}）—{x["stance"]}**');add()
    add('榜单来源：'+x['main_list_evidence']+'。13份收益类报告重点30出现'+str(x['current_return_report_focus_count'])+'次；这是关注计数。'+('旧Top30名次：'+ '、'.join(f'{k}第{v}' for k,v in x['old_top30_ranks'].items())+'。' if x['old_top30_ranks'] else '在本次重点参考的旧N02/01/02/04前30中均未出现，不称其有公司级旧榜背书。'))
    add()
    add(x['supporting_case']);add();add('最强反证与限制：'+x['countercase']);add();add('本次取舍：'+x['reassessment'])
    add()
    s=x['ticker'];support_links=[]
    for k in x['current_return_report_focus_lists']:
        if k not in ['01','02','04','06','07','E04-B','E05-A','E05-B','N03']:continue
        lines=Path(manifest[k]['report']).read_text(encoding='utf-8').splitlines()
        anchors=[i for i,t in enumerate(lines,1) if t.startswith('###') and re.search(r'(?<![A-Z])'+s+r'(?![A-Z])',t)]
        support_links.append(filelink(manifest[k]['report'],k,anchors[0] if anchors else 1))
    add('可追溯原文：'+'、'.join(support_links[:5])+'；'+filelink(x['company_report'],'一年基准',x['base_source_line'])+'、'+filelink(x['company_report'],'一年乐观',x['optimistic_source_line'])+'。')
    add()

add('**多榜支持仍不足以进入更高投资等级的几个案例**');add()
add('EME没有入选前20：虽然E04-B给过半年现价可考虑，新单公司基准一年550—673美元低于754.29美元；要给更高排序，需证明更持久的现金增长。NTAP的基准129.6—162美元也低于184.74美元。它们是好业务，但本次缺少把当前估值冲突裁决为便宜的证据。CRDO/ALAB高度受关注，包含风险和前沿研究；近端现金与估值门槛并未因关注次数增加而通过。')
add()
add('这些未入选判断是本轮相对取舍，并非已证明它们未来涨幅较低。新单公司模型普遍采用长期现金折现，一年价值仍对2030年以后持续性敏感；若其过早收敛增长，可能继续错过平台型赢家。反过来，固定高PE也可能把客户融资、现金投入和竞争反应遗漏。因此本报告保留NVDA、SNDK等的持久平台/长约替代解释，未把低DCF直接写成做空或必跌。')
add()
add('**对这20家的三个主要认识**');add()
add('第一，多榜共识最强与现价价值最明确并不相同。MU和NVDA均出现在13份收益类重点30，前者的普通现金路径仍有价格上行，后者需要在租金收敛和持续平台之间作实质判断。TEL在旧有效榜与新对照中都靠前，仍不能略过一年现金工作值约201美元的反证。')
add()
add('第二，历史收益胜出不应变成追逐近期涨幅。MSFT旧窗口涨约28.04%、近三个月涨21.87%，属于较成功预测后的价格再评价；SMCI旧窗口涨43.13%，近三个月却跌4.21%，两个不同起点同时成立。PNR三个月跌22.87%则包含真实下修，恢复到旧价格不是其合理价值的证明。')
add()
add('第三，低Forward PE必须与利润性质和现金风险一起看。MU/SNDK约6.6倍是高盈利存储周期，SMCI约7.3倍伴随融资与营运资本压力，ADBE约9.3倍伴随收费权重塑。相同“个位数PE”并不代表同一种安全边际。IV30约65%—76%的存储/系统公司，也不应与约18%的ET视为同风险仓位。')
add()
add('**本次外部事实复核**');add()
sources=[
('ADBE','6月公司指引、现金与股酬口径，并核9月10日财报仍待发布','https://www.sec.gov/Archives/edgar/data/796343/000079634326000109/adbeex991q226.htm'),
('ADBE日程','9月3日CEO交接公告同时确认9月10日财报电话会','https://news.adobe.com/news/2026/09/adobe-announces-anil-chakravarthy-to-become-president-and-ceo'),
('MU','Q3真实收入、利润与经营现金','https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Results-for-the-Third-Quarter-of-Fiscal-2026/default.aspx'),
('MSFT','FY26需求分散程度、商业RPO和资本开支','https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4'),
('ET','季度0.34美元、年化1.36美元分配','https://ir.energytransfer.com/news-releases/news-release-details/energy-transfer-announces-nineteenth-consecutive-increase'),
('BABA','6月季度经营分部及集团现金','https://www.sec.gov/Archives/edgar/data/1577552/000110465926099220/tm2623667d1_ex99-1.htm'),
('PNR','Q2收入下降与泳池去库存','https://investors.pentair.com/node/27096/pdf'),
('PNR融资','9月2日Taco收购配套14亿美元贷款','https://investors.pentair.com/static-files/18a84a7f-c929-41f5-a115-ae7e6a60e877'),
('ST','半年现金、去杠杆与下一季指引','https://investors.sensata.com/news/news-details/2026/Sensata-Technologies-Reports-Second-Quarter-2026-Financial-Results/default.aspx'),
('SMCI','全年与Q4现金不能混同','https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Financial-Results/default.aspx'),
('TEL','Q3销售、利润和经营现金','https://www.te.com/en/about-te/news-center/corporate-news/2026/2026-07-22-te-connectivity-delivers-results-above-guidance-with-14-sales-growth-and-19-eps-growth-in-third-quarter-of-fiscal-2026.html'),
('META','广告量价增长与经营利润/FCF并不一致','https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/default.aspx'),
('ASML','Q2实绩、2026指引和2027设备产能计划','https://www.asml.com/en/news/press-releases/2026/q2-2026-financial-results'),
('NVDA','Q2增长、资本安排及现金表','https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027'),
('SNDK','Q4量价拆分及NBM协议扩展','https://www.sandisk.com/company/newsroom/press-releases/2026/2026-08-05-sandisk-reports-fiscal-fourth-quarter-2026-financial-results'),
('SNDK协议','NBM最低财务保障及结构化定价；不等于全部市场永久保价','https://www.sandisk.com/company/newsroom/press-releases/2026/2026-08-13-sandisk-investor-day-2026'),
('AVGO','9月2日Q3及下一季指引','https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial'),
('IV30','Cboe定义：平值隐含波动率，30天插值期限','https://datashop.cboe.com/Documents/Cboe_OptionSentiment_Specs.pdf'),
]
for s,why,url in sources:add(f'- [{s}：{why}]({url})')
for x in records:
    primary=[(s,url) for s,why,url in sources if s==x['ticker']]
    if primary:
        idx=text.index(x['supporting_case'])
        text[idx]+=' '+ '、'.join(f'[{s}官方披露]({u})' for s,u in primary)+'。'
add()
add('**文件与核验边界**');add()
add('本次读取16份新结果的结构化横评、核对全部文件哈希，筛看38家单公司报告的当前结论和一年矩阵，对入选20家进一步追溯现金、资本与冲突处。下载38家三个月价格/quote字段，20家尝试Cboe并取得19家IV30。不是重新执行193家公司全部独立深研，也没有验证这份9月选股名单的未来收益。')
add()
add('Yahoo夜间期权接口对大多数标的给出bid/ask归零及占位IV，本表已改用Cboe IV30，不沿用这些无效值，也不把昨日单个Call/Put IV与今日标准IV30混在一列。所下载的完整链、原始时间戳、股价日线和本地引用均留在同目录，方便复算。')
add()
add('生成时间：'+datetime.now(ZoneInfo('America/Los_Angeles')).isoformat())
(OUT/'00_20家公司投资优先级与证据.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
print('WROTE',len(records),'companies;',len('\n'.join(text)),'characters')
for x in records:print(x['rank'],x['ticker'],round(x['pe_ttm_vendor'],2) if x['pe_ttm_vendor'] else None,round(x['forward_pe_vendor'],2) if x['forward_pe_vendor'] else None,round(x['price_return_3m_pct'],2),band(x['base_stock_price_range']),band(x['optimistic_stock_price_range']),round(x['iv30_pct'],1) if x['iv30_pct'] else None)
