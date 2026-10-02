# COMPUTEX 2026会议追踪：核心变化、产品爆发和市场预期差

报告完成日期：2026-06-10（America/Los_Angeles）  
材料检索截止：2026-06-10 20:44 PT / 2026-06-11 03:44 UTC  
会议日期：2026-06-02 至 2026-06-05；会前/会中关键演讲自 2026-06-01 开始  
会议地点：Taipei，主要场馆为 TaiNEX 1/2、TWTC Hall 1、TICC；NVIDIA GTC Taipei 同期覆盖 TICC/COMPUTEX 展区  
资料边界：本报告按用户要求独立追踪公开资料，未读取、引用或继承项目内既有研究报告、索引、缓存和中间结论。  

## 结论摘要

- 本届 COMPUTEX 2026 的核心变化不是“AI 还很热”，而是 AI 从 2024-2025 年的模型/算力叙事，落到 4 个可投资硬件层：整柜 AI factory、800VDC/液冷/电源、agentic inference 架构、physical AI/edge robotics。官方会后数据为 111,312 名买家与访客、152 个国家和地区、1,500 家参展商、约 6,000 个展位，说明这已经是供应链型会议而不是单纯 PC 展。
- 最大真实变化：高密 AI 机柜从“GPU 服务器堆叠”进入“电源架构、液冷、网络、部署平台共同决定 token 成本”的阶段。NVIDIA Vera Rubin NVL72 公开配置为 36 颗 Vera CPU、72 颗 Rubin GPU，100% 液冷，45°C 运行，宣称 inference performance per watt 和 cost per token 均提升 10x；ASUS 对应 AI POD TDP 187-227kW；Delta/LITEON 同步展示 800VDC、2.4MW/3MW CDU、90kW/110kW power shelf 等配套。
- 最大可放量方向：2026H2-2027 年的 800VDC、CDU、cold plate、busbar、power shelf、rack integration、deployment simulation。理由是这些环节已经跟 NVIDIA Vera Rubin/GB300/NVL72 一一绑定，客户导入周期短于新 GPU 架构本身，且会随 rack power density 从 100kW 级迈向 180-230kW 级而抬升单位价值量。
- 最大被低估方向：AI data center networking/optics 和 CPU-dense inference。会议里 Marvell 把 AI infrastructure performance 的约束从 compute/memory 推向 connectivity；Intel 则把 Xeon 6+、SambaNova RDU、NVIDIA Blackwell GPU 拆成 prefill/decode/orchestration 的 disaggregated inference。市场若仍只按 GPU 数量看 AI 资本开支，会低估网络、CPU、DPU、power delivery、液冷和部署软件的利润池。
- 最大被高估方向：AI PC 的 2026 年单位爆发。NVIDIA RTX Spark、Qualcomm Snapdragon X2 Elite mini-PC、Snapdragon C 都证明“本地 agent PC”从概念走向产品，但 IDC 2026 年 personal computing device 全年出货预测为 401.9 百万台、同比 -10.4%；Gartner 同期警告 DRAM+SSD 价格到 2026 年底可能上涨 130%、PC ASP 上涨 17%。因此 AI PC 更像 ASP/高端 mix 机会，不是 2026 年 PC unit cycle 的拐点。
- Physical AI 已从演示走向 reference design，但收入节奏要降权处理。Qualcomm Dragonwing IQ10 RRD 已给出 700 TOPS、18 Oryon cores、12 路 GMSL2 camera、LiDAR/ToF/IMU、TSN/EtherCAT/CAN-FD、-40°C 至 70°C 和 2026-09 全球可用的路线；NVIDIA Jetson Thor 宣称 2,070 FP4 TFLOPS、40-130W、相对 Orin 7.5x compute/3.5x energy efficiency。本质是边缘计算模组和开发套件先变现，机器人本体规模化仍要看安全认证、良率、工况和维护成本。
- 未来 3 个月最该跟踪：RTX Spark 秋季机型是否按期上市；Qualcomm Dragonwing IQ10 RRD 2026-09 是否全球供货；Intel OpenVINO Physical AI 预览到 GA 的进度；Delta/ASUS/LITEON 是否把 800VDC/液冷从展品转成订单；NVIDIA GB300/Vera Rubin 相关 ODM 订单和交期。
- 未来 1 年最该跟踪：AI 机柜功率是否普遍越过 100kW 并向 180-230kW 迁移；液冷是否从 hyperscaler 扩散到 colocation/enterprise；AI PC 的高端机型 ASP 能否抵消内存涨价；edge robotics 是否出现 10,000 台级 fleet 部署；Marvell/Broadcom/NVIDIA 网络平台是否绑定 1.6T/3.2T 或 CPO 量产节奏。
- 未来 2 年最可能改变行业结构的是“token 成本的硬件栈重分配”：如果 inference 成为主负载，利润池会从单一 accelerator 向 GPU/HBM、CPU、网络、power/liquid cooling、storage/context memory、deployment platform 分散；但最高利润率仍在专有 silicon/IP，最低但收入弹性大的仍是 ODM rack integration。

## 会议重点和方向变化

### 官方框架：AI Together 从算力竞赛转向系统部署

COMPUTEX 官方给出的 2026 年主题是 “AI Together”，三大主轴为 AI & Computing、Robotics & Mobility、Next-Gen Tech。会前官方材料称本届规模为 1,500 家参展商、33 个国家和地区、6,000 个展位；会后官方材料确认 111,312 名买家与访客来自 152 个国家和地区，keynote 约 6,000 人次，forum 超过 13,200 visits，InnoVEX 超过 500 家 startup，较上年增长 11% 以上。

变化性质：真实变化，来自会议官方一手材料。  
投资含义：COMPUTEX 2026 的信号强度主要来自台湾 ICT 供应链的系统集成能力，而不是单一 keynote 的概念强弱。

### 主题 1：AI factory 进入整柜、液冷、电源和部署平台竞争

代表公司和材料：

| 公司/平台 | 会议材料日期 | 关键参数 | 变化性质 | 读数 |
| --- | --- | --- | --- | --- |
| NVIDIA Vera Rubin NVL72 | 2026-05-21/2026-06-01 前后 | 36 Vera CPU、72 Rubin GPU、NVLink Switch、ConnectX-9、Spectrum-X Ethernet Photonics CPO、BlueField-4；宣称 10x inference performance/W、10x lower cost/token；100% 液冷、45°C | 产品路线/生态真实变化 | AI 机柜 KPI 从 FLOPS 转向 token/W、cost/token、power smoothing、assembly time |
| ASUS AI POD XA VR721-E3 | 2026-03-17；COMPUTEX 延展至 2026-06-02 DSX | Vera Rubin NVL72，100% liquid-cooled，TDP 187kW MaxQ/227kW MaxP，72 Rubin GPUs | 量产前整柜方案 | ODM/品牌服务器厂开始卖“AI factory from blueprint to deployment” |
| Delta COMPUTEX showcase | 2026-06-02 至 06-05 | 800VDC high-voltage DC、2.4MW liquid-to-liquid CDU、25kW HVDC e-pump、3MW GoCool CDU、90kW DC-DC shelf、110kW AC-DC shelf、Vera Rubin cold plate | 已展示具体部件 | 电源/热管理单位价值量随 rack power 增长 |
| LITEON COMPUTEX showcase | 2026-06 | 800VDC、NVIDIA Vera Rubin NVL72 AI factory solutions、power/rack/liquid cooling | 已展示具体方案 | 台湾电源链条从 PSU 扩到 rack power infrastructure |

和过去 6-12 个月相比：2025 年主线仍偏 GB200/Blackwell 供给、HBM 和服务器组装；2026 COMPUTEX 把问题显性转为“如何让 180-230kW 级机柜可部署、可维护、可供电、可冷却”。这对 Delta、LITEON、Vertiv、Schneider、cold plate/CDU/busbar/e-fuse 供应链更有利，对只做普通服务器机箱/低端 PSU 的公司不构成同等弹性。

### 主题 2：Inference 架构开始从 GPU-only 走向 disaggregated prefill/decode/orchestration

Intel 在 2026-06-01/06-02 COMPUTEX 材料里提出 rackscale AI infrastructure：Intel Xeon processors + SambaNova SN-50 RDUs + Foxconn system integration；Vector Core Compute 演示 fully disaggregated inference，用 Intel Xeon 6 负责 orchestration/execution、SambaNova SN40 RDU 负责 decode、NVIDIA Blackwell GPU 负责 prefill，并称 Together.ai 是首个商业客户。Intel 同时给出 Xeon 6+：18A 数据中心 CPU，单个液冷 rack 可在 32U compute space 提供 36,864 cores，约 100kW rack power。

变化性质：真实但仍需客户规模验证。  
投资含义：如果 agentic workload 使 CPU:GPU 比例从训练时代的约 1:4 回到 1:1 或更高 CPU 占比，Intel/AMD server CPU、DPU/NIC、RDU/ASIC、network fabric 的单位价值量会重新抬升。但 Intel 的反证条件很清楚：18A yield、Xeon 6+ 出货、Foxconn/SambaNova rack 是否有 2026H2-2027 订单。

### 主题 3：AI PC 从 Copilot+ 进入本地 agent PC，但 2026 年单位周期仍弱

NVIDIA RTX Spark 是本届最明确的 PC 端新平台：1 PFLOP AI compute、最高 128GB unified memory、20-core Grace CPU、Blackwell RTX GPU 6,144 CUDA cores、FP4、NVLink-C2C；官方称可运行 120B-parameter LLM、最高 1M token context、90GB+ 3D scene、12K 4:2:2 video、4K AI video，机型将于 2026 年秋季由 ASUS、Dell、HP、Lenovo、Microsoft Surface、MSI 推出，Acer/GIGABYTE 后续跟进。

Qualcomm 的 PC 端补位分两层：Snapdragon X2 Elite mini-PC（ASUS Ascent QN10，官方 meta 描述为 80 TOPS local AI、0.7L 设计）面向高性能小型 AI PC；Snapdragon C 面向 $300+ entry-tier laptops，2026 年后续上市。AMD 的 COMPUTEX 2026 重点则更偏平台寿命和游戏 CPU：Ryzen 7 7700X3D 于 2026-07-16 上市，建议价 $329；AM5 支持延长至 2029；Ryzen 7 5800X3D 十周年版延续 AM4；Radeon RX 9070 GRE 扩展 RDNA4。

变化性质：产品真实；市场规模判断必须保守。  
反共识：AI PC 叙事会推升高端 SoC、统一内存、OLED、散热和软件优化价值，但 IDC/Gartner 同时给出 2026 年 PC/PCD 下行和内存成本冲击。2026 年更可能是“AI PC ASP/mix 改善 + unit 下行”的组合，不是全行业 unit 爆发。

### 主题 4：Physical AI/robotics 从“展会机器人”变成 reference design、edge compute 和安全控制栈

COMPUTEX 官方首次设置 AI Robotics Zone；官方会后引用 Strategy&，称 Physical AI 2030 年全球市场价值约 €430B，并预计未来 3-5 年在制造、物流、医疗、航空航天等行业实现大规模商业采用。公司层面：

- NVIDIA Jetson Thor：官方 BCA 材料称 2,070 FP4 TFLOPS、40-130W、相对 Jetson Orin 7.5x compute、3.5x energy efficiency，面向 robots、industrial systems、medical devices、autonomous machines。
- Qualcomm Dragonwing IQ10 RRD：2026-06-01 公布，700 TOPS、18 Oryon CPU cores、多 NPU/GPU、最多 12 路 GMSL2 cameras、LiDAR/ToF/IMU、PCIe/TSN/USB/CAN、Ethernet/EtherCAT/CAN-FD、-40°C 至 70°C、12V/24V 输入、ROS2、Qualcomm AI Hub，2026-09 全球可用；早期伙伴包括 NEURA Robotics、Advantech、APLUX、Booster、Innodisk、MeiG、NEXCOM、Radxa、Thundercomm、VinMotion。
- NXP：COMPUTEX 页面聚焦 “Pioneering Trusted Edge Intelligence”，展示 CoreRide、agentic vehicle orchestration、Auto Wi-Fi Smart Link、16Mbps networking、1500V BESS management、48V BMS in robotic hot swap、i.MX95 AI camera、3D perception sensor fusion、video search/summarization。
- Advantech：以 WEDA 和 edge AI 串联 NVIDIA/Qualcomm 等生态，定位工业 physical AI 部署。

变化性质：reference design 和模组真实；机器人本体收入放量仍待验证。  
投资含义：2026-2027 年先看 edge module、industrial PC、sensor interface、motion control、battery/power management、fleet MLOps，而不是直接把 humanoid robot TAM 全部给机器人本体公司。

### 主题 5：联网、汽车和 6G 还是中期可选性，不是 3 个月收入主线

MediaTek 的 COMPUTEX 2026 材料覆盖 “edge-to-cloud AI”：Dimensity AX C-X1 车载座舱 3nm、80 TOPS edge AI、12-core CPU、10.2 TFLOP GPU；MT2739 展示 5G-Advanced/NR-NTN automotive video calling；T930 + Filogic 8800 展示 Wi-Fi 8/5G CPE、AI L4S + AI QoS、Network Doctor；6G Device-Cloud prototype 用 M90 和 Co-MIMO module 做协同 MIMO。NXP/Qualcomm 也都把车载、智能边缘和机器人连在一起。

变化性质：技术路线和 demo 真实；收入节奏偏 2027+。  
投资含义：汽车 AI cockpit、智能网关、Wi-Fi 8、5G-Advanced/NTN、6G Co-MIMO 代表下一轮 SoC/RF/连接价值量，但认证周期和车厂设计导入决定了它们不是 2026Q3 的主要业绩变量。

## 产品和技术路线三情景预测

说明：市场规模为美元口径，除明确引用外均为本报告估算。估算方法会写在“口径/假设”列；置信度按一手材料强度和市场定义清晰度分为高/中/低。

| 方向 | 当前成熟度（2026-06-10） | 未来 3 个月 | 未来 1 年基准 | 乐观情景 | 超预期乐观 | 市场规模/口径 | 利润率和价值捕获 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rack-scale AI factory / Vera Rubin-NVL72 生态 | 展示/设计中，ASUS/Delta/LITEON 已给出整柜/配套件；NVIDIA Vera Rubin 为 2026-2027 平台节奏 | 看 GB300/Vera Rubin 相关 ODM 订单、Vera Rubin cold plate/CDU/power shelf design win | 2027 年 AI data center broad market 按 MarketsandMarkets 2026 $471.6B、27.5% CAGR 推算约 $601B；其中高密 AI rack infrastructure 估算占 35-45%，约 $210-270B | 高密 rack 占比 50%，约 $300B | hyperscaler 和 sovereign AI 同步扩建，占比 55%+，约 $330B+ | 口径为 AI data center compute/power/cooling/network/storage broad market，不等于服务器厂收入；置信度中 | GPU/HBM 毛利最高；rack integration 毛利低但收入弹性大；power/liquid cooling 毛利中高且订单能见度提高 |
| 800VDC + CDU + cold plate + busbar | Delta/LITEON/ASUS 已展示具体产品；从 row 到 chip level | 800VDC、2.4MW/3MW CDU、25kW pump、90/110kW shelf 是否进入客户 RFQ | 数据中心液冷市场：MarketsandMarkets 2026 $4.07B，2027 按 31.5% CAGR 约 $5.35B；IMARC 2025 $4.2B、2034 $19.1B，2027 约 $5.8B | 2027 $6.5-7.5B，受 150kW+ rack 拉动 | 2027 $8B+，若 Rubin/GB300 出货和 enterprise 液冷渗透同时加速 | 口径为液冷 solution/services，不含全部电源和 busbar；置信度中 | CDU/cold plate/pump/control 毛利估算 25-40%；整套 power train 更看系统能力；长期赢家是能同时做电源+热+监控的厂商 |
| Disaggregated inference / CPU-dense rack | Intel+SambaNova+Foxconn+Vector Core 已演示；商业客户 Together.ai | 看 Vector Core、Together.ai benchmark 和商业价格 | 2027 年 inference rack 渗透率按 AI data center capex 15-25% 估算，约 $90-150B broad hardware opportunity | 25-35%，约 $150-210B | 35%+，若 agentic workload 使 CPU/GPU 比例显著提高 | 估算链：AI DC 2027 $601B × inference rack 15-35%；置信度低/中 | CPU、RDU/ASIC、DPU/NIC、memory、switch 均受益；Intel 需证明 18A、功耗和客户转换 |
| Local agent AI PC / RTX Spark / Snapdragon X2 Elite | RTX Spark 官方公布，2026 秋季机型；Qualcomm X2 Elite mini-PC 80 TOPS/0.7L；Snapdragon C $300+ entry laptops | 看秋季上市价格、OEM SKU 数、developer tool、Windows agent security | IDC 2026 PCD 出货 401.9M 台、同比 -10.4%；AI PC revenue 估算：2026 AI-capable PC 70-110M 台 × $850-1,200 ASP = $60-132B | 2027 AI-capable PC 120-160M 台，$110-180B | RTX Spark/Windows agent 形成高端新类别，2027 180M 台以上，但需内存供给改善 | AI PC 口径为 NPU/AI SoC/RTX Spark 等 capable PC 零售收入估算；置信度低/中 | SoC/GPU/IP 捕获最大；OEM 捕获 ASP 但受竞争压制；内存/SSD 价格是最大利润扰动 |
| Robotics edge compute / Physical AI reference design | Qualcomm IQ10 RRD、NVIDIA Jetson Thor、Intel OpenVINO Physical AI、NXP demos；多为 sample/early access | 看 IQ10 2026-09 availability、Jetson Thor module 供货、OpenVINO 2H26 GA | Humanoid robots 狭义市场按 MnM 2025 $2.92B、CAGR 39.2% 推算 2026 $4.1B、2027 $5.7B；Physical AI 广义 2030 €430B | 2027 $6-8B humanoid + $2-4B edge module/robotics compute | 若出现大规模 AMR/工业/仓储 fleet 订单，2027 狭义可接近 $10B | Humanoid 是狭义；Physical AI 包含汽车/工业/医疗/物流系统，不能混用；置信度中 | 2026-2027 赚钱先在 sensor/compute/control/power module；本体 OEM 利润率不稳定 |
| AI data center networking/optics/CPO | NVIDIA Vera Rubin NVL72 已绑定 Spectrum-X Ethernet Photonics CPO、ConnectX-9、BlueField-4；Marvell keynote 聚焦 AI connectivity | 看 1.6T/3.2T optics、CPO switch、scale-out Ethernet 订单 | 估算 AI networking/optics/interconnect 为 AI DC broad market 8-15%，2027 $48-90B | 15-18%，$90-108B | 如果 CPO/1.6T 变成大规模瓶颈，20%+，$120B+ | 估算链：AI DC $601B × 8-20%；置信度低，中长期高弹性 | Switch ASIC/DSP/optical engine 毛利可高；光模块制造毛利较低但量弹性大 |
| Automotive/edge AI connectivity | MediaTek 80 TOPS cockpit、Wi-Fi 8 CPE、5G NR-NTN、6G Co-MIMO；NXP/Qualcomm demos | 主要是 demo/设计导入 | 2027 revenue 贡献偏样品/设计费/少量量产，按相关 SoC/RF/edge module 增量 $2-5B 估算 | $5-8B | 若车厂与 CPE 同步量产，$10B+ | 无统一会议口径；按 SoC/RF/模组增量估算；置信度低 | SoC/PMIC/RF/MCU 安全认证价值高，系统集成利润有限 |

## 市场规模和利润池

### AI data center broad market：定义冲突大，但方向一致向上

第三方口径差异很大：MarketsandMarkets 2026-03 把 AI data center market 定义为 compute server、storage、cooling、power、network switches、DCIM 等，给出 2025 年 $344.24B、2026 年 $471.59B、2032 年 $2,023.52B、CAGR 27.5%。IDC 服务器数据则显示 2025Q4 server spending 同比 +52.4%、unit +10.3%，AI infrastructure buildout 是主导变量。两者不是同一口径：前者是广义 AI 数据中心，后者是 server tracker。

本报告用于 2027 年判断的基准：AI data center broad market 约 $600B；其中真正可映射到 COMPUTEX 2026 的硬件利润池按 6 层拆：

| 层级 | 2026-2027 可见产品 | 价值捕获判断 | 当前利润率估算 |
| --- | --- | --- | --- |
| Accelerator/GPU/HBM | NVIDIA Rubin/Blackwell、AMD Instinct、custom ASIC、HBM | 长期利润率最高，供给约束强 | 专有 silicon/HBM 结构性毛利最高；GPU 供应商可达高毛利，HBM 随供给周期波动 |
| CPU/RDU/DPU/NIC | Intel Xeon 6+、SambaNova RDU、ConnectX/BlueField | inference 时代占比抬升 | CPU/DPU 半导体毛利中高；需看客户锁定 |
| Network/optics/CPO | Spectrum-X、ConnectX-9、CPO、1.6T/3.2T optics | 被市场低估；scale-out 限制会越来越硬 | ASIC/DSP/IP 毛利高；光模块制造 20-35% 估算 |
| Power/liquid/cooling | Delta 800VDC、CDU、pump、cold plate、LITEON power/rack | 2026H2-2027 最直接受益 | 系统级 25-40% 毛利估算；运维/服务提升粘性 |
| ODM/rack integration | Foxconn、Quanta/Wiwynn、ASUS、Gigabyte、Supermicro | 收入弹性强，毛利率低 | 通常 6-12% 毛利、2-6% operating margin 估算 |
| Deployment/storage/context memory | ASUS DSX、CMX storage、digital twin simulation | 新兴利润池，决定 time-to-first-token | 软件/服务若能产品化，毛利高；当前收入小 |

### 液冷和电源：当前市场小，但弹性和确定性最好

MarketsandMarkets：data center liquid cooling market 2026 年 $4.07B，2033 年 $27.65B，CAGR 31.5%。IMARC：2025 年 $4.2B，2034 年 $19.1B，CAGR 17.82%。差异来自是否纳入 services、高密 AI 数据中心、immersion/direct-to-chip 等子口径。

COMPUTEX 2026 的增量不是“液冷市场存在”，而是明确展示了下一代 AI 机柜配套参数：

- Delta：800VDC in-row power、2.4MW liquid-to-liquid CDU、3MW GoCool LTL CDU、25kW HVDC e-pump、N+1 redundancy、hot-swappable、Vera Rubin NVL72 cold plate。
- ASUS：Vera Rubin NVL72 AI POD TDP 187-227kW。
- LITEON：800VDC、NVIDIA Vera Rubin NVL72 AI factory solutions、power/rack/liquid cooling portfolio。

未来一年三情景：

- 基准：2027 年全球数据中心液冷 $5.3-5.8B；高密 AI rack 占新增需求大头；gross margin 25-35%。
- 乐观：$6.5-7.5B；150kW+ rack 在 hyperscaler 扩散，colocation 开始为 AI 专区改造。
- 超预期乐观：$8B+；Vera Rubin/GB300 交付顺利，800VDC 与 liquid-to-chip 成为大客户标配。

### AI PC：规模看起来大，但利润不一定在 PC OEM

IDC 2026 PCD 全年预测 401.9M 台、同比 -10.4%；Gartner 2026-02 公开口径称内存和 SSD 价格到 2026 年底或上涨 130%，PC 价格上涨 17%，智能手机价格上涨 13%；Gartner 2026Q1 PC 出货为 62.8M 台、同比 +4%。这组数据说明 AI PC 的核心矛盾是：本地 agent 需要大内存/高 NPU/GPU，但 2026 年恰好遇到内存涨价和消费力压力。

估算链：

- 2026 年 AI-capable PC：70-110M 台，ASP $850-1,200，零售收入 $60-132B。
- 2027 年基准：120-160M 台，ASP $900-1,150，收入 $110-180B。
- 超预期情景：RTX Spark/Windows agent 形成开发者和 creator 新类别，2027 年 180M 台以上，收入 $180B+。

价值捕获：NVIDIA/Qualcomm/AMD/Intel/MediaTek 等 SoC/GPU 平台捕获主要利润；OEM 受品牌和渠道约束；内存、OLED、散热、battery 受益但会吃掉 OEM 毛利。AI PC 相关公司若没有独家 silicon、软件栈或高端渠道，不能按“AI agent PC”直接高估弹性。

### Physical AI/机器人：广义 €430B 不等于 humanoid 本体收入

Strategy& 给出 2030 年 Physical AI 广义市场约 €430B，其中汽车约 €171B，工业自动化和仓储约 €69B；MarketsandMarkets 给出 humanoid robot 狭义市场 2025 年 $2.92B、2030 年 $15.26B、CAGR 39.2%。两者不能混用：前者包括汽车、工业、医疗、物流等系统级部署，后者更接近机器人本体。

本报告判断：

- 2026-2027 最先放量：edge AI compute module、industrial PC、sensor hub、motion control、battery/power management、fleet management software。
- 2026-2027 不宜过度外推：humanoid 量产本体、消费级机器人、通用场景替人。
- 关键成本/利润变量：传感器数量、实时控制安全、环境适应性、维护/售后成本、fleet utilization。

三情景：

- 基准：2027 年 humanoid 狭义 $5-6B，robotics edge compute/module 增量 $1-2B。
- 乐观：2027 年 $8-10B，若 AMR、工业、仓储和零售出现 10,000 台级 fleet 订单。
- 超预期乐观：2027 年 $12B+，需要多个头部 OEM 或大型工业客户把 reference design 变成可复制整机平台。

## 反共识洞见和重要更新

### 1. 市场可能低估电源/液冷/整柜部署，相对高估单机 AI PC

COMPUTEX 2026 最硬的数字不是某个 PC NPU TOPS，而是 AI rack 的 TDP、CDU MW 级能力、800VDC、cold plate 和 deployment platform。PC 端仍有总量和内存成本压力；AI rack 端则是客户必须解决的物理瓶颈。股票映射上，AI PC OEM 的叙事弹性可能不如 power/liquid cooling、rack integration 和 network/optics。

### 2. Physical AI 不是纯概念，但收入先在“机器人供应链”，不是机器人本体

Qualcomm/NVIDIA/Intel/NXP/Advantech 的材料都把 hardware、sensor、real-time control、ROS2/OpenVINO、MLOps/DevOps 放在一起，这说明产业从 demo 走向 reference platform。但这不会自动转化为 humanoid 本体利润。更实用的跟踪对象是：edge module ASP、开发套件出货、industrial PC 订单、sensor 接口数量、EtherCAT/CAN-FD/TSN 认证、客户 fleet size。

### 3. Intel 的核心反转点不是“回到 GPU 竞争”，而是 inference orchestration

Intel 本届最值得跟踪的不是 Arc handheld 或 PC 设计数量，而是 Xeon 6+ 18A、36,864 cores/32U/100kW rack，以及 disaggregated inference 里 CPU/RDU/GPU 的任务分工。如果 agentic inference 真让 CPU 回到 1:1 或更高占比，Intel 有结构性机会；如果 18A 和客户交付推迟，则这仍只是 keynote 叙事。

### 4. Qualcomm 的机器人平台比入门 PC 平台更可能形成利润弹性

Snapdragon C 的 $300+ entry laptop 可以扩大出货，但 ASP/毛利可能有限。相反，Dragonwing IQ10 RRD 的 700 TOPS、12 路 GMSL2 camera、工业温度、EtherCAT/CAN-FD、ROS2/AI Hub 更接近高附加值 industrial/robotics 平台。若 2026-09 可用后出现 NEURA/Advantech/NEXCOM/Thundercomm 等量产项目，弹性可能高于 PC 端。

### 5. Marvell/网络/光互联的投资逻辑更硬，但需等官方规格和订单

本届 keynote 和媒体线索都指向 connectivity becoming the next bottleneck；NVIDIA Vera Rubin 官方材料已经把 Spectrum-X Ethernet Photonics CPO、ConnectX-9、BlueField-4 纳入 NVL72 系统。Marvell keynote 页面和会后媒体将其定位于 AI data center connectivity/custom silicon。由于本次自动检索未能完整抓取 Marvell keynote 视频细节，100T TeraLink 等具体产品参数在本报告中仅作为非官方线索，不作为核心结论支撑。后续需用 Marvell IR/press release/earnings call 确认。

### 6. 伪受益公司会很多：有 AI 展台不等于有收入弹性

应降权的公司类型：

- 只有外观/消费电子外设/概念 demo，没有 silicon、power、thermal、network、industrial certification 或客户订单。
- PC OEM 只有“AI ready”标签但无高端 mix、软件生态或供应链议价。
- 机器人整机公司没有 fleet data、安全认证、维护网络和成本曲线。
- 数据中心普通结构件公司无法进入 800VDC、液冷、busbar、cold plate、CDU、rack telemetry 等增值环节。

## 公司和产业链映射

| 层级 | 头部/代表公司 | COMPUTEX 2026 证据 | 收入暴露和投资弹性 |
| --- | --- | --- | --- |
| GPU/AI platform | NVIDIA、AMD | NVIDIA RTX Spark、Vera Rubin NVL72、Jetson Thor；AMD 主要是 Ryzen/RDNA4/平台寿命 | NVIDIA 最强；AMD 本届 AI data center 新增信号较弱，PC/gaming 更明显 |
| CPU/inference orchestration | Intel、AMD | Intel Xeon 6+、disaggregated inference、OpenVINO Physical AI | Intel 弹性取决于 18A、Xeon 6+、customer rack；AMD 本届信号较弱 |
| Edge/robotics/auto SoC | Qualcomm、MediaTek、NXP | Dragonwing IQ10 RRD、Snapdragon X2/C、Dimensity AX C-X1、NXP edge intelligence demos | Qualcomm robotics 平台弹性高；MediaTek/NXP 偏车载/连接中期导入 |
| Networking/optics/custom silicon | Marvell、Broadcom、NVIDIA networking、Coherent/Lumentum 等 | Marvell keynote；NVIDIA Spectrum-X Ethernet Photonics CPO | 可能是低估利润池；需官方订单/1.6T/3.2T 节奏确认 |
| Rack/ODM/system integration | Foxconn、Quanta/Wiwynn、ASUS、GIGABYTE、Supermicro、Pegatron、MiTAC | ASUS DSX/AI POD；Intel+Foxconn rack；COMPUTEX 展商覆盖 | 收入弹性强，毛利低；看整柜交付能力和客户锁定 |
| Power/liquid/cooling | Delta、LITEON、Vertiv、Schneider、Auras、Cooler Master 等 | Delta 800VDC/2.4MW/3MW CDU；LITEON 800VDC/Vera Rubin；ASUS partner ecosystem | 本届最清晰增量之一；订单和交期决定短期股价弹性 |
| Industrial edge/robotics integrators | Advantech、AAEON、Innodisk、NEXCOM、Thundercomm、Radxa | Advantech WEDA；Qualcomm IQ10 早期伙伴 | 中小公司弹性高，但需确认量产项目和客户行业 |
| Memory/storage/context memory | SK hynix、Samsung、Micron、Phison、Innodisk、ADATA、TeamGroup | NVIDIA/AI PC 需要高容量统一内存；Intel press kit 提及 Phison+Intel local AI workloads；COMPUTEX memory/storage 展商多 | 内存涨价利好上游但压制 PC 需求；工业/enterprise storage 更稳 |

## 风险、反证条件和后续跟踪

### 会立刻下修判断的数据

- NVIDIA/ASUS/Delta/LITEON 的 Vera Rubin/GB300/NVL72 相关方案在 2026H2 没有明确订单、交期或客户披露。
- 800VDC 和 liquid-to-chip 只停留在 showcase，未进入 hyperscaler/colocation RFQ 或认证。
- RTX Spark 秋季上市推迟、价格过高、软件兼容/安全沙箱体验不达预期，导致开发者和 creator 采用不足。
- IDC/Gartner 继续下修 2026-2027 PC/PCD 出货，同时内存/SSD 价格涨幅超过当前预期，AI PC ASP 被成本吃掉。
- Intel Xeon 6+ 18A 量产、功耗、客户验证或 SambaNova/Foxconn rack 交付不及预期。
- Dragonwing IQ10 RRD 2026-09 availability 延迟，或 early access partners 没有量产项目。
- AI inference price/token 下降速度快于硬件单位价值量增长，导致 cloud capex 进入 digestion。
- 台海/出口管制/签证许可/高端 AI 硬件出口限制影响 COMPUTEX 供应链交流和订单兑现。

### 后续跟踪清单

| 时间 | 节点 | 要看什么 | 刷新频率 |
| --- | --- | --- | --- |
| 2026-06 至 2026-07 | COMPUTEX 会后公司访谈、IR 会议、台湾供应链订单 | Delta/LITEON/ASUS/Wiwynn/Foxconn 是否披露 AI rack、800VDC、液冷订单 | 每周 |
| 2026-07-16 | AMD Ryzen 7 7700X3D 上市 | $329 定价是否刺激 AM5 中端升级；是否只是 PC 存量防守 | 一次 |
| 2026Q3 | Qualcomm Dragonwing IQ10 RRD global availability | 早期伙伴是否转 design win；是否出现量产 AMR/humanoid/industrial robot | 每月 |
| 2026Q3-Q4 | RTX Spark Windows PCs | OEM SKU、价格、内存容量、battery、Windows agent security、developer adoption | 每月 |
| 2026H2 | Intel OpenVINO Physical AI GA；Xeon 6+ rack | 18A 出货、rack customer、SambaNova/Vector Core/Together.ai 进展 | 每月 |
| 2026H2-2027H1 | GB300/Vera Rubin/NVL72 供应链 | Rack power density、liquid cooling attach rate、CDU lead time、800VDC 标配化 | 每两周 |
| 2026Q4 起 | 1.6T/3.2T optics、CPO、AI networking | Marvell/Broadcom/NVIDIA networking 订单、毛利、客户集中度 | 每月 |

## 来源清单

### 一手官方：会议/主办方

| 来源 | 日期 | 类型 | 可信度 | 用途 |
| --- | --- | --- | --- | --- |
| COMPUTEX Show Profile，https://www.computextaipei.com.tw/en/menu/A546BFC6C2E2ED34D0636733C6861689/info.html | 页面检索 2026-06-10 | 会议官网 | 高 | 会议日期、场馆、主题 |
| COMPUTEX Activity Calendar，https://www.computextaipei.com.tw/en/calendar/event-calendar.html | 页面检索 2026-06-10 | 官方议程 | 高 | Qualcomm/Marvell/Forum/Keynote 时间线 |
| COMPUTEX 2026 Opens Amid Surging Global Demand for AI Infrastructure，https://www.computextaipei.com.tw/en/news/51FD71345BDCAF86/info.html | 2026-06-02，修订 2026-06-09 | 官方新闻稿 | 高 | 1,500 公司、33 国家、6,000 展位、新专区、主讲公司 |
| AI Goes Physical — Taiwan Leads Global Industry Transformation，https://www.computextaipei.com.tw/en/news/9F6B9B767471625F/info.html | 2026-06-01，修订 2026-06-09 | 官方新闻稿 | 高 | AI Robotics Zone、Forum 主题、Physical AI 口径 |
| COMPUTEX 2026 Concludes Successfully，https://www.computextaipei.com.tw/en/news/A9462967BB2D7702/info.html | 2026-06-05 | 官方会后稿 | 高 | 111,312 visitors、152 国家、keynote/forum/InnoVEX 数据 |

### 一手公司材料

| 来源 | 日期 | 类型 | 可信度 | 用途 |
| --- | --- | --- | --- | --- |
| NVIDIA RTX Spark 新闻稿，https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark | 2026-05-31 | 公司新闻稿 | 高 | RTX Spark 1 PFLOP、128GB、120B LLM、OEM 时间 |
| NVIDIA GTC Taipei at COMPUTEX 页面，https://www.nvidia.com/en-tw/gtc/taipei/computex/ | 2026-06 | 公司活动页 | 高 | GTC Taipei/COMPUTEX 覆盖、forum speaker、demo showcase |
| NVIDIA GTC Taipei live updates/BCA，https://blogs.nvidia.com/blog/nvidia-gtc-taipei-computex-2026-news/ | 2026-05-21 起 | 公司博客 | 高 | Vera Rubin NVL72、Jetson Thor、Alpamayo、液冷/功耗/性能参数 |
| Intel Computex 2026 Press Kit，https://newsroom.intel.com/press-kit/press-kit-intel-at-computex-2026 | 2026-06-01，更新 2026-06-05 | 公司 press kit | 高 | Intel 主题、文档、生态新闻索引 |
| Intel Announces New AI Innovations at Computex，https://newsroom.intel.com/artificial-intelligence/intel-announces-new-ai-innovations-at-computex | 2026-06-01 | 公司新闻稿 | 高 | Xeon 6+、rackscale AI、disaggregated inference、Foxconn/SambaNova |
| Intel 130+ Customers Choose Series 3，https://newsroom.intel.com/client-computing/customers-choose-intel-for-edge-devices | 2026-05-31 | 公司新闻稿 | 高 | OpenVINO Physical AI、130+ edge design engagements |
| Qualcomm Computex 2026 Press Kit，https://www.qualcomm.com/news/press-kits/computex-2026-press-kit | 2026-06 | 公司 press kit | 高 | Year of Agents、forum、slides/video 索引 |
| Qualcomm Dragonwing IQ10 RRD，https://www.qualcomm.com/news/onq/2026/06/dragonwing-iq10-robotics-reference-design | 2026-06-01 | 公司博客 | 高 | 700 TOPS、18 Oryon cores、12 GMSL2、工业接口、2026-09 |
| Qualcomm Snapdragon C，https://www.qualcomm.com/news/releases/2026/05/introducing-snapdragon-c--designed-to-revolutionize-entry-tier-l | 2026-05-28 | 公司新闻稿 | 高 | $300+ entry laptop、AI NPU、2026 later availability |
| Qualcomm ASUS Ascent QN10，https://www.qualcomm.com/news/onq/2026/06/asus-ascent-qn10-snapdragon-x2-elite | 2026-06-02 | 公司页面 | 中/高 | Snapdragon X2 Elite mini-PC，80 TOPS，0.7L；正文 JS 限制，meta 可抓取 |
| AMD Computex 2026，https://www.amd.com/en/blogs/2026/amd-computex-2026-10-years-of-am4-am5-support-through.html | 2026-06 | 公司博客 | 高 | 7700X3D、$329、2026-07-16、AM5 2029、5800X3D anniversary |
| MediaTek Computex 2026，https://www.mediatek.com/computex2026 | 2026-05/06 | 公司活动页 | 高 | Dimensity AX C-X1、80 TOPS、Wi-Fi 8、5G NR-NTN、6G Co-MIMO |
| NXP at COMPUTEX 2026，https://www.nxp.com/company/about-nxp/events/computex-taipei%3ANXP-AT-COMPUTEX-TAIPEI | 2026-06 | 公司活动页 | 高 | Trusted edge intelligence、physical AI、车载/工业/IoT demos |
| Advantech COMPUTEX 2026，https://www.advantech.com/en-us/events/computex | 2026-06 | 公司活动页 | 高 | WEDA、edge AI、Physical AI forum |
| ASUS Vera Rubin AI POD，https://press.asus.com/news/press-releases/asus-ai-pod-nvidia-vera-rubin-nvl72/ | 2026-03-17 | 公司新闻稿 | 高 | 187/227kW、100% liquid-cooled、Vera Rubin NVL72 |
| ASUS DSX AI Factory，https://press.asus.com/news/press-releases/asus-nvidia-dsx-ai-factory-platform-computex-2026/ | 2026-06-02 | 公司新闻稿 | 高 | DSX、time to first token/revenue、AI factory deployment |
| Delta COMPUTEX 2026 landing，https://landing.deltaww.com/en-US/landing/Computex-2026 | 2026-06 | 公司活动页 | 高 | 800VDC、2.4MW/3MW CDU、90/110kW power shelf、Vera Rubin cold plate |
| Delta modular data center release，https://www.deltapowersolutions.com/en/mcis/news-2026-delta-debuts-prefa-ai-modular-data-center-at-computex-to-reduce-deployment-time-by-up-to-60percent.php | 2026-06 | 公司新闻稿 | 高 | prefabricated AI modular data center、部署时间 -60%、800VDC/3MW liquid cooling |
| LITEON COMPUTEX 2026，https://www.liteon.com/en/news/press-center/content/liteon-nvidia-mgx-computex-2026 | 2026-06 | 公司新闻稿 | 高 | 800VDC、NVIDIA Vera Rubin NVL72、rack/power/liquid cooling |

### 技术/市场数据

| 来源 | 日期 | 类型 | 可信度 | 用途 |
| --- | --- | --- | --- | --- |
| IDC Server Market Insights，https://www.idc.com/promo/servers/ | 2026-04 附近 | 市场数据页 | 中/高 | 2025Q4 server spending +52.4%、unit +10.3% |
| IDC PCD Forecast，https://www.idc.com/promo/pcdforecast/ | 2026 | 市场数据页 | 中/高 | 2026 PCD 401.9M、同比 -10.4% |
| Gartner Q1 2026 PC shipments，https://www.gartner.com/en/newsroom/press-releases/2026-4-10-gartner-says-worldwide-pc-shipments-increased-4-percent-in-first-quarter-of-2026 | 2026-04-10 | 市场新闻稿 | 中/高 | Q1 PC 62.8M、同比 +4%；网页对自动抓取返回 403，使用搜索可见摘要 |
| Gartner memory cost impact，https://www.gartner.com/en/newsroom/press-releases/2026-02-26-gartner-says-surging-memory-costs-will-reduce-global-pc-and-smartphone-shipments-in-2026 | 2026-02-26 | 市场新闻稿 | 中/高 | DRAM+SSD +130%、PC 出货 -10.4%、PC price +17%；网页对自动抓取返回 403，使用搜索可见摘要 |
| MarketsandMarkets AI Data Center Market，https://www.marketsandmarkets.com/Market-Reports/ai-data-center-market-267395404.html | 2026-03 | 第三方市场研究 | 中 | AI data center 2025/2026/2032 规模和 CAGR |
| MarketsandMarkets Data Center Liquid Cooling，https://www.marketsandmarkets.com/Market-Reports/data-center-liquid-cooling-market-84374345.html | 2026-03 | 第三方市场研究 | 中 | 液冷 2026 $4.07B、2033 $27.65B、CAGR 31.5% |
| IMARC Data Center Liquid Cooling，https://www.imarcgroup.com/data-center-liquid-cooling-market | 2026 | 第三方市场研究 | 中 | 液冷 2025 $4.2B、2034 $19.1B、CAGR 17.82% |
| Strategy& Physical AI，https://www.strategyand.pwc.com/de/en/industries/telecommunication-media-and-technology/physical-ai.html | 2026 | 咨询研究 | 中 | Physical AI 2030 €430B、汽车/工业拆分 |
| MarketsandMarkets Humanoid Robot，https://www.marketsandmarkets.com/Market-Reports/humanoid-robot-market-99567653.html | 2025-04 | 第三方市场研究 | 中 | Humanoid robot 2025 $2.92B、2030 $15.26B、CAGR 39.2% |

### 非官方/二手线索

| 来源 | 日期 | 类型 | 可信度 | 用途 |
| --- | --- | --- | --- | --- |
| ServeTheHome NVIDIA Computex 2026 live coverage，https://www.servethehome.com/nvidia-computex-2026-keynote-live-coverage/ | 2026-06 | 参会媒体 live blog | 中 | 交叉验证 NVIDIA keynote 叙事、robotics/RTX Spark 现场信息 |
| ServeTheHome Qualcomm Computex 2026 live coverage，https://www.servethehome.com/qualcomm-computex-2026-live-coverage/ | 2026-06 | 参会媒体 live blog | 中 | Qualcomm agentic AI keynote 线索 |
| AEI/Dempa Marvell Computex coverage，https://aei.dempa.net/archives/35208 | 2026-06 | 媒体报道 | 低/中 | Marvell connectivity/100T 线索；需 Marvell 一手材料进一步确认 |
| Tom's Hardware / PC Gamer / TechRadar COMPUTEX 2026 coverage | 2026-06 | 科技媒体 | 低/中 | PC/handheld/AI workstation 价格和现场口碑线索；仅作交叉验证，不支撑核心结论 |

