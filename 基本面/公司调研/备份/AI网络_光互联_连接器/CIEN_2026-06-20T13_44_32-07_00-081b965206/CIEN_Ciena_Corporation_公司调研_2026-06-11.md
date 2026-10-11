# CIEN_Ciena Corporation 公司调研：AI Scale-across 光网络、相干 DCI 与云客户订单周期（2026-06-11）

## 0. 结论摘要

Ciena Corporation（NASDAQ: CIEN）是一家以相干光传输、分组光网络、光线路系统、数据中心互联（DCI）、路由交换、网络软件和服务为核心的网络系统公司。它不是短距 AI 光模块龙头，也不是 GPU 集群内部以太网交换芯片公司；它更像是 AI 数据中心从单园区走向多园区、跨城和长距互联时的“高容量光底座”供应商。投资人目前给它的核心叙事已经从传统电信资本开支周期，快速转向 hyperscaler 云客户的 AI DCI、scale-across、multi-rail 光网络升级周期。

截至 2026-06-11，CIEN 股价已反映较强的 AI 基建预期：盘中价格约 460.28 美元，市值约 651.39 亿美元；按最近四个已披露季度收入约 55.69 亿美元计算，TTM P/S 约 11.7x；按公司 FY2026 收入展望约 62-64 亿美元计算，forward P/S 约 10.2-10.5x。GAAP TTM 净利润约 4.38 亿美元，对应 GAAP trailing P/E 约 149x；若用市场常用的调整后/一致预期 EPS，forward P/E 约在高 60x 至低 70x。估值已经不是传统通信设备股，而是按 AI 光网络高增长硬件平台重新定价。

业务基本面强度来自三条线：第一，FY2026 Q2 backlog 达 77 亿美元，较上一季度增加 7 亿美元，较 FY2026 初增加约 20 亿美元，其中硬件约 64 亿美元，约 80% 预计未来 12 个月交付；第二，Q2 云客户收入占总收入 46%，同比增长 70%，直接云客户收入占 39%，同比增长 94%，过去两个季度 backlog 增量中超过三分之二来自云客户；第三，RLS 线路系统、Waveserver、WaveRouter、WaveLogic 6、800ZR/1600ZR/ZR+、DCOM、Vesta CPX/Nubis 等产品组合，把公司从传统长距传输拉向 AI data center interconnect 和 inside-data-center optical interconnect 的邻近市场。

本报告的判断是：未来一年 CIEN 的核心变量不是“有没有 AI 收入”，而是云客户订单积压能否在 FY2026 H2-FY2027 兑现为收入，同时 WaveLogic 6 Nano / 800ZR / 1600ZR、Hyper-Rail、WaveRouter、DCOM 和 Vesta/Nubis 能否把一次性的 backlog 周期扩展成多年的 AI 光互联平台周期。基准情形下，公司未来 12 个月收入可达约 68-74 亿美元；乐观情形 75-83 亿美元；极度乐观情形 85-95 亿美元，但极度乐观需要更多 hyperscaler multi-rail 订单、800ZR/1600ZR 快速量产和供应链扩产同时成立。

## 1. 公司整体业务、投资人认知与产业链定位

### 1.1 公司业务结构

Ciena 的正式报告分部包括四类：

| 分部 | 2026 财年 Q2 收入 | 占 Q2 收入 | 同比增速 | 业务含义 |
|---|---:|---:|---:|---|
| Networking Platforms | 12.991 亿美元 | 82.7% | +26.0% | 核心硬件平台，包括相干光传输、线路系统、Waveserver、WaveRouter、分组光、路由交换 |
| Converged Packet Optical，Networking Platforms 内部子项 | 9.431 亿美元 | 60.0% | +30.3% | 公司最核心的相干光传输、DCI、线路系统收入池 |
| Routing and Switching，Networking Platforms 内部子项 | 3.561 亿美元 | 22.7% | +15.8% | WaveRouter、路由交换、分组网络，云客户占比提升 |
| Platform Software and Service | 1.184 亿美元 | 7.5% | +13.9% | 平台软件、生命周期软件和相关服务 |
| Blue Planet Automation Software and Services | 0.145 亿美元 | 0.9% | -5.0% | 网络自动化软件，体量小但有粘性价值 |
| Global Services | 1.388 亿美元 | 8.8% | +18.5% | 部署、维护、专业服务 |

从产品和客户角度看，CIEN 的核心业务可以理解为三层：

1. 光层和相干传输：WaveLogic coherent DSP、6500、Waveserver、RLS / RLS Hyper-Rail、800ZR / 1600ZR / ZR+ 等，是 AI DCI 和城域/长距互联的核心。
2. 分组和路由层：WaveRouter、routing and switching，用于云客户把光传输、IP 路由和分组交换更紧密地结合。
3. 软件和服务层：Navigator、Blue Planet、平台服务和全球服务，用于网络规划、自动化、运维和客户锁定。

### 1.2 投资人眼中的公司

过去 CIEN 在投资人心中主要是通信运营商光传输设备股，受电信资本开支、库存周期和供应链周期影响较大。2024-2026 年叙事发生明显变化：云客户和 AI 数据中心 interconnect 成为主要增量，电信客户不再是唯一解释变量。2026 财年 Q2，非电信客户占收入 51%，云客户占收入 46%，直接云客户占收入 39%；四个 10% 以上客户中有三个是云客户。这个客户结构变化，是估值重定价的核心。

但需要区分三类“AI 暴露”：

| 类型 | 对 CIEN 的意义 | 当前收入确定性 |
|---|---|---|
| AI data center scale-across / DCI | 云数据中心之间、园区之间、城域/长距高容量互联，Ciena 最强 | 高，已经体现在云客户收入、backlog、RLS/Waveserver/WaveRouter |
| AI 集群内部网络 | GPU rack 内部和 leaf-spine 交换网络，短距 800G/1.6T 光模块/铜缆/交换芯片 | 中低，CIEN 不是当前主导供应商，但 DCOM、Nubis、Vesta CPX 在切入 |
| CPO/NPO/CPX 下一代光引擎 | 交换 ASIC 周边的高密度低功耗光 I/O | 当前收入低，未来可选性高 |

### 1.3 最近三年重大业务变动、转型和收购

| 时间 | 事件 | 战略含义 |
|---|---|---|
| 2023-2024 | 电信客户库存消化、供应链恢复，云客户需求开始成为更大变量 | 公司从运营商周期中恢复，云客户订单弹性提升 |
| 2024-2025 | WaveLogic 6 Extreme / Nano、800ZR、1600ZR/ZR+、RLS、Waveserver、WaveRouter 推进 | 技术重心从传统长距相干系统，扩展到高容量 DCI、coherent routing 和 AI scale-across |
| 2025-2026 | 云客户 backlog 快速累积，FY2026 Q2 backlog 达 77 亿美元 | 云客户 AI 网络建设把订单可见度推到历史高位 |
| 2026 FY Q2 | 收购 Nubis Communications 完成 | 向数据中心内部光电互联、CPX/CPO/NPO 和低功耗高密度光 I/O 延伸 |
| 2026 OFC 周期 | 推出/强化 Vesta 200 CPX、Hyper-Rail、1600ZR/ZR+、WaveLogic 6 Nano 相关产品 | 试图从 DCI 进一步进入 AI 数据中心内部和近距离互联生态 |

### 1.4 产业链位置

在 AI 基建技术栈中，CIEN 不在 GPU、HBM、交换芯片、短距光模块的最上游，而在“跨数据中心光互联”和“相干光网络系统”这一层：

| AI 基建环节 | 代表厂商 | CIEN 位置 |
|---|---|---|
| GPU / AI 加速器 | NVIDIA、AMD、ASIC 自研 | 不参与 |
| AI 交换芯片和以太网交换机 | Broadcom、NVIDIA、Marvell、Arista、Cisco | WaveRouter 参与路由/交换系统，但不是 merchant switch ASIC 龙头 |
| 短距 800G/1.6T 光模块 | Coherent、Lumentum、Innolight、Eoptolink、新易盛等 | 当前不是主要短距可插拔模块供应商 |
| DCI / coherent optics / optical transport | Ciena、Cisco/Acacia、Nokia/Infinera、Huawei、ZTE | CIEN 核心战场 |
| 光线路系统 / multi-rail / scale-across | Ciena、Nokia、Cisco、Infinera、开放线路系统生态 | CIEN 重点增量 |
| CPO/NPO/CPX 光引擎 | Broadcom、Marvell、NVIDIA、Coherent、Ayar、Nubis/Ciena 等 | CIEN 正在进入，收入仍早期 |

本地 `行业调研/` 资料显示，2026 年是 800G 扩量和 1.6T 定价窗口并存的一年，CPO/NPO/CPX 仍处在设计导入到初始量产之间。Ciena 的优势不是短距 datacom 光模块出货量，而是把 coherent DSP、线路系统、DCI、open line system 和 cloud scale-across 绑定到 hyperscaler 网络升级。

## 2. 最新股价、估值和财务健康度

### 2.1 市场数据快照

| 指标 | 数值 | 日期 / 口径 | 说明 |
|---|---:|---|---|
| 股价 | 460.28 美元 | 2026-06-11 盘中快照 | 网络金融行情快照 |
| 市值 | 651.39 亿美元 | 2026-06-11 盘中快照 | 按行情工具 |
| 52 周区间 | 44.63-461.24 美元 | 2026-06-11 | 股价已接近 52 周高点 |
| TTM 收入 | 55.69 亿美元 | Q3 FY2025-Q2 FY2026 | 本文按最近四个财报季度计算 |
| TTM P/S | 约 11.7x | 2026-06-11 | 市值 / TTM 收入 |
| FY2026 forward P/S | 约 10.2-10.5x | 按 FY2026 收入 62-64 亿美元 | 公司最新展望对应口径 |
| GAAP TTM 净利润 | 4.38 亿美元 | Q3 FY2025-Q2 FY2026 | 本文按已披露季度净利润计算 |
| GAAP trailing P/E | 约 149x | 2026-06-11 | 市值 / GAAP TTM 净利润 |
| Forward P/E | 约高 60x 至低 70x | 2026-06-11 市价、市场调整后 EPS 预期口径 | 市场常用调整后预期 EPS 与 GAAP TTM 差异较大 |
| 最新季度收入增速 | +23.6% YoY | Q2 FY2026 | 收入 15.707 亿美元 |
| FY2026 H1 收入增速 | +26.4% YoY | H1 FY2026 | 收入 29.977 亿美元 |
| FY2026 收入展望 | 约 62-64 亿美元 / +30-35% | 公司 Q2 FY2026 管理层展望 | 对比 FY2025 收入 46.33 亿美元 |
| TTM 毛利率 | 约 43.1% | Q3 FY2025-Q2 FY2026 | 本文按季度 GAAP 毛利合计计算 |
| Q2 FY2026 调整后毛利率 | 44.9% | Q2 FY2026 | 管理层披露 |
| TTM GAAP 净利率 | 约 7.9% | Q3 FY2025-Q2 FY2026 | Q2 FY2026 单季净利率约 13.9% |

估值结论：CIEN 当前估值隐含的是“AI 光网络硬件平台公司”的增长折现，不是传统光通信周期股估值。如果未来 12 个月 backlog 转收入顺利、云客户订单持续、800ZR/1600ZR 和 WaveRouter 放量，估值有基本面支撑；如果 FY2027 云订单增速明显回落，P/S 10x 以上的容错率较低。

### 2.2 资产负债表健康度

| 项目 | Q2 FY2026 数值 | 判断 |
|---|---:|---|
| 现金、现金等价物和投资 | 25.20 亿美元 | 流动性强 |
| 总资产 | 75.87 亿美元 | 资产规模随收入和库存扩大 |
| 总负债 | 24.27 亿美元 | 负债压力低于资产规模 |
| 股东权益 | 51.60 亿美元 | 净资产较厚 |
| 流动资产 | 49.47 亿美元 | 高于流动负债 |
| 流动负债 | 17.30 亿美元 | 短期偿付压力可控 |
| 流动比率 | 约 2.86x | 健康 |
| 长期债务 | 6.84 亿美元 | 相对现金很低 |
| 净现金 | 约 18.36 亿美元 | 现金投资扣除债务后仍为正 |
| 存货 | 9.54 亿美元 | 需跟踪云订单兑现和组件库存风险 |
| Q2 FY2026 经营现金流 | 1.436 亿美元 | 在增长周期中仍为正 |
| Q2 FY2026 回购 | 3.4 百万股，2.946 亿美元 | 公司在高增长与高估值阶段继续回购 |

财务健康度结论：资产负债表强，净现金充足，当前不是财务杠杆驱动的故事。主要风险在经营层面：backlog 的交付节奏、云客户订单集中、供应链交付、库存和产品代际切换，而不是短期偿债风险。

## 3. 最近五次财报对比：收入、业务结构、订单和 AI 数据中心暴露

说明：Ciena 财年通常在 10 月底或 11 月初结束。公司不按“AI 数据中心收入”单独披露，因此下表使用“云客户收入 / 直接云客户收入 / 云订单 / 高容量 DCI 产品”作为 AI 基建相关收入的代理。该代理并不等于全部 AI 收入，因为云客户收入也包含非 AI 网络需求。

| 财报季度 | 总收入 / YoY | 利润率与 EPS | 业务收入结构 | 云客户、AI 与订单信息 | Backlog / RPO / 交期判断 |
|---|---:|---|---|---|---|
| Q2 FY2026，截至 2026-05-02，发布 2026-06-04 | 15.707 亿美元，+23.6% | GAAP GM 44.0%，Adj GM 44.9%；GAAP EPS 1.53，Adj EPS 1.13 | Networking Platforms 12.991 亿美元 +26.0%；其中 CPO 9.431 亿美元 +30.3%，Routing/Switching 3.561 亿美元 +15.8%；Platform Software 1.184 亿美元 +13.9%；Blue Planet 0.145 亿美元 -5.0%；Global Services 1.388 亿美元 +18.5% | 云客户收入占 46%，约 7.23 亿美元，+70% YoY；直接云客户占 39%，约 6.13 亿美元，+94% YoY；非电信客户占 51%；云客户订单环比 +40% 以上、同比超过翻倍；RLS + Waveserver 合计 +55% YoY，RLS 高容量线路系统 +75% YoY | Backlog 77 亿美元，较上季 +7 亿美元，较财年初 +20 亿美元；硬件 backlog 约 64 亿美元，其中约 80% 预计未来 12 个月交付；ASC 606 RPO 25 亿美元，约 82.3% 预计 12 个月内确认 |
| Q1 FY2026，截至 2026-01-31，发布 2026-03-11 | 14.270 亿美元，+23.6% | Adj GM 44.3%；GAAP EPS 1.05，Adj EPS 1.00 | Networking Platforms 11.610 亿美元 +39.1%；CPO 8.372 亿美元 +46.5%；Routing/Switching 3.238 亿美元 +22.9%；Platform Software 1.183 亿美元 +4.7%；Blue Planet 0.193 亿美元 +93.8%；Global Services 1.283 亿美元 -12.2% | 云客户收入约占 42%，约 5.99 亿美元，+76% YoY；直接云客户约占 34%，约 4.85 亿美元，+101% YoY；订单 +33% YoY，云客户订单 +130% YoY | Backlog 约 70 亿美元，本文根据 Q2“环比 +7 亿美元至 77 亿美元”倒推；交付可见度高，但仍受硬件供应和客户交付窗口约束 |
| Q4 FY2025，截至 2025-11-01，发布 2025-12-11 | 13.517 亿美元，+13.6% | GAAP EPS 0.14，Adj EPS 0.78；全年 FY2025 收入 46.330 亿美元，+14.4% | Networking Platforms 10.650 亿美元 +20.0%；CPO 8.220 亿美元 +17.1%；Routing/Switching 2.430 亿美元 +30.8%；Platform Software 1.398 亿美元 +22.9%；Blue Planet 0.247 亿美元 -24.1%；Global Services 1.222 亿美元 -21.4% | 公司披露订单创纪录，+50% YoY；云客户和高容量网络是订单增量核心；FY2026 增长展望开始明显上修 | Backlog 约 57 亿美元，较上季增加逾 13 亿美元；这是 FY2026 云客户收入加速的直接前置指标 |
| Q3 FY2025，截至 2025-08-02，发布 2025-09-04 | 12.194 亿美元，+29.4% | GAAP GM 41.3%，Adj GM 42.3%；GAAP EPS 0.36，Adj EPS 0.67 | Networking Platforms 9.158 亿美元 +40.3%；CPO 6.975 亿美元 +51.5%；Routing/Switching 2.183 亿美元 +13.0%；Platform Software 1.230 亿美元 +22.2%；Blue Planet 0.189 亿美元 -27.6%；Global Services 1.618 亿美元 -3.0% | 云客户和 DCI 需求开始成为主轴；CPO 增速显著高于公司总收入 | Backlog 未在新闻稿中直接完整披露；本文根据 Q4“环比增加逾 13 亿美元至约 57 亿美元”估算 Q3 backlog 约 44 亿美元 |
| Q2 FY2025，截至 2025-05-03，发布 2025-06-05 | 约 12.69 亿美元，+23.6% | GAAP GM 41.3%，Adj GM 42.1%；GAAP EPS 0.42，Adj EPS 0.53 | Networking Platforms 10.307 亿美元 +35.4%；CPO 7.237 亿美元 +28.2%；Routing/Switching 3.074 亿美元 +56.4%；Platform Software 1.040 亿美元 +10.0%；Blue Planet 0.152 亿美元 -1.4%；Global Services 1.172 亿美元 -23.6% | 订单恢复、云客户贡献提升，但 AI DCI 叙事尚未像 FY2026 一样集中爆发 | Backlog 未在新闻稿中完整披露；从后续 12 个月的订单累积看，FY2025 Q2-Q3 是新一轮 backlog 上行前段 |

五个季度的核心变化：

1. 收入从 Q2 FY2025 的约 12.69 亿美元提升至 Q2 FY2026 的 15.71 亿美元，一年增长 23.6%。
2. CPO 子项从 7.237 亿美元提升至 9.431 亿美元，同比增长 30.3%，是最核心增量。
3. 云客户从“重要客户”变成“决定订单周期的主要客户群”。Q2 FY2026 云客户收入 46%，直接云客户 39%。
4. Backlog 从 FY2025 Q3 估算约 44 亿美元，到 FY2025 Q4 约 57 亿美元，再到 FY2026 Q1 约 70 亿美元、Q2 77 亿美元，订单积压斜率很陡。
5. 利润率从 FY2025 的 41%-42% 毛利率区间提升到 FY2026 Q2 调整后 44.9%，说明产品结构、规模利用率和供应链恢复对毛利率有正面贡献。

## 4. 2026 年最新指引、收入占比和业务侧重点

### 4.1 最新指引

公司在 Q2 FY2026 后给出的短期和全年框架：

| 指引项 | 公司口径 | 本文解读 |
|---|---:|---|
| Q3 FY2026 收入 | 17.5-18.5 亿美元 | 中点 18.0 亿美元，环比 Q2 +14.6%，显示 H2 交付加速 |
| FY2026 收入 | 约 62-64 亿美元 / +30-35% | 对 FY2025 46.33 亿美元为大幅加速 |
| Backlog | 77 亿美元 | 已超过 FY2026 全年收入指引，订单覆盖度高 |
| 硬件 backlog | 约 64 亿美元 | 80% 预计 12 个月内发货，代表约 51 亿美元硬件交付可见度 |
| 长期收入增长模型 | 8-11% | FY2026 明显超出长期模型，关键是 FY2027 能否保持高于长期模型 |

### 4.2 最新季度业务收入占比

| 业务 | Q2 FY2026 收入 | 占总收入 | YoY | 是否重点 |
|---|---:|---:|---:|---|
| Converged Packet Optical | 9.431 亿美元 | 60.0% | +30.3% | 是，AI DCI 和相干光传输主力 |
| Routing and Switching | 3.561 亿美元 | 22.7% | +15.8% | 是，WaveRouter 与云客户路由增量 |
| Platform Software and Service | 1.184 亿美元 | 7.5% | +13.9% | 中等，提升粘性和运维效率 |
| Blue Planet | 0.145 亿美元 | 0.9% | -5.0% | 小体量，战略价值大于当前收入 |
| Global Services | 1.388 亿美元 | 8.8% | +18.5% | 支撑硬件部署，不是估值主线 |

最突出业务是 CPO 和其中的 RLS/Waveserver/相干 DCI 产品；最侧重的新业务是 WaveRouter、WaveLogic 6 Nano/800ZR/1600ZR、Hyper-Rail、DCOM、Vesta/Nubis inside-data-center optical interconnect。

### 4.3 重点产品与跳过产品

重点产品和产品族：

| 产品 / 产品族 | 对应业务 | 当前阶段 | 为什么重要 |
|---|---|---|---|
| RLS / RLS Hyper-Rail | Converged Packet Optical | 已有首个 hyperscaler multi-rail 订单，其他客户试验和实验室评估 | AI 多园区、多 rail、跨数据中心光网络的关键线路系统 |
| Waveserver | Converged Packet Optical | Q2 与 RLS 合计 +55% YoY，季度收入创纪录 | 云 DCI 直接受益产品 |
| WaveLogic 6 Extreme | Converged Packet Optical | 3nm 相干 DSP，1.6Tbps 单波长 | 提高每波长容量，降低每 bit 功耗和成本 |
| WaveLogic 6 Nano / 800ZR / 1600ZR / ZR+ | Converged Packet Optical / pluggables | 800ZR 夏季 field trial，FY2027 初期量产；1600ZR/ZR+ 是下一代 | 云 DCI 可插拔相干光的重要代际升级 |
| WaveRouter | Routing and Switching | FY2026 收入预计翻倍；当前约 80% 收入来自云客户 | coherent routing、IP/光融合和云网络升级 |
| DCOM | Inside data center / 新产品 | Meta 活跃试用，第二 hyperscaler 初始 2,000 台订单，第三家实验室认证 | 公司切入数据中心内部互联和管理网络的早期产品 |
| Vesta 200 CPX / Nubis | CPX / CPO / inside data center | 收购 Nubis 完成，FY2026 收入很小；产品化周期仍早 | 如果 CPX/NPO/CPO 成为 100T/200T ASIC 周边标准，弹性很高 |
| Navigator / Blue Planet | 软件和自动化 | 收入小但提升客户粘性 | 大规模 AI 光网络需要自动化和规划工具 |

低增速或非 AI 主线、本文降权处理的业务：

| 业务 / 产品 | 降权原因 |
|---|---|
| 传统电信 metro/access 光传输项目 | 仍贡献收入，但增长和估值弹性低于云 DCI |
| 传统运营商路由替换项目 | 受运营商 capex 周期约束，非 FY2026 主线 |
| Global Services 中的维护和专业服务 | 可随硬件部署增长，但不是高毛利硬件平台叙事 |
| Blue Planet 传统网络自动化项目 | 体量小，Q2 FY2026 同比下降，短期不是收入主引擎 |
| 中国市场相关业务 | 公司管理层表示预计不会获得中国业务，收入 de minimis |

## 5. 高增长和关键业务当前贡献、增长与 AI 基建重要性

评分口径：5 为最高。收入贡献为本文根据公司披露分部、云客户占比、产品评论和行业价格估计推算，不是公司逐产品披露口径。

| 关键产品 / 业务 | 当前收入贡献估算 | 当前增速 / 证据 | AI 基建重要性 | 时间紧急性 | 供需紧张程度 | 垄断和溢价能力 | 判断 |
|---|---:|---|---:|---:|---:|---:|---|
| RLS / RLS Hyper-Rail + 高容量线路系统 | 当前季度约 2.5-4.0 亿美元，年化约 10-16 亿美元；包含在 CPO 内 | RLS 高容量线路系统 +75% YoY；已获首个 hyperscaler multi-rail 订单 | 5 | 5 | 4 | 4 | AI scale-across 的核心光底座，客户替换成本高 |
| Waveserver / 云 DCI | 当前季度约 2.0-3.0 亿美元，年化约 8-12 亿美元 | RLS + Waveserver 合计 Q2 +55% YoY，季度收入创纪录 | 5 | 5 | 4 | 3.5 | DCI 需求最直接，受云客户数据中心互联扩张驱动 |
| WaveLogic 6 Extreme coherent DSP / 1.6T 系统 | 当前季度约 1.5-2.5 亿美元经济贡献，嵌入系统收入 | 1.6Tbps 单波长、3nm DSP；提升容量和功耗 | 5 | 4 | 3.5 | 4 | 技术壁垒高，但 Cisco/Acacia、Nokia/Infinera、Marvell 等竞争强 |
| WaveLogic 6 Nano / 800ZR / 1600ZR/ZR+ | 当前收入低到中等，FY2026 以试用和导入为主；FY2027 放量 | 800ZR 夏季 field trial，初始量产预计 FY2027 初 | 4.5 | 4 | 4 | 3.5 | 可能把 CIEN 从系统向可插拔相干扩展 |
| WaveRouter / coherent routing | 当前季度约 1.0-1.7 亿美元，年化约 4-7 亿美元；公司未单列 | FY2026 收入预计翻倍；当前约 80% 来自云客户 | 4 | 4 | 3 | 3.5 | 云客户把 IP/光融合，WaveRouter 是第二增长曲线 |
| DCOM | 当前收入很小，估计低于 0.25 亿美元/季 | Meta 活跃；第二 hyperscaler 初始 2,000 台订单；第三家实验室认证 | 3.5 | 4 | 3 | 3 | inside-data-center 早期切口，验证价值大于当前收入 |
| Vesta 200 CPX / Nubis | 当前收入接近 0，FY2026 minimal | Nubis 收购完成；Vesta 200 6.4T CPX，面向 100T/200T ASIC | 4 | 3 | 2 | 4 | 高可选性，但认证和生态路径未完全确定 |
| Navigator / Blue Planet / 自动化软件 | 当前季度约 1.33 亿美元，AI 直接占比较低 | Platform Software +13.9%，Blue Planet -5.0% | 3 | 3 | 2 | 3.5 | 大规模光网络自动化需要软件，但短期收入弹性小 |

### 5.1 AI 数据中心相关收入占比估计

公司未披露“AI 数据中心收入”。本文分三层估计：

| 口径 | Q2 FY2026 收入占比 | Q2 FY2026 美元 | 可信度 |
|---|---:|---:|---|
| 云客户收入，上限代理 | 46% | 约 7.23 亿美元 | 高，公司披露 |
| 直接云客户收入，更接近 hyperscaler 代理 | 39% | 约 6.13 亿美元 | 高，公司披露 |
| 本文估计 AI DCI / AI scale-across 相关收入 | 30-40% | 约 4.7-6.3 亿美元 | 中，基于云收入、RLS/Waveserver 和 DCI 产品评论 |
| 数据中心内部 AI 网络收入 | 低个位数百分比 | 估计 <0.5 亿美元/季 | 中低，DCOM/Nubis/Vesta 仍早期 |

结论：CIEN 当前的 AI 收入主要不是 GPU rack 内短距光模块，而是云客户为 AI 训练/推理集群做跨园区、跨楼宇、跨城互联时购买的高容量相干光网络系统。

## 6. 一年后关键业务三情景预测

时间口径：未来 12 个月，即 2026-06 至 2027-06 附近。收入贡献为产品族年化或未来四季度贡献估算，不是公司正式指引。

| 产品 / 业务 | 情景 | 一年后收入贡献估算 | 收入增速 | AI 重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价 | 核心条件 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| RLS / Hyper-Rail / 高容量线路系统 | 基准 | 14-20 亿美元 | +25-35% | 5 | 5 | 4 | 4 | 现有 hyperscaler 订单交付，其他客户小规模转正 |
| RLS / Hyper-Rail / 高容量线路系统 | 乐观 | 22-30 亿美元 | +45-65% | 5 | 5 | 4.5 | 4 | multi-rail 从首单扩展到 2-3 家大云客户 |
| RLS / Hyper-Rail / 高容量线路系统 | 极度乐观 | 32-42 亿美元 | +80% 以上 | 5 | 5 | 5 | 4.5 | AI campus scale-across 项目集中开工，线路系统供给紧 |
| Waveserver / 云 DCI | 基准 | 11-15 亿美元 | +20-35% | 5 | 5 | 4 | 3.5 | 云 DCI backlog 正常转收入 |
| Waveserver / 云 DCI | 乐观 | 16-22 亿美元 | +45-65% | 5 | 5 | 4.5 | 4 | 800G/1.6T DCI 链路建设速度加快 |
| Waveserver / 云 DCI | 极度乐观 | 24-32 亿美元 | +80% 以上 | 5 | 5 | 5 | 4 | 主要云客户跨区域 AI 网络同步扩张 |
| WaveLogic 6 Nano / 800ZR / 1600ZR | 基准 | 4-7 亿美元 | 从低基数放量 | 4.5 | 4 | 4 | 3.5 | 800ZR FY2027 初量产，1600ZR 设计导入 |
| WaveLogic 6 Nano / 800ZR / 1600ZR | 乐观 | 8-13 亿美元 | 高双位数至翻倍 | 4.5 | 4.5 | 4.5 | 4 | 800ZR 在 120km DCI 场景快速被云客户采用 |
| WaveLogic 6 Nano / 800ZR / 1600ZR | 极度乐观 | 15-20 亿美元 | 数倍增长 | 5 | 5 | 5 | 4 | 1600ZR/ZR+ 认证提前、可插拔相干供给紧张 |
| WaveRouter | 基准 | 8-10 亿美元 | +40-70% | 4 | 4 | 3 | 3.5 | FY2026 翻倍后继续在云客户扩展 |
| WaveRouter | 乐观 | 11-14 亿美元 | +80-120% | 4.5 | 4.5 | 4 | 4 | coherent routing 成为云 DCI 标准架构之一 |
| WaveRouter | 极度乐观 | 16-20 亿美元 | 2 倍以上 | 4.5 | 5 | 4.5 | 4 | 云客户把更多 IP/光融合项目交给 CIEN |
| DCOM | 基准 | 0.5-1.2 亿美元 | 从低基数增长 | 3.5 | 4 | 3 | 3 | Meta 和第二客户小批量扩展 |
| DCOM | 乐观 | 1.5-3.0 亿美元 | 数倍增长 | 4 | 4.5 | 4 | 3.5 | 2-3 家 hyperscaler 认证通过并重复下单 |
| DCOM | 极度乐观 | 4-7 亿美元 | 高基数突破 | 4 | 5 | 4.5 | 4 | DCOM 形成标准化 inside-DC 部署单元 |
| Vesta 200 CPX / Nubis | 基准 | <0.5 亿美元 | 样品/NRE/小批量 | 4 | 3 | 2 | 4 | 认证和样品为主 |
| Vesta 200 CPX / Nubis | 乐观 | 1-2.5 亿美元 | 初始量产 | 4.5 | 4 | 3.5 | 4 | CPX/NPO 在 100T/200T ASIC 平台导入 |
| Vesta 200 CPX / Nubis | 极度乐观 | 4-8 亿美元 | 从零突破 | 5 | 4.5 | 4.5 | 4.5 | 头部云客户提前采用 socketed CPX 光引擎 |

## 7. BOM、单位内容量、价格传导链和当前产能/认证

### 7.1 工程口径假设

Ciena 未披露每 MW、每 rack、每 GPU、每 optical port 的标准内容量。以下为工程估算，目的是把产品和 AI 基建 BOM 建立映射：

1. 对 GPU rack 内部短距互联，CIEN 当前直接内容量很低，主要由交换机、短距 800G/1.6T 光模块、DAC/ACC/AEC、NIC/DPU 等决定。
2. 对 AI data center scale-across / DCI，CIEN 的内容量与 GPU 数量不线性相关，而与数据中心之间的 Tbps 带宽、光纤对数量、距离、线路系统、相干端口数相关。
3. 对 optical port，CIEN 的内容量包括 coherent DSP、光模块/线路卡、transponder/muxponder、open line system、ROADM/放大器、管理软件和服务。

### 7.2 当前单位内容量和价格传导

| 产品 / 业务 | BOM 内容 | 每 optical port / 每链路内容量 | 每 rack / 每 GPU / 每 MW 内容量 | 价格传导链 | 当前产能能力和采纳 |
|---|---|---:|---:|---|---|
| RLS / Hyper-Rail 线路系统 | 光线路系统、放大器、ROADM/开放线路、监控、软件、部署服务 | 每 1.6T 波长对的线路系统分摊可从数千到数万美元不等；整站点可达数十万到数百万美元 | 不直接按 rack/GPU 计价；按 AI 园区 Tbps 互联需求折算，每 MW 可能贡献数万美元到数十万美元 CIEN 内容，取决于跨园区比例 | GPU 集群规模扩大 -> 跨园区流量增长 -> fiber pair / wavelength 增加 -> line system 扩容 -> CIEN 收入 | 已被 hyperscaler 采用；首个 multi-rail 订单已获得；其他客户 trial/lab |
| Waveserver / 云 DCI | DCI 平台、相干线路卡、可插拔/嵌入式相干光、电源散热、管理软件 | 单 800G/1.6T DCI 端口系统级 ASP 可从数万美元到十万美元以上，取决于距离和配置 | 每 rack/GPU 不直接对应；若大型 AI 园区需要跨楼/跨园区 DCI，CIEN 内容随 Tbps 线性上升 | AI 训练/推理集群分布式部署 -> DCI 带宽需求 -> coherent DCI 平台采购 | Q2 与 RLS 合计收入创纪录，+55% YoY；供给处于高负荷但可交付状态 |
| WaveLogic 6 Extreme | 3nm coherent DSP、相干调制解调、线路卡/平台 | 1.6Tbps 单波长；每端口价值嵌入系统价格，估计高端端口几万美元级 | 不是 rack 内部内容；每 MW 内容取决于 DCI 带宽 | DSP 性能提升 -> 每 bit 成本/功耗下降 -> 客户愿意升级系统 | 已进入高端系统周期；Ciena 自研 DSP 是溢价来源 |
| WaveLogic 6 Nano / 800ZR / 1600ZR/ZR+ | 可插拔 coherent DSP、光引擎、模块、固件 | 800ZR 早期模块 ASP 估计 4,000-8,000 美元/端口；1600ZR/ZR+ 早期估计 8,000-15,000 美元/端口，随量产下降 | 对 rack 内容量取决于 DCI 端口是否下沉到数据中心交换/路由层；当前不是每 GPU 标配 | 400ZR -> 800ZR -> 1600ZR 提升容量，云客户用同等纤芯承载更多 AI DCI 流量 | 800ZR 夏季 field trial，FY2027 初始 volume；认证阶段为客户 trial / qualification |
| WaveRouter | 路由交换机、coherent routing、端口卡、软件 | 每 400G/800G/1.6T 端口内容量取决于配置；系统 ASP 从数万美元到数十万美元级 | rack 内部 leaf-spine 不是主战场；更多用于 DCI/metro/core 边界 | 云网络需要 IP/光融合 -> 路由平台采购 -> 端口和光层联动扩容 | FY2026 预计收入翻倍；当前约 80% WaveRouter 收入来自云客户 |
| DCOM | 数据中心内部管理/控制网络相关硬件、软件和服务 | 单设备价格未披露；本文估计低千美元到数千美元级，初期可能带服务/软件 | 若按 rack 部署，当前每 rack CIEN 内容可能为 0-5,000 美元；尚非标准 BOM | hyperscaler 试用 -> rack/cluster 管理网络标准化 -> 扩大设备采购 | Meta 活跃，第二 hyperscaler 初始 2,000 台，第三家 lab qualification |
| Vesta 200 CPX / Nubis | 6.4T CPX 光引擎、低功耗光电互联、可能与 100T/200T ASIC 配套 | 6.4T optical engine 早期单价可能在数百至数千美元；若每 100T ASIC 使用约 16 个 6.4T engine，则每 ASIC 周边 CIEN 内容可达数万美元级 | 若每高端 AI rack 配多颗 100T/200T 交换 ASIC，长期每 rack 内容量可能从数万美元起步；当前为 0 或样品 | 交换 ASIC I/O 瓶颈 -> retimed pluggable 功耗过高 -> CPX/NPO/CPO 光引擎导入 | Nubis 已收购；Vesta 200 面向未来 24 个月内产品化/认证，FY2026 收入 minimal |

### 7.3 当前产能能力、供应链采纳和认证阶段

| 产品 / 业务 | 当前美元产能 / 交付能力 | 供应链采纳程度 | 认证阶段 |
|---|---:|---|---|
| 核心硬件 backlog | 硬件 backlog 约 64 亿美元，80% 约 51 亿美元预计未来 12 个月交付 | 高，订单已经形成 | 已商业化交付 |
| RLS / Hyper-Rail | 可支撑数十亿美元级年化收入池的一部分 | 高，至少一家 hyperscaler multi-rail 订单，其他 trial | 首单商业订单 + 多客户 trial/lab |
| Waveserver / DCI | 当前已是数十亿美元级 CPO 收入池主力之一 | 高，云客户收入快速增长 | 商业化 |
| WaveLogic 6 Extreme | 已嵌入高端系统 | 高 | 商业化/规模导入 |
| WaveLogic 6 Nano / 800ZR | FY2026 以 trial 为主，FY2027 初量产 | 中，客户正在 field trial | 800ZR 夏季 field trial；1600ZR/ZR+ 设计导入/展示 |
| WaveRouter | FY2026 收入预计翻倍，年化中高数亿美元到十亿美元级潜力 | 中高，云客户占当前 WaveRouter 收入约 80% | 商业化扩张 |
| DCOM | 低收入基数，小批量订单 | 中低到中，已有 Meta、第二 hyperscaler、第三家 lab | field trial / initial order / lab qualification |
| Vesta/Nubis CPX | FY2026 minimal | 早期 | 样品、生态合作、客户设计导入前期 |

## 8. 一年后产能、采纳和认证三情景

| 产品 / 业务 | 情景 | 一年后美元产能 / 交付能力 | 供应链采纳程度 | 认证阶段预测 |
|---|---|---:|---|---|
| RLS / Hyper-Rail | 基准 | 20 亿美元级年交付能力 | 1-2 家大云客户规模采用 | 首单扩容，其他客户小规模部署 |
| RLS / Hyper-Rail | 乐观 | 30 亿美元级年交付能力 | 2-3 家 hyperscaler 采用 | 多 rail 架构进入标准采购清单 |
| RLS / Hyper-Rail | 极度乐观 | 40 亿美元以上年交付能力 | 头部云客户大范围采用 | 供给成为瓶颈，交期拉长 |
| Waveserver / DCI | 基准 | 15 亿美元级 | 已有云 DCI 项目持续 | 400G/800G 到 1.6T 升级常规化 |
| Waveserver / DCI | 乐观 | 20 亿美元以上 | 多区域 AI DCI 扩张 | 800ZR/1.6T 配套放量 |
| Waveserver / DCI | 极度乐观 | 30 亿美元级 | 大云客户同步扩容 | 光线路和相干端口紧缺 |
| WaveLogic 6 Nano / 800ZR / 1600ZR | 基准 | 5-8 亿美元 | 800ZR 初始规模采用 | FY2027 初量产，1600ZR 认证推进 |
| WaveLogic 6 Nano / 800ZR / 1600ZR | 乐观 | 10-15 亿美元 | 多家云客户采用 800ZR | 1600ZR/ZR+ 小批量导入 |
| WaveLogic 6 Nano / 800ZR / 1600ZR | 极度乐观 | 20 亿美元级 | 800ZR/1600ZR 成为 AI DCI 主流 | 认证提前，供应紧张 |
| WaveRouter | 基准 | 10 亿美元级 | 云客户继续扩展 | 商业化扩张 |
| WaveRouter | 乐观 | 14 亿美元级 | coherent routing 进入更多云网络 | 多客户规模部署 |
| WaveRouter | 极度乐观 | 20 亿美元级 | 云客户把更多 IP/光融合项目交给 Ciena | 平台级标准化 |
| DCOM | 基准 | 1 亿美元级 | 1-2 家客户小批量 | Meta/第二客户扩容，第三客户通过 lab |
| DCOM | 乐观 | 3 亿美元级 | 2-3 家 hyperscaler 采用 | 从 field trial 进入 repeat orders |
| DCOM | 极度乐观 | 5 亿美元以上 | 成为 AI data center inside-control 标准组件之一 | 多客户认证完成 |
| Vesta/Nubis CPX | 基准 | <0.5 亿美元 | 样品和 NRE | 设计导入 |
| Vesta/Nubis CPX | 乐观 | 1-2.5 亿美元 | 1-2 家客户试产 | CPX/NPO 认证 |
| Vesta/Nubis CPX | 极度乐观 | 4-8 亿美元 | 头部客户提前采用 | 进入交换 ASIC 平台配套 |

## 9. 基于 backlog、订单和供给的未来一年公司增速预测

### 9.1 当前真实订单和供给约束

关键事实：

1. Q2 FY2026 backlog 为 77 亿美元。
2. 其中硬件 backlog 约 64 亿美元，约 80% 预计未来 12 个月交付，对应约 51 亿美元硬件收入可见度。
3. 过去两个季度 backlog 增加约 20 亿美元，其中超过三分之二来自云客户。
4. Q2 云客户订单环比增长超过 40%，同比超过翻倍。
5. Q2 ASC 606 RPO 为 25 亿美元，约 82.3% 预计 12 个月内确认。RPO 小于 backlog，因为 RPO 是会计准则下未履约义务，不等于所有订单积压。
6. 公司 10-K 风险披露显示，客户可能推迟、重排或取消订单，purchase commitment 不完全等于不可取消订单。因此 backlog 不是无风险收入。

### 9.2 未来一年收入预测

基准比较口径：最近四个已披露季度收入约 55.69 亿美元。

| 情景 | 未来 12 个月公司收入预测 | 对 TTM 增速 | 关键假设 | 取消率 / 推迟风险 | 供应链判断 |
|---|---:|---:|---|---|---|
| 基准 | 68-74 亿美元 | +22% 至 +33% | FY2026 H2 按指引交付，FY2027 H1 云订单延续但增速回落；硬件 backlog 大部分转收入 | 低到中，约 5-10% 订单推迟/重排 | 供应链可满足主线交付，部分 800ZR/1.6T 新品爬坡 |
| 乐观 | 75-83 亿美元 | +35% 至 +49% | 云客户继续追加订单，RLS/Waveserver/WaveRouter 高增，800ZR 初期量产顺利 | 低，约 0-5% 订单推迟 | 关键光器件、DSP、系统制造能力扩张顺利 |
| 极度乐观 | 85-95 亿美元 | +53% 至 +71% | 多家 hyperscaler multi-rail 项目集中交付，WaveRouter 和 800ZR/1600ZR 同时放量，DCOM/Nubis 形成增量 | 很低，订单锁定强 | 供给紧张但 Ciena 获得优先产能，ASP 维持高位 |

本文更倾向基准到乐观之间。原因是 backlog 覆盖度很高，但 FY2026 的 30-35% 增长已经是超常加速，FY2027 是否继续高增长取决于云客户是否把 AI DCI 订单从一次性扩容变成连续采购。

### 9.3 交期和取消率推断

公司没有公开披露标准 lead time 和取消率。根据 backlog、硬件交付比例和客户结构，可做如下判断：

| 项目 | 判断 |
|---|---|
| 交期 | 核心硬件 backlog 80% 预计 12 个月内交付，说明主流产品交付窗口大致在 1-4 个季度；新产品如 800ZR/1600ZR、Vesta/CPX 的认证和交付周期更长 |
| 取消率 | 大云客户 AI DCI 项目取消率预计低于普通运营商项目，但交付节奏可重排；本文基准用 5-10% 推迟/重排而非永久取消 |
| 订单粘性 | 线路系统、相干平台、软件自动化一旦进入网络规划，替换成本高；可插拔 coherent 产品因标准化替换成本较低 |
| 供给瓶颈 | 可能来自 coherent DSP、先进光器件、线路系统制造、光模块认证、系统集成和客户现场部署窗口 |

## 10. 竞争格局、替代方案和技术主流判断

### 10.1 主要竞争对手

| 领域 | 主要竞争对手 | CIEN 竞争位置 |
|---|---|---|
| 相干光传输 / DCI 系统 | Nokia/Infinera、Cisco/Acacia、Huawei、ZTE、NEC/Fujitsu | 在北美云客户和高端相干系统中非常强；中国市场基本不计 |
| coherent DSP / coherent pluggables | Cisco/Acacia、Marvell、Nokia/Infinera、Coherent、Lumentum 等 | 自研 WaveLogic 是核心壁垒，但可插拔标准化会压低部分溢价 |
| 光线路系统 / open line system | Nokia、Cisco、Infinera、开放光线路生态、部分白盒 | RLS/Hyper-Rail 和软件能力提升粘性 |
| 云数据中心路由交换 | Arista、Cisco、NVIDIA、Juniper/HPE、Nokia、白盒/SONiC | WaveRouter 不是数据中心 leaf-spine 绝对主流，但在 coherent routing 和 DCI 边界有差异化 |
| 短距 800G/1.6T 光模块 | Coherent、Lumentum、Innolight、中际旭创、新易盛、Eoptolink、Fabrinet 生态 | CIEN 当前不是短距模块量产龙头 |
| CPO/NPO/CPX 光引擎 | Broadcom、Marvell、NVIDIA、Coherent、Ayar Labs、Ranovus、POET、Lightmatter、Nubis/Ciena | CIEN 通过 Nubis/Vesta 切入，仍处早期 |

### 10.2 新技术是否是主流

| 技术 | 是否可能成为主流 | 对 CIEN 的影响 |
|---|---|---|
| 800ZR / 1600ZR / ZR+ coherent pluggables | 高概率成为云 DCI 的主流增量之一 | 利好 WaveLogic 6 Nano，但标准化会带来价格竞争 |
| 1.6T 单波长 coherent transmission | 高概率成为高端 DCI/长距升级方向 | 利好 WaveLogic 6 Extreme 和高端系统 |
| RLS Hyper-Rail / multi-rail optical line systems | 中高概率在 hyperscaler AI scale-across 中扩张 | 若被多家云客户采用，CIEN 溢价和订单粘性很强 |
| coherent routing | 中高概率成为 IP/光融合方向之一 | 利好 WaveRouter，但需与 Arista/Cisco/Nokia/白盒路线竞争 |
| DCOM / inside-data-center 管理互联 | 中等概率，取决于客户标准化 | 早期产品，若通过多家 hyperscaler 认证，收入弹性高 |
| CPX/NPO/CPO 光引擎 | 长期方向确定，但形态不确定 | Vesta/Nubis 可选性大，但短期收入不能高估 |

### 10.3 风险和替代方案

| 风险 | 影响 | 替代方案 / 竞争路线 |
|---|---|---|
| 云客户订单集中 | 三个云客户已是 10% 以上客户，单一客户项目节奏会影响季度波动 | 多供应商采购，云客户内部自研/白盒化 |
| FY2026 高增长后 FY2027 回落 | 当前估值需要持续高增长 | 若 backlog 下降，估值可能快速收缩 |
| 可插拔 coherent 标准化压价 | 800ZR/1600ZR 放量后 ASP 下降 | Acacia、Marvell、Coherent、Nokia 等参与 |
| CPO/NPO 路线不确定 | Vesta/Nubis 可能导入慢 | 传统 pluggable、LPO/LRO、NPO、CPO、co-packaged copper/optical 多路线竞争 |
| 电信客户低增长 | 传统业务拖累整体增速 | 云客户和 AI DCI 抵消，但周期不完全同步 |
| 供应链和交付 | backlog 大并不等于即时收入 | DSP、光器件、制造和客户现场窗口可能限制交付 |
| 中国市场缺失 | 全球 TAM 部分不可触达 | 北美云客户和非中国市场支撑增长 |

### 10.4 客户替换成本

| 产品层 | 替换成本 | 原因 |
|---|---|---|
| 光线路系统 / RLS / Hyper-Rail | 高 | 网络规划、光纤资产、线路调测、运维软件、长期可靠性绑定 |
| Waveserver / DCI 平台 | 中高 | 与线路系统、运维、认证和客户流量工程相关 |
| WaveLogic coherent 系统 | 中高 | 自研 DSP 性能和系统集成壁垒强 |
| 800ZR/1600ZR 可插拔 | 中 | 标准化增强替换可能，但客户认证周期仍有门槛 |
| WaveRouter | 中到高 | 若进入 IP/光融合架构，替换成本提升 |
| DCOM | 低到中，目前早期 | 若标准化进入 rack/cluster BOM，替换成本才会上升 |
| Vesta CPX/Nubis | 未定 | 一旦进入 ASIC 平台，替换成本很高；当前尚在早期 |

## 11. 与本地行业资料的交叉验证

项目内 `行业调研/` 对 AI 光互联的结论，与 CIEN 当前披露基本吻合：

1. 2026 年 800G 是规模年，1.6T 是设计导入和定价窗口；CIEN 的 800ZR field trial、FY2027 初量产、1600ZR/ZR+ 路线正好对应这个节奏。
2. AI 光网络瓶颈正在从单机柜/单集群短距互联，扩展到跨数据中心、跨园区、跨地域的 scale-across；CIEN 的 RLS、Waveserver、Hyper-Rail 和 coherent routing 正在受益。
3. CPO/NPO/CPX 不是 2026 年最主要收入来源，但它是 100T/200T ASIC 时代降低功耗和提升 I/O 密度的重要方向；CIEN 通过 Nubis 和 Vesta 200 建立可选性。
4. Ciena 在本地行业资料中被定位为 coherent DCI、光引擎和线路系统的重要供应商，而不是短距 AI datacom 模块主力。这一点对投资判断很关键，避免把短距 800G/1.6T 光模块公司的估值逻辑直接套到 CIEN。

## 12. 投资跟踪指标

未来四个季度最该跟踪的不是单纯收入增速，而是以下指标：

| 指标 | 为什么重要 | 乐观信号 | 警惕信号 |
|---|---|---|---|
| Backlog 总额和硬件 backlog | 决定未来 12 个月收入可见度 | 维持 75-85 亿美元以上，硬件占比高 | FY2026 H2 交付后 backlog 快速下滑 |
| 云客户订单增速 | 决定 AI DCI 周期持续性 | 云订单继续同比高双位数以上 | 订单恢复到传统季节性水平 |
| 云客户收入占比 | 衡量公司是否继续从电信周期转向云周期 | 维持 45% 以上且直接云客户高增 | 回落到 30%-35% 且服务商低增 |
| RLS/Waveserver 增速 | AI scale-across 最直接产品信号 | 继续 +40% 以上 | 增速跌破公司整体增速 |
| WaveRouter 收入 | 第二增长曲线 | FY2026 翻倍后 FY2027 继续强增 | 云客户导入放缓 |
| 800ZR/1600ZR 认证 | 下一代 DCI 可插拔机会 | FY2027 初量产、多个云客户认证通过 | field trial 延迟或被竞争产品替代 |
| DCOM 客户数 | inside-data-center 切入验证 | Meta + 第二客户 repeat order，第三客户转商用 | 停留在小批量试用 |
| Vesta/Nubis 进度 | CPX/CPO 长期可选性 | 进入 100T/200T ASIC 设计导入 | 仅停留在展示和样品 |
| 毛利率 | 反映溢价和供应链 | Adj GM 稳定在 44%-46% | 新品爬坡或价格竞争导致下滑 |

## 13. 核心判断

CIEN 当前处在一个强订单、强云客户、强产品周期的交汇点。公司最确定的收入来源是 AI DCI 和 scale-across 光网络，而不是短距 AI 光模块。RLS、Waveserver、WaveLogic、WaveRouter 构成当前收入主线；800ZR/1600ZR、DCOM、Vesta/Nubis 构成下一阶段可选性。

从基本面看，公司资产负债表健康，净现金充足，backlog 足以支撑未来 12 个月高收入可见度。最大风险是估值已经提前反映相当多乐观预期，FY2027 订单增速、云客户集中度和新品认证会决定股价能否继续消化 10x forward sales 以上的水平。

如果只用一句话概括：CIEN 是 AI 数据中心“跨园区、跨城、跨地域光互联”最直接的美国上市受益者之一，但不是 GPU rack 内部短距光模块龙头；投资价值取决于 cloud DCI backlog 能否持续滚动，以及 Ciena 能否从 DCI 进一步切入 coherent routing 和 inside-data-center optical interconnect。

## 14. 主要资料来源

### 官方资料

- Ciena Q2 FY2026 财报新闻稿，2026-06-04：https://investor.ciena.com/news/news-details/2026/Ciena-Reports-Fiscal-Second-Quarter-2026-Financial-Results/default.aspx
- Ciena FY2026 Q2 财报电话会材料 PDF：https://s25.q4cdn.com/550667411/files/content_files/Ciena-Fiscal-Q2-2026-Financial-Results-Call.pdf
- Ciena FY2026 Q2 Form 10-Q PDF：https://d18rn0p25nwr6d.cloudfront.net/CIK-0000936395/dd920567-3459-4635-bd7b-7927c9f01760.pdf
- Ciena Q1 FY2026 财报新闻稿：https://investor.ciena.com/news/news-details/2026/Ciena-Reports-Fiscal-First-Quarter-2026-Financial-Results/default.aspx
- Ciena Q4 FY2025 与 FY2025 全年财报新闻稿：https://investor.ciena.com/news/news-details/2025/Ciena-Reports-Fiscal-Fourth-Quarter-2025-and-Year-End-Financial-Results-12-11-2025/default.aspx
- Ciena Q3 FY2025 财报新闻稿：https://investor.ciena.com/news/news-details/2025/Ciena-Reports-Fiscal-Third-Quarter-2025-Financial-Results-09-04-2025/default.aspx
- Ciena Q2 FY2025 财报新闻稿：https://investor.ciena.com/news/news-details/2025/Ciena-Reports-Fiscal-Second-Quarter-2025-Financial-Results-06-05-2025/default.aspx
- Ciena FY2025 Form 10-K：https://s25.q4cdn.com/550667411/files/doc_financials/2025/ar/10-K-Report-903049ACL.pdf
- Ciena 收购 Nubis Communications 新闻稿：https://www.ciena.com/about/newsroom/press-releases/ciena-to-acquire-nubis-communications-to-expand-its-inside-the-data-center-strategy-and-further-address-growing-ai-workloads
- Ciena Vesta 200 / CPX 光引擎新闻稿：https://www.ciena.com/about/newsroom/press-releases/ciena-unveils-the-industrys-highest-density-lowest-power-pluggable-optical-engine-to-meet-data-center-ai-demands
- Ciena OFC 2026 / 高速连接创新新闻稿：https://www.ciena.com/about/newsroom/press-releases/ciena-solidifies-ai-networking-leadership-unveils-new-innovations-for-high-speed-connectivity

### 本项目内允许引用的行业资料

- `行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`
- `行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`
- `行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`
- `行业调研/AI网络_光互联_铜互联/行业调研_光DSP、TIA与CDR芯片_2026-06-11.md`
- `行业调研/产业背景/顶级会议信息/ofc_2026_conference_update.md`

### 市场数据

- CIEN 实时行情和市值快照：2026-06-11 网络金融行情工具。
- 估值倍数为本文根据行情、市值、公司已披露季度收入/利润和 FY2026 指引计算；forward P/E 因市场使用调整后 EPS 预期口径，与 GAAP TTM P/E 差异较大，报告中已分开列示。
