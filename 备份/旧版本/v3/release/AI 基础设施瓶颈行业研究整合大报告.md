

# **AI 基础设施瓶颈行业研究整合大报告**

## **小组件、小材料、小设备、AI 工厂技术栈与未来 6–24 个月增长路径**

---

# **1\. 报告口径与核心判断**

本报告关注的不是“AI 芯片整机”或“GPU 公司股价”，而是 AI 基础设施扩张过程中真正容易形成瓶颈、且增速可能明显高于母行业的小组件、小材料、小设备和小产品线。增长判断指的是相关产品线的收入、订单或 run-rate 增长，不代表整家公司收入增长，也不代表股价预测。

**AI 基建的约束正在从单颗 GPU 算力，迁移到 HBM、先进封装、测试、光互连、铜互连、电源、液冷、AI-native storage、CXL memory pooling、OCS/CPO、SOCAMM2 内存形态和 AI 工厂调度软件。**

短期 6–12 个月，最值得跟踪的是：

| 优先级 | 方向 | 关键小组件 / 小产品 |
| ----- | ----- | ----- |
| 1 | Rubin / Vera CPU 内存形态 | SOCAMM2 模块、SOCAMM2 compression connector、retention hardware、test socket、thermal pad |
| 2 | HBM4 放量 | HBM4 base die、HBM4 probe card、HBM memory tester、burn-in socket、thermal head、underfill |
| 3 | 1.6T 光互连 | 1.6T optical DSP、224G SerDes、200G EML、CW laser、optical engine、active alignment |
| 4 | OCS / CPO | MEMS mirror、fiber collimator、external laser source、SiPh PIC、wafer-level optical test |
| 5 | 高速铜互连 | AEC controller、active copper cable、twinax、retimer、scale-up fabric switch |
| 6 | 先进封装检测 | CoWoS-like AOI、micro-bump inspection、warpage metrology、X-ray / SAM |
| 7 | 液冷可靠性件 | cold plate、CDU、QD、seals、leak sensor、coolant chemistry、commissioning service |
| 8 | AI 电源 | Z-axis power、high-current VRM、48V power shelf、busbar、blind-mate connector |
| 9 | 中期技术期权 | CXL switch、memory pooling、eDTC、silicon capacitor、glass-core substrate、TGV inspection |

一句话概括：

**短期看 SOCAMM2、1.6T 光、AEC、HBM4 测试、CoWoS-like 检测、液冷可靠性件；中期看 custom HBM base die、CPO 外置激光源、SiPh 测试、eDTC / 硅电容、玻璃基板、CXL memory pooling。**

# **2\. 需求底盘：AI 芯片与机柜架构变化**

## **2.1 公开锚点与小组件映射**

| 平台 / 事件 | 公开或项目内整理数据 | 对小组件的直接拉动 |
| ----- | ----- | ----- |
| NVIDIA Vera Rubin NVL72 | 单柜包含 72 个 Rubin GPU、36 个 Vera CPU、20.7TB HBM4、54TB LPDDR5X、ConnectX-9、BlueField-4、NVLink 6 | 20.7TB HBM4 拉动 HBM4 stack、probe、underfill、TCB、HBM tester；54TB LPDDR5X 拉动 SOCAMM2 模块和连接器；rack-scale 网络拉动 1.6T / CPO / OCS / AEC |
| Rubin GPU | 最高 288GB HBM4、22TB/s HBM 带宽、NVFP4 inference 50 PFLOPS、training 35 PFLOPS | 每颗 GPU 的 HBM4 stack 数、HBM4 I/O、封装复杂度、测试复杂度显著提升 |
| Vera CPU | 88 个 Olympus cores，Arm v9.2，SOCAMM \+ LPDDR5X，1.2TB/s 内存带宽，1.5TB 容量 | SOCAMM2 从移动 / 模块形态演进为 AI server CPU 内存形态，连接器、扣具、热件、测试夹具新增需求 |
| AMD MI450 / Helios | 单 MI450 432GB HBM4、19.6TB/s；Helios 72-GPU rack 约 31TB HBM4、1.4PB/s HBM 带宽、260TB/s scale-up | MI450 单颗 HBM 容量更高，对 HBM4 stack、TCB、probe、tester、液冷、电源、scale-up fabric 拉动更强 |
| Oracle 50,000 颗 MI450 | 从 2026 Q3 起部署 50,000 颗 MI450 | 粗算对应约 45–60 万个 HBM4 stack |
| OpenAI / AMD 1GW MI450 | 首个 1GW MI450 部署从 2026 H2 开始 | 按 120–200kW / rack 粗估，约 5,000–8,333 个 72-GPU rack，对应约 36–60 万颗 GPU |
| Meta / AMD 1GW MI450 | 2026 H2 开始 | 对 HBM4、液冷、电源、scale-up 网络形成多客户放量验证 |
| AWS Trainium3 | Trn3 UltraServer 可扩展到 144 颗 Trainium3，整机 20.7TB HBM3E、706TB/s 聚合带宽 | 非 NVIDIA ASIC 也大量消耗 HBM3E、tester、SoC final test、scale-up fabric、液冷、电源 |
| Google TPU | 项目内整理提到 Google TPU 2026 年出货可能达到数百万颗量级 | TPU 量级使 HBM、先进封装、OCS、光交换、液冷、电源不再是 NVIDIA 专属需求 |
| Microsoft Maia 200 | TSMC 3nm、216GB HBM3E、7TB/s、272MB SRAM、750W TDP | 拉动 HBM3E、SRAM / data movement、液冷、AI power、SerDes test |
| Anthropic / TPU | 最高使用 100 万颗 Google TPU，并有多 GW 下一代 TPU 容量规划 | 使 HBM、advanced packaging、OCS / 光交换、液冷和电源进入超大规模部署 |
| Lumentum OCS / CPO | OCS backlog 超过 4 亿美元，CPO multi-hundred-million-dollar 订单，2027 H1 交付 | OCS 内部 MEMS mirror、fiber collimator、FAU、optical alignment、control plane；CPO 内部 ELS / CW laser、SiPh PIC、wafer optical test 放量 |

---

## **2.2 AI accelerator 出货工作模型**

项目内第二份文件给出了一个工作模型，用于反推小组件需求弹性。这个模型不是精确预测芯片出货，而是为了估算 HBM stack、test socket、probe card、光口、液冷点、电源模块的需求倍数。

| 年份 | NVIDIA 高端 GPU | CSP ASIC：Google / AWS / Meta / Microsoft | AMD MI400 / MI450 | 中国 / 其他 AI 卡 | HBM-backed advanced accelerator 合计 | HBM stack attach 粗估 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 2026E | 7–9M | 5.8–6.2M | 0.3–0.5M | 2–3M，中国卡 HBM 强度较低 | 13–15M | 100–130M stack |
| 2027E | 9–13M | 7–9M | 0.8–1.5M | 3–5M | 18–25M | 140–210M stack |
| 2028E | 11–16M | 10–14M | 1.2–2.5M | 3.5–6M | 24–33M | 180–280M stack |

HBM stack attach 的假设是：

| 平台 | HBM stack attach 粗略假设 |
| ----- | ----- |
| NVIDIA Rubin | 约 8 stack / GPU |
| AMD MI450 | 约 9–12 stack / GPU，取决于 36GB / 48GB HBM4 stack |
| Google TPU / Ironwood 类平台 | 约 4–8 stack / TPU |
| AWS Trainium3 | 约 4 stack / chip |
| Microsoft Maia 200 | 约 6 stack / chip |
| Meta MTIA | 约 6–8 stack / chip |

关键结论：

**很多小组件增长不是由 AI 芯片颗数单独决定，而是由 HBM stack 数、内存模块数、端口数、冷却点数、测试工时、封装面积和电流密度共同决定。**

---

# **3\. NVIDIA GTC 2026 技术栈：AI 工厂完整产品化**

第三份文件的核心不是“NVIDIA 又发布了下一代 GPU”，而是：

**NVIDIA 第一次把 AI 工厂完整产品化。**

它把 compute、memory、networking、storage、runtime、digital twin、power、cooling、agent workloads 全部放进一个统一架构里。

---

## **3.1 官方正式发布层级**

| 层级 | 发布内容 | 对产业链的意义 |
| ----- | ----- | ----- |
| 图形 / 基础设施 | DLSS 5、Vera Rubin 平台、BlueField-4 STX、Vera CPU、Vera Rubin DSX AI Factory reference design、Omniverse DSX Blueprint、Space Computing、Dynamo 1.0 | 把 GPU、CPU、DPU、AI storage、AI factory simulation、distributed inference OS 打成整体 |
| 模型 / agent | NemoClaw for OpenClaw、Expanded Open Model Families、Nemotron Coalition、Open Agent Development Platform、Agent Toolkit、Open Physical AI Data Factory Blueprint | 用 agent、长上下文、多步 reasoning、physical AI 持续制造 compute / memory / storage 需求 |
| 行业落地 | DRIVE Hyperion L4、T-Mobile AI-RAN、Adobe Firefly / Omniverse、Hyundai / Kia、Industrial Software Giants、Global Robotics Leaders | 把 AI 工厂需求从训练扩展到机器人、自动驾驶、电信边缘、创意工作流、工业软件 |

第三份文件的强判断：

**这不是单点 FLOPS 升级，而是 token 成本、token / 瓦、长上下文、低时延、供电和 time-to-revenue 的系统级发布。**

---

## **3.2 Vera Rubin 平台：七颗芯片、五类机架、一个 AI 超算**

Vera Rubin 平台不是单颗芯片，而是整平台。

| 组成 | 内容 |
| ----- | ----- |
| 芯片层 | Vera CPU、Rubin GPU、NVLink 6 Switch、ConnectX-9 SuperNIC、BlueField-4 DPU、Spectrum-6 Ethernet switch、Groq 3 LPU |
| 机架层 | Vera Rubin NVL72 GPU racks、Vera CPU racks、Groq 3 LPX inference racks、BlueField-4 STX storage racks、Spectrum-6 SPX Ethernet racks |
| 云 / OEM 伙伴 | AWS、Google Cloud、Azure、OCI、CoreWeave、Crusoe、Lambda、Nebius、Nscale、Together AI；Cisco、Dell、HPE、Lenovo、Supermicro、ASUS、Foxconn、Inventec、Pegatron、QCT、Wistron、Wiwynn 等 |
| 供货节奏 | Rubin-based products 从 2026 年下半年开始由伙伴提供 |

Rubin GPU 关键规格：

| 指标 | Rubin GPU |
| ----- | ----- |
| 晶体管 | 3360 亿 |
| SM | 224 个 |
| Tensor Core | 第五代 |
| NVFP4 inference | 50 PFLOPS |
| NVFP4 training | 35 PFLOPS |
| HBM4 容量 | 最高 288GB |
| HBM 带宽 | 22TB/s |
| NVLink 6 per GPU | 3.6TB/s all-to-all |
| NVL72 scale-up | 260TB/s |

系统级口径：

| 对比 Blackwell | Rubin NVL72 厂商口径 |
| ----- | ----- |
| 长上下文 / 推理型负载 | 最高 10 倍 inference throughput / MW |
| 训练大规模 MoE 模型 | GPU 数量可降至四分之一 |
| token 成本 | 压到十分之一 |

关键判断：

**Rubin 不是 Blackwell 的顺序升级，而是 NVIDIA 从 GPU 公司向 AI Factory 主承包商跨出的一步。**

---

## **3.3 Vera CPU：AI 控制平面，而不是普通 CPU 战争**

Vera CPU 不是传统意义上对 Intel / AMD 通用 CPU 的线性竞争，而是 AI 工厂控制平面的产品化。

| 指标 | Vera CPU |
| ----- | ----- |
| CPU core | 88 个 Olympus cores |
| 指令架构 | Arm v9.2 |
| 前端 | 10-wide fetch / decode |
| 分支预测 | neural branch predictor |
| fabric | 第二代 SCF |
| fabric bisection bandwidth | 3.4TB/s |
| 内存形态 | SOCAMM \+ LPDDR5X |
| 内存带宽 | 1.2TB/s |
| 内存容量 | 1.5TB |
| Vera CPU Rack | 256 颗 Vera CPU / rack |
| sandbox | 22.5K+ sandboxes |
| 对 x86 机架口径 | 4 倍容量、2 倍 perf / watt |

Vera CPU 处理的是 GPU 之外、但决定 GPU 利用率的工作负载：

| 工作负载 | 为什么重要 |
| ----- | ----- |
| RL post-training | RLHF / RLAIF / post-training 需要大量 CPU 控制与数据调度 |
| agent sandbox | agent 执行 tool use、browser、代码、模拟环境 |
| tool use | AI agent 与外部工具交互 |
| ETL | 数据清洗和管道 |
| orchestration | 推理集群调度 |
| KV / blob cache | 长上下文推理的缓存与外部 memory tier |

关键判断：

**Vera CPU 的意义不是抢传统 CPU 市场，而是把 AI 工厂里的 CPU 控制平面和内存形态也纳入 NVIDIA 体系。**

---

## **3.4 Groq 3 LPX：低时延异构推理机架**

第三份材料认为 LPX 是最容易被低估的发布之一。

| 指标 | Groq 3 LPX |
| ----- | ----- |
| LPU 数量 | 256 颗 LPU |
| FP8 | 315 PFLOPS |
| 总 SRAM | 128GB |
| on-chip SRAM bandwidth | 40PB/s |
| scale-up bandwidth | 640TB/s |
| 定位 | 面向 agentic AI 的低时延、大上下文 rack-scale inference accelerator |

Rubin GPU 与 LPX 的分工：

| 模块 | 主要工作 |
| ----- | ----- |
| Rubin GPU | prefill、decode attention、长上下文、高并发 |
| LPX | latency-sensitive decode，尤其是 FFN / MoE expert execution |
| STX / CMX | context tier、KV / 长记忆管理 |
| Dynamo | 全局调度和 serving runtime |

推理架构变化：

**未来推理基础设施可能不再是全 GPU 一把梭，而是 GPU 做 attention \+ KV，LPU 做 FFN / MoE，STX / CMX 做 context tier，Dynamo 做全局调度。**

风险：

| 风险 | 解释 |
| ----- | ----- |
| 编译器 | 异构执行需要稳定编译和算子切分 |
| runtime | serving stack 要把 attention、FFN、KV、cache tier 调度起来 |
| 开发者心智 | 应用开发者是否愿意接受新硬件层 |
| 生态融合 | LPX 是否真正成为 NVIDIA 推理栈的一部分，而不是孤立加速器 |

---

## **3.5 BlueField-4 STX / CMX：把 KV cache 问题改写成存储层问题**

STX / CMX 是三份材料中最具“隐形投资价值”的方向之一。

| 指标 / 口径 | STX / CMX |
| ----- | ----- |
| token throughput | 最高 5 倍 |
| energy efficiency | 4 倍 |
| data ingestion | 2 倍 faster |
| 核心概念 | CMX context memory storage |
| 第一代实现 | storage-optimized BlueField-4 \+ Vera CPU \+ ConnectX-9 \+ Spectrum-X \+ DOCA \+ AI Enterprise |

STX / CMX 的逻辑：

| 问题 | 传统做法 | STX / CMX 思路 |
| ----- | ----- | ----- |
| 长上下文推理 | 大量上下文和 KV 放在 HBM 中 | 把 GPU 之外的上下文、KV、长记忆抽成 context tier |
| HBM 成本 | HBM 容量昂贵且供给受限 | 用 AI-native storage / SSD / DPU / CPU / network 做分层 |
| agent memory | 多 agent 需要持久状态 | 用 storage / context memory 管理长期记忆 |
| 推理吞吐 | GPU 容易被 KV 和 memory traffic 卡住 | 通过 STX / CMX 提升 token throughput |

供应链相关方：

| 层级 | 公司 / 伙伴 |
| ----- | ----- |
| 存储软件 / 系统 | Cloudian、DDN、Dell、Hitachi Vantara、HPE、IBM、MinIO、NetApp、Nutanix、VAST、WEKA |
| 制造侧 | AIC、Supermicro、QCT |
| 首批采用者 | CoreWeave、Crusoe、IREN、Lambda、Mistral、Nebius、OCI、Vultr |
| SSD | Micron 9650 PCIe Gen6 SSD 对准 BlueField-4 STX |

核心判断：

**如果长上下文、多 agent、persistent memory 是真需求，AI-native storage 会从配角变成未来两三年非常重要的一层 attach。**

---

## **3.6 Spectrum-6、ConnectX-9、CPO：瓶颈迁移到网络**

Spectrum-6 与 CPO 的重点不是“又一代交换机”，而是 AI 工厂的 east-west traffic、光功耗、可维护性和规模化制造。

| 指标 | Spectrum-6 / CPO |
| ----- | ----- |
| switching capacity | 102.4Tb/s |
| port | 512 × 200Gb/s |
| silicon photonics engines | 32 个 |
| 每个 engine | 3.2Tbps |
| ConnectX-9 per GPU scale-out | 1.6Tb/s |
| CPO 工艺 | 与 TSMC 合作解决 micro-ring modulator 制造问题 |
| modulation | 200Gbps PAM4 per wavelength |
| laser 架构 | field-replaceable external laser source |
| laser 数量 | 减少到传统方案四分之一 |

系统收益口径：

| 指标 | Spectrum-X Ethernet Photonics 厂商口径 |
| ----- | ----- |
| power efficiency | 5 倍 |
| application uptime | 5 倍 |
| reliability | 10 倍 |

关键小组件：

| 方向 | 小组件 |
| ----- | ----- |
| CPO | external laser source、CW laser、laser redundancy module |
| SiPh | SiPh PIC、micro-ring modulator、optical engine substrate |
| 光测试 | wafer-level optical probe、electro-optical test、active alignment |
| 光耦合 | FAU、fiber attach、lens array、collimator |
| 光交换 | OCS MEMS mirror、fiber collimator、control board |

核心判断：

**NVIDIA 已经默认 AI 工厂的关键瓶颈不再是裸算力，而是 network bandwidth、signal integrity、optical power 和 serviceability。**

---

## **3.7 800VDC / Kyber：供电成为系统级瓶颈**

第三份文件把 800VDC 放到了很重要的位置。

| 指标 / 设计 | 内容 |
| ----- | ----- |
| 目标 | 超 1MW / rack 的未来机架 |
| 架构 | Kyber rack architecture |
| 电压 | 800VDC |
| 节点侧转换 | 64:1 LLC converter |
| 转换目标 | 从高压直接降到 12V |
| 面积优势 | 比传统多级方案少 26% |
| 生态伙伴 | ADI、Infineon、Navitas、onsemi、Renesas、TI、Delta、Flex、LITEON、ABB、Eaton、GE Vernova、Hitachi Energy、Schneider、Siemens、Vertiv 等 |

供电瓶颈对应的小组件：

| 小组件 | 增长逻辑 |
| ----- | ----- |
| high-current VRM | XPU core、HBM rail、多电压域供电，电流密度提升 |
| Z-axis / vertical power module | board-level PDN 损耗过高，电源需要靠近 package |
| 48V intermediate bus converter | rack-level 48V 配电与 tray 高电流供电 |
| busbar | 高电流低损耗连接 |
| blind-mate power connector | AI tray 快速维护和高可靠连接 |
| eFuse / protection | 高功率 AI rack 电源保护复杂度上升 |
| power choke / inductor | 相数、电流密度、效率要求提升 |

核心判断：

**2026–2027 年真正的执行风险不在 GPU 设计，而在 HBM4 供给、先进封装、CPO 良率、液冷装配和 HVDC 改造速度。**

---

## **3.8 DSX / DSX Air / Dynamo：AI 工厂软件层**

### **DSX**

DSX reference design \+ Omniverse DSX Blueprint 的本质，是 NVIDIA 抢 AI 工厂 EPC、digital twin 和 power orchestration 的主导权。

| DSX 子系统 | 作用 |
| ----- | ----- |
| DSX Max-Q | 固定功率下最大化 AI infrastructure |
| DSX Flex | grid-flex 和电力弹性 |
| DSX Exchange | 工厂级资源调度与交换 |
| DSX Sim | AI factory simulation |

厂商口径：

| 指标 | DSX |
| ----- | ----- |
| 固定功率下 AI 基础设施 | 可部署 30% 更多 |
| stranded grid power | 解锁 100GW |
| 目标 | 最大化 tokens per watt 和 time to first production |

### **DSX Air**

| 指标 | DSX Air |
| ----- | ----- |
| 形态 | SaaS 化 AI factory logical simulation |
| 仿真内容 | compute、networking、storage、orchestration、security |
| 作用 | 服务器拆箱之前先把 AI factory 逻辑跑通 |
| 时间收益 | 部署从 months to days，time-to-first-token 从 weeks / months 缩到 days / hours |

### **Dynamo 1.0**

Dynamo 是 NVIDIA 对推理 runtime / cluster OS 的布局。

| 指标 | Dynamo |
| ----- | ----- |
| 定位 | AI factory distributed operating system |
| 推理性能口径 | Blackwell 推理性能最高提升 7 倍 |
| 关键模块 | KVBM、NIXL、Grove |
| 集成框架 | LangChain、llm-d、LMCache、SGLang、vLLM |

核心判断：

**DSX 在抢 AI 工厂建设和运营层，Dynamo 在抢推理 runtime 和 cluster OS 层。一旦 attach rate 上来，NVIDIA 的商业模式会从卖硬件变成对工厂建设、工厂运营和工厂调度同时收租。**

---

# **4\. 第一组瓶颈：SOCAMM2 生态**

SOCAMM2 是两份行业研究中反复强调的新线索。它不是传统 DIMM 的小升级，而是 Rubin / Vera CPU 侧的新内存形态。

Vera Rubin NVL72 单 rack 有 54TB LPDDR5X。若用 192GB SOCAMM2 模块，粗估约：

**54TB / 192GB ≈ 288 个 SOCAMM2 模块 / rack。**

这意味着每个 rack 不只消耗 GPU 和 HBM，还会消耗大量 SOCAMM2 模块、压接连接器、扣具、导向件、热件和测试夹具。

---

## **4.1 SOCAMM2 组件拆解**

| 小组件 / 产品 | 未来半年年化 | 未来一年 | 未来两年年化 | 增长逻辑 | 相关公司与上市地 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| SOCAMM2 module | 100–250% | 100–200% | 60–120% | Vera Rubin NVL72 的 54TB LPDDR5X 是直接需求；Micron 192GB / 256GB、SK hynix 192GB SOCAMM2 进入量产或高产阶段 | Micron：NASDAQ MU；SK hynix：KRX 000660；Samsung：KRX 005930 |
| SOCAMM2 compression connector | 120–300% | 100–220% | 60–130% | 每个 SOCAMM2 模块至少对应一组压接连接界面；NVL72 单 rack 粗估约 288 个 SOCAMM2 模块 | Amphenol：NYSE APH；TE Connectivity：NYSE TEL；Molex：Koch 旗下未上市；JAE：东京 6807；Hirose：东京 6806；LOTES / 嘉泽：台湾 3533 |
| SOCAMM2 retention / stiffener / guide frame / screw-down hardware | 120–300% | 80–200% | 50–120% | CAMM / SOCAMM 是压接式可维护模块，需要定位、锁附、压力均匀和抗翘曲结构 | LOTES：台湾 3533；Foxconn Interconnect：港交所 6088；Amphenol：APH；TE：TEL；Molex：未上市；JAE：6807 |
| SOCAMM2 test socket / module test fixture | 80–180% | 80–160% | 50–110% | 新服务器内存模块形态，需要独立模块测试夹具、burn-in socket、high-speed test board | Cohu：NASDAQ COHU；Enplas：东京 6961；Yamaichi：东京 6941；FormFactor：NASDAQ FORM；Chroma ATE：台湾 2360 |
| SOCAMM2 heat spreader / thermal pad / module TIM | 80–180% | 70–150% | 40–100% | LPDDR5X 高密度布置在液冷 AI rack 内，导热垫、heat spreader、retention pressure 控制变重要 | Laird / DuPont：NYSE DD；Henkel：Xetra HEN3；Shin-Etsu：东京 4063；Honeywell：NASDAQ HON；Auras：台湾 3324 |

---

## **4.2 SOCAMM2 的关键判断**

SOCAMM2 模块本身会被市场注意，但更隐形的高增长来自：

| 高弹性部件 | 为什么弹性大 |
| ----- | ----- |
| compression connector | 从新规格到量产，且每个模块都需要 |
| retention hardware | 压接式模块必须保证均匀压力和可维护性 |
| guide frame / stiffener | 机械对位、抗翘曲、锁附成为可靠性关键 |
| test socket / fixture | 新内存形态需要新测试体系 |
| thermal pad / heat spreader | 密集 LPDDR5X 在 AI rack 中热管理压力更高 |

判断：

**SOCAMM2 生态是 Rubin / Vera CPU 最直接的小组件增量。未来半年和一年，它的弹性可能高于很多成熟半导体材料。**

---

# **5\. 第二组瓶颈：HBM4 base die、PHY、probe、ATE、socket**

HBM4 不只是 HBM 容量增加。真正的变化是：

| 变化 | 对小组件的影响 |
| ----- | ----- |
| I/O 从 HBM3 / HBM3E 进一步提升，HBM4 可达 2,048 pins | probe card 针数、space transformer、ATE channel 复杂度提升 |
| stack 从 12-hi 走向 16-hi | underfill、warpage、thermal、bonding 难度提升 |
| base die 更 logic-like | HBM base die、PHY、training IP、custom HBM 价值提升 |
| 每颗 AI accelerator 的 HBM 容量增加 | HBM stack 数、测试次数、封装材料消耗增加 |
| HBM4 进入 Rubin / MI450 | 2026H2–2027 大规模量产窗口打开 |

---

## **5.1 HBM4 需求粗算**

| 部署事件 | 小组件需求粗算 | 对应爆发品类 |
| ----- | ----- | ----- |
| 单个 Vera Rubin NVL72 rack | 20.7TB HBM4；若用 36GB HBM4 stack，约 576 个 HBM4 stack；若用 48GB stack，约 432 个 HBM4 stack | HBM4 probe、HBM base die、HBM underfill、SOCAMM2 连接器、SOCAMM2 测试夹具、冷板、VRM、CPO / OCS |
| Oracle 50,000 颗 MI450 | MI450 单颗 432GB HBM4；若 36GB / stack 为 12 stack / GPU，若 48GB / stack 为 9 stack / GPU；50,000 颗对应约 45–60 万个 HBM4 stack | HBM4 stack test、HBM4 probe card、MR-MUF / underfill、TCB、HBM tester、cold plate |
| 1GW MI450 部署 | 若按 120–200kW / rack 粗估，约 5,000–8,333 个 72-GPU rack，即约 36–60 万颗 GPU；按 9–12 stack / GPU，对应约 324–720 万个 HBM4 stack | HBM4 周边件进入百万级需求：probe、tester、socket、underfill、bonding、AOI、X-ray |
| Trn3 UltraServer | 144 颗 Trainium3，20.7TB HBM3E；若 24–36GB / stack，约 576–864 个 HBM3E stack | HBM3E tester、HBM probe、SoC tester、封装检测、系统级 burn-in |
| 100 万颗 TPU 级别部署 | 若未来 TPU 单颗 HBM 容量接近 192GB，按 36–48GB / stack，潜在约 400–533 万个 HBM stack | HBM、CoWoS-like inspection、ATE、OCS、液冷、电源 |

---

## **5.2 HBM4 base die / PHY / 测试小组件**

| 小组件 / 产品 | 未来半年年化 | 未来一年 | 未来两年年化 | 增长逻辑 | 相关公司与上市地 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| HBM4 base die / logic base die | 80–200% | 100–200% | 60–120% | HBM4 base die 更 logic-like，未来 custom HBM 可能把客户定制逻辑、PHY、repair、training、power features 放进 base die | Micron：NASDAQ MU；Samsung：KRX 005930；SK hynix：KRX 000660；TSMC：TWSE 2330 / NYSE TSM |
| HBM4 PHY / controller / training IP | 70–150% | 70–140% | 50–100% | HBM4 I/O 宽度和带宽提高，PHY margin、training、ECC、power integrity 更难；Rubin 单 GPU 22TB/s HBM4，MI450 约 19.6TB/s | Rambus：NASDAQ RMBS；Synopsys：NASDAQ SNPS；Cadence：NASDAQ CDNS；Marvell：NASDAQ MRVL；NVIDIA / AMD / Google / AWS 内部 IP |
| HBM4 probe card / MEMS probe / space transformer | 70–150% | 70–130% | 45–90% | HBM4 stack 数量和 I/O 数增加，wafer-level KGD 测试并行度、针数、thermal control 上升 | FormFactor：NASDAQ FORM；Technoprobe：Borsa Italiana TPRO；MPI：台湾 6223；JEM：东京 6955；Advantest：东京 6857 |
| HBM memory tester channel | 70–130% | 60–120% | 40–80% | AI compute / networking / memory 拉动 memory tester；HBM die、base die、stack、package 都要测 | Advantest：东京 6857；Teradyne：NASDAQ TER；FormFactor：NASDAQ FORM；Chroma ATE：台湾 2360 |
| HBM burn-in socket / high-power final-test socket | 60–120% | 60–110% | 40–80% | 高功率 AI package、HBM stack 和高 pin count 让 socket 的接触电阻、热阻、寿命和一致性要求提高 | Cohu：NASDAQ COHU；Enplas：东京 6961；Yamaichi：东京 6941；Smiths Interconnect：LSE SMIN；Aehr Test：NASDAQ AEHR |
| HBM test load board / high-speed probe interface board | 50–110% | 50–100% | 35–75% | HBM4 \+ 224G SerDes \+ PCIe6 / CXL 增加测试板层数、材料等级、阻抗和散热要求 | FormFactor：FORM；Technoprobe：TPRO；Cohu：COHU；Chroma ATE：2360；Advantest：6857 |
| HBM4 thermal head / thermal chuck | 50–100% | 50–100% | 35–75% | HBM4 / AI die 测试温度窗口更严格，测试时热控制更难 | Advantest：6857；Teradyne：TER；MPI：6223；Cohu：COHU；ESPEC：东京 6859 |

---

## **5.3 HBM 测试 / 封装设备更大范围**

| 小组件 / 小产品 | 需求映射 | 未来 6 个月 | 未来 12 个月 | 未来 24 个月 | 公司 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| HBM4 probe card / MEMS probe / space transformer | HBM4 2,048-pin I/O 和 12 / 16-hi 堆叠提高 probe 复杂度 | \+25–60% | \+60–120% | \+150–350% | FormFactor、Technoprobe、MPI、Japan Electronic Materials、Microfriend |
| HBM memory tester / high-parallelism ATE channel | HBM die、base die、stack、KGD、final package 都要测 | \+20–50% | \+50–100% | \+120–250% | Advantest、Teradyne、Cohu、Chroma ATE、长川科技 |
| AI SoC final-test socket / burn-in socket | 大功耗、高 pin count AI package final test 和 burn-in 强度上升 | \+20–50% | \+50–100% | \+120–250% | Cohu、Yamaichi、Enplas、ISC、Smiths Group、Johnstech |
| TCB bonder | 每颗 AI package 多个 HBM stack attach；MI450、Rubin、TPU 都增加 stack attach 工序 | \+30–70% | \+70–150% | \+180–400% | BESI、ASMPT、Shibaura Mechatronics、Kulicke & Soffa |
| Hybrid bonding tool | Future HBM、SoIC、logic-memory 3D stacking、chiplet-to-chiplet 连接 | \+20–70% | \+70–180% | \+250–700% | BESI、EV Group、Applied Materials、Tokyo Electron、ASMPT |
| Temporary bonding / debonding tool \+ adhesive | TSV、wafer thinning、3D stacking 必需 | \+15–40% | \+40–90% | \+100–250% | Brewer Science、TOK、JSR、3M、EV Group、DISCO |
| CoWoS-like 2D / 3D AOI / bump inspection / RDL inspection | RDL、micro-bump、C4、Cu pillar、die placement、warpage 全部要检测 | \+40–80% | \+70–150% | \+180–400% | Camtek、Onto Innovation、KLA、Nova、Nordson |
| Warpage metrology / X-ray CT / SAM | 大 interposer、大 ABF substrate、underfill、HBM attach 的翘曲 / void / delamination 风险上升 | \+20–50% | \+50–100% | \+120–250% | KLA、Onto、Comet / Yxlon、Nikon、PVA TePla、Nordson |
| High-power thermal chuck / wafer-level burn-in | HBM4、AI SoC、high-power SerDes 测试时温控窗口更窄 | \+20–60% | \+60–120% | \+150–350% | FormFactor、MPI、Aehr Test、Cohu、ESPEC |

核心判断：

**母行业 probe / test 未必整体 50%+，但 HBM4 probe card、HBM memory tester、burn-in socket、thermal head 这些子项有明显高增速。关键逻辑是 HBM4 stack 数 × I/O 数 × 测试工时 × 高温测试复杂度同时上升。**

---

# **6\. 第三组瓶颈：高速铜互连、AEC、SerDes、scale-up fabric**

AI rack 内的短距互连不会被 CPO 立刻完全替代。2026–2027 年更可能出现的是：

**rack 内高速铜互连继续强，switch / scale-out 侧 1.6T 光与 CPO 开始放量。**

---

## **6.1 高速铜互连组件**

| 小组件 / 小产品 | 需求映射 | 未来 6 个月 | 未来 12 个月 | 未来 24 个月 | 相关公司与上市状态 | 判断 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| AEC controller IC / active copper SerDes | 2026E 13–15M 高端 accelerator；按每颗 4–8 个 rack 内高速 endpoint，2026 endpoint 约 50–120M，2027 可能翻倍 | \+25–60% | \+60–130% | \+180–450% | Credo：NASDAQ CRDO；Astera：NASDAQ ALAB；Marvell：NASDAQ MRVL；Broadcom：NASDAQ AVGO；Amphenol：NYSE APH；Molex：私有；Samtec：私有 | 强兑现。AEC 是现在进行时 |
| 224G SerDes PHY / retimer-like IC | 1.6T optics、PCIe 6 / CXL 3、scale-up switch、custom ASIC I/O 都需要 112G / 224G SerDes | \+30–70% | \+70–150% | \+200–500% | Astera、Credo、Marvell、Broadcom、Rambus、Synopsys、Cadence | 架构刚需 |
| scale-up fabric switch ASIC | 72 / 144-chip rack 成为基本计算单元；Helios 260TB/s scale-up，Trainium3 UltraServer 144-chip fabric | \+50–150% | \+150–350% | \+400–1,000% | Astera、Broadcom、Marvell、NVIDIA、Cisco、Celestica | 低基数高赔率，2027–2028 更大 |
| PCIe 6 / CXL retimer | CXL / PCIe 链路高速化，AI server backplane 距离拉长 | \+20–50% | \+50–120% | \+150–350% | Astera、Marvell、Parade、Diodes、澜起科技 | 确定性高，弹性略低于 AEC 和 scale-up switch |
| high-speed twinax / AEC cable assembly | AEC controller 放量同步拉动高频 twinax、connector、cable assembly | \+20–50% | \+50–100% | \+120–250% | Amphenol、TE、Molex、Samtec、Foxconn Interconnect、立讯精密 | 母行业稳，但 AI rack 短距高速线缆子品类高增 |

---

## **6.2 本组核心判断**

| 方向 | 判断 |
| ----- | ----- |
| AEC controller | 当前最确定，已有强收入验证 |
| 224G SerDes | 贯穿光模块、retimer、fabric switch、custom ASIC |
| scale-up fabric switch | 低基数高赔率，受 AMD Helios、Trainium3、custom XPU 架构推动 |
| twinax / cable assembly | 价值量不如 IC，但数量大、客户扩散快 |
| PCIe6 / CXL retimer | 确定性高，受长链路和 memory pooling 拉动 |

一句话：

**AEC 是现在进行时，scale-up switch 是 2027–2028 年更大的赔率项。**

---

# **7\. 第四组瓶颈：光互连、1.6T、EML、CW laser、CPO、SiPh test**

AI 光模块不是只看“光模块总市场”。真正高弹性的小组件是：

| 大方向 | 小组件 |
| ----- | ----- |
| 1.6T 光模块 | optical DSP、200G EML、CW laser、optical engine、driver / TIA |
| CPO | external laser source、laser redundancy module、SiPh PIC、micro-ring modulator |
| SiPh 量产 | wafer-level optical probe、electro-optical test、active alignment |
| 光封装 | FAU、fiber attach、lens array、optical epoxy、micro-lens |

---

## **7.1 光互连小组件增长表**

| 小组件 / 小产品 | 需求映射 | 未来 6 个月 | 未来 12 个月 | 未来 24 个月 | 相关公司与上市状态 | 判断 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 1.6T optical DSP / 224G DSP | 800G → 1.6T，单端口带宽翻倍；AI 光模块市场 2026E 高增 | \+40–120% | \+100–250% | \+300–900% | Marvell、Broadcom、MaxLinear、Semtech、Credo | 光互连最强 IC |
| 200G / lane EML | 800G / 1.6T 单模发射端瓶颈 | \+30–80% | \+70–150% | \+200–450% | Lumentum、Coherent、MACOM、三菱电机、住友电工、ELASER、LuxNet | 瓶颈件 |
| CW laser / external laser source / laser array | SiPh、CPO、LPO / LRO 需要高可靠连续光源；CPO 需要外置 laser source | \+30–90% | \+70–160% | \+200–500% | Lumentum、Coherent、Broadcom、Ayar Labs、Lightmatter、Source Photonics、Marvell / Celestial | 如果 CPO / SiPh 加速，弹性超过普通光模块 |
| 1.6T optical transceiver / optical engine | 2026H2 开始进入实际交付窗口 | \+80–250% | \+150–400% | \+300–900% | AAOI、中际旭创、新易盛、Fabrinet、Coherent、Lumentum | 强兑现 |
| LPO / LRO analog optical front-end | 降低功耗，部分 800G / 1.6T 模块转向 linear optics | \+30–90% | \+70–180% | \+200–600% | Broadcom、Marvell、Credo、Semtech、MACOM | 路线分歧大，若 hyperscaler 接受，价值从传统 DSP 部分转向线性模拟前端 |
| CPO optical engine | 先在 switch ASIC 侧放量，再逐步扩展到更靠近 XPU / package 的互连 | \+20–80% | \+50–150% | \+200–800% | Broadcom、Marvell、Ayar Labs、Lightmatter、Coherent、Lumentum、POET | 期权型，2026–2027 更可能 switch-first |
| SiPh wafer-level optical probe / test | CPO / SiPh 上量后，wafer-level optical probing、fiber alignment、光电测试成为产能瓶颈 | \+40–120% | \+100–250% | \+300–800% | FormFactor、MPI、Keysight、EXFO、Aehr Test、ficonTEC | 被低估的二阶受益者 |
| FAU / fiber attach / active alignment equipment | 高精度 optical alignment 是光模块扩产瓶颈之一 | \+30–80% | \+70–160% | \+200–500% | ficonTEC、ASMPT、Fabrinet、Coherent、Lumentum、Hisense Broadband | 小但关键，瓶颈不只在 laser，也在 alignment 节拍 |

---

## **7.2 OCS / CPO 内部件**

Lumentum 的 OCS backlog 和 CPO 大订单，使 OCS / CPO 从概念进入量产窗口。

| 小组件 / 产品 | 未来半年年化 | 未来一年 | 未来两年年化 | 增长逻辑 | 相关公司与上市地 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| OCS MEMS mirror array | 100–300% | 80–220% | 50–140% | OCS 从小基数进入 AI cluster；MEMS mirror 是 MEMS OCS 核心 | Lumentum：NASDAQ LITE；Calient：未上市；Google 内部生态不透明；Huber+Suhner / Polatis：SIX HUBN |
| OCS fiber collimator / lens array / optical alignment module | 100–250% | 80–200% | 50–130% | OCS 端口数上升后，fiber collimator、透镜阵列、光路校准和机械稳定性成为良率瓶颈 | Lumentum、Coherent、Fabrinet、Molex、Sercalo、Huber+Suhner |
| OCS control board / calibration software / drive electronics | 80–200% | 70–180% | 50–120% | OCS 是光机械 \+ 控制系统，MEMS / Piezo / LC / robotic 方案都需要控制板、校准和监控 | Lumentum、Calient、Telescent、Huber+Suhner、iPronics |
| CPO external laser source / laser redundancy module | 80–180% | 80–160% | 60–130% | CPO 可维护性核心是外置激光源、冗余、健康监控 | Lumentum、Coherent、Ayar Labs、Broadcom、Marvell / Celestial |
| SiPh PIC / optical engine substrate | 50–120% | 80–200% | 70–160% | Rubin / Spectrum-X 已纳入 CPO 路线，短期 switch 侧先放量 | Broadcom、Marvell、NVIDIA、Ayar Labs、Lightmatter、TSMC |
| wafer-level optical probe / SiPh 自动光测试 | 50–100% | 60–130% | 60–120% | CPO / SiPh 量产会把测试从 module-level 前移到 wafer / package-level | FormFactor、MPI、Keysight、Onto、EXFO |
| active alignment / FAU / fiber attach equipment | 60–140% | 60–130% | 45–100% | 1.6T、CPO、OCS 都需要更高精度光纤阵列耦合和主动对准 | ASMPT、Fabrinet、Coherent、Molex、Hirose |

---

## **7.3 本组核心判断**

光互连最强主线：

| 时间 | 最强方向 |
| ----- | ----- |
| 未来 6–12 个月 | 1.6T optical DSP、200G EML、CW laser、1.6T optical engine |
| 未来 12–24 个月 | CPO external laser source、SiPh PIC、wafer-level optical test、OCS MEMS mirror |
| 更长期 | photonic fabric、optical I/O、co-packaged / near-package optics |

关键判断：

**不要只看光模块整机。真正的高弹性件是 200G EML、CW laser、external laser source、active alignment、SiPh optical probe、OCS MEMS mirror。**

---

# **8\. 第五组瓶颈：先进封装材料、RDL、Cu pillar、underfill、玻璃基板**

先进封装材料的特点是：

1. 母行业增速可能只有 10–20%；  
2. AI / HBM / CoWoS-like 子品类可能明显超过 50%；  
3. 供应商往往业务多元，投资纯度低；  
4. 但客户认证强、替代周期长、毛利通常优于普通机械件。

---

## **8.1 HBM / CoWoS-like 材料小组件**

| 小组件 / 小产品 | 需求映射 | 未来 6 个月 | 未来 12 个月 | 未来 24 个月 | 相关公司与上市状态 | 判断 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| HBM underfill / MR-MUF / mold compound | HBM4 12-hi / 16-hi、热机械应力、warpage、die stress | \+20–50% | \+60–120% | \+150–350% | Resonac / Namics、Henkel、Panasonic、Nagase、Shin-Etsu | HBM4 结构可靠性、热阻、堆叠高度抬升材料规格 |
| PSPI / PBO / RDL dielectric | CoWoS-R、fan-out RDL、RDL interposer、large package routing | \+15–40% | \+50–100% | \+120–280% | Toray、DuPont、Asahi Kasei、Mitsui Chemicals、HD Microsystems、Resonac | AI RDL 子线可能显著高增 |
| Cu pillar / micro-bump plating chemicals | HBM-to-interposer、logic-to-interposer、chiplet bump pitch 缩小 | \+15–45% | \+50–100% | \+120–250% | MKS / Atotech、Entegris、DuPont、JCU、Uyemura | 耗材型复合增长，受 HBM stack attach \+ chiplet \+ RDL 共同拉动 |
| Temporary bonding adhesive / release layer | TSV、wafer thinning、hybrid bonding、3D stacking | \+15–40% | \+40–90% | \+100–250% | Brewer Science、TOK、JSR、3M、AI Technology、Shin-Etsu | 小而关键，公开数据少 |
| ABF / low-loss buildup film 高端子类 | 大 package、高速 signal、AI FC-BGA | \+10–30% | \+25–60% | \+60–150% | Ajinomoto、Ibiden、Unimicron、Shinko Electric、AT\&S、Samsung Electro-Mechanics | 普通 ABF 不一定高增，但低损耗 / 高层数 AI 子类可能接近或超过 |
| eDTC / silicon capacitor / on-package decap | XPU \+ HBM 瞬态电流、IR drop、power integrity | \+20–60% | \+70–160% | \+200–500% | Murata、TDK、Samsung Electro-Mechanics、Kyocera、TSMC 内部能力 | 高技术价值，外部纯度低 |
| High-k TIM / indium / phase-change / graphite TIM | 750W–1kW+ package 到 cold plate 的热阻压力；HBM 温控更严格 | \+20–50% | \+50–100% | \+120–250% | Indium Corporation、Honeywell、Henkel、Shin-Etsu、Laird Thermal Systems、Momentive | 散热小材料，功耗越高越接近系统瓶颈 |

---

## **8.2 更细材料拆解**

| 小组件 / 材料 | 未来半年年化 | 未来一年 | 未来两年年化 | 增长逻辑 | 相关公司与上市地 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| MR-MUF / HBM underfill / molded underfill | 60–120% | 60–120% | 40–90% | HBM4 12-hi / 16-hi 堆叠提高热应力、翘曲和可靠性要求 | Resonac：东京 4004；Namics：Resonac 旗下；Henkel：Xetra HEN3；Panasonic：东京 6752；Nagase：东京 8012 |
| RDL dielectric / PSPI / PBO | 50–100% | 50–100% | 40–80% | CoWoS-R / L、fan-out、RDL interposer、bridge 方案增加 RDL 介质材料用量 | Toray：东京 3402；DuPont：NYSE DD；TOK：东京 4186；HD Microsystems；JSR |
| Cu pillar / micro-bump plating chemicals | 60–120% | 60–120% | 40–90% | HBM4、chiplet、2.5D package 连接点数提高，fine pitch bump 使电镀和表面处理难度提升 | MKS / Atotech：NASDAQ MKSI；JCU：东京 4975；DuPont：NYSE DD；Entegris：NASDAQ ENTG；Uyemura：东京 4966 |
| temporary bonding adhesive / debond chemistry | 50–100% | 50–100% | 35–80% | HBM TSV、wafer thinning、3D stacking、hybrid bonding 前工艺都要临时键合材料 | Brewer Science、TOK、3M、DuPont、JSR |
| top-end low-loss ABF / AI FC-BGA build-up material | 40–90% | 40–90% | 30–70% | 普通 ABF 未必高增长，但 AI 大 package、高层数、低损耗、高电流基板子集会显著超行业 | Ajinomoto：东京 2802；Ibiden：东京 4062；Unimicron：台湾 3037；Shinko：东京 6967；AT\&S：维也纳 ATS；Samsung Electro-Mechanics：KRX 009150 |

---

## **8.3 玻璃基板：短期非主线，中期高赔率**

玻璃基板容易被误判。整体玻璃基板市场增速不高，因为包含显示等大市场；但 AI 封装用 glass-core substrate 是低基数新技术。

| 小组件 / 材料 | 未来半年年化 | 未来一年 | 未来两年年化 | 增长逻辑 | 相关公司与上市地 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| glass-core substrate / TGV / glass drilling / metallization | 0–70% | 30–120% | 60–200% | 2026 仍是 pre-mass production，但 2027–2028 若 AI 大封装采用，低基数增长会很陡 | Absolics：SKC 旗下未上市；Samsung Electro-Mechanics：KRX 009150；Intel：NASDAQ INTC；LG Innotek：KRX 011070；Corning：NYSE GLW；LPKF：Xetra LPK；Nippon Electric Glass：东京 5214 |
| glass substrate inspection / TGV metrology | 0–80% | 40–140% | 60–200% | 玻璃基板的 TGV、翘曲、裂纹、金属化良率会产生新检测设备需求 | KLA：NASDAQ KLAC；Onto：NASDAQ ONTO；Camtek：CAMT；Nikon：东京 7731；Lasertec：东京 6920 |
| panel-level packaging / large-area RDL inspection | \+10–40% | \+40–120% | \+150–400% | CoWoS 成本和面积继续上升后，panel-level / large-area RDL 有替代或补充空间 | TSMC、ASE、Amkor、Camtek、Onto、KLA |

核心判断：

**短期最强的是 underfill、RDL dielectric、Cu pillar plating；中期赔率最大的是 glass-core substrate / TGV / glass inspection。玻璃基板不要按整个玻璃市场看，要按 AI advanced packaging 子市场看。**

---

# **9\. 第六组瓶颈：eDTC、硅电容、on-package decap、电源完整性**

随着 HBM4、CoWoS-L、背面供电、Z-axis power 和高功率 XPU 的推进，power integrity 成为隐形瓶颈。

---

## **9.1 eDTC / 硅电容**

| 小组件 / 产品 | 未来半年年化 | 未来一年 | 未来两年年化 | 增长逻辑 | 相关公司与上市地 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| eDTC / embedded deep trench capacitor | 30–80% | 50–120% | 50–120% | HBM4 / XPU 瞬态电流大，decap 越靠近 die 越有价值；CoWoS-S / L 可集成 DTC / LSI | TSMC：TWSE 2330 / NYSE TSM；Murata：东京 6981；TDK：东京 6762；Samsung Electro-Mechanics：KRX 009150 |
| silicon capacitor / ultra-low ESL decap | 40–90% | 50–120% | 50–120% | 高速 HBM PHY、SerDes 和 XPU core rail 需要更低 ESL / ESR 的近端去耦 | Murata、TDK、Kyocera、Samsung Electro-Mechanics、IPDiA / Murata |
| on-package MLCC / capacitor array | 40–80% | 40–90% | 30–70% | AI package 功耗和瞬态电流提高，package / substrate 上 decap 数量和规格提高 | Murata、TDK、Taiyo Yuden、Yageo、Samsung Electro-Mechanics |

---

## **9.2 AI 电源模块**

| 小组件 / 产品 | 未来半年年化 | 未来一年 | 未来两年年化 | 增长逻辑 | 相关公司 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| vertical power delivery module / integrated VRM near package | 70–140% | 70–130% | 50–100% | XPU 电流密度上升，横向 PCB 供电 IR drop 变大 | Monolithic Power、Vicor、Infineon、Renesas |
| high-current inductor / power choke for AI VRM | 50–100% | 50–100% | 35–80% | AI VRM 相数增加、电流密度提高，低损耗磁性件需求增加 | TDK、Murata、Vishay、Chilisin / Yageo、Coilcraft |
| Z-axis / vertical power delivery module | \+25–70% | \+70–150% | \+180–400% | AI rack power 走向 500kW+，传统 board-level PDN 损耗过高 | MPWR、Infineon、Vicor、Renesas |
| High-current VRM / POL / DrMOS / power stage | \+25–60% | \+60–130% | \+150–350% | XPU core、HBM rail、多电压域供电，电流密度提升 | MPWR、Infineon、TI、onsemi、Renesas、Alpha & Omega |
| 48V intermediate bus converter / AI power shelf | \+25–60% | \+60–130% | \+150–350% | rack-level 48V 配电、AI tray 高电流供电 | Delta、Lite-On、AcBel、Flex、Vicor |
| high-current connector / busbar / blind-mate power connector | \+20–50% | \+50–100% | \+120–250% | 48V busbar、高电流连接、AI tray 快速维护 | Amphenol、TE、Molex、Samtec、Foxconn Interconnect、HARTING |

核心判断：

**eDTC / 硅电容更像 1–2 年期权；AI VRM、Z-axis power、48V power shelf、high-current connector 是半年到一年更确定的收入线。**

---

# **10\. 第七组瓶颈：液冷内部件、QD、密封、泄漏检测、冷却液服务**

液冷市场不能只看 cold plate 和 CDU。更细的小组件包括：

| 层级 | 小组件 |
| ----- | ----- |
| 芯片接触 | cold plate、TIM、manifold |
| 流体连接 | UQD / quick disconnect、blind-mate connector |
| 密封可靠性 | O-ring、gasket、seals |
| 监控 | leak detection sensor、moisture sensor、flow sensor |
| 运维 | coolant chemistry、corrosion inhibitor、biocide、filtration、flushing、commissioning service |

---

## **10.1 液冷组件增长表**

| 小组件 / 产品 | 未来半年年化 | 未来一年 | 未来两年年化 | 增长逻辑 | 相关公司与上市地 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| direct-to-chip cold plate | 80–200% | 70–130% | 45–90% | GB300、Rubin、MI450、Maia 级高功率芯片让 direct-to-chip 液冷成为默认方案 | CoolIT：未上市，Ecolab 收购中；Auras：台湾 3324；AVC：台湾 3017；Boyd：Eaton 旗下；Delta：台湾 2308 |
| CDU / manifold / pump / valve | 80–200% | 70–130% | 45–90% | AI rack 功率密度提升，CDU 从小众变成机柜 / 列级标配 | Vertiv、Delta、Schneider、Eaton、CoolIT / Ecolab |
| UQD / quick disconnect | 70–150% | 70–130% | 45–90% | 每个 cold plate、manifold、tray 都需要快速接头；AI rack 可维护性依赖低泄漏、盲插、耐压接头 | Parker、Stäubli、CPC / Colder、CEJN、Koolance、中航光电 |
| seals / O-ring / gasket for liquid cooling | 70–150% | 60–120% | 40–90% | 液冷规模化后，漏液风险使密封件从普通机械件变成可靠性关键件 | Parker、Trelleborg、Freudenberg、NOK、Stäubli |
| leak detection sensor / moisture sensor | 70–160% | 70–140% | 45–100% | 机柜级液冷必须实时监控漏液，尤其是高密度 GPU tray 和 blind-mate 接头 | TE Connectivity、Sensata、Amphenol、Honeywell、nVent |
| coolant chemistry / corrosion inhibitor / biocide | 50–120% | 60–120% | 40–90% | 液冷从硬件交付转向长期运维，冷却液、防腐、过滤、flush 服务价值上升 | Ecolab、Chemours、Solvay、Vertiv、PurgeRite |
| filtration / flushing / commissioning service | 60–140% | 60–130% | 40–90% | 大规模液冷数据中心上线前后需要清洗、过滤、排气、维护 | Vertiv、Ecolab、PurgeRite、Parker、Pentair |

---

## **10.2 液冷与电源一体化增长表**

| 小组件 / 小产品 | 需求映射 | 未来 6 个月 | 未来 12 个月 | 未来 24 个月 | 公司 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| Direct-to-chip cold plate | 高端 GPU / ASIC 至少 1 个 cold plate；CPU、switch、power shelf 也可能液冷 | \+30–80% | \+80–170% | \+220–500% | CoolIT / Ecolab、Boyd、Auras、AVC、Delta |
| CDU / rack manifold / pump / valve | 高密度 rack 需要 CDU、泵、阀、流量控制、manifold | \+30–80% | \+70–150% | \+200–450% | Vertiv、Ecolab / CoolIT、nVent、Delta、Danfoss、Schneider |
| Quick disconnect / seals / leak detection | 每个 cold plate 至少两端 QD；manifold 还会额外增加连接数量 | \+25–70% | \+70–150% | \+180–450% | Dover / CPC、Parker、Stäubli、Danfoss、nVent、TE |
| Coolant chemistry / corrosion inhibitor / filtration | 液冷规模化后，冷却液水化学、腐蚀、微粒过滤、运维变成持续收入 | \+15–40% | \+40–90% | \+100–250% | Ecolab、Chemours、Solvay、Parker、Donaldson |

核心判断：

**母行业液冷 CAGR 可能只有 20% 左右，但 AI direct-liquid 子线里的 QD、seals、leak sensors、commissioning service 未来半年到一年可能远超 50%。它们的特点是单价小、数量多、可靠性关键、供应商分散，容易被市场漏掉。**

---

# **11\. 第八组瓶颈：CXL、memory pooling、near-memory acceleration、AI-native storage**

长上下文、agent memory、KV cache、multi-agent workflow 会把 memory hierarchy 从 HBM 扩展到 CXL / SSD / AI-native storage。

---

## **11.1 CXL / memory pooling**

| 小组件 / 小产品 | 需求映射 | 未来 6 个月 | 未来 12 个月 | 未来 24 个月 | 相关公司与上市状态 | 判断 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| CXL switch ASIC | 长上下文推理、KV cache、agent memory 对外部 DDR memory pool 的需求上升 | \+20–80% | \+70–180% | \+250–700% | Marvell、Astera、Broadcom、Microchip、XConn / Marvell | 高赔率 |
| CXL memory expander controller | 用 DDR5 / DDR4 做低成本外部 memory tier，补 HBM 容量不足 | \+20–60% | \+60–150% | \+200–500% | Marvell、Astera、Rambus、澜起科技、SMART Global | 推理型需求更强 |
| Near-memory accelerator：compression / KV cache assist / vector search | 在 CXL / DDR memory 附近做压缩、加密、vector search、KV cache 调度 | \+10–60% | \+50–150% | \+200–500% | Marvell、Rambus、澜起科技、hyperscaler 自研、部分私有 ASIC / IP | 取决于 software runtime 是否把 KV cache / vector memory tier 调度起来 |
| CXL software / fabric manager | CXL memory pooling 需要软件层做资源调度、隔离、QoS、故障恢复 | \+20–80% | \+70–200% | \+250–700% | MemVerge、Marvell、Astera、IBM / Red Hat、hyperscaler 内部 | 商业化不透明，可能被 hyperscaler 内部化 |
| DDR5 CXL memory module：RCD / PMIC / SPD hub | CXL expander 放量拉动 DDR5 模组及配套芯片 | \+15–45% | \+40–100% | \+100–250% | 澜起科技、Rambus、Renesas、TI、MPWR、Samsung、SK hynix、Micron | 慢热但确定，取决于 CXL memory expander attach rate |

---

## **11.2 AI-native storage 与 STX / CMX 的关系**

STX / CMX 与 CXL memory pooling 不是完全替代关系，而是 memory hierarchy 的不同层：

| 层级 | 介质 / 技术 | 作用 |
| ----- | ----- | ----- |
| L1 / on-chip | SRAM | 极低时延 decode、MoE expert execution |
| HBM | HBM3E / HBM4 | attention、active KV、训练 / 推理主内存 |
| CPU memory | SOCAMM2 / LPDDR5X | agent sandbox、orchestration、ETL、CPU control plane |
| CXL memory | DDR5 / pooled memory | 较低成本外部 memory tier、KV cache、长上下文 |
| STX / CMX | SSD \+ DPU \+ CPU \+ network \+ context memory storage | persistent context、long memory、agent state、AI-native storage |
| Object / file storage | VAST、WEKA、NetApp、DDN 等 | 数据集、模型、训练数据、checkpoint、长期数据 |

核心判断：

**如果推理 workload 向长上下文、agent、KV cache、persistent memory 爆发，CXL switch 与 STX / CMX 会成为 HBM 之外的新瓶颈。**

---

# **12\. 第九组瓶颈：更早期但不能漏的小组件**

这些方向不一定在未来 12 个月全部兑现，但如果下一代封装 / 光互连 / 散热路线被确认，增长会很快。

| 小组件 / 小产品 | 未来 6 个月 | 未来 12 个月 | 未来 24 个月 | 相关公司 | 为什么要跟 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| glass core substrate / glass interposer | \+10–40% | \+40–120% | \+150–500% | Corning、AGC、SKC / Absolics、Samsung Electro-Mechanics、Intel、Ibiden | 如果 AI package 从 organic substrate 继续转向 glass core，激光钻孔、TGV、warpage control 会打开新价值池 |
| panel-level packaging / large-area RDL inspection | \+10–40% | \+40–120% | \+150–400% | TSMC、ASE、Amkor、Camtek、Onto、KLA | CoWoS 成本和面积继续上升后，panel-level / large-area RDL 有替代或补充空间 |
| OCS MEMS mirror / optical circuit switch | \+10–50% | \+50–150% | \+200–600% | Calient、Huber+Suhner / Polatis、Coherent、Lumentum、Google 内部生态 | Google TPU / Ironwood 这类 pod-scale 架构强调 optical circuit switching |
| optical epoxy / micro-lens / fiber array unit | \+20–60% | \+60–150% | \+200–500% | Coherent、Lumentum、Fabrinet、ficonTEC、NTT Advanced Technology、Nippon Electric Glass | CPO / SiPh 上量后，光封装材料和耦合件可能成为良率瓶颈 |
| direct-to-silicon / microfluidic cooling | \+10–40% | \+40–120% | \+150–500% | JetCool、CoolIT / Ecolab、Boyd、Auras、AVC | 1kW+ package 后，传统 cold plate 可能不够，微流道 / 更深层冷却会成为下一阶段 |
| HBM base die / custom HBM logic die IP | \+20–60% | \+70–160% | \+200–500% | Samsung、SK hynix、Micron、TSMC、Cadence、Synopsys、Rambus | HBM4 base die 逻辑含量提高，custom HBM 可能成为 hyperscaler 定制链的一部分 |

---

# **13\. 按时间维度排序：未来半年、未来一年、未来两年**

## **13.1 未来 6 个月：订单和量产最清晰**

| 排名 | 小组件 / 产品 | 未来半年年化增长 | 为什么 |
| ----- | ----- | ----- | ----- |
| 1 | 1.6T optical engine / transceiver | 120–300% | 1.6T 进入 2026H2 交付窗口，光互连需求明确 |
| 2 | SOCAMM2 connector / retention / module test fixture | 100–300% | Rubin NVL72 54TB LPDDR5X，SOCAMM2 已进入量产，连接器和机械件从小基数启动 |
| 3 | OCS MEMS mirror / fiber collimator / control board | 100–300% | Lumentum OCS backlog 已验证 |
| 4 | QD / seals / leak detection | 70–160% | direct liquid cooling 高增，AI rack 液冷接头与密封需求随冷板数量同步增加 |
| 5 | AEC controller IC | 80–160% | Credo / Astera 等高速互连供应链已出现强增长 |
| 6 | CoWoS-like AOI / micro-bump inspection | 80–160% | AI CoWoS-like package 扩产必买检测设备 |
| 7 | TCB / hybrid bonding | 70–150% | HBM4、chiplet 和 2.5D / 3D 封装推动 |
| 8 | HBM4 probe card / HBM tester | 70–150% | Rubin / MI450 HBM4 stack 数量进入量产拉动期 |
| 9 | AI VRM / high-current power stage | 60–130% | 500kW+ rack 与高功率 XPU 推动供电升级 |
| 10 | 200G EML / CW laser | 70–160% | 1.6T 与 CPO / SiPh 的共同瓶颈 |

---

## **13.2 未来一年：Rubin / MI450 正式放量**

| 排名 | 小组件 / 产品 | 未来一年增长 | 为什么 |
| ----- | ----- | ----- | ----- |
| 1 | HBM4 base die / custom HBM logic die | 100–200% | Rubin / MI450 HBM4 放量，custom HBM 开始形成新利润池 |
| 2 | SOCAMM2 module \+ connector / socket | 100–220% | Vera CPU memory 标配化 |
| 3 | 1.6T optical DSP / EML / CW laser | 70–160% 到 100–250% | 800G → 1.6T 转换，光芯片和 DSP 是瓶颈 |
| 4 | CPO external laser source / SiPh PIC | 80–200% | 2027 H1 CPO 订单交付，switch 侧先放量 |
| 5 | scale-up fabric switch ASIC | 70–150% 到 150–350% | Helios、MTIA、custom XPU 架构推动 rack-scale fabric |
| 6 | MR-MUF / HBM underfill / Cu plating / RDL dielectric | 60–120% | HBM4 stack、CoWoS-R / L、chiplet 量产提升材料消耗 |
| 7 | AI VRM / Z-axis power / 48V power shelf | 60–130% | 500kW 级 rack 和高功率 XPU 推动供电升级 |
| 8 | liquid cooling QD / seals / leak sensor / service | 60–140% | 液冷从硬件交付转向长期运维 |
| 9 | HBM ATE / burn-in socket / thermal chuck | 50–120% | 测试工时、温控复杂度和 pin count 提升 |
| 10 | STX / CMX / CXL memory pooling | 50–180% | 长上下文和 agent memory 对外部 memory tier 的需求上升 |

---

## **13.3 未来两年：技术期权和低基数高弹性**

| 排名 | 小组件 / 产品 | 两年年化增长 | 为什么 |
| ----- | ----- | ----- | ----- |
| 1 | glass-core substrate / TGV / glass inspection | 60–200% 或 \+150–500% | 2026 仍是 pre-mass production，2027–2028 若量产突破，低基数增长非常陡 |
| 2 | photonic fabric / CPO optical engine / optical I/O | 70–160% 或 \+200–800% | 2027–2028 从 switch 侧扩散到更广 AI fabric |
| 3 | custom HBM4E base die / HBM PHY | 60–120% 或 \+200–500% | custom HBM 样品 2027 开始，base die 变成客户定制逻辑 |
| 4 | CXL switch / memory pooling switch | 50–110% 或 \+250–700% | 长上下文、agent memory、KV cache 推动 memory tiering |
| 5 | eDTC / silicon capacitor / on-package decap | 50–120% 或 \+200–500% | HBM4、CoWoS-L、背面供电、Z-axis power 拉动近端去耦 |
| 6 | wafer-level optical probe / SiPh test | 60–120% 或 \+300–800% | CPO / SiPh 量产后，测试前移成为新瓶颈 |
| 7 | SOCAMM2 ecosystem second-source components | 50–120% | 连接器、测试夹具、热件、扣具从 NVIDIA 扩展到更多 CPU / ASIC 平台 |
| 8 | microfluidic / direct-to-silicon cooling | \+150–500% | 1kW+ package 后传统 cold plate 可能不足 |
| 9 | OCS MEMS / optical circuit switch | \+200–600% | pod-scale AI cluster 对低延迟、低功耗 any-to-any optical connectivity 的需求上升 |
| 10 | panel-level packaging / large-area RDL inspection | \+150–400% | 大封装成本和面积压力推动替代路线 |

---

# **14\. 按“确定性 × 弹性 × 可投资纯度”排序**

| 排名 | 小产品 | 未来 12 个月增速 | 未来 24 个月增速 | 确定性 | 利润弹性 | 可投资纯度 | 代表公司 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 1 | 1.6T optical DSP / 224G SerDes | \+100–250% | \+300–900% | 高 | 高 | 高 | MRVL、AVGO、MXL、SMTC |
| 2 | AEC controller IC | \+60–130% | \+180–450% | 高 | 高 | 高 | CRDO、ALAB |
| 3 | 200G EML / CW laser | \+70–160% | \+200–500% | 高 | 高 | 中高 | LITE、COHR、MTSI |
| 4 | 1.6T optical engine / transceiver | \+150–400% | \+300–900% | 中高 | 中 | 中 | AAOI、300308.SZ、300502.SZ、FN |
| 5 | HBM4 probe card / MEMS probe | \+60–120% | \+150–350% | 高 | 中高 | 中高 | FORM、TPRO、6223.TWO |
| 6 | TCB / hybrid bonding | \+70–180% | \+180–700% | 中高 | 高 | 中高 | BESI、ASMPT、AMAT |
| 7 | CoWoS-like AOI / bump inspection | \+70–150% | \+180–400% | 高 | 高 | 高 | CAMT、ONTO、KLAC |
| 8 | AI SoC / HBM ATE | \+50–100% | \+120–250% | 高 | 中高 | 中 | TER、6857.T、COHU |
| 9 | Z-axis power / high-current VRM | \+70–150% | \+180–400% | 高 | 高 | 中高 | MPWR、IFX、VICR |
| 10 | direct cold plate / CDU / QD | \+70–170% | \+180–500% | 高 | 中 | 中 | VRT、ECL / CoolIT、3017.TW、3324.TW、DOV |
| 11 | CXL switch / memory pooling | \+70–180% | \+250–700% | 中 | 高 | 中 | MRVL、ALAB、MCHP |
| 12 | SiPh wafer-level optical test | \+100–250% | \+300–800% | 中 | 高 | 中 | FORM、MPI、KEYS |
| 13 | CPO optical engine / ELS | \+50–150% | \+200–800% | 中 | 高 | 中 | AVGO、MRVL、Ayar、LITE、COHR |
| 14 | HBM underfill / MR-MUF | \+60–120% | \+150–350% | 中高 | 中高 | 低中 | Resonac、Henkel |
| 15 | glass core / OCS MEMS / microfluidic cooling | \+40–150% | \+150–600% | 中低 | 高 | 低中 | GLW、SKC / Absolics、HUBN、ECL |

---

# **15\. 公司总表：按产业链归类**

## **15.1 SOCAMM2 / 内存模块 / 连接器**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| SOCAMM2 module | Micron | 上市，NASDAQ MU |
| SOCAMM2 module | SK hynix | 上市，KRX 000660 |
| SOCAMM2 module | Samsung Electronics | 上市，KRX 005930 |
| SOCAMM2 connector | Amphenol | 上市，NYSE APH |
| SOCAMM2 connector / retention | TE Connectivity | 上市，NYSE TEL |
| SOCAMM2 connector | Molex | 未上市，Koch Industries 旗下 |
| SOCAMM2 connector | JAE | 上市，东京 6807 |
| SOCAMM2 connector | Hirose | 上市，东京 6806 |
| SOCAMM2 connector / CPU socket | LOTES / 嘉泽 | 上市，台湾 3533 |
| high-speed cable / connector | Foxconn Interconnect | 上市，港交所 6088 |
| high-speed cable / connector | Luxshare / 立讯精密 | 上市，深交所 002475 |

---

## **15.2 HBM / PHY / probe / tester**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| HBM4 base die / HBM | Micron | 上市，NASDAQ MU |
| HBM4 base die / HBM | Samsung | 上市，KRX 005930 |
| HBM4 base die / HBM | SK hynix | 上市，KRX 000660 |
| HBM PHY / IP | Rambus | 上市，NASDAQ RMBS |
| HBM PHY / IP | Synopsys | 上市，NASDAQ SNPS |
| HBM PHY / IP | Cadence | 上市，NASDAQ CDNS |
| HBM probe card | FormFactor | 上市，NASDAQ FORM |
| HBM probe card | Technoprobe | 上市，Borsa Italiana TPRO |
| Probe station / optical probe | MPI | 上市，台湾 6223 |
| HBM probe | Japan Electronic Materials | 上市，东京 6855 |
| HBM probe | Microfriend | 上市，KOSDAQ 147760 |
| Test socket | Cohu | 上市，NASDAQ COHU |
| Test socket | Enplas | 上市，东京 6961 |
| Test socket | Yamaichi | 上市，东京 6941 |
| Test socket | ISC | 上市，KOSDAQ 095340 |
| ATE / memory tester | Advantest | 上市，东京 6857 |
| ATE / memory tester | Teradyne | 上市，NASDAQ TER |
| ATE / memory tester | Chroma ATE | 上市，台湾 2360 |
| ATE / tester | 长川科技 | 上市，深交所 300604 |

---

## **15.3 先进封装设备 / 检测**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| TCB / hybrid bonding | BESI | 上市，Euronext Amsterdam BESI |
| TCB / die attach | ASMPT | 上市，港交所 0522 |
| TCB / bonding | Shibaura Mechatronics | 上市，东京 6590 |
| bonding / assembly | Kulicke & Soffa | 上市，NASDAQ KLIC |
| Wafer bonding | EV Group | 未上市 |
| Hybrid bonding / wafer equipment | Applied Materials | 上市，NASDAQ AMAT |
| Hybrid bonding / wafer equipment | Tokyo Electron | 上市，东京 8035 |
| Temporary bonding | SUSS MicroTec | 上市，Xetra SMHN |
| Dicing / grinding | DISCO | 上市，东京 6146 |
| CoWoS-like AOI | Camtek | 上市，NASDAQ CAMT |
| Inspection / metrology | Onto Innovation | 上市，NASDAQ ONTO |
| Inspection / metrology | KLA | 上市，NASDAQ KLAC |
| Inspection / metrology | Nova | 上市，NASDAQ NVMI |
| X-ray / CT | Comet / Yxlon | 上市，SIX COTN |
| Metrology | Nikon | 上市，东京 7731 |
| SAM / inspection | Nordson | 上市，NASDAQ NDSN |

---

## **15.4 先进封装材料**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| HBM underfill | Resonac | 上市，东京 4004 |
| HBM underfill | Namics | Resonac 旗下，未独立上市 |
| Underfill / TIM | Henkel | 上市，Xetra HEN3 |
| Underfill / materials | Panasonic | 上市，东京 6752 |
| Materials | Nagase | 上市，东京 8012 |
| RDL dielectric / plating | DuPont | 上市，NYSE DD |
| RDL dielectric | Toray | 上市，东京 3402 |
| RDL dielectric | Asahi Kasei | 上市，东京 3407 |
| RDL dielectric | Mitsui Chemicals | 上市，东京 4183 |
| Plating chemicals | MKS / Atotech | 上市，NASDAQ MKSI |
| Plating chemicals | JCU | 上市，东京 4975 |
| Plating chemicals | Entegris | 上市，NASDAQ ENTG |
| Plating chemicals | Uyemura | 上市，东京 4966 |
| temporary bonding | Brewer Science | 未上市 |
| temporary bonding | TOK | 上市，东京 4186 |
| temporary bonding | 3M | 上市，NYSE MMM |
| eDTC / Si capacitor | Murata | 上市，东京 6981 |
| eDTC / MLCC | TDK | 上市，东京 6762 |
| Silicon capacitor / package capacitor | Samsung Electro-Mechanics | 上市，KRX 009150 |
| MLCC / capacitor | Taiyo Yuden | 上市，东京 6976 |
| MLCC / capacitor | Yageo | 上市，台湾 2327 |
| TIM / high-k materials | Honeywell | 上市，NASDAQ HON |
| TIM / graphite / phase-change | Shin-Etsu | 上市，东京 4063 |

---

## **15.5 玻璃基板 / TGV / 大面积封装**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| Glass-core substrate | Absolics | 未上市，SKC 旗下 |
| Glass substrate | Samsung Electro-Mechanics | 上市，KRX 009150 |
| Glass substrate / roadmap | Intel | 上市，NASDAQ INTC |
| Glass substrate | LG Innotek | 上市，KRX 011070 |
| Glass material | Corning | 上市，NYSE GLW |
| Glass material | AGC | 上市，东京 5201 |
| Glass processing | LPKF | 上市，Xetra LPK |
| Glass material | Nippon Electric Glass | 上市，东京 5214 |
| Substrate | Ibiden | 上市，东京 4062 |
| Substrate | Unimicron | 上市，台湾 3037 |
| Substrate | Shinko Electric | 上市，东京 6967 |
| Substrate | AT\&S | 上市，维也纳 ATS |

---

## **15.6 光互连 / CPO / OCS**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| OCS / MEMS optical switch | Lumentum | 上市，NASDAQ LITE |
| OCS | Calient | 未上市 |
| OCS / optical switching | Huber+Suhner / Polatis | Huber+Suhner 上市，SIX HUBN |
| CPO laser / EML | Lumentum | 上市，NASDAQ LITE |
| CPO laser / EML | Coherent | 上市，NYSE COHR |
| EML / RF | MACOM | 上市，NASDAQ MTSI |
| Laser / optical device | Mitsubishi Electric | 上市，东京 6503 |
| Optical device | Sumitomo Electric | 上市，东京 5802 |
| Optical component | ELASER | 上市，台湾 3450 |
| Optical component | LuxNet | 上市，台湾 4979 |
| CPO / optical I/O | Ayar Labs | 未上市 |
| Photonic fabric | Celestial AI | 已被 Marvell 收购 |
| CPO / optical engine | Broadcom | 上市，NASDAQ AVGO |
| CPO / optical engine | Marvell | 上市，NASDAQ MRVL |
| Optical module / engine | AAOI | 上市，NASDAQ AAOI |
| Optical module | Innolight / 中际旭创 | 上市，深交所 300308 |
| Optical module | Eoptolink / 新易盛 | 上市，深交所 300502 |
| Optical manufacturing | Fabrinet | 上市，NYSE FN |
| Optical test | Keysight | 上市，NYSE KEYS |
| Optical probe | FormFactor | 上市，NASDAQ FORM |
| Optical probe | MPI | 上市，台湾 6223 |
| Active alignment | ficonTEC | 未上市 |
| Active alignment / assembly | ASMPT | 上市，港交所 0522 |

---

## **15.7 高速铜互连 / SerDes / fabric**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| AEC / SerDes | Credo | 上市，NASDAQ CRDO |
| Retimer / fabric | Astera Labs | 上市，NASDAQ ALAB |
| CXL / optical DSP | Marvell | 上市，NASDAQ MRVL |
| Ethernet / custom ASIC | Broadcom | 上市，NASDAQ AVGO |
| Retimer / SerDes | Parade | 上市，台湾 4966 |
| Retimer / connectivity | Diodes | 上市，NASDAQ DIOD |
| Memory interface / CXL | Montage / 澜起科技 | 上市，科创板 688008 |
| Connector / cable | Amphenol | 上市，NYSE APH |
| Connector / cable | TE Connectivity | 上市，NYSE TEL |
| Connector / cable | Molex | 未上市 |
| Connector / cable | Samtec | 未上市 |

---

## **15.8 液冷 / 电源 / 传感**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| Liquid cooling cold plate / CDU | CoolIT | 未上市，Ecolab 收购中 |
| Liquid cooling / coolant | Ecolab | 上市，NYSE ECL |
| Liquid cooling infra | Vertiv | 上市，NYSE VRT |
| Liquid cooling / infra | Schneider Electric | 上市，巴黎 SU |
| Power / infra | Eaton | 上市，NYSE ETN |
| Cold plate / cooling | Auras | 上市，台湾 3324 |
| Cold plate / cooling | AVC | 上市，台湾 3017 |
| Power / cooling | Delta Electronics | 上市，台湾 2308 |
| QD / fluid connector | Parker | 上市，NYSE PH |
| QD / fluid connector | Stäubli | 未上市 |
| QD / fluid connector | CPC / Colder | Dover 旗下 |
| Liquid connector | AVIC Jonhon / 中航光电 | 上市，深交所 002179 |
| Seals | Trelleborg | 上市，斯德哥尔摩 TREL B |
| Seals | Freudenberg | 未上市 |
| Seals | NOK | 上市，东京 7240 |
| Leak sensor / connector | TE Connectivity | 上市，NYSE TEL |
| Sensor | Sensata | 上市，NYSE ST |
| Sensor / connector | Amphenol | 上市，NYSE APH |
| Sensor | Honeywell | 上市，NASDAQ HON |
| Enclosure / sensor | nVent | 上市，NYSE NVT |
| Coolant / chemistry | Chemours | 上市，NYSE CC |
| Coolant / chemistry | Solvay | 上市，Euronext Brussels SOLB |
| Filtration | Donaldson | 上市，NYSE DCI |
| Filtration | Pentair | 上市，NYSE PNR |

---

## **15.9 AI power**

| 小组件 / 产品 | 公司 | 上市状态 / 地点 |
| ----- | ----- | ----- |
| AI power / VRM | Monolithic Power | 上市，NASDAQ MPWR |
| AI power | Infineon | 上市，Xetra IFX |
| Power module | Vicor | 上市，NASDAQ VICR |
| Power IC | Texas Instruments | 上市，NASDAQ TXN |
| Power semiconductor | onsemi | 上市，NASDAQ ON |
| Power IC | Renesas | 上市，东京 6723 |
| Power stage | Alpha & Omega | 上市，NASDAQ AOSL |
| Power shelf | Lite-On | 上市，台湾 2301 |
| Power supply | AcBel | 上市，台湾 6282 |
| Power / manufacturing | Flex | 上市，NASDAQ FLEX |
| HVDC ecosystem | ABB | 上市，SIX ABBN |
| Grid / power | GE Vernova | 上市，NYSE GEV |
| Grid / power | Hitachi Energy | Hitachi 旗下 |
| Grid / power | Siemens | 上市，Xetra SIE |
| Power semiconductor | Navitas | 上市，NASDAQ NVTS |
| Analog / power | ADI | 上市，NASDAQ ADI |

---

# **16\. 技术路径与成熟时间表**

以下是第三份文件中对 NVIDIA 技术栈成熟节奏的整理，并结合前两份文件的小组件映射。

| 技术路径 | 当前状态 / 节奏 | 小规模量产 | 大规模量产 | 成熟期年化相关市场空间 / 生态价值池 | 直接拉动的小组件 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| Rubin GPU / NVL72 机架系统 | 七颗芯片进入 full production，伙伴产品 2H26 开始 | 2H26 | 2027 | $80B–$180B | HBM4、TCB、probe、ATE、CPO、液冷、电源、SOCAMM2 |
| HBM4 \+ 先进封装 \+ SOCAMM2 | HBM4 和 SOCAMM2 高量产 / 就绪 | 1H26–2H26 | 2H26–2027 | $25B–$60B | HBM4 stack、underfill、base die、probe、SOCAMM2 connector |
| Vera CPU \+ SOCAMM 服务器内存形态 | Vera CPU 发布，OEM 机型 2H26 上市 | 2H26 | 2027 | $8B–$20B | SOCAMM2 模块、compression connector、retention、LPDDR5X、CPU rack |
| Groq 3 LPX / 低时延异构推理机架 | 已作为 Rubin 平台组成部分发布 | 2H26 | 2027–2028 | $10B–$30B | SRAM-heavy accelerator、scale-up fabric、runtime、low-latency interconnect |
| STX / CMX / AI-native context storage | STX 发布，伙伴 2H26 出货 | 2H26 | 2027 | $6B–$18B | BlueField-4、Gen6 SSD、AI storage、CXL / memory tier、network |
| Spectrum-6 / ConnectX-9 / CPO photonics | CPO 路线公开到工程细节层 | 2H26 | 2027 | $20B–$45B | CPO、external laser、SiPh PIC、wafer optical test、OCS |
| 800VDC / Kyber 电源架构 | 产业协同爬坡 | 2027 | 2028 | $15B–$40B | HVDC、power module、64:1 converter、busbar、power connector |
| DSX / Omniverse DSX / DSX Air | DSX 参考设计发布，DSX Air 上线 | 2026 | 2027 | $2B–$8B | AI factory digital twin、EPC software、power orchestration |
| Dynamo inference OS | Dynamo 1.0 production-grade | 2026 | 2026–2027 | $3B–$10B | runtime、KV management、cluster OS、serving stack |
| Agent Toolkit / OpenShell / NemoClaw / Nemotron | 产品线形成，企业试点 | 2026–2027 | 2027–2028 | $5B–$20B | agent workload、long context、STX / CMX、LPX、Rubin |
| Physical AI Data Factory / Cosmos / Isaac / GR00T | 蓝图、模型、仿真框架齐全 | 2027 | 2028–2030 | $15B–$60B | robotics data factory、simulation、edge AI、GPU / storage |
| DRIVE Hyperion / robotaxi / AI-RAN / Space edge | 车、边缘、太空三条扩展线 | 2027–2028 | 2028–2030+ | $10B–$40B | edge compute、AI-RAN、robotaxi compute、sensor fusion |

---

# **17\. 需求链路：从 AI 工厂架构到小组件**

可以把 AI 工厂拆成 10 条需求链：

## **17.1 GPU / XPU 算力链**

| 上游变化 | 中间组件 | 下游瓶颈 |
| ----- | ----- | ----- |
| Rubin、MI450、TPU、Trainium3、Maia 放量 | HBM、advanced packaging、probe、ATE、liquid cooling、VRM | HBM4 供给、CoWoS-like capacity、测试时长、冷却装配 |

## **17.2 内存链**

| 上游变化 | 中间组件 | 下游瓶颈 |
| ----- | ----- | ----- |
| HBM4 容量和带宽提升 | base die、PHY、underfill、probe、tester | HBM4 KGD 测试、I/O margin、堆叠良率 |
| Vera CPU 引入 SOCAMM2 | SOCAMM2 module、connector、retention、thermal pad、test fixture | 新内存形态的供应商认证和机械可靠性 |
| 长上下文推理 | CXL switch、memory expander、STX / CMX | KV cache 分层、software runtime 调度 |

## **17.3 网络链**

| 上游变化 | 中间组件 | 下游瓶颈 |
| ----- | ----- | ----- |
| 800G → 1.6T | optical DSP、EML、CW laser、active alignment | EML / laser 供给和 alignment 节拍 |
| rack-scale scale-up | AEC、224G SerDes、scale-up fabric switch | copper signal integrity、retimer / fabric ASIC |
| CPO / OCS | external laser source、SiPh PIC、MEMS mirror、fiber collimator | wafer optical test、CPO serviceability、OCS 校准 |

## **17.4 电源链**

| 上游变化 | 中间组件 | 下游瓶颈 |
| ----- | ----- | ----- |
| 500kW–1MW rack | 48V power shelf、HVDC、busbar | 数据中心电力改造速度 |
| XPU 电流密度上升 | VRM、DrMOS、Z-axis power、inductor、eDTC | package 近端供电和 power integrity |

## **17.5 液冷链**

| 上游变化 | 中间组件 | 下游瓶颈 |
| ----- | ----- | ----- |
| 高功率 GPU / ASIC | cold plate、CDU、manifold、pump、valve | 装配产能和可靠性 |
| 维护需求 | QD、seals、leak detection、coolant service | 漏液风险、现场运维、标准化 |

---

# **18\. 最重要的验证点**

三份材料合并后，最值得持续验证的数据点如下。

| 验证点 | 为什么重要 |
| ----- | ----- |
| Rubin 2026H2 真实 ramp 和 HBM4 认证节奏 | 直接决定 HBM4 probe、TCB、1.6T optics、液冷、电源的放量时间 |
| HBM4 真实供给 | HBM4 是 Rubin / MI450 的硬瓶颈，影响整个 AI rack 交付 |
| Google TPU 2027 是否继续走向更高数百万颗量级 | ASIC 量级越大，先进封装、test、液冷、光互连越不依赖 NVIDIA 单一周期 |
| AMD MI450 / Helios 大规模部署节奏 | 决定 HBM4、液冷、电源和 scale-up fabric 是否形成第二条强需求曲线 |
| 1.6T optical engine 的 hyperscaler design-in 数量 | 决定 optical DSP、EML、CW laser、active alignment 是短期爆发还是多年度爆发 |
| Credo / Astera 的客户集中度和新客户 ramp | AEC / SerDes 当前强，但需要确认是否从单一大客户扩散 |
| BESI / Camtek / FormFactor / Advantest 的 HBM4 订单占比 | 区分“总行业增长”与“HBM4 子线爆发” |
| CoolIT / Ecolab、Vertiv、AVC / Auras 的产能扩张 | 液冷增速高，但机械产能、验证、交付能力会限制兑现 |
| Marvell Structera S 2026Q3 sampling 客户 | CXL switch 是否进入 AI inference rack 是关键 |
| CPO 是否只在 switch 侧先放量，还是进入更靠近 XPU 的 optical I/O | 决定 CPO optical engine、external laser、SiPh test 的爆发斜率 |
| STX / CMX attach rate | 决定 AI-native storage 是否从配套变成核心价值池 |
| 800VDC 改造速度 | 决定 1MW rack 是否能大规模部署 |
| OCS backlog 是否继续增加 | 决定 MEMS mirror、collimator、control board 的持续性 |
| glass-core substrate 是否进入 AI package 实际量产 | 决定玻璃基板 / TGV / glass inspection 是否从期权变主线 |
| SOCAMM2 是否从 NVIDIA Vera 扩展到更多 AI CPU / ASIC 平台 | 决定 SOCAMM2 connector / retention / socket 的第二增长曲线 |

---

# **19\. 风险与不确定性**

| 风险 | 影响方向 |
| ----- | ----- |
| Rubin ramp 延迟 | 影响 HBM4、SOCAMM2、1.6T、CPO、液冷、电源的短期兑现 |
| HBM4 良率 / 供给不足 | 限制 GPU / XPU 出货，推迟 probe / tester / underfill 扩张 |
| CoWoS-like 封装产能不足 | 先进封装设备和材料需求强，但系统出货受限 |
| CPO 良率和可维护性不达预期 | external laser、SiPh PIC、wafer optical test 爆发延迟 |
| 1.6T 光模块路线分歧 | DSP、LPO / LRO、CPO 价值分配可能变化 |
| 液冷现场可靠性问题 | QD / seals / leak detection 价值上升，但部署速度可能被拖慢 |
| 800VDC 数据中心改造慢 | HVDC 生态和 1MW rack 兑现推迟 |
| CXL memory pooling 软件生态不成熟 | CXL switch 和 memory expander 的高赔率延后 |
| STX / CMX attach rate 不高 | AI-native storage 可能停留在部分客户方案 |
| 玻璃基板量产验证慢 | glass-core substrate 仍是 1–2 年期权 |
| 客户自研和内部化 | hyperscaler 可能内部化部分 CXL software、OCS、AI storage、runtime |
| 公司业务多元导致投资纯度低 | 材料、连接器、传感、测试公司很多 AI 子线高增但整体财务不一定同步高增 |

---

# **20\. 最终筛选结论**

## **20.1 未来 6–12 个月最值得跟踪**

| 优先级 | 小组件 / 产品 | 为什么 |
| ----- | ----- | ----- |
| 1 | SOCAMM2 连接器 / compression socket / retention | Rubin 54TB LPDDR5X 直接拉动，模块已量产，连接器从小基数爆发 |
| 2 | 1.6T optical engine / DSP / EML / CW laser | 订单、架构升级和市场增速都已验证 |
| 3 | OCS MEMS mirror / fiber collimator / control board | OCS backlog 已验证，AI cluster 对低延迟 optical switching 需求上升 |
| 4 | HBM4 probe card / memory tester / burn-in socket | MI450 / Rubin HBM4 stack 存在百万级潜在需求 |
| 5 | CoWoS-like AOI / bump inspection / warpage metrology | 先进封装扩产必买，AI package 良率关键 |
| 6 | TCB / hybrid bonding / temporary bonding | HBM4 和 chiplet 强制拉动 |
| 7 | QD / seals / leak sensor / coolant service | 液冷大规模部署后，可靠性件和服务件增长可能高于冷板本体 |
| 8 | AI VRM / eFuse / high-current connector / Z-axis power | rack 功率密度和 XPU 电流密度同步上升 |
| 9 | AEC controller / 224G SerDes | rack 内短距高速铜连接仍强，CPO 不会立刻全面替代 |
| 10 | HBM underfill / RDL dielectric / Cu pillar plating | HBM4、CoWoS-R / L、fine pitch bump 共同拉动 |

---

## **20.2 未来 1–2 年最大赔率**

| 优先级 | 小组件 / 产品 | 为什么 |
| ----- | ----- | ----- |
| 1 | custom HBM base die / HBM PHY / HBM4E | HBM 正在从标准 DRAM 走向客户定制逻辑 \+ 内存 |
| 2 | CPO external laser source / SiPh PIC / wafer-level optical test | CPO 从 switch 侧放量后，激光和测试会成为瓶颈 |
| 3 | eDTC / silicon capacitor / on-package decap | 高功率 XPU 的 power integrity 隐形瓶颈 |
| 4 | glass-core substrate / TGV / glass inspection | 2027–2028 若量产突破，低基数增长很陡 |
| 5 | CXL switch / memory pooling switch | agentic inference 与长上下文推理推动 memory tiering |
| 6 | RDL dielectric / Cu pillar plating chemicals | CoWoS-R / L、HBM4、chiplet fine-pitch 共同拉动 |
| 7 | OCS MEMS / optical circuit switch | pod-scale AI cluster 需要低功耗、低延迟、低插损的 any-to-any optical connectivity |
| 8 | direct-to-silicon / microfluidic cooling | 1kW+ package 后传统冷板可能不足 |
| 9 | STX / CMX / AI-native storage | 长上下文、persistent memory、agent state 把 KV cache 变成存储层问题 |
| 10 | DSX / Dynamo / AI factory software | NVIDIA 正在把工厂建设、工厂运营和推理 runtime 产品化 |

---

# **21\. 最压缩但不删信息的总判断**

AI 基础设施下一轮瓶颈不是单一 GPU，而是一个完整“AI 工厂”系统。NVIDIA Vera Rubin 把 GPU、CPU、LPU、HBM4、SOCAMM2、NVLink 6、ConnectX-9、BlueField-4、STX / CMX、Spectrum-6 / CPO、DSX、Dynamo 和 800VDC 统一到一个架构里。AMD MI450、Google TPU、AWS Trainium3、Microsoft Maia、Meta MTIA 又把这些瓶颈扩散到非 NVIDIA 生态。

因此，未来 6–24 个月最值得下钻的不是“谁卖 GPU”，而是：

**HBM4 stack 数、SOCAMM2 模块数、1.6T 光口数、AEC endpoint 数、冷却点数、VRM 相数、测试工时、advanced packaging 检测次数、KV cache 外部化程度、CPO / OCS 的光耦合和测试良率。**

最确定的现在进行时：

**SOCAMM2 connector、AEC controller、1.6T optical DSP、200G EML / CW laser、HBM4 probe、CoWoS-like AOI、AI VRM、cold plate / CDU / QD、HBM underfill。**

最高赔率但更不确定：

**CXL switch、CPO optical engine、external laser source、SiPh wafer-level optical test、OCS MEMS、custom HBM base die、eDTC / silicon capacitor、glass-core substrate、STX / CMX、microfluidic cooling。**

最终一句话：

**短期看 SOCAMM2、1.6T 光、AEC、HBM4 测试、先进封装检测、液冷可靠性件；中期看 custom HBM、CPO、CXL memory pooling、AI-native storage、eDTC、玻璃基板和 800VDC。**

