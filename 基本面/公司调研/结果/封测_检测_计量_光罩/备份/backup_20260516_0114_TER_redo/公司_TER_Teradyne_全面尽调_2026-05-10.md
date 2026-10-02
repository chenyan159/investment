# 公司：TER Teradyne, Inc. 全面尽调

报告日期：2026-05-10  
市场数据口径：美股最新可得收盘价为 2026-05-08；财务数据以 Teradyne 2026Q1 财报、2026Q1 10-Q、2025 10-K、2025Q4 财报为主。  
重要口径说明：Teradyne 不披露传统意义的 backlog / bookings 明细，报告中的订单、产能、BOM 含量和未来一年分产品预测均明确区分“公司披露事实”和“基于订单线索、交付窗口、AI产业链资料的推断”。

## 0. 结论摘要

Teradyne 是 AI 硬件链里“从晶圆到数据中心”的测试平台公司，传统标签是半导体 ATE 龙头之一，过去投资人更多把它看成与 Advantest 竞争的周期性测试设备公司，外加一个尚未充分证明利润弹性的 Robotics 业务。2025-2026 年，市场对 TER 的认知发生了明显迁移：它从“手机/汽车/工业 SoC + 内存测试 + 协作机器人”公司，重新定价为“AI GPU/ASIC、HBM、224G/光互连、硅光/CPO、AI服务器板级测试”的数据中心测试设备平台。

最新财报显示迁移已经落到收入：2026Q1 收入 12.82 亿美元，同比 +87%，其中约 70% 与 AI 需求相关；Semiconductor Test 收入 11.11 亿美元，占总收入 86.6%。公司给 2026Q2 指引收入 11.5-12.5 亿美元，并称 2026 上半年预计占全年收入 55%-60%，隐含 2026 全年收入大约 41-45 亿美元。这个强度显著高于 2025 年 31.90 亿美元收入。

核心增量排序：

| 优先级 | 业务/产品 | 当前证据 | 投资含义 |
|---:|---|---|---|
| 1 | AI compute / networking SoC ATE：UltraFLEXplus、UltraPHY 112G/224G、IG-XL、TestInsight | 2026Q1 SoC 收入 8.82 亿美元，SoC 产品收入约 75% 来自 compute；Q1 获得 merchant GPU 多系统生产测试订单，2026 年已有约 5000 万美元 GPU 收入可见性 | 最直接的 AI GPU/ASIC 测试 beta；估值核心 |
| 2 | HBM / DRAM 测试：Magnum 7 / Magnum 7H | 2026Q1 Memory 收入 2.02 亿美元，同比约 +85%；2025 全年 Memory 5.05 亿美元；公司目标 2028 Memory 16 亿美元、约 50% 份额 | HBM3E/HBM4 扩产、KGD 良率和测试时长提升带来高弹性 |
| 3 | 硅光 / CPO / 光电混合测试：Photon 100、Quantifi Photonics | 2026 年发布 Photon 100；Quantifi 2025 年收购；公司称中期可扩展 TAM 3-7 亿美元/年 | 仍早期，但若 CPO/光引擎进入 HVM，是第二曲线 |
| 4 | AI服务器板级/高速互连测试：Omnyx、MLTP | 2026 年发布 Omnyx；2026 年与 MultiLane 成立 MLTP，面向 AI data center 高速数据连接 | 从芯片测试延伸到 rack/system 级测试，收入规模还需验证 |
| 5 | IST / SLT：Titan HP、企业 SSD/HDD、AI accelerator system-level test | 2025 IST 收入 1.29 亿美元，同比 +52%；2025 年已有 AI compute SLT 进入客户接受/量产推进 | 单位测试时间长、客户粘性高，但 TER 披露粒度低 |
| 6 | Robotics 中的 AI 应用 | 2026Q1 Robotics 收入 9126 万美元，同比 +32%；AI 应用约占 Robotics 15% | 对 TER 总估值不是主驱动，但若大客户 PoR 落地可改善亏损拖累 |

最大风险也很清楚：TER 当前股价已按 AI 测试稀缺资产重估，2026-05-08 收盘价 359.77 美元、市值约 563 亿美元、TTM PE 约 66.8x、forward PE 约 53.7x、P/S 约 14.9x。估值要求 AI compute/HBM 测试需求在 2026H2-2027 继续扩散，而不是只在 2026H1 提前拉货。公司自己也提示 H1 预计占全年 55%-60%，这意味着 H2 环比可能下降或至少增速放缓，订单可见性虽强但节奏可能很“块状”。

## 1. 整体业务、投资人心智、产业链位置与财务健康

### 1.1 公司业务概览

Teradyne 设计、开发并销售自动化测试设备和先进机器人系统。2025 年公司把业务披露为三大板块：

| 板块 | 2025 收入 | 2025 占比 | 2026Q1 收入 | 2026Q1 占比 | 主要产品/客户 |
|---|---:|---:|---:|---:|---|
| Semiconductor Test | 25.24 亿美元 | 79.1% | 11.11 亿美元 | 86.6% | SoC ATE、Memory ATE、IST/SLT；客户为 IDM、fabless、foundry、OSAT、封测厂和大型 AI/半导体客户 |
| Product Test | 3.58 亿美元 | 11.2% | 0.80 亿美元 | 6.3% | PCB/系统级测试、无线测试、硅光/PIC 测试、国防航天电子测试 |
| Robotics | 3.08 亿美元 | 9.7% | 0.91 亿美元 | 7.1% | Universal Robots 协作机器人、MiR AMR/移动机器人 |
| 合计 | 31.90 亿美元 | 100% | 12.82 亿美元 | 100% | 2026Q1 约 70% 收入与 AI 相关 |

Semiconductor Test 内部再分为 SoC、Memory、IST 三类。2026Q1 细分收入为：SoC 8.82 亿美元、Memory 2.02 亿美元、IST 2654 万美元。SoC 是最大业务，AI compute/networking 是当前最强增量；Memory 的关键是 HBM/DRAM；IST 包含 system-level test、HDD/SSD 等。

### 1.2 投资人心中的 TER 是什么公司

历史上，投资人对 TER 的定位是：

| 阶段 | 市场标签 | 估值核心变量 |
|---|---|---|
| 2019-2022 | 高端 SoC ATE + 手机/汽车/工业测试 + Robotics 可选成长 | 手机 SoC、汽车半导体、工业周期、机器人利润率 |
| 2023-2024 | 半导体设备下行周期中的测试设备龙头，AI 早期受益但不确定 | AI accelerator / HBM 测试能否抵消移动和工业疲弱 |
| 2025-2026 | AI 数据中心测试平台，从 wafer 到 package/board/system/optical | AI compute SoC、HBM、224G/硅光/CPO、AI服务器板级测试、订单持续性 |

2026Q1 的变化非常关键：公司明确说约 70% 收入与 AI 需求相关，且强项不只在一个单点，而是贯穿 wafer sort、final test、HBM、SLT、board test、silicon photonics、data center interconnect。投资人现在买的不是单一设备周期，而是 AI 基建复杂度上升带来的“测试强度提升”。

### 1.3 最近 3 年重大业务变动、转型和收购

| 时间 | 事件 | 战略意义 |
|---|---|---|
| 2024-05 | 以约 5.24 亿欧元投资 Technoprobe 10% 股权 | 与探针卡/探针接口核心供应链绑定，强化 wafer probe 生态；2026Q1 该投资公允价值约 10.68 亿美元 |
| 2024-2025 | AI compute 成为 SoC 业务最大组成 | 2023 年 compute 只约占 SoC 产品收入 10%；2025 年 compute 接近 SoC 产品收入 50%，2026Q1 进一步升至约 75% |
| 2025-01 | 收购 Infineon 自动化测试设备技术团队/资产，约 1830 万美元 | 强化功率/汽车/工业及 Infineon 关系；数据中心电源半导体测试是 AI 基建间接受益点 |
| 2025-03 | Product Test 成为新披露分部 | 将生产板测、国防航天、无线、硅光/PIC 测试整合，利于承接 AI server board 与 optical test |
| 2025-05 | 收购 Quantifi Photonics，约 1.272 亿美元 | 获得 PIC / 硅光测试能力，补齐电-光自动化测试 |
| 2025-08 | 发布 Magnum 7H HBM 测试平台 | 面向 HBM，高并行度与高功率 pins，用于降低 HBM 成本测试 |
| 2025-09 | UltraFLEXplus 推出 UltraPHY 224G | 面向 224G PAM4、PCIe Gen7、OIF CEI-224G、UCIe/CXL、硅光等下一代接口 |
| 2026-01 | 与 MultiLane 宣布成立 MLTP JV | 面向 AI 数据中心高速 I/O 和互连测试，Teradyne 为多数股东 |
| 2026-03 | 发布 Photon 100 | 面向硅光和 CPO 的 wafer、optical engine、module 测试 |
| 2026-03 | 发布 Omnyx | 面向 AI 时代的 board test，补充从芯片到系统的测试链条 |
| 2026-04 | 收购 TestInsight，约 2900 万美元 | 强化半导体测试开发、验证、转换软件，缩短 AI/数据中心芯片 time-to-market |

### 1.4 产业链位置

TER 在 AI 硬件产业链中的位置不是芯片供应商，也不是制造设备中的 litho/etch/deposition，而是“电性/功能/可靠性验证与量产测试”。

价格传导链条：

```text
Hyperscaler / AI芯片公司 / 网络芯片公司
        ↓ 指定质量、良率、吞吐、接口标准和量产节奏
Foundry / OSAT / IDM / ODM / EMS / test house
        ↓ 购买 ATE、probe/final test、SLT、board test、optical test、rack/system test
Teradyne / Advantest / Keysight / Cohu / Chroma / 其他测试厂商
        ↓ 测试设备折旧、耗材、接口板、软件和服务进入芯片/板卡/模块 COGS
AI GPU / ASIC / HBM / 光模块 / 交换机 / 服务器 / rack / 数据中心
```

AI 基建中，测试的重要性上升有四个原因：

1. AI accelerator 芯片面积大、功耗高、chiplet/HBM 封装复杂，测试时间和测试覆盖率上升。
2. HBM3E/HBM4 需要 known-good-die / known-good-stack，KGD 良率风险高，测试不能省。
3. 112G/224G/未来 448G 高速接口、UCIe/CXL/PCIe/以太网/硅光/CPO 需要 PHY、BER、jitter、FEC、温漂、眼图等验证。
4. AI server/rack 价值极高，field failure 成本巨大，SLT、burn-in、board test 和 system-level test 相当于“高价值硬件的保险”。

### 1.5 最新估值、股价和财务指标

| 指标 | 最新值 | 日期/口径 | 备注 |
|---|---:|---|---|
| 股价 | 359.77 美元 | 2026-05-08 收盘 | StockAnalysis / finance 数据 |
| 市值 | 563.2 亿美元 | 2026-05-08 | 约 1.565 亿股 |
| 企业价值 EV | 560.1 亿美元 | 2026-05-08 | 净现金小，EV 接近市值 |
| TTM 收入 | 37.9 亿美元 | 截至 2026Q1 | 2025 全年 + 2026Q1 - 2025Q1 |
| TTM 净利润 | 8.54 亿美元 | 截至 2026Q1 | GAAP |
| TTM EPS | 5.39 美元 | 截至 2026Q1 | GAAP |
| PE | 66.8x | 2026-05-08 / TTM | 高度反映 AI 成长预期 |
| Forward PE | 53.7x | 2026-05-08 | 市场一致预期口径 |
| PS | 14.9x | 2026-05-08 / TTM | 对测试设备公司属非常高位 |
| EV/Sales | 14.8x | 2026-05-08 / TTM | 与 P/S 接近 |
| 毛利率 | 58.7% | TTM | 2026Q1 GAAP gross margin 60.9% |
| 营业利润率 | 27.2% | TTM | 2026Q1 GAAP op margin 36.9%，non-GAAP 37.5% |
| 净利率 | 22.6% | TTM | 2026Q1 单季 GAAP 净利率 31.1% |
| 最新季度收入增速 | +87% YoY / +18% QoQ | 2026Q1 | 主要由 AI compute、networking、memory 驱动 |
| 2025 全年收入增速 | +13.1% YoY | 2025 | 31.90 亿美元 vs 2024 年 28.20 亿美元 |

估值判断：当前 TER 已不是低估的周期股，而是高预期的 AI 基建测试稀缺资产。若 2026 全年收入落在 41-45 亿美元，当前 P/S 约 12.5-13.7x；若公司在 2027 前后提前接近 Analyst Day 中的 60 亿美元收入模型，P/S 约 9.4x。但若 2026H2 订单消化、AI capex 放缓或 Advantest 抢份额，当前估值对回撤很敏感。

### 1.6 资产负债表与财务健康程度

| 项目 | 2026Q1 | 2025 年末 | 变化/解读 |
|---|---:|---:|---|
| 现金及等价物 | 2.42 亿美元 | 2.94 亿美元 | Q1 偿还 2 亿美元 revolver 后现金下降 |
| 短期+长期有价证券 | 1.52 亿美元 | 1.55 亿美元 | 稳定 |
| 现金+有价证券 | 3.94 亿美元 | 4.48 亿美元 | 仍有较好流动性 |
| 应收账款 | 11.08 亿美元 | 7.87 亿美元 | Q1 出货强、收入快速放大导致 A/R 上升 |
| 存货 | 3.63 亿美元 | 3.80 亿美元 | 收入大幅增长但存货下降，说明周转改善 |
| 总资产 | 44.34 亿美元 | 41.84 亿美元 | 资产负债表扩张 |
| 短期债务 | 0 | 2.00 亿美元 | Q1 已还清 |
| 总负债 | 12.90 亿美元 | 13.88 亿美元 | 杠杆低 |
| 股东权益 | 31.44 亿美元 | 27.96 亿美元 | Q1 盈利推升 |
| 流动比率 | 2.15x | 1.75x | 健康 |
| 2026Q1 经营现金流 | 2.65 亿美元 | 单季 | 尽管 A/R 增加 3.22 亿美元，仍正向 |
| Q1 后收购/投资现金支出 | 约 1.67 亿美元 | 2026 年 4 月 | MLTP JV + TestInsight，使用 revolver 资金 |

财务健康结论：健康。公司短债在 Q1 末清零，现金+证券 3.94 亿美元，流动比率 2.15x；还有 7.5 亿美元 revolver。主要观察点是应收账款快速上升，2026Q1 A/R 达 11.08 亿美元，约等于季度收入的 86%，说明强出货带来营运资本压力，也可能反映大客户集中和晚季出货。不是偿债风险，但会影响 FCF 节奏。

## 2. 最新和最近 4 次财报：关键数字、订单/交期、业务收入、AI占比

### 2.1 五个季度总表

| 财报季度 | 收入 | YoY / QoQ | Non-GAAP EPS | GAAP GM / Non-GAAP GM | GAAP/Non-GAAP营业利润率 | Semiconductor Test | Product Test | Robotics | AI相关收入占比 | 订单/交期/取消率线索 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2026Q1 | 12.82 亿美元 | +87% / +18% | 2.56 美元 | 60.9% / 约 60.9% | 36.9% / 37.5% | 11.11 亿美元 | 0.80 亿美元 | 0.91 亿美元 | 约 70% | UltraFLEXplus 过去 9 个月出货翻倍仍维持 12-16 周 lead time；Q1 获得首个 merchant GPU 多系统生产测试订单，预计 Q2 安装量产，2026 约 5000 万美元收入可见 |
| 2025Q4 | 10.83 亿美元 | +44% / +41% | 1.80 美元 | 57.2% | GAAP 27.1% / non-GAAP 约 29.0% | 8.83 亿美元 | 1.10 亿美元 | 0.89 亿美元 | >60% | AI compute、networking、memory 强；全年 2026H1 预计反季节性强，占全年较高比例 |
| 2025Q3 | 7.69 亿美元 | 约 +5% / +18% | 0.85 美元 | 58.5% | non-GAAP 20.4% | 6.06 亿美元 | 0.88 亿美元 | 0.75 亿美元 | 40%-50% | Memory 环比翻倍以上；Q4 指引强，说明 HBM/AI SoC 订单拉动已确认 |
| 2025Q2 | 6.52 亿美元 | 约 -11% / -5% | 0.57 美元 | 57.3% | non-GAAP 15.1% | 4.92 亿美元 | 0.85 亿美元 | 0.75 亿美元 | 未披露，显著低于 H2 | Q1 后客户因贸易/关税不确定有 pushout 和资本审查；公司称未见取消；Q2 AI compute forecast 开始转成订单 |
| 2025Q1 | 6.86 亿美元 | +14% / -9% | 0.75 美元 | 60.6% | non-GAAP 20.5% | 5.43 亿美元 | 0.74 亿美元 | 0.69 亿美元 | 未披露 | Q1 移动 SoC 强；HBM 客户消化 2024 产能；获得 HBM4 performance test win 和首个 AI compute SLT 收入 |

### 2.2 五个季度细分收入和增长

单位：百万美元。部分 2025Q4 细分由 2025 全年披露值减去前三季度计算，和公司电话会披露的 SoC/Memory 近似值一致。

| 财报季度 | SoC | SoC 变化 | Memory | Memory 变化 | IST | IST 变化 | Product Test | Product Test 变化 | Robotics | Robotics 变化 | 备注 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2026Q1 | 881.8 | +117% YoY / +36% QoQ | 202.5 | +85% YoY / -2% QoQ | 26.5 | -1% YoY / -11% QoQ | 80.4 | +8% YoY / -27% QoQ | 91.3 | +32% YoY / +2% QoQ | SoC 约 75% 来自 compute，Memory 由 HBM/DRAM 驱动 |
| 2025Q4 | 646.7 | +47% QoQ | 206.0 | +61% QoQ | 30.3 | -19% QoQ | 110.0 | +25% QoQ | 89.0 | +19% QoQ | Q4 AI compute、networking、HBM 同时上行 |
| 2025Q3 | 440.2 | +11% QoQ | 128.1 | >2x QoQ | 37.6 | +9% QoQ | 88.0 | +4% QoQ | 75.0 | 持平 QoQ | AI 相关收入约 40%-50% |
| 2025Q2 | 397.2 | -2% QoQ | 61.0 | -44% QoQ | 34.0 | +27% QoQ | 85.1 | +15% QoQ | 75.0 | +9% QoQ | 客户 pushout 影响短期收入，AI compute 订单开始转强 |
| 2025Q1 | 406.4 | - | 109.4 | - | 26.7 | - | 74.2 | - | 69.0 | - | 低基数季度；HBM 客户消化前期产能 |

### 2.3 分部利润率

| 口径 | Semiconductor Test | Product Test | Robotics | 公司合计 |
|---|---:|---:|---:|---:|
| 2025 全年收入 | 25.24 亿美元 | 3.58 亿美元 | 3.08 亿美元 | 31.90 亿美元 |
| 2025 分部毛利率 | 59.7% | 60.8% | 51.0% | 公司 GAAP GM 58.2% |
| 2025 分部税前利润率 | 27.8% | 17.0% | -32.2% | GAAP 税前利润率约 19.4% |
| 2026Q1 收入 | 11.11 亿美元 | 0.80 亿美元 | 0.91 亿美元 | 12.82 亿美元 |
| 2026Q1 分部毛利率 | 62.7% | 57.0% | 50.5% | 公司 GAAP GM 60.9% |
| 2026Q1 分部税前利润率 | 42.1% | 5.9% | -1.1% | GAAP 税前利润率 36.3% |

利润率要点：AI compute/HBM 拉动 Semiconductor Test 混合，2026Q1 分部税前利润率高达 42.1%。Robotics 仍是利润拖累，但 Q1 已接近盈亏平衡；如果大客户 PoR 和 AI 应用落地，Robotics 的亏损弹性会改善，但短期 TER 的估值主要由 Semiconductor Test 支撑。

### 2.4 订单、backlog、lead time、取消率的可验证事实与推断

| 项目 | 公司披露事实 | 推断 |
|---|---|---|
| Backlog 披露 | 10-K 明确提示 backlog 不能代表未来销售，因为客户可延迟交付或取消订单，可能有取消罚金；不披露按产品的 backlog | 不能把官方 backlog 当主指标，只能用 guide、lead time、客户订单、deferred revenue/customer advances、A/R、交付节奏推断 |
| Lead time | 2026Q1：UltraFLEXplus 过去 9 个月出货翻倍，同时维持 12-16 周 lead time | 供给紧张但未失控，TER 通过 contract manufacturing 和 multi-source 把交期控制在一个季度左右 |
| 取消率 | 2025Q1/Q2：公司提到客户 pushout 和 capital review，但没有取消；2026Q1 未披露取消压力 | AI compute/HBM 的取消率当前低，非 AI 手机/汽车/工业可能仍有推迟风险 |
| AI GPU订单 | 2026Q1 获得首个 merchant GPU 多系统生产测试订单，系统预计 Q2 发货、安装并进入生产；2026 年 GPU 相关收入可见性约 5000 万美元 | 这是 TER 从客户自研 AI ASIC 扩展到 merchant GPU 的关键验证；若该客户量产良率/吞吐达标，2027 可复制到更多 GPU/ASIC 平台 |
| Deferred revenue/customer advances | 2026Q1 deferred revenue and customer advances 为 2.55 亿美元，较 2025 年末 2.04 亿美元增加 5149 万美元 | 未交付硬件和服务义务上升，但金额相对季度收入不大；TER 的订单强度更多体现在 guide 和设备出货，而非 deferred revenue |
| A/R | 2026Q1 A/R 11.08 亿美元，较 2025 年末增加 3.21 亿美元 | 强出货、客户集中和大额设备验收导致回款滞后；需观察 Q2 经营现金流 |

## 3. 2026 最新财报指引、业务收入占比、产品映射与重点产品

### 3.1 2026Q2 指引与全年隐含收入

| 项目 | 公司指引/披露 | 推断 |
|---|---:|---|
| 2026Q2 收入 | 11.5-12.5 亿美元 | 中点 12.0 亿美元，环比 2026Q1 下降约 6.4%，同比仍强 |
| 2026Q2 Non-GAAP EPS | 1.86-2.15 美元 | 中点 2.005 美元 |
| 2026Q2 毛利率 | 58%-59% | 低于 Q1，可能因 mix、产能/交付节奏、产品组合 |
| 2026Q2 opex | 收入的 27%-28% | AI NPI 和软件/光电投入仍高 |
| 2026Q2 non-GAAP op margin | 30%-32% | 仍显著高于 2025 上半年 |
| 2026H1 占全年收入 | 55%-60% | Q1 实际 12.82 亿 + Q2 中点 12.0 亿 = 24.82 亿，隐含全年约 41.4-45.1 亿美元 |
| 2026 全年收入增速 | 公司未给明确全年收入 | 隐含 +30%-41% YoY，相比 2025 年 31.90 亿美元 |

关键信号：公司一边说 AI momentum 很强，一边把 H1 占全年放在 55%-60%。这不是坏消息，而是提醒投资人 2026 年收入会很前置，H2 可能出现客户吸收、安装节奏、program timing 的波动。极度乐观情境必须假设 H2 新 GPU/ASIC/HBM4/SiPho 订单继续接上，而不是 Q1/Q2 的拉货透支。

### 3.2 2026Q1 收入占比与增长

| 业务 | 2026Q1 收入 | 占总收入 | YoY | QoQ | 主要驱动 |
|---|---:|---:|---:|---:|---|
| SoC | 8.82 亿美元 | 68.8% | +117% | +36% | AI compute、networking、XPU/CPU、merchant GPU 初始订单、224G/高速接口 |
| Memory | 2.02 亿美元 | 15.8% | +85% | -2% | HBM/DRAM，Magnum 7 ramp |
| IST | 0.27 亿美元 | 2.1% | -1% | -11% | AI SLT、HDD/SSD；单季节奏波动 |
| Product Test | 0.80 亿美元 | 6.3% | +8% | -27% | 国防航天、生产板测、无线、硅光/PIC |
| Robotics | 0.91 亿美元 | 7.1% | +32% | +2% | 渠道调整后恢复，AI应用约 15% |
| 合计 | 12.82 亿美元 | 100% | +87% | +18% | AI 约 70% 收入 |

最突出和公司最侧重业务：AI compute SoC ATE 与 HBM/DRAM Memory ATE。第二梯队是硅光/CPO/高速互连/board test/SLT，这些业务当前收入小但战略意义高，因为它们把 TER 的覆盖从芯片本体扩展到数据中心互连和系统级质量验证。

### 3.3 产品与业务映射

| 业务 | 重点产品/型号 | 产品角色 | 2026 重要性 |
|---|---|---|---|
| SoC AI compute/networking ATE | UltraFLEXplus、UltraPHY 112G、UltraPHY 224G、IG-XL、TestInsight 软件 | AI GPU/ASIC、networking ASIC、CPU/XPU、SerDes/PHY 的 wafer/final/production test | 最高 |
| Memory/HBM | Magnum 7、Magnum 7H | HBM/DRAM wafer/final/performance test，高并行 pins 和功率 pins 降低 cost-of-test | 最高 |
| IST/SLT | Titan HP、IST 平台、AI accelerator SLT 方案 | 高价值 AI package 的 system-level test、burn-in、企业 SSD/HDD 测试 | 高 |
| Silicon Photonics/CPO | Photon 100、Quantifi Photonics 技术、UltraFLEXplus 集成光电仪器 | PIC、光引擎、CPO module、AI accelerator with CPO、switch CPO 的电光测试 | 高潜力 |
| Board/System/Product Test | Omnyx、生产板测平台、LitePoint、国防航天测试 | AI server board、tray、PCB、无线连接和复杂电子系统测试 | 高潜力 |
| Data center interconnect | MLTP JV、MultiLane 高速 I/O 仪器 | 224G/高速互连、数据中心设备测试，从 wafer 到 system | 高潜力 |
| Power semiconductor / data center power | ETS-800、Infineon AET 技术、UltraFLEX/J750 相关能力 | AI数据中心电源管理、功率器件、汽车/工业/数据中心功率半导体测试 | 中高 |
| Robotics | Universal Robots、MiR AMR、AI 应用包 | 先进制造、半导体、仓储、汽车、AI 驱动应用 | 中 |

### 3.4 可以跳过/低权重的非 AI 产品与业务

这些业务不是没有价值，而是对未来 12 个月 TER 的 AI 重估贡献有限：

| 业务/产品 | 为什么低权重 |
|---|---|
| 传统移动 SoC 测试 | 仍有收入和利润，但 2025-2026 最大弹性来自 AI compute/networking；移动受手机周期影响 |
| 传统汽车/工业非数据中心测试 | 周期性、增长慢；其中与数据中心电源相关部分另列为重点 |
| 传统无线 Wi-Fi 测试 | LitePoint 仍强，但不是 TER 当前估值主因；Wi-Fi 7/8 可保持稳定增长 |
| 国防航天电子测试 | 2025-2026 对 Product Test 有支撑，但规模小、与 AI 数据中心关联弱 |
| Robotics 传统 cobot/AMR | 渠道恢复有价值，但目前利润率和 AI 相关度低于 Semiconductor Test |

### 3.5 不应漏掉的潜力小产品/小业务

| 潜力点 | 证据 | 为什么值得看 |
|---|---|---|
| TestInsight 软件 | 2026-04 收购；用于测试开发、验证、转换，覆盖 TER 和竞争平台 | AI/数据中心芯片 NPI 更复杂，软件可提高客户粘性，毛利率可能高于硬件 |
| Photon 100 双面 wafer / optical engine / CPO module 测试 | 2026-03 发布；支持 wafer、光引擎、CPO module 测试插入点 | 如果硅光/CPO 进入 HVM，TER 有机会成为“电+光+量产自动化”集成商 |
| MLTP 高速 I/O 测试 | 2026-01 JV，Teradyne 多数股东；MultiLane 专长在高速 I/O 和数据中心互连 | 224G/未来 448G、AI data center interconnect 测试需求明显上升 |
| Omnyx board test | 2026-03 发布，定位 AI 时代板级测试 | AI server board/tray 价值高，board test 需求从消费电子/传统服务器升级 |
| Data center power devices 测试 | Q1 auto/industrial 收入中 46% 来自 data center devices；2025 收购 Infineon AET | AI rack 功率上升，power management、SiC/GaN、电源模块测试会变重要 |
| Robotics AI 应用 | Q1 Robotics 约 15% 为 AI 应用；公司曾给 2028 AI应用 1.5 亿美元目标 | 若大客户 PoR 在 2026H2 兑现，Robotics 可从拖累变成可选项 |

## 4. 当前高增长/关键产品：收入贡献、增速、AI基建重要性、供需与定价权

评分：1 低，5 高。收入贡献为当前年化或最近季度推断，不等同公司正式披露的产品级收入。

| 关键业务/产品 | 当前收入贡献估算 | 当前增速 | AI基建重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价能力 | 核心依据 |
|---|---:|---:|---:|---:|---:|---:|---|
| UltraFLEXplus / SoC AI compute & networking ATE | 2026Q1 SoC 8.82 亿美元，其中 compute 约 75% SoC 产品收入，估算单季 6.5-6.7 亿美元 | SoC +117% YoY；compute 2025 年 +90% YoY | 5 | 5 | 4 | 4 | AI GPU/ASIC/CPU/networking ASIC 量产必须测试；lead time 12-16 周 |
| UltraPHY 224G / high-speed PHY | 收入并入 SoC，独立未披露；当前估算单季数千万美元级 | 新产品，随 224G/PCIe7/CXL/UCIe/SiPho 增长 | 5 | 4 | 4 | 3.5 | 224G PAM4、OIF CEI-224G、PCIe Gen7、硅光是 2026-2027 关键验证点 |
| Magnum 7 / Magnum 7H HBM Memory ATE | 2026Q1 Memory 2.02 亿美元；HBM/DRAM 为主要驱动 | Memory +85% YoY；2025 Memory 5.05 亿美元 | 5 | 5 | 4.5 | 4 | HBM3E/HBM4 良率和 KGD 测试不可省；公司给 2028 Memory 16 亿美元目标 |
| Titan HP / IST / AI SLT | 2026Q1 IST 2654 万美元；2025 年 1.29 亿美元 | 2025 +52% YoY；2026Q1 单季波动 | 4 | 4 | 3.5 | 3.5 | AI package 价值高，SLT/burn-in 对 early failure 和系统级问题有价值 |
| Photon 100 / Quantifi / SiPho-CPO test | 当前收入大概率低双位数百万美元/季以内，主要在 Product Test/SoC 边缘 | 早期高增，基数小 | 4.5 | 3.5 | 4 | 3.5 | 硅光/CPO 尚未全面 HVM，但测试复杂度高；中期 TAM 3-7 亿美元/年 |
| Omnyx / Product Test / AI server board | 2026Q1 Product Test 8044 万美元，AI board test 未披露 | Product Test +8% YoY；AI板测新产品初期 | 4 | 4 | 3.5 | 3 | AI server board/rack 价值高，板级故障成本高 |
| MLTP / data center high-speed interconnect test | 2026Q1 尚无完整收入贡献，4 月后开始并表/贡献 | 新业务 | 4.5 | 4 | 4 | 3.5 | 从 wafer 到 system 的高速互连测试，MultiLane 具高频 I/O 仪器能力 |
| Data center power semiconductor test / ETS-800 / AET | Q1 auto/industrial 中 46% 与 data center devices 相关，估算单季 0.7-1.2 亿美元 | Q1 auto/industrial 近翻倍 QoQ | 3.5 | 4 | 3.5 | 3.5 | AI数据中心功率密度上升，电源链测试需求扩张 |
| Robotics AI applications | Q1 Robotics 9126 万美元，其中 AI应用约 15%，即约 1400 万美元 | Robotics +32% YoY；AI应用基数小高增 | 2.5 | 2.5 | 2.5 | 3 | 与 AI 基建关联间接，更多是先进制造/仓储自动化 |

## 5. 未来一年分产品三档预测

未来一年定义为 2026Q2-2027Q1 的滚动 12 个月。预测为研究判断，不是公司指引。

### 5.1 公司总收入三档

| 情境 | 未来一年收入 | 增速判断 | AI收入占比 | 触发条件 |
|---|---:|---:|---:|---|
| 基准 | 46-49 亿美元 | 较 TTM +20%-30% | 65%-70% | 2026H2 按公司“前高后低”节奏消化，HBM/compute 仍强但不继续加速 |
| 乐观 | 52-56 亿美元 | +35%-45% | 70%-75% | 新 AI ASIC/GPU、HBM4 NPI、224G/SiPho/board test 接力，H2 不明显回落 |
| 极度乐观 | 60-64 亿美元 | +55%-70% | 75%+ | ATE TAM 提前进入 120-140 亿美元级公司目标区间，TER 份额稳定，AI订单持续追单 |

### 5.2 分产品收入贡献预测

| 关键业务/产品 | 基准：未来一年收入贡献 | 乐观：未来一年收入贡献 | 极度乐观：未来一年收入贡献 | 基准增速 | 乐观增速 | 极度乐观增速 |
|---|---:|---:|---:|---:|---:|---:|
| SoC AI compute/networking ATE | 22-25 亿美元 | 27-31 亿美元 | 33-38 亿美元 | +45%-60% | +80%-100% | +120%+ |
| HBM/DRAM Memory ATE | 8-9 亿美元 | 10-12 亿美元 | 13-16 亿美元 | +55%-75% vs 2025 | +100%+ | +150%-220% |
| IST / Titan HP / AI SLT | 1.6-2.2 亿美元 | 2.5-3.5 亿美元 | 4.0-5.5 亿美元 | +25%-70% | +90%-170% | +200%+ |
| Photon 100 / SiPho / CPO | 0.8-1.3 亿美元 | 1.5-2.5 亿美元 | 3.0-4.5 亿美元 | 基数小，高增 | 高增 | 爆发式，但需 CPO HVM |
| Omnyx / Product Test / AI server board | 1.5-2.5 亿美元 | 3.0-4.5 亿美元 | 5.0-7.0 亿美元 | +20%-50% | +70%-120% | +150%+ |
| MLTP / 高速互连测试 | 0.5-1.0 亿美元 | 1.5-2.5 亿美元 | 3.0-5.0 亿美元 | 新业务 | 新业务放量 | 若 224G/448G 仪器需求超预期 |
| Data center power semiconductor test | 1.8-2.6 亿美元 | 3.0-4.2 亿美元 | 5.0-6.5 亿美元 | +30%-60% | +80%-130% | +180%+ |
| Robotics AI应用 | 0.8-1.2 亿美元 | 1.5-2.2 亿美元 | 2.5-3.5 亿美元 | +100% 左右 | +200% 左右 | PoR 大客户快速铺开 |

### 5.3 未来一年评分变化

| 关键业务/产品 | 情境 | AI基建重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价能力 | 核心判断 |
|---|---|---:|---:|---:|---:|---|
| SoC AI compute/networking ATE | 基准 | 5 | 5 | 4 | 4 | AI ASIC/GPU 测试继续供不应求，但 TER 保持 12-16 周 lead time |
| SoC AI compute/networking ATE | 乐观 | 5 | 5 | 4.5 | 4.2 | 多个 AI ASIC/GPU program 并行，客户追单 |
| SoC AI compute/networking ATE | 极度乐观 | 5 | 5 | 5 | 4.5 | 2027 项目提前下单，TER/Advantest 均满产，价格和服务议价力上升 |
| HBM Memory ATE | 基准 | 5 | 5 | 4.5 | 4 | HBM3E 扩产 + HBM4 NPI，测试是瓶颈之一 |
| HBM Memory ATE | 乐观 | 5 | 5 | 5 | 4.2 | HBM4 认证/量产提前，DRAM 厂拉设备 |
| HBM Memory ATE | 极度乐观 | 5 | 5 | 5 | 4.5 | HBM/AI package 供需极紧，测试设备成为扩产前置采购 |
| SiPho/CPO/Photon 100 | 基准 | 4 | 3.5 | 3.5 | 3.5 | 先在研发/试产/少量 HVM 部署 |
| SiPho/CPO/Photon 100 | 乐观 | 4.5 | 4 | 4.5 | 4 | CPO/optical engine 工艺成熟，客户需要一体化电光测试 |
| SiPho/CPO/Photon 100 | 极度乐观 | 5 | 5 | 5 | 4.2 | CPO 成为 AI switch/GPU 互连主流路径，测试复杂度拉满 |
| Board/System/MLTP | 基准 | 4 | 4 | 3.5 | 3 | AI server board 和高速互连测试需求稳步上升 |
| Board/System/MLTP | 乐观 | 4.5 | 4.5 | 4.5 | 3.5 | Rack-scale AI 交付导致 system test 扩产 |
| Board/System/MLTP | 极度乐观 | 5 | 5 | 5 | 4 | 224G/448G、liquid-cooled rack、NVL/ASIC 集群使系统测试成为瓶颈 |

## 6. BOM、每 MW / rack / GPU / optical port 内容量、价格传导、产能与认证

### 6.1 先定义：TER 的“BOM 含量”不是装进 GPU 的物料，而是测试设备折旧和测试工序成本

TER 的设备通常不是最终 AI GPU/服务器的直接 BOM，而是 OSAT、foundry、IDM、ODM、EMS、测试厂购买的资本设备。最终内容量应该理解为：为了制造和交付一个 GPU/ASIC、HBM stack、board、rack 或 optical port，需要摊销多少测试设备、接口板、探针、socket、handler、软件、服务和产线调试成本。

因此本报告使用“TER 可捕获的测试设备摊销内容量”：

```text
TER设备售价 / 设备可测试的生命周期单位数 / 利用率 / 良率与重测率
= 每颗芯片、每个HBM stack、每张板、每rack或每MW摊销测试设备内容量
```

### 6.2 AI GPU / ASIC 的测试内容量

| 层级 | 真实测试内容 | TER 相关产品 | 单位内容量估算 | TER 可捕获比例 |
|---|---|---|---:|---:|
| Wafer sort / final test | 数字逻辑、scan、memory interface、SerDes、power、thermal、DFT、功能测试 | UltraFLEXplus、UltraPHY 112G/224G、IG-XL、TestInsight | 成熟 AI chip：20-80 美元/颗；早期复杂 chiplet/XPU：80-250 美元/颗 | 30%-60%，取决于客户是否 TER 平台 |
| HBM stack / KGD 测试 | HBM DRAM die、stack、KGD、speed bin、thermal/retention、repair | Magnum 7 / 7H | HBM3E 成熟：1.5-7.5 美元/stack；HBM4 早期：5-20 美元/stack | 30%-50% |
| Package / SLT / burn-in | 高功耗封装、HBM 互连、NVLink/SerDes、系统级 workload、早期失效筛选 | Titan HP、IST/SLT | 30-150 美元/AI package；极复杂/早期量产可达 200 美元+ | 20%-50% |
| Board / tray test | GPU baseboard、switch tray、power delivery、connectors、firmware、high-speed links | Omnyx、Product Test、MLTP | 100-800 美元/board；高价值 liquid-cooled tray 可更高 | 10%-40% |

按单颗 GPU/ASIC 汇总：

| 情境 | 每 GPU/ASIC TER 地址able测试设备摊销内容量 | 说明 |
|---|---:|---|
| 基准 | 80-250 美元 | 包括 SoC ATE、HBM 测试部分、少量 SLT/board test 摊销 |
| 乐观 | 250-500 美元 | HBM4、chiplet、224G PHY、SLT、board test 同时提高 |
| 极度乐观 | 500-900 美元 | 早期良率低、测试时间长、CPO/board/system test 明显增加；仅适用于高端/新平台早期 |

### 6.3 每 rack 内容量

假设 AI rack 类似高密度 GPU rack，单 rack 可包含约 64-72 个 accelerator，功率 100-140 kW；不同架构差异巨大，因此用区间。

| 内容层 | 基准 | 乐观 | 极度乐观 | 解释 |
|---|---:|---:|---:|---|
| GPU/ASIC ATE 摊销 | 0.6-1.8 万美元/rack | 1.8-3.6 万美元/rack | 3.6-6.5 万美元/rack | 72 GPU * 每 GPU 80-900 美元中的 TER 可捕获段 |
| HBM 测试摊销 | 0.1-0.5 万美元/rack | 0.5-1.5 万美元/rack | 1.5-4.0 万美元/rack | 每 GPU 6-12 个 HBM stacks，TER 只捕获 ATE 部分 |
| SLT / burn-in / package test | 0.5-2.0 万美元/rack | 2.0-5.0 万美元/rack | 5.0-10.0 万美元/rack | 高价值 package 的系统级测试需求 |
| Board / tray / system test | 0.8-3.0 万美元/rack | 3.0-8.0 万美元/rack | 8.0-15.0 万美元/rack | Omnyx、PBT、MLTP 相关机会 |
| Optical / interconnect test | 0.3-2.0 万美元/rack | 2.0-6.0 万美元/rack | 6.0-12.0 万美元/rack | 800G/1.6T/未来 CPO 或 224G/448G 互连 |
| 合计 | 2.3-9.3 万美元/rack | 9.3-24.1 万美元/rack | 24.1-47.5 万美元/rack | 不是 TER 当前确认收入，而是地址able摊销内容量 |

### 6.4 每 MW 内容量

假设 1 MW 支持约 7-10 个高密度 rack 或约 500-700 个高端 accelerator。

| 情境 | TER 地址able测试设备摊销内容量 / MW | 解释 |
|---|---:|---|
| 基准 | 15-80 万美元/MW | 成熟 GPU/HBM、以传统 pluggable optics 为主 |
| 乐观 | 80-200 万美元/MW | HBM4、SLT、board test、224G/1.6T 光电测试增加 |
| 极度乐观 | 200-450 万美元/MW | CPO/系统级测试显著提高，早期良率/可靠性压力导致测试强度上升 |

这个区间的意义：AI 数据中心 capex 每 MW 动辄数千万美元，测试设备摊销占比很小，但故障成本极高，因此客户愿意为测试覆盖率、throughput、yield learning 支付溢价。

### 6.5 每 optical port 内容量

| Optical / electrical port 类型 | 测试内容 | TER/MLTP/Photon 相关性 | 内容量估算 |
|---|---|---|---:|
| 800G pluggable port | BER、眼图、FEC、jitter、温漂、模块功能 | Product Test / Quantifi / MLTP 边缘参与 | 成熟量产 2-10 美元/port |
| 1.6T pluggable port | 112G/224G lanes、PAM4、DSP、thermal | UltraPHY、MLTP、Quantifi | 10-40 美元/port |
| Optical engine / CPO port | 光电协同、alignment、wafer+module、high-density channel、thermal | Photon 100、Quantifi、UltraFLEXplus | 20-100 美元/port 或 engine 等效端口 |
| 未来 3.2T / 448G lane | 更高带宽、更高测试时间和仪器复杂度 | MLTP + UltraPHY 后续路线 | 50-150 美元/port，早期可能更高 |

### 6.6 当前产能能力、供应链采纳和认证阶段

| 业务/产品 | 当前产能能力（收入计） | 供应链采纳程度 | 认证/阶段 |
|---|---:|---|---|
| UltraFLEXplus / SoC ATE | 2026Q1 Semitest 已实现 11.11 亿美元单季收入；公司称 UltraFLEXplus 出货 9 个月翻倍且保持 12-16 周 lead time | 高，已被 AI compute、networking、VIP客户使用；2025 compute 成 SoC 最大收入 | 多个 AI ASIC/CPU/networking 量产；merchant GPU 多系统生产测试订单进入 Q2 安装/生产 |
| Magnum 7 / 7H HBM | 2026Q1 Memory 2.02 亿美元，年化约 8 亿美元；公司 2028 目标 16 亿美元 Memory 收入 | 高，HBM/DRAM 驱动；公司称 Magnum 是行业 de facto standard，并目标约 50% share | HBM4 performance test win 已获得；Magnum 7H 2025 发布、进入客户 ramp |
| Titan HP / IST/SLT | 2025 IST 1.29 亿美元；Q1 单季 2654 万美元 | 中高，已有 AI compute SLT 首批收入/客户接受 | AI accelerator SLT 从 customer acceptance 到量产爬坡；节奏取决于具体客户 |
| Photon 100 / SiPho/CPO | 当前收入小，产品刚发布；中期 TAM 3-7 亿美元/年 | 早期，客户多在研发、NPI、试产或初期量产 | 2026 OFC 发布/展示；支持 wafer、optical engine、CPO module 插入 |
| Omnyx / Product Test | Product Test 2026Q1 8044 万美元，AI board test 未单列 | 早期到中期，生产板测/国防航天有基础，AI server board 新增 | 2026 发布；需要客户板卡/服务器平台认证 |
| MLTP | 2026Q1 尚未完整贡献，4 月后关闭交易 | 早期，MultiLane 在高速 I/O 和数据中心互连有客户基础 | JV 2026-04 后落地，认证随客户标准和仪器设计推进 |
| Data center power test | Q1 auto/industrial 中数据中心设备占比 46%，估算单季 0.7-1.2 亿美元 | 中高，功率半导体客户基础 | ETS-800 2025 发布；Infineon AET 技术/关系增强 |
| Robotics AI应用 | Q1 AI应用约 1400 万美元 | 早期，2025 年大客户 PoR | PoR 不等于大规模收入，需观察 2026H2-2027 转订单 |

## 7. 未来一年产能、采纳与认证三档预测

| 业务/产品 | 情境 | 未来一年产能能力（收入计） | 供应链采纳 | 认证/阶段预测 |
|---|---|---:|---|---|
| UltraFLEXplus / SoC ATE | 基准 | 25-30 亿美元/年 | 现有 AI ASIC/networking 客户扩产；merchant GPU 初始生产 | GPU 订单 Q2 量产，更多平台 NPI |
| UltraFLEXplus / SoC ATE | 乐观 | 32-38 亿美元/年 | hyperscaler ASIC + merchant GPU + networking 同时拉货 | 多客户生产认证，客户二供策略仍给 TER 份额 |
| UltraFLEXplus / SoC ATE | 极度乐观 | 40 亿美元+/年 | AI SoC ATE 全行业紧缺，TER 份额稳定 | 新平台认证提前，客户愿意锁产能 |
| Magnum 7/7H | 基准 | 9-10 亿美元/年 | HBM3E 扩产稳定，HBM4 NPI | HBM4 试产认证推进 |
| Magnum 7/7H | 乐观 | 12-14 亿美元/年 | HBM4 和 DRAM final test 双强 | 多家 DRAM 厂 HBM4 量产认证 |
| Magnum 7/7H | 极度乐观 | 16 亿美元+/年 | 2028 目标提前实现 | HBM4 成为 2027 主流扩产前置采购 |
| Titan HP / IST/SLT | 基准 | 1.8-2.5 亿美元/年 | AI SLT 从少数客户扩到更多 package | 客户量产认证逐步扩大 |
| Titan HP / IST/SLT | 乐观 | 3-4 亿美元/年 | AI package SLT 成标准流程 | 多客户、多平台标准化 |
| Titan HP / IST/SLT | 极度乐观 | 5 亿美元+/年 | 大规模 AI accelerator burn-in/SLT 瓶颈化 | rack/system reliability 要求推高认证覆盖 |
| Photon 100 / SiPho/CPO | 基准 | 1 亿美元左右 | NPI/试产/少量量产 | OFC 后客户 evaluation 到 pilot |
| Photon 100 / SiPho/CPO | 乐观 | 2-3 亿美元 | CPO/optical engine 量产线启动 | 部分 hyperscaler/switch 客户 HVM 认证 |
| Photon 100 / SiPho/CPO | 极度乐观 | 4-5 亿美元 | CPO 进入 AI switch/GPU 主线 | HVM 认证批量通过，Photon 成生产 test cell |
| Omnyx/MLTP/Product Test | 基准 | 2-4 亿美元 | 现有板测客户升级 AI server | 逐客户板级平台认证 |
| Omnyx/MLTP/Product Test | 乐观 | 5-7 亿美元 | 224G/1.6T 和 AI server board test 扩产 | 多家 ODM/EMS/test house 采纳 |
| Omnyx/MLTP/Product Test | 极度乐观 | 9-12 亿美元 | 从 board 到 rack/system 的测试成为 AI 交付瓶颈 | rack-scale certification 和 hyperscaler 标准推动 |

## 8. 基于订单积压、供给和扩产能力的未来一年增速预测

### 8.1 真实订单与供给线索

| 线索 | 强度 | 对未来一年增速的影响 |
|---|---:|---|
| 2026Q1 收入 12.82 亿美元，同比 +87%，AI约70% | 很强 | 已确认需求不是 PPT，是出货和收入 |
| 2026Q2 指引 11.5-12.5 亿美元 | 很强 | 即使环比回落，仍维持高收入平台 |
| H1 占全年 55%-60% | 双刃剑 | 隐含全年 41-45 亿美元，但也暗示 H2 不会简单年化 Q1 |
| UltraFLEXplus 出货 9 个月翻倍，lead time 12-16 周 | 强 | 供应链响应能力好；若订单继续，产能可继续释放 |
| merchant GPU 多系统订单 + 2026 约 5000 万美元可见性 | 中高 | 打开 merchant GPU 客户路径，但短期金额相对公司总收入小 |
| Memory Q1 2.02 亿美元接近 Q4 纪录水平 | 强 | HBM/DRAM 测试需求不是一次性 |
| deferred revenue/customer advances +5149 万美元 QoQ | 中 | 支撑未交付订单，但金额相对收入有限 |
| 2025Q1/Q2 有 pushout、无取消 | 中 | 非 AI 客户会推迟；AI 客户取消风险低但节奏会波动 |
| contract manufacturing 支撑 >80% 收入 | 强 | 扩产弹性较好，但关键零部件/仪器模块仍可能是瓶颈 |

### 8.2 未来一年业务增速三档

| 情境 | 未来一年总收入增速 | Semiconductor Test 增速 | Product Test 增速 | Robotics 增速 | 假设 |
|---|---:|---:|---:|---:|---|
| 基准 | +20%-30% | +25%-35% | +10%-20% | +10%-20% | 2026H2 消化但不塌；AI compute/HBM 高位延续；SiPho/MLTP 贡献小 |
| 乐观 | +35%-45% | +45%-60% | +30%-60% | +20%-35% | H2 新订单接力，HBM4/224G/board test 初步放量；Robotics 大客户开始贡献 |
| 极度乐观 | +55%-70% | +70%-90% | +80%+ | +50%+ | AI accelerator/HBM/SiPho/SLT/MLTP 全部超预期，TER 接近 60 亿美元收入模型 |

### 8.3 订单质量判断

当前订单质量较高，但不是“无条件越多越好”：

1. AI compute/HBM 订单质量最高。原因是客户项目价值高、量产窗口明确、测试是良率和可靠性前置条件。
2. SiPho/CPO/MLTP 订单质量处于验证期。技术方向对，但收入确认取决于 CPO/224G/未来448G 是否快速进入 HVM。
3. Product Test 的 AI board/rack 测试有潜力，但客户自建/ODM内部测试、Keysight/NI/Anritsu/R&S 等竞争会分流。
4. Robotics 的 PoR 不能等同 backlog。需要实际出货、安装、服务和毛利改善验证。

## 9. 竞争格局、技术路线、替代风险与客户替换成本

### 9.1 主要竞争对手

| 领域 | TER 主要竞争对手 | TER 优势 | 主要风险 |
|---|---|---|---|
| High-end SoC ATE | Advantest V93000、Cohu、SPEA、Chroma、客户内部测试 | UltraFLEXplus、IG-XL 生态、AI compute/networking 客户关系、224G 路线 | Advantest 在 HPC/AI SoC 同样强，客户可能双供压价 |
| Memory/HBM ATE | Advantest、Cohu、Chroma、部分客户内部平台 | Magnum 7/7H、HBM/DRAM share、公司 50% share 目标 | HBM 厂商可能维持多供应商；HBM4 节奏若推迟会影响设备需求 |
| Probe/wafer interface | FormFactor、Technoprobe、MPI、Japan Electronic Materials 等 | TER 投资 Technoprobe 10%，生态绑定 | 探针卡本身不由 TER 完全控制；接口交期可影响 ATE 利用率 |
| SLT/burn-in | Chroma、Cohu、Aehr、Advantest、客户/OSAT内部方案 | Titan HP、ATE到SLT数据闭环 | SLT 方案容易客户定制化，规模化速度慢 |
| 高速/光学测试 | Keysight、Anritsu、Rohde & Schwarz、VIAVI、EXFO、NI、MultiLane历史客户生态 | Photon 100、Quantifi、UltraFLEXplus 量产自动化、MLTP | 仪器巨头技术深，CPO 若推迟会拖累需求 |
| Board/system test | Keysight、NI、R&S、Chroma、Cohu、ODM/EMS 自研测试 | Product Test、Omnyx、从芯片到系统的数据链 | ODM/EMS 可能自建，毛利率和标准化低于 ATE |
| Robotics | KUKA、ABB、FANUC、Yaskawa、Staubli、Doosan、Techman、Jaka、Omron、Rockwell、HikRobot、AGILOX 等 | UR/MiR 品牌、渠道、协作机器人先发 | 中国/亚洲低价竞争，盈利修复慢 |

### 9.2 TER 的新技术是否会成为主流

| 技术/产品 | 成为主流概率 | 判断 |
|---|---:|---|
| UltraFLEXplus for AI compute/networking | 高 | AI GPU/ASIC、networking ASIC 的测试复杂度上升是确定方向；TER 和 Advantest 会长期双寡头竞争 |
| Magnum 7/7H for HBM | 高 | HBM3E/HBM4 扩产确定，HBM 测试是良率、速度分档、KGD 的必要环节 |
| UltraPHY 224G | 高 | 224G PAM4、PCIe Gen7、OIF CEI-224G、UCIe/CXL 是 AI 数据中心下一代电互连主线 |
| Photon 100 / CPO test | 中高 | CPO/硅光长期方向强，但 2026-2027 是否大规模量产仍不确定；pluggable optics 可能延长生命周期 |
| Omnyx / board test for AI | 中高 | AI board/rack 价值极高，测试需求必然增加；但标准化和 TER 份额不如 SoC ATE 确定 |
| MLTP / high-speed data center interconnect test | 中高 | 高速互连测试需求确定，JV 能否快速商业化需要观察 |
| Robotics AI应用 | 中 | 自动化趋势确定，但对 TER 估值主线的贡献依赖大客户部署和利润率改善 |

### 9.3 替代方案与风险

| 风险 | 影响路径 | 对 TER 的影响 |
|---|---|---|
| Advantest 份额提升 | AI SoC / HBM 客户双供或切换 | 降低 TER 高增长业务份额和定价权 |
| AI capex 消化 | Hyperscaler GPU/ASIC 订单暂停，OSAT/IDM 延迟测试设备 | 2026H2 或 2027 设备订单波动 |
| HBM/CoWoS/先进封装瓶颈 | 芯片封装产能不足，测试设备安装延后 | TER 订单可能递延，不一定取消 |
| CPO 推迟 | Pluggable optics 和 LPO/LRO 延长生命周期 | Photon 100/MLTP 放量慢于预期 |
| 客户内部测试 | 大客户/ODM/OSAT 自研部分 system test | Board/system test TAM 被压缩 |
| 出口管制和关税 | 中国销售、供应链、客户项目受限 | 10-K 已提示合规限制可能影响部分地区竞争 |
| Robotics 低价竞争 | UR/MiR 毛利和销量受压 | Robotics 利润修复拖后腿 |
| 估值过高 | 增速只要低于预期，倍数压缩 | 股票风险大于公司经营风险 |

### 9.4 客户替换成本

客户替换成本在不同层级差异很大：

| 层级 | 替换成本 | 原因 |
|---|---:|---|
| AI SoC ATE 平台 | 很高 | 测试程序、DFT、loadboard、handler/probe、yield correlation、量产认证、客户工程团队都绑定平台 |
| HBM Memory ATE | 很高 | speed bin、KGD、repair、thermal、parallelism、DRAM 厂认证周期长 |
| SLT / burn-in | 中高 | 和客户系统工作负载、firmware、可靠性模型强绑定，但设备架构更可定制 |
| 硅光/CPO测试 | 中高 | 电光仪器、alignment、光引擎工艺、产线自动化复杂；但早期客户仍会评估多家 |
| Board/system test | 中 | ODM/EMS 可多供应商或自研，替换成本低于 wafer/final test |
| Robotics | 中低 | 应用集成和安全认证有成本，但硬件替代供应商多 |

结论：TER 最强护城河在 SoC ATE 和 HBM ATE；Photon/MLTP/Omnyx 是潜力增量，但护城河需要通过客户认证和量产数据建立。

## 10. 情景估值框架

本报告不做目标价，只给估值压力测试。

| 情境 | 收入 | Non-GAAP EPS 粗估 | 合理 PE 区间 | 隐含市值区间 | 对当前 563 亿美元市值的解释 |
|---|---:|---:|---:|---:|---|
| 基准 2026-2027 | 46-49 亿美元 | 7.0-8.0 美元 | 35-45x | 385-565 亿美元 | 当前价格接近基准上沿，容错率有限 |
| 乐观 | 52-56 亿美元 | 9.0-10.5 美元 | 40-50x | 560-820 亿美元 | 需要 H2 订单接力和 2027 继续高增长 |
| 极度乐观 | 60-64 亿美元 | 11-13 美元 | 45-55x | 780-1120 亿美元 | 需要公司提前进入 Analyst Day 60 亿美元收入模型，同时保持高份额 |
| 下行情境 | 38-42 亿美元 | 5.5-6.5 美元 | 25-35x | 215-360 亿美元 | 若 2026H1 拉货后 H2/2027 消化，估值压缩空间大 |

关键不是 TER 业务是否好，而是“当前股价已经预支了多少好消息”。从经营质量看，TER 是 AI测试链中少数已经兑现收入和利润的公司；从风险收益看，未来 12 个月必须持续跟踪订单/lead time/AI revenue mix，而不能只看单季 EPS beat。

## 11. 后续跟踪清单

| 跟踪项 | 为什么重要 | 观察阈值 |
|---|---|---|
| 2026Q2 实际收入和 Q3 指引 | 验证 H1 前置后 H2 是否断档 | Q3 指引若明显低于 9 亿美元，市场会担心拉货结束 |
| AI revenue mix | 验证 AI 订单持续性 | 维持 65%-70% 以上为强；跌回 50% 以下需警惕 |
| UltraFLEXplus lead time | 衡量供需紧张 | 12-16 周稳定是健康；若缩短很多可能需求降温，若拉长很多可能供应瓶颈 |
| merchant GPU 订单扩展 | 验证从 ASIC 到 merchant GPU 的增量 | 2026 5000 万美元可见性是否上修 |
| Memory/HBM 收入 | 验证 HBM4/HBM3E 扩产 | 单季保持 2 亿美元附近或继续上行 |
| Photon 100 / MLTP / Omnyx 客户认证 | 决定第二增长曲线 | 出现明确 HVM 客户或订单金额 |
| Robotics 毛利和 op margin | 看拖累是否解除 | 分部税前利润转正并持续 |
| A/R 和 FCF | 验证收入质量 | A/R/收入回落、经营现金流跟上净利润 |

## 12. 资料来源

外部公开资料：

- Teradyne 2026Q1 earnings release / 8-K Exhibit 99.1：https://investors.teradyne.com/sec-filings/all-sec-filings/content/0001193125-26-188706/ter-ex99_1.htm
- Teradyne 2026Q1 Form 10-Q：https://investors.teradyne.com/sec-filings/all-sec-filings/content/0001193125-26-201058/ter-20260329.htm
- Teradyne 2025 Form 10-K：https://investors.teradyne.com/sec-filings/all-sec-filings/content/0001193125-26-059002/ter-20251231.htm
- Teradyne 2025Q4 / FY2025 results：https://investors.teradyne.com/news-events/press-releases/detail/433/teradyne-reports-fourth-quarter-and-full-year-2025-results
- Teradyne UltraFLEXplus product page：https://www.teradyne.com/products/ultraflexplus/
- Teradyne Photon 100 product page：https://www.teradyne.com/products/photon-100/
- Teradyne Photon 100 release：https://investors.teradyne.com/news-events/press-releases/detail/436/teradyne-introduces-photon-100
- Teradyne UltraPHY 224G release：https://investors.teradyne.com/news-events/press-releases/detail/423/teradyne-unveils-industry-leading-phy-performance-testing-capabilities
- Teradyne Magnum 7H release：https://investors.teradyne.com/news-events/press-releases/detail/419/teradyne-unveils-magnum-7h---the-next-generation-memory-tester-for-high-bandwidth-memory-devices
- Teradyne / MultiLane JV release：https://investors.teradyne.com/news-events/press-releases/detail/432/teradyne-and-multilane-announce-formation-of-joint-venture-multilane-test-products
- Teradyne TestInsight acquisition release：https://investors.teradyne.com/news-events/press-releases/detail/439/teradyne-acquires-testinsight-accelerating-time-to-market-for-ai-and-data-center-devices
- TER statistics / valuation data：https://stockanalysis.com/stocks/ter/statistics/

本地项目行业资料（未引用“公司调研”目录内文件）：

- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\行业调研\行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\行业调研\行业调研/AI头部芯片市场占比和规模.md`
- `D:\drive\Investment\工作台v5\行业调研_晶圆制造_设备_材料_测试\行业调研_探针卡_ATE与系统级测试_2026-05-08.md`
- `D:\drive\Investment\工作台v5\行业调研_晶圆制造_设备_材料_测试\行业调研_HBM与存储测试设备_2026-05-08.md`
- `D:\drive\Investment\工作台v5\行业调研_晶圆制造_设备_材料_测试\行业调研_高速互连与光学验证测试_2026-05-08.md`
- `D:\drive\Investment\工作台v5\行业调研_晶圆制造_设备_材料_测试\行业调研_先进逻辑晶圆代工和封装_2026-05-08.md`
- `D:\drive\Investment\工作台v5\conference_update\ofc_2026_conference_update.md`
- `D:\drive\Investment\工作台v5\conference_update\chiplet_summit_2026_update.md`

