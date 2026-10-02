# AI数据中心建设规模与产业链订单映射（2026-2027，美国主导）

报告日期：2026-07-10  
方案版本：2026-06-04；本报告按 2026-07-10 可获得的公开资料更新  
主要数据日期：2024-12-20 至 2026-07-10；每个动态数字在正文或 Reference 中标注披露日期  
估值/股价快照日期：2026-07-10；本文不把盘中股价、单点目标价或未同步估值写入核心模型，股票排序依据订单可见度、瓶颈位置和利润池  
研究边界：美国境内 Hyperscaler、NeoCloud、AI Factory、AI colo 的新建、扩建和高密度改造；全球供应商订单按美国项目需求映射，不等同于供应商全球收入  

**核心结论摘要：**

- **总量**：基于 2026 年五家主要 hyperscaler 已披露的全球 CapEx 包络约 `$735-776B`，再扣除非 AI、海外及重复计算，并加入未包含在 hyperscaler 报表内的非重复 NeoCloud/colo 项目，本报告给出美国 AI 数据中心建设 CapEx：2026 年悲观 `$260-340B`、务实 `$350-450B`、乐观 `$470-620B`；2027 年分别为 `$300-400B`、`$440-570B`、`$680-900B`。务实情景对应 2026-2027 年中值增速约 `20-30%`，乐观情景约 `40%+`。
- **物理规模**：务实情景对应当年可转化的新增/扩建 AI IT load 约 2026 年 `9-13GW`、2027 年 `12-17GW`；这不是全部已经通电的存量，而是与当年设备采购、开工、机房交付和投产相关的建设转化量。按混合口径 `$27-36M/MW` 反推，美元规模与 MW 基本一致；高端区间依赖更高比例的 GPU/rack-scale 采购先于正式通电。
- **最大订单弹性**：compute、GPU/ASIC、HBM、机架系统和 AI fabric 的订单对 CapEx 上修最敏感；务实情景下 2026 年 compute 终端采购约 `$180-255B`，2027 年约 `$229-325B`。但 Rubin 等新平台的效率提升可能降低“每个 token 所需 GPU 数量”，因此计算量增长不等于 GPU 数量同比同幅增长。
- **最高确定性**：变压器/switchgear、UPS/PDU、液冷集成、EPC/MEP 和高压接入的确定性高于纯 GPU 云利用率。公开证据包括 Vertiv 2025 年末 `$15.0B` backlog、Eaton Electrical sector backlog 同比增长 `48%`、GE Vernova 2026 年一季度数据中心电气设备订单 `$2.4B`、Quanta 2026 年一季度总 backlog `$48.47B`、Comfort Systems USA 2026 年一季度 backlog `$12.45B`。
- **最大瓶颈**：2026 年排序为电力接入/变压器与 switchgear、HBM/先进封装、MEP 技能工人和液冷交付；2027 年若电力审批改善，瓶颈会更多转向 HBM4/HBM4E、CoWoS/基板/测试、1.6T/CPO 光互联和推理存储。FERC 于 2026-06-18 要求六大 RTO/ISO 改革大负荷并网规则，ERCOT 同期跟踪的 `438,000MW` 大负荷申请中约 `89%` 来自数据中心，但这类 queue 是意向量而非可交付订单。
- **订单拐点**：2026 年看 Blackwell/GB300 rack、800G 到 1.6T 过渡、液冷规模化以及电力设备 backlog；2027 年看 Rubin/定制 ASIC、HBM4E、微电网/自备电、AI Factory 收入确认和推理上下文存储。研究上优先把订单确认、交付、收入确认和租赁起租分开跟踪。

## 一、结论先行：总规模、最大瓶颈和最大订单弹性

### 1.1 美国 AI 数据中心建设总规模

| 年份 | 悲观 | 务实 | 乐观 |
|---|---:|---:|---:|
| 2026（美国） | `$260-340B` | `$350-450B` | `$470-620B` |
| 2027（美国） | `$300-400B` | `$440-570B` | `$680-900B` |

这里的“建设规模”是最终项目资本化口径，包含服务器/GPU/ASIC、网络、存储、电力、冷却、土建、MEP、调试和高密度改造；不把同一项目的租赁融资、hyperscaler CapEx、colo 开发商 CapEx 和供应商收入重复相加。上游 HBM、CoWoS、半导体设备属于嵌入或诱发的订单池，单独显示但不再加回总规模。

### 1.2 最大瓶颈和对应的研究优先级

| 优先级 | 环节 | 2026 判断 | 2027 判断 | 最直接验证指标 |
|---:|---|---|---|---|
| 1 | 电力接入、变压器、switchgear | 明显瓶颈；部分项目采用 behind-the-meter 发电或先租已有电力 | 局部缓解但大园区仍受高压接入和发电许可约束 | interconnection 队列转 ready-to-build 比例、lead time、utility 变电站投产 |
| 2 | HBM、CoWoS、基板和测试 | HBM3E/HBM4、封装 yield 和测试能力限制 GPU/rack 交付 | HBM4E、堆叠层数和大尺寸封装重新成为约束 | bit shipment、HBM ASP、HBM4E 量产、CoWoS capacity、tester utilization |
| 3 | MEP、液冷与调试工人 | 大型园区和 100kW 级 rack 的工程密度推高排期 | 预制化、标准化和模块化改善，但高端调试/服务仍稀缺 | backlog conversion、项目毛利、现场验收、液冷 attach rate |
| 4 | 融资和利用率 | NeoCloud 对债务、客户预付款和租赁依赖大 | AI Factory/colo 若利用率兑现，融资约束下降；若不兑现则反向放大 | RPO 中客户预付款占比、debt/EBITDA、GPU utilization、租赁起租 |
| 5 | AI 需求和推理经济性 | 训练需求强，推理收入和 token economics 仍是验证项 | agentic、多模态和长期上下文决定存储、电力效率及新增容量 | Azure/OCI/Bedrock 等供需、单位 token 成本、模型收入/利用率 |

### 1.3 投资结论的简化排序

| 维度 | 第一梯队 | 第二梯队 | 需要降权的情况 |
|---|---|---|---|
| 订单弹性 | NVDA、AVGO、AMD、MRVL、DELL、SMCI、ANET、COHR、LITE、MOD | MU、TSM、ASML、AMAT、VRT、TT、CARR | 只拥有 AI 标签但无可核验订单或 backlog 的公司 |
| 订单确定性 | ETN、VRT、GEV、PWR、FIX、EME、NVT、Schneider、Siemens | DLR、EQIX、CoreWeave、IREN | 高杠杆 GPU 云、未签约的 announced MW、远期土地 bank |
| 利润池 | GPU/ASIC、先进网络芯片、光器件、液冷系统、关键电气设备 | rack 集成、EPC/MEP、BMS/DCIM、存储 | 低毛利整机组装、未能转嫁 memory/铜钢涨价的承包商 |

## 二、研究口径、资料边界和估算方法

### 2.1 资料边界

本报告遵循本研究方案的独立性要求：不读取、不引用、不继承本地旧资料、旧报告、索引、缓存或中间结论；事实数字、技术路线、项目进度和公司订单均来自公开网络资料。模型中无法直接披露的数字标注为“模型估算”，并给出区间、公式、置信度和反证条件。

来源优先级为：公司 10-K/10-Q、earnings call、investor day 和订单公告；EIA/DOE/FERC/RTO/utility 文件；CBRE/JLL/Uptime/行业研究；供应商产品和订单材料；最后才使用新闻、会议或渠道线索。非正式线索不作为总量主锚点。

### 2.2 核心定义

| 口径 | 本报告定义 | 纳入 | 排除或单列 |
|---|---|---|---|
| AI 数据中心建设规模 | 美国境内为训练、推理、AI Factory、GPU/ASIC 集群和高密度 AI rack 服务的新建、扩建和改造 CapEx | Hyperscaler、NeoCloud、AI Factory、AI colo/build-to-suit 的最终项目投入 | 普通企业 on-prem、传统 IT refresh、非 AI colo、加密货币矿场 |
| CapEx | 项目业主或客户最终为物理 AI 基础设施支付或资本化的投入 | compute、network、storage、power、cooling、building/MEP、调试 | 云软件、人力运营、纯电费、模型训练服务费 |
| 订单池 | CapEx 落到设备商、EPC、系统集成商和上游芯片链的机会 | 已签合同、已获得订单、明确的 procurement、backlog 和可落地项目 | 仅 announced、无 site control、无电力/融资/客户承诺的远期规划 |
| 美国主导 | 项目物理位置和客户决策以美国为主 | 美国本土建设；美国客户对全球供应商的采购只按美国项目需求映射 | 中国市场、海外主权云和海外项目，除非作为对照或已明确映射美国供应链 |

### 2.3 总量公式和防重复规则

```text
US AI DC CapEx(year, scenario)
= Σ[hyperscaler global CapEx × AI/technical-infrastructure share
    × US build/decision share × year conversion]
  + non-duplicative NeoCloud / AI Factory / colo project CapEx
  - non-AI CapEx - overseas CapEx - lease/owner double count
```

三条防重复规则：

1. 同一园区的服务器、建筑、变压器、冷却和网络只在客户最终项目 CapEx 中计一次；REIT 或 colo 的融资方式不另行增加总量。
2. HBM/DRAM/先进封装是 GPU/ASIC/server BOM 的上游切片；半导体设备是为供给扩张诱发的供应商 CapEx，不是数据中心业主直接支付的项目 CapEx，因此在“嵌入/诱发订单层”显示，不能加回总量。
3. RPO、backlog、租赁合同、MW queue 和项目公告是不同层级的证据：RPO 不等于当年收入，backlog 不等于当年交付，MW queue 不等于可通电负荷。

### 2.4 公开 CapEx 包络：只作全球资金上限，不直接当作美国 AI 建设规模

| 公司 | 披露日期 | 公开数字 | 口径 | 本报告使用方式 |
|---|---|---:|---|---|
| Microsoft | 2026-04-29 | 2026 calendar CapEx 约 `$190B`，其中约 `$25B` 受组件价格影响 | 含 finance leases，全球、含非 AI | 作为最大客户资金上限；再乘 AI、美国和当年转化率 |
| Alphabet | 2026-02-04 | 2026 CapEx `$175-185B` | 全球；约 `60%` 为 servers，`40%` 为 data centers/networking；ML compute 略超过一半给 Cloud | 作为服务器与设施拆分锚点 |
| Amazon | 2026-02-05 | 2026 CapEx 约 `$200B` | 全 Amazon；AI、芯片、机器人、卫星等混合 | 只提取 AWS/AI/数据中心部分，不把全额算入 |
| Meta | 2026-04-29 | 2026 CapEx `$125-145B` | 含 finance lease principal payments；AI 与 core business 混合 | 作为 AI/数据中心高权重客户的区间锚点 |
| Oracle | 2026-06-10 | FY26 CapEx 约 `$55.7B`；FY26 融资 `$43B` debt + `$5B` equity | OCI AI 基础设施；部分大合同由客户预付或提供 GPU | 用于 NeoCloud/AI colo 融资和客户预付款校验 |
| **五家公司合计** | — | **约 `$735-776B`** | 全球、混合口径、不可直接相加为美国 AI CapEx | **总量模型的上限/资金包，不是最终预测** |

主要一手锚点： [Microsoft FY26 Q3 earnings call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3)、[Alphabet 2025 Q4 earnings call](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx)、[Amazon 2025 Q4 results](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx)、[Meta Q1 2026 results](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/)、[Oracle FY26 results](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Record-Q4-and-FY-2026-Results-Driven-by-Cloud-Infrastructure--Cloud-Applications/)。

## 三、美国 AI 数据中心建设总规模：2026/2027 三情景

### 3.1 三情景总表

| 年份 | 悲观 | 务实 | 乐观 | 年度 CapEx 变化解释 |
|---|---:|---:|---:|---|
| 2026（美国） | `$260-340B` | `$350-450B` | `$470-620B` | 2026 年公开 CapEx 资金包已被锁定，但美国项目转化受电力、HBM 和设备交付约束 |
| 2027（美国） | `$300-400B` | `$440-570B` | `$680-900B` | 2027 取决于 2026 年签约/开工项目能否转为机架交付、AI Factory 投产和推理需求兑现 |
| **中值增速** | `+10-20%` | `+20-30%` | `+35-55%` | 区间为模型中值对中值，不是单点预测 |

### 3.2 三情景驱动

| 驱动 | 悲观 | 务实 | 乐观 |
|---|---|---|---|
| GPU / ASIC 供给 | Blackwell/GB300 交付延迟；定制 ASIC 只覆盖少数客户；Rubin 主要是预购或试点 | Blackwell/GB300 在 2026 年持续放量，Rubin 在 2026 年下半年开始交付，Trainium/MTIA/定制 XPU 增加供给 | Rubin 与下一代 ASIC 大规模同步部署，rack-scale 交付成为标准模块，系统集成速度明显提升 |
| HBM / CoWoS / advanced packaging | HBM3E/HBM4 yield 与封装产能持续紧张，GPU allocation 不能转成完整 rack | 2026 逐季改善但价格仍高；2027 HBM4E 和大尺寸封装扩张 | HBM4/HBM4E 量产顺利、封装良率超预期，内存不再是硬上限 |
| 电力瓶颈 | interconnection、变压器、switchgear 和发电许可延误 12-24 个月；queue 大量撤回/缩减 | 大型项目采用分期通电、自备电、PPA、旧电厂再利用和局部并网 | FERC/RTO 改革与 behind-the-meter 方案快速转化；1GW 级园区批量开工 |
| 融资 | NeoCloud 融资成本高、客户预付款减少、GPU 云利用率不足 | hyperscaler、优质 AI lab 和投资级 colo 仍可融资，项目融资选择性增强 | 长期租赁、客户预付款、债务和 equity platform 联合放大，AI Factory 进入抢 capacity 阶段 |
| AI 需求兑现 | 模型效率提升快于使用量，推理收入/利用率低；CapEx guide 下修 | 训练与推理双增长，agentic workload 带来持续使用，但利用率仍有爬坡 | 多模态、agent、企业 adoption 和模型竞争推动 token 需求超预期，空置 capacity 被迅速吸收 |
| CapEx 增速假设 | `10-15%` | `20-30%` | `40%+` |

### 3.3 可证伪性

务实情景必须同时满足三项：

- 五大 hyperscaler 2026-2027 CapEx 指引没有出现连续两个季度的合计下修，且 Azure/Cloud 供需仍显示“需求超过可用容量”或同等表述。
- 新增建设的有效电力不是只停留在 announced MW；至少 `20-35%` 的大项目取得 site control、客户合同、融资和 utility study/energization 节点。
- HBM、封装、GPU、光互联和液冷厂商的 backlog/交期向收入转化，而不是只有 bookings 或供应商 capacity reservation。

如果上述任意两项失效，2026 年总量应向 `$260-340B` 靠拢；若同时出现 CapEx guide 下修、queue 撤回和 GPU/HBM 订单取消，应采用悲观区间。

## 四、从 CapEx 到物理规模：MW、rack、GPU、建设周期交叉验证

### 4.1 新增 AI IT load

| 年份 | 悲观 | 务实 | 乐观 | 口径 |
|---|---:|---:|---:|---|
| 2026 | `6-9GW` | `9-13GW` | `13-18GW` | 当年采购、开工、交付和部分投产对应的新增/扩建 IT load |
| 2027 | `7-11GW` | `12-17GW` | `18-25GW` | 2026 年开工项目进入机架安装和投产，新增 AI Factory/推理容量叠加 |

交叉验证：DOE/LBNL 在 2024-12-20 的美国数据中心能源报告估计，数据中心用电从 2023 年 `176TWh` 增长至 2028 年 `325-580TWh`，占美国用电比重从 `4.4%` 上升至 `6.7-12%`。CBRE 在 2026-02-26 披露北美八个主要市场 2025 年总存量 `9,432MW`、年吸收 `2,497.6MW`、在建 `5,994.4MW`；AI 项目还在向 500MW 以上园区迁移，因此本报告的乐观区间不是“全 queue 转化”，而是假设一部分已获电力和融资的超大园区在两年内提前采购设备。

### 4.2 单 MW CapEx

| 建设类型 | 模型区间 | 估算公式/锚点 | 置信度 |
|---|---:|---|---|
| facility-heavy、AI-ready 但低密度 | `$12-20M/MW` | 土建/MEP/电力/冷却较高，服务器分期安装；适用于提前建 shell、等待 GPU 的园区 | 中 |
| compute-heavy、液冷 rack | `$30-50M/MW` | GPU/ASIC、HBM、rack、网络和液冷占比高；高端 rack 先采购 | 中 |
| 务实混合口径 | `$27-36M/MW` | 由 Microsoft/Azure AI 生命周期研究的 `$7.0/W` power、`$2.5/W` cooling、`$375k/server` 和 10MW/500 H100 示例校准，再下调为混合项目 | 中 |
| 设施容量到 IT load 折算 | `1.25-1.40x` | 2026 年 NVIDIA/Siemens 参考架构为 `136MW` total facility、`100MW` IT load；高效 hyperscale 取低端，备用和自备电取高端 | 中 |

上述不是行业统一报价。Microsoft/U.T. Austin 2026 年 AI 数据中心生命周期论文给出的示例中，10MW AI 数据中心在 `75%` 利用率下约含 `500` 台 H100 服务器、年耗电约 `70GWh`，并将 CapEx 拆为 IT、network、building、power 和 cooling；本报告用其作为结构性锚点，而不是把论文的单个示例直接外推到全美国。

### 4.3 rack density 与 GPU/ASIC 数量

| workload / 平台 | 典型 rack density | 主要依据 | 订单含义 |
|---|---:|---|---|
| 传统云/CPU | `12-25kW/rack` | 传统服务器和部分推理节点 | 对普通 HVAC、UPS、存储和机房改造拉动更大 |
| AI inference | `30-80kW/rack` | 低延迟、较多内存/缓存、部分液冷 | 2027 年推理存储、网络和能效控制更敏感 |
| GB200/NVL72 | 约 `120kW/rack` | NVIDIA DGX/ OCP 设计 | 直接驱动液冷、power shelf、busbar、CDU |
| GB300/NVL72 | 最高约 `142kW/rack` | NVIDIA Enterprise Reference Architecture，8 个 `33kW` power shelf | 2026-2027 高密度 rack 的电力/热管理上限 |
| Rubin NVL72 | 目标为同一 rack-scale 形态，实际功率随配置变化 | NVIDIA 2026-01-05 发布，产品 2026 年下半年由伙伴供货 | 2027 网络、HBM、液冷和机架集成延续升级 |

| 年份 | 情景 | AI rack-scale 机架数 | GPU/ASIC 等效数量 | 计算方法 |
|---|---|---:|---:|---|
| 2026 | 悲观 | `15,000-30,000` | `1.2-2.2M` | 低转化率，混合 8-GPU server 与少量 72-GPU rack |
| 2026 | 务实 | `25,000-50,000` | `2.0-3.8M` | Blackwell/GB300 放量，部分推理集群为低密度配置 |
| 2026 | 乐观 | `40,000-70,000` | `3.0-5.0M` | 供给、融资、电力同步改善，rack-scale 交付先于正式满载 |
| 2027 | 悲观 | `20,000-40,000` | `1.5-2.8M` | GPU 数量被效率提升和项目延迟压低 |
| 2027 | 务实 | `35,000-70,000` | `2.8-5.0M` | Rubin/ASIC、HBM4 和推理扩容共同拉动 |
| 2027 | 乐观 | `60,000-100,000` | `4.5-7.0M` | 多个 AI Factory 进入批量部署，推理和 agentic workload 扩大 |

GPU/ASIC 等效数量是模型估算，不代表所有芯片都是 NVIDIA GPU，也不代表所有 rack 都是 NVL72。以 72-GPU rack 直接换算会得到较低 rack 数；本表刻意加入 8-GPU/多节点服务器、定制 ASIC 和 inference rack，以避免把所有建设假设成一种 SKU。

### 4.4 建设、采购和收入确认周期

| 环节 | 常见时间 | 2026 影响 | 2027 影响 |
|---|---:|---|---|
| site control、utility study、PPA/自备电 | `6-24+个月` | 电力已锁定的项目先获得估值和设备订单溢价 | 2026 年申请的项目进入是否真正开工的检验期 |
| 变压器/switchgear/发电机 | `12-36个月` | 设备订单可能先于园区收入确认 | 交付成为限制通电而非订单不足的主要变量 |
| 土建和 MEP | `12-36个月` | 500MW 以上 campus 需要分期 | 2026 年 backlog conversion 决定 2027 收入峰值 |
| GPU/HBM/封装/rack | `3-12个月`，新平台有更长爬坡 | Blackwell/GB300 和液冷 rack 是主要确认节点 | Rubin/HBM4E/ASIC 和 CPO 进入批量 |
| commissioning、验收、租赁起租 | `3-9个月` | 设备收入可能已经确认，colo 租金尚未开始 | 订单、收入、现金流之间的时间差暴露 |

CBRE 2026 outlook 指出，传统小于 50MW 建筑的 12-18 个月周期已不适用于 500MW 以上 AI campus；涉及新高压输电或增量发电时，interconnection 可能延长至 `24-48+个月`。因此 2026/2027 研究不能把“公告日期”当作“当年收入”。

### 4.5 美元与 MW 的一致性检查

以务实 2026 为例：`$350-450B ÷ $27-36M/MW` 对应约 `9.7-16.7GW` 的建设转化负荷；与 `9-13GW` IT load 的差异主要来自 facility-heavy 与 compute-heavy 项目混合、设施容量/IT load 换算、服务器采购提前和未满载投产。若将 `$450B` 全部除以 `$12-20M/MW`，会得到不现实的 `22.5-37.5GW`；这说明乐观美元区间必须同步满足高密度计算、GPU 供给和电力交付，不能仅靠提高项目公告数量来支撑。

## 五、CapEx 结构拆解：悲观/务实/乐观三情景

### 5.1 读表规则

下表前七行是最终项目 CapEx 的 mutually exclusive allocation，合计的中心值按 `100%` 归一化；各区间上下限独立取值，不能机械相加。`compute` 已包含 GPU/ASIC、CPU、HBM、主板、server、rack-scale system 和系统集成；“HBM/DRAM/SRAM”是 compute 内的供应链 content slice，“先进封装/半导体设备”是更上游的诱发订单，均为**非加总行**。

### 5.2 悲观情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU / 服务器 / compute | `$130-185B` | `50-55%` | `$150-220B` | `50-55%` | GPU/HBM/融资限制压低 rack 交付，服务器先做部分替换 |
| 网络 / 光互联 / 铜互联 | `$16-27B` | `6-8%` | `$18-32B` | `6-8%` | 800G attach 放缓，1.6T/CPO 主要处于验证期 |
| 电力 / UPS / BESS / 配电 | `$26-41B` | `10-12%` | `$30-48B` | `10-12%` | 长交期设备仍有订单，但项目开工受电力约束 |
| 建筑 / 土建 / MEP | `$34-54B` | `13-16%` | `$39-64B` | `13-16%` | facility 先于 compute 建设，部分 shell 等待通电 |
| 冷却 / 液冷 / HVAC | `$16-27B` | `6-8%` | `$18-32B` | `6-8%` | 液冷渗透低于预期，混合 air/liquid 方案为主 |
| SSD / HDD / 存储系统 | `$8-17B` | `3-5%` | `$9-20B` | `3-5%` | 推理和长上下文需求延后，HDD 仍维持成本优势 |
| 其他控制、安全、消防、服务 | `$5-14B` | `2-4%` | `$6-16B` | `2-4%` | DCIM/BMS、安防和维护随项目滞后 |
| HBM / DRAM / SRAM（compute 内嵌） | `$13-27B` | `5-8%` 内嵌切片 | `$15-32B` | `5-8%` 内嵌切片 | HBM3E/HBM4 yield 紧张，HBM 价值量上升但数量受限；**不加回** |
| 先进封装 / 基板 / 半导体设备（上游诱发） | `$6-12B` | `2-4%` 上游切片 | `$8-16B` | `2-4%` 上游切片 | CoWoS/测试/设备扩产慢；**不加回** |

### 5.3 务实情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU / 服务器 / compute | `$180-255B` | `52-57%` | `$229-325B` | `52-57%` | Blackwell/GB300 放量，Rubin 在 2026 年下半年建立初始交付 |
| 网络 / 光互联 / 铜互联 | `$25-41B` | `7-9%` | `$31-51B` | `7-9%` | 800G 成为主流，1.6T 在 2027 年开始提高 attach |
| 电力 / UPS / BESS / 配电 | `$32-50B` | `9-11%` | `$40-63B` | `9-11%` | 局部变压器/switchgear 瓶颈，behind-the-meter 补足并网 |
| 建筑 / 土建 / MEP | `$42-68B` | `12-15%` | `$53-86B` | `12-15%` | 在建项目持续交付，预制化和模块化缩短部分周期 |
| 冷却 / 液冷 / HVAC | `$25-41B` | `7-9%` | `$31-51B` | `7-9%` | 100kW 级 rack 推动 CDU/冷板、chiller 和热排放系统 |
| SSD / HDD / 存储系统 | `$14-23B` | `4-5%` | `$18-29B` | `4-5%` | 训练、推理、RAG、checkpoint 和 context cache 共同拉动 |
| 其他控制、安全、消防、服务 | `$7-14B` | `2-3%` | `$9-17B` | `2-3%` | DCIM/BMS、数字孪生、物理安全和 commissioning attach 提升 |
| HBM / DRAM / SRAM（compute 内嵌） | `$25-45B` | `7-10%` 内嵌切片 | `$31-57B` | `7-10%` 内嵌切片 | HBM4 量产改善，HBM4E 在 2027 年开始贡献；**不加回** |
| 先进封装 / 基板 / 半导体设备（上游诱发） | `$10-20B` | `3-5%` 上游切片 | `$15-30B` | `3-5%` 上游切片 | CoWoS、substrate、test 和 WFE 以 2-6 个季度滞后；**不加回** |

### 5.4 乐观情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU / 服务器 / compute | `$259-372B` | `55-60%` | `$374-540B` | `55-60%` | GPU/ASIC 供给、系统集成和客户预付款共同加速 |
| 网络 / 光互联 / 铜互联 | `$38-62B` | `8-10%` | `$54-90B` | `8-10%` | 1.6T、NPO/CPO、高速 DAC/AEC 快速渗透 |
| 电力 / UPS / BESS / 配电 | `$47-81B` | `10-13%` | `$68-117B` | `10-13%` | 自备电、微电网、BESS、HVDC/800VDC 与新园区并行 |
| 建筑 / 土建 / MEP | `$47-81B` | `10-13%` | `$68-117B` | `10-13%` | 多个 500MW+ 园区批量开工，预制化提升转化率 |
| 冷却 / 液冷 / HVAC | `$38-62B` | `8-10%` | `$54-90B` | `8-10%` | 液冷成为高密度 rack 标配，热回收/水处理增加 |
| SSD / HDD / 存储系统 | `$19-37B` | `4-6%` | `$27-54B` | `4-6%` | 推理上下文、长序列、多模态和 agent 日志推动存储爆发 |
| 其他控制、安全、消防、服务 | `$9-19B` | `2-3%` | `$14-27B` | `2-3%` | AI Factory 运维复杂度和软件/服务 attach 提升 |
| HBM / DRAM / SRAM（compute 内嵌） | `$38-74B` | `8-12%` 内嵌切片 | `$54-108B` | `8-12%` 内嵌切片 | HBM4/HBM4E 堆叠层数、容量和 ASP 同时上行；**不加回** |
| 先进封装 / 基板 / 半导体设备（上游诱发） | `$16-30B` | `3-5%` 上游切片 | `$24-45B` | `3-5%` 上游切片 | 先进封装、测试、设备和材料扩产形成滞后放大；**不加回** |

### 5.5 结构性判断

- 2026 年 compute 的美元占比仍高，但“新增订单弹性”不只来自 GPU 数量，还来自 rack-scale 集成、HBM 容量、系统内互联、液冷和机柜级 power shelf。
- 2027 年 facility 占比不一定上升：若 Rubin/ASIC 每 token 能耗下降，单位 IT load 产出提升，CapEx 可能更多流向高价值 compute、网络、存储和电力质量，而不是单纯扩大建筑面积。
- HBM/CoWoS 不能作为第十个独立终端 CapEx 模块；把上游内容加回会把同一块 GPU/服务器支出重复计算两次。

## 六、产业链订单映射

以下订单规模以**务实情景、美国项目需求映射**为主。子行存在“模块内嵌/层级嵌套”时会明确标注；例如 rack-scale integration 是 AI server 的价值捕获切片，不能和 AI server 顶层订单再相加。

### 6.1 电力与能源

#### 6.1.1 订单池

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | 主要公司 | 瓶颈 | 订单确认/验证指标 |
|---|---:|---:|---:|---|---|---|
| 变压器 / switchgear / 保护设备 | `$32-48B` | `$42-66B` | `20-40%` | Eaton、GE Vernova、Schneider、Siemens、Powell、Hubbell | 变压器、铜钢材料、认证和 utility 交付 slot | backlog、book-to-bill、lead time、substation 投产 |
| UPS / dynamic UPS / BESS | `$18-30B` | `$25-42B` | `20-45%` | Vertiv、Eaton、Schneider、Fluence、Tesla Energy | 功率模块、电池、BMS、并网和消防认证 | 数据中心订单、BESS MW/MWh、交付节奏、毛利 |
| busway / PDU / power shelf / busbar | `$10-17B` | `$14-24B` | `25-45%` | Vertiv、Eaton、Schneider、nVent、Legrand、Delta | 铜、连接器、客户认证、机架级 power topology | 每 MW electrical BOM、rack density、项目招标 |
| 微电网 / 天然气 / fuel cell / 临时电源 | `$12-25B` | `$20-40B` | `30-60%` | GE Vernova、Bloom、Caterpillar、Fluence、Wärtsilä、utilities/IPP | 燃机 slot、燃气管线、排放许可、PPA、并网 | PPA、发电设备订单、州审批、behind-the-meter MW |
| **电力与能源顶层订单池** | **`$72-110B`** | **`$95-150B`** | **`20-40%`** | — | — | 四项合计用于判断方向；设备、发电和园区之间仍有部分嵌套 |

#### 6.1.2 证据和判断

DOE/LBNL 的 `325-580TWh` 2028 用电区间证明电力是结构性约束，但不直接证明所有 announced load 都会建设。FERC 2026-06-18 对 PJM、MISO、SPP、CAISO、ISO-NE 和 NYISO 发出大负荷规则改革指令，重点包括 cost allocation、co-location、behind-the-meter generation 和 flexible transmission service；这会提高真实项目的转化率，但仍需要州审批和资本开工。

ERCOT 2026-06-18 公布的 `438,000MW` 大负荷请求、约 `89%` 数据中心占比是 queue 上限而非订单。2026-02 的 ERCOT 公共材料显示，约 `9,850MW` 已获批准 energize 或已运行，数据中心实际增长约 `15.5%`；因此模型只把 queue 的一小部分作为 2026-2027 可转化上限。

**投资含义**：电力设备的 Alpha 来自长交期、认证和客户先付定金，不一定来自 AI 需求的最终利用率；发电/燃料电池的 Beta 更高，但需要识别设备订单是否真正服务数据中心，避免把工业和电网的其他需求误算成 AI。

### 6.2 AI 服务器与机架

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | 主要公司 | 毛利/价值捕获 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| AI GPU/ASIC 服务器和加速系统 | `$180-260B` | `$230-340B` | `20-40%` | NVIDIA、AMD、Broadcom、Marvell、Dell、HPE、Supermicro、Quanta、Wiwynn | GPU/ASIC 设计和系统控制权高；OEM/ODM 毛利较低 | GPU/ASIC allocation、出货、客户订单、AI server revenue |
| rack-scale system / NVL72 / Helios / AI Factory pod | `$35-65B` | `$55-95B` | `30-70%` | NVIDIA、Dell、HPE、Supermicro、Wiwynn、Quanta、AMD | 液冷、网络、验收和软件集成提高价值捕获；**为上行切片** | rack 出货、系统验收、每 rack kW、交付周期 |
| 机柜级电源、液冷集成和 commissioning | `$8-15B` | `$12-22B` | `30-60%` | Vertiv、Eaton、nVent、Schneider、CoolIT、Delta | 关键路径和 field service 比标准 server 更有定价权；**为上行切片** | power shelf、CDU、现场验收、返工率、服务 attach |

Dell 2026-05-28 的 FY27 Q1 earnings call 是服务器订单的强验证：单季 AI orders `$24.4B`、AI server revenue `$16.1B`、期末 AI backlog `$51.3B`，且公司称 memory 是主要约束。Supermicro 2026-06-09 宣布拟融资 `$7B` 用于采购已收到的 AI server 订单，说明需求不只存在于大 hyperscaler，也存在于需要营运资金的系统集成商。AMD 2026-02-24 与 Meta 公布最高 `6GW` 的多代 Instinct/EPYC/Helios 部署，首个 `1GW` 预计 2026 年下半年开始出货；NVIDIA 2026-01-05 则表示 Rubin 伙伴产品将在 2026 年下半年供应。

### 6.3 网络、光互联与铜互联

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | attach 假设 | 主要公司 | 验证指标 |
|---|---:|---:|---:|---:|---|---|
| 800G / 1.6T optical modules、laser、DSP | `$12-22B` | `$20-36B` | `35-70%` | 每个 AI rack/cluster 多层 scale-out；1.6T 2027 attach 提高 | Coherent、Lumentum、Corning、Marvell、Cisco、Fabrinet、AAOI、Innolight | 出货量、ASP、客户认证、InP/EML capacity、订单 backlog |
| AI fabric switch / InfiniBand / Ethernet | `$16-28B` | `$23-40B` | `25-45%` | 每 GPU 的 scale-up/scale-out port 数随 cluster 拓扑上升 | NVIDIA、Arista、Broadcom、Marvell、Cisco | switch silicon、port shipments、AI network bookings、客户 topology |
| DAC / AEC / backplane / connector | `$8-15B` | `$12-22B` | `30-55%` | rack 内短距铜互联和高电流/高速连接随密度上升 | Amphenol、TE Connectivity、Belden、Molex、Corning、nVent | NVL rack BOM、线缆认证、每 rack 线缆数、退货/field failure |
| **网络顶层订单池** | **`$25-41B`** | **`$31-51B`** | **`25-50%`** | — | — | 光模块、交换机、铜互联存在供应商层级嵌套 |

Arista 2026-05-05 披露 Q1 revenue `$2.709B`、同比增长 `35.1%`，并在 2026-06-09 发布 1.6T AI fabric 产品，液冷版本计划 2027 年一季度可用；Lumentum 2026 年初披露 OCS backlog 已超过 `$400M`，另有可在 2027 年上半年交付的数亿美元级 CPO 订单；Coherent 2026-03-02 与 NVIDIA 签署多年度协议，包含 NVIDIA 的 multibillion-dollar purchase commitment 及 `$2B` 投资。它们支持“网络订单高弹性”，但不能把供应商的全球订单全部归因于美国项目。

### 6.4 半导体上游拉动

#### 6.4.1 上游订单池（嵌入式，不加回终端 CapEx）

| 子环节 | 2026 订单规模 | 2027 订单规模 | 订单确认节奏 | 主要公司 | 主要瓶颈 | 验证指标 |
|---|---:|---:|---|---|---|---|
| GPU / custom ASIC / XPU | `$160-235B` | `$220-330B` | allocation、预付款、系统交付；供应商收入先于园区满载 | NVIDIA、AMD、Broadcom、Marvell、Google TPU、AWS Trainium、Meta MTIA | die、HBM、CoWoS、基板、测试、软件生态 | Data Center revenue、custom XPU bookings、客户承诺、交付 |
| HBM / DRAM / SRAM / CPU memory | `$28-50B` | `$40-75B` | bit shipment、ASP、长期协议；HBM 先于普通 DRAM | Micron、SK hynix、Samsung、Rambus、Everspin/相关 IP | HBM stack、yield、logic base die、封装和电力 | HBM4/HBM4E 量产、bit growth、ASP、库存 |
| CoWoS / advanced packaging / substrate | `$12-22B` | `$18-35B` | 产能扩张和 tool delivery 领先 2-6 个季度 | TSMC、ASE、Amkor、日月光生态、基板供应商 | CoWoS capacity、interposer、ABF substrate、bonding | monthly capacity、tool acceptance、yield、lead time |
| 半导体设备 / test / metrology | `$8-16B` | `$12-24B` | 通常滞后 GPU/数据中心采购 2-6 个季度 | ASML、Applied Materials、Lam Research、KLA、Advantest、Teradyne | 设备交付、客户 CapEx、测试吞吐、技术转移 | WFE、backlog、tester utilization、HBM wafer starts |

Micron 2026-06-24 材料称 HBM4 已为主要客户平台高量出货，HBM4E 计划 2027 年量产；Micron 2026-03-16 已公布为 NVIDIA Vera Rubin 量产 HBM4、PCIe Gen6 SSD 和 SOCAMM2。Samsung 2026-02-12 宣布 HBM4 mass production，TSMC 2026 年北美技术论坛披露正在生产 `5.5-reticle` CoWoS，并规划更大尺寸版本。Applied Materials 2026-05-21 预计 2026 年半导体设备业务增长超过 `30%`，并将 HBM 和先进封装视为最快增长区域；Advantest 2026-05 披露截至 2026-03-31 财年销售额同比增长 `44.7%`，主要受 AI/HPC 和高性能 DRAM 测试需求驱动。

**关键限制**：GPU/ASIC 行与 HBM/CoWoS 行都是 compute 的上游视图，不是另外一块终端 CapEx。若把 `$160-235B` GPU/ASIC、`$28-50B` HBM 和 `$12-22B` CoWoS 全部叠加到 `$180-260B` AI server 订单上，必然重复计算。

### 6.5 建筑、工程、REIT 与开发商

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | 主要公司/平台 | 价值捕获 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| EPC / MEP / 土建 / 高低压安装 | `$50-75B` | `$65-100B` | `20-40%` | Quanta、Comfort Systems、EMCOR、MYR Group、Sterling、Jacobs、AECOM、Turner/DPR/Mortenson | backlog 转收入、专业技能和关键路径管理；人工/材料涨价可压毛利 | RPO/backlog、bookings、margin、项目延期、完工 MW |
| 预制化机房 / power-cooling pod / 模块化 | `$15-28B` | `$22-42B` | `30-60%` | Vertiv、Schneider、nVent、Eaton、Dell、Supermicro、模块化厂商 | 工厂化交付缩短时间并提高标准化溢价 | factory capacity、每月 MW delivery、模块验收 |
| REIT / colo / build-to-suit / powered land | `$40-70B` | `$55-95B` | `20-45%` | Digital Realty、Equinix、Iron Mountain、CoreWeave、IREN、Cipher、Applied Digital、QTS/Blackstone | 预租、power bank、租金和资本成本；不是设备毛利 | leased MW、pre-lease、development pipeline、起租、融资 |

证据层：Digital Realty 2026-06 investor presentation 显示约 `3GW` in-place IT capacity、约 `6GW` future development IT capacity、约 `1.2GW` under construction，并标注超过 `6GW` development capacity for cloud/AI；Equinix 2026 outlook 披露 2025 年交付 `90+MW` xScale、约 `1GW` powered land-under-control，并预计 2026 总 CapEx `$3.655-4.155B`。CoreWeave 2026-05-07 披露 backlog `$99.4B`、active power 超过 `1GW`、contracted power 超过 `3.5GW`；IREN 2025-11-03 公布与 Microsoft `$9.7B` 协议，覆盖 Childress 750MW campus 中 `200MW` critical IT load、20% prepayment。

这些证据证明“项目/租赁/融资”真实存在，但不能把 backlog 当成美国当年建设收入。对于 CoreWeave/IREN 等 NeoCloud，应额外检查 GPU 资产负债表、客户集中度、利息、利用率和电力交付。

### 6.6 冷却、存储、DCIM 和其他必要环节

| 环节 | 2026 订单规模 | 2027 订单规模 | CAGR | 主要公司/环节 | 为什么重要 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| 液冷 / CDU / 冷板 / 泵阀 / manifold | `$12-22B` | `$22-38B` | `45-80%` | Vertiv、Modine、Trane、Carrier、nVent、Schneider、Eaton/Boyd、CoolIT、ZutaCore | 100-142kW rack 直接需要；由选配向标准化过渡 | liquid attach、每 rack kW、CDU/冷板订单、现场故障 |
| Chiller / HVAC / heat rejection | `$10-18B` | `$14-26B` | `25-55%` | Carrier、Trane、Johnson Controls、Modine、Vertiv | 纯液冷也需要设施侧热排放，传统 HVAC 不会消失 | chiller MW、交付周期、PUE/WUE、服务收入 |
| 冷却液 / 水处理 / 过滤 / 热回收 | `$2-5B` | `$3-8B` | `25-70%` | Xylem、Ecolab、Pentair、Dow、specialty fluid vendors | 液冷规模化后的耗材、认证和运维 | coolant attach、water treatment、field service、泄漏率 |
| SSD / HDD / storage server / context cache | `$16-28B` | `$23-40B` | `25-55%` | Micron、Western Digital、Seagate、Samsung、Kioxia、Pure Storage、Dell | 推理、RAG、多模态、checkpoint 和日志使存储成为第二增长曲线 | NAND/HDD ASP、EB shipment、SSD/HDD mix、storage rack |
| DCIM / BMS / energy control / security | `$8-14B` | `$11-20B` | `25-60%` | Schneider、Vertiv、Johnson Controls、Honeywell、Siemens | 高密度 AI Factory 的能耗、故障和调度复杂度更高 | software attach、digital twin、energy savings、service ARR |
| 消防 / 物理安防 / 线缆管理 | `$3-6B` | `$4-8B` | `20-50%` | EMCOR、Johnson Controls、Honeywell、Hubbell、nVent、Atkore、Amphenol | 不是高 Beta，但每个项目的合规必需项 | 每 MW 造价、项目验收、消防/安全认证 |

Modine 2026-05-26 与战略数据中心客户签署 2027-2029 年超过 `$4B` 的 Airedale cooling capacity agreement，并收到 `$165M` upfront cash；Vertiv 2026-03-30 宣布美国液冷/冷冻水产能扩张，预计 2027 年二季度投产、相关系统产能提升约 `45%`；Carrier 2026-04-29 扩大对 ZutaCore 的投资并明确把 thermal management 视为 AI scale 的约束。Micron 2026-05-05 出货 245TB SSD，并称同等 raw capacity 所需 rack 数比 HDD 减少 `82%`；这说明 2027 年存储订单的核心不是单纯容量，而是每瓦、每 rack 和 context 访问效率。

## 七、三情景敏感性分析：订单变化百分比和美元变化

### 7.1 情景变量

| 变量 | 悲观 | 务实 | 乐观 |
|---|---|---|---|
| GPU / ASIC 供给 | Blackwell/GB300 allocation 集中，Rubin 延迟；系统交付低于采购意向 | Blackwell 放量、Rubin 2026 年下半年开始交付；定制 ASIC 扩大 | GPU、ASIC、rack-scale 和光互联协同放量，客户可多源采购 |
| HBM 供给 | HBM3E/HBM4 yield 和产能不足，HBM 成为硬上限 | 产能逐季改善，价格保持高位，HBM4 开始量产 | HBM4/HBM4E 堆叠、容量和 ASP 同时上行，供给不再约束 rack |
| 存储供给 | NAND/HDD 价格或供应不利，推理数据需求延后 | SSD/HDD 供给可跟上，AI context storage 增长 | context cache、长上下文、多模态和 agent 日志形成存储爆发 |
| CoWoS/封装 | 扩产慢，基板/测试成为延迟点 | 先进封装扩产兑现但仍偏紧 | 产能、良率和设备交付超预期，封装不再卡住 GPU |
| 电力供给 | interconnection、变压器、发电许可和输电阻塞 | 局部瓶颈；自备电、PPA、旧电厂和分期并网缓解 | FERC/RTO 改革快速转化，behind-the-meter 与微电网批量部署 |
| 融资 | NeoCloud/AI Factory 融资收紧，客户预付款下降 | 投资级项目和大客户继续获得债务、租赁或预付款 | 多层资本平台以项目融资、长期租赁、客户预付和 equity 放大 |
| AI 需求兑现 | utilization、token revenue 和企业 adoption 低于预期 | 训练、推理和 agentic workload 稳定增长 | 模型竞争、多模态、agent 和企业 adoption 超预期 |
| CapEx 增速 | `10-15%` | `20-30%` | `40%+` |

### 7.2 相对务实情景的订单池变化

下表的美元变化使用务实情景各模块的 2026/2027 订单池为基准；“半导体上游”仍是嵌入/诱发层，不与终端订单相加。

| 产业链 | 悲观 vs 务实 | 悲观美元变化（2026 / 2027） | 乐观 vs 务实 | 乐观美元变化（2026 / 2027） | 主要敏感变量 |
|---|---:|---:|---:|---:|---|
| 电力与能源 | `-15% to -30%` | `-$6-15B / -$8-20B` | `+20% to +45%` | `+$8-22B / +$10-30B` | interconnection、变压器、微电网、PPA |
| AI 服务器与机架 | `-20% to -35%` | `-$45-85B / -$60-115B` | `+30% to +60%` | `+$60-145B / +$80-195B` | GPU/HBM、rack-scale、客户预付款、交付 |
| 网络与光互联 | `-15% to -30%` | `-$5-12B / -$7-16B` | `+30% to +70%` | `+$8-28B / +$12-38B` | 800G/1.6T attach、cluster topology、CPO |
| 半导体上游 | `-20% to -35%` | `-$8-20B / -$10-28B` | `+35% to +75%` | `+$15-45B / +$22-65B` | GPU/ASIC、HBM、CoWoS、基板、test；**非加总** |
| 建筑与工程 | `-15% to -25%` | `-$7-17B / -$9-22B` | `+20% to +40%` | `+$10-27B / +$13-36B` | 开工、MEP、人力、电力审批、材料 |
| 冷却 | `-10% to -25%` | `-$3-10B / -$4-13B` | `+35% to +80%` | `+$9-27B / +$13-40B` | rack density、液冷渗透、CDU/冷板产能 |
| 存储 | `-15% to -35%` | `-$3-8B / -$4-11B` | `+25% to +60%` | `+$4-14B / +$6-20B` | 推理数据、context cache、SSD/HDD ASP |

### 7.3 关键敏感度公式

1. **项目转化率**：hyperscaler 资金包不变时，AI/美国/当年转化率每变化 `10%`，终端美国 CapEx 和 compute、network、cooling 订单大致同步变化 `8-10%`；电力和已签 EPC backlog 的收入变化通常滞后 `2-6` 个季度。
2. **1GW 延迟**：按务实混合口径 `$27-36M/MW`，1GW 延迟意味着约 `$27-36B` 的项目采购/收入确认向后移动；不一定取消，但会先影响当年 rack、液冷、PDU 和工程收入。
3. **GPU 效率**：Rubin 对特定 MoE 训练可用更少 GPU，降低每个工作负载的 accelerator 数量；若 token 需求同步增加，总 CapEx 不必同幅下降，订单可能从 GPU 数量转移到网络、内存、存储、电力效率和系统软件。
4. **HBM 约束**：HBM 供给减少 `10%` 不一定让总 CapEx 减少 `10%`；更可能造成 GPU/rack 出货延迟、HBM ASP 上升、服务器收入确认后移，同时电力/土建订单暂时继续。
5. **融资约束**：Oracle FY26 材料披露大规模 AI 合同中约 `$75B` 为客户预付或客户提供 GPU，这类结构降低 cloud operator 自筹 CapEx；若客户预付比例下降，NeoCloud 的 GPU 采购和融资会比 hyperscaler 更敏感。

## 八、公司受益映射：核心受益、间接受益、伪受益

### 8.1 核心受益公司与订单证据

| 公司/股票 | 产业链位置 | 美国 AI 订单映射 | 可见度 | 主要风险/验证 |
|---|---|---|---|---|
| NVIDIA（NVDA） | GPU、NVLink、InfiniBand、Spectrum-X、rack-scale | FY27 Q1 Data Center revenue `$75.2B`；compute `$60.4B`、networking `$14.8B`；Rubin 产品 2026 年下半年由伙伴供货 | 高 | 客户集中、平台效率导致 GPU 数量弹性下降、出口/供给；看 Data Center revenue、Blackwell/Rubin mix |
| Broadcom（AVGO） | custom accelerator、Ethernet、switch silicon、optical connectivity | FY26 Q2 AI semiconductor revenue `$10.8B`，Q3 指引约 `$16.0B` | 高 | 定制 ASIC 客户集中、网络拓扑变化；看 AI revenue、XPU bookings、客户 design win |
| AMD（AMD） | Instinct GPU、EPYC、Helios rack | Meta 多代 `6GW` 协议，首个 `1GW` 预计 2026 年下半年；Q1 2026 Data Center revenue `$5.8B` | 中高 | 软件生态、HBM/封装、实际部署速度；看 MI450/MI455X、Helios 和 Meta 交付 |
| Marvell（MRVL） | custom XPU、800G/1.6T optics、CPO/NPO、scale-up interconnect | 2026-05-27 称 AI bookings exceptional，FY27/FY28 上调，覆盖 800G/1.6T、51.2T switch、XPU | 高 | 客户保密、定制项目延期、估值和竞争；看 data center revenue、design win、CPO ramp |
| Dell（DELL） | AI server、Power Rack、storage、服务和融资 | FY27 Q1 AI orders `$24.4B`、AI revenue `$16.1B`、backlog `$51.3B` | 高 | memory allocation、低毛利整机、客户集中；看 AI server margin、backlog conversion |
| Supermicro（SMCI） | AI server、液冷、rack integration、BMC/系统 | 2026-06-09 拟融资 `$7B` 支付近期 AI server 组件采购 | 中 | 现金流、毛利、营运资金、客户集中；看订单对应发货和毛利，不只看融资规模 |
| Arista（ANET） | AI Ethernet fabric、800G/1.6T switch、网络软件 | Q1 2026 revenue `$2.709B`、同比 `35.1%`；1.6T 系列 2026 Q4/2027 Q1 供货 | 高 | hyperscaler 客户集中、交换芯片依赖；看 AI port、800G/1.6T revenue |
| Coherent（COHR）/ Lumentum（LITE） | InP/EML、laser、optical module、OCS/CPO | NVIDIA 与 Coherent 的 multibillion purchase commitment；NVIDIA 投资 Coherent `$2B`；LITE OCS backlog 超 `$400M` | 中高 | 光模块价格、客户认证、产能爬坡、CPO 时间表；看 ASP、出货、backlog conversion |
| Micron（MU）/ SK hynix / Samsung | HBM4/HBM4E、DRAM、NAND、SSD | HBM4 高量出货/量产；Micron PCIe Gen6 SSD、HBM4、SOCAMM2 已进入量产 | 中高 | HBM yield、内存周期、价格/bit；看 HBM4E 量产和 bit shipment |
| TSMC（TSM）/ ASE / Amkor | 先进制程、CoWoS、封装、测试 | 5.5-reticle CoWoS 生产、扩大尺寸规划；AI 逻辑/HBM/封装客户持续扩产 | 高 | 地缘、基板、封装 yield、capacity timing；看 CoWoS capacity 和客户交付 |
| Vertiv（VRT） | UPS、PDU、液冷、CDU、模块化 power/cooling、服务 | 2025 年末 backlog `$15.0B`、book-to-bill 约 `2.9x`；2026 年液冷产能扩张 | 高 | backlog 转化、组件成本、客户集中；看 Americas orders、毛利和液冷 attach |
| Eaton（ETN）/ Schneider / nVent（NVT） | switchgear、busway、PDU、保护、power architecture、液冷 | Eaton Electrical Americas rolling orders 增长 `42%`，Electrical backlog 同比增长 `48%`；nVent/Siemens/NVIDIA 2026 参考架构 | 高 | 非 AI 电气需求混入、供给扩产、项目延期；看 data center orders、lead time、book-to-bill |
| GE Vernova（GEV） | 变压器、grid、gas power、electrification、BESS | Q1 2026 数据中心电气设备订单 `$2.4B`，多于 2025 全年；gas equipment backlog/slot reservations `100GW` | 中高 | 数据中心占比、燃机订单确认、发电许可；看 Electrification backlog 和 data-center attribution |
| Quanta（PWR）/ Comfort Systems（FIX）/ EMCOR（EME） | 变电站、输配电、低压电气、MEP、工程施工 | PWR Q1 2026 backlog `$48.47B`；FIX backlog `$12.45B`；EME RPO `$15.62B` | 高 | 人工、固定价合同、毛利和 backlog 转换；看 data center-specific bookings |
| Digital Realty（DLR）/ Equinix（EQIX） | powered land、colo、xScale、build-to-suit | DLR 约 `6GW` future development IT capacity、`1.2GW` under construction；EQIX 90+MW xScale、约 1GW powered land | 中高 | CapEx、利率、起租延迟、客户集中；看 leased MW、pre-lease、cash yield |
| CoreWeave（CRWV）/ IREN（IREN） | NeoCloud、GPU-as-a-service、AI Factory | CRWV backlog `$99.4B`、active power >`1GW`、contracted power >`3.5GW`；IREN Microsoft `$9.7B`/`200MW`/20% prepayment | 中 | 杠杆、客户集中、GPU 折旧、利用率和电力；看真实出货、租约、现金流和 debt service |
| Modine（MOD）/ Trane（TT）/ Carrier（CARR） | chiller、liquid cooling、heat rejection | MOD 2027-2029 capacity agreement `$4B+`、upfront `$165M`；TT 收购 LiquidStack；Carrier 投资 ZutaCore | 中高 | 液冷 attach、项目认证、产能和收购整合；看 data center segment revenue/margin |

### 8.2 间接受益与伪受益

| 类型 | 例子 | 为什么不是核心受益 | 研究处理 |
|---|---|---|---|
| 电力运营商/utility | Dominion、AEP、Constellation、Vistra 等 | 受益来自负荷和 rate base，但 AI 项目可能带来成本分摊、监管和燃料风险；客户 CapEx 不等于 utility EPS 同幅增长 | 看 signed load、rate case、generation/transfer investment、成本回收 |
| 传统 HVAC/工业设备 | 多元化 HVAC、普通楼宇自动化公司 | 只有部分产品可进入高密度 AI 机房，普通商用建筑暴露会稀释 AI 订单 | 要求 data center segment、backlog 或项目客户证据 |
| GPU cloud 高杠杆公司 | 小型 NeoCloud、矿企转型项目 | announced MW、GPU 采购和可用电力可能错配；利息和 utilization 决定股东价值 | 先做负债/客户/电力/现金流四项审计 |
| 纯软件/数据标注/模型公司 | AI 应用、通用软件、咨询 | 受益于 AI 使用量，但不直接捕获数据中心建设订单 | 不纳入产业链订单池，另做 AI 需求兑现层 |
| 远期土地和 announced campus | 未锁定电力/融资的开发商 | 规划容量可能重复、撤回或缩水；MW queue 不是已签订单 | 只有 site control、utility commitment、客户/融资后才提高置信度 |

## 九、投资视角总结：α、β、bottleneck 和 2026/2027 订单拐点

### 9.1 α 与 β 分层

| 分层 | 结论 | 代表公司/环节 | 关键理由 |
|---|---|---|---|
| 订单弹性最大（Beta） | compute/rack、网络、光互联和液冷最能放大 CapEx 上修 | NVDA、AVGO、AMD、MRVL、DELL、SMCI、ANET、COHR、LITE、MOD | rack density、GPU/HBM attach 和 1.6T/CPO 使单位 MW 的设备价值上升 |
| 确定性最高（Alpha） | 已有 backlog、认证和长交期的电气、MEP、冷却比远期 GPU 需求更可核验 | ETN、VRT、GEV、PWR、FIX、EME、NVT、Schneider、Siemens | 即使 AI utilization 低，园区仍需变电、UPS、冷却、消防和验收 |
| 高利润池 | 关键瓶颈、平台标准、客户认证和高切换成本环节 | GPU/ASIC、HBM、先进封装、交换芯片、光器件、液冷/CDU、关键电气 | 价值来自 allocation、技术/认证壁垒、系统级集成和定价权，不只是收入规模 |
| 伪受益 | 只有概念暴露、无订单/无 backlog、或被 memory/融资成本挤压的公司 | 未披露客户的 GPU cloud、普通商用 HVAC、远期土地、泛软件 | 需要降低权重，直到看到美元订单、MW、客户预付款或收入确认 |

### 9.2 Bottleneck 清单

| 瓶颈 | 2026 状态 | 2027 状态 | 受益环节 | 被压制环节 | 反证指标 |
|---|---|---|---|---|---|
| 电力接入 | 明显；500MW+ campus 需要新变电站、输电或 behind-the-meter | 局部缓解；有电力的 site premium 仍高 | utilities、变压器、switchgear、微电网 | 无电力的开发商、GPU/rack 交付 | interconnection queue、PPA、变电站投产、实际 energize MW |
| 变压器 / switchgear | 明显；lead time 和认证成为关键路径 | 局部缓解但高压设备仍紧 | ETN、GEV、Schneider、Siemens、NVT、POWL | 只买 GPU 而未锁电力的客户 | lead time、backlog、book-to-bill、取消/延期 |
| HBM | 明显；HBM3E/HBM4 yield、stack、价格约束出货 | 局部缓解；HBM4E、容量和层数成为新约束 | MU、SK hynix、Samsung、封装供应商 | GPU/rack、服务器系统交付 | HBM4E volume、bit shipment、ASP、库存 |
| CoWoS / advanced packaging | 明显/局部；5.5-reticle 和基板/测试排期重要 | 局部缓解但大尺寸封装、CPO 和 chiplet 复杂度上升 | TSMC、ASE、Amkor、AMAT、KLA、Advantest | GPU/ASIC 交付、下一代机架 | monthly capacity、yield、tool acceptance、substrate lead time |
| 液冷集成 | 局部明显；CDU、冷板、泵阀和现场调试需要认证 | 明显转为规模化执行瓶颈，标准化改善但服务仍紧 | VRT、MOD、TT、CARR、NVT、Schneider、Eaton/Boyd | 142kW 以上 rack 的部署速度 | liquid attach、field failure、验收周期、WUE/PUE |
| 工程劳动力 / MEP | 明显；高压电气、管道、commissioning 人才有限 | 局部；预制化改善，但多园区同时开工仍受限 | PWR、FIX、EME、MYRG、STRL、模块化厂商 | 土建/机房开工和租赁起租 | backlog conversion、margin、工期、每季度交付 MW |
| 融资 / 利用率 | NeoCloud 风险高；长期合同和预付款很重要 | 若推理需求兑现则缓解，否则形成 GPU 资产过剩 | 投资级 colo、客户预付、项目融资 | 高杠杆 GPU cloud、短期租赁 | RPO 质量、预付款、利用率、利息覆盖 |

### 9.3 2026 vs 2027 订单拐点

| 年份 | 可能出现的订单拐点 | 最直接受益环节 | 跟踪指标 |
|---|---|---|---|
| 2026 | Blackwell/GB300 NVL72 放量；800G 主流；1.6T 开始 design-in；变压器/switchgear backlog 继续高位；液冷从试点到批量；AMD Helios 首个 1GW 交付 | compute、rack、网络、电力、液冷、EPC | NVIDIA/AMD/AVGO Data Center revenue、Dell AI backlog、VRT/ETN orders、MW energize |
| 2027 | Rubin/HBM4E/下一代 ASIC；1.6T/CPO 与高速铜互联；微电网/自备电扩张；AI Factory/colo 租赁起租；推理 context storage 增强 | 半导体、能源、存储、光互联、REIT、服务 | Rubin/ASIC shipments、HBM4E capacity、CoWoS/tester、leased MW、SSD/HDD ASP、utilization |

## 十、反证条件、风险和后续跟踪清单

### 10.1 反证条件

| 假设 | 反证条件 | 对模型的影响 |
|---|---|---|
| hyperscaler CapEx 持续上行 | Microsoft/Alphabet/Amazon/Meta/Oracle 合计 CapEx 在两个季度内下修 `10-15%` 以上 | 总量从务实/乐观区间下移，服务器和网络先受影响 |
| 美国项目能获得电力 | announced MW 中超过 `60-70%` 在 12-18 个月仍无 site control、utility study 或融资 | 2026/2027 MW 和土建订单下修；只保留电力已锁项目 |
| HBM/封装仍是瓶颈 | HBM4/HBM4E 供给超预期、ASP 快速下跌，但 GPU/rack 出货不增 | HBM 价格弹性下降；半导体设备和内存订单池区间下移 |
| AI 需求兑现 | token usage、Cloud AI revenue、GPU utilization 和客户 RPO 同时减弱 | 2027 乐观区间失效；NeoCloud/colo 资产风险上升 |
| 液冷渗透提升 | 高密度 rack 仍大量采用低功率/air-cooled，液冷 attach 在 2027 不超过模型下限 | MOD/VRT/TT 液冷 Beta 降低，chiller/普通 HVAC占比上升 |
| EPC/MEP backlog 可转化 | backlog 增长但 gross margin 下滑、工期延长和 change order 增加 | 订单规模仍在，但股东利润池缩水；把公司从 Alpha 降为执行风险 |
| announced campus 可落地 | 项目被地方政府、居民、环境/水资源或电网审批推迟超过 12 个月 | 远期 MW 不能纳入当年 CapEx；按延迟而非取消处理，除非客户撤单 |

### 10.2 后续跟踪清单

| 频率 | 指标 | 主要来源 | 触发条件 |
|---|---|---|---|
| 每次财报 | hyperscaler CapEx、finance lease、服务器/网络拆分、AI revenue/RPO | MSFT、GOOGL、AMZN、META、ORCL、NVDA | 合计指引变化超过 `10%` 或“需求不再超过供给” |
| 每月/每季度 | utility interconnection、RTO queue、approved/energized MW、PPA | FERC、PJM、ERCOT、MISO、SPP、州 PUC、utility IR | ready-to-build/energized 转化低于 `20%` 或 queue 撤回明显 |
| 每季度 | backlog、book-to-bill、lead time、价格传导 | ETN、VRT、GEV、NVT、PWR、FIX、EME、Schneider | backlog 增长但交付/毛利连续两个季度恶化 |
| 每季度 | GPU/ASIC、HBM、CoWoS、substrate、tester | NVDA、AMD、AVGO、MRVL、MU、SK hynix、Samsung、TSM、AMAT、Advantest | HBM/封装 supply 约束解除但终端订单同步下降 |
| 每季度 | optical 800G/1.6T/CPO 出货、ASP、客户认证 | ANET、COHR、LITE、MRVL、Corning | 订单增长来自价格而非出货，或 1.6T 量产后推迟 |
| 每季度 | colo leased MW、pre-lease、起租、租金和融资成本 | DLR、EQIX、CoreWeave、IREN、Cipher | backlog/租赁合同增长而 active MW 和现金流不增长 |
| 每季度 | liquid cooling attach、现场验收、PUE/WUE、服务 ARR | VRT、MOD、TT、CARR、NVT、Schneider | 液冷试点多但正式验收和收入确认延迟 |
| 半年度 | 项目取消、社区阻力、用水和电价监管 | CBRE、DOE、州/地方政府、utility | 主要市场 vacancy 上升、租金下降或项目停工 |

### 10.3 风险声明

本报告是产业链订单映射和情景研究，不是单点目标价或投资建议。区间宽度主要来自三类不可观测变量：美国项目的真实 AI 占比、建设转化率以及供应链收入确认时点。任何公司受益判断都应同时检查其非 AI 业务、客户集中度、毛利、营运资金、负债和估值；订单增长本身不保证每股收益增长。

## 十一、Reference 和数字来源附录

以下来源不是“链接清单”，每一条都注明支持的数字或判断。公司/政府/项目文件为一手来源；行业文件用于边界和交叉验证；模型估算不把第三方预测当作事实。

| 来源 | 日期 | 来源层级 | 支持的数字/判断 | 是否一手 | 置信度 | 备注 |
|---|---|---|---|---|---|---|
| [Microsoft FY26 Q3 earnings call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3) | 2026-04-29 | 公司 call | 2026 CapEx 约 `$190B`、约 `$25B` 组件价格影响；至少 2026 年仍受容量约束 | 是 | 高 | Fairwater、GPU/CPU/storage capacity 和需求供给表述 |
| [Microsoft FY26 Q1 earnings call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q1) | 2025-10-29 | 公司 call | AI capacity 当年增长超过 `80%`、未来两年数据中心 footprint 约翻倍、Fairwater 2GW | 是 | 高 | 用于 physical scale 和建设周期校验 |
| [Alphabet 2025 Q4 earnings call](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx) | 2026-02-04 | 公司 call | CapEx `$175-185B`；服务器约 `60%`、data center/networking 约 `40%`；ML compute 略超一半给 Cloud | 是 | 高 | 直接支持总量和 compute/facility 拆分 |
| [Amazon 2025 Q4 results](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx) | 2026-02-05 | 公司财报 | 2026 全 Amazon CapEx 约 `$200B`；AI、芯片、机器人等混合 | 是 | 高 | 不把全额直接视为美国 AI CapEx |
| [Meta Q1 2026 results](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/) | 2026-04-29 | 公司财报 | 2026 CapEx `$125-145B`，含 finance lease principal payments；Q1 CapEx `$19.84B` | 是 | 高 | AI 与 core business 混合，需乘模型占比 |
| [Oracle FY26 results](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Record-Q4-and-FY-2026-Results-Driven-by-Cloud-Infrastructure--Cloud-Applications/) | 2026-06-10 | 公司财报 | FY26 CapEx TTM 约 `$55.7B`；RPO `$638B`；客户预付/提供 GPU 约 `$75B`；FY26 debt/equity financing | 是 | 高 | 直接支持融资、RPO 质量和 NeoCloud 风险 |
| [NVIDIA FY27 Q1 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx) | 2026-05-20 | 公司财报 | Data Center revenue `$75.2B`；compute `$60.4B`；networking `$14.8B` | 是 | 高 | 全球收入，用于行业 momentum 不是美国拆分 |
| [NVIDIA Rubin platform](https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer) | 2026-01-05 | 产品/路线 | Rubin、Vera CPU、ConnectX-9、BlueField-4、Spectrum-6；伙伴产品 2026 年下半年供货 | 是 | 高 | 支持 2027 订单拐点和网络/存储 attach |
| [NVIDIA GB200/NVL72](https://www.nvidia.com/en-gb/data-center/gb200-nvl72/) | 2026-07-10 访问 | 产品资料 | 72-GPU、HBM3E、液冷 rack-scale 架构 | 是 | 高 | 产品页；功率以官方文档交叉验证 |
| [NVIDIA GB300 NVL72 Enterprise Reference Architecture](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) | 2026-06 | 技术文档 | 8 个 `33kW` power shelf；full rack 最高约 `142kW`；72 GPU | 是 | 高 | 支持 rack density、power shelf、液冷模型 |
| [Broadcom FY26 Q2 results](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial) | 2026-06-03 | 公司财报 | AI semiconductor revenue `$10.8B`；Q3 约 `$16.0B` | 是 | 高 | custom accelerator 和 AI networking 订单验证 |
| [AMD Q1 2026 results](https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results) | 2026-05-05 | 公司财报 | Data Center revenue `$5.8B`；MI450/Helios pipeline | 是 | 高 | 支持 AMD 作为第二来源和 inference/agentic 方向 |
| [AMD-Meta 6GW agreement](https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000045/pressreleasedatedfebruary2.htm) | 2026-02-24 | 公司公告 | 多代 `6GW`；首个 `1GW` 预计 2026 年下半年出货 | 是 | 高 | 支持 AI Factory / rack-scale 物理规模 |
| [Dell FY27 Q1 earnings call](https://investors.delltechnologies.com/static-files/b63ffff9-b729-403b-a231-c6af05667759) | 2026-05-28 | 公司 call | AI orders `$24.4B`、AI revenue `$16.1B`、backlog `$51.3B`；memory 约束 | 是 | 高 | 服务器订单和 memory bottleneck 的直接证据 |
| [Supermicro `$7B` financing](https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Proposed-7-0-Billion-of-Equity-and-Equity-linked-Financing-Transactions-To-Fund-AI-Orders/default.aspx) | 2026-06-09 | 公司公告 | 为近期 AI server orders 采购组件拟融资 `$7B` | 是 | 高 | 只证明资金需求和订单存在，不证明盈利 |
| [Arista Q1 2026 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-First-Quarter-2026-Financial-Results/default.aspx) | 2026-05-05 | 公司财报 | Q1 revenue `$2.709B`、同比 `35.1%`；AI networking/XPO | 是 | 高 | 支持网络需求和液冷光互联方向 |
| [Arista 1.6T portfolio](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Introduces-Next-Generation-1-6Terabit-Portfolio-for-AI-Fabrics/default.aspx) | 2026-06-09 | 产品公告 | 1.6T AI fabric；液冷版本和 800G 版本的 2026 Q4/2027 Q1 时间表 | 是 | 高 | 支持 2026-2027 网络拐点 |
| [Lumentum FY26 Q2 results](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx) | 2026-02-03 | 公司财报 | OCS backlog 超 `$400M`；CPO 数亿美元级、2027 年上半年交付 | 是 | 中高 | 公司披露的订单/时间表，需跟踪兑现 |
| [NVIDIA-Coherent partnership](https://www.coherent.com/news/press-releases/nvidia-and-coherent-announce-strategic-partnership) | 2026-03-02 | 公司公告 | multibillion purchase commitment；NVIDIA 投资 Coherent `$2B` | 是 | 高 | 先进光学 capacity 和客户锁定证据 |
| [Micron HBM4/Rubin/SSD](https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin) | 2026-03-16 | 公司公告 | HBM4 36GB 12H、PCIe Gen6 SSD、SOCAMM2 量产 | 是 | 高 | 支持 HBM、memory、SSD 和 Rubin attach |
| [Micron Q3 FY26 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-record-results-third-quarter) | 2026-06-24 | 公司财报 | HBM4 高量出货；HBM4E 2027 量产预期；245TB QLC SSD | 是 | 高 | 支持 2027 HBM4E 和存储拐点 |
| [Samsung HBM4 mass production](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 2026-02-12 | 公司公告 | HBM4 mass production、客户出货、11.7Gbps/最高 13Gbps | 是 | 高 | HBM4 供给改善的交叉验证 |
| [TSMC 2026 North America Technology Symposium](https://pr.tsmc.com/english/news/3302) | 2026-05-22 | 技术公告 | 5.5-reticle CoWoS 生产、规划更大尺寸封装 | 是 | 高 | CoWoS 产能和大尺寸封装路线 |
| [Applied Materials Q2 2026 results](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-second-quarter-2026-results) | 2026-05-21 | 公司财报 | 2026 半导体设备业务增长预期超过 `30%`；HBM/先进封装合作 | 是 | 高 | 半导体设备滞后层和 HBM/封装需求 |
| [Advantest FY26 financial review](https://www.advantest.com/en/investors/financial-highlights/review/) | 2026-05 | 公司财报 | FY ended 2026-03-31 sales 同比增长 `44.7%`，AI/HPC/DRAM test 需求强 | 是 | 高 | 避免把非美元报表直接当作美元订单；测试设备订单验证 |
| [Vertiv FY25 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 2026-02-11 | 公司财报 | orders 同比 `252%`、book-to-bill `2.9x`、backlog `$15.0B` | 是 | 高 | power/cooling 确定性和 backlog |
| [Vertiv Ohio thermal expansion](https://investors.vertiv.com/news/news-details/2026/Vertiv-to-Expand-Ohio-Manufacturing-to-Boost-U-S--Production-of-Critical-Thermal-Management-Technologies-for-AI-Data-Centers/) | 2026-03-30 | 公司公告 | 2027 Q2 投产；液冷/冷冻水系统产能约提升 `45%` | 是 | 高 | 供给扩张、液冷瓶颈 |
| [Eaton Q1 2026 results](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html) | 2026-04 | 公司财报 | Electrical Americas rolling orders 增长 `42%`、Electrical backlog 增长 `48%` | 是 | 高 | 电气设备 backlog |
| [GE Vernova Q1 2026 results](https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf) | 2026-04-22 | 公司财报 | 数据中心电气设备订单 `$2.4B`；gas backlog/slot reservations `100GW` | 是 | 高 | 电气、发电和变压器证据 |
| [Quanta 2026 Q1 filing](https://investors.quantaservices.com/sec-filings/all-sec-filings/content/0001050915-26-000016/0001050915-26-000016.pdf) | 2026-04-30 | 公司 10-Q | backlog `$48.47B`；高压/低压/数据中心及 utility infrastructure | 是 | 高 | 工程和电网订单可见度 |
| [Comfort Systems USA Q1 2026](https://investors.comfortsystemsusa.com/news-releases/news-release-details/comfort-systems-usa-reports-first-quarter-2026-results) | 2026-04-23 | 公司财报 | backlog `$12.45B` | 是 | 高 | MEP backlog 验证 |
| [EMCOR Q1 2026](https://emcorgroup.com/investor-relations/press-releases/2026-news/emcor-group-inc-reports-first-quarter-2026-results) | 2026-04-29 | 公司财报 | RPO `$15.62B`、收入 `$4.63B` | 是 | 高 | 工程/MEP backlog 验证 |
| [Modine `$4B` cooling capacity agreement](https://investors.modine.com/news/news-details/2026/Modine-Announces-Landmark-$4-Billion-Long-Term-Capacity-Agreement-through-2029-with-Strategic-Data-Center-Customer-for-Airedale-by-Modine-Cooling-Solutions/default.aspx) | 2026-05-26 | 公司公告 | 2027-2029 超过 `$4B` capacity agreement；upfront `$165M` | 是 | 高 | 液冷/chiller 长期订单和客户预付 |
| [Digital Realty June 2026 presentation](https://investor.digitalrealty.com/static-files/3fa86ccd-e071-4b5f-85d7-5885df9e4b80) | 2026-06 | 公司演示 | in-place、future development、under-construction IT capacity 和 AI/cloud development | 是 | 高 | REIT/colo MW pipeline |
| [Equinix 2026 outlook](https://investor.equinix.com/news-events/press-releases/detail/1096/equinix-provides-robust-2026-outlook-driven-by-strong) | 2026-02 | 公司财报/指引 | `90+MW` xScale、约 `1GW` powered land、2026 CapEx `$3.655-4.155B` | 是 | 高 | colo/land/CapEx 交叉验证 |
| [CoreWeave Q1 2026](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-First-Quarter-2026-Results/) | 2026-05-07 | 公司财报 | backlog `$99.4B`、active power >`1GW`、contracted power >`3.5GW` | 是 | 中高 | NeoCloud 订单和融资风险；需检查现金流/利用率 |
| [IREN-Microsoft `$9.7B` agreement](https://iren.com/resources/blog/iren-signs97-billion-agreement-with-microsoft-to-deploy-ai-cloud-infrastructure) | 2025-11-03 | 公司公告 | `200MW` critical IT load、20% prepayment、约 `$1.94B` annualized run-rate | 是 | 高 | AI Cloud/colo 项目订单和预付款 |
| [CBRE North America Data Center Trends](https://www.cbre.com/press-releases/fast-growing-north-american-data-center-market-set-records-in-2025) | 2026-02-26 | 行业报告 | 2025 存量 `9,432MW`、吸收 `2,497.6MW`、在建 `5,994.4MW`、vacancy `1.4%`、租金 `$194.95/kW/月` | 否 | 高 | 主要市场供需和价格交叉验证 |
| [CBRE U.S. Real Estate Outlook 2026: Data Centers](https://www.cbre.com/insights/books/us-real-estate-market-outlook-2026/data-centers) | 2025-12 | 行业报告 | 500MW+ campus、多年建设；`24-48+个月` interconnection；preleasing 中值约 `70%+` | 否 | 中高 | 建设周期、pre-lease 和 power-first 选址 |
| [Uptime Intelligence Giant Data Center Analysis 2026](https://intelligence.uptimeinstitute.com/sites/default/files/2026-01/UI%20Field%20report%20194_Giant%20data%20center%20power%20plans%20reach%20extreme%20levels.pdf) | 2026-01 | 行业研究 | 2025 proposals `181,209MW`；AI `76,880MW`；预计只有约 `25%` planned provisioned power actively utilized | 否 | 中 | announced queue 的上限和 25% 实际转化约束 |
| [DOE/LBNL data center electricity report release](https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers) | 2024-12-20 | 政府/实验室 | 2023 `176TWh`；2028 `325-580TWh`；数据中心占美国用电 `6.7-12%` | 是 | 高 | 美国用电和电力约束的长期边界 |
| [FERC large load action](https://www.ferc.gov/news-events/news/ferc-launches-aggressive-targeted-action-speed-large-load-integration) | 2026-06-18 | 政府/监管 | 六大 RTO/ISO 大负荷规则改革、co-location、cost allocation、behind-the-meter | 是 | 高 | 并网改革方向，不代表项目必然通电 |
| [ERCOT Batch Zero announcement](https://www.ercot.com/news/release/06182026-puct-approves-ercots) | 2026-06-18 | 电力/RTO | 大负荷请求 `438,000MW`，约 `89%` 数据中心；75MW+ batch study | 是 | 中高 | queue 规模和 speculative risk；与实际 energize MW 分开 |
| [Microsoft/UT Austin AI data center lifecycle paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/AI-DC-Lifecycle-Compass.pdf) | 2026-03 | 论文/技术研究 | 10MW AI DC、500 H100、70GWh/year；CapEx components `$7.0/W` power、`$2.5/W` cooling、`$375k/server` | 部分一手 | 中高 | 用于单 MW、rack、power/cooling 结构；不是全市场预测 |

### 11.1 模型估算与置信度总表

| 模型项 | 2026/2027 估算 | 置信度 | 主要原因 | 反证条件 |
|---|---:|---|---|---|
| 美国 AI DC 总 CapEx | `$260-900B` 按情景/年份 | 中 | hyperscaler CapEx 公开，AI/美国/转化率不公开 | CapEx guide 下修、项目 queue 不转化 |
| 新增/扩建 AI IT load | `6-25GW` 按情景/年份 | 中低 | 依赖 MW 转化、IT/facility ratio 和设备提前采购 | energize MW、utility study、PPA 不增长 |
| GPU/ASIC 等效数量 | `1.2-7.0M` 按情景/年份 | 低中 | SKU、效率、定制 ASIC 和利用率未知 | 出货、客户 allocation 和 rack BOM 不支持 |
| compute 终端订单 | `$130-540B` 按情景/年份 | 中 | 由 CapEx share、Dell/NVIDIA/AMD/AVGO 订单锚点估算 | GPU/HBM订单取消、AI server revenue 下修 |
| 电力/能源订单 | `$72-150B` 务实顶层池 | 中 | backlog、utility 和设备订单证据较强 | lead time 缩短但订单/收入下滑、项目延迟 |
| 液冷订单 | `$12-38B` 子环节 | 中低 | 公开 capacity agreements 少，attach rate 不透明 | 2027 高密度 rack 仍大规模 air-cooling |
| 上游 HBM/CoWoS/WFE | `$48-154B` 嵌入/诱发 | 低中 | 技术路线清晰但价格、产能和归因复杂 | GPU 数量下降、HBM ASP/bit shipment 快速回落 |

报告更新时，应优先替换“主要数据日期”之后的 company guidance、RTO energization、HBM/CoWoS capacity、backlog 和 leased MW，而不是直接调整情景中值。这样模型才能保持可复核、可更新和可证伪。
