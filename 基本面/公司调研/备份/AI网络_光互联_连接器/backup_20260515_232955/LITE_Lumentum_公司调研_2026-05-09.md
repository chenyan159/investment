# 公司：LITE Lumentum Holdings Inc.（Lumentum）

> 日期：2026-05-09。股票行情采用 2026-05-08/2026-05-09 最新可得交易数据；财务口径以 FY26Q3（截至 2026-03-28，2026-05-05 发布）为最新季度。  
> 说明：本文未参考本目录下其他“公司调研”文件；结合了项目内非公司调研目录的 AI 光互联、OFC 2026、800G/1.6T、CPO/OCI/OCS 行业资料，并用公司公告、SEC 文件、产品页、行业机构信息交叉验证。非公司直接披露的数据均标为“估算/推断”。非投资建议。

## 0. 核心结论

1. Lumentum 已从“周期性光通信/Apple 3D sensing/工业激光”公司，迅速转成投资人眼中的 **AI 光互联瓶颈供应商**：FY26Q3 收入 8.084 亿美元，同比 +90.1%，non-GAAP 毛利率 47.9%，non-GAAP 经营利润率 32.2%，主要由云与 AI 数据中心光器件、光模块、OCS/CPO 相关产品拉动。
2. 公司的强项不是普通模块组装，而是 **InP/EML/CW laser、narrow-linewidth laser、pump laser、OCS/MEMS、CPO/ELS、高速光模块系统**的垂直组合。NVIDIA 2026-03 宣布向 Lumentum 投资 20 亿美元，并给出多年、多十亿美元采购承诺和 advanced laser capacity access，说明激光/光器件已被 GPU 平台商视为战略约束。
3. 最新披露最硬的订单信号：FY26Q2 管理层称 **OCS backlog 已远超 4 亿美元**，CPO 获得 **增量数亿美元级订单**、交付窗口在 2027H1；FY26Q3 又称 OCS ramp 按计划推进，符合多年、多十亿美元采购协议，1.6T transceiver 将在 FY26Q4 ramp。
4. 财务健康度明显改善但估值极高：截至 FY26Q3，公司现金及短投 31.72 亿美元、总债务账面 32.82 亿美元，净债务接近中性；但大量可转债/优先股带来稀释。按最新价格约 903.80 美元、普通股 7,170 万股估算，普通股市值约 648 亿美元，TTM P/S 约 26x；完全稀释口径接近 870 亿美元。
5. 未来一年主要看四件事：1.6T 量产是否顺利、200G/400G EML 和 CW laser 是否继续短缺、OCS/CPO 订单能否按窗口兑现、以及 2027 供给扩散后 800G/1.6T ASP 是否下行过快。

## 1. 公司整体业务、定位与财务状态

### 1.1 业务概览与产业链位置

Lumentum 是光学和光子技术公司，总部位于 San Jose，产品覆盖高性能激光器、光通信组件、光模块/子系统、OCS 光路交换、3D sensing VCSEL、工业激光等。公司最新口径把收入按 **Components（组件）** 和 **Systems（系统）** 展示：

| 业务层级 | 代表产品 | AI 基建中的位置 | 投资含义 |
|---|---:|---|---|
| Components | 100G/200G/400G EML、InP CW laser、narrow-linewidth laser、pump laser、PD/TIA 相关光器件、VCSEL | 800G/1.6T 模块、coherent DCI、CPO/ELS、scale-up 光互联的上游核心物料 | 毛利和定价权通常高于普通模块，扩产慢，客户认证强 |
| Systems | 800G/1.6T transceivers、Cloud Light 模块资产、OCS 系统/子系统 | AI scale-out 网络和 Google/类 Google OCS 架构 | 收入弹性最大，但长期会受 ASP 和多供应商竞争影响 |
| Industrial / sensing legacy | 工业激光、3D sensing VCSEL、传统电信/低速产品 | 非 AI 或技术储备 | 低增长部分，本文只在其能迁移到 AI scale-up 时讨论 |

在 AI 产业链中，Lumentum 位于 **GPU/ASIC 平台商、交换芯片/网络设备商、云厂商与光模块供应链之间的光器件/光系统层**。它不是最大光模块出货商，但在高端 EML、CW laser、narrow-linewidth laser、OCS/MEMS 和 CPO external laser 方面具备更强壁垒。

### 1.2 投资人心中的公司形象

过去 Lumentum 常被看成光通信周期股，受电信资本开支、Apple/消费 3D sensing、工业激光周期影响，估值弹性有限。2025H2 到 2026H1 后，叙事变成：

- **AI optics pure-play**：收入增速由 AI 数据中心光互联驱动，FY26Q3 公司明确称 cloud and AI business 使公司总收入同比增长 90%+。
- **NVIDIA 战略供应链**：NVIDIA 20 亿美元投资、多年采购承诺和 capacity access 把 Lumentum 从普通供应商升级为 AI factory 光学基础设施战略伙伴。
- **从模块 beta 到上游瓶颈 alpha**：Cloud Light 带来模块能力，NeoPhotonics 带来 coherent/高速光器件，Lumentum 自身 InP/VCSEL/OCS 资产形成垂直整合。

### 1.3 最近三年重大变动/转型/收购

| 时间 | 事件 | 战略意义 |
|---|---|---|
| 2022-08 | 完成 NeoPhotonics 收购 | 扩展高速光通信、coherent、tunable/narrow-linewidth laser、100G+ 光器件能力 |
| 2023-11/12 | 完成 Cloud Light 收购 | 补齐面向 cloud datacenter 的高速 transceiver/AOC 能力，后续 FY26 Systems 收入高增的基础 |
| 2024-2025 | 整合 NeoPhotonics/Cloud Light，重组产线，转移部分受出口限制影响的产线 | 毛利率从 FY24 低谷恢复；提升非中国制造弹性和大客户可供性 |
| 2025-02 | Michael Hurlston 接任 CEO | 公司叙事更集中到 AI/cloud photonics、运营纪律和利润率扩张 |
| 2026-03 | NVIDIA 宣布向 Lumentum 投资 20 亿美元，并有多年、多十亿美元采购承诺 | 锁定 advanced laser components 产能；验证 Lumentum 在 CPO/硅光/AI optics 中的战略地位 |
| 2026-03 | 收购/启用 Greensboro, North Carolina 240,000 sqft 先进制造 facility，计划 mid-2028 ramp、400+ jobs | 建设美国本土 6-inch InP/先进激光产能，解决中长期 CPO/laser/AI datacenter 供给瓶颈 |

### 1.4 最新估值与经营指标

| 指标 | 最新值 | 日期/口径 | 备注 |
|---|---:|---|---|
| 股价 | 约 903.80 美元 | 2026-05-08 最新交易/盘后口径 | 2026-05-09 为周六，无常规交易 |
| 市值 | 约 648 亿美元 | 903.80 美元 x FY26Q3 common shares 71.7m | 普通股市值口径 |
| 完全稀释权益价值 | 约 869 亿美元 | 行情工具口径，接近 Q3 diluted shares 96.2m | 可转债/优先股稀释使口径差异很大 |
| TTM 收入 | 24.884 亿美元 | FY25Q4-FY26Q3 | 480.7+533.8+665.5+808.4 |
| TTM 收入增速 | 约 +68.9% | 与 FY24Q4-FY25Q3 14.726 亿美元比较 | 最新季度收入同比 +90.1% |
| PE | 约 163x | 最新行情工具口径 | GAAP TTM EPS 受稀释/一次性项影响 |
| Forward PE | 约 56x；按 FY26Q4 指引年化约 77x | consensus/行情站；FY26Q4 midpoint EPS 2.95 x4 | 市场在给 FY27/FY28 AI optics 成长溢价 |
| P/S | 约 26.0x 普通股口径；约 34.9x 完全稀释口径 | TTM revenue 24.884 亿美元 | 对订单兑现高度敏感 |
| FY26Q3 GAAP / non-GAAP 毛利率 | 44.2% / 47.9% | 2026-03-28 quarter | 环比 non-GAAP GM +540 bps |
| TTM GAAP / non-GAAP 毛利率 | 约 37.7% / 42.7% | 自算 | mix 转向 laser chips/AI optics 后扩张 |
| TTM GAAP / non-GAAP 净利率 | 约 17.7% / 20.9% | 自算 | GAAP Q4 FY25 含较多非经营因素，non-GAAP 更稳 |

### 1.5 资产负债表健康度

| 项目 | FY26Q3 | 评价 |
|---|---:|---|
| 现金及短期投资 | 31.723 亿美元 | NVIDIA 20 亿美元优先股投资后流动性大幅改善 |
| 总资产 | 70.279 亿美元 | 较 FY25 年末 42.187 亿美元上升 |
| 总负债 | 40.545 亿美元 | 其中可转债按当前负债重分类是主要表观压力 |
| 总债务账面 | 32.818 亿美元 | convertible notes 31.834 亿美元 + Japan term loans 0.984 亿美元 |
| 净债务 | 约 1.095 亿美元 | cash+ST investments 与账面 debt 基本相抵 |
| 流动比率 | 1.14x | 当前负债包含大量可转债；剔除 current converts 后运营流动性较强 |
| 9M FY26 经营现金流 | 3.884 亿美元 | 利润恢复，库存/应收增长消耗部分现金 |
| 库存 | 6.328 亿美元，较 FY25 年末 +34.6% | 支持高增长需求，也意味着若客户延期会有库存风险 |
| Purchase obligations | 17.956 亿美元 | 10-Q 披露，主要为库存和运营采购；但 open PO 通常可取消/重排，不能直接等同 backlog |
| 资本开支/产能 | PPE net 9.643 亿美元，CIP 2.484 亿美元 | 正在为 InP/laser/AI optics 扩产 |

结论：财务健康度从 FY24/FY25 初期的“高债务+周期低谷”修复为“高现金+高订单+高稀释”。短期偿债压力可控，核心风险不在破产式流动性，而在 **估值、稀释、库存、订单兑现、ASP 下行**。

## 2. 最新及最近四次财报对比

公司从 FY26 开始用 Components/Systems 产品类型披露；FY25 仍主要用 Cloud & Networking / Industrial Tech 分部。因此下表把原始披露口径保留，并对 AI 数据中心占比做估算。

| 财报 | 期间 / 发布日 | 收入 / 增速 | 毛利率 / 经营利润率 | 业务收入 | 订单、backlog、交期与取消率 | AI 数据中心收入占比（估算） | 关键解读 |
|---|---|---:|---|---|---|---:|---|
| FY26Q3 | 截至 2026-03-28 / 2026-05-05 | 8.084 亿美元；QoQ +21.5%，YoY +90.1% | GAAP GM 44.2%，non-GAAP GM 47.9%；non-GAAP OPM 32.2% | Components 5.333 亿美元，占 66.0%，YoY +77.3%；Systems 2.751 亿美元，占 34.0%，YoY +121.1% | 1.6T transceivers 将在 FY26Q4 ramp；OCS ramp on track，符合多年、多十亿美元采购协议；200G EML 收入 QoQ 翻倍以上；取消率未披露，行业交期/认证仍紧 | 80-90% | 公司进入 AI optics 加速段；margin 扩张来自 laser chips、scale-across components、价格纪律和产品 mix |
| FY26Q2 | 截至 2025-12-27 / 2026-02-03 | 6.655 亿美元；QoQ +24.7%，YoY +65.5% | GAAP GM 36.1%，non-GAAP GM 42.5%；non-GAAP OPM 25.2% | Components 4.437 亿美元，占 66.7%，YoY +68.3%；Systems 2.218 亿美元，占 33.3%，YoY +60.1% | OCS backlog “well beyond $400M”；CPO 获增量数亿美元订单，交付在 CY2027H1；推断 book-to-bill >1 | 75-85% | Q2 是市场重估点：AI 增长从 800G/EML 扩展到 OCS/CPO |
| FY26Q1 | 截至 2025-09-27 / 2025-11-04 | 5.338 亿美元；QoQ +11.0%，YoY +58.4% | GAAP GM 34.0%，non-GAAP GM 39.4%；non-GAAP OPM 18.7% | Components 3.792 亿美元，占 71.0%，YoY +63.9%；Systems 1.546 亿美元，占 29.0%，YoY +46.5% | 未披露 backlog；管理层称 revenue/OPM/EPS 均达指引高端；库存和现金上升支持需求 | 70-80% | 800G、EML、cloud datacenter 需求持续；Cloud Light 整合进入贡献期 |
| FY25Q4 | 截至 2025-06-28 / 2025-08-12 | 4.807 亿美元；QoQ +13.1%，YoY +55.9% | GAAP GM 33.3%，non-GAAP GM 37.8%；non-GAAP OPM 15.0% | Cloud & Networking 4.241 亿美元，占 88.2%，YoY +66.5%；Industrial Tech 0.566 亿美元，占 11.8%，YoY +5.6% | 未披露 backlog；公司称 AI DC cloud portfolio 需求强，EML chips、pump lasers、narrow linewidth laser assemblies、800G modules 表现强 | 65-75% | 从恢复期进入加速期；管理层当时预期 FY26Q4 或更早季度收入超过 6 亿美元，实际 FY26Q2 已超过 |
| FY25Q3 | 截至 2025-03-29 / 2025-05-06 | 4.252 亿美元；QoQ +5.7%，YoY +16.0% | GAAP GM 28.8%，non-GAAP GM 35.2%；non-GAAP OPM 10.8% | Cloud & Networking 3.652 亿美元，占 85.9%，YoY +16.4%；Industrial Tech 0.600 亿美元，占 14.1%，YoY +13.9% | 未披露 backlog；Q4 指引 4.40-4.70 亿美元；云客户需求强、networking market 恢复 | 55-65% | AI 需求已显现，但还未进入 FY26 的 OCS/CPO/1.6T 订单重估阶段 |

## 3. 2026 最新指引、业务占比与产品拆解

### 3.1 FY26Q4 指引

| 项目 | FY26Q3 实际 | FY26Q4 指引 | 含义 |
|---|---:|---:|---|
| 收入 | 8.084 亿美元 | 9.60-10.10 亿美元，中点 9.85 亿美元 | QoQ 中点 +21.9%，若兑现为历史新高 |
| non-GAAP operating margin | 32.2% | 35.0-36.0% | mix、定价和规模效应继续上行 |
| non-GAAP EPS | 2.37 美元 | 2.85-3.05 美元 | diluted shares 指引约 102m，稀释继续上升 |

按 FY26Q3 披露，业务收入占比为 Components 66.0%、Systems 34.0%。增长最突出的不是低速传统通信，而是：

- Components：100G/200G EML 出货创新高；200G EML 收入 QoQ 翻倍以上；DCI narrow-linewidth lasers 连续 9 个季度环比增长，YoY +120%+；scale-across/subsea pump lasers YoY +80%；CPO UHP lasers 按计划在 CY2026 exit 时贡献 meaningful revenue。
- Systems：cloud transceiver shipments 创纪录，QoQ +40%+；1.6T transceivers FY26Q4 ramp，开始整合 internal CW lasers；OCS ramp on track。

### 3.2 产品、收入、利润率与增长交叉验证

| 产品/业务 | 对应产品/型号 | 当前收入贡献（估算） | 增速/利润率判断 | 交叉验证 |
|---|---|---:|---|---|
| 800G/1.6T cloud transceivers | 800G OSFP/QSFP-DD；1.6T 2xDR4 TRO OSFP；1.6T DR4 OSFP with 400G differential EML demo | FY26Q3 Systems 2.751 亿美元，其中大部分为 cloud transceiver/OCS；估算 AI transceiver 2.0-2.5 亿美元/季 | Systems YoY +121.1%；1.6T 早期毛利估算 35-45%，FY26Q4 开始更高 mix | Lumentum 1.6T TRO OSFP：8 electrical + 8 optical lanes at 212.5G PAM4，1.6Tbps，500m，typical 16W；OFC 展示 4x400G differential EML DR4 |
| EML / InP / CW laser | 100G/200G EML；400G differential EML；CW laser for SiPh；SHP/UHP laser | FY26Q3 Components 5.333 亿美元，AI/datacenter components 估算 3.8-4.8 亿美元/季 | 200G EML QoQ >2x；组件毛利高于公司平均，估算 45-65% | TrendForce 指出 EML/CW-LD 是 AI 光模块扩产瓶颈；Lumentum non-GAAP GM 47.9% 说明 mix 强 |
| OCS / MEMS optical circuit switching | OCS systems、MEMS mirrors、OCS-optimized transceivers | backlog >4 亿美元；FY26Q3 收入已 ramp 但未单列，估算数千万到 1 亿美元/季级别 | 多年多十亿美元采购协议；毛利估算 35-55%，随系统/软件/服务 mix 变化 | TrendForce 称 Google Apollo OCS 约 100W vs 传统 switch 约 3000W，且 Lumentum 对 OCS/MEMS capacity 影响 rollout |
| CPO / ELS / UHP laser | 1310nm SHP laser；16-channel DWDM UHP laser；ELSFP；CPO laser source | 当前收入小，但 CPO 订单数亿美元、CY2026 exit meaningful revenue | 早期 ELS/laser 毛利估算 50-70%；系统级 CPO 取决于可靠性服务成本 | NVIDIA/Broadcom/Coherent/Lumentum 在 OFC 2026 推 CPO/CPX/NPO；NVIDIA 采购承诺验证战略性 |
| DCI scale-across components | narrow-linewidth laser assemblies；pump lasers；coherent DCI 光器件 | FY26Q3 Components 的重要利润来源，估算 1.0-1.8 亿美元/季 | narrow linewidth laser YoY +120%+，pump lasers YoY +80%；毛利估算 45-60% | AI campus/region scale-across 拉动 800ZR/1600ZR/ZR+ 和 line system |
| 1060nm VCSEL scale-up | 1060nm VCSEL array co-packaged with host ASIC；fan-out wafer-level package | 当前几乎无规模收入，属于 2027-2028 期权 | 若进入 optical scale-up，毛利估算 45-65%；短期为 design-in/qualification | OFC 2026 demo：>150C 高温、>10B emitters 3DS 制造基础，目标 UCIe/PCIe slow-and-wide scale-up |
| 3.2T / 400G-per-lane | 400G differential EML；未来 3.2T stepping stone | 当前样品/验证，收入很小 | 2027 后潜在高毛利器件；良率和测试卡点 | Broadcom Taurus、Coherent 400G-lane、OpenLight 3.2T PIC 等说明路线进入 qual |

### 3.3 可跳过的低优先级业务

本文不重点展开以下业务，因为短期 AI 数据中心弹性较弱，或收入增速/估值贡献较低：

- 传统 Industrial Tech 工业激光，用于一般材料加工、传统制造周期。
- 消费 3D sensing / Apple 类 VCSEL 存量业务。注意：其 1060nm VCSEL 量产基础可迁移到 AI scale-up，因此“消费应用”跳过，“VCSEL scale-up”保留。
- 传统低速电信/legacy transceiver 与非 AI access 产品。
- 非 AI sensing、普通工业测量和成熟光通信备件。

## 4. 高增长/关键产品当前贡献与战略评分

评分：5 = 极强/极紧/极高；1 = 弱。

| 产品/业务 | 当前收入贡献（美元） | 当前增速 | AI 技术栈重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价能力 | 解释 |
|---|---:|---:|---:|---:|---:|---:|---|
| 800G/1.6T transceivers | FY26Q3 AI transceiver/相关 Systems 估算 2.0-2.5 亿美元/季；FY26Q4 随 1.6T ramp 可能 3.0 亿美元+/季 | Systems YoY +121.1%，cloud transceiver shipment QoQ +40%+ | 5 | 5 | 4 | 3 | AI scale-out 必需；模块竞争者多，Lumentum 优势来自 Cloud Light + 自有 laser |
| 200G/400G EML / InP / CW laser | FY26Q3 AI/datacenter components 估算 3.8-4.8 亿美元/季 | 200G EML revenue QoQ >2x；Components YoY +77.3% | 5 | 5 | 5 | 5 | 1.6T、CPO、SiPh 都需要高质量光源；扩产慢、认证强 |
| OCS / MEMS | backlog >4 亿美元；当前收入未单列，估算数千万到 1 亿美元/季 | backlog 和 ramp 指向高双位数到三位数增长 | 4 | 4 | 4 | 4 | Google/TPU 类架构最直接；平台依赖强，供应商少 |
| CPO / ELS / UHP laser | 当前小，但 CPO 订单数亿美元；CY2026 exit meaningful revenue | 低基数高增长 | 5 | 4 | 5 | 5 | 2026 是 pilot/qual，2027 高端 switch 可能放量；ELS 是 CPO 可维护性核心 |
| DCI narrow-linewidth / pump lasers | 估算 1.0-1.8 亿美元/季 | narrow linewidth +120% YoY，pump +80% YoY | 4 | 4 | 4 | 4 | AI scale-across 需要 coherent DCI/line systems；技术壁垒高 |
| 1060nm VCSEL scale-up | 规模收入几乎为零 | 研发/样品阶段 | 3 | 2 | 3 | 4 | 若 optical scale-up 替代部分铜，价值大；但 2026 收入不可过度资本化 |
| 3.2T/400G-lane EML | 当前小 | 样品/qual | 4 | 3 | 4 | 4 | 2027-2028 产品周期；现在是 design win 窗口 |

## 5. 一年后收入贡献情景预测

口径：预测未来 12 个月内各业务对 Lumentum 的收入贡献，不是市场总规模。基准假设 FY26Q4 指引兑现，FY27 1.6T/OCS/CPO 按公司交付窗口推进；乐观假设大客户提前锁货；极度乐观假设 1.6T、OCS、CPO/ELS、AI DCI 同时供不应求且 ASP 保持。

| 产品/业务 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| 800G/1.6T transceivers | 年收入 18-25 亿美元；增速 +70-110%；AI 重要性 5，供需 4，溢价 3 | 28-38 亿美元；+120-170%；1.6T 成新增集群主力，供需 5，溢价 4 | 45-60 亿美元；+200%+；1.6T 长期短缺，客户给预付款/价格保护 |
| EML/InP/CW laser | 年收入 20-28 亿美元；+50-80%；供需 5，溢价 5 | 32-42 亿美元；+90-130%；200G/400G EML 和 CW laser 成共同瓶颈 | 50 亿美元+；+150%+；CPO/SiPh/1.6T/3.2T 同时抢产能 |
| OCS/MEMS | 年收入 4-8 亿美元；backlog 消化；供需 4，溢价 4 | 10-15 亿美元；Google/TPU-like 架构扩展，供需 5 | 20 亿美元+；OCS 从单一生态扩散到更多 ASIC/GPU fabric |
| CPO/ELS/UHP laser | 年收入 3-7 亿美元；CY2026 exit meaningful revenue，CY2027H1 交付 | 10-18 亿美元；数亿美元订单后续追加，进入多个 high-end switch qual | 25 亿美元+；CPO/CPX/NPO 成 2027 高端 switch 默认路线之一 |
| DCI narrow-linewidth / pump | 年收入 7-10 亿美元；+40-70% | 12-16 亿美元；+80-120%，AI campus/region DCI 拉动 | 20 亿美元+；1600ZR/ZR+ 与 multi-rail line system 提前放量 |
| 1060nm VCSEL scale-up | <0.5 亿美元，主要 NRE/sample | 1-2.5 亿美元，进入 1-2 个客户 design-in | 5 亿美元+，若 optical scale-up 在 XPU/GPU 机架中提前商用 |
| 3.2T/400G-lane | <1 亿美元，样品/qual | 2-5 亿美元，器件小批量 | 10 亿美元+，若 204.8T switch 和 3.2T 模块提前 |

公司总收入未来 12 个月情景：

| 情景 | 未来 12 个月收入 | 增速 vs 当前 TTM 24.9 亿美元 | non-GAAP GM | 主要条件 |
|---|---:|---:|---:|---|
| 基准 | 46-52 亿美元 | +85-110% | 45-50% | FY26Q4 指引兑现，1.6T ramp 顺利，OCS/CPO 逐季释放 |
| 乐观 | 58-67 亿美元 | +130-170% | 50-54% | 大客户锁货、OCS backlog 转收入、CPO/ELS 提前 |
| 极度乐观 | 80-95 亿美元 | +220-280% | 52-58% | 1.6T、CPO、OCS、AI DCI 同时缺货，ASP 高位维持 |

## 6. BOM、内容量、价格传导与当前产能/认证

### 6.1 内容量估算假设

- 高端 AI rack：约 72 GPUs/XPU，功率 100-120kW；1MW 约 8-10 rack、600-720 GPUs。
- 每 GPU scale-out 端口：2026 主流按 1-2 个 800G/1.6T 等效端口估算；考虑 switch-to-switch/fabric overhead 后，1MW 高端集群约需要 1,500-4,000 个 1.6T 模块端点，或 3,000-7,000 个 800G 模块端点。
- 1 条光链路需要两个模块端点；下表“每 optical port”以一个模块端点或一个 1.6T equivalent port 计。
- ASP 为工程估算：800G module 约 500-900 美元；1.6T module 早期约 1,400-2,000 美元；CPO/ELS/OCS 因系统形态差异大，只给区间。

| 产品/业务 | BOM 拆分 | 每 optical port 内容量 | 每 rack 内容量 | 每 MW 内容量 | 价格传导链 | 当前产能能力与采纳/认证 |
|---|---|---:|---:|---:|---|---|
| 1.6T OSFP / 800G transceiver | DSP/retimer 20-30%；EML/SiPh/CW/PD 25-40%；driver/TIA 10-15%；PCB/connector/thermal 10-15%；assembly/test/yield 15-25% | 若卖整模块：1.6T 约 1,400-2,000 美元；若只供 Lumentum 光器件：150-600 美元 | 约 150-500 个模块端点/rack，价值 20-100 万美元；Lumentum 可捕获 3-25 万美元 | 约 1,500-4,000 个 1.6T 端点，系统光模块价值 200-800 万美元；Lumentum share 30-200 万美元 | 云厂年度框架价 -> 模块厂 -> EML/CW/DSP/测试；短缺时上游先涨价，供给扩散后模块 ASP 先被压 | FY26Q3 Systems 2.751 亿美元；1.6T FY26Q4 ramp；客户认证通常 6-18 个月，Lumentum 已在 lead pack |
| 200G/400G EML / InP / CW laser | 外延/晶圆 25-35%；fab process 20-30%；封装/TEC/isolator 20-30%；测试老化 15-25% | 每 1.6T 模块 4x400G differential EML 或 8x200G lane/CW/SiPh 路线；Lumentum 内容量 150-600 美元 | 若 150-500 个端点/rack，laser/EML 内容量 2-30 万美元/rack | 30-240 万美元/MW，取决于 Lumentum share 和 1.6T attach | 上游短缺 -> 模块厂成本上涨 -> 云厂接受 premium/长期容量承诺 | Components FY26Q3 5.333 亿美元；200G EML 收入 QoQ >2x；Greensboro 240k sqft InP fab mid-2028 ramp，短期仍靠现有/外包/扩线 |
| OCS/MEMS | MEMS mirror/optical switch fabric 25-40%；fiber management 20-30%；control electronics/software 10-20%；test/service 15-25% | OCS 系统按 port 估算 100-500 美元，不含外部 optical modules | Google/TPU-like rack 需要更高光纤/模块密度；OCS 按 pod/cluster 配置，不是每 rack 固定 | 按大型集群分摊，Lumentum 内容量估算 10-80 万美元/MW，极端 OCS 架构更高 | 云厂/平台商直接采购 OCS 系统或关键 MEMS；节能/可重构性定价，而非按零件成本 | FY26Q2 OCS backlog >4 亿美元；FY26Q3 ramp on track；TrendForce 指 Lumentum capacity 影响 Apollo OCS rollout |
| CPO/ELS/UHP/SHP laser | PIC/engine 25-35%；EIC/driver/TIA 20-30%；ELS/laser/fiber 15-25%；socket/connector/thermal/test 20-35% | ELS/laser 约 200-800 美元/1.6T equivalent port；102.4T switch 约 2-8 万美元 laser/ELS 内容量 | 高端 switch rack 若 1-4 台 102.4T/204.8T switch，Lumentum 内容量约 2-30 万美元/rack | 约 20-250 万美元/MW，取决于 CPO switch attach | Switch ASIC/系统商打包给云厂；客户按 watts/port、可靠性和可维护性付费 | CPO 增量数亿美元订单，CY2027H1 交付；UHP lasers 计划 CY2026 exit 有 meaningful revenue；标准/现场维护仍在 qual |
| DCI narrow-linewidth / pump lasers | narrow-linewidth tunable laser、modulator/receiver、pump laser、amplifier/line system coupling、test/calibration | 每 coherent module/line card Lumentum 内容量约 100-700 美元 | 与 AI campus fiber-pair 数相关，不按 GPU 线性；128+ fiber pairs/rack 的 scale-across 会放大 | 约 5-50 万美元/MW，跨园区训练/推理越多越高 | Ciena/Nokia/Cisco/Marvell/云厂 DCI 方案 -> laser/pump 供应商 | narrow-linewidth lasers 连续 9 季增长、YoY +120%+；pump lasers YoY +80%；认证偏运营商级，周期长但粘性强 |
| 1060nm VCSEL scale-up | VCSEL/PD array 25-40%；driver/TIA 20-30%；fan-out wafer-level package 20-30%；multimode fiber/connector/test 10-20% | 早期每 GPU/ASIC package 20-150 美元，若 scale-up 光化可至 100-500 美元 | 72 GPU rack 约 1,500-36,000 美元早期；全面 optical scale-up 后可 1-5 万美元+ | 1-50 万美元/MW，取决于是否进入 rack-scale optical I/O | XPU/GPU package 设计 -> advanced packaging -> VCSEL array；客户按功耗/密度/热可靠性付费 | OFC 2026 demo；>10B 3DS emitters 制造经验；处于 design-in/技术验证，不应计入 2026 大收入 |

### 6.2 一年后产能/采纳/认证情景

| 产品/业务 | 当前产能/采纳 | 基准（1 年） | 乐观（1 年） | 极度乐观（1 年） |
|---|---|---|---|---|
| 1.6T/800G transceivers | Q3 Systems 年化 11 亿美元；1.6T Q4 ramp | 年化 22-28 亿美元，2-3 个核心 hyperscaler 批量 | 年化 35-45 亿美元，多客户 1.6T qual 通过 | 年化 55 亿美元+，1.6T 缺货延续、客户预付款锁产能 |
| EML/InP/CW laser | 200G EML QoQ >2x；现有 InP 产能紧 | 年化 25-32 亿美元，产能利用率高 | 年化 40 亿美元+，CPO/SiPh 同时拉货 | 年化 55 亿美元+，6-inch InP 扩产前持续稀缺 |
| OCS/MEMS | backlog >4 亿美元；单一/少数大客户为主 | backlog 转收入 4-8 亿美元 | 多客户/多 pod 复制，10-15 亿美元 | OCS 扩散到更多 AI ASIC/GPU fabric，20 亿美元+ |
| CPO/ELS | 订单数亿美元，2026 exit meaningful revenue | CY2027H1 交付，收入 3-7 亿美元 | 多个 switch ASIC 平台 design-in，10-18 亿美元 | CPO/CPX 成高端 switch 默认路线，25 亿美元+ |
| DCI lasers/pumps | +80% 到 +120% YoY 子产品增长 | 年化 7-10 亿美元 | 年化 12-16 亿美元 | 年化 20 亿美元+ |
| VCSEL scale-up | OFC demo，未量产 | NRE/sample，小于 0.5 亿美元 | 1-2 个客户 design-in，1-2.5 亿美元 | 大客户 rack optical scale-up 小批量，5 亿美元+ |

## 7. 基于 backlog、供给与订单的未来一年业务增速预测

公司不披露完整 backlog/bookings/back-to-bill。可验证线索如下：

- OCS backlog：FY26Q2 明确 “well beyond $400M”。
- CPO：FY26Q2 获增量数亿美元订单，交付 CY2027H1。
- NVIDIA：2026-03 20 亿美元投资 + multibillion purchase commitment + capacity access rights。
- FY26Q3 采购义务：17.956 亿美元，库存 6.328 亿美元，均说明公司在为需求扩张备货；但 10-Q 也说明 open purchase orders 通常可取消、重排或调整，不能机械等同 firm backlog。
- FY26Q4 指引中点 9.85 亿美元，相当于年化收入 39.4 亿美元，已高于当前 TTM 24.9 亿美元很多。

| 情景 | 收入预测 | 订单/供给假设 | 取消/延期风险 | 结论 |
|---|---:|---|---|---|
| 基准 | 未来 12 个月 46-52 亿美元；公司 YoY +85-110% | 1.6T ramp 正常，OCS backlog 按期转收入，CPO 2027H1 开始交付；EML/CW 仍紧但可扩 | 低到中；客户项目强，但数据中心上电/电力/HBM/网络验证可能造成季度波动 | 高增长兑现，估值仍要求 FY27 继续加速 |
| 乐观 | 58-67 亿美元；+130-170% | NVIDIA/云厂提前锁定 laser/ELS；OCS 多客户复制；1.6T ASP 下降慢 | 中；供应链扩产和客户集中是主要约束 | 毛利率可能继续高于 50%，股价能维持 AI scarcity premium |
| 极度乐观 | 80-95 亿美元；+220-280% | 1.6T、CPO/ELS、OCS、AI DCI 同时缺货；客户支付预付款/长约锁产能 | 中高；任何上电延迟或客户架构转向都会造成估值回撤 | 需要极强 AI capex 与供应执行，属于高 beta 上沿 |

## 8. 竞争格局、技术路线与替代风险

| 产品/业务 | 主要竞争对手 | Lumentum 竞争力 | 替代/风险 | 客户替换成本 |
|---|---|---|---|---|
| 800G/1.6T transceivers | Coherent、Innolight/中际旭创、Eoptolink/新易盛、AOI、Accelink、Hisense、Fabrinet/Jabil 生态 | Cloud Light 模块能力 + 自有 laser/EML；北美战略供应链属性 | 中国供应商价格竞争；800G ASP 下行；1.6T 多供后毛利回归 | 中高。客户 qual、firmware/CMIS、热设计、RMA 数据会锁定，但模块仍可多供 |
| EML/InP/CW laser | Coherent、Mitsubishi、Sumitomo、Furukawa、Broadcom/MACOM、AOI/Source Photonics、中国 InP 追赶者 | 高端 EML/CW/laser 深厚；NVIDIA 投资验证先进 laser 价值 | 400G-lane 路线改变、SiPh/PIC 集成、客户自研；InP 扩产执行 | 高。进入 AVL 后替换需重跑可靠性、温漂、BER、老化 |
| OCS/MEMS | Google Apollo 内部生态、Coherent、Calient、Telescent、HUBER+SUHNER Polatis、Molex/iPronics 等 | 公开信息显示 Lumentum 在 Google OCS/MEMS 供应链关键 | OCS 未扩散、传统 switch/CPO 方案分流、云厂自研压价 | 很高。OCS 是架构级组件，一旦进入 fabric，替换牵涉调度、fiber management、运维 |
| CPO/ELS | Coherent、Broadcom/NVIDIA 平台、Marvell、Ciena/Nubis、OpenLight、Ayar、Lightmatter、GF、Eoptolink NPO/XPO | UHP/SHP laser、ELS、InP/CW 供应强；有 NVIDIA 长约 | CPO field service 不达标；XPO/高密 pluggable 延长；ASIC 厂捕获更多利润 | 高。CPO/ELS 绑定 switch ASIC、热设计、光纤路由、现场维护 |
| DCI lasers/pumps | Coherent、Furukawa、Mitsubishi、Ciena、Nokia/Infinera、Cisco/Acacia 生态 | NeoPhotonics 资产 + narrow-linewidth/pump laser 增长强 | 相干 DSP/系统商垂直整合；AI campus DCI 建设延期 | 高。运营商级可靠性与长周期认证提高粘性 |
| VCSEL scale-up | Coherent、Broadcom/VCSEL 生态、Ayar/Lightmatter/Celestial optical I/O、SiPh/TFLN 方案 | >10B emitters 制造经验，1060nm 高温/可靠性优势 | 铜/AEC 足够便宜；SiPh/ELS 路线占优；光 scale-up 标准碎片化 | 早期中，量产后高。package-level design-in 一旦确定很难换 |

### 8.1 这些技术会成为未来主流吗？

- **1.6T pluggable：主流概率高。** 2026 是导入/短缺，2027 大概率成为新增高端 AI fabric 主力。风险是 2027 多供应商进入后 ASP 下行。
- **EML/CW/SiPh 并行：不会单一路线通吃。** 1.6T/3.2T 会按 reach、功耗、良率和客户偏好并行采用 EML、CW laser + SiPh、VCSEL、LRO/TRO/LPO。
- **OCS：在 Google/TPU 架构中确定性高，向其他云厂扩散仍需验证。** 若 OCS 扩散，Lumentum 的 MEMS/OCS 系统价值会被显著重估。
- **CPO/CPX/NPO：长期重要，2026 收入不宜过度前置。** CPO 的瓶颈是可维护性、laser redundancy、field service；CPX/socketed CPO/NPO 比全封闭 CPO 更可能先商业化。
- **VCSEL optical scale-up：小而不能漏。** 1060nm VCSEL 有热可靠性和量产基础，但 2026 仍是样品/设计导入，真正收入窗口更可能在 2027-2028。

## 9. 关键跟踪指标

1. FY26Q4 revenue 是否达到 9.60-10.10 亿美元，non-GAAP OPM 是否进入 35-36%。
2. 1.6T transceiver ramp：出货客户数、良率、ASP、是否整合 internal CW lasers。
3. 200G/400G EML：收入是否继续 QoQ 大幅增长，是否出现供应缓解导致价格下行。
4. OCS backlog：>4 亿美元 backlog 转收入速度、是否新增非 Google/非单一客户订单。
5. CPO/ELS：数亿美元订单是否按 2027H1 交付，CY2026 exit meaningful revenue 是否兑现。
6. NVIDIA 长约细节：采购产品类别、容量 access、优先股/可转债稀释。
7. Greensboro InP fab：改造进度、capex、mid-2028 ramp 是否提前或延后。
8. 库存与采购义务：库存继续上升是需求备货还是客户延期。
9. 竞争 ASP：Innolight/Eoptolink/Coherent/AOI 1.6T 产能是否压低模块毛利。
10. AI 数据中心外部约束：电力、液冷、HBM/CoWoS、GPU 上电节奏决定 optics 订单节奏。

## 10. 资料来源

公司与 SEC：

- Lumentum FY26Q3 results（2026-05-05）：https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- Lumentum FY26Q3 earnings presentation：https://s21.q4cdn.com/377324469/files/doc_financials/2026/q3/Q3-FY26-Earnings-Presentation_final.pdf
- Lumentum FY26Q3 Form 10-Q：https://www.sec.gov/Archives/edgar/data/1633978/000162828026030777/lite-20260328.htm
- Lumentum FY26Q2 results：https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- Lumentum FY26Q1 results：https://investor.lumentum.com/financial-news-releases/news-details/2025/Lumentum-Announces-First-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- Lumentum FY25Q4/FY2025 results：https://investor.lumentum.com/financial-news-releases/news-details/2025/Lumentum-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2025-Results/default.aspx
- Lumentum FY25Q3 results：https://investor.lumentum.com/financial-news-releases/news-details/2025/Lumentum-Announces-Fiscal-Third-Quarter-2025-Financial-Results/default.aspx
- Lumentum FY2025 Form 10-K：https://www.sec.gov/Archives/edgar/data/1633978/000162828025040830/lite-20250628.htm
- NVIDIA-Lumentum strategic partnership：https://nvidianews.nvidia.com/_gallery/download_pdf/69a58a513d6332d72ae626bb/
- Lumentum OFC 2026 event page：https://www.lumentum.com/en/events/ofc-2026
- Lumentum 1.6T 2xDR4 TRO OSFP product page：https://www.lumentum.com/products/16t-2dr4-tro-osfp-transceiver-module
- Lumentum VCSEL scale-up OFC 2026 release：https://s21.q4cdn.com/377324469/files/doc_news/Lumentum-Showcases-Breakthrough-Optical-Scale-Up-Demonstration-at-OFC-2026-Using-VCSEL-Technology-2026.pdf
- Greensboro facility local report：https://www.wfdd.org/development/2026-03-26/data-center-technology-manufacturer-coming-to-greensboro

行业与会议：

- TrendForce：800G+ optical transceiver share >60% by 2026, Google OCS/Ironwood：https://www.trendforce.com/presscenter/news/20260210-12919.html
- TrendForce：2026 AI 光收发模块市场 260 亿美元，EML/CW-LD 瓶颈：https://www.trendforce.cn/presscenter/news/20260420-13018.html
- Cignal AI：2025 optical component revenue nearly $25B：https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/
- OFC 2026 official release：https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-opens-next-week-in-los-angeles-with-sold-out-exhibition-as-ai-driven-network-demand-fuels/

项目内行业资料（非“公司调研”目录）：

- `D:\drive\Investment\工作台v5\行业调研_AI网络_光互联_铜互联\行业调研_800G_1.6T可插拔光模块_2026-05-08.md`
- `D:\drive\Investment\工作台v5\行业调研_AI网络_光互联_铜互联\行业调研_激光器_EML与光器件_2026-05-08.md`
- `D:\drive\Investment\工作台v5\行业调研_AI网络_光互联_铜互联\行业调研_CPO_NPO与交换侧光引擎_2026-05-08.md`
- `D:\drive\Investment\工作台v5\行业调研_AI网络_光互联_铜互联\行业调研_OCI_OpenCPX_XPO_2026-05-08.md`
- `D:\drive\Investment\工作台v5\conference_update\ofc_2026_conference_update.md`
- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\行业调研\行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`

