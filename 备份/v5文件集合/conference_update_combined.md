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
# Chiplet Summit 2026 高密度更新：Chiplet 从“先进封装技术”转向“AI 系统级供应链”

> 调研日期：2026-05-08。  
> 方法说明：未参考项目内文件和信息；仅使用公开网络资料、Chiplet Summit 官方动态议程/演讲 PDF/参会者 XML、厂商公开材料、行业研究机构公开摘要，并在报告中标明关键来源。  
> 预测口径：文中的“未来一年”按 2026 年当前市场规模到 2027 年市场规模理解；利润率默认指毛利率，若为软件/IP 则补充经营利润率判断。预测为基于公开资料的归一化推演，不是会议方或单一机构的正式预测。

## 一页结论

Chiplet Summit 2026 的核心信号不是“chiplet 会不会起来”，而是“怎么把 chiplet 变成可采购、可验证、可管理、可量产的系统级供应链”。会议从 2 月 17-19 日在 Santa Clara 召开，官方动态参会者 XML 统计到 368 条演讲/主持/嘉宾记录、70 个唯一 session、105 个组织；Siemens 44 条、Synopsys 38 条、Cadence 25 条、Intel 22 条，是最密集的工具链/标准/验证/封装参与方。

本届会议的增量不是单点 PHY 或先进封装，而是六条线同时收敛：HBM4/Custom HBM、64 GT/s UCIe 3.0、AI XPU 多 chiplet、先进封装产能与良率、photonic interposer/CPO、以及安全/测试/数字孪生/SLM。真正的转折在于：开放 chiplet 经济不再只靠“标准接口”，还要靠 RoT、安全域、boot firmware、known-good-die、冗余 lane、热/电/机械协同和供应链商业规则。

数字上，HBM 是最确定的爆发点：Yole 在 Chiplet Summit 2026 的 HBM Markets 材料中给出 HBM 收入从 2025 年约 350 亿美元到 2026 年约 600 亿美元，2027 年约 800 亿美元，2031 年约 1700 亿美元；2026 年 YoY 约 +70%。先进封装总市场 2026 年约 575 亿美元，增速不如 HBM，但高端 CoWoS/EMIB/SoIC/2.5D/3D 是 AI 系统的真瓶颈，TSMC CoWoS 月产能被报道将在 2026 年底达到 11.5 万至 14 万片，2027 年约 17 万片。Chiplet 产品市场定义差异极大，窄口径 2026 年约 193 亿美元，广口径把 HBM/AI GPU/CPU 多芯粒产品收入都算进去会到数百亿美元以上。

投资和产业判断上，2026-2027 最强爆发不在“通用 chiplet marketplace”，而在“被系统瓶颈强制购买”的环节：HBM/HBM4E、Custom HBM base die、先进封装产能、64G UCIe/D2D IP、3DIC EDA/验证、SLM/DFT/test、CPO/photonic interposer 的早期设计卡位。

## 会议一手信号

### 官方议程和参与结构

Chiplet Summit 2026 官方站点显示会议时间为 2026 年 2 月 17-19 日，地点为 Santa Clara Convention Center。官方 program-at-a-glance 的动态 XML/iframe 数据显示：

| 指标 | 统计 |
|---|---:|
| 演讲/主持/嘉宾记录 | 368 |
| 唯一 session | 70 |
| 参与组织 | 105 |
| Tuesday 记录 | 122 |
| Wednesday 记录 | 140 |
| Thursday 记录 | 106 |
| Top 组织 | Siemens 44、Synopsys 38、Cadence 25、Intel 22、Arm/Marvell/Alphawave 各 9、Yole/Samsung/Daedaelus 各 7 |

议程结构也很清楚：10 个 pre-con tutorial、8 个 keynote、4 个 special presentation，以及大量 D2D/HBM/Packaging/Test/Security/Automotive/Optical/Design session。会议密度说明 chiplet 生态已经从“技术展示”进入“产业工作分解”：谁做标准、谁做 IP、谁做封装、谁做验证、谁做安全、谁做量产。

### Keynotes 的方向变化

Keynote 主题本身就是一张路线图：

- Synopsys：AI-driven multi-die design，强调 AI 自动化多 die 设计。
- Alphawave/Qualcomm：connectivity 是 system-level design 的基础。
- Siemens：3D IC for AI with AI，强调 3D IC 的 multiphysics、signoff、digital twin 和 AI-driven flow。
- UCIe Consortium：open chiplet ecosystem at package level。
- Cadence：Chiplets for Everyone，强调 off-the-shelf、plug-and-play chiplets 和 Physical AI。
- Arm：open chiplet ecosystem for converged AI datacenter。
- OCP：open ecosystems for next wave of AI inference。
- Marvell：custom memory/connectivity/power/optics chiplets for XPUs，并提出 power is the new currency of datacenter。

这意味着市场重心从“chiplet 作为封装结构”转为“chiplet 作为 AI 数据中心和边缘 AI 的供应链组织方式”。

### Best of Show 暗示产业评审标准

官方 Best of Show 三个获奖项也很有信号：

- Packaging Design：Siemens EDA “Innovator3D IC”。
- Packaging Hardware：Sarcina Technology “Advanced Packaging”。
- Connectivity & Interoperability：UCIe Consortium “UCIe 3.0 Specification”。

评审维度包括多厂商互操作、compliance/plugfest、lane repair、flow control、QoS、telemetry、设计套件、合规套件和量产路径。这说明会议认可的“好技术”不是单项性能，而是生态可落地程度。

## 重点发展方向和变化

### 1. HBM 从“配套内存”变成 AI XPU 架构中心

Yole 的 HBM Markets 会议材料给出非常直接的数字：HBM 市场 2025 年约 350 亿美元、2026 年约 600 亿美元、2027 年约 800 亿美元、2031 年约 1700 亿美元；2025 年 YoY +102%，2026 年 YoY +70%，2025-2031 年 CAGR 约 30%。Yole 同时判断 HBM 到 2031 年可能超过 DRAM 收入 40%。

Marvell 的 Custom HBM 材料把问题讲得更工程化：标准 HBM 对 XPU die 的可复用性、方向、tiling、3D SOIC footprint 都造成约束；HBM4E 每 2048-bit stack 带宽可超过 3.5 TB/s，而 LPDDR5X 只有约 68-85 GB/s，CXL 3.0 via PCIe 6.0 x16 约 128 GB/s。Marvell 还给出 PHY/base die 功耗量级：10G 下 PHY 约 8W、base die 约 25W；13.8G 下 PHY 约 11.2W、base die 约 35W。

关键变化：过去市场把 HBM 看成内存 ASP 暴涨；会议视角则是 Custom HBM base die、near-memory function、D2D optimized PHY 会改变 XPU 架构和供应链议价。

### 2. UCIe 3.0 的重点不是“更快”，而是“可管理、可信、可量产”

UCIe 3.0 已把数据率提升到 48/64 GT/s。Chiplet Summit 的 UCIe 3.0/RoT 材料强调 Management Director：它发现 chiplets 和 management elements，同时作为 manageability Root of Trust。材料明确列出多厂商 SiP 的威胁：不可信 chiplet 访问敏感数据、恶意 chiplet 破坏系统完整性、供应链攻击、side-channel、DoS 等。

Alphawave/Qualcomm 的 64G UCIe 材料显示其 UCIe D2D building blocks 已覆盖 7nm、6nm、5nm、4nm、3nm、2nm；并给出 package 类型差异：standard package 约 110-130 um bump pitch、25mm+ reach；silicon interposer/RDL interposer 约 25-55 um、1-5mm；silicon bridge 约 25-45 um、1-5mm。

关键变化：UCIe 从“PHY/协议标准”升级为“多供应商 chiplet 市场的管理和安全底座”。没有 RoT、访问控制、DFT、SLM、compliance，open chiplet 经济就不会发生。

### 3. “1000-chiplet challenge” 把问题从芯片设计推到系统编排

Pre-Con F 主题为 Meeting the 1000-Chiplet Challenge，议程包括 scalable security、pathfinding/prototyping/signoff、boot firmware、hardware/software verification。官方 session 摘要指出，千芯粒系统需要 ROM startup 和 orchestration software 来分配 chiplet ID、类型、安全状态、位置、尺寸、功耗和热状态等。

关键变化：此前 chiplet 叙事多是“把大 die 拆小、提升良率”；2026 年讨论已经进入“千级实体的启动、命名、认证、调度、监控、隔离和验证”。这更接近数据中心系统工程，不再只是 IC 后端工程。

### 4. 先进封装成为 AI 部署的 gating factor

Intel 的 Chiplet Packaging to Scale AI 材料给出几条硬事实：AI scaling 需要更多 compute 和 memory，也就需要把更多 Si 放到 package 上；EMIB-T 支持 >10x reticle complex，pitch scaling capability below 45 um，且“no limit to number of top die or EMIB on package”。同一材料指出，未来更大的 package/die complex 可能需要放弃传统 SMT，转向 mechanical clamping；热管理可能需要 immersion cooling；UCIe 3.0 每 32 条 data lane 有 2 条 redundant lane。

TSMC 方面，TrendForce 2026 年 4 月报道援引 TechNews 与机构投资者数据，TSMC CoWoS 月产能预计到 2026 年底达到约 11.5 万至 14 万片，2027 年约 17 万片；CoPoS panel-level packaging 有望 2028-2029 年开始量产。

关键变化：先进封装的瓶颈从“有没有 CoWoS”扩展到 warpage、power delivery、thermal、lane repair、yield redundancy、mechanical attach 和面板级生产效率。

### 5. 光互连从“未来方向”进入 package-level 架构候选

Lightmatter 的 Photonic Interposer 材料给出很激进的系统数字：其 reference design example M1000 可达 up to 114 Tbps Tx+Rx bandwidth、1024 SerDes、4000 mm² silicon die complex、256 fibers、34 chiplets。材料还指出，102T switch ASIC 若用铜连接会产生 2040 个 224G connections；AI supercomputer scale-up domain 从 2022 年 8 GPUs 到 2024 年 72 GPUs，再到 2025 年 576 GPUs。

关键变化：CPO/photonic interposer 目前收入很小，但问题正在从“交换机 optics”进入“chiplet 下方/旁边的可编程 optical fabric”。一旦 224G/448G electrical reach 继续缩短，光互连会从可选优化变成 rack-scale AI 的必要条件。

### 6. Automotive/Physical AI 是强主题，但量产节奏不会像数据中心

会议有 State of the Art in Automotive Chiplets、What Developers Must Know about Automotive Chiplets、Safety-Critical Physical AI Applications Using RISC-V 等内容。Cadence keynote 也把 Physical AI 作为 chiplet edge 需求。汽车半导体市场本身很大，S&P Global Mobility 预测从 2025 年约 900 亿美元到 2031 年约 1390 亿美元，CAGR 约 7.5%。

关键变化：汽车 chiplet 不是 2026-2027 的最大收入爆点，因为功能安全、车规验证、生命周期、供应链责任划分都会拉长周期；但它会推动 eFPGA chiplet、RISC-V safety island、ASIL 级监控、长期可维护 IP 的需求。

## 哪些产品和技术会爆发

### HBM4/HBM4E 和 Custom HBM：爆发力度最强

基准口径：2026 年 HBM 收入约 600 亿美元，2027 年约 800 亿美元，增速约 +33%。HBM4 在 2026 年进入主流 AI accelerator roadmap，HBM4E 在 2027-2028 年接棒，custom HBM base die 从顶级 hyperscaler/XPU 厂商开始。

乐观口径：HBM 供应继续紧缺，HBM4/4E ASP 维持高位，2027 年收入可达 950 亿美元左右，增速约 +58%。Custom HBM 的价值不止内存堆栈，还包括 base die、PHY、near-memory、memory expansion 和封装协同。

超预期乐观口径：agentic AI/physical AI 推动推理上下文和 KV cache 继续膨胀，HBM 2027 年可冲击 1100 亿美元，增速约 +80%。这种情形下，HBM 供应商和能拿到 Custom HBM 设计窗口的 ASIC/平台商利润率会维持极高水平。

### 64G UCIe/D2D IP：爆发不在数量，而在设计锁定

基准口径：2026 年是 UCIe 3.0 IP、VIP、compliance、simulation、interposer/package co-design 的设计导入年，2027 年进入更多 hyperscaler ASIC 和 AI accelerator tape-out。收入规模不如 HBM，但粘性和毛利率高。

乐观口径：64G UCIe 在 2027 年变成高端 AI package 的事实标准之一，尤其是 HBM streaming、DDR/CXL retimer、multi-IO die、optical chiplet 场景。Synopsys/Cadence/Siemens/Alphawave/Arteris/Keysight 等受益。

超预期乐观口径：UCIe 3.0 的 manageability/RoT/compliance 体系提前成熟，2027 年出现实质性多厂商 plug-and-play 设计流。真正受益的是“IP + VIP + EDA + test + reference design”的组合，而不是单独卖 PHY。

### 先进封装和 3DIC 设计平台：产能、良率、warpage 是价值来源

基准口径：CoWoS/EMIB/SoIC/2.5D/3D 保持高需求，先进封装 2027 年收入约 630 亿美元。封装环节收入增速没有 HBM 高，但供需紧张使高端产能具有强定价能力。

乐观口径：TSMC CoWoS、Intel EMIB-T、Samsung/OSAT 高端封装加速扩产，2027 年市场约 690 亿美元，AI 高端封装增速显著高于总市场。

超预期乐观口径：CoPoS/玻璃/面板级封装路线提前获得大客户验证，AI ASIC 和 GPU package size 继续放大，2027 年先进封装市场可接近 780 亿美元。

### Photonic interposer/CPO：短期小市场，长期高弹性

基准口径：CPO 市场 2026 年约 1.65 亿美元，2027 年约 2.2 亿美元。2026-2027 仍以 proof-of-concept、早期 switch、co-packaged optical engine、in-package optical fabric 评估为主。

乐观口径：NVIDIA/Meta/Google 等 AI scale-up 网络拉动 800G/1.6T/3.2T optics 和 CPO，2027 年 CPO 市场约 2.8 亿美元。

超预期乐观口径：224G electrical bottleneck 比预期更早触顶，photonic interposer 在 rack-scale AI 变成架构必选，2027 年 CPO/光 chiplet 可超过 4 亿美元，2028-2030 年加速曲线会陡峭很多。

### eFPGA chiplet：不是大众爆品，但适合高毛利利基

QuickLogic 的 eFPGA chiplet on Intel 18A 材料强调 performance、adaptability、longevity，支持 UCIe adapter/PHY，DSP 场景可到 60 GSps、30 GHz BW、约 70 dBc SFDR、约 1W/channel。

基准口径：2027 年主要在国防、通信、工业、航天、Physical AI sensor fusion 等小批量高价值领域放量。

乐观口径：UCIe chiplet reference flow 成熟，eFPGA chiplet 成为“长期可更新 ASIC”的标准选项。

超预期乐观口径：车规/工业生命周期压力把 eFPGA chiplet 推成可复用平台，供应商从 IP 授权转向 chiplet 产品和模块销售。

## 市场规模、增速和利润率预测

| 产品/技术 | 2026 当前市场规模 | 当前利润率判断 | 2027 基准 | 2027 乐观 | 2027 超预期乐观 |
|---|---:|---|---:|---:|---:|
| HBM/HBM4/HBM4E | 约 600 亿美元 | HBM 毛利率估计 55-65%；头部供应商显著高于通用 DRAM | 800 亿美元，+33%，毛利 55-60% | 950 亿美元，+58%，毛利 60-65% | 1100 亿美元，+83%，毛利 65-70% |
| 先进封装总市场 | 约 575 亿美元 | 高端 CoWoS/2.5D/3D 毛利 30-45%，传统 OSAT 混合后 20-35% | 630 亿美元，+10%，利润率小幅上行 | 690 亿美元，+20%，高端供需继续偏紧 | 780 亿美元，+36%，AI 高端封装强定价 |
| Chiplet 产品市场，窄口径 | 约 193 亿美元 | AI chiplet 产品毛利 45-70%，取决于是否含 GPU/ASIC/HBM | 280 亿美元，+45% | 330 亿美元，+70% | 400 亿美元，+108% |
| D2D/UCIe/3DIC EDA+IP 子市场 | 估计 15 亿美元 | 软件/IP 毛利 80-95%，经营利润率 25-45% | 19 亿美元，+25% | 22 亿美元，+45% | 26 亿美元，+75% |
| CPO/photonic chiplet | 约 1.65 亿美元 | 产业早期，模块/器件毛利 20-40%，公司 EBIT 多数仍低或为负 | 2.2 亿美元，+35% | 2.8 亿美元，+70% | 4.1 亿美元，+150% |
| Automotive chiplet/Physical AI chiplet | 真正 chiplet 收入估计 2-5 亿美元；汽车半导体约 900 亿美元 | 车规芯片毛利 25-45%；IP/软件更高 | 4-6 亿美元，+30-50% | 7-9 亿美元，+80% | 10-13 亿美元，+150% |
| Test/DFT/SLM/KGD for chiplets | 估计 8-12 亿美元 | ATE/软件/服务混合毛利 45-80% | 10-14 亿美元，+20% | 12-16 亿美元，+35% | 15-20 亿美元，+60% |

### 口径解释

HBM 使用 Yole 在 Chiplet Summit 2026 材料中的公开数字。先进封装使用 Mordor 2026 年 574.6 亿美元口径，并用 Yole 2024 年 460 亿美元、2030 年 794 亿美元作交叉校验。Chiplet 产品市场使用 2026 年 192.7 亿美元的窄口径市场研究，但需要强调，Jim Handy 在会议上也指出 chiplets 不创造新终端市场，而是用更经济的方式服务已有市场，所以广口径和窄口径差异会非常大。D2D/UCIe/3DIC EDA+IP 是我从 EDA+IP 市场和 semiconductor IP 市场中拆出的 chiplet 相关子集估计。

## 关键路线图

### 2026 年：设计导入和产能争夺

- HBM4 初期产品进入 AI accelerator roadmap，HBM3E 仍是收入主力。
- UCIe 3.0 设计/IP/VIP/仿真开始进入实际项目，64G 成为高端讨论焦点。
- CoWoS/EMIB/SoIC 等高端封装继续是 AI 供给约束。
- Digital twin、hardware-in-the-loop、SLM、DFT、RoT 从“nice to have”变成 open chiplet 的必要条件。
- Photonic interposer 以样机和 reference design 证明带宽密度，但收入仍小。

### 2027 年：HBM4E、UCIe 3.0 和 AI ASIC 扩散

- HBM 市场基准可到约 800 亿美元，HBM4E 开始为 2028 年主力做准备。
- UCIe 3.0 的 manageability/security/compliance 是否成熟，将决定开放 chiplet 生态是真突破还是继续停留在同厂商封闭集成。
- CoWoS 产能约 17 万片/月的规划若兑现，AI GPU/ASIC 供给瓶颈将从单一封装产能转向功耗、散热、HBM、基板材料和测试良率。
- Automotive/Physical AI 还不会大规模爆发，但会形成设计 win。

### 2028-2029 年：面板级封装、CPO 和 custom HBM 进入更大规模

- CoPoS/玻璃/面板级路线若量产，可能改变超大 package 成本曲线。
- HBM5、hybrid bonding、20Hi stack 等推动内存和封装协同更深。
- CPO/photonic interposer 若进入 AI scale-up 网络，会从小市场突然变成高弹性细分赛道。

## 可能违背当前市场共识的洞见

### 洞见 1：通用 chiplet marketplace 可能慢于预期

会议声量很大，但真正要跨厂商复用 chiplet，必须解决 RoT、compliance、thermal/power envelope、business model、test responsibility、known-good-die、failure liability。UCIe 3.0 是必要条件，不是充分条件。2026-2027 更容易落地的是同一大客户/同一平台内的可复用 chiplet，而不是像软件包管理器一样的开放市场。

### 洞见 2：HBM 的“利润爆发”可能比 AI accelerator 更纯

AI accelerator 需要承受软件生态、客户集中、迭代风险和供应链成本；HBM 则是所有高端 AI XPU 的共同刚需。Yole 给出的 2026 年 600 亿美元和 2027 年 800 亿美元意味着 HBM 已经不是配套市场，而是 AI 半导体利润池本身。

### 洞见 3：先进封装的下一瓶颈不是产能，而是物理可靠性

Intel 材料提到大 package warpage、mechanical clamping、vertical power delivery、immersion cooling、redundant lanes。这说明即使 CoWoS 产能上来，系统仍会在热、机械、电源完整性和测试处遇到瓶颈。只看“月产能”会低估后段工程复杂度。

### 洞见 4：UCIe 3.0 的 RoT 价值可能高于 64 GT/s

市场容易盯着 64 GT/s，但会议材料中最关键的其实是 Management Director/RoT、access control、security clearance group、prohibited access check。开放 chiplet 经济要解决的是“我能不能信任这个 die”，不是“这个 die 能跑多快”。

### 洞见 5：CPO 的 2026 收入小，不代表技术不重要

CPO 市场 2026 年只有约 1.65 亿美元量级，但 Lightmatter 会议材料已经把问题拉到 114 Tbps、1024 SerDes、256 fibers、34 chiplets 的系统层级。对于 AI rack，CPO/photonic interposer 的重要性会在收入曲线上明显滞后体现。

### 洞见 6：Automotive chiplet 会先是“架构权”而不是“收入权”

汽车半导体约 900 亿美元级别，但 chiplet 化受安全认证、供应链责任和生命周期约束。2026-2027 更重要的是谁定义车规 chiplet 的 safety/security/monitoring interface，而不是谁已经拿到大规模收入。

## 重点受益环节排序

1. HBM/HBM4E/Custom HBM：收入弹性最大、利润率最高、需求确定性最强。
2. 高端先进封装产能和材料：CoWoS/EMIB/SoIC/CoPoS、玻璃、基板、power delivery、thermal。
3. D2D/UCIe IP/VIP/3DIC EDA：市场规模小于硬件，但毛利和粘性极强。
4. Test/DFT/SLM/KGD：chiplet 量产越复杂，测试越从成本项变成架构项。
5. Photonic interposer/CPO：短期小，长期可能出现非线性放量。
6. eFPGA/RISC-V/Physical AI chiplets：利基高毛利，尤其适合车规、工业、国防和边缘 AI。

## 主要来源

- Chiplet Summit 2026 官方 Program at a Glance：<https://chipletsummit.com/2026-program-at-a-glance/>
- Chiplet Summit 2026 官方 Keynotes：<https://chipletsummit.com/2026-keynotes-and-special-presentations-2/>
- Chiplet Summit 2026 官方 speaker XML：<https://realintelligence.com/customers/expos/00D5f000000Kf85/SNS_xmlcreator/a0qVV0000032cp3_showspeakerlist.xml>
- Chiplet Summit 2026 detailed session iframe，2 月 17 日：<https://realintelligence.com/customers/expos/00D5f000000Kf85/index-Details-iframe-anchors.php?eventId=a0qVV0000032cp3&orgId=00D5f000000Kf85&eventdate=2026-02-17&trackCategory=Session>
- Chiplet Summit 2026 detailed session iframe，2 月 18 日：<https://realintelligence.com/customers/expos/00D5f000000Kf85/index-Details-iframe-anchors.php?eventId=a0qVV0000032cp3&orgId=00D5f000000Kf85&eventdate=2026-02-18&trackCategory=Session>
- Chiplet Summit 2026 detailed session iframe，2 月 19 日：<https://realintelligence.com/customers/expos/00D5f000000Kf85/index-Details-iframe-anchors.php?eventId=a0qVV0000032cp3&orgId=00D5f000000Kf85&eventdate=2026-02-19&trackCategory=Session>
- Yole Group, High Bandwidth Memory Markets, Chiplet Summit 2026 PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260217_PreConB_Bertolazzi.PDF>
- Jim Handy, Objective Analysis, The Chiplet Market Today, Chiplet Summit 2026 PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_PLEN_Handy.PDF>
- Marvell, Using Customized HBM Solutions in Data Center Applications PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260217_PreConB_Allman.PDF>
- Rebellions, Rebel100 2 PFLOPS Quad-Chiplet AI SoC with 4 TB/s UCIe PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260217_PreConD_Jin.PDF>
- Siemens/Avery, Scalable Chiplet Integration with UCIe 3.0 and RoT PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_A-101_Li.PDF>
- Alphawave Semi, Designing Reliable 64G UCIe Chiplet Interconnects PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_B-101_Cheruliyil.PDF>
- Intel, Chiplet Packaging to Scale AI PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_E-103_Hosseini.PDF>
- Lightmatter, Photonic Interposer Supports Terabit Chiplet-Based Systems PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260219_B-202_Nowroozi.PDF>
- QuickLogic, Building an eFPGA Chiplet Ecosystem PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260219_E-202_Peterson.PDF>
- Chiplet Summit 2026 Best of Show Awards：<https://chipletsummit.com/2026-best-of-show-awards/>
- UCIe 3.0 公开发布信息：<https://www.design-reuse.com/news/202529142-ucie-consortium-introduces-3-0-specification-with-64-gt-s-performance-and-enhanced-manageability/>
- TrendForce on TSMC CoWoS/CoPoS, 2026-04-16：<https://www.trendforce.com/news/2026/04/16/news-tsmc-says-cowos-offers-industrys-largest-reticle-size-packaging-amid-intel-emib-rivalry-copos-advances/>
- Mordor advanced packaging market 2026-2031：<https://www.mordorintelligence.com/industry-reports/advanced-packaging-market>
- Yole advanced packaging public summary：<https://www.edge-ai-vision.com/2025/09/advanced-packaging-market-set-to-reach-79-4-billion-by-2030/>
- Coherent Market Insights chiplet market 2026-2033：<https://www.coherentmarketinsights.com/industry-reports/chiplet-market>
- Mordor CPO market 2026-2031：<https://www.mordorintelligence.com/industry-reports/co-packaged-optics-market>
- Semiconductor Engineering, EDA and IP Q4 2025：<https://semiengineering.com/eda-and-ip-numbers-up-again-but-numbers-are-more-nuanced/>
- SIA, 2025 global semiconductor sales and 2026 outlook：<https://www.semiconductors.org/global-annual-semiconductor-sales-increase-25-6-to-791-7-billion-in-2025/>
- S&P Global Mobility, automotive semiconductor 2026 trends：<https://www.spglobal.com/automotive-insights/en/blogs/2026/04/automotive-semiconductor-market-trends>
# CXL Consortium Webinar: Vertical Optimization of the CXL Stack 2026 调研更新

> 研究口径：仅使用外部公开资料和公开视频字幕整理，未读取、引用或交叉验证项目目录内已有文件。时间口径为截至 2026-05-08 前后的公开资料。核心一手信息来自 CXL Consortium 2026-04-01 官方 webinar 页面和公开视频；市场数字来自 Gartner、IDC、TrendForce、公司公告、白皮书和公开市场研究页面。公开视频字幕为自动字幕，个别专有名词按上下文校正，例如 KB cache 校正为 KV cache、Pangier/PJ 校正为 Pangaea。

## 0. 高浓度结论

1. 这场会的真正转折不是“CXL 可以扩内存”，而是 CXL 从接口标准进入“纵向优化”阶段：同一条 CXL 链路要同时解决应用层 KV cache、OS/NUMA 分层、CXL 控制器、交换芯片、Kubernetes 编排和数据中心 TCO。
2. Samsung 在会上把 CXL 商业化瓶颈压缩成三个硬问题：延迟、AI 带宽、虚拟化/云原生软件支持。对应技术是 S-CHMU/CHMU、CXL-PNM、Pangaea v2。
3. 会议给出的关键数字非常激进：视频输入 KV cache 约为纯文本的 8 倍；机器人 15 分钟、10 actions/s 需要约 1.2TB KV cache；S-CHMU 应用感知延迟改善 40%、部分测试相对 first-touch 策略最高约 3x 加速；CXL-PNM 把 FAISS IVF Flat 向量检索从 3.5 QPS 拉到 19.7 QPS，超过 5x；Pangaea v2 将有效内存容量提升约 50%，10GB 内存数据库 pod 在 30GB 本地 DRAM 节点上从 3 个提升到 6 个以上，单 pod 慢 10-14%，但系统吞吐最高 5x。
4. 直接 CXL 市场仍小但弹性大：CXL memory expansion 公开估算为 2025 年 13 亿美元、2026 年 16.7 亿美元、2034 年 118 亿美元；CXL component 市场为 2024 年 19 亿美元、2030 年 123 亿美元，CAGR 约 32%。这不是 HBM 级别的大盘，但它是 AI 内存短缺下的“利用率杠杆”。
5. 真正决定 CXL 经济性的上游大盘已经发生剧烈变化：IDC 预测 2026 年 DRAM 收入 4186 亿美元，同比 +177%；NAND 1741 亿美元，同比 +138.5%；Gartner 预测 2026 年 memory revenue 6333 亿美元，较 2025 年 2163 亿美元接近 3 倍，DRAM 年度价格 +125%、NAND +234%。
6. 市场可能低估的一点：DRAM 越贵，CXL pooling/tiering 的 ROI 越强。高价内存并不必然压制 CXL，反而会让云厂商更痛恨 stranded memory 和本地 DRAM 过度配置。

## 1. Webinar 一手信息提炼

### 1.1 会议基本事实

- 会议名称：CXL Consortium Webinar: Vertical Optimization of the CXL Stack。
- 日期和形式：2026-04-01，Zoom Webinar，官方页面提供 YouTube 回放。
- 主讲方：Samsung Memory Division。
- 官方定义的三大障碍：CXL 相比 DIMM 的更高延迟、数据密集 AI 应用的带宽不足、数据中心虚拟化软件中 CXL 支持不够 robust。
- 官方列出的三项关键技术：S-CHMU 解决延迟，CXL-PNM 解决 AI workload 带宽，Pangaea 支持虚拟化环境并降低 stranded memory。

### 1.2 需求侧：AI 把内存问题从“容量”推到“容量+带宽+生命周期”

会议开场将 CXL 放在 agentic AI 和 physical AI 语境下，而不是传统数据库语境下。Samsung 给出的例子是：

- 多模态输入显著放大 KV cache：视频处理需要的 KV cache 约为简单文本的 8 倍。
- 机器人场景：一个机器人运行 15 分钟、10 actions/s，仅 KV cache 就需要约 1.2TB 内存。
- 客户最常见诉求之一不是裸扩容，而是用比 RDMA-based sharing 更高性能、更低 TCO 的方式管理 KV cache。
- 另一个诉求是 memory pooling，用池化技术隔离不同 AI agents 的服务，并最大化内存效率。

### 1.3 S-CHMU/CHMU：延迟问题的关键不在链路，而在 hot page 识别和迁移

会议中的逻辑链：

- CXL memory 相比本地 DRAM 天然高延迟，原因包括 PCIe interconnect、协议开销，以及加入 CXL switch 后的额外跳数。
- 传统 host-based hot page monitoring 依赖 AutoNUMA、DAMON、PTE scanning 或 sampling，问题是 CPU 开销高、只看 access bit 时精度有限、提高采样率又会增加 profiling events。
- CHMU 的思路是把 hot page monitoring 下沉到 CXL device，在内存访问发生处观测访问模式，然后把 hot page information 交给 host。
- CHMU 已从 OCP community 需求进入 CXL Consortium 标准化讨论，CXL 3.x Q&A 也明确提到 CHMU 的目标是支持纯 OS-based memory tiering。

关键实现和数字：

- 128GB 内存对应超过 3000 万个 4KB pages，如果逐页计数，counter 本身就需要数十 MB device-side storage。
- Samsung 因此采用 Count-Min Sketch 这类概率估计方法，在硬件成本和 hot page 判断精度之间折中。
- 原型实现：FPGA 上实现硬件，扩展 vanilla CXL device driver，并部署 daemon，把 hot pages 迁移到 local DRAM。
- 会中摘要数字：应用层感知延迟改善 40%。
- 详细演示数字：相对 baseline first-touch policy，部分 workload 最高约 3x speed-up；原因不仅是延迟降低，也包括 hot pages 迁回 DRAM 后 CXL traffic 减少，缓解链路瓶颈。

投资含义：CHMU 类能力会把 CXL 控制器从“被动内存桥”升级为“带 telemetry 和 tiering intelligence 的内存管理器”。未来 CXL controller 的差异化不只看带宽/延迟，还要看 page temperature 观测、event/threshold notification、OS driver 质量和 fleet telemetry。

### 1.4 CXL-PNM：解决带宽不是只靠更快链路，而是减少跨 CXL 链路的数据移动

会议中给出的 switch bottleneck 例子非常关键：

- 两个 upstream ports，每个 64GB/s。
- 六个 CXL devices，每个 32GB/s。
- 每个 upstream port 接三个 devices，device aggregate bandwidth 是 3 x 32GB/s = 96GB/s，但 upstream port 只能交付 64GB/s。
- 结果是每个 upstream port 有 32GB/s 带宽“过不去”。设备越多，gap 越大。

CXL-PNM 的策略不是先增加 upstream bandwidth，而是把计算搬到 memory device 旁边：

- 传统 CPU-based vector search：大量 stored vectors 要从 CXL memory 经过 CXL link 到 CPU，再计算距离。
- CXL-PNM：fine search 这类 memory-intensive 部分在 CXL-PNM device 内执行，只把 reduced result 返回给 CPU。
- 使用场景：RAG 中的向量检索；实现基于 FAISS，index 类型为 IVF Flat。
- 软件改动：原代码中只加少量 API 调用，把 fine search 重定向到 PNM device；coarse search 留在 CPU。

PoC 硬件和结果：

- CXL 2.0-capable CPU，40 cores。
- 四个 CXL-PNM devices，每个 32GB memory。
- 接口为 PCIe 5.0 x8。
- CPU-only：3.5 queries/s。
- CXL-PNM：19.7 queries/s。
- 吞吐提升：超过 5x。
- 另一个重要收益：CPU utilization 显著降低，CPU 可释放给其他任务。
- 当前成熟度：主讲人明确称仍处于 research stage，后续方向包括 KV cache offload、secure memory、支持 IVF Flat 之外更多 vector search formats。

投资含义：CXL-PNM 是“带宽虚拟化”。它不增加物理链路峰值，却通过本地 reduction 提高有效带宽。若未来 vLLM、FAISS、Milvus、pgvector、vector DB 和 KV-cache runtime 接入标准化 API，CXL-PNM 会从研究原型变成 AI inference 的专用加速层。

### 1.5 Pangaea v2：CXL 商业化的短板可能是 Kubernetes 和 fabric management，而不是内存条

Pangaea v2 在会中被定位为 CXL 2.0 based memory pooling solution，集成到 cloud-native Kubernetes 环境。它解决的是 CXL hardware 已经能做 pooling，但软件生态不能动态分配、控制和回收资源的问题。

架构重点：

- CXL agent：管理底层 CXL fabric infrastructure，基于 Open Fabric Management Framework，并把各家 switch vendor 的 CLI/proprietary fabric manager API 实时转为 DMTF Redfish API。
- DCMFM manager：memory composability layer，实现 OCP Composable Memory System architectural specification。
- 粒度：把 CXL device 切成 memory blocks，单位为 128MB 或 2GB，与 Linux kernel hotplug 管理对齐。
- Kubernetes 集成：通过 CXL Node Resource Interface plugin 拦截 container runtime lifecycle，例如 containerd/CRI-O 的 sandbox create/stop event。
- 用户接口：operator 可以在 pod YAML annotation/resource spec 中声明 memory type = CXL 和容量，应用代码、OS binary、Kubernetes binary 不需要改。

会议中的经济性数字：

- 传统 virtualization/container 平台通常在 instance/pod 创建时静态分配 memory，会议称这造成 major cloud cluster 平均 utilization 约 23%。
- Pangaea v2 的目标是 runtime dynamic capacity adjustment，实时绑定/解绑 CXL memory 到 worker node。
- 10GB memory-consuming in-memory database pod，物理节点只有 30GB local DRAM：传统方式刚好 3 个 pod 就到物理上限；Pangaea 能在本地 DRAM 耗尽后从 CXL pool 实时供给，单服务器稳定运行 6 个以上 pod。
- 单 pod 由于 CXL remote access 约有 10-14% 性能下降。
- 但高密度部署后，单物理服务器总吞吐最高可达单 pod 传统运行的 5x。
- 会中总体摘要称 Pangaea 将 effective memory capacity 提高约 50%。
- 结尾路线：Pangaea v2 对应 CXL 2.0，后续期待 CXL 3.0 based solution。

投资含义：Pangaea 的核心不是“每个 workload 更快”，而是“单机/集群总吞吐和内存利用率更高”。对云厂商和企业客户，Pangaea 类软件栈的 ROI 来自更多 pod/VM consolidation、更低 stranded memory、更少高内存 bare-metal 节点采购。

## 2. 和此前市场/技术叙事相比的重要变化

### 2.1 从“硬件可用”转到“纵向协同”

2024-2025 的 CXL 叙事偏硬件：Type-3 memory expander、controller、retimer、switch、CXL 2.0/3.x 规格、CPU 是否支持。2026 这场会的叙事变成：应用、OS、runtime、Kubernetes、fabric management、CXL controller 必须一起优化，否则硬件可用也无法大规模商用。

这意味着产业链价值会从单点器件扩散到四类公司：

- 内存厂：Samsung、Micron、SK hynix，卖 CMM-D/CMM-H、CXL DRAM 和未来混合内存。
- 控制器/连接芯片：Astera Labs、Marvell、Montage、XConn、Microchip 等，卖 controller、retimer、switch、fabric。
- 系统/OEM/ODM：Supermicro、Dell、HPE、Lenovo、Gigabyte 等，把 CXL 插卡/EDSFF/主板拓扑产品化。
- 软件/云平台：Linux kernel、Red Hat、Kubernetes plugin、Pangaea-like orchestration、cloud VM product。

### 2.2 CXL 2.0 是当下量产主线，CXL 3.x/4.0 是下一阶段形态

CXL 4.0 已发布，官方亮点是从 64GT/s 翻倍到 128GT/s、zero added latency、bundled ports、memory RAS enhancements、继续兼容 3.x/2.0/1.1/1.0。但这场 Samsung webinar 的 Pangaea v2、CXL-PNM demo、当前产品化路径主要仍围绕 CXL 2.0 和 PCIe 5.0。

短期判断：

- 2026 年收入主要来自 CXL 2.0 memory expansion、controller、AIC/EDSFF 模组、少量云预览/准量产。
- 2027 年重点看 CXL 3.x dynamic capacity device、多 host/multi logical device、更成熟 switch fabric。
- CXL 4.0/PCIe 7.0 128GT/s 对系统级产品收入的贡献大概率偏 2028 年以后，但会提前影响 2026-2027 年研发和设计导入。

### 2.3 第一个 hyperscale 云部署信号已经出现

Astera Labs 2025-11-18 公告称，其 Leo CXL Smart Memory Controllers 支持 Microsoft Azure M-series VMs preview，这是公开披露的 industry first CXL-attached memory deployment。关键参数：

- Leo 支持 CXL 2.0。
- 单 controller 最高 2TB memory capacity。
- 可让 cloud provider 把 server memory capacity 提高超过 1.5x。
- 目标 workload 包括 in-memory database、big data analytics、AI inference、LLM KV cache、machine learning、recommendation systems。

这不是大规模 GA，但足以说明 CXL 已经从 lab/demo 走向 cloud VM evaluation。未来一年最重要的催化不是更多 PPT，而是 Azure M-series CXL 从 preview 走向 GA，以及 AWS/GCP/Oracle/Meta 是否公开类似产品。

### 2.4 CXL 不是 HBM 替代品，而是 HBM/DRAM/SSD 之间的新层级

市场容易把 CXL 当作“便宜 HBM 替代品”，这不准确。CXL-attached DRAM 的 latency 和 bandwidth 明显不等于本地 HBM 或 CPU DIMM。Micron 实测白皮书中，RDIMM local idle latency 为 144ns，remote DRAM 239ns，CMM-D/CZ120 local CXL 254ns，remote CXL 353ns；RDIMM all-read 278.4GB/s，两个 CMM-D/CZ120 约 52.4GB/s all-read、混合读写约 60GB/s。

但 CXL 的位置很清晰：比 SSD/NVMe 快得多，比本地 DRAM/HBM 慢，但能扩容量、降 stranded memory、减少 IO paging。对于 KV cache、vector index、IMDB main storage、warm data、Spark RDD 等，CXL 的价值来自“足够快且便宜地留在内存语义中”。

## 3. 哪些产品和技术方向会爆发

### 3.1 爆发优先级排序

#### 第一梯队：CXL Type-3 memory expansion 模组和 CXL memory controllers

当前已经最接近收入兑现。Samsung CMM-D 官方产品页显示 MD220 支持 CXL 2.0、PCIe 5.0、容量最高 256GB、DDR5、EDSFF E3.S 2T；Astera Leo A-Series AIC 支持 PCIe x16 CEM、4 个 DDR5 RDIMM slots、最高 2TB；Micron CZ120 CMM 每个模块最高 256GB，PCIe Gen5 x8，四块可贡献 1TB far memory。

爆发理由：

- AI inference 和 IMDB 直接需要 TB 级内存。
- HBM 供给被 AI accelerator 锁定，CPU/general server DDR5 同样被拉紧。
- CXL 可以让服务器不靠增加 CPU socket 就扩内存。
- Azure M-series preview 提供了 hyperscale validation 信号。

#### 第二梯队：CXL memory pooling/orchestration 软件栈

Pangaea v2、Redfish/OCP composable memory、Kubernetes NRI plugin、Linux hotplug、NUMA tiering、CHMU driver，是从 pilot 到 production 的关键。硬件厂商会倾向开源基础组件，但商业价值体现在云厂商内部 TCO、硬件 attach rate、support/subscription、fleet management 软件。

爆发理由：

- 会议中的 23% utilization、50% effective capacity、6+ pods vs 3 pods、5x total throughput 指向非常强的云经济性。
- 如果 DRAM 价格继续上涨，software-defined memory pooling 的 ROI 会迅速提高。
- 企业客户更容易接受“应用代码不改、Kubernetes YAML 声明 CXL memory”的路线。

#### 第三梯队：CXL-PNM、near-memory vector search 和 KV-cache offload

短期收入小，但技术弹性最大。会议里 3.5 QPS 到 19.7 QPS 的 PoC 说明，只要 workload 是大数据移动、小计算密度，PNM 的有效带宽收益会非常夸张。

爆发条件：

- FAISS、vector DB、RAG runtime 或 vLLM/KV cache manager 有稳定 API。
- CXL-PNM device 支持多租户隔离和 secure memory。
- 开发者改动必须保持在“几行 API”或透明 library 层，而不是重写应用。

#### 第四梯队：CXL switch/fabric/retimer 和 CXL 3.x/4.0 拓扑

Pangaea 的底层依赖 CXL switch 和 fabric manager。CXL 4.0 的 128GT/s、bundled ports、RAS 会在更大规模拓扑中重要。但 2026 的产品收入更可能来自 CXL 2.0/PCIe 5.0 和 CXL 3.x 早期导入，CXL 4.0 大规模量产节奏偏后。

#### 第五梯队：CXL hybrid/persistent memory

Samsung CMM-H PM 把 DRAM 和 NAND 结合为 CXL-based large capacity PMEM，目标是替代 Optane 后留下的 near-memory persistent tier。方向有长期价值，但 2026-2027 量产和软件生态不确定性高。

## 4. 成熟和量产路线预测

### 4.1 基准口径

- 2026H1：CXL 2.0 memory expansion 继续以 evaluation、pilot、selected customer deployment 为主。Azure M-series CXL preview、Samsung/Red Hat RHEL 9.3/KVM/Podman 验证、Micron/Samsung 白皮书案例是主要证据。
- 2026H2：少数 hyperscaler 和高端企业数据库/HPC 场景进入 production-limited deployment。主产品为 CXL memory module、AIC、controller、retimer。Pangaea 类软件仍以参考架构/客户定制为主。
- 2027：CXL memory pooling 从单 host expansion 向 multi-host pool 扩展，CXL 3.x dynamic capacity device、CHMU 支持、Linux/Kubernetes integration 更成熟。CXL-PNM 有望进入 early access，但收入仍小。
- 2028：CXL 4.0/PCIe 7.0 相关 128GT/s、bundled ports、RAS 产品进入更清晰的系统设计窗口。

### 4.2 乐观口径

- 2026H2：Azure CXL VM 从 preview 接近 GA，至少一家 AWS/GCP/Oracle/Meta 公开 CXL memory tier 或 CXL-backed bare metal/VM。
- 2027H1：CXL memory expansion 年化收入突破 30 亿美元；CXL switch/fabric attach 明显提高；Pangaea-like orchestration 被一家 hyperscaler 内部规模部署。
- 2027H2：CHMU-like device telemetry 进入更多 controller silicon，Linux 内核和 vendor daemon 支持形成事实标准。

### 4.3 超预期乐观口径

- 2026H2-2027H1：DRAM/HBM 供应继续极紧，云厂商将 CXL 作为 KV-cache 和 IMDB 内存层的“必选项”而非优化项。
- CXL memory expansion 2027 年化规模接近 40-50 亿美元，显著高于当前市场研究的平滑 CAGR。
- 至少一个主流 vector DB/RAG stack 与 CXL-PNM 形成公开性能案例，CXL-PNM 从研究原型进入加速器产品路线。
- CXL 3.x dynamic pooling 早于预期进入量产 cloud racks，Pangaea-like 软件不再只是工具，而成为 memory-as-a-service 的控制平面。

## 5. 当前市场规模、未来一年增速和利润率预测

> 注意：CXL 仍处于早期商业化，很多细分产品没有单独披露收入。下表把“公开市场数据”和“本文推算”分开。金额均为美元。

| 产品/技术 | 当前市场规模 | 未来一年基准 | 未来一年乐观 | 未来一年超预期乐观 | 当前利润率/未来走向 |
|---|---:|---:|---:|---:|---|
| CXL memory expansion 总市场 | 2025 年 13 亿；公开 2026E 16.7 亿 | 2027 年化 22-24 亿，约 +30-40% | 28-32 亿，约 +70-90% | 38-47 亿，约 +130-180% | 当前推算毛利 40-60%。DRAM 高价支撑模组 ASP，但早期良率/验证成本高；未来 12 个月毛利可能上行至 45-65%，若 DRAM 价格回落则回落 |
| CXL component 市场：controller、switch、memory expander、dev kit | 2024 年 19 亿；按 32% CAGR 推算 2026E 约 33 亿 | 2027E 约 43-45 亿，约 +32-36% | 52-58 亿，约 +60-75% | 65-75 亿，约 +100-125% | Controller/switch Fabless 毛利可参考 Astera 75% 左右；未来取决于 hyperscaler 定制占比，毛利大概率 68-78%，经营杠杆强 |
| CXL smart memory controllers | 2026E 推算 12-16 亿，来自 component 市场子集 | +35-50% | +70-100% | +120-160% | 当前高端连接芯片毛利 70%+。Astera 2025 非 GAAP gross margin 75.8%、operating margin 39.2%；未来若竞争加剧，毛利可能从 75% 附近缓慢下行，但规模效应支持 operating margin |
| CXL switch/fabric/retimer | 2026E 推算 5-9 亿，仍小于 controller/memory module | +40-60% | +80-120% | +150% 以上 | 早期产品高 ASP、高研发摊销。毛利区间 55-75%；CXL 3.x/4.0 拓扑放量后，switch value capture 提升 |
| Pangaea-like memory orchestration/software | 独立市场未披露；2026E 推算 1-3 亿，主要嵌在硬件、云内部软件和 support | +80-120% | +150-250% | 2027 年化接近 10 亿 | 软件毛利理论 70-85%，但开源/云内部化会压低可见收入。真实利润来自硬件 pull-through、云资源利用率提升和 support |
| CXL-PNM/near-memory vector search/KV cache offload | 2026 年基本是 PoC/R&D，商业收入估计小于 0.5 亿 | 0.5-1.5 亿 | 2.5-5 亿 | 6-10 亿 | 现在可能亏损或低毛利。若形成专用 SoC/模组，成熟毛利可达 55-70%；但软件生态风险最高 |
| CXL-attached DRAM/上游 memory 大盘 | IDC：2026 DRAM 4186 亿、NAND 1741 亿；Gartner：2026 memory 6333 亿 | Gartner 2027 memory 7481 亿，较 2026 +18%；IDC 2027 memory 7904 亿，较 2026 +33% | 若 AI/HBM/DDR5 继续短缺，DRAM/NAND ASP 高位维持，收入增速高于 +30% | 供应继续失衡，利润率维持历史峰值到 2027H2 | Micron FQ2 2026 gross margin 74.4%，FQ3 guide 约 81%；Samsung DS Q4 2025 op margin 约 37.3%；SK hynix Q3 2025 op margin 47%。未来 12 个月维持高位，2027H2 后有正常化风险 |

### 5.1 对利润率的拆分判断

1. Memory module 厂的利润率：受 DRAM 价格影响最大。2026 年 DRAM 价格和供应紧张是顺风，模组厂可以赚更高 ASP，但 CXL 模组早期规模小、验证和库存风险高，净利率未必等于 commodity DRAM。
2. Controller/switch 厂的利润率：更像高端 fabless connectivity。Astera Labs 2025 全年非 GAAP operating margin 39.2%，Q4 非 GAAP operating margin 40.2%，Q1 2026 指引 gross margin 约 74%，这是 CXL controller/switch 可实现利润率的上沿参考。
3. 软件编排的利润率：若以开源和云内部平台存在，收入不可见；若以 enterprise support/fleet management 收费，毛利很高。最现实的 monetization 是把软件作为卖硬件和云内存层的放大器。
4. CXL-PNM 的利润率：短期看不到稳定商业毛利。若最终成为 vector/KV offload 的标准加速器，利润率会接近 AI edge accelerator/SmartNIC；若 API 不能标准化，则停留在定制项目。

## 6. 可能和市场共识相违背的洞见

### 6.1 CXL 的杀手级卖点不是“更快”，而是“系统利用率更高”

市场常问 CXL latency 高不高。会议答案是：单个远端访问当然慢，Pangaea 甚至承认单 pod 慢 10-14%。但如果同一台机器能从 3 个 10GB pod 变成 6 个以上，系统总吞吐最高 5x，云厂商会接受单实例小幅变慢。投资上应看 utilization/TCO 指标，而不是只看 ns latency。

### 6.2 DRAM 涨价可能加速 CXL，而不是压制 CXL

直觉认为 DRAM 越贵，CXL 模组也越贵，客户会延后购买。但 2026 的环境是 memory inflation 已经破坏本地 DRAM 过配模型：Gartner 预测 2026 年 DRAM 价格 +125%、NAND +234%；IDC 预测 DRAM 收入 +177%。在这种环境下，减少 stranded memory 和把 warm data 放进共享池的 ROI 反而提高。CXL 是“贵内存时代的利用率工具”。

### 6.3 CXL-PNM 的关键不是 CXL 4.0，而是 workload API

CXL 4.0 把速率拉到 128GT/s 当然重要，但 PNM 的思路是减少数据移动。向量检索、RAG、KV cache 是最天然目标。若 FAISS/vLLM/vector DB 生态形成稳定 offload API，CXL-PNM 可能在 CXL 2.0/3.x 时代就有商业价值；如果没有 API，128GT/s 也只是更快地搬原始数据。

### 6.4 软件层是最大瓶颈，也可能是最大 alpha 来源

Samsung CMM-D 产品页自己提到，CXL 增长不如预期的原因包括 CXL 2.0 以上标准尚未充分商业化，以及 CPU、memory、switch、device 生态不成熟。Pangaea 的出现说明厂商已经把瓶颈从硬件 datasheet 转向 Kubernetes、Redfish、OCP DCMFM、Linux hotplug、NUMA policy。市场若只盯内存厂和控制器厂，会漏掉 orchestration 和 fleet management 的价值。

### 6.5 CHMU 可能比“更低延迟 CXL PHY”更关键

本地 DRAM 和 CXL memory 的绝对延迟差距很难完全消除。CHMU 的思路是只让热页留在高性能层，冷/温页在 CXL 层。若硬件能低成本识别 hot pages，OS 层自动迁移，应用层甚至无需知道 CXL 存在。这比单纯优化 PHY latency 更接近大规模部署需求。

## 7. 未来一年关键跟踪指标

1. Azure M-series CXL preview 是否 GA，是否公布客户案例、VM SKU、定价和性能边界。
2. AWS/GCP/Oracle/Meta 是否跟进公开 CXL-attached memory、memory tier 或 CXL-backed bare metal。
3. Linux kernel、Red Hat、Kubernetes NRI、CXL driver 中 CHMU/hot page monitoring/dynamic capacity 的合并进度。
4. CXL 3.x switch、MLD、DCD、memory pooling 的互操作认证和公开产品。
5. Samsung CMM-D 容量从 256GB 走向 512GB/1TB 的节奏；Micron CZ120/CMM 后续容量；SK hynix CMM 客户验证进度。
6. Pangaea v2 是否开源或形成参考实现，是否有 Kubernetes production case。
7. CXL-PNM 是否从 FAISS IVF Flat 扩展到 HNSW、PQ、DiskANN、vLLM KV cache、secure multi-tenant memory。
8. DRAM/NAND ASP 和 memory vendor gross/operating margin 是否在 2026H2 继续上行，还是提前正常化。

## 8. 来源索引

- CXL Consortium 官方会议页：2026-04-01 Vertical Optimization of the CXL Stack，列出三大问题和 S-CHMU/CXL-PNM/Pangaea 三项技术，并提供回放链接。<https://computeexpresslink.org/event/overcoming-cxl-limitations-enabling-cxl-hardware-and-software-as-vertical-optimization-technologies/>
- CXL Consortium YouTube 回放：Vertical Optimization of the CXL Stack Webinar。<https://www.youtube.com/watch?v=LPhs-f8t9uk>
- CXL 官方 About 页面：CXL 4.0 速率 128GT/s、zero added latency、bundled ports、RAS、向后兼容。<https://computeexpresslink.org/about-cxl/>
- CXL 4.0 webinar Q&A：CXL 4.0 基于 PCIe 7.0，128GT/s；CXL 3.0 Dynamic Capacity Device 支持近即时增删内存容量。<https://computeexpresslink.org/blog/introducing-the-cxl-4-0-specification-webinar-qa-recap-4386/>
- CXL 3.x webinar Q&A：OS-level tiering 更可扩展，CHMU 目标是支持纯 OS-based memory tiering。<https://computeexpresslink.org/blog/an-overview-of-the-cxl-3-x-specification-webinar-qa-recap-3624/>
- Astera Labs 与 Microsoft Azure M-series CXL preview：Leo CXL 2.0、单 controller 最高 2TB、server memory capacity 超过 1.5x。<https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-leo-cxl-smart-memory-controllers-microsoft-azure-m>
- Astera Leo CXL Smart Memory Controllers 产品页：memory expansion/pooling/sharing、AIC 最高 2TB、AI/IMDB/HPC 性能案例。<https://www.asteralabs.com/products/leo-cxl-smart-memory-controllers/>
- Astera Labs 2025 全年业绩：2025 revenue 8.525 亿美元，非 GAAP gross margin 75.8%，non-GAAP operating margin 39.2%，Q1 2026 gross margin 指引约 74%。<https://asteralabs.gcs-web.com/news-releases/news-release-details/astera-labs-reports-fourth-quarter-and-full-year-2025-financial>
- Samsung CMM-D 产品页：MD220，CXL 2.0、PCIe 5.0、最高 256GB、DDR5、EDSFF E3.S 2T；并说明 CXL 增长慢的生态原因。<https://semiconductor.samsung.com/cxl-memory/cmm-d/>
- Samsung/Red Hat CXL memory 验证：RHEL 9.3、KVM、Podman 环境验证。<https://news.samsungsemiconductor.com/global/samsung-electronics-and-red-hat-partnership-to-lead-expansion-of-cxl-memory-ecosystem-with-key-milestone/>
- Samsung CMM-D IMDB 白皮书，2026-03：CMM-D 支持 CXL 2.0/PCIe 5.0；实测 latency、bandwidth、SAP HANA/IMDB 适配。<https://download.semiconductor.samsung.com/resources/white-paper/Samsung_CMM-D_Utilization_in_IMDB_Applications.pdf>
- Micron CXL Memory Expansion 白皮书：CZ120 CMM 每块最高 256GB、PCIe Gen5 x8、四块 CMM 提供 1TB far memory；真实平台性能数据。<https://www.micron.com/content/dam/micron/global/public/products/white-paper/cxl-memory-expansion-a-close-look-on-actual-platform.pdf>
- Strategic Market Research：CXL component market 2024 年 19 亿美元、2030 年 123 亿美元、CAGR 32%。<https://www.strategicmarketresearch.com/market-report/compute-express-link-component-market>
- MarketIntelo：CXL memory expansion market 2025 年 13 亿美元、2026 年 16.7 亿美元、2034 年 118 亿美元、CAGR 28.7%。<https://marketintelo.com/report/cxl-memory-expansion-market>
- Gartner 2026 半导体预测：2026 semiconductor revenue 1.3202 万亿美元，memory revenue 6333 亿美元，DRAM price +125%，NAND +234%。<https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-2026>
- IDC 2026 半导体预测：2026 semiconductor revenue 1.29 万亿美元，DRAM 4186 亿美元，NAND 1741 亿美元，2027 memory 7904 亿美元。<https://www.idc.com/resource-center/blog/semiconductor-market-to-surge-past-the-trillion-dollar-threshold-ai-infrastructure-drives-market-growth/>
- TrendForce 2026-01-05：1Q26 conventional DRAM contract price +55-60% QoQ，server DRAM >60% QoQ。<https://www.trendforce.com/presscenter/news/20260105-12860.html>
- TrendForce 2026-02-26：4Q25 DRAM revenue 535.8 亿美元，QoQ +29.4%；Samsung/SK hynix/Micron 市占和 ASP；Nanya operating margin 39.1%。<https://www.trendforce.com.tw/presscenter/news/20260226-12938.html>
- Samsung Electronics 4Q/FY2025：DS division Q4 revenue KRW 44.0T，operating profit KRW 16.4T；Memory Business record revenue/profit。<https://news.samsungsemiconductor.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results/>
- Micron FQ2 2026：revenue 238.6 亿美元，gross margin 74.4%，FQ3 gross margin guide 约 81%，Cloud/Core Data Center gross margin 74%。<https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026>
- SK hynix 3Q25：revenue KRW 24.4489T，operating profit KRW 11.3834T，operating margin 47%，已完成下一年 HBM supply discussion，并称下一年 DRAM/NAND demand secured。<https://www.prnewswire.com/news-releases/sk-hynix-announces-3q25-financial-results-302597593.html>
# Data Center World 2026：AI 数据中心从“机房”进入“工业基础设施”的转折报告

资料边界：本报告只使用公开网络资料，不引用本地项目文件。覆盖官方 keynote/agenda、AFCOM State of the Data Center 2026、Omdia 分析师峰会、Data Center Knowledge、Data Center Frontier、TechRepublic、Trane/ABB/Belden/Schneider 等公开材料。截至日期：2026-05-08。未来一年预测口径指 2026E 到 2027E。

## 一页结论

Data Center World 2026 的主线非常清晰：AI 数据中心不再是传统 IT 机房扩容，而是在变成以电力、热管理、工业控制和供应链为核心的“AI 工厂”。官方 keynote 直接把焦点放在 Google、NVIDIA、Oracle 的 AI 基础设施扩展，以及电力获取、800VDC、工业级数据中心、阿拉斯加自然冷却/能源选址等主题上。

最重要的变化是约束条件从“芯片和机架”转向“电力接入、变压器/开关柜/UPS、液冷工程、现场发电、模块化交付和社区许可”。Omdia 在 Data Center World 2026 上给出的判断是：2026 年全球数据中心投资超过 1 万亿美元，2030 年全球数据中心市场超过 1.9 万亿美元；Gartner 口径下 2026 年全球数据中心系统支出超过 6500 亿美元，同比约 +31.7%。这意味着行业已从局部高景气进入超级周期，但瓶颈和利润池明显向电力、热、建设交付和控制软件迁移。

AI 机架密度是转折点。AFCOM 2026 报告显示，平均机架密度从 2025 年约 16kW 跳到 2026 年约 27kW，70% 的受访者预计继续上升；36% 已部署液冷，28% 计划 12-24 个月内部署。官方会程中已经出现 1MW rack、1.2MW ORv3 rack、2MW 以上 rack CDU、800VDC、medium-voltage UPS、on-site generation、microgrid、long-duration energy storage 等议题，说明“百 kW 到 MW 级机架”不再是概念演示，而是开始进入标准化工程讨论。

液冷不是单一技术爆发，而是直接液冷、CDU、冷板、rear-door heat exchanger、两相冷却、热回收、水质工程和漏液风险控制一起爆发。保守市场报告给出 2026 年数据中心液冷市场约 40.7 亿美元，2033 年 276.5 亿美元，CAGR 31.5%；会议报道还引用 Omdia 数据称冷板出货从 2025 年 800 万片增长到 2030 年 3.56 亿片，约 44.5 倍。

电力设备是更硬的瓶颈。全球数据中心电力设备市场 2026 年约 257.8 亿美元，2033 年约 717.6 亿美元，CAGR 15.7%。但 800VDC、medium-voltage UPS、solid-state transformer、rack power shelf、energy storage shelf 等高密度 AI 电力架构仍是小基数高弹性阶段。未来一年最可能出现“收入未大规模体现、订单和设计导入先爆发”的情况。

模块化和预制化会从“节省工期”升级为“AI 容量交付方式”。Vertiv 在官方 keynote 中提出 12.5MW repeatable building block；ABB 展示 medium-voltage UPS 按 25MW 模块、可并到 50MW；多篇会后报道强调 hyperscaler 和 colo 正在把电力、冷却、机柜、控制系统作为可复制的 block 采购。

最反共识的点：行业并不会简单地“液冷替代风冷”或“电网不够所以项目停掉”。更可能的路径是混合冷却长期共存、现场电力成为过渡主线、优质项目因电力排队而延后但不取消，利润池从房地产租金向电力系统、冷却系统、预制模块、控制软件和运维服务迁移。

## 1. 会议重点、发展方向与转折

### 1.1 从数据中心到 AI 工厂

官方 keynote 的措辞已经变化：Oracle 讲的是 Stargate 这类超大规模 AI 基础设施如何同时重构 grid interconnection、onsite generation、substation layout、power plant architecture、data hall layout 和 rack-level design；Mitsubishi Heavy Industries 直接把下一代 AI 数据中心称为从商业设施转向“industrial facility”。这意味着数据中心设计对象不再是楼宇，而是“电厂 + 工厂 + IT 集群”的复合体。

关键事实：

- Data Center World 2026 时间为 2026-04-20 至 2026-04-23，地点为华盛顿特区 Walter E. Washington Convention Center。
- 官方 keynote 覆盖 Google、NVIDIA、Oracle、Vertiv、Schneider Electric、Mitsubishi Heavy Industries、Alaska 等。
- Vertiv 把 AI capacity 的交付抽象成 12.5MW repeatable building blocks。
- MHI 强调 hybrid on-site power generation、MV/HVDC、water-based cooling、waste heat recovery、plant-level control。
- Schneider Electric 的官方主题是 800VDC end-to-end power ecosystem，用于支持 1MW rack 级 AI 数据中心。

### 1.2 电力成为第一约束

DCW 2026 的大量议程不是围绕服务器，而是围绕 power procurement、grid interconnection、microgrid、on-site power、medium-voltage backup、clean firm power、long-duration energy storage 和地区电力选址。Data Center Knowledge 的现场报道引用 McKinsey 数据称，美国到 2030 年 AI 可能带来约 200GW 新增电力需求，同时约 104GW 发电容量面临退役，形成约 300GW 级别的供需缺口压力。

这带来三个变化：

- 选址逻辑从“靠近用户/网络/税收优惠”转为“谁能更快拿到可扩展、可许可的电力”。
- 数据中心业主开始接受 BYOP，即 bring your own power，包括天然气机组、燃料电池、BESS、微电网、核电重启/长协、地热和长时储能。
- 传统 AC 低压配电的损耗、占地、铜耗和散热压力被放大，800VDC、medium-voltage UPS、solid-state transformer 和 DC bus 开始被正式讨论。

### 1.3 液冷从“高端选配”进入“AI 标配工程”

AFCOM 2026 报告显示，36% 受访者已经部署液冷，28% 计划 12-24 个月内部署；40% 表示现有冷却基础设施无法满足需求。Data Center Knowledge 现场报道还指出，平均机架密度从 2025 年约 16kW 增至 2026 年约 27kW，70% 受访者预计继续上升。

TechRepublic 的会后报道引用 Omdia 观点称，到 2026 年底，液冷支持的服务器容量可能达到风冷的约 2 倍；但报道同时强调，power shelf、VRM、networking、storage 等组件仍需要空气流动，风冷不会消失。最实用的判断是：AI 主热源液冷化，机房环境与非芯片部件继续混合风冷化。

### 1.4 800VDC 和 MW rack 是早期但确定的方向

官方议程中 Schneider Electric 的 800VDC keynote 明确指向 1MW rack；另一场 1MW racks session 讨论 ORv3 rack 中 1.2MW 级 power conversion，以及 AC/DC PDU、rack power shelf、energy storage shelf、modular components、end-of-row CDU 超过 2MW thermal capacity。该方向的关键不是“明年全面替换 AC”，而是 hyperscale AI hall 的新建增量会逐步采用更高电压、更少转换级数、更靠近负载的电力架构。

### 1.5 建设方式从项目制转向产品化

DCW 2026 的会后报道反复出现“modularization、prefabrication、repeatable blocks、factory-built modules”。原因很简单：AI 客户需求会在施工中变化。Aligned 的现场案例显示，有客户在施工中途把电力需求提高 50%，项目不得不重构部分供电与冷却方案。传统一次性定制设计无法承受这种变化，未来赢家更可能是能提供标准化 12.5MW、25MW、50MW、100MW block 的供应商。

### 1.6 区域迁移：内陆、电力富集区和“非传统数据中心州”

Synergy Research 的 2026 年数据显示，2025 年末全球 hyperscale 数据中心约 1360 座，美国约 580 座；未来 pipeline 全球约 803 座，美国约 437 座。美国 Texas/Midwest 目前约占美国 hyperscale 容量三分之一，但在新增 pipeline 中超过一半。Data Center World 2026 对 Alaska、地热、天然气、hydro、tidal、natural cooling 的讨论，也说明行业开始把“能源禀赋”放在传统数据中心区位之上。

## 2. 爆发产品与技术路线

| 方向 | 2026 会议信号 | 基准口径：未来一年 | 乐观口径：未来一年 | 超预期乐观口径：未来一年 |
|---|---|---|---|---|
| 直接液冷、CDU、冷板 | 已从选配转向 AI hall 的默认设计项；冷板出货 2025-2030E 可能从 800 万片到 3.56 亿片 | 2026-2027 市场 +30%-35%；高端 GPU 集群标准化 D2C，CDU 交付成为瓶颈 | +45%-55%；colo 为 enterprise inference 提供 liquid-ready halls，retrofit 需求起量 | +70%-90%；如果 2026 年底液冷服务器容量达到风冷约 2 倍，CDU/冷板/快接头出现供不应求 |
| Rear-door / 两相 / 水less cooling | Belden-OptiCool 展示两相 rear-door，目标 120kW/rack，现场报道称 60kW 已证明可行 | 中密度 retrofit 和边缘 AI 先导入；主要用于 20-120kW rack | 企业和中型 colo 加速采用，因其改造难度低于整厅 direct-to-chip | 如果水权/许可成为约束，无水或低水冷却溢价显著扩大 |
| 800VDC、HVDC、medium-voltage UPS | Schneider 官方 keynote 指向 800VDC 支持 1MW rack；ABB 展示 25MW MV UPS block | 2026-2027 以 design-in、pilot、first production 为主，收入小基数 +50%-100% | hyperscaler 新建 AI hall 把 800VDC/HVDC 纳入标准设计，子赛道 +100%-200% | ORv3 1.2MW rack、MV UPS、solid-state transformer 被头部客户共同标准化，订单 +200%-300%，收入更多体现在 2027-2028 |
| Rack-level power shelf / energy shelf | 1MW rack session 把 power shelf、energy storage shelf 作为 ORv3 rack 的模块组件讨论 | 随 AI rack 从 100kW 向 300kW+ 过渡，rack power BOM 快速提升 | power shelf 和 BBU/储能 shelf 标准化，进入整 rack 采购清单 | 如果 1MW rack 设计提前落地，rack power 价值量可能超过传统 PDU/母线槽增速 |
| 现场发电、微电网、BESS | AFCOM：25% 已有 onsite generation，高于 2025 年 19%；23% 计划增加 | 天然气机组、BESS、微电网控制先爆发，+25%-35% | hyperscaler/colo 接受 BYOP，+40%-60%；gas + BESS 组合成为 24-36 个月主方案 | 如果电网排队进一步恶化，behind-the-meter power 变成容量销售的前置条件，+70%+ |
| 模块化/预制化数据中心 | Vertiv 12.5MW building block；ABB 25MW/50MW MV UPS；多家强调 prefabrication | 模块化数据中心 +15%-20%，主要满足工期和供应链确定性 | +25%-35%；AI factory block 以 12.5MW/25MW/50MW 标准化复制 | +45%+；如果大型客户把整厅/整栋作为产品采购，模块商议价能力明显增强 |
| DCIM、BMS、数字孪生、AI 运维 | DCW 讨论 grid、power plant、data hall、rack 协同控制；复杂度超过人工调度 | DCIM/BMS 与液冷、电力、资产管理融合，+20%-30% | AI workload scheduling 与热/电实时联动，+35%-50% | 如果 GPU 利用率、电价、碳约束进入统一调度，软件层成为高毛利控制点，+60%+ |
| Clean firm power：地热、核、长时储能 | 会程和报道强调 geothermal、LDES、nuclear restart、fuel cell；但没有单一解法 | 未来一年以 PPA、试点、选址储备为主，收入有限 | 先进地热和核电长协进入大型项目 pipeline，提升估值和可融资性 | 如果政策和许可加速，clean firm power 资产被数据中心长期锁定，电力开发商获得溢价 |

## 3. 市场规模、增速与利润率预测

利润率说明：下表利润率不是数据中心业主净利率，而是对应产品/技术供应商的典型毛利率或项目 EBITDA margin 估计。硬件供应商、EPC、软件、能源项目口径不同，因此用区间表达。未来一年增速为全球美元收入或订单/出货口径的近似判断。

| 产品/市场 | 当前市场规模 | 事实锚点 | 基准增速与利润率 | 乐观增速与利润率 | 超预期乐观增速与利润率 |
|---|---:|---|---|---|---|
| 全球数据中心投资/系统支出 | Omdia：2026 年投资超过 1 万亿美元；Gartner：2026 年数据中心系统支出超过 6500 亿美元 | Omdia 预计 2030 年全球数据中心市场超过 1.9 万亿美元；Gartner 预计 2026 年数据中心系统支出 +31.7% | +25%-32%；供应链紧缺维持高价格 | +35%-45%；AI inference 扩散，colo/hyperscale 同时加单 | +50%+；如果主权 AI、企业 AI 和 hyperscale 同步抢电抢设备 |
| 数据中心建设/EPC | 2026E 约 2400 亿-3000 亿美元，不同机构口径差异大 | Mordor 口径 2026 年约 3003.8 亿美元，2031 年 4313.9 亿美元；GVR 口径 2025 年约 2613.1 亿美元，2033 年 6627.1 亿美元 | +8%-13%；EPC 毛利约 8%-14%，EBITDA 4%-8%，固定价项目风险高 | +15%-20%；电力/机械总包短缺，毛利 +1-3pct | +25%+；若 megacampus 加速开工，稀缺工程队毛利 +3-5pct |
| 模块化/预制数据中心 | 2026E 约 293 亿-400 亿美元 | FMI 口径 2026 年 293 亿美元；GVR 口径 2024 年 290.4 亿美元、2030 年 757.7 亿美元，折算 2026E 约 400 亿美元 | +15%-20%；毛利 15%-25%，EBITDA 8%-14%，规模化小幅提升 | +25%-35%；标准 block 放量，毛利 +2-4pct | +45%+；若整厅产品化采购，短期毛利 +4-6pct，随后被规模采购压回 |
| 数据中心液冷系统 | 2026E 约 40.7 亿-70 亿美元 | MarketsandMarkets：2026 年 40.7 亿美元、2033 年 276.5 亿美元，CAGR 31.5%；其他机构 2025 口径更高 | +30%-35%；毛利 25%-45%，CDU/冷板/快接头短缺使毛利 +1-2pct | +45%-55%；AI colo retrofit 放量，毛利 +3-5pct | +70%-90%；如果液冷服务器容量快速超过风冷，核心部件毛利短期 +5-8pct |
| 冷板、快接头、manifold、CDU 部件 | 冷板相关 2025E 约 38 亿美元量级；2026E 高速增长 | Omdia 现场观点：冷板出货 2025 年 800 万片到 2030 年 3.56 亿片 | +35%-50%；高可靠部件毛利 30%-50% | +60%-80%；良率和认证能力带来明显溢价 | +100%+；若 GPU 供应释放且液冷成标配，部件订单倍增 |
| 数据中心电力设备：UPS、PDU、switchgear、busway、generator 接入 | 2026E 257.8 亿美元 | GVR：2026 年 257.8 亿美元、2033 年 717.6 亿美元，CAGR 15.7%；北美约 38% | +16%-20%；毛利 25%-40%，EBITDA 12%-25%，订单能见度高 | +25%-35%；变压器、开关柜、UPS 交期拉长，毛利 +2-4pct | +45%+；若电力设备成为 AI 项目交付瓶颈，头部厂商议价显著增强 |
| 800VDC / HVDC / medium-voltage UPS / solid-state transformer | 2026E 商业收入估计低于 10 亿美元，但挂靠 258 亿美元电力设备 TAM | Schneider 800VDC keynote；ABB 25MW MV UPS block；官方 1MW rack session 讨论 1.2MW ORv3 rack power | 小基数 +50%-100%；原型/早期量产毛利 35%-55%，认证成本高 | +100%-200%；若 hyperscaler design-in，毛利维持高位 | +200%-300%；标准化成功后订单爆发，但 2027 收入确认滞后 |
| 现场发电、微电网、BESS、fuel cell for data centers | 2026E 数据中心专用 behind-the-meter power 估计 80 亿-150 亿美元；更大部分体现在电力项目和长期 PPA | AFCOM：25% 已有 onsite generation，23% 计划增加；DCW 多场讨论 gas、fuel cell、BESS、LDES、geothermal、nuclear | +25%-35%；设备毛利 15%-30%，项目 EBITDA/IRR 10%-20% | +40%-60%；天然气 + BESS + 微电网控制成为主流应急方案 | +70%+；电网接入恶化时，电力项目溢价和长期合约收益上升 |
| DCIM、BMS、数字孪生、AI 控制软件 | 2026E DCIM 约 64.7 亿美元 | 市场报告口径：2026 年 DCIM 约 64.7 亿美元，2034 年约 332.5 亿美元；会议主题显示 power/cooling/workload 联动需求上升 | +20%-30%；软件毛利 60%-85%，服务拖累后 blended 55%-70% | +35%-50%；液冷和微电网复杂度提高，毛利 +2-5pct | +60%+；若 AI 调度与电价/热/碳约束闭环，软件成为高毛利控制层 |
| 水、热回收、低水耗冷却工程 | 当前独立 TAM 较小，主要嵌在冷却和工程系统内 | MHI keynote 提到 water-based cooling、waste heat recovery；Belden-OptiCool 强调 no-water rear-door cooling | +20%-30%；工程服务毛利 15%-30% | +40%-60%；缺水地区和许可压力提高低水耗系统溢价 | +80%+；如果水权/排热许可成为项目开工条件，低水耗方案可能成为强制项 |

## 4. 三种情景下的成熟和量产路线

### 4.1 基准情景

2026-2027 年行业核心不是全面技术替换，而是工程化标准形成。直接液冷在新建 AI halls 中成为默认配置，retrofit 以 rear-door、hybrid air/liquid、局部 CDU 为主。800VDC/HVDC 进入前几批大客户 design-in，收入小但战略确定。现场发电以天然气机组、BESS、微电网控制为主，先进地热、核电、长时储能更多是选址和 PPA pipeline。模块化以 12.5MW、25MW、50MW block 形式被采购，EPC 仍紧缺。

### 4.2 乐观情景

AI inference 的企业需求比市场预期更快释放，colo 需要为 enterprise AI 提供 liquid-ready capacity。液冷从 hyperscale training 扩散到金融、医疗、政务、制造的私有 AI 集群。电力设备供应商把 medium-voltage UPS、busway、switchgear、rack power shelf 做成可复制组合，订单增长快于收入确认。模块化供应商开始绑定电力和冷却系统，不只是卖箱体。软件层通过 DCIM + BMS + workload scheduler 进入闭环调优，毛利提升。

### 4.3 超预期乐观情景

主权 AI、美国内陆 megacampus、企业 inference 和 hyperscaler 训练集群同时扩张，导致 power train、cooling train 和 module train 的缺口远大于服务器本身。液冷容量在 2026 年底显著超过风冷，冷板/CDU/快接头短期供不应求。800VDC、1MW rack、MV UPS block 获得头部客户共同标准化，虽然收入主要在 2027-2028 释放，但订单和估值提前反映。现场发电从过渡方案变成容量销售前置条件，能自带可许可电力的项目获得显著估值溢价。

## 5. 可能违背当前市场共识的洞见

### 5.1 最大瓶颈不是 GPU，而是“可交付电力”

市场经常把 AI 数据中心周期看成 GPU capex 周期，但 DCW 2026 的真正信号是 power-constrained capex。GPU 可以按季度升级，电网接入、变电站、变压器、开关柜、许可和社区关系以年为单位。未来估值溢价可能从 GPU 供给转向“谁能最快交付带电容量”。

### 5.2 风冷不会消失，液冷也不是 immersion 一条路

会议材料和报道共同指向 hybrid cooling。直接液冷负责 GPU/CPU 主热源，风冷继续负责 power shelf、VRM、networking、storage 和空间余热。两相 rear-door、无水冷却、warm-water cooling 会在 retrofit 和水资源紧张地区更快渗透。沉浸式液冷仍有机会，但并不是 2026-2027 最大确定性主线。

### 5.3 800VDC 是确定方向，但不是线性替换

800VDC 的价值在于减少转换级数、降低线损和铜耗、支持 MW rack，但它依赖安全标准、连接器、保护器件、运维流程和客户共同设计。未来一年最可能爆发的是 design-in、试点和标准制定，收入规模可能落后于资本市场叙事。

### 5.4 On-site power 不是 ESG 倒退，而是“速度资产”

天然气机组、燃料电池、BESS 和微电网会被更多采用，因为电网排队比设备采购更慢。清洁电力仍重要，但会议共识更接近“clean + firm + fast + financeable”，而不是单纯追求可再生比例。先进地热、核电重启和 LDES 的价值在于长期 firm power，短期收入不会像天然气和 BESS 那么快。

### 5.5 机房房地产逻辑正在被工业供应链逻辑替代

传统数据中心投资看 PUE、租约和空置率；AI 数据中心投资要看 MW block、utility queue position、变压器交期、水权、冷却工程、燃气接入、社区许可和模块化制造能力。拥有土地但没有电力路径的资产可能被折价，拥有电力与许可路径的非传统地区资产可能被重估。

### 5.6 企业 inference 可能比 hyperscale training 更利好“中间层供应商”

Hyperscaler 会压价并自研很多部件，但 enterprise/colo inference 更依赖成套解决方案、retrofit、运维服务、DCIM、rear-door cooling、标准 CDU、模块化 hall。中型 AI 部署的碎片化需求可能带来更高毛利，而不是最低价大单。

### 5.7 数据中心的利润池会从“租金”向“工程稀缺”迁移

未来 12-24 个月，利润率最可能上行的不是所有数据中心业主，而是稀缺电力设备、液冷部件、模块化集成、现场电力项目、控制软件和能够承担复杂交付的工程服务商。业主端若无法转嫁电力和建设成本，反而可能受到 capex inflation 压缩。

## 6. 高密度数字清单

- 2026 Data Center World：2026-04-20 至 2026-04-23，华盛顿特区。
- Omdia：2026 年全球数据中心投资超过 1 万亿美元。
- Omdia：2030 年全球数据中心市场超过 1.9 万亿美元。
- Gartner：2026 年全球数据中心系统支出超过 6500 亿美元，同比 +31.7%。
- Gartner：2026 年全球 IT 支出约 6.07 万亿美元，同比 +10%。
- AFCOM：2026 年平均机架密度约 27kW，2025 年约 16kW。
- AFCOM：70% 受访者预计机架密度继续上升。
- AFCOM：36% 已部署液冷，28% 计划 12-24 个月内部署。
- AFCOM：40% 表示当前冷却基础设施无法满足需求。
- AFCOM：74% 部署 AI-capable solutions，高于 2025 年 64%。
- AFCOM：25% 已有 onsite power generation，高于 2025 年 19%；23% 计划增加。
- AFCOM：38% 已部署可再生能源，37% 计划 12-24 个月内部署。
- McKinsey/Data Center Knowledge：美国到 2030 年 AI 可能带来约 200GW 新增电力需求，叠加约 104GW 退役容量，形成约 300GW 级别缺口压力。
- Synergy：2025 年末全球 hyperscale 数据中心约 1360 座，美国约 580 座。
- Synergy：未来 pipeline 全球约 803 座，美国约 437 座。
- Synergy：Amazon、Microsoft、Google 合计约占全球 hyperscale 容量 58%。
- Vertiv：AI capacity 交付抽象为 12.5MW repeatable building blocks。
- ABB：medium-voltage UPS 以 25MW block 展示，可并联到 50MW。
- Schneider：800VDC end-to-end ecosystem 面向 1MW rack。
- 官方 1MW rack session：ORv3 rack 讨论 1.2MW power conversion，end-of-row CDU 超过 2MW thermal。
- Belden-OptiCool：两相 rear-door cooling 目标 120kW/rack，报道称 60kW/rack 已证明可行；声称相对传统机房 cooling capacity 最高 10 倍、能耗约 1/3。
- MarketsandMarkets：数据中心液冷市场 2026 年约 40.7 亿美元，2033 年约 276.5 亿美元，CAGR 31.5%。
- Omdia/TechRepublic：冷板出货 2025 年约 800 万片，2030 年约 3.56 亿片。
- GVR：数据中心电力市场 2026 年约 257.8 亿美元，2033 年约 717.6 亿美元，CAGR 15.7%。
- GVR：北美占数据中心电力市场约 38%，solution 约占 72.2%。
- FMI：模块化数据中心市场 2026 年约 293 亿美元；GVR 口径折算 2026E 约 400 亿美元。
- Mordor：数据中心建设市场 2026 年约 3003.8 亿美元，2031 年约 4313.9 亿美元。
- GVR：数据中心建设市场 2025 年约 2613.1 亿美元，2033 年约 6627.1 亿美元。
- 市场报告口径：DCIM 2026 年约 64.7 亿美元，2034 年约 332.5 亿美元。

## 7. 信息来源

- Data Center World 官方新闻稿：[Data Center World 2026 to Host Main Stage Keynotes from Google, NVIDIA, Oracle](https://www.datacenterdynamics.com/en/news/data-center-world-2026-to-host-main-stage-keynotes-from-google-nvidia-oracle/)
- Data Center World 官方 keynote 页面：[Data Center World 2026 Keynotes](https://datacenterworld.com/keynotes/)
- Data Center World 官方议程：[2026 Event Schedule](https://schedule.datacenterworld.com/)
- Omdia 分析师峰会官方会程：[The Trillion Dollar AIDC Boom](https://schedule.datacenterworld.com/session/the-trillion-dollar-aidc-boom-from-megaclusters-and-microgrids-to-the-moon/918298)
- Data Center Knowledge 会后报道：[As AI Scale Surges, a Call to Build for Legacy](https://www.datacenterknowledge.com/ai-data-centers/data-center-world-as-ai-scale-surges-a-call-to-build-for-legacy)
- Data Center Knowledge 会后报道：[Real Estate, Distributed Power Reshape AI Buildout](https://www.datacenterknowledge.com/energy-power-supply/data-center-world-2026-real-estate-distributed-power-reshape-ai-buildout)
- Data Center Knowledge 会后报道：[The Push for Clean, Firm Power](https://www.datacenterknowledge.com/energy-power-supply/data-center-world-2026-the-push-for-clean-firm-power)
- Data Center Frontier 会后报道：[Data Center World 2026 Innovation Spotlight](https://www.datacenterfrontier.com/hyperscale/article/55373434/data-center-world-2026-innovation-spotlight)
- TechRepublic 会后报道：[Data Center World 2026 Recap](https://www.techrepublic.com/article/news-data-center-world-2026/)
- Trane Data Centers 官方总结：[Insights and Key Takeaways from DCW 2026](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/blogs/insights-key-takeaways-dcw2026.html)
- Synergy Research：[Hyperscale Data Center Capacity Growth](https://www.srgresearch.com/articles/hyperscale-data-center-capacity-growth-to-exceed-50-over-next-four-years)
- Gartner：[Forecasts Worldwide IT Spending to Grow 10% in 2026](https://www.gartner.com/en/newsroom/press-releases/2025-10-21-gartner-forecasts-worldwide-it-spending-to-grow-10-percent-in-2026)
- MarketsandMarkets：[Data Center Liquid Cooling Market](https://www.marketsandmarkets.com/Market-Reports/data-center-liquid-cooling-market-88379179.html)
- Grand View Research：[Data Center Power Market](https://www.grandviewresearch.com/industry-analysis/data-center-power-market)
- Grand View Research：[Data Center Construction Market](https://www.grandviewresearch.com/industry-analysis/data-center-construction-market-report)
- Future Market Insights：[Modular Data Center Market](https://www.futuremarketinsights.com/reports/modular-data-center-market)
- Grand View Research：[Modular Data Center Market](https://www.grandviewresearch.com/industry-analysis/modular-data-center-market)
- DCIM 市场数据参考：[Data Center Infrastructure Management Market](https://marketpublishers.com/report/it-technology/data_center_infrastructure_management_market_forecasts_from_2026_to_2031.html)
# DATE 2026 Conference 高浓度调研报告：AI 时代芯片设计的转折点

报告日期：2026-05-08  
会议对象：DATE 2026, Design, Automation and Test in Europe Conference, 2026-04-20 至 2026-04-22, Verona, Italy。  
信息范围：只使用公开外部资料，包括 DATE 官方日程、Keynote/Focus Session/Tutorial/论文摘要、公开市场数据和公司公开财报；未参考项目内文件或历史信息。  
核心来源：DATE 官方主页/日程/Keynotes、WSTS、Gartner、SEMI ESD Alliance、Cadence、Synopsys、NVIDIA、TSMC、TrendForce、Yole/Grand View Research/SHD Group 等公开材料。

## 一页结论

DATE 2026 的主线不是“AI 又带来更多算力需求”这么简单，而是芯片设计产业链的控制点在迁移：从单点 EDA 工具、单颗 SoC、单一制程节点，迁移到“AI workload - 3D/chiplet/package - memory - interconnect - security - agentic design flow”的系统级闭环。

最强信号有 7 个：

1. **AI 算法迭代月级，半导体平台迭代年级，错配正在逼迫全栈重构。** imec 开场 Keynote 明确把 next-gen AI 的先进推理 workload、密度、功耗、内存瓶颈放到同一张图里，结论是必须重塑 AI-optimized compute architecture 和半导体技术平台。
2. **Agentic EDA 从 demo 进入“可部署的生产流”叙事。** DATE 官方 Sponsors Executive Session 直接写到 Agentic AI 正从实验演示进入 production EDA flows；Focus Session FS07 把 HLS、physical design、test、security verification 串成端到端 multi-agent flow。
3. **Chiplet 进入“市场承诺兑现期”，但真正瓶颈不是有没有 UCIe，而是仿真、热、封装、安全、KGD、供应链责任。** DATE FS04 的标题就是“Chiplets: How far from making promise a reality?”，官方摘要明确列出 open chiplet marketplace 的挑战：interface standardization、simulation、security、thermal、packaging。
4. **3D/2.5D 已经从架构选择变成 EDA/可靠性问题。** DATE TS06、TS20、TS40、TS41 连续出现 3D IC thermal FEM、EM/IR drop、multi-chiplet SystemC-TLM simulator、Hetero-ChipletSim、3D stacked LLM accelerator、3D placement、BSPDN/power-thermal co-optimization。
5. **Open-source silicon 的重心从“教育/玩具 tapeout”转向“欧洲战略、open PDK、成熟节点制造、SME 定制芯片”。** Luca Benini 的午间 Keynote 是“Democratizing Silicon”，SD03 讨论 IHP 130nm SiGe BiCMOS open PDK、TinyTapeout、ChipFlow；ET03 用 Bambu、SODA-OPT、OpenROAD 做 end-to-end open-source accelerator flow。
6. **硬件安全不再是后置合规，而是 AI 基础设施和 SDV/edge AI 的前置经济约束。** FS05 聚焦 SoC/CPU/AI accelerator 新威胁和 AI-assisted validation；YPP/Best Poster 里出现神经网络 FPGA accelerator side-channel，LBR01 出现 28nm analog compute-in-memory macro 的实测功耗侧信道，QUBIP 讨论 PQC 迁移到工业 IoT。
7. **Silicon photonics 和 CPO 不是“光计算替代 GPU”的短线故事，短线更像 AI cluster interconnect/thermal co-design 的瓶颈解除器。** DATE tutorial 把 silicon photonic AI 的 microring、phase shifter、laser 热漂移、inter-chiplet thermal coupling、diamond/graphene heat dissipation 放在系统架构层讨论；TS41 用 physics-informed neural simulator 把 nanophotonic device EM 仿真时间降低 76.09%。

## DATE 2026 会议一手信号

### 官方事实

- DATE 2026 官方主页显示会议时间为 **2026-04-20 至 2026-04-22**，地点 **Verona, Italy**。官方定位是 “The European Event for Electronic System Design & Test”。来源：[DATE 2026 官方主页](https://www.date-conference.com/)。
- 官方说明 DATE 2026 proceedings 对注册用户开放下载，下载期到 **2026 年 5 月底**。来源：[DATE 2026 官方主页 Proceedings 信息](https://www.date-conference.com/)。
- 会议 Keynotes：
  - **Luc Van den hove, imec**：next-gen AI、advanced reasoning workloads、density/power/memory constraints、EU Chips Act pilot line、health/automotive ecosystem。
  - **Bettina Heim, NVIDIA**：NVQLink、GPU real-time processing for QPU、RoCE 绕过传统网络栈和 CPU、sub-microsecond data transfer、quantum error correction 对部分 QPU 架构的 latency tolerance 是 tens of microseconds。
  - **Zhiru Zhang, Cornell**：Allo, open-source Python/MLIR framework，统一 accelerator design 和 programming，指向 automated compiler construction、differentiable hardware synthesis、agentic design automation。
  - **Rolf Drechsler, Bremen/DFKI**：AI reshaping research and education，但机器结果缺少真正理解，可靠性和责任成为问题。
  - **Luca Benini, ETHZ/University of Bologna**：open-source EDA、Europe strategic roadmap、lowering barriers、technological sovereignty、open-source chips。来源：[DATE 2026 Keynotes](https://www.date-conference.com/)。
- Best Paper/PhD 信号：
  - D_low Best Paper：FSDB, folded-store dynamic-broaden hybrid compute-in-ROM/SRAM architecture for large-scale DNNs on-chip。
  - D_high Best Paper：Torrent, distributed DMA for point-to-multipoint data movement。
  - A Track Best Paper：INSPIRE, in-sensor compressed weight retrieval for ViT efficiency at edge。
  - T Track Best Paper：RIFT, LLM accelerator fault assessment using reinforcement learning。
  - PhD Forum Best Poster 包括 Generative AI in Hardware Design Flow 和 Side-Channel Awareness in Neural Network FPGA Accelerators。来源：[DATE 2026 Awards](https://www.date-conference.com/)。

### 技术信号浓缩

| 方向 | DATE 2026 一手信号 | 转折含义 |
|---|---:|---|
| Agentic EDA | FS07 讨论 HLS datasets/benchmarking、LLM/RL/TPE test generation、LLM physical design、VeriChat security verification；ES02 明确生产 EDA flows、RTL checking/fixing、spec-to-testbench、synthesis-to-GDSII agentic flow | 从“帮写 Verilog/脚本”转向“闭环调用工具、读报告、做约束优化、保留审计轨迹”的工程系统 |
| Chiplet/3D | FS04 讨论 open chiplet marketplace，TS20/TS40 有 TSIM4ICS、Hetero-ChipletSim，TS41 有 3D placement/BSPDN，TS06 有 EM/thermal/IR drop | chiplet 不是封装厂单点红利，而是 EDA/IP/test/package/thermal/security 全链条红利 |
| HBM/logic-memory | TS20 FlashGEMM 面向 3D-stacked LLM accelerators，报告 up to 1.50x TTFT、7.11x throughput improvement | LLM 推理性能瓶颈正在从 FLOPS 迁移到 memory topology 和 NoC/locality |
| Silicon photonics | Tutorial 强调 thermal robust photonic AI，TS41 SuperPhys-Net 把复杂纳米光子器件仿真精度提升 72.61%、计算时间降低 76.09% | 光子不是纯器件故事，EDA/多物理仿真/热管理会成为商业化门槛 |
| Open-source silicon | SD03: IHP open fabrication ecosystem、130nm SiGe BiCMOS open PDK、TinyTapeout、Chipathon、Code a Chip；ET03: Bambu/SODA/OpenROAD | 成熟节点、混合信号、教育、SME 定制芯片是最先兑现的 open silicon 市场 |
| Hardware security | FS05: AI accelerator threat landscape、formal-fuzzing、AI-guided validation；VeriChat Faithfulness 87.73%；side-channel work 100% layer-size recovery in folding-aware attack | 硬件漏洞一次流片后不可变，security verification 将进入 signoff 预算 |
| SDV/edge trusted AI | UP2DATE4SDV、DI-EDAI、dAIEDGE，强调 safe/secure software updates、hardware upgrades、mission-critical edge AI | 车载/工业/航空 AI 不缺模型，缺的是认证、更新、安全、实时约束下的硬件部署流 |

## 和此前市场/技术叙事相比，重要变化是什么

### 变化 1：从“节点红利”变成“系统红利”

2023-2025 年市场喜欢把 AI 半导体拆成 GPU、HBM、CoWoS、先进制程几个单点。但 DATE 2026 的论文结构显示，系统级问题已经压过单点问题：3D placement 会影响 WNS/TNS，BSPDN 会影响 IR drop 和峰值温度，chiplet simulator 要同时建模 die-to-die interconnect 和 package effects，photonic AI chip 要把 device thermal drift 和 architecture thermal mapping 放在一起。

关键数字：

- ETLA-3D 对 hybrid bonding F2F 3D IC thermal FEM 做等效薄层聚合，相比 COMSOL runtime up to **695.8x** faster，最大绝对误差 **<1.1°C**。
- EMaper 对 EM-aware placement/routing 在 ISPD2018 benchmark 消除 **92.1%-100%** EM violations，代价是 wirelength/via count **4.49%-16.3%** overhead。
- 3D IC placement 论文改善 **13.0% WNS**、减少 **7.85% TNS**。
- 7nm 3D CPU + BSPDN/thermal co-optimization：MoL+BSPDN 把 logic die worst-case IR drop 降到 2D reference 的 **1/4**，峰值温度相比 LoM 低 **>15°C**，进一步 TSV/material 优化可再降 **50% IR drop** 和 **14°C**。

结论：先进封装不是制造后段，而是前端架构和 EDA 的约束入口。未来 1-2 年，先进封装产业链里最容易被低估的是 **thermal/IR/EM-aware EDA、package-aware NoC/IP、chiplet simulation、KGD/test/security signoff**。

### 变化 2：Agentic EDA 的商业化入口不是“替代工程师”，而是“替代重复的工具闭环”

DATE 2026 对 Agentic EDA 的态度很克制但明确：LLM alone 会 hallucinate，general-purpose chatbot 不可靠；真正能进入生产的是 RAG、多代理、工具调用、结构化报告解析、约束驱动反馈回路。

关键数字和事实：

- FS07 HLS 方向明确指出 HLS 没有真正 democratize hardware design，因为仍需要 HLS optimization、DSE、toolflow debugging、QoR analysis 专家。
- HLSFactory 目标是构建 cross-vendor HLS design spaces，并把 HLS/FPGA toolflows 的输出标准化为 datasets。
- LLM/RL/TPE test generation 在 RISC-V core functional testing 和 6 个 benchmark circuits 的 structural testing 上达到接近 expert-generated ATPG scripts 的 test quality，并提升效率/可扩展性。
- VeriChat 用 retrieval-augmented multi-agent workflow，Faithfulness **87.73%**，显著高于通用 proprietary models。
- CoverAssert 用 functional coverage feedback 迭代生成 SystemVerilog assertions，在 4 个 open-source designs 上平均提升 **9.57% branch coverage**、**9.64% statement coverage**、**15.69% toggle coverage**。

结论：2026-2027 年 EDA AI 的收入不会主要来自“自然语言一键出芯片”，而来自 4 类插件化高价值闭环：verification/testbench、coverage closure、physical implementation ECO、security verification。

### 变化 3：Open-source EDA 是新入口，不是对商业 EDA 的简单替代

DATE 2026 的 open-source 讨论明显从“工具理想主义”转向“制造和商业模式”。IHP 130nm SiGe BiCMOS open PDK、TinyTapeout、ChipFlow、Bambu/SODA/OpenROAD 表明，open-source flow 首先服务教育、研究、SME、成熟节点、定制 accelerator 和 reproducible research。

市场逆向点：open-source EDA 反而可能扩大 Cadence/Synopsys 的高端市场，因为成熟节点/教育/SME 的低成本入口会产生更多真实 silicon projects，其中一部分在规模化、mixed-signal、signoff、先进节点阶段仍会购买商业工具/IP。

### 变化 4：AI 基础设施的安全面扩大，硬件安全成为前置商业需求

DATE FS05 的官方描述很重：AI accelerators 已经成为政府、企业、研究机构 AI infrastructure backbone；如果被攻破，会影响 model reliability、data confidentiality、national-scale AI systems。更重要的是，hardware flaws fabricated 后不可变，pre-silicon security validation 有直接经济价值。

关键事实：

- LBR01 提出第一批针对 fabricated **28nm analog compute-in-memory macro** 的实测 power side-channel 分析，可用 CNN workload 的 power trace 重建 private input images，MSSIM up to **0.71**。
- Neural network FPGA accelerators 的 folding-aware side-channel method 对 layer-size recovery 达到 **100%**，并显示 side-channel 也可变成 out-of-distribution/fault detection safety signal。
- QUBIP 项目把 PQC migration 放进 resource-constrained industrial IoT，目标是长期 data integrity/resilience。

结论：AI accelerator/edge AI/SDV 的硬件安全验证会成为 EDA 和 IP 预算里的新增项，且可能被法规和客户认证周期放大。

## 哪些产品和技术方向会爆发

### 1. Agentic EDA/AI-native verification

成熟与量产路线：

| 口径 | 2026-2027 路线 | 爆发力度 |
|---|---|---:|
| 基准 | 从 IDE/copilot、lint/RTL checking、testbench generation、coverage assistant 进入企业内网；要求 RAG、tool API、审计日志、deterministic fallback | EDA 增量收入 **+10%-15%/年**，AI 功能多以 seat uplift/enterprise add-on 体现 |
| 乐观 | HLS/DSE、formal/fuzzing、physical design ECO、security verification 形成闭环；Cadence/Synopsys/Siemens 与云厂自研 flow 结合 | 高价值验证/实现环节单独 **+20%-30%/年**；EDA 总市场增速上移到 **15%-18%** |
| 超预期乐观 | Agent 可以从 spec 到 RTL/test/初版 GDSII 自动跑通，并在成熟节点/FPGA/accelerator 子类设计中稳定复现 PPA | 中小芯片设计项目数量倍增，EDA+IP+云仿真合计 **+25%-35%/年**，但 signoff 仍不会完全无人化 |

判断：2026 年不是“AI 设计芯片”的元年，而是“AI 管理 EDA 工具闭环”的元年。最先赚钱的是 verification、coverage、test、security，不是全自动 SoC architect。

### 2. Chiplet/2.5D/3D/HBM 封装生态

成熟与量产路线：

| 口径 | 2026-2027 路线 | 爆发力度 |
|---|---|---:|
| 基准 | GPU/AI ASIC + HBM 的 2.5D 封装持续扩产；closed/internal chiplet 为主，UCIe 更多用于同一生态内 | AI 高端封装收入 **+40%-60%/年**，整体 advanced packaging **+15%-25%/年** |
| 乐观 | CoWoS-L/SoIC/混合键合、UCIe IP、D2D PHY、package-aware EDA 成熟；云厂 ASIC 与网络芯片扩大 chiplet 化 | 高端封装和 D2D IP **+60%-90%/年**；先进封装产能成为 AI server 交付的第二瓶颈 |
| 超预期乐观 | 多供应商 chiplet marketplace 出现可复用 SKU；KGD/test/security/thermal 标准跑通 | 2027 开始出现真正平台化 chiplet 采购，EDA/IP/test/package capture rate 大幅上升，但概率低于市场叙事 |

判断：短期真正爆发的是 **高端封装产能、HBM attach、D2D PHY/IP、thermal/power signoff、chiplet simulation**，不是通用 chiplet marketplace。

### 3. HBM/3D memory/logic-memory co-design

成熟与量产路线：

| 口径 | 2026-2027 路线 | 爆发力度 |
|---|---|---:|
| 基准 | HBM3e 继续主力，HBM4 在 2026H2 放量；AI accelerator 每卡/每封装 HBM 容量继续上升 | HBM 收入 **+25%-40%/年**，DRAM/HBM 利润率继续高于历史均值 |
| 乐观 | HBM4 良率爬坡快，Samsung/Micron 补位，custom ASIC 需求加单；memory inflation 延续到 2027 | HBM 收入 **+50%-70%/年**，供需紧张支撑高 ASP |
| 超预期乐观 | 3D-stacked logic-memory、near-memory GEMM、CXL/memory pooling 与 rack-scale AI 架构共振 | HBM+advanced memory 子市场向 **$100B+** 加速靠拢，memory 厂商利润率接近周期峰值 |

判断：DATE 2026 的 FlashGEMM、compute-in-ROM/SRAM、CIM/neuromorphic 论文说明，“内存墙”已经是 LLM 推理体验指标 TTFT/throughput 的核心问题。市场上 HBM 不只是容量周期，更是 AI 系统性能税。

### 4. Silicon photonics/CPO/optical interconnect

成熟与量产路线：

| 口径 | 2026-2027 路线 | 爆发力度 |
|---|---|---:|
| 基准 | 1.6T optical modules、LPO、near-package optics 先放量；CPO 仍是早期验证 | Silicon photonics **+25%-35%/年**，CPO 从很小基数 **+40%-70%/年** |
| 乐观 | AI rack-scale 网络功耗成为刚性约束，switch ASIC 与 optical engine 更深绑定 | CPO/光互连 **+80%-120%/年**，但绝对规模仍小于 HBM/封装 |
| 超预期乐观 | CPO serviceability、thermal、standardization 解决，进入 hyperscaler 标准平台 | CPO 从 $0.xB 迅速跃迁到数十亿美元级，但更可能在 2028 后 |

判断：近期投资抓手是 optical module、laser、driver/TIA、silicon photonics foundry、thermal/EM simulation，不是“光计算替代 GPU”。

### 5. RISC-V/open-source silicon/成熟节点定制芯片

成熟与量产路线：

| 口径 | 2026-2027 路线 | 爆发力度 |
|---|---|---:|
| 基准 | MCU、IoT、embedded controller、AI accelerator control plane、教育/研究 tapeout 继续增长 | RISC-V 相关 IP/SoC 收入 **+25%-35%/年** |
| 乐观 | Edge AI、automotive real-time、China/Europe sovereignty 需求推动商业 IP 和 open cores 并行 | 收入 **+40%-60%/年**，shipment penetration 快于收入 penetration |
| 超预期乐观 | 大厂 custom AI ASIC/edge accelerator 大规模采用 RISC-V control/host cores，open PDK 成熟 | 出货量爆发，但 IP 单价可能被开源压低，利润集中在验证、工具、support、subsystem IP |

判断：RISC-V 的关键不是替代 x86/Arm server CPU，而是在 chiplet/edge AI/控制核/安全核/定制 accelerator 里成为默认可选项。

### 6. SDV/mission-critical edge AI/security certification

成熟与量产路线：

| 口径 | 2026-2027 路线 | 爆发力度 |
|---|---|---:|
| 基准 | Zonal/domain controller、OTA、middleware、安全更新、ASIL/ISO 认证继续推进 | 汽车半导体 **+6%-10%/年**，SDV software/compute 平台 **+25%-35%/年** |
| 乐观 | ADAS/座舱/车控融合，AI accelerator 进入更多车型，高性能 central compute ASP 上升 | 车载 compute/AI SoC **+20%-35%/年**，传统 MCU 仍低个位数 |
| 超预期乐观 | L3/L4 功能商业化、法规推动安全更新和 PQC migration，整车 E/E 架构快速切换 | SDV 平台收入高增，但利润在半导体/中间件/云服务之间重新分配 |

判断：车载不是所有芯片都会好。高性能 ADAS/central compute/security middleware 好，传统 MCU/analog 仍可能被库存和价格压制。

## 当前市场规模、未来一年增速和利润率预测

说明：不同机构对 2026 半导体市场口径差异极大。WSTS Autumn 2025 预测 2026 全球半导体 **$975.46B**, +26.3%；Gartner 2026-04 预测 2026 全球半导体 **$1,320.2B**, +64%，其中 memory **$633.3B**，non-memory **$686.9B**。下表采用“可投资口径”，把 DATE 2026 的技术方向映射到可交易市场；2027 为“未来一年”预测。

| 产品/技术 | 当前市场规模，美元 | 当前利润率 | 2027 基准 | 2027 乐观 | 2027 超预期乐观 |
|---|---:|---:|---:|---:|---:|
| 全球半导体总盘 | WSTS 2026E **$975.5B**；Gartner 2026E **$1.320T** | 行业分化：AI/先进制造高，legacy 低 | **+15%-22%**，memory 增速放缓但仍高 | **+25%-35%**，AI infra 继续拉动 | **+40%+**，memory inflation 延续且 AI capex 不降 |
| AI semiconductors/accelerator stack | Gartner 称 AI semis 约占 2026 半导体 **30%**，即约 **$396B**；NVIDIA FY2026 revenue **$215.9B**，Q4 data center **$62.3B** | NVIDIA FY2026 non-GAAP gross margin **71.3%**，Q4 **75.2%**；custom ASIC 估计 45%-65% gross | 收入 **+20%-30%**；gross margin 65%-72% | **+35%-45%**；高端 GPU/HBM 仍紧，gross margin 70%-76% | **+55%-70%**；rack-scale/inference 放量，gross margin 72%-78% |
| HBM/advanced memory | Gartner memory 2026E **$633.3B**；TrendForce 称 2026 HBM shipment >**30B Gb**，HBM4 premium **>30%**，HBM4 在 2026H2 超过 HBM3e 成主流；HBM TAM 有望 2028 到 **$100B** 级 | HBM/DRAM 周期上行，估计 gross margin 45%-65%，龙头更高 | HBM 收入 **+25%-40%**；margin 维持高位 | **+50%-70%**；HBM4 供不应求，margin +5pp | **+80%+**；custom ASIC 加单，HBM 继续 sold-out |
| Advanced packaging/chiplet/2.5D/3D | Yole 口径 advanced packaging 2024 **$46B**、2030 **$79.4B**；GVR 2024 **$39.6B**、2030 **$55B**；data-center AI chip advanced packaging 2024 **$5.6B** 到 2030 **$53.1B** | TSMC 1Q26 gross margin **66.2%**、operating margin **58.1%**；OSAT gross margin 常见 15%-25% | 整体 **+15%-25%**，AI high-end **+40%-60%**；margin +1-3pp | 整体 **+25%-35%**，AI high-end **+70%**；紧缺定价 | capacity +80% 仍不够，AI high-end **+100%**；先进封装成为 AI 交付瓶颈 |
| EDA + semiconductor IP + services | SEMI EDMD Q4 2025 **$5.466B**, +10.3%；SIP Q4 **$2.083B**, +18.3%；2025 年化估计 **$21B-$22B** | Cadence FY2025 non-GAAP operating margin **44.6%**，2026 guide **44.75%-45.75%**；Synopsys FY2025 revenue **$7.054B** | 收入 **+10%-12%**；margin 稳中 +0-1pp | **+15%-18%**；AI add-on 和 IP 拉动，margin +1-2pp | **+22%-28%**；agentic flow 高 ASP，margin +2-4pp |
| Agentic EDA 子方向 | 仍嵌在 EDA 市场，2026 可计费新增 TAM 估计 **$1B-$3B** | 软件毛利高，但推理/数据/R&D 抵消部分，operating margin 20%-45% | **+30%-50%**，验证/test 最先落地 | **+60%-90%**，physical/security 闭环落地 | **+100%+**，成熟节点/FPGA/accelerator flow 批量采用 |
| RISC-V/open silicon | 口径差异大：RISC-V cores/IP 2026 约 **$0.7B-$1.65B**；广义 RISC-V market 2025 **$2.3B**、2030 **$8.57B**；SHD/RISC-V 提示 2025 shipment 约 **3B units**、2031 penetration **33.7%** | IP gross margin 可 70%-90%；open-source support/services operating margin 10%-30% | 收入 **+25%-35%**，shipment 快于 revenue | **+40%-60%**，edge AI/automotive/sovereignty 拉动 | **+70%+**，但 ASP 下行，利润转向 subsystem IP/验证/support |
| Silicon photonics/CPO | Silicon photonics 2025 约 **$2.6B-$2.8B**；CPO 2026 约 **$0.16B**，2031 **$0.75B** 口径；部分机构给出更高口径 | Optical module gross margin 20%-35%；CPO 早期良率/服务性拖累 | SiPh **+25%-35%**；CPO **+40%-70%** | SiPh **+40%-55%**；CPO **+80%-120%** | CPO 平台化，收入从小基数数倍增长，margin 2028 后改善 |
| Automotive semiconductor + SDV | Auto semiconductor 2025 约 **$53.6B**；SDV 市场 2026 口径约 **$171.9B-$390.3B**，取决于是否含整车软件/服务 | Auto semis gross margin 35%-55%；SDV 软件/中间件 20%-40%，OEM 系统利润较低 | Auto semis **+6%-10%**；SDV **+25%-35%** | 高性能 ADAS/central compute **+20%-35%**；legacy MCU 低增长 | L3/L4/监管/PQC 推动 SDV 平台 **+45%+** |
| Hardware security verification/PQC for chips | 嵌在 EDA/security/IP/IoT，2026 可计费 TAM 估计 **$3B-$6B** | 工具/IP 毛利高，服务低；operating margin 15%-40% | **+15%-25%** | **+30%-45%**，AI accelerator/SDV 采购拉动 | **+60%+**，若安全认证进入强制 signoff |

## 关键市场数据来源与交叉验证

- WSTS Autumn 2025：2025 全球半导体 **$772.243B**, +22.5%；2026 **$975.460B**, +26.3%；2026 logic **$390.863B**, memory **$294.821B**。来源：[WSTS Forecast Release PDF](https://www.wsts.org/esraCMS/extension/media/f/WST/7310/WSTS_FC-Release-2025_11.pdf)。
- Gartner 2026-04：2026 半导体 **$1.3202T**, +64%；2027 **$1.5545T**；2026 memory **$633.3B**；AI semis 约占 2026 半导体 **30%**；DRAM/NAND 年度价格 2026 分别 **+125%/+234%**，价格缓解预计不早于 2027 晚些时候。来源：[Gartner press release](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)。
- SEMI ESD Alliance：Q4 2025 ESD revenue **$5.4663B**, +10.3%；SIP **$2.0832B**, +18.3%；CAE **$1.8874B**, +9.4%；全球雇员 **71,517**，+13.8%。来源：[SEMI EDMD Q4 2025](https://www.semi.org/en/semi-press-release/esd-alliance-reports-electronic-system-design-industry-posts-5.5-billion-dollars-in-revenue-in-q4-2025)。
- Cadence FY2025：revenue **$5.297B**, +14%；non-GAAP operating margin **44.6%**；2026 revenue guide **$5.9B-$6.0B**，non-GAAP operating margin **44.75%-45.75%**；IP business +25%，包含 HBM/UCIe/PCIe/DDR/SerDes。来源：[Cadence FY2025 results](https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Fourth-Quarter-and-Fiscal-Year-2025-Financial-Results/default.aspx)。
- Synopsys FY2025：revenue **$7.054B**, +15%；FY2026 midpoint revenue **$9.610B**，包含 Ansys revenue **$2.9B**。来源：[Synopsys FY2025 results](https://investor.synopsys.com/news/news-details/2025/Synopsys-Posts-Financial-Results-for-Fourth-Quarter-and-Fiscal-Year-2025/default.aspx)。
- NVIDIA FY2026：revenue **$215.9B**，Q4 data center revenue **$62.3B**，FY2026 non-GAAP gross margin **71.3%**，Q4 non-GAAP gross margin **75.2%**。来源：[NVIDIA FY2026 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)。
- TSMC 1Q26：net revenue **$35.90B**，gross margin **66.2%**，2Q26 guide gross margin **65.5%-67.5%**；2025 annual revenue **$122.42B**，net income **$55.21B**，gross margin **59.9%**。来源：[TSMC Q1 2026 results](https://investor.tsmc.com/english/quarterly-results/2026/q1)、[TSMC 2025 Annual Report](https://investor.tsmc.com/static/annualReports/2025/english/index.html)。
- Advanced packaging：Yole 口径 2024 advanced packaging **$46B**、2030 **$79.4B**、2024-2030 CAGR **9.5%**；Grand View 口径 2024 **$39.60B**、2030 **$55.00B**、2025-2030 CAGR **5.7%**。来源：[Yole via Edge AI and Vision Alliance](https://www.edge-ai-vision.com/2025/09/advanced-packaging-market-set-to-reach-79-4-billion-by-2030/)、[Grand View Research](https://www.grandviewresearch.com/industry-analysis/advanced-packaging-market-report)。
- HBM：TrendForce 称 2026 HBM total shipments >**30B Gb**，HBM4 premium **>30%**，SK hynix 预计保持 **>50%** share，HBM4 在 2026H2 超过 HBM3e 成主流。来源：[TrendForce HBM4 note](https://www.trendforce.com/presscenter/news/20250522-12589.html)。
- RISC-V：RISC-V Annual Report 2025 引用 SHD Group，penetration 从 2021 **2.5%** 到 2031 **33.7%**；公开市场报告口径显示 2026 RISC-V core/IP 市场约 **$0.7B-$1.65B**，广义 RISC-V market 2025 **$2.3B** 到 2030 **$8.57B**。来源：[RISC-V Annual Report 2025](https://riscv.org/wp-content/uploads/2026/01/RISC-V-Annual-Report-2025.pdf)、[SHD Group market reports](https://theshdgroup.com/market-reports/)。
- Silicon photonics/CPO：silicon photonics 2025 约 **$2.62B-$2.8B**，CAGR 约 **25%-30%**；CPO 2026 约 **$0.16B** 到 2031 **$0.75B**，CAGR **35.92%**。来源：[GMI silicon photonics](https://www.gminsights.com/industry-analysis/silicon-photonics-market)、[Mordor via GlobeNewswire CPO](https://www.globenewswire.com/news-release/2026/01/29/3228606/0/en/co-packaged-optics-market-growing-at-35-92-cagr-to-reach-usd-0-75-billion-by-2031-reports-mordor-intelligence.html)。
- Automotive/SDV：automotive semiconductor 2025 约 **$53.63B**，2035 **$117.95B**；SDV 2026 市场口径 **$171.92B** 到 **$390.29B**，取决于定义。来源：[Fundamental Business Insights automotive semiconductor](https://www.fundamentalbusinessinsights.com/industry-report/automotive-semiconductor-market-4907)、[Coherent Market Insights SDV](https://www.coherentmarketinsights.com/industry-reports/software-defined-vehicle-market)、[Fortune Business Insights SDV](https://www.fortunebusinessinsights.com/software-defined-vehicle-market-111596)。

## 与当前市场可能相违背的重要洞见

### 洞见 1：2026 半导体大牛市可能不是“全面复苏”，而是 AI 和 memory inflation 对非 AI 的挤压

WSTS 仍给 2026 **$975B**，Gartner 已经给到 **$1.32T**，差距超过 **$340B**。这个差异本身就是信号：市场可能不是稳定成长，而是被 memory price shock 和 AI infrastructure capex 突然拉伸。Gartner 明确提示 memory inflation 会 destroy or delay non-AI demand into 2028。也就是说，半导体总收入暴涨可能同时伴随 PC、消费、部分车规/工业客户的 BOM 压力和需求推迟。

投资含义：买“半导体 beta”不如买 AI stack 的瓶颈项：HBM、advanced packaging、D2D IP、EDA verification、networking/optical、power/thermal。

### 洞见 2：Chiplet marketplace 的兑现会慢于市场想象，但 chiplet 基础设施会快于市场想象

DATE FS04 已经把 open chiplet marketplace 的难点列清楚：接口标准、仿真、安全、热、封装。多厂商 chiplet 交易平台要解决责任边界：谁担保 KGD，谁为 D2D PHY timing 负责，谁做 side-channel/security signoff，谁承担 package thermal failure。

投资含义：短期更确定的是 closed chiplet 和同生态 chiplet 的基础设施收入。通用 marketplace 是 2028+ 选项，2026-2027 的钱在 TSMC/OSAT capacity、UCIe/PCIe/SerDes/HBM IP、package-aware EDA、test/inspection、thermal material 和 substrate。

### 洞见 3：Agentic EDA 最大价值不是减少 headcount，而是缩短不可控迭代

硬件设计里最贵的不是写一段 RTL，而是跨工具、跨阶段、跨团队迭代无法收敛。DATE 2026 的 Agentic EDA 论文都绕着“反馈回路”走：HLS reports、coverage feedback、ATPG settings、physical design data generation、RAG security verification。真正商业化的 agent 是能读取工具输出、决定下一步约束、并保留可审计记录的系统。

投资含义：验证和实现闭环的 AI 功能会比自然语言 RTL 生成更早被大客户付费。商业 EDA 龙头不会被 AI 颠覆，反而最可能把 proprietary data/tool API 转化为 AI 时代壁垒。

### 洞见 4：Open-source EDA 会先做大成熟节点和人才池，不会马上压垮高端商业 EDA

DATE 的 open-source 材料强调 IHP 130nm SiGe BiCMOS open PDK、mixed-signal case studies、TinyTapeout、Bambu/SODA/OpenROAD。这些场景对先进节点 signoff 的替代性有限，但对教育、研究、SME、工业/IoT/edge 定制非常重要。

投资含义：open-source silicon 是“扩大设计人口”的力量。它压低入门成本，但当项目走向先进节点、高速 SerDes、HBM/UCIe、车规认证、mixed-signal signoff 时，商业 IP/EDA 仍会捕获高毛利。

### 洞见 5：Silicon photonics 短期不是 AI compute 替代，而是 AI network/power/thermal 的配套升级

DATE photonic AI tutorial 的重点不是“光矩阵乘法多快”，而是 microring/phase shifter/laser 热漂移、自热、inter-chiplet thermal coupling、diamond/graphene heat dissipation。这说明产业真正焦虑的是可靠性和封装集成。

投资含义：短期赢家更可能在 optical interconnect、CPO/LPO、driver/TIA、laser、thermal simulation、advanced substrate，而不是纯光计算芯片。

### 洞见 6：硬件安全会从“成本中心”变成“AI/SDV 交付门槛”

AI accelerator、SDV、industrial IoT 的安全问题不是软件补丁可以完全修复的。DATE 2026 多个 session 把 pre-silicon security validation、side-channel、PQC、security RAG assistant 放在核心位置，说明客户会把硬件安全纳入 signoff checklist。

投资含义：security verification、PQC IP、side-channel analysis、hardware-firmware co-verification、runtime safety sensors 可能成为 EDA/IP 新增预算项。

## 投资/产业链优先级

### 最高确定性：HBM + advanced packaging + AI accelerator supply chain

确定性来自三个事实：AI semis 占 2026 半导体约 30%，memory revenue 可能三倍增长，DATE 技术议程也集中在 memory topology、3D integration、thermal/power integrity。这里的核心不是“需求很强”，而是“系统架构被迫依赖这些瓶颈项”。

优先级：HBM/HBM4、CoWoS/SoIC/2.5D substrate、D2D PHY/IP、UCIe/PCIe/SerDes、package-aware EDA、thermal materials、test/inspection、AI server networking。

### 高确定性且被低估：EDA/IP 的 AI 化和 package-aware 化

市场容易把 EDA 当作半导体 capex 的小配角，但 SEMI EDMD Q4 2025 已经是 **$5.466B** 单季收入，SIP 单季 **$2.083B** 且 +18.3%。Cadence FY2025 non-GAAP operating margin **44.6%**，说明这是高质量收入。DATE 2026 又把 EDA 的增量从传统工具扩展到 agentic flows、chiplet simulation、photonic/thermal/multiphysics、security verification。

优先级：Cadence/Synopsys/Siemens EDA 生态，verification/coverage、HLS/DSE、package-aware signoff、IP blocks such as HBM/UCIe/PCIe/SerDes/DDR、on-prem LLM/SLM for secure EDA。

### 中高弹性：silicon photonics/CPO

CPO 当前绝对规模小，但 AI rack-scale 网络功耗和带宽会让它具备很高弹性。风险在于 serviceability、标准、热、良率和 hyperscaler adoption timing。DATE 2026 对 thermal robust photonic AI 的重视说明，产业还在补工程化短板。

优先级：1.6T/3.2T optical module、LPO/CPO、silicon photonics foundry、laser、driver/TIA、optical packaging、physics-informed photonics EDA。

### 长周期战略：RISC-V/open silicon

RISC-V 出货渗透可能快，但收入和利润未必同步，因为 open standard/open-source 会压低 CPU core ASP。真正赚钱的是 subsystem IP、verification、security、software ecosystem、support、domain-specific accelerator templates。

优先级：edge AI/IoT/automotive control cores、open PDK services、mature-node ASIC platform、RISC-V vector/DSP/AI extensions、software toolchain、certification。

## 结论

DATE 2026 给出的最重要更新是：AI 时代芯片行业的瓶颈正在从“算力芯片本身”扩散为一个更复杂的系统约束组合：HBM/3D memory、advanced packaging、chiplet interconnect、package-aware EDA、agentic verification、photonic interconnect、hardware security、SDV/edge certification。

未来一年最强的收入爆发会出现在 **AI accelerator + HBM + advanced packaging**；利润质量最高、波动更小的是 **EDA/IP/verification**；弹性最大但时点不确定的是 **CPO/silicon photonics**；战略价值高但商业化碎片化的是 **RISC-V/open-source silicon**。

一句话判断：市场还在用“GPU 供不应求”的框架给 AI 半导体定价，但 DATE 2026 显示，下一阶段的超额收益会更多来自 **谁能解除 AI 系统级瓶颈**，而不只是“谁能做一颗更大的芯片”。
# DesignCon 2026：AI 数据中心把电子设计推入 224G 部署、448G 探路和 1.6T 互连时代

> 调研范围：截至 2026-05-08 可检索的 DesignCon 2026 官方议程、获奖论文、展商发布、媒体会后报道、公司新闻稿及少量非官方讨论。未参考本地项目内既有文件或信息。DesignCon 2026 于 2026-02-24 至 2026-02-26 在 Santa Clara Convention Center 举行。

## 0. 核心结论

DesignCon 2026 的最大变化是：它已经从“高速板级 SI/PI 工程会议”转成“AI 数据中心物理层系统大会”。会场不再只讨论 PCB 上一条差分线怎么跑，而是在讨论从 die、interposer、package、top-side connector、copper flyover、optical module、switch ASIC、rack power、liquid cooling 到 agentic EDA 的整条链路。

最强信号有 7 个：

1. **224G 已从验证进入部署，448G 已从概念进入工程探路。** Samtec、Luxshare、Molex/Arista、Marvell、Keysight 等都围绕 224G/448G 做展台演示或技术论文；Best Paper 里直接出现“448Gbps scale-up/scale-out”“448Gbps via/fan-out”“400G PAM6 SerDes”等主题。
2. **PCIe 7.0 是 2026 验证主战场，PCIe 8.0 已开始 256 GT/s pathfinding。** Keysight/Teledyne/Anritsu/Synopsys 聚焦 PCIe 7.0 128 GT/s 测量，Marvell 和 Synopsys展示 PCIe 8.0-class 256 GT/s 电气性能。Marvell 明确称 PCIe 8.0 预计 2028 完成，x16 可达 1 TB/s 双向带宽。
3. **铜没有死，但铜的形态变了。** 传统长 PCB 走线继续被压缩，机会转向 co-packaged copper、near-ASIC copper、top-side interconnect、active copper cable、active electrical cable、retimer/redriver。Luxshare 展示 448G KOOLIO CPC-to-OSFP Airchannel 链路，支持超过 90 GHz 带宽；1.6T OSFP AEC 可在 27AWG 4 米、30AWG 3 米稳定工作；OSFP-XD PCIe 6.0 AEC 配 Marvell Alaska P retimer 可到 7 米、PCIe 6 x16、256 GB/s。
4. **光互连进入 1.6T 量产前夜，但 CPO/OIO 不是立刻替代 pluggable。** 2026 年 800G+ 光模块成为 AI 数据中心标准件，1.6T 从小基数进入大规模爬坡；但会场同时强调 LPO、AEC/ACC、CPC、CPO/OIO 并存，短距铜和中远距光会分层。
5. **AI 网络瓶颈从“有没有 GPU”外溢到“数据如何移动、供电如何送达、热如何拿走”。** ConnectorSupplier 会后报道提到 AI 机柜功耗继续上行，单个下一代 Rubin Ultra/Kyber rack 预期约 600 kW，2030 年前 1 MW rack 被专家视为可能情景。这直接把 power integrity、busbar、liquid cooling、leak detection、cold plate、high-current connector 拉成 DesignCon 主角。
6. **Agentic AI 从展会话题变成设计工具路线。** 2025 年还是早期讨论，2026 年已经有 keynote、panel 和“Multi-Agent AI Systems for Autonomous Signal Integrity Analysis of PCB & Package Designs”技术论文。短期不是替代工程师，而是压缩 SI/PI 建模、仿真设置、debug、测试脚本和跨工具联动时间。
7. **中国/亚洲供应链在高端互连论文与展台上的存在感显著上升。** Best Paper 里 Alibaba Group/Alibaba Cloud/Synopsys/Shennan Circuit/New H3C 的 PCIe 7.0 PCB 技术论文获奖，Alibaba/Luxshare/Synopsys 的 top-side interconnect 论文获奖；Luxshare、FIT、BizLink 等在展商和 sponsor 里位置靠前。

## 1. 公开材料地图：会场规模、议题和一手信号

### 1.1 会场事实

- 官方页面称 DesignCon 2026 有 **100+ sessions、15 tracks**，覆盖 signal integrity、power integrity、high-speed link design、machine learning。
- ConnectorSupplier 会后报道给出更细数字：2026 年为第 26 届，会议有 **183 篇 technical papers、3 场 keynote、tutorials、boot camps、poster reviews**，技术论文和 panels 分布在 **15 个深度技术 track**；展商从 2025 年 **173 家增至 2026 年 202 家**，增幅约 **16.8%**；其中 **40+ 家**供应 copper/fiber connectors 和 cable assemblies。
- 赞助结构本身就是行业热度表：Host 是 Amphenol；Diamond 为 Keysight、Molex、Samtec；Platinum 为 Cadence、Luxshare、Rohde & Schwarz、TE Connectivity、Tektronix；Gold 包括 Anritsu、Bellwether、BizLink、FIT、Hirose、Synopsys、Teledyne LeCroy。

### 1.2 Keynotes：三条主线

- Purdue Joseph Lukens：“From Spooky Action at a Distance to the Quantum Internet”，对应长期通信/网络物理极限。
- Agentrys Mark Ren：“Agentic AI for Chip Design”，对应 EDA 工作流自动化。
- NASA Goddard Bhanu Sood：“Designing for Discovery”，对应高可靠 mission-critical system design。

这三个 keynote 拼起来的含义是：DesignCon 的技术半径已经从单板信号完整性，扩展到“下一代计算系统如何被设计、验证、供电、散热、互连和长期可靠运行”。

### 1.3 2026 Best Paper：获奖题目透露的重点

2026 Best Paper 获奖题目高度集中在 AI data center channel、PCIe 7.0、448G、PAM6、EMI 和 top-side interconnect：

- 400G Channels for AI Applications: Passive & Active Copper Cable Assemblies to Enable Scale Up/Scale Out，作者来自 TE Connectivity 和 Semtech。
- 448Gbps: Challenges for Scale-Up & Scale Out Applications，作者来自 Meta、Arista Networks、Molex。
- Analytical Derivation of P/N Skews in Coupled Channels: Impact on 400G PAM6 SerDes，作者来自 Cisco。
- Breakthroughs in PCB Technology for PCIe 7.0 Interconnects，作者来自 Alibaba Group、Alibaba Cloud、Synopsys、Shennan Circuit、New H3C。
- Targeted EMI Mitigation Using Emission Source Imaging & 3D-Printed Absorbers，作者来自 Missouri S&T、Molex、HPE、Juniper。
- Top Side Interconnect Enabling for PCIe 7.0 & Beyond，作者来自 Alibaba Group、IEEE、Synopsys、Luxshare。
- Via & Fan-Out Designs for 448Gbps: SI vs Technology，作者 Mike Tucker，Shennan Circuits。

关键词不是“单一速度升级”，而是 **channel architecture 重构**：skew、via/fan-out、PCB材料、top-side connector、copper cable、PAM6/FEC/measurement、EMI mitigation 全部在同一张图里。

## 2. 重点方向和相对过去的转折

### 2.1 从 112G/800G 过渡到 224G/1.6T，448G 被提前拉进工程视野

过去两年行业主线是 112G PAM4、400G/800G 光模块、PCIe 5/6、CXL 早期生态。DesignCon 2026 的主线变成：

- **112G**：成熟量产，仍是很多 active optics、LPO、DDR/高速测试和 legacy AI fabric 的基础。
- **224G**：进入部署和生态互操作阶段。Samtec 展示 Si-Fly HD CPC 224G；Synopsys 224G PHY 与 Hirose、Luxshare、Samtec 平台互操作；Luxshare 展示 224G CPC-to-CPC cable。
- **448G**：不再只是 roadmap。Samtec 展示 BE130 test assembly 跑 448G differential signals；Luxshare 展示 448G KOOLIO CPC-to-OSFP Airchannel，带宽超过 90 GHz；Molex/Arista 的 224G/448G skew management 论文入围 Best Paper；Shennan 的 448G via/fan-out 论文获奖。
- **1.6T**：光模块和电互连系统开始进入量产前夜。Keysight 展示 1.6T interconnect benchmark；Luxshare 展示 1.6T OSFP AEC/ACC；Anritsu 做 224/448G electrical/optical 到 145 GHz 以上测试。

结论：AI cluster 的 scale-up/scale-out 需求让 lane-rate 路线被明显前置。2026 年不再是“800G 刚起来，1.6T 慢慢看”，而是 800G 成为标配、1.6T 进入部署、448G/3.2T 的测试和材料问题提前暴露。

### 2.2 PCIe 7.0/8.0：标准周期还长，但资本开支已经在买 pathfinding

Keysight 展示 PCIe 7.0 PHY/protocol validation，使用 UXR oscilloscope、M8050A BERT、PCIe test software。Teledyne LeCroy 展示 live PCIe 7.0 transmitter measurements，用 65 GHz 12-bit oscilloscope 和 Anritsu MP1900A BERT 测 Synopsys PCIe 7.0 device operating at 128 GT/s。Anritsu 展示 PCIe 7.0 over optics，SiPhx 800G LPO module，64 Gbaud PAM4，128 GT/s TDECQ。

更重要的是 PCIe 8.0 已提前进入展示：

- Marvell 展示 PCIe 8.0 SerDes at **256 GT/s**，并称 PCIe 8.0 预计 **2028** 完成，x16 可达 **1 TB/s bidirectional bandwidth**。
- Synopsys 展示 PCIe 8.0-class **256 GT/s electrical performance**，包括 eye diagram 和 receiver performance。

这意味着短期收入不一定来自 PCIe 8.0 终端设备，而来自更早环节：SerDes IP、PHY IP、retimer/redriver、connector、test fixture、BERT、oscilloscope、VNA、channel modeling、compliance software。DesignCon 上“工程探路”的钱比标准完成早 18-30 个月花出去。

### 2.3 Copper vs optics：不是二选一，而是距离、功耗、延迟和可维护性的分层

市场常见叙事是“光会替代铜”。DesignCon 2026 给出的更细结论是：**长距和跨 rack 的确定性向光迁移，短距和 near-ASIC 的确定性向更高级铜迁移。**

- Copper 的新位置：CPC、top-side connector、flyover cable、AEC/ACC、retimerized OSFP-XD、near-chip cable。
- Optics 的新位置：800G/1.6T pluggable、LPO、CPO/OIO、OCS、coherent ZR/ZR+、scale-across DCI。
- 两者的共同瓶颈：BER、FEC latency、equalization power、thermal density、mechanical tolerances、manufacturing metrology。

Luxshare 的 7 米 PCIe 6/CXL OSFP-XD AEC 和 448G CPC-to-OSFP 演示，是“铜还没死”的强信号；TrendForce 的 800G+ 模块 2026 年出货占比超过 60%，是“光进入 AI 标配”的强信号。这两个信号不冲突。

### 2.4 PCB 不再只是成本件：材料、via、fan-out、top-side 成为系统性能变量

2026 Best Paper 把 PCB 推到中心位置：

- Alibaba/Alibaba Cloud/Synopsys/Shennan/New H3C 的 PCIe 7.0 PCB breakthrough 获奖。
- Alibaba/Synopsys/Luxshare 的 top-side interconnect for PCIe 7.0 & beyond 获奖。
- Shennan 的 448G via/fan-out 设计获奖。

这说明 AI 数据中心高端 PCB 的竞争点从层数、HDI、低损耗材料，继续推进到：

- connector footprint 和 mating interface 的 return loss/crosstalk 容差；
- via stub、backdrill、fan-out geometry；
- PCB 材料 Dk/Df 与铜粗糙度模型；
- top-side cable connector 绕开长板走线；
- 测量去嵌、S-parameter manipulation、statistical process control。

工程含义：高速 PCB/基板/连接器供应商的价值不再是“按平方米报价”，而是按 channel margin、yield 和系统架构自由度定价。

### 2.5 Power integrity 和 thermal 从配角变成限制条件

ConnectorSupplier 报道称，2026 会场大量展示 liquid-cooled bus bars、leak detection、plumbing hardware、cold plate cooling。其判断是：AI rack 的电力消耗继续上行，600 kW rack 与 1 MW rack 的讨论让传统供电/散热体系必须重构。

DesignCon 2026 的 power 相关议题包括：

- “Powering the Future: AI's Role in Next-Generation Power Integrity Solutions” panel；
- “AI-Driven Emulation of Power Supply Ripple via HSS Jitter Analysis & TIE-Based Source Isolation for PI-SI Co-Design”；
- advanced packaging 里的 distributed capacitor characterization；
- package 内 embedded silicon capacitor、stackable POL converter、busbar/cooling integration。

结论：GPU/ASIC 的性能竞争会外溢到电源完整性、机柜电力分配、散热部件、冷却液监测和结构件。未来一年这些“非芯片”环节可能出现比传统半导体更高的订单弹性。

### 2.6 Agentic AI：短期价值不是“替代设计师”，而是让 SI/PI debug 变成半自动闭环

DesignCon 2026 的 AI 设计方向不是泛泛的 chat assistant，而是具体落在：

- multi-agent SI analysis for PCB/package；
- natural-language to HFSS simulation；
- AI-assisted RF/microwave design automation；
- AI-driven transient thermal solver for 3DIC；
- PI-SI co-design 的 source isolation 和 jitter analysis；
- Synopsys/Cadence/Ansys/MathWorks/Intel/Simberian/JITX 等工具生态。

可落地路径大概率是：

1. 2026：自动生成仿真 setup、rule checking、fixture/de-embedding 流程、报告摘要。
2. 2027：对 via/fan-out、equalization、PDN decap、thermal boundary condition 做 design-space exploration。
3. 2028 以后：在受限设计域内形成闭环优化，但 sign-off 和 failure analysis 仍由工程师负责。

## 3. 会爆发的产品和技术方向：成熟与量产路线

### 3.1 三情景路线表

| 产品/技术 | 基准路线 | 乐观路线 | 超预期乐观路线 |
|---|---|---|---|
| 224G copper/optical channel | 2026 年成为 AI switch、NIC、cable、CPC 的部署主线；112G 继续存量 | 2026H2 大型 hyperscaler 新 rack 默认 224G；224G AEC/ACC 供应紧张 | 224G 生命周期被压缩，2027H1 开始被 448G pilot 挤压高端新增设计 |
| 448G differential channel | 2026 年 pathfinding，2027 年小批量 design-in，2028 年较广泛部署 | 2027H1 在 scale-up/near-ASIC 短距铜链路出现低量部署 | 2026H2 某些 proprietary AI fabric 先采用 448G short-reach，带动测试设备和连接器订单提前爆发 |
| 1.6T optical module / 1.6T electrical interface | 2026 年量产爬坡，2027 年成为高端 AI fabric 标配 | 800G 与 1.6T 并行，1.6T 端口 2026 年从小基数升至千万级 | 1.6T 被 Google/NVIDIA/ASIC cluster 同时拉动，2026 供不应求延续到 2027 |
| CPC / top-side interconnect / flyover copper | 2026 年作为缩短 PCB channel 的主流解决方案进入高端交换机和加速器系统 | 224G CPC 广泛部署，448G CPC 在 2027 年提前商业化 | 短距铜可靠性超预期，推迟部分 CPO 替代，CPC/AEC/ACC 毛利保持高位 |
| CPO / OIO / silicon photonics | 2026-2027 以 demo、switch linecard pilot、特定 hyperscaler 为主；pluggable 仍是收入主体 | 2027 年部分 AI switch 平台开始批量采用 | 若 power/latency 压力过大，CPO/OIO 从“下一代”变成“本代 late-cycle upgrade” |
| PCIe 7.0 | 2026 年 validation/compliance/test 主战场，端设备逐步跟进 | PCIe 7 PHY/retimer 2026H2 design win 加速 | PCIe 7 在 AI rack 内部连接比传统服务器更快放量 |
| PCIe 8.0 256 GT/s | 2026-2027 为 IP、SerDes、connector、test pathfinding；标准预计 2028 | 2027 年 hyperscaler pre-standard prototype | 专有协议先采用 PCIe 8.0-class electrical，带动 256 GT/s 测试和 IP 收入提前 |
| UALink / Scale-up Ethernet | 2026 年生态验证，2027 年随非 NVIDIA AI rack 进入商业化 | 大型 ASIC/GPU 替代平台采用 UALink，形成多供应商生态 | UALink 成为 AI scale-up 的事实开放标准之一，迫使 retimer、switch、EDA 生态提前扩张 |
| Agentic EDA / autonomous SI | 2026 年工具辅助，2027 年局部闭环 | 高速 channel setup/debug 时间下降 20-30% | 工具公司把 AI workflow 变成高 ASP 模块，EDA 增速显著高于半导体设计开支 |
| Liquid cooling / high-current power delivery | 100 kW+ rack 默认液冷，电源完整性和冷却部件随 AI rack 扩产 | 300-600 kW rack 加速，使 busbar、manifold、leak detection、冷板供不应求 | 600 kW-1 MW rack 路线提前，液冷和高压配电成为 AI capex 的硬瓶颈 |

### 3.2 爆发力度排序

按 2026-2027 订单弹性和确定性排序：

1. **800G+/1.6T optical transceivers 和 optical components**：确定性最高，市场已有明确收入口径。TrendForce 估计 AI 专用光收发模块市场从 2025 年 **165 亿美元**增至 2026 年 **260 亿美元**，同比 **57%+**；800G+ 模块出货占比从 2024 年 **19.5%**升至 2026 年 **60%+**。
2. **high-speed copper interconnect：CPC/AEC/ACC/top-side connector**：收入口径分散，但 DesignCon 信号最强。224G 进入部署，448G demo 密集，直接受益于 AI rack 内短距连接和 PCB 路径缩短。
3. **retimer/redriver/SerDes PHY/DSP/active cable chipset**：因为 PCIe 6/7、CXL、UALink、1.6T、AEC/ACC 同时需要。Marvell、Synopsys、MACOM、Astera、Broadcom、Semtech 等都在受益链条。
4. **high-end test & measurement**：65 GHz/145 GHz/250 GHz、BERT、VNA、AWG、sampling oscilloscope、de-embedding、IEEE 370、PCIe 7/8 software。每一次 lane-rate 翻倍都会先买仪器和仿真。
5. **advanced packaging / 2.5D / 3DIC / chiplets / UCIe**：长期空间最大，但受 CoWoS/EMIB/Foveros/hybrid bonding 产能、良率和客户集中度约束。
6. **liquid cooling / high-current power distribution**：爆发由 AI rack 功耗驱动，硬件价值量快速提升，但竞争者更多，利润率分化大。
7. **agentic EDA / SI automation**：收入弹性取决于工具公司能否把 AI workflow 包装成高价值 license，而不是免费功能。

## 4. 市场规模、增速和利润率预测

### 4.1 当前可引用市场规模

| 市场/产品口径 | 当前规模与事实 | 备注 |
|---|---:|---|
| 全球 electronic connector market | 2025 年 **991.646 亿美元**，同比 **+14.7%**；其中北美 **219.756 亿美元**、欧洲 **188.741 亿美元**、日本 **41.543 亿美元**、中国 **328.418 亿美元**、亚太 **178.827 亿美元**、ROW **34.361 亿美元** | Bishop & Associates 口径；2026 预测增速 **+11.5%**，隐含 2026 约 **1,105-1,110 亿美元** |
| AI optical transceiver market | 2025 年约 **165 亿美元**，2026 年约 **260 亿美元**，同比 **+57%+** | TrendForce 口径，专指 AI 高速光收发模块 |
| Optical components market | 2025 年接近 **250 亿美元**；datacom revenue **>180 亿美元**，coherent module revenue 近 **60 亿美元** | Cignal AI 口径，较 AI optical transceiver 更宽 |
| Data center AI networking | 2025 年接近 **200 亿美元** | 650 Group 口径，包含 Ethernet、InfiniBand、800G optical transceivers 等 |
| EDA market | 2025 年约 **190 亿美元** | Synopsys、Cadence、Siemens EDA 高集中度；AI/multiphysics 推高 ASP |
| Advanced packaging | 2026 年约 **490-550 亿美元**；其中 2.5D/3D packaging 从 2025 年 **111.5 亿美元**到 2026 年 **127.3 亿美元**，2031 年 **241.8 亿美元** | 先进封装宽口径与 2.5D/3D 窄口径差异大 |
| Semiconductor/electronics test & measurement | 2025 年约 **77.135 亿美元**，CAGR **5.4%** | 高速 SerDes/PCIe/optical T&M 子品类增速显著高于总体 |
| Data center liquid cooling | Dell'Oro manufacturer revenue 口径：2025 年接近 **30 亿美元**；Grand View 宽口径：2025 年 **66.5 亿美元**；AI data center liquid cooling 2026 年约 **37 亿美元** | 口径差异来自是否包含 solution、services、facility integration |
| 全球半导体 | 2025 年 **7,917 亿美元**，同比 **+25.6%**；2026 年 SIA 预期约 **1 万亿美元** | DesignCon 相关需求主要来自 AI logic、memory、networking、custom ASIC |

### 4.2 未来一年三情景预测：规模、增速、利润率

> “未来一年”按 2026 全年到 2027H1 的订单和收入 run-rate 判断。利润率为行业典型毛利率/经营利润率区间，因公司结构差异很大，重点看方向。

| 产品/技术 | 当前市场规模 | 当前利润率 | 基准情景 | 乐观情景 | 超预期乐观情景 |
|---|---:|---:|---|---|---|
| 800G+/1.6T optical transceiver | AI 模块 2025 **165 亿美元**；2026 预测 **260 亿美元** | 模块毛利 **25-40%**；激光/DSP/SiPho 上游 **45-65%** | 2026 同比 **+55-60%**，规模 **250-265 亿美元**；毛利 +1-3pct，供需偏紧 | 同比 **+70-85%**，规模 **280-305 亿美元**；优质供应商毛利 **40%+** | 同比 **+100%+**，规模 **330 亿美元+**；1.6T/OCS/Google TPU/NVIDIA 同时拉货，上游激光和 DSP 最紧 |
| Optical components broader market | 2025 接近 **250 亿美元** | 混合毛利 **30-50%** | 2026 **+25-35%**，规模 **310-340 亿美元** | **+40-50%**，规模 **350-375 亿美元** | **+60%+**，规模 **400 亿美元+**，coherent + datacom 同时供给紧张 |
| CPC/AEC/ACC/top-side/high-speed connector cable | 宽口径 connector 2025 **991.6 亿美元**；DesignCon 相关高速 datacom 子市场估计 **100-150 亿美元** | 高速连接器/线缆毛利 **35-50%**；普通连接器 **25-35%** | 子市场 **+20-25%**；224G 放量、448G 仍 pilot；毛利稳定或 +1-2pct | **+35-45%**；top-side/CPC 进入更多 AI rack；毛利 **40-50%**维持 | **+50-70%**；铜短距能力超预期，部分原本光化链路延后，CPC/AEC/ACC ASP 高位 |
| PCIe/CXL/UALink retimer/redriver/SerDes PHY/DSP | 窄 retimer/redriver 估计 **15-25 亿美元**；高速 connectivity silicon/IP 估计 **50-80 亿美元** | 半导体毛利 **55-75%**；IP 可 **80%+** | **+30-40%**；PCIe 6/7、CXL、AEC 同步拉动；毛利稳定 | **+50-70%**；UALink 和 PCIe 7 design win 加速；高端 retimer 缺货 | **+90%+**；PCIe 8.0-class pre-standard 设计和 1.6T active cable chipset 同时提前 |
| PCIe 7/8、448G、1.6T 高速 T&M | 半导体/电子 T&M 2025 **77.1 亿美元**；高速子集估计 **10-20 亿美元** | 仪器毛利 **60-68%**；软件/服务更高 | 总体 **+6-10%**，高速子集 **+15-20%**；毛利稳定 | 高速子集 **+25-35%**；65GHz/145GHz/250GHz 仪器和 BERT/AWG 升级 | 高速子集 **+40%+**；448G/PCIe8 pathfinding 预算前置，T&M 先于终端放量 |
| Advanced packaging / 2.5D / 3DIC / chiplets / UCIe | advanced packaging 2026 **490-550 亿美元**；2.5D/3D 2026 **127 亿美元** | foundry/OSAT gross **25-45%**；受良率和 capex 影响 | **+15-20%**；CoWoS/EMIB/Foveros 继续瓶颈；利润率持平 | **+25-35%**；HBM4/ASIC/HPC 多客户拉动；稀缺产能毛利上行 | **+45%+**；chiplet/UCIe 标准化超预期，AI ASIC 爆量；但良率风险同步上升 |
| EDA / AI-assisted SI/PI / multiphysics | 2025 EDA 约 **190 亿美元** | 软件毛利 **75-85%**；经营利润 **25-35%** | **+12-15%**；AI 功能提高续费和 seat value；利润率 +1-2pct | **+20-25%**；agentic workflow 成为付费模块；利润率 +3-4pct | **+30%+**；AI design automation 直接缩短 tapeout/channel debug 周期，被高端客户按价值付费 |
| Liquid cooling / power delivery / rack thermal | manufacturer revenue 2025 近 **30 亿美元**；宽口径 2025/26 **60-66 亿美元**；AI 专用 2026 **37 亿美元** | 冷板/系统 gross **20-35%**；高定制可 **35-40%** | **+25-35%**；100kW+ rack 液冷默认化；利润率略升后趋稳 | **+50-60%**；300-600kW rack 带动 busbar/manifold/leak detection | **+75%+**；600kW-1MW rack 节奏提前，供电/散热成为 AI capex 第一瓶颈 |

## 5. 重要产品的投资/产业链判断

### 5.1 光模块：确定性最高，但注意“赢家不只模块厂”

800G/1.6T 光模块是最明确的爆发市场。TrendForce 给出 2025 到 2026 **165 亿美元到 260 亿美元**的市场跃迁，且 800G+ 模块在 2026 年占比 **60%+**。这说明 2026 年不是“渗透率刚起步”，而是高端 AI 数据中心从 400G/800G 过渡到 800G+/1.6T 的标准化阶段。

但利润最大的未必是最终 module assembly。更值得跟踪：

- EML/SiPh/InP 激光与光引擎；
- DSP/CDR/retimer；
- 1.6T test equipment；
- LPO 的 host tuning 和 validation；
- 低功耗封装、thermal design、FAU/optical connector；
- coherent ZR/ZR+ for scale-across DCI。

### 5.2 铜互连：最容易被市场低估

会场上最强反共识是：**448G 时代铜没有退出，反而在短距、near-ASIC、top-side、CPC、AEC/ACC 中变得更战略。**

原因：

- 光电转换有功耗、成本、延迟和热管理代价；
- rack 内短距链路对 latency 和 serviceability 敏感；
- PCB 走线太长时，top-side/copper flyover 反而是最直接的 SI 解决方案；
- AEC/ACC 用 retimer/redriver 把铜从“被动器件”变成系统级产品。

Samtec、Luxshare、Molex、TE、Amphenol、FIT、BizLink、Hirose 等的机会不只是连接器 ASP 提升，而是从零件进入 reference architecture。

### 5.3 Retimer/SerDes/IP：PCIe 8.0 的收入会早于 PCIe 8.0 标准

Marvell 和 Synopsys 在 DesignCon 2026 展示 PCIe 8.0-class 256 GT/s，是典型的“pre-standard revenue signal”。即使 PCIe 8.0 标准预计 2028 完成，2026-2027 年仍会产生：

- SerDes IP 授权；
- test chip；
- channel modeling；
- connector 与 cable fixture；
- retimer/redriver roadmaps；
- hyperscaler prototype；
- compliance software。

所以不能只盯“PCIe 8.0 endpoint 什么时候量产”。更早的受益环节是 IP 和验证生态。

### 5.4 Advanced packaging：UCIe/3DIC 是长期大方向，但短期瓶颈是产能和良率

DesignCon 的 3D interconnect、advanced packaging、HBM、chiplet、interposer、thermal solver 议题增加，说明 chiplet/3DIC 已经进入系统设计主战场。Mordor 口径下 2.5D/3D packaging 2026 年 **127.3 亿美元**，2031 年 **241.8 亿美元**，CAGR **13.69%**；更宽的 advanced packaging 口径 2026 年约 **490-550 亿美元**。

短期瓶颈不在需求，而在：

- CoWoS/EMIB/Foveros/advanced substrate 产能；
- HBM 堆叠良率；
- interposer warpage/thermal stress；
- die-to-die test；
- UCIe 生态互操作和责任边界；
- system-level EDA flow。

### 5.5 T&M 和 EDA：卖铲子，但要看是否绑定新标准

Keysight、Teledyne LeCroy、Anritsu、Rohde & Schwarz 在会场最活跃。原因很简单：224G/448G/PCIe 7/8/1.6T 都不是“做出来就行”，而是需要：

- 65 GHz+ real-time oscilloscope；
- 145 GHz+ electrical/optical interface testing；
- 250 GHz extender；
- BERT/AWG/sampling oscilloscope；
- BER/FEC/link quality benchmark；
- de-embedding 和 S-parameter metrology；
- PCIe/USB/DDR/GDDR compliance software。

EDA 同理。真正有弹性的不是普通 license，而是把 AI、multiphysics、3DIC、SI/PI/thermal、system validation 绑定的新 flow。

## 6. 可能与当前市场叙事相违背的重要洞见

### 6.1 “光替代铜”过于粗糙

DesignCon 2026 的事实是：光和铜都在升级。800G+/1.6T 光模块会爆发，但 448G short-reach copper、CPC、top-side interconnect、AEC/ACC 也会爆发。短距低延迟场景里，铜可能比市场预期活得更久、更贵、更战略。

### 6.2 CPO/OIO 短期不会马上吃掉 pluggable 模块收入

CPO/OIO 是长期方向，但 2026-2027 年收入主体仍是 pluggable、LPO、AEC/ACC、CPC 和 retimerized electrical links。CPO 更像下一代 switch architecture 的系统工程，不是简单把 OSFP/QSFP 一夜替换。

### 6.3 448G 的难点不只是 SerDes，而是制造统计和机械公差

Molex/Arista 的 224G/448G skew management、Intel/TE/Synopsys 的 PCIe 7 crosstalk sensitivity、Shennan 的 via/fan-out 448G 论文说明，448G 的核心问题会从“能否仿真出眼图”变成“能否稳定量产出 channel margin”。这会提高 metrology、SPC、材料和制造控制的价值。

### 6.4 PCIe 8.0 还未标准化，但供应链不能等到 2028

PCIe 8.0 预计 2028 完成，听上去很远；但 256 GT/s SerDes、connector、fixture、oscilloscope、retimer 的研发周期要求 2026 年就开始投入。市场若只按标准发布日期估值，可能低估 IP、T&M、connector 的前置订单。

### 6.5 Agentic AI 的第一桶金在“工程流程压缩”，不是“AI 自动设计芯片”

短期最值钱的是把 SI/PI/thermal/debug 流程从大量手工设置变成可复用、可审计的半自动 workflow。能节省 20-30% debug cycle 的工具，对 hyperscaler 和 ASIC 团队的价值远高于普通代码助手。

### 6.6 高速 PCB/连接器/冷却件可能比部分芯片环节更紧

AI 计算芯片的供应固然重要，但 DesignCon 2026 显示 bottleneck 正在扩散到：

- high-speed connector/cable；
- advanced PCB and substrate；
- optical module and DSP；
- liquid cooling；
- power delivery；
- T&M capacity。

这些“物理层铲子”公司在订单弹性上可能跑赢传统半导体周期。

### 6.7 中国供应链在高端互连上不只是制造承接

Alibaba、Luxshare、Shennan、New H3C 出现在 Best Paper 和关键 session 中，说明中国供应链已经在 PCIe 7.0 PCB、top-side interconnect、448G fan-out、CPC 结构上做 engineering leadership，而不仅是后端制造。对高端 PCB、连接器、光模块、线缆、AI rack 供应链格局影响很大。

## 7. 需要持续跟踪的指标

### 7.1 800G/1.6T 光模块

- 800G+ 出货占比是否按 TrendForce 路线在 2026 到 **60%+**；
- 1.6T 端口是否从小基数进入千万级；
- Google Ironwood TPU、NVIDIA Rubin/GB300/后续平台实际拉货；
- EML/InP/SiPh、DSP、LPO 良率与供应；
- 800G/1.6T ASP 是否因竞争快速下滑。

### 7.2 Copper/CPC/AEC/ACC

- 224G CPC 是否进入主流 AI switch reference design；
- 448G copper demo 是否转为 2027 design win；
- OSFP-XD PCIe/CXL AEC 在 JBOG/JBOM/JBOX 架构中的采用；
- top-side interconnect 是否从定制方案变成平台化产品；
- high-speed connector 交期和毛利率。

### 7.3 PCIe/CXL/UALink/retimer

- PCIe 7.0 compliance ecosystem 成熟度；
- PCIe 8.0 256 GT/s pre-standard demo 是否增加；
- UALink 是否获得非 NVIDIA AI rack 的真实 design win；
- CXL memory pooling 是否从概念走向部署；
- retimer/redriver 在 AI rack 中的 attach rate。

### 7.4 Power/thermal

- 100 kW、300 kW、600 kW rack 的实际部署节奏；
- cold plate、manifold、CDU、leak detection、liquid-cooled busbar 供应商订单；
- 800VDC/HVDC 或高压机柜配电路线是否被 hyperscaler 批量采用；
- 每 rack cooling BOM，从 GB300/NVL72 级别向 Rubin 级别如何变化。

### 7.5 EDA/T&M

- AI-assisted SI/PI 是否从 demo 变成付费模块；
- Synopsys/Cadence/Siemens/Ansys/Keysight/MathWorks 是否形成闭环 flow；
- 65GHz+ scope、145GHz+ optical/electrical test、250GHz extender 的订单和交期；
- 448G/PCIe 8.0 test fixture 标准化进度。

## 8. 结论：DesignCon 2026 的投资含义

DesignCon 2026 给出的最大投资线索不是“AI 继续拉动半导体”这种宽泛结论，而是：**AI cluster 的瓶颈正在从 GPU die 扩散到整个物理层。**

未来一年最强的确定性在 800G/1.6T 光模块和 optical components；最容易被低估的是 224G/448G copper interconnect、CPC、AEC/ACC、top-side connector；最前置受益的是 SerDes IP、retimer、T&M 和 EDA；中长期空间最大但约束最多的是 advanced packaging/chiplets/UCIe；最可能突然变成硬瓶颈的是液冷和高功率配电。

一个高度压缩的判断：

- **2026 年收入最确定**：800G/1.6T 光模块、光器件、AEC/ACC、retimer、PCIe 7 测试。
- **2026 年订单弹性最大**：1.6T optical、224G/448G CPC/top-side copper、liquid cooling、high-end T&M。
- **2027 年开始兑现**：448G short-reach、PCIe 7 endpoints/retimers、UALink rack-scale、CPO/OIO pilot、agentic SI/PI workflow。
- **2028 年及以后兑现**：PCIe 8.0 标准化设备、3.2T/400G-per-lane、CPO/OIO 规模化、UCIe merchant chiplet ecosystem。

市场若继续只按“GPU/ASIC/HBM”给 AI 基建定价，会低估 DesignCon 2026 暴露出来的物理层短板：连接、测量、封装、供电、散热、自动化验证。这些环节正在从后端配套变成 AI 数据中心的核心 alpha 来源。

## 9. 主要公开来源

- [DesignCon 官方页面：100+ sessions、15 tracks、sponsor、venue 信息](https://www.designcon.com/en/home.html)
- [DesignCon 2026 Best Paper Awards and Engineer of the Year，GlobeNewswire, 2026-05-06](https://www.globenewswire.com/news-release/2026/05/06/3289177/0/en/DesignCon-Crowns-2026-Winners-for-Best-Paper-Awards-and-Engineer-of-the-Year.html)
- [ConnectorSupplier 会后报道：183 technical papers、202 exhibitors、224G/448G、PCIe 8.0、600kW rack](https://connectorsupplier.com/designcon-2026/)
- [Signal Integrity Journal 会后总结：AI-driven infrastructure、448G、1.6T、system-level design](https://www.signalintegrityjournal.com/articles/4262-designcon-2026-ai-driven-infrastructure-and-system-level-design)
- [Keysight DesignCon 2026 发布：PCIe 7、448G PAM4/PAM6/PAM8、1.6T、UALink](https://www.keysight.com/it/en/about/newsroom/news-releases/2026/0209-pr26-028-keysight-to-showcase-advanced-ai-data-center-and-high-speed-interconnect-validation-at-designcon-2026.html)
- [Samtec DesignCon 2026：448 Gbps、130 GHz、CPC/CPO、Si-Fly、BE130](https://blog.samtec.com/designcon-2026/)
- [Luxshare-Tech DesignCon 2026：224G/448G CPC、1.6T OSFP AEC/ACC、PCIe 6.0 OSFP-XD AEC](https://en.luxshare-tech.com/company/resources/news/designcon-2026-unveiling-224g-448g.html)
- [Marvell DesignCon 2026：PCIe 8.0 SerDes 256 GT/s、1 TB/s x16、2028 标准预期](https://www.streetinsider.com/Business%2BWire/Marvell%2Bto%2BShowcase%2BPCIe%2B8.0%2BSerDes%2BDemonstration%2Bat%2BDesignCon%2B2026/26047870.html)
- [Synopsys DesignCon 2026：PCIe 8.0-class 256 GT/s、224G PHY、PCIe 7.0 PHY partner demos](https://www.synopsys.com/events/designcon.html)
- [Anritsu DesignCon 2026：PCIe 7.0 over optics、SiPhx 800G LPO、64 Gbaud PAM4](https://www.anritsu.com/en-us/test-measurement/news/news-releases/2026/2026-02-20-us01)
- [Cadence DesignCon 2026：EM/electronic/thermal system analysis、HBM PHY、UALink IP](https://www.cadence.com/en_US/home/company/events/industry-events/designcon-2026.html)
- [DesignNews：5 Hot Topics at DesignCon 2026](https://www.designnews.com/electronics/five-hot-topics-at-designcon-2026)
- [Bishop & Associates World Connector Market Handbook 2026 sample：2025 connector market 991.646 亿美元、+14.7%](https://bishopinc.com/wp-content/uploads/2026/03/M-700-26-B.pdf)
- [Bishop Report news brief：2026 connector sales forecast +11.5%](https://bishopinc.com/wp-content/uploads/2026/02/nb-10-26.pdf)
- [Cignal AI：2025 optical components 接近 250 亿美元，datacom >180 亿美元](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)
- [TrendForce：2026 年 AI 光收发模块 260 亿美元、800G+ 出货占比 60%+](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- [650 Group：Data Center AI Networking 2025 接近 200 亿美元](https://650group.com/press-releases/data-center-ai-networking-to-surge-to-nearly-20b-in-2025-according-to-650-group/)
- [Grand View Research：semiconductor/electronics T&M 2025 77.135 亿美元](https://www.grandviewresearch.com/horizon/statistics/test-and-measurement-equipment-market/end-use/semiconductor-and-electronics/global)
- [Grand View Research：data center liquid cooling 2025 66.5 亿美元](https://www.grandviewresearch.com/industry-analysis/data-center-liquid-cooling-market-report)
- [Dell'Oro/PRNewswire：liquid cooling 2025 接近 30 亿美元，2029 接近 70 亿美元](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html)
- [Mordor Intelligence：2.5D/3D semiconductor packaging 2025-2031](https://www.mordorintelligence.com/industry-reports/global-25d-and-3d-semiconductor-packaging-market)
- [TMT IB Guide：EDA 2025 约 190 亿美元](https://ibinterviewquestions.com/guides/tmt-investment-banking/eda-ip-semiconductor-design-tools)
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
# ISSCC 2026：AI 算力系统化拐点、存储/互连/供电瓶颈与未来一年产品爆发路线

> 资料范围：截至 2026-05-08，整理 ISSCC 2026 官方 Advance Program/CFP、公开新闻与公开市场资料；未参考本项目内已有文件或内部信息。会议官方主题为 **“Advancing AI with IC & SoC Innovations”**，会期 2026-02-15 至 2026-02-19，地点为 San Francisco Marriott Marquis。  
> 关键外部资料：ISSCC 2026 官方 Advance Program、ISSCC 2026 CFP、Gartner 2026 半导体市场预测、TrendForce 光互连资料、IBM/imec 等公开论文新闻。文末列源。

## 一句话结论

ISSCC 2026 的最大变化不是“又多了几个 AI 加速器”，而是 **AI 算力从单芯片 FLOPS 竞争，转向系统级约束竞争**：HBM4/LPDDR6/GDDR7、UCIe/D2D、800G/1.6T 光互连、CPO、48V/近负载供电、3D/Chiplet 封装、AI for EDA 与硬件安全被统一放进 AI/HPC 的同一张路线图里。  

市场上最容易被低估的地方有四个：

1. **半导体总收入被 AI 与存储提前“拉大”**：Gartner 预测 2026 全球半导体收入 **1.32 万亿美元**，2025 为 **8053 亿美元**，2027 为 **1.5545 万亿美元**；其中存储从 2025 年 **2163 亿美元**跳到 2026 年 **6333 亿美元**，2027 年 **7481 亿美元**。
2. **AI 半导体不再只是 GPU**：按 Gartner 2026 年 AI 半导体约占总半导体 **30%**测算，AI 相关芯片/存储/互连/电源链条已经是 **约 3960 亿美元**级别的大赛道。
3. **未来一年最强 beta 不是单一“边缘 AI”概念，而是 HBM、先进封装/D2D、AI 光互连、AI 供电、EDA 自动化**；CIM/片上 LLM/6G FR3 是更长周期、更高波动的期权。
4. **利润池会从“只看算力芯片毛利”转向稀缺环节毛利**：HBM、先进封装、CPO 光引擎、D2D PHY/IP、AI 电源模块、EDA/IP 会吸走一部分过去只归属于 GPU/ASIC 的超额收益。

## 1. ISSCC 2026 的重点与发展方向

### 1.1 会议结构本身已经说明主线：AI/HPC/Chiplet/Optics/Power 被并列处理

ISSCC 2026 官方 Advance Program 首页给出的核心配置：

- 会议主题：**Advancing AI with IC & SoC Innovations**。
- 10 个 Tutorial 中，直接相关主题包括 Compute-in-Memory、High-Speed DAC、Beyond FinFET memory/digital、Clocking/CDR、Doherty PA 等。
- Sunday Forum：
  - **Power Efficient Circuits and Systems for Next-Gen Agentic AI and Robotics**
  - **Electrical and Optical Links Towards 400G+ Connectivity**
- Thursday Forum：
  - **Powering the Future of AI, HPC, and Chiplet Architectures**
  - **The Race for 6G FR3 (7-24GHz)**
  - **Analog for AI and AI for Analog**
  - **Calibration & Dynamic Matching Techniques for Data Converters**
- Short Course：
  - **Circuits for Optical Subsystems: Communications and Beyond**

这相当于把 AI 算力的问题从“处理器 session”扩展到 **存储、互连、光、电源、模拟、RF、EDA、安全**。如果对照 2023-2025 的市场叙事，2026 的显著变化是：产业不再把“模型变大”看成唯一变量，而是开始把 **功耗密度、I/O 能耗、内存带宽、封装良率、链路延迟、EDA 设计复杂度**视为同等重要的约束。

### 1.2 处理器与 AI 芯片：从单 die 到 chiplet、reticle-scale、可量产软件栈

官方 Processor / Highlighted AI Chip Release / AI Accelerator session 里，最值得关注的公开题名和指标：

| 方向 | ISSCC 2026 公开材料中的硬指标/事实 | 投资和产品含义 |
|---|---:|---|
| 数据中心 GPU | AMD Instinct MI350：**CDNA 4、3D-stacked 3nm XCD + 6nm IOD** | 高端 GPU 已经默认 chiplet + 先进封装，单颗 SoC 迭代变成系统封装迭代。 |
| AI SoC chiplet | Rebellions：Quad-Chiplet AI SoC，**16Gb/s UCIe-Advanced D2D**，题名披露 **30-60 TOPS/W** | 初创/区域 AI ASIC 开始用标准化 D2D 缩短与大厂差距。 |
| 端侧/车载视觉 | UniC-Vision：**14.4Gb/s、7.3pJ/b** ViT/OFDM AI-RAN accelerator | Vision Transformer、AI-RAN、车载推理开始共用低功耗数据搬运架构。 |
| IBM AI 推理 | IBM Spyre：Inference-Optimized Scalable AI Accelerator | 企业级 AI 推理开始走“可扩展、可部署”的 ASIC 产品路线，而不只是研究 demo。 |
| 扩散模型 | MediaTek MADiC：**3nm、7.4 TOPS/mm2、17.4 TOPS/W** generative diffusion accelerator | 端侧生成式 AI 从 CNN/NPU 时代进入 diffusion/transformer 专用优化。 |
| 3D Gaussian Splatting | 3D GS processor：**1286fps、0.39mJ/frame** | AR/VR、数字孪生、机器人视觉的轻量 3D 表征开始进入硬件优化窗口。 |
| 微软 AI 加速器 | MAIA：Reticle-Scale AI Accelerator | 云厂自研芯片进入“系统产品”阶段，影响 GPU 独占利润池。 |
| NVIDIA | GB10：SoC built for AI acceleration | AI PC/工作站/边缘开发者平台继续下沉。 |

变化判断：2024-2025 市场主要看 GPU 出货与 HBM 供给；ISSCC 2026 说明 2026-2027 的关键是 **谁能把 chiplet、HBM、D2D、供电、散热、软件编译器栈一起量产**。

### 1.3 存储：HBM4、LPDDR6、GDDR7 同时出现，说明 AI 内存路线分叉

ISSCC 2026 Memory session 公开题名非常集中：

| 产品/技术 | ISSCC 2026 指标 | 含义 |
|---|---:|---|
| HBM4 | **36GB、3.3TB/s HBM4 DRAM**，per-channel TSV RDQS auto calibration | HBM4 已进入公开电路实现阶段，2026-2027 重点从 HBM3E 产能转向 HBM4 资格认证、良率、封装协同。 |
| LPDDR6 | **16Gb LPDDR6，14.4Gb/s/pin**；另有 **16Gb 12.8Gb/s LPDDR6** | 端侧 AI、手机、AI PC 会用 LPDDR6 提升能效，而不是简单移植服务器 HBM。 |
| GDDR7 | **24Gb GDDR7，48Gb/s**，题名明确指向 **mid-range inference AI** | 中端推理卡/边缘服务器可能用 GDDR7 做“低成本推理内存层”，压低部分 HBM-only 预期。 |
| SRAM | 2nm nanosheet **350mV single-rail SRAM** | 低压 SRAM 是端侧 AI 与 always-on 计算的底层门槛。 |
| eMRAM/STT-MRAM | 16nm **168Mb embedded STT-MRAM、51.2Gb/s read throughput**，车载/edge AI | 非易失嵌入式存储在车规和低功耗 AI 上的商业化继续推进。 |
| 3D NAND | **2Tb 4b/cell、37.6Gb/mm2** | AI 不是只推 DRAM；数据湖、训练集、推理日志继续拉动 NAND 层级。 |

变化判断：市场以前常把“AI 内存”直接等同于 HBM；ISSCC 2026 更像是 **三层内存爆发**：

- 训练/高端推理：HBM3E -> HBM4。
- 中端推理/高性价比卡：GDDR7。
- 端侧/AI PC/手机/机器人：LPDDR6 + 低压 SRAM/eMRAM。

### 1.4 D2D 和高密度电互连：UCIe 进入能效竞争

Die-to-Die and High-Speed Electrical Transceivers session 披露的关键指标：

| 指标 | 论文题名披露 |
|---|---:|
| UCIe-compliant D2D | **48Gb/s/lane、1.24Tb/s/mm** |
| UCIe-like D2D | **32Gb/s、12.35Tb/s/mm2、0.36pJ/b**，3nm active LSI |
| modular D2D | **0.23pJ/b、24Gb/s、zero wake penalty** |
| single-ended SBD | **112Gb/s/wire** |
| PAM-4 CDR | **112Gb/s、0.76pJ/b** |
| XSR SBD | **56Gb/s/wire、0.292pJ/b** |
| PAM transmitter | **180-240Gb/s、0.70pJ/b analog power efficiency** |
| PAM-8 transmitter | **168Gb/s、1.06pJ/b** |

这组数字说明 D2D 的竞争焦点已从“能不能连上”变成 **每 bit 能耗、每 mm 带宽、唤醒延迟、PVT/失配跟踪、与 UCIe 的互操作**。  
对市场的含义是：高端 AI 芯片的稀缺不只在计算 die，还在 **有经验的 D2D PHY/IP、封装基板、interposer、active bridge、测试与良率管理**。

### 1.5 光互连/CPO：从 400G+ 论坛走向 6.4Tb/s ASIC 和 500Gb/s 光通道

官方材料中，光互连被放在 Forum、Short Course 和论文 session 三层：

- Forum：Electrical and Optical Links Towards **400G+ Connectivity**。
- Short Course：Optical subsystems，包括 optical link architecture、VCSEL、silicon photonics、emerging optical applications。
- Next-Generation Optical Transceivers session：
  - **2-channel 800Gb/s coherent-lite transceiver**
  - **2x500Gb/s monolithic silicon-photonic DWDM PAM-4 transceiver in 45nm CMOS SOI**
  - **6.4Tb/s、4.2pJ/b co-packaged optics ASIC with direct-drive**
  - **212Gb/s/lambda、0.91pJ/b direct-drive O-band monolithic coherent**
  - **112Gb/s NRZ heterodyne burst-mode receiver，23ns settled**

变化判断：2024-2025 市场主要押 800G 光模块放量；ISSCC 2026 的信号是 **光互连正在向低延迟、短距、高密度、CPO/near-package 方向迁移**。但这不代表 pluggable 模块立刻消失，更可能是：

- 2026：800G/1.6T pluggable 继续爆发；
- 2027：CPO 在超大集群/专用网络里 pilot；
- 2028 以后：如果可靠性、维修、热管理、激光源策略成熟，CPO 进入更大规模。

### 1.6 供电：AI/HPC 的下一条硬约束

官方 Thursday Forum 直接出现 **Integrated Voltage Regulator Solutions to Enable 5kW GPUs**，并讨论 AI data-center power delivery、3D vertical power delivery、package-integrated regulators、HBM power delivery、integrated magnetics。  

Compute Power session 披露：

| 技术 | ISSCC 2026 指标 |
|---|---:|
| coupled-OSC converter | **89.5% peak efficiency @61MHz、1.82W/mm2 @360MHz** |
| resonant sigma converter | **4Vin、93.4% peak efficiency、12A load、20mV undershoot** |
| 12-to-1V converter | **90.5% peak efficiency、721A/cm3 current density** |
| 48V hybrid converter | **48V to 0.8-1.6V、92.4% peak efficiency** |
| LLC resonant converter | **100A、93.4% peak efficiency** |
| symbol power tracking | **1.2us、1-to-12V** supply modulator |

变化判断：AI 芯片从 700W/1000W 走向 rack-scale 后，**48V 到 sub-1V 的转换链、垂直供电、封装内/近封装电源、HBM 供电完整性**会成为性能释放条件。市场容易只看 GPU ASP，但供电是未来一年更确定的配套增量。

### 1.7 CIM、片上 LLM 与 always-on AI：很热，但商业化节奏要分层

Compute-in-Memory session 指标密度极高：

| 论文方向 | ISSCC 2026 指标 |
|---|---:|
| MXFP CIM | **28nm、127.54TFLOPS/W MXFP6、117.42TFLOPS/W MXFP8** |
| charge-trap CIM | **12nm、4Mb、104.56-137.75TFLOPS/W** |
| ReRAM CIM | **22nm、96Mb、50.6-90.2TFLOPS/W**，支持 Mamba/Transformer/CNN |
| gain-cell CIM | **16nm、72kb、120.5TFLOPS/W** |
| near-memory DRAM | **1.2GHz、12.77GB/s/mm2、3D two-DRAM-one-logic**，edge LLM |
| SRAM digital CIM | **16nm、1Mb、1-8b configurable、444.21TOPS/W** |
| fully synthesizable digital CIM | **147TOPS/W、250TOPS/mm2、INT8xINT8** |

AI Accelerator session 端侧 LLM/视觉指标：

| 产品/论文方向 | ISSCC 2026 指标 |
|---|---:|
| ReRAM-on-logic LLM | **14.08-135.69 token/s** |
| dual-quantized LLM | **51.6uJ/token** |
| mobile personalization | SoulMate：**9.8mW** on-device LLM personalization SoC |
| VLM | Tri-Oracle：**17.78uJ/token** |
| SSM | LUT-SSM：**99.3TFLOPS/W** |
| speculative decoding | **105-685us/token**，billion-parameter models |
| always-on vision | ALPhA-Vision：**787us face detection latency，<5mW** |

变化判断：端侧 AI 的真实商业路径不是“手机跑满云端大模型”，而是 **小模型、个人化、always-on、传感器前处理、低功耗 token 生成**。CIM 指标很亮眼，但量产要跨过可编程性、精度、编译器、良率、工艺兼容、温漂校准等门槛。

### 1.8 6G FR3、雷达、Ambient IoT：标准前夜的硬件储备期

ISSCC 2026 将 **6G FR3 7-24GHz**单独设论坛。公开议程包括 FR3 FEM architectures、spectrum sensing/sharing、direct RF sampling ADC、ambient IoT、site-specific MIMO channel optimization。  
论文侧出现：

- Ku-band 6G FR3 Doherty PA：**25.3dBm Psat、29.7% PAE6dB**。
- FR3 source-follower PA：**4:1 VSWR resilience**。
- 24-27.5GHz load-modulated balanced amplifier。
- 330-344GHz GaN PA：**86mW output @340GHz**。
- Radar/UWB：**128mW 2x4 radar-on-chip**；60/77GHz 4T/4R radar RFIC；**234-252GHz** dual-polarized transceiver；UWB transmitter **0.0523mm2、11.4mW**。

变化判断：6G FR3 还没有商业收入爆发，但 RF 前端、PA、ADC、MIMO 测试平台会在 2026-2028 先投入；真正 handset 大规模收入更可能在 2029-2031。

### 1.9 安全：FHE/PQC 从算法议题进入电路议题

Hardware Security session 里：

- HERACLES：**8192-way SIMD programmable scalable** security processor。
- FHE processor：**28nm、0.48mJ/boot**。
- PQC KEM：**16nm、0.042mm2、0.66uJ/op**。
- OmniCrypt：**435.86M-GOPS/W bootstrappable multi-scheme FHE accelerator**。
- SQIsign accelerator：**0.05mm2、1.19-7.34mW**，IoT。
- Chip-to-chip probing attack detector：**166um2/lane、8Gb/s/lane**。
- TRNG：**0.066pJ/bit**，resilient to power-noise injection attacks。

变化判断：AI agent、云端隐私、车载 OTA、IoT 长寿命设备会把 PQC/FHE/PUF/TRNG 从“安全团队问题”变成 SoC baseline feature。商业爆发不如 HBM/光模块快，但安全 IP attach rate 会持续提高。

## 2. 哪些产品/技术方向会爆发：力度、成熟和量产路线

### 2.1 爆发优先级总表

| 优先级 | 方向 | 未来 12 个月爆发力度 | 主要催化 | 主要风险 |
|---|---|---:|---|---|
| S | HBM3E/HBM4 与 AI DRAM | 极强 | AI 训练/推理集群、Gartner 存储收入跳升、HBM4 公开电路指标 | 良率、封装瓶颈、客户集中、价格周期反转 |
| S | 800G/1.6T 光模块、硅光、CPO pilot | 极强 | AI 集群 scale-out、TrendForce 预计 800G+ 份额 2026 超 60% | CPO 维修/热/激光源，模块 ASP 下滑 |
| S | 先进封装、D2D/UCIe、interposer/bridge | 很强 | AMD MI350、reticle-scale MAIA、UCIe D2D 能效指标密集 | 产能/良率、标准碎片化、客户自研 |
| S | AI/HPC 供电：48V、IVR、vertical power、HBM power | 很强 | 5kW GPU、48V-to-1V、100A converter | 电源模块价格竞争、客户定制化高 |
| A | 数据中心 AI ASIC/GPU 与自研加速器 | 很强 | hyperscaler capex、AMD/NVIDIA/Microsoft/IBM/MediaTek 等 chip release | 竞争加剧、HBM 分配、毛利回落 |
| A | EDA/AI for Design | 强 | Cadence plenary、Analog for AI forum、设计复杂度上升 | 客户预算、AI 生成结果可验证性 |
| B+ | GDDR7 中端推理卡 | 强 | ISSCC 明确“mid-range inference AI”，性价比需求 | HBM 降价、云端产品路线改变 |
| B | Edge LLM/always-on vision/CIM | 中到强 | uJ/token、mW 级 SoC 指标密集 | 软件生态、模型变化快、量产精度与良率 |
| B | PQC/FHE/secure chip-to-chip IP | 中 | 后量子标准、agentic AI 安全、车载/IoT 长寿命 | 商业付费节奏慢，IP 议价不强 |
| C+ | 6G FR3/Radar/Ambient IoT | 中低，长期强 | FR3 forum、PA/ADC/radar 硬件储备 | 标准和终端量产时间晚 |

### 2.2 三种情景：成熟和量产路线

#### HBM4 / AI DRAM

- 基准：2026 仍以 HBM3E 放量为收入主力；HBM4 进入客户验证和小批量，2027 放量。HBM 价格保持高位，但客户会要求长期供货协议。
- 乐观：2026 下半年 HBM4 在头部 GPU/ASIC 平台开始较明显 revenue contribution；HBM3E 供需仍紧，HBM 毛利保持行业高位。
- 超预期乐观：HBM4 良率爬坡快于预期，同时 2027 平台提前锁单；HBM 供应商获得类似先进封装的“准产能溢价”，年度收入增速超过 80%。

#### 800G/1.6T 光模块、硅光、CPO

- 基准：2026 爆发核心是 800G/1.6T pluggable；CPO 以 ASIC/光引擎试点为主，2028 前大规模替代比例有限。
- 乐观：AI 集群横向扩展速度继续高于市场预期，1.6T 从高端云厂向更多客户扩散；CPO 在 2027 年进入特定超大集群。
- 超预期乐观：大客户统一 CPO/near-package optical 规格，可靠性和维修模型快速成熟；2027-2028 CPO 收入斜率明显前移。

#### D2D/UCIe/先进封装

- 基准：D2D 先在 GPU、AI ASIC、网络芯片、CPU-chiplet 中放量，UCIe 更多是互联参考框架，实际产品仍有私有 PHY。
- 乐观：UCIe-compatible IP 生态形成，第三方 chiplet 在部分 AI/网络/存储控制器平台上可采购。
- 超预期乐观：hyperscaler 把 D2D/Chiplet 作为供应链多元化工具，更多 ASIC 采用标准 chiplet 采购，IP/测试/封装公司获得高弹性。

#### AI/HPC 供电

- 基准：48V rack power、近负载 converter、package-aware HBM power delivery 在 2026 明显增量；IVR/vertical power 多为高端平台。
- 乐观：5kW GPU/加速器路线确认，电源模块、磁性元件、先进封装电源协同进入平台级 design-in。
- 超预期乐观：供电/散热成为 AI 集群上限，客户愿意为 1-2 个百分点系统效率付高溢价；高端电源 IC/模块毛利上修。

#### 数据中心 AI ASIC/GPU

- 基准：GPU 仍是最大收入池，自研 ASIC 占比上升但不会短期替代 GPU；AMD/ASIC/云厂产品拉高非 NVIDIA 份额。
- 乐观：推理需求和 agentic workflow 推动多个云厂 ASIC 大规模投产，AI 加速器收入增速继续 50%+。
- 超预期乐观：推理 token 成本下降释放需求弹性，GPU + ASIC 同时爆发，算力芯片全年供不应求。

#### Edge LLM / CIM

- 基准：2026 量产收入来自传统 NPU、AI MCU、视觉 SoC；CIM 主要在研究芯片、少数专用 IP 和传感器前处理。
- 乐观：always-on vision、语音、个人化小模型在手机/眼镜/可穿戴进入差异化卖点，CIM/SRAM near-memory 被部分 SoC 采用。
- 超预期乐观：端侧隐私和低延迟需求推动本地 LLM 常驻，uJ/token 成为终端芯片新 KPI，CIM 进入第一批商业 AI MCU/edge SoC。

#### EDA / AI for Design

- 基准：2026 收入体现为 AI-assisted verification、layout、PPA optimization、analog/RF automation seat uplift。
- 乐观：agentic EDA 工作流显著缩短部分模块设计周期，按算力/使用量收费推高 ARPU。
- 超预期乐观：AI for Design 成为先进节点和 chiplet 设计刚需，EDA/IP 公司同时吃到 seat、compute、IP 三重增长。

## 3. 市场规模、增速、利润率：基准/乐观/超预期

口径说明：  
Gartner 的总半导体、存储、非存储为公开预测；细分市场如 HBM、CPO、AI 电源、D2D IP 没有统一官方口径，下表为基于公开总盘子、供应链结构和 ISSCC 2026 技术成熟度的区间推算。利润率以 **毛利率**为主；若是模块/封装类，利润率低于芯片/IP 类。

### 3.1 总盘子

| 市场 | 当前/2026 规模 | 未来一年基准 | 乐观 | 超预期乐观 | 当前利润率与趋势 |
|---|---:|---:|---:|---:|---|
| 全球半导体 | **1.32 万亿美元**，Gartner 2026 | +18%-25% 到 2027 | +25%-32% | +35%+ | 行业平均毛利分化极大；AI/EDA/IP/HBM 高，消费/通用芯片低。 |
| 存储半导体 | **6333 亿美元**，Gartner 2026；2025 为 **2163 亿美元** | +15%-25% | +25%-35% | +40%+ | DRAM/HBM 处于高景气，毛利率上行；周期反转风险从 2027 起加大。 |
| 非存储半导体 | **6869 亿美元**，Gartner 2026；2025 为 **5890 亿美元** | +10%-15% | +15%-22% | +25%+ | AI ASIC/GPU/IP 高，传统 MCU/模拟恢复较慢。 |
| AI 相关半导体 | Gartner 称 2026 约占总半导体 **30%**，约 **3960 亿美元** | +35%-50% | +50%-70% | +80%+ | 头部 GPU/ASIC 毛利高，但竞争和客户自研会压制部分超额毛利。 |

### 3.2 重点产品和技术市场

| 方向 | 2026 市场规模估计 | 基准：未来 1 年增速 | 乐观：未来 1 年增速 | 超预期乐观 | 当前利润率 | 未来利润率走向 |
|---|---:|---:|---:|---:|---:|---|
| HBM/HBM4 及 AI 高端 DRAM | **800-1100 亿美元**推算；包含 HBM3E/HBM4 及 AI 服务器高端 DRAM | +35%-55% | +55%-75% | +80%-110% | HBM 毛利约 **55%-70%**，高于普通 DRAM | 2026 仍上行；2027 若供给释放，毛利高位震荡。 |
| GDDR7 中端 AI 推理内存 | **80-150 亿美元**推算 | +25%-40% | +40%-65% | +80% | 毛利约 **35%-50%** | 若中端推理卡放量，ASP 和毛利好于普通 GDDR；但 HBM 降价会压制。 |
| 数据中心 AI 加速器 GPU/ASIC | **1800-2300 亿美元**推算，不含全部存储 | +35%-50% | +50%-70% | +80%-100% | 头部公司毛利可达 **65%-75%**；ASIC 供应链平均 **35%-60%** | 头部仍高，但客户自研、AMD/ASIC 竞争会使行业平均毛利略降。 |
| 先进封装/Chiplet/D2D 相关 | 先进封装 **500-700 亿美元**推算；D2D PHY/IP/测试为其中小但高增部分 | +20%-35% | +35%-55% | +60%-80% | OSAT/封装 **15%-30%**；foundry advanced packaging **35%-55%**；IP **70%+** | 稀缺产能维持高价，IP/测试利润率好于纯封装。 |
| 800G/1.6T 光模块与 AI 光互连 | **120-180 亿美元**推算；CPO 仍小 | +45%-65% | +65%-90% | +100%+ | 光模块 **25%-40%**；DSP/光引擎/硅光可 **40%-60%** | 模块 ASP 会降，但 1.6T/CPO mix 改善利润结构。 |
| CPO/near-package optical | 2026 约 **5-15 亿美元**推算，主要 pilot/早期产品 | +80%-150% | +150%-250% | +300%+ | 早期毛利 **40%-60%**，系统集成不稳定 | 2026-2027 取决于客户规格锁定；成熟后模块化竞争会压毛利。 |
| AI/HPC 电源 IC、模块、48V/IVR | **40-70 亿美元**AI 相关增量推算；整体 PMIC/电源管理更大 | +20%-35% | +35%-55% | +60%-80% | 模拟 IC **45%-65%**；电源模块 **25%-45%** | 高端平台 design-in 提升毛利，通用模块价格竞争仍强。 |
| EDA/IP/AI for Design | **180-240 亿美元**推算 | +10%-15% | +15%-25% | +30%+ | 软件/IP 毛利 **80%-90%**，运营利润率 **30%-45%** | AI seat/usage pricing 可能推高 ARPU，利润率稳中上行。 |
| Edge AI SoC/AI MCU/端侧 NPU | **500-800 亿美元**推算，含手机/PC/汽车/IoT AI 芯片价值 | +12%-20% | +20%-35% | +40%-55% | SoC 毛利 **35%-55%**；MCU/传感器低一些 | 量大但竞争激烈；真正高毛利来自差异化 IP 和软件生态。 |
| CIM/near-memory AI IP | **<10 亿美元**直接商业收入推算，研究和试产为主 | +30%-60% | +60%-120% | +150%+ | IP/专用芯片可 **50%-80%**，但收入基数小 | 2026 更多是技术期权；量产突破会带来非线性重估。 |
| 6G FR3/RF 前端前置研发 | FR3 直接商业 **<10 亿美元**；相邻 RFFE/测试市场约 **数百亿美元** | +5%-15% | +15%-25% | +30%+ | PA/RFFE **35%-50%** | 2026-2028 多为研发和测试设备，终端量产前利润贡献有限。 |
| PQC/FHE/security IP | **10-30 亿美元**推算，含 IP、secure MCU、加速器小市场 | +15%-30% | +30%-50% | +60%+ | IP **70%+**；secure MCU **35%-55%** | 标准和法规推动 attach rate，付费节奏慢但粘性强。 |

## 4. 与当前市场可能相违背的重要洞见

### 4.1 “半导体 2026 超高增长”不等于全行业健康

Gartner 的 2026 总半导体 **1.32 万亿美元**预测非常惊人，但结构上主要由 **存储从 2163 亿美元跳到 6333 亿美元**拉动。  
这意味着：广义半导体 ETF 或通用芯片公司未必都受益；收益会高度集中在 **HBM/DRAM、AI ASIC/GPU、先进封装、光互连、EDA/IP、电源**。消费 MCU、传统模拟、低端逻辑可能仍是弱复苏。

### 4.2 HBM 不是唯一 AI 内存，GDDR7/LPDDR6 可能改变中低端推理成本曲线

ISSCC 2026 同时出现 HBM4、LPDDR6、GDDR7，而且 GDDR7 题名直接写明 **mid-range inference AI**。  
这与“所有 AI 推理都只能走 HBM”的市场直觉相反。未来一年：

- 高端训练/大模型推理继续 HBM；
- 中端推理卡可能大量采用 GDDR7；
- 端侧 AI 主要依靠 LPDDR6/低压 SRAM/eMRAM。

若 GDDR7 推理卡形成规模，会对部分 HBM 需求外推、低端 GPU ASP、边缘服务器 BOM 产生重新定价。

### 4.3 CPO 很重要，但 2026 不是“一夜替代光模块”

ISSCC 2026 的 **6.4Tb/s、4.2pJ/b CPO ASIC**和 direct-drive 光电指标说明方向明确；TrendForce 资料也显示 800G+ 光模块份额会在 2026 明显提升。  
但 CPO 的量产难题不是单一芯片指标，而是：

- 激光源放置与可靠性；
- 现场可维修性；
- 热耦合；
- 交换 ASIC、光引擎和封装良率绑定；
- 客户网络架构统一程度。

所以 2026 最确定的是 **800G/1.6T pluggable 爆发**，CPO 更像 2027-2028 的高弹性期权。

### 4.4 AI 芯片毛利可能被“系统瓶颈环节”重新分配

市场常把 AI 利润池等同于 GPU 毛利。ISSCC 2026 更强调系统：D2D、HBM power、48V-to-1V、电光互连、EDA。  
未来一年，若 GPU/ASIC 供给被封装、HBM、光模块、电源拖住，利润池会转向：

- HBM stack 与 TSV/测试；
- CoWoS/SoIC/active bridge/interposer；
- D2D PHY/IP；
- optical DSP/硅光/激光器；
- 高端电源 IC/模块；
- EDA/IP。

### 4.5 “端侧 AI 爆发”要看 uJ/token 和 mW，而不是只看 TOPS

ISSCC 2026 端侧论文写的是 **51.6uJ/token、17.78uJ/token、9.8mW、<5mW、787us**，而不是单纯 TOPS。  
这说明真实产品指标将从“宣传 TOPS”转为：

- token 能耗；
- 常驻功耗；
- 首 token 延迟；
- memory footprint；
- 小模型个性化；
- 传感器到模型的端到端延迟。

这对 AI PC/手机 SoC 厂商是挑战：如果没有模型/编译器/系统功耗协同，单独堆 NPU TOPS 很难转化为用户体验。

### 4.6 Analog/RF 不是 AI 时代的配角，反而变成基础设施瓶颈

ISSCC 2026 里 high-speed ADC/DAC、PLL/CDR、PA、RF front-end、calibration、analog for AI 都被重点安排。典型指标包括：

- 7b **175GS/s** time-interleaved slope ADC；
- 12b **12GS/s** pipeline ADC in 5nm；
- 14b **20GS/s** RF-sampling DAC；
- 112Gb/s electrical transceiver；
- 212Gb/s/lambda coherent optical；
- FR3 PA 和 direct RF sampling ADC。

结论：AI 基建不是纯数字芯片工程，analog/mixed-signal/RF 人才和 IP 会更稀缺。

### 4.7 6G FR3 的投资窗口在设备/测试/RF，不在 2026 终端放量

ISSCC 2026 的 FR3 论坛和论文说明 6G 已经进入电路储备期；但这不等于 2026 出现 handset 大规模换机。更合理路线：

- 2026-2027：PA、FEM、ADC、测试平台、channel sounding、spectrum sharing；
- 2028-2029：预商用基站/终端原型；
- 2029-2031：标准和终端量产收入。

这与“6G 马上爆发”的叙事相反；短期更该看 RF 测试、PA/FEM、材料与高频封装。

## 5. 投资/产业链映射

### 5.1 最强确定性链条

1. **HBM/HBM4**：存储厂、TSV/测试、HBM PHY、HBM power integrity、先进封装配套。
2. **先进封装/Chiplet/D2D**：CoWoS/SoIC、interposer、active bridge、UCIe PHY、D2D verification、known-good-die 测试。
3. **AI 光互连**：800G/1.6T 光模块、DSP、硅光、VCSEL/EML、激光器、CPO optical engine、低延迟光交换。
4. **AI 电源**：48V 到低压 converter、IVR、vertical power、integrated magnetics、HBM power delivery。
5. **EDA/IP**：AI-assisted verification/layout/PPA、analog/RF design automation、chiplet/package co-design、security IP。

### 5.2 高弹性但更不确定的链条

1. **CIM/near-memory AI**：指标惊艳，但产品化路径依赖特定模型、编译器和良率。
2. **端侧 LLM SoC**：需要真实应用拉动；手机/眼镜/机器人比 AI PC 更可能先体现 always-on 价值。
3. **PQC/FHE**：法规和云隐私会推，但商业收入爬坡慢。
4. **6G FR3**：标准前夜，先看测试和 RF，不应提前按终端放量估值。

## 6. 未来一年跟踪指标

### HBM/存储

- HBM4 qualification 节点：头部 GPU/ASIC 平台是否在 2026 下半年确认。
- HBM ASP、bit growth、yield、TSV 良率。
- GDDR7 是否进入中端推理卡大规模设计。
- LPDDR6 是否在 2027 手机/AI PC 平台锁定。

### 光互连/CPO

- 800G+ 模块出货占比是否如 TrendForce 所称在 2026 超过 60%。
- 1.6T 模块实际 ASP 下降速度。
- CPO 的 laser strategy：external laser source 还是 co-packaged laser。
- CPO 是否从 demo 进入 cloud design-in。

### D2D/封装

- UCIe-compatible PHY 是否进入量产产品，而不仅是论文。
- D2D 能耗是否稳定低于 0.5pJ/b。
- Advanced packaging 交期和价格。
- known-good-die 测试覆盖率和良率损失。

### 电源

- 5kW GPU/rack-scale AI 平台是否成为主流路线。
- 48V-to-1V conversion efficiency 是否稳定在 90%+。
- IVR/vertical power 是否进入头部 AI 加速器。
- HBM power integrity 是否成为平台良率和稳定性问题。

### 端侧 AI/CIM

- 端侧产品是否开始披露 uJ/token、首 token 延迟、always-on mW，而非只披露 TOPS。
- CIM 是否进入量产 SoC 的一部分，而不是单独 test chip。
- 小模型个人化是否形成付费应用。

## 7. 资料来源

- [ISSCC 2026 Advance Program PDF](https://submissions.mirasmart.com/ISSCC2026/PDF/ISSCC2026AdvanceProgram.pdf)
- [ISSCC 2026 Call for Papers PDF](https://submissions.mirasmart.com/ISSCC2026/PDF/ISSCC2026CFP.pdf)
- [Gartner: Worldwide Semiconductor Revenue to Exceed $1.3 Trillion in 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- [TrendForce: AI-Driven Data Centers Drive Strong Growth in Optical Communications Market](https://www.trendforce.com/presscenter/news/20250630-12614.html)
- [IBM Research: On-chip power breakthrough for next-generation AI chips](https://research.ibm.com/blog/power-management-circuit-isscc)
- [imec: Analog-to-digital conversion at speed and scale](https://www.imec-int.com/en/articles/analog-digital-conversion-speed-and-scale)

# NVIDIA GTC 2026：从 GPU 周期转向“AI Factory 工业化”的关键拐点

截至日期：2026-05-08  
范围：仅使用 NVIDIA 官方发布、keynote deck、技术博客、财报/IR、公开媒体与第三方市场资料；未参考项目内既有文件或信息。  
核心结论：GTC 2026 不是一次单纯的 GPU 发布会，而是 NVIDIA 把 AI 价值链从“芯片供给”推到“1GW 级 AI factory 设计、建设、运营和变现”的拐点。真正的新变量是推理、长上下文、agentic workload、功耗/电网、存储/内存墙、低延迟异构推理和全栈软件。

## 一页结论

1. **需求口径被显著上修**：Jensen Huang 在 GTC 2026 keynote 中把 Blackwell + Vera Rubin 相关 AI 硬件到 2027 年的收入/订单机会表述为“至少 1 万亿美元”，明显高于此前通过 2026 年约 5,000 亿美元的口径。结合 NVIDIA FY2026 数据中心收入 1,937 亿美元、Q4 数据中心单季 623 亿美元、Q1 FY2027 公司收入指引 780 亿美元，短期订单能见度仍非常强。
2. **Vera Rubin 是“七颗芯片、五类机架、一套 AI factory”的系统产品**：Vera CPU、Rubin GPU、NVLink 6、ConnectX-9、BlueField-4、Spectrum-6、Groq 3 LPU 共同组成。重点不是单卡性能，而是 NVL72、LPX、STX、SPX、CPU rack 组合成 POD/GW 级 token 生产系统。
3. **推理成为第一工作负载**：官方 keynote 明确把“tokens are the new commodity / compute is revenue”作为经济模型。Deloitte 预计 2026 年 inference 约占全部 AI compute 的三分之二，inference-optimized chips 市场超过 500 亿美元；Gartner 预计 AI-optimized IaaS 2026 年 375 亿美元，其中 206 亿美元用于 inference。
4. **Vera Rubin NVL72 量产时间明确**：官方称 Vera Rubin 相关产品已进入 full production，合作伙伴产品从 2026 年下半年开始供应；NVL72 单机架 72 个 Rubin GPU + 36 个 Vera CPU，NVLink 6 每 GPU 3.6TB/s、每机架 260TB/s scale-up bandwidth，1.6PB/s HBM4 带宽，3.6EF NVFP4。
5. **LPX/Groq 3 是最大反共识技术点**：NVIDIA 把 LPU 纳入 Vera Rubin 平台，承认长上下文、低延迟 decode 不能只靠 GPU。LPX 单机架 256 个 LPU、315PFLOPS、128GB SRAM、40PB/s memory bandwidth、640TB/s scale-up bandwidth；与 Rubin 组合后官方称可达 35x inference throughput/MW、10x trillion-parameter model 收入机会。
6. **数据中心瓶颈从 GPU 转为“电力 + 内存 + 网络 + KV cache 存储”**：BlueField-4 STX/CMX 直接针对 KV cache 与 agent memory，官方给出 5x token throughput、4x energy efficiency、2x page ingestion；DSX Max-Q/DSX Flex 则把冷却、电力调度和电网接入变成 AI factory 软件的一部分。
7. **利润率短期仍有支撑**：NVIDIA FY2026 GAAP 毛利率 71.1%，Q4 75.0%，Q1 FY2027 指引约 75%。若 Rubin/LPX/STX 组合按机架/POD/GW 出货，毛利率更像系统级平台，而不是单卡 ASP 被压缩；主要风险是 HBM/DRAM 成本、定制 ASIC 替代和 hyperscaler 议价。
8. **市场规模最大的不是某个单品，而是 2026-2028 AI data center capex**：Deloitte 预计 2026 年全球 AI data center capex 4,000-4,500 亿美元，其中芯片 2,500-3,000 亿美元，2028 年 AI data center capex 可能到 1 万亿美元；Gartner 预计 2026 年 data center systems 超过 7,880 亿美元。
9. **机器人/自动驾驶是中长期，不是 2026 主要收入爆发点**：NVIDIA Automotive FY2026 仅 23 亿美元；Deloitte 估算 2026 年工业用途 humanoid robot 市场约 2.1-2.7 亿美元、1.5 万台出货。GTC 的现实意义是 Cosmos/GR00T/Alpamayo/Physical AI Data Factory 让“数据和仿真”先商业化。
10. **反共识判断**：市场若只看“GPU 单价/训练需求是否见顶”，会低估 NVIDIA 把 inference、storage、networking、CPU、power/cooling、software orchestration 全部纳入收费栈后的收入密度；但若把 1 万亿美元口径当作无风险收入，也会低估电力、内存、施工、客户 ROI 和 ASIC 替代风险。

## GTC 2026 会议事实与信息源权重

- 时间地点：NVIDIA GTC 2026 于 2026-03-16 至 2026-03-19 在 San Jose 举行，keynote 为 2026-03-16 11:00 PT。
- 规模：官方会前稿披露超过 30,000 名参会者、来自 190 多个国家/地区、1,000+ sessions、9 个 full-day workshops、60+ hands-on labs、240+ Inception startups、150+ poster presentations。
- 官方一手资料核心包括：GTC 2026 press kit、keynote deck、Vera Rubin platform press release、Vera CPU、BlueField-4 STX、DSX、Dynamo 1.0、robotics/physical AI、DRIVE Hyperion、DLSS 5、NVIDIA FY2026 财报。
- 第三方资料主要用于市场规模、capex 和反共识验证，包括 Gartner、Deloitte、IDC、TechCrunch、Reuters/Axios/Tom's Hardware 等公开报道。

## 重点方向与相对过去的变化

### 1. 从“GPU 卖方周期”到“AI factory 操作系统”

过去两年市场主线是 H100/H200/Blackwell 的 GPU 供给紧缺。GTC 2026 的变化是 NVIDIA 把叙事升级为 AI factory：芯片、机架、网络、存储、电力、冷却、数字孪生和推理操作系统一起优化，目标函数从 FLOPS 变成 **tokens/watt、tokens/sec、time-to-first-revenue、goodput、revenue/GW**。

官方 keynote 中的典型数字：

- GB300 NVL72 相比 H200 NVL8：35x lower token cost、50x higher performance/watt。
- Vera Rubin NVL72：相对 Blackwell 平台可用 1/4 GPU 训练大型 MoE，推理 throughput/watt 最高 10x，token cost 降到 1/10。
- Keynote deck 给出的 revenue/GW 框架：Hopper 约 300 亿美元/GW 年收入机会，Rubin 约 1,500 亿美元/GW，Rubin + LPX 约 3,000 亿美元/GW。

这说明 NVIDIA 的商业化指标已经从“卖多少 GPU”转向“每 GW 电力能生产多少可收费 token”。

### 2. Inference inflection：推理不再是训练后的低毛利尾声

GTC 2026 的最重要技术转折是推理变成主战场。关键原因：

- Agentic AI 带来多轮工具调用、代码执行、检索、验证、长上下文、长思考。
- Deloitte 估计 post-training 总 compute 可达到原始 foundational model training 的 30x；long thinking 可超过简单 inference 的 100x。
- Gartner 预计 AI-optimized IaaS 2026 年 375 亿美元，其中 55% 即 206 亿美元支持 inference，2029 年 inference 占比超过 65%。
- Deloitte 预计 2026 年 inference-optimized chips 市场超过 500 亿美元，2025 年已超过 200 亿美元。

反直觉点：模型效率提升不会自动减少 GPU 需求；如果 token 使用量、agent 步数、上下文长度和 test-time compute 增长更快，总 compute 仍上升。

### 3. Vera Rubin：七芯片、五机架、POD/GW 级产品化

官方将 Vera Rubin 定义为七类关键芯片与五类 rack-scale systems：

- 计算：Vera CPU、Rubin GPU、Groq 3 LPU。
- 互连/网络：NVLink 6 Switch、ConnectX-9 SuperNIC、Spectrum-6 Ethernet switch。
- 存储/安全/数据处理：BlueField-4 DPU。
- 五类机架：Vera Rubin NVL72 GPU rack、Vera CPU rack、Groq 3 LPX inference rack、BlueField-4 STX storage rack、Spectrum-6 SPX Ethernet rack。

技术博客披露 Vera Rubin POD 级别数据：40 racks、1.2 quadrillion transistors、近 20,000 个 NVIDIA dies、1,152 个 Rubin GPUs、60 exaflops、10PB/s total scale-up bandwidth。

### 4. CPU 被重新定价：Vera 不只是配角

Vera CPU 的定位很清楚：agentic AI 和 reinforcement learning 需要大量 CPU sandbox、工具环境、数据处理和 orchestration。官方给出的核心数字：

- 88 个 NVIDIA Olympus cores。
- LPDDR5X memory subsystem 最高 1.2TB/s，约为通用 CPU 2x bandwidth、约半功耗。
- NVLink-C2C coherent bandwidth 1.8TB/s，约为 PCIe Gen 6 的 7x。
- Vera CPU rack：256 个液冷 Vera CPUs，可支撑超过 22,500 个并发 CPU environments。
- 官方称结果效率 2x、速度比传统 rack-scale CPU 快 50%。

这意味着 CPU 市场中与 AI agent 调度、sandbox、数据流水线相关的部分，会从低 ASP x86 服务器转向高带宽、低功耗、与 GPU coherent coupling 的专用架构。

### 5. LPX/Groq 3：NVIDIA 把“低延迟 LPU”收进自己的生态

Groq 3 LPX 是 GTC 2026 最大的技术/商业信号之一。它不是替代 Rubin GPU，而是与 Rubin 分工：

- Rubin GPU 处理 prefill、attention、HBM 容量与吞吐。
- LPU/LPX 处理 decode loop 中 latency-sensitive 的 FFN/MoE expert execution。
- Dynamo 负责跨 GPU/LPU/存储的 inference orchestration。

官方数字：

- 256 LPUs per rack。
- 315PFLOPS AI inference compute。
- 128GB SRAM。
- 40PB/s memory bandwidth。
- 640TB/s scale-up bandwidth。
- 2026 年下半年可用。
- 与 Vera Rubin NVL72 组合，官方称可达 35x inference throughput/MW、10x trillion-parameter model revenue opportunity。

判断：LPX 将最先用于 ultra-premium reasoning、trillion-parameter、million-token context、低延迟高并发场景。它不是普及型推理，而是最高 ARPU 的推理层。

### 6. Context memory/storage 成为新瓶颈：BlueField-4 STX

Agent 的上下文不是简单文件存储，而是 KV cache、会话状态、工具结果、历史轨迹和多轮记忆。传统存储会拉低 GPU 利用率。STX/CMX 的关键是把存储变成 AI-native context memory tier。

官方数字：

- CMX context memory storage platform 相比传统存储最高 5x tokens/sec。
- STX 相比传统 CPU 架构最高 4x energy efficiency。
- 数据/page ingestion 最高 2x。
- Keynote deck：50Tb/s networking bandwidth，16TB shared context/GPU。
- 2026 年下半年由合作伙伴提供。

重要合作方包括 CoreWeave、Crusoe、IREN、Lambda、Mistral AI、Nebius、OCI、Vultr；存储/OEM 生态包括 DDN、Dell、HPE、IBM、NetApp、VAST、WEKA、Supermicro、QCT 等。

### 7. 网络与光互连：Spectrum-X、NVLink 6/7、CPO、NVLink Fusion

GTC 2026 的网络变化：

- NVLink 6：Vera Rubin NVL72 每 GPU 3.6TB/s，rack 级 260TB/s。
- Spectrum-6：keynote deck 给出 102T、CPO、CX9 1600G。
- Spectrum-X Ethernet Photonics/CPO：官方称相对传统 pluggable transceivers 可达 5x optical power efficiency、10x resiliency。
- NVLink Fusion + Marvell：NVIDIA 投资 Marvell 20 亿美元，允许客户在 NVLink ecosystem 内开发 semi-custom AI infrastructure，Marvell 提供 custom XPUs 与 NVLink Fusion-compatible scale-up networking。

反共识点：NVLink Fusion 看似“开放”，实质是把 hyperscaler custom ASIC 拉进 NVIDIA 的网络、CPU、DPU、软件和供应链框架。NVIDIA 放弃一部分封闭 GPU 纯度，换更大的 AI factory 控制面。

### 8. DSX：AI factory 的电力、冷却、施工和运营软件化

DSX 是把 AI factory 设计与运行从工程项目变成可复制平台：

- Vera Rubin DSX Reference Design：覆盖 compute、Spectrum-X networking、storage、power、cooling、controls。
- Omniverse DSX Blueprint：用于 AI factory 数字孪生、设计、仿真、运营。
- DSX Max-Q：固定 power budget 下最大化 token/watt。
- DSX Flex：把 AI factory 变成 grid-flexible asset，官方称可解锁 100GW stranded grid power。
- NVIDIA 官方称 DSX Max-Q 可在固定电力数据中心内部署 30% more AI infrastructure。
- Phaidra 与 DSX Max-Q 集成，自称通过削减 cooling spikes 可释放约 10% more compute。

市场意义：AI capex 的 bottleneck 从 GPU 供应扩散到电网并网、变压器、液冷、施工、运营调度。DSX 让 NVIDIA 可以影响“芯片以外”的 1,500 亿美元级非芯片 AI data center capex。

### 9. Open models / agent platform：用开放降低采用门槛，用全栈提高锁定

GTC 发布了 NemoClaw、OpenShell、Agent Toolkit、AI-Q Blueprint、Nemotron Coalition、Nemotron 3、Cosmos 3、GR00T N1.7、Alpamayo 1.5、BioNeMo/Proteina-Complexa 等。

重要事实：

- Agent Toolkit 包含 OpenShell runtime，强调 policy-based security、network/privacy guardrails。
- AI-Q Blueprint 在 DeepResearch Bench 上强调 accuracy/cost，官方称 hybrid frontier + open models 可将 query costs 降低约 50%。
- Nemotron Coalition 成员包括 Black Forest Labs、Cursor、LangChain、Mistral AI、Perplexity、Reflection AI、Sarvam、Thinking Machines Lab，目标是训练并开源 Nemotron 4 基础模型。
- Open models 被 CodeRabbit、CrowdStrike、Cursor、Factory、ServiceNow、Perplexity、LG、Novo Nordisk 等采用。

判断：模型开放不是放弃利润，而是把开发者、企业 agent、物理 AI、医疗 AI 的工作负载导向 NVIDIA inference stack。

### 10. Physical AI / robotics / autonomous vehicles：长周期大叙事，短期收入小但数据工厂先爆发

官方发布点：

- Robotics：ABB、AGIBOT、Agility、CMR Surgical、FANUC、Figure、Hexagon、KUKA、Medtronic、Skild AI、Universal Robots、World Labs、YASKAWA 等构建在 NVIDIA stack 上。
- 全球 FANUC、ABB、YASKAWA、KUKA 工业机器人装机超过 200 万台，正在把 Omniverse/Isaac 加入虚拟调试，并把 Jetson 集成到控制器。
- Physical AI Data Factory Blueprint：用 Cosmos Curator、Cosmos Transfer、Cosmos Evaluator、OSMO，把有限真实数据扩展为大量合成/边缘场景数据。
- Automotive：BYD、Geely、Isuzu、Nissan 采用 DRIVE Hyperion；Uber 计划 2028 年前在 28 个市场部署 NVIDIA DRIVE AV stack robotaxi，2027 年上半年从 Los Angeles 和 San Francisco Bay Area 开始。
- Alpamayo 1.5：输入 driving video、ego-motion、navigation、natural language prompts，输出 trajectories 和 reasoning traces；Alpamayo 发布后已被 100,000+ automotive developers 下载。

判断：机器人和 AV 的短期财务贡献不如数据中心，但“仿真 + 数据生成 + edge inference + safety OS”会先形成平台收入。

### 11. DLSS 5 与 RTX：消费端不是主线，但技术重要

DLSS 5 将于 2026 年秋季到来，官方称是 2018 年 real-time ray tracing 后图形领域最重要突破之一。关键点：

- 3D-guided neural rendering，不只是 upscaling/frame generation。
- 已有 DLSS 系列被集成到 750+ games。
- DLSS 5 将支持 4K real-time，基于游戏颜色、motion vectors 与 3D 场景语义生成更真实的 lighting/materials。
- 初始支持方包括 Bethesda、CAPCOM、NetEase、NCSOFT、Tencent、Ubisoft、Warner Bros. Games 等。

NVIDIA FY2026 Gaming revenue 160 亿美元，DLSS 5 对估值主线影响小于 data center，但对 RTX ecosystem、AI PC、creator workflows 和本地 agent 有粘性作用。

## 重要产品/技术的爆发判断与量产路线

| 产品/技术 | GTC 2026 关键事实 | 爆发原因 | 基准路线 | 乐观路线 | 超预期乐观路线 |
|---|---:|---|---|---|---|
| Vera Rubin NVL72 / Rubin GPU | 72 Rubin GPUs + 36 Vera CPUs；3.6EF NVFP4；1.6PB/s HBM4；260TB/s NVLink 6；2026 H2 partner availability | Blackwell 供给仍紧，agentic inference 与 MoE training 需要更高 perf/watt | 2026 H2 小批量/优先 hyperscaler；2027 大规模 ramp，接替 GB300 | 2026 Q4 即明显贡献收入，2027 成为主力 data center 增长引擎 | 供给、封装、HBM4、液冷均顺利，2027 出货接近 Blackwell ramp 速度，带动 NVIDIA data center 年化收入突破 3,500-4,000 亿美元 |
| Vera Rubin Ultra NVL576 / Kyber NVL1152 | NVL576 用 8 个 72-GPU racks 形成 576-GPU NVLink domain；Kyber 支持 NVL144/NVL1152；2028 Feynman 方向 | 超大模型、million-token context、MoE routing 需要更大 scale-up domain | 2027 旗舰训练/推理集群早期部署 | 2027 下半年成为 frontier labs 标配 | NVL576 变成 hyperscaler premium inference 标准单元，拉高整机 ASP 与网络/光模块需求 |
| Groq 3 LPX + Dynamo | 256 LPUs/rack；315PFLOPS；40PB/s SRAM bandwidth；640TB/s scale-up；2026 H2 | 低延迟 decode 与长上下文无法只靠 GPU；premium token ARPU 高 | 2026 H2 在 frontier labs/CSP 部署，2027 进入 premium inference tier | 与 Rubin 打包销售，2027 贡献数百亿美元级系统 revenue | LPX 成为 trillion-param、million-context 服务默认加速层，推理 revenue/GW 从 1,500 亿美元推向 3,000 亿美元 |
| Vera CPU / CPU rack | 88 Olympus cores；1.2TB/s LPDDR5X；256 CPUs/rack；22,500+ concurrent CPU environments；2x efficiency、50% faster | Agent sandbox、RL environment、工具调用和数据流水线把 CPU 重新变成瓶颈 | 2026 H2 随 NVL72 和 standalone CPU rack 出货 | AI CPU 从 x86 替换中拿到明显份额，云厂商开始按 agent environment 规划容量 | CPU rack 成为 AI factory 标配，CPU 份额从“配套”变为可单独定价的高毛利平台 |
| BlueField-4 STX / CMX | 5x tokens/sec；4x energy efficiency；2x ingestion；50Tb/s networking BW；16TB shared context/GPU；2026 H2 | KV cache 与 agent memory 成为推理效率上限 | 2026 H2 存储伙伴试点，2027 在长上下文推理集群扩散 | 2027 AI storage 从传统 external storage 中分化，STX 成为高端 AI factory 必配 | 大模型服务商普遍把 context memory tier 独立预算化，AI storage 年增速 >80% |
| Spectrum-X / Spectrum-6 / NVLink 6 / CPO | Spectrum-6 102T CPO，CX9 1600G；NVLink 6 3.6TB/s/GPU；CPO 5x optical power efficiency、10x resiliency | Scale-out/scale-up 网络决定 GPU 利用率，CPO 解决功耗与可靠性 | 800G/1.6T 与 NVLink 6 在 2026-2027 加速放量 | AI backend Ethernet 与 proprietary scale-up 同时增长，网络价值占 AI rack BOM 提升 | 光互连成为 AI factory 第二大稀缺资源，网络/光模块利润率短期扩张 |
| DSX / Omniverse DSX / power-flex software | DSX Max-Q、Flex、Exchange、Sim；固定电力下 30% more infra；目标解锁 100GW stranded grid power | 电力并网、冷却和施工已成为 AI factory 最大排队项 | 2026 进入设计/仿真/运营工具链，2027 转化为 reference design 与服务收入 | 主要 AI data center 设计均需要 DSX/Omniverse 兼容资产 | NVIDIA 对非芯片 capex 产生“软控制面”，把 token/watt 优化变成 recurring software/service |
| Dynamo 1.0 / TensorRT-LLM / inference OS | Open-source production-grade inference foundation；Blackwell inference performance 最高 7x；与 vLLM/SGLang/LMCache/LangChain 等集成 | 软件优化直接改善 token cost 和 GPU 利用率，影响现有数百万 GPU | 2026 作为免费开源底座扩大 NVIDIA stickiness | 2027 通过 Enterprise support、cloud service、AI factory management 间接变现 | 成为跨 GPU/LPU/STX 的事实标准，强化平台毛利率 |
| Physical AI Data Factory / Cosmos / GR00T / Alpamayo | Cosmos 3、GR00T N1.7、Alpamayo 1.5；数据生成、仿真、评估、OSMO orchestration | 机器人和 AV 最大瓶颈是数据、仿真、验证，不是单个模型 | 2026-2027 以云仿真/数据流水线收入为主，硬件慢 | 2027 形成制造、仓储、AV 的 reference workflow | 2027-2028 若 humanoid/robotaxi 进展超预期，边缘算力和仿真需求同增 |
| DRIVE Hyperion / Halos OS | BYD、Geely、Isuzu、Nissan 采用；Uber 28 markets by 2028；2027 H1 从 LA/SF 开始 | L4 需要统一 compute/sensor/safety/reference architecture | 2026-2027 仍以设计 win 和 L2+/L4 pilot 为主 | 2027 NVIDIA automotive revenue 恢复高增 | Robotaxi fleet 若监管顺利，2028 前形成显著软件/硬件 pull-through |
| DLSS 5 / RTX neural rendering | 2026 fall；750+ DLSS games 基础；支持 4K real-time neural rendering | 维持 RTX 消费生态和 creator pipeline，增强 AI PC 本地推理 | 2026-2027 推动 RTX 50/PRO refresh | 与 Adobe/creator workflow 结合带动 ProViz | 若 neural rendering 成为游戏标配，消费 GPU ASP 周期延长 |

## 市场规模、增速和利润率预测

说明：公开市场规模口径差异很大。下表采用“当前可观测收入/市场支出 + 2026 年公开预测 + 本报告情景推演”。利润率优先使用公开公司/行业毛利率；NVIDIA 未披露各产品细分毛利率，因此以公司 FY2026/Q4 毛利率和系统溢价方向估算。

| 方向 | 当前市场规模/收入基准 | 当前利润率 | 未来一年基准 | 乐观 | 超预期乐观 | 利润率走向 |
|---|---:|---:|---:|---:|---:|---|
| AI data center compute / accelerator systems | Deloitte：2026 AI data center capex 4,000-4,500 亿美元，其中 chips 2,500-3,000 亿美元；NVIDIA FY2026 data center revenue 1,937 亿美元 | NVIDIA FY2026 GM 71.1%，Q4 GM 75.0%；FY operating margin 约 60.4%，Q4 约 65.0% | 2027E AI chips 3,400-4,050 亿美元，+35%；NVIDIA DC 年收入 +35-45% | 4,000-4,800 亿美元，+55-70%；NVIDIA DC +55-65% | 4,750-5,700 亿美元，+80-100%；NVIDIA DC 年化 3,500-4,000 亿美元 | 基准 72-75%；乐观 75-77%；超预期 77-79%。系统级打包和稀缺支撑，HBM 成本和 ASIC 替代是压力 |
| AI inference infra / AI-optimized IaaS | Gartner：AI-optimized IaaS 2026 375 亿美元，其中 inference 206 亿美元；Deloitte：inference-optimized chips >500 亿美元 | 云推理服务毛利差异大，估计 35-55%；NVIDIA 硬件毛利参照 71-75% | AI-optimized IaaS 600 亿美元左右，inference 350 亿美元；inference chips 800 亿美元 | IaaS 700-750 亿美元；inference chips 950-1,050 亿美元 | IaaS 850 亿美元+；inference chips 1,200 亿美元+ | Token 单价下行，但 utilization、premium reasoning 和 LPX/Rubin revenue/GW 抬升；服务商毛利先承压后改善，硬件平台毛利稳中有升 |
| HBM4 / advanced AI memory | Gartner：2026 memory semiconductor 6,333 亿美元，2025 为 2,163 亿美元；AI semis 约占半导体 30%，即约 3,960 亿美元；DRAM 价格预计 +125% | HBM/DRAM 供应商高景气期 operating margin 可能 35-55%；价格比普通 DRAM 更强 | AI HBM/advanced memory 继续 +50-80%，HBM4 下半年成为 Rubin 关键瓶颈 | +90-120%，供应锁定到 2027 | +150%，若 HBM4e/Custom HBM 供不应求 | 2026-2027 上行，直到新增产能释放；NVIDIA 可转嫁一部分成本，但非 AI 需求受挤压 |
| AI networking / Ethernet / NVLink / CPO | IDC：2025 Ethernet switch revenue 551 亿美元，+31.5%；4Q25 data center Ethernet switch 99 亿美元，+63%；800G 占 2025 全年 Ethernet switch revenue 16.4% | 高端 switch/NIC silicon 55-70%，系统/设备 35-55%；CPO 初期溢价高 | 2027 Ethernet switch 700-750 亿美元；AI/high-speed portion +45-60% | 800-900 亿美元；1.6T/CPO 加速 | 1,000 亿美元+，网络成为 AI rack 第二大溢价层 | 高速端口/CPO/scale-up fabric 毛利上升；传统企业网络毛利被稀释 |
| AI-native storage / STX / context memory | IDC：2025 external enterprise storage systems 330 亿美元，+3.9%；Q4 97 亿美元，+5.5%；AI storage 子集本报告估算 80-120 亿美元 | 传统 enterprise storage GM 45-60%；AI storage/DPU 加速层估计 55-70% | AI storage 子集 +35-50%，约 110-180 亿美元 | +70-90%，约 140-230 亿美元 | +100-130%，约 200-280 亿美元 | STX/CMX 把存储从容量市场变为 token throughput 市场，毛利率有上修空间 |
| AI factory facilities / power / cooling / DSX ecosystem | Deloitte：2026 AI data center capex 4,000-4,500 亿美元，扣除 chips 后非芯片约 1,500 亿美元级；Gartner data center systems 2026 超 7,880 亿美元 | 设施/EPC 10-25%；电力/冷却设备 20-40%；软件/数字孪生 70-90% | 非芯片 AI factory capex +25-35% | +50-60% | +80%+，若并网和融资解决 | 工程利润率低但量大；DSX/软件层毛利高，NVIDIA 可能拿到高价值控制面 |
| Agent software / open models / NemoClaw / Nemotron | 直接收入尚小；关联到 enterprise AI software 与 AI IaaS；Gartner 预计 GenAI model development spending YoY more than double | 软件 gross margin 75-90%，但模型服务商 operating margin 分化 | Agent platform 进入企业试点，收入小但带动推理消耗 | Agent-as-a-service 带动推理 token +70-100% | OpenClaw/NemoClaw 成为企业 agent 标准栈之一 | 软件毛利高；主要价值以硬件利用率、云服务和 Enterprise support 间接体现 |
| Physical AI / robotics / simulation | Deloitte：工业机器人累计装机 2026 可达 550 万台；2026 工业用途 humanoid robots 约 15,000 台、2.1-2.7 亿美元；2030 工业机器人收入可达 210 亿美元 | 机器人硬件毛利早期低至 10-30%；仿真/数据软件 70%+ | Humanoid 2027E 3.2-4.1 亿美元；simulation/data factory +50% | Humanoid 4.2-5.4 亿美元；physical AI data infra +80% | Humanoid 6.3-8.1 亿美元；若工厂 pilot 复制，数据/仿真先翻倍 | 机器人整机利润率短期低；NVIDIA 更可能从 GPU/Jetson/Isaac/Cosmos/Omniverse 中获得高毛利 |
| Automotive / DRIVE Hyperion / robotaxi | NVIDIA FY2026 Automotive revenue 23 亿美元，+39%；Q4 6.04 亿美元 | NVIDIA automotive segment margin未披露，估计低于 data center、高于多数整车硬件，35-55% | FY2027 +20-30%，约 28-30 亿美元 | +45-60%，约 33-37 亿美元 | +80%+，若 L4 fleet 与 L2+ 上车同步加速 | 软件和安全 OS 占比提升后上行；车规周期长，短期收入滞后设计 win |
| Gaming / DLSS 5 / RTX AI PC | NVIDIA FY2026 Gaming revenue 160 亿美元，+41%；ProViz 32 亿美元，+70% | 消费 GPU/ProViz 估计 45-65%，低于 data center but healthy | Gaming +5-10%，ProViz +20-30% | Gaming +15%，ProViz +40% | DLSS 5 带动 RTX refresh，Gaming +25%、ProViz +60% | DLSS 5 提升平台粘性，毛利稳定；不是本轮最大利润弹性来源 |

## 三档情景下的核心产品成熟与量产路线

### 基准情景

- 2026 H2：Vera Rubin NVL72、Vera CPU、BlueField-4 STX、Groq 3 LPX 开始 partner availability，优先供给 hyperscaler、AI labs、NVIDIA Cloud Partners。
- 2026 Q4-2027 H1：GB300/Blackwell Ultra 与 Rubin 并行出货；Rubin 收入从小比例切入，供应链瓶颈主要在 HBM4、advanced packaging、液冷、电力接入。
- 2027：Rubin NVL72 成为新主力，LPX 用于 premium inference；STX 在长上下文 agent 服务中扩散；Dynamo 作为 inference OS 提高现有 Blackwell/Rubin 利用率。
- 2028：Feynman/Rosa、NVLink 8 CPO、Spectrum7 进入下一代路线。

### 乐观情景

- Rubin H2 2026 ramp 顺利，Blackwell 未发生明显订单切换空窗。
- LPX 被 frontier labs 证明在 premium reasoning 上有显著经济性，2027 成为高端推理机架标配。
- DSX 解决部分并网和冷却效率问题，固定 power budget 下 10-30% more compute 的案例可复制。
- NVIDIA data center revenue 2027 年维持 55-65% 增速，毛利率回到 75-77%。

### 超预期乐观情景

- 1GW AI factory 变成 hyperscaler 主流规划单元，客户按 revenue/GW 采购 Rubin + LPX + STX + Spectrum + DSX。
- HBM4、CPO、液冷和 power equipment 没有形成长期硬瓶颈，NVIDIA 机架级出货接近 Blackwell 速度。
- Long-context agents、coding agents、research agents 和 enterprise agents 的付费 token 使用量爆发，价格下降被用量和 premium tier 完全抵消。
- NVIDIA 2027 年化 data center revenue 进入 3,500-4,000 亿美元区间，公司 Q4/FY 毛利率维持高 70% 附近。

## 可能与当前市场认知相违背的洞见

### 洞见一：推理不是“便宜 ASIC 替代 GPU”，而是更复杂的异构系统

市场常把 inference 理解为低端、低毛利、容易被 ASIC 替代。GTC 2026 的信号相反：最赚钱的 inference 是长上下文、多轮 agent、premium reasoning，需要 GPU 的 HBM/attention、LPU 的低延迟 decode、STX 的 KV cache、Dynamo 的调度、CPU sandbox 和高速网络。NVIDIA 并没有否认 ASIC，而是把 Groq LPU 和 Marvell custom XPU 接入自己的 NVLink/AI factory 生态。

### 洞见二：真正的稀缺从 GPU 扩散到电力、内存、网络和施工

Gartner 预计 2026 半导体收入 1.3202 万亿美元，其中 memory 6,333 亿美元，DRAM 价格 +125%、NAND +234%；Deloitte 预计 2026 AI data center capex 4,000-4,500 亿美元，芯片外支出约 1,500 亿美元级。若只盯 GPU 交期，会漏掉电力并网、变压器、液冷、CPO、HBM4、enterprise storage 的投资弹性。

### 洞见三：NVIDIA 的“开放”并不削弱锁定，反而扩大收费边界

Nemotron、NemoClaw、OpenShell、Dynamo、CUDA-Q、Cosmos、GR00T、Alpamayo 都强调 open/open-source/open model。但这些开放层的目标是让更多 workloads 跑到 NVIDIA AI factory 上。开放的是入口，闭环的是工具链、GPU/LPU/DPU/NIC/存储、Enterprise support、cloud integration 和参考架构。

### 洞见四：Robotics 叙事大，2026 收入小，先爆发的是数据工厂和仿真

Humanoid robot 2026 年工业用途市场仅约 2.1-2.7 亿美元，远小于数据中心单季收入；NVIDIA automotive FY2026 也只有 23 亿美元。但 Physical AI Data Factory、Cosmos/Isaac/Omniverse、synthetic data、simulation validation 会先吃到预算，因为它们是机器人/AV 真正量产前的必要投入。

### 洞见五：1 万亿美元口径既是强需求信号，也是对 ROI 的高压测试

如果 Blackwell + Rubin 到 2027 年确有至少 1 万亿美元 revenue/order opportunity，那么客户需要用 AI 产品、云推理、enterprise agents、广告/搜索/软件开发效率、机器人/AV 等现金流来消化。J.P. Morgan 等机构对 AI capex ROI 的担忧仍成立：token 需求必须持续爆发，否则 2027-2028 可能出现局部过剩和价格压力。

### 洞见六：毛利率风险不在“GPU 价格自然下跌”，而在系统 BOM 与客户议价结构

HBM/DRAM 价格上行、advanced packaging、liquid cooling、CPO 等会推高成本；但 NVIDIA 若按机架/POD/AI factory 打包出售，且软件提高 goodput，可维持高毛利。真正风险是 hyperscaler custom silicon 在内部 workload 上替代一部分通用 GPU，并通过 NVLink Fusion 争取更多议价权。

## 投资/产业跟踪指标

1. Rubin H2 2026 出货节奏：NVL72 量产、HBM4 供应、CoWoS/advanced packaging、液冷 rack 交付。
2. LPX 客户案例：是否有公开 benchmark 证明 premium reasoning 的 revenue/GW 或 token cost 显著优于纯 GPU。
3. STX/CMX 真实采用：Mistral、CoreWeave、OCI、Nebius 等是否在长上下文服务中部署。
4. Dynamo 生态：vLLM/SGLang/LMCache/LangChain 等是否把 Dynamo 模块作为默认高性能路径。
5. DSX 落地：Nscale/Caterpillar、Vertiv OneCore Rubin DSX、Switch EVO 等是否形成可复制项目。
6. 800G/1.6T/CPO 出货：IDC/Dell'Oro 口径中 AI backend Ethernet 与 CPO 占比。
7. HBM4/HBM4e ASP 和供给锁定：SK hynix、Samsung、Micron 对 2026-2027 的预售、capex 和良率。
8. Hyperscaler capex revision：Amazon、Microsoft、Google、Meta、Oracle 是否继续上调 2026/2027 capex。
9. AI revenue/payback：OpenAI、Anthropic、Perplexity、Cursor、ServiceNow、Adobe 等是否证明 agent/token 需求可覆盖计算成本。
10. 监管与地缘：China data center compute revenue 是否恢复；出口管制、AI chip local substitutes、sovereign AI 订单变化。

## 主要来源

- NVIDIA GTC 2026 press kit：[GTC 2026 News](https://nvidianews.nvidia.com/online-press-kit/gtc-2026-news)
- NVIDIA GTC 2026 会议规模与议程：[NVIDIA CEO Jensen Huang and Global Technology Leaders to Showcase Age of AI at GTC 2026](https://nvidianews.nvidia.com/news/nvidia-ceo-jensen-huang-and-global-technology-leaders-to-showcase-age-of-ai-at-gtc-2026)
- NVIDIA keynote/IR 页面：[GTC 2026 Keynote](https://investor.nvidia.com/events-and-presentations/events-and-presentations/event-details/2026/GTC-2026-Keynote-2026-HhZOL0SIV4/default.aspx)
- Vera Rubin platform：[NVIDIA Vera Rubin Opens Agentic AI Frontier](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)
- Vera Rubin technical blog：[NVIDIA Vera Rubin POD: Seven Chips, Five Rack-Scale Systems, One AI Supercomputer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- Vera CPU：[NVIDIA Launches Vera CPU, Purpose-Built for Agentic AI](https://nvidianews.nvidia.com/news/nvidia-launches-vera-cpu-purpose-built-for-agentic-ai)
- BlueField-4 STX：[NVIDIA Launches BlueField-4 STX Storage Architecture With Broad Industry Adoption](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption)
- Dynamo 1.0：[NVIDIA Enters Production With Dynamo, the Broadly Adopted Inference Operating System for AI Factories](https://nvidianews.nvidia.com/news/dynamo-1-0)
- DSX/Omniverse DSX：[NVIDIA Releases Vera Rubin DSX AI Factory Reference Design and Omniverse DSX Digital Twin Blueprint](https://nvidianews.nvidia.com/news/nvidia-releases-vera-rubin-dsx-ai-factory-reference-design-and-omniverse-dsx-digital-twin-blueprint-with-broad-industry-support)
- Marvell/NVLink Fusion：[NVIDIA AI Ecosystem Expands as Marvell Joins Forces Through NVLink Fusion](https://nvidianews.nvidia.com/news/nvidia-ai-ecosystem-expands-as-marvell-joins-forces-through-nvlink-fusion)
- Robotics/Physical AI：[NVIDIA and Global Robotics Leaders Take Physical AI to the Real World](https://nvidianews.nvidia.com/news/nvidia-and-global-robotics-leaders-take-physical-ai-to-the-real-world)
- Physical AI Data Factory：[NVIDIA Announces Open Physical AI Data Factory Blueprint](https://nvidianews.nvidia.com/news/nvidia-announces-open-physical-ai-data-factory-blueprint-to-accelerate-robotics-vision-ai-agents-and-autonomous-vehicle-development)
- DRIVE Hyperion：[BYD, Geely, Isuzu and Nissan Adopt NVIDIA DRIVE Hyperion for Level 4 Vehicles](https://nvidianews.nvidia.com/news/drive-hyperion-level-4)
- AI-RAN/edge：[NVIDIA, T-Mobile and Partners Integrate Physical AI Applications on AI-RAN-Ready Infrastructure](https://nvidianews.nvidia.com/news/nvidia-t-mobile-and-partners-integrate-physical-ai-applications-on-ai-ran-ready-infrastructure)
- DLSS 5：[NVIDIA DLSS 5 Delivers AI-Powered Breakthrough in Visual Fidelity for Games](https://nvidianews.nvidia.com/news/nvidia-dlss-5-delivers-ai-powered-breakthrough-in-visual-fidelity-for-games)
- NVIDIA FY2026 财报：[NVIDIA Announces Financial Results for Fourth Quarter and Fiscal 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)
- 1 万亿美元口径媒体记录：[TechCrunch](https://techcrunch.com/2026/03/16/jensen-just-put-nvidias-blackwell-and-vera-rubin-sales-projections-into-the-1-trillion-stratosphere/)、[Axios](https://www.axios.com/2026/03/16/nvidia-ceo-jensen-huang-nvidia-gtc)、[Reuters syndication](https://whbl.com/2026/03/16/nvidia-ceo-set-to-reveal-new-chips-and-software-at-ai-megaconference-gtc/)
- Deloitte AI compute / data center capex：[Why AI’s next phase will likely demand more computational power, not less](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html)
- Gartner AI-optimized IaaS：[AI-Optimized IaaS spending and inference workloads](https://www.gartner.com/en/newsroom/press-releases/2025-10-15-gartner-says-artificial-intelligence-optimized-iaas-is-poised-to-become-the-next-growth-engine-for-artificial-intelligence-infrastructure)
- Gartner data center systems：[Worldwide IT Spending 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-22-gartner-forecasts-worldwide-it-spending-to-grow-13-point-5-percent-in-2026-totaling-6-point-31-trillion-dollars)
- Gartner semiconductor/memory：[Worldwide Semiconductor Revenue to Exceed $1.3 Trillion in 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- IDC Ethernet switch：[Datacenter segment surges 60%+ in Q4 as AI workloads expand](https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/)
- Deloitte robotics：[AI for industrial robotics, humanoid robots, and drones](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/ai-for-robots-drones.html)
- IDC enterprise storage via public summary：[Enterprise Storage Systems Market Insights](https://www.idc.com/promo/enterprise-storage-systems/)
# OCP EMEA Summit 2026 高密度调研：AI 数据中心从“买 GPU”进入“重构电力、散热、互连、标准”的阶段

> 截至 2026-05-08。报告只使用公开网页、官方议程、公开 PPTX/链接和公开市场资料，未参考项目内文件。  
> 会议：2026 OCP EMEA Summit，2026-04-29 至 2026-04-30，Barcelona, Spain。官方说明称本届重点是 EMEA 区域的数据中心可持续性、能效、热复用，以及 OCP 认可设备的区域部署。

## 0. 信息源与口径

- 官方入口：[OCP EMEA Summit 2026](https://www.opencompute.org/summit/emea-summit)，[官方会务 App](https://2026ocpemea.fnvirtual.app/)，[Full Schedule](https://2026ocpemea.fnvirtual.app/a/schedule)。
- 解析官方会务 App 的公开嵌入数据：208 个 session、303 位 speaker、34 个 track、157 条公开 `PresentationMediaUpload`，其中约 142 份 PPTX 可直接提取文本。
- 高频一手材料：IDC/OCP 采用与支出报告、Open Data Center for AI、LVDC/HVDC、冷板/浸没/UQD/TCO、UALink/ESUN/SUE-T、800G/1.6T、硅光/OCS/多芯光纤、FCSA/chiplet、Caliptra/LOCK/SOLID/openSFI。
- 市场规模使用公开市场资料校准：TrendForce、Cignal AI、Grand View Research、BCC Research、Dell'Oro 经媒体转述、OCP/IDC 会场材料。以下预测为研究估算，不是投资建议。

## 1. 一页结论

OCP EMEA 2026 的主线非常清楚：AI 数据中心的瓶颈已经从“有没有 GPU”扩展为“电力能否到位、热能否带走、互连能否保持 GPU 利用率、供应链能否多厂商化、固件和硅根信任能否被审计”。会议不像传统服务器会议，更像 AI 工厂基础设施标准化会议。

最重要的变化是六个：

- **开放 AI 数据中心成为顶层项目**：Google、Meta、AMD、NVIDIA、Microsoft 等推动 Open Data Center for AI。会场材料给出 Open DC Spec 路线：2026-05 25% 完成、2026-06 50%、2026-07 75%、2026-08 社区反馈、2026-09 OCP Steering Committee 批准与网站发布、2026-10 OCP Global Summit 展示。
- **机架功率从 40-100 kW 直接跳到 500 kW 至 1 MW 叙事**：Open DC 材料称 Top 5 超算约每年 1-2 台、今天 400 kW/rack；AI supercomputers 正向每周约 1 套推进，600 kW 在路上，目标路径到 1 MW。Schneider/Rittal keynote 均强调超过 500 kW/rack 已不再是理论。
- **电力架构转向 HVDC/LVDC 和电网协同**：ORv3/HPR 从 33 kW、72 kW 走向 100 kW/160 kW HVDC power shelf；800 VDC、700/1400 V、750/1500 V 的互操作和保护问题成为核心议题。电力不再是设施后端，而是 AI 系统架构的一部分。
- **冷板先爆发，浸没进入标准化深水区**：Promersion/OCP 材料称 2025 年 cold plate 市场突破 50 亿美元，immersion 约 8 亿美元；冷板、UQDv2、CDU/TCO 工具在 2026 年明显成熟，浸没仍有信号完整性、材料兼容、供电安全和运维标准问题。
- **AI 网络从 scale-out 进入 scale-up/scale-across 多层体系**：UALink 2.0 规格完成，800 Gbps port 可拆为 1x800G、2x400G、4x200G；ESUN 1.0 已获批，SUE-T 提出 scale-up Ethernet transport。800G 是当前主战场，1.6T 是 2026-2027 的新增长。
- **开放硅、开放固件、开放安全从“理念”变成采购门槛**：FCSA 1.0.0 2026-02 发布；Caliptra 2.2 目标 Q4 2026，2027 进入 NEXT；OCP S.O.L.I.D. 要求 2026-10-01 起进入 OCP S.A.F.E. long-form report；openSFI 0.5 正在推进并目标 OCP Global 0.7。

## 2. 重点与相较此前市场/技术的转折

### 2.1 Open Data Center for AI：从服务器标准变成“AI 工厂接口标准”

IDC 会场材料给出一个关键基准：OCP-recognized IT infrastructure and solutions 支出将从 2025 年 1320 亿美元增长到 2029 年 2950 亿美元，CAGR 22.2%；hyperscalers 当前占 OCP-specified infrastructure 超过 60%。这意味着 OCP 不是边缘开源硬件兴趣小组，而正在变成 AI 基础设施采购和设计语言。

Open DC for AI 的核心接口包括：spatial/rack form factor、network、power、cooling、power quality、security、telemetry。Open DC Spec v0.5、Project Deschutes、CDU Spec v1.0、Mt. Diablo +/-400VDC Sidecar Spec v0.7、Clean Backup Spec v0.3 都被列入基础设施组件标准化对象。

相较之前：过去 OCP 主要围绕服务器、机架、供电、BMC 等模块化规范；今年明显转向“从园区电网到 rack 到 xPU fabric 的端到端 AI data center standard”。

### 2.2 电力：800 VDC/LVDC 是本届最硬的增量方向

会议直接出现多个强数字：

- HPRv1：33 kW shelf，5.5 kW PSU，峰值效率 97.5%，满载效率 96.5%。
- HPRv2：72 kW shelf，12 kW PSU，50 Vdc 输出，1470 A nominal，峰值 97.5%，满载 96.5%。
- HPRv4 HVDC：100 kW/160 kW 讨论，输入 ±380 Vdc 至 ±420 Vdc，18 kW rectifier，50 Vdc 输出，367 A，峰值效率 98.5%，满载 97.5%。
- LVDC workstream 明确排除 >1500 VDC 的 MVDC，把当前工作聚焦在低压直流、800 VDC/700 VDC/750/1500 VDC 的互操作、安全保护、极性/接地、EMC、控制运行。
- 800 V 设备若设计为可在 750 V 下运行，可兼容 700/1400 V TN-S 系统，有利于完整使用 1500 V 低压 DC 范围。

关键变化：电力系统开始被当成“动态负载网络”设计。HPRv2 72 kW 的 abnormal voltage ride-through 演示覆盖 0.8 pu 3s、0.75 pu 3s、0.65 pu 2s、0.5 pu 0.5s、0.45 pu 0.3s 等电网暂降要求，目标 fast recovery <500 ms。AI 负载的高 slew rate 和电网稳定性已经进入 PSU 和 BBU 固件开发。

### 2.3 散热：冷板量产，浸没标准化，TCO 从“散热成本”变成“上架速度成本”

Cooling track 的关键数字：

- Promersion/OCP：2024 Q3 cold plate inflection 由 NVIDIA GPU 推动；cold plate 市场相较 2023 年约四倍增长；2025 年 cold plate 突破 50 亿美元；immersion 达 8 亿美元。
- UQDv2 draft 在 2026-04-20 技术内容冻结，UQD08 hybrid 测试中 spec max dP 1.7 psi，3 家样品约 1.0 psi ±0.2；插拔力 spec max 30 lbf，样品约 22 lbf ±4。
- Coldplate Base Specification 目标是建立 single-phase D2C cold plate 的事实行业基线，解决定义不一致、验证碎片化、供应商评价不可比的问题。
- TCO Tool v1.3 发布，Excel、无宏、无隐藏逻辑，可比较 air、DLC、RDHX、side-car、L2L CDU 等架构。材料给出例子：若电价 0.1 EUR/kWh，在 L3 rPDU outlet 计量，巴黎 breakeven 0.352 EUR/kWh、巴塞罗那 0.354 EUR/kWh，巴塞罗那 breakeven hosting rate 每年高约 879,382 欧元。
- Modular TCS panel 给出“100 kW to 1 MW per rack”路线；一次 100 MW、600 racks 部署中，若每 rack 成本 500 万美元、收入 7500 万美元，延误 1 周可能损失 2 亿至 4 亿美元业务。

关键变化：冷却不再只看 PUE，而看“time to power/time to deployment”。液冷管路、冲洗、过滤、盲插快接、CDU 位置和运维流程的标准化，直接影响收入确认速度。

### 2.4 网络与互连：Ethernet 正进入 scale-up，UALink/ESUN/SUE-T 并行

会议材料显示 AI 网络被拆为三层：

- Scale-up：single xPU node，约 8 至 1k xPUs，约 12 kW 至 1 MW，HBM bandwidth per xPU 约 100 Tb/s。
- Scale-out：single data center cluster，约 50k m²、约 100k xPUs、约 180 MW。
- Scale-across：multiple data centers，约 5 km²、1M+ xPUs、1+ GW。

UALink 材料强调 800 Gbps ports 可做 1x800G、2x400G 或 4x200G，目标是数百 accelerator、最多 1K 的 pod 内低延迟 load/store/atomic 共享内存。ESUN 1.0 已批准，166 名成员，核心是 Ethernet scale-up network 的 operator/end-user requirements、低头开销 header、LLR、PFC/CBFC、lossless 和 link reliability。

Celestica/Hedgehog/OCP Open Cluster Design 给出 2026-2027 路线：2026 H1 参考架构草案和 artifacts，2026 H1 1.6T architecture revision，2026 H2 扩展 xPU 支持，2027 继续开放集群设计。其 open fabric 支持 SONiC、1.6T Celestica DS6000、800G DS5000、Day 0/1/2 lifecycle automation。

关键变化：过去市场把 AI 网络理解为 InfiniBand vs Ethernet；本届更像“scale-up memory semantics + scale-out Ethernet + scale-across optics”的多协议现实。Ethernet 不只做大二层/三层网络，正在被压入 GPU 近端。

### 2.5 光互连：800G/1.6T 是 2026 主线，OCS/CPO/MCF 是下一层变化

TrendForce 认为 800G 及以上光模块出货占比将从 2024 年 19.5% 提升到 2026 年超过 60%；全球光收发模块出货量从 2023 年 2650 万只到 2026 年超过 9200 万只。Google Ironwood TPU 相关 800G+ 光模块需求预计超过 600 万只。

会议材料中的关键事实：

- iPronics 32x32 silicon photonic OCS 已向客户出货，1024 optical interconnects，400G LWDM 下 BER 1e-5 和 1e-7 演示，sub-ms reconfiguration，系统功耗 30 W + 0.78 W/active channel，宣称至少较传统 switch 降低 10x 功耗。
- TrendForce 给的 Google Apollo OCS 对比：单台 OCS switch 约 100 W，传统 switch 约 3000 W，功耗下降约 95%。
- imec 材料演示 400G/lane CPO：212.5 GBaud PAM4，HD-FEC threshold 6.25% OH，net 400 Gbps/lane；若 400G/lane CPO 能达 5 pJ/bit，光学部分总功耗约 1.25 kW。
- Sumitomo 多芯光纤材料：从 H200 约 320 fibers/rack 到 GB200/NVL72 约 1440 strands，再到 Rubin/NVL144 约 2880 strands；4-core MCF 示例中 6912 芯 cable 外径从单芯约 37 mm 降至 4-core 约 13 mm，截面积 1075 mm² 至 133 mm²，节省 60-80% 管道空间。

关键变化：光模块从“网络设备 BOM”变成 AI 产能节奏瓶颈，价值从组装转向硅光 wafer process、2.5D/3D packaging、electro-optical test 和 CPO 平台。

### 2.6 Chiplet：FCSA 让开放 chiplet 从 PHY 走向系统架构

OCP 在 2026-02 发布 FCSA。Arm/OCP 说 FCSA 是 vendor-neutral、ISA-neutral 的 chiplet specification，目标是把 monolithic SoC 拆成可互操作 chiplets，覆盖 memory、I/O、accelerator 等。

会场材料的关键数字：

- Qualcomm 材料：D2D interconnect silicon-proven Gen1 24 Gbps、Gen2 36 Gbps、Gen3 64 Gbps；off-chip IO reference 中 PCIe7/8 走 128G 至 248G，UALink/ESUN/Ethernet 走 200G 至 400G。
- Arm FCSA 材料：FCSA 1.0.0 于 2026-02 发布，ACSA 1.0.0 于 2026-03 发布，目标 2026-10 发布 FCSA 1.1.0。
- Cadence/Arm 材料：UCIe 1.1 32Gx16、PCIe 6.0 x8、CXL 3.2 Type-2、DDR5-9600 memory subsystem 被放入 pre-silicon verification flow。

关键变化：此前 chiplet 标准更多停在 UCIe/BoW 等物理互连；今年的 OCP Open Chiplet Economy 强调 system-level interoperability：management、security、firmware、software abstraction、threat model 和 verification。

### 2.7 安全与固件：供应链信任成为欧洲 AI 基础设施的核心接口

Microsoft keynote 将 EU Data Boundary、Caliptra、OCP S.A.F.E.、Confidential Computing 放在“Scaling Trusted AI Infrastructure”中。EMEA 的 sovereign cloud 讨论也强调真正主权不是 data residency，而是 supply chain、firmware、lifecycle、auditability 和 vendor swap。

关键一手事实：

- Caliptra roadmap：2.0/2.1 覆盖 RTL、ROM、FW；加入 NIST PQC ML-DSA/Dilithium 与 ML-KEM/Kyber；Caliptra 2.2 目标 Q4 2026；NEXT 在 2027，包含 security hardening、area/power reduction、generic key derivation/distribution 等。
- OCP L.O.C.K.：1.0 已于 2025-09 发布，1.1 计划 2026-05，KMB ROM/FW 完成，MCU reference implementation 进行中，新增 attested crypto-erasure 和 epoch key purge。
- OCP S.O.L.I.D.：面向 datacenter hardware/firmware security requirements，约 80% 覆盖 hyperscaler 重复采购要求；2026-10-01 起 OCP S.A.F.E. long-form report 必须包含 S.O.L.I.D. requirement analysis。
- openSFI：从 2025 Q1 启动 v0.3，到 2025 Q3 发布 v0.3，2026 推进 v0.5；目标是 vendor-agnostic interface between host firmware and silicon firmware，减少 host firmware 对 silicon implementation 的硬耦合。
- Arm SBMR：Arm SystemReady band 已有 56 servers、18 partners，SBMR 3.0 ALP 将在 EMEA Summit 后贡献到 OCP HW Management Project。

## 3. 哪些产品和技术会爆发：成熟与量产路线三情景

| 方向 | 会议证据 | 基准口径 | 乐观口径 | 超预期乐观口径 |
|---|---|---|---|---|
| Open Data Center for AI | Open DC Spec 2026-09 目标发布；接口覆盖 rack/network/power/cooling/security/telemetry | 2026 成为 RFP/设计参考；2027 进入 hyperscaler 与 OCP Ready v2 colocation 项目 | 2027 上半年成为大型 AI campus 的标准接口，带动 CDU、HVDC、telemetry 联合采购 | 2026 Q4 起被 Microsoft/Google/Meta 级项目写入采购条款，2027 形成事实标准 |
| 800 VDC/LVDC/HVDC rack power | 72 kW HPRv2、100/160 kW HPRv4，98.5% peak efficiency，800V/750/1500V 互操作 | 2026 以 sidecar、pilot、new-build 为主；2027 小批量 AI factory 部署 | 2027 大型 AI campus 新建电力架构优先考虑 HVDC/LVDC，rack power shelf 和 BBU 放量 | 电网 ride-through 和 power flexibility 要求加速采用，2027 800 VDC 成为 500 kW+ rack 默认选项 |
| Cold plate/D2C liquid cooling | 2025 cold plate >50 亿美元，UQDv2 内容冻结，coldplate base spec 推进 | 2026 GB300/Rubin 新机架标配冷板；2027 企业/colo 进入规模迁移 | 2026 下半年冷板、CDU、manifold 供应链紧张，毛利提升 | 500 kW+ rack 加速，冷板与 RDHX/door HX 组合成为 100-300 kW rack 的默认工程方案 |
| Immersion cooling | Immersion 2025 约 8 亿美元，15 个 active workstreams，1467 unique participants | 2026-2027 仍在 neocloud、edge、改造项目中分散采用 | 单相浸没 ORv3、power distribution、ITE guidelines 完成后，2027 部分 AI neocloud 批量采用 | 若 1 kW+ devices 与水资源限制同时加剧，浸没作为差异化方案在 2027 进入多区域标杆项目 |
| UALink/ESUN/SUE-T scale-up interconnect | UALink 2.0 complete，IP/TME ready；ESUN 1.0 approved；SUE-T 定义 scale-up transport | 2026 design-in，2027 第一批多厂商 accelerator pod | 2027 UALink switch/accelerator 开始生产验证，ESUN 用于 Ethernet scale-up 标准化 | Ethernet 在 scale-up 取得突破，up to 2048 XPUs、<1 us RTT 的架构成为推理集群关键卖点 |
| 800G/1.6T switching and optics | 800G+ optical share 2026 >60%；1.6T architecture revision 2026 H1/H2 | 2026 800G 主流，1.6T 小批量；2027 1.6T 放量 | 2026 1.6T 在 spine/scale-across 先放量，光模块紧缺 | 1.6T 端口和 CPO/OCS 带动交换芯片、DSP、硅光封装一起涨价 |
| Silicon photonics OCS/CPO | OCS 32x32 shipping；100 W OCS vs 3000 W traditional；400G/lane CPO 演示 | 2026 OCS pilot；2027 在 Google 类架构中扩大 | 2027 OCS + pluggable 1.6T 成为 scale-across/scale-up 重要形态 | 2026-2027 出现“OCS 绕过电交换”的标杆设计，显著压缩传统电交换预算 |
| Multi-core fiber | 4-core MCF 节省 60-80% duct space，NVL72 到 NVL288 光纤数量指数级增加 | 2026 布线规划采用 MCF 试点；2027 高纤芯 trunk 放量 | MCF/FIFO 与 MCF-native transceiver 配套，2027 大型 AI campus 批量使用 | CPO to ASIC 与 MCF 打通，光纤基础设施成为 AI campus 关键瓶颈投资 |
| Open chiplet/FCSA | FCSA 1.0 2026-02；FCSA 1.1 目标 2026-10；UCIe/CXL/PCIe 进入验证 | 2026 标准设计和验证工具成熟，2027 被部分 ASIC RFP 引用 | 2027 出现可复用 accelerator/IO/memory chiplet 目录 | 2028 前形成开放 chiplet marketplace，降低小厂/欧洲自研 AI silicon 门槛 |
| Caliptra/LOCK/SOLID/openSFI | Caliptra 2.2 Q4 2026；LOCK 1.1 2026-05；SOLID 2026-10 进入 SAFE long-form | 2026-2027 成为 hyperscaler/security RFP 加分项 | 欧洲 sovereign cloud 把 Caliptra/SOLID/openSFI 写入合规 baseline | 供应链风险与 CRA 触发安全审计刚需，固件/硅根信任服务利润率提升 |

## 4. 重要产品和技术的市场规模、未来一年增速、利润率

> 口径说明：当前规模优先采用 2025A 或 2026E run-rate。未来一年指从 2026 年中至 2027 年中附近的增速估计。利润率为产业链粗口径，硬件供应商、ODM、IP、系统集成之间差异很大。

| 方向 | 当前市场规模 | 未来一年增速：基准 / 乐观 / 超预期 | 当前利润率与趋势 |
|---|---:|---:|---|
| OCP-recognized IT infrastructure | 2025 年约 1320 亿美元，IDC 会场材料预测 2029 年 2950 亿美元，CAGR 22.2% | +22% / +28% / +35% | 混合毛利约 10-25%。服务器/机柜集成偏低，电力/冷却/管理软件更高。趋势：AI 设施瓶颈让非 GPU 层议价能力提升 |
| AI server/rack-scale GPU/ASIC systems | TrendForce：AI server 2025 约 2980 亿美元；2026 收入再增 30%+，约 3900 亿美元级 | +25-35% / +40% / +50% | GPU/ASIC 硅片与系统平台高，ODM rack integration 低；混合毛利约 15-25%。HBM/先进封装紧缺维持上游高毛利，整机价格压力上升 |
| Data center power infrastructure，含 UPS、busway、PDU、rack power、HVDC/LVDC | GVR：data center power 2025 约 227.7 亿美元；BCC：power infrastructure 2024 年 287 亿美元，2030 年 473 亿美元 | +12-18% / +22-25% / +30% | 电力电子、switchgear、busway 毛利约 25-40%，项目集成较低。趋势：800 VDC、ride-through、BBU/ESS 使高端产品毛利上行 |
| Liquid cooling，cold plate、CDU、manifold、immersion | GVR：2025 年 data center liquid cooling 约 66.5 亿美元；OCP/Promersion：2025 cold plate >50 亿美元、immersion 约 8 亿美元 | +25-30% / +40% / +60% | 冷板/CDU/快接/服务毛利约 25-45%。短期供需紧张和标准化不足推高毛利，2027 后随多厂商化可能分化 |
| High-speed optics，800G/1.6T、OCS、CPO、DSP | Cignal AI：2025 optical components 近 250 亿美元，其中 datacom >180 亿美元、coherent 近 60 亿美元；TrendForce：2026 transceiver >9200 万只，800G+ 占比 >60% | +20-30% / +35-45% / +50%+ | 标准 pluggable 毛利 15-30%，硅光/CPO/OCS/高端 DSP 可达 35-55%。趋势：高端上行、标准模块受中国供应链压价 |
| AI Ethernet/data center switch、NIC/DPU、cables | 数据中心交换机 2025 约 150 亿美元级；Dell'Oro 称 2025 AI back-end Ethernet switch sales 增长超过 3 倍，800G ports 三年超 2000 万 | +30-40% / +50% / +70% | Branded switch 毛利 40-65%，whitebox 10-20%，merchant silicon/NIC 更高。趋势：1.6T 和 scale-up Ethernet 提高 silicon/NIC 价值 |
| Chiplet/advanced packaging/open chiplet ecosystem | Chiplet 市场 2025 约 130 亿美元级，open chiplet direct revenue 仍小但附着于 AI ASIC/HPC | +30-45% / +50% / +70% | IP/EDA 毛利 70%+，advanced packaging 20-35%，custom silicon 项目利润高度集中。趋势：FCSA 降低 vendor lock-in，但初期服务/IP 溢价高 |
| Silicon root-of-trust、secure firmware、attestation、SAFE audit | 直接市场可能只有数十亿或更小，但附着在 3000 亿美元级 AI server 和 sovereign cloud 采购上 | +30% / +50% / +80% | IP/审计/安全服务毛利高，硬件 RoT 单价低但 attach rate 高。趋势：欧洲 CRA、sovereign cloud 和 hyperscaler RFP 会把它变成准入条件 |
| Data center storage for AI cold/archive tier | 传统 enterprise storage/HDD/NAND 是百亿美元级；Cerabyte 类“零能耗保留”仍是早期 | +5-15% / +20% / +35% | HDD/SSD 毛利受周期影响大；新型归档介质若验证成功毛利高。趋势：AI 数据保留、训练数据 lineage、合规归档扩大需求 |

## 5. 与当前市场共识相违背或容易被低估的洞见

### 5.1 不是只有 GPU 缺，真正卡量产的是“power to rack”和“time to power”

市场常把 AI capex 直接等同 GPU。OCP 会场却反复强调：超过 500 kW/rack 已经临近，100 MW 级部署延误一周可对应 2-4 亿美元业务损失。电网暂降穿越、BBU 协同、800 VDC 电压带、现场冲洗和过滤，都是 GPU 之前的“产能闸门”。

### 5.2 冷板最先商业爆发，浸没不会立刻替代冷板

会议数据支持 cold plate 先爆：2025 年 >50 亿美元，immersion 约 8 亿美元。浸没的问题不是热性能，而是电气信号完整性、材料兼容、power distribution、ITE guidelines、清洗/维护/保险/合规。超预期情景需要 1 kW+ device、供水限制和新建 AI neocloud 三个条件同时出现。

### 5.3 Ethernet 不是简单替代 InfiniBand，而是在吞掉更多层级

ESUN、SUE-T 与 UALink 的共存说明 scale-up 不是单一协议赢家通吃。Ethernet 的优势是生态、运维、供应商多样性；UALink 的优势是 memory semantics 和低延迟。更可能出现的是：rack/pod 内 UALink 或 ESUN，cluster 内 800G/1.6T Ethernet，campus 间 coherent/OCS/optical fabric。

### 5.4 光互连的利润池会从模块组装前移到硅光、封装和测试

TrendForce 明确指出 SiPh/CPO 重点在 wafer-level process 和 advanced co-packaging，而不是传统模块组装。台湾/东南亚 OSAT、PIC process、server ODM 的一体化能力会成为新入口。传统低毛利 transceiver 供应商可能不一定是最大赢家。

### 5.5 主权云不是“在本国机房跑 hyperscaler stack”

ScaleUp Germany 材料直说：很多所谓 sovereign cloud 只是美国 hyperscaler stack 在德国数据中心，属于 data residency，不是真主权。真正主权要求控制 supply chain、firmware、lifecycle、整栈可审计、可换供应商。这会放大 OCP、open firmware、Caliptra、SBMR、openSFI 的欧洲价值。

### 5.6 循环利用从 ESG 叙事变成供应链对冲

Meta circularity 材料称 2026 Big-5 hyperscaler data-center capex 6000 亿美元+，AI 占 72%；DDR5 16Gb spot price 在 Q1 至 Q4 2025 从 6.84 美元涨到 27.20 美元，涨幅 298%；server lifecycle carbon 中 78% 在制造环节，单台服务器每次 reuse 可避免约 1500 kg CO2e。旧硬件和再制造 OCP rack 的价值将不仅是碳，而是缩短 lead time 和对冲内存/电源供应。

### 5.7 安全合规的商业价值可能被低估

Caliptra、OCP L.O.C.K.、OCP S.O.L.I.D.、openSFI、SBMR 都在 2026 出现明确版本和审计路径。欧洲 CRA、云主权、硬件供应链风险会把这些从“开源基础组件”推到采购 gating factor。直接收入小，但它能决定服务器、SSD、GPU、NIC、BMC、firmware 是否进入高端客户 RFP。

## 6. 核心材料索引

会议与市场源：

- [OCP EMEA Summit 2026 官方页](https://www.opencompute.org/summit/emea-summit)
- [OCP EMEA Summit 2026 会务 App](https://2026ocpemea.fnvirtual.app/)
- [OCP Full Schedule](https://2026ocpemea.fnvirtual.app/a/schedule)
- [TrendForce：AI server 2025 产业价值 2980 亿美元](https://www.trendforce.com/presscenter/news/20250106-12433.html)
- [TrendForce：2026 AI server 出货 +28% 以上，ASIC AI server 约 27.8%](https://www.trendforce.com/presscenter/news/20260120-12887.html)
- [TrendForce：八大 CSP 2026 capex 超 5200 亿美元](https://www.trendforce.com/presscenter/news/20251013-12741.html)
- [TrendForce：800G+ 光模块 2026 占比超过 60%](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- [DRAMeXchange/TrendForce：光收发模块 2026 超 9200 万只](https://www.dramexchange.com/WeeklyResearch/Post/2/12686.html)
- [Cignal AI：2025 optical components 近 250 亿美元](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)
- [OCP：FCSA 公开发布](https://www.opencompute.org/index.php/blog/ocp-open-chiplet-economy-is-leading-the-next-wave-of-ai-inference)
- [Grand View Research：data center liquid cooling market](https://www.grandviewresearch.com/industry-analysis/data-center-liquid-cooling-market-report)
- [BCC Research via GlobeNewswire：data center power infrastructure](https://www.globenewswire.com/news-release/2026/04/30/3284618/0/en/Power-Infrastructure-for-Data-Centers-Market-to-Reach-47-3-Billion-by-2030-Driven-by-AI-Intensive-Computing-Expansion.html)
- [SDxCentral：Dell'Oro AI back-end Ethernet switch sales tripled](https://www.sdxcentral.com/news/ethernet-switch-sales-triple-as-hyperscale-ai-demand-soars/)

重点一手 PPTX：

- [IDC：Understanding the EMEA Adoption of OCP Designs](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7986/5265c5cc-296a-4d3e-86c7-2640a67fc7f3-idc-ocp-emea-regional-summit-slides-042226-76a376caae31d772d1a5c91270efa0ff.pptx)
- [Open Data Center for AI](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8069/1582675c-5782-4bc5-abd5-5531b27d3212-emea-summit-presentation-combined-9cd0a618bbd8155db966bb4ab334b462.pptx)
- [ORv3 and HVDC Power Systems](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7959/dac565c0-6ed3-4921-9748-0f7bd6ee299d-ocp-barcelona2026-requirements-considerations-of-next-generation-ai-power-shelves-a1fe41e844a1e7d1f59171f4c702a15e.pptx)
- [LVDC Power Distribution](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8109/90ea68d8-1d2a-45f2-a1c6-9f5d3c5e7767-emea-summit-lvdc-power-distribution-breakout-apr-2026-1-5e54c577caa1055218ce4b65befd4b6e.pptx)
- [DC Microgrids and 800V/750V/1500V](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8113/4d9e2248-81b4-4b2b-a4cd-a8a5fd2b37ee-emea-summit-bridging-the-worlds-of-data-centers-and-direct-current-microgrids-april-2026-e692412e6dba44a1ce3c44ce76b9ab35.pptx)
- [Cooling Environments and Cold Plate](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7923/d53d3b7f-b935-4ead-9af8-31db4337a606-ce-industry-analytics-project-progress-and-cold-plate-developments-5507e512d35bc1739f9f67c18ff4f7e2.pptx)
- [Coldplate Base Specification](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8210/15b3228c-7568-4d4d-ae35-e8a1816d9d0a-ocp26e-presentation-template-breakouts-final-260301-1-18206612699d5a86c8e715fb22abc3bc.pptx)
- [UQDv2 Interoperability](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7997/066da0b3-e950-45d7-bc9d-bd0d7f78ec58-2026-emea-summit-uqdv2-interoperability-langer-final-cbefc92fd305764961b54c8aad649598.pptx)
- [Liquid Cooling TCO Tool v1.3](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8130/89e632e4-5d21-46bf-8488-0e4123d28d34-tco-model-for-liquid-cooled-dcs-final-9c0a24a4c8b0144afd82c37765b1ad9a.pptx)
- [Immersion Cooling in 2026](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7929/28c7d464-47b2-4c20-bb0a-263129481bbb-immersion-cooling-in-2026-project-progress-industry-adoption-and-the-path-ahead-f3e2789e48ddc21620e4b968cc7f5442.pptx)
- [UALink and OCP](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8020/5ec17fde-a9c6-41ae-aa9d-a47592627aa7-ualink-ocp-emea-2026-presentation-v3-2f696567e0e8035e72bc91bd8bb29dcf.pptx)
- [ESUN 1.0](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8167/8d2fdc59-a74c-40aa-8176-e8ca1bb4b2d1-ocp-esun-ethernet-for-scale-up-network-final-cb64e37dce850945d9dc444b0784021a.pptx)
- [SUE-T](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8303/8c05a8bf-356c-43d4-922c-266498c210a5-lamb-sue-t-barcelona-april-2026-final-ebd957466b2d9c4f55fd5f4d47b8ceb4.pptx)
- [800G and 1.6T Open AI Fabrics](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8133/35a23685-896a-4b24-8098-af5e51b98711-high-performance-ai-fabrics-built-on-open-standards-ocp26e-afcf29264b11ba69ef36c4cba82712f3.pptx)
- [Silicon Photonics Switching](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8389/fe72d64c-44d5-44e3-b7d7-78a41a40b026-ocp-2026-ipronics-final-dcb5cba6b3949c687b3d569d3c5c197e.pptx)
- [400G/lane CPO and wafer-scale optical interconnect](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8386/984c946b-194e-4668-ba72-b5c5ee49a865-ocp26e-presentation-possieur-towardswaferscaleoi-relyingonsiliconphotonicsandadvanced3dassembly-final-2fa5516b0edaf6c6a8de9ccae4bf2f3b.pptx)
- [Multi-Core Fiber](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8343/b28513f2-989b-49ab-a4e3-34fc51f510d6-sel-041726-ocp-emea-presentation-v1-with-notes-5db05222a5d401ca94187823329ae26a.pptx)
- [FCSA and composable chiplets](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8176/61eeb8da-47cf-41c3-a774-06ef0cd6b97c-ocp26e-accelerating-composable-chiplets-knight-thur-0910-v2-21fd76d43631a1cb7feaf87e9841ae89.pptx)
- [Chiplet electrical-optical connectivity](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8259/0f93eaac-e8fe-432c-98cb-a8735c1f0e15-ocp-2026-enginnering-the-chiplet-era-letizia-giuliano-final-987b3d911cbf91da313dde9654174ddc.pptx)
- [Caliptra Update](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8282/822259d7-f1b0-42c6-8c21-362e7fbaf5f1-ocp26e-caliptra-update-c0d90babac26c4cc4c77dc1c755b630c.pptx)
- [OCP S.O.L.I.D.](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8077/75859441-fb86-4b3b-b420-fb06554d5960-introducing-ocp-solid-af93c4c38d6ef5ba51cacac84a44f2c1.pptx)
- [OCP L.O.C.K.](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8071/546465f7-d7d2-402b-a908-5a8cbb428cc7-ocp-emea-2026-lock-update-6af03716383450784be20acf7aade56b.pptx)
- [openSFI Update](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8090/5933d80c-f1d8-44ff-aeca-f53160c7dc9a-ocp26e-presentation-opensfi-update-d0e0136381b413f6c4239a13fbe0d29e.pptx)
- [Meta Hardware Circularity](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8211/3b15125e-1d29-482f-93f5-bea131a5d458-hardware-circularity-at-scale-ocp-emea-2026-1-ab7602f6c32d1886a4e1cfaa3e1440f8.pptx)
# OFC 2026 光通信大会更新：AI 光互联从模块升级进入架构重写

> 资料口径：本报告只整理外部公开资料，包括 OFC 官方新闻/会议指南、厂商 OFC 发布、市场机构公开摘要、会后行业博客和少量非官方会后观察；未参考本项目目录内既有文件。时间口径为 2026 年 OFC，即 2026 年 3 月 15-19 日在洛杉矶举行的 Optical Fiber Communication Conference and Exhibition。

## 一句话结论

OFC 2026 的最大变化不是“800G 升到 1.6T”这么简单，而是 AI 集群把光互联从一个可插拔模块采购问题，推成了系统架构问题：1.6T 已进入规模部署窗口，3.2T/400G-per-lane 已从路线图变成样机和器件验证，CPO/CPX/NPO/XPO/OCS/多 rail 传输都在回答同一个问题：如何在功耗、面板密度、可维护性、光纤数量和跨数据中心距离之间重新分配价值。

最直接的数字信号：OFC 官方预计 2026 年会议有 16,000 名参会者、90 个国家、700+ 展商、130 位 invited/tutorial speaker 和 45 场展厅剧场报告；Cignal AI 估计 2025 年光通信组件收入接近 250 亿美元，其中 datacom 超过 180 亿美元、coherent module 接近 60 亿美元；400G+ datacom 模块 2025 年出货约 4,200 万只，800G 2026 年预测超过 2,000 万只，1.6T 2026 年预测超过 500 万只；TrendForce 估计 800G 及以上模块出货占比将从 2024 年 19.5% 升到 2026 年 60%+。

## 1. OFC 2026 的重点和发展方向

### 1.1 会议本身释放的信号

- OFC 2026 官方新闻稿称展厅售罄，预计 16,000 名参会者、90 个国家、700+ 展商。会议主席的表述很直白：AI-driven growth 正在加速更高带宽和更高能效需求。
- 三个 plenary 分别来自 Coherent CTO Julie Sheridan Eng、NVIDIA AI Infrastructure SVP Alexis Bjorlin、Tesat-Spacecom CTO Siegbert Martin，基本覆盖了三个主战场：数据中心光互联、AI 网络架构、空间光通信。
- 官方 conference guide 里高频议题包括：AI data center networks、CPO integration ready for AI pipelines、interconnect latency and distributed AI training、silicon photonics modulators、photonic AI computing、hollow-core fiber、800G/1.6T validation、quantum/QKD、space optical networks。

### 1.2 与过去两年的关键转折

**第一，1.6T 从“演示产品”进入“规模供货前夜”。**  
2024-2025 年市场争论的是 800G 是否能顺利放量、1.6T 何时可用；OFC 2026 上，Coherent、Lumentum、Eoptolink、OpenLight、Broadcom、NVIDIA 生态都围绕 1.6T OSFP/DR8/2xDR4/LRO/LPO/TRO 给出产品或样机。Cignal AI 公开摘要直接给出 2026 年 1.6TbE 模块出货超过 500 万只的预测。

**第二，3.2T 的核心不再是“会不会做”，而是 400G-per-lane 的器件、DSP、封装、测试能否按成本量产。**  
Broadcom 在 OFC 发布 Taurus 400G/lane optical DSP，配套 400G EML/PD，目标是低功耗 1.6T 并铺路 3.2T；Coherent 展示 400G/lane PAM4 optical links，包括 400G differential EML 和基于纯硅 PN junction Mach-Zehnder Modulator 的 SiPh PIC；OpenLight 发布 3.2T DR8 PIC，使用 448G EAM，约 90% active element 到 silicon waveguide 耦合效率、2V 低驱动摆幅，3.2T beta 样品预计 2026 年 Q4。

**第三，CPO 不再只是 Broadcom/NVIDIA 的“未来方向”，而开始变成标准、连接器、ELS、可维护性和供应链生态。**  
NVIDIA 官方 CPO 页面给出的卖点是 5x power efficiency、10x resiliency、5x sustained application runtime，并称 Spectrum-X Ethernet Photonics 2026H2 可用，最高 409.6Tb/s；Open CPX MSA 在 OFC 前夕成立，创始成员包括 Ciena、Coherent、Marvell、Molex、Samtec、TeraHop，目标是给 CPO/NPO optical engine 定义 socket、connector、thermal、electrical、optical、management 规范。

**第四，XPO 说明“可插拔”没有死亡，而是在液冷和更大 form factor 中自救。**  
Arista 发起 XPO MSA：12.8Tbps 液冷可插拔模块，64 lanes，每模块 12.8Tbps，每 OCP rack unit 面板密度 204.8Tbps，比 1.6T OSFP 提升 4x；内置 cold plate，单模块支持最高 400W 冷却，支持 linear、half-retimed、fully-retimed 接口。这个方向的含义是：CPO 会长大，但高密度可插拔也会并行存在。

**第五，AI scale-across 把 coherent、线路系统、光纤数量重新拉回主线。**  
Marvell 发布 COLORZ 1600，号称行业首个 1.6T ZR/ZR+ pluggable，2nm Electra coherent DSP，支持 MACsec，1.6T 覆盖 campus 20km、metro 120km、regional 1,000km，2026H2 采样。Ciena 推 1600ZR/ZR+、hyper-rail photonics 和 full spectrum transponder；Nokia 推 1.6T coherent pluggable、2.4T pluggable、3.2T coherent-lite、full-band transponder、多 rail ILA。Nokia 会后总结提到 Meta 演示的区域 DCI 光纤需求：传统 regional DCI 常见 16-48 对光纤，AI-driven regional DCI 需要 128+ 对。

## 2. 会上最重要的产品和技术事实

### 2.1 1.6T：规模爆发最确定

- Cignal AI：2025 年 400G+ datacom 模块预计 4,200 万只，800GbE 预测超过 2,000 万只，1.6TbE 2026 年超过 500 万只。
- TrendForce：800G 及以上模块全球出货占比从 2024 年 19.5% 到 2026 年 60%+；Google 2026 年约 400 万颗 TPU 将带来超过 600 万只 800G+ 光模块需求，Innolight + Eoptolink 预计拿到 Google 800G+ 订单近 80%。
- Lumentum 1.6T DR4 OSFP 原型：4x400Gbps 光口、8x200Gbps host electrical interface，使用 4 颗 400G differential EML，明确作为未来 3.2T stepping stone。
- Coherent 展示多种 1.6T transceiver：SiPh PIC、高功率 InP CW laser、200G InP EML、200G GaAs VCSEL，并接入三家行业领先 DSP。
- Lumentum 已有 1.6T 2xDR4 OSFP 产品页面：8 个 212.5Gbps PAM4 electrical/optical lane，500m reach，fully retimed 版本典型功耗 22W，TRO 版本典型功耗 16W。

判断：1.6T 的爆发力度为“确定性强、价格下行也挡不住总收入增长”。2026 是导入和短缺年，2027 是供应链扩散和价格竞争年。

### 2.2 3.2T/400G-per-lane：技术拐点已出现，但量产要等

- Broadcom：Taurus 400G/lane optical DSP + 400G EML/PD，用于低功耗 1.6T，并为未来 3.2T 模块和 204.8T switching platform 铺路。
- Coherent：3.2T 用 400G/lane PAM4 光链路，路线同时包含 400G differential EML 和 silicon photonics PIC。
- OpenLight：3.2T DR8 PIC 已 alpha，bare die 立即可用；flip-chip 448G modulator + driver evaluation board 预计 2026 年 3 月底；3.2T beta 样品预计 2026 年 Q4。
- VIAVI 会后判断：3.2T 会显著增加系统和测试复杂度，预计 2027 年出现 initial live demonstrations 是较合理判断。

判断：3.2T 是 2027-2028 的主线，不应把 2026 的器件样品误解成模块大规模收入。但 400G/lane EML、EAM、MZM、DSP、测试设备会先赚钱。

### 2.3 CPO / CPX / NPO / ELS：从技术展示进入生态标准化

- NVIDIA：CPO switch 集成 silicon photonics，替代 pluggable transceiver，官方宣称 5x power efficiency、10x resiliency、5x sustained application runtime；Quantum-X800 CPO switch 支持 144 个 800Gb/s InfiniBand ports，连接超过 10,000 GPUs 的 non-blocking two-level fat-tree；Spectrum-X Ethernet Photonics 最高 409.6Tb/s，2026H2 可用。
- Coherent：6.4T socketed CPO，32x200G，基于 silicon photonics，配外部 ELS；另有 multimode socketed CPO + high-speed VCSEL，以及 400G-per-lane InP modulator array。
- Lumentum：1310nm SHP laser 在 25C 输出 >1.0W、50C 输出 >800mW，>40dB SMSR；16-channel DWDM UHP laser 用两个 ELSFP 模块输出 16 个 200GHz-spaced channels，单 channel 入纤约 24dBm，瞄准 CPO 减少 fiber count。
- Open CPX MSA：LightCounting CEO 在 MSA 发布中预计 co-packaged / near-package interfaces 未来五年 annual port shipments 超过 1 亿。

判断：CPO 的难点已经从“能不能跑”转到“能不能维护、能不能多供应商、laser/ELS 怎么冗余、field failure 怎么换”。这会让 CPX/socketed CPO/NPO 比早期全封闭 CPO 更容易被采用。

### 2.4 XPO：12.8T 液冷可插拔，延长 pluggable 生命周期

- Arista XPO MSA：12.8Tbps per module、204.8Tbps per OCP rack unit、比 1.6T OSFP 面板密度 4x、integrated cold plate 支持最高 400W/module。
- Eoptolink OFC 展示：12.8T XPO、400G/lambda 1.6T DR4、200G/lambda 1.6T FRO/LRO/LPO。
- Linktel OFC 展示：12.8T liquid-cooled XPO、200G/lane 1.6T module、400G/lane optical engines。

判断：XPO 是“可插拔阵营”的关键反击。它不会取代 1.6T OSFP 的近期放量，但可能在 204.8T switch/大规模 AI fabric 上延后 CPO 的完全替代。

### 2.5 Coherent / 1600ZR / coherent-lite：AI scale-across 的第二条主线

- Marvell：COLORZ 1600 1.6T ZR/ZR+ pluggable，Electra 2nm coherent DSP，MACsec，OSFP，C/L band；1.6T 覆盖 20km/120km/1,000km；Libra 800G ZR/ZR+ 可在 800G 1,000km、600G 2,000km、400G 3,000km。
- Ciena：2nm single-carrier 1.6Tb/s coherent 用于 1600ZR/ZR+；hyper-rail photonics 最高 32x density、128 fiber pairs/rack、功耗降低最高 75%、空间降低 85%；Vesta 200 6.4T CPX optical engine。
- Nokia：四个新 DSP + InP/SiPh optical front ends；1.6T coherent pluggable、2.4T pluggable、3.2T coherent-lite、double-sided pluggables、full-band transponders、2.4T/3.2T embedded transponders；产品族预计 2027 年中采样、2027H2 GA。
- Nokia 会后技术总结：1600ZR targeted power 约 32-35W；1600ZR+ 约 38-40W；1600CL 目标约 30W、300ns latency、20-40km reach。

判断：市场容易只看“数据中心内部 1.6T”，但 scale-across 的 coherent pluggable、line system、multi-rail amplifier、full spectrum transponder 可能是更隐蔽且更高壁垒的增量。

### 2.6 OCS / 光交换：节能极强，但会改变交换机和模块价值分配

- TrendForce 对 Google Apollo OCS 的描述：MEMS micromirror 做 fiber-to-fiber direct connection，避免多次 O-E-O 转换；单台 OCS switch 功耗约 100W，而传统交换约 3,000W，功耗降低约 95%。
- Google Ironwood TPU 架构中，短距用高速铜，rack 间用全光网络；2026 年约 400 万 TPU 对应 800G+ 模块需求超过 600 万只。

判断：OCS 可能减少部分电交换芯片/retimer 的功耗和价值占比，但会显著拉动光模块、光纤管理、MEMS/光交换、测试和运维软件价值。

## 3. 成熟和量产路线预测：基准、乐观、超预期乐观

| 方向 | OFC 2026 状态 | 基准口径 | 乐观口径 | 超预期乐观口径 |
|---|---:|---:|---:|---:|
| 800G/1.6T datacom pluggables | 800G 已主流，1.6T 多厂商样机/产品化 | 2026 年 1.6T >500 万只，2027 年 1,200-1,800 万只；800G 继续放量但 ASP 快速下行 | 2027 年 1.6T 2,000-2,500 万只，主要 hyperscaler 大比例从 800G 切 1.6T | 1.6T 在 2027 年成为新增 AI 集群默认配置，出货 3,000 万只级别，短缺延续 |
| 3.2T / 400G-per-lane | DSP、EML/EAM/MZM、PIC 样品密集出现 | 2026 样品/验证，2027 live demo/客户 qual，2028 规模化 | 2027H2 小批量收入，2028 上半年开始较大客户导入 | 204.8T switch 平台提前拉动，2027 年形成 10 亿美元级早期市场 |
| CPO / CPX / NPO / ELS | NVIDIA/Broadcom/Coherent/Lumentum/CPX MSA 明确推进 | 2026-2027 以 NVIDIA/Broadcom 和少数云厂 pilot 为主，收入先来自 ELS/optical engine | 2027 年 socketed CPO/CPX 标准稳定，多个 AI cluster 部署 | pluggable 功耗瓶颈加速暴露，CPO/CPX 在 2027 年成为高端 AI switch 的默认路线之一 |
| XPO 12.8T liquid-cooled pluggable | Arista 发起 MSA，多家模块商展示 | 2026 展示/标准化，2027 小批量验证，2028 配合 204.8T switch | 2027H2 开始在高端 AI fabric 中导入 | XPO 成为 CPO 之外的主流高密度路径，2027 年即形成 20 亿美元级需求 |
| 1600ZR/ZR+ / coherent-lite | Marvell 2026H2 采样；Ciena/Nokia 2nm coherent 路线 | 800ZR/1600ZR 2026-2027 放量，1600ZR+ 2027 后规模化 | AI scale-across 建设快于预期，coherent pluggable 增速 40%+ | campus/metro AI DCI 爆发，coherent-lite 进入数据中心内部长距互联 |
| OCS / optical switching | Google Apollo 进入体系化讨论 | Google/少数自研 TPU 云厂优先采用，2026-2027 市场小但拉动模块 | Meta/Microsoft/Anthropic 相关集群跟进，OCS 成为 TPU-like cluster 标配 | GPU Ethernet fabric 也广泛吸收 OCS，电交换扩容路径被部分重写 |
| Multi-rail ILA / FST / hyper-rail | Nokia/Ciena 明确推多光纤/整 band/整 fiber pair | AI regional DCI 从 wavelength 部署转向 fiber-pair 部署，2026H2 起订单增长 | 128+ fiber pairs/rack 级需求成为大型 AI region 标配 | 线路系统成为 AI capex 的新瓶颈，放大 Ciena/Nokia/Cisco/Corning/Senko 价值 |
| Test & measurement | VIAVI/Keysight 等 1.6T/3.2T 验证平台受益 | 1.6T MAC/FEC/224G SerDes 测试 2026 高景气，3.2T 2027 接棒 | 供应商扩产和客户 qual 并行，测试设备增速 40%+ | 400G/lane 难度超预期，测试/验证成为卡点和高利润环节 |

## 4. 重要产品和技术的市场规模、增速、利润率

说明：公开市场机构通常给“整体光模块/光组件/datacom/coherent/CPO”的数字，很少把 1.6T、XPO、OCS、ELS 拆成完全独立口径。下面“已公开数字”直接引用公开资料；“测算”是基于公开出货、ASP、供应链利润率和 OFC 发布节奏的估算。

| 产品/技术 | 当前市场规模（美元） | 关键事实 | 未来一年收入增速：基准 / 乐观 / 超预期 | 当前利润率与未来方向 |
|---|---:|---|---:|---|
| 全部 optical transceiver | 2025 年约 238 亿美元（LightCounting） | AI datacenter 拉动 Q4 2025 供应商收入超预期；产能追上后 2026 年末可能价格竞争加剧 | +20-30% / +30-45% / +50%+ | 领先模块/器件商 gross margin 约 30-40%+；代工 EMS 约 12%。基准：ASP 下行使利润率小幅下滑；乐观：高端 mix 抵消降价；超预期：短缺延续，利润率上修 |
| Datacom optical components / 400G+ datacom modules | 2025 年 datacom optical component >180 亿美元；400G+ 单季收入已 >50 亿美元 | Cignal：2025 年 400G+ 模块 4,200 万只；datacom optical component 2024-2029 CAGR 20%+，2029 近 290-300 亿美元 | +30-40% / +45-60% / +70% | 800G/1.6T 领先供应商 gross margin 约 30-42%；Fabrinet 这类 EMS non-GAAP GM 约 12.4%。2026H1 强，2026H2 需防 ASP 加速下行 |
| 1.6T pluggable modules | 2026E 约 70-100 亿美元（测算：>500 万只 x $1,400-2,000 ASP） | Cignal 明确 2026 年 1.6TbE >500 万只；Coherent/Lumentum/Eoptolink/OpenLight 等 OFC 集中展示 | +80-120% / +120-180% / +200%+ | 早期 gross margin 可达 35-45%；随着中国/北美多供应商扩散，2027 年 ASP 压力明显。短缺环节是 200G/400G EML、SiPh PIC、DSP、isolator/filter、测试产能 |
| 3.2T / 400G-per-lane modules & engines | 2026 年商业收入 <2 亿美元（测算，主要样品/评估板/测试） | Broadcom Taurus、Coherent 400G/lane、OpenLight 448G EAM；OpenLight 3.2T beta Q4 2026 | 2027 年 +200% 但基数低 / 形成 10-20 亿美元早期市场 / 2027 年 30 亿美元+ | 模块利润率暂不可稳定测；稀缺器件和 DSP 毛利高，module 端会被良率和测试时间压制 |
| CPO / CPX / NPO / ELS | CPO 2026 年约 1.6 亿美元，2031 年约 7.5 亿美元，CAGR 35.92%（Mordor） | NVIDIA 2026H2 Spectrum-X Photonics；Open CPX MSA；Coherent 6.4T socketed CPO；Lumentum 高功率 ELS | +50-80% / +100-150% / +200-300% | ELS/laser/optical engine gross margin 可高于传统模块；但 CPO 系统早期 NRE、可靠性、服务成本高。利润率方向取决于是否形成多供应商标准 |
| XPO 12.8T liquid-cooled pluggable | 2026 年 <1 亿美元（测算，基本是样品/开发） | Arista MSA：12.8T per module、204.8T per OCP RU、4x OSFP density、400W cooling | 2027 年 2-5 亿 / 5-15 亿 / 20 亿+ | 早期 ASP 和毛利率高，但液冷、可靠性、field service 会吃掉部分利润；标准成熟后毛利率回落 |
| Coherent pluggables / DCI optics | 2025 年 coherent module 接近 60 亿美元（Cignal） | Marvell 1.6T ZR/ZR+ 2nm DSP 2026H2 采样；Ciena/Nokia 推 1600ZR/ZR+、coherent-lite、full-band | +20-35% / +35-50% / +60%+ | DSP/高端 coherent module 毛利通常高于普通 datacom module；未来一年 mix 向 800ZR/1600ZR 倾斜，利润率稳中有升 |
| OCS / optical circuit switching | 2026 年独立硬件约 2-6 亿美元（测算；Google 生态为主） | TrendForce：OCS 单机约 100W vs 传统 switch 约 3,000W，功耗 -95%；Google 2026 年 800G+ 模块需求 >600 万只 | +50% / +100% / +200% | MEMS/OCS 硬件 gross margin 约 35-50%（测算）。如果被云厂自研压价，利润在模块和系统集成侧分散 |
| Multi-rail ILA / hyper-rail / FST | AI scale-across 相关 dedicated DCI/line system 为低个位数十亿美元（测算） | Ciena：hyper-rail 32x density、-75% power、-85% space；Nokia：multi-rail ILA 160 fiber pairs/rack，2026H2 可用 | +20-30% / +40-60% / +80% | 系统厂 gross margin 多在 35-45% 区间；功耗/空间节省使客户愿意付溢价，短期利润率优于传统传输设备 |
| 高速测试与验证 | 2026 年约 5-10 亿美元（测算，1.6T/224G SerDes/3.2T 驱动） | VIAVI 1.6T TestCenter D2、ONE-1600ER 支持 1.6TE MAC、2x800GE、4x400GE、8x200GE、FEC、224G SerDes | +30-50% / +60% / +80%+ | 测试设备 gross margin 通常高，且 400G/lane 复杂度提升会延长高景气 |

## 5. 与市场主流认知可能相违背的洞见

### 5.1 CPO 会爆发，但不会马上杀死 pluggable

市场容易把 CPO 叙事讲成“pluggable 被淘汰”。OFC 2026 反而显示 pluggable 在进化：1.6T OSFP 继续规模化，XPO 用 12.8T + 液冷 + 400W cooling 把 pluggable 推向更高密度；CPX/socketed CPO 也在借鉴 pluggable 的可维护性。更可能的路线是：OSFP 负责近期主流，XPO 负责高密度过渡，CPO/CPX 负责功耗极限和高端 switch。

### 5.2 1.6T 不是单一技术路线的胜利

Coherent 同时展示 SiPh、InP、VCSEL；Lumentum 强调 400G differential EML；OpenLight 是 III-V integrated SiPh；Broadcom 用 EML/PD + DSP 推 400G/lane。结论：2026-2027 年不会只有“硅光赢”或“EML 赢”，而是不同 reach、功耗、成本、良率和客户偏好下多技术并行。

### 5.3 价格战可能比需求放缓更早出现

LightCounting 的公开摘要提醒：光芯片和 transceiver 产能正在追上需求，2026 年末可能带来更激烈竞争和更快价格下行。也就是说，即使 AI 光模块需求继续强，个别模块厂毛利率也可能在 2026H2-2027 面临 ASP 压力。

### 5.4 AI scale-across 可能比市场想象中更快放大 coherent 和线路系统

投资者常盯数据中心内部短距模块，但大型 AI region 的瓶颈在 campus/metro/regional DCI、光纤对数、放大站空间和功耗。Ciena/Nokia 的 hyper-rail、multi-rail ILA、FST 不是传统电信小修小补，而是在给 AI 区域网络做“整 fiber pair / 整 band”部署。

### 5.5 OCS 是光模块需求放大器，不只是交换机替代品

Google Apollo OCS 100W vs 3,000W 的功耗差距非常大，但 OCS 架构也要求 AI 集群一开始就配置足够 800G/1.6T 光模块。若 OCS 扩散，电交换芯片/retimer 的某些价值会被压缩，但光模块、fiber management、MEMS switch、测试和运维软件会受益。

### 5.6 3.2T 不能按“2026 大量出货”定价

OFC 上 3.2T 信号很强，但多是 400G/lane link、PIC、DSP、evaluation board、alpha/beta sample。合理节奏是 2026H2 客户 qual、2027 live demo/小批量、2028 才真正扩产。短期更可兑现的是 400G/lane 的上游器件、DSP、测试。

### 5.7 HCF 已经从科学展示走到低延迟网络候选，但商业化仍慢

Nokia 会后总结提到 hollow-core fiber state-of-the-art loss 已到 0.04dB/km。HCF 对低延迟 DCI、金融、分布式 AI 训练有吸引力，但连接器、部署成本、可维护性和供应链还会限制其近两年收入。

### 5.8 供应链瓶颈比“模块组装能力”更细

真正的瓶颈集中在：200G/400G EML/EAM/MZM、InP laser/PD、高功率 ELS、isolator/filter、3nm/2nm DSP、224G/448G SerDes、液冷封装、high-density connector、fiber management、测试时间。只看“谁能组装 OSFP”会漏掉利润更高、更难扩产的环节。

## 6. 产业链受益顺序和风险

### 6.1 优先受益环节

1. 高速光模块：800G 继续放量，1.6T 在 2026-2027 接棒；代表方向包括 Innolight、Eoptolink、Coherent、Lumentum、NVIDIA 自有/生态模块。
2. 光芯片和激光器：200G/400G EML、InP CW laser、ELSFP、VCSEL、SiPh PIC、III-V integrated SiPh，是 1.6T/3.2T/CPO 共用瓶颈。
3. DSP/SerDes/retimer/AEC：Broadcom Taurus、Marvell 2nm coherent DSP、200G lane retimer、PCIe Gen6/以太网 retimer；但 CPO/OCS 会在部分场景减少 retimer/DSP 价值。
4. CPO/CPX/XPO 连接和热管理：Samtec、Molex、TE、Amphenol、Senko、Corning、液冷 cold plate 和高密度光纤管理。
5. Coherent DCI 和 line system：Ciena、Nokia、Cisco/Acacia、Marvell 在 scale-across 中更受益。
6. 测试设备：VIAVI、Keysight 等受益于 1.6T MAC/FEC、224G SerDes、400G/lane 和 3.2T 验证复杂度提升。

### 6.2 主要风险

- 2026 年末产能追上后，800G/1.6T ASP 下行可能快于预期。
- CPO/CPX 的 field service、laser redundancy、thermal drift、可靠性验证时间可能拖慢客户量产。
- XPO/CPX/OCI/OIF 等标准并行，可能带来 form factor 分裂和库存风险。
- AI 数据中心电力/液冷/土地/并网约束会让光互联订单出现季度波动。
- 中美供应链和客户认证风险会影响中国模块厂份额和估值。
- 3.2T 过早资本化容易踩节奏：器件先于模块，模块先于交换机平台，交换机平台先于大规模集群部署。

## 7. 资料来源

- [OFC 官方新闻：OFC 2026 opens with sold-out exhibition](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-opens-next-week-in-los-angeles-with-sold-out-exhibition-as-ai-driven-network-demand-fuels/)
- [OFC 2026 Conference Guide PDF](https://ofc-web-afd-e8csdte4dubnfvfu.z02.azurefd.net/ofc/media/images/documents/2026/2026ofc_conference_guide.pdf)
- [OFC 官方新闻：AI-era data centers and networks exhibit](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-exhibit-connects-the-global-optical-ecosystem-powering-ai-era-data-centers-and-networks/)
- [NVIDIA Silicon Photonics](https://www.nvidia.com/en-in/networking/products/silicon-photonics/)
- [Broadcom OFC 2026 AI infrastructure release](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai)
- [Coherent 1.6T/3.2T/XPO OFC 2026 release](https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026)
- [Coherent CPO OFC 2026 release](https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026)
- [Lumentum OFC 2026 release](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx)
- [Marvell COLORZ 1600 / 2nm coherent DSP release](https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html)
- [Ciena OFC 2026 AI networking release](https://www.ciena.com/about/newsroom/press-releases/ciena-brings-ai-networking-expertise-to-ofc-2026)
- [Ciena high-speed connectivity innovations release](https://www.ciena.com/about/newsroom/press-releases/ciena-solidifies-ai-networking-leadership-unveils-new-innovations-for-high-speed-connectivity)
- [Nokia AI-era optical solutions release](https://www.nokia.com/newsroom/nokia-launches-suite-of-applicationoptimized-optical-solutions-for-ai-era-networks/)
- [Nokia OFC 2026 takeaways](https://www.nokia.com/blog/ofc-2026-takeaways-pluggables-multi-rail-hcf-and-ai/)
- [Arista XPO MSA release](https://www.arista.com/en/company/news/press-release/23697-pr-20260311)
- [Open CPX MSA](https://www.opencpxmsa.org/)
- [Eoptolink 12.8T XPO release](https://www.eoptolink.com/news/13-new-products/364-eoptolink-joins-xpo-msa-and-unveils-industry-first-12-8-tbps-liquid-cooled-pluggable-optics-for-ai-data-centers)
- [OpenLight 3.2T DR8 PIC release](https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants)
- [TrendForce: Google 800G+ and OCS architecture](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- [Cignal AI: optical component revenue nearly $25B in 2025](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)
- [Mordor / GlobeNewswire: CPO market 2026-2031](https://www.globenewswire.com/news-release/2026/01/29/3228606/0/en/Co-Packaged-Optics-Market-Growing-at-35-92-CAGR-to-Reach-USD-0-75-Billion-by-2031-Reports-Mordor-Intelligence.html)
- [LightCounting: optical transceiver sales reached $23.8B in 2025](https://www.lightcounting.com/newsletter/en/march-2026-quarterly-market-update-380)
- [VIAVI: OFC 2026 1.6T going mainstream and 3.2T emergence](https://blog.viavisolutions.com/2026/04/23/ofc-2026-1-6t-going-mainstream-the-emergence-of-3-2t/)
# PCI-SIG Developers Conference 2026：AI 机柜时代的 PCIe 互连转折点

> 调研时间：截至 2026-05-08。资料边界：仅使用公开网络资料、PCI-SIG 官方页面/议程/博客、公开新闻稿、公司财报和公开市场报告摘要；未参考本项目目录内既有文件或信息。

## 0. 高浓度结论

1. **今年 DevCon 的主线不是“PCIe 又快了一倍”，而是“PCIe 从板级外设总线升级为 AI 机柜/跨机柜互连基础设施”。** 公开议程把 PCIe 6.x/7.0 电气、协议、CEM、CopprLink 线缆、SFF、光互连、Retimer、AI infrastructure、PCIe 8.0 panel 放在同一个会议框架下，说明产业关注点从 endpoint/slot 兼容转向 rack-scale 拓扑、reach、功耗、可靠性、可管理性和可验证性。

2. **PCIe 8.0 Draft 0.5 是今年最大标准事件。** PCI-SIG 在 2026-05-01 公布 PCIe 8.0 draft 0.5，目标仍是 **256.0 GT/s raw bit rate、x16 双向最高 1.0 TB/s、2028 完整发布**，并明确写入：评估新连接器、保证 latency/FEC/reliability、保持后向兼容、通过协议增强提升有效带宽、继续降功耗。Draft 0.5 的意义是架构目标和主要机制足够稳定，IP、PHY、SerDes、连接器、Retimer 和系统厂商可以开始更认真地 pathfinding/prototyping。

3. **PCIe 7.0 已经从“未来规格”变成“系统设计输入”。** PCIe 7.0 1.0 在 2025-06-11 发布，速率 **128.0 GT/s、x16 双向最高 512 GB/s**；今年 DevCon 大量内容集中在 PCIe 7.0 PHY logical、电气预算、128 GT/s PAM4、光学链路系统级相关性和 SFF/CopprLink 支持，说明 2026-2027 会进入 Gen7 前期设计、测试和生态准备期。

4. **PCIe over optics 正式从“厂商方案”进入“标准路径”。** 2025 年 Optical Aware Retimer ECN 把 PCIe 6.4/7.0 里的 Retimer-based optical fiber 方案标准化；2026 DevCon 有 “System-Level Correlation for PCIe 7 Over Optics”、“Electrical & Optical Retimer Implementation/Verification Challenges”、“AEC vs DSP-Optics vs LPO”等议题。判断：短距仍先由铜缆/AEC/CopprLink 爆发，中长距和机柜/跨机柜 AI fabric 逐步导入光。

5. **近期最容易变成收入的不是 PCIe 8.0，而是 PCIe 6.0/6.x 的量产化、PCIe 7.0 的设计导入，以及 Retimer/Smart Cable/Fabric Switch 的 attach rate 提升。** Astera Labs 2026 Q1 收入 **3.08361 亿美元，同比 +93%、环比 +14%**，GAAP gross margin **76.3%**，并称 Scorpio X-Series **320-lane AI scale-up fabric switch 已经 shipping**、H2 2026 ramp，Scorpio P-Series 多客户 H2 2026 出货、2027 更大规模 ramp。这是“互连芯片利润池正在从配套件变成 AI 系统核心件”的直接证据。

## 1. 公开会议资料和一手信息脉络

### 1.1 会议基本事实

- **美国 PCI-SIG Developers Conference 2026**：2026-05-06 至 2026-05-07，Santa Clara Convention Center, Santa Clara, CA。PCI-SIG 官方称这是面向其 **900+ member companies** 的免费技术活动；2026 年因 FIFA World Cup 使用会场，时间和场地相较往年有调整。
- 官方议程分为三条 track：**PCI Express、PCI-SIG Architecture、Members Implementation**。
- 会议覆盖：Introductory Keynote & Annual Members Meeting、PCIe 6.x/7.0 Electrical Update、PCIe CEM Updates、PCIe 6.x/7.0 Protocol Update、PCIe 7.0 PHY Logical、PCIe 5.x/6.x Internal and External Cable Specifications、PCIe 8.0 Technical Panel Discussion、PCIe Compliance deep dives、AI infrastructure panel、PCIe 7 over optics、Retimer implementation/verification、AEC/DSP-Optics/LPO 对比。

### 1.2 技术事实：今年公开议程里的硬数字

| 主题 | 关键数字/事实 | 含义 |
|---|---:|---|
| PCIe 6.0/6.x | **64.0 GT/s PAM4**；x16 双向最高约 **256 GB/s**；引入 FLIT mode、低延迟 FEC、CRC、link-level retry | Gen6 从 paper spec 进入实现、测试、合规和 AI 平台部署阶段 |
| PCIe 7.0 | **128.0 GT/s PAM4**；x16 双向最高 **512 GB/s**；2025-06-11 发布 1.0 | 2026 的重点是 Gen7 PHY/electrical/pathfinding，而不是等待 2028 |
| PCIe 8.0 Draft 0.5 | **256.0 GT/s**；x16 双向最高 **1.0 TB/s**；目标 2028 完整发布 | IP/PHY/SerDes/连接器/Retimer 开始更明确的架构验证 |
| 电气规范 | 64/128 GT/s PAM4 关注 **BER <= 1e-6**、channel loss budget、reference clock jitter、Tx equalization、Rx architecture | 物理层难点从“能跑通”变成“可重复、可量产、可验证” |
| PCIe 7.0 receiver | 议程提到 enhanced CTLE、**29-tap Rx FFE**、**1-tap DFE** | 128 GT/s 需要更复杂的接收端均衡和测试模型 |
| Transmitter equalization | PCIe 6/7 电气更新提到 mandatory **4-tap PAM4 Tx equalization**、precoding、Gray coding | PAM4 后，模拟前端和链路训练复杂度继续上升 |
| CopprLink | PCIe 5.0/6.0 internal cable **up to 1 m**；external cable **up to 2 m** | PCB-only channel reach 不够，标准化铜缆成为服务器平台设计常规选项 |
| CEM/M.2/U.2/SFF | CEM 5.0/ECR，CEM 6.0 潜在改进；M.2/U.2 更新；SFF 讨论 EDSFF、SFF-8639、CopprLink、PCIe 7.0 支持 | 形态学升级与高速信号完整性同步推进 |
| 协议更新 | 已完成 ECN 包括 DOE 1.1、Unordered I/O、12V-2x6 Connector Updates、CMA-SPDM Revised、MMIO Mailbox Passthrough、Architectural Out-of-Band Management 等 | PCIe 正在叠加管理、安全、调试、异构系统能力 |
| 验证/合规 | 64 GT/s PHY lab study 强调 pass/fail 应该是 confidence level；FLIT error injection、FEC/CRC/retry、LTSSM timeout、L0p config 都是验证重点 | 合规瓶颈会成为 Gen6/Gen7 量产节奏的重要门槛 |

### 1.3 和此前市场/技术相比，重要变化与转折

**第一，PCIe 的竞争单位从“单设备接口”转成“AI rack 级互连拓扑”。** 以前 PCIe 的主要商业叙事是 CPU-GPU/SSD/NIC 之间的总线速率升级；今年的会议把 AI accelerator、scale-up fabric、retimers、switches、copper/optical connectivity 放在一起，说明 PCIe 正在承担更接近系统 fabric 的角色。

**第二，铜的极限正在迫使产业把连接器、线缆、Retimer 和光都前置到架构阶段。** PCIe 8.0 公开目标中特别写入“evaluating new connector technology”，这不是装饰性措辞，而是信号完整性和功耗压力已经接近传统 edge connector/PCB routing 的经济极限。2026 的现实路线不是“马上全光”，而是短距 AEC/CopprLink、板上/线缆 Retimer、中长距 optical-aware retimer 并行。

**第三，合规从二元 pass/fail 转向统计置信度。** 64 GT/s PAM4 的 run-to-run variation 使传统 PVT 极限测试不再足够；测试工具、自动化、协议错误注入、系统级仿真相关性会成为产品上市速度的决定因素。

**第四，PCIe 8.0 的 draft 0.5 把“远期标准”变成“近期研发预算”。** 2028 完整发布不代表 2028 才开始投入。历史上早期采用者会在 0.5 阶段启动架构和 IP 设计，尤其是 hyperscaler、自研 ASIC、GPU/AI 加速器和高端互连芯片厂商。

**第五，利润池正在向 connectivity silicon/software 倾斜。** Astera 2025 全年收入 **8.52525 亿美元，同比 +115%**，GAAP gross margin **75.7%**，non-GAAP operating margin **39.2%**；2026 Q1 收入 **3.08361 亿美元，同比 +93%**，non-GAAP operating margin **36.2%**。这类毛利率和增长速度说明 PCIe/CXL/AI fabric 芯片已不再是低附加值外围件。

## 2. 未来会爆发的产品和技术方向

### 2.1 PCIe 6/7 Retimer、Smart Cable Module、signal conditioning 芯片

**爆发原因：** PCIe 5.0 之后板级损耗、jitter、crosstalk、连接器反射、线缆长度都快速恶化；PCIe 6.0/7.0 的 PAM4 + FEC 进一步提高系统调试难度。AI 服务器中 GPU/CPU/NIC/SSD/switch 之间链路数量增加，Retimer attach rate 上升。

**成熟/量产路线：**

- **基准**：2026 年 Gen5/Gen6 Retimer 和 Smart Cable Module 在 AI 服务器、GPU 平台、网络交换机中持续放量；Gen7 以测试芯片、IP、连接器和样品为主。
- **乐观**：2026 H2 Gen6 在新一代 GPU/ASIC rack 中成为高配平台默认件；PCIe 7.0 retimer/link pathfinding 进入头部客户设计。
- **超预期乐观**：AI scale-up 和 scale-out 拓扑比预期更快扩大，Retimer 从“解决长链路问题”变成“几乎每个高端链路的默认保险”；高端 ASP 和 attach rate 同时上行。

### 2.2 PCIe/CXL/AI Fabric Switch，尤其是 32-320 lane 高 radix switch

**爆发原因：** AI rack 需要更高 radix、更低延迟、更强诊断和可管理性。传统 PCIe switch 是扩展 lanes；新一代 AI fabric switch 开始加入 memory-semantic fabric、collective operation acceleration、in-network compute、firmware/software fleet management。

**关键公开事实：**

- Astera 2026 Q1 称 Scorpio X-Series **320-lane AI scale-up fabric switch 已 shipping**，H2 2026 production ramp。
- Scorpio X 宣称 Hypercast 和 In-Network Compute 可让 collective operations **最高提升 2x**。
- Astera 称 merchant scale-up market 到 2030 年可达 **200 亿美元**。
- Scorpio P-Series PCIe-6 Fabric Switch 覆盖 **32-320 lane**，多客户多变体预计 2026 H2 出货，2027 更大规模 volume ramp。

**成熟/量产路线：**

- **基准**：2026 年 PCIe 6 switch 在少数 AI/custom ASIC/GPU 平台 ramp，2027 扩到更多平台。
- **乐观**：open scale-up fabric 在非 NVIDIA 封闭系统和自研 ASIC 集群中快速采用，PCIe/CXL switch 成为 merchant AI 服务器关键 BOM。
- **超预期乐观**：多家 hyperscaler 同时提高开放互连采购，PCIe/UALink/CXL 生态在特定 workload 上证明足够低延迟和高效率，fabric switch 进入类似高速以太网交换芯片的战略地位。

### 2.3 CopprLink、AEC、低损耗连接器和高速线缆

**爆发原因：** PCIe 5/6 的 PCB-only reach 已经限制服务器内部布局；AI 机柜要求高密度、可维护、可插拔和更长 reach。DevCon 明确讨论 PCIe 5.x/6.x internal/external cable specs：internal up to **1 m**、external up to **2 m**，并讨论 insertion loss、return loss、crosstalk、skew、sideband signaling。

**成熟/量产路线：**

- **基准**：2026 年 PCIe 5/6 internal cable 和 AEC 在高端服务器/存储/交换机放量；PCIe 7.0 SFF 支持继续推进。
- **乐观**：AI rack 设计把线缆化作为默认架构选项，CopprLink/AEC 从“工程补丁”变成标准 BOM。
- **超预期乐观**：新连接器和线缆体系在 PCIe 7/8 之前就形成事实标准，连接器厂商、线缆厂商和 Retimer 厂商深度绑定客户平台。

### 2.4 PCIe over optics、Optical Aware Retimer、LPO/DSP optics

**爆发原因：** PCIe 7/8 的速率、reach 和功耗压力使光成为标准路线的一部分。Optical Aware Retimer ECN 已经给 PCIe 6.4/7.0 规格加入 Retimer-based optical fiber 实现方式，允许不同光技术在电/光域之间做 multiplexing/data mapping，并扩展到 racks/pods。

**成熟/量产路线：**

- **基准**：2026 年以实验室相关性、系统仿真、头部客户 qualification 为主；2027 年少量量产导入。
- **乐观**：AI 机柜跨板/跨框互连提前光化，LPO 依靠低功耗和低延迟获得更多设计；DSP optics 保持长距和更稳健链路优势。
- **超预期乐观**：PCIe optical-aware retimer 变成开放 AI rack 的关键标准接口，光模块/硅光/Retimer 的边界重组，2027 年开始贡献明显收入。

### 2.5 PCIe/CXL IP、Verification IP、Compliance Tool、协议分析仪

**爆发原因：** PCIe 8.0 draft 0.5、PCIe 7.0 1.0、PCIe 6.0 合规和 FLIT/FEC/Retimer/optical 模式共同提高验证复杂度。DevCon 里 error injection、protocol tester、electrical compliance、pass/fail confidence、system-level correlation 的比重很高。

**成熟/量产路线：**

- **基准**：2026 年 PCIe 6/7 VIP、PHY/controller IP、protocol analyzer、BERT/oscilloscope compliance app 稳定增长。
- **乐观**：PCIe 8.0 0.5 提前拉动 Gen8 IP/PHY pathfinding 预算，EDA/IP 厂商提前确认 license。
- **超预期乐观**：合规和验证成为客户平台上市瓶颈，测试软件、自动化和 compliance lab 的议价能力上升。

### 2.6 Datacenter PCIe NVMe SSD、EDSFF、U.2/M.2 形态升级

**爆发原因：** DevCon 不是存储大会，但 M.2/U.2/SFF/EDSFF 和 PCIe 线缆化直接决定数据中心 SSD 的形态。AI 训练、checkpoint、向量库、推理 KV cache 和高密度 warm storage 推动企业 SSD 出货与 ASP。

**成熟/量产路线：**

- **基准**：2026 年 PCIe Gen5 企业 SSD 继续成为主流升级方向；Gen6 SSD 仍以样品和少数高端平台为主。
- **乐观**：AI 存储需求和 NAND 供需偏紧让企业 NVMe SSD 维持量价齐升。
- **超预期乐观**：高容量 U.2/EDSFF 和 Gen5/Gen6 控制器供给紧张，企业 SSD 毛利率继续扩张。

## 3. 市场规模、增速和利润率预测

> 口径说明：公开市场报告对同一细分市场的定义差异极大。本表采用“可投资/可产业跟踪口径”，保留区间。利润率为产业链估算或上市公司公开财务的可比口径；不是单一公司的盈利承诺。

| 产品/技术 | 当前可参考市场规模 | 当前利润率/毛利率 | 基准：未来 12 个月 | 乐观：未来 12 个月 | 超预期乐观：未来 12 个月 |
|---|---:|---:|---:|---:|---:|
| PCIe Retimer / signal conditioning / SCM 芯片 | Global retimer 2025 约 **6.9 亿美元**；PCIe 4/5/6 retimer 2025 另有报告给 **13.4 亿美元**；采用可投资口径 **10-14 亿美元** | 高端 fabless 连接芯片 **65-76% GM**；Astera 2026 Q1 GAAP GM **76.3%**；线缆模块 **20-40% GM** | +**25-35%**，到 **13-19 亿美元**；GM 小幅回落到 **68-74%** | +**45-60%**，到 **15-22 亿美元**；高端 GM **70-75%** | +**75-90%**，到 **18-27 亿美元**；供应紧张时 GM **72-78%** |
| PCIe/CXL/Fabric Switch | PCIe switch 2025 公开口径约 **7.26-11.23 亿美元**；AI scale-up merchant market 2030 由 Astera 指向 **200 亿美元** | 高端 switch/fabric 芯片 **60-76% GM**；软件/firmware 诊断能力提高粘性 | +**35%**，到 **11-16 亿美元**；GM **65-72%** | +**70%**，到 **14-20 亿美元**；GM **70-76%** | +**120%**，到 **18-26 亿美元**；若开放 AI fabric 放量，GM **73-78%** |
| CopprLink / AEC / 高速连接器线缆 | Data center AEC 2025 约 **7.38 亿美元**；更宽 AEC 口径约 **16.5 亿美元** | 线缆/连接器 **20-40% GM**；高端有源线缆初期更高，铜价和竞争压制下行 | +**25-30%**；GM 维持 **22-38%** | +**45-55%**；高端 AEC GM **30-42%** | +**70-90%**；若 AI rack 线缆化提前，短期 ASP 上行、GM **35-45%** |
| PCIe over optics / optical-aware retimer / LPO/DSP optics | PCIe-specific optical 仍早期，估计 **<2 亿美元**；AI data center optical interconnect 2025 约 **37.5 亿美元**；整体 optical interconnect 2025 约 **174 亿美元**；LPO 2025 约 **3.58 亿美元** | 光模块 **25-40% GM**；硅光/光引擎/IP 初期 **35-55% GM** | +**40%**，主要来自验证和小批量；PCIe-specific 仍小 | +**80%**，2027 量产项目提前锁单；GM 稳中有升 | +**150%+**，若 optical-aware retimer 成为 AI rack 标准件，2026 订单会先于收入体现 |
| PCIe/CXL IP、VIP、合规工具 | Semiconductor IP 2025 约 **62.5 亿美元**；interface IP 约 **20 亿美元级**；PCIe IP 2025 约 **1.34 亿美元**；CXL component 2025 约 **7.10 亿美元** | IP/EDA 软件 **80-90% GM**；硬件辅助验证/仪器较低但仍高 | +**15-20%**；GM 稳定 | +**30-40%**；Gen8/Gen7 license 提前签 | +**50%+**；合规瓶颈推高验证工具和服务需求 |
| Datacenter PCIe/NVMe SSD、EDSFF/U.2/M.2 | Data center SSD 2025 约 **185 亿美元**；PCIe SSD overall 2025 约 **286 亿美元**；enterprise SSD 2025 口径约 **296.6 亿美元** | NAND/SSD 厂商随周期 **20-35% GM**；控制器 **45-60% GM** | +**12-15%**；Gen5 继续主导 | +**20-25%**；AI 存储和 NAND 供需偏紧 | +**35-45%**；高容量企业盘 ASP 上行，GM 扩张但周期风险高 |
| PCIe-specific test/compliance equipment & labs | 无统一公开口径；估计 **3-7 亿美元** PCIe 相关仪器/协议分析/合规服务可服务市场 | 仪器/软件 **55-65% GM**；lab service **30-50% GM** | +**15-20%**；PCIe 6 compliance 拉动 | +**30-40%**；Gen7/optical 测试方法提前采购 | +**50%+**；若 pass/fail confidence 和 optical correlation 成为量产门槛 |

## 4. 三种情景下的总体产业路径

### 4.1 基准情景

- 2026 年主要收入来自 **PCIe 5/6 Retimer、Smart Cable、PCIe 6 switch、Gen5 enterprise SSD、测试设备升级**。
- PCIe 7.0 主要体现为 IP/PHY/连接器/Retimer 样品和客户验证；2027 开始更多平台设计导入。
- PCIe 8.0 主要贡献研发预算，不贡献实质产品收入；2028 完整发布后，2029-2031 才会进入高端系统量产周期。
- 铜缆/AEC/CopprLink 增长快于光，光主要是 rack/pod reach 的早期导入。

### 4.2 乐观情景

- AI rack 规模继续扩大，开放 merchant accelerator 和 custom ASIC 平台增多，PCIe/CXL/UALink 生态比预期更快成为第二套 scale-up fabric。
- PCIe 6 switch、Retimer、SCM 在 2026 H2 成为头部 AI 平台重要 BOM，fabric switch 收入增速高于 Retimer。
- Optical-aware retimer 和 LPO/DSP optics 在 2027 量产前提前进入 2026 订单和 capex，测试工具/合规服务同步受益。
- 互连芯片厂商毛利率维持 70% 左右，操作杠杆继续改善。

### 4.3 超预期乐观情景

- AI 推理从单节点推理升级到大规模 agentic inference 和长上下文/KV cache 场景，scale-up collective communication 成为瓶颈；高 radix switch、in-network compute、Hypercast 类功能价值被迅速重估。
- 市场发现“GPU 不够，互连也不够”，connectivity silicon 的美元含量按每 accelerator、每 rack 快速上升。
- 新连接器和 optical-aware retimer 成为 PCIe 7/8 的先行事实标准，订单在 2026 就体现，收入在 2027-2028 放大。
- Retimer/switch/AEC/optical 之间出现套片化和平台绑定，高端 ASP 抬升，短期毛利率不降反升。

## 5. 与市场共识可能相违背的洞见

### 5.1 PCIe 8.0 不是 2026 收入主角，但它会立刻改变 2026 研发和设计胜负

市场容易把 2028 final release 理解为“太远”。更正确的看法是：Draft 0.5 已经足以让 hyperscaler、AI ASIC、SerDes、PHY、IP、连接器和 Retimer 团队启动架构选择。2026 的 Gen8 收入小，但 2026 的 Gen8 design win 和 IP lock-in 很关键。

### 5.2 光不会立刻替代铜；短距铜和 AEC 会先爆发

DevCon 同时强调 CopprLink、AEC、DSP optics、LPO 和 optical retimer，说明产业不是单一路线。短距、低成本、低功耗、可维护场景下，AEC/CopprLink 很可能先吃到更确定的量；光先从 reach/pod/rack 复杂拓扑切入。

### 5.3 PCIe 的“后向兼容”不等于连接器形态稳定

PCIe 8.0 公开目标同时写“new connector technology”和“backwards compatibility”。这意味着协议/系统兼容性会尽量保留，但物理形态、连接器、线缆和中继架构可能出现新一轮重构。连接器和线缆厂商的战略地位被低估。

### 5.4 合规和验证可能比硅本身更卡节奏

64 GT/s PAM4 的测量重复性、FLIT/FEC/retry 错误注入、Retimer/optical 模式、system-level correlation 都会拉长产品从样品到量产的时间。测试仪器、协议分析、自动化 compliance 软件和实验室 capacity 有机会变成瓶颈资源。

### 5.5 PCIe switch 正在从“扩 lanes”变成“AI collective 加速器”

Scorpio X-Series 320-lane、Hypercast、In-Network Compute、memory-semantic fabric 这类关键词说明，下一代 switch 不只是转发，而是在 AI 通信模式中承担 collective operation 优化。市场若仍按传统 PCIe switch 估值/空间理解，可能低估这一层的 TAM 扩张。

### 5.6 消费 PC 不是判断 PCIe 7/8 节奏的好指标

PCIe 5.0 在消费 PC 仍未充分用满，但这不代表 PCIe 7/8 没价值。真正的领先应用是 AI server、hyperscale cloud、HPC、800G/1.6T 网络、storage backplane 和 rack-scale accelerator fabric。

## 6. 投资/产业跟踪指标清单

1. **PCIe 6.0 Integrators List 和 compliance workshop 节奏**：若 Gen6 合规推进顺利，Retimer、switch、test equipment 收入确认更顺。
2. **Astera/Broadcom/Marvell/Credo 等高端互连厂商的 Gen6/Gen7 port 出货量和 ASP**：比单看服务器出货更接近真实 attach rate。
3. **AI rack BOM 中 connectivity dollar content per accelerator**：每 GPU/XPU 互连价值量若从几十美元上升到数百美元，TAM 会快速重估。
4. **AEC vs optical 的 reach/功耗/延迟边界**：2 m 内若 AEC 保持优势，铜路线会比市场想象更强；跨 rack/pod 若 optical qualification 提前，光路线弹性更大。
5. **PCIe 7 over optics 的系统级 correlation 结果**：实验室 silicon data 与 full-system simulation 是否能稳定闭环，是 optical PCIe 规模化的前置条件。
6. **PCIe 8.0 新连接器候选方案**：一旦产业选型明确，连接器、线缆、测试夹具和主板设计都会开始重新分配利润池。
7. **CXL/PCIe/UALink 的边界融合**：PCIe physical layer、CXL memory semantic、UALink scale-up protocol 可能在 AI rack 中共同出现，单一协议视角会漏掉真正的系统价值。

## 7. 主要来源

- PCI-SIG Developers Conference 2026 官方页面：<https://pcisig.com/pci-sig-developers-conference-2026>
- PCI-SIG Developers Conference 2026 官方议程与演讲摘要：<https://pcisig.com/pci-sig-developers-conference-2026-agenda>
- PCI-SIG 2026 DevCon 官方博客：<https://pcisig.com/blog/pci-sigr-developers-conference-2026-explore-advanced-technologies-win-exclusive-prizes-and>
- PCIe 8.0 Draft 0.5 官方博客：<https://pcisig.com/blog/pcier-80-specification-draft-05-now-available-track-2560-gts-transfer-speeds-2028>
- PCIe 7.0 1.0 官方资源页：<https://pcisig.com/specifications/pcie-70-specification-version-03-now-available-members>
- PCI-SIG Optical Interconnect Solution 新闻稿转载：<https://markets.financialcontent.com/stocks/article/bizwire-2025-6-11-pci-sig-announces-pcie-optical-interconnect-solution>
- PCIe Retimers and Cables / PCIe 7.0 & 8.0 roadmap 公开演示稿：<https://files.futurememorystorage.com/proceedings/2025/20250805_INDA-102-1_Yanes.pdf>
- Synopsys PCI-SIG DevCon 2026 页面：<https://www.synopsys.com/events/pci-sig-devcon.html>
- Tom's Hardware：PCIe 8.0 Draft 0.5 coverage：<https://www.tomshardware.com/tech-industry/pci-sig-reveals-pcie-8-0-0-5v-spec-first-draft-includes-1-tb-s-bandwidth-and-new-connector-technology>
- Phoronix：PCIe 8.0 Draft 0.5 media briefing coverage：<https://www.phoronix.com/news/PCIe-8.0-Draft-0.5>
- Marvell DesignCon 2026 PCIe 8.0 SerDes demo coverage：<https://www.electronicsmedia.info/2026/02/24/marvell-demonstrates-pcie-8-0-serdes-at-designcon-2026/>
- Astera Labs Q1 2026 results：<https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results>
- Astera Labs FY2025 results：<https://asteralabs.gcs-web.com/news-releases/news-release-details/astera-labs-reports-fourth-quarter-and-full-year-2025-financial>
- Fortune Business Insights Retimer Market：<https://www.fortunebusinessinsights.com/retimer-market-113225>
- Verified Market Research PCIe 4.0/5.0/6.0 Retimer Market：<https://www.verifiedmarketresearch.com/product/pcie-40-50-60-retimer-market/>
- Reanin PCIe Switches Market：<https://www.reanin.com/reports/pcie-switches-market>
- The Market Intelligence PCIe Switch Market：<https://www.themarketintelligence.com/market-reports/pcle-switch-market-1940>
- Data center AEC market：<https://www.24marketreports.com/ict-and-media/global-aec-active-cable-for-data-centers-market>
- Active Electrical Cables market：<https://pmarketresearch.com/chemi/active-electrical-cable-aec-connectors-market/>
- Optical Interconnect in AI Data Centers market coverage：<https://web3wire.org/web3/optical-interconnect-in-ai-data-centers-market-to-reach-18-36-billion-by-2033-at-21-87-cagr-as-ai-infrastructure-drives-ultra-high-speed-connectivity-datam-intelligence/>
- Optical Interconnect Market：<https://www.fundamentalbusinessinsights.com/industry-report/optical-interconnect-market-12983>
- LPO Market：<https://www.marketresearchintellect.com/product/linear-pluggable-optics-lpo-market/>
- Semiconductor IP Market：<https://www.fortunebusinessinsights.com/amp/semiconductor-ip-market-106877>
- PCIe IP Market：<https://www.marketresearchintellect.com/product/pcie-ip-market/>
- Compute Express Link Component Market：<https://www.gminsights.com/industry-analysis/compute-express-link-component-market>
- Data Center SSD Market：<https://www.grandviewresearch.com/industry-analysis/data-center-ssd-market-report>
- PCIe SSD Market：<https://dataintelo.com/report/global-pcie-ssd-market>
# The Xcelerated Compute Show 2026：AI 工厂从 GPU 狂热转向“推理、内存墙、开放互联、吉瓦级供电”的系统级拐点

> 调研口径：仅使用公开外部资料；未参考本项目内既有文件。核心会议材料以 2026 年 3 月 23-24 日纽约场 The Xcelerated Compute Show 为主，辅以官方 stream 页面、SDxCentral/DCD 会前资料、标准组织公开资料、公司财报/新闻稿和市场研究公开摘要。金额均为美元，韩元按约 1,450 KRW/USD 粗略折算；预测为未来 12 个月/2026-2027 过渡期判断。

## 一句话结论

The Xcelerated Compute Show 2026 的信号不是“AI 服务器继续买 GPU”这么简单，而是 AI 基础设施进入第二阶段：训练集群仍然扩张，但主战场开始转向推理经济性、长上下文/KV cache、内存与存储、1.6T/3.2T 网络、开放 scale-up fabric、CXL 级内存池化、neocloud 融资与残值管理，以及吉瓦级电力和场址规划。市场共识仍在用“GPU 供需周期”解释所有增长，但会议议程和公开数据共同指向：2026-2027 年利润池会从单一 GPU 供应链扩散到 HBM/DDR/eSSD、以太网后端网络、AI server ODM/OEM、AI storage、功率/液冷/colo capacity 和推理专用芯片。

## 会议事实与一手材料框架

### 官方会议结构

- 时间/地点：2026 年 3 月 23-24 日，纽约 Marriott Marquis, Times Square。
- 官方 2026 生态画像：2027 页面回顾 2026 生态为 550+ hardware/software decision-makers、150+ speakers、50+ technology providers；参会结构约 37% enterprise、13% hyperscale、11% neocloud、14% colocation、7% supercomputing、18% vendor/channel reseller。
- 官网议程覆盖的轨道：AI Foundations、Building AI Factories、The Future of Hardware & Software、AI Impacts、Networking、Storage & Memory、Full Stack Perspective。
- 官方 stream 页面公开 45 条会后视频，覆盖主舞台、AI factories、networking、storage/memory、inference、quantum 等。
- 官方内容伙伴 SDxCentral 会前 deep-dive 直接列出 6 个议题：neocloud、AI-driven transfers 迫使网络栈重构、AI 如何“制造/打破”存储、sovereign storage、memory crunch、2026 AI inferencing market review。

### 最重要的会议 session 信号

- **AI Labs Are the New Hyperscalers**：SemiAnalysis 参与的开场主题把 AI lab/model builder 从“云上客户”提升为基础设施定价者和容量锚定方。
- **Planning for Gigawatts**：OpenAI infrastructure strategy/capacity planning 主题进入主舞台，说明算力采购已经从 GPU 盒子变成 GW 年度容量规划。
- **GP4U - How the next generation of AI models will impact GPU procurement**：OpenAI 参与，重点是下一代模型形态如何影响 GPU 采购，不再只是“越多越好”。
- **All-In on Inference**：Cerebras、Positron AI、Ampere、ZeroPoint 等出现在同一推理专场，会议明确给了“芯片 underdogs 可能赢”的舞台。
- **Solving for the AI Memory Wall / Context Memory Revolution**：WEKA 主题说明“上下文内存”开始成为独立叙事。
- **AI's Hidden Bottleneck - Memory, Storage Scarcity, and the Race for Sovereign Infrastructure**：Vultr、ZeroPoint、Supermicro、Equinix、MaxLinear 等参与，说明瓶颈已经横跨内存、存储、连接和主权部署。
- **CXL Special Presentation / UALink Special Presentation / Ultra Ethernet Consortium / Ethernet Alliance / Ethernet Wins Again**：标准组织集体进入核心议程，说明 2026 不是单一厂商互联，而是开放互联路线的制度化节点。
- **Neocloud Revolution / Neo kids on the block**：CoreWeave、TensorWave、WhiteFiber、Deep Infra、Vast.ai、FarmGPU、Ori、BluSky 等代表 neocloud 从“矿卡再利用”转为企业 AI 的供给侧。
- **AI Futures - Building the Financial Infrastructure of the AI Economy**：Ornn AI 的残值/互换产品说明 GPU/AI server 已经金融资产化，残值风险将影响 neocloud 的真实利润。

## 重点与发展方向：相比 2024-2025 的变化

### 1. 从训练中心论到推理中心论

2024-2025 年市场更关注大模型训练集群、H100/H200/Blackwell 供给和 hyperscaler capex。2026 年会议把“推理”放到主舞台：agentic AI、长上下文、企业落地、低成本 token、KV cache、边缘/分布式推理成为新约束。NVIDIA FY2026 财报称 Blackwell Ultra 相比 Hopper 在 agentic AI 上性能/成本有 50x/35x 级改进；但这类效率提升不会等同于 capex 下降，因为 agentic workflow 会把调用次数、上下文长度和实时数据访问显著放大。

判断：未来 12 个月，推理相关基础设施支出增速大概率高于训练专用支出增速；训练仍是大额订单来源，但 marginal dollar 更容易流向 inference rack、CPU:GPU 配比、KV cache storage、内存容量和网络带宽。

### 2. 从 GPU 稀缺到“内存/存储/网络/电力”系统稀缺

公开数据验证了会议主题：

- IDC：2025 年全球 AI infrastructure spending 为 $318B，2026 年预计 $487B，增速约 53%；Q4 2025 单季 $89.9B，其中 server 为 $87.7B，占 97.6%。
- IDC：全球 server market 2025 年 $453.5B，2026 年预计 $606.7B，2027 年预计 $873.1B。
- Dell'Oro：AI data center accelerator market 未来五年 CAGR 约 25%；同时明确 memory/storage supply chain 被 AI 增长压紧。
- Micron FQ2-2026：收入 $23.86B，GAAP gross margin 74.4%，FQ3 指引收入 $33.5B、gross margin 约 81%。
- Samsung Q1-2026：总收入 KRW 133.9T，经营利润 KRW 57.2T；DS 半导体收入 KRW 81.7T、经营利润 KRW 53.7T，经营利润率约 65.7%。
- SK hynix Q1-2026：收入 KRW 52.6T、经营利润 KRW 37.6T，经营利润率 72%。

这意味着 AI 供应链的高利润不再只在 GPU：HBM、server DRAM、SOCAMM、PCIe Gen6 eSSD、HBM base die、先进封装、网络 ASIC/交换机和高密度供电同样进入卖方市场。

### 3. 从 proprietary fabric 到开放 scale-up/scale-out 标准竞争

2025 之前，AI 网络叙事往往是 NVIDIA NVLink/NVSwitch + InfiniBand/RoCE。2026 年会议把 UALink、Ultra Ethernet、Ethernet Alliance、CXL 放在显眼位置。关键事实：

- UALink 200G 1.0：定义 accelerator-to-switch 的低延迟高带宽互联，200G per lane，单 AI pod 可扩展到 1,024 accelerators。
- UALink Common 2.0：加入 in-network compute，目标是降低 latency、节省 bandwidth、提升 distributed training/inference scaling efficiency。
- Ultra Ethernet Consortium 1.0/1.0.2：从 NIC、switch、optics、cables 到 transport 的 AI/HPC 以太网栈。
- Dell'Oro：2025 年 AI back-end Ethernet switch sales 超过 InfiniBand 两倍以上，Ethernet 在 AI cluster switch sales 中占超过 2/3；800G 已成主流，1.6T 预计 2026 下半年开始出货，2027 年成为重要收入驱动。

判断：市场仍把 NVLink 视为 scale-up 的默认答案，但会议信号显示，scale-up 也开始被“开放标准 + vendor diversity + 供应链多元化”侵蚀。最有爆发力的是 1.6T Ethernet、UALink switch/IP、co-packaged optics、AI NIC/DPU。

### 4. Neocloud 从 opportunistic GPU rental 变为资产/融资/企业采购通道

会议介绍中明确写到 GPU clouds 起点是 crypto mining GPU reuse，如今已成为 AI ecosystem pillar。变化在于：

- 需求端从少数 model lab 扩散到金融、医药、政府、企业研发。
- 供给端不只是“有 GPU”，而是 metal-to-model 平台、orchestration、SLA、compliance、data locality、financing。
- 残值风险显性化：Ornn AI 这类金融基础设施公司出现，说明 lender/neocloud 开始需要 GPU residual value swap。

判断：neocloud 爆发力度很大，但并非所有 neocloud 都能挣钱。赢家是具备电力/数据中心锁定、低成本融资、长期客户合同、异构硬件调度和残值对冲能力的公司；单纯 GPU 转租会被利用率波动、融资成本、芯片代际折价和内存涨价吞掉利润。

### 5. Sovereign AI 从政治口号变成区域 capex 增量

IDC Q4 2025 数据显示，美国占全球 AI infrastructure spending 的 77%，但 Middle East & Africa Q4 同比增长 535%，达到 $1.8B；中国因出口限制 Q4 同比下降 8.1% 至 $8.4B。会议中的 Canadian Compute、Government AI Future、Sovereign Infrastructure 等主题说明主权 AI 正在成为地区性容量建设逻辑。

判断：2026-2027 年非美国 AI infrastructure 的增速可能高于美国，虽然绝对规模仍小；这会利好可绕开单一出口约束、能做本地化交付/主权云/政府合规的供应商。

## 哪些产品和技术方向会爆发：路线图与爆发力度

### A. AI servers / rack-scale systems

当前事实：

- Dell FY2026 AI-optimized server revenue 为 $24.683B，同比增长 166%；全年 AI server orders 超过 $64B，FY27 期初 backlog $43B。
- Dell 指引 FY2027 AI-optimized server revenue 约 $50B，同比增长约 103%。
- IDC server market：2026 年 $606.7B，2027 年 $873.1B，2027 年同比约 43.9%。

路线：

- 2026：Blackwell/GB200/GB300、B300、MI355X/MI450 early ramps，rack-scale supply chain 继续受 HBM、power shelf、liquid cooling、networking 限制。
- 2027：Vera Rubin、AMD Helios/MI450 family、更多 custom ASIC racks、1.6T switching、HBM4 规模化。
- 2028：3.2T network、CXL/pooled memory 与更标准化 rack integration 普及，AI server 从“项目制”走向更模块化的 hyperscale SKU。

三档预测：

- 基准：未来一年 AI server/relevant server spending +35-45%；OEM operating margin 11-15%，Dell ISG Q4 14.8% 是可参考高位。
- 乐观：+50-60%；memory 供给改善、服务/存储/网络 attach 提升，领先 OEM operating margin 15-18%。
- 超预期乐观：+70% 以上；agentic inference 和 sovereign AI 叠加，Dell 类厂商 AI server revenue 翻倍变成行业常态，领先厂商 operating margin 18-20%。

### B. AI accelerators：GPU + custom ASIC + inference ASIC

当前事实：

- NVIDIA FY2026 Data Center revenue $193.7B，同比增长 68%；Q4 Data Center $62.3B，同比增长 75%；公司 FY2026 gross margin 71.1%，FY2027 Q1 gross margin 指引约 75%。
- Broadcom Q1 FY2026 AI revenue $8.4B，同比增长 106%，Q2 AI semiconductor revenue 指引 $10.7B；公司 adjusted EBITDA margin 约 68%。
- AMD Q1 2026 Data Center revenue $5.8B，同比增长 57%；Meta 计划部署最高 6GW AMD Instinct GPUs，第一阶段 1GW 使用 custom MI450-based GPU；AMD Q2 revenue 指引 $11.2B、non-GAAP gross margin 约 56%。

路线：

- 2026：NVIDIA Blackwell Ultra/GB300 仍是主流；Broadcom custom ASIC 受 hyperscaler 自研需求驱动；AMD MI355X/MI450/Helios 提供第二供应源。
- 2027：NVIDIA Vera Rubin、AMD MI450/MI455X、Google TPU/AWS Trainium/Inferentia/Meta silicon 等 custom ASIC 份额继续上升；inference ASIC 进入更清晰的商业窗口。
- 2028：GPU 仍控制通用训练和复杂推理；ASIC 在大规模稳定 workload 中吃份额；推理专用架构按 batch size、latency、上下文长度分化。

三档预测：

- 基准：AI accelerator/custom silicon revenue +30-40%；GPU 龙头 gross margin 70-75%，ASIC/网络龙头 EBITDA 65-70%，AMD gross margin 向 57-60% 改善。
- 乐观：+45-55%；HBM4 良率改善支撑出货，NVIDIA 维持 75% 左右 gross margin，Broadcom AI revenue 年化 $45-55B。
- 超预期乐观：+65% 以上；agentic inference 使推理算力需求非线性放大，custom ASIC 与 GPU 同时紧缺，利润率维持高位而非均值回归。

### C. HBM / server DRAM / SOCAMM / eSSD：最强利润池之一

当前事实：

- Micron FQ2-2026 revenue $23.86B，GAAP gross margin 74.4%；Cloud Memory revenue $7.749B，gross margin 74%；Core Data Center revenue $5.687B，gross margin 74%；FQ3 revenue 指引 $33.5B、gross margin 约 81%。
- Samsung Q1-2026 DS Division revenue 约 $56B，operating profit 约 $37B，经营利润率约 66%；公司称 memory business 创季度收入和经营利润纪录，并已开始 HBM4 与 SOCAMM2 的 mass product sales，用于 NVIDIA Vera Rubin platform。
- SK hynix Q1-2026 revenue 约 $36B，operating profit 约 $26B，经营利润率 72%，高附加值 HBM/server DRAM/eSSD 是主要驱动。
- TrendForce 公开摘要：2026 年 HBM shipments 预计超过 30 billion Gb，HBM4 在 2026 下半年逐步超过 HBM3E 成为主流；SK hynix 预计仍维持过半份额。

路线：

- 2026：HBM3E 仍贡献大量收入，HBM4 开始放量；SOCAMM、server DDR5、高容量 RDIMM、PCIe Gen5/Gen6 eSSD 被 AI server 拉动。
- 2027：HBM4/HBM4E、高容量 server memory、KV cache SSD 成为 AI rack 标配；供给扩张但仍受 TSV、先进封装、EUV DRAM 和良率制约。
- 2028：HBM4E/更高堆叠与定制 base die 扩大，内存厂从周期股逻辑转为 AI infrastructure bottleneck 资产。

三档预测：

- 基准：AI memory/HBM 相关 revenue +45-60%；领先厂 gross margin 65-75%，operating margin 55-70%，价格高位缓慢回落。
- 乐观：+70-90%；HBM4 价格 premium、AI server DRAM 短缺、eSSD 需求一起推高 ASP，Micron/Samsung/SK hynix 维持 70%+ gross/operating margin 的时间拉长。
- 超预期乐观：+100% 以上；长上下文/agentic workload 让 KV cache 与 memory capacity 需求超过 GPU 出货增速，HBM/DDR/eSSD 成为 AI capex 的最紧约束。

### D. AI backend networking：800G 到 1.6T/3.2T，Ethernet 继续赢

当前事实：

- Dell'Oro：AI back-end switch market 到 2030 年将超过 $100B；Ethernet 预计在 scale-up 和 scale-out 都占主导。
- 2025 年 AI back-end Ethernet switch sales 同比超过 3 倍，并在 Q4 和全年占 AI cluster data center switch sales 超过 2/3。
- 800G 已占 AI back-end Ethernet shipments/revenue 的大多数；1.6T 预计 2026 下半年开始出货，推动 2027 收入和份额变化。
- NVIDIA + Celestica 2025 年 AI cluster Ethernet switch sales 合计近 50% 份额，Arista 第三，Cisco、HPE/Juniper、新进入者加速。

路线：

- 2026：800G 主流，1.6T sampling/early deployments，RoCE/UEC 优化、多厂商 Ethernet AI fabric 成为 hyperscaler/neocloud 默认选项之一。
- 2027：1.6T 大规模收入化；co-packaged optics、silicon photonics、AI NIC/DPU 和 congestion control 成为差异点。
- 2028：3.2T 准备/早期部署，scale-up Ethernet/UALink/ESUN 与 proprietary fabric 长期共存。

三档预测：

- 基准：AI back-end switching/fabric revenue +50-70%；switch/NIC silicon gross margin 60-75%，box/system gross margin 25-45%。
- 乐观：+80-100%；1.6T 提前规模化，Ethernet 在 neocloud 和 hyperscaler 中继续替代 InfiniBand。
- 超预期乐观：+120% 以上；scale-up 也显著开放化，UALink/UEC/ESUN 共同把 proprietary fabric 溢价压缩，但整体 market size 放大。

### E. UALink / UEC / CXL：开放互联与解耦内存的制度化窗口

当前事实：

- UALink 200G 1.0 支持 200G per lane、最多 1,024 accelerators/pod。
- UALink Common 2.0 引入 in-network compute。
- CXL 4.0 在 2025 年发布，带宽从 64GT/s 到 128GT/s，并支持 bundled ports、native x2 link width、更长 channel reach 和 memory RAS。
- 会议把 CXL Consortium、UALink Consortium、UEC、Ethernet Alliance 放进正式议程，说明标准生态已经从 paper/spec 进入客户教育和产品化阶段。

路线：

- 2026：CXL memory expander/pooling 仍以 PoC、少量 production pilot 为主；UALink/UEC 产品进入 IP、switch silicon、reference design、early rack 方案。
- 2027：CXL 3.x/4.0 相关 switching、memory pooling、KV cache/large memory tiering 开始在 hyperscaler/AI lab 小规模生产化；UALink first-generation product ramps。
- 2028：CXL/UALink/UEC 从“架构选项”进入 procurement checklist。

三档预测：

- 基准：CXL/UALink/UEC 直接产品收入仍小，约 $1-5B 级，但增长 +100% 左右；IP/silicon 毛利 60%+，系统集成毛利 20-35%。
- 乐观：+200-300%；KV cache 与 memory pooling 成为推理成本优化刚需，CXL memory appliance 和 UALink switch 提前量产。
- 超预期乐观：+400% 以上；开放 scale-up fabric 被多个 hyperscaler/neocloud 同时采用，2027 年订单可见性超过市场预期。

### F. AI storage / KV cache / data platform

当前事实：

- IDC Q4 2025 AI infrastructure storage spending 为 $2.2B，仅占 AI infrastructure 的 2.4%，但会议中 storage/memory 相关 session 密集出现。
- Dell FY2026 storage revenue $16.631B，仅同比 +1%；但 AI server 出货越多，后续 checkpoint、training data、RAG、KV cache、model registry 和 data governance 的滞后需求越强。
- Samsung 明确提到 PCIe Gen6 SSDs 与 KV cache storage demand；Micron/Samsung/SK hynix 的高 margin 说明企业级 NAND/eSSD 也在被 AI 重新定价。

路线：

- 2026：高性能 parallel file/object、NVMe-oF、GPU-direct storage、AI-native data platform 从训练 checkpoint 扩展到推理 KV cache。
- 2027：PCIe Gen6 eSSD、CXL-attached memory tier、storage-aware scheduler 进入主流 AI factory。
- 2028：存储不再只是成本项，而成为 token latency/cost 的决定性路径。

三档预测：

- 基准：AI storage/eSSD/data platform spending +35-50%；存储软件 gross margin 70-80%，硬件/eSSD gross margin 45-70%，OEM operating margin 10-20%。
- 乐观：+60-80%；KV cache storage 成为推理 rack 必需品，Dell/NetApp/Pure/VAST/WEKA/CoreWeave storage attach 提升。
- 超预期乐观：+100% 以上；长上下文和 agentic memory 需求使 storage spending share 从 2-3% 提升到 5%+。

### G. Power / cooling / high-density colo

当前事实：

- 会议出现 AI Factory Playbook、Planning for Gigawatts、AI Factory Alliance、dense inference rack 等主题。
- NVIDIA 宣布与 CoreWeave 深化合作，支持到 2030 年超过 5GW AI factories buildout。
- DCD 报道 OpenAI 已声明其 2029 之前的 AI infrastructure capacity 目标涉及 10GW 级容量。
- IDC 将 power generation/grid capacity 视为 2026 年 AI infrastructure 的首要 operational bottleneck。

路线：

- 2026：70-120kW/rack 继续上升，liquid cooling、power shelf、onsite/substation、PPA、grid interconnection 成为订单前置条件。
- 2027：GW campus 的电力、冷却、水、土地、网络连通和融资同步锁定；推理 workload 向电力便宜、网络可达、合规允许的地区迁移。
- 2028：AI factory 运营效率从 PUE 转向 tokens/W、tokens/$、network utilization、memory utilization。

三档预测：

- 基准：AI-related power/cooling/colo capex +25-35%；成熟 colo EBITDA margin 40-60%，设备 gross margin 20-40%。
- 乐观：+40-55%；GW campus 能源协议加速，液冷与电力设备订单提前。
- 超预期乐观：+70% 以上；sovereign AI、model lab 与 hyperscaler 三方抢电，capacity 资产 re-rating。

## 市场规模、增速和利润率：三档汇总表

| 重要方向 | 当前可观测规模 | 基准：未来一年 | 乐观：未来一年 | 超预期乐观：未来一年 | 利润率判断 |
|---|---:|---:|---:|---:|---|
| AI infrastructure | 2025 $318B；2026 IDC 预测 $487B | +30-40%，至 $630-680B | +45-55%，至 $700-750B | +65%+，至 $800B+ | 上游芯片/内存高；系统集成低双位数；colo EBITDA 高但资本密集 |
| 全球 server market | 2026 IDC $606.7B；2027 IDC $873.1B | +35-45% | +50% | +60%+ | OEM operating margin 10-16%，AI attach 好的厂商更高 |
| AI-optimized server | Dell FY26 $24.7B，FY27 指引 $50B；全球为数百亿美元到千亿美元级 | +50% | +80% | +100%+ | Dell ISG FY26 11.7%、Q4 14.8%；未来 12-18% |
| GPU/custom AI accelerator | NVIDIA DC FY26 $193.7B；Broadcom AI Q1 annualized $33.6B/Q2 guide annualized $42.8B；AMD DC Q1 annualized $23B | +30-40% | +45-55% | +65%+ | NVIDIA GM 71-75%；Broadcom EBITDA 68%；AMD GM 55-60% |
| HBM/AI memory/DC memory | Micron FQ2 $23.9B；Samsung DS Q1 ~$56B；SK hynix Q1 ~$36B；HBM pure TAM 约 $70-100B 级推测 | +45-60% | +70-90% | +100%+ | 领先 memory 厂 GM/OPM 60-80%，短期强于历史周期 |
| AI backend networking | 2025 已为百亿美元级；Dell'Oro 2030 >$100B | +50-70% | +80-100% | +120%+ | Silicon GM 60-75%；box GM 25-45%；光模块/系统视供应紧缺而扩张 |
| CXL/UALink/UEC direct products | 2026 约 $1-5B early market | +100% | +200-300% | +400%+ | IP/silicon GM 60%+；系统 20-35% |
| AI storage/KV cache/eSSD | IDC Q4 2025 AI infra storage $2.2B；2026 年约 $10B+ 级 | +35-50% | +60-80% | +100%+ | 软件 GM 70-80%；eSSD/内存高景气 GM 45-75%；OEM OP 10-20% |
| Power/liquid cooling/colo capacity | AI facility/power/cooling 为数百亿美元级 capex；GW 项目成为核心 | +25-35% | +40-55% | +70%+ | 设备 GM 20-40%；colo EBITDA 40-60%，但 ROIC 受电力和融资成本约束 |

## 与当前市场可能相违背的重要洞见

### 1. “GPU 越贵越好”的简单逻辑会失效

下一阶段最大增量不一定全在 GPU ASP，而在整体系统利用率。GPU 仍然是最大利润池，但如果 memory、network、storage、power 任一环节不足，GPU 利用率下降，客户会优先采购能提升 tokens/$ 的系统部件。HBM、server DRAM、eSSD、NIC、switch、storage scheduler 的边际价值会被重估。

### 2. Ethernet 可能不只是 scale-out winner，也可能侵入 scale-up

市场通常认为 proprietary scale-up fabric 防线很强；但 Dell'Oro 已明确判断 Ethernet 将在 scale-up 和 scale-out 长期占优，UALink 也在争夺 accelerator pod 内部互联。供应链多元化、vendor diversity、成本、可运维性会驱动客户牺牲部分封闭生态极限性能，换取大规模可采购性。

### 3. 推理专用芯片不是“反 NVIDIA”，而是 workload segmentation

Cerebras、Positron、Ampere、ZeroPoint 等进入 All-In on Inference 专场，说明市场开始承认不同 batch size、latency、model size、context length、功耗约束下最优硬件不同。NVIDIA 仍会控制通用性和生态，但推理市场会比训练市场更碎片化，under-dog 的胜率更高。

### 4. Memory company 的利润率可能不是周期顶部，而是新定价框架

历史上 DRAM 高利润常被视为周期反转前兆；但 2026 年的不同是 HBM、server DRAM、SOCAMM、eSSD 被 AI infrastructure 绑定，且供给扩张受先进封装/TSV/EUV/yield 限制。Micron 81% gross margin 指引、Samsung DS 约 66% operating margin、SK hynix 72% operating margin 是非常强的信号：至少未来 12 个月，memory 利润率均值可能显著高于过去十年。

### 5. Neocloud 的赢家可能不是 GPU 最多者，而是资产负债表最像基础设施公司的玩家

GPU 租赁表面毛利可观，但 Blackwell/Rubin/MI450 迭代会制造残值风险。会议中出现 AI financial infrastructure 和 residual value 产品，说明融资成本、折旧、合同期限、利用率和客户信用质量会决定 neocloud 生死。CoreWeave 类公司如果能锁定长期客户/电力/供应链，价值更接近 AI utility；小型转租商则更像高 beta cyclical leasing。

### 6. Storage share 当前太低，反而可能是超额收益点

IDC Q4 2025 AI infra storage share 仅 2.4%，看起来不重要；但会议中 storage/memory session 密集，Samsung 也把 KV cache storage 写入未来需求。若 agentic/long-context workload 起量，storage share 从 2.4% 到 5% 就意味着数百亿美元增量，而市场目前更容易忽略。

### 7. Quantum 在会议中有存在感，但 2026-2027 不是主要商业爆发点

Quantum 被多场讨论覆盖，但标题本身包含“Accelerator or Science Project?”和“2 years or 20?”，说明行业仍在校准时间表。短期投资应把 quantum 视为 HPC/AI ecosystem 的可选长期 upside，而非未来一年 AI infrastructure capex 的主线。

## 投资/产业链排序

### 未来 12 个月最确定

1. HBM/HBM4、server DRAM、SOCAMM、AI eSSD：供给约束强，利润率最高，需求能见度强。
2. AI backend networking：800G 到 1.6T，Ethernet/UEC/UALink/CPO/NIC/DPU 是高增速。
3. AI-optimized servers/rack integration：收入规模大，Dell 指引可见度强，但利润率弹性低于上游。
4. Custom AI ASIC + GPU：仍是最大收入池；NVIDIA/Broadcom 是核心，AMD 有第二供应源弹性。
5. Power/liquid cooling/colo capacity：增长确定但项目、区域、电力接入和融资差异大。

### 未来 12-24 个月赔率最高

1. CXL/pooled memory：小基数，若 KV cache/内存池化生产化，弹性巨大。
2. Inference ASIC/alternative accelerators：不是全面替代 GPU，而是在明确 workload 中突破。
3. AI storage/data platform：当前 spending share 低，长上下文/agentic workflow 可能重定价。
4. Neocloud financial infrastructure：残值、利用率、融资产品会成为新赛道。

### 最大风险

- 电力/并网延迟导致硬件订单递延。
- HBM/DRAM/eSSD 价格过快上涨，挤压 OEM/neocloud 利润，拖慢企业部署。
- Export controls 改变地区需求和供应商份额。
- Agentic AI 商业化慢于预期，推理 capex 从“指数增长”回落到“线性增长”。
- Open standards 产品化节奏慢，proprietary ecosystem 继续锁定高端性能。

## 关键数字清单

- The Xcelerated Compute Show 2026 NY：2026 年 3 月 23-24 日；550+ decision-makers，150+ speakers，50+ technology providers。
- 官方 stream：45 条会后视频。
- IDC AI infrastructure：2025 年 $318B；2026 年预测 $487B；2029 年超过 $1T；Q4 2025 单季 $89.9B。
- IDC AI infrastructure Q4 2025：server $87.7B，占 97.6%；storage $2.2B，占 2.4%；美国 $69.2B，占 77%；中东/非洲 $1.8B，同比 +535%。
- IDC server market：2025 $453.5B；2026 $606.7B；2027 $873.1B。
- NVIDIA FY2026：总收入 $215.9B；Data Center $193.7B；gross margin 71.1%；Q4 Data Center $62.3B。
- Broadcom Q1 FY2026：AI revenue $8.4B，同比 +106%；Q2 AI semiconductor revenue 指引 $10.7B；adjusted EBITDA margin 68%。
- AMD Q1 2026：总收入 $10.253B；Data Center $5.8B，同比 +57%；Q2 revenue 指引 $11.2B；Meta 计划最高 6GW AMD Instinct GPU。
- Dell FY2026：AI-optimized server revenue $24.683B；orders 超过 $64B；backlog $43B；FY2027 AI server revenue 指引约 $50B。
- Micron FQ2 2026：收入 $23.86B；GAAP gross margin 74.4%；FQ3 revenue 指引 $33.5B，gross margin 约 81%。
- Samsung Q1 2026：总收入 KRW 133.9T；operating profit KRW 57.2T；DS revenue KRW 81.7T；DS operating profit KRW 53.7T。
- SK hynix Q1 2026：收入 KRW 52.6T；operating profit KRW 37.6T；operating margin 72%。
- Dell'Oro AI back-end switch：2030 年超过 $100B；2025 年 Ethernet AI back-end switch sales 超过 InfiniBand 两倍以上；800G 已是主流，1.6T 预计 2026H2 开始出货。
- UALink 200G 1.0：200G per lane，最多 1,024 accelerators/pod。
- CXL 4.0：128GT/s，较 3.x 64GT/s 翻倍；加入 bundled ports、native x2、memory RAS 等。
- CoreWeave/NVIDIA：到 2030 年支持超过 5GW AI factories buildout。
- OpenAI：公开报道显示已宣称锁定 10GW 级 AI infrastructure capacity，以支撑 2029 前目标。

## Sources

- The Xcelerated Compute Show 2026 agenda: https://www.xceleratedcompute.com/new-york/2026/2026-agenda/
- The Xcelerated Compute Show 2026 stream page: https://www.xceleratedcompute.com/new-york/2026/stream-the-2026-event/
- The Xcelerated Compute Show Knowledge & Insights: https://www.xceleratedcompute.com/new-york/2026/knowledge-insights/
- The Xcelerated Compute Show 2027 page with 2026 ecosystem recap: https://www.xceleratedcompute.com/new-york/2027/
- SDxCentral, Scaling AI Infrastructure from silicon to software: https://www.sdxcentral.com/resources/scaling-ai-infrastructure/
- DCD, The AI Week Supplement: https://www.datacenterdynamics.com/en/magazines/the-ai-week-supplement/
- IDC, AI infrastructure Q4 2025 / 2026 forecast: https://www.idc.com/resource-center/blog/ai-infrastructure-spending-caps-historic-year-at-90-billion-in-q4-2025-2029-spending-to-eclipse-1-trillion/
- IDC, Servers Market Insights: https://www.idc.com/promo/servers/
- Dell'Oro, AI back-end switch market forecast: https://www.prnewswire.com/news-releases/ai-back-end-switch-market-will-push-past-100-billion-by-2030-according-to-delloro-group-302678344.html
- Dell'Oro, accelerator-led infrastructure spending: https://www.prnewswire.com/news-releases/hyperscale-ai-investment-cycle-anchors-accelerator-led-infrastructure-spending-according-to-delloro-group-302684398.html
- Dell'Oro, Ethernet vs InfiniBand in AI back-end networks: https://newswire.telecomramblings.com/2026/03/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025-according-to-delloro-group/
- NVIDIA FY2026 results: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/
- AMD Q1 2026 results: https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results
- Broadcom Q1 FY2026 results: https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial
- Dell FY2026 results PDF: https://investors.delltechnologies.com/node/19176/pdf
- Micron FQ2 2026 results: https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026
- Samsung Q1 2026 results: https://news.samsung.com/ca/samsung-electronics-announces-first-quarter-2026-results
- SK hynix Q1 2026 results: https://news.skhynix.com/q1-2026-business-results/
- UALink specifications: https://ualinkconsortium.org/specification/
- Ultra Ethernet Consortium 1.0 specification announcement: https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/
- CXL 4.0 specification announcement: https://www.businesswire.com/news/home/20251118275848/en/CXL-Consortium-Releases-the-Compute-Express-Link-4.0-Specification-Increasing-Speed-and-Bandwidth
- DCD, OpenAI 10GW AI infrastructure capacity report: https://www.datacenterdynamics.com/en/news/openai-claims-to-have-secured-10gw-of-ai-infrastructure-capacity-ahead-of-2029-target/
- TrendForce HBM4 manufacturing complexity / HBM shipment outlook: https://www.trendforce.com/presscenter/news/20250522-12589.html
- TrendForce AI server shipments 2026: https://www.trendforce.com/presscenter/news/20260120-12887.html
