# 会议追踪：ISC High Performance 2026

> 会议日期：2026-06-22 至 2026-06-26  
> 会议地点：德国汉堡 CCH Congress Center Hamburg  
> 材料检索截止日期：2026-07-10（美国太平洋时间）  
> 报告完成日期：2026-07-10  
> 研究范围：主会议、展览、教程、workshops，以及会议前后由参会公司、超算中心、TOP500、Green500、IO500 公布且能与本届会议相互验证的公开材料  
> 研究边界：本报告从外部公开资料独立重建；未读取、引用或继承项目内既有公司调研、行业调研、会议报告、日度资料、特征量化、缓存或中间结论。

## 结论摘要

### 核心判断

1. **AI 与传统 HPC 的融合已从“技术路线讨论”进入“采购和机房交付”阶段。** 2025 年 ISC 的官方叙事仍强调“通往融合的路径”和 extreme scaling；2026 年公开证据已是同一机柜同时承载 FP64 科学计算、低精度 AI、数据处理和量子协同的产品、订单与部署。NVIDIA Vera Rubin NVL4、Dell XE8812、HPE Cray GX5000、Supermicro 8 机柜 DCBBS 方案均以整机柜为最小工程单元，而非单卡或单节点。[S03][S06][S09][S18][S20][S22]

2. **竞争单位由芯片/节点上移至机柜、POD 和完整工作流。** 公开方案已达到每柜 144 个加速器、超过 300–362 kW；Supermicro 的 8 柜参考单元为 1,152 个 Rubin GPU、约 3.2 MW。系统价值量由 GPU 之外的 CPU、HBM、NVLink/交换、NIC/DPU、存储、CDU、母线、配电和软件共同决定。传统“GPU 出货量 × 单价”模型正在低估网络、供电和热管理，也高估没有系统资格认证的零部件受益。[S18][S22]

3. **供电和液冷已成为交付门槛，而非附属 BOM。** 2026 年会议官方兴趣排序中，AI applications/AI factories 居首，数据中心基础设施与冷却紧随其后；Dell 的新机柜要求 100% 直接液冷，nVent/Siemens 的参考架构已经把 100 MW IT 负载嵌入 136 MW 园区级电气设计。未来 12–24 个月，限制增量收入确认的更可能是变压器、开关设备、母线、CDU、冷却塔和并网，而不是芯片设计能力。[S02][S18][S42]

4. **网络不是简单的“Ethernet 取代 InfiniBand”。** 近期格局是三层并存：NVLink/NVSwitch 继续锁定 NVIDIA scale-up；InfiniBand 在欧洲和国家实验室科学系统中仍然强；Ethernet 在 scale-out 侧借 400/800G、UEC、Tomahawk 6、Spectrum-X 和真实客户部署加速。开放 scale-up 的 UALink 已有规范，但评估硬件到 2026 年末、商业部署主要落在 2026–2027 年，尚不足以改变 2026 年装机格局。CPO 已进入制造爬坡，但“制造中”不等于“客户机房已规模安装”。[S08][S11][S23][S27][S30][S31]

5. **算力的首要约束继续从 FLOPS 转向数据移动。** 开幕与闭幕 keynote 均把内存带宽、数据移动和能效列为系统瓶颈；Micron 已宣布 HBM4 高量产出货，但 CXL 远端内存仍有 NUMA、延迟、软件调度和安全隔离成本。CXL 适合 CPU 内存扩展、缓存、推理和内存池利用率优化，不是 HBM 或 GPU scale-up 互连的替代品。[S03][S32][S33][S45]

6. **存储正由“容量后端”转为训练、推理和科学工作流的数据通路，但近存储计算尚未形成大规模独立利润池。** IBM Storage Scale 6.0.1、NVIDIA BlueField-4 STX、ISC 的 IO500/内存中心存储议题都强调 GPU 直通、对象接口、向量化、缓存和元数据吞吐。产品和参考设计已经存在；可单独归因的近存储计算收入、规模部署数量仍未披露。[S26][S34][S35]

7. **欧洲 sovereign AI 采购加速，但“主权”主要体现在治理、数据和本地运营，并不等于供应链去美国化。** NVIDIA 披露欧洲 23 国有 35 套 AI-HPC 系统在建；瑞典 Mimer 的 €30 million 合同包含 400 个 GB200 GPU、IBM 存储和 Nokia 400G Ethernet。需求是真实的，底层加速器、网络与软件依赖反而显示 NVIDIA 的集中度仍高。[S08][S23]

8. **性能评价体系正分裂为多个口径。** LineShine 以 CPU-only、2.198 EFLOPS HPL 登顶 TOP500；El Capitan 的 HPL-MxP 为 16.7 EFLOPS、约为其 HPL 的 9.2 倍。Green500 前三名半年未变，说明公开列表中的能效前沿并未随每次新品发布同步跳升。未来系统采购更应跟踪 time-to-solution、能耗、精度和工作流完成率，而不是把 HPL、AI exaflops 或厂商低精度峰值互相替代。[S24][S25]

9. **量子计算在本届会议的务实变化是“作为 HPC 加速器接入工作流”，而非替代 HPC。** 教程和系统展示集中于 CUDA-Q、QPU/GPU 联合调度、模拟和编程环境；官方教程摘要明确承认尚无普遍可复现的 practical quantum advantage。未来两年更可验证的收入来自集成、云访问和科研合同，而不是通用计算替代。[S43]

10. **利润池仍高度偏向稀缺硅、内存和网络，整机集成并非同等受益。** NVIDIA 最近一季公司毛利率约 75%，Micron 在极端紧张的存储周期中公司毛利率达 84.6%；Dell ISG 经营利润率约 10.5%，HPE Cloud & AI 经营利润率约 12.4%。服务器收入高速增长不代表 OEM 利润按同样速度增长，反而可能因加速器转售占比提高而稀释利润率。[S12][S19][S21][S33]

### 相较 2025 年与会前预期：加速、放缓和转向

| 方向 | 2025 年状态 | 2026 年会后证据 | 相对变化 | 置信度 |
|---|---|---|---|---|
| AI-HPC 融合 | 主题与路线图，强调 extreme scaling | 144-GPU 机柜、FP64+AI 同栈、国家实验室和欧洲系统订单 | **加速，且从叙事转为交付** | 高 |
| 机柜级系统 | 芯片/节点仍是主要对比单位 | 300–362 kW/柜、3.2 MW 模块、100 MW IT 参考园区 | **快于会前多数单卡模型** | 高 |
| 液冷与供电 | 重要但多被视为基础设施配套 | 新一代高密度机柜要求 100% DLC；电气架构与机柜同步设计 | **显著加速** | 高 |
| HBM/内存墙 | 已知瓶颈 | HBM4 量产、混合精度仍受内存限制、CXL 生产化尝试 | **约束强化** | 高 |
| Ethernet scale-out | AI 集群中份额提升预期 | 102.4T 交换芯片量产、800G UEC 互通、Mimer 采用 400G Ethernet | **加速，但未消灭 IB** | 高 |
| 开放 scale-up | UALink 规范预期较高 | 规范完成，评估硬件晚至 2026 年末，商业部署跨 2026–2027 | **慢于“立即替代 NVLink”的预期** | 中高 |
| CPO/光互连 | 2026 被视为放量年 | 制造爬坡与 2H/Q4 可用性并存，规模客户部署尚缺公开数量 | **从概念到初始量产，但非普及** | 中高 |
| CXL 内存池 | 被期待缓解内存容量和利用率 | CXL 4.0 规范、Abaco Q4 目标；软件和延迟仍限制通用部署 | **产品化推进，经济贡献慢于预期** | 中 |
| AI 存储/近存储计算 | 关注数据摄取和 checkpoint | GPU 直通、对象/向量/缓存、DPU 参考架构明确 | **稳步推进，收入披露仍不足** | 中 |
| 量子计算 | 与 HPC 融合路线活跃 | 重点是混合工作流；没有通用实用量子优势 | **技术集成加速，商业替代放缓** | 高 |
| sovereign AI | 欧洲政策驱动 | 35 套在建系统、明确国家/中心合同 | **采购加速，供应链自主性被高估** | 高 |
| 评价体系 | TOP500 仍居中心 | HPL、HPL-MxP、HPCG、IO500、能效和业务工作流并列 | **由单一排名转向多指标** | 高 |

### 一页数字快照

| 指标 | 最新公开值 | 日期与口径 | 解释 |
|---|---:|---|---|
| ISC 2026 到场人数 | 4,035 人，64 国 | 2026-07-02，ISC 会后复盘 | 比 2025 年 3,585 人增加 12.6% |
| 展商 | 188 家，来自 26 国 | 2026-07-02 | 比 2025 年 195 家减少 3.6%；人数增长并非由展商数量扩张驱动 |
| TOP500 exascale 系统 | 5 套 | 2026-06 榜单 | HPL 口径，不等同 AI 低精度峰值 |
| LineShine | 2.198 EF HPL；42.22 MW | 2026-06 | CPU-only 登顶；约 52.1 GFLOPS/W |
| El Capitan | 1.809 EF HPL；29.685 MW；16.7 EF HPL-MxP | 2026-06 | 混合精度约为 HPL 的 9.2 倍 |
| Green500 第一名 KAIROS | 73.28 GFLOPS/W | 2026-06 | 前三名较前一榜未变 |
| 新一代 Rubin 机柜 | 144 GPU；超过 300–362 kW/柜 | 2026-06 厂商方案 | 约 2.1–2.5 kW/GPU 的整柜电力密度 |
| 欧洲 NVIDIA AI-HPC 系统 | 35 套、23 国 | 2026-06-22，已部署或已宣布口径 | 厂商称覆盖欧洲 AI factory buildout 的 90% 以上，属供应商口径 |
| Big Four 2026 capex 指引中点 | 约 $705 billion | 截至 2026-07-10；MSFT 190、AMZN 200、GOOGL 180、META 135 | 包含服务器、网络、园区和非 AI 资产，不能全视为 AI 芯片需求 |
| Dell FY2027 AI 服务器指引 | $60 billion | 2026-05 财报 | Q1 AI server revenue $16.1B；backlog $51.3B |
| NVIDIA 最近季度数据中心收入 | $75.2 billion | FY2027 Q1，2026-05-20 发布 | compute $60.4B，networking $14.8B |
| Micron 最近季度 Cloud Memory + Core Data Center | $25.293 billion | FY2026 Q3，2026-06-24 发布 | 受存储供需极紧和高价影响，不宜外推长期利润率 |

## 研究方法、证据分级与限制

### 事实、估算和观点的定义

- **事实**：来自 ISC 官方、客户/超算中心合同公告、TOP500/Green500/IO500、公司财报或厂商正式产品公告。厂商自行披露的性能和市占仍标为“厂商口径”，不自动视为独立验证。
- **估算**：用已披露收入、订单、机柜配置和 capex 指引建立的模型。所有估算均给出关键假设；不同价值链层级存在转售重复，不能相加为总 TAM。
- **观点**：基于事实和估算形成的行业判断，必须配套后续证伪指标。

### 证据等级

| 等级 | 来源类型 | 可用于何种结论 |
|---|---|---|
| A | 客户合同/部署方公告、公司财报、TOP500/Green500/IO500、正式规格和 ISC 官方复盘 | 确认部署、收入、订单、榜单数据和会议事实 |
| B | 厂商正式发布、产品页、官方博客 | 确认厂商承诺、产品配置和时间表；性能/份额需标注厂商口径 |
| C | ISC 演讲或 workshop 摘要、教程说明 | 确认技术议题和研究方向，不能单独证明量产或商业规模 |
| D | 专业媒体、参会者分享、工程师记录、供应链传闻 | 仅作线索或交叉验证；本报告的核心数字和核心结论未依赖 D 级来源 |

### 重要限制

1. ISC 的 workshops 与 tutorials 未进行完整公开录制；报告只能使用公开摘要、讲者材料和会后公开内容，不能把摘要外推成已展示的完整测试结果。
2. “AI exaflops”通常采用低精度和厂商自选口径，不能与 TOP500 HPL FP64、HPL-MxP 或实际模型 token throughput 横向相加。
3. NVIDIA 所称 Vera Rubin 与 Spectrum-X CPO“进入全面生产”，和 OEM 所称 2026 年下半年或 Q4 客户可用并不矛盾：前者是制造状态，后者是整机资格认证、交付和客户上线状态。
4. AMD MI430X 的超过 200 TFLOPS native FP64 为工程预测；Meta 6 GW、Oracle 50,000 MI450 是客户承诺/部署计划，但截至检索截止日不能写成已实现收入或已安装容量。
5. 公司未披露的 CPO 端口量、CXL 实际服务器数量、近存储计算收入和液冷单柜售价均标为未披露；报告用可审计代理变量，不把推断写成确认。

## 会议本身释放了什么信号

### 参会结构与议程重心

**事实：** ISC 官方会后复盘称，2026 年有 4,035 名参会者、188 家展商；参会兴趣中 AI applications 与 AI factories 居首，其后是 data center infrastructure/cooling 和 quantum computing。会议安排为 6 月 22 日 tutorials、6 月 23–25 日主会议和展览、6 月 26 日 workshops，共公布 24 个 workshops。[S01][S02][S05]

**事实：** 开幕 keynote“HPC: A Heterogeneous Future”把内存带宽、数据移动和能效列为关键瓶颈，并把 GPU、量子、神经形态和光子计算纳入统一异构栈；闭幕 keynote“HPC in Transition”进一步提出，AI/hyperscale 的经济性已在决定硅和系统架构，中心从 FP64、node-centric 系统转向 accelerator-heavy、rack-scale、workflow-defined 系统。[S03][S04]

**判断：** 会议关注度的真实位移不是“AI 取代 HPC”，而是 HPC 的资金、系统设计和软件调度开始按 AI factory 的交付方式重构。传统科学模拟仍保留 FP64、HPCG、确定性和精度要求，AI 则提供 surrogate model、数据同化、工作流编排和混合精度；两者在机房、网络、冷却和软件层共享基础设施。

### 2025 到 2026：从 convergence path 到可交付系统

**事实：** 2025 年官方议程以 AMD CTO Mark Papermaster 的 convergence keynote、extreme scaling 和开放生态为核心；2025 会后数据为 3,585 人、195 家展商，其中约 70 家展出 AI 产品。2026 年到场人数增长 12.6%，展商数反而下降 3.6%。[S06][S07]

**判断：** 人数上升而展商没有扩张，说明变化更像需求侧和技术决策者集中度提高，而非单纯扩展展会面积。2026 年的增量证据来自已签系统、整柜功率、量产路线和设施约束，会议对股票研究的价值高于普通新品发布会：它暴露了收入确认之前的系统级瓶颈。

## AI 与传统 HPC：融合架构及新增约束

### 从芯片到工作流的系统结构

| 层级 | 2026 年变化 | 新约束 | 产业含义 |
|---|---|---|---|
| 应用/工作流 | 模拟、AI、数据分析、数字孪生和量子协同进入统一队列 | 结果精度、可复现性、数据治理、容器/调度兼容 | 软件和系统集成价值上升，单一 benchmark 解释力下降 |
| 加速器 | GPU 同时覆盖 FP64、混合精度和推理；专用 XPU 由 hyperscaler 扩张 | HBM 容量、互连域、供电、软件可移植性 | NVIDIA 保持近期优势；AMD/custom ASIC 获得第二来源机会 |
| CPU | CPU-only LineShine 登顶；Vera、EPYC、Xeon 仍负责控制、数据和串行部分 | 内存通道、CXL、单线程/延迟、功耗 | “GPU 增长=CPU 消失”是错误映射 |
| scale-up | NVLink/NVSwitch 将 72/144 GPU 组成紧耦合域；UALink 开放路线推进 | 拓扑、故障域、软件一致性、铜/光距离 | NVLink 近期锁定，UALink 是 2027+ 选择权 |
| scale-out | InfiniBand 与 Ethernet 并存，800G/CPO 进入首批产品周期 | 拥塞控制、尾延迟、光学良率、可观测性 | Ethernet 份额上升，但 IB 在科研系统仍具确定性优势 |
| 内存 | HBM4 量产；CXL 扩展/池化；混合精度仍遭遇 memory wall | 带宽、延迟、容量、NUMA 和数据移动能耗 | HBM 稀缺溢价持续，CXL 先进入选择性场景 |
| 存储 | GPU Direct、对象访问、向量/缓存、元数据优化 | checkpoint、small-file、数据准备、GPU 饥饿 | AI storage 增速快于传统容量存储，近存储计算仍早期 |
| 供电/冷却 | 300–362 kW/柜、100% DLC、MW 级模块化 | 并网、变压器、开关柜、CDU、水温、热回收 | 收入确认受设施节奏约束；机电供应商订单能见度提高 |

### GPU、CPU 与专用加速器

**GPU——事实：**

- NVIDIA 披露有 238 套 TOP500 系统使用其 GPU、376 套使用其网络；该统计为厂商对榜单的归类，系统数量可核对，但“使用 NVIDIA”不等于整套系统价值均由 NVIDIA 获得。[S10]
- Vera Rubin NVL4 面向科学计算的公开配置为最高 144 GPU/柜、超过 7 AI exaflops、5 PFLOPS native FP64，并集成 Vera CPU、ConnectX-9、BlueField-4 和直接液冷；LRZ Blue Lion、Dell Doudna、LANL Mission/Vision/Veritas 已有明确部署方或选型方。[S09]
- AMD 在 TOP500 的 CPU/GPU 覆盖增加，Alice Recoque 计划采用 MI430X 和第六代 EPYC；MI430X 的超过 200 TFLOPS native FP64 是工程预测而非已验收实测。[S13][S14]
- AMD 与 Meta 正式公告最多 6 GW 的多年合作、首 1 GW 计划 2026 年下半年；Oracle 计划建设 50,000 MI450 的公有 supercluster。两者均属于客户承诺/部署计划，不是截至截止日的已安装容量。[S15][S16]

**CPU——事实：** LineShine 使用 13.79 million 个自研 CPU 核心，以 2.198 EFLOPS HPL 和 42.22 MW 登顶。它证明大规模 CPU-only 仍可达到 HPL exascale，但不能据此推断其 AI 训练经济性或通用可采购性。[S24]

**专用加速器——事实：** Broadcom FY2026 Q2 AI semiconductor revenue 为 $10.8B、同比增长 143%，并预计下一季度约 $16B；该口径同时包含 custom accelerator 和 AI networking，无法公开拆分。AWS 表示过去 12 个月落地超过 2.1 million 个 AI chips，其中过半为 Trainium，同时计划从 2026 年起部署超过 1 million 个 NVIDIA GPU。AMD 最近季度 Data Center revenue 为 $5.8B，仍是当前第二来源规模的财务锚。[S17][S28][S37]

**判断：** 未来两年不是 GPU 与 ASIC 的零和替代，而是 workload 分层：前沿训练、科学计算和软件生态继续偏 GPU；稳定、规模化的 hyperscaler 内部负载增加 custom XPU；CPU 保留控制面、数据预处理、传统 HPC 和内存容量型负载。最容易被高估的是“任何 ASIC 设计能力都能转为规模收入”，最容易被低估的是软件迁移、网络和客户验收时间。

### HBM、主存与 CXL

**事实：**

- Micron 于 2026-06-24 披露 HBM4 已为主要平台进行 high-volume shipment，HBM4E 预计 2027 年生产；同季公司收入 $41.456B、GAAP gross margin 84.6%，Cloud Memory 和 Core Data Center 合计收入 $25.293B。极高利润率反映当前供需和定价周期，不是长期稳态。[S33]
- CXL 4.0 已提高到 128 GT/s 并支持 port bundling 与增强 RAS；CXL Consortium 同时强调远端池化内存具有不同性能特征，需要 NUMA-aware 软件优化。[S32]
- ISC 的 Micron/PNNL Crete 2.0 与 Abaco 3.0 演讲把几十至数百 TB 近端/扩展内存用于推理、向量数据库和图计算，并称 Abaco 3.0 目标为 2026 Q4 production-ready。此处是演讲方路线图，尚无公开客户数量。[S45]

**判断：**

1. HBM 的核心价值是极高带宽和 GPU 邻近性；CXL 的核心价值是容量、资源利用率和 CPU/加速器外部内存分层。两者解决的问题不同。
2. 混合精度能减少算术和部分带宽负担，但对延迟敏感、内存容量受限和 irregular access 的工作负载，memory wall 仍然存在。
3. CXL 2026–2027 的可投资收入更可能先体现在 switch/controller、DRAM 容量和特定 hyperscaler 服务器，而不是“共享内存池全面取代本地 DRAM/HBM”。

### Ethernet、InfiniBand、光互连与 scale-up/scale-out

| 路线 | 公开产品/证据 | 截至 2026-07-10 的状态 | 竞争判断 |
|---|---|---|---|
| NVLink/NVSwitch scale-up | Vera Rubin NVL4 72/144 GPU 域 | 制造爬坡；OEM 整机 2H/Q4 可用 | 近期唯一大规模、完整软硬件闭环；锁定效应最强 |
| UALink scale-up | 1.0 规范，200G/lane，最多 1,024 accelerators | 评估硬件预计 2026 年末；商业部署跨 2026–2027 | 是开放选择权，不是当前装机替代 |
| InfiniBand scale-out | Quantum-X800、IT4LIA、BSC、Doudna、LANL 等 | 已部署和已签系统并存 | 在科研、MPI 和确定性低延迟场景仍强 |
| Ethernet scale-out | Spectrum-X、Tomahawk 6、UEC 800G、Mimer 400G Ethernet | 交换芯片量产、互通演示和真实客户部署均有 | 份额上升最快；多供应商与云生态优势明显 |
| CPO/NPO | NVIDIA Spectrum-X/Quantum-X CPO；Broadcom CPO/NPO | 部分器件制造爬坡，广泛客户安装量未披露 | 首先解决 800G/1.6T scale-out 功耗与可靠性，scale-up 光化更晚 |
| CXL | CXL 4.0、Crete/Abaco | 规范成熟、选择性产品化 | 是内存语义互连，不应与 GPU fabric 直接等同 |

**事实：** Broadcom 于 2026-03 宣布 102.4 Tb/s Tomahawk 6 已进入 production volume；Keysight/Broadcom 展示 800GE UEC LLR/CBFC 互通，但互通演示不等于多厂商生产网络已经安装。Mimer 的客户合同明确采用 Nokia 7220 400G Ethernet，说明 Ethernet 已不只存在于实验室。[S23][S27][S30]

**事实：** NVIDIA 对 CPO 的公开口径包括约 5 倍 power efficiency、5 倍运行时间、Spectrum-X 最高 409.6 Tb/s，并称 2026 年下半年可用；这些性能是厂商设计目标/测试口径。公开材料没有给出客户已安装端口量、光引擎良率或现场故障率。[S11]

**判断：**

- **未来 3 个月：** Ethernet 的确定性增量来自 800G 交换、NIC 和光模块；InfiniBand 随已签科研系统继续增长。CPO 的主要验证项是出货、资格认证和现场运行，而非新品数量。
- **未来 1 年：** scale-out Ethernet 份额继续提升，尤其在 hyperscaler、sovereign AI 和多供应商集群；NVIDIA 内部 NVLink+Spectrum-X/InfiniBand 的全栈组合仍占高端。UALink 若不能出现两个以上加速器和交换芯片厂商的可采购产品，将继续停留在规范选择权。
- **未来 2 年：** 光互连向更短距离推进，但铜缆、LPO/NPO、可插拔和 CPO 会长期共存。真正改变 scale-up 格局需要硬件、collective library、故障恢复和调度器同时成熟。

### 存储、IO500 与近存储计算

**事实：**

- ISC26 IO500 production list 第一名 SCNet AICS-A/Sugon ParaStor 的综合分数为 79,110，带宽项约 26,888 GiB/s、元数据项约 232,755 kIOPS；IO500 同时存在 production、research 和 full list，旧提交也可能保留，不能把榜单名次直接写成当季新增订单。[S26]
- IBM Storage Scale 6.0.1 增加 GPU Direct、cuObject 和大规模多租户能力；这是正式软件版本，而不是概念展示。[S34]
- NVIDIA BlueField-4 STX 是由 DPU、参考架构和多家存储合作伙伴组成的方案，厂商称可提高 token throughput、能效和 ingest，合作伙伴平台计划 2026 年下半年可用；截至截止日属于 reference architecture + early adopter，而非公开规模收入。[S35]

**判断：** AI 存储利润池将沿三条线增长：高吞吐 checkpoint/训练文件系统、推理 KV/cache/对象数据通路、元数据与数据准备软件。所谓“近存储计算”只有在减少 GPU 空转时间或网络流量、且能被调度/安全体系管理时才有价值；单纯在 SSD 或 DPU 上增加算力不是充分条件。

### 供电、液冷和数据中心建设

**事实：**

- Dell XE8812 NVL4 公开为 144 GPU/柜、超过 300 kW、100% direct liquid cooling；Supermicro 的 8 柜方案为 1,152 GPU、约 3.2 MW 模块，单柜设计约 362 kW。[S18][S22]
- Siemens 与合作伙伴的 NVIDIA AI data center reference architecture 以 136 MW facility、100 MW IT load 为设计点；nVent 称已部署超过 2 GW liquid-cooling capacity，后者为供应商自报累计口径。[S42]
- Vertiv 2026 Q1 sales $2.65B、同比增长 30%，adjusted operating margin 20.8%，全年销售指引中点约 $13.75B；Eaton 同季 Electrical Americas 与 Electrical Global 合计销售约 $5.5B，经营利润率分别为 25.6% 和 19.2%，数据中心订单和收入保持高增。[S40][S41]

**估算：** 以 300–362 kW/柜计，100 MW IT 电力理论上只能承载约 276–333 个满载高密度柜；考虑网络、存储、CPU 柜、冗余、降额和运行余量，可运营的等效 144-GPU 柜约 220–290 个，对应约 31,700–41,800 个 GPU。该计算是容量上限，不是特定园区配置。

**判断：** 数据中心 capex 的边际瓶颈已经从“能否买到 GPU”扩展为“能否把 300 kW 以上负载安全、持续地供电和排热”。这提高供配电、液冷和热交换资产的订单能见度，也引入更长的建设周期：芯片能在一个季度内改变收入，变电与园区许可通常不能。

### 量子计算：混合加速器，而非近期替代

**事实：** 本届量子教程和 workshop 重点是 CUDA-Q、GPU/QPU 联合编程、LRZ GPU 与 IQM QPU 的混合环境、量子系统模拟以及科研工作流。教程公开摘要明确指出，当前尚无普遍意义上的 practical quantum advantage。[S43]

**判断：** 两年内可投资的量子收入主要来自科研设备、云访问、控制电子、软件和与 HPC 中心的集成。把量子写成 GPU/CPU 需求的近期替代属于过度乐观；更现实的受益者是为混合工作流提供经典模拟、控制和数据中心集成的现有供应商。

## 量产、订单、明确路线图与概念展示

### 状态判定规则

- **已部署/可验证运行：** 有榜单、客户或运营方公开的已安装系统和运行数据。
- **量产/可采购：** 厂商已宣布 production 或正式版本，但仍需区分器件出厂与整机客户上线。
- **已签订单/明确部署计划：** 有客户、合同金额、数量、地点或时间表；截至截止日未必已确认收入。
- **明确路线图：** 有具体季度/年份和产品规格，但缺少客户验收或规模出货。
- **概念/研究展示：** 只有论文、演示、参考设计或性能预测，不能计入当前市场规模。

### 关键产品与系统状态矩阵

| 产品/系统 | 公开状态 | 量产、订单或部署证据 | 本报告归类 | 下一验证点 |
|---|---|---|---|---|
| LineShine | TOP500 #1，2.198 EF HPL | 榜单有配置、功耗与基准数据 | **已部署/运行** | HPCG、应用可用性、后续榜单与对外服务 |
| JUPITER | TOP500 #5；20,480 GH200 | 系统榜单与运营方/厂商应用案例 [S46] | **已部署/运行** | 稳态功耗、用户利用率、科学工作流产出 |
| KAIROS/ROMEO/Levante | Green500 前三，GH200 + BullSequana XH3000 | 榜单复核；排名半年未变 | **已部署/运行** | 新一代 Rubin 是否在后续榜单提高 GFLOPS/W |
| NVIDIA Vera Rubin 芯片与平台 | 厂商称进入全面生产 | 晶圆、系统组件和 OEM 生态制造爬坡 | **器件量产爬坡** | 2H/Q4 OEM 客户交付、现场验收和收入占比 |
| Dell XE8812 NVL4 / Doudna | 144 GPU、>300 kW、100% DLC | Dell 与客户项目公开；具体验收进度未完全披露 | **已选型/待交付** | Q4 出货、Doudna 上线、AI server backlog 转收入 |
| HPE Cray GX5000 / LANL Mission、Vision、Veritas | Rubin、Slingshot 400、DLC | 国家实验室选型与 HPE 产品路线 | **已选型/路线明确** | 客户验收、系统收入和 Slingshot 400 实际规模 |
| Supermicro 8 柜 Rubin DCBBS | 1,152 GPU、3.2 MW 参考单元 | 正式 blueprint，无公开对应客户金额 | **工程蓝图/待订单** | 已签客户、BOM、CDU/配电交付与毛利率 |
| AMD MI450/Helios | Meta 最多 6 GW；首 1 GW 计划 2H 2026；Oracle 50,000 MI450 计划 Q3 起 | 客户与 AMD 正式公告 | **已承诺/待出货** | 首批出货、ROCm 稳定性、客户验收与收入确认 |
| AMD MI430X | >200 TF native FP64 预测；Alice Recoque 计划采用 | 工程预测和未来系统选型 | **明确路线图，不是量产实绩** | 实测 FP64、功耗、HBM、系统上线日期 |
| Broadcom Tomahawk 6 | 102.4 Tb/s | 厂商称 production volume | **量产** | 交换系统收入、800G/1.6T 端口量、客户集中度 |
| UEC 800G | LLR/CBFC 互通演示；1.0.x 规范 | 公开互通，不含大规模客户网络数量 | **规范+互通，早于普及** | 多厂商生产网络、拥塞/尾延迟现场数据 |
| NVIDIA Spectrum-X/Quantum-X CPO | 厂商称制造爬坡；2H 2026 可用 | 正式产品与生态合作 | **初始量产/待客户规模部署** | 光引擎良率、端口出货、现场故障率与可维护性 |
| UALink 1.0 | 200G/lane，最多 1,024 accelerators | 规范完成，评估硬件预计晚 2026 | **路线图** | 至少两家加速器和交换厂商的可采购产品 |
| Micron HBM4 | lead platform high-volume shipment | 2026-06-24 财报确认 | **量产** | 2027 供给、ASP、良率和 HBM4E 节奏 |
| CXL Abaco 3.0 | 目标 2026 Q4 production-ready | ISC 演讲路线图；客户数量未披露 | **路线图/试点** | 生产 SKU、部署服务器数、延迟和 TCO |
| IBM Storage Scale 6.0.1 | GPU Direct、cuObject、多租户功能 | 正式软件发布 | **量产软件** | AI 客户增长、软件收入和 GPU 利用率改善 |
| NVIDIA BlueField-4 STX | DPU + 存储参考架构 | early adopters/合作伙伴，平台 2H 2026 | **参考架构/初始采用** | 生产系统数量、独立 benchmark、可归因收入 |
| 混合量子-HPC | CUDA-Q、IQM QPU、模拟与联合调度 | 教程、研究系统和科研环境 | **研究/早期部署** | 可复现实用优势、付费利用率和非科研客户 |

### “production”口径冲突的处理

| 表面冲突 | 差异来源 | 正确读法 |
|---|---|---|
| Vera Rubin 已全面生产 vs OEM Q4 可用 | 芯片/组件制造状态 vs 服务器资格认证、物流与客户验收 | 2026 Q3 可开始确认部分供应链收入，规模客户算力上线更偏 Q4 及以后 |
| CPO 已生产 vs 缺少现场端口数据 | 光引擎/交换硅制造 vs 完整交换机、布线、运维部署 | 不能把 tape-out 或生产线爬坡写成广泛渗透率 |
| AMD 有 6 GW/50,000 GPU 客户 vs 当前份额仍低 | 长期容量承诺 vs 当期装机/收入 | 订单提高 2027 可见度，但执行取决于 MI450、Helios、ROCm 和设施 |
| HBM4 high-volume shipment vs 终端系统仍待 Rubin | 内存提前备货与平台生产周期不同 | 内存供应商收入可领先整机上线一个到数个季度 |
| IO500/TOP500 榜单名次 vs 当季市场份额 | 榜单包含既有系统，提交策略不同 | 用于验证技术能力，不能直接转换为当季订单或收入 |

## TOP500、Green500、HPCG 与 IO500 的独立校验

### TOP500：exascale 增加，但架构并未收敛为单一路线

**事实：**

- 2026 年 6 月 TOP500 出现 5 套 exascale 系统。LineShine 以 2.198 EF HPL、42.22 MW 排名第一；El Capitan 以 1.809 EF、29.685 MW 第二；Frontier、Aurora、JUPITER 分列其后。[S24]
- LineShine 是 13.79 million core 的 CPU-only 系统，HPL efficiency 约为峰值的 80%；它打破了“exascale 必然等于 GPU”的简单叙事，但系统可采购性、软件生态和 AI 经济性没有由 HPL 证明。
- HPCG 榜单中，LineShine 为 22.0 PFLOPS、El Capitan 为 17.41 PFLOPS、Fugaku 为 16.0 PFLOPS。HPCG 更重视内存访问和通信，仍不能代表所有真实应用，但可用于校验 HPL 之外的系统平衡。[S24]

**判断：** 加速器重构商业和科研采购是主线，但 CPU、大内存和通信平衡仍能在特定工作负载形成竞争力。投资研究应区分“全球可销售平台”与“单一国家/中心的定制系统”：前者决定可持续收入，后者更多验证技术边界。

### 混合精度：有效 zettascale 是方法论，不是同一精度下的硬件跨越

| 系统 | HPL | HPL-MxP | HPL-MxP/HPL | 解释 |
|---|---:|---:|---:|---|
| El Capitan | 1.809 EF | 16.7 EF | 约 9.2× | 混合精度与算法让可用吞吐显著高于 FP64 HPL |
| LineShine | 2.198 EF | 7.92 EF | 约 3.6× | 同一系统在不同精度/算法口径差异很大 |

**判断：** Jack Dongarra 所称“effective zettascale”应理解为经过精度认证的混合精度、communication-avoiding、AI surrogate 和模拟-AI 组合，不应宣传为已经存在 1 ZFLOPS FP64 机器。对芯片需求的含义是：更低精度提高每瓦吞吐，但更大模型和更高利用率可能继续推高总功耗，Jevons effect 仍然存在。

ISC 的 mixed-precision 公开演讲同时指出，低精度并不能消除 memory- and latency-bound 工作负载的瓶颈，这与榜单口径分化相互印证。[S44]

### Green500：能效仍重要，但榜单没有证明新品宣传已经落地

**事实：** 2026 年 6 月 Green500 前三为 KAIROS 73.28、ROMEO 70.91、Levante 69.43 GFLOPS/W，均为 BullSequana XH3000、GH200 与 NDR200 架构；前三名较前一榜保持不变。[S25]

**判断：** 新平台声称的单位算力能效改善，要经过整机、冷却和生产负载验证。榜单前沿没有同步跳升，可能来自部署节奏、提交选择或系统尚未上线；因此不能用发布会中的芯片能效直接推导园区 PUE、年度电费或 Green500 排名。

### IO500：带宽与元数据都重要，单一峰值不足以评价 AI 数据通路

**事实：** ISC26 production list 的第一名在带宽和元数据两项均有高分；research/full list 则可能出现更高的单项结果。列表分类、测试规模和提交时间不同。[S26]

**判断：** 训练 checkpoint 需要大带宽，推理/向量检索和数据准备常受 small-file、metadata、随机读取和对象操作限制。只买高带宽阵列而忽略元数据、网络和数据格式，会导致 GPU 利用率低于采购模型。

## 对未来 3 个月、1 年和 2 年的行业判断

### 分环节时间表

| 环节 | 未来 3 个月：至 2026-10 | 未来 1 年：至 2027-07 | 未来 2 年：至 2028-07 |
|---|---|---|---|
| 服务器/加速器 | Rubin OEM Q4 可用性、MI450/Helios 首批交付、Dell backlog 转收入成为主验证；收入先于大规模客户上线 | Rubin 与 MI450 进入主要部署年；整柜 ASP 上升但单位算力价格下降；第二来源采购增加 | 加速器增长仍高但基数效应出现；更多 custom XPU，通用 GPU 份额可能下降、绝对收入仍可增长 |
| CPU | Vera/EPYC 随 GPU 柜增长；传统 HPC 和大内存节点稳定 | CXL 与内存容量型服务器选择性扩张 | CPU 与加速器更深封装/一致性互连；CPU 价值转向数据、控制和内存服务 |
| 网络 | 800G Ethernet/IB 同时放量；CPO 首批客户交付是关键事件 | Ethernet scale-out 份额提升，1.6T 开始贡献；NVLink 维持 scale-up | 光学向更短距推进；UALink 若形成多供应商产品，才会实质挑战 NVLink |
| HBM/内存 | HBM4、server DRAM 和高容量 SSD 继续紧；价格支撑供应商利润 | 新供给释放但需求增长；基准情景下利润率从极端高位温和回落 | HBM4E/下一代堆叠扩张；容量增长快于带宽改善，memory wall 仍在 |
| CXL | Abaco 等生产化节点；以试点和特定工作负载为主 | hyperscaler CPU 内存扩展、缓存和推理池化选择性放量 | 软件/安全成熟后扩大，但仍不取代 HBM 和 GPU fabric |
| 存储 | BlueField STX 合作平台、IBM 6.0.1 和 GPU Direct 项目开始验证 | AI storage 增速高于传统企业存储；软件和数据编排获取更多价值 | 推理上下文、KV/cache 和多模态数据使存储成为常态化算力配套 |
| 液冷/供电 | 订单和 backlog 继续增长；资格认证、并网与现场施工限制交付 | >100 kW 新 AI 柜中 DLC 成为主流，CDU/母线/开关设备价值量提升 | 园区电力成为首要选址因素；热回收、较高进水温度和模块化电气设计扩展 |
| 数据中心 capex | Big Four 约 $690–720B 的 2026 指引提供支撑，未见会议导致削减 | 基准模型约 $810B；建设结构从短寿命计算向长寿命电力/网络倾斜 | 增速可能低于 2026–2027，但设施瓶颈使绝对支出维持高位；折旧和利用率压力上升 |
| 量子 | 研究和混合工作流合同，不影响主流服务器采购 | 增加 QPU-HPC 调度和模拟需求，收入仍小 | 除非出现可复现实用优势，否则仍是科研/期权资产 |

### 资本开支传导的关键顺序

1. **最先确认：** HBM、GPU/ASIC、交换硅和已排产服务器，可在制造爬坡时先确认收入。
2. **随后确认：** 整机柜、NIC/DPU、光模块、并行文件系统和本地 CDU，取决于客户验收。
3. **更长周期：** 变电、开关设备、母线、冷却塔、冷机/干冷器、建筑和并网；订单可见度较长，但收入确认受工程进度影响。
4. **最晚验证回报：** 云 AI 收入、模型服务毛利、客户利用率和折旧回收。高 capex 不自动等于高股东回报。

## 当前市场规模与未来一年三情景

### 可核验的当前收入和订单锚

下表是公开财报/指引，不是本报告估算。不同公司处于价值链不同层，存在同一产品在硅供应商、OEM 和云厂商重复确认收入的情况，**不得横向相加为总市场**。

| 公司/买方 | 最新公开指标 | 年化或指引读法 | 利润率/质量提示 | 来源日期 |
|---|---:|---:|---|---|
| NVIDIA | Data Center $75.2B/季；compute $60.4B；networking $14.8B | 简单年化约 $300.8B，其中 compute $241.6B、networking $59.2B | 公司 GAAP gross margin 74.9%；非纯数据中心利润率 | 2026-05-20 |
| AMD | Data Center $5.8B/季 | 简单年化 $23.2B，含 EPYC 与 Instinct | 公司 GAAP gross margin 53%；MI450 尚待放量 | 2026 Q1 |
| Broadcom | AI semiconductor $10.8B/季；下一季预计 $16B | 当前年化 $43.2B，forward-quarter run-rate $64B | 含 custom XPU 与 networking，不能拆分 | FY2026 Q2 |
| Marvell | 公司收入 $2.418B/季 | 简单年化约 $9.7B | 公司 non-GAAP gross margin 58.9%；AI optics/network/custom XPU 只占其中一部分 | FY2027 Q1 |
| Dell | Q1 AI server revenue $16.1B；backlog $51.3B；FY2027 guide $60B | 指引比单季年化略低，显示季度节奏/验收影响 | ISG operating margin 10.5%；加速器 pass-through 高 | FY2027 Q1 |
| HPE | Cloud & AI $7.7B/季；server $5.5B；storage $1.2B；network $2.7B | 各分部披露口径不可简单相加 | Cloud & AI operating margin 12.4%；Network 21.6% | FY2026 Q2 |
| Micron | Cloud Memory + Core Data Center $25.293B/季 | 简单年化约 $101.2B | 公司 GAAP gross margin 84.6%，为异常紧张周期，不是稳态 | FY2026 Q3 |
| Vertiv | Q1 revenue $2.65B；FY2026 guide $13.5–14.0B | 全年中点 $13.75B | Q1 adjusted operating margin 20.8%；不全是 AI | 2026 Q1 |
| Eaton | Electrical Americas + Global $5.5B/季 | 简单年化约 $22B，只有一部分属于数据中心 | 两分部 operating margin 25.6%/19.2% | 2026 Q1 |
| Microsoft | CY2026 capex 约 $190B | 约 2/3 为较短寿命 GPU/CPU，1/3 为长寿命数据中心资产的季度口径指引 | 买方 capex，不是供应商收入 | 截至 2026 Q3 call |
| Alphabet | FY2026 capex $175–185B | 中点 $180B | 约 60% 服务器、40% 数据中心/网络的历史结构，实际会变化 | 2026 指引 |
| Amazon | FY2026 capex 约 $200B | AI、AWS、物流及其他资产，不全属于 AI | 买方 capex；自研芯片和 NVIDIA 并存 | 2026 指引 |
| Meta | FY2026 capex $125–145B | 中点 $135B | 大量用于自有 AI 基础设施 | 2026 Q1 指引 |

Big Four capex 中点 $705B 分别由 Microsoft、Amazon、Alphabet 和 Meta 的公开材料约束；这些是买方支出而不是 AI 供应商 TAM。[S36][S37][S38][S39]

### 模型口径

**估算基准：** 以 2026 年最新季度年化、公司全年指引和已披露订单建立“价值链层级收入池”。各层存在渠道重复，主要用于判断谁获取收入和利润，不能相加成总 AI 基础设施 TAM。

**三种情景：**

- **悲观：** 客户验收延迟、云 AI 收入兑现不足、2027 capex 暂停增长，HBM/整机价格回落，电力许可延误。
- **基准：** Rubin、MI450、800G/CPO 和液冷大体按 2H 2026–2027 路线交付，Big Four capex 增长约 15%，供应约束逐步缓解但需求仍强。
- **乐观：** sovereign/hyperscaler 订单加速、设施供给改善、模型和 agent 工作负载扩大，价格与产品 mix 同时支撑收入。

### 2026 当前规模与 2027 收入三情景

单位：$ billion。当前规模为模型区间和中枢；2027 为未来一年的全年收入/支出口径。

| 价值链层 | 2026 当前模型区间（中枢） | 2027 悲观 | 同比中枢 | 2027 基准 | 同比中枢 | 2027 乐观 | 同比中枢 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 加速计算硅与平台 | $300–360（$330） | $310 | -6% | $400 | +21% | $500 | +52% |
| AI 网络/互连硅、NIC、交换和光学 | $80–110（$95） | $80 | -16% | $115 | +21% | $155 | +63% |
| HBM、数据中心 DRAM 与高端 SSD | $150–190（$170） | $150 | -12% | $220 | +29% | $285 | +68% |
| AI 服务器/机柜 OEM 集成收入 | $110–150（$130） | $125 | -4% | $175 | +35% | $235 | +81% |
| AI 相关存储硬件与软件 | $35–55（$45） | $42 | -7% | $60 | +33% | $82 | +82% |
| AI 相关供配电、液冷与热管理 | $40–60（$50） | $55 | +10% | $72 | +44% | $95 | +90% |
| Big Four capex（买方支出，不是供应商收入） | $690–720（$705） | $660 | -6% | $810 | +15% | $930 | +32% |

### 利润池三情景

利润口径因行业不同：硅、网络和内存用 gross profit；OEM、存储与基础设施用 operating profit。它们不可相加为统一净利润。

| 层级 | 2026 当前利润池估算 | 2027 悲观：收入/利润率/利润 | 2027 基准：收入/利润率/利润 | 2027 乐观：收入/利润率/利润 |
|---|---:|---:|---:|---:|
| 加速计算硅与平台 | GP $215–248B（65–75%） | $310B / 60% / **$186B GP** | $400B / 68% / **$272B GP** | $500B / 73% / **$365B GP** |
| AI 网络/互连 | GP $48–62B（50–65%） | $80B / 50% / **$40B GP** | $115B / 58% / **$67B GP** | $155B / 63% / **$98B GP** |
| HBM/DC memory/SSD | GP $94–136B（55–80%） | $150B / 45% / **$68B GP** | $220B / 60% / **$132B GP** | $285B / 72% / **$205B GP** |
| AI 服务器/机柜 OEM | OP $10–16B（8–12%） | $125B / 7% / **$9B OP** | $175B / 10% / **$18B OP** | $235B / 12% / **$28B OP** |
| AI storage | OP $5–8B（10–18%） | $42B / 8% / **$3B OP** | $60B / 14% / **$8B OP** | $82B / 18% / **$15B OP** |
| 供配电/液冷/热管理 | OP $8–12B（15–23%） | $55B / 15% / **$8B OP** | $72B / 20% / **$14B OP** | $95B / 24% / **$23B OP** |

**模型解释：**

1. 加速计算层的当前中枢由 NVIDIA Data Center compute 年化 $241.6B、AMD Data Center $23.2B，以及无法完全拆分的 custom XPU/其他平台收入约束；不是独立审计的市场规模。
2. 网络层用 NVIDIA networking 年化 $59.2B、Broadcom AI semis、Marvell 和系统/光学价值量约束。Broadcom 的 custom XPU 与 networking 无法拆分，因此模型特意给区间而不把公司数字直接相加。
3. 内存层用 Micron 两个数据中心分部年化 $101.2B 及其主要同业份额作约束；2026 极高毛利率含价格周期，悲观和基准情景均假设正常化。
4. OEM 层包含大量加速器 pass-through，和硅平台层重复；其意义是判断收入规模与 7–12% 经营利润率，而非新增 TAM。
5. 电力/冷却层以 Vertiv、Eaton 分部、nVent 等公开收入和订单为锚，但只计模型归因于 AI 数据中心的部分。

### 机柜价格、出货量、功耗与价值量假设

| 参数 | 悲观 | 基准 | 乐观 | 依据与限制 |
|---|---:|---:|---:|---|
| 144-GPU 高端整柜系统 ASP | $8.0M | $10.0M | $13.0M | 含 GPU、CPU、HBM、scale-up fabric、NIC/DPU、机柜和基础集成；不含完整园区 |
| 72-GPU rack-equivalent ASP | $4.0M | $4.4M | $4.8M | 用于把平台收入换算为可比较出货价值，不代表实际物理机柜 |
| 2027 72-GPU rack-equivalent | 约 77,500 | 约 90,900 | 约 104,200 | 分别用 $310B/$4.0M、$400B/$4.4M、$500B/$4.8M；含板卡/节点等价换算 |
| 144-GPU 满载整柜功耗 | 300 kW | 330–362 kW | 400 kW 级 | Dell/Supermicro 为公开锚；高情景考虑更多网络、CPU 和功率裕量 |
| 每 GPU 整柜功率 | 约 2.1 kW | 2.3–2.5 kW | 约 2.8 kW | 含整柜而非仅芯片 TDP |
| 网络价值/加速计算平台收入 | 20% | 25–27% | 30% | NVIDIA 最近季度 networking/compute 为 24.5%，用作可观察锚 |
| HBM+host memory+本地高端 SSD 价值/加速器 | $8,000 | $12,000 | $18,000 | 模型估算；容量、代际和价格差异很大 |
| >100 kW 新增 AI 柜的直接液冷渗透率 | 65% | 85% | 95% | 工程假设；不代表全部现有服务器存量 |
| 供配电+冷却机电价值/新增 IT MW | $3M | $4.5M | $6M | 不含土地、建筑、GPU/服务器和长距离电网；用于设备/工程敏感性 |

**价格交叉验证：** 瑞典 Mimer 的 €30M 合同对应 400 个 GB200 GPU，粗略为 €75,000/GPU，但合同还含服务器、400G Ethernet、IBM storage、冷却和服务。按模型简化汇率 €1=$1.15，约 $86,000/GPU，落在本报告 144-GPU 整柜 $8–13M、即 $56,000–90,000/GPU 的全栈价值区间上沿。该换算用于量级校验，不是 NVIDIA GPU 报价。[S23]

**最重要的敏感性：**

- 每个 rack-equivalent ASP 每下降 10%，若需求弹性不能把出货提高 11.1%，平台收入会下降。
- 网络 attach ratio 每提高 5 个百分点，以 $400B 加速平台计，对应约 $20B 网络价值量变化。
- 每新增 10 GW IT 负载，按 $3–6M/MW 的供配电+冷却机电假设，对应 $30–60B 设备/工程价值；但并网和交付可能跨多年。
- Micron 当前毛利率若从 84.6% 回落到 60%，即使收入不降，利润池也会明显收缩，因此“HBM 收入增长”与“内存股利润继续同比加速”不是同一命题。

## 展览、教程、workshops 与奖项的增量信号

### 公开内容能支持的判断

| 场域 | 公开议题/证据 | 产业含义 | 证据限制 |
|---|---|---|---|
| 主会议 | heterogeneous future、HPC in transition、数字孪生、模拟+AI | HPC 的评价单位转为工作流、精度、能耗和数据移动 | keynote 是方向性判断，不等于产品收入 |
| 展览 | 188 家展商；加速器、OEM、云、网络、存储、冷却、量子完整同场 | AI factory 已是多层系统市场，而非 GPU 单品市场 | 展位/赞助不证明订单；本报告未用展商身份推断收入 |
| Trillion Parameter AI Models workshop | 指出 frontier AI 与 HPC 现实在 scheduler、storage、networking、software 上存在错配 | HPC 中心若只采购 GPU，利用率可能受软件与数据栈限制 | 公开摘要，无完整录像和统一 benchmark |
| High-Performance Containers workshop | 公有云的性能/成本/主权与 HPC 的 AI 敏捷性形成张力，讨论 Kubernetes/container 混合 | 容器、批调度和安全域融合是系统利用率变量 | 属工程路线，商业份额未披露 |
| Sustainable Supercomputing / facility sessions | 液冷、热回收、能源优化、数据中心参访 | 机房设计进入计算架构讨论核心 | 个别场地经验不可直接外推所有气候区 |
| Quantum/HPC tutorials | CUDA-Q、QPU/GPU、模拟与混合调度 | 量子先成为异构加速器和科研服务 | 无普遍 practical advantage |
| RISC-V、Arm 与 heterogeneous hardware workshops | 开放 ISA、专用核、主权计算和软件移植 | CPU/控制面长期存在多元化机会 | 多数仍是生态建设，近期服务器收入有限 |
| Hans Meuer Award | 获奖工作关注 collective operations 的性能洞察 | collective、拓扑和观测工具成为大规模系统效率关键 | 学术成果到商业产品仍需转化 |
| Best Student Paper | 研究模拟光子处理器在规模化时的转换和损耗 | 光子计算不能只比较核心 MAC 能效，ADC/DAC、转换和数据搬运必须计入 | 研究模型不等于量产器件成本 |

相关公开材料来自 workshop 摘要、设施参访、存储议题、展商目录和完整演讲索引；由于 workshops/tutorials 没有统一公开视频，本报告只把它们用于确认议题和工程方向。[S47][S48][S49][S50][S51][S52]

**判断：** 本届会议最有价值的非产品信号是“系统边界外扩”：研究者不再只讨论 GPU kernel，而是把 scheduler、collective、container、数据准备、设施供电和结果精度纳入同一个性能问题。对产业链而言，真正的增量利润来自能解除系统瓶颈的产品，而不是名称中带有 AI/HPC 的所有展商。

## 反共识洞见

### 被过度乐观定价或叙述的方向

1. **“2026 年 CPO 已经全面普及。”**  
   事实只支持器件/平台制造爬坡和 2H 2026 可用，公开客户端口量、现场失效率、光引擎良率和维护成本仍缺失。CPO 是高概率方向，但收入曲线可能晚于发布节奏。  
   **证伪本报告谨慎判断：** 2026 Q4 前披露多个独立客户、十万级以上生产端口或可审计的系统收入，并有现场可靠性数据。

2. **“UALink 会在 2026 年快速取代 NVLink。”**  
   规范完成不等于硬件、collective library、故障恢复和客户资格认证完成；评估硬件预期在 2026 年末，商业部署跨 2026–2027。  
   **证伪：** 2027 H1 前至少两种非 NVIDIA 加速器、两家交换/互连供应商提供可采购的 UALink 系统，并获得规模客户验收。

3. **“CXL 是廉价 HBM。”**  
   CXL 提供容量和池化，延迟与带宽层级不同，软件还需 NUMA-aware 优化。用 CXL 扩展推理缓存合理，把它写成 GPU 本地 HBM 替代不合理。  
   **证伪：** 生产集群在同一模型和 SLA 下，用 CXL 远端内存大幅减少 HBM、同时 token/$ 和 token/W 不下降，并公开部署规模。

4. **“服务器收入增长会等比例转化为 OEM 利润。”**  
   Dell ISG 和 HPE Cloud & AI 的经营利润率约 10–12%，远低于稀缺硅和内存层；高价 GPU pass-through 会放大收入而未必扩大毛利率。  
   **证伪：** 连续两个季度 AI server revenue 高增，同时 OEM 经营利润率提升 300 bps 以上且营运资本没有恶化。

5. **“sovereign AI 等于本土硅替代。”**  
   欧洲新增项目大量采用 NVIDIA GPU、美国存储/软件或多国网络产品。主权采购当前更多是数据、治理、地点和运营主权。  
   **证伪：** 欧洲主要 AI factory 的加速器、scale-up、编译栈和关键存储有过半价值由欧洲本土供应商提供。

6. **“量子将在两年内替代一部分通用 AI/HPC 集群。”**  
   会议教程仍承认无普遍实用优势，当前价值来自混合接入和研究。  
   **证伪：** 出现独立复现、包含误差校正和数据 I/O 成本、在商业任务上优于最佳经典系统的结果，并转化为非科研付费利用率。

7. **“AI exaflops、HPL 与 token throughput 可以互相比较。”**  
   LineShine、El Capitan 的 HPL/HPL-MxP 差异已经说明精度和算法口径决定数量级。  
   **证伪：** 只有在同一数据、精度、SLA、功耗和软件版本下的端到端 benchmark 才能推翻本报告的不可比判断。

### 被低估的方向

1. **中压配电、开关设备、母线、CDU 与 heat rejection。** 单柜 300 kW 以上把这些设备从后台成本变成 GPU 上线的必要条件；订单周期通常长于服务器。
2. **内存系统软件与数据移动优化。** HBM 扩容不能自动解决 irregular access、通信和数据准备；NUMA、collective、cache 和调度能直接改变 GPU 利用率。
3. **Ethernet scale-out 的“系统工程”而非单一交换芯片。** 拥塞控制、NIC、可观测性、光学和布线共同决定训练尾延迟；这扩大 Broadcom、Marvell、Arista、Cisco 及光学供应链的机会，但也提高认证门槛。
4. **AI storage 的元数据、对象、缓存和软件价值。** IO500 显示带宽与 metadata 必须同时优化；推理上下文和多模态数据会让存储需求更持久，而非只在大模型训练初期出现。
5. **CPU、控制面和数据处理。** GPU 柜数量增长会增加编排、网络控制、数据预处理和大容量内存需求；CPU 的工作内容变化，不是简单消失。
6. **整套设施的服务和维护。** 300 kW 以上机柜的 quick disconnect、漏液检测、备件、现场服务和 SLA 是持续收入，而非一次性硬件销售。
7. **利用率软件。** 当单柜价格达到 $8–13M，提高 5 个百分点利用率的年价值可以高于许多单项硬件升级。

### 伪受益方向

| 伪受益叙事 | 为什么不成立 | 必须看到的验证材料 |
|---|---|---|
| 有通用水冷产品就受益于 AI 液冷 | AI 柜需要高热流密度、材料兼容、快速接头、漏液检测、CDU 控制和 OEM 认证 | hyperscaler/OEM design win、交付 MW、质保与现场运行记录 |
| 普通光器件自动受益 CPO/1.6T | CPO 要求光引擎封装、良率、测试、可维护性和客户资格；旧速率产能可能被淘汰 | 800G/1.6T/CPO 订单、端口量、ASP、良率与客户认证 |
| 宣称 CXL 即拥有内存池利润 | 控制器、switch、firmware、NUMA 软件、安全隔离缺一不可 | production SKU、客户服务器数、性能/TCO 和收入 |
| 任何服务器 OEM 都能赚取 GPU 高毛利 | GPU 价值多由上游获取，OEM 可能只获得集成和服务毛利 | 分部 gross/operating margin、现金转换和 backlog 质量 |
| 展出量子或光子原型即是近期收入 | 研究演示与生产良率、错误率、开发工具、客户工作流距离很大 | 付费合同、可复现 benchmark、生产数量和续费 |
| sovereign 标签即有本土供应链价值 | 采购可能仍采用 NVIDIA/AMD、美国软件和国际网络设备 | BOM 本地化比例、IP/软件控制权和长期服务收入 |

## 公司及产业链映射

### 股票研究映射

| 公司/生态 | 直接受益点 | 本届会议及会后证据 | 当前状态 | 利润池质量 | 关键催化剂 | 主要证伪项 |
|---|---|---|---|---|---|---|
| **NVIDIA** | GPU、Vera CPU、NVLink、IB/Ethernet、DPU、CPO、软件 | 欧洲 35 系统、Rubin 科学系统、Doudna/LANL/LRZ，Data Center $75.2B/季 | 器件量产爬坡+大量选型 | **最高**；公司 GM 约 75%，但受客户集中和 capex 影响 | Q4 Rubin 整机交付、CPO 端口、networking attach | OEM/客户验收延迟；custom XPU/AMD；毛利率下行 |
| **AMD** | EPYC、MI450/MI430X、Helios、ROCm、开放 scale-up | Meta 最多 6 GW、Oracle 50,000 MI450、TOP500 覆盖增加 | 大订单明确，主要产品待 2H 2026 放量 | 潜在高，但当前 DC 规模远小于 NVIDIA | 首 1 GW 和 Oracle Q3/H2 出货、ROCm 客户数据 | 时间表后移、系统良率/软件不足、客户仅保留选择权 |
| **Intel** | Xeon、CXL、Aurora、CPU/内存生态 | Aurora 仍为 TOP500 #4；截至截止日未检出与 Rubin/MI450 同等级的 ISC 2026 新平台订单公告 | 已安装基础强，会议增量催化有限 | CPU 稳定、加速器不确定 | Xeon/CXL 生产部署、代工与封装订单 | HPC 加速器份额继续下降；CXL 收入无法量化 |
| **Broadcom** | custom XPU、Tomahawk、Ethernet、CPO/NPO | Tomahawk 6 production volume；AI semiconductor $10.8B/季、下一季 $16B 预期 | 量产+高增长收入 | **高**；硅毛利好，但口径含 XPU+network | 800G/1.6T、更多 custom XPU 客户 | 客户集中、AI 口径无法拆分、Ethernet 集群延迟不达标 |
| **Marvell** | 800G/1.6T optics、51.2T Ethernet、NPO/CPO、custom XPU | 财报称相关 bookings 强；公司收入 $2.418B/季 | 产品/订单爬坡，规模小于 AVGO/NVDA | 中高，non-GAAP GM 58.9% | 1.6T 收入、custom silicon ramps | design win 延迟、客户集中、CPO 量产良率 |
| **Arista / Cisco** | Ethernet switch、routing、可观测性 | Ethernet 路线获得会议和真实部署验证；截至截止日未检出重大的 ISC 专属客户订单公告 | 行业方向受益，会议特定收入未确认 | 系统软件和服务可提高质量 | 800G AI cluster revenue、UEC production network | NVIDIA 全栈、白盒和 Broadcom 客户自研压缩份额/毛利 |
| **Dell** | AI rack integration、storage、services、DLC | XE8812、Doudna；AI server Q1 $16.1B、backlog $51.3B、FY guide $60B | backlog 强、Rubin 待交付 | 中等；ISG OP margin 10.5% | backlog conversion、storage attach、服务收入 | 低毛利 pass-through、验收延迟、营运资本上升 |
| **HPE** | Cray GX5000、Slingshot 400、storage、national labs | LANL 系统、ISC 产品栈；Cloud & AI $7.7B/季 | 科研系统地位强、路线明确 | 中等；Cloud & AI OP 12.4%，Network 21.6% | LANL 验收、Slingshot 400、storage attach | 大项目波动、低毛利服务器 mix |
| **Supermicro** | 快速整柜、DLC、DCBBS 模块 | 1,152-GPU/3.2-MW blueprint；缺少对应客户金额 | 工程准备度高，订单证据待补 | 中等且执行敏感 | 具体 Rubin 客户、交付和现金流 | blueprint 不转订单、供应链/质量/营运资本 |
| **Lenovo / Eviden(Bull) / Fujitsu** | sovereign HPC、DLC、Arm/定制 CPU、系统集成 | Bull 获 Mimer €30M 合同；Green500 前三为 Bull 系统；Lenovo 强调 Neptune；Fujitsu 保有 FugakuNEXT 路线 | Bull 客户证据最强，其余以平台/路线为主 | 项目型、中等或偏低 | 欧洲 AI factory 招标、FugakuNEXT 里程碑 | 项目延迟、依赖上游 GPU、利润率不随收入增长 |
| **Micron** | HBM4、server DRAM、245TB QLC SSD、Gen6 SSD | HBM4 HVM；DC 两分部 $25.293B/季 | 量产且价格周期极强 | **当前极高但周期性最大** | HBM4 供给、HBM4E 2027、长期合同 | 供给释放、客户库存、GM 从 84.6% 快速正常化 |
| **IBM / DDN / WEKA / VAST 等存储** | 并行文件系统、对象、GPU direct、AI data platform | IBM Storage Scale 6.0.1、Mimer storage、BlueField STX 生态 | 正式产品+早期新架构 | 软件占比高者更优 | GPU 利用率提升、AI storage revenue、STX 出货 | 只增加容量、缺少软件 attach；云原生替代 |
| **Vertiv / Eaton / nVent / Siemens 等** | 配电、UPS、母线、CDU、液冷、热管理 | 100 MW IT 参考架构、2 GW 液冷供应商口径、强订单/收入 | 量产且跨平台 | **较高且持续**；OP margin 约 15–26% | backlog 转收入、MW 交付、服务 | 并网/项目延期、客户自建、竞争压价 |
| **AWS / Google Cloud / Microsoft / Meta** | AI 需求、custom XPU、云服务、设施 | 合计 2026 capex 中点约 $705B；自研与商用加速器并行 | 买方与平台运营方 | 取决于云 AI 收入和利用率，不是 capex 本身 | AI revenue、推理需求、折旧回收 | capex 回报不足、价格战、能源/许可延误 |
| **Arm / RISC-V 生态** | 控制 CPU、定制 SoC、主权和低功耗 | workshops 和 Fujitsu/云自研路线提供长期信号 | 生态/路线期 | IP 模式可高毛利，服务器量仍小 | 生产级系统和软件兼容 | 缺少规模客户、软件迁移慢 |
| **量子硬件/软件公司** | QPU、控制、云访问、混合调度 | 教程与研究中心接入；无普遍实用优势 | 研究/早期商业 | 小且项目型 | 可复现 advantage、付费利用率 | 误差/成本、经典算法进步、科研预算变化 |

### 产业链价值迁移

**事实：** NVIDIA 最近季度 networking/compute 收入比约 24.5%；Dell/HPE 的服务器相关经营利润率远低于上游；Marvell 披露 800G/1.6T optics、Ethernet、NPO/CPO 和 custom XPU 的强 bookings，但未拆分产品收入；Vertiv/Eaton 电气和热管理业务保持约 20% 或更高的经营利润率区间。[S12][S19][S21][S29][S40][S41]

**观点：** 价值并非从 GPU 单向迁走，而是在 GPU 供给扩大后向“解除下一个瓶颈”的环节扩散。顺序更可能是 HBM/scale-up → 800G/1.6T scale-out → 配电和液冷 → 数据/存储软件 → 利用率和服务。没有资格认证、不能量化交付规模的二三级供应商，可能只有主题 beta，没有持续利润。

## 风险与后续跟踪

### 主要风险

1. **需求回报风险：** $690–720B Big Four capex 最终需由云 AI 收入、广告/商业化和成本节约回收；利用率不足会使 2027–2028 增速急降。
2. **客户验收风险：** 144-GPU 柜的电力、冷却、网络和软件任何一项失败，都可把芯片生产与客户上线拉开数月。
3. **供应与良率风险：** HBM4、先进封装、CPO 光引擎、800G/1.6T 光学和高压配电均可能限制系统数量。
4. **价格与毛利风险：** GPU/ASIC 竞争、HBM 供给释放和 OEM pass-through 会使收入增长与利润增长分离。
5. **电网与许可风险：** 并网、变压器、发电和用水/热排放许可可能成为最长前置期。
6. **软件生态风险：** ROCm、UALink、CXL 和异构调度若缺少稳定工具链，硬件规格不能转为有效利用率。
7. **技术口径风险：** 低精度峰值、厂商 AI exaflops、HPL 和实际业务 throughput 的混用会造成估值模型数量级错误。
8. **政策与集中度风险：** sovereign 采购、出口管制、能源政策和客户集中可能改变订单地点和可交付产品。
9. **会议信息不完整：** 部分 workshops/tutorials 没有公开视频；未公开内容不能被本报告验证。

### 可证伪结论与数据仪表盘

| 本报告结论 | 后续数据 | 时间窗口 | 支持阈值 | 证伪/预警条件 |
|---|---|---|---|---|
| Rubin 已由制造转向规模交付 | NVDA/OEM 收入、客户上线、Rubin 系统数 | 2026 Q3–Q4 | 至少多个独立客户按期上线，OEM 明确确认收入 | Q4 仍只有 blueprint/样机，客户时间表普遍后移 |
| AMD 成为可信第二来源 | Meta 首 1 GW、Oracle 50,000 MI450、ROCm 生产数据 | 2026 Q3–2027 H1 | 首批按期交付且有客户性能/稳定性数据 | 推迟至 2027 H2 或订单规模缩小 |
| Ethernet scale-out 份额提升 | 800G port shipments、UEC production clusters、NVDA/AVGO/MRVL 网络收入 | 每季 | 多厂商生产网络增加，网络收入快于 compute 或总体服务器 | 互通停留在 demo，客户继续集中采购 IB |
| CPO 是 2027 增量而非 2026 全面普及 | 客户端口量、良率、现场失效率、CPO revenue | 2026 Q4–2027 H1 | 至少两个独立客户披露规模生产部署 | 只有厂商样机/生产声明，无客户数量 |
| HBM 需求强但利润率会正常化 | Micron/SK hynix/Samsung 供给、ASP、库存、GM | 每季 | bit shipment 增长，GM 温和回落仍高于历史 | 库存上升、价格下跌、GM 快速跌破模型基准 |
| 液冷/供电是持续瓶颈 | VRT/ETN/NVT orders、backlog、book-to-bill、交付 MW | 每季 | 订单增长和交付同时保持，取消率低 | backlog 取消、交期快速缩短且价格下降 |
| CXL 先选择性放量 | production server count、客户数、延迟/TCO | 2026 Q4–2027 H2 | 推理/缓存/CPU 内存扩展有可审计规模 | 仍只有演示，软件和性能数据不公开 |
| AI storage 获取更多价值 | Dell/HPE/IBM/DDN/WEKA 等 AI storage revenue、GPU idle time | 2026 H2–2027 | storage attach 和软件增长高于传统存储 | 仅容量收入，软件 attach 和利用率不改善 |
| Big Four capex 仍增长但回报受审视 | 2027 capex 指引、AI/cloud revenue、折旧、FCF | 2026 Q4–2027 Q2 | 合计指引接近或高于基准 $810B，AI 收入同步增长 | 合计低于约 $700B，或 capex 增长而 AI 收入/FCF 明显恶化 |
| Green efficiency 要经整机验证 | 2026-11/2027-06 Green500、实际 PUE | 半年 | Rubin/MI450 系统提高整机 GFLOPS/W | 榜单和现场能效无改善，芯片宣传未传导 |
| 量子仍是长期期权 | peer-reviewed advantage、付费利用率、续约 | 未来 24 个月 | 独立复现且包含 I/O/纠错总成本 | 继续只有模拟和科研 demo；此时维持“期权”判断而非证伪 |

### 未来三个月的具体跟踪日历

1. **2026-07 至 2026-09：** NVIDIA Rubin/CPO 生产与 OEM qualification；AMD MI450/Helios 首批出货；Broadcom 下一季 $16B AI semiconductor 指引兑现。
2. **2026 Q3 财报季：** Dell $51.3B AI backlog 的转化率和 ISG margin；HPE Cloud & AI margin；Micron HBM4 收入、库存与毛利率；Vertiv/Eaton orders/backlog。
3. **2026 Q4：** Vera Rubin OEM 系统可用性、CXL Abaco production-ready、BlueField STX 合作平台、UALink evaluation hardware。
4. **2026-11 榜单：** TOP500 新治理后首个榜单、Green500 是否出现 Rubin/MI450、IO500 新提交；重点比较 HPL、HPCG、能效和 I/O，而非只看名次。
5. **持续跟踪：** 欧洲 35 套系统的实际安装、Mimer 交付、Doudna/LANL/LRZ 里程碑，以及 100 MW 级园区并网/许可。

## 最终判断

ISC High Performance 2026 的核心不是又一轮 GPU 发布，而是 AI factory 的工程现实全面进入 HPC：同一设施必须处理模拟、训练、推理、数据和异构加速，单柜功率跨过 300 kW 后，网络、内存、存储、配电、液冷和软件利用率共同决定收入能否兑现。

未来 3 个月最重要的是验证“生产”能否转为客户交付；未来 1 年最重要的是 Rubin/MI450、800G/CPO、HBM4 与液冷设施能否同步爬坡；未来 2 年最重要的是电力约束、开放 scale-up 和 AI capex 回报率。基准情景仍支持服务器、网络、内存和机电基础设施增长，但利润不会平均分配：稀缺硅、网络/内存 IP 和经过认证的设施能力优于单纯转售整机或追逐概念标签。

投资上应把 NVIDIA/AMD/Broadcom/Micron 的上游利润池、Dell/HPE/Supermicro 的交付与低毛利特征、Vertiv/Eaton/nVent 的设施瓶颈，以及 AI storage/软件的利用率改善分开建模。最需要回避的是把 CPO、CXL、量子、sovereign 或液冷关键词直接映射为收入，而不要求订单、客户验收、端口/MW 数、利润率和现金流证据。

## 来源清单

### 使用说明

- 所有网页最后检索日期均不晚于 2026-07-10；表内日期优先写材料发布日期或财报期。
- “一手验证”表示该来源是否能直接确认其对应事项。厂商可以一手确认自己的产品计划和财务数据，但不能独立验证自己的性能优势或市占宣传。
- “高”置信度用于会议事实、财报、客户合同和正式榜单；“中高”用于正式产品状态但仍待客户验收；“中”用于演讲摘要、工程预测和参考设计。
- 本报告未用专业媒体、参会者社交分享或匿名供应链信息支撑核心数字。若后续出现此类线索，必须另列发布日期、来源类型、置信度及一手材料验证状态。

| ID | 日期 | 来源类型 | 公开来源 | 用途 | 一手验证状态 / 置信度 |
|---|---|---|---|---|---|
| S01 | 2026-07-10 检索 | ISC 官方 | [ISC High Performance 2026 首页](https://isc-hpc.com/) | 会议日期、教程/主会/展览/workshop 安排、地点入口 | 会议组织方一手 / 高 |
| S02 | 2026-07-02 | ISC 官方会后复盘 | [ISC 2026 Concludes With Record 4,035 Attendees](https://isc-hpc.com/isc-2026-concludes-with-record-4035-attendees/) | 4,035 人、64 国、188 展商、兴趣排序、TOP500 治理变化 | 会议组织方一手 / 高 |
| S03 | 2026-06，07-10 检索 | ISC 官方议程 | [ISC 2026 Program](https://isc-hpc.com/program/) | 三场 keynote、奖项和主会议技术方向 | 会议组织方/讲者摘要 / 高（议程）、中高（观点） |
| S04 | 2026-06，07-10 检索 | ISC 官方总结 | [2026 Conference Highlights](https://isc-hpc.com/2026-conference-highlights/) | 模拟、AI、数据、能效和 workflow 的官方主题 | 会议组织方一手 / 高 |
| S05 | 2026 会前，07-10 检索 | ISC 官方 | [ISC 2026 Unveils Workshops](https://isc-hpc.com/isc-2026-unveils-workshops-for-advanced-computing-community/) | 24 个 workshops 及 AI/HPC、可持续、量子、RISC-V、Arm 议题 | 会议组织方一手 / 高 |
| S06 | 2025 | ISC 官方历史议程 | [ISC 2025 Program](https://2025.isc-hpc.com/program/) | 2025 convergence、extreme scaling 与 keynote 对照 | 会议组织方历史一手 / 高 |
| S07 | 2025-06 | ISC 官方历史复盘 | [ISC 2025 Concludes](https://2025.isc-hpc.com/isc-2025-concludes-as-most-successful-in-40-year-history/) | 3,585 人、195 展商、约 70 家 AI 展商 | 会议组织方历史一手 / 高 |
| S08 | 2026-06-22 | NVIDIA 正式公告 | [Europe Unveils a Record 35 New NVIDIA AI Supercomputers](https://nvidianews.nvidia.com/news/europe-unveils-a-record-35-new-nvidia-ai-supercomputers) | 欧洲 35 系统、23 国、BSC/IT4LIA/Blue Swan/Mimer 等配置 | 厂商可确认项目清单；90%份额为厂商口径 / 中高 |
| S09 | 2026-06-22 | NVIDIA 正式公告 | [Vera Rubin Delivers Supercomputers for Science](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-delivers-world-class-supercomputers-for-science) | 144 GPU/柜、AI/FP64 性能、LRZ、Doudna、LANL 路线 | 厂商一手产品/选型；性能待独立验收 / 中高 |
| S10 | 2026-06 | NVIDIA 官方博客 | [TOP500 and Green500 at ISC 2026](https://blogs.nvidia.com/blog/top500-green500-supercomputers-isc-2026/) | NVIDIA GPU/网络覆盖系统数量、Green500 解读 | 榜单归类可复核；份额解读为厂商口径 / 中高 |
| S11 | 2026-07-10 检索 | NVIDIA 产品页 | [NVIDIA Silicon Photonics Networking](https://www.nvidia.com/en-us/networking/products/silicon-photonics/) | Spectrum-X/Quantum-X CPO 容量、能效声明和可用性 | 产品计划一手；5×等性能为厂商口径 / 中 |
| S12 | 2026-05-20 | NVIDIA 财报 | [NVIDIA FY2027 Q1 Results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-First-Quarter-Fiscal-2027/default.aspx) | Data Center $75.2B、compute/networking 拆分、毛利率、指引 | 发行人财报一手 / 高 |
| S13 | 2026-06 | AMD 官方博客 | [AMD Powers 4 of 10 Most Powerful Supercomputers](https://www.amd.com/en/blogs/2026/amd-powers-4-of-10-most-powerful-supercomputers.html) | AMD TOP500 覆盖和 Alice Recoque 路线 | 榜单可复核；未来系统为厂商/客户计划 / 中高 |
| S14 | 2026-05-06 | AMD 官方博客 | [AMD Instinct MI430X GPU](https://www.amd.com/en/blogs/2026/amd-sets-new-bar-for-hpc-with-amd-instinct-mi430x-gpu.html) | MI430X >200 TF native FP64 工程预测及脚注 | 厂商工程预测，未量产实测 / 中 |
| S15 | 2026-02-24 | AMD/Meta 正式公告 | [AMD and Meta 6 GW Strategic Partnership](https://www.amd.com/en/newsroom/press-releases/2026-2-24-amd-and-meta-announce-expanded-strategic-partnersh.html) | 最多 6 GW、首 1 GW 计划 2H 2026、MI450/Helios | 双方正式承诺；尚待出货/验收 / 中高 |
| S16 | 2026，07-10 检索 | AMD/Oracle 正式公告 | [Oracle and AMD Expand Partnership](https://www.amd.com/en/newsroom/press-releases/oracle-and-amd-expand-partnership-to-help-customers-ach.html) | 50,000 MI450 公有 supercluster、Q3 2026 起始计划 | 双方计划一手；部署未完成 / 中高 |
| S17 | 2026 Q1 | AMD 财报 | [AMD Reports First Quarter 2026 Results](https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results) | Data Center $5.8B、公司收入和毛利率 | 发行人财报一手 / 高 |
| S18 | 2026-06，07-10 检索 | Dell 正式公告 | [Dell AI Factory Advances Supercomputing Infrastructure](https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2026~06~the-dell-ai-factory-with-nvidia-advances-supercomputing-class-infrastructure-powering-the-next-generation-of-hpc-and-ai.htm) | XE8812、144 GPU、>300 kW、100% DLC、Doudna | 厂商/项目一手；整机验收待验证 / 中高 |
| S19 | 2026-05 | Dell 财报与电话会 | [Dell FY2027 Q1 Results](https://investors.delltechnologies.com/news-releases/news-release-details/dell-technologies-delivers-first-quarter-fiscal-2027-financial)、[财报电话会材料](https://investors.delltechnologies.com/static-files/b63ffff9-b729-403b-a231-c6af05667759) | AI server revenue、$51.3B backlog、$60B 指引、ISG margin、storage | 发行人财报一手 / 高 |
| S20 | 2026-06，07-10 检索 | HPE 官方活动/产品页 | [HPE at ISC High Performance 2026](https://www.hpe.com/us/en/events/isc-hp.html) | Cray GX5000、XD700、Slingshot 400、K3000、DLC | 厂商产品路线一手；部署状态需客户验证 / 中高 |
| S21 | FY2026 Q2 | HPE 财报 | [HPE Quarterly Results](https://investors.hpe.com/?jumpid=va_ycdgibe2fh%2Ffinancials%2Fquarterly-results%2Fdefault.aspx) | Cloud & AI、server、storage、network 收入与分部利润率 | 发行人财报一手 / 高 |
| S22 | 2026-06 | Supermicro 正式公告 | [Supermicro Vera Rubin NVL4 DCBBS Blueprint](https://www.supermicro.com/de/pressreleases/supermicro-delivers-nvidia-vera-rubin-nvl4-end-end-dcbbs-blueprint-native-fp64) | 1,152 GPU、8 柜、3.2 MW、约 362 kW/柜 | 厂商工程蓝图；无对应客户金额 / 中 |
| S23 | 2026-04 | NAISS 客户公告 | [Bull to Deliver AI-Optimised Supercomputer for Mimer AI Factory](https://www.naiss.se/news/2026/04/bull-to-deliver-ai-optimised-supercomputer-for-mimer-ai-factory/) | €30M、400 GB200、IBM storage、Nokia 400G Ethernet、交付时间 | 部署方/合同一手 / 高 |
| S24 | 2026-06 | TOP500/HPCG 官方榜单 | [LineShine Debuts No.1](https://www.top500.org/news/lineshine-debuts-no-1-top500-enters-new-global-exascale-era/)、[HPCG June 2026](https://www.top500.org/lists/hpcg/2026/06/) | 前五、功耗、HPL/HPL-MxP、CPU-only、HPCG | 正式榜单 / 高 |
| S25 | 2026-06 | Green500 官方榜单 | [Green500 June 2026](https://www.top500.org/lists/green500/green500-june-2026/) | KAIROS/ROMEO/Levante 能效和排名 | 正式榜单 / 高 |
| S26 | ISC26 | IO500 官方榜单 | [ISC26 Production List](https://io500.org/)、[ISC26 Full List](https://io500.org/list/isc26/full) | 带宽、元数据、榜单分类和存储系统比较 | 正式社区榜单；提交配置差异需谨慎 / 中高 |
| S27 | 2026-03-12 | Broadcom 正式公告 | [Broadcom OFC 2026 Announcements (PDF)](https://investors.broadcom.com/node/64036/pdf) | Tomahawk 6 production volume、Tomahawk Ultra、Thor Ultra、CPO/NPO | 厂商产品状态一手；客户规模未完全披露 / 中高 |
| S28 | FY2026 Q2 | Broadcom 财报 | [Broadcom Q2 FY2026 Results](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial) | AI semiconductor $10.8B、下一季 $16B 预期 | 发行人财报一手；XPU/网络不可拆 / 高 |
| S29 | FY2027 Q1 | Marvell 财报 | [Marvell Q1 FY2027 Results](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-26-000014/q127_8kx522026ex-991.htm) | 收入、毛利率、800G/1.6T optics、Ethernet、NPO/CPO 和 custom XPU 订单线索 | 发行人财报一手；分产品收入未披露 / 高 |
| S30 | 2025-06 至 2026-01 | UEC 官方 | [UEC Specification 1.0](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/)、[Specification History](https://ultraethernet.org/specification-history/) | UEC 正式规范及版本节奏 | 联盟一手规范 / 高 |
| S31 | 2026，07-10 检索 | UALink Consortium | [UALink Specification](https://ualinkconsortium.org/specification/)、[UALink Roadmap](https://ualinkconsortium.org/blog/ualink-roadmap-insights-accelerating-open-scalable-ai-networking-1296/) | 200G/lane、1,024 accelerators、评估硬件和商业部署时间 | 联盟路线一手；产品仍待成员交付 / 中高 |
| S32 | 2025-11 至 2026 | CXL Consortium | [CXL Specification](https://computeexpresslink.org/cxl-specification/)、[CXL 4.0 Webinar Q&A](https://computeexpresslink.org/blog/introducing-the-cxl-4-0-specification-webinar-qa-recap-4386/) | 128 GT/s、port bundling、RAS、pooling 与 NUMA 限制 | 联盟规范一手 / 高（规格）、中高（应用） |
| S33 | 2026-06-24 | Micron 财报 | [Micron FY2026 Q3 Results](https://micron.gcs-web.com/news-releases/news-release-details/micron-technology-inc-reports-record-results-third-quarter) | HBM4 HVM、HBM4E、收入、分部收入、毛利率、SSD 路线 | 发行人财报一手 / 高 |
| S34 | 2026-06-10 | IBM 官方产品博客 | [IBM Storage Scale 6.0.1 Accelerates AI Outcomes](https://community.ibm.com/community/user/blogs/ulf-troppens/2026/06/10/ibm-storage-scale-601-accelerates-ai-outcomes) | GPU Direct、cuObject、多租户与正式版本 | 厂商产品发布一手；效果需客户验证 / 中高 |
| S35 | 2026-03-16 | NVIDIA 正式公告 | [BlueField-4 STX Storage Architecture](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption) | STX 参考架构、合作伙伴、2H 2026 计划及性能声明 | 厂商/伙伴路线一手；性能与收入未独立验证 / 中 |
| S36 | FY2026 Q3 call | Microsoft 投资者材料 | [Microsoft FY2026 Q3 Earnings](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3) | CY2026 capex 约 $190B、季度 capex 与资产寿命结构 | 买方财务一手 / 高 |
| S37 | 2026 Q1 / 2025 Q4 | Amazon 财报与官方说明 | [Amazon Q1 2026 Results](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-First-Quarter-Results/)、[Amazon Q4 Results and 2026 Capex](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx) | 约 $200B capex、2.1M AI chips、Trainium 和 NVIDIA 部署计划 | 买方财务/运营一手 / 高 |
| S38 | 2026-02 | Alphabet 投资者材料 | [Alphabet 2025 Q4 Earnings Call](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx) | 2026 capex $175–185B、服务器与设施支出框架 | 买方财务一手 / 高 |
| S39 | 2026 Q1 | Meta 财报 | [Meta Reports First Quarter 2026 Results](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/) | 2026 capex $125–145B | 买方财务一手 / 高 |
| S40 | 2026 Q1 | Vertiv 财报 | [Vertiv First Quarter 2026 Results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx) | 收入、增长、经营利润率和全年指引 | 发行人财报一手 / 高 |
| S41 | 2026 Q1 | Eaton 财报 | [Eaton First Quarter 2026 Results](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html) | Electrical 分部收入、利润率、订单与数据中心需求 | 发行人财报一手 / 高 |
| S42 | 2026-06-01 | nVent/Siemens 正式公告 | [Reference Architecture for NVIDIA AI Data Centers](https://investors.nvent.com/press-releases/press-release-details/2026/Siemens-and-partners-develop-reference--architecture-purpose-built-for-NVIDIA-AI-data-centers-/default.aspx) | 136 MW facility/100 MW IT、液冷和配电架构、2 GW 供应商口径 | 参考设计一手；累计部署为供应商自报 / 中高 |
| S43 | ISC 2026，07-10 检索 | ISC tutorial 摘要 | [Quantum Computing Tutorial](https://isc.app.swapcard.com/widget/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDM5MDIzMQ%3D%3D) | practical quantum advantage 尚未普遍实现、混合工作流 | 讲者/会议摘要；无量产证明 / 中 |
| S44 | ISC 2026，07-10 检索 | ISC presentation 摘要 | [Mixed Precision and the Memory Wall](https://isc.app.swapcard.com/widget/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDQ0MzYwNg%3D%3D) | 混合精度、内存带宽与 latency-bound 限制 | 讲者摘要；研究结论待完整材料 / 中 |
| S45 | ISC 2026，07-10 检索 | ISC presentation 摘要 | [CXL Disaggregated Memory: Crete 2.0 and Abaco 3.0](https://isc.app.swapcard.com/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDQ1MDAwMA%3D%3D) | 数十/数百 TB、推理/向量/图场景、Q4 production-ready 路线 | 讲者/厂商路线；无客户规模 / 中 |
| S46 | 2026-06 | NVIDIA 官方博客 | [JUPITER Exascale Supercomputing](https://blogs.nvidia.com/blog/jupiter-exascale-supercomputing-science/) | 20,480 GH200、科学应用和量子模拟案例 | 系统配置可与榜单核对；应用效果为厂商/中心案例 / 中高 |
| S47 | ISC 2026，07-10 检索 | ISC workshop 摘要 | [Trillion Parameter AI Models and HPC](https://isc.app.swapcard.com/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDM5NTcwMA%3D%3D) | scheduler、storage、networking、software 与 frontier AI 错配 | 会议/讲者摘要 / 中 |
| S48 | ISC 2026，07-10 检索 | ISC workshop 摘要 | [High-Performance Containers Workshop](https://isc.app.swapcard.com/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDM5MDE3Mw%3D%3D) | cloud 与 HPC 的性能、成本、主权、Kubernetes/container 融合 | 会议/讲者摘要 / 中 |
| S49 | ISC 2026，07-10 检索 | ISC facility session | [Liquid Cooling and Heat Reuse Facility Tour](https://isc.app.swapcard.com/widget/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDQ3NDU0Ng%3D%3D) | 液冷、热回收和设施工程议题 | 会议/场地一手议程；不代表全行业部署 / 中 |
| S50 | ISC 2026，07-10 检索 | ISC presentation 摘要 | [Memory-Centric Storage Project](https://isc.app.swapcard.com/widget/event/isc-high-performance-2026/planning/UGxhbm5pbmdfNDQwOTk1NQ%3D%3D) | 内存中心、近数据处理和存储研究方向 | 讲者摘要；商业状态未验证 / 中 |
| S51 | ISC 2026，07-10 检索 | ISC 官方展商目录 | [ISC 2026 Exhibitors](https://isc.app.swapcard.com/event/isc-high-performance-2026/exhibitors/RXZlbnRWaWV3XzEyMDQ5NTI%3D) | 188 家展商及加速器、云、网络、存储、冷却生态覆盖 | 官方目录可确认参展，不确认订单 / 高（身份）、低（商业推断） |
| S52 | ISC 2026，07-10 检索 | ISC 官方演讲索引 | [ISC 2026 Presentation Index](https://isc.app.swapcard.com/event/isc-high-performance-2026/plannings/RXZlbnRWaWV3XzEyMDQ5NDk%3D) | AI factories、cooling、memory、network、storage、sovereignty、quantum 议题覆盖 | 官方议程索引 / 高（议题）、中（技术结论） |
