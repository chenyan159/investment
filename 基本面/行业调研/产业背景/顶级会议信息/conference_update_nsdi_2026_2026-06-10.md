# NSDI 2026会议追踪：核心变化、产品爆发和市场预期差

| 项目 | 结论 |
|---|---|
| 会议对象 | 23rd USENIX Symposium on Networked Systems Design and Implementation, NSDI '26 |
| 会议日期 | 2026-05-04 至 2026-05-06 |
| 会议地点 | Hyatt Regency Lake Washington, Renton, WA, USA |
| 材料检索截止日期 | 2026-06-10 21:00 PDT，本地工作区日期；对应 UTC 日期为 2026-06-11 |
| 报告完成日期 | 2026-06-10 PDT；对应 UTC 日期为 2026-06-11 |
| 资料边界 | 本报告独立追踪公开资料，不读取、引用或继承项目内旧报告、索引、缓存和中间结论 |
| 会议属性判断 | NSDI 不是 OFC 这类产品展，公开增量主要来自论文、keynote、slides、视频、赞助活动和公司研究博客；投资含义来自工程成熟度和 hyperscaler 生产系统披露，而不是展台新品发布 |

## 结论摘要

1. **最大变化：AI 网络从“算力配套”变成“系统架构主线”。** Amin Vahdat 的 keynote 把网络系统放到 TPU on-chip networks、rack-scale serving、ML training supercomputers 和 gigawatt-scale regional computing hubs 的连续谱里；会议论文也把 AI cluster network design、LLM serving、MoE collective communication、SmartNIC/DPU、CXL memory、telemetry 和 CDN/edge QoE 放在同一个系统优化问题下。

2. **最有投资价值的主题不是单一协议，而是“异构 AI 基础设施的控制面、仿真、调度和可观测性”。** Meta 的 Matryoshka 已运行 6 年、设计近 900 个 DCN、覆盖 18 类网络并支持 100K-GPU supercluster；Meta/NVIDIA 的 Arcadia 做 cluster-level AI network simulation；Alibaba 的 EROICA 在约 100,000 GPU 集群生产运行 1.5 年并达到 97.5% 诊断成功率。这些不是概念论文，而是大客户内部已经付费验证的痛点。

3. **最快放量的硬件链条仍是 800G/1.6T Ethernet switching、optics、NIC/DPU 和相关软件栈。** IDC 口径显示，2025 全年 data-center Ethernet switch revenue 为 325 亿美元，同比增长 53.5%；800G 占 2025 全年 revenue 的 16.4%，4Q25 已占 25.8%。Dell'Oro 认为 2025 是 Ethernet 在 AI back-end network 超过 InfiniBand 的拐点，2026 仍有强双位数增长。

4. **SmartNIC/DPU/programmable switch 的确定性被低估。** Microsoft Azure 的 SONiC DASH SmartSwitch 已达 1.53 Tbps throughput、19.2M CPS、256M concurrent connections，并相对上一代提升约 1.8 倍 power efficiency、2.7 倍 space efficiency；Alibaba Bifrost 支持每 SmartNIC O(100k) 连接，Redis tail latency 最高降 307 倍、Nginx 降 66 倍；ByteDance Net-P4ct 已在生产 WAN 运行近 1 年。这说明 DPU/SmartNIC 从“可选卸载卡”转向“云网络服务承载层”。

5. **LLM serving 的机会在 token 成本下降和 GPU 利用率，而不是又一个模型框架。** FastServe 相比 vLLM throughput 最高提升 6.1 倍；DroidSpeak 在同架构 fine-tuned model 之间复用 KV cache，throughput 最高 4 倍、prefill 约 3.1 倍；Agentix 对 agentic workloads 在相同 latency 下 throughput 提升 4-15 倍；SwiftEP 面向 MoE prefill 的 all-to-all 通信提升 algorithm bandwidth 119.7%、降低 SM occupancy 66.7%。这些会把利润池从单纯 GPU 采购转到调度、内存、NVLink/RDMA、cache 和 serving engine。

6. **CXL 和内存解耦还不是 2026 年主链条爆发，但已进入“可验证瓶颈”阶段。** Octopus 用 sparse CXL topology 避免高端 CXL switch 依赖；PD3 用 DPU 做 disaggregated memory prefetch；OneSidedMW 用 RNIC offloading 和 memory windows 做细粒度远程内存管理，disaggregated key-value store 最高 10.6 倍性能改善。市场数字上，公开 CXL component 口径 2026E 仍只有约 8.91 亿美元，和“2028 年 150 亿美元以上”这类 broader CXL revenue 口径差异很大，不能把远期 TAM 直接贴现到 2026。

7. **视频、CDN、5G/edge 是次主线但有利润率含义。** ByteDance Medley 在商业 live streaming CDN 中减少 76.83% midgress cost，峰值处理 0.85 million concurrent viewing requests per minute；Amazon Prime Video 的 AZEEM 在部分生产流量中平均 QoE 改善 2.7%、P90 改善 10.6%；SMEC 在 5G MEC testbed 中 SLO satisfaction 90-96% 对比既有方法低于 6%。这类系统的投资弹性更可能体现在云/边缘平台毛利率、CDN 成本结构和 SmartNIC 渗透，而不是单个消费 app 收入。

8. **最大反共识：NSDI 2026 强化的是“生产系统成熟度”，不是“某个新协议马上替代一切”。** HeteCCL、FAST、ForestColl、Di-PS、BURST 等论文都在解决异构 GPU、异构 fabric、cross-cluster、non-RNIC/RNIC 互通和 MoE traffic skew。这意味着 2026-2027 的真实需求不是单一赢家通吃，而是 hyperscaler 在 Ethernet、InfiniBand、NVLink、UALink/CXL、custom silicon 和 open software 之间做组合优化。

9. **最大风险：很多论文是 hyperscaler 内部降本系统，未必外溢为第三方收入。** Meta、Google、Microsoft、Alibaba、ByteDance、Tencent 的生产论文证明需求存在，但也说明头部客户会自研控制面和调度系统。外部上市公司更容易捕获的是高端 switch ASIC、NIC/DPU、optics、CXL/PCIe retimer、ODM 制造、测试认证和少数平台型云服务，而不是泛化的“AI 软件”叙事。

## 会议重点和方向变化

### 会议材料状态

| 材料类型 | 截止 2026-06-10 PDT 的状态 | 投资研究含义 |
|---|---|---|
| 官网与日程 | USENIX 官网确认 2026-05-04 至 2026-05-06，Renton；3 个 parallel technical tracks；2026-05-04 09:00 keynote；Sponsor Events 在 2026-05-04 和 2026-05-05 晚间 | 会议已经结束，可做会后追踪，不应写成会前预览 |
| Proceedings / slides | 官网说明 full proceedings 和 presentation slides 免费公开；Full Proceedings PDF 约 351 MB | 论文和 slide 是主要一手证据 |
| 视频 | 官网说明视频在会后数周内发布；公开搜索已出现 keynote、ServeGen、Bifrost、EROICA 等 NSDI '26 视频 | 视频可作为会后更新源，但本报告不把视频口播作为未核实核心证据 |
| Keynote | Amin Vahdat, Google, 题为 The Physics of Thought and the Architecture of Intelligence | 官方把 AI infrastructure 的关键瓶颈明确指向 networked systems |
| Sponsor / exhibitor | Platinum: Amazon；Gold: Baseten、Futurewei、Jane Street、Meta；Silver: Google、Netpreme；Bronze: Akamai、Microsoft；Open Access: KAUST。Tabletop 展示时间覆盖 2026-05-04 至 2026-05-06 | 赞助名单显示 hyperscaler、AI serving 平台、CDN、研究组织都把 NSDI 作为招募/影响工程生态的场域 |
| 公司材料 | Microsoft Research 2026-05-05 博客列出 11 篇 Microsoft 作者或合作论文；Meta、Alibaba 等有论文和社交/个人主页线索 | 公司一手材料偏研究影响力，不是产品发布；需要和论文 maturity 绑定 |
| 非官方材料 | LinkedIn 公开分享显示 659 submissions、150 accepted papers、约 23% acceptance；Meta 员工分享称 Meta 6 篇论文、3 篇 experience papers | 可作为会议热度线索，不能单独支撑商业结论 |

### 核心主题表

| 主题 | 对应公司 / 论文 / 技术 | 关键参数和证据 | 变化性质 | 投资读法 |
|---|---|---|---|---|
| AI cluster network design 进入生产级控制面 | Google keynote；Meta Matryoshka；Meta/NVIDIA Arcadia；Meta/NVIDIA/Uber Phantora | Matryoshka 运行 6 年，设计近 900 DCNs、18 types、100K-GPU supercluster；Arcadia 为 AI networks 做 cluster-level high-fidelity simulation；Phantora 用单 GPU 做 ML training framework 复用式仿真 | 真实变化，生产验证强 | 控制面、仿真、validation 和 network digital twin 变成 GPU capex 的前置工具；对 Arista/Broadcom/NVIDIA/Meta 自研链条和云内部平台最重要 |
| Ethernet/RDMA/collectives 不是协议口水战，而是异构调度问题 | BURST、HeteCCL、FAST、ForestColl、Di-PS、SwiftEP | BURST 在 400G NIC 达 98.7% line-rate，LLM inference latency 降至 TCP 的 25.2%；HeteCCL 在 32 H20/V100 测试床较 NCCL/TACCL/TE-CCL 带宽最高 2.8/4.4/2.6 倍，训练效率 23%-37%；FAST 覆盖 NVIDIA H200 和 AMD MI300X；SwiftEP 服务能力提升 21.2% | 真实变化，放量依赖客户集群更新 | 2026-2027 AI 网络增量不只来自交换机，还来自 NIC、collective libraries、software RDMA、MoE 通信和跨集群训练 |
| LLM serving 从 GPU 堆量进入 token economics | FastServe、DroidSpeak、Agentix、JITServe、FlexLLM、HydraServe、ServeGen | FastServe 相比 vLLM throughput 最高 6.1 倍；DroidSpeak throughput 最高 4 倍、prefill 约 3.1 倍；Agentix 4-15 倍；HydraServe cold start latency 1.7-4.7 倍改善；ServeGen 来自全球云 LLM serving workload | 真实变化，部分开源/研究，商业化路径取决于云平台 | 推动 inference platform、KV cache、memory bandwidth、RDMA/NVLink、serverless LLM、agent orchestration 的支出；对 Baseten、云厂商和 GPU/网络硬件有间接价值 |
| SmartNIC/DPU/programmable switch 成为云网络服务承载层 | Microsoft SONiC DASH SmartSwitch；Alibaba Bifrost/ZOC；ByteDance Net-P4ct；HybridMesh；eXpressSFU；PD3 | DASH: 1.53 Tbps、19.2M CPS、256M connections；Bifrost: Redis tail latency 最高 307 倍改善、Nginx 66 倍、每 SmartNIC O(100k) connections；Net-P4ct 生产 WAN 近 1 年；eXpressSFU 3 倍用户、power 降 60% | 真实变化，生产和 prototype 混合 | 价值捕获顺序：DPU/IPU silicon、SmartNIC/NIC、switch ASIC、SONiC/P4、云网络服务。单纯服务器 OEM 只吃低利润组装 |
| CXL / disaggregated memory 进入结构化验证 | Octopus、PD3、OneSidedMW、DistVS、FalconFS、ZipLLM | OneSidedMW KV store 最高 10.6 倍改善，swap-based 32.3% 改善；DistVS 查询吞吐通常提升 40%+；FalconFS 在华为 autonomous driving 10,000 NPUs 生产运行一年，训练吞吐最高 12.81 倍 | 中期变化，2026 仍早期 | CXL component 2026E 小于 10 亿美元口径，但能拉动 DRAM、CXL controller、PCIe/CXL retimer、server platform qualification |
| AI cluster 可观测性和 failure diagnosis 是刚需 | EROICA、Checkmate、PrvTel、REAL、Harp、CrossCheck、Gemini/Geminet | EROICA 100,000 GPU 级生产服务运行 1.5 年，97.5% success；Checkmate checkpoint 频率 5-34.5 倍、重复工作减少 80%-97.1%；PrvTel ownership cost 最高降 50 倍；REAL 1,000-node emulation 快 4 倍、4 台 commodity servers 扩到 4,500 nodes | 真实变化，客户痛点强 | GPU 规模扩大后，故障定位、checkpoint、simulation 和 telemetry 的 ROI 与 GPU idle cost 绑定；第三方软件若无法接入硬件 telemetry，弹性有限 |
| CDN / edge / real-time media 的系统降本可见 | Medley、AZEEM、Morphe、SMEC、Law、QCON、Syntra | Medley midgress cost 降 76.83%，峰值 0.85 million concurrent viewing requests/min；AZEEM 生产流量 QoE 平均 +2.7%、P90 +10.6%；Morphe 较 H.265 节省 62.5% bandwidth；SMEC SLO 90%-96% vs <6% | 部分生产验证 | 对 Akamai/Cloudflare/Fastly/ByteDance/Tencent 的含义是成本曲线和边缘算力效率，不是流量总量本身 |
| Optical WAN 和 high-speed optics 从容量投资转向可调优系统 | Learning to Tune Optical WANs、OpenOptics、Net-P4ct、DDoS 100 Tbps | Optical WAN field deployment 单 wavelength SNR 提升 2 dB；OpenOptics 提供开放 data center optical network research implementation；DDoS detection scale 达 100 Tbps | 真实需求但产品化链条长 | 800G/1.6T optics 仍是硬件高弹性环节；软件调优能提高可用 capacity 和良率，但多数收益内部化 |

## 产品和技术路线三情景预测

### 口径说明

- “当前市场规模”不是 NSDI 会议披露，而是用 2025-2026 公开市场资料和可复核估算给出的美元口径。
- “未来一年”按 2026H2 至 2027H1 的可投资窗口理解，不等同于完整自然年 2027。
- 情景预测是研究假设，不是公司指引；每一行都列出反证条件。

| 方向 | 当前成熟度，2026-06-10 | 当前市场规模和口径 | 未来一年基准 | 未来一年乐观 | 未来一年超预期乐观 | 利润率和价值捕获 |
|---|---|---:|---:|---:|---:|---|
| AI data-center Ethernet / AI back-end networking | 生产放量。IDC 2025 data-center Ethernet switch revenue 325 亿美元；Dell'Oro 认为 2025 Ethernet 在 AI back-end 超越 InfiniBand | 2025 data-center Ethernet switch: 325 亿美元；650 Group broader data-center networking 2026E >500 亿美元 | 2026H2-2027H1 600-700 亿美元 broader networking spend，增速 20%-30%；800G 继续提升，1.6T 初期导入 | 700-850 亿美元，增速 35%-50%；hyperscaler capex 不降，800G supply 改善 | 900 亿美元以上，增速 60%+；1.6T/scale-up Ethernet 提前、CPO 订单前移 | 高价值：switch ASIC、high-radix platform、NOS/SONiC、telemetry。系统厂毛利中高，ODM 经营利润率低，ASIC/IP 和软件控制面最高 |
| AI optics，800G/1.6T，LPO/LRO/CPO | 800G 大规模交付，1.6T 前期；NSDI 间接证据是 AI fabric 和 optical WAN 调优需求 | AI cluster optics 2026E 约 100 亿美元，置信度中；400G+ datacom modules 2029 TAM 接近 300 亿美元，公开二手口径 | 未来一年 120-135 亿美元，增速 20%-35%；800G 占主导，1.6T 小批量 | 140-160 亿美元；800G 供给仍紧，1.6T 认证提前 | 170 亿美元以上；CPO/LPO 设计 win 前移，hyperscaler 多年订单锁定 | 光模块毛利率分化很大，头部 800G/1.6T 与硅光/EML/VCSEL/测试能力更值钱；低端模块价格快速下滑 |
| SmartNIC / DPU / IPU / programmable switch offload | Azure DASH、Alibaba Bifrost、ByteDance Net-P4ct 已生产；eXpressSFU/HybridMesh/PD3 有原型验证 | Dell'Oro 口径 Ethernet Adapter + Smart NIC 2028E >160 亿美元，27% CAGR；反推 2026E 约 90-110 亿美元。SmartNIC/DPU 纯子集约 10-50 亿美元，定义差异大 | 未来一年 110-130 亿美元 total adapter+SmartNIC；DPU 子集高双位数增长 | 140-160 亿美元；网络服务 offload、storage/memory offload 加速 | 170 亿美元以上；cloud 网络服务从 CPU/host agent 大规模迁移到 DPU/SmartSwitch | 高价值在 DPU/IPU ASIC、firmware、P4/SONiC、云网络服务；网卡硬件和 ODM 利润低于 silicon/software |
| LLM inference serving software / agent serving / KV cache systems | 研究和早期平台化。FastServe/DroidSpeak/Agentix/ServeGen 等证明 4-15 倍量级效率空间，但多为开源或内部系统 | Broad AI inference 2026E 约 1,178 亿美元；narrow cross-platform LLM inference engine 2025 约 38 亿美元，2026E 约 48-55 亿美元 | Narrow engine 未来一年 60-70 亿美元；云平台主要用作毛利率改善 | 80-100 亿美元；enterprise agent workloads 大规模上线 | 120 亿美元以上；agent program scheduling 成为标准云服务计费项 | 软件毛利率理论高，但 GPU compute pass-through 拉低综合毛利。最赚钱的是云平台、模型服务商和可锁定 workload 的 inference platform |
| CXL / disaggregated memory / remote memory systems | 论文级验证多，生产放量少。Octopus/PD3/OneSidedMW 说明瓶颈真实 | GMI CXL component 2025: 7.101 亿美元，2026E: 8.911 亿美元；Yole broader CXL revenue 2028E >150 亿美元，口径更宽 | 未来一年 10-12 亿美元 component revenue；主要是 server qualification 和 pilots | 13-18 亿美元；CXL 3.0 server refresh 和 memory expansion 先行 | 20 亿美元以上；hyperscaler 采购 CXL memory pool，DRAM 价格高企强化 ROI | 长期利润池：DRAM、CXL controller、PCIe/CXL retimer、switch、server platform validation；短期更多是 design-in，不是利润兑现 |
| AI storage / vector search / RAG data path | DistVS、FalconFS、ZipLLM、Cortex 等证明 RAG 和 deep learning pipeline 数据路径瓶颈 | 没有统一可靠公开 TAM；用 vector DB/RAG infra + AI storage 粗估 2026E 50-100 亿美元，置信度低 | 未来一年 60-120 亿美元；企业 RAG 和 cloud object/block/file 增长 | 120-180 亿美元；RAG 生产化带动高性能存储和缓存 | 200 亿美元以上；agentic workflows 大量查询私有数据 | 价值在 cloud storage、metadata engine、NVMe-oF/RDMA、cache layer；纯数据库软件需证明替代成本 |
| CDN / edge real-time video optimization | ByteDance Medley、Prime Video AZEEM 生产验证；Morphe/SMEC/Law 原型 | CDN services 2026E 粗估 250-350 亿美元，置信度中低；会议证据主要是成本下降，不是 TAM 扩张 | 未来一年 270-380 亿美元，增速 8%-15%；利润改善来自 midgress/edge compute | 400 亿美元左右；AI video、live commerce、cloud gaming 提升 traffic | 450 亿美元以上；generative video streaming 和 edge AI 推高单用户算力 | CDN 毛利受 transit、peering、server depreciation 影响；SmartNIC/offload 和 routing 优化能改善单位成本，但客户议价强 |
| Network observability / testing / reliability for AI clusters | EROICA、PrvTel、REAL、Checkmate 等接近生产刚需 | 传统 observability/security/network management TAM 很大但口径混杂；AI cluster-specific 可观测性 2026E 粗估 10-30 亿美元，置信度低 | 未来一年 15-40 亿美元，hyperscaler 内部化为主 | 40-60 亿美元，neocloud/enterprise 采购外部平台 | 70 亿美元以上，GPU idle-cost insurance 成为独立预算项 | 软件/IP 毛利高，但第三方必须接入 GPU/NIC/switch telemetry；无硬件权限的软件弹性低 |

### 放量节点

| 时间窗口 | 需要跟踪的节点 | 判断变化 |
|---|---|---|
| 未来 3 个月，至 2026-09 | NSDI 视频和 slides 是否完整；2Q26 earnings 中 hyperscaler capex、Arista/NVIDIA/Broadcom/Celestica/Coherent/Lumentum/Innolight/AAOI 对 800G、1.6T、AI networking backlog 的说法；Dell'Oro/IDC 2Q26 tracker | 验证 2026H2 需求是否仍 supply-constrained。若 800G 价格/交期快速松动，光模块和交换机链条估值要下修 |
| 未来 1 年，至 2027-06 | 1.6T optics qualification；scale-up Ethernet/UALink/NVLink 竞争；DPU/IPU 是否从 Azure/Alibaba 扩散到更多 clouds；CXL memory expansion 是否进入新服务器批量配置；LLM serving 系统是否被商业云产品化 | 判断从“论文和内部系统”转向“外部供应商收入” |
| 未来 2 年，至 2028-06 | CPO/CXL switch/scale-up Ethernet 真正 ramp；agent workloads 是否带来持续 token spend；AI data center capex 是否进入 ROI 下修或继续上调 | 决定长期利润池是在硬件瓶颈、云平台内部效率，还是第三方软件 |

## 市场规模和利润池

### 1. AI networking：交换机、ASIC、optics、NIC 是 2026-2027 最确定主线

**事实：** IDC 2026-03-18 资料显示，2025 全年 Ethernet switch revenue 551 亿美元，同比增长 31.5%；其中 data-center segment 325 亿美元，同比增长 53.5%。4Q25 data-center Ethernet switch revenue 为 99 亿美元，同比增长 63.0%。800G 端口在 4Q25 占 revenue 的 25.8%，全年占 16.4%。NVIDIA 4Q25 Ethernet switch revenue 为 15 亿美元，同比增长 192.6%，占 data-center segment 15.2%；Arista 4Q25 Ethernet switch revenue 20 亿美元，data-center segment 占其 Ethernet switch revenue 的 92.6%。

**NSDI 证据：** BURST、HeteCCL、FAST、ForestColl、SwiftEP、Di-PS、Matryoshka、Arcadia 均把 AI 网络瓶颈指向 high-speed Ethernet/RDMA/NVLink/MoE/cross-cluster 的组合优化，而不是单一硬件升级。

**估算：** 如果 2025 data-center Ethernet switch 为 325 亿美元，2026 在 hyperscaler capex 上行和 800G 放量下实现 25%-40% 增长，则 2026 data-center Ethernet switch 可到 406-455 亿美元；若 broader data-center networking 2026 already above 500 亿美元，2027 上半年 run-rate 可能接近 650-800 亿美元。反证是 hyperscaler capex guide 下修、800G 库存积压、1.6T qualification 延迟。

**利润池：** 长期更赚钱的是 merchant switch ASIC、SerDes、NOS/SONiC、network telemetry、optics 核心器件和平台级系统软件；白牌/ODM 和通用服务器组装的利润率最低。Arista、NVIDIA、Broadcom、Cisco、HPE/Juniper、Celestica、Accton、Coherent、Lumentum、Innolight、Eoptolink、Fabrinet、AAOI 等需要按客户集中度和 800G/1.6T 合格供应商身份区分。

### 2. LLM serving：市场大，但可投资收入不等于节省下来的 GPU 成本

**事实：** 公开市场口径差异巨大。Fortune Business Insights 口径把 broad AI inference market 估为 2025 年 1,037.3 亿美元、2026 年 1,178.0 亿美元；DataIntelo narrow cross-platform LLM inference engine market 口径为 2025 年 38 亿美元，2034 年 286 亿美元。两者一个包括广义硬件和应用推理，一个更偏 engine/software/services。

**NSDI 证据：** FastServe 最高 6.1 倍 throughput；DroidSpeak 4 倍 throughput 和 3.1 倍 TTFT/prefill；Agentix 4-15 倍；HydraServe cold start 1.7-4.7 倍改善；SwiftEP MoE serving capacity +21.2%。这些直接压低 token serving cost。

**估算：** Narrow LLM serving engine 2026E 可按 38 亿美元基数和 25%-45% 增速估 48-55 亿美元；若 2026H2 agent workloads 进入企业主流程，未来 12 个月可到 60-100 亿美元。超预期需要证明 agent programs 不是一次性 demo，而是每用户每天高频调用。

**利润池：** 云平台和模型服务平台最容易把效率改善转为毛利率；独立 serving software 若开源化严重，商业化可能体现在托管平台、enterprise support、routing/cache product，而不是 license。硬件侧价值在 HBM/GPU、NVLink/RDMA/NIC、host memory、SSD/KV cache 层。

### 3. SmartNIC/DPU：从“降 CPU 开销”转为“云网络服务和内存/存储路径的执行面”

**事实：** Dell'Oro 的 Ethernet Adapter & Smart NIC 资料覆盖 1Gbps 至 1.6Tbps Ethernet controllers/adapters、SmartNIC、DPU 和 IPU；公开 press release 口径显示该市场 2028 年超过 160 亿美元，CAGR 约 27%。按该 CAGR 反推，2026 total Ethernet adapter + Smart NIC revenue 约 90-110 亿美元；SmartNIC/DPU 子集口径差异很大，保守按 10-50 亿美元处理。

**NSDI 证据：** DASH SmartSwitch 已在 Azure scale 部署；Bifrost 是 Alibaba Cloud next-generation VPC network；Net-P4ct 在 ByteDance production WAN 运行近一年；PD3、OneSidedMW、eXpressSFU、HybridMesh 显示 DPU/SmartNIC 可覆盖 memory disaggregation、video conferencing、service mesh ingress 和 cloud network services。

**估算：** 未来一年 total Ethernet adapter + Smart NIC 可到 110-160 亿美元，DPU/IPU 子集增速可能超过整体。反证是 DPU 在成本、软件复杂度或功耗上无法比 CPU offload 节省更多 TCO。

**利润池：** DPU/IPU silicon、firmware、security isolation、P4/SONiC、cloud network service integration。单纯插卡制造利润有限；真正弹性来自被 hyperscaler 放进标准 server/network rack 的 design-in。

### 4. CXL / memory pooling：远期空间大，2026 不能过度贴现

**事实：** GMI 2026-05 口径显示 CXL component market 2025 年 7.101 亿美元，2026 年 8.911 亿美元；Yole 2023 口径称 total CXL revenue 到 2028 年超过 150 亿美元，且 DRAM 构成大部分 revenue。两个数字不是冲突，而是 component market 与 broader CXL-attached memory revenue 口径不同。

**NSDI 证据：** Octopus 试图用 sparse topology 降低 CXL switch 依赖；PD3 用 DPU 预取 remote memory；OneSidedMW 通过 RNIC offloading 和 memory windows 做 one-sided memory management，在 disaggregated KV store 提升最高 10.6 倍。

**估算：** 2026-2027 是 design-in 和 pilot 阶段，未来一年 component revenue 基准 10-12 亿美元，乐观 13-18 亿美元，超预期 20 亿美元以上。若 DRAM 价格高企且新服务器平台支持 CXL 3.0，客户 ROI 更强；若 latency、安全隔离、软件栈和故障恢复不成熟，则继续停留在小批量。

**利润池：** DRAM、CXL memory module、CXL controller、PCIe/CXL retimer、switch fabric、server validation 和 hyperscaler system integration。短期最直接上市映射是 Astera Labs、Rambus/IP、Micron/Samsung/SK Hynix、Marvell/Broadcom 相关互连 IP 和服务器平台供应链，需逐家公司核实产品暴露。

### 5. CDN / edge / real-time media：总量增速未必最高，但单位成本下降有利润含义

**事实：** NSDI 2026 的视频和 CDN 论文重点不是“流量会增长多少”，而是 midgress、tail latency、QoE 和 edge resource efficiency。公开 CDN services TAM 口径分散，本报告按 2026E 250-350 亿美元处理，置信度中低。

**NSDI 证据：** Medley 降低 76.83% midgress cost，处理 0.85 million concurrent viewing requests per minute；AZEEM 在 Amazon Prime Video 生产流量中平均 QoE +2.7%、P90 +10.6%；Morphe 较 H.265 节省 62.5% bandwidth；eXpressSFU 支持 3 倍 concurrent users、计算功耗最高降 60%。

**估算：** 未来一年 TAM 基准 270-380 亿美元，乐观约 400 亿美元，超预期 450 亿美元以上。更重要的是毛利率：如果 midgress 和 compute cost 能降 20%-60%，CDN/edge gross margin 可显著改善，但客户议价可能吸收一部分收益。

**利润池：** CDN/edge platform、SmartNIC、routing software、video codec/generative streaming、边缘服务器；伪受益是只卖普通带宽、无 edge compute 和无 AI/video workload 的网络服务商。

## 反共识洞见和重要更新

### 被市场过度乐观的方向

1. **“Ethernet 已经一统 AI backend，所以所有相关股票都同等受益。”** NSDI 论文反而显示异构会长期存在：HeteCCL 用 32 H20/V100 测试床，FAST 覆盖 H200 和 MI300X，Di-PS 做 9 clusters、10,000+ NPUs 的 cross-cluster training，BURST 解决 non-RNIC-to-RNIC 互通。真正受益者是能解决异构调度、互通和可观测性的供应链，不是所有 Ethernet 标签公司。

2. **“CXL 2026 就会大规模替代本地 DRAM。”** NSDI 证据支持瓶颈真实，但 Octopus/PD3/OneSidedMW 仍偏系统设计和 prototype。2026 公开 component market 只有约 8.91 亿美元，不足以支撑过高当年收入预期。

3. **“LLM serving 软件可以独立捕获大部分 inference TAM。”** FastServe/DroidSpeak/Agentix 这类系统确实能大幅提升 throughput，但多为论文或开源方向；云厂商可能内部化收益。外部软件需要证明能控制 workload routing、cache、SLO、billing 和企业数据路径。

4. **“NSDI 会议就是 AI 概念热点。”** 错。会议中有大量生产系统论文：Matryoshka、DASH、Bifrost、EROICA、Medley、FalconFS、Net-P4ct。投资研究应以这些生产验证为主，弱化纯概念或实验室论文。

### 被市场低估的方向

1. **GPU cluster observability 和 troubleshooting。** EROICA 在 100,000 GPU 级生产集群运行 1.5 年、97.5% 诊断成功率。随着单集群 GPU 数量上升，减少 idle、straggler 和 silent performance bug 的价值会接近保险预算。

2. **DPU/SmartSwitch 的云网络服务化。** DASH、Bifrost、Net-P4ct 都说明网络功能从 host CPU 或 agent 迁移到 NPU/DPU/switch data plane。市场容易只盯 GPU 和 optics，而忽略 DPU/IPU、P4/SONiC 和 NIC firmware 的持续支出。

3. **Live streaming / video 的成本曲线。** Medley 76.83% midgress cost reduction 这种指标如果在更大平台复制，对 CDN gross margin 的影响可能大于单纯流量增长。

4. **Simulation / validation 工具。** Arcadia、Phantora、REAL、Matryoshka 证明大客户需要在采购和部署前模拟 AI cluster performance、control plane 和 routing。对第三方而言，可能出现“AI network verification / simulation”预算。

### 看似相关但弹性不强的公司或环节

| 类型 | 为什么弹性不强 |
|---|---|
| 普通 campus switch / enterprise WLAN | NSDI 的增量集中在 data-center AI backend、WAN、SmartNIC、LLM serving，不是传统园区网络 |
| 低端光模块和非合格 800G/1.6T 供应商 | AI optics 需求强，但客户认证、良率、功耗和交期决定份额；不能用行业增速代替公司份额 |
| 纯服务器组装商 | AI server revenue 高，但 GPU pass-through 和客户集中度可能压低利润率；利润池更多在 silicon、memory、networking、power/cooling、software control |
| 普通 observability SaaS | 若无法接入 GPU/NIC/switch counters、collective communication traces 和 cluster scheduler，难以替代 hyperscaler 内部 EROICA 类工具 |
| CDN 流量批发商 | NSDI 的价值在 midgress、routing、edge compute、SmartNIC offload 和 QoE optimization；只转售流量不容易捕获效率红利 |

### 需要立刻下修的反证条件

1. 2026Q2 或 2026Q3 hyperscaler capex 指引下修，或说明 AI networking / optics 是库存消化而非新增采购。
2. 800G optics 价格快速下跌且交期恢复正常，说明 supply-constrained 逻辑减弱。
3. 1.6T / CPO / LPO qualification 延迟到 2027H2 以后，1.6T 和 CPO 估值提前反映过多。
4. DPU/IPU 在云网络服务中被证实功耗、软件复杂度或可靠性不划算，host CPU offload 回潮。
5. LLM serving systems 的 efficiency gain 被更便宜模型或 on-device inference 抵消，cloud token volume 低于预期。
6. CXL server refresh 不支持规模化 memory pooling，或企业软件栈不适配 remote memory latency。
7. 大量 NSDI 论文视频/代码无法复现关键指标，或 production deployment 只适用于单一公司内部环境。

## 公司和产业链映射

### 头部公司和高确定性环节

| 环节 | 公司 / 资产 | NSDI 证据关联 | 收入暴露和投资弹性 |
|---|---|---|---|
| Hyperscaler / cloud | Google, Meta, Microsoft Azure, AWS, Alibaba Cloud, Tencent Cloud, ByteDance | Keynote、Matryoshka、Arcadia、DASH、Bifrost、EROICA、Net-P4ct、Medley、LADR、MirrorNet 等 | 直接受益于成本下降和 capex 效率，但很多收益内部化，不一定形成供应商收入 |
| AI Ethernet / switching systems | Arista, NVIDIA, Cisco, HPE/Juniper, white-box vendors | 会议大量 AI fabric、switch config、routing、collective communication 论文 | 受益于 data-center Ethernet 325 亿美元 2025 基数和 800G/1.6T 迁移；需区分 AI backend 份额 |
| Switch ASIC / SerDes / fabric silicon | Broadcom, NVIDIA, Marvell, Cisco Silicon One, merchant silicon ecosystem | ESUN/scale-up Ethernet、SONiC、P4、DASH、high-speed fabrics | 高利润池。若 hyperscaler 采用 merchant silicon 和 SONiC，ASIC/IP 弹性高 |
| Optics and optical components | Coherent, Lumentum, Innolight, Eoptolink, Fabrinet, AAOI, Hisense Broadband, 光芯片/EML/硅光供应链 | AI fabric 带动 800G/1.6T；Optical WAN tuning 证明光层可调优 | 量价弹性最高之一，但公司间良率、客户认证和产能差异决定利润 |
| NIC/DPU/IPU/SmartNIC | NVIDIA BlueField, Intel IPU, AMD/Pensando, Broadcom, Marvell, Microsoft/SONiC DASH ecosystem | DASH、Bifrost、ZOC、PD3、eXpressSFU、HybridMesh | 子行业从可选卸载变成云网络服务执行层，2026-2028 CAGR 高 |
| AI serving platforms | Baseten, major clouds, vLLM ecosystem, internal inference platforms | FastServe、DroidSpeak、Agentix、ServeGen、HydraServe、FlexLLM | 商业化关键是 workload 控制权和 SLO 计费；纯开源库收入弹性较弱 |
| CXL / PCIe / memory | Astera Labs, Rambus, Micron, Samsung, SK Hynix, Marvell/Broadcom connectivity IP, server OEMs | Octopus、PD3、OneSidedMW、CXL memory pooling | 2026 还是 early ramp，但若 CXL 3.0 server refresh 成立，2027-2028 弹性明显 |
| CDN / edge / security | Akamai, Cloudflare, Fastly, ByteDance/Tencent/Amazon internal platforms | Medley、AZEEM、Morphe、SMEC、DDoS 100 Tbps、eXpressSFU | 收入增速未必最快，利润弹性来自 midgress、SmartNIC、routing 和 edge compute efficiency |

### 小公司、上游瓶颈和配套环节

1. **交换机 ODM / JDM：** Celestica、Accton、Wiwynn/Wistron 系。2025-2026 AI network 硬件拉动明确，但利润率通常低于 ASIC 和品牌系统商，需看客户集中度和 800G/1.6T 平台份额。
2. **光模块测试与封装：** 800G/1.6T 良率、burn-in、DSP/linear drive、硅光封装、CPO 组装和测试认证会成为瓶颈。利润弹性可能高于成品模块代工。
3. **Network simulation / verification：** Arcadia、Phantora、REAL、Matryoshka 指向新预算，但可能先内部化。若出现商业产品，客户会是 neocloud、enterprise AI factory、telecom cloud。
4. **DPU software and security isolation：** KRAKENGUARD 的 eBPF isolation、DASH 的 P4 behavior spec、PD3 的 DPU path 说明安全隔离和可编程网络运行时是必要配套。
5. **AI storage metadata / vector search：** FalconFS、DistVS、Cortex、ZipLLM 显示 RAG 和 training pipeline 会把内存、SSD、network 和 metadata 服务重新定价。

### 伪受益公司识别

1. 只有传统企业网络产品、没有 data-center AI backend 订单或 800G/1.6T roadmap 的网络公司。
2. 宣称 CXL 受益但没有 CXL controller、retimer、switch、module、server qualification 或 hyperscaler design-in 的公司。
3. 宣称 LLM serving 受益但只是模型应用层，无法降低 GPU memory / KV cache / scheduling / RDMA 成本的公司。
4. 光模块公司如果 800G 良率低、客户认证慢、产能和交付被头部锁死，即使行业高增也可能不受益。
5. CDN 公司如果没有 edge compute、SmartNIC offload、routing optimization 和 video workload，只靠 bandwidth resale，难以捕获 Medley/AZEEM 类效率红利。

## 风险、反证条件和后续跟踪

### 主要风险

1. **会议属性风险：** NSDI 是学术/工程会议，不是产品发布会。论文指标可能来自特定 workload、内部系统和受控环境，不能机械外推到市场份额。
2. **公开资料不完整风险：** 截止 2026-06-10 PDT，视频陆续发布但可能未完全索引；部分 sponsor events 和 private hallway discussions 没有公开材料。
3. **估算口径风险：** 市场规模来自 IDC、Dell'Oro、650 Group、LightCounting、GMI、Yole、Fortune/DataIntelo 等不同口径，不能直接相加。
4. **客户内部化风险：** Meta、Google、Microsoft、Alibaba、ByteDance 公开的生产系统可能不会外采商业产品，供应商收入弱于技术趋势。
5. **供应链风险：** 800G/1.6T optics、HBM、GPU、DPU、CXL retimer、先进封装、测试设备和电力/液冷约束任何一个环节延迟，都可能改变放量节奏。
6. **利润率风险：** AI 硬件 revenue 高但 pass-through 多；服务器和 ODM 可能收入高、利润低；optics 高景气后可能快速价格竞争。

### 后续跟踪清单

| 节点 | 时间 | 要看什么 | 触发动作 |
|---|---|---|---|
| USENIX NSDI '26 videos / slides 完整归档 | 2026-06 至 2026-07 | Keynote、DASH、Bifrost、EROICA、Arcadia、FastServe、DroidSpeak、Medley、HeteCCL、FAST 的 slides/video 是否补充更多参数 | 更新报告附录，补 transcript 中的新数字 |
| IDC / Dell'Oro 2Q26 Ethernet switch tracker | 2026Q3 | Data-center Ethernet revenue、800G revenue share、NVIDIA/Arista/Cisco/HPE share、AI backend vs frontend | 若增速低于 20% 或库存上升，下修 networking 情景 |
| Hyperscaler 2Q26 / 3Q26 earnings | 2026-07 至 2026-11 | Amazon、Alphabet、Meta、Microsoft、Oracle capex，networking/optics/gpu capacity commentary | 确认 demand constrained 还是 supply constrained |
| NVIDIA / Broadcom / Arista / Celestica / optics earnings | 2026-08 至 2026-12 | 800G/1.6T、Spectrum-X/InfiniBand、Tomahawk/Jericho、客户集中度、gross margin | 做个股收入暴露和利润率修正 |
| OCP Global Summit / SIGCOMM / SC / HotNets / OFC 2027 | 2026H2 至 2027Q1 | ESUN、UALink、CPO、CXL、DPU/IPU、AI cluster simulation 的标准和产品路线 | 判断 NSDI 技术是否进入产品和标准 |
| CXL server platform launch | 2026H2 至 2027H1 | CXL 3.0 support、memory expansion SKU、server OEM qualification、hyperscaler pilot | 若进入批量采购，上调 CXL 2027 情景 |
| LLM serving commercial product化 | 2026H2 | Baseten/cloud platforms 是否发布 KV cache reuse、agent scheduling、serverless LLM cold-start SLA | 若按 SLO/agent program 计费，上调 narrow serving software TAM |

## 来源清单

### 一手官方材料

| 来源 | 日期 / 材料状态 | 类型 | 可信度 | 用途 |
|---|---|---|---|---|
| USENIX NSDI '26 官方主页，https://www.usenix.org/conference/nsdi26 | 会后页面，检索于 2026-06-10 PDT | 官方 | 高 | 会议日期、地点、公开 proceedings/slides、视频发布时间说明、venue、sponsor 页面入口 |
| USENIX NSDI '26 Schedule，https://www.usenix.org/conference/nsdi26/schedule | 2026-05 会议日程，检索于 2026-06-10 PDT | 官方 | 高 | Keynote 时间、3 个 technical tracks、Sponsor Events、Poster Session |
| USENIX NSDI '26 Technical Sessions，https://www.usenix.org/conference/nsdi26/technical-sessions | 2026-05 会后公开页面，检索于 2026-06-10 PDT | 官方 | 高 | 单篇论文摘要、作者、slides/media、关键指标 |
| NSDI '26 Table of Contents PDF，https://www.usenix.org/sites/default/files/nsdi26-contents.pdf | 2026-05 proceedings front matter | 官方 | 高 | 论文全集和 session 结构交叉验证 |
| Keynote: The Physics of Thought and the Architecture of Intelligence，https://www.usenix.org/conference/nsdi26/presentation/keynote-vahdat | 2026-05-04 keynote 页面 | 官方 | 高 | Google AI infrastructure framing、speaker role |
| USENIX NSDI '26 Exhibitor Resources，https://www.usenix.org/conference/nsdi26/exhibitor-resources | 2026-04/05 exhibitor materials | 官方 | 高 | Tabletop hours、展台位置、会议 WiFi/lead retrieval 等展商属性 |
| USENIX NSDI '26 Poster Session and Reception，https://www.usenix.org/conference/nsdi26/poster-session | 2026-05-05 poster session | 官方 | 高 | Poster/reception 和 Amazon sponsor 验证 |

### 公司一手材料

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| Microsoft Research, "Microsoft at NSDI 2026: Advances in large-scale networked systems"，https://www.microsoft.com/en-us/research/blog/microsoft-at-nsdi-2026-advances-in-large-scale-networked-systems/ | 2026-05-05 | 公司研究博客 | 高 | Microsoft 11 篇论文、DroidSpeak、DASH、KRAKENGUARD 等公司参与 |
| Google Cloud Next 2026 speaker/session pages for Amin Vahdat | 2026-04/05 | 公司活动页面 | 中高 | Google AI infrastructure role 和 AI Hypercomputer 语境 |
| Ennan Zhai personal publication page，https://ennanzhai.github.io/ | 检索于 2026-06-10 PDT | 作者主页 | 中 | Alibaba ServeGen、EROICA、HeteCCL、CSE/Cloud 系论文线索 |

### 技术材料和论文重点

| 技术 / 论文 | 会议证据 | 关键数字 |
|---|---|---|
| Matryoshka | Meta production-scale DCN design system | 运行 6 年，近 900 DCNs，18 types，100K-GPU supercluster |
| Arcadia | Meta/NVIDIA AI network simulation | cluster-level high-fidelity simulation，用于 AI network cross-layer design |
| DASH SmartSwitch | Microsoft Azure / SONiC | 1.53 Tbps，19.2M CPS，256M concurrent connections，power efficiency 约 1.8 倍，space efficiency 约 2.7 倍 |
| Bifrost | Alibaba Cloud VPC | Redis tail latency 最高降 307 倍，Nginx 66 倍，O(100k) concurrent connections per SmartNIC |
| EROICA | Alibaba large model training troubleshooting | 约 100,000 GPU production cluster，1.5 年，97.5% diagnosis success |
| FastServe | LLM inference scheduling | 相比 vLLM throughput 最高 6.1 倍 |
| DroidSpeak | KV cache sharing | throughput 最高 4 倍，prefill 约 3.1 倍 |
| Agentix | LLM agent serving | throughput 4-15 倍 |
| HeteCCL | heterogeneous GPU collective communication | 带宽最高 2.8/4.4/2.6 倍，训练效率 23%-37% |
| Medley | ByteDance live streaming CDN | midgress cost 降 76.83%，峰值 0.85 million concurrent viewing requests/min |
| SMEC | 5G MEC SLO management | SLO satisfaction 90%-96% vs <6%，tail latency 最高降 122 倍 |
| Learning to Tune Optical WANs | field deployment | 单 wavelength SNR 提升 2 dB |

### 市场与交易材料

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| IDC, "Ethernet switch market size and growth: Datacenter segment surges 60%+ in Q4 as AI workloads expand" | 2026-03-18 | 市场研究博客 | 高 | 2025 Ethernet switch revenue、data-center segment、800G share、vendor share |
| Dell'Oro, "Data Center Networking in 2025-2026: Milestones and Opportunities Amid Supply Risk" | 2025-12-17 | 市场研究博客 | 高 | Ethernet 超过 InfiniBand、2026 供需和 supply constraints |
| Dell'Oro, Data Center Switch - AI Back-end Networks page | 2026 页面，检索于 2026-06-10 PDT | 市场研究产品页 | 中高 | AI backend network 定义、speed migration、CPO、SONiC、scale-up/scale-out |
| 650 Group, "In the AI Era, Ethernet Set to Surge in Scale-Out and Ramp in Scale-Up" | 2026 前后，检索于 2026-06-10 PDT | 市场研究博客 | 中 | ESUN、scale-up switching 2030 >300 亿美元、networking TAM |
| 650 Group, "Navigating the Explosion in Data Center Networking Demand" | 2026 前后，检索于 2026-06-10 PDT | 市场研究博客 | 中 | 2026 data center networking >500 亿美元，2032 约 2000 亿美元 |
| LightCounting, July 2025 Cloud Data Center Optics newsletter | 2025-07 | 市场研究 newsletter | 中高 | 2025/2026 optics 30%-35% growth、800G ZR/ZR+ 上调 |
| Dell'Oro / PRNewswire, Ethernet Adapter and Smart NIC market to exceed 16 billion by 2028 | 2024-08 | 市场研究新闻稿 | 中高 | SmartNIC/DPU/adapter 市场 CAGR 和 2028 target |
| GMI, Compute Express Link component market | 2026-05 | 市场研究网页 | 中 | CXL component 2025/2026 美元规模 |
| Yole Group, CXL technology unlocks memory performance | 2023-10 | 市场研究 press release | 中高，但较旧 | CXL 2028 >150 亿美元 broader market 口径 |
| Fortune Business Insights, AI inference market | 2026 页面，检索于 2026-06-10 PDT | 市场研究网页 | 中 | Broad AI inference market 2025/2026 |
| DataIntelo, Cross-platform LLM inference engine market | 2025/2026 页面，检索于 2026-06-10 PDT | 市场研究网页 | 中低 | Narrow LLM inference engine market |

### 非官方和社交材料

| 来源 | 日期 | 类型 | 可信度 | 使用方式 |
|---|---:|---|---|---|
| Hakim Weatherspoon LinkedIn post on NSDI '26 registration/program | 2026-04 前后 | Program co-chair 社交分享 | 中 | 659 submissions、150 accepted、23% acceptance 的线索；不作为核心商业证据 |
| Ying Zhang LinkedIn post on Meta papers and activities at NSDI '26 | 2026-05 前后 | 公司研究人员社交分享 | 中 | Meta 6 papers、3 experience papers、sponsor event 的线索 |
| YouTube NSDI '26 talk videos | 2026-06 前后 | 官方/半官方公开视频 | 中高 | 会后视频线索；核心数字仍以 USENIX paper/abstract 为准 |
| Awesome Papers NSDI 2026 reading notes | 2026-04/05 前后 | 非官方论文笔记 | 低到中 | 只作 paper triage，不支撑核心结论 |
