# CRWV / CoreWeave 公司情绪研究

> 本报告只研究消息、市场情绪、叙事传播与未来三个月的情绪催化，不预测股价、收益率、目标价或交易路径，不构成估值判断、基本面评级、技术分析或投资建议。

## 研究元数据

| 项目 | 内容 |
|---|---|
| 报告版本 | v1.0；原始判断版本，后续复盘不得覆盖 |
| 报告日期 | 2026-07-16 |
| 信息截止时间 | 2026-07-16 05:50 PDT（UTC-7，美国太平洋夏令时） |
| 回看窗口 | 2026-04-16 00:00 PDT—2026-07-16 05:50 PDT |
| 前瞻窗口 | 2026-07-16—2026-10-16 |
| 股票代号 | CRWV |
| 公司名称 | CoreWeave, Inc. |
| 交易所 | Nasdaq Global Select Market；Class A Common Stock |
| 证券说明 | 美国本土上市普通股，不是 ADR/OTC；本窗口内未发生 ticker 变更 |
| 研究边界 | 只做情绪面；已发生的财务、价格、卖方目标价、短仓和期权数据仅作为预期与传播材料 |
| 独立性 | 从公司、SEC、合作方、行业机构、媒体、卖方二级转述、交易数据与公开社区重新取证；未读取或继承项目内旧情绪报告、基本面结论、技术面信号、排序或特征量化结果 |

### 口径与评分

- `事实`：公司、SEC、政府、合作方或可核验第三方已经披露的内容。
- `推断`：由事实推导、但尚未被直接确认的解释。
- `情绪`：市场参与者正在传播、相信或担心的内容；不等于事实。
- 来源层级：`L1` 为 SEC、政府、公司或合同对手方正式披露；`L2` 为可复核的独立行业测试/研究；`L3` 为主流财经或专业媒体；`L4` 为卖方二级转述、聚合数据；`L5` 为社区内容。
- 可靠性、重要性、新颖度均为 1—5：5 最高。重要性衡量对 CRWV 市场叙事的改变能力，不代表正面程度。
- 事件按“根事件”去重。同一财报、融资、产品发布或地方许可事件的媒体、卖方和社区反应只作为传播链，不重复计为新事实。

### 研究限制

1. 社区样本来自无需登录即可核验的 Reddit 代表性讨论，不是全量舆情抓取；X、付费通讯、Discord 和封闭社区覆盖不足。
2. 卖方观点多来自媒体二级转述，无法核验完整模型和合规披露，因此只用于判断叙事方向。
3. 短仓百分比因数据商使用不同的流通股/可交易股分母而差异很大；本报告优先使用空头股数及其变化，不用单一百分比制造精确感。
4. 期权数据是第三方单时点快照，且页面内部对隐含波动率有轻微口径差异，只能表示拥挤和分歧，不能表示未来价格方向。
5. 截止时，公司尚未正式公告 2026 年第二季度财报日期。前瞻中的“8 月上旬至中旬”是基于定期报告义务和过去披露节奏的窗口推断，不是公司日程。

## 结论摘要

### 当前判断

**CRWV 当前情绪为“高热度、高分歧、短期解释偏负面；可靠事实本身则是正负混合、略偏正向”。**

最近三个月最可靠的新事实包括：Q1 收入和积压需求继续大幅扩张、Vera Rubin NVL72 完成早期验证、MLPerf Training v6.0 获得可复核的规模化训练纪录、公司进入 Nasdaq-100、欧洲即时容量和分层存储合作落地。这些事实继续支持“AI 原生云具备真实需求和技术执行力”的主叙事。[P3][P9][P11][P12][P13][P14]

但市场的边际问题已经从“有没有 AI 需求”转为“巨额已签需求能否按期变成可计费容量和收入，并在融资成本、客户集中、地方交付和内控约束下稳定兑现”。Q1 发布后，低于高预期的 Q2 收入指引、高资本开支和利息支出成为传播焦点；6—7 月又叠加高息无担保债、创始人持续出售股份、Meta 可能出售剩余 AI 算力的媒体报道，以及 Hammond 项目协议到期。于是，同一组事实被多空双方解释成完全不同的故事。[P4][P6][P10][P16][M1][M2]

### 市场当前相信什么、担心什么、忽略什么

| 问题 | 当前占优的内容 | 本报告判断 |
|---|---|---|
| 市场相信什么 | AI 计算需求强；CoreWeave 可以比传统云更快部署最新 NVIDIA 系统；约 1000 亿美元积压订单提供长期可见度 | 前两点有产品、客户和基准事实支撑；“积压订单等于可无摩擦兑现的收入”仍是推断 |
| 市场担心什么 | 债务与利息、高资本开支、客户集中、交付延迟、客户自建/转售算力、创始人减持、内控薄弱 | 多数担忧有 SEC 或政府披露中的事实内核；“因此必然违约、欺诈或失去大客户”没有证据 |
| 市场容易忽略什么 | 约 1000 亿美元并非全部近期收入；36% 的 SEC RPO 预计在 24 个月内确认，合同还包含可用性抵扣、交付延迟和转售容量等变量 | 这是未来三个月最重要的认知校正点：需要观察“部署—通电—计费—现金回收”链条，而不是只看合同 headline |
| 正面叙事容易忽略什么 | 基准纪录、硬件首发和 Gartner 定位不等于客户采用、利用率、按时交付或融资成本改善 | 公司新闻密度高，但独立的新需求事实少于新闻数量 |
| 负面叙事容易忽略什么 | Meta 云业务报道尚未由 Meta 正式确认具体范围，也没有证据显示其已取消与 CoreWeave 的现有合同；创始人近期交易多来自预先设定的 10b5-1 计划 | 负面事实不能被无证据地放大成合同终止或管理层“逃跑” |

### 最近三个月的叙事迁移

| 阶段 | 主要触发 | 主流解释变化 |
|---|---|---|
| 4 月下旬 | 首封股东信、SUNK 扩展 | 延续“AI 从实验走向生产、CoreWeave 从 GPU 租赁走向全栈云”的公司主叙事；新颖度有限 |
| 5 月上旬 | Q1 财报、Q2/FY26 指引 | 争论从订单规模转向兑现节奏。收入和积压订单强，但低于市场高预期的下一季收入指引、利润率和利息支出压制解释 |
| 5 月中旬—6 月中旬 | Kimi、Sandboxes、Agentic AI、Vera Rubin、MLPerf | 技术能力获得更多可验证证据；同时，产品发布被质疑为“基准与营销多、商业采用指标少” |
| 6 月中下旬 | 高息票据、Nasdaq-100、Backblaze、Conapto | 指数纳入带来机构关注；基础设施继续扩张，但融资和供应承诺让“资本密集度”重新成为焦点 |
| 7 月上旬 | Meta 云业务报道、Hammond 协议到期、Gartner Visionary | 竞争与交付风险成为边际主线；Gartner 提供正面品牌材料，但不足以抵消对客户自建、地方执行和融资的追问 |

### 核心分歧

1. **积压订单是护城河，还是长期交付义务？** 多头强调近 1000 亿美元需求可见度；空头强调只有 36% 的 RPO 预计在 24 个月内确认，且兑现依赖电力、设备、施工和 SLA。
2. **“首发最新 NVIDIA 平台”是商业优势，还是高资本开支的加速器？** Vera Rubin 和 MLPerf 支持技术执行；它们尚未证明新增客户、规模利用率或融资回报。
3. **债务是与合同匹配的项目融资，还是脆弱性来源？** 管理层强调容量已售出和贡献利润；SEC 文件同时显示高息融资、较大近期偿债额和持续资本承诺。
4. **大客户自建/出售算力是互补，还是替代？** 目前只有媒体报道和评论，没有 Meta 对具体产品、时间和现有 CoreWeave 合同影响的正式说明。
5. **创始人减持是常规流动性安排，还是信心信号？** 10b5-1 计划降低了单笔交易的信息含量；规模大、频率高仍持续影响治理观感。

## 最近 3 个月重要消息

### 根事件表

| 事件ID | 首次公开时间（PDT/当地日期） | 事件摘要与根来源 | 来源层级 | 事实/推断/情绪 | 可靠性 | 重要性 | 新颖度 | 情绪方向 | 传播阶段 | 叙事影响 |
|---|---|---|---|---|---:|---:|---:|---|---|---|
| E01 | 2026-04-22 | CEO 首封年度股东信，以 2025 年数据强化“全栈 AI 云、推理时代、财务纪律”框架 [P1] | L1 | 事实：公司沟通；情绪：正面定调 | 5 | 2 | 2 | 正面 | 衰退 | 更多是既有叙事重述，不是新订单或新交付 |
| E02 | 2026-04-30 | SUNK Self-Service / Anywhere 发布，扩展到多云与本地环境 [P2] | L1 | 事实：产品发布；推断：可扩大企业采用 | 5 | 2 | 3 | 正面 | 稳定 | 支持从裸算力走向软件层，但无采用/收入指标 |
| E03 | 2026-05-07 | Q1 财报、Q2/FY26 指引、电话会及 10-Q 构成一个根事件 [P3][P4][P5][P6] | L1 | 事实+市场解释 | 5 | 5 | 5 | 混合，交易解释偏负面 | 分化 | 需求与积压订单强化；兑现节奏、资本开支、利息和集中度成为新焦点 |
| E04 | 2026-05-11 至 05-28 | Kimi K2.6 推理基准、Sandboxes、训练—推理—观测—RL 闭环；视为同一“agentic/生产 AI 产品栈”传播簇 [P7][P8] | L1/L2 | 事实：产品与测试；推断：商业采用 | 4 | 3 | 3 | 正面 | 稳定 | 强化软件栈叙事，但多次发布不能重复当成多项独立需求事实 |
| E05 | 2026-06-01 | 宣布完成 NVIDIA Vera Rubin NVL72 的早期 bring-up 与验证；Dell 和 NVIDIA 披露提供交叉印证 [P9][X1][X2] | L1 | 事实：交付/验证；推断：商业规模领先 | 5 | 4 | 5 | 正面 | 扩散后稳定 | 最新硬件执行力证据强；“已规模化产生收入”尚未验证 |
| E06 | 2026-06-09，代表性后续披露至 07-13 | Bloomberg Law 汇总 IPO 后创始人售股约 23 亿美元；近期 SEC Form 4 显示持续计划内出售 [M1][P18] | L1/L3 | 事实：出售；情绪：治理与信心担忧 | 5 | 4 | 4 | 负面 | 拥挤/反复再传播 | 10b5-1 计划是关键反证，但规模和频率形成持续情绪压制 |
| E07 | 2026-06-11 / 06-18 | 定价并完成 12.5 亿美元、票息 9.625%及 20 亿欧元、票息 8.5%的 2032 年无担保优先票据 [P10] | L1 | 事实；情绪：融资能力与高成本并存 | 5 | 5 | 4 | 混合偏负面 | 稳定 | “仍能融资”与“资本/利息负担高”同时成立 |
| E08 | 2026-06-12，06-22 生效 | 获纳入 Nasdaq-100 [P11] | L1 | 事实：指数事件；情绪：机构关注 | 5 | 3 | 4 | 正面/中性 | 已兑现 | 是机械资金与知名度事件，不是经营质量的新证据 |
| E09 | 2026-06-16 | MLPerf Training v6.0：在 8,192 张 GB300 GPU 上训练 DeepSeek-V3 约 2.02 分钟；MLCommons 独立结果支持近线性扩展 [P12][X3] | L1/L2 | 事实：基准；推断：客户价值 | 5 | 4 | 5 | 正面 | 扩散后稳定 | 是窗口内最强技术反证之一，但基准不等于利用率和利润 |
| E10 | 2026-06-23 | 与 Backblaze 签署 5 年、3.35 亿美元、多 exabyte 存储协议 [P13] | L1（合同对手方） | 事实：供应/基础设施合同 | 5 | 3 | 4 | 混合偏正面 | 形成 | 扩展分层存储能力，也增加长期供应承诺；不是 CRWV 客户收入 |
| E11 | 2026-06-24 | 与 Conapto 合作扩展瑞典容量，初始容量已在 Stockholm 4 South 上线 [P14] | L1 | 事实：容量上线；推断：欧洲需求 | 5 | 3 | 4 | 正面 | 形成 | 提供即时容量证据；未披露 MW、客户或经济条款 |
| E12 | 2026-06-29 | ARIA 进入预览、W&B Weave Agent Developer Platform GA [P15] | L1 | 事实：产品状态；推断：采用 | 5 | 2 | 3 | 正面 | 形成 | 延续 agentic 软件叙事，暂缺独立使用量证据 |
| E13 | 2026-07-01 | 媒体称 Meta 研究出售剩余 AI 计算容量；Meta 未评论，市场把它解释为 neocloud 潜在竞争 [M2][M3] | L3 | 事实：报道存在；推断：产品与合同影响；情绪：负面 | 3 | 5 | 5 | 负面 | 扩散/分化 | 把客户集中和“客户变竞争者”推到主叙事中心；不能推断现有合同已取消 |
| E14 | 2026-07-01 | Hammond 市政府宣布 301 Digital Crossroads 项目开发协议在两次延期后到期，6 月 30 日期限前里程碑未满足，且不再延长当前协议 [P16] | L1（政府） | 事实：单一项目协议到期；推断：全公司交付能力 | 5 | 4 | 5 | 负面 | 形成 | 提供罕见的地方执行反证；不能由一处项目外推全部容量计划 |
| E15 | 2026-07-09 | 公司称被 Gartner 2026 Cloud AI Infrastructure Magic Quadrant 评为 Visionary [P17] | L1/L2（公司转述第三方） | 事实：入选定位；情绪：品牌验证 | 4 | 3 | 4 | 正面 | 形成 | 提升企业采购讨论度；Visionary 不等于 Leader，也不等于新合同 |

### 最重要根事件的事实、推断与情绪拆分

#### E03：Q1 财报——最强的正负叙事共同源

**已经确认的事实：**

- Q1 收入 20.78 亿美元，同比增长 112%；公司口径 backlog 为 994 亿美元。SEC 口径 RPO 为 988 亿美元，其中约 36% 预计在未来 24 个月确认、39% 在第 25—48 个月确认，其余在第 49—84 个月确认。[P3][P6]
- 净亏损 7.40 亿美元，净利息支出 5.36 亿美元；调整后 EBITDA 为 11.57 亿美元、利润率 56%，调整后营业利润为 2100 万美元、利润率 1%。[P3]
- Q2 指引为收入 24.5—26.0 亿美元、调整后营业利润 3000—9000 万美元、资本开支 70—90 亿美元、利息支出 6.50—7.30 亿美元；FY26 收入指引 120—130 亿美元、资本开支 310—350 亿美元。[P4]
- Q1 收入中第一、第二大客户占比约 45% 和 20%；应收账款前三大客户占比为 39%、17% 和 22%。SEC 文件还披露，客户协议可能因 SLA、可用性和交付延迟产生抵扣、退款或终止权。[P6]
- 截至 3 月 31 日，债务本金总额约 251.49 亿美元，其中流动债务约 75.47 亿美元；公司披露 IT 一般控制、职责分离和合格人员不足等重大缺陷仍未修复，披露控制被认定为无效，但未称已发现重大错报。[P6]

**合理推断：** backlog 提供了需求可见度，但其兑现速度更接近一个工程和融资问题，而不是单纯的销售问题。通电、设备到场、调试、客户验收、利用率和 SLA 都会影响何时开始计费。

**市场情绪：** 财报次日 CRWV 下跌约 11%，主流报道将反应归因于下一季收入指引低于当时高预期，以及资本开支、利润率和利息负担；与此同时，部分卖方仍强调 2026 年容量大致售罄和积压订单。[M4][S1] 这说明市场并非否认需求，而是在提高对近期兑现证据的要求。

**仍待验证的关键假设：** Q2 实际收入是否落在/高于指引；新增 active power 是否按计划形成收入；高资本开支后的贡献利润是否如管理层所述在数月内出现；客户集中度是否下降；重大内控缺陷是否出现可验证的修复进展。

#### E04、E05、E09、E12：产品与技术传播簇

这组事件共同支持 CoreWeave 的“全栈、最新硬件、面向 agentic AI 的生产云”叙事，但证据强度并不相同：

| 证据 | 能证明什么 | 不能证明什么 |
|---|---|---|
| Kimi K2.6 独立推理榜单 [P7] | 在特定模型、时间和供应商样本中的速度/性价比领先 | 对所有模型长期领先；大客户采用；收入贡献 |
| Sandboxes、Agentic AI 闭环、ARIA [P8][P15] | 产品已发布/预览，CoreWeave 正把 W&B 和算力整合成软件工作流 | 用户数量、留存、跨售率、是否形成独立定价能力 |
| Vera Rubin bring-up [P9][X1][X2] | 最新 NVIDIA 系统已交付并完成早期验证，供应链和工程执行确有优势 | 已大规模部署给付费客户；利用率与经济性 |
| MLPerf Training v6.0 [P12][X3] | 独立、同行可复核的规模训练能力和近线性扩展 | 客户实际工作负载、服务可靠性和合同利润 |

因此，窗口内产品消息的**事实方向偏正面**，但市场已进入“从 demo/benchmark 向商业证明过渡”的阶段。继续发布产品而不披露采用指标，边际情绪作用会递减。

#### E06、E07：融资与治理观感

- 2032 年美元票据票息 9.625%、欧元票据票息 8.5%，定价和交割均由 SEC/公司披露确认。它同时证明资本市场仍提供资金，也显示无担保长期资金成本较高。[P10]
- Bloomberg Law 依据 Washington Service 汇总称，三位共同创始人是 IPO 后约 23 亿美元售股的主要卖方。近期 Form 4 显示，Michael Intrator 在 7 月 7—8 日出售约 36.95 万股，脚注称交易依据 2025-11-20 采纳的 Rule 10b5-1 计划；Brannin McBee 7 月 13 日合计出售约 25 万股，依据 2026-03-05 采纳的计划。[M1][P18]
- **事实结论**只能是“持续、规模较大的计划内出售”。“管理层知道坏消息”“创始人正在逃离”属于没有证据的社区推断；反过来，“10b5-1 所以完全没有信号”也过度简化，因为出售规模、节奏和治理观感仍会影响情绪。

#### E13、E14：7 月负面叙事的两个不同根源

Meta 云业务报道是**竞争/客户战略风险**：媒体称 Meta 可能出售剩余 AI 计算容量，Meta 拒绝置评。报道没有披露产品范围、上线时间、定价，也没有确认其对 CoreWeave 已签合同的影响。[M2][M3] 市场把“客户可能成为供应者”迅速外推到整个 neocloud 模式，传播强度高于证据完整度。

Hammond 则是**地方项目执行事实**：市政府明确称协议在两次延期后到期、里程碑未在 6 月 30 日完成、当前协议不再延长。[P16] 这是高可靠的负面事实，但事件范围限于一个拟建项目和一个特定协议。最需要追踪的是公司是否解释原因、容量是否转移到其他地点，以及该事件是否在其他地方复制。

### 信息边界与去重说明

- Meta 210 亿美元扩展协议、Anthropic 多年协议和 Jane Street 60 亿美元云协议分别在 2026-04-08、04-09、04-14 首次公开，早于本报告 4 月 16 日起点；它们只作为 Q1 叙事背景，不计入本窗口根事件。
- Q1 业绩新闻稿、电话会、指引演示和 10-Q 是同一个财报根事件 E03。
- Kimi、Sandboxes、Agentic AI、ARIA 是同一产品战略的不同交付节点，表中保留可验证节点，但不把媒体转载和社区复述累计为额外需求事实。
- 票据定价和交割是一个融资根事件 E07。
- Nasdaq-100 公告与生效是一个指数根事件 E08。
- BattleBots 赞助属于品牌宣传，未发现其改变客户、容量或财务预期的证据，故不列入重要根事件。

## 情绪分层与核心叙事

### 五层结构

| 层次 | 目前看到的内容 | 情绪含义 | 证据边界 |
|---|---|---|---|
| 事实层 | 约 994 亿美元 backlog、收入高速增长、最新 NVIDIA 平台验证、MLPerf 纪录、Nasdaq-100；同时有高利息/资本开支、客户集中、内控重大缺陷、Hammond 协议到期 | 整体混合，运营/技术略正面，融资/执行负面 | 事实不能自动推出股价或公司最终成败 |
| 主流叙事层 | 媒体从“AI 算力稀缺和大单”转向“能否按期交付、客户会否自建、融资能否持续” | 边际偏负面 | Meta 事件仍是报道而非完整事实；财报反应受高预期影响 |
| 卖方层 | 多数可见二级转述仍保留正面评级，强调 sold-out capacity、backlog 和技术优势；同时承认执行与资本需求是核心风险 | 正面但条件化，与市场交易情绪分离 | 完整研报和模型不可见，可能有投行业务冲突 |
| 社区传播层 | 多头反复传播“1000 亿美元 moat、最新 GPU 首发、债务与合同匹配”；空头传播“创始人卖出、债务、客户自建、项目取消” | 高热度、高极化、证据质量中低 | 同一事实被重复截图、标题化，推断经常越过原始披露 |
| 交易情绪层 | 重要负面解释日出现大幅下跌；空头股数从 5 月底到 6 月底明显增加；期权 put/call 与高 IV 显示防御和分歧 | 偏负面且拥挤，但不是单向共识 | 低 days-to-cover、高成交和指数变动可能混入对冲/套利 |
| 反证层 | 技术基准、供应链交付和新增容量反驳“公司没有真实能力”；高息融资、内控和地方协议反驳“订单会自动兑现” | 双方均有较强反证 | 结论取决于未来实际部署与计费数据 |

### 当前主叙事、次要叙事和反向叙事

| 叙事 | 核心说法 | 主要证据 | 传播状态 | 继续成立需要什么 | 失效条件 |
|---|---|---|---|---|---|
| 主叙事：AI 原生全栈云 | CoreWeave 比通用 hyperscaler 更快获得并运营最新 GPU，并用软件层把训练、推理、RL 和观测连成生产平台 | 大客户合同背景、Vera Rubin、MLPerf、Kimi、SUNK/W&B 产品 [P3][P7][P8][P9][P12] | 高热度，已从形成转为验证 | Q2/Q3 披露 active power、收入转换、可靠性和采用证据 | 部署延迟反复出现；客户转移；产品只有发布没有使用量 |
| 次要叙事：电力与合同是稀缺资产 | 3.5GW 以上 contracted power、约 994 亿美元 backlog 构成长期门槛 | Q1 财报和电话会 [P3][P5] | 多头社区拥挤 | 按期通电、交付和验收；合同实际计费 | 许可/施工延期扩散；客户利用率不足；SLA 抵扣/终止增加 |
| 次要叙事：从 GPU 云升级为软件平台 | W&B、SUNK、Sandboxes、ARIA 可以提高客户黏性和跨售 | 产品发布 [P2][P8][P15] | 公司传播强、独立传播中等 | 披露客户使用、付费、留存和工作流迁移 | 产品采用有限或客户只购买裸算力 |
| 反向叙事：债务驱动的扩张脆弱 | 高成本资本和巨额前置开支把任何延期放大成现金和叙事风险 | 10-Q、Q2 指引、票据 [P4][P6][P10] | 正在升温 | — | 较低成本项目融资、稳定计费和内控改善可削弱该叙事 |
| 反向叙事：客户也会成为竞争者 | Meta 等大客户可自建并出售剩余容量，压缩 neocloud 的中介价值 | 7 月 1 日媒体报道 [M2][M3] | 快速扩散、证据尚不完整 | Meta 正式推出相近服务并影响现有合同/新增订单 | Meta 否认、服务范围互补，或现有合同继续履行并扩大 |
| 反向叙事：治理/执行不足以支撑规模 | 大规模内部人出售、重大内控缺陷和 Hammond 协议到期暴露治理/交付风险 | SEC、政府、Bloomberg Law [P6][P16][P18][M1] | 升温且易情绪化 | — | 内控明确修复、里程碑持续兑现、减持节奏下降可削弱 |

### 传播链条

1. **公司端**高频发布技术首发、基准、产品与合作，建立“速度和最新硬件”议题。
2. **合作方/独立机构**决定信息质量：Dell、NVIDIA、MLCommons、Backblaze 能把公司声明从自证提高到可交叉验证；没有合作方或采用数据的产品稿件信息增量较低。
3. **媒体端**在财报、Meta 报道、创始人售股和地方许可事件上选择“融资/替代/执行风险”框架，产生更大的边际叙事冲击。
4. **卖方端**多数仍以 backlog 和容量售罄进行反驳，但把条件集中在 execution；这并未消除社区和交易层的担忧。
5. **社区端**将复杂披露压缩成“1000 亿美元 moat”或“insiders running”，传播速度快、条件和口径丢失。
6. **交易端**的大幅反应再被社区当成观点正确的证据，形成反馈循环。价格反应只能说明预期受冲击，不能反过来证明原叙事真假。

## 社区与意见领袖情绪

评分口径：证据质量和传播强度均为 1—5；传播强度按页面互动、跨帖复现和议题进入主流讨论的程度作定性判断，不代表精确覆盖人数。

| 日期 | 平台/来源 | 作者/账号 | 核心观点 | 情绪方向 | 证据质量 | 传播强度 | 传播变化 | 偏见/利益冲突 | 叙事作用 |
|---|---|---|---|---|---:|---:|---|---|---|
| 2026-05-08 | Reddit r/CRWV [C1] | BeSmartFiTness | 认为 Q1 很好、下跌过度；评论区指出 Q2 收入指引低于预期 | 帖主正面、评论分化 | 3 | 3 | 财报日快速升温后退潮 | 主题社区与潜在持仓偏差 | 很早暴露“历史业绩强 vs 下一季预期弱”的核心分歧 |
| 2026-07-01 | Reddit r/CRWV [C2] | Lucid_Dreamer5 | 引用 Reuters，强调 Meta 只是“可能”出售剩余容量，neocloud 下跌是过度反应 | 正面/反驳负面 | 3 | 4 | 随 Meta 报道迅速升温 | 明显持仓/主题社区偏差 | 提供重要限定词，但也倾向低估客户自建的长期叙事风险 |
| 2026-07-04 | Reddit r/ValueInvesting [C3] | orishasinc2 | 以约 23 亿美元创始人售股和 Magnetar 历史关系，推导“内部人正在逃跑” | 强负面 | 3（事实核强、外推弱） | 4 | 持续被跨帖复述 | 可能持仓未知；标题化和类比偏差明显 | 把治理观感升级为诚信/生存叙事；后半结论没有 SEC 证据支持 |
| 2026-07-08 | Reddit r/CRWV [C4] | Casztiel | 讨论 Gartner Visionary，认为对采购者可能有参考，但未必直接改变投资者判断 | 温和正面/中性 | 3 | 2 | 稳定 | 主题社区偏差较低 | 抑制“一个评级即可改变基本预期”的过度解读 |
| 2026-07-10 | Reddit r/CRWV [C5] | redditor7488283 | 将短期技术位、Gartner 和 backlog 称为“两个主要催化”；评论区集中反驳债务与执行 | 强正面，评论强分化 | 2 | 4 | 升温 | 可能持仓；把价格技术语言与事实混合 | 体现多空同时有传播能力，不能作为事实来源 |
| 2026-07-13 | Reddit r/CRWV [C6] | redditor7488283 | 声称债务“完美匹配”已签合同、Meta 合同限制转售，因此空头论点无效 | 强正面 | 1 | 3 | 对负面叙事的二次反击 | 持仓倾向明显；关键合同条款未给出原始文件 | 是“强传播、弱证据”的拥挤样本；公开 10-Q 不支持“完美匹配”的绝对表述 |

### 社区结论

- **社区不是简单看多或看空，而是高度极化。** 多头掌握 backlog、基准和硬件首发等真实事实；空头掌握利息、债务、内控、减持和 Hammond 等真实事实。问题出在双方常把局部事实外推为确定结局。
- **多头最常见的证据错误**是把 backlog 等同于近期收入，把技术 benchmark 等同于商业护城河，把 10b5-1 等同于减持完全无信息量。
- **空头最常见的证据错误**是把 Meta 媒体报道等同于合同取消，把单一地方协议到期等同于全公司无法交付，把大额计划内出售等同于欺诈或破产预告。
- **传播热度正在升高，证据质量没有同步提高。** 7 月的负面根事件给社区提供了新的事实内核，随后大量帖子仍在复用同一几项材料，因此帖子数量不应被当成新增坏消息数量。
- **尚未成为主流、但证据价值高的线索**是 RPO 确认期限、合同抵扣/终止条件、内控修复进度，以及每新增 100MW active power 对当季计费的实际传导。这些内容比标题化的目标价或单日涨跌更适合复盘。

## 卖方、媒体与交易情绪

### 媒体与卖方的错位

可见的卖方二级转述整体仍偏正面：财报后有机构强调“2026 年容量大致售罄”和积压订单，Meta 报道后也有机构维持正面评级，认为 Meta 的可能服务不必然替代 CoreWeave。[S1][S2] 但卖方的正面结论都越来越依赖“按时执行”这个条件。

媒体的边际框架更负面：Q1 后关注低于高预期的下一季指引和资本开支；6 月关注内部人出售；7 月关注客户自建/转售算力和地方项目到期。[M1][M2][M3][M4] 卖方与媒体的错位本身提高了分歧度，而不是提供确定方向。

### 已发生的市场反应

- 2026-05-08，Q1 发布后的首个完整交易日，CRWV 约下跌 11%；报道将其与 Q2 收入指引低于当时市场预期、资本开支和利润率担忧联系起来。[M4]
- 2026-07-01，Meta 云业务报道传播后，CRWV 收盘约下跌 13.9%，Meta 约上涨 9%；这是“客户可能变竞争者”叙事获得即时交易确认的表现，但单日反应不能证明报道最终范围。[M3]
- Nasdaq-100 纳入提供机械性关注和潜在被动资金流，但不应被记为正面经营事实，也不能用来抵消上述负面根事件。[P11]

### 空头情绪

| 结算日 | 报告空头股数 | 相比前期 | 数据解释 |
|---|---:|---:|---|
| 2026-04-30 | 约 6121 万股 | — | 已处于较高绝对水平 |
| 2026-05-29 | 约 5460 万股 | 较 4 月底下降 | 财报后并未立即形成持续单边加空 |
| 2026-06-15 | 约 6901 万股 | 较 5 月底上升约 26% | 融资、减持与执行议题升温 |
| 2026-06-30 | 约 8096 万股 | 较 6 月中上升约 17%；较 5 月底上升约 48% | 空头/对冲需求明显增加，日期早于 7 月 1 日 Meta 报道 |

数据商对 6 月底 short float 给出约 **18.1%—27.0%** 的巨大区间，原因是分母分别接近 4.48 亿股和 3.00 亿股；更稳定的事实是空头股数约 8096 万股、半月明显增加。days-to-cover 约 2.6 天，说明成交活跃，不能把高空头比例机械解释为即将发生 squeeze。[D1][D2]

可能的混杂因素包括：Nasdaq-100 纳入相关对冲、可转换/债务头寸对冲、借券供给变化和高成交量。因此，本报告将其判断为**负面观点和风险对冲都在上升**，而不是纯粹的方向性做空结论。

### 期权情绪

第三方在 2026-07-15 的单时点页面显示，CRWV put/call 成交量比约 1.03、未平仓比约 1.77，隐含波动率页面口径约 90%—95%。[D3] 这支持“保护需求高、分歧大”的判断，但存在三项限制：单日数据易受大宗对冲影响；到期日和执行价分布未充分拆分；数据页对 IV 的两个位置显示不同数字。故不据此推断未来方向。

### 内部人交易的情绪权重

内部人出售应给予**中高传播权重、有限方向权重**：

1. 规模大、连续披露，使治理观感和“管理层与股东是否同向”成为持续话题。
2. 代表性近期交易明确写有预先设定的 10b5-1 计划，降低了其对未公开短期信息的指示性。
3. 仍应跟踪计划采纳日期、修订/终止、实际出售节奏、剩余持股和是否出现非计划交易；不能只看媒体累计金额。

## 未来 3 个月消息频率

以下数量是可观察根事件的合理区间，不是新闻稿数量。公司可以发布更多宣传稿，但同一产品/会议传播簇只算一个根事件。

| 消息类型 | 预计频率/数量 | 主要依据 | 重要观察窗口 | 置信度 |
|---|---|---|---|---|
| 正式财报与 SEC | 1 个高重要度财报包；另有若干 8-K/Form 4 | Q2 定期披露义务；内部人计划交易持续 | 8 月上旬—中旬（日期待公司公告）；全窗口 | 高 |
| 客户合同/续约 | 1—3 个可见事件；真正改变叙事的大单可能为 0—1 个 | 公司过去高频签约，但大单并非按月稳定出现 | 财报、Fully Connected 前后 | 中 |
| 产品、基准和技术 | 3—6 个发布/更新，但可能只有 1—3 个独立信息根 | 近三个月产品传播密集，Vera Rubin 和 agentic 产品仍在早期 | 7—10 月；9/29—10/1 会议 | 中高 |
| 容量、通电、园区、许可 | 2—5 个公司或地方层面更新 | 2026 年扩容目标大、多个地点并行，Hammond 提高媒体关注 | 财报；地方会议/许可日程；季度末 | 高 |
| 融资与供应合同 | 0—2 个重要事件 | FY26 资本开支指引 310—350 亿美元，资金需求和设备/电力承诺大 | 财报前后及项目交割时点 | 中高 |
| 卖方与主流媒体 | 每周均有跟进；重要叙事节点约 3—6 个 | 高关注、高空头、高资本需求；财报和 Meta 议题会反复触发 | 财报日、NVIDIA 财报、会议、地方事件 | 高 |
| 社区与意见领袖 | 每日高频；独立高价值论点约 2—5 个 | 主题社区活跃、多空极化 | 财报前后、短仓发布日、重大 headlines | 高 |
| 交易情绪数据 | 空头数据半月一次；期权/成交连续 | 公开结算与市场数据固定更新 | 每月中/月底结算后发布；重大事件日 | 高 |

## 未来 3 个月关键消息与叙事方向

概率采用区间，表示“根事件或实质更新是否出现”；情绪方向是事件出现后最可能的解释，二者彼此独立。

| 可能消息或催化 | 预计窗口 | 发生概率 | 预期情绪方向 | 可能改变的叙事 | 判断依据 | 反证条件 | 置信度 |
|---|---|---:|---|---|---|---|---|
| Q2 业绩、Q3/FY26 指引 | 8 月上旬—中旬；官方日期未公告 | >95% | 条件式、双向 | 从“订单”转到“交付和计费” | 定期披露义务；Q2 指引已有明确区间 [P4] | 收入单点并不足够，需同时看 active power、利息、资本开支和合同转换 | 高 |
| Q2 10-Q 更新客户集中、RPO 时序、债务和重大内控缺陷 | 与 Q2 财报同时 | >95% | 改善则正面；无进展/恶化则负面 | 治理与可兑现性 | Q1 10-Q 已留下明确基线 [P6] | 只有管理层口头表述、无控制测试或职责分离证据，不算实质修复 | 高 |
| Meta 正式确认、否认或细化 AI 云/剩余算力计划 | 7—10 月 | 40%—60% | 范围重叠、低价转售或影响现有合同则负面；互补/无影响则中性至正面 | “客户会否成为竞争者” | 已有主流媒体报道但 Meta 未评论 [M2][M3] | 没有产品范围、价格、时间或合同影响的新事实，只是媒体复述 | 中 |
| Vera Rubin 从验证转入付费客户/规模化部署 | 7—10 月 | 50%—70% | 正面；延迟则负面 | 最新硬件领先能否变现 | 已完成 bring-up，NVIDIA 和 Dell 有交叉印证 [P9][X1][X2] | 仅重复“first”而无 GA、客户、容量或利用率信息 | 中 |
| active power、2026 年末 1.7GW 目标或首个 self-build 的进展 | 财报及 9 月会议 | 60%—80% 会有更新 | 里程碑按期为正面；推迟/口径模糊为负面 | 电力与交付是护城河还是瓶颈 | 管理层 Q1 电话会给出明确目标 [P5] | contracted power 增加但 active/billable power 不增加，不算兑现 | 中高 |
| 新客户/扩单和 backlog 更新 | 财报或重大活动 | 50%—70% | 正面，但取决于客户质量、期限和交付条件 | 需求广度与集中度 | 公司签约节奏强，称 10 个客户承诺至少 10 亿美元 [P5] | 只披露合同总额、不披露期限/启动条件，或集中度上升 | 中 |
| 新债务、项目融资、设备/电力承诺 | 全窗口，财报前后更重要 | 50%—70% | 获得资金为正面；高票息、短期限、无对应交付则负面 | 融资能力 vs 脆弱性 | 高资本开支和近期票据发行 [P4][P6][P10] | 低成本、无追索或与已签客户严格匹配的项目融资可减轻负面解释 | 中高 |
| 其他园区延迟、许可争议或容量迁移说明 | 7—10 月 | 40%—60% | 新延期偏负面；明确替代容量/按期通电偏正面 | Hammond 是孤例还是模式 | Hammond 已提供一项地方级反证 [P16] | 没有官方文件、只是社区地图或传闻，不应计入根事件 | 中 |
| Fully Connected 2026 举办 | 2026-09-29—10-01 | >95%（已官宣日程） | 活动本身中性；有客户采用和 GA 数据则正面 | 软件平台与 W&B 整合 | 公司正式会议页面 [P19] | 只有 demo、愿景和重复产品稿，没有采用指标 | 高 |
| 财报后的卖方评级/目标价调整 | 财报后 1—5 个交易日 | 80%—95% | 方向取决于执行差异；大概率继续分化 | 市场是否仍给 backlog 高权重 | 历次重大事件后卖方反应密集 | 二级媒体只报目标价不报假设，信息质量有限 | 高 |
| 创始人/高管 Form 4 持续披露 | 全窗口 | >80% | 计划内、节奏稳定为中性偏负面；加速或非计划交易更负面 | 治理与信心 | 已有连续 10b5-1 计划交易 [P18] | 单笔小额或税务出售不应放大；需看计划脚注和剩余持股 | 中高 |
| 空头股数继续上升或回落 | 半月数据结算与滞后发布 | 不预测方向 | 上升强化负面拥挤；下降可表示获利了结或观点减弱 | 空头信念与拥挤 | 6 月底空头股数显著增加 [D1][D2] | 必须结合分母、成交量、指数对冲和借券变化 | 中 |

### 条件式三种叙事路径

这不是股价情景，只是未来三个月的消息与解释路径。

1. **基准路径：从“规模故事”进入“季度审计”。** Q2 大致落在指引内，技术/产品发布继续，融资和地方执行担忧不消失。主叙事变成逐项核对 active power、收入转换、利息、RPO 和客户集中；情绪保持高分歧。
2. **正面叙事路径：兑现证据压过融资担忧。** Q2 指引兑现或上修，active power 和付费客户部署清晰，Vera Rubin 出现规模客户证据，内控有实质进展，Meta 服务与现有合同被证明互补。叙事会重新聚焦“速度和稀缺容量”，而不是单纯看宣传数量。
3. **负面叙事路径：多个小反证形成模式。** 收入/交付低于指引、其他园区重复延期、融资成本继续偏高、客户集中不降、Meta 正式进入重叠市场或现有合同受影响。届时 Hammond 会从“单点事件”被重解释为执行模式，创始人出售也会被赋予更强负面含义。

## 情绪判断框架

不计算单一综合分。分数只表示该维度强弱；“高热度”“高可复盘性”不是正面加分。

| 维度 | 判断 | 1—10 | 最重要依据 |
|---|---|---:|---|
| 最近事实方向 | 混合、略偏正面 | 6 | 收入/订单、Vera Rubin、MLPerf、欧洲容量为正；融资、内控和 Hammond 为负 |
| 当前主流情绪方向 | 偏负面 | 4 | 7 月边际叙事集中于 Meta、自建/竞争、交付、债务和减持 |
| 未来消息方向 | 高度条件化、中性 | 5 | 财报和部署可双向解释；活动/产品数量本身没有方向 |
| 负面催化风险 | 中高 | 7 | 高资本需求、客户集中、地方许可、内控和自建竞争均有事实基础 |
| 社区证据质量 | 中低 | 4 | 能找到原始披露，但普遍省略期限、合同条件和反证 |
| 传播热度 | 很高、仍在升温 | 8 | 财报、Meta、内部人和短仓形成连续话题 |
| 多头拥挤 | 中高 | 6 | “1000 亿美元 moat”“首发即护城河”等口号重复，但并非全市场一致 |
| 空头拥挤 | 高 | 8 | 6 月底空头股数约 8096 万股并显著上升；但 days-to-cover 低 |
| 分歧度 | 很高 | 9 | 多空都拥有真实事实、卖方与交易层方向错位、社区评论常即时对冲 |
| 可复盘性 | 很高 | 9 | Q2 指引、1.7GW 目标、RPO 时序、内控、会议和半月短仓均有明确验证点 |

### 推动因素、压制因素与最大不确定性

**正面情绪推动因素：** 独立可复核的性能记录；最新 NVIDIA 平台的供应链/工程领先；大规模 backlog；客户行业扩展；active power 和付费部署按时增加；内控修复。

**负面情绪压制因素：** 高成本资本和巨额前置开支；客户/应收集中；SLA、延迟和容量转售等合同变量；地方开发协议到期；创始人持续出售；客户自建并潜在出售剩余容量。

**最大不确定性不是 AI 总需求，而是时间匹配：** 资本、设备和电力何时支出，容量何时通电，客户何时验收并开始计费，债务何时到期。多头和空头实际上在争论同一条时间轴的不同段落。

## 反证与风险

### 对流行说法的反证表

| 流行说法 | 事实内核 | 被忽略的反证/限制 | 当前结论 |
|---|---|---|---|
| “994 亿美元 backlog 已经锁定未来” | 公司确有大额 backlog/RPO | SEC RPO 只有 36% 预计 24 个月内确认；包含可用性抵扣、交付延迟、转售容量等变量 | 证明需求可见度，不证明无摩擦兑现 |
| “技术第一就是商业护城河” | Vera Rubin、MLPerf 和 Kimi 基准有真实技术证据 | 基准不是采用、利用率、服务可靠性、迁移成本或利润 | 是强正面证据，但仍需商业验证 |
| “债务与合同完美匹配，所以没有风险” | 容量多数有合同，项目融资可与客户现金流匹配 | 10-Q 显示大量流动债务、高利率工具、未来本金与资本承诺；并非所有风险都由客户无条件承担 | “完美匹配”证据不足 |
| “高息发债说明资金链断裂” | 票息高、资金需求大 | 公司仍能发行大额无担保长期债，并称用于一般公司用途和偿债 | 融资能力与高成本同时存在，不等于已断裂 |
| “Meta 已经变成直接竞争者并取消 CRWV 合同” | 主流媒体称 Meta 研究出售剩余 AI 算力 | Meta 未正式说明范围；没有现有 CoreWeave 合同取消的证据 | 重要潜在风险，不是已证实合同事件 |
| “创始人减持证明他们知道公司要出问题” | IPO 后累计出售规模大、近期仍在卖 | 代表性交易来自提前采纳的 10b5-1 计划；没有未公开信息证据 | 治理观感负面，内幕结论不成立 |
| “10b5-1 交易完全不用看” | 预设计划降低择时含义 | 计划规模、修改、终止、出售比例和剩余持股仍影响激励与情绪 | 应降低单笔权重，不应归零 |
| “Hammond 证明所有园区无法交付” | 该协议确因未满足里程碑而到期 | 只是一个 180MW 拟建项目；Conapto 初始容量同时上线，其他地点未因此被证伪 | 是重要单点反证，是否复制要继续观察 |
| “Gartner 已证明 CoreWeave 是行业领导者” | 公司被列为 Visionary | Visionary 不是 Leader；Magic Quadrant 是供应商定位，不是合同、利用率或财务证明 | 品牌/采购讨论正面，经营证明有限 |
| “新闻很多所以情绪应持续向好” | 公司窗口内确有高频发布 | 多条稿件属于同一产品簇；品牌赞助和媒体转载不增加根事实 | 应按根事件和独立验证去重 |

### 必须持续调查的负面风险

1. **交付与地方执行：** Hammond 是否是孤例；其他园区是否出现许可、电力、施工、设备、社区反对或合作方里程碑问题。
2. **客户集中和战略变化：** 前两大客户合计约占 Q1 收入 65%；任何自建、延迟、转售、重新谈判或 SLA 抵扣都可能被市场放大。
3. **融资与期限匹配：** Q2 利息、FY26 资本开支、新融资票息、抵押/无担保结构、近期本金与 active power/计费节奏是否匹配。
4. **内部控制：** ITGC、职责分离和合格人员不足的重大缺陷何时修复；“没有发现重大错报”不等于控制有效。
5. **诉讼：** Q1 10-Q 披露证券集体诉讼和衍生诉讼，公司称其无依据且未计提；需关注法院程序和新增主张，不能把诉讼存在等同于违法成立。[P6]
6. **内部人出售：** 是否仍按原计划，是否出现计划变更、非计划交易、出售占剩余权益比例上升或关键管理人员离职。
7. **产品商业化：** 产品发布、preview、benchmark 与真实客户 GA、付费、留存、利用率之间是否持续存在信息缺口。
8. **循环与关联叙事：** NVIDIA 既是关键供应者/合作方，也可能与融资、硬件采购和客户生态形成复杂关系；社区容易把合作直接解释成无风险背书。

### 截止时间内未找到的重大事实

在本次检索到的 SEC、公司、政府和主流媒体资料中，截至 2026-07-16 05:50 PDT，**未找到已确认的 SEC 执法调查、审计重述、核心管理层离职或 Meta 取消现有 CoreWeave 合同的披露**。这只是对已检索公开来源的否定性观察，不是保证这些风险不存在；后续出现新信息时应新建版本，不能回写本报告。

## 后续跟踪清单

原始判断已在本版本冻结。复盘时只填写后五列，不修改“预计窗口”和“原始判断”。

| 跟踪项 | 预计窗口 | 原始判断 | 实际是否发生 | 实际情绪方向 | 叙事变化 | 是否命中 | 误差原因 | 状态 |
|---|---|---|---|---|---|---|---|---|
| Q2 收入是否落在 24.5—26.0 亿美元指引，Q3/FY26 指引如何变化 | 8 月上旬—中旬 | 事件几乎必然；若只达下沿且交付口径弱，市场解释偏负面；上沿/上修并有部署证据偏正面 | — | — | — | — | — | 待验证 |
| Q2 active power、年末 >1.7GW 和 first self-build 进度 | 财报及 9 月会议 | 是“订单转计费”的最高价值验证点；contracted power 增加不能替代 active power | — | — | — | — | — | 待验证 |
| RPO/backlog、24 个月确认比例和客户集中度 | Q2 10-Q | backlog 增长只有在近期确认比例/客户广度不恶化时才是强正面 | — | — | — | — | — | 待验证 |
| Q2 利息、资本开支、债务本金及新融资条款 | 财报及全窗口 | 仍可能融资；若主要是高票息通用债，负面叙事强化；项目匹配、较低成本可缓和 | — | — | — | — | — | 待验证 |
| 重大内控缺陷修复 | Q2 10-Q | 口头“正在改善”不足；需要明确测试、人员/系统和控制结论 | — | — | — | — | — | 待验证 |
| Meta AI 云/剩余容量的正式范围及对现有合同影响 | 7—10 月 | 发生正式澄清概率中等；在没有原始披露前保持条件式，不写合同取消 | — | — | — | — | — | 待验证 |
| Vera Rubin 付费客户、GA、部署规模或利用率 | 7—10 月 | 预计会有产品更新；只有客户/容量/使用证据才升级为商业正面根事件 | — | — | — | — | — | 待验证 |
| Hammond 原项目解释、替代地点/容量及其他地方项目是否重复延期 | 7—10 月 | 单点负面已确认；若无复制，不外推为全公司模式 | — | — | — | — | — | 待验证 |
| Fully Connected 2026 是否给出客户采用、GA 和整合证据 | 9/29—10/1 | 会议会举办；若只有重复愿景，情绪增量有限 | — | — | — | — | — | 待验证 |
| Form 4 的计划脚注、节奏与剩余持股 | 全窗口 | 计划内交易继续的概率高；加速、改计划或非计划出售更负面 | — | — | — | — | — | 待验证 |
| 半月空头股数与 days-to-cover | 7—10 月 | 不预测方向；用股数、成交和分母共同解释，禁止用单一百分比宣称 squeeze | — | — | — | — | — | 待验证 |
| 是否出现新的大客户根事件而非新闻重复 | 7—10 月 | 预计 0—1 个能显著改变叙事的大单；需核验合同期限、启动条件和客户质量 | — | — | — | — | — | 待验证 |

## 来源与日期

所有网页于 2026-07-16 检索或复核。日期优先使用根来源的首次公开日期；网站列表因 UTC/本地时区可能显示前一日，事件表采用新闻稿正文或监管文件的美国当地公开日期。

### 公司、SEC、政府与合同对手方

- [P1] 2026-04-22，CoreWeave CEO Michael Intrator，[2025 Letter to Shareholders](https://coreweave.com/news/ceo-michael-intrators-2025-letter-to-shareholders)。
- [P2] 2026-04-30，CoreWeave，[SUNK Expands Capabilities to Bring AI Workloads Online Faster—Anywhere](https://coreweave.com/news/coreweave-sunk-expands-capabilities-to-bring-ai-workloads-online-faster-anywhere)。
- [P3] 2026-05-07，CoreWeave IR，[CoreWeave Reports Strong First Quarter 2026 Results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-First-Quarter-2026-Results/)。
- [P4] 2026-05-07，CoreWeave，[Q2 and FY 2026 Outlook Presentation](https://s205.q4cdn.com/133937190/files/doc_financials/2026/q1/CoreWeave-1Q26-Outlook-Presentation.pdf)。
- [P5] 2026-05-07，CoreWeave，[Q1 2026 Earnings Call Transcript](https://s205.q4cdn.com/133937190/files/doc_financials/2026/q1/CoreWeave-Inc-CRWV-US-Q1-2026-Earnings-Call-7-May-2026-5_00-PM-ET.pdf)。
- [P6] 2026-05-07，SEC，[CoreWeave 2026 Q1 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000222/crwv-20260331.htm)。
- [P7] 2026-05-11，CoreWeave，[#1 Ranking for Inference Speed and Price-Performance for Kimi K2.6](https://www.coreweave.com/news/coreweave-achieves-1-ranking-for-inference-speed-and-price-performance-for-moonshot-ais-kimi-k2-6-model-in-independent-benchmark)。
- [P8] 2026-05-14 / 2026-05-28，CoreWeave，[Sandboxes Launch](https://www.coreweave.com/news/coreweave-sandboxes-launches-to-accelerate-reinforcement-learning-agent-tool-use-and-model-evaluation)；[Training-to-Inference Gap for Autonomous Agent Improvement](https://coreweave.com/news/coreweave-closes-the-training-to-inference-gap-for-autonomous-agent-improvement)。
- [P9] 2026-06-01，CoreWeave，[Industry-First Bring-Up and Validation of NVIDIA Vera Rubin NVL72](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Completes-Industry-First-Bring-Up-and-Validation-of-NVIDIA-Vera-Rubin-NVL72/default.aspx)。
- [P10] 2026-06-11 / 2026-06-18，CoreWeave / SEC，[Senior Notes Pricing](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Announces-Pricing-of-1-25-Billion-of-Senior-Notes-and-2-Billion-of-Senior-Notes/default.aspx)；[Form 8-K Closing](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000291/crwv-20260618.htm)。
- [P11] 2026-06-12 / 2026-06-22，Nasdaq，[CoreWeave to Join Nasdaq-100 Index](https://www.nasdaq.com/press-release/coreweave-join-nasdaq-100-index-2026-06-12)；[June 2026 Quarterly Changes](https://ir.nasdaq.com/node/110541/pdf)。
- [P12] 2026-06-16，CoreWeave，[MLPerf Training v6.0 Results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Sets-New-AI-Training-Records-in-MLPerf-Training-v6-0-Training-DeepSeek-V3-in-Approximately-Two-Minutes/default.aspx)。
- [P13] 2026-06-23，Backblaze IR，[Five-Year Multi-Exabyte, $335 Million Data Storage Agreement with CoreWeave](https://ir.backblaze.com/news/news-details/2026/Backblaze-Announces-Five-Year-Multi-Exabyte-Data-Storage-Agreement-with-CoreWeave/default.aspx)。
- [P14] 2026-06-24，CoreWeave，[Conapto Partnership to Expand AI Cloud Capacity in Sweden](https://www.coreweave.com/news/coreweave-partners-with-conapto-to-expand-ai-cloud-capacity-in-sweden-powered-by-renewable-energy)。
- [P15] 2026-06-29，CoreWeave，[ARIA Launches as an AI Research and Iteration Agent](https://www.coreweave.com/news/coreweave-aria-launches-as-an-ai-research-and-iteration-agent-with-autonomous-research-and-collaborative-intelligence)。
- [P16] 2026-07-01，City of Hammond, Indiana，[Expiration of Data Center Development Agreement](https://www.gohammond.com/hammond-announces-expiration-of-data-center-development-agreement/)。
- [P17] 2026-07-09，CoreWeave，[Named a Visionary in 2026 Gartner Magic Quadrant for Cloud AI Infrastructure](https://www.coreweave.com/news/coreweave-named-a-visionary-in-the-2026-gartner-magic-quadrant-tm-for-cloud-ai-infrastructure)；Gartner，[Magic Quadrant Methodology](https://www.gartner.com/en/research/magic-quadrant)。
- [P18] 2026-07-07—07-13，SEC Form 4，[Michael Intrator filing](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000318/0001769628-26-000318-index.html)；[Brannin McBee filing 1](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000320/0001769628-26-000320-index.html)；[filing 2](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000321/0001769628-26-000321-index.html)。
- [P19] 截至 2026-07-16 已官宣，CoreWeave，[Fully Connected 2026, September 29—October 1](https://www.coreweave.com/fully-connected-2026)。
- [P20] 截至 2026-07-16 05:50 PDT，CoreWeave，[Newsroom](https://coreweave.com/newsroom)；用于核验公司最新正式新闻仍为 2026-07-09 Gartner 事件。

### 独立行业与合作方交叉验证

- [X1] 2026-06-01，Dell Technologies，[First to Ship Systems Built on NVIDIA Vera Rubin Platform to CoreWeave](https://www.dell.com/en-us/blog/dell-first-to-ship-systems-built-on-nvidia-vera-rubin-platform-to-coreweave/)。
- [X2] 2026 年 NVIDIA 平台披露，NVIDIA，[NVIDIA Kicks Off the Next Generation of AI With Rubin](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Kicks-Off-the-Next-Generation-of-AI-With-Rubin--Six-New-Chips-One-Incredible-AI-Supercomputer/default.aspx)。
- [X3] 2026-06-16，MLCommons，[MLPerf Training v6.0 Results](https://mlcommons.org/2026/06/mlperf-training-v6-0-results/)；[Supplemental Discussion PDF](https://mlcommons.org/wp-content/uploads/2026/06/Final-MLPerf-Training-v6.0-Supplemental-Discussion-UNDER-EMBARGO-UNTIL-6_16_26-8_00-AM-PT.pdf)。
- [X4] 截至 2026-07-08，Compute Atlas，[CoreWeave Digital Crossroads—Hammond](https://www.compute-atlas.com/facilities/coreweave-digital-crossroads-hammond-in)；只作市政府文件的补充，不替代政府根来源。

### 主流媒体与卖方二级转述

- [M1] 2026-06-09，Bloomberg Law，[CoreWeave Founders Have Sold $2.3 Billion in Stock Since IPO](https://news.bloomberglaw.com/securities-law/coreweave-founders-have-dumped-2-3-billion-in-stock-since-ipo)。
- [M2] 2026-07-01，Reuters/Bloomberg 二级报道，[Meta to Sell Excess AI Computing Capacity via Cloud Business](https://www.investing.com/news/stock-market-news/meta-to-sell-excess-ai-computing-capacity-via-cloud-business-bloomberg-news-reports-4770550)。
- [M3] 2026-07-01，Axios，[Meta Reportedly Building a Cloud Business](https://www.axios.com/2026/07/01/meta-cloud-mark-zuckerberg)；SiliconANGLE，[Meta Shares Jump on Reported Plan to Offer AI Infrastructure Services](https://siliconangle.com/2026/07/01/meta-shares-jump-9-reported-plan-offer-ai-infrastructure-services/)。
- [M4] 2026-05-08，Kiplinger，[Stock Market Today: Q1 Results and CoreWeave Reaction](https://www.kiplinger.com/investing/stocks/s-and-p-500-nasdaq-close-week-at-new-highs-stock-market-today)。
- [S1] 2026-05 财报后卖方二级转述，Kiplinger，同上；只用于“容量售罄/执行为焦点”的叙事观察。
- [S2] 2026-07-02，Investing.com，[Rosenblatt Reiterates CoreWeave Buy Rating Amid Meta Cloud Reports](https://www.investing.com/news/analyst-ratings/rosenblatt-reiterates-coreweave-stock-buy-rating-amid-meta-cloud-reports-93CH-4772957)；未取得完整原始研报。

### 交易情绪数据

- [D1] 截至 2026-06-30 结算、2026-07-10 发布，Benzinga，[CRWV Short Interest](https://www.benzinga.com/quote/CRWV/short-interest)。
- [D2] 截至 2026-06-30，MarketBeat，[CRWV Short Interest History](https://www.marketbeat.com/stocks/NASDAQ/CRWV/short-interest/)；用于交叉验证股数并展示分母差异。
- [D3] 截至 2026-07-15 页面快照，Tradestie，[CRWV Options Statistics](https://tradestie.com/stocks/options/CRWV/)；第三方单时点数据，低于交易所原始数据优先级。

### 社区样本

- [C1] 2026-05-08，Reddit r/CRWV，BeSmartFiTness，[“Not sure what’s the upset about”](https://www.reddit.com/r/CRWV/comments/1t6wxn2/not_sure_whats_the_upset_about_it_was_good/)。
- [C2] 2026-07-01，Reddit r/CRWV，Lucid_Dreamer5，[“All Neoclouds are down on the latest Meta news”](https://www.reddit.com/r/CRWV/comments/1ukl4w5/all_neoclouds_are_down_on_the_latest_meta_news/)。
- [C3] 2026-07-04，Reddit r/ValueInvesting，orishasinc2，[“CoreWeave insiders are running to the exits”](https://www.reddit.com/r/ValueInvesting/comments/1un4srh/coreweave_inc_nasdaq_crwv_insiders_are_running_to/)。
- [C4] 2026-07-08，Reddit r/CRWV，Casztiel，[Gartner MQ Discussion](https://www.reddit.com/r/CRWV/comments/1ur9rlm/gartner_mq_for_cloud_ai_infra_just_dropped_crwv/)。
- [C5] 2026-07-10，Reddit r/CRWV，redditor7488283，[“2 Major Catalysts”](https://www.reddit.com/r/CRWV/comments/1ut36ho/2_major_catalysts/)。
- [C6] 2026-07-13，Reddit r/CRWV，redditor7488283，[“For the Bears”](https://www.reddit.com/r/CRWV/comments/1uvpvon/for_the_bears/)。

---

**复盘规则：** 本报告在 2026-07-16 05:50 PDT 冻结。截止时间后的消息不得回写本版本；复盘时保留原始判断，在跟踪表新增实际结果，或另建新日期版本。
