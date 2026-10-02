# 行业调研：【AI-native存储与KV Cache基础设施】

> 截至日期：2026-05-08  
> 口径：美元名义值；`B` = 十亿美元。市场规模为研究估算，优先使用公司公告、官方技术资料、财报/电话会、行业报告作为锚点；对缺失直接数据采用偏乐观假设。本文不是投资建议。

## 0. 高浓度结论

2026 年 AI-native 存储与 KV Cache 基础设施的核心判断是：**推理基础设施正在从“GPU + 普通存储”进入“GPU/HBM + 共享 KV cache + CXL/DDR/NVMe 分层 + DPU/RDMA + KV-aware 调度”的新架构周期**。训练时代的存储卖点是吞吐、checkpoint、数据湖；agentic inference 时代的新增卖点是 **TTFT、tokens/sec、tokens/W、KV cache 命中率、上下文复用率、尾延迟和 GPU 空转率**。

一手信号已经出现：

- NVIDIA 在 GTC 2026 发布 BlueField-4 STX/CMX，把 KV cache 定义为 pod-level context memory tier，宣称相对传统存储最高 `5x` token throughput、`4x` energy efficiency、`2x` page ingestion；早期采用方包括 CoreWeave、Crusoe、IREN、Lambda、Mistral AI、Nebius、OCI、Vultr，存储/制造生态包括 Cloudian、DDN、Dell、HPE、IBM、MinIO、NetApp、Nutanix、Supermicro、QCT、VAST Data、WEKA 等。来源：[NVIDIA STX 发布](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Launches-BlueField-4-STX-Storage-Architecture-With-Broad-Industry-Adoption/default.aspx)、[NVIDIA CMX 产品页](https://www.nvidia.com/en-us/data-center/ai-storage/cmx/)。
- NVIDIA Dynamo 文档已把 KV cache 管理写成独立层：GPU/CPU/SSD/object storage 多层缓存、KV-aware routing、NIXL 传输、vLLM/SGLang/TensorRT-LLM 后端。来源：[Dynamo 架构](https://docs.dynamo.nvidia.com/dynamo/v-0-9-0/design-docs/overall-architecture)、[Dynamo KV Cache Manager](https://docs.nvidia.com/dynamo/archive/0.2.1/architecture/kv_cache_manager.html)。
- WEKA、VAST、DDN、Supermicro、Penguin Solutions 等已把 shared KV cache、CXL KV cache server、DPU-native inference data path 作为正式产品/路线发布。WEKA 称其 NeuralMesh + STX 可带来 `4-10x` context-memory tokens/sec、`320GB/s read + 150GB/s write`；Penguin MemoryAI 宣称 `11TB` CXL KV cache server，含 `3TB DDR5 + 8 x 1TB CXL AIC`；DDN 称 Rubin/BlueField-4 方案可支持 distributed KV cache tiering、`20-40%` TTFT 降低、最高 `99%` GPU utilization。来源：[WEKA](https://www.weka.io/company/weka-newsroom/press-releases/neuralmesh-nvidia-stx/)、[Penguin](https://s204.q4cdn.com/917347554/files/doc_news/Penguin-Solutions-Introduces-Industrys-First-Production-Ready-CXL-Based-KV-Cache-Server-2026.pdf)、[DDN](https://www.ddn.com/press-releases/ddn-powers-integrated-compute-data-and-offload-at-scale-for-nvidia-rubin-platform/)。
- 供给侧正在出现“存储不再是低价 commodity”的反转。TrendForce 预计 2Q26 conventional DRAM 合约价季增 `58-63%`、NAND Flash 季增 `70-75%`，并称高性能 enterprise SSD 订单无放缓、2026 年供给明显短缺、有效扩产要到 2027 年底或 2028 年；Gartner 预计 2026 半导体收入 `$1.320T`，其中 memory `$633.3B`，DRAM 年度价格 `+125%`、NAND `+234%`，AI semis 占总收入约 `30%`。来源：[TrendForce 2Q26 memory](https://www.trendforce.com/presscenter/news/20260331-12995.html)、[Gartner semiconductor 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)。
- HDD/冷数据层也变成 AI 基建瓶颈。Seagate 2026 Q3 电话会称 nearline capacity 几乎已分配到 calendar 2027；Q3 FY2026 收入 `$3.1B`、同比 `+44%`，non-GAAP gross margin `47%`，data center 占 exabyte 出货 `88%`、收入 `80%`；Mozaic 4 可达 `44TB/drive`，Mozaic 5 目标 `50TB`、late calendar 2027 qualification。来源：[Seagate Q3 FY2026 transcript](https://s24.q4cdn.com/101481333/files/doc_financials/2026/q3/CORRECTED-TRANSCRIPT_-Seagate-Technology-Holdings-Plc-STX-US-Q3-2026-Earnings-Call-28-April-2026-5_00-PM-ET.pdf)。

**投资主线排序：**

1. **最确定：AI 存储软件/数据平台 + DPU/RDMA 集成。** 不依赖某一款 GPU 单品，直接受益于训练、RAG、agentic inference、checkpoint、上下文复用。
2. **弹性最大：共享 KV cache / STX-CMX / CXL KV server。** 当前基数小，2026H2 从 pilot/early adoption 进入产品验证，2027 有机会从“优化项”变成大模型推理集群标配。
3. **利润率最强：CXL controller/switch、BlueField/SmartNIC、KV runtime/control plane、企业存储软件。** 硬件硅/软件结合，客户认证和切换成本高。
4. **周期反转：enterprise SSD、nearline HDD。** 2026-2027 LTA、价格传导、AI 数据保留需求支撑利润率；但 NAND/HDD 是强周期，2028 后需防扩产正常化。

## 1. 行业定义与 2026 机会/挑战

### 1.1 本行业包含什么

| 层级 | 典型产品 | 核心指标 | 2026 状态 |
|---|---|---|---|
| GPU 本地 KV 管理 | vLLM PagedAttention、SGLang、TensorRT-LLM KV cache、Dynamo KVBM | HBM 利用率、batch size、cache waste、TTFT | 已大规模使用，软件快速迭代 |
| 跨节点/跨请求 KV cache | LMCache、Mooncake、Dynamo、WEKA Augmented Memory Grid、VAST shared KV | cache hit rate、prefill 复用、跨节点传输带宽 | 2025 开源/生产案例，2026 商业化加速 |
| AI-native context storage | NVIDIA STX/CMX、BlueField-4/DOCA Memos、DDN CME、VAST AI OS、WEKA NeuralMesh | tokens/sec、tokens/W、RDMA latency、SSD/flash tier 命中率 | 2026H2 进入首批产品供给 |
| CXL memory tier | Micron CZ120/CZ122、Samsung CMM-D、Astera Leo、Penguin MemoryAI | 每节点 TB 级扩展、ns 级延迟、CXL 带宽、NUMA/tiering | 2026 从 preview/PoC 到 limited production |
| AI 数据平台 | DDN、Dell、HPE、NetApp、Pure/Everpure、VAST、WEKA、IBM、MinIO、Cloudian | checkpoint 吞吐、metadata ops、GDS/RDMA、数据治理 | 已放量，AI attach rate 提升 |
| SSD/HDD/冷层 | enterprise NVMe SSD、QLC SSD、nearline HDD、HAMR、object/archive | $/TB、W/TB、IOPS、LTA、交付期 | 2026 供给紧、价格上行 |

### 1.2 2026 最大机会

1. **agentic inference 让 KV cache 从“运行时细节”变成“基础设施预算项”。** 长上下文、多轮工具调用、代码 agent、RAG、multi-agent 协作会重复使用大量上下文。没有共享 KV cache，GPU 会反复 prefill/recompute，吞吐和成本恶化。
2. **Rubin/GB300/MI400/TPU/Trainium/ASIC 同时提高 HBM 与外部存储压力。** 项目中已有芯片路线显示 2026 出货主力仍是 Blackwell/GB300、Trainium2、TPU Ironwood、MI350、国产 Ascend/寒武纪等；2026H2-2027 Rubin、MI400、Trainium3、TPU8、OpenAI/Broadcom/Meta ASIC 放量。高 HBM 容量并不会消灭 KV tier，反而会因 context 与并发同步增长而放大外部 context-memory 需求。
3. **AI 数据中心 capex 极乐观假设下，存储/内存/数据网络占比上修。** Gartner 2026 memory `$633.3B`、AI semis 约总半导体 `30%`；IDC 外部企业存储系统 2026 `$37.9B`、2027 `$40.0B`，但这是传统 ESS 口径，不包含 hyperscaler 自研存储、SSD/HDD 长协、KV cache 新层，真实 AI 数据存储支出更大。
4. **DPU/SmartNIC 把存储从 CPU data path 旁路。** BlueField-4 STX 将 NVMe、KV cache integrity/encryption、DOCA Memos、Spectrum-X RDMA 打包，目标是降低 CPU copy 和尾延迟。
5. **存储供给侧短缺增强利润率。** 企业级 SSD、nearline HDD、DDR5/CXL DRAM、PCIe/CXL controller 供给被 AI 锁定，客户更愿意签 3-5 年 LTA。

### 1.3 最大挑战

| 挑战 | 为什么难 | 对投资的含义 |
|---|---|---|
| KV cache 命中率不稳定 | 真实请求是否复用 prefix/context 取决于产品形态、prompt 模板、agent 工作流 | 需要看“可复用上下文比例”，不是只看硬件带宽 |
| 尾延迟与一致性 | KV cache 从 HBM 移到 CPU/SSD/CXL 后，P99/P999 很容易拖垮服务体验 | 真正有壁垒的是调度、prestage、RDMA、placement、eviction |
| CXL NUMA/tiering 软件不成熟 | CXL 延迟高于 DRAM，Samsung CMM-D 测试显示 local CXL 约 `254ns`、remote CXL 约 `353ns`，RDIMM local 约 `144ns` | CXL 不是 HBM 替代品，而是 warm/hot-but-not-hottest tier |
| SSD/HDD 供给瓶颈 | NAND/HDD 媒体、HAMR、controller、企业认证长周期 | 2026-2027 ASP 和毛利偏强，但扩产/需求放缓后会回落 |
| 与模型架构共同演化 | MLA/GQA/MQA、KV compression、linear/SSM attention 会改变 KV footprint | 硬件产品必须支持多策略、多模型，而非押注单一 KV 格式 |
| 标准未完全统一 | vLLM/SGLang/TensorRT-LLM、Dynamo、LMCache、Mooncake、DOCA Memos 接口仍在演进 | 开源生态与 NVIDIA 生态的桥接者更有价值 |

## 2. 技术路径与成熟/放量时间

### 2.1 当前正在使用的技术

| 技术 | 成熟度 | 代表 | 价值 |
|---|---|---|---|
| PagedAttention / block KV allocation | 成熟，已是 vLLM 核心能力 | vLLM | 将 KV cache waste 从传统 `60-80%` 降到极低，vLLM 早期相对 HF 最高 `24x` throughput |
| Continuous batching / KV-aware routing | 成熟到快速迭代 | vLLM、SGLang、Dynamo | 提高 GPU 利用率，减少 idle |
| CPU DRAM KV offload | 2026 快速产品化 | vLLM 0.11/0.12 KV offloading、LMCache | 用 DDR 扩 context/concurrency，短期最现实 |
| Disk/NVMe/S3 KV reuse | 早期商业化 | LMCache、Mooncake、WEKA AMG、VAST | 降低重复 prefill，适合 RAG/agent/code |
| Disaggregated prefill/decode | 快速增长 | Mooncake、vLLM、Dynamo | 把 prefilling 与 decoding 的算力/内存特征拆开，提高集群效率 |
| DPU-native storage/KV | 2026H2 量产导入 | BlueField-4 STX/CMX、DDN/VAST/WEKA | CPU 旁路、RDMA、KV 存储服务下沉 |
| CXL memory expansion | 2026 limited deployment | Astera Leo + Azure M-series preview、Micron CZ120/122、Samsung CMM-D、Penguin MemoryAI | TB 级 memory tier，补 HBM/DDR 与 NVMe 中间层 |
| CXL pooling / PNM | 研发/早期 | CXL-PNM、Pangaea、CHMU、DPC | 2027 以后更有爆发潜力 |
| KV compression / eviction | 研究快速活跃 | HybridKV、DMS、IceCache 等 | 减少 KV footprint，可能抑制部分外部 KV 硬件需求，但也让更长 context 可行 |

### 2.2 芯片路线背景下的需求映射

| 2026/2027 大芯片平台 | 对 KV/存储的含义 | 最受益层 |
|---|---|---|
| NVIDIA GB300/Blackwell Ultra | 2026 主力，NVL72 高密度，长上下文和推理并发上升 | 高吞吐并行文件、NVMe SSD、Dynamo/LMCache、BlueField-3/4 |
| NVIDIA Rubin/Vera/LPX/STX | 2026H2/2027 新架构，STX 直接把 KV cache tier 打入 rack-scale 设计 | CMX/STX、DPU、Spectrum-X、WEKA/VAST/DDN |
| AMD MI350/MI400/Helios | MI400 HBM4 和 rack-scale 推理/训练，会增加 UALink/Ethernet 与外部 cache 需求 | 开放 Ethernet AI fabric、并行文件、CXL/DDR tier |
| Google TPU Ironwood/TPU8 | Google 自研 pod，推理优先，内部 storage/cache 优化强 | 内部 KV/context tier、SSD/HDD 长协、OCS/网络 |
| AWS Trainium2/3 | Anthropic/Rainier 级集群，强依赖内部 EFA/NeuronLink 与存储栈 | AWS 内部存储、nearline HDD、对象存储、Trainium KV runtime |
| Broadcom XPU/OpenAI/Meta ASIC | 大规模定制推理，目标降低 token 成本，但仍需要 context memory | CXL/NVMe KV tier、DPU/SmartNIC、存储软件 |
| Microsoft Maia / Azure | Azure M-series CXL preview 是 CXL 云部署标志 | Astera Leo、CXL memory、Azure 内部 memory pooling |
| 中国 Ascend/寒武纪/阿里/百度 | HBM/先进封装受约束，可能更依赖系统级互联和外部 memory tier 弥补 | 国产 SSD/HDD、CXL/PCIe 控制、集群存储、对象存储 |

### 2.3 成熟与放量时间：三情景

| 技术方向 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---|---|
| GPU 本地 KV 管理 | 已成熟；2026 继续随 vLLM/SGLang/TensorRT-LLM 普及 | 2026H2 KVBM/LMCache/Dynamo 成为生产标配 | 2026 内云厂把 KV-aware routing 写入默认推理平台 |
| CPU/DRAM KV offload | 2026 上量，主要为中端推理和长上下文 | 2026H2 大量服务将 CPU offload 与 GPU batching 联动 | DRAM 高价仍不阻碍采用，因为节省 GPU 更值钱 |
| NVMe/shared KV tier | 2026H2 STX/WEKA/VAST/DDN pilot；2027 放量 | 2027H1 成为高端 Rubin/GB300 inference rack 选配 | 2026Q4 即有云厂生产案例，2027 变成 premium inference 默认配置 |
| CXL KV server | 2026 小批生产，2027 扩大 | Penguin/微软/Astera 等 2026H2 拿到更多生产客户 | 2027 年 CXL KV server 市场接近 `$4-6B`，超市场预期 |
| CXL pooling / DCD / CHMU | 2027 early production，2028 扩大 | 2027H2 hyperscaler 内部规模部署 | 2027H1 就出现多云公开 SKU |
| CXL-PNM / near-memory vector/KV | 2026 PoC，2027 early access | 2027 出现 FAISS/vector DB/vLLM 案例 | 2027 形成专用加速器子市场 |
| KV compression | 2026 研究与 runtime plugin 快速增加 | 2026H2 多模型默认支持 2-4x KV 压缩 | 压缩 + 外部 KV tier 共同释放 10x+ concurrency |

**2026 最可能技术路径：** PagedAttention/continuous batching + LMCache/Dynamo/Mooncake 级软件 KV 管理 + CPU DRAM offload + 高性能 NVMe/并行文件 + 首批 STX/CMX。CXL 更像高端客户的 limited deployment，不会在 2026 立刻变成大盘，但会成为估值叙事中最强的“下一层 memory”。

## 3. 已开始放量的关键产品：规模、渗透率、利润率

> “未来 3 个月”按 2026Q2-Q3 run-rate；“一年”按 2027 年中；“两年”按 2028 年中。市场规模为全球年化收入/支出口径估算。

### 3.1 已放量产品总表

| 产品/细分 | 2026 当前年化规模 | 未来 3 个月 | 未来 1 年：基准/乐观/极超 | 未来 2 年：基准/乐观/极超 | 渗透率路径 | 毛利率/利润率判断 |
|---|---:|---:|---:|---:|---|---|
| AI 数据平台/并行文件/对象存储 | `$12-18B` AI 子集；传统外部 ESS 2026 `$37.9B` | `$3.5-5.5B` | `$16-24B / $22-32B / $30-42B` | `$24-35B / $35-55B / $55-80B` | AI 训练/推理集群 attach 从 25-35% 到 50-70% | 软件 65-85%；一体机/系统 35-60%；ODM 集成 8-20% |
| Enterprise NVMe SSD / AI flash tier | `$55-85B` | `$15-25B`，价格继续上行 | `$70-110B / $95-140B / $130-180B` | `$85-130B / $130-200B / $190-260B` | AI 高性能存储 SSD attach 从 45-55% 到 65-80%；QLC 容量层提高 | NAND 紧缺下供应商毛利 35-55%，高端 SSD/控制器 45-65% |
| Nearline HDD / 冷数据与训练数据保留 | `$35-45B` | `$9-13B` | `$45-60B / $55-75B / $70-90B` | `$55-75B / $75-105B / $100-135B` | AI 数据湖/视频/物理 AI 长保留驱动；HDD 仍是 mass tier 主体 | Seagate Q3 FY26 non-GAAP GM 47%，2026-2027 可维持 40-50% 高位 |
| vLLM/SGLang/TensorRT-LLM/KV 管理软件 | 商业直接收入小，拉动 GPU 云与支持服务 `$1-3B` | `$0.3-0.8B` | `$3-6B / $5-9B / $8-14B` | `$6-12B / $12-22B / $20-35B` | 推理平台渗透率从 50%+ 到 80%+；企业付费支持提升 | 开源本体不捕获全部价值；托管/企业版毛利 70-90% |
| LMCache/Mooncake/shared KV software | `$0.3-1B` | `$0.1-0.3B` | `$1-2.5B / $2.5-5B / $5-8B` | `$3-7B / $7-14B / $14-25B` | 从长上下文/RAG/代码 agent 先渗透，2027 扩到通用推理 | 软件毛利 75-90%；若绑定硬件/云平台，收入可见度更高 |
| BlueField/DPU 存储 offload | `$2-5B` 与网络/DPU混合口径 | `$0.7-1.5B` | `$5-8B / $8-12B / $12-18B` | `$8-15B / $15-25B / $25-40B` | AI rack DPU attach 从 20-30% 到 50-70% | NVIDIA/高端 DPU 毛利接近高端网络硅，60-75% |
| CXL memory expansion modules/controllers | `$2-4B` | `$0.5-1B` | `$3-5B / $5-8B / $8-12B` | `$6-10B / $10-18B / $18-30B` | 2026 preview/limited；2027 高内存 VM、KV cache server 扩散 | controller 65-78%；CXL DRAM module 35-60%；系统早期溢价高 |
| GPU Direct Storage/RDMA data path | `$1-3B` 增量软件/网卡/认证口径 | `$0.3-0.8B` | `$3-5B / $5-8B / $8-12B` | `$6-10B / $10-18B / $18-25B` | 高端训练集群已较普及，推理 context tier 开始采用 | NIC/DPU 45-70%；软件/认证 70%+ |

### 3.2 已放量产品的关键事实

- **vLLM/PagedAttention：** vLLM 官方称传统 KV cache 管理因 fragmentation/over-reservation 浪费 `60-80%` 内存；PagedAttention 把 KV 分块映射到非连续内存，实际浪费低于 `4%`，早期测试相对 HF 最高 `24x` throughput。来源：[vLLM](https://vllm.ai/blog/vllm)。
- **LMCache：** 官方 GitHub 称可把 KV cache 存在 GPU/CPU/Disk/S3，并与 vLLM/SGLang/Dynamo/KServe 集成，典型长上下文/RAG/多轮 QA 用例可实现 `3-10x` delay savings/GPU cycle reduction。来源：[LMCache GitHub](https://github.com/lmcache/lmcache)。
- **Mooncake：** Kimi 服务平台采用 KVCache-centric disaggregated architecture，分离 prefill/decoding，利用 CPU/DRAM/SSD 资源做 disaggregated KVCache pool；论文称模拟场景最高 `525%` throughput 提升，真实 Kimi 工作负载多处理 `75%` 请求。来源：[Mooncake paper](https://arxiv.org/abs/2407.00079)、[Mooncake GitHub](https://github.com/kvcache-ai/Mooncake)。
- **CXL 已从 demo 到云 preview：** Astera Leo 支持 CXL 2.0、单 controller 最高 `2TB`，Azure M-series CXL preview 被 Astera 称为 industry first announced deployment of CXL-attached memory，目标 workload 包括 IMDB、big data、AI inference、KV cache storage。来源：[Astera + Microsoft Azure](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-leo-cxl-smart-memory-controllers-microsoft-azure-m)。
- **Samsung CMM-D 技术边界清晰：** CMM-D 支持 CXL 2.0/PCIe 5.0/E3.S 2T，容量 `128GB/256GB`；测试中 RDIMM local latency `144ns`，CMM-D local `254ns`，2 块 CMM-D 约 `52-62GB/s` 带宽；OLTP 场景接近无损，OLAP/HEX heap 不适合全部放 CXL。来源：[Samsung CMM-D white paper](https://download.semiconductor.samsung.com/resources/white-paper/Samsung_CMM-D_Utilization_in_IMDB_Applications.pdf)。

## 4. 在研/快速增长关键产品与细分技术

### 4.1 未来两年最值得跟踪的在研技术

| 技术/产品 | 当前阶段 | 未来 3 个月 | 未来 1 年：基准/乐观/极超市场规模 | 未来 2 年：基准/乐观/极超市场规模 | 利润率预测 |
|---|---|---:|---:|---:|---|
| NVIDIA STX/CMX + DOCA Memos | GTC 2026 发布，H2 伙伴可用 | 订单/PoC，收入小于 `$0.5B` | `$1-2B / $2-4B / $4-7B` | `$5-10B / $12-22B / $25-40B` | NVIDIA 硅/软件 65-75%；系统伙伴 25-55% |
| WEKA Augmented Memory Grid/STX | AMG 已 GA，STX 集成发布 | `$0.1-0.3B` | `$0.5-1B / $1-2B / $2-4B` | `$1.5-3B / $3-6B / $6-10B` | 软件高毛利，70-85%；硬件化后混合 45-65% |
| VAST AI OS on BlueField-4 | 2026-01 发布架构 | PoC/客户会议 | `$0.5-1.2B / $1-2B / $2-4B` | `$1.5-4B / $4-8B / $8-15B` | 软件订阅/一体化 55-80% |
| DDN Context Memory Extension / BlueField-4 offload | 2026-01/03 发布 | AI factory 项目导入 | `$1-2B / $2-4B / $4-6B` | `$3-7B / $7-12B / $12-20B` | 传统 HPC 存储 40-60%，数据智能软件可更高 |
| CXL KV cache server | Penguin 已称 production-ready | `$0.1-0.4B` | `$0.6-1.5B / $1.5-3B / $3-6B` | `$2-5B / $5-10B / $10-18B` | 初期溢价高，系统毛利 35-55%，controller 65-78% |
| CXL 3.x dynamic capacity/pooling | 标准与软件磨合 | 试点 | `$0.5-1B / $1-2B / $2-4B` | `$3-6B / $6-12B / $12-22B` | switch/controller 高毛利；软件管理 70%+ |
| CXL-PNM / near-memory vector/KV | 研究/PoC | 几乎无收入 | `<$0.2B / $0.5B / $1B` | `$1-3B / $3-7B / $7-12B` | 若标准化成功，SoC/加速器 55-70%；否则项目制利润不稳 |
| KV compression/eviction plugin | 论文多，工程化早期 | 开源插件增加 | `$0.2-0.5B / $0.5-1B / $1-2B` | `$1-3B / $3-6B / $6-10B` | 纯软件 75-90%，但商业化需要平台分发 |
| PCIe Gen6 enterprise SSD / ultra-high IOPS AI SSD | 2026 开始高端导入 | 工程样品/少量量产 | `$2-5B / $5-8B / $8-12B` | `$8-15B / $15-25B / $25-35B` | 高端 SSD 35-60%，controller/IP 50-70% |

### 4.2 技术洞见

- **外部 KV cache 与 KV compression 不是简单替代。** 压缩降低单 token KV footprint，但更低成本会诱发更长上下文、更高并发和更多 agent steps，可能增加总 KV tier 需求。
- **CXL 的第一波杀手场景不是替代 HBM，而是替代“为了内存而多买服务器/GPU”的过度配置。** Penguin 的 11TB KV cache server、Astera Azure preview、Samsung/Micron CMM 都指向这个逻辑。
- **DPU 是 AI-native storage 的价值捕获点。** SSD/HDD 本身较周期，但将 KV cache integrity/encryption、metadata、RDMA、prestage、telemetry 下沉到 DPU，会把存储系统从容量销售转为 token-goodput 销售。
- **开源 runtime 是标准入口，硬件厂商必须接入 vLLM/SGLang/LMCache/Dynamo。** 不能接入主流推理栈的硬件 KV tier 很难放量。

## 5. 供给侧：产能结构、瓶颈、成本与毛利

### 5.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/资产 |
|---|---|---|---|
| NAND/enterprise SSD | 韩国、日本、美国、新加坡、中国 | Samsung、Kioxia、WD/SanDisk、SK hynix/Solidigm、Micron、YMTC | 3D NAND、QLC/TLC、enterprise controller、U.2/E3.S/E1.S |
| HDD/nearline | 泰国、马来西亚、中国、美国研发 | Seagate、Western Digital、Toshiba | HAMR/CMR、盘片/磁头/马达/控制器 |
| CXL DRAM module | 韩国、美国、日本/台湾封测 | Samsung、Micron、SK hynix | DDR5 + CXL Type-3、E3.S/AIC |
| CXL/PCIe controller/switch/retimer | 美国、中国台湾、中国大陆、以色列 | Astera、Montage、Microchip、Marvell、Rambus、XConn、Synopsys/Cadence IP | PCIe 5/6/7、CXL 2/3/4、SerDes |
| DPU/SmartNIC/RDMA | 美国/以色列/中国台湾 | NVIDIA、Broadcom、Marvell、AMD/Pensando、Intel、Cisco | BlueField/ConnectX/Spectrum、Ethernet/IB/RoCE |
| 系统/OEM/ODM | 美国、中国台湾、中国大陆、墨西哥、东南亚 | Supermicro、QCT、AIC、Wiwynn、Foxconn、Dell、HPE、Lenovo | JBOF、AI storage server、liquid cooled rack |
| 存储软件 | 美国、以色列、欧洲、中国 | WEKA、VAST、DDN、Dell、HPE、NetApp、Pure、IBM、MinIO、Cloudian、Hammerspace | distributed filesystem/object、metadata、RDMA/GDS |

### 5.2 供给瓶颈

1. **NAND allocation 与 enterprise SSD 认证。** TrendForce 称 NAND 产能向 enterprise SSD 倾斜，高性能 SSD 订单无放缓，2026 明显短缺，扩产缓解要到 2027/2028。
2. **HDD HAMR/nearline 长交期。** Seagate nearline capacity 几乎分配至 calendar 2027，WD/Seagate/Toshiba 三家寡头下，客户签 LTA 后新客户拿货难。
3. **CXL controller/switch silicon 与互操作。** CXL 2.0 可用，CXL 3.x DCD/pooling 需要 OS/BIOS/BMC/Kubernetes/fabric manager 共同成熟。
4. **DPU/SmartNIC 与高端网络。** BlueField-4、ConnectX-9、Spectrum-X/6、Broadcom/Marvell 高速 SerDes 供给和认证决定 STX 类产品节奏。
5. **软件栈接入。** vLLM/SGLang/TensorRT-LLM/Dynamo/LMCache/Mooncake 的 KV layout、block size、NIXL/UCX/RDMA 接口仍在变。
6. **客户认证/数据完整性。** 存储系统进入 AI factory 需要数据一致性、加密、tenant isolation、telemetry、故障恢复、NVIDIA certification。
7. **人才与现场交付。** 高密度 AI rack 的 storage/network/power/cooling 联调需要跨 GPU、网络、文件系统、Kubernetes、模型服务的人才。
8. **封装/PCB/电源/冷却。** STX/CMX 不是普通存储阵列，高速 NIC/DPU/SSD 密度更高，E3.S 背板、电源完整性、散热都是瓶颈。

### 5.3 BOM 与价格传导

| 产品 | BOM/成本构成 | 毛利决定因素 | 价格传导 |
|---|---|---|---|
| AI storage appliance | SSD/HDD 35-55%，CPU/DPU/NIC 10-25%，DRAM 10-20%，chassis/power/cooling 10-20%，软件/支持 | 软件占比、NVIDIA 认证、RDMA/GDS 性能、客户锁定 | SSD/HDD/DRAM 涨价可向 hyperscaler/neo-cloud 传导，企业客户滞后 |
| STX/CMX storage node | BlueField-4/ConnectX/Spectrum-X、NVMe SSD、DDR/CXL、DOCA Memos、系统集成 | token throughput、tokens/W、KV 命中、生态认证 | 若按 token-goodput 销售，溢价强于普通 NVMe |
| CXL KV cache server | DDR5/CXL AIC 45-65%，controller/switch 10-20%，CPU/主板 10-20%，软件 5-15% | TB 级容量、延迟、NUMA/tiering、Dynamo/LMCache 兼容 | DRAM 高价推高 ASP，但节省 GPU 使客户接受 |
| Enterprise SSD | NAND die 55-75%，controller/DRAM/PMIC/PCB 10-20%，固件/验证 5-10% | NAND 供需、enterprise qualification、高 IOPS/低延迟 | 2026 卖方强，LTA 固定+浮动混合 |
| Nearline HDD | 磁盘/磁头/马达/HAMR 光子器件/控制器 | areal density、exabyte per unit、客户 LTA | 寡头 + capacity sold out 支持 value-based pricing |

## 6. 竞争格局与壁垒

### 6.1 市场结构

| 环节 | 集中度 | 竞争格局 |
|---|---|---|
| HDD | 极高，三家 | Seagate、Western Digital、Toshiba；HAMR/nearline 供给是核心 |
| NAND/enterprise SSD | 高，五到六家 | Samsung、Kioxia/WD、SK hynix/Solidigm、Micron、SanDisk/YMTC；周期强 |
| CXL controller | 高成长、头部未完全固化 | Astera 领先云端验证；Montage/Microchip/Marvell/Rambus/XConn 等竞争 |
| DPU/AI NIC | 高集中 | NVIDIA 强势，Broadcom/Marvell/AMD-Pensando/Intel/Cisco 分食 |
| AI data platform | 中高，软件壁垒强 | DDN/WEKA/VAST/Dell/HPE/NetApp/Pure/IBM/MinIO/Cloudian/Hammerspace |
| KV runtime | 开源快速迭代 | vLLM、SGLang、LMCache、Mooncake、Dynamo、TensorRT-LLM；商业价值被云/硬件/支持捕获 |

### 6.2 可量化壁垒：为什么能定价

| 壁垒 | 定价原因 |
|---|---|
| P99/P999 tail latency | 推理服务 SLA 对尾延迟敏感，能稳定降低 TTFT 的系统可按业务收入分成式定价 |
| GPU 利用率提升 | DDN 声称最高 99% GPU utilization、WEKA 声称 6.5x tokens/GPU，哪怕客户只实现 20-30%，节省 GPU capex 也远超存储成本 |
| 数据完整性与多租户隔离 | KV cache 不是普通临时文件，涉及用户上下文、隐私、加密、tenant boundary |
| NVIDIA/Rubin/BlueField 认证 | 高端 AI factory 采购看 reference architecture，进入名单后替换难 |
| Runtime 集成 | vLLM/SGLang/Dynamo/LMCache/Mooncake API 适配形成软件锁定 |
| Metadata 与小 IO 性能 | KV cache、checkpoint、RAG index 同时要求大吞吐和高 metadata ops，普通对象存储难以替代 |
| 供给锁定 | SSD/HDD/CXL/DRAM 短缺时，能交货本身就是定价权 |
| 数据迁移成本 | PB/EB 级训练数据、checkpoint、embedding、audit lineage 迁移成本极高 |

### 6.3 长期高 ROIC/高毛利最可能在哪

1. **KV cache control plane / inference memory OS。** 价值来自调度、命中率、跨节点一致性、tail latency，不只是硬件。
2. **DPU/SmartNIC/CXL controller。** 高速 SerDes + 协议 + 软件栈 + 认证，fabless 毛利可接近 70%+。
3. **AI data platform 软件。** 客户数据粘性强、生命周期长、能绑定 GPU 项目扩容。
4. **HDD nearline 寡头与 HAMR。** 2026-2027 供给纪律好，现金流强，但长期仍需看单位容量与价格正常化。
5. **高端 enterprise SSD。** 2026 利润强，但 NAND 周期属性更明显，长期 ROIC 不如软件和控制器稳定。

## 7. 2026 关键变化：三个最可能拐点

1. **STX/CMX 把 KV cache 写入 AI factory RFP。** 2026H2 若 CoreWeave/OCI/Mistral/WEKA/VAST/DDN/Supermicro 出现可复现 production case，KV cache tier 会从“性能优化”变成“采购清单”。
2. **存储 LTA 与涨价重塑利润率。** TrendForce/Gartner/Seagate 均验证 memory/SSD/HDD 供给紧张，2026 年 enterprise SSD、nearline HDD、CXL DRAM 模组毛利率可能显著高于传统存储周期。
3. **CXL 从组件验证转向云产品验证。** Azure M-series CXL preview、Penguin 11TB CXL KV server、Samsung/Micron 白皮书把 CXL 从概念推进到 limited deployment。2026 不一定大规模收入，但足以提高 Astera/Micron/Samsung/Penguin/Supermicro 等估值弹性。

## 8. 2027 关键变化：三个最可能拐点

1. **Rubin/MI400/Trainium3/TPU8 与定制 ASIC 放量，外部 context tier 放大。** HBM4 增加单节点能力，但 agentic workload 的上下文和并发增长更快，KV tier attach rate 提升。
2. **CXL 3.x pooling/Dynamic Capacity Device 进入生产集群。** CXL 4.0 已发布，但 2027 收入更可能来自 CXL 2.0/3.x 的 pooling、switch、DCD、NUMA/tiering 软件成熟。
3. **AI storage 从训练数据平台扩展到 inference revenue stack。** 2026 以前存储多按 checkpoint/数据湖预算；2027 premium inference 可能按 tokens/W 和 TTFT 评价存储，STX/CMX/WEKA/VAST/DDN 价值捕获上修。

## 9. 头部公司清单：尽量不遗漏

### 9.1 AI-native 存储/数据平台

- **头部/强技术：** DDN、WEKA、VAST Data、Dell Technologies、HPE、NetApp、Pure Storage/Everpure、IBM Storage Scale、MinIO、Cloudian、Nutanix、Hitachi Vantara、Hammerspace、Qumulo、Vdura/Panasas、Scality、Red Hat Ceph、Lenovo/Infinidat、Huawei OceanStor。
- **制造/系统：** Supermicro、QCT、AIC、Wiwynn、Foxconn/Ingrasys、Inventec、Gigabyte、ASUS、Jabil、Flex。
- **NVIDIA STX/AI Data Platform 生态：** NVIDIA、Cloudian、DDN、Dell、Everpure、Hitachi Vantara、HPE、IBM、MinIO、NetApp、Nutanix、Pure、Supermicro、QCT、VAST、WEKA、AIC。

### 9.2 KV cache runtime / inference software

- **开源与平台：** vLLM、SGLang、LMCache、Mooncake、NVIDIA Dynamo、TensorRT-LLM、Triton Inference Server、Hugging Face TGI、KServe、llm-d、AIBrix、Ray Serve。
- **商业推理平台/云：** Baseten、CoreWeave、Together AI、Fireworks AI、Anyscale、Modal、RunPod、Lambda、GMI Cloud、Cohere internal infra、Google Cloud GKE inference。
- **数据/缓存集成：** Redis、PliOps、WEKA、VAST、MinIO、object storage vendors。

### 9.3 CXL / memory expansion / disaggregated memory

- **控制器/retimer/switch/IP：** Astera Labs、Montage Technology、Microchip、Marvell、Rambus、XConn、Synopsys、Cadence、Intel、Broadcom、UnifabriX、Elastics.cloud。
- **内存模组：** Samsung CMM-D/CMM-H、Micron CZ120/CZ122、SK hynix CMM、SMART Modular、Netlist 相关生态。
- **系统/软件：** Penguin Solutions MemoryAI、Supermicro、Dell、HPE、Lenovo、MemVerge、VMware/Broadcom、Red Hat、Linux kernel/Kubernetes 社区。

### 9.4 SSD/HDD/控制器

- **NAND/SSD：** Samsung、Kioxia、Western Digital/SanDisk、SK hynix/Solidigm、Micron、YMTC、Phison、Silicon Motion、Marvell、InnoGrit、FADU。
- **HDD：** Seagate、Western Digital、Toshiba；关键上游包括盘片、磁头、HAMR 激光/光子、马达、控制器供应链。

### 9.5 DPU/NIC/网络/光互联

- **DPU/NIC/switch silicon：** NVIDIA BlueField/ConnectX/Spectrum-X、Broadcom Tomahawk/Jericho/Thor、Marvell、AMD Pensando、Intel IPU、Cisco、HPE Juniper。
- **交换机/系统：** Arista、Cisco、NVIDIA、HPE Juniper、Celestica、Accton、Edgecore、UfiSpace。
- **光模块/硅光/CPO：** Coherent、Lumentum、Broadcom、Marvell、Innolight、中际旭创、新易盛、Eoptolink、Fabrinet、AOI、MACOM、Credo、Ayar Labs、Lightmatter、iPronics、Intel Silicon Photonics。

## 10. 三情景总预测：2026-2028 投资框架

### 10.1 市场规模

| 口径 | 2026 基准 | 2026 乐观 | 2026 极超 | 2027 基准 | 2027 乐观 | 2027 极超 | 2028 中期极乐观上沿 |
|---|---:|---:|---:|---:|---:|---:|---:|
| AI-native 存储硬件/软件子市场 | `$25-40B` | `$40-60B` | `$60-85B` | `$40-65B` | `$70-105B` | `$110-160B` | `$200B+` |
| KV cache 基础设施直接收入 | `$2-5B` | `$5-9B` | `$9-15B` | `$8-18B` | `$18-35B` | `$35-60B` | `$80B+` |
| CXL memory/KV tier | `$2-4B` | `$4-7B` | `$7-10B` | `$5-10B` | `$10-20B` | `$20-35B` | `$45B+` |
| AI SSD/HDD/容量层 | `$90-130B` | `$120-170B` | `$160-220B` | `$115-170B` | `$170-260B` | `$260-350B` | `$400B+` |

### 10.2 渗透率

| 指标 | 2026 基准 | 2027 基准 | 乐观路径 | 极超路径 |
|---|---:|---:|---:|---:|
| 长上下文/agent 推理集群使用外部 KV tier | 5-10% | 20-30% | 40-55% | 65%+ |
| 高端 AI rack 配置 DPU-native storage/context tier | 10-20% | 30-45% | 55-70% | 80%+ |
| CXL memory 用于 AI/IMDB/高内存 VM | <5% 高内存服务器 | 8-15% | 20-30% | 35%+ |
| AI 数据平台支持 GDS/RDMA/KV-aware 接入 | 25-35% | 45-60% | 65-75% | 80%+ |
| SSD/HDD LTA 覆盖 hyperscaler AI 存储采购 | 50-65% | 60-75% | 75-85% | 90%+ |

## 11. 信息源索引

- NVIDIA STX 发布：[NVIDIA Launches BlueField-4 STX](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Launches-BlueField-4-STX-Storage-Architecture-With-Broad-Industry-Adoption/default.aspx)
- NVIDIA CMX 产品页：[NVIDIA CMX Context Memory Storage](https://www.nvidia.com/en-us/data-center/ai-storage/cmx/)
- NVIDIA CMX 技术博客：[BlueField-4-Powered CMX](https://developer.nvidia.com/blog/introducing-nvidia-bluefield-4-powered-inference-context-memory-storage-platform-for-the-next-frontier-of-ai/)
- NVIDIA Vera Rubin：[Vera Rubin Opens Agentic AI Frontier](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx)
- NVIDIA Dynamo：[Dynamo overall architecture](https://docs.dynamo.nvidia.com/dynamo/v-0-9-0/design-docs/overall-architecture)
- WEKA：[NeuralMesh for NVIDIA STX](https://www.weka.io/company/weka-newsroom/press-releases/neuralmesh-nvidia-stx/)
- VAST：[Context memory for agentic AI with BlueField-4](https://www.vastdata.com/press-releases/vast-data-brings-context-memory-to-agentic-ai-bluefield-4)
- DDN：[Rubin/BlueField-4 AI factory storage](https://www.ddn.com/press-releases/ddn-powers-integrated-compute-data-and-offload-at-scale-for-nvidia-rubin-platform/)
- Penguin Solutions：[MemoryAI 11TB CXL KV cache server](https://s204.q4cdn.com/917347554/files/doc_news/Penguin-Solutions-Introduces-Industrys-First-Production-Ready-CXL-Based-KV-Cache-Server-2026.pdf)
- Astera Labs：[Leo CXL on Azure M-series](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-leo-cxl-smart-memory-controllers-microsoft-azure-m)
- Micron CXL：[CXL memory products](https://www.micron.com/products/memory/cxl-memory)
- Samsung CMM-D：[IMDB white paper](https://download.semiconductor.samsung.com/resources/white-paper/Samsung_CMM-D_Utilization_in_IMDB_Applications.pdf)
- CXL Consortium：[CXL 4.0 and CXL overview](https://computeexpresslink.org/about-cxl/)
- CXL webinar：[Vertical Optimization of the CXL Stack](https://computeexpresslink.org/event/overcoming-cxl-limitations-enabling-cxl-hardware-and-software-as-vertical-optimization-technologies/)
- vLLM：[PagedAttention blog](https://vllm.ai/blog/vllm)
- vLLM KV offload：[KV Offloading Connector](https://vllm.ai/blog/kv-offloading-connector)
- LMCache：[GitHub](https://github.com/lmcache/lmcache)
- Mooncake：[paper](https://arxiv.org/abs/2407.00079)、[GitHub](https://github.com/kvcache-ai/Mooncake)
- KV Cache 综述：[KV Cache Optimization Strategies, 2026](https://arxiv.org/abs/2603.20397)
- HybridKV：[arXiv 2604.05887](https://arxiv.org/abs/2604.05887)
- TrendForce memory：[2Q26 memory pricing](https://www.trendforce.com/presscenter/news/20260331-12995.html)、[1Q26 memory pricing](https://www.trendforce.com/presscenter/news/20260105-12860.html)
- Gartner：[2026 semiconductor forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- IDC：[Enterprise Storage Systems Market Insights](https://www.idc.com/promo/enterprise-storage-systems/)
- Seagate：[Q3 FY2026 earnings transcript](https://s24.q4cdn.com/101481333/files/doc_financials/2026/q3/CORRECTED-TRANSCRIPT_-Seagate-Technology-Holdings-Plc-STX-US-Q3-2026-Earnings-Call-28-April-2026-5_00-PM-ET.pdf)
# 行业调研：【AI边缘推理芯片】

> 截至日期：2026-05-08  
> 研究对象：AI 边缘推理芯片，包括端侧 NPU/AI SoC、嵌入式 AI 加速器、车载/机器人 AI SoC、智能摄像头/工业视觉 SoC、AI PC/手机/可穿戴/网关中的本地推理芯片与模块。  
> 口径说明：下文的市场规模优先采用“可投资收入池”口径，即芯片、模组、板卡、车规域控/边缘盒子中可归因于本地 AI 推理的收入，不等同于整机 ASP，也不等同于纯 NPU die 面积价值。`B` = 十亿美元。  
> 情景定义：`基准`已经是偏乐观的 AI 基础设施持续扩张情形；`乐观`假设 2026-2027 云端算力、模型蒸馏、端侧代理应用顺利转化；`极度超预期乐观`假设数据中心上电、模型小型化、机器人/汽车量产节奏同时提前。  
> 重要提示：非投资建议。对缺失直接数据的部分，按用户要求采用大胆乐观假设，并在表格中显式标注为推演。

## 0. 高浓度结论

AI 边缘推理芯片不是“数据中心 AI 芯片的替代品”，而是 2026-2027 AI 计算中心大规模建设后的第二层放大器。Gartner 2026 年 4 月预测全球半导体收入将从 2025 年的约 $805B 跳升到 2026 年 $1.320T、2027 年 $1.555T，其中 AI 半导体约占 2026 年总收入 30%，且 hyperscaler AI 基建支出 2026 年增长超过 50%；这意味着云端训练、推理和内存供给仍是总盘的主轴，但也会把模型、工具链、低比特推理、端侧代理需求外溢到手机、PC、汽车、机器人和工业设备。[Gartner 2026 半导体预测](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)

Deloitte 对 2026 的判断更适合作为边缘推理芯片的“天花板校验”：推理会占 AI compute 的约三分之二，推理优化芯片市场超过 $50B，但大多数算力仍在价值 $200B+ 的高端数据中心芯片和 $400B+ 数据中心里完成。[Deloitte 2026 AI compute](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html) 因此，边缘 AI 最大的机会不在“把全部大模型搬到端侧”，而在四类高频任务：本地感知、多模态预处理、低延迟 agent action、隐私/离线场景，以及把云端大模型蒸馏成 0.5B-7B SLM/VLM 后在本地执行。

最值得关注的 2026 放量方向是：AI PC NPU、旗舰手机/平板端侧 NPU、智能驾驶/舱驾融合 SoC、Jetson Thor/IGX Thor 类物理 AI 模组、Hailo-10H/Axelera/SiMa/DEEPX 类离散边缘加速器、Ambarella/Rockchip/Axera/NXP/Renesas/ST 类视觉和工业 AI SoC。边缘 AI 芯片的窄口径纯芯片收入池 2026 年大约 $16B-$28B，广义可投资收入池约 $38B-$68B；到 2028 年，基准/乐观/极度超预期乐观情形分别可达 $70B-$115B / $110B-$180B / $170B-$280B。

投资价值最高的层不是最便宜的 NPU IP，而是“芯片 + 软件栈 + 行业认证 + 模型部署工具 + 客户长期设计定点”组合。NVIDIA Jetson/Isaac/CUDA、Qualcomm Hexagon/Dragonwing/Snapdragon Ride、Mobileye EyeQ/SuperVision/REM、Horizon Journey/HSD、Ambarella CVflow+ISP、Hailo 软件栈和车规认证，都比单纯 TOPS 更能解释定价能力。

## 1. 研究框架与锚点

### 1.1 需求锚点

| 锚点 | 关键事实 | 对边缘推理芯片的含义 |
|---|---|---|
| AI 数据中心大建设 | Gartner 预计 2026 AI 半导体约占全球半导体收入 30%，hyperscaler AI 基建支出增速超过 50%。 | 云端模型训练/蒸馏/推理服务能力提升，形成边缘模型供给；同时造成内存和先进封装紧张。 |
| 推理成为主战场 | Deloitte 预计 2026 推理占 AI compute 约 2/3，推理优化芯片超过 $50B。 | 边缘芯片会吃到“低延迟/低成本/隐私/离线”的一部分，但不会吞掉云端。 |
| PC/手机内存危机 | Gartner 2026 年 2 月称 PC 出货 -10.4%、手机 -8.4%，DRAM+SSD 价格到年底上涨约 130%，PC/手机价格分别上涨 17%/13%。[Gartner 设备预测](https://www.gartner.com/en/newsroom/press-releases/2026-02-26-gartner-says-surging-memory-costs-will-reduce-global-pc-and-smartphone-shipments-in-2026) | 单位出货承压，但 premium 化提升 AI SoC/NPU 附加值；低端设备被挤出，中高端 AI 设备份额提升。 |
| AI PC 进入多数出货 | Gartner 2025 年预测 AI PC 2026 年出货 1.431 亿台，占 PC 市场 54.7%。[Gartner AI PC](https://www.gartner.com/en/newsroom/press-releases/2025-08-28-gartner-says-artificial-intelligence-pcs-will-represent-31-percent-of-worldwide-pc-market-by-the-end-of-2025) | 40+ TOPS NPU 从卖点变成入场券；真正的利润取决于企业端本地模型和软件生态。 |
| AI 手机高端化 | IDC 在 MWC 2026 观察到 AI 设备从概念进入执行期，并提示 2026 智能手机约 -13%、PC 约 -11% 的内存约束。[IDC MWC 2026](https://www.idc.com/resource-center/blog/intelligent-devices-mwc-2026/) | 旗舰 AI 手机短期 ASP 强，但中低端升级推迟；NPU 单位价值上升，数量不一定同步上升。 |
| 边缘 AI 长期 TAM | ResearchAndMarkets 2026 报告预计 edge AI chips 到 2036 年超过 $80B，核心应用为汽车、AI 手机、AI PC、人形机器人、预测维护传感器。[Edge AI Chips 2026-2036](https://www.researchandmarkets.com/reports/6225879/edge-ai-chips-technologies-markets-forecasts) | 2030 前最强弹性来自车载/机器人/工业视觉，手机和 PC 提供数量底盘。 |

### 1.2 项目内 AI 芯片路线图锚点

项目内已有《全球 AI 芯片路线图与 2026-2027 产能释放预测》，其对 2026-2027 出货/价值权重最高的平台排序为：NVIDIA GB300/B300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA GB200/B200、Huawei Ascend 910C/950、Cambricon 590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200、Alibaba Zhenwu、AMD MI400/MI455X。边缘推理行业受到这些平台的三类外溢：

1. **低比特推理范式下沉**：Blackwell/Rubin、Trainium3、TPU、Maia 200 对 FP4/FP8/INT4、稀疏、KV cache、长上下文做了硬件化优化，2026 先在数据中心验证，2027 下沉到高端 PC、机器人、车载域控和边缘盒子。
2. **模型蒸馏供应链形成**：云端大模型训练能力越强，端侧可用的 0.5B-7B 小模型、VLM、VLA、语音/视觉 agent 越多，边缘芯片需求不是来自“裸 TOPS”，而是来自模型生态。
3. **供应链挤压传导**：HBM/CoWoS 被数据中心占用后，LPDDR、DRAM、SSD、ABF、先进节点也被挤压，边缘芯片会出现“高端有溢价、低端被延后”的分化。

## 2. 2026 的行业机遇、挑战与正在使用的技术

### 2.1 机遇

| 机遇 | 2026 触发因素 | 受益产品 |
|---|---|---|
| 云端推理成本高企，端侧承担“首轮过滤” | 多模态 token、视频流、agent action 增长导致云端推理账单上升。 | 智能摄像头 SoC、工业视觉盒子、AI PC NPU、手机 NPU、边缘网关。 |
| 隐私与离线需求强化 | 金融、医疗、工厂、安防、车载不愿把原始数据上传。 | Hailo-10H、Ambarella CVflow、NVIDIA IGX/Jetson、Qualcomm Dragonwing、NXP/Renesas/ST。 |
| 物理 AI 从演示进入生产 | NVIDIA GTC 2026 把 ABB、Agility、FANUC、Figure、KUKA、Medtronic、Universal Robots、Yaskawa 等列入机器人生态；IGX Thor/Jetson Thor 已 GA。[NVIDIA robotics GTC 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Global-Robotics-Leaders-Take-Physical-AI-to-the-Real-World/) | Jetson Thor、IGX Thor、Qualcomm Dragonwing IQ/Q 系列、SiMa Modalix、DEEPX DX-M、Axelera Europa。 |
| 车载智能化从 L2 向 L2++/L3 | Mobileye EyeQ6H 拿到美国头部车企未来量产项目；Horizon Journey 6 出货和 ASP 继续提升；Qualcomm Ride Flex/Cockpit Elite 获更多设计定点。 | Mobileye EyeQ6H、Qualcomm Ride Flex、NVIDIA DRIVE Thor、Horizon Journey 6、Black Sesame C1296/A2000、Tesla AI4/AI5。 |
| AI PC 和旗舰手机“硬件先行” | Gartner 预测 AI PC 2026 占 PC 市场 54.7%，Qualcomm X2/AMD Ryzen AI/Intel Core Ultra/Apple M 系列持续提高 NPU。 | PC/手机 SoC、LPDDR、封装、端侧模型软件。 |

### 2.2 挑战

1. **真实应用滞后于硬件渗透**：AI PC 已经有 40-80 TOPS NPU，但 2026 上半年多数消费者仍不为 NPU 单独买单，企业侧 ROI 依赖本地 Copilot、RAG、安全策略和 ISV 适配。
2. **内存比 TOPS 更稀缺**：端侧 LLM/VLM 受 LPDDR 容量、带宽和成本限制；Gartner 的“memflation”会让低端设备退场，高端设备更贵。
3. **软件栈壁垒高**：边缘 AI 芯片要支持 PyTorch/ONNX/TensorRT/OpenVINO/TVM/TFLite、量化、算子覆盖、视频管线、驱动长期维护；没有模型部署工具的芯片很难放量。
4. **车规/工业认证周期长**：AEC-Q100、ASIL、ISO 26262、IEC 61508、医疗设备认证会把从 design-in 到收入确认拉长 18-48 个月。
5. **客户锁定强但试错成本高**：一旦进入车厂、安防 OEM、工业机器人平台，生命周期长；反过来，没进入 AVL/RVL 的供应商很难靠降价切入。
6. **数据中心供应链虹吸**：TSMC N3/N4/N2、先进封装、ABF、LPDDR/HBM、EDA/掩膜、测试设备被 AI 服务器抢占，边缘高端芯片会被迫排产。

### 2.3 正在使用的主流技术

| 技术 | 2026 状态 | 用在什么产品 | 投资含义 |
|---|---|---|---|
| INT8/INT4 NPU | 成熟放量 | 手机、PC、智能摄像头、边缘盒子、Hailo/DEEPX/RK3588/Axera | 2026 最大出货基座，价格竞争也最强。 |
| FP16/BF16/FP8/FP4 混合精度 | 数据中心成熟，边缘高端导入 | Jetson Thor、RTX PRO、AI PC、未来机器人 SoC | 支撑本地 SLM/VLM/VLA，2027 开始成高端边缘标配。 |
| 低比特模型与量化 | 快速成熟 | Hailo-10H 2B 模型、MediaTek BitNet、手机/PC SLM | 软件工具链价值上升，硬件 TOPS 口径需要看精度。 |
| Transformer/VLM/VLA 加速 | 2026 高端导入 | Jetson Thor、Ambarella CVflow 3.0、Qualcomm Q-8750、NVIDIA DRIVE Thor | 机器人/工业/车载从 CNN 视觉走向“理解+行动”。 |
| 片上 SRAM/近存计算 | 2026 小规模放量 | Axelera Europa 128MB L2 SRAM、Hailo 数据流架构、Ambarella CVflow | 能绕开外部内存瓶颈，适合稳定视觉/小模型。 |
| LPDDR5X/LPDDR6、大内存统一架构 | 2026-2027 快速提升 | PC、手机、Jetson、机器人 | 模型参数量和上下文长度的真实上限由内存决定。 |
| 数字/模拟 compute-in-memory | 2026 试点，2027-2028 才可能规模化 | Axelera 数字 in-memory、学术/初创 CIM | 极度乐观情形下 2027 开始在低功耗视觉/SLM 加速出现批量订单。 |
| 车规安全岛与混合关键性 | 2026 放量 | Qualcomm Ride Flex、NXP S32N、Mobileye EyeQ6H、Black Sesame C1296 | 能把座舱、ADAS、车身/网关整合，定价不只按 TOPS。 |

## 3. 技术成熟与放量时间：三情景预测

| 技术/路径 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观成熟/放量 | 2026 最可能性 |
|---|---|---|---|---|
| AI PC 40-80 TOPS NPU | 2026 成熟，2027 企业批量软件落地 | 2026 H2 企业采购恢复，2027 本地 SLM/RAG 成标配 | 2026 H2 agent OS/企业安全模型拉动换机 | 高 |
| 旗舰手机端侧 GenAI NPU | 2026 高端标配，2027 渗透中端 | 2026 H2 premium 市占提升抵消总量下滑 | 2027 AI agent 成换机主因，NPU ASP 上行 | 高 |
| Jetson Thor/IGX Thor 物理 AI | 2026 GA/NPI，2027 工业机器人和医疗设备放量 | 2026 H2 机器人客户提前锁单 | 2027 人形/物流机器人年出货进入十万级，模组供不应求 | 中高 |
| Hailo-10H/离散 GenAI edge accelerator | 2026 开始 USB/PCIe/SoM 放量，2027 进入车载/工业 | 2026 H2 ASUS/Raspberry Pi/工控机渠道放大 | 2027 成为低功耗本地 LLM/VLM 默认外挂 | 中高 |
| 车载 L2++/L3 AI SoC | 2026 定点/量产爬坡，2027 明显放量 | 2026 中国 NOA 和美国高速 hands-free 提前量产 | 2027 L3 法规和保险配套突破，域控 ASP 大幅上行 | 高 |
| 智能摄像头/工业视觉 SoC | 2026 AI-ISP+VLM 导入，2027 新品换代 | 2026 安防/零售/工厂以“边缘 VLM”升级 | 2027 视频语义搜索成为摄像头默认功能 | 高 |
| TinyML/MCU NPU/in-sensor AI | 2026 低价放量，价值量小 | 2027 传感器预处理和预测维护加速 | 2027 电池设备/可穿戴大规模用本地小模型 | 中 |
| Compute-in-memory/类脑/事件视觉 | 2026 试点，2028 主流前夜 | 2027 部分工业视觉/低功耗传感器量产 | 2027 低功耗机器人感知切入主流 | 低到中 |
| 2nm/3nm 高端机器人/车载 SoC | 2027 样片/高端量产 | 2027 H2 高端 Robotaxi/人形机器人上量 | 2027 大客户提前锁 2nm 产能，单芯片 700-1000 TOPS 下沉 | 中 |

**2026 最可能的技术路径**：INT8/INT4 NPU + LPDDR5X/5 + CNN/VLM 混合视觉 + 轻量 SLM/VLM + 完整 SDK。真正的主流不是“端侧跑 70B 大模型”，而是“云端大模型规划/蒸馏，本地 1B-7B 模型执行感知、检索、摘要、控制和隐私过滤”。

## 4. 已开始放量的关键产品：市场规模、渗透率、增长与利润率

### 4.1 总体收入池预测

| 口径 | 未来 3 个月：2026Q2-Q3 | 未来 1 年：至 2027-05 | 未来 2 年：至 2028-05 |
|---|---:|---:|---:|
| 窄口径：纯边缘 AI 加速芯片/IP/模组 | 基准 $4-7B；乐观 $6-10B；极度 $9-15B | 基准 $18-30B；乐观 $28-45B；极度 $42-70B | 基准 $32-55B；乐观 $55-90B；极度 $85-140B |
| 广义可投资口径：AI SoC、车载域控、边缘盒子、模组中可归因 AI 的收入 | 基准 $10-17B；乐观 $15-25B；极度 $22-38B | 基准 $45-75B；乐观 $70-115B；极度 $105-170B | 基准 $70-115B；乐观 $110-180B；极度 $170-280B |
| 端侧设备渗透率：AI PC/AI 手机/智能车/工业视觉综合 | 基准 15-22%；乐观 20-30%；极度 28-40% | 基准 25-35%；乐观 35-48%；极度 45-60% | 基准 38-52%；乐观 52-68%；极度 65-80% |

### 4.2 已放量产品分拆

| 细分产品 | 代表产品/公司 | 已验证事实 | 市场规模区间：3个月 / 1年 / 2年 | 渗透率路径 | 增长预测 | 毛利率/利润率推演 |
|---|---|---|---|---|---|---|
| AI PC NPU/APU | Qualcomm Snapdragon X2/X Elite、AMD Ryzen AI 300/400、Intel Core Ultra、Apple M 系列 | Gartner 预测 AI PC 2026 1.431 亿台、占 PC 54.7%；Qualcomm X2 平台最高 80-85 TOPS；AMD 2026 CES 发布 Ryzen AI 400/PRO 400，最高 60 NPU TOPS。[Qualcomm X2](https://www.qualcomm.com/news/onq/2026/01/accelerating-the-future-of-desktop-pcs-snapdragon-x-series)、[AMD CES 2026](https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-expands-ai-leadership-across-client-graphics-.html) | B $2.0-3.5 / $8-14 / $14-25；O $3-5 / $12-22 / $22-38；X $4.5-8 / $18-32 / $35-60 | 2026 AI PC 50%+，但 Copilot+ / 40+ TOPS 实用渗透约 25-35%；2028 可达 60-75%。 | 单位出货受内存拖累，但 AI SoC ASP +10-25%；2027 企业更新周期恢复。 | SoC 厂商毛利 B 45-55%，O 50-60%，X 55-65%；高端平台因内存紧张具备价格传导。 |
| 旗舰手机/平板 AI SoC | Qualcomm Snapdragon 8 Elite Gen 5、MediaTek Dimensity 9500/9500s、Apple A/M、Samsung Exynos、Huawei Kirin | Gartner/IDC 均提示 2026 手机总量下滑；但 IDC 称 MWC 2026 智能设备进入执行期，AI 手机成为 premium 战场。MediaTek Dimensity 9500s 明确面向端侧多模态/生成式推理。[MediaTek 9500s](https://www.mediatek.com/press-room/mediatek-unveils-dimensity-9500s-and-dimensity-8500-to-propel-performance-gaming-and-efficiency-in-flagship-and-premium-smartphones) | B $3-6 / $13-23 / $20-35；O $5-8 / $20-35 / $35-60；X $7-12 / $30-50 / $55-90 | GenAI 手机 2026 约 35-45% 出货，高端机 70%+；2028 可达 55-65% 总出货。 | 内存涨价压低低端机，旗舰 AI SoC ASP 上行；2027 端侧 agent 若成功，换机弹性提升。 | 高端移动 SoC 毛利 B 45-58%，O 52-62%，X 58-68%；中端 SoC 25-40%。 |
| NVIDIA Jetson/IGX/RTX PRO 边缘平台 | Jetson Thor T5000/T4000、IGX Thor、RTX PRO 4500/6000 Blackwell | Jetson Thor 最高 2070 FP4 TFLOPS、128GB 内存、40-130W，T5000/开发套件已 GA；IGX Thor 已 GA；TrendForce 称 NVIDIA 中低端/边缘产品 2026 占总出货可超 32%。[Jetson Thor](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/)、[IGX Thor](https://www.nvidia.com/en-us/edge-computing/products/igx/)、[TrendForce](https://www.trendforce.com/presscenter/news/20260408-13003.html) | B $1.5-2.8 / $6-11 / $11-22；O $2.3-4.0 / $9-18 / $18-35；X $3.5-6.0 / $15-28 / $30-60 | 高端机器人/工业边缘 2026 渗透 5-10%，2028 15-30%；GPU 边缘工作站渗透更高。 | 2026 H2 Thor 供给爬坡，2027 机器人/医疗/工业定点转收入。 | NVIDIA 模组/板卡毛利 B 50-65%，O 60-70%，X 65-75%；软件生态带来溢价。 |
| 离散低功耗 AI 加速器 | Hailo-8/10H、Axelera Europa/Metis、SiMa Modalix、DEEPX DX-M1、Kneron、Blaize | Hailo-10H 2025 年 7 月 GA，40 TOPS INT4、典型 2.5W、AEC-Q100 Grade 2，目标 2026 SOP；Axelera Europa H1 2026 开始出货，128MB L2 SRAM、200GB/s；SiMa Modalix SoM 获 Edge AI + Vision Alliance 2026 产品奖。[Hailo-10H](https://hailo.ai/company-overview/newsroom/news/hailo-announces-general-availability-of-hailo-10h-edge-ai-accelerator-with-generative-ai-capabilities/)、[Axelera Europa](https://axelera.ai/news/axelera-announces-europa-aipu-setting-new-industry-benchmark-for-ai-accelerator-performance-power-efficiency-and-affordability)、[SiMa 2026](https://sima.ai/press-release/sima-ai-wins-edge-ai-vision-alliance-2026-product-of-the-year-for-modalix-som/) | B $0.6-1.2 / $2.5-5 / $6-12；O $1-2 / $4-8 / $10-22；X $1.8-3.5 / $7-14 / $18-40 | 低功耗边缘盒子/摄像头/工控 2026 3-7%，2028 10-25%。 | 从视觉 AI 扩展到 VLM/SLM；渠道从开发板转向 OEM 设计定点。 | 芯片毛利 B 45-60%，O 55-68%，X 65-78%；模组毛利较低 25-45%，软件/SDK 服务毛利更高。 |
| 车载 ADAS/舱驾融合 AI SoC | Mobileye EyeQ6H、Qualcomm Ride Flex/Cockpit Elite、NVIDIA DRIVE Thor、Horizon Journey 6、Black Sesame C1296/A2000、Tesla AI4/AI5 | Mobileye 2026Q1 EyeQ/SuperVision 收入 $535M，全年收入指引 $1.935-2.015B，累计 2.3 亿辆车搭载 EyeQ；Qualcomm CES 2026 称 Ride Flex 设计赢单扩大；Horizon 2025 Journey 硬件出货 401 万套，收入 +57.7%。[Mobileye Q1 2026](https://ir.mobileye.com/news-releases/news-release-details/mobileye-releases-first-quarter-2026-results-updates-full-year)、[Qualcomm Automotive 2026](https://www.qualcomm.com/news/releases/2026/01/qualcomm-drives-the-future-of-mobility-with-strong-snapdragon-di)、[Horizon 2025](https://stockanalysis.com/quote/hkg/9660/transcripts/) | B $3.5-6 / $15-26 / $28-50；O $5-8 / $23-38 / $45-80；X $7-12 / $35-60 / $75-130 | L2/L2+ 主流车 2026 35-45%，高阶 NOA/L3 5-12%；2028 高阶可达 15-30%。 | 中国 NOA、欧美高速 hands-free、Robotaxi 重新加速；舱驾融合提升单车价值。 | 车规芯片/方案毛利 B 45-65%，O 55-70%，X 65-78%；系统方案/软件栈可超过芯片毛利。 |
| 智能摄像头/工业视觉 SoC | Ambarella CV7/N1、Rockchip RK3588/RK3576、Axera M 系列、Sophgo、SigmaStar、Novatek、Renesas RZ/V2H、NXP i.MX95 | Ambarella 2026 CES 发布 4nm CV7，称累计边缘 AI SoC 出货超 3900 万；Renesas RZ/V2H 8 dense TOPS/80 sparse TOPS；NXP i.MX95 面向汽车/工业视觉，2026 文档持续更新。[Ambarella CV7](https://www.ambarella.com/news/ambarella-launches-powerful-edge-ai-8k-vision-soc-with-industry-leading-ai-and-multi-sensor-perception-performance/)、[Renesas RZ/V2H](https://www.renesas.com/en/products/rz-v2h)、[NXP i.MX95](https://www.nxp.com/products/i.MX95) | B $1.8-3 / $7-12 / $12-22；O $2.5-4.5 / $11-18 / $20-35；X $4-7 / $17-30 / $32-60 | AI 摄像头 2026 20-35%，工业视觉 10-20%；2028 分别 45-65% / 25-40%。 | VLM 视频语义搜索、工厂质检、城市安防升级；中国供应链成本优势强。 | 高端视觉 SoC 毛利 B 45-60%，O 55-68%，X 60-75%；低端通用 AIoT SoC 20-40%。 |
| MCU/TinyML/in-sensor AI | ST STM32N6、NXP i.MX93W、Sony IMX500、Himax WiseEye、Ambiq、Renesas RA/RZ 边缘系列 | STM32N6 内置 Neural-ART NPU，最高 600 GOPS；Sony IMX500 是带 AI 处理的堆叠图像传感器；2026 学术测试显示 STM32N6、GAP9、Sony IMX500 代表超低功耗路线。[STM32N6](https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html)、[Sony IMX500](https://developer.sony.com/imx500/)、[Edge/in-sensor AI review](https://arxiv.org/abs/2603.08725) | B $0.3-0.7 / $1.3-2.5 / $3-6；O $0.5-1.0 / $2-4 / $5-10；X $0.8-1.6 / $3.5-7 / $9-18 | 2026 在传感器/MCU 中低个位数，2028 可达 10-20%。 | 价值量小但数量巨大；预测维护、低功耗唤醒、隐私传感器是主线。 | MCU 毛利 B 35-50%，O 45-58%，X 55-65%；传感器+算法绑定更高。 |
| 边缘私有推理服务器/盒子 | NVIDIA RTX PRO/IGX、Blaize、Axelera PCIe、Hailo PCIe/USB、Qualcomm Dragonwing AI On-Prem Appliance、Supermicro edge servers | Qualcomm Q2 FY2026 称 Automotive+IoT 同比 +20%，并称 hyperscaler 定制数据中心硅片 2026 年晚些时候开始初始出货；Blaize 2026 预告多城市边缘推理部署收入。[Qualcomm Q2 FY26](https://www.qualcomm.com/news/releases/2026/04/qualcomm-announces-second-quarter-fiscal-2026-results)、[Blaize 2026 update](https://ir.blaize.com/node/8201/pdf) | B $1.0-1.8 / $4-8 / $9-18；O $1.5-2.8 / $7-13 / $15-30；X $2.5-5 / $12-24 / $28-60 | 企业/园区边缘 2026 3-8%，2028 12-25%。 | 数据不出园区、云端 token 成本、主权/军工/零售视频分析驱动。 | 板卡/系统毛利 B 25-45%，O 35-55%，X 45-65%；软件订阅可 70%+。 |

## 5. 在研关键产品和细分技术

| 在研方向 | 代表公司/产品 | 预计成熟与放量 | 市场规模：3个月 / 1年 / 2年 | 渗透率路径 | 利润率推演 |
|---|---|---|---|---|---|
| 700-1000 TOPS 级机器人/车载中央计算 SoC | Qualcomm Dragonwing IQ10、NVIDIA DRIVE/Jetson Thor 后续、Black Sesame A2000、Tesla AI5、Horizon Journey 后续 | 2026 样机/定点，2027 高端车型和机器人批量 | B $0.2-0.6 / $1.5-4 / $8-18；O $0.5-1.2 / $3-8 / $15-35；X $1-2.5 / $7-18 / $35-80 | 高端机器人/Robotaxi 2026 <3%，2028 10-20% | 芯片 55-70%，整套域控 25-45%，软件/安全栈 65-85%。 |
| 2nm/3nm GenAI 边缘加速器 | DEEPX DX-M2、下一代 Hailo/Axelera/SiMa、Qualcomm Q 系列后续 | 2026 tape-out/验证，2027 初步量产 | B $0.1-0.4 / $0.8-2 / $4-10；O $0.2-0.8 / $1.5-4 / $8-20；X $0.5-1.5 / $4-10 / $18-45 | 边缘盒子/机器人 2027 开始 5-10% | 高壁垒早期 60-75%，量产后普通卡 35-50%。 |
| VLM/VLA 专用边缘推理 | Ambarella CVflow 3.0、NVIDIA Isaac/GR00T、Qualcomm robotics、Hailo-10H、EdgeCIM | 2026 高端视觉/机器人验证，2027 工业/安防放量 | B $0.4-1 / $2-5 / $8-16；O $0.8-1.8 / $4-9 / $15-30；X $1.5-3 / $8-18 / $30-65 | 视频设备 2026 2-5%，2028 15-30% | 芯片 50-65%，行业算法/模型 70-90%。 |
| 数字/模拟 compute-in-memory | Axelera digital in-memory、EdgeCortix、Mythic 路线、学术 EdgeCIM | 2026 小批量，2027 低功耗视觉/SLM 试放量 | B <$0.1 / $0.3-1 / $2-6；O $0.1-0.3 / $0.8-2 / $5-12；X $0.2-0.8 / $2-5 / $12-30 | 2028 前仍 <10%，极度乐观 15% | 若能绕开 DRAM，早期毛利 65-80%；良率/工具链不足则迅速压缩。 |
| AI 传感器/in-sensor processing | Sony IMX500 后续、Himax WiseEye、Prophesee 事件视觉、ST/OmniVision 传感器 AI | 2026 传感器级场景试点，2027 可穿戴/安防/工业规模化 | B $0.1-0.4 / $0.5-1.5 / $2-5；O $0.2-0.6 / $1-3 / $4-10；X $0.4-1 / $2-6 / $9-20 | 摄像头传感器 2026 <5%，2028 10-25% | 传感器毛利 35-55%，AI sensor+算法 55-70%。 |
| 端侧 agent OS 和模型部署工具链 | Apple Intelligence、Windows Copilot+、Qualcomm AI Hub、Intel OpenVINO、AMD Ryzen AI Software、NVIDIA NIM/Jetson、Hailo SDK | 2026 硬件先行，2027 决定换机价值 | B $0.5-1.5 / $3-8 / $10-25；O $1-3 / $6-15 / $20-45；X $2-5 / $12-30 / $40-90 | AI PC/手机/工业设备 2027 后成为默认层 | 软件毛利 70-90%，生态锁定最强。 |

## 6. 供给侧：产能结构、瓶颈、成本与价格传导

### 6.1 产能结构

| 层级 | 主要地区/公司 | 工艺/能力 | 对边缘 AI 的影响 |
|---|---|---|---|
| 先进逻辑代工 | TSMC 台湾/美国、Samsung Foundry 韩国/美国、Intel Foundry 美国/欧洲、SMIC 中国 | 2nm/3nm/4nm/5nm/7nm，N3/N4 是高端 PC/手机/机器人/车载核心 | 高端边缘 SoC 与数据中心 GPU/ASIC 争先进节点。 |
| 成熟/特色逻辑 | UMC、GlobalFoundries、SMIC、Tower、TSMC mature、华虹等 | 12/16/22/28/40/55nm，车规 MCU、ISP、传感器、低端 AIoT | 供给相对充足，但车规良率和长生命周期要求高。 |
| 封装测试 | ASE、Amkor、JCET、SPIL、Powertech、Tongfu、TSMC backend | PoP、FCBGA、SiP、fan-out、2.5D、车规测试 | PC/手机/边缘模组受 LPDDR PoP、BGA、SiP 和测试产能制约。 |
| 内存 | SK hynix、Samsung、Micron、长鑫/长存等 | LPDDR5X/LPDDR6、DDR5、GDDR、HBM、NAND | 2026 最大矛盾是 AI 数据中心挤占内存，边缘设备被迫涨价。 |
| 板卡/模组 | Advantech、ADLINK、Aaeon、ASUS、Raspberry Pi、Supermicro、Foxconn、BYD Electronics、车规 Tier1 | SoM、MXM、PCIe、USB accelerator、域控、工业盒子 | 模组厂把芯片能力变成可交付产品，毛利较芯片低但订单确定性更强。 |
| 软件/工具 | NVIDIA CUDA/TensorRT/Jetson/Isaac、Qualcomm AI Hub、Intel OpenVINO、AMD ROCm/Ryzen AI、Hailo Dataflow、Ambarella CVflow、Arm Ethos、Synopsys/Cadence/CEVA IP | 编译器、量化、模型 zoo、视频管线、安全认证 | 直接决定芯片能否定价；TOPS 不是护城河，工具链才是。 |

### 6.2 供给瓶颈

1. **先进节点排产**：N3/N4/N2 被手机旗舰、AI PC、数据中心 GPU/ASIC、车载高端域控共同争抢。
2. **内存容量与价格**：LPDDR/DDR/SSD 被 HBM 和 AI 服务器挤压，Gartner 预计 2026 DRAM+SSD 价格上涨约 130%，直接推高 AI PC/手机 BOM。
3. **封装与 ABF/高阶 PCB**：高端边缘 SoC 需要大封装、PoP、SiP 或 FCBGA；机器人/车载域控需要高可靠 PCB、连接器和热设计。
4. **车规认证和功能安全**：AEC-Q100、ASIL D、ISO 26262 认证周期长；同一芯片消费级量产不等于车规可交付。
5. **软件算子覆盖**：Transformer、attention、KV cache、VLM/VLA、动态 shape 支持不足会导致标称 TOPS 无法转化成真实吞吐。
6. **视频/传感器管线**：边缘 AI 多数入口是 camera/radar/audio，ISP、encoder、sensor sync、time stamping 比纯矩阵乘更难。
7. **热设计与电源瞬态**：Jetson Thor 40-130W、车载域控数百瓦、机器人多传感器融合，都需要电源模块、散热和可靠性设计。
8. **人才瓶颈**：编译器、量化、内核优化、车规安全、机器人 VLA 部署人才稀缺。
9. **客户认证/渠道**：安防、工业、车厂设计周期长，客户一旦锁定平台不会轻易换供应商。
10. **出口管制与本地替代**：中国市场会加速 Horizon、Black Sesame、Axera、Rockchip、Sophgo、Huawei 等本土方案，但高端制程/EDA/IP 仍受限。

### 6.3 成本构成与毛利决定因素

| 产品 | 成本拆分推演 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| AI PC/手机 SoC | 晶圆 35-50%；IP/掩膜/NRE 摊销 10-20%；封测/PoP 8-15%；内存相关系统成本 20-35%。 | NPU 性能、CPU/GPU/ISP/基带综合能力、OEM 份额、台积电/三星先进节点成本。 | 高端机型可以把内存和 AI SoC 涨价传给消费者；低端机被延后或砍配置。 |
| Jetson/边缘模组 | SoC 25-40%；LPDDR/NAND 20-35%；板卡/电源/散热 15-25%；软件/支持/渠道 10-20%。 | CUDA/Isaac/Metropolis/NIM 生态、供货稳定性、开发者基数。 | 机器人/医疗/工业客户愿意为软件稳定和长期供货付溢价。 |
| 离散 AI accelerator | Die+封装 35-50%；外部内存 10-30%；板卡 15-25%；软件/FAE 10-25%。 | 每瓦性能、模型适配、SDK 易用性、车规/工业认证。 | 早期供不应求和设计定点可维持高价；通用视觉卡会被中国/台湾模组压价。 |
| 车载 AI SoC/域控 | SoC 20-35%；内存/存储 10-25%；PCB/电源/散热/连接器 15-30%；安全/测试/质保 10-20%；软件 10-30%。 | ASIL、功能安全、驾驶软件、车厂定点数量、Tier1 集成能力。 | 单车价值从芯片 ASP 转向域控+软件授权；L3/Robotaxi 溢价最高。 |
| 智能视觉 SoC | 晶圆 30-45%；ISP/AI IP 摊销 10-20%；封测 10-15%；软件/算法 10-25%；渠道 5-15%。 | ISP 画质、低功耗、视频编解码、多路输入、VLM 支持。 | 安防/工业客户以系统成本采购，能降低云带宽和人工审核即可涨价。 |
| MCU/TinyML/in-sensor | 成熟工艺晶圆 25-40%；封测 15-25%；传感器/模拟 20-40%；软件 5-15%。 | 超低功耗、长期供货、传感器集成、开发生态。 | 单价低、数量大，价格弹性有限；高端传感器 AI 可通过隐私和低功耗定价。 |

## 7. 竞争格局与壁垒

### 7.1 市场结构

| 子市场 | 2026 头部集中度推演 | 主要玩家 | 判断 |
|---|---|---|---|
| AI PC NPU/SoC | CR4 85-95% | Intel、AMD、Qualcomm、Apple | x86/Arm 生态决定份额，NPU 单点竞争次于平台生态。 |
| 手机 AI SoC | CR5 80-90% | Qualcomm、MediaTek、Apple、Samsung、Huawei/HiSilicon | 基带、ISP、功耗和 OEM 关系强锁定。 |
| 高端机器人/工业边缘 GPU/SoM | NVIDIA 50-70% 价值份额 | NVIDIA、Qualcomm、AMD/Xilinx、Intel、Advantech/ADLINK 生态 | CUDA/Isaac/开发者生态是核心壁垒。 |
| 离散边缘 AI accelerator | CR5 45-65%，仍分散 | Hailo、Axelera、SiMa、DEEPX、Blaize、Kneron、MemryX、EdgeCortix | 2026 仍是百花齐放，2027 会按软件和渠道出清。 |
| 车载 ADAS/中央计算 | CR5 70-85% | Mobileye、Qualcomm、NVIDIA、Horizon、Black Sesame、Tesla、Huawei | 车规认证、软件安全、车厂定点是定价基础。 |
| 智能摄像头/AIoT SoC | CR10 50-70%，中国供应链强 | Ambarella、Rockchip、Axera、SigmaStar、Novatek、Sophgo、Realtek、NXP、Renesas、ST | 成本、ISP、渠道和算法适配决定胜负。 |

### 7.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 为什么能定价 |
|---|---|---|
| PPA：性能/功耗/面积 | 边缘设备受电池、热、尺寸和噪声限制，TOPS/W 比绝对 TOPS 更重要。 | 省掉风扇、散热、云带宽和电池容量，客户愿意多付芯片钱。 |
| 编译器和模型工具链 | 同一模型在不同 NPU 上性能差异可能数倍；算子不支持会直接无法部署。 | 开发时间就是成本，成熟 SDK 能降低客户工程风险。 |
| 视频/传感器融合 | 摄像头、雷达、IMU、音频输入需要低延迟同步和 ISP/codec。 | 端到端 pipeline 能减少外挂芯片和系统复杂度。 |
| 认证标准 | AEC-Q100、ASIL、医疗/工业认证周期长。 | 认证通过后进入长期供货名单，客户切换成本高。 |
| 客户设计定点 | 车厂、安防 OEM、工业设备生命周期 3-10 年。 | 定点后价格不完全市场化，供应稳定比最低价更重要。 |
| 软件生态和开发者基数 | CUDA、TensorRT、OpenVINO、Qualcomm AI Hub、Hailo SDK、Ambarella CVflow 等影响应用迁移。 | 生态越大，客户越不愿换平台，形成事实标准。 |
| 供应保障 | 2026 内存/先进节点紧张，能交付就是竞争力。 | 供不应求阶段可拿交期溢价和预付款。 |

### 7.3 价值捕获判断

长期 ROIC/毛利最高的层级排序：

1. **平台软件和工具链**：CUDA/Isaac、Mobileye SuperVision/REM、Horizon HSD、Ambarella CVflow、Hailo Dataflow、Qualcomm AI Hub。边缘 AI 的痛点是部署，而不是买芯片。
2. **车规/工业高可靠 SoC 与系统方案**：生命周期长、认证锁定、单车/单机价值高。
3. **高端机器人/物理 AI 模组**：Jetson/IGX/Dragonwing/SiMa/Axelera，如果进入机器人 OEM 平台，放量弹性高。
4. **视觉 AI SoC + ISP**：画质和低功耗是长期壁垒，尤其安防/工业。
5. **通用低端 NPU/IP**：数量大但易被集成和替代，长期毛利会下行。

## 8. 2026 关键变化：最可能发生的 3 个拐点

1. **AI PC/手机从“AI 标签”进入“premium 标配”，但总量被内存压制**  
   2026 是端侧 NPU 渗透的硬件拐点，不一定是消费需求拐点。内存涨价让低端设备退场，反而提高高端 AI SoC 的收入占比。投资上应关注高端 SoC、LPDDR、封测、端侧模型工具，而不是只看 PC/手机总出货。

2. **物理 AI 进入 NPI 到小批量生产阶段**  
   NVIDIA Jetson Thor/IGX Thor GA、Qualcomm Dragonwing 扩张、SiMa 2026 产品奖、Hailo-10H 车规 SOP 指向 2026 H2-2027 的机器人/工业边缘订单。短期金额不如手机/PC，但弹性最大。

3. **智能驾驶和舱驾融合重新成为边缘 AI 最大高 ASP 场景**  
   Mobileye 2026Q1 收入和 EyeQ 累计装车、Horizon Journey 6 出货、Qualcomm Ride Flex 设计赢单、Black Sesame A2000/C1296 和 NVIDIA DRIVE Thor 说明车载 AI 仍是边缘推理最强的确定性场景。

## 9. 2027 关键变化：最可能发生的 3 个拐点

1. **L2++/L3 和舱驾融合从中国扩散到全球平台**  
   2027 将是 EyeQ6H、Journey 6、Ride Flex、DRIVE Thor、Black Sesame A2000、Tesla AI5 等项目从设计定点转量产的关键年份。若法规和责任边界更清晰，单车 AI 计算价值会从几十美元跨到数百美元。

2. **端侧小模型从“demo”变成 OS/应用层常驻能力**  
   2026 是硬件铺底；2027 如果 Windows、Android、iOS、车机、工业网关都能用本地 SLM/VLM 执行摘要、语音、视觉问答、RAG、设备控制，NPU 利用率和客户付费意愿会显著提升。

3. **边缘 AI 芯片行业开始出清**  
   2026 仍有大量 TOPS 型初创公司；2027 客户会按软件、供货、认证、总系统成本淘汰玩家。能进入车规/工业/安防大客户的公司估值上行，纯开发板销量和单芯片样片会被市场压价。

## 10. 头部公司与细分技术公司清单

### 10.1 AI PC、手机、消费端 SoC

| 公司 | 技术优势/产品 |
|---|---|
| Apple | A/M 系列 Neural Engine、统一内存、端侧 Apple Intelligence 生态；高端硬件闭环强。 |
| Qualcomm | Snapdragon 8/X/Dragonwing，Hexagon NPU、基带、ISP、连接、AI Hub；手机、PC、IoT、汽车横向覆盖。 |
| MediaTek | Dimensity 9500/9500s、NPU 990、端侧生成式/多模态推理；安卓旗舰与中高端量大。 |
| AMD | Ryzen AI 300/400、XDNA NPU、Ryzen AI Embedded P/X；PC 和嵌入式扩张。 |
| Intel | Core Ultra NPU、OpenVINO、vPro 企业生态；AI PC 份额基座大。 |
| Samsung | Exynos、Galaxy AI、内存和封装垂直能力。 |
| Huawei/HiSilicon | Kirin/Ascend/鸿蒙生态，中国端侧和车载供应链闭环。 |
| Google | Tensor SoC、Android/Pixel AI、TPU 云端到端侧协同。 |

### 10.2 高端边缘/机器人/工业模组

| 公司 | 技术优势/产品 |
|---|---|
| NVIDIA | Jetson Orin/Thor、IGX Thor、DRIVE Thor、RTX PRO Blackwell、CUDA/Isaac/Metropolis/Holoscan/NIM。 |
| Qualcomm | Dragonwing Q-8750/Q-7790/IQ 系列、QCS/QCM IoT、Ride Flex、连接和低功耗 SoC。 |
| AMD/Xilinx | Kria、Versal AI Edge、Ryzen AI Embedded、FPGA/自适应 SoC。 |
| Intel | OpenVINO、Core Ultra edge、Movidius/NCS 历史生态、工业 PC 渠道。 |
| Advantech/ADLINK/Aaeon/ASUS/Raspberry Pi/Seeed | 将 Jetson/Hailo/Qualcomm/Intel/AMD 转成可交付边缘盒子、USB/PCIe 加速器和 SoM。 |

### 10.3 离散边缘 AI 加速器与初创

| 公司 | 技术优势/产品 |
|---|---|
| Hailo | Hailo-8/10H，40 TOPS INT4、低功耗、车规 Grade 2、开发者生态强。 |
| Axelera AI | Metis/Europa，数字 in-memory，128MB L2 SRAM，H1 2026 出货 Europa。 |
| SiMa.ai | Modalix MLSoC、Palette/Edgematic，工业/视觉/物理 AI 平台化。 |
| DEEPX | DX-M1 量产、DX-M2 规划，极低功耗边缘 NPU，韩国/机器人/网关订单线索。 |
| Blaize | Graph Streaming Processor，城市/防务/智能基础设施边缘部署。 |
| Kneron | KL 系列低功耗 NPU，安防/IoT/智能家居。 |
| MemryX | 数据流边缘 AI accelerator，M.2/PCIe 模组。 |
| EdgeCortix | SAKURA 系列，可重构边缘 AI，雷达/工业/防务。 |
| BrainChip | Akida 事件/类脑/低功耗 edge AI。 |
| Kinara | Ara 系列，低功耗视觉/边缘服务器推理。 |
| Tenstorrent | Wormhole/Blackhole/Galaxy，RISC-V + AI，边缘到集群开放生态。 |
| Esperanto | RISC-V 多核低功耗 AI 推理。 |
| Expedera | NPU IP，授权给边缘 SoC 厂商。 |

### 10.4 车载 AI SoC 和智能驾驶

| 公司 | 技术优势/产品 |
|---|---|
| Mobileye | EyeQ6L/6H、SuperVision、Chauffeur、REM，累计 EyeQ 装车 2.3 亿辆以上。 |
| Qualcomm | Snapdragon Ride Flex/Cockpit Elite/Digital Chassis，混合关键性和连接能力强。 |
| NVIDIA | DRIVE Orin/Thor/Hyperion，端到端 AV/机器人软件栈。 |
| Horizon Robotics | Journey 5/6、HSD，2025 Journey 硬件出货 401 万套，国产智能驾驶龙头。 |
| Black Sesame | Huashan A1000/A2000、Wudang C1200/C1296，舱驾融合和高算力 ADAS。 |
| Tesla | FSD AI4/AI5、自研车端芯片和训练/车队数据闭环。 |
| Huawei | MDC/Ascend/ADS，智能驾驶、车云、座舱生态闭环。 |
| NXP | S32N、i.MX 95、S32 车规平台，安全和车身/网关强。 |
| Renesas | R-Car/RZ/V，日系车厂和工业视觉基础强。 |
| Ambarella | CV3/CV7/N1，低功耗视觉、车载多摄和 AI-ISP。 |
| TI/Infineon/ST/Bosch | 车规 MCU、雷达、功率、安全和域控配套。 |
| NIO Shenji/Xpeng Turing/Li Auto 自研路线 | 中国车企端侧 AI 自研趋势，更多是系统闭环和成本控制。 |

### 10.5 智能摄像头、工业视觉、AIoT

| 公司 | 技术优势/产品 |
|---|---|
| Ambarella | CVflow、CV7/N1，累计边缘 AI SoC 出货超 3900 万，安防/车载/工业视觉强。 |
| Rockchip | RK3588/RK3576，6 TOPS NPU，低成本 AIoT/边缘盒子生态庞大。 |
| Axera | M76H/AX 系列，车载/安防/边缘视觉，中国供应链强。 |
| Sophgo | BM1684/1688、边缘服务器/盒子和国产替代。 |
| SigmaStar | 安防 camera SoC，成本和渠道强。 |
| Novatek/Realtek/Himax | 摄像头/显示/低功耗视觉边缘芯片。 |
| NXP | i.MX 93W/i.MX95，工业/汽车安全和连接。 |
| Renesas | RZ/V2H，DRP-AI3 8 dense TOPS/80 sparse TOPS。 |
| STMicroelectronics | STM32N6 Neural-ART NPU，MCU 级 edge AI。 |
| Sony Semiconductor | IMX500/in-sensor AI，图像传感器加 AI 预处理。 |
| Espressif/Canaan/Kendryte/Amlogic/Allwinner/CVITEK | 低成本 AIoT、语音、视觉、开发者生态。 |

### 10.6 IP、EDA、软件和工具链

| 公司 | 技术优势/产品 |
|---|---|
| Arm | Ethos NPU、CPU/GPU IP、移动/IoT/汽车授权生态。 |
| Synopsys | ARC NPX、EDA、IP、验证工具。 |
| Cadence | Tensilica DSP/NPU、EDA、系统设计。 |
| CEVA | NeuPro NPU、DSP、无线/传感器 IP。 |
| Imagination | GPU/NNA IP，汽车和嵌入式。 |
| VeriSilicon | Vivante NPU/GPU/ISP IP，中国 SoC 设计服务。 |
| Andes/SiFive | RISC-V CPU/IP，边缘 AI 控制与开放生态。 |
| Edge Impulse | 边缘模型开发和部署平台，被 Qualcomm 收购后加强 Dragonwing/IoT 工具链。 |
| OpenVINO/ONNX/TVM/TensorRT/TFLite | 模型迁移事实标准，决定芯片可用性。 |

## 11. 投资排序与风险

### 11.1 排序

| 排名 | 方向 | 逻辑 |
|---:|---|---|
| 1 | 车载 AI SoC/舱驾融合/Robotaxi 域控 | 单车价值高、认证锁定、2027 放量清晰，软件和安全栈能长期定价。 |
| 2 | NVIDIA/Qualcomm 物理 AI 平台链 | 机器人/工业/医疗边缘从 NPI 到量产，平台生态壁垒最高。 |
| 3 | 视觉 AI SoC + VLM 视频分析 | 安防/工业/零售需求真实，云带宽节省直接可算 ROI。 |
| 4 | Hailo/Axelera/SiMa/DEEPX 等离散低功耗加速器 | 2026-2027 弹性大，但需要验证软件和渠道。 |
| 5 | AI PC/手机 NPU | 数量最大但 SoC 巨头集中，适合看龙头和内存/封装链，而不是小公司。 |
| 6 | TinyML/in-sensor AI | 长期广阔，短期价值量小；适合等待 killer app。 |

### 11.2 主要风险

1. 端侧 AI 应用没有形成刚需，AI PC/手机 NPU 利用率低。
2. 内存涨价导致设备总量大幅下滑，AI SoC ASP 提升不足以抵消出货压力。
3. 大模型继续云端化，边缘只承担轻量预处理，边缘芯片 TAM 被高估。
4. 汽车 L3/Robotaxi 法规、责任、保险进展慢于预期。
5. 边缘 AI 初创公司软件生态弱，客户验证周期拖长导致融资/现金流压力。
6. 中国供应链因制程、EDA、IP、车规验证受限，高端国产替代节奏波动。

## 12. 主要来源

| 类别 | 来源 |
|---|---|
| 半导体/AI 基建 | [Gartner 2026/2027 半导体收入预测](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026), [Deloitte 2026 AI compute/inference](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html), [TrendForce NVIDIA 2026 GPU mix](https://www.trendforce.com/presscenter/news/20260408-13003.html) |
| 设备出货/AI PC/手机 | [Gartner AI PC 2026](https://www.gartner.com/en/newsroom/press-releases/2025-08-28-gartner-says-artificial-intelligence-pcs-will-represent-31-percent-of-worldwide-pc-market-by-the-end-of-2025), [Gartner memory costs PC/smartphone 2026](https://www.gartner.com/en/newsroom/press-releases/2026-02-26-gartner-says-surging-memory-costs-will-reduce-global-pc-and-smartphone-shipments-in-2026), [IDC MWC 2026 intelligent devices](https://www.idc.com/resource-center/blog/intelligent-devices-mwc-2026/) |
| 边缘 AI 市场报告 | [ResearchAndMarkets Edge AI Chips 2026-2036](https://www.researchandmarkets.com/reports/6225879/edge-ai-chips-technologies-markets-forecasts), [Performance Analysis of Edge and In-Sensor AI Processors, 2026](https://arxiv.org/abs/2603.08725), [LLM Inference at the Edge, 2026](https://arxiv.org/abs/2603.23640) |
| NVIDIA/物理 AI | [NVIDIA Jetson Thor](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/), [NVIDIA IGX Thor](https://www.nvidia.com/en-us/edge-computing/products/igx/), [NVIDIA Robotics GTC 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Global-Robotics-Leaders-Take-Physical-AI-to-the-Real-World/), [NVIDIA DRIVE Hyperion 2026](https://investor.nvidia.com/news/press-release-details/2026/BYD-Geely-Isuzu-and-Nissan-Adopt-NVIDIA-DRIVE-Hyperion-for-Level-4-Vehicles/default.aspx) |
| Qualcomm/AMD/MediaTek | [Qualcomm Q2 FY2026](https://www.qualcomm.com/news/releases/2026/04/qualcomm-announces-second-quarter-fiscal-2026-results), [Qualcomm Dragonwing IoT CES 2026](https://www.qualcomm.com/news/releases/2026/01/qualcomm-s-ie_iot-expansion-is-complete--edge-ai-unleashed-for-d), [Qualcomm Automotive CES 2026](https://www.qualcomm.com/news/releases/2026/01/qualcomm-drives-the-future-of-mobility-with-strong-snapdragon-di), [Qualcomm Snapdragon X2](https://www.qualcomm.com/news/onq/2026/01/accelerating-the-future-of-desktop-pcs-snapdragon-x-series), [AMD CES 2026 Ryzen AI](https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-expands-ai-leadership-across-client-graphics-.html), [AMD Ryzen AI Embedded](https://ir.amd.com/news-events/press-releases/detail/1271/amd-introduces-ryzen-ai-embedded-processor-portfolio-powering-ai-driven-immersive-experiences-in-automotive-industrial-and-physical-ai), [MediaTek Dimensity 9500s](https://www.mediatek.com/press-room/mediatek-unveils-dimensity-9500s-and-dimensity-8500-to-propel-performance-gaming-and-efficiency-in-flagship-and-premium-smartphones) |
| 离散边缘加速器 | [Hailo-10H GA](https://hailo.ai/company-overview/newsroom/news/hailo-announces-general-availability-of-hailo-10h-edge-ai-accelerator-with-generative-ai-capabilities/), [Hailo-10H 产品页](https://hailo.ai/products/ai-accelerators/hailo-10h-ai-accelerator/), [ASUS UGen300 Hailo-10H](https://press.asus.com/news/press-releases/asus-ugen300-usb-ai-accelerator-generative-ai-edge/), [Axelera Europa](https://axelera.ai/news/axelera-announces-europa-aipu-setting-new-industry-benchmark-for-ai-accelerator-performance-power-efficiency-and-affordability), [Axelera 2026 funding](https://axelera.ai/news/axelera-ai-secures-more-than-250-million-funding-on-global-commercial-growth), [SiMa.ai 2026 award](https://sima.ai/press-release/sima-ai-wins-edge-ai-vision-alliance-2026-product-of-the-year-for-modalix-som/), [DEEPX DX-M1](https://deepx.org/products/ai-chips/) |
| 车载/工业视觉 | [Mobileye Q1 2026](https://ir.mobileye.com/news-releases/news-release-details/mobileye-releases-first-quarter-2026-results-updates-full-year), [Mobileye EyeQ6H design win](https://www.mobileye.com/news/mobileye-surround-adas-adds-second-top-10-automaker/), [Horizon Robotics 2025 transcript summary](https://stockanalysis.com/quote/hkg/9660/transcripts/), [Horizon Robotics revenue](https://stockanalysis.com/quote/hkg/9660/revenue/), [Ambarella CV7](https://www.ambarella.com/news/ambarella-launches-powerful-edge-ai-8k-vision-soc-with-industry-leading-ai-and-multi-sensor-perception-performance/), [Ambarella FY2026](https://investor.ambarella.com/news-releases/news-release-details/ambarella-inc-announces-fourth-quarter-and-fiscal-year-2026), [Renesas RZ/V2H](https://www.renesas.com/en/products/rz-v2h), [NXP i.MX95](https://www.nxp.com/products/i.MX95), [ST STM32N6](https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html), [Sony IMX500](https://developer.sony.com/imx500/) |
# 行业调研：【AI服务器CPU与控制平面芯片】

> 研究日期：2026-05-08  
> 研究范围：AI 服务器 host CPU、rack-scale CPU、DPU/IPU/SmartNIC、BMC/管理控制器、root-of-trust/TPM、安全管理芯片、PCIe/CXL retimer/switch/fabric controller、AI 存储/上下文存储控制器、AI 后端网络交换 ASIC。  
> 口径说明：本文市场规模为 AI 数据中心/AI 服务器相关芯片、模块和直接绑定软件/固件的出货或内部转移价值，不把 GPU/ASIC 加速器本体重复计入。自研/自用芯片按等效内部转移价估算。预测采用“基准/乐观/极度超预期乐观”三情景，且按用户要求对 2026 AI 基础设施建设保持大胆乐观。

## 0. 高浓度结论

AI 服务器 CPU 与控制平面芯片在 2026 年的投资主线，不是“GPU 附属小件”，而是 AI factory 从单机服务器进入 rack/pod/GW 级系统后，必须解决的三类控制问题：调度更多 CPU sandbox 与数据流水线、把 GPU/XPU/NIC/SSD/内存池变成可管理 fabric、把故障域和安全边界下沉到每个端口/每张卡/每个机架。

最强的一手信号来自三处：

- NVIDIA 在 GTC 2026 把 Vera CPU、Rubin GPU、NVLink 6、ConnectX-9、BlueField-4、Spectrum-6 和 Groq 3 LPU 放进同一个 Vera Rubin 平台，说明 CPU、DPU、NIC、switch 与 storage/context memory 已经被打包成 AI factory 控制平面，而不是服务器外围件。Vera CPU 官方披露 88 个 Olympus cores、LPDDR5X 内存子系统最高 1.2TB/s、NVLink-C2C coherent bandwidth 1.8TB/s，Vera CPU rack 可支持超过 22,500 个并发 CPU environments。[NVIDIA Vera CPU](https://nvidianews.nvidia.com/news/nvidia-launches-vera-cpu-purpose-built-for-agentic-ai), [Vera Rubin platform](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)
- Intel 在 2026 Q1 电话会上直说，CPU 在 AI 栈中承担 orchestration 和 control plane，并且 agentic AI 可能让 GPU:CPU 比例向 1:1 靠近；其 Q1 2026 DCAI 收入 $5.1B、同比 +22%，并披露 Xeon 6 将 host NVIDIA DGX Rubin NVL8。[Intel Q1 2026](https://www.intc.com/news-events/press-releases/detail/1767/intel-reports-first-quarter-2026-financial-results), [Q1 2026 earnings call PDF](https://download.intel.com/newsroom/2026/earnings/1Q2026-Earnings-Call.pdf)
- Astera Labs 2026 Q1 收入 $308.4M、同比 +93%、GAAP gross margin 76.3%，并称 Scorpio X-Series 320-lane AI scale-up fabric switch 已经 shipping，H2 2026 production ramp。这说明 PCIe/CXL/AI fabric 控制芯片已经可以拥有接近高端 GPU 生态的软件型毛利。[Astera Q1 2026](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results)

我对 2026-2028 的核心判断：

| 判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 全球 AI 服务器 CPU+控制平面芯片市场 | $45B-$60B | $62B-$82B | $85B-$115B |
| 未来 12 个月增速 | +30%-45% | +55%-80% | +95%-140% |
| 未来 24 个月累计市场 | $110B-$155B | $165B-$245B | $260B-$390B |
| 长期最强价值捕获 | 高端 DPU/SuperNIC、PCIe/CXL fabric switch/retimer、AI-native storage/context controller、高带宽 Arm CPU rack | 同左，叠加 CXL pooling 软件和 BMC/安全认证件 | 同左，叠加 optical-aware retimer、CXL-PNM、800G/1.6T NIC+switch 套片 |
| 2026 最确定放量 | EPYC/Xeon/Grace host CPU、ConnectX/BlueField、PCIe 5/6 retimer、BMC、800G NIC/交换 ASIC、CXL Type-3 试量 | Gen6 fabric switch、Vera CPU rack、BlueField-4 STX、CXL memory controller | PCIe/CXL/UALink 开放 scale-up fabric 被多家 hyperscaler 同时采用 |
| 2027 关键变化 | Rubin/MI400/TPU8/Trainium3 带动 HBM4、CXL、1.6T、CPU sandbox、DPU storage plane 放量 | CXL pooling 和 AI-native storage 成为长上下文推理标配 | CPU/DPU/CXL/storage controller 价值量从每服务器数百美元跳到每高端 rack 数万美元 |

投资价值排序：

1. **PCIe/CXL/AI fabric switch + retimer**：Astera 已用 70%+ 毛利和 90%+ 增速证明商业模式；AI rack 越开放、越异构，越需要 merchant fabric。
2. **DPU/SuperNIC/AI storage controller**：BlueField-4 STX、ConnectX-9、AMD Pensando、Broadcom/Marvell/NVIDIA 网络控制面会吃到每台 GPU/XPU 的网络与存储 attach。
3. **高带宽 CPU 与 CPU rack**：agentic AI 增加 sandbox、编译、检索、工具调用、数据预处理，CPU 不再只是“喂 GPU”，而成为 revenue/GW 的调度核心。
4. **BMC/root-of-trust/平台安全**：市场小于 DPU/fabric，但 attach rate 接近 100%，认证壁垒强，AI 服务器 ASP 更高，ASPEED/Nuvoton/Infineon/Caliptra 生态受益。
5. **CXL memory controller + pooling software**：2026 仍小，2027 弹性极高；DRAM 越贵，CXL pooling 的 ROI 越强。

## 1. 2026 AI 计算中心建设中的机遇、挑战和技术路径

### 1.1 行业机会

**第一，CPU attach 从“训练服务器配套”变成“agentic inference 控制面”。**  
传统训练服务器可能是 1-2 颗 CPU host 8 颗 GPU；但 agentic workload 需要更多并发环境：代码 sandbox、浏览器/工具调用、检索、数据清洗、KV cache 管理、容器调度、低延迟 RPC、故障恢复。Intel 管理层提到 agentic AI 可能把 GPU:CPU 比例向 1:1 拉近，这对 Xeon/EPYC/Grace/Vera/Graviton/Axion/Cobalt 是结构性上修。

**第二，DPU/SuperNIC 从网络卡升级为 AI 系统的安全、存储和遥测控制器。**  
BlueField-4 STX/CMX 的官方定位是 context memory storage platform，目标是让长上下文和 agent memory 不拖垮 GPU。NVIDIA 披露 STX 相比传统 CPU 架构可达更高 token throughput、能效和 page ingestion；这类 DPU 会把 storage、network、security、telemetry、compression、encryption、RDMA/NVMe-oF 绑定成 AI-native data plane。

**第三，PCIe/CXL fabric 控制芯片成为开放 AI rack 的关键。**  
PCI-SIG 2026 DevCon 的主线已经从 endpoint 速率升级转向 AI rack 内外的 retimer、CopprLink/AEC、PCIe 7 over optics、PCIe 8.0 Draft 0.5。Astera Scorpio X-Series 320-lane switch 已 shipping，Scorpio P-Series 32-320 lane PCIe 6 fabric switch 预计 H2 2026 多客户出货，说明 merchant scale-up fabric 已进入收入确认窗口。

**第四，CXL 是 AI 内存短缺时代的利用率杠杆。**  
CXL Consortium 2026 webinar 中 Samsung 把 CXL 商业化瓶颈定义为延迟、AI 带宽、虚拟化/云原生软件支持，并给出 S-CHMU、CXL-PNM、Pangaea v2。公开视频材料提到多模态输入 KV cache 约为纯文本 8 倍，机器人 15 分钟、10 actions/s 约需 1.2TB KV cache。CXL 不能替代 HBM，但适合承接 KV cache、warm data、内存池、数据库和容器弹性内存。

**第五，BMC/root-of-trust 的“低单价、高确定性”被低估。**  
AI 服务器会把功率、温度、漏液、光模块、GPU/XPU、DPU、SSD、CXL module、液冷 CDU、机架 PDU 的遥测数据压到 BMC/平台管理层。OpenBMC、Redfish、MCTP、SPDM、OCP DC-SCM、Caliptra、TPM 会从合规件变成 hyperscaler 准入门槛。BMC 单颗 ASP 不高，但 AI 服务器 BOM 中需要更高性能 AST2700/NPCM8xx、更多安全协处理、更多 out-of-band 管理端口。

### 1.2 行业挑战

| 挑战 | 为什么是 2026 的真瓶颈 | 对投资的含义 |
|---|---|---|
| 平台碎片化 | NVIDIA NVLink/BlueField/Spectrum、AMD UALink/Pensando、AWS Nitro/EFA/Neuron、Google TPU/自研网络、Meta/Microsoft ASIC 都有不同管理接口 | 中立 fabric、DPU、BMC、DCIM/telemetry software 更有价值，但开发和认证成本高 |
| PCIe/CXL Gen6/Gen7 信号完整性 | 64/128GT/s PAM4、FEC、retimer、线缆、光电转换、合规测试复杂度激增 | Retimer、AEC、connector、test/compliance 议价力上升 |
| 端到端安全 | AI agent 会调用工具、访问数据、写代码、控制工作流，攻击面从模型 API 扩散到 DPU/NIC/SSD/BMC/firmware | Root-of-trust、SPDM、secure boot、firmware signing、confidential computing 成为定价点 |
| CXL 软件生态 | 硬件可用不等于可商用；需要 Linux/Kubernetes、NUMA tiering、Redfish fabric management、allocator、telemetry | 软件/固件能力强的 controller 厂商更可能拿高毛利 |
| 供应链交期 | Advanced node、ABF、PCB、SerDes IP、HBM、CXL module DRAM、光模块、BMC wafer、测试设备都可能卡交付 | 供不应求产品维持高 ASP，二供认证价值变高 |
| 客户 ROI 压力 | 2026 capex 乐观，但客户会用 token ROI 压制低差异化部件 | 能证明提升 GPU utilization、降低 token cost、减少 downtime 的芯片更能提价 |

### 1.3 在项目已有 Top AI 芯片路线图背景下的控制平面推演

本项目已有 AI 芯片底稿把 2026-2027 年出货/价值最大的 AI 加速器主线归为：NVIDIA B300/GB300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon MLU590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200，2027 增量来自 Rubin/Kyber、MI400/MI455X、TPU8、Trainium3/4、OpenAI/Broadcom ASIC、Meta 多代 MTIA。

这些加速器路线对 CPU 与控制平面芯片的拉动如下：

| 加速器路径 | 2026 控制平面需求 | 2027 控制平面升级 |
|---|---|---|
| NVIDIA B300/GB300 | Grace CPU、ConnectX-8/9、BlueField-3/4、NVSwitch、Spectrum-X、PCIe/CXL retimer、BMC、液冷 telemetry | Vera CPU rack、BlueField-4 STX/CMX、Spectrum-6 CPO、NVLink 6/7、DSX 控制面 |
| AWS Trainium2/3 | Nitro/EFA/NeuronLink、Graviton/EPYC host、BMC、专有 fabric 管理 | Trainium3 144-chip UltraServer 带来更高 radix switch、更多 CPU orchestration、Trainium4 与 NVLink Fusion 可能开放部分接口 |
| Google TPU v7/v8 | 自研 TPU pod fabric、Axion/host CPU、Jupiter/光网络、Titan/root of trust、CXL/内存池试点 | TPU8 训练/推理分化，KV cache/内存池、CXL、1.6T 网络更重要 |
| AMD MI350/MI400 | EPYC host、Pensando/Pollara/Vulcano NIC、Infinity Fabric/UALink、PCIe 5/6 retimer、BMC | MI400/Helios 72-GPU rack 需要 UALink/PCIe/CXL fabric 和 1.6T NIC/switch |
| Meta/Microsoft/OpenAI/Broadcom ASIC | 自研/半定制 XPU + Broadcom SerDes/Ethernet + BMC/OpenBMC + security | 多 GW ASIC 导致 merchant fabric、DPU、安全、CXL 和 telemetry 的标准化采购 |
| 中国 Ascend/Cambricon/Alibaba/Baidu | 国产 BMC、PCIe switch/retimer、以太网 NIC、国产 CPU/host、液冷/电源 telemetry | 出口管制下国产控制面芯片加速替代，但软件生态和良率是约束 |

### 1.4 技术成熟与放量时间

| 技术 | 当前状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|---|
| x86 AI host CPU：EPYC Turin/Venice、Xeon 6/Clearwater Forest | 2026 已大规模出货；AI 服务器 attach 明确 | 2026 全年稳定增长，2027 随 agentic inference 提升 CPU/GPU 比例 | 2026 H2 起 CPU quota 被 hyperscaler 上修 | 2027 GPU:CPU 比例向 2:1 甚至 1:1 靠近，高端 CPU ASP 上行 |
| Arm AI CPU：Grace/Vera、Graviton、Axion、Cobalt、AmpereOne | Grace 已量产，Vera 2026 H2 partner availability | 2026 H2 Vera CPU rack 小批量，2027 放量 | 2026 Q4 高端 inference rack 开始标配 Vera/Grace 类高带宽 CPU | 2027 高带宽 Arm CPU rack 成为 premium agentic AI 的独立利润池 |
| DPU/SuperNIC：BlueField-3/4、ConnectX-8/9、Pensando、Nitro/EFA | 已放量，2026 新一代导入 | 2026 800G/1.6T NIC、DPU storage/security 扩张 | BlueField-4 STX H2 2026 在长上下文客户中试量 | 2027 DPU/storage/context memory 成为每高端 GPU rack 必配控制面 |
| PCIe 6 retimer/AEC/fabric switch | Gen5/6 retimer 已收入化，Scorpio X 已 shipping | 2026H2 Gen6 switch/retimer 在头部 AI 平台 ramp | 2027 多平台量产，PCIe/CXL/UALink 融合 | 2026H2 多家 hyperscaler 同时锁单，2027 fabric switch TAM 快速重估 |
| CXL Type-3 memory + controller | Samsung/Micron/Astera/Microsoft Azure preview | 2026 pilot，2027 limited production | 2027 云 VM/数据库/KV cache 规模化 | 2026H2-2027H1 DRAM 紧缺倒逼 CXL 成为 AI inference 必选层 |
| BMC/OpenBMC/Redfish/Caliptra | AI 服务器 100% 需要管理控制，AST2600/NPCM 已成熟 | 2026 AST2700/高端 BMC 在 AI 服务器提渗透 | 安全认证推动 ASP 上行 | BMC 从单颗管理芯片升级为 rack telemetry/security hub，ASP 翻倍 |
| Optical-aware retimer/CPO 控制面 | PCIe optical ECN/DevCon 进入标准化路径，NVIDIA Spectrum-6 CPO | 2026 验证，2027 小批量 | 2027 1.6T/CPO 与 AI rack 同步导入 | 2026 订单先行，2027 光电 retimer/switch 进入高溢价期 |

**2026 最可能的技术路径：**

- CPU：EPYC 9005/后续 Venice、Intel Xeon 6/后续 Clearwater Forest、NVIDIA Grace/Vera 在高端 AI rack 并存；自研云 CPU 用于 hyperscaler 内部成本优化。
- DPU/NIC：NVIDIA ConnectX/BlueField 继续主导 NVIDIA AI rack；AWS Nitro/EFA、Google/Meta 自研和 AMD Pensando 在非 NVIDIA/自研 ASIC 平台扩张。
- PCIe/CXL：PCIe 5/6 retimer/AEC/SCM 是确定收入，PCIe 6 fabric switch 是 H2 2026 弹性，CXL 2.0 memory expansion 是试点到小批量。
- BMC/安全：OpenBMC + Redfish + MCTP/SPDM + Caliptra/root-of-trust 成为大型客户认证语言。

## 2. 已经开始放量的关键产品：市场、渗透率、利润率

### 2.1 放量产品总表

单位：美元。未来 3 个月指 2026-05 到 2026-08 的全球 AI 服务器相关收入池；未来 12/24 个月为滚动累计。渗透率按高端 AI 服务器/rack 新出货 attach rate 估算。

| 细分技术/产品 | 代表产品/公司 | 当前放量状态 | 未来 3 个月市场 | 未来 12 个月市场 | 未来 24 个月市场 | 渗透率路径 |
|---|---|---|---:|---:|---:|---|
| AI host CPU | AMD EPYC 9005、Intel Xeon 6、NVIDIA Grace、AWS Graviton、Google Axion、Microsoft Cobalt | 已经大规模出货 | B $3.5B-$5.0B / O $5B-$7B / X $7B-$10B | B $16B-$24B / O $24B-$36B / X $38B-$55B | B $38B-$62B / O $65B-$100B / X $110B-$165B | AI 服务器 attach 接近 100%；高端 CPU ASP 因内存带宽和 PCIe lanes 提升 |
| 高带宽 Arm CPU/rack CPU | NVIDIA Grace、Vera CPU rack、云厂自研 Arm CPU | Grace 已量产，Vera H2 2026 | B $0.6B-$1.2B / O $1.2B-$2.5B / X $2.5B-$5B | B $3B-$6B / O $7B-$13B / X $15B-$28B | B $10B-$20B / O $24B-$45B / X $50B-$90B | 2026 高端 AI rack 10%-20%，2027 20%-40%，极超 50%+ |
| DPU/IPU/SmartNIC/SuperNIC | NVIDIA BlueField/ConnectX、AWS Nitro/EFA、AMD Pensando、Broadcom/Marvell NIC、Intel IPU | 已放量，800G 升级 | B $2B-$3B / O $3B-$4.8B / X $5B-$7B | B $9B-$14B / O $15B-$24B / X $25B-$38B | B $24B-$42B / O $45B-$75B / X $80B-$125B | 高端 AI 服务器 70%-90%；2027 高端 rack 几乎 100% |
| BMC/平台管理控制器 | ASPEED AST2600/AST2700、Nuvoton NPCM、Renesas/Infineon security companion | AI 服务器必配 | B $0.25B-$0.45B / O $0.45B-$0.75B / X $0.8B-$1.2B | B $1.2B-$2.0B / O $2.0B-$3.3B / X $3.5B-$5.5B | B $3B-$5.5B / O $6B-$10B / X $11B-$18B | Server attach 95%-100%；高端 AST2700/多 BMC/rack manager 渗透提升 |
| Root-of-trust/TPM/secure element | Infineon、Nuvoton、ST、Microchip、Caliptra/OCP 生态、Google Titan/AWS Nitro Security | 已强制化 | B $0.15B-$0.35B / O $0.35B-$0.65B / X $0.7B-$1.1B | B $0.8B-$1.5B / O $1.5B-$2.7B / X $3B-$5B | B $2B-$4B / O $4B-$8B / X $8B-$14B | 2026 高端 AI 服务器 60%-80%，2027 80%-95% |
| PCIe retimer/signal conditioner/SCM | Astera Aries/Taurus、Broadcom、Marvell、Credo、Parade、Montage | Gen5/6 收入化 | B $0.35B-$0.55B / O $0.55B-$0.85B / X $0.9B-$1.3B | B $1.5B-$2.2B / O $2.3B-$3.5B / X $3.8B-$5.5B | B $4B-$7B / O $7B-$12B / X $13B-$20B | 高端 AI server Gen5/6 attach 50%-70%，2027 70%-90% |
| PCIe/CXL/fabric switch | Astera Scorpio、Broadcom PEX/PCIe switch、Microchip Switchtec、Marvell、Montage | 2026 H2 ramp | B $0.25B-$0.45B / O $0.45B-$0.85B / X $0.9B-$1.5B | B $1.2B-$2.0B / O $2.2B-$4.0B / X $4.5B-$7B | B $4B-$8B / O $9B-$18B / X $20B-$35B | 2026 高端开放 rack 10%-25%，2027 25%-55%，极超 70% |
| 800G/1.6T AI Ethernet switch/NIC ASIC | NVIDIA Spectrum-X/Spectrum-6、Broadcom Tomahawk/Jericho、Marvell Teralynx、Cisco Silicon One | 800G 已放量，1.6T/CPO 导入 | B $1.8B-$3B / O $3B-$5B / X $5B-$8B | B $9B-$15B / O $16B-$27B / X $30B-$45B | B $25B-$45B / O $50B-$85B / X $90B-$140B | AI backend 网络高端端口 2026 35%-55%，2027 55%-80% |
| CXL memory controller/Type-3 module | Astera Leo、Samsung CMM-D、Micron CZ120、SK hynix CMM、Marvell/Montage | pilot/early cloud preview | B $0.4B-$0.8B / O $0.8B-$1.4B / X $1.5B-$2.5B | B $2.2B-$3.5B / O $3.8B-$6.5B / X $7B-$11B | B $6B-$11B / O $12B-$25B / X $28B-$50B | 2026 AI server <5%-10%，2027 10%-25%，极超 35%+ |
| AI storage/NVMe/RDMA controller | Marvell、Microchip、Phison、Silicon Motion、Samsung/Kioxia/Solidigm/Micron 控制器，BlueField STX | 企业 SSD/AI storage 放量 | B $0.8B-$1.4B / O $1.4B-$2.4B / X $2.5B-$4B | B $4B-$7B / O $7B-$12B / X $13B-$22B | B $11B-$20B / O $22B-$40B / X $45B-$75B | AI 存储节点 2026 30%-50% 使用高端 controller/DPU offload，2027 50%-75% |

### 2.2 增长和利润率三情景

| 细分 | 当前毛利/利润率估计 | 基准 12 个月 | 乐观 12 个月 | 极度超预期 12 个月 |
|---|---:|---:|---:|---:|
| Host CPU | AMD/Intel 数据中心 CPU blended GM 50%-65%，云自研内部转移毛利不可见 | 收入 +20%-35%，GM 50%-62% | +40%-60%，GM 55%-66% | +70%-100%，高端 CPU 供不应求，GM 60%-70% |
| Grace/Vera/高带宽 Arm CPU | NVIDIA 系统级硬件 GM 70%+，云自研按 TCO 定价 | +50%-80%，GM 65%-75% | +100%-180%，GM 70%-78% | +250%+，premium agentic rack 溢价，GM 75%-80% |
| DPU/SuperNIC | 高端 NIC/DPU 55%-75%，NVIDIA/merchant silicon 高端更高 | +35%-55%，GM 58%-70% | +70%-100%，GM 62%-74% | +120%-180%，GM 68%-78% |
| BMC/安全芯片 | ASPEED/Nuvoton 类高端控制器 55%-70%；安全芯片 40%-65% | +20%-35%，GM 55%-68% | +40%-65%，GM 58%-72% | +80%+，AI 高端 BMC ASP 提升，GM 65%-75% |
| PCIe retimer | Astera Q1 2026 GAAP GM 76.3%，行业高端 65%-76% | +25%-45%，GM 68%-74% | +55%-80%，GM 70%-76% | +100%-140%，GM 74%-80% |
| Fabric switch | 高端 switch/fabric 60%-76%，软件/firmware 拉高粘性 | +40%-70%，GM 65%-73% | +90%-130%，GM 70%-78% | +180%+，开放 scale-up fabric 成为战略件，GM 75%-82% |
| CXL controller/module | Controller 65%-78%，DRAM module 受 DRAM 成本影响 30%-60% | +35%-60%，blended GM 45%-62% | +80%-130%，GM 50%-68% | +180%+，DRAM 紧缺反而提高 pooling ROI，GM 55%-72% |
| AI Ethernet switch/NIC ASIC | Switch ASIC 55%-70%，系统设备 35%-55% | +35%-55%，GM 55%-68% | +65%-95%，GM 60%-72% | +120%-170%，CPO/1.6T 溢价，GM 65%-76% |
| AI storage controller/DPU | Enterprise storage controller 45%-65%，DPU storage 55%-75% | +25%-45%，GM 48%-65% | +60%-90%，GM 55%-70% | +110%-160%，context memory/storage 溢价，GM 60%-75% |

## 3. 在研关键产品和细分技术

### 3.1 未来快速增长的在研方向

| 在研方向 | 代表公司/产品 | 2026 状态 | 放量条件 | 未来 3 个月市场 | 未来 12 个月市场 | 未来 24 个月市场 |
|---|---|---|---|---:|---:|---:|
| Vera CPU rack / AI CPU sandbox rack | NVIDIA Vera CPU、Grace successor、ODM/OEM CPU rack | 2026 H2 partner availability | Rubin/LPX/STX 部署，agent sandbox 需求被证明 | B $0.1B-$0.3B / O $0.3B-$0.8B / X $0.8B-$1.5B | B $1B-$3B / O $3B-$8B / X $9B-$18B | B $8B-$18B / O $20B-$45B / X $50B-$95B |
| BlueField-4 STX/CMX context memory storage | NVIDIA、DDN、Dell、HPE、NetApp、VAST、WEKA、Supermicro 等生态 | 2026 H2 可用 | 长上下文/agent memory/storage tier 成为 bottleneck | B $0.1B-$0.25B / O $0.25B-$0.6B / X $0.6B-$1.2B | B $0.8B-$2B / O $2B-$5B / X $5B-$10B | B $5B-$12B / O $12B-$28B / X $30B-$60B |
| PCIe 7/8 retimer、optical-aware retimer | Astera、Broadcom、Marvell、Credo、Synopsys/Cadence IP、Keysight/Tektronix test | 2026 研发/验证 | PCIe 7 over optics、Gen8 connector pathfinding、1.6T/3.2T | B <$0.1B / O $0.1B-$0.3B / X $0.3B-$0.8B | B $0.3B-$0.8B / O $0.8B-$1.8B / X $2B-$4B | B $2B-$5B / O $6B-$12B / X $15B-$30B |
| CXL 3.x pooling/fabric + CHMU | Samsung、Astera、Micron、Marvell、Montage、Linux/Red Hat/Kubernetes/OCP | 2026 pilot | Dynamic capacity device、hot page telemetry、Redfish fabric manager 成熟 | B $0.05B-$0.15B / O $0.15B-$0.4B / X $0.4B-$0.8B | B $0.4B-$1.2B / O $1.2B-$3B / X $3B-$6B | B $3B-$8B / O $9B-$20B / X $25B-$55B |
| CXL-PNM / near-memory vector search / KV cache offload | Samsung research、memory vendors、RAG/vector DB/vLLM ecosystem | research/PoC | FAISS/vLLM/vector DB API 标准化，multi-tenant 安全 | B <$0.05B / O $0.05B-$0.15B / X $0.15B-$0.4B | B $0.2B-$0.7B / O $0.8B-$2B / X $2B-$5B | B $2B-$6B / O $7B-$18B / X $20B-$45B |
| UALink/开放 scale-up fabric 控制芯片 | AMD、Astera、Broadcom、Marvell、Intel、Synopsys/Cadence IP、UALink Consortium | 2026 design-in | MI400/Helios、非 NVIDIA ASIC rack 需要开放互连 | B $0.05B-$0.2B / O $0.2B-$0.6B / X $0.6B-$1.2B | B $0.8B-$2B / O $2B-$5B / X $5B-$10B | B $6B-$15B / O $16B-$35B / X $40B-$80B |
| Rack-level BMC/management hub | ASPEED AST2700、OpenBMC、OCP DC-SCM、Redfish、液冷/电力 telemetry aggregator | 2026 高端设计导入 | 100kW+ rack 需要统一 out-of-band telemetry | B $0.05B-$0.15B / O $0.15B-$0.35B / X $0.35B-$0.7B | B $0.4B-$1B / O $1B-$2.2B / X $2.5B-$5B | B $2B-$6B / O $7B-$15B / X $16B-$30B |
| Confidential AI / GPU-DPU-TEE control chips | AMD SEV-SNP、Intel TDX、NVIDIA Confidential Computing、DPU security offload、Caliptra | 2026 进入企业/云商用 | 金融/医疗/主权 AI 要求机密推理 | B $0.1B-$0.25B / O $0.25B-$0.6B / X $0.6B-$1B | B $0.8B-$2B / O $2B-$4B / X $4B-$8B | B $5B-$12B / O $12B-$28B / X $30B-$60B |

### 3.2 在研技术利润率

| 技术 | 基准成熟毛利 | 乐观成熟毛利 | 极度超预期毛利 | 为什么能高溢价 |
|---|---:|---:|---:|---|
| Vera/高带宽 AI CPU rack | 65%-75% | 70%-78% | 75%-82% | 与 GPU coherent coupling、LPDDR 高带宽、rack 级软件绑定，客户按 token/GW 采购 |
| Context memory storage DPU | 55%-70% | 62%-75% | 70%-80% | 直接提升 GPU utilization 和长上下文 token throughput，替换成本高 |
| PCIe 7/8 optical-aware retimer | 65%-75% | 72%-80% | 78%-85% | 物理层难度、合规测试、客户 design-in 周期长 |
| CXL pooling controller/software | 50%-68% | 60%-75% | 70%-82% | DRAM 很贵时，降低 stranded memory 的经济价值巨大 |
| CXL-PNM/KV cache offload | 45%-65% | 58%-75% | 70%-85% | 如果 workload API 标准化，可从“内存模块”变成专用推理加速器 |
| UALink/open fabric switch | 60%-75% | 70%-80% | 78%-85% | 非 NVIDIA 生态要摆脱封闭 NVLink，开放 scale-up fabric 是战略刚需 |
| Rack BMC/management hub | 55%-70% | 60%-75% | 70%-80% | 认证周期、可靠性记录、OpenBMC/Redfish 适配和客户 AVL 形成锁定 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/能力 | 供给状态 |
|---|---|---|---|---|
| 高端 CPU | 美国设计；台湾/韩国/美国代工；马来西亚/台湾/中国封测 | AMD、Intel、NVIDIA、AWS、Google、Microsoft、Ampere | TSMC 5/4/3nm、Intel 3/18A、chiplet/advanced package | 先进节点紧，但 CPU 通常不如 GPU/HBM 封装紧 |
| DPU/NIC/Switch ASIC | 美国/以色列/中国台湾设计，TSMC/Samsung 代工 | NVIDIA、Broadcom、Marvell、AMD Pensando、Intel、Cisco、AWS、Google | 7/5/4/3nm SerDes-rich SoC，112G/224G SerDes | 高端 SerDes/IP 和先进封装稀缺 |
| PCIe/CXL retimer/switch/controller | 美国、中国台湾、中国大陆、以色列 | Astera、Broadcom、Marvell、Credo、Montage、Microchip、Parade、Rambus/接口 IP | 12/7/6/5nm mixed-signal SerDes，PCIe 5/6/7 | 高端验证和客户 design-in 是瓶颈 |
| BMC/管理控制器 | 中国台湾、美国、日本 | ASPEED、Nuvoton、Renesas、Microchip、Infineon | 成熟制程 28/16/12nm，AST2700 进入更高性能 | 晶圆不紧但高端 AI BMC 认证和固件紧 |
| Root-of-trust/TPM/security | 欧洲、美国、日本、中国台湾 | Infineon、Nuvoton、ST、Microchip、Google/AWS/Meta 自研 | 安全 MCU、TPM、secure element、Caliptra IP | 认证与供应链安全审计比制程更关键 |
| CXL memory modules | 韩国/美国/中国台湾 | Samsung、Micron、SK hynix、Astera、Marvell、Montage、SMART Modular 等 | DDR5 + CXL controller + EDSFF/AIC | DRAM 价格与 CXL software readiness 决定节奏 |
| 测试/合规 | 美国、欧洲、日本、中国台湾 | Keysight、Tektronix、Anritsu、Synopsys、Cadence、PCI-SIG/CXL labs | BERT、protocol analyzer、compliance tool、VIP | Gen6/Gen7/CXL 互操作测试可能排队 |

### 4.2 供给瓶颈

1. **高端 SerDes 与 analog/mixed-signal 人才。** 112G/224G SerDes、PCIe 6/7 PAM4、CXL coherency、FEC、retimer link training 不是纯数字设计，少数团队拥有量产经验。
2. **客户认证周期。** DPU/NIC/BMC/fabric switch 一旦进入 hyperscaler 或 OEM AVL，生命周期长；但首次认证要经历信号完整性、firmware、OpenBMC/Redfish、安全、热、EMI、现场可维护性验证。
3. **Gen6/Gen7 合规和测试容量。** 64/128GT/s PAM4 需要更复杂的 BERT、scope、protocol analyzer、error injection、system-level correlation；实验室和工具本身可能成为交付瓶颈。
4. **先进节点和封装优先级被 GPU/HBM 挤占。** DPU/switch/CPU 虽不一定都用 CoWoS，但 5/4/3nm capacity、ABF、substrate、高速封装和测试仍被 AI 加速器抢占。
5. **BMC/firmware 安全审计。** OpenBMC、secure boot、firmware signing、SPDM、SBOM、漏洞响应流程会限制新进入者。
6. **CXL 软件生态。** 不是有 CXL controller 就能卖出规模，必须有 Linux/Kubernetes/Redfish/fabric manager/NUMA policy/monitoring 的端到端方案。
7. **光电互连良率和可维护性。** CPO/optical-aware retimer 要解决光引擎、热、失效更换、测试、现场清洁和标准互操作。
8. **人才与现场调试。** AI rack 的故障域跨 CPU/DPU/NIC/SSD/CXL/BMC/液冷/电源，调试人才比单芯片设计人才更稀缺。

### 4.3 成本结构与毛利决定因素

| 产品 | 成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| Host CPU | wafer 25%-40%，封装/测试 10%-20%，IP/EDA/NRE 15%-25%，渠道/OEM 10%-20% | 核心数、内存带宽、PCIe/CXL lanes、平台生命周期、云厂采购集中度 | 若 GPU/ASIC 短缺，CPU 议价弱；若 agentic CPU 比例上修，高端 CPU ASP 可上行 |
| DPU/SuperNIC | 先进 SoC wafer 25%-35%，SerDes/IP 10%-20%，封装/PCB/光电模块 15%-30%，firmware/software 10%-20% | 端口速率、RDMA/NVMe-oF/security offload、客户 stack 绑定 | 能提高 GPU utilization 或降低网络尾延迟，可把成本传导到整 rack ASP |
| BMC/安全 | 成熟制程 wafer 15%-25%，封装测试 10%-20%，固件/安全认证 20%-35%，客户支持 10%-20% | 认证、OpenBMC 适配、安全漏洞响应、长期供货 | 单价小但故障代价大，客户不会为小幅降价切换 |
| Retimer | mixed-signal die 25%-40%，封装/测试 15%-25%，高速验证 15%-25%，软件/firmware 5%-15% | PAM4 性能、功耗、兼容性、合规、客户 reference design | 只要解决 board reach 和良率问题，按端口/链路刚性 attach，价格传导强 |
| Fabric switch | 大 die/SerDes 30%-45%，封装/PCB 15%-25%，software/firmware 10%-25%，support 5%-15% | radix、latency、collective acceleration、telemetry、fabric manager | 替客户节约 GPU idle time，定价按系统价值而非芯片面积 |
| CXL module/controller | DRAM 40%-70%，controller 10%-25%，PCB/connector 5%-15%，software 5%-15% | DRAM ASP、controller telemetry、OS/K8s 适配、客户 TCO | DRAM 价格上行会推高 ASP，同时增强 pooling ROI |
| AI storage controller/DPU | controller/DPU 20%-35%，NAND/SSD BOM 50%+，software 5%-20% | NVMe/RDMA、compression、encryption、KV/context offload、存储系统生态 | 长上下文推理中，能证明 token/sec 提升即可提价 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | 市场结构 | 头部集中度判断 |
|---|---|---|
| x86 AI host CPU | AMD/Intel 双寡头，云自研 Arm 分流 | AMD+Intel 仍占绝大部分外售服务器 CPU，AI 增量 AMD 份额上行 |
| Arm AI CPU | NVIDIA Grace/Vera + AWS/Google/Microsoft 自研 + Ampere | 外售高端 rack CPU NVIDIA 最强，自用云 CPU 难外部化 |
| DPU/SuperNIC | NVIDIA 强势，AWS/Google 自研，AMD Pensando/Marvell/Broadcom/Intel 竞争 | NVIDIA 在 NVIDIA rack 生态集中度高；非 NVIDIA 生态更分散 |
| BMC | ASPEED 主导外售服务器 BMC，Nuvoton 第二梯队，部分云自研/定制 | ASPEED 在服务器 BMC 具有高集中度 |
| PCIe retimer | Astera 快速领先，Broadcom/Marvell/Credo/Parade/Montage 跟进 | AI 高端 retimer 当前 Astera 品牌和 design-in 优势显著 |
| PCIe/CXL fabric switch | Astera、Broadcom、Microchip、Marvell、Montage 等 | 仍早期，2026-2027 design win 决定格局 |
| Ethernet switch ASIC | Broadcom Tomahawk/Jericho、NVIDIA Spectrum、Cisco Silicon One、Marvell | Broadcom 仍强，NVIDIA 在 AI backend/自家平台强势 |
| CXL controller/module | Astera/Samsung/Micron/SK hynix/Marvell/Montage | 早期，controller 与 memory vendor 合作决定份额 |
| Security/TPM/root of trust | Infineon/Nuvoton/ST/Microchip + hyperscaler 自研 | 标准件分散，自研安全芯片在云内部高占比 |

### 5.2 可量化壁垒

| 壁垒 | 量化特征 | 为什么能定价 |
|---|---|---|
| 高速 SerDes | 112G/224G PAM4、PCIe 6 64GT/s、PCIe 7 128GT/s；误码、jitter、FEC、equalization 均极难 | 不稳定会导致整 rack 不可用，客户愿意为 proven silicon 支付溢价 |
| 客户认证 | Hyperscaler/OEM design-in 12-24 个月，量产后生命周期 3-5 年 | 切换成本远高于芯片差价，供应商可维持高毛利 |
| 软件/firmware | OpenBMC、Redfish、SPDM、NVMe-oF/RDMA、fabric manager、Linux/Kubernetes CXL | 控制芯片价值来自可管理性，不是裸硬件；软件越深，毛利越像平台 |
| 规模和良率 | 大客户订单带来量产学习曲线；合规测试和 burn-in 成本随规模摊薄 | 小厂即使功能相似，也难证明现场可靠性 |
| 生态绑定 | NVIDIA CUDA/NVLink/BlueField/Spectrum，AWS Nitro/EFA，Google TPU fabric，OCP/OpenBMC | 进入生态即成为默认采购；未进入生态很难替换 |
| 安全与合规 | TPM/FIPS/Common Criteria、SPDM、secure boot、SBOM、firmware signing | 安全事故成本巨大，客户优先选已有审计记录的供应商 |
| 工程支持 | AI rack 调试需要跨芯片/主板/线缆/光模块/液冷/电源支持 | 供应商能派工程团队解决现场问题，本身就是溢价能力 |

### 5.3 哪一层长期高 ROIC/高毛利

长期最高 ROIC 的不是普通 CPU，也不是低端 BMC，而是 **“高速互连控制硅 + 固件/软件 + 客户认证”** 这一层，包括 DPU/SuperNIC、PCIe/CXL retimer、fabric switch、AI storage/context controller、CXL controller。原因：

- 它们的 die size 和 BOM 低于 GPU/HBM，但影响整 rack 利用率、尾延迟和故障恢复，价值/成本比极高。
- Design-in 后生命周期长，客户切换成本高。
- 它们需要 mixed-signal、protocol、firmware、OS、cloud stack 同时成熟，新进入者学习曲线长。
- 量产后毛利率可稳定在 60%-80%，Astera 2026 Q1 GAAP GM 76.3% 是直接证据。

第二梯队高 ROIC 是 BMC/root-of-trust。市场规模小，但确定性高、认证长、现金流稳。第三梯队是 host CPU，高端 AI CPU rack 有很强弹性，但 x86 传统 CPU 会受到 hyperscaler 自研和采购议价压制。

## 6. 2026 关键变化：三个行业拐点

### 拐点一：CPU 从 host 变成 agentic AI 控制面

2026 年最可能被上修的是 CPU 需求，不是因为传统 CPU 训练变多，而是 agentic inference 把 CPU 用在 sandbox、工具调用、浏览器环境、代码执行、数据预处理和 orchestration。Intel 的“CPU 是 AI stack control plane”表述是非常重要的行业口径变化。最可能放量：

- EPYC 9005/后续 Venice 在高内存带宽/PCIe lanes 的 AI host。
- Xeon 6 在企业 AI、NVIDIA DGX Rubin NVL8 host 和 CPU-rich inference。
- Grace/Vera CPU rack 在 NVIDIA premium agentic AI factory。
- 云自研 Arm CPU 在 AWS/Google/Microsoft 内部降本。

### 拐点二：PCIe 6 fabric switch 和 retimer 从配套件变成 AI rack 核心 BOM

Astera Scorpio 320-lane switch shipping 是 2026 的商业验证。2026 H2 最可能看到：

- Gen6 retimer attach rate 在 GPU/ASIC/SSD/NIC 链路提升。
- Scorpio P/X、Broadcom/Microchip/Marvell PCIe/CXL switch 进入更多平台。
- AEC/CopprLink 成为高端 AI server/rack 内默认布线。
- PCIe 7/8 研发预算提前确认，测试工具和 IP 先受益。

### 拐点三：DPU/storage/context memory 成为长上下文推理的性能阀门

NVIDIA BlueField-4 STX 把 DPU 从安全/网络 offload 推到 context memory storage。2026H2 如果 CoreWeave、Mistral、Lambda、VAST/WEKA/DDN 等生态出现公开案例，市场会把 AI storage controller/DPU 从企业存储逻辑重估为 token throughput 逻辑。最可能放量：

- BlueField-4 STX/CMX。
- NVMe-oF/RDMA storage DPU。
- AI storage appliance 中的高端 controller 和 networking ASIC。
- 与 CXL/KV cache tiering 绑定的控制软件。

## 7. 2027 关键变化：三个行业拐点

### 拐点一：Rubin/MI400/TPU8/Trainium3 把控制平面从 server 级推到 pod 级

2027 高端 AI 平台的共同特征是更大 scale-up domain、更高 HBM/DRAM 压力、更高网络 radix、更复杂故障域。CPU/DPU/BMC/fabric switch 不再按单服务器采购，而是按 rack/pod reference design 采购。最可能放量：

- Vera CPU rack、LPX inference rack、BlueField-4 STX storage rack、Spectrum-6 SPX Ethernet rack。
- AMD Helios/MI400 对 UALink、Pensando、开放 fabric 的拉动。
- TPU8/Trainium3/4 对自研网络和 merchant support silicon 的外溢需求。

### 拐点二：CXL 从“扩内存卡”变成 AI 内存池控制面

2027 年如果 Azure CXL preview 走向 GA，且 AWS/GCP/Oracle/Meta 有至少一家公开跟进，CXL 会进入第二阶段：不是插卡扩容，而是 CXL-aware allocator、Kubernetes plugin、fabric manager、CHMU/hot page telemetry、KV cache tiering。最可能放量：

- CXL Type-3/CMM-D/CZ120 类模块。
- Leo/Structera/Marvell/Montage controller。
- CXL switch/fabric manager。
- Pangaea-like memory orchestration software。

### 拐点三：安全和管理从 BMC 板卡级进入 rack/system 级

AI rack 的故障和攻击面在 2027 会明显放大：液冷、1.6T 光模块、CXL memory、DPU storage、GPU fabric、BESS/BBU、PDU telemetry 都需要 out-of-band 管理和安全 attest。BMC 会从“一台服务器一个管理控制器”扩展到 rack manager、DC-SCM、secure update、SPDM attestation、component-level telemetry。最可能放量：

- ASPEED AST2700/Nuvoton 高端 BMC。
- OCP DC-SCM/OpenBMC/Redfish 参考设计。
- Caliptra/root-of-trust/secure element。
- Rack-level telemetry aggregator。

## 8. 头部公司与潜在受益公司清单

### 8.1 AI host CPU 和高带宽 CPU

- **AMD**：EPYC 9005 Turin，后续 Venice/Zen 6；AI 服务器 host CPU 份额上行，MI300/MI350/MI400 生态协同。
- **Intel**：Xeon 6 P-core/E-core，Clearwater Forest/18A，Xeon 6 host DGX Rubin NVL8；Q1 2026 DCAI 收入 $5.1B。
- **NVIDIA**：Grace、Vera CPU、NVLink-C2C、Vera CPU rack，CPU 与 GPU/DPU/NIC 一体化优势最强。
- **AWS Annapurna**：Graviton、Nitro、Trainium/Inferentia 生态，内部自用规模巨大。
- **Google**：Axion CPU、TPU/Jupiter/Titan 生态。
- **Microsoft**：Cobalt CPU、Maia/NIC/security 生态。
- **Ampere Computing**：AmpereOne/AmpereOne M，Arm server CPU 外售生态。
- **Arm**：Neoverse CSS/平台 IP，间接受益于云自研 CPU。
- **Qualcomm/Nuvia、Tenstorrent、SiFive/RISC-V 生态**：远期或边缘/专用控制 CPU 机会。
- **Huawei/HiSilicon、Phytium、Hygon、Loongson、Zhaoxin**：中国 AI 服务器国产 host CPU 替代方向。

### 8.2 DPU/IPU/SmartNIC/SuperNIC

- **NVIDIA**：BlueField-3/4、ConnectX-7/8/9、Spectrum-X，AI DPU/NIC 最强生态。
- **AMD Pensando**：Pensando DPU、Pollara/Vulcano AI NIC，MI400/Helios 开放 rack 重要支撑。
- **AWS**：Nitro、EFA、内部网络/安全控制面。
- **Google**：自研 NIC/offload/Titan/Jupiter fabric。
- **Broadcom**：Thor/NetXtreme/以太网控制器、Tomahawk/Jericho switch ASIC、custom AI XPU SerDes。
- **Marvell**：OCTEON DPU、Teralynx、custom silicon、NVLink Fusion 生态。
- **Intel**：IPU/Mount Evans/Oak Springs Canyon、E2000 生态，尽管商业进展需观察。
- **Cisco**：Silicon One、AI networking。
- **Napatech、Achronix/FPGA SmartNIC、Kalray、Netronome/Corigine、Fungible 技术资产**：细分 offload 和可编程网络。
- **Mellanox 生态 ODM/OEM**：Dell、HPE、Supermicro、Lenovo、Wiwynn、Quanta、Foxconn/Hon Hai、Inventec。

### 8.3 BMC、OpenBMC、平台管理

- **ASPEED**：AST2600/AST2700，服务器 BMC 事实龙头；AI 服务器高端化有 ASP 弹性。
- **Nuvoton**：NPCM/Arbel/Pilot 系列，BMC 第二梯队和安全 MCU。
- **Renesas、Microchip、Infineon、STMicroelectronics、Texas Instruments**：平台管理 MCU、hot-swap、PMBus、security companion。
- **OCP/OpenBMC 社区、DMTF Redfish、Open Compute DC-SCM**：标准与生态壁垒。
- **AMI、Phoenix、Insyde、9elements、Linux Foundation OpenBMC vendors**：固件/BIOS/BMC 软件服务。
- **Google、Meta、Microsoft、AWS**：内部 BMC/OpenBMC 分支和 rack manager 规范对供应商有决定性影响。
- **中国供应商**：华为、浪潮/Inspur、超聚变、新华三/H3C、宝德、龙芯/国产 MCU 与 BMC 替代链。

### 8.4 PCIe/CXL retimer、switch、controller、IP/EDA

- **Astera Labs**：Aries/Taurus/Leo/Scorpio，2026 Q1 高增长和高毛利，AI connectivity 代表公司。
- **Broadcom**：PCIe switch、SerDes、Ethernet switch ASIC、custom XPU。
- **Marvell**：PCIe/CXL/SerDes/custom silicon、OCTEON、Teralynx。
- **Microchip**：Switchtec PCIe switch，企业/存储/HPC 生态。
- **Montage Technology**：CXL/PCIe/DDR interface、内存接口芯片，中国本土受益者。
- **Credo**：高端 SerDes、AEC、retimer/line card 生态。
- **Parade、Rambus、Synopsys、Cadence、Alphawave Semi、Arteris、Siemens EDA**：PCIe/CXL/UCIe/SerDes IP、VIP、验证工具。
- **Keysight、Tektronix、Anritsu、Teledyne LeCroy**：高速合规测试、protocol analyzer、BERT。
- **Samtec、TE Connectivity、Amphenol、Molex、Luxshare/立讯、BizLink、Credo AEC 生态**：CopprLink/AEC/连接器线缆。

### 8.5 CXL memory、内存池和 near-memory

- **Samsung**：CMM-D、CXL-PNM、Pangaea v2、HBM/DRAM 协同。
- **Micron**：CZ120 CXL memory module，CXL memory expansion 白皮书与平台实测。
- **SK hynix**：CXL memory module、HBM/DRAM 供应。
- **Astera Labs**：Leo CXL smart memory controller，Microsoft Azure M-series preview。
- **Marvell、Montage、Microchip、Rambus**：CXL controller/switch/IP。
- **Red Hat/Linux/Kubernetes/OCP**：CXL 软件生态与编排。
- **SMART Modular、MemVerge、UnifabriX、XConn、泛联信息/澜起生态**：CXL module/pooling/fabric 细分公司。
- **FAISS、Milvus/Zilliz、Weaviate、Pinecone、pgvector、vLLM、LMCache、SGLang**：CXL-PNM/KV cache offload 的潜在软件入口。

### 8.6 AI Ethernet switch、光电互连和网络控制面

- **Broadcom**：Tomahawk、Jericho、DSP/SerDes，AI backend switch ASIC 龙头。
- **NVIDIA**：Spectrum-X、Spectrum-6、CPO、NVLink/NVSwitch/ConnectX/BlueField 一体化。
- **Marvell**：Teralynx、Alaska、custom silicon、electro-optics。
- **Cisco**：Silicon One。
- **Intel/Barefoot Tofino 资产**：可编程交换历史资产，商业动向需观察。
- **Arista、Cisco、Juniper/HPE、Celestica、Accton/智邦、UfiSpace、Edgecore**：交换机系统和白盒网络。
- **Coherent、Lumentum、Broadcom optical、Marvell、Credo、InnoLight/中际旭创、Eoptolink/新易盛、Accelink/光迅、HG Genuine/华工正源、Fabrinet**：800G/1.6T/CPO/LPO 光电链。

### 8.7 AI storage controller、NVMe、上下文存储

- **NVIDIA**：BlueField-4 STX/CMX，把 storage/context memory 纳入 AI factory。
- **Marvell**：NVMe SSD controller、storage SoC、DPU。
- **Microchip**：NVMe switch/controller、PCIe switch。
- **Phison、Silicon Motion、Maxio/联芸、InnoGrit/英韧、RayMX**：企业/客户端 SSD 控制器，AI warm storage 和国产替代受益。
- **Samsung、Kioxia、Solidigm/SK hynix、Micron、Western Digital、YMTC/长江存储**：SSD/NAND 和控制器系统。
- **DDN、Dell、HPE、IBM、NetApp、VAST Data、WEKA、Pure Storage、Weka/VAST/Cloudian/MinIO 生态**：AI storage 系统，拉动控制芯片和 DPU attach。

### 8.8 安全、可信执行和管理标准

- **Infineon、Nuvoton、STMicroelectronics、Microchip、Renesas**：TPM、secure element、security MCU。
- **OCP Caliptra、OpenTitan、Google Titan、AWS Nitro Security、Microsoft Pluton**：root-of-trust 与开放/自研安全架构。
- **AMD SEV-SNP、Intel TDX/SGX、NVIDIA Confidential Computing、Arm CCA**：confidential AI 计算基础。
- **DMTF SPDM/MCTP/Redfish、UEFI、TCG、PCI-SIG DOE/CMA-SPDM**：固件和设备认证标准。
- **Anjuna、Fortanix、Edgeless Systems、Opaque Systems、Enveil/FHE 生态**：机密计算软件，对硬件 attestation 有拉动。

## 9. 投资跟踪指标

1. **CPU/GPU attach ratio**：Intel/AMD/NVIDIA/云厂是否继续讨论 agentic AI 需要更多 CPU sandbox；如果从 1:8 向 1:4、1:2 甚至 1:1 变化，CPU TAM 会被显著上修。
2. **Vera CPU rack 和 BlueField-4 STX 客户案例**：CoreWeave、Mistral、Lambda、OCI、Vultr、VAST/WEKA/DDN 等是否公开部署。
3. **Astera Scorpio P/X 出货节奏**：H2 2026 production ramp 是否按计划，多客户变体是否扩大。
4. **PCIe 6/7 compliance 和 retimer attach rate**：Gen6 合规列表、DevCon/PCI-SIG 进展、OEM reference design。
5. **CXL 云实例 GA**：Azure M-series CXL preview 是否 GA，AWS/GCP/Oracle 是否跟进。
6. **OpenBMC/Caliptra/Redfish 进入 RFP**：如果 hyperscaler 把安全 attestation 和 rack telemetry 写入采购规范，高端 BMC 和 root-of-trust 会提价。
7. **800G/1.6T 后端网络端口增长**：IDC/Dell'Oro/公司订单中 AI backend Ethernet、CPO、LPO、DSP optics 的端口占比。
8. **DRAM/HBM 价格**：DRAM 越贵，CXL pooling 和 memory utilization software 的 ROI 越强。
9. **非 NVIDIA 开放 rack 进展**：AMD Helios/UALink、Broadcom XPU、OpenAI/Meta/Microsoft ASIC 是否采用 merchant fabric/DPU。
10. **BMC/retimer/DPU 交期与 ASP**：若交期拉长、客户愿意预付款或锁单，说明控制平面芯片已从外围件变为战略件。

## 10. 主要来源

### 一手资料与公司公告

- [NVIDIA Vera Rubin platform](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)
- [NVIDIA Vera CPU](https://nvidianews.nvidia.com/news/nvidia-launches-vera-cpu-purpose-built-for-agentic-ai)
- [NVIDIA Vera Rubin POD technical blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- [NVIDIA BlueField-4 STX](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption)
- [NVIDIA DSX/Omniverse DSX](https://nvidianews.nvidia.com/news/nvidia-releases-vera-rubin-dsx-ai-factory-reference-design-and-omniverse-dsx-digital-twin-blueprint-with-broad-industry-support)
- [Intel Q1 2026 financial results](https://www.intc.com/news-events/press-releases/detail/1767/intel-reports-first-quarter-2026-financial-results)
- [Intel Q1 2026 earnings call PDF](https://download.intel.com/newsroom/2026/earnings/1Q2026-Earnings-Call.pdf)
- [AMD Q1 2026 financial results](https://www.amd.com/en/newsroom/press-releases/2026-5-5-amd-reports-first-quarter-2026-financial-results.html)
- [AMD EPYC 9005 Series](https://www.amd.com/en/products/processors/server/epyc/9005-series.html)
- [AWS Project Rainier](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster)
- [AWS Trainium3 UltraServer](https://www.aboutamazon.com/news/aws/trainium-3-ultraserver-faster-ai-training-lower-cost/)
- [Google Ironwood TPU](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/)
- [Google eighth-generation TPU](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era/)
- [OpenAI and Broadcom 10GW collaboration](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-announce-strategic-collaboration-deploy-10)
- [Astera Labs Q1 2026 results](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results)
- [Astera Leo CXL Smart Memory Controllers for Microsoft Azure M-series preview](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-leo-cxl-smart-memory-controllers-microsoft-azure-m)
- [CXL Consortium Vertical Optimization webinar](https://computeexpresslink.org/event/overcoming-cxl-limitations-enabling-cxl-hardware-and-software-as-vertical-optimization-technologies/)
- [CXL Consortium About CXL](https://computeexpresslink.org/about-cxl/)
- [Samsung CMM-D](https://semiconductor.samsung.com/cxl-memory/cmm-d/)
- [Micron CXL memory expansion white paper](https://www.micron.com/content/dam/micron/global/public/products/white-paper/cxl-memory-expansion-a-close-look-on-actual-platform.pdf)
- [PCI-SIG Developers Conference 2026](https://pcisig.com/pci-sig-developers-conference-2026)
- [PCIe 8.0 Draft 0.5](https://pcisig.com/blog/pcier-80-specification-draft-05-now-available-track-2560-gts-transfer-speeds-2028)
- [PCIe 7.0 specification resource](https://pcisig.com/specifications/pcie-70-specification-version-03-now-available-members)
- [ASPEED AST2700 product page](https://www.aspeedtech.com/server_ast2700/)
- [Open Compute Project OpenBMC](https://www.opencompute.org/projects/openbmc)

### 行业报告与交叉验证

- [Gartner semiconductor revenue 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- [Gartner IT spending 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-22-gartner-forecasts-worldwide-it-spending-to-grow-13-point-5-percent-in-2026-totaling-6-point-31-trillion-dollars)
- [IDC semiconductor market AI infrastructure growth](https://www.idc.com/resource-center/blog/semiconductor-market-to-surge-past-the-trillion-dollar-threshold-ai-infrastructure-drives-market-growth/)
- [IDC Ethernet switch market AI data center growth](https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/)
- [Deloitte 2026 AI compute power and data center capex](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html)
- [TrendForce 2026 Blackwell/Rubin outlook](https://www.trendforce.com/presscenter/news/20260408-13003.html)
- [TrendForce HBM4 validation outlook](https://www.trendforce.com/presscenter/news/20260213-12929.html)
- [McKinsey $7T data center build-out](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-7-trillion-dollar-data-center-build-out-how-industrials-can-capture-their-share)

### 项目内已有资料

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\conference_update\nvidia_gtc_2026_research.md`
- `D:\drive\Investment\调研\v5\conference_update\pci_sig_devcon_2026_update.md`
- `D:\drive\Investment\调研\v5\conference_update\cxl_vertical_optimization_2026.md`
- `D:\drive\Investment\调研\v5\conference_update\chiplet_summit_2026_update.md`
- `D:\drive\Investment\调研\v5\conference_update\ASPLOS_2026_conference_update.md`

# 行业调研：【AI服务器整机与机架集成】

> 截至日期：2026-05-08  
> 口径：本文研究“AI服务器整机与机架集成”行业，覆盖AI服务器OEM/ODM、rack-scale系统、OCP/ORv3/ORW机架、液冷与机柜内供配电、整柜测试/交付、AI存储/网络/线缆/管理软件等与整机交付强绑定的环节。芯片路线部分引用项目内已有《全球AI芯片路线图与2026-2027产能释放预测》，外部资料侧重最近半年、尤其2026年的公司公告、发布会、订单/积压、高管表态、OCP/行业会议与行业报告。  
> 方法：用一手信息定锚，用行业报告交叉验证，用乐观到极度乐观假设测算2026-2027。所有美元为名义美元，`B` = 十亿美元。市场规模区间是订单/收入池估算，可能与客户CapEx、供应商收入、GPU含税含HBM售价存在口径差异，不能简单相加。

## 0. 一页结论

2026年，AI服务器整机与机架集成的核心变化不是“更多GPU服务器”，而是交付单位从服务器节点升级为**液冷整柜、整列、POD级AI工厂组件**。这个变化会让低毛利ODM看似只是代工，但实际把订单、测试、运维、液冷、电力、网络和客户认证的控制权集中到少数系统级交付商手里。我的核心判断如下：

| 判断 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---:|---:|---:|
| 2026全球AI服务器/整柜系统收入池 | $360-460B | $480-620B | $680-850B |
| 2027全球AI服务器/整柜系统收入池 | $520-700B | $760-1,000B | $1.10-1.45T |
| Rack-scale系统在AI服务器价值中的渗透率 | 2026: 30-40%；2027: 45-55% | 2026: 40-50%；2027: 55-68% | 2026: 50-60%；2027: 68-80% |
| AI服务器整机/机架集成商混合毛利率 | 6-12% | 8-15% | 10-18%，但只限于有GPU配额、液冷和系统测试能力的头部 |
| 价值链长期高ROIC环节 | GPU/ASIC平台、HBM/先进封装、网络/SerDes、液冷关键件、机架级电力/软件 | 同左，另加CPO/OCS、KV cache storage | 同左，且系统级认证/运维数据会形成客户锁定 |

最重要的事实锚点：

- TrendForce预计2026年全球AI服务器出货同比增长超过28%，全球服务器总出货增长12.8%；GPU服务器仍占69.7%，ASIC AI服务器占比升至27.8%，为2023年以来高点。TrendForce同时称北美Top 5 CSP 2026 CapEx预计同比增长40%。  
- Gartner预计2026年全球半导体收入达到$1.320T，AI半导体约占30%，hyperscaler AI基础设施支出同比增长超过50%；DRAM和NAND价格2026年预计分别上涨125%和234%，内存通胀会直接传导到AI服务器BOM。  
- Dell FY26披露AI优化服务器订单超过$64B、全年出货超过$25B、进入FY27时AI backlog为$43B，并指引FY27 AI优化服务器收入约$50B。  
- Supermicro FY26 Q3净销售额$10.2B，同比从$4.6B大幅增长，FY26收入指引$38.9-40.4B；其美国、台湾、荷兰制造布局和DCBBS模块化方案说明“本地化+液冷+快速NPI”正在成为门槛。  
- Foxconn/Hon Hai 2025年报称AI server sector 2026仍将强劲增长；2026年4月收入约NT$832B、同比+29.7%，市场报道指出增长由AI server和cloud/networking拉动。Foxconn官方在GTC 2026展示Vera Rubin NVL72整柜、模块化数据中心和垂直集成能力，进一步证明ODM正在从板卡/服务器转向整柜/AI factory集成。  
- NVIDIA GTC 2026公布Vera Rubin平台，称七类芯片进入full production、五类rack级系统覆盖GPU、CPU、LPU、storage和Ethernet；GB300 NVL72则已给出72颗Blackwell Ultra GPU、36颗Grace CPU、130TB/s NVLink、37TB fast memory、每GPU 800Gb/s网络连接等明确规格。

一句话投资结论：  
**2026最确定的是GB300/Blackwell Ultra整柜、冷板液冷、800G网络、AI rack power与整柜测试交付；2027弹性最大的是Rubin/MI450/Trainium3/TPU8/OpenAI-Broadcom等多路线rack-scale系统、1.6T/CPO/OCS、800VDC/HVDC供电、KV cache storage。整机ODM收入弹性大但利润率天花板低，真正能长期定价的是GPU/ASIC平台、HBM/CoWoS、液冷关键件、网络/连接、机架级电力与系统软件/认证数据。**

## 1. 2026机遇、挑战与最可能技术路径

### 1.1 机会：AI计算中心建设从“服务器采购”变成“AI工厂交付”

2026年的机会来自四个方向同步放大：

1. **计算密度上升**：GB300 NVL72、Vera Rubin NVL72、AMD Helios、Trainium3 UltraServer、Google Ironwood TPU pod等系统都把单位交付从单机服务器推向rack/POD。机架集成商的任务从装配服务器变成处理液冷、功率瞬态、NVLink/scale-up fabric、firmware、rack burn-in和现场调试。
2. **客户CapEx确定性高**：Dell FY26 AI订单/积压已经把2027出货可见度抬高；OpenAI/Broadcom 10GW、Meta/AMD最高6GW、AWS Rainier近50万颗Trainium2与Anthropic百万颗目标、Google TPU向外部客户扩张，说明AI基础设施不是单一GPU周期，而是多平台并行扩产。
3. **供应链从单点短缺变成全栈短缺**：GPU/HBM/CoWoS仍是最大瓶颈，但2026开始，液冷CDU、冷板、快接头、rack power shelf、busway、800G/1.6T光模块、AEC铜缆、系统burn-in工位也进入瓶颈清单。非GPU环节议价能力上行。
4. **OCP/开放标准降低单客户定制浪费**：OCP EMEA 2026材料显示Open Data Center for AI正在把rack form factor、network、power、cooling、security、telemetry标准化；这会提高可复制性，也会让头部供应商在标准制定阶段锁定客户。

### 1.2 挑战：高收入、低容错、低利润率的交付生意

| 挑战 | 为什么重要 | 投资含义 |
|---|---|---|
| GPU/HBM/CoWoS排产被上游锁定 | 整机厂收入随GPU到货确认；若GPU/HBM延迟，整柜交付无法确认 | 看订单不能只看backlog，要看GPU allocation、HBM供应和客户验收 |
| 液冷可靠性 | GB200/GB300/Rubin级密度下，快接头、冷板、manifold、现场冲洗和漏液检测都会决定上架速度 | 液冷关键件和现场服务利润率可能高于整柜装配 |
| 机柜功率跃迁 | 70-120kW是2026主流高密区间，OCP讨论已指向500kW-1MW/rack路线 | 48V、800VDC/HVDC、busbar、PDU、BBU、超级电容/飞轮会从设施配角变成架构变量 |
| 整柜测试和burn-in | NVLink/SerDes/HBM/冷却/电力瞬态必须整柜验证，测试时间可能成为隐形产能瓶颈 | 有大规模rack burn-in产线的ODM/OEM更稀缺 |
| 价格传导困难 | GPU/HBM涨价可传给客户，但ODM装配费很难按比例涨 | 整机厂利润弹性低于收入弹性；能卖软件、服务、液冷、电力模块的公司更好 |
| 客户集中和融资风险 | 大额订单来自hyperscaler、neocloud和主权AI；若利用率或融资变差，交付节奏会波动 | 高beta，适合看订单兑现，不适合只按收入倍数外推 |
| 出口管制与本地化 | 美国、欧洲、中国、中东主权AI要求供应链可审计/本地化 | 美国/Mexico/Taiwan/Europe多点制造与安全认证形成壁垒 |

### 1.3 当前已在使用的主流技术

| 技术层 | 2026主流形态 | 关键公司/生态 | 状态 |
|---|---|---|---|
| GPU整柜 | GB200/GB300 NVL72、HGX B200/B300、DGX/RTX PRO Blackwell | NVIDIA、Dell、Supermicro、HPE、Lenovo、Foxconn、QCT、Wiwynn、Inventec、Wistron | 大规模放量 |
| GPU开放/替代路线 | AMD MI350 PCIe/OAM、MI400/MI450/Helios早期 | AMD、Meta、OpenAI、Celestica、HPE、Supermicro | MI350放量，Helios 2026H2起步 |
| 自研ASIC整柜 | TPU Ironwood、Trainium2/3、MTIA、OpenAI/Broadcom XPU | Google/Broadcom、AWS/Annapurna、Meta/Broadcom、OpenAI/Broadcom | 从自用转向独立产能池 |
| Scale-up互连 | NVLink/NVSwitch、NeuronLink、ICI、UALink、ESUN/SUE-T | NVIDIA、AWS、Google、AMD/UALink、OCP | NVLink成熟；开放scale-up 2026 design-in |
| Scale-out网络 | 800G Ethernet/InfiniBand，1.6T导入，Spectrum-X/Quantum-X800 | NVIDIA、Broadcom、Arista、Cisco、Celestica、Marvell | 800G主流，1.6T 2026-2027放量 |
| 液冷 | D2C cold plate、CDU、manifold、UQD快接、rear-door/side-car | Vertiv、CoolIT、Boyd、Schneider/Motivair、Modine、nVent、Delta、Auras | 高密AI rack默认配置 |
| 机架供电 | 48V rack、HPRv2/HPRv4、busbar、PDU、BBU、UPS、800VDC试点 | Vertiv、Eaton、Schneider、Delta、Lite-On、AcBel、nVent、Rittal | 48V成熟，HVDC/LVDC试点 |
| 整柜管理 | BMC/Redfish、DCIM、Mission Control、telemetry、安全启动/Caliptra | NVIDIA、Dell、HPE、Lenovo、OpenBMC、AMI、Microsoft/OCP | 从可选项变成RFP项 |
| AI存储/上下文内存 | NVMe/JBOF、BlueField STX、KV cache tier、并行文件/对象存储 | NVIDIA、Dell、Supermicro、DDN、VAST、WEKA、Pure、NetApp、WDC、Seagate | 推理放量带来新增attach |

### 1.4 结合2026-2027出货量最大芯片路线的成熟/放量时间

项目内芯片研究给出的2026-2027最大出货平台包括：NVIDIA B300/GB300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon MLU 590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200、Alibaba T-Head Zhenwu、AMD MI400/MI455X Helios。对整机与机架集成行业的推演如下：

| 技术/系统 | 绑定芯片路线 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期成熟/放量 | 2026最可能性 |
|---|---|---|---|---|---|
| GB300 NVL72整柜液冷 | NVIDIA B300/GB300 | 2026 Q2-Q4持续爬坡，2027H1仍主力 | 2026Q3形成稳定大批量交付 | 2026Q2后客户提前锁满2027产能 | 最高 |
| HGX/OAM 8-GPU服务器 | B200/B300、MI350 | 2026全年企业/主权AI继续放量 | 被企业AI、私有云、政府项目拉动 | 供电/冷却门槛低，成为非hyperscaler主流 | 高 |
| 直冷冷板+CDU+快接 | GB300、Rubin、MI350/MI400、TPU、Trainium | 2026成为高端rack默认，2027向企业/colo扩散 | 2026H2冷板/CDU供不应求 | 液冷现场服务成为系统交付瓶颈，高溢价 | 最高 |
| 800G AI fabric | GB300、Ironwood、Trainium2/3、MTIA | 2026主流，2027与1.6T共存 | 1.6T提前进入spine/scale-across | 800G/1.6T均紧缺，端口价值上行 | 最高 |
| 1.6T光模块/交换机 | Rubin、MI400、TPU8、Trainium3/4 | 2026小批量，2027主流 | 2026H2开始明显贡献收入 | 2027成为大型AI region默认 | 中高 |
| CPO/OCS/硅光交换 | Spectrum-6/SPX、Google TPU-like fabric | 2026 pilot，2027小批量 | 2027进入头部客户规模项目 | 2026H2订单显性化，2027收入放大 | 中 |
| UALink/ESUN开放scale-up | AMD Helios、非NVIDIA ASIC/GPU | 2026 design-in，2027首批量产 | 2027上半年多厂商pod验证 | 2027形成第二套scale-up生态 | 中 |
| 800VDC/HVDC rack power | 500kW+ rack、AI campus | 2026新建项目试点，2027扩散 | 2027成为高密AI factory优选 | 电网灵活性要求提前触发大单 | 中 |
| KV cache/context memory rack | BlueField STX、推理AI agent | 2026随Vera Rubin/GB300导入，2027放量 | 2026H2成为推理POD标配 | 推理token爆发使存储rack紧缺 | 中高 |
| 模块化AI数据中心/预制化rack pod | Foxconn、Vertiv、Schneider、Supermicro DCBBS | 2026大型客户试点，2027复制 | 2027随主权AI/neoCloud批量 | 2026H2就被Stargate/主权AI拉动 | 中高 |

## 2. 已开始放量的关键产品：市场规模、渗透率、利润率

### 2.1 定义

“已开始放量”指2026年已经有明确大规模订单、出货或客户部署的产品，不包括只有PPT路线图的方向。市场规模是全球口径的季度/年度收入池估算，尽量不重复计算芯片本身，但对“整柜系统”由于客户采购常是含GPU的整柜，表中单列“含GPU整柜”和“系统集成/非GPU价值”两个视角。

### 2.2 已放量产品三情景

| 产品/细分技术 | 当前放量证据 | 未来3个月市场规模 | 未来12个月市场规模 | 未来24个月市场规模 | 渗透率路径：基准/乐观/极度乐观 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| 含GPU rack-scale整柜系统：GB200/GB300 NVL72、B300 rack | Dell FY26出货>$25B、backlog $43B；NVIDIA GB300规格已明确；Foxconn AI rack增长 | $45-75B / $65-95B / $90-130B | $220-340B / $320-480B / $460-680B | $360-560B / $560-850B / $850B-1.20T | AI服务器价值中rack-scale占比：30-40% / 40-50% / 50-60%，到2027-2028升至55-80% | 整柜集成商6-12% / 8-15% / 10-18%；NVIDIA平台显著更高 |
| 非GPU系统集成价值：机架、母线、液冷、线束、测试、服务 | GB300/Rubin/Helios均要求整柜交付；OCP标准推动rack接口统一 | $8-14B / $12-20B / $18-28B | $45-75B / $70-110B / $110-170B | $90-150B / $150-240B / $240-380B | 单GPU/ASIC的系统附加价值从2025约$2k-5k提升到2027约$6k-15k | 10-18% / 14-22% / 18-28%，取决于是否含现场服务 |
| 8-GPU HGX/OAM/PCIe AI服务器 | 企业、主权AI、二线云仍大量采购；MI350/RTX PRO/GB300 HGX覆盖 | $35-55B / $45-70B / $65-95B | $150-230B / $200-300B / $280-420B | $180-300B / $250-420B / $380-600B | 在AI服务器出货台数中仍高，但价值占比被NVL72挤压；2026 45-60%，2028降至25-45% | OEM/ODM 5-10% / 7-13% / 9-15%；企业品牌溢价更高 |
| D2C冷板、CDU、manifold、快接头、漏液检测、液冷集成 | OCP/Promersion称2025 cold plate >$5B；GB300/Rubin/MI400默认液冷 | $8-14B / $12-20B / $18-30B | $35-65B / $55-90B / $85-140B | $75-130B / $120-210B / $200-330B | 高端AI rack液冷attach：2026 60-75% / 75-85% / 85-95%；2027 80-98% | 25-40% / 32-48% / 40-55%，高可靠快接/现场服务最高 |
| 机架内供电：48V power shelf、PDU、busbar、BBU、机柜级监控 | OCP HPRv2/HPRv4、NVIDIA DSX、100kW+ rack需求 | $7-13B / $10-18B / $15-25B | $32-60B / $50-85B / $80-130B | $65-120B / $110-190B / $180-320B | 100kW+ AI rack供电占比：2026 25-40% / 40-55% / 55-70%；2027 50-80% | 22-35% / 28-42% / 35-50% |
| 800G交换机、NIC/DPU、光模块、DAC/AEC | TrendForce称2026 800G+出货占比>60%；GB300每GPU 800Gb/s连接 | $18-35B / $28-48B / $42-70B | $75-130B / $120-200B / $190-300B | $140-260B / $240-420B / $400-650B | 800G在AI后端网络端口中2026为主流，2027逐步与1.6T共存 | 光模块15-35%；交换芯片/品牌交换机40-65%；AEC/连接25-45% |
| 高速铜缆、背板、连接器、线束、CopprLink/AEC | Rack内铜互连复杂度提升，GB300/Rubin/Helios均需高密连接 | $2.5-5B / $4-7B / $6-10B | $10-22B / $18-32B / $28-48B | $20-45B / $38-70B / $65-110B | 高密AI rack中AEC/DAC/高端连接器attach接近100%；单rack价值持续上升 | 22-35% / 28-42% / 35-50% |
| AI数据平台与推理存储：JBOF/NVMe、并行文件、对象存储、KV cache tier | NVIDIA STX/BlueField-4、Supermicro AI Data Platform、Dell AI Factory | $5-10B / $8-15B / $12-22B | $25-50B / $40-80B / $70-120B | $60-130B / $110-220B / $200-380B | 推理rack storage attach：2026 15-30% / 25-40% / 40-55%；2027 45-75% | 硬件15-35%；软件/数据平台45-75% |
| OCP/ORv3/ORW机柜、rack integration服务 | OCP-recognized IT infrastructure 2025约$132B、2029约$295B | $6-12B / $9-16B / $14-24B | $30-55B / $45-80B / $70-120B | $55-110B / $90-170B / $150-260B | 新建AI campus采用OCP/ORv3/ORW：2026 35-50%，2027 50-70% | 8-18% / 12-25% / 18-30%，认证和现场交付带溢价 |

### 2.3 已放量产品的增长解释

- **GB300/NVL72是2026最确定主线**：TrendForce称2026 AI服务器增长主要来自北美CSP、主权云、ASIC和边缘推理；GPU仍为主导，GB300推动大部分GPU系统出货。NVIDIA官方GB300 NVL72规格显示单柜已经是72 GPU、36 Grace CPU、20TB GPU HBM、37TB fast memory和130TB/s NVLink带宽的系统级产品，不再是普通服务器节点。
- **Dell是整机需求最透明的一手样本**：FY26 AI订单>$64B、出货>$25B、backlog $43B、FY27 AI服务器收入指引$50B，说明客户下单速度远快于确认收入速度。对行业而言，这意味着2026-2027的关键不是“有没有订单”，而是“GPU/HBM/液冷/电力/客户验收能否把backlog转成收入”。
- **Supermicro显示高beta也伴随运营风险**：FY26收入指引接近$40B，Q3同比翻倍以上，但公司披露库存、应收、出口合规调查、客户集中和毛利压力等风险。整机集成是高周转、高现金消耗、高合规敏感业务。
- **液冷从增配变成准入门槛**：OCP材料称2025 cold plate市场已超过$5B、immersion约$0.8B。2026对GB300/Rubin/Helios/TPU/Trainium来说，液冷能力决定是否能拿到高密客户订单。
- **AI存储被低估**：NVIDIA Vera Rubin平台把BlueField-4 STX storage rack作为五类rack之一，专门处理agentic AI产生的KV cache，声称推理吞吐可提升至多5倍。这意味着AI服务器整柜不只是compute rack，还会带出context memory/storage rack。

## 3. 在研/快速增长关键产品与细分技术

### 3.1 在研与早期放量方向三情景

| 在研/早期技术 | 当前阶段 | 未来3个月市场规模 | 未来12个月市场规模 | 未来24个月市场规模 | 渗透率路径：基准/乐观/极度乐观 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| NVIDIA Vera Rubin NVL72、Vera CPU rack、LPX、STX、SPX | 七类芯片full production；合作伙伴2026H2可用 | $2-8B / $5-15B / $10-25B | $70-150B / $120-240B / $220-380B | $260-520B / $450-850B / $800B-1.25T | 2026H2 early ramp，2027高端训练/agentic inference主力 | NVIDIA平台65-75%；系统伙伴6-15%；STX/软件更高 |
| AMD Helios/MI450/MI455X整柜 | Meta最高6GW，首批2026H2；OpenAI也有AMD 6GW协议 | $1-4B / $3-9B / $6-18B | $25-70B / $60-140B / $120-260B | $120-300B / $260-550B / $500-900B | 2026H2验证，2027成为第二GPU供应源 | AMD GPU 45-60%+；ODM 6-15%；open rack服务10-25% |
| OpenAI/Broadcom custom accelerator rack | OpenAI/Broadcom 10GW，2026H2开始，2029完成 | $0.5-3B / $2-7B / $5-15B | $20-70B / $60-150B / $120-280B | $90-240B / $220-520B / $450-900B | 2026小批，2027>1GW级别可见 | Broadcom ASIC/网络55-70%；系统集成8-18% |
| AWS Trainium3/4 UltraServer | Trainium3 GA，144芯片/362 FP8 PFLOPs；Trainium4支持NVLink Fusion | $5-14B / $10-25B / $20-45B | $50-120B / $100-220B / $200-380B | $180-380B / $350-700B / $650B-1.1T | Trainium2已百万颗目标，Trainium3 2026-2027接棒 | 自用转移价低于GPU；系统/网络内部化，外部供应商看部件 |
| Google TPU 8t/8i、Ironwood扩展 | Ironwood 9,216芯片液冷pod，TPU8训练/推理分化 | $5-15B / $10-30B / $20-50B | $60-150B / $120-260B / $220-450B | $220-450B / $420-800B / $750B-1.2T | ASIC AI服务器2026占27.8%，TPU是最大外部化路线 | Broadcom/供应链高；Google自用利润不公开 |
| Meta MTIA 400/450/500 | 四代两年，MTIA300已生产，400/450/500主攻GenAI inference | $1-5B / $3-10B / $8-20B | $20-60B / $50-130B / $100-240B | $90-220B / $200-480B / $400-850B | 2026逐步导入，2027推理规模化 | ASIC设计/IP高；rack可复用降低系统成本 |
| UALink/ESUN/SUE-T开放scale-up fabric | UALink 2.0、ESUN 1.0；2026 design-in | <$1B / $1-3B / $2-6B | $3-12B / $8-25B / $18-55B | $18-65B / $50-140B / $120-300B | 2027在非NVIDIA GPU/ASIC pod渗透5-20% | IP/交换芯片50-75%；硬件系统20-45% |
| CPO、OCS、硅光交换、multi-core fiber | OCP展示OCS/CPO/MCF；NVIDIA Spectrum-6 CPO进入平台叙事 | $1-4B / $2-8B / $5-15B | $8-30B / $25-70B / $60-150B | $45-150B / $130-350B / $300-700B | 2026 pilot，2027头部AI region采用 | 硅光/光引擎35-60%；模块15-35%；早期系统溢价高 |
| 800VDC/HVDC rack power、sidecar、BBU协同 | OCP HPRv4、800V/750/1500V互操作讨论 | $0.5-2B / $1-5B / $3-10B | $5-18B / $15-45B / $40-100B | $35-100B / $90-250B / $220-550B | 2026新建AI campus试点，2027 500kW+ rack首选 | 30-50%，保护/控制/认证件更高 |
| 模块化/预制化AI factory、整列/POD交付 | Foxconn modular data center、Supermicro DCBBS、Vertiv/Schneider集成 | $2-8B / $5-18B / $12-35B | $20-60B / $55-150B / $130-320B | $100-280B / $260-650B / $600B-1.2T | 主权AI、Stargate、neocloud对交付速度敏感 | EPC低；模块化集成/运维15-35%；软件服务更高 |

### 3.2 哪些在研产品最值得盯

1. **Vera Rubin五rack系统**：NVIDIA不只是发布GPU，而是把Vera CPU rack、Rubin NVL72 GPU rack、Groq LPX LPU rack、BlueField-4 STX storage rack、Spectrum-6 SPX Ethernet rack打包成POD-scale架构。这会把服务器整机行业从“卖服务器”推向“交付AI supercomputer子系统”。
2. **AMD Helios/MI450**：Meta最高6GW协议和2026H2首批出货，是2027非NVIDIA rack-scale最大的变量。若Helios在ROCm、scale-up、液冷、整柜测试上顺利，AMD相关ODM/电源/液冷/网络供应链会有第二增长曲线。
3. **OpenAI/Broadcom 10GW**：这是2026H2开始、2029完成的超大规模custom accelerator与Ethernet rack项目。它的意义不是立刻替代GPU，而是证明AI实验室会直接定义rack系统，ODM会被要求按模型工作负载而非通用服务器规格交付。
4. **TPU/Trainium/MTIA外部化**：Google TPU卖给Anthropic，AWS Trainium绑定Claude，Meta MTIA数十万级部署。ASIC服务器在2026占比接近28%，意味着整机集成商要支持更多非NVIDIA参考设计。
5. **CPO/OCS/MCF**：1.6T以后，光互连的瓶颈从模块封装进入硅光、光电测试、CPO可维护性和光纤布线。若Google/NVIDIA/Broadcom推动成功，光互连供应链利润池会前移。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 产能层级 | 主要地区 | 主要公司 | 能力特征 |
|---|---|---|---|
| 品牌OEM/方案总包 | 美国、中国、欧洲 | Dell、HPE、Lenovo、Cisco、Supermicro、Inspur、H3C、xFusion | 客户关系、认证、售后、融资、软件/存储/网络attach |
| ODM/JDM整机和整柜 | 台湾、中国大陆、墨西哥、美国、捷克/荷兰 | Foxconn/Hon Hai、Quanta/QCT、Wiwynn、Wistron、Inventec、Pegatron、Gigabyte、ASUS、Aivres、Celestica、Jabil、Sanmina、Flex、ZT Systems | NPI速度、GPU平台适配、液冷装配、整柜测试、规模制造 |
| AI rack电力/热管理 | 美国、欧洲、台湾、中国 | Vertiv、Eaton、Schneider、nVent、Rittal、Delta、Lite-On、AcBel、CoolIT、Boyd、Modine、Danfoss、Parker、Auras、AVC、Nidec | 100kW+机柜供电、CDU/冷板、快接、漏液检测、现场服务 |
| PCB/载板/连接 | 台湾、日本、中国、韩国、东南亚 | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、Compeq、Tripod、Gold Circuit、Wus、Kingboard、ITEQ、Amphenol、TE、Molex、Luxshare、BizLink、FIT | 高层板、ABF、线缆、背板、连接器、信号完整性 |
| 半导体上游 | 台湾、韩国、美国、日本 | TSMC、SK hynix、Samsung、Micron、ASE、Amkor、Broadcom、Marvell、NVIDIA、AMD | GPU/ASIC/HBM/CoWoS/SerDes决定整柜可交付量 |
| 现场交付/EPC | 美国、欧洲、中东 | Quanta Services、EMCOR、MasTec、MYR、Fluor、Jacobs、AECOM、Turner、Kiewit | 电力接入、白空间、机电安装、预制化、验收 |

2026产能重心有两个方向：一是台湾/墨西哥/美国的AI rack装配和整柜测试，二是美国/欧洲本地化交付与合规认证。Foxconn、Dell、Supermicro等都在强调美国本地能力；这不是政治姿态，而是因为NVL72级整柜交付的运输、返修、客户验收和出口管制风险都更适合近场化。

### 4.2 供给瓶颈

| 瓶颈 | 具体表现 | 受影响产品 | 可能缓解时间 |
|---|---|---|---|
| HBM3E/HBM4 | HBM stack、base die、TC bonding、测试时间、内存价格上涨 | GB300、Rubin、MI400、TPU8、ASIC rack | HBM3E 2026逐步缓解；HBM4 2027仍紧 |
| CoWoS/先进封装 | CoWoS-L/S、SoIC、interposer、ABF载板、underfill、warpage | NVIDIA/AMD/Broadcom/TPU/Trainium | 2026扩产仍被预订；2027增量更大 |
| 液冷关键件 | 冷板加工、快接头可靠性、manifold、CDU、漏液传感、现场冲洗 | GB300/Rubin/Helios/Trainium3/Ironwood | 2026H2改善，但高端件持续紧 |
| 机架供电与连接 | 48V shelf、busbar、高电流连接器、PDU、BBU控制、暂降穿越 | 100kW+ AI rack | 2027标准化后改善；800VDC仍早期 |
| 整柜测试/burn-in | NVLink/SerDes/液冷/电力/firmware联合测试占用工位 | 所有rack-scale系统 | 2026是隐形瓶颈，头部ODM扩线 |
| 光模块/交换芯片 | 800G DSP、硅光、EML/VCSEL、1.6T良率、CPO测试 | AI fabric、scale-out网络 | 800G 2026主流，1.6T 2027紧 |
| 客户认证与现场验收 | 机房水质、电力波动、BMC/firmware、OCP/安全认证 | 大客户整柜订单确认收入 | 永久性壁垒，标准化只能降低摩擦 |
| 人才与交付 | 液冷运维、数据中心机电、系统调试、可靠性工程师短缺 | 大型AI campus | 2026-2027持续紧张 |
| 物流/关税/出口管制 | 整柜重量、跨境转运、美国/中国出口限制、客户本地化 | ODM/OEM全球排产 | 不确定，需多区域冗余 |

### 4.3 成本结构与毛利决定因素

典型GB300/Rubin/Helios类高端整柜BOM粗拆如下：

| 成本项 | 含GPU整柜BOM占比 | 非GPU系统价值占比 | 说明 |
|---|---:|---:|---|
| GPU/ASIC加速器模块，含HBM和先进封装 | 65-80% | 不适用 | 最大价值池，也决定整柜售价和交期 |
| CPU、主板、内存、OAM/UBB/托盘 | 4-10% | 15-25% | Grace/EPYC/Vera/自研CPU平台差异大 |
| 网络：NIC/DPU、NVSwitch/scale-up、交换机、光模块 | 5-12% | 20-35% | 1.6T、CPO、DPU/STX会提升占比 |
| 液冷：冷板、CDU、manifold、快接、管路、漏液检测 | 3-8% | 12-25% | 高密rack中价值上升，可靠性决定溢价 |
| 供电：power shelf、PDU、busbar、BBU、线束、电容 | 2-6% | 10-20% | 100kW+后单柜电力价值显著提高 |
| 机柜、结构件、线缆、背板、连接器 | 2-5% | 8-18% | 高速铜缆/连接器毛利高于普通结构件 |
| 系统集成、测试、burn-in、现场安装与服务 | 3-8% | 15-30% | ODM/OEM真正能争取利润的部分 |
| 软件/管理/安全/运维 | 1-4% | 5-15% | 毛利高但基数小；长期客户锁定强 |

毛利的决定因素：

1. **是否拿到GPU/ASIC allocation**：有配额的整机厂可以用交期换价格，没有配额只能做低价装配。
2. **是否拥有液冷和整柜测试能力**：客户愿意为稳定交付、少漏液、少现场返修支付溢价。
3. **客户结构**：hyperscaler压价强、毛利低但规模大；企业/主权AI/科研客户毛利更高但交付碎片化。
4. **是否能卖附加产品**：存储、网络、安全、DCIM、运维服务、融资租赁能显著改善利润率。
5. **供应链金融能力**：高端整柜库存和应收巨大，低资金成本本身是壁垒。
6. **价格传导机制**：GPU/HBM/DRAM/NAND涨价通常可以传给客户；人工、测试、良率、返修和液冷故障成本更难完全转嫁。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 层级 | 竞争格局 | 集中度判断 | 定价权 |
|---|---|---|---|
| GPU/ASIC平台 | NVIDIA主导，AMD第二供应源，Broadcom/Google/AWS/Meta/OpenAI自研ASIC上升 | 极高 | 最高 |
| 品牌OEM | Dell、HPE、Lenovo、Supermicro、Cisco等 | 中高 | 企业/主权AI较高，hyperscaler较低 |
| ODM/JDM | Foxconn、Quanta/QCT、Wiwynn、Wistron、Inventec、Pegatron、Celestica、Jabil等 | 高，头部客户项目集中 | 收入弹性大，毛利受压 |
| 液冷/电力 | Vertiv、Schneider、Eaton、nVent、CoolIT、Boyd、Delta、Rittal等 | 中高，关键件集中 | 高端件定价较强 |
| 网络/连接 | NVIDIA、Broadcom、Marvell、Arista、Cisco、Amphenol、TE、Credo等 | 高 | 芯片/IP强，模块/组装分化 |
| AI存储/数据平台 | Dell、HPE、NetApp、Pure、VAST、WEKA、DDN、Supermicro、NVIDIA STX生态 | 中 | 软件和数据平台强，硬件一般 |

TrendForce预测2026 GPU AI服务器仍占约69.7%，ASIC AI服务器占27.8%。这意味着NVIDIA体系仍是整机集成的最大收入来源，但ASIC rack会逐渐打破单一GPU参考架构，给ODM/JDM、网络芯片、开放scale-up和定制化散热/供电带来新机会。

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 为什么能定价 |
|---|---|---|
| GPU/ASIC配额和供应链关系 | NVIDIA/AMD/Broadcom/Google/AWS等平台需要认证伙伴协同 | 客户买的是交期；交期稀缺时可保持装配费和服务费 |
| 液冷可靠性和现场经验 | 漏液、压降、水质、冲洗、快接、维修流程都需要经验数据 | 一次事故可能造成百万美元级损失，客户愿意为低风险付费 |
| 整柜系统验证 | NVLink/SerDes/HBM/电力/firmware必须整柜burn-in | 测试工位和know-how稀缺，认证后切换成本高 |
| 规模制造与资金周转 | 单柜价值数百万美元，库存、应收、预付款和保险要求高 | 小厂难以承受现金流和供应商账期压力 |
| 客户认证与RFP锁定 | Hyperscaler/主权AI认证周期长，涉及安全、固件、运维、现场标准 | 进入供应商名单后有持续订单，切换会影响项目进度 |
| 软硬件集成 | BMC、telemetry、DCIM、Mission Control、OpenBMC、Redfish、Caliptra | 软件和运维数据形成粘性，不只是一次性硬件装配 |
| 全球交付和本地化 | 美国、墨西哥、台湾、欧洲多点制造和现场服务 | 满足关税、出口管制和客户数据/供应链主权要求 |
| 标准参与 | OCP、UALink、ESUN、Open Rack、冷板/UQD等标准制定 | 早期参与者更容易把自身接口变成客户默认规格 |

### 5.3 价值捕获：长期高ROIC在哪

最高长期ROIC层级排序：

1. **GPU/ASIC平台与网络硅**：NVIDIA、Broadcom、AMD、Marvell、AWS/Google/Meta自研生态。原因是架构、软件、HBM/封装配额和客户工作负载共设计形成强锁定。
2. **HBM/先进封装/ABF载板**：SK hynix、Micron、Samsung、TSMC、ASE、Amkor、Ibiden、Unimicron等。原因是供给扩张慢、验证周期长、替代成本高。
3. **液冷关键件和机架级电力**：CoolIT、Boyd、Vertiv、Schneider、Eaton、nVent、Delta、Rittal等。原因是可靠性事故成本高、现场认证强、供应商不容易被随意替换。
4. **高速连接/SerDes/AEC/CPO/OCS**：Amphenol、TE、Molex、Luxshare、Credo、Astera、Broadcom、Marvell、Coherent、Lumentum、Innolight、Eoptolink等。原因是信号完整性、功耗和良率决定GPU利用率。
5. **系统软件、DCIM、安全与运维数据**：NVIDIA Mission Control、Dell/HPE管理栈、OpenBMC/Redfish生态、Caliptra/OCP SAFE服务。原因是毛利高、客户锁定强，但收入基数低于硬件。
6. **整机/整柜ODM**：收入弹性最大，但长期毛利率最低。只有能够把液冷、电力、测试、服务和客户认证打包出售的头部，才能维持高于普通代工的ROIC。

## 6. 2026关键变化：三个行业拐点

### 6.1 拐点一：GB300/Blackwell Ultra整柜从爬坡进入主交付

2026最可能放量的技术路径是**GB300 NVL72 + 液冷 + 800G网络 + 48V rack power**。原因：

- NVIDIA官方GB300 NVL72规格已经完整；
- Dell FY26 backlog指向Grace Blackwell为主的AI服务器需求；
- TrendForce明确称2026 GPU AI服务器仍占主导，GB300推动多数出货；
- Foxconn、Supermicro、Dell、HPE、Lenovo、QCT/Wiwynn等均围绕Blackwell/Rubin rack扩产品线。

投资含义：GB300整柜会继续拉动液冷、供电、线缆、800G、整柜测试、现场服务。整柜ASP高，但ODM毛利不一定同步提升，除非能卖附加服务。

### 6.2 拐点二：ASIC rack从“云厂自用项目”变成第二产能池

AWS Rainier近50万颗Trainium2且Anthropic目标超过100万颗；Google Ironwood/TPU向Anthropic等外部客户扩张；Meta数十万MTIA部署并两年四代迭代；OpenAI/Broadcom 10GW从2026H2开始。TrendForce预测ASIC AI服务器2026占比27.8%。  
这意味着整机行业要从NVIDIA标准参考设计扩展到多种ASIC rack：不同冷却、供电、scale-up互连、软件栈和验收标准。

投资含义：支持多平台的ODM/JDM、开放rack、电力/液冷模块、Ethernet scale-up、Broadcom/Marvell网络生态会受益。

### 6.3 拐点三：电力/液冷标准化从工程后端变成采购前置条件

OCP EMEA 2026的信号非常强：Open Data Center for AI、HPRv4 HVDC、800V/750/1500V互操作、UQDv2、coldplate base spec、Caliptra/SOLID/openSFI都在2026推进。  
以前客户先买服务器，再让数据中心适配；2026开始，客户会在RFP阶段把rack power、冷却、telemetry、安全、维护流程写入采购条件。

投资含义：Vertiv/Eaton/Schneider/nVent/Rittal/CoolIT/Boyd/Delta/Auras等公司的议价能力提升；低质量液冷和电力供应商会被认证淘汰。

## 7. 2027关键变化：三个行业拐点

### 7.1 拐点一：Rubin、MI450/MI455X、Trainium3、TPU8进入同一年竞争

2027将从“Blackwell Ultra主导”进入多路线rack-scale竞争：

- NVIDIA Vera Rubin NVL72大规模放量，Vera CPU/LPX/STX/SPX形成POD级系统；
- AMD Helios/MI450若Meta/OpenAI协议执行，将成为最大非NVIDIA GPU rack路线；
- Trainium3 UltraServer和TPU8将扩大ASIC服务器池；
- HBM4/HBM4E与CoWoS-L/先进封装成为共同瓶颈。

投资含义：2027整机厂的关键能力是多平台NPI和并行测试，而不是单一GPU SKU制造。

### 7.2 拐点二：1.6T、CPO/OCS、scale-up Ethernet开始重构网络价值

800G在2026成为主流，2027大概率进入1.6T切换期。NVIDIA Spectrum-6 CPO、Broadcom Ethernet、OCP ESUN/UALink/SUE-T、Google TPU式大规模光网络会共同推动网络从“交换机+模块”转向“光电封装+多层fabric+网络软件”。

投资含义：传统光模块仍增长，但高毛利会向DSP/SerDes、硅光、CPO封装、OCS、AEC/连接器和网络软件迁移。

### 7.3 拐点三：800VDC/HVDC与模块化AI factory开始规模化

当单rack功率从100kW走向300-500kW+，传统AC到PSU再到48V的路径会面临效率、铜耗、保护和功率瞬态挑战。2027新建AI campus会更积极采用800VDC/HVDC、sidecar power、BBU协同、超级电容/飞轮/电池储能和现场发电。  
同时，主权AI和neocloud会更偏好可复制的模块化AI factory，缩短time-to-power。

投资含义：高压直流保护、电力电子、busway、rack power shelf、BBU/UPS、模块化数据中心、现场能源和DCIM会成为比传统机柜更高价值的子方向。

## 8. 头部公司与细分技术公司清单

### 8.1 整机OEM、ODM、JDM与rack-scale集成

| 细分 | 公司 |
|---|---|
| 全球OEM/品牌总包 | Dell Technologies、HPE、Lenovo、Cisco、Supermicro、Fujitsu、Eviden/Atos、NEC、Inspur、H3C、xFusion、Sugon |
| 台湾/亚洲ODM/JDM | Foxconn/Hon Hai、Quanta/QCT、Wiwynn、Wistron、Inventec、Pegatron、Gigabyte/Giga Computing、ASUS/Aivres、MiTAC/Tyan、ASRock Rack、Compal |
| 北美/全球EMS与系统制造 | Celestica、Jabil、Sanmina、Flex、ZT Systems、Benchmark、Plexus |
| AI rack/AI factory方案 | NVIDIA DGX/MGX/NVL/DSX生态、AMD Helios生态、Supermicro DCBBS、Dell AI Factory、HPE Private Cloud AI、Lenovo Neptune、Foxconn modular data center |

### 8.2 芯片与平台

| 细分 | 公司/生态 |
|---|---|
| GPU/AI平台 | NVIDIA、AMD、Intel |
| 云厂ASIC | Google TPU/Broadcom、AWS Trainium/Inferentia/Annapurna、Meta MTIA/Broadcom、Microsoft Maia、OpenAI/Broadcom |
| ASIC/IP/网络硅 | Broadcom、Marvell、Astera Labs、Credo、Synopsys、Cadence、Arm、Rambus、Alphawave Semi |
| 中国AI芯片 | Huawei Ascend、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Iluvatar CoreX、Moore Threads、MetaX、Enflame、Hygon、Sophon/Bitmain等 |
| 推理专用/新架构 | Groq、Cerebras、SambaNova、Tenstorrent、d-Matrix、Etched、MatX、Furiosa、Rebellions、Groq/NVIDIA LPX生态 |

### 8.3 液冷、热管理与机柜结构

| 细分 | 公司 |
|---|---|
| CDU/冷板/液冷系统 | Vertiv、Schneider Electric/Motivair、CoolIT、Boyd、Modine、nVent、Danfoss、Parker、Asetek、Delta、Auras、AVC、Nidec、Chilldyne、Cooler Master、Asia Vital Components |
| 浸没/新型冷却 | LiquidStack、Submer、GRC、Asperitas、Iceotope、ZutaCore、Green Revolution Cooling |
| 机柜/围护/门冷 | Rittal、nVent、Schneider、Vertiv、Eaton、Legrand、Chatsworth、Panduit、Belden |
| 泵阀/快接/流体控制 | Parker、Danfoss、Staubli、CPC/Colder、Swagelok、ITT、Sanhua、Dwyer、Watts |

### 8.4 机架供电、电力电子与储能

| 细分 | 公司 |
|---|---|
| UPS/PDU/busway/switchgear | Vertiv、Eaton、Schneider Electric、ABB、Siemens、GE Vernova、nVent、Legrand、Hubbell、Powell |
| PSU/power shelf/电源模块 | Delta、Lite-On、AcBel、Flex Power、Advanced Energy、Murata、TDK、Vicor、Bel Fuse、Astec/Artesyn、FSP |
| 功率半导体/电源IC | Infineon、onsemi、STMicro、Texas Instruments、Monolithic Power Systems、Renesas、Vishay、Wolfspeed、Navitas、Power Integrations |
| 储能/动态支撑 | Tesla Megapack、Fluence、Powin、Vertiv、Eaton、Schneider、Active Power、Piller、Vycon、Skeleton Technologies、Maxwell/Tesla ultracapacitor生态 |

### 8.5 网络、光互联、连接器与线缆

| 细分 | 公司 |
|---|---|
| AI交换机/网络系统 | NVIDIA Networking/Mellanox、Broadcom、Arista、Cisco、Juniper/HPE、Nokia、Celestica、Accton/Edgecore、UfiSpace |
| 光模块/硅光 | Coherent、Lumentum、Fabrinet、Innolight、中际旭创、Eoptolink、新易盛、Accelink、Hisense Broadband、Source Photonics、AOI、Macom |
| CPO/OCS/光引擎 | NVIDIA、Broadcom、Marvell、Intel Silicon Photonics、Ayar Labs、Lightmatter、iPronics、Celestial AI、Ciena、Nokia |
| 铜缆/AEC/连接器 | Amphenol、TE Connectivity、Molex、Luxshare、BizLink、Foxconn Interconnect Technology、Samtec、Rosenberger、Credo、Spectra7、Parade、Astera Labs |

### 8.6 PCB、载板、存储与软件

| 细分 | 公司 |
|---|---|
| ABF/高阶PCB/载板 | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、Compeq、Tripod、Gold Circuit、Wus、Kingboard、ITEQ、TTM、AT&S |
| HBM/DRAM/NAND/HDD | SK hynix、Micron、Samsung、Kioxia、Western Digital/SanDisk、Seagate、Solidigm |
| AI存储/数据平台 | Dell、HPE、NetApp、Pure Storage、VAST Data、WEKA、DDN、IBM Storage、Lenovo、Supermicro、Cloudian、Nutanix |
| BMC/firmware/DCIM/security | NVIDIA Mission Control、OpenBMC、AMI、ASPEED、Nuvoton、Schneider EcoStruxure、Vertiv Environet、Sunbird、Nlyte、Device42、Microsoft Caliptra/OCP SAFE生态 |

## 9. 投资优先级排序

| 排名 | 子方向 | 2026确定性 | 2027弹性 | 利润率质量 | 主要风险 |
|---:|---|---|---|---|---|
| 1 | 液冷关键件与整柜液冷服务 | 很高 | 很高 | 高 | 漏液事故、客户认证、竞争加剧 |
| 2 | GB300/Rubin/Helios整柜测试与集成 | 很高 | 很高 | 中低到中 | GPU供给、客户集中、价格压力 |
| 3 | 机架级供电、busway、PDU、BBU、HVDC | 高 | 很高 | 中高 | 标准切换、项目周期 |
| 4 | 800G/1.6T网络、AEC/连接器、SerDes | 很高 | 很高 | 中高到高 | 代际切换、价格竞争 |
| 5 | AI存储/KV cache/context memory rack | 中高 | 很高 | 中高 | 需求尚需推理规模验证 |
| 6 | 开放scale-up fabric：UALink/ESUN | 中 | 高 | 高 | 生态成熟慢，NVIDIA锁定强 |
| 7 | CPO/OCS/硅光交换 | 中 | 极高 | 高 | 可维护性、良率、标准不确定 |
| 8 | 传统OEM/ODM整机 | 很高 | 高 | 低到中 | 毛利压缩、现金流、客户集中 |

我的乐观假设下，2026-2027最好的组合不是单纯买“AI服务器代工”，而是找**绑定头部客户、拥有液冷/电力/测试/认证能力、能从整柜扩展到整列/POD/服务的软件硬件一体公司**。纯服务器组装收入会很大，但长期定价权弱；液冷、电力、连接、网络硅、AI存储和系统软件更可能出现利润率上行。

## 10. 主要来源索引

### 一手公司资料

- [NVIDIA Vera Rubin官方新闻稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx)：Vera Rubin七类芯片full production、五类rack、NVL72/LPX/STX/SPX/DSX、合作伙伴名单。  
- [NVIDIA Vera Rubin技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)：grid-to-chip、MGX rack架构、POD-scale系统设计。  
- [NVIDIA GB300 NVL72官方页面](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)：72 Blackwell Ultra GPU、36 Grace CPU、130TB/s NVLink、37TB fast memory、20TB GPU memory、每GPU 800Gb/s网络连接。  
- [Dell FY26 Q4/FY26 results](https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2026~2~dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-2026-results.htm)：AI优化服务器订单、出货、backlog和FY27指引。  
- [Supermicro FY26 Q3 results](https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Third-Quarter-Fiscal-Year-2026-Financial-Results/default.aspx)：Q3收入、FY26指引、DCBBS/液冷/制造布局与风险提示。  
- [Supermicro press releases](https://www.supermicro.com/en/newsroom/pressreleases)：2026年4月OCP/Arm/液冷/AI基础设施产品更新、AI Data Platform与NVIDIA STX storage server。  
- [Foxconn FY2025 & 4Q25 results](https://www.foxconn.com/en-us/press-center/events/foxconn-events/1978)：AI server sector 2026强劲增长表述。  
- [Foxconn GTC 2026事件页](https://www.foxconn.com.tw/en-us/press-center/events/foxconn-events/1756)：Vera Rubin NVL72、模块化数据中心、垂直集成。  
- [AWS Project Rainier](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster)：近50万颗Trainium2、Anthropic >100万颗目标、UltraServer/UltraCluster架构。  
- [AWS Trainium3 UltraServer](https://www.aboutamazon.com/news/aws/trainium-3-ultraserver-faster-ai-training-lower-cost)：144颗Trainium3、362 FP8 PFLOPs、4.4x算力、4x能效、Trainium4/NVLink Fusion。  
- [Google Ironwood TPU](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/)：9,216芯片液冷pod、42.5 Exaflops、192GB HBM、7.37TB/s、1.2TBps ICI。  
- [Google TPU 8t/8i](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era/)：第八代TPU训练/推理分化路线。  
- [Meta MTIA路线图](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)：四代MTIA两年、数十万部署、MTIA300生产、400/450/500面向GenAI inference。  
- [Meta与AMD 6GW协议](https://about.fb.com/news/2026/02/meta-amd-partner-longterm-ai-infrastructure-agreement/)：最高6GW AMD Instinct、2026H2首批、Helios rack-scale架构。  
- [OpenAI与Broadcom 10GW协议](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)：10GW自研AI accelerator，2026H2开始部署，2029完成，Ethernet scale-up/scale-out。  
- [AMD CES 2026](https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-and-its-partners-share-their-vision-for-ai-ev.html)：Helios、MI455X、MI440X、MI500、2nm/HBM4E路线。  
- [AMD与Meta官方新闻稿](https://ir.amd.com/news-events/press-releases/detail/1279/amd-and-meta-announce-expanded-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus)：6GW、2026H2首批、MI450/Helios。

### 行业报告、论坛与会议

- [TrendForce 2026 AI server forecast](https://www.trendforce.com/presscenter/news/20260120-12887.html)：AI服务器出货+28% YoY、GPU 69.7%、ASIC 27.8%、Top 5 NA CSP CapEx +40%。  
- [Gartner 2026 semiconductor forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)：2026半导体$1.320T、AI半导体30%、hyperscaler AI infra支出+50%、memflation。  
- [OCP EMEA Summit 2026](https://www.opencompute.org/summit/emea-summit)：Open Data Center for AI、HVDC/LVDC、液冷、UALink/ESUN、开放固件与安全。  
- [OCP Open Chiplet Economy/FCSA](https://www.opencompute.org/index.php/blog/ocp-open-chiplet-economy-is-leading-the-next-wave-of-ai-inference)：FCSA与开放chiplet经济。  
- 项目内资料：`D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`、`D:\drive\Investment\调研\v5\conference_update\OCP_EMEA_Summit_2026_高密度调研报告.md`、`D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`。

# 行业调研：【AI集群调度与推理运行时】

截至日期：2026-05-08  
研究范围：AI 计算中心中的集群调度、GPU/加速器资源管理、训练/推理作业编排、LLM 推理运行时、模型服务、KV cache/上下文内存调度、推理网关、异构加速器运行时与 AI Factory 控制面。  
口径说明：本报告把市场规模分为两层：**直接可收费规模**指调度/运行时软件 license、企业支持、托管推理平台毛收入、云控制面与专业服务；**影响/绑定算力规模**指这些软件影响的 GPU/ASIC/IaaS/AI server 支出。表格中的 3 个月、1 年、2 年通常指该时点的年化可收费收入 run-rate，不是所有公司收入，也不可简单相加。对找不到直接数据的部分，按用户要求采用偏乐观估算，并在文字中标注“本报告估算”。

## 0. 一页结论

1. **2026 年 AI 基础设施的控制点正在从“买到 GPU”转向“把 GPU/TPU/ASIC 变成稳定 token 工厂”。** Gartner 预计 2026 年 AI-optimized IaaS 支出达到 **$37.5B**，其中 **55%** 支持推理；Deloitte 预计 2026 年推理约占 AI compute 的 **2/3**，inference-optimized chips 超过 **$50B**；IDC 预计 2026 年 AI infrastructure spending 达 **$487B**。这些支出如果没有调度/运行时层，利用率和 SLA 都很难兑现。
2. **NVIDIA 的软件控制面明显上移。** 2026-03 GTC 发布的 Dynamo 1.0 被定位为 AI factories 的分布式推理 OS，官方称 AWS、Azure、Google Cloud、OCI、CoreWeave、Together、Nebius、Baseten、DeepInfra、Fireworks、Cursor、Perplexity 等已经采用或集成；Run:ai 则把 Kubernetes 上的 GPU 共享、quota、fairness、topology-aware scheduling 和 inference workload 管起来。
3. **Kubernetes 正在成为企业和云原生推理的标准底座，但不是单独赢家。** CNCF 2026 survey 显示，容器用户中 **82%** 已在生产使用 Kubernetes，托管 GenAI 模型的组织中 **66%** 用 Kubernetes 管理部分或全部推理 workload。与此同时，前沿训练仍大量依赖 Slurm，CoreWeave 的 SUNK、AWS HyperPod、Google DWS、Kueue/JobSet/DRA、Run:ai 都在把 Slurm、Kubernetes、云容量队列和 AI-aware scheduler 融合。
4. **2026 最可能放量的技术路径是“Run:ai/Kueue/Slurm 混合调度 + vLLM/SGLang/TensorRT-LLM/NIM/Dynamo 推理栈 + KV cache/prefix cache + 初步 prefill/decode 分离”。** 2027 的增量会转向“异构加速器调度 + STX/CXL/LMCache 类上下文内存 + power-aware scheduling + LPU/decode 加速器”。
5. **直接可收费软件/托管平台市场虽远小于芯片市场，但利润率和战略价值更高。** 本报告估算，2026 年全球 AI 集群调度与推理运行时直接可收费 run-rate 约 **$12B-$22B**，2027 年可到 **$28B-$55B**，极度乐观情形 2028 年可超过 **$140B**；其影响的算力/云/服务器支出 2026 年已在 **$150B-$300B** 量级，2027 年有望超过 **$500B**。
6. **高 ROIC 长期位置不在纯开源推理引擎本身，而在“硬件耦合 + 调度数据 + 企业 SLA + 云/客户分发”的控制面。** NVIDIA AI Enterprise/Run:ai/Dynamo/NIM、云厂商 HyperPod/DWS/Vertex/Azure/OCI、CoreWeave Mission Control/SUNK、Baseten/Fireworks/Together/Anyscale 这类 managed platform 最可能捕获定价权。
7. **最大挑战不是算法，而是系统工程。** GPU 拓扑、HBM/KV cache 内存、RDMA/RoCE、MIG/fractional GPU 隔离、模型冷启动、multi-tenant 安全、节点故障恢复、power cap、P99 latency 和客户成本归因，都会决定调度/运行时能不能从开源工具变成付费产品。

## 1. 2026 年的机遇、挑战和技术路线

### 1.1 行业机会：AI 工厂的目标函数变了

过去两年的 AI 基础设施投资更像“采购稀缺 GPU”。2026 年开始，客户关心的是更细的指标：tokens/sec、tokens/watt、tokens/$、TTFT、P99 latency、GPU goodput、模型冷启动时间、KV cache hit rate、每 GW 年收入、每个租户的 quota/fairness。NVIDIA 在 GTC 2026 把 Vera Rubin、Groq 3 LPU、BlueField-4 STX、Spectrum-6、DSX、Dynamo 放在同一张 AI Factory 图里，说明推理运行时和集群调度已经从 IT 管理工具变成收入产线的控制面。

本项目已有芯片路线报告给出的 2026-2027 主线是：2026 以 **NVIDIA B300/GB300 Blackwell Ultra、AWS Trainium2、Google TPU Ironwood、B200/GB200、MI350、Maia200、Meta MTIA、国产 Ascend/MLU** 为主；2027 切向 **Rubin、MI400/MI455X Helios、Trainium3/4、TPU8、更多 Broadcom XPU**。这会把调度/运行时需求从同构 GPU 集群推向异构、多代、多租户、多区域、多电力约束的系统。

### 1.2 当前正在被使用的核心技术

| 技术层 | 已使用产品/项目 | 2026 状态 | 主要价值 |
|---|---|---|---|
| Kubernetes AI 调度 | NVIDIA Run:ai、KAI Scheduler、Kueue、JobSet、DRA、Volcano、YuniKorn、KubeRay、KServe | 企业/云原生推理快速上量；DRA 在 K8s v1.34 后进入 GA 路线，2026 驱动和生态追赶 | quota、fair share、gang scheduling、GPU sharing、拓扑感知、弹性伸缩 |
| Slurm 与 K8s 混合 | SchedMD Slurm、CoreWeave SUNK、AWS HyperPod Slurm、Azure CycleCloud/AKS 混合、G-Research Armada | 大训练集群仍强；neocloud 需要训练作业和 K8s 推理服务共存 | 训练效率、HPC 生态、作业队列、K8s 服务化和可观测性融合 |
| 云容量调度 | Google Dynamic Workload Scheduler/Flex-start、AWS HyperPod task governance、Azure/OCI capacity reservation、DGX Cloud Lepton | 2026 随 GPU 稀缺与折扣容量需求放量 | 把高需求 GPU/TPU/Trainium 容量变成可排队、可预约、可借用的金融化资源 |
| 推理引擎 | vLLM、SGLang、NVIDIA TensorRT-LLM、Triton、NIM、Dynamo、Hugging Face TGI、Cerebras/Groq/SambaNova 专有 runtime | vLLM/SGLang 是开源主线；TensorRT-LLM/NIM/Dynamo 是 NVIDIA 商业化主线 | continuous batching、PagedAttention、prefix cache、speculative decoding、量化、OpenAI-compatible API |
| 分布式推理 | Dynamo、llm-d、Ray Serve/Anyscale、KServe、GKE Inference Gateway、NVIDIA NIXL、LMCache | 2026 从试点进入生产；llm-d 2026-03 加入 CNCF Sandbox | prefill/decode 分离、KV cache aware routing、multi-node serving、跨 GPU/CPU/storage 数据搬运 |
| KV cache/上下文内存 | LMCache、vLLM KV offload connector、SGLang RadixAttention、TensorRT-LLM KV connector、BlueField-4 STX/CMX、CXL memory pooling | 2026 试点，高端长上下文推理先用；2027 主流化 | 降低 TTFT、提升 cache hit、减少 HBM 压力、支持长上下文/Agent memory |
| 异构加速器 runtime | CUDA/TensorRT、ROCm/AITER、AWS Neuron、Google XLA/JAX/JetStream/vLLM on TPU、Azure Maia stack、Huawei CANN、Intel OpenVINO/Gaudi | 2026 仍割裂；2027 因 ASIC 放量必须跨平台调度 | 避免单一供应商、提升 tokens/$、按 workload 选择 GPU/TPU/ASIC/LPU |
| power-aware scheduling | NVIDIA DSX Max-Q/Flex、Schneider/ETAP/AVEVA、Vertiv、Google/AWS 内部电力调度、Emerald AI 类项目 | 2026 设计/试点；2027 与 power cap、BESS、园区 EMS 联动 | 固定电力下提高可运行 GPU 数、削峰、参与需求响应 |

### 1.3 2026-2027 技术成熟和放量时间

| 细分技术 | 当前成熟度 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|---|
| AI-aware quota/fair-share scheduler | 已商业化，Run:ai/HyperPod/DWS/Kueue 都有明确产品 | 2026 H2 成为 >512 加速器企业集群标配；2027 渗透率 55-70% | 2026 Q3 就随 Blackwell/TPU/Trainium 集群验收绑定；2027 渗透率 70-85% | 云厂商和 neocloud 强制按调度平台交付容量；2027 渗透率 85%+ |
| Kubernetes DRA 与 fractional GPU | API 成熟，驱动/生态仍在爬坡 | 2026 用于企业共享 GPU、notebook、轻推理；2027 进入主流生产 | NVIDIA DRA driver、Run:ai fractions、Kueue 配合，2027 高端企业 60% 采用 | 2027 前 GPU memory/compute slicing 像存储 PVC 一样标准化，极大提升小模型和 agent 利用率 |
| Slurm-on-K8s / hybrid scheduler | CoreWeave SUNK 已产品化；AWS HyperPod 支持 Slurm/EKS | 2026 neocloud 和 frontier lab 采用；2027 成为大训练+推理混部主线 | SUNK/Slurm bridge 成为 >10k GPU 集群默认方案之一 | 2027 训练/推理/数据处理统一底层集群，GPU 闲置率下降 10-25 个百分点 |
| vLLM/SGLang/TGI 开源 serving | 已大量使用，商业化刚起步 | 2026 继续主导 open-weight serving；2027 被 Dynamo/llm-d/KServe 包进平台 | 商业公司围绕 vLLM/SGLang 做企业支持和高端插件，2027 形成数十亿美元级市场 | Open-source runtime 成为所有云和私有部署的事实标准，供应商靠优化包、SLA、硬件适配收费 |
| NVIDIA Dynamo/NIM/TensorRT-LLM | 2026 Dynamo 1.0 production，NIM 企业容器成熟 | 2026 绑定 NVIDIA AI Enterprise；2027 在 Blackwell/Rubin 推理中主流 | 2027 Dynamo 成为跨 GPU/LPU/STX 的事实 inference OS | Dynamo 通过 Enterprise support 和 cloud marketplace 间接控制上百亿美元软件/服务收入 |
| Prefill/decode disaggregation | vLLM/TensorRT/llm-d 仍在快速迭代 | 2026 高端长上下文部署，2027 渗透 25-45% LLM GPU-hours | 2027 成为 70B+、长上下文、agent 服务默认架构 | 2027 渗透 60-75%，推理 rack BOM 因 P/D 分工、KV tier、专用 decode 加速器重构 |
| KV cache / context memory tier | prefix cache 已普及，跨节点/跨存储还早 | 2026 STX/LMCache/CXL 试点；2027 高端 AI factory 批量 | 2027 long-context agent 把 KV cache 变成独立预算项 | 2027 context memory attach rate 50%+，AI storage/KV tier 成为新百亿美元级产品 |
| 异构 accelerator scheduler | Hyperscaler 内部成熟，外部割裂 | 2026 以云厂商私有栈为主；2027 因 TPU8/Trainium3/Maia/MTIA 放量进入第三方平台 | 2027 出现跨 NVIDIA/AMD/TPU/Trainium 的 workload placement 平台 | 2027-2028 单一 GPU 云被异构 AI cloud 替代，调度层按 token economics 自动选硬件 |
| power-aware / carbon-aware scheduling | 设施侧和 workload 侧尚未深度融合 | 2026 DSX/EMS 设计阶段；2027 进入新建 GW campus | 2027 随并网审批和 power cap 成为 AI Factory 采购项 | 2027 数据中心以 power-aware scheduler 多部署 10-30% 有效算力，软件毛利率 80%+ |

### 1.4 2026 最可能的技术路径

2026 年最可能的主线不是单一产品替代，而是四条路线并行：

1. **NVIDIA 全栈路线**：Run:ai 管集群，NIM/TensorRT-LLM/Triton/Dynamo 管推理，GPU Operator/DRA 管设备，DSX 管 AI Factory 设计和功率。该路线在 Blackwell/GB300/Rubin 客户中最强，利润率最高。
2. **云厂商自研路线**：Google AI Hypercomputer/DWS/TPU runtime、AWS HyperPod/Neuron/Trainium、Microsoft Maia/Azure AI Foundry、Meta MTIA internal stack。该路线不会大量外售软件，但会定义事实需求，压迫第三方工具支持 TPU/Trainium/Maia/MTIA。
3. **云原生开放路线**：Kubernetes + Kueue/JobSet/DRA + KServe/llm-d + vLLM/SGLang/LMCache + Gateway API Inference Extension。该路线在企业私有云、OpenShift、GKE、neocloud、主权 AI 中最容易放量。
4. **Neocloud metal-to-model 路线**：CoreWeave Mission Control/SUNK、Lambda、Crusoe、Nebius、Nscale、Vultr、RunPod、Together/Fireworks/Baseten/DeepInfra 等，把硬件容量、模型服务、SLA、计费、可观测性一起卖。该路线增速最快，但融资、折旧、利用率风险最大。

## 2. 已经开始放量的关键产品：规模、渗透率、利润率

下表中的市场规模为本报告估算的**直接可收费 run-rate**。托管推理平台包含推理 API/endpoint 的 gross revenue，但不包含 OpenAI/Anthropic 等模型应用收入；调度软件不包含底层 GPU 租赁本金。多个细分存在重叠，不能直接相加。

| 已放量产品/技术 | 代表产品和事实锚 | 3 个月：基准/乐观/极度乐观 | 1 年：基准/乐观/极度乐观 | 2 年：基准/乐观/极度乐观 | 渗透率路径 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| AI 集群 quota/fair-share scheduler | NVIDIA Run:ai、AWS HyperPod task governance、Google DWS、Kueue、Volcano、CoreWeave SUNK；HyperPod 2026-03 增加 idle resource sharing | $1.4-2.3B / $2.3-3.4B / $3.4-5.0B | $3-6B / $6-10B / $10-16B | $8-16B / $16-30B / $30-55B | >512 加速器共享集群：2026 35-50%，2027 55-75%，2028 75-90% | 70-82% / 82-88% / 88-92% |
| Kubernetes AI 设备管理与 GPU sharing | Kubernetes DRA、NVIDIA DRA Driver、GPU Operator、Run:ai GPU fractions/time-slicing、MIG、DRA consumable capacity | $0.6-1.2B / $1.2-2.0B / $2.0-3.2B | $2-4B / $4-7B / $7-11B | $6-12B / $12-24B / $24-40B | 企业共享推理/开发集群：2026 20-35%，2027 45-65%，2028 65-85% | 75-88% / 85-92% / 90%+ |
| Slurm/K8s 混合训练平台 | Slurm、SUNK、HyperPod Slurm/EKS、KubeRay、Armada；CoreWeave 称 SUNK 可让 Slurm 与 K8s workload 同集群共存 | $0.5-1.0B / $1.0-1.8B / $1.8-3.0B | $2-4B / $4-8B / $8-13B | $6-14B / $14-28B / $28-50B | >10k GPU 训练/推理混合集群：2026 25-40%，2027 45-60%，2028 60-80% | 60-78% / 75-85% / 85-90% |
| 企业推理容器和商用 runtime | NVIDIA NIM、TensorRT-LLM、Triton、Dynamo、Hugging Face TGI Enterprise、OpenShift AI runtime | $2-4B / $4-6B / $6-9B | $6-12B / $12-22B / $22-35B | $18-35B / $35-65B / $65-110B | NVIDIA 高端推理 GPU-hours：2026 25-40%，2027 45-65%，2028 65-80% 使用商用/支持版 runtime | 78-90% / 88-94% / 92-96% |
| 开源 LLM serving 引擎生态 | vLLM、SGLang、TGI、Ray Serve、KServe；vLLM 2026 更新 KV offloading，SGLang 强调 RadixAttention/structured generation | $1.0-2.0B / $2.0-3.5B / $3.5-6.0B | $4-8B / $8-15B / $15-25B | $12-26B / $26-50B / $50-85B | open-weight 生产推理：2026 45-65%，2027 60-75%，2028 70-85% 直接或间接使用这些引擎 | 70-88% / 85-93% / 90%+；纯开源本身不收费，商业捕获来自支持、云服务、优化包 |
| 托管推理平台/API | Baseten、Fireworks、Together、DeepInfra、Replicate、Anyscale、CoreWeave Dedicated Inference、RunPod、Modal；Baseten 2026-02 宣布 $300M Series E、$5B 估值 | $6-12B / $12-18B / $18-28B | $15-30B / $30-55B / $55-90B | $45-85B / $85-150B / $150-260B | 企业外部推理 workload：2026 10-18%，2027 20-35%，2028 35-50%；AI native 公司更高 | 35-55% / 50-65% / 65-75%；取决于 GPU 利用率、token 单价和自研 runtime |
| KV cache、prefix cache、continuous batching | vLLM PagedAttention/KV offload、SGLang RadixAttention、LMCache、TensorRT-LLM KV connector、Dynamo/NIXL | $0.7-1.5B / $1.5-2.8B / $2.8-5.0B | $3-8B / $8-15B / $15-25B | $12-30B / $30-60B / $60-110B | 多轮 agent/长上下文推理：2026 25-45%，2027 50-70%，2028 75-90% 需要显式 KV 策略 | 65-85% / 80-92% / 90%+；硬件/存储参与时 blended 较低 |
| 云容量队列和折扣调度 | Google DWS/Flex-start、AWS HyperPod idle sharing、Azure/OCI capacity reservations、DGX Cloud Lepton | $1.5-3B / $3-5B / $5-8B | $5-10B / $10-18B / $18-30B | $15-30B / $30-60B / $60-100B | 高需求 GPU/TPU/Trainium 任务：2026 15-25%，2027 35-50%，2028 55-70% 通过队列/预约/spot-like 机制获得 | 50-75% / 70-85% / 80-90%；多数以云服务 take-rate 隐含体现 |

### 2.1 放量产品的增长逻辑

- **调度软件的 ROI 很直接。** 对一个 $500M-$2B 级别的 GPU/ASIC 集群，哪怕把有效利用率提高 5 个百分点，节省的年化折旧/机会成本就可能超过 $25M-$100M。Run:ai、HyperPod、DWS、Kueue、SUNK 的定价能力来自这个节省，而不是来自“软件功能多”。
- **推理 runtime 的价值来自 token economics。** continuous batching、prefix cache、PagedAttention、speculative decoding、量化、kernel fusion 和 P/D disaggregation 对同一套 GPU 的 tokens/sec 影响可达数倍级。只要 token 单价下行，客户就更愿意付费购买 runtime 优化。
- **托管推理平台的短期毛利不一定高，但增长最快。** 这类平台先吃到企业不想自建 vLLM/SGLang/K8s 的需求，后续靠高利用率、模型路由、LoRA/多模型合并、reserved capacity、专用推理芯片提升毛利。
- **Kubernetes DRA 的长期价值在标准化设备接口。** 一旦 GPU memory、compute fraction、NUMA/topology、健康状态通过标准 API 被调度器理解，GPU 资源会像存储卷一样被声明、借用、回收，企业平台供应商可以在此基础上收费。

## 3. 在研关键产品与快速增长技术

这些方向大多在 2026 进入 early production 或技术预览，真正放量在 2027-2028。市场规模仍按直接可收费 run-rate 估算，部分会与第 2 节重叠。

| 在研/早期放量技术 | 关键产品/项目 | 3 个月：基准/乐观/极度乐观 | 1 年：基准/乐观/极度乐观 | 2 年：基准/乐观/极度乐观 | 渗透率路径 | 预测毛利率 |
|---|---|---:|---:|---:|---|---|
| Dynamo 作为 AI Factory inference OS | Dynamo 1.0、NIXL、TensorRT-LLM/vLLM/SGLang/LMCache 集成、Groq LPU/STX 协同 | $0.3-0.8B / $0.8-1.5B / $1.5-3B | $3-7B / $7-15B / $15-25B | $15-35B / $35-75B / $75-140B | NVIDIA Blackwell/Rubin 推理集群：2026 10-25%，2027 40-65%，2028 65-85% | 85-95%，若随 AI Enterprise/云服务打包可接近软件高毛利 |
| llm-d / Gateway API Inference Extension 标准化 | CNCF Sandbox llm-d、Red Hat/Google/IBM/NVIDIA/CoreWeave 生态，Kubernetes-native distributed inference | $0.1-0.4B / $0.4-0.8B / $0.8-1.5B | $1-3B / $3-7B / $7-12B | $6-15B / $15-35B / $35-70B | 企业 K8s LLM serving：2026 5-10%，2027 20-35%，2028 45-65% | 75-92%；开源标准本身免费，商业捕获在 OpenShift/云/支持/网关 |
| Prefill/decode disaggregation 标准栈 | vLLM disagg prefill、TensorRT-LLM disaggregated serving、NIXL/UCX/RDMA、LMCache | $0.2-0.8B / $0.8-2B / $2-4B | $3-10B / $10-22B / $22-40B | $20-60B / $60-120B / $120-220B | 70B+ 和长上下文推理 GPU-hours：2026 5-15%，2027 25-45%，2028 55-75% | 70-90%，若绑定存储/网络硬件 blended 50-75% |
| 上下文内存/KV cache 外部化 | NVIDIA BlueField-4 STX/CMX、LMCache、CXL memory tier、NVMe-oF/GDS、Redis/向量库融合 | $0.2-0.7B / $0.7-1.5B / $1.5-3B | $2-6B / $6-14B / $14-28B | $15-45B / $45-100B / $100-180B | 长上下文/Agent 服务：2026 5-12%，2027 25-45%，2028 50-75% 有独立 KV/context tier | 软件 75-92%，硬件/存储 appliance 35-65%，系统方案 45-75% |
| 异构加速器 placement engine | TPU/Trainium/Maia/MTIA/AMD/NVIDIA/Groq/Cerebras 的 workload routing，Anyscale/Ray、SkyPilot、dstack、云内部调度 | $0.1-0.5B / $0.5-1.2B / $1.2-2.5B | $1-4B / $4-10B / $10-20B | $10-35B / $35-80B / $80-150B | 多加速器企业/云 AI workload：2026 <10%，2027 20-35%，2028 45-65% | 75-95%，核心算法和数据面壁垒高 |
| LPU/decode 加速和 premium inference runtime | NVIDIA/Groq LPX、GroqCloud、Cerebras/SambaNova/Tenstorrent/Etched/d-Matrix 专用推理 runtime | $0.2-1B / $1-2.5B / $2.5-5B | $3-12B / $12-28B / $28-55B | $15-60B / $60-150B / $150-300B | premium reasoning、低延迟语音/代码/agent：2026 2-6%，2027 10-25%，2028 25-45% | 芯片/云 blended 35-65%；runtime/support 80-95%；供不应求时溢价高 |
| power-aware / capacity-aware scheduler | NVIDIA DSX Max-Q/Flex、Emerald AI、Schneider/ETAP/AVEVA、Vertiv、园区 EMS 与 workload scheduler 联动 | $0.05-0.3B / $0.3-0.8B / $0.8-1.5B | $0.8-3B / $3-8B / $8-15B | $8-30B / $30-80B / $80-160B | 新建 AI campus：2026 <10%，2027 20-35%，2028 45-70% | 软件 75-95%；设施控制系统 35-60%；节电/削峰收益可做 success fee |
| AI workload 金融化/残值调度 | reserved GPU capacity、GPU lease/residual risk、capacity marketplace、DGX Cloud Lepton、CoreWeave/Oracle/Microsoft 合同层 | $0.05-0.2B / $0.2-0.5B / $0.5-1B | $0.5-2B / $2-6B / $6-12B | $5-20B / $20-60B / $60-120B | Neocloud 和企业长期 capacity：2026 5-10%，2027 15-30%，2028 35-55% 需要金融化工具 | 软件/交易平台 70-90%；资产融资收益受利率和残值风险影响大 |
| Agent sandbox/security runtime | NVIDIA OpenShell、Google GKE Agent Sandbox、Wasm/Kata/Firecracker、policy-based network/privacy guardrails | $0.1-0.5B / $0.5-1B / $1-2B | $1-5B / $5-12B / $12-25B | $8-30B / $30-80B / $80-160B | 企业 agent workloads：2026 5-15%，2027 25-45%，2028 50-75% 需要隔离 sandbox | 80-95%；安全认证和合规可强定价 |

### 3.1 未来快速增长产品的共同特征

未来两年高增长产品几乎都有三个共同点：第一，它能直接提升 GPU/ASIC 利用率或降低 P99 latency；第二，它拥有跨层数据，比如 topology、KV cache、request trace、power cap、tenant quota；第三，它能嵌入客户生产流程，形成切换成本。单纯“更快一点的 kernel”会被开源吸收；能把 kernel、scheduler、cache、网关、计费和 SLA 串起来的平台才有长期定价权。

## 4. 供给侧：产能、瓶颈、成本与毛利

### 4.1 产能结构

| 供给类别 | 地区/公司集中度 | 关键工艺/能力 | 2026 供给判断 |
|---|---|---|---|
| 硬件耦合 runtime | 美国：NVIDIA、AMD、Intel；云厂商 Google/AWS/Microsoft/Meta；中国：华为、阿里、百度 | CUDA/TensorRT/ROCm/Neuron/XLA/Maia/CANN，驱动、kernel、compiler、profiling | NVIDIA 生态最强；AMD/ROCm 因 MI350/MI450 和 vLLM ROCm 优化改善；TPU/Trainium/Maia 多为云内闭环 |
| Kubernetes AI 调度 | 美国/以色列：NVIDIA Run:ai；Google/Red Hat/IBM/Kubernetes SIG；中国云厂商本地栈 | CRD、scheduler extender、DRA driver、quota/fair sharing、topology | 开源标准由 CNCF/K8s 推动，商业化由 NVIDIA、Red Hat、云厂商和 neocloud 兑现 |
| Slurm/HPC 调度 | 美国 SchedMD、CoreWeave SUNK、AWS HyperPod、各国家实验室/高校 | Slurm 作业队列、gang scheduling、节点健康、MPI/NCCL 集成 | 前沿训练仍离不开 Slurm；混合 K8s 是 2026-2027 增量 |
| 推理 runtime/serving | 美国：NVIDIA、vLLM/Inferact、Anyscale、Baseten、Fireworks、Together、Hugging Face；中国：阿里、百度、字节、华为；韩国/欧洲若干初创 | attention kernel、batching、KV cache、量化、OpenAI API、gateway、observability | 开源创新快，商业化靠托管平台和企业支持；NVIDIA 在高端 NVIDIA GPU 上强定价 |
| KV/context memory | NVIDIA STX、LMCache、VAST/WEKA/DDN/Dell/HPE/NetApp/Pure、CXL/Astera/Marvell/Broadcom | KV cache movement、RDMA/NIXL/UCX、NVMe-oF、CXL、GDS | 2026 供给偏方案/试点，2027 才会有标准化 appliance |
| 中国替代生态 | 华为 CANN/MindSpore/ModelArts、阿里 PAI/EAS、百度 Paddle/Kunlun、寒武纪、字节火山引擎 | 国产 accelerator runtime、编译器、分布式训练、推理服务 | 受出口管制和国产芯片路线驱动，软件适配工作量大，客户锁定强 |

### 4.2 供给瓶颈

1. **系统软件人才短缺**：懂 GPU kernel、RDMA、Kubernetes scheduler、分布式系统、LLM inference、compiler 的工程师极少，优秀团队集中在 NVIDIA、云厂商、AI labs 和少数初创。
2. **硬件拓扑碎片化**：H100/H200/B200/GB200/GB300/Rubin、MI300/MI350/MI450、TPU、Trainium、Maia、MTIA、Ascend 的 memory、interconnect、driver 和 failure mode 都不同，通用调度难度高。
3. **多租户隔离和 SLA 难以同时满足**：MIG、time-slicing、GPU fractions 可以提升利用率，但 memory OOM、noisy neighbor、side-channel、P99 latency 会影响企业生产。
4. **KV cache 和上下文内存观测不足**：很多平台只看 GPU utilization，不知道 cache hit、prefix sharing、prefill/decode contention、model cold start，导致调度目标函数不完整。
5. **网络和存储硬件准备不足**：disaggregated serving 需要 RDMA/RoCE/UCX/NIXL、NVMe-oF、CXL、GDS 的稳定组合；大多数企业网络离这个状态还有距离。
6. **模型快速迭代导致 runtime 维护成本高**：MoE、MLA、hybrid SSM、video diffusion、多模态、structured generation、long context 都需要新 kernel 和新调度策略。
7. **企业认证/合规周期长**：金融、医疗、政府客户需要审计、数据隔离、SLA、可解释成本归因和安全 sandbox，开源 runtime 不能直接进生产。
8. **power/cooling 数据没有接入 workload scheduler**：AI 负载有毫秒到分钟级功率波动，但调度系统通常只理解 GPU，不能理解 UPS、BESS、rack power cap、热容量。

### 4.3 成本结构和毛利决定因素

| 产品类型 | 单位成本/BOM 拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 调度软件 license/企业支持 | R&D 45-65%；benchmark/测试 GPU 10-20%；SRE/support 10-20%；销售/渠道 10-20% | 是否绑定 GPU 规模、是否拥有 telemetry、是否进入客户生产流程 | 按 GPU/accelerator 数、集群规模、节省的闲置成本或云 spend take-rate 定价 |
| 托管推理平台 | GPU/ASIC compute 45-75%；HBM/存储/带宽 5-15%；SRE 5-10%；runtime/平台 5-15%；客户支持和销售 10-20% | GPU 利用率、token price、reserved capacity 成本、模型路由能力 | token 单价下降时通过更高利用率保毛利；高峰容量稀缺时收 premium tier |
| 推理 runtime 企业发行版 | R&D/kernel/compiler 50-70%；CI benchmark 10-20%；support 10-20%；文档/生态 5-10% | 性能领先幅度、硬件适配深度、企业 SLA、模型兼容范围 | 以 AI Enterprise subscription、per-GPU license、support contract 或 cloud marketplace 体现 |
| KV cache/context memory 软件 | R&D 45-65%；高速网络/存储测试 15-25%；SRE/support 10-20% | cache hit rate、TTFT/P99 改善、跨节点数据一致性 | 按节省的 HBM/GPU 资源、长上下文 premium revenue 或 storage attach 定价 |
| AI Factory power-aware scheduler | 软件/控制算法 40-60%；设施集成/现场调试 20-35%；传感器/接口 5-15%；支持 10-20% | 能否在固定 MW 下多跑 GPU、能否通过并网审查、能否削峰 | 按 MW/GW、节电收益分成、capacity 解锁收益、EPC/EMS license 定价 |

供不应求时，调度/运行时供应商的定价逻辑很强：客户不是为软件本身付费，而是为避免数亿美元 GPU 闲置、降低 token 亏损、缩短模型上线时间、通过 enterprise SLA 付费。最强的毛利来自纯软件控制面，最弱的是重资产 GPU 转租；但重资产平台如果能长期锁电、锁客户、锁 GPU 并拥有调度软件，ROIC 也会显著高于普通租赁。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 层级 | 头部集中度判断 | 关键公司/项目 | 结构判断 |
|---|---|---|---|
| NVIDIA GPU runtime/control plane | 高。NVIDIA 在高端 GPU 出货和 CUDA 生态中占绝对优势 | NVIDIA Dynamo、NIM、TensorRT-LLM、Triton、Run:ai、GPU Operator、DSX | NVIDIA 可以把免费开源入口变成硬件/企业支持/云服务粘性 |
| 开源 LLM serving | 中等集中，vLLM/SGLang/TGI 是主线，项目迭代快 | vLLM、SGLang、Hugging Face TGI、LMCache、Ray Serve、KServe | 技术影响力高但直接收费低，商业化在云服务和支持层 |
| Kubernetes AI 调度标准 | 分散但标准趋同 | Kueue、JobSet、DRA、Gateway API Inference Extension、llm-d、Volcano、YuniKorn | CNCF/K8s 会降低底层差异，商业价值转向发行版、集成和 SLA |
| 云厂商私有调度 | 极高集中，云内闭环 | Google DWS/AI Hypercomputer、AWS HyperPod/Neuron、Azure Maia/AKS/Foundry、OCI | 不一定外售，但影响行业架构和客户采购标准 |
| Neocloud 平台软件 | 头部集中度上升 | CoreWeave Mission Control/SUNK、Lambda、Crusoe、Nebius、Nscale、Vultr、RunPod | 赢家需要长期客户合同、电力、融资、软件，不只是 GPU 数量 |
| 托管推理平台 | 快速分散后再整合 | Baseten、Fireworks、Together、DeepInfra、Replicate、Anyscale、Modal、Predibase | 增速快，未来可能被云厂商/NVIDIA/模型公司收购或压价 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| Kernel/runtime 性能 | tokens/sec、TTFT、P99、HBM 占用、GPU goodput，可差 20%-300% | 推理服务的 COGS 主要是算力；性能差距直接变成毛利差距 |
| 拓扑感知调度 | NVLink/NVSwitch/RDMA locality、all-reduce bandwidth、job startup time、failure recovery | 大训练/推理作业如果放错拓扑，昂贵 GPU 会低效运行，客户愿意为确定性付费 |
| Multi-tenant fairness 和 quota | 闲置 GPU 小时、排队时间、borrowed quota、preemption 成功率 | 企业和云平台必须向不同团队分摊成本，没有公平/归因就难以扩大集群 |
| KV cache 数据面 | cache hit rate、cache transfer bandwidth、TTFT/P99 改善、GPU memory saved | 长上下文和 agent 服务的最大瓶颈之一是 KV；控制 cache 就控制延迟和成本 |
| 硬件认证和驱动适配 | 支持 GPU/TPU/Trainium/ROCm/Ascend 数量，版本升级延迟，稳定运行小时 | 客户不会把生产模型放到未经验证的 runtime；认证缩短上线周期 |
| 可观测性和成本归因 | 每模型/租户/endpoint 的 token、GPU-second、cache、latency、错误率 | CFO/平台团队需要成本归因才能扩大 AI 预算；这形成强粘性 |
| Enterprise security/SLA | RBAC、SSO、审计、数据隔离、sandbox、合规证书、99.9%+ SLA | 金融、医疗、政府客户的核心采购门槛，不是开源项目能单独满足 |
| 生态和 API | OpenAI-compatible API、K8s CRD、Terraform、Helm、LangChain/LlamaIndex 集成 | API 一旦嵌入应用和 CI/CD，切换成本高，供应商可持续收费 |

### 5.3 哪一层最可能有长期高 ROIC/高毛利

最强位置排序：

1. **硬件耦合 runtime/control plane**：NVIDIA Dynamo/NIM/Run:ai/AI Enterprise 是最强，原因是它同时掌握 GPU、driver、network、DPU、kernel、enterprise channel。增量软件毛利可达 85%-95%。
2. **云厂商内部 AI Hypercomputer 控制面**：Google/AWS/Microsoft/Meta 虽不一定外售，但通过调度和运行时把自研 ASIC 价值最大化，ROIC 体现在云毛利和芯片替代 GPU 的节省。
3. **托管推理平台**：Baseten/Fireworks/Together/Anyscale/CoreWeave Dedicated Inference 如果能把 GPU 利用率做到显著高于客户自建，并锁定开发者 API，毛利可从 35%-55% 上移到 60%-75%。
4. **KV cache/context memory 软件**：这是 2027 的潜在高 ROIC 层。客户愿意为低 TTFT、长上下文和少用 HBM 付费，且数据面一旦形成不易替换。
5. **纯开源引擎维护公司**：技术影响力高，但需要转化为托管平台、企业支持或云 marketplace，否则价值容易被云厂商和硬件厂吸收。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点 1：Dynamo 1.0、llm-d、DRA/Kueue 把推理运行时平台化

2026-03 NVIDIA 宣布 Dynamo 1.0 production；同月 llm-d 加入 CNCF Sandbox；Kubernetes DRA 已进入 GA 路线，Kueue/JobSet 变成 AI batch 和 distributed training 的标准组件。这个组合意味着“推理服务”不再是单机 vLLM 进程，而是 Kubernetes/AI Factory 级的分布式控制面。

最可能放量：NVIDIA Dynamo/NIM、Run:ai、Kueue/DRA、OpenShift AI + llm-d、KServe/Gateway API Inference Extension。

### 拐点 2：推理和 agent workload 超过训练成为新增调度压力

Gartner 和 Deloitte 的预测都指向推理在 2026 成为主要 compute 消耗。Agentic workload 有长上下文、多轮、工具调用、代码沙箱、检索和验证，调度目标从“排队跑完训练 job”变成“在 P99 SLA 下动态路由数百万请求”。这会推动 KV cache-aware routing、prefix cache、continuous batching、autoscaling、模型路由、sandbox runtime 放量。

最可能放量：vLLM/SGLang commercial support、LMCache、TensorRT-LLM KV connector、Ray Serve/Anyscale、Baseten/Fireworks/Together/DeepInfra。

### 拐点 3：GW 级订单把调度从 GPU 层推到容量/电力层

OpenAI/Broadcom 10GW、Meta/AMD 6GW、Meta/Broadcom >1GW、CoreWeave backlog $66.8B 和 3.1GW+ contracted power、NVIDIA/CoreWeave 5GW by 2030，都说明容量规划已经进入 GW 单位。2026 年客户不仅要调度 job，还要调度电力、机房、区域、合规、资本开支和残值。

最可能放量：Google DWS/Flex-start、AWS HyperPod task governance、CoreWeave Mission Control/SUNK、DGX Cloud Lepton、DSX/Power-aware scheduler。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点 1：Rubin/MI400/TPU8/Trainium3/Maia/MTIA 让异构调度变成刚需

2026 仍主要是 Blackwell/GB300 和少量自研 ASIC 并行；2027 则会有 Rubin、MI400/MI455X Helios、TPU8、Trainium3/4、Maia200、MTIA 400/450/500、OpenAI/Broadcom XPU 同时放量。企业和云平台会从“单一 NVIDIA fleet”转成“按 workload 选择硬件”的调度问题。

最可能放量：异构 placement engine、跨硬件 benchmark/router、Ray/Anyscale、SkyPilot/dstack、云厂商私有 scheduler、NVIDIA NVLink Fusion 相关生态。

### 拐点 2：Prefill/decode 分离和 KV/context memory 成为高端推理默认架构

2027 的 agent 服务会更多面向百万 token context、视频/多模态、长链路工具调用和企业记忆库。单机 HBM 无法承担所有 KV cache；prefill、decode、cache、embedding、retrieval、reranking 将在不同资源池之间调度。

最可能放量：Dynamo + NIXL、llm-d、LMCache、BlueField-4 STX/CMX、CXL memory pooling、NVMe-oF/GDS、storage-aware scheduler。

### 拐点 3：调度软件进入“token revenue/GW”时代

当 AI campus 以 GW 计价，限制因素变成电力、冷却、网络和上电节奏。2027 新建 AI Factory 会要求在固定 power cap 下最大化 token revenue，并能根据电价、BESS、并网约束和客户 SLA 调整 workload。调度软件会从 IT 工具变成能源和金融控制面。

最可能放量：DSX Max-Q/Flex、power-aware Kubernetes scheduler、AI workload financial infrastructure、reserved capacity marketplace、GPU lease/residual risk 管理。

## 8. 头部公司与细分地图

### 8.1 芯片和硬件 runtime 生态

- NVIDIA：CUDA、TensorRT-LLM、Triton、NIM、Dynamo、Run:ai、GPU Operator、DRA Driver、BlueField/STX、DSX、DGX Cloud Lepton。
- AMD：ROCm、AITER、MI300/MI350/MI450/Helios runtime，ROCm-vLLM 适配，Pensando/Vulcano NIC。
- Google：TPU/XLA/JAX/JetStream/vLLM on TPU、AI Hypercomputer、DWS、GKE Inference Gateway、TPU 8t/8i。
- AWS：Neuron、Trainium/Inferentia、SageMaker HyperPod、EKS/Slurm、EFA、Trainium3/4。
- Microsoft：Maia 100/200、Azure AI Foundry、AKS、ONNX Runtime、DeepSpeed、Triton/vLLM/NIM 集成。
- Meta：MTIA、PyTorch、TorchAO、vLLM/LLM serving 贡献、OCP rack、与 AMD/Broadcom/Arm 的定制硅路线。
- Broadcom/OpenAI：OpenAI custom accelerator、XPU platform、Ethernet/SerDes/NIC/switch、10GW 2026H2-2029 路线。
- 中国：华为 CANN/MindSpore/ModelArts/Ascend、阿里 PAI/PAI-EAS/T-Head、百度 PaddlePaddle/Kunlun、字节火山引擎、寒武纪 MLU、壁仞、沐曦、摩尔线程、燧原、天数智芯、海光 DCU。
- 专用推理/替代架构：Groq/LPU、Cerebras、SambaNova、Tenstorrent、d-Matrix、Etched、MatX、Rebellions、Furiosa、Positron、Ampere、ZeroPoint。

### 8.2 集群调度和资源管理

- 商业/云：NVIDIA Run:ai、AWS SageMaker HyperPod、Google DWS/Flex-start、Azure CycleCloud/AKS/Batch、OCI Supercluster、CoreWeave Mission Control/SUNK、Lambda、Crusoe、Nebius、Nscale、Vultr、RunPod。
- 开源/标准：Kubernetes DRA、Kueue、JobSet、Volcano、Apache YuniKorn、KubeRay、KServe、Gateway API Inference Extension、llm-d、Slurm/SchedMD、Armada、Kubeflow Trainer、Ray。
- 工具和平台：Anyscale、SkyPilot、dstack、Modal、BentoML、Predibase、Weights & Biases、Databricks/MosaicML、HPE Private Cloud AI、Dell AI Factory、Red Hat OpenShift AI、VMware Tanzu。

### 8.3 推理运行时和模型服务

- NVIDIA 线：TensorRT-LLM、Triton Inference Server、NIM、Dynamo、NIXL、NeMo、AI Enterprise。
- 开源高性能线：vLLM、SGLang、Hugging Face TGI、LMCache、Ray Serve、KServe、BentoML/OpenLLM、llama.cpp/Ollama（边缘和小规模）、DeepSpeed-MII。
- 托管推理平台：Baseten、Fireworks AI、Together AI、DeepInfra、Replicate、Anyscale、Modal、RunPod Serverless、CoreWeave Dedicated Inference、Predibase/LoRAX、Cerebras Inference、GroqCloud、SambaNova Cloud。
- 网关/可观测/成本：LangSmith/LangChain、Helicone、Portkey、Arize、WhyLabs、Datadog、Grafana/Prometheus/OpenTelemetry、Weights & Biases、Kong/Envoy/NGINX/F5、Cloudflare Workers AI（边缘/网关）。

### 8.4 KV cache、存储和上下文内存

- KV/cache 软件：LMCache、vLLM KV offload、SGLang RadixAttention、TensorRT-LLM KV connector、Dynamo/NIXL、Redis、Alluxio、JuiceFS、Ray Data。
- AI storage：VAST Data、WEKA、DDN、Dell、HPE、IBM Storage、NetApp、Pure Storage、Qumulo、MinIO、Ceph、NVIDIA BlueField-4 STX/CMX。
- CXL/内存/连接：Astera Labs、Rambus、Marvell、Broadcom、Microchip、Montage、Samsung、SK hynix、Micron、Intel、CXL Consortium。

### 8.5 投资优先级

1. **最确定**：NVIDIA runtime/control plane、Run:ai、NIM/Dynamo、Kubernetes DRA/Kueue/llm-d 生态、云厂商 HyperPod/DWS、CoreWeave/SUNK。
2. **弹性最大**：托管推理平台、KV cache/context memory、prefill/decode disaggregation、异构 accelerator scheduler、power-aware scheduler。
3. **需要验证**：专用 LPU/推理 ASIC runtime、GPU 金融化/残值工具、CXL memory pooling、跨云/跨硬件自动 placement。

## 9. 关键数字清单

- Gartner：2026 AI-optimized IaaS spending **$37.5B**，其中 **55%** 支持 inference。
- Deloitte：2026 inference workloads 约占 AI compute **2/3**；inference-optimized chips 超过 **$50B**。
- IDC：2026 AI infrastructure spending **$487B**，约 **+53% YoY**；2029 年超过 **$1T**。
- CNCF：容器用户 **82%** 在生产使用 Kubernetes；GenAI 模型托管组织中 **66%** 用 Kubernetes 管理部分或全部 inference workload。
- NVIDIA：Dynamo 1.0 于 2026-03 发布，官方列出 AWS、Azure、Google Cloud、OCI、CoreWeave、Together、Nebius、Baseten、DeepInfra、Fireworks、Cursor、Perplexity 等采用/集成。
- Run:ai：支持 Kubernetes AI workload scheduling、GPU fractions、time-slicing、quota/fairness、topology-aware scheduling。
- AWS：HyperPod task governance 2026-03 支持 idle resource sharing；Trn3 UltraServer 最高 **144** 颗 Trainium3、**362 FP8 PFLOPs**、**20.7TB HBM3E**。
- Google：TPU 8t/8i 于 Cloud Next 2026 发布，训练/推理芯片分化；Ironwood TPU 每芯片 **192GB HBM**、**7.37TB/s**。
- Microsoft：Maia 200 使用 TSMC 3nm、**216GB HBM3E**、**7TB/s**、**272MB SRAM**，目标推理经济性。
- Meta：MTIA 300 已生产，MTIA 400/450/500 将在 2026-2027 迭代，主要支持 GenAI inference。
- OpenAI/Broadcom：10GW custom AI accelerator，Broadcom 目标 2026H2 开始部署，2029 年底完成。
- Meta/Broadcom：初始超过 **1GW** custom silicon，未来多 GW。
- AMD/Meta：最高 **6GW** AMD Instinct GPUs，首个 1GW 2026H2 开始出货，基于 MI450/Helios。
- CoreWeave：2025 年收入超过 **$5B**，revenue backlog **$66.8B**；平台披露 **3.1GW+** contracted power capacity。

## 10. 主要来源

| 来源 | 用途 |
|---|---|
| [NVIDIA Dynamo 1.0 press release](https://nvidianews.nvidia.com/news/nvidia-enters-production-with-dynamo-the-broadly-adopted-inference-operating-system-for-ai-factories) | Dynamo 1.0、采用方、AI Factory 推理 OS |
| [NVIDIA Dynamo technical blog](https://developer.nvidia.com/blog/nvidia-dynamo-1-production-ready/) | 多节点推理、7x throughput、P/D 与 agentic inference 优化 |
| [NVIDIA Run:ai product page](https://www.nvidia.com/en-us/data-center/nvidia-run-ai/get-started/) | Run:ai Kubernetes GPU orchestration、利用率和 workload 支持 |
| [Run:ai Scheduler docs](https://run-ai-docs.nvidia.com/saas/platform-management/runai-scheduler/scheduling/how-the-scheduler-works) | fairness、quota、dynamic balancing、topology-aware scheduling |
| [Run:ai GPU Fractions docs](https://run-ai-docs.nvidia.com/guides/platform-management/runai-scheduler/resource-optimization/fractions) | GPU fractions、time-slicing、memory sharing |
| [Kubernetes DRA docs](https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/) | DRA stable、DeviceClass/ResourceClaim、GPU 等设备分配 |
| [Kubernetes DRA GA blog](https://kubernetes.io/blog/2025/09/01/kubernetes-v1-34-dra-updates/) | v1.34 DRA GA 与 specialized hardware 管理 |
| [NVIDIA DRA Driver donation](https://blogs.nvidia.com/blog/nvidia-at-kubecon-2026/) | NVIDIA 向 CNCF 捐赠 DRA GPU driver |
| [Kueue official site](https://kueue.sigs.k8s.io/) | batch/HPC/AI/ML job queueing、multi-tenant quotas |
| [Kueue GitHub](https://github.com/kubernetes-sigs/kueue) | fair sharing、cohorts、preemption、RayJob/JobSet 支持 |
| [JobSet docs](https://jobset.sigs.k8s.io/docs/overview/) | 分布式训练/HPC workload Kubernetes-native API |
| [CNCF llm-d announcement](https://www.cncf.io/blog/2026/03/24/welcome-llm-d-to-the-cncf-evolving-kubernetes-into-sota-ai-infrastructure/) | llm-d 加入 CNCF、分布式推理标准化 |
| [Red Hat llm-d article](https://developers.redhat.com/articles/2025/05/20/llm-d-kubernetes-native-distributed-inferencing) | llm-d、vLLM、Inference Gateway、KV-aware routing、P/D disaggregation |
| [IBM llm-d donation](https://research.ibm.com/blog/donating-llm-d-to-the-cloud-native-computing-foundation) | llm-d 作为 vendor-neutral inference stack |
| [vLLM KV offloading connector](https://blog.vllm.ai/2026/01/08/kv-offloading-connector.html) | KV cache offload、memory transfer |
| [vLLM ROCm backend](https://blog.vllm.ai/2026/02/27/rocm-attention-backend.html) | AMD ROCm inference 优化 |
| [SGLang official site](https://www.sglang.io/) | SGLang 高性能 LLM/VLM serving |
| [SGLang NVIDIA docs](https://docs.nvidia.com/deeplearning/frameworks/sglang-release-notes/overview.html) | SGLang runtime/structured generation |
| [TensorRT-LLM docs](https://docs.nvidia.com/tensorrt-llm/index.html) | TensorRT-LLM、in-flight batching、paged attention、量化 |
| [TensorRT-LLM disaggregated serving](https://nvidia.github.io/TensorRT-LLM/1.2.0rc6/features/disagg-serving.html) | P/D disaggregated serving、KV transfer |
| [NVIDIA NIM product page](https://www.nvidia.com/en-us/ai-data-science/products/nim-microservices/) | NIM 企业推理微服务 |
| [NVIDIA NIM Operator](https://docs.nvidia.com/nim-operator/latest/index.html) | Kubernetes 上部署 NIM/NeMo 微服务 |
| [AWS HyperPod idle sharing](https://aws.amazon.com/about-aws/whats-new/2026/03/sagemaker-hyperpod-idle-resource-sharing/) | HyperPod task governance、idle resource sharing |
| [AWS HyperPod docs](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod.html) | Slurm/EKS、topology-aware scheduling、cluster orchestration |
| [AWS Trn3 UltraServer](https://aws.amazon.com/ec2/instance-types/trn3/) | Trainium3、144 chips、362 FP8 PFLOPs、HBM3E |
| [Google DWS blog](https://cloud.google.com/blog/products/compute/introducing-dynamic-workload-scheduler) | Flex Start、Calendar mode、AI Hypercomputer 调度 |
| [Google Flex-start VMs](https://docs.cloud.google.com/compute/docs/instances/about-flex-start-vms) | DWS provisioning、high-demand GPUs |
| [Google TPU 8t/8i](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era) | TPU 8t/8i、训练/推理芯片分化 |
| [Google Next 2026 recap](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/google-cloud-next-26-recap/) | AI Hypercomputer、TPU8、Vera Rubin NVL72 |
| [Microsoft Maia 200](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/) | Maia 200、HBM3E、SRAM、推理经济性 |
| [Meta MTIA roadmap](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/) | MTIA 300/400/450/500、GenAI inference |
| [Meta/Broadcom custom silicon](https://about.fb.com/news/2026/04/meta-partners-with-broadcom-to-co-develop-custom-ai-silicon/) | >1GW MTIA custom silicon、Broadcom XPU |
| [OpenAI/Broadcom 10GW](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/) | 10GW OpenAI-designed accelerators、2026H2-2029 |
| [AMD/Meta 6GW](https://ir.amd.com/news-events/press-releases/detail/1279/amd-and-meta-announce-expanded-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus) | 6GW AMD Instinct、MI450/Helios、2026H2 首批 |
| [CoreWeave FY2025 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results) | CoreWeave $5B+ revenue、$66.8B backlog |
| [CoreWeave AI infrastructure](https://www.coreweave.com/ai-infrastructure) | 3.1GW+ contracted power、40+ data centers |
| [CoreWeave Mission Control](https://www.coreweave.com/mission-control) | AI cloud observability/control plane |
| [CoreWeave SUNK](https://www.coreweave.com/blog/why-sunk-redefines-the-ai-research-cluster-for-production-grade-training) | Slurm on Kubernetes、training/inference 共存 |
| [Anyscale LLM serving docs](https://docs.anyscale.com/llm/serving) | Ray Serve + vLLM + Anyscale infrastructure management |
| [Baseten Series E](https://www.baseten.co/blog/announcing-baseten-s-300m-series-e/) | $300M Series E、$5B valuation、推理平台融资 |
| [Gartner AI-optimized IaaS](https://www.gartner.com/en/newsroom/press-releases/2025-10-15-gartner-says-artificial-intelligence-optimized-iaas-is-poised-to-become-the-next-growth-engine-for-artificial-intelligence-infrastructure) | 2026 AI-optimized IaaS $37.5B、55% inference |
| [Deloitte 2026 AI compute](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html) | 推理占 compute 2/3、inference chips >$50B |
| [IDC AI infrastructure 2026](https://www.idc.com/resource-center/blog/ai-infrastructure-spending-caps-historic-year-at-90-billion-in-q4-2025-2029-spending-to-eclipse-1-trillion/) | AI infra 2026 $487B、2029 >$1T |
| [CNCF 2026 cloud native survey](https://www.cncf.io/announcements/2026/01/20/kubernetes-established-as-the-de-facto-operating-system-for-ai-as-production-use-hits-82-in-2025-cncf-annual-cloud-native-survey/) | K8s 82% production、66% GenAI inference |
| 项目内文件：`D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md` | 2026-2027 AI 芯片出货量最大平台和路线假设 |

# 行业调研：【AI芯片先进封装】

> 截至日期：2026-05-08  
> 研究口径：本报告研究 AI 数据中心加速器相关的先进封装产业链，包括 CoWoS/2.5D、SoIC/3D、EMIB/Foveros/I-Cube/X-Cube、HBM 堆叠与 HBM base die、ABF/玻璃/高阶载板、TCB/混合键合、KGD/ATE/探针卡/老化测试、先进封装材料、封装 EDA/IP/DFT/SLM，以及与 CPO/硅光、chiplet、UCIe 绑定的封装增量。  
> 预测原则：对 2026-2027 AI 基础设施建设采用明显乐观假设。凡缺少直接公开数字的细分项，用“AI 芯片出货、HBM stack、CoWoS 产能、资本开支、头部客户订单”做大胆推演，并明确为估算。

## 0. 一页结论

AI 芯片先进封装在 2026 年的投资价值不是“传统封测复苏”，而是“AI 算力供给的闸门”。先进节点、HBM、CoWoS/EMIB、ABF 载板、TCB/混合键合、KGD 测试和液冷/供电机械边界共同决定 GB300、Rubin、MI400、Trainium、TPU、MTIA、Maia、OpenAI/Broadcom XPU 能不能变成可交付机架。

最核心判断：

| 判断 | 结论 |
|---|---|
| 2026 主流技术路径 | CoWoS-L/CoWoS-S + HBM3E + 大尺寸 ABF + TCB + KGD 测试；GB300/B300、GB200/B200、MI350、TPU Ironwood、Trainium2/3、Maia200、MTIA 300/400 是主要拉动。 |
| 2026 新技术切入 | HBM4、CoWoS-L 大版图、SoIC/混合键合、CPO switch package、UCIe 3.0 设计导入、Intel EMIB-T/Samsung I-Cube/X-Cube 作为替代产能开始被客户认真验证。 |
| 2027 主线 | HBM4 从验证转向放量；Rubin/MI400/TPU8/MTIA 450/500/OpenAI XPU 带动 CoWoS-L、EMIB-T、SoIC、3DIC EDA、HBM tester 和高阶载板进入二次紧缺。 |
| 最大瓶颈 | 不是单一 CoWoS wafer start，而是“HBM KGD + 中介层/桥接 + 大尺寸载板 + TCB/HB 设备 + 测试老化 + 机械翘曲/热应力 + 客户认证”组成的复合瓶颈。 |
| 最强定价权 | TSMC CoWoS/SoIC 与先进节点组合、HBM 三巨头、TCB/混合键合/ATE/探针卡设备、ABF 高阶载板和先进封装 EDA/IP。 |
| 2026-2028 AI 先进封装 TAM 推演 | 2026：$32-55B；2027：$55-95B；2028：$85-150B。这里指 AI 加速器强相关的高端封装服务、载板、HBM 组装/封装、封装测试、核心设备与材料，不含完整 HBM 存储芯片销售额。 |

关键事实锚点：

- TSMC 1Q26 营收 $35.9B、毛利率 66.2%、HPC 占营收 61%，并把 2026 capex 指向 $52-56B 区间高端；公司称 AI demand extremely robust，并在 N3 扩产中明确包括 HBM base dies。  
- TSMC 电话会 Q&A 直接承认 advanced packaging “very tight”，并把 AI super chips 的大 die、warpage、thermal limitation 作为主要工程挑战。  
- NVIDIA GTC 2026 宣布 Vera Rubin 七类芯片 full production、合作伙伴 2026H2 可用；GB300 NVL72 单 GPU 最高 288GB HBM3E，Rubin 转向 HBM4。  
- AMD 与 Meta 宣布最高 6GW AMD Instinct GPU 多代部署，首个 1GW 从 2026H2 交付；AMD 与 Samsung 签署 HBM4 合作，MI455X 绑定 HBM4。  
- Meta 披露 MTIA 300/400/450/500 四代芯片两年内开发和部署，Broadcom/Meta 2026 年 4 月公告首期超过 1GW、多 GW 路线。  
- OpenAI/Broadcom 宣布 10GW OpenAI 自研加速器，Broadcom 机架系统计划 2026H2 开始部署，2029 年完成。  
- Besi 1Q26 订单 EUR269.7M，同比 +104.5%，主要由 hybrid bonding、mobile、photonics 拉动；ASMPT 1Q26 称 AI 推动 TCB/HB、HBM4 16H 资格认证和 embedded bridge die bonding 订单。

## 1. AI 芯片路线对先进封装的直接拉动

### 1.1 项目内已有出货量最大芯片路径摘要

以下芯片路径来自项目内 `ai_chip_research_2026_2027.md` 与会议更新材料，本节只把其对先进封装的含义抽出来。

| 2026-2027 出货/价值权重最高平台 | 先进封装路径 | 对产业链的含义 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | TSMC 4NP + CoWoS-L/S + HBM3E，GB300 NVL72 机架级液冷 | 2026 最大收入池，拉动 CoWoS-L、ABF 大尺寸载板、HBM3E KGD、NVLink/NVSwitch 测试、冷板接口。 |
| AWS Trainium2 | 定制 ASIC + HBM + NeuronLink scale-up，64 芯片 UltraServer | 自用 ASIC 不一定公开到 OSAT，但消耗 HBM、先进封装、系统级 burn-in 和 rack integration。 |
| Google TPU v7 Ironwood | Broadcom/Google 定制 XPU + 2.5D/HBM3E，192GB HBM、7.37TB/s | 推理优先 ASIC 放量，验证 Broadcom XPU 平台对 CoWoS/高级载板/以太网封装的长期需求。 |
| NVIDIA B200/GB200 | CoWoS + HBM3E，NVL72 规模交付 | 存量大，2026 仍占 CoWoS 与 HBM3E 大量产能。 |
| Huawei Ascend 910C/950 | 中国本土先进封装 + HBM/高带宽内存替代 + 超节点互连 | 受制于先进节点和 HBM，但会推动本土 2.5D、载板、OAM、测试和液冷生态。 |
| Cambricon MLU 590/690 | SMIC 可得先进节点 + HBM/OAM + 本土封装 | 规模可能大于收入弹性，本土封装良率和 KGD 测试决定实际交付。 |
| AMD MI350 | TSMC 先进节点 + 2.5D + HBM3E，PCIe/OAM/UBB 多形态 | 2026 AMD 最确定放量产品，拉动 CoWoS/等价 2.5D、UBB 载板、ROCm 系统测试。 |
| AWS Trainium3 | 3nm + HBM3E，144 芯片 UltraServer | 2026-2027 从 Trainium2 接棒，强化 ASIC 与系统级封装协同。 |
| Meta MTIA 300/400/450/500 | Broadcom XPU 平台，chiplet/标准化机架，推理优先 | 2026 首期超 1GW，2027 多 GW，先进封装需求从 NVIDIA 外溢到定制 ASIC。 |
| Microsoft Maia 200 | TSMC 3nm + HBM3E + 先进封装，216GB HBM3E、7TB/s | Azure 内部推理量产导入，验证“云厂 ASIC + HBM + 液冷”成为主流。 |
| 补充：NVIDIA Rubin/AMD MI400/OpenAI-Broadcom XPU | HBM4 + CoWoS-L/SoIC/EMIB-T/大尺寸载板 | 2026H2 小批量，2027 放量，是 HBM4、TCB/HB、CoWoS-L 和载板二次紧缺的主因。 |

### 1.2 2026 最可能的技术路径

2026 年最可能大量出货的不是最激进的 3D 封装，而是“成熟 2.5D 平台的极限放大”：

1. CoWoS-L/CoWoS-S + HBM3E：GB300/B300、GB200/B200、MI350、TPU/Trainium/ASIC 存量与新增共同拉动。  
2. 大尺寸 ABF 载板 + 低翘曲材料 + 高可靠 underfill/mold：package 版图扩大后，载板良率比单价更重要。  
3. TCB 与 HBM KGD 测试：HBM stack 数量、12-high/16-high、HBM4 early ramp 让 bonding 和 test 成为非显性瓶颈。  
4. 系统级封装验证：SerDes/NVLink/UALink/NeuronLink、PCIe 6/7、CXL、液冷和机架 burn-in 进入同一验证链路。  
5. OSAT 承接外溢：ASE、Amkor、JCET 等能拿到更多 2.5D/FOWLP/SiP/测试外包，但最高端 CoWoS 仍由 TSMC 主导。

### 1.3 技术成熟与放量时间表

| 技术 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 基准 | 2027 乐观/极度超预期 |
|---|---|---|---|---|---|
| CoWoS-S/CoWoS-L 2.5D | 成熟且满载，GB300/B300 是主力 | OSAT 承接周边工序，CoWoS-L 良率改善 | 客户预付款锁定更多产能，月产能有效产出超预期 | Rubin/MI400/ASIC 继续吃满 | CoWoS-L 成为 AI XPU 默认封装，单价不降反升。 |
| HBM3E 封装/TCB | 主力收入源，12-high 稳定 | 16-high 部分产品稳定 | HBM3E 价格高位维持至年底 | 被 HBM4 逐步替代但仍大量出货 | 作为中端推理芯片主力延续到 2028。 |
| HBM4/HBM4E | 2026H2 Rubin/MI400/TPU8/ASIC 早期导入 | 三大厂验证顺利，Q4 贡献明显 | HBM4 成为高端新增订单默认选项 | 进入主力放量 | HBM4E 提前锁单，HBM4 stack ASP 和毛利维持高位。 |
| SoIC/混合键合 D2W/W2W | 逻辑堆叠仍偏少数高端项目，HBM/3D memory 先用 | 3D cache、chiplet、HBM base die 协同增加 | 若客户接受良率风险，2026H2 出现高端 ASIC 量产案例 | 先进 AI package 中渗透率升至 10-20% | 2028 前成为高端 chiplet 的关键差异化。 |
| Intel EMIB-T/Foveros | 2026 以客户验证和少量 design-in 为主 | Google/AWS/Broadcom 类客户分流部分 CoWoS | 若 CoWoS 太紧，EMIB-T 获得急单 | 2027 商用份额提升到 5-10% | 作为第二供应源拥有战略溢价。 |
| Samsung I-Cube/X-Cube/turnkey | HBM4 + foundry + advanced packaging 组合切入 AMD 等客户 | AI memory 绑定封装提高议价 | 若 NVIDIA/AMD/ASIC 多供成功，份额快速上行 | 2027 成为 TSMC 之外最重要替代之一 | 先进封装和 HBM 一体化有较强定价权。 |
| CoPoS/面板级/玻璃载板 | pilot 和客户评估 | 2026H2 小规模 qualification | 特定 ASIC 试产 | 2027 仍以试产和认证为主 | 极度乐观情形下 2027H2 有小批量高端 ASIC 导入，真正放量更偏 2028-2029。 |
| CPO/photonic interposer | 交换芯片侧 pilot，收入小 | Spectrum-6/SPX、Broadcom switch 侧设计加速 | 1.6T/3.2T 网络功耗过高迫使提前导入 | 2027 进入高端 AI switch 小批量 | package-level photonic interposer 更偏 2028 后。 |

## 2. 已经开始放量的关键产品：市场规模、渗透率、利润率

下面市场规模为该技术对应的全球收入/订单池，不等同于单一公司收入；“未来 3 个月”按 2026Q2-Q3 可确认收入和订单计，“未来 12 个月”按 2026H2-2027H1，“未来 24 个月”按 2026H2-2028H1。

| 已放量产品/技术 | 2026 当前状态 | 未来 3 个月市场规模，基准/乐观/极度乐观 | 未来 12 个月市场规模，基准/乐观/极度乐观 | 未来 24 个月市场规模，基准/乐观/极度乐观 | 渗透率路径 | 当前与未来利润率 |
|---|---|---:|---:|---:|---|---|
| AI 2.5D 封装服务，CoWoS-L/S/R 与同类 | TSMC 主导，GB300/GB200/MI350/TPU/ASIC 拉满 | $7-10B / $9-13B / $12-16B | $34-48B / $45-65B / $60-85B | $58-85B / $80-120B / $115-170B | 高端数据中心 GPU/ASIC 渗透率 2026 已 >85%，2027 维持 >90%；CoWoS-L 在大版图产品占比从 30-45% 升到 55-75%。 | TSMC/IDM 高端封装毛利估计 45-60%，OSAT 外包 22-38%；极缺时高端项目溢价 5-15%。 |
| HBM3E 封装、TCB、base die 绑定 | 2026 主力，GB300/GB200/MI350/TPU/Trainium 均依赖 | HBM 总收入 $14-20B；封装/组装价值 $2.5-4.5B | HBM $58-75B；封装/组装 $10-16B | HBM $80-115B；封装/组装 $15-25B | AI 加速器 HBM attach rate 接近 100%；HBM3E 在高端新增中从 2026 的 70-85% 降到 2027 的 35-55%。 | HBM 毛利 60-75%，领先厂 OPM 45-70%；TCB/HBM assembly 设备商毛利 55-65%。 |
| 大尺寸 ABF/BT 载板、stiffener、underfill | ABF 面积和层数随 package 版图上升 | $2.2-3.5B / $3-4.5B / $4-6B | $10-16B / $14-22B / $20-30B | $16-26B / $24-38B / $35-55B | 高端 AI package 单芯片载板面积较传统 CPU/GPU 显著放大，2026 大尺寸 AI 载板占高阶 ABF 25-35%，2027 35-50%。 | 高阶载板毛利 25-40%，供不应求时 40%+；普通 ABF 与 PCB 低得多。 |
| TCB、flip-chip、die attach、mass reflow 设备 | ASMPT/Besi/K&S 等订单受 AI/HBM 拉动 | $2.5-3.8B / $3.5-5B / $5-7B | $11-16B / $15-22B / $21-30B | $18-28B / $26-40B / $38-60B | HBM4/16H、C2W/C2S、embedded bridge bonding 使高精度 bonding 设备 attach rate 上升。 | 设备毛利 50-65%；Besi 1Q26 毛利 63.5%，ASMPT 高端 TCB/HB 具备高溢价。 |
| KGD、HBM tester、ATE、探针卡、burn-in | HBM KGD 与高速 SerDes 测试时间上升 | $1.8-2.8B / $2.5-3.8B / $3.5-5.5B | $8-12B / $11-17B / $16-24B | $13-22B / $20-32B / $30-48B | AI package 中测试成本占比从 2024 的低个位数升到 2026 的 5-8%，HBM4/CPO 后继续上行。 | ATE/探针卡/SLT 毛利 45-65%，高端探针卡和测试软件更高。 |
| 高端 OSAT 先进封装外溢 | ASE、Amkor、JCET 等承接 TSMC/Samsung/客户非核心工序 | $1.5-2.5B / $2-3.5B / $3-5B | $7-12B / $10-18B / $16-26B | $12-22B / $20-36B / $32-55B | OSAT 在 AI 2.5D/FOWLP/SiP/测试中的份额 2026 约 15-25%，2027 可到 25-35%，但最高端仍受 TSMC/IDM 控制。 | 传统 OSAT 15-25%，高端先进封装项目 25-38%；客户集中和 capex 折旧限制估值上沿。 |
| 封装 EDA、3DIC signoff、UCIe IP/VIP、SLM/DFT | 设计进入多 die/多物理场阶段 | $0.5-0.8B / $0.7-1.1B / $1.0-1.5B | $2.2-3.2B / $3.0-4.5B / $4.2-6.5B | $4-6B / $6-9B / $9-14B | 高端 XPU/AI ASIC tape-out 中 3DIC/thermal/SI/PI signoff 从可选变必选。 | 软件/IP 毛利 80-95%，经营利润 25-45%；客户切换成本极高。 |
| 硅光/CPO 相关封装、光引擎、1.6T optical package | 800G/1.6T 光模块已放量，CPO 仍早期 | 光封装/CPO $0.8-1.4B / $1.2-2.0B / $2.0-3.5B | $3-5B / $5-9B / $8-15B | $7-14B / $12-25B / $22-45B | CPO 在交换芯片侧 2026 <5%，2027 5-12%，2028 10-25%；pluggable 仍为主体。 | 光模块组装毛利 25-40%，硅光/激光/DSP 45-65%，CPO 初期良率风险高但单价高。 |
| 热界面材料、lid、封装机械件、液冷接口 | 大 package 热密度上升，封装与冷板边界耦合 | $0.8-1.3B / $1.2-1.8B / $1.8-2.8B | $3.5-5.5B / $5-8B / $7-12B | $7-12B / $10-18B / $16-30B | 高端 AI rack 液冷 attach rate 2026 40-60%，2027 60-80%；封装侧 TIM/lid 价值量同步提升。 | 材料/机械件 25-45%，高可靠 TIM/低翘曲材料可 45%+。 |

### 2.1 已放量产品的三情景增长判断

| 技术 | 基准增长 | 乐观增长 | 极度超预期乐观增长 |
|---|---|---|---|
| AI 2.5D/CoWoS | 未来 12 个月 +35-55%，主要受 GB300 与 ASIC 放量驱动 | +60-90%，Rubin/MI400 没有明显空窗 | +100%+，GW 级订单提前、客户接受溢价和预付款。 |
| HBM3E/HBM4 总体 | +45-70%，HBM4 小比例切入 | +80-120%，HBM4 多供验证顺利 | +150% 附近，推理上下文和 KV cache 需求继续吞噬内存供给。 |
| 载板/材料 | +25-45%，紧跟高端 package 面积 | +50-75%，玻璃/低翘曲材料被提前锁定 | +90%+，大 package 良率成为交付第一瓶颈。 |
| 设备/测试 | +30-55%，订单领先收入 | +60-90%，HBM4/混合键合拉动 | +100%+，客户为 2027 产能提前下单。 |

## 3. 在研和即将快速增长的关键产品

| 在研/即将放量技术 | 当前阶段 | 未来 3 个月市场规模，基准/乐观/极度乐观 | 未来 12 个月市场规模，基准/乐观/极度乐观 | 未来 24 个月市场规模，基准/乐观/极度乐观 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| HBM4/HBM4E + 16H/Custom HBM base die | Rubin/MI400/TPU8/ASIC early access，2026H2 起量 | HBM4 $1-3B / $3-5B / $5-8B | $18-30B / $30-50B / $50-75B | $55-85B / $80-125B / $120-180B | 高端新增 HBM 中 HBM4 2026 5-15%，2027 35-60%，2028 60-80%。 | 早期毛利 65-80%；Custom HBM base die 与 PHY/IP 具备额外溢价。 |
| SoIC/D2W/W2W 混合键合逻辑堆叠 | 已有 3D V-Cache/MI300 类案例，AI XPU 更大规模导入中 | $0.4-0.8B / $0.8-1.5B / $1.5-2.5B | $2-4B / $4-7B / $7-12B | $7-14B / $12-25B / $22-40B | AI accelerator 中渗透 2026 <10%，2027 10-20%，2028 20-35%。 | Foundry/设备/IP 合计毛利高；良率和返修责任是主要风险。 |
| EMIB-T/Foveros、Samsung I-Cube/X-Cube 替代 2.5D | Intel/Samsung 争取客户验证，CoWoS 过紧提供机会 | $0.3-0.8B / $0.7-1.5B / $1.5-3B | $2-4B / $4-8B / $8-15B | $8-18B / $15-30B / $30-55B | 非 TSMC AI 2.5D 份额 2026 5-10%，2027 10-20%，2028 20-35%。 | 第二供应源具备战略溢价；初期毛利不稳定，成熟后 30-45%。 |
| CoPoS/FOPLP/面板级封装 | 2026 pilot，目标降低超大 package 成本 | <$0.2B / $0.3-0.6B / $0.8-1.5B | $0.5-1.5B / $1.5-3B / $3-6B | $3-8B / $7-15B / $15-30B | 2027 前渗透 <3%；2028 若良率过关可到 5-12%。 | 早期亏损/低毛利，量产后因成本下降可捕获高 ROIC；设备材料先受益。 |
| 玻璃基板/玻璃 interposer | Intel/Samsung/Absolics/Corning 等推动，处于验证 | <$0.1B / $0.2-0.4B / $0.5-1B | $0.5-1B / $1-2.5B / $2.5-5B | $3-7B / $6-14B / $12-25B | 2026-2027 多为试产；2028 若 AI package 面积继续放大，玻璃有望进入高端路线。 | 技术壁垒高，早期资本开支重；材料和设备毛利 40-60%。 |
| UCIe 3.0 / D2D PHY / chiplet compliance | 64GT/s、RoT、management、compliance 进入设计导入 | $0.2-0.4B / $0.4-0.7B / $0.7-1B | $1-2B / $1.8-3B / $3-5B | $3-6B / $5-9B / $8-15B | 高端自研 ASIC 中 2026 design-in 渗透 20-30%，2027 40-60%，开放 marketplace 仍慢。 | IP/VIP/EDA 毛利 80-95%；标准锁定后 switching cost 极高。 |
| Photonic interposer/CPO/OIO | 交换芯片侧先行，package-level 光互连早期 | $0.1-0.3B / $0.3-0.6B / $0.6-1B | $0.7-1.5B / $1.5-3B / $3-6B | $3-8B / $7-18B / $15-35B | CPO 2026 在 AI switch 中 <5%，2027 5-12%，2028 10-25%；photonic interposer 更晚。 | 初期良率低、EBIT 不稳；核心光引擎/激光/封装毛利可 45-65%。 |
| 封装内/板级去耦、电源完整性、semi-IVR | AI 负载瞬态电流抬高，和 package co-design | $0.2-0.5B / $0.4-0.8B / $0.8-1.3B | $1.5-3B / $2.5-5B / $5-8B | $5-10B / $8-16B / $15-28B | 2026 主要用于 GB300/Rubin/MI400 高端模块，2027 进入更多 ASIC/rack reference design。 | 功率 IC/电容/封装去耦材料毛利 30-60%，认证后锁定强。 |
| wafer-scale / panel-scale AI package | Cerebras、TSMC SoW-X、科研和特定客户 | <$0.1B / $0.1-0.3B / $0.5B | $0.3-0.8B / $0.8-2B / $2-4B | $2-5B / $4-10B / $8-18B | 2027 前非主流，但对热、供电、良率和测试提出最高要求。 | 项目制毛利分化大；若形成专用市场，壁垒极高。 |

### 3.1 哪些在研方向最值得押注

1. HBM4/HBM4E 和 Custom HBM：量价最确定，利润池最强。  
2. CoWoS-L/SoIC/EMIB-T 等大尺寸 2.5D/3D 封装：2027 由 Rubin/MI400/ASIC 共同驱动。  
3. 先进封装设备和测试：订单领先收入，且供应商集中。  
4. ABF/玻璃/低翘曲材料：客户一旦认证后切换成本高。  
5. UCIe/3DIC EDA/IP/SLM：收入体量小但长期 ROIC 和粘性优异。  
6. CPO/photonic interposer：2026 收入小，但若 1.6T/3.2T 功耗压力提前爆发，弹性极大。

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 层级 | 主要地区 | 主要公司 | 工艺/产品 |
|---|---|---|---|
| Foundry + 高端 2.5D | 台湾为核心，美国/日本扩产中 | TSMC | CoWoS-S/L/R、SoIC、InFO、N3/N2、HBM base die、3DFabric。 |
| IDM/替代高端封装 | 美国、韩国、马来西亚 | Intel Foundry、Samsung | EMIB/EMIB-T、Foveros、I-Cube/X-Cube、turnkey memory/foundry/package。 |
| OSAT 先进封装 | 台湾、中国大陆、韩国、马来西亚、越南、美国 | ASE/SPIL、Amkor、JCET、Tongfu、Huatian、Powertech、UTAC、Hana Micron | FOWLP、2.5D 后段、SiP、测试、burn-in、部分 fan-out/bridge。 |
| HBM 与 memory package | 韩国、美国、日本、台湾 | SK hynix、Samsung、Micron | HBM3E/HBM4、TC bonding、16H、base die、SOCAMM/eSSD。 |
| 高阶载板/PCB | 日本、台湾、韩国、奥地利、中国大陆 | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、AT&S、Samsung Electro-Mechanics、LG Innotek、Daeduck、Shennan、WUS | ABF、BT、large-body substrate、high-layer PCB、玻璃/低翘曲基材。 |
| 设备 | 荷兰、日本、美国、奥地利、新加坡、中国香港/大陆 | ASML、Applied Materials、Lam、TEL、KLA、Besi、ASMPT、EVG、SUSS、DISCO、Accretech、K&S、Onto、Camtek、Advantest、Teradyne、FormFactor、Technoprobe | lithography、etch/deposition、TCB、hybrid bonding、wafer bonding、temporary bonding/debonding、dicing、metrology、ATE、probe cards。 |
| 材料 | 日本、美国、德国、台湾、韩国 | Ajinomoto、Resonac、Namics、Sumitomo Bakelite、Shin-Etsu、JSR、TOK、DuPont、Entegris、Merck、3M、Corning、Absolics | ABF、underfill、mold compound、photoresist、CMP slurry、bonding materials、glass core、TIM、specialty gases。 |

### 4.2 供给瓶颈

1. CoWoS/2.5D 有效产能：名义产能扩张不能等同于有效产出，interposer、RDL、载板、HBM KGD、final test 任一不足都会卡住。  
2. HBM KGD 与堆叠良率：HBM4/16H 对 TSV、TC bonding、热和 base die 良率更敏感，损失会放大到整包成本。  
3. 大尺寸 ABF/载板翘曲：package 面积扩大后，翘曲、热膨胀、阻抗和层间可靠性直接决定良率。  
4. TCB/混合键合设备交期：Besi、ASMPT、EVG、SUSS 等高端设备订单领先，客户认证周期长，临时扩产困难。  
5. 测试/老化时间：HBM、interposer、SerDes、NVLink/UALink/CXL、CPO 都需要更长测试，ATE 与探针卡成为隐形产能。  
6. 客户认证和系统级 burn-in：AI 芯片不是封装完成就能交付，还要经过机架、液冷、供电、网络、固件和软件栈验证。  
7. 人才与工艺 know-how：高端封装量产是工程经验密集型，warpage、thermal stress、yield debug 很难靠资本开支快速复制。  
8. 地缘与供应链集中：台湾高端封装、韩国 HBM、日本材料/载板、荷兰/美国/日本设备高度集中，任何地区扰动都会放大。

### 4.3 成本构成和毛利决定因素

高端 AI accelerator 模块 BOM 的粗略拆分：

| 成本项 | 占比估算 | 影响因素 |
|---|---:|---|
| 先进逻辑 die/wafer | 30-45% | N4/N3/N2 wafer 价格、die size、良率、掩膜和重工。 |
| HBM stacks | 30-45% | HBM3E/HBM4 价格、stack 数、12H/16H 良率、供应商长协。 |
| 先进封装服务 | 8-15% | CoWoS/SoIC/EMIB 产能、RDL/interposer 面积、TCB、yield loss。 |
| 高阶载板与机械件 | 5-10% | ABF 层数、面积、低翘曲材料、stiffener/lid/TIM。 |
| 测试、burn-in、probe | 3-8% | KGD 筛选、SerDes/HBM 测试时间、SLT 与老化。 |
| 电源/散热接口等 | 2-5% | 去耦、VRM、液冷接口、可靠性要求。 |

价格传导机制：

- AI 客户优先买确定交期，愿意用预付款、长协、take-or-pay、capacity reservation 换产能。  
- Foundry/封装/载板/HBM 若同时短缺，价格沿“缺一不可”的链条传导，最紧环节获得最大溢价。  
- NVIDIA/AMD/Broadcom 等平台商可通过整机架报价向 hyperscaler 转嫁 HBM 和封装涨价；OSAT 转嫁能力弱于 TSMC/HBM，但高端认证后议价改善。  
- 一旦 2027 供给释放太快，低端 OSAT、普通 substrate、普通 fan-out 会先承压，高端 CoWoS/HBM4/混合键合仍保持稀缺。

## 5. 竞争格局、壁垒与价值捕获

### 5.1 市场结构

| 细分 | 头部集中度判断 | 定价权 |
|---|---|---|
| AI 2.5D/CoWoS | TSMC 在 NVIDIA/AMD/高端 ASIC 中占绝对主导，AI 高端 2.5D 份额估计 75-90%。 | 极强，且与先进节点绑定。 |
| HBM | SK hynix、Samsung、Micron 三家几乎垄断；2026 HBM4 份额和良率决定定价。 | 极强，长协与客户认证强化。 |
| 先进封装设备 | TCB/HB/wafer bonding/ATE/探针卡头部集中，Besi、ASMPT、EVG、SUSS、Advantest、Teradyne、FormFactor 等各有强项。 | 强，设备认证周期长。 |
| 高阶载板 | Ibiden、Shinko、Unimicron、Nan Ya、AT&S、SEMCO、LG Innotek、Kinsus 等头部集中。 | 中强，良率和客户认证决定溢价。 |
| OSAT | ASE、Amkor、JCET、Tongfu、Huatian 等竞争更分散。 | 中等，高端项目强于传统封测。 |
| EDA/IP | Synopsys、Cadence、Siemens EDA、Ansys、Keysight、Alphawave、Rambus 等高度集中。 | 很强，毛利和粘性最好。 |
| 材料 | ABF、underfill、mold、photoresist、CMP、特殊气体高度依赖日美欧供应商。 | 强，认证后粘性高。 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 解释 |
|---|---|
| 技术壁垒 | CoWoS/SoIC/EMIB 的难点是热、应力、翘曲、微凸点/混合键合、RDL、interposer、KGD、测试协同，不是单个工序。 |
| 规模壁垒 | AI 客户需要一次锁定数十万到百万颗芯片等效产能，只有少数厂商能承担 capex、良率爬坡和交付责任。 |
| 客户锁定 | NVIDIA/AMD/Broadcom/云厂 ASIC 从设计阶段就绑定封装 design rule、载板、HBM、测试和系统验证，切换会重做验证。 |
| 认证标准 | 汽车和传统服务器认证已经严苛，AI rack 更增加液冷、功率瞬态、SerDes、HBM、固件、长时间 burn-in。 |
| 切换成本 | 换封装厂或载板厂意味着重新调 SI/PI、热仿真、mechanical stress、ATE program、可靠性数据，时间成本可能 6-18 个月。 |
| 数据/经验壁垒 | warpage、thermal stress、yield debug 的最佳参数来自历史量产数据，难以从论文或设备采购直接复制。 |
| 供应链组织壁垒 | 高端封装要求 foundry、memory、substrate、OSAT、设备、材料、系统厂同步，能组织供应链本身就是壁垒。 |

### 5.3 价值链中最可能长期高 ROIC 的层

1. TSMC 型“先进节点 + 先进封装”一体化：可以同时收 wafer、HBM base die、CoWoS/SoIC、设计生态的钱，且客户无替代。  
2. HBM 龙头：所有高端 XPU 共同刚需，2026-2027 价格和良率都支持高毛利。  
3. 关键设备和测试：TCB/HB、wafer bonding、ATE、探针卡、metrology 订单领先，且客户认证强。  
4. EDA/IP/DFT/SLM：市场规模小于硬件，但毛利 80%+，客户切换成本极高。  
5. 高阶载板与材料：一旦进入 NVIDIA/AMD/Broadcom/云厂供应链，收入弹性和定价权明显上行。  
6. OSAT：高端项目会改善利润率，但长期 ROIC 受客户集中、折旧和竞争影响，不如前几层。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

1. Blackwell Ultra/GB300 把 CoWoS-L/HBM3E 推成 2026 确定性收入主线。  
   最可能放量：CoWoS-L、HBM3E、ABF 大载板、冷板接口、ATE/探针卡。  

2. HBM4 从“验证”转为“客户锁产能”。  
   Rubin、MI455X、TPU8、OpenAI/Broadcom XPU 都要求 HBM4，2026H2 即使收入占比不高，也会提前拉动 TCB/HB 设备、HBM tester、base die、低翘曲载板。  

3. Custom ASIC 从补充算力变成独立产能池。  
   Meta/Broadcom 首期 >1GW、OpenAI/Broadcom 10GW、AWS Trainium、Google TPU、Microsoft Maia 使先进封装需求不再只看 NVIDIA。Broadcom XPU 平台、Marvell custom XPU、UCIe/以太网封装会快速升温。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

1. Rubin/MI400/TPU8/MTIA 450/500 进入 HBM4 时代。  
   2027 最可能爆发的是 HBM4、CoWoS-L、EMIB-T、I-Cube/X-Cube、SoIC/HB、16H 测试和大尺寸载板。

2. 先进封装从“制造瓶颈”升级成“架构护城河”。  
   2027 客户选择封装路线时会同时考虑 package size、HBM stack 数、thermal, power delivery, scale-up bandwidth, CPO compatibility 和系统级良率。

3. 第二供应源和替代路线价值上升。  
   如果 TSMC CoWoS 继续满载，Intel EMIB-T/Foveros、Samsung turnkey packaging、ASE/Amkor 高端 OSAT、玻璃/面板级路线都会获得更高战略估值。

## 8. 头部公司和技术地图

### 8.1 芯片和 XPU 客户

- 商用 GPU/XPU：NVIDIA、AMD、Intel、Groq、Cerebras、SambaNova、Tenstorrent、d-Matrix、Etched、MatX、Rebellions、Furiosa。  
- 云厂/平台 ASIC：Google/Broadcom TPU、AWS Annapurna Trainium/Inferentia、Microsoft Maia、Meta MTIA/Broadcom、OpenAI/Broadcom、Oracle/AMD/NVIDIA 生态。  
- 中国 AI 芯片：Huawei Ascend、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Iluvatar CoreX、MetaX、Moore Threads、Enflame、Hygon、燧原等。  

### 8.2 Foundry、IDM、封装平台

- TSMC：CoWoS-S/L/R、SoIC、InFO、CoPoS、3DFabric、N3/N2、HBM base die。  
- Intel Foundry：EMIB、EMIB-T、Foveros、PowerVia 相关先进封装、美国本土 advanced packaging。  
- Samsung：I-Cube、X-Cube、HBM4、4nm logic base die、AVP/turnkey AI package。  
- OSAT：ASE/SPIL、Amkor、JCET/星科金朋、Tongfu、Huatian、Powertech、KYEC、ChipMOS、UTAC、Hana Micron、Nepes、Deca。  

### 8.3 HBM、载板、材料

- HBM/DRAM：SK hynix、Samsung、Micron。  
- HBM IP/controller/PHY：Rambus、Synopsys、Cadence、Marvell、Broadcom、Alphawave。  
- ABF/载板/PCB：Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、AT&S、Samsung Electro-Mechanics、LG Innotek、Daeduck、Shennan Circuit、WUS、TTM。  
- 玻璃/面板级：Corning、Absolics、Intel、Samsung Electro-Mechanics、SCHOTT、LPKF、相关日本材料厂。  
- 材料：Ajinomoto、Resonac、Namics、Sumitomo Bakelite、Shin-Etsu、JSR、TOK、DuPont、Entegris、Merck/EMD、3M、Mitsui Chemicals、Henkel、Indium、Honeywell。  

### 8.4 设备、测试、EDA

- 前段/后段设备：ASML、Applied Materials、Lam Research、Tokyo Electron、KLA。  
- TCB/混合键合/wafer bonding：Besi、ASMPT、EV Group、SUSS MicroTec、Tokyo Electron、K&S、Shibaura、Hanmi。  
- 切割/研磨/薄化：DISCO、Accretech、Okamoto、K&S。  
- 量测/检测：KLA、Onto Innovation、Camtek、Nova、Lasertec、Applied Materials。  
- ATE/探针卡/老化：Advantest、Teradyne、Cohu、FormFactor、Technoprobe、MPI、Micronics Japan、Chroma。  
- EDA/IP/仿真：Synopsys、Cadence、Siemens EDA、Ansys、Keysight、Alphawave Semi、Arteris、Rambus、UCIe Consortium。  

### 8.5 CPO/硅光与高速互连

- 交换芯片/硅光/CPO：Broadcom、NVIDIA Networking、Marvell、Cisco、Intel、Ayar Labs、Lightmatter、Ranovus、Rockley 相关资产。  
- 光模块/器件/代工：Coherent、Lumentum、Fabrinet、Innolight、中际旭创、新易盛、华工科技、Accelink、Eoptolink、II-VI/Coherent、Hisense Broadband、Source Photonics。  
- 高速连接器/铜互连：Amphenol、TE Connectivity、Molex、Samtec、Luxshare、FIT、BizLink、Hirose、Credo、MACOM、Semtech。  

## 9. 投资结论与跟踪指标

### 9.1 投资结论

最值得优先跟踪的是四类“供不应求且客户难以替代”的资产：

1. TSMC/HBM/高端载板/设备这类硬瓶颈。它们决定 2026-2027 AI 芯片交付上限。  
2. Broadcom/Marvell/云厂 ASIC 生态对应的第二条封装需求曲线。它会让先进封装从 NVIDIA 单周期变成多客户、多平台长期周期。  
3. HBM4、SoIC、EMIB-T、CoPoS、玻璃基板等 2027-2028 技术期权。短期收入未必最大，但估值弹性最强。  
4. EDA/IP/测试/SLM。它们是多 die 量产的“保险层”，一旦进入流程，毛利和粘性都优于硬件平均水平。

### 9.2 需要持续跟踪的指标

- TSMC advanced packaging revenue 占比、CoWoS 月产能、CoWoS-L 良率和外包比例。  
- NVIDIA Rubin、GB300、AMD MI400/MI455X、Google TPU8、AWS Trainium3/4、Meta MTIA、OpenAI/Broadcom XPU 的实际出货节奏。  
- SK hynix/Samsung/Micron HBM4 客户认证、12H/16H 良率、HBM4E sampling、ASP 和长协。  
- ABF 大尺寸载板交期、翘曲良率、玻璃基板 pilot 进展。  
- Besi/ASMPT/EVG/SUSS/Advantest/Teradyne/FormFactor 订单和 backlog。  
- 1.6T/CPO 是否从交换芯片 pilot 转成大规模 AI network 采购。  
- OSAT 是否真正拿到高端 2.5D 核心工序，而不只是测试/周边封装。  
- Hyperscaler capex 是否继续上修，尤其 Meta、Microsoft、Amazon、Alphabet、Oracle、OpenAI/Stargate。  

## 10. 主要来源与验证材料

### 一手公司信息

- TSMC 1Q26 季报与电话会页面：<https://investor.tsmc.com/english/quarterly-results/2026/q1>  
- TSMC 1Q26 earnings transcript：<https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf>  
- NVIDIA Vera Rubin 官方新闻稿：<https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx>  
- NVIDIA Vera Rubin 技术博客：<https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/>  
- NVIDIA GB300 NVL72：<https://www.nvidia.com/en-us/data-center/gb300-nvl72/>  
- AMD/Meta 6GW 合作：<https://ir.amd.com/news-events/press-releases/detail/1279/amd-and-meta-announce-expanded-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus>  
- AMD/Samsung HBM4 合作：<https://www.amd.com/en/newsroom/press-releases/2026-3-18-samsung-and-amd-expand-strategic-collaboratio.html>  
- AMD CES 2026 Helios/MI400/MI500：<https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-and-its-partners-share-their-vision-for-ai-ev.html>  
- Meta MTIA 路线图：<https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/>  
- Broadcom/Meta MTIA 多 GW 合作：<https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-extended-partnership-meta-deploy-technology>  
- OpenAI/Broadcom 10GW 合作：<https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/>  
- AWS Trainium：<https://aws.amazon.com/machine-learning/trainium>  
- Google Ironwood TPU：<https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/>  
- Besi 1Q26 results：<https://www.besi.com/events/events-shows/details/be-semiconductor-industries-nv-announces-q1-26-results/>  
- ASMPT 1Q26 results：<https://www.asmpt.com/en/investor-relations/news-events/asmpt-announces-2026-first-quarter-results/>  
- ASMPT TCB AOR milestone：<https://www.asmpt.com/en/investor-relations/news-events/asmpt-extends-technology-leadership-with-key-tcb-aor-chip-to-wafer-milestone/>  
- EV Group SEMICON Korea 2026：<https://www.evgroup.com/company/news/detail/ev-group-highlights-hybrid-and-fusion-bonding-layer-transfer-and-maskless-lithography-technologies-for-advanced-semiconductor-memory-and-packaging-at-semicon-korea-2026>  
- Micron FY2Q26 results：<https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026>  
- Samsung 1Q26 earnings presentation：<https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_1Q_conference_eng.pdf>  

### 行业报告、论坛和技术材料

- TrendForce 2026 AI technology landscape：<https://www.trendforce.com/presscenter/news/20251127-12805.html>  
- TrendForce 2026 foundry outlook：<https://www.trendforce.com/presscenter/news/20260319-12979.html>  
- TrendForce CoWoS/CoPoS update：<https://www.trendforce.com/news/2026/04/16/news-tsmc-says-cowos-offers-industrys-largest-reticle-size-packaging-amid-intel-emib-rivalry-copos-advances/>  
- Chiplet Summit 2026 program：<https://chipletsummit.com/2026-program-at-a-glance/>  
- Chiplet Summit 2026 Yole HBM material：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260217_PreConB_Bertolazzi.PDF>  
- Chiplet Summit 2026 Marvell Custom HBM material：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260217_PreConB_Allman.PDF>  
- Chiplet Summit 2026 Intel packaging material：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_E-103_Hosseini.PDF>  
- Chiplet Summit 2026 Lightmatter photonic interposer：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260219_B-202_Nowroozi.PDF>  
- DesignCon 2026 official：<https://www.designcon.com/en/home.html>  
- DesignCon 2026 best paper awards：<https://www.globenewswire.com/news-release/2026/05/06/3289177/0/en/DesignCon-Crowns-2026-Winners-for-Best-Paper-Awards-and-Engineer-of-the-Year.html>  
- ConnectorSupplier DesignCon 2026 recap：<https://connectorsupplier.com/designcon-2026/>  
- Gartner semiconductor 2026 outlook：<https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026>  
- SIA 2025 sales and 2026 outlook：<https://www.semiconductors.org/global-annual-semiconductor-sales-increase-25-6-to-791-7-billion-in-2025/>  

### 项目内参考

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`  
- `D:\drive\Investment\调研\v5\conference_update\nvidia_gtc_2026_research.md`  
- `D:\drive\Investment\调研\v5\conference_update\chiplet_summit_2026_update.md`  
- `D:\drive\Investment\调研\v5\conference_update\designcon_2026_conference_update.md`  
- `D:\drive\Investment\调研\v5\conference_update\hpca_2026_conference_update.md`  
- `D:\drive\Investment\调研\v5\conference_update\ASPLOS_2026_conference_update.md`
# 行业调研：【CXL内存扩展与内存池化】

> 截至日期：2026-05-08（美国西海岸 2026-05-07 晚间附近公开资料）  
> 研究口径：CXL memory expansion、memory pooling、CXL controller/switch/retimer、CXL-attached DRAM、CXL hybrid memory、CXL software/fabric management，以及面向 AI 推理、RAG、KV cache、IMDB/HPC 的近内存计算与池化方案。  
> 市场口径：除特别说明外，金额为硬件/软件出货或订单收入池，不等同于云厂商最终服务收入；自研云内产品按等效硬件/服务溢价估算。本文不是投资建议。

## 0. 高浓度结论

### 0.1 一句话结论

CXL 内存扩展与内存池化在 2026 年不是“全面爆发”，而是从实验室、白皮书、服务器验证，进入 **云 VM private preview、少量生产部署、关键客户 qualification** 的第一年；真正可见的放量路线是 **CXL 2.0 Type-3 DDR5 memory module + smart memory controller + RHEL/Linux/BIOS tiering**，2027 年的弹性来自 **CXL 3.x switch-based pooling / Dynamic Capacity Device / rack-level shared memory / KV-cache 与 RAG runtime 接入**。

如果对 2026-2027 AI 计算中心建设抱非常乐观预期，CXL 的投资价值不在于替代 HBM，而在于成为 HBM、CPU DRAM、SSD 之间的“第三层内存语义层”：把不能放进 GPU HBM、但又不该落到 SSD 的 warm data、KV cache、vector index、IMDB working set、RAG cache、推荐系统特征表放到 CXL-attached DRAM 或 CXL pool 中，换取更高的 GPU/CPU 利用率与更低的内存过配。

### 0.2 关键事实锚点

| 类别 | 关键事实 | 投资含义 |
|---|---|---|
| 标准 | CXL 4.0 已发布，速率从 64GT/s 翻倍到 128GT/s，增加 bundled ports 和 memory RAS，继续向后兼容 CXL 3.x/2.0/1.1/1.0。来源：[CXL Consortium About](https://computeexpresslink.org/about-cxl/) / [CXL 4.0 Q&A](https://computeexpresslink.org/blog/introducing-the-cxl-4-0-specification-webinar-qa-recap-4386/) | 2026 收入仍以 CXL 2.0/PCIe 5.0 为主；CXL 4.0 更像 2026-2027 的 design-in 与 IP/SerDes 预算前置，系统收入大概率 2028+。 |
| 云部署 | Astera Labs 宣布 Leo CXL smart memory controllers 支持 Microsoft Azure M-series VM preview；公司称这是公开披露的首个 CXL-attached memory 云部署，Leo CXL 2.0 单 controller 支持最高 2TB，可使 server memory capacity 提高超过 1.5x。来源：[Astera/Azure announcement](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-leo-cxl-smart-memory-controllers-microsoft-azure-m) | 这是 CXL 从 PoC 到 hyperscale evaluation 的最强一手信号。若 Azure 从 preview 到 GA，2026H2-2027 将成为行业拐点。 |
| 内存模块 | Micron CZ120 已量产并出货给客户，CZ122 qualification samples 可用；CZ122 最高 256GB、约 37GB/s，CZ120/CZ122 获 RHEL 9.3 认证，并经过 AMD/Intel CPU 与 OEM 测试。来源：[Micron CZ122/RHEL](https://www.micron.com/about/blog/applications/data-center/introducing-micron-cz122-and-red-hat-certification-of-memory-expansion-portfolio) | CXL 模组已经不是纯概念。2026 真实放量在高内存 CPU server、SAP HANA/IMDB、HPC、RAG/AI inference 边缘场景。 |
| 三星 CMM-D | Samsung CMM-D MD220：CXL 2.0、PCIe 5.0、DDR5、EDSFF E3.S 2T、最高 256GB；Samsung 称 CMM-D 可扩容量/带宽并改善 TCO，IMDB 白皮书显示 OLTP 场景可接近 RDIMM，OLAP 取决于访问模式。来源：[Samsung CMM-D](https://semiconductor.samsung.com/cxl-memory/cmm-d/) / [Samsung IMDB blog](https://semiconductor.samsung.com/news-events/tech-blog/breaking-the-memory-wall-with-samsung-cmm-d-for-next-generation-imdb-infrastructure/) | CXL 的早期最佳负载不是所有随机热内存，而是可分层、可顺序读、对容量敏感、对小幅延迟可容忍的数据库与 AI warm data。 |
| CXL switch | Marvell 在 OFC 2026 发布 Structera S 30260，260-lane CXL switch，支持 rack-level memory pooling；CXL 3.0 支持，aggregate bandwidth up to 4TB/s；S 30260 预计 2026Q3 开始向客户 sampling，S 20256 CXL 2.0 switch 已在 production。来源：[Marvell Structera S](https://investor.marvell.com/news-events/press-releases/detail/1017/marvell-launches-next-generation-cxl-switch-enabling-memory-pooling-to-break-through-the-ai-memory-wall) | 2026 看 CXL 2.0 expansion，2027 看 switch-based pooling。Marvell/XConn 把 CXL 从单机扩内存推进到 rack-level fabric。 |
| 互操作 | Marvell Structera CXL 2.0 产品完成与 AMD EPYC、Intel Xeon、Micron/Samsung/SK hynix DDR4/DDR5 的互操作测试；Structera X 支持向通用服务器增加 TB 级内存，Structera A 集成 16 个 Arm Neoverse V2 core 与多内存通道。来源：[Marvell interoperability](https://www.marvell.com/company/newsroom/marvell-extends-cxl-ecosystem-leadership-with-structera-interoperability-across-platforms.html) | CXL 的商业壁垒是互操作、认证、RAS、firmware、BIOS/OS，而不只是 PHY。完成全栈互操作的厂商会有议价权。 |
| 市场报告 | Strategic Market Research：CXL component market 2024 年约 $1.9B，2030 年约 $12.3B，CAGR 约 32%；MarketIntelo：CXL memory expansion 2025 年约 $1.3B，2034 年约 $11.8B，CAGR 28.7%，其中 pooling 子方向 CAGR 约 35.2%。来源：[SMR](https://www.strategicmarketresearch.com/market-report/compute-express-link-component-market) / [MarketIntelo](https://marketintelo.com/report/cxl-memory-expansion-market) | 公开报告多偏保守。若 2026-2027 AI inference/KV cache 超预期，CXL 实际收入可能从“平滑 CAGR”变成阶跃式 adoption。 |
| 需求侧 | CXL Consortium 2026-04-01 webinar 明确把三大阻碍定义为：相比 DIMM 延迟更高、AI 数据密集应用带宽不足、虚拟化/云原生软件支持不够 robust，并提出 S-CHMU、CXL-PNM、Pangaea。来源：[CXL Vertical Optimization webinar](https://computeexpresslink.org/event/overcoming-cxl-limitations-enabling-cxl-hardware-and-software-as-vertical-optimization-technologies/) | 2026 的最大变化是行业承认“硬件可用不等于商业可用”，价值正在从 module 扩展到 controller telemetry、OS tiering、Kubernetes/fabric manager。 |

### 0.3 对 2026-2027 的核心判断

1. **2026 最可能放量的技术路径**：CXL 2.0 Type-3 memory expansion module（EDSFF/AIC）+ CXL smart memory controller + Intel Xeon 6 / AMD EPYC 9005 CXL 2.0 host + RHEL/Linux/BIOS heterogeneous interleaving。  
2. **2026 不太会大规模放量但最值得跟踪的路径**：CXL 3.0/3.1 switch-based pooling、Dynamic Capacity Device、Pangaea-like Kubernetes memory orchestration、CXL-PNM/near-memory vector search/KV-cache offload。  
3. **2027 最可能出现超预期的子方向**：rack-level CXL pooling switch、CXL memory-as-a-service 云 SKU、CXL-aware RAG/KV cache runtime、CXL hybrid DRAM+NAND persistent memory。  
4. **CXL 对 AI 芯片的真实关系**：NVIDIA/AMD/TPU/Trainium 的 HBM 仍决定训练与高端推理峰值性能；CXL 决定的是 CPU side、rack side、KV cache side、RAG/vector side 和 stranded memory utilization。它不是主算力芯片，但可能提升主算力芯片利用率。  
5. **最长期高毛利层**：CXL controller/switch/retimer silicon + firmware/fleet telemetry/IP。DRAM 模组有景气周期高利润，但长期 ROIC 更受内存周期影响；软件毛利高但很多价值会被云厂商内部化。  

## 1. 2026 AI 计算中心建设下的机遇、挑战与技术路线

### 1.1 需求机遇：为什么 AI 会把 CXL 从“服务器选配”推向“基础设施层”

| AI 基础设施变化 | 对内存系统的压力 | CXL 的对应价值 |
|---|---|---|
| 长上下文、agentic inference、视频/多模态输入 | KV cache 从 GB 级走向 TB 级；同一 GPU rack 内 HBM 容量再大也很快被长上下文与并发吃掉 | 把冷/温 KV cache、prompt cache、RAG cache 从 HBM/本地 DRAM 分层到 CXL-attached DRAM；牺牲部分延迟换容量与成本 |
| GPU/ASIC rack 价格高、HBM 紧缺 | 每个 GPU idle minute 都很贵，系统瓶颈从“有没有 GPU”变成“GPU 是否被内存、网络、数据喂饱” | CXL pool 降低 stranded memory，给 CPU side data pipeline、feature store、vector index 提供低延迟大容量 |
| AI server CPU:GPU 配比变化 | 推理场景 CPU host 内存压力上升，尤其调度、tokenization、RAG、数据库、cache | CXL Type-3 memory expansion 可以不增加 CPU socket 就扩内存 |
| 数据中心 CapEx 大、供电与机架密度受限 | 过配本地 DRAM 造成资本浪费与功耗浪费 | 池化后提高 DRAM utilization，减少每台服务器必须预装的峰值内存 |
| AI 数据管道从训练走向在线推理 | 在线系统需要低抖动、可弹性扩展、可多租户隔离 | CXL 3.x/4.0 的 RAS、security、fabric、DCD、bundled ports 变重要 |

### 1.2 挑战：为什么 2026 仍然不是“所有服务器都插 CXL”

1. **延迟与带宽不是 HBM/DIMM 级别**：CXL-attached DRAM 通过 PCIe/CXL 链路，延迟高于本地 DDR5，带宽受 x8/x16、controller、switch 上游端口限制。CXL 的价值来自分层与利用率，不来自替代本地热内存。  
2. **软件栈仍是最大瓶颈**：OS tiering、NUMA policy、Kubernetes、VM/hypervisor、fabric manager、Redfish/OCP DCMFM、BIOS 配置都要成熟，否则硬件只是“能识别”，不是“能省钱”。  
3. **互操作成本高**：CPU 平台、BIOS、CXL controller、DDR5 vendor、switch、retimer、OS、RHEL certification、RAS/secure boot/IDE、BMC 管理都要测试。  
4. **客户 qualification 周期长**：hyperscaler 和大型企业数据库客户通常需要 6-18 个月验证，CXL 又涉及可靠性、数据一致性与多租户隔离，导入速度慢于 GPU/SSD。  
5. **DRAM 涨价双刃剑**：DRAM 越贵，CXL pooling ROI 越高；但 CXL module BOM 也主要是 DRAM，初期客户会要求明确 TCO 模型。  
6. **AI accelerator vendor 的封闭互联竞争**：NVIDIA NVLink/NVSwitch、Google TPU pod、AWS NeuronLink、Huawei UB、AMD Infinity/UALink 都会优先服务 GPU/XPU scale-up。CXL 更可能先在 CPU-side memory tier 与 open rack memory fabric 落地。  

### 1.3 当前正在使用的技术路线

| 技术路线 | 2026 状态 | 已知公司/产品 | 主要负载 | 投资判断 |
|---|---|---|---|---|
| CXL 2.0 Type-3 memory expansion | 已有量产/样品/认证/客户评估，是 2026 主线 | Micron CZ120/CZ122、Samsung CMM-D MD220、SK hynix CMM、SMART/Gigabyte/AIC/H3 等 | SAP HANA/IMDB、HPC、RAG cache、CPU inference、big data analytics | 2026 最现实收入池 |
| CXL smart memory controller | 已经产品化，收入由 module/AIC/cloud SKU 带动 | Astera Leo、Marvell Structera X/A、Montage MXC、Microchip SMC 2000/2100、ScaleFlux MC500 等 | CXL-attached DDR4/DDR5、compression、telemetry、near-memory | 高毛利、强互操作壁垒 |
| CXL 2.0 switch static pooling | 少量生产/系统集成，更多是示范和 enterprise pilot | Marvell/XConn S 20256、Microchip Switchtec、H3、MemVerge、Samsung demo | 多 host 共享内存、数据库、AI pipeline | 2026 小量，2027 弹性大 |
| CXL 3.x dynamic pooling / DCD / MLD | 2026 sampling/PoC，2027 早期生产化 | Marvell Structera S 30260、XConn、UnifabriX、H3、Liqid、OCP/DMTF | rack-level memory pool、memory-as-a-service | 最重要 2027 方向 |
| CXL software tiering/orchestration | 2026 从工具变成差异化能力 | Linux CXL、RHEL 9.3、MemVerge Memory Machine X、Pangaea、UnifabriX fabric manager、Kubernetes NRI | VM/pod 动态分配、NUMA tiering、fleet management | 硬件放量的前置条件 |
| CXL-PNM/NDP | 2026 仍偏研究，已有 CXL Consortium/Samsung webinar 案例 | Samsung CXL-PNM、Marvell Structera A、学术 NDP、XCENA MX1、ScaleFlux | FAISS/vector search、RAG、KV cache offload | 若 API 标准化，2027-2028 爆发 |
| CXL hybrid DRAM+NAND | 原型/白皮书阶段 | Samsung CMM-H PM/TM、潜在 Netlist/SMART/存储厂商路线 | persistent memory、large memory tier、SSD 与 DRAM 之间 | Optane 退出后的长期选项 |
| CXL 4.0/PCIe 7.0 128GT/s | 标准已发布，产品化靠后 | CXL Consortium、Synopsys、Rambus、Cadence、Marvell、Montage、Astera | 下一代 AI-scale memory fabric | 2026-2027 看 IP/design win，不看大收入 |

### 1.4 在 2026-2027 出货量最大 AI 芯片背景下，CXL 的技术适配判断

> 下表基于项目已有《全球 AI 芯片路线图与 2026-2027 产能释放预测》中的高出货/高价值平台，不重新外部搜索 AI 芯片出货。

| AI 芯片/平台 | 2026-2027 主要技术路径 | 内存压力来源 | CXL 相关机会 | 成熟/放量判断 |
|---|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | NVLink/NVSwitch + HBM3E + Grace/CPU host + 800G/1.6T scale-out | 每 GPU HBM 容量高但长上下文、并发推理、RAG 数据喂给仍吃 CPU/host memory | CXL 不替代 NVLink/HBM；可做 CPU-side KV cache、RAG/vector index、host memory expansion、数据库节点 | 2026 CXL 主要在外围 CPU/数据节点；2027 可能进入 AI factory memory tier |
| NVIDIA B200/GB200 | NVLink 5、HBM3E、液冷 rack | 存量 Blackwell 集群持续推理化 | 与 GB300 类似，偏 host-side 扩展 | 2026H2 pilot，2027 扩大 |
| NVIDIA Vera Rubin/Rubin Ultra | HBM4、NVLink 6/7、CPO/Spectrum-6 生态 | HBM4 昂贵，训练/agentic 推理对数据层容量需求更大 | CXL 作为 HBM 外部容量层更有 TCO 价值，但不会在核心 GPU fabric 替代 NVLink | 2027 开始随 Rubin/AI factory 进入系统设计 |
| AMD MI350/MI355 | HBM3E、Infinity Fabric/以太网、企业部署较友好 | 企业/云部署会需要更高 CPU 内存与数据库/RAG sidecar | AMD EPYC 9005 支持 CXL 2.0，MI350 服务器旁路采用 CXL memory expansion 的概率高 | 2026 是最容易与 CXL 同机部署的非 NVIDIA GPU 路线之一 |
| AMD MI400/MI455X/Helios | HBM4、rack-scale、UALink/open fabric 倾向 | 72 GPU rack 与 HBM4 使外部内存层更有价值 | UALink 做 scale-up，CXL 做 memory tier/pooling，二者并行 | 2027 弹性大，取决于 Meta/云厂商订单 |
| AWS Trainium2/Trainium3 | NeuronLink/EFA，AWS 垂直集成 | Project Rainier/Anthropic 训练和推理需要大规模 cache/data pipeline | AWS 未公开 CXL 主线，但通用 EC2/RDS/AI data pipeline 很可能内部评估 CXL memory tier | 公开性低，2027 若 AWS 发布 CXL-backed SKU 会是强催化 |
| Google TPU v7 Ironwood / TPU8 | TPU pod 自研互联，Broadcom/Google 垂直优化 | 推理优先、Anthropic TPU 扩容带来 KV/RAG/数据库压力 | CXL 可能在 Google Cloud general purpose memory tier、RAG/vector 服务层，而非 TPU pod 核心 | 2026-2027 主要是推断，等待 GCP SKU/论文/开源信号 |
| Microsoft Maia 200 / Azure | TSMC 3nm、HBM3E、Azure 推理 | Copilot/OpenAI/Azure enterprise inference 与 SAP HANA/IMDB | Azure 已有 CXL M-series private preview，是 CXL 商业化最强信号 | 2026H2 preview->GA 是头号指标 |
| Meta MTIA / Broadcom XPU | OCP rack、Broadcom SerDes/Ethernet/custom XPU | 推荐/广告/GenAI 推理，feature store 与 KV cache 巨大 | Meta/OCP 历史上积极 demo CXL；CXL pooling 适合 open rack memory disaggregation | 2027 可能在 internal fleet 扩大 |
| Huawei Ascend 910C/950 | UB/超节点、本土 HBM/DRAM 受约束 | 国产 HBM/DRAM 瓶颈、CPU side 数据层压力 | 中国生态可能发展兼容/类 CXL memory expansion，但受标准、供应链、CPU 平台影响 | 2026 不作为全球 CXL 主线，2027 关注国产替代 |
| Cambricon/Alibaba/Baidu 等中国 ASIC/GPU | 国产制程、HBM/DRAM/互连受限 | 单芯片算力和内存带宽弱于国际高端，需要系统级扩容 | CXL/PCIe memory expansion 对 CPU 推理和私有化部署有吸引力 | 更偏中国本地系统集成机会 |

### 1.5 新技术成熟与放量时间预测

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|
| CXL 2.0 Type-3 DDR5 expansion module | 2026H1 已产品化；2026H2 limited production；2027H1 在 Azure/企业 IMDB/HPC 扩大 | 2026H2 Azure 接近 GA，1-2 家 CSP 跟进；2027 年收入过 $3B | 2026H2 被 DRAM 紧缺与 KV cache 拉动，2027 年 CXL memory module 年收入 $6B+ |
| CXL smart memory controller | 2025-2026 成熟；2026 随模组增长 | 2026H2 关键客户 design win 密集披露；2027 controller 收入 $2B+ | controller/switch 被视为 AI memory fabric 核心，2027 头部厂商出现供不应求 |
| CXL 2.0 switch static pooling | 2026 小批 production/pilot；2027 扩大 | 2026H2 多个 H3/MemVerge/OEM demo 转订单 | 2027 上半年进入 hyperscaler rack pilot，带动 switch ASP 高企 |
| CXL 3.x dynamic capacity / MLD / DCD | 2026 采样与互操作；2027H2 small production | 2027H1 production pilot；2027H2 成为新 AI rack 选项 | 2027 年中进入一线云厂商 memory-as-a-service 内部平台 |
| CXL-PNM / near-memory vector/KV | 2026 research/PoC；2027 early access；2028 revenue | 2027H2 形成 RAG/vector DB benchmark 与初始订单 | 2027H1 vLLM/FAISS/vector DB 出现事实 API，收入提前 |
| CHMU/S-CHMU telemetry tiering | 2026 标准讨论与 vendor daemon；2027 controller feature | 2027H1 Linux/vendor stack 成熟 | 2026H2 被云厂商定制为 controller 必选项 |
| CXL hybrid DRAM+NAND CMM-H | 2026 prototype/whitepaper；2027 early customer | 2027H2 用作 Optane 替代与 persistent memory tier | 2027 年成为低成本 TB 级 memory tier 的 surprise product |
| CXL 4.0 128GT/s | 2026-2027 IP/design-in；2028+ 产品收入 | 2027H2 样片/early platform | 2027 年高端 IP/PHY/SerDes 订单显著放大，但系统收入仍靠后 |

## 2. 已开始放量/准放量的关键产品：规模、渗透率、利润率

### 2.1 已放量产品清单

| 细分产品 | 代表产品/公司 | 2026 状态 | 一手证据 |
|---|---|---|---|
| CXL DDR5 memory module / EDSFF | Micron CZ120/CZ122、Samsung CMM-D MD220、SK hynix CMM、SMART Modular、Gigabyte AI TOP CXL R5X4 | CZ120 已量产出货，CZ122 qualification samples；Samsung MD220 正式产品页；SK hynix 已完成 CMM DDR5 96GB 客户验证 | [Micron CZ122/RHEL](https://www.micron.com/about/blog/applications/data-center/introducing-micron-cz122-and-red-hat-certification-of-memory-expansion-portfolio)、[Samsung CMM-D](https://semiconductor.samsung.com/cxl-memory/cmm-d/)、[SK hynix validation](https://news.skhynix.com/sk-hynix-completes-customer-validation-of-cxl-based-ddr5/) |
| CXL smart memory controller | Astera Leo、Marvell Structera X/A、Montage MXC、Microchip SMC 2000/2100 | Astera Leo 进入 Azure M-series preview；Marvell Structera 完成多 CPU/内存互操作；Montage CXL 3.1 MXC sampling | [Astera Azure](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-leo-cxl-smart-memory-controllers-microsoft-azure-m)、[Marvell interoperability](https://www.marvell.com/company/newsroom/marvell-extends-cxl-ecosystem-leadership-with-structera-interoperability-across-platforms.html)、[Montage CXL 3.1](https://www.montage-tech.com/Press_Releases/20250901) |
| CXL switch / fabric | Marvell/XConn Structera S 20256/30260、Microchip Switchtec、XConn Apollo、H3 Platform | CXL 2.0 switch 已 production；CXL 3.0 260-lane switch 2026Q3 sampling | [Marvell Structera S](https://investor.marvell.com/news-events/press-releases/detail/1017/marvell-launches-next-generation-cxl-switch-enabling-memory-pooling-to-break-through-the-ai-memory-wall)、[H3 OCP 2025](https://www.h3platform.com/newsroom/press-release-detail/87) |
| CXL OS/virtualization certification | RHEL 9.3、Linux CXL、KVM/QEMU、BIOS interleaving | Micron CZ120/CZ122 获 RHEL 9.3 认证；Linux 6.9+ 支持 page-level interleaving 实验 | [Micron CZ122/RHEL](https://www.micron.com/about/blog/applications/data-center/introducing-micron-cz122-and-red-hat-certification-of-memory-expansion-portfolio)、[Intel/Micron Xeon 6 paper](https://www.intel.com/content/www/us/en/content-details/842211/optimizing-system-memory-bandwidth-with-micron-cxl-memory-expansion-modules-on-intel-xeon-6-processors.html) |
| CXL memory pooling appliance/software | H3 Platform、MemVerge Memory Machine X、UnifabriX MAX、Liqid | H3 2025 展示 4 host/16 modules/5TB pool；MemVerge 提供 memory expansion/pooling software；UnifabriX MAX 最高 32TB DDR5 in 2U、扩展到 256TB | [H3 FMS 2025](https://www.h3platform.com/newsroom/press-release-detail/86)、[MemVerge CXL](https://memverge.com/cxl/)、[UnifabriX](https://unifabrix.tech/) |

### 2.2 已放量产品市场规模与渗透率预测

> 口径：未来 3 个月为 2026-05 至 2026-07/08 的实际收入池；未来 1 年为 2026-05 至 2027-04/05；未来 2 年为 2026-05 至 2028-04/05 累计收入池。渗透率指“具备 CXL host 能力且有高内存需求的 eligible server/rack”，不是全部服务器。

| 细分产品 | 当前收入状态 | 未来 3 个月：基准 / 乐观 / 极度乐观 | 未来 1 年：基准 / 乐观 / 极度乐观 | 未来 2 年：基准 / 乐观 / 极度乐观 | 渗透率路径 |
|---|---:|---:|---:|---:|---|
| CXL Type-3 memory modules（CMM-D/CZ120/CZ122/AIC/EDSFF） | 2025 全球 CXL memory expansion 约 $1.3B；2026 年化公开口径约 $1.6-1.8B | $0.25-0.45B / $0.45-0.75B / $0.80-1.20B | $1.4-2.0B / $2.3-3.2B / $3.8-5.2B | $3.5-5.0B / $6.0-9.0B / $10-16B | 当前 eligible high-memory server <1-2%；1 年基准 2-4%、乐观 5-8%、极度 10-15%；2 年基准 6-10%、乐观 12-20%、极度 25-35% |
| CXL smart memory controllers | 直接收入嵌入 module/AIC/cloud deployment；component market 2024 $1.9B，controller 为最大子项 | $0.12-0.25B / $0.25-0.45B / $0.45-0.75B | $0.7-1.2B / $1.2-2.0B / $2.2-3.2B | $1.8-3.2B / $3.5-5.5B / $6-9B | 随 module attach；高端 CXL 模组 controller attach 100%，但 merchant vs captive 比例约 60-80% |
| CXL switch / retimer / fabric silicon | CXL 2.0 switch 已 production，CXL 3.0 260-lane switch 2026Q3 sampling | $0.05-0.15B / $0.15-0.30B / $0.30-0.55B | $0.35-0.80B / $0.80-1.50B / $1.6-2.5B | $1.2-2.8B / $3.0-5.0B / $5.5-9.0B | 当前 CXL expansion 节点 switch attach <10%；1 年 10-20%；2 年若 rack pooling 成立可达 25-45% |
| CXL pooling appliance/chassis（H3/AIC/UnifabriX/Liqid 类） | 2026 主要是 demo、pilot、enterprise PoC | $0.02-0.08B / $0.08-0.18B / $0.18-0.35B | $0.15-0.50B / $0.50-1.00B / $1.0-1.8B | $0.7-2.0B / $2.0-4.5B / $5-8B | 当前极低；2 年内在 IMDB/HPC/AI inference memory pool 中 5-15%，极度乐观 20%+ |
| CXL software / memory orchestration / support | 可见收入小，很多被硬件 bundle 或云内部化 | $0.01-0.03B / $0.03-0.08B / $0.08-0.15B | $0.05-0.20B / $0.20-0.50B / $0.50-1.0B | $0.2-0.8B / $0.8-2.0B / $2.0-4.0B | 作为单独软件渗透率低；作为硬件/云平台必备功能 attach 可达 50%+ |
| CXL-enabled cloud VM / memory-as-a-service premium | Azure private preview，暂无 GA 定价；收入体现在云服务溢价与硬件 pull-through | $0.03-0.10B / $0.10-0.25B / $0.25-0.50B | $0.25-0.80B / $0.80-1.8B / $2.0-3.5B | $1.0-3.0B / $3.0-7.0B / $8-15B | 当前 <1% 高内存云 VM；若 Azure GA 且 SAP/IMDB 客户采用，2 年可到 5-15%；极度乐观 20%+ |

### 2.3 已放量产品增长与利润率预测

| 细分产品 | 未来 1 年增长：基准 / 乐观 / 极度乐观 | 当前毛利率/利润率估计 | 未来利润率：基准 / 乐观 / 极度乐观 | 定价弹性来源 |
|---|---:|---|---|---|
| CXL memory modules | +30-55% / +70-110% / +150-220% | 毛利 35-55%；DRAM 极紧缺时可到 50-65%，但模组早期验证成本高 | 35-55% / 45-65% / 55-75% | DRAM 供应紧、256GB+ 高容量、CXL 认证稀缺、客户愿意用更高 ASP 换交付与 TCO |
| CXL smart controllers | +40-70% / +90-140% / +180%+ | 高端 fabless connectivity 毛利 65-78%；Astera 2026Q1 GAAP gross margin 76.3% 可作上沿参考 | 68-75% / 72-78% / 75-82% | silicon + firmware + RAS + telemetry + 互操作认证，切换成本高 |
| CXL switch/fabric | +50-100% / +150-250% / +350%+ | 毛利 60-75%，取决于 switch radix、SerDes、software stack | 60-72% / 68-76% / 72-80% | CXL 3.0 switch 稀缺、高 lane count、rack-level memory pooling 是客户架构锁点 |
| Pooling appliance/chassis | +80-150% / +200-350% / +500%+ | 系统毛利 20-35%；含软件/服务可到 35-50% | 20-35% / 30-45% / 40-55% | 端到端集成、快速部署、validated configuration，适合企业客户付溢价 |
| CXL software/orchestration | +100%+ / +250%+ / +500%+ | 软件毛利 70-85%，但可见收入低、云内部化强 | 70-85% gross；经营利润取决于规模，10-40% | Kubernetes/VM/fabric manager 一旦进入生产，续费与支持粘性强 |
| Cloud CXL VM/service | 低基数翻倍 / 3-5x / 8x+ | 云服务增量毛利可高，但硬件折旧重；贡献毛利 40-65% | 45-60% / 50-65% / 55-70% | 高内存 VM 客户重视容量与 SLA，若能少买更大 socket/节点，愿意付 premium |

## 3. 在研关键产品与细分技术：未来快速增长方向

### 3.1 在研产品/技术清单

| 在研方向 | 当前证据 | 技术壁垒 | 放量触发点 |
|---|---|---|---|
| CXL 3.x Dynamic Capacity Device / Multi-Logical Device / Multi-Head Device | CXL 3.x Q&A 指出 OS-level tiering、CHMU 与 DCD 方向；CXL 4.0 Q&A 明确 DCD 允许近即时增加/移除 memory capacity | switch/fabric manager、host mapping、security isolation、NUMA policy、multi-tenant RAS | 一线云厂商公开 memory-as-a-service 或 CXL-backed bare metal |
| Rack-level CXL 3.0 pooling switch | Marvell Structera S 30260：260 lanes、CXL 3.0、4TB/s aggregate、2026Q3 sampling | 高 radix switch、SerDes、retimer/cable、fabric management、热设计 | 2026Q3 sample 后的 customer design win、2027H1 production |
| S-CHMU/CHMU hot-page telemetry | CXL Consortium 2026 webinar 将其列为解决 latency 的关键；CXL 3.x Q&A 称目标是 OS-based memory tiering | device-side page monitoring、低成本 counter/sketch、driver/daemon、OS migration | Linux/RHEL/vendor daemon 支持，controller datasheet 把 telemetry 做成标准功能 |
| CXL-PNM / processing-near-memory | CXL Consortium/Samsung webinar 用 FAISS IVF Flat 展示近内存 vector search；Marvell Structera A 集成 Arm core 与 memory channel | API、multi-tenant security、软件生态、near-memory compute ISA/SDK | FAISS/vLLM/Milvus/pgvector/LLM runtime 接入，客户 benchmark 出现 |
| GPU direct access to CXL memory pool | 2025-2026 学术论文出现 Beluga/CCCL 等 CXL shared memory pool for GPU/KV/collectives 方向 | GPU page fault / coherency / isolation / switch latency / accelerator vendor 配合 | 非 NVIDIA open rack、AMD/UALink/custom ASIC 平台愿意引入 CXL memory tier |
| CXL hybrid DRAM+NAND CMM-H | Samsung CMM-H PM/TM 白皮书、原型与 Memcon/FMS 展示 | NAND latency hiding、DRAM cache policy、endurance、persistent semantics、OS overhead | Optane 替代需求、数据库/存储 cache、低成本 TB 级 memory tier |
| CXL 4.0 128GT/s IP/PHY/verification | CXL 4.0 public spec，Synopsys/Rambus/Cadence 等 IP 与 VIP 支持 | 128GT/s PAM4、retimer、optical/copper channel、verification closure | 2027 high-end platform design-in，2028 system ramp |

### 3.2 在研产品未来规模、渗透率与利润率

| 在研方向 | 未来 3 个月：基准 / 乐观 / 极度乐观 | 未来 1 年：基准 / 乐观 / 极度乐观 | 未来 2 年：基准 / 乐观 / 极度乐观 | 渗透率与利润率 |
|---|---:|---:|---:|---|
| CXL 3.x rack-level dynamic pooling | $0.02-0.08B / $0.08-0.20B / $0.20-0.40B | $0.25-0.70B / $0.8-1.8B / $2.0-3.5B | $1.5-3.5B / $4-8B / $9-16B | 2 年 eligible AI/IMDB rack 渗透基准 5-10%、乐观 15-25%、极度 35%+；switch/controller GM 65-78%，system GM 25-40% |
| CHMU/S-CHMU telemetry tiering | <$0.02B / $0.02-0.05B / $0.05-0.10B | $0.05-0.20B / $0.20-0.60B / $0.60-1.0B | $0.4-1.0B / $1.0-2.5B / $2.5-5.0B | 多以内嵌 controller/software attach 收入出现；毛利 70%+，但独立可见 TAM 较小 |
| CXL-PNM/vector/KV offload | <$0.01B / <$0.03B / $0.03-0.08B | $0.05-0.15B / $0.20-0.60B / $0.80-1.5B | $0.4-1.2B / $1.5-4.0B / $5-10B | 若成为 RAG/KV 标配，渗透可从 0 到 5-15%；专用 SoC/accelerator 毛利 55-75% |
| GPU-accessible CXL memory pool | PoC/R&D | $0.03-0.10B / $0.10-0.40B / $0.50-1.0B | $0.3-1.0B / $1.5-4.0B / $5-12B | 取决于 GPU/ASIC vendor 开放程度；极度乐观来自 AMD/UALink/custom XPU racks |
| CXL hybrid DRAM+NAND CMM-H | <$0.02B / $0.02-0.06B / $0.06-0.12B | $0.05-0.25B / $0.25-0.80B / $1.0-2.0B | $0.6-1.8B / $2-5B / $6-12B | Persistent memory/Optane replacement；模组 GM 35-60%，controller/firmware 65%+ |
| CXL 4.0 IP/verification/design-in | $0.03-0.08B / $0.08-0.15B / $0.15-0.30B | $0.15-0.40B / $0.40-0.90B / $1.0-1.8B | $0.5-1.5B / $1.5-3.5B / $4-7B | IP/EDA/VIP gross margin 80-90%；系统产品收入 2028 后更大 |

### 3.3 最可能快速增长的三类“未来关键产品”

1. **CXL 3.x switch + fabric manager**：因为 CXL memory pooling 的经济性必须跨 host/rack 才能充分体现；Marvell 2026Q3 sample 时间表把 2027 放量窗口显性化。  
2. **CXL controller telemetry + OS tiering**：如果没有 hot-page monitoring、NUMA policy、RHEL/Linux/Kubernetes 支持，CXL module 很难大规模生产化；这层价值会被 controller 和软件平台共同捕获。  
3. **CXL-PNM / near-memory vector/KV**：短期收入最小，但如果 RAG/vector/KV runtime 接入，CXL 的瓶颈从“带宽不够”变成“数据不用搬”，这会显著抬高 TAM。  

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 主要产能集中在哪里

| 层级 | 地区/公司 | 产能与工艺特点 |
|---|---|---|
| DRAM / DDR5 / CXL module | Samsung、SK hynix（韩国）、Micron（美国/台湾/日本/新加坡）、SMART Modular、部分台湾/中国模组厂 | CXL module BOM 主要是 DDR5/DDR4 DRAM；高容量 128GB/256GB+ RDIMM/DRAM 颗粒供应、测试、RHEL/OEM 认证决定交付 |
| CXL controller / switch silicon | Astera Labs、Marvell/XConn、Montage、Microchip、Broadcom/PLX、ScaleFlux、Rambus/Synopsys/Cadence IP | 高速 SerDes、PCIe/CXL controller、DDR controller、security/RAS、firmware；Marvell Structera 使用 5nm 并集成 compression/Arm core |
| CPU host platform | Intel Xeon 6、AMD EPYC 9005、部分 ARM server CPU | Intel Xeon 6 官方支持最高 64 lanes CXL 2.0；AMD EPYC 9005 技术指南列出最高 64 lanes CXL 2.0、可用 8 张 256GB CXL card 增加 2TB |
| 系统/OEM/ODM | Dell、HPE、Lenovo、Supermicro、Gigabyte、AIC、H3 Platform、Wiwynn、Quanta、Inventec、Foxconn | 关键在 BIOS、BMC、热设计、EDSFF/AIC 机械结构、validated configuration、客户交付 |
| 软件/云 | Microsoft Azure、Red Hat、Linux kernel、MemVerge、UnifabriX、H3、Liqid、VMware/Broadcom、Kubernetes/OCP/DMTF | 负责 OS tiering、KVM/QEMU、memory hotplug、fabric manager、Redfish API、cloud SKU、SLA |
| 测试认证 | CXL Consortium Integrators List、PCI-SIG、UNH-IOL、Granite River Labs、Keysight、Teledyne LeCroy、Tektronix、Anritsu | CXL 2.0/3.x/4.0 合规、PCIe 5/6/7 signal integrity、retimer、protocol analyzer、BERT、系统级一致性 |

### 4.2 供给瓶颈

| 瓶颈 | 具体表现 | 为什么会限制放量 |
|---|---|---|
| DDR5/HBM/DRAM 供应与价格 | AI 抢占 HBM 和 server DRAM，常规 DDR5/RDIMM 也涨价 | CXL module BOM 主要是 DRAM；内存越贵，客户 ROI 更强但采购预算也更紧 |
| CXL controller / high-speed SerDes | CXL 2.0/3.x 需要 PCIe 5/6 PHY、DDR controller、RAS/security、firmware | 芯片验证周期长；一个 bug 会影响数据一致性和客户信任 |
| CPU host 与 BIOS 支持 | 并非所有 PCIe root port 都完整支持 CXL.mem；BIOS interleaving 与 NUMA 配置复杂 | 客户需要可预测性能，不能靠手工调参做大规模 fleet |
| 互操作认证 | CPU、CXL controller、switch、DDR vendor、OS、hypervisor、BMC 全链路都要测 | 认证失败会导致客户 qualification 延迟 1-2 个季度 |
| Switch/fabric manager | CXL pooling 需要 switch、DCD、MLD、Redfish/OCP DCMFM、隔离与动态回收 | 没有 fabric manager，pooling 只能停留在静态/实验环境 |
| 热设计与形态 | EDSFF E3.S、AIC、x16、DDR5 DIMM 插槽、controller 散热与 8-pin power | CXL memory card 不只是“插内存”，高容量 DDR5 + controller 会带来功耗和风道约束 |
| 安全与多租户 | CXL memory pool 涉及 shared physical memory、TSP/IDE、VM 隔离、secure erase | 云客户不会接受“快但不安全”的共享内存层 |
| 人才/工具链 | CXL firmware、Linux memory management、NUMA、PCIe protocol、BMC/Redfish 交叉人才稀缺 | 早期客户支持成本高，限制中小厂商扩张 |

### 4.3 BOM 与单位成本拆分

| 产品 | 估算 BOM/成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| CXL DDR5 module / EDSFF | DRAM 60-75%；CXL controller 10-18%；PCB/EDSFF/power/thermal 5-10%；测试认证/firmware 5-8%；组装物流 3-5% | DRAM ASP、容量、controller 性能、RHEL/OEM 认证、早期供给稀缺 | DRAM 价格通过 module ASP 向下游传导；若客户 TCO 节省明显，厂商可保留部分溢价 |
| CXL AIC with RDIMM slots | Controller 15-25%；PCB/connector/power/thermal 20-30%；客户自配 RDIMM 30-50%；软件/测试 5-10% | 灵活性、兼容性、散热设计、支持 DIMM QVL 范围 | 系统厂按整卡定价，内存价格部分由客户自己承担 |
| CXL controller chip | 晶圆/封测 25-40%；IP/NRE/firmware/RAS 20-30%；销售支持/认证 10-15%；毛利空间 65-78% | design win、SerDes、DDR channel、capacity、compression、telemetry、安全 | 按通道数、lane、容量上限、软件包定价；通过模组/OEM 拉货 |
| CXL switch/fabric chip | Switch ASIC 25-40%；retimer/cable/PHY/IP 15-25%；firmware/fabric manager 10-20%；系统测试 10%+ | radix/lane count、aggregate bandwidth、latency、fabric management、AI workload benchmark | rack-level 架构锁定后按 switch ASIC + software support 高 ASP 定价 |
| Pooling appliance/chassis | CXL switch 20-35%；CXL memory modules 30-50%；chassis/power/cooling/cables 15-25%；software/support 5-15% | validated solution、部署速度、企业支持、TCO 模型 | 按容量 TB、host 数、SLA/support、software subscription 定价 |
| CXL software | 研发/支持/云集成占大头；边际成本低 | 是否进入生产 fleet、是否与硬件绑定、是否有 telemetry 数据闭环 | enterprise support、per-node/per-TB license、cloud internal chargeback |

## 5. 竞争格局与可量化壁垒

### 5.1 市场结构与集中度

| 价值链层级 | 头部集中度估计 | 头部公司 | 竞争状态 |
|---|---|---|---|
| DRAM/CXL memory module | Top 3 memory vendors >80% | Samsung、Micron、SK hynix | 强寡头；DRAM 供应与客户认证决定份额 |
| CXL controller | Top 5 >70-85% | Astera、Marvell、Montage、Microchip、ScaleFlux/SMART 生态 | 高速成长、design win 锁定强；Astera/Marvell 领先 cloud/AI 叙事 |
| CXL switch/fabric | Top 4 >75% | Marvell/XConn、Microchip、Astera、Broadcom/PLX | 2026 仍早期；2027 rack pooling 后集中度可能更高 |
| System/appliance | 分散，但大客户偏头部 OEM/ODM | Dell、HPE、Lenovo、Supermicro、Gigabyte、AIC、H3、Wiwynn、Quanta | 认证与客户关系强，毛利较硅片低 |
| Software/orchestration | 显性商业市场分散，云内部化高 | Microsoft、Red Hat/Linux、MemVerge、UnifabriX、H3、Liqid、VMware/Broadcom | 高毛利但可见收入不一定高；云厂商会自研 |
| IP/EDA/verification | 高集中 | Synopsys、Cadence、Rambus、Siemens EDA、Keysight、Teledyne LeCroy | 工具链/合规强壁垒，受益于 CXL 3.x/4.0 design-in |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 具体解释 | 定价逻辑 |
|---|---|---|
| 标准与合规壁垒 | CXL 2.0/3.x/4.0、PCIe 5/6/7、IDE/TSP/RAS、Integrators List、RHEL/OEM certification | 客户为“可生产部署”付费，不只为 datasheet 付费 |
| 互操作壁垒 | CPU、BIOS、controller、DDR vendor、switch、retimer、OS、hypervisor 任一环出问题都会影响稳定性 | 已验证组合能缩短客户导入周期，带来溢价 |
| Firmware/RAS 壁垒 | ECC、poison handling、PPR、secure erase、telemetry、BMC/Redfish、fleet diagnostics | 数据中心愿意为低故障率和可观测性付高 ASP |
| 软件生态壁垒 | NUMA tiering、hot page migration、Kubernetes NRI、VM memory hotplug、application hint | CXL 的 TCO 需要软件释放；软件成熟度能决定硬件是否成交 |
| 客户锁定 | 一旦某 controller/switch 进入 cloud fleet，后续 BIOS、daemon、monitoring、spares、SLA 难快速替换 | design win 后 revenue visibility 强 |
| DRAM 供应壁垒 | 高容量 DDR5/RDIMM 和测试认证在内存三巨头手中 | 供给紧张时，module ASP 和交付优先级可定价 |
| 规模壁垒 | Hyperscaler qualification、长期供货、现场支持和 failure analysis 需要规模 | 小厂难承担大客户 NRE 与支持成本 |
| 安全/多租户壁垒 | 共享内存池如果隔离失败后果严重 | 云客户会倾向买成熟大厂方案 |

### 5.3 价值捕获：哪一层可能长期高 ROIC/高毛利

1. **第一梯队：CXL controller/switch/fabric silicon + firmware**  
   毛利率可长期维持 65-78%，原因是它同时拥有高速 SerDes、协议、RAS、telemetry、firmware、互操作认证、客户 design win。Astera/Marvell/Montage/Microchip 是核心观察对象。

2. **第二梯队：IP/verification/compliance 工具链**  
   Synopsys、Cadence、Rambus、Keysight、Teledyne LeCroy、Tektronix、GRL 等受益于 CXL 3.x/4.0、PCIe 6/7 的复杂度上升，毛利高，但 TAM 小于硬件。

3. **第三梯队：DRAM/CXL module**  
   2026 内存景气下利润率很高，但长期有周期性。Samsung/Micron/SK hynix 的优势是 DRAM 供给与客户认证，不是单纯 CXL 控制器。

4. **第四梯队：software/orchestration**  
   理论毛利最高，但商业化容易被 cloud internalization 稀释。真正赚钱的模式可能是与硬件绑定的 fleet manager、enterprise support、memory-as-a-service control plane。

5. **第五梯队：system/appliance/OEM**  
   收入弹性可观，但毛利通常 20-35%，更像把多个高毛利部件集成并交付，长期 ROIC 取决于客户关系和解决方案能力。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 6.1 2026 最可能发生的三个拐点

1. **Azure CXL M-series preview 是否走向 GA**  
   这是 2026 最大单一验证点。如果 Azure 在 2026H2 公布 GA、客户案例、SKU 定价或 SAP/IMDB 性能数据，CXL 将从“企业硬件选项”升级为“云服务 SKU”。最直接受益：Astera、Micron/Samsung/SK hynix、Intel Xeon 6、Red Hat/OEM。

2. **Marvell Structera S 30260 2026Q3 sampling 与 design win**  
   CXL 2.0 memory expansion 是单机扩容；CXL 3.0 switch 是 rack-level pooling。若 Marvell 在 2026Q3 后披露客户 sampling 或 2027 production ramp，市场会重新定价 CXL switch/fabric 的 TAM。最直接受益：Marvell/XConn、retimer/cable、fabric manager、H3/UnifabriX/Liqid。

3. **DRAM 紧缺让 CXL pooling ROI 反而变强**  
   直觉是 DRAM 涨价会压制 CXL 模组，但如果企业/云厂商面对本地 DRAM 过配与 stranded memory，pooling 可节省 30-40% AI inference memory CapEx 的叙事会更强。最直接受益：memory module、controller、pooling software。

### 6.2 2026 最可能放量的子方向排序

| 排名 | 子方向 | 放量理由 | 2026 判断 |
|---:|---|---|---|
| 1 | CXL 2.0 Type-3 memory module | 已有 Micron/Samsung/SK hynix 产品与认证，CPU host 支持到位 | small-to-mid production |
| 2 | CXL smart memory controller | 随 module/Azure/OEM 放量，毛利高 | 高确定性 |
| 3 | CXL OS certification / BIOS interleaving | 没有软件就无法生产部署 | 硬件销售前置条件 |
| 4 | CXL 2.0 switch/pooling appliance | H3/MemVerge/OCP demo 已多轮出现 | enterprise pilot |
| 5 | CXL 3.0 rack pooling switch | Marvell 2026Q3 sample | 订单弹性先于收入 |

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 7.1 2027 最可能发生的三个拐点

1. **CXL 从单机扩内存转向 rack-level dynamic pooling**  
   2027 若 CXL 3.x switch、DCD、MLD、fabric manager 成熟，CXL 价值将从“多插几百 GB/TB”转向“整个 rack 的 memory utilization 提升”。这会显著放大 switch/fabric silicon 和软件控制面的价值。

2. **CXL-aware KV cache / RAG / vector DB 出现生产案例**  
   一旦 vLLM、FAISS、Milvus、pgvector、LlamaIndex、RAG runtime 或云内部 runtime 支持 CXL memory tier，CXL 市场叙事会从数据库/HPC 扩展到 AI inference 主航道。

3. **Open AI rack / custom ASIC rack 与 CXL memory fabric 共存**  
   2027 的 AI 芯片不只有 NVIDIA Rubin，还有 AMD MI400、Trainium3/4、TPU8、Maia、MTIA、OpenAI/Broadcom XPU。非 NVIDIA rack 更愿意采用开放互联和标准化 memory fabric，CXL/UALink/UEC 可能共同受益。

### 7.2 2027 最可能放量的子方向排序

| 排名 | 子方向 | 为什么 2027 放量概率高 |
|---:|---|---|
| 1 | CXL 3.x switch-based pooling | 2026Q3 sampling 后进入 2027 production window；AI rack memory wall 更明显 |
| 2 | CXL memory-as-a-service / cloud SKU | Azure preview 若成功，AWS/GCP/Oracle/Meta 有跟进压力 |
| 3 | CXL-PNM / near-memory vector/KV | LLM inference/RAG 需要减少数据移动，PNM 的 5x 级 PoC 足够吸引架构团队 |
| 4 | CXL hybrid DRAM+NAND | Optane 后 persistent memory 空位仍在，DRAM 涨价会提升低成本大容量层价值 |
| 5 | CXL 4.0 IP/PHY/VIP | 128GT/s 设计导入，收入先体现在 IP/EDA/SerDes/测试 |

## 8. 头部公司与细分领域公司清单

### 8.1 标准、CPU host、平台生态

| 细分 | 公司/组织 | 位置 |
|---|---|---|
| 标准组织 | CXL Consortium、PCI-SIG、OCP、DMTF、JEDEC | CXL/PCIe/管理接口/内存形态标准 |
| CPU host | Intel、AMD、Arm server ecosystem、NVIDIA Grace（更多是 NVLink-C2C）、Ampere、Fujitsu | CXL host root complex、CXL 2.0/3.x/PCIe lanes |
| 云厂商/超大客户 | Microsoft Azure、AWS、Google Cloud、Meta、Oracle Cloud、CoreWeave、xAI/OpenAI ecosystem、Anthropic | 真实需求与 qualification 决定放量 |

### 8.2 CXL memory module / DRAM / hybrid memory

| 公司 | 产品/优势 |
|---|---|
| Samsung Electronics | CMM-D MD220、CMM-H PM/TM、HBM/DDR5/CXL 全栈；CMM-D 最高 256GB、CXL 2.0、PCIe 5.0、EDSFF E3.S |
| Micron | CZ120 已量产出货、CZ122 samples、RHEL 9.3 certification、Intel/AMD/OEM 测试、CERN/HPC 生态 |
| SK hynix | CMM DDR5 96GB 客户验证、HBM/DDR5 供应能力、CXL 4.0 支持声明 |
| SMART Modular | CXL AIC/module、与 H3/Gigabyte/企业系统集成可能性 |
| Netlist | HybriDIMM/内存扩展相关专利与潜在 CXL NV/hybrid 方向，商业化需验证 |
| Kioxia / Western Digital / Solidigm | 可能围绕 CXL-attached storage/persistent tier/SSD cache 发展，但 2026 不是主线 |

### 8.3 CXL controller / switch / retimer silicon

| 公司 | 产品/优势 |
|---|---|
| Astera Labs | Leo CXL smart memory controller；Azure M-series preview；Aries retimer、Scorpio AI fabric、COSMOS telemetry；高毛利 connectivity 平台 |
| Marvell | Structera X/A/S CXL portfolio、XConn acquisition、CXL 3.0 260-lane switch、Alaska P retimers、custom silicon/IP |
| XConn Technologies | CXL/PCIe switch 技术，已被 Marvell 收购；Apollo 生态历史积累 |
| Montage Technology（澜起科技） | MXC CXL Memory eXpander Controller；CXL 2.0 integrators list；CXL 3.1 MXC sampling，DDR5/PCIe/CXL 控制器优势 |
| Microchip | SMC 2000/2100 CXL smart memory controller、Switchtec PCIe/CXL switching、PM8712 等 |
| Broadcom/PLX | PCIe switch、SerDes、custom ASIC 生态；CXL 相关能力可与 custom XPU 结合 |
| ScaleFlux | MC500 memory controller、CXL 3.1 interoperability demo 方向 |
| Rambus | CXL 3.1 controller IP、PCIe/CXL security、interface IP |
| Synopsys | CXL controller/VIP/IDE security、PCIe 6/7 IP、verification |
| Cadence | PCIe/CXL PHY/IP/verification、SerDes |
| Siemens EDA / Avery / Alphawave Semi | verification/IP/SerDes 相关生态 |

### 8.4 系统、服务器、内存池化 appliance

| 公司 | 产品/优势 |
|---|---|
| Dell Technologies | 高端服务器、AI server、企业客户渠道；CXL 未来 attach 取决于平台认证 |
| HPE | ProLiant/Cray/HPC 与 memory-centric workloads |
| Lenovo | ThinkSystem/HPC/企业客户 |
| Supermicro | 快速导入新平台、Petascale/Micron CXL 案例生态 |
| Gigabyte | AI TOP CXL R5X4 工作站扩展卡，CXL 从服务器向工作站/edge AI 外溢的信号 |
| AIC | H3 Platform 合作、CXL chassis/system integration |
| H3 Platform | CXL memory sharing/pooling platform，FMS/OCP demos，5TB+ pool、multi-host 演示 |
| UnifabriX | MAX Memory over Fabrics，面向 AI/HPC，2U 32TB DDR5、可扩 256TB、software-defined memory fabric |
| Liqid | composable infrastructure、dynamic memory pooling，CXL 4.0 支持声明 |
| GigaIO | composable PCIe/CXL fabric 思路，需看 CXL 产品化 |
| Wiwynn / Quanta / Inventec / Foxconn | hyperscaler ODM，若 CXL 进入云 rack，ODM 会承担集成交付 |

### 8.5 软件、云、OS、管理面

| 公司/项目 | 位置 |
|---|---|
| Microsoft Azure | 首个公开 CXL-attached memory 云 VM private preview；若 GA 将是最大催化 |
| Red Hat | RHEL 9.3 CXL certification、KVM/QEMU、多租户支持 |
| Linux kernel | CXL driver、memory hotplug、NUMA tiering、page interleaving、DAMON/AutoNUMA 类机制 |
| MemVerge | Memory Machine X，CXL memory expansion/pooling/fabric-attached memory software |
| UnifabriX | Fabric manager、software-defined autonomous tiering |
| H3 Platform | CLI/GUI memory allocation、Virtual CXL Switch、pooling management |
| VMware/Broadcom | enterprise virtualization memory tiering 潜在受益 |
| Kubernetes / containerd / CRI-O / OCP NRI | pod lifecycle memory allocation，Pangaea-like orchestration 所在层 |
| DMTF Redfish / OCP DCMFM | fabric/resource management API |

### 8.6 测试认证与设备

| 公司/机构 | 位置 |
|---|---|
| CXL Consortium Integrators List | CXL 合规与互操作背书 |
| PCI-SIG | PCIe 5/6/7 PHY/protocol 基础 |
| UNH-IOL、Granite River Labs、Allion | compliance lab |
| Keysight、Teledyne LeCroy、Tektronix、Anritsu | protocol analyzer、oscilloscope、BERT、CXL/PCIe compliance |
| Advantest、Teradyne、FormFactor | ATE/probe/test，间接受益于 controller/HBM/SerDes 测试复杂度 |

## 9. 情景模型：2026-2028 总收入池与投资排序

### 9.1 总市场三情景

| 口径 | 2026E 基准 | 2026E 乐观 | 2026E 极度超预期 | 2027E 基准 | 2027E 乐观 | 2027E 极度超预期 |
|---|---:|---:|---:|---:|---:|---:|
| CXL memory expansion hardware | $1.6-2.2B | $2.5-3.5B | $4-6B | $2.5-4B | $5-8B | $9-14B |
| CXL component/controller/switch | $2.5-3.5B | $3.8-5.5B | $6-8B | $4-6B | $7-11B | $12-20B |
| CXL pooling appliance/software | $0.2-0.6B | $0.6-1.2B | $1.2-2.5B | $0.8-2B | $2-5B | $6-10B |
| CXL-enabled cloud service premium | $0.2-0.8B | $0.8-1.8B | $2-3.5B | $1-3B | $3-7B | $8-15B |
| 合计可跟踪收入池（避免重复后） | $3-5B | $5-8B | $8-13B | $6-10B | $12-20B | $22-35B |

### 9.2 投资排序

| 排名 | 方向 | 逻辑 | 核心跟踪指标 |
|---:|---|---|---|
| 1 | CXL controller/switch silicon | 高毛利、高壁垒、design win 粘性；2027 rack pooling 带来 TAM 重估 | Astera/Marvell/Montage/Microchip 的 CXL revenue、gross margin、sampling/design win |
| 2 | CXL memory modules + DRAM suppliers | 已有产品与认证，受益于 DRAM 高景气和 memory expansion | CZ120/CZ122/CMM-D 出货、Azure GA、RHEL/OEM certified configs |
| 3 | CXL rack pooling appliance/fabric manager | 2027 弹性大，能把 CXL 从单机扩容变成 rack memory pool | Marvell S30260 sampling、H3/UnifabriX/Liqid 客户案例 |
| 4 | Software/OS tiering | 决定硬件能否 scale；毛利高但商业收入可见性低 | Linux/RHEL/Kubernetes CXL features、MemVerge/UnifabriX/H3 付费客户 |
| 5 | IP/EDA/test | CXL 4.0/PCIe 7 增加验证复杂度，稳定高毛利 | CXL 3.1/4.0 IP license、PCIe 7/8 compliance tool 订单 |

## 10. 未来 12 个月跟踪清单

1. Azure M-series CXL private preview 是否 GA；是否公布 SAP HANA、IMDB、RAG、AI inference 客户案例。  
2. AWS/GCP/Oracle/Meta 是否公开 CXL-backed VM、bare-metal、memory tier 或内部论文。  
3. Micron CZ122 是否从 samples 进入 production，CZ120/CZ122 出货是否扩展到更多 OEM。  
4. Samsung CMM-D 是否从 256GB 走向 512GB/1TB，CMM-H 是否进入 customer evaluation。  
5. Marvell Structera S 30260 2026Q3 sampling 后是否披露 design win；S 20256 production 量级。  
6. Astera Leo CXL 在 Azure 之外是否获得第二个 cloud/hyperscaler 客户。  
7. Montage CXL 3.1 MXC 是否获得 key customer sampling 反馈与量产时间表。  
8. Linux/RHEL/Kubernetes 是否合入 CHMU/hot page tiering/DCD/fabric management 更成熟功能。  
9. vLLM/FAISS/Milvus/pgvector/LlamaIndex 是否出现 CXL-aware memory tier 或 CXL-PNM benchmark。  
10. DRAM 合约价、server DDR5 交期、HBM 产能分配是否继续推高 CXL pooling ROI。  

## 11. 主要来源索引

### 标准与论坛

- CXL Consortium About CXL and CXL 4.0 features: https://computeexpresslink.org/about-cxl/  
- CXL 4.0 Specification Q&A recap, January 2026: https://computeexpresslink.org/blog/introducing-the-cxl-4-0-specification-webinar-qa-recap-4386/  
- CXL 3.x Specification Q&A recap, March 2025: https://computeexpresslink.org/blog/an-overview-of-the-cxl-3-x-specification-webinar-qa-recap-3624/  
- CXL Consortium Webinar: Vertical Optimization of the CXL Stack, April 1 2026: https://computeexpresslink.org/event/overcoming-cxl-limitations-enabling-cxl-hardware-and-software-as-vertical-optimization-technologies/  
- CXL 4.0 Specification Release PDF: https://computeexpresslink.org/wp-content/uploads/2025/11/CXL_4.0-Specification-Release_FINAL_Website-Copy.pdf  

### 公司一手资料

- Astera Labs Leo CXL on Microsoft Azure M-series preview: https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-leo-cxl-smart-memory-controllers-microsoft-azure-m  
- Astera Labs Leo CXL Smart Memory Controllers product page: https://www.asteralabs.com/products/leo-cxl-smart-memory-controllers/  
- Astera Labs Q1 2026 financial results: https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results  
- Micron CXL memory product page: https://www.micron.com/products/memory/cxl-memory  
- Micron CZ122 and RHEL certification: https://www.micron.com/about/blog/applications/data-center/introducing-micron-cz122-and-red-hat-certification-of-memory-expansion-portfolio  
- Micron CXL Memory Expansion white paper: https://www.micron.com/content/dam/micron/global/public/products/white-paper/cxl-memory-expansion-a-close-look-on-actual-platform.pdf  
- Samsung CMM-D product page: https://semiconductor.samsung.com/cxl-memory/cmm-d/  
- Samsung MD220 detail: https://semiconductor.samsung.com/cxl-memory/cmm-d/md220/  
- Samsung CMM-D IMDB blog / white paper link: https://semiconductor.samsung.com/news-events/tech-blog/breaking-the-memory-wall-with-samsung-cmm-d-for-next-generation-imdb-infrastructure/  
- Samsung CMM-H tech blog: https://semiconductor.samsung.com/us/news-events/tech-blog/samsung-cxl-solutions-cmm-h/  
- SK hynix CXL DDR5 customer validation: https://news.skhynix.com/sk-hynix-completes-customer-validation-of-cxl-based-ddr5/  
- Marvell Structera S CXL switch, OFC 2026: https://investor.marvell.com/news-events/press-releases/detail/1017/marvell-launches-next-generation-cxl-switch-enabling-memory-pooling-to-break-through-the-ai-memory-wall  
- Marvell Structera interoperability: https://www.marvell.com/company/newsroom/marvell-extends-cxl-ecosystem-leadership-with-structera-interoperability-across-platforms.html  
- Marvell CXL product page: https://www.marvell.com/products/cxl.html  
- Montage CXL 3.1 MXC: https://www.montage-tech.com/Press_Releases/20250901  
- Montage CXL 2.0 integrators list milestone: https://www.montage-tech.com/Press_Releases/20250121  
- Microchip CXL Smart Memory Controllers: https://www.microchip.com/en-us/about/news-releases/products/cxl-smart-memory-controllers  
- Intel Xeon 6 product brief: https://www.intel.com/content/www/us/en/products/docs/xeon-6-product-brief.html  
- Intel/Micron Xeon 6 CXL paper: https://www.intel.com/content/www/us/en/content-details/842211/optimizing-system-memory-bandwidth-with-micron-cxl-memory-expansion-modules-on-intel-xeon-6-processors.html  
- AMD EPYC 9005 architecture overview PDF: https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/user-guides/58462_amd-epyc-9005-tg-architecture-overview.pdf  
- H3 Platform FMS 2025 CXL memory sharing/pooling: https://www.h3platform.com/newsroom/press-release-detail/86  
- H3 Platform OCP 2025 CXL demos: https://www.h3platform.com/newsroom/press-release-detail/87  
- MemVerge CXL resource page: https://memverge.com/cxl/  
- UnifabriX product page: https://www.unifabrix.com/product  
- UnifabriX MAX overview: https://unifabrix.tech/  
- Rambus CXL 3.1 controller IP: https://www.rambus.com/interface-ip/cxl/cxl3-controller/  
- Synopsys CXL controller IP: https://www.synopsys.com/designware-ip/interface-ip/cxl/cxl-controller.html  
- 本项目本地 AI 芯片路线参考：`D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`  

### 市场报告与第三方资料

- Strategic Market Research CXL component market: https://www.strategicmarketresearch.com/market-report/compute-express-link-component-market  
- MarketIntelo CXL memory expansion market: https://marketintelo.com/report/cxl-memory-expansion-market  
- GMI Compute Express Link component market: https://www.gminsights.com/industry-analysis/compute-express-link-component-market  
- TrendForce 2026 memory pricing survey: https://www.trendforce.com/presscenter/news/20260331-12995.html  
- Micron CXL impact on DRAM bit growth white paper: https://www.micron.com/content/dam/micron/global/public/about/cxl-impact-dram-bit-growth-white-paper.pdf  

### 学术/技术论文

- CXLRAMSim v1.0, 2026: https://arxiv.org/abs/2603.29483  
- Equilibria: Fair Multi-Tenant CXL Memory Tiering At Scale, 2026: https://arxiv.org/abs/2602.08800  
- CCCL: Node-Spanning GPU Collectives with CXL Memory Pooling, 2026: https://arxiv.org/abs/2602.22457  
- Amplifying Effective CXL Memory Bandwidth for LLM Inference via Transparent Near-Data Processing, 2025: https://arxiv.org/abs/2509.03377  
- Memory Sharing with CXL: Hardware and Software Design Approaches, 2024: https://arxiv.org/abs/2404.03245  
- An Introduction to the Compute Express Link Interconnect, 2023: https://arxiv.org/abs/2306.11227  

## 12. 读数注意事项

1. CXL 市场很早期，很多厂商未单独披露收入；本文的细分规模大量来自“公开市场报告锚点 + 公司产品状态 + AI 基建乐观假设”的组合推算。  
2. CXL memory expansion、CXL component、cloud service premium 之间存在重复计算风险；因此总市场表中已做粗略去重，单项表可作为细分弹性观察。  
3. 极度乐观情景本质上假设：2026-2027 AI 推理/KV cache 需求继续超预期、DRAM/HBM 紧缺延续、Azure CXL preview 成功、至少一家其他 CSP 跟进、CXL 3.x switch pooling 进入早期生产。  
4. 最大下行风险：AI 推理 ROI 被证伪、DRAM 价格快速回落、Azure preview 不转 GA、CXL latency/software 难题导致客户延期、NVIDIA/云厂商封闭 memory fabric 吃掉开放 CXL 的空间。  
# 行业调研：【EDA工具、接口IP与Chiplet IP】

> 截至：2026-05-08  
> 口径：本报告把“EDA工具”定义为数字/模拟/验证/物理实现/DFT/SLM/多物理场/3DIC工具与EDA云，把“接口IP”定义为PCIe/CXL/Ethernet/UALink/UCIe/DDR/HBM/LPDDR/MIPI/USB/SerDes/Retimer相关IP与VIP，把“Chiplet IP”定义为D2D PHY、UCIe/BoW/CHI C2C、NoC、RoT/管理、安全、DFT/KGD/SLM、3DIC/package-aware设计平台和可复用I/O/memory/accelerator chiplet。  
> 投资判断基调：对2026-2027 AI计算中心建设保持非常乐观。直接数据缺失处采用“AI rack、HBM4、CoWoS、1.6T光互连、自研ASIC同步放量”的偏乐观假设。本文不是投资建议。

## 一页结论

2026年这个行业的核心机会不是“EDA行业正常随半导体增长”，而是AI基础设施把芯片设计的瓶颈从单颗SoC推到系统级：GPU/ASIC要同时解决HBM4、CoWoS/SoIC、UCIe/D2D、224G/448G SerDes、PCIe 7/8、CXL 4.0、UALink/ESUN、CPO/光I/O、液冷功耗、硬件安全和量产测试。每一个瓶颈都会增加EDA license、仿真算力、接口IP授权、VIP、test chip、signoff和工程服务预算。

最确定的收入池是三层：

| 层级 | 2026判断 | 2027判断 | 毛利/定价能力 |
|---|---|---|---|
| EDA工具与EDA云 | SEMI EDMD口径2025全年约212亿美元，Q4 2025达54.663亿美元、同比+10.3%；AI验证、3DIC、多物理场、硬件安全把增速从10%附近推向12-18% | 若agentic EDA进入验证/实现闭环，行业可冲15-22%增长 | 软件毛利通常75-90%，头部经营利润率30-45%；AI add-on、云仿真、signoff最能提ASP |
| 接口IP | SIP Q4 2025为20.832亿美元、同比+18.3%；高端接口IP明显跑赢普通EDA | HBM4E、PCIe 7、CXL 4、UCIe 3.0、224G/448G、1.6T/3.2T Ethernet持续拉动 | IP毛利80-95%；先进节点PHY需要硅验证和客户绑定，价格弹性强 |
| Chiplet/3DIC IP与设计平台 | 2026是设计导入年，真实收入小于HBM/封装，但战略卡位极强 | 2027随Rubin、MI400/Helios、TPU8、Trainium3/4、Meta/OpenAI/Broadcom XPU扩大 | 高端D2D PHY/IP/VIP/SLM 70-90%毛利；先进封装制造20-45%毛利，取决于产能稀缺 |

最值得跟踪的2026新增信号：

- Synopsys 2026Q1收入24.09亿美元，同比从14.55亿美元大幅上升，FY2026收入中位数96.1亿美元，含Ansys约29亿美元。Synopsys/Ansys合并把“芯片EDA”扩展到“硅到系统、多物理场、热/电/机械/封装协同”。
- Cadence 2026Q1收入14.742亿美元，Q1 backlog达80亿美元，未来12个月RPO约40亿美元，并上调2026收入展望到约17%同比增长；CEO直接把增长归因到AI需求和AI-driven portfolio。
- SEMI ESD Alliance：2025Q4电子系统设计行业收入54.663亿美元，同比+10.3%；SIP收入20.832亿美元，同比+18.3%；全球相关员工71517人，同比+13.8%。
- Broadcom 2026Q1 AI收入84亿美元，同比+106%，由custom AI accelerator与AI networking驱动；OpenAI/Broadcom 10GW自研加速器从2026H2开始部署、2029年底完成；Meta/Broadcom MTIA首期超过1GW，后续多GW。
- UCIe 3.0已发布，速率到64GT/s，重点不只是更快，而是增强manageability；PCIe 7.0已进入128GT/s设计导入，PCIe 8.0 draft 0.5目标256GT/s、x16双向1TB/s、2028 final；CXL 4.0基于PCIe 7.0；UALink 2.0已把AI scale-up开放生态推到UCIe 3.0兼容方向。

一句话：2026最可能放量的技术路径是“封闭/半封闭chiplet + 高端接口IP + package-aware EDA”，不是完全开放chiplet marketplace。真正赚钱的是工具链、IP、验证、测试、封装协同和客户锁定。

## 信息源地图：论坛、报告、公告与订单信号

| 信息类型 | 2026关键信号 | 对本报告的用途 |
|---|---|---|
| 业内论坛：Chiplet Summit 2026 | UCIe 3.0、HBM4/Custom HBM、1000-chiplet challenge、Siemens/Synopsys/Cadence/Intel密集参与；Best of Show给到Siemens Innovator3D IC、UCIe 3.0 | 判断Chiplet从“PHY标准”升级到“管理、安全、DFT、KGD、固件、供应链责任”的系统级市场 |
| 业内论坛：DesignCon 2026 | 224G进入部署、448G进入工程探路、PCIe 7验证、PCIe 8 256GT/s demo、1.6T、top-side/CPC/AEC、agentic SI/PI | 判断2026接口IP先于终端产品确认收入；T&M/SerDes/连接器/EDA先受益 |
| 业内论坛：PCI-SIG DevCon 2026 | PCIe 8.0 draft 0.5，目标256GT/s、x16双向1TB/s、2028 final；PCIe 7 over optics进入标准路径 | 判断PCIe 8虽非2026收入主角，但会立刻改变IP、PHY、连接器、retimer研发预算 |
| 业内论坛：OCP EMEA 2026 | FCSA 1.0、Open Data Center for AI、UALink/ESUN/SUE-T、Caliptra/LOCK/SOLID/openSFI、800G/1.6T、OCS/CPO | 判断开放AI基础设施会把chiplet、固件安全、scale-up互连写进RFP |
| 公司公告：Synopsys/Cadence | Synopsys FY2026收入中位数96.1亿美元，含Ansys 29亿美元；Cadence 2026Q1 backlog 80亿美元、收入展望约+17% | 证明EDA/IP不是“滞后半导体周期”，而是在AI设计复杂度上行中有订单可见度 |
| 公司公告：Broadcom/OpenAI/Meta | OpenAI/Broadcom 10GW，2026H2开始；Meta/Broadcom MTIA首期>1GW、后续多GW；Broadcom 2026Q1 AI收入84亿美元、同比+106% | 证明custom ASIC/XPU已变成独立产能池，直接拉动接口IP和EDA |
| 公司公告：Rambus/Marvell/Lightmatter | Rambus HBM4E controller 16Gbps/pin、100+ HBM设计赢单；Marvell PCIe 8 SerDes 256GT/s；Lightmatter/Synopsys集成224G SerDes与UCIe到3D CPO | 锚定“正在放量/正在设计导入”的关键产品 |
| 行业报告：SEMI EDMD | 2025Q4 ESD行业收入54.663亿美元、同比+10.3%；SIP收入20.832亿美元、同比+18.3% | 作为EDA/IP市场规模主锚 |
| 行业报告/二级口径：Yole、TrendForce、Cignal AI等 | HBM、advanced packaging、CoWoS、800G/1.6T光模块、AI server价值链多口径估算 | 用于交叉验证市场规模，避免只采单一报告 |
| 非正式/市场口径 | Broadcom 2027 AI芯片收入可能超过1000亿美元、六大客户等说法来自市场与媒体口径，需与官方AI收入和GW公告交叉验证 | 仅用于乐观/极度乐观上沿，不作为基准直接事实 |

## 1. AI计算中心大建设下的机遇、挑战与技术路径

### 1.1 需求侧：AI芯片路线把EDA/IP预算前置

项目内已有AI芯片研究显示，2026-2027出货与价值权重最大的AI芯片/平台包括：NVIDIA B300/GB300 Blackwell Ultra、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon MLU590/690、AMD MI350、AWS Trainium3、Meta MTIA 300/400/450/500、Microsoft Maia 200，以及2026H2起步的AMD MI400/Helios、NVIDIA Rubin、OpenAI/Broadcom accelerator。它们共同指向同一组设计变量：

| AI平台 | 对EDA/IP的拉动 | 2026-2027关键接口/封装 |
|---|---|---|
| NVIDIA GB300/B300 | 机柜级设计、HBM3E、NVLink、800G/1.6T scale-out、液冷和电源完整性；拉动系统仿真、热/电/SI/PI工具 | TSMC 4NP、CoWoS-L/S、HBM3E、224G SerDes、PCIe/CXL辅助接口 |
| NVIDIA Rubin/Vera Rubin | HBM4、CPO、Spectrum-6、BlueField-4、NVLink新代际；拉动HBM4 PHY/controller、CPO/硅光仿真、多die signoff | HBM4、3nm/先进封装、CPO/1.6T、PCIe Gen6/7周边 |
| Google TPU Ironwood/TPU8 | 自研互连、HBM、推理优先，Broadcom/TSMC生态；拉动custom silicon EDA、HBM、SerDes、NoC、SLM | 先进节点、HBM3E/HBM4、2.5D封装、800G+光互连 |
| AWS Trainium2/3/4 | NeuronLink/NeuronSwitch、EFA、NVLink Fusion方向；拉动定制NoC、以太网/PCIe/CXL、系统验证 | Trainium3 3nm、144芯片UltraServer、PCIe/Ethernet/专有fabric |
| Meta MTIA + Broadcom XPU | 初始>1GW、多GW路线，四代MTIA；拉动XPU平台化、SerDes、HBM、RoT、验证服务 | Broadcom XPU、TSMC先进制程、Ethernet/SerDes、chiplet封装 |
| OpenAI/Broadcom accelerator | 10GW，2026H2开始；推理优先但架构可能逐代扩到训练；拉动Arm CPU IP、custom ASIC、networking IP | Broadcom racks、custom accelerator、HBM/SerDes/PCIe/CXL/以太网 |
| AMD MI350/MI400 Helios | MI350在2026放量，MI400/Helios 2026H2首批、2027更大弹性；拉动HBM4、UALink/open rack、Pensando网络 | HBM3E到HBM4、72 GPU rack、UALink/以太网、2.5D/CoWoS |
| Microsoft Maia 200 | 3nm、216GB HBM3E、7TB/s、闭环液冷；Azure内部推理 | HBM3E、3nm、先进封装、Azure rack验证 |

对EDA/IP的含义：这些平台越走向rack-scale，越不能只买传统RTL/PNR工具，而要买“架构探索、接口IP、VIP、硬件/软件协同仿真、3DIC热/电/机械signoff、SLM、DFT、KGD、合规和安全”。预算会更像“AI系统工程税”，而不是传统芯片设计费。

### 1.2 2026正在被使用的关键技术

| 技术 | 当前状态 | 2026最可能落地路径 |
|---|---|---|
| AI-assisted/agentic EDA | 已从代码辅助进入验证、coverage、SI/PI设置、ECO、报告解析 | 先在verification、testbench、coverage closure、physical ECO、SI/PI debug收费 |
| 多物理场EDA | Synopsys+Ansys、Cadence Celsius/Clarity/Voltus、Siemens Innovator3D IC等都在强化 | 先进封装和液冷机柜使热/电/机械/EM/IR共同进入signoff |
| HBM3E/HBM4/HBM4E IP | HBM3E主力，HBM4随Rubin/MI400/TPU8导入；Rambus已发HBM4E controller IP，称超100个HBM设计赢单 | 2026H2 HBM4验证/早期量产，2027 HBM4E设计锁定 |
| PCIe 6/7/8 | PCIe 6量产化，PCIe 7.0 128GT/s已成设计输入，PCIe 8.0 256GT/s进入pathfinding | 2026先赚IP/VIP/test/retimer钱，2027 Gen7 endpoint/retimer放量，2028后Gen8 |
| CXL 3.x/4.0 | CXL 4.0基于PCIe 7.0，AI内存池化仍慢于叙事 | 2026在memory expansion/SSD/NIC/retimer设计导入，2027随内存成本压力提升渗透 |
| UCIe 3.0/D2D | 64GT/s、增强manageability；Cadence/Synopsys/Alphawave等均布局 | 2026高端ASIC design-in，2027封闭生态内放量，开放市场仍偏慢 |
| 224G SerDes/1.6T Ethernet | 224G部署，448G pathfinding；Synopsys与TSMC披露N5/N3P/N2P上PCIe7、HBM4、224G、UCIe64G等first-silicon里程碑 | 2026 224G/1.6T成为AI网络主线，2027 448G/3.2T预研拉动T&M/IP |
| Chiplet NoC/管理/安全 | RoT、Caliptra、LOCK、openSFI、FCSA把chiplet从PHY推向系统 | 2026是RFP/验证年，2027进主权AI、欧洲云、开放ASIC采购条款 |

### 1.3 新技术成熟与放量时间：三情景

| 技术/产品 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---|---|
| Agentic EDA | 2026在验证/coverage/SI/PI助手收费；2027局部闭环 | 2026H2在大客户内网部署，debug周期缩短20-30%；2027成为高ASP模块 | 2027前在成熟节点/FPGA/accelerator子类中实现spec-to-RTL/test/初版GDSII稳定闭环 |
| HBM4/HBM4E IP | 2026H2验证和首批设计，2027放量 | 三大HBM供应商多供顺利，2027 HBM4E前置设计锁定 | HBM4供给被所有GPU/ASIC预定，HBM PHY/controller授权价格继续上行 |
| PCIe 7 IP/retimer/switch | 2026设计导入，2027量产平台 | 2026H2 Gen7 design win加速，AI rack内retimer attach rate上升 | PCIe 7在部分AI rack比传统服务器提前一年放量 |
| PCIe 8/256GT/s SerDes | 2026-2027为IP/test/connector pathfinding，2028标准完成 | 2027 hyperscaler pre-standard prototype | 2026H2专有fabric采用PCIe8-class electrical，提前带动IP和T&M订单 |
| UCIe 3.0/64G D2D | 2026设计导入，2027同生态封闭chiplet量产 | 2027成为高端AI package事实标准之一 | 2027出现多供应商plug-and-play chiplet设计流，但概率低 |
| FCSA/open chiplet | 2026标准与验证工具成熟，2027部分RFP引用 | 2027出现可复用I/O/memory/accelerator chiplet目录 | 2028前形成开放chiplet marketplace，显著降低小厂自研AI silicon门槛 |
| CPO/光I/O/photonic interposer | 2026 demo/试点，2027部分switch linecard | 2027 AI switch/OCS/CPO批量试用 | 2027因224G/448G电互连瓶颈提前触发光I/O刚需 |

2026最可能的技术路径排序：

1. 高端AI ASIC/GPU继续以封闭chiplet/2.5D/HBM封装为主，接口IP和EDA先收费。
2. HBM4、PCIe 7、224G/1.6T、UCIe 3.0成为新项目的“设计输入”，但收入确认先在IP/VIP/EDA/T&M。
3. 开放chiplet经济会被FCSA/UCIe推动，但2026-2027最现实是同一大客户/同一生态内复用，而不是完全开放货架式chiplet市场。

## 2. 已经开始放量的关键产品：规模、渗透率与利润率

### 2.1 EDA工具与EDA云

| 产品 | 当前放量状态 | 未来3个月市场规模 | 未来1年市场规模 | 未来2年市场规模 | 渗透率路径 | 利润率情景 |
|---|---|---:|---:|---:|---|---|
| 数字实现/签核：PNR、STA、功耗、IR/EM | 成熟高渗透，AI芯片复杂度拉ASP | B $4.8-5.4B / O $5.2-5.8B / X $5.8-6.5B | B $20-22B / O $22-25B / X $25-28B，含EDA大盘 | B $44-50B两年累计 / O $50-58B / X $58-68B | 先进节点客户接近100%，中小成熟节点被AI add-on拉升 | 软件GM 80-90%；经营利润B 30-40%，O 35-45%，X 40-50% |
| 验证/仿真/形式验证/硬件仿真 | AI ASIC最刚需，tapeout风险最高 | B $1.5-1.9B / O $1.8-2.2B / X $2.2-2.8B | B $6.5-8B / O $8-10B / X $10-13B | B $14-18B / O $18-24B / X $24-32B | 高端ASIC 100%采购；硬件仿真云化提升中小客户渗透 | GM 75-88%；供给紧张的仿真硬件/云时段可高溢价 |
| 3DIC/package-aware EDA | 从小基数进入强放量；Synopsys 3DIC Compiler、Cadence Integrity 3D-IC、Siemens Innovator3D IC | B $0.35-0.55B / O $0.55-0.8B / X $0.8-1.1B | B $1.8-2.5B / O $2.5-3.5B / X $3.5-5B | B $4-6B / O $6-9B / X $9-14B | 2026高端AI package渗透30-50%，2027到60-75% | GM 80-90%；因绑定封装厂/代工认证，经营利润可35-50% |
| 多物理场：热、电、机械、CFD、SI/PI | Ansys并入Synopsys后成为AI rack/3D封装必需项；Cadence/SIemens同样强化 | B $1.0-1.3B / O $1.3-1.7B / X $1.7-2.3B | B $4.5-5.5B / O $5.5-7B / X $7-9B | B $10-12B / O $12-16B / X $16-22B | 从封装工程向架构阶段前移，AI芯片项目渗透从40%升到70%+ | GM 75-88%；系统级仿真服务毛利略低但粘性高 |
| Agentic EDA | 已进入商业化初期，Cadence/Synopsys/Siemens都在把AI嵌入flow | B $0.25-0.5B / O $0.5-0.9B / X $0.9-1.5B | B $1-2B / O $2-4B / X $4-7B | B $3-6B / O $7-12B / X $12-20B | 2026先在头部客户验证/实现辅助，2027扩到中型IC团队 | 早期推理成本/R&D抵消；成熟后GM 80-90%，经营利润25-45% |

### 2.2 接口IP：高速SerDes、PCIe/CXL/以太网/HBM/UCIe

| 产品 | 当前关键事实 | 未来3个月 | 未来1年 | 未来2年 | 渗透率路径 | 利润率情景 |
|---|---|---:|---:|---:|---|---|
| PCIe 6/7 Controller+PHY+VIP | PCIe 7.0 128GT/s已是2026设计输入；Synopsys披露PCIe IP累计3000+ design wins | B $0.35-0.45B / O $0.45-0.6B / X $0.6-0.8B | B $1.5-2.0B / O $2.0-2.8B / X $2.8-4.0B | B $3.5-5B / O $5-7B / X $7-10B | Gen6量产，Gen7 2026 design-in、2027端点/retimer上量 | IP GM 85-95%；极度乐观下早期license可强溢价 |
| CXL 3.x/4.0 IP | CXL 4.0基于PCIe7，AI内存池化受DRAM/HBM涨价驱动 | B $0.15-0.25B / O $0.25-0.35B / X $0.35-0.5B | B $0.7-1.1B / O $1.1-1.6B / X $1.6-2.4B | B $1.8-3B / O $3-5B / X $5-8B | 2026扩展内存/交换/retimer导入，2027 AI服务器渗透加速 | GM 80-92%；生态复杂导致VIP/合规服务高毛利 |
| 224G SerDes/1.6T Ethernet IP | Synopsys 1.6T Ethernet IP已被多客户采用，224G PHY绑定1.6T/UALink/UEC | B $0.4-0.65B / O $0.65-0.9B / X $0.9-1.3B | B $1.8-2.6B / O $2.6-3.8B / X $3.8-5.5B | B $4-6B / O $6-9B / X $9-14B | 224G在2026部署，448G 2026 pathfinding、2027设计导入 | GM 85-95%；硅验证难度高，头部IP议价最强 |
| HBM3E/HBM4/HBM4E Controller/PHY | Rambus称HBM4E controller可达16Gbps/pin，已有100+ HBM设计赢单；Synopsys/TSMC披露HBM4 IP first-silicon | B $0.25-0.4B / O $0.4-0.6B / X $0.6-0.9B | B $1.2-1.8B / O $1.8-2.8B / X $2.8-4.2B | B $3-5B / O $5-8B / X $8-12B | 2026 HBM4设计导入，2027 HBM4E前置；高端AI ASIC attach近100% | GM 85-95%；供不应求时NRE+royalty双高 |
| UCIe/D2D PHY+Controller | UCIe 3.0 64GT/s和manageability发布；Alphawave/Synopsys/Cadence布局 | B $0.15-0.25B / O $0.25-0.4B / X $0.4-0.65B | B $0.7-1.2B / O $1.2-1.9B / X $1.9-3B | B $2-3.5B / O $3.5-6B / X $6-10B | 2026高端AI ASIC导入，2027封闭chiplet生态放量 | GM 85-95%；真正难点在package/DFT/RoT，组合销售更赚钱 |
| DDR5/MRDIMM/LPDDR6/LPDDR5X/SOCAMM接口IP | AI服务器CPU/内存侧升级，Micron等推进SOCAMM2 | B $0.2-0.3B / O $0.3-0.45B / X $0.45-0.65B | B $0.8-1.2B / O $1.2-1.8B / X $1.8-2.6B | B $2-3B / O $3-4.5B / X $4.5-6.5B | CPU、DPU、NIC、SSD控制器高渗透 | GM 80-92%；成熟标准ASP下降，但高频MRDIMM/SOCAMM溢价 |

### 2.3 Chiplet相关已经开始放量的“产品化”环节

| 产品 | 当前状态 | 未来3个月 | 未来1年 | 未来2年 | 渗透率路径 | 利润率情景 |
|---|---|---:|---:|---:|---|---|
| 3DIC/advanced packaging设计平台 | 已在CoWoS/SoIC/EMIB/2.5D项目中成为必要工具 | B $0.35-0.55B / O $0.55-0.8B / X $0.8-1.1B | B $1.8-2.5B / O $2.5-3.5B / X $3.5-5B | B $4-6B / O $6-9B / X $9-14B | AI高端封装项目渗透快速向70%+走 | 软件GM 80%+，代工认证带来客户锁定 |
| KGD/DFT/SLM/test IP | Chiplet越多，known-good-die、在线监测、老化测试越重要 | B $0.25-0.4B / O $0.4-0.6B / X $0.6-0.9B | B $1.0-1.6B / O $1.6-2.4B / X $2.4-3.6B | B $2.5-4B / O $4-6B / X $6-9B | 2026高端ASIC/HBM package标配，2027扩到更多custom silicon | IP/软件GM 75-90%；ATE/服务混合毛利45-70% |
| NoC/Chiplet fabric IP | Arteris、Baya、Sonics类NoC价值随多die上升 | B $0.15-0.25B / O $0.25-0.35B / X $0.35-0.55B | B $0.6-1B / O $1-1.5B / X $1.5-2.4B | B $1.5-2.5B / O $2.5-4B / X $4-6B | AI/汽车/边缘多die项目渗透从小基数上升 | GM 80-95%；切换成本高，长期续费/royalty好 |
| RoT/管理/安全/固件IP | Caliptra、LOCK、SOLID、openSFI把安全放进RFP | B $0.1-0.2B / O $0.2-0.35B / X $0.35-0.55B | B $0.5-0.9B / O $0.9-1.5B / X $1.5-2.5B | B $1.5-2.5B / O $2.5-4B / X $4-7B | 主权AI、欧洲云、hyperscaler供应链审计提升attach | IP/审计/工具GM 70-90%；硬件RoT单价低但attach高 |

## 3. 在研关键产品与未来高增长细分技术

### 3.1 研发/导入期技术的商业化预测

| 在研方向 | 成熟时间 | 放量时间 | 未来3个月规模 | 未来1年规模 | 未来2年规模 | 利润率预测 |
|---|---|---|---:|---:|---:|---|
| PCIe 8.0 256GT/s IP、连接器与合规工具 | 2026 draft 0.5后pathfinding，2028 final | 2027 pre-standard design win，2029+终端放量 | B $0.05-0.1B / O $0.1-0.2B / X $0.2-0.35B | B $0.2-0.5B / O $0.5-0.9B / X $0.9-1.5B | B $1-2B / O $2-3.5B / X $3.5-6B | IP/T&M 60-95%；早期价格强 |
| 448G SerDes/3.2T Ethernet | 2026 DesignCon pathfinding，2027 design-in | 2027-2028高端网络/短距先导入 | B $0.05-0.12B / O $0.12-0.25B / X $0.25-0.45B | B $0.3-0.7B / O $0.7-1.2B / X $1.2-2B | B $1.5-3B / O $3-5B / X $5-8B | PHY IP 85-95%，测试仪器60-70% |
| CPO/光I/O/photonic interposer设计IP | 2026样机/合作，2027部分平台试用 | 2027-2028若rack-scale电互连压力过大放量 | B $0.05-0.12B / O $0.12-0.25B / X $0.25-0.5B | B $0.2-0.5B / O $0.5-1B / X $1-2B | B $0.8-1.8B / O $1.8-4B / X $4-8B | 早期硬件毛利低波动，IP/EDA/仿真70-90% |
| Custom HBM base die/near-memory logic IP | 2026高端项目探索 | 2027-2028随HBM4E/ASIC放量 | B $0.1-0.2B / O $0.2-0.4B / X $0.4-0.7B | B $0.5-1B / O $1-2B / X $2-3.5B | B $2-4B / O $4-7B / X $7-12B | 高壁垒，NRE/royalty/服务组合可60-85%毛利 |
| 完整chiplet marketplace | 标准2026-2027成熟，商业责任边界仍难 | 2028+ | B <$0.1B / O $0.1-0.2B / X $0.2-0.5B | B $0.3-0.8B / O $0.8-1.5B / X $1.5-3B | B $1-3B / O $3-7B / X $7-15B | 平台/IP高毛利，但初期认证和库存风险高 |
| AI-native EDA闭环代理 | 2026验证/SI/PI可用，2027局部实现闭环 | 2027-2028规模收费 | B $0.25-0.5B / O $0.5-0.9B / X $0.9-1.5B | B $1-2B / O $2-4B / X $4-7B | B $3-6B / O $7-12B / X $12-20B | 成熟后软件GM 80-90%；推理成本会压低早期经营利润 |

### 3.2 未来两年最可能快速增长的产品组合

1. HBM4/HBM4E controller/PHY + 3DIC signoff + KGD测试。  
最强原因：Rubin、MI400、TPU8、自研XPU全都需要；客户可以不买某一家GPU，但绕不开HBM和封装验证。

2. PCIe 7/CXL 4.0/UCIe 3.0/VIP合规套件。  
最强原因：2026的收入不靠终端出货，而靠所有高端项目提前license、仿真、test chip和验证。

3. 224G/448G SerDes + 1.6T/3.2T Ethernet + UALink/UEC/ESUN相关IP。  
最强原因：AI集群利用率取决于数据移动，Broadcom/Marvell/Synopsys/Cadence/Alphawave/Keysight链条同步受益。

4. Agentic verification / SI/PI / physical ECO。  
最强原因：大模型写RTL不是主价值，真正刚需是缩短不可控迭代；任何能减少1-2周tapeout或board bring-up周期的工具都有定价权。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/能力 |
|---|---|---|---|
| 高端EDA软件 | 美国为核心，欧洲/以色列/印度/中国有研发 | Synopsys、Cadence、Siemens EDA、Ansys/Synopsys、Keysight EDA、Aldec、Altair、Zuken | 数字实现、验证、3DIC、多物理场、SI/PI、DFT/SLM |
| 接口IP | 美国/英国/加拿大/以色列/中国台湾/中国大陆 | Arm、Synopsys、Cadence、Rambus、Alphawave/Qualcomm、Marvell、Broadcom、Silicon Creations、Ceva、Mixel、eTopus | PCIe/CXL/Ethernet/UCIe/HBM/DDR/MIPI/USB/SerDes |
| Chiplet/NoC/DFT/SLM | 美国/欧洲/以色列/韩国/日本/中国台湾 | Arteris、Baya Systems、Blue Cheetah、Eliyan、Ayar Labs、Lightmatter、DreamBig、proteanTecs、PDF Solutions、Advantest/Teradyne | D2D PHY、NoC、光I/O、KGD、SLM、RoT |
| 先进制程/硅验证 | 台湾、韩国、美国、日本 | TSMC、Samsung Foundry、Intel Foundry、GlobalFoundries成熟节点、UMC | N2/N3/N4/N5、silicon test chip、PHY validation |
| 先进封装 | 台湾、韩国、美国、马来西亚/新加坡、中国大陆 | TSMC CoWoS/SoIC、Intel EMIB/Foveros、Samsung I-Cube/X-Cube、ASE、Amkor、JCET、SPIL | 2.5D、3D、hybrid bonding、interposer、RDL、CoPoS探索 |
| 测试与仪器 | 美国/日本/德国/中国台湾 | Keysight、Anritsu、Tektronix、Teledyne LeCroy、Rohde & Schwarz、Advantest、Teradyne | 65GHz/145GHz/250GHz、BERT、VNA、ATE、protocol analyzer |

### 4.2 至少5条关键供给瓶颈

1. 高端PHY硅验证窗口稀缺：224G/448G、PCIe7/8、HBM4、UCIe64G必须在先进节点和真实封装上验证，test chip成本高、排队长。
2. 3DIC signoff人才短缺：传统前端/后端工程师不足以覆盖热、机械、EM/IR、封装、SI/PI、液冷边界条件。
3. IP认证和合规周期长：PCI-SIG、CXL、UCIe、JEDEC、OIF、UALink、OCP相关合规会拖慢产品收入确认。
4. 先进封装产能反向约束IP放量：客户即便拿到UCIe/HBM IP，也要等CoWoS/SoIC/EMIB、ABF/玻璃基板、KGD测试产能。
5. 测试仪器和实验室瓶颈：128GT/s、256GT/s、224G/448G需要高端scope、BERT、VNA、夹具、de-embedding能力，测试排期会变成隐形瓶颈。
6. 安全和固件责任边界不清：开放chiplet需要RoT、secure boot、firmware update、attestation、供应链审计，谁为多厂商die失效负责尚未标准化。
7. 出口管制与地缘风险：EDA和高端IP对先进制程、AI芯片、特定地区客户存在许可限制，影响中国高端AI ASIC和国产EDA/IP替代节奏。

### 4.3 成本构成与毛利决定因素

| 产品 | 成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| EDA license/SaaS | R&D 35-50%，销售/FAE 15-25%，云算力/IT 5-15%，摊销/并购整合 | 工具覆盖率、签核认证、客户数据、license renewal、seat扩张 | 客户tapeout风险远大于工具费，先进节点按项目价值付费 |
| 接口PHY IP | 模拟/SerDes团队、test chip、foundry shuttle、封装/测试、应用工程 | 是否硅验证、是否多节点、多客户design win、PPA领先 | 一次授权费+NRE+royalty+VIP，早期节点可收高NRE |
| HBM/UCIe/D2D IP | PHY/controller/VIP/DFT/封装协同、HBM供应商验证 | 与HBM/封装/EDA完整flow绑定程度 | 客户抢时间上市，愿意用高NRE换低风险 |
| Chiplet/3DIC平台 | 软件研发、多物理求解器、封装PDK、代工厂认证 | 是否进入TSMC/Samsung/Intel reference flow | 代工厂认证即护城河，客户切换成本高 |
| DFT/KGD/SLM | IP、传感器、ATE程序、数据平台、现场分析 | 能否减少封装后报废、提升良率、支持RMA定位 | 以良率提升和失效率降低定价，ROI可量化 |

EDA/IP的价值捕获很强：工具/IP通常只占先进AI ASIC项目总成本的低个位数，但能决定数亿美元到数十亿美元芯片是否按期tapeout，故具备“低BOM占比、高故障成本”的定价权。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | CR3/集中度判断 | 龙头 | 竞争状态 |
|---|---|---|---|
| EDA大盘 | 极高，三巨头占绝大多数商业EDA预算 | Synopsys、Cadence、Siemens EDA | 工具链锁定强，点工具有突破但难替代全流程 |
| 半导体IP | 中高，Arm在CPU IP绝对强，Synopsys/Cadence/Rambus/Alphawave在接口分散领先 | Arm、Synopsys、Cadence、Rambus、Alphawave/Qualcomm | 高端接口IP因硅验证形成小寡头 |
| HBM controller/PHY | 高 | Rambus、Synopsys、Cadence、Samsung/TSMC生态IP | 客户极少愿意冒险用未经验证IP |
| PCIe/CXL IP/VIP | 高 | Synopsys、Cadence、Rambus、Siemens/Avery、PLDA/Rambus | 标准复杂，VIP和合规工具是粘性来源 |
| UCIe/D2D | 早期但快速集中 | Synopsys、Cadence、Alphawave、Blue Cheetah、Eliyan、Ayar Labs | 技术路线未完全统一，封装生态决定赢家 |
| 3DIC/多物理场 | 高 | Synopsys/Ansys、Cadence、Siemens、Keysight | 代工厂reference flow与客户数据是护城河 |
| NoC/片上互连 | 中高 | Arteris、Baya、Synopsys、Cadence、Siemens | 可替代性高于PHY，但SoC架构一旦采用切换成本高 |

### 5.2 可量化壁垒清单：为什么能定价

| 壁垒 | 解释 | 定价逻辑 |
|---|---|---|
| 硅验证壁垒 | 先进PHY必须在N3/N2、复杂封装和真实信道跑通 | 客户买的是“降低tapeout失败概率”，不是代码行数 |
| 标准与合规壁垒 | PCIe/CXL/UCIe/HBM/JEDEC/OIF版本快速升级 | VIP、protocol analyzer、compliance tool成为准入费 |
| 客户锁定 | 同一项目的EDA脚本、IP、约束、verification environment深度绑定 | 切换可能重跑数月验证，license续费弹性强 |
| 代工厂认证 | TSMC/Samsung/Intel reference flow和PDK协同 | 通过认证的工具/IP更容易进入客户短名单 |
| 人才壁垒 | 高速模拟、SerDes、HBM PHY、3DIC热机械复合人才稀缺 | 人力不是短期能堆出来，头部厂商议价稳 |
| 数据壁垒 | EDA AI需要历史设计、bug、timing、layout、test数据 | 私有数据让AI-native EDA更像平台，不像通用模型 |
| 责任壁垒 | Chiplet多厂商责任边界复杂 | 能提供端到端IP+VIP+DFT+SLM的供应商可收组合溢价 |

### 5.3 哪一层最可能长期高ROIC/高毛利

最高质量：EDA/IP/VIP/SLM软件。原因是资本开支轻、复用性强、客户切换成本高、低BOM占比高价值。长期高ROIC最可能出现在Synopsys、Cadence、Arm、Rambus、Arteris这类软件/IP资产。

最大弹性：高端接口PHY和D2D/UCIe/HBM IP。原因是AI ASIC项目数量增加，而每个项目都要买“已验证、可签核”的接口能力。这里的毛利接近软件，但需要test chip投入，弹性取决于设计赢单。

硬件高增长但ROIC更分化：先进封装、CPO、测试仪器、retimer/switch silicon。它们收入弹性强，但资本开支、良率、库存和价格竞争更明显。

## 6. 2026关键变化：最可能的3个拐点

1. EDA从“芯片工具”变成“硅到系统工具”。  
Synopsys+Ansys、Cadence multiphysics、Siemens 3DIC说明设计边界已扩到封装、热、液冷、电源完整性和系统可靠性。2026 AI rack功耗和封装复杂度会把多物理场工具写进采购清单。

2. UCIe/PCIe/CXL/UALink等接口标准进入AI ASIC RFP。  
UCIe 3.0、PCIe 7、CXL 4.0、UALink 2.0并行出现，客户不一定立刻买开放chiplet，但会要求供应商证明路线可扩展、可管理、可验证。

3. Custom silicon订单让接口IP进入景气上行。  
OpenAI/Broadcom 10GW、Meta/Broadcom >1GW到多GW、Google TPU、AWS Trainium、Microsoft Maia共同说明：自研ASIC不是边缘补充，而是新增主产能池。每新增一个ASIC项目，就新增一套EDA/IP/VIP/测试/封装协同预算。

## 7. 2027关键变化：最可能的3个拐点

1. HBM4/HBM4E与UCIe 3.0联动放量。  
2026是HBM4验证和早期出货，2027更可能成为HBM4E/Custom HBM base die/64G D2D设计锁定年。HBM IP、D2D、3DIC signoff和KGD测试将从项目成本项变成平台能力。

2. 非NVIDIA rack-scale开放互连开始商业化。  
AMD Helios/MI400、AWS Trainium3/4、Meta MTIA、OpenAI/Broadcom、Google TPU会推动UALink/ESUN/CXL/PCIe/以太网组合路线。2027若开放AI fabric证明够用，retimer、switch、SerDes IP和NoC会被重估。

3. 安全/固件/供应链信任成为高端客户准入门槛。  
主权AI、欧洲云和hyperscaler会把Caliptra、openSFI、SBMR、OCP S.A.F.E./S.O.L.I.D.这类要求写入RFP。硬件安全验证、RoT IP、固件生命周期工具会从“小市场”变成“准入市场”。

## 8. 头部公司与技术优势公司清单

### 8.1 EDA工具

| 公司 | 优势 |
|---|---|
| Synopsys | 数字EDA、验证、DesignWare IP、3DIC Compiler、SLM；并入Ansys后补强多物理场；与TSMC/Samsung先进节点合作深 |
| Cadence | Virtuoso、Innovus、Tempus、Voltus、Jasper、Palladium/Zebu、Celsius/Clarity、Integrity 3D-IC；AI portfolio和IP业务增长强 |
| Siemens EDA | Calibre、Aprisa、Tessent、Xpedition、Innovator3D IC；封装/PCB/DFT强 |
| Ansys/Synopsys | HFSS、RedHawk、Icepak、Mechanical等多物理场资产，AI rack/3DIC价值上升 |
| Keysight EDA | ADS、PathWave、SI/PI、高速互连测试闭环 |
| Altair | 仿真、HPC、AI工程软件，偏系统和机械/多物理 |
| Zuken/Altium/Autodesk | PCB/系统设计，中高端AI板级复杂度提升受益 |
| Empyrean/华大九天、Primarius/概伦电子、Xpeedic/芯和半导体、Agnisys、Aldec | 国产/专用EDA、验证、建模、IP-XACT和模拟/板级工具补位 |

### 8.2 接口IP

| 公司 | 优势 |
|---|---|
| Arm | CPU IP、AMBA/CHI、CSS、chiplet系统架构影响力；Cloud AI和边缘AI royalty增长 |
| Synopsys | PCIe、CXL、1.6T/800G Ethernet、HBM、DDR、UCIe、USB、MIPI全组合；3000+ PCIe design wins |
| Cadence | UCIe、PCIe/CXL、HBM/DDR、112G/224G SerDes、VIP、Verification Suite |
| Rambus | HBM4/HBM4E controller、PCIe/CXL、memory interface、安全IP；Q1 2026收入1.802亿美元，产品收入8800万美元 |
| Alphawave Semi/Qualcomm | 112G/224G SerDes、64G UCIe、AI平台连接IP；TSMC先进封装生态 |
| Marvell | 224G/PCIe 8 SerDes、custom silicon、DSP/retimer、DPU/NIC、AI网络 |
| Broadcom | XPU平台、AI networking、Tomahawk/Jericho、custom ASIC、SerDes、光互连；AI收入高速增长 |
| Credo | AEC、retimer、SerDes、Dove/HiWire生态，AI互连高弹性 |
| Astera Labs | Aries/COSMOS、Leo CXL、Scorpio P/X fabric switch；2026Q1收入同比高增长，GM约75%级 |
| Silicon Creations、Mixel、eTopus、GUC、Faraday、M31、T2M-IP | PLL/SerDes/MIPI/USB/DDR/PCIe等专用IP，适合细分设计 |

### 8.3 Chiplet、D2D、NoC、光I/O与SLM

| 公司 | 优势 |
|---|---|
| Arteris | NoC和SoC/Chiplet互连IP，汽车和AI SoC设计采用度高 |
| Baya Systems | 可组合chiplet fabric和system IP，新兴高增长 |
| Blue Cheetah | D2D/BoW/UCIe PHY方向，适合chiplet互连 |
| Eliyan | NuLink/BoW/UCIe相关D2D，主打标准封装上高带宽 |
| Ayar Labs | 光I/O chiplet，面向AI/HPC互连瓶颈 |
| Lightmatter | Passage CPO/photonic interposer，与Synopsys集成224G SerDes和UCIe IP |
| DreamBig Semiconductor | chiplet平台、AI/网络定制硅 |
| proteanTecs | SLM、芯片监测、预测性可靠性 |
| PDF Solutions | 良率、制造数据、DFT/analytics |
| QuickLogic | eFPGA chiplet，国防/工业/长生命周期场景 |
| Zero ASIC、Tenstorrent、SiFive、Esperanto、Rebellions、Furiosa、d-Matrix | RISC-V/AI加速器/chiplet化潜在采用者 |

### 8.4 代工、封装、测试和仪器

| 公司 | 优势 |
|---|---|
| TSMC | N3/N2、CoWoS、SoIC、3DFabric、OIP，AI封装事实核心 |
| Samsung Foundry | I-Cube/X-Cube、HBM与代工协同，先进封装追赶 |
| Intel Foundry | EMIB、Foveros、18A、玻璃基板/先进封装路线 |
| ASE、Amkor、JCET、SPIL、Powertech | OSAT和先进封装外包承接 |
| Ibiden、Unimicron、Nan Ya PCB、Shinko、AT&S、欣兴、深南电路 | ABF/高端PCB/载板 |
| Keysight、Anritsu、Tektronix、Teledyne LeCroy、Rohde & Schwarz | 224G/448G、PCIe7/8、1.6T测试仪器 |
| Advantest、Teradyne、FormFactor、MPI | ATE、探针卡、HBM/KGD测试 |

## 9. 情景汇总：2026-2028市场规模与利润率

| 细分 | 2026E规模 | 2027E基准 | 2027E乐观 | 2027E极度乐观 | 2028E极度乐观上沿 | 毛利/经营利润判断 |
|---|---:|---:|---:|---:|---:|---|
| EDA+SIP+设计服务总盘 | $23-25B | $26-29B | $30-33B | $34-38B | $45B+ | GM 75-90%；经营利润30-45% |
| EDA工具 | $14-16B | $16-18B | $18-21B | $21-24B | $28B+ | 头部经营利润35-45% |
| Semiconductor IP | $7-9B，SEMI SIP run-rate更高 | $8-10B | $10-13B | $13-16B | $20B+ | GM 80-95% |
| 高端接口IP子集 | $3.5-5B | $4.5-6.5B | $6.5-9B | $9-13B | $18B+ | 85-95% GM |
| Chiplet/D2D/3DIC EDA+IP | $1.5-2.5B | $2-3.5B | $3.5-5.5B | $5.5-8B | $12B+ | 70-95% GM，组合销售最优 |
| DFT/KGD/SLM/安全 | $1.5-2.5B | $2-3B | $3-4.5B | $4.5-7B | $10B+ | 45-90%，软件/IP更高 |
| 先进封装制造 | $55-60B左右 | $63B | $69B | $78B | $100B+ | 高端30-45%，传统OSAT 15-25% |

## 10. 最重要跟踪指标

1. Synopsys Q2 FY2026（预计2026-05-27）对Ansys整合、EDA/IP organic growth、FY2026 margin的表述。
2. Cadence backlog是否继续高于80亿美元，以及IP业务是否保持20%+增长。
3. Broadcom AI revenue：Q2 FY2026 AI半导体收入是否继续高增，custom XPU客户从Google/Meta/OpenAI扩到更多家。
4. Rambus/Cadence/Synopsys HBM4/HBM4E IP design wins数量和客户节点。
5. UCIe 3.0 plugfest、FCSA 1.1、OCP open chiplet economy是否进入真实RFP。
6. PCIe 7/8测试生态：Keysight/Anritsu/LeCroy、Marvell/Synopsys 256GT/s demo后是否有客户设计赢单。
7. CoWoS/SoIC/EMIB实际产能和良率：如果2026H2扩产顺利，EDA/IP收入确认会更快；若封装卡住，EDA/IP仍先收license但royalty延后。

## 11. 主要来源

- [SEMI ESD Alliance EDMD Q4 2025：ESD收入$5.466B、同比+10.3%](https://www.semi.org/en/semi-press-release/esd-alliance-reports-electronic-system-design-industry-posts-5.5-billion-dollars-in-revenue-in-q4-2025)
- [Cadence 2026Q1财报：收入$1.474B、backlog $8.0B](https://investor.cadence.com/news/news-details/2026/Cadence-Reports-First-Quarter-2026-Financial-Results/default.aspx)
- [Synopsys 2026Q1财报：收入$2.409B、FY2026中位数$9.61B](https://investor.synopsys.com/news/news-details/2026/Synopsys-Posts-Financial-Results-for-First-Quarter-Fiscal-Year-2026/default.aspx)
- [Synopsys/TSMC 2026合作：PCIe 7.0、HBM4、224G、UCIe 64G等first-silicon里程碑](https://investor.synopsys.com/news/news-details/2026/Synopsys-Partners-with-TSMC-to-Power-Next-Generation-AI-Systems-with-Silicon-Proven-IP-and-Certified-EDA-Flows/default.aspx)
- [Rambus HBM4E Controller IP，16Gbps/pin，100+ HBM design wins](https://investor.rambus.com/press-releases/press-release-details/2026/Rambus-Sets-New-Benchmark-for-AI-Memory-Performance-with-Industry-Leading-HBM4E-Controller-IP/default.aspx)
- [Rambus PCIe 7.0 Switch IP，2026-05-05](https://www.rambus.com/rambus-introduces-pcie-7-0-switch-ip-with-time-division-multiplexing-for-scalable-ai-and-data-center-infrastructure/)
- [Marvell DesignCon 2026：PCIe 8.0 SerDes 256GT/s demo](https://investor.marvell.com/news-events/press-releases/detail/1009/marvell-to-showcase-pcie-8-0-serdes-demonstration-at-designcon-2026)
- [UCIe Consortium 3.0：64GT/s与增强manageability](https://www.uciexpress.org/press-releases)
- [CXL 4.0 white paper](https://computeexpresslink.org/wp-content/uploads/2025/11/CXL_4.0-White-Paper_FINAL.pdf)
- [OpenAI/Broadcom 10GW自研AI加速器合作](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)
- [Meta/Broadcom MTIA首期>1GW、多GW路线](https://about.fb.com/news/2026/04/meta-partners-with-broadcom-to-co-develop-custom-ai-silicon/)
- [Broadcom 2026Q1财报：AI收入$8.4B、同比+106%](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm)
- [Astera Labs 2026Q1财报：AI connectivity与Scorpio X/P ramp](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results)
- [Arm FY2026结果：全年royalty $2.61B、licensing $2.31B](https://newsroom.arm.com/news/arm-q4-fye26-results)
- [Synopsys PCIe 7.0 IP：3000+ PCIe design wins](https://investor.synopsys.com/news/news-details/2024/Synopsys-Accelerates-Trillion-Parameter-HPC--AI-Supercomputing-Chip-Designs-with-Industrys-First-PCIe-7.0-IP-Solution/default.aspx)
- [Synopsys 1.6T Ethernet IP](https://investor.synopsys.com/news/news-details/2024/Synopsys-Launches-Industrys-First-Complete-1.6T-Ethernet-IP-Solution-to-Meet-High-Bandwidth-Needs-of-AI-and-Hyperscale-Data-Center-Chips/default.aspx)
- [Lightmatter/Synopsys：224G SerDes和UCIe IP集成到Passage 3D CPO](https://lightmatter.co/press-release/lightmatter-collaborates-with-synopsys-to-integrate-advanced-interface-ip-with-its-passage-co-packaged-optics-platform/)
- [OCP Open Chiplet Economy / FCSA](https://www.opencompute.org/index.php/blog/ocp-open-chiplet-economy-is-leading-the-next-wave-of-ai-inference)
- 本项目内参考：[ai_chip_research_2026_2027.md](D:/drive/Investment/调研/v5/ai_chip_research_2026_2027.md)、[chiplet_summit_2026_update.md](D:/drive/Investment/调研/v5/conference_update/chiplet_summit_2026_update.md)、[designcon_2026_conference_update.md](D:/drive/Investment/调研/v5/conference_update/designcon_2026_conference_update.md)、[pci_sig_devcon_2026_update.md](D:/drive/Investment/调研/v5/conference_update/pci_sig_devcon_2026_update.md)、[OCP_EMEA_Summit_2026_高密度调研报告.md](D:/drive/Investment/调研/v5/conference_update/OCP_EMEA_Summit_2026_高密度调研报告.md)
# 行业调研：【HBM与高带宽内存】

> 写作截点：2026-05-08  
> 研究口径：以 AI 数据中心加速器使用的 HBM、高带宽 DRAM/LPDDR/SOCAMM、HBM PHY/Controller、HBM 封装测试设备、先进封装/基板等直接受益环节为核心。  
> 情景口径：本报告按“基准 / 乐观 / 极度超预期乐观”三档建模。缺少直接披露的产品级市场规模时，使用 AI 芯片出货底稿、HBM stack 数量、ASP、HBM bit growth、客户 CapEx、供应瓶颈和行业报告互相校验。  
> 非投资建议。所有市场规模为研究估算，美元口径；公司财务数字以原披露币种或美元折算近似。

## 0. 一页结论：2026 年 HBM 是 AI 算力建设里最稀缺、最能涨价的“算力阀门”

**核心判断：**

1. **2026 年主线不是 HBM4 全面替代，而是 HBM3E 12Hi 继续统治 + HBM4 在 Rubin/MI400/下一代 ASIC 上抢先导入。** TrendForce 指出 NVIDIA 在 2025Q3 上调 Rubin HBM4 speed-per-pin 至 11Gbps 以上，导致三大供应商需重送样并把 HBM4 放量节奏推向 2026Q1 末至 Q2；同时 Blackwell Ultra B300/GB300 需求被上修，HBM3E 订单继续增加。
2. **HBM 市场 2026 年进入 500 亿美元以上收入池。** SK hynix 新闻室引用 BofA 估算，2026 年 HBM 市场约 **546 亿美元、同比 +58%**；TrendForce 估算 2026 年 HBM consumption 仍将 **同比 +70% 以上**；Gartner 则把 2026 年全球 memory revenue 上修至 **6333 亿美元**，DRAM 年均价格预计 +125%，证明“内存通胀”已从 HBM 外溢到 DDR5/NAND。
3. **供给不是单一 wafer 瓶颈，而是 DRAM wafer + TSV + stack bonding + KGD 测试 + CoWoS/interposer + GPU 认证的复合瓶颈。** HBM4 还新增 logic base die / foundry 协同变量。短期最稀缺的是“已被 NVIDIA/AMD/Google/AWS/Microsoft/Broadcom 认证、能按期交付的 HBM3E/HBM4 bit allocation”。
4. **利润率弹性极强。** Micron FY2026 Q2 公司层面 GAAP gross margin 已到 **74.4%**，FY2026 Q3 指引约 **81%**；虽然这不是纯 HBM 毛利，但说明 AI 内存供不应求已把传统周期品推到平台型硬件利润率区间。HBM3E/HBM4 在 2026 年的供应商毛利率合理估计为 **60-80%**，极度超预期情景可短期触及 **80%+**。
5. **长期价值捕获顺序：** 2026 年最强为 SK hynix / Samsung / Micron；2027 年开始转向 HBM4E、custom HBM、base die foundry、hybrid copper bonding、HBM tester/probe/TC bonder、CoWoS/基板；长期高 ROIC 最可能在 **HBM IP/EDA、测试探针/关键设备、客户认证后的高端 HBM 供应份额**。

### 0.1 全球 HBM 与高带宽内存收入池三情景

| 口径 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 基准 | 2027 乐观 | 2027 极度超预期乐观 | 2028 基准 | 2028 乐观 | 2028 极度超预期乐观 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HBM 单品收入 | $52-65B | $65-85B | $85-110B | $80-115B | $115-170B | $170-240B | $115-165B | $170-260B | $260-380B |
| HBM + SOCAMM/LPDDR + AI DDR5/MRDIMM + HBM IP | $95-140B | $140-210B | $210-300B | $155-240B | $240-380B | $380-560B | $230-360B | $380-620B | $620-900B |
| HBM 相关设备/封装/基板/IP 收入池 | $20-38B | $35-60B | $60-95B | $38-75B | $70-125B | $125-210B | $60-110B | $120-210B | $220-360B |
| HBM 在高端 AI 加速器内存价值占比 | 70-78% | 75-83% | 80-88% | 72-82% | 78-88% | 85-92% | 68-80% | 75-88% | 82-93% |
| 高端 AI 加速器受 HBM 约束程度 | 高 | 很高 | 极高但客户预付款保障 | 高 | 很高 | 极高 | 中高 | 高 | 高 |

**解释：** 2026 HBM 单品基准锚定 BofA/SK hynix 的 546 亿美元估计；2027-2028 上沿来自本地 AI 芯片底稿中 Rubin、MI400、TPU8、Trainium3/4、Meta/OpenAI/Broadcom ASIC 同时放量的极乐观假设。极度超预期情景本质是假设“AI inference token 增长吞掉所有新增 HBM、DDR5、SOCAMM 和 SSD 供应”，且客户愿意用高价锁交期。

## 1. 2026 AI 计算中心建设下的机遇、挑战与技术路径

### 1.1 当前正在使用的关键技术

| 技术 | 2026 状态 | 典型用途 | 关键事实 | 投资含义 |
|---|---|---|---|---|
| HBM3 / HBM3E 8Hi | 成熟在产 | H100/H200、MI300/MI325、部分 ASIC | HBM3E 单 stack 可达 TB/s 级带宽，H200 用 HBM3E 解决 H100 容量瓶颈 | 仍有存量需求，但新增价值被 HBM3E 12Hi 和 HBM4 挤压 |
| HBM3E 12Hi | 2026 主力放量 | B200/GB200、B300/GB300、MI350、TPU/Trainium/ASIC | SK hynix 新闻室引用多家机构判断：HBM3E 约占 2026 HBM 出货三分之二 | 2026 收入确定性最高，供不应求和价格传导最强 |
| HBM4 12Hi | 2026 Q1/Q2 进入量产/验证，H2 放量 | Vera Rubin、MI400/MI455X、TPU8、OpenAI/Meta/Broadcom ASIC | Samsung 宣布 HBM4 量产并商用出货；Micron 宣布 36GB 12H HBM4 已于 2026Q1 volume shipment；SK hynix 已完成 HBM4 开发和量产体系 | 2026 是份额争夺期，2027 是收入斜率最大环节 |
| HBM4 16Hi | 2026 样品，2027 主力化 | 高容量训练、长上下文推理 | Micron 已向客户送样 48GB 16H；Samsung 规划 16-layer 最高 48GB | 2027 高端 xPU 单卡容量上移的关键 |
| HBM4E | 2026 H2 样品，2027 放量 | Rubin Ultra、MI500、下一代 TPU/ASIC | Samsung GTC 2026 展示 HBM4E，16Gbps/pin、4TB/s 级；Micron 预计 2027 ramp HBM4E | 2027-2028 弹性最大，客户定制化提高溢价 |
| SOCAMM2 / LPDDR server memory | 2026 量产 | Vera CPU、Grace/Vera CPU、CPU memory pool、推理系统 | Micron 与 Samsung 均在 GTC 2026 强调 SOCAMM2；Micron 192GB SOCAMM2 量产，最高 2TB/CPU、1.2TB/s/CPU | 从 GPU HBM 扩散到 AI CPU 和 rack memory hierarchy |
| DDR5 / MRDIMM | 2026 供给紧张 | 推理 prefill、CPU 内存池、通用服务器 | TrendForce 指出 DDR5 与 HBM3E 价差从 4-5 倍收敛，2026 年底可能到 1-2 倍 | DDR5 也从周期品转为 AI 资源品 |
| GDDR7 / 专用高带宽显存 | 2026 局部使用 | Rubin CPX、低成本/低延迟推理、边缘 AI | 高带宽、低成本，但功耗/容量/封装密度不如 HBM | 可成为 HBM 不足时的推理分层替代 |
| CXL memory / pooled memory | 2026 pilot，2027 扩张 | CPU 侧内存池、推理缓存、内存扩展 | 与 HBM 互补，不替代 GPU 近端内存 | 2027 后形成 AI memory fabric 机会 |
| HBF / High Bandwidth Flash | 标准化早期 | KV cache、向量检索、容量型高速存储 | SanDisk/SK hynix 推进方向，主流量产更可能在 2030 前后 | 2026-2028 不是主收入，但可改变长期内存层级 |

### 1.2 项目底稿中的 2026-2027 出货量最大 AI 芯片与 HBM 技术路径

以下来自项目已有 `ai_chip_research_2026_2027.md`，不再重复外部搜索。排序按“2026-2027 年初可见等效芯片出货数量 + 价值权重”。

| 排名 | 芯片/平台 | 2026-2027 出货逻辑 | 对 HBM / 高带宽内存的拉动 | 对行业判断 |
|---:|---|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | 2026 Blackwell 主力，GB300/B300 领先出货结构 | 每 GPU 最高 288GB HBM3E，NVL72 rack 内统一内存/互连 | 2026 HBM3E 12Hi 最大需求源 |
| 2 | AWS Trainium2 | Project Rainier 近 50 万颗，Anthropic 目标百万级 | HBM + NeuronLink，ASIC 需求使 HBM 不再只是 NVIDIA 驱动 | HBM3E 向云厂商 ASIC 扩散 |
| 3 | Google TPU v7 Ironwood | Google Cloud + Anthropic 扩容 | 192GB HBM、7.37TB/s，推理优先 | TPU 证明推理也需要高带宽内存 |
| 4 | NVIDIA B200/GB200 Blackwell | 既有订单延续，部分客户继续采购 | HBM3E，NVLink 5，GB200 NVL72 | HBM3E 存量收入延续 |
| 5 | Huawei Ascend 910C/950PR/950DT | 中国国产替代第一梯队 | 910C/950 受国产 HBM、先进封装与供应链约束 | 中国 HBM 国产化期权很大但不确定性高 |
| 6 | Cambricon MLU 590/690 | 2026 目标约 50 万颗级别 | HBM + MLU-Link，SMIC/封装/国产 HBM 约束 | 本土 AI 芯片放量会创造非美 HBM 需求 |
| 7 | AMD MI350X/MI355X/MI350P | 2026 AMD 最确定放量产品 | HBM3E，8-GPU UBB/PCIe 形态 | 2026 AMD 对 HBM3E 是边际增量 |
| 8 | AWS Trainium3 | 3nm Trainium3 UltraServer，144 芯片 scale-up | HBM3E 级别，2027 主力 | 私有 ASIC 会拉长 HBM 紧张周期 |
| 9 | Meta MTIA 300/400/450/500 | Meta 已部署数十万 MTIA，2026-2027 四代迭代 | GenAI inference 需要更高内存带宽和效率，Broadcom XPU 牵引 | 定制 ASIC 份额上升利好 HBM IP/base die |
| 10 | Microsoft Maia 200 | Azure/Copilot/OpenAI 推理导入 | 216GB HBM3E、7TB/s、272MB SRAM | 云厂商自研芯片正在把 HBM 变成平台标配 |
| 11 | NVIDIA Vera Rubin NVL72 | 2026 H2 出货，2027 主力 | Rubin GPU 配 HBM4；NVIDIA GTC 2026 称七类芯片 full production | HBM4 2027 最大需求源 |
| 12 | AMD MI400/MI455X Helios | 2026 H2 首批，2027 放量 | MI455X 目标 432GB HBM4、约 19.6TB/s | HBM4 供给决定 AMD 高端平台斜率 |

### 1.3 新技术成熟与放量时间：三情景

| 技术 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观成熟/放量 | 2026 最可能路径 |
|---|---|---|---|---|
| HBM3E 12Hi | 已成熟，2026 全年主力；2027 逐步让位 | 2026 供给继续紧张且 ASP 维持高位 | 2026 B300/GB300、ASIC 订单上修，全年缺货 | **最确定主线** |
| HBM4 12Hi | 2026Q2 完成多家验证，2026H2 进入 Rubin 小批量；2027 放量 | 2026Q2/Q3 三家均形成量产供货，Rubin/MI400/ASIC 同步导入 | 2026Q2 即出现多供应商可交付，2026Q4 已成高端新增默认 | **第二主线，2027 主力** |
| HBM4 16Hi | 2026 样品，2027H2 放量 | 2027H1 进入高端训练平台 | 2026Q4 小批量进最高端客户 | 2026 关注 design-win，不押大收入 |
| HBM4E | 2026H2 样品，2027H2 放量 | 2027H1 随 Rubin Ultra/下一代 ASIC 放量 | 2027Q1 即进入部分平台量产 | 2026 是期权，2027 是弹性 |
| custom HBM / cHBM | 2027 样品，2028 放量 | 2027H2 OpenAI/Meta/Google/Broadcom 开始放量 | 2027Q2 被大客户作为标准化采购 | 2026 先看 base die 与客户联合设计 |
| hybrid copper bonding | 2026 展示/验证，2027-2028 用于 16Hi+ | 2027 高端 HBM4E 采用率快速上升 | 2027 直接成为 16Hi 高端主流 | 2026 是设备和良率导入期 |
| SPHBM4 / 低成本窄接口 HBM | 2026 标准化，2028 放量 | 2027 样品，2028 大量用于中端推理 | 2027 下半年已有云厂商试点 | 2026 不是收入主线 |
| CXL pooled memory | 2026 pilot，2027 扩大 | 2027 成为 CPU 推理内存池常规配置 | 2027 与 SOCAMM2/MRDIMM 共同进入 AI rack 标配 | 辅助 HBM，不替代 HBM |
| HBF / high bandwidth flash | 2026-2028 标准与研发 | 2028-2029 样品 | 2028 小批量用于 KV cache | 更偏 2030 以后长期机会 |

**2026 最可能的技术路径：**  
**B300/GB300/ASIC 继续吃 HBM3E 12Hi，Rubin/MI400/下一代 ASIC 抢 HBM4 12Hi 早期份额；AI CPU 与 DPU/SSD 侧用 SOCAMM2、DDR5/MRDIMM、PCIe Gen6 SSD 搭出第二层高带宽内存/存储体系。**

## 2. 已经开始放量的关键产品：市场规模、渗透率、利润率

本节“未来 3 个月 / 未来 1 年 / 未来 2 年”为自 2026-05-08 起的滚动累计收入或订单窗口；相邻环节如 HBM 成品、CoWoS、设备、基板之间存在价值链传导关系，不能简单加总为终端市场规模。

### 2.1 已放量产品总表

| 已放量产品 | 主要供应商 | 证据与状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 毛利率三情景 |
|---|---|---|---:|---:|---:|---|---|
| HBM3E 12Hi / 8Hi | SK hynix、Samsung、Micron | 2026 主力；SK hynix 新闻室引用机构判断 HBM3E 约占 2026 HBM 出货三分之二 | 基准 $12-18B；乐观 $18-24B；极度 $25-32B | 基准 $42-55B；乐观 $55-70B；极度 $70-90B | 基准 $55-80B；乐观 $80-120B；极度 $110-160B | 2026 AI HBM bit 60-70%；2027 35-50%；2028 20-35% | 基准 58-70%；乐观 68-78%；极度 75-85% |
| HBM4 12Hi | Samsung、Micron、SK hynix | Samsung 宣布 HBM4 量产并商用出货；Micron 宣布 2026Q1 volume shipment；SK hynix 量产体系已就绪 | 基准 $2-6B；乐观 $6-10B；极度 $10-16B | 基准 $18-32B；乐观 $35-55B；极度 $60-85B | 基准 $65-105B；乐观 $100-160B；极度 $150-230B | 2026 8-18%；2027 35-55%；2028 45-65% | 基准 62-75%；乐观 72-82%；极度 80-88% |
| SOCAMM2 / LPDDR server modules | Micron、Samsung、SK hynix | Micron 192GB SOCAMM2 已量产；Samsung 称 SOCAMM2 mass production | 基准 $0.8-2B；乐观 $2-4B；极度 $4-7B | 基准 $5-12B；乐观 $12-22B；极度 $22-35B | 基准 $15-35B；乐观 $35-65B；极度 $65-110B | AI CPU/Vera/Grace 类节点 2026 5-15%，2027 20-45%，2028 35-60% | 基准 45-58%；乐观 55-68%；极度 65-75% |
| AI DDR5 / RDIMM / MRDIMM | Samsung、SK hynix、Micron、Montage 等 | DDR5 受 AI 推理和通用服务器升级拉动；TrendForce/Gartner 均提示价格上行 | 基准 $6-12B；乐观 $12-20B；极度 $20-30B | 基准 $35-65B；乐观 $65-100B；极度 $100-150B | 基准 $70-130B；乐观 $130-220B；极度 $220-350B | AI CPU/推理 prefill 2026 25-40%，2027 40-60%，2028 55-75% | 基准 42-58%；乐观 55-70%；极度 65-78% |
| HBM PHY/Controller IP | Rambus、Synopsys、Cadence、Siemens EDA | Rambus HBM4E controller 支持至 16Gbps/pin、4TB/s 级；ASIC 客户增加 | 基准 $0.1-0.3B；乐观 $0.3-0.6B；极度 $0.6-1B | 基准 $0.5-1.5B；乐观 $1.5-3B；极度 $3-5B | 基准 $1.5-4B；乐观 $4-8B；极度 $8-15B | 高端 ASIC 2026 50%+ 需要成熟 IP，2027 70%+ | 基准 70-82%；乐观 78-88%；极度 85-92% |
| TC bonder / HBM stacking equipment | Hanmi、Hanwha Semitech、ASMPT、BESI、Applied Materials、TEL | SK hynix 2026 初继续下单 TC bonder；16Hi/HBM4E 推动设备升级 | 基准 $0.5-1.3B；乐观 $1.3-2.5B；极度 $2.5-4B | 基准 $3-8B；乐观 $8-14B；极度 $14-22B | 基准 $8-20B；乐观 $20-38B；极度 $38-65B | HBM 新增产线绑定率接近 100% | 基准 42-55%；乐观 52-65%；极度 60-72% |
| HBM probe/test/KGD equipment | Advantest、Teradyne、FormFactor、Technoprobe、KLA、Onto、Camtek | HBM KGD 与 stack 后测试时间增加，HBM4 pin 数翻倍 | 基准 $0.6-1.5B；乐观 $1.5-3B；极度 $3-5B | 基准 $4-9B；乐观 $9-16B；极度 $16-28B | 基准 $10-24B；乐观 $24-45B；极度 $45-75B | HBM4 100% 需要更复杂 KGD/probe/burn-in | 基准 45-60%；乐观 58-70%；极度 65-78% |
| CoWoS/interposer/ABF 高端基板 | TSMC、ASE、Amkor、Samsung、Intel、Ibiden、Shinko、Unimicron、Nan Ya、AT&S | HBM 与 xPU 共同依赖 2.5D/CoWoS/载板 | 基准 $5-10B；乐观 $10-18B；极度 $18-28B | 基准 $25-50B；乐观 $50-85B；极度 $85-130B | 基准 $60-120B；乐观 $120-220B；极度 $220-360B | 高端 AI 加速器 2026 80%+ 依赖先进封装 | 基准 30-48%；乐观 42-58%；极度 55-68% |

### 2.2 已放量产品的增长预测区间

| 产品 | 基准增长 | 乐观增长 | 极度超预期乐观增长 | 主要驱动 |
|---|---:|---:|---:|---|
| HBM3E 12Hi | 2026 +45-65%，2027 -10% 至 +20% | 2026 +60-85%，2027 +10-35% | 2026 +90-120%，2027 +25-50% | B300/GB300、MI350、TPU/Trainium/ASIC 继续消化 |
| HBM4 12Hi | 2026 从低基数到 $20B+，2027 +150-250% | 2027 +180-300% | 2027 +220-350% | Rubin/MI400/TPU8/ASIC 新平台同步 |
| SOCAMM2 / LPDDR server | 2026 从零到 $5B+，2027 +80-150% | 2027 +120-220% | 2027 +200-320% | Vera CPU、AI CPU、推理内存池 |
| AI DDR5/MRDIMM | 2026 +70-120% 收入口径 | 2026 +120-180% | 2026 +180-250% | 价格上涨 + server content 增加 |
| HBM IP | 2026 +40-80% | 2026 +80-140% | 2026 +140-220% | ASIC 客户增加、HBM4/4E 控制器升级 |
| HBM 设备/测试 | 2026 +60-110% | 2026 +100-180% | 2026 +180-300% | 产线扩建、16Hi、hybrid bonding |

## 3. 在研关键产品与细分技术：2027-2028 的弹性来源

本节同样采用自 2026-05-08 起的滚动窗口。早期产品的 3 个月规模多为样品、工程验证、预付款、设备订单和 NRE，不等同于最终量产收入。

### 3.1 在研产品市场规模、渗透率、利润率

| 在研/早期产品 | 2026 状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 利润率三情景 |
|---|---|---:|---:|---:|---|---|
| HBM4 16Hi / 48GB | Micron 已送样；Samsung/SK hynix 路线图推进 | 基准 $0.1-0.5B；乐观 $0.5-1.2B；极度 $1.2-2.5B | 基准 $3-8B；乐观 $8-18B；极度 $18-35B | 基准 $35-70B；乐观 $70-130B；极度 $130-210B | 2026 <5%，2027 15-35%，2028 35-55% 高端 HBM4 | 基准 60-72%；乐观 70-82%；极度 80-88% |
| HBM4E | Samsung GTC 2026 展示；Micron 预计 2027 ramp；SK hynix 2027 量产目标 | 基准 $0-0.3B；乐观 $0.3-1B；极度 $1-2B | 基准 $2-10B；乐观 $10-25B；极度 $25-50B | 基准 $45-90B；乐观 $90-180B；极度 $180-300B | 2026 样品，2027 10-30%，2028 35-60% 高端新增 | 基准 65-78%；乐观 75-85%；极度 82-90% |
| custom HBM / cHBM | 2026 设计协同，2027 样品 | 基准 $0-0.2B；乐观 $0.2-0.8B；极度 $0.8-1.5B | 基准 $1-5B；乐观 $5-15B；极度 $15-35B | 基准 $15-45B；乐观 $45-100B；极度 $100-180B | 2027 ASIC 高端 5-15%，2028 20-45% | 基准 68-80%；乐观 78-88%；极度 85-92% |
| hybrid copper bonding / bumpless HBM | Samsung 展示 HCB；设备链导入 | 基准 $0.1-0.4B；乐观 $0.4-1B；极度 $1-2B | 基准 $2-6B；乐观 $6-14B；极度 $14-25B | 基准 $10-28B；乐观 $28-60B；极度 $60-100B | 16Hi/HBM4E 2027 10-25%，2028 35-60% | 设备/材料毛利基准 45-60%；乐观 55-70%；极度 65-78% |
| HBM5 / HBM5E | 架构预研，2028 以后 | 0 | 基准 $0-0.5B；乐观 $0.5-2B；极度 $2-5B | 基准 $5-20B；乐观 $20-60B；极度 $60-120B | 2028 仅高端试点 | 基准 65-80%；乐观 75-88%；极度 85-92% |
| SPHBM4 / low-cost HBM | JEDEC 方向，标准化早期 | 0 | 基准 $0-0.5B；乐观 $0.5-2B；极度 $2-5B | 基准 $2-12B；乐观 $12-35B；极度 $35-70B | 2028 中端推理 5-15%，极度 25% | 基准 45-60%；乐观 55-68%；极度 65-75% |
| HBF / High Bandwidth Flash | SanDisk/SK hynix 标准化方向，主流量产更靠后 | 0 | 基准 $0-0.2B；乐观 $0.2-0.8B；极度 $0.8-2B | 基准 $0.5-3B；乐观 $3-10B；极度 $10-25B | 2028 仍 <5%，2030 后更重要 | 基准 35-55%；乐观 50-65%；极度 60-75% |
| CXL memory / pooled memory | 2026 pilot | 基准 $0.2-0.8B；乐观 $0.8-2B；极度 $2-4B | 基准 $2-7B；乐观 $7-18B；极度 $18-35B | 基准 $12-35B；乐观 $35-80B；极度 $80-150B | 2026 试点，2027 CPU 推理内存池 10-25%，2028 25-45% | 基准 40-55%；乐观 52-68%；极度 62-75% |
| HBM-PIM / near-memory compute | 研发/小规模应用 | 基准 $0-0.1B；乐观 $0.1-0.5B；极度 $0.5-1B | 基准 $0.5-2B；乐观 $2-8B；极度 $8-18B | 基准 $5-20B；乐观 $20-55B；极度 $55-100B | 2028 前偏定制/科研/搜索推荐 | 基准 50-65%；乐观 65-78%；极度 75-85% |
| GDDR7/GDDR8 inference memory | 2026 用于部分专用推理/CPX/边缘 AI | 基准 $0.5-1.5B；乐观 $1.5-3B；极度 $3-6B | 基准 $4-10B；乐观 $10-22B；极度 $22-40B | 基准 $15-40B；乐观 $40-85B；极度 $85-150B | 中低端推理 2026 5-10%，2028 15-30% | 基准 35-50%；乐观 45-60%；极度 55-70% |

### 3.2 最值得跟踪的在研方向

1. **HBM4E：** 2027 最强弹性。Samsung 展示 16Gbps/pin、4TB/s 级 HBM4E；Rambus HBM4E controller 支持 16Gbps/pin。若 Rubin Ultra、MI500、TPU8/TPU9、OpenAI/Meta ASIC 同步上修规格，HBM4E 会成为 2027 年的新缺口。
2. **custom HBM / cHBM：** 逻辑 base die 从“标准接口”转为“客户差异化接口”，把 HBM 从内存标准品变成接近 ASIC 协同设计的半定制品。Samsung 的 memory + foundry + packaging 一体化优势会被放大；SK hynix 需要 TSMC/外部 foundry 协同；Micron 需要用能效和客户工程速度抢份额。
3. **hybrid copper bonding：** 16Hi 以后热阻、翘曲、pitch、良率压力上升，传统 TC bonding/NCF/MUF 路线会面临极限。Samsung 在 GTC 2026 展示 HCB，称相对 TCB 可降低热阻；设备商和材料商会出现提前订单。
4. **SOCAMM2 + CXL + SSD memory tier：** AI Agent 与长上下文推理的瓶颈不只在 GPU HBM，还在 KV cache、CPU memory、SSD random read。Micron/Samsung 在 GTC 2026 同时推 HBM4、SOCAMM2、PCIe Gen6 SSD，本质是“AI memory hierarchy 打包销售”。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构：地区、公司、工艺

| 环节 | 主要地区 | 主要公司 | 工艺/资产 | 供给判断 |
|---|---|---|---|---|
| DRAM wafer / HBM core die | 韩国、美国、日本、台湾、新加坡 | SK hynix、Samsung、Micron | 1b/1c/1γ nm DRAM，EUV 比例提高 | 韩国仍是 HBM 核心；Micron 用日本/台湾/美国/新加坡布局分散风险 |
| HBM logic base die | 韩国、台湾、美国/日本供应链 | Samsung Foundry、TSMC、可能的 Intel Foundry/客户自研 | HBM4 起 base die 逻辑化，4nm/5nm/7nm 级别参与 | Samsung 一体化优势上升；SK hynix 需外部 foundry 协同 |
| TSV / RDL / stacking | 韩国、台湾、日本、东南亚 | 三大 DRAM 厂、Hanmi、Hanwha、ASMPT、BESI、Applied Materials、TEL | TC bonding、MR-MUF、TC-NCF、hybrid copper bonding | 设备 throughput 与 stack 良率是隐性瓶颈 |
| Advanced packaging / CoWoS | 台湾、韩国、美国、日本 | TSMC、Samsung、Intel、ASE、Amkor、JCET、Powertech | CoWoS-S/L/R、SoIC、EMIB/Foveros、2.5D interposer | HBM 出来后仍需和 xPU 封装，CoWoS 决定有效交付 |
| ABF/BT substrate | 日本、台湾、韩国、奥地利 | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、Samsung Electro-Mechanics、AT&S | 高层数 ABF、大面积低翘曲基板 | 2026-2027 高端载板再次紧张 |
| Probe/test/KGD | 日本、美国、台湾、韩国、欧洲 | Advantest、Teradyne、FormFactor、Technoprobe、KLA、Onto、Camtek | wafer probe、known-good-die、burn-in、interposer test | HBM4 I/O 翻倍后测试时间和 probe card 复杂度上升 |
| Materials | 日本、美国、欧洲、台湾 | Ajinomoto、Resonac、Namics、Henkel、Dow、Shin-Etsu、SUMCO、GlobalWafers、JSR、TOK、Entegris | ABF film、underfill、photoresist、CMP slurry、silicon wafer | 小材料在高良率产品中有超额定价权 |

### 4.2 至少 10 条供给瓶颈

1. **先进 DRAM wafer 产能：** HBM 占用高端 DRAM 产线，且 HBM die 面积、KGD 要求和 stack 数导致等效 bit 供给效率低于普通 DDR5。
2. **EUV 与 1b/1c/1γ 节点迁移：** SK hynix 订购 EUV、Samsung 用 1c DRAM、Micron 推 1γ，节点升级带来早期良率波动。
3. **TSV 与 wafer thinning：** HBM 需要 TSV、超薄 die、背面处理，良率损失以 stack 形式复合放大。
4. **stack bonding throughput：** TC bonder/混合键合设备节拍限制产能；16Hi 堆叠更慢、更难。
5. **underfill / MR-MUF / NCF / HCB 材料：** 热阻、翘曲、应力控制决定 12Hi/16Hi 可靠性。
6. **known-good-die 测试：** HBM stack 中任一 die 失效都会拖累良率，wafer-level high-speed probe 和 burn-in 时间上升。
7. **logic base die foundry：** HBM4 base die 开始使用先进逻辑工艺，Samsung 可内部协调，SK hynix/Micron 需锁 foundry 资源。
8. **CoWoS / interposer：** HBM stack 生产出来不等于 GPU 可交付；xPU + HBM 仍要进入先进封装队列。
9. **ABF 高端基板：** 大尺寸 GPU/ASIC 与多 HBM stack 需要低翘曲、高层数、大面积基板。
10. **客户认证与 long-term agreement：** NVIDIA/AMD/Google/AWS/Microsoft/Broadcom 认证后才能大量供货，未认证产能无法等价替代。
11. **人才与工程组织：** HBM 是 memory、logic、thermal、package、SI/PI、test 的跨学科工程，韩国工程师被硅谷/大厂争抢。
12. **交付优先级：** 大客户预付款、LTA、绑定设计使新客户拿不到货，即使报价更高也可能没有 allocation。

### 4.3 成本构成与单位经济模型

| 成本项 | HBM stack 成本占比估算 | 2026 变化 | 毛利影响 |
|---|---:|---|---|
| DRAM die wafer | 35-45% | 1b/1c/1γ 切换、die 面积和层数提高 | 最大成本项，但 ASP 上涨可覆盖 |
| logic base die | 8-15% | HBM4 开始逻辑化，先进 foundry 成本上升 | Samsung 一体化或 TSMC 协同能力决定成本 |
| TSV/RDL/microbump | 10-15% | I/O 从 1024 到 2048，RDL 与 bump 密度上升 | 工艺稳定后可降本，初期良率拖累 |
| stacking/bonding/underfill | 12-18% | 12Hi 到 16Hi，TC/HCB 设备和材料单耗上升 | 高端设备和材料商议价增强 |
| probe/KGD/final test | 8-15% | 高速 I/O、可靠性、burn-in 时间上升 | 测试设备与 probe card 获高毛利 |
| interposer/substrate allocation | 5-10% | 大尺寸封装、CoWoS 和 ABF 紧张 | 成本可向 GPU/云客户转嫁 |
| 良率损失 | 隐含 10-25% | 初期 HBM4/16Hi 复合良率波动 | 决定供应商份额和定价能力 |

**ASP 粗略假设：**

| 产品 | 2026 基准 ASP/stack | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| HBM3E 12Hi 36GB | $450-650 | $600-800 | $750-1,000 |
| HBM4 12Hi 36GB | $650-950 | $900-1,250 | $1,200-1,600 |
| HBM4 16Hi 48GB | $900-1,300 | $1,250-1,800 | $1,700-2,400 |
| HBM4E / cHBM | $1,200-1,800 | $1,800-2,800 | $2,800-4,000 |

**价格传导机制：** HBM 是 GPU/ASIC 可交付的前置条件。若单 GPU 使用 8-12 个 HBM stack，即使 HBM 单 stack 涨价数百美元，相对一颗高端 GPU/整柜售价仍是客户愿意支付的“交期保险”。云厂商通过长期供应协议、预付款和整柜采购把成本传到 AI 服务价格、租赁合同和内部 token economics；因此 2026-2027 HBM 供应商具备强价格传导能力。

## 5. 竞争格局与壁垒：为什么能定价

### 5.1 市场结构

| 环节 | 市场结构 | 2026 份额判断 | 变化方向 |
|---|---|---|---|
| HBM 成品 | 三寡头：SK hynix、Samsung、Micron | SK hynix 仍大概率 45-60%；Samsung 25-35%；Micron 12-25% | HBM4 使 Samsung/Micron 获得追赶窗口，但 SK hynix 长协和良率优势仍强 |
| HBM4 for Rubin | 三家均争取认证 | TrendForce 预计三家 2026Q2 完成或接近完成验证；Samsung 进度快，SK 位元分配优势强，Micron 相对慢但已宣布 volume shipment | 多供应商是 NVIDIA 降低风险的必然策略 |
| HBM PHY/Controller IP | Rambus、Synopsys、Cadence 为主 | ASIC/SoC 客户依赖成熟 IP | 毛利高、资本开支低、客户粘性强 |
| Stack bonding equipment | Hanmi、Hanwha、ASMPT、BESI、AMAT/TEL 等 | TC bonder 紧张，hybrid bonding 导入 | 设备认证后切换成本高 |
| Probe/test | Advantest、Teradyne、FormFactor、Technoprobe 等 | HBM4 pin 数翻倍，测试复杂度提升 | 高端 probe card 与 ATE 获益 |
| Advanced packaging | TSMC 最强，Samsung/Intel/ASE/Amkor 补位 | CoWoS 是 GPU/HBM 有效出货瓶颈 | 封装产能扩张仍慢于 AI 需求 |
| Substrate | Ibiden、Shinko、Unimicron、Nan Ya、Kinsus、Semco、AT&S | 大尺寸 ABF 再紧张 | 产能和良率决定订单 |

### 5.2 壁垒清单：逐条解释“为什么能定价”

| 壁垒 | 具体内容 | 为什么能定价 |
|---|---|---|
| 技术壁垒 | 12Hi/16Hi stack、TSV、warpage、thermal、PDN、低电压高速 I/O | 良率差 5-10pct 就会导致可交付 bit 大幅差异，客户为稳定供应付溢价 |
| 认证壁垒 | NVIDIA/AMD/Google/AWS/Microsoft/Broadcom 平台认证周期长 | GPU/ASIC 设计一旦绑定 HBM 供应商，切换需要重新验证 SI/PI/thermal/test |
| 规模壁垒 | HBM 需前道 DRAM、后道封装、测试和客户工程同步扩产 | 只有三大 DRAM 厂能承担数十亿美元 capex 和长期产能承诺 |
| 交付壁垒 | 大客户 LTA、预付款、优先 allocation | 新客户即使出高价也未必拿到货，已认证份额具备稀缺权 |
| 供应链壁垒 | EUV、TC bonder、probe、CoWoS、ABF、underfill 材料协同 | 任何一环短缺都会影响有效出货，拥有完整链条的厂商可收费更高 |
| 工艺路线壁垒 | SK 的 MR-MUF、Samsung 的 1c DRAM + 4nm base die、Micron 的能效/1γ 路线 | 不同路线决定热/功耗/良率/客户定制能力，非单纯价格竞争 |
| 客户锁定 | GPU/ASIC 公司与 HBM 供应商联合定义规格 | HBM4/cHBM 以后更像共同研发，供应商可收取技术溢价 |
| 资金壁垒 | P&T7、M15X、Yongin、Micron Taiwan/Japan/US、Samsung Pyeongtaek 均为百亿美元级 | 高 capex 排除小厂，周期下行时也只有头部能继续投入 |

### 5.3 价值链哪一层最可能长期高 ROIC / 高毛利

| 层级 | 2026 毛利/ROIC 判断 | 长期质量 | 原因 |
|---|---|---|---|
| HBM 成品供应商 | 2026-2027 最高利润池 | 高但周期性强 | 供不应求时毛利可 60-80%，但 capex 重、价格周期会回落 |
| HBM PHY/Controller IP / EDA | 毛利最高 | 极高 | 轻资产、客户锁定、每代标准升级都需要重新授权 |
| Probe/test/TC bonder/hybrid bonding 设备 | 高 ROIC | 高 | 认证设备切换难，技术迭代带来替换周期 |
| CoWoS/advanced packaging | 毛利中高 | 中高 | 需求强，但 capex 重、客户议价强 |
| ABF/基板 | 毛利中高 | 中 | 周期性强，但高端大尺寸基板壁垒高 |
| 材料 underfill/ABF film/photoresist | 高 ROIC | 高 | 小材料、大失效成本，客户认证后粘性强 |
| 服务器 ODM/OEM | 毛利较低 | 中 | 美元收入大，但 HBM/GPU 价值被上游捕获 |

**结论：** 2026 年买“确定性瓶颈”是 HBM 成品和绑定 NVIDIA/AMD/ASIC 的供应份额；2027 年买“代际升级期权”是 HBM4E/cHBM、hybrid bonding、test/probe、HBM IP 和 base die foundry 协同。

## 6. 2026 关键变化：最可能发生的 3 个拐点

### 拐点一：HBM3E 12Hi 成为 Blackwell Ultra / ASIC 的全年主力，价格继续强势

2026 上半年 NVIDIA 上修 B300/GB300 目标，HBM3E 订单同步增加。Google TPU、AWS Trainium、Microsoft Maia、Meta/Broadcom MTIA、OpenAI/Broadcom ASIC 的放量意味着 HBM3E 不再是 NVIDIA 单一客户故事，而是 AI 基础设施共同标准。基准情景下，HBM3E 2026 收入可达 $42-55B；极度超预期可到 $70-90B。

### 拐点二：HBM4 从“验证故事”变成“多供应商商业出货”

Samsung 2026 年 2 月宣布 HBM4 量产并商用出货；Micron 2026 年 3 月宣布 HBM4 36GB 12H 已在 2026Q1 volume shipment；SK hynix 早在 2025 年 9 月宣布完成 HBM4 开发和量产体系。TrendForce 预计三家都将进入 NVIDIA HBM4 供应链。2026 的核心不是谁宣布第一，而是谁能稳定拿到 Rubin/MI400/ASIC 的 **bit allocation + good die yield**。

### 拐点三：内存预算从 GPU HBM 扩散到 AI memory hierarchy

Micron/Samsung 在 GTC 2026 同时推 HBM4、SOCAMM2、PCIe Gen6 SSD；NVIDIA Vera Rubin 体系同时包含 GPU、CPU、DPU、storage rack、Ethernet rack。AI Agent、长上下文、KV cache 和 RAG 让 DDR5、SOCAMM2、SSD、CXL 成为 HBM 的外延市场。内存从“GPU BOM 项”升级为“AI factory 系统预算项”。

## 7. 2027 关键变化：最可能发生的 3 个拐点

### 拐点一：HBM4/HBM4E 成为高端新增平台主流

Rubin、Rubin Ultra、MI400/MI500、TPU8、Trainium4、Meta/OpenAI/Broadcom ASIC 将把 HBM4 和 HBM4E 推到主力位置。基准情景下 HBM4/HBM4E 2027 收入 $80B+；乐观情景 $150B+；极度超预期情景 $220B+。

### 拐点二：custom HBM 把竞争从“内存制程”推向“foundry + memory + package 联合设计”

HBM4 起 logic base die 更重要，cHBM 进一步要求客户定制 base die、接口、电源、热和测试。Samsung 的一体化模式、SK hynix + TSMC 模式、Micron 的客户工程和能效路线会形成三种竞争结构。2027 开始，谁能参与客户早期定义，谁就能获得溢价和份额。

### 拐点三：先进封装/测试扩产缓解一部分短缺，但瓶颈从“有没有货”转向“谁被认证”

SK hynix P&T7 计划 2027 年底前完工，M15X 与 Cheongju 后道集群强化；TSMC CoWoS、OSAT、ABF 基板、probe/test 也会扩张。到 2027 下半年，纯产能短缺可能有所缓解，但高端平台认证、良率、客户 LTA 仍让头部供应商维持定价权。

## 8. 头部公司与细分领域全景清单

### 8.1 HBM / 高带宽内存供应商

| 细分 | 头部公司 | 技术/产能优势 | 备注 |
|---|---|---|---|
| HBM3E / HBM4 | SK hynix | HBM3E 领先、MR-MUF、NVIDIA 长期合作、Cheongju/M15X/P&T7 | 2026 仍是份额核心 |
| HBM3E / HBM4 / HBM4E / cHBM | Samsung Electronics | 1c DRAM、4nm logic base die、memory + foundry + packaging 一体化、HCB | 2026 HBM4 追赶最强 |
| HBM3E / HBM4 / SOCAMM2 / SSD | Micron | HBM4 36GB 12H volume shipment、16H samples、1γ、SOCAMM2/Gen6 SSD 组合 | 美国供应链和能效叙事强 |
| 国产高带宽内存潜在 | CXMT、Huawei 生态、长江存储/国内封测链 | 国产 AI 芯片需求拉动 | 高端 HBM 与先进封装仍有明显差距 |
| NAND/HBF 潜在 | SanDisk/Western Digital、SK hynix/Solidigm、Kioxia、Samsung、Micron、YMTC | 高容量高带宽 flash 可能用于 KV cache | 主流放量更靠后 |

### 8.2 AI 芯片/客户生态

| 生态 | 关键公司 | 对 HBM 的意义 |
|---|---|---|
| Merchant GPU | NVIDIA、AMD、Intel | NVIDIA B300/GB300 决定 2026 HBM3E；Rubin 决定 2027 HBM4；AMD MI400 提供第二需求源 |
| Cloud ASIC | Google/Broadcom、AWS/Annapurna、Microsoft、Meta/Broadcom、OpenAI/Broadcom | 将 HBM 需求从 GPU 扩散到自研 ASIC，降低单一客户风险但提高定制化 |
| ASIC 设计服务 | Broadcom、Marvell、Alchip、GUC、Faraday、Socionext、Fujitsu | HBM PHY/controller、base die、advanced package 需求增加 |
| 中国 AI 芯片 | Huawei、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Iluvatar、Moore Threads、Enflame、MetaX、Hygon | 国产 HBM/封装/DDR 高带宽内存长期期权 |
| 推理专用 | Groq、Cerebras、Tenstorrent、SambaNova、d-Matrix、Etched、MatX、Furiosa、Rebellions | 部分使用 HBM，部分用 SRAM/GDDR/LPDDR；推动多层 memory hierarchy |

### 8.3 HBM IP / EDA / 接口

| 细分 | 公司 | 优势 |
|---|---|---|
| HBM controller/PHY | Rambus、Synopsys、Cadence、Siemens EDA | HBM4/4E 控制器、PHY、验证 IP；ASIC 客户粘性强 |
| Die-to-die / chiplet | Synopsys、Cadence、Alphawave Semi、Rambus、Ayar Labs、UCIe 生态 | HBM 与 chiplet/xPU 封装协同 |
| SI/PI/thermal EDA | Cadence、Synopsys、Siemens EDA、Ansys | HBM4 2048-bit、PDN、thermal signoff 难度上升 |

### 8.4 设备、材料、封测、基板

| 环节 | 公司 |
|---|---|
| EUV/光刻/量测 | ASML、KLA、Applied Materials、Lam Research、Tokyo Electron、ASM、Lasertec、Onto Innovation、Camtek |
| TSV/沉积/刻蚀/CMP | Applied Materials、Lam Research、TEL、ASM、KLA、EBARA、SCREEN |
| TC bonder / hybrid bonding | Hanmi Semiconductor、Hanwha Semitech、ASMPT、BE Semiconductor、SUSS MicroTec、Kulicke & Soffa、Applied Materials |
| Wafer thinning/dicing | DISCO、Tokyo Seimitsu/Accretech |
| ATE / burn-in | Advantest、Teradyne、Cohu、Chroma |
| Probe card | FormFactor、Technoprobe、Japan Electronic Materials、Microfriend |
| OSAT / advanced packaging | TSMC、ASE、Amkor、Samsung、Intel Foundry、JCET、Powertech/PTI、KYEC、Hana Micron、Tongfu Microelectronics、Huatian |
| ABF/BT substrate | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、Samsung Electro-Mechanics、AT&S、LG Innotek、Daeduck |
| 材料 | Ajinomoto、Resonac、Namics、Henkel、Dow、DuPont、Shin-Etsu、SUMCO、GlobalWafers、JSR、Tokyo Ohka、Merck/EMD、Entegris、FUJIFILM Electronic Materials |
| CXL/内存模块 | Montage Technology、Astera Labs、Rambus、Microchip、SMART Modular、Viking、Innodisk、Samsung、Micron、SK hynix |

## 9. 投资观察框架：2026 买确定性，2027 买代际期权

### 9.1 2026 最确定方向

| 排名 | 方向 | 理由 | 关键验证指标 |
|---:|---|---|---|
| 1 | HBM3E 12Hi 供应份额 | B300/GB300 与 ASIC 主力，2026 收入确定性最高 | NVIDIA/AMD/Google/AWS 订单、ASP、bit allocation |
| 2 | HBM4 12Hi 早期认证 | 2027 主力平台前置采购 | Rubin/MI400/TPU8 qualification、yield、客户公告 |
| 3 | HBM test/probe/TC bonding | 所有新增 HBM 都需要，且不易绕开 | 设备订单、交期、毛利率、客户集中度 |
| 4 | CoWoS/ABF 高端封装 | xPU + HBM 有效交付瓶颈 | TSMC CoWoS 扩产、ABF 价格、OSAT 外包比例 |
| 5 | SOCAMM2/DDR5/MRDIMM | AI 推理内存层级扩散 | Vera CPU、BlueField、CPU inference server 设计 |

### 9.2 2027 弹性最大方向

| 排名 | 方向 | 理由 |
|---:|---|---|
| 1 | HBM4E / 16Hi | 平台换代 + 单 stack 价值上升 + 客户缺货 |
| 2 | custom HBM/cHBM | 把 HBM 从标准品变成客户联合研发品，溢价更强 |
| 3 | Hybrid copper bonding | 16Hi/更高层数的核心良率工具 |
| 4 | HBM IP/PHY/controller | ASIC 客户数量增加，轻资产高毛利 |
| 5 | CXL/pooled memory/HBF | 推理 memory hierarchy 的长期补充 |

## 10. 主要来源与交叉验证

| 类型 | 来源 | 本报告使用的信息 |
|---|---|---|
| 一手公司公告 | [Samsung HBM4 press release](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | HBM4 量产/商用出货、11.7Gbps、最高 13Gbps、3.3TB/s、1c DRAM、4nm base die、HBM sales 2026 >3x、HBM4E H2 2026 samples、cHBM 2027 samples |
| 一手公司公告 | [Micron HBM4 for NVIDIA Vera Rubin](https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin) | HBM4 36GB 12H 2026Q1 volume shipment、>2.8TB/s、+20% power efficiency、48GB 16H samples、SOCAMM2/PCIe Gen6 SSD 量产 |
| 一手公司页面 | [Micron HBM4 product page](https://www.micron.com/products/memory/hbm/hbm4) | 2048-pin bus、>11Gbps、>2.8TB/s、HBM4 12H 36GB、HBM 制造流程 |
| 一手公司公告 | [SK hynix HBM4 development](https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/) | HBM4 开发完成、2048 I/O、>10Gbps、功耗效率 +40%、MR-MUF、1bnm |
| 一手/公司市场展望 | [SK hynix 2026 HBM supercycle outlook](https://news.skhynix.com/2026-market-outlook-focus-on-the-hbm-led-memory-supercycle/) | BofA 2026 HBM 市场 $54.6B、+58%；HBM3E 约占 2026 出货三分之二；Counterpoint SK hynix 2025Q2 shipment 62%、Q3 revenue 57% |
| 行业报告 | [TrendForce HBM4 validation 2026Q2](https://www.trendforce.com/presscenter/news/20260213-12929.html) | 三大供应商有望进入 NVIDIA HBM4 供应链；Samsung 验证进度快，SK bit allocation 优势，Micron 也预计 Q2 完成 |
| 行业报告 | [TrendForce China: HBM4 delay and HBM3E demand](https://www.trendforce.cn/presscenter/news/20260108-12870.html) | NVIDIA 上调 HBM4 speed-per-pin 至 11Gbps 以上，HBM4 放量延后；B300/GB300 和 HBM3E 订单上修 |
| 行业报告 | [TrendForce memory wall](https://www.trendforce.com/insights/memory-wall) | 2026 HBM consumption 仍 +70% 以上；HBM4 2048-bit/2TB/s；memory wall 与 DDR5 价格扩散 |
| 行业报告 | [TrendForce memory supercycle](https://www.trendforce.com/presscenter/news/20260209-12917.html) | 2026 memory market $551.6B；AI 推动 memory revenue 超 foundry；CSP 价格敏感度低 |
| 行业报告 | [Gartner semiconductor 2026 forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | 2026 半导体 $1.320T、memory $633.3B、DRAM 价格 +125%、AI 半导体占 30%、hyperscaler AI infra spending +50% |
| 一手公司财报 | [Micron FY2026 Q2 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026) | FY2026 Q2 revenue $23.86B、gross margin 74.4%、FY2026 Q3 gross margin 指引约 81% |
| 一手公司展示 | [Samsung 1Q 2026 earnings presentation](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_1Q_conference_eng.pdf) | Memory 供应有限、行业涨价、HBM4/SOCAMM2 for NVIDIA Vera Rubin、2H 2026 HBM4E samples |
| 一手公司公告 | [NVIDIA Vera Rubin GTC 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | Vera Rubin 七类芯片 full production、NVL72、NVLink 6、ConnectX-9、BlueField-4、Spectrum-6、agentic AI factory |
| 行业/新闻 | [Yonhap: SK hynix P&T7](https://en.yna.co.kr/view/AEN20260113002300320) | SK hynix 19 万亿韩元 P&T7 后道封装测试厂，2026 年 4 月开工，2027 年底前完成；HBM CAGR 33% through 2030 |
| IP 公司页面 | [Rambus HBM controller IP](https://www.rambus.com/interface-ip/hbm/) | HBM4E controller up to 16Gbps/pin、4TB/s+，HBM4/4E 2048-bit 接口与 IP 价值 |
| 项目底稿 | `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md` | 2026-2027 出货量最大 AI 芯片平台、B300/GB300、TPU、Trainium、MI350/MI400、Maia、MTIA 等技术路径 |
| 项目底稿 | `D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md` | AI 数据中心 CapEx 中 HBM/DRAM/SRAM、GPU/ASIC、先进封装、供电/液冷的三情景约束 |

---

**最终判断：**  
2026 年 HBM 与高带宽内存行业的投资价值来自“AI 基础设施建设速度大于内存供给扩张速度”。基准情景下，HBM3E 12Hi 是现金流，HBM4 12Hi 是增长，SOCAMM2/DDR5/SSD 是外延；乐观情景下，三大 HBM 厂同时扩产但仍被云厂商预定；极度超预期情景下，Rubin、MI400、TPU8、Trainium3/4、OpenAI/Meta/Broadcom ASIC 同时把 2027 需求前置，HBM4E 和 custom HBM 提前进入商业化，内存从 AI 服务器 BOM 的一个部件升级为 AI factory 的核心稀缺资产。
# 行业调研：【HDD、对象存储与冷温数据存储】

> 版本日期：2026-05-08  
> 研究口径：未来 3 个月指 2026-05 至 2026-08；未来 1 年指 2026-05 至 2027-04；未来 2 年指 2026-05 至 2028-04。市场规模如未特别说明，均为美元名义收入池或采购额，`B` = 十亿美元。  
> 核心假设：对 2026 年 AI 数据中心建设抱乐观预期。对缺失的直接数据，采用“GPU/ASIC 上电节奏、云厂商长期供货协议、单位 TB 成本、对象存储 attach rate”推导，并明确标为模型假设。

## 0. 最高浓度结论

1. **HDD 不但没有被 AI 边缘化，反而在 2026 重新获得定价权。** AI 数据湖、训练语料、视频/多模态输出、RAG 索引、checkpoint、合规留存和对象归档让“热层 SSD + 温层对象 + 冷层 HDD/磁带”的分层结构更清晰。Seagate FY2026 Q3 收入 $3.11B、non-GAAP gross margin 47.0%；Western Digital FY2026 Q3 收入 $3.337B、non-GAAP gross margin 50.5%，并指引 FY2026 Q4 non-GAAP gross margin 51-52%。这是典型卖方市场利润率，而不是成熟硬件均值回归。
2. **2026 最可能放量的技术路径是两条并行：Seagate HAMR/Mozaic 与 WD ePMR/UltraSMR/OptiNAND。** Seagate 已把 Mozaic 4+ 44TB nearline HDD 投入 revenue shipment，Mozaic 5+ 50TB 计划 2027 年底客户 qualification；WD 已在 2026-02 发布 40TB UltraSMR ePMR，预计 2026H2 volume shipment，同时 HAMR qualification 已开始，2027 年进入 ramp。
3. **对象存储正在从“低成本容量池”升级为 AI 基础设施的控制面和上下文层。** AWS 在 2026-04 推出 S3 Files，把 S3 bucket 直接暴露为共享文件系统；NVIDIA 在 GTC 2026 推出 BlueField-4 STX 与 CMX，使对象/文件存储能够参与上下文数据路径，官方给出的提升是 tokens/sec 最高 5x、能效最高 4x、数据摄取最高 2x。这意味着对象存储厂商从“便宜 TB”进入“GPU 利用率工具链”。
4. **冷数据不会冷门。** LTO-10 已把单盘 cartridge 提升到 30TB native / 75TB compressed、400MB/s native 传输；Quantum 新一代 Scalar i7 RAPTOR 宣称单 rack 最高 60PB、相对归档磁盘 operational cost 降低约 70%。AI 训练数据、合规、主权 AI 和模型输出留存会让磁带/对象归档成为 2026-2027 的二阶受益环节。
5. **2026-2027 AI 数据中心 SSD/HDD/数据存储采购池，基准情景可从 2026 年 $25-45B 增至 2027 年 $35-65B；乐观情景 $35-65B 增至 $55-95B。** 其中 HDD/对象/归档相关约占一半以上，企业级 SSD 和 KV cache warm tier 占另一半。极度超预期情景下，若 agentic inference 与视频生成同时爆发，2027 年 AI 相关 SSD/HDD/对象/归档采购池可冲击 $110B+。

## 1. AI 大规模建设下的行业机遇、挑战与技术路径

### 1.1 需求如何传导到 HDD、对象存储和冷/温数据

项目内 AI 芯片路线图显示，2026 至 2027 年初出货量和价值权重最高的平台包括 NVIDIA B300/GB300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon MLU590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia200，以及 Alibaba Zhenwu 810E 和 AMD MI400/MI455X。它们对存储的影响不是线性的“多一台服务器多一块盘”，而是四层放大：

| AI 芯片/集群变化 | 对存储的直接影响 | 最受益层 |
|---|---|---|
| GB300/B300、Trainium2、Ironwood 在 2026 大规模上电 | 训练数据湖、checkpoint、模型版本、向量/RAG 数据长期保存 | 对象存储、nearline HDD、数据管理软件 |
| Rubin、MI400/MI455X、TPU8、Trainium3 在 2027 加速 | HBM4/长上下文拉高中间态数据和 KV cache；checkpoint 规模继续上行 | 高性能对象/并行文件、eSSD warm tier、STX/CMX |
| agentic inference 和视频/多模态推理扩张 | token、日志、检索、用户文件、生成内容留存指数级增长 | S3-compatible object、cold object、HDD archive |
| 主权 AI、行业 AI、企业私有部署 | 数据不能随意外流，需要本地对象存储和长期归档 | Cloudian、Scality、MinIO、Dell、NetApp、IBM、HPE、Ceph |

### 1.2 2026-2027 技术成熟与放量时间表

| 技术路径 | 2026 状态 | 2027 状态 | 基准放量时间 | 乐观放量时间 | 极度超预期乐观放量时间 | 投资判断 |
|---|---|---|---|---|---|---|
| HAMR / Seagate Mozaic 3+/4+ | 30TB/32TB 已商业化，44TB Mozaic 4+ revenue shipment | 44TB 扩产，50TB Mozaic 5+ 客户验证 | 2026H2 | 2026Q2-Q3 | 2026Q2 即被 hyperscaler 长约锁死 | 2026 最强技术 beta，毛利率弹性大 |
| ePMR + OptiNAND + UltraSMR / WD | 32TB ePMR、40TB UltraSMR qualification，2026H2 volume | 40TB 主流化，HAMR ramp 接力 | 2026H2 | 2026Q3 | 2026Q2-Q3 大客户提前拉货 | 量最大、风险较低，UltraSMR 是云厂商默认高密路径之一 |
| FC-MAMR + 12-disk helium / Toshiba | 30TB/32TB/34TB SMR sampling；28TB CMR 预计 2026Q3 | 进入更广 nearline 客户验证 | 2027H1 | 2026Q4 | 2026H2 被日系/亚洲云客户提前采用 | 第三供应源价值上升，但份额仍受客户认证慢影响 |
| Host-managed SMR / Zoned Storage | hyperscaler 已成熟使用 | 更高比例进入对象归档和温层 | 已放量 | 已放量 | 已放量且价格溢价扩大 | 软件/固件/调度能力决定谁能卖高价 |
| 对象存储 + S3 API + erasure coding | 云端和 on-prem 已成熟；S3 Files 扩大应用面 | 与 AI 数据平台、表格式和向量检索进一步融合 | 已放量 | 已放量 | AI 数据湖默认底座 | 长期赢家是云厂商和高性能对象软件 |
| NVIDIA STX / CMX / storage accelerator | 2026H2 合作伙伴系统可用 | 2027 生产集群采用，尤其 RAG/agentic inference | 2027H1 | 2026H2 | 2026H2 进入头部客户标准 rack | 新兴高毛利方向，能把存储预算从 capacity 拉向 performance |
| LTO-10 / active archive | 30TB native、75TB compressed；新库系统发布 | 主权 AI、企业归档、备份恢复增长 | 2026H2 | 2026Q2-Q3 | AI 监管和数据留存强制拉动 | 稳健、低估值、现金流型受益 |
| 陶瓷/玻璃/光存储、DNA 存储 | 仍为试点/验证 | 2027 可能有 hyperscale PoC | 2029 以后 | 2028 以后 | 2027 出现示范订单但非大规模收入 | 可跟踪，不应作为 2026 主线 |

### 1.3 机会与挑战

| 机会 | 关键事实/模型判断 |
|---|---|
| nearline HDD 供给进入 LTA 锁定 | 公开媒体和公司口径均显示，大客户把 HDD/SSD 长约拉长至 3-5 年；Seagate、WD 的高毛利和强指引验证价格纪律。 |
| AI 数据从热训练走向“全生命周期保存” | 训练语料、清洗后数据集、checkpoint、模型权重、推理日志、RAG 文档、用户上传内容、合规留存都不能只放在 eSSD。 |
| HDD 容量代际重新加速 | 30-34TB 已经放量/送样，40-44TB 进入 2026 商业窗口，50TB 指向 2027 末验证。 |
| 对象存储从容量层变成 AI 数据层 | S3 Files、S3 Vectors、Iceberg/S3 Tables、STX/CMX 让 S3-compatible object 与模型上下文、表格式、向量检索结合。 |
| 冷归档被 AI 监管和主权数据拉动 | 企业会被迫保存训练数据来源、模型版本、输出日志和审计轨迹，冷归档从“可选降本”变成“合规基础设施”。 |

| 挑战 | 投资含义 |
|---|---|
| hyperscaler 认证周期长 | HDD 从 qualification 到 fleet ramp 往往 2-6 个季度；新技术收入确认比新闻稿慢。 |
| SMR 不是所有客户都能用 | host-managed SMR 需要对象层、调度和写入模式配合；企业客户采用慢于云厂商。 |
| all-flash 阵列在热层继续侵蚀 HDD | KV cache、向量库、实时检索仍偏 eSSD/QLC；HDD 赢的是温冷容量和低 W/TB。 |
| 数据中心电力也限制存储 | HDD 单 TB 功耗下降，但总 EB 增长会拉高 rack、网络、冷却和维护复杂度。 |
| 云厂商自研压缩利润池 | hyperscaler 能通过长约、认证和联合开发取得低价，小厂如果没有软件壁垒会被压价。 |

## 2. 已开始放量的关键产品：市场规模、渗透率与利润率

### 2.1 总市场框架

项目内数据中心建设模型给出的 2026-2027 SSD/HDD/数据存储订单池为：

| 场景 | 2026 AI 相关 SSD/HDD/数据存储订单 | 2027 AI 相关 SSD/HDD/数据存储订单 | 主要假设 |
|---|---:|---:|---|
| 基准 | $25-45B | $35-65B | GB300/Trainium2/Ironwood 稳定上电，HDD 供应紧但可交付 |
| 乐观 | $35-65B | $55-95B | agentic inference、RAG、视频生成带动 warm/cold 数据持续增长 |
| 极度超预期乐观 | $55-80B | $85-120B+ | 2027 需求前置，hyperscaler 抢签 HDD/SSD/对象存储长约，价格继续上行 |

### 2.2 已放量产品拆分

| 已放量产品/技术 | 2026 渗透率基线 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 基准增长 | 乐观增长 | 极度超预期乐观增长 |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| 24-32TB nearline CMR/ePMR HDD | nearline HDD EB 的 45-55% | 基准 $3.5-4.8B；乐观 $4.8-6.0B；极乐观 $6.0-7.5B | 基准 $15-21B；乐观 $21-28B；极乐观 $28-36B | 基准 $18-25B；乐观 $25-35B；极乐观 $35-48B | 2026 仍是主力，2027 被 36-44TB 部分替代 | +15-25% | +30-45% | +50%+ |
| 28-40TB SMR / UltraSMR HDD | nearline HDD EB 的 20-30% | $1.4-2.4B / $2.4-3.4B / $3.4-4.8B | $7-12B / $12-18B / $18-26B | $12-22B / $22-35B / $35-52B | hyperscaler object/cold 默认高密度盘；企业采用较慢 | +35-55% | +60-90% | +100%+ |
| 30-44TB HAMR HDD | nearline HDD EB 的 5-12% | $0.8-1.6B / $1.6-2.5B / $2.5-4.0B | $5-10B / $10-16B / $16-25B | $12-25B / $25-42B / $42-65B | 2026 qualification 转 revenue ramp；2027 进入主流采购 | +80-120% | +150-220% | +250%+ |
| S3-compatible cloud object storage | AI/云存储容量层 50%+ | $8-12B / $12-16B / $16-22B | $38-55B / $55-75B / $75-105B | $60-90B / $90-130B / $130-180B | S3 API 是事实标准；AI 数据湖、向量、表格式继续增强 | +25-35% | +40-55% | +70%+ |
| Enterprise/on-prem object storage | 企业非结构化存储 15-25% | $1.2-2.0B / $2.0-2.8B / $2.8-4.0B | $6-9B / $9-13B / $13-19B | $9-15B / $15-24B / $24-36B | 主权 AI、私有 RAG、合规归档拉动 | +20-35% | +40-60% | +80%+ |
| Active archive / LTO-10 / object+tape | 企业冷归档 20-30% | $0.6-1.0B / $1.0-1.5B / $1.5-2.3B | $3-5B / $5-7B / $7-10B | $5-8B / $8-12B / $12-18B | AI 审计和长期留存提高 attach rate | +10-20% | +25-40% | +55%+ |

### 2.3 已放量产品利润率预测

| 产品/技术 | 当前利润率证据 | 基准毛利率 | 乐观毛利率 | 极度超预期乐观毛利率 | 为什么能维持 |
|---|---|---:|---:|---:|---|
| HDD OEM nearline 组合 | Seagate FY2026 Q3 non-GAAP GM 47.0%；WD FY2026 Q3 non-GAAP GM 50.5% | 42-48% | 48-54% | 54-60% | 三家寡头、qualification 长、客户长约、AI 抢货 |
| HAMR 高容量盘 | Seagate 44TB revenue shipment，新平台稀缺 | 48-55% | 55-62% | 62-68% | 单 TB TCO 明显改善，早期供给稀缺，头部客户愿意溢价 |
| SMR/UltraSMR 高密度盘 | hyperscaler 已能消化 host-managed SMR | 45-52% | 52-58% | 58-64% | 容量密度与 W/TB 优势可量化，软件适配形成客户锁定 |
| 云对象存储服务 | hyperscaler 服务毛利通常高于硬件，但 capex 重 | 55-70% 服务毛利 | 65-75% | 75%+ | API 锁定、数据重力、egress、生态工具、合规功能 |
| 企业对象软件/一体机 | 软件订阅和支持占比高 | 55-70% | 65-78% | 75-82% | S3 兼容、对象锁、合规、跨站点 erasure coding、客户认证 |
| 磁带库/active archive | 硬件中等，介质和服务稳定 | 35-50% | 45-55% | 55-60% | 冷数据 TCO 独特，介质生态集中，库系统替换成本高 |

## 3. 在研关键产品：成熟时间、市场规模与利润率

| 在研/早期 ramp 技术 | 当前状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 基准/乐观/极乐观利润率 |
|---|---|---:|---:|---:|---|---|
| Seagate Mozaic 5+ 50TB HAMR | 2027 年底客户 qualification 目标 | 近 0 | $0-0.5B / $0.5-1B / $1-2B | $3-8B / $8-16B / $16-28B | 2027 末验证，2028 放量 | 55-65% / 62-70% / 70%+ |
| WD HAMR 40TB+ | qualification 已开始，2027 ramp | $0-0.3B | $1-3B / $3-6B / $6-10B | $8-16B / $16-28B / $28-45B | WD 客户基盘大，2027 一旦过认证会很快 | 50-58% / 58-65% / 65%+ |
| Toshiba 12-disk / HAMR 后续 | M12 FC-MAMR sampling，HAMR 后续路线 | $0.1-0.3B | $1-2B / $2-4B / $4-7B | $4-8B / $8-14B / $14-22B | 第三供应源战略价值提高 | 35-45% / 45-52% / 52-58% |
| 高带宽 HDD / dual actuator / dual pivot | WD 宣称 2028 high-bandwidth HDD | 近 0 | 近 0 | $1-3B / $3-6B / $6-10B | 2028 起用于温数据并行读、AI 数据摄取 | 45-55% / 55-62% / 62%+ |
| NVIDIA STX / CMX 存储加速 | 2026H2 partner systems 可用 | $0.1-0.4B | $1-3B / $3-6B / $6-10B | $6-12B / $12-22B / $22-35B | 从 RAG/agentic inference 试点到 2027 生产 | 软件/加速器 60-75% / 70-80% / 80%+ |
| S3 Vectors / object-native vector tier | AWS 已预览，目标低成本向量存储 | $0.1-0.5B | $1-4B / $4-8B / $8-14B | $5-12B / $12-24B / $24-40B | 冷/温向量与实时向量库分层 | 云服务 60-75% / 70-80% / 80%+ |
| 陶瓷/玻璃长期归档 | Cerabyte 等处于试点/合作阶段 | 近 0 | $0-0.2B | $0.2-1B / $1-3B / $3-8B | 2027 可能有示范订单，2029+ 才看规模 | 早期不稳定，若成功长期 60%+ |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区/公司 | 产能/工艺特征 | 供给判断 |
|---|---|---|---|
| HDD 整机 | Seagate、Western Digital、Toshiba；产能集中在泰国、马来西亚、菲律宾、中国等亚洲基地 | helium sealed drive、10-12 platter、CMR/SMR、HAMR/ePMR/MAMR | 三家寡头，扩产不是简单加线，需要洁净制造、良率和客户认证 |
| HDD 磁头/悬臂 | TDK、Seagate/WD 内部能力、相关日美精密供应链 | HAMR 需要 near-field transducer、激光/热辅助结构 | HAMR 放量最大隐性瓶颈之一 |
| 磁盘介质/基板 | Resonac/Showa Denko、HOYA、Nippon Electric Glass、Seagate/WD 内部介质 | 玻璃/铝基板、磁性薄膜、HAMR media | 12-disk 与更高 areal density 提高良率难度 |
| HDD 控制器/PCB | Marvell、Broadcom、WD/Seagate 自研与合作 | SoC、DRAM/NAND cache、servo control、SMR firmware | 固件和 host-managed SMR 是价值点，不只是芯片 |
| 云对象存储 | AWS、Azure、Google、Oracle、Alibaba、Tencent、Huawei | 自建数据中心、分布式对象、erasure coding、生命周期管理 | 云厂商最强，但也给 on-prem S3 兼容市场留下主权空间 |
| 企业对象/文件 | Dell、NetApp、IBM、HPE、Pure、VAST、DDN、WEKA、Cloudian、Scality、MinIO、Qumulo、Ceph | 软件定义 + x86/ARM + HDD/QLC/eSSD 混合 | AI 需要高性能元数据、GPU 直连、S3/NFS/SMB 多协议 |
| 磁带/归档 | IBM、HPE、Quantum、Fujifilm、Sony、Spectra Logic | LTO drive/media/library、active archive software | 供给稳定，增长弹性来自合规和 AI 数据留存 |

### 4.2 供给瓶颈

1. **HAMR 磁头和 near-field transducer 良率。** 激光热辅助让磁头、介质和伺服控制同时升级，量产良率决定 44TB/50TB 成本曲线。
2. **高密度盘片、玻璃基板和 12-disk 机械公差。** 盘片更多、磁道更密、helium sealing 更严，任何微小偏差都会放大返工和测试时间。
3. **客户 qualification 和 fleet burn-in。** hyperscaler 不会只看单盘规格，必须验证 firmware、failure mode、rack vibration、power、rebuild、SMR 写放大，周期可达数个季度。
4. **host-managed SMR 软件栈。** SMR 的价值需要对象层写入调度、zone management、后台整理和运维经验，小客户很难复制 hyperscaler 效率。
5. **长期供货协议挤压现货。** 头部云厂商为了 2026-2027 AI 数据保供签长约，中小客户可能面对更高价格和更长交期。
6. **对象存储元数据和小文件性能。** AI/RAG 场景文件数量巨大，瓶颈常在 metadata、namespace、listing、consistency 和权限模型，不只是 TB。
7. **数据中心电力与 rack 认证。** HDD/对象节点虽然低于 GPU 功耗，但 EB 级 fleet 的 rebuild、网络和冷却会占用真实机房资源。
8. **磁带库驱动器与介质认证。** LTO-10 需要新 drive/media 生态匹配，企业采购节奏会慢于规格发布。

### 4.3 成本构成与价格传导

| 产品 | BOM/单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| nearline HDD | 磁头/盘片/介质 35-45%；机械件/马达/actuator/helium HDA 20-25%；PCB/SoC/缓存 10-15%；组装测试折旧 15-25%；保修 3-6% | 单盘 TB、良率、SMR 溢价、客户组合、LTA 价格 | 大客户按季度/半年合同；高容量盘以 $/TB TCO 和供货优先级定价 |
| HAMR HDD | 在传统 HDD 基础上增加 HAMR 头、激光/热辅助、HAMR media、更多测试 | 初期良率、qualification 通过率、客户愿意为 W/TB 付费 | 先对 hyperscaler 高溢价，随多厂商 HAMR 后下降 |
| 对象存储一体机 | HDD/SSD 45-65%；服务器/NIC/网络 15-25%；软件/支持 15-30% | 软件订阅、服务、容量扩容、S3/多协议功能 | 初始节点销售 + 容量扩容 + 支持续约，数据重力降低价格敏感度 |
| 云对象存储 | 数据中心折旧、电力、HDD/SSD、网络、软件平台、运维 | 利用率、生命周期管理、egress/API 请求、冷热分层 | list price + tiering + API/egress；客户迁移成本提高定价力 |
| 磁带归档 | drive/library 机器人、介质、软件、维护 | 介质耗材、库系统密度、服务续约 | 长周期 TCO 采购，容量扩展和介质消耗形成 recurring revenue |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | 结构 | 头部集中度判断 | 定价权 |
|---|---|---:|---|
| nearline HDD | Seagate、Western Digital、Toshiba 三家 | CR3 近 100%，Seagate+WD 在 nearline 收入/EB 中占绝大部分 | 高，尤其 30TB+ 与 HAMR/UltraSMR |
| 公有云对象存储 | AWS S3、Azure Blob、Google Cloud Storage、Oracle OCI、Alibaba OSS 等 | 前三/前四云厂商占云对象主导 | 高，数据重力和 API 锁定强 |
| 企业对象/文件 | Dell、NetApp、IBM、Pure、VAST、DDN、WEKA、HPE、Cloudian、Scality、MinIO、Ceph 等 | 分散，但 AI 高端市场向少数性能平台集中 | 中高，软件和认证决定 |
| 磁带归档 | IBM/HPE/Quantum/Fujifilm/Sony/Spectra 等生态 | LTO 生态集中 | 中，高端库系统和介质有稳定利润 |
| 新型长期归档 | Cerabyte、Microsoft Project Silica、DNA 存储公司 | 早期分散 | 未来高，现在商业不确定 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 为什么能定价 |
|---|---|---|
| areal density 和机械良率 | 每 TB 成本来自盘片密度、磁头能力、盘数、helium sealing、servo 精度 | 同样 rack 和功耗下更大容量直接降低客户 TCO |
| hyperscaler qualification | 大客户验证时间长，fleet 失败代价极高 | 一旦进白名单，替换成本高，供应商可拿长期合同 |
| SMR/firmware/host integration | 高密度 SMR 需要对象层和 firmware 共同优化 | 客户不是买硬盘，而是买稳定可预测的 EB 级写入模型 |
| 数据重力/API 锁定 | S3 API、IAM、lifecycle、object lock、egress、生态工具绑定 | 迁移 PB/EB 数据成本极高，云对象存储能长期收费 |
| 软件元数据性能 | AI 小文件、向量、RAG、checkpoint 需要高并发 metadata | 性能瓶颈会直接影响 GPU 利用率，客户愿意为确定性付费 |
| 合规/认证/不可变存储 | 金融、医疗、政府、AI 训练来源审计需要 WORM/object lock | 合规功能不是 commodity TB，出问题代价远高于价格 |
| 供应链规模 | HDD、磁带、云对象都是资本密集、认证密集行业 | 小厂无法快速扩产或承担保修/服务风险 |

### 5.3 价值捕获：长期高 ROIC/高毛利层

1. **第一层：HDD 高容量平台龙头。** 2026-2027 最可能维持高毛利的是 30TB+ nearline HDD，尤其 HAMR/UltraSMR 供不应求阶段。Seagate/WD 已经用 47-52% non-GAAP gross margin 验证。
2. **第二层：云对象存储服务。** AWS S3、Azure Blob、GCS 的高 ROIC 来自 API、数据重力、请求费、egress、生命周期和合规功能。硬件降本不一定传给客户。
3. **第三层：AI-native 高性能对象/文件软件。** VAST、DDN、WEKA、Pure、NetApp、Dell、IBM、MinIO、Cloudian、Scality 等若能把 GPU 利用率、RAG 延迟、checkpoint 时间量化，软件毛利可显著高于硬件。
4. **第四层：归档介质和库系统。** 增速不如 AI GPU 链，但现金流稳、替换周期长、合规驱动强。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

1. **HDD 从去库存周期切换到 AI 长约供给周期。** Seagate/WD 高毛利、长约、40TB/44TB 产品节点同时出现，说明行业从“拼价格”转向“拼可交付 EB”。
2. **对象存储从 archive/data lake 进入 AI runtime 附近。** S3 Files、S3 Vectors、NVIDIA STX/CMX、VAST/DDN/WEKA/Pure/Dell/NetApp 等 AI 存储方案让对象存储开始影响 tokens/sec、checkpoint 和 GPU 利用率。
3. **SMR 和 HAMR 同年成为主线。** SMR 依靠软件调度和高密度快速放量，HAMR 依靠 areal density 重新打开 40TB+ 成本曲线。2026 最可能放量的是 WD 40TB UltraSMR、Seagate 44TB HAMR、Toshiba 30-34TB FC-MAMR SMR 的客户验证。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

1. **HAMR 多厂商化与 50TB 级验证。** Seagate 50TB Mozaic 5+ qualification、WD HAMR ramp、Toshiba 后续 HAMR/12-disk 路线会决定 2028 成本曲线。若多厂商都过认证，EB 出货会放量；若只有单一厂商过，龙头溢价更高。
2. **AI 推理 warm tier 爆发。** Rubin、MI400、TPU8、Trainium3 和更多 custom ASIC 把长上下文、agentic inference、KV cache、RAG 文档从“应用层问题”变成“基础设施容量问题”。2027 最可能超预期的是高性能对象 + eSSD + HDD 分层平台。
3. **冷归档从备份走向 AI 治理。** 数据来源可追溯、模型版本保留、生成内容审计、主权 AI 本地保留，会使 LTO-10、对象锁、immutable archive、air-gap backup 的采购优先级上升。

## 8. 头部公司与细分技术全景

### 8.1 HDD 与关键零部件

| 细分 | 头部公司 | 优势 |
|---|---|---|
| HDD OEM | Seagate、Western Digital、Toshiba | 三家寡头；nearline qualification、客户长约、容量路线图 |
| HAMR | Seagate 领先，WD/Toshiba 追赶 | Seagate Mozaic 已商业 revenue；WD 2027 ramp 是第二变量 |
| ePMR/OptiNAND/UltraSMR | Western Digital | 40TB UltraSMR、OptiNAND 和客户基础强 |
| MAMR/FC-MAMR | Toshiba | 第三供应源，30-34TB SMR sampling |
| 磁头/悬臂 | TDK、Seagate/WD 内部供应链 | HAMR/MAMR 精密部件壁垒高 |
| 盘片介质/基板 | Resonac、HOYA、Nippon Electric Glass、Seagate/WD 内部介质 | 高密度盘片、玻璃基板、HAMR media |
| 电机/机械件 | Nidec、MinebeaMitsumi 等 | spindle motor、精密机械件 |
| 控制器/SoC | Marvell、Broadcom、HDD OEM 自研 | firmware、SMR、servo、接口控制 |

### 8.2 对象存储、公有云与 on-prem

| 细分 | 公司 | 位置 |
|---|---|---|
| 公有云对象 | AWS S3、Azure Blob、Google Cloud Storage、Oracle OCI Object Storage、Alibaba OSS、Tencent COS、Huawei OBS、IBM Cloud Object Storage | 最大收入池，API 和数据重力最强 |
| 企业对象/文件一体 | Dell ECS/ObjectScale/PowerScale、NetApp StorageGRID/ONTAP、IBM Storage Scale/COS、HPE Alletra Storage MP X10000、Hitachi Content Platform、Quantum ActiveScale | 企业客户、合规和混合云 |
| AI 高性能数据平台 | VAST Data、DDN Infinia/EXAScaler、WEKA、Pure Storage FlashBlade、Qumulo、Panasas/VDURA | checkpoint、RAG、GPU direct、metadata 性能 |
| S3-compatible 软件 | MinIO AIStor、Cloudian HyperStore、Scality RING/ARTESCA、Ceph/Red Hat OpenShift Data Foundation、Nutanix Objects | 私有云、主权 AI、边缘和成本敏感客户 |
| 低成本云对象 | Wasabi、Backblaze B2、Cloudflare R2 | 价格和 egress 策略差异化 |

### 8.3 冷/温数据与长期归档

| 细分 | 公司/项目 | 优势 |
|---|---|---|
| LTO 生态 | IBM、HPE、Quantum、Fujifilm、Sony、Spectra Logic | LTO-10、库系统、介质、长期兼容 |
| Active archive | Quantum、Spectra Logic、IBM、HPE、Fujifilm Object Archive | 数据保护、air gap、低 TCO |
| 云归档 | AWS S3 Glacier、Azure Archive Blob、Google Cloud Archive Storage、Oracle Archive Storage | 生命周期策略、低成本、合规 |
| 新型长期介质 | Cerabyte、Microsoft Project Silica、DNA Data Storage Alliance 相关公司 | 2027-2030 潜在颠覆，2026 仍早 |

## 9. 情景投资地图

| 子方向 | 2026 最可能走势 | 2027 最可能走势 | 最值得跟踪指标 |
|---|---|---|---|
| HDD OEM | 价格和毛利维持强势，30-44TB mix 改善 | HAMR/UltraSMR 竞速，50TB 验证 | Seagate/WD gross margin、nearline EB、LTA、30TB+ mix |
| HDD 零部件 | HAMR/MAMR 带来规格升级，但收入确认滞后 | 12-disk、HAMR media、磁头良率成为瓶颈 | HAMR drive qualification、media/head 订单 |
| 企业对象存储 | AI 数据湖、私有 RAG、主权 AI 拉动 | STX/CMX 和 GPU-adjacent storage 放量 | GPU 利用率案例、RAG 延迟、checkpoint 时间 |
| 云对象存储 | S3 Files/Vectors/Tables 扩大平台边界 | object-native AI 数据服务成为云厂商毛利池 | 存储收入增速、API 请求、egress 政策 |
| 磁带/active archive | LTO-10 替换和 AI 治理需求启动 | 合规/主权 AI 形成持续采购 | LTO media shipment、library backlog、监管要求 |
| 新型归档 | PoC 和战略合作 | 少量示范订单 | hyperscaler 是否给出量产时间表 |

## 10. 关键事实与来源

| 编号 | 来源 | 关键事实 |
|---|---|---|
| S1 | [Seagate FY2026 Q3 results](https://investors.seagate.com/news-releases/news-release-details/seagate-technology-reports-fiscal-third-quarter-2026-financial) | FY2026 Q3 revenue $3.11B；GAAP gross margin 46.0%；non-GAAP gross margin 47.0%；free cash flow $953M。 |
| S2 | [Seagate CFO commentary Q3 FY2026](https://investors.seagate.com/static-files/13fd8021-0760-47f7-a984-134a11fcbbf5) | Nearline cloud demand strong；Q4 revenue guide $3.35B +/- $150M；non-GAAP diluted EPS $3.40 +/- $0.20。 |
| S3 | [Seagate Mozaic 4+ press release](https://www.seagate.com/news/news-archive/seagate-extends-hard-drive-capacity-leadership-with-mozaic-4-plus-platform-pr/) | 44TB Mozaic 4+ platform revenue shipments in late March 2026；Mozaic 5+ 50TB qualification planned late 2027；Mozaic 6+ lab tests hit >6TB per platter / >60TB drive。 |
| S4 | [Western Digital FY2026 Q3 results](https://investor.wdc.com/news-releases/news-release-details/western-digital-reports-fiscal-third-quarter-2026-financial) | FY2026 Q3 revenue $3.337B；GAAP GM 48.7%；non-GAAP GM 50.5%；Q4 revenue guide $3.75-3.95B；non-GAAP GM 51-52%。 |
| S5 | [Western Digital AI-era storage roadmap](https://www.westerndigital.com/company/newsroom/press-releases/2026/2026-02-03-western-digital-accelerates-storage-innovation-for-ai-era) | 40TB UltraSMR ePMR qualification、2026H2 volume；HAMR quals underway、2027 ramp；100TB 目标 2029；high-bandwidth HDD with Dual Pivot in 2028。 |
| S6 | [Toshiba 12-disk nearline HDD sampling](https://storage.toshiba.com/corporateblog/post/2026/03/toshiba-ships-samples-of-12-disk-helium-sealed-nearline-hdds-with-up-to-34tb-and-conventional-recording-models-with-up-to-28tb) | M12 30TB/32TB/34TB SMR sampling；28TB conventional recording planned 2026Q3；FC-MAMR；2.5M hour MTTF；550TB/year workload。 |
| S7 | [NVIDIA BlueField-4 STX / CMX](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Launches-BlueField-4-STX-Storage-Architecture-With-Broad-Industry-Adoption/default.aspx) | STX/CMX for AI storage；tokens/sec up to 5x、energy efficiency up to 4x、data ingestion up to 2x；partner systems expected 2026H2。 |
| S8 | [AWS S3 Files launch](https://aws.amazon.com/blogs/aws/introducing-amazon-s3-files-making-s3-buckets-accessible-as-file-systems/) | 2026-04 Amazon S3 Files lets applications access S3 buckets as shared file systems；available in 34 commercial AWS Regions at launch。 |
| S9 | [AWS S3 object size increase](https://aws.amazon.com/blogs/aws/amazon-s3-increases-default-object-size-limits-from-5-tb-to-50-tb/) | 2025-12 S3 default object size limit increased from 5TB to 50TB；relevant for large AI datasets and checkpoints。 |
| S10 | [AWS S3 Vectors preview](https://aws.amazon.com/blogs/aws/introducing-amazon-s3-vectors-first-cloud-storage-with-native-vector-support-at-scale/) | S3 Vectors positions object storage as low-cost vector storage; AWS claims up to 90% lower cost for vector upload/storage/query versus specialized vector databases in some cases。 |
| S11 | [LTO Program Generation 10](https://www.lto.org/2025/08/the-lto-program-introduces-generation-10-of-leading-tape-technology-delivering-unparalled-media-density/) | LTO-10 cartridge 30TB native / 75TB compressed；native transfer rate 400MB/s。 |
| S12 | [Quantum Scalar i7 RAPTOR](https://www.quantum.com/en/company/news-room/2026/quantum-launches-scalar-i7-raptor-modern-tape-library-for-hyperscale-ai-cloud-and-enterprise-archive/) | Single rack up to 60PB；single library over 200EB；claims up to 70% lower operational cost than archival disk。 |
| S13 | [IDC enterprise storage systems 2026 forecast](https://www.businesswire.com/news/home/20260311384539/en/IDC-Worldwide-Enterprise-Storage-Systems-Market-Revenue-Grew-5.5-Year-Over-Year-in-4Q25-and-13.6-for-Calendar-2025) | 4Q25 enterprise storage systems revenue $9.7B, +5.5%；IDC forecasts 2026 $37.859B and 2027 $40.024B；AFA +18.1%，HDD arrays +3.1%。 |
| S14 | [Tom's Hardware on storage LTAs](https://www.tomshardware.com/pc-components/ssds/crushing-shortages-have-pushed-long-term-supply-agreements-for-ssds-and-hdds-to-record-five-years-large-customers-are-signing-large-contracts) | SSD/HDD long-term supply agreements reportedly extended to record 3-5 years as large customers secure capacity。 |
| S15 | 项目内文件 `ai_chip_research_2026_2027.md` | 2026-2027 出货量最大 AI 芯片/平台和路线图：GB300、Trainium2、Ironwood、GB200、Ascend、Cambricon、MI350、Trainium3、MTIA、Maia200、Alibaba、MI400。 |
| S16 | 项目内文件 `AI数据中心建设规模与产业链订单映射_2026-2027_美国.md` | AI 数据中心 SSD/HDD/数据存储订单池：2026 基准 $25-45B、2027 基准 $35-65B；乐观 2026 $35-65B、2027 $55-95B。 |

## 11. 风险提示

1. AI 推理商业化不及预期会降低 warm/cold 数据增速，但数据留存和合规需求仍提供底部支撑。
2. HDD 高毛利可能吸引客户延后采购或转向 QLC/eSSD，但在 EB 级冷/温容量上 HDD 的 TCO 仍最强。
3. HAMR 量产良率若低于预期，44TB/50TB 放量会推迟，短期反而利好成熟 ePMR/UltraSMR 和 CMR。
4. 对象存储竞争激烈，纯硬件节点供应商若没有软件、协议、元数据和 AI 工作流能力，难以捕获长期高 ROIC。
5. 本报告是产业研究和情景推演，不构成投资建议。
# 行业调研：【封装基板、中介层与RDL】

> 截至日期：2026-05-08  
> 研究口径：聚焦 AI 计算中心相关的先进封装基板、硅/有机/RDL 中介层、RDL fan-out/bridge、2.5D/3D 封装服务。金额均为美元名义值，`B` = 十亿美元。  
> 情景标记：`B/O/X` = 基准/乐观/极度超预期乐观。本文对 2026-2027 AI 基础设施建设采取偏乐观假设：需求端按 hyperscaler 和 AI startup 继续锁电、锁机柜、锁 HBM/CoWoS 处理；供给端用“交付能力”而非“潜在需求”约束上限。

## 0. 一句话结论

封装基板、中介层与 RDL 是 2026 AI 芯片从“买得到 GPU”升级为“交付得出整柜”的共同闸门。2026 最确定的路线不是玻璃基板或面板级封装，而是 **高层数大面积 ABF/FC-BGA + CoWoS-S/L/R + HBM3E/HBM4 过渡 + 少量 EMIB/SoIC/Foveros 分流**。2027 的拐点在于 Rubin/MI400/TPU8/Trainium3/OpenAI-Broadcom ASIC 把封装尺寸、HBM stack 数、RDL/桥接密度和基板翘曲控制一起推高，促使 **RDL interposer、CoWoS-L、EMIB-T、玻璃/陶瓷 core substrate** 从技术展示进入实质 NPI 和小批量收入。

投资价值排序：

1. **短期最强**：AI 高端 ABF/FC-BGA 基板、CoWoS 产能、RDL interposer/CoWoS-L、2.5D 封装测试设备与材料。
2. **2026 H2 到 2027 放量**：CSP ASIC 用大面积基板、AI switch ASIC 基板、RDL bridge/fan-out on substrate、HBM4 相关中介层和测试。
3. **2027-2028 期权**：EMIB-T、glass core substrate、ceramic core substrate、CoPoS/面板级 2.5D、光波导/CPO 基板。

## 1. 最近半年关键事实与一手锚点

| 时间 | 来源 | 关键信号 | 对本行业含义 |
|---|---|---|---|
| 2026-04 | TSMC 2026Q1 | 1Q26 revenue 约 $35.9B，gross margin 66.2%，2Q26 revenue guidance $39.0-40.2B、gross margin 65.5-67.5%。 | AI 先进节点和先进封装需求仍在抬升，TSMC 有强价格和排产能力。 |
| 2026-03 | TrendForce | 2026 全球晶圆代工收入预计 +24.8% 至约 $218.8B；AI GPU、CSP ASIC、OpenAI/Groq 等自研芯片在 2026 量产出货。 | 先进制程、CoWoS、ABF 和 RDL 不是单一 NVIDIA 周期，而是 GPU + ASIC 双周期。 |
| 2026-04 | TrendForce 报告摘要 | CoWoS 长期缺货，订单外溢至 SPIL/Amkor；Intel EMIB 获 AWS/Google 采用的说法进入产业报告。 | 2026 产能不是纯 TSMC 内部问题，OSAT 和替代桥接方案开始获得战略价值。 |
| 2025-10 至 2026 | Ibiden 法说 Q&A/报告 | Ibiden 称 AI server/ASIC 基板进入更大尺寸、多次层压、嵌入式电源组件；AI server IC package substrate 市占自估约 70-80%；2027 年底 SAP 能力较 2024H1 超过 2 倍。 | 高端 ABF 从周期品变成准战略产能，客户会为大面积、良率和认证付费。 |
| 2026-02 | Unimicron 法说会媒体转述 | 2026 capex 提升至约 NT$34B，约 70% 投入 ABF；AI 收入占比目标超过 60%，稼动率维持 90%+。 | 台湾 ABF 供给由“去库存”切回“客户预订+涨价传导”。 |
| 2026-04 | Samsung Electro-Mechanics Q1 | Package Solution sales 1Q26 为 KRW 725B，YoY +45%；强调 AI/server/network 高端 FCBGA、下一代高多层/大面积/embedded products。 | SEMCO 已从 AMD/server FC-BGA 切入，韩国/越南产能是 2026-2027 第二供应源。 |
| 2025-12/2026-01 | TOPPAN | Niigata FC-BGA 新线 2026-01 上线，面向 AI/data center；Niigata 能力达到 FY2022H1 的 2 倍，Singapore plant 预计 2026 年底投产。 | 日本新进入/扩产者在高端 FC-BGA、玻璃 core、organic RDL interposer 上加速。 |
| 2026-04 | Kyocera | 发布 AI xPU/switch ASIC 用 multilayer ceramic core substrate，ECTC 2026 展示，主打刚性、减小翘曲、三维布线。 | 有机基板翘曲逼近极限，陶瓷/玻璃 core 是 2027+ 的真实期权。 |
| 2026 | Intel Foundry | EMIB-T 增加 TSV，用于 HBM4/UCIe/垂直供电；Intel 称 EMIB 2.5D 支持 2026 年 >8x reticle、约 120x120mm、12 HBM、>20 EMIB，2028 年 >12x reticle、>120x180mm、>24 HBM。 | EMIB-T 是 CoWoS 的最现实替代/补充路线，先在自有或封装服务客户小批量上量。 |
| 2025-05 | AT&S | Malaysia Kulim 高端 IC substrate HVM，供应 AMD data center processors，并称未来客户会增加。 | 高端基板产能从日本/台湾向马来西亚/奥地利/韩国/越南扩散，但良率爬坡需要时间。 |

## 2. 技术图谱：封装基板、中介层、RDL 分工

### 2.1 三层结构

1. **封装基板**：芯片封装和主板之间的机械、电气、热和电源过渡层。AI GPU/ASIC 主流是高层数大面积 ABF/FC-BGA，重点指标是面积、层数、线宽线距、低损耗材料、翘曲、可靠性、SAP 良率。
2. **中介层**：die 与 HBM/其他 chiplet 之间的高密度互连层。包括硅中介层、RDL 中介层、局部硅桥、EMIB、玻璃/陶瓷/有机中介层。重点指标是 pitch、RC、TSV、HBM landing、良率和封装尺寸。
3. **RDL**：重布线层，通常由铜和聚合物构成，用于把 die I/O 重新分布到更大 pitch。它既可作为 fan-out 的核心，也可在 CoWoS-R/CoWoS-L、InFO-oS、organic RDL interposer、panel-level packaging 中承担关键互连。

### 2.2 TSMC 官方 CoWoS 路线的含义

TSMC 把 CoWoS 分为三类：

| 路线 | 核心结构 | 适用场景 | 投资含义 |
|---|---|---|---|
| CoWoS-S | 硅中介层，TSV/细 pitch 布线 | 最高带宽、成熟 HPC/GPU/HBM | 2026 主力，TSMC 产能和硅 interposer 良率决定出货。 |
| CoWoS-R | RDL interposer，铜/聚合物布线，TSMC 页面披露 RDL interposer 最小 4um pitch、2um L/S。 | 更大面积、更好 CTE 缓冲、成本低于全硅中介层 | 2026-2027 提升占比，用于缓解硅中介层面积/成本/产能限制。 |
| CoWoS-L | RDL-based interposer + embedded local silicon interconnect，LSI 支持高密度 die-to-die，并可集成 eDTC 改善电源。 | Blackwell/Rubin/大型 ASIC 这类大尺寸多 die 封装 | 2026 最可能成为高端 AI 的新增主线，RDL、LSI、embedded capacitor 和大基板同时受益。 |

### 2.3 与 2026-2027 出货主力 AI 芯片的映射

项目既有 AI 芯片路线图显示，2026-2027 年初出货/价值权重最高的平台大致包括 GB300/B300、Trainium2/3、TPU Ironwood/TPU8、GB200/B200、Rubin、AMD MI350/MI400、Meta MTIA、Microsoft Maia、OpenAI/Broadcom ASIC、Ascend/Cambricon 等。它们对本行业的拉动如下：

| 芯片/平台 | 2026-2027 阶段 | 封装/基板路径判断 | 2026 对应机会 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主力放量 | CoWoS-L/S + HBM3E + 大面积 ABF；NVL72 整柜拉动基板和封装测试。 | 最确定的 CoWoS-L/RDL、ABF、HBM landing、C4/underfill 收入池。 |
| NVIDIA B200/GB200 | 2026 延续交付 | CoWoS-S/L + ABF，技术成熟。 | 给供应链良率曲线和产能利用率打底。 |
| NVIDIA Rubin/Vera Rubin | 2026 H2 开始，2027 放量 | HBM4、更多/更大 interposer、CoWoS-L/Super Carrier、RDL 和电源完整性要求上升。 | 2026 先贡献 NPI、预订、设备和材料；2027 才是大收入。 |
| AWS Trainium2/3 | Trainium2 已大规模，Trainium3 2026-2027 接续 | HBM + 定制互连 + 高端基板；Trainium3 3nm、144-chip UltraServer 提高封装复杂度。 | 非 NVIDIA ASIC 产能池，拉动 ABF 和 OSAT 分流。 |
| Google TPU v7 Ironwood / TPU8 | Ironwood 2026 部署，TPU8 早期导入 | Broadcom/TSMC 生态，2.5D/HBM + 大基板；TPU8 将强化训练/推理分化。 | RDL/CoWoS/ABF 从 GPU 转向自用 ASIC。 |
| AMD MI350 | 2026 放量 | 2.5D + HBM3E + UBB/PCIe/基板；企业和云客户补位 NVIDIA。 | 基板和封装需求确定，但 2027 会被 MI400 接棒。 |
| AMD MI400/MI455X Helios | 2026 H2 早期，2027 主力 | HBM4、开放 rack、超大封装，对 RDL/CoWoS-L、ABF、液冷和供电同步提要求。 | 2026 是产能锁定和样品验证，2027 是弹性。 |
| Meta MTIA 300/400/450/500 | 2026-2027 多代迭代 | Broadcom XPU + FC-BGA/RDL/2.5D；推理 ASIC 更看成本和规模。 | AI ASIC 基板从少数 GPU 客户扩展到社交广告推理。 |
| Microsoft Maia 200 | 2026 Azure 导入 | TSMC 3nm、HBM3E、大封装、闭环液冷；高端基板。 | 推理 ASIC 认证长，一旦进 Azure 生命周期稳定。 |
| OpenAI/Broadcom ASIC | 2026 H2 起步，2027 多 GW | Broadcom XPU + 2.5D/RDL + 高端 ABF；重点是容量预订。 | 2027 极度乐观情景的最大新增变量之一。 |
| Ascend/Cambricon/国产 AI | 2026 国产替代 | 国产 2.5D/HBM/OAM + 本土 ABF/BT/封测爬坡。 | 受出口管制和本土云需求推动，技术差距由规模和系统互连弥补。 |

## 3. 2026 机遇、挑战与最可能技术路径

### 3.1 机会

1. **每颗高端 AI 芯片的封装价值量上升**：HBM stack 从 6/8 到 8/12，封装面积从 2x-4x reticle 走向 5x-8x，基板层数、尺寸、SAP 次数、RDL 层数同步提升。
2. **GPU + ASIC 双曲线**：NVIDIA Blackwell/Rubin 之外，Google/AWS/Meta/Microsoft/OpenAI/Broadcom/Marvell ASIC 同步争夺 HBM、CoWoS、ABF。
3. **产能预订货币化**：客户更愿意签 LTA、预付款、共同投资设备。对 Ibiden/Unimicron/SEMCO/AT&S/TOPPAN 这类供应商，订单能见度拉长。
4. **RDL 价值上移**：RDL 从 fan-out 智能手机时代的成本优化工具，变成 AI 大封装里解决面积、翘曲、局部高密互连和电源完整性的核心层。
5. **OSAT 外溢**：TSMC CoWoS 满载会把部分工序/客户外溢到 ASE/SPIL、Amkor、Samsung、Intel、JCET/TFME 等。

### 3.2 挑战

1. **材料约束**：ABF film、低 CTE 玻纤布/T-glass、低损耗树脂、铜箔、贵金属、underfill、临时键合胶同时紧张。
2. **大尺寸翘曲和良率**：AI 封装面积越大，CTE mismatch、C4 joint stress、warpage、void、污染颗粒造成的报废损失非线性放大。
3. **设备交期**：SAP/laser drilling/desmear/plating、TCB、hybrid bonding、wafer thinning、metrology、ATE/SLT/burn-in 都可能成为 12-24 个月瓶颈。
4. **客户认证不可压缩**：AI 芯片一代产品窗口通常只有一年左右，客户不愿为小幅降价冒封装失效和整柜停机风险。
5. **产能地缘集中**：TSMC/ASE/Unimicron/Kinsus/Nan Ya 在台湾，日本材料和 Ibiden/Shinko/TOPPAN/Kyocera 重要，韩国/越南/马来西亚/美国扩产仍需爬坡。

### 3.3 2026 最可能的技术路径

| 路径 | 2026 成熟度 | 放量时间 | 结论 |
|---|---|---|---|
| 高层数大面积 ABF/FC-BGA | 已成熟但供不应求 | 2026 全年 | 绝对主线，所有高端 GPU/ASIC/CPU/switch 都绕不开。 |
| CoWoS-S 硅中介层 | 已成熟 | 2026 全年 | 高端 AI 仍是核心方案，但被面积/成本/产能约束。 |
| CoWoS-L/RDL interposer + local silicon bridge | 已进入主力导入 | 2026 H2 加速 | 2026 最重要的“新技术放量”之一。 |
| CoWoS-R/organic RDL interposer | 成熟度提升 | 2026 H2 至 2027 | 成本和 CTE 优势明显，适合 ASIC/switch/部分大封装。 |
| EMIB/EMIB-T | Intel 生态成熟，外部客户导入早期 | 2026 NPI，2027 小批量到中批量 | CoWoS 替代/补充，不会 2026 大规模替代 CoWoS。 |
| SoIC/Foveros Direct/hybrid bonding | 局部成熟 | 2026 选择性使用，2027 扩大 | 先在 base die、3.5D、高端 CPU/GPU chiplet 中扩张。 |
| Glass/ceramic core substrate | 展示/认证 | 2027 pilot，2028+ 批量 | 不是 2026 主线，但估值期权很大。 |
| CoPoS/Panel-level 2.5D | 研发/试验线 | 2028-2029 基准放量，极超情景 2027 H2 早期 | 解决 wafer-level 面积浪费，短期仍受设备生态限制。 |

## 4. 已放量关键产品：市场规模、渗透率、利润率

以下为全球 AI/HPC 相关收入池估算，不等同于公司公开营收，且高端 GPU/ASIC 内部转移价可能被低估。未来 3 个月按 2026Q2-Q3 可确认或可交付收入推算，1 年按 2026-05 至 2027-05，2 年按 2026-05 至 2028-05。

| 已放量产品 | 2026 事实基础 | 未来3个月市场规模 B/O/X | 未来1年市场规模 B/O/X | 未来2年市场规模 B/O/X | 渗透率路径 | 增长预测 | 毛利率/利润率假设 B/O/X |
|---|---|---:|---:|---:|---|---|---|
| AI GPU/ASIC 高端 ABF/FC-BGA 基板 | Ibiden、Unimicron、SEMCO、Shinko、AT&S 等满载或高稼动；AI server 基板面积和层数上升。 | $1.2-1.8B / $1.7-2.5B / $2.4-3.5B | $5.5-8.0B / $8-12B / $12-18B | $9-14B / $14-22B / $22-34B | 高端 AI xPU attach rate 接近 95-100%；高阶 ABF 在整体 IC substrate 中占比由 2026 约 35-45% 升至 2028 50-65%。 | 2026 +25-60%，2027 +35-80%。 | 22-32% / 30-42% / 40-55%；极超情景来自涨价、客户预付款、良率领先。 |
| AI CPU/switch/network ASIC FC-BGA | AI Ethernet/InfiniBand、switch ASIC、CPU 与 ASIC 同步升级；SEMCO Q1 提到 AI datacenter networking substrates。 | $0.8-1.3B / $1.2-1.9B / $1.8-2.8B | $3.8-6.0B / $6-9B / $9-13B | $6-10B / $10-16B / $16-25B | AI network/switch 封装中高阶 FC-BGA 渗透率 2026 50-65%，2028 70-85%。 | 2026 +20-45%，2027 +35-65%。 | 18-28% / 25-35% / 35-45%。 |
| CoWoS-S 硅中介层/硅 interposer | TSMC 主导高端 GPU/HBM；硅中介层仍是最高密度方案。 | $1.5-2.5B / $2.2-3.5B / $3.5-5.5B | $7-11B / $11-17B / $17-26B | $12-20B / $20-32B / $32-50B | 在 2.5D AI 加速器封装中占比 2026 45-55%，2028 35-45%，份额被 RDL/bridge 分流但绝对金额上升。 | 2026 +40-80%，2027 +45-75%。 | 45-60% / 55-65% / 60-70%；TSMC 型产能稀缺毛利最高。 |
| RDL interposer/CoWoS-R/CoWoS-L RDL 层 | TSMC 官方 CoWoS-R/L 已明确 RDL interposer 和 LSI；Blackwell/Rubin 需要更大封装。 | $0.8-1.6B / $1.5-2.5B / $2.5-4.0B | $4-7B / $7-12B / $12-20B | $9-16B / $16-28B / $28-45B | 在 2.5D 封装中渗透 2026 25-40%，2028 45-65%。 | 2026 +60-120%，2027 +70-130%。 | 35-50% / 45-60% / 55-70%；高端 RDL 制程和良率定价强。 |
| 2.5D/CoWoS-like 封装服务 | TSMC、ASE/SPIL、Amkor、Samsung、Intel 争夺 AI/HPC 封装。 | $6-10B / $9-14B / $14-20B | $28-45B / $42-65B / $65-95B | $50-80B / $80-125B / $125-190B | 高端 AI 加速器 2.5D/3D attach rate 2026 70-85%，2028 85-95%。 | 2026 +45-90%，2027 +50-90%。 | TSMC/IDM 45-65%，OSAT 25-45%，极超可达 50%+。 |
| Fan-out/RDL on substrate：InFO-oS、FOCoS、SWIFT/SLIM、XDFOI | switch/network ASIC、部分 chiplet ASIC 用 RDL 降成本。 | $0.4-0.8B / $0.7-1.2B / $1.1-1.8B | $2-4B / $3.5-6.5B / $6-10B | $5-9B / $8-15B / $15-28B | AI ASIC/switch 中 2026 10-20%，2028 25-40%。 | 2026 +25-70%，2027 +50-100%。 | 25-38% / 35-48% / 45-60%。 |
| HBM/CoWoS assembly 相关 C4 bump、underfill、microbump、test socket | HBM KGD、interposer、package test 成为有效产出瓶颈。 | $0.7-1.2B / $1.1-1.8B / $1.8-2.8B | $3.5-6B / $5.5-9B / $9-14B | $7-12B / $11-20B / $20-32B | HBM attach 高端 AI 几乎 100%；HBM4 切换带来单位价值提升。 | 2026 +40-80%，2027 +50-100%。 | 材料 25-45%，设备/测试耗材 35-60%，稀缺 socket/probe 可更高。 |

## 5. 在研/早期导入产品：成熟时间、放量时间与收入区间

| 在研/早期技术 | 当前阶段 | 基准成熟/放量 | 乐观成熟/放量 | 极超成熟/放量 | 未来3个月市场规模 B/O/X | 未来1年市场规模 B/O/X | 未来2年市场规模 B/O/X | 毛利率/利润率假设 |
|---|---|---|---|---|---:|---:|---:|---|
| EMIB-T / bridge-in-substrate | Intel 官方路线，HBM4/UCIe/垂直供电；封装服务客户导入中。 | 2026 NPI，2027 小批量，2028 规模化 | 2027 进入 CSP ASIC 10%+ 封装份额 | 2026 H2 获关键客户量产订单，2027 占高端 ASIC 20%+ | $0.1-0.3B / $0.2-0.6B / $0.5-1.0B | $0.8-2.5B / $2-5B / $5-10B | $5-12B / $12-25B / $25-45B | 40-60%，若封装产能替代 CoWoS 可有更高溢价。 |
| SoIC/Foveros Direct/hybrid bonding | MI300/Intel/Foveros 等已验证，HBM/base die 和 3.5D 需求上升。 | 2026 选择性使用，2027 扩大 | 2027 成为 Rubin/MI400/TPU8 的关键增量 | 2027 前半即被多家 ASIC 采用 | $0.3-0.7B / $0.6-1.2B / $1-2B | $2-4B / $4-8B / $8-15B | $6-12B / $12-25B / $25-45B | 45-65%，设备/良率壁垒极高。 |
| Glass core substrate | Intel/TOPPAN/Samsung/SKC Absolics 等推进，仍非主流量产。 | 2027 pilot，2028+ 批量 | 2027 H2 高端 ASIC 小量 | 2027 在 CSP ASIC 或 switch ASIC 中提前设计进入 | <$0.1B / $0.1-0.2B / $0.2-0.4B | $0.1-0.5B / $0.3-1B / $1-2B | $1-3B / $3-8B / $8-18B | 35-70%，早期良率风险大，成功者毛利高。 |
| Ceramic core substrate | Kyocera 2026 ECTC 展示，解决大封装翘曲和细线化。 | 2027 pilot，2028-2029 量产 | 2027 H2 xPU/switch ASIC 小批量 | 2027 被高可靠 AI switch/defense AI 采用 | <$0.05B / $0.05-0.15B / $0.15-0.3B | $0.1-0.4B / $0.3-0.8B / $0.8-1.5B | $0.8-2B / $2-5B / $5-10B | 40-65%，定制和材料 know-how 定价强。 |
| CoPoS / panel-level 2.5D | 产业试验线阶段，目标降低超大封装的 wafer 面积浪费。 | 2028-2029 放量 | 2028 初小批量 | 2027 H2 工程收入明显 | <$0.05B / $0.05-0.1B / $0.1-0.3B | $0.1-0.5B / $0.5-1.5B / $1.5-3B | $1-4B / $4-10B / $10-25B | 30-60%，取决于 panel 工具生态和良率。 |
| Organic RDL interposer on glass carrier / large-panel RDL | TOPPAN 展示 organic RDL interposer，ASE/Amkor/JCET 等有 fan-out 基础。 | 2026-2027 NPI，2027 下半年加速 | 2027 成为 ASIC/switch 成本优化路径 | 2027 大客户绑定产线 | $0.1-0.3B / $0.2-0.5B / $0.5-0.8B | $0.8-2B / $1.5-4B / $4-7B | $3-7B / $7-14B / $14-25B | 30-55%。 |
| Optical waveguide substrate / CPO substrate | Shinko、TOPPAN 等展示 CPO/optical wiring substrate。 | 2027-2028 随 1.6T/3.2T 和 CPO 上量 | 2027 AI switch 早期 | 2027 数据中心交换芯片大客户拉动 | $0.05-0.2B / $0.1-0.3B / $0.3-0.6B | $0.4-1B / $0.8-2B / $2-4B | $2-5B / $5-12B / $12-25B | 35-60%，可靠性认证决定溢价。 |
| Embedded power substrate：eDTC/eMIM/embedded capacitor/IVR | TSMC CoWoS-L、Intel EMIB-T 均强调电源完整性。 | 2026 高端样品，2027 更广 | 2027 成为 2kW+ 封装标配选项 | 2026 H2 即被 GB300/Rubin/ASIC 设计拉动 | $0.2-0.5B / $0.4-0.8B / $0.8-1.3B | $1-2.5B / $2-5B / $5-9B | $3-7B / $7-15B / $15-30B | 35-65%，靠专利/良率/客户共设产线定价。 |

## 6. 产能结构与供给瓶颈

### 6.1 产能集中

| 环节 | 主要地区 | 主要公司 | 产能/工艺特点 |
|---|---|---|---|
| CoWoS/2.5D foundry packaging | 台湾为核心，美国/日本/韩国补充 | TSMC、Intel、Samsung Foundry | TSMC 3DFabric/CoWoS 主导 GPU/HBM；Intel EMIB/Foveros 有差异化；Samsung I-Cube/H-Cube/R-Cube 追赶。 |
| OSAT advanced packaging | 台湾、中国大陆、韩国、马来西亚、美国 | ASE/SPIL、Amkor、JCET、Tongfu、PTI、Samsung、Intel ASAT | 承接 CoWoS-like、fan-out、RDL、test/burn-in 外溢；关键在客户认证和良率。 |
| 高端 ABF/FC-BGA | 日本、台湾、韩国、马来西亚、奥地利、中国大陆 | Ibiden、Shinko、Unimicron、Kinsus、Nan Ya PCB、Samsung Electro-Mechanics、AT&S、Kyocera、TOPPAN、Daeduck、LG Innotek、Shennan Circuits | AI server 基板面积大、层数高、材料低损耗，头部集中，产能爬坡慢。 |
| RDL/fan-out/organic interposer | 台湾、日本、韩国、中国大陆、美国 | TSMC、ASE、Amkor、Samsung、JCET、Nepes、Powertech、TOPPAN、Intel | RDL 由手机 fan-out 向 AI/HPC 大封装升级，面临 panel/wafer 工艺兼容问题。 |
| 材料 | 日本最强，台湾/韩国/美国/欧洲补充 | Ajinomoto、Resonac、Sumitomo Bakelite、Mitsubishi Gas Chemical、Namics、Shin-Etsu、JSR/TOK、DuPont、Nittobo、Nan Ya、Taiwan Glass、AGC、Corning、Schott、SKC Absolics | ABF film、低 CTE 玻纤布、低损耗树脂、underfill、photoresist、玻璃 core 决定上限。 |
| 设备/检测 | 日本、欧洲、美国、新加坡/中国台湾 | ASMPT、BESI、Kulicke & Soffa、Applied Materials、Lam、TEL、KLA、Onto、Camtek、Nova、SUSS MicroTec、EVG、DISCO、Accretech、SCREEN、Ushio | TCB、hybrid bonding、RDL litho/plating、laser drilling、metrology、SLT 是隐性瓶颈。 |

### 6.2 至少 10 条供给瓶颈

1. **低 CTE 玻纤布/T-glass**：高层数 ABF 要控制翘曲和介电损耗，玻纤布无法快速扩产。
2. **ABF film 和低损耗树脂**：Ajinomoto 等材料供应集中，AI 客户优先级提高后非 AI 客户被挤出。
3. **SAP 制程设备**：desmear、化学铜、图形电镀、fine line 检测、洁净搬运交期长。
4. **大面积基板良率**：面积越大，单颗缺陷概率越高，多次层压使 scrap cost 放大。
5. **RDL 光刻/电镀/聚合物一致性**：2um-4um 级 RDL 对厚度、应力、平坦度、铜粗糙度要求更高。
6. **TCB/hybrid bonding throughput**：HBM stack、chiplet、bridge 越多，bonding 和检测时间越长。
7. **HBM known-good-die 和封装联动**：HBM 良率/测试与中介层/封装有效产出绑定，任何一个差都会拖低总产出。
8. **客户认证周期**：新基板、新材料、新 OSAT 通常需要 9-18 个月，且 AI 芯片客户不愿在一代产品中频繁切换。
9. **可靠性验证**：温循、翘曲、C4 joint fatigue、underfill void、电迁移和高速 SI/PI 需要长周期。
10. **人才和工艺 know-how**：先进封装不是简单买设备，良率靠制程窗口、化学品、清洁度和在线量测经验。
11. **物流和交付**：高价值大尺寸基板/中介层需要防潮、防颗粒、防翘曲运输，交付事故代价高。
12. **地缘与客户分配**：美国/日本/韩国/台湾产能再平衡会带来重复认证和区域成本上升。

## 7. 成本构成、毛利决定因素与价格传导

### 7.1 高端 ABF/FC-BGA 单位成本拆分

| 成本项 | 占比区间 | 说明 |
|---|---:|---|
| 材料：ABF film、玻纤布、树脂、铜箔、solder mask、贵金属 | 35-45% | AI 用低损耗材料和 T-glass 价格传导能力最强。 |
| SAP/层压/laser via/desmear/plating 制程 | 25-35% | 大面积高层数导致循环次数上升，设备 amortization 高。 |
| 报废与良率损失 | 10-20% | 大尺寸产品良率差一点，单位成本就显著上升。 |
| 折旧 | 10-18% | 新产线 capex 高，早期稼动和良率决定利润释放。 |
| 检测/可靠性/客户工程 | 5-10% | AI 客户要求更严，NPI 工程资源稀缺。 |
| 人工/能源/厂务 | 5-8% | 高洁净度和稳定厂务水电气是必要条件。 |

### 7.2 中介层/RDL/2.5D 封装成本拆分

| 成本项 | 占比区间 | 说明 |
|---|---:|---|
| 硅 wafer/玻璃/有机 carrier 或 interposer 基材 | 20-40% | 硅中介层成本高但密度高；RDL/organic 目标是降本和放大面积。 |
| RDL/TSV/litho/plating/polymer | 20-35% | 线宽线距、层数、铜厚和应力控制决定良率。 |
| bonding/assembly/underfill/molding | 15-25% | HBM/chiplet 数越多，设备时间越值钱。 |
| test/metrology/burn-in | 8-15% | 高端封装测试越来越像系统测试，ATE/SLT 价值上升。 |
| yield reserve/scrap | 10-25% | 价值几万美元的封装任何失效率都很贵。 |

### 7.3 毛利决定因素

1. **尺寸和层数**：基板面积、层数、RDL 层数越高，头部供应商越能定价。
2. **客户绑定**：进入 NVIDIA/AMD/Broadcom/Google/AWS/Microsoft/Meta/TSMC/Intel 供应链后，生命周期和切换成本高。
3. **材料转嫁能力**：玻纤布、铜箔、贵金属、树脂涨价能否用季度或项目制价格传导。
4. **良率曲线**：新线 early ramp 毛利可能低，成熟后可快速扩张。
5. **产能预订**：LTA、预付款、共同投资设备会降低供应商周期风险。
6. **工艺独占性**：CoWoS-L、EMIB-T、Foveros Direct、玻璃/陶瓷 core 这类平台如果绑定客户，毛利可显著高于普通基板。

## 8. 竞争格局、壁垒与价值捕获

### 8.1 市场结构

| 细分 | 头部集中度判断 | 原因 |
|---|---|---|
| AI 高端 CoWoS/2.5D foundry packaging | TSMC 显著领先，CR1 估计 70%+，高端 GPU 更高。 | NVIDIA/AMD/Broadcom/Google/ASIC 生态深度绑定，3DFabric/CoWoS 良率和产能领先。 |
| AI server ABF/FC-BGA | 头部集中，Ibiden/Shinko/Unimicron/SEMCO/AT&S/Kinsus/Nan Ya/Kyocera/TOPPAN 形成核心供应圈；Ibiden 在部分 AI server substrate 自估 70-80%。 | 大尺寸、多层数、材料、客户认证难，扩产 18-30 个月。 |
| RDL/fan-out on substrate | TSMC、ASE、Amkor、Samsung、JCET、Nepes 等分散度高于 CoWoS。 | 手机 fan-out 历史产能可迁移，但 AI 大封装良率门槛提高。 |
| EMIB/Foveros/3D | Intel 自成体系，Samsung/TSMC/ASE 追赶。 | 工艺路线、EDA/IP、客户生态决定份额，短期不是完全开放商品市场。 |
| 玻璃/陶瓷 core | 早期分散，Intel、TOPPAN、Samsung、SKC Absolics、Kyocera、Corning/AGC/Schott 等卡位。 | 未量产前不看份额，看谁先过客户可靠性和工具链。 |

### 8.2 壁垒清单：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| 技术壁垒 | 大面积封装的 warpage、SI/PI、C4 fatigue、HBM landing、RDL 应力不是靠低价能解决，客户会买确定性。 |
| 规模壁垒 | 一条高端 ABF 或 advanced packaging 线投资大、爬坡慢，短期没有弹性供给。 |
| 客户锁定 | 供应商从设计阶段进入 stack-up、材料、仿真、可靠性验证，一旦量产切换会影响整代芯片。 |
| 认证标准 | AI 客户的温循、老化、power cycling、system-level test 标准严，认证失败会错过整代窗口。 |
| 切换成本 | 每代 AI 芯片 NPI 时间很短，客户宁愿支付溢价，也不愿冒封装失效造成数十亿美元整柜交付延误。 |
| 良率数据 | 头部厂商拥有历史 defect map、材料批次、设备参数和客户失效数据库，后来者难以复制。 |
| 产能金融化 | 预付款和 LTA 把产能变成战略资产，现货低价竞争意义下降。 |

### 8.3 价值捕获判断

长期高 ROIC/高毛利最可能在四层：

1. **TSMC/Intel/Samsung 等平台型先进封装**：客户把设计、EDA、封装、测试和产能一起绑定，议价权最强。
2. **高端 AI ABF 龙头**：Ibiden、Unimicron、Shinko、SEMCO、AT&S 等只要保持良率和客户绑定，2026-2027 可享受量价齐升。
3. **关键材料**：ABF film、低 CTE 玻纤布、低损耗树脂、underfill、临时键合材料、玻璃/陶瓷 core。材料单价不一定最大，但断供会卡整条线。
4. **先进封装设备和检测**：TCB、hybrid bonding、RDL metrology、probe card、SLT、burn-in。客户扩产越快，设备越先受益。

低 ROIC 风险较高的是通用 BT、普通 PCB、非 AI 低阶封测和没有客户预订的新建产能。

## 9. 2026 关键变化：3 个拐点

1. **GB300/B300 把 CoWoS-L/RDL 和高端 ABF 拉成 2026 主线**  
   Blackwell Ultra 是 2026 真正可见的量。Rubin 虽有发布和 H2 可用口径，但 2026 大额收入仍主要来自 GB300/B300、GB200/B200 和 Ironwood/Trainium2/3 等成熟平台。

2. **CSP ASIC 从补充产能变成单独产能池**  
   Google TPU、AWS Trainium、Meta MTIA、Microsoft Maia、OpenAI/Broadcom 和 Broadcom/Marvell 其他 XPU 共同争夺 2.5D、ABF、RDL 和 HBM，封装供应商的客户结构更分散。

3. **ABF 价格/产能重新进入卖方市场**  
   2023-2024 的消费电子去库存后，高端 ABF 由 AI/HPC 驱动反转。2026 年涨价能否持续取决于材料和良率，不再是简单的产能过剩/不足周期。

## 10. 2027 关键变化：3 个拐点

1. **HBM4 + Rubin/MI400/TPU8 放大 interposer 和 RDL 价值**  
   12 HBM stack、更多 chiplet、更大 reticle-size 封装将使 RDL interposer、CoWoS-L、EMIB-T、hybrid bonding 的边际价值上升。

2. **先进封装产能外溢制度化**  
   TSMC 继续主导，但 ASE/SPIL、Amkor、Samsung、Intel、AT&S/TOPPAN 等承担更多客户验证和第二来源，先进封装供应链从单点瓶颈走向多点瓶颈。

3. **玻璃/陶瓷/面板级路线从展示进入客户认证**  
   2027 不是大规模收入年，但可能是设计胜出年。拿到 GPU/ASIC/switch 的 early design-in 的公司，会在 2028-2029 获得高弹性。

## 11. 头部公司与细分公司清单

### 11.1 Foundry/先进封装平台

| 领域 | 公司 |
|---|---|
| CoWoS/SoIC/InFO/3DFabric | TSMC、GUC、Alchip、ASE/SPIL、Amkor |
| EMIB/Foveros/ASAT | Intel Foundry、Intel New Mexico/Oregon/Malaysia packaging 生态 |
| I-Cube/H-Cube/R-Cube/Foundry packaging | Samsung Foundry、Samsung Electro-Mechanics、Samsung memory/HBM ecosystem |
| OSAT advanced packaging | ASE Technology、SPIL、Amkor、JCET、Tongfu Microelectronics、Powertech/PTI、Nepes、UTAC、KYEC、ChipMOS、Huatian、SJ Semi |

### 11.2 ABF/FC-BGA/BT/高端基板

| 区域 | 公司 |
|---|---|
| 日本 | Ibiden、Shinko Electric、Kyocera、TOPPAN、Meiko、Daisho Denshi、DNP/TOPPAN 相关电子材料与基板生态 |
| 台湾 | Unimicron、Kinsus、Nan Ya PCB、Compeq、Wus Printed Circuit、Tripod、Zhen Ding、Gold Circuit、Taiwan PCB Techvest |
| 韩国 | Samsung Electro-Mechanics、Daeduck Electronics、LG Innotek、Simmtech、Korea Circuit |
| 欧洲/东南亚 | AT&S Austria/Malaysia/China、Schweizer、ICAPE 相关供应链 |
| 中国大陆 | Shennan Circuits、Fastprint、Zhuhai Access、SCC、Wus China、Victory Giant、Avary/Zhen Ding China、Kinwong、Founder PCB、Suntak、AKM Meadville、Xingsen、Aoshikang |

### 11.3 RDL/fan-out/interposer/PLP

| 技术 | 公司 |
|---|---|
| RDL interposer/CoWoS-R/L/InFO-oS | TSMC、ASE、Amkor、Samsung、TOPPAN、Intel、JCET、Nepes |
| Fan-out on substrate/FOCoS/SWIFT/SLIM/XDFOI | ASE、Amkor、JCET、Samsung、TSMC、Tongfu、Nepes、Deca Technologies |
| Silicon interposer/TSV | TSMC、Samsung、Intel、ASE、Amkor、UMC ecosystem、X-FAB/Tezzaron 等特殊工艺厂 |
| Panel-level packaging/large-panel RDL | Samsung、Intel、TOPPAN、ASE、Amkor、Nepes、Powertech、JCET、SUSS/EVG/SCREEN equipment ecosystem |
| Optical waveguide/CPO substrate | Shinko、TOPPAN、Intel、Broadcom silicon photonics ecosystem、Coherent/Lumentum 光器件生态、Ayar Labs/Lightmatter 等 optical I/O 生态 |

### 11.4 材料

| 材料 | 公司 |
|---|---|
| ABF film/build-up film | Ajinomoto、Resonac、Sekisui、Mitsubishi Chemical Group |
| BT resin/低损耗树脂/CCL | Mitsubishi Gas Chemical、Panasonic Industry、Resonac、Sumitomo Bakelite、Taiwan Union Technology、Elite Material、Nan Ya Plastics、Rogers、Isola、Doosan |
| 玻纤布/T-glass/低 CTE cloth | Nittobo、Nan Ya Plastics、Taiwan Glass、Asahi Kasei、AGY、Kingboard Fiberglass |
| 铜箔/表面处理 | Mitsui Mining & Smelting、JX Advanced Metals、Furukawa Electric、Chang Chun、Co-Tech、LCY、NPC |
| Underfill/molding/封装胶 | Namics、Resonac、Henkel、Panasonic、Shin-Etsu、Sumitomo Bakelite、Nagase、Hitachi Chemical legacy |
| Photoresist/RDL chemicals | JSR、TOK、Shin-Etsu、DuPont、Merck/EMD、Brewer Science、MacDermid Alpha、Atotech/MKS |
| Glass/ceramic core | Corning、AGC、Schott、SKC Absolics、Intel glass ecosystem、TOPPAN、Kyocera、NGK、CoorsTek |

### 11.5 设备、测试与 EDA

| 环节 | 公司 |
|---|---|
| TCB/hybrid bonding/die attach | ASMPT、BESI、Kulicke & Soffa、Shibaura、Panasonic Connect |
| RDL/TSV/电镀/沉积/刻蚀 | Applied Materials、Lam Research、Tokyo Electron、ASM、SCREEN、Ulvac、EV Group、SUSS MicroTec、ACM Research |
| Laser drilling/切割/减薄 | DISCO、Accretech、EO Technics、Han's Laser、LPKF、MKS/ESI |
| AOI/metrology/inspection | KLA、Onto Innovation、Camtek、Nova、Lasertec、Ushio、Orbotech/KLA、CyberOptics/Nordson |
| Probe/test/burn-in/SLT | Advantest、Teradyne、FormFactor、Technoprobe、MPI、Chroma、Cohu、Hon Precision、KYEC |
| EDA/3DIC/package co-design | Cadence、Synopsys、Siemens EDA、Ansys、Keysight、ANSYS/Apache、GUC、Alchip、Broadcom/Marvell custom ASIC teams |

## 12. 情景模型汇总

### 12.1 本行业核心收入池

| 收入池 | 2026 基准 | 2026 乐观 | 2026 极超 | 2027 基准 | 2027 乐观 | 2027 极超 |
|---|---:|---:|---:|---:|---:|---:|
| AI/HPC 高端 ABF/FC-BGA | $6-9B | $9-13B | $13-20B | $9-14B | $14-22B | $22-34B |
| 中介层：硅 + RDL + bridge | $10-18B | $16-28B | $28-45B | $18-32B | $32-55B | $55-90B |
| 2.5D/3D 封装服务 | $28-45B | $42-65B | $65-95B | $50-80B | $80-125B | $125-190B |
| RDL/fan-out/organic interposer | $3-6B | $5-10B | $10-18B | $7-14B | $14-28B | $28-50B |
| 设备/材料/测试相关增量 | $12-22B | $20-35B | $35-55B | $20-38B | $38-70B | $70-120B |

### 12.2 关键假设

| 变量 | 基准 | 乐观 | 极度超预期 |
|---|---|---|---|
| AI 需求 | 2026 GB300/ASIC 稳定，Rubin 2027 放量 | Blackwell Ultra 与 ASIC 同时满载，Rubin 2026 H2 较顺 | 2027 需求被提前到 2026 H2，客户愿意用高价锁封装产能 |
| HBM/CoWoS | 仍紧，但逐季改善 | HBM4 验证顺利，CoWoS-L/RDL 外包加速 | HBM4、CoWoS、ABF 同步高良率爬坡 |
| ABF | 高端满载，普通基板分化 | 高端涨价传导，客户预付款扩产 | 高端 ABF 进入 2027 年前即售罄，现货溢价扩大 |
| RDL/EMIB | RDL interposer 渗透上升，EMIB 小量 | EMIB-T 获关键 ASIC 客户 | EMIB-T/RDL bridge 2027 前成为 CoWoS 替代核心 |
| 新技术 | 玻璃/陶瓷/CoPoS 以展示和认证为主 | 2027 小批量收入 | 2027 H2 进入头部 ASIC 设计，市场提前定价 |

## 13. 投资观察清单

| 优先级 | 子方向 | 看多理由 | 主要风险 |
|---:|---|---|---|
| 1 | 高端 ABF/FC-BGA 龙头 | 2026 已放量、客户锁产能、基板面积和层数提升直接涨 ASP。 | 2027 新产能过快释放、良率不及预期、材料涨价吞噬毛利。 |
| 2 | TSMC CoWoS/RDL/SoIC 生态 | 供给瓶颈最硬，平台议价权最强。 | 单一公司估值高、地缘风险、客户议价。 |
| 3 | RDL interposer/CoWoS-L/organic RDL | 从可选成本优化变成大封装必要技术。 | 良率、可靠性、与硅中介层的边界变化。 |
| 4 | 先进封装设备和检测 | 扩产先买设备，AI 封装测试复杂度提高。 | 客户 capex 节奏波动、设备验收延迟。 |
| 5 | 低 CTE 玻纤布/ABF/树脂/underfill | 小材料卡大出货，价格传导能力强。 | 扩产后价格回落、客户多源认证。 |
| 6 | EMIB-T/玻璃/陶瓷 core | 2027-2028 可能替代部分 CoWoS 和有机基板。 | 2026 收入很小，商业化时间可能晚于预期。 |

## 14. 主要来源

| 类别 | 来源 |
|---|---|
| TSMC 技术 | [TSMC CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm), [TSMC 3DFabric for HPC](https://www.tsmc.com/schinese/dedicatedFoundry/technology/platform_HPC_tech_WLSI) |
| TSMC 财务 | [TSMC 2026 Q1 Quarterly Results](https://investor.tsmc.com/english/quarterly-results/2026/q1) |
| 产业报告 | [TrendForce 2026 Foundry Growth](https://www.trendforce.com/presscenter/news/20260319-12979.html), [TrendForce advanced packaging report page](https://www.trendforce.com.tw/research/download/RP260428PL), [TechInsights Advanced Packaging Outlook 2026](https://www-prod.techinsights.com/outlook-reports-2026/advanced-packaging-outlook-report) |
| Ibiden | [Ibiden interim financial Q&A FY2026](https://www.ibiden.com/ir/items/en_QY20251st.pdf), [Ibiden FY2025 Q2 presentation](https://www.ibiden.com/ir/items/en_kessannsetsumei2025Q2.pdf), [Ibiden Integrated Report 2025](https://www.ibiden.com/ir/items/IntegratedReport2025_en.pdf) |
| Unimicron | [CNA 2026-02-25](https://www.cna.com.tw/news/afe/202602250198.aspx), [工商时报 2026-02-26](https://www.chinatimes.com/newspapers/20260226000285-260202), [UDN 2026-02-25](https://money.udn.com/money/story/5612/9344020) |
| Samsung Electro-Mechanics | [SEMCO 1Q26 earnings release](https://m.samsungsem.com/resources/file/global/ir/earnings_release/1Q26_Earnings_Release_eng.pdf), [SEMCO FCBGA roadmap 2026](https://sem.samsung.com/global/newsroom/news/view.do?id=8382) |
| Intel | [Intel Foundry AI/HPC](https://www.intel.com/content/www/us/en/foundry/library/ai-hpc.html), [Intel AI/HPC platform brief](https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-11/intel-foundry-hpc-ai-brief.pdf), [Intel glass-core substrate brief](https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2024-08/foundry-glass-core-substrates-pb.pdf), [Foveros Direct 3D brief](https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-11/foveros-direct-3d-tech-brief.pdf) |
| TOPPAN | [TOPPAN Niigata FC-BGA line](https://www.holdings.toppan.com/en/news/2025/12/newsrelease251217_1.html), [TOPPAN SEMICON Japan glass/RDL showcase](https://www.holdings.toppan.com/en/news/2025/12/newsrelease251210_1.html) |
| Kyocera | [Kyocera multilayer ceramic core substrate, 2026-04-27](https://global.kyocera.com/newsroom/news/2026/001185.html) |
| AT&S | [AT&S Kulim high-volume manufacturing](https://ats.net/en/press/ats-starts-high-volume-manufacturing-at-new-plant-in-kulim-malaysia/) |
| Shinko/TOPPAN products | [Shinko semiconductor package products](https://www.shinko.co.jp/english/product/package/), [Shinko optical waveguide substrate](https://www.shinko.co.jp/english/product/under-development/ows/), [TOPPAN FC-BGA product](https://www.toppan.com/en/electronics/package/fc-bga/) |

## 15. 风险提示

1. AI 资本开支兑现不及预期，客户开始按 token ROI 压缩 2027 订单。
2. HBM4、CoWoS-L、RDL interposer、玻璃/陶瓷 core 良率低于预期，技术放量延迟。
3. 2026 高端 ABF 涨价后，2027 新产能释放导致价格回落。
4. 地缘政治、出口管制、台湾风险、美国/中国/日本/韩国补贴政策变化影响供应链布局。
5. 本文对自用 ASIC 和内部转移价做了大胆乐观估算，不能与公开公司营收简单相加。

# 行业调研：【服务器BMC、MCU与嵌入式控制】

> 截至日期：2026-05-08  
> 研究范围：服务器 BMC SoC、BMC SiP/DC-SCM、安全 RoT/PFR/TPM、OpenBMC/商用 BMC 固件、GPU/ASIC 加速卡管理控制器 AMC、rack manager、PSU/BBU/BMIC/数字电源 MCU、风扇/泵阀/漏液检测 MCU、液冷/电力/机柜控制接口。  
> 口径说明：本文把“市场规模”限定为控制面半导体、控制板、固件、软件授权、认证/安全服务和 rack 级管理控制组件的供应商收入，不把 GPU、CPU、HBM、整机服务器、全站 UPS、CDU、冷板、PDU 等大件全额计入。美元为名义值，`B`=十亿美元。本文按用户要求对 2026-2027 AI 计算中心建设采取非常乐观的需求假设；直接数据不可得处会明确标为模型假设。

## 0. 结论先行

**核心判断：2026 年服务器 BMC/MCU/嵌入式控制的投资逻辑从“传统服务器随附芯片”升级为“AI rack control plane”。** 传统服务器是一块主板一颗 BMC；GB200/GB300、Trainium、TPU、MTIA、Maia、MI400 这类 rack-scale 系统把 GPU tray、switch tray、power shelf、cooling loop、BBU、accelerator baseboard、fabric 与安全 RoT 都纳入远程管理，管理节点数量出现乘数效应。

最重要的量化锚点：

- ASPEED 在 2025 年 11 月投资者材料中把 2030 年 BMC TAM 上调到超过 4,650 万颗，并给出 AI server BMC 占比从 2024 年 12.0%、2025 年 20.0%、2026 年 30.2%、2027 年 36.6%、2028 年 42.6% 继续上升；若按其增长假设倒推，2026 BMC 单位 TAM 约 2,560 万颗、2027 约 2,960 万颗。
- 2026 年 5 月台湾媒体转述法人估算称，ASPEED 又把 2030 年 BMC TAM 从 4,650 万颗上修到 6,577 万颗；市场同时估算 GB200 平台约 89 颗 BMC、GB300 NVL72 约 71 颗 BMC、定制 AI ASIC 服务器约 22 颗 BMC，且 AST2700 导入可带动 ASP 提高约 40%-50%。
- Nuvoton 2026Q1 投资者材料直接写出：AI rack 中 BMC 数量预计从 80 颗增加到 120 颗；144 GPU 到 576 GPU 的扩展会带来 2-3 倍 tray 数量；rack power 从 2024 年 120kW 走向 2028 年 1,000kW，推动高性能 MCU、BMIC、风扇/液冷控制器需求。
- TrendForce 经 The Register 转述称，2026 服务器出货增长预期从 20% 下修到 13%，原因包括 PMIC 与 BMC 交期拉长；BMC 对非 AI 客户交期可拉到 21-26 周。这说明 BMC/控制芯片已经从小配件变成交付瓶颈。
- ASPEED 2024 年营收 NT$6.428B、毛利率 64.41%、营益率 45.56%；2026Q1 公司指引营收 NT$2.60-2.70B、毛利率 66.5%-67.5%。BMC SoC 是少数具备“高集中度 + 高毛利 + 供不应求 + 代际 ASP 提升”的 AI 基建小芯片环节。

**本文的总量模型：** 未来 12 个月，全球 AI 数据中心相关 BMC/MCU/嵌入式控制收入池约 $4.0-7.8B（基准）、$6.8-12.5B（乐观）、$12-22B（极度超预期乐观）。到未来 24 个月，收入池约 $7.5-14B / $13-26B / $25-45B。这里的极度乐观情景本质是假设 GB300/Rubin/Trainium/TPU/MTIA/MI400 的 rack 交付与电力上架没有明显断档，且客户开始把 RoT/PQC、rack manager、BBU、液冷控制和电源控制当成强制配置。

**2026 最可能放量的技术路径：**

1. `AST2600/AST2700 + Nuvoton NPCM7/8 + OpenBMC/MegaRAC` 继续主导 host BMC 与 tray BMC。
2. `Redfish + MCTP + PLDM + SPDM` 成为 accelerator、NIC、switch、power/cooling 的共同管理接口。
3. `OCP DC-SCM 2.0/LTPI + Caliptra/PFR + OCP S.A.F.E./S.O.L.I.D.` 从加分项变成 hyperscaler RFP 的准入条件。
4. `power shelf/BBU/BMIC/数字电源 MCU + 液冷泵阀/漏液控制 MCU` 跟随 48V/54V ORv3/MGX 机柜放量。
5. `accelerator AMC/UBB BMC + rack manager` 变成 AI 整柜的新增价值层，尤其是 GB300、Rubin、MI400、MTIA、多芯片 ASIC 与私有 rack。

## 1. 2026 AI 计算中心建设中的机会、挑战与技术路线

### 1.1 为什么 BMC/MCU 在 AI rack 中突然重要

BMC 过去负责远程开关机、传感器、风扇、SEL 日志、KVM、BIOS/固件更新等“低速运维”。AI rack 把它推到新的位置：

- 单 rack 价值从传统数万美元升到 $3M-$9M，任何 firmware、液冷、供电或 GPU tray 故障都会造成巨大停机损失，客户愿意为可观测性和确定交付付费。
- GPU/ASIC、NVSwitch、retimer、NIC/DPU、power shelf、BBU、风扇、泵、阀、漏液传感器都需要 sideband telemetry，BMC/MCU 从主板扩展到整柜。
- 推理集群对 uptime、power capping、thermal loop、firmware rolling update、security attestation 的要求高于训练试验集群。
- 大客户倾向减少黑盒私有接口，OCP/DMTF/OpenBMC/Redfish 的价值提高，但真正能赚钱的是通过 NVIDIA、Meta、Google、AWS、Microsoft、Dell/HPE/SMCI/ODM 认证的实现。

### 1.2 机会与挑战

| 维度 | 2026 机会 | 2026 挑战 |
|---|---|---|
| 需求乘数 | AI rack 从 host board 扩展到 GPU tray、switch tray、power、cooling、BBU，BMC/MCU 数量按 rack 复杂度增长 | GPU/HBM/电力若延迟，BMC 订单也会滞后；客户可能先锁货、后上架 |
| 代际 ASP | AST2700、Nuvoton Arbel、Axiado TCU、BMC SiP、PQC RoT 提升单价 | 传统 AST2600/NPCM7xx 会有价格锚；低端通用服务器仍价格敏感 |
| 供给 | BMC lead time 拉长，认证供应商具备溢价 | 12nm/28nm/40nm/55nm 与 8-inch 模拟/PMIC 产能不一定同步扩张 |
| 软件 | OpenBMC 与 MegaRAC OneTree 把多硅平台统一到一个代码库，降低客户验证成本 | BMC 固件团队、Yocto/OpenEmbedded、Redfish schema、PLDM/MCTP/SPDM 工程人才稀缺 |
| 安全 | CRA、CNSA 2.0、OCP S.A.F.E./S.O.L.I.D.、PQC、Caliptra 推动 attach rate | FIPS/OCP/客户审计周期长；密钥注入、供应链追溯、固件签名流程复杂 |
| 电源/液冷 | 48V/54V power shelf、BBU、leak detection、pump/fan control 放量 | 800VDC 安全、拉弧、保护、UL/IEC/NEC 认证会拖慢 2027 前量产 |

### 1.3 当前正在使用的关键技术

| 技术 | 当前状态 | 2026 判断 |
|---|---|---|
| ASPEED AST2600/AST2700 | AST2600 成熟；AST2700 为 12nm、4x Cortex-A35、2x Cortex-M4、PCIe Gen4、DDR5、USB3.2、UFS、CAN、LTPI、Caliptra | AST2700 是 2026 高端 AI server/rack 主线，ASP 与毛利上修 |
| Nuvoton NPCM7xx/NPCM8mnx Arbel | NPCM7xx 覆盖企业/超大规模；NPCM8mnx 为 4x A35、TIP security enclave、OpenBMC；2025 推 SiP | Arbel SiP 把 BMC、DDR4、eMMC、NOR、PMIC、被动件封成 23x23mm，适合 accelerator card/multi-node |
| OpenBMC | Linux Foundation 开源 BMC 栈，hyperscaler 广泛使用 | 从“客户自维护”走向 AMI/Insyde/Phoenix/OEM hardened distribution |
| AMI MegaRAC SP-X / OneTree | SP-X 成熟；OneTree 3.0 2026 支持 AST2700、NVIDIA GB300、早期 Vera Rubin、Blackwell/Rubin GPU | 商用固件是高毛利层；客户为测试覆盖、OCP SAFE、长期维护付费 |
| Redfish | DMTF 主流 out-of-band API；2025.3/2025.4 持续增强 | ComponentIntegrity、PowerDistribution、Telemetry、Firmware Update 成为 AI rack 关键 schema |
| MCTP/PLDM | BMC 与 GPU/NIC/retimer/SSD/power 子设备的 sideband 管理协议 | PLDM Type 2 sensor/control、Type 5 firmware update 在 UBB/accelerator 中普及 |
| SPDM | 设备身份、测量、密钥交换、attestation | 与 Redfish ComponentIntegrity、NVIDIA GB200 switch attestation、OCP accelerator 管理绑定 |
| OCP DC-SCM 2.0 / LTPI | 把 BMC/RoT/flash/TPM 等安全控制模块标准化 | LTPI 让低速信号隧道化，便于多节点和 DC-SCM 模块复用 |
| Caliptra / silicon RoT | OCP 开放 silicon RoT，ASPEED AST2700 已适配 Caliptra | 2026-2027 成为可审计 RoT 基线；Caliptra 2.2 与 PQC 是新催化 |
| OCP S.A.F.E. / S.O.L.I.D. | S.A.F.E. 是安全审计框架；S.O.L.I.D. 2026 进入 long-form report 要求 | 主权云/欧洲 CRA/云厂商供应链安全把它变成采购门槛 |
| Digital power MCU/BMIC | PSU、BBU、PDB、hot-swap、PMBus、CAN、I2C/I3C 控制 | BBU 变成高端 AI rack 可靠运行的关键件，MCU 性能和安全要求提高 |
| Cooling control MCU | 风扇、泵、阀、漏液、水质、压力、温度与 Redfish/DCIM 集成 | 2026 液冷 attach rate 上升，控制与传感从附属件变成 uptime 保险件 |

### 1.4 结合 2026-2027 出货量最大的 AI 芯片/平台看控制面需求

下表的 AI 芯片排序与出货/价值判断来自项目内 `ai_chip_research_2026_2027.md`，本文只做 BMC/MCU/嵌入式控制映射。

| 排名 | AI 芯片/平台 | 2026-2027 技术背景 | BMC/MCU/嵌入式控制增量 |
|---:|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | 2026 主力，GB300 NVL72 约 142kW 液冷整柜，48V/54V power shelf | 市场估算 GB300 NVL72 约 71 颗 BMC；AST2700、OpenBMC/MegaRAC、AMC、power shelf MCU、液冷控制器最确定 |
| 2 | AWS Trainium2 | Project Rainier 大规模，Anthropic 目标百万颗 Trainium2 级别 | 私有 rack control plane；BMC/MCU 外部可见度低，但 UltraServer、NeuronLink、EFA、BBU、电源控制需求高 |
| 3 | Google TPU v7 Ironwood | 192GB HBM，推理优先，Anthropic/Google Cloud 拉动 | Google 自有管理栈 + BMC/firmware/RoT；软件价值内部化，但 Nuvoton/ASPEED/firmware/IP 仍受益 |
| 4 | NVIDIA B200/GB200 | 2025-2026 延续放量，第一代 Blackwell rack learning curve | 市场估算 GB200 平台约 89 颗 BMC；形成 GB300/Rubin 的管理和液冷/供电验证经验 |
| 5 | Huawei Ascend 910C/950 | 中国国产替代，SuperPoD/超节点靠系统级互连 | 国产 BMC、MCU、firmware、RoT、液冷/电源控制替代；软件生态和可靠性是壁垒 |
| 6 | Cambricon MLU 590/690 | 2026 中国市场数量弹性大，SMIC/HBM 约束 | OAM/国产集群需要国产 BMC/MCU/电源/液冷控制；单价低于 NVIDIA 但数量可观 |
| 7 | AMD MI350X/MI355X | 2026 AMD 最确定放量，PCIe/UBB/企业形态并存 | 标准服务器 BMC + UBB 管理；ROCm/firmware update、power telemetry、OCP/UALink 生态 |
| 8 | AWS Trainium3 | 3nm，144 芯片 UltraServer，2026 H2-2027 放量 | 更高 rack 复杂度，power/thermal/firmware sideband 通道增多；BBU/BMIC 与 rack manager 价值提高 |
| 9 | Meta MTIA 300/400/500 | Meta 自研推理/推荐 ASIC，Broadcom XPU，>1GW 初期 | Meta/OCP/OpenBMC 牵引强；标准化 rack manager、OpenRMC、S.O.L.I.D./Caliptra 受益 |
| 10 | Microsoft Maia 200 | TSMC 3nm、216GB HBM3E、750W SoC、闭环液冷 | Azure 私有控制平面；PQC RoT、firmware update、液冷电源联动、rack telemetry 为重点 |
| 11 | Google TPU8 / Broadcom XPU | 2026 早期导入，2027 增量 | ASIC baseboard AMC、firmware/RoT、PLDM/SPDM、rack manager 成为 Broadcom XPU 配套 |
| 12 | AMD MI400/MI455X Helios | 2026 H2 首批，2027 可能成为 AMD 主力，HBM4/ORW | Helios open rack、72 GPU、液冷、电源与 UALink 管理使 BMC/MCU attach 明显上行 |

### 1.5 新技术成熟与放量时间表

| 技术方向 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|
| AST2700 / NPCM8mnx 高端 BMC | 2026 H2 GB300/新 CPU 平台导入，2027 主力替代 AST2600/NPCM7 | 2026 Q3 起 AI rack 紧缺，AST2700 ASP +40%-50% 被市场接受 | 2026 H2 因 BMC 短缺成为整柜交付瓶颈，客户预付锁产能 |
| BMC SiP / DC-SCM 模块 | 2026 样品/小批量，2027 在 accelerator card 和 multi-node 放量 | 2027 上半年成为高密 AI tray 的优选形态 | 2026 H2 就被 GB300/ASIC 加速板大规模采用，设计周期缩短带来溢价 |
| OpenBMC 商用发行版 | 2026 OneTree/SP-X/Insyde/Phoenix 继续导入，2027 多平台统一 | AMI Rack Manager + OneTree CE 带动 rack-level subscription | hyperscaler 统一控制面外溢到 OEM/NeoCloud，固件订阅成为新利润池 |
| OCP GPU/Accelerator management | 2026 v0.9 进入参考，2027 v1.0 后量产 | 2027 高端 UBB/ASIC 必须支持 Redfish/PLDM/MCTP/SPDM | 2026 H2 大客户 RFP 直接引用，AMC 成为 GPU/ASIC baseboard 标配 |
| Caliptra/PQC RoT | 2026-2027 成为安全加分项 | 2026 Q4 后 OCP S.O.L.I.D. 进入 SAFE long-form，欧洲/主权云强制化 | PQC secure boot/RoT 在 2026 H2 成为 frontier AI 集群采购硬门槛 |
| 48V/54V power MCU/BMIC/BBU | 2026 全年跟随 GB300/TPU/Trainium 放量 | BBU 在高端 AI rack attach 过半 | 近 rack 储能/BBU 因功率瞬态成为强制配置，BMIC/MCU 缺货 |
| 800VDC 控制/保护 MCU | 2026 样机/设计导入，2027 Rubin Ultra/Kyber 小批量 | 2027 H2 高端新建 AI factory 10%-20% 采用 | 2027 新建高端项目 30%+ 直接采用，安全控制器与高压传感器放量 |
| 液冷控制 MCU/漏液检测 | 2026 随 direct-to-chip attach 进入高增长 | 2027 L2L/warm-water 标准化，控制软件进入 DCIM/Mission Control | 液冷事故风险使漏液/水质/泵阀控制从可选变必配 |

## 2. 已开始放量的关键产品：市场规模、渗透率与利润率

### 2.1 总市场三情景

这里的收入池包括 BMC SoC、BMC SiP、BMC/firmware 软件、RoT/TPM/PFR、power/cooling MCU、BBU BMIC、accelerator AMC、rack manager、控制网关和安全认证服务。它不包括大功率 PSU、CDU、冷板、整机服务器本体。

| 时间窗口 | 基准 | 乐观 | 极度超预期乐观 | 关键假设 |
|---|---:|---:|---:|---|
| 未来 3 个月（2026-05 至 2026-08） | $0.7-1.5B | $1.2-2.4B | $2.0-3.6B | GB300/B300 拉货，BMC/PMIC 交期拉长，客户开始锁 AST2700、power MCU、RoT |
| 未来 12 个月（至 2027-05） | $4.0-7.8B | $6.8-12.5B | $12-22B | 2026 H2 GB300 + Trainium/TPU/MTIA 放量，Rubin/MI400 初批导入 |
| 未来 24 个月（至 2028-05） | $7.5-14B | $13-26B | $25-45B | Rubin/MI400/TPU8/Trainium3 扩大，rack manager、PQC RoT、800VDC 控制开始规模化 |

### 2.2 细分产品市场规模与渗透率路径

| 已放量产品 | 当前状态 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| BMC SoC：ASPEED AST2600/AST2700、Nuvoton NPCM7/8 | 传统服务器 100% attach，高端 AI rack 多节点 attach | 基准 $0.20-0.33B；乐观 $0.30-0.45B；极度 $0.45-0.65B | 基准 $0.95-1.4B；乐观 $1.35-1.9B；极度 $2.0-2.8B | 基准 $1.3-2.0B；乐观 $2.0-3.2B；极度 $3.5-5.2B | host BMC 近 100%；AI BMC 占总量 2026 约 30%-35%，2027 约 37%-45%，2028 约 43%-55% |
| BMC SiP / DC-SCM 模块 | Nuvoton Arbel SiP、Axiado Smart-SCM，小批量导入 | $30-80M / $60-140M / $120-250M | $0.20-0.45B / $0.40-0.80B / $0.90-1.60B | $0.80-1.50B / $1.40-2.80B / $3.00-5.50B | AI accelerator/multi-node attach 2026 <5%-10%，2027 10%-25%，2028 25%-45% |
| 商用 BMC 固件与支持：AMI、Insyde、Phoenix、OEM | MegaRAC SP-X 成熟，OneTree 3.0/CE 2026 发布 | $0.10-0.18B / $0.18-0.32B / $0.35-0.60B | $0.60-1.10B / $1.0-1.8B / $2.0-3.2B | $0.90-1.80B / $1.80-3.50B / $4.0-7.0B | 高端 AI/enterprise 付费支持 2026 30%-45%，2027 40%-60%，2028 55%-75% |
| GPU/ASIC accelerator AMC / UBB BMC | OCP accelerator management v0.9，GB200/GB300/MI400/ASIC baseboard 拉动 | $50-120M / $120-250M / $250-500M | $0.30-0.80B / $0.80-1.60B / $1.80-3.50B | $0.80-2.20B / $2.00-4.80B / $5.50-10B | UBB/accelerator baseboard attach 2026 10%-25%，2027 30%-60%，2028 60%-85% |
| RoT/PFR/TPM/secure MCU | Microchip CEC1736/TS1800、Nuvoton TIP、ASPEED Caliptra、Axiado TCU | $80-180M / $150-300M / $300-550M | $0.50-1.0B / $0.90-1.8B / $2.0-3.8B | $1.0-2.4B / $2.2-5.0B / $5.0-9.0B | server platform attach 2026 40%-65%，2027 60%-80%，2028 80%-95% |
| PSU/BBU/BMIC/数字电源 MCU | power shelf、BBU、PMBus/CAN、PDB、hot-swap、battery monitor | $0.15-0.35B / $0.30-0.70B / $0.70-1.20B | $0.80-1.80B / $1.60-3.20B / $3.50-6.50B | $1.60-4.00B / $3.80-8.50B / $9.0-16B | 高端 AI rack power/BBU attach 2026 30%-60%，2027 50%-75%，2028 70%-90% |
| 风扇/泵阀/漏液/水质控制 MCU | 液冷与高功率风扇控制，从附属件变 uptime 必配 | $80-200M / $180-420M / $450-800M | $0.40-1.20B / $1.00-2.20B / $2.50-4.80B | $0.90-3.00B / $2.50-6.00B / $7.00-13B | 液冷控制 attach 2026 40%-60%，2027 55%-80%，2028 70%-95% |
| rack manager / control gateway / telemetry appliance | AMI Rack Manager、OpenRMC-DM、OEM/DCIM edge gateway | $50-150M / $120-300M / $300-600M | $0.40-1.0B / $0.90-2.0B / $2.20-4.50B | $1.0-3.0B / $3.0-7.0B / $8.0-14B | AI rack attach 2026 15%-30%，2027 30%-50%，2028 50%-75% |
| 安全审计/固件签名/密钥注入服务 | OCP S.A.F.E.、FIPS、CRA、secure provisioning | $20-60M / $50-120M / $120-250M | $0.15-0.45B / $0.35-0.90B / $1.0-2.0B | $0.40-1.20B / $1.0-2.80B / $3.0-6.0B | 高端客户 2026 20%-40%，2027 40%-65%，2028 65%-90% |

### 2.3 当前利润率三情景

| 产品 | 基准毛利率 | 乐观毛利率 | 极度超预期毛利率 | 为什么能维持价格 |
|---|---:|---:|---:|---|
| BMC SoC | 58%-68% | 66%-72% | 72%-78% | 市场集中、客户认证长、AST2700 代际升级、BMC 断供会卡整柜 |
| BMC SiP/DC-SCM | 40%-55% | 50%-65% | 60%-72% | 节省 PCB、DDR/eMMC/NOR/PMIC 设计验证，缩短 time-to-market |
| 商用 BMC 固件 | 55%-75% | 65%-82% | 75%-90% | 固件维护、CVE 修复、Redfish/PLDM 合规、客户测试资产形成锁定 |
| Accelerator AMC/UBB BMC | 45%-60% | 55%-70% | 65%-80% | 直接影响 GPU/ASIC 固件更新、telemetry、attestation 和 downtime |
| RoT/PFR/TPM/secure MCU | 35%-55% | 45%-65% | 60%-78% | OCP SAFE、CRA、PQC、密钥注入和供应链审计是准入门槛 |
| Digital power MCU/BMIC | 35%-55% | 45%-62% | 55%-70% | power transient、BBU、PMBus/CAN 与整柜稳定性强绑定 |
| Cooling/leak/fan/pump MCU | 35%-55% | 45%-65% | 60%-75% | 单柜价值高，漏液/过热事故成本远高于控制器 BOM |
| rack manager 软件/网关 | 45%-70% | 60%-82% | 75%-90% | 从一次性设备走向订阅、fleet policy、事件分析和远程运维 |

## 3. 在研关键产品和细分技术

### 3.1 快速增长产品池

| 在研/早期导入方向 | 技术意义 | 成熟与放量判断 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月市场规模 | 渗透率路径 |
|---|---|---|---:|---:|---:|---|
| AST2700/下一代 BMC 全面替代 | 12nm、4xA35、2xM4、DDR5、UFS、CAN、LTPI、Caliptra | 2026 H2 高端 AI server，2027 主力 | $50-120M / $120-250M / $250-450M | $0.50-1.20B / $1.0-2.0B / $2.2-3.5B | $1.2-2.5B / $2.5-4.5B / $5.0-8.0B | 高端 AI BMC 中 2026 15%-30%，2027 45%-70%，2028 70%-90% |
| Integrated TCU / secure BMC | Axiado AX3080 把 BMC、RoT、TPM、firewall、HSM、LPDDR/eMMC、AI threat detection 集成 | 2026 样机/小批量，2027 若被 NVIDIA/ODM 认证放量 | <$50M / $50-120M / $150-300M | $0.20-0.60B / $0.60-1.30B / $1.50-3.00B | $0.80-2.50B / $2.50-6.00B / $7.00-13B | 2026 <3%，2027 5%-15%，2028 15%-35% |
| PQC RoT / secure boot controller | Microchip TS1800、Nuvoton Arbel A3、Caliptra 2.2 支持 ML-DSA/ML-KEM/LMS 等 | 2026 受 CRA/CNSA/OCP 推动；2027 高端平台标配 | <$50M / $50-120M / $120-250M | $0.15-0.45B / $0.40-1.0B / $1.2-2.5B | $0.60-1.80B / $1.80-4.50B / $5.0-10B | 2026 5%-15%，2027 20%-45%，2028 50%-80% |
| Caliptra/OpenTitan/IP + SAFE/SOLID 审计 | 开放 silicon RoT 和审计要求，降低黑盒安全风险 | 2026 Q4 后 SAFE long-form 引用 S.O.L.I.D.，2027 RFP 强化 | $30-80M / $80-160M / $180-350M | $0.20-0.60B / $0.50-1.2B / $1.3-2.8B | $0.60-1.50B / $1.50-3.50B / $4.0-8.0B | 高端客户 2026 10%-25%，2027 35%-60%，2028 60%-85% |
| Virtual AMC / software-defined accelerator management | OCP v0.9 提到未来 UBB Redfish 可由 AMC 或 supplier software library 暴露 | 2026 规范和试点，2027 随 ASIC/UBB 普及 | $20-70M / $70-180M / $200-400M | $0.20-0.70B / $0.70-1.80B / $2.0-4.0B | $0.80-2.50B / $2.50-6.00B / $7.0-15B | UBB/ASIC 2026 <10%，2027 25%-50%，2028 60%-90% |
| AI rack manager / OpenRMC-DM | 从 server-by-server 管理转向 rack 级 power/cooling/network/accelerator policy | 2026 AMI CE/Rack Manager 与 OCP，2027 平台化 | $30-100M / $100-250M / $250-500M | $0.30-0.90B / $0.90-2.20B / $2.5-5.0B | $1.2-3.5B / $3.5-8.0B / $9.0-18B | AI rack 2026 10%-25%，2027 30%-60%，2028 60%-85% |
| 800VDC control/protection MCU | 高压 DC busway、solid-state breaker、hot-swap、arc detection、isolation sensing | 2026 设计导入，2027 Rubin Ultra/Kyber 小批量 | $50-150M / $150-350M / $400-800M | $0.50-1.40B / $1.40-3.50B / $4.0-8.0B | $2.0-6.0B / $6.0-14B / $15-30B | 新建高端 AI rack 2026 <5%，2027 10%-30%，2028 35%-60% |
| AI predictive maintenance sensor fusion | BMC/TCU 内置 AI，结合温度、电压、振动、流量、日志做异常检测 | 2026 高端 TCU/软件试点，2027 服务化 | $20-80M / $80-180M / $200-400M | $0.20-0.70B / $0.70-1.80B / $2.0-4.5B | $0.80-2.50B / $2.50-6.00B / $7.0-13B | 高端 rack 2026 <10%，2027 20%-45%，2028 45%-75% |
| OCP L.O.C.K./KMB/attested erase | 存储安全，但与 BMC/RoT/密钥管理生态重叠 | 2026 规范/MCU reference，2027 SSD/AI storage 客户化 | $20-70M / $70-150M / $150-300M | $0.20-0.60B / $0.60-1.50B / $1.8-3.5B | $0.60-2.0B / $2.0-5.0B / $6.0-12B | AI storage/secure SSD 2026 <5%，2027 15%-35%，2028 40%-70% |

### 3.2 在研产品利润率预测

| 在研方向 | 基准毛利率 | 乐观毛利率 | 极度超预期毛利率 | 价值捕获理由 |
|---|---:|---:|---:|---|
| AST2700/next BMC | 65%-70% | 70%-75% | 75%-80% | 代际 ASP、客户认证、供给稀缺 |
| Integrated TCU | 45%-60% | 60%-75% | 70%-85% | 把多颗芯片和安全软件集成，替代 BOM + 降低攻击面 |
| PQC RoT | 40%-60% | 55%-72% | 70%-85% | 法规/标准驱动，客户对 secure provisioning 不敏感 |
| Caliptra/SOLID/IP/审计 | 70%-85% | 80%-90% | 85%-95% | IP、审计、工具链和服务属性强 |
| Virtual AMC / rack manager | 65%-82% | 75%-90% | 85%-95% | 软件订阅与 fleet management，客户迁移成本高 |
| 800VDC 控制/保护 | 35%-55% | 45%-65% | 60%-75% | 安全认证、失效风险、系统级 design-in |
| AI predictive maintenance | 60%-80% | 75%-90% | 85%-95% | 数据闭环和模型/规则库形成长期锁定 |
| OCP L.O.C.K./KMB | 50%-70% | 65%-85% | 80%-92% | 安全 IP + firmware + certification，而非普通 MCU 定价 |

## 4. 供给侧：产能、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/能力 |
|---|---|---|---|
| BMC SoC 设计 | 台湾、以色列、美国 | ASPEED、Nuvoton、Axiado、Intel/AMD/OEM 内部、华为/中国本土 BMC 供应链 | AST2700 公开为 12nm；AST2600/NPCM7xx 多为成熟逻辑节点；BMC 需要模拟、视频、I/O、安全和嵌入式内存协同 |
| BMC/TCU 封装与 SiP | 台湾、中国大陆、东南亚、以色列供应链 | Nuvoton Arbel SiP、Axiado AX3080、OSAT/EMS | BGA、SiP，集成 DDR/eMMC/NOR/PMIC/被动件；关键是良率、测试和 secure provisioning |
| RoT/TPM/secure MCU | 美国、台湾、欧洲、日本 | Microchip、Infineon、Nuvoton、ST、NXP、Renesas、Axiado | 多用 40/55/90/130nm mature nodes，重安全认证、密钥注入和防篡改 |
| Digital power MCU/BMIC/PMIC | 美国、欧洲、日本、台湾、中国大陆 | TI、Infineon、ST、Renesas、Microchip、Nuvoton、MPS、ADI、onsemi、Richtek、uPI | 8-inch/12-inch mature analog BCD/CMOS，受 PMIC/模拟产能约束 |
| 风扇/泵阀/液冷控制 | 台湾、中国大陆、日本、欧美 | Nuvoton、Microchip、TI、ST、Infineon、Renesas、NXP、Danfoss、Parker、Delta | MCU + motor driver + sensor ADC + isolation/CAN/I2C/PMBus |
| 固件/软件 | 美国、台湾、中国大陆、印度、以色列、欧洲 | AMI、Insyde、Phoenix、OpenBMC 社区、Dell/HPE/Lenovo/Cisco/SMCI/OEM、NVIDIA/Meta/Google/AWS/Microsoft 内部 | Yocto/OpenEmbedded、Linux kernel、Redfish、PLDM/MCTP、SPDM、secure update、fleet telemetry |

### 4.2 供给瓶颈

1. **BMC 高端工艺和封装产能。** AST2700 进入 12nm 后不再只是低端成熟制程小芯片，先进一点的逻辑产能和高速 I/O 验证都会限制爬坡。
2. **8-inch 模拟/PMIC/MCU 产能。** PMIC、BMIC、hot-swap、isolated sense、motor driver 常依赖成熟节点；AI server 优先级提高后，传统服务器和工业客户被挤压。
3. **DDR/eMMC/NOR 与 SiP 配套。** Nuvoton Arbel SiP 把 DDR4、eMMC、NOR、PMIC、120+ 被动件封装进去，任何小料缺货都会影响 SiP 出货。
4. **安全认证和密钥注入流程。** OCP S.A.F.E.、FIPS 140-3、NIST SP 800-193、客户 secure manufacturing 审计、PQC 算法迁移都会拖慢新产品量产。
5. **OpenBMC/Redfish/PLDM 工程人才。** 能把 BMC SoC、host BIOS、GPU firmware、NIC、SSD、retimer、power、cooling 打通的人很少，人才比芯片面积更稀缺。
6. **客户 AVL 与整柜验证。** BMC/MCU 更换会触发热、电、固件、冗余、KVM、security、remote update 重测；认证周期本身就是供给瓶颈。
7. **sideband interoperability。** I2C/I3C/MCTP/PLDM/SPDM/Redfish schema 的版本差异会造成系统集成风险，尤其是 GPU/ASIC baseboard 和多供应商 rack。
8. **现场交付与 firmware update 风险。** 数据中心不愿为 BMC/AMC 更新停机；OCP GPU FW update 要求非破坏性、可回滚、少依赖，工程难度高。

### 4.3 成本构成和毛利决定因素

| 产品 | BOM/单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| BMC SoC | wafer/test 35%-50%；封装 10%-15%；IP/EDA/NRE 摊销 10%-20%；渠道/支持 10%-20% | 市占率、die size、工艺节点、客户认证、固件生态、供给紧缺 | 高端 AI 平台若指定 AST2700/NPCM8，客户以交期和验证风险接受涨价 |
| BMC SiP/DC-SCM | BMC die 25%-40%；DDR/eMMC/NOR 20%-35%；PMIC/passive/oscillator 10%-20%；SiP 封测 15%-25% | 集成度、良率、缩短客户 PCB/验证周期的价值 | 用“减少 PCB 面积/仿真/调试/库存”的系统价值定价，不按裸 BMC die 定价 |
| BMC 固件 | 工程人力 50%-70%；测试与合规 10%-20%；支持/安全响应 15%-25% | 测试覆盖、长期维护、CVE 响应、OCP SAFE、客户定制 | 授权费 + NRE + 支持订阅；AI rack 越复杂，客户越不愿自维护 |
| RoT/PFR/TPM | secure MCU die 25%-45%；封装/测试 10%-20%；security IP/firmware/provisioning 25%-45% | 认证、密钥注入、安全生命周期、PQC 支持 | 法规和客户 RFP 强制 attach，单价小但客户不愿冒安全审计风险 |
| Digital power MCU/BMIC | MCU/analog die 30%-45%；AFE/sensor/isolation 15%-30%；固件 10%-20%；测试 10%-20% | 转换效率、瞬态响应、PMBus/CAN、functional safety、BBU 算法 | 对 $3M-$9M rack 来说控制器成本极低，缺货可直接涨价 |
| Cooling control MCU | MCU/driver/sensor 30%-50%；PCB/connector 20%-35%；软件/标定 15%-30% | 漏液误报/漏报率、泵阀冗余、与 DCIM/Redfish 集成 | 漏液事故成本极高，认证控制板可获得安全溢价 |
| rack manager | appliance hardware 20%-40%；软件 40%-70%；服务 10%-25% | policy engine、跨设备兼容、遥测数据、故障预测、客户运维流程 | 硬件一次性 + 软件订阅 + fleet support，客户迁移成本逐年上升 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | 头部集中度判断 | 主要玩家 |
|---|---|---|
| BMC SoC | 高集中。ASPEED 是全球 BMC SoC 第一，媒体/法人估算 CPU server BMC 份额约 70%；ASPEED + Nuvoton 在第三方报告中常被估计占 80%-85% | ASPEED、Nuvoton、Axiado、少数 OEM/中国本土 BMC |
| 商用 BMC 固件 | 中高集中。AMI 在通用服务器/OEM/ODM 覆盖最广，Insyde/Phoenix 有特定客户 | AMI MegaRAC、Insyde Supervyse、Phoenix ServerBMC、OpenBMC community、Dell iDRAC、HPE iLO、Lenovo XCC、Cisco CIMC/Intersight |
| RoT/PFR/TPM | 分散但认证壁垒高 | Microchip、Infineon、Nuvoton、ST、NXP、Renesas、Axiado、Google/OpenTitan、OCP Caliptra ecosystem |
| Accelerator management | 早期，标准形成中，平台方强势 | NVIDIA NVBMC/MGX/GB200/GB300、AMD/MI 系列、Broadcom XPU/Meta、AWS/Google/Microsoft 私有、OCP GPU Management |
| Power/cooling MCU | 分散，头部模拟/MCU 厂在高端方案中强势 | TI、Infineon、ST、Renesas、Microchip、Nuvoton、MPS、ADI、onsemi、NXP、Richtek、uPI、Delta |
| Rack manager/DCIM edge | 早期，软件平台竞争 | AMI Rack Manager、OpenRMC-DM、NVIDIA Mission Control/DSX、Schneider EcoStruxure/ETAP、Vertiv OneCore、Eaton Brightlayer、Dell OpenManage、HPE OneView、Lenovo XClarity、Cisco Intersight |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 定价能力来源 |
|---|---|---|
| 技术壁垒 | BMC 要同时支持 Linux、视频/KVM、PCIe/eSPI/LPC/I3C/I2C、MCTP/PLDM、Redfish、secure boot、firmware update | 功能越多、接口越复杂，客户越不愿换供应商 |
| 安全壁垒 | RoT、PFR、PQC、DICE、FIPS、OCP SAFE、NIST 800-193、密钥注入需要多年积累 | 没有认证就进不了高端 RFP，价格不是首要变量 |
| 规模壁垒 | AI rack 需要一平台多 tray 批量交付，故障率 ppm、现场支持和长期供货能力比样片更重要 | 大客户为供货确定性预付和多年度锁单 |
| 渠道/客户锁定 | ODM/OEM/CSP 的 BMC 固件、传感器 mapping、FRU、BIOS、电源、液冷策略深度绑定 | design-in 后生命周期内很难替换 |
| 标准/认证壁垒 | Redfish/PLDM/MCTP/SPDM/OCP DC-SCM/OCP accelerator management 的真实互通需要测试资产 | 通过互操作测试的供应商可享受认证溢价 |
| 切换成本 | 更换 BMC/MCU 会触发主板、固件、热、电、冗余、remote update、安全重测 | 小芯片可影响整柜交付，客户对价格不敏感 |
| 数据壁垒 | rack manager 和 predictive maintenance 拥有长期遥测、故障、维修数据 | 软件/服务续费和模型优化形成复利 |

### 5.3 价值捕获排序

1. **BMC SoC / high-end BMC silicon。** 份额集中、毛利高、代际升级明确，2026 最直接。
2. **BMC firmware + rack manager 软件。** 直接收入小于硬件，但毛利最高，且从一次性授权走向订阅和安全维护。
3. **RoT/PQC/PFR 安全链。** 单颗 ASP 不高，但 attach rate 可能接近 100%，法规与主权云带来非周期性需求。
4. **Power/BBU/BMIC 与 cooling control MCU。** 受益 AI rack 数量和功率密度，产品多而分散，进入头部平台认证后毛利上行。
5. **BMC SiP/DC-SCM/TCU。** 2026-2027 弹性大，但还需要证明被高端平台规模采用。
6. **普通低端 MCU/风扇控制。** 数量大但竞争更激烈，除非绑定液冷/BBU/高压安全认证。

## 6. 2026 关键变化：行业拐点与最可能放量方向

### 6.1 拐点一：AI rack 使 BMC 数量从“一台一颗”跳到“一柜几十到上百颗”

Nuvoton 直接给出 80 到 120 颗/AI rack 的方向，台湾市场估算 GB200/GB300/ASIC 服务器的 BMC 用量也在几十颗级别。2026 年最确定放量的是 GB300/B300 对 AST2700、AST2600、NPCM8、OpenBMC/MegaRAC、AMC、power/cooling MCU 的拉动。

最可能放量子方向：

- AST2700/NPCM8 高端 BMC SoC。
- GPU/switch/power/cooling tray 管理控制器。
- BMC SiP/DC-SCM 在 accelerator card 和 multi-node 中导入。

### 6.2 拐点二：OpenBMC 从 hyperscaler 内部工程变成商用平台

AMI OneTree 3.0 在 2026 年明确支持 AST2700、GB300、早期 Vera Rubin、Blackwell/Rubin GPU，并披露 6,175 个测试用例、超过 95% pass rate、545 个 issue 修复。OneTree Community Edition 和 AMI Rack Manager 则把 rack 级 power/cooling/network 管理纳入 OpenBMC 生态。

最可能放量子方向：

- 商用 OpenBMC distribution 与支持订阅。
- Rack Manager / OpenRMC-DM。
- OCP GPU firmware update 和 accelerator management 合规工具。

### 6.3 拐点三：安全从“可选增强”变成采购 gating factor

Nuvoton NPCM8mnx A3 通过 OCP S.A.F.E.，支持 PQC LMS secure boot、TIP、DICE；Microchip 2026-04 发布 TS1800/TS50x PQC-ready RoT；OCP EMEA 2026 材料显示 S.O.L.I.D. 将从 2026-10-01 起进入 OCP S.A.F.E. long-form report。安全链路会决定服务器、BMC、SSD、GPU、NIC 是否进高端客户 RFP。

最可能放量子方向：

- PQC RoT / secure boot controller。
- Caliptra / OCP S.A.F.E. / S.O.L.I.D. 审计服务。
- Firmware signing、密钥注入、secure provisioning。

## 7. 2027 关键变化：行业拐点与最可能放量方向

### 7.1 拐点一：Rubin/MI400/TPU8/Trainium3 把管理面推向 rack-scale 和 pod-scale

2027 的核心不只是 GPU 更快，而是 rack 变成基本交付单元。Rubin、MI400 Helios、Trainium3 UltraServer、TPU8、MTIA 400/500 都会提高 tray 数量、sideband telemetry、firmware update 和 security attestation 复杂度。

最可能放量子方向：

- Accelerator AMC / UBB BMC。
- Virtual AMC / supplier software library。
- Rack manager 与 fleet policy engine。

### 7.2 拐点二：800VDC 与 BBU 把 MCU/BMIC 从辅助件推到安全边界

2026 主流仍是 48V/54V power shelf，2027 Rubin Ultra/Kyber 与新建 AI factory 会推动 800VDC 控制、固态保护、isolation sensing、arc detection、BBU/BMIC、supercapacitor 控制放量。

最可能放量子方向：

- 800VDC hot-swap/eFuse/solid-state breaker 控制。
- BBU BMIC、pack monitor、power smoothing MCU。
- 高压隔离传感、functional safety MCU。

### 7.3 拐点三：主权云与 CRA 把 firmware/RoT 可审计性变成溢价层

欧洲主权云讨论不只是 data residency，而是 supply chain、firmware、lifecycle、auditability、vendor swap。2027 年 OCP S.O.L.I.D.、Caliptra、openSFI、SBMR、PQC RoT 可能被更多写入 RFP。

最可能放量子方向：

- 可审计 OpenBMC/OpenSFI/SBMR 固件。
- PQC/Caliptra silicon RoT。
- 安全审计、固件生命周期管理、attestation as a service。

## 8. 头部公司全景清单

### 8.1 BMC SoC / BMC SiP / TCU

| 公司 | 优势 |
|---|---|
| ASPEED | BMC SoC 绝对龙头；AST2600 成熟，AST2700 12nm/Caliptra/LTPI/CAN/DDR5 面向 AI server；2024 毛利 64%+ |
| Nuvoton | NPCM7xx/NPCM8mnx Arbel；TIP security enclave、OpenBMC、OCP S.A.F.E.、BMC SiP；2026Q1 材料明确 BMC count/rack 增长 |
| Axiado | AX3000/AX3080 TCU，把 BMC、RoT、TPM、firewall、HSM、AI threat detection 集成；面向 NVIDIA/AI data center |
| Intel / AMD 平台生态 | 通过 server platform、PFR、Management Engine/PSP、OEM 设计影响 BMC 接口与固件要求 |
| 中国本土 BMC 供应链 | 华为、浪潮、新华三、龙芯/飞腾/鲲鹏生态、国芯/兆易/中微半导体等可能在国产服务器中替代；公开份额不透明 |

### 8.2 BMC 固件、OpenBMC 与服务器管理软件

| 公司/项目 | 优势 |
|---|---|
| AMI | MegaRAC SP-X、MegaRAC OneTree、OneTree CE、Rack Manager；覆盖 ASPEED/Nuvoton/NVIDIA/AMD/Intel/ODM |
| Insyde Software | Supervyse OPF/OpenBMC-based firmware，2026 宣布 Intel Oak Stream 平台 OpenBMC power-on |
| Phoenix Technologies | ServerBMC，面向 Linux-based BMC firmware 与 OEM 客户 |
| OpenBMC community | hyperscaler 共同底座；Google、Meta、Microsoft、IBM、Intel、Arm 等生态 |
| Dell | iDRAC/OpenManage，企业客户粘性强，PowerEdge AI server 管理生态 |
| HPE | iLO/OneView/GreenLake，企业和 HPC/AI 管理生态 |
| Lenovo | XClarity Controller / XClarity Administrator，企业和云客户 |
| Cisco | CIMC/Intersight，网络与 UCS 管理整合 |
| Supermicro | BMC/IPMI/Redfish 与 AI server 出货绑定，NVIDIA/AMD 生态强 |
| NVIDIA | NVBMC、Mission Control、DSX、device attestation、GB200/GB300/Rubin 管理面 |
| Google / Meta / Microsoft / AWS | 自有 OpenBMC fork、rack manager、ASIC 管理与安全流程，外部商业收入少但决定供应链要求 |

### 8.3 RoT、PFR、TPM、secure MCU、PQC

| 公司/项目 | 优势 |
|---|---|
| Microchip | CEC1736 TrustFLEX/Soteria-G3、TS1800/TS50x PQC-ready RoT、NIST/OCP 相关定位 |
| Infineon | OPTIGA TPM、安全芯片、功率/MCU 组合，欧洲客户和工业安全能力 |
| Nuvoton | TPM、TIP security enclave、OCP S.A.F.E.、PQC LMS secure boot |
| ASPEED | AST2700 适配 Caliptra，BMC SoC 内建安全引擎 |
| Axiado | TCU 集成 RoT/TPM/HSM/firewall/AI threat detection |
| STMicroelectronics | STM32/secure element/STSAFE、PQC/工业安全潜力 |
| NXP | EdgeLock、secure MCU、网络/汽车/工业安全生态 |
| Renesas | Secure MCU、RA/RZ 生态、电源/工业控制 |
| Google OpenTitan / lowRISC | 开放 RoT 项目，长线影响可审计 silicon |
| CHIPS Alliance / Caliptra | OCP silicon RoT IP 与 firmware，云厂商推动 |

### 8.4 Power/BBU/BMIC/数字电源 MCU

| 公司 | 优势 |
|---|---|
| Texas Instruments | C2000/MCU、isolated sensing、gate driver、PMBus、800VDC architecture 生态 |
| Infineon | XMC/PSoC、Si/SiC/GaN、TLVR、grid-to-core、电源系统能力 |
| STMicroelectronics | STM32、STNRG、GaN/SiC、800V-to-12/6V 架构 |
| Renesas | RA/RX MCU、digital power、power stage、server PMIC |
| Microchip | dsPIC33/digital power、安全 MCU、CEC 系列 |
| Nuvoton | BMIC、MCU、fan motor、BMC 协同，2026 材料明确 AI rack 机会 |
| MPS | AI/server/memory/optical/switch power solutions，800V data center solution sampling |
| Analog Devices / Maxim | power management、isolation、monitoring、precision sensing |
| onsemi | high/low voltage power, sensing, driver |
| Navitas / EPC / Power Integrations / ROHM / Innoscience | GaN/SiC 与高密电源设计导入 |
| Richtek / uPI / Silergy / Monolithic local peers | 亚洲服务器电源/PMIC 供应链 |
| Delta / Lite-On / Chicony / Flex / Megmeet | PSU/power shelf/BBU 系统供应商，控制板和 MCU 需求内嵌 |

### 8.5 Cooling/fan/pump/leak 控制

| 公司 | 优势 |
|---|---|
| Nuvoton | MCU、fan motor、BMC 组合 |
| Microchip / TI / ST / Infineon / Renesas / NXP | MCU、motor control、sensor AFE、CAN/I2C/I3C、functional safety |
| Delta | 风扇、泵、电源、CDU、BBU，AI rack 系统级能力 |
| Danfoss / Parker / Belimo / Grundfos / Xylem / Wilo | 泵阀、流体控制、传感与工业控制 |
| Schneider / Vertiv / Eaton / nVent / CoolIT / Boyd / Motivair | 液冷系统和控制软件，决定 MCU/控制板规格 |
| 中国/台湾供应链 | 台达、AVC、Cooler Master、Auras、英维克、申菱、高澜、同飞、三花、盾安、立讯等 |

### 8.6 Rack manager / DCIM / AI factory control

| 公司/项目 | 优势 |
|---|---|
| AMI Rack Manager / OpenRMC-DM | OpenBMC 延伸到 rack-level power/cooling/network management |
| NVIDIA Mission Control / DSX / Omniverse DSX | 将 AI factory power/cooling/controls 与 GPU token/watt 绑定 |
| Schneider EcoStruxure / ETAP / AVEVA | 电力仿真、DCIM、AI factory blueprint |
| Vertiv OneCore / Unify | 电力、冷却、控制和服务 |
| Eaton Brightlayer | 电力系统和 rack/BBU/液冷控制 |
| Siemens / Honeywell / Johnson Controls / Rockwell | 工业控制、BMS/OT 与数字孪生 |
| Dell / HPE / Lenovo / Cisco | 企业服务器 fleet management |
| Google / Meta / AWS / Microsoft | 自有 hyperscale fleet control，制定事实标准 |

## 9. 投资框架

**2026 最高确定性：BMC SoC + 商用 OpenBMC 固件 + 48V/54V power/cooling MCU。** 这些已经随 GB300/B300、Trainium、TPU、MTIA、Maia、MI350 进入订单周期。ASPEED 是最纯粹标的；Nuvoton 同时覆盖 BMC、BMIC、MCU、fan motor，弹性更分散；AMI/Insyde/Phoenix 更偏非上市或软件生态。

**2026 最大预期差：BMC 数量乘数。** 市场容易按服务器台数线性估 BMC，但 AI rack 真实逻辑是 tray 数量、管理节点和安全域数量。若 GB300 NVL72、custom ASIC、Trainium/TPU rack 大规模交付，BMC unit growth 会明显快于普通 server shipment。

**2027 最大期权：secure control module + rack manager + 800VDC 控制。** Rubin/MI400/TPU8/Trainium3 会使管理平面从主板进入整柜/整 pod。Axiado TCU、PQC RoT、Caliptra、OCP S.O.L.I.D.、OpenRMC-DM、800VDC protection controller 是弹性方向。

**长期最高 ROIC 层：软件/安全/IP。** BMC SoC 毛利已经很高，但总 TAM 仍小；真正长期可复利的是 firmware、security attestation、rack manager、fleet telemetry 和 predictive maintenance，因为它们可以按平台生命周期持续收费。

主要风险：

- GPU/HBM/CoWoS/电力交付不及预期导致 AI rack 延迟。
- BMC/MCU 供应商扩产后，2027 普通产品价格回落。
- 大客户把控制平面完全内制，外部供应商只能拿低毛利制造收入。
- OpenBMC 标准化降低部分固件差异化，但会提高认证和服务价值。
- 安全漏洞或 BMC 远程攻击事件可能短期打击个别供应商，但长期提升行业 attach rate 与审计需求。

## 10. 主要来源与校验

| 来源 | 用途 |
|---|---|
| [ASPEED AST2700 官方页面](https://www.aspeedtech.com/server_ast2700/) | AST2700 12nm、4x Cortex-A35、2x Cortex-M4、PCIe Gen4、DDR5、UFS、CAN、LTPI、Caliptra |
| [ASPEED 2025/11 投资者材料](https://www.tpex.org.tw/event/web/supervise_11411/2.5274%E4%BF%A1%E9%A9%8A.pdf) | BMC TAM、AI BMC 占比、2026Q1 营收/毛利指引 |
| [ASPEED 2024 sustainability report](https://www.aspeedtech.com/file/social/sustainability_report-2024-en.pdf) | 2024 营收 NT$6.428B、毛利率 64.41%、BMC SoC 市占第一 |
| [经济日报：信骅 BMC 晶片出货看增](https://money.udn.com/money/amp/story/11074/9479259) | GB200/GB300/ASIC BMC 用量估算、AST2700 ASP +40%-50%、2030 TAM 上修到 6,577 万颗 |
| [Nuvoton 2026Q1 investor conference](https://www.nuvoton.com/export/sites/nuvoton/2026Q1-Investor-Conference-ppt.pdf) | BMC per rack 80 到 120、rack power 120kW 到 1,000kW、BMIC/MCU/fan motor 机会 |
| [Nuvoton Arbel NPCM8mnx SiP](https://www.nuvoton.com/news/news/all/TSNuvotonNews-000572/) | 23x23mm BMC SiP、DDR/eMMC/NOR/PMIC/120+ 被动件、AI server 场景 |
| [Nuvoton NPCM8mnx OCP S.A.F.E.](https://www.nuvoton.com/news/news/products-technology/TSNuvotonNews-000560/) | TIP、DICE、PQC LMS、FIPS/OCP SAFE、OpenBMC |
| [Nuvoton iBMC 产品页](https://www.nuvoton.com/products/cloud-computing/ibmc/) | NPCM7xx/NPCM8mnx 架构、secure BMC、MCTP over PCIe、OpenBMC |
| [The Register / TrendForce 2026 服务器组件短缺](https://www.theregister.com/on-prem/2026/04/23/ai-now-gobbling-up-power-and-management-chips-for-servers/5229166) | PMIC/BMC lead time、2026 server shipment forecast 从 20% 下修到 13% |
| [AMI MegaRAC](https://www.ami.com/products/megarac/) | MegaRAC OneTree、Redfish、PLDM、MCTP、RAS、telemetry、AI infrastructure management |
| [AMI OneTree 3.0](https://www.ami.com/resources/announcing-megarac-onetree-version-3-0/) | 2026 支持 AST2700、GB300、早期 Vera Rubin、Blackwell/Rubin GPU、测试覆盖 |
| [AMI OneTree Community Edition / Rack Manager](https://www.ami.com/resources/ami-accelerates-ai-factory-command-and-control-with-new-megarac-onetree-community-edition/) | OpenBMC CE、AI factory rack management、OpenRMC-DM |
| [OCP DC-SCM 2.0](https://www.opencompute.org/documents/ocp-dc-scm-2-0-ver-1-0-pdf) | DC-SCM、BMC、RoT、TPM、LTPI、多节点管理 |
| [OCP GPU Firmware Update v0.9](https://www.opencompute.org/documents/ocp-gpu-fw-update-specification-v0-9-pdf) | Accelerator BMC/AMC、Redfish UpdateService、PLDM over MCTP、非破坏性 firmware update |
| [OCP GPU & Accelerator Management Interfaces v0.9](https://www.opencompute.org/documents/ocp-gpu-accelerator-management-interfaces-v0-9-pdf) | UBB Redfish、MCTP/PLDM/SPDM、AMC/virtual AMC、1s telemetry |
| [DMTF Redfish presentations](https://www.dmtf.org/education/presentations) | Redfish 2025.4、PLDM firmware update、libspdm、streaming telemetry |
| [Redfish Release History](https://redfish.dmtf.org/schemas/Redfish_Release_History.pdf) | ComponentIntegrity、SPDM/TPM alignment、PowerDistribution、metrics |
| [Microchip TS1800/TS50x PQC RoT](https://ir.microchip.com/news-events/press-releases/detail/1384/microchip-expands-its-family-of-post-quantumready-root-of-trust-controllers-for-nextgeneration-systems) | 2026 PQC-ready RoT、ML-DSA/ML-KEM/LMS、CRA/CNSA 2.0 |
| [Microchip data center embedded controllers](https://www.microchip.com/en-us/products/embedded-controllers/data-center) | CEC1736、TS1800、NIST 800-193、OCP、SPDM attestation |
| [Axiado AX3080 announcement](https://axiado.com/axiado-announces-industrys-first-ai-driven-single-chip-secure-control-and-management-solution/) | BMC+RoT+TPM+firewall+HSM+AI threat detection、25x25mm、4 TOPS、Q4 2025 production |
| [Axiado products](https://axiado.com/products/) | AX3080、Smart-SCM、AI-driven secure management card、<5W、OCP DC-SCM |
| [DCD: Axiado raises $100M](https://www.datacenterdynamics.com/en/news/axiado-raises-100m-for-hardware-based-data-center-security-platform/) | 2025 融资、AI data center security/platform management 扩张 |
| [NVIDIA GB200 switch attestation docs](https://docs.nvidia.com/networking/display/dpunicattestation/switch-system-attestation-view) | GB200 switch system BMC/eRoT/TPM/SPDM attestation |
| [NVIDIA Vera Rubin platform](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform) | Rubin、BlueField-4、Spectrum-6、rack-scale AI factory |
| [NVIDIA Vera Rubin technical blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | Rubin POD、五类 rack、power/cooling/controls 背景 |
| [项目内 AI 芯片路线图](../ai_chip_research_2026_2027.md) | 2026-2027 前十大 AI 芯片/平台、出货与技术背景 |
| [项目内 OCP EMEA 2026 调研](../conference_update/OCP_EMEA_Summit_2026_%E9%AB%98%E5%AF%86%E5%BA%A6%E8%B0%83%E7%A0%94%E6%8A%A5%E5%91%8A.md) | Caliptra 2.2、OCP L.O.C.K.、S.O.L.I.D.、openSFI、SBMR、Open DC for AI |
| [项目内机柜级供电报告](../行业调研_AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026.md) | 48V/54V、800VDC、BBU、power shelf、数字电源 MCU |
| [项目内直液冷报告](../行业调研_AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026.md) | 液冷控制、漏液检测、CDU 控制、Redfish/DCIM 集成 |

非投资建议。本报告用于产业链研究和情景分析；所有未来市场规模和利润率均为模型估算，关键风险包括 AI capex 放缓、GPU/HBM/CoWoS/电力交付扰动、客户自研替代、BMC 安全漏洞、标准路线变化、价格竞争和认证延期。
# 行业调研：【精密时钟与同步芯片】

截至日期：2026-05-08  
研究口径：本报告聚焦 AI 数据中心、AI 服务器、AI 网络、5G/vRAN 与跨数据中心同步所需的精密时钟与同步芯片/模块，包括 MEMS/石英振荡器、差分低抖动 XO/TCXO/OCXO、PCIe/Ethernet 时钟发生器与缓冲器、jitter cleaner、DPLL/SMU、SyncE/IEEE 1588 PTP 同步芯片、PTP grandmaster/time appliance、以及 PTP/时间戳 PHY/NIC 中的同步功能。市场规模为美元名义值，`B`=十亿美元，`M`=百万美元。

重要说明：精密时钟是一个“小美元、大杠杆”的 AI 基建环节。它不像 GPU/HBM 那样直接形成百亿美元单品，但它决定 800G/1.6T 光互联、224G SerDes、PCIe Gen6/7、SmartNIC/DPU、PTP/SyncE 和跨集群日志/调度的一致性。AI 数据中心里一颗几十美分到几十美元的时钟器件，可能保护的是单机架数百万美元 GPU/ASIC 的有效利用率。本报告对 AI 数据中心建设采取非常乐观假设：2026-2027 美国与全球 AI factory 继续抢电、抢 GPU、抢网络，且 Blackwell Ultra、Trainium、TPU、MI350/MI400、MTIA/Maia/OpenAI ASIC 等多路线并行扩张。

## 1. 核心结论

1. **2026 年最确定放量的是“低抖动参考时钟 + PCIe Gen5/6 clock tree + 800G/1.6T 网络时钟”。** Skyworks 2025H2 发布 18fs/17fs 级 clocks，Kyocera 2026 年 X 系列差分晶振从月产 20 万颗扩到 6 月月产 200 万颗，Diodes 2026-05 发布 PCIe 7.0 sub-30fs 时钟发生器，Microchip 已把 PCIe Gen7 clock generator/buffer/oscillator 作为数据中心产品线推广。
2. **2026 新增拐点是“同步从通信/金融/电力走进 AI 集群”。** SiTime 2026-05 Elite 2 Super-TCXO 直接宣称用于提高 AI 数据中心 GPU 利用率，目标 2030 年累计 $1.5B 市场；Microchip 2026-04 MD-990-0011-B 插卡同步模块与 Intel Xeon 6 SoC 平台配合，面向数据中心服务器、5G vRAN、分布式 AI workload。
3. **SiTime 收购 Renesas Timing 是行业结构性事件。** 交易对价为 $1.5B 现金 + 约 4.13M 股 SiTime 股票；公司披露被收购业务 post-close 12 个月收入约 $300M、毛利率约 70%、AI datacenter-comms 约占被收购收入 75%。这等于把 MEMS 振荡器、clock generator、clock buffer、network synchronizer、jitter cleaner 和 1588 软件整合成纯 timing 平台。
4. **时钟市场总体不大，但 AI 高端子市场增速很高。** SiTime 投资者材料给出的 2027 timing TAM 为约 $11B；第三方报告给 2026 crystal oscillator 市场约 $3.3B、前五家约 45.3% 份额。我的模型估算：AI 数据中心直接相关 timing/sync 芯片和模块收入池 2026 年约 $1.0-1.6B，乐观 $1.5-2.5B，极度乐观 $2.2-3.6B；2027 年分别约 $1.8-3.0B、$2.8-4.8B、$4.8-7.5B。
5. **价值捕获最强的不是普通晶振，而是系统级 timing platform。** 长期高 ROIC 层最可能出现在 MEMS/BAW 高端振荡器、PCIe/224G clock tree、PTP/SyncE DPLL/SMU、time appliance 软件/模块和客户认证工具链。普通石英晶振规模大但竞争更碎；高端 AI 时钟一旦进入 switch、SmartNIC、accelerator、optical module 或 time card 设计，切换成本高、认证周期长、毛利有机会维持 50-75%。

## 2. 2025H2-2026 一手信息与关键事实

| 时间 | 公司/组织 | 事实 | 对 AI 精密时钟的含义 |
|---|---|---|---|
| 2026-05 | SiTime | Q1 2026 收入 $113.6M，同比 +88.3%；CEO 表示 AI infrastructure 和 high-performance systems 使 precision timing 成为 system-level requirement，并带来更高 ASP 与 margin。 | 这是纯 timing 公司首次把 AI 基建上行显性反映到收入与管理层措辞中。 |
| 2026-05 | SiTime | Elite 2 Super-TCXO 面向 AI 数据中心时间同步，1ns 同步精度、±50ppb 稳定度、3.2mm x 2.5mm 封装；已 sampling，预计 2026 Q3 商业量产；公司给出 2030 年累计 $1.5B 市场。 | 这是“时钟提高 GPU 利用率”的直接产品化信号，2026H2 进入客户验证，2027 有望随 AI rack 放量。 |
| 2026-02 | SiTime/Renesas | SiTime 收购 Renesas timing business，$1.5B 现金 + 约 4.13M 股；被收购业务 post-close 12 个月约 $300M 收入、70% 毛利，AI datacenter-comms 约 75%。 | 行业从分散器件向完整 clock tree + sync platform 集中，SiTime 将成为纯 timing 龙头。 |
| 2026-04 | Microchip | MD-990-0011-B 插卡 timing module 面向数据中心服务器和 5G vRAN，与 Intel 合作，支持 GNSS/SyncE/PTP 自动源选择和锁定。 | PTP/SyncE 不再只是网络设备功能，而是进入服务器/平台选项。 |
| 2025-11 | Microchip | TimeProvider 4500 v3 支持 HA-TT，可在 800km 光网络做 sub-ns 时间分发，目标 ITU-T G.8271.1/Y.1366.1 Class A 5ns/800km。 | 跨园区、跨数据中心的可信时间分发进入产品化，GNSS 备份和 vPRTC 会成为 AI factory 韧性配置。 |
| 2025-10 | Microchip | 10/25G Optical Ethernet PHY 集成 IEEE 1588 PTP 与 MACsec，分布式节点 <1ns 同步精度。 | PTP 硬件时间戳和安全开始下沉到 PHY，工业/园区/边缘 AI 有增量。 |
| 2025-06 | Skyworks | SKY63104/5/6 与 SKY62101 支持 Ethernet + PCIe clock，224G PAM4 Ethernet SerDes 18fs RMS 相位抖动，PCIe Gen1-6；目标光网络、交换机、SmartNIC、AI 加速器。 | 224G SerDes 和 800G/1.6T 网络把 jitter 从“指标”变成系统余量核心。 |
| 2025-11 | Skyworks | BAW 可编程 clocks：SKY63101/02/03 SyncE jitter 17fs，用于 800G/1.2T/1.6T optical/DCI；SKY69001/02/101 支持 IEEE 1588 Class C/D 和 AccuTime 1588。 | BAW 从 RF 前端优势迁移到高端 timing，可能成为 MEMS/石英之外第三条路线。 |
| 2026-05 | Diodes | PI6CG33A06 PCIe 7.0 六输出时钟发生器发布，RMS jitter <30fs，低于 PCIe 7.0 67fs 要求；面向服务器、HPC、数据中心 AI 平台；LP-HCSL 降低 clock 相关功耗至少 50%。 | PCIe 7 仍是 2027 以后收入，但 2026 design-in 已经开始；Gen7 器件会先变成高端 AI 主板/交换/存储的认证筹码。 |
| 2026-02 | Kyocera | X 系列差分晶振 30fs phase jitter，2026-01 量产，2026-06 起月产能从 20 万颗提升到 200 万颗；用于 AI server、optical transceiver、storage、ADAS；156.25MHz LV-PECL 功耗较传统品 -42%。 | 传统石英龙头仍在高端低抖动市场进攻，且给出了明确产能扩张数字。 |
| 2026-05 | PCI-SIG DevCon | 议程包括 PCIe 6.x/7.0 electrical、PCIe 7 over optics、AI infrastructure with PCIe、AEC/DSP optics/LPO、PCIe 8.0 panel。 | 时钟、retimer、connector、optical-aware retimer 与 compliance 工具将在 2026 同步前置下单。 |
| 2026 | OCP Time Appliance Project | 2026 会议议题包括 PTP at nanosecond scale、resilient/tail-optimal RDMA NIC for distributed ML workloads、optical frequency & timing distribution with femtosecond precision。 | hyperscaler/OCP 社区把数据中心 timing 从运维工具升级为 AI/ML 网络基础设施议题。 |
| 2026 | WSTS | 2026 agenda 包含 Equinix “Neoclouds and AI Sovereignty - Timing at the Intersection of Data, Edge, and Trust”。 | 主权 AI、neocloud、colo 会提升跨地点可信时间、审计、日志一致性和合规需求。 |
| 2026-03 | Broadcom | Tomahawk 6 已 production volume shipping，102.4Tbps，512 个 200G 或 1024 个 100G SerDes。 | 102.4T switch、224G/200G SerDes、CPO/光模块对 17-30fs 级参考时钟形成确定需求。 |

## 3. AI 数据中心机会与挑战

### 3.1 为什么 AI 集群突然需要更好的 timing

AI 数据中心对 timing 的需求分成三层：

| 层级 | 需求 | 典型器件 | 2026 变化 |
|---|---|---|---|
| 物理链路层 | 112G/224G PAM4、800G/1.6T 光模块、PCIe Gen5/6、CXL/retimer、SmartNIC/DPU 需要低相位噪声和低 jitter refclk。 | SPXO、差分 XO、MEMS oscillator、BAW clock、clock generator、clock buffer、jitter attenuator。 | jitter 指标从 50-100fs 继续压到 17-30fs；AI switch/optic 对时钟良率和温漂更敏感。 |
| 网络同步层 | PTP/SyncE 让交换机、NIC、服务器、time card、grandmaster 具有亚微秒到纳秒级一致时间。 | DPLL/SMU、network synchronizer、PTP PHY/NIC、PTP grandmaster、time appliance、OCXO/TCXO/CSAC。 | OCP/Meta/NVIDIA/Microchip/SiTime 把数据中心 PTP 从“可选”推向“高端集群默认选项”。 |
| 系统调度/运维层 | 分布式训练、RDMA、日志排序、能耗调度、故障定位、主权 AI 审计需要可信时间。 | Time appliance、vPRTC、GNSS firewall、HA-TT、time observability 软件。 | neocloud/colo/跨园区 AI factory 增多，客户开始愿意为可靠同步付费。 |

### 3.2 2026 的机遇

1. **网络带宽升级强制拉动低 jitter 时钟。** 800G 继续放量，1.6T 进入头部客户导入，Tomahawk 6、Spectrum-X/Spectrum-6、Marvell 224G SerDes、CPO/硅光都会扩大 156.25/312.5/625MHz 等低噪声参考时钟需求。
2. **AI rack 价值太高，客户愿意用更贵时钟换 GPU 利用率。** 一台 NVL72/GB300/MI400/Trainium/TPU rack 的价值可达数百万美元，时钟 BOM 占比极低。只要同步能提升 0.5-2% 集群效率，高端 TCXO/OCXO/PTP 模块就有定价空间。
3. **服务器 timing 模块化。** Microchip MD-990-0011-B 说明 timing 可以作为服务器/平台 plug-in 模块进入 OEM/ODM BOM，利于在 AI 服务器、vRAN、边缘 AI 节点复用。
4. **SiTime + Renesas 可能重塑客户采购。** 客户原来需要分别采购 oscillator、clock generator、buffer、network synchronizer 和软件；整合后可卖 complete clock tree，design-in 粘性更强。
5. **国产替代也会拉动。** 华为 Ascend、寒武纪、阿里 PPU、百度昆仑等国产 AI 集群需要本土低抖动晶振、PCIe/Ethernet clock、PTP/SyncE、OCXO/TCXO 和测试设备，给 TXC、Epson、NDK、Kyocera、国产晶振/时钟 IC 厂商更多机会。

### 3.3 2026 的挑战

1. **客户教育仍在早期。** 对很多 AI 服务器采购方，timing 仍被当作小 BOM，而非系统效率变量；供应商必须拿出 GPU utilization、packet loss、BER、tail latency、debug time 的量化证据。
2. **标准碎片化。** NVIDIA NVLink/Spectrum、AMD UALink/Ethernet、AWS Neuron/EFA、Google TPU pod、自研 ASIC、OCP DC-PTP、telecom PTP profiles 会导致 clock tree 和同步 profile 不完全一致。
3. **高端低 jitter 测试能力紧缺。** 17fs/30fs 级相位噪声测量、PTP time error、wander、ADEV、TDEV、MTIE、temperature ramp、vibration 测试需要仪器、方法和工程人才。
4. **GNSS 安全与合规风险上升。** 数据中心依赖 GNSS 会面临 jamming/spoofing，需要 BlueSky/GNSS firewall、vPRTC、HA-TT、terrestrial timing 或多源 holdover。
5. **替代路线并存。** 石英、MEMS、BAW、OCXO、CSAC、DPLL、White Rabbit/optical timing 都能覆盖部分需求，2026-2027 会出现客户平台分裂，不会单一路线通吃。

## 4. 在主流 AI 芯片路线下的 timing 需求映射

本表使用项目已有 AI 芯片路线图作为底座，不重新外搜芯片信息。

| 2026-2027 出货/价值权重最高的平台 | 互连与系统背景 | 对精密时钟/同步芯片的拉动 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | rack 内 NVLink/铜互连，scale-out 800G/1.6T Ethernet/InfiniBand；高密液冷机柜。 | 交换机/SmartNIC/DPU/光模块低 jitter clock、PCIe Gen5/6 clock tree、PTP/SyncE time appliance、服务器级 TCXO/OCXO；2026 最强确定需求。 |
| AWS Trainium2 | Rainier/Anthropic 百万颗级目标，EFA/以太网 scale-out，rack 内 NeuronLink。 | EFA/NIC/switch/optic refclk、PTP/SyncE 做跨机架日志与调度、数据中心 vPRTC；AWS 自研规模大，供应商更多通过 ODM/模块进入。 |
| Google TPU v7 Ironwood | TPU pod + AI Hypercomputer；Google 自有数据中心和网络。 | 高可靠低功耗 oscillator、PTP/TrueTime/Spanner 类时间体系、跨数据中心 HA timing；Google 内部自研强，外部器件更偏底层 clock。 |
| NVIDIA B200/GB200 | 2026 存量与延续订单，NVL72 机柜。 | 与 GB300 类似，但新增 design-in 弹性低于 GB300。 |
| Huawei Ascend 910C/950 | 国产超节点，光模块/交换/国产服务器配套。 | 国产/日台晶振、低 jitter XO、PTP/SyncE、OCXO/TCXO、测试仪器国产替代；供给约束不在最先进工艺，而在高可靠认证和一致性。 |
| Cambricon MLU 590/690 | 国产 AI 卡和 OAM 集群，规模由国内客户订单驱动。 | OAM/PCIe/Ethernet clock generator、低功耗差分晶振、国产 clock buffer；价格敏感但量可能大。 |
| AMD MI350/MI355 | PCIe/UBB 形态覆盖企业和云端，以太网 scale-out。 | PCIe Gen5/6 clock、Ethernet/UALink 生态同步、PTP time appliance；企业客户更愿采购标准化 timing 模块。 |
| AWS Trainium3 | 3nm UltraServer，144 芯片 scale-up。 | rack 内同步精度提高，SmartNIC/EFA 和 PTP/SyncE 的价值上升；2027 放量强。 |
| Meta MTIA 300/400/450/500 | Meta OCP rack、自研 ASIC、Broadcom XPU/Ethernet 生态，>1GW 首期。 | OCP Time Appliance、SPTP/PTP、low-jitter Ethernet clock、Broadcom switch/SerDes clock；Meta 会推动开放 profile 与服务器 time card。 |
| Microsoft Maia 200 | 3nm、216GB HBM3E、Azure 闭环液冷。 | Azure/OpenAI 推理集群需要时间戳、日志、调度一致性；服务器 timing module + NIC hardware timestamping 机会高。 |
| OpenAI/Broadcom custom ASIC | 2026H2 起步，10GW 长周期。 | AI factory 网络规模极大，PTP/SyncE/HA-TT、1.6T optics、CPO/SerDes clock 均有超预期空间。 |
| AMD MI400/MI455X Helios | 2026H2 首批，HBM4、72 GPU rack、UALink/Ethernet。 | PCIe/UALink/Ethernet Gen6/7 设计导入，2027 高端 clock tree 与 PTP 默认化。 |

### 4.1 技术成熟与放量时间表

| 技术路径 | 2026 成熟度 | 基准放量 | 乐观放量 | 极度超预期放量 | 备注 |
|---|---|---|---|---|---|
| 低 jitter 差分石英 XO/SPXO | 成熟，已量产 | 2026 全年随 800G/AI switch 放量 | 2026H2 随 1.6T optics 加速 | 2026Q2-Q4 若 1.6T/102.4T switch 超预期 | Kyocera 30fs X 系列 2026 已扩产，Epson/NDK/TXC/Murata 同步受益。 |
| MEMS oscillator / Super-TCXO | 高端导入，SiTime 最强 | 2026H2 小批，2027 放量 | 2026Q4 被高端 GPU rack 采用，2027 大规模 | 2026Q3 起随 Elite 2 被头部客户快速拉货 | 抗震、温漂、数字调谐、尺寸优势明显，价格更高。 |
| BAW integrated clocks | 新产品导入 | 2027 通信/数据中心扩量 | 2026H2 进入 1.6T/224G 设计 | 2026 就被部分头部 switch/optics 采用 | Skyworks BAW clock 是关键观察点。 |
| PCIe Gen5/6 clock generator/buffer | 成熟 | 2026 服务器/retimer/SSD/AI switch 主力 | 2026H2 跟 PCIe 6 switch/AEC 放量 | 2026 Gen6 成为开放 AI rack 常见 BOM | 100MHz refclk、low additive jitter、LP-HCSL 是核心。 |
| PCIe Gen7 clock generator/buffer | 样品/design-in | 2027 design-in，2028 量产 | 2027 首批 AI switch/storage 平台收入 | 2026H2 订单先体现，2027 小规模量产 | Diodes sub-30fs、Microchip <50fs、Skyworks Gen7 buffers 已进入竞争。 |
| SyncE/PTP DPLL/SMU | 成熟 | 2026 网络设备与 time appliance 稳增 | 2026H2 AI colo/neocloud 开始标配 | 2026 起成为高端 AI cluster RFP 要求 | Renesas 82P33813、Microchip、Skyworks、TI、ADI 均有路线。 |
| PTP grandmaster/time card/vPRTC | 成熟但数据中心渗透提升中 | 2026-2027 渗透率上升 | 2026H2 大型 neocloud/colo 拉动 | 2026 主权 AI/金融/AI cloud 把 PTP 作为默认配置 | OCP TAP、Meta SPTP、Microchip TP4500/MD 模块是核心线索。 |
| HA-TT / terrestrial time / GNSS-resilient timing | 早期产品化 | 2027 关键基础设施和跨 DC 增长 | 2026H2 大客户试点 | 2026 大型 AI factory 要求 GNSS-free redundancy | Microchip TP4500 v3 5ns/800km 是标志。 |
| Optical/femtosecond timing distribution / White Rabbit-like DC timing | 研究/试点 | 2028+ | 2027 试点，2028 放量 | 2027 就在特定 AI/HPC/跨楼宇场景出收入 | 2026 OCP TAP 已讨论 femtosecond precision optical frequency/timing。 |

### 4.2 2026 最可能的技术路径

2026 最可能赚钱的不是最前沿的 femtosecond optical timing，而是四条务实路径：

1. **224G/1.6T 网络低抖动参考时钟。** 以 17-50fs 指标、156.25/312.5/625MHz、LVDS/LVPECL/HCSL/CML、2.0x1.6 到 8x8mm 封装为主。
2. **PCIe Gen6 clock tree，Gen7 先做 design win。** Gen6 在 AI 服务器、retimer、switch、SSD、CXL 上收入更确定；Gen7 2026 主要体现为样品、认证和平台锁定。
3. **PTP/SyncE 同步模块和 time appliance。** 从 hyperscaler 自研 time card 向 colo、neocloud、vRAN、主权 AI 扩散。
4. **MEMS/BAW 替代高端 quartz 的局部突破。** 不是全面替代，而是在抗震、温漂、尺寸、数字调谐、可靠性、系统级整合要求高的 AI rack 优先替代。

## 5. 已开始放量的关键产品：市场规模、渗透率、毛利率

口径：这里的“未来 3 个月”为 2026-05 至 2026-08 可确认收入/订单池；“一年”为 2026-05 至 2027-05；“两年”为 2026-05 至 2028-05。数字为 AI 数据中心与高端网络直接相关收入池，不是全行业 timing TAM。

### 5.1 市场规模与渗透率路径

| 已放量产品 | 主要供应商 | 未来3个月 基准/乐观/极度乐观 | 未来1年 基准/乐观/极度乐观 | 未来2年 基准/乐观/极度乐观 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 差分低 jitter 石英 XO/SPXO，100/125/156.25/312.5/625MHz | Epson、Kyocera、NDK、TXC、Murata、Daishinku/KDS、Rakon、Abracon、CTS、Siward | $120-220M / $180-320M / $280-480M | $550-900M / $850M-1.35B / $1.2-2.0B | $900M-1.6B / $1.5-2.8B / $2.5-4.5B | 800G/1.6T optics/switch attach 2026 65-85%，2027 75-90%；高端 30-50fs 产品占比从 15-25% 升到 35-55%。 |
| MEMS oscillator / precision TCXO | SiTime、Microchip、Abracon、Murata、Epson 部分 MEMS/programmable | $35-80M / $70-140M / $120-240M | $220-420M / $400-750M / $700M-1.2B | $450M-900M / $900M-1.8B / $1.6-3.2B | AI 服务器和网络高端 timing 渗透 2026 8-15%，2027 15-30%，2028 25-45%。 |
| PCIe Gen5/6 clock generator、buffer、mux | Microchip、Renesas/SiTime、Skyworks、Diodes、TI、Onsemi、NXP、IDT legacy | $70-150M / $120-240M / $200-380M | $350-650M / $600M-1.1B / $900M-1.7B | $650M-1.25B / $1.1-2.1B / $1.8-3.2B | AI server PCIe Gen5/6 attach 2026 55-75%，2027 65-85%；Gen6 份额 2026 10-20%，2027 25-45%。 |
| 224G Ethernet / SyncE jitter attenuator 和 network synchronizer | Skyworks、Renesas/SiTime、TI、Microchip、ADI、MaxLinear 部分 | $90-180M / $150-300M / $250-450M | $420-800M / $700M-1.25B / $1.1-2.0B | $800M-1.6B / $1.4-2.8B / $2.4-4.6B | 800G/1.6T switch/transport attach 2026 40-65%，2027 60-80%；DPLL/SMU 在 PTP-aware 设备中接近必配。 |
| PTP grandmaster、time card、server timing module | Microchip、Adtran Oscilloquartz、Meinberg、Safran/Orolia、EndRun、Net Insight、Meta/OCP 生态、NVIDIA/Mellanox NIC 生态 | $35-100M / $70-170M / $140-300M | $220-520M / $420-900M / $800M-1.6B | $500M-1.3B / $1.0-2.4B / $2.0-4.8B | 大型 AI DC PTP/NTP appliance 渗透 2026 20-40%，2027 45-70%，2028 60-85%；colo/neocloud 上升最快。 |
| PTP-capable Ethernet PHY/NIC 时间戳与安全同步功能 | Microchip、Intel、NVIDIA/Mellanox、Broadcom、Marvell、AMD Pensando、Napatech、Exablaze/Cisco | $40-110M / $80-190M / $150-320M | $240-600M / $480M-1.1B / $900M-2.0B | $550M-1.4B / $1.1-2.7B / $2.2-5.2B | 高端 NIC/DPU hardware timestamp 2026 45-65%，2027 60-80%，2028 75-90%；PTP 精度要求上升带来 ASP。 |

### 5.2 增长预测与毛利率

| 已放量产品 | 2026-2027 增长 基准 | 乐观 | 极度乐观 | 当前/未来毛利率判断 |
|---|---:|---:|---:|---|
| 差分低 jitter 石英 XO/SPXO | +25-45% | +50-80% | +90-140% | 普通晶振 20-35%；AI 低 jitter 35-55%；供不应求和认证绑定下头部可到 50-60%。 |
| MEMS oscillator / TCXO | +55-85% | +90-140% | +160-250% | SiTime 2026Q1 GAAP GM 59%；高端 MEMS/TCXO 可 55-70%，系统级 clock tree 后有 65-75% 空间。 |
| PCIe Gen5/6 clocks | +35-60% | +70-110% | +120-180% | Clock IC/analog mixed-signal 45-65%；高端 Gen6/7 和低功耗 LP-HCSL 55-70%。 |
| Ethernet/SyncE jitter cleaner/SMU | +40-70% | +80-130% | +150-220% | DPLL/SMU/jitter cleaner 50-70%；客户认证后价格粘性高，极端供需紧时 70%+。 |
| PTP grandmaster/time module | +55-90% | +100-180% | +220-350% | 硬件 appliance 40-60%；模块+软件+校准服务 55-75%；time observability 软件可 75-85%。 |
| PTP PHY/NIC timestamping | +45-75% | +90-160% | +180-300% | PHY/NIC 芯片整体 45-65%；增量 PTP/MACsec/SyncE 功能由于嵌入 SoC，价值捕获取决于整芯片议价。 |

## 6. 在研/即将快速增长的关键产品与技术

### 6.1 产品路线与市场规模

| 在研/早期放量技术 | 代表进展 | 未来3个月 基准/乐观/极度乐观 | 未来1年 基准/乐观/极度乐观 | 未来2年 基准/乐观/极度乐观 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| SiTime Elite 2 / AI GPU synchronization Super-TCXO | 2026-05 sampling，2026Q3 commercial production，1ns 同步精度，2030 累计 $1.5B 市场 | $5-20M / $15-50M / $40-120M | $60-180M / $150-400M / $350-800M | $200-650M / $600M-1.5B / $1.3-3.0B | 2026H2 头部试点 1-5%；2027 10-20%；2028 20-40%。 |
| PCIe Gen7 sub-30/50fs clock generator/buffer | Diodes PI6CG33A06、Microchip ZL3039x/DSC1224、Skyworks Gen7 buffers | $5-30M / $20-80M / $60-180M | $40-180M / $120-450M / $350M-1.0B | $250M-900M / $700M-2.0B / $1.5-4.0B | 2026 design-in；2027 高端 AI/storage/switch 5-15%；2028 15-35%。 |
| BAW integrated clocks / NetSync | Skyworks BAW clocks，17fs SyncE jitter，IEEE 1588 Class C/D | $10-50M / $30-120M / $100-250M | $80-280M / $250-800M / $700M-1.8B | $300M-1.0B / $900M-2.5B / $2.0-5.0B | 2026 通信和早期 DC；2027 1.6T optics/switch 渗透 10-25%；2028 25-45%。 |
| HA-TT/vPRTC/GNSS-resilient terrestrial time | Microchip TP4500 v3，5ns/800km Class A；BlueSky/SkyWire | $20-80M / $60-180M / $150-400M | $150-450M / $400M-1.0B / $900M-2.2B | $450M-1.3B / $1.2-3.0B / $2.8-6.0B | 2026 关键基础设施/金融/colo；2027 主权 AI 和跨园区 15-35%；2028 35-60%。 |
| Optical/femtosecond timing distribution | OCP TAP 2026 已讨论 optical frequency & timing distribution with femtosecond precision | <$10M / $10-40M / $30-120M | $20-120M / $100-400M / $300M-1.2B | $150-600M / $500M-2.0B / $1.5-5.0B | 2026 研究/PoC；2027 HPC/跨楼宇试点；2028 后看 CPO/AI factory 结构。 |
| CPO/optical-aware retimer timing | PCI-SIG 2026 讨论 PCIe over optics、DSP optics、LPO、optical retimer | $5-30M / $20-100M / $80-250M | $60-250M / $200-800M / $700M-2.0B | $300M-1.2B / $1.0-3.5B / $3.0-8.0B | 2026 订单/验证；2027 CPO switch 与 optical PCIe 小量；2028 加速。 |
| Chip-scale atomic clock / rack atomic time card | OCP TAP、Meta Time Card 生态，CSAC 更偏时间源/holdover | $5-25M / $20-80M / $60-180M | $50-200M / $150-600M / $500M-1.5B | $150-700M / $500M-2.0B / $1.5-5.0B | 成本高，2026 只在 time appliance；2027-2028 若每园区多源冗余普及则放量。 |

### 6.2 毛利率预测

| 在研/快速增长技术 | 基准毛利率 | 乐观毛利率 | 极度乐观毛利率 | 为什么能有溢价 |
|---|---:|---:|---:|---|
| Elite 2 / MEMS Super-TCXO | 58-68% | 65-75% | 70-80% | 1ns 同步、抗震/温漂/数字调谐、客户替换成本高；价值按 GPU 利用率而非 BOM 定价。 |
| PCIe Gen7 clock | 50-65% | 60-72% | 68-78% | PCIe 7 128GT/s 设计余量稀缺，认证早期客户愿为低 jitter 和低功耗付费。 |
| BAW integrated clocks | 55-70% | 65-78% | 70-82% | BAW 工艺和 DSPLL/软件一体化，替代外部 XO/VCXO 可降低系统 BOM 和功耗。 |
| HA-TT/vPRTC | 50-68% | 65-78% | 75-85% | 设备+软件+校准+安全服务，且 GNSS-resilient timing 是合规/韧性需求。 |
| Optical/femtosecond timing | 35-60% | 55-75% | 70-85% | 早期硬件成本高；若成为 AI factory 标配，专利、校准算法和服务形成高毛利。 |
| CSAC/time card | 40-60% | 55-70% | 65-80% | 原子钟/OCXO/软件组合贵，客户按可靠 holdover 和审计价值付费。 |

## 7. 供给侧：产能、瓶颈、成本与价格传导

### 7.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/产能特征 |
|---|---|---|---|
| 石英晶体/晶振 | 日本、台湾、中国大陆、美国、欧洲、新西兰 | Epson、Kyocera、NDK、Murata、TXC、Daishinku/KDS、Rakon、Abracon、CTS、Siward、River、Hosonic | 石英切割/研磨/封装/老化/温补；高端低 jitter 依赖高频基模晶体、低噪声振荡 IC、自动化测试。 |
| MEMS resonator/oscillator | 美国设计、德国/台湾/美国 foundry、东南亚封测 | SiTime、Microchip、Murata、Bosch/TSMC/Teledyne 供应链 | MEMS resonator + CMOS analog/PLL + 封装校准；SiTime 依赖 Bosch、TSMC、Teledyne 等 foundry。 |
| BAW clock | 美国设计与 BAW 工艺平台，全球封测 | Skyworks | BAW resonator + DSPLL/MultiSynth，利用 Skyworks 高频 BAW 量产经验。 |
| Clock IC / DPLL / jitter cleaner | 美国、日本、欧洲设计；台湾/成熟节点 foundry；东南亚/中国封测 | Renesas/SiTime、Microchip、Skyworks、TI、ADI、Diodes、Onsemi、NXP、MaxLinear | 多为成熟 CMOS/BCD/BiCMOS/SiGe，不抢 3nm/CoWoS，但需要低噪声模拟设计和高精度测试。 |
| PTP grandmaster/time appliance | 美国、德国、瑞士、以色列、日本 | Microchip、Meinberg、Adtran Oscilloquartz、Safran/Orolia、EndRun、Net Insight、NVIDIA/Meta/OCP 生态 | BOM 包含 GNSS receiver、OCXO/TCXO/CSAC、FPGA/CPU/NIC、PTP software、冗余电源、校准。 |
| 测试/认证 | 美国、欧洲、日本、中国台湾 | Keysight、Rohde & Schwarz、Tektronix、Anritsu、Calnex、Microchip/SiTime/Skyworks 内部实验室 | 相位噪声、jitter、ADEV/TDEV/MTIE、PTP time error、temperature ramp、PCI-SIG compliance 是瓶颈。 |

### 7.2 供给瓶颈

1. **17-30fs 级相位噪声测试产能。** 高端时钟出货不是只看晶圆，必须逐颗/批次验证 jitter、phase noise、温漂和老化，测试时间和仪器成为隐性产能。
2. **高端石英 blank 与封装。** AI 光模块/交换机需要小封装、高频、低功耗、低噪声，传统消费级晶振不能直接替代。
3. **MEMS/BAW 专有工艺。** SiTime 依赖 Bosch/TSMC/Teledyne 等，Skyworks 依赖自身 BAW 能力；供应链不像通用 CMOS 那样可轻易二供。
4. **客户认证与 design-in 周期。** Switch ASIC、NIC/DPU、AI accelerator、optical module、PCIe clock tree 的认证常需 6-18 个月；一旦错过平台窗口，短期无法补单。
5. **PTP/SyncE 工程人才。** 会写 PTP daemon 不够，真正难点是 hardware timestamp、PHY/NIC delay、asymmetry、DPLL loop、holdover、profile、安全和现场校准。
6. **GNSS 韧性与法规/安全。** 大型数据中心必须考虑 jamming/spoofing、国家授时、审计可追溯，对 BlueSky/GNSS firewall、vPRTC、HA-TT 认证要求提高。
7. **封测与可靠性筛选。** AI 数据中心工作温度、振动、长期 uptime 要求高；高端 TCXO/OCXO/MEMS 需要更长老化和温循测试。
8. **客户集中导致产能预定。** 头部 hyperscaler、交换机/光模块大厂可能锁定产能，二线 AI 服务器厂拿货成本上升。

### 7.3 成本结构与毛利决定因素

| 产品 | BOM/单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 普通/中高端石英 XO | 石英 blank 15-30%，振荡 IC 15-25%，陶瓷/金属封装 15-25%，测试/老化 15-30%，物流/良率 5-15%。 | 频率、jitter、温度范围、封装尺寸、长期稳定性、客户认证。 | 大客户年度议价；高端 AI 型号可按性能溢价，低端按成本竞争。 |
| MEMS oscillator/TCXO | MEMS wafer 20-35%，CMOS die 20-35%，封装 10-20%，校准/测试 20-30%。 | MEMS 良率、数字调谐、ADEV/温漂、抗震、尺寸、软件配置工具。 | 以系统可靠性和替代多颗器件的 BOM 节省定价，ASP 高于 quartz。 |
| Clock generator/buffer/jitter cleaner | CMOS/analog die 25-45%，封装 10-15%，测试 20-35%，IP/R&D 摊销 10-25%。 | 输出数量、jitter、DPLL 数量、PCIe/SyncE/PTP profile、功耗、软件工具。 | 进入主板/交换机 reference design 后锁定，价格随平台代际上行。 |
| PTP grandmaster/time module | OCXO/TCXO/CSAC 20-40%，GNSS/FPGA/NIC/CPU 20-35%，电源/机箱 10-20%，软件/校准 20-40%。 | holdover、授时源数量、HA-TT/vPRTC、BlueSky/GNSS 安全、管理软件。 | 按系统可靠性、合规、SLA 和维护合同定价，软件服务带来持续毛利。 |

## 8. 竞争格局与壁垒

### 8.1 市场结构

| 子市场 | 结构判断 | 量化线索 |
|---|---|---|
| 全 timing TAM | 分散但向平台化集中 | SiTime 2027 timing TAM 约 $11B；其收购 Renesas timing 后更接近完整平台。 |
| 石英晶振 | 前五集中度中等，长尾很多 | 第三方报告称 2025 前五 Crystal Oscillator 厂商约 45.3%，Epson 约 10.9%。 |
| 高端 MEMS timing | SiTime 高度领先 | SiTime 2026Q1 收入 $113.6M、同比 +88.3%，MEMS timing 覆盖 400+ 应用。 |
| PCIe/Ethernet clock IC | 头部模拟/混合信号厂商集中 | Microchip、Renesas/SiTime、Skyworks、TI、ADI、Diodes 多家竞争，但高端 Gen6/7 认证门槛高。 |
| PTP grandmaster/time appliance | 专业厂商集中，OCP 开放生态扩大 | Microchip、Meinberg、Adtran Oscilloquartz、Safran/Orolia、EndRun、Net Insight；Meta/OCP/NVIDIA 推开放 time card。 |

### 8.2 壁垒清单：为什么能定价

1. **低 jitter 模拟设计壁垒。** 224G PAM4、PCIe Gen6/7 的 jitter budget 极窄，17-50fs 不是普通模拟 IC 可快速复制；能直接提高 BER/eye margin。
2. **长期可靠性与老化数据。** 数据中心客户要 5-10 年 uptime 和批次一致性；供应商必须积累温漂、老化、震动、封装应力数据。
3. **客户认证与切换成本。** 时钟是全系统 clock tree 起点，换器件意味着重做 SI/PI、EMI、jitter、PTP、compliance；成本远高于器件价格。
4. **软件/配置生态。** ClockBuilder、ClockWorks、TICS Pro、PTP stack、TimePictra 等工具把客户锁在供应商生态里。
5. **标准与 profile 理解。** PCIe、SyncE、IEEE 1588、ITU-T G.826x/G.827x、OCP DC-PTP、telecom power profile、SMPTE/broadcast、金融 MiFID 等 profile 复杂，支持越全越能溢价。
6. **供应链与产能优先级。** Kyocera 月产 200 万颗级扩产、SiTime Bosch/TSMC MEMS 链、Skyworks BAW 链都不是短期可复制。
7. **测试方法壁垒。** 客户愿意为“可证明的 fs jitter/ns time error”付费，Calnex/Keysight/R&S/Tek 等测试体系是高端供应商护城河的一部分。

### 8.3 价值捕获判断

长期最可能拥有高 ROIC/高毛利的是：

1. **MEMS/BAW 高端 timing platform：** 规模小、ASP 高、客户锁定强，SiTime/Skyworks 是最明显代表。
2. **DPLL/SMU/network synchronizer：** 位于 clock tree 和 SyncE/PTP 的核心，既是芯片又带软件，毛利优于普通晶振。
3. **PTP/vPRTC/time observability：** 硬件 + 软件 + 服务 + 合规，客户按 SLA 付费，不按 BOM 付费。
4. **PCIe Gen7/224G clock tree：** 2026-2027 design-in 决定 2028 收入，先发者拿认证和平台位置。

价值捕获较弱的是普通低端晶振和标准 clock buffer：量大但 ASP 低，二供多，客户更容易压价。

## 9. 2026 关键变化：三个拐点

1. **AI 数据中心同步产品化拐点。** SiTime Elite 2、Microchip MD-990-0011-B、OCP TAP/WSTS 议题共同说明：PTP/SyncE/TCXO 从 telecom/finance/power 进入 AI server 和 neocloud。
2. **17-30fs 低 jitter 成为高端网络标配。** 224G SerDes、Tomahawk 6、1.6T optics、PCIe Gen7 design-in 使 50fs 以上产品在最高端 AI 网络中压力增大。
3. **行业集中度上升。** SiTime 收购 Renesas timing 业务后，纯 timing 龙头从 oscillator 扩到 clock tree 和 network synchronization；中小厂若没有高端指标或客户认证，会被挤到低毛利区。

## 10. 2027 关键变化：三个拐点

1. **PTP/SyncE 从“可选功能”变成高端 AI cluster RFP 条款。** 2027 若 Rubin/MI400/Trainium3/TPU8/MTIA/OpenAI ASIC 扩到多园区，客户会要求可观测、可审计、GNSS-resilient 的时间体系。
2. **PCIe Gen7/optical-aware retimer 进入早期收入。** 2026 DevCon/样品锁定后，2027 高端 AI switch、CXL/PCIe fabric、storage backplane 和 optical PCIe 开始小批。
3. **1.6T/CPO/224G 让 timing 价值继续上移。** 当可插拔光模块、CPO、CPC、DSP/LPO 并行，clock recovery、reference clock 和 jitter cleaner 的系统价值提升；clock 厂商更靠近交换芯片/光模块 reference design。

## 11. 头部公司与细分清单

### 11.1 MEMS/BAW/石英振荡器

| 细分 | 公司 |
|---|---|
| MEMS timing | SiTime、Microchip、Murata、Abracon、Epson 部分产品、TXC/Siward 部分 programmable oscillator。 |
| BAW clocks | Skyworks。 |
| 高端石英 XO/SPXO/VCXO/TCXO/OCXO | Epson、Kyocera、NDK、Murata、TXC、Daishinku/KDS、Rakon、Abracon、CTS、Siward、River Eletec、Hosonic、Taitien、IQD、Raltron、Crystek、Connor-Winfield、Bliley、Vectron/Microchip、Wenzel。 |
| CSAC/原子钟/高稳时钟源 | Microchip、Safran/Orolia、Microchip/Symmetricom legacy、Microsemi legacy、Microchip Quantum/cesium portfolio、Microchip SA.45s 生态、AccuBeat、Jackson Labs、EndRun。 |

### 11.2 Clock IC、jitter cleaner、network synchronizer

| 细分 | 公司 |
|---|---|
| PCIe clock generator/buffer/mux | Microchip、Renesas/SiTime、Skyworks、Diodes、TI、Onsemi、NXP、ADI、Pericom legacy/Diodes。 |
| Ethernet/SyncE jitter cleaner/DPLL | Skyworks、Renesas/SiTime、Microchip、TI、ADI、MaxLinear、Diodes、Semtech 部分网络链路器件。 |
| Network synchronizer / SMU | Renesas 82P/8A 系列、Microchip ZL/DSC/SY 系列、Skyworks Si55xx/SKY69xxx、TI LMK5B/LMK5C、ADI AD954x。 |
| Clock design tools | Skyworks ClockBuilder Pro、Microchip ClockWorks、TI TICS Pro、ADI ACE、Renesas Timing Commander/配置工具、SiTime Time Machine/编程生态。 |

### 11.3 PTP/time appliance/系统同步

| 细分 | 公司/组织 |
|---|---|
| PTP grandmaster/time server | Microchip TimeProvider/SyncServer、Meinberg、Adtran Oscilloquartz OSA、Safran/Orolia SecureSync、EndRun Sonoma/Meridian、Net Insight、Elproma、Galleon Systems、Spectracom legacy。 |
| OCP time card/time appliance | Meta/OCP Time Appliance Project、NVIDIA ConnectX/NVIDIA networking、Adtran OSA 5400 TimeCard、Timebeat、Makerfabs/OCP derivative。 |
| NIC/DPU hardware timestamp/PTP | NVIDIA/Mellanox ConnectX/BlueField、Intel Ethernet、Broadcom NetXtreme/Tomahawk ecosystem、Marvell/Pensando、AMD Pensando、Cisco/Exablaze、Napatech、Solarflare/Xilinx legacy。 |
| PTP/SyncE 测试 | Calnex、Keysight、Rohde & Schwarz、Anritsu、Tektronix、Microchip/Skyworks/SiTime apps labs、UNH-IOL。 |

### 11.4 中国/亚洲潜在受益供应链

| 地区 | 公司 |
|---|---|
| 台湾 | TXC、Taitien、Siward、Hosonic、TXC/嘉硕、晶技相关供应链、Unimicron/PCB 配套但非 timing 核心。 |
| 日本 | Epson、Kyocera、NDK、Murata、Daishinku/KDS、River Eletec。 |
| 中国大陆 | 泰晶科技、惠伦晶体、东晶电子、鸿星科技、扬兴科技、成都频岢、晶赛科技、相关 OCXO/授时模块厂商；高端 30fs/PCIe Gen7 仍需追赶。 |
| 新西兰/欧美 | Rakon、Abracon、CTS、Bliley、Wenzel、Connor-Winfield、Crystek、IQD、Raltron。 |

## 12. 投资排序

| 排名 | 子方向 | 2026-2027 投资吸引力 | 原因 |
|---:|---|---|---|
| 1 | MEMS/BAW 高端 timing platform | 极高 | 高毛利、高 ASP、AI 数据中心直接叙事、客户锁定强；SiTime/Skyworks 最典型。 |
| 2 | PCIe Gen6/7 + 224G clock tree | 很高 | 服务器/交换机/SmartNIC/retimer/SSD 全部受益，2026 design-in 决定 2027-2028 收入。 |
| 3 | PTP/SyncE time appliance/vPRTC | 很高 | neocloud、主权 AI、colo、跨园区 AI factory 会把可信时间作为运维和合规底座。 |
| 4 | 高端低 jitter 石英 XO | 高 | 2026 已有 Kyocera 明确扩产；量最大、确定性强，但毛利低于 MEMS/BAW。 |
| 5 | PTP test/compliance 工具 | 高 | 标准复杂且测试难，客户采购滞后但粘性高。 |
| 6 | 普通晶振/普通 clock buffer | 中 | 受益于 AI 服务器量增，但竞争多、价格传导弱。 |

## 13. 风险

1. AI 数据中心 CapEx 或 GPU 交付不及预期，时钟订单随服务器/网络延后。
2. 客户发现 PTP/高端 TCXO 对 GPU 利用率提升不明显，AI synchronization 叙事降温。
3. 高端石英、MEMS、BAW 竞争加剧，价格快速下行。
4. PCIe Gen7/optical PCIe 真正量产时间推迟，2027 收入低于 design-in 热度。
5. SiTime/Renesas 整合进度、客户迁移和债务/股权稀释带来短期波动。
6. 国产替代路线受制于高端测试、可靠性和客户认证，短期难以替代日美欧高端产品。

## 14. 主要来源

| 来源 | 关键信息 |
|---|---|
| [SiTime Q1 2026 results](https://www.sitime.com/de-de/company/newsroom/press-release/sitime-reports-first-quarter-2026-financial-results) | Q1 2026 收入 $113.6M、同比 +88.3%；AI infrastructure 使 precision timing 成为 system-level requirement。 |
| [SiTime Elite 2 Super-TCXO](https://www.sitime.com/de-de/company/newsroom/press-release/sitime-boosts-gpu-utilization-ai-data-centers-elite-2-super-tcxo) | 1ns 同步精度、2030 累计 $1.5B 市场、2026Q3 量产。 |
| [SiTime/Renesas transaction](https://www.renesas.com/en/about/newsroom/sitime-acquire-renesas-timing-business) | $1.5B 现金 + 约 4.13M 股；timing 业务转让。 |
| [Microchip MD-990-0011-B timing module](https://www.microchip.com/en-us/about/news-releases/products/new-plug-in-timing-module-delivers-precise-reliable-synchronization-for-data-centers-and-5g) | 数据中心服务器/5G vRAN 插卡同步模块，与 Intel Xeon 6 SoC 平台配合，支持 GNSS/SyncE/PTP。 |
| [Microchip TimeProvider 4500 v3](https://ir.microchip.com/news-events/press-releases/detail/1341/high-accuracy-time-transfer-solution-provides-sub-nanosecond-time-transfer-up-to-800-km-using-long-haul-optical-networks) | HA-TT、sub-ns、800km、5ns/800km、500ps/node。 |
| [Microchip Optical Ethernet PHY](https://www.microchip.com/en-us/about/news-releases/products/next-generation-of-optical-ethernet-phy-transceivers-deliver-pre) | 10/25G optical PHY 集成 IEEE 1588 PTP 与 MACsec，<1ns 同步。 |
| [Microchip PCIe timing](https://www.microchip.com/en-us/products/clock-and-timing/components/application-specific/pcie-timing) | PCIe Gen1-7 oscillator/clock generator/buffer，ZL3039x <50fs。 |
| [Skyworks 18fs Ethernet/PCIe clocks](https://investors.skyworksinc.com/news-releases/news-release-details/skyworks-unveils-industrys-first-clocks-ethernet-and-pci) | 224G PAM4 18fs、PCIe Gen1-6、AI accelerators/SmartNIC/switches。 |
| [Skyworks BAW clocks](https://investors.skyworksinc.com/news-releases/news-release-details/skyworks-introduces-new-programmable-bulk-acoustic-wave-clocks) | 17fs SyncE jitter、800G/1.2T/1.6T optical/DCI、IEEE 1588 Class C/D。 |
| [Diodes PCIe 7.0 clock](https://www.diodes.com/zh/about/news/press-releases/pcie-7-0-clock-generator-from-diodes-incorporated-delivers-sub-30fs-jitter-for-next-gen-ai-infrastructure) | PI6CG33A06 sub-30fs、PCIe 7.0、AI infrastructure、LP-HCSL 低功耗。 |
| [Kyocera X Series differential clock oscillators](https://www.kyocera.co.jp/newsroom/news/2026/002954.html) | 30fs、2026-01 量产、2026-06 月产 200 万颗、AI server/optical/storage/ADAS。 |
| [TI LMK5B33414](https://www.ti.com/product/LMK5B33414) | 3-DPLL/3-APLL/14-output network synchronizer，47fs，112G/224G PAM4 应用文档。 |
| [Renesas 82P33813 SMU](https://www.renesas.com/en/products/82p33813) | IEEE 1588/PTP 与 SyncE timing references、clock sources、timing paths 管理。 |
| [Epson Timing Devices](https://epson.com/oscillator-timing-devices) | 数据中心、carrier、enterprise networking、IEEE 1588、ultra-low jitter。 |
| [OCP Time Appliance Project](https://www.opencompute.org/wiki/Time_Appliance_Project) | Data Center PTP profile、2026 PTP ns scale/RDMA ML/optical timing 议题。 |
| [WSTS 2026 agenda](https://www.wsts.atis.org/2026-agenda/) | Neoclouds and AI Sovereignty - Timing at the Intersection of Data, Edge, and Trust。 |
| [PCI-SIG Developers Conference 2026 agenda](https://pcisig.com/pci-sig-developers-conference-2026-agenda) | PCIe 6.x/7.0 electrical、PCIe 7 over optics、AI infrastructure、PCIe 8 panel。 |
| [Broadcom Tomahawk 6](https://investors.broadcom.com/news-releases/news-release-details/broadcom-now-shipping-worlds-first-1024-tbps-switch-production) | 102.4Tbps production volume shipping，512x200G/1024x100G SerDes。 |
| [SiTime investor presentation](https://investor.sitime.com/static-files/a915b385-a26d-40c8-a51e-b95e7c2b9454) | 2027 timing TAM 约 $11B。 |
| [GMI crystal oscillator market](https://www.gminsights.com/industry-analysis/crystal-oscillator-market) | 2026 crystal oscillator 约 $3.3B；2025 前五份额约 45.3%。 |
| [ITU-T G.8271.1/Y.1366.1 Amd.2](https://www.itu.int/rec/dologin_pub.asp?id=T-REC-G.8271.1-202401-I%21Amd2%21PDF-E&lang=e&type=items) | HA-TT Class A 5ns、Class B 1ns、800km reference chain 等标准依据。 |
# 行业调研：【片上SRAM、MRAM与近存计算】

> 版本日期：2026-05-08  
> 研究口径：本报告聚焦片上 SRAM、嵌入式/独立 MRAM、RRAM/ReRAM、SRAM/DRAM/HBM 近存与存内计算、CXL-PNM/PIM，以及它们在 2026-2027 AI 计算中心、推理 ASIC、边缘 AI、汽车/工业 SoC 中的投资价值。  
> 重要说明：片上 SRAM 通常不单独销售，市场规模用“AI 芯片可归因价值”估算；MRAM/RRAM/CIM 则尽量用可销售芯片、IP 授权、foundry option、模块/系统收入估算。全文数字为产业研究假设，不是投资建议。

## 0. 高密度结论

1. **2026 最确定的技术路线不是“MRAM 取代 SRAM”，而是 SRAM 继续被 AI 芯片当作最关键的片内数据搬运资产。** Microsoft Maia 200 官方披露 **272MB on-chip SRAM**、Google TPU 8i 披露 **384MB Vmem SRAM**、TPU 8t 披露 **128MB SRAM**；NVIDIA Vera Rubin POD 则把 **SRAM-only Groq LPU** 与 HBM-rich Rubin GPU 配对，说明“高带宽片上 SRAM + 大容量 HBM/DRAM/SSD 分层”已经成为 agentic inference 的公开路线。
2. **片上 SRAM 的投资机会主要被 AI ASIC/GPU 设计者、foundry/IP/EDA、先进封装、测试与电源/散热链条捕获，而不是传统独立存储公司。** SRAM 是 die area 和良率税：以 TSMC N2 公开级别 SRAM bitcell 估算，真实宏密度扣除外围后约 **20-40Mb/mm²**；384MB SRAM 等价约 **77-154mm²** 的高价值先进逻辑面积，足以改变 AI ASIC 的 die size、良率和 ASP。
3. **MRAM 在 2026 的现实商业化在汽车、工业、国防、边缘 AI 的 eNVM/持久存储，不在云端 AI 主计算阵列。** TSMC 2025 年报披露 **16MRAM 通过车规 qualification**；GF 22FDX eMRAM 已进入生产、GF 22FDX+ RRAM 计划 2026 量产；Everspin 2026Q1 产品收入 **$14.1M**、毛利率 **52.7%**，并推出 UNISYST 128Mb-2Gb MRAM，样品预计 2026Q4。
4. **RRAM/ReRAM 比 MRAM 更像“AI 权重存储/低功耗边缘 AI”的期权。** TSMC N12e RRAM、22RRAM 在 2025 通过消费级/高耐久 qualification；GF 22FDX+ RRAM 指向 wireless MCU 和 AI IoT；Weebit 2026 年披露与 TI 授权、客户 tape-out。2026 是设计导入，2027-2028 才可能看到较大产品收入。
5. **近存计算的第一波放量更可能来自“SRAM-heavy/digital CIM 推理卡”和“CXL/DRAM/HBM 分层”，而不是经典模拟 ReRAM 大阵列。** d-Matrix Corsair 公开规格为单 rack **128GB performance memory @ 9.6PB/s**；GSI Gemini-II、EnCharge charge-domain IMC、Samsung HBM-PIM/CXL-PNM、UPMEM/Qualcomm 都是方向，但主流云端 2026 仍会优先采用可编程、可验证、可维护的数字方案。
6. **大胆乐观主线：2026-2027 agentic AI 会把 KV cache、采样、routing、RAG/vector search、long-context decode 变成比训练更大的数据搬运问题。** 这会把“SRAM 容量、片上集合通信、近存 KV cache、CXL memory pool、AI-native storage”重估为 AI 基建核心瓶颈。

## 1. 2026 AI 计算中心机遇、挑战与主流技术路径

### 1.1 机遇：AI 基建从 FLOPS 转向 Memory Locality

2026 年 AI 基础设施的增量来自三类 workload：

- **Reasoning / agentic inference**：多步推理、工具调用、代码执行、RAG、长上下文，核心瓶颈是 KV cache、采样同步、低尾延迟和 tokens/W。
- **Post-training / RL / synthetic data**：需要大量短作业、环境沙箱、CPU-GPU/ASIC 协同，要求片上 SRAM、NoC、DMA 和 scale-up 网络减少 idle。
- **多模态/视频/世界模型**：视频 token 与状态缓存暴涨，HBM 容量、片上 SRAM、SSD/AI-native storage 共同承压。

这解释了为什么 2026 的头部芯片都在公开强调内存结构，而不是只说 FLOPS：

| 一手事实 | 对 SRAM/MRAM/近存计算的含义 |
|---|---|
| Microsoft Maia 200：TSMC 3nm、216GB HBM3e、7TB/s、**272MB on-chip SRAM**、750W、>140B transistor，并称提升 token generation economics。来源：[Microsoft](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/) | Hyperscaler 自研推理 ASIC 开始把 SRAM 规模作为可公开卖点；SRAM + DMA + NoC 是 token throughput 的核心。 |
| Google TPU 8i：**384MB on-chip SRAM**、288GB HBM、8.6TB/s HBM 带宽；TPU 8t：128MB SRAM、216GB HBM；TPU 8i 用 CAE 和 Boardfly 降低 all-to-all latency。来源：[Google Cloud TPU 8 deep dive](https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive?e=48754805) | 训练和推理硬件正式分叉：推理芯片需要更多 SRAM 放 KV cache，训练芯片需要 embedding/SparseCore 和超大 torus/fabric。 |
| NVIDIA Vera Rubin POD：把 Rubin GPU 的大 HBM 容量与 **SRAM-only Groq LPU** 配对；LPX rack 256 LPU/rack；Spectrum-6 CPO 102.4Tb/s。来源：[NVIDIA developer blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | SRAM-only/低延迟推理加速器从“异类”被纳入 NVIDIA rack-scale 体系，说明低延迟 decode 是独立价值层。 |
| d-Matrix Corsair：Digital In-Memory Compute，单 rack 128GB performance memory @ 9.6PB/s；Llama3 70B 单 rack 30k tokens/s @ 2ms/token latency。来源：[d-Matrix product](https://www.d-matrix.ai/product/) | SRAM-based DIMC 已经面向数据中心推理做成 PCIe/rack 产品形态，是 2026 最接近商业化的 CIM 路径之一。 |
| AWS Trn3 UltraServer：144 Trainium3、20.7TB HBM3e、706TB/s aggregate memory bandwidth、NeuronSwitch-v1；Trainium4 2027 提升 FP4、内存带宽和 HBM 容量。来源：[AWS Trn3](https://aws.amazon.com/ec2/instance-types/trn3/) | 自研 ASIC 的竞争焦点是“每 MW 输出 token”和系统级 HBM/scale-up 带宽，而不是单芯片峰值。 |

### 1.2 挑战：SRAM 贵、MRAM 慢、CIM 难、软件比晶体管更难

1. **SRAM 面积不按逻辑等比例缩小**：先进节点逻辑密度继续上升，但 SRAM scaling 明显慢于 logic，导致大 SRAM 变成 die cost、良率和热设计问题。  
2. **片上 SRAM 不能解决容量问题**：384MB 对 KV cache 很大，但相比 HBM 的 216-288GB 仍小三个数量级；最优架构是 SRAM/HBM/DRAM/CXL/SSD 分层，而不是单层替代。
3. **MRAM 写入能耗/速度/密度三角仍限制主存化**：STT-MRAM 适合 eNVM、快速 OTA、持久日志、配置和部分 cache；要取代 SRAM，需要 SOT-MRAM/VC-MRAM 更成熟，时间更偏 2028+。
4. **模拟 CIM 的精度、温漂、ADC/DAC、校准和编译器门槛高**：ISSCC 2026 指标惊艳，但量产 SoC 要跨过 variation、yield、model drift、软件生态和安全认证。
5. **客户认证周期长**：数据中心 AI 芯片要验证 PyTorch/JAX/XLA/编译器、collectives、RAS、安全隔离、液冷、现场可维护性；汽车/工业 MRAM/RRAM 要 AEC-Q100、功能安全、长期 retention。
6. **供应链工序复杂**：MRAM/RRAM 是 BEOL/MTJ/OxRAM 模块，涉及沉积、刻蚀、磁屏蔽、热预算、良率；3D SRAM/DRAM 堆叠涉及 hybrid bonding、TSV、thermal stress、test。

### 1.3 项目内 2026-2027 出货量最大 AI 芯片背景下的技术路径

项目内已有 AI 芯片清单显示，2026-2027 价值和出货权重最高的平台大致是：NVIDIA GB300/B300、AWS Trainium2、Google Ironwood/TPU8、NVIDIA GB200/B200、Huawei Ascend、Cambricon MLU、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200，以及 2027 起放量的 Rubin/MI400/Trainium4/OpenAI-Broadcom ASIC。对应到 SRAM/MRAM/近存计算：

| 平台 | 2026-2027 技术路径 | 对本行业的结论 |
|---|---|---|
| NVIDIA GB300/B300/GB200 | HBM3E + NVLink/NVSwitch + Grace LPDDR + 大片上 cache/scratchpad；系统通过 Dynamo disaggregation、Mission Control 提高推理利用率。 | SRAM 是隐性价值，真正显性放量在 HBM/CoWoS/电源/液冷；CIM 不在主路线。 |
| NVIDIA Vera Rubin + Groq LPX | Rubin GPU HBM4 + Vera CPU + BlueField-4 STX context storage + **SRAM-only LPU** + CPO Spectrum-6。 | 2026 最重要信号：SRAM-only 低延迟推理被纳入主流 rack-scale 架构。 |
| Google TPU v7 Ironwood / TPU 8t / TPU 8i | Ironwood 192GB HBM/7.37TB/s；TPU 8t/8i 分叉，8i 384MB SRAM 放 KV cache。 | “推理专用 SRAM”成为 Google TPU8 的公开 KPI，2027 云端 ASIC 会跟进。 |
| Microsoft Maia 200 | 3nm、216GB HBM3e、**272MB SRAM**、DMA、NoC、Ethernet scale-up。 | 标准以太网 + SRAM-heavy inference ASIC 是云厂自研可复制路线。 |
| AWS Trainium2/3/4 | HBM + NeuronLink/NeuronSwitch；Trainium3 144GB HBM3e/4.9TB/s per chip；Trainium4 2027 更高 FP4、带宽和 HBM 容量。 | 近存重点在 HBM/collectives/scale-up，而不是 MRAM/CIM。 |
| Meta MTIA + Broadcom XPU | Broadcom XPU platform，logic/memory/high-speed I/O tightly coupled；>1GW 起步、多 GW rollout。 | 定制 ASIC 会把 SRAM/NoC/SerDes/IP 价值内化给 Broadcom 和 Meta。 |
| AMD MI350/MI400 | MI350 HBM3E；MI400/Helios 转向 HBM4/UALink/open rack。 | HBM4 与封装是主瓶颈；片上 SRAM/CIM 不是短期投资主线。 |
| Huawei Ascend / Cambricon / Alibaba / Baidu | 先进节点/HBM 受限，靠超节点、互连和软件栈弥补；片上 SRAM/本地 buffer 很关键但工艺受限。 | 国产替代会拉动本土 eNVM、SRAM IP、封装测试，但高端 CIM 短期更难。 |

### 1.4 新技术成熟与放量时间：三情景

| 技术 | 2026 最可能状态 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---|---|---|
| 大容量片上 SRAM / scratchpad / Vmem | 已在 Maia 200、TPU8i、LPU 等成为核心指标 | 2026 全面放量，2027 单芯片 SRAM 容量继续 +50%-200%；作为 AI ASIC 默认架构 | 2027 推理 ASIC 普遍公开 SRAM 容量，SRAM macro/IP 价值重估 | 2027 新一代 ASIC 把 512MB-1GB 级片上/近片 SRAM 作为长上下文卖点 |
| SRAM-based digital CIM / SRAM-only LPU | Groq/d-Matrix/GSI 等开始产品化或验证 | 2026 小批量，2027 数据中心推理渗透 1%-3% | 2027 渗透 3%-8%，进入 hyperscaler 二供/专项 workload | 2027 渗透 10%+ 的低延迟 decode/agent workload，成为独立百亿美元级订单池 |
| 3D stacked SRAM / SRAM chiplet | Fujitsu Monaka 类 CPU 路线、TSMC SoIC 支撑；AI ASIC 仍 NPI | 2026-2027 验证，2028 量产更现实 | 2027H2 在特定 AI ASIC/CPU cache die 小规模导入 | 2027 成为定制 ASIC 高端版本卖点，提前创造 $2B-$5B 订单 |
| eMRAM STT-MRAM | 22/28/16nm 商业化，汽车/工业/edge 为主 | 2026 放量在 MCU/SDV/工业；数据中心仅配置/日志/防掉电 | 2027 汽车 zonal controller、robotics、industrial AI MCU 渗透显著上升 | 2027 被部分 AI edge SoC 作为 code+data persistent memory 标配 |
| SOT-MRAM / VC-MRAM | TSMC 等研究，目标 <2ns、更高密度、更低能耗 | 2028+ 才可能商业导入 | 2027 出现客户 test chip/小批量 IP | 2027 被先进节点 AI/edge chip 宣布为 SRAM-cache 替代候选 |
| RRAM/ReRAM eNVM / ReRAM CIM | TSMC/GF/Weebit 已进入 qualification、tape-out、授权 | 2026 设计导入，2027 低功耗边缘 AI 出货 | 2027 形成 $0.5B-$1.5B 级 IP+foundry+产品收入 | 2027 ReRAM 权重存储/ACiM 被头部 MCU/edge AI 平台采用 |
| DRAM/HBM PIM、CXL-PNM | Samsung HBM-PIM/CXL-PNM、UPMEM/Qualcomm、学术论文密集 | 2026 PoC，2027 小规模 KV/vector/search/IMDB | 2027 部分云厂作为 memory tier 加速功能部署 | 2027 近存向量检索/KV cache offload 形成 $3B-$8B 订单 |

## 2. 已开始放量的关键产品：市场规模、渗透率、利润率

### 2.1 定义

- **3个月**：2026Q2-Q3 附近可确认/交付收入。
- **1年**：2026H2-2027H1。
- **2年**：2026H2-2028H1。
- **渗透率**：按各自可服务市场，不跨口径相加。
- **利润率**：以毛利率为主；foundry/封装用业务毛利或合理估计。

### 2.2 当前已放量产品总表

| 细分 | 当前已经放量/商用产品 | 3个月市场规模 | 1年市场规模 | 2年市场规模 | 渗透率路径 | 毛利率：基准/乐观/极超 |
|---|---|---:|---:|---:|---|---|
| 片上 SRAM in AI ASIC/GPU | Maia 200 272MB SRAM、TPU8i 384MB、TPU8t 128MB、NVIDIA/GPU cache、Groq LPU SRAM-only、Cerebras wafer SRAM | B $1.5-2.5B / O $2.5-4B / X $4-7B 可归因价值 | B $8-14B / O $14-24B / X $25-45B | B $16-32B / O $35-60B / X $70-120B | 高端 AI ASIC/GPU 100%；“>128MB 级 SRAM”在推理 ASIC 从 20%-30% 升至 50%-80% | ASIC/GPU blended 55%-75%；SRAM IP/EDA 75%-90%；foundry capture 55%-67% |
| SRAM-heavy / digital CIM 推理卡 | d-Matrix Corsair、Groq LPU/LPX、GSI Gemini 早期、部分低延迟 ASIC | B $0.05-0.20B / O $0.2-0.5B / X $0.5-1B | B $0.5-1.5B / O $1.5-4B / X $4-9B | B $2-6B / O $6-15B / X $15-35B | 数据中心推理加速器 <1% -> 1%-3% -> 3%-8%；极超可 10%+ | 早期硬件 35%-55%；若绑定云服务/软件 55%-75%；极超 65%+ |
| 嵌入式 STT-MRAM foundry option | TSMC 22ULL/16MRAM、GF 22FDX eMRAM、Samsung 28FDS/14/8 roadmap、NXP S32 16MRAM | B $0.05-0.12B / O $0.12-0.25B / X $0.25-0.45B | B $0.25-0.6B / O $0.6-1.2B / X $1.2-2.5B | B $0.7-1.8B / O $1.8-4B / X $4-8B | advanced MCU/auto eNVM 从 3%-8% 到 10%-25%；极超 35% | Foundry option 35%-60%；IP/license 70%-90%；车规高可靠宏有溢价 |
| 独立 MRAM | Everspin PERSYST/Toggle/STT-MRAM、Avalanche Space Grade MRAM、NVE 等 | B $0.04-0.07B / O $0.07-0.10B / X $0.10-0.15B | B $0.18-0.30B / O $0.30-0.55B / X $0.55-0.9B | B $0.35-0.8B / O $0.8-1.6B / X $1.6-3B | mission-critical NVM 很小，工业/国防/auto 逐步从 <2% 到 5%-10% | Everspin 2026Q1 gross margin 52.7%；高可靠/国防可 55%-70% |
| 嵌入式 RRAM/ReRAM eNVM | TSMC N12e/22RRAM、GF 22FDX+ RRAM、Weebit-TI/DB HiTek/onsemi/SkyWater 生态 | B $0.03-0.08B / O $0.08-0.18B / X $0.18-0.35B | B $0.15-0.45B / O $0.45-1.0B / X $1.0-2.2B | B $0.7-1.8B / O $1.8-4.5B / X $4.5-9B | below-28nm eNVM 从设计导入到 5%-15%；极超 25% | IP/license 70%-90%；foundry 35%-55%；产品公司初期低利润 |
| CXL memory / near-memory tier | Samsung CMM-D、Micron CZ120、Astera Leo、云端 memory pooling | B $0.3-0.6B / O $0.6-1.0B / X $1.0-1.8B | B $1.5-2.8B / O $2.8-5B / X $5-8B | B $3.5-8B / O $8-15B / X $15-30B | AI/IMDB/KV cache 服务器低个位数 -> 5%-15%；极超 20%+ | 模块 30%-50%；控制器/IP 55%-75%；软件池化 70%+ |

### 2.3 已放量产品的利润率判断

- **供不应求程度最高**：高端 AI accelerator、HBM 绑定平台、CXL/内存控制器、SRAM-heavy 推理卡。利润率取决于能否证明 tokens/$ 或 tokens/W，而不是 BOM。
- **短期利润率最稳**：Everspin 等独立 MRAM 高可靠产品，虽然市场小，但客户愿意为 endurance、radiation、persistent logging 支付溢价。
- **foundry 端最强议价**：TSMC/GF/Samsung 的 eMRAM/RRAM option 不是靠单一 IP 赚钱，而是靠“客户锁在某个 process + PDK + qualification”的生命周期定价。
- **SRAM macro/IP 的隐性高 ROIC**：AI ASIC 大客户不会因为几个点 royalty 风险迁移 SRAM/compiler/NoC IP；但 merchant SRAM IP 市场绝对规模远小于 GPU/HBM。

## 3. 在研关键产品与未来高增长方向

### 3.1 在研/试产方向总表

| 技术/产品 | 关键公司 | 2026 证据 | 3个月市场 | 1年市场 | 2年市场 | 放量判断 | 毛利率三情景 |
|---|---|---|---:|---:|---:|---|---|
| 3D stacked SRAM / SRAM chiplet | TSMC SoIC、Fujitsu Monaka、AMD/Intel/云厂 ASIC 生态 | TSMC 2026 Symposium 披露 SoIC、CoWoS 放大；Fujitsu Monaka 公开路线指向 N2 compute + N5 SRAM chiplet | <$0.05B | B $0.1-0.5B / O $0.5-1.5B / X $1.5-3B | B $1-5B / O $5-12B / X $12-25B | 2027H2 进入高端 CPU/ASIC NPI，2028 主放量 | 封装 30%-55%；IP/architecture 60%-85% |
| SOT-MRAM/VC-MRAM cache | TSMC、Samsung、imec、Intel Research、Spin Memory/Numem 生态 | TSMC 公开称探索 SOT/VC-MRAM，目标 <2ns、比 6T-SRAM 更密更省能 | 近 0 | <$0.05B | B $0.1-0.5B / O $0.5-1.5B / X $1.5-5B | 2028+ 主商业窗口；2027 是 test chip/design win | IP 70%-90%；foundry option 40%-60% |
| Charge-domain analog CIM | EnCharge AI | 2025 获 >$100M Series B；公开称 20x TOPS/W、5代 silicon、多 process node | <$0.03B | B $0.1-0.4B / O $0.4-1B / X $1-2B | B $0.8-3B / O $3-8B / X $8-18B | 先 client/edge，再企业推理；云端 2027 前不主流 | 早期 35%-55%；若 IP+software 60%-80% |
| ReRAM analog CIM / 权重存储 | Weebit、TetraMem、Mythic、CrossBar/相关 IP、Samsung/TSMC/GF 生态 | Weebit 2026 H1 收入 A$5.6M、TI license、客户 tape-out；ISSCC 2026 ReRAM CIM 96Mb、50.6-90.2TFLOPS/W | <$0.03B | B $0.1-0.5B / O $0.5-1.2B / X $1.2-3B | B $0.8-2.5B / O $2.5-7B / X $7-15B | 2026 设计导入，2027 边缘/工业/传感器前处理小放量 | IP 70%-90%；芯片初期 30%-55% |
| CXL-PNM / near-memory vector/KV offload | Samsung CXL-PNM、Micron/Samsung/SK hynix CXL、Astera、Rambus、云厂软件 | Samsung 公开 HBM-PIM + CXL-PNM；本地 CXL 报告显示 Samsung 把 CXL 瓶颈归纳为 latency/AI bandwidth/cloud-native software | <$0.05B | B $0.1-0.5B / O $0.5-1.5B / X $1.5-3B | B $1-4B / O $4-10B / X $10-25B | 2027 最可能在 KV cache、vector search、IMDB 先上量 | 控制器/IP 55%-75%；模块 30%-50%；软件 70%+ |
| DRAM-PIM / HBM-PIM | Samsung, SK hynix, UPMEM/Qualcomm, academic ecosystem | UPMEM 团队/技术被 Qualcomm 接收；Samsung HBM-PIM/CXL-PNM 技术公开 | <$0.05B | B $0.1-0.4B / O $0.4-1.2B / X $1.2-2.5B | B $0.8-3B / O $3-8B / X $8-18B | 主流云需 compiler/标准成熟，2027 仍偏专项 | 若绑定内存 SKU，memory 厂毛利可 +3-8pct |
| GSI APU / associative CIM | GSI Technology | 2025 FY26 Q2 revenue $6.44M、gross margin guide 54%-56%；称 Gemini-II 8x memory、10x performance vs Gemini-I | <$0.02B | B $0.05-0.2B / O $0.2-0.6B / X $0.6-1.2B | B $0.3-1B / O $1-3B / X $3-8B | 先 RAG/search/edge/国防，数据中心主流需系统验证 | SRAM 产品 50%+；APU 若成功 55%-75% |

### 3.2 为什么这些方向可能快速增长

1. **成本曲线逼迫专用化**：高端 GPU 一颗绑定 6-12 个 HBM stack，而推理 decode 的热点并不总需要整颗 GPU；SRAM-heavy、CIM、PNM 可以用较低功耗处理采样、KV、RAG、routing。
2. **token 需求弹性大于成本下降**：如果专用推理把单 token 成本降 3x-10x，企业 agent、视频、代码、客服、搜索重构会吃掉节省下来的算力。
3. **软件栈开始补齐**：Google TPU8 支持 JAX/PyTorch，AWS Trainium3 支持 PyTorch/JAX/HF，d-Matrix 推 JetStream 和 runtime；硬件若不能接入主流框架，量产窗口会推迟。
4. **电力约束强化 tokens/W 定价**：AI 数据中心的电力/液冷约束让“每 MW token 输出”成为采购指标，给 CIM/PNM 一个比传统 benchmark 更有利的评价口径。

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区/公司/工艺 | 产能与战略含义 |
|---|---|---|
| 先进逻辑 SRAM | TSMC N3/N2/A16/A14，Samsung SF4/SF2，Intel 18A/14A，SMIC N+2/N+3 | 片上 SRAM 依附逻辑 wafer；AI ASIC 抢先进节点时，SRAM 容量越大，越直接消耗最稀缺 die area。 |
| SRAM IP/EDA/编译器 | Arm physical IP、Cadence、Synopsys、Siemens EDA、Rambus、foundry OIP | 价值在低 Vdd SRAM、compiler-aware memory hierarchy、NoC/DMA、DFT/BIST、package-aware signoff。 |
| eMRAM | TSMC 22ULL/16FFC MRAM、GF 22FDX eMRAM Fab 1 Dresden、Samsung 28FDS/14/8nm eMRAM、Everspin IP/产品 | 以汽车/工业/国防/edge AI 为主，亚洲 foundry + 德国 FD-SOI + 美国独立 MRAM 构成供应。 |
| RRAM/ReRAM | TSMC N12e/22RRAM、GF 22FDX+ RRAM、Weebit + TI/DB HiTek/onsemi/SkyWater、OxRAM 生态 | 2026 进入更多 tape-out 和 small production；BEOL 集成低增量成本是卖点。 |
| SRAM/CIM 推理芯片 | d-Matrix、Groq/NVIDIA、GSI、EnCharge、Mythic/edge AI 生态 | 产能取决于逻辑 wafer、chiplet packaging、PCIe/rack integration 和软件栈，不是存储晶圆产能。 |
| CXL/PNM/PIM | Samsung/Micron/SK hynix CXL memory，Astera/Rambus/Montage 等控制器，UPMEM/Qualcomm，Samsung HBM-PIM/CXL-PNM | 2026 仍是硬件可得、软件未充分成熟；2027 若 KV cache/IMDB 需求更急，会加速部署。 |
| MRAM/RRAM 设备材料 | Applied Materials、Lam Research、TEL、KLA、Canon Anelva、Singulus、Onto、Nova、磁性靶材/MTJ 材料供应商 | 专用沉积、刻蚀、量测、磁屏蔽、可靠性测试是良率瓶颈；小批量高毛利但设备生态不如 CMOS 成熟。 |

### 4.2 关键供给瓶颈

1. **先进节点 SRAM 面积与良率**：SRAM 宏越大，随机缺陷敏感度越高；redundancy/BIST/ECC 增加面积和测试时间。
2. **低 Vdd SRAM 稳定性**：ISSCC 2026 出现 2nm nanosheet 350mV single-rail SRAM，说明低压工作仍是前沿问题；AI edge 与 always-on 需求需要更低漏电。
3. **MRAM MTJ 堆叠与均匀性**：MTJ 尺寸、TMR、写入电流、retention/endurance 分布决定良率；磁性材料与 CMOS BEOL 热预算冲突。
4. **车规/国防认证**：AEC-Q100 Grade 1、IATF 16949、radiation/SEL、10年 retention、solder reflow，会把新技术收入确认推迟 12-24 个月。
5. **CIM 精度与编译器**：模拟 CIM 需要 ADC/DAC、校准、量化感知训练、operator mapping；数字 SRAM CIM 也需要编译器、runtime、memory placement。
6. **3D 堆叠测试与返修**：SRAM/DRAM chiplet stacking 要 KGD、hybrid bonding inspection、thermal stress、post-bond test；坏 die 叠上去会放大损失。
7. **客户软件迁移成本**：GPU 生态强，任何 CIM/PIM 都要证明 PyTorch/JAX/ONNX/vLLM/RAG pipeline 的迁移成本低于节省的电费和 GPU 成本。
8. **人才瓶颈**：能同时懂 SRAM circuit、AI compiler、NoC、封装、电源完整性、模型推理 workload 的团队稀缺。

### 4.3 成本构成与毛利决定因素

| 产品 | 成本构成 | 毛利决定因素 | 价格传导 |
|---|---|---|---|
| 片上 SRAM in AI ASIC | 先进逻辑 wafer 面积、SRAM redundancy/ECC、BIST/DFT、NoC/DMA、EDA/IP、良率损失 | 节点稀缺、die size、良率、客户是否认可 tokens/$ 提升 | 通过 AI ASIC/GPU ASP 传导；SRAM 不单独报价但抬高芯片价值 |
| SRAM-heavy 推理卡 | 逻辑 die/chiplet、SRAM 宏、HBM/DDR/PCIe、PCB、软件栈、系统集成 | 是否进入低延迟推理刚需 workload；软件可迁移性 | 按 tokens/s、latency、tokens/W 定价，供不应求时溢价高 |
| eMRAM | CMOS wafer + MTJ BEOL 模块 + 额外 mask/测试 + 车规认证 | retention/endurance、温度范围、AEC 认证、客户生命周期 | 替代 eFlash/NOR 时按系统 BOM 节省与 OTA 停机时间定价 |
| RRAM/ReRAM | CMOS wafer + BEOL ReRAM/OxRAM 模块 + selector/外围 + IP royalty | below-28nm eNVM 成本优势、权重存储密度、良率 | 按 eFlash 不可扩展的痛点定价；初期 royalty 高、量大后 foundry 议价 |
| CXL/PNM | DRAM、CXL controller、PCB/EDSFF、firmware、orchestration software | 延迟、带宽、RAS、云原生管理、CPU/OS 兼容 | DRAM 价格上涨可直接传导；软件池化可按节省内存采购收费 |
| Analog CIM | 模拟阵列、ADC/DAC、校准电路、软件、封装 | 精度/能效/良率/模型覆盖；是否减少外部 DRAM | 如果能证明确切 tokens/$，可高溢价；否则被 NPU/GPU 价格压制 |

## 5. 竞争格局、壁垒与价值捕获

### 5.1 市场结构

| 市场 | 集中度判断 | 头部玩家 |
|---|---|---|
| 先进 AI 芯片片上 SRAM | 极高，随 AI ASIC/GPU 集中 | NVIDIA、Google、Microsoft、AWS、Broadcom/Meta/OpenAI、AMD、Huawei、Cambricon |
| SRAM IP/EDA/physical design | 高 | Arm、Cadence、Synopsys、Siemens EDA、TSMC OIP/Samsung SAFE、Rambus |
| eMRAM foundry | 中高，工艺平台少 | TSMC、GlobalFoundries、Samsung；NXP 等客户推动车规落地 |
| 独立 MRAM | 高，市场小 | Everspin、Avalanche、NVE、Honeywell/国防高可靠生态 |
| RRAM/ReRAM IP | 中，仍分散 | Weebit Nano、TSMC/GF/Samsung RRAM、CrossBar/Intrinsic/TetraMem/4DS 等 |
| 数据中心 CIM | 中低，仍早期 | d-Matrix、Groq/NVIDIA、GSI、EnCharge、Samsung HBM-PIM、UPMEM/Qualcomm、Mythic 等 |
| CXL/PNM | 中高 | Samsung、Micron、SK hynix、Astera Labs、Rambus、Montage、云厂软件栈 |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 量化指标 | 为什么能定价 |
|---|---|---|
| SRAM 宏密度/低压稳定性 | Mb/mm²、最低 Vdd、read/write fail ppm、ECC overhead | 直接影响 die area、良率、功耗；先进 AI 芯片不会为小折扣冒 PPA 风险。 |
| Memory hierarchy/compiler | SRAM hit rate、HBM traffic reduction、tokens/W、tail latency P99 | 客户买的是 token economics；能减少 HBM/网络访问就能提高 GPU/ASIC 利用率。 |
| 车规/国防认证 | AEC-Q100 Grade 1、10年 retention、radiation LET、DPPM | 认证周期长，design-in 后切换成本极高；可靠性事故成本远超器件价差。 |
| Foundry process lock-in | PDK、IP macro、BIST、qualified stack、客户 tape-out | eMRAM/RRAM 一旦进 SoC PDK，客户迁移相当于重做芯片。 |
| 数据中心软件生态 | PyTorch/JAX/vLLM/ONNX support、kernel library、调度器、observability | 没有软件就没有利用率；有软件的硬件可按节省 GPU capex 分成。 |
| 先进封装/3D stacking | bonding pitch、KGD yield、reticle size、thermal resistance | 片上/近片 SRAM 堆叠必须通过高良率封装；产能稀缺形成价格权。 |
| 供应确定性 | lead time、allocation、long-term supply agreement | AI 基建窗口期里，上电时间比单价更重要；能按期交付者可获得溢价。 |

### 5.3 长期高 ROIC/高毛利最可能在谁手里

1. **AI ASIC/GPU 架构层**：NVIDIA、Google、Microsoft、AWS、Broadcom、AMD 等掌握 workload、compiler 和数据中心部署，能把 SRAM/近存优化转化成 tokens/$。
2. **foundry + process option 层**：TSMC、GF、Samsung 的 eMRAM/RRAM/SoIC/CPO 是平台能力，客户 lock-in 强，ROIC 高于普通成熟制程。
3. **EDA/IP/编译器层**：Cadence、Synopsys、Siemens、Arm、Rambus、专用 CIM compiler，软件毛利高且伴随设计复杂度上升。
4. **高可靠 MRAM 小市场**：Everspin/Avalanche 类产品绝对规模小，但国防、航天、工业客户对可靠性溢价敏感度低。
5. **SRAM-heavy 推理系统胜出者**：若 d-Matrix/Groq/GSI/EnCharge 中有公司进入 hyperscaler 生产路径，早期毛利可接近高端 ASIC；但失败率同样高。

## 6. 2026 关键变化：三个最可能拐点

1. **SRAM 容量从隐性参数变成公开竞争指标**  
   Microsoft Maia 200、Google TPU8i 已经把片上 SRAM 写进官方规格；NVIDIA/Groq 把 SRAM-only LPU 纳入 Vera Rubin POD。2026H2 开始，推理 ASIC 的核心比较会从“FP4 PFLOPS”扩展到“SRAM 容量、KV cache locality、P99 latency”。

2. **eMRAM/RRAM 从技术验证转入商业 tape-out/量产导入**  
   TSMC 16MRAM 车规 qualification、GF 22FDX+ RRAM 2026 量产计划、Weebit-TI license、Everspin UNISYST Q4 2026 samples，意味着 eNVM 替代 eFlash 的商业窗口真正打开。最先受益不是云端，而是汽车 zonal controller、industrial AI MCU、国防/航天、边缘传感。

3. **近存计算从学术论文转向“特定 workload 产品化”**  
   d-Matrix Corsair、Groq LPX、GSI Gemini、Samsung CXL-PNM 共同指向同一个现实：不会有一个通吃 GPU 的 PIM，但会有 decode、KV cache、vector search、embedding lookup、RAG、IMDB 等专项加速收入池。

## 7. 2027 关键变化：三个最可能拐点

1. **推理芯片分叉成为常态**  
   TPU 8t/8i 已经把 training/inference 分叉公开化；2027 Trainium4、Rubin、MI400、Meta/Broadcom、OpenAI/Broadcom ASIC 会继续把 memory hierarchy 和低精度推理专用化。SRAM-heavy inference die 或 near-memory accelerator attach rate 上升。

2. **3D SRAM/DRAM/SoIC 从 CPU/HPC 扩散到 AI ASIC NPI**  
   当单 die SRAM 继续变贵，stacked SRAM chiplet 会成为绕过 SRAM scaling 的重要路径。基准情景下 2027 仍小规模，乐观情景下 2027H2 进入高端 AI ASIC 样机，极超情景下提前形成数十亿美元订单。

3. **CXL/PNM/KV cache 分层从“可选优化”变成长上下文刚需**  
   如果 agentic workload 持续增长，HBM 不可能存下所有可复用上下文。2027 起 CXL memory、AI-native SSD、BlueField/STX 类 context storage、CXL-PNM/vector search offload 会从 PoC 进入 selected production。

## 8. 公司清单：按细分技术尽可能完整覆盖

### 8.1 片上 SRAM / AI ASIC / SRAM-heavy 推理

- **NVIDIA**：GB300/GB200/Rubin、NVLink、BlueField-4 STX、Groq 3 LPX 融入 Vera Rubin POD。
- **Groq / NVIDIA Groq LPX**：SRAM-only LPU、低延迟 token decode、LPX rack。
- **Google TPU / Broadcom 生态**：TPU v7 Ironwood、TPU 8t/8i，TPU 8i 384MB SRAM。
- **Microsoft Maia**：Maia 200，272MB SRAM、TSMC 3nm、Azure SDK。
- **AWS Annapurna Labs**：Trainium2/3/4、NeuronLink/NeuronSwitch、Trainium4 2027。
- **Meta MTIA + Broadcom XPU**：>1GW 起步、多 GW rollout，logic/memory/high-speed I/O co-design。
- **AMD**：MI350/MI400/Helios，HBM3E/HBM4 与 UALink/open rack。
- **Huawei Ascend、Cambricon、Alibaba T-Head、Baidu Kunlun、Biren、Iluvatar、MetaX、Moore Threads、Enflame、Hygon**：国产 AI ASIC/GPU，片上 SRAM/NoC 是系统效率关键。
- **d-Matrix**：Corsair DIMC、JetStream、3DIMC stacked DRAM 路线。
- **Cerebras**：Wafer-scale SRAM-rich 架构，训练/推理系统。
- **GSI Technology**：Gemini APU、associative processing、legacy SRAM + AI APU 转型。
- **EnCharge AI**：charge-domain analog IMC，edge-to-cloud roadmap。
- **Mythic、Rain AI、TetraMem、MemryX、Syntiant、Hailo、Kneron、Ambiq**：更多在边缘 AI/低功耗 NPU/CIM，云端 2026 影响较小。
- **Tenstorrent、SambaNova、Etched、Positron、MatX、Furiosa、Rebellions**：推理/训练 ASIC，部分受益 SRAM/NoC/近存优化。

### 8.2 eMRAM / MRAM

- **TSMC**：22ULL consumer-grade eMRAM mass production；16FFC eMRAM；2025 年报披露 16MRAM 通过车规 qualification；探索 SOT/VC-MRAM。
- **GlobalFoundries**：22FDX eMRAM 生产，Fab 1 Dresden；22FDX+ RRAM 2026 量产计划。
- **Samsung Foundry**：28FDS eMRAM 量产；汽车页面披露 28nm eNVM/eMRAM 与 14/8nm eMRAM 发展。
- **Everspin**：PERSYST、Toggle/STT-MRAM、UNISYST；2026Q1 产品收入 $14.1M、毛利率 52.7%。
- **Avalanche Technology**：space-grade MRAM、radiation-hardened MRAM、高可靠国防航天。
- **NVE Corporation**：MRAM/spintronic sensor 小型高可靠生态。
- **Numem**：NuRAM/SmartMem，定位低漏电、高密度 SRAM/nvRAM 替代 IP。
- **Spin Memory、Crocus、Honeywell/航天高可靠生态、Renesas/NXP 等汽车 MCU 客户**：MRAM 技术或产品导入生态。

### 8.3 RRAM/ReRAM / memristor / ACiM

- **Weebit Nano**：ReRAM IP，TI license、DB HiTek qualification、onsemi test chips、客户 tape-out。
- **TSMC**：N12e RRAM、22RRAM qualification。
- **GlobalFoundries**：22FDX+ RRAM with OxRAM，2026 volume production planned。
- **Samsung**：RRAM/eNVM 研究与 foundry option 生态。
- **CrossBar、Intrinsic Semiconductor、4DS Memory、TetraMem、Panasonic/Adesto/Dialog CBRAM 生态**：ReRAM/CBRAM/IP/analog compute 相关。
- **EMASS + Weebit**：超低功耗 edge AI demonstration。

### 8.4 DRAM/HBM PIM、CXL-PNM、near-memory

- **Samsung Memory**：HBM-PIM、CXL-PNM、CMM-D、HBM4/HBM4E、CXL memory ecosystem。
- **SK hynix**：HBM、高端 DRAM、AiM/GDDR-PIM 相关研究生态。
- **Micron**：HBM4、SOCAMM2、PCIe Gen6 SSD、CZ120 CXL memory。
- **UPMEM / Qualcomm**：DRAM PIM 技术团队与 IP 被 Qualcomm 接收，适合 big data/AI near-data。
- **Astera Labs、Rambus、Montage、Microchip、Broadcom/Marvell**：CXL/PCIe/memory controller/IP。
- **NVIDIA BlueField-4 STX / CMX**：AI-native context memory storage，把 KV cache 当成专用数据层。
- **云厂软件栈**：Google Pathways/JAX/TPU Direct Storage、AWS Neuron/SageMaker HyperPod、Microsoft Azure Maia SDK、Meta/Broadcom MTIA stack。

### 8.5 Foundry、封装、EDA/IP、设备材料

- **Foundry/封装**：TSMC、Samsung、GlobalFoundries、Intel Foundry、SMIC、UMC、Tower、DB HiTek、onsemi、SkyWater、ASE、Amkor、JCET、SPIL。
- **EDA/IP**：Cadence、Synopsys、Siemens EDA、Arm、Rambus、Alphawave Semi、eTopus、proteanTecs、Ansys/Synopsys multiphysics。
- **材料/设备/测试**：ASML、Applied Materials、Lam Research、Tokyo Electron、KLA、Canon Anelva、Singulus、Onto Innovation、Nova、Teradyne、Advantest、FormFactor、Cohu。
- **系统/OEM**：Dell、HPE、Supermicro、Lenovo、Foxconn、Quanta/QCT、Wiwynn、Inventec、Jabil；这些公司决定 SRAM-heavy/CXL/near-memory 加速器能否进入标准服务器。

## 9. 投资价值排序

| 排名 | 子方向 | 投资弹性 | 确定性 | 核心原因 |
|---:|---|---:|---:|---|
| 1 | 片上 SRAM-heavy AI ASIC/GPU 架构与 compiler | 极高 | 高 | 已被 Maia/TPU/NVIDIA 公开验证，直接影响 token economics。 |
| 2 | SRAM-based digital CIM / LPU / 低延迟推理系统 | 极高 | 中 | 小基数、若进入 hyperscaler 二供弹性巨大；软件和客户验证是风险。 |
| 3 | eMRAM/RRAM foundry option | 高 | 中高 | below-28nm eFlash 替代明确，车规/工业生命周期长；云端弹性较弱。 |
| 4 | CXL/PNM/KV cache near-memory layer | 高 | 中 | 长上下文和 memory inflation 推动；2026 收入小，2027 可加速。 |
| 5 | 独立 MRAM 高可靠产品 | 中 | 高 | 市场小但毛利稳，国防/航天/工业需求提升。 |
| 6 | 3D stacked SRAM / SRAM chiplet | 极高 | 中低 | 技术方向明确，但量产窗口偏 2027H2-2028；高端 ASIC 若提前采用会重估。 |
| 7 | Analog/ReRAM CIM | 极高 | 低中 | 指标强但商业化门槛最高；适合作为期权而非基准仓位。 |

## 10. 核心风险

1. **AI capex 放缓或 ROI 审查变严**：SRAM-heavy/CIM 的弹性收入最先被延后。
2. **GPU/HBM 继续垄断推理 economics**：如果 HBM4 供给充足且 GPU 软件效率快速提升，专项 CIM 的窗口会变窄。
3. **MRAM/RRAM 认证慢于预期**：车规/工业 design-in 转收入可能推迟 4-8 个季度。
4. **模拟 CIM 精度和软件问题**：论文 TOPS/W 不能直接等于生产 tokens/$。
5. **foundry 客户集中**：单一车厂、云厂、国防项目变化会导致小公司收入波动。
6. **价格竞争**：CXL module、普通 eNVM option、低端 MRAM 一旦供应增加，毛利会被压缩。

## 11. 重要来源

- Microsoft Maia 200 官方博客：<https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/>
- Google TPU 8t/8i technical deep dive：<https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive?e=48754805>
- Google Ironwood TPU 官方博客：<https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/>
- NVIDIA Vera Rubin POD 技术博客：<https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/>
- NVIDIA Vera Rubin 新闻稿：<https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx>
- NVIDIA GB300 NVL72：<https://www.nvidia.com/en-us/data-center/gb300-nvl72/>
- AWS Trainium3 UltraServers：<https://aws.amazon.com/ec2/instance-types/trn3/>
- AWS Project Rainier：<https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster>
- Anthropic/Amazon 5GW compute agreement：<https://www.anthropic.com/news/anthropic-amazon-compute>
- Broadcom/Meta MTIA partnership：<https://www.globenewswire.com/news-release/2026/04/14/3273998/19933/en/broadcom-announces-extended-partnership-with-meta-to-deploy-technology-to-support-multi-gigawatts-of-meta-s-custom-silicon-mtia.html>
- TSMC 2025 年报技术章节：<https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf>
- TSMC MRAM research page：<https://research.tsmc.com/page/mram/1.html>
- NXP/TSMC 16nm eMRAM：<https://media.nxp.com/node/12966/pdf>
- GlobalFoundries 22FDX eMRAM：<https://gf.com/gf-press-release/globalfoundries-delivers-industrys-first-production-ready-emram-22fdx-platform-iot/>
- GlobalFoundries 22FDX+ RRAM：<https://gf.com/gf-press-release/globalfoundries-announces-availability-of-22fdx-rram-technology-for-wireless-connectivity-and-ai-applications/>
- Samsung eMRAM tech blog：<https://semiconductor.samsung.com/news-events/tech-blog/the-basic-theory-of-emram-a-chip-optimized-for-ai-and-next-generation-automotive-in-the-data-driven-era/>
- Samsung automotive foundry eMRAM roadmap：<https://semiconductor.samsung.com/foundry/application-specific-service/automotive/>
- Everspin 2026Q1 results：<https://www.nasdaq.com/press-release/everspin-reports-unaudited-first-quarter-2026-financial-results-2026-04-29>
- Everspin UNISYST MRAM：<https://www.nasdaq.com/press-release/everspin-launches-new-generation-unified-memory-embedded-systems-2026-03-10>
- Weebit Nano FY26 H1 / TI license：<https://www.weebit-nano.com/news/press-releases/weebit-nano-achieves-record-half-year-revenue-licenses-reram-to-tier-1-texas-instruments/>
- Weebit customer tape-outs：<https://www.weebit-nano.com/news/press-releases/two-weebit-nano-product-customers-tape-out-one-already-demonstrating-a-functional-prototype/>
- d-Matrix Corsair product：<https://www.d-matrix.ai/product/>
- d-Matrix 3DIMC blog：<https://www.d-matrix.ai/going-vertical-why-we-created-a-3d-dram-solution-to-advance-low-latency-ai-inference/>
- EnCharge AI technology：<https://www.enchargeai.com/technology>
- GSI FY2026 Q2 results：<https://ir.gsitechnology.com/news-releases/news-release-details/gsi-technology-inc-announces-second-quarter-fiscal-2026-results/>
- UPMEM：<https://www.upmem.com/>
- Gartner 2026 semiconductor forecast：<https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026>
- Global Market Insights CIM chip market：<https://www.gminsights.com/industry-analysis/compute-in-memory-cim-chip-market>
- 本项目本地会议资料：`conference_update/isscc_2026_ai_ic_soc_research.md`、`conference_update/hpca_2026_conference_update.md`、`conference_update/date_2026_conference_research.md`、`conference_update/cxl_vertical_optimization_2026.md`、`ai_chip_research_2026_2027.md`。
# 行业调研：【企业级SSD与高速存储控制器】

截至日期：2026-05-08  
研究对象：企业级/数据中心 SSD、NVMe/PCIe/CXL 存储控制器、EDSFF 高密度形态、AI-native storage/KV cache/context memory、NVMe-oF/GPU-direct storage、存储 fabric/switch/retimer。  
核心立场：本报告对 2026-2027 AI 计算中心建设采取偏乐观口径；直接数据缺失处用“大胆但标注”的假设，并用一手公司发布、财报、标准组织和多家行业报告做交叉校验。  

## 0. 高浓度结论

1. **企业级 SSD 正从“服务器配套件”升级为 AI Factory 的 context memory 层。** 2024-2025 的主线是 HBM、GPU、光模块；2026 的新变化是长上下文、agentic workflow、RAG、checkpoint、训练数据湖和多模态视频把 NAND/SSD 重新拉进瓶颈清单。NVIDIA 在 2026 年发布 BlueField-4 / Inference Context Memory Storage Platform，称可把 GPU memory 扩展到 AI-native storage，并给出最高 5x token/s、最高 5x 能效改善的系统级目标；这等于把 SSD 从“数据盘”提升为推理系统的一部分。

2. **2026 年最可能放量的技术路径：PCIe Gen5 TLC/QLC eSSD + EDSFF E1.S/E3.S + OCP NVMe + NVMe-oF/GPUDirect Storage；Gen6 是高端 AI 推理/训练的早期放量，不是传统存储的主流替换。** Micron 9650 和 Samsung PM1763 已把 PCIe Gen6 eSSD 拉到 28GB/s 级；但 2026 真实主力仍是 Gen5，因为服务器 CPU/平台、Retimer/线缆、合规和客户认证需要时间。

3. **高容量 QLC 是最大反共识增量。** Solidigm D5-P5336 122.88TB、Kioxia LC9 245.76TB、Micron 6600 ION 245TB、SanDisk UltraQLC 256TB 都指向同一件事：AI 数据湖和 warm tier 正在从 HDD-only/混合阵列转向“QLC SSD + HDD”的分层结构。若 AI storage 在 AI infra 中的占比从 IDC Q4 2025 的约 2.4% 升到 2027 的 4%-6%，就是数百亿美元级别的增量池。

4. **控制器和 fabric 的利润弹性大于整盘。** NAND 是最大成本项，整盘毛利受周期影响；但 PCIe Gen5/Gen6 SSD controller、CXL controller、PCIe/CXL switch、retimer、BlueField/DPU 存储处理器、软件调度层具备 55%-80% 毛利潜力。Astera Labs 2026 Q1 收入 $308.4M，同比 +93%，GAAP gross margin 76.3%，并称 320-lane Scorpio X-Series AI fabric switch 已 shipping，是高速连接/控制 silicon 变成 AI 核心件的强信号。

5. **基准情景下，全球 AI 相关 SSD/HDD/数据存储订单池 2026 约 $25B-$45B，2027 约 $35B-$65B；乐观情景 2026 $35B-$65B，2027 $55B-$95B。** 若只看企业级 SSD 和高速存储控制器，不含 HDD 和完整存储系统，2026 全球可服务市场约 $32B-$52B，2027 约 $48B-$82B，2028 滚动可到 $75B-$130B。

## 1. AI 计算中心建设给行业带来的机会与挑战

### 1.1 机会

| 机会 | 2026 触发因素 | 对 SSD/控制器的影响 |
|---|---|---|
| 长上下文与 agentic inference | 单会话 token、工具调用、检索和中间状态持续膨胀 | KV cache/context memory 需要从 HBM 溢出到 DRAM、CXL、NVMe SSD；高 IOPS、低尾延迟和多 SSD 并行调度价值上升 |
| GPU 利用率提升 | Blackwell/GB300、Trainium、TPU、MTIA 等高价值加速器不能被数据等待拖住 | GPU-direct storage、NVMe-oF、BlueField/STX、storage-aware scheduler 进入 AI rack BOM |
| AI 数据湖扩容 | 训练数据、合成数据、多模态视频、日志和 model registry 爆发 | 122TB-256TB QLC eSSD 与 nearline HDD 同时紧张；QLC SSD 替代部分 warm HDD/TLC |
| 高密 AI 服务器形态 | EDSFF E1.S/E3.S、liquid-cooled rack、无风扇存储舱 | EDSFF、热插拔液冷 SSD、25W+ Gen6 SSD、电源完整性和散热件价值提高 |
| 供应被长期锁定 | WD/SanDisk 等提到客户协议延至 2028/2029，HDD/SSD LTA 拉长 | ASP 和毛利率高位持续；非头部客户拿货难，认证客户议价反而更强 |

### 1.2 挑战

| 挑战 | 为什么卡产业 | 2026-2027 影响 |
|---|---|---|
| NAND wafer 供给与产品组合 | HBM/DRAM 抢资本开支，NAND 厂过去几年扩产谨慎 | 高容量 QLC、企业 TLC 同时涨价；client/consumer SSD 被挤出 |
| PCIe Gen6 平台成熟度 | 64GT/s PAM4、FEC、retimer、channel loss、合规测试都更复杂 | Gen6 先在少数 hyperscaler AI 平台跑，2027 才更广泛 |
| QLC endurance 与尾延迟 | AI 数据湖读多写少适合 QLC，但 checkpoint/ETL/向量库混写会放大 WAF | FDP/ZNS、智能 FTL、写入整形和客户 workload tuning 成为卖点 |
| 客户认证周期 | 企业 SSD 需要 OCP、NVMe、固件、遥测、安全、PLP、thermal、fleet tools 长周期验证 | 新进入者难以迅速放量；头部厂商有定价能力 |
| 价值链口径重叠 | NVIDIA/DPU、存储软件、SSD、服务器 OEM、云客户内部平台会重复计算 | 投资测算必须区分整盘收入、controller IC、系统 attach、软件订阅 |

### 1.3 与 2026-2027 出货最大的 AI 芯片路径的映射

本项目既有 AI 芯片资料显示，2026-2027 初出货/价值权重最高的计算平台包括：NVIDIA B300/GB300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon MLU 590/690、AMD MI350、AWS Trainium3、Meta MTIA 300/400、Microsoft Maia 200，Rubin 和 AMD MI400/Helios 从 2026H2 起进入早期导入。

| AI 平台 | 存储侧关键需求 | 最可能采用的技术路径 |
|---|---|---|
| GB300/B300、GB200 | 长上下文推理、checkpoint、训练数据吞吐、全液冷机柜 | Gen5 TLC eSSD 主力；EDSFF E1.S/E3.S；NVMe-oF；BlueField-4/STX/CMX 2026H2 早期 |
| Rubin/Vera Rubin | Agentic AI、context memory、ConnectX-9/BlueField-4、Spectrum-6 | Gen6 eSSD + CMX/STX；NVMe-oF/RDMA；CXL/内存池 PoC；液冷 SSD |
| Trainium2/3 | Anthropic/Rainier 级训练与推理，EFA/NeuronLink 大集群 | 高容量 QLC 数据湖 + Gen5 TLC checkpoint；云厂自研存储调度 |
| TPU Ironwood/TPU8 | 推理优先，数据湖、embedding/RAG、内部 pod 互连 | 高密 QLC + 自研分布式存储；CXL/内存池小规模验证 |
| MI350/MI400 Helios | 企业 PCIe 到 rack-scale 过渡，ROCm 数据路径优化 | Gen5 TLC/QLC + NVMe-oF；2027 Gen6 attach 上升 |
| MTIA/Maia/自研 ASIC | 稳定 workload、大规模推理、成本敏感 | QLC warm tier、KV cache SSD、CXL memory tier、开放 PCIe/CXL fabric |

### 1.4 新技术成熟与放量时间：三情景

| 技术 | 当前阶段 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---|---|---|
| PCIe Gen5 TLC enterprise SSD | 已大规模出货 | 2026 继续主力，2027 占 AI performance eSSD 收入 55%-65% | 2027 仍因性价比维持 50%+ | Gen6 供应紧张，Gen5 高端盘维持溢价到 2028 |
| 122TB-256TB QLC eSSD | 122TB 已出货，245/256TB 进入 shipping/导入 | 2026H2 AI 数据湖放量，2027 成为 warm tier 标配 | 2026 即被 LTA 锁量，2027 容量 PB 占比 25%-35% | 2027 在部分 AI 数据湖替代 15%-25% warm HDD PB 增量 |
| PCIe Gen6 enterprise SSD | Micron/Samsung 已进入量产/产品页，客户早期 | 2026 小批量高端，2027 AI performance eSSD 收入 15%-25% | 2026H2 头部 AI rack 开始规模采购，2027 30%-40% | 2027 Gen6 因 KV cache 成为高端 inference rack 默认件，>45% |
| EDSFF E1.S/E3.S | AI server 采用上升 | 2026 新 AI 服务器 SSD bay 35%-50%，2027 55%-70% | 2027 70%+ | 液冷 EDSFF 把 U.2/U.3 新设计挤到 20% 以下 |
| BlueField-4/STX/CMX context storage | 2026 官方发布，H2 可用 | 2026H2 早期，2027 5%-12% 高端 inference rack attach | 2027 15%-25% | 2027 大模型服务商默认配置，30%+ |
| CXL memory expansion/pooling | CXL 2.0 pilot，Azure preview 信号 | 2026 pilot，2027 production-limited | 2027 多家云公开 SKU，收入 $3B-$5B | DRAM/HBM 极紧，2027 CXL memory tier 接近 $5B-$8B |
| FDP/ZNS/host-managed SSD | 标准与 hyperscaler 内部采用提升 | 2026 OCP/FDP 在头部客户加速，2027 成为大客户 RFP 条款 | 2027 enterprise QLC 默认支持 | 2027 写放大下降成为 QLC 定价核心卖点 |
| Computational storage/CXL-PNM | PoC/论文/定制项目 | 2026-2027 研发，小收入 | 2027 vector DB/RAG early access | 2027 形成 $1B+ 早期加速器/模组订单 |

## 2. 已开始放量的关键产品：市场规模、渗透率、利润率

口径说明：未来 3 个月为 2026Q2-Q3 附近订单/收入窗口；未来一年为 2026H2-2027H1；未来两年为 2026H2-2028H1 滚动。金额为全球出厂/可服务收入池，包含企业级 SSD 整盘、相关控制器和直接绑定的软件/硬件，不简单等同某一家收入。

### 2.1 分技术产品表

| 已放量产品/技术 | 代表产品/公司 | 关键事实 |
|---|---|---|
| PCIe Gen5 TLC performance eSSD | Micron 9550/7600、Samsung PM9D3a/PM1743、Kioxia CM9、Solidigm D7-PS1010、Phison Pascari X 系列 | Gen5 是 2026 训练/推理热数据主力；Micron 7600 用 G9 NAND，面向 AI 与数据中心 QoS；Kioxia CM9 基于 BiCS FLASH TLC |
| 高容量 QLC eSSD | Solidigm D5-P5336 122.88TB、Kioxia LC9 245.76TB、Micron 6600 ION 245TB、SanDisk UltraQLC 256TB、Samsung BM1743 61.44/122.88TB | Solidigm 称 QLC 可减少 AI storage racks 最高 9:1；Micron 称 245TB 6600 ION 相对 HDD 配置可减少 5.5x racks；Kioxia LC9 支持 2.5-inch 与 EDSFF E3 |
| PCIe Gen6 eSSD | Micron 9650、Samsung PM1763 | Micron 9650 最高 28GB/s sequential read、5.5M random read IOPS；Samsung PM1763 最高约 28.4GB/s read、21GB/s write，瞄准 AI/HPC |
| EDSFF/液冷 SSD | Solidigm D7-PS1010 E1.S liquid-cooled、Micron 9650 E1.S/E3.S、Kioxia LC9 E3 | Solidigm 展示冷板包覆式液冷 E1.S，面向下一代 AI server；Gen6 25W 级 SSD 使热设计成为关键 |
| PCIe Gen5 enterprise SSD controller | Silicon Motion MonTitan SM8366、Microchip Flashtec 4016/5016、Phison enterprise controllers、FADU、InnoGrit、Marvell/Microchip | Microchip Flashtec 4016 >14GB/s、>3M IOPS；5016 为 16-channel high-performance NVMe controller；Silicon Motion 在 GTC 2026 展示面向 NVIDIA AI 生态的 MonTitan |
| NVMe-oF/GPU-direct storage | NVIDIA GPUDirect Storage、BlueField DPU、DDN/Dell/HPE/IBM/NetApp/Pure/VAST/WEKA | BlueField-4/STX 把 NVMe SSD 与 GPU context memory 连接起来；高端 AI 存储平台开始卖“tokens/$”而不是单纯 GB/s |

### 2.2 市场规模与渗透率预测

| 产品/技术 | 未来3个月：基准/乐观/极度乐观 | 未来1年：基准/乐观/极度乐观 | 未来2年：基准/乐观/极度乐观 | 渗透率路径 |
|---|---:|---:|---:|---|
| PCIe Gen5 TLC performance eSSD | $5B-$7B / $7B-$9B / $9B-$12B | $22B-$32B / $30B-$42B / $40B-$55B | $30B-$48B / $45B-$65B / $60B-$85B | 2026 AI performance eSSD 收入 65%-80%；2027 因 Gen6 上升降至 50%-65%，但绝对额继续增 |
| 高容量 QLC eSSD 61-256TB | $1.5B-$3B / $3B-$5B / $5B-$8B | $9B-$16B / $15B-$25B / $24B-$38B | $18B-$36B / $32B-$55B / $50B-$80B | AI warm NVMe PB 占比 2026 8%-15%，2027 18%-30%，2028 30%-45% |
| PCIe Gen6 eSSD | $0.4B-$1B / $1B-$2B / $2B-$4B | $3B-$7B / $7B-$13B / $12B-$22B | $10B-$22B / $22B-$38B / $36B-$60B | 2026 AI performance eSSD 收入 3%-8%；2027 15%-30%；2028 30%-50% |
| EDSFF/液冷 SSD | $0.8B-$1.8B / $1.8B-$3.2B / $3B-$5B | $4B-$8B / $8B-$14B / $13B-$22B | $10B-$22B / $20B-$38B / $35B-$60B | 新 AI 服务器 SSD bay 中 EDSFF 2026 35%-50%，2027 55%-70%，2028 70%+ |
| Enterprise SSD controller IC/固件授权 | $0.8B-$1.4B / $1.3B-$2B / $2B-$3B | $3.8B-$6B / $5.5B-$8.5B / $8B-$12B | $6B-$10B / $10B-$16B / $15B-$24B | 高端 eSSD controller 中 Gen5/6、OCP/FDP/telemetry 支持率 2026 40%-55%，2027 65%-80% |
| AI-native storage / KV cache 平台 | $0.2B-$0.6B / $0.6B-$1.2B / $1B-$2.5B | $2B-$5B / $5B-$10B / $10B-$18B | $8B-$20B / $18B-$38B / $35B-$70B | 高端 inference rack attach 2026 <5%，2027 8%-20%，2028 20%-45% |

### 2.3 利润率预测

| 产品/技术 | 当前毛利率判断 | 未来1年基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|---:|
| PCIe Gen5 TLC eSSD | 30%-50%，头部企业盘高于消费盘 | 32%-48% | 40%-55% | 50%-65% |
| 高容量 QLC eSSD | 25%-45%，受 NAND 成本和良率影响 | 30%-48% | 40%-58% | 50%-68% |
| PCIe Gen6 eSSD | 早期高 ASP，但验证/良率成本高，35%-55% | 38%-55% | 48%-65% | 58%-72% |
| SSD controller IC | 45%-65%，高端可更高 | 50%-65% | 58%-72% | 65%-78% |
| PCIe/CXL switch/retimer/fabric | 60%-76%，Astera 可比口径 70%+ | 65%-75% | 70%-78% | 73%-82% |
| AI storage 软件/调度层 | 60%-85%，但收入常嵌入系统 | 65%-80% | 70%-85% | 75%-88% |

## 3. 在研关键产品与高增长技术

### 3.1 未来快速增长方向

| 在研/早期导入技术 | 代表公司 | 成熟时间 | 放量时间 | 主要风险 |
|---|---|---|---|---|
| PCIe Gen6/Gen7 SSD controller | Micron captive、Samsung captive、Silicon Motion SM8466 路线、FADU、Marvell/Microchip、Phison | Gen6 2026；Gen7 2028 后 | Gen6 2027；Gen7 2029+ | PAM4、FEC、功耗、热、平台 lanes、合规 |
| 512TB 级 QLC/UltraQLC SSD | Samsung roadmap、SanDisk UltraQLC、Kioxia/BiCS、Micron/Solidigm | 2027 样品/早期 | 2028+ | QLC/PLC endurance、封装厚度、32-die stack 良率 |
| CXL memory expansion/pooling | Samsung CMM-D、Micron CZ120、Astera Leo、Montage、XConn、Marvell、Microchip | 2026 pilot | 2027-2028 | 软件/Kubernetes/NUMA/tiering、客户 SLA |
| CXL-PNM / near-memory vector search | Samsung CXL-PNM、学术/FAISS/vector DB 生态 | 2026 PoC | 2027 early access，2028+ 放量 | API 标准化、租户隔离、安全、开发者采用 |
| BlueField-4/STX/CMX context memory storage | NVIDIA、DDN、Dell、HPE、IBM、NetApp、Pure/Everpure、VAST、WEKA、Supermicro | 2026H2 | 2027 | 与现有存储架构集成、成本、软件成熟度 |
| FDP/ZNS/host-managed SSD | Samsung、Meta/OCP、Micron、Solidigm、Kioxia、Linux/NVMe | 2026 成熟 | 2027 大客户标配 | 应用适配、运维工具、数据迁移 |
| SSD-based KV cache 多盘并行 | Swarm 等研究、WEKA/VAST/自研 runtime | 2026 论文/原型 | 2027 小规模 | 尾延迟、随机读放大、SSD 磨损、调度复杂度 |
| Computational storage / SmartSSD 2.0 | ScaleFlux、Samsung、NGD legacy、DPU/FPGA 生态 | 2026-2027 定制 | 2028 选择性 | 过去商业化失败阴影，软件生态不足 |

### 3.2 在研技术市场规模、渗透率、利润率

| 在研技术 | 未来3个月 | 未来1年 | 未来2年 | 渗透率与利润率 |
|---|---:|---:|---:|---|
| Gen6 SSD controller/PHY/IP | $0.2B-$0.5B / $0.5B-$1B / $1B-$2B | $1.5B-$3B / $3B-$5B / $5B-$8B | $4B-$8B / $8B-$14B / $12B-$20B | 2027 Gen6 controller 占高端 performance eSSD 20%-35%；毛利 55%-78% |
| CXL memory/controller/fabric | $0.4B-$0.8B / $0.8B-$1.4B / $1.2B-$2B | $2.2B-$4.5B / $4B-$7B / $6B-$10B | $6B-$12B / $12B-$22B / $20B-$35B | 2027 高内存 AI/IMDB 服务器 3%-8% attach；毛利 controller 65%-78%，模组 35%-60% |
| BlueField/STX/CMX context storage | $0.1B-$0.4B / $0.4B-$0.8B / $0.8B-$1.5B | $1.5B-$4B / $4B-$8B / $8B-$15B | $7B-$18B / $18B-$35B / $35B-$65B | 2027 高端 inference rack 8%-20% attach；软件/DPU 毛利 60%-80%，系统 25%-45% |
| 512TB QLC/UltraQLC SSD | 研发/样品，收入极小 | $0.3B-$1B / $1B-$2B / $2B-$4B | $3B-$8B / $8B-$16B / $15B-$30B | 2028 AI warm SSD PB 5%-15%；早期毛利可 45%-70% |
| CXL-PNM / vector/KV offload | < $0.1B | $0.2B-$0.8B / $0.8B-$2B / $2B-$5B | $1B-$4B / $4B-$10B / $8B-$18B | 若 vLLM/FAISS/vector DB API 成形，2028 高端 RAG 节点 5%-12%；毛利成熟后 55%-75% |
| FDP/ZNS/host-managed SSD 软件价值 | 主要嵌入 SSD ASP | $0.5B-$1.5B / $1.5B-$3B / $3B-$5B | $2B-$5B / $5B-$10B / $8B-$15B | 2027 hyperscaler 新 SSD RFP 50%+ 要求；毛利体现在 ASP premium 和低 WAF |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 关键工艺/能力 |
|---|---|---|---|
| NAND wafer | 韩国、中国西安、日本四日市/北上、新加坡、中国武汉、美国少量 | Samsung、SK hynix/Solidigm、Kioxia/WD/SanDisk、Micron、YMTC | 176L-300L+ 3D NAND、TLC/QLC、BiCS、V-NAND、G9 NAND、Xtacking、32-die stack |
| 企业 SSD 设计/固件 | 美国、韩国、日本、台湾、中国大陆、以色列 | Micron、Samsung、Kioxia、Solidigm、SanDisk、Phison、Silicon Motion、FADU、DapuStor | FTL、LDPC/ECC、QoS、NVMe/OCP、FDP/ZNS、telemetry、安全 |
| SSD controller IC | 台湾、美国、韩国、中国大陆 | Silicon Motion、Phison、Marvell、Microchip、FADU、InnoGrit、Maxio、DapuStor、ScaleFlux | PCIe Gen5/6 PHY、16-channel NAND、LDPC、NVMe 2.0/2.1、OCP 2.5/2.6 |
| 高速 fabric / retimer / CXL | 美国、台湾、以色列、中国大陆 | Astera Labs、Broadcom、Marvell、Microchip、Montage、XConn、Rambus、Cadence、Synopsys | PCIe 5/6/7 PAM4、CXL 2.0/3.x/4.0、retimer、switch、VIP/IP |
| 组装/测试/模组 | 台湾、中国大陆、马来西亚、菲律宾、新加坡、泰国、韩国、日本 | NAND 厂自有、OSAT、ODM/OEM | EDSFF、U.2/U.3、E1.S/E3.S、PLP、电源完整性、热测试、burn-in |
| 系统集成 | 美国、台湾、中国大陆、欧洲、日本 | Dell、HPE、Lenovo、Supermicro、Quanta、Wiwynn、Foxconn、Inventec、Gigabyte、AIC | NVMe-oF、GPU-direct、BlueField/DPU、storage server、AI data platform |

### 4.2 供给瓶颈

1. **高层数 NAND wafer 与 QLC 良率。** 245TB/256TB SSD 需要高密度 NAND、复杂封装和严格筛选，良率/可靠性直接决定有效产能。
2. **Gen6 controller PHY 与功耗。** 64GT/s PAM4、FEC、retimer、信号完整性和 25W 级热设计使 Gen6 eSSD 从样品到量产的时间拉长。
3. **企业固件与客户认证。** Hyperscaler 会测试 QoS、PLP、FDP/ZNS、telemetry、secure erase、坏块、热、5 年 endurance；认证周期经常 6-18 个月。
4. **EDSFF 机械件/热件/连接器。** E1.S/E3.S、液冷冷板、hot-swap blind-mate connector、低损耗背板是高密服务器瓶颈。
5. **PLP 电容、电源与 PCB。** 高容量/高性能盘断电保护和电源完整性更难，PLP 和高 Tg PCB 供应会影响交付。
6. **测试/burn-in 产能。** 企业 SSD 需要长时间老化、全容量写入、温循和数据保持测试，高容量盘测试时间本身就是产能消耗。
7. **存储软件/系统工程人才。** AI storage 需要懂 GPU、RDMA、NVMe、分布式文件/对象、KV cache runtime 的跨域团队，人才稀缺。
8. **长期协议锁量。** 头部云/AI 客户签 LTA 后，二线客户拿不到高容量盘，现货价和交付期被放大。

### 4.3 BOM 与毛利决定因素

| 产品类型 | BOM 粗拆 | 毛利决定因素 |
|---|---|---|
| Gen5 TLC performance eSSD | NAND 50%-65%；controller 5%-10%；DRAM/PLP/PMIC 8%-12%；PCB/连接器/散热 5%-8%；测试/固件/质保 10%-18% | NAND 合约价、QoS、endurance、认证客户、OCP/FDP、交付期 |
| 高容量 QLC eSSD | NAND 65%-78%；controller 3%-7%；DRAM/PLP 5%-9%；机械/散热 4%-7%；测试/质保 8%-15% | QLC 良率、容量 premium、PB/TCO、HDD 替代性、写放大控制 |
| Gen6 eSSD | NAND 45%-60%；Gen6 controller/PHY 8%-15%；retimer/连接/散热 6%-12%；DRAM/PLP 8%-12%；测试/认证 12%-20% | 早期稀缺、平台认证、性能/瓦、液冷/EDSFF、PAM4 合规 |
| SSD controller IC | 晶圆/封装/测试 25%-40%；IP/EDA/NRE 摊销 15%-25%；固件/支持 20%-35%；销售/FAE 10%-15% | 设计胜率、固件锁定、OCP 合规、PCIe PHY、NAND 兼容库 |
| AI-native storage 系统 | SSD 35%-55%；DPU/NIC/switch 10%-25%；服务器/电源/散热 15%-25%；软件 10%-25% | token/s、GPU 利用率、软件粘性、客户集成和服务 |

### 4.4 价格传导机制

| 上游变化 | 传导路径 | 谁最能留住利润 |
|---|---|---|
| NAND contract price 上涨 | SSD ASP 季度重定价，LTA 中设置 price adjuster | 头部 NAND+SSD 一体厂、已认证高容量产品 |
| Gen6 controller 稀缺 | 高端 eSSD 出厂价 premium，客户为抢先上架接受高 ASP | controller 自研厂、merchant controller 龙头 |
| QLC 高容量供不应求 | 以 $/TB 降低但 $/drive、$ /rack、gross profit/drive 提升 | Solidigm/Kioxia/Micron/SanDisk/Samsung |
| AI storage 系统能提升 GPU 利用率 | 按系统价值定价，不按 SSD 成本加成 | NVIDIA/DPU、存储软件平台、集成商 |
| 长交期/LTA | 大客户预付款或 take-or-pay，供应商优先排产 | 有产能和认证资格的头部供应商 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | 集中度判断 | 龙头 |
|---|---|---|
| NAND wafer | CR5 约 90%+ | Samsung、SK hynix/Solidigm、Kioxia/WD/SanDisk、Micron、YMTC |
| 企业级 SSD OEM | CR5 约 75%-85% | Samsung、Micron、Kioxia、Solidigm、SanDisk/WD、SK hynix |
| 高容量 QLC eSSD | CR4 约 70%-85%，且技术路线分化 | Solidigm、Kioxia、Micron、SanDisk、Samsung |
| Enterprise SSD controller merchant | 头部集中但 captive 占比高 | Silicon Motion、Phison、Marvell、Microchip、FADU、InnoGrit、Maxio |
| PCIe/CXL retimer/switch/fabric | 高端 AI fabric 早期集中 | Astera Labs、Broadcom、Marvell、Microchip、Montage、XConn、Credo |
| AI storage software/platform | 分散，客户锁定强 | VAST、WEKA、DDN、Pure/Everpure、NetApp、Dell、HPE、IBM、Nutanix、Hammerspace |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 量化/验证方式 | 为什么能定价 |
|---|---|---|
| NAND 规模与良率 | wafer starts、bits shipped、层数、die yield、QLC endurance | 没有 NAND 产能就无法抢高容量盘；LTA 锁量带来交付溢价 |
| 控制器与固件 | IOPS、QoS P99/P999、WAF、UBER、LDPC correction、FDP/ZNS 支持 | AI workload 不只看峰值，尾延迟和写放大决定 GPU 等待成本 |
| 客户认证 | OCP 版本、hyperscaler qualification、fleet telemetry、failure rate | 一旦进入客户 AVL，切换会触发长周期再认证和数据迁移风险 |
| 形态和热设计 | EDSFF 支持、25W/35W thermal、液冷、hot swap | 高密 AI rack 空间和风量极贵，热设计可直接转化为 rack 价值 |
| 安全与可靠性 | PLP、secure boot、FIPS/TCG、NVMe-MI、远程遥测 | 云客户重视 fleet 级故障和数据安全，愿为低风险供应商付 premium |
| 生态和软件接口 | GPUDirect、NVMe-oF、DOCA、Kubernetes、CSI、Redfish、OCP DCMFM | 能接进 GPU/云原生调度系统的存储更像平台，不像硬件 |
| 长期供货能力 | LTA 年限、预付款、交付准点率、售后 RMA | AI 客户最怕停线，确定性本身可以定价 |

### 5.3 价值捕获：长期高 ROIC/高毛利层

1. **高端控制器/fabric silicon。** SSD controller、PCIe/CXL switch、retimer、DPU/BlueField 类产品资本开支轻，客户认证后生命周期长，毛利可达 60%-80%。
2. **AI storage 软件与调度层。** 若能证明提高 token/s 或 GPU 利用率，定价按系统收益而不是硬件成本，毛利可达 70%+。
3. **头部高容量 QLC SSD。** NAND 仍有周期性，但 2026-2027 供不应求和 LTA 会把高容量盘毛利推高。
4. **单纯 SSD 组装/模组厂 ROIC 较弱。** 若没有 NAND、controller、固件和客户认证，只做代工/贴牌容易被挤压。
5. **完整存储系统厂商 ROIC 分化。** DDN/VAST/WEKA/Pure/NetApp/Dell/HPE 取决于软件 attach、客户留存和是否进入 AI reference architecture。

## 6. 2026 关键变化：三个最可能拐点

1. **PCIe Gen6 eSSD 从发布转向早期量产。** Micron 9650、Samsung PM1763 把 Gen6 性能带到 28GB/s 级；2026 不会全面替换 Gen5，但会在高端 AI 推理、checkpoint、context memory storage 中拿到 premium design win。

2. **QLC 245TB/256TB 进入 AI 数据湖采购清单。** Kioxia LC9、Micron 6600 ION、SanDisk UltraQLC、Solidigm D5-P5336 共同证明超高容量 SSD 不是概念。2026H2 最大变化是客户从评估 $/TB 转向评估 $/rack、W/PB、GPU 旁路数据吞吐和交付确定性。

3. **NVIDIA BlueField-4/STX 让“KV cache storage”产业化。** 这会把存储采购从传统 IT 部门推向 AI infra 架构团队。若 CoreWeave、Oracle、Lambda、Mistral 等早期客户验证顺利，2027 context memory storage 会成为 inference rack 的新 BOM。

## 7. 2027 关键变化：三个最可能拐点

1. **Gen6 eSSD 与 EDSFF/液冷形态开始成为高端 AI rack 默认项。** Rubin、MI400/Helios、TPU8、Trainium3 的平台密度和推理上下文压力会让 25W+ Gen6 E1.S/E3.S 进入更多正式 SKU。

2. **CXL memory tier 与 SSD KV tier 合流。** CXL 不是 HBM 替代品，而是 HBM/DRAM/SSD 之间的 memory semantic tier。2027 如果 Azure CXL preview 走向 GA，且 AWS/GCP/Oracle/Meta 有跟进，CXL controller、memory expander、pooling software 将进入订单化。

3. **供应链从现货周期转为多年 LTA。** SSD/HDD 长协延至 2028/2029 会改变行业利润框架：头部客户锁 supply，头部供应商锁价格/产能，二线客户面对更高价格和更长交期。NAND/SSD 会更像 AI 基础设施 bottleneck asset，而不是传统 PC 周期件。

## 8. 公司与细分技术清单

### 8.1 NAND 与企业级 SSD 龙头

| 公司 | 强项 |
|---|---|
| Samsung | V-NAND、PM1763 Gen6、PM9D3a/PM1743、BM1743 QLC、HBM/DRAM/SSD 全栈、CMX/CXL |
| Micron | 9650 Gen6、6600 ION 245TB、7600/9550、G9 NAND、数据中心收入与毛利弹性强 |
| SK hynix / Solidigm | HBM 龙头 + Solidigm QLC D5-P5336 122TB、D7-PS1010 液冷 SSD |
| Kioxia | BiCS FLASH、CM9、LC9 245.76TB、EDSFF E3 高容量 |
| SanDisk / WD Flash | UltraQLC 256TB、SN670 128TB、Kioxia JV NAND 生态 |
| Western Digital | HDD AI roadmap、40TB UltraSMR qualification、100TB+ HDD 路线、AI-scale cold/warm storage |
| Seagate | HAMR/Mozaic、nearline HDD，AI 数据湖冷层受益 |
| YMTC | Xtacking、国产高层 NAND，国内 AI/云供应链替代 |

### 8.2 SSD controller / storage controller

| 公司 | 强项 |
|---|---|
| Silicon Motion | MonTitan SM8366/SM8466 路线、merchant enterprise SSD controller、NVIDIA AI ecosystem 展示 |
| Phison | Pascari enterprise SSD、控制器和整盘一体化、快速产品化 |
| Microchip | Flashtec NVMe 4016/5016、SmartROC/SmartIOC、企业存储控制历史深 |
| Marvell | Bravera/存储控制器、PCIe/CXL/Ethernet/SerDes，全栈 silicon 能力 |
| FADU | 韩国 enterprise SSD controller，低功耗和 hyperscaler 设计导入 |
| InnoGrit | Rainier/enterprise controller、中国/北美供应链 |
| Maxio | 中国 SSD controller，国产替代 |
| DapuStor | 企业 SSD 与控制器/固件能力，国内 AI 数据中心机会 |
| ScaleFlux | Computational storage、压缩/数据路径加速 |
| Huawei | 存储系统、OceanStor、国产 AI 生态内存储与控制器协同 |

### 8.3 PCIe/CXL fabric、retimer、DPU

| 公司 | 强项 |
|---|---|
| NVIDIA | BlueField-4、DOCA、GPUDirect Storage、STX/CMX、ConnectX-9/Spectrum-X |
| Astera Labs | Aries retimer、Leo CXL controller、Scorpio PCIe/CXL/AI fabric switch，320-lane scale-up |
| Broadcom | PCIe switch、Ethernet/SerDes、custom ASIC 生态 |
| Marvell | PCIe 8.0 SerDes demo、CXL/PCIe/存储/网络协同 |
| Microchip | Switchtec PCIe switch、Flashtec NVMe、storage controller |
| Montage Technology | CXL memory expander/controller、DDR5 interface，中国供应链优势 |
| XConn | CXL switch/fabric 早期公司 |
| Credo | AEC/retimer/SerDes，AI rack 连接受益 |
| Rambus / Cadence / Synopsys | PCIe/CXL/NVMe IP、PHY、VIP、验证工具 |

### 8.4 AI storage software 与系统

| 公司 | 强项 |
|---|---|
| VAST Data | AI data platform、NVIDIA/AI factory 生态、disaggregated shared-everything 架构 |
| WEKA | 高性能并行文件、Augmented Memory Grid、NVMe/GPU 数据路径 |
| DDN | AI/HPC 存储龙头、NVIDIA 生态、Lustre/EXAScaler |
| Pure Storage / Everpure | FlashBlade/AI 存储平台、企业客户基础 |
| NetApp | ONTAP、企业数据管理、NVIDIA STX 生态 |
| Dell / HPE / Lenovo | 服务器+存储+AI rack 一体交付 |
| IBM Storage | GPUDirect/AI data platform、企业/主权客户 |
| Nutanix | 云原生/虚拟化存储，BlueField-4 生态 |
| Hammerspace | Global data orchestration，AI 数据管道 |
| MinIO / Cloudian / Ceph | 对象存储、私有云/主权 AI 数据湖 |
| Supermicro / AIC / QCT | AI storage server 与 EDSFF/BlueField 参考系统 |

## 9. 投资判断与风险

### 9.1 最值得关注的投资方向

1. **Gen6 eSSD controller/PHY/fabric：** 2026 小基数，2027 上台阶，毛利最高。
2. **高容量 QLC eSSD：** 直接受益 AI data lake、RAG、视频和 warm storage；2026-2027 量价齐升概率高。
3. **AI-native context storage：** BlueField/STX/CMX、WEKA/VAST/DDN/Pure 等若被高端 inference rack 标配，收入弹性极大。
4. **CXL memory pooling：** 不是大盘最大，但赔率高；DRAM/HBM 越贵，CXL ROI 越强。
5. **EDSFF/液冷 SSD 供应链：** 连接器、冷板、背板、热插拔机构、测试验证是小而紧的瓶颈环节。

### 9.2 主要风险

| 风险 | 影响 |
|---|---|
| AI 推理 monetization 慢于预期 | KV cache/context storage attach 延后，Gen6 premium 下降 |
| NAND 扩产过快或需求误判 | 2027H2 后 SSD ASP 和毛利率回落 |
| Gen6 平台兼容/合规延迟 | Gen6 eSSD 放量推迟到 2028，Gen5 生命周期拉长 |
| CXL 软件生态不成熟 | CXL 停留在 pilot，controller/switch 收入低于预期 |
| 客户自研/垂直整合 | Hyperscaler 自研存储层可能压低外部系统厂商利润 |
| 出口管制与地缘风险 | 中国 AI 数据中心存储供应链与海外技术路径分化 |

## 10. 关键来源

### 一手公司/标准组织

- Micron 9650 PCIe Gen6 SSD：<https://www.micron.com/products/storage/ssd/data-center-ssd/9650-ssd>
- Micron 6600 ION 245TB SSD shipping：<https://investors.micron.com/news-releases/news-release-details/industry-leading-245tb-micron-6600-ion-data-center-ssd-now>
- Micron FY2026 Q2 results：<https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026>
- Samsung PM1763 Gen6 SSD：<https://semiconductor.samsung.com/ssd/enterprise-ssd/pm1763/>
- Samsung Q1 2026 results：<https://news.samsung.com/ca/samsung-electronics-announces-first-quarter-2026-results>
- Samsung GTC 2026 memory/storage update：<https://news.samsung.com/kr/%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90-gtc%EC%84%9C-hbm4e-%EC%B5%9C%EC%B4%88-%EA%B3%B5%EA%B0%9C%ED%86%A0%ED%84%B8-%EC%86%94%EB%A3%A8%EC%85%98%EC%9C%BC%EB%A1%9C-%EC%97%94%EB%B9%84>
- Kioxia LC9 245.76TB：<https://americas.kioxia.com/en-us/business/news/2025/ssd-20250721-1.html>
- Solidigm D5-P5336：<https://www.solidigm.com/products/data-center/d5/p5336.html>
- Solidigm liquid-cooled D7-PS1010：<https://news.solidigm.com/en-WW/248022-solidigm-develops-one-of-the-world-s-first-liquid-cooled-enterprise-ssds-for-ai-deployments>
- Western Digital AI-era storage roadmap：<https://www.westerndigital.com/company/newsroom/press-releases/2026/2026-02-03-western-digital-accelerates-storage-innovation-for-ai-era>
- SanDisk UltraQLC 256TB：<https://www.sandisk.com/ja-jp/company/newsroom/press-releases/2025/2025-08-05-sandisk-showcases-ultraqlc-technology-platform-with-milestone-enterprise-ssd-capacity-at-fms-2025>
- NVIDIA BlueField-4 AI-native storage：<https://nvidianews.nvidia.com/news/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai>
- NVIDIA Vera Rubin / BlueField-4 STX：<https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx>
- Astera Labs Q1 2026：<https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results>
- Astera Scorpio 320-lane switch：<https://www.asteralabs.com/news/astera-labs-extends-leadership-in-open-ai-scale-up-networking-with-new-320-lane-scorpio-x-series-smart-fabric-switch/>
- Silicon Motion GTC 2026 enterprise SSD controllers：<https://ir.siliconmotion.com/news-releases/news-release-details/silicon-motion-showcases-differentiated-enterprise-ssd/>
- Microchip Flashtec NVMe controllers：<https://www.microchip.com/en-us/products/storage/flashtec-nvme-controllers>
- CXL 4.0 specification：<https://www.businesswire.com/news/home/20251118275848/en/CXL-Consortium-Releases-the-Compute-Express-Link-4.0-Specification-Increasing-Speed-and-Bandwidth>
- PCI-SIG DevCon / PCIe 8.0 draft 0.5：<https://pcisig.com/blog/pcier-80-specification-draft-05-now-available-track-2560-gts-transfer-speeds-2028>

### 行业报告与项目内交叉验证

- IDC AI infrastructure Q4 2025 / 2026 forecast：<https://www.idc.com/resource-center/blog/ai-infrastructure-spending-caps-historic-year-at-90-billion-in-q4-2025-2029-spending-to-eclipse-1-trillion/>
- Tom's Hardware 对 SSD/HDD 长协延长的报道：<https://www.tomshardware.com/pc-components/ssds/crushing-shortages-have-pushed-long-term-supply-agreements-for-ssds-and-hdds-to-record-five-years-large-customers-are-signing-large-contracts>
- 本项目：`ai_chip_research_2026_2027.md`
- 本项目：`AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- 本项目：`conference_update/xcelerated_compute_show_2026_report.md`
- 本项目：`conference_update/pci_sig_devcon_2026_update.md`
- 本项目：`conference_update/cxl_vertical_optimization_2026.md`

非投资建议。本报告用于产业链研究和情景推演，所有市场规模均为估算区间，尤其是自研云基础设施、内部转移价、软件 attach 和系统集成收入存在口径重叠风险。
# 行业调研：【商用AI加速芯片】

截至日期：2026-05-08  
研究口径：本文把“商用 AI 加速芯片”定义为用于数据中心、云厂商、自建 AI 工厂和主权 AI 集群的 GPU、XPU、TPU、Trainium/Inferentia、MTIA/Maia、国产 AI ASIC/GPGPU、专用推理 ASIC，以及与这些加速器强绑定的 HBM、先进封装、scale-up/scale-out 互连、AI 服务器关键芯片级供电和系统集成价值。对 Google TPU、AWS Trainium、Meta MTIA、Microsoft Maia、OpenAI/Broadcom 等自用 ASIC，使用“等效外部采购价/内部转移价”估算，不等同公开销售收入。

## 0. 高浓度结论

### 0.1 一句话判断

2026 年商用 AI 加速芯片最值得押注的主线不是“某一颗 GPU 继续涨价”，而是 **AI 计算中心从训练集群扩张进入推理和 agentic workload 的系统化放量期**。在极度乐观情景下，GPU、hyperscaler ASIC、HBM、CoWoS、1.6T 网络、液冷和高密度供电不是互相挤出，而是同时紧缺。

### 0.2 总盘子预测

| 口径 | 2025/当前锚点 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 基准 | 2027 乐观 | 2027 极度超预期乐观 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 全球 AI 基础设施支出 | IDC：2025 年 $318B，Q4 $89.9B | $487B | $560-650B | $700-830B | $650-760B | $850B-1.0T | $1.1T+ |
| AI 加速器芯片/模块/直接互连内存价值 | 2025 约 $220-270B | $300-360B | $390-470B | $520-650B | $430-520B | $590-720B | $850B-1,050B |
| AI 半导体大口径 | Gartner：2026 AI 半导体约占全球半导体 30% | 约 $396B | $430-520B | $580B+ | $500-650B | $700B+ | $900B+ |
| AI server 出货量 | TrendForce：2026 出货量 +28% 以上 | +28-32% | +35-42% | +50%+ | +25-35% | +40-55% | +65%+ |
| ASIC AI server 出货占比 | TrendForce：2026 约 27.8% | 27-30% | 31-35% | 36-42% | 32-38% | 40-48% | 50%+ |

核心验证点：

- IDC 指出 2025 年全球 AI 基础设施支出 $318B，2026 年预计 $487B，2029 年超过 $1T；Q4 2025 服务器占 AI 基建支出 97.6%，储存仅 2.4%，说明当前仍是加速计算硬件主导。
- Gartner 预计 2026 全球半导体收入超过 $1.3T，AI 半导体约占 30%，且 DRAM/NAND 年度价格分别上升 125%/234%，意味着加速器和内存都在卖方市场。
- TrendForce 2026-05-06 将九大 CSP 2026 CapEx 上修到约 $830B，较 2026 年初 $710B 口径再次上调，说明需求锚继续抬升。
- NVIDIA FY2026 数据中心收入 $193.7B，Q4 数据中心 $62.3B，FY2026 GAAP 毛利率 71.1%；Broadcom FY2026 Q1 AI 收入 $8.4B、同比 +106%，Q2 AI semiconductor 指引 $10.7B，调整后 EBITDA 率 68%；AMD Q1 2026 数据中心收入 $5.8B、同比 +57%，Meta 计划部署最高 6GW AMD Instinct GPU。

### 0.3 2026 最可能的技术路径

1. **NVIDIA Blackwell Ultra/GB300/B300 是 2026 最大确定性主线。** TrendForce 预计 2026 年 Blackwell 在 NVIDIA 高端 GPU 出货中占比从 61% 升至 71%，Rubin 因 HBM4、CX9、功耗和液冷调校下修至 22%。这意味着 2026 的大货仍然是 GB300/B300，而不是 Rubin。
2. **hyperscaler ASIC 从“替代 GPU 的边缘补充”变成第二条主产能线。** Google Ironwood/TPU 8t/8i、AWS Trainium2/3、Microsoft Maia 200、Meta MTIA、OpenAI/Broadcom custom accelerator 同时进入量产或导入窗口。TrendForce 预计 2026 ASIC AI server 出货占比 27.8%，且增速高于 GPU AI server。
3. **推理专用和长上下文架构开始重估。** Google TPU 8i、Microsoft Maia 200、Meta MTIA 400/450/500、NVIDIA/Groq LPX、d-Matrix/Etched/MatX/Rebellions/Furiosa 等都指向低延迟、低 token 成本、KV cache、decode loop 和 agentic inference。
4. **HBM3E 是 2026 主力，HBM4 是 2026 H2 到 2027 的最大弹性。** TrendForce 指出 Samsung、SK hynix、Micron 预计 2026 Q2 前后完成 NVIDIA Rubin HBM4 验证。基准情景下 HBM4 2026 贡献小，乐观情景下 2027 成为 Rubin/MI400/TPU8 的产能闸门。
5. **供给瓶颈从 GPU die 扩散到 CoWoS、HBM、ABF、测试、液冷、供电、光互连和电力上电。** TSMC CoWoS 公开市场估计 2026 年底月产能约 11.5-14 万片、2027 约 17 万片，仍无法让所有高端 GPU/ASIC 同时无限放量。

## 1. 行业机遇、挑战与技术成熟时间

### 1.1 2026 机遇

| 机遇 | 为什么 2026 更强 | 投资含义 |
|---|---|---|
| AI 数据中心 CapEx 再上修 | TrendForce 将九大 CSP 2026 CapEx 估算提高到 $830B；IDC 预测 2026 AI infrastructure $487B | 加速器、HBM、先进封装、网络和电力冷却都有量价支撑 |
| 推理需求从边际 workload 变成核心 workload | Google TPU 8i、Maia 200、MTIA 400/450/500、GB300 均强调 inference/reasoning/token economics | 专用推理 ASIC、GDDR7/HBM、KV cache storage、低延迟互连受益 |
| hyperscaler 自研 ASIC 大规模商业化 | AWS Rainier 近 50 万 Trainium2，Anthropic 目前使用超过 100 万 Trainium2；OpenAI/Broadcom 10GW；Meta/Broadcom 首期 >1GW 线索 | Broadcom、Marvell、Alchip/GUC、TSMC、HBM、SerDes/IP、先进封装价值上移 |
| 主权 AI 和中国国产替代 | 出口限制使中国、海湾、欧洲本地集群需求增加 | Huawei Ascend、Cambricon、Alibaba T-Head、Baidu Kunlun、Biren、Iluvatar 等承接国产需求 |
| 供不应求带来高毛利 | NVIDIA FY2026 毛利率 71.1%，Broadcom 调整后 EBITDA 率 68%，高端 memory 厂商毛利率处于极高景气 | 高壁垒环节 ROIC 和利润率维持时间可能长于传统半导体周期 |

### 1.2 2026 挑战

| 挑战 | 约束方式 | 对行业影响 |
|---|---|---|
| HBM3E/HBM4 供应和良率 | 高端 GPU/ASIC 每颗通常需要 6-12 个 HBM stack，HBM4 验证和良率决定 Rubin/MI400/TPU8 节奏 | 内存涨价传导到 GPU/ASIC ASP，非头部客户被挤出 |
| CoWoS/SoIC/先进封装 | 大尺寸 interposer、HBM KGD、载板良率、热翘曲、测试时间都限制有效产出 | TSMC、OSAT、ABF、高端测试设备获得产能溢价 |
| 机柜上电和液冷 | GB300/Rubin/MI400 进入 100kW 以上整柜时代，500kW/1MW rack 进入路线图 | 真实交付从“芯片发货”变成“园区电力和冷却可上架” |
| 软件生态和模型适配 | CUDA、ROCm、Neuron、XLA/JAX、PyTorch/vLLM/Triton 生态差异决定实际利用率 | 非 NVIDIA 产品放量不能只看芯片规格，需看 workload lock-in |
| 客户 ROI 与融资 | AI capex 前置，但企业 agent 收入、token 价格、GPU 租赁残值仍有不确定性 | 2027-2028 若推理变现低于预期，高端硬件可能出现局部价格压力 |
| 出口管制和地缘政治 | H20/H200、国产替代、主权云采购路径均受政策影响 | 需求不消失，但供应商和地区份额发生迁移 |

### 1.3 2026-2027 出货量最大的 10 款平台和技术路径

说明：该表基于项目已有芯片路线图，不重新外搜“出货量最大 10 款”的排序。按 2026-2027 年初可见出货数量和价值权重综合判断。

| 排名 | 平台/芯片 | 技术路径 | 2026 放量判断 | 2027 放量判断 | 关键约束 |
|---:|---|---|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | TSMC 4NP、双 die/大封装、288GB HBM3E、NVLink/NVL72、全液冷 rack | 2026 最大主力，TrendForce 指 GB300/B300 主导 Blackwell 71% 份额 | 2027 上半年仍大量交付，后续逐步让位 Rubin | HBM3E、CoWoS-L、ABF、液冷、机房上电 |
| 2 | AWS Trainium2 | AWS/Annapurna 自研 ASIC、HBM、NeuronLink/EFA、Project Rainier | Rainier 近 50 万颗，Anthropic 使用超过 100 万颗 Trainium2 | 2027 被 Trainium3 接续，但存量扩容仍大 | 自有云内部消化、Neuron 软件、供应链封闭 |
| 3 | Google TPU v7 Ironwood | 推理优先 TPU、192GB HBM、7.37TB/s、TPU pod/AI Hypercomputer | 2026 Google 自用和 Cloud 外部客户扩容，Anthropic TPU 需求强 | 2027 继续放量并与 TPU8 切换 | Broadcom/TSMC/封装/HBM、Google Cloud 外部销售节奏 |
| 4 | NVIDIA B200/GB200 Blackwell | TSMC 4NP、HBM3E、NVLink 5、NVL72 | 既有订单延续，成本敏感客户继续采购 | 2027 变成存量和低价配置 | 被 GB300 挤占新增份额 |
| 5 | Huawei Ascend 910C/950PR/950DT | SMIC N+2/N+3 级 DUV、多芯片超节点、自研互连、国产 HBM 路线 | 中国国产替代第一梯队，系统级 SuperPoD 弥补单芯差距 | 950/960 上量，主权和国产云需求支撑 | DUV 良率、HBM、软件生态、先进封装 |
| 6 | Cambricon MLU 590/690 | 国产 AI ASIC/GPGPU、SMIC 先进节点、HBM/OAM、MLU-Link | MLU 590 放量，690 可能 2026 H2 小批量 | 2027 若良率和客户验证顺利可接棒 | SMIC 产能、字节等客户集中度、软件栈 |
| 7 | AMD MI350/MI355 | CDNA、HBM3E、PCIe/OAM/UBB、ROCm，企业部署较灵活 | 2026 AMD 最确定放量产品 | 2027 仍服务企业和第二供应源，MI400 接棒高端 | ROCm、HBM、客户集群验证 |
| 8 | AWS Trainium3 | AWS 3nm AI chip、144GB HBM3E、4.9TB/s、144 chip UltraServer | 2026 GA/导入，已有 EC2 Trn3 UltraServer | 2027 主力放量，Trainium4 进入下一代 | 3nm/封装、NeuronSwitch、客户迁移 |
| 9 | Meta MTIA 300/400/450/500 | Broadcom XPU 平台、OCP rack、推理优先、快速迭代 | MTIA 300 已生产，Meta 已部署数十万 MTIA | 400/450/500 支撑 GenAI inference，>1GW 线索推动 | Meta 内部 workload、Broadcom/TSMC 产能 |
| 10 | Microsoft Maia 200 | TSMC 3nm、216GB HBM3E、7TB/s、272MB SRAM、闭环液冷 | 2026 Azure 推理导入 | 2027 扩大内部部署，Copilot/OpenAI/Foundry 需求牵引 | Azure 自用、HBM、系统软件 |

### 1.4 新技术成熟和放量时间表

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 | 2026 最可能性 |
|---|---|---|---|---|
| HBM3E | 2026 全年主力，GB300/MI350/Ironwood/Maia 等大量使用 | 价格维持高位，绑定长期合约 | DRAM 短缺使 HBM3E 溢价继续扩大 | 极高 |
| HBM4 | 2026 Q2 验证，H2 小批量，2027 放量 | 2026 Q4 对 Rubin/MI400/TPU8 贡献明显 | 2027 上半年多平台大规模导入 | 中高，2026 仍偏早期 |
| CoWoS-L/S、SoIC、2.5D | 2026 扩产但仍紧，2027 缓解一部分 | OSAT 外包顺利承接，产能释放快 | 客户预付锁产能，先进封装长期高溢价 | 极高 |
| CoPoS/面板级封装 | 2026-2027 pilot，2028-2029 量产 | 2027 大客户提前验证 | 2028 前进入高端 ASIC/GPU 试产 | 2026 低 |
| 2nm AI compute die | 2026 H2 工程样片/少量，2027 平台导入 | MI400/TPU8/ASIC 更早量产 | 2027 头部客户争抢 2nm，ASP 很高 | 2026 低到中 |
| UALink/开放 scale-up fabric | 2026 design-in，2027 小批量 | 2027 进入 AMD/custom ASIC rack | 2027 侵入部分 proprietary fabric | 2026 中 |
| 800G/1.6T 光模块 | 800G 2026 主力，1.6T H2 早期 | 1.6T 2027 放量 | CPO/OCS 拉动 1.6T 提前爆发 | 高 |
| CPO/硅光 OCS | 2026 pilot，2027 小批量 | 2027 特定超大集群采用 | 2026 订单前置，2027 贡献明显收入 | 2026 中低，期权高 |
| 48V/54V rack power | 2026 高端 rack 默认 | 随 GB300/Rubin/MI400 成标配 | 供电模块成为交付瓶颈，ASP 上行 | 极高 |
| 800VDC/HVDC rack power | 2026 H2 pilot，2027 新建 AI factory 批量 | 2027 高端新建项目 10-20% 采用 | 2027 30%+ 高端新建项目采用 | 2026 中低，2027 高弹性 |
| D2D/UCIe/FCSA chiplet | 2026 以大厂私有 D2D 为主，标准生态成熟 | 2027 被部分 ASIC RFP 引用 | 2028 前出现开放 chiplet catalog | 中 |
| PCIe 6/7 Retimer/Fabric switch | 2026 PCIe 6 放量，PCIe 7 design-in | Gen6/Gen7 成 AI rack 标配 | Fabric switch 从外围件重估为 AI collective 加速器 | 高 |
| CIM/near-memory 推理 | 2026 多为研发/小量 | 2027 专用 edge/推理场景放量 | 2027-2028 若模型稳定可非线性增长 | 低，长周期期权 |

## 2. 已开始放量的关键产品：市场规模、渗透率和利润率

### 2.1 已放量产品分层

| 细分层 | 已放量产品 | 放量证据 |
|---|---|---|
| Merchant GPU/rack | NVIDIA H100/H200、B200/GB200、B300/GB300；AMD MI300/MI350；Intel Gaudi 3 | NVIDIA FY2026 DC $193.7B；TrendForce 指 2026 Blackwell >70% 高端 GPU 份额；AMD Q1 2026 DC $5.8B |
| Hyperscaler 自研 ASIC | AWS Trainium2/3、Google Ironwood TPU、Microsoft Maia 200、Meta MTIA 300 | AWS Rainier 近 50 万 Trainium2，Anthropic 使用 >100 万 Trainium2；Meta 数十万 MTIA；Microsoft Maia 200 发布 |
| 中国国产替代 | Huawei Ascend 910B/910C、Cambricon MLU 590、Alibaba Zhenwu/PPU、Baidu Kunlun P800 | 出口管制和国产云需求推动，部分产品进入十万到数十万级线索 |
| 专用推理和非传统架构 | Groq LPU、Cerebras WSE/CS、SambaNova SN40L、Tenstorrent Wormhole/Blackhole、d-Matrix/Corsair 等早期 | 多数仍小规模，但推理 workload 切分给了商业窗口 |
| 关键使能部件 | HBM3E、CoWoS、ABF、PCIe/CXL Retimer、AI Ethernet switch/NIC、800G 光模块、液冷/供电 | 这些不是“加速器芯片”本体，但决定加速器出货和利润传导 |

### 2.2 已放量产品的三情景预测

口径：未来 3 个月指 2026-05 至 2026-08 附近的产能释放金额；未来 12 个月指 2026-05 至 2027-05；未来 24 个月指 2026-05 至 2028-05。渗透率指对应细分市场中的价值份额或部署份额，非全行业单一口径。

| 产品/技术 | 未来 3 个月规模和渗透率：基准 / 乐观 / 极度乐观 | 未来 12 个月规模和渗透率：基准 / 乐观 / 极度乐观 | 未来 24 个月规模和渗透率：基准 / 乐观 / 极度乐观 | 毛利率/利润率：基准 / 乐观 / 极度乐观 |
|---|---|---|---|---|
| NVIDIA GB200/GB300/B300 Blackwell 系列 | $45-65B、merchant AI GPU 55-60% / $65-85B、60-65% / $85-110B、65-70% | $165-230B、55-63% / $230-310B、60-68% / $310-420B、65-72% | $260-380B、35-45% / $380-550B、40-50% / $550-720B、45-55% | 70-74% / 74-77% / 77-80%，系统级短缺维持溢价 |
| NVIDIA Hopper/H200/H20 存量 | $4-8B、GPU 存量扩容 10-12% / $8-12B / $12-18B | $12-25B / $25-40B / $40-60B | $15-35B / $35-60B / $60-90B | 60-68% / 65-70% / 70%+；中国出口政策影响大 |
| AMD MI350/MI355 | $3-6B、merchant GPU 5-7% / $6-10B、7-9% / $10-15B、9-12% | $15-30B、6-9% / $30-50B、9-12% / $50-75B、12-16% | $30-65B / $65-110B / $110-170B | 48-56% / 56-61% / 61-65%；ROCm 和第二供应源价值提升 |
| AWS Trainium2/3 | $6-12B、hyperscaler ASIC 22-28% / $12-18B、28-33% / $18-28B、33-38% | $35-60B、23-30% / $60-90B、30-36% / $90-130B、36-42% | $80-135B / $135-210B / $210-320B | 内部 TCO 毛利不可比；供应链可得 35-55%，AWS 云服务长期毛利取决于利用率 |
| Google TPU v7 Ironwood | $5-10B、hyperscaler ASIC 18-25% / $10-16B / $16-25B | $30-55B、20-28% / $55-85B、28-34% / $85-120B、34-40% | $70-125B / $125-200B / $200-300B | Broadcom/供应链 45-60% / 55-65% / 60-70%；Google 自用按 token 成本优化 |
| Microsoft Maia 200 | $1-3B、Azure 推理 ASIC 5-8% / $3-5B / $5-8B | $8-18B、8-12% / $18-32B、12-18% / $32-55B、18-25% | $25-60B / $60-100B / $100-150B | 35-50% / 45-58% / 55-65%；内部转移价低于 NVIDIA，但锁定 Azure workload |
| Meta MTIA 300 | $0.5-1.5B、Meta 自研 ASIC 5-8% / $1.5-3B / $3-5B | $3-8B、8-12% / $8-16B、12-18% / $16-28B、18-25% | $12-35B / $35-75B / $75-130B | Broadcom XPU 项目 45-60% / 55-65% / 60-70%；Meta 以 TCO 优先 |
| Huawei Ascend 910B/910C | $3-6B、中国高端 AI 加速 35-45% / $6-10B、45-55% / $10-16B、55-65% | $15-30B / $30-50B / $50-80B | $45-90B / $90-150B / $150-240B | 40-55% / 55-65% / 65%+；国产替代溢价强，但良率成本高 |
| Cambricon MLU 590 | $0.8-2B、中国非华为 AI 加速 10-15% / $2-4B / $4-7B | $4-9B / $9-16B / $16-28B | $10-25B / $25-55B / $55-95B | 35-50% / 50-60% / 60-68%；产能紧张时 ASP 弹性大 |
| Alibaba T-Head Zhenwu/PPU | $0.5-1.5B / $1.5-3B / $3-5B | $3-8B / $8-15B / $15-25B | $10-25B / $25-50B / $50-85B | 35-50% / 50-60% / 60-68%；云内自用，外部可见度较低 |
| Intel Gaudi 3 | $0.1-0.4B / $0.4-0.8B / $0.8-1.5B | $0.5-1.5B / $1.5-3B / $3-5B | $0.8-3B / $3-6B / $6-10B | 20-35% / 35-45% / 45-55%；路线图信心不足压制议价 |
| HBM3E/AI 高端 DRAM | $20-30B / $30-40B / $40-55B | $90-130B / $130-180B / $180-250B | $180-280B / $280-420B / $420-600B | 55-70% / 65-78% / 75-85%；价格强周期但 2026 极紧 |
| PCIe/CXL Retimer/Fabric switch | $1-2B / $2-3B / $3-5B | $5-9B / $9-15B / $15-25B | $15-30B / $30-55B / $55-90B | 60-74% / 70-76% / 74-80%；Astera 类高毛利验证互连芯片重估 |
| AI 800G/1.6T 光模块和网络 ASIC | $8-14B / $14-22B / $22-35B | $45-70B / $70-105B / $105-150B | $110-180B / $180-280B / $280-420B | 光模块 25-40%，网络 ASIC/SerDes 55-75%，CPO/硅光初期更高 |

### 2.3 对已放量产品的增长排序

| 增长确定性 | 方向 | 逻辑 |
|---|---|---|
| S | GB300/B300、HBM3E、CoWoS、800G/1.6T、AI server rack power/liquid cooling | 已进入交付主线，需求和供给都高度可见 |
| S- | Trainium2/3、Ironwood TPU、Maia 200、MTIA 300 | 自用 ASIC 订单可见，但公开收入和外部市场化较弱 |
| A | AMD MI350、Ascend 910C、Cambricon MLU590、Alibaba PPU | 第二供应源和国产替代弹性强，但生态和良率约束更大 |
| B+ | Gaudi 3、Cerebras/SambaNova/Tenstorrent 等 | 有细分客户，但短期难撼动 GPU/大厂 ASIC |
| B | CIM/edge 专用 AI、纯推理小厂 | 可能出现单点爆款，但客户集中和软件风险高 |

## 3. 在研关键产品和快速增长技术

### 3.1 在研和导入期产品清单

| 产品/技术 | 2026-05 阶段 | 关键技术路径 | 最早成熟窗口 | 真实放量窗口 |
|---|---|---|---|---|
| NVIDIA Vera Rubin NVL72 | 已宣布 full production，2026 H2 partner availability | Rubin GPU、Vera CPU、HBM4、NVLink 6、CX9、BlueField-4、Spectrum-6/CPO | 2026 H2 | 2027 全年 |
| NVIDIA Rubin Ultra/Kyber | 设计/工程导入 | HBM4E、NVLink 7、更大 NVLink domain、800VDC/1MW rack 路线 | 2027 H2 | 2028 |
| AMD MI400/MI455X Helios | 2026 H2 目标部署，Meta 首期 1GW custom MI450-based GPU | HBM4、Helios 72 GPU rack、UALink/Open rack、ROCm | 2026 H2 | 2027 |
| AMD MI500 | 预览，2027 路线 | CDNA 6、2nm、HBM4E | 2027 H2 | 2028 |
| Google TPU 8t/8i | 2026 Cloud Next 发布 | 8t 训练，9600 chips superpod、2PB HBM；8i 推理，288GB HBM、384MB SRAM | 2026 H2 | 2027 |
| AWS Trainium4 | 设计阶段 | FP4 6x、FP8 3x、带宽 4x，可能兼容 NVLink Fusion | 2027 | 2028 |
| OpenAI/Broadcom custom accelerator | 官方 10GW 协作，2026 H2 开始部署 | OpenAI 设计 accelerator/system，Broadcom Ethernet/PCIe/optical/connectivity | 2026 H2 小批 | 2027-2029 |
| Meta MTIA 400/450/500 | 2026-2027 分批部署 | GenAI inference-first，OCP/PyTorch/vLLM/Triton 标准生态 | 2026 H2 | 2027 |
| Huawei Ascend 950/960 | 950PR/950DT 路线，国产 HBM/超节点 | 国产先进节点、多芯互连、Atlas SuperPoD/Cluster | 2026 | 2027 |
| Cambricon MLU 690 | 测试/小规模试产 | 国产先进节点、HBM、OAM、MLU-Link | 2026 H2 | 2027 |
| Baidu Kunlun M100/M300 | M100 2026、M300 2027 路线 | 云端推理/训练、Tianchi 超节点 | 2026-2027 | 2027 |
| Intel Jaguar Shores | Falcon Shores 后继 | 系统级 AI rack solution，可能 EMIB/Foveros/HBM4 | 2027 | 2028 |
| Groq 3 LPX/NVIDIA LPX | 2026 H2 可用 | 256 LPU/rack、低延迟 decode、SRAM bandwidth | 2026 H2 | 2027 |
| d-Matrix/Etched/MatX/Rebellions/Furiosa | 试产/客户验证 | 专用 LLM inference、低延迟、低 token cost、GDDR/HBM 分化 | 2026-2027 | 2027-2028 |
| UALink/ESUN/Ethernet scale-up | 标准和 design-in | 200G/800G、memory semantics、in-network compute | 2026 | 2027 |
| CPO/OCS/硅光 | pilot | Spectrum-6/CPO、OCS、400G/lane、1.6T/3.2T | 2026-2027 | 2027-2028 |

### 3.2 在研产品的三情景预测

| 在研产品/技术 | 未来 3 个月规模和渗透率：基准 / 乐观 / 极度 | 未来 12 个月规模和渗透率：基准 / 乐观 / 极度 | 未来 24 个月规模和渗透率：基准 / 乐观 / 极度 | 利润率：基准 / 乐观 / 极度 |
|---|---|---|---|---|
| NVIDIA Vera Rubin NVL72 | $2-5B、新一代 GPU <5% / $5-10B / $10-18B | $35-80B、8-15% / $80-150B、15-25% / $150-250B、25-35% | $180-330B / $330-550B / $550-800B | 70-75% / 75-78% / 78-82% |
| Rubin Ultra/Kyber/800VDC rack | $0 / $0-1B / $1-3B | $2-10B / $10-25B / $25-50B | $40-110B / $110-220B / $220-380B | 72-76% / 76-80% / 80%+，若成为 premium AI factory 标配 |
| AMD MI400/MI455X Helios | $0.5-2B / $2-5B / $5-9B | $10-30B / $30-60B / $60-100B | $55-130B / $130-250B / $250-380B | 50-58% / 58-64% / 64-68% |
| Google TPU 8t/8i | $0-1B / $1-3B / $3-6B | $8-25B / $25-55B / $55-90B | $60-140B / $140-260B / $260-400B | 45-60% / 55-68% / 65-75%，供应链和自用 TCO 双重收益 |
| OpenAI/Broadcom 10GW accelerator | $0.5-2B / $2-5B / $5-10B | $8-25B / $25-55B / $55-95B | $60-140B / $140-300B / $300-500B | Broadcom/IP/网络 55-68% / 65-72% / 70%+ |
| Meta MTIA 400/450/500 | $0.5-2B / $2-5B / $5-9B | $8-22B / $22-50B / $50-85B | $50-110B / $110-220B / $220-350B | 50-62% / 60-70% / 70%+ |
| AWS Trainium4 | $0 / $0-1B / $1-3B | $1-5B / $5-15B / $15-30B | $25-70B / $70-150B / $150-250B | 内部 TCO 优先；供应链 35-55%，若支持 NVLink Fusion 则价值上移 |
| Huawei Ascend 950/960 | $1-4B / $4-9B / $9-16B | $12-30B / $30-60B / $60-100B | $60-130B / $130-250B / $250-420B | 45-60% / 60-70% / 70%+ |
| Cambricon MLU690/Baidu M100/M300 | $0.3-1B / $1-3B / $3-6B | $4-12B / $12-28B / $28-50B | $25-70B / $70-140B / $140-240B | 35-55% / 55-65% / 65-72% |
| Groq 3 LPX/低延迟 LPU | $0.2-1B / $1-3B / $3-6B | $4-12B / $12-25B / $25-45B | $20-55B / $55-120B / $120-220B | 50-65% / 65-75% / 75%+；premium reasoning 若成立，ASP 很强 |
| d-Matrix/Etched/MatX/Rebellions/Furiosa 等专用推理 ASIC | $0.1-0.8B / $0.8-2B / $2-4B | $2-8B / $8-20B / $20-40B | $15-50B / $50-130B / $130-250B | 45-60% / 60-75% / 75%+，但客户集中风险极高 |
| CPO/OCS/硅光 AI 互连 | $0.5-2B / $2-5B / $5-10B | $5-18B / $18-40B / $40-75B | $35-100B / $100-220B / $220-380B | 35-55% / 50-65% / 60-75%，测试和封装良率决定 |
| UALink/PCIe/CXL AI fabric switch | $1-3B / $3-6B / $6-10B | $8-20B / $20-45B / $45-80B | $40-110B / $110-230B / $230-400B | 60-74% / 70-78% / 78-82% |

### 3.3 最可能快速增长的在研方向

1. **Rubin/MI400/TPU8/Trainium3-4 代表的 HBM4 rack-scale 平台。** 2026 H2 是样品和首批，2027 是规模化。
2. **OpenAI/Meta/Anthropic 等模型公司绑定的 custom accelerator。** OpenAI 10GW、Meta >1GW、Anthropic 多云 TPU/Trainium/GPU 组合，正在把 ASIC 需求变成 GW 级项目。
3. **低延迟推理 ASIC 和 LPU。** 如果 agentic inference 的付费 token 和 test-time compute 持续扩大，专用 decode/推理芯片会在 2027 获得窗口。
4. **AI fabric switch、Retimer、CPO/OCS。** GPU/ASIC 越多，互连美元含量越高；PCIe 8.0 draft、UALink、ESUN、1.6T 都指向这一点。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 主要产能结构

| 环节 | 主要地区 | 主要公司 | 关键工艺/资源 | 供给状态 |
|---|---|---|---|---|
| 先进逻辑晶圆 | 台湾、韩国、美国、日本、中国大陆 | TSMC、Samsung Foundry、Intel Foundry、SMIC | 4/5nm、3nm、2nm、N+2/N+3 DUV | TSMC 高端节点最紧，中国国产受设备和良率约束 |
| 先进封装 | 台湾、韩国、美国、东南亚、中国大陆 | TSMC CoWoS/SoIC、ASE/SPIL、Amkor、Samsung AVP、Intel EMIB/Foveros、JCET、Tongfu、Huatian | CoWoS-L/S、2.5D、SoIC、EMIB、F2F、CoPoS | CoWoS 是共同瓶颈，2026 年底月产能约 11.5-14 万片估计仍偏紧 |
| HBM | 韩国、美国、日本配套、台湾封测 | SK hynix、Samsung、Micron | HBM3E、HBM4、TC bonding、base die、KGD | 2026 HBM3E 极紧，HBM4 Q2 验证后仍要爬良率 |
| ABF/高阶基板 | 日本、台湾、奥地利、中国大陆 | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、AT&S、Kyocera、Zhen Ding、Shennan | 大尺寸 ABF、低翘曲、高层数、高速材料 | 大 package 加速器拉高面积和良率门槛 |
| 测试 | 日本、美国、台湾、欧洲 | Advantest、Teradyne、FormFactor、Technoprobe、Chroma、Cohu | HBM tester、wafer probe、KGD、SerDes、burn-in | 测试时间随 HBM/CPO/rack burn-in 增加 |
| 互连网络芯片 | 美国、台湾 | NVIDIA/Mellanox、Broadcom、Marvell、AMD/Pensando、Astera、Credo、Cisco/Acacia | NVLink、Ethernet、PCIe/CXL、SerDes、Retimer、Switch ASIC | AI backend 高端芯片供不应求 |
| 光模块/硅光 | 中国、美国、泰国、马来西亚、台湾 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、Broadcom、Marvell、Fabrinet、Accelink、Source Photonics | 800G、1.6T、CPO、LPO、DSP、硅光、EML/VCSEL | 800G 已放量，1.6T 和 CPO 进入供应链争夺 |
| 电源/VRM | 台湾、中国大陆、美国、日本、欧洲 | Delta、Lite-On、Flex、Murata、Vicor、MPS、Infineon、TI、ADI、Renesas、ST、onsemi | 48V、54V、800VDC、DC/DC、IVR、DrMOS、TLVR | 高密度 AI rack 使 power shelf 和板级 VRM 紧张 |
| 散热 | 美国、欧洲、台湾、中国大陆、日本 | Vertiv、Schneider/Motivair、CoolIT、Asetek、Boyd、Delta、AVC、Nidec、Foxconn、Quanta、Supermicro | 冷板、CDU、manifold、UQD、浸没、漏液检测 | 冷板/液冷交付直接影响 rack 上架 |

### 4.2 供给瓶颈清单

至少 12 条关键瓶颈如下：

1. **HBM stack 产能和良率。** HBM4 需要更复杂 base die、TSV、堆叠和验证，任何一家供应商延迟都会影响 Rubin/MI400/TPU8。
2. **CoWoS/SoIC 产能。** 高端 GPU/ASIC 共享 TSMC 先进封装，CoWoS-L/S 产能扩张仍慢于需求。
3. **ABF 基板面积和良率。** GB300/Rubin/MI400 等大 package 对翘曲、阻抗、热膨胀和层数要求更高。
4. **先进节点排产。** TSMC 3nm/2nm 被 NVIDIA、AMD、Google/Broadcom、Microsoft、Apple 等争抢；中国国产依赖 DUV 多重曝光，良率和周期压力大。
5. **SerDes/Retimer/Fabric switch 验证。** PCIe 6/7、800G/1.6T、UALink、CXL、NVLink/NVSwitch 都需要复杂合规和系统级验证。
6. **光模块和 CPO 测试。** 1.6T、CPO、硅光的热、光、电、封装良率和现场可维护性尚未完全成熟。
7. **整柜 burn-in 和交付。** 100kW+ rack 测试需要高功率假负载、液冷环路和网络稳定性验证，测试场地也成为产能。
8. **液冷冷板、CDU 和快接头。** OCP 材料显示冷板先爆发，UQD/冷板标准化仍在推进，供应商认证周期长。
9. **电力接入和并网。** IDC 认为电力/电网是 2026 主要运营瓶颈；即使芯片可交付，数据中心未上电也无法确认真实产能。
10. **高端工程人才。** HBM package co-design、SerDes、compiler/runtime、rack power、liquid cooling 和 cloud orchestration 的人才高度稀缺。
11. **软件生态适配。** CUDA、ROCm、Neuron、XLA/JAX、Triton/vLLM/SGLang 差距会影响非 NVIDIA 真实利用率。
12. **出口管制和合规认证。** 中国可获得芯片、海外主权云、本地安全审计和固件信任要求改变供应路径。

### 4.3 BOM 和成本拆分

高端 AI 加速器单模块粗略 BOM：

| 成本项 | 单模块成本占比 | 说明 |
|---|---:|---|
| HBM/HBM base die/堆叠 | 25-40% | HBM3E/HBM4 是最大成本变量，供不应求时可超过 compute die 成本影响 |
| Compute die 晶圆 | 20-32% | 4NP/3nm/2nm 晶圆、良率、die size 和 NRE 摊销决定成本 |
| 先进封装/Interposer/CoWoS | 12-22% | CoWoS-L/S、underfill、bonding、封装良率，紧缺时价格上行 |
| ABF/PCB/载板 | 5-12% | 大尺寸载板、低损耗材料、高层数和良率 |
| 电源/VRM/电容/连接器 | 4-10% | 高瞬态电流和 48V/54V 架构拉高价值量 |
| 测试、KGD、burn-in | 5-10% | HBM KGD、SerDes、NVLink/PCIe、package test、rack burn-in |
| 机械、散热、装配 | 3-8% | OAM/SXM 模块、冷板、结构件 |
| NRE/IP/软件摊销 | 3-10% | 自研 ASIC 初期 NRE 很高，规模越大摊薄越快 |

整柜 AI rack 粗略价值拆分：

| 成本项 | 整柜价值占比 | 说明 |
|---|---:|---|
| GPU/ASIC 加速器模块 | 60-75% | 含 HBM 和先进封装，是价值核心 |
| CPU/host memory/storage | 5-10% | Agentic workloads 使 CPU 和 KV cache storage 占比提高 |
| Scale-up/scale-out 网络 | 8-15% | NVSwitch/NIC/InfiniBand/Ethernet/Retimer/光模块 |
| Power shelf/VRM/rack busbar | 3-7% | 48V/54V，未来 800VDC 可能提升 |
| 液冷和机械集成 | 3-8% | 冷板、CDU、manifold、leak detection、rack |
| 系统集成、测试、服务 | 3-6% | ODM/OEM 的主要利润来源但毛利率较低 |

### 4.4 毛利决定因素和价格传导

| 因素 | 如何决定毛利 | 价格如何传导 |
|---|---|---|
| 供需缺口 | HBM/CoWoS/高端 GPU 供不应求时，头部厂商可维持高 ASP | 上游涨价先传给 GPU/ASIC，再传给云服务和 token 价格 |
| 软件和生态锁定 | CUDA、Neuron、XLA、Azure/Google/AWS 私有栈提高切换成本 | 客户按可用产能和 time-to-market 支付溢价 |
| 良率和测试时间 | 良率低会提高单位成本，但紧缺期可部分转嫁 | 非头部客户拿不到最优价格和交期 |
| 规模和 NRE 摊销 | 自研 ASIC 初期 NRE 高，百万颗/GW 级后成本优势显现 | Hyperscaler 以低内部转移价换长期 TCO，供应商拿设计服务和 IP 利润 |
| 客户集中度 | NVIDIA 对多客户议价强，Broadcom 对少数大客户绑定强，但客户议价也强 | 多年锁单、预付款、产能 reservation 成为价格机制 |
| 系统交付能力 | 能把芯片、网络、电力、冷却和软件一起交付的厂商可拿系统溢价 | 价格从“单卡 ASP”转向“rack/POD/GW token economics” |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 维度 | 2026 结构判断 | 量化锚 |
|---|---|---|
| 高端 merchant GPU | NVIDIA 仍绝对主导，AMD 是第二供应源，Intel 弱化 | TrendForce 预计 NVIDIA 高端 GPU 出货中 Blackwell >70%；AI server GPU 出货仍约 69.7% |
| Hyperscaler ASIC | Google/AWS/Microsoft/Meta/OpenAI 进入 GW 级扩张，Broadcom 是最大外部实现层 | TrendForce 预计 ASIC AI server 2026 27.8%；Broadcom AI Q1 $8.4B，Q2 指引 $10.7B |
| 中国国产 AI 芯片 | Huawei 第一梯队，Cambricon、Alibaba、Baidu、Biren、Iluvatar 等分食国产替代 | 出口限制使中国仍是全球第二大 AI 基建市场之一，IDC Q4 2025 中国 $8.4B |
| HBM | SK hynix、Samsung、Micron 三家寡头 | TrendForce 预计三家进入 NVIDIA HBM4 供应链 |
| Foundry/advanced package | TSMC 高度集中，Samsung/Intel/SMIC 争取特定客户 | TSMC CoWoS 2026 年底约 11.5-14 万片/月估计 |
| AI networking | NVIDIA、Broadcom、Marvell、Arista、Cisco、Astera、Credo 等 | Ethernet/InfiniBand/NVLink/UALink/CXL 多标准并行 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 可量化观察 | 为什么能定价 |
|---|---|---|
| 先进制程和封装 | 3nm/2nm tape-out、CoWoS/SoIC、HBM KGD、大 die 良率 | 客户无法短期复制，失败一次 tape-out 会损失数亿美元级时间和资金 |
| HBM 供应锁定 | HBM3E/HBM4 长约和预付款 | 没有 HBM 就没有高端加速器，供应商可获得稀缺溢价 |
| 软件生态 | CUDA、ROCm、Neuron、XLA/JAX、Triton/vLLM、compiler/runtime | 用户迁移成本高，模型、内核、调度、debug 工具都绑定硬件 |
| Rack-scale 系统能力 | NVL72、Trainium UltraServer、TPU pod、Helios、MTIA OCP rack | 竞争单位从芯片变成 rack/POD，单芯片性价比不足以替代系统 |
| 客户验证和认证 | Hyperscaler qualification、OCP、S.A.F.E.、security RoT、液冷认证 | 一旦进入客户标准平台，替换成本很高，供应商有持续订单 |
| 规模采购和供应链金融 | GW 级订单、产能 reservation、预付锁定 | 大客户拿低价但也锁定供应商，供应商获得高可见度和资本效率 |
| 高速互连 IP | 1.6T SerDes、PCIe 6/7、CXL、UALink、NVLink、CPO | 链路稳定性和低延迟直接决定 GPU 利用率，客户愿意为可用性付费 |
| 电力和液冷协同 | 100kW+ rack、闭环液冷、800VDC、ride-through | AI rack 停机损失高，可靠交付比单件成本更重要 |

### 5.3 价值捕获：长期高 ROIC/高毛利最可能在哪里

| 层级 | 长期价值捕获判断 | 原因 |
|---|---|---|
| NVIDIA 平台层 | 最高 | GPU + NVLink + CUDA + networking + DPU + rack reference design 形成系统锁定，毛利率可维持 70% 以上 |
| Broadcom/Marvell custom silicon 和网络 IP | 很高 | 自研 ASIC 需要实现层、SerDes、Ethernet、PCIe、光互连，客户 GW 级但切换风险高 |
| HBM 头部厂商 | 很高但周期性强 | 2026-2027 是 AI 内存短缺高点，长期仍受 DRAM 周期和 capex 影响 |
| EDA/IP/verification | 高 | 先进节点、chiplet、SerDes、PQC/security、AI for EDA 让工具成为刚需，软件毛利 80%+ |
| 高端互连芯片/Retimer/Fabric switch | 高 | AI 利用率受互连制约，Astera 类财务已显示高增长高毛利 |
| TSMC/先进封装 | 高 | 产能稀缺，但资本开支大，毛利低于纯 IP/平台层 |
| ODM/OEM rack integration | 中 | 收入大、周转快，但毛利常为低双位数，除非绑定液冷/服务/金融 |
| 电力/液冷设备 | 中到高 | 增长确定，毛利 20-45%，高端认证供应商可上行 |
| Neocloud/GPU 租赁 | 分化 | 利用率、融资成本、残值、长约客户决定生死，高 beta 但风险大 |

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 6.1 三个最可能的 2026 拐点

1. **推理和 agentic AI 从叙事变成硬件采购主线。**  
   GB300、Ironwood、TPU 8i、Maia 200、MTIA 400/450/500 都围绕低 token 成本、低延迟、长上下文、agentic workflow 设计。2026 采购会从“训练大模型”扩展到“日常推理产能池”。

2. **Blackwell Ultra 确认成为 2026 最大收入平台，Rubin 变成 2027 弹性。**  
   TrendForce 下修 Rubin 2026 份额至 22%，Blackwell >70%。这意味着 2026 最稳的不是押最前沿 HBM4，而是押 GB300/B300 供应链，包括 HBM3E、CoWoS、ABF、液冷、power shelf 和 800G/1.6T。

3. **自研 ASIC 的份额出现可量化跃迁。**  
   TrendForce 预计 2026 ASIC AI server 27.8%，AWS、Google、Meta、Microsoft、OpenAI/Broadcom 都有明确路线。2026 将是“ASIC 不再只是 Google TPU”的产业确认年。

### 6.2 2026 最可能放量子方向

| 子方向 | 放量概率 | 关键受益公司/环节 |
|---|---:|---|
| GB300/B300 整柜 | 很高 | NVIDIA、TSMC、SK hynix/Samsung/Micron、Quanta/Foxconn/Supermicro/Dell、Vertiv/Delta/Lite-On |
| HBM3E 和 server DRAM | 很高 | SK hynix、Samsung、Micron、Advantest、Teradyne、FormFactor |
| CoWoS/ABF/测试 | 很高 | TSMC、ASE、Amkor、Ibiden、Shinko、Unimicron、Nan Ya、AT&S |
| AWS/Google/Microsoft/Meta 自研 ASIC | 高 | Broadcom、AWS Annapurna、Google TPU team、Microsoft、Meta、TSMC、Marvell/Alchip/GUC |
| 800G/1.6T 光模块和 AI Ethernet | 高 | NVIDIA、Broadcom、Marvell、Arista、Cisco、Celestica、Innolight、Eoptolink、Coherent、Lumentum |
| 液冷和 48V rack power | 高 | Vertiv、Schneider、CoolIT、Asetek、Delta、Lite-On、MPS、Vicor、Infineon、TI |
| 中国国产 AI 芯片 | 高但地区性 | Huawei、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Iluvatar、Enflame、MetaX |

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 7.1 三个最可能的 2027 拐点

1. **HBM4 平台从验证转向规模化。**  
   Rubin、MI400/MI455X、TPU8、后续 Broadcom XPU 和部分国产新平台都会争抢 HBM4。2027 的最大 beta 是 HBM4 供给、CoWoS-L、HBM tester、ABF 和液冷能否同步爬坡。

2. **ASIC 和开放互连共同提高非 NVIDIA 份额，但不会快速消灭 NVIDIA。**  
   Google、AWS、Meta、Microsoft、OpenAI 的 ASIC 主要吃稳定推理和内部 workload。NVIDIA 通过 NVLink Fusion、Spectrum-X、Dynamo、BlueField、LPX 等把自研 ASIC 拉进其 AI factory 生态，竞争会从 GPU 单点变成 rack/POD 控制权。

3. **高密度机柜电力架构进入 800VDC/1MW rack 的商业试点。**  
   Rubin Ultra/Kyber、MI400/MI500、TPU8 后续版本、CPO/1.6T/3.2T 网络会使 500kW 至 1MW rack 从概念转向新建 AI factory 设计约束。电力、储能、固态保护、液冷和数字孪生成为芯片出货的上游条件。

### 7.2 2027 最可能放量子方向

| 子方向 | 放量逻辑 | 2027 观察指标 |
|---|---|---|
| Vera Rubin NVL72 | HBM4 多供、partner availability 后进入全年交付 | NVIDIA data center revenue mix、HBM4 qualification、NVL72 rack 交期 |
| AMD MI400/Helios | Meta 6GW 协议和第二供应源需求 | 首 1GW 交付、ROCm benchmark、Helios UALink 生态 |
| TPU 8t/8i | Google 将训练/推理分化，外部 Cloud 客户扩张 | TPU8 GA、Anthropic/外部客户容量、Broadcom/MediaTek 供应链线索 |
| Broadcom custom XPU | OpenAI 10GW、Meta >1GW、Anthropic/Google TPU 等 | Broadcom AI revenue run-rate、2027 $100B 目标兑现度 |
| UALink/ESUN/PCIe-CXL fabric | 非 NVIDIA rack 和 custom ASIC 需要开放 scale-up | Astera/Marvell/Broadcom switch port 出货、UALink product ramp |
| CPO/OCS/1.6T/3.2T | 数据中心光纤数量和功耗成为限制 | 1.6T 光模块价格、CPO 失效率、OCS 规模化项目 |
| 800VDC/HVDC power | 500kW+ rack 需要电力架构升级 | Vertiv/Schneider/Delta/Lite-On 订单、OCP HPR/HVDC 规范落地 |

## 8. 头部公司和技术优势公司清单

### 8.1 加速器芯片和平台

| 细分 | 公司 |
|---|---|
| Merchant GPU/rack-scale | NVIDIA、AMD、Intel |
| 中国国产 AI GPU/ASIC/GPGPU | Huawei Ascend、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Iluvatar CoreX、Moore Threads、MetaX、Enflame、Hygon、Tencent 自研线索、壁仞/沐曦/燧原/天数智芯等 |
| Hyperscaler 自研 ASIC | Google TPU、AWS Annapurna Trainium/Inferentia、Microsoft Maia、Meta MTIA、OpenAI custom accelerator、Tesla AI5/Dojo、Apple Private Cloud Compute 相关 silicon |
| Custom silicon 实现层 | Broadcom、Marvell、Alchip、GUC、MediaTek、Socionext、Faraday、Arm CSS/Neoverse、Synopsys IP、Cadence IP |
| 专用推理和新架构 | Groq、Cerebras、SambaNova、Tenstorrent、d-Matrix、Etched、MatX、Rebellions、FuriosaAI、Positron AI、Untether AI、Encharge AI、SiMa.ai、Kneron、Axelera AI、Mythic、Tachyum、Graphcore/IP 资产相关方 |
| 企业/主权 AI accelerator | IBM Spyre、Fujitsu、NEC、Preferred Networks、Sapeon/Rebellions 合并生态、SoftBank/SambaNova 相关生态 |

### 8.2 HBM、存储和内存

| 细分 | 公司 |
|---|---|
| HBM/DRAM | SK hynix、Samsung、Micron |
| NAND/eSSD/KV cache | Samsung、Micron、SK hynix/Solidigm、Kioxia、Western Digital/SanDisk、Phison、Silicon Motion、Marvell、Microchip |
| AI storage 系统 | Dell、HPE、NetApp、Pure Storage、VAST Data、WEKA、DDN、IBM Storage、Lenovo、Supermicro、QCT |
| HBM/DRAM 测试设备 | Advantest、Teradyne、FormFactor、Technoprobe、Chroma、Cohu |

### 8.3 Foundry、封装、基板、设备

| 细分 | 公司 |
|---|---|
| Foundry | TSMC、Samsung Foundry、Intel Foundry、SMIC、UMC/GlobalFoundries 成熟节点配套 |
| 先进封装/OSAT | TSMC CoWoS/SoIC、ASE/SPIL、Amkor、Samsung AVP、Intel EMIB/Foveros、JCET、Tongfu Micro、Huatian、Powertech |
| ABF/IC substrate/PCB | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、AT&S、Kyocera、Zhen Ding、Shennan Circuits、WUS、TTM |
| 半导体设备 | ASML、Applied Materials、Lam Research、Tokyo Electron、KLA、ASM、BESI、ASMPT、Disco、SCREEN、Onto Innovation |

### 8.4 网络、互连、光模块和 PCIe/CXL

| 细分 | 公司 |
|---|---|
| AI network silicon | NVIDIA/Mellanox、Broadcom、Marvell、Cisco/Acacia、AMD/Pensando、Intel Ethernet、Astera Labs、Credo、Alphawave Semi |
| Switch/system | Arista、Cisco、NVIDIA、HPE/Juniper、Celestica、Accton、Edgecore、Wistron、Delta Networks |
| 光模块/硅光/DSP | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、Fabrinet、Broadcom、Marvell、MACOM、Semtech、Accelink、Hisense Broadband、Source Photonics、AOI |
| PCIe/CXL Retimer/Switch/IP | Astera Labs、Broadcom、Microchip、Diodes、Parade、Montage、Rambus、Synopsys、Cadence、Avery、Teledyne LeCroy、Keysight |
| 标准生态 | PCI-SIG、CXL Consortium、UALink Consortium、Ultra Ethernet Consortium、OCP、UCIe Consortium |

### 8.5 电源、液冷、安全和 EDA/IP

| 细分 | 公司 |
|---|---|
| AI 电源和功率半导体 | Delta、Lite-On、Flex、Bel Fuse、Vicor、Monolithic Power Systems、Infineon、Texas Instruments、Analog Devices、Renesas、STMicro、onsemi、Murata、TDK、Nichicon、Panasonic |
| 液冷和热管理 | Vertiv、Schneider Electric/Motivair、CoolIT、Asetek、Boyd、Delta、AVC、Nidec、Johnson Controls、Carrier、Modine、LiquidStack、Submer |
| EDA/IP | Synopsys、Cadence、Siemens EDA、Ansys、Keysight EDA、Arm、Rambus、CEVA、Arteris、Alphawave、Avery |
| 安全/固件/Root of Trust | Microsoft Caliptra 生态、Google/OpenTitan、OCP S.A.F.E./S.O.L.I.D./L.O.C.K.、NVIDIA BlueField、Broadcom/Marvell secure boot、Rambus security IP |

## 9. 信息源、置信度和关键事实索引

### 9.1 一手信息

- [NVIDIA Vera Rubin 官方新闻稿](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)：Vera Rubin 七类芯片 full production，five rack-scale systems，AI factory 路线。
- [NVIDIA Vera Rubin 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)：Vera Rubin POD、1,152 Rubin GPUs、60 exaflops、10PB/s bandwidth、2026 H2 ship。
- [NVIDIA GB300 NVL72 官方页](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)：72 Blackwell Ultra GPUs、36 Grace CPUs、288GB HBM3E、液冷 rack。
- [NVIDIA FY2026 财报](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)：FY2026 数据中心 $193.7B、Q4 $62.3B、毛利率锚点。
- [AMD Q1 2026 财报](https://www.amd.com/en/newsroom/press-releases/2026-5-5-amd-reports-first-quarter-2026-financial-results.html)：Data Center $5.8B、同比 +57%、Meta up to 6GW。
- [AMD CES 2026 官方发布](https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-and-its-partners-share-their-vision-for-ai-ev.html)：Helios、MI400、MI455X、MI500、CDNA 6、2nm、HBM4E。
- [AWS Project Rainier](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster)：近 50 万 Trainium2，Anthropic 使用超过 100 万 Trainium2。
- [AWS Trainium3](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-ec2-trn3-ultraservers/)：Trainium3 2.52 PFLOPs FP8、144GB HBM3E、4.9TB/s、Trn3 UltraServer 144 chips。
- [Anthropic/Amazon compute 合作](https://www.anthropic.com/news/anthropic-amazon-compute)：Anthropic 签署 up to 5GW capacity，2026 年底近 1GW Trainium2/3 容量。
- [Google Ironwood TPU](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/)：192GB HBM、7.37TB/s、1.2TBps ICI、推理定位。
- [Google TPU 8t/8i](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era/)：8t 训练、8i 推理、9600 chips superpod、2PB HBM、8i 288GB HBM/384MB SRAM、2026 later GA。
- [Microsoft Maia 200](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)：TSMC 3nm、216GB HBM3E、7TB/s、272MB SRAM、30% better performance per dollar。
- [Meta MTIA 路线图](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)：四代 MTIA 两年内推出，MTIA 300 已生产，数十万 MTIA 部署。
- [OpenAI/Broadcom 10GW](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)：OpenAI 设计 custom accelerator，Broadcom 部署 racks，2026 H2 开始，2029 完成 10GW。
- [Broadcom Q1 FY2026 SEC/IR](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm)：Q1 AI revenue $8.4B、同比 +106%、Q2 AI semiconductor $10.7B、Adjusted EBITDA 68%。

### 9.2 行业报告和交叉验证

- [IDC AI Infrastructure Tracker 公共摘要](https://www.idc.com/resource-center/blog/ai-infrastructure-spending-caps-historic-year-at-90-billion-in-q4-2025-2029-spending-to-eclipse-1-trillion/)：2025 AI infrastructure $318B，2026 $487B，2029 >$1T，Q4 服务器 97.6%。
- [Gartner 2026 半导体预测](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)：2026 semiconductor >$1.3T，AI semis 约 30%，DRAM/NAND 涨价。
- [TrendForce AI server 2026](https://www.trendforce.com/presscenter/news/20260120-12887.html)：AI server 出货 +28% 以上，GPU 69.7%，ASIC 27.8%。
- [TrendForce Blackwell/Rubin 2026](https://www.trendforce.com/presscenter/news/20260408-13003.html)：Blackwell 高端 GPU 份额 71%，Rubin 下修至 22%，LPU 需求数十万。
- [TrendForce HBM4](https://www.trendforce.com/presscenter/news/20260213-12929.html)：三大 HBM 供应商预计 2026 Q2 完成 NVIDIA HBM4 验证。
- [TrendForce TSMC CoWoS](https://www.trendforce.com/news/2026/04/16/news-tsmc-says-cowos-offers-industrys-largest-reticle-size-packaging-amid-intel-emib-rivalry-copos-advances/)：CoWoS 2026 年底 11.5-14 万片/月、2027 17 万片/月估计。
- [TrendForce/PRNewswire 九大 CSP CapEx](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html)：2026 九大 CSP CapEx 约 $830B。
- [TrendForce Broadcom 2027 目标](https://www.trendforce.com/news/2026/03/05/news-broadcom-reportedly-eyes-100b-ai-chip-revenue-in-2027-backed-by-six-key-clients-including-google-meta/)：Broadcom 2027 AI chip revenue >$100B 媒体/电话会线索。
- [OCP EMEA 2026](https://www.opencompute.org/summit/emea-summit)：Open Data Center for AI、HVDC、液冷、UALink/ESUN、FCSA、Caliptra 等标准化线索。
- [PCI-SIG DevCon 2026](https://pcisig.com/pci-sig-developers-conference-2026)：PCIe 6/7/8、Retimer、光互连、AI infrastructure 议程。

### 9.3 非正式或媒体线索的使用方式

| 线索 | 来源类型 | 本文处理 |
|---|---|---|
| Broadcom 2027 AI chip revenue >$100B | Reuters/TrendForce/电话会转述 | 用作乐观和极度乐观上沿，不作为基准 |
| 中国 Ascend/Cambricon/Alibaba/Baidu 具体出货 | TrendForce、SCMP、行业媒体 | 用区间估算，强调良率和软件风险 |
| OpenAI/Meta/Anthropic GW 级容量 | 官方公告 + 媒体/投资者转述 | 官方部分高置信，非官方具体金额只用于校验 |
| CoWoS 月产能 | TrendForce 引述机构和供应链 | 作为供给约束锚，不视为 TSMC 官方产能承诺 |

## 10. 投资观察清单

1. NVIDIA GB300/B300 交付是否从 GPU 单卡转向 NVL72 整柜确认收入。
2. Rubin HBM4 qualification 是否在 2026 Q2-Q3 完成，多供应商份额如何分配。
3. Broadcom AI revenue 是否从 $8.4B/Q1 到 $10.7B/Q2 后继续加速，是否接近 2027 $100B 轨道。
4. AWS Trainium3 和 Google TPU8 的外部客户采用率，尤其 Anthropic 是否扩大多云 ASIC 使用。
5. AMD MI400/Helios 首 1GW Meta 部署能否在 2026 H2 按计划启动。
6. HBM/DRAM 价格是否继续上涨，内存是否从 GPU BOM 成本项变成最大利润池。
7. TSMC CoWoS 扩产和 OSAT 外包是否顺利，ABF/测试是否成为下一个瓶颈。
8. 1.6T 光模块、CPO、OCS 的量产良率和客户设计导入。
9. UALink/ESUN/PCIe-CXL fabric switch 是否进入 2027 非 NVIDIA rack 的量产 BOM。
10. 中国国产 AI 芯片实际大集群稳定性，尤其 Ascend 950、Cambricon 690、Baidu M100/M300。
11. AI agent 收入和 token 使用量能否覆盖 2026-2027 capex，否则 2028 可能出现局部消化压力。

# 行业调研：【系统内存、SOCAMM与内存模组】

> 版本日期：2026-05-08（美国时间 2026-05-07 晚间资料口径）  
> 研究范围：AI 服务器 CPU/主机侧系统内存、SOCAMM/SOCAMM2、DDR5 RDIMM/LRDIMM/MRDIMM、CXL-attached memory、内存模组 PCB/连接器/PMIC/SPD/RCD/DB/MRCD/CXL controller 等。除对比需要外，本报告不把 HBM 计入“系统内存”市场规模，但会把 HBM4 对 DRAM 产能挤占、价格和路线选择的影响纳入判断。  
> 情景口径：按用户要求，对 2026 AI 基础设施建设采取明显乐观假设；“极度超预期乐观”不是中性预测，而是用于评估供应链弹性、订单斜率和投资期权上沿。

## 0. 高浓度结论

1. **2026 年系统内存的最大新变量是 SOCAMM2，不是普通 DDR5。** NVIDIA Vera CPU/Rubin 平台把 LPDDR5X 服务器模组推到 AI factory 中心：Vera CPU 公开规格为 88 个 Olympus cores、LPDDR5X 子系统最高约 **1.2TB/s**，Vera Rubin NVL72 用 **36 个 Vera CPU + 72 个 Rubin GPU**。若按每 CPU 8 个 192GB SOCAMM2、每模块约 153.6GB/s 估算，单 NVL72 rack 的 CPU 侧 LPDDR 容量约 **55TB**，带宽约 **44TB/s**；这使 SOCAMM2 从“省电笔记本式内存形态”变成 AI 机柜的主内存架构。
2. **DDR5 RDIMM/LRDIMM 是 2026 收入底盘，MRDIMM 是性能溢价层。** 2026 AI 服务器主机侧仍大量依赖 DDR5 RDIMM，尤其是 128GB/256GB 高容量模组；Intel Xeon 6 平台推动 MRDIMM 进入高端 CPU memory bandwidth 升级，短期 attach rate 小，但 ASP 与接口芯片价值高。
3. **CXL memory 2026 仍小，但 ROI 随 DRAM 涨价上升。** CXL Type-3 memory expansion、CXL pooling、CXL-PNM 不是 HBM 替代品，而是把 stranded memory、KV cache、向量索引、IMDB 和 warm memory 留在内存语义里的利用率杠杆。2026 主要是 Azure/高端企业 pilot，2027 才可能进入小规模生产化。
4. **2026-2027 的 AI 内存利润池高度集中在 DRAM 三巨头和高端接口芯片。** Samsung、SK hynix、Micron 直接掌握 DRAM die、LPDDR binning、HBM/DDR/SOCAMM 产能分配和客户认证；Rambus/Montage/Renesas/Astera/Marvell 等接口与 CXL silicon 具备 60%+ 毛利的高 ROIC 特征；普通模组组装利润率较低，但 SOCAMM PCB、MRDIMM logic、CXL controller 能获得结构性溢价。
5. **未来两年最值得跟踪的不是“内存够不够”，而是“内存形态是否从 DIMM 插槽迁移到机柜级模块化”。** 2026 看 SOCAMM2、DDR5 高容量 RDIMM、MRDIMM Gen1、CXL 2.0 pilot；2027 看 256GB SOCAMM2、LPDDR6/SOCAMM 后继、MRDIMM Gen2、CXL pooling/PNM 与 AI storage/KV cache memory tier。

## 1. 关键事实锚点

| 锚点 | 关键数字/事实 | 对本报告的含义 |
|---|---:|---|
| NVIDIA Vera CPU | 88 cores；LPDDR5X memory subsystem 约 1.2TB/s；NVLink-C2C 约 1.8TB/s；用于 agentic AI CPU environments | 高带宽、低功耗 CPU 侧内存成为 Rubin 时代机柜 BOM 核心 |
| Vera Rubin NVL72 | 72 Rubin GPUs + 36 Vera CPUs；2026H2 合作伙伴产品供应；HBM4 与 LPDDR/SOCAMM 并行 | 每个 rack 需要数百个 SOCAMM2 模组，产生非线性模组需求 |
| Micron SOCAMM2 | LPDDR5X，速度最高 9.6Gb/s，192GB HVP，256GB sampling，单模组最高约 153GB/s，面向 Vera/Rubin | SOCAMM2 已进入量产导入，不只是样品 |
| Samsung SOCAMM2 | 192GB、256GB；LPDDR5X；用于下一代 AI 服务器平台 | 三大 DRAM 厂都在抢平台认证 |
| SK hynix SOCAMM2 | 192GB 产品面向 AI 服务器，强调低功耗和高带宽 | 供应源从 2026 起多元化，利于 NVIDIA/云厂商放量 |
| Rambus SOCAMM2 chipset | SOCAMM2 server module chipset，支持 LPDDR5X SOCAMM2 平台 | 接口芯片/模组配套成为独立利润池 |
| Gartner 半导体预测 | 2026 全球半导体收入约 **$1.320T**，2027 约 **$1.555T**；2026 memory 收入约 **$633B** | DRAM/内存不是边角料，而是 AI capex 最核心预算之一 |
| IDC/公开市场口径 | 2026 DRAM 收入可超过 **$400B**，NAND 也进入强涨价周期 | 系统内存 ASP 和模组毛利在 2026 继续受供需支撑 |
| Micron FY2026 Q2 | 数据中心收入占比高，HBM/DDR5/高容量服务器内存需求强；公司给出高毛利指引 | 验证 AI memory 价格和 mix 改善正在进入财务报表 |
| CXL 4.0 | 2025 年发布，速率到 128GT/s，支持 bundled ports、memory RAS 等 | 2026 收入主要还是 CXL 2.0/3.x，4.0 提前影响研发和设计导入 |

## 2. 行业边界与需求逻辑

### 2.1 本报告定义的“系统内存/内存模组”

| 层级 | 产品 | 是否计入市场规模 | 说明 |
|---|---|---|---|
| CPU/主机侧 DRAM | DDR5 RDIMM、LRDIMM、3DS RDIMM、MRDIMM | 计入 | AI server host、storage server、front-end CPU、agent sandbox、数据预处理 |
| LPDDR 服务器模组 | SOCAMM/SOCAMM2，未来 LPDDR6 SOCAMM | 计入 | 重点服务 Vera/Rubin CPU rack、低功耗高带宽 CPU memory |
| CXL 内存 | CXL Type-3 memory module/AIC/EDSFF、CXL pooling appliance | 计入 | memory expansion、pooling、tiering、KV cache、IMDB |
| 模组配套 | RCD、DB、MRCD/MDB、SPD Hub、PMIC、VR、CXL controller、CXL switch、SOCAMM chipset、PCB、连接器、测试 | 计入 | 其中接口 silicon/控制器价值捕获能力强 |
| HBM | HBM3E/HBM4/HBM4E | 不计入主规模，作为约束变量 | HBM 挤占 DRAM/EUV/封装资源，影响 DDR/SOCAMM 供给和价格 |
| SSD/NAND | eSSD、KV cache SSD | 不计入主规模，作为相邻需求 | CXL 与 SSD 共同形成 memory/storage tier |

### 2.2 为什么 2026 AI 数据中心把系统内存重新定价

AI 训练阶段的市场叙事主要看 GPU/HBM；2026 的变化是推理、agentic workload、长上下文、RAG、强化学习环境和多模态输入把 **CPU 侧内存容量、带宽和功耗** 重新推到瓶颈位置。

| 需求源 | 对系统内存的拉动 | 受益形态 |
|---|---|---|
| Agentic inference | 多轮工具调用、sandbox、代码执行、检索、planning，CPU environments 和 KV cache 生命周期变长 | SOCAMM2、DDR5 RDIMM、CXL memory tier |
| 长上下文/多模态 | KV cache 随上下文长度和视频输入暴增，HBM 留给 hot tokens，warm context 需要外部内存层 | CXL memory、AI storage、high-capacity RDIMM |
| Rubin/Vera CPU rack | GPU rack 旁边出现高带宽 CPU rack 和专用 agent CPU memory | SOCAMM2、LPDDR server module、SOCAMM chipset |
| 自研 ASIC/开放 rack | 非 NVIDIA 平台无法完全依赖 NVLink 封闭内存池，更重视 CPU/host memory 和 CXL | DDR5/MRDIMM、CXL、UALink/CXL fabric |
| DRAM 供给紧张 | HBM4/3E 抢占先进 DRAM wafer 和 TSV/封装资源，普通 server DRAM 也涨价 | DRAM 三巨头、模组库存、PMIC/RCD |

## 3. 2026-2027 AI 芯片技术路径下的系统内存映射

本节使用项目内既有 AI 芯片路线图作为底座，不再逐项外搜芯片出货。排序按 2026-2027 年初等效出货和价值权重。

| 芯片/平台 | 2026-2027 芯片路径 | 系统内存路径 | 对内存模组的直接拉动 | 2026 最可能状态 | 2027 放量状态 |
|---|---|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主力高端 GPU rack | Grace/host DDR5/LPDDR，GPU HBM3E；rack 内 memory pool 主要靠 NVLink | DDR5 高容量 RDIMM、服务器主机内存、少量 CXL | 大规模放量 | 仍有存量交付，逐步让位 Rubin |
| NVIDIA Vera Rubin NVL72 | 2026H2 首批，2027 主力 | Vera CPU 采用 LPDDR5X/SOCAMM2；Rubin GPU 用 HBM4 | SOCAMM2 爆发，CPU rack 内存从 DIMM 转向 LPDDR 模组 | 初期 HVP、客户验证、优先 hyperscaler | 大规模放量，256GB SOCAMM2 加速 |
| AWS Trainium2/3 | Trainium2 大量部署，Trainium3 2026 起步 | AWS 自研 server/rack，HBM + host DDR5，未来可能引入 CXL tier | 高容量 DDR5、eSSD、CXL memory pilot | Trainium2/3 混合交付 | Trainium3/4 推动 memory tier 优化 |
| Google TPU v7 Ironwood/TPU8 | TPU v7 2026 主力，TPU8 设计导入 | TPU pod 自研互连；host/server DDR5，CXL/pooled memory 可能用于 KV/cache 服务 | 高容量 DDR5、CXL pooling、memory orchestration | TPU v7 带动 server DRAM | TPU8 + CXL/AI storage 更清晰 |
| AMD MI350/MI400 Helios | MI350 2026 放量，MI400/Helios 2026H2 起步 | x86/EPYC host DDR5/MRDIMM，MI400 HBM4；开放 rack 更适配 CXL/UALink | MRDIMM、高容量 DDR5、CXL | MI350 依赖 DDR5 RDIMM | MI400 开放 rack 提高 MRDIMM/CXL 机会 |
| Microsoft Maia 200 | 2026 Azure 推理自研 | Azure host memory、HBM3E、液冷 rack | DDR5 高容量、CXL VM/内存池化 | 内部部署扩张 | CXL-backed VM 可能生产化 |
| Meta MTIA 300/400/500 | 2026-2027 Broadcom XPU + Meta OCP rack | 推荐/推理 rack 需要大量 host memory 与 warm cache | DDR5 RDIMM、CXL pooling、eSSD | MTIA 300/400 小到中规模 | 多 GW 后系统内存弹性上升 |
| Huawei Ascend 910C/950 | 中国国产替代 | 国产 DDR5/HBM/自研互连；受 HBM 和先进制程限制 | 国产 DDR5 RDIMM、模组 PCB、PMIC、CXL 进展较慢 | 国产替代带动 DDR5 | 950/960 若放量，国产内存配套升级 |
| Cambricon/Alibaba/Baidu | 国产 AI 加速器 | 国产/混合 DDR5、高容量主机内存、OAM 模组 | 国产 RDIMM、模组组装、PCB | 小到中规模 | 若集群化，主机内存需求放大 |
| Groq 3 LPX / 专用推理 | 低延迟 decode/推理 | 大量 SRAM + host/context memory；GPU/LPU/存储协同 | CXL memory、context memory、AI storage | 2026H2 小批量 | 2027 高端推理层期权 |

### 3.1 新技术成熟与放量时间表

| 技术 | 成熟时间：基准 | 放量时间：基准 | 乐观 | 极度超预期乐观 |
|---|---|---|---|---|
| DDR5 128/256GB RDIMM | 已成熟 | 2026 全年继续放量 | ASP 高位、128GB 成为 AI host 默认，256GB 供不应求 | DRAM 缺口扩大，客户预付锁量到 2027 |
| DDR5 MRDIMM Gen1 | 2025-2026 成熟 | 2026H2 在 Xeon 6/高内存带宽服务器扩散 | 高端 AI host attach rate 快速到 15-20% | 2027 前成为 CPU memory bandwidth 标配之一 |
| SOCAMM2 192GB | 2026H1 HVP/认证 | 2026H2 随 Vera/Rubin 首批放量 | 2026Q4 形成数百万级模组季度需求 | 2026 年底即成为 AI memory 最强增量品类 |
| SOCAMM2 256GB | 2026 sampling/客户验证 | 2027H1-H2 主流化 | 2026Q4 小批量进入高端 rack | 2027 上半年替代 192GB 成为 premium SKU |
| LPDDR6 SOCAMM 后继 | 2026 研发/标准推进 | 2027H2-2028 | 2027 头部客户设计锁定 | 2027H2 早期量产，提前抢 DDR5/MRDIMM 预算 |
| CXL Type-3 expansion | CXL 2.0 产品已可用 | 2026 pilot，2027 小批量生产 | Azure/GCP/AWS 公开 CXL memory tier | 2027 成为 AI inference/KV cache 标准采购项 |
| CXL pooling/orchestration | 2026 参考架构/云内测 | 2027 生产化 | Pangaea-like 软件被 hyperscaler 内部规模部署 | 2027 直接产品市场从个位数十亿美元跳到两位数十亿美元 |
| CXL-PNM / near-memory vector search | 2026 research/PoC | 2027 early access，2028 放量 | 2027 与 FAISS/vector DB/KV runtime 结合 | 2027 进入高端 RAG/agent cache appliance |
| MRDIMM Gen2/高速接口逻辑 | 2026 标准/样品 | 2027 平台导入 | 2027H1 出现较大 CPU 平台订单 | 2027 成为 high-bandwidth CPU host memory 主流升级 |

## 4. 已开始放量的关键产品：市场规模、渗透率、利润率

说明：下表为全球口径，收入按模组/部件销售额估算，非纯 DRAM die 口径；“未来 3 个月”约指 2026-05 至 2026-07/08 的滚动季度；“一年”为未来 12 个月；“两年”为未来 24 个月。利润率为行业区间，不代表单家公司指引。

### 4.1 已放量产品总表

| 产品/细分技术 | 当前状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| DDR5 高容量 RDIMM/LRDIMM（128GB/256GB） | 已大规模放量，是 AI host/default server memory 底盘 | 基准 $25-38B；乐观 $35-50B；极度 $50-65B | 基准 $95-145B；乐观 $140-205B；极度 $210-285B | 基准 $170-260B；乐观 $260-390B；极度 $420-580B | AI 服务器主机侧内存 2026 渗透率 70-85%；2027 仍为最大体量，但份额被 SOCAMM/CXL 稀释 | DRAM 厂 55-68% / 65-75% / 72-82%；模组组装 8-18% / 12-22% / 15-28% |
| DDR5 MRDIMM Gen1 | 已随高端 CPU 平台导入，仍早期 | 基准 $1.0-2.5B；乐观 $2.0-4.5B；极度 $4.5-7.0B | 基准 $5-11B；乐观 $10-20B；极度 $20-32B | 基准 $15-30B；乐观 $30-55B；极度 $55-85B | 高带宽 x86/AI host attach rate 2026 3-8%，2027 15-30%，2028 可到 30-45% | 模组 45-60% / 55-68% / 62-75%；MRCD/MDB 60-70% / 65-75% / 70-80% |
| SOCAMM2 192GB LPDDR5X | 2026 HVP，绑定 Vera/Rubin 初期平台 | 基准 $1.5-3.5B；乐观 $3-6B；极度 $6-10B | 基准 $14-26B；乐观 $28-48B；极度 $50-78B | 基准 $40-70B；乐观 $80-125B；极度 $140-210B | 2026 在 Rubin/Vera CPU rack 内接近 100%；在全部 AI system memory 中 5-12%；2027 到 15-30% | DRAM/SOCAMM 模组 60-72% / 68-78% / 75-85%；PCB/连接器 25-40% / 35-48% / 45-55% |
| SOCAMM2 chipset/PMIC/SPD/连接器/PCB | 随 SOCAMM2 同步放量，价值小但弹性大 | 基准 $0.3-0.8B；乐观 $0.7-1.4B；极度 $1.2-2.2B | 基准 $1.8-4.0B；乐观 $4-7.5B；极度 $7-12B | 基准 $5-11B；乐观 $11-20B；极度 $20-35B | 每个 SOCAMM2 模组都需要专用 PCB、连接、PMIC/SPD/VR/thermal；attach rate 与 SOCAMM 出货 1:1 | 接口 silicon 55-70% / 65-75% / 70-80%；PCB 25-38% / 32-45% / 40-55% |
| 标准 DDR5 interface chips：RCD/DB/SPD Hub/PMIC/TS | 已充分放量，受 DDR5 服务器内存增长驱动 | 基准 $1.5-2.6B；乐观 $2.4-3.8B；极度 $3.8-5.0B | 基准 $7-11B；乐观 $11-17B；极度 $17-24B | 基准 $12-20B；乐观 $20-32B；极度 $32-48B | DDR5 server DIMM attach rate 接近 100%；MRDIMM 会拉高单模组逻辑价值 | 55-65% / 60-70% / 65-75% |
| CXL Type-3 memory expansion 模组/AIC | 已有产品与云 preview，但规模仍小 | 基准 $0.25-0.6B；乐观 $0.5-1.0B；极度 $1.0-1.8B | 基准 $1.5-3.5B；乐观 $3.5-7B；极度 $7-12B | 基准 $6-14B；乐观 $14-28B；极度 $30-55B | 2026 AI/高内存服务器 <2%；2027 3-8%；2028 若云 GA 可 10%+ | CXL controller 65-75% / 70-78% / 75-82%；模组系统 35-50% / 45-60% / 55-65% |
| 服务器内存模组 PCB（RDIMM/MRDIMM/SOCAMM） | 已放量，SOCAMM 是新增高阶料号 | 基准 $1.0-1.8B；乐观 $1.6-2.8B；极度 $2.8-4.0B | 基准 $5-8B；乐观 $8-13B；极度 $13-20B | 基准 $9-16B；乐观 $17-28B；极度 $30-45B | 高容量 RDIMM/MRDIMM/SOCAMM 拉高层数、材料、良率要求 | 22-32% / 30-42% / 40-52% |

### 4.2 关键增速判断

| 产品 | 基准增长 | 乐观增长 | 极度超预期乐观增长 | 为什么会涨 |
|---|---:|---:|---:|---|
| SOCAMM2 | 未来 12 个月从近零到 $14-26B | $28-48B | $50B+ | Vera/Rubin 机柜一旦交付，每 rack 需要数百个模组，单位需求离散跳升 |
| MRDIMM | +80-120% | +150-250% | +300%+ | CPU memory bandwidth 成为 agent/RAG/数据预处理瓶颈，客户愿意为带宽付溢价 |
| CXL memory | +100-180% | +200-350% | +500%+ | 基数小，Azure preview 与 AI KV cache 可以迅速改变采购节奏 |
| DDR5 高容量 RDIMM | +35-60% | +60-90% | +100%+ | DRAM 价格上涨 + AI server DIMM 容量上移 + 256GB 高端模组紧缺 |
| Interface chips | +30-50% | +50-80% | +90%+ | DDR5/MRDIMM/SOCAMM/CXL 都提高单模组 silicon attach value |

## 5. 在研关键产品与细分技术：市场规模、渗透率、利润率

| 在研/导入技术 | 当前阶段 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| 256GB SOCAMM2 | sampling/客户验证，2027 主流化候选 | 基准 <$0.5B；乐观 $0.5-1.2B；极度 $1.2-2.5B | 基准 $4-10B；乐观 $10-22B；极度 $22-38B | 基准 $30-55B；乐观 $60-100B；极度 $110-170B | 2026 主要 premium SKU；2027 在 Vera/Rubin CPU memory 中从 10-20% 升到 40-70% | 65-75% / 72-82% / 78-88% |
| LPDDR6 SOCAMM / SOCAMM3 | 研发/标准前期，2027 设计锁定 | 近零 | 基准 <$2B；乐观 $2-5B；极度 $5-10B | 基准 $8-20B；乐观 $25-55B；极度 $60-100B | 2027H2 早期，2028 才是主流窗口 | 60-75% / 70-82% / 78-88% |
| MRDIMM Gen2 / 高速 MDB-MRCD | 标准/样品/平台导入 | 基准 <$0.5B；乐观 $0.5-1B；极度 $1-2B | 基准 $2-6B；乐观 $6-12B；极度 $12-22B | 基准 $18-35B；乐观 $35-70B；极度 $75-120B | 2027 在高端 CPU host memory 中 10-20%，2028 可 30%+ | 模组 50-68%；接口芯片 65-80% |
| CXL memory pooling appliance/software | reference architecture、云内测 | 基准 <$0.2B；乐观 $0.2-0.6B；极度 $0.6-1B | 基准 $1-3B；乐观 $3-8B；极度 $8-15B | 基准 $6-18B；乐观 $20-45B；极度 $50-90B | 2026 pilot；2027 hyperscaler/NeoCloud 小规模生产；2028 标准化采购 | 软件 70-90%；appliance 35-55%；controller 65-78% |
| CXL-PNM / near-memory vector search | 研究原型/PoC | 近零 | 基准 <$1B；乐观 $1-3B；极度 $3-7B | 基准 $3-10B；乐观 $12-30B；极度 $35-70B | 2027 early access，取决于 FAISS/vector DB/KV runtime API | silicon 60-80%；软件 75-90% |
| CXL 4.0 128GT/s controllers/switches | spec 已发布，产品在研发 | 近零 | 基准 <$1B；乐观 $1-2B；极度 $2-4B | 基准 $4-10B；乐观 $10-25B；极度 $25-45B | 2027 设计导入，2028 系统收入更明显 | 65-80% |
| CMM-H / CXL persistent/hybrid memory | 产品概念/早期 | 近零 | 基准 <$0.5B；乐观 $0.5-1.5B；极度 $1.5-3B | 基准 $2-7B；乐观 $8-18B；极度 $20-40B | 2027 仍是特定场景，2028 若 Optane 空白被填补则放量 | 45-65% |
| AI memory telemetry/thermal/power management | 随高端模组导入 | 基准 $0.1-0.3B；乐观 $0.3-0.6B；极度 $0.6-1B | 基准 $0.8-2B；乐观 $2-4B；极度 $4-7B | 基准 $3-7B；乐观 $8-15B；极度 $15-28B | DDR5/MRDIMM/SOCAMM 每模组 attach，更多 sensor/PMIC/firmware | 45-70%，软件/firmware 更高 |

## 6. 供给侧：产能结构、瓶颈、成本与价格传导

### 6.1 产能结构

| 环节 | 主要地区 | 主要公司 | 产能/工艺特征 |
|---|---|---|---|
| DRAM die / LPDDR / DDR5 | 韩国、美国、日本、台湾、新加坡、中国大陆追赶 | Samsung、SK hynix、Micron；CXMT/Nanya/Winbond 为中低端或追赶 | 1b/1c/1γ DRAM、EUV layer、LPDDR5X 高速 bin、HBM/DDR/SOCAMM 产能互相挤占 |
| SOCAMM2 模组 | 韩国、美国/台湾供应链、越南/马来西亚后段 | Micron、Samsung、SK hynix，配套 Rambus/PCB/连接器厂 | LPDDR5X 封装 + 小型高密度模组 + 高速信号完整性 + AI 服务器认证 |
| DDR5 RDIMM/MRDIMM | 美国、韩国、台湾、中国大陆、东南亚 | Micron、Samsung、SK hynix、Kingston、SMART Modular、Innodisk、ADATA、Apacer、Transcend 等 | 高容量 RDIMM、3DS RDIMM、MRDIMM 需要更多 interface logic 和平台验证 |
| Interface chips | 美国、台湾、中国大陆、以色列/全球设计 | Rambus、Montage、Renesas、Microchip、Astera、Marvell、TI、MPS、ADI、Infineon | RCD/DB/MRCD/MDB/SPD/PMIC/CXL controller，先进封装和固件能力重要 |
| CXL controller/switch | 美国、中国大陆/台湾、以色列等 | Astera Labs、Marvell、Microchip、XConn、Montage、Rambus、Samsung/Micron 自研生态 | PCIe 5/6、CXL 2.0/3.x，controller + firmware + OS/cloud integration |
| 模组 PCB | 韩国、台湾、中国大陆、日本 | Simmtech、Daeduck、TLB、Korea Circuit、Tripod、Unimicron、Nan Ya PCB、Shennan、WUS、SCC 等 | 细线路、高层数、低损耗、高翘曲控制；SOCAMM 小型化提高良率门槛 |
| 连接器/插座 | 美国、日本、台湾/中国大陆 | Amphenol、TE Connectivity、Molex、LOTES、Foxconn Interconnect、Hirose 等 | SOCAMM compression attached、DIMM connector、EDSFF/CXL connector |
| 测试与探针 | 日本、美国、欧洲、台湾/韩国 | Advantest、Teradyne、FormFactor、Technoprobe、Chroma、Keysight 等 | 高速 DRAM test、module burn-in、CXL compliance、SI/PI/thermal validation |

### 6.2 供给瓶颈：至少 10 条

| 瓶颈 | 为什么卡 | 对价格/交付的影响 |
|---|---|---|
| DRAM 先进制程产能 | HBM4、HBM3E、DDR5、LPDDR5X 争抢同一批先进 wafer 与 EUV/良率资源 | DDR5/SOCAMM 即使需求强，也可能被 HBM 优先级挤压，ASP 维持高位 |
| LPDDR5X 高速 bin | SOCAMM2 要求服务器级可靠性、9.6Gb/s 等高速规格和长期稳定供货 | 可用 die 不是普通 LPDDR 等价替换，早期良率和筛选成本高 |
| SOCAMM2 模组良率 | 小尺寸、高密度、多通道 LPDDR、热/机械压力、连接可靠性要求高 | PCB/连接器/封装短缺时，模组溢价显著 |
| NVIDIA/云厂认证 | AI rack 内存需要平台 firmware、thermal、RAS、长时间 stress、供应链安全认证 | 没有认证就无法进入大客户；认证形成定价权 |
| MRDIMM interface logic | MRDIMM 需要 MRCD/MDB 等高速逻辑，信号完整性、功耗和时序复杂 | 高速接口芯片厂商获得高毛利，供应不足会限制 MRDIMM attach |
| CXL 软件栈 | Linux/kernel、hypervisor、Kubernetes、NUMA tiering、fabric manager 仍在磨合 | 硬件有货不等于能大规模部署，2026 收入上限受软件限制 |
| CXL controller/retimer/switch | 需要 PCIe/CXL 高速 SerDes、firmware、RAS、cloud validation | controller 稀缺时 CXL 模组利润率可高于普通 DIMM |
| PCB/连接器材料 | 高速内存模组需要低损耗材料、翘曲控制、细线宽和高一致性 | SOCAMM/MRDIMM PCB 毛利显著高于普通 DIMM PCB |
| 测试时间 | 高容量 RDIMM/SOCAMM/CXL 模组 burn-in 时间长，CXL 还要做协议和一致性测试 | 测试产能成为隐性瓶颈，拉长交期 |
| 技术人才 | AI memory 平台需要 DRAM、SI/PI、thermal、firmware、cloud software 复合能力 | 小厂很难跨过客户认证，头部集中度提高 |
| 资金和库存 | DRAM 高价周期中，大客户用 LTA/预付款锁定供应，小客户库存成本上升 | 价格传导更快，中小模组厂被挤出高端料号 |

### 6.3 成本构成与毛利决定因素

| 产品 | 成本构成估算 | 毛利决定因素 |
|---|---|---|
| 192GB SOCAMM2 | DRAM/LPDDR die 75-85%；LPDDR package 4-8%；高阶 PCB 3-6%；PMIC/SPD/VR/连接器/thermal 4-8%；组装测试 4-7%；RMA/质保 1-3% | LPDDR5X bin、NVIDIA/Vera 认证、DRAM 合约价、模组良率、是否 192GB/256GB premium SKU |
| DDR5 128/256GB RDIMM | DRAM die 70-82%；PCB 3-5%；RCD/DB/SPD/PMIC/TS 5-10%；组装测试 4-7%；渠道/库存 2-6% | DRAM contract price、高容量 die 供给、RCD/PMIC 短缺、客户 LTA、服务器平台认证 |
| MRDIMM | DRAM die 65-78%；MRCD/MDB/PMIC/SPD 8-15%；PCB 4-7%；测试 5-8%；thermal/mechanical 2-5% | 高速接口芯片、平台 attach rate、带宽溢价、Intel/AMD 支持和 BIOS/FW 成熟度 |
| CXL Type-3 模组/AIC | DRAM 50-65%；CXL controller 15-25%；PCB/E3.S/thermal 5-10%；固件/验证 5-10%；测试 5-8% | controller 供应、cloud validation、CXL software maturity、是否可带来 VM/pod consolidation ROI |
| SOCAMM PCB/连接器 | 材料 35-45%；加工/良率 25-35%；测试 5-10%；折旧/管理 10-15%；客户认证和库存 5-10% | 高速良率、客户认证、层数/材料、产能紧张度 |

### 6.4 价格传导机制

1. **DRAM 厂到 hyperscaler/OEM：** 通过季度/半年合约、LTA、capacity reservation、预付款和价格 escalator 传导；AI 客户优先级高，接受交期溢价。
2. **内存厂到模组/PCB/接口芯片：** SOCAMM/MRDIMM 初期以 design win 和认证锁定，价格弹性大于普通 DIMM。
3. **OEM/ODM 到云厂商：** GPU rack 整柜报价中内存通常被打包，但当 DRAM/SOCAMM 缺货时会以 BOM surcharge 或交付优先级体现。
4. **CXL 产品：** 价格不只按 GB，而按“节省多少 stranded DRAM、减少多少服务器、提高多少 VM/pod density”定价，软件和 controller 有更强价值定价能力。

## 7. 竞争格局与壁垒

### 7.1 市场结构

| 环节 | 市场结构 | 集中度判断 | 谁最有定价权 |
|---|---|---|---|
| DRAM/SOCAMM/DDR5 | 三巨头主导 | Samsung + SK hynix + Micron 占全球 DRAM 绝大多数，高端 AI DRAM 更集中 | DRAM 三巨头，尤其拿到 NVIDIA/云厂认证的供应商 |
| SOCAMM2 模组 | 初期寡头 | 三大内存厂 + 少数芯片/PCB/连接器配套 | 认证内存厂、Rambus 等配套 silicon、首批 PCB 供应商 |
| DDR5 RDIMM | 上游集中，下游模组较分散 | DRAM die 集中，模组品牌/组装分散 | DRAM die 供应商，高容量料号下游议价弱 |
| MRDIMM | 平台/接口芯片寡头 | Intel/CPU 平台 + DRAM 三巨头 + MRCD/MDB 供应商 | 接口逻辑与平台认证厂商 |
| CXL memory | 早期分散但 controller 集中 | controller/switch/IP 有高壁垒，模组和系统仍早 | Astera/Marvell/Microchip/XConn/Montage 等 controller + 云平台 |
| 模组 PCB/连接器 | 中度集中，高端料号更集中 | 普通 PCB 分散，SOCAMM/MRDIMM 高速料号集中 | 通过客户认证和高速良率爬坡的 PCB/连接器厂 |

### 7.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 定价逻辑 |
|---|---|---|
| DRAM 先进制程和良率 | 高容量 DDR5/LPDDR5X/SOCAMM/HBM 都依赖 1b/1c/1γ DRAM 与 EUV/良率 | 供给不是短期可复制，客户用价格换确定交期 |
| 平台认证 | AI rack 内存要通过 NVIDIA/AMD/Intel/云厂长周期验证 | 认证料号可以拿 premium，未认证产品只能打低端 |
| 高速信号完整性 | MRDIMM、SOCAMM、CXL 都接近链路极限，SI/PI/thermal 共同约束 | 低误码率和稳定性可直接转化为溢价 |
| 软件/固件栈 | CXL/PNM/pooling 不只是硬件，涉及 OS、hypervisor、K8s、fleet telemetry | 能把硬件变成 TCO 改善的厂商才有长期高毛利 |
| 客户锁定/LTA | Hyperscaler 为保证机柜上电和 GPU 利用率，会提前锁内存 | 大客户绑定提高收入可见度，也形成小客户供给挤出 |
| 切换成本 | 内存出错会导致 rack instability；更换供应商需重新认证和 burn-in | 客户不愿为小幅降价承担稳定性风险 |
| 规模和资本开支 | DRAM fab、测试、模组高阶产线都需高资本投入 | 景气期供给弹性慢，价格可维持较长 |

### 7.3 价值链中最可能长期高 ROIC/高毛利的层

| 排名 | 层级 | 长期高 ROIC 原因 |
|---:|---|---|
| 1 | DRAM/SOCAMM/HBM 头部内存厂 | 三寡头、资本密集、客户认证强，AI memory mix 把历史周期股毛利上限抬高 |
| 2 | CXL/controller/MRDIMM/SOCAMM 接口 silicon | Fabless 轻资产、高速 SerDes/协议/firmware 壁垒强，毛利可维持 60-80% |
| 3 | CXL pooling/AI memory orchestration 软件 | 若成为 cloud 内部调度层，软件毛利 70-90%，且能影响硬件采购 |
| 4 | SOCAMM/MRDIMM 高阶 PCB/连接器 | 单位价值小但稀缺弹性大，认证和良率提高进入壁垒 |
| 5 | 普通模组组装/渠道 | 需求强时盈利改善，但长期同质化，ROIC 低于上游和接口 silicon |

## 8. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点 1：SOCAMM2 从样品进入 AI 机柜量产

2026H2 Vera/Rubin 合作伙伴产品供应后，SOCAMM2 将首次在 AI 数据中心形成数百万到千万级模组需求。最可能放量方向是 **192GB SOCAMM2 + SOCAMM2 chipset/PCB/connector**。极度乐观情景下，2026 年底 SOCAMM2 单季度市场就可能超过 $8-10B。

### 拐点 2：DDR5 高容量模组进入卖方市场

HBM4 抢产能、AI host 内存容量上移、服务器 DDR5 价格上涨共同推动 128GB/256GB RDIMM 供不应求。最可能放量方向是 **256GB RDIMM、3DS RDIMM、PMIC/RCD/SPD**。

### 拐点 3：MRDIMM/CXL 由“架构选项”变成客户教育重点

2026 的 MRDIMM 已经有平台抓手，CXL 有 Azure preview 和 CXL 4.0 远期标准锚点。最可能放量方向是 **MRDIMM Gen1 高端服务器、CXL Type-3 memory expansion pilot、CXL controller**。

## 9. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点 1：256GB SOCAMM2 与 LPDDR6 SOCAMM 开始替代 192GB

如果 Rubin 和后续 AI CPU rack 继续按高带宽低功耗路线推进，SOCAMM 将从单一 NVIDIA 供应链扩散到更多专用 CPU/ASIC rack。最可能放量方向是 **256GB SOCAMM2、LPDDR6 SOCAMM、SOCAMM thermal/power management**。

### 拐点 2：CXL pooling 进入生产化

2027 的关键不是 CXL 4.0 是否大量出货，而是 CXL 2.0/3.x 是否在 hyperscaler 内部证明能提高 memory utilization、VM density、KV cache TCO。最可能放量方向是 **CXL memory appliance、CXL switch/controller、Kubernetes/Redfish/fabric manager 软件**。

### 拐点 3：AI host memory 从“容量采购”转为“带宽/延迟/功耗分层采购”

AI rack 会同时采购 HBM、SOCAMM、DDR5/MRDIMM、CXL memory、eSSD/KV cache storage。2027 最可能的子方向是 **MRDIMM Gen2、高容量 DDR5、CXL-PNM、near-memory vector search**。

## 10. 头部公司清单

### 10.1 DRAM、SOCAMM、DDR5、MRDIMM

| 细分 | 头部公司 | 关注点 |
|---|---|---|
| 高端 DRAM/LPDDR/SOCAMM | Samsung、SK hynix、Micron | 三大核心供应商；谁拿到 Vera/Rubin/SOCAMM2 认证和 256GB 良率，谁获得最大溢价 |
| 中国 DRAM 追赶 | CXMT、福建晋华相关生态、Nanya、Winbond | 中低端 DDR/LPDDR 受益国产替代；高端 AI SOCAMM/HBM 仍有差距 |
| DDR5 RDIMM/MRDIMM 模组品牌/组装 | Kingston、SMART Modular、Innodisk、ADATA、Apacer、Transcend、Teamgroup、V-Color、Memblaze/企业存储生态 | 普通组装利润低，高容量认证料号和工业/服务器渠道有弹性 |
| MRDIMM 平台 | Intel、AMD、Micron、Samsung、SK hynix | Xeon 6 是初期抓手，AMD/其他 CPU 平台支持决定 2027 上限 |

### 10.2 Interface chips、CXL、控制器

| 细分 | 头部公司 | 关注点 |
|---|---|---|
| DDR5 RCD/DB/MRCD/MDB/SPD | Montage Technology、Rambus、Renesas、Microchip、IDT legacy、澜起科技 | MRDIMM 和高容量 DDR5 提高单模组逻辑价值 |
| SOCAMM2 chipset | Rambus、DRAM 厂自研/合作生态 | 直接绑定 Vera/Rubin，attach rate 近 100% |
| PMIC/VR/电源管理 | Renesas、Monolithic Power、TI、Analog Devices、Infineon、Richtek、Silergy | DDR5/SOCAMM 高功耗动态管理和可靠性要求提高 |
| CXL controller/switch/retimer | Astera Labs、Marvell、Microchip、XConn、Montage、Rambus、Broadcom、Credo（相邻互连） | controller + firmware + cloud validation 是高毛利层 |
| IP/EDA/验证 | Synopsys、Cadence、Siemens EDA、Rambus、Avery/Synopsys VIP、Keysight | CXL/PCIe/MRDIMM/SOCAMM 合规和验证需求增长 |

### 10.3 PCB、连接器、测试

| 细分 | 头部公司 | 关注点 |
|---|---|---|
| 内存模组 PCB | Simmtech、Daeduck、TLB、Korea Circuit、Tripod、Unimicron、Nan Ya PCB、Shennan Circuits、WUS、SCC | SOCAMM/MRDIMM 高速高密度 PCB 是最有弹性的子环节 |
| 连接器/插座 | Amphenol、TE Connectivity、Molex、LOTES、Foxconn Interconnect、Hirose、JAE | SOCAMM compression、DDR5 DIMM、EDSFF/CXL connector |
| 测试/探针/仪器 | Advantest、Teradyne、FormFactor、Technoprobe、Chroma、Keysight、Anritsu | 高容量 DRAM、CXL compliance、高速 SI/PI 测试 |
| 热管理相邻 | Delta、Auras、Nidec、Cooler Master server arm、Vertiv、nVent、Boyd、Laird | SOCAMM/DDR5 单体不是液冷核心，但 AI rack 内热密度提升带来模组级 thermal 价值 |

### 10.4 系统/OEM/云客户

| 细分 | 头部公司 | 关注点 |
|---|---|---|
| AI server OEM/ODM | Dell、HPE、Lenovo、Supermicro、Foxconn、Quanta、Wiwynn、Inventec、QCT、Gigabyte、ASUS server | 决定内存模组认证、BOM 打包和交付节奏 |
| 云/AI lab 客户 | Microsoft Azure、AWS、Google Cloud、Meta、Oracle、OpenAI、CoreWeave、Crusoe、Lambda、Vultr、Nebius、xAI | LTA/预付款/机柜架构决定内存路线 |
| 标准组织 | JEDEC、CXL Consortium、OCP、PCI-SIG、SNIA | 标准成熟度决定多供应商生态和价格竞争节奏 |

## 11. 投资含义：按确定性与弹性排序

| 排名 | 方向 | 2026 投资含义 | 风险 |
|---:|---|---|---|
| 1 | SOCAMM2 供应链 | 最强新增品类，从近零到数十亿美元；DRAM 厂、Rambus、PCB/连接器弹性大 | Rubin 交付延迟、SOCAMM 良率、NVIDIA 改版 |
| 2 | 高容量 DDR5 RDIMM/3DS RDIMM | 现金流最确定，DRAM 涨价和 AI host 容量上移支撑利润 | DRAM 扩产、客户推迟 capex、价格监管/议价 |
| 3 | MRDIMM | 小基数高增速，接口芯片价值高 | 平台支持不足、功耗/热和 BIOS 稳定性 |
| 4 | CXL controller/memory appliance | 2027 期权大，controller 和软件毛利高 | CXL 软件栈成熟慢、客户 pilot 停留时间长 |
| 5 | 模组 PCB/连接器 | 单位价值小但 SOCAMM/MRDIMM 认证带来溢价 | 产能扩张后 ASP 下滑，客户集中度高 |
| 6 | 普通模组组装 | 周期弹性有，但长期壁垒较低 | DRAM 厂直供、大客户压价、库存风险 |

## 12. 风险与反证指标

| 风险 | 观察指标 |
|---|---|
| Rubin/Vera 延期 | NVIDIA/ODM 对 2026H2 partner availability 是否改口；SOCAMM2 订单是否延后 |
| HBM4 抢产能导致 SOCAMM 供应不足 | 三大内存厂 capex、HBM4 qualification、LPDDR5X server bin 良率 |
| DRAM 价格过快上涨压制下游 | OEM/NeoCloud 毛利、服务器交付延期、hyperscaler 是否要求重谈价格 |
| CXL 商业化慢 | Azure CXL VM 是否 GA；AWS/GCP/Oracle 是否跟进；Linux/K8s 支持是否成熟 |
| MRDIMM 生态受限 | Intel/AMD 平台支持、MRDIMM 兼容性问题、客户实际 attach rate |
| SOCAMM 被单一平台锁定 | 是否只有 NVIDIA Vera/Rubin 采用；AMD/Arm/custom ASIC rack 是否跟进 |

## 13. 资料来源

| 类别 | 来源 |
|---|---|
| NVIDIA Vera/Rubin/SOCAMM 需求 | [NVIDIA Vera CPU 技术博客](https://developer.nvidia.com/blog/nvidia-vera-cpu-delivers-high-performance-bandwidth-and-efficiency-for-ai-factories)，[NVIDIA Vera Rubin 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)，[NVIDIA Vera Rubin 官方新闻稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) |
| SOCAMM2 产品 | [Micron SOCAMM2 官方页面](https://www.micron.com/products/memory/lpddr-modules/socamm)，[Samsung SOCAMM2 官方页面](https://semiconductor.samsung.com/dram/module/socamm2/)，[SK hynix SOCAMM2 新闻稿](https://news.skhynix.com.cn/mass-production-socamm2-192gb/)，[Rambus SOCAMM2 chipset 新闻稿](https://www.rambus.com/rambus-enables-power-efficient-ai-platforms-with-socamm2-server-module-chipset/) |
| DDR5/MRDIMM | [Micron MRDIMM 官方页面](https://www.micron.com/products/memory/dram-modules/mrdimm)，JEDEC MRDIMM/DDR5 公开标准进展，Intel Xeon 6/MRDIMM 生态资料 |
| CXL | [CXL Consortium 4.0 specification announcement](https://www.businesswire.com/news/home/20251118275848/en/CXL-Consortium-Releases-the-Compute-Express-Link-4.0-Specification-Increasing-Speed-and-Bandwidth)，Samsung CXL webinar 公开资料，Micron CZ120/CZ122 CXL memory module 资料，Astera Labs Leo CXL controller/Microsoft Azure preview 资料 |
| 市场规模 | [Gartner 2026/2027 semiconductor forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)，IDC/TrendForce 公开摘要，Micron/Samsung/SK hynix 2026 财报与新闻稿 |
| 项目内底座 | `ai_chip_research_2026_2027.md`、`conference_update/nvidia_gtc_2026_research.md`、`conference_update/cxl_vertical_optimization_2026.md`、`conference_update/xcelerated_compute_show_2026_report.md` |

# 行业调研：【先进封装材料与热界面材料】

> 截至日期：2026-05-08  
> 研究口径：聚焦 AI 计算中心建设带动的先进封装材料、先进封装相关基板/介质/化学品、热界面材料（TIM）及其上游填料/金属/树脂。除特别说明外，美元金额为全球口径；“未来 3 个月”指 2026-05-08 至 2026-08-08，“未来 1 年”指至 2027-05，“未来 2 年”指至 2028-05。  
> 方法说明：AI 芯片技术路径和 2026-2027 出货排序主要引用本项目已有的 `ai_chip_research_2026_2027.md`、GTC 2026、Xcelerated Compute Show 2026 等本地研究；外部搜索重点用于材料、TIM、封装服务、公司公告和行业市场规模交叉验证。  
> 投资假设：对 2026-2027 年 AI 计算中心建设保持明确乐观。凡直接公开数据缺失处，采用“算力出货、封装面积、HBM stack、机柜功率、材料单耗”自下而上做乐观推演，并标明为估算。

## 0. 一页结论

**核心判断：2026 年先进封装材料与 TIM 的主线是“CoWoS/HBM3E/HBM4 供给瓶颈 + 100kW 级液冷机柜 + 1kW+ 单芯片热流密度”共同把材料从低弹性辅材重新定价为 AI 基础设施的准瓶颈资产。** GPU/ASIC 的价值最大，但材料的边际利润弹性很可能更好：封装面积放大、HBM stack 数增加、良率压力上升、液冷 attach rate 提升，使 underfill、ABF/低 CTE 载板、RDL 介质、临时键合材料、molding compound、TIM1/TIM1.5/TIM2、金属 TIM、导热填料和冷板界面材料的价值量上升。

### 0.1 最重要数字

| 指标 | 2026 基准 | 2026 乐观 | 2026 极度乐观 | 2027-2028 方向 |
|---|---:|---:|---:|---|
| 全球 AI 计算芯片/模块产能释放金额（项目内锚点） | $300B-$360B | $390B-$470B | $520B-$650B | 2027 极度乐观可到 $850B-$1,050B |
| 全球 AI/HPC 先进封装服务收入池，含 CoWoS/2.5D/3D/高端 OSAT 服务 | $32B-$45B | $45B-$62B | $65B-$85B | 2028 可接近 $90B-$140B |
| 全球 AI/HPC 先进封装材料与高端基板收入池，不含服务费 | $8.5B-$12B | $12B-$17B | $18B-$25B | 2028 可到 $24B-$40B |
| 全球 AI 数据中心/AI 服务器 TIM 与导热材料收入池 | $0.9B-$1.5B | $1.4B-$2.4B | $2.2B-$3.6B | 2028 可到 $3.5B-$7.5B |
| CoWoS/2.5D 关键材料价值量/高端 GPU 或 XPU package | $450-$900 | $800-$1,500 | $1,300-$2,500 | HBM4 与更大 interposer 后继续上升 |
| TIM/导热界面价值量/高端加速器模块 | $20-$80 | $60-$180 | $150-$450 | 裸 die、metal TIM、cold-plate attach 后显著上升 |
| TIM/导热界面价值量/GB300/Rubin/Helios 类高密度整机柜 | $3,000-$12,000 | $10,000-$35,000 | $30,000-$90,000 | 取决于 TIM2、gap filler、冷板、维护备件和液冷架构 |

### 0.2 2026 最可能放量的材料路径

1. **ABF/FC-BGA 大尺寸高层数载板 + 低 CTE 树脂/玻纤体系**：AI GPU/ASIC 封装面积、层数和电源完整性要求持续上升，ABF 仍是 2026 最大美元池。
2. **CoWoS-S/L/RDL interposer + HBM3E/HBM4 周边材料**：underfill、micro-bump/flux、molding、RDL dielectric、Cu plating、CMP/cleaning 是最直接受益项。
3. **大 die/HBM 封装 underfill 与低应力 molding compound**：AI 封装翘曲、热循环、湿热可靠性难度上升，客户愿意为低 void、低 CTE、低 alpha、高 Tg 付溢价。
4. **高性能 TIM2/phase-change pad/gel/putty + 冷板界面材料**：GB200/GB300、Rubin、MI400、Maia200、Trainium3 等高密度液冷机柜提高 TIM attach rate。
5. **金属 TIM/indium foil/solder TIM、液态金属、CNT/graphite/diamond 复合 TIM 的局部导入**：2026 仍不是最大收入池，但 2027-2028 赔率最高。
6. **临时键合/解键合、hybrid bonding 表面处理与清洗材料**：HBM4、SoIC、X-Cube/Foveros/EMIB-T 类先进封装放量后，验证期长但利润率高。

### 0.3 反共识

市场通常把“先进封装”理解为 TSMC/ASE/Amkor 的服务收入，或者把“散热”理解为冷板/CDU。真正被低估的是**中间材料层**：这些材料单价低于 GPU，但认证周期长、失效代价极高、客户切换成本高，且毛利率有机会高于多数封装代工和整机 OEM。2026 年若 AI 服务器从 70-120kW/rack 迈向 150kW/rack，TIM/导热填料/低 CTE 封装材料的供需弹性会比传统电子化学品更像“高壁垒耗材”。

### 0.4 近半年/2026 论坛、报告与一手事件清单

| 时间 | 事件/来源 | 关键事实 | 对先进封装材料与 TIM 的含义 |
|---|---|---|---|
| 2026-02-17 至 2026-02-19 | Chiplet Summit 2026, Santa Clara | 官方动态数据对应 368 条演讲/主持/嘉宾记录、70 个 session、105 个组织；Yole 会议材料给出 HBM 收入约 2025 年 $35B、2026 年 $60B、2027 年 $80B、2031 年 $170B；先进封装 2026 年约 $57.5B | HBM4/Custom HBM、UCIe、CoWoS/EMIB/SoIC、KGD/test/thermal 成为同一供应链问题；材料机会集中在 HBM underfill、RDL、低翘曲 molding、临时键合、TIM |
| 2026-02-24 至 2026-02-26 | DesignCon 2026, Santa Clara | 100+ sessions、15 tracks、183 篇 technical papers、202 家展商；Best Paper 集中在 448Gbps、PCIe 7.0、top-side interconnect、via/fan-out；本地研究口径下 advanced packaging 2026 约 $49B-$55B，2.5D/3D 2026 约 $12.7B | AI 物理层瓶颈外溢到 package/PCB/connector/thermal；低损耗材料、封装热边界条件、PI/SI/thermal co-design 会提前进入客户 RFP |
| 2026-03-16 至 2026-03-19 | NVIDIA GTC 2026 | NVIDIA 官方会前稿披露 30,000+ 参会者；Vera Rubin 相关产品 2026 H2 partner availability；Rubin NVL72 为 72 Rubin GPU + 36 Vera CPU，1.6PB/s HBM4 带宽，260TB/s NVLink 6 scale-up bandwidth | Rubin/HBM4/液冷把 2027 材料规格提前锁定；metal TIM、低翘曲封装材料、HBM4 underfill 和冷板界面材料进入核心观察名单 |
| 2026-03-23 至 2026-03-24 | The Xcelerated Compute Show 2026, New York | 2026 生态回顾为 550+ decision-makers、150+ speakers、50+ technology providers；会议主题覆盖 memory wall、context memory、CXL、UALink、neocloud、gigawatt planning | 先进封装材料不再只跟训练 GPU，推理、KV cache、AI storage、1.6T 网络和 GW 级供电都会带来导热/封装材料外溢需求 |
| 2026 年公开行业报告 | SEMI、Yole、Grand View、Gartner、Deloitte、TrendForce 等 | Gartner 预计 2026 半导体 $1.320T、AI semis 约占 30%；Deloitte 预计 2026 AI data center capex $400B-$450B，其中 chips $250B-$300B；TrendForce 公开摘要指向 2026 HBM shipment >30B Gb、HBM4 价格 premium >30% | 自上而下验证：AI 材料不是孤立小赛道，而是 AI 半导体、HBM、CoWoS、液冷和数据中心 capex 的交叉瓶颈 |
| 2026 公司公告/产品发布 | NVIDIA、AMD、AWS、Microsoft、Meta/Broadcom、Google、Indium、Henkel、Dow/Carbice 等 | GPU/ASIC 平台均指向更高 HBM、更大 package、更高机柜功率；Indium 在 productronica China 2026 强调面向 next-gen AI systems 的 thermal innovations；Dow/Carbice 推动 CNT TIM；Henkel 持续覆盖半导体封装与 thermal materials | 公司一手信号一致：材料规格向高导热、低应力、低污染、可返修、液冷兼容和长寿命可靠性升级 |

## 1. AI 计算中心建设给行业带来的机遇与挑战

### 1.1 需求侧：从 GPU 供给紧缺扩散到封装、材料和热管理紧缺

本项目 AI 芯片研究给出的 2026 需求锚点是：全球 AI 计算芯片/模块产能释放金额基准 $300B-$360B，乐观 $390B-$470B，极度乐观 $520B-$650B；2027 年基准 $430B-$520B，乐观 $590B-$720B，极度乐观 $850B-$1,050B。NVIDIA Blackwell/GB300 是 2026 主力，Rubin 从 2026 H2 进入首批量产；Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA、OpenAI/Broadcom 等 custom ASIC 同步从内部优化工具变成独立产能池。

对材料行业的意义不是简单跟随 GPU 数量，而是 **package 面积、HBM stack、互连密度、热流密度、机柜功率**同时上升：

- 每颗高端 GPU/ASIC 通常绑定 6-12 个 HBM stack；HBM4 初期验证、base die 和 TSV 良率决定 Rubin/MI400/TPU8 节奏。
- TSMC CoWoS 2026 年底公开估计产能约 11.5-14 万片/月，2027 年约 17 万片/月；每一次扩产都拉动 ABF/玻纤/underfill/介质/化学品/TIM。
- NVIDIA GTC 2026 对 Rubin NVL72、LPX、STX、Spectrum-6、DSX 的描述表明，AI factory 目标函数从 FLOPS 转成 tokens/watt、tokens/sec、revenue/GW。热界面材料不再只是可靠性辅材，而是 tokens/W 的变量。
- Microsoft Maia 200 已明确 750W SoC TDP 和闭环液冷；NVIDIA GB300/Rubin、AMD Helios、AWS Trainium3、Google TPU pod 都把液冷从选项推成默认趋势。

### 1.2 2026 使用中的关键技术

| 技术 | 2026 使用状态 | 关键材料/产品 | 对 AI 芯片的意义 |
|---|---|---|---|
| CoWoS-S/L/R | 高端 GPU/ASIC 主流；TSMC 仍是核心瓶颈 | 硅 interposer/RDL interposer、ABF/FC-BGA、underfill、molding、RDL dielectric、Cu plating、CMP slurry、flux | 连接 GPU die 与 HBM，决定 HBM 带宽和封装面积 |
| HBM3E 封装 | 2026 主力 | TC bonding 材料、micro-bump、underfill、molding、thermal spreader、KGD test materials | Blackwell Ultra、MI350、Maia200、Ironwood 主力 |
| HBM4 封装 | 2026 H2 进入验证/早期放量 | hybrid bonding/TC bonding、低翘曲 molding、underfill、高导热 TIM、base die | Rubin、MI400/MI455X、TPU8、下一代 ASIC 的核心瓶颈 |
| ABF/FC-BGA 大载板 | 全面放量 | ABF build-up film、低 CTE core、玻纤布、Cu foil、solder mask、低损耗树脂 | 面积、层数、供电、信号完整性同步上升 |
| EMIB/Foveros/SoIC/X-Cube | 部分平台与下一代封装采用 | 混合键合表面处理、临时键合胶、die attach、underfill、RDL dielectric | 2027-2028 更重要，2026 以高端验证和小批量为主 |
| TIM1/TIM1.5 | 部分 GPU/ASIC die-to-lid 或 die-to-cold-plate 使用 | solder TIM、indium foil、phase-change、liquid metal、silicone-free TIM、CNT sheet | 解决 die hotspot、pump-out、热循环和长期可靠性 |
| TIM2/冷板界面 | 液冷机柜快速放量 | phase-change pad、gap filler、thermal gel、putty、graphite sheet、adhesive | 100kW+ rack 的可维护性和热阻瓶颈 |
| 冷却液/浸没液 | 仍以 direct-to-chip 水/乙二醇为主，浸没在部分场景试点 | 低腐蚀冷却液、密封材料、fluorinated fluids、PAO/ester fluids | 2026 收入更多在系统侧，材料端需要长期认证 |

### 1.3 2026-2027 最大挑战

1. **材料认证慢于芯片路线图**：高端 underfill/TIM/ABF 通常需要 6-18 个月客户认证；AI 芯片代际 12 个月刷新，材料供应商必须提前介入 design-in。
2. **翘曲和热膨胀失配**：GPU die、HBM、硅 interposer、有机载板、金属 lid、冷板 CTE 差异巨大；封装面积越大，warpage 越像良率杀手。
3. **TIM 泵出、干裂、金属腐蚀和可返修性**：1kW+ 加速器和液冷热循环会放大 TIM2 pump-out；液态金属/indium 方案导热好但腐蚀、迁移、返修和成本难度高。
4. **HBM4 与封装良率耦合**：HBM4 需要更高带宽、更高 I/O 密度和更复杂 base die；任何 KGD、bonding 或 underfill 缺陷都会放大到整包价值损失。
5. **低 alpha、高纯度和离子污染控制**：先进封装靠近逻辑 die 和 HBM，材料的 Cl/Na/K、outgassing、alpha 粒子、湿热可靠性要求高，筛选掉大量普通电子化学品供应商。
6. **PFAS/环保合规与供应链地缘风险**：高性能冷却液、某些氟材料、特殊溶剂和清洗剂面临法规压力；日韩美欧材料链和中国本土替代链会走向双轨。
7. **客户集中和议价错配**：头部芯片/云厂话语权强，但材料若进入 AVL 后切换成本高；中小供应商有技术壁垒，却可能被长账期和扩产资金压制。

## 2. 出货量最大的 AI 芯片路径对材料的拉动

### 2.1 2026-2027 出货量/价值最大的 10+ 平台与材料映射

| 芯片/平台 | 2026-2027 阶段 | 封装/内存路径 | 散热路径 | 直接受益材料 |
|---|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 最确定主力 | TSMC 4NP + CoWoS-L/S + HBM3E + 大尺寸 ABF | NVL72 全液冷/冷板 | ABF、underfill、molding、RDL dielectric、TIM2、gap filler、冷板密封材料 |
| NVIDIA B200/GB200 | 存量大、2026 继续交付 | CoWoS + HBM3E | 液冷为主，部分风液混合 | 与 GB300 类似，但材料单耗略低 |
| NVIDIA Vera Rubin/Rubin NVL72 | 2026 H2 小批量，2027 主力 | HBM4 + 更大 CoWoS/advanced packaging + NVLink 6 | 液冷默认，热流密度更高 | HBM4 underfill、低翘曲材料、metal/PCM TIM、hybrid bonding 周边材料 |
| AWS Trainium2 | 2026 大规模部署，Rainier 主力 | HBM + custom package | 液冷/风液混合 | ABF、underfill、TIM2、系统级 gap filler |
| AWS Trainium3 | 2026 初放量，2027 主力 | 3nm + HBM3E 级内存 + 144 芯片 UltraServer | 高密度液冷 | 大载板、underfill、TIM2、高可靠冷板界面 |
| Google TPU v7 Ironwood | 2026 云端放量 | Broadcom/TSMC 生态 + HBM3E | 大规模数据中心液冷趋势 | HBM 封装材料、ABF、TIM2、冷板材料 |
| Google TPU8 | 2026 设计/早期，2027 放量 | 训练/推理分化，可能 HBM4/更先进节点 | 液冷 | HBM4、hybrid bonding、低 CTE 材料 |
| AMD MI350/MI355X | 2026 AMD 最确定放量 | HBM3E + OAM/UBB/PCIe | 液冷选项增加 | ABF、underfill、TIM、PCIe/OAM 级导热垫 |
| AMD MI400/MI455X Helios | 2026 H2 首批，2027 重要 | HBM4 + 72 GPU rack | 全液冷 | HBM4 材料、CoWoS-L/2.5D、TIM2/metal TIM、高导热填料 |
| Microsoft Maia 200 | 2026 Azure 推理导入 | TSMC 3nm + 216GB HBM3E | 750W SoC + 第二代闭环液冷 | HBM3E 封装材料、TIM2、冷板密封/界面 |
| Meta MTIA 300/400/450/500 | 2026-2027 多代 ASIC | Broadcom XPU + advanced packaging | OCP rack，风液混合转液冷 | ASIC 载板、underfill、molding、TIM、低成本高可靠材料 |
| Huawei Ascend/Cambricon/国产 ASIC | 中国替代需求强 | 国产 2.5D/HBM/大载板能力爬坡 | 风液到液冷 | 国产 ABF、underfill、TIM、molding、导热填料替代链 |

### 2.2 新技术成熟与放量时间：三情景

| 技术 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---|---|
| CoWoS-L/S 大尺寸 2.5D | 2026 全年紧缺，2027 产能改善但仍排队 | 2026 H2 OSAT/外包承接更多后段，2027 交付明显改善 | 2026 Q4 即进入“可交付但被预定”状态，材料订单被 2027 需求提前锁定 |
| HBM4 封装材料 | 2026 H2 小批量验证，2027 H1 主力 ramp | 2026 Q4 Rubin/MI400/TPU8 多平台同步拉动 | 2026 H2 多供应商良率超预期，HBM4 underfill/TIM 溢价持续到 2028 |
| hybrid bonding/SoIC/X-Cube 材料 | 2026 高端验证，2027 小规模收入化 | 2027 被高端 GPU/ASIC/HBM base die 广泛采用 | 2027 直接成为下一代 AI package 的差异化瓶颈 |
| 玻璃基板 | 2026 R&D/样品，2027 小规模试产 | 2027 H2 头部客户导入小批量 AI ASIC | 2028 前形成高端封装第二载板路线，分流部分 ABF 紧缺 |
| Panel-level packaging/CoPoS | 2026 仍以验证和非最顶级 AI 为主 | 2027 在 RDL interposer/large package 成本优化中放量 | 2027 H2 获得 hyperscaler ASIC 设计 win，材料用量指数放大 |
| 金属 TIM/液态金属/CNT TIM | 2026 局部导入，TIM2 仍以 PCM/gel/pad 为主 | 2027 高端 Rubin/MI400/ASIC 采用率快速提高 | 2027 成为 premium AI rack 标配，TIM ASP 翻倍以上 |
| CPO/硅光封装材料 | 2026 switch 端早期部署，材料收入小 | 2027 1.6T/CPO 放量，光学胶、underfill、封装基板起量 | 2027 CPO 从 switch 向 AI rack fabric 加速，材料成为新利润池 |

## 3. 已经开始放量的关键产品：市场规模、渗透率、利润率

### 3.1 当前放量产品总表

| 产品/细分技术 | 当前状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 主要公司 |
|---|---|---:|---:|---:|---|---|
| ABF/FC-BGA 高端 AI 载板 | 已放量，AI GPU/ASIC 必需 | $1.2B-$2.0B | $5.5B-$9.5B | $9B-$17B | 高端 GPU/ASIC 近 100%；AI 价值占 ABF 总需求 35%-55% | Ajinomoto、Ibiden、Shinko、Unimicron、Nan Ya、Kinsus、AT&S、SEMCO、Kyocera |
| CoWoS/2.5D underfill/encapsulant | 已放量，随 CoWoS 紧缺 | $180M-$350M | $850M-$1.8B | $1.8B-$4.0B | 高端 HBM package 近 100%；高端材料替代中低端 | Henkel、Namics、Resonac、Sumitomo Bakelite、Shin-Etsu、Nagase |
| RDL dielectric/PSPI/PBO/BCB | 已放量，RDL/CoWoS/PLP 受益 | $200M-$420M | $950M-$2.0B | $1.8B-$4.5B | AI advanced package attach 40%-65%，2028 可到 70%+ | DuPont/HD MicroSystems、JSR、TOK、Merck、Fujifilm、Toray、Sumitomo Chemical |
| 临时键合/解键合材料 | HBM/2.5D/3D 生产持续放量 | $80M-$180M | $350M-$850M | $800M-$2.0B | advanced packaging wafer handling 渗透 30%-55%，2028 60%+ | Brewer Science、3M、TOK、JSR、DuPont、Merck |
| Cu plating/CMP/clean/flux | 已放量，随 RDL/micro-bump 增长 | $250M-$500M | $1.2B-$2.6B | $2.2B-$5.0B | advanced package 全流程消耗品，随产能线性增长 | MKS/Atotech、Uyemura、Okuno、Entegris、Fujimi、CMC/Entegris、JX Metals、Tanaka |
| 低应力 molding compound | HBM/SiP/2.5D 放量 | $120M-$260M | $600M-$1.3B | $1.2B-$2.8B | 高端 AI package 渗透 35%-60%，2028 65%+ | Sumitomo Bakelite、Resonac、Shin-Etsu、Panasonic、Nagase、Kyocera |
| 高性能 TIM2/PCM/pad/gel/putty | GB200/GB300/液冷 rack 放量 | $220M-$450M | $1.0B-$2.1B | $2.0B-$5.0B | 液冷 AI rack 2026 35%-55%，2028 70%-90% | Henkel/Bergquist、Honeywell、DuPont/Laird、Parker、Fujipoly、Shin-Etsu、Boyd、3M、Dow |
| 金属 TIM/indium/solder TIM | 已在高热流应用导入 | $25M-$70M | $120M-$450M | $450M-$1.6B | 高端 bare die/AI module 2026 3%-8%，2028 15%-35% | Indium Corp、Honeywell、Henkel、Shin-Etsu、MacDermid Alpha、AIM Solder |
| 导热填料：BN/AlN/氧化铝/石墨/碳材料 | 已随 TIM 同步放量 | $180M-$380M | $850M-$1.9B | $1.8B-$4.2B | 高导热 TIM 中高填充体系渗透提升 | Denka、Tokuyama、Momentive、3M、Saint-Gobain、Resonac、SGL Carbon、NeoGraf、Kaneka |

### 3.2 三情景增长与利润率

| 产品 | 基准：未来 1 年增长/利润率 | 乐观：未来 1 年增长/利润率 | 极度乐观：未来 1 年增长/利润率 | 定价原因 |
|---|---|---|---|---|
| ABF/高端载板 | +25%-45%；基板厂 GM 22%-35%，材料端 45%-65% | +45%-70%；高端产线 GM 35%-45% | +80%+；紧缺品类溢价 20%-40% | 认证长、尺寸/层数/良率难、Ajinomoto ABF 材料锁定强 |
| underfill/encapsulant | +35%-60%；GM 40%-55% | +60%-90%；GM 50%-62% | +100%+；GM 60%-70% | 失效代价极高，客户不愿换料；大 package 低 void 难度高 |
| RDL dielectric/PSPI | +30%-55%；GM 45%-60% | +60%-85%；GM 55%-68% | +100%+；GM 65%-75% | 高纯度、低应力、低 Dk/Df、光刻适配形成壁垒 |
| 临时键合/解键合 | +40%-70%；GM 50%-65% | +80%-120%；GM 60%-72% | +150%+；GM 70%+ | 晶圆级工艺窗口窄，客户认证和设备配套强 |
| molding compound | +25%-45%；GM 30%-45% | +45%-70%；GM 40%-52% | +90%+；GM 50%-60% | 低翘曲、低 alpha、高热导和高可靠配方更稀缺 |
| TIM2/PCM/pad/gel | +45%-75%；GM 35%-55% | +80%-120%；GM 50%-65% | +150%+；GM 60%-75% | 液冷 rack attach rate 提升，现场返修和长期可靠性带来锁定 |
| 金属 TIM/indium | +80%-150%；GM 45%-65% | +200%+；GM 55%-75% | +300%+；GM 70%+ | 热阻优势明显，但可制造/腐蚀/返修限制使合格供应商少 |
| 导热填料 | +35%-60%；GM 25%-45% | +60%-100%；GM 35%-55% | +120%+；特种填料 GM 55%+ | BN/AlN/diamond/CNT 高纯高粒径控制稀缺 |

## 4. 在研关键产品和未来快速增长技术

### 4.1 研发/早期导入技术

| 技术/产品 | 当前阶段 | 未来 3 个月 | 未来 1 年 | 未来 2 年 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| 玻璃核心基板 | Intel、Samsung、日系/美系材料链积极验证 | $10M-$40M | $50M-$220M | $250M-$1.2B | AI 高端 package 2026 <1%，2028 3%-10% | 早期 GM 50%-70%，但良率和设备折旧高 |
| Panel-level RDL/CoPoS/FOPLP 材料 | 试产/验证 | $20M-$80M | $120M-$500M | $600M-$2.0B | AI advanced package 2026 1%-3%，2028 8%-20% | 材料 GM 45%-65%，良率成熟后服务端降价 |
| hybrid bonding 表面处理/介质/清洗 | HBM4/SoIC/X-Cube 受益 | $70M-$150M | $350M-$1.0B | $1.2B-$3.0B | HBM4/3D package 渗透 2026 5%-10%，2028 25%+ | GM 55%-75%，因为 defect tolerance 极低 |
| CPO/硅光封装胶材/基板/热材料 | 交换机侧导入 | $30M-$100M | $250M-$900M | $1.0B-$3.2B | AI backend 2026 <3%，2028 15%-30% | 光学级材料 GM 50%-70% |
| liquid metal/低腐蚀金属 TIM | 实验室到小批量 | $10M-$40M | $80M-$300M | $350M-$1.5B | 高端 GPU/ASIC 2026 <3%，2028 10%-25% | 合格品 GM 60%-80%，失败风险高 |
| CNT/碳纳米管 TIM | Carbice/Dow 等推动 | $20M-$70M | $100M-$350M | $350M-$1.2B | 高端模块 2026 1%-4%，2028 8%-20% | 早期 GM 55%-75%，规模化后 45%-60% |
| diamond/AlN/BN 高导热复合 TIM | 高热流密度预研 | $20M-$60M | $120M-$450M | $500M-$1.8B | 高端 AI package 2026 2%-5%，2028 10%-25% | 特种填料利润高，但成本和供应受限 |
| microfluidic/on-package cooling 材料 | 研发/少量 HPC | <$20M | $50M-$180M | $200M-$900M | 2028 前仍小众，但热瓶颈严重时弹性大 | 材料/工艺 GM 高，系统可靠性是瓶颈 |
| 封装内去耦/背面供电相关介质 | 设计导入 | $20M-$80M | $150M-$600M | $700M-$2.0B | 随 2nm/背供电/HBM4E 增长 | 高纯介质/薄膜 GM 50%-70% |

### 4.2 最可能超预期的 5 条路线

1. **metal TIM 从小众走向 premium AI rack**：若 Rubin/MI400/下一代 ASIC 的 die hotspot 超过传统 PCM/gel 可承受范围，indium/solder/liquid metal 会从 5% 以下渗透率快速迈向 15%-25%。
2. **hybrid bonding 材料提前收入化**：HBM4/HBM4E 的 base die、逻辑 die 叠层和 SoIC/Foveros/X-Cube 会放大表面处理、临时键合、清洗和检测消耗。
3. **CPO 封装材料被 1.6T/3.2T 网络带动**：AI backend Ethernet 和 Spectrum-6/Tomahawk/Jericho 生态若加速，光学级胶材、低损耗基板、热管理材料会从几千万美元快速变成十亿美元级。
4. **AI storage/KV cache 让 eSSD 和导热材料外溢**：长上下文 agent 把存储和内存变成热源，SSD controller/NAND 模组 TIM、gap filler、散热片也会升级。
5. **国产替代链条出现局部高溢价**：中国国产 AI 芯片的先进节点受限，系统级并联更多、功耗更高，对国产 TIM、载板、underfill 的单位价值量可能高于传统消费电子。

## 5. 供给侧：产能结构、瓶颈、成本和价格传导

### 5.1 产能结构

| 环节 | 主要地区 | 头部公司/产能特征 |
|---|---|---|
| CoWoS/2.5D/3D 封装服务 | 台湾为核心，日本/韩国/美国扩张，中国大陆替代链爬坡 | TSMC 主导 CoWoS；ASE/Amkor 承接 OSAT；Intel EMIB/Foveros；Samsung I-Cube/X-Cube；JCET/Tongfu/TFME/Powertech 做区域补充 |
| ABF/FC-BGA 载板 | 日本、台湾、韩国、奥地利/马来西亚、中国大陆 | Ibiden、Shinko、Unimicron、Nan Ya、Kinsus、AT&S、SEMCO、Kyocera；中国厂商加速但高端 AI 良率仍爬坡 |
| ABF build-up film/低 CTE 树脂 | 日本压倒性强势 | Ajinomoto ABF 事实标准；Resonac、Mitsubishi Gas Chemical、Panasonic、味之素生态配套 |
| underfill/molding/die attach | 日本、美国、德国、中国台湾 | Henkel、Namics、Resonac、Sumitomo Bakelite、Shin-Etsu、Panasonic、Nagase、DELO |
| RDL dielectric/PSPI/photoresist | 日本、美国、欧洲 | DuPont/HD MicroSystems、JSR、TOK、Merck、Fujifilm、Toray、Sumitomo Chemical、UBE |
| plating/CMP/清洗 | 日本、美国、德国 | MKS/Atotech、Uyemura、Okuno、Entegris、Fujimi、JX Metals、Tanaka、Mitsubishi Materials |
| TIM/导热材料 | 美国、日本、德国、中国台湾/中国大陆 | Henkel/Bergquist、Indium、Honeywell、Dow、DuPont/Laird、Parker、Fujipoly、Shin-Etsu、Boyd、3M、Denka、Sekisui |
| 导热填料 | 日本、美国、欧洲、中国 | Denka、Tokuyama、Momentive、Saint-Gobain、3M、Resonac、SGL Carbon、NeoGraf、Kaneka、Imerys、Element Six |

### 5.2 供给瓶颈（至少 5 条）

1. **CoWoS 产线与超大尺寸封装设备**：高端 AI package 面积接近或超过多 reticle 级别，曝光、RDL、临时键合、molding、warpage control、final test 都需要专用窗口。
2. **ABF 高端载板良率**：AI package 面积大、层数高、孔密度高，良率提升慢；载板报废会吞掉昂贵 GPU/HBM 价值。
3. **HBM KGD 与 underfill 工艺耦合**：HBM4 每个 stack 价值高，KGD、micro-bump、TC/hybrid bonding 和 underfill 任一环节缺陷都会导致整包损失。
4. **低翘曲封装材料供应**：大 package 对低 CTE、高模量、低应力材料要求同时提高，普通 epoxy/molding 不能直接替代。
5. **TIM 可靠性认证**：高导热 TIM 不只看 W/mK，还要看热阻、厚度控制、泵出、长期 dry-out、腐蚀、绝缘、返修和现场维护。
6. **导热填料纯度和粒径控制**：高导热 TIM 往往需要 BN/AlN/graphite/diamond/CNT 高填充；填料的形貌、表面处理和离子污染决定粘度与可靠性。
7. **临时键合/解键合材料与设备配套**：胶材必须和 SUSS/EVG/TEL 等设备、客户 wafer process 窗口匹配，换料成本高。
8. **人才和工艺经验**：advanced packaging 工艺师、可靠性工程师、热仿真工程师紧缺；材料供应商必须能和封装厂/芯片厂共同 debug。
9. **交付和库存策略**：云厂/GPU 厂开始提前锁定 2027 材料，长周期特殊化学品、金属 indium/gallium、球形 silica、玻纤布可能提前紧张。
10. **法规和出口管制**：PFAS、溶剂、氟冷却液、高纯金属/化学品跨境限制可能造成区域性缺货。

### 5.3 成本拆分与毛利决定因素

#### 单颗高端 AI package 的材料成本示意（不含 HBM/GPU die）

| 项目 | 2026 基准成本 | 乐观/紧缺成本 | 说明 |
|---|---:|---:|---|
| ABF/FC-BGA 载板 | $300-$900 | $800-$1,800 | 面积、层数、良率、供电密度决定 |
| interposer/RDL/介质/化学品分摊 | $80-$250 | $200-$600 | CoWoS-L/RDL 面积越大越高 |
| underfill/flux/molding/die attach | $40-$150 | $120-$400 | HBM stack 数和大 package 可靠性溢价 |
| TIM1/TIM1.5/TIM2 | $15-$80 | $80-$300 | 金属 TIM 或高端 PCM 会显著抬升 |
| 测试/探针/耗材分摊 | $60-$250 | $200-$600 | HBM KGD、package burn-in、SerDes/NVLink 测试 |
| 合计：材料与耗材 | $500-$1,600 | $1,400-$3,700 | 不含封装服务费、设备折旧和 die/HBM |

#### GB300/Rubin/Helios 类液冷机柜 TIM/导热材料价值量示意

| 项目 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| GPU/ASIC TIM2 与冷板界面 | $2,000-$8,000/rack | $8,000-$25,000/rack | $25,000-$65,000/rack |
| CPU/NIC/SSD/VRM gap filler/pad | $800-$3,000/rack | $2,500-$8,000/rack | $6,000-$18,000/rack |
| 维护备件、返修和现场替换 | $300-$1,500/rack | $1,500-$5,000/rack | $5,000-$15,000/rack |
| 合计 | $3,100-$12,500/rack | $12,000-$38,000/rack | $36,000-$98,000/rack |

### 5.4 价格传导机制

- **GPU/ASIC 厂向云客户传导**：HBM、CoWoS、TIM 和载板成本上升通常被打包进整机柜 ASP；在 GPU 紧缺期，客户更在意交期而非材料价格。
- **封装厂向芯片厂传导**：TSMC/OSAT 若产能紧缺，会通过 wafer-level packaging 服务费、NRE、优先排产费用传导。
- **材料厂向封装厂传导**：进入 AVL 后，材料涨价需要客户认可，但若是唯一合格配方，可获得 10%-50% 溢价。
- **TIM 厂向整机/OEM 传导**：TIM 占整机成本低但失效代价高，价格弹性小；高性能 PCM/metal TIM 可以按“降低热阻/提升功率上限”定价。
- **填料厂向 TIM 厂传导**：BN/AlN/diamond/CNT 等特种填料若供给紧张，会直接推高 TIM 毛利或压缩配方厂利润，取决于配方厂议价能力。

## 6. 竞争格局与壁垒

### 6.1 市场结构

| 细分 | 集中度判断 | 头部优势 |
|---|---|---|
| ABF build-up film | 极高，Ajinomoto 事实标准 | 客户认证、配方/IP、长期可靠性数据 |
| ABF/FC-BGA 高端载板 | 高，日台韩少数厂领先 | 资本开支、良率、客户绑定、面积/层数能力 |
| underfill/molding | 中高，日美欧头部强 | 配方 know-how、低应力/低污染、封装厂认证 |
| RDL dielectric/PSPI | 中高，日美头部强 | 光刻/固化/机械性能组合，客户认证长 |
| plating/CMP/clean | 中高，细分龙头众多 | 设备配套、缺陷控制、纯度体系 |
| TIM2/pad/gel/PCM | 中等，品牌多但高端集中 | 热阻/可靠性/可制造性数据，客户现场经验 |
| 金属 TIM/液态金属/CNT | 早期高集中 | 材料创新、应用工程、可靠性验证 |
| 导热填料 | 中高，特种 BN/AlN/CNT/diamond 集中 | 粒径/表面处理/纯度/规模 |

### 6.2 为什么这些壁垒能定价

1. **技术壁垒**：先进封装材料要同时满足热、机械、电、化学、工艺窗口，单一指标高没有意义。能在 CoWoS/HBM/Rubin package 通过认证的配方天然稀缺。
2. **规模壁垒**：客户需要千万到亿级 chip-hour 可靠性数据；新供应商即使样品性能好，也缺少量产失效数据库。
3. **渠道/客户锁定**：材料一旦进入 TSMC/ASE/Amkor/NVIDIA/AMD/Broadcom/云厂 AVL，切换会重新跑可靠性，延误芯片发布风险远大于材料降价收益。
4. **认证标准**：JEDEC、AEC、客户自定义 thermal cycling、HTHH、HAST、power cycling、liquid cooling compatibility 等测试周期长。
5. **切换成本**：underfill/TIM 变化会影响 warpage、热阻、应力、良率、返修、冷板压力；不是采购部门单独能决定。
6. **供给响应慢**：高纯化学品和特殊填料扩产往往 12-24 个月；客户为了交期会接受预付款、长协和溢价。

### 6.3 长期高 ROIC/高毛利最可能在哪一层

最高 ROIC 层：**ABF 树脂/关键膜材、RDL/PSPI 介质、临时键合/解键合材料、hybrid bonding 表面处理、高端 underfill、金属/CNT/diamond 复合 TIM、特种导热填料。**

理由：

- 资本开支低于载板厂/封装厂，但客户锁定接近设备/工艺层。
- 材料成本占整包/整机柜比例低，涨价对客户总成本影响小。
- 失败代价极高，客户会为可靠性数据付费。
- AI 芯片代际加速反而提高材料 co-development 价值。

中等 ROIC 层：**高端载板厂、先进封装 OSAT、冷板/TIM 模组集成商。**收入规模大但资本开支和折旧更重，毛利弹性取决于产能紧缺程度。

较低但确定性强层：**普通 TIM pad、通用 molding、通用电子化学品。**增长跟随行业，但定价能力容易被替代品和客户压价稀释。

## 7. 2026 关键变化：行业拐点与最可能放量方向

### 7.1 2026 最可能发生的 3 个拐点

1. **Blackwell Ultra/GB300 让液冷与 TIM2 进入默认配置**  
   2026 主力不是远期 Rubin，而是 GB300/B300 的大规模交付。其对材料的最大影响是把高性能 TIM2、冷板界面材料、gap filler、液冷兼容密封材料从“高配”变成“AI rack 默认件”。

2. **HBM4 从验证走向首批收入，材料供应商提前锁 2027 订单**  
   Rubin、MI400/MI455X、TPU8、custom ASIC 都指向 HBM4。2026 H2 即使量不大，也会决定 2027 供应商格局；HBM4 underfill、molding、thermal spreader、hybrid bonding 周边材料最值得跟踪。

3. **CoWoS 紧缺从封装产能扩散到材料和基板**  
   TSMC CoWoS 扩产和 OSAT 承接会把瓶颈转移到 ABF 载板、低翘曲材料、临时键合、RDL 介质、检测耗材。材料厂会提前获得 2027 需求可见度。

### 7.2 2026 最可能放量的子方向排序

1. ABF/FC-BGA 高端 AI 载板与 ABF film。
2. CoWoS/HBM underfill、molding、die attach、flux。
3. TIM2/PCM/gel/pad 和冷板界面材料。
4. RDL dielectric/PSPI/PBO、plating/CMP/clean。
5. 临时键合/解键合材料。
6. 金属 TIM/indium/CNT 复合 TIM 小批量高溢价。

## 8. 2027 关键变化：行业拐点与最可能放量方向

### 8.1 2027 最可能发生的 3 个拐点

1. **Rubin/HBM4 成为新主力，封装材料价值量再上台阶**  
   2027 若 Rubin NVL72、MI400/Helios、TPU8、Trainium3/4 同步放量，HBM4 package 的材料单耗和可靠性溢价会明显高于 HBM3E。

2. **CPO/1.6T 网络与 AI storage 把先进封装材料从 GPU 扩散到网络/存储芯片**  
   2027 后 AI backend Ethernet、CPO、KV cache storage 会拉动 optical adhesive、low-loss substrate、thermal pad、DPU/NIC/SSD 导热材料。

3. **开放 ASIC 与多供应商封装路线加速，材料 AVL 变成战略资产**  
   Broadcom/Marvell custom XPU、Meta MTIA、OpenAI ASIC、AWS/Google 自研 ASIC 会推动封装路径多元化。材料供应商若能同时进入 TSMC、ASE、Amkor、Intel、Samsung、云厂参考设计，将获得超额定价权。

### 8.2 2027 最可能放量的子方向排序

1. HBM4 underfill/molding/hybrid bonding 周边材料。
2. 金属 TIM、CNT/graphite/diamond 高端 TIM。
3. CPO/硅光封装胶材、低损耗基板和热材料。
4. panel-level RDL/CoPoS 材料。
5. 玻璃核心基板小批量导入。
6. CXL/AI storage/SSD controller 导热材料。

## 9. 头部公司和细分技术公司清单

### 9.1 封装服务/平台

- **TSMC**：CoWoS-S/L/R、SoIC、InFO；AI GPU/HBM 先进封装核心瓶颈。
- **ASE Technology / SPIL**：先进封装 OSAT、SiP、FC-BGA、测试服务。
- **Amkor**：先进封装、2.5D/3D、美国 Arizona 扩产，服务 HPC/AI 客户。
- **Intel Foundry**：EMIB、Foveros、玻璃基板路线，适合 chiplet/AI/HPC。
- **Samsung Foundry/Advanced Package**：I-Cube、X-Cube、HBM/logic 生态。
- **JCET、Tongfu Microelectronics、Powertech、TFME、Huatian、Chipbond**：中国/亚洲 OSAT 补充和本土替代链。

### 9.2 ABF/基板/载板材料

- **Ajinomoto**：ABF build-up film 事实标准，AI 载板最强材料壁垒之一。
- **Ibiden、Shinko Electric、Unimicron、Nan Ya PCB、Kinsus、AT&S、Samsung Electro-Mechanics、Kyocera、LG Innotek、Daeduck、Simmtech、Toppan、TTM**：高端 FC-BGA/ABF 基板。
- **Nitto Boseki、Asahi Glass/AGC、Taiwan Glass、Nan Ya、Isola、Panasonic Industry、Mitsubishi Gas Chemical、Resonac、Shengyi Technology、Elite Material**：玻纤布、低 CTE/低损耗树脂、铜箔和基板材料。

### 9.3 underfill、molding、die attach、encapsulant

- **Henkel/Loctite**：capillary underfill、non-conductive paste、die attach、TIM 和电子材料全线。
- **Namics**：高端 underfill/encapsulation，AI/HBM 封装关键供应商。
- **Resonac（Showa Denko）**：molding compound、underfill、CMP/slurry、封装材料生态。
- **Sumitomo Bakelite**：molding compound/封装树脂强势。
- **Shin-Etsu Chemical**：silicone、encapsulant、TIM、半导体材料。
- **Panasonic Industry、Nagase ChemteX、Kyocera、DELO、H.B. Fuller、MacDermid Alpha**：封装胶、die attach、molding/underfill 补充。

### 9.4 RDL/PSPI/photoresist/临时键合/湿化学品

- **DuPont / HD MicroSystems**：PI/PBO、先进封装介质、光刻介质。
- **JSR、TOK、Fujifilm、Merck/EMD Electronics、Toray、UBE、Sumitomo Chemical**：photoresist、PSPI、low-k/low-stress dielectric。
- **Brewer Science、3M、TOK、JSR、DuPont**：临时键合/解键合材料。
- **MKS/Atotech、Uyemura、Okuno、JX Advanced Metals、Tanaka、Mitsubishi Materials、Entegris、Fujimi、CMC Materials/Entegris**：plating、CMP、clean、金属材料和高纯耗材。

### 9.5 TIM/导热材料/导热填料

- **Henkel/Bergquist**：gap pad、gap filler、phase-change、液冷/电子热材料；AI data center 直接受益。
- **Indium Corporation**：indium foil、solder TIM、HSMF、heat-spring 类金属 TIM，适合高热流密度。
- **Honeywell**：PTM 系列 phase-change TIM、高性能数据中心/半导体 TIM。
- **Dow + Carbice**：Carbice carbon nanotube TIM、silicone/thermal materials。
- **DuPont/Laird、Parker Chomerics、Boyd、Fujipoly、Shin-Etsu、3M、Momentive、Wacker、Sekisui Polymatech、Denka、Saint-Gobain、t-Global**：TIM pad/gel/putty/phase-change/EMI-thermal 复合材料。
- **Denka、Tokuyama、Momentive、3M、Saint-Gobain、Resonac、SGL Carbon、NeoGraf、Kaneka、Imerys、Element Six、Coherent/II-VI**：BN、AlN、石墨、碳材料、diamond 等特种导热填料。
- **中国公司补充**：中石科技、飞荣达、天脉导热、硅宝科技、回天新材、三环集团、联瑞新材、雅克科技、华海诚科、德邦科技、方邦股份、兴森科技、深南电路、生益科技、胜宏科技、沪电股份等在导热材料、填料、封装材料、载板/PCB 国产替代链中具备跟踪价值。

## 10. 投资排序

### 10.1 未来 3-12 个月最确定

1. **ABF/高端载板与 ABF film**：收入规模最大，2026 AI 出货确定性最强。
2. **CoWoS/HBM underfill/molding/RDL materials**：和 CoWoS/HBM 瓶颈同频，客户愿意为良率和交期付溢价。
3. **TIM2/PCM/gel/pad/冷板界面材料**：GB300/液冷机柜放量即带来订单。
4. **临时键合/湿化学/CMP/清洗耗材**：随先进封装产线扩张持续消耗，利润率好。

### 10.2 未来 12-24 个月赔率最高

1. **metal TIM/indium/liquid metal/CNT TIM**：小基数、高壁垒、高热流密度驱动。
2. **HBM4/hybrid bonding 周边材料**：Rubin/MI400/TPU8 放量后弹性最大。
3. **CPO/硅光封装材料**：1.6T/3.2T 网络和 co-packaged optics 打开新收入池。
4. **玻璃基板/panel-level packaging 材料**：若获得 AI ASIC design win，估值重估会快于收入确认。
5. **国产先进封装材料替代链**：政策和供应链安全驱动，局部品类可能出现高溢价。

### 10.3 主要风险

- AI capex 因 ROI 或电力并网低于预期而递延。
- HBM/CoWoS 扩产顺利导致材料紧缺窗口缩短。
- 材料公司扩产过快，2027-2028 出现价格回落。
- TIM 新路线可靠性失败，客户回退到成熟低风险材料。
- PFAS/环保法规、出口管制和地缘冲突扰乱供应链。

## 11. 来源索引

### 项目内资料

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\conference_update\nvidia_gtc_2026_research.md`
- `D:\drive\Investment\调研\v5\conference_update\xcelerated_compute_show_2026_report.md`
- `D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`

### 外部公开来源

- SEMI Packaging Materials Outlook：[Packaging Materials Outlook](https://www.semi.org/en/products-services/market-data/packaging-materials-outlook)
- TSMC CoWoS roadmap 公开报道：[TSMC details next-gen CoWoS roadmap](https://www.tomshardware.com/tech-industry/semiconductors/tsmcs-details-next-gen-cowos-roadmap-over-14-reticle-packages-and-48x-leap-in-compute-power-expected-by-2029-massive-size-enables-24-hbm5e-stacks-and-additional-memory-bandwidth-jump)
- NVIDIA GTC 2026 press kit：[GTC 2026 News](https://nvidianews.nvidia.com/online-press-kit/gtc-2026-news)
- NVIDIA Vera Rubin platform：[Vera Rubin Opens Agentic AI Frontier](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)
- NVIDIA Vera Rubin technical blog：[Seven Chips, Five Rack-Scale Systems, One AI Supercomputer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- NVIDIA GB300 NVL72：[GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- TrendForce HBM4 / CoWoS / Blackwell 公开摘要：[TrendForce Press Center](https://www.trendforce.com/presscenter)
- Gartner semiconductor 2026：[Worldwide Semiconductor Revenue to Exceed $1.3 Trillion in 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- Deloitte AI compute and data center capex：[Why AI’s next phase will likely demand more computational power, not less](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/compute-power-ai.html)
- Henkel semiconductor and thermal materials：[Henkel Electronics](https://www.henkel-adhesives.com/)
- Indium Corporation thermal innovations for AI systems：[Productronica China 2026 thermal innovations](https://www.indium.com/es/press-releases/indium-corporation-to-spotlight-thermal-innovations-enabling-next-generation-ai-systems-at-productronica-china-2026/)
- Dow / Carbice advanced thermal interface collaboration：[Dow and Carbice](https://corporate.dow.com/)
- Intel advanced packaging / EMIB / Foveros：[Intel Foundry Advanced Packaging](https://www.intel.com/content/www/us/en/foundry/advanced-packaging.html)
- Samsung advanced packaging / I-Cube / X-Cube：[Samsung Advanced Package](https://semiconductor.samsung.com/foundry/advanced-package/)
- Amkor advanced packaging：[Amkor Advanced Package](https://amkor.com/technology/advanced-packaging/)
- ASE advanced packaging：[ASE Technology Advanced Packaging](https://ase.aseglobal.com/)
# 行业调研：【云厂自研AI ASIC】

截至日期：2026-05-08  
研究口径：本报告把“云厂自研 AI ASIC”定义为由 hyperscaler、AI 实验室或大型互联网平台主导架构和系统目标，面向自有云/模型/推荐/广告/推理工作负载深度优化，并通过 Broadcom、Marvell、TSMC、三星、SK hynix、Micron、封测和服务器供应链实现量产的专用 AI 加速器。Google TPU、AWS Trainium、Meta MTIA、Microsoft Maia、OpenAI/Broadcom accelerator、Anthropic TPU/Trainium 容量、中国云厂/互联网自研 ASIC 均纳入；NVIDIA/AMD GPU 只作为技术路线和替代基准，不计入“云厂自研 ASIC”主市场规模。

金额口径：自用 ASIC 不存在公开芯片售价，本报告采用“等效硬件/模块/机架内部转移价值”，包括加速器芯片、HBM、先进封装、载板、板卡、rack 内互连、必要的供应链溢价与部分 NRE 摊销；不包括云服务长期收入、完整数据中心土建/电力 CapEx，也尽量避免重复计算服务器 OEM 加价。未来 3 个月指 2026-05 至 2026-08；未来 1 年指 2026-05 至 2027-05；未来 2 年指 2026-05 至 2028-05。

## 0. 核心结论与数字锚

### 0.1 投资结论

云厂自研 AI ASIC 在 2026 年已经从“Google TPU 的单点领先”进入“多云厂、多 AI lab、多 GW 订单同时落地”的阶段。GPU 仍是训练和通用生态的王者，但自研 ASIC 正在吃掉高重复、高利用率、高 token 量的推理、推荐、MoE serving、合成数据、RL 后训练和内部 agent 工作负载。2026 年最可能放量的是 HBM3E + 2.5D 封装 + 自研/以太网 scale-up + 液冷的推理/训练混合 ASIC；2027 年的斜率来自 HBM4、2nm/3nm 多代 ASIC、3.5D/F2F chiplet、CPO/硅光和 OpenAI/Meta/Anthropic/Google/AWS 的多 GW 容量合约。

我的三情景判断如下，均偏乐观：

| 指标 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 云厂自研 AI ASIC 等效市场 | $70B-$110B | $120B-$180B | $190B-$280B |
| 2027 云厂自研 AI ASIC 等效市场 | $140B-$220B | $260B-$380B | $450B-$650B |
| 2028 年化运行率 | $230B-$330B | $420B-$620B | $700B-$950B |
| 自研 ASIC 占全球数据中心 AI 加速器价值 | 2026: 17%-25%；2027: 24%-33% | 2026: 25%-35%；2027: 35%-45% | 2026: 35%-45%；2027: 45%-60% |
| 最强价值捕获层 | Broadcom/Marvell custom silicon、TSMC/CoWoS、HBM、EDA/IP、SerDes/光互联 | 同左，叠加 CPO/3.5D/F2F | 同左，且云厂内部 token 毛利显著扩张 |
| 最大风险 | 软件迁移、HBM/CoWoS、客户机房上电、模型路线变化 | HBM4 良率和 2nm/3nm wafer allocation | 需求过热导致电力/内存/封装/融资全线瓶颈 |

关键判断：2026 年不是“ASIC 替代 GPU”，而是“GPU 和 ASIC 同时不够用”。ASIC 的投资价值不在芯片是否完全替代 NVIDIA，而在它把 hyperscaler 的增量 capex 从单一 GPU 供应链扩散到 Broadcom/Marvell/TSMC/HBM/封装/光互联/EDA/IP，同时让云厂把高频推理工作负载的单位 token 成本压低 20%-50%。

### 0.2 一手信息与行业报告锚点

| 来源 | 关键信息 | 投资含义 |
|---|---|---|
| [AWS Project Rainier](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster) | Rainier 已上线近 50 万颗 Trainium2；Anthropic 的 Claude 到年底预计运行在超过 100 万颗 Trainium2 上。 | Trainium2 已经从样板集群进入百万颗级别。 |
| [AWS Trainium3](https://www.aboutamazon.com/news/aws/trainium-3-ultraserver-faster-ai-training-lower-cost) | Trn3 UltraServer 采用 AWS 首颗 3nm AI 芯片，单系统 144 颗 Trainium3、362 FP8 PFLOPs，AWS 已在做 Trainium4。 | 3nm 云厂 ASIC 进入 2026 放量，2027 接 Trainium4。 |
| [Amazon 2026Q1](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-First-Quarter-Results/default.aspx) | Amazon 芯片业务年化收入超过 $20B；OpenAI 承诺从 2027 年开始消费约 2GW Trainium 容量；Anthropic 将获得最高 5GW Trainium。过去 12 个月落地 210 万+ AI 芯片，超过一半是 Trainium。 | AWS 自研芯片已是 $20B+ run-rate，并在 OpenAI/Anthropic 外部客户中变成战略算力。 |
| [Google TPU 8t/8i](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era/) | TPU 8t 面向训练，单 superpod 9600 颗、2PB 共享 HBM、121 EFLOPS；TPU 8i 面向低延迟推理，288GB HBM、384MB SRAM、19.2Tb/s ICI，性能/美元较前代提升 80%。 | Google 2026 直接把训练/推理分化成两颗 ASIC，agentic inference 成为架构起点。 |
| [Anthropic/Google Cloud TPU](https://www.anthropic.com/news/expanding-our-use-of-google-cloud-tpus-and-services) | Anthropic 计划使用最高 100 万颗 Google TPU，价值数百亿美元，2026 年上线超过 1GW 容量。 | TPU 的外部商业化和 AI lab 采用度明显提高。 |
| [Microsoft Maia 200](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/) | Maia 200 为 TSMC 3nm、140B+ 晶体管、216GB HBM3e、7TB/s、272MB SRAM、750W TDP，FP4 >10 PFLOPS，Azure 集群可扩至 6144 accelerators。 | Azure 进入推理 ASIC 实部署阶段，标准以太网 scale-up 是重点。 |
| [Meta MTIA 路线](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/) | Meta 已部署数十万颗 MTIA；两年内推进 MTIA 300/400/450/500 四代，MTIA 300 已量产，400/450/500 主要面向 GenAI inference。 | Meta 的 ASIC 从推荐推理扩到 GenAI inference，六个月迭代 cadence 是核心打法。 |
| [Broadcom/Meta](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-extended-partnership-meta-deploy-technology) | Broadcom 与 Meta 扩大战略合作，支持 MTIA 多 GW 部署；初始承诺超过 1GW，计划延伸至 2029；Broadcom 称首个 2nm AI compute accelerator。 | Broadcom 是 Meta 自研 ASIC 的实现层和网络层核心受益者。 |
| [OpenAI/Broadcom](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/) | OpenAI 与 Broadcom 合作部署 10GW OpenAI 自研 AI accelerator，2026H2 开始 rack 部署，2029 年底完成，使用 Broadcom Ethernet/PCIe/optical。 | OpenAI 自研芯片是 2027 最大预期差之一，10GW 对应数百万颗级别等效加速器。 |
| [Broadcom 2026Q1 SEC 8-K](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm) | Broadcom 2026Q1 收入 $19.3B，同比 +29%；AI 收入 $8.4B，同比 +106%；Q2 AI semiconductor 指引 $10.7B。 | Custom XPU + AI networking 已经是季度 $8B-$10B+ 收入池。 |
| [Broadcom 3.5D XDSiP](https://investors.broadcom.com/node/63946/pdf) | Broadcom 2026 年 2 月宣布开始出货首个 2nm custom compute SoC，基于 3.5D XDSiP/F2F。 | 2nm + 3.5D/F2F 已从技术宣告进入早期出货，2027 可能放量。 |
| [Marvell FY2026](https://investor.marvell.com/news-events/press-releases/detail/1011/marvell-technology-inc-reports-fourth-quarter-and-fiscal-year-2026-financial-results) | Marvell FY2026 收入 $8.195B，同比 +42%，AI 需求驱动；FY2027 各季度收入增速预计加速，design wins 创历史新高。 | Marvell 是 Broadcom 之外最重要的 custom ASIC + interconnect 供应商。 |
| [Gartner 2026 半导体](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | 2026 全球半导体收入 $1.320T，2027 $1.555T；AI 半导体占 2026 总收入约 30%；DRAM/NAND 价格 2026 年分别 +125%/+234%，到 2027 年底前无显著缓解。 | 自研 ASIC 的美元规模上沿受到内存涨价与 AI 半导体总盘子共同抬升。 |
| [TrendForce Top 8 CSP CapEx](https://www.trendforce.com/presscenter/news/20260225-12934.html) | 全球八大 CSP 2026 CapEx 超 $710B，同比 +61%；Google 2026 AI server 中 TPU 预计接近 78%，是唯一 ASIC server 多于 GPU server 的 CSP。 | Google 是 ASIC 渗透率上限样本，AWS/Meta/Microsoft 在追赶。 |
| [TrendForce Top 9 CSP CapEx](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html) | 2026 Top 9 CSP CapEx 上修至约 $830B，同比 +79%；Microsoft $190B、Google $180B-$190B、Meta $125B-$145B、AWS 预计超 $230B。 | 云厂 capex 强度足以支撑“GPU + ASIC 双线放量”。 |
| [TrendForce Blackwell/Rubin](https://www.trendforce.com/presscenter/news/20260408-13003.html) | 2026 NVIDIA 高端 GPU 出货中 Blackwell 占比从 61% 升至 71%，Rubin 因 HBM4/CX9/功耗/液冷调校等从 29% 降至 22%。 | 2026 仍是 Blackwell + ASIC 的年，Rubin 更偏 2027。 |
| [TrendForce HBM4](https://www.trendforce.com/presscenter/news/20260213-12929.html) | 三大 HBM 厂商预计 2026Q2 完成 HBM4 验证，NVIDIA Rubin 是 HBM4 主要催化。 | HBM4 是 2027 ASIC/GPU 放量共同阀门。 |

项目内底稿：`D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md` 提供了 2026-2027 出货量最大的 AI 芯片平台技术拆解，本报告在该底稿基础上只聚焦云厂自研 ASIC 及其价值链。

### 0.3 最近半年论坛、发布会与技术材料脉络

| 时间 | 论坛/材料 | 对云厂自研 ASIC 的指向 |
|---|---|---|
| 2026-01 | [Microsoft Maia 200 官方发布](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/) | Azure 把 first-party silicon 从 Maia 100 推到 3nm/HBM3e 推理平台，强调标准 Ethernet scale-up 和闭环液冷。 |
| 2026-02 | [TrendForce HBM4 验证报告](https://www.trendforce.com/presscenter/news/20260213-12929.html) | HBM4 多供应商验证成为 2027 ASIC/GPU 共用瓶颈。 |
| 2026-02 | [Broadcom 3.5D XDSiP 技术发布](https://investors.broadcom.com/node/63946/pdf) | 2nm + 3.5D/F2F chiplet 从技术路线进入早期出货，直接面向 GW 级 XPU。 |
| 2026-03 | [Meta MTIA 路线官方文章](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/) | Meta 把 MTIA 迭代节奏缩短到六个月以内，400/450/500 重点服务 GenAI inference。 |
| 2026-03 | [NVIDIA GTC 2026 Vera Rubin](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | 虽然不是云厂自研 ASIC，但 Rubin/HBM4/液冷/CPO/DSX 是 ASIC 供应链的外部技术基准和瓶颈参照。 |
| 2026-03 | [Broadcom OFC 2026 AI optical materials](https://investors.broadcom.com/node/64036/pdf) | Broadcom 把 1.6T、3.2T、CPO/OCI 生态放到 AI scale-up/scale-out 关键路径。 |
| 2026-04 | [Google Cloud Next 2026 TPU 8t/8i](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era/) | Google 直接把第八代 TPU 分成训练 8t 和推理 8i，确认 agentic AI 需要差异化 ASIC。 |
| 2026-04 | [Broadcom/Meta MTIA 多 GW 合作](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-extended-partnership-meta-deploy-technology) | Meta 自研 ASIC 从内部项目变为 >1GW 初始承诺、持续多 GW rollout。 |
| 2026-04 | [OpenAI Stargate 进展](https://openai.com/index/building-the-compute-infrastructure-for-the-intelligence-age/) | OpenAI 称已超过最初 10GW 目标，过去 90 天新增超过 3GW，验证自研 ASIC 和多云 capacity 的需求弹性。 |
| 2026-05 | [TrendForce Top 9 CSP CapEx 上修](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html) | 最新行业报告把 Top 9 CSP 2026 CapEx 上修到约 $830B，是本报告极度乐观情景的重要需求锚。 |

## 1. 2026 年 AI 计算中心建设下的机遇、挑战与技术路径

### 1.1 行业机会

1. **AI 数据中心 CapEx 足够大。** TrendForce 先在 2026-02 估算 Top 8 CSP CapEx 超 $710B，5 月进一步把 Top 9 CSP 上修到约 $830B。这个体量意味着即使 ASIC 只拿到 AI server compute 的 15%-25%，也已经是 $70B-$110B 的年化市场。
2. **推理需求从“峰值训练”转为“持续吞吐”。** 训练大模型可以容忍 GPU 溢价，但高频 inference、agent、多轮推理、广告/推荐排序和合成数据生成更看重每 token 成本、内存带宽、队列延迟和利用率。ASIC 的定制化优势在这里最强。
3. **GPU 供应不再是唯一算力来源。** AWS 过去 12 个月落地 210 万+ AI 芯片，其中超过一半为 Trainium；Anthropic 已在 AWS 与 Google 双线锁定百万级 Trainium/TPU；OpenAI 也同时签 NVIDIA、AMD、AWS Trainium、Broadcom 自研芯片。
4. **资本开支变成长期供应链合约。** OpenAI/Broadcom 10GW、Meta/Broadcom 1GW 起步、Anthropic/Google TPU 1GW+，使 ASIC 供应商能够提前锁定 HBM、先进封装、N3/N2 wafer、基板和网络芯片产能。
5. **云厂内部可直接捕获 TCO 改善。** 自研 ASIC 不一定有外部芯片毛利，但可以通过更低 token 成本、更高 fleet utilization、更低网络/内存/能耗成本转化为云服务毛利、产品体验和模型迭代速度。

### 1.2 核心挑战

1. **HBM 与先进封装是共同瓶颈。** TPU、Trainium、Maia、MTIA、OpenAI ASIC 与 GPU 共用 HBM3E/HBM4、2.5D/3.5D 封装、ABF/高层载板和高端测试产能。Gartner 已把 2026 DRAM/NAND 涨价看作全行业变量。
2. **软件成熟度决定真实出货。** Google XLA/JAX/Pathways 和 AWS Neuron 已成熟；Meta/Microsoft 的新平台还要解决 kernel 覆盖、PyTorch/Triton 适配、scheduler、模型切分、debug 和运维工具。
3. **ASIC 适合稳定工作负载，不适合模型剧烈变动。** 如果 2027 模型架构大幅偏离现有 dense/MoE/attention/KV cache 路线，一代 ASIC 的有效利用率可能快速下降。
4. **大规模集群 RAS 难度极高。** 10 万至 100 万颗加速器集群看的是 goodput，而不是单芯片峰值；故障隔离、链路绕行、checkpoint、thermal throttling、供应链批次一致性都会影响产能释放。
5. **客户机房上电速度可能慢于芯片交付。** ASIC 更便宜但仍要消耗 GW 级电力。2026 年真正的边界经常是变压器、开关柜、并网、冷却、PPA、施工人力和水资源。
6. **供应商客户集中度高。** Broadcom/Marvell 的 custom silicon 订单通常绑定少数超大客户；某一客户路线变化、内部自研替代或资本开支调整会影响季度收入。
7. **出口管制与地缘政治改变产品组合。** 中国云厂会加速国产 ASIC/GPU，但先进节点、HBM、EDA、封装设备受限，导致系统级路线更依赖超节点和国产互连。

### 1.3 2026 正在使用的技术

| 技术层 | 2026 已经在用的主路线 | 代表产品/公司 | 对投资的含义 |
|---|---|---|---|
| 计算核心 | 矩阵/张量阵列、低精度 FP8/FP4/INT8/自定义格式、MoE/attention 加速、inference-first datapath | Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA、Broadcom XPU | 算力不再只看 FLOPS，内存和通信决定 token cost。 |
| 内存 | HBM3E 主流，片上 SRAM/KV cache 加大，HBM4 进入验证/早期导入 | Maia 200 216GB HBM3e；TPU 8i 288GB HBM；GB300 288GB HBM3E | HBM 是最大成本项之一，也是最强价格传导环节。 |
| 先进封装 | CoWoS/2.5D、大尺寸 interposer、chiplet、F2F/3.5D 早期 | TSMC、Broadcom XDSiP、Marvell custom platform | 封装 capacity 与 yield 直接决定 ASIC 可交付量。 |
| 互连 | Google ICI/Virgo、AWS NeuronLink/EFA、Microsoft 标准 Ethernet scale-up、Broadcom Ethernet scale-up/scale-out | TPU 8t/8i、Trainium2/3、Maia 200、OpenAI/Broadcom、MTIA | 2026 ASIC 更倾向标准以太网或自研 fabric，2027 开始看 CPO/硅光。 |
| 主机 CPU | Axion、Graviton、EPYC、Vera/Grace、Arm/自研 CPU | Google TPU 8 使用 Axion host；AWS Trainium 配合 Graviton；Maia/MTIA 使用云厂自有 host stack | host-to-accelerator 数据搬运成为系统优化点。 |
| 软件栈 | XLA/JAX/Pathways、AWS Neuron SDK、PyTorch/Triton、vLLM/SGLang、Maia SDK、MTIA internal compiler | Google/AWS/Microsoft/Meta | 软件壁垒可能比芯片本身更强。 |
| 供电散热 | 48V rack、全液冷/闭环液冷、动态功率管理 | Maia 200 二代闭环液冷；TPU 8 支持四代液冷；GB300/Rubin 类 rack | 液冷和电力架构决定 ASIC 能否进入 GW 级。 |

### 1.4 基于 2026-2027 大出货 AI 芯片路线的新技术成熟与放量时间

| 新技术 | 2026/2027 关联芯片 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|---|
| HBM3E + 2.5D/CoWoS ASIC | TPU v7、Trainium2/3、Maia 200、MTIA 300/400、GB300 | 2026H1 已成熟，2026 全年主流放量 | 2026H2 供应改善，ASIC 与 GPU 同时扩产 | 2026H2 供应链接受高价锁单，HBM/CoWoS 溢价维持 |
| 3nm 云厂推理 ASIC | Trainium3、Maia 200、TPU 8i、后续 MTIA | 2026H2 小规模到中规模，2027 主流 | 2026H2 即多区域部署，2027H1 大客户批量 | 2026 年底成为新推理集群默认方案之一 |
| HBM4 ASIC/GPU | Rubin、MI400、TPU8 后续、OpenAI/Broadcom 下一代 | 2026Q2 验证，2027H1 批量，2027H2 放量 | 2026H2 早期批量，2027H1 主力 | 2026Q4 头部客户优先锁单，2027 形成供应竞赛 |
| 2nm + 3.5D/F2F chiplet XPU | Broadcom 2nm XDSiP、Meta/Broadcom、OpenAI/Broadcom、Marvell 2nm IP | 2026 早期出货/验证，2027H2 放量 | 2027H1 多客户量产 | 2026H2 进入 Meta/OpenAI 标杆 rack，2027 成为高端自研 ASIC 主线 |
| Ethernet scale-up | Maia 200、OpenAI/Broadcom、Meta/Broadcom、Trainium fabric | 2026 可用，2027 标准化 | 2026H2 被更多客户接受为 NVLink 外替代 | 2027 前主流 ASIC 集群都采用 Ethernet scale-up/scale-out 统一协议 |
| CPO/硅光 scale-up | Broadcom、Marvell/Celestial AI、交换芯片、未来 TPU/XPU | 2026 论坛/样机，2027 小批，2028 放量 | 2027H2 在超大集群进入批量 | 2027H1 被 OpenAI/Meta/Google 写入下一代 rack 设计 |
| 编译器/软件迁移自动化 | Maia SDK、AWS Neuron、XLA、MTIA stack、PyTorch/Triton | Google/AWS 成熟，Microsoft/Meta 2027 成熟 | 2026H2 Microsoft/Meta 推理模型迁移顺利 | 2027 ASIC 生态对主要开源模型“近似即插即用” |
| 机架级液冷与动态功率管理 | GB300、Rubin、TPU8、Maia200、Trainium3 | 2026 高端 rack 默认液冷 | 2026H2 100kW+ rack 快速复制 | 2027 200kW-500kW rack 与设施侧储能协同设计 |

### 1.5 2026 最可能的技术路径

2026 最可能出收入的路径是：**HBM3E + 3nm/4nm ASIC + 2.5D advanced package + cloud-owned scale-up fabric + Ethernet scale-out + 液冷 + 自研编译器**。具体落地为 Google TPU v7/Ironwood 与 TPU8 预导入、AWS Trainium2/3、Microsoft Maia 200、Meta MTIA 300/400、OpenAI/Broadcom 初始 rack 和 Broadcom/Marvell 的 XPU 实现层。

2026 不太可能大规模成为主流的路径是：全量 CPO、完全开放的跨云 ASIC 软件生态、无 HBM 的大规模替代、以及 2nm/F2F 在所有客户中全面铺开。这些更可能是 2027-2028 的放量主题。

## 2. 已经开始放量的关键产品：市场规模、渗透率与利润率

### 2.1 已放量产品市场规模与渗透率

注意：下表各产品存在供应链重叠，不能简单相加。例如 Google TPU 的等效价值已经包含部分 Broadcom/TSMC/HBM/封装价值；Broadcom 行是供应商收入口径，Google/AWS/Meta/Microsoft 行是客户内部转移口径。

| 已放量产品/技术 | 2026 证据 | 未来 3 个月市场规模：基准/乐观/极超 | 未来 1 年市场规模：基准/乐观/极超 | 未来 2 年累计规模：基准/乐观/极超 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| Google TPU v6/v7 Ironwood 与存量 TPU fleet | Anthropic 最高 100 万 TPU；TrendForce 估算 Google 2026 AI server 中 TPU 接近 78% | $7B-$12B / $12B-$18B / $18B-$28B | $35B-$60B / $60B-$95B / $95B-$145B | $85B-$150B / $160B-$260B / $260B-$400B | Google 内部 AI server ASIC 份额 70%-80%；全球云厂 ASIC 价值份额 25%-35% |
| AWS Trainium2/Trainium3 | Rainier 近 50 万 Trainium2；Anthropic >100 万 Trainium2；AWS 芯片业务 run-rate >$20B；Trn3 GA | $8B-$14B / $14B-$22B / $22B-$35B | $40B-$70B / $70B-$110B / $110B-$170B | $90B-$160B / $170B-$280B / $280B-$450B | AWS AI 加速器颗数中 Trainium 2026 35%-50%，2028 45%-65%；外部 AI lab 采用率上升 |
| Microsoft Maia 200 | 2026-01 发布，已部署美国 Central，US West 3 跟进；服务 OpenAI、Microsoft Foundry、Copilot | $1.5B-$3B / $3B-$5B / $5B-$8B | $10B-$22B / $22B-$40B / $40B-$70B | $30B-$70B / $70B-$130B / $130B-$220B | Azure 内部推理 attach 2026 2%-6%，2027 8%-18%，2028 极超可达 35%-40% |
| Meta MTIA 300 与现有 MTIA fleet | Meta 已部署数十万颗 MTIA，MTIA 300 已生产，400/450/500 面向 GenAI inference | $1B-$3B / $3B-$6B / $6B-$10B | $8B-$18B / $18B-$35B / $35B-$65B | $35B-$85B / $85B-$170B / $170B-$300B | Meta 推荐/广告/GenAI inference ASIC attach 2026 10%-20%，2028 30%-55%；TrendForce 仍认为 2026 Meta GPU server >80% |
| Broadcom XPU + AI networking | 2026Q1 AI 收入 $8.4B，同比 +106%；Q2 AI semiconductor 指引 $10.7B；Meta/OpenAI/Google 长约 | $10B-$13B / $13B-$17B / $17B-$22B | $50B-$80B / $80B-$120B / $120B-$170B | $130B-$250B / $250B-$420B / $420B-$650B | 全球 custom ASIC implementation 份额 55%-70%；AI networking 与 XPU 捆绑提升 ASP |
| Marvell custom silicon + interconnect | FY2026 收入 $8.195B，同比 +42%；custom AI、electro-optics、Celestial AI/XConn 强化 scale-up | $2B-$3.5B / $3.5B-$5B / $5B-$8B | $9B-$16B / $16B-$28B / $28B-$45B | $25B-$55B / $55B-$100B / $100B-$180B | custom ASIC 供应商第二梯队，2027 若 CPO/scale-up 光互连提前，份额弹性更大 |
| HBM3E/CoWoS/ABF 载板对云厂 ASIC 的 attach value | HBM3E 是 2026 ASIC 主内存；Gartner 指 memory revenue 2026 三倍增长 | $8B-$16B / $16B-$28B / $28B-$45B | $45B-$85B / $85B-$140B / $140B-$220B | $120B-$260B / $260B-$450B / $450B-$750B | 高端云厂 ASIC advanced package attach 80%-95%；HBM 成本占模块 25%-40% |
| 中国云厂/互联网自研与国产 AI ASIC | 阿里平头哥/百度昆仑芯/腾讯/字节自研或国产替代，华为昇腾和寒武纪承接出口管制缺口 | $2B-$5B / $5B-$10B / $10B-$18B | $12B-$30B / $30B-$60B / $60B-$110B | $35B-$100B / $100B-$220B / $220B-$400B | 中国新增 AI 算力中国产/自研 ASIC+GPU 2026 20%-45%，2028 极超可超过 60% |

### 2.2 已放量产品利润率预测

| 环节 | 当前利润率判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---:|---:|---:|
| Google/AWS/Microsoft/Meta 自用 ASIC 的内部经济利润 | 不体现为芯片毛利，体现为 token 成本下降、云服务毛利和模型速度 | 相比 GPU 总拥有成本低 20%-35% | 低 30%-45% | 低 40%-55%，高利用推理池可更高 |
| Broadcom XPU + AI networking | 供不应求、设计壁垒高、网络 IP 强；公司 non-GAAP 毛利很高 | 60%-68% | 65%-72% | 70%-75%，但若 rack/system 集成占比上升会稀释 |
| Marvell custom ASIC + optics | 公司 FY2027 指引 non-GAAP gross margin 约 58%-59%；custom silicon 和光互联混合 | 52%-60% | 58%-64% | 62%-68%，CPO/硅光早期可溢价 |
| TSMC 先进节点 + CoWoS | N3/N2/CoWoS 稀缺，客户愿意预付和签长期协议 | 52%-58% | 56%-62% | 60%+，但 capex 和折旧上升 |
| HBM 供应商 | HBM3E/HBM4 是全行业瓶颈，价格和 mix 上行 | 50%-65% | 60%-72% | 70%-80%，前提是良率达标且客户接受涨价 |
| ABF/高端载板 | 良率和面积驱动价格，供需紧张但议价弱于 HBM | 25%-35% | 32%-42% | 40%-50% |
| OSAT/测试 | 大客户压价，但高端测试/CoWoS 外包具备瓶颈价值 | 18%-30% | 25%-38% | 35%-45% |
| 云厂对外租赁 ASIC 算力 | 折旧/电力/利用率决定实际利润 | 云服务毛利 40%-55% | 50%-65% | 60%-75%，若自研 ASIC 成为高利用推理池 |

## 3. 在研关键产品与未来快速增长子技术

### 3.1 在研和即将放量产品

| 在研产品/技术 | 2026-05 阶段 | 未来 3 个月市场规模：基准/乐观/极超 | 未来 1 年市场规模：基准/乐观/极超 | 未来 2 年累计规模：基准/乐观/极超 | 放量判断与利润率 |
|---|---|---:|---:|---:|---|
| Google TPU 8t/8i | Cloud Next 2026 发布，预计 2026 年晚些时候 GA；8t 训练、8i 推理 | $1B-$3B / $3B-$6B / $6B-$10B | $12B-$35B / $35B-$70B / $70B-$120B | $70B-$180B / $180B-$350B / $350B-$600B | 2027H1 成 Google/Anthropic/Gemini 主力；内部 TCO 利润高，供应链毛利集中在 Broadcom/TSMC/HBM |
| AWS Trainium4 | AWS 已披露目标 FP4 6x、FP8 3x、内存带宽 4x，预计 2027 起交付 | $0-$0.5B / $0.5B-$1B / $1B-$2B | $3B-$12B / $12B-$25B / $25B-$50B | $35B-$100B / $100B-$220B / $220B-$400B | 2027H2 主力；若 OpenAI 2GW 和 Anthropic 5GW 需求前置，毛利/TCO 改善极强 |
| OpenAI/Broadcom 10GW 自研 accelerator | 2026H2 开始 rack 部署，2029 完成；OpenAI 设计，Broadcom 实现和网络 | $0.5B-$2B / $2B-$5B / $5B-$10B | $8B-$25B / $25B-$55B / $55B-$100B | $80B-$200B / $200B-$420B / $420B-$750B | 2027 最大预期差；Broadcom 设计/网络/供应链毛利 60%+，OpenAI 捕获 token 成本下降 |
| Meta MTIA 450/500 与 2nm MTIA | Broadcom/Meta 初始 >1GW，路线延伸至 2029；Meta 两年四代 | $0.5B-$2B / $2B-$5B / $5B-$10B | $10B-$30B / $30B-$70B / $70B-$120B | $80B-$200B / $200B-$360B / $360B-$600B | 2027 GenAI inference 放量；软件调校是关键，Broadcom/TSMC/HBM 利润率高 |
| Microsoft Maia 下一代/扩区域 | Maia 200 已部署，后续代际设计中 | $0.5B-$2B / $2B-$4B / $4B-$8B | $8B-$25B / $25B-$50B / $50B-$90B | $50B-$140B / $140B-$260B / $260B-$420B | 2027 若 Copilot/OpenAI/Foundry 推理迁移顺利，Azure 内部 ASIC 份额上行 |
| HBM4 ASIC 平台 | 三大厂预计 2026Q2 完成验证，Rubin/MI400/TPU8/OpenAI 后续共用 | $1B-$5B / $5B-$10B / $10B-$18B | $20B-$60B / $60B-$120B / $120B-$200B | $120B-$300B / $300B-$550B / $550B-$900B | 2027 最大供应链瓶颈；HBM4 毛利 60%-80% |
| 2nm/3.5D/F2F chiplet XPU | Broadcom 宣布 2nm 3.5D XDSiP SoC 已出货；Marvell 2nm IP/Custom SRAM | $1B-$4B / $4B-$8B / $8B-$15B | $10B-$35B / $35B-$80B / $80B-$140B | $80B-$220B / $220B-$420B / $420B-$700B | 2027H2 放量；若良率爬坡顺利，设计实现层定价权强 |
| CPO/硅光 scale-up | Broadcom OFC、Marvell/Celestial AI、1.6T/3.2T 光互联路线 | $0.5B-$2B / $2B-$4B / $4B-$8B | $5B-$15B / $15B-$35B / $35B-$60B | $50B-$140B / $140B-$300B / $300B-$520B | 2027 小批，2028 大放量；早期毛利 45%-65%，可靠性是门槛 |
| NVLink Fusion/UALink/Ethernet 开放 scale-up | GPU/ASIC 混合集群和第三方 XPU 接入需求上升 | $0.5B-$2B / $2B-$5B / $5B-$9B | $5B-$20B / $20B-$45B / $45B-$80B | $40B-$120B / $120B-$260B / $260B-$450B | 2027 互联标准争夺；SerDes/交换芯片/协议 IP 毛利高 |
| 中国云厂下一代 ASIC/PPU | 阿里/百度/腾讯/字节持续自研，国产替代受出口管制推动 | $1B-$3B / $3B-$8B / $8B-$15B | $8B-$25B / $25B-$55B / $55B-$100B | $50B-$150B / $150B-$320B / $320B-$600B | 本土需求强，但先进节点/HBM 限制明显；系统集成利润率高低分化 |

### 3.2 最值得跟踪的技术指标

1. **HBM4 验证节点：** Samsung、SK hynix、Micron 是否在 2026Q2 前后完成主流客户验证；若全部通过，2027 ASIC/GPU 上限大幅抬升。
2. **Broadcom 2026Q2/Q3 AI revenue：** Q2 指引 $10.7B 是第一道验证线；若连续上修，说明 Meta/OpenAI/Google/Anthropic 订单正在进入收入。
3. **Google TPU8 GA 时间：** 若 2026H2 TPU 8t/8i 进入客户可用，Anthropic/Google Cloud 的 2027 自研 ASIC 份额会超预期。
4. **AWS Trainium3 supply commitment：** Trainium3 若 2026 年中前后几乎满订，Trainium4 的 2027 预付款会提前。
5. **Maia 200 区域扩张速度：** US Central 到 US West 3 再到更多 region 的速度，决定 Microsoft ASIC 从展示到经济规模的周期。
6. **Meta MTIA 软件调校：** TrendForce 已提示 Meta 可能被软硬件 tuning 约束；若 MTIA 400/450 在 GenAI inference 上稳定，Meta 的 GPU 依赖会更快下降。
7. **CPO/硅光量产良率：** 2027 是否进入 hyperscaler rack 设计，而不仅停留在 OFC/论坛样机。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 层级 | 主要地区 | 主要公司 | 关键能力 |
|---|---|---|---|
| 云厂/AI lab 架构定义 | 美国、中国 | Google、AWS、Microsoft、Meta、OpenAI、Anthropic、Oracle、Apple、Alibaba、Baidu、Tencent、ByteDance | 工作负载画像、模型/编译器/数据中心协同、长期 capex |
| Custom ASIC 实现 | 美国、台湾、日本 | Broadcom、Marvell、AMD semi-custom、Alchip、GUC、Socionext、Faraday、MediaTek、Realtek/瑞昱相关设计服务、Arm ecosystem | RTL/physical design、SerDes、HBM controller、D2D、package co-design |
| Foundry | 台湾、韩国、美国、中国 | TSMC、Samsung Foundry、Intel Foundry、SMIC | N3/N2/4NP、DUV/EUV、多重曝光、良率 |
| 先进封装 | 台湾、日本、韩国、美国、马来西亚 | TSMC CoWoS/SoIC、ASE、Amkor、Samsung AVP、Intel EMIB/Foveros、JCET、TFME、Powertech | 2.5D/3D、interposer、hybrid bonding、F2F、HBM attach |
| HBM | 韩国、美国 | SK hynix、Samsung、Micron | HBM3E/HBM4 die、base die、TC bonding、KGD |
| 基板/PCB | 日本、台湾、奥地利、中国 | Ibiden、Shinko、Unimicron、Nan Ya、Kinsus、AT&S、Toppan、Shennan、SCC | 大尺寸 ABF、高层板、低损耗材料 |
| EDA/IP | 美国、英国 | Synopsys、Cadence、Siemens EDA、Arm、Rambus、Alphawave Semi、Imagination、SiFive | signoff、仿真、HBM/PCIe/SerDes/IP、安全 IP |
| 测试设备 | 日本、美国、台湾 | Advantest、Teradyne、Cohu、Chroma、FormFactor、MPI | HBM KGD、高速 SerDes、burn-in、ATE |
| 服务器/机架 | 台湾、美国、中国、墨西哥、东南亚 | Foxconn、Quanta/QCT、Wiwynn、Wistron、Inventec、Supermicro、Dell、HPE、Lenovo、Celestica、Jabil | rack integration、液冷、供电、系统 burn-in |
| 网络/光互联 | 美国、中国、台湾、东南亚 | Broadcom、Marvell、NVIDIA、Cisco、Arista、Coherent、Lumentum、Fabrinet、Innolight、新易盛、华工、光迅、Accelink、Hisense Broadband | 800G/1.6T/3.2T、DSP、激光器、CPO/硅光 |

### 4.2 供给瓶颈

| 瓶颈 | 为什么卡 | 2026 影响 | 2027 影响 |
|---|---|---|---|
| HBM3E/HBM4 | die 堆叠、KGD、base die、TC bonding、客户验证长 | HBM3E 涨价并占用普通 DRAM 产能 | HBM4 良率决定 TPU8/OpenAI/MTIA/Rubin/MI400 |
| CoWoS/2.5D/3.5D | interposer/RDL/封装设备/良率/基板面积 | 高端 ASIC wafer 出来后仍可能排队封装 | 3.5D/F2F 若放量，封装产能成为更强约束 |
| N3/N2 wafer allocation | TSMC 先进节点同时被 Apple、NVIDIA、AMD、Google、Broadcom、Marvell 抢占 | 3nm ASIC 价格和交期上行 | 2nm 首年产能更紧，客户预付款/长约重要 |
| ABF/高端载板 | AI ASIC 面积大、层数高、低损耗要求高 | 交期变长，良率影响有效出货 | 2.5D/3.5D/高带宽 SerDes 推高基板规格 |
| 高速 SerDes/PHY/IP | 224G/448G PAM、D2D、PCIe 6/7、以太网 scale-up 验证难 | Broadcom/Marvell/IP 厂定价能力强 | CPO/硅光把 IP 与封装绑定更深 |
| ATE/测试和 burn-in | HBM KGD、interposer、SerDes、整 rack burn-in 时间长 | 非显性瓶颈，影响出货节奏 | HBM4/CPO 测试复杂度上升 |
| 软件和编译器人才 | ASIC 需要内核、runtime、scheduler、debug、profiling | Meta/Microsoft 放量速度受影响 | 软件成熟者会形成客户锁定 |
| 液冷/供电/上电 | 100kW+ rack、GW 园区、并网和变压器长交期 | 芯片可交付但机房未必能上电 | 2027 多 GW 合约最大的交付风险 |
| 认证与可靠性 | 安全、热、EMI、供应链质量、RAS | 新平台导入慢 | 影响云厂是否敢把核心模型迁移 |
| 地缘政治/出口管制 | 中国先进节点和 HBM 获取受限，美国云厂供应链也要合规 | 中国需求转国产，海外供应链重排 | 主权 AI 与出口管制共同推高本土 ASIC 投资 |

### 4.3 成本结构与价格传导

高端 3nm/HBM 自研 ASIC 模块的典型成本拆分：

| 成本项 | 占模块成本比例 | 说明 |
|---|---:|---|
| 计算 die/wafer/yield | 18%-28% | N3/N2 wafer、reticle、良率、re-spin 共同决定成本；首代 ASIC 更贵。 |
| HBM stacks + base die | 25%-40% | HBM3E/HBM4 是最大单项，供不应求时占比可接近 45%。 |
| 先进封装/interposer/RDL/substrate | 15%-25% | CoWoS/3.5D/F2F、ABF 载板、underfill、hybrid bonding。 |
| 板卡/供电/VRM/局部散热 | 8%-15% | 48V power shelf、VRM、电容、电感、cold plate、传感器。 |
| 网络/光互联 attach | 8%-20% | scale-up/scale-out NIC、switch、DSP、光模块；OpenAI/Broadcom 以太网路线使此项很关键。 |
| 测试/burn-in/RMA | 5%-12% | HBM KGD、package test、SerDes、系统级 burn-in。 |
| NRE/EDA/mask/IP 摊销 | 2%-10% | 首代可高达 10%+；百万颗/GW 级部署后快速摊薄。 |

价格传导机制：

1. **HBM/CoWoS 价格上涨先传给 Broadcom/Marvell/模块供应商，再进入云厂 capex。** Meta 在 2026Q1 直接把 capex 上调部分归因于 component pricing。
2. **客户通过长期供应协议换交期。** OpenAI/Meta/Anthropic/Google/AWS 的 GW 订单会预定 wafer、HBM、基板、封装和光互联产能，使供应商毛利稳定。
3. **ASIC 对云厂的收益不是芯片售价，而是 token cost。** 如果 ASIC 让推理成本下降 30%，云厂可以选择降价抢份额，也可以维持价格扩毛利。
4. **缺货产品有溢价。** HBM、先进封装、2nm/3.5D 实现、224G/448G SerDes、高速 ATE、CPO 早期产品都具备溢价。
5. **软件成熟度影响实际成本。** ASIC 利用率低 10 个点，足以吃掉大部分硬件成本优势；因此 runtime/compiler/RAS 是隐性 BOM。

## 5. 竞争格局、壁垒与价值捕获

### 5.1 市场结构

| 层级 | 集中度 | 头部 |
|---|---|---|
| 云厂自研 ASIC 需求方 | 极高，5-8 家决定全球大部分订单 | Google、AWS、Microsoft、Meta、OpenAI、Anthropic、Oracle、中国头部云厂 |
| Custom ASIC 实现 | 高，Broadcom 第一、Marvell 第二梯队强 | Broadcom、Marvell、Alchip/GUC/Socionext/Faraday 等设计服务 |
| Foundry/先进封装 | 极高 | TSMC 是核心；Samsung/Intel/SMIC 分别在特定客户/地区补充 |
| HBM | 三寡头 | SK hynix、Samsung、Micron |
| EDA/IP | 三大 EDA + 少数 IP | Synopsys、Cadence、Siemens EDA、Arm、Rambus、Alphawave |
| 光互联/交换芯片 | 高 | Broadcom、Marvell、NVIDIA、Cisco、Arista、Coherent、Lumentum、Fabrinet、中国光模块龙头 |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 量化/事实线索 | 为什么能定价 |
|---|---|---|
| NRE 与 re-spin 成本 | 高端 3nm/2nm ASIC 从架构到量产通常需要数亿美元到十亿美元级综合投入；一次重大 re-spin 可损失 1-2 个季度 | 客户不愿轻易换供应商，供应商可通过 NRE、COT、长期协议锁定回报 |
| 最小经济规模 | 100MW-1GW 级部署才能充分摊薄 mask/NRE/software；AWS/Google/Meta/OpenAI 都在 GW 化 | 小厂难以进入，头部客户更依赖成熟实现伙伴 |
| 高速互连 IP | 224G/448G SerDes、D2D、HBM controller、Ethernet scale-up 需要多年 IP 积累 | Broadcom/Marvell 的核心壁垒不是“画 RTL”，而是网络、I/O、封装协同 |
| 软件生态 | Google XLA/JAX、AWS Neuron、Maia SDK、MTIA stack 都绑定模型迁移和调度 | 一旦模型运行稳定，切换硬件需要重新验证性能、精度、SLA |
| 供应链 assurance | Broadcom/Marvell 能替客户锁 wafer/HBM/substrate/封装 | 在短缺周期里“保证交付”本身可收费 |
| RAS/goodput | 百万颗集群的有效训练时间比单芯片峰值更重要 | 可靠性、故障绕行、telemetry、checkpoint 优化提升可用算力 |
| 数据中心协同 | 芯片、rack、液冷、供电、调度、云计费一体化 | 只有云厂和深度伙伴能做全栈优化，外部通用芯片难以完全复制 |
| 客户锁定 | OpenAI/Broadcom 10GW、Meta/Broadcom 到 2029、Anthropic TPU/Trainium 多 GW | 长约降低供应商收入波动，形成长期议价权 |

### 5.3 价值捕获排序

1. **EDA/IP/SerDes/D2D/HBM controller：** 长期 ROIC 最高，资本开支相对轻，毛利 70%-90% 可见，但增长弹性依赖 tape-out 数和 IP attach。
2. **Broadcom/Marvell custom ASIC + networking：** 单客户大、收入弹性强、技术壁垒和供应链壁垒都高。Broadcom 2026Q1 AI revenue $8.4B 已验证规模。
3. **HBM：** 2026-2027 最强瓶颈之一，毛利和价格弹性大，但周期性和扩产风险也大。
4. **TSMC/先进封装：** 价值捕获极强且份额稳定，缺点是重资产、折旧高、政治风险高。
5. **云厂自身：** 长期价值来自 token 成本下降、模型体验和云服务毛利，不是芯片毛利；短期会承受巨大 capex 和折旧。
6. **服务器 ODM/机架集成：** 收入弹性大但毛利较低，除非绑定液冷/电力/测试能力形成差异化。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点一：ASIC 从单云厂优势变成 GW 级行业共识

2026 年以前，Google TPU 是最强验证样本。2026 年开始，AWS Trainium、Microsoft Maia、Meta MTIA、OpenAI/Broadcom、Anthropic TPU/Trainium 同时进入 GW 或百万颗级别承诺。最可能放量方向是 **inference-first ASIC + cloud-owned software stack**。

投资线索：Broadcom、Marvell、TSMC、HBM、EDA/IP、high-speed SerDes、光互联。

### 拐点二：推理经济性成为采购主因

Maia 200、TPU 8i、MTIA 400/450/500 都明确面向推理、agent 和 GenAI production，而不只是大训练。2026 的最现实需求不是“训练一个更大模型”，而是“把已上线模型服务给更多用户、更多 agent、更多 token，同时把单位成本压下来”。

投资线索：HBM 容量、on-chip SRAM、KV cache、低精度 FP4/FP8、compiler/kernel、SGLang/vLLM/PyTorch/Triton 适配。

### 拐点三：内存/封装/电力从后台约束变成前台定价

Gartner 的 memory price 预测、TrendForce 的 HBM4 验证和 CSP capex 上修共同说明，2026 年客户愿意为“确定交付”付溢价。最可能放量的子方向是 **HBM3E/HBM4、CoWoS/3.5D、ABF 载板、液冷与 800G/1.6T 光互联**。

投资线索：SK hynix、Micron、Samsung、TSMC、ASE、Amkor、Ibiden、Unimicron、Advantest、Teradyne、Coherent、Lumentum、Fabrinet、中际旭创/新易盛等光模块链。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点一：HBM4 + 2nm/3nm ASIC 进入多客户批量

2027 年若 HBM4 多供应商验证顺利，TPU8、OpenAI/Broadcom、MTIA 后续、Trainium4、Maia 后续将从 2026 的早期部署进入主力出货。自研 ASIC 的全球数据中心 AI 加速器价值份额有望从 2026 的 20%-35% 上升到 35%-45%，极度乐观可达 50%+。

最可能放量子方向：HBM4、2nm/3.5D/F2F XPU、HBM controller、advanced packaging equipment、high-end substrate。

### 拐点二：以太网 scale-up 与 CPO/硅光开始改变集群架构

OpenAI/Broadcom 和 Maia 200 都强调以太网 scale-up/scale-out；Google TPU8 强调 Virgo Network、ICI 和高 goodput；Marvell/Celestial AI、Broadcom OFC 路线则把硅光/CPO 推到 scale-up。2027 年会出现“ASIC 集群不必照搬 GPU NVLink”的架构竞争。

最可能放量子方向：1.6T/3.2T 光互联、CPO、D2D、SerDes、Ethernet switch ASIC、optical circuit switching。

### 拐点三：AI lab 与云厂的供应链关系重排

OpenAI 同时使用 Microsoft、Oracle、AWS、Google Cloud、NVIDIA、AMD、AWS Trainium、Cerebras 和 Broadcom 自研芯片；Anthropic 同时锁 AWS Trainium、Google TPU 和 NVIDIA/Microsoft Azure。2027 年最可能出现的是“AI lab 多供应商 portfolio”，而不是单一云厂或单一芯片锁死。

最可能放量子方向：可跨云调度的软件层、模型编译/量化/serving 工具、capacity marketplace、云厂自研 ASIC 对外租赁。

## 8. 头部公司清单：按细分领域尽量覆盖

### 8.1 云厂、AI lab 与平台方

| 领域 | 头部公司 |
|---|---|
| 美国 hyperscaler | Google/Alphabet、Amazon/AWS、Microsoft Azure、Meta、Oracle OCI、Apple、CoreWeave、Lambda、Nebius、Nscale |
| AI lab/模型公司 | OpenAI、Anthropic、xAI、Mistral AI、Cohere、Perplexity、Cursor/Anysphere、Databricks/Mosaic、Character.AI |
| 中国云厂/互联网 | Alibaba Cloud/平头哥、Baidu/昆仑芯、Tencent、ByteDance、Huawei Cloud/昇腾、China Mobile/Telecom/Unicom 云、京东云、快手、美团 |
| 主权 AI/政府云 | Oracle、Microsoft、AWS、Google、NVIDIA sovereign AI partners、G42、Singtel/Bridge Alliance、各国国家云项目 |

### 8.2 自研 ASIC 与 custom silicon 实现

| 细分 | 公司 |
|---|---|
| Custom XPU/ASIC 龙头 | Broadcom、Marvell |
| 半定制/加速器平台 | AMD semi-custom、NVIDIA NVLink Fusion ecosystem、Intel Foundry/IFS custom、MediaTek、Socionext |
| ASIC 设计服务 | Alchip、GUC、Faraday、Socionext、eInfochips、Siemens EDA services、Wipro/Capgemini engineering、Tata Elxsi、Sondrel |
| IP/CPU/D2D/SerDes | Arm、Rambus、Alphawave Semi、Synopsys IP、Cadence IP、SiFive、Andes、Imagination、Arteris、M31、Credo |
| AI 芯片初创/专用推理 | Cerebras、Groq、SambaNova、Tenstorrent、d-Matrix、Etched、MatX、Positron AI、Rain AI、Rebellions、FuriosaAI、Kneron、Untether AI |
| 中国 AI ASIC/GPU | Huawei HiSilicon/Ascend、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Enflame、Iluvatar CoreX、MetaX、Moore Threads、Hygon、壁仞、燧原、沐曦、摩尔线程、天数智芯 |

### 8.3 制造、封装、内存与设备

| 细分 | 公司 |
|---|---|
| Foundry | TSMC、Samsung Foundry、Intel Foundry、SMIC、UMC、GlobalFoundries |
| 先进封装 | TSMC CoWoS/SoIC、ASE、Amkor、Samsung AVP、Intel EMIB/Foveros、JCET、TFME、Powertech、SPIL |
| HBM/DRAM | SK hynix、Samsung、Micron、CXMT（中国替代但高端 HBM 仍需爬坡） |
| 载板/PCB | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、AT&S、Toppan、Shennan Circuits、SCC、Tripod、Compeq |
| 设备 | ASML、Applied Materials、Lam Research、KLA、Tokyo Electron、ASM International、BE Semiconductor、Kulicke & Soffa、DISCO、SCREEN |
| 测试 | Advantest、Teradyne、Cohu、FormFactor、MPI、Chroma、Hon Precision、京元电子 |

### 8.4 网络、光互联、服务器和电力冷却

| 细分 | 公司 |
|---|---|
| 交换芯片/网络 ASIC | Broadcom、Marvell、NVIDIA、Cisco、Intel、Credo、Astera Labs |
| 光模块/硅光/激光器 | Coherent、Lumentum、Fabrinet、Innolight、中际旭创、新易盛、光迅科技、华工科技、Accelink、Hisense Broadband、Eoptolink、Applied Optoelectronics、MACOM |
| 服务器/ODM | Foxconn、Quanta/QCT、Wiwynn、Wistron、Inventec、Supermicro、Dell、HPE、Lenovo、Celestica、Jabil、Flex |
| 液冷/热管理 | Vertiv、Schneider Electric、Eaton、CoolIT、Aavid/Boyd、Asetek、Delta、nVent、Modine、Motivair、Submer |
| 数据中心电力 | Eaton、Schneider Electric、ABB、Siemens、GE Vernova、Vertiv、Powell、Hubbell、nVent、Delta、Legrand |

### 8.5 软件栈和模型 serving

| 细分 | 公司/项目 |
|---|---|
| 云厂自研编译器 | Google XLA/JAX/Pathways/MaxText、AWS Neuron、Microsoft Maia SDK/Triton、Meta MTIA stack/PyTorch |
| 推理/serving | vLLM、SGLang、TensorRT-LLM、Triton Inference Server、ONNX Runtime、Ray Serve、KServe |
| 训练框架 | PyTorch、JAX、TensorFlow、DeepSpeed、Megatron-LM、FSDP、Accelerate |
| 调度和运维 | Kubernetes、Slurm、Ray、OpenAI internal scheduler、Google Borg、AWS internal control plane、Azure control plane |

## 9. 投资观察清单

1. **Broadcom：** 2026Q2 AI semiconductor 是否超过 $10.7B 指引，Q3 是否继续上修；Meta/OpenAI/Google/Anthropic 是否带来 2027 $100B+ chip revenue 可信度。
2. **Marvell：** FY2027 data center/custom silicon 增速、Celestial AI/XConn 整合、1.6T/CPO 和 custom XPU design wins。
3. **TSMC：** N3/N2 wafer allocation、CoWoS 月产能、SoIC/F2F/CoWoS-L 扩产、客户预付款。
4. **HBM：** SK hynix/Samsung/Micron HBM4 验证和量产进度，HBM3E/HBM4 ASP，base die 良率。
5. **Google：** TPU8 GA 时间、Anthropic TPU 容量上线进度、Google Cloud AI backlog 和 capex 指引。
6. **AWS：** Trainium3 供给是否在 2026 年中满订，Trainium4 2027 交付时间，OpenAI 2GW 与 Anthropic 5GW 进度。
7. **Microsoft：** Maia 200 区域扩张、Copilot/OpenAI workloads 迁移比例、Azure AI capacity 约束是否缓解。
8. **Meta：** MTIA 400/450/500 在 GenAI inference 的真实利用率，Broadcom 1GW 首期是否按期。
9. **OpenAI：** Broadcom 自研芯片 2026H2 rack 是否如期开启、Stargate 和多云 capacity 是否继续上修。
10. **中国云厂：** 国产 ASIC/GPU 集群规模、SMIC 先进节点良率、国产 HBM/封装/光互联替代进度。

## 10. 最后判断

云厂自研 AI ASIC 的本质不是“芯片公司卖芯片”，而是“超大客户把模型、软件、网络、内存、机架、数据中心和电力统一优化”。在这种结构里，最确定的投资价值通常不在单颗 ASIC 本身，而在实现层和瓶颈层：Broadcom/Marvell 的 custom silicon 与 AI networking，TSMC 的先进节点与 CoWoS，SK hynix/Micron/Samsung 的 HBM，Synopsys/Cadence/Arm/Rambus/Alphawave 的 EDA/IP，以及基板、测试、光互联、液冷和电力链。

2026 年最现实的主线是 Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA 和 OpenAI/Broadcom 的早期 rack 同时扩张；2027 年最大的预期差是 OpenAI 10GW、Meta 多 GW、Anthropic TPU/Trainium 多 GW、TPU8/Trainium4/HBM4/2nm/3.5D/F2F 同时进入批量。如果 AI 数据中心建设继续以当前乐观强度推进，云厂自研 AI ASIC 有机会在 2027 年成为仅次于 NVIDIA GPU 的第二大 AI compute 产业链，并把供应链高毛利从 GPU 一条线扩散到 custom ASIC、HBM、先进封装和以太网/光互联生态。
