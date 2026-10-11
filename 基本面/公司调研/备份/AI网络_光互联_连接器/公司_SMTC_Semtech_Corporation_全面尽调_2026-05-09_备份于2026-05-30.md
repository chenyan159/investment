# 公司：SMTC Semtech Corporation（Semtech）全面尽调

> 研究日期：2026-05-09。货币单位默认美元。财务季度采用 Semtech 财年口径，FY2026 截至 2026-01-25。  
> 说明：本报告没有参考本目录下其他公司调研文件；行业交叉验证使用了项目内非“公司调研”目录的 AI 光互联、铜互联、DesignCon/OFC 资料。凡公司未披露的 backlog、BOM 内容量、AI 数据中心季度拆分，均标注为“测算/推断”。

## 0. 核心结论

Semtech 现在已经从传统模拟/混合信号与 IoT 公司，重新被市场定价为“AI 数据中心光互联/铜互联上游 IC 供应商”。FY2026 公司收入 10.50 亿美元，同比 +15.5%；其中数据中心收入 2.23 亿美元，同比 +58%，Q4 数据中心收入 6300 万美元，同比 +26%、环比 +12%。管理层给出的 FY2027 数据中心目标是同比增长超过 50%，这意味着该业务至少要到 3.35 亿美元以上。

最重要的业务不是 IoT，而是 data-center interconnect：224G/200G TIA、MZM/laser driver、1.6T LPO/LRO/FRO、CopperEdge ACC redriver、以及 2026-03 收购 HieFo 后新增的 InP gain chip/DFB laser。OFC 2026 上 Semtech 展示了 NVIDIA 1.6T DR8 OSFP 模块采用 GN1834D TIA 与 GN187N1 driver，另有 GN8234/GN8304 铜缆 redriver 和 TN622/TN14740 448G PMD 样品。这些信息把 Semtech 从“有周期性 IoT 包袱的模拟公司”推向“AI 光模块与铜缆内容量扩张”的交易逻辑。

估值已经反映高预期：截至 2026-05-08 收盘，SMTC 股价 121.81 美元，市值 113.4 亿美元，P/S 10.80x，Forward P/E 55.11x；由于 FY2026 GAAP 仍亏损 4040 万美元，TTM P/E 为 n/a。资产负债表明显改善，现金 1.95 亿美元、总债务约 5.03 亿美元、净债务约 3.08 亿美元，FY2026 自由现金流 1.714 亿美元；但客户订单可取消、收入 74% 通过分销、China/HK ship-to 占 47%，且设计赢单竞争激烈，估值安全垫不厚。

## 1. 公司整体业务、产业链定位与财务健康

### 1.1 业务结构与投资人认知

Semtech 是高性能半导体、IoT 系统和云连接服务供应商。FY2026 三个报告分部如下：

| FY2026 分部 | 收入 | 收入占比 | YoY | 分部毛利率 | 核心产品/应用 | AI 相关性 |
|---|---:|---:|---:|---:|---|---|
| Signal Integrity | 3.226 亿 | 30.7% | +23.3% | 65.2% | 数据中心/企业网/PON/无线前传光收发器 IC、视频传输、光/铜高速链路 | 最高，AI 数据中心 TIA/driver/ACC/PMD 主要落在此处 |
| Analog Mixed Signal & Wireless | 3.734 亿 | 35.6% | +15.6% | 58.9% | TVS/保护、PerSe sensing、LoRa/无线、部分高速模拟/基础设施产品 | 中等，含部分基础设施/高速信号链；非 AI 产品较多 |
| IoT Systems & Connectivity | 3.539 亿 | 33.7% | +9.0% | 35.5% | Sierra Wireless 模块、路由器、连接服务、IoT edge-to-cloud | 低，收入大但毛利率低、AI 数据中心相关性弱 |
| 合计 | 10.500 亿 | 100% | +15.5% | GAAP 51.6% / 调整后 52.8% | 半导体产品 + IoT 系统/服务 | 数据中心收入 2.23 亿，占总收入 21.2% |

投资人眼中的 Semtech 有两层：  
第一层是传统模拟/IoT 公司。2023 年完成 Sierra Wireless 收购后，公司收入规模接近翻倍，但高杠杆、IoT 模块低毛利、整合与商誉减值压制估值。  
第二层是 AI 光互联公司。2025-2026 年数据中心收入快速放大，Semtech 的 TIA/driver/linear optics/ACC 产品进入 800G、1.6T、3.2T 光铜互联升级周期，市场开始把它与 MACOM、Credo、Marvell、Broadcom、Astera 这类 AI interconnect 标的放在一起比较。

### 1.2 最近 3 年重大变化

| 时间 | 事件 | 对业务与估值的影响 |
|---|---|---|
| 2023-01 | 完成 Sierra Wireless 收购，企业价值约 12 亿美元；交易带来蜂窝 IoT 模块、路由器、连接服务，并新增约 1 亿美元高毛利 IoT cloud services recurring revenue 的战略目标。 | 收入规模扩大，但债务、整合、低毛利硬件和商誉减值成为股价包袱。 |
| 2024-2025 | 持续重组、降本、资本结构优化；公司把重点从“端到端 IoT 平台叙事”转向高毛利半导体和现金流。 | FY2026 经营现金流 1.812 亿、FCF 1.714 亿，债务压力显著缓和。 |
| 2025-2026 | 数据中心收入成为增长主轴：FY2026 数据中心收入 2.23 亿美元，同比 +58%；Q4 数据中心 6300 万美元，同比 +26%、环比 +12%。 | Semtech 的投资叙事切换为 AI 数据中心 800G/1.6T/3.2T 光铜互联 IC。 |
| 2026-03-03 | 收购 HieFo Corporation，现金约 3400 万美元，获得 InP gain chip、DFB laser 等上游光器件能力。 | 扩大从 TIA/driver 到 laser/gain chip 的内容量，强化 CPO/NPO/3.2T 光平台。 |
| 2026-03-12/16 | OFC 2026 展示 1.6T optical、1.6T/3.2T ACC、448G PMD；发布 224Gbps TIA/driver family。 | 进入 224G/lane 量产窗口与 448G/lane 预研窗口，和 NVIDIA 生态验证相关性提高。 |

### 1.3 产业链位置

Semtech 不做 GPU、交换芯片或完整光模块，而是在 AI 网络互联链条里卖“高速模拟/光电前端 IC”：

GPU/ASIC 节点 -> NIC/交换机 SerDes -> 光模块或主动铜缆 -> 光/铜物理层 IC -> 模块厂/线缆厂 -> 系统厂 -> hyperscaler。  

Semtech 的价值点在光模块接收端 TIA、发射端 MZM/laser driver、linear optics 信号链、ACC redriver、以及 HieFo 的 InP laser/gain chip。AI 集群从 800G 升级到 1.6T、3.2T 时，每个 optical port 或 ACC port 对低功耗、高线性度、低噪声、低时延 IC 的依赖上升，Semtech 的内容量有机会从 800G 模块的个位数美元，提升到 1.6T 的十几到数十美元，3.2T/CPO/NPO 更高。

### 1.4 最新行情与估值

| 指标 | 最新数值 | 日期/口径 | 评价 |
|---|---:|---|---|
| 股价 | 121.81 | 2026-05-08 收盘，StockAnalysis | 52 周涨幅 +254%，接近 52 周高位 127.19 |
| 盘后价 | 122.69 | 2026-05-08 19:56 EDT，StockAnalysis | 盘后仍强 |
| 市值 | 113.4 亿 | 2026-05-08，StockAnalysis | 已按 AI interconnect 成长股定价 |
| EV | 116.7 亿 | 2026-05-08，StockAnalysis | EV/Sales 11.11x |
| TTM P/E | n/a | FY2026 GAAP 净亏损 4040 万 | GAAP 亏损主要受商誉/无形资产减值影响 |
| Forward P/E | 55.11x | 2026-05-08，StockAnalysis | 高，需要 FY2027-2028 快速放量支撑 |
| P/S | 10.80x | 2026-05-08，StockAnalysis | 对 FY2026 15.5% 收入增速而言偏贵，但对数据中心 +50%+ 预期可解释 |
| FY2026 收入增速 | +15.5% | 10-K，10.50 亿 vs 9.093 亿 | 增长来自数据中心、LoRa 与半导体产品 |
| TTM 毛利率 | 52.51% | StockAnalysis | 半导体产品分部毛利率 61.8%，IoT 系统拉低整体 |
| TTM 净利率 | -3.85% | StockAnalysis/10-K | FY2026 净亏损 4040 万 |
| FCF | 1.714 亿 | FY2026，10-K | FCF margin 16.3%，质量明显改善 |

### 1.5 资产负债表健康程度

FY2026 末现金及等价物 1.952 亿美元，总债务面值 5.030 亿美元，其中 2027 可转债 1.005 亿、2030 可转债 4.025 亿，净债务约 3.08 亿美元；StockAnalysis 口径总债务 5.180 亿、净债务 3.228 亿。流动资产 6.551 亿，流动负债 2.759 亿，流动比率 2.37，营运资本 3.792 亿，短期偿债压力较小。FY2026 经营现金流 1.812 亿、资本开支 980 万、FCF 1.714 亿，足以覆盖当前现金利息和小规模并购。

风险在三点。第一，资产结构仍有商誉 4.579 亿和无形资产 4000 万，FY2026 已确认商誉减值 8480 万，说明 Sierra 整合和非核心业务价值仍需观察。第二，订单多数基于 purchase order，10-K 明确称许多客户订单可取消，backlog 大多要求 6 个月内交付且相当部分可取消或重排。第三，客户和区域集中：FY2026 通过独立分销收入占 74%；China/HK ship-to 占 47%，美国 18%，台湾 6%；应收账款客户 A/B/C/D 分别约 13%/12%/12%/10%。财务健康度从“杠杆修复中”提升到“可投资扩产”，但不是净现金型公司。

## 2. 最新和最近 4 次财报：分部、利润率、订单/交期与 AI 数据中心

> 注：Semtech 不披露正式 bookings/B2B/backlog 金额。下表 backlog/交期列采用 10-K 订单披露、财报电话会和产品验证信息推断。AI 数据中心收入中，Q4 FY26、FY26 年度、Q4 FY25 为电话会披露或可由 YoY 反推；Q3 FY26 由 Q4 环比 +12% 反推；Q1/Q2 FY26 为在年度总额内的模型拆分。

| 财报季度 | 总收入/增速 | 分部收入与分部毛利率 | EPS/现金流 | AI 数据中心收入占比 | 订单、交期、取消率与定性 B2B |
|---|---:|---|---|---:|---|
| Q4 FY26，2026-01-25，2026-03-16 发布 | 2.744 亿；QoQ +3%，YoY +9.3% | SI 9070 万，GM 67.4%；AMW 9370 万，GM 56.2%；IoT 8990 万，GM 31.6% | GAAP EPS -0.32；调整 EPS 0.44；FCF 5910 万 | 6300 万，23.0%；YoY +26%，QoQ +12% | 无 backlog 金额；1.6T/3.2T、LPO、ACC 与 HieFo 形成 FY27 订单能见度。公司 10-K：backlog 多数 6 个月内交付、相当部分可取消/重排；推断数据中心 B2B >1，IoT B2B 接近 1。 |
| Q3 FY26，2025-10-26，2025-11-24/25 发布 | 2.670 亿；QoQ +3.6%，YoY +12.7% | SI 8160 万，GM 65.1%；AMW 9700 万，GM 58.0%；IoT 8830 万，GM 36.6% | GAAP EPS -0.03；调整 EPS 0.48；调整 EBITDA 6270 万 | 测算 5630 万，21.1% | Q4 data-center +12% QoQ 反推 Q3 约 5630 万；客户对高带宽低功耗链路需求增强，Semtech 称客户合作加深。订单仍以可取消 PO 为主。 |
| Q2 FY26，2025-07-27，2025-08-25/26 发布 | 2.576 亿；QoQ +2.6%，YoY +19.6% | SI 7676 万，GM 62.4%；AMW 9204 万，GM 59.3%；IoT 8879 万，GM 39.5% | GAAP EPS -0.31，含 4200 万商誉减值；调整 EPS 0.41 | 测算 5300 万，20.6% | 经营层称客户 engagement 强、现金流和去杠杆改善；数据中心继续爬坡，但 H2 前 1.6T/LPO/ACC 仍多为验证与早期放量。 |
| Q1 FY26，2025-04-27，2025-05-27/29 发布 | 2.511 亿；QoQ 持平，YoY +21.8% | SI 7352 万，GM 65.5%；AMW 9062 万，GM 62.3%；IoT 8692 万，GM 34.4% | GAAP EPS 0.22；调整 EPS 0.38；调整 EBITDA margin 22.1% | 测算 5080 万，20.2% | 基数从 800G/早期 1.6T optics 继续增长；Semtech 已开始把 R&D 投向 data-center networking、LoRa 和 sensing。 |
| Q4 FY25，2025-01-26，2025-03 发布 | 2.510 亿；Q4 FY26 对比基数 | SI 7250 万，GM 63.4%；AMW 8540 万，GM 53.8%；IoT 9310 万，GM 42.5% | GAAP EPS 0.43；调整 EPS 0.40；FCF 3090 万 | 由 Q4 FY26 +26% 反推约 5000 万，19.9% | 仍处于 Sierra 整合和数据中心早期 ramp；后续一年的核心变化是 data-center 从约 1.41 亿年收入提升到 2.23 亿。 |

关键变化：FY2026 全年半导体产品收入 6.961 亿，毛利率 61.8%；IoT Systems & Connectivity 收入 3.539 亿，毛利率 35.5%。因此公司利润弹性主要来自 data-center-heavy 的 SI/AMW 组合，而不是 IoT 硬件。

## 3. 最新指引、业务收入占比与产品映射

### 3.1 Q1 FY2027 指引

| 指标 | Q1 FY2027 指引 | 含义 |
|---|---:|---|
| 净销售额 | 2.83 亿 +/- 500 万 | 中点同比 Q1 FY26 +12.7%，环比 Q4 FY26 +3.1% |
| 调整后毛利率 | 52.8% +/- 50bp | 高于 Q4 FY26 51.6%，产品结构预计改善 |
| 半导体产品毛利率 | 60.4% +/- 50bp | 公司专门披露该指标，说明半导体产品利润率是市场关注点 |
| 调整后 opex | 9690 万 +/- 100 万 | FY27 加大数据中心 R&D、HieFo 整合、容量投资 |
| 调整后 EPS | 0.45 +/- 0.03 | 中点略高于 Q4 FY26 0.44 |
| 调整后 EBITDA | 5950 万 +/- 300 万 | EBITDA margin 中点 21.0% |

管理层最强调的业务是数据中心：FY2027 预计同比 +50% 以上，即从 FY2026 的 2.23 亿提高到至少 3.35 亿。若 Q1 data-center 按 Q4 的 6300 万顺季增长约低双位数测算，Q1 FY27 data-center 可到 7000 万美元上下，占 Q1 收入约 25%。

### 3.2 FY2026 业务收入占比和增长

| 收入口径 | FY2026 收入 | 占总收入 | YoY | 评论 |
|---|---:|---:|---:|---|
| Data center | 2.23 亿 | 21.2% | +58% | 最关键增长引擎，FY2027 目标 +50%+ |
| Signal Integrity | 3.226 亿 | 30.7% | +23.3% | 数据中心光/铜互联相关性最高 |
| Analog Mixed Signal & Wireless | 3.734 亿 | 35.6% | +15.6% | 既有保护/无线/sensing，也含高速模拟和基础设施 |
| IoT Systems & Connectivity | 3.539 亿 | 33.7% | +9.0% | 收入大但毛利率低，非 AI 核心 |
| Semiconductor Products（SI+AMW） | 6.961 亿 | 66.3% | +19.1% | FY2026 GM 61.8%，利润核心 |

### 3.3 产品与型号映射

| 业务/产品族 | 关键产品/型号 | 对应 AI 数据中心场景 | 2026 状态 | 利润率/增速判断 |
|---|---|---|---|---|
| 224G/200G TIA | GN1832、GN1834D、GN1834L、GN1834DL、GN1836、GN1838DL | 800G/1.6T optical receiver，LPO/LRO/FRO/NPO/CPO | GN1834L/GN1834DL 已可用；GN1838DL 预计 2026-04 发布 | 高毛利，随 1.6T 与 linear optics 放量；产品级毛利估计 60-75% |
| 224G MZM/laser driver | GN187N1、GN1877、GN1878、GN1887 | SiPho、InP MZM、TFLN transmitter，1.6T/3.2T optical | GN1887 已可用，GN1877 预计 2026-04 | 与 TIA 成套销售，议价能力强于单一器件 |
| 448G PMD | TN622 driver、TN14740 TIA | 3.2T、448G/lane optical，未来 CPO/NPO/XPO | OFC 2026 demo，样品/客户验证阶段 | 小收入高期权；若 3.2T 时间提前，增速可非常高 |
| CopperEdge ACC redriver | GN8234、GN8304 | 1.6T/3.2T active copper cable，AI scale-up/机架内外短距连接 | OFC 2026：GN8234 1.6T ACC 跑 NVIDIA 224G/lane SerDes；GN8304 3.2T/448G demo | 当前收入小；若 GB300/Rubin/ASIC rack 采用 ACC，1 年可从低个位数百万到数千万 |
| Linear optics/LPO/LRO/XPO/NPO/CPO | CEI-224G-Linear、LPO-MSA compliant TIA/driver family | 去 DSP、降低光模块功耗/成本/时延 | Q4 FY26 已开始向 LPO transceiver 出货；2026 发布 224G family | Semtech 的核心增量方向；LPO 若被 hyperscaler 放量，内容量和毛利率向上 |
| HieFo InP laser/gain chip | InP gain chip、DFB laser、C-band gain chip | coherent optics、IMDD links、1.6T/3.2T/CPO/NPO | 2026-03 收购；Alhambra, CA 扩产和招聘 | 目前贡献低但战略重要；公司称首年可增厚 non-GAAP EPS |

### 3.4 可跳过或低优先级业务

以下业务并非没有价值，但对 AI 数据中心弹性较弱，本报告仅简述：IoT cellular modules/routers/managed connectivity、LoRa 低功耗广域网、PerSe smart sensing、TVS/circuit protection、power management、broadcast video/Pro AV、PON/XGS-PON。LoRa 在 FY2026 表现不错，但不是 AI 基建瓶颈；IoT Systems 收入占 33.7%，毛利率仅 35.5%，且可能存在组合优化/出售非核心蜂窝模块业务的可能。

## 4. 当前关键产品：收入贡献、增速、AI 重要性与供需

评分：1 低，5 高。收入贡献为 FY2026 或 FY2026 末 run-rate 测算。

| 关键产品/业务 | 当前收入贡献 | 收入增速 | AI 基建重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价能力 | 依据与判断 |
|---|---:|---:|---:|---:|---:|---:|---|
| Data-center optical PMD：TIA/driver/FiberEdge/DirectEdge，含 800G/1.6T | FY2026 约 1.75-1.95 亿，占 data-center 78-87% | data-center 总体 +58% | 5 | 5 | 4 | 3.5 | 光模块每端口必需，1.6T 端口从 2026 开始进入 volume；Semtech 在 NVIDIA 1.6T DR8 OSFP demo 中有 TIA/driver 位置。 |
| 224G linear optics：GN1834L/GN1838DL/GN1887/GN1877 | 当前已出货，FY2026 收入包含在上项，LPO 单项 Q4 开始 | 从小基数高双位/三位数 | 5 | 5 | 4 | 4 | 去 DSP 可省功耗/时延，是 AI cluster 光互联的重要方向；但 LPO 链路预算和系统级调试难度高。 |
| CopperEdge ACC：GN8234/GN8304 | FY2026 估计 500-1500 万，Q4/FY27 开始更重要 | 小基数 >100% 潜力 | 4 | 4 | 3.5 | 3 | 主动铜缆解决 scale-up/短距高带宽和成本/功耗问题；Credo、Marvell、Astera 等竞争强。 |
| 448G PMD：TN622/TN14740 | FY2026 几乎无量产收入，样品/验证 | 样品到量产期权 | 4.5 | 3 | 2.5 | 3.5 | 3.2T/448G 是 2027+ 路线，若 Rubin/下一代交换 ASIC 提前，价值显著。 |
| HieFo InP gain chip/DFB laser | FY2026 无并表贡献；独立产能可能已有限量 | FY2027 高增长 | 4 | 4 | 4 | 3.5 | InP laser 是 silicon photonics/coherent/IMDD 的上游瓶颈之一；公司称需要扩 Alhambra 产能。 |

## 5. 一年后收入贡献预测：基准、乐观、极度乐观

| 产品/业务 | FY2026 基准点 | FY2027 基准 | FY2027 乐观 | FY2027 极度乐观 | 关键触发条件 |
|---|---:|---:|---:|---:|---|
| Data center 总收入 | 2.23 亿 | 3.35-3.60 亿，+50-61% | 4.00-4.50 亿，+79-102% | 5.20-6.00 亿，+133-169% | 1.6T optics 与 ACC 同时放量，客户扩产不延迟，设计赢单份额扩大 |
| 800G/1.6T TIA/driver/optical PMD | 1.75-1.95 亿 | 2.75-3.10 亿 | 3.30-3.70 亿 | 4.20-4.80 亿 | GN1834/GN1887/GN187x 系列在 1.6T OSFP/linear optics 模块中高 attach |
| Linear optics/LPO/LRO/XPO/NPO | Q4 已开始，收入低两位数百万级以下 | 5000-8000 万 | 1.0-1.5 亿 | 2.0 亿+ | LPO-MSA/CEI-224G linear 架构被 hyperscaler 量产采用，链路良率可控 |
| CopperEdge ACC redriver | 500-1500 万 | 3500-5500 万 | 7000 万-1.0 亿 | 1.3-1.8 亿 | 1.6T ACC 获 hyperscaler rack-level 量产；GN8304 3.2T/448G 进入早期订单 |
| HieFo InP gain chip/DFB laser | 并表 0 | 1500-2500 万 | 3500-5000 万 | 7000 万-1.0 亿 | Alhambra 扩产成功，gain chip 供不应求，Semtech 将 laser+TIA+driver 打包销售 |
| 448G PMD TN622/TN14740 | <300 万 | 1000-2500 万 | 4000-7500 万 | 1.0-1.5 亿 | 3.2T optical/CPO/NPO 客户验证提前，224G 到 448G 迁移加速 |

一年后 AI 重要性/紧急性排序：TIA/driver 与 linear optics 仍为 5/5；ACC 为 4-5/5，取决于 rack 内 copper 路径；HieFo/InP 为 4/5，因 laser 供给与 CPO/NPO 生态绑定；448G PMD 是 2027+ 的高期权，当前紧急性低于 224G 量产产品。

## 6. BOM 内容量、价格传导链、产能能力与认证/采纳

### 6.1 价格传导链

Semtech 晶圆/封测/部分 InP 内部或外部制造 -> Semtech TIA/driver/redriver/gain chip -> 光模块厂或主动铜缆厂 -> 交换机/NIC/服务器系统厂 -> hyperscaler。  
价格传导能力来自三点：功耗和时延降低带来的系统级价值、设计赢单后的切换成本、以及 224G/448G 高速模拟器件调试门槛。压力来自模块 ASP 年降、DSP/retimer 厂商打包销售、以及 module maker 自研/二供。

### 6.2 每 port / GPU / rack / MW 内容量测算

主要假设：1.6T OSFP 为 8x200G lanes；72-GPU AI rack 的外部网络按 36-144 个 1.6T optical ports 区间测算；单 rack 功耗按 120-140kW，1MW 约 7-8 racks。实际 topology、oversubscription、front-end/back-end 网络拆分会显著改变内容量。

| 产品 | BOM 位置 | 每 optical port / cable 内容量 | 每 GPU 内容量 | 每 rack 内容量 | 每 MW 内容量 | 当前产能/采纳/认证 |
|---|---|---:|---:|---:|---:|---|
| 1.6T TIA + driver | 1.6T OSFP/DR8/LPO/LRO/FRO 的 receiver/transmitter 模拟前端 | 1.6T port 约 15-35 美元；800G 为高个位数到十几美元 | 约 8-35 美元/GPU | 0.5k-5.0k 美元/rack | 4k-40k 美元/MW | 已在 NVIDIA 1.6T DR8 OSFP demo、multi-vendor 1.6T OSFP demos 出现；GN1834L/GN1834DL/GN1887 已可用，GN1838DL/GN1877 2026-04 预期发布。 |
| Linear optics LPO/LRO/XPO/NPO | 去 DSP 或半 retimed 光模块的高线性 TIA/driver | 1.6T port 约 20-45 美元，取决于是否 bundled telemetry/equalization | 10-45 美元/GPU | 0.7k-6.5k 美元/rack | 5k-52k 美元/MW | CEI-224G-Linear、LPO-MSA compliant；Q4 FY26 已开始 LPO transceiver 出货。客户验证门槛高，认证状态多为客户私有。 |
| CopperEdge GN8234/GN8304 | 1.6T/3.2T active copper cable 两端 redriver/linear equalization | 1.6T ACC 每条 cable Semtech IC 内容量约 10-25 美元；3.2T 约 25-60 美元 | 5-35 美元/GPU | 0.7k-8.6k 美元/rack | 5k-70k 美元/MW | GN8234 在 OFC 2026 跑 NVIDIA 224G/lane SerDes live traffic；GN8304 448G/3.2T demo。DesignCon 2026 的 Semtech/TE active copper 论文说明其在 ACC 生态中活跃。 |
| HieFo InP gain chip/DFB laser | tunable laser/coherent/IMDD 光源上游 | 800G/1.6T 增量约 5-15 美元；3.2T/CPO 若集成，可将 Semtech 总内容量推向数十美元，管理层讨论过 3.2T 约 80 美元内容量机会 | 3-40 美元/GPU | 0.2k-6.0k 美元/rack | 2k-48k 美元/MW | 2026-03 收购，CFIUS non-objection；Alhambra 扩产和招聘已启动。短期产能受限，认证为光模块/laser 客户级私有验证。 |
| 448G TN622/TN14740 | 3.2T/448G lane PMD | 3.2T optical engine/port 约 40-80 美元内容量机会 | 10-60 美元/GPU | 1k-12k 美元/rack | 8k-95k 美元/MW | OFC 2026 demo；当前为样品/验证阶段，FY2027 后半才可能更有量。 |

### 6.3 产能能力与供应链采纳

Semtech 采用 fabless/outsourced 模式为主，第三方 foundry、封测和 EMS 负责大部分制造；IoT systems 由 EMS 生产。FY2026 10-K 提到供应商 lead time、产能限制和客户需求误判会影响交付。公司并未披露按产品的美元产能，但从 FY2026 data-center 2.23 亿收入和 FY2027 +50% 指引推断，当前可支持至少 3.35 亿美元 data-center 年收入，基准情形下产能上限约 3.6 亿。HieFo 是例外：InP gain chip 具备国内制造属性且短期扩产中，供给更可能成为约束。

供应链采纳证据分为三层：  
第一，实物 demo：NVIDIA 1.6T DR8 OSFP transceiver 采用 Semtech GN1834D/GN187N1；1.6T ACC 与 NVIDIA 224G/lane SerDes 跑 live traffic。  
第二，标准/生态：CEI-224G-Linear、LPO-MSA、FRO/LRO/LPO multi-vendor OSFP、DesignCon 2026 active copper 论文。  
第三，收入验证：FY2026 data-center 2.23 亿，Q4 6300 万，FY2027 指引 +50%+。

## 7. 一年后产能、采纳与认证预测

| 产品/业务 | 基准：2027 年中 | 乐观：2027 年中 | 极度乐观：2027 年中 |
|---|---|---|---|
| TIA/driver/optical PMD | 年化产能支持 3.0 亿美元左右 optical PMD 收入；1.6T OSFP/FRO/LRO 多客户量产；NVIDIA 生态验证转为常规出货。 | 年化 3.5-4.0 亿美元；LPO/LRO 从验证转向前两大 hyperscaler 的 volume；Semtech attach rate 提升。 | 年化 4.5 亿美元+；1.6T 端口部署快于 Dell'Oro 5M ports/1-2 年预期，Semtech 成为部分模块平台默认二供/一供。 |
| Linear optics | LPO/LRO 客户认证通过率逐步提高，收入 5000-8000 万。 | CEI-224G linear 在 AI cluster 光链路中成为主流选择之一，收入 1 亿+。 | hyperscaler 为降功耗加速去 DSP，Semtech linear portfolio 形成强绑定，收入 2 亿+。 |
| CopperEdge ACC | hyperscaler 量产尾端/中期 ramp，年化产能 5000 万级；认证聚焦 1.6T ACC。 | GN8234/8304 被多个 cable/module 厂采用，年化 1 亿级；3.2T demo 转样品订单。 | ACC 在 scale-up/rack 内短距连接中显著替代光，年化 1.5 亿+；供需偏紧。 |
| HieFo InP | Alhambra 扩产初见效，年化 3000-5000 万；gain chip 与 Semtech driver/TIA 打包。 | 年化 5000-8000 万；多个 coherent/IMDD 客户完成验证。 | InP laser/gain chip 供不应求，年化 1 亿+；Semtech 形成 laser+driver+TIA 平台级销售。 |
| 448G PMD | 认证/样品收入 1000-2500 万；主要为 3.2T 和 CPO/NPO 预研。 | 2027 年下半年开始早期量产，收入 5000 万左右。 | 3.2T/448G 被下一代 AI switch 提前拉动，收入 1 亿+。 |

## 8. 订单积压、供给与未来一年业务增速推断

Semtech 官方不披露 backlog 金额，且 10-K 明确说明 backlog 多数要求 6 个月内交付、相当部分可取消或重排，不能直接当未来收入。更可靠的订单信号是：Q4 data-center 6300 万，FY2026 data-center 2.23 亿，管理层 FY2027 data-center +50%+，OFC 2026 中 NVIDIA 生态 live demo，HieFo 扩产，和 Q1 FY2027 收入指引 2.83 亿。

| 情景 | FY2027 公司总收入 | FY2027 data-center 收入 | 业务增速推断 | 供给/订单逻辑 | 取消率/风险 |
|---|---:|---:|---|---|---|
| 基准 | 12.2-13.0 亿，+16-24% | 3.35-3.60 亿，+50-61% | Data-center 拉动 SI +25-40%；AMW 中低双位；IoT 低个位到中个位 | 现有 1.6T optical 和 LPO 小规模放量，ACC/HieFo 贡献有限但增量明确 | backlog 可取消，基准假设 hyperscaler 交付窗口稳定、模块 ASP 正常下降 |
| 乐观 | 13.5-14.5 亿，+29-38% | 4.00-4.50 亿，+79-102% | SI 接近或超过 4.5 亿；semiconductor products 毛利率维持 60%+ | 1.6T 端口量产快于预期；LPO/LRO 认证通过率高；ACC 获第二个大客户 | 供应链紧张有利于排产和价格，但若模块客户 double order，后续会修正 |
| 极度乐观 | 15.5-17.0 亿，+48-62% | 5.20-6.00 亿，+133-169% | Semtech 从“上游 IC 供应商”变成多个 hyperscaler 1.6T/3.2T 平台关键器件供应商 | 1.6T switch volume 超预期、3.2T/448G 早采纳、HieFo 扩产成功、ACC scale-up 大量替代光 | 需要多个假设同时成立；任何客户切换、功耗/良率失败或 capex 延迟都会压缩估值 |

目前我对未来一年的主判断是：公司整体收入最可能在 +20% 左右，data-center 至少 +50%；如果 1.6T 光模块订单在 2026 下半年继续追单，Semtech 有机会超过管理层指引，但股价已按较高成功率定价。

## 9. 竞争格局、主流性、替代方案与切换成本

| 产品/业务 | 主要竞争对手 | Semtech 优势 | 替代/风险 | 客户切换成本 |
|---|---|---|---|---|
| 224G/200G TIA/driver | MACOM、MaxLinear、Broadcom、Marvell、TI、Coherent/Lumentum 自供、Cisco/Acacia | 高速模拟经验、FiberEdge/DirectEdge 产品线、NVIDIA/OFC demo、多模式 FRO/LRO/LPO 支持 | 模块厂自研、DSP 厂商打包、MACOM 在 linear optics 强势、价格年降 | 中高。光模块设计验证长，替换会带来 SI/BER/热/良率风险，但 hyperscaler 通常要求二供。 |
| LPO/LRO/XPO/NPO/CPO | Broadcom/Marvell DSP/retimer 路线、MACOM linear IC、Credo、Ayar Labs/光 I/O 方案 | 去 DSP 低功耗低时延，224G linear family 完整；HieFo 后可做 laser-driver-TIA 优化 | LPO 链路预算/温漂/系统调试失败；客户继续用 fully retimed optics；CPO 节奏推迟 | 高。linear optical 架构需要系统级调参，设计赢单后替换难；但架构路线尚未完全定型。 |
| CopperEdge ACC | Credo、Marvell Alaska、Broadcom、Astera、MACOM、MaxLinear、Spectra7、Point2、线缆厂方案 | GN8234/GN8304 覆盖 1.6T/3.2T，OFC 与 NVIDIA SerDes live traffic；功耗/低延迟卖点 | 被 passive DAC 限制距离、被 optical 替代、retimer/redriver 热设计失败、Credo 已有 AEC 先发 | 中。线缆/retimer 可换供应商，但 rack/cable 认证和 SI margin 使量产后切换成本上升。 |
| HieFo InP gain chip/DFB laser | Lumentum、Coherent、Broadcom、Sumitomo、Furukawa、Mitsubishi、MACOM、Nokia/Infinera、OpenLight | 美国本土 InP 能力；可与 Semtech TIA/driver 联合优化；HieFo 交易金额小、财务风险低 | 扩产慢、良率不足、客户已有垂直整合供应链；InP 供需缓和后溢价下降 | 中高。Laser/gain chip 一旦进入光源平台，重新认证耗时，但大厂有多供策略。 |
| 448G PMD | MACOM、Broadcom、Marvell、MaxLinear、Coherent/Lumentum、Acacia | 提前展示 TN622/TN14740，能承接 3.2T/448G 预研需求 | 448G 标准/SerDes/rack 节奏推迟；客户停留 224G 更久；CPO/NPO 路线改变内容量分配 | 当前低、量产后高。样品阶段可替换，平台定型后切换难。 |
| IoT/LoRa/routers/modules | Quectel、Telit Cinterion、u-blox、Digi、Ericsson Cradlepoint、Peplink、NB-IoT/蜂窝替代 | LoRa 生态强，Sierra 渠道与连接服务 | 毛利低、竞争激烈、非 AI 估值贡献有限；可能组合优化/出售 | 低到中。模块和路由器可替代，平台服务迁移有一定成本。 |

技术主流性判断：1.6T optical 在 2026 是确定方向，224G/lane TIA/driver 是主流刚需；LPO/LRO 是重要但仍需验证的低功耗方向；ACC 是 rack 内/短距 scale-up 的成本和功耗补充，不会完全替代 optical；448G/3.2T 是下一轮高期权，不是 FY2026 收入主体。

## 10. 投资监控清单

| 监控项 | 为什么重要 | 好信号 | 坏信号 |
|---|---|---|---|
| Q1/Q2 FY2027 data-center 收入 | 验证 +50% FY27 指引是否保守 | Q1 超 7000 万、Q2 继续环比增长 | Q1 低于 6800 万或 Q2 不增长 |
| Signal Integrity 毛利率 | 验证高端 optical/ACC mix | SI GM 维持 65%+，semiconductor products GM 60%+ | 价格战或良率问题导致 SI GM 下滑 |
| LPO/LRO 客户量产 | 决定内容量和估值上限 | 公司披露 LPO 收入从小规模转为显著贡献 | 客户回退到 fully retimed DSP optics |
| CopperEdge 量产客户数 | 决定 ACC 是否成为第二增长腿 | hyperscaler 量产、GN8304 3.2T design-in | 只有 demo、无量产订单 |
| HieFo 产能 | 决定 InP 收购是否成为真实收入 | 高 teens 到 5000 万收入路线明确，扩产顺利 | 认证/良率/产能延迟 |
| Backlog/PO 质量 | Semtech 官方 backlog 可取消 | 指引上调、交期延长但取消率低 | double ordering 后订单重排/取消 |
| 非核心 IoT 组合优化 | 降低低毛利拖累 | 出售低毛利模块业务或提高 IoT GM | IoT 继续占用营运资本、毛利下行 |

## 资料来源与口径

主要官方来源：  
- Semtech FY2026 10-K / SEC：`https://www.sec.gov/Archives/edgar/data/88941/000008894126000005/smtc-20260125.htm`  
- Semtech Q4 FY2026 8-K Exhibit 99.1 / SEC：`https://www.sec.gov/Archives/edgar/data/88941/000008894126000003/smtc-01252026x8k991.htm`  
- Semtech Q1/Q2/Q3 FY2026 10-Q：`https://www.sec.gov/Archives/edgar/data/88941/000008894125000101/smtc-20250427.htm`；`https://www.sec.gov/Archives/edgar/data/88941/000008894125000160/smtc-20250727.htm`；`https://www.sec.gov/Archives/edgar/data/88941/000008894125000166/smtc-20251026.htm`  
- Semtech HieFo 收购公告：`https://www.semtech.com/company/press/semtech-expands-data-center-portfolio-with-acquisition-of-hiefo-corporation`  
- Semtech OFC 2026 1.6T/3.2T demo 公告：`https://www.semtech.com/company/press/showcases-ai-interconnect-leadership-with-live-1.6t-demos-ofc-2026`  
- Semtech 224Gbps TIA/driver family 公告：`https://www.semtech.com/company/press/semtech-launches-224-gbps-ic-family-for-linear-optics-era`  
- Semtech Q4 FY2026 earnings call transcript：`https://www.fool.com/earnings/call-transcripts/2026/03/16/semtech-smtc-q4-2026-earnings-call-transcript/`  
- 行情与估值：StockAnalysis `https://stockanalysis.com/stocks/smtc/statistics/`，2026-05-08 收盘。

项目内行业交叉验证资料（非“公司调研”目录）：  
- `行业调研_AI网络_光互联_铜互联/行业调研_光DSP_TIA与CDR芯片_2026-05-08.md`  
- `行业调研_AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-05-08.md`  
- `conference_update/designcon_2026_conference_update.md`  
- `行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`

