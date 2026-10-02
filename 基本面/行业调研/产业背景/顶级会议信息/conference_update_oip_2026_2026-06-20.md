# 2026 OIP 会议追踪：核心变化、产品爆发和市场预期差

- 会议名称：Optical Interconnects and Packaging (OIP) Conference 2026
- 会议日期：2026-06-15 至 2026-06-17
- 会议地点：Fort Collins, Colorado, USA；The Elizabeth Hotel
- 会议主题：Navigating Communication and Packaging Challenges in the AI Era
- 材料检索截止日期：2026-06-20
- 报告完成日期：2026-06-20
- 写作边界：本报告按本次任务要求独立追踪会议，仅使用公开联网资料、会议公开日程、公司公开材料、标准/联盟资料和明确标注的二手市场资料；未读取、引用或继承项目内旧报告、索引、缓存和中间结论。

证据分级：

| 级别 | 来源类型 | 使用方式 |
| --- | --- | --- |
| A | OIP 官网、官方详细日程、公司新闻稿/技术博客/投资者材料、标准/联盟官网 | 可支撑事实、技术路线和公司映射 |
| B | LightCounting、Cignal AI、Yole、市场报告公开摘录、媒体转述公司材料 | 可支撑市场规模和情绪判断，但需注明口径 |
| C | LinkedIn、YouTube、参会者分享、论坛、券商/媒体会后纪要 | 仅作为线索或情绪，不单独支撑核心结论 |

## 结论摘要

1. OIP 2026 的核心信号不是“CPO 明天全面替代 pluggable”，而是 AI 集群互连的讨论中心从光模块速率转向系统级可制造性、链路稳定性、测试并行度、外置光源、基板/材料和开放接口。官方日程把 3 天拆成 AI Datacenters、Next Generation SerDes and CPO、High Speed Modulators、Photonic Interconnects、PIC、VCSELs/Emerging Topics，以及 3 个 workshop：能效报告、CPO 基板材料、CPO 规模制造。这个结构本身就是产业优先级。

2. 客户侧声音比以往更重。NVIDIA、Microsoft、Meta、Oracle 在 OIP 日程中直接出现：NVIDIA keynote 讲 Photonics and Circuits for Next Generation AI Datacenters；Microsoft keynote 讲 Transitioning to Optically Connected AI Scale-up Domains；Meta 有 CPO 可靠性/能效、400G electrical scale-up 是否仍可行两类主题；Oracle 讲 resilient AI fabrics。这意味着光互连已经不是光模块厂的局部升级，而是在云厂/系统厂的 AI fabric 架构层被重新定义。

3. 未来 12 个月的实际收入主线仍是 800G/1.6T pluggable 和 200G/lane 生态，CPO/NPO 是高弹性增量而不是最大收入池。Cignal AI 在 2025-05 的公开口径称 datacom optical component 2025 收入将超过 160 亿美元；LightCounting 在 2026-04 将 2026 年 Ethernet transceiver 增长预期上调至 65%。按这两个口径交叉，2026 年 AI/datacenter 光互连组件和高速以太网光收发收入可粗略落在 250 亿至 280 亿美元区间；CPO 直接市场仍可能只有 1 亿至 3 亿美元量级，但与 CPO 相关的激光、光引擎、连接器、测试和封装已开始锁定未来利润池。

4. CPO 的真正瓶颈不是“有没有 demo”，而是 known-good optical engine、光电共封装良率、detachable fiber attach、晶圆级/封装级光测试、外置光源寿命和现场可维护性。Lightmatter 在 OIP 的公开摘要明确把 CPO HVM 难点列为 known-good optical engines、scalable detachable fiber attachment、assembly/packaging/test；Marvell 在 2026-05 技术博客中把测试瓶颈描述为从“分钟级、单站、rack-and-stack”转向 IC 式并行和自动化；OIP WS3 专门安排 GlobalFoundries、TEL、Marvell、Lightmatter、Keysight 讨论规模制造。

5. 市场可能低估了材料、基板、连接和测试环节的利润弹性。OIP WS2 的参会者不是只围绕交换芯片和模块：AT&S、Applied Materials、Ajinomoto、Resonac、DNP、Intel、IC Photonics 都在 CPO 基板、材料、玻璃基板、ELS 和 advanced packaging 上出现；OIP 展商 Nagase ChemteX 直接强调 LMC、光学 bonding、V-groove bonding、165°C aging、85/85、-55°C 至 125°C thermal cycle 等封装可靠性条件。这些环节的单位价值小于 switch ASIC/光模块，但在 CPO/NPO 规模化早期更容易成为瓶颈。

6. 反共识结论：短期最危险的过度乐观是把 CPO 当作 2026 年收入主线；最可能被低估的是 1.6T pluggable 的持续性、400G/448G electrical pathfinding 的顽强生命力、外置高功率激光与 VCSEL wide-parallel scale-up 的可选性，以及晶圆级测试/连接器/基板材料的供给约束。OIP 的 Meta 题目“Is 400G Still a Viable Option for Electrical Scale-Up -- and Why It Matters”本身提醒：铜/电不是立即死亡，CPO 的 adoption 取决于系统成本、可靠性和维护模型，而不只是 pJ/bit。

## 会议重点和方向变化

### 1. 公开日程显示的 10 个核心主题

| 主题 | OIP 2026 直接证据 | 对应公司/机构 | 技术参数和客户需求 | 投资含义 |
| --- | --- | --- | --- | --- |
| AI datacenter 光互连成为系统架构问题 | M1 AI Datacenters；NVIDIA/Microsoft keynotes；Meta/Oracle talks | NVIDIA、Microsoft、Meta、Oracle、University of Toronto、Cambridge、UW | AI scale-up/out fabric 需要更低 pJ/bit、更少 link flap、更高 radix、更短部署周期 | 价值从光模块 SKU 扩展到系统、交换、封装、软件 telemetry |
| 1.6T/3.2T 和 400G/lane 路线进入工程验证 | Marvell 400G SerDes I/O；Keysight 400Gbps measurements；AMD 448G SERDES and Optics；Broadcom OFC 2026 Taurus 400G/lane DSP | Marvell、Keysight、AMD、Broadcom、Coherent、Lumentum | 200G/lane 是 1.6T 量产基线；400G/lane 支撑 3.2T 和 204.8T switch | 2026-2027 收入主线仍在 pluggable/LPO/LRO/光 DSP/EML/TIA |
| CPO 从“概念”转向 HVM、serviceability 和 known-good die | WS3 Overcoming CPO Manufacturing Challenges at Scale；Lightmatter OIP 摘要 | Lightmatter、GlobalFoundries、TEL、Marvell、Keysight、NVIDIA | known-good optical engine、detachable fiber attachment、wafer-level validation、pick-and-place automation | CPO 规模化更利好测试设备、封装材料、连接器、OSAT/基板 |
| 基板/材料成为 CPO 是否规模化的硬约束 | WS2 Substrates, Materials, and the Rise of CPO | AT&S、Applied Materials、Ajinomoto、Resonac、DNP、Intel、IC Photonics、Nagase | organic substrate、glass substrate、ABF/封装材料、低 CTE/低 shrinkage bonding、ELS | 上游材料/设备可能比模块组装更有议价弹性 |
| 外置光源和高功率激光成为 CPO/NPO 的关键件 | OIP WS2 IC Photonics ELS；Lumentum 800 mW SHP laser；NVIDIA 对 Coherent/Lumentum 的投资 | IC Photonics、Lumentum、Coherent、NVIDIA | Lumentum 1310nm SHP laser：25°C >1.0W、50°C >800mW、linewidth <100kHz、SMSR >40dB | InP/laser capacity 是继 HBM/CoWoS 后的 AI 硬约束之一 |
| VCSEL “slow and wide” scale-up 重新被摆到台前 | OIP WS1 Lumentum VCSEL wide-parallel；W2 PicoJool VCSELs ready to take over copper；Lumentum OFC VCSEL demo | Lumentum、PicoJool、FUJIFILM BI | 1060nm VCSEL array、fan-out wafer-level package、UCIe/PCIe 等 slow-wide scale-up | 不是传统 multimode datacom 的简单延长，而是 rack/host co-packaged optical I/O 选项 |
| 硅光器件平台分化：fast-narrow vs wide-slow | imec OIP：Ge/Si APD、GeSi FK EAM、400G/lane fast-narrow CPO、3D Optical I/O wide-slow | imec、Marvell、Huawei、Lumentum、Lightwave Logic、Aluvia | 400G/lane、>110GHz plasmonic modulator、212Gbps O-band DWDM microring coherent transmitter | 量产价值取决于 foundry compatibility、热调谐、可靠性和封测成本 |
| 标准/联盟成为 hyperscaler 降低供应链风险的工具 | OCI MSA、Open CPX MSA、OCP CPO initiative | AMD、Broadcom、Meta、Microsoft、NVIDIA、OpenAI；Ciena、Coherent、Marvell、Molex、Samtec、TeraHop；Lightmatter/OCP | OCI：NRZ+WDM，silicon-centric optical scale-up；Open CPX：mechanical/thermal/electrical/optical/management interface | 开放接口降低单一供应商锁定，也会压缩纯模块厂长期超额毛利 |
| Coherent scale-across 从电信回到 AI 网络 | OIP 关注 scale-up/out；LightCounting 2026-04 提到 800G ZR/ZR+ in 2026，1.6T ZR/ZR+ in 2028-2029 | Ciena、Cisco/Acacia、Marvell、Coherent、Lumentum | 多数据中心 AI cluster、DCI、800ZR/ZR+、1.6T ZR/ZR+ | coherent DCI 是 AI capex 延伸，不应只按传统电信周期估值 |
| 光计算互连仍处早期，短期更多是技术线索 | OIP W2 Optalysys compute-in-transit；University of Kentucky photonic tensor cores | Optalysys、学术团队 | compute-in-transit、photonic tensor cores | 可作为远期 optionality，不应并入 2026-2027 基准收入 |

### 2. 相比过去 6 至 12 个月，方向变化在哪里

| 维度 | 2025 下半年至 OFC 2026 前后的市场共识 | OIP 2026 后的判断变化 |
| --- | --- | --- |
| CPO 节奏 | NVIDIA 和 Broadcom 带动 CPO 预期，市场容易把 2026 视为 CPO revenue breakout | OIP 强化的是“工程化和供应链进入关键阶段”，不是“所有收入立即切换”。CPO/NPO 需要良率、测试、连接器、ELS 和现场维护同步过关 |
| Pluggable 生命周期 | 有观点认为 CPO 会快速挤压 pluggable | LightCounting/Cignal 公开口径和 OIP 议题共同指向：2026-2027 主收入仍在 800G/1.6T pluggable、LPO/LRO、TRO/FRO、EML/SiPh/DSP |
| 电互连 | 市场叙事容易走向“铜墙已到，全部转光” | Meta 在 OIP 直接讨论 400G electrical scale-up 是否仍可行，Marvell/Broadcom/Keysight/OIF 仍在 224G/448G electrical pathfinding；电和光会在 rack/row/scale-up 不同距离分层共存 |
| 价值捕获 | 市场聚焦光模块厂和 CPO 概念股 | OIP 把基板、材料、玻璃、bonding、wafer-level test、ELS、fiber shuffle、detachable connector 提到同等重要位置；这些环节可能更早形成瓶颈溢价 |
| 标准 | NVLink/UALink/UEC/以太网各自叙事 | OCI、Open CPX、OCP CPO initiative 显示 hyperscaler 希望把 optical scale-up/near-package/co-package 从封闭方案推向可互操作生态 |
| 风险 | 市场常把 AI 光互连需求线性外推 | LightCounting 2026-04 提醒需求当前超过供给约 30%，但短缺可能在 2026 年底缓解；一旦双重下单消退，价格下降可能加速 |

### 3. 未来 3 个月、1 年、2 年的判断调整

| 时间 | 主要判断 | 需要跟踪的数据 |
| --- | --- | --- |
| 未来 3 个月，至 2026-09 | OIP 会后最重要的是确认哪些 talk 有论文/白皮书/客户验证公开，尤其是 Microsoft/Meta/Oracle 对 optical scale-up 的表述是否转成 RFP/标准/供应链订单 | IEEE Xplore/OIP 论文公开情况；NVIDIA Quantum-X Photonics availability；Open CPX draft spec；1.6T DR4/DR8 出货；Lumentum/Coherent capacity update |
| 未来 1 年，至 2027-06 | 1.6T pluggable 和 200G/lane 仍是收入核心；CPO/NPO 在 NVIDIA/Broadcom/Marvell/Lightmatter 客户项目中形成 early production；测试/连接/ELS 成为小而紧的利润池 | 800G/1.6T ASP；InP/EML/laser lead time；CPO link flap 数据；known-good optical engine yield；wafer-level test throughput；云厂 capex 与 GPU/XPU 出货 |
| 未来 2 年，至 2028-06 | 400G/lane、3.2T、204.8T switch 和 optical scale-up 标准进入真实产品节奏；如果 CPO 良率和维护模型被验证，利润池从模块转向 optical engine、ELS、封装和测试 | 3.2T module qualification；OCI/Open CPX/OCP 互操作测试；400G/lane electrical/optical BER；CPO field failure rate；客户是否把 optical I/O 放进 XPU/package roadmap |

## 产品和技术路线三情景预测

以下数字为截至 2026-06-20 的估算或公开口径整理。除非标为公司披露，否则市场规模数字不是精确财务预测，而是用于股票研究的量级判断。

| 产品/技术方向 | 会议和外部证据 | 成熟度 | 当前市场规模或收入基数，美元口径 | 未来 12 个月三情景 | 爆发力度判断 |
| --- | --- | --- | --- | --- | --- |
| 800G/1.6T pluggable datacom optics，包括 OSFP/QSFP-DD、DR/FR/LR、LPO/LRO/TRO/FRO | Cignal AI 2025-05：datacom optical component 2025 收入超过 160 亿美元；LightCounting 2026-04：2026 Ethernet transceiver 增长预期 65%；OIP 多个 1.6T/200G/lane/400G/lane 主题 | 800G 已量产；1.6T 进入 volume ramp；3.2T 预研 | 2026 年高速 datacom 光互连组件/以太网光收发收入估算约 250 亿至 280 亿美元，按 2025 >160 亿美元并乘 60% 至 65% 增长粗算 | 悲观：GPU/XPU/ASIC 限制和双重下单消退，2027 年滚动收入 270 亿至 300 亿美元；基准：1.6T 接棒 800G，320 亿至 360 亿美元；乐观：供给继续紧、云厂加库存，400 亿美元以上 | 高。收入确定性最高，但 ASP 和毛利在短缺缓解后可能下行 |
| 1.6T DR4/DR8 到 3.2T，400G/lane EML/SiPh/DSP 路线 | Broadcom OFC 2026 Taurus 400G/lane optical DSP + 400G EML/PD；Lumentum 1.6T DR4 OSFP with 4x400G differential EML；Coherent 400G/lane、3.2T、XPO；OIP AMD 448G SERDES and Optics | 1.6T 200G/lane 量产；400G/lane 多为 demo/工程验证 | 作为高速 datacom optics 的子集，2026 年 1.6T 相关收入估算约 20 亿至 50 亿美元；400G/lane/3.2T 真实收入仍以样品和早期设计为主，估算低于 5 亿美元 | 悲观：1.6T 延后，2027 约 40 亿至 60 亿美元；基准：1.6T 成 AI 新建网络主力，2027 约 70 亿至 120 亿美元；乐观：3.2T 前置设计和 400G/lane component 拉动，超过 150 亿美元 | 很高。最先兑现的是 DSP、EML/PD、TIA/CDR、测试设备，而不是所有模块厂 |
| CPO/NPO/Open CPX optical engines、CPO switch-side optics | OIP M2/T2/WS3；NVIDIA Quantum-X/Spectrum-X Photonics；Broadcom TH6-Davisson 102.4Tbps CPO；Open CPX MSA 2026-03；Lightmatter CPO HVM talk | 工程化/early production；非全面普及 | 直接 CPO 市场公开报告口径差异较大：SNS 2025 CPO 市场约 0.91 亿美元；360iResearch 2026 约 1.28 亿美元；实际含 CPO switch/optical engine/laser 的可寻址增量估算 2026 为 1 亿至 3 亿美元 | 悲观：reliability/test/field service 卡住，2027 低于 5 亿美元；基准：NVIDIA/Broadcom early access 和部分云厂试产，8 亿至 20 亿美元；乐观：CPO switch 规模出货且 Open CPX 供应链成熟，25 亿至 50 亿美元 | 弹性极高，但验证门槛最高。股价容易提前透支 |
| 外置光源 ELS、UHP/SHP laser、InP/EML/PD | OIP WS2 IC Photonics ELS；Lumentum 800mW SHP laser；NVIDIA 2026-03 分别向 Coherent/Lumentum 投资 20 亿美元并带采购承诺；LightCounting 提到 InP EML/laser capacity 是 2026 供给约束 | 高功率激光和 InP 供给进入战略稀缺；CPO ELS 仍在资格验证 | 2026 年 lasers/PICs for transceivers 估算约 35 亿至 45 亿美元；CPO/ELS 直接增量估算低于 5 亿美元，但采购承诺为多年数十亿美元量级 | 悲观：CPO 延迟，2027 ELS/CPO 激光增量 5 亿至 10 亿美元；基准：NVIDIA/Broadcom/Marvell 项目拉动，10 亿至 30 亿美元；乐观：laser capacity 继续成为卡点，30 亿至 50 亿美元 | 高。利润率和供给壁垒优于普通模块组装 |
| VCSEL wide-parallel optical scale-up | OIP Lumentum VCSEL wide-parallel、PicoJool VCSELs ready to take over copper、FUJIFILM 200Gb/s VCSEL；Lumentum OFC 2026 1060nm VCSEL array co-packaged with host ASIC | demo/早期系统验证；与传统 multimode VCSEL 不同 | 2026 年 AI scale-up VCSEL co-packaged/OIO 增量估算低于 2 亿美元；传统 VCSEL 数据通信市场另计 | 悲观：仅保留为 demo，2027 低于 3 亿美元；基准：rack-level slow-wide scale-up 小规模导入，3 亿至 8 亿美元；乐观：替代部分铜背板/短距电缆，10 亿至 20 亿美元 | 中高。若验证通过，Lumentum/VCSEL 阵列/多模连接受益；若失败，回到传统 VCSEL 周期 |
| 硅光器件平台：Ge/Si、GeSi EAM、MRM、plasmonics、EO polymer、Al2O3 | imec OIP 400G/lane fast-narrow CPO 与 wide-slow 3D Optical I/O；Marvell plasmonics >110GHz；Lightwave Logic EO polymer reliability；Aluvia Al2O3 PIC | SiPh 主流成熟；新材料平台大多处于 qualification 或 niche | 公开市场摘录称 silicon photonics 2026 市场约 23 亿美元；数据中心 SiPh PIC die 子市场 2026 估算约 6 亿至 9 亿美元 | 悲观：传统 EML/SiPh MZI 主导，2027 SiPh 市场 25 亿至 30 亿美元；基准：1.6T/CPO 拉动，30 亿至 40 亿美元；乐观：CPO/NPO 设计大量采用 SiPh engine，45 亿美元以上 | 中高。真正受益者是有 foundry、封装、测试和客户认证闭环的平台，不是单点材料故事 |
| 光封装、基板、玻璃、bonding、连接器、晶圆级/封装级测试 | OIP WS2/WS3；Nagase 展商 LMC/optical bonding；Keysight wafer-level validation；Applied/TEL/GF/AT&S/Ajinomoto/Resonac/DNP | 传统封装材料成熟，CPO 工艺窗口仍在扩大 | Yole 公开转述口径：photonics packaging 市场预计 2031 达 144 亿美元，若按“三倍”倒推，2026 broad photonics packaging 约 45 亿至 55 亿美元；AI CPO/NPO 相关子集估算低于 10 亿美元 | 悲观：CPO 延迟，2027 AI 子集 8 亿至 15 亿美元；基准：CPO/NPO qualification 拉动，15 亿至 30 亿美元；乐观：多家云厂导入，30 亿至 50 亿美元 | 高。不是最大 TAM，但容易形成瓶颈溢价和高毛利耗材/设备机会 |
| Coherent DCI/scale-across，800ZR/ZR+、1.6T ZR/ZR+ | LightCounting 2026-04：DWDM transceiver 2025 增长 12%，2026-2031 CAGR 13%，800G ZR/ZR+ 受 AI scale-across 拉动，1.6T ZR/ZR+ 在 2028-2029 | 400ZR/800ZR 成熟度高；1.6T ZR+ 仍靠后 | 2026 年 AI scale-across coherent 增量估算 5 亿至 15 亿美元；整体 coherent/DWDM transceiver 为数十亿美元级市场 | 悲观：跨园区训练需求慢，2027 增量低于 10 亿美元；基准：多站点 AI 集群增多，10 亿至 30 亿美元；乐观：800ZR/ZR+ 成 AI DCI 标配，30 亿美元以上 | 中高。Ciena/Cisco Acacia/Marvell/Coherent 受益，但节奏慢于 800G/1.6T 短距 |

## 市场规模和利润池

### 1. 市场规模口径统一

| 市场口径 | 已公开数据，标注日期 | 本报告采用的研究口径 |
| --- | --- | --- |
| Datacom optical components | Cignal AI 2025-05：2025 年收入超过 160 亿美元，主要由 400G/800G 继续增长驱动；1.6T 2025 低于 100 万只 | 作为 2025 高速光互连组件基数 |
| Ethernet optical transceivers | LightCounting 2026-04：2024 增长 93%，2025 估计增长 82%，2026 预计增长 65%；2026 当前需求超过供给约 30%，短缺可能年底缓解 | 用于 2026 估算，得出 250 亿至 280 亿美元级别的高速 datacom/以太网光互连收入 |
| AI cluster optics long-term TAM | LightCounting 2026-03：AI cluster optical interconnect annual sales 有机会在 2030 达 1000 亿美元，但需要多项条件同时满足；基准仍偏 soft landing | 用作长期乐观上限，不作为 2026-2027 基准 |
| CPO direct market | SNS 2026-05：2025 CPO 市场约 0.91 亿美元；360iResearch 2026-06：2025 约 1.01 亿美元、2026 约 1.28 亿美元 | 直接 CPO 产品收入仍小，和股价叙事差距大 |
| Open CPX/NPO/CPO ports | Open CPX/Marvell 2026-05 引用 LightCounting：2025 near/co-packaged ports 少于 100 万，2030 年每年超过 1 亿 ports | 用于判断端口数拐点，而非短期美元收入 |
| Photonics packaging | Yole 公开转述：photonics packaging 市场预计 2031 达 144 亿美元 | Broad market；AI CPO/NPO 只是子集 |
| Silicon photonics | 公开市场报告摘录：2026 市场约 23 亿美元，2035 约 178 亿美元，2026-2035 CAGR 约 25.3% | 用于方向性，不单独作为公司收入预测 |

### 2. 利润池分层

| 层级 | 2026 收入量级 | 当前利润率/价值捕获 | 未来利润率方向 | 核心受益者 |
| --- | --- | --- | --- | --- |
| Switch ASIC、SerDes、optical DSP、retimer/AEC | 数十亿美元至百亿美元级，随 800G/1.6T/102.4T switch 扩张 | 半导体 IP 和高端 ASIC/DSP 毛利通常高于模块组装，软件/telemetry 增强粘性 | 400G/lane、448G、CPO/NPO 使设计门槛继续上升，但 hyperscaler 定制会压价格 | Broadcom、Marvell、NVIDIA、AMD、Credo、MACOM、Semtech |
| InP/EML/PD、VCSEL、UHP/SHP laser、ELS | 2026 约 35 亿至 45 亿美元，CPO/ELS 子集较小 | 当前供给偏紧，激光/材料/器件垂直整合者议价较强 | 2026 年底若短缺缓解，普通器件价格承压；CPO ELS/UHP laser 仍有溢价 | Coherent、Lumentum、Broadcom、IC Photonics、Femtum |
| SiPh PIC、modulator、PD、光引擎 | 2026 SiPh 市场约 20 亿美元级；数据中心 PIC die 子集小于总市场 | 价值取决于量产良率、热控制、封装和测试；纯 IP 议价不稳 | CPO/NPO 推动 optical engine ASP 上行，但标准化会压缩同质化利润 | Marvell、NVIDIA、Broadcom、Lightmatter、imec ecosystem、TSMC、GlobalFoundries、Tower、Intel |
| Pluggable modules、LPO/LRO/TRO/FRO | 2026 最大收入池，约 250 亿美元以上口径的一部分 | 模块组装毛利低于芯片/激光，供给紧时改善；大客户议价强 | 2026 之后 ASP 下行概率上升，靠 1.6T/3.2T mix 对冲 | Coherent、Lumentum、Innolight、Eoptolink、Fabrinet、Cisco/Acacia、Ciena |
| Packaging、substrate、connector、fiber attach、glass/organic substrate | broad photonics packaging 约 45 亿至 55 亿美元；AI CPO 子集低于 10 亿美元 | 特种材料、设备和高可靠连接器毛利通常好于普通组装 | CPO 导入初期利润率上行，标准化后回落；产能/良率决定议价 | AT&S、Ajinomoto、Resonac、DNP、Applied Materials、TEL、Nagase、Corning、SENKO、Sumitomo、Samtec、Molex |
| Optical test、wafer-level validation、ATE integration | 2026 仍是小市场，但增长快 | 高端仪器和测试软件毛利较高，客户验证周期长 | 随 CPO/NPO 进入量产，测试从研发工具转为产线瓶颈 | Keysight、GlobalFoundries test ecosystem、TEL、Applied Materials |

利润池核心变化：在 pluggable 时代，模块厂可通过客户认证和供给紧张获取阶段性超额利润；在 CPO/NPO 时代，超额利润更可能由“能让客户安全量产”的环节获取，包括高可靠 ELS、高功率激光、known-good optical engine、detachable optical connector、wafer-level optical test、低损耗/低 CTE 材料和系统 telemetry。

## 反共识洞见和重要更新

### 1. 过度乐观：把 2026 当成 CPO revenue breakout 年

CPO 的产品新闻非常强，但市场规模还小。直接 CPO 市场公开口径仍约 1 亿美元级别，和高速 datacom optics 250 亿美元以上的 2026 收入口径不在同一数量级。OIP 的 CPO workshop 重点是 manufacturing challenges at scale，而不是宣布行业已经解决 scale manufacturing。对股票研究而言，2026 年 CPO 更像订单/资格认证/供应链锁定年份，收入爆发更可能落在 2027-2029。

反证条件：NVIDIA Quantum-X Photonics 和 Spectrum-X Photonics 在 2026 下半年提前大规模出货，且 Lumentum/Coherent/Corning/Fabrinet/SENKO/SPIL/Sumitomo/TSMC 等供应链给出明确产能扩张和收入确认。

### 2. 被低估：pluggable、LPO/LRO 和 1.6T 的收入持续性

OIP 虽然重度讨论 CPO，但公司材料显示 1.6T/200G/lane 仍是 2026-2027 收入核心。Marvell 1.6T silicon photonics light engine 支持 8x200G PAM4，典型功耗低于 5 pJ/bit；Lumentum 1.6T DR4 OSFP 原型使用 4 个 400G differential EML；Coherent 展示 1.6T/3.2T 和 XPO；Broadcom 400G/lane DSP 也是为了让模块厂做低功耗 1.6T 并铺垫 3.2T。

反证条件：主要云厂明确把 2027 新建 AI fabric 从 1.6T pluggable 大幅切换到 CPO/NPO，且模块采购订单被实质性砍单。

### 3. 被低估：外置光源和高功率激光是 CPO 的战略部件

NVIDIA 对 Coherent 的 20 亿美元投资和采购承诺、一并出现的 Lumentum 交易、Lumentum 的 800mW SHP laser、IC Photonics 在 OIP 的 ELS 演讲，共同说明外置光源不是边缘配件，而是 CPO/NPO 的 uptime、热管理和供应链瓶颈。若 CPO adoption 发生，ELS/laser 的价值捕获可能早于 optical engine 大规模收入。

反证条件：CPO 设计转向低功率分布式片上光源或第三方 laser 充分商品化，导致高功率 ELS ASP 快速下降。

### 4. 被低估：材料/连接器/测试的小公司弹性

OIP 展商只有四家，但 Nagase、Femtum、Optalysys 的出现很说明问题。Nagase 的 LMC、optical bonding、V-groove bonding、dual cure adhesive、water-removable masking resin 是 CPO 量产工艺里的“脏活累活”；Femtum 的 ultrafast laser trimming 指向 silicon photonics tuning power penalty；Optalysys 的 compute-in-transit 属于远期光计算互连线索。市场通常先买模块和光芯片，但 CPO yield ramp 失败时，资金会寻找封装材料、测试和工艺补短板公司。

反证条件：NVIDIA/Broadcom/Marvell/Lightmatter 垂直整合解决大部分材料和测试问题，第三方材料/设备供应商只获得低利润代工式收入。

### 5. 伪受益：只有“硅光/CPO”标签、没有客户认证和封测路径的公司

OIP 出现了 EO polymer、plasmonics、Al2O3、microring、GeSi EAM 等多条器件路线。真正可投的不是实验室指标最高的路线，而是能通过 hyperscaler reliability、温控、封装、测试、产能、供应链二供和现场维护要求的路线。没有客户、没有 foundry/OSAT、没有 high-volume test plan 的“新材料故事”只能当 optionality。

反证条件：某新材料路线获得 NVIDIA/Broadcom/Marvell/Lightmatter/Meta/Microsoft 任一明确 design-in、量产节点和可靠性数据。

### 6. 市场预期差：光互连需求也会经历库存和 capex 周期

LightCounting 2026-04 提醒，当前需求超过供给约 30%，但 InP EML/laser 短缺可能在 2026 年底缓解；供应商扩产之后，双重下单消退和价格下降可能再次出现。AI 光互连不是不会周期化，只是周期驱动从传统电信 capex 变成 GPU/XPU、switch ASIC、HBM/CoWoS 和云厂 capex 联动。

反证条件：GPU/XPU、switch ASIC 和电力容量持续紧缺，使光模块供给即便扩产仍长期不足，ASP 和毛利维持高位。

## 公司和产业链映射

| 公司/机构 | OIP 2026 直接关联 | 会外一手/公开验证 | 研究判断 |
| --- | --- | --- | --- |
| NVIDIA | Tom Gray keynote；Liron Gantz 为 TPC；Dan Kuchta 参与 WS3；主题覆盖 CPO、能效、AI datacenter | Quantum-X Photonics 115Tb/s、144x800G；Spectrum-X Photonics SN6810 102.4Tb/s、SN6800 409.6Tb/s；CPO 3.5x 至 5x power efficiency 口径；2026 进入 availability/production 节点 | 不只是买光器件，而是在定义 CPO 系统架构和供应链；会把利润向通过认证的 laser、fiber、package、manufacturing partners 分配 |
| Broadcom | Farhang Yazdani 技术主席；Marvell/Broadcom 相关 AI/CPO 主题密集出现 | TH6-Davisson 102.4Tbps CPO，16x6.4Tbps optical engines，200Gbps/link，70% optical interconnect power reduction；Gen4 400G/lane CPO roadmap；Taurus 400G/lane DSP | 开放以太网和 CPO 平台主导者之一；受益于 switch ASIC、DSP、VCSEL/NPO、OCI 标准 |
| Marvell | OIP M2 400G SerDes I/O、T2 3D-integrated CPO SiPh、WS3 manufacturing、test 相关讨论 | Ara 3nm 1.6T PAM4 DSP；Photonic Fabric；1.6T SiPh light engine <5pJ/bit；NPO/CPO/scale-up portfolio | 最核心的“连接全栈”公司之一；关键在于从 demo/portfolio 变成 hyperscaler 量产收入 |
| Microsoft | Ram Huggahalli keynote：Transitioning to Optically Connected AI Scale-up Domains | OCI MSA founding member；Azure AI infrastructure 是 optical scale-up 的自然需求方 | 客户验证权重高；若其公开标准/采购路径变化，将改变光互连 TAM 假设 |
| Meta | OIP M1 CPO for AI infrastructure；M2 400G electrical scale-up viability；WS1 energy efficiency | OCI MSA founding member；长期自研 AI infra | Meta 的“400G electrical 是否仍可行”是重要降温信号；其 CPO adoption 取决于 reliability/job interruption economics |
| Oracle | OIP M1 Building Resilient AI Fabrics | OCI cloud 为 NVIDIA Spectrum-X Photonics first adopter 页面列名 | 关注 resilient fabric、link flap、可维护性，供应商需给出 uptime 证据 |
| Lightmatter | OIP WS3：From Pluggables to Co-Packaged, Scaling SiPh HVM for CPO | 2026-03 发起 OCP CPO reference architecture initiative；强调 known-good engines、fiber attach、assembly/test | 是 CPO 量产方法论的重要观察窗口；更接近系统/封装问题而非单纯 photonic chip |
| Coherent | 无明显 OIP 主会演讲，但与 OIP 主题高度相关 | OFC 2026 展示 400G/lane、3.2T、12.8T+ XPO、CPO、1.6T transceivers；NVIDIA 20 亿美元投资和采购承诺 | 垂直材料/器件/模块/系统能力强，受益于 laser/EML/VCSEL/InP-on-silicon 和 3.2T |
| Lumentum | OIP WS1 VCSEL wide-parallel；W1 passive components for SiPh IMDD chipsets and wafer-level test | OFC 2026：1.6T DR4 OSFP with 400G differential EML；800mW SHP laser；16-channel DWDM UHP laser；VCSEL scale-up demo | 受益点从 telecom laser 扩到 AI CPO/VCSEL/1.6T；核心看 NVIDIA 供应份额、laser capacity 和 operating margin |
| Ciena | Open CPX founding member；coherent DCI 相关 | Open CPX MSA；800ZR/ZR+ 和 coherent scale-across 受 AI 多园区训练拉动 | 不是 OIP 中心公司，但在 scale-across/CPX 标准中有位置 |
| Cisco/Acacia | OIP co-chair Jock Bovington；Cisco 光互连/封装背景 | Cisco 2025 optics deck 显示 AI back-end switch ports 2025 以 800G 为主、2027 进入 1600G；Acacia coherent | Cisco/Acacia 受益于 800G/1.6T optics 和 coherent DCI，但 CPO 节奏可能更谨慎 |
| Arista | 未见 OIP 直接核心演讲 | XPO MSA 由 Arista 组织的媒体报道线索；AI Ethernet 网络受益 | 受益于 AI Ethernet fabric，但未必直接捕获 optical component 超额利润 |
| Credo、MACOM、Semtech | 未见 OIP 直接核心演讲 | 高速 DSP、retimer、AEC、TIA/CDR、linear/retimed connectivity 相关 | 作为 200G/lane、LPO/LRO/AEC 和 electrical pathfinding 受益者跟踪；需用订单和客户认证验证 |
| TSMC | NVIDIA CPO partner；Broadcom TH6-Davisson 使用 TSMC COUPE 公开口径 | TSMC SoIC/COUPE 支撑 silicon photonics 与 3D stacking | 最底层制造平台，价值大但难以单独从光互连主题拆分 |
| Intel | OIP WS2 Scaling CPO with advanced packaging | 硅光和先进封装长期布局 | 可能在 foundry/packaging/客户 CPO 项目中受益，但需具体 design win |
| GlobalFoundries | OIP W1 chair；WS3 photonic test parallelism | 硅光代工和测试生态 | 关注 wafer-level photonic test、SiPh PDK、CPO customer tape-out |
| Tower Semiconductor | OIP 未见直接演讲 | 硅光/SiGe/analog foundry 能力相关 | 仅作为 SiPh foundry watchlist，未由 OIP 直接验证 |
| AT&S、Ajinomoto、Resonac、DNP、Applied Materials、TEL、Nagase | OIP WS2/WS3 和展商材料直接出现 | 材料、基板、玻璃、WFE、bonding、封装可靠性 | 是本届 OIP 最值得增加权重的上游瓶颈组合 |
| Keysight | OIP M2 400Gbps measurement；WS3 wafer-level PIC validation | 448G/3.2T AI networking testing 相关材料 | 测试需求从实验室走向量产，若 CPO/NPO ramp，Keysight 类工具链价值上升 |
| Optalysys | OIP 展商和 W2 compute-in-transit talk | 光计算/compute-in-transit | 远期 optionality，短期不纳入核心收入预测 |

## 风险、反证条件和后续跟踪

1. GPU/XPU 和 switch ASIC 约束会反向限制光互连需求。LightCounting 指出 2026 年 AI cluster 扩张仍可能受 XPU 和 switch ASIC 短缺限制；如果 GPU 供应或电力/机房建设出问题，光模块订单也会同步调整。

2. 供给缓解后 ASP 和毛利可能回落。InP EML/laser 短缺若在 2026 年底缓解，双重下单消退会带来价格压力。高增长不等于高利润永久化。

3. CPO 的 field service 模型仍是核心风险。Pluggable 的优势是可替换、供应商灵活和生态成熟；CPO 需要证明 failure isolation、fiber attach、laser replacement、link flap、液冷/热管理和现场维护成本可接受。

4. 标准碎片化可能拖慢 adoption。OCI、Open CPX、OCP CPO、UEC、UALink、NVLink、ESUN、PCIe/CXL over optics 并行推进。短期有利于创新，长期也可能造成供应链重复认证和客户观望。

5. 新材料路线的可靠性和温控是硬门槛。EO polymer、plasmonics、MRM、Al2O3、GeSi FK EAM 都有潜力，但 hyperscaler 需要多年级稳定性、温度窗口、良率和可测试性；没有可靠性数据的材料故事应降权。

6. 非官方材料不能单独支撑结论。LinkedIn、YouTube、论坛和媒体会后纪要可用于发现线索，但核心判断必须回到 OIP 官方日程、公司公开材料、标准/联盟文件和可复核市场数据。

7. 估值风险很高。2026 上半年光互连股票已被 NVIDIA 采购承诺、CPO 叙事和 1.6T 放量推高；如果夏季缺少催化剂、CPO adoption 延后或 1.6T ASP 下修，股价可能先于基本面回撤。

后续跟踪清单：

| 跟踪项 | 判断意义 | 触发信号 |
| --- | --- | --- |
| OIP 论文/摘要是否公开进入 IEEE Xplore | 验证 talk 是否有可复核技术细节 | 212Gbps O-band DWDM microring、400G electrical、Ge/Si EAM、wafer-scale assembly 的论文公开 |
| NVIDIA Quantum-X/Spectrum-X Photonics 出货 | 验证 CPO 是否进入真实产线 | 系统厂 SKU、交付客户、供应链收入确认、CPO field data |
| Broadcom TH6-Davisson early access 转 production | 验证开放以太网 CPO 规模化 | 客户名单、Micas/Celestica/HPE 等系统出货、link flap 数据 |
| Lumentum/Coherent laser capacity | 验证 ELS/laser 是否为瓶颈 | capex、lead time、NVIDIA 采购收入、InP wafer capacity |
| Open CPX/OCI spec 版本和互操作测试 | 验证标准化是否降低 adoption 风险 | spec v1.0、interop demo、成员扩充、云厂采纳 |
| 1.6T module ASP 与出货 | 验证 2026-2027 主收入线 | 1.6T unit shipment、OSFP/DR4/DR8 mix、DSP/EML 份额 |
| 400G/lane 和 448G electrical BER/test | 验证 3.2T 节点提前或延后 | OIF/IEEE CEI-448G、Keysight demo、Broadcom/Marvell/AMD silicon validation |
| CPO/NPO test throughput | 验证 known-good optical engine 经济性 | wafer-level parallelism、ATE integration、seconds-per-device 而非 minutes-per-device |

## 来源清单

| 来源 | 类型/日期 | 使用内容 | 置信度 | 是否被一手材料验证 |
| --- | --- | --- | --- | --- |
| https://oip-conference.org/ | OIP 官网，2026-06 检索 | 会议日期、地点、主题、keynote/chair 信息 | 高 | 是 |
| https://oip-conference.org/program | OIP 官方 program 页，2026-06 检索 | 公开日程入口、展商目录、registration 信息 | 高 | 是 |
| https://www.engr.colostate.edu/~mnikdast/files/papers/OIP/OIP26_DetProgram.pdf | OIP 官方详细日程 PDF，2026-06 | 三天 session、keynote、workshop、talk title、speaker/company | 高 | 是 |
| https://oip-conference.org/paper-submission-1 | OIP 官方 CFP，2026-03/04 | 12 个征稿主题、IEEE Xplore proceedings、submission/acceptance dates | 高 | 是 |
| https://www.engr.colostate.edu/~mnikdast/files/papers/OIP/NAGASE_OIP.pdf | OIP 展商材料，2026-06 | LMC、optical bonding、V-groove bonding、可靠性条件 | 高 | 是 |
| https://www.engr.colostate.edu/~mnikdast/files/papers/OIP/FEMTUM_OIP.pdf | OIP 展商材料，2026-06 | Femtum 作为 ultrafast laser trimming/CPO 线索 | 中 | 部分，OIP 日程验证 |
| https://www.engr.colostate.edu/~mnikdast/files/papers/OIP/OPTALYSYS_OIP.pdf | OIP 展商材料，2026-06 | Optalysys 光计算/compute-in-transit 线索 | 中 | 部分，OIP 日程验证 |
| https://www.imec-int.com/en/events/ieee-optical-interconnects-and-packaging-oip-conference | 公司/研究机构一手材料，2026-06 | imec OIP 题目：Ge/Si APD、GeSi FK EAM、400G/lane fast-narrow CPO、3D Optical I/O wide-slow | 高 | 是 |
| https://lightmatter.co/event/optical-interconnect-and-packaging-conference/ | 公司一手材料，2026-06 | Lightmatter OIP talk：CPO HVM、known-good optical engine、detachable fiber attach、assembly/test | 高 | 是 |
| https://lightmatter.co/press-release/lightmatter-announces-reference-architecture-initiative-with-industry-leaders-in-the-open-compute-project-for-co-packaged-optics/ | 公司一手材料，2026-03-16 | OCP CPO reference architecture initiative、参与生态 | 高 | 是 |
| https://www.nvidia.com/en-us/networking/products/silicon-photonics/ | 公司产品页，2026-06 检索 | NVIDIA Quantum-X/Spectrum-X Photonics、CPO benefits、partners、first adopters | 高 | 是 |
| https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Spectrum-X-Photonics-Co-Packaged-Optics-Networking-Switches-to-Scale-AI-Factories-to-Millions-of-GPUs/default.aspx | 公司新闻稿，2025-03 | 100/400Tbps Spectrum-X Photonics、144x800G Quantum-X、生态伙伴、availability | 高 | 是 |
| https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/ | 公司技术博客，2025-08 | 115Tb/s、SN6810 102.4Tb/s、SN6800 409.6Tb/s、3.5x power efficiency、10x resiliency、availability | 高 | 是 |
| https://developer.nvidia.com/blog/scaling-power-efficient-ai-factories-with-nvidia-spectrum-x-ethernet-photonics/ | 公司技术博客，2026-01-06 | 512-lane 200G architecture、5x power reduction per 1.6Tb/s port、detachable fiber connector、100% yield claim | 高 | 是 |
| https://nvidianews.nvidia.com/news/nvidia-and-coherent-announce-strategic-partnership-to-develop-optics-technology-to-scale-next-generation-data-center-architecture | 公司新闻稿，2026-03-02 | NVIDIA 对 Coherent 20 亿美元投资、采购承诺、capacity rights | 高 | 是 |
| https://www.coherent.com/news/press-releases/nvidia-and-coherent-announce-strategic-partnership | 公司新闻稿，2026-03-02 | Coherent 与 NVIDIA partnership 同源验证 | 高 | 是 |
| https://www.coherent.com/news/press-releases/coherent-ai-scale-optical-innovations-ofc-2026 | 公司新闻稿，2026-03-17 | Coherent OFC 2026：400G/lane、3.2T、12.8T+ XPO、CPO、1.6T transceivers | 高 | 是 |
| https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx | 公司新闻稿，2026-03-17 | Lumentum 1.6T DR4 OSFP、400G differential EML、800mW SHP laser | 高 | 是 |
| https://www.lumentum.com/en/events/ofc-2026 | 公司 event recap，2026-03 | Lumentum OFC 2026 demos、视频、新闻稿入口 | 高 | 是 |
| https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Showcases-Breakthrough-Optical-Scale-Up-Demonstration-at-OFC-2026-Using-VCSEL-Technology/default.aspx | 公司新闻稿，2026-03-17 | 1060nm VCSEL array、fan-out wafer-level package、UCIe/PCIe slow-wide scale-up | 高 | 是 |
| https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai | 公司新闻稿，2026-03-12 | Broadcom OFC 2026：3.5D XDSiP、102.4T CPO、400G/lane optical DSP、VCSEL NPO、OCI | 高 | 是 |
| https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-tomahawkr-6-davisson-industrys-first-1024 | 公司新闻稿，2025-10-08 | TH6-Davisson：102.4Tbps、16x6.4Tbps optical engines、200Gbps/link、70% power reduction、512 scale-up nodes | 高 | 是 |
| https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-third-generation-co-packaged-optics-cpo | 公司新闻稿，2025-05-15 | Broadcom Gen3 200G/lane CPO、Gen4 400G/lane roadmap、ecosystem milestones | 高 | 是 |
| https://www.marvell.com/company/newsroom/marvell-ai-data-center-connectivity-ofc-2026.html | 公司新闻稿，2026-03-12 | Marvell OFC 2026：Ara T、Ara 1.6T DSP、Photonic Fabric、Teralynx、COLORZ | 高 | 是 |
| https://www.marvell.com/company/newsroom/marvell-co-packaged-optics-architecture-custom-ai-accelerators.html | 公司新闻稿，2025-01-06 | Marvell custom XPU + CPO、3D SiPho engine、100x reach、10B device-hours | 高 | 是 |
| https://www.marvell.com/company/newsroom/marvell-demonstrates-silicon-photonics-light-engine-for-low-power-rack-scale-interconnect-in-ai-networks.html | 公司新闻稿，2025-03-31 | 1.6T SiPh light engine、8x200G、<5pJ/bit、LPO/CPO foundation | 高 | 是 |
| https://www.marvell.com/blogs/why-scale-up-ai-networks-demand-scalable-optical-test.html | 公司技术博客，2026-05 | 光测试从低量/单站/分钟级转向 IC-style parallelism | 高 | 是 |
| https://www.marvell.com/blogs/scale-up-network-solutions-for-ai-infrastructure.html | 公司技术博客，2026-05-06 | Marvell scale-up network portfolio、CPC/NPO/CPO、Photonic Fabric、multiple foundries/OSAT | 高 | 是 |
| https://www.marvell.com/blogs/open-cpx-msa-flexible-scalable-connectivity.html | 公司技术博客，2026-05-28 | Open CPX、2025 <1M near/co-packaged ports、2030 >100M ports 引用 | 中高 | Open CPX 官网验证 |
| https://oci-msa.org/ | 标准/联盟官网，2026-03 | OCI MSA founding members、NRZ+WDM、silicon-centric optical scale-up objectives | 高 | 是 |
| https://www.opencpxmsa.org/ | 标准/联盟官网，2026-03-12 | Open CPX founding members、mechanical/thermal/electrical/optical/management specs、>100M ports quote | 高 | 是 |
| https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382 | 市场研究公开摘录，2026-03 | AI cluster optics 2030 $100B 上限、2026 optical transceiver growth only 60%、100+ product categories | 中高 | 非公司一手；与 Cignal/公司材料交叉 |
| https://www.lightcounting.com/newsletter/en/april-2026-market-forecast-379 | 市场研究公开摘录，2026-04 | 2024/2025/2026 Ethernet transceiver growth、InP laser shortage、DWDM 13% CAGR | 中高 | 非公司一手；与公司材料交叉 |
| https://cignal.ai/2025/05/800gbe-optics-shipments-to-grow-60-in-2025/ | 市场研究公开摘录，2025-05 | 2025 datacom optical component >$16B、1.6T <1M units、CPO 3 年内不显著影响 pluggables | 中高 | 非公司一手；与 LightCounting 交叉 |
| https://www.ciscolive.com/c/dam/r/ciscolive/global-event/docs/2025/pdf/BRKOPT-2699.pdf | 公司技术材料，2025 | AI backend ports 2025 800G、2027 1600G、pluggable advantages、AI rack bandwidth/power变化 | 中高 | Cisco 材料 |
| https://blogs.sw.siemens.com/semiconductor-packaging/2026/02/05/five-key-trends-of-co-packaged-optics-cpo-in-2026/ | 产业技术博客，2026-02 | CPO 2026 trends、LightCounting laser/PIC $2.4B to $5.9B quote、1.6T CPO 30W to 9W claim | 中 | 作为二手辅助，不单独支撑核心结论 |
| https://www.snsinsider.com/reports/co-packaged-optics-market-8328 | 市场报告公开摘录，2026-05 | 2025 CPO market $91.27M、2035 $1.92B | 中 | 与 360iResearch/Open CPX 交叉 |
| https://www.360iresearch.com/library/intelligence/co-packaged-optics | 市场报告公开摘录，2026-06 | 2025 CPO $101.14M、2026 $127.85M、2032 $526.94M | 中 | 与 SNS/Open CPX 交叉 |
| https://www.photonics.com/Articles/Yole-Report-Calls-for-Photonics-Packaging-Market/a72129 | 媒体转述 Yole，2026 | Photonics packaging 2031 $14.4B | 中 | 作为市场口径，不作为精确预测 |
| https://www.optica.org/events/global_calendar/events/optical_interconnects_and_packaging_%28oip%29_conference/ | Optica event page，2026 | OIP endorsed by Optica、日期地点 | 高 | OIP 官网交叉 |
| LinkedIn：Ali Ghiasi、Mahdi Nikdast 等 OIP 2026 posts | 非官方/组织者社交线索，2026-05 至 2026-06 | 会议小型、single-track、highly interactive、参会情绪 | 低至中 | 仅作线索；核心事实用 OIP 官网验证 |
| YouTube/公司视频：NVIDIA CPO video、Lumentum OFC videos、Coherent OFC demo videos、Marvell OFC 2026 video | 公司/公开视频，2026 | 产品演示线索 | 中 | 未作为核心定量依据，仅辅助判断 |

