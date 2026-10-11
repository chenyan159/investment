# CSCO Cisco Systems：公司业务与 AI 数据中心链条全面尽调（截至 2026-05-10）

> 口径说明：本报告新写，未引用或比对 `工作台v5/公司调研` 目录内其他文件。行业判断结合项目内非“公司调研”目录的 AI 网络、AI 数据中心、800G/1.6T 光模块、AI Fabric 软件等资料，并用 Cisco 官方财报、公告和外部行业资料交叉验证。2026-05-10 为周日，美股未开盘；股价采用 2026-05-08 收盘附近的最新可得行情。Cisco Q3 FY2026 财报预定 2026-05-13 盘后披露，因此当前最新已发布财报为 FY2026 Q2。

## 0. 高浓度结论

- Cisco 仍是全球最大网络设备和企业网络平台公司之一，投资人传统上把它看作“高毛利、强现金流、分红回购、低到中个位数增长”的成熟科技股；2025-2026 年叙事正在被 AI 后端网络、Silicon One、800G/1.6T 光互联和 Splunk 数据/安全平台重新定价。
- 最新基本面最强信号是订单：FY2025 AI infrastructure orders 超过 20 亿美元；FY2026 Q1 hyperscaler AI 订单 13 亿美元；FY2026 Q2 进一步到 21 亿美元，FY2026 上半年已超过 30 亿美元。Q2 total product orders 同比 +18%，Service Provider & Cloud orders +65%，Networking product orders 超过 +20%。
- 公司 FY2026 指引已上调到收入 612-617 亿美元，中点 614.5 亿美元，较 FY2025 的 566.54 亿美元约 +8.5%；Q3 FY2026 指引收入 154-156 亿美元，non-GAAP gross margin 65.5%-66.5%，non-GAAP operating margin 33.5%-34.5%。
- 最新财报业务结构中，Networking 占总收入约 54.0%，同比 +21%，是最突出的增长引擎；Security 占 13.1%，同比 -4%，说明 Splunk/安全业务战略价值很高但短期增长并不顺；Observability 仅 1.8%，同比持平。
- AI 相关核心产品不是 GPU，而是 AI Ethernet fabric：Silicon One G300/P200、N9000/8000/N9100、Nexus One/Nexus Dashboard、Acacia 光学/相干光模块、800G/1.6T optics、Secure AI Factory with NVIDIA、UCS/AI POD、安全与可观测性软件。
- 竞争格局很硬：Arista 在 AI Ethernet 系统层强，NVIDIA Spectrum-X/Spectrum-6 把 NIC/DPU/交换机/软件打包，Broadcom+白盒/ODM 是 hyperscaler 的低成本默认选项，HPE/Juniper、Nokia、Dell/SONiC 也在抢份额。Cisco 的优势是 silicon+system+NOS+optics+security+observability 全栈和企业客户信任；短板是 hyperscaler 直采生态中并非默认第一供应商。
- 估值已不便宜：以 2026-05-08 收盘价约 96.57 美元、稀释股本约 39.84 亿股估算，市值约 3,847 亿美元，TTM P/E 约 34x-35x，P/S 约 6.5x；若用 FY2026 non-GAAP EPS 指引中点 4.15 美元，forward P/E 约 23.3x。AI 订单必须继续兑现为收入，否则估值弹性会受限。

## 1. 公司整体业务、定位、转型与财务健康

### 1.1 公司业务和投资人心智

Cisco Systems 是网络基础设施、企业安全、协作、可观测性和 IT 服务公司。它的收入按类似产品和服务分为 Networking、Security、Collaboration、Observability、Services。2026 年最新财报中，Networking 仍是绝对主轴，Security/Splunk 是战略第二曲线，Services 提供稳定利润和递延收入。

投资人心中 Cisco 的形象可以分三层：

- 传统形象：企业网络和运营商网络龙头，现金牛，分红回购稳定，收入周期受企业/运营商设备更新影响。
- 2024-2025 新形象：通过 280 亿美元现金收购 Splunk，转向“networking + security + observability + data platform”的软件化公司。
- 2026 新叙事：AI 后端网络和 AI 数据中心 fabric 供应商。Cisco 不卖 GPU，但能捕获 AI 集群中 800G/1.6T 交换机、光模块、软件、运维和安全的价值。

### 1.2 最近 3 年重大业务变动

| 时间 | 事件 | 影响 |
|---|---:|---|
| 2024-03-18 | 完成收购 Splunk，157 美元/股现金，总股权价值约 280 亿美元 | Cisco 变成全球大型软件公司之一，强化安全、SIEM、可观测性和数据平台，但也带来债务、商誉/无形资产和整合风险 |
| 2024-2025 | 产品分类重构为 Networking、Security、Collaboration、Observability、Services | 更突出软件、安全和可观测性，也让 Splunk 对 Security/Observability 增速产生同比扰动 |
| 2025 | AI infrastructure orders 从初始 10 亿美元目标提升并最终超过 20 亿美元 | 证明 Cisco 已进入 hyperscaler AI 后端网络采购，但收入确认仍有交付和客户资格认证周期 |
| 2025-2026 | Campus networking refresh 与 Wi-Fi 7、smart switches、secure routers 进入更新周期 | 企业网络传统盘子恢复，Q1/Q2 FY26 campus 相关订单加速 |
| 2026-02 | 发布 Silicon One G300、102.4T N9000/8000、1.6T OSFP、800G LPO、Nexus One/AgenticOps | Cisco 把 AI 网络从“交换机硬件”升级为 silicon+optics+software+telemetry 全栈 |
| 2026-03 | 扩展 Secure AI Factory with NVIDIA，支持 Cisco Silicon One 或 NVIDIA Spectrum-X/Spectrum-6 路线 | 有利于企业 AI 工厂和 neocloud 采购，但也意味着 Cisco 在部分方案中承认 NVIDIA silicon 是重要选择 |

### 1.3 产业链位置

Cisco 位于 AI 基建产业链的网络层和安全/运维层：

- 上游：TSMC/先进制程、SerDes/IP、内存、光芯片、DSP、激光器、PCB、电源/散热、ODM/EMS。
- Cisco 自有能力：Silicon One 交换/路由芯片，Nexus/N9000/8000/8223/N9100 系统，NX-OS/ACI/Nexus One/Nexus Dashboard，Acacia 相干光学和光模块技术，Splunk/ThousandEyes/AI Defense/Hybrid Mesh Firewall。
- 下游：hyperscaler、neocloud、sovereign cloud、运营商、企业 AI 数据中心、渠道/系统集成商。
- 价值位置：不直接拿 GPU/HBM 最大 BOM，但能拿 AI 集群中随 GPU 数量放大的 scale-out/scale-across 网络、光互联、telemetry、网络安全和服务收入。

### 1.4 最新估值与经营指标

| 指标 | 最新口径 | 读数 |
|---|---:|---|
| 股价 | 2026-05-08 收盘附近，2026-05-10 周日未开盘 | 约 96.57 美元 |
| 市值 | 股价 x Q2 FY26 稀释股本约 39.84 亿股 | 约 3,847 亿美元 |
| TTM 收入 | FY25 Q3 + FY25 Q4 + FY26 Q1 + FY26 Q2 | 约 590.54 亿美元 |
| P/S | 市值 / TTM 收入 | 约 6.5x |
| TTM GAAP 净利 | 同上四季官方净利合计 | 约 113.49 亿美元 |
| TTM 净利率 | TTM GAAP 净利 / TTM 收入 | 约 19.2% |
| TTM P/E | 市值 / TTM GAAP 净利 | 约 34x-35x |
| Forward P/E | 股价 / FY26 non-GAAP EPS 指引中点 4.15 美元 | 约 23.3x |
| 最新季度收入增速 | Q2 FY26 | +10% YoY |
| FY2026 收入指引增速 | 指引中点 614.5 亿美元 vs FY25 566.54 亿美元 | 约 +8.5% |
| 最新 GAAP gross margin | Q2 FY26 | 65.0% |
| 最新 non-GAAP gross margin | Q2 FY26 | 67.5% |
| 最新 GAAP operating margin | Q2 FY26 | 24.6% |
| 最新 non-GAAP operating margin | Q2 FY26 | 34.6% |

### 1.5 资产负债表健康度

| 项目 | Q2 FY2026 | 评价 |
|---|---:|---|
| Cash + investments | 158 亿美元 | 现金仍充足，但低于总债务 |
| Total current assets | 351.31 亿美元 | 流动资产大 |
| Total current liabilities | 约 365 亿美元级别 | current ratio 约 0.96，短期流动性不宽 |
| Total debt | 约 300 亿美元级别 | Splunk 收购后杠杆上升，净债务约 140 亿美元级别 |
| Goodwill | 约 591 亿美元 | Splunk 后商誉很重 |
| Purchased intangibles | 约 80-90 亿美元级别 | 摊销影响 GAAP 盈利 |
| RPO | 434 亿美元，+5%；Product RPO +8%，长期 product RPO 118 亿美元，+11% | 订单/递延可见度强，是财务健康的重要缓冲 |
| Deferred revenue | 284 亿美元，+2% | 软件、服务和订阅基础稳定 |
| Q2 operating cash flow | 18 亿美元，-19% | 受税款和 AI 需求相关投入影响，短期现金流低于收入增长 |
| FY26 H1 capital return | 66 亿美元 | 分红回购力度仍大 |

结论：财务健康但不再是“净现金无压力”的老 Cisco。现金流、RPO、递延收入和毛利率仍强，足以支持分红回购和研发；但 Splunk 后债务、商誉、无形资产与内存涨价压力提高了财务弹性要求。如果 AI 订单转收入并维持 65%+ gross margin，资产负债表风险可控；若 AI hyperscaler 大单毛利低于传统企业网络，同时 Splunk 增长不恢复，估值和债务承受力会被市场重新审视。

## 2. 最新和最近 4 次财报复盘

> 注：Cisco 不按 Networking/Security/Collaboration/Observability 单独披露毛利率，也不披露严格意义的 backlog、book-to-bill、lead time、取消率。下表用 RPO、product orders、AI infrastructure orders 和递延收入作为 backlog/order proxy；“AI 数据中心收入占比”为基于订单、FY26 hyperscaler revenue 指引、收入确认节奏和 Networking 规模的模型估算。

| 财报季度 | 收入与业务结构 | 订单/RPO/交期/取消率 proxy | 利润率 | AI 数据中心相关信息与占比估算 |
|---|---|---|---|---|
| Q2 FY2026，2026-01-24，2026-02-11 发布 | 总收入 153.49 亿美元，+10%；Networking 82.94 亿，+21%；Security 20.18 亿，-4%；Collaboration 10.54 亿，+6%；Observability 2.77 亿，持平；Services 37.07 亿，-1% | Product orders +18%；Networking product orders >+20%；Service Provider & Cloud orders +65%；hyperscaler AI orders 21 亿美元；RPO 434 亿，+5%；Product RPO +8%；ARR 310 亿，+3%；subscription revenue 78 亿，占收入 51%；未披露取消率，RPO/订单上行未显示取消恶化 | GAAP GM 65.0%，product 63.9%，services 68.4%；non-GAAP GM 67.5%，product 66.4%，services 70.9%；GAAP OM 24.6%，non-GAAP OM 34.6% | FY26 H1 AI orders 已超过 30 亿美元；Q2 计算口径 AI/DC 收入估计 8-12 亿美元，占总收入约 5%-8%，占 Networking 约 10%-15%；收入确认滞后订单 1-4 个季度 |
| Q1 FY2026，2025-10-25，2025-11-12 发布 | 总收入 148.83 亿美元，+8%；Networking 77.68 亿，+15%；Security 19.80 亿，-2%；Collaboration 10.55 亿，-3%；Observability 2.74 亿，+6%；Services 38.06 亿，+2% | Product orders +13%；hyperscaler AI orders 13 亿美元；RPO 429 亿，+7%；Product RPO +10%，长期 Product RPO 118 亿，+13%；campus switching/routing/wireless/IoT 订单加速 | GAAP GM 65.5%，product 64.5%，services 68.4%；non-GAAP GM 68.1%，product 67.2%，services 70.7%；GAAP OM 22.6%，non-GAAP OM 34.4% | AI/DC 收入估计 6-9 亿美元，占总收入约 4%-6%；订单明显领先收入，说明 backlog 正在建立 |
| Q4 FY2025，2025-07-26，2025-08-13 发布 | 总收入 146.73 亿美元，+8%；Networking 76.33 亿，+12%；Security 19.52 亿，+9%；Collaboration 10.42 亿，+2%；Observability 2.59 亿，+4%；Services 37.87 亿，持平 | FY25 全年 AI infrastructure orders 超过 20 亿美元；RPO 417 亿，+6%；Product RPO +4%；FY26 初始收入指引 590-600 亿美元 | GAAP GM 65.7%，product 64.7%，services 68.3%；non-GAAP GM 68.4%，product 67.5%，services 70.8%；GAAP OM 23.5% 左右，non-GAAP OM 34.3% | AI/DC 收入估计 5-8 亿美元，占总收入约 3%-5%；webscale orders 明显增长，进入 FY26 转收入窗口 |
| Q3 FY2025，2025-04-26，2025-05-14 发布 | 总收入 141.49 亿美元，+11%；Networking 70.68 亿，+8%；Security 20.13 亿，+54%；Collaboration 10.31 亿，+4%；Observability 2.61 亿，+24%；Services 37.75 亿，+3% | Q3 AI infrastructure orders 超过 6 亿美元，FY25 YTD 超过 10 亿美元；Product orders +20%；RPO 405 亿，+7%，Product RPO +6%，Services RPO +8% | GAAP GM 65.6%，product 64.4%，services 68.7%；non-GAAP GM 68.6%，product 67.6%，services 71.3%；non-GAAP OM 34%+ | AI/DC 收入估计 3-5 亿美元，占总收入约 2%-4%；Security/Observability 高增主要由 Splunk 同比并表贡献，不等同 AI 网络 |
| Q2 FY2025，2025-01-25，2025-02-12 发布 | 总收入 139.91 亿美元，+9%；Networking 68.50 亿，-3%；Security 21.11 亿，+117%；Collaboration 9.96 亿，+1%；Observability 2.77 亿，+47%；Services 37.57 亿，+6% | RPO 412.68 亿，+16%，其中未来 12 个月确认比例 51%；Product RPO +25%，Services RPO +8%；当季 web-scale AI orders 超过 3.5 亿美元，FY25 YTD 超过 7 亿美元 | GAAP GM 65.1%，product 63.7%，services 68.9%；non-GAAP GM 68.7%，product 67.7%，services 71.6% | AI/DC 收入估计 1.5-3.5 亿美元，占总收入约 1%-3%；Networking 仍在传统去库存/换代影响中，AI 网络还未完全体现在收入 |

### 2.1 订单和交期判断

- 官方 backlog proxy 最强的是 RPO：Q2 FY26 RPO 434 亿美元，Product RPO +8%，长期 Product RPO 118 亿美元 +11%。这不是纯硬件 backlog，但能说明订单可见度强。
- AI 订单曲线非常陡：Q2 FY25 当季 >3.5 亿美元，Q3 FY25 >6 亿美元，FY25 全年 >20 亿美元；Q1 FY26 >13 亿美元，Q2 FY26 >21 亿美元，FY26 上半年 >30 亿美元。
- 交期推断：成熟 400G/800G 以太网系统可在 1-3 个季度交付并确认；新 1.6T、102.4T G300、CPO/LPO、客户定制 telemetry 的交付和资格认证更接近 2-6 个季度。大型 hyperscaler 项目通常有 lab qualification、pilot cluster、production ramp 三段。
- 取消率：Cisco 未披露。订单、RPO、递延收入均增长，且管理层明确谈到 AI 需求相关投入和供应链锁定，目前没有异常取消证据。主要取消风险来自 AI capex 延迟、电力/液冷/园区许可瓶颈、GPU 交付窗口变化，而不是 Cisco 单点需求消失。

## 3. FY2026 最新指引、业务占比和产品映射

### 3.1 最新 FY2026 指引

| 指引项目 | 最新指引 |
|---|---:|
| Q3 FY2026 revenue | 154-156 亿美元 |
| Q3 FY2026 non-GAAP gross margin | 65.5%-66.5% |
| Q3 FY2026 non-GAAP operating margin | 33.5%-34.5% |
| Q3 FY2026 non-GAAP EPS | 1.02-1.04 美元 |
| FY2026 revenue | 612-617 亿美元 |
| FY2026 GAAP EPS | 3.00-3.08 美元 |
| FY2026 non-GAAP EPS | 4.13-4.17 美元 |

管理层同时提示，内存价格显著上涨，Cisco 已采取涨价、调整渠道/客户合同条款、利用供应链规模锁供三类措施。Q3 non-GAAP GM 指引 65.5%-66.5% 低于 Q2 67.5%，说明 AI 和高速网络需求虽强，但成本/产品组合压力真实存在。

### 3.2 Q2 FY2026 业务收入占比

| 业务 | Q2 FY2026 收入 | YoY | 占总收入 | 重点程度 |
|---|---:|---:|---:|---|
| Networking | 82.94 亿美元 | +21% | 54.0% | 最高，AI 网络和 campus refresh 同时拉动 |
| Security | 20.18 亿美元 | -4% | 13.1% | 战略重要，但短期增长弱 |
| Collaboration | 10.54 亿美元 | +6% | 6.9% | 非核心 AI，偏成熟 |
| Observability | 2.77 亿美元 | 0% | 1.8% | Splunk/Nexus/Splunk integration 对 AI 运维重要，但独立收入小 |
| Services | 37.07 亿美元 | -1% | 24.2% | 稳定现金流和客户粘性 |
| Product subtotal | 116.42 亿美元 | +14% | 75.8% | 订单加速主体 |

### 3.3 产品映射：重点、潜力小业务与跳过项

| 业务/产品组 | 代表产品/型号 | 与 AI 数据中心关系 | 预计利润率/增长判断 |
|---|---|---|---|
| Silicon One AI switching | G300、G200、P200、N9000、Cisco 8000、8223、N9364E-SP2R-X、N9364F-SG3 | 后端 scale-out/scale-across 以太网 fabric 核心；G300 102.4T，支持 1.6T；P200 51.2T 适合 routing/DCI/universal spine | 系统毛利低于传统企业软件但仍高于白盒；订单增长最快；1.6T 和 102.4T 是 FY26H2-FY27 弹性 |
| AI optics / Acacia | 800G ZR/ZR+、1.6T OSFP、800G LPO、相干 pluggables、co-packaged optics engine | GPU 集群跨 rack、跨 DC、scale-across 的瓶颈部件；光互联是 AI capex 中增速最高的环节之一 | 早期 1.6T/相干/CPO 溢价更强；行业供应紧张，Acacia bookings/光学需求是潜力小业务 |
| Nexus One / Nexus Dashboard / AgenticOps | Unified fabric、AI job observability、native Splunk integration、telemetry | AI 集群需要 job-aware telemetry、拥塞控制、故障定位和 GPU 利用率优化 | 软件毛利高，直接收入披露少；attach rate 提升比硬件毛利更关键 |
| Secure AI Factory with NVIDIA | Cisco AI POD、Cisco UCS、Nexus Hyperfabric AI、N9000/N9100、AI Defense、Hybrid Mesh Firewall、Splunk Enterprise Security | 企业/sovereign/neocloud 把 GPU、网络、安全、运维打包采购；支持 Cisco Silicon One 和 NVIDIA Spectrum-X 路线 | 规模可能小于 hyperscaler 网络，但客户粘性高，销售周期更企业化 |
| Security/Splunk AI security | AI Defense、Hypershield、XDR/SIEM/SOAR、Secure Access、Isovalent、Hybrid Mesh Firewall | 模型、agent、workload、DPU/BlueField、东西向流量安全；AI 工厂必须安全可审计 | 最新 Security -4%，短期不是高增长；但若 AI governance 预算落地，弹性来自 Splunk/AI Defense |
| UCS/compute/Hyperfabric | UCS servers、Cisco AI PODs、Hyperfabric AI clusters、Intersight | Cisco 不主导 GPU，但可卖企业 AI 集成系统和管理 | 管理层提到 compute/服务器需求强，增长可观但竞争极强 |

跳过或低优先级业务：传统 Webex seat/终端、普通会议室设备、低端 SMB 网络、非 AI 的常规服务续约、传统语音/协作、非 AI 旧代 campus 设备、一般性运营商路由更新。这些业务贡献现金流，但不是未来 12 个月 AI 相关估值弹性的主要来源。

不能漏掉的小业务/小产品：

- Acacia 相干光学和 800G/1.6T/CPO/LPO：收入未单列，但在 AI scale-across 与 DCI 中可能是 Cisco 边际增长和毛利弹性的关键。
- Nexus One + Splunk native integration：AI job observability 如果成为客户验收的一部分，软件 attach 可从“附属管理工具”变成“生产控制系统”。
- N9100 + NVIDIA Spectrum-X/Spectrum-6：它会分流 Cisco 自有 Silicon One 的 silicon 价值，但能让 Cisco 进入 NVIDIA Cloud Partner/NCP reference architecture 项目，守住系统、OS、服务和企业客户入口。
- AI Defense + Hybrid Mesh Firewall on BlueField：若 agentic AI 和 sovereign AI 对审计/隔离/策略下沉有强需求，安全收入可能从当前低增长恢复。

## 4. 高增长/关键产品当前收入贡献与战略评分

评分 1-5，越高代表越重要/越紧急/越供不应求/越有溢价能力。收入为模型估算，因 Cisco 未按这些产品单独披露。

| 产品/业务 | 当前收入贡献估算 | 当前增速/订单 | AI 技术栈重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价能力 | 结论 |
|---|---:|---|---:|---:|---:|---:|---|
| AI Ethernet switching systems：Silicon One G300/P200、N9000/8000/8223 | FY26 hyperscaler AI revenue 管理层口径可超过 30 亿美元；Q2 收入估计 8-12 亿美元 | FY26 H1 hyperscaler AI orders >30 亿美元，Q2 单季 21 亿美元，订单同比大幅加速 | 5.0 | 5.0 | 4.0 | 3.5 | Cisco 最重要的 AI beta，决定估值能否从成熟网络股转向 AI infra 供应商 |
| AI optics / Acacia / 800G-1.6T / coherent / LPO-CPO | 当前年化收入估计 8-15 亿美元级别，未单列 | 行业 800G+ 光模块 2026 出货占比预计 >60%；Cisco 新发布 1.6T OSFP 和 800G LPO | 4.5 | 5.0 | 4.5 | 4.0 | 小而关键，供需紧张和技术壁垒强，可能被市场低估 |
| Nexus One / telemetry / AgenticOps / Splunk integration | 直接 AI fabric software attach 估计 5-10 亿美元年化；总 ARR 310 亿美元 | 软件收入 Q2 57 亿美元 +2%，订阅收入 78 亿美元，占总收入 51%；产品 ARR +6% | 4.0 | 4.5 | 3.0 | 4.0 | 高毛利、强粘性；收入披露不透明，但对 GPU 利用率和故障恢复很关键 |
| Secure AI Factory with NVIDIA / AI POD / UCS | 企业 AI 工厂相关年化收入估计 10-25 亿美元区间，含 UCS/网络/安全/服务 | Cisco 与 NVIDIA 扩展架构，Cisco 可提供 Silicon One 或 Spectrum-X/Spectrum-6 路线 | 4.0 | 4.0 | 3.5 | 3.0 | 更偏企业/sovereign/neocloud，未必爆发最快，但销售面更宽 |
| AI security / Splunk / AI Defense / Hypershield | Security Q2 20.18 亿美元，Observability 2.77 亿美元，但 AI 专项占比小 | Security -4%，Observability 持平；Splunk 整合仍在过渡 | 3.5 | 4.0 | 2.5 | 3.5 | 战略必要但短期没证明高增长，重点看 AI Defense 和 Splunk 是否形成 attach |

## 5. 未来一年三情景预测：收入、增长、重要性与供需

| 产品/业务 | 基准情景，未来 12 个月 | 乐观情景，未来 12 个月 | 极度乐观情景，未来 12 个月 |
|---|---|---|---|
| AI Ethernet switching systems | 收入 40-50 亿美元，YoY +35%-55%；G300/P200 从 beta/早期出货进入更多 production cluster；重要性 5，供需 4，溢价 3.2 | 收入 55-70 亿美元，YoY +70%-100%；neocloud/sovereign cloud 和第二批 hyperscaler 放量；重要性 5，供需 4.5，溢价 3.8 | 收入 80-100 亿美元，YoY +130%-180%；1.6T/102.4T 快速替代 800G/51.2T，Cisco 拿到多个大客户第二供应商甚至主供应商份额；供需 5，溢价 4 |
| AI optics / Acacia | 收入 14-20 亿美元，YoY +30%-60%；800G/LPO/相干光学稳步附着 | 收入 22-32 亿美元，YoY +80%-120%；1.6T OSFP、800G ZR/ZR+ 和跨 DC scale-across 项目扩大 | 收入 40 亿美元以上；若 CPO/3.2T engine 提前被关键客户接受，Cisco optics 从“配套”变成稀缺卖点 |
| Nexus One / telemetry / Splunk integration | AI fabric software/telemetry 直接相关收入 8-13 亿美元，attach 稳定提升；总软件低个位数增长 | 15-25 亿美元；AI job observability 和 Splunk native integration 成为大型集群验收项 | 30 亿美元以上；Cisco 把网络运维、AI job telemetry 和安全日志合成 AI 工厂控制平面 |
| Secure AI Factory / AI POD / UCS | 15-25 亿美元，YoY +25%-40%；企业 AI pilot 到 production | 30-40 亿美元，YoY +60%-100%；NVIDIA Enterprise RA/NCP 带动渠道复制 | 50 亿美元以上；edge/enterprise inference 与 sovereign AI 批量复制，Cisco 吃到全栈集成和服务 |
| AI security / Splunk / AI Defense | Security 恢复到 +3%-6%，AI security 仍小；AI Defense 做战略 attach | Security +10%-15%，AI governance/agent security 预算显性化 | Security +20% 以上，Splunk/AI Defense/Hybrid Mesh Firewall 成为 AI 工厂标准模块 |

## 6. BOM、每 MW/每 rack/每 GPU/每 optical port 内容量与价格传导

> 下列为模型化 BOM，不代表 Cisco 报价。实际取决于 GPU 平台、oversubscription、rail-optimized topology、是否用 DAC/AEC/optics、客户自研 SONiC/FBOSS/NX-OS、是否捆绑服务和多年订阅。

### 6.1 AI Ethernet switching systems

| 维度 | 内容量与价值链 |
|---|---|
| 每 switch | 51.2T 系统通常对应 64 x 800G；102.4T 系统对应 64 x 1.6T 或 128 x 800G 等效。Cisco G300 新系统覆盖 102.4T，N9000/8000 可支持 1.6T。 |
| 每 rack | 100-140kW GPU rack 假设 64-72 GPU，scale-out 通常至少 64-72 个 800G/1.6T 端点；含 leaf/spine/冗余后，每 rack 对应 100-250 个 800G 等效交换端口需求。 |
| 每 GPU | AI scale-out 口径通常对应 1-3 个 800G 等效网络侧端口，训练集群冗余和跨 rack 通信越强，端口数越高。Cisco 不一定拿 NIC 价值，主要拿 switch-side port、NOS、telemetry、optics attach。 |
| 每 MW | 1MW IT power 约对应 7-10 个高密 GPU rack、500-720 个 GPU；网络侧需求约 800-2,500 个 800G 等效交换端口。若 Cisco 全栈中标，系统+软件+服务+可选光学价值约 150 万-1,200 万美元/MW。 |
| 每 optical port | 800G switch port 系统侧价值粗略 1,000-3,000 美元；1.6T early port 价值 2,500-6,000 美元；若叠加光模块，两端 optics/cables 可能再增加数百至数千美元/链路。 |
| BOM 拆分 | Switch ASIC/SerDes/package 25%-35%；PCB/电源/散热/机箱 15%-25%；光/电端口和 cage/connector 10%-20%；内存/packet buffer 5%-15%；软件、支持、测试、质保 10%-20%。 |
| 价格传导 | GPU cluster RFP -> hyperscaler/neocloud/enterprise -> Cisco or ODM/system vendor -> Silicon One/Nexus/optics/软件 -> 组件供应商。内存涨价会压 product GM，Cisco 已涨价和改合同条款传导。 |
| 当前产能能力，美元计 | 官方 FY26 hyperscaler AI revenue 目标已超过 30 亿美元，且 FY26 H1 orders 已超过 30 亿美元；当前可服务产能至少是数十亿美元/年，但 1.6T/G300 仍在爬坡。 |
| 供应链采纳/认证 | G300、系统和 optics 官方口径为 2026 年出货；客户引用覆盖 AMD、Intel、du、Sharon AI、Cirrascale、CDW、Computacenter、WWT、DDN、VAST、NetApp 等生态。Hyperscaler 认证通常经历 lab -> pilot -> production。 |

### 6.2 AI optics / Acacia / 800G-1.6T

| 维度 | 内容量与价值链 |
|---|---|
| 每 rack | rack 内短距可能用 DAC/AEC，跨 rack/spine 使用 800G/1.6T optics。每 GPU rack 可能需要 50-150 条高速光链路，视 topology 和冗余而变。 |
| 每 GPU | 0.5-2 个 optical link 等效，低端企业 inference 更低，大规模 training/scale-across 更高。 |
| 每 MW | 500-720 GPU 口径下，可能需要 500-2,000 个 800G/1.6T 光口等效。若 800G module ASP 600-1,500 美元、1.6T early ASP 1,500-3,500 美元，光模块链条价值约 100 万-700 万美元/MW；Cisco/Acacia 只捕获其中自有 optics/DSP/相干部分。 |
| 每 optical port BOM | 800G retimed module：DSP/retimer 20%-30%，光引擎/laser/modulator/PD 30%-40%，driver/TIA 10%-15%，PCB/thermal/connector 10%-15%，assembly/test 10%-20%。1.6T：光源/调制/PD 35%-45%，DSP/electrical 20%-30%，driver/TIA 10%-15%，thermal/test 15%-25%。 |
| 供需紧张 | 800G 已成熟但需求仍强，1.6T 从 qualification 进入 scale delivery，行业瓶颈在 224G SerDes、laser、DSP、SiPh/EML、test/burn-in 和良率。 |
| 当前产能能力，美元计 | Cisco 未披露 Acacia/optics 独立产能；以订单和产品发布推断，当前可承接年化 10 亿美元以上 AI/DC optics 相关业务，但完整 1.6T/CPO 产能仍取决于外部光器件和代工。 |
| 认证 | 800G/ZR/ZR+ 属成熟到批量；1.6T OSFP 处于 2026 出货/客户验证窗口；CPO/3.2T engine 更偏 2026-2027 pilot 和长期 qualification。 |

### 6.3 Nexus One / telemetry / Splunk / AgenticOps

| 维度 | 内容量与价值链 |
|---|---|
| 每 rack / 每 GPU | 软件不按物理 BOM 消耗，但 AI 后端网络软件、telemetry、可观测性和支持可占 switch/fabric 合同价值的 10%-18%；超大集群、合规和 sovereign 场景可超过 20%。 |
| 每 MW | 若网络硬件+光学为 300 万-1,500 万美元/MW，软件/支持/telemetry attach 可约 30 万-300 万美元/MW，取决于 Splunk ingest、retention、Nexus One、ThousandEyes 和服务年限。 |
| 价格传导 | Switch/NOS license -> Nexus Dashboard/Nexus One -> Splunk ingest/observability/security analytics -> professional services/managed service。 |
| 产能能力 | 软件不受制造产能限制，限制在客户集成、数据治理、日志成本、运维流程迁移和安全认证。 |
| 认证 | 关键不是硬件认证，而是与客户 GPU scheduler、Kubernetes/Slurm、NVIDIA/AMD telemetry、SIEM/SOC、sovereign data locality 的集成认证。 |

### 6.4 Secure AI Factory / AI POD / UCS

| 维度 | 内容量与价值链 |
|---|---|
| 每 rack | Cisco 可拿 UCS server、Intersight、Nexus/N9100/N9000、security、observability、services；GPU、HBM、NVLink 价值主要归 NVIDIA/AMD 和服务器供应链。 |
| 每 GPU | 排除 GPU 本体后，Cisco 系统/网络/管理/安全内容量可约 1,000-8,000 美元/GPU；企业小集群因服务和安全 attach 更高。 |
| 每 MW | 企业/sovereign AI factory 若由 Cisco 作为集成架构核心，Cisco 可捕获 200 万-1,500 万美元/MW，差异由是否包含 UCS、交换机、光模块、软件和多年服务决定。 |
| 采纳 | Cisco Secure AI Factory with NVIDIA 支持 Cisco Silicon One 或 NVIDIA Spectrum-X switch silicon；N9100/Spectrum-X 路线有助于进入 NVIDIA reference architecture 项目。 |
| 风险 | 企业 AI 工厂采购周期长，GPU 配额、电力、数据准备和应用 ROI 会拖慢硬件确认；系统集成利润率可能低于软件。 |

## 7. 未来一年产能、采纳和认证三情景

| 产品/业务 | 基准 | 乐观 | 极度乐观 |
|---|---|---|---|
| AI Ethernet switching | 年化可交付收入 40-50 亿美元；G300/P200 多客户 pilot/production；UEC/客户互通验证推进 | 年化 60-70 亿美元；1.6T N9000/8000 进入多个 neocloud/sovereign production；Cisco 成为 hyperscaler 第二供应商 | 年化 80-100 亿美元；G300 102.4T 成为 2027 AI Ethernet 主力之一，客户提前锁单，供给紧张 |
| AI optics / Acacia | 年化 14-20 亿美元；800G 稳定，1.6T 开始批量；CPO 仍 pilot | 年化 22-32 亿美元；1.6T OSFP、800G LPO 和相干 DCI 被更多客户采用 | 年化 40 亿美元以上；3.2T/CPO/scale-across coherent optics 超预期，被关键客户纳入标准架构 |
| Nexus One / telemetry / Splunk | 软件 attach 稳步提升；native Splunk integration 落地，更多客户试用 job-aware observability | AI job observability 成为大集群验收项，attach rate 从低双位数提升到中高双位数 | Cisco/Splunk 成为 AI 工厂运维安全数据平面，软件收入增速显著高于硬件 |
| Secure AI Factory / UCS | 企业 AI POD 按区域复制，NVIDIA Enterprise RA/NCP 项目逐步形成 | neocloud/enterprise/edge inference 快速复制，Cisco 渠道优势体现 | Cisco 在 enterprise AI factory 中成为默认架构商，安全/可观测性强绑定 |
| AI Security / Splunk | AI Defense 作为 attach，Security 恢复低个位数增长 | AI governance、agent security、DPU firewall 明显带动新单 | Splunk+AI Defense+Hybrid Mesh Firewall 成为 AI workload 安全标配，Security 重回双位数增长 |

## 8. 基于真实订单积压和供给的未来一年增速推断

### 8.1 官方可验证订单线索

- FY25 AI infrastructure orders 超过 20 亿美元。
- Q1 FY26 hyperscaler AI infrastructure orders 13 亿美元。
- Q2 FY26 hyperscaler AI infrastructure orders 21 亿美元。
- FY26 上半年 AI infrastructure orders 已超过 30 亿美元。
- Q2 FY26 total product orders +18%；Networking product orders >+20%；Service Provider & Cloud orders +65%，其中 hyperscaler orders 三位数增长。
- Q2 FY26 RPO 434 亿美元，Product RPO +8%，长期 Product RPO 118 亿美元 +11%。
- Q2 FY26 经营现金流下降部分来自“为整体需求和 AI infrastructure 需求做投入”，说明公司正在为交付锁供应链。

### 8.2 订单到收入的模型

| 情景 | AI 网络订单假设 | 供给假设 | 未来一年 AI infra 收入增速 | 对 Cisco 总收入影响 |
|---|---|---|---:|---|
| 基准 | FY26 H2 AI orders 维持强但低于 Q2 峰值，全年 orders 55-70 亿美元 | 800G 供应可控，1.6T/G300 爬坡，内存价格压毛利 | +35%-55% | FY27 总收入 +5%-8%，Networking 高个位数到低双位数 |
| 乐观 | FY26 H2 继续拿 hyperscaler/neocloud/sovereign 新单，全年 orders 75-95 亿美元 | 1.6T optics 和 G300 认证顺利，Cisco 锁住关键组件 | +70%-100% | FY27 总收入 +8%-11%，gross margin 短期承压但 operating leverage 维持 |
| 极度乐观 | Q2 订单节奏延续且出现多客户 multi-year awards，全年 orders 100 亿美元以上 | 供应链优先级提升，客户接受涨价和多年承诺 | +130%-180% | FY27 总收入 +12%-15%，Cisco 估值从成熟网络股向 AI infra 平台重估 |

### 8.3 取消率和供给约束

Cisco 不披露 AI backlog、book-to-bill、lead time 和取消率。当前推断取消率偏低，依据是 product orders、RPO 和 deferred revenue 同时上行，且需求来自 hyperscaler、neocloud、sovereign、enterprise、campus refresh 多来源。真正的风险更像“交付滑期”而不是“订单取消”：

- 电力、液冷、园区审批和 GPU 到货时间可能推迟 AI cluster acceptance。
- 内存涨价和高速光模块供应会压 product gross margin，Q3 non-GAAP GM 指引已明显反映压力。
- 若客户选择 NVIDIA Spectrum-X 全栈、Broadcom whitebox/SONiC 或 Arista EOS，Cisco 订单份额可能被挤压。
- 新 1.6T/G300/CPO 从 beta 到量产需要客户资格认证，若良率或稳定性慢于预期，收入确认会后移。

## 9. 竞争格局、主流技术判断、风险和替代方案

### 9.1 主要竞争对手

| 领域 | 竞争对手 | Cisco 相对位置 |
|---|---|---|
| AI Ethernet 系统 | Arista、NVIDIA、Celestica/ODM、HPE/Juniper、Nokia、Dell | Cisco 正在加速出货，产品强，但 2025 AI 后端份额并非第一；需要靠 G300/P200/Nexus/安全全栈抢份额 |
| Switch ASIC | Broadcom Tomahawk/Jericho、NVIDIA Spectrum、Marvell、客户自研 | Silicon One 是差异化资产，统一 routing/switching 架构强；但 Broadcom 白盒生态和 NVIDIA NIC/DPU 绑定非常强 |
| 光模块/光互联 | Coherent、Lumentum、Innolight、Eoptolink、Marvell/Broadcom DSP、Ciena/Nokia、Fabrinet/AOI | Acacia 在相干光学和 coherent pluggables 强，Cisco 不是通用光模块出货量第一，但在系统捆绑和 DCI 有优势 |
| Fabric software | Arista EOS/CloudVision、NVIDIA Cumulus/DOCA/UFM/NMX、SONiC/FBOSS、Juniper Apstra | Cisco 企业 installed base 强，Nexus One/Splunk integration 是亮点；hyperscaler 自研软件会压缩溢价 |
| Security/observability | Palo Alto、CrowdStrike、Zscaler、Fortinet、Microsoft、Cloudflare、Wiz、Datadog、Dynatrace、Elastic | Splunk 数据平台粘性高但成本高；Security 最新季度下滑，必须证明 AI Defense/Hypershield 可以带新增长 |
| Enterprise AI systems | Dell、HPE、Lenovo、Supermicro、NVIDIA DGX Cloud partners、云服务商 | Cisco 强在网络+安全+渠道，不强在 GPU server 成本和供应链规模 |

### 9.2 Cisco 新技术是否可能成为主流

更可能成为主流的部分：

- 800G Ethernet/RoCE + 51.2T/102.4T switch ASIC + 1.6T optics 是 2026-2027 AI 后端网络主线；Cisco G300/P200 正踩在主线上。
- UEC 1.0、Ethernet scale-out/scale-up/scale-across 的开放标准趋势有利于 Cisco，削弱 InfiniBand 和单一 vendor lock-in。
- Nexus One + job-aware telemetry + Splunk integration 符合 AI 工厂从“搭得起来”走向“跑得稳、可审计、可优化”的需求。
- Acacia/coherent/ZR/ZR+ 在跨数据中心、scale-across 和 DCI 中有长期价值。

不确定或有替代风险的部分：

- NVIDIA Spectrum-X/Spectrum-6 可能成为 GPU 集群事实标准，Cisco 即使卖 N9100，也可能让出 switch silicon 价值。
- Broadcom+whitebox+SONiC 对 hyperscaler 成本优势巨大，Cisco 必须证明性能、功耗、buffer、telemetry 和交付可靠性能抵消溢价。
- CPO 何时从 pilot 到主流仍不确定，pluggable 800G/1.6T 可能持续更久。
- AI security 预算会增长，但买方可能优先选择 Palo Alto、CrowdStrike、Microsoft、Zscaler 或云原生方案，而不是 Cisco 全家桶。

### 9.3 客户替换成本

| 客户类型 | 替换成本 | 原因 |
|---|---:|---|
| Hyperscaler 自研网络团队 | 中等 | 他们能用白盒/SONiC/自研控制平面，硬件供应商可替换；但一旦通过 large cluster qualification，替换会影响稳定性和交付窗口 |
| Neocloud/sovereign cloud | 中高 | 团队规模较小，更依赖 Cisco/Arista/NVIDIA 的 reference architecture、支持和可观测性 |
| 企业 AI 数据中心 | 高 | Cisco installed base、渠道、服务、安全策略、Nexus/ACI/NX-OS 运维经验带来粘性 |
| Splunk/SIEM/SOC 客户 | 高但有价格压力 | 数据模型、告警、SOC 流程和合规报表迁移成本高；但 Splunk 成本高，Datadog/Elastic/Microsoft 等替代会持续施压 |

## 10. 投资判断框架

### Bull case

- AI infrastructure orders 从 FY25 >20 亿美元到 FY26 H1 >30 亿美元，说明 Cisco 已进入主流 AI 网络采购。
- G300 102.4T、1.6T OSFP、800G LPO、Nexus One/AgenticOps 正好对应 2026-2027 AI 网络升级周期。
- Ethernet 在 AI scale-out 中已经超过 InfiniBand，并向 scale-up/scale-across 延伸，Cisco 的开放以太网路线受益。
- Splunk + Nexus + AI Defense 如果形成 AI 工厂控制/安全/观测平台，软件估值倍数可高于硬件。
- Campus refresh 也在启动，意味着 AI 之外传统 Networking 不再拖累。

### Bear case

- 估值已经反映不少 AI 乐观预期，forward non-GAAP P/E 约 23x，P/S 约 6.5x，不是传统 Cisco 的便宜估值。
- Q3 GM 指引下滑，内存涨价、hyperscaler mix、光模块成本可能压低产品毛利。
- Arista、NVIDIA、Broadcom 白盒生态和 HPE/Juniper 都在抢同一个 AI Ethernet 池子。
- Security -4%、Observability 持平，Splunk 整合尚未证明能带来持续高增长。
- 大型 AI 数据中心受电力、冷却、园区审批和 GPU 交付约束，Cisco 订单转收入可能后移。

### 关键跟踪指标

1. 2026-05-13 Q3 FY26 财报中 AI infrastructure orders 是否继续超过 15-20 亿美元。
2. Product RPO 和 long-term Product RPO 是否继续增长。
3. Networking 收入是否维持 15%-20%+ 增长，还是 Q2 高点后回落。
4. Q3/Q4 non-GAAP gross margin 是否稳定在 65% 以上，以及涨价能否抵消内存成本。
5. G300/N9000/8000/1.6T optics 是否出现 production customer 而不仅是 beta/生态 quote。
6. Security 和 Observability 是否从 Splunk 并表扰动中恢复到正增长。
7. Cisco 是否披露更多 neocloud、sovereign cloud、enterprise AI pipeline 金额和转化率。

## 11. 信息来源

- Cisco Q2 FY2026 earnings release, 2026-02-11: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m02/cisco-reports-second-quarter-earnings.html
- Cisco Q2 FY2026 prepared remarks: https://s21.q4cdn.com/812015656/files/doc_events/2026/02/Q2FY26-Prepared-Remarks-1.pdf
- Cisco Q1 FY2026 earnings release: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2025/m11/cisco-reports-first-quarter-earnings.html
- Cisco Q4 FY2025 and FY2025 earnings release: https://investor.cisco.com/news/news-details/2025/CISCO-REPORTS-FOURTH-QUARTER-AND-FISCAL-YEAR-2025-EARNINGS/
- Cisco Q3 FY2025 earnings release: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2025/m05/cisco-reports-third-quarter-earnings.html
- Cisco Q2 FY2025 earnings release: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2025/m02/cisco-reports-second-quarter-earnings.html
- Cisco Silicon One G300/N9000/8000/1.6T optics announcement, 2026-02-10: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m02/cisco-announces-new-silicon-one-g300.html
- Cisco Secure AI Factory with NVIDIA, 2026-03-16: https://newsroom.cisco.com/content/r/newsroom/en/us/a/y2026/m03/cisco-secure-ai-factory-with-nvidia-GTC-2026.html
- Cisco completes Splunk acquisition, 2024-03-18: https://investor.cisco.com/news/news-details/2024/Cisco-Completes-Acquisition-of-Splunk/
- Dell'Oro AI back-end switch market forecast, 2026-02-04: https://www.prnewswire.com/news-releases/ai-back-end-switch-market-will-push-past-100-billion-by-2030-according-to-delloro-group-302678344.html
- Dell'Oro Ethernet vs InfiniBand AI scale-out market, 2026-03-10: https://www.prnewswire.com/news-releases/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025-according-to-delloro-group-302708949.html
- TrendForce 800G+ optics share forecast, 2026-02-10: https://www.trendforce.com/presscenter/news/20260210-12919.html
- Ultra Ethernet Consortium Specification 1.0 release, 2025-06-11: https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/
- 项目内非“公司调研”行业资料：AI Ethernet/Fabric switch、AI 数据中心建设规模与订单映射、800G/1.6T 光模块、AI Fabric 网络操作系统与遥测软件、AI 头部芯片市场占比和规模等。
