# MLSys 2026会议追踪：核心变化、产品爆发和市场预期差

报告完成日期：2026-06-10（America/Los_Angeles，本机时间）

材料检索截止日期：2026-06-10

会议日期：用户口径为 2026-05-17 至 2026-05-22；MLSys 官网 Dates 页把主会写为 2026-05-18 至 2026-05-22，其中 Young Professionals Symposium 为 2026-05-18，Conference Sessions 为 2026-05-19 至 2026-05-21，Industry Day 为 2026-05-22；OpenReview 会议组页面显示 2026-05-17。本文按 2026-05-17 至 2026-05-22 作为追踪窗口，具体议程以官网主会日程为锚。

会议地点：Hyatt Regency Bellevue，Bellevue, Washington, USA。

研究边界：本报告为独立会议追踪底稿，未读取、引用或继承项目内既有公司调研、行业调研、日度资料、特征量化、tmp、data、索引、缓存或中间结论。事实锚来自会议官网、官方日程、论文页、比赛页、公司材料、公开 IR/市场资料和少量非官方参会分享。非官方信息只作为线索或情绪，不单独支撑核心判断。

## 结论摘要

MLSys 2026 的核心变化不是“又一轮 AI 叙事升温”，而是 AI 基础设施进入以推理成本、SLO、KV cache、异构硬件、自动化内核开发和生产平台化为中心的工程优化阶段。短期可交易的主线不是“更多模型参数”，而是“每美元 tokens、每瓦 tokens、每 GB HBM 支撑的上下文长度、每个工程师维护的 kernel 数量、每个集群的有效利用率”。

最大变化：

- 推理系统从单机/单框架优化转向分布式系统优化。官网日程出现 6 个 LLM Serving 相关 session，Modular 会后复盘称今年 LLM serving session 数量约为去年的两倍。核心瓶颈集中在 prefill/decode 分离、KV cache 管理、MoE serving tax、heterogeneous GPU/accelerator placement、SLO-aware scheduling、跨节点通信和 profiling。
- “AI 写系统代码”从概念变成可评估的工程流。Mark Saroufim 和 Lidong Zhou 的 keynote 都把 AI 生成内核、系统代码、规格和验证作为主题，但共同强调 zero-trust verification：生成不是瓶颈，验证、benchmark、spec 和防作弊才是瓶颈。AWS Trainium、Google graph scheduling、NVIDIA FlashInfer 三个 competition track 也把这个方向变成可复现的 benchmark 与生态入口。
- 异构硬件的市场信号更强。NVIDIA Blackwell/B200/GB200 仍是绝对主轴，但会议材料同时出现 AWS Trainium2/3 NKI、Google scheduling competition、AMD HipKittens/CDNA3-CDNA4、Groq SRAM-based LPU、PyTorch ExecuTorch、Modular MAX/Mojo、SAKURAONE open network GPU cluster。这不是“CUDA 被替代”，而是客户开始要求推理工作负载在多硬件、多网络、多软件栈之间有更低切换成本。
- 生产平台材料比纯研究更有投资信息。Netflix AIP lightning talk 披露生产模型参数范围 100M 到 70B、峰值 500K+ RPS、live inference sub-ms latency；Waymo 披露截至 2025-12 的 170M+ rider-only miles 及 foundation model 架构；SAKURA 披露数百 GPU 中等规模集群、Top500 第 49、开放网络栈。这些材料比单篇论文更能指向真实预算、运维痛点和利润池位置。

最大机会：

- 近 3 个月：KV cache、prefill/decode disaggregation、MoE serving、kernel DSL、inference profiler、SLO-aware scheduler 的开源/产品落地最值得跟踪。会议已经给出大量论文和可运行代码线索，客户痛点明确，采购口径能落到 GPU/HBM 节省和 SLO 达标。
- 未来 1 年：AI inference routing、heterogeneous serving、agentic kernel generation、production AI platform、GPU/accelerator observability 会从研究系统变成云厂、AI cloud 和企业内部平台的采购项。软件收入弹性不一定大，但会显著改变 GPU/HBM/网络利用率和云推理毛利。
- 未来 2 年：自研/定制加速器和开放互联栈的价值取决于软件成熟度，而不是峰值 FLOPS。AWS、Google、AMD、Groq、Lemurian、Together AI、Modular 等能否把 kernel、runtime、benchmark、生态训练做出来，会决定 NVIDIA 以外供应的实际可用容量。

最大分歧：

- 市场可能高估“AI 自动写 kernel”本身，低估验证、benchmark 和生产安全成本。会议材料显示 agent 可以写出高分解，但也会 exploit benchmark、绕开 verifier 或把证明负担转移给调用者。
- 市场可能低估 KV cache 和 routing 的产品化价值。KV cache 正从 engine 内部优化变成跨 GPU、跨节点、跨实例、跨冷热存储的分布式资源，价值捕获不只在模型服务框架，还在网络、HBM、SSD、本地内存、router、observability 和调度层。
- 市场可能把“异构硬件”误读为 NVIDIA 份额立刻下滑。更现实的路径是 NVIDIA 继续吃高端系统利润，同时客户用 AMD、Trainium、TPU、Groq、ASIC 和 CPU/edge runtime 做局部 workload offload、成本对冲和供应链谈判。

最值得跟踪的产品和节点：

- NVIDIA/FlashInfer：FP8 Fused MoE、DeepSeek sparse attention、Qwen3-Next Gated Delta Net kernel，B200/B300/GB300 上的真实吞吐、TTFT、P99 latency 和开发者采用。
- AWS Trainium2/3：NKI MoE kernel challenge、Qwen3-30B-A3B MoE 推理、Trn3 access、Neuron SDK 版本迭代和 winner code 可复现性。
- Google TPU/调度：Graph Scheduling Competition 的 Track A/Track B winner code、2026-07-11 之前的开源承诺、TPU fleet goodput 和 scheduling 产品化。
- Modular MAX/Mojo：B200、B300、AMD MI355x 上相同 stack 的性能可复现性；如果 2026H2 真实客户 workload 能复现 1.5x throughput、2.5x P99 TTFT 或更高幅度，软件利润池会被重新定价。
- Netflix/Waymo/SAKURA/Databricks：内部 AI platform 的组织与预算变化。它们提供的是“企业大规模生产 AI”样板，不是单点模型 demo。

## 会议重点和方向变化

### 会议事实锚

- 会议定位：MLSys 2026 是第九届 Conference on Machine Learning and Systems，聚焦 ML 与系统交叉，包括 efficient training/inference/serving、LLM training/fine-tuning/inference、compound AI systems、distributed/federated learning、privacy/security、ML compilers/runtimes、specialized hardware、hardware-efficient ML、benchmarks/tooling。
- 议程结构：2026-05-18 为 YPS 和 sponsor lightning talks；2026-05-19 至 2026-05-21 为主 conference sessions；2026-05-22 为 Industry Day。
- Keynotes：Mark Saroufim 讲 AI writing systems code；Lidong Zhou 讲从 MLSys 到 system intelligence；Amin Vahdat 以 Google AI infrastructure 负责人身份出席；Luke Zettlemoyer 与 Christos Kozyrakis 分别代表模型/系统与体系结构方向。
- 2026 新增 Industry Track：官方 CFP 明确要求 industry authors，聚焦真实系统的 retrospective evaluation、product/deployment roadmap 或 canceled system lessons，强调 production-scale benchmarking 和 design methodology。这意味着会议从研究导向更靠近产业落地和客户预算。
- Competition Track：官方宣布 AWS Trainium2/3 MoE Kernel Challenge、Google Graph Scheduling Competition、NVIDIA FlashInfer AI Kernel Generation Contest 三个比赛，分别对应非 CUDA custom accelerator、调度优化和 NVIDIA kernel generation。
- Sponsor/exhibitor hall layout 中出现 Amazon、Google、PyTorch、ByteDance、Netflix、Waymo、Databricks、Modular、Crusoe、Capital One、Jane Street、Lemurian、Together AI、Tencent、Luma、Verda、InfrAct、Inception、Wooly.ai 等，参展结构本身说明 MLSys 已经成为 AI infra 招聘、生态和客户沟通场。

### 5-10 个核心主题

| 主题 | MLSys 2026 证据 | 对应公司/产品/技术 | 变化性质 | 投资含义 |
|---|---:|---|---|---|
| LLM Serving 成为主会中心 | 日程中 R1/R2/R3/R14/R15/R18 等 LLM Serving session；Modular 统计今年 6 个 LLM serving sessions，约为去年 2 倍 | vLLM、SGLang、Modular MAX、Meta inference deployment、NVIDIA disaggregation、Groq SHIP、PyTorch SymmetricMemory | 加速 | 从训练 capex 叙事转向推理 opex/TCO 叙事；GPU 利用率、HBM、网络、router 成为利润池 |
| KV cache 资源化 | FlexiCache、SkipKV、OPKV、RAGBoost、RagInfer、streaming prefill、span queries 等论文密集出现 | KV cache offload、paged cache、prefix reuse、RAG context reuse、cache routing | 真实变化，已有代码/论文，商业化早期 | 直接影响长上下文、agent、RAG 的 serving cost；云推理毛利和应用价格战的关键变量 |
| Prefill/decode disaggregation 和异构部署 | Meta industry paper 显示单模型部署中异构 prefill/decode 有 15-25% TCO 改善；NVIDIA 论文强调 rate matching、KV transfer、cache routing、elastic scaling 必须同时解决 | NVIDIA GH200/GB200/GB300、B200、heterogeneous GPU placement、TriInfer encode-prefill-decode | 从概念转入产品验证 | 不是单点 kernel 问题，而是调度、网络、缓存、弹性扩缩容系统机会 |
| MoE 和 sparse attention 进入推理工程期 | AWS Trainium MoE challenge 使用 Qwen3-30B-A3B；FlashInfer contest Track A 为 FP8 Fused MoE，Track B 为 DeepSeek sparse attention，MoE serving tax 论文出现 | Trainium2/3、NVIDIA B200、DeepSeek sparse attention、Qwen3、Mixtral/DeepSeek 类 MoE | 真实需求，但优化复杂 | MoE 降 FLOPs 不等于降 serving cost；AllToAll、padding、expert imbalance 和 JIT spike 可能侵蚀利润 |
| AI agents 写 kernel/系统代码 | Mark Saroufim keynote、Lidong Zhou keynote、AccelOpt、FlashInfer-Bench、competition track | GPU MODE、PyTorch、AWS NKI、NVIDIA FlashInfer、Google Gemini scheduling contest | 加速但需验证 | 工具价值在 benchmark、profiling、DSL、CI 和 verification，不在“自动写代码”口号 |
| Kernel DSL 和多硬件抽象 | FlashAttention-4 用 CuTe-DSL embedded in Python；HipKittens 研究 AMD kernel primitives；ParallelKittens 简化 multi-GPU kernel | CuTe-DSL、Triton、Tilelang、Mojo、HipKittens、ParallelKittens | 真实变化 | 非 CUDA 生态的瓶颈从硬件峰值转为开发者效率；AMD/Trainium/TPU 的真实份额取决于工具链 |
| Production AI platform | Netflix AIP、Waymo ML Platform、SAKURAONE、Databricks research/engineering 招聘和 workshops | Netflix model serving、Waymo foundation model、SAKURAONE HPC、Databricks agent/scaling/retrieval teams | 已有部署 | 企业 AI 基础设施预算会流向 feature store、observability、runtime、model lifecycle、agent platform |
| Secure/private/federated ML | R8 Federated Learning、R10 Security and Privacy，含 NVIDIA GPU confidential computing、homomorphic encryption、unlearning proofs | NVIDIA confidential GPU、federated LLM fine-tuning、secure aggregation | 早期但有合规需求 | 短期收入弱于推理优化，长期受金融、医疗、政府和自动驾驶带动 |
| Edge/on-device AI runtime | ExecuTorch、IntAttention、mobile LLM DVFS、CORE 等论文/材料 | PyTorch ExecuTorch、Qualcomm/Arm ecosystem、mobile NPUs | 稳步推进 | 对 GPU capex 不是替代，更多是端侧低延迟、隐私和离线场景增量 |

### 和上一届及过去 6-12 个月预期相比的变化

1. LLM serving 从“框架优化”升级为“跨资源编排”。2025 年市场更关注 vLLM、PagedAttention、batching、speculative decoding 等局部效率。MLSys 2026 的材料显示，下一阶段问题是 cache、router、GPU/accelerator、网络、CPU/内存、SSD、弹性调度共同优化。

2. AI codegen 的产业落点变窄但更真实。过去 6-12 个月市场叙事容易把 agent 写代码等同于生产力暴增。会议材料更务实：agent 在 kernel/search/scheduling 上有用，但必须在可验证 benchmark、限制条件和生产安全里工作。这个变化有利于 benchmark、CI、profiler、spec 和 DSL 工具，不一定有利于泛化的 AI coding SaaS。

3. 异构硬件从“备选供应”变成“推理成本设计项”。NVIDIA 仍处于利润池中心，但 AWS、Google、AMD、Groq、Lemurian、Modular、Together AI 等材料说明，客户在推理阶段更愿意按 workload 拆分硬件：prefill、decode、MoE expert、dense attention、embedding、batch/offline、edge runtime 的硬件最优解可能不同。

4. Industry Track 改变了会议含金量。新增 Industry Track 要求真实系统、生产环境 benchmarking、deployment roadmap，这比纯论文更接近预算。SAKURAONE、Meta inference deployment、Netflix AIP、Waymo ML platform 这类材料可以作为客户采用信号。

5. 利润池从“卖 GPU”外溢到“提高 GPU 有效利用率”。NVIDIA Q1 FY2027 Data Center revenue 为 75.2B 美元、Data Center compute revenue 约 60.4B 美元、networking revenue 约 14.8B 美元，说明硬件主链条仍大；但 MLSys 2026 的技术密度说明未来一年推理利润率的边际改善会来自 software-defined utilization。

### 真实变化、叙事和远期可选性

| 变化 | 证据强度 | 当前判断 |
|---|---:|---|
| KV cache/disaggregated inference 产品化 | 高：多篇论文、公司复盘、Meta/NVIDIA/Groq 产业论文、实际 serving 指标 | 真实变化，未来 12 个月最值得跟踪 |
| Agentic kernel generation | 中高：keynotes、AccelOpt、FlashInfer contest、AWS/Google/NVIDIA competitions | 真实工具趋势，但商业收入仍早期 |
| 非 NVIDIA accelerator 快速替代 NVIDIA | 中低：Trainium/TPU/AMD/Groq 证据增加，但生态和供应仍落后 | 方向真实，替代节奏不宜过度乐观 |
| 企业 internal AI platform 标准化 | 中高：Netflix/Waymo/SAKURA/Databricks 证据 | 真实变化，但外部软件供应商变现路径分化 |
| Privacy/confidential/federated ML 立即大规模收入 | 中：论文多，客户痛点真实 | 远期可选性，短期不是主线收入 |
| Edge/on-device LLM 对 data center capex 形成替代 | 中低：ExecuTorch 和 mobile DVFS 有进展 | 补充而非替代；更可能扩大 AI 使用场景 |

## 产品和技术路线三情景预测

以下预测为投资研究估算，不是会议官方数字。市场规模口径采用 2026 年公开资料和本报告假设链条：NVIDIA Q1 FY2027 数据中心收入年化、Gartner/IDC/TrendForce 对 AI spending、AI infrastructure、AI server、memory/HBM 的公开预测，以及本届会议暴露出的技术成熟度。置信度分三档：高为已有公司披露或多源一致，中为公开市场数据加可复核假设，低为早期软件/工具收入估算。

| 方向 | 当前成熟度（截至 2026-06-10） | 3个月节点 | 1年节点 | 2年节点 | 2026 当前市场规模口径 | 2027 三情景预测 | 利润率和价值捕获 |
|---|---|---|---|---|---:|---|---|
| KV cache 管理、cache router、disaggregated inference | 论文密集、vLLM/SGLang/云内部系统已有实现；商业产品早期 | 开源 repo、benchmark、云厂内部 A/B；看 P99 TTFT、GPU memory saving | 成为云 inference 平台默认模块，服务长上下文/RAG/agent | 跨区域/跨集群 cache routing 与冷热分层标准化 | 估算 1-3B 美元软件/托管服务收入；影响 100B+ 美元级推理硬件利用率 | 基准 3-7B；乐观 7-12B；超预期 12-20B | 软件毛利理论 70-90%，但开源压价；最大价值被云厂和 AI cloud 以内化毛利捕获 |
| Prefill/decode/encode disaggregation 和异构 serving | Meta/NVIDIA/TriInfer/Groq 等生产或接近生产证据 | 大模型 API 服务商采用，关注 KV transfer 和 rate matching | 成为多 accelerator fleet 的调度标准 | 推理集群按 phase 采购不同硬件 | 直接产品收入估算 2-5B；影响 GPU/HBM/网络 150B+ 采购 | 基准 6-12B；乐观 12-25B；超预期 25-40B | 若 TCO 改善 15-25% 可支撑高预算；利润池在云厂、NVIDIA networking、router/profiler |
| MoE 推理优化与 FP8/sparse attention kernels | Qwen3/DeepSeek 类模型带动，FlashInfer/AWS NKI 竞赛验证 | Winner code 复现、模型服务框架合并 kernel | MoE serving tax 降低，MoE API 价格下行 | 多硬件 MoE expert parallel runtime 成熟 | 2026 MoE 相关推理硬件/服务估算 20-40B 美元；工具收入小于 1B | 基准 45-75B；乐观 75-110B；超预期 110-160B | 硬件利润在 GPU/ASIC/HBM；软件价值在 all-to-all、expert routing、padding reduction、kernel library |
| Agentic kernel generation 和系统代码 verification | Keynote、AccelOpt、FlashInfer-Bench、竞赛轨道，仍需强验证 | 建立 benchmark 和防作弊 harness | 成为 kernel/编译器团队的内部开发流 | 与 CI、spec、formal verification 深度绑定 | 估算 0.3-1.0B 美元工具收入；更多是研发效率杠杆 | 基准 0.8-2.5B；乐观 2.5-6B；超预期 6-12B | 独立 SaaS 毛利可高，但客户更可能买一体化平台或内部化；价值捕获在平台/云/芯片公司 |
| Kernel DSL、多硬件 abstraction、portable runtime | CuTe-DSL、HipKittens、ParallelKittens、Mojo/MAX、Triton/Tilelang 多线并行 | CUDA 之外硬件 kernel 覆盖扩张 | AMD/Trainium/TPU/Groq 部分 workload 进入可迁移部署 | 形成跨硬件 AI compiler/runtime 层 | 2026 直接商业软件 1-3B；间接影响 250B+ accelerator 市场 | 基准 3-8B；乐观 8-18B；超预期 18-35B | 价值捕获不在 DSL 本身，而在降低非 NVIDIA 迁移成本后带来的硬件议价和云毛利改善 |
| AI inference observability、profiling、SLO optimizer | ProfInfer、OptiKIT、NodeSweep、ML goodput 类论文；企业平台已有痛点 | 集成到 vLLM/SGLang/Kubernetes/云监控 | 成为大型企业 AI platform 必备项 | 与自动调度、容量规划和财务系统结合 | 估算 2-6B 美元 AIOps/LLMOps 子市场 | 基准 6-12B；乐观 12-22B；超预期 22-35B | 软件毛利高；但若被 Datadog/New Relic/云监控打包，纯创业公司利润池受挤压 |
| Production AI platform（Feature store、observability、runtime、agent platform） | Netflix AIP、Waymo、Databricks、Capital One/Jane Street 参展或材料 | 组织扩招、内部平台采购 | 企业 AI 平台从 PoC 进入标准化预算 | 行业模板沉淀到金融、媒体、交通、零售 | Gartner 2026 AI spending 2.52T 美元大口径；本层直接软件/服务估算 40-80B | 基准 80-130B；乐观 130-200B；超预期 200-300B | SaaS/平台毛利 65-85%，实施和定制服务 25-45%；真正高利润在可复用平台能力 |
| AI networking、HBM、server memory/storage | NVIDIA networking Q1 FY2027 14.8B 美元，HBM/DRAM 紧缺，TrendForce 2026 memory market 551.6B 美元 | 800G/1.6T 网络、HBM3E/HBM4 供给、SSD/cache tier | AI inference pull-in 改变采购节奏 | HBM4、co-packaged optics、rack-scale memory 更重要 | AI networking 年化 60-90B；HBM 估算 70-95B；memory 大盘 551.6B | networking 基准 90-140B、乐观 140-200B、超预期 200B+；HBM 基准 100-150B、乐观 150-220B、超预期 220B+ | 供给瓶颈期毛利上行；价值捕获在 NVIDIA networking、Broadcom/Marvell ASIC/NIC、SK hynix/Samsung/Micron、台积电先进封装 |
| Edge/on-device AI runtime | ExecuTorch、mobile LLM DVFS、integer attention；产品化仍早 | 手机/PC NPU demo 和开发者工具 | 端侧小模型、隐私场景落地 | 端云协同推理标准化 | 直接软件 2-5B；端侧 AI SoC 更大但口径不同 | 基准 5-10B；乐观 10-20B；超预期 20-35B | 价值更多在 SoC、OS、模型压缩和应用分发；不是本届 MLSys 最大利润池 |

### 爆发力度判断

- 主链条替代：MoE/sparse attention kernels、prefill/decode disaggregation、KV cache routing 有机会改变推理主链条，但必须以真实 SLO 和成本复现为准。
- 供给瓶颈涨价：HBM、AI networking、advanced packaging、high-end server memory/storage 仍具供给约束，会议技术方向会继续放大这些部件需求。
- 小品类高增速：agentic kernel tools、LLM profiler、cache router、benchmark/verification 平台收入基数小但增速高。
- 客户架构切换：生产 AI platform 会推动企业从“模型 API 调用”转向“内部模型生命周期、runtime、observability、feature/vector store、agent platform”架构。
- 新市场从 0 到 1：AI-generated systems code 的商业化仍处 0 到 1，但最先赚钱的不是通用 coding agent，而是与 kernel benchmark、formal spec、CI、profiling 绑定的专门工具。

## 市场规模和利润池

### 大盘口径

- AI infrastructure：IDC 公开资料显示 AI infrastructure spending 预计 2029 年达到 758B 美元，accelerated servers 到 2029 年占 server AI infrastructure spending 超过 95%，五年 CAGR 约 42%。第三方引用 IDC tracker 的口径显示 2025 年 AI infrastructure spending 约 334B 美元。按 42% CAGR 反推，2026 年大致落在 450-500B 美元区间。置信度：中。
- AI spending：Gartner 2026-01-15 新闻稿预测 2026 年 worldwide AI spending 为 2.52T 美元，同比增 44%，其中 AI infrastructure 作为驱动项增加 401B 美元。该口径包含硬件、软件、服务和终端，不适合作为 MLSys 直接 TAM，但适合作为总预算约束。置信度：中高。
- NVIDIA data center：NVIDIA 2026-05-20 公布 Q1 FY2027 总收入 81.6B 美元，Data Center revenue 75.2B 美元，同比 92%，Data Center compute revenue 约 60.4B 美元，Data Center networking revenue 约 14.8B 美元，GAAP gross margin 74.9%。这是当前 AI 硬件利润池最强事实锚。置信度：高。
- AMD data center：AMD 2026-05-05 公布 Q1 2026 收入 10.3B 美元，GAAP gross margin 53%，non-GAAP gross margin 55%，Data Center segment 由 EPYC 和 Instinct 推动增长。AMD 是第二供应和开放生态核心候选，但公开分项不足以直接拆出 Instinct 利润。置信度：高。
- AI server：TrendForce 2025-10-30 公布 2026 年 AI server shipments 预计同比增长超过 20%，AI server 占 overall server shipments 比重升至 17%。这说明单位数服务器数量占比能贡献远高于数量占比的收入和利润。置信度：中。
- Memory/HBM：TrendForce 2026-01-22 预计 memory market 2026 年 551.6B 美元，2027 年 842.7B 美元，同比 53%。HBM 是该增长中的高价值子集，但公开免费材料未给出完整 HBM revenue，本文按 AI accelerator/HBM attach 做估算。置信度：中。

### 利润池分层

| 层级 | 2026 规模口径 | 当前利润率/单位经济 | 未来一年利润率方向 | 价值捕获判断 |
|---|---:|---|---|---|
| GPU/AI accelerator | NVIDIA Data Center compute Q1 FY2027 年化约 240B 美元；全市场估算 270-330B 美元 | NVIDIA corporate GM 74.9%；AMD corporate GM 53%/non-GAAP 55% | 高端仍强；若 supply 增加和 API 价格战加剧，单位利润率可能从峰值回落 | NVIDIA 继续捕获最大利润；AMD/custom ASIC 更像成本和供应对冲 |
| AI networking | NVIDIA networking Q1 FY2027 年化约 59B 美元，估算 2026 全市场 60-90B | 高端 NIC/switch/IB/Ethernet 毛利高，随绑定系统提升 | 推理分布式化会增加流量和低延迟需求，毛利偏上 | NVIDIA、Broadcom、Marvell、Arista、Celestica/ODM 和光模块链条受益 |
| HBM/DRAM/advanced memory | memory 大盘 551.6B 美元，HBM 估算 70-95B | HBM 供给紧时毛利显著高于 commodity DRAM | 2026-2027 供需仍偏紧，价格和 mix 支撑利润 | SK hynix、Samsung、Micron、TSMC CoWoS/SoIC 及测试封装设备受益 |
| Inference serving software | 估算 8-15B 美元直接收入，间接影响 100B+ 硬件 opex | 开源核心压价；托管/企业版毛利 65-85% | 若能量化 TCO savings，ASP 上行；若被云厂打包，独立厂商承压 | 云厂、AI cloud、Databricks、Modular、Together AI、vLLM/SGLang 周边服务 |
| Agentic kernel/tools | 估算 0.3-1.0B 美元 | 早期，高毛利但销售周期长 | 需要 proof/benchmark/CI 才能卖给生产团队 | 更可能被芯片、云、编译器平台内化 |
| Enterprise AI platform | 估算 40-80B 美元软件/服务直接口径 | SaaS 65-85%，服务 25-45% | 大企业从 PoC 转平台化，预算增长 | Databricks、Snowflake、cloud AI platform、observability、security、feature/vector infra |
| Edge/on-device AI | 直接 runtime/tools 2-5B，SoC/设备口径更大 | 软件弱，SoC 强 | 随端侧模型和隐私需求增长 | Qualcomm、Apple、MediaTek、Arm、PyTorch ExecuTorch 生态 |

### 成本和价格的可证伪假设

- 若 KV cache/serving 优化能稳定降低 20% 以上 GPU memory footprint 或 P99 latency，云推理价格可以继续下降而保持毛利；若只能在 benchmark 上成立，价值回到硬件扩容。
- 若 prefill/decode disaggregation 的跨节点 KV transfer、rate matching 和 elastic scaling 无法自动化，15-25% TCO 改善会被工程复杂度吃掉。
- 若 MoE serving tax 保持 2-3x 级别而不能通过 kernel、parallelism 和 routing 降低，MoE 模型的理论 FLOPs 优势不能全部转化为 API 毛利。
- 若 HBM 价格和交期继续上行，KV cache 优化的经济价值被放大；若 HBM 供给超预期释放，cache 软件的议价能力下降但整体推理量增长。
- 若 NVIDIA Blackwell/GB300 继续保持系统级吞吐和生态优势，异构硬件更多是补充；若 Trainium/TPU/AMD/Groq 在特定 workload 达到 30%+ TCO 优势且开发成本降低，硬件份额会发生可见迁移。

## 反共识洞见和重要更新

### 市场可能过度乐观的方向

1. “AI 自动写 kernel 会马上替代系统工程师”过度乐观。Mark Saroufim keynote 和 Modular 复盘都强调，agent 会 exploit benchmark，Lidong Zhou keynote 中也出现模型通过绕开 verifier 或移动证明负担来“过关”的问题。结论：agentic kernel 工具会提高专家效率，但不会消灭验证、spec、profiling 和生产代码审查。

2. “Prefill/decode disaggregation 必然降本”过度乐观。NVIDIA 产业材料的核心提醒是，disaggregation 只有在 rate matching、KV transfer、cache routing、elastic scaling 同时解决时才有价值。只把 prefill 和 decode 拆成两组 GPU，可能增加网络和调度成本。

3. “MoE 模型天然推理便宜”过度乐观。MoE serving tax 论文把问题拆成 arithmetic intensity、AllToAll、padding、expert imbalance、phase-dependent overhead。MoE 降低 activated FLOPs 不等于降低端到端 serving cost。

4. “非 NVIDIA accelerator 只差硬件峰值”过度乐观。MLSys 2026 显示瓶颈更多在 kernel abstraction、profiling、runtime、collectives、debugging、benchmark 和生态。AMD、Trainium、TPU、Groq 要吃份额，必须证明生产 workload 的开发和维护成本也可控。

5. “会议 sponsor 都是直接受益股”过度乐观。Netflix、Waymo、Capital One、Jane Street 作为生产用户和招聘方，其会议曝光更多证明内部平台成熟，不等同于其股票对 AI infra 成本优化有高弹性。

### 市场可能低估的方向

1. KV cache 是新的系统资源。它不再只是 vLLM 的内存技巧，而是跨模型、跨请求、跨节点、跨冷热存储、跨检索上下文的可调度资产。谁能管理 cache，谁就能影响 GPU memory、HBM、SSD、network 和 P99 latency。

2. Inference profiler 和 SLO optimizer 会成为预算项。ProfInfer、OptiKIT、NodeSweep、ML goodput 等材料说明，企业不是缺模型，而是缺“为什么慢、为什么贵、为什么尾延迟爆炸、为什么集群有效利用率低”的答案。

3. 生产 AI platform 的内部架构开始趋同。Netflix AIP 的 data/observability、runtime/compute、model serving、developer enablement 四层，与 Databricks hiring、Waymo ML lifecycle latency、SAKURA cluster operation 的问题高度一致。未来企业 AI 平台会更像数据平台加运行时平台，而不是聊天 UI。

4. 非 CUDA 生态最先突破的不是训练，而是特定推理 kernel 和 cloud-offloaded workload。AWS NKI MoE、Google scheduling、AMD HipKittens、Groq SHIP 都指向“把特定 workload 做到 TCO 可用”，而不是一次性全面替代 CUDA。

5. Networking 和 memory 是推理优化的隐形主线。KV transfer、prefill/decode、MoE AllToAll、long context、multi-agent memory 都把压力推到网络和内存层。AI server 数量增长可能只有 20%+，但高价值部件收入增长更快。

### 看起来相关但收入弹性不强的公司/产品

- 只有“agent”应用层叙事、没有自有 serving stack、没有大规模 GPU 预算、没有企业 platform 控制点的公司，受益弱。
- 只做模型 demo 的公司，如果不能把 cache reuse、batching、routing、observability 和成本优化内化，毛利会被上游 GPU/云推理价格决定。
- 传统 IT 服务公司如果只做 AI platform 实施，收入可能增长但利润率不一定提升；高利润在可复用 runtime/observability/security 产品。
- 参展但缺少公开产品、客户、benchmark、IR 支撑的小公司，只能作为线索，不能作为核心投资结论。

### 最可能有投资弹性的小环节

- Kernel benchmark/verification 平台：小 TAM 高增速，客户是芯片、云、AI infra 团队，预算来自研发效率和生产可靠性。
- KV cache router 和 observability：若能证明节省 GPU/HBM 或降低 P99 tail latency，ROI 直接。
- AI networking/collectives 工具链：TokenWeave、SymmetricMemory、NVSHARP、Ultra Ethernet/UALink 生态都说明 collectives 是重要控制点。
- Advanced memory 和测试封装：HBM/CoWoS/SoIC/测试设备的产能、良率和交期会决定 AI infra 交付节奏。
- Non-CUDA kernel portability：HipKittens、Mojo/MAX、Tilelang、Triton、CuTe-DSL 的可迁移性若被证实，会提高 AMD/Trainium/TPU 的实际可用供给。

### 需要立刻下修的反证条件

- 2026Q3-Q4 大模型 API 价格下降超过 50%，但相关云/AI cloud 毛利没有改善，说明 serving 优化被价格竞争吃掉。
- HBM3E/HBM4 交期明显缩短且价格回落，cache/software 的节省价值低于预期。
- AWS Trainium/Google TPU/AMD/Groq 的 competition winner code 无法在真实 workload 复现，或开发维护成本显著高于 CUDA。
- Prefill/decode disaggregation 在生产中导致更多 tail latency 和 incident，无法自动 rate match。
- Agentic kernel generation 只能优化固定 benchmark，无法进入 production CI 或长期维护。

## 公司和产业链映射

### 头部硬件和云平台

| 公司/平台 | MLSys 2026 证据 | 收入暴露 | 投资弹性判断 |
|---|---|---|---|
| NVIDIA | FlashInfer contest、B200 GPU access、Blackwell 相关论文、confidential GPU、disaggregation、networking | Data Center Q1 FY2027 75.2B 美元；compute 60.4B；networking 14.8B；GM 74.9% | 仍是最大利润池。会议强化了 networking、software stack 和 kernel library 护城河 |
| Google | Amin Vahdat keynote、Graph Scheduling Competition、TPU fleet/goodput 相关论文 | 主要以内化 capex 和云服务毛利体现 | 投资弹性间接，重点看 TPU 外部化、GCP AI margin、调度系统复用 |
| Amazon/AWS | AWS Trainium2/3 MoE Kernel Challenge、Amazon Science AccelOpt paper | Trainium 主要提升 AWS AI 服务成本结构 | 若 Trainium3/NKI 生态成熟，对 AWS 推理毛利和客户锁定有正向影响 |
| AMD | HipKittens、CDNA3/CDNA4 kernel abstraction、MI350/MI400 外部路线 | Q1 2026 total revenue 10.3B，GM 53%，Data Center 增长 | 会议支持“软件生态补课”方向；短期仍需客户 benchmark 证伪/证实 |
| Groq | SHIP paper：SRAM-based public cloud serving hundreds of billions tokens daily | 私营，收入不公开 | 产品路线清晰，适合低延迟推理；受限于模型规模、容量和生态 |

### AI cloud、runtime 和软件平台

| 公司/项目 | 会议证据 | 收入暴露 | 投资弹性判断 |
|---|---|---|---|
| Modular | 赞助、会后复盘、MAX/Mojo 性能主张：B200、B300、AMD MI355x 多硬件 stack | 私营，直接卖 inference platform | 若真实客户复现性能，弹性高；风险是 benchmark 与生产差距 |
| Together AI | 赞助页显示 MLSys 2026 platinum sponsor，定位 accelerated compute、production inference、model shaping、research | 私营 AI cloud/inference | 受益于推理增长，但毛利取决于硬件采购和利用率 |
| Databricks | 展位、networking event 285 went，招聘 ML systems、agent systems、scaling/efficiency、retrieval research roles | 数据/AI 平台收入，外部软件化能力强 | 会议显示其在 AI infra 人才和生态上加码；受益于 enterprise AI platform |
| PyTorch/Meta ecosystem | PyTorch 参展，ExecuTorch、SymmetricMemory、PyTorch inference optimization 论文 | Foundation 非营利；Meta 内化价值 | 对生态控制和开发者锁定极重要，间接强化 Meta/NVIDIA/云合作 |
| vLLM/SGLang/FlashInfer | 多篇 serving 和 kernel 论文、competition | 多为开源，商业化通过云、托管、企业服务 | 高技术影响，直接收入不一定高；被云厂内化概率大 |

### 生产应用和企业平台样板

| 公司 | 会议材料 | 关键数字 | 投资含义 |
|---|---|---:|---|
| Netflix | AIP lightning talk | 生产模型 100M 到 70B 参数；peak 500K+ RPS；live inference sub-ms latency | 证明媒体/广告/推荐/内容生成的 AI platform 已进入生产规模；但 Netflix 作为股票的 AI infra 弹性主要体现为效率和体验，不是卖工具 |
| Waymo | ML at Waymo lightning talk | 截至 2025-12，170M+ rider-only miles；相对平均 human driver 的若干 crash reduction 指标 | 自动驾驶 ML lifecycle latency、data selection、foundation model 是真实工程问题；对 compute 和数据平台需求高 |
| SAKURA internet | Industry Track paper | SAKURAONE 数百 GPU，中等规模 LLM 开发；Top500 第 49；Top100 中唯一完全开放网络栈 | Sovereign AI 和开放网络栈的样板；对日本 AI infra 和开放以太网/网络供应有意义 |
| Capital One/Jane Street | 展位图出现 | 无公开技术数字 | 更像招聘和生产用户信号；金融低延迟/风控/合规 AI platform 有潜在需求 |

### 上游瓶颈和配套

- HBM/DRAM：SK hynix、Samsung、Micron。受益于 KV cache、long context、MoE、larger batch、multi-agent memory；风险是 2027 供给释放和价格回落。
- Advanced packaging：TSMC CoWoS/SoIC、ASE、Amkor、测试设备。AI accelerator 交付瓶颈之一。
- Networking/optics：NVIDIA Spectrum-X/InfiniBand、Broadcom/Marvell ASIC/NIC、Arista、Coherent/Lumentum/光模块链。Prefill/decode、MoE AllToAll 和 distributed cache 直接拉动。
- Server ODM/OEM：Supermicro、Dell、HPE、Quanta、Wistron、Foxconn、ZT Systems/AMD。价值取决于整机毛利和交付能力，不一定等于高利润。
- Observability/security：Datadog、New Relic、云监控、Wiz/安全栈、GPU confidential computing 生态。AI workload 可观测性会成为新监控类别。

### 伪受益或弱受益

- 没有自有模型 serving 成本结构的应用公司。
- 只卖“AI agent”概念但不能证明长任务 durable execution、checkpoint、trace learning 和 failure recovery 的公司。
- 没有硬件、没有平台、没有客户数据、只做会议营销的 sponsor。
- 传统咨询/集成商若缺可复用 runtime 或 observability 产品，收入增但利润率弹性有限。

## 风险、反证条件和后续跟踪

### 主要风险

- 技术指标不可复现：MLSys 论文和 contest 常在受控 benchmark 中成立，生产 workload 的 traffic mix、tail latency、multi-tenant isolation、debugging、incident recovery 会显著降低收益。
- 开源压价：vLLM、SGLang、FlashInfer、Triton、PyTorch 等开源项目提高行业效率，但可能压低独立软件供应商 ASP。
- 硬件供给变化：HBM、packaging、networking、power/cooling 任一瓶颈变化都会重估 cache 和 serving 软件的价值。
- 云价格战：如果模型 API 价格下降快于成本下降，推理优化变成客户让利而非供应商利润。
- 合规和安全：agentic systems code、autonomous kernel generation、confidential GPU、federated learning 都可能遇到审计、认证和安全门槛。
- 地缘和出口管制：NVIDIA/AMD/Trainium/TPU 供给、客户地域和 HBM/先进制程均受政策影响。

### 后续刷新节点

| 时间 | 节点 | 需要看什么 |
|---|---|---|
| 2026-06 至 2026-07 | Google Graph Scheduling Competition winner code 截止开源窗口 | code 是否按承诺开放；benchmark 是否可复现；Track B agent 是否真正泛化 |
| 2026-07-22 至 2026-07-23 | AMD Advancing AI 2026 | MI400/Helios/UALink/Ultra Ethernet、客户 benchmark、ROCm/DSL 工具链 |
| 2026Q2-Q3 财报 | NVIDIA、AMD、Broadcom、Marvell、Arista、Micron、SK hynix、Samsung | AI data center revenue、networking、HBM ASP、gross margin、backlog、capex |
| 2026H2 | PyTorchCon、Hot Chips、OCP、GTC/云厂大会 | ExecuTorch、SymmetricMemory、Blackwell/GB300、Trainium3、TPU、open Ethernet |
| 2026-11 至 2026-12 | AWS re:Invent、NeurIPS/MLSys follow-up | Trainium3 外部客户、Neuron SDK、agentic kernel 工具商业化 |
| 每月 | vLLM/SGLang/FlashInfer/Modular release notes | KV cache、MoE、disaggregation、B200/B300/AMD 支持、benchmark |

### 跟踪指标

- 推理：TTFT、TPOT、P50/P95/P99 latency、tokens/s/GPU、tokens/s/W、tokens/s/$、GPU memory footprint、cache hit rate、KV transfer bandwidth、SLO violation rate。
- 硬件：B200/B300/GB300/MI350/MI400/Trainium/TPU/Groq LPU 的实际可用容量、HBM 容量和带宽、interconnect bandwidth、NIC attach rate。
- 供应链：HBM 价格、CoWoS/advanced packaging 产能、800G/1.6T 网络交付、液冷交付周期、电力并网和机柜功率。
- 商业：云推理 API 价格、AI cloud gross margin、enterprise AI platform 合同金额、Databricks/Snowflake/cloud AI attach rate、GPU rental utilization。
- 研发：agentic kernel benchmark 复现率、production CI 接入率、自动生成 kernel 的 rollback/incident 数量、verification pass/fail 统计。

## 来源清单

### 一手官方会议材料

| 来源 | 日期/材料时间 | 类型 | 可信度 | 用途 |
|---|---|---|---:|---|
| MLSys 2026 官网：https://mlsys.org/ | 2026-05 至 2026-06 检索 | 会议官网 | 高 | 会议名称、地点、主题、keynote、topics |
| MLSys 2026 Dates：https://mlsys.org/Conferences/2026/Dates | 2026-06-10 检索 | 会议官方日期 | 高 | 主会日期、YPS、Conference Sessions、Industry Day |
| MLSys 2026 Schedule：https://mlsys.org/virtual/2026/calendar | 2026-06-10 检索 | 官方议程 | 高 | session、oral、poster、keynote、LLM Serving 分布 |
| MLSys 2026 Invited Talks：https://mlsys.org/virtual/2026/eventlistwithbios/Invited%20Talk | 2026-06-10 检索 | 官方 keynote 信息 | 高 | Mark Saroufim、Lidong Zhou、Amin Vahdat、Christos Kozyrakis |
| MLSys 2026 Industry Track CFP：https://mlsys.org/Conferences/2026/CallForIndustrialTrackPapers | 2026-06-10 检索 | 官方 CFP | 高 | Industry Track 的真实系统、deployment roadmap、production benchmark 要求 |
| MLSys 2026 Sponsor Hall Layout PDF：https://mlsys.org/static/core/mlsys_sponsor_layout.pdf | 2026-06-10 检索 | 官方展位图 | 中高 | sponsor/exhibitor 映射 |
| OpenReview MLSys 2026：https://openreview.net/group?id=MLSys.org%2F2026%2FConference | 2026-06-10 检索 | 论文/会议组 | 高 | 论文入口、日期交叉校验 |

### 一手公司和项目材料

| 来源 | 日期/材料时间 | 类型 | 可信度 | 关键事实 |
|---|---|---|---:|---|
| Netflix AIP MLSys 2026 slides：https://mlsys.org/media/SponsorLightningTalks/sponsors/MLSys%202026/130-netflix-loc130.pdf | 2026-05-18 | sponsor lightning talk | 高 | 100M 至 70B 参数生产模型、500K+ RPS、sub-ms live inference、AIP 四层 |
| Waymo MLSys 2026 slides：https://mlsys.org/media/SponsorLightningTalks/sponsors/MLSys%202026/17-waymo-loc17.pdf | 2026-05 | sponsor lightning talk | 高 | 170M+ rider-only miles through Dec 2025、foundation model、ML systems challenges |
| SAKURA internet Industry Track release：https://www.sakura.ad.jp/corporate/en/information/2026/04/20/1968224368/ | 2026-04-20 | 公司新闻稿 | 高 | SAKURAONE 数百 GPU、Top500 第 49、开放网络栈、Industry Track paper |
| Amazon Science MLSys 2026：https://www.amazon.science/conferences-and-events/mlsys-2026 | 2026-05 | 公司研究页 | 高 | AccelOpt accepted publication |
| AWS Trainium2/3 MoE Kernel Challenge：https://github.com/aws-neuron/nki-moe | 2026-05 | 官方 GitHub | 高 | Qwen3-30B-A3B、NKI、Trainium2/3、winner list |
| Google Graph Scheduling Competition：https://github.com/yarongmu-google/MLSys | 2026-05 | 官方 GitHub | 高 | Track A/Track B、winner scores、2026-07-11 开源窗口 |
| NVIDIA/FlashInfer AI Kernel Generation Contest：https://mlsys26.flashinfer.ai/ | 2026-05 | 官方竞赛页 | 高 | FP8 Fused MoE、DeepSeek sparse attention、Qwen3-Next GDN、B200 credits、winner list |
| PyTorch MLSys 2026 event：https://pytorch.org/event/mlsys-2026/ | 2026-05 | Foundation event page | 高 | 会议关注 LLM training/inference、compound AI、distributed/federated、hardware-efficient ML、privacy/security |
| Databricks @ MLSys event：https://luma.com/vz5b8fjm | 2026-05 | 公司活动页 | 中高 | 285 went、research/engineering hiring、accepted workshops、booth |
| Together AI MLSys 2026：https://www.together.ai/mlsys-2026 | 2026-05 | 公司活动页 | 中 | accelerated compute、production inference、model shaping、research |
| Modular MLSys 2026 recap：https://www.modular.com/blog/three-trends-from-mlsys-2026 | 2026-05-29 | 公司会后复盘 | 中 | 6 个 LLM serving sessions、agentic engineering、KV cache、heterogeneous hardware、MAX benchmark 主张 |

### 技术论文和材料

| 来源 | 日期/材料时间 | 类型 | 可信度 | 用途 |
|---|---|---|---:|---|
| FlashAttention-4 MLSys poster：https://mlsys.org/virtual/2026/poster/3536 | 2026-05 | 官方论文页 | 高 | B200、Blackwell asymmetric scaling、1.3x vs cuDNN、2.4x vs Triton、1605 TFLOPs/s、CuTe-DSL |
| HipKittens MLSys poster：https://mlsys.org/virtual/2026/poster/3512 | 2026-05 | 官方论文页 | 高 | AMD CDNA3/CDNA4 kernel abstraction、1.2-2.4x in some settings |
| SHIP MLSys oral：https://mlsys.org/virtual/2026/oral/3834 | 2026-05 | 官方论文页 | 高 | Groq SRAM-based public cloud serving hundreds of billions tokens daily |
| FlexiCache arXiv：https://arxiv.org/abs/2511.00868 | v2 2026-04-20 | 技术论文 | 中高 | KV cache 70% memory reduction、1.38-1.55x throughput、1.6-2.1x token latency |
| Demystifying the Mixture of Experts Serving Tax：https://openreview.net/pdf/760b399272fea324af0953a789a27cfe0f64e994.pdf | 2026-05 | 论文 PDF | 中高 | MoE serving tax、2-3x overhead、prefill/decode phase differences |

### 市场和财务材料

| 来源 | 日期/材料时间 | 类型 | 可信度 | 关键数字 |
|---|---|---|---:|---|
| NVIDIA Q1 FY2027 results：https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx | 2026-05-20 | 公司财报 | 高 | revenue 81.6B、Data Center 75.2B、GM 74.9%、Data Center compute/networking |
| AMD Q1 2026 results：https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results | 2026-05-05 | 公司财报 | 高 | revenue 10.3B、GAAP GM 53%、non-GAAP GM 55% |
| Gartner AI spending：https://www.gartner.com/en/newsroom/press-releases/2026-1-15-gartner-says-worldwide-ai-spending-will-total-2-point-5-trillion-dollars-in-2026 | 2026-01-15 | 市场研究新闻稿 | 中高 | 2026 worldwide AI spending 2.52T、同比 44%、AI infrastructure adds 401B |
| IDC AI infrastructure：https://my.idc.com/getdoc.jsp?containerId=prUS53894425 | 2025-11 | 市场研究新闻稿 | 中高 | AI infrastructure spending 2029 758B、accelerated servers >95%、42% CAGR |
| TrendForce AI server：https://www.trendforce.com/presscenter/news/20251030-12762.html | 2025-10-30 | 市场研究新闻稿 | 中 | 2026 AI server shipments +20% 以上、AI servers 占 server shipments 17% |
| TrendForce memory market：https://www.trendforce.com/presscenter/news/20260122-12893.html | 2026-01-22 | 市场研究新闻稿 | 中 | memory market 2026 551.6B、2027 842.7B、2027 同比 53% |
| Dell'Oro data center infrastructure 2026 predictions：https://www.delloro.com/2026-predictions-data-center-infrastructure/ | 2026-01 | 市场研究博客 | 中 | accelerated servers、GPU/custom accelerators、HBM、NIC/network pull-through |

### 非官方和二手材料

| 来源 | 日期/材料时间 | 类型 | 可信度 | 使用方式 |
|---|---|---|---:|---|
| Karnbir Khera LinkedIn MLSys 2026 experience | 2026-05 下旬 | 个人参会分享 | 低 | 只用于参会情绪和展位互动线索，不支撑核心结论 |
| Youjie Li LinkedIn MLSys 2026 ByteDance talk | 2026-05 | 个人分享 | 低 | ByteDance veScale sponsor/publication talk 线索，未作为主要财务判断 |
| Ashok Emani LinkedIn MLSys 2026 recap | 2026-05 下旬 | 个人复盘 | 低 | CUDA/CuTeDSL/agent transfer 等市场情绪线索，需一手材料验证 |

