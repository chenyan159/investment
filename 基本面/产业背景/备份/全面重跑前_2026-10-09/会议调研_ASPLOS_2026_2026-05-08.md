# ASPLOS 2026会议更新：AI系统从“模型扩张”进入“推理、内存与全栈协同”时代

> 调研日期：2026-05-08。资料范围：只使用公开互联网资料，包括ASPLOS 2026官方日程/奖项/Workshop页面、公开演讲页面、公开论文/新闻稿/市场预测；未参考本项目目录内任何文件或信息。

## 一页结论

ASPLOS 2026的核心信号不是“又有更多AI论文”，而是计算系统研究的重心已经从训练大模型转向可规模化、可盈利、可验证的AI生产系统。官方主会在2026年3月24-26日安排了167篇unique papers，每篇25分钟报告；3月22-23日是workshop/tutorial；ASPLOS还要求报告统一录制，这意味着公开材料后续会继续增加。主会3个keynote分别来自Google、UC Berkeley/Databricks/Anyscale、IBM，主题正好覆盖AI基础设施全栈协同、AI stack/Ray/vLLM/SGLang/LMArena、以及企业级高可靠系统。

最重要的产业判断：2026-2027的系统瓶颈不是“有没有模型”，而是每token成本、KV cache、HBM/DRAM/NAND供应、CXL/分解式内存、跨GPU通信、可靠性和能耗。对应到市场，IDC预计2026年AI基础设施支出4870亿美元、同比约+53%；Gartner预计2026年全球AI支出2.53万亿美元、AI基础设施1.37万亿美元、AI软件4525亿美元；Gartner还预计2026年半导体收入1.32万亿美元，其中AI半导体约占30%，内存收入6333亿美元，DRAM/NAND价格分别上涨125%/234%。这解释了ASPLOS 2026为什么会出现密集的LLM serving、CXL、PIM、tiered memory、FHE、TEE、AI for architecture design论文。

最反共识的更新：市场仍把“算力”当作单一指标，但ASPLOS 2026展示的是“内存和调度成为新摩尔定律”。未来一年最可能爆发的产品不是单个模型，而是四类系统产品：推理服务控制平面、HBM/先进内存和CXL内存池、AI加速器+互连的rack-scale系统、AI辅助芯片/系统设计工具。边缘AI/AI PC会大量出货，但利润兑现弱于出货；FHE/量子会继续被资本关注，但2027年前仍是小市场、强研发、弱利润。

## 会议事实与主题密度

### 官方事实

- 时间地点：ASPLOS 2026在Pittsburgh, USA举行，会议日期为2026年3月22-26日，主会为3月24-26日。
- 主会规模：官方Program写明“167 unique papers”，每篇报告25分钟，主会每天8:30开始、18:00左右结束。
- Workshop/Tutorial：官方列表包含16个workshop和13个tutorial。
- Keynote 1：Partha Ranganathan, Google，主题是智能时代的软硬件垂直协同，强调AI基础设施从数据中心硬件到云软件的全栈共设计。
- Keynote 2：Ion Stoica, UC Berkeley，主题是AI stack，覆盖Ray、vLLM、SGLang、LMArena，直接把“训练/推理/评测”串成基础设施问题。
- Keynote 3：Hillery Hunter, IBM，主题是mission-critical enterprise systems，强调IBM Z/Power系统的99.999999% uptime，以及AI fraud detection、insurance claims、AIOps对企业级处理器和系统可靠性的改变。
- 录制与材料：官方presentation guideline要求统一用会议设备/Zoom账户进行录制，报告slides需在2026年3月22日前上传，因此后续公开视频/slide会持续补全。

### 论文session的结构性变化

按官方session标题粗分，ASPLOS 2026至少有13个session直接围绕LLM/ML/Generative AI/GPU/AI accelerator/tensor programs/on-device AI，保守约60-70篇论文；若把CXL KV cache、PIM for LLM、FHE GPU、low-bit quantization、profiling和AI for compiler纳入，AI相关论文接近或超过全会40%。

最密集的方向如下：

- LLM Serving：1A LLM Serving: Throughput Optimization、1B LLM Serving: Latency & Scheduling、2B Speculative Decoding、3A LLM Attention & KV Cache、3B Mixture-of-Experts & Efficient Inference、5A Generative Model Serving。
- 训练与编译：2A LLM Training Systems、4A ML Training & Monitoring、4B ML Compilers & Tensor Programs、7B Compilers & Code Generation、9A Systems Profiling & Optimization。
- 内存墙：1D CXL & Memory Fabric、2D DRAM Reliability & Security、4D Processing-in-Memory、6D Disaggregated Memory Systems、8C Memory Hierarchy & Performance。
- 可信和可靠：3D Trusted Execution Environments、5C Formal Verification、7A Fully Homomorphic Encryption、7C Testing & Fuzzing、9C Reliability & Fault Tolerance。
- 新计算：1C Quantum Computing: Compilation、4C Quantum Error Correction、9B Quantum & Emerging Computing。
- 边缘/视觉/渲染：3C 3D Gaussian Splatting & Rendering、5B On-Device & Edge AI、VisArch workshop。

### Best Paper信号

ASPLOS 2026 Best Paper Awards包括5篇：CounterPoint、Finding Reusable Instructions via E-Graph Anti-Unification、Lifetime-Aware Design of Item-Level Intelligence、PF-LLM、vCXLGen。它们分别对应微架构测量、编译器/指令复用、极端边缘智能、LLM提示硬件预取、CXL bridge自动综合与验证。这组获奖名单的含义很强：最佳论文没有集中给“更大模型”，而是给了可测量、可生成、可验证、可部署的系统机制。

Honorable Mentions也很有指向性：RowArmor、MSCCL++、PACT、M2XFP、RedFuser、SuperOffload、Graphiti等，分别指向DRAM攻击防护、GPU通信抽象、tiered memory、低比特量化格式、AI accelerator算子融合、大模型训练offload、可验证乱序执行。

## 重点发展方向与和此前市场/技术的变化

### 1. LLM推理从“单机吞吐优化”转向“生产调度系统”

ASPLOS 2026的LLM serving论文标题已经像云系统产品路线图：Prefill-decode Multiplexing、Dynamic Spatial-Temporal Orchestration、Breaking the Silos、Shift Parallelism、Production Serving for Dynamic LLM Workloads、Prefix-Aware Attention、Lossless Compression、Resource-Aware Batching、Adaptive Precision Expert Offloading、Disaggregated Speculative Decoding、Long-context Reasoning with Speculative Context Sparsity。

技术变化：2023-2025市场主要买GPU训练集群；2026转向推理集群的利用率、尾延迟、KV cache、prefill/decode拆分、MoE expert放置、speculative decoding、DiT/多模态生成服务。单卡FLOPS不再是唯一卖点，调度器和内存层级可以改变有效毛利。

产业变化：IDC口径下2025年AI基础设施支出已达3180亿美元，2026年预计4870亿美元；其中Q4 2025 AI基础设施支出899亿美元，服务器占877亿美元/97.6%（按IDC披露为Q4 2025的AI infrastructure结构）。这意味着“让同一批GPU多吐token”的软件，哪怕提升10%-20%有效利用率，也是在数百亿美元级硬件池上做利润再分配。

### 2. 内存成为系统定价权核心：HBM、DRAM、CXL、PIM同时升温

ASPLOS 2026的内存主题不是传统cache小修小补，而是围绕AI基础设施的成本墙展开：CXL memory tiering、CXL bridge synthesis/verification、CXL shared-memory model checking、disaggregated memory programming model、CXL pod allocator、DRAM disturbance attacks、PIM、tiered memory、heterogeneous memory predictability、LLM-hinted hardware prefetching。

市场变化极其剧烈：Gartner预计2026年半导体收入1.3202万亿美元，同比增长64%；内存收入从2025年的2163亿美元升至2026年的6333亿美元，2027年7481亿美元。IDC则预计2026年DRAM收入4186亿美元，同比+177%；NAND收入1741亿美元，同比+138.5%。这说明“内存墙”已经不是性能话题，而是利润池和供应链话题。

重要转折：此前CXL常被市场视为“慢内存扩容”，但ASPLOS 2026把CXL放在主会第一天同一时段的独立session，且vCXLGen获Best Paper。对AI推理，CXL未必替代HBM，但可以承接KV cache、冷权重、租户隔离、内存池化、容错恢复等“容量优先”的负载。

### 3. AI for Systems Design成为显性赛道，不再只是EDA局部自动化

Architecture 2.0 workshop的主题是AI for Computing Systems Design，日程包括Lightweight AI for Resource Management、Datacenter Management Policy Optimization、Multi-Agent SoC Generation、AccelOpt、ArchAgent、EggMind、AC Loop等。更重要的是，它还设置QuArch竞赛，用architecture/system问题来评估AI agent的系统推理能力，并试用ArchScholar做AI辅助反馈。

这代表一个转折：过去AI辅助芯片设计多集中在placement、routing、EDA局部优化；ASPLOS 2026把目标扩大到架构设计、编译器、OS/runtime、cost model、resource management和benchmark本身。短期产品不会是“全自动造芯片”，而是设计空间搜索、kernel优化、形式化/测试辅助、RTL simulation加速、文献/设计知识库。

### 4. 可靠性、安全和形式化验证回到中心，因为AI系统已经进入生产和关键行业

IBM keynote强调企业系统8个9的可用性；主会有TEE、FHE、formal verification、testing/fuzzing、silent data corruption、DPU recovery、DRAM disturbance、space radiation、edge NN fault injection等论文。AI基础设施的下一阶段，可靠性不是合规成本，而是SLA和客户准入门槛。

市场变化：Gartner预计2026年AI cybersecurity支出513亿美元，2027年859.97亿美元；AI软件2026年4524.58亿美元、2027年6361.46亿美元。随着AI代理开始调用工具、访问数据、执行动作，安全边界从“模型接口”扩展到OS、TEE、网络、存储、GPU、DPU和agent工具链。

### 5. 边缘AI出货会爆，但利润未必同步爆

ASPLOS 2026有On-Device & Edge AI session，Lifetime-Aware Design of Item-Level Intelligence获Best Paper，AgenticOS和CoDAIM workshop把agentic/multimodal工作负载拉到OS和系统协同层。Gartner预计AI PC 2026年出货1.431亿台，占全球PC市场54.7%；到2026年底，40%软件供应商会优先投资本地PC AI能力，而2024年这一比例只有2%。

但IDC同时下修PC/平板出货：2026年全球PC出货预计下降11.3%，平板下降7.6%；尽管PC市场价值因ASP上涨增至2740亿美元。换句话说，AI PC会成为标配，但“AI PC利润爆发”不等于“AI PC出货爆发”：内存成本、用户付费意愿、软件功能同质化会压制OEM利润。

## 未来一年爆发产品与技术路线：三种口径

### 定义

- 基准口径：AI基础设施继续增长，但受电力、HBM/DRAM/NAND、交付周期和企业ROI约束；技术从论文进入头部云/大厂生产。
- 乐观口径：企业推理、agentic workflow、多模态生成放量快于预期；调度、CXL、PIM、低比特格式、通信库显著降低每token成本。
- 超预期乐观口径：agentic AI带来第二轮推理需求跃迁；主权AI和大企业私有AI共同扩张；内存和互连供给释放，rack-scale系统成为采购基本单位。

### 产品/技术路线总表

| 方向 | ASPLOS 2026证据 | 2026E当前市场规模 | 未来一年增速：基准/乐观/超预期 | 当前利润率与未来走向 | 成熟与量产路线 |
|---|---:|---:|---:|---|---|
| AI基础设施与加速器 | LLM serving/training、GPU systems、MSCCL++、SuperOffload、rack-scale相关论文 | IDC AI infra 4870亿美元；Gartner AI infra 1.366万亿美元；AI半导体约3960亿美元 | +30-35% / +45-55% / +65-80% | 领先GPU厂商FY26 GAAP毛利71.1%、Q4毛利75.0%；行业毛利55-75%，2027或因竞争小幅压缩但规模利润上升 | 2026 Blackwell/MI400/custom ASIC/rack-scale放量；2027推理优化采购成为主线 |
| LLM推理服务软件/控制平面 | vLLM/SGLang/Ray keynote；prefill-decode、KV cache、spec decoding、MoE serving密集 | Gartner AI software 4525亿美元；AI DS/ML platform 311亿美元；推理控制平面可看作其中10-30亿美元级新软件池 | +35% / +60% / +100% | 软件毛利70-85%；但被云厂/模型厂bundling压制，独立厂商经营利润10-30% | 2026云内置+开源主导；2027形成“token operating system”：调度、cache、路由、计费、观测一体化 |
| HBM/DRAM/NAND与先进内存 | CXL、DRAM、PIM、tiered memory、PF-LLM、M2XFP | Gartner memory 6333亿美元；IDC DRAM 4186亿美元、NAND 1741亿美元；HBM单独估计约500-900亿美元区间 | +18-25% / +30-40% / +50%+ | SK hynix 2025经营利润率49%、Q4 58%；HBM/服务器DRAM利润率高位，2027仍偏强，晚2027后看供给 | 2026 HBM3E主流、HBM4在2H26加速；2027 HBM4/12-high/16-high、LPDDR server、CXL内存模块共同放量 |
| CXL/分解式内存/内存池 | 1D CXL独立session，vCXLGen Best Paper，HCDS/Virtuoso workshop | 2026仍小：约20-30亿美元量级；Yole系早期预测2028 CXL总市场超过150亿美元，其中DRAM behind CXL超过120亿美元 | +60% / +100% / +180% | 控制器/IP毛利高但量小；模块利润受DRAM成本挤压，系统级毛利20-45%；2027随switch/fabric成熟改善 | 2026 direct-attached CXL Type-3和云内试点；2027 CXL pod/pooling、KV cache tiering；2028 fabric-attached memory进入规模采购 |
| AI for chip/system design | Architecture 2.0、ArchAgent、AccelOpt、EggMind、LOOPRAG、E-graph Best Paper | EDA总市场约百亿美元级；AI-native architecture/tooling当前约数亿美元到低十亿美元 | +40% / +80% / +150% | 软件毛利75-90%；早期研发/销售投入高，经营利润多为负到20%；被EDA巨头收编概率高 | 2026用于kernel/RTL/验证/探索；2027进入企业设计流程辅助，不会替代sign-off |
| On-device/Edge AI/AI PC | 5B On-Device & Edge AI、item-level intelligence Best Paper、AgenticOS | Gartner AI PC 1.431亿台、占PC 54.7%；IDC PC市场价值2740亿美元 | 出货+80%+，价值+5-15% / +20% / +35% | PC OEM经营利润通常低个位数到低双位数；NPU/SoC毛利高于OEM；内存成本使2026-27利润承压 | 2026 NPU成中高端标配；2027本地SLM、隐私推理、离线agent成熟，但消费者付费仍慢 |
| Confidential Computing/TEE/FHE | TEE session、FHE session、Cheddar/Maverick/ReliaFHE、FHE tutorials | Confidential computing按Grand View 2023 54.63亿美元、2030 1538亿美元推算2026约220-240亿美元；FHE单独仅1.5-3亿美元级 | Confidential +50-70% / +80% / +100%；FHE +10-35% | TEE云服务毛利较高；FHE软件/硬件多处研发期，整体利润低或为负 | 2026 TEE/GPU confidential更快商业化；FHE先在金融、医疗、链上隐私和GPU库落地，通用FHE ASIC仍需2-4年 |
| Quantum/hybrid quantum computing | 1C、4C、9B三组量子session，AI for Quantum/Q-VTK/tutorial | McKinsey称2025量子计算公司收入超过10亿美元，2028最高44亿美元；2026估计15-20亿美元 | +35% / +60% / +100% | 多数硬件商经营利润为负；云访问/软件工具毛利较高但规模小 | 2026仍是cloud access+hybrid workflow；2027-28收入来自金融/化学/优化试点扩展，不是通用量子计算量产 |
| 3D Gaussian Splatting/Neural Rendering/AR-VR视觉系统 | 3C session、VisArch workshop | XR/视觉计算相关硬件+软件约数百亿美元，但3DGS工具链本身仍小 | +30% / +60% / +120% | 工具软件毛利高；硬件利润取决于终端；2027前主要在内容生产、仿真、机器人数据 | 2026进入实时渲染/AR效率优化；2027与端侧AI、机器人仿真、数字孪生结合 |

## 三口径市场规模、增速、利润率预测

### 1. AI基础设施/AI加速器

当前规模：IDC预计2026年AI基础设施支出4870亿美元，同比约+53%；Gartner广义AI基础设施为1.366万亿美元。Gartner半导体口径下，2026年AI semiconductors约占总半导体1.3202万亿美元的30%，即约3960亿美元。Deloitte更激进，认为2026年genAI chips接近5000亿美元。

2027预测：

- 基准：AI infra 6500-6700亿美元，增速+33%-38%；AI semis 5000-5300亿美元。利润率：领先GPU/ASIC毛利维持65%-75%，系统集成商毛利10%-25%，经营利润继续向芯片、HBM、网络和云平台集中。
- 乐观：AI infra 7000-7300亿美元，增速+45%-50%；企业推理和主权AI带来增量。利润率：GPU毛利略降但仍高，网络/HBM利润上行。
- 超预期乐观：AI infra 7800-8500亿美元，增速+60%-75%；agentic/multimodal推理使GPU利用率和采购同步上升。利润率：整机毛利改善，核心芯片/内存仍是最大利润池。

成熟路线：2026是rack-scale AI server从训练扩散到推理的起点；2027采购单位从“GPU卡”转向“rack/cluster+network+memory+serving stack”。

### 2. HBM、DRAM、NAND与内存系统

当前规模：Gartner预计2026年内存收入6333亿美元，2027年7481亿美元；IDC预计2026年DRAM 4186亿美元，NAND 1741亿美元。TrendForce预计2026年HBM出货量突破30Billion Gb，HBM4在2026年下半年逐步超过HBM3E成为主流方向。市场上对HBM 2026收入的估计差异较大，保守可按500-900亿美元区间处理。

2027预测：

- 基准：总内存收入7400-7600亿美元，接近Gartner 7481亿美元；DRAM继续高位但增速从2026的三位数降至20%-35%。利润率：HBM/服务器DRAM维持高毛利，传统消费内存利润修复。
- 乐观：总内存收入8000-8500亿美元；HBM4顺利放量、AI服务器DDR5/LPDDR server需求持续。利润率：HBM龙头经营利润率可维持45%-60%。
- 超预期乐观：总内存收入9000亿美元以上；agentic AI造成KV cache/长上下文/多模态存储需求二次上修。利润率：短期非常强，但2028后存在供给扩张和客户议价反噬。

成熟路线：2026 HBM3E为量产主体、HBM4开始贡献；2027 HBM4/更高堆叠、CXL扩展内存、LPDDR server、近存计算共同构成AI memory hierarchy。

### 3. CXL与分解式内存

当前规模：CXL仍处早期商业化。按公开市场估计，2026年CXL Type-3/内存扩展相关市场约20-30亿美元；Yole系早期预测2028年CXL总市场超过150亿美元，其中DRAM behind CXL超过120亿美元。ASPLOS 2026的1D session和vCXLGen Best Paper说明学术界已经从“是否可行”转向“如何综合、验证、编程、分配和池化”。

2027预测：

- 基准：40-50亿美元，+60%-80%。利润率：控制器/IP毛利较高，模块受DRAM价格影响，系统毛利约20%-40%。
- 乐观：60-75亿美元，+100%-150%。前提是云厂把CXL用于KV cache tiering、数据库内存池和VM/container内存弹性。
- 超预期乐观：90-110亿美元，+200%上下。前提是CXL switch/fabric稳定、软件栈成熟、内存价格继续高企迫使客户采用池化。

成熟路线：2026 direct attach和单机扩容；2027 pod级池化、CXL-aware allocator、model checking和编程模型开始进入生产；2028 fabric-attached memory才可能真正规模化。

### 4. 推理服务软件、AI平台、LLMOps

当前规模：Gartner预计2026年AI software 4525亿美元，2027年6361亿美元；AI Models 263.8亿美元，AI DS/ML Platforms 311.2亿美元，AI Application Development Platforms 84.2亿美元。纯LLM serving控制平面不是单独大类，但在云、模型API、私有部署、GPU云中形成10-30亿美元级软件/服务利润池。

2027预测：

- 基准：AI software 6360亿美元，Gartner口径约+40.6%；推理控制平面+35%-50%。利润率：SaaS毛利70%-85%，但AI token成本使经营利润承压。
- 乐观：AI software 6800-7200亿美元；推理控制平面+60%-80%。利润率：能直接降低GPU成本的软件会获得更高定价权。
- 超预期乐观：AI software 7800亿美元以上；推理控制平面翻倍。利润率：云平台和垂直软件先受益，独立中间件面临被云厂吸收。

成熟路线：2026开源引擎+云平台深度融合；2027形成“推理OS”：prefill/decode分离、KV cache tiering、request routing、observability、billing、safety policy统一管理。

### 5. AI PC/端侧AI

当前规模：Gartner预计2026年AI PC出货1.431亿台，占全球PC的54.7%；IDC预计2026年全球PC市场价值2740亿美元，但出货下降11.3%。这说明AI PC是结构渗透，不是总量繁荣。

2027预测：

- 基准：AI PC占比65%-70%，出货增速继续高于PC大盘；但PC总量恢复有限。OEM经营利润率维持3%-10%，SoC/NPU毛利更强。
- 乐观：本地SLM、隐私AI、企业端侧安全应用提升换机意愿，AI PC价值量+15%-25%。
- 超预期乐观：端侧agent成为Windows/macOS/企业安全标配，AI PC价值量+30%+，但仍受内存成本制约。

成熟路线：2026 NPU成为中高端标配，2027软件生态决定价值。端侧AI的胜负点不是TOPS，而是本地模型、权限系统、企业数据隔离和电池/散热体验。

### 6. Confidential computing、TEE、FHE

当前规模：Grand View Research给出confidential computing 2023年54.63亿美元、2030年1538.43亿美元、CAGR 61.1%；按该CAGR推算2026年约230亿美元。FHE单独市场仍很小，公开预测从2026年1.5亿到3.3亿美元不等，差异巨大，说明商业定义尚未稳定。

2027预测：

- 基准：confidential computing +50%-60%；FHE +10%-25%。利润率：TEE云服务较好，FHE硬件/软件多数仍在研发投入期。
- 乐观：confidential computing +75%；FHE +35%-50%，受金融、医疗、政府、链上隐私驱动。
- 超预期乐观：如果GPU FHE库和专用加速器把性能成本下降一个数量级，FHE市场可+100%，但基数仍小。

成熟路线：TEE/confidential GPU在2026-27商业化更快；FHE的ASPLOS论文更多是算法-硬件共设计、GPU库、加速器可靠性，距离通用量产还有2-4年。

### 7. 量子计算

当前规模：McKinsey称2025年量子计算公司全球收入超过10亿美元，2028年可能达到44亿美元；2025年量子技术创业投资126亿美元，是2024年的6.3倍。ASPLOS 2026有量子编译、量子纠错、hybrid quantum-classical、quantum visualization、AI for quantum等内容。

2027预测：

- 基准：量子计算收入20-25亿美元，+35%-50%。利润率：硬件公司整体仍亏损，软件/云访问毛利较高但规模小。
- 乐观：30亿美元上下，+60%-80%，来自金融、化学、物流优化的hybrid workflow。
- 超预期乐观：35-40亿美元，+100%左右，但需要商业用例从pilot变为repeatable product。

成熟路线：2026-27是“商业化准备期”，不是通用容错量子量产期。最现实产品是cloud access、编译器、纠错工具、hybrid optimization workflow。

## 与市场共识相违背的重要洞见

### 洞见1：AI基础设施的核心瓶颈正在从GPU转向memory hierarchy

市场喜欢把AI capex简化为GPU采购，但ASPLOS 2026把CXL、PIM、tiered memory、DRAM security、KV cache、prefetching、low-bit format放到核心位置。2026年真正的稀缺不是单一FLOPS，而是HBM容量、DRAM/NAND供给、电力、网络、调度器和可用性共同构成的系统吞吐。

### 洞见2：CXL不是HBM替代品，但可能是AI推理利润率工具

常见反对意见是CXL带宽/延迟不如HBM，因此“不适合LLM”。ASPLOS 2026的信号更细：CXL适合容量弹性、KV cache分层、冷数据、内存池、VM/container恢复、异构共享内存，而不是替代热路径HBM。若CXL让GPU有效利用率提升5%-15%，它的经济价值就可能远大于单模块收入。

### 洞见3：AI PC会普及，但AI PC不一定赚钱

Gartner的AI PC渗透率很强：2026年1.431亿台、占54.7%。但IDC同时预测PC出货下降11.3%，只是ASP推高使市场价值到2740亿美元。端侧AI可能是“标配化”而非“溢价化”：消费者未必为AI功能单独付费，内存涨价反而吃掉OEM利润。

### 洞见4：FHE和量子被高估的是短期收入，被低估的是系统研究价值

ASPLOS 2026给FHE/量子很多位置，但它们短期市场规模远小于AI infra/HBM/CXL。真正值得重视的是它们推动编译器、GPU库、纠错、可靠性、加速器设计，这些工具链能力会外溢到AI安全、隐私计算和高可靠计算。

### 洞见5：AI for chip design不会先替代工程师，而会先替代“搜索、调参、文献和评测摩擦”

Architecture 2.0的QuArch竞赛和ArchScholar试验说明，领域正在先建立“如何评估AI系统设计能力”。这与市场上“AI马上自动造芯片”的叙事不同。2026-2027最真实的商业化是kernel优化、设计空间探索、验证辅助、文献检索、自动benchmark生成。

### 洞见6：中国和亚洲机构在系统AI论文中存在感很强，市场叙事仍过度美国hyperscaler中心化

官方program中上海交大、清华、北大、阿里、华为、字节、StepFun、港科大、浙江大学、南京大学等机构频繁出现，尤其在LLM serving、training、CXL、PIM、MoE、speculative decoding、low-bit格式等方向。考虑到出口管制和国产AI硬件路线，系统软件和内存/调度优化可能成为中国AI基础设施的重要杠杆。

## 投资和产业跟踪指标

未来12个月建议跟踪以下高频指标：

- AI infra capex：IDC AI infrastructure quarterly tracker、四大/五大hyperscaler capex、主权AI订单。
- GPU有效利用率：prefill/decode分离、KV cache命中率、speculative decoding acceptance rate、MoE expert load balance、token/sec/$。
- HBM供给：HBM3E/HBM4良率、12-high/16-high量产、SK hynix/Samsung/Micron长单、CoWoS/先进封装产能。
- 内存价格：DRAM/NAND合约价、server DDR5 RDIMM、enterprise SSD、AI server BOM中memory占比。
- CXL落地：CXL Type-3模块出货、CXL switch、云实例、Linux kernel支持、CXL-aware allocator、内存池TCO。
- 可靠性：GPU/CPU silent data corruption、DRAM disturbance攻击、TEE性能损耗、DPU恢复、AIOps incident rate。
- AI软件付费：推理平台是否按“节省GPU成本”定价，而不是按传统seat或API markup定价。
- Edge AI：AI PC真实激活率、本地SLM使用时长、企业端侧安全/隐私部署，而不仅是NPU出货。

## 资料来源

- ASPLOS 2026 official program: https://www.asplos-conference.org/asplos2026/program/
- ASPLOS 2026 awards: https://www.asplos-conference.org/asplos2026/awards/
- ASPLOS 2026 workshops and tutorials: https://www.asplos-conference.org/asplos2026/workshops-and-tutorials.html
- ASPLOS 2026 presentation guidelines: https://www.asplos-conference.org/asplos2026/presentation-guidelines/index.html
- Architecture 2.0 workshop: https://harvard-edge.github.io/asplos-26-arch-2-workshop/
- AgenticOS 2026 workshop: https://os-for-agent.github.io/
- CoDAIM 2026 workshop: https://codaim-asplos.github.io/
- Virtuoso workshop: https://cmu-safari.github.io/Virtuoso/workshop/asplos2026.html
- Columbia CS ASPLOS 2026 paper summary: https://www.cs.columbia.edu/2026/4-papers-from-cs-researchers-at-asplos-2026/
- Gartner semiconductor revenue forecast, Apr 2026: https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026
- Gartner worldwide AI spending forecast, Jan 2026: https://www.gartner.com/en/newsroom/press-releases/2026-1-15-gartner-says-worldwide-ai-spending-will-total-2-point-5-trillion-dollars-in-2026
- IDC AI infrastructure spending, Apr 2026: https://www.idc.com/resource-center/blog/ai-infrastructure-spending-caps-historic-year-at-90-billion-in-q4-2025-2029-spending-to-eclipse-1-trillion/
- IDC semiconductor market forecast, Apr 2026: https://www.idc.com/resource-center/blog/semiconductor-market-to-surge-past-the-trillion-dollar-threshold-ai-infrastructure-drives-market-growth/
- Gartner AI PC forecast, Aug 2025: https://www.gartner.com/en/newsroom/press-releases/2025-08-28-gartner-says-artificial-intelligence-pcs-will-represent-31-percent-of-worldwide-pc-market-by-the-end-of-2025
- IDC personal computing devices market insight, 2026: https://www.idc.com/promo/pcdforecast/
- NVIDIA FY2026 financial results: https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026
- S&P Global/Visible Alpha AMD data-center AI chip forecast: https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/03/amd-s-next-generation-ai-chips-set-to-power-2026-data-center-growth
- TrendForce on SK hynix 2025 results/HBM: https://www.trendforce.com/news/2026/01/28/news-sk-hynix-smashes-records-in-2025-beats-samsung-with-krw-47-2t-operating-profit/
- TrendForce HBM4 manufacturing/2026 HBM shipment trend: https://www.trendforce.com/presscenter/news/20250522-12589.html
- McKinsey Quantum Technology Monitor 2026: https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/mckinsey-quantum-technology-monitor-2026-a-commercial-tipping-point
- Grand View Research confidential computing market outlook: https://www.grandviewresearch.com/horizon/outlook/confidential-computing-market-size/global
- StorageNewsletter/Yole CXL market reference: https://www.storagenewsletter.com/2023/10/11/cxl-technology-unlocks-memory-performance/
