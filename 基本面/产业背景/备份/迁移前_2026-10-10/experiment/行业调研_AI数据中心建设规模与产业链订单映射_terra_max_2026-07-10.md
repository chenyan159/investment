# AI数据中心建设规模与产业链订单映射（2026-2027，美国主导）

报告日期：2026-07-10（美国太平洋时间）  
主要数据日期：2025-12-31 至 2026-07-10；不同公司财报采用其各自财季，逐项标注。  
估值/股价快照日期：2026-07-10；本报告不把股价、估值倍数或目标价作为规模模型输入。  
方案版本：2026-06-04；本次为基于公开外部资料重新建立的独立模型，不读取、引用或继承本地旧研究、索引、缓存或中间结论。

> 读法：除来源的已披露精确值外，正文所有预测规模均为区间。`客户 CapEx` 是不重复的客户支出口径；HBM、CoWoS、半导体设备等为对该 CapEx 的“价值穿透/上游订单池”，**不得再与客户 CapEx 相加**。这条处理是避免把一颗 GPU 内含的 HBM、封装与整机价格重复计算三次。

## 核心结论摘要

| 结论 | 2026 | 2027 | 可复核的核心依据 | 置信度 |
|---|---:|---:|---|---|
| 美国 AI 数据中心全口径建设 CapEx，务实情景 | `$335-410B` | `$410-510B` | 五大云厂商全球 CapEx 锚点、美国/AI/建设转化系数、NeoCloud/colo 净增量 [R01-R09] | 中 |
| 美国 AI 数据中心全口径建设 CapEx，乐观情景 | `$430-530B` | `$600-750B` | GPU/ASIC 供给按计划释放、AI Factory 融资不收紧、自备电/微电网缩短接入瓶颈 | 低-中 |
| 2026-2027 最硬的约束 | 电力接入、变压器/switchgear、燃机 slot、HBM/先进封装、MEP 劳动力 | 电力仍是第一约束；HBM/CoWoS 从“绝对瓶颈”转为“高价紧平衡”的概率上升 | FERC 大负荷改革、Oncor 请求、Eaton/GEV/Vertiv backlog、Micron/TSMC 路线 [R10-R18] | 高 |
| 最大订单弹性（beta） | 高密度 rack、1.6T 网络、液冷、微电网/自备电 | Rubin/定制 ASIC、HBM4、封装测试、推理存储、AI Factory EPC | 单机架功率由传统 `8-20kW` 向 `90-150kW+` 迁移；GB300 NVL72 最高约 `142kW/rack` [R19] | 中-高 |
| 确定性最高（alpha） | 配电、UPS、switchgear、液冷集成、EPC/MEP | 电力设备、项目交付、服务/运维 | 这些支出是通电与验收的硬前置条件，不能由“模型效率提升”替代 | 中-高 |

## 一、结论先行：总规模、最大瓶颈和最大订单弹性

### 1.1 本报告的中心判断

美国在 2026 年处于“GPU 订单—园区开工—电力接入—机架验收”同时拥挤的阶段，而 2027 年更像“Rubin/定制 ASIC—自备电—AI Factory 转收入—推理存储”共同驱动的第二波。务实情景下，**美国境内可归属的 AI 数据中心建设 CapEx** 为 2026 年 `$335-410B`、2027 年 `$410-510B`。这个口径包括 GPU/ASIC 服务器、网络、存储、机电、土建、能源接入、微电网、冷却与集成；不包括纯软件、人力、耗电费、普通企业 IT refresh 和海外项目。

该结论不是把五大云厂商 CapEx 直接相加。Microsoft 已表示 2026 日历年 CapEx 约 `$190B`；Alphabet 指引 `$175-185B`，且其 2025 CapEx 中约 `60%` 是服务器、`40%` 是数据中心与网络；Meta 指引 `$125-145B`；Amazon 预计约 `$200B`；Oracle FY2026 已支出 `$55.7B` 并以客户预付款/融资支持 OCI 扩张 [R01-R05]。这些是全球、混合用途、不同会计口径的总额，因此本模型才对每家依次施加 **AI/数据中心占比 × 美国建设占比 × 当年建设转化率**，再扣掉租赁/客户预付款造成的重复。

### 1.2 三情景总规模

| 年份 | 悲观 | 务实 | 乐观 |
|---|---:|---:|---:|
| 2026（美国） | `$245-300B` | `$335-410B` | `$430-530B` |
| 2027（美国） | `$275-345B` | `$410-510B` | `$600-750B` |

| 情景 | 2026-2027 中枢增速 | 解释 | 最快反证 |
|---|---:|---|---|
| 悲观 | `10-15%` | GPU/HBM 价格高而供给/融资受限；已签项目因接入、变压器、审批或劳动力而延后；NeoCloud 以延租替代自建 | 云厂商下调 CapEx、服务器 backlog 连续两个季度下降、已签 MW 转为取消/延期 |
| 务实 | `20-30%` | Blackwell/GB300 大规模部署，Rubin 准备订单开始进入；局部电力瓶颈由自备电、临时电、PPA 和园区迁移缓解 | 供应商 book-to-bill 回落至 `<1.0x`，AWS/Azure/GCP 供给紧张明显缓解，PPA/变电站投产不及计划 |
| 乐观 | `40%+` | 定制 ASIC 与 GPU 同时放量，AI Factory 项目由融资/预付款支持；大园区直接配置燃机、BESS、专用变电站 | HBM4 良率/封装良率失败、燃机 slot 或电网许可使新园区无法在 2027 通电、利用率/AI 收入不兑现 |

### 1.3 订单最值得跟踪的排序

| 排名 | 环节 | 2026-2027 订单属性 | 为什么不是概念叙事 | 重点公司（美国需求暴露，不限上市地） |
|---:|---|---|---|---|
| 1 | 变压器、switchgear、UPS、busway、配电 | 高确定性、长交期、项目硬门槛 | GPU 到货但无电不能验收；Eaton 电气美洲数据中心订单在 2026Q1 同比约增 `240%` [R16] | Eaton、Schneider、Vertiv、Powell、Hubbell、GE Vernova |
| 2 | GPU/ASIC、AI 整机、rack-scale 集成 | 最大绝对金额 | NVIDIA FY2027Q1 数据中心收入 `$75.2B`，其中 compute `$60.4B`、networking `$14.8B` [R20] | NVIDIA、AMD、Broadcom、Dell、SMCI、HPE、Quanta、Wiwynn、Celestica |
| 3 | 液冷、CDU、冷水机、泵阀、预制化白空间 | 订单弹性大、供给偏紧 | GB300 NVL72 是全液冷架构且单 rack 最高约 `142kW` [R19] | Vertiv、Schneider、Modine、nVent、JCI、Carrier、Trane |
| 4 | 800G/1.6T、交换机、NIC/DPU、AEC/DAC | 2027 弹性高于 2026 | 1.6T 开始进入 rack-scale AI fabric；Arista 已发布面向 AI fabric 的 1.6T 平台 [R21] | Arista、Broadcom、NVIDIA、Marvell、Coherent、Lumentum、Innolight |
| 5 | HBM、CoWoS、测试、半导体设备 | 高利润穿透池、确认滞后 | HBM4 已开始放量，HBM4E 的量产目标在 2027；TSMC 持续扩大 CoWoS [R17-R18] | Micron、SK hynix、Samsung、TSMC、ASE、Amkor、Advantest、Teradyne、AMAT、LRCX、KLAC |
| 6 | EPC/MEP、预制模块、REIT/colo | 由“开工”向“收入确认”错位 | 能源、土建、设备进场和租赁起租不是同一日期；Digital Realty 在建/可开发容量与预租反映项目持续性 [R07-R08] | EMCOR、Quanta、Mastec、Fluor、Jacobs、DLR、EQIX、APLD、CRWV |

## 二、研究口径、资料边界和估算方法

### 2.1 资料边界与定义

| 口径 | 本报告定义 | 纳入 | 排除或单列 |
|---|---|---|---|
| AI 数据中心建设规模 | 为训练、推理、AI Factory、GPU/ASIC 集群和高密度 AI rack 服务的新建、扩建、改造所形成的美国客户 CapEx | Hyperscaler、NeoCloud、AI Factory、AI colo/build-to-suit、能源接入、机电与集成 | 小型企业 on-prem、传统 IT refresh、普通 colo、加密矿场、纯软件/人员/电费 |
| 客户 CapEx | 终端客户或其融资/租赁载体在建设时支付的资本性投入 | 服务器、网络、存储、电力、冷却、土建、MEP、能源接入、BESS、设计集成 | 上游半导体厂再投资；后者只作穿透订单池，不可相加 |
| 订单池 | 客户 CapEx 传导给供应商的可签约设备、工程、集成和服务机会 | 硬件、EPC、集成、预制模块、长期维护 | 未签约远期规划、无法履约 backlog、纯估值主题 |
| 美国主导 | 美国境内项目和美国客户决策可明确映射的需求 | 美国园区、美国客户主导的供货、海外厂商对美供货 | 中国市场、主权云、欧洲/中东建设，除非仅作对照 |
| 上游穿透池 | 已嵌入服务器/网络/存储价格的半导体价值与产能再投资 | GPU/ASIC、HBM、CoWoS、测试、WFE | 不计入建设总额；用于评估谁拿到利润和瓶颈溢价 |

### 2.2 来源优先级与日期治理

本报告仅使用联网获得的公开资料作为事实基础：公司财报/电话会、监管/电网/utility 文件、公司产品文档、IR 公告和有署名的行业资料。非正式线索不作为总规模锚点；凡使用，均在附录中标为“非正式/低置信度”。所有动态数字均带源日期，且以 2026-07-10 为截止日。

| 日期层 | 本报告处理 | 例子 |
|---|---|---|
| 报告完成日期 | `2026-07-10` | 结论、情景与来源截止日 |
| 数据披露日期 | 每条参考来源单列 | Meta 2026Q1 于 2026-04-29 上调 CapEx 指引；Oracle FY2026 于 2026-06-10 披露 |
| 估值/股价快照日期 | `2026-07-10` | 本稿不使用任何实时股价或估值输入，避免把估值叙事混入订单模型 |

### 2.3 总量公式与防重复规则

```text
美国 AI 数据中心建设规模(year, scenario)
= Σ[客户群全球 CapEx × AI/数据中心占比 × 美国建设占比 × 当年建设转化率]
+ NeoCloud / AI Factory 增量融资与自建 CapEx
+ AI colo / REIT 专用 AI build-to-suit 的非重叠部分
- 客户 finance lease、预付款、租赁载体和同一项目的重复确认
- 非 AI 云、普通 IT refresh、海外建设、尚未可执行的远期规划
```

防重复的三个规则：

1. 同一项目若客户把设备列为 finance lease、开发商列为建设 CapEx，只留最终承担建设风险的一侧，并给出 `$15-35B` 的年度重复扣减带。
2. GPU 服务器总价已含 GPU、HBM、封装、主板和部分网络；HBM/CoWoS 只在“穿透池”中显示，不再加回建设总额。
3. 数据中心 REIT 的“已签 MW/未来租金”不是当年建设收入；其建造订单与客户自建/租赁项目存在交集，只以净新增方式进入总量。

### 2.4 CapEx 锚点与模型输入（务实情景）

| 客户群/证据 | 已披露的全球锚点与日期 | 模型 AI/DC 占比 | 美国建设占比 | 当年建设转化率 | 对 2026 美国 AI CapEx 的贡献 | 证据强度 |
|---|---:|---:|---:|---:|---:|---|
| Microsoft | 2026 日历年预计 CapEx 约 `$190B`；2026Q3 资本开支 `$31.9B` [R01] | `70-85%` | `55-65%` | `80-95%` | `$70-95B` | 高 |
| Alphabet | 2026 CapEx 指引 `$175-185B`；结构约 `60%` 服务器、`40%` 数据中心/网络 [R02] | `70-85%` | `45-55%` | `80-95%` | `$48-75B` | 高 |
| Meta | 2026 CapEx 指引 `$125-145B`，主要用于 AI 与数据中心 [R03] | `75-90%` | `75-90%` | `85-98%` | `$65-95B` | 高 |
| Amazon | 2026 公司 CapEx 预计约 `$200B`，但含 AI、芯片、机器人和低轨卫星 [R04] | `55-70%` | `50-65%` | `75-90%` | `$50-70B` | 中-高 |
| Oracle | FY2026 CapEx `$55.7B`；RPO/预付款与融资支持 OCI 扩张 [R05] | `70-90%` | `60-75%` | `80-95%` | `$25-40B` | 高 |
| NeoCloud / AI Factory | CoreWeave 2026Q1 backlog `$99.4B`、已签/合同电力超过 `3.5GW`；OpenAI/Oracle/Stargate 多 GW 站点 [R06, R28-R30] | 不适用 | `75-95%` | `45-75%` | `$30-55B` | 中 |
| AI colo / REIT / build-to-suit | Digital Realty、Equinix、Applied Digital 的在建/预租/已签 MW 反映供给载体 [R07-R09] | 不适用 | `55-80%` | `50-75%` | `$20-40B` 毛额，净额计入较少 | 中 |
| 重复/延迟扣减 | finance lease、客户预付款、未通电项目、跨年交付 | 不适用 | 不适用 | 不适用 | `-$15-35B` | 中 |

**务实情景总量的建模结果**：先得到五大云厂商 `$258-375B` 的美国 AI 建设候选池；再加入 NeoCloud/AI Factory 与 AI colo 的净增量，扣除租赁与跨年重复后，校准为 `$335-410B`。区间而不是单点的原因是：公司不会披露“AI 占比 × 美国占比 × 当前年实际通电比例”，且 Amazon、Oracle 与租赁载体的会计处理差异较大。

### 2.5 物理规模的独立校验框架

| 校验锚 | 外部事实 | 本模型用法 |
|---|---|---|
| 全美负荷 | DOE/LBNL 估计数据中心 2023 年耗电 `176TWh`，2028 年为 `325-580TWh`；EIA 明确认为 2026-2027 负荷增长由大算力设施驱动 [R10-R11] | 总量不能只由财务 CapEx 推导，必须受可获得 MW 限制 |
| 电网/接入 | FERC 于 2026-06-18 要求各区域电网说明或改革大负荷接入规则；Oncor 收到约 `271GW` 数据中心请求、只向 ERCOT 提交 `122GW` 大负荷预测 [R12-R13] | “申请 MW”不能直接等于“可通电 MW”；用较低的建设转化率 |
| 园区与预租 | CBRE 统计北美主要市场 2025 年末在建约 `5,994MW`；Digital Realty 2026Q1 展示超过 `1.2GW` 在建/可建设容量与超过 `6GW` 后备开发容量 [R07, R15] | 公开 REIT 数据只覆盖部分市场；Hyperscaler 自建与大园区不应被遗漏 |
| 单 MW 成本 | JLL 对 2026 全球平均建设成本约 `$11.3M/MW`，高密度 AI 基础设施可到约 `$25M/MW`；本模型对美国 AI 集群采用 `$21-31M/MW` 的全口径区间 [R14] | 用于交叉验证，不把普通 colo 成本机械套给 AI rack |

## 三、美国 AI 数据中心建设总规模：2026/2027 三情景

### 3.1 总量与客户群拆分

| 年份 / 情景 | Hyperscaler 净建设 CapEx | NeoCloud / AI Factory | AI colo / REIT 净建设 | 重复和不可交付扣减 | 美国 AI DC 建设总额 |
|---|---:|---:|---:|---:|---:|
| 2026 悲观 | `$205-245B` | `$22-35B` | `$18-28B` | `-$10-18B` | `$245-300B` |
| 2026 务实 | `$258-375B` | `$30-55B` | `$20-40B` | `-$15-35B` | `$335-410B` |
| 2026 乐观 | `$330-455B` | `$48-80B` | `$35-60B` | `-$18-35B` | `$430-530B` |
| 2027 悲观 | `$225-280B` | `$25-42B` | `$22-35B` | `-$12-20B` | `$275-345B` |
| 2027 务实 | `$320-415B` | `$42-70B` | `$32-55B` | `-$22-35B` | `$410-510B` |
| 2027 乐观 | `$470-610B` | `$70-115B` | `$55-95B` | `-$35-70B` | `$600-750B` |

> 注：`AI colo / REIT` 行是以开发商承担建设的净部分计入；同一 build-to-suit 若已在 Hyperscaler finance lease 中确认，必须在“重复和不可交付扣减”中抵消。各列端点不适合机械相加，最后一列是按项目归属去重后的结果。

### 3.2 四类决定总量的驱动与反证

| 驱动 | 悲观 | 务实 | 乐观 | 关键跟踪指标 |
|---|---|---|---|---|
| GPU / ASIC 供给 | HBM/封装分配集中，GB300 与定制 ASIC 交付延后 | Blackwell 放量、GB300 进入规模部署，Rubin 开始预订 | GPU、定制 ASIC、rack-scale 系统同步扩产 | NVIDIA/AMD/AVGO 数据中心收入、Dell/SMCI backlog、客户预付款、rack 出货 |
| HBM / CoWoS / advanced packaging | HBM4 良率、基板与测试拖慢整机 | HBM4 逐季改善、价格高位、CoWoS 仍紧 | HBM4/HBM4E、CoWoS 与测试扩产超预期 | HBM bit shipment、ASP、TSMC/OSAT 产能、测试机利用率 |
| 电力瓶颈 | 等待并网、变电站、燃机和许可，设备到站却不能通电 | 关键区域受限，德州/中西部/东南部通过自备电与迁址缓解 | 园区式专用变电站、燃机/BESS、PPA 快速落地 | interconnection queue、变电站投产、PPA、燃机 slot、FERC/州审批 |
| 融资环境 | NeoCloud 债务成本上升，预租变短、股权融资摊薄 | 大客户和有合同/电力资产的项目继续融资 | 客户预付款、基础设施基金与长期租赁降低资金成本 | project finance、lease prepayment、债券利差、客户集中度 |
| AI 需求兑现 | utilization、推理单价和企业 adoption 不及预期 | 训练与推理稳定扩张、供给继续紧张 | agent、多模态、长期上下文和企业工作流推动 token/GPU 消耗 | 云 AI 收入、GPU 利用率、RPO、客户续约、推理 token/美元 |

### 3.3 关键项目/需求锚点：可用来否定或支持总量

| 项目或平台 | 已披露信号 | 对模型的含义 | 使用限制 |
|---|---|---|---|
| Microsoft Fairwater | 2026 财年电话会称其 Wisconsin Fairwater 可扩至 `2GW`，并计划两年内约翻倍整体数据中心 footprint [R01] | 证明单园区已经从百 MW 进入多 GW；支持 2027 电力设备、冷却和 MEP 的持续性 | 不能把 `2GW` 当年全部计入 2026 CapEx |
| Stargate / Oracle / OpenAI | 已宣布多个美国站点；OpenAI 称 10GW 目标、已在 90 天新增超过 `3GW` 计划/能力 [R28-R30] | AI Factory 的上行尾部真实存在，尤其是 2027 | “计划 MW”不等于已签设备、通电 MW 或收入 |
| Anthropic / AWS | 2026-04 披露最多 `5GW` 新算力安排，年末近 `1GW` Trainium2/3 容量计划上线 [R30] | 定制 ASIC 使 “GPU only” 模型低估网络、HBM、功率和建造总量 | 多年承诺，年度建设节奏仍不确定 |
| CoreWeave | 2026Q1 backlog `$99.4B`，合同电力逾 `3.5GW` [R06] | NeoCloud 是订单弹性来源，也增加融资/客户集中度风险 | backlog 是服务收入，不等于年度设备 CapEx |
| Digital Realty / Applied Digital | DLR 在建与后备容量可观；APLD 已宣布超过 `1GW` 合同容量 [R07-R09] | 租赁型 AI Factory 把 CapEx 从云厂商资产负债表转移至开发商 | 预租、施工、上电、租金确认存在多年时滞 |

## 四、从 CapEx 到物理规模：MW、rack、GPU、建设周期交叉验证

### 4.1 物理规模交叉验证

| 年份 / 情景 | 建设 CapEx | 全口径 CapEx / 新建 AI IT load | 对应当年深度开工/签约 AI IT load | 当年实际通电 AI IT load | 高密度 rack 等价数 | GPU/ASIC 等价数 | 设施峰值负荷（PUE `1.15-1.30`） |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026 悲观 | `$245-300B` | `$23-30M/MW` | `8-11GW` | `5-8GW` | `57-122K rack` | `4-9M` | `6-10GW` |
| 2026 务实 | `$335-410B` | `$21-31M/MW` | `12-16GW` | `7-11GW` | `86-178K rack` | `6-13M` | `8-14GW` |
| 2026 乐观 | `$430-530B` | `$20-30M/MW` | `16-22GW` | `10-15GW` | `114-244K rack` | `8-18M` | `12-20GW` |
| 2027 悲观 | `$275-345B` | `$23-30M/MW` | `9-13GW` | `6-9GW` | `64-144K rack` | `5-10M` | `7-12GW` |
| 2027 务实 | `$410-510B` | `$21-30M/MW` | `15-21GW` | `10-15GW` | `107-233K rack` | `8-17M` | `12-19GW` |
| 2027 乐观 | `$600-750B` | `$20-29M/MW` | `22-30GW` | `16-22GW` | `157-333K rack` | `11-24M` | `18-29GW` |

口径说明：

- **深度开工/签约 AI IT load**：已锁定土地/电力/主要设备或已进入土建、机电和设备进场的容量，允许跨年度完工。
- **实际通电 AI IT load**：完成接入、关键机电、commissioning，并具备实质运行条件的容量；这才是 EIA/utility 负荷的近似对应物。
- **rack 等价数**：以 `90-140kW/rack` 为高密度基准。GB300 NVL72 最高约 `142kW/rack`，但全市场还包含 `20-90kW/rack` 的 HGX、推理与定制 ASIC rack，因此不是 NVIDIA 实际出货量 [R19]。
- **GPU/ASIC 等价数**：以每高密度 rack `72` 个加速器的简单上限换算；将 AMD、Trainium、TPU、MTIA、Broadcom 定制 ASIC、旧代 GPU 和 CPU/存储节点折算为“性能/功率等价”，不能解读成 NVIDIA 实物 GPU 订单。

### 4.2 美元与 MW 是否一致

务实情景的 `$335-410B` 对应 `12-16GW` 的深度建设/签约 IT load，隐含 `$21-31M/MW`。这一水平高于普通 colo，但与高密度 AI 设施相容：JLL 给出 2026 全球平均约 `$11.3M/MW`，同时指出 AI 基础设施可接近 `$25M/MW`；本模型额外覆盖加速器、网络、储能/能源接入、复杂液冷和项目预付款 [R14]。

若把 2026 务实 CapEx 全部强行除以同年“已通电” `7-11GW`，会得到高于 `$31M/MW` 的表观成本。这不是计算错误，而是以下三类时点差：

1. GPU、HBM、网络设备可能在园区通电前 `6-18` 个月下单、预付或入库；
2. 变压器、switchgear、燃机、变电站和许可会令“已花的钱”先于“可用 MW”；
3. 2026 年新签 AI Factory 与 build-to-suit 项目的峰值支出，部分对应 2027 的上电和收入。

因此，若 2027 实际通电 AI IT load 显著低于务实区间的 `10-15GW`，但服务器/网络收入仍很高，最可能的解释是建设期错配而非需求立即消失；若低于 `8GW` 且供应商 backlog 同时转弱，则务实情景被证伪。

### 4.3 建设周期与订单确认节奏

| 阶段 | 典型周期 | 最先确认的订单 | 最容易延迟的节点 | 对 2026 / 2027 的含义 |
|---|---:|---|---|---|
| 土地、负荷申请、PPA、utility 方案 | `6-24` 个月 | 土地、工程咨询、部分变压器 slot | interconnection、变电站、州/县许可 | 2026 的申请量主要转化为 2027-2029 的通电容量 |
| 变电站、输电、燃机/BESS | `18-48` 个月 | 变压器、GIS/switchgear、EPC、燃机 reservation | 变压器/燃机交期、环境许可、输电建设 | 最能决定园区是否只是“GPU 订单”而非“可运行 AI Factory” |
| shell、土建、MEP、预制模块 | `12-24` 个月 | EPC/MEP、混凝土、钢材、预制化模块 | 熟练电工、设备到场、变更单 | 2026 开工转为 2027 工程收入的主路径 |
| UPS、busway、CDU、冷水系统 | `9-18` 个月 | Vertiv/Eaton/Schneider/冷却供应商 | 设备认证、现场集成、液冷验收 | 2026 下半年与 2027 是订单和收入都较强的窗口 |
| GPU/ASIC、服务器、网络 | `3-12` 个月 | GPU allocation、ODM/OEM、交换机、光模块 | HBM、封装、客户验收、电力就绪 | 2026 先体现为订单/收入，实际利用率取决于电力与调试 |
| commissioning、客户验收、起租 | `2-6` 个月 | 服务、DCIM、维护、容量租赁 | 并网、可靠性测试、热管理 | 2027 对 REIT/colo、运维和推理收入更关键 |

### 4.4 电力约束不是抽象风险

| 区域/资料 | 公开信号 | 模型含义 |
|---|---|---|
| 德州 / Oncor / ERCOT | Oncor 2026Q1 称其收到约 `271GW` 数据中心负荷请求，并向 ERCOT 2026 RTP 提交 `122GW` 大负荷预测 [R13] | 请求数远高于可快速交付容量；德州是乐观情景上行来源，也是“申请不等于通电”的最大风险 |
| PJM / Virginia | PJM 长期负荷预测已把 data center load 单列；FERC 要求区域电网改革大负荷接入 [R12, R31] | Northern Virginia 仍有生态优势，但边际项目会向中西部、德州和东南部迁移 |
| 全国 | EIA 预计 2026、2027 全美电力负荷增速分别约 `1-3%`，大型算力设施是主要驱动之一 [R11] | 不是单一州的供给问题；输电、变电、燃气、储能和负荷管理同时成为订单池 |
| 需求迁移 | Synergy 指出美国 hyperscale 新增容量更偏向德州和中西部 [R32] | 建筑、PWR/EME、变压器、土地和 local utility 受益不应只盯 Northern Virginia |

## 五、CapEx 结构拆解：悲观/务实/乐观三情景

### 5.1 拆解规则

下列三张主表的前九行是**不重复的客户 CapEx**，加总目标为各情景总规模。带 `*` 的 HBM/DRAM/SRAM、CoWoS/先进封装/半导体设备是**嵌入式价值穿透池**：已包含在 compute、network 或 storage 的采购价中，或是芯片供应链为满足需求而发生的上游再投资；只用于订单映射，绝不能再加到总额。

#### 悲观情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU / AI 服务器 / compute | `$120-150B` | `49-50%` | `$135-166B` | `49-50%` | HBM、融资和电力瓶颈压低 rack 交付；优先保证最强客户 |
| 网络 / 光互联 / 铜互联 | `$16-22B` | `6-7%` | `$18-23B` | `6-7%` | fabric attach 放缓，800G 为主，1.6T 仅少量项目 |
| 电力 / UPS / 配电 | `$20-25B` | `8-8%` | `$22-27B` | `8-8%` | switchgear/变压器 lead time 限制项目进场 |
| 能源与微电网 | `$6-9B` | `2-3%` | `$7-11B` | `2-3%` | 燃机 slot 与并网许可无法快速放量 |
| 建筑 / 土建 / MEP | `$28-35B` | `11-12%` | `$31-40B` | `11-12%` | 已开工项目继续，但新园区开工下降 |
| 冷却 / 液冷 / HVAC | `$11-14B` | `4-5%` | `$12-17B` | `4-5%` | 液冷渗透率提高，但安装/验收限制放量 |
| SSD / HDD / 存储系统 | `$6-8B` | `2-3%` | `$6-9B` | `2-3%` | 推理、RAG 与 checkpoint 扩容延后 |
| DCIM / 能控 / 安全 / 服务 | `$3-4B` | `1-2%` | `$4-5B` | `1-2%` | 以关键运维和合规配置为主 |
| 场地、设计、集成、备件、预付款及其他 | `$35-39B` | `13-14%` | `$40-47B` | `14-15%` | 反映大项目的设计/集成/跨年交付成本与不确定性 |
| *HBM / DRAM / SRAM（穿透，不相加） | `$19-30B` | `已含在 compute/存储` | `$24-38B` | `已含在 compute/存储` | HBM4 良率与供给仍是硬瓶颈 |
| *先进封装 / 半导体设备 / 测试（穿透，不相加） | `$8-13B` | `已含在 compute` | `$10-17B` | `已含在 compute` | CoWoS、基板、测试扩产慢，设备收入滞后 |

#### 务实情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU / AI 服务器 / compute | `$165-195B` | `47-49%` | `$205-235B` | `46-50%` | Blackwell/GB300 放量，Rubin 与定制 ASIC 开始备货 |
| 网络 / 光互联 / 铜互联 | `$23-28B` | `6-7%` | `$29-35B` | `7-7%` | 800G 主流、1.6T 进入新增 AI fabric |
| 电力 / UPS / 配电 | `$28-34B` | `8-8%` | `$35-44B` | `8-9%` | 设备价格和 backlog 保持强势，局部供给改善 |
| 能源与微电网 | `$9-14B` | `3-3%` | `$13-20B` | `3-4%` | 自备电、BESS、PPA 解决部分 speed-to-power 问题 |
| 建筑 / 土建 / MEP | `$38-48B` | `11-12%` | `$47-58B` | `11-11%` | 2025-2026 开工项目持续转化，预制化提高交付速度 |
| 冷却 / 液冷 / HVAC | `$15-22B` | `4-5%` | `$20-27B` | `5-5%` | rack density 推动 direct-to-chip、CDU、冷水系统升级 |
| SSD / HDD / 存储系统 | `$8-12B` | `2-3%` | `$10-15B` | `2-3%` | 训练与推理并行拉动 NVMe、对象存储与 checkpoint |
| DCIM / 能控 / 安全 / 服务 | `$4-6B` | `1-2%` | `$5-7B` | `1-2%` | 多 MW 园区把 BMS/DCIM/数字孪生变成标配 |
| 场地、设计、集成、备件、预付款及其他 | `$45-51B` | `12-13%` | `$46-69B` | `11-14%` | 集成、长交期预付款和跨年度项目占比高 |
| *HBM / DRAM / SRAM（穿透，不相加） | `$28-44B` | `已含在 compute/存储` | `$38-60B` | `已含在 compute/存储` | HBM 供给逐季改善，HBM4 进入高量产 |
| *先进封装 / 半导体设备 / 测试（穿透，不相加） | `$12-21B` | `已含在 compute` | `$17-30B` | `已含在 compute` | 先进封装扩产继续，测试与设备收入滞后 `2-6` 季度 |

#### 乐观情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU / AI 服务器 / compute | `$215-250B` | `50-47%` | `$300-355B` | `50-47%` | GPU/ASIC 供给超预期，rack-scale 交付和验收速度提升 |
| 网络 / 光互联 / 铜互联 | `$30-37B` | `7-7%` | `$42-54B` | `7-7%` | 1.6T、CPO/LPO、高阶 AEC/DAC 加速进入规模项目 |
| 电力 / UPS / 配电 | `$36-44B` | `8-8%` | `$51-63B` | `9-8%` | 高密度供电与配电改造以项目包形式采购 |
| 能源与微电网 | `$14-22B` | `3-4%` | `$28-42B` | `5-6%` | 微电网、燃机、BESS、专用变电站被前置部署 |
| 建筑 / 土建 / MEP | `$50-60B` | `12-11%` | `$68-84B` | `11-11%` | 多 GW 园区批量开工，预制模块拉动施工效率 |
| 冷却 / 液冷 / HVAC | `$21-29B` | `5-5%` | `$30-42B` | `5-6%` | 液冷从选配变为高密度 rack 的基线配置 |
| SSD / HDD / 存储系统 | `$10-16B` | `2-3%` | `$15-23B` | `3-3%` | 推理缓存、多模态数据、长上下文和日志爆发 |
| DCIM / 能控 / 安全 / 服务 | `$5-7B` | `1-1%` | `$8-12B` | `1-2%` | AI Factory 的运维复杂度和能耗优化价值上升 |
| 场地、设计、集成、备件、预付款及其他 | `$49-65B` | `11-12%` | `$58-75B` | `10-10%` | 项目融资、定制设计、备件与集成服务扩大 |
| *HBM / DRAM / SRAM（穿透，不相加） | `$37-58B` | `已含在 compute/存储` | `$58-88B` | `已含在 compute/存储` | HBM4/HBM4E 过渡顺利且 ASP 高位 |
| *先进封装 / 半导体设备 / 测试（穿透，不相加） | `$17-30B` | `已含在 compute` | `$28-45B` | `已含在 compute` | CoWoS、SoIC、测试与设备订单出现滞后放大 |

### 5.2 为什么 HBM、封装与半导体设备不计入 CapEx 总和

| 项目 | 在客户 CapEx 表中的位置 | 在产业链订单池中的位置 | 正确的分析动作 |
|---|---|---|---|
| HBM / DRAM / SRAM | 主要嵌入 GPU/ASIC、服务器和部分存储价格 | 直接收入/订单受益者为 Micron、SK hynix、Samsung、IP/接口厂商 | 用每 GPU 的 HBM attach、容量/ASP、供给协议来测算；不再加回整机 CapEx |
| CoWoS / advanced packaging | 嵌入 GPU/ASIC ASP 与交付周期 | TSMC、ASE、Amkor、测试与材料/设备公司获得订单 | 用 wafer/package capacity、substrate、测试时长与设备 lead time 追踪 |
| 半导体设备 | 不由数据中心客户直接购买 | 属于供应链为扩产 HBM/逻辑/封装而发生的后续 WFE/测试投资 | 单列为 `2-6` 季度滞后的穿透订单，不能与服务器订单相加 |
| SSD / HDD | 是客户直接 CapEx 中独立的存储模块 | NAND、HDD、存储系统厂商确认收入 | 与 compute 分列，但需防止将服务器自带 boot/cache SSD 计两次 |

Micron 已披露 HBM4 对领先客户平台高量产发货、HBM4E 目标在 2027 年量产；TSMC 则持续扩大 CoWoS 并在其路线中提高单封装可集成 HBM 堆叠数 [R17-R18]。这支持穿透池在 2027 的增速高于直接客户 CapEx，但不支持把它们第二次加总。

## 六、产业链订单映射

### 6.0 订单池的读法与可加总边界

本节默认使用**务实情景、美国需求归属、当年可签/可确认订单机会**。同一张表内的子项可近似相加；不同表之间通常不可相加。例如：AI 整机订单已含 GPU，GPU/ASIC 表又把同一价值穿透到 NVIDIA/AMD/Broadcom/TSMC/Micron；因此两张表用于比较“谁拿价值”，不用于制造一个更大的市场总数。

`2026-2027 CAGR` 均按区间中点的近似年增长率表示，数字用于方向与敏感性，不代表公司收入指引。所有公司列为产业链映射，**不是买卖建议**。

### 6.1 电力与能源

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | 主要公司 | 瓶颈 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| 变压器 / switchgear / 中压配电 | `$15-23B` | `$21-32B` | `+35-42%` | Eaton、Schneider、GE Vernova、Hubbell、Powell、Siemens、Hitachi Energy | 产能、铜/钢、认证、utility 规格、现场安装 | backlog、lead time、book-to-bill、变电站投产、utility CAPEX |
| UPS / dynamic UPS / BESS / 飞轮 | `$10-15B` | `$14-22B` | `+38-47%` | Vertiv、Eaton、Schneider、Tesla Energy、Fluence、CATL 相关供应链 | 电芯、功率模块、消防规范、与微电网调度的集成 | 数据中心订单、UPS MW、BESS MWh、项目并网/验收 |
| busway / PDU / rack PDU / 保护器件 | `$6-9B` | `$8-12B` | `+30-36%` | Vertiv、Eaton、Schneider、Starline、nVent、Hubbell | 高密度铜排、客户认证、机房设计变更 | 每 MW BOM、rack power shelf、工厂产能、招标结果 |
| 微电网 / 自备燃机 / 燃料电池 / 临时电源 | `$12-20B` | `$18-30B` | `+39-47%` | GE Vernova、Caterpillar、Cummins、Bloom、Wärtsilä、utilities、IPP | 燃机 slot、燃气接入、排放许可、并网与容量市场 | PPA、发电机订单、燃机 reservation、州审批、COD |
| 输配电接入 / 专用变电站 / utility EPC | `$18-30B` | `$25-40B` | `+30-38%` | Quanta、Mastec、MYR、EMCOR、utility 设备商 | 输电走廊、并网研究、熟练电工、变电站土地 | interconnection agreement、RTP/IRP、变电站开工、EPC backlog |

2026Q1 的公司信号已使这张表具有可验证性，而不是纯宏观推演：Vertiv 2025Q4 backlog 达 `$15.0B`、book-to-bill 约 `2.9x`；Eaton 电气美洲滚动订单增长受数据中心驱动；GE Vernova 2026Q1 电气化业务拿到 `$2.4B` 数据中心设备订单，超过其上一年全年相关订单 [R16, R23-R25]。这些公司并不全是“AI 纯标的”，但其订单证明了电力层已经是 CapEx 的必要支出。

### 6.2 AI 服务器与机架

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | 主要公司 | 毛利 / 价值捕获 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| AI 整机（GPU/ASIC server） | `$165-195B` | `$205-235B` | `+22-26%` | Dell、SMCI、HPE、Quanta、Wiwynn、Celestica、Inventec | GPU/ASIC 与软件平台拿高价值；OEM/ODM 更多是供应链/集成利润 | AI orders、backlog、GPU allocation、shipment、客户集中度 |
| rack-scale system（GB/VR NVL、同类 ASIC rack） | `$65-95B` | `$90-135B` | `+38-45%` | NVIDIA、AMD、Broadcom、Quanta、Wiwynn、Foxconn、Dell、SMCI | NVLink/scale-up、液冷、供电与系统验证形成高门槛；**已含在 AI 整机，不能相加** | NVL rack 出货、rack acceptance、液冷 attach、机架功率 |
| 机柜级电源、power shelf、集成与部署 | `$15-23B` | `$22-33B` | `+40-45%` | Vertiv、Eaton、Delta、Lite-On、Celestica、Flex | 高密度直流供电、母排、现场验收的溢价；与电力表有交叉 | `kW/rack`、power shelf 规格、交付周期、现场调试 |
| 管理节点、控制面、存储/网络节点 | `$10-18B` | `$15-25B` | `+38-43%` | Dell、HPE、SMCI、Cisco、NVIDIA、Pure、WDC、Seagate | 单位价值低于加速器，但对可用集群不可缺 | cluster BOM、节点数/GPU、客户部署公告 |

Dell FY2026 已披露全年 AI 优化服务器订单超过 `$64B`、出货超过 `$25B`，FY2027Q1 又披露 AI 订单 `$24.4B`、AI server revenue `$16.1B`、backlog `$51.3B` [R22]。该证据支持“整机订单池大”，但也提醒投资者：OEM 增长并不等同于其获得 GPU/软件层的高毛利。

### 6.3 网络、光互联与铜互联

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | attach 假设 | 主要公司 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| 800G / 1.6T 光模块、LPO / silicon photonics | `$8-13B` | `$12-20B` | `+45-50%` | 每 GPU 的 scale-out 端口和多层交换网络提升；1.6T 从新增集群开始渗透 | Coherent、Lumentum、Innolight、Eoptolink、Fabrinet、Marvell、Broadcom | 出货、ASP、客户认证、DSP/laser 供给、1.6T mix |
| AI fabric 交换机、NIC、DPU、IB / Ethernet | `$13-21B` | `$20-32B` | `+45-52%` | 训练集群需要 scale-up + scale-out；ASIC/以太网并行扩张 | NVIDIA、Arista、Broadcom、Cisco、Marvell、AMD Pensando | switch silicon、system order、port shipment、客户设计赢单 |
| DAC / AEC / 背板 / 连接器 / 高速铜互联 | `$3-5B` | `$5-9B` | `+50-60%` | rack 内短距优先铜互联；功耗/距离决定 AEC 与光的分界 | Credo、Astera、Amphenol、TE、Molex、NVIDIA、Marvell | NVL rack BOM、线缆订单、每 rack 米数、热/功耗指标 |
| 园区/跨园区 DCI（800G ZR / ZR+、1.6T） | `$2-4B` | `$3-6B` | `+40-50%` | AI 训练跨楼、跨园区和多站点扩张 | Ciena、Coherent、Lumentum、Nokia、Cisco | DCI port、ZR/ZR+ 出货、跨园区带宽合同 |

Arista 已发布面向 rack-scale AI 的 1.6T 产品，Broadcom 已量产 102.4T Tomahawk 6 并推动 800G NIC，LightCounting 亦上调 800G/1.6T 预测 [R21, R26, R33]。因此，网络不是“GPU 支出的固定小比例”：在乐观场景中，GPU 数量、拓扑层级、跨园区训练和 1.6T ASP 可以同时上调，使网络订单弹性高于总 CapEx。

### 6.4 半导体上游拉动（美国需求归属的穿透订单池）

| 子环节 | 2026 订单规模 | 2027 订单规模 | 订单确认节奏 | 主要公司 | 主要瓶颈 | 验证指标 |
|---|---:|---:|---|---|---|---|
| GPU / ASIC | `$125-175B` | `$160-230B` | allocation、预付款、系统交付；通常早于园区通电 | NVIDIA、AMD、Broadcom、Google TPU、AWS Trainium、Meta MTIA、Marvell | GPU die、HBM、CoWoS、板卡与整机集成 | data center revenue、客户承诺、server backlog、定制 ASIC tape-out |
| HBM / DRAM / SRAM | `$28-44B` | `$38-60B` | bit shipment、ASP、长期供货协议，随平台切换跳升 | SK hynix、Micron、Samsung、Rambus、Synopsys/接口 IP | HBM stack 良率、DRAM die、封装、测试 | HBM bit growth、ASP、产能、客户认证、资本开支 |
| CoWoS / advanced packaging / substrate | `$12-21B` | `$17-30B` | package capacity 和订单通常早于最终 GPU 完整出货 | TSMC、ASE、Amkor、Ibiden、Unimicron、Shinko | CoWoS 产能、基板、interposer、测试 | 月产能、substrate lead time、OSAT utilization、tool order |
| 半导体设备 / 测试 | `$8-14B` | `$12-22B` | 滞后 `2-6` 季度；设备订单先于产线有效产能 | AMAT、LRCX、KLAC、ASML、Advantest、Teradyne、BESI、ASMPT | 客户 CapEx、工具交期、安装/认证 | backlog、WFE、tester utilization、厂房开出时间 |
| 先进电源半导体与高速连接芯片 | `$6-10B` | `$9-15B` | 随 rack power、NIC、retimer、AEC 提前进入 BOM | Infineon、onsemi、Monolithic Power、Navitas、Credo、Astera | 功率密度、认证、散热、供给连续性 | power shelf、retimer/AEC 出货、GaN/SiC 设计导入 |

NVIDIA FY2027Q1 数据中心 compute 与 networking 合计为 `$75.2B`，AMD 2026Q1 数据中心收入 `$5.8B` 且 Meta/AMD 约定最多 `6GW` 的部署，Broadcom 2026Q2 AI 半导体收入 `$10.8B` [R20, R27, R34]。这三组一手证据足以说明 GPU/ASIC 订单池是全链条最大价值池；但其“美国需求归属”并不意味着制造地点在美国。

### 6.5 建筑、工程、REIT 与开发商

| 子环节 | 2026 订单规模 | 2027 订单规模 | CAGR | 主要公司 | 价值捕获 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| EPC / MEP / 电气总包 | `$35-48B` | `$45-65B` | `+30-35%` | EMCOR、Quanta、Mastec、Fluor、Jacobs、AECOM、MYR、Rosendin | backlog 转收入、可用电工/技师、设计-施工协同 | bookings、RPO/backlog、毛利率、项目工时、变更单 |
| 预制化模块、skid、白空间、集装箱式机房 | `$8-13B` | `$11-18B` | `+35-42%` | Vertiv、Schneider、Eaton、HITEC、Modular Power、工程承包商 | 交付速度、标准化设计、工厂产能 | MW delivery、factory capacity、客户验收时间 |
| REIT / colo / developer 的建设合同 | `$20-35B` | `$30-50B` | `+45-50%` | Digital Realty、Equinix、Applied Digital、CoreWeave、CyrusOne、Vantage、QTS | 预租、power bank、融资、长租现金流 | leased MW、pre-lease、development pipeline、融资成本 |
| utility / 输电接入工程 | `$18-30B` | `$25-40B` | `+30-38%` | Quanta、Mastec、utilities、变电设备厂商 | 监管回报、工程/设备可得性、节点稀缺 | IRP/RTP、输电立项、interconnection agreement、COD |

工程和开发商必须分开看：EMCOR 2026Q1 RPO 为 `$15.62B`、公司称 data center/network & communications 活动强劲 [R35]；Digital Realty 的租金 backlog/开发容量则更接近未来起租与资产价值 [R07]。前者可先确认工程收入，后者常在通电、验收、起租后确认收入，不能用同一个“订单增长率”处理。

### 6.6 冷却、存储、DCIM 和其他必要环节

| 环节 | 2026 订单规模 | 2027 订单规模 | CAGR | 为什么必须看 | 主要公司 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| 液冷 / CDU / 冷板 / 泵阀 | `$15-22B` | `$20-30B` | `+32-38%` | 高密度 rack 的直接前置条件，GB300/后续平台推动从试点走向标准化 | Vertiv、Schneider、Modine、nVent、CoolIT、Asetek | 液冷 attach、CDU MW、rack acceptance、现场故障率 |
| 冷水机组 / HVAC / heat rejection | `$6-10B` | `$9-14B` | `+40-45%` | 即便 IT 侧液冷，facility heat rejection 仍需要规模化冷却 | JCI、Carrier、Trane、Vertiv、Modine | 每 MW 成本、chiller lead time、PUE/WUE、交付周期 |
| 冷却液 / 水处理 / 过滤 / 服务 | `$1-3B` | `$2-4B` | `+45-55%` | 液冷规模化后的耗材、认证、运维和可靠性需求 | Ecolab、Kurita、Parker、Donaldson、服务商 | coolant attach、维护合同、认证、耗材复购 |
| SSD / HDD / 存储系统 | `$8-12B` | `$10-15B` | `+25-30%` | 训练 checkpoint、RAG、多模态数据、推理 cache 同时增加需求 | Micron、Samsung、Kioxia、WDC、Seagate、Pure、NetApp | enterprise SSD/HDD ASP、exabyte shipment、对象存储部署 |
| DCIM / BMS / energy control / digital twin | `$4-6B` | `$5-8B` | `+25-35%` | 多 GW 园区需要对电力、冷却、负荷和故障进行统一调度 | Schneider、Vertiv、JCI、Honeywell、Siemens | 软件 attach、服务收入、PUE 改善、项目验收 |
| 消防、物理安防、线缆管理、弱电 | `$3-5B` | `$4-7B` | `+30-40%` | 高密度机房不可省略，但常被 GPU 叙事掩盖 | Honeywell、JCI、nVent、Legrand、Hubbell | 每 MW BOM、项目交付、法规与保险要求 |

冷却有两层价值：一层是 GPU/rack 侧的 direct-to-chip 液冷，另一层是园区侧的热排放、冷水、泵和水处理。将二者混为“液冷市场”会低估 HVAC/热管理，也会重复计算。Vertiv 已因 AI 高密度需求扩充美国液冷和 chilled-water 产能，且把 power/cooling 预制化作为缩短部署时间的产品方向 [R23, R24]。

## 七、三情景敏感性分析：订单变化百分比和美元变化

### 7.1 情景变量

| 变量 | 悲观 | 务实 | 乐观 |
|---|---|---|---|
| GPU / ASIC 供给 | HBM/封装 allocation 集中，系统交付延后 | Blackwell/GB300 逐步放量，Rubin 准备期开始 | GPU、定制 ASIC 与 rack-scale 同时超预期 |
| HBM 供给 | HBM3E/HBM4 良率、堆叠和封装不足 | 产能逐季改善，价格仍高 | HBM4 过渡顺利，HBM4E 准备提前 |
| 存储供给 | SSD/HDD 价格或供给冲击压制扩容 | 价格走高但供给可跟上 | 推理/多模态需求使容量与 ASP 同时提高 |
| CoWoS / 封装 | CoWoS、基板、测试为硬瓶颈 | 扩产兑现但保持紧平衡 | 产能与良率快于预期，更多系统可在 2027 出货 |
| 电力供给 | 接入、变压器、燃机和许可明显约束 | 局部瓶颈，自备电/迁址缓解 | 专用电力方案和微电网使多 GW 园区批量开工 |
| 融资环境 | NeoCloud 融资收紧，项目落地率下降 | 大客户、预租和高质量项目继续融资 | 债务、lease、客户预付款和基础设施资本共同加速 |
| AI 需求兑现 | utilization 与推理收入低于预期 | 训练、推理稳定增长 | agent、多模态、企业 AI 与模型竞赛爆发 |
| CapEx 增速 | `10-15%` | `20-30%` | `40%+` |

### 7.2 相对务实情景的订单池变化（以 2027 为主）

| 产业链 | 务实 2027 订单池 | 悲观 vs 务实 | 悲观美元变化 | 乐观 vs 务实 | 乐观美元变化 | 主要敏感变量 |
|---|---:|---:|---:|---:|---:|---|
| 电力与能源 | `$90-136B` | `-15% to -28%` | `-$17-34B` | `+20% to +40%` | `+$23-45B` | 电力接入、变压器、燃机、微电网 |
| AI 服务器与机架 | `$205-235B` | `-20% to -35%` | `-$44-77B` | `+30% to +55%` | `+$66-121B` | GPU/HBM/rack-scale 交付、融资、客户利用率 |
| 网络与光互联 | `$37-61B` | `-20% to -35%` | `-$8-21B` | `+35% to +65%` | `+$17-40B` | 1.6T、集群拓扑、GPU 数量、光/铜取舍 |
| 半导体上游（穿透，不相加） | `$227-342B` | `-20% to -35%` | `-$49-112B` | `+30% to +55%` | `+$68-188B` | GPU、HBM、CoWoS、设备/测试滞后 |
| 建筑与工程 | `$70-105B` | `-15% to -30%` | `-$13-32B` | `+25% to +45%` | `+$22-47B` | 开工、MEP 劳力、电力审批、预制化 |
| 冷却 | `$20-30B` | `-18% to -30%` | `-$5-9B` | `+35% to +60%` | `+$9-18B` | rack density、液冷渗透、验收与可靠性 |
| 存储 | `$10-15B` | `-15% to -25%` | `-$2-4B` | `+35% to +60%` | `+$4-9B` | 推理数据、RAG、SSD/HDD ASP |

> “半导体上游”行与“AI 服务器与机架”行有嵌套，故其美元变化不能与其他行相加；其用途是显示同一 CapEx 在不同利润池的放大/滞后路径。

### 7.3 五个高杠杆敏感性

| 变量变化 | 对总 CapEx 的一阶影响 | 首先受益 | 最晚受益 | 反方向受损 |
|---|---|---|---|---|
| GPU/ASIC 供给较务实多/少 `10%` | 2027 总 CapEx 大致变化 `+/-$25-45B` | GPU/ASIC、整机、NIC/交换机 | 工程、设备、REIT 起租 | OEM/ODM、光模块与冷却的订单延后 |
| HBM 可用 bit 较务实多/少 `10%` | 主要影响 compute 转化，不是单纯降价；总量约 `+/-$15-30B` | HBM、封装、GPU、服务器 | 电力与工程 | GPU/rack 出货受限或备货推迟 |
| 可通电 IT load 较务实多/少 `3GW` | 约对应 `+/-$60-90B` 的跨年建设/订单机会 | 变压器、switchgear、EPC、冷却、REIT | GPU 利用率/云收入 | 已采购服务器可能延迟验收 |
| NeoCloud 融资成本变化 `+/-200bp` | 影响 AI Factory 的开工率，约 `+/-$10-25B` | 高质量开发商、预租资产 | 整机供应链 | 高杠杆 NeoCloud、缺乏预租的项目 |
| 推理 token 需求高/低于预期 `25%` | 2027 对存储、网络、功率效率的影响大于对训练 GPU 的边际影响 | 存储、网络、ASIC、DCIM、液冷 | 新训练园区 | 单一依赖前沿训练的项目 |

## 八、公司受益映射：核心受益、间接受益、伪受益

### 8.1 受益层级

| 产业层 | 核心受益（收入直接映射） | 间接受益（取决于项目落地） | 需降权的“伪受益” | 投资者应验证 |
|---|---|---|---|---|
| GPU / ASIC / 系统 | NVIDIA、AMD、Broadcom、Dell、SMCI、HPE、Quanta、Wiwynn、Celestica | Marvell、Astera、Credo、板卡/电源供应商 | 只有“AI server”标签、没有 GPU allocation/客户 backlog 的低端组装商 | AI orders、backlog、客户集中度、GPU/ASIC 可得性 |
| 网络 / 光互联 | Arista、NVIDIA、Broadcom、Coherent、Lumentum、Credo、Amphenol | Cisco、Ciena、Fabrinet、TE | 单靠传统企业网交换机、无 AI fabric/1.6T 客户认证 | 端口出货、1.6T mix、客户设计赢单、ASP |
| 电力与能源 | Eaton、Vertiv、Schneider、GE Vernova、Powell、Hubbell、Quanta | BESS、燃料电池、IPPs、utility | 没有 interconnection/PPA/设备订单支撑的“电力概念股” | backlog、lead time、燃机 slot、PPA、utility 政策 |
| 冷却 / 热管理 | Vertiv、Schneider、Modine、nVent、JCI、Carrier、Trane | 泵阀、水处理、冷却液、服务商 | 传统 HVAC 厂商若无液冷/CDU/高密度项目，不应按 AI 高增速外推 | liquid cooling attach、CDU MW、field acceptance、服务合同 |
| HBM / 封装 / 测试 | Micron、SK hynix、Samsung、TSMC、ASE、Amkor、Advantest、Teradyne | 基板、材料、WFE 设备 | 将“美国项目”误读成“美国制造”；或把设备订单提前计入当期收入 | HBM bit/ASP、CoWoS capacity、tester utilization、设备 backlog |
| 工程 / 开发 / REIT | EMCOR、Quanta、Mastec、DLR、EQIX、APLD、Vantage、CyrusOne | Fluor、Jacobs、AECOM、土地/光纤供应商 | 只有土地储备但没有 power bank、预租/融资或许可的开发商 | leased MW、pre-lease、COD、融资成本、RPO 转化 |
| 存储 / 控制 | WDC、Seagate、Micron、Samsung、Pure、NetApp、Schneider、Honeywell | DCIM 软件、物理安防、线缆管理 | 将传统 HDD/普通安全设备按 GPU 增速外推 | exabyte shipment、SSD/HDD mix、服务 attach、每 MW BOM |

### 8.2 价值捕获而非“相关性”

| 类型 | 判断标准 | 2026-2027 代表环节 | 为什么 |
|---|---|---|---|
| 核心受益 | 客户 CapEx 直接形成订单，且供给/认证/设计赢单限制竞争 | GPU/ASIC、HBM、CoWoS、交换机芯片、变压器/switchgear、液冷集成 | 高价值、长交期、客户认证或技术门槛使价格/毛利更可守 |
| 间接受益 | 有明确项目后才确认订单，受开工/通电影响大 | EPC、预制化、REIT/colo、燃机/BESS、存储系统 | 订单能见度高但收入确认晚，且有融资/许可风险 |
| 伪受益 | 与 AI 名词相关但没有直接 BOM、项目、合同或稀缺资源 | 泛数据中心地产、无差异 HVAC、无客户的电源概念、泛光通信 | 主题能提升估值，无法保证订单/毛利；应优先要求 company-specific evidence |

## 九、投资视角总结：α、β、bottleneck 和 2026/2027 订单拐点

### 9.1 α 与 β 分层

| 分层 | 定义 | 结论 | 务实至乐观的美元上行 |
|---|---|---|---:|
| 订单弹性最大（beta） | 总 CapEx 上修时订单非线性增加 | rack-scale 系统、1.6T 光/交换、液冷、微电网/燃机、先进封装测试 | 服务器/rack `$66-121B`、网络 `$17-40B`、冷却 `$9-18B`、电力 `$23-45B` |
| 确定性最高（alpha） | 即使悲观情景仍必须采购，且受 backlog/预付款支持 | switchgear、UPS、busway、变压器、MEP、液冷基础设施、DCIM/验收服务 | 需求从“推迟”而非“消失”，主要是跨年转移 |
| 高利润池 | 技术/认证/供给约束使议价强于工程量 | GPU/ASIC、HBM、CoWoS、网络 ASIC/光 DSP、高密度供电与液冷集成 | 半导体穿透池的利润增速可高于客户 CapEx，但不可与其相加 |
| 防守型收益 | CapEx 周期中仍能靠服务、租金、维护稳住 | 数据中心服务、UPS/冷却服务、DCIM、已起租且电力有保障的资产 | 低于 GPU 弹性，但对交付延迟更耐受 |

### 9.2 Bottleneck 清单

| 瓶颈 | 2026 状态 | 2027 状态 | 受益环节 | 被压制环节 | 反证指标 |
|---|---|---|---|---|---|
| 电力接入 | 明显，尤其 PJM、Virginia、Texas 的真实通电能力 | 局部缓解，但大园区仍明显 | utilities、输配电、变压器、微电网、EPC | 开发商、服务器交付、REIT 起租 | interconnection agreement、PPA、变电站 COD、FERC/州改革 |
| 变压器 / switchgear | 明显，已转化为 backlog 和价格 | 局部缓解，仍是长交期设备 | Eaton、Schneider、GEV、Powell、Hubbell | 项目开工、机电进场 | lead time、book-to-bill、工厂扩产、招标中标 |
| HBM | 明显，高价紧平衡 | 从绝对短缺向高价/结构性紧平衡过渡 | Micron、SK hynix、Samsung、封装 | GPU/rack 出货 | bit shipment、ASP、yield、长期协议 |
| CoWoS / advanced packaging | 明显，尤其大尺寸/高 HBM stack | 局部缓解但规格升级带来新瓶颈 | TSMC、OSAT、测试、设备 | GPU/ASIC 供给 | capacity、substrate、tester utilization、tool delivery |
| 液冷集成 | 局部，工程设计与现场验收仍是短板 | 继续局部，标准化后缓解 | CDU、冷板、泵阀、热管理、预制化 | 高密度 rack 部署 | rack acceptance、field failure、CDU MW、交付时间 |
| 工程劳动力 / MEP | 明显，尤其大园区与新区域 | 局部，预制化有所改善 | EMCOR、Quanta、Mastec、预制化厂商 | 园区投产、REIT 起租 | backlog conversion、工时、工资、毛利、项目延误 |

### 9.3 2026 与 2027 的订单拐点

| 年份 | 可能出现的订单拐点 | 最直接受益环节 | 跟踪指标 |
|---|---|---|---|
| 2026 | Blackwell/GB300 rack 放量；800G 向 1.6T 的设计导入；变压器/switchgear 继续紧张；液冷从试点走向大规模部署 | compute、网络、电力、液冷 | GPU/rack 出货、AI server backlog、光模块订单、lead time、CDU MW |
| 2027 | Rubin/下一代 ASIC 的准备或放量；HBM4 规模化、HBM4E 准备；微电网/自备电扩大；AI Factory 从开工转为服务收入；推理存储增强 | 半导体、能源、存储、工程、REIT/colo | CapEx guide、PPA、燃机/变电站 COD、CoWoS/HBM capacity、leased MW、AI 云收入 |

2026 的关键不在于“有没有宣布项目”，而在于**Blackwell/GB300 是否完成从 GPU 交付到有电、有冷却、可验收的 rack-scale 部署**；2027 的关键不在于“新一代芯片是否发布”，而在于**Rubin/ASIC、HBM4、能源和 AI Factory 这四条链能否同时到位**。任何一条失速，订单会从 2027 滚动到 2028，而非平均地消失。

## 十、反证条件、风险和后续跟踪清单

### 10.1 能使务实情景失效的反证条件

| 反证条件 | 触发阈值 / 现象 | 对模型的影响 | 优先下调的订单池 | 需要区分的替代解释 |
|---|---|---|---|---|
| 五大云厂商削减建设投入 | 任何两家把 2026/2027 CapEx 指引合计下调 `15%+`，且理由是需求/利用率而非交付时点 | 务实总量从 `$335-410B` 向悲观区间靠拢 | GPU/ASIC、整机、网络 | 单季 finance lease 或组件价格造成的会计波动，不应误判为需求断崖 |
| AI 云供需不再紧张 | Azure/AWS/GCP 明确表示 AI 容量不再受限，同时 RPO/AI 收入增速下行 | AI/DC 占比、建设转化率同时下降 | compute、网络、冷却 | 由效率提升释放供给而需求仍增长，可能只压制新增设备速度 |
| 通电容量断层 | 2026 实际通电 AI IT load 低于 `5GW`，且 2027 已签变电站/PPA 无法弥补 | CapEx 与 MW 的交叉验证失败 | EPC、配电、REIT/colo、服务器验收 | 客户提前预付服务器、建设从 2026 延至 2027 的时点差 |
| HBM / CoWoS 延迟 | HBM4 良率、CoWoS/基板/测试问题导致高端 GPU/ASIC 出货连续两季低于客户计划 | 整机金额和 rack-scale 部署率下降 | GPU/ASIC、HBM、封装、服务器、网络 | GPU 供给改善但电力限制更强，应单独归因 |
| NeoCloud 融资收紧 | 高杠杆 NeoCloud 融资失败、预租取消、客户集中度恶化 | 乐观尾部最先被删除 | AI Factory、REIT/开发商、ODM | 大客户改为自建/转租，可能只是订单归属迁移 |
| 电力/社会许可逆转 | 州监管提高大负荷收费或建设许可持续撤销，PPA/变电站 COD 批量后延 | `2027` 比 `2026` 受损更大 | utility EPC、微电网、园区开发 | 更严格规则若让客户承担成本，可能反而提高电力设备订单价值 |
| 组件价格冲击 | HBM/DRAM/光器件价格急升但可用量下降 | 名义 CapEx 上升、真实 MW/算力下降 | 服务器交付、MW、终端云毛利 | 不能把价格通胀误读为真实建设规模扩大 |

### 10.2 更新模型的最小数据面板

| 频率 | 应更新的指标 | 一手来源优先级 | 触发的模型变量 | 红旗 |
|---|---|---|---|---|
| 每季 | Microsoft、Alphabet、Meta、Amazon、Oracle CapEx 与 AI/DC 描述 | 公司 earnings release / transcript | AI/DC 占比、美国占比、建设转化率 | 总额下调、短寿命资产比重下降、供给不再紧张 |
| 每季 | NVIDIA、AMD、Broadcom、Dell、SMCI 的数据中心订单、收入、backlog | 公司 IR / 10-Q / earnings | GPU/ASIC、服务器、网络订单池 | backlog 连续下降、客户集中度升高、供给/验收问题 |
| 每季 | Vertiv、Eaton、GEV、EMCOR、Quanta 的 backlog、book-to-bill、lead time | 公司 IR | 电力、冷却、EPC 订单池 | book-to-bill `<1.0x`、工程毛利受劳力/变更单挤压 |
| 每季 / 月度 | utility queue、RTP/IRP、PPA、变电站及燃机 COD | FERC、PJM/ERCOT、utility、州 PUC | 可通电 MW、能源与微电网 | 请求 MW 上升而签约/上电 MW 停滞 |
| 每季 | HBM bit/ASP、CoWoS、OSAT/测试设备动态 | Micron、TSMC、OSAT、设备商 | GPU/ASIC 供给、上游穿透池 | HBM4/CoWoS 延期、test utilization 下行 |
| 半年 | CBRE/JLL/Synergy 的在建 MW、预租、租金、空置率 | 行业资料交叉验证 | 美国建设规模、colo/REIT 净增量 | 在建 MW/预租同步下行、空置率抬升 |

### 10.3 下次更新时应先改哪些参数

1. 先更新五大云厂商的 `CapEx` 和 AI/DC 占比，不先改行业 TAM。
2. 再更新美国可通电 MW：PPA、interconnection、变电站、燃机/BESS COD，而不是只看申请队列。
3. 使用 GPU/ASIC、HBM、CoWoS 与 rack shipment 校验服务器 CapEx；如果三者不一致，优先检查预付款/库存/跨季交付。
4. 用 Vertiv/Eaton/GEV/EMCOR/Quanta 的 backlog 与 book-to-bill 复核电力、冷却与工程订单。
5. 最后才调整 NeoCloud/AI Factory 的融资与开发商净增量；这是乐观情景中波动最大、证据等级最低的一层。

### 10.4 结论的风险权重

| 结论 | 结论等级 | 为什么 | 不能据此做出的推论 |
|---|---|---|---|
| 2026 美国 AI 数据中心建设处于高景气扩张 | 高 | 多家 hyperscaler CapEx、GPU/ASIC、物理基础设施供应商订单一致 | 不代表所有相关股票都将受益或估值合理 |
| 电力、switchgear、变压器与 MEP 是核心瓶颈 | 高 | FERC、utility、Eaton、GEV、Vertiv、工程商的证据相互印证 | 不代表每个电力概念公司都有直接订单 |
| 2027 比 2026 更利好微电网、HBM4、Rubin/ASIC、推理存储 | 中 | 产品/产能路线与建设周期支持，但真实需求和融资仍未完全披露 | 不能把 2027 上游设备收入提前确认到 2026 |
| 2027 乐观情景可到 `$600-750B` | 低-中 | 需要多个多 GW 项目、融资、电力、HBM/封装共同兑现 | 不是基准预测，也不应被用于单一公司收入外推 |

## 十一、Reference 和数字来源附录

### 11.1 参考资料说明

本附录的“支持的数字/判断”明确说明每个来源在模型中承担的作用。`高` 表示一手披露、监管或技术规格；`中` 表示可信行业资料或一手资料中的前瞻项目；`低` 表示项目计划/非正式性质较强，只用于情景边界而非主锚点。除非特别说明，链接均在 2026-07-10 访问。

| 编号 / 来源 | 日期 | 来源层级 | 支持的数字/判断 | 是否一手 | 置信度 | 备注 |
|---|---|---|---|---|---|---|
| R01 [Microsoft FY2026 Q3 earnings call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3) | 2026-04-29 | 公司财报 / call | 2026 日历年 CapEx 约 `$190B`；Q3 CapEx `$31.9B`；AI capacity、Fairwater、短寿命资产占比 | 是 | 高 | CFO CapEx 章节；计入 finance leases，不能与开发商重复 |
| R02 [Alphabet 2025Q4 / 2026 outlook call](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx) | 2026-02-04 | 公司财报 / call | 2026 CapEx `$175-185B`；2025 CapEx 结构约 `60%` servers、`40%` data center/network | 是 | 高 | 主锚点，用于 AI/DC 结构和全球 CapEx 上限 |
| R03 [Meta 2026Q1 results](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/) | 2026-04-29 | 公司财报 | 2026 CapEx 指引上调至 `$125-145B` | 是 | 高 | 含 finance lease principal；主模型按美国/AI 系数转换 |
| R04 [Amazon 2025Q4 results](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx) | 2026-02-05 | 公司财报 | 2026 公司 CapEx 约 `$200B`，涵盖 AI、chips、robotics、LEO 等 | 是 | 高 | 因用途混合，模型采用较低 AI/DC 比例 |
| R05 [Oracle FY2026 results](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Record-Q4-and-FY-2026-Results-Driven-by-Cloud-Infrastructure--Cloud-Applications/) | 2026-06-10 | 公司财报 | FY2026 CapEx `$55.7B`、RPO `$638B`、客户 GPU 预付款与融资安排 | 是 | 高 | 解释 OCI/AI Factory 的高投入与预付款去重 |
| R06 [CoreWeave 2026Q1 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-First-Quarter-2026-Results/) | 2026-05-07 | 公司财报 | backlog `$99.4B`、NeoCloud 扩张证据 | 是 | 高 | backlog 为服务收入，非当年建设 CapEx |
| R07 [Digital Realty 2026Q1 results](https://investor.digitalrealty.com/news-releases/news-release-details/digital-realty-reports-first-quarter-2026-results) | 2026-04-23 | 公司财报 | 租赁 bookings/backlog 与开发管线，辅助验证 hyperscale/AI colo | 是 | 高 | 配合其 [2026Q1 presentation](https://investor.digitalrealty.com/static-files/6de94c2d-af96-43ca-ab81-45ab3dc11eb6) 中的容量数据 |
| R08 [Equinix 2026 outlook](https://investor.equinix.com/news-events/press-releases/detail/1096/equinix-provides-robust-2026-outlook-driven-by-strong) | 2026-02-11 | 公司财报 | xScale、在建项目、已控制电力/土地和 2026 非经常性 CapEx | 是 | 高 | 用于 colo 预租/开发载体，而非直接替代客户 CapEx |
| R09 [Applied Digital contracted capacity](https://ir.applieddigital.com/news-events/press-releases/detail/152/applied-digital-reaches-significant-milestone-surpassing-1) | 2026-05-20 | 公司公告 | 超过 `1GW` 合同容量、`300MW` lease 等 AI Factory 项目信号 | 是 | 高 | 项目 MW 需按 COD、融资和客户承担方折减 |
| R10 [DOE/LBNL U.S. data center energy use](https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers) | 2024-12-20 | 政府 / 一手研究 | 2023 年 `176TWh`，2028 年 `325-580TWh`，占比 `6.7-12%` | 是 | 高 | 是全美负荷边界，不等同 AI-only |
| R11 [EIA 2026 electricity-demand forecast](https://www.eia.gov/pressroom/releases/press582.php) | 2026-01-13 | 政府 | 2026-2027 用电增长与大算力设施驱动 | 是 | 高 | 用来校验电力/能源订单，不当作项目 CapEx |
| R12 [FERC large-load integration action](https://www.ferc.gov/news-events/news/ferc-launches-aggressive-targeted-action-speed-large-load-integration) | 2026-06-18 | 监管机构 | 对六大区域电网的大负荷接入改革要求 | 是 | 高 | 证明接入规则是建设速度变量 |
| R13 [Oncor 2026Q1 results](https://www.oncor.com/content/oncorwww/wire/en/home/newsroom/oncor-reports-first-quarter-2026-results.html) | 2026-05-07 | Utility / 一手 | 约 `271GW` 数据中心请求、向 ERCOT 提交 `122GW` 大负荷预测 | 是 | 高 | 请求量不是通电量，专门用于防止过度外推 |
| R14 [JLL 2026 Global Data Center Outlook](https://www.jll.com/en-ca/insights/market-outlook/global-data-centers) | 2026-01 | 行业资料 | 2026 平均建设成本约 `$11.3M/MW`，AI 基础设施可接近 `$25M/MW` | 否 | 中 | 本模型将美国 AI 全口径扩展为 `$21-31M/MW`，该扩展为本报告估算 |
| R15 [CBRE North America Data Center Trends H2 2025](https://www.cbre.com/insights/books/north-america-data-center-trends) | 2026-01 | 行业资料 | 北美主要市场在建约 `5,994MW`、租金/电力供给紧张 | 否 | 中-高 | 私有 hyperscaler 自建未必完全覆盖 |
| R16 [Eaton 2026Q1 analyst presentation](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf) | 2026-05-05 | 公司财报 | 电气美洲数据中心订单约增 `240%`、backlog/订单动能 | 是 | 高 | 电力设备订单的直接验证 |
| R17 [Micron FY2026 Q3 results](https://investors.micron.com/node/50671) | 2026-06-24 | 公司财报 | HBM4 高量产发货、HBM4E 目标 2027 量产、PCIe Gen6 SSD 进展 | 是 | 高 | HBM/存储供给与时间表主锚点 |
| R18 [TSMC 2026 Technology Symposium](https://pr.tsmc.com/english/news/3302) | 2026-04-22 | 公司技术资料 | 持续扩展 CoWoS、封装尺寸/未来 HBM stack 路线、CPO 进度 | 是 | 高 | 支持 CoWoS/先进封装结构性需求，非当期收入指引 |
| R19 [NVIDIA GB300 NVL72 reference architecture](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) | 2026-06 | 公司技术文档 | GB300 NVL72 全液冷、`72` GPU、最高约 `142kW/rack` | 是 | 高 | rack density 和冷却/供电模型主锚点 |
| R20 [NVIDIA FY2027 Q1 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/) | 2026-05-20 | 公司财报 | Data Center revenue `$75.2B`，compute `$60.4B`，networking `$14.8B` | 是 | 高 | 证明 compute/network 订单规模和强度 |
| R21 [Arista 1.6T AI fabric launch](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Introduces-Next-Generation-1-6Terabit-Portfolio-for-AI-Fabrics/default.aspx) | 2026-06-09 | 公司产品公告 | 1.6T 面向 rack-scale AI fabric、128 个 800G ports 等 | 是 | 高 | 1.6T 产品切换证据，不代表全市场立刻完成替换 |
| R22 [Dell FY2027 Q1 earnings call](https://investors.delltechnologies.com/static-files/b63ffff9-b729-403b-a231-c6af05667759) | 2026-05-28 | 公司财报 / call | AI orders `$24.4B`、AI server revenue `$16.1B`、backlog `$51.3B` | 是 | 高 | 服务器订单和客户广度验证 |
| R23 [Vertiv FY2025 Q4 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/) | 2026-02-11 | 公司财报 | backlog `$15.0B`、book-to-bill 约 `2.9x`、AI 相关订单强劲 | 是 | 高 | 电力/冷却硬件订单的主锚点 |
| R24 [Vertiv U.S. liquid-cooling expansion](https://investors.vertiv.com/news/news-details/2026/Vertiv-to-Expand-Ohio-Manufacturing-to-Boost-U-S--Production-of-Critical-Thermal-Management-Technologies-for-AI-Data-Centers/) | 2026-03-30 | 公司公告 | 美国液冷/chilled-water 产能扩展、2027 投产 | 是 | 高 | 支持液冷 2027 供给改善与订单可交付性 |
| R25 [GE Vernova 2026Q1 results](https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf) | 2026-04-22 | 公司财报 | 电气化业务拿到 `$2.4B` 数据中心设备订单；燃机 backlog/slot 信号 | 是 | 高 | 微电网、配电与燃机瓶颈验证 |
| R26 [Broadcom OFC 2026 AI infrastructure solutions](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai) | 2026-03-12 | 公司产品公告 | 102.4T switch、800G NIC、CPO/AI networking 产品状态 | 是 | 高 | 网络 ASIC 与 CPO 的技术路线 |
| R27 [AMD 2026Q1 results](https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results) | 2026-05-05 | 公司财报 | Data Center revenue `$5.8B`；Meta 最多 `6GW` AMD GPU 部署计划 | 是 | 高 | GPU 竞争与 ASIC/GPU 多元化证据 |
| R28 [OpenAI: building compute infrastructure](https://openai.com/index/building-the-compute-infrastructure-for-the-intelligence-age/) | 2026-04-29 | 公司公告 | Stargate 超过初始 10GW 进展的项目性陈述、近 `3GW` 增量 | 是 | 中 | 前瞻性项目资料，不能直接按年确认为 CapEx |
| R29 [OpenAI / Oracle / SoftBank five Stargate sites](https://openai.com/index/five-new-stargate-sites/) | 2025-09-23 | 公司公告 | 近 `7GW` 计划容量、超过 `$400B` 三年投资叙事、站点与项目进度 | 是 | 中 | 计划与签约/通电之间存在重大差异 |
| R30 [Anthropic and Amazon up to 5GW compute](https://www.anthropic.com/news/anthropic-amazon-compute?source=syndication) | 2026-04-20 | 公司公告 | 最多 `5GW` 新算力、年末近 `1GW` Trainium2/3 容量计划 | 是 | 中-高 | 多年安排，用于定制 ASIC 的上行场景 |
| R31 [PJM 2026 long-term load forecast](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/load-forecast-supplement-2026.pdf) | 2026-05 | 电网运营商 | 大负荷/数据中心负荷预测方法与区域压力 | 是 | 高 | 辅助判断 PJM/DOM 的上电能力 |
| R32 [Synergy: U.S. hyperscale investment shifts inland](https://www.srgresearch.com/articles/focus-of-us-hyperscale-investment-shifts-dramatically-inland) | 2026-04-13 | 行业资料 | Texas/Midwest 在未来美国 hyperscale 新增容量中的占比上升 | 否 | 中 | 支持区域迁移判断 |
| R33 [LightCounting April 2026 optical forecast update](https://www.lightcounting.com/newsletter/en/april-2026-market-forecast-379) | 2026-04 | 行业资料 | AI cluster 连接带动 800G ZR/ZR+、后续 1.6T ZR/ZR+ | 否 | 中 | 公开摘要，不替代厂商出货数据 |
| R34 [Broadcom FY2026 Q2 results](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial) | 2026-06-03 | 公司财报 | AI semiconductor revenue `$10.8B`、由 custom accelerator 与 AI networking 驱动 | 是 | 高 | ASIC 与网络价值池的财务验证 |
| R35 [EMCOR 2026Q1 results](https://emcorgroup.com/investor-relations/press-releases/2026-news/emcor-group-inc-reports-first-quarter-2026-results) | 2026-04-29 | 公司财报 | RPO `$15.62B`、数据中心/network 活动强劲 | 是 | 高 | MEP/工程 backlog 交叉验证 |
| R36 [Georgia Power data-center tariff and infrastructure page](https://www.georgiapower.com/data-centers.html) | 2026-07 访问 | Utility | 大负荷客户需承担本地基础设施与长期合同/担保，体现“电力不是免费输入” | 是 | 中-高 | 规则会因州/utility 而异，不能外推全国 |

### 11.2 可复算参数汇总

| 参数 | 悲观 | 务实 | 乐观 | 主要来源 / 本报告推导 |
|---|---:|---:|---:|---|
| 2026 美国 AI DC CapEx | `$245-300B` | `$335-410B` | `$430-530B` | 五大云厂商 CapEx + 去重公式 [R01-R09] |
| 2027 美国 AI DC CapEx | `$275-345B` | `$410-510B` | `$600-750B` | 2026 基数、CapEx 增速、MW/供给/融资约束 |
| 全口径 CapEx / 新建 AI IT load | `$23-30M/MW` | `$21-31M/MW` | `$20-30M/MW` | JLL 成本边界 [R14] + 高密度 GPU/能源/预付款的估算调整 |
| 高密度 rack power | `70-110kW` | `90-140kW` | `120-180kW` | GB300 `142kW` [R19]；跨平台混合估算 |
| 设施 PUE | `1.20-1.30` | `1.15-1.25` | `1.12-1.22` | 本报告工程估算；按液冷/气候/设计不同而变化 |
| 2027 同年实际通电 AI IT load | `6-9GW` | `10-15GW` | `16-22GW` | CapEx/MW、建设周期、电网/项目证据交叉推导 [R10-R15, R28-R31] |
| 2027 HBM / DRAM / SRAM 穿透订单 | `$24-38B` | `$38-60B` | `$58-88B` | 每 GPU HBM attach、平台升级与供应能力推导 [R17-R18, R20, R27] |

---

### 结尾提示

本研究的正确使用方式是把总 CapEx、上电 MW、服务器/网络/电力供应商订单和 HBM/CoWoS 供给放在同一张监控面板上。只看 CapEx，会高估可运行容量；只看 MW 申请，会高估已落地项目；只看 NVIDIA/服务器收入，会低估电力与工程的时滞；只看 REIT 预租，又会把多年租约误当为当年收入。四条证据链同时成立，才是 2026-2027 美国 AI 数据中心爆发周期可以被证伪、也可以被持续上修的模型。
