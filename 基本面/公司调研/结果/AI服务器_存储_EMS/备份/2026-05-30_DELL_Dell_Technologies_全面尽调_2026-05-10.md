# 公司：DELL Dell Technologies Inc. 全面尽调

> 生成日期：2026-05-10。价格与估值口径采用 2026-05-08 美股收盘数据，因为 2026-05-09/10 为周末。  
> 资料口径：未参考本目录“公司调研”下其他公司报告。外部资料以 Dell IR/SEC、Dell/NVIDIA 产品发布、财报电话会、StockAnalysis、行业会议和公开媒体为主；项目内只参考非“公司调研”目录的 AI 服务器、AI 数据中心、GTC/Xcelerated Compute 等行业材料。  
> 重要说明：本文是产业与财务尽调，不构成投资建议。文中“推断/估算”均明确标注，实际订单、客户交付和取消率以公司后续披露为准。

## 0. 结论摘要

Dell 已经从“PC+企业服务器+存储”的成熟硬件公司，变成 2026 年最直接受益于 AI 工厂建设的系统级交付商之一。最新官方数据很清楚：FY2026 全年收入 1135.38 亿美元，同比增长 19%；AI-optimized server 收入 246.83 亿美元，同比增长 166%；FY2026 AI 服务器订单超过 640 亿美元，Q4 单季订单 341 亿美元，期末 backlog 430 亿美元；公司 FY2027 指引 AI 服务器收入约 500 亿美元，同比增长约 100%。这使 Dell 的投资叙事从“低估值硬件股/PC 周期股”切到“AI rack-scale 供应链总包+企业 AI 基础设施入口”。

最值得重视的不是 PC，而是四条线：

| 重点 | 当前证据 | 投资含义 |
|---|---|---|
| AI-optimized servers/rack-scale | FY26 收入 246.83 亿美元，FY27 指引约 500 亿美元；Q4 backlog 430 亿美元 | 收入可见度极高，但毛利率主要受 GPU/HBM pass-through、客户结构和存储/服务 attach 影响 |
| Dell Integrated Rack Scalable Systems | XE9712/GB300、XE9812/Rubin、IR5000/IR7000/IR9000，液冷/风冷/平台可选 | Dell 的壁垒在工程、认证、安装、支持和融资，不是单个服务器 SKU |
| AI Data Platform/Storage | PowerScale、ObjectScale、Lightning File System、Exascale Storage、Data Orchestration Engine | AI 服务器出货后，RAG、checkpoint、KV cache、数据治理带来滞后 attach，利润率高于纯服务器 |
| AI networking + rack power/cooling integration | PowerSwitch Z9964、SN6000/Spectrum、SmartFabric、PowerCool RCDU | 单独收入未披露，但决定 rack 可交付性；也是服务和系统溢价来源 |

最大风险也很具体：AI 服务器是高收入、低容错、相对低毛利的交付生意。上游 GPU/HBM/内存涨价、neocloud 融资质量、客户集中度、项目验收延期、NVIDIA 参考设计标准化压缩集成商溢价，都会影响盈利质量。Dell 的胜负手是让 AI 服务器订单带动更高毛利的存储、网络、服务、软件和长期支持，而不是只做 GPU 盒子搬运。

## 1. 公司整体业务、市场定位与近三年变化

### 1.1 业务结构

Dell Technologies 主要分两大运营部门：

| 部门 | FY2026 收入 | 同比 | FY2026 占比 | 主要内容 |
|---|---:|---:|---:|---|
| Infrastructure Solutions Group, ISG | 608.26 亿美元 | +40% | 53.6% | AI-optimized servers、传统服务器与网络、存储 |
| Client Solutions Group, CSG | 509.84 亿美元 | +5% | 44.9% | 商用 PC、消费 PC、工作站、显示器和相关服务 |
| Corporate/Other | 17.28 亿美元 | -52% | 1.5% | VMware resale、Secureworks/Virtustream 等退出或非核心业务残留 |
| 合计 | 1135.38 亿美元 | +19% | 100% | FY2026 全年 |

ISG 内部变化更关键：

| ISG 子业务 | FY2026 收入 | 同比 | 占公司收入 | 占 ISG 收入 |
|---|---:|---:|---:|---:|
| AI-optimized servers | 246.83 亿美元 | +166% | 21.7% | 40.6% |
| Traditional servers & networking | 195.12 亿美元 | +9% | 17.2% | 32.1% |
| Storage | 166.31 亿美元 | +1% | 14.6% | 27.3% |

投资人眼中的 Dell 正在快速重估。过去 Dell 常被看作 PC 周期、企业 IT 预算和低毛利硬件的综合体；2025-2026 年，AI 服务器 backlog 和 FY2027 500 亿美元 AI 服务器指引让市场把它当作 NVIDIA/AMD AI 基建的系统总包商、企业 AI 私有化入口，以及 Supermicro、HPE、Lenovo、ODM/JDM 厂的直接对标。

### 1.2 近三年重大变化

1. AI Factory 叙事确立：2024 年推出 Dell AI Factory with NVIDIA，2026 年两周年时披露已有 4000+ 客户部署，早期客户最高 2.6x 首年 ROI。Dell 将服务器、存储、网络、服务、AI 数据平台和工作站打包为从桌面到数据中心的 AI 工厂。
2. AI 服务器从小业务变成主驱动：FY2024 AI server 收入约 19 亿美元，FY2025 约 93 亿美元，FY2026 246.83 亿美元，FY2027 指引约 500 亿美元。
3. 存储与数据平台从传统存储升级为 AI 数据层：2026 年推出/强化 Dell AI Data Platform with NVIDIA、Data Orchestration Engine、Lightning File System、Exascale Storage、PowerScale pNFS、ObjectScale AI-Optimized Search 等。
4. 资产组合简化：Secureworks 于 2025 年 2 月被 Sophos 收购，Dell 持股获得现金退出；VMware 已于 2021 年 spin-off，并在 2023 年被 Broadcom 收购，Dell 现在更聚焦硬件、基础设施和服务。
5. 成本结构持续压缩：FY2026 员工约 97000 人，较 FY2023 的约 133000 人下降约 27%；FY2026 severance 约 5.69 亿美元，显示公司用降本支持 AI 服务器低毛利扩张。
6. 治理/注册地变化：2026-05-04 董事会建议将注册地从 Delaware 迁至 Texas，预计不影响业务、战略、资产或员工地点。

### 1.3 产业链位置

Dell 位于 AI 基建产业链的“系统集成/品牌 OEM/企业交付”层：

| 上游/下游 | Dell 的位置 |
|---|---|
| 上游芯片 | 依赖 NVIDIA GB200/GB300/Rubin、AMD MI355X/MI450、Intel/AMD CPU、Broadcom/NVIDIA 网络芯片 |
| 上游内存/封装 | 间接受 HBM3E/HBM4、DRAM、SSD、CoWoS/先进封装供需影响 |
| 系统层 | Dell 的核心战场：PowerEdge AI server、Integrated Rack Scalable Systems、PowerSwitch、PowerCool、OpenManage/SmartFabric、服务 |
| 数据层 | PowerScale/ObjectScale/PowerProtect/DataDomain/Lightning/Exascale + Data Orchestration Engine |
| 客户 | hyperscaler、neocloud、主权 AI、企业、科研/HPC、能源/生命科学/金融 |
| 竞争对手 | HPE、Lenovo、Supermicro、Cisco、Foxconn/QCT/Wiwynn/Wistron/Inventec 等 ODM/JDM，以及 NVIDIA DGX 体系 |

Dell 的独特性不是 GPU 本身，而是“多平台+全球供应链+企业销售+现场服务+融资+存储 attach”。它比 ODM 更有企业客户与服务能力，比纯品牌 PC 厂更深地进入 AI rack，比高毛利芯片厂更低利润但更贴近项目交付。

## 2. 估值、利润率与资产负债表

### 2.1 最新市场与财务指标

| 指标 | 数值 | 日期/口径 | 说明 |
|---|---:|---|---|
| 股价 | 260.46 美元 | 2026-05-08 收盘 | 盘后 262.69 美元 |
| 市值 | 1693.5 亿美元 | 2026-05-08 | StockAnalysis |
| PE | 30.01x | 2026-05-08 | 基于 TTM EPS 8.68 美元 |
| Forward PE | 20.12x | 2026-05-08 | 与 FY2027 EPS 指引 12.90 美元大体一致 |
| PS | 1.49x | 2026-05-08 | TTM revenue 1135.4 亿美元 |
| Forward PS | 1.18x | 2026-05-08 | FY2027 revenue 指引 1400 亿美元附近 |
| TTM 收入 | 1135.4 亿美元 | FY2026 | +18.8%/+19% |
| FY2026 Non-GAAP 毛利率 | 20.4% | FY2026 | Q4 为 20.5% |
| FY2026 GAAP 净利率 | 约 5.2% | FY2026 | GAAP net income 约 59.4 亿美元 |
| FY2026 Non-GAAP 净利率 | 约 6.2% | FY2026 | Non-GAAP net income 70.46 亿美元 |
| FY2026 Adj. FCF | 115 亿美元 | FY2026 | 创纪录，自由现金流质量强 |
| 员工 | 约 97000 人 | FY2026 | 近三年显著精简 |

### 2.2 资产负债表健康度

Dell 资产负债表的表面特征是“负股东权益+高应付+高现金流”，不能简单用传统账面权益判断。

| 指标 | FY2026 Q4 | 判断 |
|---|---:|---|
| 现金及等价物 | 115.28 亿美元 | 流动性强 |
| 总流动资产 | 576.02 亿美元 | AI 服务器增长推高应收和库存 |
| 总流动负债 | 632.69 亿美元 | 流动负债高，当前比率 0.91 |
| 存货 | 104.37 亿美元 | Q4 随 AI 服务器交付显著上升 |
| 应付账款 | 336.30 亿美元 | 供应链融资/负现金转换周期的一部分 |
| 总债务本金 | 318 亿美元 | 其中 core debt 170 亿、DFS 相关债务 146 亿 |
| Core leverage | 1.4x | 接近长期 1.5x 目标 |
| 股东权益 | -24.70 亿美元 | 主要来自历史交易、回购和资本结构，不等同于短期偿债危险 |
| FY2026 CFO | 112 亿美元 | 能覆盖股东回报和经营扩张 |
| FY2026 资本回报 | 75 亿美元 | 回购+分红，FY2027 分红提高 20% |

综合判断：财务状况“健康但不保守”。健康来自强现金流、1.4x core leverage、可滚动的供应链账期和庞大订单；不保守来自 AI 服务器大单带来的应收/库存波动、总债务 318 亿美元、流动比率低于 1、负权益以及 neocloud/主权项目融资风险。若 backlog 兑现顺利，Dell 的现金转换能力很好；若 GPU/HBM 延迟或大客户推迟验收，营运资本会迅速吃现金。

## 3. 最新及最近五个财报季度分析

### 3.1 财报核心表

金额单位：十亿美元；利润率为部门 operating income/revenue 或公司 non-GAAP operating margin。AI backlog/orders 为公司披露和根据订单-出货关系推算；取消率未披露。

| 财报季度 | 总收入/同比 | Non-GAAP GM | Non-GAAP OI/率 | ISG 收入/率 | AI server 收入 | AI orders/book-to-bill/backlog | 传统 server+networking | Storage | CSG | AI 数据中心相关占比 | 重点信息 |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|
| FY26 Q4, 截至 2026-01-30 | 33.38 / +39% | 20.5% | 3.54 / 10.6% | 19.60 / 14.8% | 8.95，shipments 9.5 | orders 34.1；B/B 3.6x；backlog 43.0 | 5.85 / +27% | 4.80 / +2% | 13.49 / +14% | AI server 为总收入 26.8%，ISG 45.7% | 单季订单爆发，FY27 AI revenue 指引 50B；ISG 利润率环比修复 |
| FY26 Q3, 截至 2025-10-31 | 27.01 / 约 +11% | 21.1% | 2.50 / 9.3% | 14.11 / 12.4% | 5.64 | orders 12.3；B/B 2.18x；backlog 18.4 | 4.48 | 3.98 | 12.48 | 20.9% | five-quarter pipeline 为 backlog 的数倍，客户包括 neocloud、sovereign、enterprise |
| FY26 Q2, 截至 2025-08-01 | 29.78 / +19% | 18.7% | 2.28 / 7.7% | 16.80 / 8.8% | 8.21 | orders 5.6；B/B 0.68x；backlog 11.7 | 4.74 | 3.86 | 12.50 | 27.6% | 大额 AI 出货拉高收入，但毛利率承压；公司将 FY26 AI shipment 指引升至 20B |
| FY26 Q1, 截至 2025-05-02 | 23.38 / +5% | 21.6% | 1.67 / 7.1% | 10.32 / 9.7% | 1.88 | orders 12.1；B/B 6.4x；backlog 14.4 | 4.44 | 4.00 | 12.51 | 8.1% | AI 订单超过 FY25 全年 shipments，验证需求斜率 |
| FY25 Q4, 截至 2025-01-31 | 23.93 | 24.3% | 2.67 / 11.2% | 11.35 / 18.1% | 2.03 | backlog 约 9.0；orders/取消率未披露 | 4.61 | 4.72 | 11.88 | 8.5% | 传统业务利润率高，AI 业务规模尚小；后续进入大单期 |

交期推断：Q4 FY26 结束时 AI backlog 430 亿美元。相对 FY27 AI server 指引 500 亿美元，覆盖率约 86%；相对 Q1 FY27 AI server 指引 130 亿美元，约等于 3.3 个 Q1 的出货量；相对 Q4 shipments 95 亿美元，约等于 4.5 个 Q4。公司没有披露 lead time 和取消率，但 backlog/年度指引关系说明交付窗口大概率覆盖未来 3-4 个季度，核心瓶颈为 GPU/HBM/先进封装、液冷、power shelf、网络和现场验收。

### 3.2 最近财报的几个反常识点

1. AI 服务器收入暴增，但公司毛利率没有同步扩张。FY26 Q2 AI server 收入 82 亿美元时 Non-GAAP GM 只有 18.7%，ISG margin 8.8%，说明早期大单、GPU/HBM/内存 pass-through 和客户议价压缩毛利。
2. Q4 ISG margin 从 Q2 的 8.8% 修复到 14.8%，部分来自 storage mix 和执行改善。若 FY27 AI mix 更高但 storage/service attach 不提升，利润率仍可能波动。
3. Storage FY26 仅 +1%，和 AI server +166% 形成强烈反差。我的判断是 AI storage attach 仍在滞后期：训练数据、RAG、KV cache、checkpoint 和治理需求会在服务器交付后逐步体现。
4. FY26 Q4 orders 341 亿美元远高于 shipments 95 亿美元，book-to-bill 约 3.6x。它不是收入，但代表 FY27 可见度；真正要跟踪的是 backlog 是否在 Q1/Q2 FY27 兑现而不牺牲利润率。
5. 取消率未披露。根据 FY26 Q3/Q4 backlog 从 184 亿美元跳到 430 亿美元的轨迹，短期取消率不像是主要问题；但 neocloud 融资、GPU 租金、客户 ROI 和电力交付会决定 2027 年后订单质量。

## 4. FY2027 指引、收入占比与产品拆解

### 4.1 最新官方指引

最新官方指引来自 2026-02-26 发布的 FY2026 Q4/FY2026 全年财报，FY2027 Q1 财报计划 2026-05-28 发布。

| 指引项 | FY2027 | FY2027 Q1 | 含义 |
|---|---:|---:|---|
| 总收入 | 1400 亿美元 ±20 亿，约 +23% | 352 亿美元 ±5 亿，约 +51% | AI server 是主驱动 |
| Non-GAAP EPS | 12.90 美元 ±0.25，约 +25% | 2.90 美元 ±0.10，约 +87% | EPS 增速高于收入，依赖费用纪律和回购 |
| AI server revenue | 约 500 亿美元，约 +100% | 约 130 亿美元 | AI server 将达总收入约 36% |
| ISG | mid-forties 增长 | over 100% 增长 | ISG 成为公司主业务 |
| Traditional server + storage | mid-single digits 增长 | 未细分 | 非 AI 仍稳健但不是爆发点 |
| CSG | 约 +1% | 约 +2% | PC 更新周期温和，不是核心变量 |
| 毛利率 | 剔除 AI mix 后同比提升 | 未披露 | AI mix 会压低表观 GM |

按 FY2027 指引粗略拆分：

| 业务 | FY2026 收入 | FY2027 基准估算 | 增长 | FY2027 占比 |
|---|---:|---:|---:|---:|
| AI-optimized servers | 246.83 亿美元 | 500 亿美元 | +103% | 35.7% |
| Traditional server + networking + storage | 361.43 亿美元 | 约 378-385 亿美元 | 中个位数 | 27% |
| CSG | 509.84 亿美元 | 约 515 亿美元 | +1% | 36-37% |
| Corporate/Other | 17.28 亿美元 | 低个位数/继续下降 | 下降 | <1% |

最突出的业务是 AI-optimized server，其次是 AI storage/data platform 和 rack-scale integration。PC/Consumer、普通外设、传统非 AI 服务器、legacy/other 已不应作为主要投资变量。

### 4.2 产品与业务对应关系

| 业务 | 关键产品/型号 | 收入口径 | 增长/利润判断 |
|---|---|---|---|
| NVIDIA rack-scale AI servers | PowerEdge XE9712, XE9812, XE8712, XE9680L/XE9685L, XE9780L/XE9785L；GB200/GB300/Rubin NVL72 | AI-optimized server | FY27 指引 500 亿美元；毛利率低于软件/芯片，但服务、storage attach 可改善 |
| AMD AI/HPC servers | PowerEdge XE9785/XE9785L，AMD EPYC + MI355X，AMD Pensando Pollara AI NIC | AI-optimized server | 第二供应源，有助于非 NVIDIA 客户和 TCO 优化；规模小于 NVIDIA |
| Integrated Rack Scalable Systems | IR5000 EIA 19"、IR7000 OCP ORv3、IR9000 exclusive rack；PowerCool RCDU | AI server + services | 单独收入未披露；是 Dell 与白牌 ODM 拉开差距的服务/工程层 |
| AI Data Platform/storage | PowerScale、ObjectScale、Lightning File System、Exascale Storage、PowerProtect、DataDomain、Data Orchestration Engine | Storage + software/services | FY26 storage 166.31 亿美元只 +1%，但 AI attach 潜力大，利润率高于 AI server |
| AI networking | PowerSwitch Z9964F/FL、SN6000/Spectrum-6、SONiC、SmartFabric Manager | server/networking + rack | 单独未披露；1.6T/102.4Tbps 与 AI fabric 需求强，毛利率取决于交换机/光模块/服务结构 |
| Edge/desktop AI | Dell Pro Max with GB10/GB300、Pro Precision 5/7/9、RTX PRO Blackwell workstation | CSG/Workstation | 小基数、高 ASP；对总收入影响小，但可能提升 CSG mix |
| AI services | Accelerator Services for Agentic AI、AI use-case pilots、one-call rack support、ProSupport | Services/attach | 高毛利、小基数；决定客户转换成本和复购 |

### 4.3 可跳过或低权重业务

以下业务仍重要，但不是本次 AI 投资主线：

| 低权重业务 | 原因 |
|---|---|
| Consumer PC | FY26 consumer revenue 69.22 亿美元，同比 -8%；Q4 基本持平 |
| 普通商用 PC | CSG FY27 指引约 +1%，不是高增长来源 |
| 普通外设/显示器 | 与 AI data center 相关性弱，增速有限 |
| VMware resale、Secureworks、Virtustream 等 Other | Secureworks 已出售，Other FY26 同比 -52% |
| 非 AI 传统服务器 | 有 16G/17G 更新机会，但 mid-single digits 增长，不决定估值弹性 |

## 5. 高增长/关键产品当前贡献与战略评分

评分 1-5：5 为最强。收入贡献为官方披露或估算，估算会注明。

| 产品/业务 | 当前收入贡献 | 收入增速 | AI 基建重要性 | 时间紧急性 | 供需紧张度 | 垄断/溢价能力 | 关键判断 |
|---|---:|---:|---:|---:|---:|---:|---|
| AI-optimized servers | FY26 246.83 亿美元；Q4 89.52 亿美元 | +166% FY26；Q4 +342% | 5 | 5 | 5 | 3 | Dell 最核心增长引擎；供给由 NVIDIA/AMD/HBM 决定，Dell 溢价来自交付和认证 |
| GB300/XE9712 NVL72 | 包含在 AI server；推断 FY26 下半年主要增量之一 | 高三位数放量 | 5 | 5 | 5 | 3 | CoreWeave 首批 GB300 NVL72 与 Dell/Switch/Vertiv 合作，验证交付能力 |
| Rubin/XE9812 NVL72 | 当前收入小，2H26 GA | 2027 起高增长 | 5 | 4 | 5 | 3 | 未来 12 个月订单认证关键；HBM4、液冷、1.6T 网络制约 |
| Integrated Rack + PowerCool | 官方未拆；估算 FY26 约 10-20 亿美元服务/集成价值 | +50-100% | 5 | 5 | 4 | 4 | rack burn-in、液冷、现场支持是客户愿意付费的风险降低层 |
| AI Data Platform/storage | FY26 storage 166.31 亿美元；AI 相关估算 20-40 亿美元 | storage 总体 +1%，AI 子集高增长 | 4 | 4 | 3 | 4 | 目前收入没有爆发，但利润率和客户锁定潜力优于服务器 |
| PowerSwitch/AI networking | 未拆；估算低个位数十亿美元 | +30-80% | 4 | 4 | 4 | 3 | Z9964 102.4Tbps、SN6000/Spectrum-6 对 1.6T AI fabric 关键 |
| Data Orchestration Engine | 当前收入小，Dataloop 技术整合 | 小基数高增长 | 3 | 3 | 2 | 4 | 如果与 PowerScale/ObjectScale 绑定，可增强 AI 数据平台黏性 |
| Pro Max GB300/Pro Precision | CSG 内小业务，估算 <20 亿美元 | +20-50% | 2 | 2 | 2 | 3 | 本地 agent/AI workstation 叙事强，但短期不改变公司收入结构 |

## 6. 一年后收入贡献三情景预测

时间口径：从最新 FY2026 Q4 披露向后约一年，即 FY2027/FY2027 Q4 附近。所有非官方拆分为估算。

| 产品/业务 | 基准：收入/增长/评分 | 乐观：收入/增长/评分 | 极度乐观：收入/增长/评分 |
|---|---|---|---|
| AI-optimized servers | 500 亿美元，+103%；重要性 5、紧急性 5、紧张度 4、溢价 3 | 600-650 亿美元，+140-160%；紧张度 5、溢价 3.5 | 750-800 亿美元，+200%+；供给顺利且新增订单继续爆发，溢价 4 |
| GB300/XE9712 | AI server 内约 300-380 亿美元；FY27 主力 | 400-480 亿美元；GB300 交付高于计划 | 550 亿美元以上；Rubin 之前 GB300 超长窗口 |
| Rubin/XE9812 | 20-50 亿美元；2H26 早期收入 | 80-120 亿美元；2H26 验证顺利 | 150-200 亿美元；Rubin 与 GB300 并行且客户提前锁量 |
| Integrated Rack + services/cooling | 25-35 亿美元；+70% 左右 | 40-55 亿美元；液冷/现场支持 attach 提升 | 70 亿美元以上；rack-level 服务成为 RFP 标配 |
| AI storage/data platform | AI 相关 45-60 亿美元；storage 总体 170-180 亿美元 | AI 相关 70-90 亿美元；KV cache/RAG attach 提升 | AI 相关 120 亿美元以上；AI storage share 快速抬升 |
| AI networking/PowerSwitch | 35-50 亿美元 | 60-85 亿美元 | 100-120 亿美元；1.6T/CPO/Spectrum-6 拉动 |
| Data Orchestration Engine | 2-5 亿美元，主要随服务/平台打包 | 8-12 亿美元 | 20 亿美元级，若成为 Dell AI Data Platform 控制层 |
| Edge/desktop AI workstation | 20-30 亿美元 | 35-50 亿美元 | 70 亿美元；本地 agent/workstation 更新周期超预期 |

我的基准情景基本贴近公司 FY2027 指引：AI server 500 亿美元，总收入 1400 亿美元，Non-GAAP EPS 12.90 美元。乐观情景来自三个条件同时满足：GB300/HBM3E 供给顺，Rubin early ramp 不挤压 GB300，storage/network/service attach 提升。极度乐观情景需要 Q4 FY26 这种 341 亿美元级订单不是一次性，而是 FY27 继续滚动出现，同时电力和客户融资没有卡住。

## 7. BOM、单位含量、价格传导与产能能力

### 7.1 典型 AI rack BOM 拆分

以 GB300/Rubin NVL72 级别整柜为例，行业实际价格随 GPU、内存、网络、客户配置和服务条款差异很大。以下为用于交叉验证的估算框架，不是 Dell 官方报价。

| 成本项 | 含 GPU 整柜 BOM 占比 | Dell 可捕获价值 | 价格传导 |
|---|---:|---|---|
| GPU/ASIC + HBM + advanced packaging | 65-80% | 主要 pass-through，毛利率低于上游 | GPU/HBM 涨价通常传导给客户，但压缩 Dell 绝对毛利率 |
| CPU、主板、内存、UBB/OAM、SSD | 4-10% | Dell/ODM 可捕获中低毛利 | DRAM/SSD 涨价可部分转嫁，短期影响 GM |
| NVLink/NVSwitch/Scale-up fabric | 5-12% | 多数来自 NVIDIA/Broadcom，上游价值高 | 随 GPU 平台绑定，切换成本高 |
| Scale-out networking、NIC/DPU、光模块 | 5-12% | Dell 可通过 PowerSwitch、SmartFabric、SONiC 和服务捕获 | 800G/1.6T 光模块和交换机紧张时溢价 |
| 液冷：cold plate、manifold、CDU/RCDU、UQD、传感器 | 3-8% | Dell 多为集成/服务，关键部件来自生态伙伴 | 可靠性溢价强，故障成本高 |
| 机柜供电：48V shelf、PDU、busbar、BBU/UPS 接口 | 2-6% | Dell 集成价值中等 | rack power 瓶颈时可形成服务溢价 |
| 机柜结构、线缆、背板、连接器 | 2-5% | 低到中毛利 | 高速铜缆/AEC 价值高于普通结构件 |
| 系统集成、burn-in、现场安装、支持 | 3-8% | Dell 最应争取的高质量收入 | 客户愿为少延期、少故障、one-call support 付费 |
| 软件/管理/安全/数据平台 | 1-5% | 高毛利，小基数 | 长期锁定客户，提升复购 |

### 7.2 每 rack、每 MW、每 GPU、每 optical port 内容量

| 单位 | 典型内容量 | Dell 收入/价值估算 | 备注 |
|---|---|---:|---|
| 每 GB300 NVL72 rack | 72 个 Blackwell Ultra GPU、36 个 Grace CPU、NVLink/NVSwitch、每 GPU 约 800Gb/s 网络、液冷、rack power、management | 整柜 ASP 估算 350-500 万美元；Dell 非 GPU/服务含量约 60-120 万美元 | NVIDIA 官方 GB300 NVL72 为全液冷 rack-scale；Dell XE9712 为对应 PowerEdge 平台 |
| 每 Rubin NVL72 rack | 72 个 Rubin GPU、36 个 Vera CPU、NVLink 6、ConnectX-9、BlueField-4、Spectrum-6 生态 | 初期 ASP 估算高于 GB300，可能 450-650 万美元 | 2H26 供货/认证，HBM4 和液冷是关键 |
| 每 MW IT load | 若 120-150kW/rack，则约 6.7-8.3 个 NVL72 rack，约 480-600 GPU/MW | 含 GPU 系统收入约 2700-4200 万美元/MW；Dell 非 GPU/服务约 400-800 万美元/MW | 若未来 rack 功率升至 200kW，GPU/MW 与收入/MW 会变化 |
| 每 GPU | 1/72 rack；含 HBM、NVLink、network、share of CPU/power/cooling/storage | 系统 ASP 约 5-7 万美元/GPU；Dell 非 GPU/集成约 0.8-1.7 万美元/GPU | 与 GPU 采购价、客户折扣相关 |
| 每 800G optical/logical port | GB300 每 GPU 800Gb/s，约 72 个逻辑 800G 连接/rack；物理模块可能 72-144 个，取决于 breakout/冗余 | 800G 端口含光模块/交换端口/线缆约 1500-3000 美元；1.6T 约 3000-7000 美元 | Dell 可捕获交换机、SONiC/SmartFabric、服务；光模块多为生态 pass-through |
| 每 10PB AI storage cluster | Exascale/PowerScale/ObjectScale/Lightning 组合；Dell 披露 Exascale 面向 10PB+，可达每 rack 6TB/s 性能口径 | 估算 300-1200 万美元，视闪存/HDD/性能层比例 | AI storage 与 GPU 利用率、RAG/KV cache 绑定 |
| 每 150kW rack cooling | Dell PowerCool RCDU 支持最高 150kW rack density，4U form factor | 单 rack 液冷/分配/服务约 8-25 万美元，极高密度更高 | Dell 捕获集成、维护和支持，不一定制造全部部件 |

### 7.3 当前产能、采纳与认证阶段

| 产品/业务 | 当前产能能力（美元计） | 供应链采纳 | 认证/阶段 |
|---|---:|---|---|
| AI-optimized servers | Q4 FY26 shipments 约 95 亿美元，Q1 FY27 指引约 130 亿美元，年化 520 亿美元 | hyperscaler、neocloud、sovereign、enterprise 全部采纳 | GB300/XE9712 已商业交付；FY27 guide 50B |
| GB300/XE9712 | 已在 CoreWeave 等客户部署；Q4/FY27 主力 | 与 Dell/Switch/Vertiv 协同交付获验证 | NVIDIA GB300 NVL72 平台；Dell XE9712 spec/IRSS |
| Rubin/XE9812 | 当前小批/认证期，2H26 GA | Dell、HPE、Lenovo、SMCI 等均为生态伙伴 | Dell PowerEdge XE9812 全球 2H26 可用 |
| AI Data Platform/storage | FY26 storage 166 亿美元基础盘；AI 子集仍小 | PowerScale/ObjectScale/Lightning/Exascale 支持 AI/RAG/KV cache | Lightning 2026-04；Exascale 2026 2H；NVIDIA CMX/STX 支持陆续推出 |
| PowerSwitch/AI networking | 单独未披露；随 server/networking 和 rack 交付 | Broadcom TH6、NVIDIA Spectrum-6 双路线 | Z9964F/FL 2H26；SN6000 2026-07；Quantum-X800 Q4 2026 |
| Rack cooling/services | 与 AI rack 出货绑定，RCDU 1H26 | OCP 19/21 inch rack，IR5000/IR7000/IR9000 | PowerCool RCDU 1H26；OpenManage/Integrated Rack Controller 2026 |

### 7.4 一年后产能与认证三情景

| 产品/业务 | 基准 | 乐观 | 极度乐观 |
|---|---|---|---|
| AI servers | 年收入能力 500-550 亿美元；backlog 覆盖 FY27 大半 | 650 亿美元能力；GB300/Rubin 并行交付 | 800 亿美元能力；新订单继续高于出货 |
| GB300/XE9712 | 大规模交付，逐步被 Rubin 接棒 | 供给更顺，GB300 延长高收入窗口 | GB300 与 Rubin 同时紧缺，客户提前锁 2027 产能 |
| Rubin/XE9812 | 2H26 认证/早期生产，FY27 收入 20-50 亿美元 | 2H26 快速 ramp，FY27 收入 80-120 亿美元 | 成为 2027 主力之一，收入 150 亿美元以上 |
| AI Data Platform/storage | AI attach 率逐季提升，Lightning/Exascale GA | CMX/KV cache、RAG storage 成为企业 AI 标配 | AI storage 从补充采购变成每个 inference pod 的必要配置 |
| PowerSwitch/networking | 800G 主流，1.6T 初期 | 1.6T 2H26 提前放量，SN6000/Z9964 贡献明显 | CPO/1.6T/AI Ethernet 供需紧张，Dell 网络 attach 率大幅提高 |
| Rack cooling/services | RCDU、现场服务随 rack 出货增长 | 液冷服务成为大客户 RFP 必选 | 交付/burn-in/现场可靠性成为限制行业产能的瓶颈，Dell 溢价扩大 |

## 8. 基于 backlog 和供给的未来一年增速预测

### 8.1 订单与供给交叉验证

| 指标 | 数值 | 含义 |
|---|---:|---|
| FY26 AI server orders | >640 亿美元 | 大于 FY26 AI revenue 246.83 亿美元 2.6 倍 |
| FY26 Q4 AI orders | 341 亿美元 | 单季订单接近 FY26 全年收入的 1.4 倍 |
| FY26 Q4 AI shipments | 95 亿美元 | 单季高 run-rate，但仍低于订单 |
| FY26 Q4 AI backlog | 430 亿美元 | 覆盖 FY27 AI revenue 指引约 86% |
| FY27 AI revenue guide | 500 亿美元 | 官方基准 |
| FY27 Q1 AI revenue guide | 约 130 亿美元 | 年化 520 亿美元，说明供给/交付能力已接近 FY27 指引 |
| 取消率 | 未披露 | 需用 backlog 转收入和订单续签观察 |

我的推断：FY27 AI server 增速的下限主要由已披露 backlog 提供，上限由新增订单、GB300/Rubin/HBM4 供给和客户电力/融资决定。若 FY27 不再新增订单，430 亿美元 backlog 也能覆盖绝大部分官方 500 亿美元目标；但现实中 Dell 需要持续新增订单来维持 FY28 产能可见度。

### 8.2 未来一年三情景

| 情景 | AI server revenue | 新增 orders | FY27 末 backlog | 隐含 B/B | 取消/延期假设 | 主要条件 |
|---|---:|---:|---:|---:|---|---|
| 基准 | 500 亿美元 | 500-600 亿美元 | 400-500 亿美元 | 1.0-1.2x | 取消率低个位数，部分交付延期 | GB300 稳定，Rubin 小规模，电力和客户融资可控 |
| 乐观 | 600-650 亿美元 | 700-850 亿美元 | 500-650 亿美元 | 1.2-1.4x | 取消率低，部分客户追加 | GB300 供给提升，Rubin 2H26 顺利，storage/network attach 增加 |
| 极度乐观 | 750-800 亿美元 | 950-1150 亿美元 | 650-900 亿美元 | 1.3-1.5x | 取消率仍低，客户提前锁 2027-2028 | neocloud/主权 AI/hyperscaler 同时抢产能，HBM/液冷/网络无硬卡点 |

## 9. 竞争格局、替代方案与客户切换成本

### 9.1 主要竞争对手

| 细分 | 竞争对手 | Dell 相对位置 |
|---|---|---|
| 品牌 AI OEM | HPE、Lenovo、Supermicro、Cisco | Dell 在企业销售、存储、全球服务和融资强；SMCI 速度快但治理/交付波动更高；HPE 有 Cray/HPC 和 Juniper 网络 |
| ODM/JDM | Foxconn、Quanta/QCT、Wiwynn、Wistron、Inventec、Pegatron | ODM 在 hyperscaler 白牌成本强；Dell 在品牌/服务/企业/主权 AI 更强 |
| NVIDIA 自有系统 | DGX、DGX SuperPOD、NVIDIA reference design | NVIDIA 控制平台与生态，Dell 是重要交付伙伴但被上游约束 |
| AI storage | NetApp、Pure、VAST、WEKA、DDN、HPE、IBM | Dell 有 PowerScale/ObjectScale/PowerProtect 大客户基础；纯软件/AI-native 厂商在性能/灵活性上有威胁 |
| AI networking | Arista、Cisco、NVIDIA Networking、HPE/Juniper、Celestica/Accton | Dell 可打包 PowerSwitch/SONiC/SmartFabric，但高端网络品牌壁垒低于 Arista/NVIDIA/Cisco |
| PC/workstation | HP、Lenovo、Apple、ASUS | Dell 商用渠道强，但 CSG 增速慢 |

### 9.2 新技术是否是主流

| 技术/产品 | 是否主流 | 风险与替代 |
|---|---|---|
| GB300/NVL72 rack-scale | 2026 主流高端 AI rack | 受 NVIDIA 节奏控制；替代为 AMD MI355X/MI450、云厂 ASIC rack |
| Rubin/NVL72 | 2027 高端主流候选 | HBM4/液冷/网络 ramp 风险；GB300 延长、ASIC 替代、AMD Helios 分流 |
| Direct liquid cooling | 高密度 AI rack 默认趋势 | 现场维护、漏液、水质、客户数据中心改造难度 |
| 800G/1.6T AI Ethernet/InfiniBand | 主流升级方向 | NVIDIA proprietary fabric、UEC/UALink 开放路线、Arista/Cisco/NVIDIA 竞争 |
| AI Data Platform/KV cache storage | 2026 仍早期，2027 潜力大 | 企业 adoption 慢；VAST/WEKA/DDN/NetApp/Pure 抢 AI-native 叙事 |
| Data Orchestration Engine | 小基数潜力业务 | 可能被 Databricks、Snowflake、cloud-native pipeline 或开源工具替代 |
| AI PC/workstation | 边缘/本地开发有价值，但非主线 | 云端推理更经济、本地模型需求不及预期 |

### 9.3 客户替换成本

| 产品 | 替换成本 | 原因 |
|---|---:|---|
| AI rack-scale server | 高 | rack 设计、液冷、NVLink/网络、BMC/firmware、burn-in、现场验收和供应链认证绑定 |
| Dell Integrated Rack + support | 高 | one-call support、现场服务、保修、融资和验收流程难以快速替代 |
| Storage/Data Platform | 中高到高 | 数据迁移、性能验证、治理/权限/备份策略复杂 |
| PowerSwitch/SONiC/SmartFabric | 中 | Ethernet 标准化降低锁定，但 fabric 调优、遥测和运维仍有黏性 |
| PC/workstation | 低到中 | 采购标准化，替换相对容易，除非绑定企业管理和服务合同 |

## 10. 需要持续跟踪的指标

| 指标 | 为什么重要 | 下次观察点 |
|---|---|---|
| FY27 Q1 AI server revenue 是否达到约 130 亿美元 | 验证 backlog 转收入能力 | 2026-05-28 FY27 Q1 财报 |
| FY27 Q1/Q2 ISG margin | 判断 AI 大单是否继续压毛利 | 目标是维持 12%+，接近/高于 Q4 14.8% 更强 |
| AI orders 与 backlog | 判断 FY28 可见度 | 若 B/B 仍 >1，估值支撑更强 |
| Storage 增速与 Dell IP mix | 判断 AI server 是否带动高毛利 attach | PowerScale/ObjectScale/Lightning/Exascale adoption |
| Rubin/XE9812 GA 节奏 | 2027 新平台切换风险 | 2H26 availability、客户认证、HBM4 供给 |
| 1.6T/SN6000/Z9964 出货 | 网络是否成为新增利润池 | 2026-07 后 SN6000、2H26 Z9964 |
| 库存、应收、CFO | 监控 AI 大单营运资本压力 | 若收入增长但 CFO 断崖，订单质量需重估 |
| neocloud 客户融资和利用率 | 影响取消/延期率 | CoreWeave、Nscale、IREN、xAI 等项目融资与租金 |

## 11. 核心参考资料

外部官方与财务：

- Dell IR 首页与最新事件：https://investors.delltechnologies.com/
- Dell FY2026 Q4/FY2026 performance review：https://delltechnologies.gcs-web.com/static-files/433e7b1b-c749-4411-bcd7-2f23fbf7f112
- Dell FY2026 Q4/FY2026 press release：https://investors.delltechnologies.com/node/19176/pdf
- Dell FY2026 10-K：https://www.sec.gov/Archives/edgar/data/0001571996/000157199626000008/dell-20260130.htm
- Dell FY2026 Q3 press release：https://investors.delltechnologies.com/node/19036/pdf
- Dell FY2026 Q2 press release：https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2025~08~dell-technologies-delivers-second-quarter-fiscal-2026-financial-results.htm
- Dell FY2026 Q1 press release：https://investors.delltechnologies.com/node/17691/pdf
- StockAnalysis DELL quote/statistics：https://stockanalysis.com/stocks/dell/ 和 https://stockanalysis.com/stocks/dell/statistics/

产品、AI Factory 与客户：

- Dell AI Factory with NVIDIA, 2026-03-16：https://investors.delltechnologies.com/news-releases/news-release-details/dell-ai-factory-nvidia-delivers-proven-path-enterprise-ai-roi
- Dell AI Data Platform with NVIDIA：https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2026~03~dell-ai-data-platform-with-nvidia-supercharges-enterprise-ai-with-breakthrough-data-orchestration-and-storage-innovations.htm
- Dell Data Orchestration Engine blog：https://www.dell.com/en-us/blog/powering-ground-truth-for-agentic-ai-with-the-dell-data-orchestration-engine/
- Dell SC25 AI Factory update：https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-accelerates-enterprise-ai-powerful-automated
- Dell delivers first NVIDIA GB300 NVL72 to CoreWeave：https://www.dell.com/en-us/blog/dell-delivers-market-s-first-nvidia-gb300-nvl72-to-coreweave/
- CoreWeave GB300 NVL72 deployment：https://investors.coreweave.com/news/news-details/2025/CoreWeave-Becomes-First-Hyperscaler-to-Deploy-NVIDIA-GB300-NVL72-Platform/default.aspx
- NVIDIA GB300 NVL72：https://www.nvidia.com/en-us/data-center/gb300-nvl72/
- NVIDIA Vera Rubin NVL72：https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/
- NVIDIA Vera Rubin platform release：https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform

行业与项目内非公司调研材料：

- `conference_update/nvidia_gtc_2026_research.md`
- `conference_update/xcelerated_compute_show_2026_report.md`
- `行业调研_AI服务器_存储_芯片/行业调研_AI服务器整机与机架集成_2026-05-08.md`
- `行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- `行业调研_AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-05-08.md`
- `行业调研_AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026.md`
- `行业调研_AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026.md`

