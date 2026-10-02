# 全球AI需求与Token经济框架研究方案

title:"全球AI需求与Token经济框架"

我要研究全球 AI 需求侧和 token 经济的真实增长框架。研究重点不是泛泛讨论 AI 应用前景，而是建立一套能把应用使用量、模型架构、token 价格、推理成本、训练需求、GPU/ASIC 利用率、云 AI 收入和 AI 基础设施 CapEx 连接起来的可复核模型。最终报告必须回答：AI 基础设施建设到底由哪些真实需求支撑，token 增长和 AI 收入能否覆盖 CapEx，训练和推理分别拉动哪些产业链环节，哪些需求只是叙事或提前投资。

本研究对 2026-2028 年 AI 需求保持乐观但可证伪的假设。对缺少直接披露的 token、GPU-hour、模型调用量和企业 AI 收入，可以做大胆估算，但必须写清楚估算链条、口径、来源日期、置信度和反证条件。所有美元规模必须用区间表达；token、FLOPs、GPU-hour、活跃用户、请求量、上下文长度和利用率作为物理校验指标。

方案版本：2026-07-10

## 一、资料边界与来源优先级

资料边界：

- 每次仅依据外部资料独立完成数据采集、模型、情景和结论，不使用本地研究成果、报告、索引、缓存和中间文件作为研究输入。需要分析时间变化时，从外部来源建立口径一致的分期数据。
- 允许读取本研究方法文件本身，并允许把最终 Markdown 写入指定输出目录。
- 可以联网搜索公开资料、公司材料、监管文件、会议资料、论文、技术文档和可信非正式线索；非正式信息必须标注来源类型、日期、置信度和验证状态。

外部资料优先级：

| 来源层级 | 优先来源 | 必须抽取的数字 | 使用方式 |
|---|---|---|---|
| 一手 AI 平台资料 | OpenAI、Anthropic、Google、Meta、Microsoft、Amazon、xAI、Mistral、Cohere、Perplexity 等 | API 定价、用户数、调用量、产品收入、模型路线、上下文长度、延迟指标 | 需求和价格主锚点 |
| 云厂财报与产品 | Azure、AWS、Google Cloud、Oracle Cloud、CoreWeave 等 | AI/云收入、CapEx、GPU/ASIC 实例价格、租赁合同、利用率线索 | 连接 AI 收入和基础设施投入 |
| 企业软件和应用 | Microsoft、Salesforce、ServiceNow、Adobe、Datadog、GitHub、Atlassian、Intuit、Shopify 等 | AI ARR、attach rate、seat price、使用频次、毛利率 | 校验企业 AI 付费和 token 需求 |
| 模型和技术资料 | 模型卡、技术报告、benchmark、论文、推理优化资料、系统论文 | 参数量、FLOPs/token、context、batching、KV cache、MoE、speculative decoding | 推导算力和存储需求 |
| 行业数据 | IDC、Gartner、Omdia、SemiAnalysis、Epoch AI、Stanford AI Index、a16z、Menlo、Synergy 等 | AI 软件支出、GenAI 市场、AI infra、云 AI 规模、企业采用率 | 区间边界和交叉验证 |
| 非正式线索 | 开发者社区、招聘、客户案例、渠道调研、价格追踪、实例可用性 | 使用强度、供需、排队、折扣、客户流失 | 降权使用，必须标注验证状态 |

## 二、研究目标

本研究必须完成十一件事：

1. 建立全球 AI 需求分层：训练、推理、agent、多模态、搜索、广告、代码、企业自动化、视频、机器人、科研和主权 AI。
2. 建立 token 经济模型：token 数量、价格、成本、毛利、延迟、利用率和单位 token 资本强度。
3. 将 token 需求转换为 GPU/ASIC 算力、内存、存储、网络、电力和数据中心 CapEx。
4. 判断 AI 收入能否支撑 AI CapEx，输出 2026、2027、2028 三情景的收入/CapEx/回收期框架。
5. 区分训练需求和推理需求：训练更拉动 GPU/HBM/scale-out network，推理更拉动利用率、内存、KV cache、存储、网络和电力效率。
6. 识别需求侧反证条件：AI 产品收入放缓、token 价格崩塌、利用率不足、企业 ROI 不达标、CapEx 下修、GPU 租赁价格下跌。
7. 给出投资映射：哪些环节受 token 增长直接驱动，哪些只是被 CapEx 前置拉动，哪些容易被价格下降抵消。
8. 建立近 30/90 日前线信号表，按日期、来源等级、需求/供给方向、影响变量和置信度判断最新变化是否足以调整情景。
9. 独立估算当前 tokens/day、tokens/year 和等价 AI workload run-rate；用外部可比期间数据解释使用量、价格、工作负载结构和模型效率的变化，区分真实增长与统计口径变化。
10. 判断当前供需状态及过去六个月的状态迁移，区分高端算力、通用/低价值算力、API token、Agent workload、HBM、存储和网络的供需差异。
11. 建立 Token 效率与 ROI 仪表板，跟踪 cost/task、cost/merged PR、Agent 成功率、人工接管率、cache hit、context reuse、tokens/GPU-hour、gross margin/token、GPU 价格和预算利用率。

## 三、核心定义和口径

| 口径 | 定义 | 单位 | 纳入 | 排除或单独列示 |
|---|---|---|---|---|
| token 需求 | 用户、应用、agent 和模型训练产生的输入/输出 token 总量 | tokens/day、tokens/year | API、聊天、代码、搜索、RAG、agent、多模态文本化 token | 纯下载量、未调用模型的用户数 |
| 训练需求 | 训练和后训练模型所需的算力需求 | FLOPs、GPU-hour、训练 run | pre-training、post-training、RL、synthetic data、distillation | 普通推理请求 |
| 推理需求 | 模型服务在线或批处理输出的算力需求 | tokens/sec、GPU-hour、QPS | API、consumer app、enterprise workflow、agent、batch inference | 训练计算 |
| token 价格 | 客户为输入/输出 token 或等价服务支付的价格 | $/M tokens、ARR/seat | API 价格、企业套餐、云实例收费 | 免费额度、内部转移价需单列 |
| token 成本 | 生成 token 的摊销成本 | $/M tokens | GPU/ASIC 折旧、电力、运维、网络、存储、软件 | 研发、销售费用需单列 |
| GPU/ASIC 利用率 | 可用算力被有效 token 或训练任务使用的比例 | % | batch utilization、memory utilization、network utilization | 名义装机率 |
| AI 收入 | AI 产品、API、实例、软件或服务的收入 | USD | 云 AI、AI SaaS、模型 API、GPU instance | 硬件销售和客户 CapEx 需分开 |
| CapEx 回收期 | 对应资产累计净现金流回收初始投入的时间 | 年 | GPU/ASIC、数据中心、网络、存储、电力、冷却，考虑爬坡、寿命、更新投入及残值 | 不以当年收入/CapEx 比例直接代替回收期 |
| 当前 run-rate | 以最新可验证使用量折算的年化 token 或等价 workload | tokens/day、tokens/year、GPU-hour/year | 当期 API、应用、Agent、企业工作流和批处理推理 | 未发生的长期预测、重复统计 |
| 供需状态 | 某类算力或 token 服务在当前时点的紧张、平衡或宽松程度 | 状态、价格、交付期、利用率 | 高端 GPU/ASIC、通用 GPU、API、HBM、存储、网络 | 只看名义装机而不看有效利用率 |
| Token 效率与 ROI | 单位业务结果所消耗的 token、算力和全部成本及其产出质量 | $/task、tokens/task、成功率、毛利率 | 推理成本、基础设施摊销、工具费用、人工复核 | 只看 token 单价而忽略任务结果 |

## 四、需求分层模型

最终报告必须把需求按场景分层，不允许只引用一个 GenAI 市场规模数字。

| 需求层 | 代表应用 | 关键变量 | 主要硬件压力 | 主要收入模式 |
|---|---|---|---|---|
| 消费聊天和搜索 | ChatGPT、Gemini、Perplexity、AI Search | MAU、queries/user、tokens/query、广告或订阅 | 推理 GPU、KV cache、网络、存储 | subscription、ads、API |
| 代码和开发者 | GitHub Copilot、Cursor、Windsurf、企业代码助手 | seats、completion/day、context length、repo indexing | 推理、长上下文、代码检索、存储 | seat、enterprise license |
| 企业办公和流程 | Copilot、Salesforce、ServiceNow、Adobe、Atlassian | attach rate、seat price、workflow frequency | 推理、RAG、agent、私有数据存储 | SaaS uplift、usage-based |
| 多模态和视频 | Sora、Veo、Runway、Adobe Firefly、生成式设计 | frames、resolution、duration、render latency | 高算力推理、存储、网络 | subscription、credits |
| Agent 和自动化 | browser agent、coding agent、enterprise agent | steps/task、tool calls、context retention、success rate | 长上下文、存储、网络、调度 | outcome-based、seat、usage |
| 训练和模型竞争 | frontier model、domain model、synthetic data | training FLOPs、run count、post-training | GPU/HBM、scale-out network、存储 | 战略投入、API 未来收入 |
| 主权 AI 和私有云 | 国家/企业私有模型和 AI 工厂 | project CapEx、data sovereignty、local demand | 全栈数据中心、电力、ASIC/GPU | project contract、cloud service |

## 五、核心推导公式

报告必须使用公式连接需求和基础设施，不允许只写趋势判断。

```text
场景输入 token = Σ[各类模型调用次数 × 每次输入 token]
场景输出 token = Σ[各类模型调用次数 × 每次输出 token]
同一统计口径的总 token = 输入 token + 输出 token
```

```text
推理 GPU/ASIC 数量（计算量校验）
= 年工作负载 FLOPs ÷ [单设备峰值 FLOPs/秒 × 年运行秒数 × 有效利用率]
或 = 年工作负载量 ÷ 同类工作负载的单设备年实测有效吞吐
```

```text
推理收入
= 按实际计费规则计算的 API 收入 + 不与其重复的订阅/seat/workflow 收入
API 收入需分别计算非缓存输入、缓存输入、输出及其他收费项；套餐内调用不再按标价追加收入
```

```text
推理毛利
= 推理收入 - GPU/ASIC 折旧 - 电力 - 网络/存储 - 运维 - 模型服务软件成本
```

```text
简化静态现金回收期（仅适用于现金贡献较稳定的情形）
= 对应资产初始投入 ÷ 不重复扣除折旧的年度可归因运营现金净流入
完整回收判断：按资产寿命、投产爬坡、利用率、更新再投资与残值分析累计净现金流
```

```text
训练需求
= 模型训练 run 数 × 每次训练 FLOPs × 后训练/实验倍数
```

```text
当前 run-rate 调整
= 当期硬披露锚点 + 可验证新增量 - 重复统计/口径排除项
```

```text
单位任务全成本
= 外购服务费用 + 自有基础设施的可归因成本 + 工具费用 + 人工复核成本
外购 API 费用中已包含的提供方硬件成本不得再加；混合部署分别核算，不重复分摊
```

公式说明：输入、输出、缓存命中/重算及推理计算分别计量，缓存 token 的计费量不等于重新计算量。不同 tokenizer、模型、模态与质量目标的 token 不直接相加比较；图像、音频、视频保留各自工作量单位，需要折算时说明基准和不确定性。调用次数已经包含 Agent 步数时，不再重复乘调用链长度。

使用实测有效吞吐时不再扣一次利用率；计算量模型还需以显存容量、带宽、KV cache、时延和网络约束校验。年度收入或现金对当年 CapEx 的覆盖只用于观察资金承受能力，不等同于资产回收期；毛利包含折旧时不能直接代替现金流。

公式输出以下结果，按数据可识别程度选择范围或条件：

- token 结果：tokens/day、tokens/year、输入/输出比例、长上下文占比。
- 物理结果：GPU/ASIC 数量、GPU-hour、rack、MW/GW、storage PB/EB、network bandwidth。
- 美元结果：AI 收入、推理成本、CapEx、订单池、回收期。
- 动态结果：当前 run-rate、近 30/90 日变化、过去六个月状态迁移、Token 效率与 ROI、可比期间的变化分解。

## 六、必须输出的表格

### 6.1 全球 AI 需求分层表

| 场景 | 2026 token 规模 | 2027 token 规模 | 2028 token 规模 | 收入模式 | 主要公司 | 最大不确定性 |
|---|---:|---:|---:|---|---|---|

### 6.2 Token 价格和成本表

| 模型/服务类型 | 输入价格 | 输出价格 | 成本区间 | 毛利率区间 | 降价速度 | 主要证据日期 |
|---|---:|---:|---:|---:|---:|---|
| Frontier API | `$X-Y/M tokens` | `$X-Y/M tokens` | `$X-Y/M tokens` | `X-Y%` | `X-Y%/year` |  |
| 企业 AI seat | `$X-Y/month` | token 等价 | token 等价 | `X-Y%` |  |  |

### 6.3 训练 vs 推理硬件需求表

| 需求类型 | 关键瓶颈 | GPU/ASIC 需求 | HBM/内存需求 | 网络需求 | 存储需求 | 电力需求 | 受益环节 |
|---|---|---:|---:|---:|---:|---:|---|

### 6.4 AI 收入支撑 CapEx 表

| 客户/平台类型 | 2026 AI 收入 | 2026 AI CapEx | 2027 AI 收入 | 2027 AI CapEx | 回收期 | 反证指标 |
|---|---:|---:|---:|---:|---:|---|
| Hyperscaler | `$X-YB` | `$X-YB` | `$X-YB` | `$X-YB` | `X-Y 年` |  |
| NeoCloud | `$X-YB` | `$X-YB` | `$X-YB` | `$X-YB` | `X-Y 年` |  |

### 6.5 需求到产业链映射表

| 需求变化 | 直接受益 | 间接受益 | 被压制环节 | 验证指标 | 反证指标 |
|---|---|---|---|---|---|
| 长上下文推理增长 | HBM、DRAM、KV cache、CXL、SSD | 网络、调度、存储软件 | 低内存推理卡 | context length、cache hit rate | 短上下文模型占比上升 |
| Agent 步数增长 | 推理 GPU/ASIC、调度、网络、存储 | DCIM、电力、监控 | 单次问答应用 | steps/task、tool calls | agent 留存和付费低 |

### 6.6 近 30/90 日前线信号表

| 日期 | 信号 | 来源等级 | 需求/供给 | 影响变量 | 对当前情景的调整 | 置信度 |
|---|---|---|---|---|---|---|

必须覆盖最新 API 定价与配额、模型/产品使用量、企业 AI 预算与采用、云厂/NeoCloud 实例价格和可用性、GPU/HBM/存储交付、CapEx 指引及重要效率优化。每项信号必须写清事件日期和资料发布日期。

### 6.7 当前 run-rate 与可比期间变化

| 指标与口径 | 外部来源可比期数据 | 当前独立估算 | 变化 | 来源与日期 | 对需求判断的影响 |
|---|---:|---:|---:|---|---|

仅用外部来源建立可比期间数据，说明统计范围差异。无法可靠比较时明确不可比，不读取项目上期报告补数。

### 6.8 当前供需状态矩阵

| 层级 | 当前状态 | 供需方向 | 价格方向 | 最大瓶颈 | 反证 |
|---|---|---|---|---|---|

至少覆盖高端 GPU/ASIC、通用 GPU、API token、coding agent、enterprise agent、consumer AI、HBM/KV cache/SSD，以及 Hyperscaler 与 NeoCloud 的差异。

### 6.9 过去六个月状态迁移表

| 阶段 | 需求端变化 | 供给端变化 | 计费/预算变化 | 供需结论 | 情景动作 |
|---|---|---|---|---|---|

### 6.10 Token 效率与 ROI 仪表板

| 指标 | 当前值/区间 | 外部来源可比期值 | 方向 | 解释 | 触发阈值 | 情景动作 |
|---|---:|---:|---|---|---|---|

至少覆盖 cost/task、cost/merged PR、Agent 成功率、人工接管率、cache hit、context reuse、tokens/GPU-hour、gross margin/token、GPU 租赁价格和 AI 预算利用率；无法取得的数据必须说明替代指标和置信度，不得留空后跳过。

## 七、三情景假设

| 变量 | 基准 | 乐观 | 极度乐观 | 反证数据 |
|---|---|---|---|---|
| token 增长 | 消费和企业稳定增长 | agent 和多模态明显放量 | agent 工作流成为主流生产力入口 | API/AI ARR 增速下滑、usage 停滞 |
| token 价格 | 每年快速降价但 volume 抵消 | 高价值场景维持价格 | outcome-based pricing 提升收入/token | API 价格战快于成本下降 |
| 推理成本 | GPU 折旧和电力下降有限 | ASIC、优化和 batching 降低成本 | 专用推理架构显著改善 TCO | 利用率不足、实例价格下跌 |
| AI 收入/CapEx | 回收期较长但可接受 | 云厂和企业付费支持扩建 | AI 收入和战略需求同步支撑加速 CapEx | CapEx guide 下修、NeoCloud 融资收紧 |
| 训练需求 | frontier model 持续迭代 | 合成数据和 post-training 放大 | 多公司/主权 AI 训练竞赛升级 | 训练 run 减少、模型 scaling 回报下降 |

## 八、投资视角输出要求

最终报告必须回答：

1. 2026-2028 年 AI 需求增长主要来自 token 数量、价格、用户数、agent 步数还是模型复杂度。
2. 训练和推理分别驱动哪些硬件、网络、存储、电力和半导体环节。
3. AI 收入是否足以解释当前和未来 CapEx，哪些客户群最可能提前投资。
4. 如果 token 价格继续下跌，哪些公司仍能受益，哪些环节会被压缩利润。
5. 如果 agent、多模态或企业 AI 不达预期，哪些产业链环节最先被证伪。
6. 哪些需求侧指标应该纳入日常跟踪。
7. 当前 token/等价 workload run-rate 是多少，外部可比数据支持哪些真实变化，哪些差异来自统计范围。
8. 最新 30/90 日信号是否改变未来三年情景，过去六个月供需状态如何迁移。
9. 高端算力与通用/低价值 token 是否处在不同供需阶段，价格和利用率分别说明什么。
10. Token 效率和单位任务 ROI 是否改善，哪些阈值会触发需求、收入或 CapEx 假设调整。

## 九、最终报告结构

正式报告必须严格按以下结构输出：

```markdown
# 全球AI需求与Token经济框架

报告日期：
主要数据日期：
估值/股价快照日期：
核心结论摘要：

## 一、结论先行：AI 需求是否足以支撑 2026-2028 基础设施扩张

## 二、研究口径、资料边界和估算方法

## 三、全球 AI 需求分层：训练、推理、agent、多模态和企业 AI

## 四、Token 经济模型：数量、价格、成本、毛利和降价路径

## 五、从 token 到 GPU/ASIC、存储、网络、电力和 CapEx

## 六、AI 收入与 CapEx 回收期：Hyperscaler、NeoCloud、企业和主权 AI

## 七、训练 vs 推理：不同 workload 对产业链的差异拉动

## 八、三情景预测：2026/2027/2028 token、收入、算力和 CapEx

## 九、产业链受益映射：直接受益、间接受益和伪受益

## 十、反证条件、风险和后续跟踪清单

## 十一、Reference 和数字来源附录
```

在上述十一章内必须嵌入四个动态更新模块：第三章纳入近 30/90 日信号和过去六个月状态迁移；第四章纳入当前 run-rate、可比期间变化及 Token 效率/ROI；第五章纳入分层供需状态矩阵；第十章把关键指标、阈值和情景动作整理成可持续更新的仪表板。不得另写一篇独立“前线跟踪”报告替代这些模块。

## 十、Reference 附录要求

Reference 不能只贴链接。每条来源必须说明它支持了哪个数字或判断。

| 来源 | 日期 | 来源层级 | 支持的数字/判断 | 是否一手 | 置信度 | 备注 |
|---|---|---|---|---|---|---|

报告至少覆盖以下 reference 类型：

1. AI 平台/API 的价格、用户、调用量或收入证据。
2. 云厂和 NeoCloud 的 AI 收入、CapEx、实例价格、租赁和利用率证据。
3. 企业软件 AI attach、seat price、ARR 和客户采用证据。
4. 模型技术资料对 FLOPs/token、context、KV cache 和推理优化的证据。
5. 行业第三方数据对 AI 软件、AI infra、云 AI 和企业采用率的交叉验证。
6. 最新 30/90 日 API 定价、预算、使用量、实例价格/可用性和基础设施交付信号。
7. Token/Agent 效率、单位任务成本、成功率、人工接管和企业 ROI 的证据。
8. 用于期间比较的外部原始披露及统计范围说明。

输出要求：

- 正式研究报告必须写成中文 Markdown，有一个大 title（`#`），适当二级标题（`##`）和三级标题（`###`）。
- 多用表格、公式、区间和反证指标，少写空泛叙事。
- 输出目录必须是 `D:\drive\Investment\基本面\行业调研\产业背景\`。
- 文件名建议为 `全球AI需求与Token经济框架_YYYY-MM-DD.md`。
