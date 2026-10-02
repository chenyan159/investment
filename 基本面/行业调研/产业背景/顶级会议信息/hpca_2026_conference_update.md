# HPCA 2026 公开材料高密度调研：架构主线从“更多算力”转向“推理经济、内存墙、先进封装与可靠性”

资料口径：本报告只使用外部公开材料，不引用本项目内任何文件或历史信息。会议材料以 HPCA 2026 官方网站、官方 program、accepted papers、industry track、plenary keynote、Best of CAL 为主；市场数据以 Gartner、IDC、公司财报和公开市场研究为主。资料截至 2026-05-08。

## 1. 会议硬事实和主题密度

HPCA 2026 是第 32 届 IEEE International Symposium on High-Performance Computer Architecture，于 2026-01-31 至 2026-02-04 在澳大利亚悉尼举行，并与 CGO、PPoPP、CC 联合举办。官方主页明确将 HPCA 定位为计算机体系结构顶会，覆盖 processor/memory/storage、interconnect、accelerator、heterogeneous/reconfigurable systems、datacenter/cloud、security/reliability 等方向。

我从官方 Main Conference 的 Accepted Papers 页面抽取并去重得到 119 篇主会论文。按标题关键词粗分，多个方向会重叠，得到如下密度：

| 主题簇 | 论文标题命中数 | 代表性论文/信号 |
|---|---:|---|
| LLM/AI serving/inference/training/accelerator | 56 | RPU、PASCAL、SLINFER、ELORA、AUM、BitDecoding、VectorLiteRAG、V-Rex、PADE、WATOS、MoEntwine |
| PIM/CIM/near-data/memory systems | 35 | PIMphony、AQPIM、LoCaLUT、MPU、CoCoTree、PIM-malloc、BARD、ASPA、ReScue |
| GPU/datacenter/resource management | 23 | ARIADNE、muShare、QuCo、FlashFuser、Swift、LEGO、serverless LLM、spot instances |
| FPGA/reconfigurable/EDA/verification | 22 | TurboFuzz、TraceRTL、DP-HLS、NPUWattch、TENET-v2、design automation for NTT |
| Security/FHE/ZKP/side-channel | 16 | UniFHE、Peregrine、CROPHE、zkPHIRE、SCALE、DSASSASSIN、SSBleed、Protean |
| CXL/chiplet/MCM/wafer-scale | 14 | C3 CXL coherence、Cohet、deadlock-free chiplet bridge、HDPAT、FACE、TEMP、ReThermal |
| Reliability/sustainability | 12 | PinDrop、Architecting Resilience keynote、DRAM failure prediction、LLM voltage droops、Architectural Sustainability Indicator |
| Quantum architecture | 7 | QCCD、quantum LDPC、cryogenic decoder、TraceQ、distributed quantum compilation |

Industry Track 的 3 个题目非常关键，因为它们不是纯学术方向：IBM Telum II 的 enterprise on-chip accelerator integration、ByteDance cloud-native LLM inference characterization、Alibaba eGPU production-scale elastic sharing over 10,000 GPUs。Plenary Keynotes 的 3 条主线也很一致：Oracle 的云规模漏洞检测、MIT 的 Compiler 2.0/ML compiler、AMD 的大规模可靠性架构。Best of CAL 则补了 3 个方向：AI agents for computer architecture 的 QuArch、架构可持续性指标、真实硬件 per-row activation counting。

结论先行：HPCA 2026 的转折不是“又多了一批 AI 加速器论文”，而是研究重心从峰值 FLOPS 转到 5 个更接近量产和利润的瓶颈：推理调度和 token 成本、内存容量/带宽/价格、CXL/Chiplet/Wafer 的互联一致性、规模化可靠性、安全隐私计算。

## 2. 重点发展方向和与过去相比的转折

### 2.1 Agentic AI 把架构问题从训练吞吐改成推理经济

会议中 LLM/AI 相关论文约 56 篇，占 119 篇主会论文的接近一半。更重要的是，论文名称已经从“训练更快”转向“推理服务更便宜、更稳定、更可调度”：RPU - A Reasoning Processing Unit、The Cost of Dynamic Reasoning、PASCAL reasoning-based LLM scheduling、SLINFER serverless LLM inference、ELORA multi-LoRA/KV cache management、VectorLiteRAG、BitDecoding low-bit KV cache、V-Rex streaming video LLM KV cache retrieval。

技术转折：2023-2025 市场主要买 GPU 做训练和大模型扩容，2026 的学术信号是 reasoning、agents、RAG、多 LoRA、长上下文、视频 LLM 会把在线推理推成最大成本中心。未来一年的胜负不是单卡 TFLOPS，而是单位 token 成本、GPU 利用率、KV cache 层级、prefill/decode 分离、批处理和 SLA 调度。

商业转折：Gartner 预计 2026 年全球 AI 支出为 USD 2.528 万亿，其中 AI infrastructure 为 USD 1.366 万亿；IDC 预计 2026 年 data center semiconductor revenue 为 USD 477.1B，其中 CPUs/AI accelerators/GPUs/custom ASICs/networking silicon 等 intelligent datacenter segment 为 USD 281B。NVIDIA FY2026 Data Center revenue 已达 USD 193.7B，FY2026 全公司 non-GAAP gross margin 71.3%，Q4 FY2026 gross margin 75.2%。这意味着“推理效率软件/系统”会直接吃掉数百亿美元级硬件采购效率红利。

### 2.2 内存从配角变成战略资产，PIM/CXL 是内存墙的两条路线

HPCA 2026 的内存相关论文非常密集：PIMphony、LoCaLUT、AQPIM、The Memory Processing Unit、CoCoTree、PIM-malloc、BARD、ASPA、RoMe、Pulse、ReScue、MIRZA、SALT。Best of CAL 也把真实硬件 row activation counting 放在显眼位置。

技术转折：过去内存论文多是 cache、prefetch、DRAM row buffer 优化；现在变成三层问题：HBM/DRAM 的物理供给紧张，CXL 负责容量池化和异构一致性，PIM/CIM 负责把部分计算搬到数据附近。HPCA 论文里 CXL 不只是“扩内存”，而是 coherence controller、full-system simulation、CXL memory reliability。PIM 不再只是概念，已经绑定 long-context LLM、activation quantization、LUT inference、collective communication 和 dynamic allocator。

商业转折：Gartner 预计 2026 年全球 semiconductor revenue 超过 USD 1.320T，同比增长 64%；其中 memory revenue 从 2025 年 USD 216.3B 升到 2026 年 USD 633.3B，DRAM 与 NAND 年度价格分别上升 125% 和 234%。IDC 口径更具体：2026 年 total memory revenue 为 USD 594.7B，DRAM 为 USD 418.6B，同比增长 177%，NAND 为 USD 174.1B，同比增长 138.5%。SK hynix 2026Q1 revenue KRW 52.576T，operating margin 72%，这在历史上非常反常，说明 AI 内存短缺正在把 memory 从周期品改造成战略约束。

### 2.3 Chiplet/MCM/Wafer-scale 从“封装故事”变成系统架构问题

HPCA 2026 出现了 C3 CXL Coherence Controllers、Deadlock-Free Bridge Module for Inter-Chiplet Communication、COMET for MCM accelerators、LRM-GPU multi-chiplet GPU、HDPAT wafer-scale GPUs、WATOS wafer-scale LLM training、MoEntwine wafer-scale expert parallel inference、ReThermal liquid-cooled wafer-scale LLM training、TEMP wafer tensor partition mapping。

技术转折：Chiplet 不再只是降低 die cost 或先进封装产能问题，而是 coherence、deadlock、page address translation、thermal scheduling、expert parallel、collective communication、compiler/runtime co-design 的问题。Wafer-scale 的真实路线也不是“一整片晶圆替代 GPU”，而是通过 expert parallel、静态/动态热调度、tensor mapping、液冷和内存层级把不可切分的大模型 workload 变成可制造系统。

商业转折：先进封装市场 2025 年约 USD 40.86B，2026 年约 USD 44.07B，长期 CAGR 约 7.6%。但这个均值会掩盖 AI 2.5D/CoWoS/HBM packaging 的供需紧张。TSMC 2026Q1 revenue USD 35.9B，gross margin 66.2%，2Q26 guidance gross margin 65.5%-67.5%，说明先进节点加先进封装链条仍有很强定价权。HPCA 给出的信号是：封装和互联会从“制造 bottleneck”升级成“架构 moat”。

### 2.4 可靠性、安全和可持续性不再是成本中心

AMD keynote 是 Architecting Resilience at Scale，Oracle keynote 是云规模漏洞检测，Best of CAL 有 Architectural Sustainability Indicator。主会里 PinDrop 研究 large-scale fleet SDCs，Exploration of LLM Workload Reliability 研究 di/dt effects and voltage droops，ReScue 做 reliable/secure CXL memory，MIRZA/SALT 做 Rowhammer 防御，DSASSASSIN/SSBleed/Protean 做跨 VM/Arm/Spectre 防御，FHE/ZKP 方向至少包括 UniFHE、Peregrine、CROPHE、zkPHIRE。

市场转折：AI 集群一旦进入 10,000 GPU、100,000 GPU 级别，可靠性和安全不再是“合规开销”。它们会影响 GPU 可用率、重算成本、SLA、数据泄露风险和保险/审计成本。Alibaba eGPU 题目直接写 production-scale elastic sharing over 10,000 GPUs，ByteDance 题目直接写 cloud-native LLM inference characterization，这类工业题目说明市场已经在真实集群里遇到调度、隔离、利用率、故障和安全问题。

### 2.5 AI for architecture/EDA 是新的工具链红利

Compiler 2.0 keynote、QuArch、NPUWattch、TraceRTL、TurboFuzz、TENET-v2、AutoHAAP、Nugget 等题目说明 AI 已经开始反过来改造架构设计、验证、建模和编译。EDA software market 2026 年约 USD 15.9B 至 USD 17.9B，不是最大市场，但毛利率和粘性高。更重要的是，它会决定 custom ASIC、chiplet、NPU、PIM 的迭代速度。

## 3. 哪些产品和技术会爆发：三档路线判断

### 3.1 Agentic inference stack：推理调度、KV cache、RAG、multi-LoRA、reasoning accelerator

当前市场规模：可直接映射到 IDC 的 2026 年 intelligent datacenter semiconductor segment USD 281B、Gartner 的 2026 年 AI infrastructure USD 1.366T、NVIDIA FY2026 Data Center revenue USD 193.7B。软件层市场规模更难单独拆分，但其经济影响会通过 GPU 采购、云推理成本和 utilization 释放体现。

| 口径 | 未来一年路线 | 增速和利润率判断 |
|---|---|---|
| 基准 | 2026-2027 年先在 hyperscaler、AI cloud、头部互联网公司落地：prefill/decode 分离、KV cache quantization、multi-LoRA serving、RAG resource partitioning、serverless inference。 | 相关硬件收入 +30%-45%；推理系统软件收入 +40%-70%，但绝对规模仍小。GPU/ASIC gross margin 60%-75%；云推理服务 gross margin 20%-45%，取决于利用率和电力成本。 |
| 乐观 | Reasoning/agent workload 的 token 消耗继续超预期，企业 agent 开始规模化，调度系统成为采购 GPU 前的必配层。 | 相关硬件 +50%-70%；推理优化软件/平台 +80%-120%。高端 AI silicon gross margin 65%-78%；云服务毛利率因利用率提升上行 3-8 pct。 |
| 超预期乐观 | RPU/专用 reasoning unit 或推理 ASIC 出现可量产产品，部分 decode/KV/RAG workload 从通用 GPU 转移到专用芯片或 on-package accelerator。 | 新增专用推理芯片市场 12 个月内可到 USD 5B-15B 设计赢单/采购额，但真正出货利润滞后。早期 ASIC 毛利率 45%-65%，若绑定云服务可更高。 |

爆发强度：强。它会先体现在 NVIDIA/AMD/custom ASIC、云推理平台、GPU 云利用率和网络/内存采购上，而不是先出现一个独立的“RPU 大市场”。

### 3.2 Memory supercycle：HBM、server DRAM、eSSD、CXL memory、PIM/CIM

当前市场规模：Gartner 2026 memory revenue USD 633.3B；IDC 2026 memory revenue USD 594.7B，其中 DRAM USD 418.6B，NAND USD 174.1B。CXL memory expansion 2025 年约 USD 1.3B、2026 年约 USD 1.67B。CIM chip market 2025 年约 USD 0.5B、2026 年约 USD 0.688B。HBM-only 的公开市场口径分歧很大，2026 年常见公开估计从约 USD 4B 到 USD 18B+ 不等；更可靠的判断是，HBM 通过占用 wafer/packaging capacity 抬高了整个 DRAM/eSSD 曲线。

| 口径 | 未来一年路线 | 增速和利润率判断 |
|---|---|---|
| 基准 | HBM3E/HBM4、server DDR5、eSSD 继续缺货；CXL 从 qualification 和小批量部署进入更多 AI inference memory tier；PIM/CIM 仍以论文、prototype、少量专用客户为主。 | DRAM revenue +100%-180%，NAND +80%-140%；CXL +25%-35%；PIM/CIM +30%-50%。SK hynix 72% operating margin 很可能不可长期维持，但 2026 年 memory vendor operating margin 45%-70% 仍合理。 |
| 乐观 | HBM4 产能爬坡顺利，CXL memory tier 被用于 KV cache/embedding/in-memory DB，PIM 在 long-context LLM 中出现早期商用加速卡或内存模块。 | 高端 AI memory +80%-150%；CXL +40%-60%；PIM/CIM +60%-100%。利润率保持高位，HBM/server DRAM gross margin 60%-75%，CXL 模块 35%-55%。 |
| 超预期乐观 | Memory shortage 延续到 2027，HBM 和 enterprise SSD 被长期锁单；PIM 与 HBM/DRAM 绑定销售，变成“高端内存 SKU”的差异化功能。 | memory revenue 超过 Gartner/IDC 基准 10%-20%；CXL 2026 收入冲到 USD 2B+；PIM/CIM 2026 收入冲到 USD 1B+。利润率上行但伴随客户反弹和监管/长协重定价风险。 |

爆发强度：最强，且最可能“违背市场共识”。市场常把内存当周期股，HPCA 和 IDC/Gartner 数据共同指向 2026 年内存是 AI 的战略瓶颈。

### 3.3 Chiplet、advanced packaging、wafer-scale、liquid-cooled high-density AI systems

当前市场规模：advanced packaging 2026 年约 USD 44.07B；TSMC 2026Q1 revenue USD 35.9B，gross margin 66.2%，2Q26 gross margin guidance 65.5%-67.5%。Wafer-scale 单独市场仍小，主要体现为 Cerebras 等少数系统和未来定制 AI cluster，但 HPCA 论文密度已明显上升。

| 口径 | 未来一年路线 | 增速和利润率判断 |
|---|---|---|
| 基准 | 2.5D/HBM packaging 继续紧张；chiplet coherence、interposer、bridge、thermal scheduling 成为 AI ASIC 量产必要条件。 | advanced packaging +8%-12%；AI/HBM 相关先进封装子段 +25%-40%。Foundry gross margin 60%+；OSAT/packaging 20%-35%，高端 CoWoS/SoIC 更高。 |
| 乐观 | Hyperscaler custom ASIC 和 GPU 迭代推动 MCM/wafer-scale 设计增加，液冷和高密度 rack 系统绑定销售。 | advanced packaging +15%-25%；AI 先进封装子段 +40%-70%。高端封装产能议价能力继续上行。 |
| 超预期乐观 | Wafer-scale 或 large MCM 在 MoE inference/training 上证明显著 TCO 优势，进入 1-2 家 hyperscaler 二供/定制路线。 | 新增 wafer-scale/large-MCM 系统订单 USD 1B-5B，但量产交付仍受良率、散热、软件生态限制。早期系统毛利率可能 30%-50%，取决于是否绑定服务。 |

爆发强度：中强。真正的 alpha 不是“谁会做 chiplet”，而是谁掌握封装产能、散热、系统软件、compiler/runtime 和供应链长协。

### 3.4 GPU fabric、DPU/SmartNIC、in-switch computing、elastic GPU sharing

当前市场规模：DPU 市场公开口径差异较大，2026 年约 USD 2.63B 至 USD 4.5B；SmartNIC+DPU 2025 年约 USD 1.1B，2035 年约 USD 4.2B 的保守口径也存在。更大市场嵌在 IDC 2026 data center semiconductor USD 477.1B 和 NVIDIA data center networking/compute 平台里。HPCA 题目中 Alibaba eGPU over 10,000 GPUs、Sassy SmartNIC-assisted RDMA、in-switch LLM tensor-parallelism 都指向同一件事：AI cluster 的利用率瓶颈越来越靠近网络和资源池化。

| 口径 | 未来一年路线 | 增速和利润率判断 |
|---|---|---|
| 基准 | GPU sharing 从内部平台扩散到云服务；RDMA notification、DPU offload、network scheduling 成为 AI cloud 差异化。 | DPU/SmartNIC +20%-35%；AI networking silicon +30%-50%。Silicon gross margin 50%-70%；NIC/system gross margin 25%-45%。 |
| 乐观 | In-network compute 用于 tensor parallel、collective communication、KV transfer，云厂商采购更高端 NIC/switch ASIC。 | DPU/SmartNIC +40%-60%；AI networking +60%-90%。利润率随软件绑定上行。 |
| 超预期乐观 | 弹性 GPU 池化成为企业/政府 AI 云标配，10,000 GPU 级资源池复制到多家云厂商。 | 资源池化软件和 DPU attach rate 快速提升，新增软件/控制面市场 USD 1B-3B；硬件拉动更大。 |

爆发强度：强，但收入不一定在“DPU 公司”单独体现，更多体现在 NVIDIA networking、Broadcom/Marvell custom silicon、云平台和整机厂。

### 3.5 FHE/ZKP/confidential multi-GPU/security accelerator

当前市场规模：privacy-enhancing computation 2026 年约 USD 6.9B-7.28B；homomorphic encryption 单独市场约 USD 0.23B-0.33B。HPCA 2026 的 FHE/ZKP 论文密度远高于这个当前收入规模，说明技术关注度领先商业收入。

| 口径 | 未来一年路线 | 增速和利润率判断 |
|---|---|---|
| 基准 | FHE/ZKP 仍以金融、医疗、政府、Web3、数据协作为早期市场；加速器以 FPGA/GPU kernel/ASIC prototype 为主。 | PET +20%-30%；FHE +10%-35%。软件毛利 70%+，硬件和服务早期利润率低甚至负。 |
| 乐观 | AI data clean room、跨机构隐私推理、confidential multi-GPU ML 带来商业 PoC，FHE accelerator 出现少量生产部署。 | PET +35%-50%；FHE +40%-80%。硬件毛利 35%-55%，软件/服务 60%-80%。 |
| 超预期乐观 | 合规/主权 AI 要求推动“密文推理/可验证计算”成为云 AI SKU，ZKP/FHE ASIC 被头部云验证。 | FHE/ZKP 加速器订单可到 USD 0.5B-1B，但收入确认和生态成熟慢。 |

爆发强度：中。技术含金量高，商业化一旦发生会很陡，但未来 12 个月更像“设计赢单和 PoC 爆发”，不是大规模利润兑现。

### 3.6 AI-EDA、compiler/runtime、hardware verification

当前市场规模：EDA market 2025 年约 USD 17.53B，另有 EDA software 2026 年约 USD 15.89B 的口径。HPCA 的 Compiler 2.0 keynote、QuArch、TraceRTL、TurboFuzz、NPUWattch、TENET-v2 表明设计自动化正在向 AI-assisted architecture search、performance modeling、RTL evaluation、verification fuzzing 延伸。

| 口径 | 未来一年路线 | 增速和利润率判断 |
|---|---|---|
| 基准 | AI 辅助编译、验证、性能建模作为 Synopsys/Cadence/Siemens 和 hyperscaler internal tools 的增强功能。 | EDA +8%-12%；AI-EDA 子功能 +20%-40%。软件 gross margin 75%-90%，订阅粘性高。 |
| 乐观 | Custom ASIC 迭代压力导致 AI-EDA 进入 signoff 前 workflow，硬件验证和 architecture exploration 周期明显缩短。 | AI-EDA 子市场 +50%-80%，但基数仍小。 |
| 超预期乐观 | AI agents 能稳定生成/验证 microarchitecture snippets，QuArch 类 benchmark 变成工具链评测标准。 | 可能产生 USD 0.5B-1B 新增 ARR 机会，但需要可信验证和 IP 责任边界成熟。 |

爆发强度：中强。它不会像 GPU/HBM 那样爆收入，但会放大 custom ASIC、chiplet 和 NPU 的研发效率。

### 3.7 Quantum architecture

当前市场规模：McKinsey 估计 quantum computing companies 2025 年全球收入超过 USD 1B，2028 年可能到 USD 4.4B；同时 2025 年 quantum technology startup investment 达 USD 12.6B，其中约 90% 流向 quantum computing。HPCA 2026 有 7 篇 quantum architecture 相关论文，集中在 QCCD、LDPC decoding、cryogenic decoder、compilation/simulation/dataflow。

| 口径 | 未来一年路线 | 增速和利润率判断 |
|---|---|---|
| 基准 | 仍以 cloud access、政府/企业 PoC、科研系统为主；硬件架构论文领先商业交付 3-7 年。 | 收入 +20%-35%；多数硬件公司 operating margin 为负。 |
| 乐观 | Hybrid quantum-classical workflow 在金融、化学、优化场景增加预算。 | 收入 +40%-60%；服务/云访问毛利改善，但整体仍亏损。 |
| 超预期乐观 | 某类 error correction/decoder/control electronics 路线显著降低扩展成本，引发资本和订单重估。 | 12 个月收入翻倍可能存在，但更可能是估值和融资爆发，不是利润爆发。 |

爆发强度：弱到中。技术很重要，但和 GPU/HBM/CXL/PIM 不是同一个商业时间尺度。

## 4. 重要市场规模、未来一年增速、利润率表

| 产品/技术 | 2026 当前市场规模或锚 | 基准未来一年 | 乐观未来一年 | 超预期乐观 | 当前/未来利润率走势 |
|---|---:|---:|---:|---:|---|
| AI infrastructure | Gartner: USD 1.366T | +35%-45% | +50%-60% | +70%+ | 硬件高毛利，服务毛利取决于利用率；推理优化提高云毛利 |
| Intelligent datacenter silicon | IDC: USD 281B | +30%-45% | +50%-70% | +80%+ | GPU/ASIC 60%-75% gross margin，竞争加剧后分化 |
| NVIDIA Data Center | FY2026 USD 193.7B | +40%-60% | +70% | +90% | FY2026 non-GAAP GM 71.3%，Q4 75.2%；短期仍高 |
| Total semiconductor | Gartner: 2026 USD 1.320T；IDC: 2026 USD 1.29T | +20%-25% 到 2027 | +30% | +40% | 利润集中在 AI silicon、memory、foundry/packaging |
| Memory total | Gartner: 2026 USD 633.3B；IDC: USD 594.7B | +10%-25% after huge 2026 jump | +30%-40% | +50% | SK hynix 2026Q1 OM 72%；2027 前仍高但波动大 |
| DRAM | IDC: 2026 USD 418.6B | +15%-35% | +50% | +70% | HBM/server DRAM 定价强，commodity DRAM 受挤压 |
| NAND/eSSD | IDC: 2026 USD 174.1B | +10%-25% | +35% | +50% | enterprise SSD 强于消费 NAND |
| CXL memory expansion | 2025 USD 1.3B；2026 USD 1.67B | +25%-35% | +40%-60% | +80% | 早期模块/控制器毛利 35%-55%，软件池化更高 |
| CIM/PIM chip | 2025 USD 0.5B；2026 USD 0.688B | +30%-50% | +60%-100% | +100%+ | 独立硬件利润早期不稳，若绑定 HBM/DRAM SKU 则改善 |
| Advanced packaging | 2026 USD 44.07B | +8%-12% | +15%-25% | +30% | TSMC 2026Q1 GM 66.2%；OSAT 较低，高端封装溢价 |
| DPU/SmartNIC | 2026 USD 2.6B-4.5B | +20%-35% | +40%-60% | +80% | Silicon 50%-70%；系统卡 25%-45%；软件控制面上行 |
| Privacy-enhancing computation | 2026 USD 6.9B-7.28B | +20%-30% | +35%-50% | +70% | 软件高毛利，FHE/ZKP 硬件早期低利润 |
| Homomorphic encryption | 2026 USD 0.23B-0.33B | +10%-35% | +40%-80% | +100%+ | 小市场，高研发，盈利滞后 |
| EDA/AI-EDA | EDA 2025 USD 17.53B；EDA software 2026 USD 15.89B | +8%-12% | +15%-25% | +30% | 订阅软件 GM 75%-90%，AI 功能提升 ARPU |
| Quantum computing | 2025 revenue > USD 1B；2028 up to USD 4.4B | +20%-35% | +40%-60% | +100% | 多数硬件公司仍亏损，服务毛利先改善 |

## 5. 与当前市场可能相违背的重要洞见

1. 内存可能比 GPU 更稀缺。市场通常把 AI 看成 GPU shortage，但 Gartner/IDC 的 2026 数据显示 memory revenue 增幅远超 non-memory，DRAM 和 NAND 价格上行会影响 AI server、PC、mobile、edge 乃至汽车。HPCA 的 PIM/CXL/Rowhammer/reliability 密度也说明瓶颈已从 compute 转向 memory hierarchy。

2. CXL 不是 2026 年最大收入爆点，但可能是 2027-2029 年服务器架构重构的入口。当前 CXL 市场只有十亿美元级，和 GPU/HBM 不是一个量级；但 HPCA 的 CXL coherence、CXL simulation、CXL memory reliability 说明真正难点是可预测延迟、一致性、可靠性和软件分层，不是把 DRAM 插到 PCIe 上。

3. PIM/CIM 未来一年最可能以“高端内存差异化功能”赚钱，而不是以独立 PIM 芯片赚钱。HPCA 的 LoCaLUT、PIMphony、AQPIM 都和 LLM 内存容量/带宽痛点绑定。若 PIM 能减少 HBM/DRAM 数据移动，它的经济价值会通过 HBM ASP、memory vendor margin 和 AI server TCO 体现。

4. Agentic AI 会同时降低单 token 成本、提高总 token 消耗。市场容易只看 quantization、KV cache、sparse attention 带来的单位成本下降，但 The Cost of Dynamic Reasoning、RPU、PASCAL 这类论文暗示 reasoning 会创造更高总推理需求。结论是：效率优化不会必然减少硬件需求，反而可能扩大可经济运行的 agent 应用集合。

5. 可靠性会成为 AI cluster 的利润项。PinDrop、AMD resilience keynote、LLM voltage droop、CXL reliable memory 都指向同一个问题：当集群规模上万卡，silent data corruption、重算、掉卡、内存错误、side-channel 和漏洞检测都能直接影响毛利率。

6. Wafer-scale 的瓶颈不是“能不能做一大片芯片”，而是 thermal/runtime/compiler/memory mapping。HPCA 的 ReThermal、TEMP、HDPAT、WATOS、MoEntwine 说明 wafer-scale 成熟路线需要系统工程，短期超预期订单可能有，但可复制量产要看软件栈。

7. Quantum 会吸引资本，但未来一年很难成为收入主线。HPCA quantum 论文偏 fault tolerance、decoder、compilation、dataflow，McKinsey 的收入规模仍是十亿美元级。它更像 2026 年的战略期权，而不是可以替代 AI/HBM/CXL 的主线。

8. AI-EDA 可能是被低估的“卖铲子”。HPCA 出现 QuArch、Compiler 2.0、TraceRTL、TurboFuzz、NPUWattch，说明 AI agent 正在进入架构设计和验证。这个市场规模小于 GPU/HBM，但毛利率高、客户粘性强、会直接加速 ASIC 和 chiplet 迭代。

## 6. 未来 12 个月最该跟踪的验证指标

1. NVIDIA/AMD/custom ASIC 的推理收入占比、Blackwell/Rubin/MI 系列的 inference benchmark 和 cost per token。
2. HBM4/HBM3E 产能锁单、HBM stack 良率、server DRAM ASP、enterprise SSD ASP。
3. CXL Type 3 memory module 从 qualification 到 production 的客户数量，CXL switch 和 memory pooling software 的真实部署。
4. PIM/CIM 是否进入 SK hynix/Samsung/Micron 的商业 SKU，而不只是学术 prototype。
5. AI cloud 的 GPU utilization、preemption/elastic sharing、multi-tenant isolation、DPU attach rate。
6. 先进封装产能扩张：CoWoS/SoIC/2.5D interposer、hybrid bonding、HBM packaging bottleneck。
7. Large-scale reliability 指标：SDC rate、GPU failure rate、job restart cost、memory error rate、voltage droop。
8. FHE/ZKP 是否有生产级云 SKU 或 ASIC design win。
9. AI-EDA 是否能进入 signoff/verification，而不是只做辅助代码生成。
10. Quantum 订单是否从 PoC 变成 repeatable cloud workflow revenue。

## 7. 信息源

- HPCA 2026 官方主页：https://2026.hpca-conf.org/
- HPCA 2026 Main Conference / Accepted Papers：https://conf.researchr.org/track/hpca-2026/hpca-2026-main-conference
- HPCA 2026 Industry Track：https://2026.hpca-conf.org/track/hpca-2026-industry-track
- HPCA/CGO/PPoPP/CC 2026 Plenary Keynotes：https://2026.hpca-conf.org/track/hpca-cgo-ppopp-cc-2026-plenary-keynotes
- HPCA 2026 Best of CAL：https://2026.hpca-conf.org/track/hpca-2026-best-of-cal
- Gartner, Worldwide AI Spending 2026：https://www.gartner.com/en/newsroom/press-releases/2026-1-15-gartner-says-worldwide-ai-spending-will-total-2-point-5-trillion-dollars-in-2026
- Gartner, Worldwide Semiconductor Revenue 2026：https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026
- IDC, Semiconductor Market Forecast 2026：https://www.idc.com/resource-center/blog/semiconductor-market-to-surge-past-the-trillion-dollar-threshold-ai-infrastructure-drives-market-growth/
- NVIDIA FY2026 financial results：https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/
- SK hynix 2026Q1 financial results：https://www.prnewswire.com/news-releases/sk-hynix-announces-1q26-financial-results-302750959.html
- TSMC 2026Q1 quarterly results：https://investor.tsmc.com/english/quarterly-results/2026/q1
- McKinsey Quantum Technology Monitor 2026：https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/mckinsey-quantum-technology-monitor-2026-a-commercial-tipping-point
- Advanced packaging market sizing：https://www.towardspackaging.com/insights/advanced-packaging-market-sizing
- CXL memory expansion market sizing：https://marketintelo.com/report/cxl-memory-expansion-market
- Compute-in-memory chip market sizing：https://www.gminsights.com/industry-analysis/compute-in-memory-cim-chip-market
- DPU market sizing：https://www.fortunebusinessinsights.com/data-processing-unit-market-115828
- Privacy-enhancing computation market sizing：https://www.strategymrc.com/report/privacy-enhancing-computation-market
- Homomorphic encryption market sizing：https://www.fortunebusinessinsights.com/homomorphic-encryption-market-111218
- EDA market sizing：https://www.globenewswire.com/news-release/2026/04/08/3270311/0/en/electronic-design-automation-eda-market-size-to-hit-42-85-billion-by-2035-research-by-sns-insider.html
