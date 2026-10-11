# 公司：ONTO Onto Innovation Inc.

> 生成日期：2026-05-09。美国股市 2026-05-09 为周六，股价采用 2026-05-08 收盘价。  
> 研究口径：只新做本报告；未参考 `工作台v5/公司调研` 目录下任何既有公司报告。公司披露只有一个 reportable segment；文中 advanced packaging、advanced nodes、software/services 等为管理层电话会使用的市场口径，部分细分收入为本报告推算。

## 0. 结论先行

Onto Innovation 是半导体 process control 设备公司，核心产品是量测、检测、缺陷分类、3D metrology、先进封装光刻和良率软件。它不是直接卖给 AI 数据中心的公司，而是卖给 TSMC/三星/SK hynix/OSAT/先进封装厂/存储厂的设备供应商；AI 受益链条是：AI GPU/ASIC/HBM 需求增加 -> 先进节点、HBM、CoWoS/2.5D/3D/面板级封装扩产 -> 更高检测量测强度 -> ONTO 工具订单。

最核心的投资叙事已经从“中型检测量测设备商”变成“AI HBM + 2.5D/3D advanced packaging 的高弹性 process-control 供应商”。2026Q1 收入 2.919 亿美元，同比约 +9.5%、环比约 +9.4%；管理层给 2026Q2 收入指引 3.20-3.30 亿美元，并把 2026 全年收入增速上调到 `>30%`、advanced packaging 增速上调到 `>50%`、advanced nodes 增速上调到约 `25%`。

订单能见度明显改善。2025Q4 公司披露 backlog 近 3 个月翻倍，达到约两个季度收入量级；同时拿到一个 HBM 客户 `>$240M` 的 Dragonfly 2D inspection + 3D bump metrology volume purchase agreement，覆盖到 2027。2026Q1 又披露 Dragonfly G5 在领先 2.5D logic 客户和 HBM 客户处完成 qualification，3Di 在当季新增 10+ 订单，JetStep 获两家 AI device packaging suppliers qualification。

估值已经明显反映乐观预期。2026-05-08 收盘价 284.67 美元，市值约 141.6 亿美元；StockAnalysis 同日口径 trailing PE 132.4x、forward PE 35.9x、PS 13.7x、forward PS 10.0x。资产负债表很强，现金/短投约 6.54 亿美元、基本无债、current ratio 6.15，但 Rigaku 27% 股权投资约 7.10 亿美元将在 2026H2 消耗现金或引入融资，净现金缓冲会下降。

## 1. 公司业务、产业链位置与近三年变化

### 1.1 公司做什么

ONTO 的业务是半导体制造过程控制，覆盖前道和后道先进封装：

| 层级 | 主要产品/能力 | 应用 |
|---|---|---|
| Advanced packaging inspection/metrology | Dragonfly G3/G5、3Di、EchoScan、Clearfind、sub-surface inspection | HBM、2.5D logic、CoWoS-like package、chiplet、microbump/TSV/hybrid bonding、CPO |
| Advanced packaging lithography/inspection | JetStep、Firefly、StepFAST、PACE lab | panel-level packaging、大尺寸 RDL、large-format heterogeneous packaging |
| Advanced nodes metrology | Atlas/Atlas G6 OCD、Iris films、integrated metrology、Ai Diffract、SpectraProbe、AiGen X | GAA、DRAM/HBM、NAND、TSV、critical films、1nm/2nm 路线 |
| Materials/electrical metrology | Semilab USA: FAaST、CnCV、MBIR | wafer contamination、materials characterization、surface charge metrology、advanced logic/memory/AI packaging |
| Yield software/services | Discover yield management、defect classification、pattern analysis、parts/service | 良率数据、recipe、installed base 服务 |

在产业链位置上，ONTO 是设备端的“良率保险”和“产能爬坡加速器”。AI 芯片越贵、封装越大、HBM 堆叠越复杂，单点 defect 的经济损失越高，客户就越愿意为 100% inspection、更快 recipe、更高 throughput 和更低 nuisance defect 付费。

### 1.2 投资人心中的公司形象

投资人现在看 ONTO，重点不是传统 mature-node cyclicality，而是三条 AI 制造链弹性：

1. HBM/2.5D/3D advanced packaging：Dragonfly、3Di、EchoScan 是最核心弹性。
2. GAA/DRAM/HBM advanced nodes：Atlas G6/OCD、Iris films、integrated metrology 带来前道弹性。
3. 新 metrology 组合：Semilab surface charge/materials + Rigaku X-ray + Ai Diffract，可能把 ONTO 从纯 optical process control 扩到 hybrid optical/X-ray metrology。

### 1.3 近三年重大业务变化

| 时间 | 事件 | 对业务含义 |
|---|---|---|
| 2023 | 披露 Dragonfly G3 for HBM / chip-on-wafer GPU package 订单超过 1 亿美元，交付延伸到 2024 | AI advanced packaging 从“机会”变成订单 |
| 2024-2025 | 3Di、sub-surface inspection、EchoScan 持续进入 HBM、2.5D logic、wafer bonding、CPO 场景 | 从 2D surface inspection 扩为 2D+3D+subsurface 综合平台 |
| 2025-08 | 宣布收购 Semilab International 的部分材料分析产品线 | 增加 surface charge、materials characterization、wafer contamination，提升 advanced node/AP 覆盖 |
| 2025-11-17 | 完成 Semilab USA 相关产品线收购，交易价值约 4.95 亿美元 | 2026 贡献低百百万美元级收入，Q1 已贡献约 2,500 万美元 |
| 2026-03 | Launch Dragonfly G5，HBM manufacturer 完成 HBM4 评估并给出 double-digit Dragonfly G5 与 3Di 订单承诺 | G5 从验证进入 Q2 交付，直接对应 HBM4 和更小 interconnect |
| 2026-04-20 | 宣布与 Rigaku 战略合作，并拟以约 7.10 亿美元收购 Rigaku 27% 股权 | 布局 X-ray/CD-SAXS + Ai Diffract hybrid metrology，不并表但可能带来接近 100% 毛利的软件授权 |
| 2026Q1 | Dragonfly G5 在领先 2.5D logic 客户、HBM 客户完成 qualification；JetStep 在两家 AI device packaging suppliers qualified | 先进封装客户面扩大，panel-level packaging 2027 可能变成新弹性 |

## 2. 股价、估值、利润率与资产负债表

### 2.1 最新市场数据

| 指标 | 数值 | 日期/口径 |
|---|---:|---|
| 股价 | 284.67 美元 | 2026-05-08 收盘 |
| 盘后价 | 287.40 美元 | 2026-05-08 19:56 EDT |
| 市值 | 141.6 亿美元 | StockAnalysis，2026-05-08 |
| Enterprise value | 135.1 亿美元 | StockAnalysis，2026-05-08 |
| TTM revenue | 10.3 亿美元 | StockAnalysis，2026-05-08 |
| TTM net income | 1.064 亿美元 | StockAnalysis，2026-05-08 |
| Trailing PE | 132.41x | StockAnalysis，2026-05-08；受 Semilab purchase accounting/摊销影响 |
| Forward PE | 35.88x | StockAnalysis，2026-05-08 |
| PS / Forward PS | 13.74x / 10.03x | StockAnalysis，2026-05-08 |
| TTM gross margin | 54.19% | StockAnalysis，2026-05-08 |
| TTM operating margin | 18.81% | StockAnalysis，2026-05-08 |
| TTM net margin | 10.33% | StockAnalysis，2026-05-08 |
| 现金与等价物/短投 | 6.54 亿美元 | StockAnalysis 与 2026Q1 披露 |
| 总债务 | n/a/基本无债 | StockAnalysis，2026-05-08 |
| Current ratio / quick ratio | 6.15 / 4.48 | StockAnalysis，2026-05-08 |
| TTM FCF | 2.388 亿美元 | StockAnalysis，2026-05-08 |

### 2.2 财务健康评估

财务健康度高。ONTO 2026Q1 末现金/短投约 6.54 亿美元，working capital 约 11.1 亿美元，基本无债，TTM FCF 2.39 亿美元。对设备公司来说，这是很强的抗周期资产负债表。

主要变化是 Rigaku 交易。公司拟以约 7.10 亿美元购买 Rigaku 27% 股权，预计 2026H2 closing，且不并表。管理层称主要用手头现金，并有融资安排；因此交易完成后净现金会显著下降，若使用债务则 leverage 从“几乎无债”变为“低到中等杠杆”。战略上，它换来 X-ray/CD-SAXS + Ai Diffract 的长期期权；短期上，它降低资产负债表缓冲。

毛利率口径需要拆开看。2026Q1 GAAP gross margin 50.1%，主要受收购摊销、采购会计、重组及 M&A 费用影响；non-GAAP gross margin 55.7%。管理层指引 2026Q2 non-GAAP gross margin 56.0%-56.5%，Q3/Q4 每季至少再提升约 50bps，并希望 Q4 exit operating margin `>30%`。

## 3. 最近五个季度财报与订单/交期

| 财报期 | 收入与增速 | 利润率/EPS | 市场口径收入拆分 | 订单、backlog、lead time | AI 数据中心相关判断 |
|---|---:|---:|---|---|---|
| 2026Q1 | 2.919 亿美元；YoY +9.5%；QoQ +9.4% | GAAP GM 50.1%；non-GAAP GM 55.7%；GAAP EPS 0.67；non-GAAP EPS 1.42 | Specialty + AP 约 1.60 亿美元，其中 AP 约 1.07 亿美元、Semilab 约 0.25 亿美元、其余 specialty；advanced nodes 约 0.80 亿美元，其中 memory/DRAM 约 60%；software/services 为剩余约 0.52 亿美元 | Q2 指引 3.20-3.30 亿美元；backlog 为 record；G5 Q1 已出货 several systems，Q2/Q3/Q4 继续增长；3Di 新增 10+ orders；JetStep 两家 packaging suppliers qualified | 严格口径 AP + HBM/DRAM advanced-node 约 1.55 亿美元，约 53%；若计入部分 GAA/HPC logic 与 AI supply-chain services，广义约 55%-60% |
| 2025Q4 | 2.669 亿美元；YoY +1.1%；QoQ +22% | GAAP GM 46.4%；non-GAAP GM 54.6%；GAAP EPS 0.21；non-GAAP EPS 1.26 | Specialty + AP 约 1.45 亿美元，略超收入一半；其中 2.5D packaging revenue QoQ 近翻倍；Semilab 约 900 万美元；advanced nodes 0.72 亿美元；software/services 约 0.50 亿美元 | HBM VPA `>$240M` through 2027，其中 `>$60M` 3D bump metrology；JetStep + 8 Firefly 大面板封装厂订单；backlog 近 3 个月翻倍，约两个季度收入量级；precision optics lead time 拉长 | AI packaging 从 Q3 低点反弹，订单能见度显著提高；HBM/CoWoS/OSAT/panel 全部进入管理层重点 |
| 2025Q3 | 2.182 亿美元；YoY -13.5%；QoQ -14.0% | GAAP GM 50.7%；non-GAAP GM 54.0%；GAAP EPS 0.57；non-GAAP EPS 0.92 | Specialty + AP 1.13 亿美元，占 52%；advanced nodes 0.54 亿美元，占 25%；software/services 0.51 亿美元，占 23% | Dragonfly 3Di fully qualified by two major HBM customers，并拿到 2.5D logic AI packaging 订单；Q4 指引 2.50-2.65 亿美元；预计 Q4 Specialty + AP 反弹到约 1.50 亿美元 | 这是 2025 低点，主要是 advanced nodes timing/pause；AI packaging/HBM qualification 反而增强 |
| 2025Q2 | 2.536 亿美元；YoY +5%；QoQ -4.9% | GAAP GM 48.2%；non-GAAP GM 54.5%；GAAP EPS 0.69；non-GAAP EPS 1.25 | Advanced nodes 0.89 亿美元，占 35%；Specialty + AP 1.17 亿美元，占 46%；software/services 0.48 亿美元，占 19% | Dragonfly 3Di 已向 10+ customers 出货；advanced applications AI packaging 当季 Dragonfly systems >20 台；Q3 指引 2.10-2.25 亿美元，原因是 advanced nodes spending 暂停 | AI packaging 仍强，但 Q3 节奏受 front-end timing 影响；Semilab 当时仍 pending |
| 2025Q1 | 2.666 亿美元；YoY +16.5%；QoQ +1.0% | GAAP GM 54%；non-GAAP GM 55%；GAAP EPS 1.30；non-GAAP EPS 1.51 | Transcript 口径：Specialty + AP 约 1.29 亿美元，占 48%；software/services 约 0.44 亿美元，占 17%；advanced nodes 约 0.94 亿美元，占 35% | Advanced nodes revenue QoQ doubled；multiple 3D bump metrology systems shipped；Q2 指引 2.40-2.60 亿美元 | 高级节点和先进封装共同支撑 record quarter；但 AP 从 2024Q4 record level 回落 |

### 3.1 Backlog/Bookings/取消率推断

公司不逐季披露 bookings、B2B、取消率。能落地的硬信息有三条：

1. 2025Q4 backlog 约两个季度收入量级，按 Q4 revenue 2.669 亿美元推算约 `5 亿美元+`，且 Q1 管理层继续称 record backlog。
2. 单一 HBM 客户 VPA `>$240M` through 2027，其中 `>$60M` 为 3D bump metrology；管理层后来表示节奏从 2027 权重更高，向 2026/2027 更接近 50/50 拉动。
3. 内部制造 capacity 管理层称可支持约 `20 亿美元` 年化收入 run-rate；真正瓶颈在 precision optics 等供应链，lead time 较固定且在延长。

取消率没有披露。我的判断：基准情景下取消率应低，约 0%-5%，因为工具已通过客户 qualification、对应 HBM/AP 扩产窗口，且客户会先锁定长交期部件；风险主要是 pushout 而不是 outright cancellation。若 AI capex 急刹、HBM 客户库存误配、出口管制升级，则 pushout/cancellation 可升到 5%-15%。

## 4. 2026 最新指引、收入占比与产品映射

### 4.1 2026Q1 实际和 Q2 指引

| 项目 | 数值 |
|---|---:|
| 2026Q1 revenue | 2.919 亿美元 |
| 2026Q1 non-GAAP GM | 55.7% |
| 2026Q1 non-GAAP operating margin | 26.7% |
| 2026Q1 non-GAAP EPS | 1.42 美元 |
| 2026Q2 revenue guide | 3.20-3.30 亿美元，中点 3.25 亿美元 |
| 2026Q2 non-GAAP GM guide | 56.0%-56.5% |
| 2026Q2 non-GAAP operating margin guide | 28.0%-28.6% |
| 2026Q2 non-GAAP EPS midpoint | 约 1.69 美元 |
| 2026 全年 revenue guide/commentary | `>13 亿美元`，同比 `>30%` |
| 2026 advanced packaging outlook | `>50%` growth |
| 2026 advanced nodes outlook | 约 `25%` growth |

### 4.2 2026Q1 业务收入占比

| 口径 | 2026Q1 收入 | 占比 | 同比/环比或趋势 |
|---|---:|---:|---|
| Advanced packaging | 约 1.07 亿美元 | 36.5% | 2026 全年管理层预期 `>50%` 增长；G5/3Di/HBM/2.5D 为主驱动 |
| Semilab USA | 约 0.25 亿美元 | 8.6% | Q4 约 900 万美元，Q1 完整季度约 2,500 万美元；全年低百百万美元级 |
| Specialty devices including power | 约 0.28 亿美元 | 9.6% | power semi 2026 偏弱，管理层原先预计约 -10% |
| Advanced nodes | 约 0.80 亿美元 | 27.4% | 2026 全年约 +25%；其中 memory/DRAM 约 60%，logic 约 40% |
| Software/services | 约 0.52 亿美元 | 17.9% | installed base、parts、yield software；跟随系统装机增长 |
| Formal product source: systems/software | 2.472 亿美元 | 84.7% | SEC 10-Q 口径 |
| Formal product source: parts | 0.266 亿美元 | 9.1% | SEC 10-Q 口径 |
| Formal product source: service | 0.182 亿美元 | 6.2% | SEC 10-Q 口径 |

### 4.3 产品和业务交叉验证

| 重点产品/平台 | 对应业务 | 最新硬事实 | 收入/增速推断 | 利润率推断 |
|---|---|---|---|---|
| Dragonfly G5 | Advanced packaging inspection/metrology | 2026-03 launch；leading HBM manufacturer for HBM4 ramp 完成评估并选择；detect defects down to 150nm；throughput up to 5x previous Dragonfly；double-digit G5 + 3Di orders Q2 起发货 | 当前 G5 从低基数爬坡，Q1 “handful of tools”，Q2/Q3/Q4 nearly double each quarter；advanced packaging 2026 `>50%` 增长 | 硬件+光学+软件，早期 ramp 毛利低于成熟产品，但量产后应高于公司平均；估计 GM 55%-65% |
| Dragonfly G3 + 3Di + EchoScan | HBM/2.5D/3D metrology | Q3 已由两大 HBM 客户 fully qualified；Q4 HBM VPA `>$240M` through 2027；Q1 新增 10+ 3Di orders | 是 2026 advanced packaging revenue 的最大已验证贡献者；current product qualified now，G5 是 upside | 3D metrology/算法价值高，估计 GM 55%-65%；service/recipe 粘性较强 |
| JetStep + Firefly + StepFAST | Panel-level packaging / large panel RDL | Q4 获 JetStep + 8 Firefly systems 的大面板封装厂订单；Q1 JetStep qualified at two suppliers to AI device manufacturers，ramp expectation 2027 | 2026 贡献有限但不能忽略；2027 若 panel-level packaging 供需紧张，弹性显著 | 早期订单硬件比重大，估计 GM 45%-55%；若形成标准产线组合可上行 |
| Atlas G6/OCD + Iris films + integrated metrology | Advanced nodes | 2026Q1 advanced nodes 约 0.80 亿美元；Atlas G6 被第二个 logic customer 选择用于 GAA metrology；2026 advanced nodes 约 +25% | 2026 年化约 3.8-4.2 亿美元业务池；HBM DRAM、GAA logic、NAND recovery | OCD/film metrology 技术壁垒高，估计 GM 55%-65%；竞争强于 AP |
| Semilab FAaST/CnCV/MBIR | Materials/electrical metrology | 2025-11 完成约 4.95 亿美元交易；Q1 贡献约 2,500 万美元；增加 surface charge/materials/wafer contamination | 2026 低百百万美元级；短期部分 power semi 弱，长期 advanced logic/AP 交叉销售 | 公司称排除 purchase accounting 后 accretive；估计 non-GAAP GM 55%+ |
| Rigaku X-ray + Ai Diffract | Hybrid optical/X-ray metrology | ONTO 拟以 7.10 亿美元买 27% Rigaku；Rigaku 2025 revenue `>6 亿美元`，约 40% semiconductor；two key customers selected integrated offering | 2026 不并表；1 年内收入来自 Ai Diffract licensing、additional Atlas sales、Rigaku dividends | 软件 licensing 接近 100% margin；工具 pull-through 取决于客户采纳 |

### 4.4 可以低权重/暂时跳过的产品和业务

以下业务不是没有价值，而是相对 AI/HBM/AP 主线增速或弹性较低：

| 低权重业务 | 原因 |
|---|---|
| Power semiconductor specialty devices | 2026 管理层预计 power semi revenue 约 -10%，EV/infrastructure 周期弱 |
| LED/VCSEL/MEMS/CIS/RF filters/data storage 等 specialty | 长期稳定但不是当前 AI 数据中心主要瓶颈 |
| 常规 parts/service | 现金流好，但增长跟随 installed base，弹性低于 Dragonfly/Atlas/Semilab |
| Mature-node China exposure | 2025 中国收入同比明显下降；先进节点中国受出口管制和客户节奏影响 |

## 5. 高增长/关键业务当前贡献与战略评分

评分 1-5，5 最强。收入贡献为 2026Q1 或当前 run-rate 推算，非公司法定分部。

| 业务/产品 | 当前收入贡献 | 当前增速/订单 | AI 基建重要性 | 时间紧急性 | 供需紧张度 | 垄断/溢价能力 | 关键判断 |
|---|---:|---|---:|---:|---:|---:|---|
| Dragonfly G3/G5 + 3Di/EchoScan | 2026Q1 advanced packaging 约 1.07 亿美元；其中 Dragonfly/3Di 为主，但未单独披露 | Advanced packaging 2026 `>50%`；G5 Q2-Q4 出货加速；HBM VPA `>$240M` | 5.0 | 5.0 | 4.5 | 4.0 | 这是 ONTO 最大 AI 弹性。HBM4、CoWoS-like、hybrid bonding、microbump 缩小都会提高检测强度 |
| Atlas G6/OCD/Iris/integrated metrology | 2026Q1 advanced nodes 约 0.80 亿美元，其中 memory/DRAM 约 0.48 亿美元 | 2026 advanced nodes 约 +25%；Atlas G6 新 logic wins；TSV metrology H2 出货 | 4.5 | 4.0 | 3.5 | 3.2 | 对 GAA、DRAM/HBM 前道关键，但 KLA/Nova/ASML/Hitachi 等竞争更强 |
| JetStep + Firefly panel-level packaging | 当前收入未披露；Q4 已有 JetStep + 8 Firefly 单厂订单 | 两家 AI device packaging suppliers qualification；ramp expectation 2027 | 3.5 现在 / 4.5 期权 | 3.5 | 3.5 | 3.5 | panel-level packaging 仍是期权，但若 2027 大尺寸 AI package 走向 panel/RDL，ONTO 有小业务变大业务的可能 |
| Semilab FAaST/CnCV/MBIR | 2026Q1 约 0.25 亿美元；年化约 1.0 亿美元 | 2026 低百百万美元级；先进材料/surface charge 交叉销售 | 3.5 | 3.5 | 3.0 | 3.5 | 短期是并购贡献，长期看 advanced materials/3D architectures 的检测问题 |
| Rigaku X-ray + Ai Diffract | 2026 当前不并表；潜在 licensing/dividend/Atlas pull-through | two key customers selected integrated offering；closing expected 2026H2 | 4.0 期权 | 3.5 | 3.0 | 4.0 软件端 | 如果 1nm/GAA/HBM4/3D hidden structures 需要 X-ray + optical hybrid，这可能成为 2027-2028 新曲线 |

## 6. 一年后收入贡献预测：基准、乐观、极度乐观

预测口径：未来一年 run-rate/2027Q1 TTM 附近，不是公司指引。以 2025 revenue 10.05 亿美元、2026 管理层 `>13 亿美元` 为锚。

| 产品/业务 | 基准情景 | 乐观情景 | 极度乐观情景 |
|---|---|---|---|
| Dragonfly G3/G5 + 3Di/EchoScan advanced packaging | 年化收入 5.2-6.0 亿美元；YoY +35%-45%；重要性 5；供需紧张 4；溢价 4 | 6.5-7.5 亿美元；YoY +55%-75%；G5 share gain 加快，HBM/2.5D pull-in；供需紧张 4.5 | 8.5 亿美元+；YoY +90%+；HBM4/CoWoS-like/OSAT 全部前拉，精密光学不再严重卡交付；供需紧张 5 |
| Atlas G6/OCD/Iris/integrated metrology advanced nodes | 年化 3.9-4.3 亿美元；YoY +25%-35%；GAA/DRAM/HBM 稳定 | 4.6-5.2 亿美元；YoY +45%-60%；GAA 多客户、HBM DRAM VPAs、NAND recovery | 6.0 亿美元+；YoY +80%+；多座先进 fab 同步开，客户争抢 OCD/film/integrated metrology |
| JetStep + Firefly panel-level packaging | 0.6-0.9 亿美元；2026-2027 初步放量 | 1.0-1.5 亿美元；两家 qualified suppliers 进入 HVM，更多 panel 工厂订单 | 2.0 亿美元+；panel-level packaging 2027 出现供不应求，JetStep/Firefly 成为标准产线组合 |
| Semilab FAaST/CnCV/MBIR | 1.2-1.5 亿美元；交叉销售初见效 | 1.7-2.2 亿美元；surface charge/materials 在 AP/advanced nodes 扩大 | 3.0 亿美元+；与 Onto/Rigaku/Ai Diffract 联合方案进入多个高阶客户 |
| Rigaku X-ray + Ai Diffract | ONTO 直接收入 0.1-0.3 亿美元，主要 software licensing/dividend/Atlas pull-through | 0.3-0.6 亿美元，并带动更多 Atlas G6/OCD | 1.0 亿美元+ 间接/直接贡献；X-ray hybrid metrology 被多个 memory/logic 客户标准化 |
| 公司整体 | FY2026 13.0-13.8 亿美元；YoY +29%-37% | 14.5-16.0 亿美元；YoY +44%-59% | 17.5-20.0 亿美元；接近管理层称可支持的 20 亿美元 run-rate，要求供应链和客户 capex 极顺 |

## 7. BOM、单位内容量和价格传导链

重要说明：ONTO 的设备不是 GPU/rack/MW BOM 的直接采购项；它是制造设备 capex。下面“每 GPU/每 rack/每 MW/每 optical port 内容量”是把 ONTO 可获得的 process-control equipment revenue 按终端 AI 硬件出货进行摊销，属于经济内容量，而不是成品 BOM 中的一颗器件价格。

假设：

- 1 个高端 AI rack = 72 GPUs/accelerators。
- 1 个 liquid-cooled rack 功率约 120-130 kW。
- 1 MW 约 550-650 GPUs/accelerators。
- 一个高端 AI package 需覆盖 HBM known-good-die、interposer/RDL、microbump/TSV、hybrid bonding、after-attach、final package 等多个 inspection/metrology step。

| 产品/业务 | 每 GPU/accelerator 摊销内容量 | 每 72-GPU rack | 每 MW | 每 optical port | 价格传导 |
|---|---:|---:|---:|---:|---|
| Dragonfly/3Di/EchoScan | 基准 5-30 美元；极度乐观 20-60 美元 | 基准 360-2,160 美元；极度乐观 1,440-4,320 美元 | 基准 3,000-18,000 美元；极度乐观 12,000-36,000 美元 | 现有 pluggable optics 直接内容量接近 0；若 CPO/SiPh package 用 3Di/inspection，约 0.02-0.10 美元/port | GPU/ASIC/HBM 需求 -> TSMC/OSAT/HBM 封装 capex -> Dragonfly/3Di tool order -> 2-4 个季度交付/验收 |
| Atlas G6/OCD/Iris/integrated metrology | 3-15 美元；HBM4/GAA 加速时 10-30 美元 | 216-1,080 美元；高端 720-2,160 美元 | 1,800-9,000 美元；高端 6,000-18,000 美元 | SiPh wafer/metrology 情景 0-0.03 美元/port | Advanced node wafer starts -> OCD/films/integrated metrology attach -> tool + software/model revenue |
| JetStep/Firefly panel-level packaging | 仅适用于 panel/RDL 路线：1-10 美元；传统 CoWoS-like 路线可为 0 | 72-720 美元 | 600-6,000 美元 | CPO/optical engine panel package 0.01-0.05 美元/port | 大尺寸 package/RDL 经济性 -> panel-level line capex -> JetStep litho + Firefly inspection |
| Semilab/Rigaku materials/X-ray | 1-8 美元；advanced materials/hybrid metrology 标准化后 5-15 美元 | 72-576 美元；高端 360-1,080 美元 | 600-4,800 美元；高端 3,000-9,000 美元 | SiPh/materials 情景 0.01-0.05 美元/port | Exotic materials/hidden structures -> surface charge/X-ray/materials metrology -> software/license + tool pull-through |

### 7.1 当前产能、供应链采纳与认证阶段

| 产品/业务 | 当前产能能力 | 供应链采纳 | 认证阶段 |
|---|---|---|---|
| Dragonfly/3Di/EchoScan | 公司整体内部产能管理层称可支持约 20 亿美元年化 run-rate；供应链瓶颈在 precision optics | HBM 客户 VPA；leading 2.5D logic customer qualified；15+ applications / 10+ customers pipeline；OSAT 客户增加 | G3/3Di 已在 HBM 与 2.5D logic 多客户 qualified；G5 已在 HBM4 和领先 2.5D logic 客户 qualified，Q2 起加速出货 |
| Atlas G6/OCD/Iris | 内部产能不是主瓶颈，更多取决于客户 fab timing 与 tool mix | 两个 logic customers for GAA；memory/DRAM traction；integrated metrology 从 memory 扩到 logic | Atlas G6 已完成多客户 competitive evaluations，部分客户已选择；TSV metrology H2 2026 初始出货 |
| JetStep/Firefly | 产能相对小，但 panel-level demand 尚在早期 | Q4 JetStep + 8 Firefly 单厂订单；两家 AI device packaging suppliers qualified | 已 qualification；ramp expectation 2027 |
| Semilab FAaST/CnCV/MBIR | 并购后进入 Onto 全球制造/服务体系；Q1 完整季度 2,500 万美元收入 | 既有 Semilab 客户 + Onto advanced node/AP 客户交叉销售 | 已完成产品线收购；先进 AP/logic 协同应用仍在拓展 |
| Rigaku X-ray + Ai Diffract | Rigaku 2025 收入 `>6 亿美元`，约 40% semiconductor；ONTO 不并表 | Integrated offering 已被 two key customers selected | 交易预计 2026H2 close；hybrid metrology 处于客户选型/评估和 early adoption |

### 7.2 一年后产能、采纳和认证预测

| 产品/业务 | 基准 | 乐观 | 极度乐观 |
|---|---|---|---|
| Dragonfly/3Di/EchoScan | ONTO 总 revenue capacity 13-15 亿美元年化可满足；G5 进入多个 HVM ramps；供应链仍紧但可控 | Precision optics 供应改善，G5 在 HBM/2.5D logic 多客户扩散；additional VPAs | 供应链前拉成功，接近 20 亿美元总 run-rate；G5/3Di 成为 HBM4/2.5D 多客户 tool-of-record |
| Atlas G6/OCD/Iris | 2nm/GAA/DRAM/HBM 客户持续下单，25% 左右增长 | 多家 logic/memory VPAs，Atlas G6 与 Rigaku/Ai Diffract 绑定销售 | Hybrid optical/X-ray 成为 advanced logic/memory 新 recipe 标准，Atlas pull-through 大幅提高 |
| JetStep/Firefly | 两家 qualified suppliers 2027 ramp，收入开始可见 | 追加 panel factory phase 2/phase 3 订单，形成 1 亿美元+业务 | 2027 panel-level packaging 供需缺口出现，JetStep/Firefly 成为先进封装扩产核心瓶颈设备之一 |
| Semilab/Rigaku | Semilab 低百百万美元收入，Rigaku closing 后贡献 licensing/dividend | Surface charge/materials 与 Atlas/Dragonfly 联合方案被更多客户采用 | X-ray + surface charge + optical metrology 被 HBM4/GAA/hybrid bonding 标准化，形成新增长平台 |

## 8. 基于订单积压和供给的未来一年业务增速预测

| 情景 | 关键假设 | 2026/未来一年公司收入 | 主要限制 |
|---|---|---:|---|
| 基准 | Q2 指引达成；H2 比 H1 至少 +15%；VPA 约一半拉入 2026；advanced packaging +50%，advanced nodes +25%；precision optics 偶有延迟 | 13.0-13.8 亿美元，同比 +29%-37% | AP/HBM 客户节奏、G5 ramp 良率、供应商 lead time |
| 乐观 | G5 adoption 比管理层保守假设快；additional VPAs 落地；panel-level 有新增订单；Semilab 交叉销售顺利 | 14.5-16.0 亿美元，同比 +44%-59% | 需要供应链、field apps、客户验收同时顺 |
| 极度乐观 | HBM4/Rubin/MI400/TPU/ASIC 带动 HBM+2.5D+panel 多线抢产能；客户愿意 pre-book/pull-in；precision optics 扩产成功 | 17.5-20.0 亿美元，同比 +74%-99% | 接近管理层称内部可支持的 20 亿美元 run-rate，但需要外部供应链不再卡；估值会把执行风险放大 |

我对未来一年的中性判断偏向“基准到乐观之间”。原因是 backlog/VPA/qualification 真实存在，且 Q2 guide 已经把 run-rate 拉到 13 亿美元以上；但极度乐观需要 Dragonfly G5、3Di、Atlas、Semilab/Rigaku、panel-level 同时顺风，且 precision optics 等供应链不拖后腿。

## 9. 竞争格局、替代方案与替换成本

### 9.1 主要竞争对手

| 领域 | ONTO 产品 | 主要竞争对手 | 竞争态势 |
|---|---|---|---|
| Thin film / OCD / CD metrology | Atlas/Atlas G6、Iris、Ai Diffract | KLA、Nova、ASML/HMI、Hitachi 等 | KLA/Nova 强；ONTO 通过 optical ecosystem、spot size、integrated metrology 和 Rigaku X-ray 合作增强差异化 |
| Advanced packaging inspection | Dragonfly G3/G5、3Di、EchoScan | KLA、Camtek、Nova、Utechzone/区域厂商等 | ONTO 在 HBM/2.5D/3D bump 与 multi-sensor 平台上拿到强 proof points；KLA/Camtek 客户基础也深 |
| Packaging lithography | JetStep | Ushio、Canon 等 | JetStep/Firefly 在 panel-level packaging 是小业务期权，尚未证明大规模主流化 |
| Panel inspection | Firefly | GigaVis、KLA/Camtek 相关方案 | 取决于 panel-level packaging 是否进入 AI package 主流供应链 |
| Yield software | Discover、defect classification | PDF Solutions、KLA software、客户自研 | 软件粘性高，但设备绑定更关键 |
| X-ray/hybrid metrology | Ai Diffract + Rigaku X-ray | Rigaku 自身、Bruker、Nova/KLA/其他 X-ray/CD-SAXS players | 2026-2027 属于新技术组合窗口，标准未完全确定 |

### 9.2 新技术是否是主流

确定性最高的是 Dragonfly/3Di/advanced packaging inspection。HBM3E/HBM4、2.5D logic、chiplet、hybrid bonding、microbump 缩小这些方向已是 AI accelerator 的主路线，inspection/metrology 强度只会提高。ONTO 的 G5/3Di 正好踩在这个变化上。

Atlas G6/OCD 是 advanced-node 主流需求，但竞争更硬。GAA、DRAM/HBM、TSV、critical films 都需要 process control；问题不是有没有需求，而是 ONTO 能从 KLA/Nova 等强对手那里拿多少 wallet share。

JetStep/Firefly 的 panel-level packaging 是潜在主流，不是已验证主流。若 2027 AI package 面积继续变大、traditional CoWoS-like capacity 仍紧，panel/RDL 路线会更有吸引力；否则它会保持小而有弹性的补充业务。

Rigaku X-ray + Ai Diffract 是中长期主流候选。越往 1nm/GAA/HBM4/hybrid bonding，hidden structures 和 exotic materials 越多，单纯 optical 会遇到物理信息限制；但 X-ray throughput、cost of ownership、recipe maturity 和客户 fab integration 需要验证。

### 9.3 客户替换成本

替换成本高。先进封装和前道 metrology 不是买一台工具即可替换，客户需要 recipe、defect library、golden die algorithm、tool matching、yield correlation、field application support、factory automation 和量产认证。项目内行业资料对 advanced node/HBM/AP 认证周期的判断是 6-18 个月；ONTO 自身 G5 从 onsite competitive evaluation 到 Q2 shipments，也体现了这个时间成本。

但替换成本不是垄断。大客户通常会多供应商策略，且 KLA、Camtek、Nova 等都有强产品。ONTO 的溢价来自“在关键窗口已通过 qualification + 可交付 + cost of ownership 更好”，而不是永久独占。

### 9.4 主要风险

1. 估值风险：forward PE 35.9x、forward PS 10.0x 已经要求 2026-2027 高增长兑现。
2. 供应链风险：precision optics、光源、stage、image compute、field apps 都可能限制交付。
3. 客户集中：2025 年 Samsung Semiconductor 15%、SK hynix 14%；2024 年 TSMC 23%、Samsung 17%、SK hynix 12%。AI/HBM 客户 capex 节奏对 ONTO 影响大。
4. 订单节奏：backlog 强，但工具收入需要客户验收；pushout 会让季度波动很大。
5. 竞争：KLA/Nova/Camtek 在核心客户处有深 installed base；G5 虽有 wins，但还要持续转化为多客户 HVM。
6. 并购/投资：Semilab 整合、Rigaku 交易 closing、融资和公允价值波动会影响 GAAP 利润和现金。
7. 地缘/出口管制：中国 mature/advanced 市场弱或受限；台湾/韩国集中也带来区域风险。

## 10. 最值得跟踪的验证指标

| 指标 | 为什么重要 | 未来 1-2 个季度观察 |
|---|---|---|
| Dragonfly G5 shipment cadence | 决定 advanced packaging 是否从 +50% 走向更高 | Q2/Q3 是否如管理层所说 nearly double each quarter |
| Additional HBM/DRAM VPAs | 验证 backlog 是否从单客户扩散 | 是否出现第二/第三个 HBM 客户 long-term agreement |
| Advanced packaging gross margin | 验证新平台是否提升利润而非只拉收入 | Q2 56%-56.5% GM 后，Q3/Q4 是否每季 +50bps |
| Precision optics lead time | 供给侧最大瓶颈 | 是否仍被客户 pull-in 压迫，或供应商扩产顺利 |
| JetStep/Firefly panel orders | 小业务变大业务的拐点 | 2026H2 是否有更多 panel factory phase/order |
| Rigaku closing 与 Ai Diffract licensing | X-ray/hybrid metrology 期权兑现 | 2026H2 closing、two key customers 后是否有更多客户 |
| Semilab advanced-node/AP synergies | 并购是否只是 revenue add，还是技术平台扩展 | Q2-Q4 Semilab 是否超低百百万美元年化 run-rate |

## 11. 资料来源

### 官方与财务资料

- Onto Innovation 2026Q1 earnings release: https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Reports-2026-First-Quarter-Results/default.aspx
- Onto Innovation 2026Q1 10-Q: https://www.sec.gov/Archives/edgar/data/704532/000119312526206707/onto-20260331.htm
- Onto Innovation FY2025 10-K: https://www.sec.gov/Archives/edgar/data/704532/000119312526066937/onto-20260103.htm
- Onto Innovation 2025Q4/FY2025 earnings release: https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Reports-2025-Fourth-Quarter-and-Full-Year-Results/default.aspx
- Onto Innovation 2025Q3 earnings release: https://investors.ontoinnovation.com/news/news-details/2025/Onto-Innovation-Reports-2025-Third-Quarter-Results/default.aspx
- Onto Innovation 2025Q2 earnings release: https://investors.ontoinnovation.com/news/news-details/2025/Onto-Innovation-Reports-2025-Second-Quarter-Results/default.aspx
- Onto Innovation 2025Q1 earnings release: https://investors.ontoinnovation.com/news/news-details/2025/Onto-Innovation-Reports-2025-First-Quarter-Results/default.aspx
- StockAnalysis ONTO statistics: https://stockanalysis.com/stocks/onto/statistics/

### 电话会与产品资料

- 2026Q1 transcript: https://stockanalysis.com/stocks/onto/transcripts/560656-q1-2026/
- 2025Q4 transcript: https://stockanalysis.com/stocks/onto/transcripts/401878-q4-2025/
- 2025Q2 transcript: https://stockanalysis.com/stocks/onto/transcripts/344404-q2-2025/
- 2025Q3 transcript excerpts: https://www.marketbeat.com/earnings/reports/2025-11-6-onto-innovation-inc-stock/ and https://www.roic.ai/quote/ONTO/transcripts/2025-year/3-quarter
- 2025Q1 transcript excerpts: https://www.stockinsights.ai/us/ONTO/earnings-transcript/fy25-q1-2e72 and https://www.roic.ai/quote/ONTO/transcripts/2025/1
- Dragonfly G5 launch: https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Launches-Dragonfly-G5-Inspection-System/default.aspx
- Dragonfly G5 2.5D AI packaging qualification: https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovations-Dragonfly-G5-System-Qualified-for-Applications-in-2-5D-AI-Packaging/default.aspx
- Atlas G6 launch: https://investors.ontoinnovation.com/news/news-details/2025/Onto-Innovation-Launches-Next-Generation-OCD-Metrology-Platform-to-Enable-Process-Control-for-Advanced-AI-Devices/default.aspx
- 3Di/EchoScan process-control suite: https://investors.ontoinnovation.com/news/news-details/2025/Onto-Innovation-Advances-Process-Control-Suite-for-3D-Interconnect-Yields/default.aspx
- Semilab acquisition close: https://investors.ontoinnovation.com/news/news-details/2025/Onto-Innovation-Completes-Acquisition-of-Unique-Materials-Composition-and-Electrical-Analysis-Product-Lines-from-Semilab-International/default.aspx
- Rigaku strategic partnership: https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Announces-Strategic-Partnership-With-Leading-X-Ray-Provider-Rigaku-To-Advance-Next-Generation-Process-Control-Solutions/default.aspx

### 行业与项目内资料

- SEMI equipment forecast, 2025-2027: https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports
- 项目内行业资料，未读取 `公司调研` 目录：`D:\drive\Investment\工作台v5\行业调研_晶圆制造_设备_材料_测试\行业调研_半导体检测量测设备_2026-05-08.md`
- 项目内行业资料，未读取 `公司调研` 目录：`D:\drive\Investment\工作台v5\行业调研_AI服务器_存储_芯片\行业调研_封装基板_中介层与RDL_2026-05-08.md`
