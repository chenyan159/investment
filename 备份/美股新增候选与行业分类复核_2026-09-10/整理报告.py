from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter
import json, hashlib

ROOT = Path(r'D:\drive\Investment')
OUT = Path(__file__).parent
data = json.loads((OUT/'候选公司与分类建议.json').read_text(encoding='utf-8'))
audit = json.loads((OUT/'项目覆盖核验.json').read_text(encoding='utf-8'))
quotes = {x['symbol']: x for x in json.loads((OUT/'美股交易身份与行情核查.json').read_text(encoding='utf-8'))}
candidates = data['candidates']
categories = data['proposed_categories']

def link(path, label=None, line=None):
    p = str(path).replace('\\','/')
    tail = ':'+str(line) if line else ''
    return f'[{label or Path(path).name}](</{p}{tail}>)'

def report(key):
    hits = [x['file'] for x in audit['industry_files'] if '行业调研_'+key+'_2026' in x['file']]
    assert len(hits)==1, (key,hits)
    return hits[0]

def evidence(key, line, finding):
    return {'report':report(key),'line':line,'finding':finding}

actions = [
 {'id':'I01','action':'新增','delta':1,'name':'AI高多层PCB、低损耗覆铜板与铜箔',
  'reason':'连接器报告把背板PCB加工交给PCB专题；封装基板报告排除服务器PCB，但82个行业索引中没有承接专题。属于明确的经济对象覆盖缺口。',
  'scope':'覆盖服务器/交换机高多层PCB、HDI、低损耗覆铜板和铜箔；分别核算板级产值与上游材料收入，不能直接相加为终端市场。排除ABF/BT封装基板和独立连接器。',
  'metrics':'板层/面积、传输损耗、良率、合格产能、每机架或每MW用板价值、ASP、扩产资本回报、客户认证周期。',
  'companies':['TTMI'],
  'evidence':[evidence('高速连接器、背板与结构化布线',32,'PCB本体和加工被交给另一个PCB专题。'),evidence('封装基板、中介层与RDL',21,'封装基板市场明确排除服务器PCB和模组板。')]},
 {'id':'I02','action':'拆分：1变3','delta':2,'name':'机器人硬件',
  'targets':['工业自动化控制、工业机器人与协作机器人','仓储物流机器人与自动化系统','人形机器人与关键执行部件'],
  'reason':'现有报告把工业机械臂、物流机器人和具身平台放在一个硬件交付模型，并尽量剔除独立软件、集成和多年服务。ROK/EMR的控制软件和SYM的系统交付经济性需要更明确的研究责任。',
  'scope':'第一篇研究PLC/运动与过程控制、工业/协作机器人；第二篇研究仓储系统吞吐、集成验收与软件维护；第三篇研究人形任务能力、执行部件和商业化。三篇用同一BOM及最终客户支出台账消除内部重复。',
  'metrics':'生产有效小时、每次合格任务成本、故障/接管率；设备台数、系统项目额、软件服务费分开；控制业务与机器人分部收入/利润分开。',
  'companies':['ROK','EMR','SYM','FANUY','YASKY','SMCAY','ALGM'],
  'evidence':[evidence('机器人硬件',22,'当前I、L、E三个子池按新增硬件等价值计量，并剔除独立软件、集成和多年服务。'),evidence('机器人硬件',24,'具身平台交付含实验室/展示/采集，不能视为同量的自主工业工人。')]},
 {'id':'I03','action':'新增','delta':1,'name':'工业机器视觉与精密感知',
  'reason':'机器人硬件报告覆盖视觉等部件，但工厂检测、读码、视觉部署、磁性位置/电流感知横跨机器人、仓储与半导体设备，没有清晰的专题主责。',
  'scope':'分别研究视觉系统/算法平台、视觉SoC、精密位置/电流传感器三个经济层；共享需求模型，不把芯片、系统和整机产值重复相加。',
  'metrics':'缺陷检出/误报率、延迟、标定与部署成本、每工位价值、软件附加率、器件设计采用到量产转化、认证及更换成本。',
  'companies':['CGNX','AMBA','ALGM'],
  'evidence':[evidence('机器人硬件',22,'当前主模型围绕整机硬件交付，未单独承担工厂视觉和精密感知的完整商业模型。')]},
 {'id':'I04','action':'拆分：1变3','delta':2,'name':'商业火箭与商业航天',
  'targets':['运载火箭、航天器与空间基础设施','低轨卫星通信、直连手机与地面终端','地球观测、遥感数据与空间信息服务'],
  'reason':'发射/制造按任务和里程碑收费；卫星通信按连接与服务收费；遥感按影像、数据、订阅和主权系统收费。现有报告已指出这些市场及订单定义不能混用。',
  'scope':'前两层之间区分内部星座发射与外部商业采购；遥感硬件交付与数据订阅分开。保留现有综合报告作为历史和跨层综述。',
  'metrics':'任务成功/发射节奏与现金成本；在轨有效容量/付费客户/ARPU；独特数据覆盖/重访时间/续订；卫星寿命、更替CapEx与政府合同回款。',
  'companies':['CW','RDW','ASTS','PL'],
  'evidence':[evidence('商业火箭与商业航天',15,'卫星产业统计与广义太空经济统计定义不同，均不能整体当作火箭公司的收入空间。'),evidence('商业火箭与商业航天',19,'主权需求改善融资但不能替代资本回报检验；Planet增长包含硬件和政府合同结构变化。')]},
 {'id':'I05','action':'新增','delta':1,'name':'核燃料循环与浓缩服务',
  'reason':'数据中心自备发电报告的定量主责是美国现场/专线专用发电的可用MW，并不能承担铀资源、转化、SWU浓缩及HALEU的供需和订单模型。',
  'scope':'铀、转化、常规浓缩、HALEU、去转化与燃料制造分阶段。公司可以跨阶段经营，但不得把全链价值都归为同一阶段的收入。',
  'metrics':'铀磅数、转化kgU、SWU、交付和合格HALEU公斤数；已签/有条件/已拨款合同区分；扩产资本支出、许可、材料供应与交付义务。',
  'companies':['CCJ','LEU'],
  'evidence':[evidence('数据中心自备发电与微电网',19,'该专题的可审查定量主责为美国数据中心专用发电与微电网。')]},
 {'id':'I06','action':'新增','delta':1,'name':'云与AI应用可观测性、运维自动化',
  'reason':'Fabric遥测报告明确排除通用APM；数据库报告聚焦数据组织与查询；推理运行时关注执行效率。因此DDOG的应用、日志、链路追踪和LLM运行问题没有完整承接。',
  'scope':'应用性能、日志/指标/追踪、LLM调用的质量/成本/故障诊断、自动化运维。网络设备遥测、安全独立采购、数据库存储分别保留在原专题。',
  'metrics':'可观测工作负载、付费客户/NRR、单次查询与遥测成本、净现金和SBC、开源/云平台免费功能替代、故障定位与恢复时间。',
  'companies':['DDOG'],
  'evidence':[evidence('AI_Fabric网络操作系统与遥测软件',35,'核心软件池明确排除通用APM、安全和训练平台收入。'),evidence('数据平台、数据库与AI数据软件',13,'数据组织、授权和运行责任与工作负载增长不能简单等同于供应商收入。')]},
 {'id':'I07','action':'新增','delta':1,'name':'边缘云、应用交付与无服务器计算',
  'reason':'边缘推理芯片关注硬件器件，GPU云关注集中式计算供给，安全报告关注安全预算；NET的全球边缘执行与应用交付需要独立的收费及资本模型。',
  'scope':'CDN/应用交付、边缘CPU执行、Workers等无服务器平台。与安全产品有交叉的合同按主要付费对象拆分，内部调用不虚构为外部收入。',
  'metrics':'请求/CPU时间、付费执行/开发者转化、网络带宽与资本成本、毛利/FCF、回源节省、云厂捆绑及平台迁移。',
  'companies':['NET'],
  'evidence':[evidence('AI边缘推理芯片',1,'现有相邻专题的主对象是芯片。'),evidence('网络安全、身份权限与AI治理',58,'同一合同涉及多个营销标签，TAM不能相加。')]},
 {'id':'I08','action':'改为横向标准/架构专题，移出独立经济市场计数','delta':-1,'name':'OCI（光学计算互连）/ Open CPX / XPO',
  'reason':'现有报告明确三者分别是光线路接口、靠近ASIC的连接/维修边界和高密度可插拔形态，可以组合使用。把它们当又一个独立市场，容易与CPO、光I/O、连接器、模块重复。',
  'scope':'保留全文及历史；将经济归属交叉映射到CPO/NPO、封装内光I/O、高速连接器及800G/1.6T光模块。保留路线比较、认证、替代关系和标准进展的横向研究。',
  'metrics':'标准状态、认证/量产客户、功耗、密度、链路距离、可维护性、光/铜替代位置与每位置器件价值。',
  'companies':[],
  'evidence':[evidence('OCI_（光学计算互连）_Open_CPX_XPO',9,'三个概念承担不同层次，可竞争也可组合。'),evidence('OCI_（光学计算互连）_Open_CPX_XPO',17,'Open CPX同时服务铜和光；XPO有不同重定时架构。')]},
 {'id':'I09','action':'更新状态与覆盖映射，不新增数量','delta':0,'name':'五个AI应用与软件行业',
  'reason':'行业索引仍标“新增待调研”，但五个行业均已有2026-09-06正式报告。缺口主要转移到公司层，不能再按缺行业处理。',
  'scope':'企业Agent、创作文档、数据平台、安全治理、广告搜索五篇继续独立。补NOW/PLTR、SNOW、PANW，并建立DDOG/NET与新专题的交叉映射。',
  'metrics':'最新报告日期、实际完成状态、公司覆盖、收费与成本；不把应用运行量当做供应商收入。',
  'companies':['NOW','PLTR','SNOW','PANW','DDOG','NET'],
  'evidence':[evidence('企业AI与Agent工作流软件',353,'已有Palantir/AIP的商业归属与不能全额计入该专题的说明。'),evidence('数据平台、数据库与AI数据软件',15,'已有Snowflake等最新财务证据。')]},
 {'id':'I10','action':'升级边界，不新增数量','delta':0,'name':'电力、冷却、功率器件与工业控制的交叉研究',
  'reason':'施耐德系统硬件与软件增长不同，安川运动控制与机器人利润方向不同。公司名或单个热词不能代替业务分部的研究归属。',
  'scope':'保留风冷/HVAC、直液冷、小组件/流体、配电设备与功率器件各自经济对象；补齐部件—系统—施工—软件的收入分配与跨公司对照。',
  'metrics':'分部收入/利润/现金流、AI/DC可辨识增量、安装/交付责任、订单取消及延迟条款、并购与有机增长拆分。',
  'companies':['SBGSY','YASKY','SPXC','ITT','ALGM','EMR','ROK'],
  'evidence':[evidence('DCIM、能控与AI工厂数字孪生',20,'施耐德系统收入有机增长28%，软件与数字服务增长7%；ETAP与RIB约持平。')]},
]
parent_mapping={
 'I01':'半导体与电子制造_设备_材料_测试',
 'I02':'工业自动化_机器人_感知',
 'I03':'工业自动化_机器人_感知',
 'I04':'商业航天_火箭_卫星',
 'I05':'AI园区电力_机电_冷却',
 'I06':'AI应用_软件_数据平台',
 'I07':'AI应用_软件_数据平台',
 'I08':'AI网络_光互联_铜互联',
}
for a in actions:
    if a['id'] in parent_mapping: a['proposed_parent_category']=parent_mapping[a['id']]
industry_plan={'date':'2026-09-10','status':'仅建议，未实施正式索引和报告迁移','current_topics':82,'proposed_economic_topics':82+sum(a['delta'] for a in actions),'retained_horizontal_topics':1,'industry_parent_categories_count':7,'industry_parent_category_renames':{'机器人_硬件_零部件':'工业自动化_机器人_感知','晶圆制造_设备_材料_测试':'半导体与电子制造_设备_材料_测试'},'actions':actions}
assert industry_plan['proposed_economic_topics']==90
(OUT/'行业调整建议.json').write_text(json.dumps(industry_plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def venue(c):
    q=quotes[c['ticker']]['quote']
    return {'NGM':'Nasdaq','NMS':'Nasdaq','NCM':'Nasdaq','NYQ':'NYSE','PNK':'美国OTC ADR'}.get(q['exchange'],q['fullExchangeName'])

def money_guard(c):
    t=c['ticker']
    if t in {'LEU','ASTS','RDW'}: return '高风险：技术/项目兑现与融资风险需单独建模'
    if t in {'AMBA','PL','NET','SNOW','SYM'}: return '成长型：现金、盈利质量、客户集中或估值需重点核验'
    if t in {'CGNX','ROK','EMR','SBGSY','FANUY','SMCAY','CW','ITT','SPXC'}: return '成熟业务提供经营支撑；买价、周期与资产负债表仍决定回撤'
    return '已有商业收入；需分别检验增长持续性与股东现金回报'

intro=f'''# 美股新增公司与行业分类升级建议

研究截止：2026-09-10（美国太平洋时间）。本文件是对话产生的一次性研究建议，正式归档位置与任务以项目索引为准。

**建议补充25家公司：21家NYSE/Nasdaq股票，4家美国OTC ADR。** 我以当前公司索引193家公司为权威名单，同时排查分类目录下的正式公司报告；25家均未正式入库。行业报告提到一家公司，并不代表已完成该公司的独立研究。若全部补入，公司数为218；仅纳入21家交易所股票则为214。

这份名单按技术资产、已经形成的付费业务、长期价值获取能力、资金与经营支撑、对现有研究的补缺价值筛选。**“优先”是研究顺序，不能当作当前价格买入排名。** 有实际技术和高增长，也可能因为高估值、资本支出、稀释或周期而没有足够股票回报。

核验依据：{link(audit['company_index'],'公司索引')}；{link(audit['industry_index'],'行业索引')}。已核对82个行业主题及其82份2026-09-06正式报告的文件覆盖，并重点阅读与候选有关的边界、增长机制和竞争章节。索引用于确认覆盖和分类，下面的判断依据具体报告正文及公司一手披露。

**最值得先补的12家交易所股票**：TTMI、ALGM、CGNX、SYM、ROK、EMR、SPXC、NOW、PANW、SNOW、DDOG、PLTR。若支持OTC，再优先加入SBGSY。它们分别补上高端PCB、精密感知、工业自动化、仓储系统、排热及企业AI商业化的代表公司。

**重点候选**：AMBA、ITT、CW、CCJ、PL、NET，以及FANUY、YASKY、SMCAY。**高风险研究候选**：LEU、ASTS、RDW；它们有值得研究的技术和资产，但经营兑现与融资的不确定性更大。

## 25家公司与建议归类

下表中的经营数字是披露事实；技术如何形成未来利润、研究优先级和分类是本次判断。增长期按各公司的财季标注；季度自由现金流不能直接年化，不同公司的调整后指标不能混作GAAP利润。

| 公司 / 美国交易路径 | 研究优先级 | 技术与业务资产 | 近期证据 | 建议主类别 |
|---|---|---|---|---|
'''
rows=[]
for c in candidates:
    rows.append(f"| **{c['ticker']} · {c['name']}** / {venue(c)} | {c['priority']} | {c['technology']} | {c['evidence']} [原始披露]({c['source_url']}) | {c['category_id']} {categories[c['category_id']]} |")

discussion='''

## 为什么它们能改善研究池

**TTMI、ALGM、CGNX最能说明“补公司”和“补研究责任”要同步。** TTMI销售高端PCB和射频等产品，不能简单套用ABF封装基板的产能或价格；ALGM的电流和位置传感连接供电、汽车和工业运动；CGNX把视觉从硬件器件变成客户可以部署和使用的检测/读码系统。这些业务的认证、算法、良率和现场可靠性比“属于AI产业链”的标签更接近价值来源。TTMI航空航天与国防业务占2026Q2收入37%，ALGM的汽车收入仍是主体，CGNX披露现金与投资7.55亿美元且无债务；这些是需要分别建模的现有业务支撑，不能保证股价不跌。[TTMI财报](https://investors.ttm.com/news-events/press-releases/detail/411/ttm-technologies-inc-reports-second-quarter-2026-results)、[ALGM财报](https://investors.allegromicro.com/news-releases/news-release-details/allegro-microsystems-reports-first-quarter-2027-results/)、[CGNX财报](https://www.sec.gov/Archives/edgar/data/851205/000085120526000061/a07052026-xex991xq22026ear.htm)

**工业自动化要同时看整机、控制和系统交付。** SYM的关键是仓库的连续吞吐、验收与长期维护；ROK/EMR的关键是控制软件、仪表、工艺知识和客户既有安装基础；FANUY/YASKY的关键是运动控制与成熟工业客户。它们能帮助项目区分“机器人任务变多”与“哪个供应商的利润变多”。这些价值机制是判断，需由后续分部财务、客户回报和合同条款验证。

**安川是分类可能直接影响投资判断的实际例子。** FY26Q1集团收入增长10.6%，运动控制收入增长21.5%；机器人收入只增长2.0%，机器人营业利润下降82.3%，公司解释包含ERP切换和欧洲改革费用影响。运动控制的驱动器增长还涉及数据中心空调、服务器冷却与半导体真空泵。若只归为“机器人公司”，可能把真正增长来源和经营问题同时看错。[安川FY26Q1财报，第3—4页](https://www.yaskawa-global.com/wp-content/uploads/2026/07/20260710_en.pdf)

**软件候选能检验AI能否从资本开支走向客户付费。** NOW/PLTR对应业务流程与行动，SNOW对应受管数据，DDOG对应应用可观测性，PANW对应安全和身份，NET对应边缘执行与交付。新增它们有助于比较算力卖方和最终应用卖方谁获取了利润。但应跟踪AI新增收费、席位蚕食、推理成本、SBC、销售及实施人工，不能把公司全部收入自动计为AI增量。

**航天与核燃料提供不同期限的研究对象。** CW有成熟高可靠系统业务；PL有影像与数据产品；ASTS需要把技术链路演示推进为持续商业服务；RDW要检验并购后的盈利和现金转化；CCJ有资源、燃料服务和Westinghouse权益；LEU的未来浓缩扩产与现有贸易业务需要分开。它们不能共同使用一个“太空经济增速”或“AI电力增速”。

## 公司归类：建议10类升级为16类

归类用于确定主要研究责任。建议采用“一个主类别＋多个业务标签＋多个行业关联”，并保存生效日期与历史别名；主类别不是公司全收入的行业归属。复杂集团按主要利润、现金流和经营模式确定主类别，AI新业务可以是次级标签或单独业务池。

| 现有类别 | 建议调整 | 数量变化 | 具体理由与既有公司处理 |
|---|---|---:|---|
| 配电_电源_功率器件 | 功率半导体_电源管理_传感器；配电_电源系统_电气设备 | 1→2 | ALGM/MPWR/IFNNY与ETN/SBGSY卖的产品、资本强度和认证机制不同。ON、STM的公司研究可迁入器件类，保留汽车/工业/MCU等业务标签。 |
| 机电_冷却_工程_水处理_边缘工业AI | 热管理_流体_水处理；工程建设_机电安装；机器人_工业自动化_智能硬件；航空航天_卫星_高可靠系统 | 1→4 | 当前RKLB、SPCX及TSLA混在该大类。火箭/卫星、建筑施工、控制器与排热设备的收入模型差异过大。TSLA仍须分清汽车、能源和机器人期权。 |
| 云算力_IDC_AI软件平台 | 云算力_IDC_边缘云；企业软件_数据平台；网络安全_身份权限_治理 | 1→3 | 云租赁/地产与轻资产软件的资本开支、毛利、合同与估值不同。NET主归边缘云，保留安全标签；大型互联网集团保留各分部标签。 |
| 半导体材料_化学品_基板 | 电子材料_化学品_基板_PCB | 1→1 | 明确容纳PCB；TTMI板级业务不等同于ABF基板，需行业映射区分。 |
| 其余六类 | 保留 | 6→6 | 先修复实质边界和业务归属，再处理目录命名。 |

完整16类及本次新增公司的映射如下。

| 编号 | 建议类别 | 本次候选 |
|---|---|---|
'''
catrows=[]
for k,v in categories.items():
    syms='、'.join(c['ticker'] for c in candidates if c['category_id']==k) or '本轮无新增；保留现有覆盖'
    catrows.append(f'| {k} | {v} | {syms} |')

industry_text='''

## 行业报告：建议82个经济主题调整为90个，并保留1个横向标准专题

计算：82＋机器人拆分净增2＋航天拆分净增2＋新增PCB/视觉/核燃料/应用可观测性/边缘云5篇－OCI标准专题转横向1篇＝90。横向专题全文和历史保留，所以若按所有活动研究入口计数则为91；90是调整后的经济研究主题数。这是拟议结构，尚未修改正式索引。

行业父类别可以维持7个；建议将“机器人_硬件_零部件”更名为“工业自动化_机器人_感知”，将“晶圆制造_设备_材料_测试”扩为“半导体与电子制造_设备_材料_测试”。新增PCB放后者，视觉和三个机器人专题放前者；核燃料放电力大类，应用可观测性和边缘云放AI应用/软件大类，航天专题沿用航天大类。公司主类别与行业专题各有用途，无需一对一对应；跨行业公司用多重关联解决。

'''
for a in actions:
    targets='；'.join(a.get('targets',[]))
    refs='；'.join(link(e['report'],Path(e['report']).name.replace('行业调研_','').replace('_2026-09-06.md','')+f" 第{e['line']}行",e['line']) for e in a['evidence'])
    industry_text+=f"### {a['id']} · {a['name']}：{a['action']}\n\n"
    industry_text+=a['reason']+f' 依据：{refs}。\n\n'
    if targets: industry_text+='调整后的专题：'+targets+'。\n\n'
    if 'proposed_parent_category' in a: industry_text+='建议行业父类别：'+a['proposed_parent_category']+'。\n\n'
    industry_text+='研究边界：'+a['scope']+'\n\n核心数据：'+a['metrics']+'\n\n'
    if a['companies']: industry_text+='对应新增候选：'+'、'.join(a['companies'])+'。\n\n'

closing='''## 哪些内容暂时不必继续拆

**光通信优先解决边界与归属。** 现有AI网络行业已有18个主题，公司类别已有20家公司，覆盖密度明显高于机器人和航天。CPO/NPO、封装内光I/O、Optical Interposer分别可以研究系统位置、计算封装和光引擎制造等不同对象，暂不建议整体合并。应共享BOM与替代关系，防止把激光器、光引擎、光模块和系统TAM相加。只有在买方、计价单位、技术约束或利润池不同的时候，新增独立行业才有价值。

**冷却和电力设备已有足够多细分主题。** SPXC、ITT、SBGSY首先需要补公司与业务分部映射。不能因为新增一家泵阀企业就另开一个冷却行业。SPXC与已被ITT收购的SPX FLOW需要在公司身份字段中区分；公司整体有机增长与收购放大的收入增长也应分别保存。[ITT季度披露](https://investors.itt.com/results-and-filings/quarterly-results)

**网络安全不按营销标签无限拆分。** 现有报告已提醒SASE、零信任、身份、数据安全、AI安全可能来自同一份合同。PANW可先放入现有专题，保留产品/付费对象的子标签；身份平台和AI治理的价值需验证独立收费，而不是增加重复市场规模。

## 三层研究方案应如何配合

| 层级 | 应补充的结构化信息 | 防止的分析偏差 |
|---|---|---|
| 行业调研 | 买方、最终预算、收费单位、部件/系统边界、替代路线、合格产能、商业化阶段、增长与利润归属；新主题明确承接被相邻主题排除的对象 | 上游报告都“排除”，下游仍假定已有覆盖；同一预算/TAM反复相加 |
| 公司调研 | 分部收入/利润/现金流、AI可辨识增量、并购/汇率/有机增长、客户集中、认证/设计采用/量产、合同可取消性、融资与SBC、美国上市身份和ADR信息 | 把集团增长当成某个热点业务爆发；把认证/合作/条件订单当作收入 |
| 公司情景投资决策 | 各业务分别建收入和利润桥；时间滞后、CapEx、营运资金、净债务、股本变化、退出估值和条件回报；成熟业务与未验证期权分开 | 技术成功但每股价值不增长；乐观情景漏掉资金缺口；好公司被误写为任何价格都值得买 |

新增公司的行业关联不应只取一个目录名。建议记录primary_category、business_segments、industry_ids、commercialization_stage和US_listing_identity；各字段带时点，未知份额保留未知，不用主类别回填100%。分类先以元数据和映射落实，后续目录迁移再保留旧到新映射及历史报告。

第一批研究宜同步补PCB专题与TTMI、视觉专题与CGNX/ALGM、仓储专题与SYM，再补ROK/EMR/SPXC及软件12家名单中的其余公司。既有软件专题可直接支撑NOW/PANW/SNOW/PLTR，DDOG和NET则需要新增的应用可观测性、边缘云研究承接。最终投资比较仍需这些公司完成正式公司调研和情景决策。

## 美国交易身份与未纳入对象

21家NYSE/Nasdaq股票为主要候选。SBGSY、FANUY、YASKY、SMCAY属于美国OTC ADR，是否能买取决于券商的OTC支持和账户权限；不能把有美元报价等同于所有美股账户都能下单。SMC官方披露SMCAY为OTC的Sponsored Level I ADR，20份ADR代表1股普通股。[SMC ADR资料](https://www.smcworld.com/ir/en-jp/adr.html)；施耐德和FANUC美国ADR的现行交易信息可在存托行目录核对：[SBGSY](https://www.adrbny.com/directory/dr-details/_jcr_content/root/drDetailsComponent.overview.overview.80687P106.html)、[FANUY](https://www.adrbny.com/directory/dr-details/_jcr_content/root/drDetailsComponent.overview.overview.307305102.html)。

Hamamatsu的美国ADR正确代码为HPHTY。技术值得观察，但本轮查到的美国交易流动性很弱，因此未纳入25家；原始查询中的HPKCY为未通过核验的错误候选代码，已排除。[存托行资料](https://depositaryreceipts.citi.com/adr/guides/pgm_dispdsfhist.aspx?cusip=40652R107&pageId=15&subpageID=192)

Ibiden、Unimicron本轮未核实足够可用的美国交易路径；日本或台湾本地代码不能满足本次限制，暂未纳入。LFUS、Q、MOD、MPWR、VRT、ETN、GEV、NBIS、CRWV、IREN等已在现有公司索引中，不属于新增缺口。未上市的公司、已有上市公司的已收购业务不另算一家公司。

## 数据与可复核范围

原始行情核验保存了交易所、币种、报价日期、价格和成交量；它用于辨认美国证券身份和发现明显异常。不同供应商的forward PE可能对应不同财年和调整口径，亏损或接近零EPS时还会产生无意义倍数，本报告不以这些未经统一的倍数给出买入排名。

最终清单25家均具有正的美元报价，且未与当前193家权威索引或正式公司报告文件名冲突。报告中的公司经营数字以链接的一手披露为准；SMC的技术依据主要为官方产品资料，本轮未填入未经提取核验的季度财务数字。所有增长与分类判断可根据后续正式研究调整。

'''
main=intro+'\n'.join(rows)+discussion+'\n'.join(catrows)+industry_text+closing
(OUT/'美股新增公司与行业分类升级建议.md').write_text(main,encoding='utf-8')

appendix='''# 25家公司入库建议表与后续核验重点

日期：2026-09-10。所有条目为候选建议；归类不代表公司全部收入属于该行业。量化估值和条件回报留待正式公司情景投资决策统一研究。

'''
for i,c in enumerate(candidates,1):
    q=quotes[c['ticker']]['quote']
    when=datetime.fromtimestamp(q['regularMarketTime'],ZoneInfo('America/New_York')).strftime('%Y-%m-%d %H:%M %Z')
    old=', '.join(c['existing_industries'])
    new=', '.join(c['proposed_industries']) or '沿用现有行业，更新公司覆盖与业务分部映射'
    appendix+=f'''## {i}. {c['ticker']} — {c['name']}

研究优先级：**{c['priority']}**。美国交易路径：**{venue(c)}**。身份核验报价：{q['regularMarketPrice']} USD，行情时间{when}；仅用于识别证券，不作为买价建议。

技术与业务资产：{c['technology']}。

事实依据：{c['evidence']} [公司一手披露/产品资料]({c['source_url']})（资料日期：{c['source_date']}）。

价值传导判断：{c['value_mechanism']}

主要反证与风险：{c['risks']}

经营支撑判断：{money_guard(c)}。

建议主类别：**{categories[c['category_id']]}**。若暂维持旧10类，过渡归类可放在：{c['current_category_if_unchanged']}。

现有相关行业：{old}。

新增/拆分后相关行业：{new}。

'''
(OUT/'25家公司入库建议表.md').write_text(appendix,encoding='utf-8')

issues=[]
symbols=[c['ticker'] for c in candidates]
assert len(symbols)==len(set(symbols))==25
existing={x['symbol'] for x in audit['existing_companies']}
assert not existing.intersection(symbols)
assert len(existing)==193
assert len(categories)==16
venues=Counter(venue(c) for c in candidates)
assert venues['美国OTC ADR']==4 and len(symbols)-venues['美国OTC ADR']==21
for c in candidates:
    q=quotes[c['ticker']]['quote']
    assert q['currency']=='USD' and q['regularMarketPrice']>0,c['ticker']
    assert c['category_id'] in categories
    for n in c['existing_industries']:
        if n not in {x['name'] for x in audit['industries']}: issues.append('现有行业名称未匹配：'+n)
for p,h in [(audit['company_index'],audit['company_index_sha256']),(audit['industry_index'],audit['industry_index_sha256'])]+[(x['file'],x['sha256']) for x in audit['industry_files']]:
    if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h: issues.append('来源文件哈希变化：'+p)
company_reports=[p for d in (ROOT/'基本面/公司调研').iterdir() if d.is_dir() and d.name in {c['category'] for c in audit['existing_companies']} for p in d.glob('*.md')]
collision=[str(p) for p in company_reports if p.name.split('_')[0] in symbols]
assert not collision
result={'checked_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'final_candidates':25,'exchange_listed':21,'otc_adr':4,'existing_companies':193,'proposed_companies_all':218,'proposed_companies_exchange_only':214,'company_category_count_proposed':16,'industry_economic_topics_proposed':90,'horizontal_standards_topics_retained':1,'current_industry_reports_hashed':len(audit['industry_files']),'formal_company_report_collisions':collision,'issues':issues,'files':[p.name for p in OUT.iterdir() if p.is_file()]}
(OUT/'交付核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'candidate_count':len(symbols),'venues':venues,'main_report_characters':len(main),'appendix_characters':len(appendix),'validation_issues':issues},ensure_ascii=False))
assert not issues,issues
