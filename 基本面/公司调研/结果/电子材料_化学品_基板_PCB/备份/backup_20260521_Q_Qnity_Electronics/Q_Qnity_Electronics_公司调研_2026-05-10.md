# 公司：Q Qnity Electronics Inc.

> 截至日期：2026-05-10，美国太平洋时间。今天是周日，`Q` 最近一个完整交易日为 2026-05-08。Qnity 已公告将于 2026-05-12 发布 2026Q1 业绩，因此本文的“最新已发布财报”为 2025Q4/FY2025，2026Q1 只作为未来催化点。  
> 方法：未参考本目录 `公司调研` 下任何已有文件；结合项目内非公司调研目录的 AI 数据中心、AI 芯片、先进封装、前道材料、热界面材料和会议调研框架，并使用公司公告、SEC 文件、IR、行业会议/技术页面和市场数据交叉验证。  
> 记号：`B/O/X` = 基准/乐观/极度乐观。美元金额除特别说明外均为 USD。产品组收入为本文基于分部、产品映射和行业单耗的估算，不是公司逐项披露。

## 0. 一页结论

Qnity 是 DuPont 电子材料业务在 2025-11-01 分拆出来的纯电子材料公司，2025-11-03 以 `Q` 在 NYSE 开始交易。它不是 AI 芯片公司，而是 AI 半导体和 AI 服务器物理层的“材料铲子”：CMP pad/slurry、post-CMP clean、EUV/ArFi/KrF 光刻材料、RDL/TSV/Cu pillar 电镀与清洗、IC substrate/PCB 干膜与金属化、Kapton/Pyralux/Laird 热管理和 EMI 材料。

投资人眼中的 Qnity：高质量、客户认证深、毛利率 46% 左右、FCF 好的半导体材料资产；同时也是新分拆公司，负债被分拆交易抬高，估值按 2025-2026 年利润看已经不便宜。市场给它 AI premium 的核心理由不是“每颗 GPU 的 Qnity 价值量巨大”，而是 AI 带来的先进节点 wafer starts、HBM、CoWoS/2.5D、RDL、ABF/PCB、液冷/热界面材料需求同时放大，且材料一旦进客户 AVL，替换成本高。

最重要的判断：Qnity 对 AI 的弹性集中在五条线，按未来一年收入弹性排序为：先进封装 RDL/TSV/Cu pillar/清洗材料、Laird 热/EMI 材料、AI PCB/IC substrate 材料、CMP pad/slurry/clean、EUV/DUV 光刻材料。Eon EUV photoresist、无氟 KrF/ArFi、Cyclotene/玻璃基板相关介质、Emblem CMP、Laird TPCM/Tgel/Tputty 是不能漏的小产品或小业务。

估值和财务快照：2026-05-08 收盘价约 `$147.33`，市值约 `$30.9B`；StockAnalysis 显示 TTM P/E `43.5x`、forward P/E `37.7x`、P/S `6.3x`、EV/EBITDA `24.7x`。2025 年收入 `$4.754B`，同比 +10%；毛利率 46.2%；公司口径 GAAP net income `$729M`，EPS 口径净利润约 `$692M`，净利率约 14.6%-15.3%。2026 指引收入 `$4.97-5.17B`，中点同比 +6.6%；调整后 operating EBITDA `$1.465-1.575B`，中点同比 +8.4%；调整后 EPS `$3.55-3.95`。

最大风险：公司不披露 backlog/bookings；AI 订单需要用客户长协、产能投资、材料认证和下游 HBM/CoWoS/AI rack 交付推断。若 2026H2 GB300/Rubin/HBM4/ASIC 节奏被电力、CoWoS 或客户 capex 拉长，Qnity 的 AI 材料斜率会延后；若中国材料国产替代加快、EUV 胶无法打入主流层、或 PFAS/含氟材料监管加压，估值容错会明显下降。

## 1. 公司业务、定位与财务状态

### 1.1 业务概览

Qnity 由两个分部组成：

| 分部 | 2025 收入 | 占比 | 2025 分部 operating EBITDA | 分部 EBITDA margin | 业务实质 |
|---|---:|---:|---:|---:|---|
| Semiconductor Technologies | `$2.642B` | 55.6% | `$945M` | 35.8% | 晶圆制造、CMP、光刻材料、清洗/去胶、先进封装材料、半导体工艺耗材与部分工业聚合物 |
| Interconnect Solutions | `$2.112B` | 44.4% | `$539M` | 25.5% | PCB/IC substrate 干膜、金属化/电镀、Kapton/Pyralux 软板材料、Laird 热管理/EMI、显示和电子互连材料 |
| 合计 | `$4.754B` | 100% | 分部合计 `$1.484B`，公司调整后 pro forma operating EBITDA `$1.402B` | 29.5% | AI 半导体制造 + AI 服务器/网络互连物理层材料组合 |

公司产业链位置：Qnity 位于晶圆厂、存储厂、OSAT、IC substrate/PCB 厂、服务器/网络 OEM/ODM 的上游材料层。它很少直接面对 hyperscaler 采购，但材料会被 TSMC、Samsung、SK hynix、Micron、Intel、ASE/Amkor、Ibiden/Unimicron/SEMCO、服务器和光模块供应链设计进工艺配方、封装流程和系统 BOM。

客户和地理暴露：2025 年 Samsung 占收入约 11%，TSMC 约 8%；中国大陆收入约 `$1.57B`，约占 33%，韩国约 `$725M`，台湾约 `$707M`。因此公司既受益于亚洲先进制造，也暴露于中国半导体周期、出口管制和国产替代。

### 1.2 最近 3 年重大变化、转型和交易

| 时间 | 事件 | 投资含义 |
|---|---|---|
| 2023 | 半导体库存去化和消费电子弱周期压制电子材料；DuPont 电子业务仍保持高毛利和客户认证壁垒 | 2024-2025 收入增长有低基数和库存修复因素，但 AI/HBM/先进封装是结构性新增 |
| 2024-05 | DuPont 宣布将 Electronics 与 Water 分拆，后续 Electronics 业务命名为 Qnity | 从综合化工集团内部业务变成 pure-play electronics materials，估值可按半导体材料公司重估 |
| 2025-07 至 2025-10 | 分拆前路演、投资者日；公司披露 2024 约 15% 收入来自 data center / HPC / AI end market | 市场开始把它放进 AI 半导体材料篮子，而不是传统化工/电子材料周期股 |
| 2025-10 | 与 SK hynix 签 long-term CMP pad supply agreement/MOU；Qnity 称合作覆盖下一代半导体材料、HBM 和先进封装需求 | 对 CMP pad 进入 HBM/DRAM 核心客户的订单能见度有正面意义，虽未披露金额 |
| 2025-11-01/03 | 完成从 DuPont 分拆并在 NYSE 以 `Q` 交易；Qnity 向 DuPont 支付约 `$4.1B` 分拆相关现金分配，形成较高初始债务 | 纯电子材料属性增强，但资产负债表从轻负债变为中等杠杆 |
| 2026-02 | 发布 Eon EUV photoresist，并配套 AR EUV underlayer、EUVSolv cleans | 试图从 EUV ancillary 扩到 EUV 光刻胶本体；若能获得主流先进逻辑/HBM 层认证，弹性大 |
| 2026-03 | 与 NVIDIA 合作探索材料科学创新，支持 AI/high-performance computing；宣布约 `$61.5M` 投资台湾 facility，预计 2027 年初投产 | NVIDIA 合作更偏 R&D/生态背书；台湾投资是客户贴近、local-for-local 和先进封装/半导体材料需求的订单前置线索 |
| 2026-03/04 | 推出无氟 UV/KrF photoresist 方案并披露 ArF immersion 方向进展；Emblem CMP pad 获 Edison Awards | 环保替代与高端 CMP 双线推进，利好长期产品结构 |

### 1.3 最新市场数据和估值

| 指标 | 最新值 | 日期/口径 | 备注 |
|---|---:|---|---|
| 股价 | `$147.33` | 2026-05-08 收盘，finance/market data | 2026-05-10 为周日 |
| 市值 | 约 `$30.9B` | 2026-05-08，按约 209.5M 股估算；StockAnalysis 约 `$30.1B` | 数据商因收盘价/股数更新时间略有差异 |
| Enterprise value | 约 `$33.7B` | StockAnalysis 统计页，2026-05 | 反映分拆后债务 |
| TTM P/E | `43.5x` | StockAnalysis，2026-05 | 按 EPS/归母利润口径；按 2025 GAAP EPS `$3.30` 与 2026-05-08 价格粗算约 `44.6x` |
| Forward P/E | `37.7x` | StockAnalysis，2026-05 | 与 2026 adjusted EPS 指引 `$3.55-3.95` 中点粗算约 `39.3x` 接近 |
| P/S | `6.3-6.5x` | 市值 / 2025 收入 `$4.754B` | 高于传统化工，接近优质半导体材料估值 |
| EV/EBITDA | `24.7x` | StockAnalysis，2026-05 | 按 TTM EBITDA；按 2026 指引中点 `$1.52B` 粗算约 `22.2x` |
| 2025 收入增速 | +10% | FY2025 | organic sales +10% |
| 2025 毛利率 | 46.2% | FY2025 | gross profit `$2.196B` |
| 2025 净利率 | 14.6%-15.3% | FY2025 | StockAnalysis 净利润 `$692M` 对收入为 14.6%；公司 GAAP net income `$729M` 对收入为 15.3% |
| 2025 调整后 operating EBITDA margin | 29.5% | FY2025 | `$1.402B` / `$4.754B` |
| 2026 收入指引 | `$4.97-5.17B` | 2026-02-26 FY2025 release | 中点 `$5.07B`，同比 +6.6% |
| 2026 调整后 EPS 指引 | `$3.55-3.95` | 2026-02-26 | 中点 `$3.75` |
| 2026 调整后 FCF 指引 | `$450-550M` | 2026-02-26 | 分拆后利息、税、独立公司成本会压低相对 2025 的 FCF 转化 |

### 1.4 资产负债表健康度

| 项目 | 2025-12-31 | 判断 |
|---|---:|---|
| Cash and cash equivalents | `$915M` | 现金充足 |
| Current assets / current liabilities | `$2.638B / $1.356B` | current ratio 约 `1.95x`，短期偿债健康 |
| Long-term debt | `$4.003B` | 分拆交易后债务显著上升 |
| 数据商 total debt | 约 `$4.53B` | 含其他债务/租赁等口径 |
| Net debt | 约 `$3.1-3.6B` | 约为 2025 adjusted EBITDA 的 `2.2-2.6x`，按数据商 debt/EBITDA 约 `3.1x` |
| 2025 operating cash flow | `$1.273B` | 现金生成能力强 |
| 2025 capex | 约 `$285M` | capex/revenue 约 6%，材料资产不算特别重 |
| 2025 FCF 粗算 | 约 `$988M` | 分拆前历史 FCF 强；2026 指引 FCF 明显低于此，反映独立公司利息、税、分拆成本和营运资本 |

健康程度：中等偏健康。业务质量和现金流强，短期流动性好；主要扣分项是分拆后净债务和可能的 PFAS/环境责任分担。按 2026 EBITDA 中点看，去杠杆可控，但估值对 2026-2027 AI 材料增长兑现比较敏感。

## 2. 最新和最近 4 次财报拆解

### 2.1 财报节奏说明

Qnity 2026Q1 财报电话会安排在 2026-05-12，尚未发布。下表使用最新已发布 2025Q4/FY2025、2025Q3 10-Q、Form 10/Q1 与 H1 披露以及 FY2025 release 的 Q4 2024 对比数据。Q1/Q2 2025 的部分分部值由 Q1、H1 与 Q3 9M 数据反推，已在表内标注。

### 2.2 最近五个季度核心数字

| 财报季度 | 发布/披露状态 | Net sales | YoY | Semiconductor Technologies | Interconnect Solutions | 毛利/净利 | EBITDA/利润率 | 订单、交期、取消率判断 | AI/DC/HPC 收入占比估计 |
|---|---|---:|---:|---|---|---|---|---|---|
| 2025Q4 | 2026-02-26 release / 10-K | `$1.190B` | +8% | 收入 `$661M`，YoY +7%；分部 EBITDA 约 `$232M`，margin 35.1% | 收入 `$529M`，YoY +9%；分部 EBITDA 约 `$136M`，margin 25.7% | gross profit `$549M`，GM 46.1%；GAAP net income 约 `$109M` | adjusted pro forma operating EBITDA `$349M`，margin 29.3% | 不披露 backlog/bookings；2026 指引中点 +6.6%，说明订单可见度稳健但不是爆发式；无取消率披露 | 估计 17%-20%，约 `$200-240M`；先进封装、AI PCB、热管理支撑 |
| 2025Q3 | 2025-11 10-Q / business update | `$1.276B` | +11% | 收入 `$693M`，YoY +8%；分部 EBITDA `$240M`，margin 34.6% | 收入 `$583M`，YoY +15%；分部 EBITDA `$152M`，margin 26.1% | gross profit `$575M`，GM 45.1%；net income `$223M` | 分部 EBITDA 合计 `$392M`；扣 corporate 后约 `$382M`，margin 约 29.9% | 分拆系统切换和客户预拉货可能抬高 Q3；订单强度来自 volume +11%，不是官方 backlog | 估计 18%-21%，约 `$230-270M`；Interconnect 斜率最强 |
| 2025Q2 | H1 与 Q1 数据反推 | `$1.170B` | 约 +6% | 收入约 `$644M`，YoY 约 +4%；分部 EBITDA 约 `$226M`，margin 35.1% | 收入约 `$526M`，YoY 约 +8%；分部 EBITDA 约 `$137M`，margin 26.0% | gross profit 约 `$540M`，GM 46.2%；net income 约 `$198M` | 分部 EBITDA 合计约 `$363M`，margin 31.0% | 订单未披露；Q2 是 AI/HBM/先进封装需求向 Interconnect 传导的早期阶段 | 估计 17%-19%，约 `$200-220M` |
| 2025Q1 | Form 10 / Q1 carve-out | `$1.118B` | 约 +14% | 收入 `$644M`，YoY 约 +11%；分部 EBITDA `$247M`，margin 38.4% | 收入 `$474M`，YoY 约 +17%；分部 EBITDA `$114M`，margin 24.1% | gross profit 约 `$531M`，GM 47.5%；historical net income `$199M`，pro forma EPS 会受独立债务影响更低 | 分部 EBITDA 合计 `$361M`，margin 32.3% | 消费/半导体库存修复 + AI 初期拉动；无 backlog 披露 | 估计 17%-19%，约 `$190-210M` |
| 2024Q4 | FY2025 release 对比期 | `$1.101B` | 基期 | 收入 `$616M`；分部 EBITDA 约 `$246M`，margin 39.9% | 收入 `$485M`；分部 EBITDA 约 `$117M`，margin 24.1% | gross profit `$515M`，GM 46.8%；net income `$221M` | adjusted pro forma operating EBITDA `$322M`，margin 29.2% | 2024 仍有电子材料库存周期影响；AI 端已开始成为叙事但收入占比低于 2025 | 公司披露 2024 data center/HPC/AI 约 15%，Q4 估计约 `$165M` |

### 2.3 Backlog / bookings / lead time / cancellation 的可验证结论

Qnity 不像设备商或服务器 OEM 那样披露 backlog，也没有按季度披露 bookings、book-to-bill、lead time 或取消率。对它更合适的订单框架是“客户 AVL/design-in + 长期供货协议 + 工厂贴近产能 + wafer starts/封装产能消耗”。

| 维度 | 官方披露 | 本文推断 |
|---|---|---|
| Backlog | 未披露 | 传统 backlog 不是核心指标；消耗性材料更多随客户产量和安全库存滚动采购 |
| Bookings / B2B | 未披露 | 2025Q3 revenue +11%、Q4 +8%、2026 revenue guide +4.5%-8.7%，暗示需求稳健但不是“订单翻倍” |
| Lead time | 未披露 | 已认证消耗材料通常以周到数月滚动交付；新材料认证/导入 6-24 个月；新产线如台湾投资预计 2027 年初开始贡献 |
| 取消率 | 未披露 | 合格材料替换成本高，终端取消率低于普通电子零件；但客户 wafer starts、HBM/CoWoS 延期会改变消耗节奏 |
| 关键订单线索 | SK hynix CMP pad 长协/MOU、台湾 `$61.5M` 投资、NVIDIA R&D 合作、Q3 volume 拉动 | 这些是订单可见度和技术路线信号，不应直接等同于已披露 backlog 金额 |

## 3. 2026 指引、收入占比和产品映射

### 3.1 2026 最新指引

| 2026 指标 | 指引 | 中点 | 对 2025 增长 | 观察 |
|---|---:|---:|---:|---|
| Net sales | `$4.97-5.17B` | `$5.07B` | +6.6% | 比 2025 +10% 放缓，但高于多数成熟电子材料周期品 |
| Adjusted pro forma operating EBITDA | `$1.465-1.575B` | `$1.520B` | +8.4% | EBITDA 增速快于收入，说明价格/ mix /成本效率有支撑 |
| Adjusted EPS | `$3.55-3.95` | `$3.75` | 约 +12% vs 2025 adjusted EPS `$3.35` | 独立公司利息负担仍在，但成本优化和 buyback 支撑 EPS |
| Adjusted free cash flow | `$450-550M` | `$500M` | 低于 2025 历史 FCF | 分拆成本、税、独立公司成本、营运资本影响 |

### 3.2 2025-2026 收入结构判断

| 业务/产品组 | 2025 收入估计 | 2025 占比 | 2026 基准收入估计 | 2026 增速估计 | AI 相关性 | 说明 |
|---|---:|---:|---:|---:|---|---|
| CMP pads/slurries + post-CMP clean/removers | `$0.90B` | 19% | `$0.98B` | +8%-12% | 高 | 先进逻辑、HBM DRAM、CoWoS/RDL planarization、SK hynix 长协是关键 |
| Lithography materials：Eon/Epic/UV/AR/EUVSolv | `$0.65B` | 14% | `$0.70B` | +7%-12% | 中高 | Eon EUV 是小基数期权；DUV/ArFi/KrF 与 HBM、先进逻辑同步 |
| Advanced packaging wet process / RDL / TSV / Cu pillar / dielectric | `$0.55B` | 12% | `$0.70B` | +20%-30% | 很高 | 与 CoWoS-L/RDL、HBM microbump、2.5D/3D、AI ASIC 直接相关 |
| AI PCB / IC substrate / high-speed interconnect materials | `$1.15B` | 24% | `$1.28B` | +10%-15% | 很高 | Riston、Circuposit、Microfill、Interra、Pyralux/Kapton、metal finishing 受 AI rack/PCB/ABF 牵引 |
| Laird thermal / EMI / assembly materials | `$0.55B` | 12% | `$0.66B` | +18%-25% | 很高 | 100kW+ rack、liquid cooling、optical/AI switch、GPU/ASIC 热界面拉动 |
| 其他：display、一般 metal finishing、industrial seals、consumer flex、silver nanowire 等 | `$0.95B` | 20% | `$0.75B-0.85B` | -5% 至 +3% | 低到中 | 可现金流打底，但不是 AI thesis 核心 |

2026 最突出的业务：先进封装材料、AI PCB/IC substrate materials、热管理/EMI、CMP。公司短期真正侧重的不是单一 Eon EUV 胶，而是“半导体工艺材料 + 先进封装 + 互连/热材料”的组合，覆盖从 wafer 到 package 到 board/rack 的多个瓶颈。

### 3.3 跳过或降权的业务

以下业务仍可能贡献现金流，但不是本文 AI 高增长重点：OLED/display 材料、一般 plating-on-plastics、传统 automotive/consumer flex、普通工业 metal finishing、低端 PCB 化学品、非半导体 Kalrez/industrial seals、silver nanowire 透明导电材料。例外是 Kalrez 在半导体设备密封件中的高端应用仍需跟踪，但它更像半导体 capex/设备稼动率受益，不是 AI rack 直接弹性。

## 4. 关键产品当前贡献、AI 重要性和供需紧张程度

评分：1 = 低，5 = 高。收入为 2025 估算。

| 关键产品/业务 | 代表产品和型号 | 2025 收入贡献估计 | 2025 增速估计 | AI 基建重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价能力 | 当前判断 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| CMP pads/slurries/cleans | Emblem CMP pad、Ikonic、IC1000、Acuplane/Novaplane/Optiplane/Klebosol slurry、EKC clean/remover | `$0.85-1.05B` | +10%-15% | 4 | 4 | 3 | 4 | 先进逻辑/HBM/CoWoS 都要 CMP；pad + slurry + clean 配方认证深，替换成本高 |
| Lithography：EUV/ArFi/KrF stack | Eon EUV PR、AR EUV underlayer、EUVSolv cleans、Epic ArF immersion、UV KrF/无氟 photoresist | `$0.55-0.75B` | +8%-12% | 4 | 3 | 3 | 3 | Eon EUV 是新增期权，但 EUV 胶主战场仍由日系/TOK/JSR/Shin-Etsu/Fujifilm 等把持 |
| Advanced packaging RDL/TSV/Cu pillar/dielectric | Solderon BP TS7000、Intervia 8540HSP、Cyclotene advanced packaging dielectric、Cu RDL、TSV Cu、UBM、bump PR/removers | `$0.45-0.65B` | +20%-30% | 5 | 5 | 4 | 4 | 与 CoWoS-L/RDL、HBM4、AI ASIC 直接耦合，单耗随 package 面积和 RDL 层数上升 |
| AI PCB / IC substrate / interconnect materials | Riston DI86/DI16/DWB81M dry film、Circuposit 6800W、Microfill EVF-IV、Copper Gleam PPR、Interra HK04J、Kapton/Pyralux laminates | `$1.05-1.25B` | +12%-18% | 5 | 4 | 4 | 3 | AI server board、switch board、substrate、CPC/top-side copper 等都提高材料规格 |
| Laird thermal/EMI | Tgel 600、Tpcm 7000、Tputty 910、MaxAir vent panels、absorbers、EMI shielding、thermal pads/gels | `$0.45-0.65B` | +15%-25% | 5 | 5 | 4 | 4 | 100kW+ rack 和液冷让 TIM/EMI 从普通配件变成系统可靠性材料 |
| 小基数期权：玻璃基板/TGV/CPO/photonic packaging 材料 | Cyclotene、low-loss dielectric、optical/thermal adhesives、Kapton/Pyralux flex for optical modules | `<$0.10-0.20B` | +20%+，但基数小 | 3 | 2 | 3 | 3 | 2026 更多是认证/样品；若 2027 CPO/玻璃基板 design-in，估值弹性大于收入弹性 |

## 5. 未来一年产品收入三情景预测

未来一年按 2026 年全年到 2027 年初订单/收入节奏理解。产品收入为本文估计，非公司披露。

| 产品/业务 | 基准 B：一年后收入/增速 | 乐观 O：一年后收入/增速 | 极度乐观 X：一年后收入/增速 | AI 重要性变化 | 供需和溢价判断 |
|---|---|---|---|---|---|
| CMP pads/slurries/cleans | `$0.98B`，+9% | `$1.08B`，+20% | `$1.20B`，+33% | HBM4/先进逻辑增加 CMP 层数和良率要求 | 基准下供应可控；乐观下 SK hynix/HBM 和先进封装客户拉动高端 pad 溢价 |
| Lithography stack | `$0.70B`，+8% | `$0.78B`，+20% | `$0.88B`，+35% | Eon EUV 进入更多客户评价；ArFi/KrF 无氟替代打开 ESG/合规需求 | 最大不确定是 EUV 胶认证；若只是 ancillary，增速较温和 |
| Advanced packaging RDL/TSV/Cu pillar/dielectric | `$0.70B`，+27% | `$0.82B`，+49% | `$0.95B`，+73% | CoWoS-L/RDL、HBM4 microbump、AI ASIC 使其从利基变成核心 | 供给紧张度最高；配方认证和良率代价支撑溢价 |
| AI PCB/IC substrate/interconnect | `$1.28B`，+11% | `$1.42B`，+23% | `$1.60B`，+39% | 224G/448G、AI switch、GB300/NVL72、1.6T optical 拉动高频/高可靠材料 | 竞争比半导体工艺材料更分散，但客户认证和工艺包仍有粘性 |
| Laird thermal/EMI | `$0.66B`，+20% | `$0.78B`，+42% | `$0.95B`，+73% | rack 功率上升、液冷普及，TIM/EMI 单机架价值量上升 | 高端定制材料供需偏紧；客户替换需重新做热/可靠性验证 |
| 小基数：glass/TGV/CPO/photonic packaging | `$0.12B`，+20% | `$0.18B`，+60% | `$0.28B`，+150% | 2026-2027 主要是 design-in，不是大收入 | 极度乐观需要 CPO/玻璃基板提前进入 hyperscaler 标准平台 |

公司整体收入三情景：基准 `$5.05-5.15B`，接近公司指引；乐观 `$5.25-5.40B`，需要 AI 材料和 Interconnect 同时超预期；极度乐观 `$5.55-5.75B`，需要 GB300/Rubin/HBM4/ASIC、AI rack 和材料认证全部顺利，且非 AI 业务不拖累。

## 6. BOM 拆分、单位内容量和价格传导链

Qnity 产品多为材料和工艺包，不像 GPU、光模块或服务器电源那样有公开 BOM。下表为基于先进晶圆、封装、PCB、rack 热管理和 optical module 材料单耗的估算，用于量级判断。

| 产品/业务 | 在 AI 技术栈里的真实位置 | 每 GPU/ASIC 内容量估计 | 每 rack 内容量估计 | 每 MW 内容量估计 | 每 optical port 内容量估计 | 价格传导链 |
|---|---|---:|---:|---:|---:|---|
| CMP pads/slurries/cleans | 先进逻辑/HBM wafer CMP、CoWoS/RDL planarization、post-CMP defect control | `$2-10/GPU equivalent`，取决于逻辑 die、HBM stacks 和良率要求 | `$150-900/NVL72 equivalent` | `$2k-15k/MW IT` | 基本无直接口径 | Hyperscaler demand -> GPU/ASIC/HBM wafer starts -> foundry/memory fab -> CMP pad/slurry/clean 消耗；价格靠认证和良率价值传导 |
| Lithography stack | EUV/ArFi/KrF photoresist、underlayer、developer/clean | `$1-8/GPU equivalent` | `$75-600/rack` | `$1k-10k/MW` | 无直接口径 | 先进节点/HBM 层数 -> 光刻材料用量；EUV 胶若进主层，ASP 和毛利显著高于 ancillary |
| Advanced packaging RDL/TSV/Cu pillar/dielectric | CoWoS-L/RDL、HBM microbump/TSV、Cu pillar、UBM、临时/后清洗 | `$5-25/GPU/ASIC package` | `$360-1,800/NVL72 rack` | `$3k-25k/MW` | CPO/photonic package `$0.2-2.0/port`，目前小 | GPU/ASIC vendor -> TSMC/OSAT/HBM -> RDL/TSV/plating/clean 材料；良率和可靠性决定溢价 |
| AI PCB/IC substrate/interconnect | IC substrate wet process、ABF/FC-BGA 周边、GPU baseboard、switch board、high-speed PCB/flex | `$5-25/GPU`，服务器和交换板分摊后可能更高 | `$0.8k-4.0k/rack` | `$8k-45k/MW` | `$0.05-0.50/800G-1.6T port` | NVIDIA/ASIC rack -> ODM/OEM/PCB/substrate -> dry film、metallization、laminate；金属可 pass-through，配方和低损耗材料有溢价 |
| Laird thermal/EMI | GPU module/rack TIM2、gap filler、phase change、EMI absorber/shield、vent panels | `$5-25/GPU/accelerator` | `$0.5k-2.5k/rack`，高功率 rack 可更高 | `$5k-30k/MW` | `$0.05-0.30/port`，CPO/linear optics 可能更高 | Rack power density -> thermal design -> ODM/OEM/cooling integrator -> Laird 材料；热可靠性验证提升替换成本 |

### 6.1 当前产能能力、采纳程度和认证阶段

| 产品/业务 | 当前产能能力，收入口径 | 供应链采纳程度 | 认证阶段 | 关键事实 |
|---|---:|---|---|---|
| CMP pads/slurries/cleans | 约 `$0.9-1.1B/年` | 已在主流晶圆厂/存储厂 HVM；SK hynix 长协/MOU 提升 HBM/DRAM 能见度 | 高端产品多为 HVM/AVL；Emblem 属新平台客户导入期 | CMP 是 Qnity 最成熟、最能变现的半导体工艺材料之一 |
| Lithography stack | 约 `$0.6-0.8B/年` | ArFi/KrF/underlayer/clean 已有客户基础；Eon EUV 为 2026 新推 | Eon EUV 仍应视为 sampling/customer qualification；AR/EUVSolv ancillary 更成熟 | EUV 胶主赛道壁垒极高，不能假设快速拿大份额 |
| Advanced packaging RDL/TSV/Cu pillar/dielectric | 约 `$0.5-0.7B/年` | OSAT/foundry/先进封装/载板链采纳程度高，AI 高端项目提升单耗 | RDL/TSV/Cu pillar 量产；Cyclotene/玻璃/新型 dielectric 更多 NPI/qualification | 与 CoWoS-L/RDL、HBM4、AI ASIC 节奏最同频 |
| AI PCB/IC substrate/interconnect | 约 `$1.1-1.3B/年` | PCB/substrate 产业链大量采用；中国 CPCA 2026 展示面向 AI/data center 的 DI86、DI16、DWB81M 等 | 成熟 HVM + 新高频/高密度材料持续认证 | 高速互连和 AI server PCB 使 Interconnect 增速高于公司平均 |
| Laird thermal/EMI | 约 `$0.5-0.7B/年` | 服务器、网络、光模块、汽车/工业已有广泛 design-in | 平台级 thermal/EMI 验证，客户切换需重新验证 | 直接受益 100kW+ rack、液冷和高密度 AI switch |

## 7. 一年后产能能力、采纳和认证三情景

| 产品/业务 | 基准 B | 乐观 O | 极度乐观 X |
|---|---|---|---|
| CMP pads/slurries/cleans | 收入能力 `$1.05B`；SK hynix/HBM 客户逐步放量；Emblem 继续多客户导入 | 收入能力 `$1.15B`；HBM4/DRAM/EUV CMP 订单提前；高端 pad 供给局部紧 | 收入能力 `$1.25B+`；HBM wafer starts 和 CoWoS/RDL CMP 同时紧，pad 配方成为短交期瓶颈 |
| Lithography stack | 收入能力 `$0.75B`；Eon EUV 维持评价/小批量；无氟 KrF/ArFi 样品增加 | 收入能力 `$0.85B`；Eon 至少获得 1-2 个客户关键层前置认证或非关键层量产 | 收入能力 `$1.0B`；EUV 胶从 ancillary 变成主流层二供，概率低但估值影响大 |
| Advanced packaging RDL/TSV/Cu pillar/dielectric | 收入能力 `$0.80B`；CoWoS-L/RDL 和 HBM4 NPI 拉动 | 收入能力 `$0.95B`；AI ASIC/OSAT 外溢订单显著提升 | 收入能力 `$1.10B+`；panel-level/RDL/玻璃基板材料提前获得 hyperscaler design-in |
| AI PCB/IC substrate/interconnect | 收入能力 `$1.35B`；GB300/NVL72、AI switch、800G/1.6T 板材需求稳步增长 | 收入能力 `$1.55B`；224G/448G 互连和高端 substrate 同时紧 | 收入能力 `$1.75B+`；rack-scale ASIC 和 CPO/optical engine 提前拉动新材料 |
| Laird thermal/EMI | 收入能力 `$0.75B`；100kW+ rack 放量，TIM/EMI design-in 增加 | 收入能力 `$0.90B`；300-600kW rack 和液冷冷板界面材料加速 | 收入能力 `$1.10B+`；1MW rack/高热流密度平台提前，金属/phase-change/CNT 类 TIM 进入更多量产项目 |

## 8. 基于真实订单线索和供给的未来一年增速判断

### 8.1 订单线索的可信度分层

| 线索 | 类型 | 对收入的含义 | 可信度 |
|---|---|---|---|
| 2026 revenue guide `$4.97-5.17B` | 官方财务指引 | 公司层面最硬；意味着 +4.5%-8.7% | 高 |
| 2025Q3/Q4 分部增长，尤其 Interconnect Q3 +15%、Q4 +9% | 已披露收入 | AI PCB/热/先进封装已在收入中体现 | 高 |
| SK hynix long-term CMP pad MOU | 官方客户长协/MOU | 对 HBM/DRAM CMP pad 有中长期正面信号，但无金额 | 中高 |
| 台湾 `$61.5M` facility，预计 2027 年初投产 | 官方 capex/产能 | 说明客户贴近需求强，可能带来 `$80-150M/年` 成熟收入能力，2026 贡献有限 | 中 |
| NVIDIA material science collaboration | 官方合作 | 技术背书强，但不是采购订单；更利于长期材料 design-in | 中 |
| 项目内 AI 产业链判断：2026-2027 HBM/CoWoS/ABF/液冷/光模块为瓶颈 | 行业模型 | 提供 Qnity 产品增长上限和节奏校验 | 中高 |

### 8.2 未来一年增速预测

| 产品/业务 | 基准增速 | 乐观增速 | 极度乐观增速 | 约束和取消风险 |
|---|---:|---:|---:|---|
| CMP pads/slurries/cleans | +8%-12% | +18%-22% | +30%+ | HBM/DRAM wafer starts 和客户认证；若 HBM 扩产延后，消耗递延但不完全取消 |
| Lithography stack | +7%-12% | +18%-22% | +30%-40% | EUV 胶认证是硬约束；若只是 underlayer/clean，增长接近基准 |
| Advanced packaging RDL/TSV/Cu pillar/dielectric | +20%-30% | +40%-55% | +65%-80% | CoWoS/RDL/OSAT 外溢和 AI ASIC 封装；若 CoWoS 产能卡住，材料订单递延 |
| AI PCB/IC substrate/interconnect | +10%-15% | +22%-28% | +35%-45% | AI rack 交付和高端 PCB/substrate 产能；中国国产替代和价格压力是风险 |
| Laird thermal/EMI | +18%-25% | +35%-45% | +60%-80% | rack 功率密度、液冷标准化、ODM design-in；若客户平台推迟，订单递延 |
| 公司总收入 | +5%-8% | +9%-12% | +13%-18% | 非 AI 业务拖累、债务/利息不影响收入但影响 EPS；公司指引是短期硬锚 |

## 9. 竞争格局、主流技术和替代风险

| 产品/业务 | 主要竞争对手 | Qnity 优势 | 是否未来主流 | 替代风险 | 客户替换成本 |
|---|---|---|---|---|---|
| CMP pads/slurries/cleans | Entegris/CMC Materials、Fujimi、Resonac、Fujifilm、Anji、SKC/Enf 等 | pad + slurry + clean 组合、历史 DuPont/IC1000 基础、客户共研深 | 是。先进逻辑/HBM/CoWoS 都依赖 CMP | 客户二供、国产 slurry、价格压力 | 高。缺陷/刮伤/良率风险使替换周期长 |
| Lithography stack | TOK、JSR/Inpria、Shin-Etsu、Fujifilm、Merck/EMD、Sumitomo、Dongjin | 既有 underlayer/clean 和 ArFi/KrF 基础，Eon EUV 打开新空间 | EUV/ArFi/KrF 仍是 2026-2027 主流 | EUV 胶本体竞争非常强，Eon 需要证明性能/defect/dose | 极高。关键层 PR 切换需长认证 |
| Advanced packaging RDL/TSV/Cu pillar/dielectric | MKS/Atotech、Element Solutions/MacDermid Alpha、Uyemura、Technic、JCU、Okuno、Resonac、Shanghai Sinyang、Anji | 工艺包宽、Cu/RDL/clean/PR/dielectric 全线覆盖 | 是。CoWoS-L/RDL、HBM4、AI ASIC 推动 RDL 和 Cu pillar 成主线 | OSAT 自有配方、MKS/MacDermid 强竞争、中国替代 | 高。电镀/清洗/介质缺陷会直接影响封装良率 |
| AI PCB/IC substrate/interconnect | Ajinomoto、Resonac、Panasonic、MGC、Rogers、Isola、Taiyo、MKS/Atotech、MacDermid、Chemleader、中国 PCB 化学材料商 | Riston/Circuposit/Microfill/Kapton/Pyralux 品牌和工艺生态，贴近 PCB/substrate 客户 | 是。AI rack 需要更高层数、更低损耗、更高可靠 PCB/基板 | ABF 关键材料 Ajinomoto 仍强；中国供应链降价 | 中高。PCB 化学品二供比前道容易，但高端板良率约束强 |
| Laird thermal/EMI | Henkel/Bergquist、Honeywell、Dow/Carbice、Indium、Parker Chomerics、Boyd、3M、Shin-Etsu、Fujipoly、t-Global | Laird 在 thermal + EMI + venting + absorbers 组合强，系统级客户深 | 是。100kW+ rack 让 TIM/EMI 变成可靠性瓶颈 | 金属 TIM/CNT/graphite/diamond 路线替代传统 pad/gel；客户自研热设计 | 中高。热循环、泵出、压缩永久变形、EMI 测试需重做 |
| Glass/TGV/CPO/photonic packaging 材料 | Corning/AGC/TOPPAN/SKC、MKS/MacDermid、Brewer、3M、Henkel、DELO、Toray、Merck 等 | Cyclotene/low-loss dielectric/Kapton/flex/thermal 组合可卡位 | 2026 非主流，2027-2028 期权 | 路线不确定，CPO serviceability/laser/thermal 难题 | 早期较低，量产后升高 |

技术主流判断：Qnity 最稳的是成熟主流路线里的材料升级，而不是押单一颠覆性路线。2026-2027 主流仍是 low-NA EUV + ArFi、HBM3E/HBM4、CoWoS-S/L/RDL、ABF/FC-BGA、800G/1.6T pluggable + 高速 PCB/铜互联、100kW+ 液冷 rack。Qnity 的材料大多是这些主流路线的增量耗材。CPO、玻璃基板、panel-level 2.5D 是赔率高但收入靠后的路线。

## 10. 跟踪指标

1. 2026-05-12 Q1 2026：收入是否超过 `$1.24B` 季均指引、Interconnect 是否继续跑赢 Semiconductor Technologies、毛利率是否保持 46%+。
2. 公司是否开始披露 AI/data center/HPC 收入占比；若从 2024 的 15% 提升到 2026 的 20%+，估值逻辑更稳。
3. Eon EUV：是否披露客户 sampling、qualification、non-critical layer 或 HVM 进展。
4. SK hynix CMP pad 长协：是否变成实际收入上修、HBM4 相关 CMP pad 认证或扩产。
5. 台湾 `$61.5M` facility：2027 年初是否按期投产，服务哪些产品组。
6. Advanced packaging：Qnity 是否披露 RDL/TSV/Cu pillar/advanced packaging materials 增速，尤其 CoWoS-L/RDL/OSAT 外溢。
7. Laird：是否出现 AI rack、liquid cooling、optical module、CPO 相关 design win。
8. 资产负债表：net leverage 是否按 FCF 去杠杆；share repurchase 是否影响去杠杆速度。
9. 中国业务：33% 中国收入是否受国产替代、出口管制或客户 capex 影响。

## 11. 主要来源

- Qnity FY2025 results release, 2026-02-26: <https://ir.qnityelectronics.com/press-releases/detail/50/qnity-reports-fourth-quarter-and-full-year-2025-results>
- Qnity 2025 Form 10-K: <https://ir.qnityelectronics.com/sec-filings/all-sec-filings/content/0002058873-26-000010/q-20251231.htm>
- Qnity 2025Q3 Form 10-Q: <https://ir.qnityelectronics.com/sec-filings/all-sec-filings/content/0002058873-25-000023/q-20250930.htm>
- Qnity 2025H1 / Form 10 exhibit financial update: <https://ir.qnityelectronics.com/sec-filings/all-sec-filings/content/0001193125-25-240313/d21160dex991.htm>
- StockAnalysis Q statistics and valuation page: <https://stockanalysis.com/stocks/q/statistics/>
- Qnity Advanced Computing and AI portfolio: <https://www.qnityelectronics.com/advanced-computing-and-artificial-intelligence.html>
- Qnity Eon EUV photoresist announcement, 2026-02: <https://www.qnityelectronics.com/news/qnity-expands-offerings-for-extreme-ultraviolet-lithography.html>
- Qnity non-fluorine photoresist innovation, 2026-03: <https://www.qnityelectronics.com/news/qnity-advances-more-sustainable-semiconductor-manufacturing-through-photoresist-innovation.html>
- Qnity and SK hynix CMP pad long-term supply agreement/MOU, 2025-10: <https://www.dupont.com/news/qnity-and-sk-kynix-sign-long-term-cmp-pad-supply-agreement.html>
- Qnity Taiwan facility investment, 2026-03: <https://ir.qnityelectronics.com/press-releases/detail/51/qnity-announces-61-5-million-investment-in-new-advanced-semiconductor-research-manufacturing-facility>
- Qnity / NVIDIA collaboration announcement, 2026-03: <https://www.qnityelectronics.com/news/qnity-collaborates-with-nvidia-to-accelerate-innovation-for-semiconductor-and-advanced-electronics-materials.html>
- Qnity CPCA 2026 interconnect materials: <https://www.qnityelectronics.com/news/ai-enabling-solutions-at-cpca-show-2026.html>
- Qnity DesignCon 2026 high-speed/thermal materials: <https://www.qnityelectronics.com/news/qnity-at-design-con-2026.html>
- Qnity Emblem CMP pad Edison Awards, 2026-04: <https://www.qnityelectronics.com/news/qnity-wins-2026-edison-award.html>
- 项目内非公司调研文件：《行业调研/AI头部芯片市场占比和规模.md》《行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md》《行业调研_先进封装材料与热界面材料_2026.md》《行业调研_硅片_光刻胶与前道材料_2026-05-08.md》《行业调研_先进封装湿化学与表面处理材料_2026-05-08.md》《designcon_2026_conference_update.md》《chiplet_summit_2026_update.md》。

---

非投资建议。本文的产品组拆分、AI 收入占比、单位 BOM 内容量和三情景预测均为基于公开披露和产业链模型的推算，应以后续 Qnity 10-Q、earnings call、客户认证和订单披露更新。

