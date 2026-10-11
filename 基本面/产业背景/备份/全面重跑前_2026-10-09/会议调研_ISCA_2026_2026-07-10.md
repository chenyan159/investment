# 会议追踪：ISCA 2026——架构红利从算力密度转向数据移动、内存与能效

> **会议**：53rd International Symposium on Computer Architecture（ISCA 2026）  
> **会议日期**：2026-06-27 至 2026-07-01  
> **地点**：美国北卡罗来纳州 Raleigh，Raleigh Convention Center  
> **材料检索截止时间**：2026-07-10（美国太平洋时间）  
> **报告完成日期**：2026-07-10  
> **研究边界**：本报告只使用 ISCA 官方材料、论文/作者公开版本、项目页、代码/数据集及公司一手材料重新研究；未读取、引用或继承项目内既有公司调研、行业调研、会议报告、日度资料、特征量化、缓存或中间结论。

## 结论摘要

1. **本届最强信号不是“再造一个更大的矩阵乘单元”，而是重构数据移动。** 两篇 Best Paper 分别处理大规模 MoE 推理中的专家数据移动，以及 HBM/LPDDR 的跨层 ECC；官方议程又安排了五个 LLM 专场、多个 PIM/PNM、内存、Chiplet/wafer-scale、能源与数据中心专场。这一组合说明架构优化的边际价值已明显从峰值 FLOPS 转向容量、带宽、通信、可靠性、调度和电力。

2. **AI 推理比训练更直接地推动架构分化。** MoE 专家调度、KV cache、低比特量化、CXL 容量层、SSD 活跃层、3D-DRAM/PIM、低延迟小 batch 等议题密集出现；训练侧则主要向 collective offload、内置 NIC、scale-up 网络、流水线和解耦训练迁移。训练仍需大规模通用 GPU，但推理更有条件被工作负载专用芯片切走。

3. **HBM 与 CXL 不是替代关系。** HBM 解决靠近加速器的高带宽，CXL 解决 CPU/服务器侧的低成本容量和冷页分层。Meta 的 Vistara 已在生产环境证明 CXL 的商业价值，但其 CXL 层带宽约为本地 DDR 的十分之一、负载下时延高约 60%；这恰好证明 CXL 是容量层，而不是“HBM 平替”。

4. **最接近 1—2 年商业兑现的是软件/固件和已有接口的再优化。** MoE 预取与放置、功率动态分配、冷热页迁移、CXL 直连扩容、HBM4、加速器内置 NIC/collective engine、KV cache 量化，均不要求先创造全新工艺。相反，异构 Chiplet 动态迁移、千核一致性、通用近存计算、细粒度超高 IOPS SSD 和光子矩阵计算仍需 3—5 年或更久。

5. **论文峰值增益不能直接资本化。** 本报告筛选的 12 个方向中，只有 Vistara 具有明确的 hyperscale 生产部署；Power Sloshing 有真实服务器实验；Raptor 属于早期硅；其余大量结果来自 trace-driven simulation、RTL 综合、预测工艺、QEMU/SST、MQSim 或公开成本模型。最醒目的 6.6×、4.7×、4.0× 等数字，大多不是同一代量产系统上的端到端独立测试。

6. **被低估的利润池是“让昂贵芯片被用好”的层。** 包括内存控制器/ECC、网络 collective、调度器、功率控制、3D-IC 验证、SerDes/PCIe/CXL IP、先进封装测试和冷却控制。其单位价值远小于 GPU，但能直接释放 GPU 利用率、延长服务器寿命，客户 ROI 更容易验证。

7. **被过度乐观的是光子计算、通用 PIM 和“CXL 等于共享 HBM”。** ISCA 的光子 DNN 论文反而指出，在等精度、等吞吐条件下，计入非线性、码间干扰和噪声后，部分既有光子方案至少比数字实现多耗 5× 能量。光互连仍有商业价值，但不能把光互连的确定性外推为光子 MAC 的确定性。

8. **2026 年最强现实锚点仍是加速器、网络和 HBM。** NVIDIA 截至 2026-04-26 的单季数据中心计算收入为 604 亿美元、网络收入为 148 亿美元；Broadcom FY2026 Q1 AI 收入 84 亿美元；Micron 给出的 HBM TAM 从 2025 年约 350 亿美元以约 40% CAGR 增至 2028 年约 1,000 亿美元。会议结果支持这些利润池继续扩张，但也指向单位 token 成本下降和专用化带来的长期价格压力。

9. **未来三个月是“验证会后叙事”的窗口，不是论文立刻转收入的窗口。** 应观察 HBM4 客户资格/良率、CXL 商用模块和交换芯片样品、Raptor 客户试用、800G/1.6T 端口增长、MoE 调度是否进入主流 serving stack，以及功率控制是否给出生产 SLO 数据。

10. **一年尺度上，网络与内存内容量增速大概率继续高于裸算力增速。** 推理上下文变长、MoE 扩大、agentic workload 增加 CPU 控制面和存储访问，均提高每个计算单元所需的 HBM、DDR/CXL、SSD、NIC、交换和光模块价值。

11. **两年尺度上，赢家不一定是“最激进的新器件”，而是能让新内存/互连无痛进入既有软件栈者。** Meta 强调 MTIA 使用 PyTorch、vLLM、Triton 和 OCP；Vistara 用 Linux 分层迁移；Raptor 仍需证明编译器、模型覆盖和客户迁移。软件兼容性可能比器件峰值更能决定采用率。

12. **投资上的反共识结论**：CXL 可能先增加控制器、交换、系统软件的价值，却通过复用旧 DDR4 抑制部分新 DDR5 采购；推理专用 ASIC 可能扩大总算力市场，却稀释通用 GPU 的收入份额；先进封装需求确定性高，但扩产后价格、良率和客户集中决定利润率，不能把产能等同于利润。

## 研究口径与证据等级

- **事实**：会议官方页面、论文原文/作者 camera-ready、公开代码或公司财报/产品页可直接复核的内容。
- **估算**：本报告基于一手收入锚点、单位量价和采用率建立的模型；不是公司指引，也不是第三方市场报告的照抄。
- **判断**：对产业化时间、受益方向、利润率和证伪节点的研究判断。
- **证据等级 A**：生产部署或量产出货，且有端到端数据；**B**：真实硅/真实服务器，但规模或独立性有限；**C**：RTL/综合/模拟器/trace-driven 结果；**D**：作者会后分享或公司前瞻声明，完整 proceedings 尚未公开索引。

截至检索截止日，[ISCA 官方 program](https://iscaconf.org/isca2026/program/) 和奖项已经公开，但若干作者明确表示 ACM/IEEE proceedings 的最终索引仍在更新，因此本文对尚未进入 proceedings 的论文使用作者公开 camera-ready、项目页或会后材料，并降低置信度。

## 官方议程透露的架构主线

### 奖项、Keynote 与 Workshop 的共同指向

- [ISCA 官方主页](https://iscaconf.org/isca2026/)确认会议日期、地点和会后奖项。两篇 Best Paper 是 **Patterns Behind Chaos**（大规模 MoE 推理数据移动）与 **Cerberus**（跨层 ECC），分别指向性能与可靠性两端的“内存墙”。
- 7 月 1 日 Babak Falsafi 的 keynote **Beyond the AI Energy Wall** 明确提出：AI 需求增长快于电力、冷却和数据中心容量，解决方案应跨硬件、系统、工作负载和运行约束，而不是只扩大加速器。
- Debbie Marr 的 keynote 把后摩尔时代架构与经济性并置；这与会议中的数据中心全生命周期 TCO、功率调度和冷却论文形成闭环。
- [Workshop/Tutorial program](https://iscaconf.org/isca2026/program/workshops.php)集中出现 ASTRA-sim、MLArchSys、MCCSys、DRAMSec、Ramulator/DRAM Bender、NexNPU、Beethoven、Full-Stack Carbon Accounting、XiangShan RISC-V 和 cloud-native infrastructure。Workshop 是早期路线信号，不能当作论文结论，但说明工具链、开放 NPU、内存中心化和能耗核算已成为共同基础设施。
- 产业 track 同时出现 Meta Vistara、Panmnesia CXL、Meta MTIA 300、Google Prometheus cooling、Microsoft Rowhammer 和 Meta KernelEvolve，表明 hyperscaler 正把架构研究下沉到自研 ASIC、内存控制、网络、运维和可靠性。

### 训练与推理的重心变化

| 层级 | 训练侧变化 | 推理侧变化 | 产业含义 |
|---|---|---|---|
| 计算 | 低精度、流水线、解耦训练、collective offload | MoE、KV cache、speculative decoding、低 batch/低时延专用化 | 推理更容易产生 ASIC/NPU 分流，训练仍依赖大规模通用 GPU |
| 内存 | 参数、优化器状态与 checkpoint 的容量/带宽 | 权重、KV cache、专家路由导致持续读带宽和容量压力 | HBM、DDR/CXL、SSD 形成分层而非单一替代 |
| 通信 | scale-up collective、NIC offload、拓扑感知 | expert placement、in-switch compute、请求/专家协同调度 | NIC、交换芯片、SerDes、光模块的内容量提高 |
| 系统 | 故障恢复、流水线气泡、集群调度 | SLO、突发流量、能耗、冷热页、模型迁移 | 软件可在 0—1 年兑现，硬件重构更慢 |
| 设施 | 电力、冷却和网络一次性建设限制 | 推理长周期运行使 OpEx 更敏感 | 服务器利润池从采购扩展到利用率和生命周期管理 |

**判断**：本届并非“算力不重要”，而是当算力供应急剧增长后，决定可交付 token 的约束依次外溢到 HBM、网络、电力、可靠性和调度。计算芯片仍是最大收入池，但增量价值更多被周边层捕获。

## 核心论文与架构变化

### 总览：12 个最重要论文或技术方向

| # | 论文/方向 | 核心瓶颈 | 公开峰值结果 | 证据等级 | 初步产业化窗口 |
|---:|---|---|---|---|---|
| 1 | Patterns Behind Chaos | MoE 专家数据移动与放置 | 未来 wafer-scale 模拟平均 6.6×；现有多 GPU 最多 1.25× | C/B | 软件 0—1 年；wafer-scale 3—5 年 |
| 2 | Cerberus | HBM/LPDDR ECC 冗余、误纠正与能耗 | 冗余减少 33.3%；IPC +0.7%；能耗 -1.84% | C | 局部 1—2 年；完整跨层 3—5 年 |
| 3 | Vistara | 内存容量受限与旧 DDR 复用 | 生产 workload 吞吐 +8.6% 至 +33%；部分服务器 -25% | A | 已生产，1—2 年扩散 |
| 4 | Panmnesia CXL controller/switch | CXL switch 时延与可扩展性 | 最多 64 节点保持稳定；pre-release silicon | B/D | 样品 0—1 年；规模部署 2—3 年 |
| 5 | PLENA | 长上下文推理的权重/KV/激活内存墙 | 2.23× A100、4.70× TPU v6e；能效 4.04× A100 | C | 设计思想 1—2 年；完整芯片 3—5 年 |
| 6 | Five-Minute Rule 40 Years Later | GPU 内存昂贵，flash 粒度与 IOPS 不足 | 512B 细粒度模型约 57.4M IOPS；GPU break-even 约 5 秒 | C | SSD/KV offload 1—2 年；新介质/控制器 3—5 年 |
| 7 | Raptor 3D-DRAM | HBM 带宽/功耗与 SRAM 容量矛盾 | 相对 HBM 配置吞吐 4.71×；相对 SRAM 2.44× | B/D | 试用 1—2 年；规模产品 3—5 年 |
| 8 | PhaseWeave | 异构 Chiplet 资源错配 | P99 -65%、吞吐 1.6×、perf/W 1.9× | C；软件实验 B | 软件 1—2 年；硬件 3—5 年 |
| 9 | Power Sloshing | 复合 CPU/GPU 服务器功率闲置 | perf/W 最多 1.83×；保守策略省电约 8%—11% | B | 0—1 年 |
| 10 | Datacenter Lifecycle for AI | 建设、更新、运行割裂导致 TCO 浪费 | 分阶段 15%/23%/19%；联合最多降 TCO 40% | C | 工具/策略 0—2 年 |
| 11 | Dorado | 1,000+ core cache coherence 元数据与广播 | 1.36×；load latency -46.1%；无效化消息 -39% | C | 3—5 年 |
| 12 | Shining Light on Silicon Photonic DNN Accelerators | 光子计算信号完整性与系统能耗 | 等精度/等吞吐下，部分方案至少 5× 数字实现能耗 | D | 计算路线 >5 年或被证伪；光互连 1—3 年 |

### 1. Patterns Behind Chaos：MoE 的瓶颈是“专家去哪儿”，不是只有乘法

**问题。** 超大 MoE 每个 token 只激活部分专家，但专家分布、跨 GPU 搬运和 all-to-all 通信可能占据主要时间；如果按“随机专家选择”设计系统，会错失可预测的局部性。

**方法与事实。** [论文当前版本](https://arxiv.org/abs/2510.05497)分析 4 个 2025 年公开的大型 MoE 模型、约 2,000 亿至 1 万亿参数、超过 24,000 个请求，并公开约 199GB 的[专家选择 traces](https://huggingface.co/datasets/core12345/MoE_expert_selection_trace)。作者发现相邻层、相邻 token、共同激活专家及 prefill/decode 之间存在可利用模式，据此提出预测、缓存、专家复制、层级感知放置和请求调度。

**关键指标。** 当前摘要报告：在设想的 wafer-scale GPU 上，所提修改平均提升 6.6×；在现有多 GPU 上，prefill-aware expert placement 对 MoE 计算最多提升 1.25×。

**实验边界。** 6.6× 是 trace-driven 的未来 wafer-scale 架构模拟，不是量产 GPU；1.25× 更接近当前硬件，但只覆盖 MoE 核心阶段，未必等同端到端请求吞吐。公开数据提升可复核性，但请求构成、输出长度、模型版本和路由器训练都会改变局部性。

**产业化障碍与判断。** 软件放置、预取和复制可在 0—1 年进入 serving runtime；需要全局/局部 command processor 的 wafer-scale 方案需 3—5 年。最直接映射到 NVIDIA/AMD/自研 ASIC 的运行时与网络，也会降低“只靠多买 GPU”解决 MoE 的必要性。

### 2. Cerberus：可靠性开始反向决定 HBM 的有效容量和能效

**问题。** HBM/LPDDR 的 on-die、link 和 system ECC 各自增加冗余、读写和延迟；若分层编码彼此不知情，还可能放大误纠正。

**方法与事实。** [Cerberus](https://arxiv.org/abs/2605.02220)把 on-die ECC、link ECC 与 system ECC 做跨层协同，采用 Encode-Once Decode-Many、冗余复用和对错误模式的分层处理。论文面向 32B 访问粒度和 8—32 bit 聚簇故障，而不是只处理理想独立单 bit 错误。

**关键指标。** 相对论文建模的 HBM4 基线，32-bit 方案把存储冗余降低 33.3%，几何平均 IPC 提升约 0.7%，能耗降低约 1.84%；40-bit 方案 IPC 约 +0.5%、能耗约 +0.86%，体现可靠性强度与成本的交换。

**实验边界。** 性能使用 V100-like、80 SM、32 HBM channel 的 Accel-Sim，并替换为假设 HBM4 时序；16 个 workload 来自 Rodinia、Parboil、GraphBIG 和 PolyBench，不是大模型训练集群；逻辑以 UMC 28nm 综合，可靠性依赖故障模型，没有量产 HBM4 的 field FIT 数据。

**产业化障碍与判断。** 局部 decoder/控制器优化可能 1—2 年进入产品；完整跨层设计需 DRAM 厂、GPU/CPU 控制器、封装链路与 JEDEC 接口共同暴露信息，周期更可能为 3—5 年。受益者不是单一存储芯片，而是内存厂、控制器/IP、验证与测试。

### 3. Vistara：CXL 第一次以生产数据证明“冷容量层”成立

**问题。** Meta 发现 43.7% 的通用服务器 fleet 受内存容量约束，但新 CPU 平台本地 DDR5 昂贵，退役服务器中的 DDR4 又成为沉没资产。

**方法与事实。** [Vistara camera-ready](https://jovans2.github.io/files/vistara_camera_ready.pdf)覆盖自研 CXL 2.0 Type-3 ASIC、板卡、可靠性和 Linux TPP 页迁移到 hyperscale 部署的完整路径。生产板每个 ASIC 接两条 DDR4 72-bit channel，当前配 128GB；双 ASIC 板提供 256GB CXL DDR4。ASIC 约 9W，idle path 约 50ns，并内置 RS ECC、x4 chipkill 和 3 个管理 RISC-V core。

**关键指标。** 本地 768GB DDR5 的实测读带宽约 497GB/s，CXL 层约 48GB/s；60% 负载时延约 234ns 对 372ns。尽管如此，生产 workload 获得：CacheA 吞吐 +25%、Spark executors/server +25%、CI jobs/server +33%、FtStorex +8.6%；部分大型参数服务可减少约 25% 服务器并提高约 12% 吞吐。TPP overhead 低于 0.5%。

**实验边界。** 单一 hyperscaler、自研 ASIC、冷热页明显的 workload；不是 GPU HBM pooling。默认约 3:1 本地:CXL 较稳健，激进到 1:1 且 35%—40% working set 落在 CXL 时会回归。论文未披露 merchant ASP 和完整 ROI。

**产业化障碍与判断。** 这已经是生产证据，但商业复制仍需 CPU/CXL 兼容、OS tiering、RAS、验证和客户 workload profiling。CXL 近期最确定的场景是容量扩展、旧内存复用和冷页，不是低延迟共享显存。

### 4. Panmnesia：CXL 从直连扩容走向可交换 fabric，但证据仍偏厂商侧

**问题。** 早期 CXL switch 沿用 PCIe 分层缓冲和树状路由，增加同步时延，也限制共享内存拓扑。

**方法与事实。** Panmnesia 的[会前/会后公司材料](https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/)称其重构跨层 buffer，并在兼容 hierarchy-based routing 的同时加入 port-based routing，使设备可组成更灵活 fabric。论文属于 ISCA industry track，硬件为 silicon-proven controller/switch。

**关键指标。** 公司披露评估扩展至 64 节点仍保持稳定，PCIe 6.4/CXL 3.2 Fusion Switch 已有 pre-release chip，PCIe 7.0/CXL 4.0 Combo IP 可供合作方接洽。

**实验边界。** 截止检索日，完整 proceedings/独立测试尚未公开索引；“相似时延”“稳定性能”缺少同页可复核绝对数值和 merchant 客户部署。证据等级 B/D，不能与 Vistara 的生产 workload 数据等量齐观。

**产业化障碍与判断。** 0—1 年可见样片和 pilot，2—3 年才可能出现规模 fabric。关键节点是主流 CPU root complex、CXL memory module、Linux/virtualization、交换管理和客户 RAS 的共同认证。

### 5. PLENA：长上下文推理要求计算阵列、量化和 FlashAttention 一体设计

**问题。** Agentic inference 的 decode 长度可比传统请求高两个数量级，权重、KV cache 和激活形成不同数据类型、访问形态和精度要求；单一 systolic array 难以同时高效处理“胖 GEMM”和 attention。

**方法与事实。** [PLENA](https://arxiv.org/abs/2509.09505)采用 flattened systolic array、权重/激活/KV 非对称量化、原生 FlashAttention、定制 ISA 与编译器，并用 cycle simulator、Ramulator、RTL 和设计空间搜索共同评估。

**关键指标。** 当前论文摘要在相同乘法器数量和内存配置下报告：相对 A100 2.23×、相对 TPU v6e 4.70×，相对 A100 能效 4.04×。

**实验边界。** 完整系统没有 tapeout；RTL 以预测 7nm OpenROAD PDK、Synopsys、1GHz 综合；竞争基线部分为作者重实现/归一化配置，而非等价格、等机柜、等软件成熟度。量化质量主要看 WikiText-2 perplexity 和有限模型集，不能替代客户任务质量、尾时延和完整 TCO。

**产业化障碍与判断。** KV cache 低比特、attention/dataflow 融合和形状感知阵列可在 1—2 年被现有 NPU/ASIC 吸收；PLENA 原样成为商业芯片需 3—5 年，并依赖编译器、模型算子覆盖和量化精度迁移。

### 6. Five-Minute Rule 40 Years Later：flash 从“存储”尝试变成 GPU 的活跃容量层

**问题。** 传统 five-minute rule 决定数据应留在 DRAM 还是磁盘/SSD；在高价 GPU+HBM 与超高 IOPS flash 组合下，break-even 时间大幅缩短，KV cache、embedding 和 ANN 可被更积极下沉。

**方法与事实。** [论文](https://arxiv.org/abs/2511.03944)建立包含 host、DRAM、NAND、SSD、访问粒度、IOPS、尾时延和成本的模型，并设想 512B 细粒度读取、每 sector BCH 加 4KB 外层 LDPC 的 Storage-Next SSD，避免 4KB read amplification。

**关键指标。** 建模 SSD 在 512B 随机读约 57.4M IOPS；MQSim-Next 在只读/90:10/70:30/50:50 读写比下约 82M/68M/52M/34M IOPS。CPU+DDR 的 break-even 随粒度约 34 秒至 10 秒，GPU+GDDR 在 512B 约 5 秒。

**实验边界。** Storage-Next 不是量产产品；使用 Gen7×8 PCIe、2025 成熟 NAND 成本和模拟器，应用案例主要为 SSD-resident KV 与 HNSW 的分析/合成负载。host IOPS、软件栈、写放大、耐久性、能耗和真实 p99 都可能把收益压低。

**产业化障碍与判断。** 现有 GPU direct storage/KV offload 可能 1—2 年扩张；细粒度 ECC、极高 IOPS 控制器和新接口需 3—5 年。机会更偏企业 SSD controller、firmware、数据路径和 context store，而非“SSD 全面替代 DRAM”。

### 7. Raptor：logic-on-3D-DRAM 是最接近产品的近存推理路线之一

**问题。** SRAM 推理加速器带宽高但容量小，HBM 容量较大却受外部总线功耗和带宽约束；直接把 DRAM 叠在逻辑上又引入微凸点接口、热、刷新、ECC、冗余和高 bank 数问题。

**方法与事实。** 作者[公开论文页](https://prashantnair.bitbucket.io/publications/)称 Raptor 是面向生成式推理的早期 3D-DRAM silicon，提出 stream-blocking KV 映射、单周期 micro-bump 接口上的 pinless DBI、保持拓扑的冗余、thermal-aware refresh 和 interleaved ECC。d-Matrix 的[公司材料](https://www.d-matrix.ai/going-vertical-why-we-created-a-3d-dram-solution-to-advance-low-latency-ai-inference/)说明 Pavehawk 是验证 3DIMC 的 test chip，Raptor 为后续商业平台。

**关键指标。** 在 Llama 3.1 70B、DeepSeek-V3、Kimi K2、GPT-OSS、Whisper 和 Canary 上，作者报告相对 HBM 配置吞吐 4.71×、相对 SRAM 配置 2.44×，同时降低对网络时延和带宽的敏感度。

**实验边界。** “early silicon”不等于大规模量产；比较配置、软件栈、功耗边界、batch/SLO、良率和完整成本尚缺独立复测。公司另称 3DIMC 相对 HBM4 的目标可达 10×，这是产品目标，不应与论文的 4.71×混用。

**产业化障碍与判断。** 1—2 年可看 pilot/早期客户，3—5 年才适合判断规模化。证伪节点包括：Raptor 是否按期提供客户可复测硬件、热/刷新是否在持续负载稳定、3D bonding 良率和成本是否可接受、编译器能否覆盖主流模型。

### 8. PhaseWeave：Chiplet 的下一阶段不是“拼起来”，而是按 phase 动态选芯粒

**问题。** 数据中心 workload 在 compute、memory、network 和 low-power phase 间切换，固定映射到同质 core 会造成 P99、功耗和面积浪费。

**方法与事实。** Microsoft Research 的[PhaseWeave](https://www.microsoft.com/en-us/research/publication/phaseweave-phase-aware-execution-on-heterogeneous-chiplet-architectures-for-datacenters/)设计高计算、快内存、近网络、低功耗四类 chiplet，并用 15 棵、深度 5 的随机森林按 100μs counter/syscall window 预测 phase，再迁移执行。

**关键指标。** 预测器短 phase 准确率 93%，未见过的 DeathStarBench workload 为 91%；iso-area 模拟中 P99 降 65%、吞吐 1.6×、perf/W 1.9×。预测器估算仅约 0.02% core area、低于 100 cycles。真实 Emerald Rapids 服务器用软件/频率配置模拟异构池，得到相同吞吐下功耗降低 7.2%，平均迁移约 23.8μs、中位 9.5μs。

**实验边界。** 1.6×/1.9×来自 QEMU+SST 的异构多 chiplet 模拟，不是实体多 chiplet CPU；真实实验只是现有服务器上的软件代理，且软件 predictor 会带来明显吞吐 overhead。

**产业化障碍与判断。** 软件 phase-aware scheduling 可在 1—2 年落地；完整异构 chiplet 需 ISA/OS 状态迁移、cache coherence、封装/供电、验证与调度共同设计，周期 3—5 年。最直接受益是 chiplet interconnect、3D-IC/thermal EDA、coherence IP，而不是所有 CPU 厂商自动受益。

### 9. Power Sloshing：一行新 silicon 都不用，也能释放 AI 服务器电力

**问题。** CPU+多 GPU 的 compound server 往往有固定节点功率上限，但 workload phase 使部分 GPU/CPU 闲置，静态 cap 无法把空闲功率给到真正受限的器件。

**方法与事实。** [论文 camera-ready](https://jovans2.github.io/files/power_sloshing_isca_camera_ready.pdf)观察到超过 60% 的服务器在部分 GPU 上存在 20%—40% 未使用 TDP；作者在 Grace Hopper H100+Grace CPU 上用简单利用率 controller 动态转移功率预算。

**关键指标。** 在受功率限制的实验中 perf/W 最多 1.83×。对一个 1 小时 workload，保守 SLO-aware 策略省电 11%，p99 违规 interval 从 4% 增至 5%；激进策略省电 24%，但违规升至 14%。其他 workload 保守节省约 8%，激进约 19%。

**实验边界。** 模型 A/B/C/D 匿名、服务器规模有限，“最多 1.83×”不是 fleet 平均；突发流量会让反应式 controller 失效。论文未证明全 fleet 生产部署。

**产业化障碍与判断。** 这是 0—1 年最可兑现方向，但商业价值取决于 SLO。投资模型应以 5%—10% 稳健节电为基准，而非 24% 峰值；若生产 p99 违规增加超过 1 个百分点，客户可能放弃激进策略。

### 10. Rearchitecting the Datacenter Lifecycle for AI：从芯片性能转向 15—30 年设施约束

**问题。** 数据中心建筑寿命可达 15—30 年，IT 设备约 4—6 年更新；电力、冷却、网络在建设时确定，却要承受快速变化的 GPU 功耗、成本和模型。

**方法与事实。** Microsoft/UT Austin 的[论文与开源框架](https://www.microsoft.com/en-us/research/publication/rearchitecting-datacenter-lifecycle-for-ai-a-tco-driven-framework/)把 build、IT provisioning/refresh 和 operation 联合优化，使用开源 LLM、公开硬件规格与成本，比较电力拓扑、冷却、网络、设备更新、模型迁移、推理解耦和调度。

**关键指标。** 单独优化 build、provisioning、operation 分别最多降低 TCO 15%、23%、19%；跨阶段联合最多 40%。

**实验边界。** 结果是长期成本模型，不是 Microsoft 生产 fleet 实际节省；GPU 价格、利用率、折旧、能源和当地建设成本的微小变化会改变最优点。“最多 40%”不能按年直接映射收入或利润。

**产业化障碍与判断。** TCO 工具、功率共享和 refresh 决策可在 0—2 年采用；建筑/供电重构需要多年。对服务器/冷却/电力链的含义是：客户会更加比较全生命周期，而不是接受所有“AI 数据中心”溢价。

### 11. Dorado：千核 CPU 的 coherence 仍是 AI 控制面和数据处理的隐藏瓶颈

**问题。** 当 CPU 扩至 1,000+ core，完整 bit-vector directory 面积大，limited pointer 又会触发广播和无效化风暴；AI agent control plane、数据预处理、storage/network stack 仍依赖 CPU。

**方法与事实。** [Dorado camera-ready](https://jovans2.github.io/files/dorado_isca_camera_ready.pdf)使用两级 home、临时 directory slice、动态共享存储和 SetOverflow，在 32-core cluster 组成的 1,024-core 模型中减少目录压力。

**关键指标。** 相对同面积 limited-pointer 方案，平均性能 1.36×、load latency 降 46.1%、invalidation message 降 39%；性能距完整 bit-vector 不到 1%，directory storage 少 2.75×。

**实验边界。** 结果来自 1,024-core 仿真，无实体 CPU；workload 包括图、Redis、FaaS、ML serving 等，但规模、内存系统和网络假设会显著影响 coherence。

**产业化障碍与判断。** 3—5 年方向。受益逻辑是大核数 CPU、RISC-V/Arm server、coherence fabric 和 chiplet IP；但如果 agentic workload 更多把控制下沉 DPU/加速器，CPU core 数本身未必线性增长。

### 12. Shining Light：光子“互连可行”不等于光子“计算必胜”

**问题。** 既有 photonic DNN accelerator 常用理想器件或忽略信号完整性，把调制器/波导的 MAC 能耗优势直接外推到系统。

**方法与事实。** 截止检索日，完整 proceedings 尚待索引；作者的[会后公开说明](https://www.linkedin.com/posts/avilash-mukherjee_shining-light-isca-2026-presentation-activity-7478469082007240704-EPsy)称论文显式加入非线性、inter-symbol interference 和噪声，并要求与数字实现等精度、等吞吐比较。

**关键指标。** 作者报告：在这些约束下，所评估的既有 silicon-photonic accelerator 至少消耗数字实现 5× 能量。

**实验边界。** 当前可复核材料是作者会后摘要，缺少完整配置、器件工艺、laser/ADC/DAC 分摊和敏感性表，证据等级 D、置信度中等。结论不能泛化到所有未来光子方案，也不否定 optical I/O/CPO。

**产业化障碍与判断。** 未来 1—3 年，光的确定性机会仍在 800G/1.6T、NPO/CPO、scale-up/scale-out interconnect；光子 MAC 若不能公开展示等精度、wall-plug energy 和可制造性，仍应按 >5 年高风险 optionality 估值。

## 不同器件和系统路线的产业化含义

| 路线 | ISCA 2026 信号 | 1—2 年可见变化 | 3—5 年可能变化 | 主要障碍 |
|---|---|---|---|---|
| GPU | MoE placement、KV/量化、collective、fault tolerance | HBM4、更强 NIC/collective、调度/功率软件 | wafer-scale/更深异构 memory | 电力、HBM、网络、软件兼容、利用率 |
| CPU | Dorado、ATX、CXL、agent control plane | 更多内存容量、CXL tier、DPU/near-core offload | 千核 coherence、异构 chiplet | 单线程/尾时延、coherence、软件迁移 |
| 专用加速器 | PLENA、Raptor、PIM、MTIA 300 | 推理 ASIC 增长、内置 NIC、低精度/KV 专用化 | 3D-DRAM/IMC、更多模型专用 dataflow | 模型变化、编译器、客户迁移、规模经济 |
| Chiplet/3D | PhaseWeave、Raptor、wafer-scale、packaging simulator | 2.5D chiplet 与 advanced packaging 继续普及 | 动态异构 chiplet、logic-on-DRAM | bonding 良率、热、测试、供电、coherence |
| HBM | Cerberus、HBM-CASO、3D/PIM | HBM4 量产，容量/带宽和 RAS 提升 | HBM4E、更多 logic base die 功能 | 良率、TSV/封装、功耗、客户集中 |
| CXL | Vistara、Panmnesia | 冷页/容量扩展、旧 DDR 复用、直连模块 | CXL 3.x fabric/pooling | 时延、OS tiering、RAS、交换管理 |
| PIM/PNM | 多个专场、AXLE、DCC、3D Hybrid PIM | 特定 kernel/内存厂 pilot | 领域专用 PIM 商业化 | 通用编程、数据一致性、热、良率、模型变化 |
| 光/电互连 | 光子计算负面结果；800G/1.6T 产业需求 | 电 SerDes+可插拔光仍是主流；NPO/CPO pilot | CPO/optical scale-up 增加 | laser/封装/维修、标准、成本、可靠性 |
| scale-up 网络 | MoE in-switch、MTIA 300 collective、RoCC | NIC/collective offload 和拓扑感知增强 | 更开放 scale-up fabric | 标准竞争、软件栈、拥塞、故障域 |
| 数据中心效率 | Power Sloshing、Lifecycle、Prometheus、keynote | 功率控制、SLO 调度、液冷/气候模型 | 建筑/供电/冷却联合设计 | 客户现场差异、尾时延、资本周期 |

### 一个重要分界：带宽层、容量层和持久层

```text
计算单元/寄存器/SRAM
        ↓ 最高带宽、最低容量
HBM / 3D-DRAM / 专用 PIM
        ↓ 高带宽、昂贵、靠近加速器
本地 DDR / SOCAMM
        ↓ CPU/主机容量层
CXL-attached DDR
        ↓ 冷页、共享/扩容、较高时延
高 IOPS SSD / context store
        ↓ 持久、便宜、软件管理更重
对象存储/远端存储
```

**判断**：未来产品不会由单一新内存“替代全部旧内存”，而会增加层级。对投资而言，这使 controller、tiering software、RAS、互连和 observability 的价值上升，也增加系统集成风险。

## 产业化时间表

### 已落地或 0—2 年

- **已生产/量产证据**：Meta Vistara；Meta 表示 MTIA 300 已用于 ranking/recommendation training 并进入生产；Micron 表示 HBM4 已高量出货给 lead customer；Samsung CXL 2.0 256GB CMM-D 已标注 mass production。
- **软件/固件优先**：MoE expert placement/replication、KV cache 量化、功率 sloshing、Linux/CXL tiering、模型调度、collective offload。
- **产业判断**：对 2026—2027 收入最相关的是 HBM4、AI networking、800G/1.6T optics、CXL module/controller、先进封装和 EDA/IP，而不是全新物理计算范式。

### 3—5 年

- Raptor/logic-on-3D-DRAM 的规模产品、完整跨层 Cerberus、CXL 3.x fabric、多 chiplet phase migration、千核 coherence、Storage-Next 级细粒度 SSD、部分 PIM/PNM。
- 关键 gate：量产良率、热与 ECC、主流软件适配、客户 workload 迁移、互操作认证、单位 token TCO。

### 5 年以上或高不确定性

- 通用 photonic MAC、把 CXL 当低延迟共享 HBM、通用可编程 PIM、无软件代价的 wafer-scale fault tolerance。
- 这些路线不能因单篇论文高倍数而给予与 HBM/网络同样确定性的估值。

## Benchmark 审计：学术增益如何折算为商业价值

### 逐项风险

| 方向 | 主要 benchmark 风险 | 可接受的商业验证 |
|---|---|---|
| Patterns Behind Chaos | 最大增益来自未来 wafer-scale 模拟；trace 的请求/输出分布可能偏 | 主流 serving stack 在真实流量中端到端吞吐、p99、网络字节和 GPU 数 |
| Cerberus | V100-like+假设 HBM4；28nm 综合；故障模型非 field data | HBM4/LPDDR 样片 FIT、误纠正、面积/功耗、JEDEC 互操作 |
| Vistara | 单一 hyperscaler、冷热页 workload、自研 ASIC | 第二家客户/merchant platform，更多 workload 和完整 TCO；现有证据已较强 |
| Panmnesia | 公司自报、绝对时延和客户数据不完整 | CPU+module+switch 的第三方互操作、64 节点尾时延和真实应用 |
| PLENA | 预测 7nm、归一化基线、无 tapeout；perplexity 不等于任务质量 | 实体芯片在 vLLM/主流模型上的 token/s、TTFT/TPOT、质量和系统功耗 |
| Five-Minute Rule | 假设不存在的 512B/57M IOPS SSD；合成 trace | 量产 SSD 的 512B/1KB p99、写放大、耐久和 GPU host IOPS |
| Raptor | 早期硅、厂商配置、无独立客户复测 | 客户可获得卡/系统、同模型同 SLO 同功耗/成本 benchmark |
| PhaseWeave | 核心高倍数来自模拟；真实硬件只模拟异构池 | 实体 heterogeneous chiplet、迁移一致性、OS overhead、生产 p99 |
| Power Sloshing | 匿名 workload、小规模、峰值口径 | fleet 平均节电、SLO 违规、突发恢复、不同 CPU/GPU 组合 |
| Lifecycle | 长期成本模型，假设敏感 | 实际项目 IRR、建设/刷新前后 TCO，按地区和利用率复核 |
| Dorado | 1,024-core 模拟、无 silicon | 实体 many-core CPU 上 directory 面积、功耗、p99 和软件扩展 |
| Photonic DNN | 当前仅作者摘要；器件/ADC/DAC/laser 假设未公开 | 完整论文、等精度/等吞吐、wall-plug energy、工艺良率 |

### 折算公式

学术峰值增益应至少经过以下折扣：

> **可商业兑现增益 ≈ 论文增益 × 可覆盖 workload 比例 × 真实硬件实现系数 × 软件/迁移系数 × 集群利用率系数 × 价格捕获系数**

例如，6.6× 的模拟峰值若只覆盖 MoE 阶段、需要未来硬件、客户还要承担迁移，商业价值可能只表现为 10%—30% 的整机吞吐或较少 GPU 数；反之，Power Sloshing 的“仅”8%—11% 稳健节电，因为无需新 silicon、可覆盖大量已装机服务器，可能比更高的模拟 speedup 更快产生现金回报。

### 五类常见误读

1. **小模型/短输出**：对 KV cache、MoE 和长上下文不具代表性。
2. **模拟器/理想工艺**：预测 7nm、未来 Gen7 PCIe、wafer-scale topology 不等于可制造产品。
3. **不可比基线**：相同 MAC/内存配置不等于相同价格、机柜功率、软件或供货能力。
4. **只看平均吞吐**：推理商业价值往往由 TTFT、TPOT、p99、SLO 违规和质量决定。
5. **忽略迁移成本**：编译器、kernel、模型版本、算子覆盖、调试和客户验证可能抵消硬件优势。

## 对未来 3 个月、1 年和 2 年的产业判断

| 产业环节 | 未来 3 个月（至 2026-10） | 未来 1 年（至 2027-07） | 未来 2 年（至 2028-07） | 最重要跟踪指标 |
|---|---|---|---|---|
| AI 加速器 | 会议论文不会立刻改变采购；观察 Rubin/MI450/MTIA 等供货、MoE 软件进入生产 | 推理专用/自研 ASIC 份额上升，GPU 仍占最大收入；内置 NIC/collective 更普遍 | 通用 GPU 与 workload-specific ASIC 分层，单位 token 价格下降 | accelerator 出货、ASP、推理占比、token/$、客户自研份额 |
| CPU | agent control plane、CXL host、数据/存储前处理提高 CPU 价值 | Arm/RISC-V/定制 server CPU 与高容量 DDR/CXL 结合 | many-core/chiplet/coherence 技术进入新平台 | server unit、每节点 core/DDR、CXL lane、DPU offload 比例 |
| HBM/DRAM | HBM4 出货与资格认证、供给紧张和长期合约继续主导 | HBM4/4E 占比上升；每 accelerator stack/容量增加 | logic base die、更多 RAS/近存功能；供给扩张带来价格波动 | HBM bit shipment、stack ASP、良率、封装产能、客户集中 |
| CXL | Vistara 和 Samsung/Panmnesia 提供可验证样本；仍以 pilot/内部部署为主 | 直连 CMM-D、冷热页和旧内存复用扩散，merchant revenue 开始可见 | CXL 3.x switch/fabric 进入部分规模场景 | 合格 CPU/OS、模块出货、eligible server penetration、p99、带宽利用 |
| SSD/context storage | 现有高容量/Gen6 SSD 受益于 context store，论文型 512B SSD 尚远 | KV/embedding/ANN offload 增长，GPU direct data path 改善 | 细粒度超高 IOPS controller 可能出现样品 | 512B/4KB IOPS、p99、DWPD、GPU direct adoption、SSD/模型容量 |
| 互连/网络 | NVIDIA/Broadcom/Marvell 高增长是一手现实锚点 | 800G 普及、1.6T 放量、scale-up Ethernet/专用 fabric 并存 | NPO/CPO 增加；开放 scale-up 标准与 proprietary fabric 竞争 | 800G/1.6T port、switch radix、SerDes、optical ASP、attach rate |
| EDA/IP | 3D-IC、HBM、PCIe/CXL/SerDes、thermal/signoff 需求立刻存在 | AI 辅助设计提高效率，但复杂度/设计数量仍推高工具与 IP 使用 | multi-die system verification 和先进封装数字孪生成为标准流程 | backlog/ACV、core EDA/IP 增速、HBM/SerDes IP license、设计重用率 |
| 先进封装/测试 | CoWoS/SoIC 类产能、HBM packaging、burn-in/test 仍是瓶颈 | 扩产释放出货，良率/交期决定利润率而非名义产能 | 3D bonding、logic-on-memory、更多 chiplet test 拉高复杂度 | package wafer、yield、cycle time、substrate/thermal/test attach |
| 服务器/冷却 | 功率管理、液冷和现场调优比新 architecture 更快兑现 | AI server unit 高增，但 ODM 毛利仍低；客户更看整机 TCO | 电力/冷却/网络与 refresh 联合规划，项目分化加大 | server equivalent、液冷渗透、rack kW、PUE、SLO、ODM gross margin |

### 时间维度的核心判断

- **3 个月**：把 ISCA 当“验证清单”，不要当交易催化剂。最可量化的会后节点是 HBM4、CXL 样品/客户、Raptor 可获得性、800G/1.6T、生产调度和功率节省。
- **1 年**：内存、网络、先进封装和 EDA/IP 的内容量继续提高；但 GPU 软件优化和自研 ASIC 会同时降低每项任务需要的通用 GPU 数，市场收入取决于需求增速能否高于效率增速。
- **2 年**：如果 agentic workload 的上下文和工具调用继续扩张，CPU/control plane、context SSD、CXL/DDR 与网络的增量可能高于纯训练算力；如果模型转向更小、更稠密或更高效，MoE/wafer-scale/PIM 的部分叙事会被削弱。

## 市场规模与利润池：2026E 基准和 2027 三情景

### 一手现实锚点

以下数据用于约束模型，不直接等于市场总额：

- [NVIDIA FY2027 Q1](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx)（截至 2026-04-26）：数据中心计算收入 604 亿美元、网络 148 亿美元，合计 752 亿美元；公司单季 GAAP/Non-GAAP gross margin 约 75%。这给 AI 计算和网络池提供了最低量级锚点，但不能把公司整体毛利直接套给所有供应商。
- [Broadcom FY2026 Q1](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial)（截至 2026-02-01）：AI 收入 84 亿美元，同比增长 106%，FYQ2 指引 107 亿美元；收入混合 custom accelerator 与 AI networking。
- [AMD 2026 Q1](https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results)：Data Center 收入 57.75 亿美元，同比增长 57%，同时包含 EPYC CPU 和 Instinct GPU，不能全部计为 accelerator。
- [Micron 2025-12 投资者材料](https://investors.micron.com/static-files/530bd7ed-a8c8-4687-af4a-8c129f740e09)：HBM TAM 约从 2025 年 350 亿美元以约 40% CAGR 增至 2028 年约 1,000 亿美元。[2026-06-24 prepared remarks](https://investors.micron.com/static-files/631b1a32-5537-46ae-8f40-82e42fc79dfe)称 HBM4 12-high 已出货超过 10 亿美元、DRAM/NAND 紧张可能延续到 2027 年后。
- [Marvell FY2027 Q1](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-26-000014/q127_8kx522026ex-991.htm)：收入 24.18 亿美元，同比增长 28%；公司明确列出 800G/1.6T optics、51.2T Ethernet switch、NPO/CPO scale-up、datacenter interconnect 与 custom XPU/XPU attach 为增长来源。
- [TSMC 2026 Q1](https://investor.tsmc.com/english/quarterly-results/2026/q1)：收入 359 亿美元，HPC 占 61%，先进制程（7nm 及以下）占 wafer revenue 74%；但公司没有单列 AI advanced packaging 收入，因此本报告封装池置信度低于 HBM/网络。
- [Cadence 2026 Q1](https://investor.cadence.com/news/news-details/2026/Cadence-Reports-First-Quarter-2026-Financial-Results/default.aspx)：core EDA 同比 +18%，IP +22%，IP 增长由 HBM、LPDDR、PCIe、SerDes 和 foundation IP 等推动。
- [Synopsys FY2026 Q2](https://news.synopsys.com/2026-05-27-Synopsys-Posts-Financial-Results-for-Second-Quarter-Fiscal-Year-2026)：季度收入 22.76 亿美元，FY2026 收入指引中值 96.65 亿美元，但其中含 Ansys，不能视为纯 EDA/IP。
- [Arm FY2026 Q4 transcript](https://investors.arm.com/static-files/78526857-5997-46eb-9b65-0d3249d83711)：FY2026 收入 49 亿美元，data-center royalty revenue 继续同比翻倍以上；DPU/SmartNIC 亦带来 royalty。

### 模型口径

1. 金额均为全球供应商收入池、美元，2026E 为报告估算；不是股票目标价或公司指引。
2. “单位”是为了强制量价闭环的**等效单位**，例如 AI accelerator package/module equivalent、high-speed port equivalent、12-high HBM stack equivalent；不同产品配置差异很大，单位量不是第三方出货统计。
3. 组件池彼此可能在公司披露中交叉，本报告做了归类，但仍不能机械相加；“AI server system”更是整机交叉校验，明确排除在组件合计之外。
4. 毛利率是相应供应商群的模型区间/中值，不代表任一公司；HBM/封装/光模块和 ODM 的周期性尤其强。
5. 采用率定义因产品而异，已在表中注明。情景的关键不是精确小数，而是数量、ASP、渗透和毛利是否自洽。

### 2026E 当前市场基准

| 收入池 | 2026E 金额（十亿美元） | 等效出货量 | 等效 ASP | 采用率假设 | 供应商毛利率假设 | 置信度 |
|---|---:|---:|---:|---|---:|---|
| AI accelerator compute package/module | 360.0 | 900 万 | 4.00 万美元 | 自研/专用推理 accelerator 占收入约 24% | 58% | 中 |
| HBM | 48.8 | 6,500 万个 12-high stack eq. | 750 美元 | HBM4 占 HBM 收入约 30% | 50% | 中高；受 Micron TAM 约束 |
| AI networking silicon（NIC/DPU/switch/retimer，排除光模块） | 84.8 | 1,600 万个高速端口 eq. | 5,300 美元 | 800G+ 端口占约 45% | 60% | 中 |
| 800G/1.6T optical module | 16.2 | 1,800 万只 eq. | 900 美元 | 1.6T 占单位量约 15% | 30% | 中低 |
| AI 相关 advanced packaging service | 25.0 | 210 万片 12-inch package-wafer eq. | 1.19 万美元 | 高端 accelerator 采用 2.5D/3D/chiplet 约 85% | 38% | 低；缺少单列收入 |
| CXL module/controller/switch | 1.5 | 75 万个 256GB module eq. | 2,000 美元 | eligible general server 渗透约 1.5% | 42% | 低 |
| AI/chiplet 相关 EDA 与 interface IP 子市场 | 9.0 | 1,800 个先进设计项目 eq. | 500 万美元 | leading-edge AI design 使用 multi-die/3D-IC flow 约 65% | 80% | 中低；项目等效口径 |
| AI server/rack node system **交叉校验，不可与上项相加** | 525.0 | 35 万个 system eq. | 150 万美元 | 液冷/高密度冷却渗透约 45% | 12% | 低 |

**基准解读。** 计算芯片仍是最大高毛利池；网络与 HBM 已各自形成数百亿美元级池；CXL 当前规模小但增速弹性大；先进封装需求确定、收入/毛利透明度却低；服务器整机金额最大但 component pass-through 高、ODM 毛利最低。

### 2027 三情景：金额、增速、量、价、采用率和毛利

| 收入池 | 下行情景 | 基准情景 | 上行情景 |
|---|---|---|---|
| AI accelerator compute | **342B（-5%）**；950 万×36k；专用/自研 27%；GM 54% | **480B（+33%）**；1,200 万×40k；专用/自研 32%；GM 58% | **645B（+79%）**；1,500 万×43k；专用/自研 38%；GM 62% |
| HBM | **51.8B（+6%）**；7,200 万×720；HBM4/4E 45%；GM 45% | **69.8B（+43%）**；9,000 万×775；HBM4/4E 55%；GM 53% | **90.2B（+85%）**；1.10 亿×820；HBM4/4E 65%；GM 60% |
| AI networking silicon | **90B（+6%）**；1,800 万 port×5.0k；800G+ 55%；GM 55% | **121B（+43%）**；2,200 万×5.5k；800G+ 65%；GM 60% | **162B（+91%）**；2,700 万×6.0k；800G+ 75%；GM 64% |
| 800G/1.6T optical | **16.0B（-1%）**；2,100 万×760；1.6T 25%；GM 24% | **23.0B（+42%）**；2,700 万×850；1.6T 35%；GM 30% | **32.3B（+99%）**；3,400 万×950；1.6T 45%；GM 36% |
| AI advanced packaging | **27.6B（+10%）**；240 万 wafer eq.×11.5k；2.5D/3D 88%；GM 32% | **36B（+44%）**；300 万×12k；渗透 92%；GM 38% | **45B（+80%）**；360 万×12.5k；渗透 95%；GM 44% |
| CXL module/controller/switch | **1.8B（+20%）**；100 万×1.8k；eligible server 2%；GM 35% | **3.6B（+140%）**；180 万×2.0k；渗透 4%；GM 43% | **6.6B（+340%）**；300 万×2.2k；渗透 7%；GM 50% |
| AI/chiplet EDA + interface IP | **9.7B（+8%）**；1,900 design eq.×5.1M；3D-IC flow 70%；GM 78% | **11.6B（+29%）**；2,150×5.4M；渗透 78%；GM 80% | **13.9B（+55%）**；2,400×5.8M；渗透 85%；GM 82% |
| AI server system，**不可与组件相加** | **499.5B（-5%）**；37 万×1.35M；液冷 50%；GM 9% | **744B（+42%）**；48 万×1.55M；液冷 60%；GM 12% | **1,020B（+94%）**；60 万×1.70M；液冷 70%；GM 15% |

### 情景驱动因素

**下行情景**：hyperscaler CapEx 增速降、模型效率提高快于请求增长、accelerator ASP 下滑、HBM/advanced packaging 扩产导致价格下降、1.6T 价格竞争、CXL 仍停留在少数内部部署。即使数量增长，AI compute 与整机收入可因 ASP 下滑而下降。

**基准情景**：agentic inference 和长上下文使需求增长高于效率改善；HBM4、800G/1.6T、custom accelerator 与液冷同步扩张；CXL 从验证进入小规模生产；advanced packaging 保持较高利用率。

**上行情景**：推理请求、reasoning token 和模型并发超预期；大型客户同时扩张 GPU 与自研 ASIC；HBM/网络/封装继续供不应求，ASP 与数量同升。该情景容易产生重复下单和后续库存风险，不能外推为长期稳态。

### 利润池排序

1. **高利润率且规模大**：merchant accelerator、custom accelerator design/networking、HBM（紧缺期）、高端 switch/NIC、EDA/IP。
2. **规模上升、利润依赖良率/差异化**：advanced packaging、HBM packaging/test、CXL controller/switch、SerDes/retimer。
3. **高增长但价格侵蚀快**：可插拔 optical module；1.6T mix 可暂时抬高 ASP，成熟后仍会降价。
4. **金额大、利润率低**：AI server/ODM、通用机柜和 pass-through 集成。若没有液冷、功率控制、BIOS/firmware 和交付能力，收入增长未必转化为利润。
5. **高 optionality、高失败率**：3D-DRAM accelerator、通用 PIM、photonic compute、wafer-scale 新架构。

## 公司与产业链映射

| 公司/环节 | ISCA 2026 对应信号 | 可映射产品/利润池 | 应跟踪的现实节点 | 主要反作用或风险 |
|---|---|---|---|---|
| NVIDIA | MoE 调度、memory wall、network collective、energy wall | GPU/系统、HBM attach、NVLink/InfiniBand/Ethernet、DPU、软件 | DC compute/network 增速、Rubin 供货、token/$、network attach | 软件效率和客户自研 ASIC 减少每任务 GPU 数；高毛利吸引替代 |
| AMD | GPU+CPU+Helios rack、CXL host、chiplet | Instinct、EPYC、ROCm、scale-up/system | MI450/Helios 客户、Data Center mix、ROCm 迁移 | 软件生态、供货、网络完整性和 NVIDIA 平台效应 |
| Broadcom | custom accelerator、scale-up/out Ethernet、Meta MTIA | XPU design、switch/SerDes/DSP、PCIe/CXL | AI revenue、客户数、2nm MTIA 节点、network mix | 大客户集中；custom silicon 可压低 merchant ASP |
| Marvell | 800G/1.6T、51.2T、NPO/CPO、XPU attach | optical DSP、switch、custom silicon、CXL/XConn/Celestial | data center revenue、1.6T shipment、CPO/NPO 客户 | 光模块 ASP 下降、项目时序、客户集中 |
| Meta | Vistara、MTIA 300、Power Sloshing、KernelEvolve | 不是传统供应商利润池；是自研 silicon/系统的需求和替代信号 | MTIA 四代路线、Vistara 扩展、生产 SLO/功率数据 | 自研成功会分流外部 GPU；公司数据难外推其他客户 |
| Google/Microsoft/AWS | Prometheus cooling、Lifecycle、TPU/Trainium 等自研趋势 | 自研 ASIC、云服务、网络/冷却采购 | 自研芯片部署、客户可用实例、PUE/refresh | 技术收益可能被内部化，供应商未必获得利润 |
| Micron / SK hynix / Samsung | HBM、CXL、PIM/PNM、ECC、SSD active tier | HBM4/4E、DDR5/SOCAMM、CMM-D、enterprise SSD | HBM bit/ASP/yield、长期合约、CXL module 客户、SSD mix | 扩产后价格周期；CXL 复用旧 DDR 可能少买新 DRAM |
| TSMC / ASE / Amkor / substrate/test | Chiplet、3D-DRAM、wafer-scale、advanced package | CoWoS/SoIC 类封装、bonding、substrate、test | package wafer、良率、cycle time、客户集中 | 资本密集、扩产后价格下降、复杂封装 yield 风险 |
| Cadence / Synopsys / Arm / Rambus 等 IP | PhaseWeave、Cerberus、CXL、SerDes/HBM、many-core | 3D-IC/thermal/signoff、verification、CPU/NoC/CXL/HBM IP | ACV/backlog、core EDA/IP 增速、先进节点 design start | AI 自动化可能降低单项人时，但通常提高设计数量/复杂度 |
| Samsung CMM-D / Panmnesia / Astera 等 CXL 链 | Vistara 与 silicon-proven switch | module、controller、switch、retimer、software | merchant 出货、CPU/OS 认证、真实 p99、客户数 | 市场小、标准代际快、CXL 被误用作低时延层 |
| d-Matrix / Alchip / Andes | Raptor early silicon | 3D-DRAM inference accelerator、ASIC design、RISC-V control | 可获得产品、客户 benchmark、良率/热、软件支持 | 初创融资与技术路线风险；厂商自报 benchmark |
| Dell / HPE / Supermicro / ODM / cooling | Power Sloshing、Lifecycle、Prometheus、energy keynote | AI server、rack、液冷、power management、服务 | rack 出货、液冷 attach、GM、售后和 site qualification | GPU pass-through 导致收入高毛利低；项目交付/客户 CapEx 波动 |
| 光器件/模块/CPO 链 | 光子计算负面结果与 interconnect 增长并存 | 800G/1.6T、laser、DSP、NPO/CPO package | 等级迁移、ASP、良率、field failure、维修模式 | 把 photonic compute 叙事错误映射给所有光互连公司 |

### 产业参与的两个重要信号

1. [Meta 2026-03 官方路线](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)称已部署数十万 MTIA inference chip，MTIA 300 已用于 ranking/recommendation training 并进入生产，未来两年推进 300/400/450/500 四代，并强调 PyTorch、vLLM、Triton 和 OCP。官方 ISCA program 又把 MTIA 300 定义为首个带 built-in NIC 和 collective offloading engine 的 Meta training chip。**含义**：网络和软件兼容已进入加速器本体，custom ASIC 不再只是“算力核”。
2. [Meta 与 Broadcom 2026-04 官方合作](https://about.fb.com/news/2026/04/meta-partners-with-broadcom-to-co-develop-custom-ai-silicon/amp/)提出先部署超过 1GW custom silicon、再走向多 GW；这既扩大 custom silicon/网络/封装需求，也说明 merchant GPU 的总市场份额不能简单按总 AI CapEx 外推。

## 反共识洞见：过度乐观、被低估与伪受益

### 市场过度乐观的方向

1. **光子计算短期替代数字矩阵乘。** ISCA 会后材料给出相反证据；除非完整系统在等精度、等吞吐和 wall-plug energy 下胜出，否则只应给予远期 optionality。
2. **CXL 可以替代 HBM。** Vistara 的成功来自冷热页分层和旧 DDR4 低成本，而非低时延；约 10× 带宽差和约 60% 负载时延差不能忽略。
3. **PIM 是通用 GPU 替代。** 多篇 PIM 论文反映需求真实，但数据布局、编程、ECC/热、模型快速变化和客户迁移使其更可能先服务稳定 kernel。
4. **论文 speedup 等于可售产品优势。** PLENA、Dorado、PhaseWeave、Five-Minute Rule 的高倍数主要是模拟/归一化；需要以真实 SLO、价格、功率和软件折扣。
5. **所有先进封装扩产都保持高毛利。** 需求方向确定，但扩产、良率、package mix、客户议价和折旧决定利润；commodity substrate/OSAT 与顶级 2.5D/3D 能力不可混同。
6. **AI server 收入高增长等于利润高增长。** GPU/HBM 是大额 pass-through，ODM/整机毛利可能只有个位数至十几；真正差异化在液冷、供电、firmware、服务和交付。

### 被低估的方向

1. **功率和调度软件。** 5%—10% fleet 级节电乘以已安装数十亿美元服务器资产，可能比一颗新芯片更快形成客户 ROI。
2. **ECC、RAS 和验证。** 更高 stack、3D bonding、CXL pooling、wafer-scale 扩大故障域，可靠性会从成本项变成可用容量和 SLA 的决定项。
3. **CPU/control plane 与 context storage。** Agentic AI 不只是 GPU token；工具调用、程序执行、数据获取、checkpoint/context store 增加 CPU、DDR、SSD 和网络负载。
4. **CXL 的“资产回收”价值。** Vistara 的核心商业意义之一是让旧 DDR4 进入新服务器；这可能提高 controller/software 利润，却不同比例增加新 DRAM bit。
5. **EDA/IP/thermal/test。** Chiplet、HBM4、3D-DRAM 和 CXL 引入的验证、SI/PI、热、封装和互操作复杂度，比 nominal transistor 数更难压缩。
6. **光互连而非光计算。** ISCA 的负面 photonic compute 结果并不削弱 800G/1.6T、CPO/NPO 的数据移动需求；反而要求把两者估值逻辑分开。

### 伪受益方向

- 只有“CXL”标签、却没有 CPU/OS 认证、RAS、switch management 和真实客户的 module/controller。
- 只有普通封装产能、没有大型 interposer、hybrid bonding、thermal/test 和良率能力的 OSAT/材料供应商。
- 停留在 400G commodity、无法进入 800G/1.6T 或缺少 DSP/laser/封装协同的光模块供应商。
- 只做机箱组装、没有高密度供电/液冷/BIOS/firmware/现场服务的“AI server”公司。
- 把光子传感、光通信收入直接映射为 photonic AI compute 收入的公司。
- 把学术 PIM demo 当成大规模 HBM/GPU 替代、却没有 compiler/runtime、模型客户和量产存储合作方的项目。

## 风险与可证伪条件

| 研究结论 | 支持结论应出现的节点 | 证伪/降权节点 | 检查时间 |
|---|---|---|---|
| MoE 数据移动成为核心瓶颈 | vLLM/主流 runtime 或 hyperscaler 披露 expert placement/replication，端到端吞吐 >10% 或网络流量明显下降 | 主流 workload 转向 dense/smaller model；真实流量提升 <5% 或局部性随模型/任务失效 | 2026 Q4—2027 H1 |
| CXL 作为容量层成立 | 第二家以上公开生产客户；merchant module/controller 出货；eligible server 渗透达到约 2%—4% | 仍只有内部 DDR4 回收场景；p99/带宽导致客户关闭 tiering；渗透低于 2% | 2027 H1—H2 |
| CXL 不替代 HBM | 产品继续用于 cold page/CPU memory，GPU 热数据留 HBM | 若出现公开量产 GPU memory pooling，在主流训练/推理上接近 HBM SLO/TCO，则需重估 | 持续至 2028 |
| HBM 收入继续高增 | HBM4/4E qualification、stack/accelerator 上升、2027 TAM 接近基准 700 亿美元 | accelerator 出货放缓、良率/封装供给过剩、stack ASP 大幅下降，TAM <520 亿美元 | 每季至 2027 年末 |
| 3D-DRAM 有商业价值 | Raptor 在 2027 年中前提供客户可获得系统和同 SLO 独立 benchmark；热/良率稳定 | 延期、仅 test chip、客户不公开、相对 HBM 优势在整机低于 20% | 2027 H1—H2 |
| 功率软件被低估 | 生产 fleet 在 p99 违规增加不超过 1 个百分点时节电 ≥8% | 突发 workload 使违规显著上升，平均节电 <3% | 2026 Q4—2027 Q1 |
| photonic compute 被高估 | 若完整论文仍显示等精度等吞吐至少 5× 更耗能，结论增强 | 独立 silicon 在含 laser/ADC/DAC 的 wall-plug energy 上优于数字 ≥2×，且精度/SLO 相同 | proceedings 发布后至 2028 |
| advanced packaging 保持利润 | utilization >85%、cycle time 长、复杂 package mix/良率改善 | 扩产后 utilization <80%、ASP/毛利下降、客户转向更简单封装 | 2027 全年 |
| custom ASIC 稀释 merchant GPU 份额 | MTIA/TPU/Trainium 等生产量和 Broadcom/Marvell custom revenue 持续高增 | 软件迁移失败或客户回到通用 GPU，自研芯片利用率低 | 2027—2028 |
| EDA/IP 是稳定受益层 | core EDA/IP、HBM/SerDes/CXL IP 增速保持双位数，ACV/backlog 增长 | design start 减少、客户内制/开源替代、AI automation 导致价格压缩 | 每季至 2028 |

### 额外风险

- **材料完整性**：若干 ISCA 2026 最终 proceedings、slides/video 尚未完全公开索引；作者帖只作为中等置信线索。
- **选择偏差**：会议偏好新颖性，不代表量产路线优先级；industry paper 亦可能只展示成功 workload。
- **模型范式变化**：dense/MoE、参数规模、上下文长度、speculative decoding 和量化会改变内存/网络瓶颈。
- **供应与地缘政治**：先进制程、HBM、封装、出口限制和客户地区会改变单位量价。
- **标准竞争**：NVLink、UALink、Ethernet、CXL/PCIe、proprietary fabric 的演进可能造成重复投资和迁移成本。
- **收入重复计算**：NVIDIA/Broadcom 等披露含系统、网络或 custom mix；本报告的市场池是分析归类，不能直接加总为“AI 市场总额”。
- **毛利周期**：紧缺期的 HBM、封装和光模块毛利不能作为长期稳态；价格下降可能快于出货增长。

## 来源清单

### 会议官方与议程

| 来源 | 日期/状态 | 类型 | 用途 | 置信度 |
|---|---|---|---|---|
| [ISCA 2026 官方主页/awards](https://iscaconf.org/isca2026/) | 检索至 2026-07-10 | 会议官方 | 日期、地点、Best Paper | 高 |
| [ISCA 2026 full program](https://iscaconf.org/isca2026/program/) | 会后公开 | 会议官方 | keynote、sessions、论文题目/作者、industry track | 高 |
| [ISCA 2026 workshops/tutorials](https://iscaconf.org/isca2026/program/workshops.php) | 会后公开 | 会议官方 | workshop 技术方向 | 高 |

### 核心论文、作者材料与数据

| 来源 | 日期/版本 | 类型 | 主要使用内容 | 置信度 |
|---|---|---|---|---|
| [Patterns Behind Chaos](https://arxiv.org/abs/2510.05497) | v5，2026-05-12 | 作者论文 | 4 个大型 MoE、24,000+ 请求、6.6×/1.25× | 高（方法/摘要）；商业外推中 |
| [MoE Expert Selection Trace](https://huggingface.co/datasets/core12345/MoE_expert_selection_trace) | 检索 2026-07-10 | 作者数据集 | 公开 trace、模型覆盖、约 199GB | 高 |
| [Cerberus](https://arxiv.org/abs/2605.02220) | v2，2026-05-14 | 作者论文 | 跨层 ECC、冗余/性能/能耗、模拟条件 | 高 |
| [Vistara camera-ready](https://jovans2.github.io/files/vistara_camera_ready.pdf) | ISCA 2026 | 作者论文/产业实践 | CXL ASIC、OS、生产 workload | 高 |
| [Panmnesia ISCA 2026 CXL](https://panmnesia.com/news/en/2026-06-24-panmnesia-isca2026-eng/) | 2026-06-24 | 公司一手/论文摘要 | silicon-proven controller/switch、64 节点、产品状态 | 中 |
| [PLENA](https://arxiv.org/abs/2509.09505) | v3，2026-04-12 | 作者论文 | 长上下文 accelerator、量化、2.23×/4.70×/4.04× | 高（论文）；商业外推中低 |
| [Five-Minute Rule 40 Years Later](https://arxiv.org/abs/2511.03944) | v2，2026-05-08 | 作者论文 | Storage-Next、IOPS、break-even、MQSim | 高（模型）；产品外推低 |
| [Raptor author publication page](https://prashantnair.bitbucket.io/publications/) | 会后更新 | 作者材料 | 3D-DRAM 架构、workload、4.71×/2.44× | 中高 |
| [d-Matrix 3D-DRAM/Pavehawk](https://www.d-matrix.ai/going-vertical-why-we-created-a-3d-dram-solution-to-advance-low-latency-ai-inference/) | 2026-03-16 | 公司一手 | test chip 与 Raptor 产品关系 | 中 |
| [PhaseWeave](https://www.microsoft.com/en-us/research/publication/phaseweave-phase-aware-execution-on-heterogeneous-chiplet-architectures-for-datacenters/) | 2026-04 | 作者/公司研究页和论文 | phase predictor、模拟/真实实验、P99/吞吐/功耗 | 高 |
| [Power Sloshing camera-ready](https://jovans2.github.io/files/power_sloshing_isca_camera_ready.pdf) | ISCA 2026 | 作者论文 | 空闲 TDP、节电、SLO 风险 | 高 |
| [Rearchitecting Datacenter Lifecycle for AI](https://www.microsoft.com/en-us/research/publication/rearchitecting-datacenter-lifecycle-for-ai-a-tco-driven-framework/) | ISCA 2026 | 作者/公司研究页和论文 | build/provision/operation TCO | 高（模型）；实际节省中低 |
| [Dorado camera-ready](https://jovans2.github.io/files/dorado_isca_camera_ready.pdf) | ISCA 2026 | 作者论文 | 1,024-core coherence 模拟 | 高（论文）；产品外推低 |
| [Shining Light 作者会后说明](https://www.linkedin.com/posts/avilash-mukherjee_shining-light-isca-2026-presentation-activity-7478469082007240704-EPsy) | 2026-07，会后 | 作者公开说明 | 信号完整性、等精度/等吞吐至少 5× 能耗 | 中；待 proceedings |

### 公司与产业一手材料

| 来源 | 日期 | 主要使用内容 | 置信度 |
|---|---|---|---|
| [NVIDIA FY2027 Q1 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx) | 2026-05-20 | DC compute/network 收入、gross margin | 高 |
| [Broadcom FY2026 Q1 results](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial) | 2026-03-04 | AI revenue、增长与下一季指引 | 高 |
| [AMD 2026 Q1 results](https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results) | 2026-05-05 | Data Center 收入与 MI/EPYC 驱动 | 高 |
| [Micron HBM TAM presentation](https://investors.micron.com/static-files/530bd7ed-a8c8-4687-af4a-8c129f740e09) | 2025-12-17 | 2025 HBM TAM、至 2028 CAGR/TAM | 高（公司预测） |
| [Micron FY2026 Q3 prepared remarks](https://investors.micron.com/static-files/631b1a32-5537-46ae-8f40-82e42fc79dfe) | 2026-06-24 | HBM4 出货、供需、server/SSD/context 趋势 | 高（公司披露/预测） |
| [Marvell FY2027 Q1 filing](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-26-000014/q127_8kx522026ex-991.htm) | 2026-05-27 | 收入、800G/1.6T、switch、CPO/NPO、XPU | 高 |
| [TSMC 2026 Q1](https://investor.tsmc.com/english/quarterly-results/2026/q1) | 2026-04-16 | 收入、HPC 与先进制程 mix | 高 |
| [Cadence 2026 Q1](https://investor.cadence.com/news/news-details/2026/Cadence-Reports-First-Quarter-2026-Financial-Results/default.aspx) | 2026-04-27 | core EDA/IP 增速及 HBM/PCIe/SerDes 驱动 | 高 |
| [Synopsys FY2026 Q2](https://news.synopsys.com/2026-05-27-Synopsys-Posts-Financial-Results-for-Second-Quarter-Fiscal-Year-2026) | 2026-05-27 | 收入与 FY2026 指引 | 高 |
| [Arm FY2026 Q4 transcript](https://investors.arm.com/static-files/78526857-5997-46eb-9b65-0d3249d83711) | 2026-05-06 | FY 收入、DC royalty、DPU/SmartNIC | 高 |
| [Meta custom silicon roadmap](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/) | 2026-03-11 | MTIA 部署、300/400/450/500、软件/OCP | 高（公司披露/前瞻） |
| [Meta–Broadcom custom silicon partnership](https://about.fb.com/news/2026/04/meta-partners-with-broadcom-to-co-develop-custom-ai-silicon/amp/) | 2026-04 | 1GW 到多 GW、multi-generation MTIA | 高（前瞻） |
| [Samsung 256GB CXL 2.0 CMM-D](https://semiconductor.samsung.com/us/cxl-memory/cmm-d/md210/mxfaf2560b40-cql/) | 检索 2026-07-10 | 256GB、PCIe 5.0×8、30.5GB/s、mass production | 高（产品页） |
| [SK hynix HPE Discover 2026](https://news.skhynix.com/hpe-discover-2026/) | 2026-06 | CXL pooled memory、PNM 与 HMSDK | 中高（公司展示） |

## 最终投资判断

ISCA 2026 对产业路线的最重要修正，不是宣布某种新器件立刻取代 GPU，而是把“可交付 AI 计算”重新定义为一个由 **计算、内存层级、网络、可靠性、功率、冷却和调度**共同决定的系统产品。

近期最值得给予收入确定性的仍是 HBM4、AI networking、800G/1.6T、先进封装和 EDA/IP；CXL 是小基数高弹性，但应按容量层而非 HBM 替代估值；3D-DRAM 是最值得跟踪的早期硅方向之一，却必须等独立客户 benchmark；photonic compute 和通用 PIM 仍应保持高折扣。

真正可能形成反共识收益的，是那些能以较小新增成本释放昂贵 installed base 的技术：MoE 数据放置、动态功率、冷热页迁移、ECC/RAS、collective offload 和全生命周期调度。它们的论文倍数未必最高，却最接近客户可验证的现金回报。
