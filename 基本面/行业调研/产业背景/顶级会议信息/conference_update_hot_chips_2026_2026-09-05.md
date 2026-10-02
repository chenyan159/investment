# Hot Chips 2026 会议追踪：核心发现、技术路径与采用条件

- **会议日期**：2026-08-23 至 2026-08-25；美国加利福尼亚州 Stanford University，Memorial Auditorium；现场及线上混合形式。8 月 23 日为教程，8 月 24–25 日为主会议。
- **材料检索截止日期**：2026-09-05，America/Los_Angeles（PDT，UTC−7）。本报告只使用本次执行时已经公开且能够检索到的材料，不代表覆盖该日尚未发生时段的发布。
- **报告完成日期**：2026-09-05，America/Los_Angeles。
- **研究定位**：会议驱动的阶段性上游研究底稿；不构成公司评级、股价判断或交易建议。
- **独立性**：未读取或继承项目内旧报告、行业/公司索引、缓存及中间结论。仅读取目标路径适用的目录管理说明；研究证据来自外部公开来源。
- **证据标记**：**事实**为可核验的披露或观察；“厂商实测”仍是厂商口径，区别于独立复测；**估算**列明输入和算法；**判断**列明机制、条件和反证。“未取得/未找到”仅描述本次检索结果，不证明资料或订单不存在。

## 结论摘要

1. **会议的实质变化是推理基础设施的分工细化，不能概括成单一芯片算力升级。** Google 将第八代 TPU 分成训练与服务两型；NVIDIA 将 Rubin 与 LPU 协同；SambaNova 展示 GPU 负责 prefill、RDU 负责 decode 的组合；OpenAI 则以单一加速器和互联域覆盖不同推理阶段。几条路线对“如何减少等待和数据搬运”给出不同答案，尚不能宣布一种架构全面胜出。[Google 技术说明][S08]、[NVIDIA 会期发布][S05]、[SambaNova 会后技术说明][S17]、[OpenAI 实测披露][S13]

2. **定制 ASIC 已有生产采用证据，但必须逐代确认。** Meta 的 MTIA 300 有生产推荐模型数据，Microsoft 已披露 Maia 200 在 Azure 部署；这些证据不能自动升级为 MTIA 400/450/500 全面量产，也不能证明 Jalapeño 已规模上线。OpenAI 8 月 25 日仍明确列出生产资格验证、软件成熟和更多模型验证，目标为 2026 年底开始部署。[Meta 生产数据][S11]、[Maia 部署公告][S15]、[Jalapeño 状态][S13]

3. **HBM4 的收入兑现与后续新内存的研发进展处于不同阶段。** Micron 6 月已披露 HBM4 高量交付；d-Matrix 的 3D DRAM 有测试芯片验证；Samsung zHBM 为概念模型；HBF 已有首版规范披露，但本次未取得大规模客户验收证据。不能把这些阶段串成统一的“下一代内存即将放量”。[Micron 财报][S33]、[d-Matrix 测试芯片][S20]、[Samsung 3D 路线][S21]、[HBF 规范披露][S23]

4. **性能数字最需要审计的不是倍数大小，而是分母。** Jalapeño 的每千瓦性能按芯片额定功率归一化；AMD 的部分每美元性能使用预测价格；XCENA 的能效扣除系统空闲功率；Cerebras 的片上总带宽与整机架互联带宽也不是同一统计边界。它们各自具有解释力，但不能直接组成投资收益排行榜。[OpenAI 方法][S13]、[AMD 脚注][S07]、[XCENA 方法][S24]、[Cerebras 技术说明][S16]

5. **CPU 的机会来自工作负载和软件生态，不能用核心数代替有效 agent 吞吐。** Vera、Arm AGI、Diamond Rapids 强调内存和 I/O；IBM 将 Arm 原生应用引入未来 Z/LinuxONE 是软件可用性变化。SiFive 的 CUDA 主机演示说明 RISC-V 进入开发验证阶段，也意味着其可以与 NVIDIA GPU 配合，并不等于替代 GPU。[Arm 会后总结][S27]、[Intel 会期披露][S19]、[IBM 公告][S28]、[SiFive 开发平台][S26]

6. **网络和封装不是所有供应商都同等受益。** 片内/封装内 NIC、集合通信卸载、多平面网络及模块化机架，可能增加系统设计和验证价值，却减少某些外置器件或交换层级的用量。需按拓扑、BOM 和每台设备的实际暴露核算，而不是把“更多 AI”映射为全部网络、散热、测试公司同步扩张。[Meta 通信架构][S11]、[Broadcom 多路径方案][S25]、[Cerebras 机架设计][S16]

7. **当前不能据此声称 GPU 盈利已被 ASIC 侵蚀。** NVIDIA 会后财报仍显示强劲的数据中心收入和集团毛利率；定制芯片也继续消耗代工、封装、HBM、互联和软件资源。较可信的判断是价值分配更依赖平台与客户之间的议价和工作负载归属，而非会议演讲数量。[NVIDIA FY2027 Q2][S32]

8. **材料覆盖存在明确边界。** 官方议程、部分公司会后说明和独立访谈已公开；抽查的大会 PDF 与全套 proceedings 返回 HTTP 401、认证域为 Attendees Only。不能把索引页出现 PDF 链接当作已经读过演讲全文。完整回放和幻灯片公开时间按官方 FAQ 暂预计为 2026 年 12 月初。[官方议程][S01]、[官方 FAQ][S02]

## 会议核验、材料覆盖与研究边界

### 日期、议程与实际发生是三种不同证据

会议官网已经标示本届结束；官方征稿页给出 2026-08-23 至 08-25 的日期。单独的议程只能证明被安排，不能证明每一项实际按原计划发生。对 NVIDIA、Intel、OpenAI、Cerebras、SambaNova、BOS、XCENA，已取得与会期对应的公司发布或会后说明；IBM 另有现场采访文字稿。其余仅有议程的项目保持较低结论等级。[会议官网][S01]、[日期和投稿安排][S03]

本届检索到的主题演讲为 Waymo 的自动驾驶计算议题。本报告取得其 8 月 20 日配套技术文章，未取得 keynote 全部录音或逐字稿；不将配套文章说成主旨演讲的完整内容。

### 实际覆盖清单

| 材料类别 | 本次取得的公开资料 | 可以支持什么 | 缺口与处理 |
|---|---|---|---|
| 官网、日期、议程 | 2026 官网、FAQ、征稿页；2025 官方归档 | 会期、安排、跨届主题对照 | 不凭议程推断出货 |
| 完整演讲幻灯片 | 识别官方 PDF 链接；未取得受限正文 | 文件入口存在 | 抽查 SK hynix、Samsung PIM、Fujitsu PDF 均为 401；不引用未读页码 |
| 全套 proceedings | 官方页面提供约 160 MB ZIP 入口 | 大会提供成套资料 | ZIP HEAD 请求同为 401，未下载或解包 |
| 公开视频 | NVIDIA 会期文章含短视频；IBM 独立采访含视频入口及可读文字稿；Meta 配套博客含视频入口 | 厂商发布和采访核验 | 未观看完整大会回放；嵌入视频存在不等于已看过内容 |
| 论文/技术报告 | CN101 arXiv 摘要；Meta MTIA/HCCL 论文入口；多家公司技术博客 | 原型路线、方法和可复核入口 | 只对实际取得内容作结论，不视所有大会演讲为同行评审论文 |
| 赞助和展示材料 | 官网 HTML 中的赞助商图片标识；Chroma 活动页；BOS、XCENA 会期材料 | 公司参与、产品展示位置 | 赞助不是客户订单，也不是独立技术背书 |
| 产品发布 | Intel、NVIDIA、OpenAI 会期披露；AMD、Google、Samsung 等会前公告 | 首次发布与会期技术展开的区别 | 不将 1 月、4 月、7 月发布重记为 8 月新产品 |
| 投资者资料 | NVIDIA 8 月财报、Micron 6 月财报和 prepared remarks、AMD 7 月公告 | 已实现收入、合同和未来部署指引 | 财报总额不能分摊给单一演讲产品 |
| 客户采用 | Meta 自用生产数据、Microsoft 自用部署；Nebius 官网采用表述 | 自用与客户侧确认 | 已宣布采用未必是规模交付或可公开购买 |
| 非官方分享 | Chips and Cheese 采访；STH 会场记录；Andrew Sloss 帖文；Reddit 讨论 | 交叉验证、分歧和下一步检索线索 | 未取得来源可靠的量化供应链访谈、券商完整会后报告 |
| 采购、验收、价格、交期 | Micron 合同披露；部分厂商部署计划 | 供需约束存在及阶段差异 | 未得到各新产品统一口径的成交价、客户验收单、良率和交期数据库 |

**访问检查记录，2026-09-05 PDT：** 对官方链接直接进行未登录 HEAD 检查，SK hynix 包装教程、Samsung LPDDR5X-PIM、Fujitsu MONAKA 三个 PDF 及全套 ZIP 均返回 401。该结果和 FAQ 相互印证；没有尝试绕过认证。涉及这些演讲的细节，若只有媒体转述，本文将其列为“待核线索”。

官方赞助标识可识别 NVIDIA、AMD、Intel、Samsung、Google Cloud、Marvell、Advantest、Murata、Chroma、Normal Computing、XCENA、Etched、XSight 等。**这是一份参与线索，不是完整展商产品认证表。** Chroma 自有活动页也能交叉确认参与，但没有由此取得特定 AI 芯片测试订单或收入拆分。[官网][S01]、[Chroma 活动页][S40]

## 会议重点和方向变化

### 从 2025 到 2026：哪些变化可以确认

2025 官方议程已经包含机架、电力、液冷、AI kernel 编程、光学 I/O、MI350、Ironwood 和存内计算。因此，“系统协同”“内存瓶颈”“AI 编程”并非 2026 年突然出现。2026 的增量更接近产品代际细节、不同计算阶段的分型，以及一部分方案从路线图走向可测硬件或部署。[2025 官方归档][S04]

| 主题 | 过去 6–12 个月的可核验基线 | 本届/会后新增的认识 | 变化性质与置信度 |
|---|---|---|---|
| 推理架构分型 | Google 4 月已发布 TPU 双路线；SambaNova 2 月已发布 SN50 | 多家公司围绕 decode、通信和低时延重新设计系统 | 架构细分；高。不能仅凭会期判定需求突然加速 |
| GPU 到机架竞争 | 2025 已有 NVL72 教程；AMD 7 月已推出 Helios | 评价边界扩到完整机架、内存、网络与软件 | 系统竞争加深；高 |
| 自研 ASIC | Meta 3 月披露多代路线；OpenAI 6 月公开工程样片 | OpenAI 增加公开模型实测，Meta 增加生产通信数据 | 验证证据增强；高。各代量产程度不同 |
| 内存路线 | HBM4 已有交付；3D DRAM、HBF、zHBM 均有会前公开信息 | 会期将性能、容量、封装热约束与软件采用放到同一框架 | 多路线分层；高。具体新制程时间仍不确定 |
| 网络 | Thor Ultra 于 2025-10 已发布；2025 会议已有 AI NIC 与交换芯片 | 多路径、通信卸载、多平面和系统故障恢复受到强调 | 架构优化；高。不能把 800G 重记为本届首发 |
| CPU 和软件兼容 | Arm 服务器生态已经存在，RISC-V 去年有 RVA23 IP 演讲 | IBM 双 ISA 设计；SiFive 提供可用开发服务器 | 软件平台边界扩展；高。商业规模中低 |
| 物理 AI | 自动驾驶已有自用计算系统 | Waymo 公开定制前端处理机制；BOS 明确 chiplet 扩展方向 | 垂直工作负载定制；中高。外售空间未知 |
| 光计算、热力学与边缘研究 | 2025 已有独立 Optical session 和多种学术海报 | CN101 等继续验证不同计算原语 | 研究进展；中。议程份额减少不代表行业衰退 |

**“市场共识”边界：** 上表比较的是公开路线和披露状态，不是投资者仓位或价格隐含预期。本次没有取得足够统一的卖方预测、估值分解和机构调查，因而不宣称这些变化已经“超预期”或“尚未定价”。

## 产品和技术路线

### 1. NVIDIA Rubin 与 AMD MI455X：比较先统一精度和整机边界

| 项目 | NVIDIA Rubin | AMD MI455X |
|---|---|---|
| 公开规格来源与日期 | 2026-07-21 技术文章 | 产品页标注发布日 2026-07-23；2026-09-05 检索 |
| 显存容量、带宽 | 288 GB HBM4；最高 22 TB/s | 432 GB HBM4；最高 23.3 TB/s |
| 低精度峰值 | 最高 50 PFLOPS NVFP4 | 40.3 PFLOPS OCP MXFP4 |
| 互联公开值 | NVLink 6，3,600 GB/s | UALoE scale-up 双向 3.6 TB/s |
| 商业状态证据 | 8 月 26 日公司称 Vera Rubin 已全面生产 | 7 月公告称 Helios 已生产；客户上线仍有时间差 |
| 采用门槛 | 软件、机架供电、液冷、网络、客户容量 | ROCm 模型效率、整机验收、液冷、HBM 与网络供应 |

数字来自 [Rubin 技术说明][S06]、[MI455X 规格页][S09]、[NVIDIA 财报][S32]、[AMD 公告][S07]。这里不对 NVFP4 与 MXFP4 峰值进行横向排名；精度、稀疏性、缩放规则、算子覆盖和模型质量须先一致。

**事实与估算分开：** 72 颗 MI455X 的显存按规格相加为 31,104 GB，约 31.1 TB（十进制），带宽相加为 1,677.6 TB/s，约 1.68 PB/s。这是理想规格加总，不是一个请求可获得的远端内存带宽，也不是实测吞吐。MI455X 相对上述 Rubin 单卡规格容量高 50%，带宽高约 5.9%；容量优势不能直接转换为吞吐优势。

**采用条件。** 更大显存可能减少模型切分或容纳更多 KV cache，但若数据已驻留且计算/通信成为瓶颈，容量增量未必带来同比收益。采购应核验同一模型、精度、上下文、并发和尾时延下的有效吞吐；还需计入节点失效率、维护时间、可用配额和软件持续优化成本。

**会前与会期区别。** AMD 7 月公告已把 OpenAI 的 Helios 上线目标写为 2026 年第四季度、2027 年加速部署；Meta 当时仍在测试验证。公告中的“生产”与“客户生产业务运行”可以同时处于不同阶段。本届技术演讲不能消除这一时间差。[AMD 部署披露][S07]

### 2. NVIDIA Groq 3 LPX：低时延解码成为平台内的专业分工

**事实，2026-08-24：** NVIDIA 宣布 Groq 3 LPX 全面生产，采用 Rubin 与 LPU 协作。其公开数字为 Gemma 4 31B、100,000-token 长上下文场景下输出 3,400 token/s，并称约为被比较平台的 4 倍；机架配置可含 256 个 LP30。该页面还披露 Nebius 采用和 CoreWeave 多平面网络生产部署。[NVIDIA 会期发布][S05]

**证据等级。** 这是供应商披露，不能直接称为本报告独立复测。Nebius 官网可确认采用 LPX 的表述，但没有取得同一服务的完整价格表、可用地域、保障容量和交付量，因此提升的是客户采用可信度，不是收入可估算程度。[Nebius 客户侧材料][S31]

**判断。** 专用解码并不天然流向独立小芯片公司；成熟 GPU 平台也能吸收这一模块，继续捕获网络、软件和整机价值。独立解码方案需要证明在不同模型、输入/输出比例、并发和低负载时仍能覆盖额外硬件及调度成本。长上下文单用户速度尤其不能直接替代多租户总吞吐。

### 3. OpenAI Jalapeño：可测芯片成立，年底部署仍是下一道门槛

**事实。** 6 月公开材料确认工程样片在实验室运行，并点名 Broadcom 与 Celestica 的实现、网络和系统角色。8 月 25 日新增 InferenceX 实测，测试覆盖 GPT-OSS 120B、DeepSeek R1、Kimi K2.5；按各加速器额定芯片功率归一化，峰值每瓦性能提高约 1.5–1.9 倍。Jalapeño 额定 700 W，厂商称被测负载持续功率不超过 550 W。[6 月工程样片][S12]、[8 月实测及方法][S13]

具体可比性边界：公开附录标注 nominal 8k/1k，DeepSeek/Kimi 使用 MXFP4；比较对象随模型为 GB200 或 GB300。额定芯片功率归一化不等于墙端电表实测；prefill 与 decode 混合吞吐、单用户速度和最小 TBT 也不能混成同一个收益倍数。模型精度、请求分布、系统数量和整机成本仍需复核。

**状态与时间。** 公司目标是 2026 年底开始在自有基础设施部署，8 月披露时仍进行生产资格验证和软件成熟工作。因此本报告评为“工程硬件实测/部署准备”，不写成规模收入兑现。[Jalapeño 状态][S13]

**竞争性解释。** 将模型状态和 KV cache 保持局部、通过统一互联覆盖不同阶段，有机会减少异构拆分带来的跨池迁移。这和 GPU+专用解码是两条竞争路线。若下一代模型所需算子迅速变化，或维护自研编译器的成本过高，架构收益可能被吞噬。Broadcom/Celestica 的明确角色支持产业链映射，但未公开每芯片价值量、合同毛利和分代采购额。

### 4. Google TPU 8t/8i：同一体系内的训练与服务分型

**事实，2026-04-22 的会前基线：**

| 参数 | TPU 8t | TPU 8i |
|---|---:|---:|
| 主要优化任务 | 大规模训练 | 采样、服务、推理 |
| HBM | 216 GB | 288 GB |
| HBM 带宽 | 6,528 GB/s | 8,601 GB/s |
| 片上 SRAM | 128 MB | 384 MB |
| FP4 峰值 | 12.6 PFLOPS | 10.1 PFLOPS |
| 拓扑 | 3D torus，最高 9,600 芯片 superpod | Boardfly，最高 1,152 芯片 |
| 差异化模块 | SparseCore 等 | Collectives Acceleration Engine |

来源为 [Google 架构技术文章][S08]。拓扑规模是设计能力，不是已验收集群数量。

**判断。** 8i 的低精度峰值低于 8t，但更高的内存配置和针对通信的设计可更适合特定服务任务。这直接说明峰值 FLOPS 排名不适合作为商业价值排名。片上 SRAM 只能保存有限工作集，不能把宣传中的“KV cache 留在片上”理解为任意上下文、任意并发的全部 KV cache 都可容纳。

4 月发布时 Google 写的是将很快向云客户提供。本次没有取得足以确认截至 9 月 5 日各地域、配额和 SKU 全面可用的完整证据，因此不从大会报告自动升级为全面 GA。旧一代 TPU 的客户案例也不移植到 8t/8i。[Google 发布范围][S10]

### 5. Meta MTIA 与 Microsoft Maia：自用价值需要拆分“模型、芯片代际、部署状态”

**Meta。** 3 月路线披露称过去代际已有数十万颗生产部署，MTIA 300 用于推荐训练；MTIA 400 实验室测试完成、迈向数据中心；450 计划 2027 年初规模部署、500 计划 2027 年。既有累计部署不是 400 的出货量。[Meta 分代路线][S14]

8 月 24 日披露提供了较强的使用证据：150B 参数的生产推荐模型，40 个 MTIA 300 的通信总时间相对其比较 GPU 集群约快 3.9 倍；**该数字是通信时间，不是端到端训练速度。** 其片内网络与专用消息引擎解释了优势机制，但未充分公开所有 GPU 配置，仍是厂商生产数据。[Meta 生产通信说明][S11]

**Microsoft。** Maia 200 使用 216 GB HBM3e、7 TB/s 带宽、272 MB SRAM；公开技术架构含双向 2.8 TB/s 互联、最高 6,144 加速器的两层以太网设计。Microsoft 1 月已称 US Central 部署，其他区域后续扩展；技术规格不是 8 月才首次发布。[Maia 技术说明][S18]、[Maia 部署公告][S15]

**采用与价值。** 两者首先服务内部流量、模型和云平台经济性；客户侧节省的采购溢价未必表现为可独立售卖的芯片收入。软件适配、模型迭代、集群利用率和可靠性决定节省能否落地。Meta 继续采购第三方 GPU、Microsoft 继续经营异构云，并不与自研采用矛盾。

### 6. Cerebras、SambaNova：低时延价值与容量、利用率的交换

**Cerebras，2026-08-25。** 公司说明 CS-4 采用 Nexus 机架平台，可容纳三个 WSE 模块，并把电源、冷却、I/O 模块化；CS-5 为 2027 年目标，CS-6 指向晶圆级计算与 3D DRAM。后两代的速度和体积改善应归为路线目标。本报告不把片上总带宽相对 GPU 机架互联的“倍数”解释为整模型加速倍数。[Cerebras 会期架构说明][S16]

价值机制是降低片间通信并提高现场更换、供电和冷却可维护性。相反约束是模型切分、片上容量、跨晶圆通信、器件良率和客户设施集成。没有取得 CS-4 分型号确认收入，不以技术文章的产品化表述估算收入规模。

**SambaNova。** 9 月 2 日公司会后文章把证据分成三层：SN50 的 432 MB SRAM；8/16/32 芯片 GEMM 的硅上测量；64→256 RDU 的 DeepSeek-R1 速度与带宽利用率建模。最后一项明确是建模，不是生产测量。[SambaNova 会后文章][S17]

7 月演示采用 4 个 H200 做 prefill、16 个 SN50 做 decode。必须计入这两类硬件，不能把结果列为“单独 SN50 击败 GPU”。2 月原始发布的交付目标为 2026 年下半年；当前演示与建模不提供广泛客户验收证明。[SN50 演示配置][S30]、[原始交付计划][S29]

**可证伪判断。** 异构拆分成立的前提是阶段间迁移、排队和负载不均成本小于专业化收益。若短输出、低并发或频繁模型切换使专用池闲置，即使每用户解码快，也可能损失每美元服务容量。

### 7. HBM、3D DRAM、zHBM、PIM、HBF、CXL：不同路线不能放在一个成熟度刻度上

| 路线 | 已取得的一手证据及日期 | 当前可确认成熟度 | 核心采用障碍 |
|---|---|---|---|
| HBM4 | Micron 2026-06-24 称高量交付；HBM4 收入累计已超 10 亿美元 | 有商业交付 | 逐客户认证、先进封装、良率和实际可分配产能 |
| SK hynix iHBM | 2026-05-26 宣布将冷却结构嵌入封装，称热阻降低 30%，沿用 MR-MUF | 热管理方案发布 | 特定客户产品验证、热循环可靠性、制造成本 |
| d-Matrix 3DIMC | 2026-03-16 称 Pavehawk 测试芯片跨电压/温度验证，最差测试约 0.4 pJ/bit | 测试芯片验证 | 容量扩展、良率、量产整合、系统级效率 |
| Samsung zHBM | 2026-08-04 展示概念模型；内存垂直置于计算之上 | 概念/路线 | 热耦合、键合、测试维修、供电、客户协同 |
| Samsung LPDDR5X-PIM | 8 月 FMS 公司材料确认产品展示；大会安排专门报告 | 公开产品展示；具体客户量产未证实 | AP/内存控制器、编程、算子支持、热和功耗 |
| HBF | 2026-08-04 SK hynix/Sandisk 宣布首版规范，经 OCP 披露 | 规范和生态建设 | 闪存访问/耐久特性、数据放置、预取、软件、主机接口 |
| XCENA MX1 | 2026-08-25 厂商测量及软件说明 | 样品/实测；年底量产、2027 初始收入为目标 | CXL 平台、工具链、数据局部性和客户集成 |

来源：[Micron 收入与产品状态][S34]、[iHBM][S22]、[3DIMC][S20]、[Samsung 路线][S21]、[HBF][S23]、[MX1][S24]。

**重要口径：** 0.4 pJ/bit 是测试芯片数据传输指标，不能替代整机焦耳/token；热阻下降 30% 不等于整机电耗下降 30%；zHBM 宣传参数是不同参考系统下的目标，不能与 HBM4E、iHBM 百分比排序。

关于 SK hynix 将 hybrid bonding 推迟到 HBM5、16 层资格验证及 EMIB 合作程度，本次主要找到媒体会场报道，受限原始幻灯片未取得。**这些属于待核路线线索，不足以据此上调/下调某家键合设备公司的订单。** 多家媒体转载同一场演讲也不构成多个独立证据。[相关会场报道，待核][S43]

#### HBF 的商业边界

公开厂商规范给出最高 512 GB、约 0.4–3.0 TB/s 的分级带宽，使用 UCIe。它提供的是介于热内存和持久存储之间的候选层级。本文取得的是厂商对规范的披露，未逐条审核 OCP 原始规范与互操作测试，不能称为完成所有生态认证。[HBF 公司披露][S23]

**判断：** 有望先从容量大、读占比高、访问可预测的工作集切入。对频繁写入、严格尾时延或高并发热数据，必须证明访问放大、预取和缓存命中没有抵消容量成本优势。这是根据存储分层机制的条件推演；不能由“同样成本容量更大”的宣传直接推导 HBM 被替代。

#### XCENA：比较基准改变，性能倍数也改变

MX1 将最高 2 TB DDR5、SSD 支撑容量及 1,000 多个 RISC-V 核放进一个 CXL Type 3 架构。六类数据处理 kernel 的“最高 4.7 倍吞吐、18.7 倍能效”以主机跨 CXL 处理为基线；改为主机本地 DDR5，分别为最高 2.0 倍和 6.2 倍。能效分母是超过系统空闲值的活动功耗。[XCENA 发布及脚注][S24]

因此不能把它描述为 LLM 全模型推理加速 18.7 倍。下一步应测试 FAISS/RAG 检索、数据库算子或特定 KV 工作集的完整路径，包括复制、页缓存、召回质量及远端访问。公司说年底量产、2027 年首批客户收入，意味着其潜在价值目前仍需跨过商业转化环节。

### 8. CPU：主机编排、内存与兼容性决定实际位置

| 路线 | 关键事实 | 对客户的意义 | 不可越过的证据边界 |
|---|---|---|---|
| NVIDIA Vera | 2026-03-16：88 Olympus 核、176 线程、最高 1.2 TB/s 内存带宽 | 高并发主机、代码执行、预处理和加速器供数 | 不从线程数推导 agent 实测容量 |
| Arm AGI | 2026-09-02：最高 136 Neoverse V3 核、12 DDR5 通道、PCIe Gen6/CXL 3.0、300 W TDP | 在核心密度、内存和功耗间选择 | Arm 的行业覆盖叙述是利益相关方观点 |
| Intel Diamond Rapids | 2026-08-24：最高 256 核、16 通道 12,800 MT/s、128 PCIe Gen6 lanes；18A-P、Foveros Direct | 高带宽主机和通用服务器路线 | 本次未取得量产验收和公开可购配置 |
| IBM 双 ISA Z/LinuxONE | 2026-08-24 发布未来支持 IBM 与 Arm 原生软件的设计 | 将更多软件靠近现有关键数据与业务 | “未来处理器”不是当前安装量或新增授权收入 |
| FUJITSU-MONAKA | 2026 议程和 Arm 会后文确认该 Arm CPU 方向 | 绿色数据中心及系统市场候选 | 原始报告受限；不补写现场性能和新客户订单 |
| SiFive BigSky | 2026-08-24：32 个 2 GHz P870-D，256 GB DDR5；有限量可用 | RISC-V 软件移植和 NVIDIA GPU 主机验证 | 开发服务器不是已形成大规模云采购 |

来源：[Vera 技术说明][S35]、[Arm 会后材料][S27]、[Intel 公告][S19]、[IBM 公告][S28]、[SiFive 公告][S26]。

**IBM 的意外发现。** 8 月 30 日独立媒体发布的现场采访中，IBM 设计负责人解释两套解码器共享大部分核心资源；商业动机涉及把 Arm 软件与主机数据放到同一运行环境。采访同时强调成熟内存、测试和可靠性取舍。它支持“兼容性与可靠性可能比追求最高规格更重要”的解释，但不提供产品售价或量产时间。[设计者访谈文字稿][S41]

**RISC-V 的正确读法。** SiFive 明确说 CUDA 已在开发平台作为 NVIDIA GPU 的 host 运行；计算仍由 GPU 承担。RVA23、发行版、驱动和平台服务的贯通比 ISA 本身更接近商业采用门槛。开发设备供应紧张也不能直接解释为大规模生产 CPU 需求超预期。


**Crescent Island 提供另一种内存与部署取舍。** Intel 8 月 24 日披露最高 480 GB LPDDR5X、350 W 风冷 PCIe 卡；Wildcat Lake 则以主流客户端/边缘芯片采用 UCIe。前者提示，存得下模型与适配现有机房也能成为产品目标。[Intel 会期公告][S19] **判断：** 大容量 LPDDR 路线是否划算，要看带宽、并发、尾时延和整卡价格；容量大不等于每秒服务量高。若客户主要受机房改造、电力与液冷条件限制，它可能有适用空间；若热数据搬运占主导，低功耗卡也可能需要更多卡才满足吞吐。当前缺少足够完整的同 SLA 客户测试和成交价，不能直接认定 TCO 优于 HBM 方案。

### 9. 网络：从端口速率到拥塞、通信卸载与故障后的有效吞吐

Broadcom 的 800G Thor Ultra 于 2025-10-14 已公开发布，会议是架构展开；其 2026 年 MRC 技术材料讨论多路径可靠连接与多平面网络。必须区分 scale-up、scale-out 和前端服务网络，不能仅按 800G/1.6T 速率合并市场。[Thor Ultra 原始发布][S36]、[MRC 技术材料][S25]

NVIDIA 会期强调多平面网络与 BlueField-4 服务卸载；Meta 则把 NIC 与集合通信引擎放到自研封装/芯片体系。共同方向是提高故障、拥塞和并行通信状态下的有效产出，采用条件包括可靠传输、拥塞控制、拓扑与软件匹配。[NVIDIA 会期说明][S05]、[Meta 技术说明][S11]

**判断：** 同样的加速器数量，多平面、更高 radix、片内 NIC 和机架内直连可能改变外置 NIC、交换层数、光模块和铜缆用量。可用模型为“设备数 × 每设备端口 × 光/铜比例 × 冗余系数 × 单位售价”，每一项都须依具体架构确定。不能把网络 ASIC 收入、光模块收入与整网投资重复相加。

### 10. 物理 AI、FPGA 与非主流研究：保留技术价值，暂不强造市场规模

**Waymo。** 8 月 20 日配套文章披露 5 nm 定制 ASIC，用于原始传感器数据处理和融合；前端 ASIC 合计超过 1,000 TOPS，系统同时处理 13 路高分辨率相机，并强调冗余和低 batch 时延。这里的 TOPS 没有足够统一条件与数据中心 FP4 FLOPS 横比；文中超过 2 亿英里为 Waymo 经验总量，不能归因给新芯片。[Waymo 技术文章][S37]

**BOS Eagle-N。** 8 月 26 日公司确认 24 日演讲已发生；产品页为 Tenstorrent NPU、250 INT8 dense TOPS，并支持 PCIe/UCIe 集成。重点是可扩展车载计算和软件/安全集成。本次未取得客户车型定点、SOP 数量或价格；产品页另写 Eagle-A 的 2028 量产计划，不能移用于 Eagle-N。[BOS 会后说明][S38]、[产品规格][S39]

**AMD Versal RF。** 会前 2025-11-11 公告已经说 VR1602 工程样片出货；它整合 RF 转换器、硬化 DSP 与可编程计算。相同功能最高节电 80% 的口径是相对 FPGA-only 实现，不是所有整机节电 80%。2026 议程和工具支持不单独证明已规模量产。[Versal RF 样片公告][S42]

**Normal Computing CN101。** 2026-08-01 预印本描述标准 CMOS 的数字热力学计算原型，可在随机动态与计算精度之间取舍。公司 8 月材料展示小规模 MNIST/CIFAR-10 生成，六芯片系统的层间并行实验有周期改善；这不是前沿大模型整机能效或商业收益证明。[CN101 预印本][S44]、[公司原型说明][S45]

**其余学术海报。** 本届还有光子 crossbar、事件驱动 GNN、边缘小模型 chiplet 和开源编译器/教学芯片等。原始海报未取得时，不引用标题中的延迟、工艺或系统规模作完整性能结论；下一轮优先取得数据集、精度、频率、功耗、芯片面积和比较基线，而非先分配美元 TAM。

## 商业采用与价值捕获

### 已披露美元数据：先限定可计算的市场边界

| 口径与日期 | 数字 | 计算或披露依据 | 可以推导的结论 | 不能推导的结论 |
|---|---|---|---|---|
| NVIDIA 数据中心业务，FY2027 Q2，截至 2026-07-26，8 月 26 日发布 | 收入约 890 亿美元；同比 +117% | 公司财报；集团收入约 962 亿美元 | 已有大规模硬件/系统/网络需求，且会前已形成 | 890 亿美元不是 Hot Chips 新品收入或整个 AI 芯片 TAM |
| NVIDIA 集团毛利率，同期 | GAAP/非 GAAP 均 75.0% | 集团财报 | 目前平台价值捕获仍强 | 不是 Rubin、LPX 或网络业务独立毛利率 |
| Micron，FY2026 Q3，2026-06-24 披露 | 公司收入 414.56 亿美元；DRAM 收入 313.28 亿美元 | 财报和财报演示 | 存储涨价和高端产品已有财务反映 | 不能将全部 DRAM 算作 HBM |
| Micron Cloud Memory BU，同期 | 收入 137.69 亿美元；分部毛利率 83% | 公司分部披露 | 提供高端云存储价值捕获的观察点 | 分部含多产品，不是 HBM 独立毛利率 |
| Micron HBM4，截至 2026-06-24 | 已交付对应收入超过 10 亿美元 | Prepared remarks | HBM4 跨过样片/纯路线阶段 | 不是全球 HBM4 市场总额，也不是本季度全 HBM 收入 |
| Micron 多年 SCA，2026-06-24 | 14 项协议最低价格对应剩余累计收入约 1,000 亿美元；预计现金存款和相关财务承诺 220 亿美元 | 合同最低价/承诺量口径 | 部分供需从短期采购走向多年约束 | 不全是 HBM；不是 2026 单年收入，承诺也不等于已到账现金 |

来源：[NVIDIA 财报][S32]、[Micron 财报][S33]、[Micron prepared remarks][S34]、[Micron 财报演示][S46]。财报里的毛利金额与毛利率分别读取，未将金额误记为百分比。

**HBM 市场规模的历史参考。** Micron 在 2025-12-17 曾给出 2025 年约 350 亿美元、2028 年约 1,000 亿美元的全球 HBM TAM 预测，约 40% CAGR。这是会前供应商预期基线，不是 2026-09-05 已实现市场规模。本次未取得同口径、足够完整的最新全球 HBM 实现额，故不通过直线插值填一个“2026 实际规模”。[2025 年底的预测原文，检索索引可读][S47]

对 HBF、zHBM、CN101、自研 ASIC 的“可替代市场”，目前缺少独立销售边界、客户量、价格和投入成本，报告保留未知。客户自用芯片价值可表现为服务成本下降而非芯片营收；以全体 GPU 收入作它们的立即可服务市场会严重高估。

### 从技术指标到经济结果的推导

**1. 推理容量。** 在 memory-bound 且其它条件保持一致时：

`有效模型带宽 = 峰值内存带宽 × 带宽利用率`

`token 吞吐上限 ≈ 有效模型带宽 ÷ 每 token 实际需搬运字节数`

第二个分母不能省略：batch、权重复用、KV cache、MoE 激活比例及量化都会改变它。因此不能把“TB/s × 利用率”直接写成“token/s”，也不能用同一个带宽利用率横跨不同模型。这是量纲与机制分析，非公司盈利预测。

**2. 显存的美元敏感度。** 按 MI455X 规格，每颗 432 GB、72 颗机架合计 31,104 GB。**假设采购价格每 GB 变动 1 美元**，且全部显存按这一相同幅度传导，则每颗物料差额 432 美元、每机架 31,104 美元。此处 1 美元是敏感度单位，不是当前 HBM 报价；还未计入封装、测试、良率及合同差异。它说明显存价格和交付数量比宣称的峰值倍数更适合跟踪成本传导。

**3. 能源成本示例，非实际项目预算。** 假设一个设施持续消耗 100 MW IT 功率、PUE=1.2、全年 8,760 小时、电价 0.06–0.12 美元/kWh，则年电费约 **6,307 万–1.261 亿美元**。如果在相同有效业务量下，整机而非单芯片电耗下降 20%，理论节省约 **1,261 万–2,523 万美元/年**。这一估算不含建设资本、网络、人员、融资、闲置与税费；若节省的功率被用于新增请求，体现为产能扩张而非账面电费下降。

**4. 自研/替代的门槛。** 净收益应为“避免的外购成本 + 运营节省 + 有用产出增量 − 芯片研发/NRE − 软件与验证 − 新系统部署 − 失效率和闲置损失”。缺少这些输入时，不能把厂商每瓦领先 1.5 倍直接转成平台毛利率提高 50%。

**5. 多芯片良率与维修。** 模块化可降低整机更换成本，但串联器件和复杂封装增加失效与测试负担。作为简化数学例子，若 12 个必须同时合格的独立部件每个通过率为 99%，系统一次全部通过概率为 `0.99^12≈88.6%`；若为 99.9%，则约 98.8%。实际生产采用已知良品、返修、冗余和分阶段测试，不能用此例替代厂商良率；它解释为何测试、工艺控制和可靠性可能比名义器件数量更有价值。

### 利润率的方向：分层判断

- **HBM/先进封装：** 性能要求、堆叠复杂度和可分配产能支持议价，但更高层数/速率也增加成本。Micron 当前高利润不应永久化；需区分价格周期与结构性单位含量增长。多年协议的价格上下限可能降低周期波动，同时限制部分现货上涨收益。
- **GPU 平台：** 软硬件协同、供应可得性、支持和网络能维持溢价；自研和异构部署提升客户议价能力。只有收入组合、成交价格与全栈利润变化才能检验侵蚀是否发生。
- **自研 ASIC：** 直接受益者可能是拥有稳定内部工作负载的平台；实现和制造伙伴获取收入，但不等于拥有模型/应用租金。
- **独立解码/近存公司：** 若软件集成可重复、客户续单且芯片利用率足够高，技术优势可转化为毛利；否则定制工程和支持费用可能使名义硬件毛利失真。
- **系统、测试和散热：** 看每机架新增价值、生产测试时长和服务收入。整合可减少独立部件数量；不能仅凭电力密度提高就推导所有冷却或连接供应商收入等比例增长。

## 开放洞见与重要分歧

### 1. 最容易低估的可能是“软件可移植到可高效运行”之间的工程成本

事实基础是 SiFive 将平台定位为移植/调优/验证，Meta 和 Microsoft 保留专用编译器及通信库，OpenAI 仍需模型专用优化。**判断：** 支持 PyTorch/CUDA 接口是入口，达到稳定 SLA 和高利用率才是采用完成。竞争核心可能从“是否有软件”变为新模型适配速度、回归验证和运维成本，而不是单纯 ISA 或算力。[SiFive][S26]、[Meta 软件路线][S14]、[Maia 工具链][S18]

反证：跨架构部署若已能自动达到相同质量和 SLA，且长期维护成本低，上述软件壁垒的重要性应下修。

### 2. 自研 ASIC 是价值重新分配，也可能扩大现有 GPU 平台边界

会期并列出现 ASIC 和 GPU，并不证明二者需求零和。Google 同时宣布 TPU 与 NVIDIA 平台；SambaNova 的演示仍使用 NVIDIA prefill；OpenAI 公开表示仍将部署其他伙伴加速器。**判断：** 应拆分每阶段占比、单位请求成本和总业务量。[Google 产品组合][S10]、[SN50 演示][S30]、[OpenAI][S13]

反证：若客户同口径披露第三方 GPU 净采购缩减，且原因确为同工作负载被自研芯片替代，而非设施/融资约束，则替代论才得到更强支持。

### 3. HBF 与高带宽冷数据，可能比“廉价 HBM 替身”更合理

HBF 厂商自己的层级定义就不是所有热内存的等价替换。**判断：** 最先有收益的用例可能是大容量、低访问强度的工作集，而不是任意实时 attention。这里不声称市场普遍错误，因为未取得可量化共识；只修正部分宣传容易诱发的过度外推。[HBF 一手披露][S23]

反证：如果公开客户数据证明高写入、高并发、长上下文实时路径在同质量下也有稳健 TCO 优势，应扩大采用边界。

### 4. “HBM 三倍晶圆面积”不能推出全行业 DRAM 供给减少三分之二

本次检索到的 Reddit 讨论出现这类外推；页面仅给出相对时间，精确发帖日期未取得，检索日为 2026-09-05。即便某代 HBM 对同容量 DDR 的晶圆消耗比为 3，也必须知道用于 HBM 的晶圆占比、工艺、位密度和良率。若简化假定总晶圆数固定、其中比例 `f` 转向每 bit 占面积 3 倍的产品，则总 bit 相对全做普通 DRAM 为 `(1−f)+f/3=1−2f/3`，只有 `f=1` 才是减少三分之二。该公式仅为条件校验，不是产业供给预测。[非官方讨论][S49]

Micron 6 月材料确实指出 HBM 的 trade ratio 与代际复杂度会挤压非 HBM 供应，支持方向但不支持上述全行业固定降幅。[Micron 供需说明][S34]

### 5. 新颖不等于低置信，量产也不等于没有风险

CN101 有可访问预印本和测试原型，应保留研究价值；IBM 的双 ISA 虽不是 GPU 热点，却可能扩大软件可用范围。相反，声称生产的机架仍要经过客户验收、配置调整和稳定运行。需要分别记录“机制成立”“产品可制造”“业务愿意买”“财务能赚钱”四层，不能用单一成熟度标签包办。

### 非官方材料如何影响本报告

| 来源 | 日期、类型 | 本次使用方式 | 置信度及一手验证 |
|---|---|---|---|
| Chips and Cheese：IBM 现场采访 | 2026-08-30 发布；具名设计负责人访谈，文字稿编辑过 | 解释双 ISA 商业动机、可靠性取舍 | 中高；双 ISA 由 IBM 官方确认，具体访谈措辞仍按采访来源处理 |
| STH：MI400、MTIA、TPU、Jalapeño 等现场记录 | 2026-08-24/25；技术媒体实时记录 | 辅助确认会议实际展开和寻找原始材料 | 中；关键规格优先回查公司，不把多个转载当独立测量 |
| Tom’s Hardware：SK hynix hybrid bonding 路线 | 2026-08-24；媒体演讲报道，部分内容受限 | 只作为 HBM5/包装时间线的待核线索 | 中低；本次未取得同场原始 PDF，不支撑设备订单结论 |
| Andrew Sloss 会后反思 | 页面仅显示相对时间；2026-09-05 检索；个人帖文 | 关于营销倍数和单 workload 优化的质性提醒 | 低；不推定具体发帖日，不视为机构共识 |
| Reddit：HBM 晶圆面积讨论 | 精确发帖日未取得；2026-09-05 检索；论坛讨论 | 检查“单位面积比→全行业供给”错误外推 | 低；产业挤压方向由 Micron 另行验证，论坛计算未获确认 |

相关入口：[IBM 采访][S41]、[STH MI400][S48]、[HBM 路线报道][S43]、[Sloss 帖文][S50]、[论坛讨论][S49]。未取得可核验的非公开采购或供应链访谈，本报告没有匿名“产业链称”式核心结论。

## 公司和产业链映射

下表说明技术位置与经济条件，不是推荐顺序。“关联不足”表示证据不足以认定受益，不表示公司没有相关能力。

| 公司/群组 | 产业位置与实际暴露 | 当前证据 | 价值捕获条件与误判风险 |
|---|---|---|---|
| NVIDIA | GPU、CPU、LPU、网络、软件及机架 | 会期发布、技术文章、财报 | 综合平台和供应能力；专用解码不必导致平台份额流失 |
| AMD | GPU、EPYC、网络、机架及 FPGA | 产品规格、客户计划、工程样片 | ROCm、交付和验收；不能把合作 GW 上限当当年收入 |
| Intel | CPU、推理 GPU、工艺与封装 | 会期具体规格 | 性能、制造和客户平台兑现；内部产品使用某工艺不证明外部代工订单 |
| Google | TPU/Axion 与云服务、内部模型平台 | TPU 双路线公开技术资料 | 价值主要在云服务成本和产品能力；无独立 TPU 芯片销售口径 |
| Meta | 内部推荐、广告与 GenAI 加速器 | 生产通信数据及分代路线 | 节省采购/运营成本；不能用 300 的采用证明 400/500 收入 |
| Microsoft | Maia、自用云基础设施 | 1 月部署和技术披露 | 内部利用率、模型覆盖；集团云利润不等于单 ASIC 毛利 |
| OpenAI | 自用模型—芯片—服务协同 | 工程样片、实测和部署计划 | 软件成熟和量产资格；年底计划不等于已经规模部署 |
| Broadcom | 自研 ASIC 实现、以太网及连接 | OpenAI/Meta 点名合作，Thor Ultra | 实现/网络价值；客户自研不等于 Broadcom 利润率确定 |
| Celestica | 板卡、机架及系统工业化 | OpenAI 6 月公告明确点名 | 交付量、复杂度及服务价值；未公开合同金额和产品毛利 |
| TSMC | 多种先进芯片工艺、封装需求 | AMD、Microsoft 等具体工艺披露 | 良率、产能、封装组合；多个芯片路线可共同消耗产能，不能重复计 TAM |
| SK hynix | HBM、热管理、HBF | iHBM、HBF 一手材料 | 客户认证与持续供给；HBF 不是当前 HBM 收入的直接替代量 |
| Samsung | HBM、logic base die、PIM、3D 内存 | FMS 和会期议程 | 定制协同与制造；zHBM 概念不能变成当前订单 |
| Micron | HBM、DRAM、NAND 和长期供货 | 财报、HBM4 收入、SCA | 供需和合同；分部毛利不可直接归因 HBM |
| Sandisk | HBF/NAND 生态 | SK hynix 联合规范披露 | 规范采用、读写特性与软件；缺实际 HBF 收入边界 |
| Arm | ISA/IP 生态与 Arm AGI 产品 | 公司会后说明、IBM 合作 | IP 与芯片业务分别计量；兼容性扩张不能直接换算 royalty |
| SiFive | RISC-V CPU IP 和开发平台 | 有限量 BigSky 可用 | 客户移植转成生产 SoC；GPU 主机支持不等于取代 NVIDIA |
| Cerebras | 晶圆级计算及机架平台 | CS-4 技术披露、后续路线 | 服务可用性、模型规模和维护；CS-5/6 目标单列 |
| SambaNova | RDU、软件和服务 | 演示、kernel 测量、模型推演 | 异构成本和稳定模型效率；建模不可充当收入验证 |
| d-Matrix | 低时延推理、3D DRAM | Pavehawk 测试芯片 | 可制造性与系统规模；pJ/bit 不能当美元/token |
| XCENA | CXL 内存扩展与近存计算 | MX1 厂商实测 | 2026 年底/2027 年目标兑现、客户软件；不得外推 kernel 倍数 |
| BOS / Tenstorrent | 车载 chiplet、NPU IP | 产品参数及会后说明 | 车型定点、安全集成和寿命周期；未证实量产车型数量 |
| Waymo | 自用物理 AI 系统 | 定制计算公开说明 | 自动驾驶服务单位经济性；不应视为外售 ASIC 市场 |
| Normal Computing | 新计算原语、原型与研发 | CN101 预印本和演示 | 大模型质量、能耗及系统扩展；暂无可合理估计的芯片 TAM |
| Advantest、Chroma、Murata 等配套 | 测试、元件等候选位置；本次先确认参与关联 | 官网赞助/活动入口 | 要取得对应设备、客户和单位含量；赞助标识不构成特定产品订单 |
| Etched、XSight、其他赞助企业 | 本次主要取得参会关联 | 赞助标识 | 缺与本届技术、客户及收入相连证据，暂不列确定受益者 |

资料依据集中于前述产品段与 [官方参与入口][S01]。对“伪受益”的处理原则是找出推理链缺口：只有名称、赞助、同属 AI 标签的公司，不给予订单、利润或估值弹性推断。

## 风险、反证条件和后续跟踪

### 哪些信息足以推翻或下修本报告

| 当前判断 | 关键反证/升级证据 | 需要的原始字段 | 建议刷新频率与节点 |
|---|---|---|---|
| 低时延专用芯片有分工价值 | 同 SLA 下整机 TCO 未改善，或低负载利用率明显更差 | 模型/精度、ISL/OSL、并发、TTFT、TBT/P99、墙端功率、价格 | 每次独立 benchmark、客户公开服务上线时 |
| Jalapeño 从样片走向部署 | 年底未上线、资格验证拖延、模型覆盖受限；反之实际业务稳定运行可升级 | 客户/自用地域、芯片数、生产模型、可靠性、验收 | 月度；重点 2026 Q4 至 2027 Q1 |
| Helios 实际采用推进 | 客户上线晚于目标、机架验收或 ROCm 性能不达预期 | 实际通电/上线日期、交付与验收数量 | 季度财报及客户公告；重点 2026 Q4 |
| MTIA 代际扩展 | 400/450/500 未按计划部署，或 GenAI 负载回退 GPU | 各代数量、工作负载、故障率、迁移成本 | 季度；450 的 2027 年初目标单独核验 |
| HBM4 收入已成立，后续供给仍受约束 | 新产能快速释放、价格/毛利显著下降，或客户需求转弱 | 产品 ASP、良率、实际产能、客户认证、合同价格机制 | 季度财报；新增工厂/封装产线进度 |
| 3D DRAM/HBF 尚未规模商业化 | 命名客户、大规模验收、可复核软件和量产经济性出现 | 客户、出货、单位成本、带宽/延迟/耐久和完整系统功耗 | 月度；标准版本、样片、客户资格验证逐事件更新 |
| RISC-V 处开发平台阶段 | 云生产 SKU、持续采购和完整 SLA 出现 | 可买 SKU、系统认证、驱动、长期支持、工作负载基准 | 季度及发行版/平台发布 |
| 互联整合改变器件价值量 | 新拓扑实际 BOM、端口/交换层/光铜比例与推演不符 | 拓扑图、BOM、数量、传输距离、冗余、故障后吞吐 | 每次机架公开设计/OCP 材料更新 |
| 车载路线未确认外部放量 | OEM 定点、车型 SOP 和可追溯验收证据 | 客户、车型、SOP 时间、芯片含量、功能范围 | 季度；不套用云芯片月度节奏 |
| 非主流原型保留技术可选性 | 大模型效果不达标、扩展能耗恶化；或第三方复现实验显著提升 | 数据集、质量、实际能耗、成本、扩展曲线 | 论文/开源发布时，至少半年复查 |

以上为建议的人工跟踪计划，未创建自动任务、订阅或通知。

### 下一轮优先补齐的材料

1. **2026 年 12 月初官方公开窗口**：按 FAQ 预期检查完整 slides 和录像，核对变更版本与实际问答。优先 SK hynix、Samsung PIM、Fujitsu、MI400 系统、TPU8、Waymo keynote。
2. **性能复核**：取得公开 benchmark 原始配置和输出；记录精度/质量、完整系统数量、有效 token、功率分母和价格来源，避免复制宣传摘要。
3. **采用复核**：优先客户自己的发布、验收和可购买服务，依次跟进 Nebius LPX、Helios 客户、Jalapeño 自用部署、XCENA 2027 收入。
4. **标准与软件**：HBF 的 OCP 正文、平台互操作结果；RISC-V 主机与 NVIDIA GPU 的完整要求；通信协议版本和不同厂商间互操作。
5. **供给与利润**：HBM4/4E 实际收入及认证客户、先进封装产能投产、合同预付款与收入确认。收到公司财报后刷新，不能仅用会议路线图滚动上调。
6. **独立现场材料**：优先具名工程师访谈和实际测试记录；不将未标来源的社交截图或多个自动摘要叠加成“产业共识”。

## 来源清单

所有来源均于 2026-09-05 检索；以下“高”指适合核验该主体的日期、规格或披露，不代表厂商预测具有高实现概率。没有明确发布日的页面标为“无固定日期，截止日快照”。同一公司材料跨语言版本或转发不计为独立验证。

### 一手官方会议材料

| 编号 | 来源与日期 | 可信度、用途和访问情况 |
|---|---|---|
| S01 | [Hot Chips 2026 官网及议程][S01]；2026 会期，页面无固定更新日 | 高：日期安排、会议结束、报告入口、赞助图片标识；未获得受限演讲全文 |
| S02 | [Hot Chips 2026 FAQ][S02]；截止日页面 | 高：录像/幻灯片访问限制与预计 12 月公开 |
| S03 | [Call for Contributions][S03]；2026 投稿安排 | 高：外部核验 8 月 23–25 日会期 |
| S04 | [Hot Chips 2025 归档][S04]；2025-08-24 至 26 | 高：上届主题基线，不继承任何项目研究结论 |

### 一手公司、客户与投资者材料

| 编号 | 来源与材料日期 | 可信度及边界 |
|---|---|---|
| S05 | [NVIDIA：Vera Rubin、LPX、多平面网络会期发布][S05]；2026-08-24 | 高于转述；性能/客户状态为供应商披露。正文局部把 8 月 24 日写为 Tuesday，与日历不符，采用页首绝对日期，不依赖星期标记 |
| S06 | [NVIDIA Rubin 架构][S06]；2026-07-21 | 一手技术；峰值与推演不等于完整生产基准 |
| S07 | [AMD Advancing AI 2026 公告及脚注][S07]；2026-07-23 | 一手产品、客户计划与测试条件；价格部分为预测 |
| S08 | [Google TPU 8t/8i 技术深入说明][S08]；2026-04-22 | 一手技术；理论规格、拓扑能力和厂商比较 |
| S09 | [AMD MI455X 规格][S09]；发布日 2026-07-23，截止日快照 | 高：规格；页面动态，未把上市日当客户验收日 |
| S10 | [Google Next 2026 AI infrastructure][S10]；2026-04-22 | 一手发布基线与供应状态；不证明截至 9 月各地 GA |
| S11 | [Meta MTIA 300 通信与生产数据][S11]；2026-08-24 | 高：自用数据；通信加速不等于全训练加速 |
| S12 | [OpenAI/Broadcom Jalapeño 首次披露][S12]；2026-06-24 | 一手样片及合作角色；九个月指设计至 tapeout 的路径 |
| S13 | [OpenAI Jalapeño 首批实测][S13]；2026-08-25 | 一手方法/实测；按额定芯片功率归一化，部署尚在推进 |
| S14 | [Meta 四代 MTIA 路线][S14]；2026-03-11 | 一手分代成熟度与目标；不把累计量移用于新代 |
| S15 | [Microsoft Maia 200 部署公告][S15]；2026-01-26 | 一手内部部署；未披露全量区域和经济明细 |
| S16 | [Cerebras Hot Chips 架构及后续路线][S16]；2026-08-25 | 一手；CS-5/6 为未来路线，带宽比较需统一边界 |
| S17 | [SambaNova Hot Chips 会后技术文章][S17]；2026-09-02 | 一手演讲者总结；区分硅上测量与建模 |
| S18 | [Microsoft Maia 200 architecture deep dive][S18]；2026-01-26，01-30 更新 | 一手技术，原文产品峰值口径 |
| S19 | [Intel Hot Chips 三类架构公告][S19]；2026-08-24 | 一手会期规格；未提供所有产品的量产验收 |
| S20 | [d-Matrix Pavehawk/3DIMC 验证][S20]；2026-03-16 | 一手测试芯片结果；系统经济性未知 |
| S21 | [Samsung FMS 3D-memory vision][S21]；事件 2026-08-04，页面 08-05 | 一手概念、样品与路线；不是同场 Hot Chips 全文 |
| S22 | [SK hynix iHBM][S22]；2026-05-26 | 一手热管理方案，30% 为热阻口径 |
| S23 | [SK hynix/Sandisk HBF 首版规范披露][S23]；2026-08-04 | 一手标准参与者披露；未独立审核 OCP 全文及互操作 |
| S24 | [XCENA MX1 公司新闻稿（Business Wire 分发镜像）][S24]；2026-08-25 | 明确标为 XCENA 经 Business Wire 发布，一手厂商声明；原站本次未成功打开 |
| S25 | [Broadcom MRC 技术文章][S25]；2026 年，会前页面，精确日期本次未确认 | 一手技术；仅作为截至截止日的架构材料 |
| S26 | [SiFive BigSky 开发平台][S26]；2026-08-24 | 一手有限量供应与 CUDA host 验证 |
| S27 | [Arm Hot Chips 会后总结][S27]；2026-09-02 | 一手参与者；Arm 生态判断存在厂商立场 |
| S28 | [IBM 双架构处理器公告][S28]；2026-08-24 | 一手未来产品方向 |
| S29 | [SambaNova SN50 首次公告][S29]；2026-02-24 | 一手原始交付目标 |
| S30 | [SambaNova RAISE 演示配置][S30]；2026-07-08 | 一手演示；厂商转述基准，未独立重跑 |
| S31 | [Nebius 官网采用披露][S31]；无固定日期，截止日快照 | 客户侧采用确认；未取得交易金额和广泛服务可用性 |
| S32 | [NVIDIA FY2027 Q2 财报][S32]；2026-08-26 | 高：财务披露与生产状态；不是新品分项利润 |
| S33 | [Micron FY2026 Q3 财报][S33]；2026-06-24 | 高：实现收入、分部毛利率、产品状态 |
| S34 | [Micron FY2026 Q3 prepared remarks][S34]；2026-06-24 | 高：HBM4 收入、SCA、供给约束；PDF 正文可取 |
| S35 | [NVIDIA Vera CPU 技术说明][S35]；2026-03-16 | 一手规格和平台计划 |
| S36 | [Broadcom Thor Ultra 首次发布][S36]；2025-10-14 | 一手历史基线；不误记为 2026 首发 |
| S37 | [Waymo 计算系统说明][S37]；2026-08-20 | 一手自用系统；不是 keynote 全录 |
| S38 | [BOS Eagle-N 会后说明][S38]；2026-08-26 | 一手确认实际演讲；没有客户量产订单明细 |
| S39 | [BOS Eagle 产品页][S39]；无固定日期，截止日快照 | 一手参数；Eagle-A 与 Eagle-N 时间线分开 |
| S40 | [Chroma Hot Chips 活动页][S40]；2026 会期，页面无发布日 | 仅用于参与核验，不证明测试订单 |
| S42 | [AMD Versal RF 样片公告][S42]；2025-11-11 | 一手会前成熟度；后续目标不自动当完成 |
| S45 | [Normal Computing 原型说明][S45]；页面标 8.4.2026，按美国日期为 2026-08-04 | 一手原型与观点，商业化结论低置信 |
| S46 | [Micron FY2026 Q3 earnings deck][S46]；2026-06-24 | 高：财报中的收入与分部表格；与新闻稿交叉核对 |
| S47 | [Micron FY2026 Q1 prepared remarks 原始入口][S47]；2025-12-17 | 本次检索索引读到 TAM 段落；旧链接存在迁移风险，只保留为历史预期基线，不作当前事实锚 |

### 技术论文与独立具名访谈

| 编号 | 来源与日期 | 可信度及用途 |
|---|---|---|
| S44 | [CN101 — A Digital Thermodynamic Computer for Generative AI][S44]；arXiv v1，2026-08-01 | 一手预印本；本次核验摘要/版本，未声称完成全文或复现实验 |
| S41 | [Chips and Cheese 采访 IBM 设计负责人][S41]；2026-08-30 | 具名一手访谈，经媒体编辑；读取文字稿，未声称观看完整视频 |

Meta MTIA/HCCL 的论文入口见 S11，因本次主要核验配套一手技术正文，不把未读论文列为独立证据数量。

### 非官方分享、二手报道与研究线索

| 编号 | 来源与日期 | 降权处理 |
|---|---|---|
| S43 | [Tom’s Hardware：SK hynix hybrid bonding 路线报道][S43]；2026-08-24 | 二手会场报道；原始 PDF 受限，路线时间仅作待核 |
| S48 | [ServeTheHome：AMD MI400 会场记录][S48]；2026-08-24 | 二手技术报道；规格回查 AMD，现场记录不作独立性能测试 |
| S49 | [Reddit：HBM 晶圆面积讨论][S49]；精确发帖日未取得，2026-09-05 检索 | 非官方论坛；只用于识别外推风险 |
| S50 | [Andrew Sloss：Hot Chips 2026 reflections][S50]；精确发帖日未取得 | 个人质性分享；只使用截止日前可检索内容，不当机构共识 |

### 可复核的受限官方入口

- [SK hynix 包装教程 PDF](https://hc2026.hotchips.org/assets/program/tutorials/HC2026.SK%20hynix.Jaesik_FINAL1.pdf)
- [Samsung LPDDR5X-PIM PDF](https://hc2026.hotchips.org/assets/program/conference/day2/HC2026.Samsung.KaramHwang.v06(final_legal%20disclaimer).pdf)
- [FUJITSU-MONAKA PDF](https://hc2026.hotchips.org/assets/program/conference/day1/HC2026.FUJITSU.RYOHEI_OKAZAKI.v7.pdf)
- [全套 proceedings ZIP v2](https://hc2026.hotchips.org/assets/program/hc2026-full-program-v2.zip)

以上入口用于重现访问边界，不代表正文已取得。报告结论不会因为链接存在而获得额外证据等级。

[S01]: https://hc2026.hotchips.org/
[S02]: https://hc2026.hotchips.org/faq/
[S03]: https://hotchips.org/call_for_contrib/
[S04]: https://hc2025.hotchips.org/
[S05]: https://blogs.nvidia.com/blog/vera-rubin-lpx-spectrum-x-nvlink-fusion/
[S06]: https://developer.nvidia.com/blog/inside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai/
[S07]: https://ir.amd.com/news-events/press-releases/detail/1294/aai-2026-amd-delivers-full-stack-compute-for-the-agentic-ai-era
[S08]: https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive
[S09]: https://www.amd.com/en/products/accelerators/instinct/mi400/mi455x.html
[S10]: https://cloud.google.com/blog/products/compute/ai-infrastructure-at-next26
[S11]: https://engineering.fb.com/2026/08/24/networking-traffic/mtia-300-meta-training-chip-built-in-nics/
[S12]: https://openai.com/index/openai-broadcom-jalapeno-inference-chip/
[S13]: https://openai.com/index/jalapeno-first-results/
[S14]: https://ai.meta.com/blog/meta-mtia-scale-ai-chips-for-billions/
[S15]: https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/
[S16]: https://www.cerebras.ai/blog/ultrafast-frontier-inference-cerebras-deep-dive-at-hot-chips-2026
[S17]: https://sambanova.ai/blog/hot-chips-2026-dataflow-at-scale
[S18]: https://techcommunity.microsoft.com/blog/azureinfrastructureblog/deep-dive-into-the-maia-200-architecture/4489312
[S19]: https://www.intel.com/content/www/us/en/newsroom/news/client-computing/intel-outlines-architectures-for-agentic-ai-at-hot-chips-2026.html
[S20]: https://www.d-matrix.ai/going-vertical-why-we-created-a-3d-dram-solution-to-advance-low-latency-ai-inference/
[S21]: https://news.samsungsemiconductor.com/global/samsung-unveils-next-gen-3d-memory-vision-at-fms-2026-charting-the-future-of-ai-infrastructure/
[S22]: https://news.skhynix.com/en/ihbm-solution/
[S23]: https://news.skhynix.com/en/hbf-at-fms-2026/
[S24]: https://markets.financialcontent.com/wral/article/bizwire-2026-8-25-xcena-details-mx1-architecture-integrating-memory-expansion-and-near-memory-computing-at-hot-chips-2026
[S25]: https://www.broadcom.com/blog/enabling-ai-networking-scale-with-multi-path-reliable-connections-mrc-
[S26]: https://www.sifive.com/press/risc-v-in-the-datacenter-bigsky-development-server
[S27]: https://newsroom.arm.com/blog/hot-chips-2026-arm-cpu-agentic-ai
[S28]: https://newsroom.ibm.com/campaign?item=2919
[S29]: https://sambanova.ai/blog/introducing-the-sn50-rdu-purpose-built-for-agentic-inference
[S30]: https://sambanova.ai/blog/sn50-runs-fastest-minimax-speeds-in-the-world
[S31]: https://nebius.com/
[S32]: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/default.aspx
[S33]: https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Results-for-the-Third-Quarter-of-Fiscal-2026/default.aspx
[S34]: https://s25.q4cdn.com/621799436/files/doc_financials/2026/q3/Q3-FY26-Prepared-Remarks.pdf
[S35]: https://developer.nvidia.com/blog/nvidia-vera-cpu-delivers-high-performance-bandwidth-and-efficiency-for-ai-factories/
[S36]: https://investors.broadcom.com/news-releases/news-release-details/broadcom-introduces-industrys-first-800g-ai-ethernet-nic
[S37]: https://waymo.com/blog/2026/08/look-under-our-trunk/
[S38]: https://www.bos-semi.com/post/bos-semiconductors-presents-chiplet-based-ai-accelerator-eagle-n-at-hot-chips-2026
[S39]: https://www.bos-semi.com/product
[S40]: https://www.chromaus.com/events/hot-chips-2026
[S41]: https://chipsandcheese.com/p/hot-chips-2026-interviewing-ibms
[S42]: https://www.amd.com/en/blogs/2025/now-shipping-versal-rf-series.html
[S43]: https://www.tomshardware.com/tech-industry/semiconductors/sk-hynix-says-hybrid-bonding-wont-be-ready-for-hbm4e-as-ai-memory-runs-into-a-775-micron-ceiling
[S44]: https://arxiv.org/abs/2608.00754
[S45]: https://normalcomputing.com/blog/ai-inference-needs-new-hardware
[S46]: https://s25.q4cdn.com/621799436/files/doc_financials/2026/q3/Micron_Q3_26_Earnings_Deck.pdf
[S47]: https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9
[S48]: https://www.servethehome.com/amd-mi400-gpu-at-hot-chips-2026/
[S49]: https://www.reddit.com/r/LocalLLaMA/comments/1w0mmk7/micron_hbm_requires_three_times_more_wafer_area/
[S50]: https://www.linkedin.com/posts/activity-7498408786278252544-riaI

