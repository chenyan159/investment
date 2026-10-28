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
    if item['status'] == '建议改名扩围':
        assert item['original_name'] in industry_names, item
        assert item['name'] not in industry_names, item
    elif item['status'] == '现有复用':
        assert item['name'] in industry_names, item
    else:
        assert item['status'] == '建议新增' and item['name'] not in industry_names, item
prior_to_current = {}
for item in topics:
    for old_id in item['previous_topic_ids']:
        assert old_id not in prior_to_current, old_id
        prior_to_current[old_id] = item['id']
assert len(prior_to_current) == 58
for row in rows:
    old_id = row.get('original_topic', row['topic'])
    row['original_topic'] = old_id
    row['topic'] = prior_to_current[old_id]
(ROOT / '候选公司.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
assert set(x['topic'] for x in rows) == set(topic_map)
counts = Counter(t['status'] for t in topics)
assert counts == {'建议新增':19, '建议改名扩围':8, '现有复用':2}, counts
company_counts = Counter(topic_map[r['topic']]['status'] for r in rows)
assert company_counts == {'建议新增':74, '建议改名扩围':22, '现有复用':2}, company_counts
report_files = list((ROOT.parent.parent / '基本面/行业调研/结果').rglob('*.md'))
report_sizes = sorted(len(p.read_text(encoding='utf-8-sig')) for p in report_files)
import statistics
median_chars = int(statistics.median(report_sizes))

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
'指数标记：S＝出现于SPY官方持仓，N＝纳斯达克100；S+N＝两者。本版采用N01至N19新增主题、M01至M08现有主题改名扩围、E1与E2直接复用。旧56项新主题已合并为报告内模块或转入既有主题。公司主行业表示本次研究归属，其他分部另作关联。']
for start,end,title in groups:
    lines += ['',f'### {title} {end-start+1}家','', '| 序号 | 公司 | 指数 | 研究优先 | 主行业或新增建议 | 纳入研究的理由 | 关键风险与检验点 |','|---|---|---|---|---|---|---|']
    for r in rows[start-1:end]:
        t=r['ticker']; m=memberships[t]; topic=topic_map[r['topic']]
        source=json.loads((ROOT/'sources'/f'{t}.json').read_text(encoding='utf-8'))
        assert source.get('description'),t
        idx='S+N' if m['sp500_proxy'] and m['nasdaq100'] else ('S' if m['sp500_proxy'] else 'N')
        label='★优先' if t in priority else ('代表/修复' if t in representative else '候选')
        code=r['topic']
        lines.append(f"| {r['id']} | [{t} {r['name']}]({source['url']}) | {idx} | {label} | {topic['status']} {code} {topic['name']} | {r['reason']} | {r['risk']} |")
lines += ['', '## 行业合并方案', '',
'新增主题从56个压缩至19个，减少37个，约66%。其中18个行业、1个横向专题；另改名扩围8个既有主题，直接复用2个。98家全部保留：74家归入新增主题，22家并入扩围主题，2家直接复用。若将本方案全部正式登记，项目主题数由102增至121，而非158；改名不增加主题数。', '',
'这些是单篇报告的研究主题，不能只放进同一父目录而仍生成56份报告。原细分类别降为章节、模型维度或业务标签，不独立入队。公司父类别和主题保持多对多关系；本次仅更新提案。', '',
'### 信息量判断依据', '',
f'已检查现有{len(report_files)}份行业报告及现行研究方案。Markdown全文字符数中位数为{median_chars:,}，范围{min(report_sizes):,}至{max(report_sizes):,}，包含表格、链接和附录，不是汉字数、token数或有效研究量。篇幅只作量级参考，不能靠报告长短直接判断质量或决定合并。', '',
'现行方案允许重要细分在同一报告附录建模，要求关键子市场保留各自情景数据。合并主要依据：能否共享需求或资金链、来源与更新节奏；保留多少套独立经营模型；合并是否使核心问题被挤压。预计信息量是编辑规划估计，尚未完成新行业调研，不是已验证字数、执行时长或硬性篇幅配额。', '',
'默认一篇容纳2至4个重要模块，低信息量单一公司放入模块；少数业务特别宽的报告保留分部附录。篇幅变长本身不触发拆分，只有出现不同资料体系和独立更新需求、共同结论很少且核心模型被挤压时才重新考虑。', '',
'### 8个现有主题改名扩围', '',
'| 编号 | 现有名称 | 建议名称 | 本次新增样本 | 报告内模块 | 预计整篇信息量 | 合并理由 |', '|---|---|---|---|---|---|---|']
for t in topics:
    if t['status'] != '建议改名扩围': continue
    samples='、'.join(r['ticker'] for r in rows if r['topic']==t['id'])
    lines.append(f"| {t['id']} | {t['original_name']} | {t['name']} | {samples} | {t['modules']} | {t['estimated_information']} | {t['merge_reason']} |")
lines += ['', '### 19个新增主题', '',
'| 编号 | 建议主题 | 类型 | 本次样本 | 报告内模块 | 预计整篇信息量 | 合并理由 |','|---|---|---|---|---|---|---|']
for t in topics:
    if t['status'] != '建议新增': continue
    samples='、'.join(r['ticker'] for r in rows if r['topic']==t['id'])
    lines.append(f"| {t['id']} | {t['name']} | {t['type']} | {samples} | {t['modules']} | {t['estimated_information']} | {t['merge_reason']} |")
lines += ['', '### 直接复用', '',
'FTNT复用“网络安全、身份权限与AI治理”；APP复用“广告推荐、搜索与数字分发”，均不改名。', '',
'### 合并后的经济边界与既有样本', '',
'下列既有公司仅说明关联机会，不重复计入新增98家，也不代表全公司收入归属于该主题。正式改名时应保留原主题的核心覆盖，更新索引、活动引用与后续报告任务；旧报告仍按原范围视为历史研究，不能只改文件名就声称完成了扩围。', '',
'| 编号 | 主题 | 保留的经济边界 | 可关联的既有项目公司 |','|---|---|---|---|']
for t in topics:
    if t['status'] == '现有复用':continue
    lines.append(f"| {t['id']} | {t['name']} | {t['scope']} | {'、'.join(t['related_existing_companies']) or '—'} |")
lines += ['', '### 原提案到本版的合并映射', '',
'旧编号仅用于追溯上一版56项建议，已不作为当前主题或任务入口。', '',
'| 原提案编号 | 当前归属 | 处理方式 |','|---|---|---|']
for t in topics:
    old='、'.join(f'N{int(v):02}' if v.isdigit() else v for v in t['previous_topic_ids'])
    lines.append(f"| {old} | {t['id']} {t['name']} | {t['status']} |")
lines += ['',
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
'- 当前29个承接主题覆盖98家：19个新增、8个改名扩围、2个直接复用。原58个承接主题全部找到唯一新归属，98家公司无遗漏。',
'- 新增与改名后的主题名称无重复，8个被修改名称及2个复用名称均可在当前102条行业索引中找到；行业索引本身尚未修改。',
'- 此次没有批量抓取或比较当前估值、最新全部季报，也没有给出目标价。正式投资筛选需检验估值、资本回报、现金流、负债、稀释和主要风险；不能把“好公司”直接等同于“当前好价格”。', '']
report='\n'.join(lines)
(ROOT/'98家公司与行业扩充建议.md').write_text(report,encoding='utf-8',newline='\n')
print(json.dumps({'companies':len(rows),'priority':len(priority),'topic_actions':dict(counts),'company_actions':dict(company_counts),'current_report_median_chars':median_chars,'report_chars':len(report)},ensure_ascii=False))
