# 公司：VRT - Vertiv Holdings Co 全面尽调

> 日期：2026-05-09。本文未参考 `工作台v5/公司调研` 目录下任何既有公司报告；公开信息以 Vertiv IR/SEC、StockAnalysis、公司技术公告、NVIDIA/OCP/行业资料为主，并结合项目内 AI 数据中心电力、液冷、机架供电、预制化交付、DCIM 等行业研究。非公司披露的订单拆分、AI 收入占比、产品线收入、每 MW/每 rack 价值量均为估算，已在表中标注。

## 0. 结论摘要

Vertiv 是目前美股中最纯的 “AI 数据中心电力 + 热管理 + 预制化基础设施 + 服务” 组合之一。市场买它不是买传统 UPS，而是买 AI factory 从 GPU 订单变成可上电、可冷却、可验收算力的瓶颈环节。2025Q4 公司 organic orders 同比 +252%、book-to-bill 约 2.9x、backlog 达 **$15.0B**；2026Q1 收入 **$2.65B**、同比 +30%、全年收入指引上调至 **$13.5B-$14.0B**，这是当前投资故事的核心锚。

估值已经极高。2026-05-08 收盘价 **$339.97**，市值 **$130.59B**，TTM P/E **85.44x**，Forward P/E **49.96x**，P/S **12.04x**，Forward P/S **8.99x**。这意味着股价已经定价了较长时间的高增长和 margin expansion。若 2026H2 GB300、Blackwell Ultra、AI colo/hyperscaler 项目兑现，VRT 有继续上修空间；若 AI 数据中心项目延迟、800VDC 标准落地慢、客户压价或执行失误，估值回撤会很快。

最重要的业务不是单一产品，而是 **power + cooling + rack + prefabricated module + service + software** 的成套交付能力。高增长产品优先级：1）UPS/配电/母线/电能质量；2）CoolChip/XDU/CDU、RDHx、液冷流体服务和 heat rejection；3）MegaMod/SmartRun/Great Lakes/BMarko 的预制化白区和灰区模块；4）PurgeRite/服务；5）360AI/Waylay/Environet/OneCore 控制与运维软件；6）800VDC/HVDC 作为 2027 弹性期权。

## 1. 公司业务、投资人认知、产业链定位

### 1.1 整体业务

Vertiv 的业务是 critical digital infrastructure：让数据中心、通信网络、商业/工业关键设施持续供电、散热、监控和维护。公司官网和财报把产品分为：

| 大类 | 核心产品 | AI 数据中心相关性 |
|---|---|---|
| Critical Power | UPS、DC power、power distribution、static transfer switch、power monitoring/control、Li-ion battery cabinet | 极高。AI rack 功率从 10kW 级进入 100kW+，电力链从备用系统变成交付前置条件 |
| Thermal Management | High-density cooling、room/in-row/rack cooling、heat rejection、rear-door heat exchanger、CDU、液冷环路 | 极高。GB200/GB300/Rubin/MI400 等把 DTC 液冷从可选变成主流 |
| Racks & Enclosures / Integrated Solutions | 标准/定制机柜、OCP 机柜、预制化 power/cooling block、MegaMod、SmartRun | 很高。整柜/整列/模块化 AI factory 缩短施工周期 |
| Monitoring & Management | Environet、Vertiv Intelligence、360AI、OneCore、Waylay | 中高。AI 工厂需要 power-cooling-workload telemetry 和预测性维护 |
| Services | UPS/battery/thermal/rPDU/DC power/ERS 服务、液冷冲洗/过滤/调试 | 很高。液冷和高压电力的现场服务、认证、SLA 是重要壁垒 |

公司收入按地理区域披露，而不是按产品线披露。2026Q1 地区收入：Americas **$1.814B**，占 **68.5%**；APAC **$514M**，占 **19.4%**；EMEA **$321M**，占 **12.1%**。按产品/服务披露：Products **$2.091B**，占 **78.9%**；Services & spares **$558M**，占 **21.1%**。

### 1.2 投资人心中的 VRT

投资人通常把 VRT 看成三类资产的叠加：

| 认知标签 | 事实锚 | 含义 |
|---|---|---|
| AI 基建 picks-and-shovels | 2025Q4 organic orders +252%、backlog $15.0B；2026Q1 Americas organic sales +44.3% | 不直接卖 GPU，但卖 GPU 上电和散热所需基础设施 |
| 高增长工业科技股 | FY2025 organic sales +26.3%；FY2026 指引 organic +29%-31% | 增速已接近高成长科技硬件，而非传统工业个位数增长 |
| 订单可见度资产 | 2025Q4 backlog $15.0B，约为 FY2025 revenue 的 1.47x | 项目型收入可见度强，但也有项目延迟和取消风险 |
| 技术/认证壁垒股 | NVIDIA GB200/GB300 参考架构、800VDC 合作、4,000+ field service engineers | 通过 reference design 和服务网络提高客户替换成本 |
| 高估值高波动股 | Forward P/E 约 50x、52 周涨幅约 +256%、beta 2.10 | 对订单、毛利、AI capex 预期高度敏感 |

### 1.3 最近 3 年重大业务变化、转型、收购

| 时间 | 事件 | 战略意义 |
|---|---|---|
| 2023 起 | Giordano Albertazzi 任 CEO 后，聚焦执行、margin、AI 数据中心需求和全球产能 | 公司从传统关键基础设施供应商，被重新定价为 AI 数据中心基础设施核心受益者 |
| 2024 | 与 NVIDIA 发布/共研 GB200 NVL72 7MW 级 power/cooling 参考架构 | 从卖单品升级为参与 AI factory reference design |
| 2025-03 | 全球推出 Vertiv SmartRun，整合高密度 busbar、液冷管路、hot aisle containment 和网络基础设施 | 把现场 fit-out 转成预制化 overhead infrastructure |
| 2025-06 | 发布 NVIDIA GB300 NVL72 142kW power/cooling reference architecture 和 Omniverse SimReady 资产 | GB300/NVL72 上电、液冷、空间效率成为 VRT 直接卖点 |
| 2025-08 | 完成 Great Lakes Data Racks & Cabinets 收购，价格约 **$200M**，扩展机柜/集成白区能力 | 强化 high-density racks、custom cabinets、factory integration |
| 2025-08 | 收购 Waylay NV，AI/hyperautomation 软件平台 | 增强 AI-based monitoring、predictive services、performance optimization |
| 2025-12 | 完成 PurgeRite 收购，价格约 **$1.0B**，另有最高 $250M earn-out；约 10x 2026E EBITDA | 补强液冷冲洗、过滤、purging、commissioning 等服务，服务毛利高于公司平均 |
| 2026-03 | 宣布拟收购 ThermoKey S.p.A.，heat rejection / heat exchange | 补齐端到端 thermal chain，尤其 EMEA 制造能力 |
| 2026-04 | 收购 BMarko Structures | 增强北美 manufactured / prefabricated / converged infrastructure 结构件和工程控制 |
| 2026-04 | 收购 Strategic Thermal Labs | 增强 advanced liquid-cooling 系统能力，小但有技术期权 |
| 2025-11 至 2026H2 | 与 NVIDIA 推进 800VDC 平台设计，计划 2026H2 发布相关产品组合 | 2027 Rubin Ultra/Kyber、500kW-1MW rack 的高弹性期权 |

### 1.4 产业链位置

AI 数据中心链条可以简化为：电力接入/变电 -> UPS/BESS/配电 -> 白区机柜/母线/PDU -> AI server rack -> 液冷/CDU/heat rejection -> DCIM/运维服务。VRT 处在 IT 设备之外、但比传统 MEP 更靠近 AI rack 的位置。它不控制 GPU/HBM，但控制 “GPU 能不能按计划上架、上电、散热和稳定运行” 的一大部分工程链。

项目内行业研究给出的 2026-2027 美国/全球 AI 数据中心非 IT 基础设施中，电力链和液冷是先行订单池：电力设备包括 transformer/switchgear/busway/UPS/BESS，冷却包括 CDU、冷板、泵阀、heat rejection。VRT 同时覆盖 UPS/BESS、电能质量、机柜/母线/PDU、液冷、预制化模块和 DCIM/服务，综合度仅少数公司能匹敌，主要对手是 Schneider Electric、Eaton、ABB、Delta、Huawei、Siemens/Legrand/nVent 等。

## 2. 当前股价、估值、财务健康度

### 2.1 市场数据

数据源：[StockAnalysis VRT statistics](https://stockanalysis.com/stocks/vrt/statistics/)，截至 2026-05-08 美股收盘。

| 指标 | 数值 | 日期/口径 |
|---|---:|---|
| 股价 | **$339.97** | 2026-05-08 16:00 EDT 收盘 |
| 盘后价 | $341.50 | 2026-05-08 19:59 EDT |
| 市值 | **$130.59B** | 2026-05-08 |
| Enterprise Value | $131.35B | 2026-05-08 |
| TTM P/E | **85.44x** | TTM EPS $3.98 |
| Forward P/E | **49.96x** | StockAnalysis consensus |
| P/S | **12.04x** | TTM revenue $10.84B |
| Forward P/S | **8.99x** | consensus forward sales |
| TTM revenue | **$10.84B** | 最近 12 个月 |
| TTM net income | **$1.56B** | 最近 12 个月 |
| TTM gross margin | **37.15%** | 最近 12 个月 |
| TTM operating margin | **18.80%** | 最近 12 个月 |
| TTM net margin | **14.37%** | 最近 12 个月 |
| TTM FCF | **$2.28B** | FCF margin 21.04% |
| 52 周涨幅 | **+255.92%** | 2026-05-08 |
| Beta | 2.10 | 5 年 beta |

### 2.2 资产负债表健康度

| 指标 | 数值 | 判断 |
|---|---:|---|
| 2026Q1 cash + short-term investments | **$2.50B** | 流动性强 |
| 2026Q1 long-term debt, net | **$2.92B** | 债务可控 |
| StockAnalysis total debt | $3.26B | 含更广义债务口径 |
| Net cash / debt position | net debt 约 $0.76B | 低杠杆 |
| Company net leverage | **约 0.2x** | 2026Q1，公司披露 |
| Current ratio | **1.49x** | 健康 |
| Quick ratio | 1.06x | 健康但项目型营运资本仍重 |
| Debt / EBITDA | 1.30x | 健康 |
| Interest coverage | 27.88x | 利息压力很低 |
| 2026Q1 liquidity | **$5.0B** | 包括现金/短投/信贷 |
| 信用评级 | Moody's Baa3、S&P BBB- | 2026-02 首次投资级 |
| 资本结构动作 | 发行 $2.1B senior unsecured notes，设立 $2.5B revolver，并偿还 term loan / ABL | 提高期限和融资弹性 |

结论：资产负债表是强项。VRT 目前不是高杠杆周期股，反而是现金流和预收款改善的项目型成长股。2026Q1 deferred revenue 从 2025 年底 **$1.815B** 升至 **$2.462B**，一个季度增加 **$647M**，与大型项目预付款和 backlog 转化相互印证。主要财务风险不是偿债，而是高增长下的产能扩张、并购整合、项目固定价、关税/铜/钢/电池成本、以及应收和库存占用。

## 3. 最近五次财报：订单、收入、利润率、AI 数据中心占比

### 3.1 五季核心财务和订单表

| 财报季度 | 披露日 | 收入 / YoY / organic | 订单、BTB、Backlog | 毛利率 / 净利率 | Adj. operating profit / margin | 分区域收入和利润率 | Products / Services | AI 数据中心相关估算 |
|---|---:|---:|---|---:|---:|---|---|---|
| **2026Q1** | 2026-04-22 | **$2.650B**, +30.1%, organic +22.6% | Q1 未披露新 orders/backlog；Q4 backlog $15.0B 延续；deferred revenue QoQ +$647M；Q2 指引 $3.25B-$3.45B | **37.7% / 14.7%** | **$551M / 20.8%** | AMER $1.814B +53.1%, org +44.3%, margin 27.0%；APAC $514M +14.9%, margin 13.1%；EMEA $321M -20.3%, margin 16.6% | Products $2.091B +29.8%；Services $558M +31.4% | 公司未披露；估算 core data center 70%+，AI/high-density 35%-50%，Americas 是主引擎 |
| **2025Q4** | 2026-02-11 | **$2.880B**, +22.7%, organic +19.3% | Organic orders **+252% YoY**、+117% QoQ；TTM organic orders +81%；BTB **~2.9x**；backlog **$15.0B**, +109% YoY | **38.9% / 15.5%** | **$668M / 23.2%** | AMER $1.886B +50.2%, org +46.2%, margin 30.1%；APAC $492M -9.6%；EMEA $502M -8.2% | Products $2.309B +23.2%；Services $571M +21.0% | 极高。公司称 Americas 与 hyperscale/colocation data centers 是订单主驱动 |
| **2025Q3** | 2025-10-22 | **$2.676B**, +29.0%, organic +28.4% | Organic orders **+60% YoY**、+20% QoQ；TTM organic orders +21%；BTB **~1.4x**；backlog **$9.5B** | **37.8% / 14.9%** | **$596M / 22.3%** | AMER $1.712B +42.9%, org +43.0%, margin 29.3%；APAC $520M +20.2%；EMEA $444M +0.2% | Products $2.168B +34.2%；Services $508M +11.0% | 高。AI-driven infrastructure 被公司明确列为需求和 backlog 增长驱动 |
| **2025Q2** | 2025-07-30 | **$2.638B**, +35.1%, organic +34.0% | Organic orders **+15% YoY**、+11% QoQ；TTM organic orders +11%；BTB **~1.2x**；backlog **$8.5B** | **34.0% / 12.3%** | **$489M / 18.5%** | AMER $1.602B +42.9%, org +43.2%, margin 24.0%；APAC $560M +36.9%；EMEA $476M +12.5% | Products $2.119B +39.6%；Services $519M +19.2% | 高。收入超预期但 margin 受关税、供应链迁移和执行成本影响 |
| **2025Q1** | 2025-04-23 | **$2.036B**, +24.2%, organic +25.3% | Orders **+13% YoY**、+21% QoQ；TTM orders +20%；BTB **~1.4x**；backlog **$7.9B**, QoQ +10% | **33.7% / 8.1%** | **$337M / 16.5%** | AMER $1.185B +28.1%, org +28.8%, margin 21.9%；APAC $447M +34.6%；EMEA $404M +5.7% | Products $1.611B +30.2%；Services $425M +5.8% | 中高。公司提到 iGenius AI infrastructure、NVIDIA GB200/GB300 参考设计 |

资料来源：Vertiv [2026Q1 release](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx)、[2025Q4 release](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)、[2025Q3 release](https://investors.vertiv.com/news/news-details/2025/Vertiv-Reports-Strong-Third-Quarter-Results-including-Organic-Orders-60-Diluted-EPS-122-Adjusted-EPS-63-Raises-2025-Guidance/)、SEC [2025Q2 exhibit](https://www.sec.gov/Archives/edgar/data/1674101/000167410125000006/q22025exhibit991vrt7302025.htm)、SEC [2025Q1 exhibit](https://www.sec.gov/Archives/edgar/data/1674101/000162828025018915/q12025exhibit991vrt042325.htm)。

### 3.2 财报趋势解读

| 观察 | 含义 |
|---|---|
| Backlog 从 2025Q1 $7.9B -> Q2 $8.5B -> Q3 $9.5B -> Q4 $15.0B | Q4 出现阶跃式订单爆发，核心来自 Americas、hyperscale、colocation 和 AI infrastructure |
| Q1 2026 未披露新 backlog | 不能简单假设继续增长；但 deferred revenue 增至 $2.462B、Q2/FY 指引上调，说明大订单正在进入预收和交付 |
| Americas 2026Q1 收入占比 68.5%、organic +44.3% | 北美 AI 数据中心是公司业绩核心，区域集中度提高 |
| EMEA 2026Q1 -29.4% organic | 2025 重组/执行/项目时点影响仍在，管理层预计 2026H2 改善；也是 ThermoKey 等并购补位原因 |
| 产品收入增速持续快于服务，但 2026Q1 服务 +31.4% | PurgeRite/服务扩张开始进入收入；服务通常高于公司平均 margin，能增强周期韧性 |
| Adjusted op margin 从 Q2 18.5% -> Q3 22.3% -> Q4 23.2%，Q1 2026 20.8% | Q2 关税/供应链冲击后恢复；Q1 季节性和投资增加，全年指引 22.8%-23.8% |

## 4. 2026 最新指引、收入占比、重点业务与被跳过业务

### 4.1 2026 最新一次财报指引

2026Q1 后，公司上调全年指引：

| 指标 | 2026Q2 指引 | FY2026 指引 | 重点 |
|---|---:|---:|---|
| Net sales | **$3.25B-$3.45B** | **$13.50B-$14.00B** | FY 中点 $13.75B，同比 FY2025 $10.23B 增约 +34.4% |
| Organic sales growth | +20%-24% | **+29%-31%** | 高于 Q4 2025 初始 FY 指引 +27%-29% |
| Adjusted operating profit | $690M-$730M | **$3.14B-$3.26B** | FY 中点 $3.20B |
| Adjusted operating margin | 20.7%-21.7% | **22.8%-23.8%** | FY 中点约 23.3% |
| Adjusted diluted EPS | $1.37-$1.43 | **$6.30-$6.40** | FY 中点同比 +51% |
| Adjusted FCF | 未披露 | **$2.10B-$2.30B** | FCF conversion 很强 |

### 4.2 2026Q1 收入占比

| 维度 | 收入 | 占比 | 同比增长 | Organic 增长 | 结论 |
|---|---:|---:|---:|---:|---|
| Americas | $1.814B | **68.5%** | +53.1% | +44.3% | 最大、最快、利润率最高，是 AI hyperscale/colo 主战场 |
| APAC | $514M | 19.4% | +14.9% | +12.0% | 稳健增长，利润率 13.1% |
| EMEA | $321M | 12.1% | -20.3% | -29.4% | 短期拖累，管理层做重组和并购补强 |
| Products | $2.091B | **78.9%** | +29.8% | +24.9% | 高密电力/冷却/预制化硬件驱动 |
| Services & spares | $558M | 21.1% | +31.4% | +13.7% | 服务收入受并购和液冷调试需求推动 |

### 4.3 重点产品/业务与收入估算

公司不披露按产品线收入；下表是基于产品/服务口径、公司并购方向、订单/行业资料和 VRT FY2026 $13.75B 指引的估算。产品之间有套包和交叉，不能机械相加。

| 产品/业务 | 对应产品和型号/平台 | 当前收入贡献估算 | 增速估算 | 毛利/利润率判断 | 证据和交叉验证 |
|---|---|---:|---:|---|---|
| AI power train：UPS、配电、电能质量、PDU、busway、rack power | Liebert UPS、Trinergy UPS、EnergyCore Li-ion cabinet、PowerDirect in-rack DC power、rack PDU、PowerNexus/电力控制、static transfer switch | FY2026 revenue exposure **$5.0B-$6.0B**；AI 相关 $3.5B-$4.8B | +25%-45% | 产品 gross margin 30%-40%，系统/认证/服务 attach 后更高；公司级 adj op margin 23% 左右 | 2026Q1 Products +29.8%，Americas +53.1%；AI 数据中心必须先锁 UPS/配电，项目内行业研究把 UPS/BESS/电能质量列为高确定性订单池 |
| Thermal management / liquid cooling / heat rejection | Vertiv CoolChip CDU 70-1350kW、Liebert XDU、CoolLoop RDHx、CoolChip in-rack CDU、Fluid Network Rack Manifold、MegaMod CoolChip、ThermoKey heat rejection、STL 技术 | Thermal 总 exposure **$3.5B-$4.5B**；direct liquid cooling 子集 $1.2B-$2.0B | +35%-60%，direct liquid cooling 可能 +60%+ | CDU/冷板/泵阀/服务毛利 30%-50%；热管理服务更高 | NVIDIA GB300 142kW reference design、CoolChip CDU 产品页、PurgeRite/Strategic Thermal/ThermoKey 并购均指向端到端 thermal chain |
| Prefabricated / integrated infrastructure / racks | MegaMod HDX、MegaMod CoolChip、SmartRun overhead infrastructure、Great Lakes racks/cabinets、BMarko structures、OCP racks | FY2026 exposure **$1.8B-$2.8B** | +40%-70% | 模块化集成毛利 22%-35%；若含工程服务和认证可更高 | Great Lakes $200M 收购、BMarko 2026 收购、SmartRun 2025 launch；AI campus 需要缩短 time-to-capacity |
| Services / liquid cooling commissioning / ERS | PurgeRite flushing/purging/filtration、UPS/battery/thermal/rPDU services、Electrical Reliability Services | FY2026 服务收入 **$2.7B-$3.1B**，其中液冷服务快速上升 | +20%-35%；液冷 fluid management +60%+ | 服务 margin 通常高于公司平均；PurgeRite 被公司称为 margin accretive | 2026Q1 Services +31.4%；PurgeRite $1.0B 收购约 10x 2026E EBITDA |
| Software / DCIM / digital twin / AI ops | Environet、Vertiv Intelligence、360AI、OneCore、Waylay hyperautomation/genAI、SimReady assets | FY2026 单独可见收入 **$0.2B-$0.5B**，更多以 bundle 体现 | +40%-100%，小基数 | 纯软件高毛利，但实施服务稀释；硬件绑定提高 stickiness | Waylay 收购、NVIDIA Omniverse SimReady、360AI/OneCore |
| 800VDC / HVDC / rack-level DC/DC | Centralized rectifiers、DC busways、rack-level DC/DC converters、800VDC protection/service | 2026 revenue 可能 **<$0.2B-$0.4B**，主要为设计导入/样板 | 2026H2 起，2027 弹性最大 | 高压安全、固态保护、认证、服务可支撑较高溢价 | Vertiv/NVIDIA 800VDC readiness 称 2026H2 产品组合、对齐 2027 Rubin Ultra |

### 4.4 可以跳过或降低权重的业务

| 业务/产品 | 跳过原因 |
|---|---|
| 传统通信网络 DC power、部分 NetSure telecom 需求 | 相对成熟，增速低于 AI 数据中心，且受电信 capex 周期影响 |
| 低密企业机房、网络 closet、micro data center | 不是当前 VRT 订单爆发主因，价值量和紧迫性低 |
| 传统 KVM、serial console、低端 monitoring 单品 | 有现金流和客户基础，但不是 2026-2027 AI 增量核心 |
| 传统 CRAC/CRAH room cooling 的低密改造 | 存量仍有需求，但 AI 高密度正把价值转向 DTC、RDHx、CDU、heat rejection |
| VRLA 电池替换 | 仍存在，但 Li-ion UPS cabinet、BESS、grid-interactive UPS 更重要 |
| 普通机柜/钣金外壳 | 只有进入 OCP/AI rack、液冷/电力集成、预制化模块时才值得高权重 |

## 5. 高增长关键产品当前贡献、重要性、紧急性、供需和定价权

评分：1 低，5 高。收入为当前 12 个月或 FY2026 近似 run-rate 估算，存在产品交叉。

| 关键产品/业务 | 当前 VRT 收入贡献估算 | 当前收入增速 | AI 基建重要性 | 时间紧急性 | 供需紧张 | 垄断/认证能力 | 溢价能力 | 核心判断 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| UPS/配电/电能质量/power train | $5.0B-$6.0B | +25%-45% | 5 | 5 | 4 | 4 | 4 | 所有 AI 数据中心先锁电力，VRT 是第一梯队综合供应商 |
| 液冷/CDU/RDHx/thermal chain | $3.5B-$4.5B | +35%-60% | 5 | 5 | 5 | 4 | 5 | 100kW+ rack 把液冷变成交付条件，漏液风险和服务能力形成壁垒 |
| 预制化模块/AI factory blocks/racks | $1.8B-$2.8B | +40%-70% | 4 | 5 | 4 | 3.5 | 4 | time-to-power/time-to-token 变成客户 KPI，工厂集成价值上升 |
| Services/PurgeRite/ERS | $2.7B-$3.1B | +20%-35%；液冷服务更快 | 4 | 5 | 4 | 4 | 4.5 | 液冷冲洗、过滤、commissioning 是 AI rack 上线前置服务，且毛利好 |
| Software/360AI/Waylay/OneCore/DCIM | $0.2B-$0.5B | +40%-100% | 4 | 4 | 3 | 3.5 | 4 | 单独收入小，但决定硬件 bundle、预测维护和客户锁定 |
| 800VDC/HVDC | <$0.2B-$0.4B | 小基数高增长 | 5 for 2027 | 3 in 2026, 5 in 2027 | 4 | 4 | 5 | 2026 是 design-in，2027 Rubin Ultra/Kyber/1MW rack 才验证收入弹性 |

## 6. 一年后关键产品三情景预测

口径：从 2026-05 往后 12 个月，近似 2026H2-2027H1 revenue run-rate；不是公司指引。

| 产品/业务 | 情景 | 一年后收入贡献估算 | 增速 | AI 重要性 | 紧急性 | 供需紧张 | 垄断/认证 | 溢价能力 | 关键假设 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| UPS/配电/电能质量 | 基准 | $6.3B-$7.0B | +20%-30% | 5 | 5 | 4 | 4 | 4 | Q4 backlog 按计划转收入，BTB 1.1x+ |
| UPS/配电/电能质量 | 乐观 | $7.5B-$8.5B | +35%-50% | 5 | 5 | 5 | 4 | 4.5 | AI campus 并网和电力设备锁单继续前置 |
| UPS/配电/电能质量 | 极度乐观 | $9.0B-$10.5B | +60%+ | 5 | 5 | 5 | 4.5 | 5 | 大客户为交期支付溢价，UPS/BESS/Power block 供不应求 |
| 液冷/CDU/thermal chain | 基准 | $4.7B-$5.4B | +30%-45% | 5 | 5 | 5 | 4 | 5 | GB300/NVL72 批量交付，液冷 attach 继续上升 |
| 液冷/CDU/thermal chain | 乐观 | $5.8B-$7.0B | +55%-75% | 5 | 5 | 5 | 4.5 | 5 | GB300 + TPU/Trainium/Maia/MI350 同步拉动 |
| 液冷/CDU/thermal chain | 极度乐观 | $7.5B-$9.0B | +90%+ | 5 | 5 | 5 | 5 | 5 | 100kW+ rack 成为主流交付单元，CDU/服务持续缺口 |
| 预制化模块/racks | 基准 | $2.8B-$3.4B | +25%-45% | 4 | 5 | 4 | 3.5 | 4 | Great Lakes/BMarko/SmartRun 进入更多项目 |
| 预制化模块/racks | 乐观 | $3.8B-$4.8B | +60%+ | 4 | 5 | 5 | 4 | 4.5 | 工厂集成显著缩短现场施工，客户成套采购 |
| 预制化模块/racks | 极度乐观 | $5.5B-$7.0B | +100%+ | 5 | 5 | 5 | 4.5 | 5 | BYOP&C/AI factory blocks 成为大项目标准采购方式 |
| Services/PurgeRite/ERS | 基准 | $3.1B-$3.5B | +18%-28% | 4 | 5 | 4 | 4 | 4.5 | 服务 attach 随装机增长 |
| Services/PurgeRite/ERS | 乐观 | $3.7B-$4.3B | +35%-50% | 4 | 5 | 5 | 4.5 | 5 | 液冷 commissioning/过滤/维护成为瓶颈 |
| Services/PurgeRite/ERS | 极度乐观 | $4.7B-$5.5B | +70%+ | 5 | 5 | 5 | 5 | 5 | 客户把 uptime 和液冷责任外包给少数服务商 |
| Software/DCIM/360AI | 基准 | $0.5B-$0.7B | +40%-70% | 4 | 4 | 3 | 3.5 | 4 | 随硬件 bundle 增长 |
| Software/DCIM/360AI | 乐观 | $0.8B-$1.1B | +100%+ | 5 | 4 | 4 | 4 | 4.5 | DSX/Omniverse/Waylay 接入大型项目运维闭环 |
| Software/DCIM/360AI | 极度乐观 | $1.3B-$1.8B | +200%+ | 5 | 5 | 4 | 4.5 | 5 | AI 工厂按 MW/token 进行电热联合优化，软件单独收费提高 |
| 800VDC/HVDC | 基准 | $0.6B-$1.0B | 小基数多倍 | 5 | 4 | 4 | 4 | 5 | 2026H2 产品发布，2027H1 少数新建 AI factory 导入 |
| 800VDC/HVDC | 乐观 | $1.5B-$2.5B | 多倍 | 5 | 5 | 5 | 4.5 | 5 | Rubin/Rubin Ultra/Kyber 早期项目采用 800VDC |
| 800VDC/HVDC | 极度乐观 | $3.0B-$5.0B | 多倍 | 5 | 5 | 5 | 5 | 5 | 500kW-1MW rack 设计前置，VRT 进入客户标准架构 |

## 7. BOM、每 MW / 每 rack / 每 GPU / 每 optical port 价值量与价格传导

### 7.1 AI 数据中心每 MW 口径

口径：1MW IT load，不含 GPU/服务器/网络设备本体。不同项目差异极大，以下是高密 AI 项目可参考区间。

| 层级 | 主要内容 | 全市场典型价值量 / MW | VRT 可捕获内容 / MW | 价格传导 |
|---|---|---:|---:|---|
| 上游电力接入 | 变压器、中压开关柜、保护、E-house | $0.4M-$1.2M | $0.1M-$0.4M，取决于 VRT 是否做 power block | 铜、钢、变压器交期直接进入项目报价 |
| UPS/电池/电能质量 | MW 级 UPS、Li-ion cabinet、static switch、BMS | $0.5M-$1.2M | **$0.3M-$0.9M** | 电芯、功率半导体、铜排、关税可传导但有项目合同滞后 |
| 白区配电 | busway、rPDU、RPP、rack PDU、monitoring | $0.25M-$0.7M | **$0.15M-$0.45M** | 高密认证件供不应求时可溢价 |
| 液冷白区 | CDU、manifold、RDHx、冷板接口、泵阀、传感、漏液检测 | $0.5M-$1.8M | **$0.35M-$1.2M** | 泵阀、快接、铜/不锈钢、控制器，按 rack density 溢价 |
| Heat rejection / secondary loop | dry cooler、chiller、heat exchanger、cooling tower、pumps | $0.4M-$1.3M | $0.1M-$0.6M，ThermoKey 后提高 | 气候、水权和能效要求决定 ASP |
| 预制化模块和安装服务 | power/cooling block、SmartRun、工厂测试、现场调试 | $0.3M-$1.2M | **$0.2M-$0.8M** | 客户为工期缩短支付溢价 |
| 软件/运维 | DCIM、EPMS、BMS 接入、预测维护、SLA | $0.05M-$0.25M | $0.03M-$0.15M | 按 site/MW/device/SLA 收费 |
| **合计** | 传统高密 AI 非 IT 基础设施 | **$2.0M-$6.5M / MW** | **$1.1M-$4.5M / MW** | VRT 捕获率取决于是否提供成套 power+cold+service |

### 7.2 每 rack / 每 GPU / 每 optical port

以 NVIDIA GB300 NVL72 级别估算：单 rack 约 **142kW**，72 GPU。1MW 约对应 7 个 142kW rack。

| 口径 | VRT 内容量估算 | 解释 |
|---|---:|---|
| 每 142kW AI rack，直接 rack/白区内容 | **$150k-$450k / rack** | rack enclosure、rack PDU、busbar、in-rack CDU/歧管、RDHx、漏液检测、监控、现场服务 |
| 每 142kW AI rack，含上游 UPS/配电/heat rejection 分摊 | **$350k-$900k / rack** | 把 UPS、Li-ion、配电、二次侧冷却、预制化和服务按 rack 功率分摊 |
| 每 GPU，直接 rack/白区内容 | **$2.1k-$6.3k / GPU** | $150k-$450k / 72 GPU |
| 每 GPU，含上游设施分摊 | **$4.9k-$12.5k / GPU** | $350k-$900k / 72 GPU |
| 每 optical port | **VRT 光模块直接 BOM = $0**；间接设施分摊约 **$250-$2,000 / 800G port** | VRT 不卖光模块；若按每 GPU 4-8 个等效网络/光端口摊分，power/cooling/rack 成本形成间接 burden |
| 每 MW VRT 可捕获 | **$1.1M-$4.5M / MW** | 成套供应程度越高、液冷 attach 越高、预制化越多，越接近上沿 |

价格链条：GPU/AI 平台路线决定 rack density -> colo/hyperscaler 锁定机电方案 -> EPC/设计院把 power/cooling block 纳入招标 -> Vertiv 报价 UPS、PDU、CDU、RDHx、机柜、模块、软件、服务 -> 上游铜、钢、泵阀、功率半导体、电芯、控制器、钣金涨价通过项目报价和 escalator 部分传导。最大风险在 fixed-price contract 和关税变动：VRT 2025Q2 已经展示过关税和供应链迁移对 margin 的短期冲击。

### 7.3 当前产能能力、采纳程度、认证

| 产品/业务 | 当前产能能力，美元计 | 供应链采纳程度 | 重要认证/平台阶段 |
|---|---:|---|---|
| UPS/配电/power train | 2026 指引支撑公司总 revenue $13.5B-$14.0B；power train 估算 $5B-$6B | 高。hyperscale/colo 项目广泛采用第一梯队供应商 | UL/NFPA/AHJ、客户数据中心标准、UPS/电池安全认证；投资级评级有助于大项目履约担保 |
| CoolChip/XDU/CDU/液冷 | Thermal exposure $3.5B-$4.5B，direct liquid cooling 子集 $1.2B-$2.0B | 快速提高。GB300/NVL72 reference design、CoolChip CDU 产品化 | NVIDIA GB200/GB300 reference design；OCP/客户液冷规范；漏液/水质/流量/压差测试 |
| 预制化模块/racks | $1.8B-$2.8B exposure；Great Lakes、BMarko 加北美/欧洲制造能力 | 中高。AI 项目为缩短工期更愿意采用 | 客户工程验证、运输/现场安装/AHJ、OCP racks |
| Services/PurgeRite | $2.7B-$3.1B FY2026 服务收入 | 高。液冷 fluid management 是 commissioning 前置服务 | hyperscaler/Tier 1 colo 现场资质、安全培训、服务 SLA |
| Software/DCIM | $0.2B-$0.5B 显性收入，更多作为 bundle | 中。多数 hyperscaler 有自研系统，但需要设备 telemetry 和资产模型 | 网络安全、客户 IT/OT 集成、NVIDIA SimReady / Omniverse 资产 |
| 800VDC/HVDC | 2026 小量，估算 <$0.4B；产品组合计划 2026H2 | 早期。处于设计导入和样板阶段 | 高压 DC 安全、拉弧保护、固态断路、运维流程、NVIDIA 800VDC ecosystem |

### 7.4 一年后产能和认证情景

| 产品/业务 | 基准：一年后 | 乐观：一年后 | 极度乐观：一年后 |
|---|---|---|---|
| UPS/配电/power train | capacity/revenue $6.3B-$7.0B；客户采纳继续高；UL/AHJ 成熟 | $7.5B-$8.5B；新 capacity 被大客户锁定 | $9B+；电力 block 供不应求，客户预付款显著 |
| 液冷/CDU | $4.7B-$5.4B；GB300 量产认证稳定 | $5.8B-$7.0B；多平台 CDU/冷板/服务标准化 | $7.5B+；液冷成为高密 rack 默认，低质供应商出清 |
| 预制化模块/racks | $2.8B-$3.4B；Great Lakes/BMarko 整合完成 | $3.8B-$4.8B；AI factory blocks 成套交付 | $5.5B+；客户按整列/整舱采购 |
| Services/PurgeRite | $3.1B-$3.5B；服务 attach 稳步上升 | $3.7B-$4.3B；液冷冲洗/维护成为瓶颈 | $4.7B+；服务容量本身成稀缺资产 |
| Software/DCIM | $0.5B-$0.7B；软件更多 bundle | $0.8B-$1.1B；DSX/Waylay 接入更多项目 | $1.3B+；power-cooling-workload 闭环控制开始单独收费 |
| 800VDC/HVDC | $0.6B-$1.0B；少数客户 design-in | $1.5B-$2.5B；Rubin/Kyber 早期采用 | $3B+；500kW-1MW rack 项目前置，成为高端项目默认架构之一 |

## 8. 基于 backlog 和供给的未来一年公司增长预测

### 8.1 Backlog 和订单真实性

| 证据 | 含义 |
|---|---|
| 2025Q4 organic orders +252%，BTB ~2.9x，backlog $15.0B | 大项目真实下单，不只是 pipeline |
| 2025Q4 deferred revenue +$668M，2026Q1 deferred revenue 再 +$647M 至 $2.462B | 客户预付款/项目进度款上升，取消率应低于普通非约束 pipeline |
| 2026Q1 FY 指引上调至 $13.5B-$14.0B，Q2 指引 $3.25B-$3.45B | 管理层对 backlog 转收入有较高把握 |
| 2026Q1 capex $112.6M，远高于 2025Q1 $36.5M | 公司正在扩产以消化订单 |
| 风险披露明确提到 long sales cycles、customer order cancellation、failure to realize backlog、fixed-price contracts | backlog 不是无风险收入，项目延迟会影响季度节奏 |

### 8.2 未来一年公司整体增速三情景

| 情景 | 未来 12 个月收入 | 增速 | Adj. op margin | Backlog/BTB | 订单取消/延迟假设 | 产能约束 | 投资含义 |
|---|---:|---:|---:|---|---|---|---|
| 基准 | **$16.5B-$17.5B** | +20%-27% vs FY2026 guide midpoint annualized | 24%-25% | BTB 1.05x-1.20x；backlog $16B-$18B | 取消 5%-8%，更多是交付窗口后移 | CDU、服务技师、预制化工厂、功率件 | 股价需靠持续 beat/raise 支撑，估值仍不便宜 |
| 乐观 | **$18.5B-$20.5B** | +35%-49% | 25%-27% | BTB 1.25x-1.45x；backlog $20B-$24B | 取消 3%-6%，客户预付款上升 | 液冷/UPS/现场服务全面紧 | 估值可被高增长和 margin 扩张消化 |
| 极度乐观 | **$22B-$25B** | +60%-82% | 27%-29% | BTB 1.5x+；backlog $28B-$35B | 取消 <3%-5%，项目抢产能 | 800VDC、液冷、预制化、field service 全线供不应求 | VRT 成为 AI factory 标准供应商，收入曲线重估 |

我的基准判断偏向 **未来 12 个月 +20%-35%**，乐观情形可上探 +40% 以上。Q4 2025 的 $15B backlog 给 2026 已经提供强可见度，但 2027 增速要看新订单是否持续、GB300/Rubin/ASIC rack 是否顺利上电、以及 VRT 自身能否把收购和扩产变成交付能力。

## 9. 竞争格局、技术路线、替代风险和客户替换成本

### 9.1 竞争对手矩阵

| 领域 | VRT 主要对手 | VRT 相对优势 | VRT 风险 |
|---|---|---|---|
| UPS/critical power | Schneider/APC、Eaton、ABB、Delta、Huawei Digital Power、Socomec、Piller | 全球服务、数据中心经验、NVIDIA reference design、成套方案 | Schneider/Eaton/ABB 技术和客户关系同样强；Delta/Lite-On 在电源硬件上成本强 |
| 配电/PDU/busway/rack power | Schneider、Eaton、Legrand/Starline、nVent、Hubbell、ABB、Siemens、Panduit | power + cooling + rack 集成；服务网络 | Legrand/nVent 在白区配电和机柜生态强，Eaton 在 grid-to-chip 强 |
| 液冷/CDU/冷板/热管理 | Schneider/Motivair、CoolIT、Boyd/Eaton、Modine、nVent、Danfoss、STULZ、Delta、Asetek、LiquidStack、Submer | CoolChip/XDU、PurgeRite、ThermoKey/STL、NVIDIA GB300 reference | CoolIT/Boyd 在服务器冷板生态强；Schneider 通过 Motivair 补强 |
| 预制化模块 | Schneider、Eaton/Fibrebond、Compass、Flex、Jabil、Foxconn、Quanta/Wiwynn、PCX、TAS、Exyte | MegaMod、SmartRun、Great Lakes、BMarko，端到端方案 | ODM/EPC 可能向上延伸，客户可能多源采购 |
| DCIM/软件/数字孪生 | Schneider EcoStruxure/ETAP/AVEVA、Eaton Brightlayer、Siemens、ABB Ability、Sunbird、Nlyte、Hyperview、Phaidra、NVIDIA DSX | 硬件 telemetry + 服务绑定；Waylay/360AI | Hyperscaler 自研强，纯软件收入可能被压缩 |
| 800VDC/HVDC | Eaton、Schneider、ABB、Delta、Lite-On、Siemens、GE Vernova、Hitachi Energy、TI/ST/Infineon/Navitas 生态 | 800VDC 产品组合计划明确、NVIDIA 协同、服务能力 | 标准尚早，Delta/Lite-On 在 power rack/PSU 上 aggressive，ABB/Eaton 在高压保护强 |

### 9.2 VRT 新技术是否是未来主流

| 技术/产品 | 是否主流 | 判断 |
|---|---|---|
| 480/415VAC 到 UPS/配电，再到 48/54V rack power | 2026 主流 | 成熟、可认证、可大规模部署，GB300/B300 当年仍主要靠这一路线 |
| Direct-to-chip liquid cooling + CDU/RDHx | 2026-2027 主流 | 100kW+ AI rack 几乎不可绕开；浸没式会存在但不是 2026 主流 |
| 预制化 power/cooling blocks | 越来越主流 | 现场劳动力和调试成为瓶颈，工厂集成能缩短 time-to-capacity |
| 800VDC/HVDC | 2027 以后高端 AI factory 重要路线，但 2026 仍是试点/设计导入 | 若 rack 从 100kW 走向 300kW-1MW，800VDC 逻辑强；但 AHJ、安全、保护、维护和标准化决定节奏 |
| Software/digital twin/AI ops | 必需但 monetization 不确定 | 大型客户可能自研，但设备资产模型、telemetry 和服务 SLA 会给 VRT 绑定机会 |

### 9.3 替代方案和风险

| 风险/替代 | 对 VRT 的影响 |
|---|---|
| AI capex 或数据中心建设延期 | backlog 转收入延后，股价估值受压 |
| GPU/HBM/CoWoS 交付节奏低于预期 | rack power/cooling 延后，但已签电力/预制订单可能缓冲 |
| 800VDC 标准化慢 | 800VDC 收入弹性延后，但 48/54V 和传统 UPS 仍受益 |
| Schneider/Eaton/Delta 抢份额 | VRT 不是垄断，需靠 reference design、服务和产能守份额 |
| 客户自研/ODM 上延 | hyperscaler 可能把部分机柜/液冷/控制内化，压低供应商 margin |
| 液冷事故 | 漏液、过滤、水质、气泡、腐蚀会造成客户巨额损失，利好头部也会放大保修风险 |
| 固定价合同和关税 | 2025Q2 已出现 margin 压力；铜、钢、电芯、功率半导体和关税需传导 |
| 并购整合 | PurgeRite、Great Lakes、BMarko、ThermoKey、STL 需要整合成可复制交付能力 |

### 9.4 客户替换成本

VRT 的客户替换成本在高密 AI 项目中高于传统数据中心单品，原因是：

1. Reference design 绑定：GB200/GB300/NVL72 级别需要 power、cooling、rack、液冷控制同时验证，换供应商不是换一个部件。
2. 认证链长：客户、server OEM/ODM、colo、EPC、保险、AHJ、运维团队都要接受。
3. 现场服务网络：液冷冲洗、过滤、调试、UPS/battery 服务和紧急响应对 uptime 影响很大。
4. 项目风险大：一个漏液/跳闸事故可能造成百万美元级损失，客户愿意为已验证供应商付溢价。
5. 预付款和 backlog：deferred revenue 上升说明项目绑定和资金承诺增强。

但 VRT 没有绝对垄断。客户会多源采购 Schneider、Eaton、ABB、Delta、CoolIT、Boyd、nVent、Legrand、Rittal 等供应商，以避免单点风险。VRT 的超额收益来自 “组合能力和交付速度”，不是单点专利垄断。

## 10. 关键跟踪指标

| 指标 | 为什么重要 |
|---|---|
| 2026Q2/Q3 orders、book-to-bill、backlog 是否继续披露或继续增长 | 判断 Q4 2025 是否一次性大单，还是持续 AI 订单周期 |
| Americas organic growth 和 margin | 核心 AI hyperscale/colo 区域 |
| EMEA 是否在 2026H2 修复 | 决定全年 margin 和 ThermoKey/重组效果 |
| Services & spares 增速和 margin | PurgeRite 是否真正提升高毛利服务 |
| Capex、产能扩张和库存 | 判断能否把 backlog 转成收入 |
| Deferred revenue | 交叉验证订单质量、预付款和取消率 |
| NVIDIA GB300/Rubin、AMD MI400、TPU/Trainium/Maia 项目节奏 | 决定液冷和高密 power 的真实交付斜率 |
| 800VDC 产品发布、认证、客户试点 | 2027 弹性期权是否进入订单 |
| 关税/铜/钢/电芯/功率半导体成本 | 影响短期 gross margin |
| 大客户集中度和项目延期 | 估值最大的下行风险 |

## 11. 资料来源

- Vertiv IR：[2026Q1 earnings release](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx)
- Vertiv IR：[2025Q4 earnings release](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)
- Vertiv IR：[2025Q3 earnings release](https://investors.vertiv.com/news/news-details/2025/Vertiv-Reports-Strong-Third-Quarter-Results-including-Organic-Orders-60-Diluted-EPS-122-Adjusted-EPS-63-Raises-2025-Guidance/)
- SEC：[2025Q2 earnings exhibit](https://www.sec.gov/Archives/edgar/data/1674101/000167410125000006/q22025exhibit991vrt7302025.htm)
- SEC：[2025Q1 earnings exhibit](https://www.sec.gov/Archives/edgar/data/1674101/000162828025018915/q12025exhibit991vrt042325.htm)
- StockAnalysis：[VRT statistics and valuation](https://stockanalysis.com/stocks/vrt/statistics/)
- Vertiv：[Great Lakes acquisition](https://investors.vertiv.com/news/news-details/2025/Vertiv-Completes-Acquisition-of-Great-Lakes-Data-Racks--Cabinets/default.aspx)
- Vertiv：[PurgeRite acquisition](https://investors.vertiv.com/news/news-details/2025/Vertiv-Completes-Acquisition-of-PurgeRite-Expanding-Leadership-in-Liquid-Cooling-Services/default.aspx)
- Vertiv：[Waylay acquisition](https://investors.vertiv.com/financial-news/news-details/2025/Vertiv-Acquires-Generative-AI-Software-Leader-Waylay-NV-to-Enhance-Critical-Digital-Infrastructure-Operational-Intelligence-Optimization-and-Services/)
- Vertiv：[BMarko acquisition](https://investors.vertiv.com/news/news-details/2026/Vertiv-Acquires-BMarko-Structures-to-Expand-Capacity-for-Manufactured-and-Converged-Infrastructure-Solutions/default.aspx)
- Vertiv：[ThermoKey acquisition announcement](https://investors.vertiv.com/news/news-details/2026/Vertiv-to-Acquire-ThermoKey-Expanding-Heat-Rejection-Portfolio-for-Converged-Physical-Infrastructure/default.aspx)
- Vertiv：[Strategic Thermal Labs acquisition](https://investors.vertiv.com/news/news-details/2026/Vertiv-Strengthens-Liquid-Cooling-System-Capability-with-Acquisition-of-Strategic-Thermal-Labs/)
- Vertiv：[GB300 NVL72 142kW reference architecture](https://investors.vertiv.com/news/news-details/2025/Vertiv-Develops-Energy-Efficient-Cooling-and-Power-Reference-Architecture-for-the-NVIDIA-GB300-NVL72-Platform-Available-as-SimReady-Assets-in-NVIDIA-Omniverse-Blueprint-for-AI-Factory-Design-and-Operations/default.aspx)
- Vertiv：[800VDC readiness with NVIDIA](https://investors.vertiv.com/news/news-details/2025/From-Vision-to-Readiness-Vertiv-Collaborates-with-NVIDIA-to-Advance-800-VDC-Platform-Designs-to-Power-the-Next-Generation-of-AI-Factories/default.aspx)
- Vertiv：[MegaMod HDX modular liquid cooling infrastructure](https://investors.vertiv.com/news/news-details/2026/Vertiv-Introduces-New-Modular-Liquid-Cooling-Infrastructure-Solution-to-Support-High-Density-Compute-Requirements-in-North-America-and-EMEA/default.aspx)
- Vertiv：[CoolChip CDU product page](https://www.vertiv.com/en-us/products-catalog/thermal-management/high-density-solutions/liebert-xdu-x-treme-density-coolant-distribution-unit/)
- NVIDIA：[800 VDC Architecture](https://www.nvidia.com/en-us/data-center/technologies/800-vdc-architecture/)
- NVIDIA Developer Blog：[800V HVDC Architecture for AI factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)
- NVIDIA：[GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- OCP：[Open DC for AI](https://www.opencompute.org/projects/open-dc-for-ai)
- McKinsey：[The $7 trillion data center build-out](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-7-trillion-dollar-data-center-build-out-how-industrials-can-capture-their-share)
- 项目内行业资料：`行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`、`行业调研_AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-05-08.md`、`行业调研_机柜级供电与服务器电源架构_2026.md`、`行业调研_数据中心直液冷系统_2026.md`、`行业调研_数据中心土建_MEP与预制化交付_2026-05-08.md`、`行业调研_DCIM_能控与AI工厂数字孪生_2026-05-08.md`、`行业调研/AI头部芯片市场占比和规模.md`。


