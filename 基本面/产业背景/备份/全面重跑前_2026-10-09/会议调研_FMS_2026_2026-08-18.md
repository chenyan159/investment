# 会议追踪：FMS 2026

| 项目 | 内容 |
|---|---|
| 会议 | FMS 2026（Future of Memory and Storage） |
| 会议日期 | 2026-08-04 至 2026-08-06 |
| 地点 | 美国加州圣克拉拉，Santa Clara Convention Center 与 Hyatt Regency Santa Clara |
| 材料检索截止日期 | 2026-08-18（美国太平洋时间） |
| 报告完成日期 | 2026-08-18 |
| 研究边界 | 仅使用从外部公开渠道重新检索的一手资料、公司披露、标准组织资料和明确标注的第三方市场数据；未使用项目内既有公司调研、行业调研、会议报告、日度资料、特征量化、缓存或中间结论 |

## 结论摘要

### 核心判断

1. **FMS 2026 的主线不是“更大容量”，而是推理阶段每 token 的数据搬运效率。** 2025 年已经出现 245.76TB QLC SSD、PCIe 6.0、CXL 内存扩展、HBF、GPU Direct Storage 等方向；2026 年真正发生的变化，是评价指标从顺序带宽转到 512B 小块随机 IOPS、尾延迟、IOPS/W、IOPS/美元、KV cache 命中率、GPU 利用率和数据路径安全性。FMS 官方议程也把 inference、KV cache、GPU-direct、CXL、近存/近内存计算和液冷放到同一架构语境中。[FMS 2026 官方议程](https://www.terrapinn.com/conference/future-memory-storage/agenda.stm)（检索：2026-08-18）

2. **企业级 SSD 出现两条彼此互补、而非相互替代的路线。** 第一条是 245.76TB 级 QLC，以最低机架空间、功耗和运维成本承载容量层；第二条是 TLC/XL-FLASH、PCIe 6.0、50 DWPD 和 512B 小块 I/O，以高 IOPS 和低尾延迟承载热 KV cache、向量检索和 GPU 按需读取。把二者合并成一个“SSD ASP”会掩盖利润池分化。

3. **PCIe 6.0 已从 2025 年的预告和奖项阶段进入有限量产，但生态成熟度仍不一致。** Samsung PM1763、Micron 9650 已明确量产；Kioxia CM10、GP1 仍处功能样品或年底送样阶段；Marvell Bravera SC6、Silicon Motion SM8466 等控制器仍是 2026 年第四季度至 2027 年的样品/设计导入节奏。2026 年收入会先集中在少数拥有自研控制器、NAND 与系统验证能力的厂商，而不是平均扩散到全行业。

4. **GPU-direct 数据路径开始成为开放生态，但“开源”边界必须精确。** NVIDIA 公开的是 cuFile APIs 及垂直存储软件栈，并与 Google、Intel、Meta 组成初始维护者；Storage-Next 已有 40 多家参与方。SCADA 则是让 GPU 从 SSD 选择性拉取数据到 HBM 的架构，DDN 宣布集成，但截至检索截止日，不能据此写成“完整 SCADA 已开源且大规模客户部署”。[NVIDIA FMS 2026 官方博客](https://blogs.nvidia.com/blog/ai-storage-fms/)（2026-08-04）

5. **CXL 的现实进展高度不对称。** Meta Vistara 证明了定制化 CXL 内存扩展可在数百万台生产服务器落地，并称可使内存容量受限的分离式推理服务器减少最多 25%；但开放、可组合的商用 CXL pooling 和 CXL flash 仍主要处于演示、功能样品或生态验证阶段。近一年最可能形成收入的是内存扩展控制器、交换/重定时器和整机适配，而不是跨机架共享内存池。

6. **HBM 的紧缺与价值量继续上升，但 HBF、zHBM 和 zNAND-O 不能计入未来十二个月基准收入。** Samsung、SK hynix、Micron 均已披露 HBM4 量产/商业出货；HBM4E 已进入样品阶段。HBF 在 2026 年取得的实质进展是 SK hynix 与 Sandisk 发布开放规范，尚无商业硅片、量产控制器或公开客户部署。Samsung zHBM、zNAND-O 是概念模型；“8 倍 HBM5 性能”等数字属于厂商目标，不是可订货产品规格。

7. **液冷、控制器固件和安全隔离从配套项变成性能上限。** 28GB/s 级 PCIe 6.0 SSD、高并发小 I/O 与 GPU 直连会把热密度、写放大、QoS、ECC、地址映射权限和故障域同时推到前台。受益的不只有 NAND 厂商，还包括控制器、PCIe/CXL 交换与重定时、DPU、液冷部件、数据放置软件和多协议存储系统。

8. **供给周期没有被 AI 消灭，只是合同结构和产品组合改变了波动。** TrendForce 在 2026-07-21 仍预计 2026 年 NAND 供给缺口 4%–5%，但预计 2027 年供给转为高于需求、尤其下半年缓和；Sandisk 则在 2026-08 的投资者材料中给出更激进的 2027 年约 5,000 亿美元 NAND 市场判断。两者可以同时对应“受约束的高价牛市”和“新增供给后的价格回落”两种路径，不能把长期采购协议直接解释为价格周期永久消失。

9. **基准情景下，未来一年最大的绝对利润池仍是 NAND 与 HBM，不是 CXL。** 本报告估算 2026 年 NAND 收入约 2,706 亿美元、HBM 约 490 亿美元、外部企业存储系统约 411 亿美元；2027 年基准情景分别为约 3,794 亿、686 亿和 433 亿美元。狭义 CXL 内存连接器件市场虽可能从约 0.99 亿增至 3.01 亿美元、增速最高，但绝对规模仍小。各层市场相互包含，严禁简单相加。

10. **股票研究上应买“已验证的瓶颈价值量”，而不是所有带 AI 标签的路线图。** 未来 3 个月优先验证 NAND/eSSD 合同价、PCIe 6.0 量产收入、HBM4 良率与液冷附着率；未来 1 年验证 Storage-Next/SCADA 的非厂商生产部署、CXL 商用收入、HBF 首颗硅片和 375 层 NAND 量产；未来 2 年再判断 HBF、zHBM、CXL pooling 是否能成为独立利润池。

### 一句话投资框架

**先赚紧缺和量产的钱（HBM4、PCIe 6.0 eSSD、245TB QLC），再赚架构复杂度的钱（控制器、交换/重定时、DPU、液冷、软件），最后才给尚无硅片与客户的 HBF、zHBM、zNAND-O 估值。**

## 研究方法、证据等级与口径

### 事实、估算和观点的分离

- **事实**：来自 FMS 官方、公司新闻稿/产品页/财报、标准组织、论文或客户部署材料；正文尽量给出发布日期。厂商性能数字仍是“厂商披露事实”，不等于独立测试结论。
- **估算**：由公开收入、bit 出货、价格或单位价值量推导，统一以名义美元计；公式和关键假设在“市场规模和利润池”中列出。
- **观点**：本报告对产业节奏、竞争格局、股票映射和反共识方向的判断；均附带可证伪指标。

### 证据与成熟度标记

| 标记 | 定义 | 可否计入未来十二个月基准收入 |
|---|---|---|
| P：量产/商业出货 | 公司明确写明 mass production、high-volume production、commercial shipment 或 now shipping | 可以，但仍需验证收入占比和客户集中度 |
| D：生产部署/平台可用 | 有生产服务器、客户平台、公开代码或已上市系统支撑 | 可以按实际采用率计入 |
| S：样品/客户验证 | evaluation sample、functional sample、engineering sample、qualification | 仅按小额样品和设计导入计入 |
| R：路线图/开放规范 | 有明确目标和时间表，但未见商业硅片或量产 | 不计入基准收入，作为期权 |
| C：概念展示 | 模型、概念规格、未给出量产时间和客户 | 不计入收入 |

### 置信度

- **高**：官方/监管财报与可核验产品状态、论文中的实际生产部署。
- **中**：公司基准测试、客户计划、第三方市场预测；方向可用，数值需折扣。
- **低**：定义不透明的商业市场报告、媒体采访中的目标份额或未披露客户的供应链说法。本报告没有把匿名传闻写入结论。

### 市场口径警告

NAND 包含 eSSD 所用闪存，eSSD 又包含控制器；存储系统包含 SSD、网络和软件；HBM 与 CXL 是内存层，不应与整机市场直接相加。利润池表用于比较价值量和敏感度，**不是总可寻址市场的加总表**。

## 会议重点和相较 2025 年的变化

### 2025 基线与会前预期

2025 年公开材料已经给出多数方向的“原型”：Samsung 当时已展示 PM1763、液冷 SSD、CXL、HBM4/4E 与定制 HBM；Kioxia 已发布 245.76TB LC9、BiCS9/10、32-die QLC 和 CXL XL-FLASH；HBF 还获得 FMS 2025 Best of Show；NVIDIA Storage-Next 自 2024-12 启动，2025 年 SCADA 仍是封闭/内部架构。这意味着 2026 年不能以“首次出现”为评价标准，而应看是否发生了代码开放、样品送客、量产、客户部署或单位经济性变化。[Samsung FMS 2025 回顾](https://news.samsungsemiconductor.com/global/samsung-electronics-presents-vision-for-ai-memory-and-storage-at-fms-2025/)；[Kioxia FMS 2025 发布](https://americas.kioxia.com/en-us/business/news/2025/ssd-20250804-1.html)；[FMS 2025 奖项名单](https://futurememorystorage.com/news/press-releases/download/114/FMS%202025%20Best%20of%20Show_FINAL.pdf)；[NVIDIA GTC 2025 Storage-Next/SCADA 演讲](https://www.nvidia.com/en-us/on-demand/session/gtc25-s73012/)（均检索：2026-08-18）

会前合理预期可概括为：PCIe 6.0 从样品转量产、245TB QLC 扩客户、HBM4 进入收入、CXL 从互操作演示转规模部署、GPU-direct 软件扩生态、HBF 从奖项转产品。会议后的实际结果是前三项兑现较多，CXL 与 HBF 的商业化低于叙事热度，而小块 I/O、液冷、安全和软件开放的重要性高于单纯容量升级。

### 本届最重要的九个变化

| 变化 | 2025/会前状态 | FMS 2026 后的可核验证据 | 节奏判断 |
|---|---|---|---|
| 1. 工作负载中心转向推理与 KV cache | 训练检查点和顺序吞吐仍占主叙事；推理分层处早期架构阶段 | 官方议程密集出现 inference、KV cache、RAG、小块 I/O、memory tiering；NVIDIA CMX/Storage-Next 明确以 context memory 为对象 | **加速**；最重要的结构变化 |
| 2. SSD 从 GB/s 转向 512B IOPS、尾延迟、IOPS/W | 2025 多以 245TB 容量、PCIe 6.0 峰值带宽和聚合模拟为亮点 | Kioxia GP1 给出单盘 512B 随机读 10M IOPS、50 DWPD，未来架构目标 100M；NVIDIA 提出 Gen6/Gen7 约 200M/400M IOPS 的系统需求 | **加速**，但高 IOPS 仍处样品/研究阶段 |
| 3. PCIe 6.0 从预告进入首批量产 | Samsung PM1763 在 2025 已获奖/预告 | Samsung PM1763、Micron 9650 明确量产；Kioxia CM10/GP1、Marvell SC6 等仍在样品节奏 | **由点到线**，生态尚未全面成熟 |
| 4. 容量 SSD 与性能 SSD明确分层 | 245.76TB QLC 已发布，但市场常把所有 eSSD 混为一类 | Micron 6600 ION 已出货；Kioxia LC9/戴尔 9.8PB/2U 强化容量层；GP1/XL1 强化热数据层 | **分化加速**，产品组合比总 bit 更重要 |
| 5. GPU-direct 由单厂功能转向多方维护生态 | Storage-Next 已启动，SCADA 尚封闭 | cuFile APIs/垂直软件栈开源，Google、Intel、Meta、NVIDIA 为初始维护者，Storage-Next 超过 40 家 | **显著加速**；SCADA 本身仍需生产验证 |
| 6. 液冷、安全和故障隔离进入 SSD 设计一等公民 | 2025 已有液冷概念与样品 | PM1763、CM10、GP1 等把液冷写入产品/样品；SCADA 明确拆出特权映射组件 | **加速**，价值量向机架级系统扩散 |
| 7. CXL 呈“定制扩展已落地、开放池化仍早期” | 大量互操作展示和路线图 | Meta Vistara 已在数百万生产服务器部署；FMS CXL demos 仍以 1TB 混合内存、GPU 利用率提升等演示为主 | **内存扩展加速，池化低于预期** |
| 8. HBF 从概念/奖项转开放规范，但未转产品 | 2025 HBF 已获奖，市场容易误判为即将量产 | SK hynix/Sandisk 公布开放规范和 OCP 合作，Google/Tenstorrent 参与；无商业硅片、订单或客户部署 | **标准化加速，商业化未加速** |
| 9. 垂直堆叠愿景更大胆，近期可投资性反而下降 | HBM4/4E、CXL 和高层 NAND 路线明确 | Samsung zHBM、zNAND-O、HBM5 模型及 V10 >400 层展示；多数无时间表或客户 | **概念加速、收入可见度低** |

### 不能混淆的两组性能数字

Kioxia 在 2025 年会后报告中写到，基于仿真的 GPU-direct SSD 聚合系统达到 143M IOPS；2026 年 GP1 的 10M IOPS 是单盘、512B 随机读、功能样品条件。前者不是一块已经量产的 143M IOPS SSD，后者也不能直接外推到完整机架。[Kioxia FMS 2025 会后报告](https://americas.kioxia.com/en-us/insights/fms25-202510.html)；[Kioxia GP1 发布](https://europe.kioxia.com/en-europe/business/news/2026/20260804-2.html)（检索：2026-08-18）

## AI 存储瓶颈如何变化

### 从“带宽墙”变成七层协同约束

AI 推理的数据路径可简化为：对象/数据湖 → 容量 SSD → 高 IOPS SSD/上下文缓存 → CXL/主机 DRAM → HBM → GPU；网络、DPU、控制器和软件横跨全部层。2026 年的新问题不是某一层绝对不够快，而是**最慢的元数据、最差的尾延迟、错误的数据放置或权限切换，足以让昂贵 GPU 等待**。

| 层 | 新约束 | FMS 2026 证据 | 产业含义 |
|---|---|---|---|
| NAND 介质 | 供给约束、层数/良率、QLC 耐久、读延迟与资本开支回报 | BiCS10 QLC 为 332 层、CBA 架构，厂商称 bit 密度较 BiCS8 提升约 60%、接口 4.8Gb/s，但仍写“加速商业化”而非量产日期 | 高密度 QLC 扩容量层；热数据仍需要 TLC/XL-FLASH，不能用最低美元/TB 统一定价 |
| 企业 SSD | 512B 小 I/O、尾延迟、50 DWPD、功耗和冷却 | GP1 10M IOPS/50 DWPD；PM1763 28.4/21.9GB/s；CM10、NX1 加液冷 | 峰值顺序带宽不再足够；验证周期、固件 QoS 与散热决定收入 |
| 控制器 | ECC、写放大、FTL、QoS、安全、CXL/PCIe 6.0 信号完整性 | Samsung 4nm 自研控制器；Marvell SC6、SM8466、PCIe 6.0 交换芯片进入样品 | 自研控制器强化 NAND 原厂优势；独立厂商必须靠定制、RDK 和客户覆盖突围 |
| CXL/主机内存 | 容量、页放置、时延可预测性、故障域和软件透明性 | Vistara 生产部署；Montage/Astera/SMART 仍为演示 | 近一年先是 Type-3 扩展和专用控制器，跨主机 pooling 后置 |
| HBM | 封装能力、良率、功耗、热阻、容量和年度定价 | Samsung/SK hynix/Micron HBM4 量产；HBM4E 样品；zHBM 仅概念 | HBM 单位价值继续升，但需警惕 DDR5 价格上行时 HBM 的相对晶圆利润变化 |
| 网络/DPU | 东西向流量、存储协议卸载、加密/隔离、光电功耗 | NVIDIA BlueField-4 STX/CMX、Spectrum-X、Marvell 260-lane PCIe 6.0 switch | 上下文缓存外溢使存储网络更像内存互连；DPU/交换价值量提高 |
| 软件/系统 | 数据放置、缓存复用、对象/文件/块统一、可观测性、开放接口 | cuFile 栈开源；DDN Infinia 宣布接入 SCADA；FMS 议程强调 RAG/KV/cache tiering | 软件可减少“每 token 搬运字节数”，可能同时扩大高性能层价值并压低原始容量需求 |

### 各层出现的具体新约束

#### NAND 与容量层

- **事实（中高置信）**：TrendForce 2026-07-21 预计 2026 年 NAND 供给缺口 4%–5%，2027 年供给转为高于需求、下半年尤其缓和；同时预计 2026 年服务器出货量同比约增 17%，消费端较弱。[TrendForce NAND 供需更新](https://www.trendforce.com/presscenter/news/20260721-13148.html)
- **事实（高置信）**：Kioxia 投资者日引用 TechInsights 数据，全球 flash bit 从 2025 年 997EB 增至 2028 年 1,807EB，CAGR 约 22%；数据中心从 295EB 增至 909EB，CAGR 约 46%；其中 **inference 用途的 bit 需求 CAGR 估计为 86%**，不是说 inference 已占数据中心需求的 86%。[Kioxia Investor Day 2026](https://www.kioxia-holdings.com/content/dam/kioxia-hd/en-jp/ir/library/event/asset/Kioxia-Investor-Day-2026-en.pdf)
- **判断**：2026 年的短缺不是所有 NAND 同质受益。AI 容量盘受益于 QLC bit 密度和高 ASP，客户端 NAND 则受高价格抑制。到 2027 年，新增层数、产线转节点和中国厂商供给可能把“缺货溢价”重新变成“产品组合溢价”。

#### 企业级 SSD 与控制器

- **事实（高置信）**：Samsung 于 2026-07-08 宣布 PM1763 量产，首批 4/8/16TB，PCIe 6.0、9 代 V-NAND、4nm 控制器，顺序读/写 28.4/21.9GB/s，并称能效较上一代提升超过 1.8 倍。[PM1763 量产公告](https://news.samsungsemiconductor.com/global/samsung-begins-mass-production-of-pm1763-ssd-optimized-for-next-generation-ai-infrastructure/)
- **事实（高置信）**：Micron 于 2026-03-16 宣布 9650 PCIe 6.0 SSD 进入高量产；2026-05-05 又宣布 245TB 6600 ION 已出货，额定约 30W、8.2TB/W。[Micron HBM4/9650 HVM](https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin)；[Micron 6600 ION 出货](https://investors.micron.com/news-releases/news-release-details/industry-leading-245tb-micron-6600-ion-data-center-ssd-now)；[6600 ION 技术说明](https://www.micron.com/about/blog/storage/ssd/micron-6600-ion-redefining-data-center-storage)
- **事实（中高置信）**：Kioxia GP1 是功能样品，计划 2026 年底向特定客户提供评估样品；CM10 当前也是功能样品，NX1 正向特定 hyperscale 客户送样。它们不能与 Samsung/Micron 的量产收入等同。[Kioxia CM10](https://europe.kioxia.com/en-europe/business/news/2026/20260730-2.html)；[Kioxia NX1](https://europe.kioxia.com/en-europe/business/news/2026/20260729-1.html)
- **判断**：控制器成为 eSSD 的隐性瓶颈。高速介质若缺乏稳定 QoS、低写放大、细粒度地址转换和热管理，无法把峰值 IOPS 转成可持续的 GPU 利用率。

#### HBM、CXL 与内存分层

- **事实（高置信）**：Samsung 2026-02-12 宣布 HBM4 商业出货，2026-05-29 宣布 HBM4E 样品出货；Micron 2026-03-16 宣布 36GB、超过 2.8TB/s 的 HBM4 高量产；SK hynix 2026 年二季度材料称 HBM4 已开始大规模出货并将在下半年爬坡。[Samsung HBM4](https://news.samsungsemiconductor.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing/)；[Samsung HBM4E](https://news.samsungsemiconductor.com/global/samsung-electronics-begins-shipment-of-industry-first-hbm4e-samples/)；[SK hynix 2Q26](https://www.prnewswire.com/news-releases/sk-hynix-announces-2q26-financial-results-302837085.html)
- **事实（高置信）**：Meta Vistara 论文称其 CXL 内存扩展已部署在数百万台生产服务器；约 40% 工作负载受内存容量约束，分离式推理配置最多可减少约 25% 服务器，缓存场景平均延迟降低约 29%。这验证的是定制内存扩展，不是开放跨机架池化。[Vistara 论文](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf)；[CXL Consortium Vistara webinar](https://computeexpresslink.org/event/scaling-cxl-to-millions-of-servers-vistara-for-hyperscale-efficiency/)
- **判断**：HBM 缓解的是最热层，CXL 扩的是较温层，SSD 承担最便宜且可持久化的上下文层。三者的相对价格、软件命中率和尾延迟，而非单一带宽，决定最优配比。

#### 网络、软件与存储系统

- **事实（中置信）**：NVIDIA 称 BlueField-4 STX/CMX 可把 flash context tier 接入 Spectrum-X，并给出最高约 5 倍 TPS、4–5 倍能效等厂商基准；合作伙伴平台计划 2026 年下半年推出，早期客户措辞主要是“计划采用”。[NVIDIA CMX 技术博客](https://developer.nvidia.com/blog/?p=111143)；[BlueField-4 STX 合作伙伴公告](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption)
- **事实（中置信）**：DDN 2026-07-29 对 Infinia 公布 18 倍 TTFT、75% 输入成本下降、RAG 22 倍、checkpoint 600 倍等结果，并称与 SCADA 集成。它是厂商工作负载测试，未见同口径第三方生产复现。[DDN Infinia 更新](https://www.ddn.com/blog/ddn-infinia-expands-to-power-inference-intelligent-data-lakes-and-multi-protocol-ai-workloads/)
- **事实（高置信）**：Micron 在 SC25 的单服务器演示使用 44 块 9650、3 张 H100 和 Broadcom 交换，达到 230M IOPS；这是实验室系统记录，不是单盘性能，也不是客户生产部署。[Micron 230M IOPS 演示](https://www.micron.com/about/blog/storage/ssd/sc25-performance-breakthrough-230m-iops-in-a-single-server)
- **判断**：AI 存储系统的议价权将取决于能否同时管理对象、文件、块、KV cache 和 GPU-direct 路径，并用可验证的 token/s、TTFT 和 GPU 利用率证明价值；仅有介质带宽的传统阵列更容易被压缩毛利。

## 发布、量产、订单和部署核验

### 成熟度矩阵

| 公司/组织 | 发布或能力 | 截至 2026-08-18 的公开状态 | 成熟度 | 置信度 | 研究处理 |
|---|---|---|---|---|---|
| Samsung | HBM4 | 2026-02 宣布商业出货 | P | 高 | 计入 2026 HBM 收入 |
| Samsung | HBM4E | 2026-05 向客户送样 | S | 高 | 计入验证费用，不计大规模收入 |
| Samsung | PM1763 PCIe 6.0 SSD | 2026-07 宣布量产；首批 4/8/16TB | P | 高 | 计入 2026 下半年 eSSD 收入 |
| Samsung | V10 BV-NAND、HBM5 模型 | V10 >400 层并称较 V9 密度提高约 58%；未给量产节点 | R/C | 中 | 只计路线图期权 |
| Samsung | zHBM、zNAND-O | FMS 展示模型；zHBM 目标相对 HBM5 约 8 倍性能、10 倍以上密度等，无时间表/客户 | C | 中 | 不进入十二个月收入模型 |
| Micron | HBM4、9650 PCIe 6.0 | 2026-03 宣布高量产 | P | 高 | 计入当前收入 |
| Micron | 6600 ION 245TB QLC | 2026-05 宣布 now shipping | P | 高 | 容量层量产证据 |
| SK hynix | HBM4 | 2026Q2 已开始大规模出货、H2 爬坡 | P | 高 | 计入当前收入 |
| SK hynix/Sandisk/OCP | HBF | 开放规范，最高 512GB、8/16-high、约 0.4–3TB/s；无商业硅片 | R | 中高 | 不计收入，跟踪互操作和首颗硅片 |
| SK hynix | 375 层 4D NAND eSSD | 称性能/瓦提升约 2.5 倍，eSSD 计划 2027 年初量产 | R/S | 中高 | 计入 2027 小幅爬坡，不前置到 2026 |
| Kioxia | LC9 245.76TB | 公司投资者材料列为量产；Dell 2U/40 盘平台可配 9.8PB | P/D | 中高 | 计入容量层；平台可配不等于已公开规模采购 |
| Kioxia | CM10 PCIe 6.0 | 功能样品，最高 61.44TB、1/3 DWPD | S | 高 | 等待客户资格认证 |
| Kioxia | GP1 XL-FLASH | 功能样品，10M 512B IOPS、50 DWPD；年底评估样品 | S | 高 | 不把奖项当量产 |
| Kioxia | NX1 液冷 E1.S | 向特定 hyperscale 客户送样 | S | 高 | 有客户验证，未披露订单 |
| Kioxia | XL1 CXL XL-FLASH | 2026-08 向生态合作方提供评估样品 | S | 中高 | CXL flash 尚非商业规模 |
| Kioxia/Sandisk | BiCS10 QLC | 332 层、CBA、4.8Gb/s；措辞为加速商业化 | R/S | 高 | 未给量产日期，不计大规模收入 |
| NVIDIA/社区 | cuFile APIs 与垂直栈 | 代码开放；四家初始维护者；40+ Storage-Next 参与方 | D | 高 | 软件生态实质进展 |
| NVIDIA/DDN | SCADA 集成 | 架构与厂商集成公告；未见独立生产客户数据 | S/R | 中 | 不写成全面开源或规模部署 |
| Meta | Vistara CXL 内存扩展 | 数百万台生产服务器部署 | D | 高 | CXL 最强量产证据，但限于定制扩展 |
| Astera/SMART、Montage | CXL 演示 | 5.5 倍 GPU 利用率、1TB 混合内存等为会场演示 | S/Demo | 中 | 作为技术可行性，不当作客户收入 |
| Marvell | Bravera SC6 | PCIe 6.0、NAND-agnostic；2026Q4 样品 | R/S | 高 | 2027 设计导入期权 |
| Marvell | Structera X、Photonic Fabric | 与 hyperscaler 开发/32TB warm KV 概念，未给公开 GA/客户收入 | R | 中 | 不前置规模收入 |
| Marvell | 260-lane PCIe 6.0 switch | 工程样品，计划 2026Q3 客户样品 | S | 高 | 近端交换价值量增量 |
| Silicon Motion | SM8466 | PCIe 6.0、28GB/s、7M IOPS、>512TB 目标；工程样品预计 2027Q1 | R | 中高 | 2026 仅展示/RDK，不计量产 |
| DDN | Infinia | 基础平台可用，公布 SCADA/推理测试；缺独立复现 | D/S | 中 | 计入系统收入，但性能溢价折扣 |

相关一手材料：[Samsung FMS 2026](https://news.samsungsemiconductor.com/global/samsung-unveils-next-gen-3d-memory-vision-at-fms-2026-charting-the-future-of-ai-infrastructure/)；[Samsung FMS 展台回顾](https://news.samsungsemiconductor.com/global/inside-fms-2026-samsung-electronics-showcases-the-future-of-ai-memory/)；[Kioxia FMS 2026 总览](https://americas.kioxia.com/en-us/business/news/2026/ssd-20260803-2.html)；[Kioxia GP1](https://europe.kioxia.com/en-europe/business/news/2026/20260804-2.html)；[Kioxia XL1 官方发布 PDF](https://europe.kioxia.com/content/dam/kioxia/en-europe/business/news/2026/asset/KIE_PR_20260804-1_EN.pdf)；[Sandisk FMS 2026](https://www.sandisk.com/company/newsroom/press-releases/2026/sandisk-nand-innovation-for-era-of-ai-inference-at-fms-2026)；[SK hynix HBF](https://news.skhynix.com/en/hbf-at-fms-2026/)；[FMS 2026 CXL demos](https://computeexpresslink.org/fms-2026-cxl-demos/)；[Marvell FMS 2026](https://investor.marvell.com/news-events/press-releases/detail/1030/marvell-advances-ai-memory-infrastructure-portfolio-to-accelerate-agentic-ai-inference)；[Marvell PCIe 6.0 switch](https://investor.marvell.com/news-events/press-releases/detail/1016/marvell-launches-industrys-first-260-lane-pcie-6-switch-ai-data-center-scale-up-infrastructure)；[Silicon Motion FMS 2026](https://siliconmotiontechnologycorporation.gcs-web.com/news-releases/news-release-details/huirongkejiliangxiang-fms-2026zhanshimianxiang-agentic-ai)（检索：2026-08-18）

### 公开材料中的冲突与不可直接比较项

1. **PM1763 容量口径**：2026-07-08 量产公告写首批 4/8/16TB；当前产品页列出更广的 4–64TB 和不同形态。可能是产品组合扩充或页面更新，但在没有逐型号出货证据时，本报告只把 4/8/16TB 作为首批量产事实，不把 64TB 自动视为同期规模出货。[PM1763 产品页](https://semiconductor.samsung.com/ssd/enterprise-ssd/pm1763/)（检索：2026-08-18）
2. **143M 与 10M IOPS**：前者是 2025 年聚合仿真，后者是 2026 年单盘功能样品；不能据此判断单盘性能倒退。
3. **cuFile 开源与 SCADA 开源**：NVIDIA 明确写的是 cuFile APIs/垂直栈开放；SCADA 是架构和集成对象。除非代码库进一步公开，不能把两者合并。
4. **CXL 市场规模**：Astera 2024 年上市文件引用的 2027 年相关可寻址市场约 44 亿美元，包含更广的 connectivity；Frost & Sullivan 2026 年材料中的狭义 CXL memory connectivity revenue 仅预计 2027 年约 3.01 亿美元。超过十倍差异主要来自定义，而非同一市场预测相互矛盾。[Astera Labs SEC 文件](https://www.sec.gov/Archives/edgar/data/1736297/000119312524069611/d285484ds1a.htm)；[Frost & Sullivan/HKEX 行业材料](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0130/12005367/2026013000025.pdf)
5. **NAND 2027 市场规模**：TrendForce 2026-05-29 预测约 3,794 亿美元；Sandisk 2026 年 8 月材料给出约 5,000 亿美元。后者更接近供给受限、ASP 维持极高的牛市情景，不能作为无条件基准。[TrendForce 2026/2027 memory market](https://www.trendforce.com/presscenter/news/20260529-13068.html)；[Sandisk FY2026 Q4/Investor materials](https://sandisk.gcs-web.com/static-files/c75d1bee-c5c9-4e5a-8605-302c1aeac59b)
6. **厂商倍数与生产效果**：NVIDIA 的 5 倍、DDN 的 18/22/600 倍和 CXL demo 的 5.5 倍均依赖特定基线、模型、缓存命中和配置。报告把它们视为性能上限线索，不直接转成全市场出货或客户 ROI。

## 技术路线与未来三阶段影响

### 路线一：容量层——245TB QLC、更多层数与机架密度

戴尔 PowerEdge R7725xd 配置 40 块 Kioxia LC9 时可在 2U 提供约 9.8PB；Kioxia 称若改用 30.72TB 盘，为获得同等容量需要多 7 台服务器、280 块盘及约 8 倍盘级功耗。这是配置级 TCO 比较，不是公开的大规模客户采购。[Kioxia/Dell 9.8PB 平台](https://americas.kioxia.com/en-us/business/news/2026/ssd-20260514-2.html)（2026-05-14）

- **3 个月**：245TB 产品从“最大容量”转向真实资格认证、供货量和重复订单；高 NAND 合同价会帮助收入，但也可能延迟从 HDD 迁移。
- **1 年**：332/375 层 NAND、CBA 和更高堆叠密度推动单位机架容量；容量盘 ASP 取决于 NAND 紧缺是否持续到 2027 下半年。
- **2 年**：512TB 级盘具备技术可行性，但是否成为主流取决于故障域、重建时间、客户对单盘失效风险和双供应商策略的接受度。

### 路线二：性能层——PCIe 6.0、XL-FLASH 与小块 I/O

Samsung/Micron 已把 PCIe 6.0 带入量产，Kioxia 的 GP1 把 512B 10M IOPS 与 50 DWPD 作为新的产品类别。NVIDIA 在 GTC 2026 的研究演讲中给出：要在 512B 访问下饱和 Gen6，系统约需 200M IOPS；面向 Gen7 的愿景约 400M IOPS/GPU，并强调 IOPS/美元和 IOPS/W。这是架构目标，不是当前单盘产品承诺。[NVIDIA GTC 2026 small-block storage transcript](https://www.nvidia.com/en-us/on-demand/session/gtc26-s81840/)（检索：2026-08-18）

- **3 个月**：量产收入集中于 Samsung、Micron；Kioxia/Marvell/独立控制器厂以样品和客户验证为主。
- **1 年**：若 Storage-Next/SCADA 出现可复现的非厂商生产数据，高耐久低延迟 SSD 会形成高于通用 TLC 的独立 ASP/毛利池。
- **2 年**：100M IOPS 架构若不能在功耗、散热、CPU/DPU 开销和可靠性上闭环，可能只留在狭窄的 KV/RAG 加速器市场。

### 路线三：HBM—CXL—SSD 上下文内存分层

HBM4 是 2026 年实际收入，HBM4E 是 2027 年验证/爬坡，HBF 与 zHBM 是更远期期权。HBF 开放规范给出的最高 512GB、8/16-high、0.4–3TB/s 和 UCIe 接口，使 NAND 有机会以更低成本靠近加速器；但介质延迟、耐久、控制器、软件 I/O 和一致性仍没有量产验证。

- **3 个月**：HBM4 良率、封装产能和客户认证决定供应；CXL 收入以扩展控制器/交换/重定时器为主。
- **1 年**：HBM4 成主流、HBM4E 开始量产；CXL Type-3 扩展进入更多通用服务器；HBF 若出现首颗硅片，才可从规范转为产品期权。
- **2 年**：若软件能稳定管理 HBM、CXL DRAM、SSD/HBF 的冷热迁移，价值从单一内存介质向控制器和数据放置软件移动；若迁移开销和尾延迟不可控，架构会继续以固定分层为主。

### 路线四：网络/DPU/软件把存储变成上下文基础设施

BlueField-4 STX、Spectrum-X、Storage-Next、cuFile 和 SCADA 的共同方向，是让 GPU 只拉取需要的数据、降低 CPU 中转和重复读取。对系统厂商而言，新的销售单位不再只是 PB，而是每机架 token/s、TTFT、GPU 利用率、每 token 功耗和故障恢复时间。

- **3 个月**：合作伙伴平台发布和 SDK/代码活跃度比峰值 benchmark 更重要。
- **1 年**：DPU、PCIe/CXL switch、retimer、NIC 和光互连的单位价值随上下文外溢增加；多协议系统通过软件订阅维持毛利。
- **2 年**：若 context cache 变成跨节点共享服务，网络/存储边界进一步模糊；若模型压缩、KV reuse 或长上下文算法显著降低每 token 搬运量，硬件容量增速会低于当前乐观预期。

### 容量、价格、出货、资本开支和竞争格局的时间表

| 时间 | 容量/出货 | 价格 | 资本开支 | 竞争格局 |
|---|---|---|---|---|
| 未来 3 个月（至 2026-11-18） | HBM4 与量产 PCIe 6.0 盘放量；245TB QLC 扩资格认证；GP1/CM10/XL1 仍以样品为主 | NAND 合同价和 allocation 维持强势，但不同耐久等级价差扩大 | 以节点迁移、先进封装、测试和液冷适配为主，暂不需要全面扩晶圆厂 | Samsung/Micron 先享受 PCIe 6.0 量产；SK hynix 在 HBM；Kioxia/Sandisk在高密度 NAND与样品管线 |
| 未来 1 年（至 2027-08-18） | 375 层 eSSD、HBM4E、更多 Gen6 控制器进入市场；CXL 扩展量增，pooling 仍小 | 基准为 NAND 高位但涨幅放缓；悲观情景在 2027H2 转跌 | 龙头保持高额节点/封装投资；若订单与 ASP 下行，新增晶圆产能延后 | 竞争从“有没有产品”转为“资格认证、固件稳定、液冷、长期合同和系统协同” |
| 未来 2 年（至 2028-08-18） | 全球 flash bit 向约 1,807EB 的 2028 参考值靠近；245/512TB 级容量层普及，高 IOPS 层需证明规模 | 供给弹性恢复后，介质 ASP 下行；高耐久、低延迟和软件仍有溢价 | 新层数、CBA、先进封装及中国供给决定周期；错误扩产会压缩利润池 | NAND 原厂、自研控制器厂、DPU/交换与软件平台重新分配利润；HBF/zHBM 只有量产才改变格局 |

Kioxia 披露年度资本开支约 4,700 亿日元、研发约 2,300 亿日元，并目标 FY2028 数据中心收入占比超过 60%；这说明当前投入更偏节点、产品和数据中心组合，而非简单追求全行业 wafer 扩张。[Kioxia Investor Day 2026](https://www.kioxia-holdings.com/content/dam/kioxia-hd/en-jp/ir/library/event/asset/Kioxia-Investor-Day-2026-en.pdf)

## 市场规模和利润池：2026 当前值与 2027 三情景

### 模型说明

所有金额为名义美元，收入和毛利率为市场层估计，不等同于任何单家公司财报。2026 为截至 2026-08-18 可得材料下的全年估计；2027 为未来一年三情景。毛利额 = 收入 × 毛利率。物理量采用十进制单位。为避免伪精确，关键结果保留 2–3 位有效数字。

### 2026 当前规模估计

| 利润池 | 2026 收入 | 物理量/指数 | 隐含单价或单位价值 | 毛利率假设 | 毛利额 | 依据与置信度 |
|---|---:|---:|---:|---:|---:|---|
| NAND 全市场 | **2,706 亿美元** | **1,217EB** bit shipment | **0.222 美元/GB** | 60% | **1,624 亿美元** | 收入取 TrendForce 2026-05-29；bit 以 997EB（2025）至 1,807EB（2028）约 22% CAGR 平滑推导。2026Q2 前五厂收入 688.7 亿美元、年化约 2,755 亿，与全年估计接近。中置信 |
| 企业级 SSD（NAND 子集） | **1,250 亿美元** | **约 500EB** NAND capacity-equivalent | **约 250 美元/TB** | 60% | **750 亿美元** | 以 2026Q1 前五大 eSSD 收入 184.6 亿美元、价格环比约 +80%、服务器已占 NAND bit 需求 40% 以上，以及 Kioxia 数据中心 bit 曲线交叉校准。中低置信，不能与 NAND 相加 |
| HBM | **490 亿美元** | **3.75B GB**，约 **117M 个 32GB stack-equivalent** | **13.1 美元/GB** | 60% | **294 亿美元** | Micron 给出 2025 年约 350 亿、2028 年约 1,000 亿和约 40% CAGR；TrendForce 2025 预计 2026 出货超过 30B Gb。中置信 |
| 企业级 SSD 控制器 | **39.8 亿美元** | **31.8M 个 controller-equivalent** | **125 美元/个** | 50% | **19.9 亿美元** | 商业研究报告给出 2026 年 39.8 亿；产品定义可能含原厂自用控制器。低置信 |
| 狭义 CXL memory connectivity | **0.989 亿美元** | **0.283M 个 device-equivalent** | **350 美元/个** | 60% | **0.593 亿美元** | Frost & Sullivan/HKEX 口径；明显窄于整个 PCIe/CXL connectivity TAM。中低置信 |
| 外部企业存储系统 | **410.9 亿美元** | volume index 100 | price/mix index 100 | 45% | **184.9 亿美元** | IDC 2026 预测 410.89 亿、同比约 16.3%。中高置信；含设备与系统价值，和 SSD 重叠 |
| 广义高速数据中心互连 | **234 亿美元** | volume index 100 | price/mix index 100 | 60% | **140.4 亿美元** | Frost & Sullivan/HKEX 广义口径，含高速连接而非只含存储网络。中低置信 |

企业级 SSD 的 500EB 是容量当量而非成品盘铭牌容量：TrendForce 称 2026 年服务器已占 NAND bit 需求 40% 以上，对本报告 1,217EB 总 bit 的机械映射约为 487EB；Kioxia/TechInsights 的数据中心曲线从 2025 年 295EB 按 46% CAGR 平滑到 2026 年约 431EB。两者定义不同，本报告取约 500EB，并把 enterprise 非 hyperscale 用途和高价高耐久 mix 反映在约 250 美元/TB 中。因此该行应视为约 430–500EB、收入约 1,100–1,250 亿美元的区间估计，表中使用上沿作为与季度收入 run-rate 一致的基准。

关键来源：[TrendForce NAND/DRAM 2026–2027](https://www.trendforce.com/presscenter/news/20260529-13068.html)；[TrendForce 2026Q2 NAND](https://www.trendforce.com/presscenter/news/20260818-13186.html)；[TrendForce 2026Q1 eSSD](https://www.trendforce.com/presscenter/news/20260611-13092.html)；[Micron HBM TAM](https://investors.micron.com/static-files/530bd7ed-a8c8-4687-af4a-8c129f740e09)；[TrendForce 2025 HBM4 预测基线](https://www.trendforce.com/presscenter/news/20250522-12589.html)；[企业级 SSD 控制器商业口径](https://www.researchandmarkets.com/reports/6123353/enterprise-level-ssd-controllers-market-global)；[IDC Enterprise Storage Systems](https://www.idc.com/promo/enterprise-storage-systems/)；[Frost & Sullivan/HKEX](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0130/12005367/2026013000025.pdf)（检索：2026-08-18）

### 2027 三情景预测

| 利润池 | 悲观情景 | 基准情景 | 乐观情景 |
|---|---|---|---|
| NAND 全市场 | **收入 2,600 亿美元，-3.9%**；1,550EB；0.168 美元/GB；毛利率 35%；毛利额 910 亿。供给在 2027H1 即明显超过需求，bit 出货高但价格回落 | **收入 3,794 亿美元，+40.2%**；1,485EB；0.255 美元/GB；毛利率 60%；毛利额 2,276 亿。采用 TrendForce 市场值，供需在 H2 才缓和 | **收入 5,000 亿美元，+84.8%**；1,430EB；0.350 美元/GB；毛利率 72%；毛利额 3,600 亿。接近 Sandisk 高景气判断；供给纪律使 bit 低于悲观情景但 ASP 极高 |
| 企业级 SSD（NAND 子集） | **收入 1,040 亿，-16.8%**；650EB；160 美元/TB；毛利率 40%；毛利额 416 亿。供给释放使 bit 增长但价格快速回落，服务器采购延后 | **收入 1,512 亿，+21.0%**；680EB；222 美元/TB；毛利率 55%；毛利额 832 亿。容量盘和 Gen6 同时放量，ASP 温和下降 | **收入 1,989 亿，+59.1%**；740EB；269 美元/TB；毛利率 68%；毛利额 1,353 亿。AI context tier 快速部署、供应紧张且高耐久产品占比上升 |
| HBM | **收入 550 亿，+12.2%**；4.69B GB；11.73 美元/GB；毛利率 52%；毛利额 286 亿。GPU/ASIC 延期、普通 DRAM 涨价压缩相对晶圆回报 | **收入 686 亿，+40.0%**；5.25B GB；13.07 美元/GB；毛利率 62%；毛利额 425 亿。沿 Micron 的约 40% CAGR，HBM4 主流、HBM4E 起量 | **收入 877 亿，+79.0%**；5.81B GB；15.10 美元/GB；毛利率 70%；毛利额 614 亿。更大 stack 容量、定制 HBM 与封装紧缺共同提高单价 |
| 企业级 SSD 控制器 | **收入 38 亿，-4.5%**；31.7M；120 美元/个；毛利率 45%；毛利额 17.1 亿。NAND 原厂自研渗透、Gen6 验证延迟 | **收入 44 亿，+10.6%**；35.2M；125 美元/个；毛利率 52%；毛利额 22.9 亿。Gen5/Gen6、RDK 和高容量盘组合增长 | **收入 52 亿，+30.7%**；40.0M；130 美元/个；毛利率 58%；毛利额 30.2 亿。独立控制器拿到 hyperscaler 定制和高 IOPS 设计 |
| 狭义 CXL memory connectivity | **收入 1.8 亿，+82%**；0.60M；300 美元/个；毛利率 50%；毛利额 0.90 亿。仅定制扩展，pooling 延迟 | **收入 3.01 亿，+204%**；1.00M；301 美元/个；毛利率 60%；毛利额 1.81 亿。采用第三方基准，Type-3 扩展进入更多平台 | **收入 5.5 亿，+456%**；1.57M；350 美元/个；毛利率 68%；毛利额 3.74 亿。交换、扩展和部分 pooling 同时进入商业部署 |
| 外部企业存储系统 | **收入 400 亿，-2.7%**；volume 94.3；price/mix 103；毛利率 42%；毛利额 168 亿。云客户自建、介质成本挤压 | **收入 433.1 亿，+5.4%**；volume 99.3；price/mix 106；毛利率 46%；毛利额 199.2 亿。采用 IDC 预测，AI 系统抵消通用阵列放缓 | **收入 480 亿，+16.8%**；volume 106.2；price/mix 110；毛利率 50%；毛利额 240 亿。GPU-direct、多协议和软件订阅提高 mix |
| 广义高速数据中心互连 | **收入 250 亿，+6.8%**；volume 110；price/mix 97.1；毛利率 55%；毛利额 137.5 亿 | **收入 285 亿，+21.8%**；volume 118；price/mix 103.2；毛利率 62%；毛利额 176.7 亿 | **收入 330 亿，+41.0%**；volume 128；price/mix 110.2；毛利率 68%；毛利额 224.4 亿 |

### 三情景的关键触发条件

| 情景 | NAND/eSSD | HBM | CXL/互连/系统 |
|---|---|---|---|
| 悲观 | 2027H1 供给即转过剩；季度合同 ASP 连续下跌；客户端需求未恢复，服务器采购延迟 | GPU/ASIC 量产推迟；先进封装瓶颈缓解快于需求；DDR5 利润吸引晶圆回流 | CXL 资格认证延迟；Storage-Next 无生产案例；云厂商继续自建，外部阵列量跌 |
| 基准 | 2026 缺口延续至 2027H1，H2 缓和；数据中心 bit 增长快于总市场 | HBM4 成主流，HBM4E 小规模起量；价格/容量合同支持约 40% 收入增长 | CXL 扩展控制器放量但 pooling 仍小；AI 系统 mix 抵消传统存储量疲弱 |
| 乐观 | 长期协议和供给纪律限制 bit，245TB/Gen6 高价值产品占比快速升 | 大容量 HBM4/4E、定制 HBM 与封装紧缺同时推高量价 | 上下文缓存外溢使 DPU、交换、retimer、软件和外部系统价值量同步提升 |

### 与公司财报的交叉核验

- Micron FY2026 Q3 披露**单季收入** 414.56 亿美元，NAND 收入约 99 亿美元；季度 NAND bit 出货环比中个位数增长、价格环比中 80% 增长，数据中心 SSD 收入超过 50 亿美元且环比超过翻倍；非 GAAP 毛利率 84.9%、资本开支 71 亿美元。这验证当前利润主要由价格/mix 而非 bit 单独驱动。[Micron FY2026 Q3 SEC 附件](https://www.sec.gov/Archives/edgar/data/723125/000072312526000013/a2026q3ex991-pressrelease.htm)；[Micron FY2026 Q3 演示](https://investors.micron.com/static-files/2354ecda-77a0-4ddd-8462-a631eb491356)
- TrendForce 于检索截止日 2026-08-18 发布的 2026Q2 数据显示，前五大 NAND 厂收入环比增加 77% 至 688.7 亿美元；Samsung、SK hynix Group、Micron、Kioxia、Sandisk 分别约 230.6、142.7、118.5、107.2、89.7 亿美元。其年化值约 2,755 亿美元，与本报告 2,706 亿美元全年估计接近，但 Q2 高价年化仍可能高估淡旺季之外的可持续收入。[TrendForce NAND 2026Q2](https://www.trendforce.com/presscenter/news/20260818-13186.html)
- Sandisk FY2026 Q4 收入 89.65 亿美元、毛利率 84.6%，约三分之一增长来自 volume、三分之二来自 price；FY2026 收入 202.48 亿美元，数据中心 Q4 收入 29.77 亿、全年 51.53 亿。公司还披露长期采购安排、最低收入与 RPO，但这些是合同支持，不是无风险现金收入。[Sandisk FY2026 Q4](https://sandisk.gcs-web.com/news-releases/news-release-details/sandisk-reports-fiscal-fourth-quarter-2026-financial-results)
- TrendForce 2026Q1 统计前五大 eSSD 厂商收入 184.6 亿美元、环比 +86.1%，价格约 +80%；Samsung、SK hynix、Micron、Kioxia、Sandisk 分别约 70.5、46.4、30.9、22.2、14.7 亿美元。极高的价格贡献支持高景气事实，也说明 2027 对 ASP 的敏感度远高于对 bit 的敏感度。[TrendForce eSSD 2026Q1](https://www.trendforce.com/presscenter/news/20260611-13092.html)
- TrendForce 2026-06-02 指出，HBM 晶圆投入占比从 2025 年 18% 升至 2026 年 22%、2027 年约 30%，但因 HBM 年度定价，2026Q1 HBM 单晶圆利润可能低于价格快速上涨的 DDR5 RDIMM。HBM 高增长不等于每个季度都拥有最高机会成本回报。[TrendForce HBM/DRAM profitability](https://www.trendforce.com/presscenter/news/20260602-13074.html)

## 反共识洞见

### 1. 最稀缺的可能不是 NAND bit，而是可持续的小块 IOPS

**事实**：容量盘已达 245TB，PCIe 6.0 顺序读接近 28GB/s；但单 GPU 在 512B 访问下的系统需求可高达数亿 IOPS。**观点**：AI context tier 的高毛利不是“更多 NAND”，而是介质、控制器、固件、散热和软件共同提供的低尾延迟。**证伪**：若生产系统主要使用 4KB 以上大块顺序访问，或 KV 压缩使小 I/O 需求显著低于 NVIDIA 的研究假设，高 IOPS 产品会成为小众。

### 2. CXL 已经规模部署，但投资者容易买错那一段

Vistara 证明定制 CXL 扩展有效；它没有证明通用 pooling、CXL flash 或所有商用交换芯片已经进入百万级部署。未来一年更确定的是每服务器的控制器/retimer/内存扩展价值，最不确定的是跨机架可组合池。**证伪**：若 2027 年出现多个非定制、跨厂商 pooling 的公开生产客户，并给出稳定尾延迟与故障隔离数据，应上调交换和软件市场。

### 3. HBF 的重要性是真的，十二个月收入却接近零

开放规范、OCP 和 Google/Tenstorrent 参与降低生态风险，但 2025 年它已经获奖，2026 年仍没有商业硅片。把 HBF 直接映射为 2027 年大额 NAND/HBM 替代收入属于时间错配。**证伪**：2027H1 前若出现控制器硅片、加速器接口、互操作测试和明确客户量产时间，应把 HBF 从 R 提升至 S/P。

### 4. 245TB SSD 不会全面替代 HDD

在高 IOPS、机架受限、能耗昂贵的 warm data 场景，QLC SSD 的机架 TCO 有优势；在低访问频率、容量极大、资本预算敏感的冷数据场景，HDD 的美元/TB 仍难被替代。**证伪**：若多家云厂商公开显示 245TB SSD 的全生命周期美元/TB（含写入寿命、故障域）低于高容量 HDD，并出现连续两季重复采购，替代斜率可上调。

### 5. 公开软件栈可能比一款新介质更改变竞争格局

cuFile/Storage-Next 让应用、GPU、SSD、DPU 和文件系统之间的接口更开放，降低单一封闭存储栈的锁定。它可能扩大合格硬件供应商数量，同时把差异化上移到调度、缓存、可观测性和安全。**证伪**：若代码贡献长期只有 NVIDIA/合作厂商、缺少非厂商生产案例，开放生态溢价应归零。

### 6. 液冷并非 SSD 附件，而是 Gen6 密度的出货门槛

TrendForce 2026-08-17 估计 2026 年 AI 芯片液冷渗透约 53%、2027 年接近 60%，并称 Google 已有超过 80% 的 AI 服务器采用液冷；当 SSD、DPU、交换也进入高热密度，冷板、歧管、CDU、连接器和机架设计会共享增量价值。[TrendForce 液冷更新](https://www.trendforce.com/presscenter/news/20260817-13183.html)（2026-08-17）**证伪**：若量产 Gen6 SSD 在目标 IOPS 下可长期依赖风冷且不降频，液冷附着率会低于本报告判断。

### 7. 长期合同重塑周期，但不会废除周期

Micron 称 2026 年 HBM 量价已锁定，Sandisk 披露多年安排与最低承诺；然而节点良率、客户平台延期、提前采购、竞争供给和替代介质仍会改变实际提货及下一轮定价。合同降低近端波动，可能把风险推迟到续约和产能释放时点。

## 公司及产业链映射

### 主要受益公司

| 公司/类别 | 受益逻辑 | 已验证证据 | 主要催化剂 | 主要风险 |
|---|---|---|---|---|
| Samsung Electronics | HBM4、PCIe 6.0 eSSD、V-NAND、自研控制器全栈；可在容量/性能两层配置产品 | HBM4 商业出货、PM1763 量产 | PM1763 客户扩展、HBM4E 认证、V10 量产时间 | HBM 客户资格与良率；zHBM 概念被过早估值 |
| Micron | HBM4、9650 Gen6、6600 ION 245TB 均已量产/出货；数据中心 SSD 收入快速增长 | 公司财报与量产公告 | HBM4 供货、9650 revenue mix、6600 repeat order | 当前高毛利依赖价格；2027 NAND 供给缓和 |
| SK hynix/Solidigm | HBM4 领先、eSSD 与 375 层路线、HBF 规范期权 | HBM4 大规模出货；375 层 eSSD 计划 2027 初量产 | HBM4E 样品、375 层良率、HBF 硅片 | HBF 时间过早；普通 DRAM 与 HBM 的晶圆机会成本 |
| Kioxia | LC9 容量盘、BiCS10、CM10/GP1/NX1/XL1 覆盖多层；数据中心 bit CAGR 高 | LC9 量产/平台支持，多款样品 | GP1 年底样品、CM10/NX1 资格认证、BiCS10 商业化 | 样品多于量产；高资本开支与价格周期 |
| Sandisk | 数据中心收入与价格弹性高、BiCS10/HBF、长期合同支持 | FY2026 财报、BiCS10/HBF 官方材料 | NBM 合同兑现、数据中心占比、QLC 商业化 | 公司 5,000 亿美元 NAND 预测过于乐观；客户/合同集中 |
| Marvell | PCIe 6.0 SSD 控制器、260-lane switch、CXL/内存基础设施 | 工程样品与明确样品时间 | Q3/Q4 样品、hyperscaler 设计赢单 | 多数产品尚未量产；被 NAND 原厂自研控制器挤压 |
| Astera Labs、Montage、Microchip、Rambus、Renesas | CXL/PCIe 控制器、retimer、switch 和信号完整性 | Vistara 证明需求；会场互操作/演示；Microchip DCS 收入披露 | 新服务器平台采用、Type-3 扩展量产 | 狭义 CXL 市场绝对规模仍小；客户定制化 |
| Silicon Motion、Phison、FADU 等独立控制器 | 多 NAND 支持、RDK、定制固件和客户覆盖 | SM8466/SM8366 等展示 | Gen6 工程样品、hyperscaler 认证 | 自研控制器、验证延期、价格竞争 |
| NVIDIA、Broadcom | GPU/DPU/以太网/PCIe switch 控制上下文数据路径 | Storage-Next、BlueField-4 STX、Micron 演示中的交换平台 | 合作伙伴系统 H2 发布、非厂商生产部署 | 软件可能降低硬件容量需求；生态主导权监管/客户自研 |
| DDN、VAST、WEKA、Hammerspace 等 AI 存储软件/系统 | 以 token/s、TTFT、多协议和 GPU-direct 销售，而非只卖 PB | DDN 产品/测试；VAST 披露累计 bookings >40 亿美元、CARR >5 亿美元 | SCADA/CMX 生产案例、订阅收入、客户扩展 | 厂商 benchmark 不可外推；云厂商自建与估值过高 |
| Dell、HPE 等 OEM | 高密度 SSD、CXL、液冷和 AI 机架集成价值 | Dell/Kioxia 9.8PB/2U 配置 | 认证完成、整机订单和服务收入 | 介质高价挤压整机毛利；hyperscaler 直接采购 |

VAST 的业务数字来自公司 2026-04-22 融资公告：估值 300 亿美元、累计 bookings 超过 40 亿美元、CARR 超过 5 亿美元，并称经营利润和自由现金流为正；这些是私营公司自报，不能当作审计后同口径上市公司收入。[VAST Series F](https://www.vastdata.com/press-releases/vast-series-f-financing-at-30-billion-valuation)

Microchip 2026 年披露 Data Center Solutions 业务（存储、PCIe/CXL、交换）2025 年收入约 3.027 亿美元、2026 年预计约 5 亿美元，可用于验证连接/控制器收入正在放量，但该口径并非纯 CXL。[Microchip DCS revenue](https://ir.microchip.com/news-events/press-releases/detail/1395/microchip-provides-data-center-solutions-business-unit-revenue-information)

### 可能受损或相对落后的方向

1. **客户端/手机/消费电子采购方与低议价渠道**：NAND/DRAM 高价侵蚀 BOM 和需求，短期承担价格转移。
2. **只靠低价通用盘、没有固件/散热/客户资格的模组厂**：介质涨价时资金占用上升，Gen6 和高耐久设计难以跟进。
3. **只卖峰值顺序带宽的控制器厂**：若不能证明小块 QoS、IOPS/W、安全和热稳定，规格表优势无法进入 AI 热层。
4. **缺少 GPU-direct、多协议与软件层的通用存储阵列**：介质成本上升而系统差异化下降，毛利更易受压。
5. **HDD 在延迟敏感 warm data 的新增部署**：会被 245TB QLC 抢份额；但冷数据市场并非整体受损。

### 过度乐观方向

- HBF 在未来十二个月形成大规模收入。
- zHBM 相对 HBM5 “8 倍性能”直接等价于可采购产品。
- CXL pooling 已在通用数据中心全面部署。
- 所有 245TB SSD 都能以厂商实验室 TCO 替代 HDD。
- 5 倍、18 倍、22 倍、600 倍等单一 benchmark 可线性外推到客户收入。
- 长期采购协议已经消灭 NAND/HBM 周期。

### 被低估方向

- Gen6 SSD 与 DPU/交换的冷板、连接器、歧管和机架热设计。
- 控制器固件、ECC、QoS、写放大、安全映射和故障恢复的单位价值。
- cuFile/Storage-Next 之类开放软件对供应商资格和系统竞争的改变。
- 高密度盘减少机架、服务器、线缆和运维的“非介质”价值。
- CXL 先扩内存、后做池化的渐进商业路径。
- 软件压缩、KV reuse 和数据放置既可能提高系统价值，也可能降低原始 bit 需求。

## 风险与后续跟踪

### 可证伪结论和数据清单

| 本报告结论 | 可证伪数据/阈值 | 最晚观察时间 | 首选数据源 |
|---|---|---|---|
| 2026 缺货延续、2027H2 才缓和 | NAND 合同 ASP 在 2026Q4–2027Q1 连续环比为负，或权威供需模型在 2027Q2 前转为零缺口/过剩 | 每季；重点 2027Q2 | TrendForce、原厂财报与 bit/ASP 指引 |
| eSSD 是 NAND 增量核心 | 数据中心 bit 占比连续两季低于约 40%，或 hyperscaler 取消/延后 245TB 与 Gen6 订单 | 2027H1 | 原厂财报、客户资本开支、OEM 配置订单 |
| PCIe 6.0 进入实际放量 | 2027H1 Gen6 在新企业 SSD 出货/收入占比仍低于约 10%，或主要控制器认证整体推迟至 2027H2 后 | 2027-08 | Samsung/Micron/Kioxia/Marvell/SMI 产品与财报 |
| 高 IOPS SSD 形成独立溢价层 | GP1 类产品没有生产客户，或同耐久/容量下 ASP 溢价不足以覆盖液冷和控制器成本 | 2027-08 | 客户部署、公开报价、性能/瓦与 TCO |
| Storage-Next/SCADA 改变生产架构 | 除参与厂商外没有公开生产客户，cuFile 代码贡献和版本发布长期停滞 | 2027-08 | 官方代码库、客户工程博客、可复现实测 |
| HBF 是有价值的两年期权 | 2027H1 无控制器/商业硅片，2027H2 无加速器接口、OCP 互操作或客户量产时间 | 2027H2 | OCP、SK hynix、Sandisk、加速器厂商 |
| CXL 先扩展后池化 | 狭义 CXL 2027 收入明显低于 3.01 亿美元，或除 Meta 定制方案外没有新生产部署 | 2027-08 | 上市公司 CXL 收入、OEM/云客户部署 |
| 245TB QLC 扩大 warm-data 替代 | 没有重复订单，故障域/重建时间使客户回退，或全生命周期美元/TB 不优于 HDD | 2027-08 | Dell/OEM、云客户、故障与功耗数据 |
| HBM 约 40% 收入增长可持续 | GPU/ASIC 推迟、HBM bit/stack 容量增长低于约 25%，或 ASP 下跌超过约 10% | 每季；重点 2027H1 | Micron/Samsung/SK hynix、GPU 平台出货 |
| 网络/DPU/软件价值量上升 | 每 GPU 的 NIC/DPU/switch/retimer content 不升反降，或软件显著降低每 token 搬运字节 | 2027-08 | BOM、平台配置、token/byte 与 cache hit 数据 |

### 月度/季度追踪模板

1. **价格与供需**：NAND 合同价、eSSD ASP、HBM 每 GB/每 stack 价格、bit shipment、inventory days、供需缺口。
2. **产品成熟度**：量产、样品、资格认证、首个公开客户、重复订单分别记录，不允许以 Best of Show 替代量产。
3. **系统效率**：512B/4KB IOPS、P99/P999 延迟、IOPS/W、GPU 利用率、TTFT、token/s、每 token 能耗、cache hit ratio。
4. **热与可靠性**：风冷/液冷附着率、降频、DWPD、写放大、UBER、故障域、重建时间。
5. **资本开支**：NAND wafer capacity、层数转换、HBM advanced packaging、controller tape-out、液冷和测试设备。
6. **生态**：cuFile/Storage-Next 代码提交者、SCADA/CMX 非厂商案例、CXL 互操作、HBF 硅片和 OCP 测试。

### 主要风险

- **宏观与客户集中**：AI 基础设施资本开支若从少数 hyperscaler 同时放缓，HBM/eSSD 的量价会共振。
- **供给错配**：高价格诱发扩产和节点爬坡，2027H2 可能先压价格、后暴露库存。
- **技术基线风险**：厂商 benchmark 可能选择最弱对照组；生产模型、缓存命中、数据集和故障处理会显著缩小倍数。
- **软件替代硬件**：更好的 KV 压缩、稀疏读取、缓存复用和模型路由可能降低每 token 所需 flash/HBM 字节。
- **标准碎片化**：CXL、UCIe、HBF、GPU-direct 安全模型若缺乏跨厂互操作，会拖慢资格认证。
- **地缘与出口限制**：先进封装、控制器、NAND/HBM 设备和中国供给变化会改变价格与竞争份额。
- **定义风险**：CXL、互连、控制器与 AI storage TAM 的公开口径差异巨大，市场规模不能跨来源直接相加。

## 来源清单

除另行标明外，以下网页均于 2026-08-18 检索。公司性能数据均保留“厂商披露”属性；没有独立客户材料时，验证状态不高于中等。Terrapinn 的会议主页和议程是滚动页面，下一届上线后可能重定向；本报告因此同时以 FMS26 官方发布快照交叉核对 2026 年日期、地点和名称。

### FMS 官方与 2025 对照

| 日期 | 来源 | 类型 | 用途/验证状态 |
|---|---|---|---|
| 2026 年会前 | [FMS26 官方发布快照](https://futurememorystorage.com/news/press-releases/download/119/FMS26_CFP_PressRelease_FINAL.pdf) | 会议官方 | Future of Memory and Storage、2026-08-04 至 08-06、Santa Clara；高置信 |
| 2026-07/08 更新 | [FMS 2026 官方议程](https://www.terrapinn.com/conference/future-memory-storage/agenda.stm) | 会议官方 | 主题、演讲与技术方向；高置信，议程不等于部署 |
| 2026 | [FMS FAQ](https://www.terrapinn.com/conference/future-memory-storage/frequently-asked-questions.stm) | 会议官方 | 会场、奖项和参会信息 |
| 2025-08 | [FMS 2025 Best of Show](https://futurememorystorage.com/news/press-releases/download/114/FMS%202025%20Best%20of%20Show_FINAL.pdf) | 会议官方 | 证明 HBF/PM1763 等方向 2025 已出现 |
| 2025-08 | [Samsung FMS 2025 回顾](https://news.samsungsemiconductor.com/global/samsung-electronics-presents-vision-for-ai-memory-and-storage-at-fms-2025/) | 公司一手 | PCIe 6.0、液冷、CXL、HBM4/4E 会前基线 |
| 2025-08-04 | [Kioxia FMS 2025 发布](https://americas.kioxia.com/en-us/business/news/2025/ssd-20250804-1.html) | 公司一手 | LC9、BiCS、CXL XL-FLASH 会前基线 |
| 2025-10 | [Kioxia FMS 2025 会后报告](https://americas.kioxia.com/en-us/insights/fms25-202510.html) | 公司一手 | 143M 聚合仿真口径；中置信 |
| 2025 | [NVIDIA GTC25 Storage-Next/SCADA](https://www.nvidia.com/en-us/on-demand/session/gtc25-s73012/) | 公司技术演讲 | 2025 架构成熟度基线 |

### 2026 公司、产品、论文与标准资料

| 日期 | 来源 | 类型 | 用途/验证状态 |
|---|---|---|---|
| 2026-08-04 | [NVIDIA：AI storage at FMS](https://blogs.nvidia.com/blog/ai-storage-fms/) | 公司一手 | cuFile 开放、Storage-Next、SCADA 边界；高置信 |
| 2026 | [NVIDIA GTC26 small-block storage](https://www.nvidia.com/en-us/on-demand/session/gtc26-s81840/) | 公司技术演讲 | 200M/400M IOPS 研究目标；非产品承诺 |
| 2026 | [NVIDIA CMX 技术博客](https://developer.nvidia.com/blog/?p=111143) | 公司一手 | flash context tier 厂商 benchmark；中置信 |
| 2026 | [NVIDIA BlueField-4 STX 合作公告](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption) | 公司/合作伙伴 | H2 平台计划、adoption wording；中置信 |
| 2026 | [Micron 230M IOPS 单服务器演示](https://www.micron.com/about/blog/storage/ssd/sc25-performance-breakthrough-230m-iops-in-a-single-server) | 公司实验 | 实验室聚合上限；非生产部署 |
| 2026-08 | [Samsung FMS 2026 发布](https://news.samsungsemiconductor.com/global/samsung-unveils-next-gen-3d-memory-vision-at-fms-2026-charting-the-future-of-ai-infrastructure/) | 公司一手 | zHBM、zNAND-O、V10、产品组合 |
| 2026-08 | [Samsung FMS 展台回顾](https://news.samsungsemiconductor.com/global/inside-fms-2026-samsung-electronics-showcases-the-future-of-ai-memory/) | 公司一手 | 确认 mockup/model 性质 |
| 2026-07-08 | [Samsung PM1763 量产](https://news.samsungsemiconductor.com/global/samsung-begins-mass-production-of-pm1763-ssd-optimized-for-next-generation-ai-infrastructure/) | 公司一手 | 量产、首批容量、性能 |
| 2026-02-12 | [Samsung HBM4 商业出货](https://news.samsungsemiconductor.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing/) | 公司一手 | HBM4 成熟度 |
| 2026-05-29 | [Samsung HBM4E 样品](https://news.samsungsemiconductor.com/global/samsung-electronics-begins-shipment-of-industry-first-hbm4e-samples/) | 公司一手 | HBM4E 成熟度 |
| 2026-08-03 | [Kioxia FMS 2026 总览](https://americas.kioxia.com/en-us/business/news/2026/ssd-20260803-2.html) | 公司一手 | FMS 产品矩阵 |
| 2026-08-04 | [Kioxia GP1](https://europe.kioxia.com/en-europe/business/news/2026/20260804-2.html) | 公司一手 | 10M IOPS、50 DWPD、年底样品 |
| 2026-08-04 | [Kioxia XL1](https://europe.kioxia.com/content/dam/kioxia/en-europe/business/news/2026/asset/KIE_PR_20260804-1_EN.pdf) | 公司一手 | CXL XL-FLASH、8 月评估样品；仅供评估 |
| 2026-07-30 | [Kioxia CM10](https://europe.kioxia.com/en-europe/business/news/2026/20260730-2.html) | 公司一手 | 功能样品、容量、液冷 |
| 2026-07-29 | [Kioxia NX1](https://europe.kioxia.com/en-europe/business/news/2026/20260729-1.html) | 公司一手 | hyperscaler 样品、液冷 E1.S |
| 2026-05-14 | [Kioxia/Dell 9.8PB/2U](https://americas.kioxia.com/en-us/business/news/2026/ssd-20260514-2.html) | 公司/OEM 配置 | 容量密度和厂商 TCO；无公开采购量 |
| 2026-08-04 | [Kioxia/Sandisk BiCS10 QLC](https://www.sandisk.com/company/newsroom/press-releases/2026/2026-08-04-new-3d-flash-memory-technology-from-kioxia-and-sandisk-qlc-nand) | 公司一手 | 332 层、CBA、密度/接口；尚无量产日 |
| 2026-08 | [Sandisk FMS 2026](https://www.sandisk.com/company/newsroom/press-releases/2026/sandisk-nand-innovation-for-era-of-ai-inference-at-fms-2026) | 公司一手 | HBF、高耐久 KV SSD、路线图 |
| 2026-08 | [SK hynix HBF 开放规范](https://news.skhynix.com/en/hbf-at-fms-2026/) | 公司/标准合作 | 容量、带宽、UCIe、OCP；尚无硅片 |
| 2026 | [FMS 2026 CXL demos](https://computeexpresslink.org/fms-2026-cxl-demos/) | 标准组织 | 会场演示及配置；不等于部署 |
| 2026 | [Meta Vistara 论文](https://aisystemcodesign.github.io/papers/isca26/vistara_camera_ready.pdf) | 论文/客户一手 | 数百万服务器生产部署；高置信 |
| 2026 | [CXL Consortium Vistara webinar](https://computeexpresslink.org/event/scaling-cxl-to-millions-of-servers-vistara-for-hyperscale-efficiency/) | 标准组织/客户 | Vistara 补充验证 |
| 2026-08 | [Marvell AI memory infrastructure](https://investor.marvell.com/news-events/press-releases/detail/1030/marvell-advances-ai-memory-infrastructure-portfolio-to-accelerate-agentic-ai-inference) | 公司一手 | SC6、Structera、Photonic Fabric 成熟度 |
| 2026 | [Marvell 260-lane PCIe 6.0 switch](https://investor.marvell.com/news-events/press-releases/detail/1016/marvell-launches-industrys-first-260-lane-pcie-6-switch-ai-data-center-scale-up-infrastructure) | 公司一手 | 工程/客户样品时间 |
| 2026-08 | [Silicon Motion FMS 2026](https://siliconmotiontechnologycorporation.gcs-web.com/news-releases/news-release-details/huirongkejiliangxiang-fms-2026zhanshimianxiang-agentic-ai) | 公司一手 | SM8366/SM8466 展示与规格 |
| 2026-07-29 | [DDN Infinia 更新](https://www.ddn.com/blog/ddn-infinia-expands-to-power-inference-intelligent-data-lakes-and-multi-protocol-ai-workloads/) | 公司一手 | 推理/RAG benchmark；缺独立复现 |

### 财报、市场与产业数据

| 日期 | 来源 | 类型 | 用途/限制 |
|---|---|---|---|
| 2026-06-24 | [Micron FY2026 Q3 SEC 附件](https://www.sec.gov/Archives/edgar/data/723125/000072312526000013/a2026q3ex991-pressrelease.htm) | 监管文件/公司财报 | 单季收入、毛利、资本开支；高置信 |
| 2026-06-24 | [Micron FY2026 Q3 演示](https://investors.micron.com/static-files/2354ecda-77a0-4ddd-8462-a631eb491356) | 公司投资者材料 | NAND bit/ASP、数据中心 SSD 收入；高置信 |
| 2026 | [Micron HBM TAM](https://investors.micron.com/static-files/530bd7ed-a8c8-4687-af4a-8c129f740e09) | 公司投资者材料 | 2025/2028 HBM 市场与合同；中高置信 |
| 2026 | [Sandisk FY2026 Q4](https://sandisk.gcs-web.com/news-releases/news-release-details/sandisk-reports-fiscal-fourth-quarter-2026-financial-results) | 公司财报 | 收入、毛利、数据中心 mix；高置信 |
| 2026-08 | [Sandisk Investor materials](https://sandisk.gcs-web.com/static-files/c75d1bee-c5c9-4e5a-8605-302c1aeac59b) | 公司预测 | 2027 高景气情景、合同/RPO；中置信 |
| 2026 | [Kioxia Investor Day 2026](https://www.kioxia-holdings.com/content/dam/kioxia-hd/en-jp/ir/library/event/asset/Kioxia-Investor-Day-2026-en.pdf) | 公司投资者材料/第三方数据 | bit CAGR、数据中心需求、资本开支；中高置信 |
| 2026-05-29 | [TrendForce memory market](https://www.trendforce.com/presscenter/news/20260529-13068.html) | 第三方研究 | 2026/2027 NAND/DRAM 收入；中置信 |
| 2026-07-21 | [TrendForce NAND supply-demand](https://www.trendforce.com/presscenter/news/20260721-13148.html) | 第三方研究 | 供给缺口和 2027 拐点；中置信 |
| 2026-06-11 | [TrendForce eSSD 2026Q1](https://www.trendforce.com/presscenter/news/20260611-13092.html) | 第三方研究 | 前五厂收入、价格贡献；中置信 |
| 2026-08-18 | [TrendForce NAND 2026Q2](https://www.trendforce.com/presscenter/news/20260818-13186.html) | 第三方研究 | 前五厂收入与份额、全年收入交叉核验；中置信 |
| 2026-06-02 | [TrendForce HBM/DRAM](https://www.trendforce.com/presscenter/news/20260602-13074.html) | 第三方研究 | HBM wafer/bit share、相对利润；中置信 |
| 2026-08-17 | [TrendForce liquid cooling](https://www.trendforce.com/presscenter/news/20260817-13183.html) | 第三方研究 | 2026/2027 液冷渗透、部件范围；中置信 |
| 2026-07-01 更新 | [IDC Enterprise Storage Systems](https://www.idc.com/promo/enterprise-storage-systems/) | 第三方研究 | 外部存储系统市场；中高置信 |
| 2026-01 | [Frost & Sullivan/HKEX market data](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0130/12005367/2026013000025.pdf) | 监管文件所载第三方研究 | 狭义 CXL、广义互连；定义敏感 |
| 2024 | [Astera Labs SEC S-1/A](https://www.sec.gov/Archives/edgar/data/1736297/000119312524069611/d285484ds1a.htm) | 监管文件 | 较宽 PCIe/CXL TAM 对照；较旧，不作基准 |
| 2026 | [Enterprise SSD controller commercial estimate](https://www.researchandmarkets.com/reports/6123353/enterprise-level-ssd-controllers-market-global) | 商业研究摘要 | 控制器市场规模；低置信、定义不透明 |
| 2026 | [Microchip DCS revenue](https://ir.microchip.com/news-events/press-releases/detail/1395/microchip-provides-data-center-solutions-business-unit-revenue-information) | 公司一手 | storage/PCIe/CXL/switch 收入交叉核验 |
| 2026-04-22 | [VAST Series F](https://www.vastdata.com/press-releases/vast-series-f-financing-at-30-billion-valuation) | 私营公司自报 | bookings/CARR/估值；未经独立同口径核验 |

## 最终判断

FMS 2026 证明 AI 基础设施的竞争正从“谁能提供最多 bit”转向“谁能把最合适的数据，以最少搬运、最低尾延迟和可接受功耗安全地送到 GPU”。短期利润仍由供给紧张、HBM4 和首批 PCIe 6.0 量产决定；中期增量来自高 IOPS SSD、控制器、交换/DPU、液冷和数据放置软件；CXL pooling、HBF、zHBM 与 zNAND-O 仍需硅片、互操作、订单和生产部署四重验证。

因此，未来一年应把量产状态、客户资格、重复订单和可复现生产指标置于发布会峰值规格之上；未来两年则要持续观察供给扩张与软件效率能否抵消 AI 上下文长度和并发增长。只要这两组力量尚未分出胜负，最稳健的研究方法就是把**已量产利润、架构价值量和远期技术期权分开估值**。
