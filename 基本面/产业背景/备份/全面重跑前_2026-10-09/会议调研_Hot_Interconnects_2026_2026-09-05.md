# Hot Interconnects 2026 会议追踪：核心发现、技术路径与采用条件

> 会议：第 33 届 IEEE Symposium on High-Performance Interconnects（HotI 33），在线举行。会议日期：**2026-08-19 至 2026-08-21**；前两日为主要技术议程，第三日为教程，官网日程采用 Pacific Time。材料检索截止日期：**2026-09-05，America/Los_Angeles**。报告完成日期：**2026-09-05**。会议日期由官网议程及 UALink 联盟活动页交叉核验。[S01][S02]
>
> 资料边界：本报告独立检索外部公开材料，不读取、引用或继承项目内既有研究、索引、缓存和中间结论。只读取了输出路径上的 AGENTS.md 操作规则。本文是会议驱动的阶段性上游底稿；对未取得的演讲录像、论文全文、规格和客户验收资料，明确保留未知。

## 结论摘要

1. **最有实际采用支撑的进展是网络传输、拓扑与运行控制的协同，而不是所有光互连路线同时量产。** 本届纳入 MRC 传输论文；会前的系统论文已披露 OpenAI、Microsoft 生产训练使用，涉及 NVIDIA、AMD、Broadcom NIC。光共享内存、OCI、多芯光纤和 XPO 的证据阶段各不相同，不能放进一个“2026 全面商用”的篮子。[S01][S10][S11][S12]
2. **光互连的投资逻辑应从“更快端口”扩展到“更大的高带宽计算域”。** Lightmatter 会后公开的 prefill 论文研究跨出原生 scale-up 域所付出的通信代价；但结果来自模型，尚未在部署的光子硬件上验证。因此可上调“高基数、多机架互连值得验证”的优先级，不能直接把数倍性能收益变成客户收入或采购预测。[S14]
3. **四项 MSA 解决不同接口，既有竞争也有组合关系。** OCI 定义光 PHY，XPO 定义高密度液冷可插拔外形，Open CPX 面向靠近 ASIC 的可插接光引擎，SDM4 面向四芯光纤。它们均有会前来源，不能写成 8 月首次发布；联盟成立也不代表跨厂商完整互操作已完成。[S17][S18][S19][S20][S22]
4. **本届 XPO 热点的可核验核心是“12.8T、64 通道、液冷、LRO 演示主题”，还不是大批量客户交付。** 约 130 W 的会中演示数字目前仅找到媒体转述，缺少可取得的原始测试报告；400 W 则是会前公布的冷板散热能力，二者不能混用。12.8T XPO 演示在 3 月 OFC 已有厂商公告。[S01][S18][S23][S40]
5. **共享内存是值得追踪的新产品边界，但“接近本地内存”的条件仍需澄清。** Marvell 在 8 月 4 日已发布光共享内存组合，本届演讲继续讨论该架构；同日新闻稿写最远 50 米，技术博客写 30 米，并提出小于 350 ns 的访问延迟。缺乏统一测量边界，不能把三个指标合并成“50 米、完整访问小于 350 ns”。[S07][S25][S26]
6. **被热点掩盖的风险是 benchmark 失真。** 本届 DODOCO 研究显示，在其五类 MoE、真实文本与 H100 实验条件下，模拟 token 可能显著夸大路由不均衡；增加 expert parallelism 也不一定改变模型固有的专家热点。更大交换容量并不自动消除所有 MoE 长尾。[S15]
7. **需求是真实的，但特定新技术的收入归属仍要逐项核验。** Corning—Meta 的最高 60 亿美元多年协议及扩产开工有双方材料；Ciena 9 月 3 日财报反映光网络业务增长。这些可以验证互连投入，不能证明 SDM4、Open CPX 或某种 CPO 已对应同等订单。[S28][S29][S30][S32]
8. **本报告不把“多路线并存”包装为已发现市场错价。** NVIDIA 自身已明确支持可插拔与 CPO 两种形式；供应商公开预测也多指向多年迁移。缺少可核验的投资者一致预期与定价证据，本次形成的是技术和商业假设的纠偏，而非证券层面的反共识交易结论。[S20][S33]

### 证据等级与可取得性

| 标签 | 含义 | 能支持什么 | 不能直接支持什么 |
|---|---|---|---|
| F：事实 | 可核验文件、日期、协议、论文或财务披露 | 文件存在、明确披露的交易和财务数字 | 供应商性能陈述已独立复现 |
| V：厂商/运营方陈述 | 官方产品、演讲摘要、客户或运营团队自述 | 发布、目标、指定条件的自测/部署陈述 | 全行业效果、无条件量产、独立认证 |
| T：技术研究 | 可取得的方法、实验或建模材料 | 对应工作负载与配置的结论 | 自动推广到商业部署 |
| L：线索 | 媒体、个人笔记、社交平台分享 | 找原文、识别分歧、交叉核验 | 单独支撑核心技术或收入结论 |
| E / J | 本报告估算 / 判断 | 公开假设下的机制和条件 | 已发生的事实 |

“高置信度”首先指来源和命题可核验，不等于对未来收入高置信度。官方会议摘要中的“将讨论”按议程处理；实际演讲细节若只见于媒体，则仍标 L。

| 材料类别 | 本次取得情况，截至 2026-09-05 | 研究处理 |
|---|---|---|
| 官网、议程、keynote、赞助演讲摘要 | 已取得；官网确认在线形式及日期 | 可确认安排与主办方发布内容 |
| 正式论文集 | 找到 `conferences.computer.org/hotipub26/`；直接请求返回 **HTTP 401 Unauthorized** | 不能声称全文均已阅读；转向作者公开稿 |
| 作者公开论文 | 取得 MRC、光子 prefill、DODOCO、NVSHMEM 等；另取得 MRC 配套生产系统论文 | 注明版本日期；不默认与会场最终版完全相同 |
| 2026 全量演讲 slides | 当前议程页未取得完整下载集合 | 不把摘要扩写成已观看演讲实录 |
| 2026 录像 | 官网有嵌入视频及官方 YouTube 频道；嵌入抓取受限，频道未返回可核验的本届完整视频清单 | 未逐段观看、未取得逐字稿；不能声称录像不存在 |
| 会后报道 | 找到 Converge Digest、HPCwire、Semiconductor Engineering，以及 9 月 3 日 LightCounting 跨会议短评 | 作为线索与交叉验证；跨会议内容不能全部归入 HotI |
| 展商目录、客户订单、验收、报价、交期 | 取得赞助信息和公司外部材料；未取得独立展商目录及本届专属订单汇总 | 在线赞助演讲不能当作展位销售或客户采购证明 |

论文集和录像入口来自会后报道及官网；“会后约两周提供录像”是媒体转述的预期，并非本次已经验证全部上传。[S03][S39][S44][S45]

## 会议重点和方向变化

### 1. 与 2025 年相比：工作负载与交付条件变得更具体

2025 年官方议程已经包含 3D 光互连 MoE 训练、光子内存池、Ultra Ethernet、NVLink Fusion、UALink 和 token economy。因此，AI 网络、推理和光互连都不是 2026 年才出现的主题。本届更值得追踪的是：prefill 的具体性能条件、MRC 的生产经验、光接口分工，以及异构设备与软件栈如何实现协同。[S04]

| 主题 | 2026 年新增或强化的证据 | 相对于会前的变化性质 | 判断及置信度 |
|---|---|---|---|
| 多域 AI 网络 | Meta、NVIDIA、Ciena 三场 keynote 分别从运营、平台与光传输切入 | 从分类讨论推进到跨域协同设计；不是物理边界消失 | 架构要求强化，高；具体收益依赖部署 |
| MRC、多平面与可靠性 | 协议论文进入本届；已有会前生产系统论文 | 生产经验和开放规范结合；不是会中首次商用 | 本次采用证据最强的方向之一，高 |
| 高基数光互连 | prefill 论文与单跳 MoE 交换主题 | 从训练叙事扩展到推理工作负载、计算域边界 | 技术相关性高；规模经济中低 |
| XPO / Open CPX / OCI / SDM4 | 四项 MSA 同台，叠加 XPO 热点演示 | OFC 发布后的设计、生态与接口跟踪 | 标准化方向明确；认证和量产仍分层 |
| 共享内存 | Marvell 从 Photonic Fabric 走向内存模块、NIC、chiplet 产品组合 | FMS 发布后的架构解释与导入准备 | 产品边界更清楚；部署量未知 |
| 通信软件与可观测性 | NVSHMEM、DODOCO、MTIA HCCL、Omnistat/Cassini 主题 | 优化关注点下沉到工作负载、运行时和故障定位 | 可形成近期效率改善；独立收入池不明 |
| UALink + UCIe | 联合 chiplet 教程 | 4 月规范发布后的工程教育与生态建设 | 规范进展高；互操作商用不能据教程推定 |

主题与议程见 [S01]；三个 keynote 的原始摘要见 [S05][S06][S08]。表内“变化性质”为本报告比较判断。

### 2. 三种规模扩展应共同设计，但不能共用同一性能假设

Meta 官方摘要将 Prometheus 的网络建设经验、季度技术引入、性能、容量迁移与灵活性放在一起，并主张将 scale-up、scale-out、scale-across 整体考虑。这支持“客户采购越来越受整机群交付条件约束”，尚不能推出某家供应商已拿到某比例采购份额。[S05]

本报告使用以下工程边界：scale-up 着重紧耦合计算域，scale-out 着重集群横向扩展，scale-across 着重跨地点协同。它们有共同的拥塞、抖动、故障恢复问题，但距离、同步频率、通信语义和故障域不同。Ciena 摘要所述 IMDD 与相干光的边界变化，是值得测试的产品方向；不是“所有短距离链路都要相干化”。[S08]

### 3. 会前—会中—会后的时间归属

| 时间 | 可核验事件 | 归属与用途 |
|---|---|---|
| 2025-08，上一届 | 已讨论 CPO、MoE 训练、光内存池及开放互连 | 外部历史对照，不是项目旧结论 |
| 2026-01-27；03-31 | Corning—Meta 协议；扩产开工 | 需求/供给背景，不是本届新订单 |
| 2026-03-11 至 03-13 | OCI v1.0、XPO、Open CPX、SDM4 相关发布 | 本届 MSA 讨论的既有基础 |
| 2026-04-07 | UALink 新规范组合批准 | 本届教程之前的标准进展 |
| 2026-05 至 06 月 | MRC 公开与协议/系统论文 | 会前已经有采用与技术证据 |
| 2026-07-21 | NVIDIA Spectrum-6 产品及采用方陈述 | 会前平台进展 |
| 2026-08-04 | Marvell 光共享内存产品组合发布 | FMS 事件，不能写成 HotI 首发 |
| 2026-08-19 至 21 | HotI 技术议程及教程 | 本届会议范围 |
| 2026-08-21 至 24 | 多家会后报道 | 实际演讲线索，需原文交叉验证 |
| 2026-08-26；09-03 | NVIDIA 财报；Ciena 财报 | 会后公司证据，不能反推会议导致收入 |
| 2026-09-01 | 光子 prefill 论文 v1 公开 | 截止日前可取得的会后技术材料 |

以上事件分别见 [S04][S17][S18][S19][S22][S24][S10][S11][S25][S28][S30][S32][S33][S34][S39][S41]。

## 产品和技术路线

### 1. MRC：从容忍丢包到容忍故障，重点是有效训练时间

**机制与成熟度。** MRC 扩展 RoCEv2 RC，以逐包多路径、选择性确认/重传和端点反馈改善负载分配及恢复；目前的数据操作聚焦 Write 与 Write-with-Immediate。协议中的源路由、多平面和若干恢复特性有可选项，所以“支持 MRC”不等于所有 NIC 功能相同，也不等于必须采用一种 SRv6 方案。[S10]

**可复核性能条件。** 2026-05-05 配套系统论文的 Cluster B 为 GB200、CX-8 800G、Spectrum 5、两层 8×100G 多平面：32 KB、4 QP 的 `ib_write_bw` 约 770 Gb/s；2 B、1 QP 的 `ib_write_lat` 在本地 T0 为 5.09 μs、跨 T1 为 6.54 μs。生产案例中，5 万 GPU 作业遭遇光模块抖动时约降速 25%，随后恢复，作业未崩溃。论文承认没有大型 MRC/RoCE 同集群直接对照。[S11]

**采用边界。** Microsoft 已公开说明 Fairwater 的网络建设使用 MRC 与多平面协同设计；AMD 也发布了生产实现相关材料。这是运营方和供应商一手披露，强于仅列出合作伙伴 logo，但仍不等于跨所有工作负载的独立复现。[S12][S13]

**J：价值机制。** 真正的收益由减少中断、减轻长尾、降低无效重跑带来。客户愿付价格应与避免损失的 GPU 小时相关，而不是只与网卡峰值带宽相关。网络控制器、NIC、交换 ASIC、诊断工具和通信库需要一起验证。若应用依赖读取或原子操作，需要检查上层如何适配，不能把 MRC 直接当作所有 HPC/推理协议的替代。

**采用时点。** 特定生产训练已发生；其他客户需要按 NIC 固件、交换机功能、通信库适配、混合流量及故障注入测试推进。没有公开证据支持统一的“几个月完成迁移”。

### 2. 高基数光互连：计算域边界可能比单通道速率更重要

**T：取得的工作。** 9 月 1 日公开的 Lightmatter prefill 论文用 XLA 成本模型分析三类 MoE 与 1K–1M 上下文；在通信受限配置中报告 2.8–5.8 倍改善。关键假设包括理想的 4 倍 scale-up 带宽、更大计算域；作者明确排除了新增链路延迟、热与信号完整性、部署成本和完整 TCO，且未以部署光子硬件验证。decode 饱和还会限制端到端收益。[S14]

**V：硬件阶段。** Lightmatter 6 月 2 日材料称多代硅片正在其验证数据中心运行；其产品页定位为评估套件送样及 early-access 合作。加入 NVLink Fusion 是生态进展，不等于已有可披露规模收入。产品页未注明最后更新时间，本文仅把它作为 9 月 5 日可见状态。[S35][S36]

**J：为什么重要。** 如果一项任务原本被迫跨入低带宽 scale-out 网络，扩大 scale-up 域可能避免性能台阶式下降；若任务本身由计算或内存限制，网络提升就可能只产生小收益。因此要按模型、精度、batch、上下文和并行策略判断，不能直接将最佳倍率套到所有 token。

**必须核验的条件。** 客户测试应包含：真实模型与真实请求分布、相同精度和质量、相同加速器数量或明确的资源差异、光电完整链路功耗、prefill 与 decode 合并后的 p99、故障下退化及全年运维成本。光子链路样品存在与论文假想系统被验证，是两件事。

**时间尺度。** 当前处于硬件评估/集成与应用系统验证交叠阶段；大规模采用取决于整机设计锁定、封装和光纤装配良率、激光供给、维修方式及应用收益。公开资料不足以确定统一量产日期。

### 3. 光接口路线：先辨认协议层、物理层与封装位置

| 路线 | 已核验参数/定位与材料日期 | 成熟度证据 | 关键障碍及价值位置 |
|---|---|---|---|
| OCI | v1.0，2026-03-11；每方向 4×53.125 Gbaud NRZ，承载 212.5 Gb/s 线速；单纤双向、不同波长组 | 有可下载 PHY 规范；不是规模部署证明 | 波长/热稳定、激光、微环与耦合、管理和链路恢复；价值在光引擎、激光、封装和系统设计 |
| XPO | 2026-03-12 公布 12.8 Tb/s、64 通道、每 OCP rack unit 204.8 Tb/s、冷板能力最高 400 W | MSA、演示与参考设计；本次未取得客户验收数量 | 电连接、冷板与运维协同；模块、连接器与系统厂商共同捕获价值 |
| Open CPX | 2026-03 组建；Ciena 05-07 材料说明 32×200G、6.4T 插接式引擎，12.8T/448G 属路线图 | 多厂商展示、接口规范推进 | 接近 ASIC 的电通道与可更换性取舍；插座、引擎、散热、测试 |
| SDM4 MCF | 2026-03-11 合作公告：四芯、O-band、短距/园区无源连接 | 规范制定及生态开发；初版发布/全面互通本次未确认 | 串扰、连接旋转对准、熔接与扇入扇出、安装维护；光纤及配套工艺 |

参数来源：[S17][S18][S19][S20][S22]。表中障碍与价值位置为本报告工程判断。

#### OCI：慢而宽不意味着无 FEC 或无训练开销

OCI 的 200G 名称与 212.5 Gb/s 线速口径必须区分。其规范还包括 deskew、管理与诊断，并在光学测试条件中使用 pre-FEC BER 门限；不能从“NRZ”推出整条链路没有纠错或初始化开销。[S17]

**J：经济方向。** 单纤双向与多波长提高每根纤维承载量，可以缓解布线密度压力；但波长控制、外置激光、耦合和维修的新增成本需要计入。物理接口开放不保证上层加速器协议和软件自动互通，也不保证某家参与者获得独占订单。

#### XPO：散热能力、模块功耗、链路能效必须分开

会前 TeraHop 和 Linktel 已有 12.8T XPO 展示公告；LUXIC 的 3 月 24 日材料还报告另一套 XPO-LPO 回环展示使用其 113 GBaud driver。它们证明生态和演示基础，不能自动验证本届 LRO 模块的全部参数。[S23][S47][S48]

**L：待验证演示线索。** Semiconductor Engineering 8 月 21 日转述本届 64 通道、每通道约 212 Gb/s、约 130 W，以及满足相关 IEEE 要求的表述。因未取得原始测试全文，本报告不将这些标成独立认证结果。[S40]

**E：只做算术校验。** 若 130 W 确为完整模块电功耗，以 12.8 Tb/s 单方向额定容量作分母，得到约 **10.2 pJ/bit**；若使用全双工合计吞吐，分母会翻倍。两种记账方式不能与仅 PIC+laser、包含 host SerDes、或整机插座功耗的数字直接比较。400 W 是散热设计能力，也不能代入实际能耗。

**J：放量门槛。** 需要确认 64 通道同时工作的持续 BER、距离、模式、冷热条件、流量和持续时间，以及连接器寿命、冷板服务流程、整机认证和保修责任。LRO/LPO 的省电收益可能把更高要求转移给 host 电通道，不能只看模块端节省。

#### Open CPX 与 SDM4：可维护性和基础设施密度也是技术变量

Open CPX 试图在靠近 ASIC 的位置保留插接和多源供应；它可能扩大传统模块公司的能力边界，也可能把一部分价值转移给连接器、光引擎和系统验证供应商。SDM4 则主要改变每根物理光纤内的通道数量，不直接提高每个光电端口的速率。

**E：密度不等于收入。** 在相同通道数、长度和利用率条件下，四芯相对单芯最多可把物理纤维根数降为约四分之一；实际光缆、连接器、冗余及施工成本不会自动按同一比例下降。它可能缓解缺纤问题，同时降低单位带宽消耗的纤维数量，因此不能简单推导“光纤厂商收入乘四”。

### 4. Marvell 光共享内存：新增中间内存层，不是直接替代全部 HBM

**F/V：产品边界。** 8 月 4 日新闻稿列出 Photonic Fabric memory module、NIC、chiplet，目标为多机架 warm KV cache，共享容量最高 32 TB，并宣称相同机房空间和功率约束下 token 吞吐最多提高 2–3 倍。该新闻稿没有给出该光内存组合的明确量产日期；其中 Q4 2026 送样日期指 Bravera SC6 SSD 控制器。[S25]

同日 Ravi Mahatme 技术博客列出每 PFMM 最多 8 条 DDR5 DIMM、72 GB HBM cache、7.2 Tb/s 光带宽，PF-NIC 使用 CXL 3.1/PCIe 6；文字写跨机架 30 米与小于 350 ns 访问延迟。新闻稿则写最远 50 米。这是应保留的口径差异，不能擅自解释为同一条件。[S26]

**J：采用机制。** 收益取决于 warm KV 的重用率和迁移策略：若共享缓存减少重新 prefill 或昂贵存储访问，就可能提高 GPU 利用率；若命中率低、传输粒度太小或尾延迟高，共享层可能成为新的堵点。保留 HBM cache 也说明这里是层次扩展，不是取消 HBM。

**E：延迟物理校验。** 仅为判断口径，假设普通光纤传播约 5 ns/m，则 30 米单程约 150 ns、50 米单程约 250 ns；一次往返分别约 300/500 ns，尚未加入控制器和 DRAM。故必须询清“小于 350 ns”是否为完整 load-to-use、缓存命中、附加开销、单向路径或较短距离测试。此推导不判定厂商数据错误，只证明这些指标不能无条件拼接。

**时间与收入边界。** Marvell 2 月 2 日收购完成公告曾指引 Celestial 初始收入于 FY2028 下半年开始，FY2028 Q4 达年化 5 亿美元，FY2029 Q4 达年化 10 亿美元。它是当时前瞻指引，并非 2026 年已实现收入；年化 run rate 也不等于整个财年收入。该节点后续必须用最新财报更新，不能仅凭 8 月产品发布判定提前兑现。[S27]

Marvell 财年在最接近 1 月 31 日的星期六结束，因此 FY2028 下半年大致对应自然年 **2027 年下半年至 2028 年 1 月附近**，不能误读为自然年 2028 年下半年；这里的自然年换算为按财年规则推算的近似范围。[S58]

### 5. 通信库、专家路由和诊断：可能比下一代器件更早影响利用率

**DODOCO。** 采用 2026-07-17 的 v2 作者稿。五类 MoE、六类数据条件及 H100 expert-parallelism 扫描显示：模拟 token 对路由不均衡的高估最高约 2.35 倍，且增加 EP 不会显著消除每个专家的固有负载集中。其结论针对所测模型与数据，不是所有 MoE 的定律。[S15]

**NVSHMEM。** 6 月公开研究解释对称内存、GPU 发起的单边通信及 device-side collective，并用 DeepEP 作为案例；这是通信运行时研究，不是新光器件交付。部署评价需要绑定 NVSHMEM、GPU、NIC、传输路径和算子版本。[S16]

**MTIA。** Meta 官方摘要说明 HCCL 与 PyTorch 集成，通过卸载、计算通信重叠、kernel 融合降低通信成本，并说明 MTIA scale-up/out 使用 Ethernet。这能支持客户正在联合设计通信栈，不能从摘要推导具体模型吞吐、MTIA 出货规模或某款交换芯片份额。[S09]

**J：产业含义。** 运营平台与运行时软件有机会通过调度、故障恢复和应用优化保留系统价值。开源规范会降低部分接口壁垒，但不必然压低拥有完整验证和运维能力的系统供应商利润。对外部工具公司而言，关键是能否把观测结果转化为可执行修复，而非单纯增加遥测数据。

### 6. UALink、UCIe 与专用 SerDes：标准边界收敛仍需硅片验证

UALink 4 月 7 日规范组合包含 Common 2.0、200G DL/PL 2.0、Manageability 1.0、Chiplet 1.0；本届 UALink/UCIe 联合教程是将这些接口向工程集成推进。规范批准、IP 可用、硅片流片、互操作、系统验收与收入是六个不同节点。[S02][S24]

Eliyan 官方演讲摘要强调为 AI 设计的 224G PAM4 SerDes 和适当电传输距离；Qualcomm 摘要讨论 chiplet/CPO 及 direct-drive、digital-drive 的取舍。二者未提供足以核验新产品量产或本届客户订单的材料。[S37][S38]

配套验证已经有产品边界：Keysight 2 月发布 UALink 200G 接收端一致性测试等方案。但这只证明工具供给，不证明所有 UALink 产品已完成认证。Astera Labs 的 Computex PCIe 6 LPO 演示是另一个技术路径：其 50 米演示不能被改写为 UALink 大规模部署。[S49][S50]

### 7. 九项技术论文/热点的取证台账

以下以官网议程中的九个条目为全集；缩写标题仅用于定位，不暗示已读到所有全文。[S01]

| 论文/热点方向 | 取得的一手材料 | 允许形成的结论 | 尚缺材料 |
|---|---|---|---|
| Multipass Random Leaf-Spine | 议程题名 | 本届讨论极大规模网络拓扑 | 全文、配置、流量、成本对照 |
| High-Radix Photonic Prefill | 09-01 arXiv v1 | 条件化的建模收益和限制 | 部署硬件的真实服务验证 |
| 12.8T XPO LRO Demonstration | 议程题名；会前 XPO 厂商材料 | 有对应热点演示安排与生态基础 | 本届原始测试全文、距离/温度/BER |
| Petabit-Class Single-Hop MoE Switching | 议程题名 | 将单跳域与 MoE 训练结合的研究问题 | 原文、真实芯片/仿真边界；不能根据题名认定 Pbit ASIC 出货 |
| MRC Transport | 06-16 arXiv；配套系统论文 | 协议机制及特定生产部署 | 本届最终版变化、更多客户互操作 |
| Omnistat / Cassini Telemetry | 议程题名 | 本届包含隐藏互连瓶颈诊断 | 全文、数据和工具复现说明 |
| DODOCO Dispatch | 07-17 arXiv v2；作者机构论文记录 | 对 benchmark 输入与路由集中度的条件性纠偏 | 更大生产模型的外部复现 |
| Long-Haul RDMA Federated Learning | 议程及作者 SR-APPFL 出版目录；目录的 Paper 标签未取得可用正文链接 | 本届存在真实长距 RDMA 联邦学习研究 | 距离、RTT、带宽、模型、隐私/同步配置；不推导跨洲同步训练效率 |
| NVSHMEM Analysis | 06-04 arXiv v1 | 对称内存与 GPU 直接通信的系统分析 | 最新版本对比、客户应用级收益 |

补充作者出处见 [S14][S15][S16][S46][S51]。没有用同名异年或其他会议的 Pbit 光网络成果替代缺失论文。

## 商业采用与价值捕获

### 1. 可核验的商业锚点及其边界

| 商业证据 | 金额/指标、期间及发布日期 | 可以验证什么 | 不能验证什么 |
|---|---|---|---|
| Corning—Meta | 2026-01-27：多年、最高 **60 亿美元**；03-31 开工，Meta 04-14 确认锚定客户角色 | 客户采购承诺、供给建设已具体化 | 不能全部算当年收入；不能归为 SDM4 或 CPO 专项订单 |
| NVIDIA—Corning | 2026-05-06：美国光连接产能计划扩大至 10 倍，美国光纤产能增加超过 50% | 商业/技术合作与扩产方向 | 不是全球产能增幅，非已经全部投产，未证明所有产品缺货 |
| Ciena 财报 | 2026-09-03 发布；季度截至 08-01，营收 **16.711 亿美元**、同比 **37.0%**；GAAP 毛利率 **45.4%**，调整后 **46.4%** | 公司层面的增长与盈利兑现 | 不是 AI 光互连行业 TAM，也不是 CPX 新品毛利率 |
| NVIDIA 产品/财报披露 | 07-21 说明 Spectrum-6 为 102.4T，支持 pluggable/CPO；08-26 财报继续披露平台推进 | 有产品、采用方和公司披露的交叉支撑 | 未披露的 CPO 独立收入、单客户台数和验收不能补填 |
| Marvell / Celestial 前瞻指引 | 02-02：FY2028 Q4 年化 5 亿美元，FY2029 Q4 年化 10 亿美元 | 可用于未来兑现审计的公司目标 | 不能当作 2026 市场规模或当年订单 |

来源：[S27][S28][S29][S30][S31][S32][S33][S34][S56]。Ciena 的会后财报覆盖期间早于本届会议，增长不能归因于参会。

**供应链判断。** 客户承诺与开工比“供应紧张”口号更有信息量；但从已取得材料尚无法确认 XPO、OCI、SDM4、PFMM 各自的产量、良率、ASP、交期及订单覆盖。不能从总光连接扩产推算某一工艺的供需缺口。激光、封装或连接器可能成为瓶颈，需要逐产品 BOM 与工艺路线确认。

### 2. 当前市场规模：明确哪些美元边界已知，哪些未知

截至截止日，本报告**没有形成可可靠相加的“2026 AI 互连总市场规模”**。交换系统、NIC、光模块、光引擎、激光、光纤和测试设备之间有上下游重复计价；scale-up 与 scale-out 的端口口径也不一致。用公司整体营收、融资估值或多年供货上限拼接，会造成虚假精度。

| 方向 | 当前美元口径 | 未来估算条件 | 置信度 |
|---|---|---|---|
| 成熟光网络系统 | Ciena 已披露单季度营收可作供应商规模锚点，不能代表行业总量 | 需要同行分部、客户类别及 AI 暴露的统一口径 | 财务事实高；行业外推低 |
| XPO、OCI、Open CPX、SDM4 | 新接口专属已实现收入未单列，当前规模未知；未知不等于零 | 客户验收端口×每端口/模块单价，扣除被替代产品与上下游重复 | 低，暂不提供强制美元 TAM |
| 光共享内存 | 产品专属营收与量未知；存在较远期公司指引 | 内存 appliance 数×PFMM/NIC 配置×厂商收入单价；需缓存命中和客户验证支撑 | 低至中，按目标审计 |
| 通信库/协议软件 | MRC、NVSHMEM 不能按许可单价直接形成市场 | 价值可能体现在 NIC/系统溢价、服务、云平台利用率 | 机制中；单独利润池未知 |

要扩大规模估计，优先补齐**实际发货数量、单价和收入确认边界**，而不是为每篇学术论文设置美元规模。以上处理不影响对技术采用条件进行比较。

### 3. 单位经济性：可计算的部分与不能偷换的部分

**E：可插拔 DSP 的成本/功率压力。** Ciena 2026-05-07 的厂商估算使用每颗 1.6T DSP 约 15 W、量产价格约 75 美元。以 64 个模块为例，仅 DSP 为约 **960 W、4,800 美元**；若按 30% 加价为约 **6,240 美元**。这只是其模型中的 DSP 部分，价格是预测，不是已获取采购报价；30% 加价也不是 30% 毛利率。[S20]

这个算式说明消除或简化重定时器为何有吸引力，但不能将 960 W 全部视为 CPO 的整机净节省。激光、冷却、host SerDes、封装、冗余和维修会抵消一部分收益。若最终用电价、PUE 和利用率估算电费，必须另行声明当地条件，本报告不虚设实际客户电价。

**E：性能改善的经济传导。** 若基准总作业时间中只有比例 `f` 能被新网络加速，网络部分提高 `r` 倍，则理想总加速为 `1 / [(1-f)+f/r]`。示例取 `f=30%`、`r=3`，总加速仅 **1.25 倍**；取 `f=70%`，才约 **1.875 倍**。这是敏感性示例，不是测得的行业参数；新增故障或排队会进一步削弱收益。

**E：可靠性的美元边界。** 年度避免损失可写为“受影响 GPU 数×减少的停顿/重跑小时×有效 GPU 小时成本”。MRC 的收入机会和客户愿付价，应建立在此类测量上；本次未取得同一客户的 GPU 小时成本、作业失败分布和净节约数据，因此不填美元回报率。

### 4. 利润率方向与价值捕获

| 环节 | 更可能赚钱的机制（J） | 利润改善条件 | 利润受压/反证 |
|---|---|---|---|
| 交换 ASIC、NIC、系统平台 | 协议实现、拥塞/故障控制、整机验证、软件集成 | 高利用率得到客户验证，设计锁定和系统价值可收费 | 开放接口、多源采购、客户自研扩大议价 |
| 光引擎、激光、封装 | 功率密度、波长稳定、耦合和装配良率 | 可重复的量产工艺，较高测试通过率 | 路线改变、激光/封装成本超预期、返修成本高 |
| 光模块 | 可维护性、现有采购和服务能力 | XPO/CPX 帮助模块商延伸到新外形 | 大客户直接采购引擎；成熟模块价格下降 |
| 光纤/连接器 | 密度、安装、低损耗、扩产兑现 | 新规格和工程复杂度形成差异化，客户锁量 | 每 bit 用纤下降，扩产过快，规格未定导致返工 |
| 测试/认证 | 多标准和多厂商互通增加验证需求 | 工具复用、自动化与量产测试渗透 | 研发测试与量产测试不连续；标准冻结慢 |
| 客户侧平台 | 提高有效算力、压缩采购溢价与降低运维成本 | 具备联合设计、调度与自研运维能力 | 集成复杂性和维护人力吞噬收益 |

除上表 Ciena 公司级毛利率外，本次不为 XPO、OCI、PFMM、SDM4 等方向填写无披露基础的产品毛利率。即使行业需求增长，标准化与规模良率改善也可能使每 bit 单价下降；利润取决于谁承担风险、谁控制客户验收和最终集成。

## 开放洞见与重要分歧

### 1. 网络问题需要区分“搬运不够快”与“模型分配不均”

高基数光互连解决带宽/域边界问题，DODOCO 指出部分专家热点源自模型路由，两者可以同时成立。不能用后一项证明网络没有价值，也不能用前一项证明增加网络即可消除所有长尾。可证伪测试是：使用相同真实路由 trace，分别增加网络带宽、改变专家布局、改变路由策略，再比较 p99 和有效 token/s。[S14][S15]

### 2. 对光互连最有价值的比较单位可能是“完成同一任务的系统”

本报告判断：跨机架可达性、扩大计算域、改善容错可能比局部 pJ/bit 更能改变客户经济性。相反，仅以最佳光引擎功耗比较含 host 与冷却的电系统，会系统性高估替代价值。建议比较相同 SLO、模型质量和有效输出量下的整机功耗、空间、成本及失败恢复时间。

### 3. “光子产品就绪”与“论文系统被验证”可以同时一真一未知

Lightmatter 可提供评估硬件，但 prefill 论文中的理想系统仍待部署验证；Marvell 可发布内存产品组合，但客户验收、规模交付与收入仍有后续节点。术语“production-ready”“available to partners”不应被翻译成“已量产放量”。[S14][S25][S35][S36]

### 4. 不支持“CPO 已证明所有 pluggable 即将退出”的强结论

可核验的对照包括：NVIDIA Spectrum-6 明确支持两类外形；Ciena 5 月材料引用的 LightCounting 预测是在特定高速端口口径下、约 2031 年 CPO 超过可插拔，属于预测而非现状。多路线竞争可以由公开供应商材料证实；“资本市场已经错误定价”则未得到验证。[S20][S33]

### 5. 更大模块可能改变故障相关性

**J：待验证推论。** XPO 等高通道密度方案可能减少面板和连接器，但如果更多链路共用一个模块、冷板或激光源，失效影响可能更集中。MRC 的容错能力有助于降低故障代价，却不能替代物理冗余设计。需要把模块失效影响的端口数、恢复流程和多平面分布一起测试，而不是只统计单链路 BER。

### 6. 会议信息本身存在需要降权的细节

- **演讲人版本差异：** Arista 社交预告转发名单中的 Corning 代表为 Duane Robbins，最终官网日程为 Gabe Sudduth；正文采用官网名单，实际发言线索另由会后报道核对。这显示会前预告不能当最终实录。[S01][S42][S41]
- **赞助与研究选择：** 主办方赞助页明确 Diamond 5,000 美元对应 15 分钟、Platinum 3,500 美元对应 10 分钟发言。因此赞助演讲出现频次不能单独当作独立技术排名；这不否定内容，但需要研究或客户证据补强。[S52]
- **算术警示：** Lightmatter 官网演讲摘要同时写算力百万倍、互连千倍与“10,000x gap”，这些文字并不能直接由前两项相除得到。本文不采用此宣传倍率构建市场模型。[S53]

### 7. 非官方与二手线索的使用记录

| 材料 | 日期/类型/置信度 | 线索 | 一手核验情况及处理 |
|---|---|---|---|
| Converge Digest 总结 | 08-21；会议媒体伙伴；中 | 会后活动、材料入口、获奖和实际演讲线索 | 议程结构与官网吻合；人数、获奖和具体演讲参数未全部独立核验，不作商业核心证据 |
| Semiconductor Engineering | 08-21；媒体；中 | XPO 约 130 W | 12.8T/64 通道主题得到议程支持；功耗、完整测试条件尚待原文 |
| HPCwire 光互连报道 | 08-24；媒体；中 | CPX 与 MCF 的实际讲解、服务性争论 | MSA 目标有公司/联盟公告；现场数值及成员数量不用于收入估计 |
| LightCounting 跨会议短评 | 09-03；二手研究；中 | 当月 AI 互连讨论延伸到 Hot Chips/OCP/SIGCOMM | 用于发现线索，不能将其他会议芯片发布并入 HotI |
| Arista LinkedIn 预告 | 页面相对日期，不把它转换为精确发布日期；公司社交材料；中 | 四项 MSA 与会前讲者名单 | 以官网校准；属于宣传/议程，不是实际发言证明 |
| T.I.L 个人技术笔记 | 2026-08-01 发布、09-02 更新；个人分享；低至中 | MRC 的功能与限制阅读笔记 | MRC 原论文可验证若干机制；没有足够证据称其作者实际参会，不作参会纪要 |

来源：[S39][S40][S41][S43][S42][S54]。未将匿名供应链数字、无法追溯的券商截图或社交平台估值叙事转成核心结论。

## 公司和产业链映射

以下为技术位置与证据映射，不是股票推荐或收益排序。公司级实际收入暴露应与特定新技术暴露区分。

| 公司/组织 | 位置与本届关联 | 已见业务/技术证据 | 采用条件与容易误判之处 |
|---|---|---|---|
| NVIDIA | keynote；NIC、交换、NVLink、运行时 | MRC 实现、Spectrum-6、NVSHMEM；产品/财报材料 | 平台能力强不等于 CPO 收入已单列；不同外形可并存 |
| Broadcom | 赞助演讲；交换与 NIC | MRC 作者/实现参与、Ethernet 路线 | 具体芯片型号和客户份额须另取产品/订单证据 |
| AMD | MRC、UALink/UCIe 教程、GPU 通信生态 | Pollara MRC 及规范贡献 | GPU 总收入不能等同开放互连收入 |
| Intel | UALink/UCIe 教程、MRC 合作者 | 规范与协议参与 | 参与标准并非出货/客户中标 |
| Meta | keynote、MTIA、OCI | HCCL/网络联合设计；Corning 采购与扩产合作 | 更像客户与架构影响者；外部供应商不能无依据认领其全部 capex |
| Microsoft、OpenAI | MRC 运营/研究与 OCI 生态 | 生产系统论文、运营方披露 | 价值可留在客户利用率；不能由论文推导未公开采购价 |
| Arista | XPO、MSA 与热点演示 | 12.8T XPO 公告；系统设计/可插拔路线 | 模块由生态公司供应，系统营收不等于自产光器件收入 |
| Ciena | keynote、CPX、相干/光网络 | Vesta 200 相关材料及季度财报 | 现有光网络增长不能全部归功于 CPX；公司毛利不代表新引擎毛利 |
| Marvell / Celestial AI | 光共享内存、Photonic Fabric | 收购完成、产品组合、指引 | Celestial 已纳入 Marvell，不能重复计算为两家独立上市受益者 |
| Lightmatter | 光子互连、激光、prefill 论文 | 验证硬件、early access、NVLink Fusion 生态 | 私营公司收入不透明；论文 modeled 不等于客户 realized |
| TeraHop、Linktel | XPO 模块、CPX 引擎及生态 | 会前厂商演示公告 | 技术位置直接，具体新品订单和毛利未披露 |
| Corning、AFL、Sumitomo Electric | SDM4、光纤与连接工艺 | 联盟公告；Corning 另有客户协议与扩产 | 普通光纤收入、MCF 新品收入不可混算；AFL 与母集团不宜重复计数 |
| Coherent、Molex、Samtec | CPX 光引擎/连接器配套 | MSA 发起成员，Ciena 材料涉及多源连接 | 属供应链候选；不能仅凭成员身份判定瓶颈溢价 |
| LUXIC | 高速 driver，小型配套公司线索 | OFC XPO-LPO 回环展示提及其 113 GBaud driver | 不是本届 LRO 供应商验证；客户与收入规模待核 |
| Eliyan | AI 专用 224G SerDes | 本届官方演讲摘要 | 电通道优化可与光配合；未见本届量产订单 |
| Napatech | 可编程网络基础设施 | 本届赞助演讲摘要 | 本次未见对应 AI fabric 规模合同；不能按 sponsor 等级认定收入弹性 |
| Qualcomm | chiplet 与 CPO 演讲 | 架构讨论 | 现有公司收入结构未因一次演讲而变成光互连纯标的 |
| Keysight | 测试/一致性验证配套 | 02-18 UALink 等验证工具发布 | 非本届新品；需跟踪研发测试转量产测试收入 |
| Astera Labs | 邻接的 PCIe 光互连、scale-up 生态 | Computex PCIe 6 LPO 演示 | 明确为外部对照；不把 PCIe 演示当 UALink 验收或本届发布 |

依据：[S09]—[S13][S16][S18]—[S24][S25]—[S38][S47]—[S50][S55]。其中“价值捕获和误判”属于本报告判断。

**“伪受益”识别规则。** 本报告不把没有披露订单的公司直接贴成伪受益者；应降权的是具体论证：只参加 MSA 就认领所有相关市场；只讨论 CPO 就把全公司收入当光互连；用标准会员名单推断客户份额；把行业缺纤映射成任意含材料概念公司的盈利增长。反过来，小公司有 demo 也不等于它没有价值，只是必须先验证可替代性、工艺能力、客户导入和经营规模。

## 风险、反证条件和后续跟踪

### 1. 优先级与刷新条件

| 优先级 | 当前判断 | 会推翻/削弱判断的数据 | 下一步材料与节点 | 建议刷新频率 |
|---|---|---|---|---|
| P0 | MRC 已有生产价值，外推需条件 | 混合流量、多租户或非训练应用下显著退化；适配成本大于恢复收益 | 最新 OCP 规范、NIC 支持矩阵、客户生产实验、故障注入 trace | 每月；规范/产品更新即时 |
| P0 | 光子 prefill 可能受益于扩大计算域 | 同资源真实服务中收益消失；decode/排队吞噬 TTFT 改善 | 原型硬件、真实请求 p99、功耗/价格与故障测试 | 每月；客户结果即时 |
| P0 | PF 共享内存有明确产品边界但指标待统一 | 缓存命中不足、远程访问长尾、软件改造成本过高；量产节点后移 | 澄清 30/50 米、<350 ns 的定义；规格书、客户验收、最新财报指引 | 每季度，重大产品文件即时 |
| P0 | XPO 有现实生态和演示 | 热/电/服务性失败；高通道模块故障代价超出收益 | 本届论文和演讲、完整 BER/距离/温度、客户样品到量产进展 | 每两周检查公开材料，拿到后改月度 |
| P1 | OCI/CPX 有多源化价值 | 可替换机械接口成立但光、电、管理不能跨厂商互通 | 规范版本、互操作报告、参考平台和第二来源客户认证 | 每月 |
| P1 | SDM4 可提高布线密度 | 串扰/接续损耗或施工成本抵消节省；初版持续推迟 | 公开初版、跨厂商连接器与熔接测试、真实园区导入 | 每月 |
| P1 | 客户承诺支持光连接扩产 | 工厂进度延误、取消/延后承诺、ASP 和利用率下降 | Corning/Meta 扩产更新、资本开支和财务披露 | 每季度 |
| P1 | 真实路由 trace 应改变网络评测 | 更广模型复现失败、对生产路由误差无显著影响 | DODOCO 代码/数据及其他模型、通信库版本复现 | 每季度 |
| P2 | UALink 教程反映工程推进 | 标准/测试存在但互通 silicon 或客户设计滞后 | UALink、UCIe、测试商和首批客户公开结果 | 每月 |

### 2. 材料补齐计划

1. **先补会后原始材料。** 建议 2026-09-12、09-19 复查官网议程、2026 论文集和 YouTube；日期是本报告建议检查日，不是主办方承诺。重点补 XPO、单跳 Pbit 交换、Omnistat 和长距 RDMA 四项缺口，以及三场 keynote 原始图表。
2. **再按采购阶段更新。** 样品、客户测试、小批量、量产、规模交付分别要求独立证据；每次更新保留“哪项材料改变了哪条判断”，不能用新 press release 覆盖历史验证不足。
3. **关注后续 OCP、SC、OFC 及公司财报。** 本届 MTIA 摘要已提及 SC26 论文，可在正式公开后复核；本报告未另行核验后续会议确切日期，不补造日程。公司财报以官方实际发布日期为准。
4. **最小验收数据集。** 每条高性能链路至少补全：速率口径、双向/单向、距离、拓扑、端口并发、调制/FEC、BER 前后口径、温度和持续时间、系统/模块功耗边界、负载类型、平均/p99、失败恢复；商业侧补客户、数量、价格、交期和收入确认。

### 3. 本次明确保留的未知

- 未取得全部九项论文的最终全文，未逐段观看 2026 全套录像；实际演讲可能包含摘要外的信息。
- 未确认本届 XPO 的完整原始测试配置，也未取得本届专属采购、验收、价格、毛利率和排产表。
- 未统一 Marvell 光共享内存的距离/延迟定义；不能估算其实际客户 TCO。
- 未取得足以证明 SDM4 最终初版和跨厂商全链路认证完成的材料；Open CPX 官网访问受限，使用发起公司资料补充，不把访问失败解释为规范不存在。
- 非官方参会者分享覆盖有限，找到的个人笔记不等于实际参会证明；未以匿名供应链消息补足商业缺口。
- 没有形成证券估值、未定价机会或全行业一致预期结论；本报告用于后续研究取证和假设更新。

## 来源清单

统一检索日期为 **2026-09-05（America/Los_Angeles）**。网页未给独立发布日期的，写“日期未注明/本次可见”，不把搜索引擎抓取时间当发布日期。可信度针对材料可追溯性；性能、市场预测和交付目标另保留供应商立场。

### 一手官方会议材料

| 编号 | 来源与日期 | 类型、可信度及用途 |
|---|---|---|
| [S01] | HotI 2026 Program；独立发布日期未注明，会议 08-19—21 | 官方，高；日期、安排、九项论文/热点、教程 |
| [S03] | HotI 2026 首页；日期未注明 | 官方，高；会议形式、主题、视频入口 |
| [S04] | HotI 2025 Program；2025 年会议归档 | 官方，高；上一届对照 |
| [S05] | Omar Baldonado keynote 摘要；2026 本届 | 官方发布/运营方陈述，高；Meta 多域协同 |
| [S06] | Gilad Shainer keynote 摘要；2026 本届 | 官方发布/厂商陈述，高；平台方向 |
| [S07] | Ravi Mahatme sponsor talk 摘要；2026 本届 | 官方发布/厂商陈述，高；共享内存 |
| [S08] | Bilal Riaz keynote 摘要；2026 本届 | 官方发布/厂商陈述，高；跨域及光传输 |
| [S09] | Kirtesh Patil MTIA 摘要；2026 本届 | 官方发布/客户技术陈述，高；HCCL/Ethernet |
| [S37] | Eliyan sponsor talk 摘要；2026 本届 | 官方发布，高；224G 专用 SerDes 方向 |
| [S38] | Qualcomm sponsor talk 摘要；2026 本届 | 官方发布，高；chiplet/CPO 方向 |
| [S52] | HotI 2026 Sponsors；日期未注明 | 官方，高；赞助发言的商业边界 |
| [S53] | Lightmatter sponsor talk 摘要；2026 本届 | 官方发布/厂商陈述，高；BiDi DWDM；宣传算术保留 |
| [S55] | Napatech sponsor talk 摘要；2026 本届 | 官方发布，高；可编程基础设施，未含订单 |

### 一手公司、客户与投资者材料

| 编号 | 来源与日期 | 类型、可信度及用途 |
|---|---|---|
| [S12] | Microsoft，Building resilient networks for AI supercomputers；2026-05-06 | 运营方一手，高；MRC/Fairwater |
| [S13] | AMD，Next Gen Networking Transport；2026-05-06 | 厂商一手，高；MRC 实现 |
| [S18] | Arista XPO 发布；2026-03-12 | 新闻稿，高；外形、密度和冷板能力 |
| [S19] | TeraHop，Open CPX 发起公告；页面 2026-03-13 | 公司一手，高；发起人和接口范围 |
| [S20] | Ciena，How open ecosystems will advance CPO adoption；2026-05-07 | 公司博客；事实高、预测中；CPX、DSP 估算与长期迁移 |
| [S23] | TeraHop XPO 展示公告；页面 2026-03-13，稿内 03-12 | 公司一手，高；会前发布归属 |
| [S25] | Marvell AI memory portfolio；2026-08-04 | 新闻稿，高；PF 组合、32 TB/50 米及厂商吞吐陈述 |
| [S26] | Marvell Photonic Fabric 技术博客；2026-08-04 | 演讲者本人公司博客，高；PFMM/NIC、30 米与延迟口径 |
| [S27] | Marvell 完成 Celestial 收购；2026-02-02 | 投资者公告，高；归属与当时前瞻收入目标 |
| [S28] | Corning—Meta 供货协议；2026-01-27 | 投资者公告，高；多年最高金额 |
| [S29] | Meta 对同一协议披露；2026-01-27 | 客户一手，高；采购交叉核验 |
| [S30] | Corning 扩产开工；2026-03-31 | 公司一手，高；实际开工节点 |
| [S31] | NVIDIA—Corning 合作；2026-05-06 | 联合合作公告，高；美国扩产计划 |
| [S32] | Ciena FY2026 Q3 财报；2026-09-03 | 财报，高；营收与 GAAP/调整后利润率 |
| [S33] | NVIDIA Spectrum-6 博客；2026-07-21 | 厂商产品及客户引语，高；102.4T、外形和采用方边界 |
| [S34] | NVIDIA FY2027 Q2 财报；2026-08-26 | 财报，高；会后平台披露，不能等同独立 CPO 收入 |
| [S35] | Lightmatter，Scale-Up is a Problem Made for Photonics；2026-06-02 | 公司博客，高；验证平台和生态，未验证外部规模收入 |
| [S36] | Lightmatter Products；日期未注明，09-05 可见 | 公司产品页，高；送样/early access 状态 |
| [S47] | Linktel OFC 发布；2026-03-17 | 公司新闻稿托管于 OFC 新闻室，高；会前 XPO |
| [S48] | LUXIC OFC recap；2026-03-24 | 配套厂商一手，中高；driver 与回环展示，非本届全套测试 |
| [S49] | Keysight scale-up validation；2026-02-18 | 公司新闻稿，高；测试工具供给 |
| [S50] | Astera Labs Computex PCIe 6 LPO demo；2026 年，正文未注明精确日 | 公司技术博客，中高；邻接技术对照，不是 HotI 新品 |
| [S56] | Meta 扩产合作进度；2026-04-14 | 客户一手，高；开工与锚定客户 |
| [S58] | Marvell 10-Q；2026-05-28，季度截至 05-02 | 监管申报，高；财年日历及收购归属 |

### 标准、联盟、论文与技术一手材料

| 编号 | 来源与日期 | 类型、可信度及用途 |
|---|---|---|
| [S02] | UALink Hot Interconnects 活动页；会议 2026-08-19—21，页面发布日期未注明 | 联盟，高；日期与联合教程 |
| [S10] | The MRC Transport；arXiv 2606.18170v1，2026-06-16 | 协议作者论文，高；必选/可选、语义边界 |
| [S11] | Resilient AI Supercomputer Networking using MRC and SRv6；arXiv 2605.04333v1，2026-05-05 | 生产团队技术论文，高；配置、性能与故障案例 |
| [S14] | Scaling Inference Prefill with High-Radix Photonic Interconnects；2609.01821v1，2026-09-01 | 作者论文，高；建模及局限；实际部署外推有限 |
| [S15] | DODOCO；2605.20982v2，2026-07-17；v1 为 05-20 | 作者论文，高；真实/模拟路由对照 |
| [S16] | Demystifying NVSHMEM；2606.05951v1，2026-06-04 | 作者论文，高；运行时机制 |
| [S17] | 200G OCI Optical PHY/Line Interface Specification v1.0；2026-03-11 | MSA 规范，高；线速、波长、训练与测试条件 |
| [S21] | XPO MSA 官网；日期未注明 | 联盟，高；64 lane 外形范围，未取得完整规范 |
| [S22] | Sumitomo Electric 等 SDM4 发起公告；2026-03-11 | 发起公司共同公告，高；四芯、O-band、拟定规范 |
| [S24] | UALink 规范批准公告；2026-04-07 | 联盟，高；四项规范版本 |
| [S46] | SR-APPFL Publications；页面日期未注明，2026 论文条目 | 作者项目目录，高；长距 RDMA 论文存在，未取得全文 |
| [S51] | FAU CRIS DODOCO 论文记录；2026 年 | 作者机构，高；HotI 论文归属与 DOI |

### 非官方分享、二手报道与研究

| 编号 | 来源与日期 | 类型、可信度及是否一手验证 |
|---|---|---|
| [S39] | Converge Digest HotI 总结；2026-08-21 | 会议媒体伙伴，中；议程已核，现场细节未全部核 |
| [S40] | Semiconductor Engineering 周报；2026-08-21 | 媒体，中；XPO 功耗未由本次原文验证 |
| [S41] | HPCwire，Inside the Next Generation of Optical Interconnects；2026-08-24 | 媒体，中；取得搜索索引正文片段，全文直接抓取超时；MSA 方向有一手支持，现场数值降权 |
| [S42] | Arista LinkedIn MSA 预告；精确发布日期未确认 | 公司社交预告，中；最终名单用官网校准 |
| [S43] | LightCounting，August Conferences Bring the Heat；2026-09-03 | 二手研究，中；跨会议线索，不归并发布 |
| [S54] | T.I.L，OpenAI MRC；2026-08-01，更新 09-02 | 个人分享，低至中；MRC 机制可回原论文，未确认实际参会 |

### 已定位但未完整取得的入口

| 编号 | 入口 | 本次限制 |
|---|---|---|
| [S44] | HotI 2026 论文集入口 | HTTP 401；没有绕过登录，也没有据此声称论文未发表 |
| [S45] | IEEEHOTI 官方 YouTube 频道 | 本次抓取没有取得本届可核验完整清单；未观看全套 |
| [S57] | Open CPX MSA 官网 | 抓取超时；正文用发起公司一手材料，不推断规范不存在 |

[S01]: https://hoti.org/2026/program.html
[S02]: https://ualinkconsortium.org/event/hot-interconnects-2/
[S03]: https://hoti.org/2026/
[S04]: https://hoti.org/2025/program.html
[S05]: https://hoti.org/2026/keynotes-omar.html
[S06]: https://hoti.org/2026/keynotes-gilad.html
[S07]: https://hoti.org/2026/sponsortalk-marvell.html
[S08]: https://hoti.org/2026/keynotes-Bilal.html
[S09]: https://hoti.org/2026/sponsortalk-meta.html
[S10]: https://arxiv.org/html/2606.18170v1
[S11]: https://arxiv.org/html/2605.04333v1
[S12]: https://techcommunity.microsoft.com/blog/azurehighperformancecomputingblog/building-resilient-networks-for-ai-supercomputers/4516919
[S13]: https://www.amd.com/en/blogs/2026/next-gen-networking-transport-for-large-scale-ai-training.html
[S14]: https://arxiv.org/html/2609.01821v1
[S15]: https://arxiv.org/html/2605.20982v2
[S16]: https://arxiv.org/html/2606.05951v1
[S17]: https://oci-msa.org/assets/files/200G-OCI-Optical-Phy-Specification-v1.0.pdf
[S18]: https://www.arista.com/en/company/news/press-release/23697-pr-20260311
[S19]: https://www.terahop.com/newsinfo/147
[S20]: https://www.ciena.com/insights/blog/2026/how-open-ecosystems-advance-cpo-adoption
[S21]: https://www.xpomsa.com/
[S22]: https://sumitomoelectric.com/press/2026/02/prs011
[S23]: https://www.terahop.com/newsinfo/146.html
[S24]: https://ualinkconsortium.org/wp-content/uploads/2026/04/UALink-2.0-Specification-PR_FINAL.pdf
[S25]: https://www.marvell.com/company/newsroom/marvell-ai-memory-infrastructure-agentic-ai-inference.html
[S26]: https://www.marvell.com/blogs/photonic-fabric-technology-optical-connectivity-ai-infrastructure.html
[S27]: https://investor.marvell.com/news-events/press-releases/detail/1005/marvell-completes-acquisition-of-celestial-ai
[S28]: https://investor.corning.com/news-and-events/news/news-details/2026/Corning-and-Meta-Announce-Multiyear-up-to-6-Billion-Agreement-to-Accelerate-US-Data-Center-Buildout/default.aspx
[S29]: https://about.fb.com/news/2026/01/meta-6-billion-agreement-corning-support-us-manufacturing/
[S30]: https://www.corning.com/worldwide/en/about-us/news-events/news-releases/2026/03/corning-and-meta-celebrate-start-of-construction-on-cable-manufacturing-expansion-in-north-carolina-to-support-ai-buildout.html
[S31]: https://nvidianews.nvidia.com/news/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure
[S32]: https://investor.ciena.com/news/news-details/2026/Ciena-Reports-Fiscal-Third-Quarter-2026-Financial-Results/default.aspx
[S33]: https://blogs.nvidia.com/blog/nvidia-spectrum-six-arrives-in-gigascale-ai-factories/
[S34]: https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027
[S35]: https://lightmatter.co/blog/scale-up-is-a-problem-made-for-photonics/
[S36]: https://lightmatter.co/products/
[S37]: https://hoti.org/2026/sponsortalk-eliyan.html
[S38]: https://hoti.org/2026/sponsortalk-qualcomm.html
[S39]: https://convergedigest.com/hot-interconnects-2026-ai-networking-scale-up-scale-out-scale-across/
[S40]: https://semiengineering.com/chip-industry-week-in-review-152/
[S41]: https://www.hpcwire.com/2026/08/24/inside-the-next-generation-of-optical-interconnects/
[S42]: https://www.linkedin.com/posts/arista-networks-inc_make-sure-you-catch-hot-interconnects-2026-activity-7495277496972509184-Ycrg
[S43]: https://mail.lightcounting.com/research-note/september-2026-august-conferences-bring-the-heat-453
[S44]: https://conferences.computer.org/hotipub26/
[S45]: https://www.youtube.com/@IEEEHOTI
[S46]: https://sites.google.com/view/sr-appfl/publications
[S47]: https://ofc.vporoom.com/2026-03-17-Linktel%2C-Founding-Member-of-XPO-MSA%2C-to-Debut-12-8T-Liquid-Cooled-Module-at-OFC-2026
[S48]: https://www.luxictech.com/en/index.php?c=show&id=30
[S49]: https://www.keysight.com/zz/en/about/newsroom/catalog/news-release.2026.0218-pr-026-keysight-introduces-scale-up-validation-solutions-for-ai-data-centers.html
[S50]: https://www.asteralabs.com/resources/blog/computex-2026-demo-how-linear-optics-enables-longer-link-reach-lower-latency-for-scorpio-smart-fabric-switches/
[S51]: https://cris.fau.de/publications/366829352/
[S52]: https://hoti.org/2026/sponsors.html
[S53]: https://hoti.org/2026/sponsortalk-lightmatter.html
[S54]: https://blog.thomarite.uk/index.php/2026/08/01/openai-mrc/
[S55]: https://hoti.org/2026/sponsortalk-napatech.html
[S56]: https://datacenters.atmeta.com/2026/04/investing-in-american-manufacturing-to-build-the-infrastructure-for-ai/
[S57]: https://www.opencpxmsa.org/
[S58]: https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-26-000019/mrvl-20260502.htm
