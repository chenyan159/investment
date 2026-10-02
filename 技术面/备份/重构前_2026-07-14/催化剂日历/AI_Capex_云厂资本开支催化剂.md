# AI Capex / 云厂资本开支催化剂

研究日期：2026-05-15（美西时间）  
适用范围：MSFT、GOOGL、META、AMZN、ORCL、CoreWeave，以及 AI server、networking、HBM、先进封装、电力和冷却链条。  
重要声明：本文为产业研究和催化剂跟踪，不构成投资建议。

## 一页结论

云厂 AI capex 在 2026 年仍处于上修周期，但市场已经从“谁宣布更大预算”转向“预算能否变成可交付 capacity、RPO/backlog 能否变成收入、token 成本下降能否支撑 ROI”的第二阶段。当前最重要的结论有三点：

1. 预算强度仍然很高。MSFT 给出 calendar 2026 约 1900 亿美元级别 capex 线索，AMZN/AWS 约 2000 亿美元级别，GOOGL 2026 约 1800-1900 亿美元且 2027 仍显著更高，META 2026 capex 指引 1250-1450 亿美元，ORCL FY26 capex 约 500 亿美元且 RPO 已到 5530 亿美元，CoreWeave FY26 capex 指引 310-350 亿美元。它们合计已经足以支撑 AI server、GPU/ASIC、HBM、CoWoS、光互联、交换芯片、电力接入和液冷链条的多季度需求能见度。
2. 约束条件从单一 GPU 变成系统级瓶颈。2026 年的供给瓶颈同时出现在 HBM3E/HBM4、CoWoS/SoIC/先进基板、800G/1.6T 光模块、以太网/InfiniBand fabric、电力接入、变压器、开关柜、机电工程、液冷 CDU/冷板/快接头。NVIDIA 仍是 AI 加速卡和整机价值量核心，但受益面正在扩散到 TSM、AVGO、MRVL、MU、COHR、VRT、ETN、PWR、GEV 等“卖铲子”环节。
3. 最大风险不是“云厂不想买”，而是“买太多以后 ROI 兑现慢于折旧、租赁和电力成本”。如果 AI 收入、RPO 消化、推理负载和企业应用 adoption 无法跟上 capex 折旧，云厂会先调整订单节奏、机柜上电节奏和自研 ASIC 替代率，而不是立刻取消全部建设。因此后续跟踪重点应放在 RPO 转收入、AI ARR、推理使用量、GPU/ASIC 利用率、单位 token 成本、power available、液冷部署和供应商 backlog 质量。

当前基准判断：未来 6-12 个月 AI capex 仍偏正面，受益公司从 GPU 主线扩展为“算力芯片 + 存储 + 先进封装 + 网络 + 电力冷却”的组合；但 2026 年下半年开始，估值和订单反应会更依赖 ROI 证据，而不是单纯 capex headline。

## 云厂 capex 催化剂矩阵

| 云厂 | 2026 capex / 需求线索 | AI 需求证据 | 自研 ASIC / 关键架构 | 主要受益链条 | 需要警惕的负面触发 |
|---|---:|---|---|---|---|
| MSFT | FY26 Q3 capex 319 亿美元；Q4 capex 指引高于 400 亿美元；calendar 2026 约 1900 亿美元级别；组件价格上涨约 250 亿美元 | Microsoft Cloud 545 亿美元，同比增长 29%；Azure +40%；AI ARR 超 370 亿美元，同比增长 123%；Commercial RPO 6270 亿美元，同比增长 99% | Maia 200、Cobalt、Azure AI 集群；仍大量依赖 NVIDIA GPU 与外部模型合作 | NVDA、TSM、AVGO/MRVL、MU、COHR、ANET、VRT、ETN、PWR、GEV；OpenAI/Anthropic 订单也推高 AWS 与 Azure 互相竞赛 | OpenAI/Anthropic 大单集中度；Copilot 和企业 AI 付费 ROI 若低于预期；GPU/CPU/存储/电力 capacity 继续短缺导致收入递延 |
| GOOGL | 2026 capex 约 1800-1900 亿美元；2027 继续显著高于 2026；采购承诺约 3324 亿美元，其中短期约 1380 亿美元 | Google Cloud Q1 revenue 200.3 亿美元，同比增长 63.4%；Cloud operating margin 32.9%；Cloud backlog 4623 亿美元，超过 50% 预计 24 个月内确认 | TPU v7/v8、AI Hypercomputer、OCS 光交换；Intersect 收购强化能源和数据中心资源 | AVGO、TSM、HBM 供应商、光模块、交换/光交换、电力接入和冷却；同时减少对通用 GPU 的部分边际依赖 | 搜索 AI monetization 被挤压；TPU 交付或客户采用不及预期；capex 继续上修导致 FCF 压力 |
| META | 2026 capex 指引 1250-1450 亿美元，较前值上修 100 亿美元；非可撤销承诺 2377 亿美元，未开始租赁义务 1829 亿美元；4 月新增约 240 亿美元基础设施承诺 | Q1 ad revenue 550 亿美元，同比增长 33%；impressions +19%，price +12%；FoA margin 48.1%；收入仍能覆盖 AI 投入 | MTIA 300/400/450/500；Broadcom 参与，自研 ASIC 初始超过 1GW 并走向 multi-GW；CoreWeave 210 亿美元承诺 | AVGO、TSM、HBM、先进封装、网络、液冷、电力；CoreWeave 和 GPU 云 | 直接 AI monetization 仍不清晰；广告周期下行时 capex 对 FCF 压力放大；租赁和容量承诺刚性上升 |
| AMZN / AWS | 2026 capex 约 2000 亿美元级别；AWS 相关估算可超过 2300 亿美元；2025 已新增 3.9GW 电力，目标 2027 power capacity 翻倍 | AWS Q1 revenue 376 亿美元，同比增长 28%；operating income 142 亿美元，margin 37.7%；RPO 3640 亿美元；AI run-rate 超 150 亿美元，芯片 run-rate 超 200 亿美元 | Trainium2/3/4、Inferentia；Project Rainier 接近 50 万颗 Trainium2；OpenAI/Anthropic 大额长期承诺，Anthropic up to 5GW，OpenAI 约 2GW Trainium 线索 | AVGO/MRVL 定制芯片生态、TSM、HBM、NVDA 作为并行需求、电力接入、液冷、机电工程 | Trainium 软件生态和开发者迁移慢；大客户长约导致单一项目风险；capex 与 FCF 错配；电力/土地/许可进度慢 |
| ORCL | FY26 capex 约 500 亿美元；Q3 FY26 RPO 5530 亿美元，同比增长 325%；未来 3 年 secured power 10GW | OCI IaaS revenue 49 亿美元，同比增长 84%；AI infrastructure revenue +243%；FY27 revenue guide 900 亿美元 | GPU-neutral OCI Supercluster，NVIDIA/AMD/客户自带 GPU 并行；更像高杠杆 AI capacity aggregator | NVDA、AMD、网络、存储、电力、数据中心租赁和工程；大型 AI 客户订单映射到供应商 | 资产负债表压力大，借款约 1346 亿美元；off-balance lease commitments 约 2480 亿美元；大客户融资或项目延迟会放大波动 |
| CoreWeave | FY26 capex 310-350 亿美元；active power 超 1GW，contracted power 超 3.5GW，2030 目标超 8GW | Q1 revenue 20.78 亿美元，同比增长 112%；backlog 994 亿美元；Q1 新承诺超 400 亿美元，含 META 210 亿美元；2026 capacity 基本售罄 | 主要是 GPU 云和 AI factory 交付商，短期受益 NVIDIA GPU 稀缺；未来需面对 ASIC 替代和 GPU 租价周期 | NVDA、VRT、ETN、PWR、GEV、COHR/网络、数据中心 REIT/租赁、融资链条 | 负债和利息费用压力；客户集中；GPU 租价下行；active power 交付慢；云厂自建或 ASIC 替代 |

## Capex 传导链：从预算到股票受益

云厂 capex 并不会平均分配。更值得跟踪的是每一美元 capex 流向哪类瓶颈，以及这些瓶颈是否具备定价权、交付约束和订单可见度。

| 环节 | 需求驱动 | 2026 年关键指标 | 主要受益公司 | 催化剂强度 | 关键风险 |
|---|---|---|---|---|---|
| AI server / GPU 整机 | GB200/GB300、B300、HGX/DGX、NVL72 机柜部署；云厂训练和推理集群扩张 | NVDA 数据中心收入、networking 收入、GB300 机柜出货、云厂 capex 上修 | NVDA、SMCI、DELL、HPE、台系 ODM | 高 | 单柜功耗 130kW+ 带来上电和液冷约束；客户集中；China restriction |
| 自研 ASIC | 云厂希望降低单位 token 成本、掌握推理成本曲线、避免完全依赖 GPU | TPU、Trainium、MTIA、Maia、OpenAI ASIC、Anthropic TPU/GPU 混合订单 | AVGO、MRVL、TSM、ARM、EDA、HBM、先进封装 | 高 | 设计周期 18-36 个月；软件生态迁移慢；先进封装和 HBM 仍卡脖子 |
| HBM | GPU/ASIC 的 memory bandwidth 是训练和推理吞吐核心约束 | HBM3E 12Hi、HBM4 认证、HBM 合约价格、DRAM wafer allocation | MU、SK hynix、Samsung；设备和材料链 | 高 | 2027-2028 供给过剩风险；客户认证失败；CoWoS 和测试产能不匹配 |
| 先进封装 | GPU/ASIC + HBM 需要 CoWoS、SoIC、interposer、ABF substrate、test | TSM CoWoS/3DFabric capex、先进封装交期、HBM base die 和 interposer 供应 | TSM、ASML、AMAT、LRCX、KLAC、ABF/测试链 | 高 | 良率和扩产节奏；客户产品切换导致短期 digestion |
| AI networking | 多 GPU、多机柜、多数据中心训练需要高带宽低延迟网络 | 800G/1.6T 光模块、DSP、CPO/OCS、以太网交换 ASIC、InfiniBand/Ethernet 份额 | ANET、AVGO、MRVL、COHR、LITE、FN、CIEN | 中高 | 价格下降快；云厂自研或白盒化；1.6T 转换期库存错配 |
| 电力接入和高压变电 | AI 园区从 MW 进入 GW 级，电力成为真正稀缺资源 | signed power、interconnect queue、变压器/开关柜 lead time、utility capex | ETN、VRT、GEV、PWR、POWL、HUBB、FIX | 高 | 许可、并网、燃气轮机交期、劳动力和项目执行风险 |
| 液冷和热管理 | GB200/GB300、Rubin 等高密度机柜需要直液冷和 warm-water 方案 | CDU、cold plate、manifold、quick disconnect、leak detection 订单 | VRT、ETN、NVDA reference design 生态、NVT、ITRI/台系链 | 中高 | 部署标准未完全统一；漏液/维护风险；数据中心改造节奏慢 |

## 关键指标仪表盘

| 指标 | 当前读数 / 线索 | 解释 | 跟踪频率 |
|---|---:|---|---|
| MSFT AI ARR | 超 370 亿美元，同比增长 123% | AI capex 是否能转化为商业化收入的最直接指标之一 | 财报季 |
| MSFT Commercial RPO | 6270 亿美元，同比增长 99%；约 25% 在 12 个月内确认 | backlog 对 Azure/AI revenue 的支撑 | 财报季 |
| GOOGL Cloud backlog | 4623 亿美元，超过 50% 预计 24 个月内确认 | TPU/Cloud capex 的收入能见度 | 财报季 |
| META capex 指引 | 2026 年 1250-1450 亿美元 | 广告现金流支持 AI 基建的能力 | 财报季与指引更新 |
| AWS RPO | 3640 亿美元，平均寿命 5.5 年 | 长约支撑 AI factory 和 Trainium 需求 | 财报季 |
| ORCL RPO | 5530 亿美元，同比增长 325% | OCI AI 基建订单强，但融资和交付风险也高 | 财报季 |
| CoreWeave backlog | 994 亿美元；contracted power 超 3.5GW | GPU 云需求和电力资源锁定程度 | 财报季 |
| HBM 价格和合约 | HBM3E 12Hi 为主，HBM4 开始认证和量产准备 | HBM 是 GPU/ASIC 出货上限之一 | 月度/财报季 |
| CoWoS / 先进封装产能 | TSM 2026 capex 520-560 亿美元，AI/HPC 相关需求强 | 先进封装决定 GPU/ASIC 实际可交付量 | 月度/季报 |
| 800G/1.6T 光模块订单 | AI 数据中心 book-to-bill 高，COHR 数据中心 book-to-bill 曾超过 4x | 网络从配套变成瓶颈 | 月度/季报 |
| 电力接入订单 | 数据中心电力接入 1 年新订单基准 380-550 亿美元；关键设备 lead time 18-36 个月 | 电力链条订单能见度通常长于服务器 | 月度/季报 |
| 市场风险背景 | 2026-05-15：SOXX 当日 -4.06%，SMH -3.80%，VIX 18.43，10Y 4.47% | AI capex 主题短期会受利率和半导体拥挤交易影响 | 日频 |

## 正面催化剂

| 时间窗口 | 正面触发 | 观察信号 | 受益方向 |
|---|---|---|---|
| 1-3 个月 | 云厂继续上修 capex 或给出 2027 更高展望 | MSFT/GOOGL/AMZN/META capex 指引、RPO、AI revenue、power capacity 更新 | NVDA、TSM、AVGO、MU、VRT、ETN、PWR、GEV、COHR |
| 1-3 个月 | GB300/NVL72 和高密度机柜交付顺利 | NVDA 数据中心和 networking revenue、液冷方案验证、客户部署节奏 | NVDA、VRT、ETN、COHR、ANET、MRVL |
| 3-6 个月 | HBM4 / HBM3E 12Hi 认证和价格维持强势 | MU/SK hynix/Samsung HBM 合约、毛利率、产能 allocation | MU、存储设备材料链、TSM 先进封装 |
| 3-6 个月 | 自研 ASIC 进入 multi-GW 订单兑现 | Google TPU、AWS Trainium、META MTIA、OpenAI/Broadcom、Anthropic TPU/GPU 混合订单 | AVGO、MRVL、TSM、HBM、封装、EDA |
| 3-12 个月 | 电力和液冷订单持续加速 | ETN/VRT/GEV/PWR backlog、book-to-bill、lead time、数据中心项目 win | ETN、VRT、GEV、PWR、POWL、HUBB、FIX |
| 6-12 个月 | AI 应用收入兑现，证明 ROI | Copilot seat expansion、AI ARR、AWS Bedrock/Trainium 使用量、Google Cloud AI 客户、META ad AI ROI | 云厂本身和整条 capex 链条 |

## 负面触发和风险

| 风险 | 触发信号 | 影响路径 | 最敏感环节 |
|---|---|---|---|
| AI ROI 不达预期 | AI ARR 增速放缓、企业 Copilot/agent adoption 不及预期、推理收入不足以覆盖折旧 | 云厂不会立刻停建，但会调整订单节奏和自建/租赁比例 | GPU、服务器 ODM、CoreWeave、租赁链 |
| RPO 质量被质疑 | RPO 增长但收入确认慢；合同集中在少数客户；项目延期或融资条件改变 | backlog 打折，估值从订单逻辑转向现金流逻辑 | ORCL、CoreWeave、部分电力/工程链 |
| 自研 ASIC 替代 GPU 加速 | TPU/Trainium/MTIA 单位成本和软件栈明显改善 | 通用 GPU 边际份额受压，但 HBM/TSM/封装/网络仍受益 | NVDA 高估值弹性，GPU 云租价 |
| 供应链扩产后过剩 | HBM/CoWoS/光模块价格松动，lead time 缩短过快 | 从“量价齐升”变成“量升价跌” | MU、光模块、封装设备 |
| 电力和许可拖延 | signed power 无法转 active power；变压器和燃机交付延迟；并网审批慢 | 服务器已采购但不能上电，收入确认递延 | CoreWeave、ORCL、VRT/ETN/PWR 项目节奏 |
| 宏观和利率压力 | 10Y 继续上行、VIX 抬升、SOXX/SMH 继续回撤，广度恶化 | 高估值长久期 AI 资产被压缩 | NVDA、AVGO、MU、VRT、CRWV 等高弹性标的 |
| 政策和出口限制 | 中国相关 AI 芯片限制升级，H20/替代品出货受压 | 区域收入下修，供应链重配 | NVDA、部分半导体设备和存储链 |

## AI ROI 风险框架

AI capex 的 ROI 不能只看 capex headline，应拆成四个桥：

| ROI 桥 | 要问的问题 | 关键数据 | 结论倾向 |
|---|---|---|---|
| 需求桥 | 企业和开发者是否真的把 AI 用量跑起来？ | AI ARR、Bedrock/Vertex/Azure AI 使用量、推理 token、agent 工作流渗透率 | 目前偏正面，但需要持续验证 |
| 成本桥 | 单位 token 成本是否随 GPU/ASIC/HBM/网络迭代下降？ | GPU/ASIC 性价比、HBM 带宽成本、集群利用率、电力成本 | 自研 ASIC 是降本核心，利好 AVGO/MRVL/TSM/HBM |
| 转收入桥 | backlog/RPO 是否按期变收入？ | RPO current portion、Cloud revenue、OCI/AWS/Azure/Google Cloud growth | MSFT/GOOGL/AMZN 较强，ORCL/CoreWeave 更需看交付 |
| 资产效率桥 | 折旧、租赁、利息和电力成本是否吞噬现金流？ | capex/revenue、FCF margin、lease commitments、interest expense、active power | ORCL/CoreWeave 风险最高，META 和云厂需看广告/云利润覆盖 |

### 公司维度 ROI 读法

| 公司 | ROI 支撑 | ROI 压力 | 关键判断 |
|---|---|---|---|
| MSFT | AI ARR、RPO、Azure 增长强；企业分发能力强 | OpenAI/Anthropic 集中度、Copilot ROI 争议 | 若 AI ARR 继续高增长，capex 可被市场接受 |
| GOOGL | Cloud backlog、TPU 成本优势、搜索现金流 | 搜索 AI 答案侵蚀广告、capex 对 FCF 压力 | TPU 若外部化成功，ROI 叙事增强 |
| META | 广告 AI 已经改善转化率和价格；现金流强 | GenAI/Reality Labs 直接收入不清晰，承诺和租赁刚性 | 广告主线能否继续支付 AI 基建账单是核心 |
| AMZN | AWS margin 高、RPO 强、Trainium 降本 | Trainium 生态和软件兼容性、长约项目交付 | 若 Trainium 大客户使用稳定，AWS ROI 改善明显 |
| ORCL | RPO 爆发，OCI AI infra 高增长 | 杠杆和租赁承诺高，大客户集中 | 高弹性但更像融资和交付考验 |
| CoreWeave | backlog 和 power 资源稀缺，GPU 云需求强 | 利息费用、客户集中、GPU 租价周期、ASIC 替代 | 需盯 active power 转 revenue 和融资成本 |

## 情景分析

| 情景 | 概率判断 | 触发条件 | 产业影响 | 股票映射 |
|---|---|---|---|---|
| 基准：capex 高位延续，瓶颈扩散 | 较高 | 云厂 capex 稳中上修；RPO 继续转收入；HBM/CoWoS/电力短缺延续 | GPU 与 ASIC 共存，供应链订单能见度维持到 2027 | NVDA、TSM、AVGO、MU、VRT、ETN、PWR、GEV、COHR 受益；云厂估值取决于 ROI |
| 牛市：AI revenue 兑现快于折旧 | 中 | AI ARR/Cloud AI 收入加速；企业 agent 和推理使用爆发；单位 token 成本快速下降 | capex 被视为高 ROIC 投资，2027 指引继续上修 | 云厂和卖铲子双重扩张，GPU/ASIC/HBM/电力冷却全面受益 |
| 熊市：ROI 质疑 + 宏观压估值 | 中 | AI 收入放缓；SOXX/SMH 继续回撤；10Y 上行；云厂 FCF 被 capex/lease 压缩 | 订单不一定消失，但估值从 growth 切到 cash discipline | 高估值半导体、GPU 云和高杠杆基建最脆弱；电力链相对有 backlog 缓冲 |
| 结构性轮动：GPU 弹性降，自研 ASIC 和电力链占优 | 中高 | TPU/Trainium/MTIA 多 GW 订单兑现；GPU 租价回落；power/cooling 继续卡 | AI capex 从单一 GPU 主题转向系统级 capex | AVGO、MRVL、TSM、MU、VRT、ETN、PWR、GEV 相对占优 |

## 后续跟踪清单

| 跟踪项 | 为什么重要 | 具体看什么 | 可能的结论变化 |
|---|---|---|---|
| 云厂最新财报 capex 指引 | 决定 AI capex 总量是否继续上修 | MSFT、GOOGL、META、AMZN、ORCL 的 capex、purchase commitments、lease commitments | 上修继续利好供应链；若 capex 增速低于预期，GPU/服务器先承压 |
| RPO/backlog 到 revenue 的转化 | 验证订单不是纸面繁荣 | Azure/AWS/GCP/OCI revenue、CoreWeave revenue、RPO current portion | 转化顺畅则 ROI 质疑下降；延迟则风险上升 |
| AI 收入和使用量 | 验证需求真实 | AI ARR、Bedrock/Vertex/Azure AI、推理 token、企业 seat expansion | 若收入和用量跟不上，capex 可能进入 digestion |
| 自研 ASIC 进展 | 决定 GPU 与 ASIC 利益再分配 | TPU、Trainium、MTIA、Maia、OpenAI/Broadcom、Anthropic 订单和部署 | ASIC 超预期利好 AVGO/MRVL/TSM/HBM，压制部分 GPU 租价 |
| HBM 和先进封装 | 决定 GPU/ASIC 实际出货上限 | HBM4 认证、HBM 合约价、TSM CoWoS/SoIC 产能、封装 lead time | 短缺延续利好 MU/TSM；松动则估值重估 |
| 网络和光互联 | 决定大集群效率 | 800G/1.6T、DSP、OCS、Ethernet switching、NVLink/InfiniBand 份额 | 网络 attach rate 上升利好 COHR/AVGO/MRVL/ANET |
| 电力和液冷 | 决定 data center 能不能上电 | active power、contracted power、变压器/开关柜 backlog、CDU/冷板订单 | 上电慢会压收入确认；电力链 backlog 强则防御性更好 |
| 市场技术面 | 决定主题能否承受高估值 | SOXX/SMH、VIX、10Y、breadth、EPS revision | 宏观恶化时优先降低高杠杆和远期估值弹性假设 |

## 当前结论

截至 2026-05-15，美股 AI capex 主线没有结束，但已经从“GPU 供不应求”升级为“AI factory 系统工程供不应求”。MSFT、GOOGL、META、AMZN、ORCL 和 CoreWeave 的 capex、RPO、backlog、power commitments 共同说明，2026 年 AI 基建需求仍处于高景气阶段。最直接的受益者仍是 NVDA 和 TSM，但新增弹性更可能在 AVGO/MRVL 的自研 ASIC、MU 的 HBM、COHR/ANET/光模块和网络、VRT/ETN/PWR/GEV 的电力冷却链条中体现。

不过，AI capex 的交易难度也在上升。市场已经开始要求云厂证明 ROI：AI ARR 和 Cloud revenue 要足够快，RPO 要能按期确认，GPU/ASIC utilization 要足够高，电力和液冷项目要能真正交付。如果后续财报出现 capex 继续上修但收入确认放慢、FCF 下修、租赁和利息成本快速上升的组合，主题会从供应链乐观转为 ROI 审查。基准路径仍偏正面，但研究跟踪重心应从单点 GPU 扩展到 HBM、先进封装、网络、电力和液冷，并持续监控自研 ASIC 对价值分配的改变。

## 主要本地来源

- AI产业和股票研究结果/公司调研/MSFT_微软_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/GOOGL_Alphabet_Inc_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/META_Meta_Platforms_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/AMZN_Amazon_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/ORCL_Oracle_Corporation_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/CRWV_CoreWeave_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/NVDA_NVIDIA_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/TSM_台积电_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/AVGO_Broadcom_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/MRVL_Marvell_Technology_全面尽调_2026-05-09.md
- AI产业和股票研究结果/公司调研/公司_MU_Micron_Technology_美光科技_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/VRT_Vertiv_全面尽调_2026-05-09.md
- AI产业和股票研究结果/公司调研/公司_ETN_Eaton_Corporation_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/PWR_Quanta_Services_全面尽调_2026-05-10.md
- AI产业和股票研究结果/公司调研/GEV_GE_Vernova_全面尽调_2026-05-10.md
- AI产业和股票研究结果/行业调研_AI服务器_存储_芯片/行业调研_云厂自研AI_ASIC_2026.md
- AI产业和股票研究结果/行业调研_AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026.md
- AI产业和股票研究结果/行业调研_AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026.md
- AI产业和股票研究结果/行业调研_AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-05-08.md
- AI产业和股票研究结果/行业调研_AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026.md
- AI产业和股票研究结果/行业调研_AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026.md
- 股票基本面和价格历史研究/data/common_daily/features/common_research_daily_panel_full.csv
- 股票基本面和价格历史研究/研究可靠性检查_技术面_消息面.md
