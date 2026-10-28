import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rows = json.loads((ROOT / '候选公司.json').read_text(encoding='utf-8'))
topics = json.loads((ROOT / '行业建议.json').read_text(encoding='utf-8'))
topic_map = {x['id']: x for x in topics}
verification = json.loads((ROOT / '指数与去重核验.json').read_text(encoding='utf-8'))
memberships = {x['ticker']: x for x in verification['candidates']}
priority = set('V MA SPGI MCO MSCI CME ICE JPM BRK.B LLY SYK BSX IDXX CTAS GWW ORLY INTU ROP MELI BKNG'.split())
representative = set('DIS TTWO UBER BAC ZTS UNH SBUX NKE UPS SLB FCX'.split())
assert len(priority) == 20
assert len(rows) == len({x['ticker'] for x in rows}) == 98
assert set(x['ticker'] for x in rows) == set(memberships)
assert not verification['duplicates_with_project']
assert not verification['outside_verified_union']
current_industries = (ROOT.parent.parent / '基本面/行业调研/行业索引.md').read_text(encoding='utf-8-sig')
industry_names = set(re.findall(r'^\|\s*([^|]+?)\s*\|\s*`', current_industries, re.M))
assert len(industry_names) == 102
for item in topics:
    assert (item['name'] in industry_names) == (item['status'] == '现有'), item
assert set(x['topic'] for x in rows) == set(topic_map)

groups = [(1,18,'科技软件与数字平台'),(19,38,'金融支付与保险服务'),(39,56,'医药器械与医疗服务'),(57,70,'消费品牌与零售'),(71,82,'工业服务与航空国防'),(83,86,'交通物流'),(87,94,'能源资源与材料'),(95,98,'房地产与基础设施租赁')]
lines = ['# 纳斯达克100与标普500新增98家公司研究候选', '',
'日期：2026-10-28（America/Los_Angeles）。本清单是公司扩充与行业覆盖建议，优先级衡量研究价值、商业模式与补齐覆盖的作用，未做98家公司同口径估值，因此不构成按当前价格买入的排序。', '',
'现有项目登记252家公司、102个行业主题。候选98家公司与现有索引无重复，若未来全部登记，公司总数将达到350家。此次只保存提案，没有修改公司索引、行业索引、正式研究报告或任务队列。', '',
'## 范围与筛选依据', '',
'- 标普500以State Street官方SPY持仓作为成分范围代理，文件日期为2026-10-26；96家候选出现在该持仓中。',
'- 纳斯达克100依据Nasdaq官网公司表，并与Slickcharts当日成分表交叉核对；27家候选在两份名单中均出现。两指数重合25家，去重后98家。基金持仓与指数成分的口径并非完全相同，这里只核验选中公司的资格，不用持仓总条目数代替公司数量。',
'- 项目排除依据为当前公司索引逐条股票代码和公司名称；同公司不同股票类别不重复计数，例如不因GOOG未出现而重新推荐已收录的Alphabet。',
'- 选取能代表收费网络、客户迁移成本、品牌复购、专业认证、路网密度或资源禀赋的公司，同时保留部分周期或经营修复样本。不为每个指数、板块设置机械等额配额。',
'- ★为先研究的20家；“代表/修复”强调观察价值，不默认经营问题已解决。理由、风险与优先级是本次筛选判断。公司业务事实来自逐家公司简介，重点方向另附公司一手资料。风险栏列后续应检验的变量，不表示均已发生。', '',
'指数来源：[State Street SPY持仓](https://www.ssga.com/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx)、[Nasdaq公司名单](https://www.nasdaq.com/articles/global-indexes/nasdaq-100-index)、[Slickcharts交叉核对](https://www.slickcharts.com/nasdaq100)。', '',
'## 建议先研究的20家公司', '',
'支付网络：V、MA。金融数据与交易基础设施：SPGI、MCO、MSCI、CME、ICE。银行与资本配置：JPM、BRK.B。医疗：LLY、SYK、BSX、IDXX。工业与售后服务：CTAS、GWW、ORLY。软件与数字平台：INTU、ROP、MELI、BKNG。', '',
'这20家优先用于建立新领域研究基准；支付与数据授权、医疗器械耗材、工业服务的经营驱动，与当前AI硬件及数据中心投资周期有明显区别。上市公司仍可能共享市场估值和利率风险。', '',
'## 98家公司及行业映射', '',
'指数标记：S＝出现于SPY官方持仓，N＝纳斯达克100；S+N＝两者。新主题编号N01至N56只是提案标识。公司主行业采用主要经济活动，其他分部在关联主题中另行研究。']
for start,end,title in groups:
    lines += ['',f'### {title} {end-start+1}家','', '| 序号 | 公司 | 指数 | 研究优先 | 主行业或新增建议 | 纳入研究的理由 | 关键风险与检验点 |','|---|---|---|---|---|---|---|']
    for r in rows[start-1:end]:
        t=r['ticker']; m=memberships[t]; topic=topic_map[r['topic']]
        source=json.loads((ROOT/'sources'/f'{t}.json').read_text(encoding='utf-8'))
        assert source.get('description'),t
        idx='S+N' if m['sp500_proxy'] and m['nasdaq100'] else ('S' if m['sp500_proxy'] else 'N')
        label='★优先' if t in priority else ('代表/修复' if t in representative else '候选')
        code=r['topic'] if r['topic'].startswith('E') else f"N{int(r['topic']):02}"
        lines.append(f"| {r['id']} | [{t} {r['name']}]({source['url']}) | {idx} | {label} | {topic['status']} {code} {topic['name']} | {r['reason']} | {r['risk']} |")
lines += ['', '## 新行业名称与边界建议', '',
'主行业能够直接复用现有主题的有FTNT与APP两家；其他公司的主营经济活动需要补齐主题。下面提出56个主题名称，其中54个行业、2个横向专题。数量较多源于本次从AI产业链扩展到金融、消费、医疗和传统实体经济，不能把这些公司都归入“AI应用”或“电力能源”。', '',
'行业主题与公司父分类是多对多关系。下面的名称不是新增目录的指令；例如金融数据、支付、商业银行可归入一个新父类“金融服务_支付_资本市场”，医疗器械与医疗服务可归入“医疗器械_诊断_医疗服务”。软件、消费、交通物流、油气资源与非IDC地产也应有相应父类，具体目录调整留待正式归档时统一设计。', '',
'建议首批展开：N12支付网络、N18金融数据评级指数、N19交易所清算、N14综合银行、N21保险经纪、N22代谢疾病治疗、N24心血管器械、N28动物健康、N36汽车后市场、N38企业制服设施服务、N39工业MRO和N41航空部件售后。这是研究任务安排建议，不是买入时点排序。', '',
'| 提案编号 | 建议主题名称 | 类型 | 本次样本 | 研究边界 |', '|---|---|---|---|---|']
for topic in topics:
    if topic['status']=='现有':continue
    samples='、'.join(r['ticker'] for r in rows if r['topic']==topic['id'])
    lines.append(f"| N{int(topic['id']):02} | {topic['name']} | {topic['type']} | {samples} | {topic['scope']} |")
lines += ['', '## 与现有主题的关联方式', '',
'- WDAY、INTU、VEEV、ROP与ACN：可关联“企业AI与Agent工作流软件”，但传统订阅、行业软件和咨询收入不能全部算成AI收入。',
'- ADSK：可关联“AI创作与文档生产软件”及“DCIM、能控与AI工厂数字孪生”；主责仍应是工程设计软件。',
'- JNJ、ABBV、MRK、AMGN、GILD：新型免疫治疗管线可关联“自身免疫与肿瘤新型免疫治疗”；成熟药品不能全部归入该增量专题。',
'- SYK：机器人辅助手术可关联“智能机器人与自主作业装备”；骨科植入耗材与机器人系统分开。',
'- BRK.B：保险分部可复用现有原保险、再保险主题；整个集团以分部估值及资本配置研究。AJG、AON是保险经纪，不按承保公司分析。',
'- HWM、TDG、RTX：民用航空发动机及售后不应笼统归入“运载火箭、航天器与空间基础设施”。既有GE、HEI、RYCEY、PH等也可在以后关联新航空主题，但本次98家不重复计入它们。',
'- RTX、LMT、NOC：无人系统和航天分部可关联现有国防无人系统及空间基础设施主题；军机、导弹主承包保留新主行业。',
'- WMB、NEE：可与现有数据中心电力主题建立需求关联，但管网、公用事业或新能源运营的全部收入不能视为AI收入。',
'- AMT：数据中心分部可关联现有云算力和IDC主题，通信塔租约仍单独研究。', '',
'## 重点方向的一手资料', '',
'以下资料支持业务事实及行业边界；“值得优先研究”是本清单的判断，不是来源的投资评级。', '',
'- [Visa 2025年报](https://s29.q4cdn.com/385744025/files/doc_downloads/2025/Visa-Fiscal-2025-Annual-Report.pdf)：支付网络、交易处理和服务的业务结构。',
'- [Mastercard 2026年第二季度公告](https://www.sec.gov/Archives/edgar/data/1141391/000114139126000081/ma06302026-exx991xearnings.htm)：支付网络与增值服务。',
'- [S&P Global公司资料](https://investor.spglobal.com/ir-home/default.aspx)与[MSCI业务介绍](https://www.msci.com/discover-msci/about-us)：评级、指数、数据及风险分析业务。',
'- [CME 2026年第二季度公告](https://www.cmegroup.com/media-room/press-releases/2026/7/22/cme_group_inc_reportsstrongfinancialresultsforq22026.html)：交易、清算与数据收入。',
'- [礼来2026年第二季度公告](https://investor.lilly.com/news-releases/news-release-details/lilly-reports-second-quarter-2026-financial-results-raises-full)：代谢疾病产品及管线；销量增长与实现价格变化需分开。',
'- [Stryker 2026年第二季度公告](https://www.sec.gov/Archives/edgar/data/310764/000031076426000048/sykex991earningsq22026.htm)：外科、神经与骨科器械。',
'- [Boston Scientific季度经营资料](https://investors.bostonscientific.com/~/media/Files/B/Boston-Scientific-IR-V3/FOH/q2-2026-foh.pdf)：心血管细分业务的增长、竞争与临床风险。',
'- [MercadoLibre 2026年第二季度公告](https://www.sec.gov/Archives/edgar/data/1099590/000109959026000021/meli-20260805xex991.htm)：电商与金融业务。',
'- [O’Reilly公司介绍](https://corporate.oreillyauto.com/investor-relations-information/)：专业维修客户与DIY双市场。',
'- [Cintas年度分部收入](https://www.sec.gov/Archives/edgar/data/723254/000072325426000028/R30.htm)：制服设施、急救安全与消防服务。', '',
'## 核验记录', '',
'- 候选98条、股票代码98个、与现有252家公司重复0家。',
'- SPY持仓96家、Nasdaq-100名单27家、重合25家，范围外0家。',
'- 逐公司业务简介98份均已读取，链接置于公司名称；sources目录保留限长摘要与访问日期，完整业务以链接及后续公司正式披露为准。',
'- 主行业建议覆盖98家，现有主题2个、新增建议56个；新增名称与当前102个行业主题无同名重复。语义相近但经济活动不同的边界在上表及关联说明中列明。',
'- 此次没有批量抓取或比较当前估值、最新全部季报，也没有给出目标价。正式投资筛选需检验估值、资本回报、现金流、负债、稀释和主要风险；不能把“好公司”直接等同于“当前好价格”。', '']
report='\n'.join(lines)
(ROOT/'98家公司与行业扩充建议.md').write_text(report,encoding='utf-8')
print(json.dumps({'companies':len(rows),'priority':len(priority),'new_topics':56,'new_industries':54,'new_cross_topics':2,'existing_primary_topics':2,'report_chars':len(report)},ensure_ascii=False))
