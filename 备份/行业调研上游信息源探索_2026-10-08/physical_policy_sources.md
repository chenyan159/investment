# 电力、项目许可、设备贸易与监管上游：公开源实测

实测日期：2026-10-08，America/Los_Angeles。本文是一次性非正式探索，不是正式行业结论；未修改研究方案、索引或 runner。资料范围对应当前行业索引中的电力接入、自备发电、开关与变压器、冷却与厂务、半导体设备和核燃料等主题。

## 主要判断

这些来源应进入上游，但应保存“对象—事件—状态—证据”，而不是新增一批宏观叙事报告。最有价值的用途是：给建设规模模型增加现实约束；把请求、获准、建设、送电、爬坡和实际耗电分开；验证设备交付与贸易方向；发现政策变化和许可阻碍。它们大多不能独立证明终端 AI 需求、采购金额或供应商收入。

最关键的分类是把**发电侧并网队列、负荷侧接入、项目许可、实际运行、贸易统计、法规及核燃料许可**分开。不能建立一个混合“ISO 并网排队总库”然后直接加总 MW。

现行行业方案 `基本面/行业调研/研究方案/研究方案_20260918_130642.md` 只允许把 `基本面/行业调研/产业背景/` 作为本地研究资料根目录。因此，即使新事实库按根目录分工放进 `金融资料/`，现行 industry 任务也不会因此自动获得读取资格；正式接入需要明确输入合同，或把经过证据整理的专题成果发布到获准的产业背景根。此次只讨论，不实施改变。

## 1. 电力侧：必须拆开的四类资料

| 平台与实测 | 公开对象、字段与更新 | 质量和可证明范围 | 接入判断 |
|---|---|---|---|
| [LBNL Queued Up 2026](https://eta.lbl.gov/publications/queued-2026-edition-characteristics)；网页及下载入口可读 | 2026-05 发布，经济期间截至 2025 年底；项目级 XLSX、数据字典和汇总页，跨 50 多个电网运营方 | 官方明确只含输电侧发电接入，不含负荷、配电接入或表后项目；适合历史退出率、投运周期、发电和储能供给筛查，不代表数据中心待接入负荷 | 年度基线，A 级；数据文件 CC BY 4.0，须署名 LBNL 与 GridTracker |
| [CAISO Generator interconnection](https://www.caiso.com/generation-transmission/generation/generator-interconnection)；首页与队列入口可读 | 公开队列涵盖 Active、Complete、Withdrawn；Cluster 15 文件页面日期 2026-07-16；Resource ID 报告页面日期 2026-10-05 | 这是发电资源接入，不能映射成 AI 园区负荷。公开首页列完整流程；一些详细研究附件位于需要权限的 Market Participant Portal；本次直接 XLSX 抓取失败，未宣称解析项目行 | 每周检查新版文件 + 月度快照；A 级元数据，附件权限逐项记载 |
| [PJM 2026 Load Forecast](https://www.pjm.com/-/media/DotCom/library/reports-notices/load-forecast/2026-load-report.pdf)；36 页 PDF 可读 | 2026-01-14 发布；提供区域、LDA、Zone 的 20 年峰值/电量预测；B-9/B-9b 负荷调整表另有 Excel；模型历史数据截至 2024/2025，具体段落各有截止日 | 公开报告把近期开工/供电承诺视为 firm，远期 non-firm 折减；它是经过筛查的负荷预测，不是完整逐项目数据中心申请库，也不是未来实际耗电 | 年度基线 + Load Analysis Committee/调整材料变化监控；A 级，但预测性质必须保留 |
| [ERCOT LLWG 2026-09-17](https://www.ercot.com/calendar/09172026-LLWG-Meeting) 与 [QSA/IROL 原文](https://www.ercot.com/files/docs/2026/09/16/QSA-Results-and-Large-Load-IROL-Mitigation-Plans_final.pdf)；公开材料可读 | 会议发生 09-17，文件上传 09-16；季度稳定性评估、群组获准容量、最大非同步/同步消费、模型和爬坡安排 | 原文给出 NORTH_LL 获准 5,465 MW、最大同步消费 1,615 MW；并说明部分已送电计算负荷消费 <5 MW、远落后于 LCP 爬坡。群组有交叉，不能相加成整个 ERCOT 市场，也不是按客户公开完整队列 | 月度 LLWG/PUCT/董事会文件；A 级事件证据。大负荷“获准容量 ≠送电获准 ≠实际消费”必须成为字段，而不是脚注 |
| [EIA-860M](https://www.eia.gov/electricity/data/eia860m/index.php)；网页与月份下载链接可读 | 2026-09-24 发布 August 2026 文件，下一次 10-23；≥1 MW 电站现有、计划、退役机组，月度 XLSX，正式基线来自年度 EIA-860 | 补充并网队列的已在建/近期开机信息。EIA 明说它是初步估计，之后月份可无特别说明修订，不是设施方容量承诺；也不是大型负荷数据库 | 月度优先；每期保留版本，差分应识别回溯修订；A 级 |
| [FERC eLibrary 搜索说明](https://elibrary.ferc.gov/eLibraryhelp/General_Search.htm) 与 [文档权限分类](https://www.ferc.gov/related-document-classes)；帮助页可读，样本文件列表抓取失败 | 案号、子案号、accession、Filed/Posted 两个日期、Issuance/Submittal、Public/CEII/Protected/Privileged；公开规则、tariff 和当事人提交材料可形成事件链 | Public 原文和决定适合确认费用分摊、服务条件、共址等制度边界。目录有索引不等于附件公开；非公开工程资料不得视为可自动取得。提交方的预测/请求与委员会决定要区分 | 按有限案号白名单跟踪，不全站深读；B 级自动接入（内容本身可为 A 级，技术接入未跑通） |

ERCOT 的 [2026-08-19 Data Center 听证材料](https://www.ercot.com/files/docs/2026/08/19/ERCOTPanel1DataCenters.pdf) 另公开说明批次研究将年度 MW 分配、财务承诺和 Load Commissioning Plan 联系起来。这比媒体的“总申请 GW”更接近可执行容量约束。工作重点应是追踪阶段变化、地区差异和条件，不是频繁复述同一请求总量。

FERC 共址案可用 [2025-12-18 官方 fact sheet，EL25-49 等案](https://www.ferc.gov/news-events/news/fact-sheet-ferc-directs-nations-largest-grid-operator-create-new-rules-embrace) 作为导航，再追实际决定与后续 tariff。Fact sheet 是发现入口，法律或费用结论应引用具体案卷原文。

## 2. 许可：公开度很高，但按项目追踪的工作量最大

### 实际查到的 MDEQ 样本

[MDEQ 近期许可活动列表](https://opcgis.deq.state.ms.us/ensearchonline/epd-activity-search.aspx) 无需登录，可按县和事件日期读取；2026-10-08 实测页面已有 10-06 条目。其列出 MZX Tech LLC 于 2026-09-14 获施工 general permit 修改。打开 [AI ID 12592 设施页](https://opcgis.deq.state.ms.us/ensearchonline/ai_info.aspx?ai=12592)，得到：

- 物理地址 2875 Stanton Road, Southaven；历史主体和旧许可别名，能减少资产换名造成的漏报。
- Air-Construction PSD 许可 0680-00119，2026-03-11，状态 Permit Issued。
- MSR109658 施工许可修改，2026-09-14。
- 水预处理许可 MSP092491，2026-07-09 状态 Additional Information Requested from Applicant。
- 同页“Active Coverages”及“Current Status”对 MSR109658 出现 Modification 与 Coverage Terminated 的冲突；页面声明行政档案为准，数据库可能不完整。抓取成功不等于状态已经核实。

另一个 [AI ID 90524，Project Tulane](https://opcgis.deq.state.ms.us/ensearchonline/ai_info.aspx?ai=90524) 使用不同地址和建设覆盖号 MSR109819。仅用 MZX/公司名把两条记录合并，会丢失项目和许可类别的区别。本次只确认这些公开行政记录；未用它们直接推导已建设的 GPU、已运行 MW 或收入。

**可纳入**：土地/园区项目 ID、parcel/地址、申请主体及历史别名、许可 ID、许可类型、申请/批准/到期/修改日期、当前行政事件、原文链接、原始附件可用性、关联公用事业。

**不能自动推导**：雨水施工许可不是建筑验收，也不是空气许可、用水许可或电力服务承诺；空气建设许可不是全部机组实际运行；按同一地址出现许可也不必然对应相同业主/园区阶段。

### 土地规划与地方听证

[Loudoun 官方 Data Center Standards & Locations](https://www.loudoun.gov/5990/Data-Center-Standards-Locations) 可读，链接到 LandMARC、既有/拟建园区 GIS、规划委员会和监事会材料。项目 ID CPAM-2024-0001 / ZOAM-2024-0001、2025-03-18 Phase 1 批准、祖父条款以及 Phase 2 都可追溯。其官方说明公众意见通常并入听证前公布的 staff report。

[2026-09-15 暂停审议程序新闻](https://www.loudoun.gov/m/newsflash/home/detail/10874) 使用的措辞是未来考虑一个可能暂停的 resolution，不能仅因媒体标题写成已经全面暂停许可。规划/听证案可提前揭示噪声、用水、退界、变电站和道路等限制，属于正式监管程序证据，关联园区建设与冷却、MEP、变电设备主题。

**适合先建区域试点，而不是全美国全县覆盖**：按 20–30 个重点项目/有限州县监控；政府平台异构、SPV 别名、扫描附件、GIS/地址归并和程序状态比抓取本身更费人工。必须保留“申请/建议/通过/签发/上诉/生效”等动作词。

## 3. 贸易：适合月度实物流向验证，不能当 AI 芯片台数数据库

| 平台 | 2026-10-08 实测与公开边界 | 可用性和归类 |
|---|---|---|
| [Census HS exports 元数据](https://api.census.gov/data/timeseries/intltrade/exports/hs.html)、[当前 key 规则官方通告](https://content.govdelivery.com/accounts/USCENSUS/bulletins/41aaf23) | 元数据公开；匿名请求 HS8486/2026-07 返回 **HTTP 200 + text/html + Missing Key**，不是 JSON 数据成功。2026-06 通告明确所有数据查询需要 key，metadata 例外 | 美国月度商品×国家×区/运输方式，价值、重量和数量可用；免费凭证接入项；不能沿用旧的“500 次内不用 key”经验 |
| [USITC DataWeb API guide](https://www.usitc.gov/applications/dataweb/api/dataweb_query_api.html)、[网页/API 区别](https://www.usitc.gov/faq/question/how_do_i_use_sitequery_data.htm) | 官方指南可读；API 要注册账号、Login.gov 身份认证和 key，6 个月后需重生成；本次未登录或创建账号，未执行带 key 查询。官方 FAQ 说多数网页查询无需登录，与保存/共享/API 分开 | 美国贸易/关税分类最适合国家×细税号核对与关税政策连接。不是无凭证 runner 默认接口；与 Census 同源口径不能作为双重独立确认 |
| [UN Comtrade 免费档](https://comtradeplus.un.org/Subscriptions)、[匿名样本](https://comtradeapi.un.org/public/v1/preview/C/A/HS?period=2025&reporterCode=842&cmdCode=8486&flowCode=X&partnerCode=0&partner2Code=0&customsCode=C00&motCode=0&maxRecords=1) | 匿名 preview 实测 JSON count=1；2025 美国 HS8486 对全球 primaryValue/fobvalue=19,266,066,639，qty=0、isQtyEstimated=true、isReported=false、isAggregate=true。免费注册档文档为 500 calls/day、1/sec、100k/请求；Bulk/Async 为付费档 | 全球交叉验证与缺省基线可用。此次年度样本只是接口/字段验证，不能代表最新月度设备出货；数量缺失/估计标记必须入库，0 不能当 0 台 |
| [日本财务省检索](https://www.customs.go.jp/toukei/srch/indexe.htm)、[下载路由](https://www.customs.go.jp/toukei/info/tsdl_e.htm)、[发布日历](https://www.customs.go.jp/toukei/calendar/calend_e.htm)、[e-Stat API 规则](https://www.e-stat.go.jp/api/api/api/index.php/en/api-info/api-guide) | 官方检索和 e-Stat 下载路由可读；API 需注册 Application ID。日历注明 2026-08 详细数据 09-29 发布，2026-09 详细数据预计 10-29；本次未执行带 ID 的产品样本 | 日本设备/电子元件出口的更细月度验证源；月中速报不能冒充完整九位产品表，修订/确定版要保存 |
| [台湾海关数据集 6053](https://data.gov.tw/dataset/6053) 与 [GA30 查询入口](https://portal.sw.nat.gov.tw/APGA/GA30E) | 6053 页面可读：月度、免费、政府开放资料授权、CSV 链接；字段只有总进出口/复进口/复出口金额，2026-09-18 是 metadata 更新时间。GA30 web 抓取失败，不能据 6053 声称细产品 API 已跑通 | 总贸易 CSV 可用，但对半导体设备/AI 服务器细税号没有足够分辨率。台湾细产品/目的国必须另做 GA30 下载流程验证或官方更细统计源 |

### 产品税号的底层工作

建议用 HS 8486（半导体制造设备）、8504（变压器/变流器等）、8541（半导体器件）、8542（集成电路）作为**探索起点**，进一步核验当年 HS/HTS/各国扩展税号的定义和变更。四位税号过粗：8504 既不专属于 AI 园区变压器，8542 不能识别 GPU/HBM，芯片装入服务器后可能进入整机税号；金额变化还含 ASP、产品结构、币值、转口/复出口。

第一期只做 10–20 个经核对的细税号、3–5 个报告国/目的国，保留 classification/version、flow、reported/estimated、value basis、currency、quantity unit、report period、publication/vintage、revision。不能把镜像进口出口重复加总，也不能用 FOB/CIF 差额当利润。

## 4. BIS / Federal Register：高价值的事件源

[BIS 2026-01-13 公告](https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china) 可读并直链 [2026-00789 正式规则页面](https://www.federalregister.gov/documents/2026/01/15/2026-00789/revision-to-license-review-policy-for-advanced-computing-commodities)：规则类型 Final rule、生效 2026-01-15、相关 CFR Parts 742/744/748、阈值和附加提交要求均可追溯。这说明公告日期、刊登日期和生效日期必须分开。此次把该条作为公开性样本，不据此宣称它就是 10-08 所有当前出口规则的完整汇总。

应跟踪规则文号/RIN、action（proposed/final/correction）、发布日期、effective date、相关 ECCN/CFR、地区与最终用户条件、截止日、被修改或替代规则、官方 PDF。当前合并条文另可追 [BIS EAR 740](https://www.bis.gov/regulations/ear/740)。新规/撤销/过渡期适合每日增量，重大更改人工检查 30–90 分钟；一般日常只做元数据筛选。

可以证明法定许可条件和状态变化，不能证明某一笔商业许可已经获批或某客户已经收到芯片。新闻稿不能替代细条文，proposed rule 不能当成已生效。FederalRegister.gov 自述 HTML 属信息展示，法律审查宜核对其 govinfo 官方 PDF。

## 5. 核燃料：NRC 许可与 DOE 采购应同时进入

当前行业索引已有“核燃料循环与浓缩服务”。[NRC 燃料设施许可/建设状态](https://www.nrc.gov/facilities-safety/fuel-cycle-facilities/new-fuel-cycle-facility-licensing) 明确一些获许可设施并未推进建设，适合检验“license ≠有效供给”。[General Matter 2026-01-22 公共会议信息](https://www.nrc.gov/public-meetings-hearings/public-meeting-schedule/20260011) 可验证预申请技术沟通，而非商业浓缩已投产。

[NRC ADAMS developer guide](https://adams-search.nrc.gov/assets/APS-API-Guide.pdf) 可读，REST JSON 有按 AccessionNumber 取文档和布尔/过滤搜索；API 要注册并持 subscription key。本次核验指南和公开门户，未带 key 请求。其公开文档页称每日分批发布新文件，适合按少量公司/设施/案号追踪，不应每天深读全部核行业文档。技术字段保留 docket、accession、DocumentDate/DateAdded、title、document type、设施/公司、original PDF 与文本。

[DOE HALEU enrichment 项目页](https://www.energy.gov/ne/haleu-enrichment-services) 可读，明确初始可竞争 IDIQ 对象与随后 task orders 分开；2026-01-05 的 task orders 分列 ACO 与 General Matter 各 900m 美元，获框架合同不等于金额全部实现。适合核燃料阶段（转化、LEU/HALEU 浓缩、去转化、燃料制造）对应的许可、拨款、采购、交付和产能证据链。不能把所有环节都算同一浓缩收入，也不能把核电建设新闻直接换算核燃料即时销量。

## 6. 给 research-runner 的分类和工作量

这里的工时为探索后的规划估计，尚无生产任务基准测试。单位按“一个稳定平台/一个辖区/一个产品代码篮子”，不能按 91 个行业每次重复采集。

| 证据族 | 建议运行单元和节奏 | 首次接入估计 | 持续工作估计 | 适合的 runner 负载 |
|---|---|---|---|---|
| 发电与储能接入 | 平台×新版文件，周检测/月快照；LBNL 年更 | 单源 1–3 人日，另需统一项目 ID 与阶段 | 3 个平台每周人工 30–90 分钟；年度基线半日 | 下载/解析/差分为确定性任务；变化摘要才进入模型 |
| 大型负荷接入与消费 | 区域×公开会议/预测/稳定性文件，月/季度 | PJM/ERCOT 合计 3–6 人日 | 月度 2–4 小时；重要制度调整另算 | 列表检测→只读新文件→抽取状态及口径；同源跨专题共用 |
| 园区和厂务许可 | 项目×辖区×许可事件，周 | 2–3 个辖区 + 20–30 项目 5–10 人日 | 每周 3–8 小时，复杂项目 30–90 分钟/事件 | 限定项目白名单；地址/SPV 归并与冲突状态需要人工 |
| 设备贸易 | 报告国×商品篮子×最新月份，月 | 细税号定义、单位、镜像与修订 3–5 人日；凭证接入另计 | 月度 2–4 小时维护解读，采集成本较低 | 参数化 API/CSV 采集，确定性同比/环比，不让模型猜税号 |
| 政策与监管 | 官方规则 ID/案号×增量，日检测 | 2–4 人日 | 普通周 1–2 小时；每项重大规则 0.5–1.5 小时 | 日检元数据，小批次新文档；proposal/final/effective 事件必须保留 |
| 核燃料许可/采购 | 设施/案号/供应商×增量，周 | 2–3 人日 | 每周 1–2 小时 | 许可、采购与交付分开；优先相关设施过滤 |

### 入库合同

每条至少保存：source/source URL、source item ID、原始文件 hash、公开/访问状态、抓取时间、发布时间、事件时间、经济期间、对象 ID/公司/项目/地址、行业多标签、动作和旧/新状态、单位及口径、证据等级、原文定位、已确认/冲突/待核验。网页日期与数据期间不能复用一个 date 字段。

各源设置 watermark、rate limit、原文缓存、去重、有限重试；200 页面必须验证 Content-Type/schema。权限缺失、网页结构变更、无更新和事实缺失是不同状态，不能都写“无新信息”。源更新完成与行业研究成功应分开记录。

行业上游消费应采用 cutoff 下的最新可用快照 + 截止前增量事件 + 待核验缺口。新文件晚于研究截止日不得进入历史回测。行业标签多对多，不为每个行业拷贝同一事实文件。申请 MW、获准 MW、预期爬坡 MW、最大同步 MW、实际电量必须保留不同变量。

### 接入顺序

1. 先接 EIA-860M、LBNL、PJM 公开负荷调整/预测、ERCOT LLWG/PUCT 和 BIS/Federal Register：公开原文质量好、覆盖面大、范围可控。
2. 并行做 MDEQ/Loudoun 项目许可小试点，建立项目 ID 与状态机；它可能比会议更早，但全国化维护成本最高。
3. Comtrade preview 可先验证字段和少量篮子；Census、USITC、日本 e-Stat、NRC ADAMS 完整 API 为免费凭证接入项。只在真正实施且用户愿意提供其自有凭证时配置，不能称为匿名可用。
4. 台湾细产品数据与 CAISO 附件保持“入口确认、细粒度抓取未验证”状态，投入下一轮特定接口试验。公开入口存在不构成 runner 已可自动采集的证据。

## 实测覆盖与局限

已实际打开：LBNL、CAISO 入口、PJM PDF、ERCOT PDF/会议、EIA-860M、MDEQ 两个设施及活动列表、Loudoun 规则入口、Census metadata、USITC guide、Comtrade API 匿名记录及免费档、日本检索/下载日历与 e-Stat guide、台湾开放数据 metadata、BIS/FR 原文、NRC guide/设施/会议、DOE 页、FERC 帮助和权限分类。

已实际发 HTTP：Census 匿名数据请求得到 Missing Key HTML；Comtrade 匿名 preview 得到 JSON 样本。普通沙箱网络首次 DNS 失败，经批准的只读直连后重验成功；不能把沙箱 DNS 失败写成平台封禁。

未验证：任何需要账号/key 的生产 API、全量/定期运行、跨源项目实体匹配、许可 PDF 完整性、贸易细税号完整映射、平台批量采集的条款和频率稳定性。本文的 A/B 等级区分资料权威和技术接入成熟度，不是经济结论置信度。
