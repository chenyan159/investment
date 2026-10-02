# 行业调研：【DCIM、能控与AI工厂数字孪生】

截至日期：2026-05-08  
研究对象：DCIM、EPMS/BMS/能控、液冷控制、AI 工厂数字孪生、AI 园区级电力和冷却运行软件。  
口径说明：本文把“市场规模”定义为全球 AI 数据中心/AI 工厂相关的新签订单、软件订阅 ARR、控制系统硬件和工程交付收入池。不包含 GPU/ASIC/服务器整机收入，不包含完整土建和主变压器订单，除非该项与能控软件/控制系统深度绑定。  
情景说明：基准、乐观、极度超预期乐观均对 2026 年 AI 基础设施建设保持积极假设。极度超预期情景假设客户愿意为“time to power”和“time to token”支付高溢价，且通过预制化、现场发电、BESS、液冷标准化和数字孪生缩短交付周期。

## 0. 核心结论

1. **DCIM 正在从“资产台账+告警面板”升级为 AI 工厂操作系统的一部分。** 传统 DCIM 关注机柜、资产、空间、功率和告警；AI 工厂要求它实时理解 GPU/ASIC 负载、液冷 TCS 回路、CDU 设定值、UPS/母线/开关柜状态、园区发电和电网信号。真正的增量不是传统 DCIM 软件本身，而是 DCIM + EPMS + BMS + 液冷控制 + GPU 调度 API + 数字孪生的集成层。

2. **2026 年最确定放量的是“可交付的控制基础设施”：EPMS、BMS、智能 PDU/传感器、液冷 CDU 控制、功率/热管理监控、数据接入和虚拟调试。** 这些产品的需求领先服务器上架，因为业主要先证明电力、冷却、并网、冗余和安全联锁可行。纯 DCIM 市场研究口径给 2026 全球 DCIM 约 $4B 级别，但 AI 工厂扩展口径已经是 $25B-$45B 的订单池，2027 可上到 $40B-$75B，极度乐观情景 2028 年滚动收入池可超过 $120B。

3. **数字孪生在 2026 年出现真实拐点。** NVIDIA 于 2026-03-16 发布 Vera Rubin DSX AI Factory reference design 和 Omniverse DSX Blueprint GA；Schneider、AVEVA、ETAP、Cadence、Jacobs、Siemens、Eaton、Vertiv、Trane、Phaidra、Switch、CoreWeave 等同步加入。过去数据中心数字孪生常停留在 BIM/CFD 项目制，2026 开始变成“设计-仿真-采购-虚拟调试-运行-持续优化”的标准工具链。

4. **2026 最可能的技术路径是“人机共管的闭环控制”，不是完全无人自治。** Phaidra/CoreWeave/Applied Digital 已在生产 Grace Blackwell 和 GB200 NVL72 环境验证前馈式 AI 液冷控制，把响应从传统 PID 的 3-5 分钟降到 10 秒内，并把热过冲降低 75%-80%。但超大规模客户仍会要求 fail-safe、人工审批、回退控制和网络隔离。因此 2026 是 AI agent 辅助运行，2027 才会向跨电力、冷却、负载的自动化策略放量。

5. **价值链中长期高毛利/高 ROIC 最可能集中在三层：标准化数字孪生资产库与仿真验证 IP、跨 IT/OT 的闭环控制软件、已认证的高密电力/液冷控制平台。** 纯硬件会受产能和价格周期影响，EPC 服务毛利较低；但能把 GPU token revenue per MW 直接提升、能帮助客户更快并网和投产的软件层，会有更强定价权。

## 1. 需求底座、AI 芯片路径与一手信号

### 1.1 本项目已有 AI 芯片与建设规模底座

本研究沿用项目内两份底稿，不对芯片出货量重新外搜：

- `ai_chip_research_2026_2027.md`：2026 全球 AI 计算芯片/模块产能释放金额基准 $300B-$360B、乐观 $390B-$470B、极度乐观 $520B-$650B；2027 基准 $430B-$520B、乐观 $590B-$720B、极度乐观 $850B-$1,050B。
- `AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`：美国 AI 数据中心建设规模 2026 基准 $400B-$490B、乐观 $540B-$650B；2027 基准 $520B-$650B、乐观 $760B-$950B。该底稿已把电力、冷却、建筑、网络、服务器、存储拆分。

本文对 DCIM/能控/数字孪生的三情景进一步设定如下：

| 情景 | AI 机架与芯片节奏 | 电力与冷却节奏 | 对 DCIM/能控/数字孪生的含义 |
|---|---|---|---|
| 基准 | 2026 B300/GB300、Trainium2、TPU Ironwood、MI350 是主力；Rubin/MI400/TPU8 在 2026H2 试产和首批部署 | 电力接入、变压器、开关柜、CDU、现场调试仍是节奏约束 | DCIM/EPMS/BMS 作为必装项，AI agent 主要做告警归因、热管理建议和局部前馈控制 |
| 乐观 | Blackwell Ultra 稳定，Rubin 2026H2 有可见订单，ASIC 与 GPU 并行扩张 | 预制化和现场发电/BESS 缓解 time to power；液冷供应链标准化加快 | 数字孪生从设计工具变成虚拟调试工具，液冷控制和能耗优化软件进入批量项目 |
| 极度超预期乐观 | 2027 需求明显前置，OpenAI/Meta/Anthropic/Google/AWS 等 GW 级项目争抢可交付电力 | BYOP&C、微电网、柔性负载控制和 800VDC 试点快速扩散 | AI 工厂操作系统出现，客户按“每 MW 多产 token”给闭环控制软件付费 |

### 1.2 近半年/2026 年一手信号

| 公司/来源 | 关键事实 | 对本行业的意义 |
|---|---|---|
| NVIDIA | 2026-03-16 发布 Vera Rubin DSX AI Factory reference design 和 Omniverse DSX Blueprint GA，面向大规模设计、建设和运行的物理精确数字孪生；披露能源是最大瓶颈，美国有超过 $300B 设备积压和超过 200GW 项目在并网队列 | AI 工厂数字孪生从概念进入 NVIDIA 参考架构；能控软件成为并网和投产的关键 |
| Schneider Electric | 2026-03-16 与 NVIDIA、AVEVA 推出 Vera Rubin power/cooling reference design、Omniverse DSX 生命周期数字孪生、Nemotron agentic alarm management 测试；设计支持 480VAC、45°C TCS supply、MaxP/MaxQ 运行点 | 电力、冷却、数字孪生、告警 agent 合流，Schneider 正把 EcoStruxure IT、ETAP、AVEVA 打成 AI 工厂软件栈 |
| Schneider Electric Q1 2026 | Q1 收入 €9.767B，集团有机增长 11.2%；Data Center & Networks 需求双位数增长；Field Services +9%，EcoStruxure advisors 强劲 | 软件、服务、生命周期维护的 attach rate 正在提高 |
| Schneider/Motivair | 2025 收购 Motivair 75% 股权，现金 €850M；2025-09 推完整液冷组合，覆盖 CDUs、RDHx、HDUs、dynamic cold plates、chillers、软件和服务；称行业正越过 140kW/rack，未来需预留 1MW/rack | 液冷控制与 DCIM/BMS 的交叉成为高价值入口；Motivair 扩产 Buffalo、Italy、India，称制造输出翻三倍 |
| Vertiv | 2025Q4 organic orders +252%，TTM organic orders +81%，book-to-bill 约 2.9x，backlog $15B；2026Q1 sales $2.65B +30%，Americas organic +44%，FY2026 sales guide $13.5B-$14.0B，organic +29%-31% | 电力/冷却订单显著领先收入，AI 数据中心控制和服务需求有多年度可见性 |
| Vertiv/NVIDIA | 2026-03 推 Vertiv OneCore Rubin DSX，12.5MW 标准化模块；Vertiv 360AI 参考设计 #026 为 2.3MW、36 racks，其中 16 racks at 127kW，72% direct-to-chip liquid cooling | 预制化容量块和仿真资产会压缩设计周期，DCIM/控制接口需要模块化 |
| Eaton | 2026Q1 sales $7.451B；Electrical Americas orders rolling 12m +42%，其中 data centers 在季度内约 +240%；backlog +$4.4B/+44%；Data Centers & Distributed IT 占 2025 sales 21% | 电力链条订单爆发，EPMS/Brightlayer/Beam DSX 可随硬件一起 attach |
| Eaton/NVIDIA | 2026-03 推 Eaton Beam Rubin DSX，grid-to-chip 模块化电力架构，OpenUSD SimReady 资产可与 compute 模型实时仿真；公司提到柔性负载管理可释放超过 100GW 可用电网容量 | 800VDC、柔性负载、数字孪生三条线绑定，能控软件有明确商业价值 |
| ABB | 2026Q1 Electrification orders $6.647B +51%，backlog $11.46B +40%，data center 订单三位数增长；Operational EBITA margin 24.0% | 电气控制和数字监控具备供不应求定价环境 |
| ABB/VoltaGrid | 2026-03 延长合作，为 AI 数据中心 power projects 供应 35 台带飞轮 synchronous condensers 和 prefabricated eHouse，用于电压稳定、短路支撑、瞬态响应 | AI 负载瞬态让“电能质量+稳定控制”从可选变必选 |
| ABB/NVIDIA | 2025-10 合作开发 800VDC 架构，服务未来 1MW server racks；ABB 称全球 data center demand 从 2024 80GW 到 2030 约 220GW，AI 约占增长 70%，capex 超 $1T | 800VDC/MV UPS/固态断路器是 2027 后的关键技术方向 |
| Siemens/NVIDIA | 2026 CES 扩大合作，面向 AI factories 设计 repeatable blueprint，平衡 power/cooling/automation；Siemens 提供 power infrastructure、electrification、grid integration、automation、digital twins | Siemens 的长处在工业自动化和电力系统数字孪生，适合进入高可靠 AI 工厂运行层 |
| Siemens Energy | FY2026Q1 Grid Technologies 因美国多个数据中心相关订单贡献 high triple-digit million euro，集团 backlog €146B | 电网侧软件、控制、变电站和稳定性需求被 AI 拉动 |
| AVEVA | 2026-03 与 NVIDIA 集成 Omniverse DSX；PI System 将汇聚 BMS、EPMS、cooling systems、server racks、workloads telemetry；Operations Control/UOC 管 UPS、switchgear、PDU、generator、chiller、CDU 等 | 关键不是“3D 模型”，而是把 IT/OT 实时数据接进同一运行中枢 |
| Cadence | 2026-03 宣布 Reality Digital Twin Platform 与 Omniverse libraries 集成，使用 physics-based models + AI 设计和运行 AI factories；Fidelity CFD、Celsius 等可用于热流/多物理仿真 | Cadence/Future Facilities/6SigmaDCX 一类工具从设计阶段进入运行优化阶段 |
| Jacobs | 2026-03 发布 Data Center Digital Twin solution，首个 module 已面向业主/运营商可用，面向 1GW AI data center，未来扩展到 250MW 设计 | EPC/工程公司把数字孪生产品化，可能成为业主投决和虚拟调试工具 |
| Phaidra | 2026-03 与 CoreWeave、Applied Digital、NVIDIA 公布生产环境前馈式液冷控制：热过冲下降 75%-80%，CDU 设定响应从分钟级降到 10 秒内，CoreWeave 将扩展到液冷 fleet | AI cooling agent 已有生产验证，是 2026 最值得跟踪的新技术 |
| nVent | 2026Q1 sales $1.2B +53%，organic +34%，backlog $2.6B；增长来自 grey space 和 white space 数据中心 | 连接、机柜、电力分配、液冷结构件随 AI 机柜密度一起放量 |
| Delta | Data Center World 2026 展出 grid-to-chip 架构；美国已部署 6.5GW UPS；3MW Liquid-to-Liquid CDU 支持 3000 LPM；800VDC 架构可到 1.1MW/rack、最高 98% 效率 | 亚洲电源/楼控厂商在高密 AI 数据中心中具备系统级竞争力 |

## 2. 2026 机遇、挑战、技术路径与成熟/放量时间

### 2.1 行业机遇

1. **AI 机架功率密度快速跨越传统白空间设计边界。** 2026 主力 B300/GB300、GB200、Trainium2/3、TPU Ironwood、MI350、Maia200、MTIA/OpenAI/Broadcom ASIC 都要求更高功率密度、更高热流密度和更严密的遥测。传统 10-30kW/rack 的 DCIM 只看平均功率已经不够，100kW+ rack 需要秒级甚至亚分钟级电力和热响应。

2. **客户从“买设备”转向“买可投产容量”。** Vertiv、Eaton、Schneider、ABB 的订单和 backlog 都显示客户在提前锁电力/冷却/控制能力。软件和数字孪生能直接缩短 time to power、time to token，定价逻辑从软件席位费变成投产节奏和每 MW token 收益。

3. **ASIC 和 GPU 并行扩张提高控制复杂度。** TPU、Trainium、Maia、MTIA、OpenAI/Broadcom ASIC 的电力曲线、散热策略、调度器接口不同。客户需要一套统一的能控层把不同加速器、不同液冷回路和不同园区电源协同起来。

4. **电网瓶颈把 AI 工厂变成“可调负载资产”。** NVIDIA DSX Flex、Emerald AI、Schneider/AlphaStruxure、Vertiv/Generate、ABB/VoltaGrid 等信号说明，未来能证明“负载可控、瞬态可控、能参与需求响应”的 AI 工厂，更容易获得并网批准和融资。

5. **高密液冷从机械工程问题变成控制软件问题。** CDU、chiller、TCS、rack power、GPU scheduler 之间存在热惯性和延迟。谁能把前馈控制、实时仿真和 fail-safe 做稳，谁就有高毛利软件入口。

### 2.2 挑战

| 挑战 | 影响 | 投资含义 |
|---|---|---|
| 数据语义不统一 | BMS、EPMS、DCIM、CDU、PDU、GPU telemetry、CMDB、工单系统、BIM tag 经常不一致 | 有数据规范化、知识图谱、资产模型迁移能力的软件商更值钱 |
| 自动控制安全门槛高 | AI 工厂不允许“黑盒 agent”直接控制 UPS、breaker、CDU、chiller | 可审计、可回退、IEC 62443/UL/数据中心客户认证能力是壁垒 |
| Hyperscaler 内部自研强 | Google/AWS/Microsoft/Meta 有自研 DCIM、调度、能效优化系统 | 外部供应商要卖 hardware-attached software、digital twin assets、工程验证和标准接口 |
| 高密液冷现场风险 | 泄漏、污染、气泡、快接头、过滤、冲洗、压差控制都可能导致宕机 | 传感、预测性维护、清洁度检测、数字化调试价值上升 |
| 软件价值难单独计价 | 工程总包常把控制软件打包在硬件或服务里 | 有平台化 ARR 和跨项目复用能力的厂商估值应高于项目制集成商 |
| 供应链长交期 | 变压器、开关柜、UPS、busway、PDU、PLC、传感器、CDU、阀泵、工程人力都紧 | 预制模块和标准化接口是 2026-2027 订单转收入的关键 |

### 2.3 在 2026/2027 最大出货 AI 芯片背景下的技术要求

| AI 芯片/平台 | 2026-2027 路径 | 对 DCIM/能控/数字孪生的直接要求 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主力，GB300 NVL72 高密整柜 | 100kW+ rack、液冷 TCS、NVLink/NVSwitch 机柜拓扑、MaxP/MaxQ 运行点要进入容量规划和能耗优化 |
| NVIDIA GB200/B200 | 2026 延续放量，部分转为存量扩容 | 已验证液冷/电力架构，适合训练 DCIM 与液冷控制模型 |
| NVIDIA Vera Rubin / Rubin DSX | 2026H2 首批，2027 主力放量 | Vera Rubin NVL72、HBM4、更高功耗密度，需要 DSX/Omniverse 数字孪生、480VAC、45°C TCS、能控与工作负载协同 |
| AWS Trainium2/3 | Trainium2 Rainier 2026 大规模，Trainium3 2026-2027 接棒 | 超大 ASIC pod 的内部调度和 EFA/Neuron fabric 需要设施层理解批量负载斜率，减少同步负载对 cooling/power 的冲击 |
| Google TPU Ironwood / TPU8 | Ironwood 2026 推理主力，TPU8 2027 训练/推理分化 | Google 自研强，但外部 colo/园区和供应链需要数字化电力、冷却和容量验证 |
| AMD MI350/MI400 Helios | MI350 2026 确定性更强，MI400/MI455X 2026H2 首批、2027 放量 | MI400/HBM4/72 GPU rack 提高液冷和电力瞬态难度，UALink/以太网开放路线更需要 vendor-neutral DCIM |
| Microsoft Maia 200 | 3nm、216GB HBM3E、750W SoC、闭环液冷 | Azure 内部闭环为主，但证明高密自研 ASIC 也会带动液冷 HEU、BMS/EPMS 数据融合 |
| Meta MTIA / OpenAI Broadcom ASIC | 2026-2027 从自研推理 ASIC 扩容到 GW 级 | 专用推理负载更适合负载预测和动态功率调度，若 API 开放会放大能控软件价值 |
| Huawei Ascend / 国产 AI 芯片 | 中国 AI 园区国产替代主线 | 单芯片效率不足时会用更大规模集群弥补，带来更强的电力、冷却、可靠性和国产 DCIM/NetEco/iMaster 需求 |
| Cambricon/Alibaba/Baidu 等国产 ASIC | 2026-2027 推理和训练集群扩张 | 软件生态和硬件 telemetry 标准化不足，给本土能控、液冷、运维平台留出机会 |

### 2.4 技术成熟时间和放量时间

| 技术 | 当前状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期成熟/放量 |
|---|---|---|---|---|
| 传统 DCIM SaaS/私有化：资产、容量、告警、能耗 | 已成熟 | 2026 持续放量，随新 AI 白空间必配 | 2026H2 大客户把旧 DCIM 升级为 AI-ready DCIM | 2026 即被打包进每个预制 AI 容量块 |
| EPMS/BMS/SCADA 数据融合 | 已成熟但集成碎片化 | 2026H2 项目放量，2027 成为 AI 工厂标准 | 2026 多数 100MW+ 项目要求统一 data lake | 2026H2 即成为融资/验收要求 |
| 高密 rack PDU/母线/传感器秒级遥测 | 已放量 | 2026 全年随 100kW+ rack 放量 | 2026H2 从分钟级升级到秒级采样 | 2026H2 因闭环控制需求出现溢价和缺货 |
| 液冷 CDU/冷板/泄漏检测控制 | 正在快速放量 | 2026H2 随 GB300/MI350 上量，2027 批量 | 2026H2 直接成为 NVL72 类项目默认配置 | 2026 供不应求，控制系统毛利显著上修 |
| OpenUSD/Omniverse DSX 生命周期数字孪生 | 2026-03 GA，生态形成 | 2026H2 在 1GW/250MW 项目先用，2027 放量 | 2026H2 成为大客户虚拟调试标准 | 2026H2 进入 Switch/CoreWeave/Nscale 类项目批量复制 |
| CFD/热流/电力系统多物理仿真 | 工程设计成熟，运行联动刚起步 | 2026-2027 从离线设计转实时校准 | 2026H2 与 PI/EPMS/BMS 数据闭环 | 2027 成为高密 AI 园区运营必配 |
| AI cooling agent/前馈控制 | Phaidra 已在生产环境验证 | 2026H2 小规模，2027 大规模 | 2026H2 头部云/NeoCloud fleet 扩容 | 2026Q4 形成“每 MW 多 token”收费 |
| Workload-power-cooling 联合调度 | 试点和自研为主 | 2027 商业化，2028 规模化 | 2026H2 在 NVIDIA Mission Control/DSX API 生态试点 | 2027 即成为 AI 工厂操作系统核心 |
| DSX Flex/柔性负载/需求响应 | 2026 商业规模试点计划 | 2027 放量，2028 成熟 | 2026H2 随并网压力进入大项目 | 2027 成为获取并网容量的必要条件 |
| 800VDC/MV UPS/固态断路器控制 | ABB/Eaton/Delta/Hitachi 等 2025-2026 研发/展示 | 2027 试点，2028-2029 放量 | 2027 首批 1MW rack 园区采用 | 2027H2 部分 Rubin/后 Rubin 项目提前采用 |
| Agentic alarm/root-cause/自动工单 | 2026 测试，LLM 可用 | 2026H2 辅助告警，2027 批量 | 2026 就与 Schneider/AVEVA/UOC 集成 | 2027 替代一线 NOC/DC ops 大量人工 triage |

### 2.5 2026 最可能的技术路径

1. **架构形态：标准化容量块 + 仿真资产 + 现场可调参数。** Vertiv OneCore 12.5MW、Eaton Beam DSX、Schneider GB300/Rubin 参考设计、Siemens IEC/UL Rubin blueprint 都指向同一模式：先定义可复用电力/冷却/控制接口，再根据场地调整。

2. **控制层形态：BMS/EPMS/DCIM 不会被单一软件吃掉，而是通过统一数据层和 digital twin 汇聚。** AVEVA PI、EcoStruxure、ETAP、Brightlayer、ABB Ability、Siemens Xcelerator/Building X、Vertiv Environet 等会继续共存，关键在 API、tagging、资产模型和仿真校准。

3. **液冷路径：direct-to-chip 是主线，rear-door/液-空作为 retrofit 和过渡。** 2026 已经越过 100kW/rack，Schneider 指出行业越过 140kW/rack 并预留 1MW+；Delta 展出 3MW CDU；Vertiv 360AI 参考设计 72% direct-to-chip。

4. **运行策略：MaxP/MaxQ 可调运行点进入设施控制。** Schneider/NVIDIA 参考设计明确提到 MaxP/MaxQ，2026 最可能以策略建议、功率上限、预设 setpoint 形式落地，2027 才向自动闭环发展。

5. **电力路径：短期 AC/480V + 48V rack 仍是主流，中期 800VDC/MV UPS 试点。** 2026 大规模项目不会大面积切换 800VDC，但新建 GW 园区会在设计上预留 DC 架构。

## 3. 已经开始放量的关键产品：市场规模、渗透率与利润率

时间定义：  
未来 3 个月 = 2026-05 至 2026-08 新签订单/可确认 ARR；未来 1 年 = 2026-05 至 2027-05 滚动收入/订单池；未来 2 年 = 2027-05 至 2028-05 滚动收入/订单池。  
渗透率 = 新建/扩建 AI 数据中心 IT 负载中采用该类产品或同等自研能力的比例；对 hyperscaler 自研系统，计入渗透率但不全计入外部可获得市场 TAM。

### 3.1 已放量产品收入池

| 细分产品 | 放量证据 | 渗透率路径 | 3 个月市场规模 | 1 年市场规模 | 2 年市场规模 | 毛利率情景 |
|---|---|---|---:|---:|---:|---|
| Core DCIM：资产、容量、空间、能耗、告警、工单 | Gartner Peer Insights 已列 Schneider、Vertiv、Sunbird、Nlyte 等；Precedence 估 2026 纯 DCIM $4.22B；AI 项目改造需求上升 | 2026 AI 新建项目 45%-60%；2027 60%-75%；2028 75%-88%，其中 hyperscaler 多为自研 | 基准 $1.0B-$1.8B；乐观 $1.6B-$2.6B；极度 $2.4B-$3.8B | 基准 $4.8B-$7.0B；乐观 $7B-$10B；极度 $10B-$15B | 基准 $8B-$12B；乐观 $13B-$20B；极度 $20B-$30B | 软件 gross 65%-85%；项目制 blended 35%-55%；供不应求时头部 SaaS/私有化可 80%+ |
| EPMS/电力监控/SCADA：UPS、switchgear、PDU、generator、meter、PQ | Eaton、ABB、Schneider、Siemens Energy 订单强；ABB data center 订单三位数增长，Eaton data center orders 季度约 +240% | AI 新建项目 75%-90%；2028 90%-98% | 基准 $2B-$3.5B；乐观 $3B-$5B；极度 $5B-$8B | 基准 $9B-$14B；乐观 $14B-$22B；极度 $22B-$35B | 基准 $14B-$24B；乐观 $25B-$40B；极度 $40B-$65B | 硬件+软件 blended 38%-58%；纯软件/服务 60%-80%；电气短缺支持价格传导 |
| BMS/热管理监控：chiller、CRAH、CDU、TCS、泵阀、阀门、楼控 | Schneider/AVEVA、Siemens、Johnson Controls、Honeywell、Vertiv、Delta 均在 AI 数据中心集成 | 基础 BMS 85%+；高级热分析 2026 25%-40%，2028 60%-80% | 基准 $1.8B-$3.2B；乐观 $3B-$5B；极度 $4.5B-$7B | 基准 $8B-$13B；乐观 $13B-$22B；极度 $20B-$32B | 基准 $14B-$24B；乐观 $25B-$42B；极度 $40B-$70B | 楼控软件 55%-75%；集成项目 25%-45%；AI 热分析附加模块可 70%-85% |
| 智能 PDU/ePDU/rPDU、rack sensors、母线监测、环境传感 | Legrand/Raritan/Server Technology/Starline、nVent、Eaton、Vertiv、Schneider、Delta 全面受益；高密机架需要细粒度遥测 | 2026 60%-75%；2027 75%-88%；2028 85%-95% | 基准 $3B-$5B；乐观 $5B-$8B；极度 $8B-$12B | 基准 $12B-$20B；乐观 $20B-$32B；极度 $32B-$48B | 基准 $20B-$35B；乐观 $35B-$55B；极度 $55B-$85B | 硬件 gross 25%-45%；高端 metered/switched PDU 和短缺型号可 40%-55% |
| 液冷 CDU 控制、leak detection、过滤/洁净度监控、TCS loop control | Schneider/Motivair、Vertiv、Delta、nVent、CoolIT、Boyd、Danfoss、Parker 等随 direct-to-chip 放量 | 液冷 attach rate：2026 30%-50%；2027 50%-70%；2028 65%-85%；高端 NVL72 类项目接近 100% | 基准 $1.5B-$3B；乐观 $3B-$5B；极度 $5B-$8B | 基准 $6B-$12B；乐观 $12B-$20B；极度 $20B-$32B | 基准 $12B-$25B；乐观 $25B-$40B；极度 $40B-$65B | 控制/传感 gross 40%-60%；软件 65%-85%；CDU 硬件 blended 25%-45%；高端交付可溢价 |
| 数字孪生设计包：CFD、电力系统仿真、BIM-to-ops、虚拟调试 | Schneider ETAP/EcoStruxure IT Design CFD、Cadence Reality、Jacobs、Siemens、Dassault、Bentley、Autodesk、NVIDIA DSX | 2026 15%-25%；2027 35%-55%；2028 55%-75%；1GW 项目更高 | 基准 $0.8B-$2B；乐观 $1.5B-$3B；极度 $3B-$5B | 基准 $3B-$7B；乐观 $7B-$12B；极度 $12B-$20B | 基准 $8B-$18B；乐观 $18B-$35B；极度 $35B-$60B | 仿真软件 gross 75%-90%；工程服务 25%-45%；平台化资产库 blended 55%-75% |
| 能源优化/微电网/BESS/现场发电控制 | Schneider/AlphaStruxure、Vertiv/Generate、ABB/VoltaGrid、Eaton Brightlayer Energy、GE Vernova、Siemens Energy、Tesla/Fluence | 2026 AI 项目 15%-25%；2027 30%-50%；2028 45%-70%，电力受限地区更高 | 基准 $1B-$3B；乐观 $3B-$5B；极度 $5B-$9B | 基准 $5B-$12B；乐观 $12B-$25B；极度 $25B-$40B | 基准 $15B-$35B；乐观 $35B-$65B；极度 $65B-$100B | 控制软件 60%-85%；BESS/发电项目 blended 15%-35%；调度优化平台可高毛利 |
| 统一运维平台/UOC/NOC、告警归因、工单自动化、服务合约 | AVEVA UOC、Schneider services、Vertiv Services、Eaton lifecycle services、Siemens/ABB service | 2026 35%-50%；2027 50%-70%；2028 70%-85% | 基准 $2B-$4B；乐观 $4B-$7B；极度 $7B-$10B | 基准 $10B-$20B；乐观 $20B-$35B；极度 $35B-$55B | 基准 $22B-$45B；乐观 $45B-$75B；极度 $75B-$120B | 服务 gross 25%-45%；托管运维和软件订阅 50%-75%；紧缺工程师推高费率 |

### 3.2 已放量产品增长率区间

| 产品 | 基准增长 | 乐观增长 | 极度超预期增长 |
|---|---:|---:|---:|
| Core DCIM | 2026-2028 CAGR 25%-35% | 35%-50% | 55%-75% |
| EPMS/电力监控/SCADA | 30%-45% | 50%-65% | 70%-95% |
| BMS/热管理监控 | 30%-45% | 45%-65% | 65%-90% |
| 智能 PDU/传感/母线监测 | 35%-50% | 50%-70% | 75%-100% |
| 液冷控制/泄漏检测 | 55%-80% | 80%-110% | 110%-160% |
| 数字孪生设计/仿真 | 70%-100% | 100%-150% | 150%-220% |
| 微电网/BESS/能控 | 70%-110% | 110%-170% | 180%+ |
| UOC/运维自动化/服务 | 40%-60% | 60%-90% | 90%-130% |

## 4. 在研和新兴关键产品：未来快速增长方向

### 4.1 在研/早期商业化产品市场预测

| 在研/新兴方向 | 当前状态 | 渗透率路径 | 3 个月市场规模 | 1 年市场规模 | 2 年市场规模 | 利润率情景 |
|---|---|---|---:|---:|---:|---|
| Omniverse DSX/OpenUSD AI 工厂生命周期数字孪生 | NVIDIA DSX Blueprint 2026-03 GA，Schneider/AVEVA/ETAP、Cadence、Jacobs、Siemens、Eaton、Vertiv 等接入 | 2026 <10% AI MW；2027 20%-40%；2028 45%-70% | 基准 $0.2B-$0.6B；乐观 $0.6B-$1.2B；极度 $1.2B-$2.5B | 基准 $1B-$3B；乐观 $3B-$6B；极度 $6B-$10B | 基准 $7B-$15B；乐观 $15B-$30B；极度 $30B-$60B | 平台/资产库 gross 75%-90%；生态集成 blended 45%-70% |
| AI cooling agent：液冷前馈控制、CDU setpoint agent、chiller agent | Phaidra 已生产验证，热过冲降 75%-80%，响应 <10 秒 | 2026 <5%；2027 15%-35%；2028 35%-60% | 基准 $0.1B-$0.4B；乐观 $0.4B-$0.9B；极度 $0.9B-$1.8B | 基准 $0.8B-$2B；乐观 $2B-$5B；极度 $5B-$9B | 基准 $5B-$12B；乐观 $12B-$25B；极度 $25B-$50B | 软件 gross 75%-90%；按节能/算力增益分成可产生超额毛利 |
| Workload-power-cooling 联合调度：MaxQ/MaxP、DPS、GPU scheduler 连接设施层 | Schneider/NVIDIA 参考设计已提 MaxQ，Phaidra 集成 DSX Max-Q；多数仍是 hyperscaler 自研 | 2026 <5%；2027 10%-25%；2028 30%-55% | 基准 $0.2B-$0.6B；乐观 $0.6B-$1.5B；极度 $1.5B-$3B | 基准 $1B-$3B；乐观 $3B-$7B；极度 $7B-$12B | 基准 $8B-$20B；乐观 $20B-$45B；极度 $45B-$90B | 若按 token/MW 增益收费，gross 80%-90%；若项目交付 blended 45%-65% |
| DSX Flex/柔性负载/需求响应/并网可信控制 | NVIDIA/Emerald AI 2026 商业规模试点计划；电网侧关心可控负载 | 2026 <3%；2027 10%-25%；2028 25%-50% | 基准 $0.05B-$0.3B；乐观 $0.3B-$0.8B；极度 $0.8B-$1.5B | 基准 $0.8B-$2.5B；乐观 $2.5B-$6B；极度 $6B-$12B | 基准 $8B-$25B；乐观 $25B-$55B；极度 $55B-$110B | 纯软件/交易平台 70%-90%；需求响应收益分成可能高 ROIC |
| 800VDC/MV UPS/固态断路器 + DC 能控 | ABB/NVIDIA、Eaton、Delta、Hitachi 等在 2025-2026 推架构与仿真 | 2026 <5%；2027 5%-15%；2028 15%-35%；1MW rack 项目更快 | 基准 $0.3B-$1B；乐观 $1B-$2B；极度 $2B-$4B | 基准 $2B-$6B；乐观 $6B-$12B；极度 $12B-$25B | 基准 $12B-$40B；乐观 $40B-$80B；极度 $80B-$150B | 硬件 gross 30%-45%；控制软件 60%-80%；先发认证有高溢价 |
| Cognitive DCIM：知识图谱、语义模型、LLM root-cause、自动工单 | 论文和产品试点阶段，Schneider 测 Nemotron alarm management | 2026 5%-10%；2027 20%-35%；2028 40%-60% | 基准 $0.1B-$0.3B；乐观 $0.3B-$0.8B；极度 $0.8B-$1.5B | 基准 $0.5B-$1.5B；乐观 $1.5B-$4B；极度 $4B-$8B | 基准 $3B-$10B；乐观 $10B-$25B；极度 $25B-$50B | SaaS gross 75%-90%；专业服务影响初期毛利 |
| 预测性泄漏/污染/过滤/冷却液健康监控 | 学术与供应商原型活跃，液冷 fleet 扩容后刚需 | 2026 10%-20%；2027 25%-45%；2028 50%-75% | 基准 $0.1B-$0.3B；乐观 $0.3B-$0.7B；极度 $0.7B-$1.2B | 基准 $0.6B-$2B；乐观 $2B-$5B；极度 $5B-$9B | 基准 $3B-$8B；乐观 $8B-$18B；极度 $18B-$35B | 传感硬件 30%-50%；分析软件 70%-85%；宕机风险定价力强 |
| 自动虚拟调试/施工数字线程：BIM/PLM/Procore/Jacobs/PTC/DSX | Jacobs first module available；Procore/PTC 接入 DSX | 2026 10%-20%；2027 30%-50%；2028 50%-70% | 基准 $0.2B-$0.8B；乐观 $0.8B-$1.8B；极度 $1.8B-$3B | 基准 $1B-$4B；乐观 $4B-$9B；极度 $9B-$15B | 基准 $6B-$18B；乐观 $18B-$40B；极度 $40B-$80B | 工程服务 25%-45%；平台订阅 70%-85%；项目复用越高毛利越高 |

### 4.2 最值得押注的新技术

1. **AI cooling agent 和 workload-aware cooling。** 这是最接近商业化且 ROI 最清楚的方向。它可以减少过冷、提高供水温度、避免 GPU throttle，把 cooling power 和 stranded power 转成 IT compute。Phaidra 的生产验证给了非常强的一手信号。

2. **AI 工厂 digital twin asset library。** 单个 1GW 园区包含数十万资产、上万连接关系和复杂联锁。谁能提供可复用 SimReady/OpenUSD 资产、ETAP 电力模型、CFD 模型和运行遥测映射，谁就会在项目前期被锁定。

3. **柔性负载和并网可信控制。** 如果电网愿意因为 AI 工厂能证明快速降载/升载、可控 ramp rate、能配合现场发电而批准更大接入容量，这类软件的价值可能超过传统节能软件。

4. **800VDC 过渡控制。** 2026 不是大规模收入年，但 2027-2028 会成为高密机架分水岭。ABB HiPerGuard、SACE Infinitus、Eaton Beam DSX、Delta 800VDC 架构都是早期信号。

5. **Cognitive DCIM/agentic alarm management。** 人才短缺会让高质量告警归因和自动工单非常值钱，但前提是有干净资产模型和运行数据。单纯 LLM chat 不构成壁垒，OT 语义和闭环可审计才构成壁垒。

## 5. 供给侧：产能结构、瓶颈、成本和毛利

### 5.1 产能结构

| 环节 | 主要地区 | 主要公司/生态 | 产能特点 |
|---|---|---|---|
| DCIM/能控软件 | 美国、法国、德国、瑞士、英国、中国、台湾 | Schneider/EcoStruxure/ETAP/AVEVA、Eaton/Brightlayer、Vertiv、Siemens、ABB、Sunbird、FNT、Nlyte、Hyperview、Huawei NetEco、Delta InfraSuite | 软件开发不缺物理产能，缺行业数据模型、现场经验、客户认证和集成能力 |
| EPMS/BMS/SCADA 控制硬件 | 美国、欧洲、中国、印度、墨西哥、台湾 | Schneider、Eaton、ABB、Siemens、Honeywell、Johnson Controls、Delta、Mitsubishi、Rockwell、Emerson | PLC、网关、meter、保护装置、BMS controller 受电子元件和认证约束 |
| 智能 PDU/母线/机柜传感 | 美国、墨西哥、欧洲、中国、台湾 | Legrand/Raritan/Server Technology/Starline、Eaton、Schneider、Vertiv、nVent、Panduit、Rittal、Delta | 高端 metered/switched PDU、busway tap-off、传感器和连接器需要提前排产 |
| 液冷控制/设备 | 美国、加拿大、意大利、德国、丹麦、印度、中国、台湾 | Schneider/Motivair、Vertiv/ThermoKey、CoolIT、Boyd、Modine/Airedale、Danfoss、Parker、nVent、Delta、Submer、LiquidStack、GRC、ZutaCore、JetCool | CDU、冷板、快接头、阀泵、过滤、泄漏检测和现场维护团队是交付瓶颈 |
| 电力数字孪生/CFD/多物理仿真 | 美国、法国、德国、英国 | NVIDIA Omniverse、Cadence Reality/Fidelity、Schneider ETAP、AVEVA、Siemens Xcelerator/Simcenter、Dassault、Synopsys/Ansys、Jacobs、Bentley、Autodesk | 软件能力强，但高质量资产库、校准数据和工程模板稀缺 |
| 微电网/现场能源控制 | 美国、欧洲、中国 | Schneider/AlphaStruxure、Vertiv/Generate、ABB/VoltaGrid、Eaton、GE Vernova、Siemens Energy、Tesla、Fluence、Wartsila、Stem、Caterpillar、Cummins、Bloom Energy | 项目制强，受发电设备、燃气接入、BESS、并网许可和融资结构约束 |

### 5.2 供给瓶颈

| 瓶颈 | 为什么重要 | 2026-2027 影响 |
|---|---|---|
| OT+IT+AI 复合人才 | 需要同时懂 UPS/开关柜、BMS、液冷、GPU 集群、网络、数据建模、安全 | 交付工程师费率上升；头部厂商服务 attach rate 提高 |
| 语义模型和数据清洗 | 同一个 PDU、rack、CDU 在 BIM、CMDB、DCIM、BMS 中名字不同 | 没有资产语义就不能做自动 root-cause 和数字孪生闭环 |
| 控制安全和认证 | AI agent 不能无约束控制高压电、冷却和负载 | 认证和客户验收周期限制新 entrants；利好 Schneider/Eaton/ABB/Siemens/Vertiv |
| 长交期硬件 | meter、PLC、PDU、busway、UPS、CDU、传感器和快接头都可能缺货 | 订单提前，价格上行；软件绑定硬件的厂商更容易获单 |
| 现场虚拟调试能力 | AI 园区建设速度快，现场变更多，传统调试无法满足 | Jacobs/DSX/ETAP/Cadence/AVEVA 类工具需求上升 |
| 液冷洁净度和泄漏风险 | 冷却液污染、微漏、气泡、过滤失败会造成宕机或保修纠纷 | 泄漏检测、洁净度监测、预测维护高增长 |
| 数据主权和网络隔离 | AI 工厂运行数据是核心资产，云 SaaS 难进入部分 hyperscaler/政府/主权 AI | 私有化部署、edge analytics、on-prem license 仍有市场 |
| 接口碎片化 | Modbus、BACnet、SNMP、OPC UA、Redfish、OCP、厂商私有 API 并存 | 中间件、网关、semantic layer 成为高价值小环节 |

### 5.3 成本结构和价格传导

| 产品 | 成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| Core DCIM SaaS/私有化 | R&D 20%-30%；云/托管 5%-12%；实施/迁移 20%-35%；支持 8%-15%；销售渠道 15%-25% | 是否可跨项目复用、是否有资产模型迁移工具、是否被客户运维流程锁定 | 按 site/MW/rack/device/模块订阅；AI 高密项目可按 MW 或资产数溢价 |
| EPMS/BMS 项目 | meter/PLC/gateway/protection 30%-45%；panel/integration 15%-25%；SCADA 软件 10%-20%；工程调试 20%-30% | 认证、可靠性、与开关柜/UPS/PDU 硬件绑定程度、项目交付风险 | 硬件缺货和交付期直接传导；软件通常随硬件 bundle |
| 智能 PDU/传感器 | 电源/测量芯片/继电器/MCU/通信 35%-50%；金属/外壳 15%-25%；制造测试 15%-25%；渠道 10%-20% | 高精度计量、远程切换、温湿度/压差/漏液集成、交期 | 高端型号按 rack 密度和交期定价；替换成本高 |
| 液冷控制 | PLC/edge controller/sensors/leak detection 20%-30%；阀泵/VFD/接口 25%-35%；软件 10%-20%；测试/冲洗/调试 20%-30% | 可靠性、清洁度、GPU/OEM 认证、控制算法、现场服务 | 供不应求时按 CDU capacity、rack density、SLA 溢价 |
| 数字孪生/仿真 | 软件 license/云/HPC 15%-30%；工程建模 30%-45%；数据接入 20%-30%；校准维护 10%-20% | 模型精度、资产库复用率、是否能进入运营闭环 | 大项目按 MW/site 和模块收费；虚拟调试若缩短工期可收成功费 |
| AI agent 能控 | 模型开发/RL/仿真 25%-35%；数据接入 20%-30%；安全验证 15%-25%；持续监控 10%-20% | 是否能证明节能、少 throttle、多 token、少宕机 | 按节能分成、按释放 IT power 分成、按 MW/年订阅 |

## 6. 竞争格局、壁垒和价值捕获

### 6.1 市场结构

1. **传统 DCIM 分散，但 AI 工厂 digital twin 初期高度集中。** 传统 DCIM 有 Schneider、Eaton、Vertiv、Sunbird、Nlyte、FNT、Hyperview、Cormant、Device42、Panduit 等数十家；但 2026 的 AI 工厂数字孪生被 NVIDIA DSX 生态牵引，Schneider/AVEVA/ETAP、Cadence、Jacobs、Siemens、Eaton、Vertiv、Dassault、PTC、Procore 等头部更容易拿首批项目。

2. **硬件/控制集成集中在电气和热管理龙头。** Schneider、Vertiv、Eaton、ABB、Siemens、Legrand、nVent、Delta、Johnson Controls、Honeywell、Trane、Carrier 等拥有客户认证、服务网络和硬件 supply chain。高密 AI 项目倾向找能承担责任的龙头。

3. **Hyperscaler 内部系统强，外部供应商主要通过“工程验证+硬件绑定+资产库”进入。** Google/AWS/Microsoft/Meta/NVIDIA/CoreWeave/Switch/xAI 等会自研调度和运维，但仍需要电力/冷却 vendor 提供 validated designs、SimReady assets、设备 telemetry、现场服务和保修边界。

4. **中国市场将形成独立生态。** 华为 NetEco/iMaster/FusionDC、科华、英维克、维谛中国、台达、曙光/浪潮/联想相关平台、运营商自研系统会与海外生态分化。国产 AI 芯片效率和供应链约束会放大系统级能控价值。

### 6.2 可量化壁垒

| 壁垒 | 为什么能定价 | 量化观察指标 |
|---|---|---|
| 客户认证和运行记录 | AI 工厂宕机损失远高于软件费用，客户偏好用有大型数据中心 uptime 记录的 vendor | 已部署 MW/GW、critical incident rate、SLA、客户名单 |
| 高密 rack/liquid cooling 知识 | 100kW+ rack 的热惯性、压差、过滤、泄漏、GPU throttle 非通用楼控可解决 | 支持 rack density、CDU capacity、响应时间、热过冲减少比例 |
| IT/OT 数据模型 | 能把 rack、GPU、job、PDU、CDU、breaker、BMS tag 连接起来才可自动诊断 | 已建资产模型数量、设备协议数量、数据延迟、tag 映射自动化率 |
| 仿真资产库和模型校准 | 真实可用的数字孪生需要设备几何、性能曲线、联锁逻辑和运行数据 | SimReady/OpenUSD 资产数量、CFD/ETAP 模型精度、虚拟调试节省工期 |
| 安全和可审计控制 | AI agent 若影响 UPS、cooling、breaker，必须可解释、可回退、可审计 | IEC 62443、SOC2、客户安全审计、fail-safe 模式、人工审批流程 |
| 服务网络 | 液冷和电力控制需要现场维护，跨国客户要全球交付 | field service tech 数量、备件库、响应时长、区域覆盖 |
| 供应链和产能 | CDU、PDU、meter、PLC、传感器、busway 供不应求时交付就是定价权 | backlog、book-to-bill、lead time、扩产计划 |
| 切换成本 | DCIM/EPMS/BMS 一旦与工单、SOP、合规报告、设备保修绑定，替换风险高 | 软件续费率、site retention、平均合同年限、迁移成本 |

### 6.3 价值捕获判断

| 价值链层级 | 长期 ROIC/毛利潜力 | 原因 |
|---|---|---|
| AI 工厂闭环控制软件：workload-power-cooling | 最高 | 直接影响 token/MW、节能、避免 throttle、并网可信度；软件复用率高 |
| 数字孪生资产库/仿真验证 IP | 很高 | 前期锁定业主和 EPC，模型可跨项目复用，客户切换成本高 |
| 电力/液冷控制平台 | 高 | 硬件+软件+服务绑定，认证壁垒高，供不应求期间有溢价 |
| Core DCIM | 中高 | 软件毛利高，但产品同质化和 hyperscaler 自研压制定价 |
| 智能 PDU/传感器 | 中 | 高端产品有定价权，但硬件周期性和多供应商竞争明显 |
| EPC/系统集成 | 中低到中 | 需求强但人力密集，项目风险高；龙头可通过模板化提升毛利 |
| Commodity BMS/仪表 | 中低 | 必需但可替代，除非绑定关键认证和数据平台 |

## 7. 2026 关键变化：拐点与最可能放量子方向

### 拐点 1：Blackwell Ultra/GB300 和高密液冷机柜把 DCIM 拉进秒级热电控制

2026 年最确定的硬件主线是 Blackwell Ultra/GB300、Trainium2、TPU Ironwood、MI350 等放量。机柜从几十 kW 迈向 100kW+，传统“每 5 分钟/15 分钟读取一次功率和温度”的 DCIM 不够用。放量子方向：

- 智能 PDU、rack-level power telemetry、漏液/压差/流量传感。
- CDU/TCS 与 BMS/EPMS 的数据打通。
- 高密 rack 容量规划，从平均功率改为 load profile 和 ramp profile。
- 液冷运维服务和预测性维护。

### 拐点 2：NVIDIA DSX 让 AI 工厂数字孪生标准化

2026-03 的 Vera Rubin DSX 和 Omniverse DSX Blueprint 是行业结构性事件。它把 Schneider/AVEVA/ETAP、Cadence、Jacobs、Siemens、Eaton、Vertiv、Trane、Phaidra 等纳入统一参考架构。放量子方向：

- OpenUSD/SimReady 设备资产库。
- ETAP/CFD/thermal-fluid/power distribution 模型。
- 1GW/250MW reference design 数字孪生。
- 虚拟调试和设计协同。
- 运行阶段 real-time twin 和 anomaly detection。

### 拐点 3：电力瓶颈推动能控成为并网和融资工具

2026 年电力瓶颈已经从风险变成主要建设约束。NVIDIA 披露美国超过 $300B 设备 backlog 和超过 200GW 并网队列；Eaton、ABB、Siemens Energy、Vertiv 都在订单和合作中验证。放量子方向：

- 微电网/BYOP&C 控制。
- BESS 和现场发电 dispatch。
- 柔性负载/DSX Flex/需求响应。
- 电能质量、同步调相机、飞轮、瞬态支撑。
- 电网侧数字孪生和并网可信控制。

## 8. 2027 关键变化：拐点与最可能放量子方向

### 拐点 1：Rubin/HBM4/MI400/TPU8 把“数字孪生先行”变成项目标准

2027 更大规模 Rubin、MI400、TPU8、Trainium3/4、OpenAI/Broadcom/Meta ASIC 将推动更高 rack power 和更复杂的互连/冷却。业主会要求在土建、设备采购、现场调试前用数字孪生验证电力、冷却、网络、维修空间和事故场景。放量子方向：

- DSX-aligned reference design。
- 生命周期 asset information management。
- 运行数据校准 CFD/ETAP 模型。
- 工程公司数字孪生交付包。

### 拐点 2：Agentic controls 从 advisory 走向闭环

2026 是液冷 agent 验证年，2027 会进入更广泛 closed-loop。尤其推理 workload 可预测性更高，适合动态 power cap、供水温度、chiller staging、BESS dispatch 联合优化。放量子方向：

- AI cooling agent。
- GPU scheduler 与 BMS/EPMS API。
- MaxQ/MaxP 自动策略。
- 故障 root-cause 和自动工单。
- SLA-aware dynamic power allocation。

### 拐点 3：AI 工厂成为电网资产

2027 年 AI 工厂若能证明可快速响应电网信号，可能获得更快并网、更优 PPA、更低 demand charge，甚至获得需求响应收入。放量子方向：

- DSX Flex/柔性负载控制。
- Utility interconnection digital proof。
- AI data center BESS optimization。
- On-site generation + load orchestration。
- 电能质量和瞬态稳定控制。

## 9. 头部公司和细分玩家清单

### 9.1 Core DCIM/资产容量/运维

| 公司 | 代表产品/优势 |
|---|---|
| Schneider Electric | EcoStruxure IT、EcoStruxure IT Advisor、Data Center Expert、EcoStruxure IT Design CFD；与 ETAP、AVEVA、Motivair 协同最完整 |
| Eaton | Brightlayer Data Centers suite：DCPM、EPMS、DITPM；电力硬件和软件 attach 能力强 |
| Vertiv | Environet、Vertiv Intelligence、360AI/OneCore，电力+冷却+服务绑定 |
| ABB | ABB Ability Data Center Automation，电气自动化和 power monitoring 强 |
| Siemens | Desigo CC、Building X、SICAM、Xcelerator、Simcenter，工业自动化和数字孪生强 |
| Johnson Controls | OpenBlue、Metasys，楼控和 chiller 生态强 |
| Honeywell | Forge、楼宇自动化、BMS/安防集成 |
| Huawei | NetEco、iMaster、FusionDC，中国/中东/新兴市场强 |
| Delta | InfraSuite Manager、楼控、电源和 CDU 控制结合 |
| Sunbird Software | DCIM 纯软件代表，资产和容量管理口碑强 |
| Nlyte | 老牌 DCIM，资产、容量、工作流；适合企业和 colo |
| FNT Software | FNT Command，网络/设施资源管理强 |
| Hyperview | 云原生 DCIM，适合多站点和边缘 |
| Cormant | Cormant-CS，资产、连接和容量管理 |
| Panduit | SmartZone、物理基础设施和连接 |
| Device42/Freshworks | IT asset/CMDB discovery，可与 DCIM 互补 |

### 9.2 电力监控、EPMS、能控、微电网

| 公司 | 代表产品/优势 |
|---|---|
| Schneider Electric / ETAP / AVEVA | ETAP 电力系统数字孪生、Power Monitoring Expert、Power SCADA Operation、AVEVA PI/UOC、AlphaStruxure 微电网 |
| Eaton | Brightlayer、Foreseer/EPMS、Beam DSX、UPS/switchgear/busway，数据中心订单动能强 |
| ABB | ABB Ability、HiPerGuard MV UPS、SACE Infinitus、synchronous condenser、VoltaGrid 合作 |
| Siemens / Siemens Energy | SICAM、grid integration、Noedra、Grid Technologies、数字孪生和自动化 |
| GE Vernova / GridOS | 电网数字化、发电和 grid digital twin |
| Hitachi Energy | 变压器、HVDC、grid edge、数字电网 |
| Delta | UPS、BESS、电源、800VDC、楼控统一控制 |
| Tesla / Fluence / Wartsila / Stem | BESS 和能源优化 |
| Caterpillar / Cummins / Bloom Energy / Enchanted Rock / VoltaGrid | 现场发电、燃料电池、微电网与电能质量 |
| Emerald AI / Gridmatic | 柔性负载、需求响应、AI 工厂电网协同 |

### 9.3 AI 工厂数字孪生、CFD、工程仿真

| 公司 | 代表产品/优势 |
|---|---|
| NVIDIA | Omniverse DSX Blueprint、DSX Max-Q、DSX Flex、OpenUSD/SimReady 生态 |
| Schneider Electric | ETAP、EcoStruxure IT Design CFD、AI factory reference designs |
| AVEVA | CONNECT、PI System、Asset Information Management、Process Simulation、Operations Control/UOC |
| Cadence | Reality Digital Twin Platform、Fidelity CFD、Celsius、Clarity；原 Future Facilities/6SigmaDCX 能力 |
| Siemens | Xcelerator、Digital Twin Composer、Simcenter、Building X、工业 AI OS |
| Dassault Systemes | CATIA、3DEXPERIENCE、Model-Based Systems Engineering、Virtual Twin |
| Synopsys/Ansys | Fluent、Icepak、Twin Builder、多物理仿真和数字孪生 |
| Jacobs | Data Center Digital Twin solution，1GW/250MW reference design |
| Bentley Systems | iTwin、基础设施数字孪生 |
| Autodesk | BIM/Revit/Construction Cloud，与数字线程互补 |
| PTC | Windchill/PLM，与 DSX Accelerator/BOM 管理连接 |
| Procore | 施工数字线程和项目协同 |
| Hexagon / Trimble | 工程测量、施工数字化、资产数据 |

### 9.4 液冷、热管理和 AI 控制

| 公司 | 代表产品/优势 |
|---|---|
| Schneider/Motivair | CDUs、RDHx、HDUs、dynamic cold plates、chillers、EcoStruxure 软件和全球服务 |
| Vertiv | XDU、CoolLoop、OneCore、360AI、ThermoKey heat rejection |
| CoolIT Systems | Direct liquid cooling 冷板/CDU，高端 AI 服务器生态强 |
| Boyd | 冷板、热管理、液冷系统 |
| Modine/Airedale | chiller、CRAH、冷却系统 |
| Danfoss / Parker | 泵阀、换热、流体控制关键部件 |
| nVent | 液冷和电力连接/保护/机柜方案 |
| Delta | 3MW CDU、UPS、楼控、电源 |
| Trane Technologies / Carrier / Johnson Controls | chiller、冷站、楼控和服务 |
| Submer / LiquidStack / GRC / Asperitas | 浸没式液冷和相关控制 |
| ZutaCore / JetCool / Accelsius | 两相冷却、微通道、直接芯片冷却等新方案 |
| Phaidra | AI cooling agent、前馈液冷控制、DSX Max-Q 集成 |
| Vigilent / EkkoSense / Coolgradient | AI 热管理、冷却优化、数据中心热分析 |

### 9.5 白空间硬件、PDU、母线、连接和机柜

| 公司 | 代表产品/优势 |
|---|---|
| Legrand | Raritan、Server Technology、Starline、USystems、Minkels；智能 PDU、母线、rear-door cooling |
| Eaton | busway、PDU、UPS、rack power、Brightlayer |
| Schneider Electric | APC、PDU、UPS、机柜、EcoStruxure |
| Vertiv | rack PDU、UPS、机柜、power/cooling integrated systems |
| nVent | Schroff、Hoffman、Caddy、Erico、Trachte 等连接和保护 |
| Panduit | cabling、SmartZone、物理基础设施 |
| Rittal | 机柜、冷却、配电 |
| Amphenol / TE Connectivity | 高速连接器、铜互联、电力连接 |
| Belden / CommScope | 结构化布线和连接 |
| Delta / Lite-On / Chicony / AcBel | 电源、PDU、模块电源和亚洲供应链 |

### 9.6 需求侧和平台生态关键客户

| 类别 | 公司/项目 |
|---|---|
| Hyperscaler | Microsoft Azure、Amazon AWS、Google Cloud、Meta、Oracle |
| AI 原生/NeoCloud | OpenAI/Stargate、CoreWeave、xAI、Crusoe、Applied Digital、Nscale、Lambda、Nebius、Core42、Hut 8 |
| 数据中心开发商/REIT | Digital Realty、Equinix、QTS、Vantage、Switch、Aligned、DataBank、Stack、NTT Global Data Centers、Compass |
| 芯片/系统平台 | NVIDIA、AMD、Broadcom、Marvell、Intel、AWS Annapurna、Google TPU、Microsoft Maia、Huawei Ascend、Cambricon |

## 10. 投资结论

### 10.1 最强 alpha

1. **Schneider Electric/ETAP/AVEVA/Motivair 生态。** 从电力、液冷、DCIM、工业数据、数字孪生到服务全覆盖，且与 NVIDIA DSX 绑定紧。AI 工厂软件栈完整度最高。

2. **Eaton 和 ABB 的电力控制链。** 数据中心订单、backlog 和 800VDC/MV UPS/柔性负载方向都验证了“电力先行”的投资逻辑。它们不仅卖设备，还在控制、仿真和电能质量中建立壁垒。

3. **Vertiv 的预制化 power/cooling blocks。** Vertiv backlog 和订单增长极强，OneCore/360AI 把硬件、控制和服务打包，直接服务 time to capacity。

4. **Cadence/Jacobs/NVIDIA DSX 生态中的数字孪生资产。** 若数字孪生成为 1GW/250MW 项目投决和虚拟调试标准，复用型资产库会有很高毛利。

5. **Phaidra 类 AI cooling agent。** 生产环境数据已经显示能降低热过冲和释放 power headroom。如果 2027 可证明增加 token revenue per MW，定价上限会很高。

### 10.2 最强 beta

1. **液冷控制和传感。** 直接受 rack density 上行驱动，2026-2028 在乐观情景 CAGR 可 80%-110%。

2. **数字孪生和虚拟调试。** 基数小、项目大、标准化刚开始，乐观情景 2 年收入池可到 $18B-$35B，极度乐观可到 $35B-$60B。

3. **柔性负载和微电网能控。** 一旦并网审批把可控性作为条件，软件和控制平台会从“节能工具”变成“容量解锁工具”。

4. **高端智能 PDU/母线/传感器。** 相比传统数据中心，AI 高密机柜的每 rack telemetry value 更高，且短期硬件缺货可能带来价格弹性。

### 10.3 主要风险

| 风险 | 触发 | 影响 |
|---|---|---|
| AI capex 放缓 | 推理收入不及预期、GPU 利用率下滑 | 数字孪生和能控软件延后，项目服务订单推迟 |
| 电力/并网延期 | 变压器、开关柜、审批、燃气接入受阻 | 短期设备订单仍强，但收入确认推迟 |
| Hyperscaler 自研替代 | 大客户把 DCIM/能控完全内化 | 外部软件 TAM 缩小，硬件绑定和工程验证仍受益 |
| 安全事故 | AI agent 控制失误、液冷泄漏、误触发降载 | 自主控制推广放慢，客户转向 advisory-only |
| 标准碎片化 | NVIDIA DSX、OCP、各大云自研接口分裂 | 生态锁定加剧，中立软件商集成成本上升 |

## 参考来源

1. NVIDIA: [Vera Rubin DSX AI Factory reference design and Omniverse DSX Blueprint](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-Vera-Rubin-DSX-AI-Factory-Reference-Design-and-Omniverse-DSX-Digital-Twin-Blueprint-With-Broad-Industry-Support/default.aspx)
2. Schneider Electric: [Teams with NVIDIA to develop validated blueprints for gigawatt-scale AI factories](https://www.se.com/us/en/about-us/newsroom/news/press-releases/schneider-electric-teams-with-nvidia-to-develop-validated-blueprints-to-design-simulate-build-operate-and-maintain-gigawattscale-ai-factories-69b82f61aa1027e04205d273/)
3. AVEVA: [Lifecycle digital twin architecture for gigawatt-scale AI Factories](https://www.aveva.com/en/about/news/press-releases/2026/aveva-develops-a-new-lifecycle-digital-twin-architecture-that-delivers-industrial-intelligence-for-gigawatt-scale-ai-factories-accelerated-by-nvidia/)
4. Cadence: [Cadence and NVIDIA unveil accelerated engineering solutions](https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-and-nvidia-unveil-accelerated-engineering-solutions.html)
5. Jacobs: [Data Center Digital Twin solution for AI data centers](https://www.jacobs.com/newsroom/press-release/jacobs-releases-digital-twin-solution-ai-data-centers)
6. Phaidra: [AI-driven liquid cooling management with CoreWeave and Applied Digital](https://www.phaidra.ai/blog/breakthrough-AI-driven-liquid-cooling-management)
7. Phaidra: [Phaidra Factory product page](https://www.phaidra.ai/products/phaidra-factory)
8. Vertiv: [Q4 2025 results and 2026 guidance](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)
9. Vertiv: [Q1 2026 earnings release](https://s205.q4cdn.com/554782763/files/doc_financials/2026/q1/Vertiv-First-Quarter-2026-Earnings-Release.pdf)
10. Vertiv: [BYOP&C collaboration with Generate Capital](https://investors.vertiv.com/news/news-details/2026/Vertiv-and-Generate-Capital-Collaborate-to-Accelerate-Data-Center-Capacity-with-Complete-Power-and-Cooling-Infrastructure/default.aspx)
11. Vertiv: [ThermoKey acquisition](https://www.vertiv.com/en-us/about/news-and-events/corporate-news/2026/vertiv-to-acquire-thermokey-expanding-heat-rejection-portfolio-for-converged-physical-infrastructure/)
12. Vertiv: [360AI high density reference design #026](https://www.vertiv.com/48ea2a/globalassets/documents/brochures/vertiv-360ai-reference-design-026.pdf)
13. Schneider Electric: [Q1 2026 revenues](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026)
14. Schneider Electric: [Motivair liquid cooling portfolio](https://www.se.com/ww/en/about-us/newsroom/news/press-releases/Schneider-Electric-Unveils-Liquid-Cooling-Portfolio-with-Motivair-Featuring-Dedicated-Solutions-and-Services-for-HPC-and-AI-Workloads-68d69e595c9dbb622505caf3/)
15. Schneider Electric: [Motivair acquisition terms in 2025 half-year statements](https://www.webdisclosure.com/press-release/schneider-electric-epa-su-2025-half-year-financial-statements-rDLSNxk7FIb)
16. Schneider Electric: [BNEF NY 2026 power gap comments](https://www.prnewswire.com/news-releases/schneider-electric-advances-pathways-to-close-us-power-gap-at-bnef-ny-2026-302747913.html)
17. Eaton: [Q1 2026 results](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html)
18. Eaton: [Beam Rubin DSX platform with NVIDIA](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-collaborates-with-nvidia-to-unveil-its-beam-rubin-dsx-platform.html)
19. Eaton: [Brightlayer Energy](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-unveils-brightlayer-energy-an-ai-powered-energy-management.html)
20. Eaton: [Brightlayer Data Centers suite](https://www.eaton.com/us/en-us/digital/brightlayer/brightlayer-data-centers-suite.html)
21. Eaton: [Q1 2026 analyst presentation](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf)
22. Siemens: [Siemens and NVIDIA expand partnership](https://press.siemens.com/global/en/pressrelease/siemens-and-nvidia-expand-partnership-build-industrial-ai-operating-system)
23. Siemens: [Engineering the AI Factory with Siemens and NVIDIA](https://www.siemens.com/en-us/company/insights/us-stories/siemens-delivers-nvidia-dsx-infrastructure-ai-factory/)
24. Siemens Energy: [Q1 FY2026 earnings release](https://www.siemens-energy.com/global/en/home/press-releases/earnings-release-q1-fy-2026.html)
25. ABB: [Q1 2026 interim report](https://library.e.abb.com/public/dd7e26e13f7a4a4783979a725ef8ff7e/ABB-Q1-2026-press-release-English.pdf)
26. ABB: [ABB and VoltaGrid extend collaboration on data center power infrastructure](https://resources.news.e.abb.com/attachments/published/134418/en-US/3C94CF49905F/26032026_ABB_and_VoltaGrid_extend_collaboration_on_data_center_power_infrastructure_EN_update.pdf)
27. ABB: [ABB to develop next-generation AI data centers with NVIDIA](https://resources.news.e.abb.com/attachments/published/129805/en-US/D1659BBF0D16/20251013_ABB_to_develop_next-generation_AI_data_centers_with_NVIDIA_EN.pdf)
28. nVent: [Q1 2026 results](https://s22.q4cdn.com/268397047/files/doc_financials/2026/q1/Q1-2026-NVT-Press-Release.pdf)
29. nVent: [2026 Investor Day](https://investors.nvent.com/press-releases/press-release-details/2026/nVent-Highlights-Portfolio-Transformation-and-Growth-Priorities-at-2026-Investor-Day/default.aspx)
30. Delta Electronics: [Integrated power, cooling, and infrastructure architecture for AI data centers](https://www.prnewswire.com/news-releases/delta-unveils-integrated-power-cooling-and-infrastructure-architecture-for-ai-data-centers-at-data-center-world-2026-302746844.html)
31. Gartner Peer Insights: [Data Center Infrastructure Management tools definition and vendor list](https://www.gartner.com/reviews/market/data-center-infrastructure-management-tools)
32. Precedence Research: [DCIM market size 2026-2035](https://www.precedenceresearch.com/data-center-infrastructure-management-market)
33. Legrand: [NorthC case and data center solution brands](https://www.legrand.com/datacenter/sites/g/files/ocwmcr1671/files/2025-11/Legrand_NorthC%20-%20Press%20Release%20-%20November%202025%20-%20EN.pdf)

非投资建议。本报告使用公开一手资料、行业报告、项目内已有测算和乐观情景假设进行产业研究；未披露订单金额、内部系统渗透率和私有化软件收入处均为本报告估算。
# 行业调研：【导管、桥架与线缆管理】

截至日期：2026-05-08  
口径说明：本文研究的是 AI 数据中心/AI Factory 建设中用于电力线缆、光纤、铜缆、低压控制线、传感器线缆和机柜内外跳线的物理路径产品，包括导管、桥架、线槽、光纤走线槽、支吊架、线缆固定/保护、接地 bonding、线缆标识和预制化线缆管理组件。不含光模块、服务器、交换机、UPS、母线槽、成品线缆本体和纯安装人工；若采用“安装完成口径”，市场规模通常是本文材料/设备口径的 1.8-2.6 倍。

本文对 AI 数据中心建设保持大胆乐观假设：本地项目已有模型显示，2026 年美国 AI 数据中心可交付新增 IT 负载基准 6-8GW、乐观 8.5-11GW；2027 年基准 8-11GW、乐观 12-16GW。导管、桥架与线缆管理不是最贵环节，却是把 GPU、交换机、电力和冷却真正变成可运维容量的“低成本高约束”环节。

## 1. 核心结论

1. **2026 最确定的放量路径是“开放式桥架 + 高密度光纤走线 + 电力/数据分层隔离 + 预制化安装”。** AI 机柜的网络侧从 400G/800G 走向 800G/1.6T，Panduit 指出 AI 服务器的光纤数量通常是传统服务器的 4-6 倍，Panduit/NVIDIA 架构指南进一步把 AI 数据中心的光纤密度描述为传统数据中心的 4-8 倍。线缆数量、弯曲半径、托盘承载、空气流动、可维护性都变成设计变量，而不是施工细节。

2. **导管/桥架/线缆管理的 AI 数据中心相关市场，未来 12 个月全球设备/材料订单口径约 $8.2B-$12.8B，乐观 $12.0B-$18.5B，极度超预期 $17.0B-$27.0B。** 若用安装完成口径，对应约 $15B-$33B、$22B-$48B、$31B-$70B。未来 24 个月累计，设备/材料口径基准约 $19B-$31B，乐观 $31B-$49B，极度超预期 $48B-$78B。

3. **每 1GW AI IT 负载对应导管、桥架、线缆管理材料价值量约 $0.65B-$1.15B，极度乐观可到 $1.4B/GW。** 其中白空间光纤走线、wire mesh tray、机柜内外 slack/radius 管理的弹性最大；灰空间/电力侧的 conduit、ladder tray、cable cleats 更受电力密度、短路电流和 800VDC/高压直流路径影响。

4. **短期最有定价权的不是最普通的 EMT/PVC 导管，而是“工程化系统”。** 包括 UL/NEMA/IEC 合规的宽幅 wire mesh tray、可作为设备接地导体的桥架系统、免切割/预成型弯头和 drop-out、光纤专用 raceway、高密度 MPO/APC slack management、短路认证 cable cleats、预制化支吊架和 BIM/submittal 服务。

5. **公司验证已经出现在 2026 一季报和二季报里。** nVent Q1 2026 销售 $1.242B、同比 +53%、有机 +34%，CEO 明确称数据中心在 gray space 和 white space 都在驱动增长，backlog 升至 $2.6B。Eaton Q1 2026 Electrical Americas 数据中心订单同比约 +240%、收入约 +50%，并与 NVIDIA 推出 Eaton Beam Rubin DSX 平台。Legrand Q1 2026 美国销售有机 +29.1%，归因于数据中心相关产品成功，并在年初完成/宣布 4 个数据中心与能源转型并购。Atkore Q2 2026 披露金属构架、线缆管理和施工服务占 FY2026 YTD 净销售 27%，并继续预期项目与数据中心相关需求爬坡。

## 2. 需求从哪里来：AI 计算中心的线缆路径变化

### 2.1 AI 机柜让“线缆管理”从辅材变成可用容量瓶颈

AI 集群的变化不是单纯“服务器更多”，而是：

| 变化 | 对导管/桥架/线缆管理的影响 |
|---|---|
| GB300/NVL72、Rubin、MI400、Trainium3、TPU Ironwood 等 rack-scale 系统密度提升 | 机柜后部线缆、液冷管路、PDU、维护空间相互抢占；需要更宽机柜、更清晰的垂直/水平管理和更强 strain relief |
| 800G/1.6T 光互联放量 | 光纤数量、MPO/APC 连接器、光纤 tray、弯曲半径保护、清洁和可更换性成为高频设计点 |
| DAC/ACC/AEC 在短距离仍存在，但外径更大、弯曲半径更大 | 短距铜缆不会消失，但会挤占路径空间，要求分层走线和更大的桥架填充余量 |
| 推理集群从单机柜变成多 pod、多 row、多 hall | 白空间 overhead tray、fiber raceway、ladder tray、dropout 和预制化支吊架数量随端口数放大 |
| 电力从 40kW/rack 进入 100kW+、甚至更高 | 大截面馈线、柔性导管、液密导管、电力桥架、cable cleats、接地 bonding 和短路约束需求上升 |
| 液冷普及 | 电缆必须避开冷却软管、阀组、快接头、漏液检测和维护路径，传统“能放下就行”的走线方式不够 |

Panduit 的 AI FAQ 明确提到，超过 40kW/rack 时要考虑 RDHX 或 direct-to-chip 液冷，同时需要额外关注网络线缆和路径；同一材料还指出 AI 服务器需要 4-6 倍光纤。NVIDIA DGX SuperPOD cabling guide 要求铜缆和光纤分开、线缆不要阻挡 airflow 或设备抽换、线缆每 2m 支撑或放入 tray，并把 fiber optic trays、basket/wire mesh、cable ladders 列为三类常见支撑系统。

### 2.2 2026-2027 最大出货 AI 芯片路径对本行业的映射

本项目已有 AI 芯片路线图显示，2026 年最大出货/价值主线是 NVIDIA B300/GB300 Blackwell Ultra、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、华为 Ascend 910C/950、Cambricon、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200、Alibaba Zhenwu、AMD MI400/Helios。对应到物理路径：

| 芯片/平台主线 | 2026-2027 线缆路径需求 | 最受益产品 |
|---|---|---|
| GB300/B300/NVL72 | rack 内 NVLink 铜互连为主，scale-out 800G/1.6T 光纤，液冷标配化 | 宽幅 wire mesh tray、光纤 raceway、MPO slack 管理、机柜后部垂直管理、液冷兼容桥架布局 |
| Rubin/MI400/Trainium3/TPU8 | 2026 H2 试量，2027 更高密度和 1.6T/高压供电 | 高承载 ladder tray、cable cleats、800VDC/HVDC 路径、预制化支吊架 |
| TPU/Trainium/MTIA/自研 ASIC | hyperscaler 自建标准化 pod，重复复制 | 供应商认证、BIM 模块、可复制 BOM、全球交付能力 |
| 中国国产 AI 集群 | 单芯片算力不足用超节点和更多互连弥补 | 光纤/铜缆路径、桥架、模块化线槽、国产供应链替代 |

### 2.3 2026 最可能的技术路径

2026 年最可能放量的不是某个颠覆性材料，而是成熟产品在 AI 场景下的高密度化：

1. **白空间：wire mesh/basket tray 成为默认主路径。** 原因是开放、散热好、现场可改、适合未来扩容。Legrand Cablofil 已推出 30 英寸和 36 英寸宽 wire mesh tray，并称 36 英寸面向 hyperscale data centers；Eaton Flextray 也覆盖 30/32/36 英寸宽度。

2. **光纤：专用 fiber raceway + 高密度 MPO/APC patch/slack 管理。** NVIDIA/Panduit 指南已覆盖 400G、800G、1600G transceiver 的 OSFP、MPO12 APC、Duplex LC、OM3/OM4/OS2 路径，2026 会以 800G 为主、1.6T 开始导入。

3. **电力：导管继续用于保护性分支和合规路径，ladder tray/cleats 用于高电流馈线。** EMT/RMC/IMC/PVC/RTRC/flexible conduit 不会被桥架替代，尤其在穿墙、保护、室外、地下、设备端接和消防/安全要求强的路径。

4. **施工：预成型弯头、免切割 drop-out、fast splice、trapeze kits、BIM submittal 将快速渗透。** AI 项目真正稀缺的是并行施工速度和返工率控制。

## 3. 市场规模与三情景预测

### 3.1 总行业锚点

公开第三方报告对总行业给出的基准：

| 口径 | 市场规模和增速 | 含义 |
|---|---:|---|
| 全球 cable management system | 2024 年 $23.5B，2025-2030 CAGR 8.2% | 数据中心只是其中一部分，传统建筑/工业占比仍大 |
| 全球 cable management market | 2026 年约 $27.89B，2035 年 $57.22B，CAGR 8.3% | 包含 cable trays、raceways、conduits、connectors/glands 等 |
| 全球 cable tray | 2025 年 $6.41B，2026 年 $7.34B，2034 年 $16.14B，CAGR 10.35% | 数据中心、可再生能源、工业共同驱动 |
| 全球 electrical conduit | 2025 年 $8.45B，2033 年 $15.14B，2026-2033 CAGR 7.6% | 北美 2025 占比 31.6%，金属和刚性产品占主导 |
| 全球 data center cable management | 2025 年 $6.2B，2035 年 $14.6B，CAGR 9.0% | 这一口径低估 2026-2027 AI Factory 爆发，因为多数报告尚未充分计入 GW 级 AI 项目提前下单 |

本文将 AI 数据中心相关增量建模为：  
`AI DC 全栈 CapEx × 0.8%-1.8% 材料/设备系数 × AI 高密度加成 × 订单提前系数`。  
在基准情景中，导管、桥架、线缆管理设备/材料约占全栈 AI DC CapEx 的 1.0%-1.4%；乐观 1.3%-1.8%；极度超预期 1.7%-2.2%。如果只看非 IT 机电/建筑部分，占比可达 3%-6%。

### 3.2 AI 数据中心相关市场规模：累计订单/出货口径

| 时间窗口 | 基准 | 乐观 | 极度超预期乐观 | 关键假设 |
|---|---:|---:|---:|---|
| 未来 3 个月 | $1.9B-$3.1B | $3.0B-$4.8B | $4.6B-$7.2B | 2026 H2 GB300/NVL72、800G、液冷项目锁 BOM；电力设备长交期带动灰空间先下单 |
| 未来 12 个月 | $8.2B-$12.8B | $12.0B-$18.5B | $17.0B-$27.0B | 2026 美国 6-8GW 基准落地，全球叠加欧洲/中东/亚洲；AI 线缆密度 4-8x 开始兑现 |
| 未来 24 个月 | $19B-$31B | $31B-$49B | $48B-$78B | 2027 Rubin/Trainium3/TPU/ASIC 与多园区 AI Factory 复制；1.6T 和高密度电力路径放量 |

### 3.3 已经开始放量的关键产品

| 产品/技术 | 当前阶段 | 未来 3 个月市场 | 未来 12 个月市场 | 未来 24 个月市场 | 渗透率路径 | 毛利/EBITDA 率判断 |
|---|---|---:|---:|---:|---|---|
| Wire mesh/basket tray、宽幅 30/36 英寸、配套弯头/drop-out | 已放量 | 基准 $350M-$550M；乐观 $550M-$850M；极度 $850M-$1.3B | 基准 $1.6B-$2.5B；乐观 $2.4B-$3.7B；极度 $3.6B-$5.5B | 基准 $3.8B-$6.2B；乐观 $6.0B-$9.5B；极度 $9.2B-$14.5B | AI 白空间新建项目 2026 60%-75%，2027 70%-85%，2028 75%-90% | 毛利 30%-45%；EBITDA 15%-25%，短交期/宽幅/认证产品可更高 |
| Ladder tray、heavy-duty power tray、cable ladder | 已放量 | $260M-$430M / $420M-$700M / $650M-$1.0B | $1.2B-$2.0B / $1.8B-$3.0B / $2.8B-$4.6B | $2.9B-$4.8B / $4.8B-$7.6B / $7.5B-$12B | 电力主路径渗透率本来高，AI 高密度使价值量提升 20%-60% | 毛利 25%-40%；项目型产品 EBITDA 12%-22% |
| EMT/RMC/IMC 金属导管及 fittings | 已放量但偏周期 | $300M-$520M / $450M-$760M / $700M-$1.1B | $1.4B-$2.4B / $2.0B-$3.5B / $3.0B-$5.0B | $3.2B-$5.5B / $5.0B-$8.5B / $8.0B-$13B | 保护路径、穿墙、设备端接、室外/安全路径接近刚需；单位价值随电力密度上升 | 毛利 18%-32%；EBITDA 8%-18%，受钢价、进口、价格竞争影响大 |
| PVC/RTRC/HDPE/fiberglass conduit | 已放量，室外/地下/腐蚀环境强 | $180M-$330M / $300M-$520M / $480M-$800M | $0.9B-$1.6B / $1.4B-$2.5B / $2.2B-$3.8B | $2.0B-$3.5B / $3.5B-$5.8B / $5.5B-$9B | 园区化、地下管廊、变电站和长距离馈线拉动 | 毛利 18%-35%；高端 fiberglass/RTRC 毛利高于普通 PVC |
| Fiber raceway、MPO/APC 高密度 patch/slack 管理 | 快速放量 | $280M-$480M / $450M-$780M / $700M-$1.2B | $1.4B-$2.3B / $2.2B-$3.7B / $3.5B-$5.8B | $3.6B-$5.8B / $6.0B-$9.2B / $9.5B-$15B | 2026 AI rows 50%-65%，2027 65%-80%，2028 80%+；1.6T 后进一步上移 | 毛利 35%-55%；EBITDA 18%-32%，设计锁定强 |
| Rack/row vertical/horizontal cable managers、bend radius guides、labels | 已放量 | $180M-$300M / $280M-$460M / $450M-$700M | $0.8B-$1.3B / $1.2B-$2.0B / $1.9B-$3.2B | $2.0B-$3.3B / $3.4B-$5.2B / $5.0B-$8.0B | 高密 AI 机柜和液冷使后门/侧面空间管理成为必需 | 毛利 30%-50%；高密度专用件溢价明显 |
| Strut、trapeze、J-hooks、supports、seismic bracing | 已放量 | $230M-$390M / $360M-$620M / $560M-$900M | $1.1B-$1.8B / $1.7B-$2.9B / $2.7B-$4.5B | $2.6B-$4.4B / $4.4B-$7.0B / $7.0B-$11B | 多层 overhead tray、液冷管路、电力路径共架，支吊架价值量上升 | 毛利 25%-45%；认证/抗震/预装件更高 |
| Cable cleats、grounding/bonding、短路保护固定件 | 已放量，AI 电力侧加速 | $90M-$170M / $150M-$280M / $250M-$450M | $0.45B-$0.8B / $0.75B-$1.4B / $1.2B-$2.3B | $1.2B-$2.0B / $2.1B-$3.5B / $3.6B-$6.0B | 高电流馈线渗透率 2026 35%-50%，2027 50%-70%，2028 65%-85% | 毛利 35%-55%；短路测试和客户认证带来高定价 |
| 预制化桥架/导管模块、BIM kits、项目服务 | 初步放量 | $150M-$280M / $260M-$480M / $430M-$750M | $0.8B-$1.4B / $1.4B-$2.5B / $2.4B-$4.2B | $2.2B-$3.8B / $4.0B-$6.8B / $7.0B-$11.5B | 2026 15%-25% 项目采用，2027 30%-45%，2028 45%-65% | 毛利 25%-45%；资本轻、ROIC 高，但依赖项目管理能力 |

### 3.4 在研/导入期关键产品和细分技术

| 在研/导入技术 | 成熟时间 | 放量时间：基准/乐观/极度超预期 | 未来 12 个月市场 | 未来 24 个月市场 | 利润率潜力 |
|---|---|---|---:|---:|---|
| 800VDC/HVDC 数据中心线缆路径、绝缘隔离、arc mitigation、DC-rated cleats | 2026 试点，2027 工程化，2028 标准化 | 基准 2028；乐观 2027 H2；极度 2027 H1 | $50M-$180M / $150M-$450M / $400M-$1.0B | $0.4B-$1.2B / $1.0B-$2.5B / $2.2B-$5.0B | 毛利 40%-60%，认证壁垒高 |
| 液冷机柜专用 cable + hose 共存管理、漏液/电气隔离路径 | 2026 成熟 | 基准 2027；乐观 2026 H2；极度 2026 Q3 | $200M-$550M / $500M-$1.2B / $1.0B-$2.0B | $1.0B-$2.5B / $2.2B-$4.8B / $4.5B-$8.5B | 毛利 35%-55%，系统集成商可拿高溢价 |
| 1.6T/3.2T fiber raceway、MPO16/SN-MT/MMC 高密度管理 | 2026 H2-2027 | 基准 2027；乐观 2026 H2；极度 2026 Q4 | $250M-$700M / $650M-$1.6B / $1.4B-$3.0B | $1.5B-$3.5B / $3.0B-$6.5B / $6.0B-$12B | 毛利 40%-60%，生态绑定强 |
| 智能化线缆标识、RFID/QR、digital twin、自动生成 BOM/submittal | 2026 可用 | 基准 2027；乐观 2026；极度 2026 大客户强制 | $100M-$300M / $250M-$650M / $600M-$1.2B | $0.7B-$1.6B / $1.5B-$3.2B / $3.0B-$6.0B | 软件/服务毛利高，但硬件渗透依赖业主标准 |
| 抗篡改/高安全 cable tray、secure covers、物理安全路径 | 2026 小量 | 基准 2027；乐观 2026 H2；极度主权 AI 推动 | $60M-$180M / $160M-$420M / $350M-$850M | $0.4B-$1.0B / $0.9B-$2.0B / $1.8B-$4.0B | 毛利 35%-55%，主权 AI 和金融/政府客户溢价 |
| 机器人/半自动化布线与线缆审计 | 2027-2028 | 基准 2028 后；乐观 2027 H2；极度 2027 | $20M-$80M / $60M-$200M / $150M-$500M | $0.2B-$0.6B / $0.6B-$1.5B / $1.5B-$3.0B | 高毛利但技术/流程成熟度不足 |

## 4. 供给侧：产能、瓶颈、成本和价格传导

### 4.1 产能结构

| 产品 | 主要产能地区 | 典型公司/品牌 | 关键工艺 |
|---|---|---|---|
| 金属导管 EMT/RMC/IMC | 美国、墨西哥、加拿大、中国、印度、土耳其、欧洲 | Atkore Allied Tube & Conduit、Zekelman/Wheatland、Nucor Tubular、Robroy、ABB/Thomas & Betts、Anamet、Electri-Flex | 钢带分切、成型、焊接、镀锌、螺纹、弯管、涂层 |
| PVC/HDPE/RTRC/fiberglass conduit | 美国、加拿大、墨西哥、中国、印度、中东 | Atkore Heritage/FRE、CANTEX、JM Eagle、IPEX、Dura-Line/Orbia、Champion Fiberglass、Prime Conduit | PVC/HDPE 挤出、玻纤拉挤、树脂配方、连接件注塑 |
| Wire mesh/basket tray | 美国、欧洲、中国、印度、东南亚 | Legrand Cablofil、Eaton B-Line Flextray、nVent CADDY、Panduit、Snake Tray、OBO、Niedax、Basor、MP Husky | 钢丝成型、点焊、切割、镀锌/喷粉/不锈钢、配件冲压 |
| Ladder tray/heavy tray/cable ladder | 美国、欧洲、中东、中国、印度 | Eaton B-Line、Legrand、Niedax、OBO、MP Husky、Basor、Oglaend/Hilti、Schneider、ABB | 铝挤压/钢板冲压、焊接、热浸镀锌、喷涂、现场拼接 |
| Fiber raceway/塑料线槽 | 美国、欧洲、中国、墨西哥、东南亚 | Panduit FiberRunner、Legrand Ortronics、CommScope、Corning、Belden、Siemon、Leviton | 阻燃塑料挤出/注塑、弯头/三通模具、颜色/阻燃认证 |
| 支吊架、strut、cleats、bonding | 美国、欧洲、中国、印度、英国 | nVent CADDY/ERICO、Atkore Unistrut、Eaton B-Line/TOLCO、Hilti/Oglaend、Panduit、Hubbell/Burndy、Ellis Patents、CMP | 轧制成型、冲压、铸造、聚合物/铝夹具、短路测试、UL/IEC 认证 |

### 4.2 供给瓶颈

1. **钢、铝、铜、PVC/HDPE 树脂和玻纤价格波动。** Atkore Q2 2026 明确披露 input costs 增长远高于售价增长，电气业务 EBITDA margin 同比从 18.5% 降至 14.0%。

2. **热浸镀锌、喷粉、特殊涂层和不锈钢产能。** 数据中心要求交付快、外观一致、耐腐蚀、低毛刺；宽幅 tray 与特殊颜色/finish 会占用后处理产能。

3. **UL/NEMA/CSA/IEC/NEC 合规和客户认证。** Cable Tray Institute 指出 NEMA VE 1、VE 2、IEC 61537、NEC Article 392 是核心标准；产品是否 UL Classified as equipment grounding conductor、是否符合 load/span class，会直接影响能否进入 hyperscaler AVL。

4. **工程 submittal、BIM、load/fill 计算和结构复核。** NVIDIA 指南要求考虑 building overhead support、trapeze capacities、tray construction、stacked trays、fiber tray、busway、cable type 和 cable runs，且安装前需结构工程师复核。材料供应不是唯一瓶颈，工程图纸和批准周期也会限制订单转收入。

5. **施工人力和数据中心经验。** 线缆路径安装必须与母线槽、液冷、消防、照明、传感器、安防、网络交叉施工；熟练电工/低压施工团队不足会把高价值产品变成现场拥堵。

6. **大件物流和现场库存。** 10 英尺直段、30/36 英寸宽 tray、长导管、预制化模块体积大，运输半径和分销库存决定交期。Wesco/Anixter、Sonepar、Rexel、Graybar 等渠道价值上升。

7. **进口、关税和原产地。** Atkore 在 Q1/Q2 材料中提到 imports/tariffs 仍是市场动态变量；nVent 也在 Q1 2026 面临关税和通胀压力。美国 AI 园区会更偏好本地/北美供应，利好本土产能但加剧短期交期。

8. **短路认证和高电流 restraint。** cable cleats 需要短路测试和安装间距/载荷设计，不是普通夹具可替代。800VDC/HVDC 后认证周期会更长。

### 4.3 成本构成和毛利决定因素

| 产品 | BOM/单位成本拆分 | 毛利决定因素 | 价格传导 |
|---|---|---|---|
| 金属导管 | 钢材/锌 45%-60%，人工/能耗 10%-18%，折旧 3%-8%，包装物流 8%-15%，SG&A/渠道 10%-18% | 钢价、进口价格、利用率、地区库存、项目规格 | 钢价上涨通常 1-2 个季度传导，长期项目需 escalation clause |
| PVC/HDPE/RTRC 导管 | 树脂/玻纤 45%-65%，挤出/拉挤能耗 8%-15%，人工 8%-15%，物流 10%-20% | 树脂价、阻燃/耐腐蚀认证、地下/室外项目 | 大宗树脂驱动强，普通产品定价权弱，高端 RTRC/fiberglass 强 |
| Wire mesh/ladder tray | 钢/铝/不锈钢 35%-55%，焊接/成型 10%-18%，涂层 5%-12%，配件/紧固件 5%-12%，物流 10%-18% | 宽幅、finish、UL EGC、配件体系、交期 | 数据中心短交期订单可加价，标准品价格随钢铝波动 |
| Fiber raceway/机柜线缆管理 | 工程塑料/金属件 25%-45%，模具/折旧 5%-12%，组装/包装 10%-20%，工程支持 10%-20% | 生态锁定、专利/模具、MPO/APC 密度、可维护性 | 以系统 BOM 定价，客户更看总安装成本和停机风险 |
| Cleats/grounding/bonding | 金属/聚合物 30%-50%，测试认证 5%-15%，加工 10%-20%，渠道 10%-20% | 短路等级、UL/IEC、安装间距、工程责任 | 高认证产品可维持溢价，替换成本高 |
| 预制化/BIM kits | 标准件 40%-60%，工程设计 10%-25%，工厂预装 10%-20%，物流 10%-20% | 节省现场人工、减少返工、压缩工期 | 按项目价值定价，不只按材料成本加成 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

这个行业整体分散，但数据中心高端项目集中度更高。总 cable management 市场 CR5 估计 25%-35%，但 hyperscale 数据中心合格供应商池中，Legrand、Eaton、nVent、Panduit、Atkore、Schneider/Vertiv、CommScope/Corning/Belden/Siemon、Hubbell/ABB 等头部供应商占比可达 50%-65%。原因不是普通制造难，而是客户认证、工程响应、渠道库存、标准兼容和全球交付能力。

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| 认证标准 | NEC 392、NEMA VE1/VE2、IEC 61537、UL 568/2239、UL EGC、短路测试、阻燃等级等决定产品能否被设计院和 AHJ 接受，低价未认证产品进不了关键项目 |
| 客户 AVL 和历史项目记录 | hyperscaler 一旦验证某套 tray/fiber pathway/cleat 系统，换供应商会引入设计、审批、维护和事故责任风险 |
| 工程服务和 BIM/submittal | AI 数据中心的多层路径、液冷、busway、电力馈线、光纤密度需要前期图纸协同，供应商从“卖米数”升级成“交付可安装系统” |
| 渠道库存和交期 | 数据中心工期按周计算，能在 Graybar/Wesco/Sonepar/Rexel 等渠道快速补货的供应商可拿更高价格 |
| 产品生态 | tray、splice、dropout、support、grounding、label、rack manager 如果同一体系兼容，施工效率高，返工低 |
| 安全责任 | 线缆阻塞 airflow、拉伤 transceiver、短路电缆甩动、接地不连续都可能造成停机或安全事故；客户愿意为低风险付溢价 |
| 预制化能力 | 能把现场切割、打磨、弯折、拼接转移到工厂，节省高工资电工时间，价格锚不再是材料成本，而是工期价值 |

### 5.3 价值捕获判断

长期高 ROIC/高毛利层级从强到弱：

1. **高密度 fiber raceway、MPO/APC slack/bend 管理、机柜线缆管理。** 与 AI 网络架构绑定，替换成本高，设计锁定强。

2. **cable cleats、grounding/bonding、短路/高压认证固定件。** 认证和安全责任壁垒高，ASP 小但毛利高。

3. **预制化桥架/支吊架/BIM kits。** 工程能力和交付速度带来资本轻 ROIC。

4. **宽幅 wire mesh/ladder tray + 配件体系。** 比普通导管更工程化，能吃到数据中心密度溢价。

5. **普通 EMT/PVC conduit。** 量大但更像大宗建材，价格受钢/PVC/进口竞争压制。Atkore/同类企业在 AI 周期中会受益于量，但利润率更不稳定。

## 6. 2026 关键变化和最可能放量子方向

1. **GB300/NVL72 整柜交付爬坡把 white space cable pathway 拉成显性订单。** nVent、Eaton、Legrand、Schneider 的 2026 Q1 信息已经显示数据中心在 gray 和 white space 同时拉动。最受益：wire mesh tray、fiber raceway、rack managers、liquid-cooling-compatible cable/hose management。

2. **800G 主流化、1.6T 导入，光纤路径密度进入新台阶。** Panduit/NVIDIA 架构中 1600G transceiver、MPO12 APC、OS2/OM4、HD Flex/QuickNet 等已在参考架构中出现。最受益：Panduit、Legrand Ortronics/Cablofil、CommScope、Corning、Belden、Siemon、Leviton。

3. **工期压力推动预制化和工程服务溢价。** Legrand Cablofil 强调数据中心一个项目可能有上千个 bends/drops；Eaton B-Line、nVent CADDY、Legrand Cablobend、Panduit BOM 服务都在卖“少切割、少返工、快安装”。最受益：nVent、Eaton、Legrand、Atkore Unistrut、Hilti/Oglaend、Wesco/Anixter 等。

## 7. 2027 关键变化和最可能放量子方向

1. **Rubin/MI400/TPU8/Trainium3 放量后，1.6T、HBM4、高密度液冷机柜成为主流项目规格。** 线缆路径将从 800G 过渡到 1.6T 常态，光纤 raceway 和高密度 patch/slack 管理二次放量。

2. **800VDC/HVDC 和 grid-to-chip 架构从试点走向工程化。** ABB 已在 2026 Q1 数据中心通讯中讨论 800VDC 与 NVIDIA 相关架构，Eaton 也在 Q1 2026 展示 Eaton Beam Rubin DSX。2027 最可能放量的是 DC-rated cleats、隔离路径、接地/bonding、arc mitigation、专用 conduit/tray。

3. **多园区 AI Factory 复制带来标准化 BOM。** 一旦 OpenAI/Oracle/Stargate、Meta、AWS、Google、xAI/CoreWeave 等 GW 级项目进入复制阶段，采购会从单项目招标转向标准 kit 和跨地区框架协议。具备全球产能、渠道和工程服务的公司份额提升。

## 8. 公司一手信息和投资信号

| 公司 | 2026 最新信号 | 对本行业含义 |
|---|---|---|
| nVent | Q1 2026 销售 $1.242B，同比 +53%，有机 +34%；backlog $2.6B；Systems Protection +76%，Electrical Connections +15%；管理层称数据中心在 gray/white space 广泛增长 | nVent CADDY、ERICO、SCHROFF、ILSCO 等连接/固定/机柜/电气保护组合直接受益；高订单和 backlog 说明 AI DC 需求已经从规划进入采购 |
| Eaton | Q1 2026 Electrical Americas 数据中心订单约 +240%、收入约 +50%；Electrical Americas backlog +44%，Electrical Global backlog +73%；关闭 Boyd Thermal 并展示 Eaton Beam Rubin DSX | Eaton 不只是电力设备，也有 B-Line/Flextray/support systems；grid-to-chip 和液冷会带动 cable pathway 与支撑系统一起销售 |
| Legrand | Q1 2026 销售 €2.538B， organic +9.3%，美国 +29.1%，由数据中心相关产品驱动；年初 4 个并购合计年收入约 €275M，包括 Keydak、TES、Kratos、Green4T | Cablofil、Ortronics、rack、busway/power distribution、数据中心服务并购组合增强；在白空间/灰空间同时扩张 |
| Atkore | Q2 2026 net sales $731M，organic volume 约 +5%；FY2026 YTD 金属构架/线缆管理/施工服务占 27%，PVC/塑料导管 22%，金属电气导管 22%，电缆/柔性导管 17%；继续预期项目和数据中心需求爬坡 | Atkore 是导管、Unistrut、FRE/Heritage、Allied Tube 等核心供应商，但利润率受钢/PVC/进口/诉讼影响，AI 量弹性强、毛利弹性较弱 |
| Schneider Electric | Q1 2026 Data Center & Networks demand double digit；AI-ready infrastructure 带动端到端组合；北美增长由数据中心和液冷强劲驱动 | Schneider 更偏电力/冷却/软件，但 EcoStruxure、APC、rack/PDU/服务会带动线缆管理和生命周期服务 |
| ABB | Q1 2026 Electrification orders $6.647B，同比 +51%，data centers triple digit；backlog $11.46B；并推广 800VDC 和数字化 switchgear | 电力侧路径、cleats、接地、导管/支撑、HVDC 方案会受益；ABB 还通过 Thomas & Betts 等品牌覆盖线缆保护 |
| Panduit | AI 数据中心页面强调 fiber、power、cooling 和 pathways；AI FAQ 称 AI 服务器需要 4-6 倍光纤；Data Centre World 2026 展示 DTC cooling cabinet、cable cleats、grounding/bonding、Gen 7 SAN Director connectivity | Panduit 是高密度光纤路径、接地、cleats、机柜和标识的高毛利代表 |
| NVIDIA/Panduit 参考架构 | 明确 structured cabling 在 AI 中用于标准化、保护、uptime、未来升级，且 AI 光纤密度 4-8x | 证明 hyperscaler 不会把线缆管理当作低端辅材，而会纳入参考架构和标准 BOM |

## 9. 头部公司和细分领域清单

### 9.1 导管、管件和线缆保护

| 细分 | 代表公司 |
|---|---|
| EMT/RMC/IMC 金属导管 | Atkore Allied Tube & Conduit、Zekelman/Wheatland Tube、Western Tube、Nucor Tubular、Robroy Industries、ABB/Thomas & Betts、Calbond、Republic Conduit、Picoma、Allied Fittings |
| PVC/HDPE conduit | Atkore Heritage Plastics、CANTEX、JM Eagle、IPEX、Dura-Line/Orbia、Prime Conduit、Carlon/ABB、Cantex、National Pipe & Plastics |
| fiberglass/RTRC conduit | Atkore FRE Composites、Champion Fiberglass、United Fiberglass、Aeron、Enduro Composites |
| flexible/liquidtight conduit | Electri-Flex、Atkore AFC Cable Systems、Southwire、ABB/Thomas & Betts、Anamet、Hubbell/Killark、HellermannTyton |
| cable glands/connectors | CMP Products、Hubbell/Killark、nVent HOFFMAN/ERICO、TE Connectivity、ABB、Eaton Crouse-Hinds、Prysmian/BICON、LAPP |

### 9.2 桥架、线槽和 pathway

| 细分 | 代表公司 |
|---|---|
| wire mesh/basket tray | Legrand Cablofil、Eaton B-Line Flextray、nVent CADDY、Panduit、Snake Tray、OBO Bettermann、Niedax Group、Basor Electric、MP Husky、Chatsworth Products、Leviton、FS.com |
| ladder/heavy-duty tray | Eaton B-Line、Legrand、Niedax、OBO Bettermann、MP Husky、Basor、Oglaend System/Hilti、Vantrunk、Schneider Electric、ABB、EAE、Larsen & Toubro、Unistrut/Atkore |
| fiber raceway | Panduit FiberRunner、Legrand Ortronics、CommScope SYSTIMAX、Corning、Belden、Siemon、Leviton、Eaton Tripp Lite、Chatsworth Products |
| rack/row cable management | Panduit、Legrand Raritan/Ortronics、Chatsworth Products、Vertiv、Schneider/APC、Eaton/Tripp Lite、nVent SCHROFF、CommScope、Belden、Siemon、Rittal、AMCO Enclosures |
| supports/strut/seismic | nVent CADDY/ERICO、Atkore Unistrut、Eaton B-Line/TOLCO、Hilti/Oglaend、Gripple、Walraven、Sikla、Anvil/ASC、Mason Industries |

### 9.3 安全、接地和预制化

| 细分 | 代表公司 |
|---|---|
| cable cleats | Panduit、nVent ERICO、Ellis Patents、CMP Products、Prysmian/BICON、Eaton、Hubbell/Burndy、ABB/Thomas & Betts、TE Connectivity |
| grounding/bonding | nVent ERICO、Panduit、Hubbell Burndy、ABB/Thomas & Betts、Eaton、TE Connectivity、3M、HellermannTyton |
| 预制化和工程服务 | Legrand Cablofil/Cablobend、Eaton B-Line CoSPEC、nVent CADDY、Panduit TSE/BOM、Atkore Construction Services/Unistrut、Hilti/Oglaend、Wesco/Anixter、Graybar、Rexel、Sonepar |
| 数据中心机柜/机电一体化 | Legrand, Schneider/APC, Vertiv, Eaton, nVent SCHROFF, Chatsworth Products, Panduit, Rittal, Keydak, TES, E+I Engineering |

## 10. 投资价值排序

| 排名 | 子方向 | 投资逻辑 | 风险 |
|---:|---|---|---|
| 1 | 高密度 fiber raceway、MPO/APC、rack cable management | 直接受 800G/1.6T 和 4-8x 光纤密度驱动，设计锁定强，毛利高 | 若 CPO/OCS 架构减少部分可插拔光纤路径，远期弹性可能变化 |
| 2 | wire mesh/wide tray + fast install accessories | 2026 最确定放量，施工节省价值高，客户认证强 | 钢价、进口和本地竞争压制普通品毛利 |
| 3 | cable cleats、grounding/bonding、HVDC safety | 100kW+ rack、800VDC、高短路电流带来安全认证溢价 | 标准成熟速度和客户采用节奏不确定 |
| 4 | 预制化支吊架/BIM/submittal | 工期瓶颈下最容易从辅材转成服务价值，ROIC 高 | 需要项目管理能力，规模化不如标准制造容易 |
| 5 | conduit/fittings 大宗产品 | 量弹性大，AI 园区和电力扩张都会拉动 | 更周期、更大宗，毛利受原材料和进口竞争影响 |

## 11. 主要风险

1. AI 数据中心项目延期或取消，尤其是电力接入、变压器、开关柜、并网和融资导致的节奏变化。  
2. GPU/HBM/CoWoS 供应不及预期，使 white space 线缆路径订单后移。  
3. 线缆管理产品本身低技术门槛，普通规格容易价格竞争。  
4. 钢、铝、铜、PVC、HDPE 和关税造成毛利波动，价格传导滞后。  
5. 800VDC/HVDC、CPO、OCS、液冷架构如果路线突变，会改变具体产品组合。  
6. 客户为了降低 CapEx，可能压缩冗余路径和预留扩容空间，但在极高密 AI 场景下这会增加运维风险。

## 12. 资料来源

公司一手信息与技术资料：

- nVent Q1 2026 press release: [nVent Delivers Record Sales, Orders and Backlog in Q1 2026](https://www.sec.gov/Archives/edgar/data/1720635/000162828026029098/q12026nvtpressrelease.htm)
- Eaton Q1 2026 analyst presentation: [Eaton 1Q 2026 analyst presentation](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf)
- Eaton Q1 2026 press release: [Eaton Reports Record First Quarter 2026 Results](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html)
- Atkore Q2 2026 press release: [Atkore Inc. Announces Second Quarter 2026 Results](https://www.sec.gov/Archives/edgar/data/1666138/000162828026030054/atkr2q26exhibit991.htm)
- Atkore Q2 2026 earnings presentation: [Q2 2026 Earnings Deck](https://s202.q4cdn.com/690266772/files/doc_financials/2026/q2/Q2-2026-Earnings-Deck-vFinal.pdf)
- Legrand Q1 2026 press release: [Legrand 2026 first-quarter results](https://www.legrand.com/sites/default/files/Documents_PDF_Legrand/Finance/2026/3m/Legrand_Press_Release_Results_3M2026_1778074218.pdf)
- Schneider Electric Q1 2026 revenues: [Schneider Electric Q1 2026 Revenues](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026)
- ABB Q1 2026 press release: [ABB Q1 2026 press release](https://library.e.abb.com/public/dd7e26e13f7a4a4783979a725ef8ff7e/ABB-Q1-2026-press-release-English.pdf)
- ABB data center Q1 2026 notes: [ABB Electrification Data Center News Q1 2026](https://powertalk.electrification.us.abb.com/ELUS26-Data-Center-Q1.html)
- Panduit AI data center solutions: [Panduit Artificial Intelligence Data Center Solutions](https://www.panduit.com/chn/en/solutions/applications/ai-data-center-solutions.html)
- Panduit AI FAQ ebook: [13 Most Frequently Asked Questions About AI Data Center Environments](https://www.panduit.com/content/dam/panduit/en/website/solutions/applications/ai-data-center-solutions/documents/ai-faq-ebook-cpeb16-ww-eng.pdf)
- Panduit/NVIDIA guide: [NVIDIA AI Structured Cabling Reference Architecture](https://www.panduit.com/content/dam/panduit/en/website/solutions/applications/ai-data-center-solutions/documents/nvidia-ai-web-fbag15-sa-eng.pdf)
- NVIDIA DGX SuperPOD cabling guide: [Cable Management Best Practices](https://docs.nvidia.com/dgx-superpod/design-guide-cabling-data-centers/latest/cable-management-best-practices.html), [Cable Tray Standards](https://docs.nvidia.com/dgx-superpod/design-guide-cabling-data-centers/latest/cable-tray-standards.html), [Cable Management Guidance](https://docs.nvidia.com/dgx-superpod/design-guide-cabling-data-centers/latest/cable-management-guidance.html)
- Legrand Cablofil data center solutions: [Data Center Cable Management Solutions](https://www.legrand.us/cablofil/data-centers)
- Legrand Cablofil wire mesh tray: [Wire Mesh Cable Tray](https://www.legrand.us/cablofil/wire-mesh-cable-tray)
- Eaton Flextray: [B-Line Flextray wire mesh basket tray](https://www.eaton.com/us/en-us/catalog/support-systems/flextray-wire-mesh-basket-tray.html)
- nVent CADDY wire basket tray: [Wire Basket Tray System](https://www.nvent.com/en-us/caddy/products/wire-basket-tray-system)
- Cable Tray Institute standards: [Codes and Standards](https://www.cabletrays.org/codes-and-standards/)

行业报告与交叉验证：

- Grand View Research: [Electrical Conduit Market](https://www.grandviewresearch.com/industry-analysis/electrical-conduit-market-report)
- Grand View Research: [Cable Management System Market](https://www.grandviewresearch.com/industry-analysis/cable-management-system-market)
- Fortune Business Insights: [Cable Tray Market](https://www.fortunebusinessinsights.com/industry-reports/cable-tray-market-101529)
- Fortune Business Insights: [North America Electrical Conduit Market](https://www.fortunebusinessinsights.com/industry-reports/north-america-electrical-conduit-market-107444)
- OMR Global: [Data Center Cable Management Market](https://www.omrglobal.com/press-release/global-data-center-cable-management-market)
- Econ Market Research: [Cable Management Market](https://www.econmarketresearch.com/industry-report/cable-management-market)

本地项目底层假设：

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
# 行业调研：【动态UPS、飞轮与超级电容】

截至日期：2026-05-08  
口径：本报告聚焦 AI 数据中心、AI Factory、超算/高性能计算园区中用于毫秒级到分钟级电能质量、短时后备、负载平滑、发电机/微电网稳定的动态 UPS、飞轮储能与超级电容。美元为名义值。报告不是投资建议。

## 0. 高浓度结论

2026 年这个行业的核心变化不是“UPS 需求增长”，而是 AI 负载把传统数据中心电力系统从稳态工程推向动态工程。GB300/Blackwell Ultra、Rubin、Trainium、TPU、MI350/MI400、MTIA、Maia 等平台让单机架功率进入 100kW+，并且训练、后训练、agentic inference 会产生毫秒到秒级的同步负载跃迁。电力链条以前只要扛断电，现在还要扛“没有断电但上游电网、发电机、UPS、PDU 被高频冲击”的工况。

最值得跟踪的不是单一产品，而是三层短时储能架构：

| 层级 | 2026 最现实路线 | 2027 最可能升级 | 投资含义 |
|---|---|---|---|
| 园区/中压层 | 中压 UPS、BESS、DRUPS、飞轮稳定器、微电网控制 | 34.5kV 级 MV UPS、grid-forming BESS、BTM 自备电厂稳定器 | 项目金额最大，认证/交付壁垒高，ABB、Eaton、Vertiv、Piller/HITEC、Shoals/ON.energy、Schneider/Delta 受益 |
| 机房/UPS 层 | 大功率静态 UPS 加 AI 控制、动态旋转 UPS、飞轮 UPS | UPS 变成输入功率平滑器和电网交互资源 | 存量 UPS 厂商可以最快变现，飞轮和 DRUPS 在岛式/自备电园区弹性最大 |
| 机架/板级层 | OCP ORv3 BBU、锂电 BBU、超级电容/CBU 试点 | 超级电容、混合锂电+超级电容、800VDC power sidecar | 早期空间小但弹性最大，一旦被 hyperscaler 认证，可能从“几十万美元试点”跳到“每 GW 数亿美元” |

第一手信息显示行业已经进入产品化阶段：Piller 在 2025 年为 Nebius 芬兰 AI 数据中心供应 200 多台 Active Power CLEANSOURCE 无电池飞轮 UPS，并在 2026 年发布面向 AI 岛式电厂的 SHIELDX；HITEC 2026 年 AI DRUPS 白皮书直接把动态旋转 UPS 定义为可同时保护 IT 与冷却的 AI-tolerant UPS；ABB 2026 年在 Data Center World 发布 34.5kV HiPerGuard，并披露 Applied Digital 北达科他 400MW 与 300MW AI 园区部署；Vertiv 发布 Battery Shield 和 Input Power Smoothing；Eaton 2026 年白皮书把超级电容定位为应对 AI pulse-load 的关键；Skeleton 2026 年 5 月宣布 Pre-IPO 首轮 3300 万欧元融资，并把 AI 数据中心列为高功率储能核心应用。

传统市场报告给出的数据中心 UPS 市场 2025 年约 $4.4B-$10.2B、2030 年约 $8.9B-$12.5B，但这低估 AI 园区的真实机会，因为它通常不充分计入中压 UPS+BESS、BTM 自备电稳定器、机架级 BBU/CBU、以及微电网控制。我的乐观模型中，全球 AI 数据中心相关“短时储能/UPS/动态电能质量”订单池在未来 12 个月为 $9B-$22B，未来 24 个月累计可达 $25B-$75B；极度超预期情景下，如果 2027 年 Rubin/MI400/TPU8/ASIC 与 BTM 自备电同步放量，24 个月累计可上探 $95B。

## 1. 2026 年 AI 计算中心大规模建设下的机遇、挑战与技术路径

### 1.1 需求为什么突然变得很硬

来自项目内已有 AI 芯片路线图的判断：2026 年出货和上电主线仍是 NVIDIA GB300/B300 Blackwell Ultra、B200/GB200 延续、AWS Trainium2/3、Google TPU v7 Ironwood、AMD MI350、华为 Ascend 910C/950、寒武纪 MLU590/690、Meta MTIA、Microsoft Maia 200；2027 年 Rubin、MI400/MI455X、TPU8、Trainium3/4、OpenAI/Broadcom ASIC、Meta 多代 MTIA 会把机架密度继续推高。NVIDIA 2026 年 GTC 披露 Vera Rubin 平台已包含 NVL72、Vera CPU rack、Groq LPX、BlueField-4 STX、Spectrum-6 SPX，并通过 DSX Max-Q 在固定电力数据中心内部署 30% 更多 AI 基础设施，这意味着功率动态调度和短时缓冲会变成架构变量。

外部行业数据的交叉验证：

- MarketsandMarkets 2025 年报告预计数据中心 UPS 市场从 2025 年 $8.76B 增至 2030 年 $12.47B，CAGR 7.3%；同机构的数据中心 power market 预计从 2025 年 $35.14B 增至 2030 年 $50.51B。
- Uptime Institute 2026 年报告显示，2025 年提出的 100MW+ 巨型数据中心项目合计规划电力达到 181,209MW，其中 AI 相关规划功率在 colocation 与 hyperscale/cloud 两类中合计约 76,880MW。
- 彭博经 Tom's Hardware 转述的 2026 年美国数据中心口径显示，约 12GW 计划在 2026 年上线，但只有约三分之一处于 active construction，核心瓶颈是变压器、开关柜、电池等电气设备，部分大型变压器交期可达 5 年。
- OCP 在 2026 年 4 月 Open Data Center for AI 相关发布中，把低压直流、更高机架功率、数据中心 ESS 安全、现场发电和 BESS/微电网标准化列为重点。

结论：AI 数据中心客户在 2026 年愿意为三件事付溢价：更快上电、更少降频、更少被电网/发电机瞬态约束。动态 UPS、飞轮与超级电容正好卡在这个交点。

### 1.2 当前正在被使用的技术

| 技术 | 已使用形态 | 典型响应时间 | 优势 | 挑战 |
|---|---|---:|---|---|
| 静态双变换 UPS + 锂电/VRLA/NiZn | Vertiv、Schneider、Eaton、ABB、Delta、Huawei、Socomec 等 | ms 到秒级，取决于控制与储能 | 主流、可规模采购、服务网络强 | 电池浅循环老化、热失控/消防、AI 高频脉冲需要新控制 |
| 动态旋转 UPS / DRUPS | Piller UNIBLOCK、HITEC QPS、Kinolt/Euro-Diesel、Hitzinger、Rolls-Royce mtu 等 | 机械惯量天然瞬时 | 高短路容量、抗负载阶跃、可整合柴油/燃气、可保护冷却负载 | 机械系统、维护人才、噪声/排放/许可、单机运输和安装 |
| 飞轮 UPS | Active Power CLEANSOURCE、VYCON、Piller POWERBRIDGE 等 | ms 到秒级，通常 15 秒到 2 分钟 ride-through | 高功率密度、无电池更换、长寿命、低消防风险 | 能量密度低、长时后备仍需 genset/BESS，市场规模较小 |
| 中压 UPS / UPS-BESS | ABB HiPerGuard、Shoals+ON.energy MV AI UPS、EPC Power grid-forming BESS | ms 级逆变控制，分钟到小时级能量 | 减少低压转换、适合 100MW+ 园区、可参与 grid support | UL/IEC/并网认证、PCS/变压器/电池供应、项目制交付 |
| 超级电容/CBU | Eaton supercapacitor banks、Skeleton GrapheneGPU/GrapheneBBU、Capacitech C-Link 等 | us 到 ms 级 | 最适合高频脉冲、百万级循环、无热失控或低热失控风险 | 成本/kWh 高、漏电、机架空间、标准和 hyperscaler 认证早期 |
| 机架级 BBU | OCP ORv3 48V BBU、锂电 BBU、未来混合 BBU/CBU | ms 到秒级 | 靠近负载、减少上游过度设计、可标准化 | 分布式消防/热管理、维护和寿命模型复杂 |
| 800VDC / SST / grid-to-rack | Hitachi 800VDC 仿真、Delta 800VDC、NVIDIA DSX 生态 | 系统级 | 降低转换损耗、提升功率密度、便于高压直流配电 | 2026 多为样机/参考设计，保护与认证体系仍在形成 |

### 1.3 结合 2026-2027 AI 芯片路线的成熟与放量预测

| 技术路径 | 与芯片路线的触发点 | 基准情景成熟/放量 | 乐观情景成熟/放量 | 极度超预期情景 |
|---|---|---|---|---|
| 静态 UPS AI 控制：Battery Shield、IPS、grid-interactive UPS | GB300、Trainium2/3、TPU v7 形成 100kW+ 机架，负载阶跃先被 UPS 看到 | 2026H1 成熟，2026H2 新建项目 attach rate 20%-35%，2027 成为高端 UPS 默认功能 | 2026H2 在 hyperscale 项目快速导入，2027 attach 50%+ | 2026 年下半年被云厂商写入招标规范，存量 UPS 固件升级也贡献收入 |
| DRUPS/动态旋转 UPS 保护 IT+冷却 | 液冷泵、CDU、冷机与 AI 负载同时成为关键负载 | 2026 主要用于高可靠 greenfield、工业/政府/部分 AI 园区；2027 在 BTM 自备电项目加速 | 2026H2 因电网排队、自备电增加而上量 | 2027 前三大 AI 园区开发商把 DRUPS 作为标准备选，渗透率翻倍 |
| 飞轮 UPS 模块 | 需要 10 秒到 2 分钟 bridge、无电池/低消防风险 | 2026 由 Nebius 等项目验证，2027 在欧洲/美国 AI colo 扩张 | 2026H2 飞轮模块订单随 AI retrofit 上行 | 2027 与 BTM 发电、BESS 形成标准化短时 buffer 包 |
| 超级电容机架/设施级脉冲平滑 | DSX Max-Q、OCP ORv3、800VDC 让短时储能下沉 | 2026 试点，2027 小批量，2028 才明显放量 | 2026H2 Skeleton/Eaton/Capacitech 等拿到多个 hyperscaler 认证，2027 放量 | 2026 年底就出现单客户 100MW+ 超级电容 smoothing 订单，2027 进入每 GW $0.2B-$0.8B 附加价值 |
| 中压 UPS/BESS | 400MW-1GW 园区希望减少低压转换和房间面积 | 2026 产品和认证成熟，2027 随 ABB HiPerGuard、Shoals+ON.energy 类项目放量 | 2026 夏季订单开启，2027 成为 100MW+ 园区主流方案之一 | 2027 年 AI 园区以 34.5kV 接入和 grid-forming UPS 为核心，订单池超过传统低压 UPS 增速 |
| 800VDC/SST | Rubin/MI400/TPU8 与 1MW rack roadmap | 2026 仿真/示范，2027 首批，2028 放量 | 2027 上半年在 Vera Rubin DSX 标杆项目导入 | 2027 年 800VDC 被主流 AI reference design 确认为默认路线 |

### 1.4 2026 最可能的技术路径

最可能、最能出收入的是“静态大 UPS + AI 控制 + 锂电/NiZn + 部分 BESS”。理由是客户已认证、供应商全球服务能力强、能在 2026 年直接采购。Vertiv 的 IPS/Battery Shield、Eaton 的 grid-interactive UPS、Schneider/ABB/Delta 的集成电力方案都属于这一路线。

第二条是“中压 UPS/BESS + 微电网控制”。ABB 34.5kV HiPerGuard 在 2026 年 Data Center World 发布并取得 UL 9540 认证，Shoals 与 ON.energy 在 2026 年宣布面向领先 AI 数据中心运营商部署多 GW critical-power systems，这说明中压化正在从概念进入订单。

第三条是“DRUPS/飞轮用于高动态、岛式、自备电、政府/金融/欧洲高可靠场景”。Piller/HITEC 的 2026 年材料都强调 AI 负载与冷却负载可集中在 no-break 输出，Piller SHIELDX 则把自备电厂的频率/电压稳定作为 AI 园区痛点。这个方向不是最大众，但毛利和交付壁垒高，且在极度乐观 AI 园区建设情景下弹性最大。

第四条是“超级电容/CBU 从机架级和设施级试点开始”。2026 年还不是最大收入池，但可能是最大预期差。Eaton 明确提出 AI pulse power loading 可达到每秒 50% 需求变化，超级电容适合做 power smoothing banks；Skeleton 已经把 GrapheneGPU/GrapheneBBU 直接定位为 AI 数据中心 peak shaving 和 backup bridging。

## 2. 已经开始放量的关键产品：市场规模、渗透率、利润率

### 2.1 预测口径与核心假设

口径为全球 AI 数据中心相关新增订单/出货收入池，不含传统企业小 UPS，不含完整土建，不含 GPU/服务器，不含长期云服务收入。3 个月指 2026 年 5-8 月窗口；1 年指未来 12 个月；2 年指未来 24 个月累计。各产品可以叠加，不是互斥渗透率，因为一个园区可能同时使用 MV UPS、静态 UPS、BESS、机架 BBU 和超级电容。

基础换算假设：

| 项 | 基准 | 乐观 | 极度超预期 |
|---|---:|---:|---:|
| 未来 12 个月全球 AI 新增/改造可交付 IT 负载 | 7-10GW | 10-14GW | 14-20GW |
| 未来 24 个月全球 AI 新增/改造可交付 IT 负载 | 18-28GW | 30-45GW | 50-75GW |
| 受 AI 动态负载影响需要专门 power smoothing 的比例 | 25%-40% | 40%-60% | 60%-80% |
| 大型 UPS/短时储能硬件平均价值 | $120-$450/kW | $160-$650/kW | $220-$900/kW |
| 供不应求溢价 | 0%-8% | 8%-18% | 18%-35% |

### 2.2 已放量产品清单与三情景增长

| 产品/技术 | 已放量证据 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月累计市场规模 | 渗透率路径 | 毛利率预测 |
|---|---|---:|---:|---:|---|---|
| 大功率静态 UPS + AI 控制 + 锂电/NiZn | Vertiv IPS/Battery Shield、Eaton grid-interactive UPS、Schneider/Delta/ABB 大客户项目 | 基准 $1.8B-$3.2B；乐观 $3.0B-$5.0B；极超 $4.5B-$7.5B | 基准 $8B-$14B；乐观 $14B-$24B；极超 $22B-$38B | 基准 $20B-$38B；乐观 $40B-$75B；极超 $70B-$120B | 新 AI UPS 主链路 attach 2026: 55%-75%，2028: 60%-85%；AI 控制功能 attach 从 15%-25% 升至 45%-70% | 基准 28%-36%；乐观 34%-42%；极超 38%-48% |
| 中压 UPS / UPS-BESS / grid-forming BESS | ABB HiPerGuard 34.5kV、Applied Digital 400MW/300MW、Shoals+ON.energy 多 GW 协议 | 基准 $0.6B-$1.2B；乐观 $1.2B-$2.5B；极超 $2.5B-$5.0B | 基准 $3B-$7B；乐观 $7B-$15B；极超 $15B-$30B | 基准 $9B-$22B；乐观 $22B-$50B；极超 $45B-$95B | 100MW+ AI 园区 attach 2026: 5%-12%，2028: 18%-35%；极超可达 45% | 硬件 22%-32%；系统集成 25%-38%；极超供给紧张 35%-45% |
| 动态旋转 UPS / DRUPS | Piller UNIBLOCK 1MW-50MW、UBTD+ 500kW-40MW；HITEC AI DRUPS；政府/工业/数据中心存量验证 | 基准 $0.35B-$0.8B；乐观 $0.8B-$1.8B；极超 $1.5B-$3.2B | 基准 $1.8B-$4.0B；乐观 $4B-$8B；极超 $8B-$15B | 基准 $5B-$12B；乐观 $12B-$28B；极超 $25B-$55B | 全体 AI protected MW attach 2026: 4%-8%，2028: 7%-14%；岛式/BTM 园区可达 20%-35% | 基准 25%-35%；乐观 32%-42%；极超 38%-50%，服务毛利更高 |
| 飞轮 UPS 模块 | Active Power CleanSource HD 675kW/625kW、Nebius 200+ 台、VYCON/Piller Powerbridge 存量 | 基准 $0.12B-$0.30B；乐观 $0.30B-$0.75B；极超 $0.7B-$1.5B | 基准 $0.7B-$1.6B；乐观 $1.6B-$3.8B；极超 $3.5B-$7.5B | 基准 $1.8B-$5B；乐观 $5B-$12B；极超 $10B-$25B | AI 项目 attach 2026: 2%-5%，2028: 5%-12%；在电池受限/低消防风险场景更高 | 基准 30%-42%；乐观 38%-48%；极超 45%-55% |
| 机架级锂电 BBU / OCP ORv3 BBU | OCP ORv3 48V BBU 规范、ORv3 rack 广泛采用、AI rack 需要本地短时备电 | 基准 $0.35B-$0.8B；乐观 $0.8B-$1.8B；极超 $1.6B-$3.5B | 基准 $2B-$5B；乐观 $5B-$11B；极超 $10B-$22B | 基准 $6B-$16B；乐观 $16B-$38B；极超 $35B-$75B | 高密 AI rack attach 2026: 10%-25%，2028: 30%-60% | BBU pack 18%-30%；安全/热管理方案 30%-45%；极超 35%-50% |
| UPS 监控、微电网 EMS、功率动态软件 | Vertiv/Schneider/Eaton/ABB/Delta DCIM+EPMS，NVIDIA DSX Flex/Max-Q 方向 | 基准 $0.15B-$0.35B；乐观 $0.35B-$0.8B；极超 $0.8B-$1.5B | 基准 $0.8B-$2B；乐观 $2B-$5B；极超 $5B-$10B | 基准 $2B-$7B；乐观 $7B-$18B；极超 $16B-$35B | 新 AI 园区 attach 2026: 20%-40%，2028: 55%-80% | 软件/服务 55%-80%；极超 70%-85% |

### 2.3 最可能出现高溢价的已放量产品

| 排名 | 产品 | 为什么能溢价 | 2026-2027 价格趋势 |
|---:|---|---|---|
| 1 | 中压 UPS/BESS 与 grid-forming 控制 | 认证少、项目巨大、客户不能因 UPS 延期导致 GPU 空转 | 2026H2 到 2027H1 溢价最强，可能高于常规 UPS 10%-25% |
| 2 | DRUPS/动态旋转 UPS | 机械+电气+发电机集成经验稀缺，现场调试和服务壁垒高 | 大客户定制化强，毛利优于常规硬件 |
| 3 | 飞轮 UPS | 无电池、低消防风险、长寿命，在电池交付/消防压力下替代价值上升 | ASP 稳中升，规模化不足限制成本下降 |
| 4 | AI UPS 控制软件/固件 | 在既有 UPS 平台上增加价值，边际成本低 | 软件毛利高，常绑定硬件和服务合同 |
| 5 | 机架级 BBU 安全/热管理 | 分布式锂电进入 rack 后，热失控与维护成为客户痛点 | 安全认证和客户白名单带来溢价 |

## 3. 在研与早期关键产品：未来快速增长方向

### 3.1 在研产品与细分技术

| 技术 | 2026 阶段 | 关键公司 | 成熟与放量判断 |
|---|---|---|---|
| 超级电容设施级 power smoothing bank | 试点到小批量 | Eaton、Skeleton、Capacitech、UCAP/Maxwell、KYOCERA AVX、LS Mtron、VINATech、Nichicon | 2026 验证，2027 小规模放量，2028 若 OCP/UL 标准明确后大幅放量 |
| 机架级 CBU/混合 BBU | 研发/早期认证 | Skeleton GrapheneBBU、OCP 生态、Murata、Delta、Advanced Energy、KULR 安全方案 | 2026 下半年样机，2027 随 ORv3/ORW 和 800VDC 进入早期订单 |
| 800VDC + SST + BESS | 仿真/示范 | Hitachi Energy、Delta、Eaton、Siemens Energy、Navitas、Infineon、onsemi、ST、TI | 2026 reference design，2027 首批，2028 主流化概率上升 |
| 多层 ESS 协调：chip/rack/facility/grid | 学术与供应商联合验证 | NVIDIA DSX、Emerald AI、Vertiv、Eaton、ABB、Schneider、EPC Power、大学/电网研究团队 | 2026 先软件化，2027 绑定 grid services 和 interconnection |
| 飞轮+BESS+燃机/柴油的 BTM 稳定器 | 已有产品，AI 场景重定义 | Piller SHIELDX、HITEC、Bergen Engines、Marelli、Rolls-Royce、Caterpillar、Cummins | 2026 岛式项目导入，2027 若自备电爆发则快速放量 |
| 固态变压器驱动 UPS / MVDC-LVDC | 研究/试点 | EPC Power、Hitachi、ABB、Eaton/Resilient Power、Siemens Energy、华为数字能源 | 2027 前收入较小，2028 后若 800VDC 成标准会明显扩张 |

### 3.2 早期产品市场规模与利润率预测

| 早期产品 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月累计市场规模 | 渗透率路径 | 毛利率预测 |
|---|---:|---:|---:|---|---|
| 超级电容设施级 smoothing bank | 基准 $50M-$150M；乐观 $150M-$400M；极超 $400M-$900M | 基准 $0.4B-$1.2B；乐观 $1.2B-$3B；极超 $3B-$7B | 基准 $1.5B-$5B；乐观 $5B-$15B；极超 $15B-$35B | AI 园区 attach 2026 <3%，2028 基准 5%-10%，极超 20%-30% | 初期项目 30%-45%；材料/IP 龙头 45%-65%；极超 55%-70% |
| 机架级超级电容 CBU / 混合 BBU | 基准 $20M-$100M；乐观 $100M-$300M；极超 $300M-$800M | 基准 $0.2B-$0.8B；乐观 $0.8B-$2.5B；极超 $2.5B-$6B | 基准 $1B-$4B；乐观 $4B-$13B；极超 $12B-$30B | 高密 rack attach 2026 <2%，2028 基准 8%-18%，极超 30%+ | 模组 25%-40%；系统/IP 40%-60%；极超 55%-70% |
| 800VDC/SST power train | 基准 $50M-$200M；乐观 $200M-$700M；极超 $0.7B-$1.8B | 基准 $0.6B-$2B；乐观 $2B-$6B；极超 $6B-$14B | 基准 $4B-$12B；乐观 $12B-$35B；极超 $35B-$80B | 2026 示范，2027 少数 AI factory，2028 可能 10%-25% 新建 attach | 系统 25%-38%；功率半导体/控制 35%-55% |
| AI 动态功率编排软件 | 基准 $80M-$250M；乐观 $250M-$700M；极超 $0.7B-$1.5B | 基准 $0.5B-$1.5B；乐观 $1.5B-$4B；极超 $4B-$9B | 基准 $1.5B-$6B；乐观 $6B-$18B；极超 $18B-$40B | 2026 先随大型 UPS/MV UPS 出货，2027 绑定电网服务和 SLAs | 60%-85% |
| SHIELDX 类飞轮/电磁稳定器 | 基准 $80M-$250M；乐观 $250M-$700M；极超 $0.7B-$1.6B | 基准 $0.7B-$2B；乐观 $2B-$5B；极超 $5B-$12B | 基准 $3B-$9B；乐观 $9B-$25B；极超 $25B-$55B | BTM 自备电 AI 园区 attach 2026: 5%-10%，2028: 20%-40% | 30%-45%；服务/备件 45%-60% |

### 3.3 为什么超级电容可能成为最大预期差

超级电容不是替代电池的长时储能，而是替代“为了毫秒到秒级尖峰而过度配置的电网、发电机、UPS、电缆、变压器容量”。Eaton 2026 年白皮书指出，生成式 AI 可带来每秒 50% 的需求变化，超级电容可以在峰值放电、低谷充电。Skeleton 产品页给出的数据包括 1 秒充电、最长 1 分钟放电、92.6kW/L 功率密度、20 年以上寿命；GrapheneBBU 则强调最长 90 秒 backup bridging 和 90 秒充电。

我的判断：2026 年超级电容的收入不会很大，但若 2027 年客户从“买更多变压器/发电机”转向“买更快的脉冲缓冲”，超级电容的 TAM 会从普通 supercapacitor 市场中脱离出来，变成 AI power train 的独立增量。最乐观路径是 hyperscaler 把 CBU 或 smoothing bank 写进 ORv3/ORW/800VDC reference design。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 主要产能与工艺分布

| 环节 | 主要地区 | 主要公司 | 关键工艺/资产 |
|---|---|---|---|
| 动态旋转 UPS / DRUPS | 德国、荷兰、比利时/欧洲、美国、日本、中国 | Piller、HITEC、Kinolt/Euro-Diesel、Hitzinger、Rolls-Royce mtu、Air Water/Power Partners、Kehua、KSTAR 等 | 大型电机、飞轮、柴油/燃气耦合、离合器、MV switchgear、现场调试 |
| 飞轮 UPS | 美国、德国、欧洲、中国 | Active Power、Piller、VYCON/Calnetix、Beacon Power、Amber Kinetics、Stornetic、Levisys、Zooz Power、Dumarey Green Power | 高速转子、磁/机械轴承、真空腔体、IGBT/SiC 变换器、控制算法 |
| 超级电容单体 | 日本、韩国、中国、欧洲、美国 | Skeleton、Eaton、UCAP/Maxwell、KYOCERA AVX、Nichicon、Panasonic、Nippon Chemi-Con、LS Mtron、VINATech、Samwha、CAP-XX、Tecate、Yunasko、奥威科技、宁波中车新能源等 | 活性炭/石墨烯/曲面石墨烯、电解液、隔膜、卷绕/叠片、老化分选 |
| 超级电容模组/系统 | 欧洲、美国、中国、台湾 | Skeleton、Eaton、Capacitech、Delta、Murata、Advanced Energy、KULR、KEMET/YAGEO 等 | 模组均衡、busbar、BMS/EMS、热管理、绝缘与安全认证 |
| 大型 UPS/MV UPS/BESS | 美国、欧洲、中国、印度/东南亚 | Vertiv、Schneider、Eaton、ABB、Delta、Huawei、Socomec、Riello、Toshiba/Mitsubishi、Fuji、Shoals/ON.energy、EPC Power | PCS、变压器、开关柜、锂电/钠电/NiZn 电池柜、控制软件 |
| 功率电子与控制 | 美国、欧洲、日本、中国台湾、中国大陆 | Infineon、onsemi、ST、TI、Wolfspeed、Navitas、Mitsubishi Electric、Fuji、Semikron Danfoss、Hitachi Energy | IGBT/SiC/GaN、驱动、传感、实时控制、保护算法 |

### 4.2 供给瓶颈

1. 变压器、开关柜、中压断路器、busway 交期：AI 项目可以 12-18 个月建楼，但大型电气设备可能 24-60 个月。
2. 大型旋转电机与飞轮转子加工：高速转子材料、动平衡、真空腔体、轴承可靠性验证产能有限。
3. 现场工程师与调试队伍：DRUPS/MV UPS 不是箱子到场即可运行，需要并网、发电机、保护、短路电流、负载阶跃联合调试。
4. UL 9540/9540A、IEC、NFPA、Uptime Tier、OCP、低电压穿越等认证：AI 园区客户采购前需要系统级安全和可靠性证据，认证周期就是壁垒。
5. 电池与超级电容材料：锂电受储能/EV/数据中心共同争抢；超级电容受高纯活性炭、石墨烯材料、电解液一致性和老化分选影响。
6. 功率半导体和大电流电容电感：SiC/GaN/IGBT 模块、薄膜电容、电感、母排和热管理决定高功率密度 PCS/UPS 的交付。
7. 柴油/燃气机组排放与许可：DRUPS/BTM 自备电受噪声、NOx、燃料供应、空气许可、备用运行小时数限制。
8. 客户认证窗口：hyperscaler 一旦验证通过会快速放量，但从样机到白名单通常需要 6-18 个月。
9. 消防与保险：机架级锂电 BBU、BESS 和超级电容进入数据厅时，FM Global/保险人/消防顾问会实质影响方案。
10. 标准尚未完全稳定：800VDC、ORW、facility ESS safety、grid-flexible AI factory 仍在 2026-2027 成形，过早押注可能面临架构切换。

### 4.3 成本结构与毛利决定因素

| 产品 | 典型成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| DRUPS/动态 UPS | 旋转电机/飞轮 18%-25%；柴油/燃气机组与离合 18%-30%；PCS/控制 12%-18%；开关柜/变压器 15%-25%；外壳冷却安装 8%-12%；测试服务 10%-18% | 单机 MW 级别、定制化、服务网络、现场调试能力、客户认证 | 铜/电工钢/发动机/功率模块涨价通过项目报价和 change order 传导 |
| 飞轮 UPS | 转子/轴承/真空 25%-35%；电机 15%-22%；变换器 18%-25%；外壳冷却 8%-12%；控制软件 5%-8%；测试服务 10%-15% | 转子可靠性、现场寿命数据、功率密度、无电池 TCO | 供给紧张时按 kW 溢价；长期以生命周期成本销售 |
| 超级电容模组 | 单体 35%-55%；busbar/均衡/BMS/热管理 20%-30%；PCS/接口 10%-20%；测试认证 5%-10% | 单体能量密度、ESR、一致性、循环寿命、客户认证 | 早期按功能价值定价；规模后单体降本，但系统/软件保留溢价 |
| 静态 UPS + 电池 | UPS 功率模块 25%-40%；电池 20%-35%；开关保护 10%-20%；机柜/冷却 8%-12%；服务 10%-18% | 效率、模块化、维护便利、AI 控制功能、服务半径 | 电池、铜、半导体、关税通过季度价格调整 |
| MV UPS/BESS | 电池 30%-45%；PCS 20%-30%；变压器/开关柜 15%-25%；EMS 5%-10%；EPC 10%-20% | UL/IEC 认证、grid-forming 算法、并网经验、项目交付 | 项目制锁价，长交期设备采用 escalator 或预付款 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

传统大型三相 UPS 与数据中心 power infrastructure 是 Vertiv、Schneider、Eaton、ABB、Delta、Huawei 等头部厂商的市场，集中度高但不是赢家通吃。Vertiv 2025 年年报称其在 thermal management 以及三相大型 UPS/配电基础设施领域为第一梯队，且 2025 年约 85% 收入来自数据中心。Schneider 2026 Q1 披露 Data Center & Networks 强双位数增长，North America 仍是主要需求区域。Delta 2026 年 Data Center World 披露其在美国数据中心已经部署超过 6.5GW UPS 容量。

动态旋转 UPS/DRUPS 和飞轮 UPS 是更小、更集中的市场。Piller/Active Power、HITEC、Kinolt/Euro-Diesel、VYCON、Hitzinger 等少数公司有长期现场数据和大型客户认证。我估计 AI 数据中心可采购的高端 DRUPS/飞轮 UPS 中，前五名公司收入份额可达 70%-85%。

超级电容单体市场分散，但 AI 数据中心系统级应用高度早期。Skeleton、Eaton、UCAP/Maxwell、KYOCERA AVX、Nichicon、LS Mtron、VINATech、Capacitech 等都有技术或产品入口；真正壁垒不只是 cell，而是“在 AI power topology 中被认证为可维护、可监控、可保险的系统”。

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| 可靠性现场数据 | 运行小时、故障率、MTBF、客户复购 | AI 园区 GPU 空转一天损失巨大，客户愿意为可证明可靠性付费 |
| 大功率短路/负载阶跃能力 | 10%-100% load step、短路电流倍数、频率/电压偏差 | AI 动态负载下，能否不让发电机/电网跳闸是核心价值 |
| 认证 | UL 9540/9540A、IEC、OCP、Uptime、FM、NFPA | 未认证产品无法进入大型项目，认证周期让新进入者慢 1-2 年 |
| 服务网络 | 服务工程师数量、备件响应时间、全球现场覆盖 | UPS/DRUPS 是生命线设备，客户买的是全生命周期可用性 |
| 系统集成 | UPS+switchgear+BESS+genset+EPMS+cooling 联调能力 | 单设备便宜但系统不稳没有价值，集成商可把复杂度转化为毛利 |
| 客户锁定 | hyperscaler 白名单、参考架构、长期框架协议 | 一旦进入标准设计，复制到多个园区，销售成本下降而毛利稳定 |
| 供应链锁定 | 变压器、功率模块、超容 cell、飞轮转子、发动机产能 | 2026-2027 交付能力本身就是定价权 |

### 5.3 价值捕获判断

长期高 ROIC 最可能在三层：

第一层是“中压 UPS/PCS/控制软件平台”。原因是认证壁垒高、项目价值大、替换成本高、服务收入长尾明显。ABB HiPerGuard、Eaton/Vertiv/Schneider 的 grid-interactive UPS、Shoals+ON.energy 的 MV AI UPS 都符合这一方向。

第二层是“动态 UPS/飞轮的核心机械和控制平台”。市场没有静态 UPS 大，但客户场景高可靠、定制化、服务毛利高，且 AI 自备电和岛式园区会把飞轮/旋转惯量重新估值。

第三层是“超级电容材料+模组+系统认证”。如果 Skeleton/Eaton/Capacitech 等能证明在 AI 负载下减少电力预留、减少降频、降低发电机冗余，定价会从 $/Wh 转向 $/kW 和 $/可释放算力，毛利上限会比普通电容高很多。

低 ROIC 风险较大的层是纯 EPC、低端 UPS 组装、普通电池柜和无差异化 BESS 集成，因为价格会被规模供应商和项目招标压低。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点一：AI 负载瞬态成为正式设计输入

Vertiv、Eaton、HITEC、Piller、EPC Power、NVIDIA/OCP 的 2026 年材料都指向同一件事：AI 数据中心不是稳定负载，传统按峰值容量和断电 ride-through 的 UPS 设计不足以覆盖高频功率波动。2026 年最可能放量的是 UPS firmware/controls、输入功率平滑、Battery Shield、设施级 smoothing。

### 拐点二：中压 UPS 与 BESS 从示范进入招标

ABB HiPerGuard 34.5kV 取得 UL 9540 并计划 2026 年夏季开放订购，Applied Digital 400MW/300MW 项目提供了大型 AI 园区锚点。Shoals+ON.energy 的多 GW 协议说明 MV UPS 与 utility-scale storage 正在进入 AI 数据中心采购框架。2026 年下半年最可能放量的是 100MW+ 园区的 MV UPS、PCS、BESS、switchgear。

### 拐点三：BTM 自备电让 DRUPS/飞轮重新变成战略设备

Uptime Institute 显示 2025 年巨型数据中心提案中大量仍依赖电网，但电网将限制扩张；Eaton 明确说 BYOP/on-site generation 可绕开电网扩建节奏。自备电厂缺少大电网惯量，AI 负载尖峰会冲击发动机和燃机，Piller SHIELDX 类设备正是为此出现。2026 年最可能增长的是岛式 AI 园区的动态稳定器、DRUPS 和飞轮短时储能。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点一：Rubin/MI400/TPU8/HBM4 把机架功率再次上推

2027 年高端 GPU/ASIC 会从 GB300/Trainium2/TPU v7 过渡到 Rubin、MI400、TPU8、Trainium3、OpenAI/Broadcom ASIC。机架功率、液冷依赖、功率瞬态都会提高。最可能放量的是 800VDC、机架级 BBU/CBU、液冷 CDU 的 no-break 电源、AI UPS 控制软件。

### 拐点二：超级电容从“太贵”变成“便宜的电力预留替代品”

如果一个 100MW AI 园区因为尖峰需要多预留 10%-20% 发电/变压器/UPS 容量，增量 CapEx 可能是数千万到上亿美元。超级电容如果能削减 5%-15% 的预留容量，即使按 $150-$500/kW 定价也有经济性。2027 年最可能出现第一批多 MW 到百 MW 级超级电容 smoothing bank 订单。

### 拐点三：标准化开始淘汰小供应商

OCP Open DC for AI、ORv3/ORW、ESS safety、LVRT/grid-flex 规范会使 AI 电力架构更开放，但也更严苛。2027 年后，没有 UL/IEC/OCP 认证、没有 hyperscaler 运行数据、没有全球服务网络的供应商会被排除；头部公司反而更容易提价和扩份额。

## 8. 头部公司与细分技术公司清单

### 8.1 大型 UPS、MV UPS、数据中心电力集成

Vertiv、Schneider Electric/APC、Eaton、ABB、Delta Electronics、Huawei Digital Power、Socomec、Riello UPS、Legrand/Starline/Raritan、Toshiba、Mitsubishi Electric、Fuji Electric、Kehua Data、KSTAR、S&C Electric、Powell Industries、Hubbell、nVent、Siemens、Hitachi Energy、TMEIC。

### 8.2 动态旋转 UPS / DRUPS / 旋转电源

Piller Group、Active Power、HITEC Power Protection、Kinolt/Euro-Diesel、Hitzinger、Rolls-Royce mtu Kinetic PowerPack/Power Systems、Air Water/Power Partners、Marelli Motori、Bergen Engines、Caterpillar、Cummins、Himoinsa、Pramac/Generac、Kohler Energy、Kehua、KSTAR。

### 8.3 飞轮储能与飞轮 UPS

Active Power、Piller POWERBRIDGE、VYCON/Calnetix、Beacon Power、Amber Kinetics、Stornetic、Levisys、Zooz Power、Dumarey Green Power、Punch Flybrid、Adaptive Balancing Power、Kinetic Traction Systems、Schwungrad Energie、Temporal Power/NRStor、Vycon Energy partners。

### 8.4 超级电容单体、模组与系统

Skeleton Technologies、Eaton Electronics、UCAP Power/Maxwell ultracapacitor、KYOCERA AVX、Nichicon、Panasonic Industry、Nippon Chemi-Con、LS Mtron、VINATech、Samwha、KEMET/YAGEO、CAP-XX、Tecate Group、Cornell Dubilier、Yunasko、NAWA Technologies、Capacitech Energy、奥威科技、宁波中车新能源、锦州凯美、上海奥威、Nesscap 历史资产相关供应链。

### 8.5 机架级电源、BBU、CBU、OCP 生态

Advanced Energy、Murata、Delta、Lite-On、AcBel、Bel Fuse、Flex Power Modules、Vicor、Infineon、onsemi、STMicroelectronics、Texas Instruments、Navitas、Wolfspeed、Monolithic Power Systems、KULR Technology、Americase、Sanmina、Celestica、Jabil、Flex、Foxconn、Quanta、Wiwynn、Supermicro、OCP Open Rack V3/ORW 生态。

### 8.6 微电网、BESS、现场能源与并网控制

ABB、Eaton、Schneider Electric、Vertiv、EPC Power、Shoals Technologies、ON.energy、Tesla Megapack、Fluence、Powin、Generac、Bloom Energy、GE Vernova、Siemens Energy、Caterpillar、Cummins、Rolls-Royce Power Systems、Plug Power、Enchanted Rock、NextEra Energy、AES、Constellation、Vistra、Invenergy、Nscale Energy & Power、Hitachi Energy。

## 9. 投资跟踪指标

| 指标 | 观察方法 | 看多信号 |
|---|---|---|
| AI UPS 控制是否被写入 RFP | Vertiv/Eaton/Schneider/ABB 发布、客户 tender、OCP 规范 | IPS/Battery Shield/grid-interactive UPS 从 optional 变 mandatory |
| 中压 UPS 订单 | ABB HiPerGuard、Shoals+ON.energy、Applied Digital 类项目披露 | 单项目 100MW+、电压 13.8kV/34.5kV、UL/IEC 认证 |
| DRUPS/飞轮订单 | Piller/HITEC/Active Power 新闻、Langley/Piller 报告 | AI 数据中心客户从几十 MW 扩到百 MW，多园区复制 |
| 超级电容认证 | Skeleton/Eaton/Capacitech/OCP/UL 客户验证 | hyperscaler 公开 reference design 或百 MW 级采购 |
| 机架级 BBU/CBU 安全标准 | OCP ORv3/ORW、UL、FM、保险指南 | power sidecar 标准化，消防/维护流程明确 |
| 800VDC 真实部署 | NVIDIA DSX、Hitachi/Delta/Eaton/Siemens 试点 | 从仿真演示变成 Vera Rubin/MI400 实际园区 |
| 价格与毛利 | 供应商 backlog、book-to-bill、lead time、gross margin | backlog 超 12 个月且毛利不被铜/电池成本侵蚀 |

## 10. 主要资料来源

| 来源 | 关键事实/用途 |
|---|---|
| [Piller SHIELDX Dynamic Power Stabilization](https://www.piller.com/product/shieldx-dynamic-power-stabilisation/) | AI 负载大阶跃、自备电厂 ramp-rate、BESS 局限、4-6 周 built-to-stock |
| [Piller UNIBLOCK UPS](https://www.piller.com/product/uniblock-ups-from-150kw-up-to-50mw/) | UB-V 1MW-50MW、UBTD+ 500kW-40MW、flywheel/battery ride-through |
| [Piller Nebius AI data center order](https://www.piller.com/major-expansion-of-high-performance-data-center-in-southern-finland/) | Active Power 为 Nebius 芬兰 75MW AI 数据中心供应 200+ CLEANSOURCE battery-free UPS |
| [Piller US Government repeat order](https://www.piller.com/classified-us-government-data-center-repeat-order/) | 2026 年美国政府 classified data processing facility 复购 UNIBLOCK rotary UPS |
| [Active Power CLEANSOURCE HD](https://www.activepower.com/product/cleansource-hd-ups/) | 675kW/625kW、35 sqft、10.2MJ flywheel、20 年无电池更换、最高 98% 效率 |
| [HITEC AI DRUPS whitepaper](https://hitec-ups.com/wp-content/uploads/2026/01/HITEC-Whitepaper-Artificial-Intelligence-and-Dynamic-Rotary-UPS-Systems.pdf) | 动态旋转 UPS 可同时保护 IT 与冷却，单机到 3600kVA，AI rack 100kW+ |
| [ABB HiPerGuard 34.5kV](https://www.globenewswire.com/news-release/2026/04/21/3278541/0/en/New-34-5kV-HiPerGuard-UPS-direct-grid-connection-cuts-AI-data-center-power-costs.html) | Data Center World 2026 发布，UL 9540，4.16kV-34.5kV，Applied Digital 400MW/300MW |
| [Vertiv Input Power Smoothing](https://www.vertiv.com/en-us/insights/articles/white-papers/enabling-stable-power-protection-for-next-generation-ups-solutions-with-input-power-smoothing-ips/) | Battery Shield、IPS、AI 负载平滑、保护发电机与上游基础设施 |
| [Vertiv 2025 Annual Report](https://www.sec.gov/Archives/edgar/data/1674101/000119312526174909/d27762dars.pdf) | 数据中心收入占比、三相大型 UPS/配电基础设施地位、服务工程师网络 |
| [Eaton AI and data centers supercapacitor whitepaper](https://www.eaton.com/content/dam/eaton/products/electronic-components/resources/brochure/eaton-ai-and-data-centers-white-paper-elx1549-en.pdf) | AI pulse-load 每秒可达 50% 变化，超级电容平滑电力需求 |
| [Eaton integrated energy strategies](https://www.eaton.com/us/en-us/markets/data-centers/impact-of-ai-data-center-infrastructure/integrated-energy-strategies-ai-data-centers.html) | BYOP、BESS、grid-interactive UPS、微电网架构 |
| [Eaton Q1 2026 presentation](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf) | 与 NVIDIA 的 AI factory power blueprint、grid-to-chip 架构 |
| [Delta Data Center World 2026](https://www.delta-americas.com/en-US/news/delta-unveils-integrated-power%2C-cooling%2C-and-infrastructure-architecture-for-ai-data-centers-at-data-center-world-2026) | Delta grid-to-chip power/cooling/control，已在美国数据中心部署 6.5GW+ UPS |
| [NVIDIA Vera Rubin GTC 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | Rubin、LPX、STX、Spectrum-6，DSX Max-Q 固定电力下多部署 30% AI infrastructure |
| [NVIDIA + Emerald AI flexible AI factories](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Emerald-AI-Join-Leading-Energy-Companies-to-Pioneer-Flexible-AI-Factories-as-Grid-Assets/default.aspx) | AI factory 作为 grid-flexible asset，co-located generation and storage |
| [OCP Open Data Center for AI](https://www.opencompute.org/projects/open-dc-for-ai) | 1MW rack roadmap、GW/multi-GW campus、BESS/microgrid/LVRT 标准方向 |
| [OCP April 2026 ecosystem announcement](https://www.hpcwire.com/off-the-wire/open-compute-project-delivering-an-open-data-center-ecosystem-for-ai/) | 低压 DC、数据中心 ESS 安全、AI cluster/reference architecture |
| [OCP ORv3 BBU Module Spec](https://www.opencompute.org/documents/open-rack-v3-bbu-module-spec-1-4-pdf) | rack-level BBU 技术规范、E-cap life、pulse power 等要求 |
| [Skeleton Pre-IPO funding](https://www.skeletontech.com/news/skeleton-announces-first-close-of-pre-ipo-funding-round) | 2026 年 5 月首轮 3300 万欧元、德国超级电容、芬兰 1GW SuperBattery、美国扩产计划 |
| [Skeleton data center peak shaving](https://www.skeletontech.com/datacenters-peak-shaving-power-backup) | 1 秒充电、最长 1 分钟放电、92.6kW/L、20+ 年寿命、GrapheneBBU 90 秒 |
| [Skeleton Houston facility via DCD](https://www.datacenterdynamics.com/en/news/supercapacitor-developer-skeleton-opens-first-us-manufacturing-facility-in-houston-texas/) | 2026 年美国工程设施、H1 2026 规划 AI 数据中心制造能力、美国部署 100MW+ |
| [Capacitech AI voltage sags](https://www.capacitechenergy.com/blog/how-supercapacitors-eliminate-voltage-sags-in-ai-data-centers) | AI 毫秒级瞬态、电压暂降、超级电容补充传统 UPS |
| [MarketsandMarkets Data Center UPS report](https://pdf.marketpublishers.com/marketsnmarkets/data-center-ups-market-mnm.pdf) | 数据中心 UPS 2025 $8.76B、2030 $12.47B |
| [MarketsandMarkets Data Center Power via PRNewswire](https://www.prnewswire.com/news-releases/data-center-power-market-worth-50-51-billion-by-2030--marketsandmarkets-302564168.html) | 数据中心 power market 2025 $35.14B、2030 $50.51B，UPS 为最大电力解决方案 |
| [Yano supercapacitor market](https://www.yanoresearch.com/en/press-release/show/press_id/4066) | 全球超级电容 2025 3107 亿日元、2030 6332 亿日元，AI 应用扩张 |
| [Grand View U.S. flywheel market](https://www.grandviewresearch.com/horizon/outlook/flywheel-energy-storage-system-market/united-states) | 美国 FESS 2023 $292M、2030 $575M，UPS/数据中心为细分应用 |
| [Technavio flywheel market](https://www.technavio.com/report/flywheel-energy-storage-market-industry-analysis) | 2026-2030 flywheel 市场增量 $283.5M，UPS 为 2024 最大技术收入段，披露 2025 Piller 400MW AI 项目线索 |
| [Uptime Institute giant data center power plans 2026](https://intelligence.uptimeinstitute.com/sites/default/files/2026-01/UI%20Field%20report%20194_Giant%20data%20center%20power%20plans%20reach%20extreme%20levels.pdf) | 2025 年 100MW+ 数据中心规划 181,209MW，AI 规划功率显著上升 |
| [Tom's Hardware/Bloomberg data center delays](https://www.tomshardware.com/tech-industry/artificial-intelligence/half-of-planned-us-data-center-builds-have-been-delayed-or-canceled-growth-limited-by-shortages-of-power-infrastructure-and-parts-from-china-the-ai-build-out-flips-the-breakers) | 2026 美国 12GW 计划上线、约三分之一 active construction、变压器/开关柜/电池瓶颈 |
| [EPC Power grid-forming AI data centers](https://www.epcpower.com/insights/agile-grid-forming-power-for-data-centers) | rack-level 超级电容、flywheel/UPS 短时限制、3MW 到 100MW+ BESS、ms 级 grid-forming |
| [Hitachi 800VDC + NVIDIA DSX](https://www.nasdaq.com/press-release/hitachi-unveils-800-vdc-power-supply-simulation-enabled-nvidia-omniverse-dsx) | 800VDC grid-to-rack、spiky AI workloads 仿真、BESS 平滑、15x legacy power |
| [arXiv 2603.00415](https://arxiv.org/abs/2603.00415) | AI 数据中心 ESS 四层架构：chip/rack/facility/grid，传统 ESS dispatch 不足 |
| [arXiv EasyRider](https://arxiv.org/abs/2604.15522) | rack-level passive + actively-controlled auxiliary energy storage 缓解训练负载功率波动 |
| [S&P Global 451 Research 2026 Trends](https://www.spglobal.com/content/dam/spglobal/energy/en/documents/news-research/special-reports/E-0326-2026-Trends-Report-Preview-Data-Center-Services-Infrastructure.pdf) | 2026 数据中心建设继续、约束影响选址和速度、AI 促进电力/冷却创新 |

## 11. 读数注意事项

1. 传统 UPS 报告、flywheel 储能报告和 supercapacitor 报告的统计口径差别极大。本报告的 AI 数据中心订单池口径会大于单独 UPS 市场，因为纳入了 MV UPS、BESS、机架级 BBU/CBU、微电网控制和 power smoothing。
2. 超级电容用 $/kWh 衡量会显得昂贵，但 AI 场景应更多按 $/kW、响应时间、减少电力预留和释放算力价值衡量。
3. DRUPS 和飞轮 UPS 不会替代所有静态 UPS。它们最有价值的场景是自备电/岛式园区、高动态机械负载、低消防风险、政府/金融/工业高可靠项目。
4. 极度超预期情景的前提是：2026H2-2027 Blackwell/Rubin/ASIC 交付不被 HBM/CoWoS/电力接入明显拖累，且 hyperscaler 愿意把电力 smoothing 写入标准设计。
5. 最大风险是项目延期、客户改用负载调度/降频而不是硬件 buffer、超级电容认证慢、柴油/燃气许可受限、以及传统 UPS 厂商用固件升级压低独立短时储能供应商价值。
# 行业调研：【功率半导体与高压保护器件】

> 截至日期：2026-05-08  
> 研究范围：AI 数据中心/AI Factory 电源树中的功率半导体与高压保护器件，包括 Si/SiC/GaN MOSFET、IGBT/SiC 模块、GaN/SiC PFC 与 LLC 器件、48V/54V hot-swap/eFuse/ORing、800V HVDC PDB 与热插拔控制、Vcore 多相控制器/智能功率级/电源模块、TVS/MOV/GDT/thyristor/fuse/SSCB 等。  
> 口径说明：本报告的市场规模为从 2026-05-08 起的滚动期间收入/订单池估算，`B` = 十亿美元，`M` = 百万美元。对未公开直接数据处采用偏乐观假设，并用 TechInsights、NVIDIA/GE Vernova、TI/ST/Navitas/Infineon/onsemi/Vicor/MPS/Littelfuse 等公开资料交叉校验。非投资建议。

## 0. 最高浓度结论

1. **2026 最确定放量的不是 800V，而是 48V/54V AI 机架电源树全面升级。** GB300/B300、GB200、Trainium2、TPU Ironwood、MI350、Maia200、MTIA 等主力平台仍以 48V/54V rack bus、3.3-8kW/8-30kW 高密 PSU、48V hot-swap/eFuse、48V/12V/6V IBC、6V/12V 到 sub-1V Vcore 多相供电为核心。最先变现的是 SiC/GaN PSU 器件、100V hot-swap MOSFET、smart fuse、Vcore 智能功率级和高密 power module。

2. **800V HVDC 在 2026 是“设计定点与样机验证”，2027 才是第一轮收入拐点。** NVIDIA 明确推动从现有 AC/54V 架构逐步转向 800VDC，并称未来 AI 服务器功率会超过 54VDC 架构能力；GE Vernova/NVIDIA 白皮书把 2027 Kyber/1MW 机架作为 800VDC 大规模部署节点，MV SST 到 5MW+、24.5-34.5kV 直连 800VDC 的产品化更偏 2028。2026 年 TI、ST、Navitas 在 GTC/APEC 展示 800V 到 6V/12V/50V 的样机，把产业从“架构讨论”推到“器件定点”阶段。

3. **AI 数据中心功率半导体收入的独立第三方低口径锚点已经很强。** TechInsights 估算 data center power semiconductor revenue 2026 年约 $5B，并以 24.6% CAGR 增长到 2031 年 $14.3B，单 rack power semiconductor BOM 从 2025 年约 $2,300 增至 2031 年约 $7,600。若把 Vcore 模块、保护器件、UPS/BESS/800V HVDC 半导体和 smart fuse 都纳入，本报告的偏乐观宽口径为：未来 1 年 $12B-$24B，未来 2 年 $35B-$80B；极度超预期情形可到 $100B+ 累计订单池。

4. **最高壁垒/最高毛利环节是“贴近 GPU/ASIC 的最后 1 米和最后 1.5 毫米”。** MPS、Vicor、Empower、Infineon、TI、Renesas/ADI 等的 Vcore controller、smart power stage、power module、vertical/backside power delivery 既受益于 xPU 电流 >1,000A，也受益于客户认证和板级布局锁定，毛利可维持 50%-65%，极度紧缺时可更高。

5. **保护器件从低价值“保险丝”升级为高价值“AI 资产保护系统”。** 48V live insertion、800V HVDC tray insertion、BESS/UPS、sidecar PSU、固态断路器都需要 hot-swap controller、enhanced SOA MOSFET、smart fuse、TVS/MOV/thyristor clamp、DC fuse/SSCB。Nexperia 在 APEC 2026 专门讲 AI data center hotswap MOSFET，Littelfuse 投资者材料明确称 HVDC 数据中心带来 2-4x content upside。

6. **2026 投资排序：Vcore/电源模块 > 48V 保护/热插拔 > WBG PSU > 传统保护器件 > 800V 样机链。2027 投资排序：800V PDB/SSCB > VPD/in-package power > SiC/GaN SST/sidecar > 高压保护。** 800V 并不取代 48V，而是在 2027-2028 逐步把价值从 PSU/power shelf 向 sidecar、PDB、SSCB、SST、直流母线保护和高压隔离迁移。

## 1. AI 计算中心建设带来的机会、挑战与技术路线

### 1.1 上游需求口径

本项目已有两份上游材料：[全球 AI 芯片路线图与 2026-2027 产能释放预测](../ai_chip_research_2026_2027.md) 和 [AI 数据中心建设规模与产业链订单映射](../AI数据中心建设规模与产业链订单映射_2026-2027_美国.md)。本报告沿用其中的核心假设：

| 上游变量 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 全球 AI 计算芯片/模块产能释放金额 | $300B-$360B | $390B-$470B | $520B-$650B |
| 2027 全球 AI 计算芯片/模块产能释放金额 | $430B-$520B | $590B-$720B | $850B-$1,050B |
| 2026 美国 AI 数据中心建设规模 | $400B-$490B | $540B-$650B | 可上探 $700B+ |
| 2027 美国 AI 数据中心建设规模 | $520B-$650B | $760B-$950B | 可上探 $1T+ |
| 关键推力 | GB300/B300、GB200、Trainium2、Ironwood、MI350 | Rubin、Trainium3、MI400、MTIA/OpenAI ASIC 前置 | 800V/1MW rack、HBM4、ASIC 与 GPU 同时放量 |

### 1.2 2026-2027 出货最大的 AI 芯片平台如何决定电源树

| 平台 | 2026-2027 出货地位 | 供电/保护技术含义 | 对本行业的拉动 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 最主力高端平台 | 54V rack bus、液冷整柜、48V hot-swap、超高电流 Vcore；800V sidecar 在 2026 H2 进入设计验证 | 8-30kW PSU、SiC/GaN PFC/LLC、100V MOSFET、smart fuse、Vcore module 最大受益 |
| AWS Trainium2 | Rainier/Anthropic 百万颗级潜在需求 | AWS 自研机架，48V/54V 与高密 PSU 为主，强调整体 TCO | 服务器 PSU、IBC、Vcore、BESS/UPS 保护器件受益 |
| Google TPU v7 Ironwood | Google Cloud/Anthropic 大规模 TPU 池 | hyperscaler 自有电源架构，推理优化；可能更早采用自定义 power module | 高效率 PSU、Vcore 模块、热插拔与电源遥测 |
| NVIDIA B200/GB200 | 2026 存量和延续订单 | Blackwell 第一代 rack-scale，液冷和 48V 保护已成为标配 | 3.3-8kW PSU、48V eFuse、低压 MOSFET、TVS |
| Huawei Ascend 910C/950 | 中国国产替代主线 | 国产 48V/液冷/超节点；高端 SiC/GaN/VR 受国产供应链约束 | 中国 MOSFET、IGBT/SiC、保护器件、国产 PMIC 放量 |
| Cambricon MLU 590/690 | 中国 OAM/集群需求 | OAM 卡 + 48V/12V/低压多相，热插拔要求上升 | 国产 100V MOSFET、hot-swap、Vcore 控制器 |
| AMD MI350 | 2026 AMD 最确定量产 | PCIe/UBB 多形态，企业部署门槛低于 rack-scale | 12V/48V 兼容电源树、Vcore module、PSU 器件 |
| AWS Trainium3 | 2026 GA/2027 主力 | 144 芯片 UltraServer，rack power density 显著提高 | 48V 高电流、PSU、hot-swap、早期 HVDC 试点 |
| Meta MTIA 300/400/450/500 | Meta 自研 ASIC 连续迭代 | OCP 48V、推理负载、Broadcom XPU/网络生态 | 低压高流 Vcore、smart fuse、板级电源模块 |
| Microsoft Maia 200 | Azure 推理芯片，750W SoC | 3nm、216GB HBM3E、闭环液冷；强调推理 TCO | Vcore、液冷 CDU 电源、隔离/监测/保护 |
| Alibaba Zhenwu 810E/PPU | 中国云推理/训练 | 国产云端 48V、低压 VR、国产保护器件 | 中国功率 MOSFET、PMIC、TVS/fuse |
| AMD MI400/MI455X Helios | 2026 H2 首批，2027 放量 | 72 GPU rack、HBM4、极高电流和热负荷；800V/VPD 候选 | 2027 800V PDB、VPD、SiC/GaN、高压保护的核心增量 |

### 1.3 当前正在使用的技术

| 层级 | 2026 主流技术 | 典型器件 | 代表公司 |
|---|---|---|---|
| 设施/电网到电源室 | 480VAC/400VAC、UPS、BESS、柴油/燃气备电、PFC 整流 | IGBT、SiC MOSFET、SiC/IGBT 模块、整流桥、TVS/MOV/fuse | Infineon、onsemi、ST、Mitsubishi、Fuji、Semikron Danfoss、Littelfuse、Mersen |
| 服务器 PSU/power shelf | 3.3kW/5.5kW/8kW，向 18-30kW sidecar 过渡；totem-pole PFC、Vienna PFC、LLC | 650/750V SiC、650/700V GaN、superjunction Si、gate driver、MCU | Infineon、TI、onsemi、ST、Navitas、Renesas/Transphorm、Power Integrations、ROHM |
| Rack bus | 48V/54V Open Rack v3 类架构 | hot-swap MOSFET、eFuse、ORing、current sense、TVS | TI、Infineon、onsemi、Nexperia、ADI、MPS、AOS、Littelfuse |
| IBC | 48V 到 12V/6V/4.8V，fixed-ratio converter、LLC、hybrid switched-cap | 100V/150V GaN、low-Rds(on) MOSFET、module、magnetics | MPS、Vicor、Infineon、TI、Renesas、Murata、Delta、Flex Power |
| GPU/ASIC Vcore | 12V/6V 到 sub-1V，多相 buck、smart power stage、integrated power module、TLVR/VPD | DrMOS/SPS、controller、power module、silicon capacitor | MPS、Infineon、Renesas、TI、ADI、Vicor、Empower、Alpha & Omega、onsemi |
| 高压保护 | 48V hot-swap、400/800V HVDC hot-swap、DC fuse、MOV/TVS/GDT、SSCB | enhanced SOA MOSFET、SiC MOSFET/JFET、thyristor、MOV、fuse | Littelfuse、Nexperia、ST、TI、Infineon、onsemi、Eaton、Mersen、Bourns、Vishay |

### 1.4 2026-2028 新技术成熟与放量时间

| 技术 | 2026 状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观成熟/放量 | 关键判断 |
|---|---|---|---|---|---|
| 48V/54V rack + smart hot-swap/eFuse | 已量产，AI 服务器强绑定 | 2026 全年高增 | 2026 H2 供不应求 | 2026 Q2-Q4 价格/份额双升 | 2026 最确定路径 |
| 650/750V SiC Gen2 PSU | Infineon/onsemi/ST 等量产，8-30kW PSU 导入 | 2026 H2 放量 | 2026 Q2 起加速 | 2026 年成为 AI PSU 默认高端方案 | EV SiC 过剩不等于 AI PSU 过剩，高性能封装仍紧 |
| 650/700V GaN PSU/PDB | TI/ST/Navitas/Power Integrations 等持续推出 | 2026 设计定点，2027 放量 | 2026 H2 进入高端 PSU/PDB | 2026 H2 大客户直接锁定 800V PDB | 可靠性和散热验证决定速度 |
| Vcore smart power stage / power module | MPS/Vicor/Infineon 等已经放量 | 2026-2027 连续放量 | 2026 H2 随 GB300/ASIC 急升 | 2026 形成明显紧缺和溢价 | 最贴近 xPU，价值捕获强 |
| Vertical/backside power delivery | Vicor/Empower/Infineon 等技术验证和客户导入 | 2027 初步放量 | 2026 H2 小规模高端 xPU | 2027 成为 HBM4/Rubin/MI400 标配 | 电流 >1,000A 后 PCB 横向供电损耗不可忽略 |
| 800V 到 50V/54V PDB | ST 12kW 800V-to-50V 已满功率测试，Navitas/TI 展示样机 | 2027 H1 小批量，2027 H2 放量 | 2026 H2 进入 GB300/Rubin pilot | 2026 H2 形成 sidecar 标准件订单 | 从 800V 保留 50V 中间母线最容易先量产 |
| 800V 到 12V/6V 直降 | TI 800V-to-6V、ST/Navitas 800V-to-6V/12V 展示 | 2027 H2 早期量产 | 2027 H1 放量 | 2026 H2 少数客户预量产 | 省掉 48/54V stage，但认证、EMI、保护难度高 |
| 800V hot-swap/SSCB | TI/NVIDIA 架构、ST SSCB、Nexperia hot-swap 讨论升温 | 2027 H2 放量 | 2027 H1 放量 | 2026 H2 随 800V tray pilot 出货 | 800V live insertion 没有成熟保护就无法规模运维 |
| MV SST 10kV/24-34kV 到 800V | Navitas/EPFL 250kW APEC demo，GE 指向 5MW+ | 2028 产品化 | 2027 H2 试点 | 2027 少数 AI gigafactory 先导 | 真正改变 grid-to-rack，但认证和工程周期长 |
| 固态断路器/eMOV/thyristor clamp | ST、Littelfuse、Eaton 等布局 | 2027-2028 放量 | 2027 放量 | 2026 H2 被 800V 标准拉动 | DC 无自然过零，保护协调是刚需 |

### 1.5 2026 最可能技术路径

2026 最可能兑现收入的技术路径按确定性排序：

1. **54V rack + 48V hot-swap/eFuse + Vcore smart power stage。** 对 GB300、GB200、MI350、TPU、Trainium、ASIC 都适用，和具体 GPU/ASIC 胜负无关。
2. **高端 PSU 的 SiC/GaN 混合化。** Infineon 8kW AI PSU 方案和 650/750V CoolSiC、onsemi EliteSiC/CJFET、ST/Navitas/TI GaN 都在推动 500kHz-1MHz、高功率密度 PSU。
3. **48V 到 6V/4.8V 中间母线 + 6V 到 core。** MPS 已明确 4V-6V 架构、130A/170A Intelli-Module；TI 也把 6V 到 sub-1V 作为 800V 路径中的关键后级。
4. **800V sidecar pilot。** 2026 是 GTC/APEC 样机、客户验证和安全标准定点；大规模收入更偏 2027。
5. **保护器件升级。** enhanced SOA MOSFET、smart fuse、TVS/MOV/fuse 从低价值被动件变为系统 uptime 和昂贵 xPU 保护的必需件。

## 2. 已经开始放量的关键产品、市场规模、渗透率和利润率

### 2.1 已放量产品市场规模总览

以下规模为从 2026-05-08 起滚动期间内的收入/订单池，包含芯片、模块和高压保护器件；不同产品之间可能存在少量系统级重复计算，但已尽量扣除整机 PSU/OEM 加价。

| 已放量产品 | 当前阶段 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 毛利率/溢价能力 |
|---|---|---:|---:|---:|---|---|
| 650/750V SiC + 650/700V GaN + superjunction Si：AI server PSU/PFC/LLC 器件 | 3.3-8kW 量产，8-30kW 高端 PSU 导入 | 基准 $0.45B-$0.65B；乐观 $0.65B-$0.90B；极度 $0.90B-$1.25B | 基准 $2.2B-$3.2B；乐观 $3.2B-$4.8B；极度 $5.0B-$7.0B | 基准 $6B-$9B；乐观 $9B-$14B；极度 $15B-$22B | AI PSU WBG attach 2026 年 30%-45%，2027 年 45%-65%，2028 年 60%-80% | 基准 38%-48%；乐观 45%-55%；极度 50%-60%。AI-qualified 封装和低损耗器件可定价，普通 SiC 受 EV 过剩压价 |
| 48V/54V hot-swap、eFuse、ORing、enhanced SOA MOSFET、smart fuse | 已经随 AI tray/电源架放量 | 基准 $0.20B-$0.35B；乐观 $0.35B-$0.55B；极度 $0.60B-$0.90B | 基准 $1.0B-$1.8B；乐观 $1.8B-$3.0B；极度 $3.0B-$4.8B | 基准 $3B-$5.5B；乐观 $5.5B-$9B；极度 $10B-$16B | 高端 AI tray 热插拔保护接近 100%；smart telemetry/eFuse attach 2026 年 30%-50%，2027 年 50%-75% | 基准 40%-55%；乐观 50%-60%；极度 55%-65%。客户不愿因几美元器件损坏数万美元加速器 |
| Vcore 多相控制器、DrMOS/SPS、智能功率级、低压 MOSFET、电源模块 | 已是 AI xPU 标配，MPS/Vicor 等收入快速增长 | 基准 $0.90B-$1.50B；乐观 $1.50B-$2.30B；极度 $2.40B-$3.50B | 基准 $4.5B-$7.5B；乐观 $7.5B-$12B；极度 $12B-$18B | 基准 $12B-$22B；乐观 $22B-$36B；极度 $36B-$55B | 高端 GPU/ASIC advanced VR attach 70%-90%；VPD/backside module 2026 年 5%-15%，2027 年 15%-35%，2028 年 30%-55% | 基准 50%-60%；乐观 55%-65%；极度 60%-70%。封装、控制算法、客户板级锁定带来高 ROIC |
| 48V 到 12V/6V/4.8V IBC、fixed-ratio converter、bus converter 模块 | 48V 数据中心主流，6V 架构开始导入 | 基准 $0.35B-$0.70B；乐观 $0.70B-$1.00B；极度 $1.10B-$1.60B | 基准 $1.6B-$3.2B；乐观 $3.2B-$5.0B；极度 $5.0B-$7.5B | 基准 $5B-$9B；乐观 $9B-$15B；极度 $15B-$24B | 48V rack attach 在高端 AI 机架接近 100%；6V/4.8V 后级 2026 年 10%-25%，2027 年 25%-45% | 基准 42%-55%；乐观 50%-60%；极度 55%-65%。模块化、认证和热设计抬高壁垒 |
| TVS、MOV、GDT、thyristor、DC fuse、PPTC、ESD array 等传统与高端保护器件 | 数据中心、UPS、BESS、通信端口已大量使用 | 基准 $0.20B-$0.40B；乐观 $0.40B-$0.65B；极度 $0.70B-$1.10B | 基准 $0.9B-$1.7B；乐观 $1.7B-$3.0B；极度 $3.0B-$5.0B | 基准 $2.5B-$5B；乐观 $5B-$9B；极度 $9B-$15B | 传统保护几乎全覆盖；高压 DC 专用保护 2026 年 <10%，2027 年 10%-25% | 基准 30%-45%；乐观 35%-50%；极度 45%-55%。普通 TVS/fuse 商品化，高压认证件和定制保护有溢价 |
| UPS/BESS/整流器/逆变器用 IGBT、SiC 模块、二极管与隔离驱动 | 数据中心电力系统先行锁单 | 基准 $0.35B-$0.80B；乐观 $0.80B-$1.30B；极度 $1.30B-$2.20B | 基准 $1.8B-$3.8B；乐观 $3.8B-$6.5B；极度 $6.5B-$10B | 基准 $5.5B-$12B；乐观 $12B-$22B；极度 $22B-$36B | BESS/UPS 功率半导体随 AI 园区电力订单增长；SiC 在高频高效率系统中从个位数向 20%-40% 走 | 基准 32%-45%；乐观 40%-52%；极度 45%-60%。系统认证和功率等级越高越能定价 |

### 2.2 已放量产品的增长预测区间

| 产品 | 基准增长 | 乐观增长 | 极度超预期乐观增长 | 主要驱动 |
|---|---:|---:|---:|---|
| PSU WBG 器件 | 2026-2028 CAGR 35%-45% | 45%-60% | 65%-85% | GB300/MI350/Trainium3 推动 PSU 功率密度，SiC/GaN 从效率优化变为交付门槛 |
| 48V hot-swap/eFuse | 40%-55% | 60%-80% | 90%+ | AI tray 价值上升，live insertion 保护从可选变必选 |
| Vcore VR/module | 45%-65% | 70%-90% | 100%+ | xPU 电流、HBM、电源完整性和板面积共同推高价值量 |
| IBC/bus converter | 35%-55% | 55%-75% | 80%-100% | 48V 到 6V/4.8V 架构渗透，模块化提高 ASP |
| TVS/MOV/fuse/protection | 20%-35% | 35%-55% | 60%-80% | HVDC 和 BESS 把传统保护带入更高电压/更高认证价值 |
| UPS/BESS power devices | 35%-55% | 60%-85% | 90%+ | 数据中心先锁电、BESS/UPS/微电网订单领先 GPU |

## 3. 在研关键产品、未来快速增长方向与利润率预测

### 3.1 在研/导入期关键产品

| 在研产品/技术 | 2026 公开进展 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 毛利率/溢价能力 |
|---|---|---:|---:|---:|---|---|
| 800V 到 50V/54V PDB | ST 12kW 800V-to-50V 原型满功率测试，Navitas/TI 参与 NVIDIA 800V reference ecosystem | 基准 $30M-$80M；乐观 $80M-$200M；极度 $200M-$500M | 基准 $0.3B-$0.8B；乐观 $0.8B-$2.0B；极度 $2.0B-$4.5B | 基准 $2B-$5B；乐观 $5B-$10B；极度 $12B-$25B | 800V AI rack 2026 <2%，2027 5%-20%，2028 15%-45% | 基准 45%-55%；乐观 50%-65%；极度 60%-70%。早期定制件 ASP 高 |
| 800V 到 12V/6V 直降 DC/DC | TI 800V-to-6V 97.6% peak、>2000W/in3；Navitas 20kW 800V-to-6V、97.5% target；ST 6kW/20kW boards | 基准 $20M-$70M；乐观 $70M-$180M；极度 $200M-$600M | 基准 $0.25B-$0.7B；乐观 $0.7B-$1.8B；极度 $2.0B-$5.0B | 基准 $1.5B-$4B；乐观 $4B-$9B；极度 $10B-$22B | 2026 样机/小批，2027 早期量产，2028 可能成为高端 rack 重要路径 | 基准 48%-60%；乐观 55%-68%；极度 65%-75%。省掉中间 stage 的系统价值极高 |
| 800V hot-swap controller、HV ORing、SSCB | TI 提出 800V hot-swap input protection；ST SSCB/eMOV；Nexperia 强调 AI hotswap MOSFET SOA | 基准 $10M-$50M；乐观 $50M-$120M；极度 $150M-$350M | 基准 $0.1B-$0.4B；乐观 $0.4B-$1.0B；极度 $1.0B-$2.5B | 基准 $0.8B-$2.0B；乐观 $2B-$5B；极度 $5B-$12B | 800V rack 无保护不能规模运维；2027 attach 随 800V tray 同步 | 基准 45%-60%；乐观 55%-70%；极度 65%-75%。认证和安全责任带来高定价 |
| MV SST：10kV/24-34kV 到 800V/1500V | Navitas/EPFL 250kW demo，GE Vernova 白皮书指向 5MW+、2028 产品化 | 基准 $0-$30M；乐观 $30M-$80M；极度 $100M-$250M | 基准 $0.1B-$0.5B；乐观 $0.5B-$1.2B；极度 $1.2B-$3B | 基准 $0.5B-$3B；乐观 $3B-$8B；极度 $8B-$18B | 2026 demo，2027 pilot，2028 first scale | 基准 40%-55%；乐观 50%-65%；极度 60%-75%。系统级价值高但工程周期长 |
| Vertical/backside/in-package power delivery | Vicor 2nd Gen VPD、Empower Crescendo HD 5A/mm2、Infineon BVM 路线 | 基准 $50M-$150M；乐观 $150M-$350M；极度 $350M-$800M | 基准 $0.4B-$1.2B；乐观 $1.2B-$3.0B；极度 $3B-$6B | 基准 $1.5B-$5B；乐观 $5B-$12B；极度 $12B-$25B | >1,000A xPU 2026 5%-15%，2027 15%-35%，2028 30%-55% | 基准 55%-65%；乐观 60%-72%；极度 70%+。IP/封装/客户协同壁垒极高 |
| 双向 GaN、三电平/Vienna PFC、stacked LLC | TI 白皮书称 bidirectional GaN 可替代多颗背靠背 MOSFET，但仍需市场验证 | 基准 $20M-$80M；乐观 $80M-$200M；极度 $200M-$500M | 基准 $0.2B-$0.7B；乐观 $0.7B-$1.5B；极度 $1.5B-$3.5B | 基准 $1B-$3B；乐观 $3B-$7B；极度 $7B-$15B | 2026 参考设计，2027 高端 PSU/PDB，2028 中高端普及 | 基准 45%-58%；乐观 55%-65%；极度 65%-75% |
| 高压 DC 专用 TVS/MOV/thyristor/eMOV/fuse 协同保护 | Littelfuse、ST、Eaton、Mersen 等布局；DC 无自然过零增加保护难度 | 基准 $10M-$40M；乐观 $40M-$100M；极度 $100M-$250M | 基准 $0.1B-$0.4B；乐观 $0.4B-$1.0B；极度 $1.0B-$2.2B | 基准 $0.6B-$2.5B；乐观 $2.5B-$6B；极度 $6B-$12B | 2026 BESS/UPS 优先，2027 跟随 800V rack，2028 进入标准化 | 基准 35%-50%；乐观 45%-60%；极度 55%-70% |
| AI workload-aware power smoothing、rack/server-level energy buffer | GE/NVIDIA 指出 AI 训练负载每秒多次大幅摆动，需要 batteries/supercapacitors 过滤 | 基准 $20M-$80M；乐观 $80M-$250M；极度 $250M-$700M | 基准 $0.2B-$0.8B；乐观 $0.8B-$2.0B；极度 $2.0B-$5.0B | 基准 $1B-$4B；乐观 $4B-$10B；极度 $10B-$20B | 设施级 BESS 已放量，rack/server 级更偏 2027-2028 | 半导体/保护件 35%-55%；控制系统和模块可 50%+ |

### 3.2 为什么这些在研产品会快速增长

1. **电流已成为性能瓶颈。** Vicor 公开测算显示，把部分 PoL 从横向搬到处理器下方可把 PDN 阻抗从 60μΩ 降至 11μΩ，1000A 时 PCB 损耗从 60W 降到 11W；单 rack 64 个 accelerator module 可省约 3.2kW 连续损耗。这个数字对 hyperscaler 很敏感，因为省下来的电力可以直接转化为 token。

2. **800V 是铜、空间和转换级数问题的系统解。** TI 指出 1MW rack 如果用 48V 配电，为控制损耗会需要约 450lb 铜；NVIDIA/GE Vernova 的核心逻辑也是提高电压、减少 conversion stages、把 800VDC 直接送到 rack。

3. **保护器件必须先于 800V 放量成熟。** 800VDC live insertion、DC arc、短路无过零、creepage/clearance、隔离通信、热插拔偏置电源，都会把 hot-swap controller、SSCB、TVS/MOV/fuse 的规格从“低压服务器件”提升到“高压安全系统”。

4. **客户愿意为确定性交付付溢价。** 高端 xPU rack 的价值远高于单颗保护器件成本；一个失效导致 rack downtime 或损坏 GPU/ASIC，经济损失远大于器件 ASP。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/封装特征 |
|---|---|---|---|
| Si power MOSFET / superjunction | 美国、欧洲、日本、台湾、中国、马来西亚、菲律宾 | Infineon、onsemi、ST、Vishay、Nexperia、AOS、Toshiba、ROHM、Diodes、Silan、CR Micro | 8-inch/12-inch power CMOS、superjunction、PowerTrench/OptiMOS、TOLL/TOLT/LFPAK/QDPAK/PowerFLAT |
| SiC substrate/epi/device | 美国、奥地利/德国/意大利、马来西亚、日本、中国 | Wolfspeed、Infineon、ST、onsemi、ROHM、Mitsubishi、Fuji、Sanan、SICC、TankeBlue、StarPower、CRRC Times | 6-inch 向 8-inch 过渡，650V/750V/1200V/1700V/3300V，银烧结/铜夹/top-side cooling |
| GaN-on-Si / GaN power IC | 美国、欧洲、中国、台湾、日本 | TI、Infineon/GaN Systems、Navitas、Power Integrations、Renesas/Transphorm、EPC、Innoscience、ST、ROHM、Nexperia | 650/700V lateral GaN、100/150V mid-voltage GaN、integrated driver/protection、QFN/TOLL/custom modules |
| Vcore controller/SPS/module | 美国、台湾、中国、马来西亚、菲律宾 | MPS、Infineon、Renesas、TI、ADI/Maxim、Vicor、Empower、onsemi、AOS、Vishay、Murata、TDK | BCD/DMOS、multi-phase controller、DrMOS/SPS、integrated inductor module、silicon capacitor、vertical/backside module |
| 保护器件 | 美国、墨西哥、欧洲、中国、日本、台湾、东南亚 | Littelfuse、Eaton Bussmann、Mersen、Vishay、Bourns、TDK/EPCOS、Yageo/KEMET、Nexperia、ST、Diodes、Semtech、ProTek、Wayon、BrightKing | TVS/MOV/GDT/PPTC/fuse/thyristor/SSCB，认证和材料体系决定可靠性 |
| 模块和系统封装 | 马来西亚、菲律宾、中国、台湾、美国、欧洲、日本 | Infineon、ST、onsemi、Mitsubishi、Fuji、Semikron Danfoss、ASE、Amkor、Vicor、MPS、Delta、Flex | 功率模块、铜基板、DBC/AMB、液冷冷板适配、隔离驱动、系统级 burn-in |

### 4.2 供给瓶颈

1. **SiC substrate/epi 和高压良率。** AI 数据中心需要的是低损耗、高可靠、热循环强的 650/750/1200/3300V 器件，不完全等同于 EV 市场的商品化 SiC。8-inch SiC 良率、微管缺陷、epi 均匀性仍影响成本。

2. **GaN 可靠性与动态 Rds(on)。** 800V/高频/高功率密度场景要求 p-GaN gate、dynamic switching、短路鲁棒性、封装寄生、EMI 全部过关。APEC 2026 仍有大量 GaN reliability 议题，说明还处于工程加速期。

3. **先进功率封装。** Top-side cooling、copper clip、银烧结、低寄生封装、薄型 power module、垂直供电模块都需要专用封装和热仿真能力。封装比裸 die 更能决定 AI 客户是否采用。

4. **800VDC 安规和认证。** DC 无自然过零，arc fault、creepage/clearance、绝缘、隔离通信、hot swap 偏置电源、维护流程都要重新定义。UL/IEC/OCP/NVIDIA reference design 的收敛速度决定 2027 放量斜率。

5. **客户认证和设计锁定周期。** Hyperscaler、ODM、GPU/ASIC 厂商对电源树认证一般需要 6-18 个月；一旦定点，切换成本高，但新进入者难以快速替换。

6. **隔离驱动、传感、数字控制 IC。** 800V 架构需要 isolated gate driver、isolated current/voltage sense、isolated power module、MCU/DSP。缺一个小 IC 就会卡住整板验证。

7. **高压保护协同测试能力。** fuse、TVS/MOV、SSCB、hot-swap MOSFET 的 I2t、clamping、SOA、热失控和系统级短路测试需要专门实验室，很多传统低压供应商不具备。

8. **功率电子人才。** 高频 GaN/SiC、数字控制、磁件设计、EMI、热管理、安规认证的复合人才短缺，比晶圆产能更难短期复制。

### 4.3 成本结构和毛利决定因素

| 产品 | 典型成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 8kW AI PSU power stage | power switches 25%-35%，磁件 15%-25%，电容 10%-15%，控制/驱动/传感 8%-12%，PCB/连接器/热件 10%-15%，组装测试 10%-15% | SiC/GaN die 成本、封装热阻、效率、客户认证、良率 | 电价节省和 rack density 提升可量化，PSU OEM 愿为 0.5%-1% 效率改善付费 |
| 800V PDB | GaN/SiC switches 30%-45%，磁件/变压器 20%-30%，隔离驱动/传感/MCU 10%-15%，热/封装 10%-15%，保护器件 5%-10% | 单级转换效率、功率密度、EMI、热插拔安全、NVIDIA/ODM design-in | 初期按定制板/模块定价，规模化后向器件 BOM 压降 |
| Vcore power module | MOSFET/driver/controller 35%-45%，电感/磁件 20%-30%，封装/基板/热件 15%-25%，电容 10%-20%，测试 5%-10% | 电流密度、瞬态响应、power integrity、厚度、散热和 IP | 一旦 GPU/ASIC 板级 layout 锁定，换供应商需重做电源完整性验证 |
| hot-swap/eFuse | MOSFET die 25%-40%，controller/driver/sense 20%-35%，封装/散热 15%-25%，测试 10%-15% | SOA、短路能量、PMBus telemetry、封装热阻 | 保护昂贵加速器，客户对可靠件价格不敏感 |
| TVS/MOV/fuse/thyristor | 陶瓷/金属/硅片/银铜材料 35%-50%，封装 20%-30%，测试认证 5%-15%，制造开销 10%-20% | 电压/电流等级、认证、失效率、客户定制 | 普通件随周期波动；高压 DC 认证件和 BESS/数据中心定制件可加价 |

### 4.4 毛利率区间

| 环节 | 当前基准毛利 | 乐观毛利 | 极度超预期毛利 | 说明 |
|---|---:|---:|---:|---|
| Commodity Si MOSFET/TVS/fuse | 25%-40% | 35%-45% | 40%-50% | 价格竞争较强，但认证件改善 |
| AI PSU SiC/GaN high-performance devices | 38%-50% | 45%-58% | 55%-65% | WBG 性能和封装定价，高端客户锁单 |
| Vcore controller/SPS/module | 50%-60% | 55%-68% | 65%-75% | MPS/Vicor 类业务毛利已验证高位 |
| hot-swap/eFuse/smart fuse | 40%-55% | 50%-65% | 60%-70% | 系统保护价值远高于 BOM 成本 |
| 800V PDB/SSCB/SST 样机链 | 45%-60% | 55%-70% | 65%-75% | 早期 custom + 高安规，若规模化后会回落 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 子领域 | 市场结构估算 | 头部集中度 | 定价权判断 |
|---|---|---:|---|
| 宽口径功率半导体 | Infineon、onsemi、ST、TI、Vishay、Renesas、ROHM、Mitsubishi、Toshiba 等分散竞争 | Top 5 约 40%-50% | 中等，汽车/工业周期会影响价格 |
| AI PSU WBG 器件 | Infineon、onsemi、ST、TI、Navitas、Renesas/Transphorm、ROHM、Power Integrations、Innoscience | Top 6 约 55%-70% | 高端 AI-qualified 器件定价权较强 |
| Vcore/SPS/power module | MPS、Infineon、Renesas、TI、ADI、Vicor、Empower、onsemi、AOS | Top 5 约 60%-75% | 强，客户认证和 board layout 锁定 |
| 48V hot-swap/eFuse | TI、ADI、Infineon、onsemi、MPS、Nexperia、AOS、Littelfuse | Top 6 约 55%-70% | 强，SOA/可靠性/保护算法壁垒 |
| TVS/MOV/fuse/GDT | Littelfuse、Vishay、Bourns、TDK、Yageo、Mersen、Eaton、Nexperia、Diodes | Top 6 约 45%-60% | 普通件中等，高压 DC 认证件强 |
| SiC 模块/UPS/BESS | Infineon、Mitsubishi、Fuji、Semikron Danfoss、onsemi、ST、Wolfspeed、StarPower、CRRC Times | Top 8 约 60%-75% | 中高，受项目认证和交期影响 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 为什么形成定价权 |
|---|---|
| 器件物理和可靠性 | GaN gate reliability、SiC short-circuit ruggedness、dynamic Rds(on)、SOA 都直接影响失效率；客户愿意为低失效率买单 |
| 封装和热管理 | AI 电源器件不是裸 die 竞争，top-side cooling、copper clip、低寄生、低热阻和液冷适配决定能否进高端 rack |
| 控制算法和系统参考设计 | TI/ST/Navitas/Infineon 不只卖器件，还提供 800V-to-6V、8kW PSU、30kW PSU、hot-swap reference design，缩短客户开发周期 |
| 客户认证/渠道锁定 | 进入 NVIDIA reference ecosystem、OCP、hyperscaler approved vendor list 后，替换需要重新做电源完整性、EMI、热和安规测试 |
| 安规认证 | 800VDC、BESS、UPS、SSCB 的 UL/IEC 认证和系统短路测试成本高，认证件可长期维持 premium |
| 规模和供货能力 | AI 客户要的是百万颗级器件和多年供货；小厂即使性能好，也需要第二来源、OSAT 和质量体系 |
| IP/专利 | Vicor VPD/current multiplier、Empower VPD、MPS module、Infineon/TI GaN/driver 等均有专利和 know-how，直接限制可替代性 |
| 现场失效责任 | 保护器件失效会损坏高价值 GPU/ASIC 或导致 downtime，客户更重视 track record 而非最低价 |

### 5.3 价值链里最可能长期高 ROIC 的层

1. **Vcore controller/SPS/power module/VPD。** 最贴近 GPU/ASIC，随每代 xPU 电流和封装面积变化同步升级；客户切换成本最高；毛利和 ROIC 最优。

2. **800V hot-swap/SSCB/保护控制。** 800V 放量后，安全保护从配套件变为架构许可条件；控制 IC + power device + protection coordination 的组合最有长期定价权。

3. **高端 GaN/SiC reference design 供应商。** 能同时提供器件、驱动、隔离、控制和热设计的公司比单卖 MOSFET 的公司更能捕获系统价值。

4. **高压 DC fuse/MOV/TVS/thyristor 认证件。** 普通保护器件 ROIC 中等，但高压 DC、BESS、AI rack 认证件的定制化和安全责任提高长期利润率。

5. **纯商品 SiC/Si MOSFET。** 需求大，但中国 SiC/Si MOSFET 产能扩张会压制长期 ROIC，除非公司拥有封装、客户认证或系统方案优势。

## 6. 2026 关键变化：行业拐点与最可能放量的子方向

### 拐点 1：48V/54V AI 电源树进入确定性放量

GB300/B300、GB200、MI350、Trainium2、Ironwood、Maia200、MTIA 等都需要更高 rack power density。2026 年 revenue 最容易兑现的是：

| 子方向 | 受益产品 | 受益公司 |
|---|---|---|
| AI PSU WBG | 650/750V SiC、650/700V GaN、gate driver、digital controller | Infineon、onsemi、ST、TI、Navitas、Renesas、Power Integrations、ROHM |
| 48V hot-swap/eFuse | 100V enhanced SOA MOSFET、smart fuse、hot-swap controller | TI、ADI、Infineon、onsemi、Nexperia、MPS、AOS |
| Vcore power | SPS、DrMOS、controller、power module、silicon capacitor | MPS、Vicor、Empower、Infineon、Renesas、TI、ADI、onsemi |

### 拐点 2：APEC/GTC 2026 把 800V 从概念推入 design-in

TI 在 2026-03-16 发布与 NVIDIA 的 800VDC 架构，包含 800V hot-swap、800V-to-6V DC/DC、6V-to-<1V multiphase buck；ST 在 APEC 2026 展示 800V 到 12V/6V/50V 的 PDB；Navitas 展示 20kW 800V-to-6V 和 250kW SST。2026 的关键不是规模收入，而是：

| 观察点 | 为什么重要 |
|---|---|
| NVIDIA/ODM reference design 是否固定 800V-to-50V 还是 800V-to-6V | 决定中间母线是否保留，影响 IBC 与 Vcore 价值分配 |
| 800V hot-swap/SSCB 标准 | 决定 tray 是否能现场维护 |
| GTC/APEC 样机是否进入 hyperscaler pilot | 决定 2027 上量的供应商名单 |

### 拐点 3：SiC 从 EV 周期切换到 AI 电源高性能市场

TechInsights 明确提示 2026 年 SiC 面临中国 EV 市场过剩和价格压力，但 AI data centers 又在推动高效率、高密度 PSU 对 SiC/GaN 的需求。投资上要区分：

| 类型 | 投资含义 |
|---|---|
| 普通车规/工业 SiC | 可能继续价格竞争 |
| AI PSU 650/750V SiC Gen2、top-side cooled package | 受益于 8-30kW PSU，高毛利概率更高 |
| 1200/3300V SiC module for SST/UPS/BESS | 2027-2028 更大，2026 以 design-in 为主 |

## 7. 2027 关键变化：行业拐点与最可能放量的子方向

### 拐点 1：Rubin/Kyber/MI400 把 800V HVDC 推向第一轮量产

GE Vernova/NVIDIA 白皮书把 2027 Kyber rack-scale systems 与 1MW rack 作为 800VDC 规模部署节点。若 Rubin/MI400/HBM4 放量顺利，2027 年最可能出现：

| 子方向 | 2027 放量逻辑 |
|---|---|
| 800V PDB | 从 sidecar/IT tray 样机进入小批量订单 |
| 800V hot-swap/SSCB | 保护和维护成为硬门槛 |
| 800V high-voltage sensing/isolation | 所有控制、通信和风扇/辅助电源都需隔离 |
| 高压 DC protection | TVS/MOV/fuse/thyristor/eMOV 从 BESS 进入 rack/sidecar |

### 拐点 2：VPD/backside power 成为 HBM4 时代 xPU 的电源完整性解法

Rubin、MI400、TPU8、OpenAI/Broadcom ASIC、Meta MTIA 后续版本会把功耗、电流和封装面积继续推高。2027 年 VPD 的关键是从“先进客户定制”走向“平台化模块”。

| 观察点 | 受益公司 |
|---|---|
| 3A/mm2 到 5A/mm2 current density | Vicor、Empower、Infineon、MPS |
| silicon capacitor / embedded capacitor | Empower、Murata、TDK、AVX/KEMET、KYOCERA |
| OAM/UBB/MGX 对薄型 power module 的标准化 | MPS、Vicor、Infineon、Renesas、TI |

### 拐点 3：AI 园区电力波动催生 rack/server-level energy buffer

GE Vernova 提到 AI training 的同步计算会导致每秒多次大负载摆动，需要 batteries/supercapacitors 直接接入 DC distribution 进行过滤。2027 年若 AI Factory 进入多 GW 复制，功率半导体机会从服务器内部扩展到：

| 子方向 | 产品 |
|---|---|
| BESS/UPS 快速响应 | SiC/IGBT 模块、bidirectional DC/DC、battery monitor、isolated driver |
| supercapacitor/eSTATCOM | SiC module、IGBT、thyristor、TVS/MOV、控制 MCU |
| workload-aware power management | sensing、isolation、digital power controller、solid-state relay |

## 8. 头部公司和技术优势公司清单

### 8.1 按产品/技术拆分

| 细分 | 头部/优势公司 |
|---|---|
| 宽口径功率半导体 IDM | Infineon、onsemi、STMicroelectronics、Texas Instruments、Renesas、Vishay、Nexperia、ROHM、Toshiba、Mitsubishi Electric、Fuji Electric、Microchip、Diodes、Alpha and Omega Semiconductor |
| SiC substrate/epi | Wolfspeed、Coherent、II-VI/Coherent、SICC 天岳先进、TankeBlue 天科合达、Sanan、Resonac、SK Siltron CSS、Soitec、昭和电工系供应链 |
| SiC MOSFET/JFET/module | Infineon CoolSiC、onsemi EliteSiC/CJFET、ST STPOWER SiC、Wolfspeed、ROHM、Mitsubishi、Fuji、Toshiba、Microchip、Navitas GeneSiC、Qorvo/UnitedSiC 资产、StarPower 斯达半导、CRRC Times 中车时代电气、BASiC 基本半导体、Silan 士兰微、Sanan 三安、BYD Semiconductor |
| GaN power IC/device | TI、Infineon/GaN Systems、Navitas、Power Integrations、Renesas/Transphorm、EPC、Innoscience 英诺赛科、ST、ROHM、Nexperia、GaNPower、Cambridge GaN Devices |
| Server PSU reference/器件 | Infineon、TI、onsemi、ST、Navitas、Renesas、Power Integrations、ROHM、Delta Electronics、Lite-On、AcBel、Flex Power、Advanced Energy、Bel Power、Murata |
| 800V HVDC PDB / direct conversion | TI、STMicroelectronics、Navitas、Infineon、onsemi、Renesas/Transphorm、Power Integrations、EPC、Delta、Flex、Murata、GE Vernova、ABB、Mitsubishi Electric |
| MV SST / grid-to-rack | GE Vernova、ABB、Siemens Energy、Schneider Electric、Eaton、Mitsubishi Electric、Navitas/EPFL、Infineon、onsemi、ST、Hitachi Energy、Wolfspeed |
| Vcore controller/SPS/DrMOS | MPS、Infineon、Renesas、TI、ADI/Maxim、onsemi、Alpha and Omega、Vishay、Monolithic Power Systems、Richtek/MediaTek、uPI、Silergy 矽力杰 |
| Power module/VPD/backside | Vicor、MPS、Empower Semiconductor、Infineon、Renesas、TI、Murata、TDK、Delta、Flex Power、AmberSemi、Analog Devices |
| Silicon/embedded capacitor for AI power | Empower、Murata、TDK、KYOCERA AVX、Yageo/KEMET、Vishay、Samsung Electro-Mechanics、Taiyo Yuden |
| 48V hot-swap/eFuse/smart fuse | TI、ADI/Maxim、Infineon、onsemi、MPS、Nexperia、Alpha and Omega、Littelfuse、Microchip、Diodes |
| Enhanced SOA MOSFET | Nexperia ASFET、Infineon OptiMOS、onsemi PowerTrench T10、Vishay、AOS、Toshiba、ROHM、Diodes |
| TVS/ESD array | Littelfuse、Vishay、Bourns、Nexperia、Diodes、Semtech、ProTek Devices、ST、onsemi、Toshiba、Yageo、Wayon 维安、BrightKing 君耀 |
| MOV/GDT/surge | Littelfuse、Bourns、TDK/EPCOS、Vishay、Yageo/KEMET、Eaton、Mersen、Phoenix Contact、DEHN |
| DC fuse / high-voltage fuse | Littelfuse、Eaton Bussmann、Mersen、Schurter、Bel Fuse、SIBA、Fuji、Mitsubishi、Xi'an Sinofuse 中熔电气 |
| SSCB / solid-state relay / high-voltage protection | ST、TI、Infineon、onsemi、Littelfuse/IXYS、Eaton Breaktor、Schneider、ABB、Mitsubishi、Mersen、Microchip、Sensata |
| Gate driver / isolation / current sensor | TI、ADI、Infineon、onsemi、ST、Silicon Labs、Broadcom isolation、Allegro、LEM、Tamura、Monolithic Power、Microchip、Renesas |
| 中国国产功率器件 | Silan 士兰微、CR Micro 华润微、StarPower 斯达半导、Sanan 三安、BYD Semiconductor、CRRC Times、中微半导、扬杰科技、捷捷微电、华微电子、新洁能、东微半导、闻泰/Nexperia 中国链、英诺赛科、基本半导体、天岳先进、天科合达 |
| 数据中心保护和电力系统集成 | Littelfuse、Eaton、Schneider Electric、ABB、Siemens、GE Vernova、Vertiv、Mersen、nVent、Hubbell、Powell、Delta |

### 8.2 最值得跟踪的公司信号

| 公司 | 2026 关键信号 | 投资观察点 |
|---|---|---|
| MPS | Q1 2026 Enterprise Data $262.8M，同比增长 97.7%，由 AI/server power management 拉动；公司毛利约 55.5% | AI Vcore/模块化 power 的高毛利代表 |
| Vicor | Q1 2026 backlog $301M，同比 +75%、环比 +70%；扩产 2nd Gen VPD | VPD/IP/高密模块是否进入更多 hyperscaler |
| Infineon | 8kW AI PSU、650/750V CoolSiC Gen2、CoolGaN、OptiMOS；白皮书指向 8-30kW PSU | Si/SiC/GaN 全栈，AI PSU 受益确定 |
| TI | 与 NVIDIA 展示 800VDC 架构：800V hot-swap、800V-to-6V、6V-to-core | 800V 控制/隔离/保护和 6V 后级定点 |
| ST | 12kW/6kW/20kW 800V PDB、700V GaN、SiC/thyristor/SSCB | 800V PDB 和固态保护早期标准参与者 |
| Navitas | 20kW 800V-to-6V、250kW SST、3300V/1200V GeneSiC；AI/grid/high-power SAM 2030 $3.5B、60%+ CAGR | 800V option value 高，但公司规模和盈利需跟踪 |
| onsemi | Q1 2026 AI data center revenue more than doubled YoY；Power Solutions Group $736.6M | EliteSiC、CJFET、PowerTrench、smart fuse 的 AI 设计赢单 |
| Littelfuse | 投资者材料称 data center HVDC 可带来 2-4x content upside | 保护器件从传统件升级为 HVDC/BESS 安全件 |
| Nexperia | APEC 2026 hot-swap MOSFET for AI datacenters，AN90081 强调 40-60V/54V bus 需 80/100V enhanced SOA MOSFET | 48V 保护和 LFPAK/ASFET 的性价比路线 |
| Renesas/Transphorm | 高压 GaN 与电源控制器组合 | 服务器 PSU/PDB GaN 是否突破大客户 |
| Power Integrations | 高压 GaN/driver 集成能力 | 高效率 PSU 和 auxiliary power 机会 |
| Innoscience | 8-inch GaN-on-Si 产能和成本优势 | 中国/全球中低压 GaN 价格和份额扰动 |

## 9. 投资价值总结

### 9.1 最强 alpha

| 排名 | 方向 | 原因 |
|---:|---|---|
| 1 | Vcore/Power module/VPD | xPU 代际升级直接拉动；毛利高；客户切换成本高；MPS/Vicor 已用财务数据验证需求 |
| 2 | 48V hot-swap/eFuse/enhanced SOA MOSFET | 2026 即放量；保护昂贵 AI tray；设计一旦通过认证不易替换 |
| 3 | AI PSU SiC/GaN 器件 | 8-30kW PSU 和高效率刚需；SiC/GaN 从 EV 周期转向 AI 高性能应用 |
| 4 | 高压 DC protection | 800V 放量前必须完成标准和认证，2027 beta 很高 |
| 5 | 800V PDB/SSCB/SST | 2026 option，2027-2028 beta；若 NVIDIA Kyber/1MW rack 提前，弹性最大 |

### 9.2 最大风险

1. **800V 推迟。** 如果 Rubin/Kyber/MI400 交付或数据中心安规标准延迟，800V PDB/SSCB/SST 收入会从 2027 推到 2028。
2. **SiC 商品化。** EV SiC 过剩可能压低普通 SiC 价格，只有 AI-qualified 封装/系统方案能保持毛利。
3. **客户自研/垂直整合。** Hyperscaler 或 ODM 可能把模块价值内化，单一器件供应商被压价。
4. **供应链双源要求。** 小厂技术领先但产能、质量和第二来源不足，可能只能拿小批量高端订单。
5. **AI CapEx 波动。** 若 2027 云厂商因 token ROI 下修 CapEx，beta 高的 800V/VPD 会先受估值冲击。

## 10. 主要资料来源

| 来源 | 关键信息 |
|---|---|
| [NVIDIA 800 VDC Architecture](https://www.nvidia.com/en-us/data-center/technologies/800-vdc-architecture/) | 800VDC 从当前 AC 架构演进；future AI servers need more power than 54VDC；减少转换损耗 |
| [GE Vernova / NVIDIA AI Factory 800 VDC Reference Designs](https://content.cdntwrk.com/files/aT0xNTQwNjg5JnY9MSZpc3N1ZU5hbWU9d2hpdGVwYXBlci1haS1mYWN0b3J5LTgwMC12ZGMtcmVmZXJlbmNlLWRlc2lnbnMmY21kPWQmc2lnPWU1NDMyZjEyNDhiNWMyMDBiYjA4MmViNjJjNDRlNjk0) | 800VDC 参考设计、2027 Kyber/1MW rack、SST 5MW+ 2028、DC protection/energy storage |
| [TI 800 VDC with NVIDIA press release](https://www.prnewswire.com/news-releases/ti-unveils-complete-800-vdc-power-architecture-for-future-generation-ai-data-centers-with-nvidia-302714861.html) | 800V hot-swap、800V-to-6V 97.6% peak efficiency、>2000W/in3、6V-to-core |
| [TI 800V PSU white paper](https://www.ti.com/lit/wp/stda027/stda027.pdf?ts=1776196649413) | 800V sidecar PSU 与传统 PSU 对比、1200V SiC/650V serial topology、BDG、HV ORing |
| [TI 800V technical article](https://www.ti.com/lit/SSZTD83) | 1MW rack 使用 48V 需要约 450lb 铜；800V 需要 sensing/protection/isolation |
| [TechInsights datacenter power semiconductor analysis](https://www.techinsights.com/blog/analysis-power-semiconductor-datacenter-power-distribution) | 2026 data center power semiconductor revenue $5B，2031 $14.3B，rack BOM $2,300 到 $7,600 |
| [TechInsights Power Outlook 2026](https://www-prod.techinsights.com/outlook-reports-2026/power-outlook-report) | 2031 global power semiconductor $71.4B；AI datacenter、SiC commoditization、GaN rules |
| [APEC 2026 Program Book](https://apec-conf.org/wp-content/uploads/2026/03/APEC-2026-Program-Book-20260223.pdf) | Mitsubishi 800V/megawatt rack WBG seminar、Nexperia hot-swap MOSFET、Nyobolt ESS |
| [Infineon SiC data center power supply whitepaper](https://www.infineon.com/assets/row/public/documents/24/59/infineon-how-infineon-technologies-sic-solutions-are-shaping-the-future-of-data-center-power-supplies-whitepaper-en.pdf) | 650/750V CoolSiC Gen2、8-30kW PSU、.XT interconnect、2.9TWh/5年节电估算 |
| [Infineon 8kW AI PSU solution brief](https://www.infineon.com/assets/row/public/documents/24/63/infineon-8-kw-psu-for-ai-server-smps-solution-brief-additionalproductinformation-en.pdf) | 8kW AI server PSU，Si/SiC/GaN 混合方案 |
| [ST APEC 2026](https://www.st.com/content/st_com/en/events/apec.html?ecmp=tt48859_us_enews_mar2026) | 800V AI data center PDB、solid-state protection、eMOV/thyristor |
| [ST 800V AI data center blog](https://blog.st.com/800-v-hvdc-data-center/) | 6kW 800V-to-12V、20kW 800V-to-6V、12kW 800V-to-50V，97.5%/98%+ 等效率信息 |
| [ST 800V press release](https://newsroom.st.com/media-center/press-item.html/t4727.html) | 12kW GaN LLC 800V input、1MHz、>98%、>2600W/in3 |
| [ST 800V APEC presentation PDF](https://www.st.com/content/dam/static-page/events/apec-2026/gan-800v-ai-data-center-arch-pdb-exh-sem-apec-2026.pdf) | 800V 到 54V/12V/6V 架构和 BOM 示例 |
| [Navitas 800V-to-6V GTC 2026](https://navitassemi.com/navitas-debuts-revolutionary-800-v-6-v-power-delivery-board-at-nvidia-gtc-2026/) | 800V-to-6V 一阶段 PDB，面向 NVIDIA AI infrastructure |
| [Navitas/EPFL 250kW SST](https://navitassemi.com/navitas-epfl-to-demonstrate-novel-solid-state-transformer-solution-for-ai-data-center-enabling-800-v-dc-implementation/) | 3300V/1200V GeneSiC、250kW SST、800VDC distribution |
| [Navitas Q1 2026 results](https://ir.navitassemi.com/news-releases/news-release-details/navitas-semiconductor-announces-first-quarter-2026-financial) | 高功率市场增长、20kW 800V-to-6V、250kW SST、2030 SAM $3.5B/60%+ CAGR |
| [onsemi Data Center](https://www.onsemi.com/solutions/computing/data-center) | EliteSiC、PowerTrench T10、GaN HEMT、PoL buck、smart fuse、Vcore |
| [onsemi Server Power Supply](https://www.onsemi.com/solutions/computing/data-center/server-power-supply) | 800V HVDC PSU、SiC CJFET、vGaN、3.6kW TPPFC 99.3% |
| [onsemi Q1 2026 results](https://investor.onsemi.com/static-files/bda7f74d-e2fc-474c-8b7a-2ee1aac54f80) | Q1 revenue $1.513B；AI data center revenue more than doubled YoY |
| [MPS Q1 2026 earnings commentary](https://www.monolithicpower.com/media/investor-relations/press-releases/Q1_2026_MPS_Earnings_Commentary.pdf) | Enterprise Data $262.8M，YoY +97.7%；gross margin 55.5% |
| [MPS 48V Data Center](https://www.monolithicpower.com/en/products/power-management/48v-data-center.html) | 48V-to-4.8/6V 架构、130A/170A Intelli-Module、eFuse |
| [Vicor Q1 2026 results](https://vicorcorporation.gcs-web.com/news-releases/news-release-details/vicor-corporation-reports-results-first-quarter-ended-march-13) | Revenue $113M、gross margin 55.2%、backlog $301M、2nd Gen VPD capacity |
| [Vicor VPD article](https://www.vicorpower.com/resource-library/articles/high-performance-computing/modules-mitigate-the-environmental-impact-of-genai) | VPD 降 PDN 阻抗/PCB 损耗，1000A 和 64 AM rack 节电测算 |
| [Empower APEC 2026](https://www.globenewswire.com/news-release/2026/03/10/3252703/0/en/empower-semiconductor-showcases-Vertical-Power-Delivery-Innovations-at-APEC-2026.html) | Crescendo VPD、Crescendo HD 5A/mm2、kilowatt-class AI processors |
| [Littelfuse Data Center & Communications](https://www.littelfuse.com/applications/data-center-communications-solutions) | UPS/BESS/数据中心保护、TVS、PPTC、MOSFET、Schottky、overcurrent/overvoltage |
| [Littelfuse 2026 investor material](https://d18rn0p25nwr6d.cloudfront.net/CIK-0000889331/278802f7-d2e5-4d1f-85e5-c2120b59820e.pdf) | 数据中心 AC-DC 转向 ±400/800VDC，HVDC content 2-4x upside |
| [Nexperia AN90081 hot-swap MOSFET](https://assets.nexperia.com/documents/application-note/AN90081.pdf) | AI server hot-swap、40-60V/54V bus、80/100V enhanced SOA MOSFET |
| [Nexperia APEC 2026 hot-swap presentation](https://apec2026.eventscribe.net/fsPopup.asp?PresentationID=1775085&efp=UEhSTERXT0kyNDg3MA&rnd=0.6239164&mode=presInfo) | AI data center hot-swap MOSFET 专用要求、SOA、inrush、thermal stress |
| [ST Solid State Circuit Breaker](https://www.st.com/en/applications/energy-generation-and-distribution/solid-state-circuit-breaker-sscb.html) | SSCB 微秒级中断、SiC/GaN 对高压固态保护的意义 |
# 行业调研：【机柜级供电与服务器电源架构】

> 截至日期：2026-05-08  
> 研究范围：AI 数据中心机柜级供电、服务器电源架构、48V/54V 机柜电源、800VDC 高压直流、机柜内/板级 DC/DC、VRM/垂直供电、机柜侧 BBU/超级电容/瞬态能量缓冲、配套连接器/母线/监控。  
> 口径说明：本文不把园区外部电网、主变、燃机、全站 UPS/BESS 全额计入“机柜级供电”市场，但会在供给瓶颈与价值链中讨论它们，因为它们决定机柜能否上电。市场规模为模型估算，美元为名义值，`B`=十亿美元。

## 0. 结论先行

**核心判断：2026 年确定性最高的技术路径不是 800VDC，而是 48V/50V/54V ORv3/MGX 机柜供电继续大规模放量。** NVIDIA GB300 NVL72 官方参考架构已经明确：单柜最高约 142kW，配置 8 个 33kW power shelf，每个 power shelf 内含 6 个 5.5kW PSU；OCP 已有 Delta 33kW 1OU ORv3 power shelf，输出 48/50VDC、效率超过 97.5%。这类产品在 2026 年是实打实的订单池。

**800VDC 是 2027 年最大的增量期权。** NVIDIA 明确把 800VDC 定位为支持 1MW IT racks and beyond、从 2027 年开始随下一代平台推进；Vertiv 称 800VDC 产品组合计划 2026 年下半年发布、对齐 2027 Rubin Ultra；Delta、Lite-On、Eaton、ABB、Schneider、TI、ST、Infineon、MPS、Navitas 等都在 2025 Q4-2026 Q1 公开展示或发布方案。也就是说，2026 年是设计导入与试点锁单，2027 年才进入第一轮可验证放量。

**投资价值最强的层级不是普通 PSU 代工，而是“被 AI 芯片平台认证锁定的高密度电源系统 + 板级电源模块/功率半导体 + 高压直流保护/连接”。** 机柜电源在整柜 $3M-$9M 价值中占比不高，但故障代价极高，客户愿意为效率、可维护性、认证确定性和交付期支付溢价。

**滚动 12 个月全球 AI 机柜/服务器电源架构设备与关键电源半导体市场：**

| 口径 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 未来 3 个月收入池 | $3.8-6.5B | $6.5-10.5B | $10-17B |
| 未来 12 个月收入池 | $15-24B | $25-39B | $42-65B |
| 未来 24 个月收入池 | $32-52B | $58-90B | $95-145B |

这里的收入池包括：AI server PSU / 48V power shelf、rack busbar/rPDU/BBU、板级 DC/DC/VRM/电源模块、800VDC power rack/rectifier/DC busway/固态保护、连接器/线缆/监控软件。它不是传统 data center power market 的全站口径；Grand View Research 的全数据中心 power market 2025 年约 $22.77B、2033 年约 $71.76B，可作为下限校验，但 AI 机柜电源在 2026-2028 会显著跑赢普通数据中心电力设备。

## 1. 2026 机遇与挑战：AI 计算中心大规模建设对供电架构意味着什么

### 1.1 机会

1. **100kW+ AI 机柜变成主流交付单元。** GB200 NVL72 官方用户指南显示机柜功耗约 120kW；GB300 NVL72 参考架构显示整柜最高约 142kW。传统 5-15kW 企业机柜的 PDU/PSU 逻辑已经不够用，机柜级电源从“配套件”升级成“系统交付能力”。
2. **48V/54V 标准化带来确定订单。** OCP ORv3、Meta/Open Rack Wide、NVIDIA MGX/NVL72 都把供电、液冷、服务性和 rack-scale 计算绑定在一起。33kW power shelf、5.5kW PSU、48/50V 母线、rack-level power controller、热插拔、冗余与监控，会在 2026 年跟随 GB300/B300、Trainium2/3、Ironwood TPU、MI350、Maia200、MTIA 等平台出货。
3. **800VDC 把电源价值从 PSU 扩展到“grid-to-chip”。** 800VDC 不是简单换电压，而是把 AC/DC 集中到 power room/row，800VDC 经 busway 送到 compute rack，再在机柜/节点内转 54V/12V/6V/核心电压。对应新增产品包括中央整流器、SST、DC busway、固态断路器、800V-to-54V/12V/6V DC/DC、高压连接器、机柜侧超级电容/BBU。
4. **板级电源成为 AI 芯片性能瓶颈。** AI accelerator 核心电压低于 1V、电流上千安到数千安，HBM、GPU、CPU、交换芯片都需要极快瞬态响应。Infineon 2026 年发布 TLVR quad-phase 模块，Empower 在 APEC 2026 推 VPD，ST 发布 800V 到 12V/6V 架构，说明价值正在从“机柜到板卡”继续下沉到“板背/封装附近”。
5. **供不应求产品具备溢价。** 对 $3M-$9M 的 AI rack 来说，power shelf、DC/DC、VRM、连接器的 BOM 绝对值不大，但停机成本巨大。被 NVIDIA/Meta/Google/AWS/Microsoft/Oracle/HPE/Dell/SMCI 认证的供应商有明显交付与定价权。

### 1.2 挑战

| 挑战 | 为什么重要 | 对投资的含义 |
|---|---|---|
| 安全与认证 | 800VDC 涉及 DC 拉弧、人员安全、故障隔离、UL/IEC/NEC/NFPA 适配，远比 48V 难 | 固态断路器、eFuse、熔断器、接触器、监控传感器价值提升 |
| 标准碎片化 | NVIDIA MGX/DSX、OCP ORv3、Meta ORW、Google/AWS 私有架构并存 | 头部供应商要支持多平台，研发与库存压力上升 |
| 动态负载 | LLM 推理/训练带来毫秒到秒级功率波动，传统 UPS 只解决断电，不解决高频波动 | 机柜侧超级电容、power capacitance shelf、软件功率调度变成新产品 |
| 热与电耦合 | 电源效率损失直接变成热，PSU/VRM 也要被液冷/风液混合管理 | 能把 power+cold plate+CDU+rack 一起验证的供应商更有议价权 |
| 高端元件供应 | GaN/SiC、MOSFET、磁性件、MLCC/聚合物电容、铜排、连接器、传感器都可能卡交付 | 非芯片瓶颈会放大，二三线供应商进入机会变多 |
| 客户认证周期 | 一个 power shelf/DC/DC 模块更换可能触发整机热、电、固件、BMC、冗余重测 | 一旦 design-in，切换成本高，毛利稳定 |

## 2. 当前正在使用的技术路径

### 2.1 传统路径：415/480VAC 到机柜，机柜 PSU 转 12V 或 54V

传统数据中心是 MVAC 入站，降压到 415/480VAC，经 UPS/PDU/busway 到机柜，在机柜或服务器内用 AC/DC PSU 转为 12V，再由板级 VRM 转核心电压。优点是成熟、标准清晰、供应商多；缺点是在 100kW+ 机柜下，机柜 PSU 体积、风扇、铜耗、热耗和维护复杂度迅速上升。

### 2.2 2026 主流路径：OCP ORv3 / MGX 48V-54V power shelf + 机柜母线

2026 年最确定的路线是：415/480VAC 或三相 AC 到 rack power shelf，power shelf 内部由 5.5kW/更高功率 PSU 转 48/50/54VDC，经机柜母线供给 compute tray / switch tray，节点内再转 12V/6V/核心电压。OCP Marketplace 上 Delta 33kW 1OU ORv3 power shelf 是标志性产品：6 槽、6 个 5.5kW PSU、最大 33kW、5+1 冗余时 27.5kW、48/50VDC 输出、效率超过 97.5%。

NVIDIA GB300 NVL72 参考架构显示：8 个 33kW power shelf、每个 power shelf 6 个 5.5kW PSU，满柜最高约 142kW；in-rack switches 接入 DC busbar。这意味着 2026 年的主流不是“单台服务器 PSU”，而是“整柜电源系统 + DC 母线 + 管理控制”。

### 2.3 板级路径：48V IBC + 12V/6V 中间母线 + TLVR/多相 VRM

AI 加速器板卡通常由 48V 输入，经 IBC 转 12V、6V 或 4-6V，再由多相 buck/TLVR/DrMOS/功率模块转核心电压。MPS、Infineon、Vicor、TI、Renesas、ADI、onsemi、ST、Empower 等在这一层竞争。方向包括：

- 48V 到 12V/6V 高效率 IBC；
- 12V/6V 到核心电压的 TLVR、多相 power stage、DrMOS；
- 垂直供电 VPD，把电源模块放到 PCB 背面甚至封装附近，减少 IR drop；
- 硅电容/高密度去耦，提升 GPU 快速负载变化时的电源完整性。

### 2.4 2027 路线：800VDC 进数据大厅/机柜，机柜内晚级降压

NVIDIA 800VDC 架构的核心是：在 power room/perimeter 直接把中压 AC 转成 800VDC，再通过数据大厅 busway/row-level protection 送至 IT rack，机柜内通过 DC/DC 降为 54V/12V/6V/核心电压。NVIDIA 称 800VDC 相比 54V 架构可减少电流、铜用量和线缆体积，面向 1MW rack and beyond；其技术博客还提出 Kyber 架构中用高压直接到节点，再用 64:1 LLC 在 GPU 附近降到 12V。

**判断：** 800VDC 在 2026 年属于“客户项目设计基准 + GTC/OCP 展示 + 早期样机/试点”，2027 年随 Rubin Ultra/Kyber 进入第一波量产。2028 年以后才可能从 NVIDIA 生态外溢到多家平台。

### 2.5 最近半年会议、论坛与技术报告信号

| 时间/场景 | 信号 | 对本行业的含义 |
|---|---|---|
| 2026-03 NVIDIA GTC | NVIDIA 发布 Vera Rubin DSX，Delta/Lite-On/TI/ST/Schneider/Eaton 等集中展示 800VDC、power rack、DC/DC、数字孪生 | 800VDC 从 NVIDIA 单点路线变成系统生态联盟 |
| 2026-04 Data Center World | Schneider Secure Power CTO Jim Simonelli 公开强调：800VDC 的核心不只是效率，而是把电源和铜缆从 rack 中移出去，为 GPU 腾空间 | 证明行业一线共识已经从“AC vs DC”转为“机柜空间、可维护性和规模化” |
| 2026-03 APEC | Infineon、Empower、ST 等围绕 TLVR、VPD、800V-to-12/6V 做技术展示 | 板级/封装级供电进入 2027-2028 高端 AI 芯片 design-in 周期 |
| 2025-10 OCP Global Summit | NVIDIA、Delta、Eaton、Vertiv、AMD/Meta ORW 等展示 800VDC、Open Rack Wide、AI rack power/cooling/serviceability | OCP 继续提供开放标准底座，但真实利润会落在通过平台验证的供应商 |
| 2026-04 Bloomberg/Sightline 转述 | 2026 美国计划上线约 12GW 数据中心容量，但只有约三分之一在建；变压器、switchgear、电池等电力设备短缺拖慢项目 | 机柜级产品需求很强，但实际收入确认受外部电力链条约束；电源供应商订单可能领先机柜上电 |

### 2.6 行业报告与规模交叉校验

本文的市场规模不是直接照搬单一报告，而是三层校验：第一层用既有项目底稿中的美国 AI 数据中心建设规模和芯片出货节奏估算 AI rack 数量；第二层用 GB200/GB300/Rubin/MI400/Trainium/TPU 的单柜功率和 power shelf 配置估算机柜电源价值量；第三层用 Grand View Research 的传统 data center power market、NVIDIA/ABB 的 80GW 到 220GW 数据中心需求展望、Bloomberg/Sightline 对 2026 美国 12GW 计划容量但实际建设受限的描述做上下限约束。因此，报告中的“极度超预期乐观”数字本质上是假设大客户把 2027-2028 的 AI factory 与 800VDC 需求明显前置。

## 3. AI 芯片技术路径对供电架构的影响

项目已有芯片底稿显示，2026-2027 年初最关键的出货平台集中在 Blackwell/Blackwell Ultra、Trainium2/3、TPU Ironwood、MI350/MI400、Maia/MTIA、Ascend 等。对机柜供电的含义如下：

| 芯片/平台 | 2026-2027 阶段 | 供电架构影响 | 对应最可能放量产品 |
|---|---|---|---|
| NVIDIA B300/GB300 NVL72 | 2026 主力放量 | 142kW 级液冷整柜，8x33kW power shelf，48/50/54V DC busbar | 33kW power shelf、5.5kW PSU、48V 母线、rack controller、液冷耦合 PDU |
| NVIDIA GB200 NVL72 | 2025-2026 延续放量 | 约 120kW 整柜，验证了 NVL72 机柜级供电模型 | 48V power shelf、AC/DC PSU、DC/DC IBC、power monitoring |
| NVIDIA Vera Rubin NVL72 | 2026 H2 首批，2027 放量 | 仍可沿 MGX/NVL72 第三代过渡，但功耗/瞬态更高 | 高功率 48V shelf、90kW/110kW DC/DC shelf、强化 VRM |
| NVIDIA Rubin Ultra / Kyber | 2027 关键期权 | 800VDC/Kyber、1MW rack、800V 到 12V/6V 晚级降压 | 800VDC power rack、DC busway、固态保护、64:1 LLC、高压连接器 |
| AWS Trainium2/3 | 2026 Trainium2 主力，2027 Trainium3 | 私有 rack/UltraServer，强调能效与自研 fabric | 定制 48V 电源、机柜 BBU、内部 power shelf，外部可见度较低 |
| Google TPU v7 Ironwood / TPU8 | 2026 Ironwood，2027 TPU8 | Google 自有数据中心协同供电，推理优先但规模大 | 高效 power shelf、私有 rack power、48V/液冷/储能调度 |
| AMD MI350 / MI400 Helios | 2026 MI350，2026 H2 MI400 初期 | Helios 对齐 Meta Open Rack Wide，面向开放 rack-scale | ORW/ORv3 power shelf、开放 rack busbar、MI400 以后更高功率 |
| Meta MTIA 300/400/500 | 2026-2027 自研 ASIC 扩大 | Meta/OCP 标准牵引，GenAI inference 密度上升 | ORW/ORv3 rack power、定制 DC/DC、OCP 标准连接器 |
| Microsoft Maia200 | 2026 Azure 推理导入 | 750W SoC + 闭环液冷，强调推理 TCO | Azure 私有 power shelf、板级 VRM、液冷电源协同 |
| Huawei Ascend 910C/950 | 中国国产替代主线 | SuperPoD/超节点以系统并联弥补单芯片差距，电源/冷却压力上升 | 国产 48V power shelf、VRM、电感/电容、液冷耦合供电 |

### 3.1 新技术成熟与放量时间

| 技术路径 | 基准情景 | 乐观情景 | 极度超预期乐观 |
|---|---|---|---|
| 48V/54V ORv3/MGX power shelf | 已成熟，2026 全年放量，2027 随 GB300/Rubin/MI400 延续 | 2026 H2 供应商扩产，power shelf 成整柜标配 | 2026 H2 交付瓶颈从 GPU 转向 power shelf/液冷，ASP 上行 |
| 5.5kW-8kW 高功率 AI PSU | 2026 放量，5.5kW 为主，8kW+ 局部 | 2027 8kW/12kW 级产品在高端 rack 加速 | 2027 前因 800VDC 过渡，AC/DC PSU 与 DC/DC shelf 双线缺货 |
| 800VDC power room/row/rack | 2026 H2 试点，2027 随 Rubin Ultra/Kyber 小批量 | 2027 新建 AI factory 10-20% 采用 | 2027 大客户把 2028 需求前置，30%+ 新建高端 rack 项目采用 |
| 800V-to-54/12/6V DC/DC | 2026 样机/设计导入，2027 量产初期 | 2027 H2 随 Kyber/非 NVIDIA 平台扩散 | 2027 直接 800V-to-12/6V 成高端 rack 卖点 |
| 垂直供电/封装附近 VRM | 2026 APEC/GTC 设计展示，2027 进入少数 ASIC/GPU | 2027 高端 xPU 量产 design-in，2028 放量 | 2028 成为高端 AI 芯片性能释放必要条件 |
| 机柜侧超级电容/BBU/功率平滑 | 2026 在 Delta/Eaton/NVIDIA 架构中出现，项目制 | 2027 随 800VDC 和功率波动管理放量 | 大模型推理瞬态引发电网侧限制，近 rack 储能变成强制配置 |

### 3.2 2026 最可能的技术路径

2026 年最可能落地的是 **“480/415VAC 到机柜 power shelf，48/50/54VDC 母线进 compute tray，板级 12V/6V/核心电压转换，整柜液冷耦合”**。800VDC 会在大型客户和新建 AI factory 的设计中被提前锁定，但大规模收入确认更可能在 2027。

## 4. 已开始放量的关键产品：规模、渗透率、利润率

### 4.1 产品拆分与市场规模预测

| 已放量产品 | 当前状态 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 48V/50V/54V ORv3/MGX power shelf 与高功率 AI PSU | 2026 主力，33kW shelf/5.5kW PSU 已标准化 | 基准 $1.2-2.1B；乐观 $2.0-3.5B；极度 $3.5-5.8B | 基准 $5.5-8.8B；乐观 $9-14B；极度 $15-23B | 基准 $10-16B；乐观 $18-29B；极度 $32-46B | 新建高端 AI rack 2026 55-70%，2027 70-85%，2028 80-92% |
| 机柜 DC busbar / rPDU / ORv3 母线 / 盲插连接 | 与 GB200/GB300/ORv3 同步 | 基准 $0.5-0.9B；乐观 $0.9-1.6B；极度 $1.6-2.8B | 基准 $2.2-4.0B；乐观 $4.0-7.0B；极度 $7.5-12B | 基准 $4.5-8B；乐观 $9-16B；极度 $18-28B | 100kW+ rack 2026 45-60%，2027 60-75%，2028 70-85% |
| 48V IBC、12V/6V 中间母线、板级 VRM/DrMOS/TLVR | 随 AI GPU/ASIC 线性增长，单机价值提升 | 基准 $1.1-1.9B；乐观 $1.8-3.1B；极度 $3.0-5.0B | 基准 $4.8-8.2B；乐观 $8-13B；极度 $14-22B | 基准 $10-18B；乐观 $19-32B；极度 $35-55B | 高端 AI 加速器板卡 2026 60-75%，2027 75-88%，2028 85-95% |
| 高电流连接器、线缆、铜排、eFuse/hot-swap | 与 rack power density 同步 | 基准 $0.4-0.8B；乐观 $0.8-1.3B；极度 $1.3-2.2B | 基准 $1.8-3.2B；乐观 $3.0-5.5B；极度 $5.5-9.0B | 基准 $3.8-6.8B；乐观 $7-12B；极度 $13-22B | AI rack 2026 50-65%，2027 65-80%，2028 75-90% |
| 机柜级电源监控、PMC、PMBus、能耗调度软件 | power shelf 标配化 | 基准 $0.15-0.35B；乐观 $0.35-0.65B；极度 $0.65-1.1B | 基准 $0.7-1.4B；乐观 $1.3-2.4B；极度 $2.5-4.0B | 基准 $1.8-3.2B；乐观 $3.5-6.0B；极度 $6.5-10B | 2026 30-45%，2027 50-65%，2028 70%+ |
| 48V rack BBU / power capacitance shelf / 超级电容缓冲 | 早期但已有 Delta/Eaton/NVIDIA 方案牵引 | 基准 $0.2-0.5B；乐观 $0.5-1.0B；极度 $1.0-1.8B | 基准 $1.0-2.2B；乐观 $2.5-5.0B；极度 $5.5-9.0B | 基准 $3.0-6.0B；乐观 $7.0-14B；极度 $16-26B | 2026 10-20%，2027 25-40%，2028 45-65% |

### 4.2 已放量产品毛利率预测

| 产品 | 当前毛利率判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|---:|
| 标准 AI PSU / 33kW power shelf | 18-26% | 18-24% | 22-30% | 28-38% |
| 客制化 rack power shelf / 90-110kW DC/DC shelf | 24-35% | 25-34% | 32-42% | 40-50% |
| 48V IBC / VRM / TLVR / power module | 45-60% | 45-55% | 52-64% | 60-72% |
| 高端连接器/母线/盲插组件 | 25-38% | 25-35% | 32-42% | 38-50% |
| 电源监控/固件/软件 | 55-80% 软件毛利，但硬件混合后 35-55% | 35-50% | 45-60% | 55-70% |
| 机柜 BBU/超级电容 shelf | 22-35% | 22-32% | 30-42% | 40-55% |

## 5. 在研与即将快速增长的关键产品

### 5.1 关键技术与市场规模预测

| 在研/放量前产品 | 技术状态 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 800VDC power rack / 中央整流 / DC busway | GTC/OCP 展示，2026 H2 design-in | 基准 $0.2-0.6B；乐观 $0.6-1.2B；极度 $1.2-2.5B | 基准 $1.5-4.0B；乐观 $4-9B；极度 $9-18B | 基准 $8-18B；乐观 $22-42B；极度 $48-80B | 2026 <3%，2027 5-15%，2028 15-35%；极度情景 2028 可达 45%+ 新建高端 AI factory |
| 800V-to-54V/12V/6V 高压 DC/DC | ST/TI/Delta/LiteOn/Vertiv 等发布方案 | 基准 $0.1-0.4B；乐观 $0.4-0.9B；极度 $0.9-1.8B | 基准 $0.8-2.2B；乐观 $2.5-6.0B；极度 $6-12B | 基准 $5-12B；乐观 $14-28B；极度 $30-55B | 2026 试点，2027 进入 Rubin Ultra/Kyber，2028 多平台扩散 |
| 固态断路器、DC protection、eFuse、安全传感 | ABB/Infineon/Eaton 等牵引 | 基准 $0.1-0.25B；乐观 $0.25-0.55B；极度 $0.55-1.0B | 基准 $0.6-1.6B；乐观 $1.8-4.0B；极度 $4-8B | 基准 $3-7B；乐观 $8-16B；极度 $18-32B | 随 800VDC 绑定，2027 起刚性需求 |
| 垂直供电 VPD / in-package VRM / silicon capacitor | APEC 2026 展示，少数客户验证 | 基准 $0.08-0.25B；乐观 $0.25-0.55B；极度 $0.55-1.0B | 基准 $0.7-2.0B；乐观 $2.0-5.0B；极度 $5-10B | 基准 $4-10B；乐观 $12-28B；极度 $30-60B | 2026 <5%，2027 10-20%，2028 25-50% 高端 xPU |
| GaN/SiC 高压功率器件与高速控制器 | 800V 架构拉动，Navitas/ST/TI/Infineon/onsemi 等 | 基准 $0.2-0.6B；乐观 $0.6-1.2B；极度 $1.2-2.2B | 基准 $1.0-2.8B；乐观 $3-7B；极度 $7-14B | 基准 $6-14B；乐观 $16-32B；极度 $35-65B | 高端 power conversion 2026 10-20%，2028 35-60% |
| 动态功率调度与 AI factory 电源数字孪生 | NVIDIA DSX、Schneider ETAP、Siemens、Vertiv 等 | 基准 $0.1-0.3B；乐观 $0.3-0.7B；极度 $0.7-1.2B | 基准 $0.8-1.8B；乐观 $2-4B；极度 $4-7B | 基准 $3-6B；乐观 $7-13B；极度 $14-22B | 2026 设计工具，2027 运营软件，2028 与功率限额绑定 |

### 5.2 在研产品毛利率预测

| 产品 | 基准 | 乐观 | 极度超预期乐观 | 定价能力来自哪里 |
|---|---:|---:|---:|---|
| 800VDC power rack / 中央整流 / SST | 25-35% | 32-45% | 42-55% | 高压安全、系统验证、服务网络、与 NVIDIA/云厂商参考设计绑定 |
| 800V-to-12/6V 高密度 DC/DC | 35-50% | 45-60% | 55-70% | 转换效率、功率密度、热设计、GPU 附近瞬态响应 |
| 固态断路器 / DC protection | 45-60% | 55-68% | 65-78% | DC 拉弧/保护算法/认证门槛，替换风险高 |
| VPD / in-package power | 55-68% | 62-75% | 70-82% | 直接决定 xPU 性能释放，IP 与客户绑定强 |
| GaN/SiC 器件 | 40-55% | 50-62% | 58-70% | 高压高频器件良率、封装、长期认证 |
| 电源数字孪生/控制软件 | 60-85% 软件毛利 | 65-85% | 70-90% | 数据、平台、闭环控制与设施级接口绑定 |

## 6. 供给侧分析

### 6.1 产能结构

| 层级 | 主要地区 | 主要公司 | 工艺/能力 |
|---|---|---|---|
| AI PSU / power shelf | 台湾、中国大陆、泰国、越南、墨西哥、美国小批量 | Delta、Lite-On、Chicony Power、AcBel、FSP、Flex、Advanced Energy/Artesyn、Murata/TDK-Lambda、Bel Fuse、Great Wall、Huntkey、Megmeet | 高功率 AC/DC、PFC、LLC、热插拔、PMBus、钣金与风扇/液冷耦合 |
| 800VDC 系统 | 美国、欧洲、日本、台湾 | Vertiv、Eaton、Schneider、ABB、Siemens、GE Vernova、Hitachi Energy、Delta、Lite-On、Mitsubishi Electric、Heron Power | 中央整流、SST、MV UPS、DC busway、保护、数字孪生 |
| 板级电源模块/VRM | 美国、欧洲、日本、台湾、中国大陆 | MPS、Infineon、Vicor、TI、Renesas、ADI、onsemi、ST、Empower、EPC、Navitas、ROHM、Power Integrations、Innoscience、Richtek、AOS | 48V IBC、TLVR、多相 power stage、GaN/SiC、VPD |
| 连接器/母线/线缆 | 美国、欧洲、日本、中国大陆、台湾 | Amphenol、TE Connectivity、Molex、Samtec、BizLink、Lead Wealth、Methode、Mersen、Littelfuse、Legrand/Starline、nVent、Hubbell、Panduit | 高电流低阻抗、盲插、镀层、温升、弧光安全 |
| 整柜/服务器集成 | 台湾、中国大陆、美国、墨西哥、捷克、东南亚 | Foxconn、Quanta/QCT、Wiwynn、Wistron、Inventec、Pegatron、Jabil、Celestica、Flex、Supermicro、Dell、HPE、Lenovo、Gigabyte | MGX/NVL72、ORv3/ORW、液冷整柜、rack burn-in |

### 6.2 供给瓶颈

1. **高功率磁性件与变压器。** 5.5kW-18.5kW PSU、800VDC SST、LLC/DC/DC 都依赖高频磁性件，良率和热设计难度高。
2. **GaN/SiC 与高压 MOSFET/控制器。** 800VDC、98%+ AC/DC、1MHz LLC 需要更高频、更高压、更高可靠性器件。
3. **高电流连接器与铜排。** 48V 架构下电流巨大，母线温升、接触电阻、盲插可靠性、镀层和机械公差都可能卡产能。
4. **DC protection 与安全认证。** 800VDC 拉弧、故障隔离、维护规程、UL/IEC/NEC/NFPA 标准仍在磨合，认证周期会拖慢导入。
5. **板级电源完整性工程人才。** TLVR/VPD/封装去耦涉及电源、封装、热、信号完整性协同，经验型工程师稀缺。
6. **整柜测试与 burn-in。** GB300 级整柜 142kW，测试本身需要高功率假负载、液冷环路、电源扰动仿真。
7. **客户平台认证。** NVIDIA/AMD/Meta/Google/AWS/Microsoft 平台认证后才能量产，切换供应商要重跑可靠性与固件测试。
8. **上游电力设备长交期。** 虽不计入机柜电源市场，但主变、switchgear、UPS、BESS、busway 交期会决定 power shelf 订单能否兑现。

### 6.3 成本与毛利

**33kW 级 ORv3 power shelf BOM 拆分估算：**

| 成本项 | 占比 | 说明 |
|---|---:|---|
| 功率半导体、控制 IC、驱动、保护 | 25-35% | PFC、LLC、MOSFET/GaN/SiC、PMBus、eFuse |
| 磁性件、电感、变压器 | 15-25% | 高频磁性件是效率和体积关键 |
| 电容、MLCC、聚合物、超级电容接口 | 8-15% | 去耦、hold-up、瞬态响应 |
| PCB、铜排、连接器、线缆 | 12-20% | 高电流、低阻抗、温升约束 |
| 结构件、风扇/冷却、钣金 | 8-15% | 1OU 高密度机械难度高 |
| 测试、老化、固件、质保 | 8-15% | 高功率 burn-in 与客户认证成本高 |

**毛利决定因素：**

- 效率：97.5%、98%、98.5% 的差异会被数据中心 PUE、电费和散热成本放大。
- 功率密度：1OU 33kW、110kW power shelf、90kW DC/DC shelf 等决定机柜中留给 compute 的空间。
- 平台认证：GB300/Rubin/ORW/Trainium/TPU 认证供应商有高粘性。
- 交期：供不应求时，客户为确定交付支付溢价。
- 服务能力：800VDC 和液冷电源需要现场维护能力，Vertiv/Eaton/Schneider/ABB 这类供应商因此更强。

**价格传导机制：** 功率半导体/磁性件/铜材涨价会先传到 PSU/power shelf，再传到服务器 ODM/OEM，最终进入 AI rack 总价。由于电源成本占整柜比例低，但故障风险高，2026-2027 上游涨价较容易向客户传导。

## 7. 竞争格局与壁垒

### 7.1 市场结构

| 层级 | 集中度判断 | 原因 |
|---|---|---|
| 标准 AI PSU / power shelf | CR5 约 55-70% | Delta、Lite-On、Chicony、AcBel、FSP/Flex 等具备大客户认证和产能 |
| 800VDC 系统级架构 | CR5 约 65-80% | Vertiv、Eaton、Schneider、ABB、Delta、Lite-On、Siemens/GE Vernova/Hitachi Energy 等要同时有高压、服务和系统能力 |
| 板级 VRM/电源模块 | CR5 约 60-75% | MPS、Infineon、Vicor、TI、Renesas/ADI/onsemi/ST 等 design-in 粘性强 |
| 高端连接器/母线 | CR5 约 50-65% | Amphenol、TE、Molex、Samtec、Legrand/Starline、nVent、Hubbell 等认证周期长 |
| 整柜集成 | 头部集中但客户多源 | Dell、SMCI、HPE、Foxconn、Quanta、Wiwynn、Jabil、Celestica 等跟随 GPU 分配 |

### 7.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 定价逻辑 |
|---|---|---|
| 电源完整性与瞬态响应 | AI GPU/ASIC 电流突变极快，掉压会直接影响稳定性 | 客户为避免整柜宕机支付高可靠溢价 |
| 平台认证 | 通过 GB300/Rubin/ORW/TPU/Trainium 认证后替换难 | design-in 后切换成本高，价格弹性小 |
| 高压安全认证 | 800VDC 涉及 DC 拉弧、固态保护、维护流程 | 认证稀缺形成高毛利 |
| 功率密度 | 更小体积释放更多 compute 空间 | 每节省 1OU 都能转化为 GPU/网络价值 |
| 热设计协同 | PSU、VRM、液冷、机柜气流/水路耦合 | 能做整柜联调的供应商更少 |
| 规模交付 | 大客户要数千到数万机柜一致性 | 有全球制造/服务网络者享有份额溢价 |
| 固件/监控 | PMBus、Redfish、BMC、power capping 与数据中心软件集成 | 软件锁定提升长期毛利 |

### 7.3 价值捕获：长期高 ROIC 在哪里

最可能长期高 ROIC 的层级是 **板级电源模块/功率半导体、800VDC 保护与 DC/DC、通过大客户认证的系统级 power rack**。普通 PSU 代工会被规模竞争压低毛利，但高密度模块、VPD、固态断路器、高压 DC/DC、平台参考设计具有更高技术壁垒和更强客户粘性。

## 8. 2026 关键变化：三个最可能拐点

1. **GB300/B300 让 100kW+ 机柜成为常态交付，33kW power shelf 与 5.5kW PSU 放量。** 这会把订单从传统服务器 PSU 厂商扩展到 rack power shelf、母线、监控和整柜验证。
2. **800VDC 生态在 GTC/OCP 后形成事实联盟。** NVIDIA 公开合作伙伴覆盖 ABB、Eaton、Schneider、Vertiv、Delta、Lite-On、TI、ST、Infineon、MPS、Navitas 等，2026 H2 的关键不是收入，而是进入客户设计基准。
3. **功率瞬态从工程问题变成产品问题。** Delta 展示 480kW embedded BBU、NVIDIA 800VDC 架构提到 subsecond GPU power fluctuations，Eaton 引入 supercapacitors，这意味着机柜侧能量缓冲会从可选项变成高端 AI rack 的保险件。

## 9. 2027 关键变化：三个最可能拐点

1. **Rubin Ultra/Kyber 推动 800VDC 第一轮商业放量。** 基准情景下只在少数新建 AI factory 放量；乐观情景下，800VDC 成为 2027 年高端项目的默认设计之一。
2. **800V-to-12V/6V 与垂直供电开始决定芯片性能释放。** ST 明确 50V、12V、6V 中间母线会共存；Empower、Infineon、MPS 等把供电推近 GPU，2027-2028 高端 ASIC/GPU 会把 VPD 作为性能工具。
3. **标准从“开放”走向“平台绑定”。** OCP ORv3/ORW 会降低通用 rack 门槛，但真正能挣钱的是被 NVIDIA DSX/MGX、Meta ORW、Google/AWS 私有 rack 验证过的系统。标准化提高市场规模，平台认证决定利润率。

## 10. 头部公司与细分清单

### 10.1 机柜电源、800VDC 与系统级架构

| 公司 | 优势 | 观察点 |
|---|---|---|
| Vertiv | GB300 142kW 参考架构、800VDC H2 2026 产品计划、全球服务工程师 | 800VDC 真实订单、Rubin Ultra 项目进入 backlog |
| Eaton | grid-to-chip、ORv3 busbar、supercapacitor、DC connectors、800VDC 参考架构 | 800VDC 与 supercap 是否进入标准配置 |
| Schneider Electric | ETAP/EcoStruxure/AVEVA 数字孪生、GB300/Rubin 参考设计、Motivair 液冷 | power+cooling+software 套餐化能力 |
| ABB | MV UPS、DC distribution、solid-state circuit breaker、SACE Infinitus | 800VDC 安全保护与 IEC 认证优势 |
| Delta Electronics | 48V ORv3 power shelf、800VDC 660kW power rack、480kW embedded BBU、18.5kW 98% PSU | 从部件到系统级方案的份额提升 |
| Lite-On | 800VDC power rack、110kW power shelf、NVIDIA Vera Rubin/MGX 展示 | 是否获得 Rubin/Kyber 量产认证 |
| Siemens / Siemens Energy | DSX、工业电气、数字化、现场电力系统 | 与 AI factory 建设/EPC 绑定 |
| GE Vernova / Hitachi Energy / Mitsubishi Electric | 中压、变换、grid interface | 800VDC 与园区电力接口 |
| Flex / Lead Wealth / Megmeet | 电源系统组件与制造能力 | 是否进入 NVIDIA 800VDC 合作项目量产 |

### 10.2 AI Server PSU / Power Shelf

| 公司 | 优势 |
|---|---|
| Delta | 全球电源龙头，OCP 33kW ORv3 power shelf，NVIDIA 800VDC 深度合作 |
| Lite-On | AI data center power rack、110kW power shelf、NVIDIA GTC 2026 展示 |
| Chicony Power | 高功率电源制造与云/服务器客户基础 |
| AcBel | 服务器 PSU、云客户认证、台湾供应链 |
| FSP | 高功率 PSU、OCP/服务器电源经验 |
| Flex / Artesyn / Advanced Energy | 高可靠电源与系统制造 |
| Murata / TDK-Lambda | 高可靠电源模块、磁性件和工业客户 |
| Bel Fuse / Compuware | 数据中心电源和网络电源 |
| Great Wall / Huntkey / MEAN WELL | 中国供应链与中低端/部分服务器电源能力 |

### 10.3 板级电源模块与功率半导体

| 公司 | 优势 |
|---|---|
| MPS | AI/server/memory/optical/switch power solutions，48V 模块，已 sampling 800V data center solution |
| Infineon | grid-to-core，TLVR quad-phase >2A/mm²，Si/SiC/GaN 与 48V IBC |
| Vicor | 48V direct-to-load、Factorized Power Architecture，高密度 AI accelerator 供电 |
| TI | 2026 GTC 推 800VDC complete architecture，模拟/控制/隔离/传感完整 |
| STMicroelectronics | 800V-to-50V/12V/6V，GaN LLC，>98% 级原型 |
| Renesas | 控制器、power stage、数据中心电源 |
| Analog Devices | 电源管理、隔离、传感、数据中心系统 |
| onsemi | 高压/低压功率器件、NVIDIA 800VDC 生态伙伴 |
| Navitas | GaN/SiC，NVIDIA 800VDC 合作，100V/650V/高压 SiC |
| Empower Semiconductor | VPD/Crescendo，5A/mm² 目标，AI kilowatt-class processor |
| EPC / Innoscience / ROHM / Power Integrations / AOS / Richtek | GaN/SiC/控制器/PMIC，在 800VDC 与板级供电中有设计导入机会 |

### 10.4 连接器、母线、机柜与整柜集成

| 层级 | 公司 |
|---|---|
| 高电流连接器/线缆 | Amphenol、TE Connectivity、Molex、Samtec、BizLink、Lead Wealth、Methode、Mersen、Littelfuse |
| 母线/配电/机柜 PDU | Legrand/Starline/Raritan、nVent、Hubbell、Eaton、Schneider、ABB、Siemens、Vertiv、Panduit、Chatsworth |
| 整柜/服务器 ODM/OEM | Foxconn、Quanta/QCT、Wiwynn、Wistron、Inventec、Pegatron、Jabil、Celestica、Flex、Supermicro、Dell、HPE、Lenovo、Gigabyte/Giga Computing |
| 机柜侧储能/BBU/超级电容 | Eaton、Delta、Vertiv、Schneider/APC、ABB、Tesla、Fluence、Powin、Saft、Samsung SDI、LG Energy Solution、CATL、Skeleton Technologies、Piller、Active Power、VYCON、EnerSys |

## 11. 投资结论

**2026 年最优策略：买确定性瓶颈。** 48V/54V power shelf、5.5kW-8kW AI PSU、rack busbar、板级 DC/DC/VRM、液冷耦合电源是确定性订单；供应商只要进入 GB300/B300/Rubin/ORW/TPU/Trainium 认证，就能享受高可见度。

**2027 年最优策略：买 800VDC 放量期权。** 800VDC 的系统级供应商、固态保护、高压 DC/DC、GaN/SiC、VPD 是弹性最大方向。基准情景下 2027 是小批量；乐观情景下 2027 H2 开始大客户规模复制；极度超预期情景下，新建 AI factory 把 2028 的高压直流需求前置到 2027。

**价值链排序：**

1. 板级电源模块/功率半导体：长期毛利最高，客户锁定强。
2. 800VDC 系统与保护：2027-2028 增速最快，安全认证壁垒高。
3. 48V power shelf/AI PSU：2026 收入确定性最高，但竞争更激烈。
4. 连接器/母线/机柜 PDU：稳健增长，毛利取决于是否高端认证。
5. 普通服务器 PSU：总量增长但毛利压力较大，需观察 AI 定制化占比。

## 12. 关键来源与数字锚点

| 来源 | 关键事实 |
|---|---|
| [NVIDIA 800 VDC Architecture](https://www.nvidia.com/en-us/data-center/technologies/800-vdc-architecture/) | NVIDIA 称传统 54V 成瓶颈，800VDC 可减少转换、铜耗和线缆体积，并列出 ABB、Delta、Eaton、Infineon、Lite-On、MPS、Navitas、Schneider、ST、TI、Vertiv 等生态伙伴 |
| [NVIDIA 800VDC Technical Blog](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) | 800VDC 支持 1MW IT racks and beyond，2027 起随下一代 AI factory 推进；提到 54V 在 200kW+ rack 的空间/铜耗限制 |
| [NVIDIA 800VDC Ecosystem Blog](https://developer.nvidia.com/blog/building-the-800-vdc-ecosystem-for-efficient-scalable-ai-factories/) | Kyber rack 采用 800VDC，节点附近用高比率 64:1 LLC 降到 12V；提出机柜附近超级电容和设施级 BESS 处理不同时间尺度负载波动 |
| [NVIDIA GB300 NVL72 Reference Architecture PDF](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory-with-gb300-nvl72-dual-plane-networking-architecture.pdf) | GB300 NVL72：8 个 33kW power shelf，每个 6 个 5.5kW PSU，整柜最高 142kW，in-rack switch 连接 DC busbar |
| [NVIDIA DGX GB User Guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) | GB200 NVL72 机柜功耗约 120kW |
| [OCP Delta 33kW ORv3 Power Shelf](https://www.opencompute.org/products/430/delta-33kw-1ou-open-rack-v3-power-shelf) | 6 槽、6x5.5kW、最大 33kW、5+1 冗余 27.5kW、48/50VDC 输出、效率超过 97.5% |
| [Delta GTC 2026](https://www.delta-americas.com/en-US/news/40116) | 800VDC 660kW power rack、480kW embedded BBU、18.5kW AC/DC PSU 最高 98%、1RU 90kW DC/DC power shelf、2.4MW CDU |
| [Lite-On GTC 2026](https://www.liteon.com/en/news/press-center/content/liteon-nvidia-gtc-2026) | 展示 NVIDIA Vera Rubin、800VDC power rack、110kW power shelf、2.1MW in-row CDU |
| [Vertiv 800VDC readiness](https://www.vertiv.com/en-us/about/news-and-events/corporate-news/from-vision-to-readiness-vertiv-collaborates-with-nvidia-to-advance-800-vdc-platform-designs-to-power-the-next-generation-of-ai-factories/) | 800VDC 产品组合计划 2026 H2 发布，对齐 2027 Rubin Ultra；包含 centralized rectifiers、DC busways、rack-level DC/DC |
| [Vertiv GB300 reference architecture](https://www.vertiv.com/en-us/about/news-and-events/corporate-news/vertiv-develops-energy-efficient-cooling-and-power-reference-architecture-for-the-nvidia-gb300-nvl72/) | GB300 142kW power/cooling 参考架构，支持 50% faster on-site builds、30% less physical space 等目标 |
| [Eaton 800VDC reference architecture](https://www.eaton.com/gb/en-gb/company/news-insights/news-releases/2025/eaton-unveils-next-generation-architecture.html) | Eaton 800VDC 参考设计包括 supercapacitors、ORv3 busbar、hot aisle containment、DC connectors |
| [ABB + NVIDIA](https://new.abb.com/news/detail/129900/abb-to-develop-next-generation-ai-data-c%E2%80%A6) | ABB 支持 NVIDIA 800VDC 1MW server racks；提到 MV UPS + DC distribution + solid-state power electronics |
| [Schneider + NVIDIA GTC 2026](https://www.se.com/us/en/about-us/newsroom/news/press-releases/Schneider-Electric-teams-with-NVIDIA-to-develop-validated-blueprints-to-design-simulate-build-operate-and-maintain-gigawattscale-AI-Factories-69b82f61aa1027e04205d273/) | Schneider 参与 Vera Rubin reference design，验证最新 rack-scale 架构的 power/cooling，并与 Omniverse DSX/ETAP/EcoStruxure 结合 |
| [ST 800VDC portfolio](https://newsroom.st.com/media-center/press-item.html/t4766.html) | ST 发布 800VDC 到 12V/6V 架构，称 50V、12V、6V 中间母线会共存；此前 800V-to-50V GaN LLC 原型 >98%、>2600W/in³ |
| [Infineon TLVR module](https://www.infineon.com/market-news/2026/infpss202603-076) | 2026 年发布 TDM24745T TLVR quad-phase power module，电流密度超过 2A/mm²，用于 AI accelerator 高电流核心轨 |
| [Infineon data center power](https://www.infineon.com/cms/en/applications/information-communications-technology/data-center-ai-data-center/) | AI rack 从今天约 100kW 走向 1MW+；48V IBC、VPD、Grid-to-core 是主线 |
| [MPS Q4 2025 commentary](https://www.globenewswire.com/en/news-release/2026/02/05/3233414/0/en/Monolithic-Power-Systems-Provides-Earnings-Commentary-for-the-Quarter-and-Year-Ended-December-31-2025.html) | MPS 称 data center power solutions 客户扩大，已 sampling 800V power solution for data center |
| [Empower APEC 2026](https://www.empowersemi.com/empower-semiconductor-showcases-vertical-power-delivery-innovations-at-apec-2026/) | 展示 Crescendo VPD，称 AI xPU 进入多千瓦功率域，下一代技术冲击 5A/mm² |
| [AMD Helios/OCP ORW](https://ir.amd.com/news-events/press-releases/detail/1261/amd-showcases-helios-rack-scale-platform-built-on-the-open-compute-project-open-rack-for-ai-introduced-by-meta) | AMD Helios 对齐 Meta 提交 OCP 的 Open Rack Wide，双宽 rack 面向下一代 AI power/cooling/serviceability |
| [Grand View Research data center power market](https://www.grandviewresearch.com/industry-analysis/data-center-power-market) | 全球 data center power market 2025 年约 $22.77B，2033 年约 $71.76B，2026-2033 CAGR 15.7% |
| [Data Center World 2026 / Data Center Knowledge](https://www.datacenterknowledge.com/build-design/data-center-world-2026-new-limits-push-power-architecture-beyond-the-rack) | Schneider CTO 在 DCW 2026 强调 800VDC 是为解决 rack 内空间、铜缆、电源和冷却挤占 GPU 空间的问题 |
| [Tom's Hardware / Bloomberg / Sightline](https://www.tomshardware.com/tech-industry/artificial-intelligence/half-of-planned-us-data-center-builds-have-been-delayed-or-canceled-growth-limited-by-shortages-of-power-infrastructure-and-parts-from-china-the-ai-build-out-flips-the-breakers) | 2026 美国约 12GW 计划数据中心容量中仅约三分之一在建；变压器、switchgear、电池等电力设备短缺拖慢上线 |

---

非投资建议。本报告用于产业链研究和情景分析；关键风险包括 AI capex 放缓、GPU/HBM/CoWoS 交付扰动、800VDC 标准化慢于预期、安全认证延迟、供电事故导致监管趋严、客户自研架构封闭化、价格竞争压缩 PSU 毛利。
# 行业调研：【机柜、围护结构与物理安防】

版本日期：2026-05-08  
研究窗口：最近半年，重点覆盖 2025-11 至 2026-05 的一手公告、论坛/展会材料、行业报告与公司技术路径。  
口径说明：本文把“机柜、围护结构与物理安防”定义为 AI 计算中心白空间和安全边界里的非 IT 服务器硬件，包括高密度机柜、OCP/ORW 机架、整柜预集成、机柜液冷接口、通道/机柜围护、笼式隔离、机柜级门锁、门禁、视频、周界、访客和审计系统。不包括 GPU、服务器主板、UPS、变压器、主 CDU、冷却塔和总包 EPC，但会讨论与这些系统的接口。

## 0. 结论先行

2026 年这个行业不是传统“机柜铁皮”周期，而是 AI factory 把机柜重新定义为“算力交付单元”的拐点。过去机柜的定价锚是尺寸、承重、交期和品牌；2026-2027 年的定价锚变成：能否承载 80-150kW 以上的液冷 rack-scale 系统、是否进入 NVIDIA/AMD/OCP/云厂商认证清单、能否工厂预集成并带着机柜液冷歧管/线缆/传感/安防审计一起交付。

最强判断：

| 判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 全球 AI 相关机柜、围护与物理安防收入池 | $14B-$19B | $20B-$28B | $32B-$45B |
| 2027 全球 AI 相关机柜、围护与物理安防收入池 | $21B-$30B | $34B-$50B | $58B-$85B |
| 2028 年化收入池 | $30B-$45B | $58B-$85B | $100B-$145B |
| 2026 最确定放量 | 高承重液冷就绪机柜、预集成整柜、机柜液冷歧管、AI 园区门禁/视频/机柜锁 | OCP ORV3、白空间模块、笼式隔离、安全平台统一化 | ORW 双宽机架、800VDC/sidecar power rack、机柜级 BBU/储能、物理安全数字孪生 |

和第三方报告的关系：MarketsandMarkets 预计全球数据中心机柜市场从 2025 年 $5.17B 增至 2030 年 $9.42B，CAGR 12.7%。Grand View Research 预计数据中心围护市场 2024 年 $2.38B，2033 年 $6.92B，CAGR 12.7%；数据中心物理安防市场 2025 年 $2.40B，2033 年 $7.27B，CAGR 15.0%。这些是窄口径市场报告。本文的乐观/极度乐观口径额外计入 AI 高密机柜的预集成、液冷接口、项目制围护、机柜级电子安防、软件许可与快速交付溢价，因此显著高于传统报告。

## 1. 最近半年一手信号：订单、公告与技术路径

| 日期 | 公司/组织 | 一手信号 | 对本行业的含义 |
|---|---|---|---|
| 2026-04-22 | Vertiv | Q1 2026 净销售 $2.65B，同比 +30%；Americas 有机增长 +44.3%；上调 2026 全年指引至 $13.5B-$14.0B，全年有机增长 +29%-31%。 | AI 数据中心对关键基础设施的需求已经进入收入确认，不只是 pipeline。高密度机柜、白空间集成、冷却和服务会一起放量。 |
| 2026-03-24 | Vertiv | 宣布美洲四个新建/扩建制造设施，覆盖 infrastructure solutions、power management 和 integrated cabinets。 | 机柜/集成柜产能成为限制交付速度的瓶颈之一，Vertiv 在把 Great Lakes 并入后的 rack capability 工厂化。 |
| 2025-08-20 | Vertiv | 完成约 $200M 收购 Great Lakes Data Racks & Cabinets。 | 高端定制机柜从小众机械件变成 AI 基础设施平台公司的战略资产。 |
| 2026-03-18 | nVent | 2026 Investor Day 提出基础设施垂直加速增长，驱动来自 AI data center build-outs 与 power utilities，三年有机增长目标 +10%-13%。 | nVent 的 Hoffman/Schroff/Trachte 等组合受益于机柜、保护外壳、预制控制建筑和电气连接。 |
| 2025-09-03 | nVent | 在 Blaine, Minnesota 新增 117,000 平方英尺数据中心解决方案产能，2026 年初投产，含液冷解决方案；Anoka+Blaine 合计新增 325+ jobs。 | 液冷就绪机柜、歧管、连接与保护件的供应链正在北美本地化。 |
| 2026-05-07 | Legrand | Q1 2026 销售额剔除汇率 +18%，有机 +9.3%，收购 +8.2%，调整后经营利润率 20.7%；称增长由 datacenters 和收购驱动。 | Legrand 已把数据中心作为集团增长核心，机柜、PDU、busway、containment、security/monitoring 组合价值上升。 |
| 2026-04-01 | Legrand | 收购 Keydak（中国广州机柜厂，330+ 人，年收入 >€60M）和 TES（英国配电系统，年收入近 €85M，其中一半以上来自数据中心）。Legrand 称 2025 年底数据中心占集团收入 26%，2026 年四项收购合计新增年收入约 €285M。 | “机柜产能+区域交付+关键电力”正在被头部公司并购整合；中国/欧洲本地机柜产能被全球巨头纳入。 |
| 2026-02-12 | Legrand | 收购 Kratos Industries，并战略投资 Accelsius 两相直接到芯片液冷。 | 机柜供应商向灰空间电力和液冷接口延伸，目标是 AI-ready end-to-end infrastructure。 |
| 2026-04-30 | Schneider Electric | Q1 2026 收入 €9.767B，有机 +11.2%；Energy Management +12.8%，由 Data Center 强劲驱动。 | Schneider 的 NetShelter/Pod/Rack Infrastructure、Motivair 液冷、ETAP/EcoStruxure 数字孪生形成 AI 数据中心设计入口。 |
| 2026-03-16 | Schneider + NVIDIA + AVEVA | 在 GTC 2026 推进 gigawatt-scale AI factories 的 validated blueprints；此前 2025-09 已有支持 NVIDIA Mission Control 和 GB300 NVL72 的参考设计，纳入 ETAP 与 EcoStruxure IT Design CFD。 | 机柜/围护从“施工末端采购”前移为 rack layout、CFD、液冷控制、电力控制的早期设计变量。 |
| 2026-05 | Eaton | Q1 2026 销售 $7.5B，同比 +17%；Electrical Americas rolling 12-month orders 有机 +42%，由 data center momentum 驱动；Electrical sector backlog +48%。 | Eaton/Tripp Lite/ORV3 机柜、prefab power enclosure、busway、rack power 与 AI 数据中心同步吃到订单。 |
| 2026-03 | Eaton + NVIDIA | GTC 2026 推出 Eaton Beam Rubin DSX 平台，并讨论 800VDC power infrastructure。 | 2026 是 800VDC/sidecar power rack 的 reference/pilot 年，2027-2028 才可能实质放量。 |
| 2026-03 | NVIDIA | GB300 NVL72 官方定位为 fully liquid-cooled rack-scale architecture，单系统含 72 个 Blackwell Ultra GPU 和 36 个 Grace CPU。 | 100kW+ 级整柜交付成为 2026 主线，传统 19 英寸机柜必须升级承重、深度、线缆、液冷接口和工厂测试能力。 |
| 2026-03 | NVIDIA | Vera Rubin DSX AI Factory 参考设计覆盖 compute、Spectrum-X Ethernet networking 和 storage；Switch、Nscale/Caterpillar 等按 DSX 设计推进 AI factory。 | 2027 的机柜采购将跟着 DSX/Omniverse 数字孪生和 rack-scale 标准走，供应商需要提供可仿真的设备模型和接口数据。 |
| 2026-04 | Rittal | OCP EMEA Summit 2026 展示 Open Rack V3、高密 rack、智能 power、液冷；展出与 NVIDIA 新架构共同开发的 MGX rack 后门冷却方案。 | Rittal 将 ORV3、MGX、rear-door cooling、DLC 绑定为标准化 AI 基础设施路径。 |
| 2026-04 | Rittal | OCP ORV3 Rack 获 OCP accepted，支持 21 英寸 OCP 部件、busbar 直接接触，并预留 DLC。 | ORV3 在 2026 从 hyperscaler 内部标准走向可采购产品。 |
| 2026 | OCP/Eaton | Eaton ORV3 支持 21 英寸 ORV3 与传统 19 英寸混装，可内置 ORV3 busbar 和 power shelf，使用 blind-mate power connection。 | 2026-2027 机架的核心变化是从“PDU 接线”向“busbar/blind-mate/模块化供电”迁移。 |
| 2025-11 | Genetec | 2026 物理安防趋势强调云/混合部署、开放架构、IT/OT/physical security convergence；Genetec 服务 42,500+ 客户、159+ 国家。 | 数据中心物理安防正在从孤立门禁/视频变成统一平台，软件和渠道粘性变强。 |
| 2026 | Axis | 数据中心方案从 perimeter 到 server racks，覆盖视频分析、门禁、QR/PIN/key card、双向音视频。 | 摄像头不只是安全设备，也会成为运维/访客/效率数据源。 |
| 2025-11 | ASSA ABLOY | 数据中心物理安防白皮书提出安全下沉到 server cabinet level，柜门 access control 可记录授权/拒绝尝试并保留 audit trail；HES KS 支持 OSDP、Wiegand、Aperio。 | AI rack 单柜价值 $2M-$4M 甚至更高，机柜级电子锁从 colo 可选件变成高价值资产的保险/合规工具。 |

## 2. 2026 AI 芯片路线对机柜、围护与安防的影响

项目已有 AI 芯片路线图显示，2026 出货主力仍是 NVIDIA B300/GB300 Blackwell Ultra、GB200/B200、AWS Trainium2/3、Google TPU v7 Ironwood、AMD MI350，2026 下半年到 2027 年初开始导入 Vera Rubin、AMD MI400/MI455X Helios、TPU8、Meta MTIA 400/450/500、Microsoft Maia 200、OpenAI/Broadcom ASIC、Huawei Ascend 950。它们对本行业的影响不是“更多机柜”这么简单，而是 5 个机械和安防变量同时跳变：

| 芯片/平台 | 2026-2027 出货节奏 | 对机柜/围护的要求 | 对物理安防的要求 |
|---|---|---|---|
| NVIDIA GB300/B300 Blackwell Ultra | 2026 主力放量 | NVL72 为 fully liquid-cooled rack-scale，72 GPU+36 Grace；机柜需高承重、深柜、液冷歧管、线缆管理、运输预集成、残余热围护。 | 单柜价值极高，推荐柜门电子锁、摄像头覆盖、柜级审计。 |
| NVIDIA GB200/B200 | 2025-2026 交付延续 | 形成 GB300 的机械/液冷/整柜交付经验曲线。 | 高价值 GPU 资产，colo 场景更需要租户级隔离。 |
| NVIDIA Vera Rubin NVL72 | 2026 H2 开始，2027 放量 | 第三代 MGX NVL72 rack design，继续推高 rack-scale 标准化；DSX 数字孪生会要求供应商提供可仿真设备数据。 | AI factory 级别，多园区复制需要统一身份、视频、访客和审计平台。 |
| AMD MI400/MI455X Helios | 2026 H2 早期，2027 主要增量 | 项目内路线显示 Helios/MI455X 指向 Open Rack Wide/高密液冷 rack；双宽或开放 rack 有望在 2027 获得实际需求。 | 开放 rack/双宽 rack 对通道布置、笼式隔离、运维权限边界提出新要求。 |
| AWS Trainium2/3 | 2026 已大规模，2027 Trainium3 延续 | 自研 UltraServer/机架内部互连，公开供应商少，但会拉动定制机柜、内部白空间模块和专用工装。 | Hyperscaler 自用为主，强周界、强访问控制，柜级锁不一定公开采购但会有内部等效需求。 |
| Google TPU v7/v8 | 2026 Ironwood，2027 TPU8 | Google 自定义 pod/rack，供应链更封闭；对机柜机械件、液冷、线缆和高可靠交付有强认证。 | 高安全自有园区，物理安防软件/硬件更强调开放接口和隐私合规。 |
| Meta MTIA / OCP | 2026-2027 四代迭代 | Meta 是 OCP/开放机架标准关键推动者；ORV3/ORW、48V busbar、工厂化 rack 配置受益。 | 多租户少，自用多，但大规模员工/承包商访问使身份治理和视频审计很重要。 |
| OpenAI/Broadcom ASIC | 2026 H2 起步，2027 多 GW | 以推理为主，若 10GW 节奏加速，预集成整柜、模块化机房和物理安防会被提前锁定。 | 模型权重和推理容量成为战略资产，柜级和房间级双重隔离提升。 |
| Huawei Ascend/国产 AI | 2026 中国替代主线 | 国产 rack、液冷、围护、安防供应链本地化；SuperPod/CloudMatrix 推高机柜和超节点布置复杂度。 | 国资/政企/运营商场景要求国产安防、等保/信创、门禁视频一体化。 |
| Microsoft Maia 200 | 2026 导入 Azure | 3nm/216GB HBM3E/推理导向，Azure 自用 rack 和闭环液冷。 | Azure 级别物理安防平台化，柜级资产审计价值上升。 |

## 3. 技术路线成熟和放量时间

| 技术路线 | 2026-05 状态 | 基准情景成熟/放量 | 乐观情景成熟/放量 | 极度超预期乐观成熟/放量 | 2026 最可能性 |
|---|---|---|---|---|---|
| 高承重 42-52U、深柜、液冷就绪 19 英寸机柜 | 已成熟，正在扩产 | 2026 全年放量，2027 成为 AI colo 默认 | 2026 H2 缺货，ASP +10%-20% | 2026 H2 到 2027 交付排队，客户接受项目级溢价 | 极高 |
| 整柜预集成/rack-and-stack/白空间集成柜 | Vertiv、Legrand、Dell/HPE/SMCI/ODM 均在推进 | 2026 H2 主流化，2027 30%-45% 新 AI rack 采用 | 2026 H2 渗透率 35%+，2027 50%+ | 2027 大型园区把整柜预集成作为默认交付 | 极高 |
| 机柜液冷歧管、blind-mate quick disconnect、漏液传感 | GB200/GB300 已带动放量 | 2026 H2 大规模，2027 70%+ 新高端 AI rack | 2026 年底成紧缺件，2027 附加值显著提升 | 2027 进入 rack vendor 核心利润池 | 极高 |
| 热通道/冷通道围护、chimney、RDHx | 传统成熟，AI 改造中 | 空冷/混合冷却大厅继续放量，液冷大厅做残余热管理 | 2026 retrofit 和 brownfield 高增长 | 若液冷机柜供不应求，RDHx 作为过渡方案超预期 | 高 |
| OCP ORV3 21 英寸、48/54V busbar、power shelf | OCP accepted 产品可采购，hyperscaler 已验证 | 2026 从自用/少数云走向 10%-20% 新 AI rack，2027 20%-35% | 2027 35%-45% 新 AI rack | 若 Meta/AMD/ASIC 需求超预期，2027 可接近 50% | 中高 |
| Open Rack Wide/双宽高功率机架 | 2026 处于早期/平台导入 | 2027 小批量，2028 放量 | 2027 H2 伴随 MI400/MTIA/ASIC 放量 | 2027 成为非 NVIDIA 高密 rack 的核心路径之一 | 中 |
| 800VDC/sidecar power rack | GTC 2026 参考/展示，早期工程 | 2027 pilot，2028 批量 | 2027 H2 在 Rubin/Ultra 高功率园区小规模收入 | 2027 就进入头部云和 NeoCloud 的采购清单 | 中 |
| 机柜级智能门锁/电子把手/OSDP 审计 | colo 已用，hyperscale 分层采用 | 2026-2027 在 AI colo、主权 AI、金融/政府 AI 中加速 | 2027 成为高价值 GPU rack 的保险要求 | 2027 大型 colo 新 AI 区 70%+ 配置 | 高 |
| 统一门禁+视频+访客+ALPR+证据平台 | 成熟，Genetec/LenelS2/Axis/Johnson Controls 等主导 | 2026 继续升级，2027 与 DCIM/BMS 交叉 | AI 视频分析、移动凭证、云/混合平台加速 | 软件 license 和运维服务成为长期高毛利层 | 高 |
| 安防/机柜数字孪生、SimReady 资产与自动审计 | 2026 刚从电力/冷却数字孪生向安全延伸 | 2027 早期项目 | 2027 与 DSX/ETAP/CFD/DCIM 集成放量 | 2028 前成为高端园区标配 | 中 |

2026 年最可能的技术路径：高承重液冷就绪 19 英寸机柜 + GB300/MGX 整柜预集成 + 机柜液冷歧管 + 混合通道围护 + 门禁/视频统一平台。ORV3 会增长，但 2026 最确定的是“液冷 rack-scale 的机械和集成能力”，不是完全替代 19 英寸生态。

## 4. 已开始放量的关键产品：市场规模、渗透率和毛利

下表为全球 AI 数据中心增量采购口径，时间从 2026-05-08 起算。规模包含产品、定制、集成和项目溢价，不含 GPU/服务器、主 UPS、变压器和主 CDU。

### 4.1 市场规模与渗透率

| 产品 | 未来 3 个月：基准/乐观/极度 | 未来 1 年：基准/乐观/极度 | 未来 2 年：基准/乐观/极度 | 渗透率路径 |
|---|---:|---:|---:|---|
| 高承重液冷就绪机柜、深柜、预装门/线缆管理 | $1.2B-$1.6B / $1.6B-$2.1B / $2.1B-$3.0B | $5.0B-$6.2B / $6.5B-$8.5B / $9B-$12B | $7B-$9B / $10B-$14B / $16B-$22B | 新 AI rack 约 75%-85%，两年内 90%+。 |
| 预集成整柜、rack-and-stack、AI 白空间集成柜 | $0.8B-$1.3B / $1.4B-$2.2B / $2.4B-$3.8B | $3.5B-$5.5B / $6B-$9B / $10B-$15B | $6B-$9B / $10B-$16B / $18B-$28B | 2026 新 AI rack 20%-30%，2028 基准 45%-60%，极度情景 70%+。 |
| OCP ORV3/21 英寸/48V busbar/power shelf 机架 | $0.25B-$0.45B / $0.45B-$0.75B / $0.8B-$1.3B | $1.0B-$1.8B / $2.0B-$3.2B / $4B-$6B | $2B-$3.5B / $4.5B-$7B / $8B-$13B | 2026 新 AI rack 8%-15%，2028 基准 20%-35%，极度 45%+。 |
| 热/冷通道围护、rigid panels、end doors、chimney、curtains | $0.8B-$1.0B / $1.0B-$1.4B / $1.4B-$2.0B | $3.0B-$3.8B / $4B-$5.2B / $5.5B-$7.5B | $4.2B-$5.6B / $6B-$8.5B / $9B-$13B | 空冷/混合大厅 80%+；纯液冷 AI 区域仍有 45%-65% 残余热/维护通道围护。 |
| 机柜液冷歧管、RDHx、quick disconnect、漏液传感、液冷机柜附件 | $0.7B-$1.2B / $1.3B-$2.1B / $2.2B-$3.4B | $3B-$5B / $6B-$9B / $10B-$15B | $6B-$9B / $12B-$18B / $22B-$32B | 新高端 AI rack 2026 H2 45%-60%，2027 65%-85%，2028 80%-95%。 |
| Colocation cages、private suites、mesh cage、抗入侵围护和安全隔断 | $0.3B-$0.6B / $0.6B-$1.0B / $1.1B-$1.8B | $1.5B-$2.4B / $2.8B-$4.5B / $5B-$8B | $2.5B-$4B / $5B-$8B / $9B-$15B | AI colo 新增区 30%-45%，两年内 50%-70%；主权 AI/金融/政府更高。 |
| 机柜级电子锁、智能把手、OSDP/Aperio/Wiegand 接入、柜门审计 | $80M-$140M / $150M-$250M / $300M-$500M | $0.4B-$0.8B / $0.9B-$1.4B / $1.6B-$2.5B | $0.8B-$1.5B / $1.8B-$3.0B / $3.5B-$5.5B | AI colo 约 15%-30%，两年内 35%-60%；极度情景高价值 GPU rack 75%+。 |
| 数据中心物理安防系统：门禁、视频、周界、访客、mantrap、ALPR、VMS/ACS | $0.7B-$0.9B / $1.0B-$1.3B / $1.5B-$2.0B | $2.8B-$3.6B / $4B-$5.2B / $6B-$8B | $4.5B-$6B / $7B-$10B / $12B-$18B | 新 AI 园区几乎 100% 配置；升级点是 AI 视频、统一平台、移动凭证、生物识别和柜级审计。 |

### 4.2 增速和利润率

| 产品 | 2026-2028 收入 CAGR：基准/乐观/极度 | 当前毛利率估计：基准/乐观/极度 | 未来两年利润率方向 |
|---|---:|---:|---|
| 高承重液冷就绪机柜 | 25%-35% / 40%-55% / 65%-90% | 22%-30% / 28%-36% / 35%-45% | Commodity rack 被压价，高端定制、短交期、预装线缆和抗震认证提升毛利。 |
| 预集成整柜/rack-and-stack | 45%-60% / 65%-85% / 100%+ | 25%-35% / 32%-42% / 40%-50% | 工厂测试、现场时间压缩和客户认证会把利润从施工现场转移到集成厂。 |
| OCP ORV3/ORW 开放机架 | 55%-75% / 80%-110% / 130%+ | 22%-32% / 30%-40% / 38%-48% | OCP accepted、busbar、blind-mate、混装能力提高定价；标准化后会有价格下行。 |
| 围护/containment | 20%-30% / 35%-50% / 60%-80% | 25%-40% / 35%-45% / 45%-55% | 项目制设计、安装和改造毛利高；纯材料件毛利一般。 |
| 机柜液冷附件 | 55%-75% / 85%-120% / 150%+ | 35%-50% / 45%-58% / 55%-65% | quick disconnect、歧管洁净度、漏液测试、认证供应商清单形成高壁垒。 |
| 安全 cages/suites | 30%-45% / 50%-70% / 90%+ | 25%-38% / 35%-50% / 45%-60% | 受益于 colo 租户隔离和合规，现场安装能力决定毛利。 |
| 机柜级电子锁/智能把手 | 45%-70% / 80%-110% / 140%+ | 35%-50% / 45%-58% / 55%-70% | 电子锁硬件+访问控制软件+运维服务，若进入标准配置，毛利可接近安防软件层。 |
| 物理安防平台 | 25%-40% / 45%-60% / 75%-100% | 硬件 30%-45%，软件 70%-85%，系统集成 20%-35%， blended 35%-55% | 软件订阅、云/混合平台、视频分析和证据管理提高长期毛利。 |

## 5. 在研和快速增长的新技术

| 技术/产品 | 2026-05 状态 | 未来 3 个月市场 | 未来 1 年市场 | 未来 2 年市场 | 渗透率与毛利判断 |
|---|---|---:|---:|---:|---|
| Open Rack Wide/双宽 AI rack | 早期导入，依赖 AMD Helios、Meta/OCP 和自研 ASIC 生态 | $50M-$150M / $150M-$300M / $300M-$600M | $0.6B-$1.5B / $1.5B-$3.5B / $4B-$7B | $3B-$8B / $8B-$15B / $18B-$30B | 2027 渗透率基准 5%-12%，极度 25%+；毛利 25%-50%。 |
| 800VDC / sidecar power rack / 高压直流白空间柜 | GTC 2026 reference/pilot，尚非主流 | $0-$100M / $100M-$250M / $250M-$600M | $0.5B-$1.5B / $1.5B-$4B / $5B-$9B | $2B-$7B / $8B-$18B / $22B-$45B | 2027 多为头部园区试点，2028 才有大规模；高壁垒毛利 35%-60%。 |
| Rack-level BBU/超级电容/机柜级短时储能 enclosure | OCP/AI rack power 讨论升温，产品化早期 | $50M-$200M / $200M-$500M / $0.5B-$1B | $0.5B-$1.2B / $1.5B-$4B / $5B-$10B | $2B-$6B / $7B-$18B / $20B-$40B | 若动态功率调度普及，机柜安全 enclosure、热失控防护和认证成为利润点。 |
| 安防/机柜/冷却数字孪生与 SimReady 设备模型 | 电力/冷却先行，安防与机柜 telemetry 正在接入 | $100M-$250M / $250M-$500M / $0.5B-$1B | $0.6B-$1.5B / $1.5B-$3.5B / $4B-$8B | $2B-$5B / $5B-$12B / $15B-$30B | 软件毛利 65%-85%；采购壁垒是与 ETAP/EcoStruxure/Omniverse/DCIM/VMS 集成。 |
| Zero-trust physical identity：生物识别、mobile credential、anti-tailgating、访客 AI | 技术成熟，数据中心高安全场景加速 | $200M-$400M / $400M-$800M / $0.8B-$1.4B | $1B-$2B / $2B-$4B / $5B-$8B | $3B-$6B / $6B-$12B / $15B-$25B | 软件+读头+turnstile；毛利 45%-75%；隐私法规和误识率是瓶颈。 |
| 封闭液冷 AI pod、containerized white-space、secure modular enclosure | 早期到项目制放量 | $0.2B-$0.5B / $0.5B-$1.2B / $1.5B-$3B | $1.5B-$4B / $4B-$9B / $10B-$18B | $5B-$15B / $16B-$35B / $40B-$75B | NeoCloud 和 BYOP&C 推动，毛利 25%-45%，交付速度比单品毛利更关键。 |
| 机柜/通道级自动巡检、视频运维分析、安全机器人 | 早期 | $20M-$80M / $80M-$200M / $200M-$500M | $0.2B-$0.6B / $0.6B-$1.5B / $2B-$4B | $1B-$3B / $3B-$8B / $10B-$20B | 若劳动力短缺严重，巡检自动化放量；硬件毛利一般，软件/数据高。 |

## 6. 供给侧：产能、瓶颈、成本与价格传导

### 6.1 产能结构

| 区域 | 主要产能/公司 | 优势 | 风险 |
|---|---|---|---|
| 美国/墨西哥 | Vertiv/Great Lakes、Legrand、nVent、Eaton/Tripp Lite、Panduit、Chatsworth Products、Great Lakes、Modular/prefab integrators | 靠近 hyperscaler 与 AI colo 项目；关税与 Buy American 受益；可做预集成和短交期。 | 熟练钣金/电气/液冷装配工不足，工资高，扩产周期 6-18 个月。 |
| 欧洲 | Schneider、Rittal、Legrand/Minkels、nVent Schroff、Eaton、Siemens/Rittal、ASSA ABLOY、dormakaba | 高端电气标准、机柜和物理安防强；EN 50600、GDPR、主权 AI 项目受益。 | 能源成本、劳动力和跨国项目认证复杂。 |
| 中国/台湾 | Keydak、Cheval、Sanmina、Gigabyte、AMAX、Delta、Huawei 生态、ODM/OEM 供应链 | 成本、钣金、机箱、ODM 系统集成能力强；ORV3/白牌 rack 可快速扩产。 | 美国项目关税/安全审查/NDAA 限制；高安全 AI 园区更倾向本地供应。 |
| 东南亚/印度 | Legrand/Valrack、NetRack、部分 ODM 迁移产能 | 成本和供应链多元化；满足非中国采购。 | 高端认证、液冷洁净装配和项目管理能力仍需爬坡。 |
| 日本/韩国 | Murata power shelf、Fujitsu/NEC、部分精密连接/安防 | 高可靠电气和连接器。 | 机柜大规模制造成本不占优。 |

### 6.2 供给瓶颈

1. 高承重、大深度、抗震认证机柜：AI rack 重量、深度、线缆和液冷接口远高于传统 8-15kW 机柜，ASCE 7、UL、EIA-310、OCP accepted、客户自定义测试会拉长认证。
2. 机柜液冷接口：歧管、quick disconnect、软管、阀、漏液检测、洁净冲洗、压力测试的质量事故成本极高，供应商必须通过 GPU/ODM/设施方联合认证。
3. 预集成和运输：装好服务器和液冷件的整柜重量高、重心复杂，需要专用包装、抗震、air-ride logistics、现场 rack tug 和安装工装。
4. 铜/铝/钢和关税：busbar、机柜框架、门板、线缆管理和电气连接件受金属价格、关税和本地化采购影响。
5. 熟练工和项目管理：钣金焊接、粉末喷涂、电气装配、液冷检漏、安防接线、软件配置都需要人；AI 项目压缩交付周期，返工成本高。
6. 客户认证清单：进入 NVIDIA、Dell、HPE、Supermicro、Foxconn/Wiwynn/Quanta、hyperscaler AVL 后，切换供应商的时间成本很高；没进清单的供应商很难吃到高端订单。
7. 安防平台集成：门禁、视频、访客、柜锁、BMS、DCIM、SOC 的接口需要 OSDP Secure Channel、ONVIF、API、日志留存和网络安全认证。
8. 生物识别与隐私合规：美国州法、欧盟 GDPR、跨境数据、员工/承包商隐私都会影响 biometric deployment。
9. 现场施工窗口：机柜、围护、安防通常在白空间交付后密集进场，与电气、消防、冷却、网络施工冲突。
10. 供应链财务能力：大客户要求项目垫资、库存、定制件备货和长期服务，小厂现金流承压。

### 6.3 成本构成和毛利决定因素

| 产品 | 成本拆分 | 定价和毛利决定因素 |
|---|---|---|
| 高密度机柜 | 钢/铝/框架 30%-45%；门板/侧板/顶板/冲孔 10%-18%；导轨/脚轮/抗震件 8%-15%；锁具和线缆管理 5%-10%；人工 15%-25%；包装物流 8%-15%；质量/认证/overhead 8%-15%。 | 承重、深度、抗震、交期、是否可整柜运输、客户认证。传统毛利 15%-25%，高端定制可 30%-45%。 |
| 预集成 AI rack | 基础机柜 15%-25%；液冷歧管/QD/传感 20%-35%；busbar/power shelf brackets/cabling 15%-25%；线缆与标签 5%-10%；集成测试 15%-25%；物流 5%-10%。 | 工厂测试替代现场工时，客户愿为 time-to-token 付溢价。毛利 25%-50%。 |
| 围护/containment | 透明/金属/复合面板 25%-40%；门/框架 15%-25%；密封/刷条/五金 8%-15%；工程设计 10%-20%；现场安装 20%-35%。 | 新建 vs retrofit、定制程度、是否与 CFD/消防/运维流程绑定。毛利 25%-55%。 |
| 笼式隔离/private suite | 钢网/墙体/门 30%-45%；电子锁/读头/监控 10%-25%；安装 25%-40%；设计/合规 10%-20%。 | 多租户合规、抗入侵等级、现场安装难度。毛利 25%-60%。 |
| 机柜电子锁/智能把手 | 锁体/执行器/读头/控制板 35%-55%；软件/firmware 10%-25%；安装与接线 20%-35%；服务 5%-15%。 | 是否接入门禁平台、审计日志、OSDP/Aperio、批量部署。硬件毛利 35%-55%，软件/服务可 60%+。 |
| VMS/ACS/物理安防平台 | 摄像头/读头/控制器 35%-55%；软件许可 10%-30%；系统集成 20%-35%；维护 10%-20%。 | 开放架构、客户标准化、云/混合部署、AI analytics、证据管理。blended 35%-55%，软件 70%-85%。 |

价格传导机制：AI rack 交付一旦延误，会影响上电、GPU 验收和 token revenue，所以客户对“非 GPU 但卡交付”的小额部件价格弹性很低。机柜和物理安防占全栈 CapEx 比例不高，但一旦缺货会阻塞项目，2026-2027 高端产品可通过 expedited delivery、项目制 engineering、认证供应、保修服务和集成测试传导成本上涨。

## 7. 竞争格局与壁垒

### 7.1 市场结构

| 细分 | 集中度判断 | 头部公司 |
|---|---|---|
| 全球机柜/机架窄口径 | 中等分散，Top 10 约 45%-60%，区域小厂多。 | Schneider/APC, Vertiv/Great Lakes, Legrand/Minkels/Keydak, Eaton/Tripp Lite, Rittal, nVent, Panduit, CPI, Belden, Siemon。 |
| AI 高密整柜/预集成 | 集中度更高，Top 5 可能 55%-70%，因为需要 GPU/ODM/hyperscaler 认证。 | Vertiv, Schneider, Legrand, Eaton, Rittal, Dell, HPE, Supermicro, Foxconn, Wiwynn, Quanta。 |
| OCP/ORV3/ORW | 标准开放但客户集中，供应商份额取决于 OCP accepted 和云厂商关系。 | Rittal, Eaton, Cheval, Sanmina, AMAX, Gigabyte, Wiwynn, Meta/OCP ecosystem。 |
| 围护/containment | 项目制，区域性强，Top 10 约 40%-55%。 | Legrand/Minkels, Schneider, Vertiv, Eaton, Rittal, nVent, Panduit, CPI, Subzero Engineering, Polargy, Tate。 |
| 机柜电子锁/智能把手 | 机械锁分散，电子锁和平台接入集中度提升。 | ASSA ABLOY/HES/ABLOY/HID, Southco, dormakaba, TZ Limited, Allegion/Schlage, EMKA, DIRAK, Panduit, nVent。 |
| 数据中心物理安防平台 | 软件平台集中，硬件分散。 | Genetec, Honeywell/LenelS2/Pro-Watch, Johnson Controls/Software House/American Dynamics, Axis, Bosch, Motorola/Avigilon/Openpath, Siemens, Gallagher, AMAG, Verkada, Rhombus。 |

### 7.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 定价能力 |
|---|---|---|
| 客户认证/AVL | 机柜、液冷歧管、电子锁一旦进入 GPU 服务器 OEM、hyperscaler、colo 标准清单，替换需要重新测试、消防/CFD/运维流程验证。 | 高。客户更怕延误和返工。 |
| Rack-scale co-design | GB300、Rubin、Helios、Trainium、TPU 都是 rack/pod 级系统，机械、公差、线缆、液冷、供电、传感一起设计。 | 高。供应商参与越早，越能锁定 BOM。 |
| 规模和交付 | AI 园区需要数千到数万 rack，交期压缩；只有少数厂商能同时做钣金、液冷接口、预集成、物流和服务。 | 高。短交期和库存可直接换溢价。 |
| 认证标准 | OCP accepted、ASCE 7 seismic、UL/IEC、EN 50600、TIA-942、Uptime、OSDP、ONVIF、ISO/SOC 合规。 | 中高。标准件会降价，但合规组合仍值钱。 |
| 现场风险 | 漏液、柜体变形、线缆阻塞、锁具故障、摄像盲区都可能导致停机或安全事件。 | 高。客户会为可靠性和保修买单。 |
| 软件和审计数据 | 门禁/VMS/柜锁/访客/ALPR 一旦沉淀权限、日志、证据和流程，切换成本高。 | 很高。长期高毛利主要在软件平台和服务。 |
| 资产价值 | 单个 AI rack 服务器价值可达数百万美元，柜门/通道/视频系统的相对成本极低。 | 高。保险、审计、合规会提高配置率。 |

### 7.3 长期高 ROIC 层

最可能长期高 ROIC 的不是纯金属机柜，而是三层：

1. 机柜液冷接口、预集成整柜和 rack-scale mechanical integration：资本开支低于芯片/服务器，客户认证强，项目交付溢价高。
2. 物理安防软件平台：Genetec、LenelS2、Johnson Controls、Axis ecosystem 等通过 VMS/ACS/云/混合部署、AI analytics、证据管理获得 70%+ 软件毛利。
3. 高可靠连接与锁控硬件：quick disconnect、漏液传感、OSDP 柜锁、智能把手、anti-tailgating 传感等小部件价值占比低但失效成本极高。

## 8. 2026 关键变化：最可能发生的 3 个拐点

1. GB300/NVL72 把“机柜”升级为“rack-scale compute delivery unit”。  
   2026 H2，采购逻辑从单机柜招标转向整柜预集成、工厂测试、液冷接口和线缆管理。Vertiv/Legrand/Schneider/Eaton/Rittal 的公告都指向这个方向。

2. 机柜产能和液冷接口成为白空间瓶颈。  
   Vertiv 扩产 integrated cabinets、Legrand 收购 Keydak、nVent 扩建 Blaine 说明头部公司已把机柜/液冷接口看作供给瓶颈。高端 rack 的 lead time 会从几周拉长到数月，客户愿用溢价锁交付。

3. 物理安防下沉到柜级审计。  
   AI rack 单柜价值高、租户多、模型权重/训练数据敏感，ASSA ABLOY 等白皮书强调 cabinet-level access control 和 audit trail。2026 年 colo、金融、政府和主权 AI 会先导入。

## 9. 2027 关键变化：最可能发生的 3 个拐点

1. Rubin/MI400/TPU8/ASIC 推动 ORV3/ORW 和双宽机架放量。  
   2027 非 NVIDIA 路线为了降低供应锁定和提高 serviceability，会更积极采用 OCP/ORW。Rittal/Eaton/Cheval/Sanmina/ODM 受益。

2. 800VDC/sidecar power rack 从 reference 进入首批商业园区。  
   2026 是 GTC 展示和工程验证，2027 在 Rubin/Ultra、高密推理园区和 power-flexible AI factory 中出现早期订单。极度乐观情景下，sidecar power rack 和机柜级短时储能会成为新收入池。

3. 物理安全、BMS、DCIM、CFD、数字孪生融合。  
   NVIDIA DSX、Schneider ETAP/EcoStruxure、Vertiv digital twin、Genetec/Honeywell/Axis 的安全平台会向统一数据层靠拢。2027 采购将要求设备提供 telemetry、资产模型、审计日志和网络安全接口。

## 10. 头部公司和潜在受益名单

### 10.1 机柜、机架、整柜集成

| 公司 | 优势 |
|---|---|
| Vertiv / Great Lakes Data Racks & Cabinets | Critical infrastructure + racks + integrated cabinets + power/cooling/service；2025 年 $200M 收购 Great Lakes，2026 年美洲扩产。 |
| Schneider Electric / APC / NetShelter / Motivair | NetShelter、EcoStruxure Pod/Rack、ETAP/CFD、NVIDIA reference designs、液冷控制。 |
| Legrand / Minkels / Raritan / Server Technology / Starline / Keydak | 机柜、PDU、busway、containment、rack power；2026 收购 Keydak 和 TES，数据中心已占 2025 年底收入 26%。 |
| Eaton / Tripp Lite / Fibrebond | ORV3、rack power、prefab power enclosures、busway、800VDC 参考路径。 |
| Rittal | OCP ORV3、VX IT、DLC/RDHx、与 NVIDIA MGX rack 后门冷却合作，欧洲高端机柜强势。 |
| nVent / Hoffman / Schroff / Trachte | 保护外壳、机柜、电气连接、预制控制建筑；2026 数据中心产能扩建。 |
| Panduit | SmartZone、机柜、线缆管理、智能把手、物理层基础设施。 |
| Chatsworth Products (CPI) | ZetaFrame、高密度机柜、机柜安全和线缆管理，在 colo/enterprise 强。 |
| Belden / Siemon / Leviton | 网络机柜、结构化布线、机柜和白空间连接。 |
| Cheval / Sanmina / AMAX / Gigabyte | OCP/ORV3 rack、ODM/系统集成，适合 hyperscale 和开放 rack。 |
| Dell / HPE / Supermicro / Lenovo / Foxconn / Wiwynn / Quanta / Inventec | AI 服务器和 rack-scale 系统集成，会向机柜/液冷/白空间方案延伸。 |
| Huawei / Delta / Envicool / Inspur / Sugon ecosystem | 中国本土 AI 数据中心机柜、模块化机房、液冷和物理安防生态。 |

### 10.2 围护、containment、cages

| 公司 | 优势 |
|---|---|
| Legrand/Minkels | Cabinet + containment + rack power 组合完整，适合欧洲和全球 colo。 |
| Schneider Electric | NetShelter、EcoStruxure Pod、reference design 与 CFD。 |
| Vertiv | 白空间集成、modular/prefab、power/cooling/rack 打包。 |
| Eaton | ORV3、prefab power、rack power，与 containment/机柜配套。 |
| Rittal | ORV3/DLC、rear-door cooling、欧洲工业标准。 |
| nVent | Enclosures、保护件、电气连接和数据中心产能。 |
| Panduit / CPI / Subzero Engineering / Polargy / Tate / Kingspan | 通道围护、气流管理、raised floor、定制改造。 |
| 区域施工和金属围护厂 | Cages/private suites 多为区域项目制，小厂可凭本地安装和交期吃到高毛利。 |

### 10.3 机柜级物理安防

| 公司 | 优势 |
|---|---|
| ASSA ABLOY / HES / ABLOY / HID | 数据中心门、锁、柜锁、读卡器、凭证；HES KS server cabinet lock 支持多协议。 |
| Southco | 电子锁、latch、swinghandle、工程五金，适合机柜和工业 enclosure。 |
| dormakaba | 数据中心门禁、机柜把手锁、入口控制和全球服务。 |
| Allegion / Schlage / Von Duprin | 商业门锁、凭证、门控五金，在北美强。 |
| TZ Limited | Data Centre Cabinet Security、智能柜锁和 micro-access control。 |
| EMKA / DIRAK / Rittal / Panduit / nVent | 工业柜门锁、智能把手、机柜五金和集成件。 |

### 10.4 物理安防平台、视频、门禁、周界

| 公司 | 优势 |
|---|---|
| Genetec | Security Center，VMS/ACS/ALPR/证据管理开放架构，42,500+ 客户。 |
| Honeywell / LenelS2 / Pro-Watch / Onity | 2024 收购 LenelS2 后强化 access + video；2026 与 Rhombus 推 AI cloud video/access。 |
| Johnson Controls / Software House / American Dynamics | C-CURE、Tyco、视频/门禁/入侵生态，企业和关键设施基础强。 |
| Axis Communications | IP 摄像头、门禁、音频、analytics；数据中心方案覆盖 perimeter 到 racks。 |
| Bosch Security | 视频、入侵、门禁、消防联动。 |
| Motorola Solutions / Avigilon / Openpath | 云门禁、AI 视频、企业安全平台。 |
| Siemens | 楼宇和工业安全、OT/IT 集成，AI-ready edge/data center 解决方案。 |
| Gallagher / AMAG / Suprema / Iris ID / IDEMIA | 高安全门禁、生物识别和政府/关键基础设施。 |
| Verkada / Rhombus / Cisco Meraki | 云视频、云门禁和远程多站点管理，适合快速扩张 AI 园区。 |
| Hanwha Vision / Hikvision / Dahua | 摄像头硬件强，但美国敏感/政府/高安全数据中心受 NDAA 和安全审查限制。 |
| Boon Edam / Gunnebo / Automatic Systems / Delta Scientific / Senstar / Fiber SenSys / Optex | Mantrap、turnstile、vehicle barriers、周界探测和入侵检测。 |

## 11. 投资价值排序

| 排名 | 子方向 | 投资逻辑 | 主要风险 |
|---:|---|---|---|
| 1 | 机柜液冷接口、quick disconnect、歧管、漏液传感 | 小部件卡大项目，认证壁垒高，毛利高，随 GB300/Rubin/MI400 强绑定。 | 质量事故、被服务器 OEM 内制、标准化后降价。 |
| 2 | 预集成整柜和 AI rack integration | time-to-token 价值高，客户愿意为工厂测试和短交期付费。 | 需要营运资本和项目管理，交付失误会伤害品牌。 |
| 3 | OCP ORV3/ORW 高密机架 | 2027 开放 rack 和非 NVIDIA 平台放量，标准化带来大批量。 | 标准化后竞争加剧，毛利下行。 |
| 4 | 机柜级电子锁和物理安防软件 | 单柜价值上升，柜级审计和合规增加，软件毛利高。 | Hyperscaler 自研/自集成，隐私和网络安全问题。 |
| 5 | Cages/private suites/高安全围护 | AI colo、主权 AI 和金融政府需求强，项目制毛利高。 | 区域施工属性强，难以形成全球规模。 |
| 6 | 传统机柜和通道围护 | 需求确定，市场大。 | 竞争多、金属件毛利有限，需向高密/预集成升级。 |

## 12. 关键风险

1. GPU/HBM/CoWoS 延迟：若 Blackwell/Rubin/MI400 实际交付放慢，整柜和高密机柜订单可能推迟。
2. 电力并网和变压器拖期：机柜通常靠后交付，若园区上电延期，订单确认会后移。
3. 过度扩产：2026-2027 高端机柜短缺可能诱导小厂扩产，2028 若 AI capex 降温会价格战。
4. 标准路线分裂：19 英寸、ORV3、ORW、MGX/NVL72、云厂自定义 rack 并存，供应商押错路线会损失客户。
5. 安防隐私和网络安全：生物识别、云视频、柜锁联网带来隐私与 cyber 风险，事故会拖慢部署。
6. 中国供应链限制：低成本机柜和摄像头供应充足，但美国高安全 AI 数据中心对中国硬件审查严格。

## 13. 主要来源

| 来源 | 用途 |
|---|---|
| [Vertiv Q1 2026 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx) | Q1 销售、增长、指引、Americas demand。 |
| [Vertiv capacity expansion, Mar 2026](https://investors.vertiv.com/news/news-details/2026/Vertiv-Announces-Expansion-of-Manufacturing-Capacity-Spanning-Infrastructure-Solutions-Power-and-Rack-Systems-to-Meet-Rising-Demand/default.aspx) | Integrated cabinets 和美洲扩产。 |
| [Vertiv completes Great Lakes acquisition](https://investors.vertiv.com/news/news-details/2025/Vertiv-Completes-Acquisition-of-Great-Lakes-Data-Racks--Cabinets/default.aspx) | 约 $200M 机柜收购。 |
| [nVent 2026 Investor Day](https://investors.nvent.com/press-releases/press-release-details/2026/nVent-Highlights-Portfolio-Transformation-and-Growth-Priorities-at-2026-Investor-Day/default.aspx) | AI data center build-outs、三年增长目标。 |
| [nVent Blaine manufacturing expansion](https://investors.nvent.com/press-releases/press-release-details/2025/nVent-Expands-Data-Center-Solutions-Manufacturing-with-New-U-S--Production-Facility/default.aspx) | 117,000 平方英尺数据中心制造扩产、液冷产品。 |
| [Schneider Electric Q1 2026 revenues](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026) | €9.767B、+11.2% organic、Energy Management/data center。 |
| [Schneider Electric + NVIDIA GTC 2026](https://www.se.com/us/en/about-us/newsroom/news/press-releases/schneider-electric-teams-with-nvidia-to-develop-validated-blueprints-to-design-simulate-build-operate-and-maintain-gigawattscale-ai-factories-69b82f61aa1027e04205d273/) | Gigawatt AI factory blueprints、GB300 reference designs。 |
| [Legrand Q1 2026 results](https://www.legrand.com/en/news/2026-first-quarter-results) | +18% sales ex-FX、20.7% margin、datacenter-driven growth。 |
| [Legrand Keydak/TES acquisitions](https://www.legrand.com/sites/default/files/Documents_PDF_Legrand/Finance/2026/acquisitions/Legrand_Press%20Release_Acquisitions_April-2026_1774971744.pdf) | Keydak 机柜、TES 配电、数据中心收入占比。 |
| [Legrand Kratos/Accelsius announcement](https://www.legrand.us/about-us/newsroom/press/legrand-acquires-kratos-industries) | Critical power 和两相液冷布局。 |
| [Eaton Q1 2026 results](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html) | Electrical Americas orders/backlog、data center momentum。 |
| [Eaton + NVIDIA Beam Rubin DSX](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-collaborates-with-nvidia-to-unveil-its-beam-rubin-dsx-platform.html) | 800VDC、grid-to-chip AI factory architecture。 |
| [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) | 72 Blackwell Ultra GPU、36 Grace CPU、fully liquid-cooled rack-scale。 |
| [NVIDIA Vera Rubin DSX reference design](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-Vera-Rubin-DSX-AI-Factory-Reference-Design-and-Omniverse-DSX-Digital-Twin-Blueprint-With-Broad-Industry-Support/default.aspx) | AI factory reference design、DSX/Omniverse ecosystem。 |
| [OCP Eaton Open Rack v3](https://www.opencompute.org/products/390/eaton-open-rack-v3-orv3) | 21 英寸/19 英寸混装、ORV3 busbar、blind-mate power。 |
| [Rittal OCP EMEA Summit 2026](https://www.rittal.com/com-en/Company/Presse/Pressemeldungen/PR-RITTAL-OCP-EMEA-Summit) | ORV3、高密 rack、NVIDIA MGX rear-door cooling。 |
| [Rittal OCP ORV3 Rack](https://www.rittal.com/us-en_US/products/PG20231215ITI101/PG20240402ITI203/PRO136577?variantId=7100120) | OCP accepted、21 英寸、DLC ready。 |
| [MarketsandMarkets data center rack market](https://www.marketsandmarkets.com/Market-Reports/data-center-rack-market-210971325.html) | 2025 $5.17B 至 2030 $9.42B，CAGR 12.7%。 |
| [Grand View Research containment market](https://www.grandviewresearch.com/industry-analysis/data-center-containment-market-report) | 2024 $2.38B 至 2033 $6.92B，CAGR 12.7%。 |
| [Grand View Research data center physical security market](https://www.grandviewresearch.com/industry-analysis/data-center-physical-security-market-report) | 2025 $2.40B 至 2033 $7.27B，CAGR 15.0%。 |
| [Genetec 2026 physical security trends](https://www.genetec.com/press-center/press-releases/2025/11/genetec-predicts-top-physical-security-trends-for-2026) | 物理安防平台趋势、开放架构、IT/OT/physical convergence。 |
| [Axis data center security](https://www.axis.com/solutions/data-center-security) | 从周界到 racks 的视频/门禁/analytics。 |
| [ASSA ABLOY data center security whitepaper](https://www.assaabloy.com/tr/tr/documents/solutions/topics/access-control/Securing%20Data%20Centers%20-%20Varied%20Technologies%20and%20Exacting%20Demands.pdf) | Cabinet-level access control、audit trail、HES KS protocols。 |

非投资建议。本报告使用公开资料、项目内已有芯片/AI 数据中心建设模型和乐观情景推演，数字用于产业链研究和投资筛选，不应视为公司收入指引。
# 行业调研：【冷却液、水处理、过滤与制冷剂】

> 截至日期：2026-05-08  
> 研究口径：面向 AI 计算中心/AI Factory 的热管理流体链条，覆盖服务器侧冷却液、直液冷与浸没液、CDU/冷板相关过滤和水质、设施侧水处理/回用、冷水机组及低 GWP 制冷剂。金额为美元名义值。  
> 核心假设：对 2026-2027 年 AI 基础设施建设保持非常乐观；对找不到直接公开数据的细分品类，采用“芯片功耗/机架功率/项目 CapEx/并购估值/供应链瓶颈”交叉推导。本文不是投资建议。

## 0. 一页结论

2026 年这个行业的核心变化不是“数据中心也需要冷却”，而是 AI 机架把冷却从建筑机电的配套项，推成了算力交付的前置约束。NVIDIA GB300 NVL72 已是“fully liquid-cooled rack-scale architecture”，单柜含 72 颗 Blackwell Ultra GPU 和 36 颗 Grace CPU；项目中已有芯片路线图显示 2026 的主力是 GB300/B300、Trainium2、TPU v7 Ironwood、GB200/B200、国产 Ascend/Cambricon、MI350、Trainium3、Meta MTIA、Microsoft Maia200，2027 再由 Rubin、MI400/MI455X、TPU8、Trainium3/4 等抬升热密度。结论很直接：2026 最确定放量的是直达芯片冷板 + CDU + 二次侧过滤/水质 + 设施侧冷水/水处理，不是大规模两相浸没。

最强一手信号来自并购和产品发布。Ecolab 2026 年 3 月宣布以 47.5 亿美元收购 CoolIT，披露 CoolIT 未来 12 个月销售额约 5.5 亿美元，并把 CDUs、cold plates、liquid loops、rack manifolds 纳入水处理平台。Eaton 2025 年 11 月宣布以 95 亿美元收购 Boyd Thermal，披露 Boyd Thermal 2026 年预测销售 17 亿美元，其中 15 亿美元为液冷。Trane 2026 年 2 月宣布收购 LiquidStack，补齐 chillers、heat rejection、controls、liquid distribution、on-chip cooling。Schneider/Motivair 2026 年 1 月发布 2.5MW CDU，产品组合可扩展到 10MW 以上。Panasonic 2026 年 3 月在欧洲开始接受 400/800kW CDU 和 800/1200kW free-cooling chiller 订单。这些动作说明，巨头正在抢“chip-to-chiller / chip-to-grid / water-to-chip”的系统控制点。

我把市场分成两个口径看：窄口径液冷硬件出厂收入，Dell'Oro 预计全球数据中心液冷到 2029 年约 70 亿美元；MarketsandMarkets 报告给出的 2025 年液冷市场约 28.8 亿美元、2033 年约 276.5 亿美元，CAGR 31.5%。广义 AI 热管理订单口径则远大于此，因为它包括冷板、CDU、机架管路、泵阀、过滤、安装冲洗、冷水机组、冷却塔/干冷器、控制系统、水处理和服务。结合本项目 AI 数据中心 CapEx 模型，2026 年全球 AI 相关“冷却、流体、水处理、过滤、制冷剂与设施热管理”广义收入池基准为 450-750 亿美元，乐观为 650-1,050 亿美元，极度超预期为 900-1,450 亿美元；到 2027 年分别提高到 700-1,150 亿、1,050-1,750 亿、1,600-2,600 亿美元。这里的广义口径不能和 Dell'Oro 的制造商收入直接相加。

投资价值最强的层次并不完全等于最大收入池。长期高 ROIC 最可能在三类环节：一是与质保绑定的水/冷却液化学品、在线监测、过滤耗材、冲洗运维服务；二是高可靠快接头、盲插 manifold、漏液检测、冷板微通道清洁度这类“小部件决定大停机”的环节；三是能把冷板、CDU、chiller、water treatment、controls、服务合同打包的集成商。纯冷板和 CDU 在 2026-2027 会高增长、高溢价，但中期可能被规模制造和 ODM 议价压低毛利。

## 1. 2026 机遇、挑战与最可能技术路径

### 1.1 AI 芯片路径对冷却链条的含义

项目内已有 AI 芯片路线图显示，2026-2027 出货量和价值权重最大的 AI 平台，几乎都在把服务器热设计推向“液冷默认”：

| 芯片/平台 | 2026-2027 状态 | 对冷却液/水处理/过滤/制冷剂的直接含义 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主力放量；GB300 NVL72 为全液冷 rack-scale 架构 | 冷板、CDU、manifold、快接头、TCS 过滤和 W3/W4 温水成为刚需；设施侧冷水机组/干冷器/冷却塔容量同步上行。 |
| NVIDIA GB200/B200 | 存量订单延续，2026 仍大量交付 | 与 GB300 共用直液冷生态，早期项目会沉淀标准、运维流程和质保规则。 |
| NVIDIA Vera Rubin / Rubin | 2026 H2 首批，2027 上量 | GPU/CPU/NVSwitch 热流密度继续上升，45C 级温水、微通道冷板、嵌入式/喷射冷板开始验证。 |
| AWS Trainium2/3 | Rainier 和 Anthropic 大规模部署；Trainium3 2026 放量初期 | 大规模自用 ASIC 更重视 TCO，液冷和设施侧水/电效率强绑定，给 CDU、chiller、water treatment 带来持续需求。 |
| Google TPU v7 Ironwood / TPU8 | 2026 Ironwood 放量，TPU8 早期导入 | Google 自有数据中心能内化热设计，倾向系统级优化、再生水和设施侧水效率。 |
| AMD MI350 / MI400 Helios | MI350 2026 确定放量；MI400/MI455X 2026 H2 首批、2027 增长 | MI400/Helios rack 级液冷、HBM4 高热密度，会提高冷板和 W4 温水需求。 |
| Microsoft Maia200、Meta MTIA、OpenAI/Broadcom XPU | 2026-2027 自研 ASIC 进入独立产能池 | ASIC 放量并不削弱冷却链条，反而增加非 NVIDIA 参考设计和定制冷板机会。 |
| 中国 Ascend/Cambricon/Alibaba/Baidu | 国产替代放量，单位数量可能很大 | 风冷到液冷过渡加速，国内液冷机柜、冷板、氟化工制冷剂、水处理和过滤厂商受益。 |

### 1.2 2026 最可能技术路径

2026 年最可能的主路径是：直达芯片冷板（DTC/DLC）+ CDU + 机架 manifold/快接头 + 二次侧技术冷却系统（TCS）闭环冷却液 + 设施水系统（FWS）热交换 + chiller/free cooling/冷却塔或干冷器。原因很朴素：它兼容现有服务器形态、能被 NVIDIA/AMD/ODM 质保接受、便于分阶段改造，也能支撑 GB200/GB300/NVL72 级机架。

第二路径是水侧优化：温水液冷、free cooling、air-cooled chiller、hybrid chiller、再生水和冷却塔浓缩倍数提升。JCI 2026 年 5 月推出 AI Factory air-cooled chiller 参考设计，并强调水资源限制和热岛问题；Veolia 2026 年 4 月推出 Data Center Resource 360，提出最多降低 75% water footprint，且与 Amazon 在 Mississippi 数据中心合作用再生水替代每年超过 8,300 万加仑饮用水。

第三路径是过滤和水质运维成为“可融资的可靠性产品”。微通道冷板对颗粒、腐蚀产物、助焊剂残留、垫圈碎屑极敏感；OCP 液冷物流白皮书要求冷板运输前冲洗测试液和颗粒，以防存储和运输过程中的 fouling/scaling。过滤从冷却塔/冷冻水侧的传统旁滤，升级为 TCS 侧 <25um 级别的洁净度、在线监测、冲洗记录和质保凭证。

第四路径是低 GWP 制冷剂和制冷剂服务。美国 AIM Act HFC 配额在 2026 继续执行；EPA 已发布 2026 HFC allowance，冷库等多个制冷应用从 2026 年 1 月起进入 GWP 限制。数据中心 chiller 会向 R-1234ze、R-1233zd(E)、R-513A/R-515B、R-32/R-454B、CO2/氨等低 GWP 或自然工质组合迁移，但 A2L 安规、压缩机供应、维修人员和回收再生制冷剂会成为现实瓶颈。

### 1.3 新技术成熟与放量节奏：三情景

| 技术 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观/极度超预期 |
|---|---|---|---|---|---|
| DTC 冷板 + CDU | GB200/GB300/NVL72 主流，AI 新建高密机架 attach rate 55-70% | 70-80%，brownfield 改造加速 | 80%+，成为高端 AI 默认招标项 | 75-85% | 90-95%，冷板/CDU 从项目制转为平台件。 |
| W3/W4 温水液冷 | W3 32C 成熟，W4 45C 在高端项目验证 | GB300/Rubin 项目推动 W4 进入早期规模 | 45C 供水 + chillerless/free-cooling 在优质气候区放量 | W4 成熟、W5 55C 小规模 | W4 成为新 AI 园区标配之一，热回收可融资。 |
| 过滤/冲洗/水质在线监测 | 作为 commissioning 和质保附件放量 | 进入 CDU/TCS 标配 | 被 hyperscaler 写入统一规格 | 运维耗材收入加速 | 成为 SLA 和保险条款的一部分。 |
| 单相浸没 | 小规模 HPC、边缘、特殊高密场景 | OCP 标准化推进，PFAS-free 流体更可用 | 部分云厂商新建 pod 试点 | 仍是细分高增长 | 若 PFAS-free 流体、维护和服务器可服务性过关，2027 H2 放量。 |
| 两相浸没 | PFAS/Novec 退场后处于再验证 | Chemours/Syensqo/新材料方案做试点 | 非 PFAS 两相流体若通过可靠性验证，订单前置 | 仍不作主流假设 | 2028 前更像高风险期权，不是 2026 主线。 |
| 低 GWP 制冷剂 chiller | 新项目逐步切换，R-410A/R-134a 存量服务继续 | HFO/低 GWP chiller 交付顺畅 | 制冷剂短缺推升 ASP 和回收再生价值 | 低 GWP 成为新 chiller 默认 | 制冷剂回收、泄漏监测、A2L 安规培训放量。 |
| 再生水/近零排放水处理 | 水紧张地区项目制 | AWS/Veolia 类模板复制 | 当地审批把水回用写入准入条件 | 规模化包年服务 | “water-positive” 成为大型园区融资和社区许可工具。 |

## 2. 已经开始放量的关键产品

口径说明：下表为全球 AI 数据中心新增/改造项目相关“年化收入池”估计，3 个月指 2026-08 左右滚动订单/交付节奏，1 年指 2027-05，2 年指 2028-05。产品之间有系统集成重叠，不能简单相加。

### 2.1 放量产品的市场规模、渗透率、增长和毛利率

| 已放量产品 | 当前状态与证据 | 未来 3 个月市场规模 | 1 年市场规模 | 2 年市场规模 | 渗透率路径 | 增长预测 | 毛利率/利润率情景 |
|---|---|---:|---:|---:|---|---|---|
| DTC 冷板、液冷模组、manifold、快接头、软管/管路 | GB300 全液冷；Boyd 2026 预测液冷销售 15 亿美元；CoolIT 被 Ecolab 收购 | 基准 20-35 亿；乐观 35-55 亿；极度 55-80 亿 | 基准 120-220 亿；乐观 220-360 亿；极度 360-550 亿 | 基准 220-380 亿；乐观 400-700 亿；极度 700-1,100 亿 | AI 高密机架 2026Q3 55-75%，2027 75-90%，2028 85-95% | 基准年增 45-65%，乐观 70-100%，极度 100%+ | 冷板/组件基准 28-38%；乐观 38-50%；极度供不应求 50-60%。快接头/密封件可更高。 |
| CDU、泵阀、板换、控制系统 | Schneider/Motivair 2.5MW CDU；Panasonic 2026 欧洲接单 400/800kW CDU；Trane/Ecolab/Eaton 均补齐 CDU | 基准 15-30 亿；乐观 30-50 亿；极度 50-75 亿 | 基准 80-160 亿；乐观 160-280 亿；极度 280-450 亿 | 基准 150-280 亿；乐观 300-550 亿；极度 550-900 亿 | 2026Q3 45-70%，2027 65-85%，2028 80-95% | 基准 50-70%，乐观 75-110%，极度 110%+ | CDU 基准 25-35%；乐观 35-48%；极度 45-58%。工程安装服务 20-35%。 |
| 水/乙二醇或 PG25 类二次侧冷却液、缓蚀剂、杀菌剂 | DTC 主流冷却液仍以处理水/PG 或乙二醇体系为主；Castrol PG25 获 OCP Inspired | 基准 1.5-3.5 亿；乐观 3.5-6 亿；极度 6-10 亿 | 基准 8-18 亿；乐观 18-35 亿；极度 35-60 亿 | 基准 18-40 亿；乐观 40-80 亿；极度 80-140 亿 | 新 AI 液冷 loop 首充 60%+，运维补液/检测逐季上升 | 基准 35-55%，乐观 60-90%，极度 100%+ | 基准 35-50%；乐观 50-65%；极度 60-75%，尤其是 OEM 认证配方。 |
| 冷却液过滤、冲洗、旁滤、颗粒监测、水质传感器 | OCP/Parker 物流白皮书强调冷板冲洗去颗粒；Donaldson、Tekleen、Lakos、Sani-Matic 等推出数据中心方案 | 基准 2-5 亿；乐观 5-8 亿；极度 8-12 亿 | 基准 12-28 亿；乐观 28-50 亿；极度 50-80 亿 | 基准 30-65 亿；乐观 65-120 亿；极度 120-200 亿 | 2026 从 commissioning 附件进入标准件；2027 成为 TCS 质保项 | 基准 50-80%，乐观 80-120%，极度 120%+ | 过滤硬件 30-45%；耗材/监测/服务 45-70%。 |
| 设施侧水处理、再生水、RO/UF/MBR、冷却塔化学品、ZLD | Veolia/Amazon Mississippi 再生水项目，预计每年替代 8,300 万加仑饮用水；Xylem/GWI 称 AI 价值链水需求到 2050 +129% | 基准 4-10 亿；乐观 10-18 亿；极度 18-30 亿 | 基准 25-55 亿；乐观 55-100 亿；极度 100-160 亿 | 基准 50-110 亿；乐观 110-220 亿；极度 220-350 亿 | 水紧张地区 2026 先行；2027 大型园区审批前置 | 基准 25-45%，乐观 50-80%，极度 80%+ | 化学品/服务 25-45%；膜/设备 25-40%；数字化运维 40-60%。 |
| Air-cooled/water-cooled/hybrid chiller、free cooling、干冷器/冷却塔 | JCI 推 AI Factory chiller design；Panasonic 接单 free-cooling chiller；Trane/Carrier/Daikin/LG/JCI 均发布数据中心冷却方案 | 基准 30-60 亿；乐观 60-95 亿；极度 95-140 亿 | 基准 150-300 亿；乐观 300-500 亿；极度 500-750 亿 | 基准 250-500 亿；乐观 500-900 亿；极度 900-1,400 亿 | 所有 AI 园区均需热排放；液冷提高设施水温但不消灭 heat rejection | 基准 20-35%，乐观 35-55%，极度 55%+ | 大型 chiller 25-38%；磁悬浮/低 GWP/定制数据中心方案 35-50%；服务 40%+。 |
| 低 GWP 制冷剂、回收再生、泄漏检测、A2L 安规服务 | EPA 2026 HFC allowance；AIM Act 推动替代；R-454B/R-32/HFO 供应链转换 | 基准 2-4 亿；乐观 4-7 亿；极度 7-12 亿 | 基准 8-18 亿；乐观 18-35 亿；极度 35-60 亿 | 基准 15-35 亿；乐观 35-70 亿；极度 70-120 亿 | 新 chiller 低 GWP 渗透率 2026 35-55%，2027 55-75%，2028 70-90% | 基准 20-40%，乐观 40-70%，极度受短缺/法规驱动 70%+ | 传统 HFC 15-30%；HFO/专利低 GWP 35-60%；回收再生在短缺期可 40-65%。 |

### 2.2 2026 最确定的产品组合

2026 年最可能成为主线的不是单一“液冷概念股”，而是一整套项目包：

1. 服务器冷板 + 盲插 manifold + 快接头 + leak detection。
2. 机架/列级/房间级 CDU，容量从几百 kW 进入 1-2.5MW，多个 CDU 组成 10MW+ 控制系统。
3. TCS 闭环冷却液，配套缓蚀剂、杀菌剂、导电率/pH/颗粒在线监测。
4. 过滤、冲洗、氮气封存、现场填充、验收测试和运维耗材。
5. 设施侧冷水、free cooling、air-cooled/hybrid chiller 和低 GWP 制冷剂。
6. 再生水/回用水处理，特别是水权紧张、社区反对较强的美国州和欧洲市场。

## 3. 在研和即将快速增长的关键技术

### 3.1 在研产品与放量路径

| 在研/早期放量技术 | 当前证据 | 3 个月市场规模 | 1 年市场规模 | 2 年市场规模 | 渗透率路径 | 毛利率情景 |
|---|---|---:|---:|---:|---|---|
| PFAS-free dielectric cold-plate fluid / 单流体 DTC | Perstorp Synplate DC、Synmerse DC；Castrol OCP Inspired；OCP 生态推动 | 基准 0.5-1.5 亿；乐观 1.5-3 亿；极度 3-6 亿 | 基准 3-10 亿；乐观 10-25 亿；极度 25-50 亿 | 基准 15-40 亿；乐观 40-90 亿；极度 90-180 亿 | 2026 小批验证，2027 进入敏感行业/边缘/高可靠场景，2028 有望成为差异化路线 | 基准 45-60%；乐观 60-75%；极度 70%+，但认证成本高。 |
| PFAS-free 单相浸没液 + 标准化 tank/pod | OCP immersion requirements；Shell/Intel/Submer case；3M 已退出 PFAS 制造 | 基准 2-6 亿；乐观 6-12 亿；极度 12-20 亿 | 基准 10-35 亿；乐观 35-80 亿；极度 80-150 亿 | 基准 40-120 亿；乐观 120-250 亿；极度 250-450 亿 | 2026 仍 niche；2027 若服务器可维护性和材料兼容过关，边缘/HPC/云局部上量 | 设备 30-45%；流体 40-65%；运维 40%+。 |
| 非 PFAS 两相浸没流体 | Novec/fluorinated legacy 被监管压制；替代化学仍需可靠性验证 | 基准 <0.5 亿；乐观 0.5-1.5 亿；极度 1.5-4 亿 | 基准 1-5 亿；乐观 5-15 亿；极度 15-40 亿 | 基准 5-25 亿；乐观 25-80 亿；极度 80-200 亿 | 2026-2027 更像技术期权；若非 PFAS、高安全、高沸点窗口打开，2028 才可能大放量 | 极高壁垒可 55-80%，但合规和责任风险也最高。 |
| 4kW+ 微喷射/3D 微通道/嵌入式冷板 | Frore LiquidJet 等方案瞄准 4kW+；Rubin Ultra/Feynman 级热流密度需要新冷板 | 基准 1-3 亿；乐观 3-6 亿；极度 6-10 亿 | 基准 7-20 亿；乐观 20-50 亿；极度 50-100 亿 | 基准 20-80 亿；乐观 80-180 亿；极度 180-350 亿 | 2026 工程样机，2027 Rubin/MI400 后续高端 SKU 带动，2028 规模化 | 基准 35-50%；乐观 50-65%；极度 65%+。 |
| W4/W5 温水、chillerless、热回收 | OCP ASHRAE W4=45C、W5=55C；JCI/Trane/Daikin/Alfa Laval 推高温/热回收方案 | 基准 5-15 亿；乐观 15-30 亿；极度 30-50 亿 | 基准 40-100 亿；乐观 100-200 亿；极度 200-350 亿 | 基准 100-250 亿；乐观 250-550 亿；极度 550-900 亿 | 2026 试点，2027 新建 AI 园区标准化，气候友好地区最快 | 设备 25-40%；软件/控制/服务 40-60%。 |
| 模块化再生水/近零液体排放/水正效益服务 | Veolia containerized reclaimed water + Amazon；社区和投资者要求披露水足迹 | 基准 1-4 亿；乐观 4-8 亿；极度 8-15 亿 | 基准 10-40 亿；乐观 40-90 亿；极度 90-160 亿 | 基准 40-120 亿；乐观 120-300 亿；极度 300-500 亿 | 2026 项目制，2027 审批刚需化，2028 园区级服务合同化 | 设备 25-40%；服务/运营/数字化 35-60%。 |
| 自动补液机器人、数字孪生冷却控制、AI 水质控制 | OCP 2025 展示自动补液机器人；Vertiv 2026 Frontiers 强调 adaptive liquid cooling 和 digital twins | 基准 0.5-2 亿；乐观 2-5 亿；极度 5-10 亿 | 基准 5-20 亿；乐观 20-50 亿；极度 50-100 亿 | 基准 20-70 亿；乐观 70-160 亿；极度 160-300 亿 | 2026 先在 hyperscaler 试点，2027 与 SLA/保险/运维平台绑定 | 软件/控制 50-75%；硬件 25-45%。 |

### 3.2 哪些技术会最快增长

最快增长的不是“最科幻”的两相浸没，而是三个看起来普通但很硬的环节：

第一，过滤/冲洗/水质监测。它的基数小、质保相关性强、耗材属性好，一旦冷板微通道堵塞或腐蚀，损失不是一套过滤器，而是整柜 GPU 可用性。

第二，W4 温水 + free cooling / hybrid chiller。AI 园区的电力和水权审批会越来越难，能减少 chiller 运行小时、减少蒸发耗水或用热回收换许可的方案，会从 ESG 叙事变成项目落地工具。

第三，PFAS-free dielectric fluids。3M 已在 2025 年底完成 PFAS 制造退出，传统 Novec/Fluorinert 路线被迫迁移。PFAS-free 单相流体和介电冷板流体如果通过 OEM 材料兼容、介电、消防、长期老化验证，毛利和认证壁垒都会很高。

## 4. 供给侧：产能、瓶颈、成本与价格传导

### 4.1 产能集中地区与公司

| 环节 | 主要产能地区 | 代表公司 |
|---|---|---|
| 冷板、液冷模组、manifold、快接头 | 北美、台湾、中国大陆、欧洲；高端冷板靠近 OEM/ODM 与芯片客户协同 | Boyd Thermal/Eaton、CoolIT/Ecolab、nVent、Auras、AVC、Delta、Foxconn、Quanta、Wiwynn、Inventec、Supermicro、Dell、HPE、Lenovo、JetCool、Chilldyne、ZutaCore |
| CDU、泵阀、板换、控制 | 美国、欧洲、日本、台湾、中国 | Schneider/Motivair、Vertiv、Eaton/Boyd、Trane/LiquidStack、Panasonic、Delta、Rittal、STULZ、Airedale/Modine、CoolIT、Alfa Laval、Danfoss、Kelvion、Grundfos、Xylem |
| 冷却液/浸没液/添加剂 | 美国、欧洲、日本、中国氟化工基地 | Castrol/BP、Shell、Perstorp、Ecolab/Nalco、Dober、Engineered Fluids、Chemours、Honeywell、Arkema、Syensqo/Solvay、Fuchs、TotalEnergies、Lubrizol、巨化、三美、永和、东岳 |
| 水处理与回用 | 全球本地化工程和服务网络 | Veolia、Ecolab/Nalco、Xylem/Evoqua、Kurita、Solenis、DuPont Water、Pentair、Danaher/ChemTreat/Pall、Aquatech、Gradiant、IDE、Ovivo、碧水源、沃顿科技、三达膜 |
| 过滤与洁净度控制 | 美国、欧洲、中国、以色列、日本 | Donaldson、Parker、Pall/Danaher、Eaton Filtration、Pentair、3M、Amiad、LAKOS、Tekleen、Sani-Matic、Cool Filtration、AALfilter、Alfa Laval、Porvair、Mott |
| Chiller、CRAH、冷却塔、干冷器 | 美国、欧洲、日本、韩国、中国 | Carrier、Trane、Johnson Controls/York、Daikin、Mitsubishi Electric、LG、Panasonic、STULZ、Airedale/Modine、Vertiv、Schneider、Munters、SPX/Marley、Baltimore Aircoil、Evapco、Guntner、格力、美的、海尔、申菱、英维克 |
| 制冷剂和回收再生 | 美国、欧洲、日本、中国、印度；HFO 技术集中度更高 | Honeywell、Chemours、Arkema、Daikin、Koura/Orbia、AGC、Dongyue、Juhua、Sanmei、Yonghe、Sinochem、A-Gas、Hudson Technologies |

### 4.2 供给瓶颈

1. 冷板制造良率：微通道加工、钎焊/扩散焊、平面度、翘曲、热阻、流阻、helium leak test 和批量一致性决定交付。
2. 快接头和密封件：盲插、低压降、低泄漏、耐 PG/乙二醇/介电液、反复插拔寿命和微颗粒脱落都需要验证。
3. CDU 核心件：高可靠泵、板式换热器、VFD、传感器、控制器、阀组、冗余设计和 UL/CE 认证可能成为瓶颈。
4. 冷却液认证：pH、电导率、缓蚀剂、材料兼容、消防、毒理、介电、长期氧化稳定性；一旦进入 OEM 质保清单，切换周期通常 6-18 个月。
5. 现场冲洗和洁净施工人才：冷板和 manifold 在运输、安装、切换过程中残留颗粒会造成堵塞；commissioning 记录会成为质保凭证。
6. 水权和排污许可：冷却塔补水、blowdown、再生水接入、ZLD 和化学品排放审批会影响项目开工。
7. Chiller 和制冷剂供应：磁悬浮压缩机、低 GWP 制冷剂、A2L 安规、维修人员培训和回收再生制冷剂都会影响交期。
8. 客户集中和固定价格合同：hyperscaler 议价强，但供应紧缺时会用预付款、长期框架协议和工程服务锁产能。

### 4.3 成本结构和毛利决定因素

| 产品 | 单位成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 冷板/液冷模组 | 铜/铝/不锈钢材料 20-35%；加工/焊接/镀层 25-35%；测试/清洗 10-20%；工程设计 10-20%；良率损耗 5-15% | 是否绑定 GPU/ASIC 参考设计；热阻/压降；漏率；批量良率；客户质保 | 新芯片代际前 2-4 季度溢价强，后续 ODM/EMS 规模化压价。 |
| CDU | 泵/板换/阀组/电控 45-60%；机柜/管路 10-20%；软件/传感 5-10%；装配测试 15-25% | MW 级容量、冗余、控制软件、服务网络、认证 | 项目交期越紧，越能向客户传导；多 MW 标准化后毛利回落。 |
| 冷却液/添加剂 | 基础液 30-60%；添加剂包 10-25%；认证/测试 10-20%；包装物流 5-15% | OEM 认证、寿命、材料兼容、PFAS-free/低毒、可追溯批次 | 初装液 + 补液 + 检测服务，价格以 SLA 和质保清单传导。 |
| 过滤/冲洗 | 滤芯/膜/外壳 30-45%；传感器/仪表 10-20%；工程 skid 20-30%；服务 15-30% | 过滤精度、压降、寿命、在线监测、维护便利性 | 耗材复购和 commissioning 刚性强，价格对停机损失不敏感。 |
| 水处理/回用 | 预处理/膜/树脂 25-40%；药剂 10-25%；土建/管道/水箱 20-30%；运维 15-30% | 当地水价、水权、排污标准、回用率、数字化运营能力 | 通过水许可、节水目标和 O&M 合同传导，项目越难获批，服务溢价越高。 |
| Chiller/热排放 | 压缩机/换热器/风机 50-65%；控制和电力电子 10-20%；制冷剂 2-8%；安装服务 15-25% | 能效、低 GWP、可靠性、快速重启、噪音、水耗、交期 | 客户按 PUE/WUE/交期采购，长交期时设备商可提高价格。 |
| 制冷剂 | 原料和合成 40-60%；配额/合规 10-25%；包装物流 5-15%；渠道 10-20% | HFO 专利、HFC 配额、回收再生能力、A2L 适配 | 法规和短缺直接推动 ASP，服务端回收再生价格弹性大。 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

液冷硬件正在从碎片化走向巨头整合。CoolIT、Boyd、LiquidStack、Motivair 这类专业厂商，在 2025-2026 被 Ecolab、Eaton、Trane、Schneider 分别收入体系，意味着未来头部会围绕“集成能力 + 全球交付 + 客户认证”集中。冷板和 CDU 的 CR5 在 2026 仍不算绝对垄断，但 hyperscaler 关键项目的合格供应商名单会非常短；我估算高端 AI DTC 冷板和 CDU 的项目可见份额中，前 8-10 家可覆盖 65-80%。

水处理和制冷剂本来就是集中行业。Ecolab/Nalco、Veolia、Xylem/Evoqua、Kurita、Solenis、DuPont 等在水化学、膜、服务网络上长期积累；Honeywell、Chemours、Arkema、Daikin、Koura、AGC 以及中国巨化/三美/永和/东岳在制冷剂和氟化工上具备配额、工艺、法规和客户认证壁垒。

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| OEM 认证和质保绑定 | 冷却液、冷板、快接头、过滤器一旦进入服务器或 GPU 平台认证，客户切换会触发重新验证、停机、冲洗和质保风险。 |
| 漏液风险非线性 | 一只快接头或垫圈的价格很小，但泄漏可能造成整柜数百万美元 GPU 停机，客户愿意为可靠性和保险买单。 |
| 微通道清洁度 | 颗粒堵塞会提升热阻、触发降频或故障；过滤和冲洗服务的价值来自避免停机，不是材料成本。 |
| 规模制造和良率 | 冷板需要高精度加工和 100% 测试；能稳定交付百万级冷板的厂商比能做样机的厂商少很多。 |
| 全球工程服务 | AI 园区项目跨国复制，客户需要同一供应商在北美、欧洲、亚洲提供设计、安装、运维和备件。 |
| 水权/排污/社区许可 | 能提供再生水、节水、ZLD 和披露数据的厂商，帮助客户拿到项目许可，服务价值高于设备价值。 |
| HFC/PFAS 法规 | 低 GWP 制冷剂、PFAS-free 流体、回收再生制冷剂都有法规驱动，合规供应商获得稀缺溢价。 |
| 系统级优化 | chip-to-chiller 的控制能力能降低 PUE/WUE 和泵功耗，节省的电费和上电容量可被供应商分享。 |

### 5.3 长期价值捕获

长期高毛利/高 ROIC 最可能在四层：

1. 认证型流体和化学服务：冷却液、水处理药剂、在线监测、补液、实验室检测、数字化水管理，具备耗材和服务复购。
2. 高可靠连接和洁净度：快接头、盲插 manifold、密封、过滤、冲洗 skid、颗粒传感，单价小但故障成本巨大。
3. 集成控制平台：CDU、chiller、泵、阀、水质、漏液、热回收的控制软件，越靠近 SLA 越有粘性。
4. 低 GWP 制冷剂和回收再生：配额、专利、法规和回收网络带来定价权，但政策风险也高。

冷板和 CDU 2026-2027 的收入弹性最大，但如果没有认证、设计、运维和服务闭环，2028 后可能从高毛利工程件走向 ODM 化硬件。

## 6. 2026 关键变化：三大拐点

1. Blackwell Ultra/GB300 让“液冷默认”落地。NVIDIA 官方 GB300 NVL72 是全液冷 rack-scale 架构，Supermicro、Dell 等 OEM 已将液冷 AI rack 和 Rubin 后续平台列入 2026 交付。2026 的主战场是能否把冷板/CDU/过滤/现场服务标准化交付。

2. 巨头并购改变竞争边界。Ecolab-CoolIT、Eaton-Boyd、Trane-LiquidStack、Schneider-Motivair 不是财务并购，而是水处理、电力、HVAC 巨头把液冷作为 AI 数据中心核心入口。2026 起，客户更愿意采购“可质保的全栈热管理”，小型单品供应商要么被收购，要么绑定大厂渠道。

3. 水和化学法规进入项目经济。Veolia/Amazon 再生水项目、Xylem/GWI 的 AI 水需求研究、EPA HFC 2026 allowance、3M 退出 PFAS 制造，共同把水处理、低 GWP 制冷剂、PFAS-free coolant 从 ESG 主题推成审批和供应链主题。

## 7. 2027 关键变化：三大拐点

1. Rubin/MI400/TPU8 把冷却从 1kW 级 GPU 推向 1.8kW-3kW+ 封装热管理。W4 45C 温水、微喷射/嵌入式冷板、4kW+ 热设计会从实验室走向高端 SKU 导入。

2. 过滤和水质成为 SLA 条款。2026 早期液冷项目的经验会暴露颗粒、腐蚀、微生物、材料兼容和现场冲洗问题；2027 起，过滤精度、冷却液批次、冲洗记录、在线监测会成为保险、质保和客户验收的一部分。

3. 水正效益/零水冷却成为园区许可工具。美国部分地区电力和水权紧张，欧洲又更重视热回收和资源循环。2027 新园区很可能把再生水、air-cooled/hybrid chiller、热回收、WUE 披露写入规划条件。

## 8. 头部公司和细分技术清单

### 8.1 全栈热管理与机电集成

Vertiv、Schneider Electric/Motivair、Eaton/Boyd Thermal、Trane Technologies/LiquidStack、Carrier、Johnson Controls/York、Daikin/Daikin Applied、STULZ、Rittal、Legrand、Delta Electronics、Huawei Digital Power、Munters、Modine/Airedale、LG Electronics、Panasonic、Mitsubishi Electric、Lennox、Nortek、Danfoss。

### 8.2 直液冷冷板、CDU、液冷服务器和 rack 集成

CoolIT Systems/Ecolab、Boyd Thermal/Eaton、LiquidStack/Trane、Motivair/Schneider、nVent、Vertiv、Delta、Auras、Asia Vital Components、Nidec、JetCool、Chilldyne、ZutaCore、Asetek、LiquidCool Solutions、Supermicro、Dell、HPE、Lenovo Neptune、Foxconn/Industrial Fii、Quanta、Wiwynn、Inventec、Gigabyte、ASUS、H3C、Inspur、Sugon、Huawei、浪潮信息、联想、新华三、中科曙光、工业富联。

### 8.3 浸没冷却与介电流体

Submer、LiquidStack、Asperitas、GRC、Midas Immersion Cooling、Iceotope、ZutaCore、TMGcore、ExaScaler、Shell、Castrol/BP、Perstorp、Engineered Fluids、Chemours、Syensqo/Solvay、3M legacy Novec/Fluorinert、Dober、Fuchs、TotalEnergies、Lubrizol、SuperLiq。

### 8.4 水处理、膜、回用和化学服务

Ecolab/Nalco Water、Veolia、Xylem/Evoqua、Kurita、Solenis、DuPont Water Solutions、Pentair、Danaher/ChemTreat/Pall、SUEZ、Aquatech、Gradiant、IDE Technologies、Ovivo、LG Water Solutions、Toray、Hydranautics/Nitto、碧水源、沃顿科技、三达膜、久吾高科、中持股份、景津装备。

### 8.5 过滤、冲洗、颗粒控制和密封连接

Donaldson、Parker Hannifin、Pall/Danaher、Eaton Filtration、Pentair、3M、Amiad、LAKOS、Tekleen、Sani-Matic、Cool Filtration、AALfilter、Alfa Laval、Porvair、Mott、Graver、Hayward、Shelco、Schroeder、Parker/CPC、Stäubli、CEJN、Swagelok、Victaulic、Gates、Trelleborg、Freudenberg、Danfoss、Kelvion。

### 8.6 制冷剂、chiller 和热排放

制冷剂/氟化工：Honeywell、Chemours、Arkema、Daikin、Koura/Orbia、AGC、Dongyue Group、Juhua、Sanmei、Yonghe、Sinochem、Mexichem legacy、A-Gas、Hudson Technologies、Airgas。

Chiller/冷却塔/干冷器：Carrier、Trane、Johnson Controls/York、Daikin、Mitsubishi Electric、LG、Panasonic、STULZ、Airedale/Modine、Vertiv、Schneider Electric、Munters、SPX Cooling/Marley、Baltimore Aircoil、Evapco、Guntner、Alfa Laval、Kelvion、Smardt、Kaltra、格力、美的、海尔、申菱环境、英维克、佳力图、依米康、海鸥股份、盾安环境、三花智控。

## 9. 投资框架：哪些环节更值得跟踪

| 优先级 | 环节 | 投资逻辑 | 需要跟踪的指标 |
|---:|---|---|---|
| 1 | 认证型冷却液/水处理/过滤耗材 | 高复购、与质保绑定、客户切换成本高 | OEM 认证数量、数据中心客户数、服务合同、耗材收入占比、毛利率。 |
| 2 | 快接头、manifold、密封、漏液检测 | 小部件决定大停机，定价权强 | 盲插良率、压降、漏率、材料兼容、随 GB300/Rubin/MI400 平台导入情况。 |
| 3 | CDU 和冷板平台供应商 | 2026-2027 最大高 beta 收入池 | 订单/产能/交期、MW 级 CDU SKU、冷板产能、客户集中度、并购估值。 |
| 4 | Chiller/free cooling/热排放 | 所有热最终都要排出去，水电约束提高价值 | 数据中心订单、低 GWP chiller 占比、air/hybrid chiller、快速重启、噪音和水耗指标。 |
| 5 | 制冷剂和回收再生 | AIM Act 和低 GWP 切换带来价格和配额弹性 | HFC allowance、HFO 产能、A2L 供应、回收再生价格、客户库存。 |
| 6 | 水回用/水正效益工程 | 审批和社区许可约束下的确定性增长 | 再生水项目数量、年节水量、WUE 披露、长期 O&M 合同。 |

最强组合是“硬件 + 流体 + 服务 + 监测”。单独做冷板/机柜可能高增长但容易被压价；单独做化学品如果没有 OEM 和现场服务，也难进入质保名单。Ecolab 收 CoolIT 的意义就在于把水化学、数字监测和冷板/CDU 工程结合起来；Eaton 收 Boyd 的意义在于 power + liquid cooling；Trane 收 LiquidStack 的意义在于 central plant + liquid-to-chip。

## 10. 主要风险

1. AI 数据中心项目因电力、融资、社区和水权延迟，导致 2026 订单确认不及预期。
2. 冷板/CDU 产能扩张过快，2027 后价格从短缺溢价转向竞争性报价。
3. 液冷早期项目出现漏液、腐蚀、颗粒堵塞或材料不兼容事故，拖慢客户验收。
4. PFAS-free 和低 GWP 流体性能不及预期，或法规变化导致库存减值。
5. Hyperscaler 自研规格提高议价权，压缩中游硬件毛利。
6. 水处理项目本地化强，工程交付和许可周期长，不能简单按全球 TAM 外推。

## 11. 参考来源

### 一手公司公告、产品和监管

- NVIDIA GB300 NVL72 官方页面：<https://www.nvidia.com/en-gb/data-center/gb300-nvl72/>
- Vertiv Q1 2026 results：<https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx>
- Vertiv Q4 2025 results / organic orders +252%：<https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/>
- Schneider/Motivair 2.5MW CDU：<https://www.se.com/us/en/about-us/newsroom/news/press-releases/Motivair-by-Schneider-Electric-announces-new-CDU-with-capability-to-scale-to-10MW-and-beyond-for-nextgen-AI-Factories-69705c3655f8517e99086bbd/>
- Ecolab acquiring CoolIT Systems：<https://www.ecolab.com/news/2026/03/ecolab-to-acquire-coolit-systems-a-global-leader-in-advanced-liquid-cooling-for-next-gen-ai-data-ce>
- Trane acquiring LiquidStack：<https://ir.tranetechnologies.com/news-and-events/news-releases/news-release-details/2026/Trane-Technologies-to-Acquire-LiquidStack-to-Accelerate-EndtoEnd-Data-Center-Thermal-Management-Solutions/default.aspx>
- Eaton acquiring Boyd Thermal：<https://www.eaton.com/us/en-us/company/news-insights/news-releases/2025/eaton-signs-agreement-to-acquire-boyd-thermal--expanding-solutio.html>
- Johnson Controls AI Factory cooling guide：<https://www.johnsoncontrols.com/media-center/news/press-releases/2026/05/05/johnson-controls-releases-second-data-center-reference-design-guide-to-advance-industrialscale-ai-fa>
- Panasonic Europe CDU/free-cooling chiller order launch：<https://news.panasonic.com/global/press/en260304-2>
- Dell AI Factory with NVIDIA 2026：<https://investors.delltechnologies.com/news-releases/news-release-details/dell-ai-factory-nvidia-delivers-proven-path-enterprise-ai-roi>
- Castrol ON OCP Inspired cooling fluids：<https://www.castrol.com/en/global/corporate/about-castrol/newsroom/castrol-on-ocp.html>
- Perstorp PFAS-free data center cooling fluids：<https://www.perstorp.com/en/products/engineered_fluids_solutions/thermal_management_fluids/innovative_solutions_for_data_center_cooling>
- 3M PFAS manufacturing exit：<https://www.3m.com/3M/en_US/pfas-stewardship/operations-innovation/>
- EPA HFC allowances：<https://www.epa.gov/climate-hfcs-reduction/hfc-allowances>
- EPA Technology Transitions HFC restrictions：<https://www.epa.gov/climate-hfcs-reduction/technology-transitions-hfc-restrictions-sector>
- Veolia/Amazon reclaimed water for cooling：<https://www.veolia.com/sites/g/files/dvc4206/files/document/2026/04/Finance_PR_Amazon_Veolia_04-27-2026.pdf>
- Veolia Data Center Resource 360：<https://www.veolia.com/sites/g/files/dvc4206/files/document/2026/04/pr-data-centers-new-offer-041426.pdf>
- Xylem/GWI AI water demand research：<https://prod.xylem.com/en-bb/about-xylem/newsroom/press-releases/ais-water-demand-to-surge-nearly-130-by-2050--new-research-shows-how-to-build-a-water-secure-ai-economy/>

### 标准、报告与技术资料

- Dell'Oro liquid cooling market to approach $7B by 2029：<https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html>
- MarketsandMarkets Data Center Liquid Cooling Market 2026-2033：<https://www.marketsandmarkets.com/Market-Reports/data-center-liquid-cooling-market-84374345.html>
- OCP ACS Immersion Requirements：<https://www.opencompute.org/documents/ocp-acs-immersion-requirements-specification-1-pdf>
- ASHRAE TC 9.9 Water-Cooled Servers white paper：<https://www.ashrae.org/File%20Library/Technical%20Resources/Bookstore/WhitePaper_TC099-WaterCooledServers.pdf>
- Parker/OCP Liquid Cooling Integration and Logistics white paper：<https://www.parker.com/content/dam/parker/fcg/group/data-centers/OCP%20Liquid%20Cooling%20Integration%20and%20Logistics%20White%20Paper%20Revision%201.0%20%281%29.pdf>
- Precedence Research data center chiller market：<https://www.precedenceresearch.com/press-release/data-center-chillers-market>
- AALfilter data center liquid cooling filtration：<https://www.aalfilter.com/blog/industry-news/why-data-centers-need-filtration/>
- Donaldson data center coolant filtration skid：<https://info.donaldson.com/en-amer-data-centers.html>
- Tekleen data center filtration and dewatering strategy：<https://www.prweb.com/releases/tekleen-responds-to-growing-data-center-water-concerns-with-full-flow-filtration-and-dewatering-strategy-302697294.html>
- ASHRAE Journal cold plates overview：<https://www.ashrae.org/technical-resources/ashrae-journal/featured-articles/september-2025-liquid-cooling-cold-plates>

### 本项目内参考

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
# 行业调研：【数据中心UPS与电池储能】

> 版本日期：2026-05-08  
> 研究口径：美元计价；B = 十亿美元；MW/GW 为 IT 负载或电力容量，除非另有说明。  
> 核心假设：对 2026-2027 年 AI 计算中心建设保持非常乐观，且把“UPS-only 市场”和“AI 数据中心 UPS+BESS+电能质量/并网订单池”分开测算。传统第三方 UPS 市场报告通常只统计 UPS 系统收入或投资额，低估了 AI 园区里正在变成标配的站侧 BESS、grid-interactive UPS、负载平滑、LVRT、EMS/软件和预制化电力模块。

## 0. 结论先行

数据中心 UPS 与电池储能在 2026 年的投资主线不是“备用电源替换”，而是“AI 工厂的电力波动管理和 time-to-power 工具”。GB300/Blackwell Ultra、TPU、Trainium、MI350/MI400、Ascend、MTIA、Maia 等平台在 2026-2027 年把机柜功率、集群同步负载波动、建设周期和并网约束同时推高，UPS 从低频故障保险，升级为“毫秒-秒级电能质量 + 分钟级桥接 + 小时级站侧储能 + 电网交互”的组合。

最可能放量的 2026 技术路径：1MW 级模块化在线 UPS + 锂电池柜、10-40MW 预制化电力 block、站侧 LFP BESS/Megapack 式 AC 耦合储能、grid-to-chip 监控软件、以及少量飞轮/旋转 UPS 做高功率短时桥接。VRLA 继续存在但主要在存量/低成本/监管保守场景。800VDC、机架级储能、超级电容、钠离子、镍锌会在 2026 年开始进入可见订单或验证，但大规模收入更可能在 2027 年后。

市场规模的关键差异：Grand View Research 的数据中心 UPS 口径为 2024 年 40.4 亿美元、2030 年 62.7 亿美元；Arizton 的“UPS investment”口径为 2024 年 88.9 亿美元、2030 年 207.5 亿美元。项目内美国 AI 数据中心模型更适合本报告的投资口径：美国 AI 数据中心 UPS/BESS/电能质量订单池 2026 年基准为 180-300 亿美元，2027 年基准为 280-450 亿美元。向全球外推后，2026 年 AI 相关 UPS+BESS+电能质量订单池可看 300-550 亿美元；乐观为 550-850 亿美元；极度超预期为 850-1,250 亿美元。2027 年全球区间可进一步上移到 500-850 亿美元、850-1,350 亿美元、1,350-2,000 亿美元。

价值捕获排序：第一层是 Schneider/Vertiv/Eaton/ABB/Delta/Huawei 这类能交付 UPS、开关柜、母线、配电、BMS、DCIM、服务和预制电力模块的综合电力链厂商；第二层是 Tesla/Fluence/Sungrow/CATL/BYD/Power Electronics 等站侧 BESS 与 PCS/EMS 厂商；第三层是 ZincFive、Natron/钠离子、超级电容、飞轮/动态 UPS 等高功率短时储能技术。如果 2026 下半年 AI 园区并网瓶颈继续加剧，长期 ROIC 最高的不是单一电芯，而是“可被 AHJ、保险商、超大客户和 EPC 一次性接受的整套电力架构”。

## 1. 2026 机遇、挑战与技术路线

### 1.1 一手信号：订单已经落到电力层

2026 年外部一手资料显示，AI 基础设施需求已经明确传导到 UPS、电气化、BESS 和预制化电力模块：

| 来源 | 关键事实 | 对 UPS/储能的含义 |
|---|---:|---|
| Eaton Q1 2026 | Electrical Americas 数据中心订单同比约 +240%，收入约 +50%；Electrical Americas backlog 同比 +44%；Eaton 推出与 NVIDIA Rubin DSX/Omniverse 相关的 grid-to-chip power blueprint | 数据中心订单不是泛泛而谈，已经进入 Eaton 电力产品和工程 backlog；2026-2027 预制化、模块化、NVIDIA 参考架构兼容产品会被优先采购 |
| Schneider Electric Q1 2026 | Q1 收入 97.67 亿欧元， organic +11.2%；Energy Management +12.8%；Systems +16%；Data Center & Networks 需求和销售均双位数增长，北美和中国/东亚强 | Schneider 的强项是端到端 offer、prefab、配电、冷却、ETAP/EcoStruxure，说明客户更愿意买“系统”而非单台 UPS |
| ABB Q1 2026 | Electrification 订单 66.47 亿美元， comparable +44%，book-to-bill 1.44，backlog 115 亿美元；数据中心订单“三位数”增长 | ABB 低压/中压配电、开关设备、动态电力质量、自动化正在被 AI 数据中心拉动 |
| Vertiv Q1 2026 | Q1 净销售 26.5 亿美元，同比 +30%；2026 全年指引净销售 135-140 亿美元、organic +29%-31%；Americas organic +44% | Vertiv 是最纯的关键数字基础设施 beta 之一，UPS/thermal/integrated rack/服务能力一起受益 |
| Delta DCW 2026 | 披露美国数据中心 UPS 装机 6.5GW+，UZR3 Li-ion Battery Cabinet 全球 footprint 3GW+；DPM Gen-2 UPS 250-2500kVA，最高 97.5% double conversion 效率，可扩到 20MW N+1；展示 800VDC 架构，最高 1.1MW/rack、98% 效率 | 锂电 UPS 柜与高密度 UPS 已经不是概念；800VDC 和 rack power shelf 是 2027 的高弹性方向 |
| Tesla Megapack for Data Centers | 官方材料把 Megapack 定位为 AI 数据中心的负载平滑、LVRT、降低并网压力、站侧 backup 和可再生消纳工具；示例 4 台 Megapack 3 XL 为 4.8MW/21.4MWh | BESS 进入数据中心不是为了替代 UPS，而是把并网/波动/备用从成本中心变成可调度资产 |
| Fluence Q1 FY2026 | Q1 收入 4.752 亿美元，同比 +154.4%；签单 7.5 亿美元+，backlog 约 55 亿美元；管理层称数据中心、公共事业和工业负载推动储能需求，pipeline 自 2025 年 9 月以来增至约 300 亿美元 | 专业 BESS integrator 已经把数据中心视为储能需求的核心驱动之一 |
| Uptime Institute 2026 | 2021-2025 年公开宣布的 >100MW 数据中心园区项目 377 个；2025 年新增 proposal power 181.2GW；AI 驱动约 60%；北美占 2025 proposal power 的 80%；Uptime 认为实际会有约 25% planned provisioned power 被活跃使用 | 即使只兑现 25%，UPS+BESS+配电链条的订单增量也足以超出传统 UPS 报告 |

### 1.2 项目内 AI 芯片假设对电力架构的映射

本报告不对 2026/2027 出货量最大的 AI 芯片做外部搜索，采用项目内文件 `ai_chip_research_2026_2027.md` 的平台假设。核心结论是：GPU/ASIC 订单越集中到整 rack/整 pod/整 campus，电力系统越从“按楼配置”变成“按 AI factory 单元配置”。

| AI 平台/芯片 | 2026-2027 本地假设摘要 | 对 UPS 与储能的电力含义 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主平台，2027 仍大量交付 | NVL72/GB300 级别机柜和 pod 需要高密度 UPS、母线、48V/高压 DC 转换、液冷协同；集群同步训练造成站侧瞬时波动 |
| AWS Trainium2 | Rainier 级项目、百万芯片级扩张假设 | 超大云厂自建区域更倾向标准化电力 block、站侧 BESS、长期 PPA 和 grid-interactive 控制 |
| Google TPU v7 Ironwood | Google Cloud/Anthropic 等需求，百万级扩张假设 | Google 对电网/可再生/储能软件经验深，BESS 和 UPS 调度的概率高 |
| NVIDIA B200/GB200 | 2026 仍有大交付 | 仍是大量新建和改造项目的主力负载，推动锂电 UPS 替代 VRLA |
| Huawei Ascend 910C/950PR/950DT | 中国 AI 算力主线 | 华为 FusionPower/SmartLi、国产 UPS、电池和配电链条受益，交付节奏受本土供应链和园区审批影响 |
| Cambricon MLU 590/690 | 2026 出货乐观假设可到数十万片 | 中国/东南亚区域的国产 UPS、锂电柜、模块化数据中心需求扩散 |
| AMD MI350X/MI355X | 2026 放量，云客户和主权 AI 需求 | 与 NVIDIA 相比生态更分散，电力链会更多由 ODM/EPC/整机厂共同定义 |
| AWS Trainium3 | 2026 H2/2027 early，144-chip UltraServer 方向 | 进入更高 rack power 和更高同步波动，拉动 2027 机架级缓冲和站侧 BESS |
| Meta MTIA 300/400/450/500 | 自研 ASIC + Broadcom 大电力订单背景 | 超大客户有能力把 UPS/BESS 设计内生化，供应商要进入其参考架构 |
| Microsoft Maia 200 | Azure 自研 AI 加速器迭代 | 微软已有 grid-interactive UPS 实践，2026-2027 可能继续推动 UPS 参与电网服务 |
| Alibaba/T-Head Zhenwu | 中国云厂自研平台 | 中国 UPS、SmartLi、液冷、电池柜和预制模块协同放量 |
| AMD MI400/MI455X Helios | 2026 H2 early，2027 弹性大 | 若 2027 放量，800VDC/高压 DC/机架级电能缓冲弹性最大 |

### 1.3 当前正在使用的技术

| 技术 | 当前状态 | 优势 | 主要挑战 | 2026 判断 |
|---|---|---|---|---|
| 双变换在线 UPS + VRLA | 最成熟、存量最大 | 认证成熟、初始 capex 低、AHJ 熟悉 | 占地大、寿命短、维护重、AI 负载高循环不友好 | 存量维护和保守项目继续，新 AI 白区占比下降 |
| 双变换/eco mode UPS + Li-ion 电池柜 | 已经规模化 | 占地小、寿命长、可高温运行、维护少、TCO 优 | UL9540A/NFPA855/保险和热失控测试要求高 | 2026 新建 AI 项目最确定放量路线 |
| 模块化 UPS 500kVA-2.5MVA | 已经规模化 | 快速扩容、热插拔、标准化、适配 10-40MW power block | 功率模块、测试产线、现场调试瓶颈 | 2026 主力产品 |
| 预制化电力模块/power skid | 快速放量 | 缩短工期、减少现场 labor、可复制 | 上游变压器/开关柜/运输/现场吊装 | 2026 高增长，毛利好于单机 |
| 站侧 LFP BESS | 公用事业成熟，数据中心快速渗透 | 负载平滑、LVRT、削峰、并网缓解、备用桥接 | 与生命安全 UPS 的边界、消防审批、调度责任 | 2026 从 optional 变成大型园区强推荐 |
| Grid-interactive UPS | 已有验证案例 | UPS 电池从闲置资产变可调度资产，软件高毛利 | 电网规则、客户风险偏好、SOC 保证 | 2026 选择性采用，2027 放量 |
| 飞轮 UPS/动态旋转 UPS | 成熟 niche | 高功率、超长寿命、无化学电池、秒级桥接 | 能量时长短、机械维护、噪音/空间 | 高可靠/高功率场景保持增长 |
| 镍锌电池 | 商业化早期 | 高功率、安全、无钴镍锂依赖、适合 UPS 短时 | 供应商集中、成本和长期现场数据 | 2026 开始放量，2027 弹性大 |
| 钠离子电池 | 早期商业化/不确定 | 安全、低温、无锂资源约束、高循环潜力 | 银行信用、产能、实际成本曲线、认证 | 2026 pilot，2027 有超预期可能 |
| 超级电容/机架级储能 | 试点/小规模 | 毫秒级响应、极高循环、适合 AI transient | 成本、能量密度、系统集成标准 | 2026 验证，2027 与 800VDC/rack power 绑定 |
| 800VDC/高压 DC 配电 | 展示/试点 | 降转换损耗、支撑 MW/rack、减少铜耗 | 标准、安全、断路/eFuse、运维体系 | 2026 demo，2027 小规模工程化 |

### 1.4 技术成熟与放量时间：三情景

| 技术/产品 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|
| Li-ion UPS 电池柜 | 2026 H1 已放量，2026 H2 成新建 AI 默认之一；2027 渗透 60%-75% | 2026 年渗透 60%-70%；2027 达 75%-85% | 2026 H2 因 VRLA 占地/维护被快速替换，2027 渗透 85%-92% |
| MW 级模块化 UPS | 2026 全年主力；2027 继续由 1MW 走向 1.5-2.5MW block | 客户标准化 power block，2026 订单增速 40%-70% | 2026 因超大订单造成 2-4 季度交期紧张和溢价 |
| 预制化 grid-to-chip 电力模块 | 2026 快速提升到 AI 新建项目 40%-55% attach | 2026 H2 大客户把其作为标准设计，2027 attach 70%-85% | 2026 年成为抢 time-to-power 的核心手段，综合电气厂毛利上修 |
| BTM LFP BESS/ Megapack 式系统 | 2026 大型园区 attach 18%-30%；2027 30%-45% | 2026 30%-45%；2027 45%-65% | 2026 H2 并网瓶颈恶化，BESS attach 45%-65%，2027 达 65%-80% |
| Grid-interactive UPS | 2026 试点/少量区域，attach 5%-10% | 2026 H2 在电力紧张市场落地 10%-18% | 2027 前形成高毛利软件/调度收入，attach 35%-50% |
| 飞轮/旋转 UPS | 2026 稳定增长，渗透 5%-12% | 高可靠项目提升到 12%-18% | 化学电池消防约束导致 niche 扩大，2027 18%-25% |
| 镍锌 UPS 电池 | 2026 从低个位数到 6%-12% | 2027 达 15%-28% | 若头部 hyperscaler 认证通过，2027 可达 28%-40% |
| 钠离子 UPS/短时储能 | 2026 pilot | 2027 小规模量产 | 2027 因安全/成本/供应链突破成为锂电补充 |
| 超级电容/机架级缓冲 | 2026 机柜/电源架构验证 | 2027 与 Rubin/MI400/Trainium3 等高密度平台联动 | 2027 进入 rack BOM 或 power shelf 标准件，毛利极高 |
| 800VDC/固态变压器/DC-only | 2026 展示/少量工程样板 | 2027 有限新建区 adoption | 若 NVIDIA/Delta/Eaton/Vertiv 参考架构被 hyperscaler 采纳，2027 从小批量跃迁为设计标准 |

## 2. 已开始放量的关键产品：市场规模、渗透率、增长与毛利

### 2.1 口径说明

下表为“全球 AI 数据中心相关订单口径”，包括新建和大规模改造项目中的 UPS、本体电池柜、站侧 BESS、PCS、EMS、预制化电力模块、软件和服务。它不是传统 UPS-only 市场。传统 UPS-only 2026 年全球大约在 60-120 亿美元区间，取决于统计口径；AI 相关订单池则因 BESS/预制化/电能质量/服务被纳入而显著放大。

### 2.2 已放量产品测算表

| 产品/技术 | 现有放量证据 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 增长预测 | 产品毛利率情景 |
|---|---|---:|---:|---:|---|---|---|
| MW 级模块化在线 UPS（500kVA-2.5MVA） | Eaton 数据中心订单 +240%；Delta DPM Gen-2 250-2500kVA；Schneider Galaxy VXL 500-1250kW；Vertiv/ABB/Huawei 均有高端产品 | 基准 20-40 亿；乐观 30-55 亿；极度 55-85 亿 | 基准 90-140 亿；乐观 140-220 亿；极度 220-320 亿 | 基准 140-230 亿；乐观 220-360 亿；极度 360-550 亿 | 新建 AI UPS attach：2026 75%-88%，2027 80%-95% | 2026 YoY +25%-60%；极度 +80%+ | 基准 24%-34%；乐观 30%-40%；极度 34%-45% |
| Li-ion UPS 电池柜（LFP/NMC） | Delta UZR3 全球 footprint 3GW+；Vertiv EnergyCore；Huawei SmartLi；Schneider/Eaton lithium cabinets | 基准 10-18 亿；乐观 16-26 亿；极度 24-38 亿 | 基准 50-80 亿；乐观 80-120 亿；极度 120-180 亿 | 基准 80-130 亿；乐观 130-220 亿；极度 220-350 亿 | 新建 AI UPS 电池房：2026 45%-70%，2027 60%-92% | 2026 +35%-90%；极度供不应求 | 基准 24%-34%；乐观 30%-40%；极度 36%-48% |
| 预制化电力模块/PowerPod/Power skid（UPS+开关柜+母线+控制） | Schneider Systems +16%、数据中心 complete offer；Eaton grid-to-chip blueprint；Huawei FusionPower6000；Vertiv AI factory blocks | 基准 30-55 亿；乐观 55-85 亿；极度 85-125 亿 | 基准 120-200 亿；乐观 200-320 亿；极度 320-480 亿 | 基准 220-380 亿；乐观 380-650 亿；极度 650-950 亿 | AI 新建项目 attach：2026 40%-70%，2027 55%-92% | 2026 +40%-100%；极度 +120% | 基准 22%-32%；乐观 28%-38%；极度 32%-44% |
| 站侧 LFP BESS/Megapack 式系统（0.5-4h） | Tesla AI 数据中心材料；Fluence backlog 55 亿美元/pipeline 300 亿美元；Uptime 披露大型园区开始配置 battery storage | 基准 15-30 亿；乐观 30-60 亿；极度 60-100 亿 | 基准 70-120 亿；乐观 120-220 亿；极度 220-400 亿 | 基准 140-280 亿；乐观 280-550 亿；极度 550-1,000 亿 | 大型 AI campus attach：2026 18%-45%，2027 30%-80% | 2026 +50%-150%；极度 +200% | 硬件基准 10%-18%；乐观 14%-24%；极度 18%-30%；软件 40%-70% |
| Grid-interactive UPS/EMS/电能质量软件 | Eaton EnergyAware/Microsoft Dublin 案例；Schneider ETAP/EcoStruxure；Tesla/Fluence 软件栈；Vertiv 360AI | 基准 1-2.5 亿；乐观 2.5-5 亿；极度 5-9 亿 | 基准 5-12 亿；乐观 12-25 亿；极度 25-50 亿 | 基准 20-40 亿；乐观 40-80 亿；极度 80-150 亿 | 2026 attach 5%-18%；2027 12%-50% | 小基数 +80%-200% | 基准 45%-65%；乐观 55%-75%；极度 60%-82% |
| 飞轮 UPS/旋转 UPS/动态 UPS | Piller、Hitec、Active Power、ABB 等成熟装机；电池消防和高功率桥接需求提升 | 基准 3-7 亿；乐观 6-11 亿；极度 10-18 亿 | 基准 13-25 亿；乐观 25-45 亿；极度 45-80 亿 | 基准 25-50 亿；乐观 50-90 亿；极度 90-160 亿 | AI 新建中 5%-18%，高可靠/化学电池受限项目更高 | 2026 +10%-45% | 基准 25%-35%；乐观 30%-42%；极度 35%-48% |
| 传统 VRLA UPS 电池/维护 | 存量规模巨大；低 capex 和 AHJ 熟悉 | 基准 8-15 亿；乐观 10-18 亿；极度 12-22 亿 | 基准 35-55 亿；乐观 45-70 亿；极度 60-90 亿 | 基准 55-85 亿；乐观 70-105 亿；极度 90-130 亿 | 新 AI 项目渗透下降，但存量替换稳定 | 收入低个位数至 +15%，利润由维护支撑 | 基准 15%-25%；乐观 18%-28%；极度 20%-32% |

### 2.3 已放量产品的利润率判断

短期毛利的核心不是“电芯涨价”，而是认证、交付和系统责任。单电芯价格可能下行，但通过 UL9540A/NFPA855、与 UPS/PCS/BMS 联调、可被保险商接受、能在客户 witness test 中一次通过的产品会获得更高价格。2026 年最容易出现溢价的环节是：1）MW 级 UPS 功率模块和测试产能；2）UL9540A/UL1973/NFPA855 证据链完整的锂电池柜；3）预制化电力模块的工程交付槽位；4）grid-interactive UPS 的控制软件和生命周期服务；5）大型 AI campus 的 BESS EMS/并网控制。

## 3. 在研和未来快速增长的关键产品

| 产品/技术 | 当前阶段 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 增长与放量触发 | 产品毛利率情景 |
|---|---|---:|---:|---:|---|---|---|
| 镍锌 UPS 电池（NiZn） | ZincFive 等已经商业化，2026 survey 显示认知度提升 | 基准 1.5-4 亿；乐观 4-8 亿；极度 8-15 亿 | 基准 8-16 亿；乐观 16-32 亿；极度 32-60 亿 | 基准 20-40 亿；乐观 40-80 亿；极度 80-140 亿 | 2026 3%-12%；2027 8%-40% | 大客户认证、消防优势、AI dynamic power 能力被验证 | 基准 30%-45%；乐观 38%-52%；极度 45%-60% |
| 钠离子 UPS/短时储能 | Natron/HiNa/Tiamat/Faradion 等技术路径，银行信用分化 | <1 亿；乐观 1-2 亿；极度 2-4 亿 | 基准 2-8 亿；乐观 8-20 亿；极度 20-40 亿 | 基准 10-30 亿；乐观 30-80 亿；极度 80-150 亿 | 2026 pilot；2027 3%-15%，极度 20%+ | 产能、认证、循环寿命、成本低于 LFP 或安全溢价 | 基准 20%-35%；乐观 30%-45%；极度 40%-55% |
| 机架级储能/超级电容/Power Capacitance Shelf | 2026 AI transient 需求显性化；Delta/ZincFive 等披露相关方向 | 基准 1-3 亿；乐观 3-8 亿；极度 8-18 亿 | 基准 5-15 亿；乐观 15-40 亿；极度 40-100 亿 | 基准 20-50 亿；乐观 50-120 亿；极度 120-250 亿 | 2026 <5%；2027 在高密 rack 中 10%-35% | Rubin/MI400/Trainium3/TPU 机柜波动、800VDC 架构、eFuse 标准 | 基准 35%-55%；乐观 45%-65%；极度 55%-75% |
| 800VDC/高压 DC 配电和固态变压器 | Delta 展示 800VDC；学术/产业开始 RTDS 仿真；NVIDIA DSX/Rubin 带动 | 基准 0.5-2 亿；乐观 2-5 亿；极度 5-12 亿 | 基准 3-10 亿；乐观 10-30 亿；极度 30-70 亿 | 基准 20-60 亿；乐观 60-150 亿；极度 150-350 亿 | 2026 demo；2027 高密新建区 5%-20% | 标准、断路保护、运维培训、OEM 参考设计 | 基准 30%-50%；乐观 40%-60%；极度 50%-70% |
| BESS+燃气/燃料电池/微电网控制 | 数据中心 off-grid/混合供电方案上升；Uptime 报告显示天然气、太阳能、battery storage 同时出现 | 基准 5-15 亿；乐观 15-30 亿；极度 30-60 亿 | 基准 30-80 亿；乐观 80-180 亿；极度 180-350 亿 | 基准 100-250 亿；乐观 250-600 亿；极度 600-1,200 亿 | 大型 campus attach：2026 5%-25%；2027 15%-55% | 并网排队、气轮机交付、PPA、容量市场和可靠性要求 | 硬件 15%-30%；控制/软件 40%-70% |
| 长时储能（flow/iron-air/LDES） | 非 UPS 主路径，适合园区韧性/能源套利 | 可忽略至 1 亿 | 基准 1-5 亿；乐观 5-15 亿；极度 15-35 亿 | 基准 10-30 亿；乐观 30-80 亿；极度 80-150 亿 | 2027 后小规模，非关键负载优先 | 4-100h backup、燃料限制、可再生占比、容量市场 | 基准 15%-30%；乐观 25%-40%；极度 35%-50% |
| UPS-as-a-grid-asset 金融化 | 技术已可行，商业模式早期 | <1 亿 | 基准 2-8 亿；乐观 8-20 亿；极度 20-40 亿 | 基准 10-40 亿；乐观 40-100 亿；极度 100-200 亿 | 由电力市场规则决定 | UPS/BESS 参与频率响应、需求响应、容量服务，客户降低 TCO | 软件/服务 50%-80% |

未来两年最值得跟踪的“非共识高弹性”是机架级瞬态缓冲和 800VDC。理由是，传统 UPS/BESS 解决的是楼宇/园区电能质量，而 AI 训练负载的同步变化可能发生在 rack/pod 级；如果高密度 rack 从 100kW 进入 300kW-1MW，系统会需要更靠近负载的毫秒级能量缓冲。该环节一旦进入参考设计，价值捕获接近 GPU 电源供应链里的高端功率器件，毛利和壁垒都高。

## 4. 供给侧：产能、瓶颈、成本与价格传导

### 4.1 产能结构

| 区域 | 主要公司/能力 | 强项 | 短板 |
|---|---|---|---|
| 北美/墨西哥 | Vertiv、Eaton、Schneider NA、ABB NA、Tesla Megapack、Fluence、Generac、Powell、IEM、nVent、Legrand/Starline、ZincFive | 超大客户近场交付、服务网络、UL/NFPA/AHJ 经验、数据中心 EPC 协同 | 变压器/开关柜/熟练电工/现场调试排队，成本高 |
| 欧洲 | Schneider、ABB、Siemens、Socomec、Riello UPS、Piller、Hitec、Saft、Legrand | 旋转 UPS、低压/中压配电、工业电气标准、服务 | 能源价格、工厂扩产速度、部分项目审批 |
| 中国大陆/台湾 | Huawei Digital Power、Delta、Kehua、KSTAR、INVT、Sungrow、CATL、BYD、EVE、Hithium、CALB、Narada、Shoto、Sinexcel、NR Electric、HyperStrong | 锂电/PCS/BESS 成本与产能、快速工程化、国产 AI 园区配套 | 出口认证、地缘/关税、北美 AHJ/保险准入 |
| 韩国/日本 | Samsung SDI、LG Energy Solution、Panasonic、GS Yuasa、Mitsubishi Electric、Fuji Electric、Toshiba | 高质量电芯、UPS/工业电气、长期客户信任 | 成本和扩产速度弱于中国，系统集成覆盖较分散 |
| 印度/东南亚 | Schneider、Delta、Vertiv、Huawei、ABB、local panel builders、电池组装 | 数据中心增长快、区域制造迁移 | 本地认证/施工能力不均、关键部件仍依赖进口 |

### 4.2 至少 10 个供给瓶颈

1. 通过数据中心安全认证的锂电池柜产能：不是普通 LFP 电芯短缺，而是电芯、BMS、柜体、消防、热失控测试、UPS 联调、客户 AVL 全部打通的“可用柜”短缺。
2. UL1973、UL9540、UL9540A、NFPA855、LSFT、当地 AHJ 与保险审批：室内电池房、间距、通风、探测、灭火、热失控传播测试都可能拖慢交付。
3. 大功率 IGBT/SiC 模块、磁性件、薄膜电容、高压接触器、断路器、eFuse 和母排：UPS 和高压 DC 的核心电子材料。
4. 中压变压器、开关柜、断路器和保护继电器：UPS 可以生产出来，但 upstream electrical gear 不到位，机房仍无法通电。
5. 工厂 FAT、客户 witness test、现场 SAT 槽位：AI 客户会对 MW 级 UPS/BESS 做严格测试，测试台和工程师成为瓶颈。
6. 消防/热管理工程人才：电池柜/BESS 需要把电气、热、消防、建筑 code 同时做对，人才比硬件更缺。
7. Cybersecurity 和控制软件认证：grid-interactive UPS/EMS 涉及远程控制、并网和关键负载，需要 UL2900-1、IEC62443 等证据。
8. 现场 commissioning 技术员和高压电工：预制模块减少现场施工，但最终并网、调试、保护定值、黑启动测试仍依赖熟练人员。
9. 新化学体系的 bankability：镍锌/钠离子/长时储能若没有可融资 warranty、保险接受和现场数据，无法进入核心负载。
10. 并网研究、保护方案和电力市场规则：BESS 和 UPS 想参与 grid services，需要 utility 批准、计量、SOC 约束和调度协议。
11. 运输和吊装：大型 BESS、预制 power room、液冷/电力模块体积和重量大，受道路、港口、现场 crane 资源影响。
12. 客户标准化锁定：一旦 hyperscaler 定义了参考架构，二供/三供必须跟随其接口和测试流程，非标供应商进入周期长。

### 4.3 BOM/单位成本拆分

| 产品 | 成本构成估算 | 毛利决定因素 |
|---|---|---|
| MW 级模块化 UPS 本体 | 功率模块/IGBT/SiC 25%-35%；磁性件/电容 15%-22%；柜体/母排/断路器 15%-20%；控制器/HMI/软件 5%-10%；测试/质量 5%-8%；人工/物流/服务 10%-15%；warranty/overhead 8%-12% | 功率密度、效率、冗余架构、模块热插拔、认证、交付周期、服务网络 |
| Li-ion UPS 电池柜 | 电芯 45%-60%；BMS/接触器/熔断器 8%-15%；柜体/热管理/消防探测 10%-18%；集成测试 8%-12%；物流/warranty 8%-15% | 电芯采购、热失控测试、与 UPS 兼容、室内布置合规、寿命和 warranty |
| 站侧 BESS | 电芯 35%-50%；PCS/逆变器/变压器 15%-25%；热管理/消防/柜体 10%-15%；EMS/软件 5%-10%；EPC/并网/调试 15%-25% | 电芯成本、PCS 并网能力、grid-forming、项目风险、软件调度价值、国内内容要求 |
| 预制化 power module | UPS/开关柜/母线/电池/控制 55%-70%；工厂集成和测试 10%-18%；结构件/机柜/HVAC/fire 8%-15%；物流吊装 5%-10%；项目管理 5%-10% | 标准化设计、工厂产能、EPC 协同、交期、一次通过率 |
| 飞轮/旋转 UPS | 转子/电机/发电机 30%-45%；功率电子 15%-25%；真空/磁悬浮/轴承 10%-18%；控制/柜体/测试 15%-25%；服务/warranty 8%-15% | 可靠性、服务合同、机械寿命、与发电机桥接能力 |
| Grid-interactive 软件/EMS | 研发与云平台 25%-40%；现场集成 15%-25%；网络安全/认证 10%-20%；销售/服务 20%-30% | 调度收益分成、客户风险偏好、并网协议、算法和设备闭环 |

### 4.4 价格传导机制

2026 的价格传导是“交期优先”而非“原材料优先”。当客户的 AI 芯片、土地、PPA 和 EPC 都已锁定，UPS/BESS 如果延迟 3-6 个月，机会成本可能远高于硬件涨价 5%-15%。因此头部供应商具备三类涨价能力：第一是 expediting premium，即加急交付和工厂测试槽位；第二是 certified system premium，即通过 AHJ/保险和客户 AVL 的整套系统；第三是 lifecycle service premium，即 24/7 维护、远程监控、预测性维护和电网调度。电芯成本下降会被部分传导给客户，但在 2026 的 AI 园区项目中，系统集成和认证溢价会抵消大部分电芯降价。

## 5. 竞争格局、壁垒与价值捕获

### 5.1 市场结构

传统高端数据中心 UPS 的全球头部高度集中。综合第三方报告和供应商装机，Schneider/APC、Vertiv、Eaton 通常是欧美高端数据中心 UPS 的第一梯队，ABB、Huawei、Delta、Socomec、Piller、Riello、Kehua、KSTAR 在区域或细分技术中强势。高功率 AI 项目中，前三家在北美/欧洲高端客户中的合计份额可粗略看 45%-60%；加入 ABB/Delta/Huawei 后，全球前六在高端数据中心 UPS/电力链中的份额可看 65%-80%。

BESS 则更分散。Tesla、Fluence、Wartsila、Sungrow、CATL、BYD、Powin、Hithium、EVE、LGES Vertech、Samsung SDI、Saft、Nidec、GE Vernova、HyperStrong 等均具备项目机会。数据中心场景会比普通公用事业 BESS 更看重 bankability、并网控制、消防和服务，因此最终会从“电芯低价竞争”向“可被 hyperscaler 接受的系统供应商”集中。

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 定价逻辑 | 可量化指标 |
|---|---|---|
| 安全/认证壁垒 | UL1973/UL9540/UL9540A/NFPA855/IEC62040 等一旦进入设计和许可证，替换会重新触发测试和审批 | 认证周期 6-18 个月；AHJ 审批失败会导致项目延期 |
| 客户 AVL 和参考架构 | Hyperscaler 标准化后，供应商需要通过长期可靠性、接口、远程监控和服务测试 | 进入 AVL 后可跨园区复制；退出成本高 |
| 服务网络 | 数据中心停机损失巨大，客户愿意为 4 小时响应、备件、远程诊断付费 | 服务 attach rate、MTTR、备件覆盖城市数 |
| 工厂测试与交付产能 | MW 级 UPS/BESS 需要 FAT、witness test、SAT；交付槽位稀缺时可溢价 | backlog、book-to-bill、lead time、FAT 一次通过率 |
| 系统集成能力 | UPS、开关柜、母线、BESS、冷却、DCIM、保护继电器、发电机必须联动 | 单 MW capex、工期压缩、现场 labor 减少比例 |
| 并网/电力市场能力 | Grid-interactive UPS/BESS 需要 utility 认可和可审计控制，软件可抽成 | MW 可调容量、年化调度收益、SOC 可用率 |
| 保险和融资 bankability | 电池系统若被保险商/贷款方接受，可降低项目资本成本 | warranty 年限、保险费率、项目融资可得性 |
| 规模采购 | 头部厂商锁定 IGBT/SiC、电芯、断路器、变压器和铜材，保障交期 | 原材料框架协议、产能扩张 capex、库存周转 |
| 运维数据 | 历史故障和热数据越多，预测性维护和 warranty 定价越准 | 装机 GW、运行小时、故障数据库 |

### 5.3 长期高 ROIC 层级

长期高 ROIC 最可能在综合电力链和软件服务层，而不是单一电芯。UPS/BESS 电芯可能周期化，PCS 也可能竞争加剧；但一套经过认证的 grid-to-chip 架构一旦进入客户标准，可在多个园区复制，并带来 10-20 年服务收入。综合厂商同时出售 UPS、配电、开关柜、母线、监控、服务、软件和预制模块，可把单次设备销售变成生命周期合约。软件层如果能把 UPS/BESS 变成可调度资产，毛利可达 50%-80%，但商业化受电力市场规则约束。

价值捕获优先级：1）Schneider/Vertiv/Eaton/ABB/Delta/Huawei 这种综合 power train；2）Tesla/Fluence/Sungrow/CATL/BYD/Power Electronics 等 bankable BESS+PCS+EMS；3）ZincFive、Piller/Hitec、Natron/HiNa、超级电容等高功率短时储能；4）纯电芯和普通柜体制造商，除非具备认证和系统入口。

## 6. 2026 关键变化：三个最可能拐点

### 6.1 锂电 UPS 成为 AI 新建项目默认选项

2026 年 Li-ion UPS 的胜负手是占地和维护。AI 数据中心的电力和冷却空间极贵，VRLA 占地、重量、维护和寿命劣势放大。Delta 披露 UZR3 Li-ion Battery Cabinet 全球 footprint 3GW+ 且通过关键安全测试，说明锂电柜已进入成熟采购期。基准情景下，2026 新建 AI UPS 电池房 Li-ion 渗透率达到 45%-60%；乐观为 60%-70%；极度超预期可达 70%-80%。

### 6.2 BESS 从备用电源变成并网和负载平滑工具

AI 训练负载会产生快速功率摆动；并网排队和电网稳定性也使大型园区必须在站侧配置可控资源。Tesla 官方把 Megapack 用例明确放在 AI 数据中心负载平滑、LVRT、降低并网依赖和 backup；Fluence 管理层也把数据中心增长列为储能 demand driver。2026 年大型 AI campus 的 BESS attach 基准为 18%-30%，乐观 30%-45%，极度 45%-65%。

### 6.3 Grid-to-chip 参考架构成为销售方式

Eaton Beam Rubin DSX、Vertiv 360AI/NVIDIA GTC、Delta 800VDC grid-to-chip、Schneider complete offer 都指向同一变化：客户不再单独采购 UPS、配电、冷却和监控，而是按 AI factory block 采购。2026 年赢家是能把灰空间和白空间、电力和冷却、UPS 和 BESS、工程和软件一次性交付的厂商。

## 7. 2027 关键变化：三个最可能拐点

### 7.1 Grid-interactive UPS/BESS 从试点走向常规收入

到 2027 年，如果电力紧张、容量市场和需求响应机制继续扩张，UPS/BESS 的经济性会从“避免停机”扩展到“降低总电力成本和并网成本”。Microsoft/Eaton/Enel X 的 Dublin 经验说明 UPS 参与电网服务在技术上可行；2027 关键是 SOC 管理、客户可用性担保和 utility 规则标准化。软件和服务收入会是高毛利弹性来源。

### 7.2 Rack/pod 级短时储能和 800VDC 开始进入设计标准

2027 年 Rubin、MI400/MI455、Trainium3、TPU 下一代平台若按项目内乐观出货，机柜功率和动态负载会进一步上升。站侧 UPS/BESS 可以平滑秒级和分钟级波动，但毫秒级 transient 更适合 rack/pod 级超级电容、镍锌/钠离子高功率电池、power shelf 和 eFuse 配合。Delta 已公开 800VDC 方案，Eaton/Vertiv 也围绕 NVIDIA DSX 进行架构绑定；2027 是从 demo 到小批量工程的关键年。

### 7.3 新化学体系分化

LFP 继续占据站侧 BESS 主流，Li-ion 继续占据 UPS 电池柜主流；镍锌若通过更多 hyperscaler 认证，将在短时高功率 UPS 中获得 10%-30% 渗透；钠离子如果能解决 bankability 和产能，可能在安全敏感、长寿命、高循环场景快速起量。长时储能不会成为 UPS 主体，但会在大型园区的能源韧性和 off-grid/混合供电中出现。

## 8. 头部公司和细分技术清单

### 8.1 UPS、关键电力和预制化模块

| 细分 | 头部/优势公司 | 主要优势 |
|---|---|---|
| 高端数据中心 UPS | Schneider Electric/APC、Vertiv/Liebert、Eaton、ABB、Delta、Huawei Digital Power | 全球客户、认证、服务、端到端电力链 |
| 区域/专业 UPS | Socomec、Riello UPS、Mitsubishi Electric、Toshiba、Fuji Electric、Kehua Data、KSTAR、INVT、AEG Power Solutions、CyberPower、Eaton Tripp Lite | 区域渠道、成本、工业/中小数据中心 |
| 飞轮/旋转 UPS/动态 UPS | Piller Power Systems、Hitec Power Protection、Active Power、Rolls-Royce mtu/Kinolt、Hitzinger、ABB | 高功率短时桥接、化学电池替代、工业可靠性 |
| 中低压配电/开关柜/保护 | Schneider、ABB、Eaton、Siemens、GE Vernova、Hitachi Energy、Mitsubishi Electric、Powell Industries、IEM、Hyosung、Hyundai Electric | 上游瓶颈、认证和交付能力 |
| 母线槽/RPP/PDU/白区配电 | Legrand/Starline/Raritan、Schneider、Vertiv、Eaton、ABB、nVent、Panduit、Chatsworth Products、Delta、Huawei | 白区高密度配电和服务 attach |
| 预制化 power room/skid | Schneider、Vertiv、Eaton/Fibrebond、ABB、Siemens、Huawei FusionPower、Delta、IEM、Powell、nVent | 缩短工期、工厂集成、标准化复制 |

### 8.2 UPS 电池和短时储能

| 细分 | 公司 | 主要优势 |
|---|---|---|
| Li-ion UPS 电池柜/模块 | Samsung SDI、LG Energy Solution、Panasonic、Saft、Kokam/SolarEdge、CATL、BYD、EVE、Hithium、CALB、Gotion、Narada、Shoto、Vision Group、Delta、Vertiv、Huawei、Schneider、Eaton | 电芯质量、系统集成、认证和客户关系 |
| VRLA/铅酸 | EnerSys、East Penn/Deka、C&D Technologies/Trojan、Exide/Clarios、Leoch、Narada、Shoto、GS Yuasa、Hoppecke、FIAMM | 存量维护、低成本、渠道 |
| 镍锌 | ZincFive、EnerSys 等潜在合作链 | 高功率、安全、无热失控传播优势、AI dynamic power 适配 |
| 钠离子 | Natron Energy、HiNa Battery、中科海钠、Tiamat、Faradion/Reliance、CATL 钠离子路线、BYD/中创新航等潜在路线 | 安全、资源约束低、高循环潜力；短板是产能和 bankability |
| 超级电容/混合电容 | Maxwell/Tesla legacy、Skeleton Technologies、LS Mtron、Nippon Chemi-Con、Panasonic、Eaton、Kyocera AVX、Cornell Dubilier、CAP-XX | 毫秒级响应、高循环、机架级缓冲 |

### 8.3 站侧 BESS、PCS、EMS 和微电网

| 细分 | 公司 | 主要优势 |
|---|---|---|
| BESS integrator | Tesla Megapack、Fluence、Wartsila、Powin、Sungrow、CATL、BYD、Hithium、EVE、LGES Vertech、Samsung SDI、Saft、Nidec、GE Vernova、HyperStrong、Canadian Solar e-STORAGE、Kehua、CLOU | 大项目交付、bankability、电芯/PCS/EMS 一体化 |
| PCS/逆变器 | Sungrow、Power Electronics、SMA、Sinexcel、Kehua、Dynapower/Sensata、Parker、ABB、Siemens、Schneider、Eaton、Delta、Hitachi Energy、Danfoss、Nidec | 并网、grid-forming、高效率、认证 |
| EMS/优化软件 | Tesla Autobidder/Powerhub/Opticaster、Fluence Mosaic/Nispera、Wartsila GEMS、Stem Athena、Schneider EcoStruxure/ETAP、Eaton Brightlayer/EnergyAware、Vertiv 360AI/Environet/Waylay、ABB Ability、Siemens Xcelerator、Delta InfraSuite、Huawei NetEco、AutoGrid | 调度收益、并网、数字孪生、预测维护 |
| 微电网/现场发电集成 | Schneider、Eaton、Siemens、ABB、GE Vernova、Caterpillar、Cummins、Generac、Bloom Energy、Plug Power、FuelCell Energy、Tesla、Fluence、Powin | off-grid/混合供电、黑启动、燃料和电池协同 |
| 长时储能 | ESS Inc、Invinity、Redflow、Form Energy、Eos Energy、Ambri、Highview Power、Hydrostor、Energy Vault | 园区级韧性和能源套利，非 UPS 主路径 |

### 8.4 与 AI rack power 相关的功率器件和高压 DC

| 细分 | 公司 | 主要优势 |
|---|---|---|
| SiC/GaN/功率半导体 | Infineon、STMicroelectronics、onsemi、Wolfspeed、ROHM、Mitsubishi Electric、Fuji Electric、Navitas、Transphorm、Power Integrations、Microchip | UPS/PCS/DC-DC 效率和功率密度 |
| DC/DC、eFuse、power shelf | Delta、Eaton、Vertiv、Huawei、Vicor、Bel Power、Advanced Energy、Flex Power Modules、Artesyn/Advanced Energy、MPS、Texas Instruments、Analog Devices、Infineon | 48V/800VDC/机架级配电 |
| 固态变压器/高压 DC 研究 | Delta、Eaton、ABB、Schneider、Siemens、Hitachi Energy、华为、大学/实验室 RTDS 路线 | 2027+ 高密 rack 和 DC-only 架构 |

## 9. 投资判断：子方向排序

| 排名 | 子方向 | 2026 确定性 | 2027 弹性 | 毛利/ROIC | 主要标的/公司 |
|---:|---|---|---|---|---|
| 1 | 综合 grid-to-chip 电力链（UPS+配电+预制+软件+服务） | 极高 | 高 | 高 | Schneider、Vertiv、Eaton、ABB、Delta、Huawei |
| 2 | Li-ion UPS 电池柜 | 极高 | 中高 | 中高 | Delta、Vertiv、Huawei、Schneider、Eaton、Samsung SDI、LGES、CATL、BYD、EVE |
| 3 | 站侧 BESS/负载平滑/LVRT | 高 | 极高 | 中；软件高 | Tesla、Fluence、Sungrow、CATL、BYD、Wartsila、Powin、Hithium |
| 4 | Grid-interactive UPS/EMS | 中 | 极高 | 极高 | Eaton、Schneider、Tesla、Fluence、Vertiv、ABB、Siemens |
| 5 | 预制化电力模块 | 高 | 高 | 高 | Schneider、Vertiv、Eaton/Fibrebond、ABB、Huawei、Delta、IEM、Powell |
| 6 | 镍锌/高功率安全电池 | 中 | 高 | 高 | ZincFive、相关 UPS 合作方 |
| 7 | 机架级储能/超级电容/800VDC | 中低 | 极高 | 极高 | Delta、Eaton、Vertiv、Huawei、Vicor、Navitas、Infineon、Skeleton 等 |
| 8 | VRLA/传统维护 | 高但成长低 | 低 | 中 | EnerSys、East Penn、C&D、Leoch、Narada |

最强的投资表达是“既有 2026 订单确定性，又有 2027 技术弹性”的公司：Vertiv、Eaton、Schneider、ABB、Delta、Huawei Digital Power，以及 BESS 侧的 Tesla、Fluence、Sungrow、CATL、BYD。若寻找中小弹性，ZincFive、Powin、Hithium、Sinexcel、Kehua、KSTAR、nVent、Powell、IEM、Starline/Legrand、Skeleton、Vicor/Navitas/功率半导体链值得跟踪。

## 10. 风险和反证指标

1. AI 数据中心建设延期：Uptime 已提示大量 >100MW proposal 会延迟、缩减或取消。反证指标是 hyperscaler capex 下修、园区电力合同取消、GPU 订单延期。
2. 电力设备上游瓶颈导致 UPS/BESS 无法转收入：变压器、开关柜、断路器、EPC 和并网审批若卡住，订单会进入 backlog 但收入确认推迟。
3. 锂电消防事故或保险趋严：若大型数据中心电池事故发生，AHJ 和保险可能延长审批，利好飞轮/镍锌/钠离子，利空普通锂电柜。
4. 电芯价格下行压缩硬件毛利：BESS integrator 硬件毛利可能被竞争拉低，只有软件/EMS/服务能保护利润率。
5. Grid-interactive UPS 商业模式低于预期：若电网规则和客户风险偏好不配合，UPS 仍只是备用资产，软件收入推迟。
6. 800VDC 标准推进慢：若 hyperscaler 不统一接口，机架级储能和高压 DC 可能停留在展示阶段。
7. 新化学体系 bankability 失败：镍锌/钠离子如果无法取得大客户认证、融资和保险认可，渗透率会显著低于乐观情景。

## 11. 来源与交叉验证

### 11.1 公司一手资料

| 来源 | 链接 | 本报告使用点 |
|---|---|---|
| Eaton Q1 2026 analyst presentation | [Eaton PDF](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf) | 数据中心订单 +240%、Electrical Americas backlog、Boyd Thermal、NVIDIA Rubin DSX grid-to-chip blueprint |
| Schneider Electric Q1 2026 revenues | [Schneider PDF](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026) | Energy Management +12.8%、Systems +16%、Data Center & Networks 双位数增长、complete offer 和 services attach |
| ABB Q1 2026 presentation/press release | [ABB presentation](https://resources.news.e.abb.com/attachments/published/135137/en-US/E927A561C202/ABB-Q1-2026-Group-results-presenation.pdf) / [ABB press release](https://library.e.abb.com/public/dd7e26e13f7a4a4783979a725ef8ff7e/ABB-Q1-2026-press-release-English.pdf) | Electrification 订单 +44%、book-to-bill 1.44、backlog 115 亿美元、数据中心订单三位数增长 |
| Vertiv Q1 2026 results | [PRNewswire release](https://www.prnewswire.com/news-releases/vertiv-reports-strong-first-quarter-with-diluted-eps-growth-of-136-adjusted-diluted-eps-growth-of-83-raises-full-year-guidance-302750110.html) | Q1 净销售 26.5 亿美元、2026 指引 135-140 亿美元、Americas organic +44% |
| Vertiv at NVIDIA GTC 2026 | [Vertiv GTC page](https://www.vertiv.com/en-in/about/news-and-insights/events/2026-nvidia-gtc/) | AI factory、BYOP&C、grid-to-chip、factory-assembled blocks |
| Delta Data Center World 2026 | [Delta press release](https://www.delta-americas.com/en-US/news/delta-unveils-integrated-power%2C-cooling%2C-and-infrastructure-architecture-for-ai-data-centers-at-data-center-world-2026) | 6.5GW+ 美国数据中心 UPS 装机、UZR3 3GW+、DPM Gen-2、800VDC、1.1MW/rack |
| Tesla Megapack resources | [Tesla Megapack resources](https://www.tesla.com/support/energy/megapack/resources) / [Megapack for Data Centers PDF](https://digitalassets.tesla.com/tesla-contents/image/upload/megapack-resources-megapack-for-data-centers-powering-growth-of-ai-infrastructure.pdf) | AI 数据中心 BESS 用例：负载平滑、LVRT、备用、并网压力缓解 |
| Fluence Q1 FY2026 results | [Fluence release](https://ir.fluenceenergy.com/news-releases/news-release-details/fluence-energy-inc-reports-first-quarter-2026-results-reaffirms) | Q1 收入 4.752 亿美元、backlog 55 亿美元、pipeline 300 亿美元、数据中心需求驱动 |
| Huawei FusionPower6000 | [Huawei PDF](https://digitalpower.huawei.com/attachments/data-center-facility/1bad892d17c54accb26d8b57f5994fd5.pdf) | MW 级预制 PowerPod、TTM 缩短、占地减少、链路效率 |
| Schneider Galaxy VXL | [Schneider product page](https://www.se.com/ww/en/product-range/99068679-galaxy-vxl/) | 500-1250kW 高密度 UPS 产品路线 |
| Vertiv EnergyCore Li-ion cabinet | [Vertiv product page](https://www.vertiv.com/en-us/products-catalog/critical-power/uninterruptible-power-supplies-ups/vertiv-energycore-lithium-ion-battery-cabinet/) | 数据中心 UPS 锂电柜产品化 |
| Eaton EnergyAware / Microsoft case | [EnergyAware UPS](https://www.eaton.com/ie/en-gb/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/energyaware-ups.html) / [Microsoft-Enel X-Eaton](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2022/eaton--microsoft-and-enel-x-announce-grid-interactive-ups-system.html) | Grid-interactive UPS 商业化验证 |

### 11.2 行业报告、标准与本地模型

| 来源 | 链接/路径 | 本报告使用点 |
|---|---|---|
| Uptime Institute 2026 giant data center power report | [Uptime PDF](https://intelligence.uptimeinstitute.com/sites/default/files/2026-01/UI%20Field%20report%20194_Giant%20data%20center%20power%20plans%20reach%20extreme%20levels.pdf) | 377 个 >100MW 项目、2025 proposal power 181.2GW、AI 占约 60%、北美占 80%、实际利用 25% 假设 |
| Arizton Data Center UPS Market | [Arizton report page](https://www.arizton.com/market-reports/data-center-ups-market-size) | 2024 UPS investment 88.9 亿美元、2030 207.5 亿美元、CAGR 15.17%、2030 power capacity 19,666MW |
| Grand View Research Data Center UPS Market | [GVR report page](https://www.grandviewresearch.com/industry-analysis/data-center-ups-market) | 2024 UPS market 40.4 亿美元、2030 62.7 亿美元、CAGR 8.0%，用于交叉验证口径差异 |
| ZincFive 2026 Data Center Energy Storage Industry Insights | [ZincFive PDF](https://zincfive.com/wp-content/uploads/2026/03/2026-Data-Center-Energy-Storage-Industry-Insights-Report.pdf) | 150 名行业人士调查；84% 重视 TCO，76% 重视安全，66% 认为 AI dynamic power mitigation 有价值，54% 中央 UPS 使用锂电 |
| UL 9540A | [UL 9540A](https://www.ul.com/services/ul-9540a-test-method) | 电池储能热失控传播测试 |
| NFPA 855 | [NFPA 855](https://www.nfpa.org/codes-and-standards/nfpa-855-standard-development/855) | 固定式储能系统安装标准 |
| 本地 AI 芯片路线 | `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md` | 2026/2027 AI 芯片平台、乐观出货和技术路径假设 |
| 本地美国 AI 数据中心建设模型 | `D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md` | 美国 AI IT load、capex、UPS/BESS/电能质量订单池情景 |

## 12. 一句话总括

2026 年数据中心 UPS 与电池储能的核心投资机会，是从“关键负载备用设备”升级为“AI 工厂建设速度、电网接入、负载动态稳定和能源金融化”的基础设施杠杆；最确定的是 Li-ion UPS、MW 级模块化 UPS、预制化电力模块，最大弹性在 BESS 站侧负载平滑、grid-interactive UPS、机架级短时储能和 800VDC。
# 行业调研：【数据中心低压配电、PDU与母线槽】

截至日期：2026-05-08  
研究口径：本文聚焦 AI 数据中心从 UPS/低压总配电到机柜的“最后几百米电力分配”价值链，包括低压开关柜/开关板、RPP/列头柜/楼层 PDU、母线槽与 tap-off、rack PDU、ORv3/48V 机架母排与电源架、预制化低压电力模块、监控传感与数字化运维。除非特别说明，市场规模为全球 AI 数据中心相关订单/收入池，美元名义值；不同产品之间存在集成和重复计价，表格不可简单相加。

## 0. 核心结论

数据中心低压配电、PDU 与母线槽在 2026 年已经从传统机电配套，变成 AI 计算中心交付节奏的硬瓶颈。GPU/HBM 仍是最贵的环节，但“能不能按时上电”正在决定 GPU 能不能变成收入。Eaton、Vertiv、Schneider、ABB、Legrand、nVent 等公司的 2026 年一季度订单、收入和扩产动作，都在显示一个同方向信号：电力链条订单在提前，客户愿意为交期、认证和成套能力付溢价。

2026 年最可能放量的技术路径不是完全颠覆性的 800VDC，而是成熟的 **415/480V 三相 AC + 高电流 overhead busway + 智能 rack PDU + ORv3/48V 机架内母排 + 预制化电力模块**。800VDC 在 2026 年会从发布会和工程样机进入小批量验证，真正的订单斜率更可能出现在 2027 下半年以后，并与 Rubin Ultra、Kyber/1MW 机架、MI400/MI500、下一代 hyperscaler ASIC 绑定。

本文的基准判断是：全球 AI 数据中心低压配电/PDU/母线槽相关订单池，2026 年约 **$24B-$38B**，2027 年约 **$35B-$55B**；乐观情景下 2027 年可到 **$60B-$95B**；极度超预期情景下，如果 2027 需求前置、现场发电和电网接入同步推进，2027 可冲到 **$105B-$160B**。其中最有定价权的不是裸铜排，而是经过客户认证的高密度智能 PDU、busway tap-off/插接箱、预制化电力模块、DC 保护与软件化电力管理。

## 1. 2026 AI 算力建设带来的机遇与挑战

### 1.1 需求侧机遇

1. **机柜功率密度跃迁**：传统企业机柜常见 5-15kW，AI 推理/训练机柜在 2026 年大规模进入 70-150kW，NVIDIA GB200/GB300 NVL72、AMD Helios、AWS Trainium UltraServer、Google TPU pod 等把电力分配从“按机柜配电”推到“按整柜/整排/整 pod 设计”。Legrand 2026 年 AI 数据中心页面已把高密度 PDU 需求描述为 70-100kW+ 机柜，Raritan/Server Technology/Starline 的产品组合正是为这一密度服务。

2. **订单先于服务器确认**：低压开关柜、母线槽、PDU、插接箱、断路器、预制电力模块需要提前设计、认证、排产、现场安装。即使 GPU 延迟，业主也会先锁电力设备，因为电力设备缺货会使整栋楼空置。Vertiv 在 2026 年 3 月宣布新增和扩建美洲 4 个制造设施，部分基础设施方案满产后区域产能预计提升约 7 倍；Eaton 2026Q1 Electrical Americas 订单滚动同比增长 42%，数据中心订单约增长 240%；ABB 2026Q1 Electrification 订单同比增长 51%，并称数据中心订单为三位数增长。

3. **价值量从“每机柜几百美元”上升到“每 MW 数十万到百万美元”**：传统 rack PDU 是相对标准化耗材；AI 机柜需要 480/277V 或 415/240V 三相输入、60A/100A/125A 级别、双路冗余、 outlet-level metering/switching、热插拔控制器、环境传感、Redfish/SNMP/Modbus API。busway 也从低安培支线变为 800A/1000A/1250A 甚至更高等级的连续底部插接系统。

4. **预制化和标准化成为交付货币**：AI 数据中心客户越来越用“time to first token”衡量基础设施，低压配电不再只是按图施工，而是通过预制电力模块、sidecar power rack、标准化 busway run、BIM 模型和数字孪生缩短交付。

### 1.2 挑战与瓶颈

1. **电力设备交期**：变压器、开关柜、断路器、母线槽、UPS、BESS、现场发电设备共用供应链。Bloomberg/Sightline 相关报道显示，美国 2026 年部分数据中心项目因电力设备和并网约束延期，变压器交期可从过去约 24-30 个月拉长到最高 5 年。低压设备交期通常短于大型变压器，但受同一批铜、断路器、壳体、认证、工程人力约束。

2. **高功率瞬态负载**：AI 训练和推理负载有同步功率波动，传统配电按平均功率和缓慢变化负载设计。NVIDIA Vera Rubin 资料强调 rack-level power smoothing 和本地能量缓冲，说明未来低压系统不仅要承载稳态电流，还要处理毫秒到秒级瞬态。

3. **铜/铝/银和高端连接器用量上升**：54V DC 机架内供电在 200kW 以上会遇到电流和铜排体积问题；NVIDIA 800VDC 技术路线的核心动机之一就是降低电流、铜用量和线缆体积。但 2026 年大部分部署仍在 415/480V AC 与 48/54V 机架内电源架之间运行，铜排和高可靠连接件仍是直接瓶颈。

4. **认证和客户 AVL 锁定**：UL857、IEC 61439-6、UL/IEC 低压开关设备认证、NFPA/NEC、现场短路电流测试、客户内部标准，都使供应商切换慢。客户不会为了便宜几百美元更换 PDU 或 busway 供应商，因为一次故障可能烧毁百万美元级机柜。

5. **800VDC 标准、安全和保护体系尚未成熟**：800VDC 会减少转换级数，但需要 DC 断路器、固态保护、eFuse、SST、直流母线、接地与电弧管理、运维培训和消防规则同步成熟。2026 年可见样机和参考架构，2027 年先在少数新建 AI factory 中小批量。

## 2. 当前正在使用的主要技术

### 2.1 2026 主流路径：415/480V AC 到机柜，48/54V DC 到服务器托盘

今天绝大多数 AI 数据中心仍是 AC 主导：

- 中压进线经变压器、UPS 或 MV UPS，到低压 switchgear/switchboard。
- 低压侧使用 415/240V 或 480/277V 三相 AC，送入 RPP、PDU、busway 或预制电力模块。
- 机柜侧使用高密度 rack PDU 或 OCP power shelf，把 AC 转为 48/54V DC，再由板级 VRM 转到 GPU/ASIC 核心电压。
- 母线槽通常布在机柜上方，tap-off 直接向 rack PDU 或列头/机柜供电，减少电缆施工和未来改造成本。

这一路径 2026 年的优势是成熟、可认证、供应商多、现场工程师熟悉，能承接 GB200/GB300、MI350、Trainium2、TPU v7 Ironwood、Maia 200 等绝大多数 2026 主力平台。

### 2.2 高密度智能 rack PDU

Rack PDU 已经从基础插排升级为高功率测量和控制节点。Legrand/Raritan 官方资料显示，其智能 PDU 支持 12A 到 125A 每线，100VAC 单相到 480/277V 三相，最高可交付约 86.6kW；HDOT Cx 混合插座可兼容 C14/C20 线缆并提高单位 PDU 插座密度。AI 机柜中，rPDU 的价值从“分电”扩展到：

- 每相、每支路、每插座功率测量；
- 双路 A/B 供电冗余监控；
- 远程开关、上电顺序控制和 inrush 管理；
- 温湿度、漏液、振动、门禁传感；
- Redfish、SNMP、Modbus、REST API 接入 DCIM/客户运维平台。

### 2.3 高电流 overhead busway

母线槽对 AI 数据中心的价值在于灵活和快交付。Starline T5 系列覆盖 250A、400A、600A、800A、1000A、1200-1250A，最高 600V 连续工作，满足 UL857 与 IEC 61439-6 等标准；Eaton Pow-R-Way III 可做到铜排 5000A、600V、200kA 短路耐受。这说明 busway 在 AI 时代不是小配件，而是把白空间改造成可快速扩容电力网格的核心产品。

### 2.4 ORv3/48V 机架内母排与 power shelf

OCP Open Rack v3 的 48V DC busbar 和 power shelf 正在成为 hyperscaler 和 AI rack-scale 系统的重要形态。Legrand、Rittal、Flex、Advanced Energy、Delta、Lite-On、Bel、AcBel 等都在围绕 ORv3 做机架、电源架、垂直母排、连接器和管理固件。2026 年它会和传统 AC rack PDU 并存：AC 到机柜或 power rack，机柜内 48V DC busbar 给 GPU 托盘供电。

### 2.5 800VDC：2026 样机，2027 早期量产，2028 才更像主流

NVIDIA 800VDC 架构的核心是减少转换级数，将 800V DC 在数据中心内分配并由计算机柜直接使用。NVIDIA 官方材料明确把 800VDC 作为支持未来 1MW IT rack 的路径，并与 Eaton、Schneider、Vertiv、Delta、TI、Infineon、ST、Navitas、onsemi 等生态伙伴推进。Delta 在 Data Center World 2026 展示的 800VDC 方案声称可在 rack 内交付最高 1.1MW、最高 98% 效率；Siemens 与 Rittal 则在 2026 年发布面向白空间的 power sidecar/标准化低压配电合作。

我的判断：800VDC 的投资价值很高，但 2026 年大规模收入仍有限；2027 年有望在新建 AI factory、Rubin Ultra/Kyber 和部分自研 ASIC 项目中形成首批高毛利订单；2028 年以后才会对传统 AC busway/rPDU 产生更明显替代。

## 3. 结合 2026-2027 最大出货 AI 芯片的技术路径判断

本节芯片路线图来自项目内已有 `ai_chip_research_2026_2027.md`，未额外外搜。

| 2026-2027 出货/价值权重靠前平台 | 对低压配电/PDU/母线槽的含义 | 2026 最可能配电路径 | 2027 变化 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | NVL72 整柜液冷、高功率、rack-scale 集成；是 2026 最核心的高密度机柜拉动项 | 415/480V AC + high-current busway + high-density intelligent rPDU + 48/54V rack power shelf | Rubin 接棒后，同类架构继续，但本地能量缓冲和功率平滑需求提高 |
| AWS Trainium2 | Project Rainier 级别大规模自用，UltraServer 64 芯片 scale-up；AWS 自有设施可高度标准化 | 传统 AC 配电 + 自研 rack/server power + 液冷/风液混合 | Trainium3/4 提高机柜功率，可能更快采用 OCP/48V 和定制 busbar |
| Google TPU v7 Ironwood | Google 自有数据中心可从 pod 到设施协同设计，推理规模大 | 传统 AC + Google 自有 rack/pod 供电 + 高密度监控 | TPU8 和 AI Hypercomputer 扩张推动更高电压和更强软件化电力管理 |
| NVIDIA B200/GB200 | 2026 仍有大量既有订单和成本敏感客户 | 与 GB300 类似但功率密度略低，传统 AC 路径更稳 | 逐步转存量，PDU/母线槽改造需求仍在 |
| Huawei Ascend 910C/950 | 中国国产替代和 SuperPoD 路线依赖系统级并联；国内园区电力和液冷约束大 | 国内 380/400V AC + 机柜/列级配电 + 液冷逐步提升 | 950/960 超节点推动高密度母排和国产化 PDU/断路器 |
| AMD MI350/MI355 | 2026 AMD 最确定放量，PCIe/UBB 形态更适配企业和云端混合 | 传统 AC、3-phase rPDU、UBB 高电流供电 | MI400/Helios 72 GPU rack 使 OCP/48V、sidecar 和 800VDC 关注度提升 |
| AWS Trainium3 | 144 芯片 UltraServer，3nm，强调能效 | 2026 小批量，仍以成熟 AC/48V 架构为主 | 2027 可带动更高功率 power shelf 和 rack busbar |
| Meta MTIA 300/400/450/500 | OCP 标准化能力强，推理规模大，电力 TCO 敏感 | ORv3/48V、标准化 rack 与 busbar 渗透高 | Meta/Broadcom >1GW 级 ASIC 项目可能成为 DC power architecture 的重要试验场 |
| Microsoft Maia 200 | 750W SoC、闭环液冷、Azure 内部标准化 | 传统 AC + Azure rack-level power/cooling | Maia 后续代际可能提高 rack buffer 和智能配电需求 |
| AMD MI400/MI455X Helios | 2026H2 起步，HBM4、72 GPU rack、全液冷，2027 潜在爆发 | 2026 试点多用成熟 AC + 48V/机架内母排 | 若 Meta/Oracle 等客户放量，2027 可能率先导入 sidecar/800VDC 试点 |

### 3.1 技术成熟和放量时间表

| 技术路径 | 2026H1 | 2026H2 | 2027H1 | 2027H2 | 基准判断 | 乐观判断 | 极度超预期判断 |
|---|---|---|---|---|---|---|---|
| 415/480V AC + 智能 rPDU | 已成熟、放量 | GB300/MI350/TPU/Trainium 继续拉动 | 继续主流 | 仍占最大安装基数 | 2026-2027 订单主力 | 高密度型号缺货、价格强 | 由于项目前置，订单峰值延长到 2028 |
| Overhead AC busway + tap-off | 已成熟、交期紧 | 高电流 T5/Canalis/Pow-R-Way 等放量 | AI hall 标配化 | 与预制模块绑定 | 2026 渗透率上升最快 | 1000A/1250A tap-off 供不应求 | 大客户锁年度产能，毛利上冲 |
| ORv3/48V rack busbar/power shelf | hyperscaler 导入 | GB300、MTIA、Helios 试点增多 | 规模化 | 成为 rack-scale 标准件 | 2027 真正加速 | 2026H2 已明显拉货 | 2027 成为新 AI rack 默认 |
| 预制化低压电力模块 | 成熟但产能紧 | 大客户加速采用 | 大园区复制 | 标准 SKU 化 | 2026-2027 高确定性 | 绑定 EPC/液冷成套交付 | 成为大型客户唯一可接受交付方式 |
| 800VDC facility/row distribution | 参考设计/样机 | GTC/展会/工程样机 | 少数新建项目试运行 | Rubin Ultra/Kyber 首批生产 | 2027 小批量，2028 放量 | 2027H2 进入多个 hyperscaler 项目 | 2027 即出现 10%+ 新高密 rack 渗透 |
| DC solid-state breaker/eFuse/SST | 实验和样机 | 小批量验证 | 工程认证 | 随 800VDC 绑定 | 800VDC 的前置瓶颈 | 高毛利 niche 产品 | 标准快速冻结，头部供应商垄断首批 |

### 3.2 2026 最可能技术路径

2026 年最可能路径按确定性排序：

1. **415/480V AC 低压配电 + overhead busway + high-density intelligent rPDU**：确定性最高，服务 GB300/GB200、MI350、Trainium2、Ironwood、Maia 200 等绝大多数新部署。
2. **ORv3/48V rack busbar + power shelf**：在 hyperscaler、Meta/OCP 生态和 rack-scale AI 平台中快速增渗透，尤其是整柜交付和自研 ASIC。
3. **预制化低压电力模块 + 白空间 fit-out 一体化**：受益于客户对交付速度的极端重视，Vertiv、Schneider、Eaton、Siemens/Rittal、Delta 等都在强化。
4. **800VDC/sidecar/固态保护**：2026 是“验证和设计定型”，不是大规模收入年；但对 2027-2028 投资弹性最大。

## 4. 已经开始放量的关键产品：市场规模、渗透率、利润率

说明：以下为未来 3 个月、12 个月、24 个月累计订单/收入池区间，三情景分别为基准/乐观/极度超预期乐观。渗透率为对应技术在新增 AI 数据中心项目或新增高密机柜中的采用比例，不同产品口径不同，已在“渗透率路径”中注明。表格存在系统集成重复，不可简单求和。

### 4.1 市场规模与渗透率

| 已放量产品 | 未来3个月市场规模：基准/乐观/极乐 | 未来12个月市场规模：基准/乐观/极乐 | 未来24个月市场规模：基准/乐观/极乐 | 渗透率路径 | 增长判断 |
|---|---:|---:|---:|---|---|
| 415/480V AC 低压 switchgear/switchboard/panelboard | $3.0-4.8B / $4.5-7.5B / $7-11B | $13-21B / $20-32B / $31-48B | $31-50B / $52-82B / $90-135B | 新增 AI 项目 2026Q2 90-95%，2027Q2 85-90%，2028Q2 75-85% | 不是新技术，但受所有 AI 项目前置锁单拉动，价格和交期强 |
| Overhead AC busway、tap-off、插接箱 | $1.0-1.8B / $1.6-2.8B / $2.5-4.2B | $4.5-7.5B / $7-12B / $11-18B | $11-18B / $20-32B / $36-55B | 新 AI 白空间 60%→68%→75%；1000A+ 高电流产品占 busway 新单 20%→35%→45% | 高密机柜把母线槽从可选变成默认；tap-off 是高毛利核心 |
| 智能高密 rack PDU（metered/switched/outlet-level） | $0.8-1.2B / $1.1-1.8B / $1.6-2.6B | $3.5-5.4B / $5-7.8B / $7.5-11.5B | $8-13B / $13-20B / $22-34B | 新 AI 机柜智能化 45%→60%→70%；70kW+ PDU 15%→35%→50% | 市场报告给 2026 rack PDU 全市场约 $3.06B，但 AI 高功率/智能 ASP 上移会显著抬高订单口径 |
| RPP/楼层 PDU/列级 PDU/branch circuit monitoring/STS | $1.2-2.0B / $1.8-3.0B / $2.8-4.5B | $5-8.5B / $8-13B / $13-21B | $12-20B / $22-34B / $40-60B | 传统 floor PDU 渗透 70%→65%→55%，但监测型 RPP/STS 单 MW 价值上升 | 部分被 busway 和 rack-direct 替代，但改造项目和冗余切换仍有强需求 |
| ORv3/48V rack busbar、power shelf、垂直母排 | $0.8-1.5B / $1.3-2.4B / $2.0-3.8B | $3.5-6.5B / $6-11B / $10-17B | $10-18B / $20-35B / $38-65B | 新 AI rack 10%→20%→35%；hyperscaler rack-scale 可达 25%→45%→60% | 2026 是加速导入，2027 随 MTIA/Helios/Rubin/ORv3 复制 |
| 预制化低压电力模块、eHouse、white-space power POD | $2.0-3.5B / $3.2-5.5B / $5-8B | $9-15B / $15-25B / $25-40B | $24-40B / $45-75B / $85-130B | 大型新建 AI 项目 25%→35%→50% | 客户用钱买时间；供应商可通过标准化提高周转和毛利 |
| PDU/母线槽传感、DCIM、电力监控软件/API | $0.3-0.6B / $0.5-0.9B / $0.8-1.4B | $1.5-2.7B / $2.5-4.5B / $4-7B | $4-7B / $8-13B / $14-24B | 新高密项目 40%→60%→75% | 软件和数据层价值被低估，随功率波动和容量调度复杂化提升 |

### 4.2 毛利率/利润率情景

| 已放量产品 | 当前毛利率基准 | 乐观毛利率 | 极度超预期毛利率 | 为什么能有溢价 |
|---|---:|---:|---:|---|
| 低压 switchgear/switchboard | 30-38% | 34-42% | 38-48% | 交期、客户 AVL、短路测试、断路器供应和现场服务稀缺 |
| AC busway + tap-off | 30-42% | 35-47% | 40-52% | 铜排本体不稀缺，但 tap-off、认证、改造灵活性和高电流插接件有强定价权 |
| 智能高密 rack PDU | 35-48% | 42-55% | 48-60% | 高功率、智能控制器、固件/API、客户认证和低故障率决定价格 |
| RPP/列级 PDU/branch monitoring/STS | 28-38% | 32-44% | 36-50% | 冗余切换和监控能力直接关系 uptime；改造项目可加急收费 |
| ORv3/48V rack busbar/power shelf | 22-33% | 27-38% | 32-45% | hyperscaler 量大压价，但早期高密产品、连接器和电源架仍有壁垒 |
| 预制化低压电力模块/eHouse | 18-28% | 23-32% | 28-38% | 项目制本来毛利较低，但标准化、工厂预制和交付速度能提高溢价 |
| 电力监控软件/DCIM/API | 50-70% | 60-80% | 70-85% | 一旦接入客户运维系统，切换成本高，软件毛利结构优秀 |

## 5. 在研和未来快速增长的关键产品

### 5.1 关键在研方向

1. **800VDC 数据中心配电**：中央整流、800VDC 母线、DC 保护、rack/row distribution、sidecar power rack。2026 年处在生态构建和客户验证阶段。
2. **固态断路器、eFuse、SST**：DC 系统保护的核心难点。没有可靠、可认证、可维护的保护体系，800VDC 无法大规模商业化。
3. **rack/row 级能量缓冲**：超级电容、锂电、固态电池、飞轮等用于毫秒到秒级功率平滑，解决 synchronized AI workload 的电力冲击。
4. **高压 DC 到 48V/12V/6V 的高效转换**：GaN、SiC、先进磁性件、低损耗连接器和冷却一体化电源模块。
5. **AI-aware 电力调度软件**：把 GPU telemetry、power cap、PDU/UPS/电网数据合并，按 token/MW 优化，而不是按传统 PUE 维度优化。
6. **DC-capable busway 和高压直流连接器**：800VDC 需要新的母线、接头、绝缘、爬电距离、电弧和维护标准。

### 5.2 在研产品市场预测

| 在研/早期产品 | 未来3个月市场规模：基准/乐观/极乐 | 未来12个月市场规模：基准/乐观/极乐 | 未来24个月市场规模：基准/乐观/极乐 | 渗透率路径 | 毛利率基准/乐观/极乐 |
|---|---:|---:|---:|---|---|
| 800VDC facility/row distribution | $0.05-0.15B / $0.10-0.30B / $0.20-0.60B | $0.5-1.5B / $1.5-3.5B / $3.5-7B | $3-8B / $8-18B / $18-35B | 新高密 AI rack <1%→2-5%→6-15% | 35-50% / 40-58% / 45-65% |
| DC 固态断路器/eFuse/SST | $0.03-0.12B / $0.10-0.25B / $0.25-0.60B | $0.3-1.0B / $1-2.5B / $2-5B | $2-5B / $5-12B / $12-25B | 与 800VDC 绑定，2027 后开始进 AVL | 40-60% / 45-65% / 50-70% |
| 800V sidecar power rack | $0.10-0.30B / $0.30-0.70B / $0.70-1.50B | $1-3B / $3-7B / $7-15B | $6-14B / $15-35B / $35-70B | 2026 样机，2027 Rubin/Helios/ASIC 小批量 | 28-42% / 35-50% / 42-58% |
| rack/row 能量缓冲 | $0.05-0.20B / $0.15-0.40B / $0.40-0.90B | $0.5-1.5B / $1.5-4B / $4-8B | $2-6B / $6-15B / $15-35B | 先用于最高密度机柜和电网弱区域 | 30-45% / 38-55% / 45-65% |
| 高压 DC/DC、GaN/SiC 电源模块 | $0.10-0.25B / $0.25-0.60B / $0.60-1.20B | $0.8-2.0B / $2-5B / $5-10B | $4-10B / $10-25B / $25-55B | 2027 随 800VDC 与 1MW rack 放量 | 32-50% / 40-58% / 48-68% |
| AI-aware 电力编排/DCIM | $0.10-0.30B / $0.20-0.50B / $0.50-1.00B | $0.8-1.8B / $1.5-3.5B / $3-6B | $3-7B / $6-14B / $12-28B | 大客户先自研，商业软件从多租户 colo 切入 | 60-80% / 70-85% / 75-90% |
| DC busway/高压直流连接器 | $0.05-0.15B / $0.15-0.35B / $0.35-0.80B | $0.5-1.2B / $1.2-3B / $3-6B | $3-7B / $7-16B / $15-35B | 2027 小批量，2028 与 800VDC 共振 | 35-50% / 42-58% / 48-65% |

## 6. 供给侧：产能结构、瓶颈、成本与价格传导

### 6.1 产能结构

| 环节 | 主要产能地区 | 代表公司 | 产能/工艺特点 |
|---|---|---|---|
| 低压 switchgear/switchboard | 美国、墨西哥、加拿大、欧洲、中国、印度 | Eaton、Schneider、ABB、Siemens、Vertiv、GE Vernova、Powell、Hubbell、Chint、良信、LS Electric | 工程定制、钣金、铜排、断路器、保护继电器、短路测试、客户工厂验收 |
| Busway/母线槽 | 美国、欧洲、中国、印度、土耳其、韩国 | Legrand Starline/Zucchini/XCP、Eaton Pow-R-Way、Schneider Canalis/I-Line、Siemens SIVACON 8PS、ABB、EAE、LS、Rittal RiLineX | 铜/铝导体、绝缘、壳体、插接箱、短路耐受测试、UL/IEC 认证 |
| Rack PDU | 美国、欧洲、中国、东南亚 | Legrand Raritan/Server Technology、Vertiv Geist、Schneider APC、Eaton/Tripp Lite、Panduit、Leviton、CyberPower、Austin Hughes、ATEN、Yosun | 金属壳体、插座/线缆、断路器、计量芯片、控制器、固件、网络安全 |
| ORv3 power shelf/48V busbar | 台湾、中国、美国、欧洲 | Delta、Lite-On、Advanced Energy/Artesyn、Bel Power、AcBel、Murata、Flex、Legrand、Rittal、BizLink、Amphenol、TE、Molex | 高效率 AC/DC、48V 母排、连接器、OCP 规范、热设计和固件 |
| 预制化电力模块 | 美国、墨西哥、欧洲、中国、东南亚 | Vertiv、Schneider、Eaton/Fibrebond、Siemens/Rittal、ABB、Delta、Huawei Digital Power、Mitsubishi | 工厂集成、模块化电力房、BIM/数字孪生、现场吊装和调试 |
| 800VDC/固态保护 | 美国、欧洲、日本、中国台湾、中国大陆 | NVIDIA 生态、Eaton、Schneider、Vertiv、ABB、Delta、TI、Infineon、ST、Navitas、onsemi、Wolfspeed、DG Matrix、Rittal | SiC/GaN、SST、DC breaker/eFuse、800V 母线、直流安全认证 |

### 6.2 至少 5 个关键供给瓶颈

1. **铜、铝、银和高可靠连接器**：高电流 busway、tap-off、rack busbar、断路器触点直接吃导体材料。800VDC 可降低部分铜用量，但短期无法替代所有 AC/48V 架构。
2. **断路器、熔断器、DC 保护器件**：传统 AC 保护件已经紧，DC 保护件认证更少。高故障电流场景要求短路耐受、选择性保护和电弧控制。
3. **UL/IEC/客户认证周期**：母线槽、PDU、switchgear、插接箱都要通过标准和客户内部测试。AI 客户一旦确定 AVL，新增供应商导入可能需要 6-18 个月。
4. **工程设计和 submittal 人力**：每个数据中心电气系统都需要短路计算、选择性协调、热仿真、BIM 模型、现场布线和变更单，电气工程师短缺是隐性瓶颈。
5. **工厂测试和 FAT 产能**：高端 switchgear、预制模块、母线槽 run 需要工厂验收测试；测试间、负载箱、短路实验室和质检人员会卡住交付。
6. **现场安装与 commissioning**：母线槽和 rPDU 看似标准，但现场吊装、支架、接地、相序、负载平衡、漏液/传感联调都需要熟练电工。
7. **网络安全和固件维护**：智能 PDU 已经接入客户网络，固件漏洞、供应链安全、证书管理成为客户审核重点。
8. **关税和地缘供应链**：美国项目对中国电力设备、锂电池、电子元件依赖仍高，关税/进口审查会放大交期和库存需求。

### 6.3 成本构成和毛利决定因素

| 产品 | 典型成本拆分 | 毛利决定因素 |
|---|---|---|
| Busway/母线槽 | 铜/铝 45-60%；壳体 10-15%；绝缘/接头 8-12%；tap-off/断路器 10-20%；人工/测试/物流 10-15% | 铜价传导、tap-off 复杂度、认证等级、短路耐受、交期 |
| Rack PDU | 插座/线缆/断路器 25-35%；金属壳体/母排 15-25%；计量/控制器/网络 15-25%；装配测试 15-20%；固件/支持 5-10% | 智能化等级、单 PDU kW、outlet-level 功能、客户认证、固件和 API |
| 低压 switchgear/switchboard | 断路器/保护 30-45%；母排 20-30%；钣金 10-15%；计量控制 5-15%；工程装配测试 15-25% | 断路器供应、短路等级、选择性保护、FAT/现场服务、客户项目紧急程度 |
| ORv3/48V power shelf | 电源模块 45-60%；母排/连接器 15-25%；控制器 5-10%；壳体/散热 10-15%；测试 5-10% | 效率、功率密度、OCP 兼容、冗余、客户规模压价 |
| 预制电力模块 | switchgear/UPS/母排/线缆 55-70%；壳体/暖通/消防 10-20%；工程设计 10-15%；测试物流 5-10% | 标准化程度、交期、现场工程节省、客户是否接受成套溢价 |
| 800VDC/固态保护 | SiC/GaN/IGBT/磁性件 35-55%；母排/绝缘/壳体 15-25%；传感控制 10-20%；认证测试 10-20% | 技术壁垒、认证稀缺、可靠性数据、客户首批导入 |

价格传导机制：铜/铝等大宗材料通常通过项目报价或指数化条款传导；断路器、控制器、固件、认证和交期溢价则更像“能力定价”。AI 项目最特殊的地方是客户愿意为交付速度付费，供应商可以通过预付款、年度产能保留、加急费、变更单和成套服务捕获超额毛利。

## 7. 竞争格局与可量化壁垒

### 7.1 市场结构

| 细分 | 头部集中度估计 | 主要竞争者 | 结构判断 |
|---|---:|---|---|
| 北美低压 switchgear/switchboard | Top 5 约 65-80% | Eaton、Schneider、ABB、Siemens、Vertiv、Powell、Hubbell | 大客户项目和服务网络高度集中 |
| 数据中心 busway | Top 5 约 55-70% | Legrand Starline、Schneider、Eaton、Siemens、ABB、EAE、LS、Rittal | Starline 在高端数据中心心智强，其他电气巨头靠成套方案竞争 |
| 高端智能 rack PDU | Top 4 约 60-75% | Legrand Raritan/Server Technology、Vertiv Geist、Schneider APC、Eaton/Tripp Lite、Panduit | 智能化和客户认证带来强锁定 |
| 预制电力模块 | Top 5 约 55-70% | Vertiv、Schneider、Eaton/Fibrebond、Siemens/Rittal、ABB、Delta | 产能、项目管理和成套能力比单品更重要 |
| ORv3/48V power shelf | Top 6 约 50-70% | Delta、Lite-On、Advanced Energy、Bel、AcBel、Flex、Legrand、Rittal | hyperscaler 量大压价，但供应商认证门槛高 |
| 800VDC/固态保护 | 早期格局未定 | NVIDIA 生态、Eaton、Schneider、Vertiv、ABB、Delta、TI、Infineon、ST、Navitas、onsemi、Wolfspeed、DG Matrix | 2026-2027 是标准和首批 AVL 争夺期 |

### 7.2 壁垒清单：为什么能定价

1. **技术壁垒**：高短路电流、热管理、相平衡、谐波、选择性保护、DC 电弧、固件安全都不是简单钣金加工。客户买的是 uptime。
2. **规模壁垒**：AI 项目是多园区、多 GW 复制，供应商必须同时有产能、全球交付、现场服务、备件和质量体系。小厂能做样品，不一定能做 200MW 项目。
3. **渠道/客户锁定**：hyperscaler 与 colo 的标准化目录一旦选定，后续园区会复制同一套 PDU、busway、断路器和监控协议，切换成本高。
4. **认证标准**：UL857、IEC 61439-6、UL 891/1558、NEC/NFPA、客户内部 FAT/SAT，会把未经验证的供应商挡在外面。
5. **切换成本**：更换 busway 或 rPDU 不只是换硬件，还涉及 BIM、支架、插接箱、线缆、PDU 固件、DCIM 集成、运维 SOP 和备件。
6. **交付信用**：如果供应商延迟，客户的 GPU 上电延迟，损失远大于设备价差。交付记录本身就是定价权。
7. **软件和数据**：智能 PDU 和 DCIM 接入客户平台后，形成持续数据和 API 依赖，软件毛利和服务续费会增强 ROIC。

### 7.3 价值捕获：哪一层长期 ROIC/毛利最高

长期最可能拥有高 ROIC 的不是裸母线槽本体，而是三类公司：

1. **完整 power train 成套商**：Schneider、Eaton、Vertiv、ABB、Siemens 这类从 switchgear、UPS、busway、PDU、监控到服务都有能力的供应商，可以把单品毛利变成系统毛利和服务收入。
2. **高端智能 rack PDU/传感/软件平台**：Legrand Raritan/Server Technology、Vertiv Geist、Schneider APC、Eaton 等拥有客户认证和固件平台，单位硬件不大，但毛利高、切换成本高。
3. **800VDC 和固态保护首批标准制定者**：如果 2027-2028 800VDC 放量，早期通过客户验证的 DC breaker、SST、sidecar power rack 和高压 DC/DC 模块供应商有机会获得远高于传统电气件的利润率。

## 8. 2026 关键变化：最可能放量的 3 个拐点

1. **GB300/NVL72 级整柜交付爬坡，使 100kW+ 机柜从少数项目变成主流订单假设**。这会直接拉动 480V/415V 三相 PDU、高电流 busway、tap-off、液冷兼容机柜和 ORv3/48V 机架母排。

2. **电力设备成为项目排产核心，供应商从卖产品变成卖交期**。Vertiv、Eaton、nVent、Legrand、Schneider、ABB 的 2026Q1 数据已验证订单前置和 backlog 可见度，2026 年设备产能比需求预测更重要。

3. **预制化 power module 和白空间 power POD 进入大型 AI 项目的默认选项**。客户为了加速 time-to-power，会减少现场散件安装，转向工厂预制、模块化吊装、BIM/数字孪生和成套验收。

## 9. 2027 关键变化：最可能放量的 3 个拐点

1. **Rubin/MI400/TPU8/下一代 ASIC 把 rack power 再抬一级，800VDC 从验证走向首批商业项目**。基准情景下 800VDC 仍不是多数，但它会决定边际估值和高毛利新品。

2. **DC 保护、sidecar power rack 和 rack-level energy buffer 成为新 AVL 的争夺点**。一旦客户把这些器件写入 2027-2028 设计规范，首批认证供应商将有强锁定。

3. **AI factory 园区化复制，供电架构从单楼优化变成 GW 级园区标准化**。这会把价值从单个 PDU/母线槽，提升到“低压配电 + 现场能源 + UPS/BESS + 冷却 + 软件”整体方案。

## 10. 头部公司与细分公司清单

### 10.1 低压配电、开关柜、配电板

- 全球头部：Eaton、Schneider Electric、ABB、Siemens、Vertiv、GE Vernova、Powell Industries、Hubbell、Mitsubishi Electric、Fuji Electric、LS Electric、Hyosung Heavy Industries。
- 中国和亚洲重要供应商：Huawei Digital Power、Delta Electronics、Chint/正泰、上海良信、德力西、大全集团、特变电工、科华数据、科士达、LS Electric、Hyundai Electric。
- 高密数据中心/项目型供应商：Eaton/Fibrebond、Vertiv Integrated Power Modules、Schneider prefabricated solutions、Siemens/Rittal、ABB + Maverick Power、Powell、Hubbell。

### 10.2 母线槽、busway、tap-off

- 高端数据中心：Legrand Starline、Legrand Zucchini、Legrand XCP、Schneider Canalis/I-Line、Eaton Pow-R-Way III、Siemens SIVACON 8PS、ABB、EAE Elektrik、LS Electric、Rittal RiLineX、nVent ERIFLEX。
- 细分优势：Starline 在数据中心 overhead track busway 心智强；Eaton 和 Schneider 在北美低压成套和工程渠道强；Siemens/Rittal 在 IEC 市场和标准化 sidecar/低压系统上发力；EAE 在欧洲、中东和亚洲 busbar trunking 有竞争力。
- 中国供应商：正泰、良信、大全、华鹏、威腾电气、川开电气、香江科技等；国产替代和本地交付有优势，但高端 hyperscaler AVL 仍需要时间。

### 10.3 Rack PDU、智能 PDU、环境传感

- 头部：Legrand Raritan、Legrand Server Technology、Vertiv Geist、Schneider APC、Eaton/Tripp Lite、Panduit、Leviton、CyberPower、Enlogic、Austin Hughes、ATEN、Rittal。
- 细分优势：Legrand/Raritan/Server Technology 在高密智能 PDU、HDOT、Xerus 固件和数据中心客户基础强；Vertiv Geist 与 Vertiv power/cooling 成套协同；Schneider APC 在企业和 colo 渠道强；Panduit/Leviton 在布线、连接和机柜生态有优势。
- 中国和 ODM：Yosun、克莱沃、海悟、科士达、科华、华为数字能源相关生态、部分台湾/大陆 PDU ODM；价格和定制灵活，但高端客户认证是主要门槛。

### 10.4 ORv3/48V rack busbar、power shelf、连接器

- Power shelf/电源：Delta、Lite-On、Advanced Energy/Artesyn、Bel Power、AcBel、Murata、Flex Power、Chicony、FSP、Vicor、MEAN WELL 高端线。
- 机架/母排/连接器：Meta/OCP、Legrand、Rittal、Flex、BizLink、Amphenol、TE Connectivity、Molex、Rosenberger、Samtec、nVent。
- 生态平台：OCP、Meta Open Rack、AMD Helios/Open Rack Wide、NVIDIA MGX/GB/Rubin rack、Google/AWS/Microsoft 自有 rack 标准。

### 10.5 800VDC、固态保护、sidecar power rack

- 系统推动者：NVIDIA、Vertiv、Eaton、Schneider Electric、ABB、Delta、Siemens/Rittal、Huawei Digital Power。
- 功率半导体和控制：TI、Infineon、STMicroelectronics、Navitas、onsemi、Wolfspeed、ROHM、Renesas、Analog Devices、MPS、Innoscience。
- SST/固态保护/新架构：DG Matrix、Eaton/Resilient Power Systems、ABB、Schneider、Siemens、Delta、Vertiv、部分高校/电力电子初创公司。

### 10.6 预制模块、EPC、安装与服务

- 预制电力模块：Vertiv、Schneider、Eaton/Fibrebond、ABB、Siemens/Rittal、Delta、Huawei Digital Power、Mitsubishi、Powell。
- EPC/机电安装：Quanta Services、EMCOR、MYR Group、MasTec、Fluor、Jacobs、AECOM、Kiewit、DPR Construction、Holder Construction、Turner、Skanska、Mortenson。
- 价值判断：EPC 毛利通常不如智能硬件高，但在 2026-2027 交付瓶颈中，掌握大型项目人力和 commissioning 能力的公司有很强订单可见度。

## 11. 投资价值排序

| 排名 | 子方向 | 2026 确定性 | 2027 弹性 | 毛利/ROIC | 投资评价 |
|---:|---|---|---|---|---|
| 1 | 高端智能 rack PDU + 传感 + API | 高 | 高 | 高 | 单价上移、客户认证锁定、软件化，最适合捕获高毛利 |
| 2 | 高电流 busway + tap-off | 很高 | 中高 | 中高 | 订单确定性强，tap-off 和高电流产品供需紧 |
| 3 | 低压 switchgear/switchboard 成套 | 很高 | 中高 | 中高 | 交期和 backlog 强，但项目制和原材料影响毛利 |
| 4 | 预制化电力模块/eHouse | 高 | 很高 | 中 | time-to-power 价值巨大，适合大公司成套能力 |
| 5 | ORv3/48V rack busbar/power shelf | 中高 | 很高 | 中 | hyperscaler 放量强，但大客户压价，需要规模和认证 |
| 6 | 800VDC/固态保护/sidecar | 低到中 | 极高 | 很高 | 2026 收入小，2027-2028 弹性最大，适合寻找早期技术赢家 |
| 7 | 电力监控软件/DCIM | 中 | 高 | 很高 | 容易被低估，关键在是否能接入 hyperscaler/colo 真实运维系统 |

最强 2026 α 是 **高端智能 PDU、busway/tap-off、低压 switchgear、预制电力模块**；最强 2027 β 是 **800VDC、sidecar power rack、固态保护、rack energy buffer、AI-aware power orchestration**。

## 12. 主要来源与校验

| 来源 | 关键事实/用途 |
|---|---|
| [NVIDIA 800 VDC Architecture](https://www.nvidia.com/en-us/data-center/technologies/800-vdc-architecture/) | 800VDC 架构、减少转换级数、降低电流/铜/线缆体积、支持未来 AI factory |
| [NVIDIA 800VDC Technical Blog](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) | 2027 起支持 1MW rack、合作伙伴名单、54V 架构在 200kW+ 后的限制 |
| [Vertiv Q1 2026 Results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx) | 2026Q1 销售 $2.65B、同比 +30%、Americas 有机增长强、全年指引上调 |
| [Vertiv 2026 Manufacturing Expansion](https://investors.vertiv.com/news/news-details/2026/Vertiv-Announces-Expansion-of-Manufacturing-Capacity-Spanning-Infrastructure-Solutions-Power-and-Rack-Systems-to-Meet-Rising-Demand/default.aspx) | 美洲 4 个新增/扩建制造设施，基础设施、power management、integrated cabinets 扩产 |
| [Eaton Q1 2026 Results](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html) | Electrical Americas 订单/积压和数据中心动能，低压电气成套需求验证 |
| [Eaton Q1 2026 Analyst Presentation](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf) | Electrical Americas 数据中心订单、backlog、产能扩张和 AI 基础设施口径 |
| [Schneider Electric Q1 2026 Revenues](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026) | Q1 收入 €9.767B、有机 +11.2%，Energy Management 和 Systems 由 data center 拉动 |
| [ABB Q1 2026 Press Release](https://library.e.abb.com/public/dd7e26e13f7a4a4783979a725ef8ff7e/ABB-Q1-2026-press-release-English.pdf) | Electrification 订单 $6.647B、同比 +51%，数据中心订单三位数增长 |
| [Legrand Investors - Q1 2026](https://www.legrand.com/en/investors-and-shareholders) | Q1 2026 销售 excl. FX +18%，有机 +9.3%，调整后经营利润率 20.7%，数据中心并购持续 |
| [nVent Q1 2026 SEC filing](https://www.sec.gov/Archives/edgar/data/1720635/000162828026029098/q12026nvtpressrelease.htm) | Q1 2026 销售、订单、backlog、数据中心灰白空间需求验证 |
| [Legrand AI Data Center Solutions](https://www.legrand.us/markets/data-center/artificial-intelligence-solutions) | AI 高密机柜、Starline busway、Raritan/Server Technology 智能 PDU 产品路径 |
| [Legrand Raritan rack PDU](https://www.legrand.us/critical-power-and-infrastructure/rack-power-distribution/raritan-intelligent-pdus) | rPDU 支持 12A-125A、最高 480/277V 三相、最高约 86.6kW、HDOT Cx 和智能控制器 |
| [Legrand Starline T5 busway](https://www.legrand.com/datacenter/gb-en/grey-space/busbar-busway/starline-track-busway/t5-series-250-1250-amp-busway) | T5 250A-1250A、最高 600V、UL857/IEC 61439-6 等认证 |
| [Eaton Pow-R-Way III busway](https://www.eaton.com/us/en-us/catalog/low-voltage-power-distribution-controls-systems/pow-r-way-III-busway.html) | 低压 busway 最高 5000A 铜、600V、200kA，数据中心 grey space 应用 |
| [Siemens and Rittal Partnership](https://press.siemens.com/global/en/pressrelease/siemens-and-rittal-enter-strategic-partnership-data-center-energy-infrastructure) | 2026 年合作开发数据中心标准化电力基础设施和 power rack，AI 机柜 100kW+ 成常态 |
| [Delta Data Center World 2026](https://www.delta-americas.com/en-US/news/delta-unveils-integrated-power%2C-cooling%2C-and-infrastructure-architecture-for-ai-data-centers-at-data-center-world-2026) | 800VDC、rack 内高密 DC power shelf、最高 1.1MW/rack、98% 效率路线 |
| [Grand View Research rack PDU market](https://www.grandviewresearch.com/industry-analysis/data-center-rack-power-distribution-unit-pdu-market) | Rack PDU 公开市场报告口径：2025 $2.81B，2026 $3.06B，2033 $5.87B |
| [Grand View Research busway segment](https://www.grandviewresearch.com/horizon/statistics/data-center-power-market/solution/busway/global) | 数据中心 busway 窄口径市场：2025 $404M，2035 $2.058B，CAGR 17.9% |
| [IEA Key Questions on Energy and AI](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) | 数据中心用电 2025 年增长 17%，AI-focused 数据中心用电增长 50%，2030 数据中心用电约 950TWh |
| [JLL 2026 Global Data Center Outlook](https://www.jll.com/en-us/newsroom/global-data-center-sector-to-nearly-double-to-200gw-amid-ai-infrastructure-boom) | 全球数据中心容量到 2030 接近翻倍至 200GW，AI 设施功率密度和租金溢价 |
| [CBRE 2026 Data Centers Outlook](https://www.cbre.com/insights/books/us-real-estate-market-outlook-2026/data-centers) | 美国数据中心需求、空置率、电力可得性和 2026 租赁活动背景 |
| [Tom's Hardware / Bloomberg-Sightline summary](https://www.tomshardware.com/tech-industry/artificial-intelligence/half-of-planned-us-data-center-builds-have-been-delayed-or-canceled-growth-limited-by-shortages-of-power-infrastructure-and-parts-from-china-the-ai-build-out-flips-the-breakers) | 美国 2026 数据中心项目延期、电力设备交期和变压器/switchgear 约束的二手交叉验证 |
| 项目内 `ai_chip_research_2026_2027.md` | 2026-2027 AI 芯片出货/技术路线、GB300/Trainium/TPU/MI350/MI400/MTIA/Maia 等平台假设 |
| 项目内 `AI数据中心建设规模与产业链订单映射_2026-2027_美国.md` | AI 数据中心 CapEx、电力与能源订单、机柜/母线槽/配电单元订单池基准 |

## 13. 读数注意事项

1. 公开市场报告中的 rack PDU 和 busway 规模偏窄，通常只统计标准产品出厂收入；AI 项目中的成套电力模块、tap-off、插接箱、工程集成、监控软件和加急交付会显著放大实际订单口径。
2. 800VDC 是高弹性方向，但 2026 年不要把发布会样机等同于大规模收入。基准情景中 2027 年仍是小批量，乐观和极度乐观情景才假设其进入多客户项目。
3. 本文故意采用对 AI 算力建设偏乐观的假设：hyperscaler、OpenAI/Stargate、Meta、AWS、Google、Microsoft、Oracle、CoreWeave 等会继续抢电、抢设备、抢工期；若 AI ROI 或融资环境明显恶化，实际值会向基准区间下沿靠拢。
4. 非投资建议。本文用于产业链研究和情景分析，关键风险包括 AI 需求低于预期、GPU/HBM/CoWoS 延迟、电力并网受阻、关税和进口限制、数据中心社区反对、供应商扩产后价格竞争、800VDC 标准化低于预期。
# 行业调研：【数据中心电力接入与高压变电】

> 版本日期：2026-05-08  
> 研究口径：以美国/北美 AI 数据中心为主，美元名义值；全球市场可粗略按北美口径的 1.6-2.0x 做映射。市场规模多采用“新增订单/签约额”口径，不等同于当期收入确认，也不等同于云厂商 CapEx。  
> 需求底座：项目内《全球 AI 芯片路线图与 2026-2027 产能释放预测》和《AI数据中心建设规模与产业链订单映射》作为算力侧基础假设；外部资料重点补充 2026 年行业报告、一手公司公告、订单和高管口径。  
> 核心立场：本报告对 2026-2027 AI 计算中心建设保持非常乐观。直接数据缺口处采用“大胆但可解释”的上沿假设，并在表格中区分基准、乐观、极度超预期乐观三种情景。

## 0. 结论先行

数据中心电力接入与高压变电已经从“土建配套”升级为 AI 基础设施的第一瓶颈和第一先行订单。2026 年最确定的路径不是科幻式全直流，而是更朴素也更赚钱的组合：115/138/230/345/500kV 接入、园区主变电站、大型电力变压器、MV/HV switchgear、模块化 e-house/电力 skid、busway、UPS/BESS、电能质量设备、并网 EPC，以及部分现场燃气/燃料电池/储能形成的微电网。

需求侧锚点非常密集：TrendForce 在 2026-05-06 将全球 Top 9 CSP 2026 CapEx 上调至约 **$830B**；JLL 预计 2026-2030 全球新增约 **100GW** 数据中心容量、总投入可接近 **$3T**；IEA 称 2025 全球数据中心用电 **485TWh**，2030 约 **950TWh**，其中 AI-focused 数据中心用电增长更快；CBRE 指出 2026 美国租赁活动有望创新高、预租率预计维持 **mid-70%**；Uptime 2026 giant data center 统计显示 2025 公布的 >100MW 巨型园区规划功率达 **181GW**，其中约 **60%** 由 AI 驱动，北美占最大头。

供给侧也已经在一手财报里兑现：GE Vernova 2026Q1 Electrification 订单 **$7.1B**、同比有机增长 **+86%**，单季数据中心电气设备订单 **$2.4B**，超过 2025 全年；Eaton Electrical Americas 2026Q1 data center 订单 **+约240%**，backlog 同比 **+44%**；Vertiv 2026Q1 销售 **$2.65B**、同比 **+30%**，美洲有机增长 **+44%**，2026 全年有机增长指引 **+29%-31%**；nVent 2026Q1 backlog **$2.6B**，有机订单 **+约40%**，数据中心灰空间/白空间都在增长；Quanta 2026Q1 backlog **$48.5B**；Powell 2026 财年 Q2 backlog **$1.8B**，并在季后拿到超过 **$400M** 的绿色地数据中心 mega order。

我的行业判断：2026 是“电力设备先锁单”的年份，2027 是“AI Factory 多园区复制 + 电力架构升级”的年份。短期最有确定性的是变压器、MV/HV 开关柜、模块化变电站和电气 EPC；弹性最大的是 BESS/微电网、电能质量、800VDC/LVDC、数字孪生与负载柔性调度；长期最可能保持高 ROIC 的是“受认证保护的高压设备 + 模块化 power block + 数字化控制/服务”这一层。

## 1. 行业机会、挑战与 2026-2027 技术路径

### 1.1 AI 计算中心建设带来的机遇

1. **从“卖设备”变成“卖交付时间”。** 大型 AI 园区的收入机会不是单台变压器，而是把 100MW、500MW、1GW 级负载从公告推进到可上电。JLL 给出的 2026 全球 shell/core 建设成本为 **$11.3M/MW**，AI 租户 IT fit-out 还可达 **$25M/MW**，电力接入只占总 CapEx 的小部分，但延迟会冻结整个项目。
2. **长交期设备具备订单前置属性。** 变压器、GIS/AIS、高压断路器、MV switchgear、保护控制、BESS 和现场发电并网设备通常需要在土建前锁定。Wood Mackenzie 口径经 APPA 转述称美国数据中心电气设备关键部件交期 **18-36 个月**，约 **600GW** 数据中心项目仍在找电力容量，已有电力或施工/供电协议的约 **183GW**。
3. **AI 芯片路线强化高密功率趋势。** 项目内芯片资料显示 2026 最大量的 B300/GB300、Trainium2、TPU v7、GB200、Ascend、MI350、Trainium3、MTIA、Maia200 等都会推高 rack 功率与瞬态负载。GB300 NVL72 供应商资料显示单 rack 约 **132-140kW**；Rubin/Vera Rubin 在 2026H2 出货后，会推动更强的 rack-level energy storage 和动态功率管理。
4. **电力架构成为芯片生态的一部分。** NVIDIA Vera Rubin DSX 明确把 power/cooling/compute 联动；NVIDIA 称 DSX Max-Q 可在固定电力数据中心部署 **30%** 更多 AI infrastructure，并释放 **100GW** stranded grid power。Eaton、Hitachi Energy、Vertiv、Siemens 都在围绕“grid-to-chip”做参考设计、数字孪生和模块化方案。
5. **现场能源和电网柔性从备选变成主线之一。** Uptime 统计 2025 >100MW 巨型园区规划中，约 **68%** 仍想用 grid-only，**28%** 是 grid plus onsite energy，**4%** off-grid；但其也指出超过一半老项目处于 stalled/delayed/uncertain。2026-2027 真实落地会倒逼 BESS、燃气轮机、燃料电池、可中断负荷、负载迁移进入标准方案。

### 1.2 核心挑战

| 挑战 | 2026 表现 | 投资含义 |
|---|---|---|
| 大型变压器交期 | 公开资料显示 LPT/GSU 交期常见 80-210 周；2026 数据中心项目更愿意抢 factory slot | 价格、预付款、框架协议、二级供应商认证成为 alpha |
| 并网队列和公用事业审批 | 大负荷 study、网络升级、成本分摊、社区反对拉长周期 | 已获电力的园区、EPC 和 utility-facing 工程商议价更强 |
| 保护与电能质量 | AI workload 有快速功率波动，GPU 集群上电/降载对电压、谐波、无功、短路容量提出新要求 | STATCOM、同步调相机、电容器组、保护继电器、BESS load shaping 增长 |
| 供应链材料 | GOES、铜、铝、HV bushing、tap changer、真空灭弧室、BESS 电芯/PCS、控制芯片 | 高端电力设备不是简单扩产，材料和认证决定速度 |
| 人才和施工 | 保护工程师、继电保护调试、HV 测试、变电站施工、线路工、项目经理短缺 | Quanta/MYR/EMCOR/Turner/Kiewit 等具备 craft labor 平台优势 |
| 政策与社会接受度 | 电价、用水、天然气、碳排、居民反对、PJM/NYISO 等大负荷规则变化 | 负载柔性、bring-your-own-power、长期 PPA、社区收益方案更重要 |

### 1.3 2026 最可能放量的技术路径

| 技术路径 | 2026 成熟度 | 2026 放量概率 | 说明 |
|---|---:|---:|---|
| 传统 AC 高压接入 + 园区主变电站 | 极高 | 极高 | 115/138/230/345/500kV 接入，主变降到 34.5/13.8kV，再进 MV 配电，是 2026 绝对主流 |
| 大型液浸式/干式变压器 + MV/HV switchgear | 极高 | 极高 | 所有已开工项目必需，价格和交期是关键 |
| 模块化 e-house / prefabricated power module | 高 | 高 | Eaton、Vertiv、Schneider、Siemens 等都在推，核心价值是缩短现场施工与调试 |
| BESS + UPS + load shaping | 中高 | 高 | 不只是备电，逐渐用于 ramp-rate control、削峰、并网加速 |
| 现场燃气/燃料电池/微电网 | 中 | 中高 | 对 500MW-1GW 园区尤其重要，但燃机、燃气管线、排放许可仍约束 |
| 数字化保护/SCADA/ETAP/Omniverse/数字孪生 | 高 | 中高 | 2026 先在设计和运维中放量，软件收入体量小但毛利高 |
| SF6-free MV/HV 开关设备 | 中高 | 中 | Schneider 已披露 Power & Grid 对 SF6-free 有 traction；2026 还不是所有地区强制 |
| 800VDC/LVDC 数据中心配电 | 中低到中 | 试点放量 | OCP/Current OS、Eaton/Hitachi/NVIDIA 推动，2026 以 pilot/首批参考设计为主 |
| 固态变压器/SST + MVDC | 低到中 | 低 | 技术价值很大，但 2026 主要是研发、仿真和小规模验证 |

### 1.4 按 AI 芯片路线推演的新技术成熟和放量时间

| 算力平台背景 | 对电力接入/高压变电的要求 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|---|
| 2026 B300/GB300、GB200、Trainium2、TPU v7、MI350 主导 | 100kW+ rack、液冷、34.5kV 园区配电、常规 UPS/BESS、传统 AC 变电站 | AC 变电站和 MV switchgear 2026 全年放量；模块化电力模块 2026H2 加速 | 电力模块与 BESS 绑定采购，2026Q4 形成标准 power block | 大客户直接采购 1GW 级标准化 power train，2026 年内出现多个跨园区复制订单 |
| 2026H2-2027 Rubin、Trainium3、Maia200、MTIA、MI400 导入 | 更强瞬态功率、rack-level energy smoothing、动态功率调度、800VDC 需求出现 | Rubin 电力新架构 2026H2 首批，2027 形成早期订单 | 800VDC/LVDC 在 2027H1 进入 hyperscaler 新建园区设计默认选项之一 | 2027 年 800VDC 直接成为 200kW+ rack 项目的事实标准，传统 LVAC 白空间设计被压缩 |
| 2027 HBM4、Rubin/MI400/TPU8、1.6T/CPO | 更高 rack 密度、更高电力品质、更低转换损耗、数字孪生运维 | 2027H2 power-flex、BESS、数字保护明显上量 | 2027 全年 BESS/STATCOM/软件与主变电站打包采购 | 电网侧允许 AI load 作为可调度资源，数据中心用负载柔性换取更快并网 |

## 2. 已经开始放量的关键产品：市场规模、渗透率、利润率

### 2.1 总市场三情景

这里的“行业总市场”指北美 AI 数据中心电力接入与高压变电子链条的新增订单：LPT/GSU、HV/MV switchgear、GIS/AIS、主变电站 EPC、模块化 power block、保护控制、电能质量、部分 BESS/UPS 并网侧价值。它不包括全部服务器、冷却、发电机销售额，也不包括全部低压白空间配电。

| 时间窗口 | 基准 | 乐观 | 极度超预期乐观 | 推导逻辑 |
|---|---:|---:|---:|---|
| 未来 3 个月 | $9-14B | $14-22B | $22-35B | Q2-Q3 2026 大客户继续抢变压器和 switchgear slot，订单领先施工 |
| 未来 1 年 | $38-55B | $55-78B | $78-115B | 对应 6-9GW 可落地 AI IT load 以及更大的已签 power queue 设备预采 |
| 未来 2 年累计 | $90-145B | $145-220B | $220-360B | 2027 Rubin/ASIC/GB300 二次扩张，BESS/现场能源/模块化 power block 放大 |

### 2.2 已放量产品细分表

| 产品/细分技术 | 当前放量状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年累计市场规模 | 渗透率路径 | 毛利率三情景 |
|---|---|---:|---:|---:|---|---|
| 大型电力变压器/LPT/GSU，50-1000MVA | 最紧缺，交期最长，已进入预付款抢产能 | 基准 $2.0-3.5B；乐观 $3.5-6B；极乐观 $6-10B | 基准 $9-14B；乐观 $14-22B；极乐观 $22-35B | 基准 $24-38B；乐观 $38-60B；极乐观 $60-95B | 真实开工大型园区接近 100%；冗余 N+1/2N 使价值量高于 IT MW | 基准 23-32%；乐观 30-40%；极乐观 38-48% |
| HV GIS/AIS、断路器、隔离开关、继保柜 | 高压站必需，GIS 在土地/可靠性约束场景提升 | $1.5-2.5B；$2.5-4B；$4-7B | $6-10B；$10-16B；$16-26B | $15-24B；$24-40B；$40-65B | 大型站 80-95%；GIS 占比从 25-35% 升至 35-50% | 28-38%；34-45%；42-55% |
| MV switchgear / metal-clad switchgear / switchboards | 34.5kV/13.8kV 园区配电主力，Powell/Eaton/Schneider/ABB 受益 | $2-4B；$4-6B；$6-10B | $8-14B；$14-22B；$22-35B | $20-36B；$36-58B；$58-90B | 所有园区 90-100%；高密 AI 项目单位 MW 价值上升 | 26-36%；32-44%；40-52% |
| 模块化变电站/e-house/power skid | 从“省现场人力”变成“抢上线时间” | $1.2-2.5B；$2.5-4.5B；$4.5-8B | $5-10B；$10-18B；$18-32B | $15-30B；$30-55B；$55-95B | 2026 25-40%；2027 40-60%；极乐观 70%+ | 24-35%；32-45%；40-55% |
| 并网 EPC / 变电站 EPC / T&D 工程 | Quanta、MYR、MasTec、EMCOR、Kiewit 等受益 | $1.5-3B；$3-5B；$5-8B | $7-12B；$12-20B；$20-32B | $18-35B；$35-60B；$60-105B | 已获电力项目 100%；瓶颈是 craft labor | EPC 毛利 10-18%；乐观 14-22%；极乐观 18-26% |
| Busway/母线槽/高密配电连接 | 从低压白空间延伸到高密 power train | $1-2B；$2-3.5B；$3.5-6B | $4-8B；$8-14B；$14-24B | $11-22B；$22-40B；$40-70B | 80-95%；100kW+ rack 提高单位价值 | 25-38%；32-45%；40-52% |
| UPS/BESS 并网侧价值、电池室、PCS、EMS | 备电 + 削峰 + ramp-rate control + 并网加速 | $1.5-3B；$3-6B；$6-10B | $7-14B；$14-26B；$26-45B | $20-42B；$42-80B；$80-140B | 2026 20-35%；2027 35-60%；极乐观 70%+ | BESS 集成 15-25%；乐观 20-32%；软件/控制可 50%+ |
| 电能质量：STATCOM、SVC、电容器组、谐波滤波、同步调相机 | 从电网项目进入大负荷接入包 | $0.8-1.8B；$1.8-3.5B；$3.5-6B | $4-8B；$8-14B；$14-25B | $12-24B；$24-45B；$45-80B | 2026 10-20%；2027 25-45%；极乐观 60% | 30-42%；38-52%；48-62% |
| 保护继电器/SCADA/EMS/数字监控 | 单体小但粘性强，服务 attach 提升 | $0.4-0.9B；$0.9-1.6B；$1.6-3B | $2-4B；$4-7B；$7-12B | $6-12B；$12-22B；$22-40B | 新建站 80-100%；数字化功能渗透从 30% 升至 60%+ | 硬件 30-45%；软件/服务 55-80% |

### 2.3 订单和利润率判断

最强定价权在 **LPT/HV switchgear/MV switchgear/模块化 power block**。原因不是技术参数本身多神秘，而是“认证供应商 + factory slot + 可靠性事故成本 + 长交期”叠加。APPA 转述 Wood Mackenzie 报告称制造商已对一年前 PO 回头要求 **20%** 涨价以维持交付；这说明价格传导已经从材料涨价扩散到“交期溢价”。

利润率上，Eaton 2026Q1 Electrical Americas segment operating margin **25.6%**，2026 指引 **28.8%-29.2%**；Vertiv 2026Q1 adjusted operating margin **20.8%**，全年指引 **22.8%-23.8%**；nVent Q1 adjusted ROS **20.0%**；Powell Q2 gross margin **29.6%**。这些公开一手数字支持“供不应求产品毛利率向 30%-45% 甚至更高冲击”的乐观假设。

## 3. 在研与未来快速增长的关键产品/技术

### 3.1 在研/准放量技术总览

| 技术 | 2026 阶段 | 成熟时间 | 放量时间 | 关键公司 |
|---|---|---|---|---|
| 800VDC / LVDC 数据中心配电 | OCP/Current OS 标准推进，Eaton/Hitachi/NVIDIA 展示 | 基准 2027H2；乐观 2027H1；极乐观 2026Q4 | 基准 2028；乐观 2027H2；极乐观 2027H1 | Eaton、Hitachi Energy、NVIDIA、Schneider、Siemens、ABB、Delta、Vicor、Infineon、TI、Renesas |
| 固态变压器/SST、MVDC power train | 仿真/研发/小规模 pilot | 基准 2028；乐观 2027H2；极乐观 2027H1 | 基准 2029；乐观 2028；极乐观 2027H2 | Eaton、Hitachi、Siemens、ABB、Schneider、GE Vernova、Wolfspeed、Infineon |
| Grid-flex AI load orchestration | NVIDIA DSX Max-Q、Siemens/Emerald AI 合作 | 基准 2026H2；乐观 2026Q3；极乐观 2026Q2 | 2027 成为并网谈判工具 | NVIDIA、Siemens、Emerald AI、Fluence、Schneider ETAP、GE GridOS、Hitachi HMAX |
| Rack-level energy smoothing / 超级电容 | NVIDIA Vera Rubin 400J/GPU closed-loop | 2026H2 Rubin 出货即成熟 | 2027 随 Rubin/高密 rack 放量 | NVIDIA、Eaton、Vertiv、KULR、Skeleton、Maxwell/Tesla 生态、电容/电源模块商 |
| SF6-free MV/HV switchgear | 商业化但数据中心渗透早期 | 2026 已成熟 | 2027 在 ESG/法规驱动下加速 | Schneider、Hitachi、Siemens Energy、ABB、GE Vernova、Mitsubishi、Eaton |
| Digital twin for grid-to-chip | Omniverse DSX、ETAP、PhysicsX/HMAX | 2026 已可商用 | 2026H2-2027 设计标准化 | NVIDIA、Eaton、Vertiv、Hitachi、Siemens、Schneider/ETAP、Bentley |
| Grid-forming BESS / STATCOM for AI campuses | 电网侧成熟，数据中心侧渗透提升 | 2026 已成熟 | 2026H2-2027 放量 | Fluence、Tesla、Wartsila、Sungrow、Powin、GE Vernova、Hitachi、Siemens、ABB |

### 3.2 在研产品三情景市场规模与利润率

| 技术/产品 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年累计市场规模 | 渗透率路径 | 利润率三情景 |
|---|---:|---:|---:|---|---|
| 800VDC/LVDC 电力架构 | 基准 $0.1-0.3B；乐观 $0.3-0.8B；极乐观 $0.8-1.5B | $0.8-2B；$2-5B；$5-10B | $4-10B；$10-25B；$25-55B | 2026 <5%；2027 5-15%；极乐观 25%+ 新建高密 rack | 早期毛利 35-50%；乐观 45-60%；极乐观 55-70% |
| SST/MVDC 转换设备 | $0.05-0.2B；$0.2-0.5B；$0.5-1B | $0.3-1B；$1-3B；$3-6B | $1-4B；$4-12B；$12-30B | 2026 pilot；2027 <5%；极乐观 10% | 40-55%；50-65%；60-75%，但早期研发费用高 |
| Grid-flex / AI 负载柔性软件 | $0.2-0.5B；$0.5-1B；$1-2B | $1-3B；$3-6B；$6-12B | $4-10B；$10-25B；$25-50B | 2026 5-15%；2027 20-45%；极乐观 60% | 软件毛利 60-80%；服务/集成 30-45% |
| Rack-level energy smoothing / 超级电容 | $0.1-0.3B；$0.3-0.8B；$0.8-1.5B | $0.5-2B；$2-5B；$5-10B | $3-8B；$8-20B；$20-45B | 随 Rubin/MI400/GB300 后续 rack 渗透，2027 10-35% | 30-45%；40-55%；50-65% |
| SF6-free GIS/MV switchgear | $0.3-0.8B；$0.8-1.8B；$1.8-3B | $1.5-4B；$4-8B；$8-15B | $5-14B；$14-30B；$30-60B | 2026 10-20%；2027 25-45%；欧洲/部分 hyperscaler 更快 | 35-50%；45-58%；55-65% |
| Digital twin / 电力仿真 / 预测维护 | $0.3-0.7B；$0.7-1.5B；$1.5-3B | $1.5-4B；$4-8B；$8-16B | $5-15B；$15-35B；$35-70B | 2026 20-35%；2027 50-75% | 软件 60-85%；硬件服务混合 35-55% |
| Grid-forming BESS + STATCOM 打包 | $1-2B；$2-4B；$4-7B | $5-10B；$10-20B；$20-35B | $15-35B；$35-75B；$75-140B | 2026 10-25%；2027 30-55%；极乐观 70% | BESS 集成 15-28%；电力电子/控制 30-50% |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能集中在哪里

| 环节 | 主要产能/公司 | 区域结构 | 工艺/能力要点 |
|---|---|---|---|
| 大型电力变压器 LPT/GSU | Hitachi Energy、GE Vernova/Prolec GE、Siemens Energy、ABB、Hyundai Electric、Hyosung、Mitsubishi、Toshiba、Virginia Transformer、WEG、TBEA、华明/特变等 | 美国、墨西哥、加拿大、韩国、日本、欧洲、中国、印度 | GOES 铁芯、铜/铝绕组、绝缘/油箱、HV bushing、tap changer、FAT、重件运输 |
| HV GIS/AIS、断路器 | Hitachi、Siemens Energy、GE Vernova Grid Solutions、ABB、Mitsubishi、Hyosung、Schneider、Eaton | 欧洲、日本、韩国、中国、美国/Mexico 局部 | 高压绝缘、真空/SF6/SF6-free 灭弧、机械寿命、局放测试、型式试验 |
| MV switchgear/e-house | Eaton、Schneider、ABB、Siemens、Powell、Hubbell、Vertiv/E+I、nVent、Legrand、S&C、G&W | 美国、墨西哥、加拿大、欧洲、中国、印度 | 金属铠装柜、母排、保护控制、工厂集成、UL/ANSI/IEC 认证 |
| 模块化 power block | Eaton/Fibrebond/NordicEPOD/Flexnode、Vertiv、Schneider、Siemens、ABB、Legrand、nVent | 美国南部、墨西哥、北欧、欧洲、东南亚 | 预制化、工厂测试、运输尺寸、现场拼装、快速 commissioning |
| 变电站/T&D EPC | Quanta、MYR、MasTec、EMCOR、Kiewit、Burns & McDonnell、Black & Veatch、Bechtel、Jacobs、AECOM、Fluor、DPR/Holder/Turner | 美国本土为主，强区域劳动力网络 | 线路/变电站施工、继保调试、安全记录、工会/非工会劳动力、项目管理 |
| BESS/电能质量 | Tesla、Fluence、Wartsila、Sungrow、Powin、GE Vernova、Hitachi、Siemens、ABB、Schneider、Eaton | 中国、美国、欧洲、韩国、东南亚 | 电芯、PCS、EMS、消防、grid-forming controls、并网测试 |

### 4.2 至少 8 条供给瓶颈

1. **LPT factory slot。** 大型变压器通常定制化程度高，铁芯、绕组、油箱、FAT、运输全部占用稀缺产线。WoodMac/行业口径显示交期已进入 18-36 个月甚至更长区间。
2. **GOES 与铜。** 取向硅钢决定铁芯损耗和效率，铜/铝决定绕组成本。材料涨价可通过 escalation clause 传导，但交付延迟不能简单用钱解决。
3. **HV bushing、tap changer、真空灭弧室和 GIS 关键部件。** 高压设备可靠性要求极高，替代供应商需要型式试验和长周期验证。
4. **保护/控制工程师。** AI 园区不是普通工业负荷，短路容量、谐波、快速 ramp、保护选择性和 NERC/CIP 要求提高工程复杂度。
5. **EPC 和现场调试人才。** 变电站施工、线路工、继保调试、HV testing、安全管理是硬瓶颈。Quanta 这类 craft labor 平台的价值会被重估。
6. **并网 study 和 utility queue。** 即使设备有货，也可能卡在 interconnection、网络升级、成本分摊和地方审批。
7. **重件运输和现场条件。** 大型主变运输受铁路、桥梁、港口、特种车辆、吊装窗口约束，任何一个节点延迟都会拖累 COD。
8. **BESS 电芯/PCS/tariff 风险。** Bloomberg/Tom's Hardware 转述显示美国部分电池进口高度依赖中国，关税和供应链扰动会影响 BESS 作为并网加速工具的可用性。
9. **认证和 approved vendor list。** Utility/hyperscaler 不会轻易换供应商；新进入者即使有产能，也要经历工厂审核、样机、型式试验、现场运行记录。

### 4.3 成本构成和毛利决定因素

| 产品 | 典型成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 大型电力变压器 | GOES/铁芯 20-30%；铜/铝绕组 20-30%；油箱/冷却 10-15%；绝缘油/纸 5-10%；bushing/tap changer/仪表 8-15%；工程/人工/FAT 10-20%；运输 3-8% | factory slot、额定容量、损耗要求、阻抗/短路能力、认证、交期 | 材料 escalator、排产溢价、预付款、框架协议、延期重报价 |
| HV/MV switchgear | 断路器/灭弧 20-30%；母排/铜 15-25%；柜体/绝缘 15-25%；保护控制 10-20%；工程测试 10-20% | 额定短路电流、SF6-free、模块化程度、UL/ANSI/IEC 认证、交付周期 | 铜/钢/tariff 调价、加急费、项目变更单 |
| 模块化 e-house | 内置 switchgear/transformer/UPS 45-65%；结构/暖通消防 10-20%；工程集成 10-20%；运输/吊装 5-10% | 工厂集成能力、标准化设计、客户重复采购、现场节省工期 | 以“缩短 time-to-power”定价，客户愿意付 premium |
| 变电站 EPC | 设备 45-65%；人工 15-30%；土建 8-15%；工程许可 5-10%；contingency 5-15% | 劳动力、项目管理、采购能力、变更单、安全记录 | 成本加成、EPC 固价附 escalation、变更单 |
| BESS/电能质量 | 电芯 45-60%；PCS 12-20%；热管理/消防 7-12%；EMS 5-10%；EPC/并网 10-20% | 电芯价格、PCS 控制能力、消防认证、软件调度、电网服务收入 | 电芯价格传导、availability guarantee、软件订阅/服务 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 环节 | 集中度判断 | 说明 |
|---|---|---|
| LPT/HV GIS | 高，CR5 估计 55-70% 的可认证高端产能 | Hitachi、GE Vernova/Prolec、Siemens Energy、ABB、Hyundai/Hyosung/Mitsubishi 等掌握多数 utility/hyperscaler 认可产能 |
| MV switchgear/e-house | 中高，数据中心可用供应商集中 | Eaton、Schneider、ABB、Siemens、Powell、Vertiv/E+I、nVent 等，普通工业柜厂难直接进入 AI 园区 |
| 变电站 EPC/T&D | 区域分散但头部平台优势强 | Quanta/MYR/MasTec/EMCOR 等拥有劳动力、安全、采购和客户关系 |
| BESS/电能质量 | 中等，电芯较分散但 grid-forming/PCS/EMS 更集中 | Tesla/Fluence/Wartsila/Sungrow/GE/ABB/Siemens/Schneider |
| 数字保护/软件 | 高毛利、客户锁定强 | SEL、Schneider ETAP/EcoStruxure、GE GridOS、Siemens、Hitachi HMAX、ABB Ability |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| 可靠性事故成本 | 一个主变或 GIS 故障可能让 100MW+ AI 园区停机，客户会为低失效率、现场服务和备件付 premium |
| 认证标准 | IEEE/ANSI/IEC/UL、utility AVL、NERC/CIP、hyperscaler 工厂审核使替代供应商导入周期长 |
| 定制工程 | 电压等级、短路容量、阻抗、谐波、保护选择性、现场空间和施工节奏都要定制，不是纯商品 |
| 产能 slot 稀缺 | 交期从 12-18 个月拉长到 18-36 个月甚至更久时，factory slot 本身成为可定价资产 |
| 系统集成 | 模块化 power block 把变压器、开关柜、UPS/BESS、保护、冷却、数字孪生打包，客户买的是确定交付 |
| 切换成本 | 一旦进入设计、保护整定、utility 审批、现场土建，换供应商会重新测试和审批 |
| 资金和履约能力 | 大项目需要担保、预付款管理、长周期 working capital 和 warranty，弱小供应商难承接 |
| 服务网络 | 现场 commissioning、预测维护、紧急维修、备件仓决定生命周期收入和客户粘性 |

### 5.3 价值捕获判断

长期高 ROIC 最可能出现在三层：

1. **受认证保护的高压/MV 设备 OEM。** 变压器和开关柜资本开支较重，但已有产能和客户认证的厂商能把稀缺交期转为价格和预付款。
2. **模块化 power block 与 grid-to-chip 集成商。** Eaton、Vertiv、Schneider、Siemens、ABB、nVent/Legrand 等可以把硬件、工程、软件和服务打包，毛利和客户锁定优于单一设备。
3. **数字保护、仿真、EMS、负载柔性软件。** 单体收入小于设备，但边际毛利高，能嵌入并网许可、运维和电力市场调度，长期 ROIC 最高。

传统 EPC 的毛利率较低，但 Quanta 类平台可能通过劳动力稀缺和供应链能力拿到稳定高 backlog，投资属性更偏“确定性复利”，不是最高毛利。

## 6. 2026 关键变化：拐点与最可能放量方向

1. **电力从约束条件变成选址第一变量。** CBRE 预计 2026 美国数据中心租赁创新高、预租率 mid-70%；但供给交付由 power availability 决定。2026 开始，“有地”不如“有可交付电力”。
2. **设备商财报确认订单超级周期。** GE Vernova、Eaton、Vertiv、nVent、Powell、Quanta 的 Q1/Q2 订单和 backlog 同时上行，说明需求不是停留在论坛和规划图上，而是转化为 PO、backlog 和产能扩张。
3. **grid-to-chip 参考设计进入产业化。** NVIDIA Vera Rubin DSX、Eaton Beam Rubin DSX、Hitachi 800VDC 数字仿真、Vertiv 预制化 power/cooling、Siemens-Emerald-Fluence 负载柔性共同指向：AI 数据中心的电力架构要跟芯片和冷却一起设计。

2026 最可能放量的子方向：**LPT/MV switchgear、模块化 e-house、并网 EPC、BESS/load shaping、保护控制和数字孪生设计工具**。

## 7. 2027 关键变化：拐点与最可能放量方向

1. **Rubin/MI400/TPU8/Trainium3 推动电力架构二次升级。** 2027 rack 功率、瞬态功率和液冷复杂度继续上升，800VDC/LVDC、rack-level energy smoothing、动态功率调度会从示范走向早期规模化。
2. **BESS/微电网成为并网谈判工具。** 2027 不是简单“有备用电源”，而是用 BESS、现场燃气、燃料电池和 AI workload shifting 让大负荷对 utility 更可控，从而换取更快并网。
3. **监管开始重塑项目经济性。** 大负荷 special tariff、可中断电价、bring-your-own-generation、成本分摊和社区收益安排会更普遍。没有电力确定性的 pipeline 会被出清，已获电力和标准化 power block 的资产溢价提高。

2027 最可能放量的子方向：**800VDC/LVDC 早期量产、grid-forming BESS/STATCOM、SF6-free switchgear、数字化运维、现场能源并网包、跨园区标准 power block**。

## 8. 头部公司与细分公司清单

### 8.1 变压器、高压设备、开关柜

| 细分 | 公司 |
|---|---|
| 大型电力变压器/LPT/GSU | Hitachi Energy、GE Vernova/Prolec GE、Siemens Energy、ABB、Hyundai Electric、Hyosung Heavy Industries、Mitsubishi Electric、Toshiba、Virginia Transformer、WEG、HD Hyundai Electric、TBEA、特变电工、中国西电、华明装备、明阳电气、伊戈尔 |
| HV GIS/AIS/断路器 | Hitachi Energy、Siemens Energy、GE Vernova Grid Solutions、ABB、Mitsubishi Electric、Hyosung、Toshiba、Schneider Electric、Eaton、XD Electric、中国西电、Pinggao/平高电气 |
| MV switchgear/switchboards | Eaton、Schneider Electric、ABB、Siemens、Powell Industries、Hubbell、Vertiv/E+I Engineering、nVent、Legrand、S&C Electric、G&W Electric、LS Electric、Hyundai Electric、正泰电器、良信股份 |
| Busway/母线槽/配电连接 | Eaton、Schneider、Siemens、ABB、Vertiv、Legrand/Starline、nVent/ERICO、Hubbell、Leviton、TE Connectivity、Amphenol、Rittal、威腾电气 |
| SF6-free / 环保开关 | Schneider Electric、Hitachi Energy、Siemens Energy、ABB、GE Vernova、Eaton、Mitsubishi、Toshiba |

### 8.2 EPC、工程、模块化集成

| 细分 | 公司 |
|---|---|
| T&D/变电站 EPC | Quanta Services、MYR Group、MasTec、EMCOR、Kiewit、Burns & McDonnell、Black & Veatch、Bechtel、Jacobs、AECOM、Fluor、Primoris、MYR、Mastec |
| 数据中心机电/总包 | DPR Construction、Holder、Turner、Clark、Skanska、Mortenson、JE Dunn、Whiting-Turner、EMCOR、Comfort Systems USA、IES Holdings |
| 模块化电力/e-house | Eaton/Fibrebond/NordicEPOD/Flexnode、Vertiv、Schneider、Siemens、ABB、Powell、nVent、Legrand、Rittal、Delta Electronics |
| 现场能源/燃机接入 | GE Vernova、Siemens Energy、Caterpillar、Cummins、Solar Turbines、Rolls-Royce mtu、Kohler、Generac、Bloom Energy、FuelCell Energy、Plug Power、Enchanted Rock |

### 8.3 储能、电能质量、软件控制

| 细分 | 公司 |
|---|---|
| BESS/PCS/EMS | Tesla Megapack、Fluence、Wartsila、Powin、Sungrow、CATL、BYD、Samsung SDI、LG Energy Solution、GE Vernova、Hitachi Energy、Siemens、ABB、Schneider、Eaton |
| STATCOM/SVC/同步调相机 | GE Vernova、Hitachi Energy、Siemens Energy、ABB、Mitsubishi、NR Electric/南瑞继保、荣信汇科、思源电气 |
| 保护继电器/SCADA/EMS | Schweitzer Engineering Laboratories、GE GridOS、Schneider ETAP/EcoStruxure/AVEVA、Siemens、Hitachi HMAX/Lumada、ABB Ability、Emerson/OSI、AspenTech、南瑞继保、国电南自 |
| AI load flexibility / grid orchestration | NVIDIA DSX、Siemens/Emerald AI、Fluence、Schneider ETAP、GE GridOS、Hitachi HMAX、AutoGrid、Voltus、Enel X、C3.ai |
| 数字孪生/仿真 | NVIDIA Omniverse DSX、Eaton SimReady assets、Schneider ETAP/RIB/AVEVA、Siemens/PhysicsX、Hitachi HMAX、Bentley、Autodesk、Ansys |

### 8.4 800VDC/LVDC、功率半导体与高密电源

| 细分 | 公司 |
|---|---|
| 800VDC/LVDC 架构 | Eaton、Hitachi Energy、NVIDIA、Schneider、Siemens、ABB、Current/OS、OCP、Delta Electronics、Vertiv、Legrand |
| 固态变压器/SST/MVDC | Eaton、Hitachi、Siemens、ABB、Schneider、GE Vernova、Delta、Wolfspeed、Infineon、STMicroelectronics、onsemi、Mitsubishi Electric |
| 电源模块/VRM/电容/超级电容 | Vicor、Delta、Lite-On、Advanced Energy、Bel Fuse、Murata、TDK、Nichicon、Panasonic、KEMET/Yageo、Skeleton Technologies、Maxwell/Tesla 生态、KULR |
| rack power shelves / 高密供电 | NVIDIA ecosystem、Eaton、Vertiv、Delta、Lite-On、AcBel、Chicony、Murata、Flex、Jabil |

## 9. 信息源与数字锚点

| 来源 | 关键事实 | 链接 |
|---|---|---|
| TrendForce/PRNewswire，2026-05-06 | Top 9 CSP 2026 CapEx 上修至约 $830B，年增率从 61% 上调到 79% | [TrendForce press release](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html) |
| JLL 2026 Global Data Center Outlook | 2026-2030 新增约 100GW；总支出接近 $3T；2026 shell/core 建设成本 $11.3M/MW | [JLL](https://www.jll.com/en-uk/insights/market-outlook/global-data-centers) |
| IEA Key Questions on Energy and AI | 2025 数据中心用电 485TWh，2030 约 950TWh；AI-focused 数据中心用电 2025 增长 50% | [IEA](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) |
| CBRE 2026 U.S. market outlook | 2026 美国数据中心租赁活动有望创新高；under-construction 预租率预计 mid-70% | [CBRE](https://www.cbre.com/insights/books/us-real-estate-market-outlook-2026/data-centers) |
| Cushman & Wakefield H2 2025 update | Americas 市场进入 managed growth，增长受政策、资源和基础设施 readiness 影响 | [Cushman](https://www.cushmanwakefield.com/en/united-states/news/2026/02/americas-data-center-market-shifts-to-managed-growth) |
| Uptime Institute 2026 Giant Data Center Analysis | 2025 >100MW proposals 规划功率 181GW；约 60% 由 AI 驱动；北美是最大增量 | [Uptime PDF](https://intelligence.uptimeinstitute.com/sites/default/files/2026-01/UI%20Field%20report%20194_Giant%20data%20center%20power%20plans%20reach%20extreme%20levels.pdf) |
| APPA/Wood Mackenzie | 美国数据中心电气设备市场到 2030 可达 $65B；约 600GW pipeline 仍在找电力容量，183GW 已签施工/供电协议；关键部件交期 18-36 个月 | [APPA](https://www.publicpower.org/periodical/article/us-data-center-electrical-equipment-market-projected-surge-65-billion) |
| GE Vernova 2026Q1 | 总订单 $18.3B、+71%；Electrification 订单 $7.1B、+86%；数据中心电气设备订单 $2.4B，超过 2025 全年 | [GE Vernova Q1 release](https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf) |
| GE Vernova 2026Q1 presentation | Electrification backlog 从 2022 $9B 升至 2026Q1 $42B；HVDC/substations、switchgear、transformers、capacitors 是关键产品 | [GE Vernova presentation](https://www.gevernova.com/sites/default/files/gev_webcast_presentation_04222026.pdf) |
| Eaton 2026Q1 | Electrical Americas data center 订单 +约240%；segment backlog +$4.4B/+44%；Electrical Americas margin 25.6%，2026 指引 28.8-29.2% | [Eaton Q1 presentation](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf) |
| Eaton/NVIDIA 2026 GTC | Eaton Beam Rubin DSX、grid-to-chip、模块化 gigawatt AI factories、800VDC | [Eaton press release](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-collaborates-with-nvidia-to-unveil-its-beam-rubin-dsx-platform.html) |
| NVIDIA Vera Rubin | Vera Rubin full production；DSX Max-Q 固定电力下多部署 30% AI infrastructure，释放 100GW stranded grid power | [NVIDIA press release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) |
| NVIDIA technical blog | Vera Rubin NVL72 2026H2 出货；rack-level energy storage 400J/GPU，6x prior generations | [NVIDIA technical blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) |
| Vertiv 2026Q1 | Q1 net sales $2.65B、+30%；美洲有机增长 +44%；adjusted operating margin 20.8%；2026 全年有机增长 29-31% | [Vertiv Q1 release](https://s205.q4cdn.com/554782763/files/doc_financials/2026/q1/Vertiv-First-Quarter-2026-Earnings-Release.pdf) |
| Vertiv capacity expansion | 美洲新增/扩建 4 个制造设施；South Carolina capacity fully ramped 后约 7x；SmartRun 现场部署时间最高快 85% | [Vertiv release](https://investors.vertiv.com/news/news-details/2026/Vertiv-Announces-Expansion-of-Manufacturing-Capacity-Spanning-Infrastructure-Solutions-Power-and-Rack-Systems-to-Meet-Rising-Demand/default.aspx) |
| Schneider Electric 2026Q1 | Q1 收入 €9.767B、+11.2% organic；Data Center & Networks 需求 double-digit；North America +14.4% organic；Data Center led growth | [Schneider Q1 release](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026) |
| Hitachi Energy CERAWeek 2026 | 北美供应链和技术开发投资超过 $2B；与 NVIDIA 设计/仿真 800VDC；美国 $457M 大型变压器新厂 | [Hitachi Energy](https://www.hitachienergy.com/es/es/news-and-events/press-releases/2026/03/hitachi-at-ceraweek-2026) |
| Siemens 2026 data center ecosystem | 投资 Emerald AI；与 Fluence BESS、PhysicsX 合作，用负载柔性和储能加速数据中心并网 | [Siemens](https://press.siemens.com/global/en/pressrelease/siemens-expands-data-center-partner-ecosystem-scale-next-generation-ai-infrastructure) |
| nVent 2026Q1 | Q1 sales $1.2B、organic +34%；backlog $2.6B；基础设施由数据中心灰/白空间增长驱动 | [SEC exhibit](https://www.sec.gov/Archives/edgar/data/1720635/000162828026029098/q12026nvtpressrelease.htm) |
| nVent manufacturing | 2026 初 Blaine, MN 新 117,000 sqft 液冷数据中心产能；2020 以来部署超过 1GW 液冷 | [nVent release](https://investors.nvent.com/press-releases/press-release-details/2025/nVent-Expands-Data-Center-Solutions-Manufacturing-with-New-U-S--Production-Facility/default.aspx) |
| Powell 2026Q1/Q2 | Q1 data center orders 超 $100M；Q2 backlog $1.8B；季后获得超 $400M data center mega award | [Powell Q1 release](https://powellindustriesinc.gcs-web.com/static-files/5a2af01d-fbd5-4837-a64b-11212ea64dfa) / [Q2 summary](https://www.stocktitan.net/news/POWL/powell-industries-announces-second-quarter-fiscal-2026-4kx5spwkrt8c.html) |
| Quanta Services 2026Q1 | Q1 revenue $7.87B；record backlog $48.5B；utility/generation/large-load TAM through 2030 约 $2.4T | [Quanta Q1 release](https://investors.quantaservices.com/news-events/press-releases/detail/396/quanta-services-reports-first-quarter-2026-results) |
| OCP/Current OS 2026 | OCP 与 Current/OS 推进 LVDC data center power distribution 白皮书、培训和规格，面向 AI workload | [Current/OS PDF](https://currentos.org/wp-content/uploads/2026/04/20260409_OCP-CurrentOS-Alliance-Direct-Current-Adoption-Data-Centers.pdf) |
| pv magazine / BloombergNEF | 大型变压器 100MVA+ 交期较 2019 翻倍，美国价格 +79%；工厂设备扩产交期 2-4 年 | [pv magazine](https://pv-magazine-usa.com/2026/02/27/global-energy-transition-hits-a-hardware-bottleneck/) |

## 10. 投资观察清单

| 观察项 | 为什么重要 | 关键公司 |
|---|---|---|
| LPT backlog、交期、预付款 | 判断稀缺是否持续、价格是否还能上行 | Hitachi、GE Vernova、Siemens Energy、ABB、Hyundai、Virginia Transformer |
| Data center 订单占比 | 判断 AI 是否真实转化为设备订单 | Eaton、Schneider、Vertiv、nVent、Powell、Hubbell |
| 模块化 power block 产能 | 决定能否跨园区复制、缩短 time-to-power | Eaton、Vertiv、Schneider、Siemens、ABB、nVent |
| BESS/负载柔性并网案例 | 决定 2027 是否从 grid-only 转向 flexible load standard | Siemens、Fluence、Tesla、Schneider、GE、Hitachi、NVIDIA |
| 800VDC/LVDC 标准和首批客户 | 决定 2027-2028 新电力架构 alpha | OCP、Current/OS、Eaton、Hitachi、NVIDIA、Schneider |
| utility large-load tariff | 决定数据中心承担电网升级成本的方式 | PJM、ERCOT、MISO、NYISO、Dominion、AEP、Duke、Southern、NextEra |
| EPC craft labor 和安全 | 决定订单能否从 backlog 转收入 | Quanta、MYR、MasTec、EMCOR、Kiewit |

非投资建议。本报告用于产业链研究与情景推演，关键风险包括 AI 需求兑现不及预期、云厂商 CapEx 下修、项目融资收紧、电价/水资源/社区阻力、并网审批延迟、变压器与 switchgear 扩产快于预期导致价格回落、政策和关税扰动。
# 行业调研：【数据中心风冷、冷水机组与HVAC】

> 截至日期：2026-05-08  
> 研究口径：本报告聚焦 AI 计算中心/AI Factory 中的风冷、冷水机组、HVAC、热排放、直接液冷配套设施、CDU、冷板、泵阀、换热、控制软件和运维服务。  
> 重要口径差异：Dell'Oro 的“数据中心液冷市场”是制造商收入口径，2025 年接近 30 亿美元、2029 年约 70 亿美元。本报告的市场规模表是更宽的“AI 数据中心冷却/HVAC 设备+系统集成+提前订单池”口径，包含冷水机组、干冷器、AHU/CRAH、CDU、冷板、管路、控制、现场集成和服务，因此显著大于纯液冷设备口径。  
> 情景基调：按用户要求，对 2026 年 AI 基础设施建设保持非常乐观；没有直接数据的地方，用可追溯的大胆假设，并在表格中给出基准/乐观/极度超预期乐观三情景。

## 0. 一页结论

**最核心判断：2026 年不是“风冷 vs 液冷”的替代年，而是“直接液冷上机架、冷水机组/干冷器/风冷继续承接热排放”的混合架构放量年。** 对 GB300、GB200、Trainium3、Maia 200、Ironwood TPU、MI350/MI400 等高密度平台，服务器侧会快速转向冷板/CDU；但设施侧仍然需要风冷冷水机组、水冷冷水机组、干冷器、CRAH/FCW/RDHx 和控制系统。换句话说，液冷不是消灭 HVAC，而是把 HVAC 从房间级空调升级成“芯片到园区”的热链条工程。

**2026 最可能放量的技术路径：**

1. **单相直接到芯片液冷 + CDU + 冷水机组/干冷器混合热排放**：2026 年主流，2027 年成为 >50kW/rack AI 新建项目的默认配置。
2. **高温冷却水/温水 TCS 环路**：45C 级服务器进水会扩大 free cooling 窗口，但不会让冷水机组消失，因为热浪、回风短路、混合密度机房和冗余可靠性仍需要机械制冷兜底。
3. **3MW+ 空冷/高 lift 冷水机组与 1GW AI Factory 参考设计**：JCI、Carrier、Modine、Munters、Trane、Vertiv 都在把产品语言从“数据中心 HVAC”改成“AI Factory thermal chain”。
4. **预制化 power/cooling pod 与 10MW 级热管理单元**：Vertiv MegaMod HDX 可到 10MW、Schneider/Motivair 单台 CDU 2.5MW 且 10MW+ 级联，说明交付瓶颈正在从单设备转向标准化整段热链。
5. **两相直接液冷和浸没冷却**：2026 仍偏试点/早期订单，2027 在水资源受限、极高热流密度、主权 AI 或专用集群中放量；大规模替代单相冷板更可能在 2028 以后。

**投资价值排序：**

| 排名 | 子方向 | 为什么有投资弹性 |
|---:|---|---|
| 1 | 直接液冷冷板、CDU、快接头、泵阀、漏液检测 | 单机柜功率上升后从“可选件”变“交付前置条件”，客户愿为可靠性/交期付溢价 |
| 2 | 高密度冷水机组、干冷器、热排放系统 | 液冷最终仍要排热；水资源、噪音、热岛和能耗约束使高性能 chillers 价值上升 |
| 3 | 模块化 power + cooling 集成 | AI Factory 进入 100MW-1GW 复制后，现场工程时间比单设备价格更关键 |
| 4 | 控制软件、数字孪生、AI cooling optimization | 冗余机组、冷却环路和 GPU workload 变成动态系统，长期毛利/服务属性更好 |
| 5 | 传统 CRAH/FCW/RDHx/风墙 | 不会消失，但更像稳定增长而非高 alpha，除非绑定高密度 retrofit 和大客户认证 |

### 0.1 最近半年信号：公司公告、论坛和行业报告

| 时间 | 类型 | 信号 | 投资含义 |
|---|---|---|---|
| 2026-01 | 行业报告 | Dell'Oro 预计数据中心液冷制造商收入 2025 接近 $3B、2029 约 $7B，且单相 D2C 仍占主导 | 纯液冷设备口径仍小，但增速最高；本报告的冷却/HVAC 订单池要把 chiller、热排放和集成一起看 |
| 2026-01 | 公司发布 | Schneider/Motivair 发布 2.5MW MCDU-70，支持 10MW+ 级联 | CDU 从 rack/row 级向 AI Factory 标准模块演进 |
| 2026-02 | AHR Expo/公司发布 | Johnson Controls 预览 YORK YK-HT，强调高 lift、零水耗热排放、噪声降低 | 冷水机组厂商正在围绕缺水、噪声、热岛重新定义数据中心 chiller |
| 2026-02 | 公司发布 | Trane 宣布收购 LiquidStack，3 月完成 | 传统 HVAC 巨头补齐 D2C/浸没冷却，从中央机房打到芯片侧 |
| 2026-03 | NVIDIA GTC | NVIDIA 发布 Vera Rubin DSX AI Factory reference design 和 Omniverse DSX Blueprint | 电力、冷却、施工、控制软件进入同一参考设计，供应商被“设计锁定”的价值上升 |
| 2026-03 | 公司发布 | Ecolab 约 $4.75B 收购 CoolIT，估值 29x NTM EBITDA | 液冷资产估值被 AI 基建重估，冷却 + 水化学 + 服务一体化成为新叙事 |
| 2026-04 | 公司财报 | Carrier Q1 2026 数据中心订单增长 >500%；Trane backlog $10.7B；Vertiv backlog $15B | 需求不是 PPT，已经进入头部 HVAC/电力/热管理公司的订单和 backlog |
| 2026-04 | 行业观点 | Uptime Institute 提醒液冷不会覆盖所有低密度 IT，主要由高 rack density 和 high heat flux 驱动 | 风冷和传统 HVAC 仍有存量和低中密度增量，投资上应避免“一刀切液冷替代” |

## 1. AI 芯片路线对冷却路径的约束

项目内已有 AI 芯片底稿显示，2026-2027 年初出货量和价值权重最高的平台主要是：NVIDIA B300/GB300 Blackwell Ultra、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon MLU 590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200，以及 2026 下半年早期导入的 AMD MI400/Helios 和 NVIDIA Rubin。冷却行业的关键不是“芯片名”，而是这些平台共同把 rack power 从传统 10-30kW 推向 50kW、100kW、150kW 甚至更高。

| AI 平台 | 2026-2027 状态 | 对冷却/HVAC 的直接含义 |
|---|---|---|
| NVIDIA GB300/B300 Blackwell Ultra | 2026 主力放量 | NVL72/整柜级系统推动全液冷、rack CDU、低压损冷板、100kW+ 机柜、二次侧冷却环路 |
| NVIDIA GB200/B200 | 既有订单延续 | 高密度液冷 rack 已成熟，仍会拉动 CDU、冷板、冷水机组和风液混合改造 |
| NVIDIA Rubin / Rubin DSX | 2026 H2 首批，2027 加速 | DSX 参考设计使电力、冷却、数字孪生和标准模块一起进入客户设计锁定 |
| AWS Trainium2/3 | Rainier 和 Trn3 UltraServer 放量 | 自研 ASIC 大规模集群同样需要液冷/风液混合，设施侧更重视端到端效率和自有运维 |
| Google Ironwood TPU / TPU8 | TPU v7 规模部署，TPU8 早期 | 自有数据中心可内化热设计，温水环路、AI Hypercomputer、光/电/热协同更强 |
| Microsoft Maia 200 | 3nm、216GB HBM3E、闭环液冷 | Hyperscaler 自研芯片也直接验证“closed-loop liquid cooling”会进入云厂商标准栈 |
| AMD MI350 / MI400 Helios | MI350 确定放量，MI400 2026 H2 起步 | MI350 可覆盖风液混合和 PCIe/UBB；MI400/Helios 更接近全液冷 rack-scale |
| Meta MTIA / OpenAI-Broadcom ASIC | 2026-2027 GW 级导入 | 推理 ASIC 不一定单芯片最热，但规模会把园区级热排放和电力调度推到前台 |
| 中国 Ascend/Cambricon/国产 GPU | 国产替代推动大规模集群 | 由于单芯片能效与互连差异，集群规模和冗余可能更大，风液混合和冷水机组需求不弱 |

### 1.1 技术成熟与放量时间

| 技术路径 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观/极度超预期 |
|---|---|---|---|---|---|
| 单相直接到芯片液冷 | >50kW/rack 新建 AI 项目主流；GB200/GB300、Trainium、TPU、Maia 等优先采用 | CDU、冷板、快接头交付跟上，成为 100kW 级 rack 默认配置 | 大客户把 2027 需求前置，冷板/CDU 出现供不应求溢价 | >75% 新建高密 AI rack 采用 | >90% 新建高密 AI rack 采用，液冷从 GPU rack 延伸到网络/内存/电源 |
| 风液混合：D2C + CRAH/FCW/RDHx | 2026 最主流工程形态 | 标准化设计模板复制，retrofit 加速 | 老机房局部改造也快速上量 | 标配 | 成为大多数 AI data hall 的基础架构 |
| 高温水/温水 TCS loop | 45C 级趋势扩大 free cooling 窗口 | 温水 loop 与干冷器结合，降低 PUE/WUE | 部分地区开始 chiller-light 方案 | 进入标准设计 | 在凉爽/缺水地区成为优先方案，但热浪地区仍保留机械制冷 |
| 3MW+ 空冷/水冷冷水机组 | JCI YDAM、Modine TurboChill 3+MW、Carrier 30CF 等加速导入 | 供给紧张，交期/认证成为瓶颈 | 3MW+ 机型被 100MW+ 园区提前锁单 | 大规模交付 | 4-5MW 级单机与高 lift 产品进入下一轮竞争 |
| 预制化 10MW power/cooling pod | Vertiv MegaMod HDX、Schneider/Motivair 10MW+ CDU 架构放量初期 | 客户为 time-to-power 付溢价 | AI Factory 复制使标准 pod 订单前置 | 放量 | 标准化热链产品成为头部客户指定架构 |
| 两相直接到芯片 | ZutaCore、Accelsius 等试点/早期订单 | 水资源受限项目采用 | 单相冷板在局部热流密度上遇到边界，头部客户扩大测试 | 小规模量产 | 2027 H2-2028 开始更明确放量 |
| 浸没冷却 | 特定 HPC/边缘/高密封闭场景 | 部分新建专用园区试点 | 如果 GPU/OEM 认证突破，订单弹性较大 | 仍为选择性方案 | 极度乐观下可在 2027 H2 出现若干 MW 级集群 |
| 微流道/封装内冷却 | 实验室/早期工程 | Hyperscaler 自研芯片小批验证 | 先进封装与冷却协同设计提前 | 2027 仍偏研发 | 2028-2029 才可能规模化 |

## 2. 已经开始放量的关键产品

### 2.1 未来 3 个月、1 年、2 年订单池与渗透率

口径：以下为全球 AI 数据中心相关冷却/HVAC **累计订单池**，包含设备、系统集成和部分服务，不等同于当期收入；渗透率指在新建或重大改造 AI 高密度项目中的采用率。

| 已放量产品 | 未来 3 个月订单池 | 未来 12 个月订单池 | 未来 24 个月订单池 | 渗透率路径：基准/乐观/极度超预期 | 增长预测 |
|---|---:|---:|---:|---|---|
| 高密度空冷冷水机组、free-cooling chiller、干冷器 | 基准 $4-7B；乐观 $6-10B；极度 $8-14B | 基准 $16-28B；乐观 $24-40B；极度 $35-60B | 基准 $35-65B；乐观 $55-95B；极度 $85-150B | 新建 AI 园区 45-60% / 55-70% / 70%+ 采用高效空冷或混合热排放 | 2026-2027 年复合增速 25-60% |
| 水冷离心机组、冷却塔/闭式塔、水侧系统 | $3-6B / $5-8B / $7-12B | $14-26B / $20-35B / $30-50B | $30-60B / $45-85B / $70-130B | 大型园区 50-65% / 60-75% / 75%+；水资源受限地区改用干冷/空冷 | 20-45%，受水权和 WUE 约束 |
| 单相 D2C：冷板、CDU、manifold、快接头 | $1.8-3.5B / $3-5.5B / $5-8B | $6-11B / $9-16B / $14-24B | $16-30B / $26-48B / $40-75B | >50kW/rack 新建 AI rack 55-70% / 70-85% / 85%+ | 45-90%，最具 beta |
| RDHx、风墙、CRAH/CRAC 高效风侧系统 | $2.5-5B / $4-7B / $6-10B | $10-20B / $15-28B / $22-40B | $22-45B / $35-65B / $55-95B | 所有 AI data hall 仍有 70-90% 需要风侧余热、存储、网络、电源冷却 | 15-35%，retrofit 强 |
| 模块化 power+cooling pod、预制化白空间热链 | $3-7B / $5-10B / $8-15B | $12-25B / $20-40B / $35-65B | $30-60B / $55-100B / $90-170B | 新建 100MW+ AI 园区 25-40% / 40-60% / 60%+ | 50-100%，time-to-power 溢价高 |
| 冷却控制、传感器、漏液检测、数字孪生、运维服务 | $0.8-1.8B / $1.2-2.8B / $2-4B | $4-8B / $6-12B / $10-18B | $10-22B / $18-35B / $30-55B | 高密 AI 项目 40-60% / 60-80% / 80%+ | 40-80%，软件和服务毛利最好 |

### 2.2 毛利率情景

| 产品 | 当前毛利率：基准 | 乐观 | 极度超预期乐观 | 为什么可能定价 |
|---|---:|---:|---:|---|
| 冷板/快接头/液冷歧管 | 35-45% | 45-55% | 55-65% | 芯片/板级验证周期长，泄漏风险不可接受，客户重视可靠性高于单价 |
| CDU：rack/row/facility | 28-38% | 35-45% | 45-55% | 泵、换热、控制、冗余和现场调试一体化；交期紧时可溢价 |
| 空冷/水冷大型冷水机组 | 25-35% | 32-42% | 40-48% | 3MW+、高 lift、低 GWP、磁悬浮/变频和极端环境测试形成门槛 |
| 干冷器、热交换器、冷却塔 | 20-30% | 28-38% | 35-45% | 热排放容量成为园区瓶颈，微通道、低噪声、低水耗方案有溢价 |
| CRAH/FCW/RDHx/AHU | 20-30% | 28-35% | 35-42% | 定制化、现场适配和大客户认证可改善毛利，但金属加工属性较重 |
| 预制化 power/cooling 模块 | 18-28% | 25-35% | 35-45% | 价值在工程压缩、系统责任和项目交付确定性，而不是单个设备 |
| 控制软件/数字孪生/运维服务 | 45-65% | 60-75% | 70-85% | 绑定全生命周期，数据闭环和运维 SLA 带来复购/订阅属性 |

## 3. 在研和早期放量的关键产品

| 在研/早期技术 | 2026 阶段 | 未来 3 个月订单池 | 未来 12 个月订单池 | 未来 24 个月订单池 | 渗透率路径 | 毛利率假设 |
|---|---|---:|---:|---:|---|---|
| 两相直接到芯片：ZutaCore、Accelsius 等 | 早期商用/试点 | $0.2-0.6B / $0.4-1.0B / $0.8-2.0B | $1-3B / $2-5B / $4-9B | $4-10B / $8-18B / $15-35B | 2026 <5%；2027 基准 5-10%、乐观 10-18%、极度 20%+ | 45-65%，极度乐观可 70%+ |
| 浸没冷却：LiquidStack、Submer、GRC、Iceotope 等 | 选择性部署 | $0.2-0.5B / $0.4-0.9B / $0.8-1.8B | $0.8-2B / $1.5-4B / $3-8B | $3-8B / $6-15B / $12-28B | 2026 低个位数；2027 仍偏专用场景 | 35-55%，受标准化和运维接受度影响 |
| 微流道/封装内冷却/喷射冷却 | 研发/小批验证 | <$0.2B | $0.3-1B / $0.6-2B / $1-4B | $1-4B / $3-8B / $6-18B | 2027 仍 <5%；2028 后决定性更高 | 50-75%，但良率/责任边界不清 |
| Chiller-less 高温水 + 直接干冷 | 有利气候放量 | $0.5-1.2B / $1-2B / $2-4B | $2-5B / $4-9B / $8-16B | $6-15B / $12-28B / $25-55B | 2026 10-20%；2027 15-35%；极度乐观 40%+ | 25-40%，系统设计溢价高于设备 |
| 吸收式冷机/燃气余热驱动冷却 | 概念到项目验证 | <$0.3B | $0.5-1.5B / $1-3B / $2-6B | $2-6B / $5-12B / $10-25B | 现场燃气/微电网项目中率先采用 | 25-45%，取决于能源合同 |
| AI cooling optimizer / workload-aware cooling | 早期商用 | $0.2-0.8B / $0.5-1.5B / $1-3B | $1.5-4B / $3-7B / $6-12B | $5-12B / $10-22B / $18-40B | 高密 AI 园区 2027 可达 30-60% | 60-85%，若与设备绑定 ROIC 高 |

## 4. 供给侧：产能、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区 | 代表公司/资产 | 产能特征 |
|---|---|---|---|
| 大型冷水机组与 HVAC 主机 | 美国、欧洲、中国、日本、印度 | Johnson Controls/YORK、Trane、Carrier、Daikin、Mitsubishi、Airedale/Modine、Munters/Geoclima、STULZ、AAON、Vertiv | 工厂测试、压缩机、换热器、低 GWP 制冷剂和大型项目交付能力决定产能 |
| CDU、冷板、快接头、液冷管路 | 北美、加拿大、欧洲、台湾、中国、东南亚 | CoolIT、Motivair/Schneider、Vertiv/CoolTera、nVent、Boyd、Danfoss、Parker/CPC、LiquidStack、ZutaCore、Accelsius | 精密加工、泄漏测试、泵阀冗余、芯片/服务器 OEM 认证决定产能 |
| 热交换器、干冷器、微通道 | 意大利、德国、美国、中国、印度 | ThermoKey/Vertiv、Danfoss、Kelvion、Modine、Munters、Lu-Ve、Baltimore Aircoil、SPX Cooling | 铜铝、不锈钢、翅片/微通道制造与低噪声风机是关键 |
| 机房风侧设备 | 美国、欧洲、中国、东南亚 | Vertiv Liebert、Schneider、JCI Silent-Aire、STULZ、Rittal、Airedale、AAON、Munters | 定制 AHU/CRAH、风墙和现场安装能力强，毛利受金属加工约束 |
| 控制/数字孪生/运维 | 全球软件和设备厂生态 | Schneider EcoStruxure、JCI OpenBlue、Carrier QuantumLeap、Trane/BrainBox AI、Vertiv Unify/Next Predict、NVIDIA Omniverse DSX | 数据接口、设备绑定、运维服务网络和大客户信任形成壁垒 |

### 4.2 供给瓶颈

1. **芯片/服务器级验证瓶颈**：冷板、manifold、快接头和 CDU 必须随 GPU/ASIC、主板、rack 共同验证，不能像普通 HVAC 标品一样临时替换。
2. **漏液与可靠性工序**：压力测试、氦检/水检、热循环、腐蚀测试、过滤洁净度、快接头寿命都会吃掉产能。
3. **大型冷水机组交期**：3MW+ 空冷/水冷机组、高 lift 机型、磁悬浮/变频压缩机和 VFD 供应链会成为 2026-2027 关键瓶颈。
4. **铜、铝、不锈钢、泵阀和风机**：热交换器、冷板、管路、busway 和电力设备同时抢铜铝，价格传导能力取决于合同条款。
5. **制冷剂与环保认证**：低 GWP 制冷剂、压力容器、UL/CE/CSA、ASHRAE、当地噪声/水耗许可会影响交付。
6. **现场机电安装和调试人才**：AI 园区不是只买设备，泵站、管路冲洗、过滤、平衡、BAS/DCIM 集成和冗余测试需要熟练团队。
7. **客户认证和 reference design 锁定**：NVIDIA DSX、OCP、hyperscaler AVL、服务器 OEM 认证决定供应商能否进入项目。
8. **热排放与水资源约束**：缺水地区不能只看 COP；WUE、热岛、噪声和可用土地会决定空冷/水冷/干冷组合。

### 4.3 BOM 和毛利决定因素

| 产品 | 粗略 BOM/单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| CDU | 泵/VFD 15-25%；换热器 15-25%；阀组/过滤/水箱 15-25%；传感器/控制 10-15%；管路/外壳/装配测试 20-30% | 冗余设计、压损、流量控制、软件、现场调试 | 大客户框架协议 + 原材料 escalator + 交期溢价 |
| 冷板/快接头 | 铜/基材 25-35%；加工/焊接/钎焊 20-30%；密封/连接 10-20%；测试良率 15-25%；工程验证 10%+ | 热阻、压降、泄漏率、芯片适配、良率 | 芯片平台认证后绑定，切换成本高 |
| 空冷/水冷冷水机组 | 压缩机/电机/VFD 25-35%；换热器/盘管 20-30%；风机/泵 10-15%；制冷剂/阀件/管路 10-15%；控制/框架/测试 15-25% | COP/IPLV、lift、低噪声、低水耗、极端天气可靠性 | 项目制报价，长交期设备可通过预付款和变更单传导 |
| CRAH/AHU/风墙/RDHx | 盘管/EC 风机 30-45%；钣金/框架 15-25%；阀件/控制 10-15%；过滤/加湿 5-10%；人工测试 15-20% | 定制化、风量/压损、与机房布局匹配 | 竞争较多，靠交期和客户认证改善价格 |
| 控制软件/服务 | 软件研发/云平台/传感器/现场服务 | 数据闭环、SLA、节能收益分成 | 订阅、服务合同、性能保证和设备绑定 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 子市场 | 集中度判断 | 主要玩家 |
|---|---|---|
| 大型冷水机组/HVAC 主机 | 头部集中，全球 Top 5 在高端数据中心 chiller 中约 55-70% | Trane、Carrier、Johnson Controls/YORK、Daikin、Mitsubishi、Modine/Airedale、Munters/Geoclima、STULZ、AAON |
| 液冷 CDU/冷板/快接头 | 正快速集中，Top 5 约 50-65%，M&A 正在重塑 | Vertiv、CoolIT/Ecolab、Schneider/Motivair、nVent、Boyd、LiquidStack/Trane、Danfoss、Parker/CPC |
| 热排放/干冷器/换热器 | 中等集中，项目和区域属性强 | ThermoKey/Vertiv、Danfoss、Kelvion、Modine、Munters、SPX Cooling、Baltimore Aircoil、Lu-Ve |
| 预制化 power/cooling 模块 | 头部工程能力差异大 | Vertiv、Schneider、Eaton、JCI、Trane、Carrier、nVent、Legrand、Rittal |
| 控制软件/数字孪生 | 设备巨头和 NVIDIA/工业软件生态共存 | Schneider EcoStruxure、JCI OpenBlue、Carrier QuantumLeap、Trane/BrainBox AI、Vertiv Unify、Siemens、NVIDIA Omniverse DSX、Phaidra |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| 技术可靠性 | 漏液率、热阻、压降、MTBF、极端环境测试小时数 | 一次漏液/热失控可能导致数千万美元级停机和 GPU 损失，客户不愿为小幅降价换风险 |
| 平台认证 | NVIDIA/AMD/OEM/hyperscaler AVL、OCP、UL/CE/CSA | 一旦进入 reference design，后续园区复制会沿用供应商 |
| 规模制造 | CDU/冷板月产能、chiller 工厂测试位、服务网点 | 大客户要的是按季度交付几百 MW 热链，只有少数公司能保证 |
| 项目交付 | 现场调试周期、预制化比例、commissioning 人员 | Time-to-power 价值高于单设备节省，交付快可溢价 |
| 客户锁定 | 管路接口、冷却液化学、控制软件、运维数据 | 换供应商涉及排液、冲洗、重新验证和 downtime，切换成本高 |
| 服务网络 | 24/7 运维 SLA、备件覆盖、远程监控 | 设备收入后可叠加高毛利服务，长期 ROIC 更稳定 |

### 5.3 长期价值捕获判断

长期最可能拥有高 ROIC/高毛利的是三层：

1. **冷板/快接头/CDU 核心液冷包**：直接绑定芯片平台，验证周期和泄漏责任形成强壁垒。
2. **设备 + 水化学 + 监控 + 运维的一体化服务**：Ecolab 买 CoolIT 的逻辑就在这里，把一次性硬件转成 fluid management 和 cooling-as-a-service。
3. **AI Factory reference design 和预制化系统集成**：Vertiv、Schneider、JCI、Trane、Carrier、Eaton 等从卖设备转向卖“可复制的热链/电链模块”，毛利未必最高，但资本周转和客户锁定更好。

相对弱的环节是低端钣金件、普通 AHU、通用风机盘管和非认证管路，价格竞争更明显。

## 6. 2026 关键变化

1. **液冷 M&A 和估值重定价成为行业拐点。**  
   Trane 2026-03 完成 LiquidStack 收购；Ecolab 2026-03 宣布以约 47.5 亿美元现金收购 CoolIT，CoolIT 未来 12 个月销售额约 5.5 亿美元；Legrand 投资 Accelsius；Carrier 追加 ZutaCore；Vertiv 收 ThermoKey 并扩 Ohio 产能。资本已经把液冷从“小众设备”定价为 AI 基建核心资产。

2. **冷水机组重新成为 AI Factory 关键设备，而不是被液冷替代。**  
   JCI 发布 1GW AI data center 参考设计，空冷方案称可回收/释放 50MW 给 AI Factory、年能耗改善 32%、每日节水 1200 万加仑以上；Modine 推 TurboChill 3+MW 并强调高温水不等于不需要 chillers；Carrier 推 AquaEdge 30CF；这些都说明设施侧 HVAC 仍是主战场。

3. **10MW 级标准模块出现，交付方式从项目工程转向产品化复制。**  
   Vertiv MegaMod HDX 支持最高 10MW、144 racks、50kW 到 >100kW/rack；Schneider/Motivair MCDU-70 单台 2.5MW、6 台可做 4+2 冗余服务 10MW 设计。2026 下半年，谁能把电力、冷却、控制、服务做成标准 pod，谁就拿走超额订单。

## 7. 2027 关键变化

1. **Rubin、MI400、TPU8、Trainium3/4 和更多 ASIC 把液冷 attach rate 推向 75-90%。**  
   2027 的问题不是“要不要液冷”，而是冷板压降、CDU 冗余、热排放和供电瞬态能否跟上 rack-scale 平台。

2. **高温水、干冷、低水耗设计从 ESG 叙事变成电力容量工具。**  
   水和电会一起约束 AI 园区。能把冷却功耗降低、把更多 MW 还给 IT load 的设计，会被客户当成“算力增容”而非节能小修小补。

3. **行业出清：只有能跨越芯片、rack、设施和服务的供应商留在头部。**  
   单点设备公司会被收购、绑定大厂或被挤出。冷板/CDU/快接头、3MW+ chiller、预制化模块、数字孪生运维会形成头部名单。

## 8. 公司清单：按细分领域尽量完整覆盖

### 8.1 冷水机组、HVAC、风侧与热排放

| 公司 | 细分优势 | 2026 观察点 |
|---|---|---|
| Johnson Controls / YORK / Silent-Aire | YORK YDAM 3.5MW、YK-HT 高 lift、1GW AI Factory reference designs、Silent-Aire 数据中心定制 | 1GW 水冷/空冷/吸收式/直液冷指南，空冷方案强调 50MW 返回 IT、32% 年能耗改善 |
| Trane Technologies / LiquidStack / Stellar Energy | Trane chiller + controls + LiquidStack D2C/immersion，端到端 thermal chain | Q1 2026 record backlog $10.7B；LiquidStack 完成收购 |
| Carrier / ZutaCore | AquaEdge 30CF、QuantumLeap、CDU、ZutaCore 水less 两相 D2C | Q1 2026 数据中心订单 >500%；追加 ZutaCore 投资 |
| Daikin | 全球 HVAC 和 chiller 产能，亚洲/美国数据中心项目 | 低 GWP、磁悬浮/变频、高效机组 |
| Modine / Airedale | TurboChill 3+MW、free cooling、AHU、CDU、智能控制 | Q3 FY2026 数据中心销售 +78%；未来两年数据中心销售年增 50-70% |
| Munters / Geoclima | DCT、蒸发/空气处理、Circlemiser chillers | Q4 2025 DCT 订单 +416%；2026 Q1 订单继续强 |
| Vertiv / Liebert / ThermoKey | 热链、电链、MegaMod、CoolChip、TrimCooler、干冷器 | Q4 2025 organic orders +252%、backlog $15B；Ohio 扩产液冷/冷水系统 |
| STULZ | 精密空调、液冷、全球数据中心渠道 | 高密 retrofit 和欧洲/亚洲项目 |
| AAON / BASX | 定制 AHU、数据中心空气侧和液冷支持 | 北美 hyperscaler 定制项目 |
| Rittal | IT rack、液冷、模块化数据中心 | 欧洲工业客户和机柜生态 |
| SPX Cooling / Baltimore Aircoil / EVAPCO | 冷却塔、闭式塔、蒸发/干冷设备 | WUE/噪声/热排放约束 |
| Kelvion / Lu-Ve / ThermoKey | 换热器、干冷器、微通道 | Vertiv 收 ThermoKey 验证热排放资产价值 |

### 8.2 直接液冷、CDU、冷板、快接头

| 公司 | 细分优势 | 状态 |
|---|---|---|
| CoolIT Systems / Ecolab | hyperscale D2C、CDU、cold plates；Ecolab 水化学/服务 | Ecolab 47.5 亿美元收购，CoolIT NTM sales 约 5.5 亿美元 |
| Motivair / Schneider Electric | CDU 105kW-2.5MW，MCDU-70 可 10MW+ 级联，EcoStruxure 控制 | 2026-01 发布 MCDU-70，全球可订 |
| Vertiv / CoolTera / STL | CoolChip CDU、rack CDU、fluid network、MegaMod HDX | 通过收购和扩产补齐全链条 |
| nVent | 机柜、配电、液冷和连接件 | Dell'Oro 点名为重要液冷份额玩家 |
| Boyd | 冷板、热界面、液冷组件 | GPU/服务器 OEM 供应链优势 |
| Danfoss | 泵阀、换热、制冷控制、快接和热管理 | 设施侧与液冷侧均受益 |
| Parker / CPC | 快速接头、流体连接、密封 | 泄漏和维护决定客户粘性 |
| LiquidStack / Trane | D2C 与浸没冷却 | 被 Trane 收购后有全球 chiller/服务渠道 |
| ZutaCore / Carrier | 水less 两相 D2C HyperCool | Carrier 2026 追加投资，偏高热流密度场景 |
| Accelsius / Legrand | 两相 D2C NeuCool | Legrand 2026 战略投资 |
| JetCool | 微对流/微流道芯片级冷却 | 高热流密度早期 |
| Submer / GRC / Iceotope | 浸没冷却/精密液冷 | 专用场景和边缘/高密 retrofit |
| Asetek | 服务器/高性能液冷历史经验 | 需观察能否重新切入 hyperscale AI |
| Delta Electronics | 电源、风扇、热管理、CDU/数据中心方案 | 台系 ODM/电源生态协同强 |
| AVC / Asia Vital Components、Nidec、ebm-papst、Ziehl-Abegg | 风扇、散热模组、EC fan | 风侧和热排放设备的关键部件 |
| Xylem、Grundfos、Wilo、Armstrong Fluid Technology | 泵、流体控制 | 大型二次侧冷却环路和 CDU 泵系统受益 |
| Alfa Laval、SWEP、Kelvion、Danfoss | 板式换热器、热交换 | CDU、冷水机组和干冷器核心部件 |
| Chemours、Honeywell、Solvay/Syensqo、Castrol、Shell | 制冷剂、介电液/冷却液 | 低 GWP 和两相/浸没路线的材料变量 |

### 8.2.1 中国及亚洲供应商补充

| 公司 | 细分优势 | 观察点 |
|---|---|---|
| 英维克 | 数据中心温控、液冷 CDU、机房空调 | 国内 AI 机房和通信机房客户基础强 |
| 申菱环境 | 数据中心空调、间接蒸发冷却、液冷相关 | 国内大型数据中心和运营商项目 |
| 高澜股份 | 电力电子/服务器液冷、冷板和冷却系统 | 国内 GPU/服务器液冷订单弹性 |
| 同飞股份 | 工业温控、液冷设备 | 从工业温控向数据中心液冷延伸 |
| 依米康、佳力图、科华数据、科士达 | 精密空调、UPS、数据中心基础设施 | 国内数据中心建设链条受益 |
| 台达电子 | 电源、风扇、热管理、数据中心系统 | 与服务器 ODM 和电源架构协同 |
| 富士康、广达、纬颖、英业达、纬创、神达 | AI server/rack 集成与液冷整柜制造 | 不是纯冷却公司，但决定液冷 BOM attach 和整柜交付 |
| 比亚迪电子、立讯精密、工业富联等 | 机柜/连接/服务器结构件与制造 | 若进入液冷 manifold、快接和整柜集成，弹性较大 |

### 8.3 控制软件、数字孪生和运维

| 公司 | 方向 | 投资含义 |
|---|---|---|
| NVIDIA Omniverse DSX | AI Factory reference design/digital twin | 把电力、冷却、网络、施工和运维放进同一仿真环境 |
| Schneider EcoStruxure | 电力+冷却+楼控一体化 | Motivair CDU 和电力设备形成全栈控制 |
| Johnson Controls OpenBlue | HVAC/BAS/服务 | 大型 chiller plant 优化与服务化 |
| Carrier QuantumLeap | data center thermal lifecycle + IDCM | chiller、CDU、BAS、服务、预测维护集成 |
| Trane / BrainBox AI | AI HVAC optimization | 商用 HVAC 优化经验向数据中心迁移 |
| Vertiv Unify / Next Predict | power/cooling 监控、预测维护 | 与 MegaMod、UPS、CDU 绑定 |
| Siemens / Cadence / Dassault / PTC / Phaidra | 工业数字孪生、控制优化 | DSX 生态和 AI cooling optimizer 受益 |

## 9. 信息源与关键事实

| 来源 | 关键事实 |
|---|---|
| [Johnson Controls air-cooled AI Factory guide, 2026-05-05](https://www.johnsoncontrols.com/media-center/news/press-releases/2026/05/05/johnson-controls-releases-second-data-center-reference-design-guide-to-advance-industrialscale-ai-fa) | 支持最高 1GW AI factory；220MW compute cluster sizing；空冷方案可“return up to 50MW”、年能耗改善 32%、每日节水 1200 万加仑以上 |
| [Johnson Controls 1GW reference design, 2026-02-02](https://investors.johnsoncontrols.com/news/news-details/2026/Johnson-Controls-launches-series-of-thermal-management-reference-design-guides-for-gigawatt-scale-AI-data-centers/default.aspx) | 水冷/空冷/吸收式 chiller guides，整合 CRAH、FCW、CDU、YORK centrifugal chillers，支持 NVIDIA DSX |
| [Johnson Controls YK-HT, 2026-02-02](https://investors.johnsoncontrols.com/news/news-details/2026/Johnson-Controls-previews-YORK-YK-HT-two-stage-economized-centrifugal-chiller-at-AHR-Expo-delivering-energy-water-and-space-savings/default.aspx) | 165F condenser leaving fluid、110F lift；可减少干冷器 60%、噪声降低最高 20dBA |
| [Vertiv MegaMod HDX, 2026-01-14](https://investors.vertiv.com/news/news-details/2026/Vertiv-Introduces-New-Modular-Liquid-Cooling-Infrastructure-Solution-to-Support-High-Density-Compute-Requirements-in-North-America-and-EMEA/default.aspx) | 最高 10MW、144 racks、50kW 到 >100kW/rack，集成 D2C 液冷与 air cooling |
| [Vertiv Q4 2025 results, 2026-02-11](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/default.aspx) | Q4 organic orders +252%、book-to-bill 约 2.9x、backlog $15.0B、2026 organic sales growth guide 27-29% |
| [Vertiv Ohio expansion, 2026-03-30](https://investors.vertiv.com/news/news-details/2026/Vertiv-to-Expand-Ohio-Manufacturing-to-Boost-U-S--Production-of-Critical-Thermal-Management-Technologies-for-AI-Data-Centers/default.aspx) | 投资约 $50M，Ironton 液冷和 chilled water systems 产能预计 +45%，2027 Q2 投产 |
| [Vertiv ThermoKey acquisition, 2026-03-23](https://investors.vertiv.com/news/news-details/2026/Vertiv-to-Acquire-ThermoKey-Expanding-Heat-Rejection-Portfolio-for-Converged-Physical-Infrastructure/default.aspx) | 收购干冷器、换热、微通道能力，补强 AI 数据中心热排放 |
| [Schneider/Motivair MCDU-70, 2026-01-21](https://www.se.com/us/en/about-us/newsroom/news/press-releases/Motivair-by-Schneider-Electric-announces-new-CDU-with-capability-to-scale-to-10MW-and-beyond-for-nextgen-AI-Factories-69705c3655f8517e99086bbd/) | 单台 CDU 2.5MW；CDU 组合可 10MW+；105kW-2.5MW 产品范围；1.5 LPM/kW 目标 |
| [Schneider Q1 2026 revenues](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026) | Data Center & Networks demand/sales 双位数增长；北美增长由 data center 和 liquid cooling 推动 |
| [Trane completes LiquidStack acquisition, 2026-03-03](https://investors.tranetechnologies.com/news-and-events/news-releases/news-release-details/2026/Trane-Technologies-Completes-Acquisition-of-LiquidStack/default.aspx) | Trane 从 central plant 到 chip 补齐 D2C/immersion 液冷 |
| [Trane Q1 2026 results](https://s2.q4cdn.com/950394465/files/doc_financials/2026/q1/Q1-2026-Earnings-Release-Final.pdf) | Organic bookings +24%；record backlog $10.7B；Americas Commercial HVAC bookings 约 +40%，applied equipment bookings >160% |
| [Carrier AquaEdge 30CF, 2026-02-26](https://www.carrier.com/commercial/en/us/news/news-article/carrier-introduces-aquaedge--30cf-chiller-to-enhance-data-center-reliability-and-uptime.html) | 数据中心空冷离心 chiller，强调 AI/cloud/HPC 下 real-world uptime |
| [Carrier CDU Europe, 2026](https://www.carrier.com/commercial/en/eu/news/news-article/carrier-expands-data-centre-cooling-portfolio-with-new-coolant-distribution-unit.html) | CDU 模块化换热器 approach temperature 可低至 2C，帮助最高 15% chiller energy savings |
| [Carrier expands ZutaCore investment, 2026-04-29](https://www.carrier.com/us/en/news/carrierventures-expands-investment-in-zutacore-to-scale-liquid-cooling-for-ai-data-centers/) | 追加 direct-to-chip waterless liquid cooling 投资，覆盖单相和两相能力 |
| [Carrier Q1 2026 webcast](https://s205.q4cdn.com/164393362/files/doc_financials/2026/q1/Carrier-Q1-2026-Earnings-Release-Webcast.pdf) | Commercial HVAC data center orders growth >500%；2026+ 可投标市场估计 >$10B |
| [Modine/Airedale TurboChill 3+MW, 2026-01-22](https://www.prnewswire.com/news-releases/airedale-by-modine-unveils-turbochill-3mw-redefining-air-cooled-efficiency-for-ai-data-centers-302666923.html) | 3+MW hybrid chiller；free cooling + mechanical cooling 兜底；反驳“高温水=不需要 chiller” |
| [Modine Q3 FY2026 results](https://s205.q4cdn.com/270741342/files/doc_financials/2026/q3/Modine-Reports-Third-Quarter-Fiscal-2026-Results.pdf) | 数据中心销售 +78%；Climate Solutions +51%；未来两年数据中心销售年增 50-70% |
| [Munters Q1 2026 release](https://www.munters.com/en-us/news-media/press-releases/2026/good-momentum-across-all-business-areas/) | DCT 需求强；2026 年 4 月获得约 SEK 2.0B 模块化 AI cooling solution 订单 |
| [Munters Q4 2025 release](https://www.munters.com/en-us/news-media/press-releases/2026/exceptional-demand-while-earnings-weakened/) | Q4 order intake +191%，DCT order intake +416%，进入 2026 backlog 强 |
| [Ecolab acquires CoolIT, 2026-03-20](https://www.ecolab.com/news/2026/03/ecolab-to-acquire-coolit-systems-a-global-leader-in-advanced-liquid-cooling-for-next-gen-ai-data-ce) | 约 $4.75B cash；CoolIT 未来 12 个月 sales 约 $550M；估值 29x NTM EBITDA/24x 2027 EBITDA |
| [Dell'Oro liquid cooling forecast, 2026-01-08](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html) | 液冷制造商收入 2025 接近 $3B、2029 约 $7B；单相 D2C 仍主导；Vertiv 领先，CoolIT、nVent、Boyd 份额强 |
| [Uptime Institute, 2026-04-15](https://journal.uptimeinstitute.com/liquid-cooling-will-not-outgrow-its-high-density-niche/) | 液冷主要由高 rack density 和高 heat flux 驱动，短期不会覆盖所有低密度 IT |
| [Legrand/Kratos/Accelsius, 2026-02-12](https://www.legrand.us/about-us/newsroom/press/legrand-acquires-kratos-industries) | 收购电力设备 Kratos，并投资两相 D2C 液冷 Accelsius，验证“电力+冷却”一体化 |
| [NVIDIA Vera Rubin DSX, 2026-03-16](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-Vera-Rubin-DSX-AI-Factory-Reference-Design-and-Omniverse-DSX-Digital-Twin-Blueprint-With-Broad-Industry-Support/default.aspx) | Eaton、Schneider、Siemens、Trane、Vertiv 等提供电力/冷却 SimReady assets，DSX 把 AI factory 设计数字孪生化 |

## 10. 投资结论

**基准情景**下，2026 年 AI 数据中心冷却/HVAC 全球订单池约 $35-65B，2027 年约 $55-95B；其中直接液冷硬件仍低于整体 HVAC，但增长最快。**乐观情景**下，2026 年 $50-85B、2027 年 $80-135B。**极度超预期乐观情景**下，如果 hyperscaler 把 2027 需求前置、GB300/Rubin/ASIC 与电力同步交付，2026 年可见订单池可能冲到 $75-125B，2027 年 $130-220B。

最值得跟踪的高频信号：

1. Vertiv、Schneider、Trane、Carrier、JCI、Modine、Munters 的 backlog、book-to-bill 和数据中心订单增速。
2. GB300/Rubin/MI400/Trainium3/TPU8 的实际 rack 功率和液冷 BOM attach rate。
3. CDU、冷板、快接头、泵阀的交期和价格是否从季度变成半年以上。
4. 大型 chiller/dry cooler 的交期、低 GWP 制冷剂供应、噪声/水耗许可。
5. NVIDIA DSX/OCP/hyperscaler reference design 中被列入的设备供应商。

一句话：2026 年最确定的技术路径是“单相直接液冷 + 风液混合 + 高密冷水机组/干冷器 + 预制化热链模块”。液冷最有弹性，冷水机组最有确定性，控制/服务最可能长期高毛利。
# 行业调研：【数据中心开关设备与变压器】

版本日期：2026-05-08  
研究对象：AI 数据中心和 AI Factory 使用的高压/中压/低压开关设备、变压器、母线槽、预制电力模块、数字保护与监控，以及正在导入的 800VDC/MVDC/固态变压器等新技术。  
口径说明：本文的“市场规模”优先采用“新增订单/项目锁单”口径，而不是会计收入，因为变压器、开关柜和预制电力模块的订单常常领先收入 6-36 个月。美元为名义美元。情景分为基准、乐观、极度超预期乐观；所有乐观假设均建立在 AI 计算中心建设继续强扩张的前提下。

## 0. 一页结论

数据中心开关设备与变压器已经从“土建机电子项”变成 AI 基础设施建设最硬的瓶颈之一。2026 年最确定的投资机会不是某一种单点新技术，而是传统 AC 配电体系的超高强度扩产：大型园区先锁 230/138/69kV 接入、主变、34.5/13.8kV 中压开关柜、480/415V 低压开关柜、母线槽和预制电力模块；新技术的主线是 SF6-free、数字化、预制化、800VDC 试点、BESS/现场发电接入，而不是 2026 年直接大规模替代传统交流架构。

最重要的数字锚点：

| 类别 | 2026 最新事实 | 对行业的含义 |
|---|---|---|
| 数据中心建设 | JLL 2026 Outlook 预计全球数据中心容量从 2025 年约 103GW 增至 2030 年约 200GW，2026-2030 新增 100GW 需要最高约 $3T 投资；全球数据中心设备平均交期 33 周，美国平均 42 周，较 2019 年高 83%；2025 年 57% 项目延误 3 个月以上。 | 电气长交期设备先于 GPU/服务器锁单，订单能见度上升。 |
| 电力瓶颈 | IEA 称到 2030 数据中心贡献全球新增电力需求约 10%，约 20% 已规划数据中心项目可能因电网延迟受风险，先进经济体新输电线可需 4-8 年，变压器和电缆等待时间三年内翻倍。 | “可交付电力”成为选址和租约的核心稀缺资产。 |
| Eaton | 2026 Q1 Electrical Americas 数据中心订单同比约 +240%，该部门 backlog 同比 +44%，Electrical Americas Q1 销售 $3.6B、利润率 25.6%；Eaton 还推出与 NVIDIA Vera Rubin DSX 相关的 Beam Rubin DSX grid-to-chip 平台。 | 北美数据中心电气设备进入超常规订单周期，且利润率仍高。 |
| Schneider Electric | 2026 Q1 收入 €9.767B、organic +11.2%；Energy Management +12.8%，由数据中心驱动；北美 +14.4%，系统业务 +16%。 | Schneider 的“端到端电力+液冷+软件”组合正在提高 attach rate。 |
| ABB | 2026 Q1 Electrification 订单 $6.647B、收入 $4.613B、book-to-bill 1.44；数据中心订单在报道口径下达到三位数增长。 | ABB 在中低压开关、电气包、UPS、配电系统上的景气度已落到订单。 |
| Vertiv | 2026 Q1 销售 $2.65B、同比 +30%，有机增长 +22.6%；全年 2026 销售指引 $13.5-14.0B，调整后经营利润率 22.8-23.8%。 | 数据中心电力/冷却/模块化系统供应商正在从订单高峰转收入。 |
| GE Vernova | 2026 Q1 订单 $18.3B、organic +71%；backlog 环比 +$13B；Electrification 当季数据中心设备订单 $2.4B，超过 2025 全年；完成 Prolec GE 剩余 50% 股权收购。 | 大型变压器、开关、并网、电气化设备的景气被数据中心与电网共同推高。 |
| Siemens Energy | 2026 Q1 backlog €146B；Grid Technologies Q1 订单 +21.8%，美国数据中心相关订单达高三位数百万欧元；4 月上调 2026 Grid Technologies 指引至收入 +25-27%、利润率 18-20%。 | 电网级变压器、GIS、HV substations 与数据中心接入正在同一产能池中争抢产能。 |
| 供给瓶颈 | DOE 指出配电变压器交期从 2019 年 3-6 个月上升到 2023 年 12-30 个月，瓶颈包括 GOES、铜铝、组件与劳动力；Wood Mackenzie 称 2025 年美国 power transformer 和 distribution transformer 分别有约 30% 和 10% 供给缺口。 | 价格传导和订单排队会延续到 2027，扩产并不能立刻释放。 |

本文对“数据中心开关设备与变压器”订单池的核心预测：

| 口径：全球 AI 数据中心直接相关新增订单 | 未来 3 个月 | 未来 12 个月 | 未来 24 个月 |
|---|---:|---:|---:|
| 基准 | $10-16B | $45-70B | $105-160B |
| 乐观 | $16-24B | $70-105B | $170-255B |
| 极度超预期乐观 | $24-36B | $105-155B | $260-390B |

这里包含变压器、中低压开关柜、母线槽、预制电力模块、电气保护/监控与数据中心专用配电集成，不包含 GPU/服务器、UPS 电池本体、燃气轮机、冷却设备和一般土建。若只看“变压器+开关柜”两个最窄环节，规模大致为上表的 60-70%；若把 busway、PDU、E-house、并网开关站完整计入，接近上表上沿。

## 1. AI 计算中心 2026-2027 对本行业的机会、挑战与技术路径

### 1.1 机会：AI rack 功率密度把电气价值量推上新台阶

项目中既有 AI 芯片研究显示，2026 出货价值和功率压力最大的计算平台主要是 NVIDIA B300/GB300、B200/GB200、Vera Rubin 早期、AWS Trainium2/Trainium3、Google TPU v7 Ironwood、AMD MI350/MI400、Meta MTIA、Microsoft Maia 200、Huawei Ascend、Cambricon 等。它们的共同点不是“都用同一种芯片”，而是都把电气系统推向同一个方向：更高机架功率、更短部署周期、更强瞬态功率波动、更高可用性要求。

| 芯片/平台路径 | 对开关设备和变压器的含义 | 2026 最可能落地的电气方案 |
|---|---|---|
| NVIDIA GB300/B300/GB200，NVL72 rack | 100kW+ 级别机架成为主流大型 AI 集群设计假设，液冷与高密母线槽同步成为标配。 | 传统 AC 架构为主：utility feed -> HV/MV 变电站 -> 34.5/13.8kV MV switchgear -> 480/415V transformer/LV switchgear -> busway/PDU/rack power。 |
| NVIDIA Vera Rubin / Rubin POD | NVIDIA 在 2026 GTC 公开 40 racks、1,152 Rubin GPUs、60 exaflops、10PB/s 带宽的 POD 级设计，并强调 dynamic power steering、rack-level energy storage、45C liquid cooling；800VDC 架构进入生态。 | 2026 下半年开始高端客户试点 800VDC 与预制 power block；大规模收入仍落在 AC 开关柜、变压器、母线槽、冷却/电力一体模块。 |
| AWS Trainium2/3、Google TPU Ironwood、Microsoft Maia 200、Meta MTIA | 自研 ASIC 降低单位 token 成本，但总功率需求不降，反而把 hyperscaler 自建园区和长期电力锁单做大。 | 云厂商自定义电气包增多，AVL 供应商提前参与设计；开关柜和变压器更偏工程化、模块化、标准化。 |
| AMD MI350/MI400、Huawei Ascend、国产 GPU/ASIC | 非 NVIDIA 路线增加电气系统多样性，主权 AI 与中国/中东项目更重视本地供应和可替代供应商。 | 本地化 MV/LV switchgear、dry-type/cast resin transformer、油浸式主变与预制变电站加速。 |

### 1.2 挑战：行业增长受“物理供给”约束

数据中心电气设备的挑战不是需求，而是能不能按期交付：

| 挑战 | 具体表现 | 投资含义 |
|---|---|---|
| 交期长 | JLL 统计全球数据中心设备平均交期 33 周，美国 42 周；transformer、generator、switchgear、UPS 都处在长交期清单。Bloomberg/Sightline 经 Tom's Hardware 转述称高功率变压器等待期可从疫情前 24-30 个月拉长到最高 5 年。 | 客户愿意预付、锁产能、接受价格升级；但收入确认滞后，供应商 working capital 压力上升。 |
| 定制化 | 230kV/138kV 主变、34.5kV 金属铠装开关柜、保护逻辑、短路容量、谐波/接地方案往往按项目定制。 | 规模扩张不等于完全自动化；设计、测试和项目管理能力成为壁垒。 |
| 材料 | GOES/CRGO、铜、铝、绝缘纸、油/天然酯、真空灭弧室、套管、断路器机构均可能成为瓶颈。 | 成本传导能力决定毛利；有价格调整条款的订单优于固定价订单。 |
| 认证与客户 AVL | Hyperscaler 对短路测试、温升、arc-flash、UL/ANSI/IEC/IEEE、现场运维、网络安全都有严格要求。 | 新进入者难以快速切入核心电气包，只能从低压盘柜、配件或二线市场开始。 |
| 并网与法规 | 变压器/开关柜交付不等于可上电，公用事业并网审批、输电扩容、环保许可、噪声和消防都可能拖慢项目。 | 具备“设备+工程+并网+现场能源”组合的供应链更有定价权。 |

### 1.3 三情景下新技术成熟与放量时间

| 技术路径 | 2026 状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期成熟/放量 | 备注 |
|---|---|---|---|---|---|
| 传统 AC 架构升级：34.5/13.8kV MV + 480/415V LV + busway | 已大规模使用 | 2026-2027 继续占新增 AI MW 的 85-95% | 2026-2027 占 75-90% | 2027 仍占 55-75% | 这是 2026 最确定主线。 |
| 预制电力模块/E-house/Power Skid | 已放量 | 2026 attach rate 25-40%，2027 35-55% | 2026 35-55%，2027 50-70% | 2026H2 起大型 AI 园区 70%+ 采用 | 缩短工期，降低现场电工瓶颈。 |
| SF6-free 中压/高压开关设备 | MV 已商业化，HV GIS 逐步成熟 | 2026 新项目渗透 5-12%，2027 10-20% | 2026 10-18%，2027 20-35% | 2027 欧盟/高 ESG 客户 40%+ | 受法规、客户 ESG、价格溢价和型号覆盖影响。 |
| 数字开关柜/智能变压器监测 | 已放量 | 2026 大型项目 35-55%，2027 50-70% | 2026 50-70%，2027 70-85% | 2027 几乎成为 hyperscale 标配 | 传感器、保护继电器、局放/油色谱/热模型、SCADA/DCIM 接口。 |
| 800VDC 数据中心配电 | NVIDIA 2026 公开生态，处试点阶段 | 2026 <2%，2027 5-10%，2028 10-20% 新增高密 AI MW | 2026 2-5%，2027 10-20%，2028 20-35% | 2026H2 5-8%，2027 25-40%，2028 40%+ | 减少转换级数、铜耗和线缆体积，但需要 DC 开关、保护、标准和运维成熟。 |
| MVDC/固态变压器/SST | 示范和小批量 | 2027 前低于 2%，2028-2029 才有项目化 | 2027 3-6%，2028 8-15% | 2027 起在现场能源+BESS+AI campus 中快速试点 | 技术壁垒高，但故障保护、效率、成本、可靠性还需证明。 |
| BESS/微电网集成开关站 | 已放量但非所有项目 | 2026 attach 15-30%，2027 25-45% | 2026 25-45%，2027 45-65% | 2027 70%+ 大型园区有 BESS/现场电源接口 | 用于削峰、备用、需求响应、缩短并网等待。 |

### 1.4 2026 最可能的技术路径

2026 年最可能的商业赢家是“传统架构高端化+预制化+数字化”，而不是全新 DC 架构直接替代：

1. 230/138/69kV utility interconnect + 34.5kV campus distribution。
2. 大容量油浸式主变/中压配电变压器 + 数据中心白空间 dry-type/cast resin transformer。
3. 金属铠装 MV switchgear、vacuum breaker、arc-resistant switchgear、数字继电保护。
4. 低压 switchgear/switchboards、busway、RPP/PDU、高密度母线槽。
5. 预制变电站、E-house、电力 skid，把现场施工从“土建项目”改成“制造+总装+调试”。
6. BESS/柴油/燃气/燃料电池/微电网接入开关站。
7. 高端客户的 800VDC 试点，尤其围绕 NVIDIA Vera Rubin/800VDC 生态。

## 2. 已经开始放量的关键产品：市场规模、渗透率、利润率

### 2.1 已放量产品清单

| 产品/细分技术 | 当前状态 | 主要需求驱动 | 代表供应商 |
|---|---|---|---|
| 大型电力变压器/主变，69-345kV，100MVA+ | 供不应求，交期最长 | AI campus 接入、输电扩容、现场电源升压/降压 | Hitachi Energy、GE Vernova/Prolec GE、Siemens Energy、HD Hyundai Electric、Hyosung、Mitsubishi、Virginia Transformer、SPX Waukesha、WEG、SGB-SMIT、TBEA、中国西电 |
| 中压/配电变压器，34.5/13.8kV 到 480/415V | 大规模放量 | 每个园区的 campus distribution、模块化 power block | Eaton、Schneider、ABB、Hitachi Energy、Prolec GE、Howard、Virginia Transformer、Delta Star、Hammond、SGB-SMIT、CG Power、LS Electric |
| 干式/浇注树脂变压器 | 数据中心内快速增长 | 白空间/楼内安全、防火、低维护、液冷机房改造 | Schneider、Eaton、Hitachi Energy、Siemens、SGB-SMIT、TMC、Hammond、Legrand、CG Power、JST、MGM |
| MV metal-clad / metal-enclosed switchgear | 极强订单周期 | 34.5/13.8kV 配电、变电站、发电机/BESS 并网 | Eaton、Schneider、ABB、Siemens、Powell、GE Vernova、Mitsubishi、LS Electric、Hyosung、S&C、G&W、Ormazabal、Lucy Electric |
| LV switchgear/switchboard/panelboard | 已放量 | 480/415V 低压分配、冷却/泵/白空间配电 | Schneider/Square D、Eaton、Siemens、ABB、Vertiv/E+I、Powell、Legrand、nVent/Avail、Mitsubishi、Fuji |
| Busway / busduct / RPP / PDU | 已放量且高密度化 | 机架功率 50kW -> 100kW+，需要可扩展母线 | Legrand Starline、Eaton、Schneider、Siemens、ABB、Vertiv/E+I、nVent/ERIFLEX/Avail、LS Electric、EAE Electric、Anord Mardix |
| 预制电力模块/E-house/模块化变电站 | 快速放量 | 缩短交付、减少现场劳动力、复制 AI campus | Vertiv、Eaton/Fibrebond、Schneider、ABB、Siemens、nVent Trachte/Avail、Powell、GE Vernova、AZZ |
| 数字继电保护/监测/电能质量 | 放量 | 高可用性、远程运维、负载瞬态、谐波治理 | Schneider、Eaton、ABB、Siemens、SEL、GE Vernova、Hitachi Energy、Schweitzer Engineering、S&C、Omicron |

### 2.2 已放量产品的订单规模与渗透率

口径：2026-05 起算的全球 AI 数据中心直接相关新增订单窗口。渗透率指在新增 AI 数据中心电气包中的使用比例或 attach rate；传统必配产品渗透率接近 100%，表中重点看高价值型号/高密度形态/预制形态。

| 已放量产品 | 情景 | 未来 3 个月订单 | 未来 12 个月订单 | 未来 24 个月订单 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 大型电力变压器/主变 | 基准 | $2.0-3.5B | $9-14B | $22-34B | 大型 AI campus 接入 70-85% 需要新增或专用主变；交期限制收入。 |
|  | 乐观 | $3.5-5.5B | $14-22B | $35-55B | 现场发电/新增输电并行推进，主变锁单前置。 |
|  | 极度超预期 | $5.5-8.5B | $22-34B | $55-85B | 2027 之前客户用预付款抢 slot，价格上行。 |
| 中压/配电变压器 | 基准 | $1.5-2.5B | $7-11B | $17-27B | 新建 AI MW 几乎 100% attach，高容量/低损耗型号占比上升。 |
|  | 乐观 | $2.5-4.0B | $11-17B | $27-42B | 预制 power block 带动标准化中压变压器批量采购。 |
|  | 极度超预期 | $4.0-6.5B | $17-27B | $42-65B | 大客户提前锁 2028 产能。 |
| 干式/浇注树脂变压器 | 基准 | $0.6-1.0B | $2.5-4.0B | $6-10B | 白空间/楼内改造 attach 20-35%。 |
|  | 乐观 | $1.0-1.6B | $4-6.5B | $10-16B | 液冷改造、企业 AI 私有云机房增加。 |
|  | 极度超预期 | $1.6-2.5B | $6.5-10B | $16-25B | 高安全/低维护需求推动更多油浸替代。 |
| MV switchgear | 基准 | $2.2-3.5B | $10-16B | $24-38B | 新增 AI campus 基本 100% attach；arc-resistant/digital 占 35-55%。 |
|  | 乐观 | $3.5-5.5B | $16-24B | $38-58B | 并网/BESS/现场发电开关站增加。 |
|  | 极度超预期 | $5.5-8.0B | $24-36B | $58-90B | 订单从 2027 前置，Powell/Eaton/Siemens 等受益。 |
| LV switchgear/switchboards | 基准 | $1.8-2.8B | $8-13B | $20-32B | 480/415V 仍为 2026 主流；高短路容量/高密封装占比上升。 |
|  | 乐观 | $2.8-4.5B | $13-20B | $32-50B | 100kW+ rack 改造拉动白空间配电。 |
|  | 极度超预期 | $4.5-7.0B | $20-30B | $50-75B | 大客户采用多区域重复设计，批量采购。 |
| Busway/PDU/RPP | 基准 | $1.2-2.0B | $6-10B | $15-24B | 高密 AI 白空间 attach 55-75%。 |
|  | 乐观 | $2.0-3.2B | $10-16B | $24-38B | 母线替代线缆成为 100kW rack 默认方案。 |
|  | 极度超预期 | $3.2-5.0B | $16-24B | $38-60B | 机架级交付带动整包 busway。 |
| 预制电力模块/E-house | 基准 | $1.0-1.8B | $5-9B | $13-22B | 2026 attach 25-40%，2027 35-55%。 |
|  | 乐观 | $1.8-3.0B | $9-15B | $22-36B | 大型园区复制，缩短工期。 |
|  | 极度超预期 | $3.0-4.8B | $15-24B | $36-58B | “AI Factory power block”成为主流采购方式。 |
| 数字保护/监控/电能质量 | 基准 | $0.7-1.2B | $3-5B | $8-13B | 大型项目 attach 35-55%。 |
|  | 乐观 | $1.2-2.0B | $5-8B | $13-21B | predictive maintenance 与 DCIM/SCADA 深度集成。 |
|  | 极度超预期 | $2.0-3.0B | $8-12B | $21-32B | 负载调度和电网互动要求提高。 |

### 2.3 已放量产品的利润率预测

口径：产品层面毛利率/项目毛利率区间，不等于公司合并毛利率。供不应求产品可能有 slot premium、工程变更收益和原材料传导；固定价老订单可能拉低毛利。

| 产品 | 当前利润率判断 | 基准：未来 12 个月 | 乐观：未来 12 个月 | 极度超预期乐观：未来 12 个月 | 关键决定因素 |
|---|---:|---:|---:|---:|---|
| 大型电力变压器/主变 | 毛利 20-32%，优质急单更高 | 22-32% | 26-36% | 30-42% | 测试能力、GOES/铜传导、交期溢价、质保风险。 |
| 中压/配电变压器 | 18-30% | 20-30% | 24-34% | 28-38% | 标准化程度、产线自动化、材料传导。 |
| 干式/浇注树脂变压器 | 20-35% | 22-34% | 26-38% | 30-42% | 安全/环保溢价、楼内认证、低维护价值。 |
| MV switchgear | 25-38% | 26-38% | 30-42% | 34-46% | 客户 AVL、断路器供应、arc-resistant/digital 溢价。 |
| LV switchgear/switchboard | 22-35% | 23-35% | 27-39% | 30-43% | 设计重复性、铜价传导、交付窗口。 |
| Busway/PDU/RPP | 25-40% | 26-39% | 30-44% | 34-48% | 高密度母线槽、快速安装、客户标准化。 |
| 预制电力模块/E-house | 18-30% | 20-32% | 24-36% | 28-40% | 工程管理、现场风险转移、规模化生产。 |
| 数字保护/监控/软件服务 | 35-60% | 38-60% | 45-65% | 50-70% | 软件/服务 mix、装机基数、网络安全认证。 |

## 3. 在研或早期放量关键产品：市场规模、渗透率、利润率

### 3.1 关键在研/早期产品

| 技术 | 为什么重要 | 2026 阶段 | 主要公司/生态 |
|---|---|---|---|
| 800VDC 数据中心配电 | NVIDIA 称 800VDC 可减少转换级数、电流、铜耗和线缆体积，并让未来 AI server 支持更高功率。 | 生态发布与试点，尚非大规模标准。 | NVIDIA、ABB、Eaton、GE Vernova、Hitachi Energy、Schneider、Siemens、Vertiv、Delta、Flex、Lite-On、Megmeet、Infineon、TI、ADI、MPS、Navitas、EPC、ROHM、Renesas、Onsemi、ST。 |
| DC switchgear / DC breaker / e-fuse | DC 架构必须解决直流故障切断、选择性保护、arc flash 和接地。 | 试点和产品化早期。 | ABB、Schneider、Eaton、Siemens、Hitachi Energy、GE Vernova、Mitsubishi、Infineon、onsemi、TI、MPS、EPC、Navitas。 |
| MVDC campus distribution | 直接把 BESS、光伏、燃料电池、整流与 AI rack 接入中压 DC，可减少转换。 | 示范和方案阶段。 | ABB、Siemens、Schneider、GE Vernova、Hitachi Energy、Eaton、Mitsubishi、Heron Power。 |
| 固态变压器/SST | 用 SiC/GaN 电力电子实现电压变换、功率质量、隔离和双向能量流。 | 2026 仍早期，适合特殊场景试点。 | Eaton/Ultra PCS、Schneider、Siemens、ABB、GE Vernova、Hitachi Energy、Delta、Huawei Digital Power、Mitsubishi、Heron Power。 |
| SF6-free HV GIS / MV switchgear | 降低温室气体和监管风险；欧洲/高 ESG 客户优先。 | MV 商业化，HV GIS 扩展型号。 | Schneider AirSeT、ABB EconiQ/NeoGear、Siemens blue GIS、Hitachi Energy EconiQ、GE Vernova g3、Eaton Xiria、Mitsubishi、Toshiba。 |
| Grid-interactive AI load + BESS fast transfer | 用 AI workload scheduling、BESS 和开关控制把数据中心从纯负荷变成可调资源。 | 试点到早期商业化。 | Schneider、Eaton、Vertiv、ABB、Siemens、GE Vernova、Tesla Energy、Fluence、Powin、Bloom Energy、Enchanted Rock、utilities。 |

### 3.2 早期产品的订单规模与渗透率

| 早期/在研产品 | 情景 | 未来 3 个月订单 | 未来 12 个月订单 | 未来 24 个月订单 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 800VDC 配电与 rack power architecture | 基准 | $0.05-0.20B | $0.8-2.0B | $6-14B | 2026 试点 <2%，2027 5-10%，2028 10-20%。 |
|  | 乐观 | $0.20-0.60B | $2-5B | $14-32B | NVIDIA 生态方案被头部客户纳入 2027 标准设计。 |
|  | 极度超预期 | $0.60-1.50B | $5-12B | $32-70B | Vera Rubin/GB300 后续旗舰园区提前采用，DC switchgear 同步受益。 |
| DC breaker/e-fuse/DC protection | 基准 | $0.03-0.12B | $0.4-1.2B | $3-8B | 跟随 800VDC，2027 进入小批量。 |
|  | 乐观 | $0.12-0.35B | $1.2-3.0B | $8-18B | 保护标准和客户验证提前通过。 |
|  | 极度超预期 | $0.35-0.90B | $3-7B | $18-40B | DC 故障保护成为新的高壁垒利润池。 |
| MVDC campus / solid-state transformer | 基准 | $0.02-0.08B | $0.3-1.0B | $2-6B | 2028 前仍低个位数渗透。 |
|  | 乐观 | $0.08-0.25B | $1-2.5B | $6-15B | BESS/现场发电项目带动少量商业化。 |
|  | 极度超预期 | $0.25-0.70B | $2.5-6B | $15-35B | 若公用事业并网延迟倒逼 behind-the-meter DC 微电网，增速会很快。 |
| SF6-free MV/HV switchgear | 基准 | $0.3-0.7B | $2-4B | $6-12B | 新增 AI 项目 2026 5-12%，2027 10-20%。 |
|  | 乐观 | $0.7-1.3B | $4-8B | $12-24B | 欧洲、高 ESG hyperscaler、绿色融资项目优先。 |
|  | 极度超预期 | $1.3-2.2B | $8-14B | $24-42B | 法规/客户标准快速把 SF6-free 写入招标。 |
| Grid-interactive BESS + switchgear skids | 基准 | $0.5-1.0B | $3-6B | $10-20B | 2026 attach 15-30%，2027 25-45%。 |
|  | 乐观 | $1.0-2.0B | $6-12B | $20-38B | 并网排队和电价波动增强客户自备调节意愿。 |
|  | 极度超预期 | $2.0-3.5B | $12-22B | $38-70B | 大型 AI campus 默认配储能和现场电源接口。 |
| AI 电气数字孪生/预测维护软件 | 基准 | $0.1-0.3B | $0.8-1.8B | $2.5-5B | 与硬件打包，2027 开始显著增厚服务收入。 |
|  | 乐观 | $0.3-0.6B | $1.8-3.5B | $5-10B | Hyperscaler 要求跨园区资产健康模型。 |
|  | 极度超预期 | $0.6-1.2B | $3.5-7B | $10-20B | 电网互动、负载预测和可靠性保险定价推动软件高溢价。 |

### 3.3 早期产品利润率预测

| 产品 | 基准毛利率 | 乐观毛利率 | 极度超预期毛利率 | 为什么可能有高溢价 |
|---|---:|---:|---:|---|
| 800VDC 配电系统 | 28-42% | 35-50% | 45-60% | 初期供应商少，需共同设计、验证和长期服务。 |
| DC breaker/e-fuse/protection | 35-55% | 45-65% | 55-75% | 直流故障保护是安全核心，认证和失效数据壁垒高。 |
| MVDC/SST | 25-40% | 35-50% | 45-65% | 技术难、客户愿为并网速度和效率付费，但早期质保风险高。 |
| SF6-free switchgear | 28-42% | 34-48% | 40-55% | ESG/法规属性带来 green premium，型号覆盖决定规模。 |
| BESS + switchgear skid | 18-30% | 24-36% | 30-45% | 系统集成、保护逻辑和现场调试能力稀缺。 |
| 数字孪生/预测维护软件 | 55-75% | 60-80% | 70-85% | 软件订阅和服务随装机基数扩张，长期 ROIC 最高。 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 主要产能地区与公司

| 地区 | 产能特点 | 代表公司 |
|---|---|---|
| 美国 | 高价值最终市场，数据中心客户集中；主变/开关柜/低压盘柜/母线槽和 E-house 均在扩产，但仍依赖进口和海外部件。 | Eaton、Schneider/Square D、Siemens、ABB、GE Vernova/Prolec GE、Hitachi Energy、Powell、Hubbell、Vertiv/E+I、nVent/Avail/Trachte、Hyosung HICO、HD Hyundai Electric USA、Virginia Transformer、SPX Waukesha、Howard、Delta Star、S&C、G&W。 |
| 墨西哥/拉美 | Prolec GE 等变压器产能重要，服务北美；成本和供应链优势明显。 | Prolec GE、WEG、Siemens、Schneider、ABB。 |
| 欧洲 | 高端 MV/HV switchgear、SF6-free、自动化、dry-type transformer 技术强；本土数据中心和电网升级需求也强。 | Schneider、ABB、Siemens、Hitachi Energy、GE Vernova Grid Solutions、SGB-SMIT、Ormazabal、Lucy Electric、Socomec、Legrand。 |
| 韩国 | 超高压变压器、GIS 和北美出口优势突出，2026 订单高增长。 | HD Hyundai Electric、Hyosung Heavy Industries、LS Electric。 |
| 日本 | 超高压、GIS、工业电气可靠性强，但产能扩张相对谨慎。 | Mitsubishi Electric、Toshiba Energy Systems、Meidensha、Fuji Electric。 |
| 中国 | 规模产能最大之一，价格竞争力强；在高压、开关、变压器和数据中心电源均有完整链条，但受贸易/安全审查影响。 | TBEA、China XD、中国西电、平高电气、思源电气、许继电气、正泰、特变电工、华为数字能源、海鸿电气、伊戈尔。 |
| 印度/东南亚/中东 | 本地化和主权 AI 带动，正在承接部分变压器/开关柜扩产。 | CG Power、Bharat Heavy Electricals、Siemens Energy India、Hitachi Energy India、Schneider India、ABB India、Kirloskar Electric、Elsewedy、Alfanar。 |

### 4.2 供给瓶颈清单

至少 10 条瓶颈需要跟踪：

| 瓶颈 | 为什么卡 | 受影响产品 |
|---|---|---|
| GOES/CRGO 电工钢 | 变压器铁芯关键材料，全球可用产能有限，规格和损耗要求高。 | 主变、配电变压器、干式变压器。 |
| 铜/铝 | 绕组和母线用量大，价格波动直接影响 BOM。 | 变压器、switchgear、busway、PDU。 |
| 高压测试能力 | 大型变压器和 GIS 必须通过高压、冲击、温升、局放等测试，测试 bay 是硬瓶颈。 | 100MVA+ 主变、765kV 级变压器、HV GIS。 |
| 真空灭弧室/断路器机构 | MV switchgear 的核心件，可靠性和短路开断认证要求高。 | MV switchgear、arc-resistant switchgear。 |
| 套管、绝缘、油/天然酯 | 大型主变的关键部件，任何一个长交期都会拖延整机。 | 油浸式变压器、主变。 |
| 熟练工人 | 线圈绕制、焊接、装配、测试、现场调试依赖经验，培训周期长。 | 全部 ETO 电气设备。 |
| 客户认证/AVL | Hyperscaler 和 utilities 不会轻易导入未经长期验证的供应商。 | 开关柜、变压器、保护系统。 |
| 现场工程与调试 | 设备到场后仍需并网、保护整定、BMS/SCADA/DCIM 集成。 | 预制变电站、E-house、现场发电接入。 |
| 物流与运输 | 大型变压器超重超限，港口、铁路、公路许可和吊装都可能延误。 | 主变、E-house、大型 skids。 |
| 标准碎片化 | 各公用事业、州、客户短路容量、保护逻辑、接地和冗余偏好不同。 | 变压器、MV/HV switchgear。 |
| 关税与地缘风险 | 北美对中国电气部件依赖与安全审查并存。 | 开关柜部件、变压器部件、电子控制件。 |
| 800VDC 标准与保护 | DC arc、选择性保护、运维安全仍需标准化。 | 800VDC、DC switchgear、SST。 |

### 4.3 成本构成

| 产品 | 典型成本拆分 | 毛利决定因素 |
|---|---|---|
| 油浸式大型变压器 | GOES/铁芯 20-35%；铜/铝绕组 20-35%；油箱/钢材/散热器 10-18%；绝缘/油/套管/分接开关 10-20%；人工/测试 10-18%；物流/质保 5-10%；工程和 overhead 8-15%。 | 材料传导条款、产能稼动率、高压测试能力、客户愿付交期溢价、质保质量。 |
| 干式/浇注树脂变压器 | 铜/铝 25-40%；铁芯 15-25%；树脂/绝缘/外壳 15-25%；人工/测试 12-20%；工程/overhead 10-15%。 | 数据中心安全溢价、标准化批量、温升/噪声/效率指标。 |
| MV switchgear | 断路器/真空灭弧室 20-35%；铜母排 12-25%；钢柜体 10-20%；继电保护/控制 10-20%；人工装配/测试 15-25%；工程和物流 5-12%。 | arc-resistant、digital、短交期、客户 AVL、项目变更。 |
| LV switchgear/switchboards | 断路器/开关件 20-35%；铜母排 15-25%；柜体 10-18%；控制和仪表 8-18%；人工/测试 15-25%。 | 低压大批量能力、铜价传导、与 busway/PDU 打包。 |
| Busway/PDU/RPP | 铜/铝导体 25-45%；外壳和绝缘 15-25%；插接箱/保护 10-25%；人工/测试 10-18%；物流 5-10%。 | 高密度、快速安装、客户标准设计、热管理能力。 |
| E-house/预制电力模块 | 内含变压器、开关柜、母线、保护、暖通/消防、结构件；人工和项目管理占比高。 | 集成能力、现场风险转移、批量复制、工厂调试比例。 |

### 4.4 价格传导机制

1. 材料 pass-through：铜、铝、GOES 和钢材通常采用价格调整条款或报价有效期缩短。
2. 产能 slot premium：热门交期客户接受预付款、不可取消订单和 expedite fee。
3. 设计变更订单：AI 园区常因机架功率、BESS/发电机、utility interconnect 改变而产生变更。
4. 框架协议：hyperscaler 通过多年 MSA 锁价锁量，供应商换取可见度但牺牲部分 spot upside。
5. 服务附加：commissioning、maintenance、monitoring、spares、retrofit 带来更高毛利的售后收入。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 子市场 | 集中度判断 | 说明 |
|---|---|---|
| 数据中心端到端电气包 | CR5 约 55-70% | Schneider、Eaton、ABB、Siemens、Vertiv/GE/Hitachi 等拥有客户认证、全球服务和完整产品线。 |
| 北美 MV/LV switchgear for hyperscale | CR5 约 60-75% | Eaton、Schneider、Siemens、ABB、Powell、Vertiv/E+I 等主导大项目。 |
| 大型电力变压器/主变 | Top 10 约 60-75%，区域分割强 | Hitachi Energy、GE Vernova/Prolec、Siemens Energy、HD Hyundai、Hyosung、Mitsubishi、Virginia Transformer、SPX、WEG 等。 |
| Busway/PDU/RPP | CR5 约 50-65% | Legrand Starline、Eaton、Schneider、Vertiv/E+I、Siemens、ABB、nVent 等。 |
| SF6-free switchgear | 头部技术集中 | Schneider、ABB、Siemens、Hitachi、GE Vernova、Eaton、Mitsubishi 等有核心型号和试点案例。 |
| 800VDC/DC protection | 早期生态，集中度未定 | NVIDIA 牵引生态；最终价值可能在电力电子、DC protection、系统集成和标准制定者。 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 定价能力来源 |
|---|---|---|
| 可靠性和事故成本 | 数据中心电气事故可能导致整园区宕机，损失远超设备价格。 | 客户宁愿买贵设备和成熟供应商。 |
| 认证与短路测试 | UL/ANSI/IEEE/IEC、arc-resistant、short-circuit、温升、局放测试周期长且昂贵。 | 新进入者难以快速替代已认证供应商。 |
| 客户 AVL 和共同设计 | Hyperscaler 的参考设计、BMS/DCIM、保护逻辑与设备深度绑定。 | 一旦进入标准设计，后续园区复制带来长期订单。 |
| 服务网络 | 调试、备件、故障响应、现场改造需要本地工程师。 | 本地服务能力提升客户粘性。 |
| 高压测试和产能 slot | 大型变压器测试 bay、线圈设备和熟练工人有限。 | 供不应求时产能本身就是定价权。 |
| 工程项目管理 | E-house 和预制电力模块需要跨设备、结构、消防、HVAC、保护、软件集成。 | 能把现场工期从年压到月的供应商获得溢价。 |
| 供应链金融和履约能力 | 大订单需要履约保函、库存、应收和质保承担能力。 | 小厂难承接 hyperscale 多园区订单。 |
| 数据与软件 | 运行数据越多，预测维护模型越准确。 | 软件和服务可形成高毛利 recurring revenue。 |

### 5.3 价值捕获：哪一层最可能长期高 ROIC/高毛利

长期最有价值的是三层：

1. 端到端电气系统集成商：Schneider、Eaton、ABB、Siemens、Vertiv、GE Vernova/Hitachi 等，能从主变/MV/LV/busway/软件/服务中捕获多层价值，并通过客户标准化设计锁定重复订单。
2. 高压变压器和关键开关设备产能：Hitachi Energy、GE Vernova/Prolec、Siemens Energy、HD Hyundai、Hyosung、Powell、Eaton 等，产能和测试能力稀缺，2026-2027 定价权强。
3. 新架构核心保护与电力电子：如果 800VDC/MVDC 成为 2027-2028 主流增量，DC breaker、solid-state protection、SST、digital control 可能出现类似“电气系统里的高端芯片/模块”利润池。

纯低端盘柜、普通配件和无客户认证的二线产能 ROIC 会低得多，容易在扩产后价格回落。

## 6. 2026 关键变化：行业拐点与最可能放量的子方向

### 6.1 三个最可能拐点

| 2026 拐点 | 判断 | 最受益方向 |
|---|---|---|
| 电气设备从施工采购变成战略锁单 | GE Vernova、Eaton、Siemens Energy、Schneider、ABB 的 2026 订单均显示客户提前锁电气产能。 | 主变、MV switchgear、预制电力模块、busway。 |
| AI Factory 参考架构开始从 chip/rack 延伸到 grid-to-chip | Eaton 与 NVIDIA Beam Rubin DSX、NVIDIA 800VDC、Hitachi CERAWeek speed-to-power 等表明电气系统进入芯片路线图讨论。 | 端到端电力架构、800VDC 试点、数字电力系统。 |
| 数据中心项目开始“自带电力” | JLL 指出 behind-the-meter generation、BESS、private wire、bring-your-own-power 趋势增强。 | BESS 接入开关站、微电网 switchgear、现场发电变压器、并网设备。 |

### 6.2 2026 最可能放量子方向

1. MV switchgear：13.8/34.5kV 金属铠装、arc-resistant、数字化型号。
2. 大型主变/配电变压器：尤其北美本地产能和韩国/墨西哥进口链条。
3. 预制 power block/E-house：用于 50-200MW campus 快速复制。
4. Busway/PDU：100kW+ rack 的白空间配电价值量上升。
5. 数据中心电气监控和服务：从一次性设备向 lifecycle revenue 转化。

## 7. 2027 关键变化：行业拐点与最可能放量的子方向

### 7.1 三个最可能拐点

| 2027 拐点 | 判断 | 最受益方向 |
|---|---|---|
| 推理工作负载超过训练，园区从单个训练集群转向多园区复制 | JLL 预计 2027 inference 可能超过 training 成为主要 AI 需求。 | 标准化电气包、busway、低压配电、模块化白空间。 |
| 800VDC 从试点进入头部客户新设计 | 若 Vera Rubin/后续 rack 功率继续上行，800VDC 将从技术宣传转为招标项。 | DC switchgear、DC breaker、电力电子、SiC/GaN、800V busway。 |
| 供给扩产开始兑现，但仍不足以消除高端短缺 | Eaton、Hitachi、Siemens、HD Hyundai、Hyosung 等扩产陆续贡献，但测试/人才/认证仍约束。 | 已有客户认证和产能 slot 的供应商继续维持高利润。 |

### 7.2 2027 最可能放量子方向

1. 预制 AI Factory power block：从单项目工程变成批量制造。
2. SF6-free switchgear：欧洲和高 ESG 客户从可选项转入标准设计。
3. 800VDC/DC protection：从实验室/旗舰园区试点进入小规模商业订单。
4. Grid-interactive 数据中心：BESS、现场发电、负载调度、电气监控打包。
5. 高压输电与 765kV/500kV/345kV 设备：AI 园区外部电网升级拉动主变/GIS/reactor。

## 8. 头部公司与细分优势清单

### 8.1 端到端数据中心电气系统

| 公司 | 细分优势 | 2026 最新线索 |
|---|---|---|
| Schneider Electric | Energy Management、MV/LV、UPS、母线、液冷、EcoStruxure、数据中心端到端组合。 | 2026 Q1 Energy Management +12.8%，数据中心需求强；美国 $700M+ 投资支持能源与 AI。 |
| Eaton | Electrical Americas、MV/LV、变压器、switchgear、busway、UPS、电能质量、液冷并购。 | Q1 数据中心订单 +240%；Nebraska $30M MV switchgear 扩产；South Carolina $340M 变压器投资；Beam Rubin DSX。 |
| ABB | Electrification、switchgear、UPS、modular substation、NeoGear/EconiQ、DC 架构。 | Q1 Electrification book-to-bill 1.44；数据中心订单强。 |
| Siemens / Siemens Energy | Siemens AG 做 LV/MV、busway、自动化；Siemens Energy 做 HV transformers、GIS、grid。 | Siemens AG $165M 扩产 AI 基建电气设备；Siemens Energy Grid Technologies 2026 指引上调。 |
| Vertiv | Critical power、UPS、switchgear、busway、modular power、thermal、服务。 | Q1 销售 +30%，全年指引 $13.5-14B；E+I 和模块化电力能力强。 |
| GE Vernova / Prolec GE | Grid Solutions、transformers、HVDC、switchgear、electrification、Prolec 变压器。 | Q1 数据中心 Electrification 订单 $2.4B，完成 Prolec GE 收购。 |
| Hitachi Energy | HV/MV transformers、GIS、EconiQ、grid automation、服务。 | 美国 $1B+ 制造投资，含 Virginia $457M transformer facility；CERAWeek 2026 强调 speed-to-power。 |

### 8.2 变压器

| 细分 | 头部公司 |
|---|---|
| 超高压/大型主变 | Hitachi Energy、GE Vernova/Prolec GE、Siemens Energy、HD Hyundai Electric、Hyosung Heavy Industries、Mitsubishi Electric、Toshiba Energy Systems、SPX Waukesha、Virginia Transformer、WEG、SGB-SMIT、TBEA、中国西电、保变电气。 |
| 北美本地与近岸产能 | Eaton、GE Vernova/Prolec GE、Hitachi Energy、Siemens Energy、Virginia Transformer、SPX Waukesha、Howard Industries、Delta Star、HD Hyundai Electric USA、Hyosung HICO、WEG、Hammond。 |
| 干式/浇注树脂 | Schneider、Eaton、Hitachi Energy、Siemens、SGB-SMIT、Hammond、TMC Transformers、CG Power、MGM Transformer、Legrand、JST、伊戈尔、海鸿电气。 |
| 韩国出口链 | HD Hyundai Electric、Hyosung Heavy Industries、LS Electric。 |
| 中国供应链 | TBEA、China XD、中国西电、保变电气、特变电工、正泰电器、思源电气、许继电气、平高电气。 |

### 8.3 开关设备、母线与模块化电力

| 细分 | 头部公司 |
|---|---|
| MV switchgear | Eaton、Schneider、ABB、Siemens、Powell Industries、GE Vernova、Hitachi Energy、Mitsubishi、LS Electric、Hyosung、S&C Electric、G&W Electric、Ormazabal、Lucy Electric、Chint、正泰、平高、许继、思源。 |
| LV switchgear/switchboard | Schneider/Square D、Eaton、Siemens、ABB、Vertiv/E+I、Legrand、nVent/Avail、Powell、Mitsubishi、Fuji Electric、LS Electric、Chint。 |
| Busway/PDU/RPP | Legrand Starline、Eaton、Schneider、Siemens、ABB、Vertiv/E+I、nVent ERIFLEX/Avail、EAE Electric、Anord Mardix、LS Electric、Delta Electronics、Socomec。 |
| E-house/预制模块 | Vertiv、Eaton/Fibrebond、Schneider、ABB、Siemens、nVent Trachte/Avail、Powell、GE Vernova、AZZ、Dashiell、Powell、Anord Mardix。 |
| SF6-free switchgear | Schneider AirSeT、ABB EconiQ/NeoGear、Siemens blue GIS、Hitachi Energy EconiQ、GE Vernova g3、Eaton Xiria、Mitsubishi、Toshiba、Ormazabal。 |
| 数字保护/监控 | Schneider EcoStruxure、Eaton Brightlayer、ABB Ability、Siemens SICAM/SIPROTEC、SEL、GE Vernova、Hitachi Energy、S&C、Schweitzer Engineering、Omicron、Doble。 |

### 8.4 800VDC、DC protection、SST 和电力电子

| 细分 | 公司 |
|---|---|
| 800VDC 系统生态 | NVIDIA、ABB、Eaton、GE Vernova、Hitachi Energy、Schneider Electric、Siemens、Vertiv、Delta、Flex、Lite-On、Megmeet、Mitsubishi Electric。 |
| 功率半导体与控制 | Infineon、Texas Instruments、Analog Devices、Monolithic Power Systems、Navitas、EPC、Power Integrations、ROHM、Renesas、onsemi、STMicroelectronics、AOS、Wolfspeed。 |
| 固态变压器/高级电力电子 | Eaton/Ultra PCS、ABB、Siemens、Schneider、GE Vernova、Hitachi Energy、Mitsubishi、Delta、Huawei Digital Power、Heron Power。 |
| 连接器/铜缆/高密电力连接 | Amphenol、TE Connectivity、BizLink、Molex、Legrand、nVent、Eaton、Schneider、Vertiv。 |

## 9. 投资价值判断

### 9.1 最强 alpha

| 排名 | 方向 | 为什么 |
|---:|---|---|
| 1 | 北美/近岸大型变压器产能 | 交期最长、供应最紧、客户最愿预付，且 AI/电网/新能源共同抢产能。 |
| 2 | MV switchgear 与 arc-resistant/digital switchgear | 每个 AI campus 必配，供给扩张慢，客户认证壁垒强。 |
| 3 | 预制电力模块/E-house | 把现场施工瓶颈转为工厂制造，直接解决 JLL 所说的项目延误。 |
| 4 | Busway 与高密白空间配电 | 100kW+ rack 提高单位白空间电气价值量。 |
| 5 | 电气软件/监测/服务 | 装机基数扩张后 recurring revenue 和毛利率更高。 |

### 9.2 最强 beta

| 排名 | 方向 | 触发条件 |
|---:|---|---|
| 1 | 800VDC/DC protection | NVIDIA Vera Rubin/后续平台若把 800VDC 写入头部客户参考设计。 |
| 2 | BESS/现场发电接入开关站 | 并网延迟恶化，AI campus 继续“bring your own power”。 |
| 3 | SF6-free switchgear | 欧洲法规、hyperscaler ESG 和绿色融资把 SF6-free 变成硬要求。 |
| 4 | 高压输电和 765kV 设备 | 美国/中东/印度 AI 园区需要远距离大容量输电。 |

### 9.3 最大风险

1. AI CapEx 短期降速：如果 hyperscaler 对 token ROI 转谨慎，订单可能从极度超预期回到基准，但电气设备因前置锁单仍有滞后保护。
2. 扩产后周期性：2028 之后若太多中低端产能释放，普通配电变压器/低压盘柜毛利可能回落。
3. 固定价老订单：材料成本和关税上升可能侵蚀 2024-2025 签的低价订单。
4. 质量和质保：大型变压器事故、开关柜故障和现场集成问题会造成巨额赔付和客户流失。
5. 监管和社区阻力：水、电、噪声、碳排、土地许可可能影响实际建设节奏。

## 10. 信息源与验证表

| 来源 | 关键事实/用途 | 链接 |
|---|---|---|
| Eaton 2026 Q1 analyst presentation | Electrical Americas 数据中心订单 +240%；Electrical Americas backlog +44%；数据中心占 2025 Eaton sales 21%；Beam Rubin DSX 与 NVIDIA；Electrical Americas Q1 利润率 25.6%。 | [Eaton Q1 2026 analyst presentation](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf) |
| Eaton 2026 Nebraska MV switchgear investment | $30M+ 扩产 MV switchgear，直接指向 AI data center boom；Eaton 自 2023 年全球制造投资 $1.5B+。 | [Eaton Nebraska expansion](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-expands-operations-in-nebraska-with-new-manufacturing-facility.html) |
| Eaton South Carolina transformer site | $340M 三相变压器投资，服务数据中心、电网现代化、电气化和工业化。 | [Eaton transformer manufacturing](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2025/eaton-invests-in-new-south-carolina-transformer-manufacturing.html) |
| Schneider Electric 2026 Q1 revenues | Q1 收入 €9.767B、organic +11.2%；Energy Management +12.8%；数据中心和北美强。 | [Schneider Q1 2026](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026) |
| Schneider U.S. investment | 美国 $700M+ 投资，支持能源和 AI sectors。 | [Schneider U.S. investment](https://www.se.com/us/en/about-us/newsroom/news/press-releases/schneider-electric-plans-to-invest-over-700-million-in-the-u-s-supporting-energy-ai-sectors-and-job-growth-67bdeb3ee4475a5955011b6a/) |
| ABB Q1 2026 financial information | Electrification 订单 $6.647B、收入 $4.613B、book-to-bill 1.44；产品组合包含 switchgear、UPS、modular substations 等。 | [ABB Q1 2026 financial information](https://library.e.abb.com/public/92757491d9cc40af8425ef03a7f45f81/ABB-Q1-2026-financial-information.pdf) |
| ABB Q1 2026 secondary coverage | 数据中心订单三位数增长的补充线索。 | [ABB Q1 2026 EMR coverage](https://www.emr-online.com/abb-q1-2026-results/) |
| Vertiv Q1 2026 results | Q1 销售 $2.65B、同比 +30%；有机销售 +22.6%；全年销售指引 $13.5-14.0B，调整后经营利润率 22.8-23.8%。 | [Vertiv Q1 2026](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx) |
| GE Vernova Q1 2026 | Q1 订单 $18.3B、organic +71%；backlog +$13B；Electrification 数据中心设备订单 $2.4B；Prolec GE acquisition；Electrification 指引 $14.0-14.5B、margin 18-20%。 | [GE Vernova Q1 2026](https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf) |
| Siemens Energy Q1 FY2026 | backlog €146B；Grid Technologies 订单 +21.8%；美国数据中心相关订单高三位数百万欧元；Grid margin 17.6%。 | [Siemens Energy Q1 FY2026](https://www.siemens-energy.com/global/en/home/press-releases/earnings-release-q1-fy-2026.html) |
| Siemens Energy Q2 preliminary / guidance raise | Grid Technologies 2026 指引上调至收入 +25-27%、利润率 18-20%；Q2 Grid 订单 €6.996B、+41.5%。 | [Siemens Energy Q2 preliminary](https://www.siemens-energy.com/global/en/home/press-releases/ad-hoc--siemens-energy-ag-raises-full-year-outlook-and-releases-.html) |
| Siemens AG U.S. AI infrastructure investment | $165M 扩产 North/South Carolina 电气设备，支持数据中心和 AI factories。 | [Siemens $165M AI infrastructure manufacturing](https://press.siemens.com/global/en/pressrelease/siemens-invests-165-million-expand-us-manufacturing-ai-infrastructure) |
| Hitachi Energy U.S. investment | $1B+ 美国制造投资，含 $457M South Boston power transformer facility、dry-type transformer、high-voltage components。 | [Hitachi U.S. grid investment](https://www.hitachi.com/en-us/press/hitachi-announces-historic-1-billion-usd-manufacturing-investment-to-power-americas-energy-future/) |
| Hitachi Energy transformer expansion | $250M additional transformer investment，建立在 $6B 2024 投资计划和 $1.5B transformer scaling 上。 | [Hitachi additional transformer investment](https://www.hitachi.com/New/cnews/month/2025/03/250311a.html) |
| Hitachi at CERAWeek 2026 | 强调 speed-to-power、AI factories 会达到城市级 GW 电力需求。 | [Hitachi CERAWeek 2026](https://www.hitachienergy.cn/cn/zh/news-and-events/press-releases/2026/03/hitachi-at-ceraweek-2026) |
| Powell Industries Q2 FY2026 | backlog $1.8B，Q2 后获得 $400M+ mega data center order。 | [Powell Q2 FY2026](https://www.stocktitan.net/news/POWL/powell-industries-announces-second-quarter-fiscal-2026-4kx5spwkrt8c.html) |
| nVent Q1 2026 | organic orders 约 +40%，backlog $2.6B，AI data center buildout 为主因；Avail 提供 enclosures、switchgear、bus systems。 | [nVent Q1 2026 coverage](https://www.fool.com/earnings/call-transcripts/2026/05/01/nvent-nvt-q1-2026-earnings-call-transcript/)、[nVent official site](https://www.nvent.com/) |
| Hyosung Feb 2026 | 美国 $530M 765kV 超高压变压器和电抗器订单；2025 曾签 765kV transformer + 800kV GIS full-package；Memphis 是美国少数 765kV 产能。 | [Hyosung PRNewswire](https://www.prnewswire.com/news-releases/hyosung-heavy-industries-secures-record-order-as-hyun-joon-chos-us-strategy-pays-off-302686142.html) |
| HD Hyundai Electric Mar 2026 | Alabama 第二工厂，$200M 投资，容量 +50%，新增 765kV class 能力。 | [HD Hyundai Electric U.S. expansion](https://www.prnewswire.com/news-releases/hd-hyundai-electric-expands-us-production-subsidiary-solidifies-leadership-in-north-american-extra-high-voltage-power-transformer-market-302707507.html) |
| JLL 2026 Global Data Center Outlook | 全球容量 2025-2030 约 103GW -> 200GW；2026-2030 新增 100GW 需最高 $3T；设备平均交期 33 周，美国 42 周；57% 项目延误。 | [JLL 2026 Global Data Center Outlook](https://www.jll.com/content/dam/jllcom/en/global/documents/reports/research-reports/26-research-global-data-center-outlook-new.pdf) |
| IEA Energy and AI | 数据中心约贡献全球 2030 前电力需求增长 10%；20% 规划项目可能因电网延迟受风险；变压器和电缆等待时间三年翻倍。 | [IEA Energy and AI executive summary](https://www.iea.org/reports/energy-and-ai/executive-summary%C2%A0) |
| Uptime Institute 2026 predictions | 2030 前全球数据中心电力需求增长 75-125GW，推动 gas turbines 等 primary power。 | [Uptime 2026 predictions](https://uptimeinstitute.com/about-ui/press-releases/uptime-institute-announces-five-data-center-predictions-report-for-2026) |
| DOE supply chain and market analysis | 配电变压器交期从 2019 年 3-6 个月上升到 2023 年 12-30 个月；瓶颈含 GOES、铜铝、劳动力、组件。 | [DOE supply chain and market analysis](https://www.energy.gov/oe/supply-chain-and-market-analysis) |
| Wood Mackenzie transformer deficit | 2025 年美国 power transformer 和 distribution transformer 供给缺口约 30%/10%。 | [Wood Mackenzie transformer supply deficit](https://www.woodmac.com/press-releases/power-transformers-and-distribution-transformers-will-face-supply-deficits-of-30-and-10-in-2025/) |
| NVIDIA 800VDC architecture | 800VDC 目标减少转换级数、电流、铜耗和线缆体积；合作伙伴包括 ABB、Eaton、GE Vernova、Hitachi、Schneider、Siemens、Vertiv 等。 | [NVIDIA 800VDC architecture](https://www.nvidia.com/en-us/data-center/technologies/800-vdc-architecture/) |
| NVIDIA Vera Rubin technical blog | Vera Rubin POD、dynamic power steering、rack-level energy storage、45C liquid cooling、Spectrum-6 CPO 等。 | [NVIDIA Vera Rubin POD blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) |
| NVIDIA Vera Rubin press release | 2026 年 Vera Rubin 七类芯片 full production、五种 rack-scale systems。 | [NVIDIA Vera Rubin press release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) |
| Tom's Hardware / Bloomberg / Sightline secondary | 非一手但有用的供需压力线索：美国 2026 约 12GW 预期上线但只有约 1/3 在建；高功率变压器交期可到 5 年。 | [Tom's Hardware summary](https://www.tomshardware.com/tech-industry/artificial-intelligence/half-of-planned-us-data-center-builds-have-been-delayed-or-canceled-growth-limited-by-shortages-of-power-infrastructure-and-parts-from-china-the-ai-build-out-flips-the-breakers) |

## 11. 读数注意事项

1. 本文市场规模为 AI 数据中心“直接相关新增订单”，不是全部电网设备市场，也不是供应商确认收入。
2. 同一个 AI campus 的电气包可能被拆分为 utility substation、owner-furnished equipment、EPC、white-space fit-out 和 OEM skid，因此公司订单不能直接相加。
3. 变压器、switchgear、busway、UPS、BESS、现场发电之间存在边界重叠；本文尽量把 UPS 电池本体、发电机和冷却设备排除，只保留与开关设备和变压器直接相连的电气集成。
4. 极度超预期乐观情景的核心假设是：2026-2027 AI 推理需求继续吸收所有可交付电力，hyperscaler 继续用预付款抢电气产能，且 800VDC/预制 power block 的客户验证快于常规工业周期。
5. 非投资建议，仅用于产业链研究和情景分析。
# 行业调研：【数据中心土建、MEP与预制化交付】

> 截至日期：2026-05-08  
> 口径：美元名义值，`B` = 十亿美元。除特别说明外，市场规模指全球 AI 数据中心新增建设中的土建、MEP、电力、冷却、预制化模块、调试与运维相关订单/收入池，不含 GPU/HBM/服务器本体价值。美国仍是最大落地区域，约占 2026-2027 年全球 AI 数据中心非 IT 基础设施增量的 45%-60%。  
> 情景：`基准` = 高速增长但受电力/设备/人力约束；`乐观` = hyperscaler 和 neocloud 公告项目按计划转化；`极度超预期乐观` = 2027 需求前置、现场能源与预制化显著缓解上电约束。  
> 非投资建议。本报告刻意对 2026-2027 AI 计算中心建设保持乐观假设；找不到直接数据的环节以公开锚点加产业链推算给出大胆区间。

## 0. 一页结论

数据中心土建、MEP 与预制化交付正在从传统地产/工程生意，变成 AI Factory 的“算力发行能力”。2026 年的核心不是“有没有需求”，而是“能不能把电、冷却、机电安装和调试能力变成可复制模块”。这会使价值链从低毛利土建向三类高价值环节迁移：高压/中压配电与 800 VDC 保护、电液一体化预制模块、客户认证后的液冷组件与运维软件。

**最强投资主线：**

| 排名 | 子方向 | 2026-2027 变化 | 最可能捕获价值的公司类型 |
|---:|---|---|---|
| 1 | 变压器、开关柜、母线槽、UPS/BESS、电能质量 | 电力设备成为项目开工前置条件，交期 24-60 个月；即使 GPU 延迟，业主也先锁电力链 | Eaton、Schneider、Vertiv、ABB、Siemens、GE Vernova、Hitachi Energy、Powell、Hubbell、nVent |
| 2 | 直接到芯片液冷 DTC：CDU、冷板、歧管、快接、泵阀、传感器 | GB300/Rubin/MI400/Trainium/TPU 推动 100kW+ 机架，液冷从选配变默认 | Vertiv、Schneider/Motivair、Eaton/Boyd、CoolIT、nVent、Nidec、Delta、Asetek、LiquidStack、Submer |
| 3 | 预制化 MEP：power block、e-house、white-space pod、rack/pod integration | 现场工人和交叉施工成为瓶颈，工厂集成+现场拼装缩短工期 30%-70% | Vertiv、Schneider、Eaton、Compass、Flex、Jabil、Foxconn、Quanta/Wiwynn、Exyte、DPR、Holder |
| 4 | 高端 MEP/EPC 与调试 | 数据中心项目从单楼变成 500MW-GW 园区，客户要“可交付电力+确定工期” | Comfort Systems USA、EMCOR、Quanta、MYR、MasTec、Rosendin、M.C. Dean、Faith Technologies、Jacobs、AECOM |
| 5 | 数字孪生/DCIM/预测性维护 | DSX/ETAP/AVEVA/Omniverse 把设计、施工、调试、运行连成闭环，按 MW/token 优化 | Schneider ETAP/AVEVA、Vertiv Unify/Next Predict、NVIDIA DSX、Siemens、Cadence、Dassault、Phaidra、Procore、Jacobs |

**关键锚点：**

- CBRE 2026 展望称美国数据中心需求继续创纪录，但 500MW+ AI 园区把传统 12-18 个月项目拉长到多年，若涉及高压输电/新增发电，并网周期可到 24、36 甚至 48+ 个月；在建项目预租率预计维持 mid-70%，远高于 40%-50% 历史均值。[CBRE 2026 Data Centers](https://www.cbre.com/insights/books/us-real-estate-market-outlook-2026/data-centers)
- JLL 预计全球数据中心 shell/core 建设成本从 2020 年 $7.7M/MW 升至 2025 年 $10.7M/MW，2026 年再升至 $11.3M/MW；AI 技术 fit-out 可高达 $25M/MW。[JLL 2026 Global Data Center Outlook](https://www.jll.com/en-ca/insights/market-outlook/data-center-outlook)
- McKinsey 2026 年 3 月报告把到 2030 年数据中心建设机会量级放到约 $7T，明确提出 liquid cooling、预制化模块和电力动态响应正在打破传统供应商模式。[McKinsey $7T build-out](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-7-trillion-dollar-data-center-build-out-how-industrials-can-capture-their-share)
- McKinsey 另一篇电力/冷却报告预计液冷设备从 2025 年 $2B-$3B 增至 2030 年 $15B-$17B，CAGR 45%-50%；heat rejection 从 $3B-$5B 增至 $12B-$14B。[McKinsey power/cooling PDF](https://www.mckinsey.com/~/media/mckinsey/industries/advanced%20electronics/our%20insights/beyond%20compute%20infrastructure%20that%20powers%20and%20cools%20ai%20data%20centers/beyond-compute-infrastructure-that-powers-and-cools-ai-data-centers.pdf)
- NVIDIA GTC 2026 发布 Vera Rubin DSX AI Factory reference design，合作伙伴包括 Eaton、Jacobs、Schneider、Siemens、Switch、Trane、Vertiv 等，重点是 power/cooling/network/compute 统一数字孪生。[NVIDIA DSX 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-Vera-Rubin-DSX-AI-Factory-Reference-Design-and-Omniverse-DSX-Digital-Twin-Blueprint-With-Broad-Industry-Support/default.aspx)
- Vertiv 2025Q4 organic orders 同比 +252%，backlog $15.0B、同比 +109%；2026Q1 revenue $2.65B、同比 +30%，2026 年收入指引 $13.5B-$14.0B。[Vertiv Q4 2025](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)；[Vertiv Q1 2026](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx)
- Eaton 2026Q1 Electrical Americas 12 个月滚动平均订单 +42%，Electrical sector backlog 同比 +48%，收购 Boyd Thermal 强化数据中心热管理。[Eaton Q1 2026](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html)
- Schneider 2026Q1 Data Center & Networks 需求 double-digit，pure Data Center 需求 double-digit，AI-ready 基础设施端到端组合被广泛采用。[Schneider Q1 2026](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026)
- OCP 2026 Open Data Center for AI 指出 rack power density 已出现数量级跃迁，路线图指向未来数年 1MW rack，优先标准包括高电压 LVDC、Liquid Cooling CDU、BESS、microgrid、遥测与功率估算。[OCP Open DC for AI](https://www.opencompute.org/projects/open-dc-for-ai)

## 1. AI 芯片技术路径如何映射到 2026-2027 土建/MEP/冷却机会

项目本地已有芯片底稿：`ai_chip_research_2026_2027.md`。这里不重新外搜芯片，只把 2026-2027 出货量/价值最大的 AI 芯片路径映射成设施侧需求。

### 1.1 2026-2027 最大 AI 芯片/平台及设施含义

| 芯片/平台 | 2026-2027 判断 | 设施侧直接影响 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 最确定主力，NVL72 rack 级交付 | 100kW+ rack、DTC 液冷、480VAC/54V 仍主流，800G/1.6T 网络拉动灰空间与光纤布线 |
| AWS Trainium2 | Rainier/Anthropic 大规模部署，百万级芯片池 | 自研 rack + 云厂商自有园区，风液混合到液冷，要求大规模重复交付 |
| Google TPU v7 Ironwood | Google Cloud + Anthropic TPU 扩容，推理优先 | Google/OCP/Project Deschutes 推动 2MW CDU、开放冷却规范 |
| NVIDIA B200/GB200 | 存量订单延续，部分客户继续部署 | 既有 NVL72 机房改造与液冷运维、brownfield retrofit |
| Huawei Ascend 910C/950 | 中国国产替代与超节点集群 | 国产液冷、国产配电、国内园区电力接入和主权 AI 项目 |
| Cambricon MLU 590/690 | 中国云厂商与国产替代订单 | 风冷到液冷过渡，OAM/国产互连配套 |
| AMD MI350/MI355 | 2026 AMD 最确定放量，企业/云双路线 | UBB/PCIe 多形态，风液并存，ROCm 集群调试复杂度提高 |
| AWS Trainium3 | 2026 初期、2027 扩张，144 芯片 UltraServer | 高密 rack，垂直整合电源与网络，液冷 attach 上升 |
| Meta MTIA 300/400/500 | 推理 ASIC GW 级趋势 | OCP/Open Rack Wide、低 TCO、标准机架与液冷/风液混合 |
| Microsoft Maia 200 | Azure 推理自研芯片，闭环液冷 | 750W 级 SoC、闭环液冷 HEU，Azure 机房内生热管理标准化 |
| AMD MI400/MI455X Helios | 2026H2 起步，2027 潜在主力 | HBM4 + 72 GPU rack，全液冷，2027 对 800VDC/高功率母线更友好 |

### 1.2 技术成熟与放量时间：三情景

| 技术路径 | 2026 成熟度 | 基准放量 | 乐观放量 | 极度超预期乐观放量 | 2026 最可能结论 |
|---|---|---|---|---|---|
| 480VAC/415VAC 到 rack，rack 内 54V/48V | 成熟 | 已放量 | 已放量 | 已放量 | 2026 主流，不会被 800VDC 立刻替代 |
| Direct-to-chip 液冷：冷板+CDU+歧管 | 高速爬坡 | 2026H2 GB300/NVL72 批量 | 2026Q2-Q4 全面 attach | 2026Q3 起 100kW+ rack 默认 | 2026 最确定放量产品 |
| Rear-door heat exchanger / hybrid air-liquid | 成熟上量 | brownfield 与中密 rack 放量 | 与 DTC 组合放量 | 成为改造项目标配 | 适合过渡与 retrofit |
| Project Deschutes/OCP 2MW CDU | 样机/认证到小批量 | 2026H2 小批量 | 2026H2-2027H1 多供应商 | 2026Q4 成为 hyperscaler 标准 CDU 之一 | 2026 认证，2027 放量 |
| Prefab power block / e-house / white-space pod | 成熟但供应不足 | 2026 全年放量 | 2026H2 工厂化显著扩产 | 大项目强制模块化，现场工期缩短 50%+ | 2026 高确定、高弹性 |
| Digital twin for AI Factory | 设计端成熟、运维端早期 | 2026 用于设计/仿真 | 2026H2 进入调试和运维 | 2027 按 token/MW 自动优化 | 2026 设计工具，2027 运维工具 |
| 800 VDC / +/-400V DC | 标准与生态爬坡 | 2027 Kyber/Rubin 后小批量 | 2027H1 首批商业项目 | 2026H2 部分 rack-level 示范，2027 成为新建 AI hall 可选主线 | 2026 非主流，2027 关键拐点 |
| SST 中压 AC 到 800VDC | 论文/示范阶段 | 2028 后 | 2027H2 小规模 | 2027 在大型园区局部试点 | 高壁垒在研，不宜计入 2026 主收入 |
| 浸没/两相/相变冷却 | 产品可用但标准和服务弱 | 2027 小众高密/边缘 | 2027 扩大到专用 AI pod | 2026H2 少数专用集群突破 | 2026 不是主流，2027 后可选 |
| On-site generation + BESS + microgrid | 需求强，审批/燃料约束 | 2026-2027 项目合同先行 | 2027 形成批量园区方案 | 2026H2 大客户绕过电网瓶颈 | 最强“上电加速器” |

### 1.3 2026 最可能技术路径

2026 最可能不是某个单点技术胜出，而是“480VAC/54V + DTC 液冷 + 预制化 power/cooling block + 数字孪生设计”的组合拳。800VDC、SST、1MW rack、两相冷却会成为 2027 估值叙事，但 2026 大规模收入仍主要来自成熟可认证产品。

## 2. 已经开始放量的关键产品：市场规模、渗透率、毛利率

### 2.1 产品拆分与三情景市场规模

口径：全球 AI 数据中心新增建设订单/供应商收入池；未来 3 个月为 2026-05-08 至 2026-08-08，1 年为 2027-05，2 年为 2028-05 的累计区间。

| 已放量产品 | 未来 3 个月：基准/乐观/极度乐观 | 未来 1 年：基准/乐观/极度乐观 | 未来 2 年：基准/乐观/极度乐观 | 当前渗透率 | 2 年渗透率路径 |
|---|---:|---:|---:|---:|---|
| 土建、场平、壳体、白空间基础 fit-out | $18-28B / $26-38B / $35-52B | $85-125B / $120-180B / $170-250B | $190-300B / $280-460B / $420-700B | AI-ready 新建项目约 55%-70% | 70%-90%，由传统云楼变 AI hall/AI campus |
| MEP 安装、管线、电气/机械调试 | $20-32B / $30-45B / $42-65B | $90-150B / $135-220B / $200-330B | $220-380B / $360-620B / $550-950B | 高端项目中专业 MEP 约 65%-80% | 80%-95%，客户更偏 self-perform 与认证承包商 |
| 变压器、开关柜、母线槽、PDU/RPP | $22-36B / $34-52B / $48-78B | $95-160B / $150-240B / $230-370B | $240-430B / $400-720B / $650-1,150B | AI 项目电力链订单约 45%-60% | 65%-85%，800VDC 前先由 480VAC/高密母线吃量 |
| UPS、电池、BESS、电能质量、飞轮/超级电容 | $12-22B / $20-34B / $32-55B | $55-105B / $95-170B / $160-280B | $145-310B / $260-560B / $480-950B | 新建 AI 园区约 30%-45% 采用 BESS/microgrid 方案 | 55%-80%，负载波动和并网约束推动 |
| 柴油/燃气发电机、燃气轮机、燃料电池、现场能源 | $8-16B / $15-28B / $28-48B | $40-90B / $80-160B / $150-280B | $120-300B / $260-650B / $550-1,250B | 现阶段多为备用，主动供电约 10%-20% | 25%-55%，取决于天然气接入和监管 |
| 预制 power module / e-house / power skid | $7-14B / $12-24B / $22-40B | $35-75B / $65-130B / $120-230B | $95-230B / $190-480B / $380-900B | 新建高密项目约 20%-35% | 45%-70%，现场工期越紧越高 |
| Direct-to-chip 液冷组件：CDU、冷板、歧管、快接、泵阀 | $5-9B / $8-15B / $14-25B | $22-45B / $40-80B / $75-140B | $65-160B / $130-320B / $260-650B | 高端 AI rack attach 约 25%-40% | 60%-85%，100kW+ rack 基本默认 |
| Heat rejection：冷水机组、冷却塔、干冷器、板换、二次侧泵站 | $6-12B / $10-19B / $18-32B | $28-60B / $52-105B / $95-180B | $80-190B / $160-380B / $320-750B | 液冷项目约 35%-50% 需要升级 | 65%-90%，warm water/dry cooler 提升价值 |
| RDHx / InRow / hybrid air-liquid | $2-4B / $3-7B / $6-12B | $9-20B / $18-38B / $35-70B | $25-65B / $55-140B / $110-280B | brownfield AI 改造约 15%-25% | 30%-55%，作为 DTC 过渡与辅冷 |
| 预制 white-space pod / AI pod / rack-roll solution | $5-11B / $9-20B / $18-35B | $28-70B / $60-140B / $120-260B | $85-230B / $190-520B / $420-1,000B | 新建项目约 10%-25% | 35%-65%，尤其 10MW-100MW 标准区块 |
| DCIM、数字孪生、预测性维护、AI 运维 | $1-3B / $2-5B / $4-8B | $7-16B / $14-32B / $28-60B | $25-70B / $55-150B / $120-320B | 大型 AI 项目约 20%-35% | 55%-85%，从设计仿真进入运行优化 |

### 2.2 已放量产品毛利率：三情景

毛利率为供应商层面粗略区间，不等同公司整体毛利率；EPC/MEP 更应看项目毛利与 operating margin。

| 产品/环节 | 当前供需状态 | 基准毛利率 | 乐观毛利率 | 极度超预期乐观毛利率 | 定价能力原因 |
|---|---|---:|---:|---:|---|
| 土建壳体 | 需求强但可替代供应商较多 | 8%-14% | 12%-18% | 15%-22% | 位置/电力稀缺比施工本身更值钱 |
| MEP 专业安装与调试 | 认证承包商紧缺 | 16%-24% | 22%-30% | 28%-36% | 工期、质量、带电调试风险和客户信用锁定 |
| 变压器/开关柜/母线槽 | 长交期、扩产慢 | 28%-40% | 36%-48% | 45%-58% | 规格认证、交期、产能槽位、客户预付款 |
| UPS/BESS/电能质量 | 从备电走向主动调峰 | 25%-38% | 32%-45% | 40%-55% | 电网侧约束和 AI 负载波动提高冗余价值 |
| 发电机/燃气轮机/fuel cell | 项目制，监管和燃料决定节奏 | 18%-32% | 28%-42% | 38%-55% | 能“先上电”的项目有强溢价 |
| 预制 power block/e-house | 工厂产能紧缺 | 18%-30% | 26%-38% | 35%-48% | 缩短现场工期、降低返工、可复制设计 |
| CDU/冷板/歧管/快接 | 多数供应商仍在认证/爬坡 | 28%-42% | 38%-52% | 48%-65% | 漏液责任、热性能、客户认证和服务网络 |
| Heat rejection | 龙头设备+本地工程混合 | 22%-34% | 30%-42% | 38%-52% | 高温水、干冷、节水、热回收设计能力 |
| RDHx/InRow/hybrid | 成熟但因 retrofit 需求提高 | 24%-36% | 32%-45% | 40%-55% | brownfield 改造时间价值高 |
| 预制 AI pod/rack-roll | 系统集成溢价提升 | 20%-32% | 30%-42% | 40%-55% | 模块认证、供应链协同、工期确定性 |
| DCIM/数字孪生/预测性维护 | 软件毛利高，实施复杂 | 55%-75% | 65%-82% | 75%-90% | 数据闭环、客户切换成本、运维 SLA |

## 3. 在研/早期放量技术：成熟时间、市场规模和利润率

### 3.1 在研关键技术与产品

| 在研/早期技术 | 2026 状态 | 未来 3 个月市场 | 未来 1 年市场 | 未来 2 年市场 | 2 年渗透率路径 | 毛利率潜力 |
|---|---|---:|---:|---:|---|---|
| 800 VDC / +/-400V rack 或 facility distribution | 标准、生态、示范；NVIDIA 指向 2027 Kyber | $0.5-2B | $3-12B | $25-90B | <3% -> 10%-25% 新建高端 AI hall | 35%-60%，保护器件/电力电子更高 |
| 固态变压器 SST：MVAC 到 800VDC | 论文/RTDS/示范阶段 | <$0.5B | $1-4B | $8-30B | <1% -> 3%-10% | 40%-65%，但工程风险高 |
| rack 级超级电容 + facility BESS 多时间尺度储能 | 技术清晰，工程标准化不足 | $1-3B | $8-25B | $40-140B | 5%-10% -> 25%-50% | 30%-55%，控制软件/功率器件更高 |
| 1MW rack power/cooling building block | 设计路线明确，2026 非主流 | <$1B | $2-8B | $20-70B | <1% -> 5%-15% | 35%-60%，早期高溢价 |
| 45°C warm-water loop 与高温液冷 | Schneider/NVIDIA 参考设计已采用 45°C TCS 思路 | $1-4B | $8-22B | $35-120B | 5%-15% -> 30%-60% | 28%-50%，节水/能耗价值大 |
| 生成式/仿真优化冷板、微通道、两相冷板 | 2026 论文与小批量设计优化 | <$0.5B | $1-5B | $8-30B | <2% -> 5%-15% | 45%-70%，IP 和制造良率决定 |
| 单相/两相浸没冷却 | 可用但运维/材料/保修标准未统一 | $0.5-2B | $3-12B | $15-60B | 2%-5% -> 8%-20% | 35%-60%，专用液体和模块高 |
| AI Factory 全生命周期数字孪生 | 设计端快速成熟，运维端早期 | $1-3B | $8-25B | $40-130B | 10%-25% -> 50%-80% 大型项目 | 60%-90%，但实施服务稀释 |
| 机器人/自动巡检/自愈液冷 | 概念到试点 | <$0.3B | $1-3B | $8-25B | <1% -> 5%-12% | 50%-80%，取决于可靠性 |
| 热回收到园区供暖/工业热 | 欧洲较快，美国慢 | <$0.5B | $2-8B | $12-45B | 2%-8% -> 10%-25% | 20%-40%，项目经济性分散 |
| 小型模块化核电 SMR / 长周期清洁电力 | 合同和选址阶段，非 2027 主流 | <$0.2B | $1-5B | $5-25B | 远期选址权，非建设渗透 | 工程利润可高，但审批长 |

### 3.2 在研技术的最可能赢家

800VDC 的赢家不是传统低压配电单品，而是“保护器件+功率转换+母线+安全标准+调试服务”的系统商。NVIDIA 公开称 800VDC 可减少转换阶段、铜用量和线缆体积，并支持未来 AI server；其技术博客把 full-scale production 与 2027 Kyber rack-scale systems 关联。[NVIDIA 800 VDC](https://www.nvidia.com/en-us/data-center/technologies/800-vdc-architecture/)；[NVIDIA 800V technical blog](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)

液冷在研方向里，最先赚钱的是传感、快接、歧管、泵冗余和服务，而不是“冷却概念”。Project Deschutes 5 的 2MW CDU 标准要求 3°C approach temperature difference、500GPM、80PSI、N+1 sealless pump redundancy 等指标，说明 hyperscaler 的核心关注是可靠性和可维护性。[OCP Nidec Project Deschutes 5](https://www.opencompute.org/ai-marketplace/products/781/nidec-project-deschutes-5-cdu)；[Eaton Project Deschutes](https://www.eaton.com/us/en-us/markets/data-centers/data-center-cooling/cdus/what-is-the-open-compute-project-ocp-project-deschutes.html)

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要产能地区 | 代表公司 | 产能特征 |
|---|---|---|---|
| 数据中心土建/EPC | 美国 Sun Belt、Northern Virginia、Texas、Georgia、Arizona、Nevada、Ohio、Indiana、Carolinas；欧洲 Frankfurt/Ireland/Nordics；APAC Malaysia/Johor/Japan/India | Turner、DPR、Holder、HITT、Clayco、Mortenson、Skanska、Jacobs、AECOM、Fluor、Black & Veatch、Burns & McDonnell、Exyte | 本地化强，受劳动力、许可、并网影响大 |
| MEP 专业承包 | 美国为主，区域工会/非工会能力差异大；欧洲和中东靠大型工程商 | Comfort Systems、EMCOR、Quanta/Cupertino/Tri-City、MYR、MasTec、Rosendin、M.C. Dean、Faith、Southland、Bergelectric | 合格项目经理、调试工程师和 prefabrication shop 是核心 |
| 变压器/开关柜/母线槽 | 美国、墨西哥、加拿大、韩国、日本、欧洲、中国 | Eaton、Schneider、ABB、Siemens、GE Vernova/Prolec GE、Hitachi Energy、Mitsubishi、Hyosung、Hyundai Electric、Powell、Hubbell、nVent、Legrand | 长交期，客户预付款和产线排期决定交付 |
| UPS/BESS/电能质量 | 美国、欧洲、中国、韩国；电芯供应仍高度亚洲化 | Vertiv、Eaton、Schneider、Delta、Socomec、Piller、Tesla、Fluence、Powin、Generac | 电芯、功率电子、并网认证和软件控制共同约束 |
| 液冷 CDU/冷板/歧管/快接 | 北美：Vertiv、CoolIT、Motivair、Boyd/Eaton；欧洲：Schneider、STULZ、Danfoss；亚洲：Delta、Nidec、Asia Vital、Foxconn 生态 | Vertiv、Schneider/Motivair、Eaton/Boyd、CoolIT、nVent、Nidec、Delta、Asetek、LiquidStack、Submer、Iceotope、ZutaCore | 客户认证、漏液责任、区域服务和批量一致性是门槛 |
| 预制化模块 | 美国东南/中西部、墨西哥、欧洲、东南亚、中国 | Vertiv、Schneider、Eaton、Compass、Flex、Jabil、Foxconn、Quanta/Wiwynn、PCX、TAS Energy、Exyte | 工厂测试可减少现场返工，但模块运输和安装窗口复杂 |
| 热排放设备 | 美国、欧洲、中国、日本 | Trane、Carrier、Johnson Controls/York、Daikin、Modine、Munters、STULZ、Alfa Laval、Kelvion、Rittal、Danfoss | 冷却塔/干冷器/冷机交期与水资源许可相关 |

### 4.2 供给瓶颈：至少 10 条

1. **变压器和高压开关设备长交期**：Bloomberg/Sightline 口径显示美国大功率变压器交期从 2020 年前 24-30 个月拉长到最长约 5 年；电力设备虽占总成本不到 10%，但单点延迟可使整个项目无法上电。[Tom's Hardware/Bloomberg summary](https://www.tomshardware.com/tech-industry/artificial-intelligence/half-of-planned-us-data-center-builds-have-been-delayed-or-canceled-growth-limited-by-shortages-of-power-infrastructure-and-parts-from-china-the-ai-build-out-flips-the-breakers)
2. **并网和输电容量**：500MW-GW 园区往往需要多个现场变电站，若触发新高压输电或新增发电，周期可到 24-48+ 个月。
3. **液冷客户认证**：冷板、CDU、快接、过滤、冷却液、传感器必须通过服务器 OEM、芯片平台、colo/hyperscaler 多方验证，漏液责任使切换成本极高。
4. **CDU/泵阀/快接/传感器批量一致性**：单个样机不难，批量数千套仍要满足流量、压差、冗余、维护、告警与远程监控。
5. **现场 MEP 劳动力**：电工、管工、焊工、调试工程师、BAS/DCIM 工程师不足；Comfort Systems Q1 2026 backlog $12.45B、同比接近翻倍，反映专业承包商产能紧张。[Comfort Systems Q1 2026](https://investors.comfortsystemsusa.com/news-releases/news-release-details/comfort-systems-usa-reports-first-quarter-2026-results)
6. **预制化工厂产能**：工厂空间、测试台、工程变更管理、运输尺寸限制都会限制模块化交付。
7. **水资源与热排放许可**：液冷减少 IT 侧风量但不消除热排放，冷却塔/干冷器/冷机选型受气候和水权影响。
8. **电芯和功率半导体供应**：BESS、UPS、800VDC、SST 都需要电芯、SiC/GaN、IGBT/MOSFET、控制器和并网认证。
9. **多代芯片并行导致设计变更**：GB200/GB300/Rubin/MI400/TPU/Trainium/Maia 的 rack power、流量、进出水温不同，reference design 和现场工程不断迭代。
10. **融资与客户信用**：neocloud 和 AI lab 需要长约支撑项目融资；一旦租户或 PPA 变更，EPC 和设备订单可能延后。
11. **标准割裂**：OCP、NVIDIA DSX、OCP ORV3/Open Rack Wide、各 hyperscaler 内部规范并行，短期提高工程复杂度。

### 4.3 成本构成与价格传导

| 产品 | 成本构成粗拆 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 土建/壳体 | 钢材/混凝土 25%-35%，机具与分包 20%-30%，人工 25%-35%，设计/许可/管理 10%-15% | 地块、工期、变更单、天气、劳动力 | 成本加成与 GMP，变更单传导快 |
| MEP 安装 | 人工 35%-50%，材料 25%-35%，设备 10%-20%，项目管理/调试 10%-15% | 工程师/工人利用率、返工率、客户变更、现场窗口 | 紧缺时客户接受 premium crew 与加急费 |
| 电力设备 | 铜/铝/钢 25%-40%，磁材/绝缘/半导体 15%-25%，制造人工 10%-20%，测试认证 10%-15% | 交期、容量、电压等级、短路能力、认证 | backlog 和产线槽位定价，长协带价格调整条款 |
| UPS/BESS | 电芯 35%-55%，功率电子 15%-25%，热管理 5%-10%，EMS/软件 5%-15%，集成 10%-20% | 电芯价格、并网能力、软件和保修 | 电芯价格可传导，大客户锁价锁量 |
| CDU/冷板/液冷环路 | 铜/铝/不锈钢 20%-35%，泵/阀/快接 20%-30%，传感/控制 10%-15%，测试 10%-20%，服务 10%-15% | 漏液率、压降、流量、服务 SLA、客户认证 | 认证后强粘性；供不应求时按 rack 或 MW 溢价 |
| 预制模块 | 设备 45%-60%，钢结构/外壳 10%-20%，工厂人工 10%-20%，测试/物流 10%-15% | 工厂利用率、标准化程度、运输半径、现场安装 | 节省工期即价值，客户愿为 certainty 付费 |
| DCIM/数字孪生 | 软件开发 20%-35%，实施集成 30%-45%，数据/传感 10%-20%，支持 10%-15% | 数据接口、模型准确性、运维 ROI | SaaS/订阅+实施费，客户切换成本高 |

## 5. 竞争格局与壁垒：可量化判断

### 5.1 市场结构

| 领域 | 结构判断 | 头部集中度估算 | 变化趋势 |
|---|---|---:|---|
| Critical power + thermal integrated infra | 全球头部集中，项目上由 Vertiv/Schneider/Eaton 三强领跑 | Top 3 约 35%-50%，AI 认证项目更高 | AI 项目向 end-to-end 供应商集中 |
| 变压器/开关柜/母线槽 | 区域垄断+全球巨头 | Top 8 约 45%-65% | 交期使二线厂也有订单，但高端认证仍集中 |
| 液冷 DTC | 仍分散，但 hyperscaler 认证名单变窄 | Top 8 约 50%-70% | 从组件商走向系统商，低质供应商出清 |
| EPC/土建 | 总市场分散，hyperscaler-qualified 集中 | Top 20 在大型 AI 项目中约 40%-60% | 客户更看项目履历和工期 |
| MEP 专业承包 | 地域分散，但上市龙头和区域强商受益 | Top 10 在美国大型项目约 25%-40% | prefab shop 与数据中心履历提高集中度 |
| 预制模块 | 设备商、服务器 ODM、EPC 交叉竞争 | Top 10 约 50%-70% | 标准化越强，制造型公司越占优 |
| DCIM/数字孪生 | 传统 BMS/DCIM 与新 AI 工具并存 | Top 10 约 50%-65% | NVIDIA DSX/Omniverse 生态提升互操作要求 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 具体表现 | 为什么能定价 |
|---|---|---|
| 技术认证 | NVIDIA/GB300/Rubin、OCP、hyperscaler 内部规范、UL/IEC/IEEE | 未认证产品不能进入关键路径，客户不会为低价承担停机/漏液风险 |
| 可靠性数据 | 泵、快接、冷板、CDU、UPS、电力保护需长期 MTBF、维护记录 | 可靠性是可融资资产的一部分，影响租约和 SLA |
| 规模与产能槽位 | 变压器、开关柜、CDU、模块工厂排期稀缺 | 客户买的不是设备，是确定交付窗口 |
| 系统集成 | power、cooling、IT rack、BMS/DCIM、消防、调试需一体化 | 单点最优不等于系统可运行，集成商承担接口风险 |
| 客户锁定 | 大客户标准化后多园区复制 | 一次进入 reference design，后续项目复用率高 |
| 切换成本 | 更换冷板/CDU/母线槽/开关柜会触发重新认证和现场改造 | 短期省价可能换来停机和延期，客户不愿冒险 |
| 服务网络 | AI 园区需要 7x24 服务、备件、远程监控 | 服务半径和响应时间变成产品价格的一部分 |
| 工程人才 | MEP 项目经理、调试工程师、液冷管路团队稀缺 | 好团队可提高交付确定性，客户愿意付 premium |
| 数据闭环 | 数字孪生/预测维护越跑越准 | 数据积累形成软件锁定和持续订阅 |

### 5.3 价值捕获：长期高 ROIC/高毛利层

1. **客户认证后的液冷组件和系统服务**：冷板、CDU、快接、歧管、漏液监测、冷却液管理。原因是可靠性、认证和服务锁定强，且每一代 GPU/ASIC 都要重做热设计，带来持续升级。
2. **高端配电与 800VDC 保护/功率转换**：开关柜、母线槽、DC breaker、整流、SST、rack-level power shelf。原因是安全标准、故障责任和长期交期带来强定价。
3. **预制化 power/cooling block**：标准化模块的毛利未必最高，但周转快、返工低、可复制，优秀厂商 ROIC 可能显著高于传统 EPC。
4. **DCIM/数字孪生/预测维护**：毛利率最高，但需要先拿到设备和运行数据入口。NVIDIA DSX、Schneider ETAP/AVEVA、Vertiv Unify/Next Predict、Siemens/Cadence/Jacobs 等会围绕“token per MW”形成新软件层。
5. **纯土建壳体**：需求大但长期毛利较低，除非绑定已获电力、稀缺地块或自有开发资产。

## 6. 2026 关键变化：3 个行业拐点与最可能放量方向

### 拐点 1：液冷从“高端可选”变“高密默认”

GB300/NVL72、TPU、Trainium、Maia、MI350/MI400 把 rack density 推上 50kW-100kW+。Vertiv 2026 MegaMod HDX 支持 50kW 到 >100kW/rack、最高 10MW 模块；Schneider/Motivair 发布 2.5MW CDU，CDU portfolio 覆盖 105kW 到 2.5MW，并可扩展到 10MW+。[Vertiv MegaMod HDX](https://investors.vertiv.com/news/news-details/2026/Vertiv-Introduces-New-Modular-Liquid-Cooling-Infrastructure-Solution-to-Support-High-Density-Compute-Requirements-in-North-America-and-EMEA/default.aspx)；[Motivair by Schneider 2.5MW CDU](https://www.nasdaq.com/press-release/motivair-schneider-electric-announces-new-cdu-capability-scale-10mw-and-beyond-next)

最可能放量：CDU、冷板、快接、歧管、漏液监测、RDHx、heat rejection。

### 拐点 2：电力设备订单领先算力交付

Microsoft 2026Q3 call 称 2026 calendar year CapEx 约 $190B，仍至少到 2026 年受容量约束；Meta 10-Q 指引 2026 CapEx $125B-$145B；Alphabet 2026Q1 PPE purchases $35.7B、TTM $109.9B；Amazon 2026Q1 称过去 12 个月 landed 2.1M+ AI chips，并宣布 2026 起部署 1M+ NVIDIA GPUs。[Microsoft FY26Q3](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3)；[Meta 10-Q](https://www.sec.gov/Archives/edgar/data/1326801/000162828026028526/meta-20260331.htm)；[Alphabet Q1 2026](https://s206.q4cdn.com/479360582/files/doc_financials/2026/q1/2026q1-alphabet-earnings-release.pdf)；[Amazon Q1 2026](https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q1/earnings-result/AMZN-Q1-2026-Earnings-Release.pdf)

最可能放量：变压器、开关柜、母线槽、UPS、BESS、微电网、燃气发电、变电站 EPC。

### 拐点 3：预制化从“加速工具”变“投产前提”

Vertiv 2026 年宣布美洲四个新增/扩建制造设施，南卡相关 infrastructure solution 区域产能完全爬坡后预计提升约 7x；其 SmartRun 预制 white-space solution 将高密母线、液冷管路、网络和围护整合，现场部署时间最多快 85%。Schneider 与 Compass 的 EcoStruxure Pod 把 power、cooling、technical water loop 和 cabling 放入预制白空间模块，减少现场工人和返工。[Vertiv capacity expansion](https://investors.vertiv.com/news/news-details/2026/Vertiv-Announces-Expansion-of-Manufacturing-Capacity-Spanning-Infrastructure-Solutions-Power-and-Rack-Systems-to-Meet-Rising-Demand/default.aspx)；[Schneider/Compass EcoStruxure Pod](https://www.se.com/us/en/about-us/newsroom/news/press-releases/compass-datacenters-and-schneider-electric-announce-prefabricated-white-space-module-to-accelerate-data-center-delivery-timelines-68af2d56cbd7ebbcda05501d/)

最可能放量：e-house、integrated power module、AI pod、rack manifold kit、factory acceptance test、modular commissioning。

## 7. 2027 关键变化：3 个行业拐点与最可能放量方向

### 拐点 1：800VDC 商业化起步

NVIDIA 称 800VDC 降低 current、copper use、cable bulk 和 conversion stages；技术博客把 full-scale production 与 2027 Kyber rack-scale systems 相关联，并称端到端效率可提升最高 5%、TCO 最高降低 30%、维护成本最高降低 70%。ABB 白皮书也把 800VDC 与 1MW server rack 联系起来。[NVIDIA 800 VDC](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)；[ABB 800VDC white paper](https://resources.news.e.abb.com/attachments/published/129788/en-US/3515A12A5C51/ABB_800_VDC_NVIDIA_white_paper.pdf)

最可能放量：DC breaker、power rack、high-voltage busway、SiC/GaN、energy buffer、SST 试点。

### 拐点 2：Rubin/MI400/HBM4 把液冷和热排放推到设施级

2026 的 DTC 更多是 rack/pod 级放量，2027 随 Rubin、MI400、Trainium3/4、TPU8、Maia 后续版本进入更高密度，设施侧会从“给 rack 上水”升级为“IT、二次侧、冷机/干冷器、热回收、功率调度一体化设计”。45°C TCS loop、warm-water cooling、dry cooler 和 heat reuse 价值上升。

最可能放量：高温 CDU、dry cooler、板式换热器、泵站、热回收、液冷运维服务。

### 拐点 3：AI Factory 园区化和现场能源成为主流融资变量

OCP Open DC for AI 把 Energy and Grid Solutions、BESS、microgrids 和 power estimation methodology 列为核心优先事项；Vertiv 与 Generate Capital 的 BYOP&C 模式强调客户可以先部署现场电力，再保留切换到公用电网的灵活性。[OCP Open DC for AI](https://www.opencompute.org/projects/open-dc-for-ai)；[Vertiv/Generate BYOP&C](https://investors.vertiv.com/news/news-details/2026/Vertiv-and-Generate-Capital-Collaborate-to-Accelerate-Data-Center-Capacity-with-Complete-Power-and-Cooling-Infrastructure/default.aspx)

最可能放量：BESS、燃气轮机、燃料电池、PPA、微电网 EMS、现场变电站 EPC、需求响应软件。

## 8. 头部公司清单：按产品/技术全景

### 8.1 土建、EPC、开发商、REIT

| 细分 | 公司 |
|---|---|
| 数据中心开发/REIT/colo | Digital Realty、Equinix、QTS、Vantage、DataBank、Aligned、Stack、NTT Global Data Centers、Switch、Compass Datacenters、Crusoe、CoreWeave 自建/租赁生态、Oracle/Stargate 生态、xAI/Colossus 生态 |
| 总包/EPC/设计 | Turner、DPR Construction、Holder、HITT、Clayco、Mortenson、Skanska、AECOM、Jacobs、Fluor、Black & Veatch、Burns & McDonnell、Kiewit、Bechtel、Exyte、Winthrop、Mercury、Mace |
| 场平/土方/站点基础 | Sterling Infrastructure、MasTec、Kiewit、Granite、Ames、Flatiron、区域土方承包商 |

### 8.2 MEP、机电安装、调试

| 细分 | 公司 |
|---|---|
| 机械/电气/管道综合 | Comfort Systems USA、EMCOR、Southland Industries、TDIndustries、ACCO、J.F. Ahern、McKenney's、Murphy Company |
| 电气承包/变电站/低压高密安装 | Quanta Services、Cupertino Electric、Tri-City、Rosendin、M.C. Dean、Faith Technologies、MYR Group、MasTec、Bergelectric、IES Holdings、Encore Electric、Power Design |
| 调试/运维/设施服务 | Vertiv Services、Schneider Field Services、Eaton Services、EMCOR、CBRE Data Center Solutions、JLL Critical Environments、BGIS、Johnson Controls、Honeywell |

### 8.3 电力设备、UPS、母线、BESS、现场能源

| 细分 | 公司 |
|---|---|
| 变压器/开关柜/中低压配电 | Eaton、Schneider Electric、ABB、Siemens、Siemens Energy、GE Vernova/Prolec GE、Hitachi Energy、Mitsubishi Electric、Toshiba、Hyosung、Hyundai Electric、Virginia Transformer、SPX Transformer、Powell Industries、Hubbell |
| 母线槽/PDU/RPP/rack power | Eaton、Schneider、Vertiv、nVent、Legrand/Raritan、ABB、Siemens、Delta、Panduit、Starline、Server Technology、Socomec |
| UPS/电能质量 | Vertiv、Eaton、Schneider、Delta、Socomec、Piller、Kohler Uninterruptible Power、Riello、Huawei Digital Power |
| BESS/储能/微电网 | Tesla Megapack、Fluence、Powin、Wartsila、Sungrow、CATL、BYD、LG Energy Solution、Samsung SDI、Generac、Stem、Hitachi Energy、Schneider、Eaton |
| 发电机/燃气轮机/fuel cell | Caterpillar、Cummins、Rolls-Royce mtu、Kohler、Generac、GE Vernova、Solar Turbines/Caterpillar、Siemens Energy、Mitsubishi Power、Bloom Energy、Plug Power |
| 800VDC/电力电子/保护 | NVIDIA ecosystem、ABB、Eaton、Schneider、Vertiv、GE Vernova、Hitachi Energy、Siemens、Delta、Flex、Lite-On、Navitas、Infineon、TI、STMicro、onsemi、Renesas、ROHM、MPS、AOS |

### 8.4 冷却、液冷、热排放

| 细分 | 公司 |
|---|---|
| DTC 液冷系统/CDU | Vertiv、Schneider/Motivair、Eaton/Boyd、CoolIT Systems、nVent、Nidec、Delta、Asetek、Asia Vital Components、Foxconn thermal ecosystem、Lenovo Neptune、HPE Cray/Slingshot ecosystem |
| 冷板/歧管/快接/泵阀 | Boyd/Eaton、CoolIT、Asetek、Danfoss、Parker、CPC/Dover、Victaulic、nVent、Delta、Nidec、Modine、Alfa Laval、Kelvion |
| 浸没/两相/特种冷却 | LiquidStack、Submer、Iceotope、ZutaCore、GRC、Shell/3M 替代冷却液生态、Solvay/Chemours 等流体供应链 |
| 冷机/冷却塔/干冷器/CRAH/CRAC | Vertiv、Schneider、Johnson Controls/York、Trane Technologies、Carrier、Daikin、STULZ、Munters、Modine、Airedale、Rittal、Baltimore Aircoil、SPX Cooling、Alfa Laval、Kelvion |
| heat reuse/warm water | Danfoss、Alfa Laval、Kelvion、Johnson Controls、Trane、Carrier、Schneider、Vertiv、区域供热公司 |

### 8.5 预制化、rack/pod、AI Factory 参考设计

| 细分 | 公司 |
|---|---|
| 预制 power/cooling module | Vertiv、Schneider Electric、Eaton、ABB、Siemens、GE Vernova、PCX、TAS Energy、Flex、Jabil、Foxconn、Exyte、Compass Datacenters |
| white-space pod / AI pod | Schneider/Compass EcoStruxure Pod、Vertiv SmartRun/MegaMod HDX、nVent rack-roll solution、Flex AI Infrastructure Platform、Dell/SMCI/HPE 服务器 rack 生态 |
| 服务器 ODM 与 rack integration | Foxconn、Quanta、Wiwynn、Inventec、Jabil、Flex、Supermicro、Dell、HPE、Lenovo、xFusion |
| 开放标准 | OCP Open DC for AI、OCP Cooling Environments、Project Deschutes、OCP ORV3、Open Rack Wide、NVIDIA MGX/GB300/Vera Rubin DSX |

### 8.6 软件、数字孪生、DCIM、AI 运维

| 细分 | 公司 |
|---|---|
| AI Factory 数字孪生 | NVIDIA Omniverse DSX、Schneider ETAP/AVEVA、Cadence Reality Data Center Digital Twin、Dassault CATIA/3DEXPERIENCE、Siemens Xcelerator、PTC Windchill、Jacobs Data Center Digital Twin、Procore |
| DCIM/BMS/运维 | Schneider EcoStruxure IT、Vertiv Unify/Next Predict、Siemens Desigo/Building X、Johnson Controls OpenBlue、Honeywell Forge、Carrier Abound、Nlyte、Sunbird、EkkoSense、Vigilent、Phaidra |
| 施工与项目管理 | Procore、Autodesk Construction Cloud、Bentley Systems、Trimble、Oracle Primavera、Hexagon、Jacobs/AVEVA 工程数据链 |

## 9. 投资排序：确定性、弹性、利润质量

| 排名 | 方向 | 确定性 | 弹性 | 利润质量 | 关键观察指标 |
|---:|---|---|---|---|---|
| 1 | 电力设备：变压器/开关柜/母线/UPS | 极高 | 高 | 高 | backlog、book-to-bill、交期、扩产、price-cost |
| 2 | 液冷 DTC 系统与核心组件 | 高 | 极高 | 高 | NVIDIA/OCP 认证、MW deployed、漏液率、服务 attach |
| 3 | MEP 专业承包与调试 | 高 | 高 | 中高 | backlog、gross margin、labor availability、prefab capacity |
| 4 | 预制化 power/cooling/white-space module | 高 | 极高 | 中高到高 | 工厂利用率、标准化比例、现场工期缩短 |
| 5 | BESS/现场能源/microgrid | 中高 | 极高 | 中高 | PPA、燃气接入、并网规则、BESS attach |
| 6 | 数字孪生/DCIM/预测维护 | 中高 | 高 | 极高 | DSX/ETAP/AVEVA/Vertiv adoption、运行数据闭环 |
| 7 | 纯土建壳体 | 高 | 中 | 中低 | 已获电力地块、预租率、建设成本/MW |

## 10. 风险与反证指标

1. Hyperscaler 下修 2026/2027 CapEx 或把 AI 建设从自建转向租赁，供应商订单确认慢于预期。
2. 变压器、开关柜、BESS 或冷却关键部件交期继续拉长，导致 2026 公告项目延后到 2027-2028。
3. GPU/HBM/CoWoS 交付不及预期，导致高密 rack 无法同步进入机房。
4. 液冷出现大规模漏液/保修事件，客户推迟 DTC attach 或增加验收周期。
5. 美国州/地方对水、电价、噪音、柴油发电和土地使用的监管趋严。
6. NeoCloud 客户融资失败或 GPU 租金下行，影响租赁合同和设备预付款。
7. 800VDC 标准推进慢于预期，2027 相关产品只停留在示范。

## 11. 资料来源精选

| 主题 | 来源 |
|---|---|
| 美国数据中心需求、预租率、并网周期 | [CBRE 2026 Data Centers](https://www.cbre.com/insights/books/us-real-estate-market-outlook-2026/data-centers) |
| 全球建设成本、AI fit-out 成本、100GW 供给 | [JLL 2026 Global Data Center Outlook](https://www.jll.com/en-ca/insights/market-outlook/data-center-outlook) |
| $7T 建设机会、预制化、液冷标准化 | [McKinsey $7T race](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-7-trillion-dollar-data-center-build-out-how-industrials-can-capture-their-share) |
| 电力与冷却市场规模、DTC/RDHx/immersion | [McKinsey power/cooling PDF](https://www.mckinsey.com/~/media/mckinsey/industries/advanced%20electronics/our%20insights/beyond%20compute%20infrastructure%20that%20powers%20and%20cools%20ai%20data%20centers/beyond-compute-infrastructure-that-powers-and-cools-ai-data-centers.pdf) |
| NVIDIA DSX、Vera Rubin reference design | [NVIDIA DSX 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-Vera-Rubin-DSX-AI-Factory-Reference-Design-and-Omniverse-DSX-Digital-Twin-Blueprint-With-Broad-Industry-Support/default.aspx) |
| NVIDIA 800VDC 技术路线 | [NVIDIA 800 VDC page](https://www.nvidia.com/en-us/data-center/technologies/800-vdc-architecture/)；[NVIDIA 800V blog](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) |
| OCP Open DC for AI、液冷标准 | [OCP Open DC for AI](https://www.opencompute.org/projects/open-dc-for-ai)；[OCP Cooling Environments](https://www.opencompute.org/community/cooling-environments) |
| Project Deschutes 2MW CDU | [OCP Nidec Deschutes 5 CDU](https://www.opencompute.org/ai-marketplace/products/781/nidec-project-deschutes-5-cdu)；[Eaton Deschutes](https://www.eaton.com/us/en-us/markets/data-centers/data-center-cooling/cdus/what-is-the-open-compute-project-ocp-project-deschutes.html) |
| Vertiv 订单、预制化、液冷模块、产能扩张 | [Vertiv Q4 2025](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/)；[Vertiv Q1 2026](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx)；[MegaMod HDX](https://investors.vertiv.com/news/news-details/2026/Vertiv-Introduces-New-Modular-Liquid-Cooling-Infrastructure-Solution-to-Support-High-Density-Compute-Requirements-in-North-America-and-EMEA/default.aspx)；[capacity expansion](https://investors.vertiv.com/news/news-details/2026/Vertiv-Announces-Expansion-of-Manufacturing-Capacity-Spanning-Infrastructure-Solutions-Power-and-Rack-Systems-to-Meet-Rising-Demand/default.aspx) |
| Eaton 订单、Boyd Thermal、NVIDIA 协作 | [Eaton Q1 2026](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html)；[Eaton Beam Rubin DSX](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-collaborates-with-nvidia-to-unveil-its-beam-rubin-dsx-platform.html) |
| Schneider 订单、NVIDIA reference design、预制化 pod、CDU | [Schneider Q1 2026](https://www.se.com/ww/en/assets/pdf/release-q1-revenues-2026)；[Schneider/NVIDIA GTC 2026](https://www.se.com/us/en/about-us/newsroom/news/press-releases/Schneider-Electric-teams-with-NVIDIA-to-develop-validated-blueprints-to-design-simulate-build-operate-and-maintain-gigawattscale-AI-Factories-69b82f61aa1027e04205d273/)；[Compass/Schneider Pod](https://www.se.com/us/en/about-us/newsroom/news/press-releases/compass-datacenters-and-schneider-electric-announce-prefabricated-white-space-module-to-accelerate-data-center-delivery-timelines-68af2d56cbd7ebbcda05501d/)；[Motivair 2.5MW CDU](https://www.nasdaq.com/press-release/motivair-schneider-electric-announces-new-cdu-capability-scale-10mw-and-beyond-next) |
| nVent 2026 液冷/高密 PDU 产品 | [nVent next-generation liquid cooling and power](https://raychem.nvent.com/en-ve/data-solutions/next-generation-liquid-cooling-and-power-portfolios-coming-2026) |
| MEP 需求与 backlog | [Comfort Systems Q1 2026](https://investors.comfortsystemsusa.com/news-releases/news-release-details/comfort-systems-usa-reports-first-quarter-2026-results)；[EMCOR Q1 2026](https://emcorgroup.com/investor-relations/press-releases/2026-news/emcor-group-inc-reports-first-quarter-2026-results)；[Quanta FY2025/Q4 release](https://investors.quantaservices.com/_assets/_c33e63906c5e56bc75e345eb419a7a70/quantaservices/news/2026-02-19_QUANTA_SERVICES_REPORTS_FOURTH_QUARTER_AND_FULL_390.pdf) |
| Hyperscaler CapEx 和芯片/容量信号 | [Microsoft FY26Q3 call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3)；[Meta 2026Q1 10-Q](https://www.sec.gov/Archives/edgar/data/1326801/000162828026028526/meta-20260331.htm)；[Amazon Q1 2026](https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q1/earnings-result/AMZN-Q1-2026-Earnings-Release.pdf)；[Alphabet Q1 2026](https://s206.q4cdn.com/479360582/files/doc_financials/2026/q1/2026q1-alphabet-earnings-release.pdf) |
| 800VDC 学术/技术验证 | [arXiv: SST-driven 800 VDC architecture](https://arxiv.org/abs/2601.16502)；[arXiv: Generative design for DTC liquid cooling](https://arxiv.org/abs/2604.10941) |

# 行业调研：【数据中心直液冷系统】

截至：2026-05-08  
研究口径：本文把“数据中心直液冷系统”定义为以 direct-to-chip / cold plate 为核心的单相或两相直接液冷系统，覆盖冷板、服务器内液冷 loop、快接头、歧管、CDU、泵阀过滤、漏液检测、冷却液、水质与控制软件。为避免混淆，市场规模分为两个口径：  
1. 严格设备口径：冷板、CDU、歧管、快接头、液冷 loop、控制和相关部件的制造商收入。Dell'Oro 2026 年 1 月报告给出的公开锚是 2025 年接近 30 亿美元、2029 年约 70 亿美元。本文在 AI 极度乐观情形下允许 2026-2028 显著高于该保守设备口径。  
2. 热管理项目口径：把直液冷相关的 TCS 管路、干冷器、冷水机组、热交换器、安装调试和现场服务也纳入。这个口径会远大于设备收入，和 AI 园区机电订单更接近。

## 0. 核心结论

直液冷不是 2026 年 AI 数据中心的“可选升级”，而是 GB300、Rubin、MI400、Maia 200、Trainium3、TPU Ironwood/TPU8 等高密 AI 集群能否上电的交付前置条件。2025 年 NVIDIA GB200/GB300 NVL72 把单机柜功率推到 130-142kW，2026 年 Vera Rubin NVL72 继续走 100% 液冷、45°C 高温供液、无风扇/无软管/无线缆化的机柜内设计。TrendForce 已把 AI 数据中心液冷渗透率从 2024 年 14% 到 2025 年 33%作为公开锚，2026 年的核心变化是从“试点/少数超算”进入“NVL72/AI Factory 标准交付”。

最强投资判断：

| 判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 全球直液冷严格设备市场 | $4.0-5.5B | $5.5-8.0B | $8.0-12.0B |
| 2027 全球直液冷严格设备市场 | $5.5-8.0B | $8.5-13.0B | $14.0-22.0B |
| 2028 全球直液冷严格设备市场 | $7.0-10.5B | $12.0-19.0B | $22.0-35.0B |
| 2026 全球相关热管理项目订单 | $18-30B | $30-48B | $48-75B |
| 2027 全球相关热管理项目订单 | $28-48B | $50-85B | $85-140B |
| AI 加速器高密机柜液冷 attach rate | 2026: 50-60%；2027: 65-75% | 2026: 65-75%；2027: 80-90% | 2026: 80-88%；2027: 90-97% |
| 主流技术路线 | 单相 direct-to-chip + L2A/L2L CDU | L2L 加速、45°C warm-water、干冷/free cooling | Rubin/MI400/TPU8 前置，2kW+芯片推动先进冷板和两相直冷早放量 |

2026 最确定放量的产品是：GPU/CPU/NVSwitch 冷板、机柜歧管与 blind-mate QD、1-2.5MW in-row/sidecar CDU、L2A 过渡型 CDU、漏液检测与控制系统、PG25/去离子水水质服务。2027 更可能放量的是：L2L warm-water 架构、液冷母排、UQD08/OCP 标准件、高温干冷器、两相 direct-to-chip 试点、AI factory 级冷却数字孪生与自动控制。

从价值捕获看，长期高毛利/高 ROIC 最可能在三层：芯片级定制冷板与热仿真设计、通过 NVIDIA/OCP/hyperscaler 认证的快接头与歧管、MW 级 CDU 控制/冗余/服务生态。整柜集成和传统冷水机组也很大，但更偏项目制造和施工能力，毛利弹性弱于“认证接口件+定制热设计”。

## 1. AI 芯片路线图对直液冷的拉动

项目内已有芯片报告显示，2026-2027 初出货/价值权重最高的平台包括 NVIDIA GB300/B300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA GB200、Huawei Ascend 910C/950、Cambricon MLU 590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200、Alibaba Zhenwu、AMD MI400。它们共同指向一个结论：冷却路径从“服务器级散热”升级为“芯片-托盘-机柜-数据大厅协同设计”。

### 1.1 2026-2027 关键 AI 芯片冷却背景

| 芯片/平台 | 2026-2027 出货背景 | 热设计含义 | 直液冷成熟/放量节奏 |
|---|---|---|---|
| NVIDIA GB300/B300 Blackwell Ultra | 项目内判断为 2026 主力；Schneider/NVIDIA GB300 参考设计给出最高 142kW/rack；Supermicro GB300 rack 数据表显示总功率约 132kW | 全液冷机柜成为基准；GPU、Grace CPU、NVSwitch 都需要冷板/液冷 loop | 已成熟，2026 Q2-Q4 大规模放量 |
| NVIDIA GB200/B200 | 2025-2026 存量和新增交付 | GB200 NVL72 已建立第一代大规模直接液冷交付经验 | 成熟，2026 主要是交付爬坡和现场运维学习曲线 |
| NVIDIA Vera Rubin NVL72 | NVIDIA 称 2026 H2 出货；官方技术博客称 45°C 高温供液可释放最多 10% 同等电力预算给更多 rack | 100% liquid-cooled，第三代 MGX rack，内部 tray manifold、UQD08 manifold、liquid cooled busbar 最高 5,000A | 2026 H2 首批，2027 主力；带动 UQD08、液冷母排、45°C warm-water 标准化 |
| AMD MI350 | 2026 AMD 最确定的放量产品，企业/云混合 | PCIe/OAM/UBB 形态并存，液冷 attach rate 低于 NVL72 但高密部署需要 DLC | 2026 放量，风液混合和 direct-to-chip 并行 |
| AMD MI400/Helios | 项目内判断 2026 H2 首批，2027 可能成为 AMD 主力 | 72 GPU rack、HBM4、高功耗 rack-scale；对 CDU、L2L、OCP/UALink 生态要求高 | 2026 H2 验证，2027 放量 |
| AWS Trainium2/3 | Rainier 大规模部署，Trainium3 UltraServer 144 芯片 scale-up | AWS 自有数据中心可深度定制，液冷/混合冷却会随机柜密度提高 | Trainium2 2026 大规模，Trainium3 2026 H2-2027 推升液冷比例 |
| Google TPU Ironwood/TPU8 | Ironwood 2026 主力，TPU8 训练/推理分化 | Google 新数据中心液冷 ready；自有 pod 和设施协同 | 2026 大规模混合液冷，2027 L2L 与 warm-water 比例提高 |
| Microsoft Maia 200 | 官方称 2026 1 月推出，TSMC 3nm、216GB HBM3E、7TB/s，第二代 closed-loop liquid cooling HEU | Hyperscaler 自研 ASIC 明确把闭环液冷作为平台复杂系统之一 | 2026 Azure 内部导入，2027 扩大 |
| Meta MTIA/Broadcom XPU | 2026-2027 四代迭代，>1GW 初期路线 | OCP 机架、推理密度提升，风液混合向 DLC 过渡 | 2026 推理集群局部放量，2027 多 GW 需求打开 |
| Huawei/Cambricon/Alibaba/Baidu 国产 AI | 中国国产替代数量大，单芯片功耗/系统效率差异大 | 早期风液混合，超节点/万卡集群需要 direct-to-chip 和集中 CDU | 2026 高密集群逐步导入，2027 国产液冷生态扩张 |

### 1.2 技术路线成熟时间和放量时间

| 技术路线 | 2026 状态 | 2027 状态 | 基准放量 | 乐观放量 | 极度超预期放量 |
|---|---|---|---|---|---|
| 单相 direct-to-chip cold plate | 主流量产，NVIDIA/AMD/ASIC 都依赖 | 继续主导，热流密度要求更高 | 2026 全年 | 已发生，2026 H2 加速 | 2026 Q2 起供不应求，冷板厂商获得溢价 |
| L2A CDU/sidecar CDU | 存量数据中心改造的过渡主线 | 新建 AI hall 中占比下降 | 2026-2027 | 2026 Q3 大批量 | 若旧机房抢 GB300，2026 下半年爆单 |
| L2L in-row/sidecar CDU | 新建 AI hall 主线之一 | 2027 起取代 L2A 成为新增主流 | 2027 H1 | 2026 H2 | 2026 Q3 进入超大 AI factory 标准模块 |
| 45°C warm-water / dry cooler | GB300/Rubin 参考设计验证 | 大规模复制，降低机械制冷依赖 | 2027 | 2026 H2 | 2026 就成为 hyperscaler 新建项目默认要求 |
| UQD08/OCP blind-mate 快接 | 随 GB300/Rubin 扩大 | 标准化、认证件供给吃紧 | 2026 H2 | 2026 Q2-Q3 | 2026 成为短缺最强环节之一 |
| 液冷母排/机柜内 power-cooling 协同 | Rubin MGX 明确方向 | 2027 高端机柜扩散 | 2027 H1 | 2026 H2 | Rubin 前置导致 2026 H2 小规模抢单 |
| 两相 direct-to-chip | 早期试点，ZutaCore 等 waterless 方案验证 GB200 | 2kW+芯片下试点扩大 | 2028 | 2027 H2 | 2027 H1 在少数 hyperscaler 批量部署 |
| 浸没式冷却 | 选择性应用，ASIC/边缘/HPC 小规模 | 仍受维护、供应链和标准限制 | 2028 后 | 2027 局部 | 除特殊客户外难以在 NVL72 主流化 |
| 生成式/AI 优化冷板微通道 | 2026 论文和工程试验；GB200 热点优化有 >5°C 平均降温和 >35°C 峰值降温的研究结果 | 进入新一代冷板设计工具链 | 2027-2028 | 2027 | 2026 H2 被头部厂导入定制设计 |

### 1.3 2026 最可能的技术路径

2026 的主线不是浸没式，也不是两相液冷，而是“单相 direct-to-chip + L2A/L2L CDU + warm-water ready”。原因有五个：

| 证据 | 含义 |
|---|---|
| Dell'Oro 称单相直液冷已经巩固为 AI clusters 的 dominant architecture，并预计大部分部署到本十年末仍以单相为主 | 主流客户优先选择可验证、可维护、供应链可放大的技术 |
| TrendForce 称 2025 AI 数据中心液冷渗透率从 14%升到 33%，GB200/GB300 NVL72 TDP 为 130-140kW/rack，L2A 是短期过渡主流，L2L 从 2027 快速增长 | 2026 是从 L2A 过渡到 L2L 的斜坡期 |
| NVIDIA Vera Rubin 技术博客明确 45°C max inlet、PG25/去离子水可 10 年闭环维护、MGX rack 可 100% liquid-cooled | 生态将围绕高温水、标准歧管、UQD 和液冷母排展开 |
| Schneider/NVIDIA GB300 参考设计直接面向最高 142kW/rack，数据大厅可容纳三组 GB300 cluster、1,152 GPUs，使用 liquid-to-liquid CDU 和高温 chiller | 直液冷开始进入标准 reference design，而不是现场定制项目 |
| CoolIT、Motivair、Eaton/Boyd、Vertiv、nVent、Modine 都在 2025-2026 推出 800kW-2.5MW 级 CDU 或扩产 | 供给侧已经围绕 GB300/Rubin 的功率等级重新布局 |

## 2. 已经开始放量的关键产品

下面表格的市场规模为严格设备口径，单位为美元收入/订单。3 个月指 2026 年 5-8 月新增订单或交付 run-rate，1 年指 2027 年 5 月前后 LTM，2 年指 2028 年 5 月前后 LTM。渗透率以 AI 加速器高密机柜液冷 attach rate 或相关液冷系统内部占比衡量。

### 2.1 放量产品市场规模和渗透率

| 产品 | 当前放量证据 | 未来 3 个月 | 1 年 | 2 年 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| GPU/CPU/NVSwitch 单相冷板与 server loop | CoolIT 称月产 10,000s server coldplate loops；Boyd/CoolIT 均称冷板已冷却超过 500 万 GPU/CPU/AI accelerator | 基准 $0.45-0.75B；乐观 $0.70-1.10B；极度 $1.10-1.80B | 基准 $2.0-3.2B；乐观 $3.2-5.0B；极度 $5.5-8.5B | 基准 $3.2-5.0B；乐观 $5.5-9.0B；极度 $10-16B | AI 高密机柜冷板 attach rate：2026 55-80%，2027 70-95%，2028 80-98% |
| CDU，含 in-row、sidecar、in-rack，L2L/L2A | Motivair MCDU-70 2.5MW；CoolIT CHx2000 >2MW；Eaton/Boyd ROL4000 2MW；nVent CDU800；Airedale 400kW-2MW+ | 基准 $0.40-0.70B；乐观 $0.75-1.20B；极度 $1.20-2.00B | 基准 $1.8-3.0B；乐观 $3.0-5.2B；极度 $5.5-9.0B | 基准 $2.8-5.0B；乐观 $5.5-10B；极度 $11-18B | L2A 2026 55-65%短期占优；L2L 2027 新建 AI hall 升至 45-60%；2028 L2L 60-75% |
| 机柜歧管、UQD、blind-mate QD、软管套件 | TrendForce 点名 CPC/Parker/Danfoss/Stäubli 在 GB200 QD 早期有优势；NVIDIA Rubin 提到 rack UQD08 manifolds | 基准 $0.25-0.45B；乐观 $0.45-0.80B；极度 $0.80-1.40B | 基准 $1.1-1.9B；乐观 $2.0-3.5B；极度 $3.8-6.5B | 基准 $1.8-3.2B；乐观 $3.5-6.5B；极度 $7-12B | 每个液冷 rack 必配，认证件渗透率接近 100%；UQD08 随 Rubin 2027 提升 |
| 漏液检测、过滤、补液、水质监测、控制软件 | Eaton/Boyd CDU 强调自动补液、0.2 微米过滤和 leak detection；Schneider/NVIDIA controls reference design 接入 Mission Control | 基准 $0.08-0.16B；乐观 $0.16-0.30B；极度 $0.30-0.55B | 基准 $0.4-0.8B；乐观 $0.8-1.5B；极度 $1.6-2.8B | 基准 $0.8-1.5B；乐观 $1.6-3.0B；极度 $3.2-5.5B | 从硬件附属变成 uptime 必配，2026 attach 40-60%，2028 70-90% |
| RDHx / 液冷门 / liquid-to-air sidecar | Motivair ChilledDoor 支持 75kW；nVent RDHX PRO 到 78kW；L2A 适合无 facility water 的改造 | 基准 $0.15-0.30B；乐观 $0.30-0.55B；极度 $0.55-0.90B | 基准 $0.7-1.3B；乐观 $1.3-2.3B；极度 $2.5-4.0B | 基准 $1.0-1.8B；乐观 $2.0-3.8B；极度 $4.0-6.5B | 2026 改造项目占优；2027 后新建项目 L2L 占比上升，RDHx 转为补热/混合冷却 |
| 冷却液、PG25、去离子水、水处理与服务 | NVIDIA 称 PG25/去离子水在闭环中可 10 年低维护；Ecolab 收购 CoolIT意图做 fluid management + cooling platform | 基准 $0.05-0.12B；乐观 $0.12-0.25B；极度 $0.25-0.45B | 基准 $0.3-0.6B；乐观 $0.6-1.2B；极度 $1.2-2.2B | 基准 $0.6-1.2B；乐观 $1.3-2.8B；极度 $3.0-5.5B | 设备一次性，化学/监控/服务有 recurring 属性；2027 后高毛利属性增强 |

### 2.2 已放量产品增长和利润率预测

| 产品 | 2026-2028 CAGR 基准 | CAGR 乐观 | CAGR 极度超预期 | 当前毛利率基准 | 乐观 | 极度超预期 |
|---|---:|---:|---:|---:|---:|---:|
| 单相冷板/server loop | 35-55% | 60-85% | 90-130% | 25-35% | 35-45% | 45-55% |
| CDU | 35-55% | 60-90% | 100-150% | 25-35% | 35-45% | 45-55% |
| QD/歧管/软管 | 40-65% | 70-105% | 110-170% | 35-50% | 45-58% | 55-68% |
| 控制/漏液/水质 | 50-80% | 85-130% | 140-220% | 40-55% | 50-65% | 60-75% |
| RDHx/L2A | 25-40% | 45-70% | 75-110% | 20-30% | 30-40% | 40-50% |
| 冷却液/服务 | 50-85% | 90-140% | 150-250% | 45-60% | 55-70% | 65-80% |

利润率锚点：Eaton 收购 Boyd Thermal 的材料披露 Boyd Thermal 2026E 销售额约 17 亿美元、调整后 EBITDA 约 25%；Ecolab 称 CoolIT 是 high-growth、high-margin，未来 12 个月销售额约 5.5 亿美元，交易估值约 29x NTM EBITDA；Vertiv 2026 全年 adjusted operating margin 指引升至 22.8-23.8%。这些都支持“头部液冷设备/接口件毛利率显著高于传统机电制造”的判断。

## 3. 在研和快速增长的关键产品

### 3.1 在研/早期商业技术

| 技术/产品 | 当前阶段 | 技术价值 | 未来 3 个月市场 | 1 年市场 | 2 年市场 | 放量判断 |
|---|---|---|---:|---:|---:|---|
| 两相 direct-to-chip / waterless cold plate | ZutaCore 等已宣称支持 GB200；多数仍是试点或早期商业 | 降低水风险，应对 2kW+芯片热流密度 | 基准 <$50M；乐观 $50-120M；极度 $150-300M | 基准 $0.15-0.35B；乐观 $0.4-0.9B；极度 $1.0-2.0B | 基准 $0.5-1.2B；乐观 $1.5-3.5B；极度 $4-8B | 基准 2028；乐观 2027 H2；极度 2027 H1 |
| 4kW+ 高热流冷板 | CoolIT 公开 4,000W TTV/冷板技术简报；Frore 等推进 jet/microstructure | 为 Rubin Ultra/Feynman/高功率 ASIC 预研 | 基准 <$80M；乐观 $80-200M；极度 $250-500M | 基准 $0.2-0.5B；乐观 $0.6-1.2B；极度 $1.5-3.0B | 基准 $0.8-1.8B；乐观 $2.0-4.5B；极度 $5-10B | 2027 设计导入，2028 规模化 |
| 生成式设计/AI 优化微通道冷板 | 2026 arXiv 针对 GB200 的生成式设计研究显示较基准并行通道可降平均温度 >5°C、峰值 >35°C | 可降低热点、压降和泵功耗，提升频率稳定 | 基准 <$20M；乐观 $30-80M；极度 $100-200M | 基准 $0.08-0.2B；乐观 $0.25-0.6B；极度 $0.8-1.5B | 基准 $0.3-0.8B；乐观 $1-2B；极度 $2.5-5B | 先体现为设计服务/高端冷板溢价 |
| 液冷母排 / power-cooling 集成组件 | NVIDIA Rubin MGX 提到 liquid cooled busbars 支持 5,000A | 解决 100kW+ rack 内电流、热和服务问题 | 基准 <$50M；乐观 $50-150M；极度 $200-400M | 基准 $0.2-0.5B；乐观 $0.6-1.2B；极度 $1.5-3B | 基准 $0.8-1.8B；乐观 $2-4B；极度 $5-9B | 随 Rubin 2026 H2-2027 上量 |
| AI factory 冷却数字孪生/自动控制 | Schneider-NVIDIA controls reference design 接入 Mission Control；Vertiv OneCore/数字孪生 | 把冷却从设备变成可调度资源，提升 uptime/能效 | 基准 $50-120M；乐观 $120-250M；极度 $250-500M | 基准 $0.3-0.7B；乐观 $0.8-1.6B；极度 $1.8-3.5B | 基准 $0.8-1.8B；乐观 $2-4B；极度 $5-9B | 2026 从大型客户开始，2027 平台化 |
| 热回收/高温水再利用 | 45°C warm-water 使热回收和 dry cooler 更可行 | 降 WUE/PUE，改善地方审批 | 基准 <$100M；乐观 $150-350M；极度 $400-800M | 基准 $0.3-0.8B；乐观 $1-2B；极度 $2.5-5B | 基准 $1-2.5B；乐观 $3-6B；极度 $7-12B | 取决于城市/园区能源耦合，2027 以后更强 |

### 3.2 在研产品利润率预测

| 技术/产品 | 基准毛利率 | 乐观毛利率 | 极度超预期毛利率 | 为什么能高定价 |
|---|---:|---:|---:|---|
| 两相 direct-to-chip | 35-50% | 50-65% | 65-80% | 可靠性验证难，冷媒/材料/密封/服务一体化，客户愿为 waterless 和高热流买单 |
| 4kW+ 高热流冷板 | 35-45% | 45-60% | 60-75% | 绑定下一代芯片 hotspot map，定制设计和测试壁垒强 |
| 生成式微通道冷板设计 | 45-60% | 60-75% | 70-85% | 软件/仿真/IP 属性高，单位材料成本低 |
| 液冷母排 | 30-45% | 45-58% | 55-70% | 电气安全、热、机械、维护同时认证，供应商少 |
| 数字孪生/控制软件 | 55-70% | 65-80% | 75-90% | 与 Mission Control/DCIM/OT 集成后有订阅和锁定属性 |
| 热回收/能源耦合 | 25-40% | 35-50% | 45-60% | 项目型较重，但能源/审批价值大 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能集中在哪些地区和公司

| 地区 | 主要公司/能力 | 产能和战略信号 |
|---|---|---|
| 美国/加拿大 | Vertiv Ohio；CoolIT Calgary；Motivair Buffalo；Eaton/Boyd 美国；Modine Rockbridge VA/Grenada MS；nVent；Supermicro San Jose | CoolIT 称加拿大、中国、越南扩产，月产数百 CDU、数千 rack manifold、数万 server loop；Vertiv 2026 投资约 5,000 万美元扩 Ohio，Ironton 液冷/冷水系统产能 2027 Q2 投产后增约 45%；Motivair 推 2.5MW CDU；Eaton/Boyd 2026E 销售约 17 亿美元 |
| 欧洲 | Vertiv/ThermoKey Italy；Airedale UK；Schneider/Motivair 欧洲供应链；Danfoss；Stäubli；Rittal；STULZ；Kelvion | Vertiv 2026 收购 ThermoKey，强化 EMEA dry cooler、heat exchanger 和液冷；Airedale 400kW-2MW+ CDU 覆盖美国和欧洲生产 |
| 台湾/中国大陆/东南亚 | Delta、Cooler Master、AVC、Auras、Boyd/CoolIT 亚洲产线、ODM/OEM Quanta/Wiwynn/Foxconn/Inventec、Supermicro Taiwan、Giga Computing、ASUS | TrendForce 称冷板供应商 Cooler Master、AVC、Auras 在东南亚扩液冷产能以服务美国 CSP；服务器 ODM 掌握整柜装配和现场交付 |
| 中国本土 | 英维克、申菱环境、高澜股份、同飞股份、佳力图、依米康、曙光数创、华为数字能源、中兴、浪潮、新华三、科华数据、三花智控、盾安环境等 | 国产 AI 集群和算力中心建设推动冷板、CDU、浸没、空液混合、冷水机组本土替代；高端 QD/认证件仍有国际品牌优势 |

### 4.2 供给瓶颈

| 瓶颈 | 为什么卡供给 | 受影响产品 |
|---|---|---|
| 芯片级热图和冷板定制 | GB300/Rubin/MI400/ASIC 封装形态、hotspot、压紧力、翘曲、介电/腐蚀要求不同，不能简单通用 | 冷板、server loop |
| 漏液可靠性和 dry-break QD | 一次漏液可能损失整柜 GPU，hyperscaler 认证周期长，QD 要兼顾压力、流量、盲插、寿命 | QD、歧管、软管 |
| CDU 高压头和冗余泵 | 高密冷板 loop 压降大，CDU 要在高流量下保持压力、过滤、N+1 泵、热备和控制稳定 | CDU |
| 设施水/TCS 管路改造 | 存量机房没有 FWS/TCS，L2L 需要二次侧管路、阀组、排水、维护空间和防漏设计 | L2L CDU、TCS |
| 45°C warm-water 运行经验 | 高温供液提升 free cooling，但要求服务器、冷板、材料、水质和控制都能长期稳定 | GB300/Rubin 新建 hall |
| 现场服务人才 | 液冷交付不是单纯卖设备，需要安装、冲洗、补液、压测、漏测、维护和备件 | 全链条 |
| 标准和客户认证 | NVIDIA RVL、OCP Project Deschutes、UQD04/UQD08、UL/CE、ASHRAE、hyperscaler AVL 决定能否进入 BOM | 冷板、QD、CDU |
| 热拒绝设备 | 干冷器、冷水机组、微通道换热器、自然冷却系统和低 GWP 冷媒供应成为园区级瓶颈 | 热管理项目口径 |
| 供应链地域 | 北美客户希望近岸供应，亚洲冷板和 QD 产能又最成熟，关税/出口/物流会扰动 | 冷板、歧管、整柜 |

### 4.3 成本结构和毛利决定因素

以 132-142kW GB300 NVL72 级机柜为例，严格直液冷硬件制造 BOM 可粗略估为 $45k-70k/rack，系统售价/装配后价值约 $75k-140k/rack；若把 TCS 管路、CDU 共享分摊、施工和热拒绝设备纳入，单 rack 对应热管理项目价值可上升到 $180k-450k，存量改造或极端冗余场景更高。

| 成本项 | BOM 占比 | 毛利决定因素 |
|---|---:|---|
| 冷板，含 GPU/CPU/NVSwitch | 25-35% | 铜材/加工不是主要壁垒，芯片级定制、热均匀性、压降、良率和 leak test 是关键 |
| QD、歧管、软管、阀组 | 20-30% | 高端 dry-break QD 认证少，流量/寿命/盲插可靠性决定溢价 |
| CDU 分摊，含泵、板换、过滤、传感、控制 | 20-30% | MW 级容量、N+1、压力头、低 approach temperature、服务便利性决定售价 |
| 漏液检测、控制、电气接口 | 5-10% | 与 DCIM/Mission Control/EcoStruxure/Redfish 集成后毛利较高 |
| 集成、测试、包装、现场服务 | 10-20% | 客户越急、现场越复杂，服务和工程溢价越高 |

价格传导机制：

| 触发 | 价格如何传导 |
|---|---|
| NVIDIA/AMD/ASIC 平台升级 | 芯片 TDP 上升或 rack 功率上升，冷板面积、流量、QD 规格、CDU 压力头同步升级 |
| 客户抢工期 | 短交期 CDU、认证 QD、现场服务团队溢价；2026 H2 最明显 |
| 水资源和能耗压力 | 高温水、干冷、闭环、低 WUE 方案获得项目溢价 |
| 认证锁定 | 一旦进入 GB300/Rubin/TPU/Trainium AVL，供应商可在平台生命周期内维持价格 |
| 事故风险 | 客户为低漏液率、可维护性、备件和全球服务付安全溢价 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 环节 | 头部集中度判断 | 核心公司 |
|---|---|---|
| 全链路液冷方案/CDU | Top 5 约 50-65%严格设备收入，项目口径更分散 | Vertiv、CoolIT/Ecolab、Schneider/Motivair、Eaton/Boyd、nVent、Modine/Airedale、Delta |
| 冷板/server loop | Hyperscaler 高端平台 Top 5 约 60-75% | CoolIT、Boyd/Eaton、Motivair、Cooler Master、AVC、Auras、Delta、Wakefield Thermal |
| QD/歧管 | 高端认证 QD Top 4 约 65-80% | CPC/Dover、Parker Hannifin、Danfoss、Stäubli、CEJN、Swagelok |
| 整柜/服务器集成 | 高度受 GPU 分配和 OEM 客户关系影响 | Supermicro、Dell、HPE、Lenovo、Quanta、Wiwynn、Foxconn/Ingrasys、Inventec、ASUS、Giga Computing |
| 热拒绝/冷水机/干冷器 | 比较分散，但大项目偏头部 | Vertiv/ThermoKey、Modine/Airedale、Schneider、Johnson Controls/Silent-Aire、Trane、Carrier、Munters、STULZ、Alfa Laval、Kelvion |

Dell'Oro 公开指出 Vertiv 是液冷市场领先者，CoolIT、nVent、Boyd 保持强份额，Aaon 依靠 hyperscaler 深度合作快速增长。TrendForce 在部件层面点名冷板供应商 Cooler Master、AVC、Boyd、Auras；CDU 侧 Delta 在 sidecar 中领先，Vertiv/Boyd 在 in-row CDU 中更适合高密 AI rack；QD 侧 CPC、Parker、Danfoss、Stäubli 在 GB200 项目中先发。

### 5.2 可量化壁垒和为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| 热性能 | 芯片温差、热点温度、压降、流量、approach temperature、泵功耗 | 直接影响 GPU throttle、tokens/watt 和 uptime，客户愿付溢价换稳定频率 |
| 漏液可靠性 | 100% leak test、压力循环、插拔寿命、现场故障率 ppm | 单柜 GPU 价值数百万美元，防漏价值远高于部件成本 |
| 平台认证 | NVIDIA RVL/OCP/UQD/客户 AVL、UL/CE | 认证周期长，未认证供应商无法进入高端项目 |
| 规模制造 | 月产 CDU、manifold、server loop 数量；全球现场服务国家数量 | Hyperscaler 需要 GW 级交付，不只买样品 |
| 工程协同 | 与芯片厂、OEM、CSP 同步设计的提前期 | 冷板必须在芯片/托盘设计阶段进入，后进入者很难替换 |
| 切换成本 | TCS 管路、冷却液、QD 标准、备件、运维流程 | 一旦数据大厅按某套液冷标准建设，换供应商会影响施工和运维 |
| 软件控制 | 与 DCIM、Mission Control、EcoStruxure、Redfish、BMS 打通 | 冷却从静态设备变成动态调度系统，软件和服务毛利更高 |

### 5.3 价值捕获排序

| 排名 | 价值链层级 | 长期 ROIC/毛利判断 | 原因 |
|---:|---|---|---|
| 1 | 认证 QD、blind-mate connector、歧管 | 最高 | 小部件决定系统可靠性，认证和失效率是壁垒，客户对价格不敏感 |
| 2 | 芯片级定制冷板和热仿真 | 很高 | 绑定芯片平台，热性能直接影响算力收入 |
| 3 | MW 级 CDU 控制、冗余与服务 | 高 | 系统工程复杂，头部客户需要全球服务和快速交付 |
| 4 | 冷却液/水质/监控服务 | 高且 recurring | Ecolab/CoolIT 的并购逻辑就在于从一次性设备扩到 fluid management |
| 5 | 整柜液冷集成 | 中高 | 收入体量大、客户粘性强，但服务器 OEM 竞争激烈，毛利被 GPU 分配和客户压价约束 |
| 6 | 传统冷水机、干冷器、热交换器 | 中 | 体量大但工程制造竞争更多，除非与液冷控制/低 GWP/高温水强绑定 |

## 6. 2026 关键变化：行业拐点与最可能放量方向

### 6.1 三个拐点

| 拐点 | 发生概率 | 影响 |
|---|---:|---|
| GB300/NVL72 使 130-142kW rack 成为 AI 数据大厅标准设计单元 | 高 | 冷板、QD、CDU、液冷门和 TCS 管路从项目定制转为标准 BOM |
| 供应链 M&A 和扩产把液冷从小厂赛道变成巨头平台战 | 高 | Ecolab-CoolIT、Eaton-Boyd、Schneider-Motivair、Vertiv-ThermoKey/Ohio 扩产提高行业集中度 |
| L2A 过渡和 L2L 新建并行，存量改造与新建 AI factory 同时拉货 | 高 | 2026 CDU 结构会分化：旧机房 L2A/sidecar，新增 AI hall L2L/in-row |

### 6.2 最可能放量的子方向

| 子方向 | 2026 放量强度 | 订单领先指标 |
|---|---:|---|
| GB300/B300 冷板和机柜 liquid loop | 极高 | NVIDIA GB300、Supermicro/Dell/HPE/Lenovo/ODM 出货和 reference design |
| 1-2.5MW CDU | 极高 | Motivair MCDU-70、CoolIT CHx2000、Eaton ROL4000、Airedale 2MW+ |
| QD/歧管/UQD08 | 极高 | OCP/NVIDIA Rubin MGX 标准件导入 |
| 热拒绝设备和高温 chiller/dry cooler | 高 | Vertiv ThermoKey、Airedale TurboChill 3+MW、Modine/Johnson Controls/Carrier/Trane |
| 控制软件和数字孪生 | 中高 | Schneider-NVIDIA Mission Control reference design、Vertiv OneCore |

## 7. 2027 关键变化：行业拐点与最可能放量方向

### 7.1 三个拐点

| 拐点 | 发生概率 | 影响 |
|---|---:|---|
| L2L warm-water 成为新建 AI hall 主流，L2A 从主流过渡方案转为存量改造方案 | 高 | CDU 价值向 in-row/central L2L、干冷器和高温水控制转移 |
| Rubin/MI400/TPU8/HBM4 使 2kW+芯片和液冷母排成为新增设计重点 | 中高 | 先进冷板、液冷母排、UQD08、AI 优化微通道和两相直冷开始有付费试点 |
| 水资源/能耗/地方审批压力把闭环、低 WUE、热回收变成项目竞争条件 | 高 | Ecolab、Schneider、Vertiv、Modine、Johnson Controls 等“设备+水+控制+服务”更有优势 |

### 7.2 最可能放量的子方向

| 子方向 | 2027 放量强度 | 关键公司 |
|---|---:|---|
| L2L CDU 和集中 TCS | 极高 | Vertiv、CoolIT/Ecolab、Motivair/Schneider、Eaton/Boyd、nVent、Modine/Airedale、Delta |
| 液冷母排和机柜 power-cooling 组件 | 高 | NVIDIA MGX 生态、Eaton、Vertiv、Schneider、nVent、Amphenol/TE 等 |
| 两相 direct-to-chip 和 waterless cold plate | 中高 | ZutaCore、Boyd/Eaton、CoolIT/Ecolab、Frore、LiquidStack、Iceotope |
| 冷却数字孪生和自治控制 | 高 | Schneider、Vertiv、NVIDIA、Siemens、Honeywell、Johnson Controls、Eaton |
| 高温干冷、free cooling、热回收 | 高 | Vertiv/ThermoKey、Modine/Airedale、Johnson Controls、Trane、Carrier、Munters、Alfa Laval、Kelvion |

## 8. 公司全景清单

### 8.1 国际头部和细分优势公司

| 环节 | 公司 |
|---|---|
| 芯片/平台牵引 | NVIDIA、AMD、Intel、Google TPU/Broadcom、AWS Annapurna/Trainium、Microsoft Maia、Meta MTIA/Broadcom、OpenAI/Broadcom、Marvell、Huawei、Cambricon、Alibaba T-Head、Baidu Kunlun |
| 整柜/服务器/OEM/ODM | Supermicro、Dell、HPE、Lenovo、ASUS、Giga Computing/Gigabyte、Quanta、Wiwynn、Foxconn/Ingrasys、Inventec、Wistron、Jabil、MiTAC/Tyan、xFusion、Inspur、H3C |
| 全链路液冷/CDU | Vertiv、CoolIT Systems/Ecolab、Schneider Electric/Motivair、Eaton/Boyd Thermal、nVent、Modine/Airedale、Delta、STULZ、Rittal、Johnson Controls/Silent-Aire、Trane、Carrier、AAON、Munters |
| 冷板/server loop | CoolIT、Boyd/Eaton、Motivair、Cooler Master、AVC、Auras、Delta、Wakefield Thermal、Wieland、D6 Industries、Fujikura、Frore Systems |
| 快接头/QD/歧管/流体连接 | CPC/Dover、Parker Hannifin、Danfoss、Stäubli、CEJN、Swagelok、Eaton、nVent、Boyd、CoolIT |
| 泵阀过滤与换热器 | Grundfos、Xylem、Wilo、Danfoss、Parker、Alfa Laval、Kelvion、SPX Flow、Belimo、Watts、Armstrong、ThermoKey、Güntner |
| 冷却液/水处理/化学品 | Ecolab/Nalco、Chemours、Engineered Fluids、Shell、Castrol/BP、Solvay/Syensqo、Lubrizol、Dow、DuPont、3M legacy fluids |
| 浸没/两相/水less 方案 | ZutaCore、LiquidStack、Submer、GRC、Iceotope、Asperitas、Engineered Fluids、Frore Systems |
| 控制/数字孪生/DCIM | Schneider EcoStruxure/ETAP、Vertiv Unify/OneCore、NVIDIA Mission Control/DSX/Omniverse、Siemens、Honeywell、Johnson Controls、Eaton Brightlayer、Rockwell、nVent |

### 8.2 中国/亚洲相关公司

| 环节 | 公司 |
|---|---|
| 液冷整机和数据中心方案 | 华为数字能源、中兴通讯、浪潮信息、新华三、曙光数创、联想、宝德、烽火通信 |
| 温控/冷却设备 | 英维克、申菱环境、高澜股份、同飞股份、佳力图、依米康、科华数据、盾安环境、三花智控、双良节能、海悟、科士达 |
| 冷板/结构件/材料 | 飞荣达、银轮股份、强瑞技术、精研科技、立讯精密、富士康工业富联、台达、Cooler Master、AVC、Auras |
| 连接器/流体件/机柜配电 | 立讯精密、安费诺、TE Connectivity、正泰电器、良信股份、汇川技术、麦格米特、科华数据 |

## 9. 投资排序

| 投资吸引力 | 子赛道 | 逻辑 |
|---|---|---|
| 第一梯队 | QD/歧管、定制冷板、MW 级 CDU | 直接卡交付，认证强，客户价格敏感度低，2026-2027 订单弹性最大 |
| 第二梯队 | 冷却控制软件、水质/冷却液服务、现场服务 | recurring 属性增强，行业从一次性交付走向持续运维 |
| 第三梯队 | 热拒绝设备、高温 chiller、dry cooler | 项目金额大，受益于 warm-water 和低 WUE，但竞争更像传统机电 |
| 第四梯队 | 整柜液冷集成/OEM | 收入大但毛利受 GPU 分配、客户集中和 ODM 竞争约束 |
| 观察型 | 两相 direct-to-chip、浸没、热回收 | 技术弹性大，但 2026 仍偏试点，真正主流化看 2027-2028 |

## 10. 风险

| 风险 | 影响 |
|---|---|
| AI CapEx 延期或利用率不及预期 | 设备订单延后，特别是 NeoCloud 和非头部客户 |
| HBM/CoWoS/GPU 供给拖延 | 液冷项目随 rack 交付推迟，但电力/机电先行订单可能仍保留 |
| 液冷事故 | 漏液、腐蚀、堵塞、微生物、水质问题会导致客户转向认证头部，长尾出清 |
| 标准路线变化 | 两相/浸没若突然被某大客户采用，会改变冷板/CDU 价值分布 |
| 区域水资源和审批 | 闭环、干冷和热回收是机会，也会增加项目复杂度 |
| 价格下行 | 一旦 2027 供给扩张过快，普通冷板/CDU 可能从短缺转向竞争，只有认证件/软件/服务留住毛利 |

## 主要资料来源

- [Dell'Oro Group: Data Center Liquid Cooling Market to Approach $7 Billion by 2029](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html)
- [TrendForce: Liquid Cooling Penetration to Surpass 30% in 2025](https://www.trendforce.com/presscenter/news/20250821-12682.html)
- [NVIDIA Vera Rubin POD Technical Blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- [NVIDIA Vera Rubin official release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx)
- [NVIDIA Rubin launch release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Kicks-Off-the-Next-Generation-of-AI-With-Rubin--Six-New-Chips-One-Incredible-AI-Supercomputer/default.aspx)
- [NVIDIA GB300 NVL72 official page](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- [Supermicro Vera Rubin liquid-cooling capacity release](https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Support-for-Upcoming-NVIDIA-Vera-Rubin-NVL72-HGX-Rubin-NVL8-and-Expanded-Rack-Scale-Manufacturing-Capacity-for-Liquid-Cooled-AI-Solutions/default.aspx)
- [Supermicro DLC-2 direct liquid cooling](https://www.supermicro.com/en/pressreleases/supermicros-dlc-2-next-generation-direct-liquid-cooling-solutions-aims-reduce-data)
- [Supermicro GB300 NVL72 rack](https://www.supermicro.com/en/products/system/gpu/48u/srs-gb300-nvl72)
- [Schneider Electric / Motivair MCDU-70 2.5MW CDU](https://www.se.com/us/en/about-us/newsroom/news/press-releases/motivair-by-schneider-electric-announces-new-cdu-with-capability-to-scale-to-10mw-and-beyond-for-next-gen-ai-factories-69705c3655f8517e99086bbd/)
- [Schneider Electric liquid cooling portfolio with Motivair](https://www.se.com/ww/en/about-us/newsroom/news/press-releases/Schneider-Electric-Unveils-Liquid-Cooling-Portfolio-with-Motivair-Featuring-Dedicated-Solutions-and-Services-for-HPC-and-AI-Workloads-68d69e595c9dbb622505caf3/)
- [Schneider/NVIDIA GB300 power and liquid cooling reference design](https://live.euronext.com/sites/default/files/company_press_releases/attachments/2025/09/18/cpr01_notified_2025-09-18_Press%20Release_Schneider%20Electric%20Announces%20New%20Reference%20Designs_NVIDIA.pdf)
- [Vertiv MegaMod HDX modular liquid cooling infrastructure](https://investors.vertiv.com/news/news-details/2026/Vertiv-Introduces-New-Modular-Liquid-Cooling-Infrastructure-Solution-to-Support-High-Density-Compute-Requirements-in-North-America-and-EMEA/default.aspx)
- [Vertiv Q1 2026 results and guidance](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx)
- [Vertiv ThermoKey acquisition](https://investors.vertiv.com/news/news-details/2026/Vertiv-to-Acquire-ThermoKey-Expanding-Heat-Rejection-Portfolio-for-Converged-Physical-Infrastructure/default.aspx)
- [Vertiv Ohio manufacturing expansion](https://investors.vertiv.com/news/news-details/2026/Vertiv-to-Expand-Ohio-Manufacturing-to-Boost-U-S--Production-of-Critical-Thermal-Management-Technologies-for-AI-Data-Centers/default.aspx)
- [Ecolab to acquire CoolIT Systems](https://www.ecolab.com/news/2026/03/ecolab-to-acquire-coolit-systems-a-global-leader-in-advanced-liquid-cooling-for-next-gen-ai-data-ce)
- [CoolIT rapid growth and capacity release](https://www.prnewswire.com/news-releases/coolit-systems-continues-rapid-growth-as-it-celebrates-25-years-302696525.html)
- [CoolIT CHx2000 AI CDU](https://www.coolitsystems.com/resources/news/chx2000-the-ai-cdu/)
- [Eaton completes Boyd Thermal acquisition](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-completes-acquisition-of-leading-liquid-cooling-solutions-provider-boyd-thermal.html)
- [Eaton/Boyd ROL4000 CDU](https://www.eaton.com/us/en-us/catalog/thermal-management-solutions/coolant-distribution-unit-cdu.html)
- [Eaton 3Q 2025 Boyd Thermal presentation](https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2025/q3/3Q-2025-analyst-presentation.pdf)
- [nVent liquid cooling products](https://www.nvent.com/en-us/data-solutions/products/liquid-cooling)
- [nVent next generation liquid cooling and power portfolios](https://www.nvent.com/en-gb/data-solutions/next-generation-liquid-cooling-and-power-portfolios-coming-2026)
- [Modine/Airedale CDU](https://www.airedale.com/data-centers/liquid-cooling/cdu/)
- [Modine Airedale $180M data center cooling orders](https://www.modine.com/news/airedale-by-modine-secures-180-million-in-orders-for-data-center-cooling-systems/)
- [Modine TurboChill 3+MW AI data center cooling](https://investors.modine.com/news/news-details/2026/Airedale-by-Modine-Unveils-TurboChill-3MW-Redefining-Air-Cooled-Efficiency-for-AI-Data-Centers/default.aspx)
- [Microsoft Maia 200 official blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)
- [Microsoft Fairwater AI datacenter](https://blogs.microsoft.com/blog/2025/09/18/inside-the-worlds-most-powerful-ai-datacenter/)
- [arXiv 2026: Generative Design for Direct-to-Chip Liquid Cooling for Data Centers](https://arxiv.org/abs/2604.10941)

非投资建议，仅供产业链研究和情景推演。
# 行业调研：【数据中心自备发电与微电网】

> 版本日期：2026-05-08  
> 研究口径：全球 AI 数据中心自备发电与微电网，重点看美国和北美。金额均为美元名义值，`B` = 十亿美元，`GW` = 吉瓦。  
> 市场规模口径：按“数据中心相关的新签订单、设备交付池、PPA/电力基础设施合同中可由供应链捕获的设备与工程价值”估算，不等同于当期收入确认。  
> 时间口径：未来 3 个月指 2026-05 到 2026-08，1 年指到 2027-05，2 年指到 2028-05。  
> 芯片背景：采用项目内 `ai_chip_research_2026_2027.md` 和 `AI数据中心建设规模与产业链订单映射_2026-2027_美国.md` 的芯片/建设假设，不再外搜芯片路线。

## 0. 结论先行

数据中心自备发电与微电网在 2026 年已经从“应急桥接方案”升级为 AI 基础设施的一线主战场。我的核心判断是：

1. **2026 最确定放量路径是天然气发电加 BESS 加微电网控制**。AI 园区要的是“现在就能上电”，不是 2030 年的完美能源结构。燃气往复式机组、燃气轮机、BESS、UPS、开关柜、微电网控制器会成为 2026 订单弹性最大的组合。
2. **燃料电池从小众变成可见 GW 级路线**。Bloom Energy 与 Oracle 2026-04 宣布主协议最高 2.8GW、初始 1.2GW 已签约并部署，是目前最强的一手验证。燃料电池在土地、噪声、水、NOx、许可压力大的项目中会获得高溢价。
3. **公用事业侧和园区侧正在合流**。Meta/Entergy 的 Louisiana Hyperion 方案把 5.2GW 新增联合循环、240 英里 500kV 输电、BESS、核电增容和 2.5GW 可再生资源打包，由 Meta 支付完整成本。这不是传统“买电”，而是 hyperscaler 定制电力系统。
4. **2027 的爆点会从单项目订单转为多园区复制**。如果 GB300、Rubin、MI400、Trainium3、TPU Ironwood/TPU8、Maia/MTIA 等机架密度按乐观节奏上电，数据中心会从“找电力接入点”转向“自带电厂、自带储能、自带微电网控制”。
5. **长期高 ROIC 更可能在控制、电力电子、服务和已认证高端设备层**。重资产 IPP/电厂利润受燃料和监管压制，EPC 毛利不高但订单大；真正可持续高毛利在微电网 EMS、保护控制、grid-forming PCS、关键开关柜/UPS、燃料电池堆和燃机长协服务。

## 1. 2026 机会、挑战与最可能技术路径

### 1.1 一手信号：最近半年已经不是概念验证

| 日期 | 公司/项目 | 一手或强验证信息 | 对行业含义 |
|---|---|---|---|
| 2026-01-28 | AIP Corp / Caterpillar / Boyd CAT | AIP 为 West Virginia Monarch Compute Campus 订购 **2GW** Caterpillar G3516 快速响应天然气机组，2026-09 到 2027-08 交付，并配 BESS；项目远期目标 **8GW**；G3516 可约 7 秒从零到满载。[Caterpillar](https://www.caterpillar.com/en/news/corporate-press-releases/h/aip-boyd-cat.html) | 往复式燃气机组正式进入 GW 级 AI 园区主电源，而非只做备用。 |
| 2026-02-11 | Baker Hughes / Twenty20 Energy | Baker Hughes 获 Twenty20 Energy 订单，10 台 Frame 5 燃气轮机和发电设备，最高 **250MW**，用于 Georgia 和 Texas 数据中心项目；同时推进多 GW 战略合作。[Nasdaq/GlobeNewswire](https://www.nasdaq.com/press-release/baker-hughes-receives-gas-turbine-order-twenty20-energy-power-us-data-center) | 中小型燃气轮机用于数据中心独立电源包，交付从 2027 开始。 |
| 2026-03-04 | Babcock & Wilcox / Base Electron / Applied Digital | B&W 获 full notice to proceed，**$2.4B** 设计建造合同，1.2GW 新增天然气发电，4 套 300MW 燃气锅炉和汽轮发电系统，供 Applied Digital AI Factory 园区。[B&W](https://www.babcock.com/home/about/corporate/news?f=ec425f1b-cde7-46e4-8502-965836e95e08) | AI 园区电源 EPC 订单开始进入十亿美元级别，项目融资依赖长约承购。 |
| 2026-03-05 | Generac / EPC Power | 双方宣布面向数据中心的完整 behind-the-meter 能源解决方案，组合 Generac SBE Block、ARC Controller 和 EPC Power grid-forming inverter，用于 AI 负载平滑、ride-through、离网/并网。[Generac](https://investors.generac.com/news-releases/news-release-details/generac-and-epc-power-deploy-fully-integrated-energy-solutions) | 微电网从“发电机加电池”升级为“电池、PCS、控制器、发电机、并网要求”的成套产品。 |
| 2026-03-20 | NextEra | NextEra 获批开发最高 **10GW** Texas/Pennsylvania 天然气发电项目服务大负载；公司称有接近 30 个 hub，目标约 40 个。[NextEra](https://www.investor.nexteraenergy.com/news-and-events/news-releases/2026/03-20-2026-143924472) | 大型能源开发商把数据中心 hub 作为单独增长通道。 |
| 2026-03-27 | Entergy Louisiana / Meta | Entergy 与 Meta 新协议：Meta 支付完整成本，建设 **5.2GW+** 新联合循环燃气电厂、约 240 英里 500kV 输电、三处 BESS、核电增容，并承诺支持最高 2.5GW 可再生资源。[Entergy](https://www.entergy.com/news/entergy-louisiana-announces-a-new-agreement-with-meta-that-will-deliver-an-additional-2b-in-customer-savings) | Hyperscaler 正在“定制公用事业扩建”，监管焦点转向 ratepayer protection。 |
| 2026-04-13 | Bloom Energy / Oracle | Oracle 拟采购最高 **2.8GW** Bloom 固体氧化物燃料电池，初始 **1.2GW** 已签约且部署中，支持美国 AI/云基础设施。[Bloom](https://www.bloomenergy.com/news/bloom-energy-and-oracle-expand-strategic-partnership-to-deploy-up-to-2-8-gw-to-accelerate-ai-infrastructure-build-out/) | 燃料电池第一次具备 GW 级 AI 数据中心订单验证。 |
| 2026-04-22 | GE Vernova | Q1 2026 backlog 环比增长超 **$13B**；预计 2026 年底燃气轮机 backlog 和 slot reservation 至少 **110GW**；Electrification 单季数据中心设备订单 **$2.4B**，超过 2025 全年。[GE Vernova](https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf) | 燃机和电气设备供给成为 2026-2028 关键瓶颈，客户抢 slot。 |
| 2026-04-29 | Cummins | Q1 2026 CEO 称 Power Systems 创纪录，数据中心备用电源需求持续强劲，且电力发电需求超预期；上调 2026 收入和 EBITDA 指引。[Cummins](https://investor.cummins.com/news/detail/694/cummins-delivered-strong-operating-results-and-returned) | 柴油/天然气备用电源仍是最稳的现金流池。 |
| 2026-04-29 | Generac | Q1 2026 C&I 销售同比 +28%，称数据中心客户 backlog 增长，多个 hyperscale 供应商认证进入最后阶段；收购 Enercon 强化机箱/开关柜垂直整合。[Generac](https://www.globenewswire.com/de/news-release/2026/04/29/3283534/0/en/generac-reports-first-quarter-2026-results.html) | 后备电源供应商正在向“兆瓦级完整电力模块”迁移。 |
| 2026-05-05 | Blue Energy / GE Vernova | 双方宣布 **2.5GW** gas-plus-nuclear 合作，Texas 首站计划 2027 FID；两台 GE 7HA.02 slot reservation 2029 到场，2030 先上约 1GW 燃气，2032 起切入约 1.5GW BWRX-300 核电。[PRNewswire](https://www.prnewswire.com/news-releases/blue-energy-and-ge-vernova-accelerate-gas-plus-nuclear-approach-for-powering-american-communities-and-fueling-global-ai-leadership-302761986.html) | 2027 之后会出现“燃气桥接加 SMR 后切换”的融资叙事。 |

### 1.2 行业机会

1. **Time-to-power 溢价**：传统并网、变电站、输电审批周期常常是 24-60 个月；AI 客户愿意为 6-18 个月上电支付溢价。AIP/Caterpillar、Bloom/Oracle、B&W/Applied Digital 都是这个逻辑。
2. **负载波动变成产品需求**：AI 训练和推理负载不是平滑工业负载。GB300、Rubin、MI400、TPU、Trainium3 进入 100kW+ 机架密度后，毫秒到分钟级功率摆动需要 BESS、grid-forming PCS、飞轮/超级电容、微电网 EMS 共同处理。
3. **监管压力反而推动“自带电源”**：ratepayer protection 要求科技公司不把电网扩建成本转嫁给居民。Meta/Entergy 是模板，后续大型项目会越来越多采用客户出资、专线/专用电厂、可核算成本服务。
4. **气、电、热一体化**：CCHP、废热回收、吸收式制冷、液冷二次侧能源管理可以把电力、冷却、热管理打包，降低 PUE 和总拥有成本。
5. **设备订单先于 GPU 交付**：电力设备长交期导致 2026 先抢变压器、开关柜、燃机、发动机、SCR、BESS、PCS。即使 GPU 短期有波动，电力订单也会先行锁定。

### 1.3 行业挑战

1. **燃机和发动机 slot 被抢空**：GE Vernova 已给出 110GW backlog/slot reservation 目标，Caterpillar、Cummins、Rolls-Royce mtu 均显示数据中心需求外溢。长交期将从 2026 延续到 2028。
2. **空气许可和社区反对**：xAI Memphis/Southaven 的临时燃气轮机争议说明，未许可现场发电会触发 EPA、州环保部门和社区诉讼。天然气路线越快，NOx、CO、甲醛、噪声、水耗越会被放大。
3. **燃气管道和 firm gas**：数据中心要 24/7 高可用，不能只靠中断性气源。燃气管线、压缩机、储气、firm transportation 会成为和电气设备同级的瓶颈。
4. **微电网保护复杂**：多台发电机、BESS、UPS、并网点、AI 瞬态负载并联后，短路电流、保护定值、黑启动、同步并网、谐波和网络安全难度明显上升。
5. **财务与承购风险**：Bloom/Oracle、B&W/Applied、AIP/CAT 都靠大型客户承购或融资支持。若 AI 租赁价格或 GPU 利用率波动，重资产项目的融资成本会迅速变化。

### 1.4 2026 最可能技术路径

按“能否 2026 放量、能否融资、能否通过许可、是否匹配 AI 负载”排序：

| 排名 | 技术路径 | 2026 状态 | 2027 放量判断 | 适配场景 |
|---:|---|---|---|---|
| 1 | 天然气往复式机组 + BESS + 微电网 EMS | 已有 AIP/CAT 2GW 订单验证 | 大概率高增长 | 200MW 到 2GW 园区、快速桥接、负载跟随 |
| 2 | 公用事业联合循环/燃气轮机 + 专线输电 + BESS | Meta/Entergy、Homer City、NextEra 体现 GW 级趋势 | 2027-2028 大规模确认 | 1GW 以上超大 AI campus |
| 3 | 燃料电池微电网 | Oracle/Bloom 最高 2.8GW 验证，但供应链要爬坡 | 2027 从高端项目向多客户扩散 | 水/空气/噪声受限、要求低排放和高可靠项目 |
| 4 | 柴油/HVO 备用 + grid-interactive UPS | 成熟且持续增长 | 稳定增长，不是主电源 | 备用、黑启动、N+1/N+2 韧性 |
| 5 | BESS/grid-forming PCS/飞轮/超级电容 | 已从 UPS 扩展到电网支撑和负载平滑 | 2027 成为并网审批的标配 | 毫秒到小时级支撑、需求响应、孤岛运行 |
| 6 | 核电重启/SMR/燃气加核电桥接 | 2026 主要是协议、许可、slot reservation | 2029 前实际电量有限，2027 先放量工程订单 | 5-10 年视角的低碳 24/7 电源 |
| 7 | 地热/长时储能/纯可再生离网 | 项目制，地区受限 | 2027-2028 仍偏示范 | 高 ESG 要求、资源禀赋地区 |

## 2. 受 2026-2027 AI 芯片路线驱动的成熟与放量时间

项目内芯片报告给出的 2026-2027 主线是：2026 以 NVIDIA B300/GB300 Blackwell Ultra、AWS Trainium2、Google TPU Ironwood、B200/GB200、MI350、Maia200、Meta MTIA、国产 Ascend/MLU 为主；2027 切向 Rubin、MI400/MI455X Helios、Trainium3/4、TPU8、更多 Broadcom XPU。它们对电力的共同影响是：

| 芯片/平台 | 电力和微电网含义 | 对 2026-2027 电源路线的拉动 |
|---|---|---|
| GB300/B300、GB200/B200 | NVL72/整柜交付带来 100kW+ 机架、全液冷、48V 机柜供电、瞬态负载更大 | 2026 下半年开始显著推高 BESS、UPS、CDU、电源质量和现场发电需求 |
| AWS Trainium2/3 | Project Rainier 近 50 万颗级别，Trainium3 144 芯片 UltraServer，高密度云自用 | 以 hyperscaler 自有园区为主，推动公用事业侧专用发电和储能 |
| Google TPU Ironwood / TPU8 | 推理优先，百万级 TPU 目标意味着长期高利用率、低延迟、规模化电力需求 | 更偏 PPA、储能、需求响应和电力调度软件 |
| AMD MI350/MI400 Helios | MI400 72 GPU rack、HBM4、更高液冷和供电密度 | 2027 拉动高压直流、BESS、微电网控制和燃气桥接 |
| Microsoft Maia200、Meta MTIA、OpenAI/Broadcom ASIC | 自研 ASIC 大规模推理把“训练峰值”变成“全天候推理基荷” | 自备电源从临时桥接变成 24/7 基础设施 |
| 华为 Ascend、寒武纪、国产 AI 集群 | 大规模并联弥补单芯片差距，对园区电力、国产 UPS/液冷/配电要求高 | 中国和中东主权 AI 园区将推动本地微电网和储能 |

### 2.1 新技术成熟与放量时间三情景

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|
| 天然气往复式机组 AI 微电网 | 2026 H2 订单放量，2027 成套交付，2028 标准化 | 2026 Q3 即出现更多 GW 订单，2027 形成 10GW+ 年订单池 | CAT/Cummins/mtu/Generac 快速扩产，2027 年可见 20GW+ 数据中心专用订单 |
| 燃气轮机/联合循环 AI campus | 2026 抢 slot，2027-2028 交付第一批大项目 | 2027 H2 多项目开工，2028 形成 30GW 以上 pipeline | 政府 fast-track 加速许可，2027 就确认 50GW+ 项目池 |
| SOFC 燃料电池 | 2026 Oracle 项目爬坡，2027 多客户验证 | 2027 供应链到 3-5GW/年，更多 Oracle/colo 项目采用 | 2028 前成为“低排放快速上电”默认方案之一，年订单 10GW+ |
| Grid-forming BESS/PCS | 2026 与 UPS/微电网绑定，2027 标配化 | 2027 并网审查要求 BESS 负载平滑，attach rate 到 40-60% | AI 负载参与调频/需求响应，BESS 订单随每 GW IT 配 0.5-2GWh |
| DC/MVDC 微电网 | 2026 试点，2027 小批量 | 2027 在高密度机架园区商业化 | 2028 成为新建 AI 机房配电架构重要分支 |
| SMR/核电重启 | 2026-2027 以协议和许可为主，2029+ 电量 | 2027-2028 重启项目融资落地，SMR 工程订单增加 | 燃气加核电桥接模型被金融机构接受，2030 前可见首批商业电量 |
| 地热/长时储能 | 资源地区小规模 PPA | 2027 多个 hyperscaler 24/7 clean power 项目签约 | 2028 前从 ESG 项目变成供电组合的 5-10% |

## 3. 已开始放量的关键产品：市场规模、渗透率、利润率

### 3.1 未来市场规模和渗透率

| 产品 | 当前放量证据 | 未来 3 个月市场规模 | 1 年市场规模 | 2 年市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 柴油/HVO 备用发电机组 2-4MW | Cummins、Generac、Rolls-Royce 均指向数据中心备用电源强需求；Generac 新 2.25-3.25MW 产品线 | 基准 $2-4B；乐观 $4-6B；极度 $6-9B | 基准 $10-16B；乐观 $16-24B；极度 $24-35B | 基准 $22-35B；乐观 $35-55B；极度 $55-80B | 备用 attach rate 仍 80-95%；但主电源占比低于 5% |
| 天然气往复式机组 | CAT/AIP 2GW，7 秒满载，BESS 配套；Rolls-Royce mtu 推出 fast-start gas genset | 基准 $3-7B；乐观 $7-11B；极度 $11-18B | 基准 $15-28B；乐观 $28-45B；极度 $45-75B | 基准 $35-65B；乐观 $65-110B；极度 $110-180B | 新建 AI 园区现场主电源 MW 占比：2026 8-15%，2027 15-28%，2028 20-35% |
| 燃气轮机/联合循环成套 | Baker Hughes 250MW、B&W/Applied 1.2GW、Meta/Entergy 5.2GW、Homer City 4.5GW | 基准 $4-10B；乐观 $10-18B；极度 $18-30B | 基准 $25-45B；乐观 $45-75B；极度 $75-130B | 基准 $60-110B；乐观 $110-200B；极度 $200-350B | GW 级 campus 自备/专用电源占比：2026 20-35%，2027 35-50%，2028 45-65% |
| SOFC 燃料电池 | Bloom/Oracle 最高 2.8GW，初始 1.2GW；Bloom Q1 2026 product gross margin 34.3% | 基准 $3-6B；乐观 $6-10B；极度 $10-16B | 基准 $12-22B；乐观 $22-40B；极度 $40-70B | 基准 $25-55B；乐观 $55-100B；极度 $100-180B | AI 新增现场电源 MW 占比：2026 2-5%，2027 5-12%，2028 8-18% |
| BESS/grid-forming PCS | Generac/EPC、NextEra 1.3GW 单季储能 origination、Entergy/Meta BESS | 基准 $2-5B；乐观 $5-9B；极度 $9-15B | 基准 $12-25B；乐观 $25-45B；极度 $45-80B | 基准 $28-60B；乐观 $60-120B；极度 $120-220B | AI 自备电源项目 attach rate：2026 25-40%，2027 40-65%，2028 55-80% |
| UPS、飞轮、超级电容、rack/园区短时储能 | AI 瞬态负载、NVIDIA DSX 类动态调度、数据中心传统 UPS 升级 | 基准 $3-6B；乐观 $6-9B；极度 $9-14B | 基准 $14-24B；乐观 $24-38B；极度 $38-60B | 基准 $30-55B；乐观 $55-90B；极度 $90-140B | 关键 AI 机房 attach rate 接近 100%，高端短时储能 attach rate 从 10-20% 升至 30-50% |
| 微电网 EMS、保护控制、开关柜集成 | Siemens/Eaton、Generac/EPC、Schneider/Eaton/ABB/SEL 体系成熟 | 基准 $1-3B；乐观 $3-5B；极度 $5-8B | 基准 $6-12B；乐观 $12-22B；极度 $22-35B | 基准 $15-30B；乐观 $30-60B；极度 $60-100B | 自备电源项目 attach rate 2026 40-60%，2027 60-80%，2028 75-90% |
| 专用输电/变电/中高压配电 | Entergy/Meta 240 英里 500kV，GE Vernova Q1 数据中心电气订单 $2.4B | 基准 $5-10B；乐观 $10-18B；极度 $18-30B | 基准 $30-55B；乐观 $55-90B；极度 $90-150B | 基准 $70-130B；乐观 $130-230B；极度 $230-380B | 所有 GW 级项目必配，瓶颈强于发电本体 |

### 3.2 利润率三情景

| 产品 | 基准毛利率 | 乐观毛利率 | 极度超预期乐观毛利率 | 为什么能提价 |
|---|---:|---:|---:|---|
| 柴油/HVO 备用发电机组 | 22-30% | 28-35% | 35-42% | 客户认证、交期、冗余设计、全球服务网络 |
| 天然气往复式机组 | 20-30% | 28-38% | 38-45% | 快速响应、连续运行能力、排放控制、成套调试 |
| 燃气轮机 OEM | 20-28% 设备；25-40% 服务 | 28-35% 设备；35-45% 服务 | 35-45% 设备；45%+ 服务 | slot 稀缺、长协服务、热部件维护锁定 |
| 燃气电厂 EPC | 5-10% | 8-13% | 12-18% | 项目复杂、并行施工、变更订单、长交期采购能力 |
| SOFC 燃料电池 | 30-38% | 38-45% | 45-55% | 低排放、低水耗、小占地、高可靠和可快速模块化部署 |
| BESS 系统集成 | 10-18% | 16-25% | 25-32% | grid-forming、消防认证、并网模型、软件控制 |
| PCS/逆变器/控制器 | 25-38% | 35-45% | 45-60% | 算法、认证、动态响应、并网代码和网络安全 |
| 微电网 EMS/保护软件 | 35-55% | 50-65% | 65-75% | 软件、保护逻辑、客户锁定、运维数据闭环 |
| UPS/飞轮/超级电容 | 25-38% | 35-45% | 45-55% | 可靠性认证、短时功率密度、维护和替换周期 |

## 4. 在研或早期商业化关键技术

### 4.1 未来市场规模、渗透率、利润率

| 技术 | 当前阶段 | 未来 3 个月市场规模 | 1 年市场规模 | 2 年市场规模 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| SMR / 核电重启 / 核电增容 | 协议、许可、工程准备；Blue/GE 2.5GW，NextEra Duane Arnold Q1 2029 目标 | 基准 $0.2-1B；乐观 $1-3B；极度 $3-6B | 基准 $1-5B；乐观 $5-15B；极度 $15-35B | 基准 $5-20B；乐观 $20-60B；极度 $60-150B | 2028 前实际电量接近 0，但合同 pipeline 可到新增 AI 电力 5-15% | 设备/工程早期 10-25%；成熟后燃料服务和运维 25-40% |
| 燃气加核电桥接 | Blue/GE：2030 先上约 1GW 燃气，2032 切到约 1.5GW 核 | $0.1-0.5B；$0.5-1.5B；$1.5-4B | $1-4B；$4-10B；$10-25B | $5-15B；$15-45B；$45-100B | 2027-2028 主要是 slot 和早期 EPC | 取决于风险分摊，gas side 15-30%，nuclear EPC 低但服务长尾高 |
| MVDC/HVDC 数据中心微电网 | 试点和设计阶段，受 48V rack、800V DC、液冷泵等驱动 | $0.1-0.4B；$0.4-1B；$1-2B | $0.8-2B；$2-5B；$5-10B | $3-8B；$8-20B；$20-45B | 2026 小于 3%，2028 可达高密 AI 新建项目 10-25% | 功率电子 25-45%，控制软件 50%+ |
| 长时储能 LDES | 铁空气、液流、热储能、压缩空气仍以示范和 PPA 为主 | $0.1-0.5B；$0.5-1.5B；$1.5-4B | $0.5-3B；$3-8B；$8-20B | $3-12B；$12-35B；$35-80B | 2028 前多为 ESG/韧性附加，attach rate 低于 10% | 早期负毛利到 20%，系统成熟后 20-35% |
| 地热/增强型地热 + 数据中心 | Google/Fervo 等验证，但资源受限 | $0.1-0.5B；$0.5-1B；$1-2B | $0.5-2B；$2-5B；$5-12B | $2-8B；$8-20B；$20-45B | 资源地区 2028 可见 1-5% 电量贡献 | 开发商项目 IRR 8-15%，设备服务 20-35% |
| 燃机碳捕集/低碳燃料 | B&W 碳捕集、氢掺烧、SCR/CCS 前端设计 | $0.2-1B；$1-3B；$3-6B | $1-5B；$5-12B；$12-25B | $5-15B；$15-40B；$40-90B | 先作为许可选项，2028 后看政策 | 碳捕集设备 15-30%，溶剂/服务 30-45% |
| 柔性 AI Factory / 需求响应 | NVIDIA/Emerald AI 与电力公司探索 flexible AI factories | $0.1-0.3B；$0.3-1B；$1-3B | $0.5-2B；$2-6B；$6-15B | $2-8B；$8-25B；$25-60B | 2026 框架，2027 商业试点，2028 可进入电网容量市场 | 软件和调度平台 50-75% |

### 4.2 哪些在研方向最可能快速增长

1. **Grid-forming inverter 和微电网保护控制**：比发电本体更轻资产，客户一旦认证，复制速度快。
2. **SOFC 供应链扩产**：Oracle 2.8GW 是锚点。如果 Bloom 在 2026-2027 证明交付能力，燃料电池会成为高端 AI 园区第三条主电源路线。
3. **燃气加核电桥接**：2027 FID 之前不会贡献大量收入，但它能解决“2030 前先上电、2032 后降碳”的融资叙事。
4. **MVDC/HVDC**：如果 Rubin/MI400/后续 ASIC 继续推高机架电流，交流配电加多级 AC/DC 损耗会推动 DC 微电网加速。

## 5. 供给侧：产能结构、瓶颈、成本与毛利

### 5.1 产能结构

| 环节 | 主要地区 | 主要公司 | 产能/工艺特征 |
|---|---|---|---|
| 大型燃气轮机 | 美国、欧洲、日本 | GE Vernova、Siemens Energy、Mitsubishi Power、Ansaldo、Baker Hughes/Nuovo Pignone | H/J/HA/F 级大机和中小型 Frame 机组，slot 和热部件服务稀缺 |
| 往复式燃气/柴油机组 | 美国、德国、英国、芬兰、中国、印度 | Caterpillar、Cummins、Rolls-Royce mtu、Wartsila、INNIO Jenbacher、Kohler、Generac、Mitsubishi Heavy Industries Engine、Yuchai/Weichai | 2-4MW 备用机、10-20MW 大型燃气发动机、连续运行和快速启动能力 |
| 燃料电池 | 美国、日本、韩国 | Bloom Energy、FuelCell Energy、Doosan Fuel Cell、Plug Power、Ballard、Bosch SOFC | SOFC/PEM/MCFC 路线，数据中心当前最强验证为 Bloom SOFC |
| BESS/PCS | 美国、中国、韩国、欧洲 | Tesla、Fluence、Wartsila、Powin、CATL、BYD、Sungrow、EPC Power、SMA、Nidec、Hitachi Energy | LFP 电芯、grid-forming PCS、消防和并网模型是核心 |
| UPS/短时储能 | 美国、欧洲、日本、中国 | Vertiv、Schneider Electric、Eaton、ABB、Legrand、Socomec、Piller、Active Power、VYCON、Riello UPS | 双变换 UPS、锂电 UPS、飞轮 UPS、超级电容短时支撑 |
| 中高压配电/变压器/开关柜 | 美国、墨西哥、欧洲、中国、印度 | Eaton、Schneider、Siemens、ABB、GE Vernova/Prolec GE、Hitachi Energy、Hubbell、Powell、nVent、Rittal、Hyosung、Mitsubishi Electric | 变压器、MV/HV switchgear、busway、E-house、SF6-free 设备 |
| 微电网控制/保护 | 美国、欧洲 | Schneider、Siemens、Eaton、ABB、SEL、ETAP、GE Vernova、Emerson、Rockwell、Honeywell、Generac、Enchanted Rock、PowerSecure | EMS、SCADA、继保、孤岛控制、黑启动、网络安全 |
| EPC/电气施工 | 美国为主 | Quanta、MYR Group、EMCOR、MasTec、Kiewit、Black & Veatch、Burns & McDonnell、Fluor、Jacobs、AECOM、DPR、Turner | 人力、项目管理、变更单、采购能力决定交付 |

### 5.2 供给瓶颈

1. **燃气轮机 slot 和大型发电机**：110GW 级 backlog/slot reservation 表明 2027-2029 大机交付紧张。  
2. **发动机、alternator、控制柜和机组封装**：Caterpillar、Cummins、mtu、Generac 都在数据中心方向扩产，封装和测试能力会成为瓶颈。  
3. **SCR/催化剂/排放后处理**：NOx 和 CO 许可越来越严，后处理不仅是成本项，也是能否获批的门槛。  
4. **天然气基础设施**：firm gas、管线、调压站、压缩机、计量站决定燃气项目能否 24/7 运行。  
5. **中高压变压器和开关柜**：GE Vernova 单季数据中心电气订单 $2.4B 说明瓶颈已从 IT 设备外溢到电气设备。  
6. **BESS 消防、PCS 并网模型和保险**：UL 9540A、NFPA 855、本地消防审批、热失控隔离都会拉长周期。  
7. **微电网继保和控制人才**：孤岛、并网、黑启动、动态负载、短路电流变化需要电力系统工程师，不是普通 IT 机电团队可直接完成。  
8. **空气许可和社区接受度**：xAI 案例说明临时机组也难绕开许可；大型燃气项目会面临更强公众审查。  
9. **融资与承购合同**：重资产项目必须有 hyperscaler 长约、信用支持或 ratepayer protection 结构。  
10. **服务和备件**：燃机热部件、发动机大修、燃料电池堆替换、UPS 电池更换会变成长期运维瓶颈。

### 5.3 成本构成与价格传导

| 产品 | 单位成本区间 | 成本拆分 | 毛利决定因素 | 价格传导 |
|---|---:|---|---|---|
| 往复式燃气机组 turnkey | $1.0-1.8M/MW | 发动机/alternator 35-45%，封装/冷却/控制 15-25%，排放 8-15%，安装/EPC 20-35% | 交期、连续运行等级、冗余、排放、服务网络 | 通过设备涨价、加急费、O&M 长约传导 |
| 大型燃气/联合循环 | simple cycle $0.8-1.4M/MW；CCGT $1.2-2.2M/MW | 燃机/汽机/发电机 30-45%，BOP 25-35%，EPC 20-30%，燃气/电网接入 10-20% | slot、热效率、氢掺烧、服务长协、融资 | slot reservation、LTSA、EPC escalation |
| SOFC 燃料电池 | $3.5-6.0M/MW installed | 电堆 30-45%，功率模块/逆变 20-30%，气体处理 5-10%，安装 15-25%，服务准备 5-10% | 电堆寿命、产能、可用率、排放优势 | 高价值项目可按 time-to-power 和低排放溢价定价 |
| BESS 2-4h | $0.8-1.6M/MW 或 $200-400/kWh | 电芯 45-60%，PCS 15-25%，热管理/消防 8-15%，EMS 3-8%，EPC 10-20% | 电芯价格、PCS 响应、消防认证、并网模型 | 电芯价格部分传导，grid-forming 和项目风险另加价 |
| UPS/飞轮/超级电容 | $0.2-0.8M/MW | 功率模块 30-45%，储能介质 20-35%，控制/开关 10-20%，安装 10-20% | 可靠性认证、功率密度、维护周期 | 数据中心认证后溢价强，替换件和服务长尾 |
| 微电网控制/EMS | $0.05-0.3M/MW，复杂项目更高 | 软件/控制器 25-50%，继保/SCADA 20-35%，工程调试 25-40% | 算法、系统经验、认证、网络安全 | 项目越复杂，软件和调试费越能提价 |

## 6. 竞争格局与壁垒

### 6.1 市场结构和集中度

| 细分 | 头部集中度判断 | 头部玩家 | 结构特征 |
|---|---|---|---|
| 大型燃气轮机 | CR4 约 80%+ | GE Vernova、Siemens Energy、Mitsubishi Power、Ansaldo、Baker Hughes | 技术、服务网络、交期和融资能力决定份额 |
| 数据中心备用/往复式机组 | CR5 约 55-70% | Caterpillar、Cummins、Rolls-Royce mtu、Kohler、Generac、Wartsila、INNIO | 客户认证和本地服务极强，替换难 |
| SOFC 数据中心 | Bloom 在 AI 数据中心订单领先 | Bloom、FuelCell Energy、Doosan、Bosch、Plug Power | 产能和电堆寿命是第一壁垒 |
| BESS 系统 | CR10 约 50-65% | Tesla、Fluence、Wartsila、Powin、CATL、BYD、Sungrow、LG ES、Samsung SDI | 电芯规模与项目集成能力分层 |
| Grid-forming PCS | 中高集中 | EPC Power、SMA、Sungrow、Power Electronics、Nidec、Hitachi Energy、ABB、Tesla | 并网模型和控制算法壁垒高 |
| UPS/电力保护 | CR5 约 60% | Vertiv、Schneider、Eaton、ABB、Socomec、Piller | 数据中心认证和售后锁定 |
| 微电网 EMS/保护 | 分散但高端集中 | Schneider、Siemens、Eaton、ABB、SEL、ETAP、GE Vernova、Generac、Enchanted Rock、PowerSecure | 工程经验和网络安全比单一软件功能更重要 |
| 中高压电气设备 | 中高集中 | Eaton、Schneider、Siemens、ABB、GE Vernova/Prolec、Hitachi Energy、Hubbell、Powell、nVent、Rittal | 产能和认证稀缺，交期长 |

### 6.2 壁垒清单：为什么能定价

1. **技术壁垒**：燃气轮机热端、燃料电池堆、grid-forming 控制、继保定值、UPS 高可靠设计都需要多年验证；故障代价是整园区停机，客户不愿试错。
2. **规模壁垒**：大客户要 GW 级交付和备件，只有少数公司能全球供应、调试和维护。
3. **渠道和客户锁定**：数据中心客户认证周期长，进入 approved vendor list 后复购强。Generac 明确提到多个 hyperscale 认证进入最后阶段，这本身就是壁垒。
4. **认证标准**：UL、NFPA、IEEE、NERC/CIP、当地空气许可、并网规范、Tier/可用性标准都抬高小厂进入门槛。
5. **切换成本**：微电网控制、UPS、燃机 LTSA、燃料电池服务和 BESS EMS 都与运维数据绑定，替换不仅换设备，还要重新做模型、许可和调试。
6. **项目融资壁垒**：能拿到设备融资、slot reservation、EPC 保函、长期服务合同的供应商更容易进入 GW 项目。

### 6.3 价值捕获

长期最可能高 ROIC/高毛利的层级：

1. **微电网 EMS、grid-forming PCS、保护控制**：资产轻，软件和工程知识可复制，attach rate 随自备电源提升。
2. **燃机/发动机长期服务**：设备销售有周期性，LTSA、备件和大修是高毛利长尾。
3. **燃料电池电堆和模块**：如果 Bloom/Oracle 交付成功，电堆产能和寿命数据会形成强护城河。
4. **UPS/短时储能高端产品**：AI 负载对毫秒级功率质量要求更高，认证和可靠性可定价。
5. **已获电力/燃气/许可的园区开发权**：土地本身不稀缺，已获电力、燃气和环保许可的土地稀缺。

## 7. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点 1：自备电源从“临时过桥”变成“标准园区设计”

Bloom 2026 Power Report 调研显示数据中心领导者在降低对公用电网依赖，并预测未来更多园区走向 500MW/1GW 级别；Uptime Institute 2026 field report 则显示 2021-2025 年提出的 giant data center power 计划总计 **181GW**，其中北美 **144GW**，2025 提案中 off-grid 与 grid-plus-onsite 已占重要份额。[Bloom Power Report](https://investor.bloomenergy.com/press-releases/press-release-details/2026/Data-Centers-Plan-to-Reduce-Reliance-on-Grid-Finds-Bloom-Energys-2026-Power-Report/default.aspx)、[Uptime Institute](https://intelligence.uptimeinstitute.com/sites/default/files/2026-02/UI%20Field%20report%20194_Giant%20data%20center%20power%20plans%20reach%20extreme%20levels_0.pdf)

最可能放量：天然气机组、BESS、微电网 EMS、E-house、开关柜。

### 拐点 2：燃料电池被 Oracle 推入 GW 级

Oracle/Bloom 的 2.8GW master agreement 改变了市场对燃料电池规模上限的认知。Bloom Q1 2026 收入 **$751M**，同比大幅增长，product gross margin **34.3%**，说明至少在财务报表上已经不是小规模示范状态。[Bloom Q1](https://investor.bloomenergy.com/press-releases/press-release-details/2026/Bloom-Energy-Reports-Record-First-Quarter-2026-Results-and-Raises-Full-Year-2026-Guidance/default.aspx)

最可能放量：SOFC 模块、电堆、逆变器、燃气处理、微电网并联控制。

### 拐点 3：ratepayer protection 成为项目审批核心

Meta/Entergy 的协议明确 Meta 支付完整成本，并把客户节省、输电、BESS、核电增容、可再生资源打包。未来大型 AI 园区不是单纯“向电网申请负荷”，而是“自带资金给电力系统扩容”。

最可能放量：公用事业电气设备、输电 EPC、联合循环、BESS、客户侧专用变电站。

## 8. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点 1：Rubin/MI400/TPU8/Trainium3 推动机架功率再上台阶

2026 是 Blackwell Ultra 和 ASIC 起量，2027 是 HBM4、Rubin、MI400、TPU8 等把高密度 AI Factory 推到新一轮功耗台阶。园区电力不再只关心年用电量，还要关心瞬态功率、黑启动、N+2、并网扰动和液冷泵负载。

最可能放量：grid-forming BESS、飞轮/超级电容、MVDC/高压直流配电、液冷联动 EMS。

### 拐点 2：燃气项目从 slot reservation 进入建设确认

2026 已经抢燃机和发动机，2027 会看到更多 FID、EPC full notice to proceed、LTSA 和燃气管道合同。GE Vernova、Siemens、Mitsubishi、CAT、Cummins、mtu 的交期会决定真实上电节奏。

最可能放量：燃气轮机、电厂 EPC、SCR、燃气管线、压缩机、长期服务。

### 拐点 3：SMR/核电重启从“故事”进入可融资结构

NextEra Duane Arnold 目标 Q1 2029 前重启；Blue/GE 的 gas-plus-nuclear 模型把 2030 前燃气桥接和 2032 后核电接入结合。2027 若 FID 和许可推进顺利，核电不会贡献即时电量，但会贡献工程、slot、许可和融资价值。

最可能放量：核电工程服务、SMR 前期设计、汽轮机/发电机、长周期设备、核电站址数据中心 co-location。

## 9. 头部公司清单

### 9.1 发电设备

| 细分 | 公司 |
|---|---|
| 大型燃气轮机/联合循环 | GE Vernova、Siemens Energy、Mitsubishi Power、Ansaldo Energia、Baker Hughes、Solar Turbines、Kawasaki Heavy Industries |
| 往复式燃气机组 | Caterpillar、Cummins、Rolls-Royce mtu、Wartsila、INNIO Jenbacher、Kohler、Generac、Mitsubishi Heavy Industries Engine、MAN Energy Solutions、Yuchai、Weichai |
| 柴油/HVO 备用 | Caterpillar、Cummins、Rolls-Royce mtu、Kohler、Generac、Mitsubishi、Doosan Bobcat、FG Wilson、Aggreko、Himoinsa |
| 燃料电池 | Bloom Energy、FuelCell Energy、Doosan Fuel Cell、Plug Power、Ballard、Bosch SOFC、Ceres Power、Kyocera、Aisin |
| 核电/SMR | GE Vernova Hitachi BWRX-300、X-energy、Kairos Power、Oklo、NuScale、TerraPower、Westinghouse AP300/AP1000、Rolls-Royce SMR、Last Energy、Holtec、BWXT |
| 地热 | Fervo Energy、Ormat、Sage Geosystems、Eavor、Chevron New Energies、Baker Hughes、SLB |

### 9.2 储能、电力电子、微电网

| 细分 | 公司 |
|---|---|
| BESS 集成 | Tesla Energy、Fluence、Wartsila、Powin、CATL、BYD、Sungrow、LG Energy Solution、Samsung SDI、Saft、Nidec、Energy Vault |
| PCS / grid-forming inverter | EPC Power、SMA、Sungrow、Power Electronics、Nidec、Hitachi Energy、ABB、Tesla、Dynapower、Kehua、Sinexcel |
| UPS / 电力保护 | Vertiv、Schneider Electric、Eaton、ABB、Socomec、Legrand、Piller、Active Power、VYCON、Riello UPS、Huawei Digital Power、Delta Electronics |
| 飞轮/超级电容 | Piller、Active Power、VYCON、Temporal Power、Skeleton Technologies、Maxwell/Tesla、Eaton、ABB |
| 微电网 EMS/控制 | Schneider Electric、Siemens、Eaton、ABB、SEL、ETAP、GE Vernova、Emerson、Rockwell、Honeywell、Generac、Enchanted Rock、PowerSecure、AutoGrid、GridBeyond |
| 中高压配电/开关柜 | Eaton、Schneider、Siemens、ABB、GE Vernova/Prolec GE、Hitachi Energy、Hubbell、Powell Industries、nVent、Rittal、Hyosung、Mitsubishi Electric、Toshiba、Lucy Electric |

### 9.3 项目开发、EPC、园区能源

| 细分 | 公司 |
|---|---|
| 公用事业/IPP/能源开发 | NextEra Energy、Entergy、Constellation、Vistra、Talen Energy、NRG、AES、Invenergy、Duke Energy、Southern Company、Dominion、Exelon、AEP、Xcel、Enchanted Rock、PowerSecure、Twenty20 Energy、Base Electron、Fermi America |
| 数据中心开发/colo/neocloud | Oracle、OpenAI/Stargate、Meta、Google、Microsoft、AWS、CoreWeave、Crusoe、Applied Digital、Equinix、Digital Realty、QTS、Vantage、Stack、Aligned、DataBank、NTT Global Data Centers、Switch、Compass、CyrusOne |
| EPC/电气施工 | Quanta Services、MYR Group、EMCOR、MasTec、Kiewit、Black & Veatch、Burns & McDonnell、Fluor、Jacobs、AECOM、DPR Construction、Turner、Clark、Mortenson、Rosendin、Faith Technologies |
| 燃气基础设施 | Kinder Morgan、Williams、Energy Transfer、Enbridge、TC Energy、ONEOK、Baker Hughes、Chart Industries、Air Products、Linde |

## 10. 投资价值排序

### 10.1 2026-2027 弹性最高

1. **燃气发电设备和 slot**：GE Vernova、Siemens Energy、Mitsubishi、Baker Hughes、Caterpillar、Cummins、Rolls-Royce mtu。
2. **中高压电气设备**：Eaton、Schneider、ABB、Siemens、GE Vernova/Prolec、Powell、Hubbell、nVent、Rittal。
3. **BESS/PCS/微电网控制**：Generac/EPC、Tesla、Fluence、Wartsila、Powin、Sungrow、Schneider、Eaton、SEL、ETAP。
4. **燃料电池**：Bloom 是最直接标的，FuelCell Energy 和 Doosan 是潜在跟随。
5. **EPC/输配电施工**：Quanta、MYR、EMCOR、MasTec、Kiewit 等受益于项目数量和复杂度。

### 10.2 确定性最高

1. **备用电源和 UPS**：所有 AI 数据中心都需要，不依赖某单一自备发电路线。
2. **开关柜、变压器、busway、E-house**：不论电来自电网、燃气、燃料电池还是核电，都需要。
3. **微电网控制和保护**：现场发电越多，控制价值越高。
4. **发电设备服务合同**：设备装机后，长协服务和备件是更稳的利润池。

### 10.3 最大风险

1. AI 算力投资节奏低于极度乐观假设，导致重资产项目融资放慢。
2. 地方空气许可、社区反对和环境诉讼延误现场燃气项目。
3. 天然气价格和 firm transportation 成本上行，侵蚀电价优势。
4. 燃机/发动机/变压器产能不能按期扩张，导致订单转为延期。
5. 燃料电池 GW 级交付若出现质量或服务问题，会影响估值和客户扩散。

## 11. 核心预测表

| 指标 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026-05 到 2027-05 全球 AI 数据中心自备发电/微电网订单池 | $120-210B | $210-360B | $360-600B |
| 2027-05 到 2028-05 全球 AI 数据中心自备发电/微电网订单池 | $220-420B | $420-750B | $750B-1.2T |
| 2027 前可见新建/专用/现场电源 pipeline | 25-45GW | 45-80GW | 80-140GW |
| 2028 前可见新建/专用/现场电源 pipeline | 50-90GW | 90-160GW | 160-260GW |
| AI 新建园区采用现场/专用电源的 MW 渗透率 | 2026 20-35%，2028 35-50% | 2026 30-45%，2028 50-70% | 2026 40-55%，2028 70%+ |
| 燃气路线在现场/专用电源中占比 | 60-75% | 65-80% | 70-85% |
| 燃料电池在现场/专用电源中占比 | 3-8% | 8-15% | 15-25% |
| BESS/微电网控制 attach rate | 40-60% 到 70-85% | 55-75% 到 80-90% | 70-85% 到 90%+ |

极度乐观情景成立的关键前提：AI token 需求继续吞掉所有新增电力；hyperscaler 愿意用长约锁电和锁设备；燃机、发动机、燃料电池、BESS、变压器和 EPC 产能都能扩；地方监管允许“客户自付、不涨居民电价”的模式快速复制。

## 12. 主要来源

| 来源 | 用途 |
|---|---|
| [Caterpillar / AIP / Boyd CAT 2GW alliance](https://www.caterpillar.com/en/news/corporate-press-releases/h/aip-boyd-cat.html) | 2GW 往复式燃气机组订单、交付节奏、BESS、8GW 远期目标 |
| [Bloom Energy / Oracle 2.8GW partnership](https://www.bloomenergy.com/news/bloom-energy-and-oracle-expand-strategic-partnership-to-deploy-up-to-2-8-gw-to-accelerate-ai-infrastructure-build-out/) | 燃料电池 GW 级订单验证 |
| [Bloom Energy Q1 2026 results](https://investor.bloomenergy.com/press-releases/press-release-details/2026/Bloom-Energy-Reports-Record-First-Quarter-2026-Results-and-Raises-Full-Year-2026-Guidance/default.aspx) | Bloom 收入、毛利、财务表现 |
| [Bloom 2026 Data Center Power Report press release](https://investor.bloomenergy.com/press-releases/press-release-details/2026/Data-Centers-Plan-to-Reduce-Reliance-on-Grid-Finds-Bloom-Energys-2026-Power-Report/default.aspx) | 数据中心降低电网依赖、GW 园区趋势 |
| [Entergy Louisiana / Meta agreement](https://www.entergy.com/news/entergy-louisiana-announces-a-new-agreement-with-meta-that-will-deliver-an-additional-2b-in-customer-savings) | Meta 5.2GW 新燃气电厂、输电、BESS、核电增容、2.5GW 可再生资源 |
| [Babcock & Wilcox news page](https://www.babcock.com/home/about/corporate/news?f=ec425f1b-cde7-46e4-8502-965836e95e08) | B&W/Base Electron/Applied Digital $2.4B、1.2GW AI Factory 电源合同 |
| [Baker Hughes / Twenty20 Energy](https://www.nasdaq.com/press-release/baker-hughes-receives-gas-turbine-order-twenty20-energy-power-us-data-center) | 250MW 燃气轮机订单与多 GW 合作线索 |
| [GE Vernova Q1 2026 results](https://www.gevernova.com/sites/default/files/gev_webcast_pressrelease_04222026.pdf) | 燃气轮机 backlog/slot reservation、电气设备数据中心订单 |
| [Blue Energy / GE Vernova gas-plus-nuclear](https://www.prnewswire.com/news-releases/blue-energy-and-ge-vernova-accelerate-gas-plus-nuclear-approach-for-powering-american-communities-and-fueling-global-ai-leadership-302761986.html) | 2.5GW gas-plus-nuclear、BWRX-300、7HA.02 slot、时间表 |
| [Uptime Institute 2026 Giant Data Center report](https://intelligence.uptimeinstitute.com/sites/default/files/2026-02/UI%20Field%20report%20194_Giant%20data%20center%20power%20plans%20reach%20extreme%20levels_0.pdf) | 181GW giant data center proposed power、北美占比、off-grid/onsite 趋势 |
| [Vertiv Frontiers 2026](https://www.vertiv.com/48d902/globalassets/content---assets-2025/documents/vertiv-frontiers-2026-report-en-gl-web.pdf) | AI 数据中心 self-generation、燃气、BESS、DC microgrid、SMR 观察 |
| [Generac / EPC Power data center energy solutions](https://investors.generac.com/news-releases/news-release-details/generac-and-epc-power-deploy-fully-integrated-energy-solutions) | BESS、PCS、ARC Controller、grid-forming、AI load smoothing |
| [Cummins Q1 2026 results](https://investor.cummins.com/news/detail/694/cummins-delivered-strong-operating-results-and-returned) | 数据中心备用电源需求、Power Systems 创纪录、2026 指引上调 |
| [Generac Q1 2026 results](https://www.globenewswire.com/de/news-release/2026/04/29/3283534/0/en/generac-reports-first-quarter-2026-results.html) | C&I 增长、数据中心 backlog、hyperscaler 认证、Enercon 收购 |
| [Rolls-Royce 2025 annual report](https://www.rolls-royce.com/~/media/Files/R/Rolls-Royce/documents/annual-report/2026/rr-plc-annual-report-2025.pdf) | mtu 数据中心份额、订单、fast-start gas genset |
| [NextEra Investor Conference 2025](https://www.investor.nexteraenergy.com/~/media/Files/N/NEE-IR/news-and-events/events-and-presentations/2025/2025-12-08%20NextEra%20Energy%20Investor%20Conference%20vF.pdf) | 15GW by 2035、30GW upside、data center hubs |
| [NextEra Q1 2026 script](https://www.investor.nexteraenergy.com/~/media/Files/N/NEE-IR/reports-and-fillings/quarterly-earnings/2026/Q1%202026/Q1%202026%20Earnings%20Script%20vF.pdf) | 4GW 储能 origination、110GW 储能 pipeline、9.5GW large load 项目、Duane Arnold |
| [Homer City / Kiewit / GE Vernova](https://www.nasdaq.com/press-release/homer-city-redevelopment-and-kiewit-announce-countrys-largest-natural-gas-powered) | 4.5GW 天然气 AI campus、7 台 GE 7HA.02、2026 交付、2027 发电 |
| [Fermi America 6GW clean air permit](https://www.prnewswire.com/news-releases/fermi-america-secures-final-6gw-clean-air-permit-from-the-texas-commission-on-environmental-quality-tceq-for-worlds-largest-11-gw-private-power-grid-302697603.html) | Project Matador、6GW 许可、11GW behind-the-meter private grid、2GW 长周期资产 |
| [Siemens / Eaton modular onsite data center power](https://www.eaton.com/us/en-us/markets/data-centers/eaton-and-siemens-energy.html) | 500MW 模块化 onsite power、N+2、BESS、减少部署时间 |

# 行业调研：【液冷小组件与流体控制】

截至日期：2026-05-08  
研究口径：本报告研究 AI 计算中心/AI Factory 中与液冷相关的“小组件与流体控制”收入池，覆盖冷板、冷板回路、CDU、manifold/二次侧管路、快接头、软管/接头、泵阀、板式换热器、传感器、漏液检测、过滤与冷却液/水处理，也包括早期放量的浸没与两相直触技术。除特别说明外，市场规模为全球 AI 数据中心项目的订单/发货收入池，美元名义值，不等同于单一厂商财务收入。

## 0. 结论先行

1. 2026 年最确定的技术路径是 **单相 direct-to-chip 冷板 + 液液 CDU + OCP/UQD 标准化快接头 + 机架/列级 manifold + 传感器/漏液检测**。液气 CDU、后门换热器仍用于存量机房改造和残余热负载，浸没式与两相直触会增长，但 2026 主流不是它们。
2. 2026 年行业需求的拐点不是“液冷是否有效”，而是 **GB300/GB200、TPU/Trainium、MI350/MI400、Maia/MTIA 等机架级平台把液冷从工程选项变成交付前提**。NVIDIA GB300 NVL72 官方页面已明确为 fully liquid-cooled rack-scale 架构；Vera Rubin NVL72 与 Vera CPU Rack 也延续液冷机架路线。
3. 供给侧正在快速工业化：Ecolab 2026 年 3 月宣布以约 **$4.75B** 收购 CoolIT，披露 CoolIT 未来 12 个月销售约 **$550M**，并点名 CDU、冷板、liquid loops、rack manifolds；Schneider/Motivair 披露 CDU 组合从 **105kW 到 2.5MW**，Motivair 在美国 Buffalo、意大利、印度扩产并把制造输出提升至约 3 倍；Vertiv 2025 年底 backlog 达 **$15B**、Q4 有机订单同比 **+252%**；Delta 2026 年 3 月称 **3MW L2L CDU 已开始出货**。
4. 窄口径第三方预测相对保守：Dell'Oro 2026 年 1 月称全球 data center liquid cooling manufacturer revenue 到 2029 年接近 **$7B**。本报告在用户要求的乐观 AI 基建假设下采用更宽订单口径：未来 12 个月液冷小组件与流体控制收入池基准 **$10-18B**，乐观 **$16-28B**，极度超预期 **$26-45B**；未来 24 个月累计基准 **$25-45B**，乐观 **$45-78B**，极超 **$80-140B**。两者差异来自口径：前者偏设备厂商净收入，后者包含服务器内冷板/回路、机架级系统集成、现场流体控制与项目订单提前。
5. 价值捕获最强的环节：高可靠冷板/冷板回路、2MW+ CDU、OCP 兼容低压降快接头、泵阀传感器控制、冷却液与水质监测/服务。长期 ROIC 最强的不是简单铜件加工，而是 **被 GPU/服务器 OEM 和 hyperscaler 验证锁定、能量产且现场事故率极低的系统级组件平台**。

## 1. 需求背景：2026 AI 芯片路线如何把液冷小组件推成刚需

### 1.1 项目已有 AI 芯片路径锚点

项目内 `ai_chip_research_2026_2027.md` 已给出 2026-2027 年 AI 芯片/平台出货与技术路径判断。对液冷组件最关键的 10 个平台如下：

| 排名 | 芯片/平台 | 2026-2027 液冷含义 |
|---:|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | 2026 主力，GB300 NVL72 是 fully liquid-cooled rack-scale 架构；冷板、CDU、manifold、快接头、液冷整柜成为交付绑定件。 |
| 2 | AWS Trainium2 | Project Rainier 近 50 万颗级、Anthropic 目标 >100 万颗，拉动 AWS 自研机架与二次侧液冷工程。 |
| 3 | Google TPU v7 Ironwood | TPU 自用+云+Anthropic 扩容，Google/OCP Project Deschutes 2MW CDU 标准会外溢到供应链。 |
| 4 | NVIDIA B200/GB200 Blackwell | GB200 NVL72 大量存量订单延续，2026 继续拉动冷板和 CDU；GB300 之前的成熟放量平台。 |
| 5 | Huawei Ascend 910C/950PR/950DT | 中国超节点/智算中心密度上行，国产冷板、CDU、管路、工质和漏液检测受益。 |
| 6 | Cambricon MLU 590/690 | 国内 OAM/集群规模放大，风冷到风液/冷板液冷迁移。 |
| 7 | AMD MI350X/MI355X/MI350P | 2026 AMD 最确定放量平台，PCIe/UBB 多形态，需要液冷选项和企业改造型 CDU。 |
| 8 | AWS Trainium3 | 144 颗 Trainium3 UltraServer 高密度 scale-up，2026-2027 进入液冷刚需。 |
| 9 | Meta MTIA 300/400/450/500 | Meta/Broadcom >1GW 首期与多 GW 路线提高推理 ASIC 机架液冷渗透。 |
| 10 | Microsoft Maia 200 | Azure 推理 ASIC，官方披露闭环液冷 HEU；自研芯片不减少液冷需求，反而要求更深定制。 |

补充：AMD MI400/MI455X/Helios 在项目内排第 12，但对液冷更关键。72 GPU rack、HBM4、48V/高压供电和 rack-scale 互连意味着 2027 会成为液冷高端增量弹性源。

### 1.2 公开一手信号

| 来源 | 关键事实 | 对液冷组件的含义 |
|---|---|---|
| [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) | 72 Blackwell Ultra GPU + 36 Grace CPU，fully liquid-cooled rack-scale architecture。 | 冷板、CDU、manifold、QDs 不再是选配，而是平台级 BOM/交付件。 |
| [NVIDIA Vera Rubin 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | Vera Rubin POD 包含 40 racks、1,152 Rubin GPUs，指出常用冷却液可为去离子水或 PG25，并提到闭环可低维护运行多年。 | PG25/DI water、低污染管路、流体维护和监测成为标准设计变量。 |
| [NVIDIA Vera Rubin 新闻稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | Vera CPU Rack、Groq LPX Rack 等均为 liquid-cooled/MGX rack 形态，2026 H2 可用。 | 2026 下半年起，液冷需求从 GPU rack 扩展到 CPU rack、LPU rack、storage/context rack。 |
| [Dell PowerEdge XE8712 GB200](https://infohub.delltechnologies.com/en-us/p/poweredge-xe8712-with-nvidia-gb200-a-high-density-foundational-server-for-rack-scale-ai-2/) | Dell 明确 GB200 rack-level server 使用 direct liquid cooling。 | OEM 服务器交付会内含冷板/loop/现场连接件，压缩纯设备商交付窗口。 |
| [HPE 2026 AI factory with NVIDIA](https://www.hpe.com/us/en/newsroom/press-release/2026/03/hpe-unveils-next-generation-ai-factory-and-supercomputing-advancements-with-nvidia.html) | HPE Rubin 系统结合液冷集成、服务和数据中心设计能力；称 HPE 直接液冷经验超过 50 年、专利超过 300 件。 | 机架液冷不只是部件销售，还要捆绑 site readiness、commissioning、leak detection、thermal monitoring。 |
| [Supermicro FY26 deck](https://ir.supermicro.com/files/doc_financials/2026/q1/FQ126-SMCI-Earnings-Deck.pdf) | 目标 FY26 年底 6,000 racks/月产能，其中 3,000 DLC racks/月；150kW racks 已批量出货，250/500kW 即将跟进。 | 整机厂的液冷产能本身成为竞争变量，DLC rack 放量会外溢至快接头、manifold、CDU。 |

## 2. 2026 机遇、挑战与技术路线

### 2.1 机遇

| 机遇 | 2026 影响 |
|---|---|
| 100kW+ rack 成为高端 AI 常态 | GB200/GB300、Rubin、MI400、TPU/Trainium 等平台把传统风冷推到极限，冷板与 CDU 的 attach rate 快速上升。 |
| 从“服务器冷却”升级为“AI Factory 流体系统” | 数据中心需要 TCS/FWS、CDU、manifold、漏液检测、水质监测、数字孪生和运维服务，价值池从铜件扩大到系统级流体控制。 |
| 标准化加速 | OCP UQD/LQC、Project Deschutes 2MW CDU、Open Rack V3 等让多供应商接入成为可能，行业从项目制转向平台制。 |
| 订单提前 | 电力、机电与冷却长交期迫使客户提前锁定 CDU、板换、快接头、阀泵、服务队伍；优质厂商会看到 backlog 和预付款。 |
| M&A 抬高行业估值锚 | Ecolab/CoolIT、Schneider/Motivair、Trane/LiquidStack、Vertiv/CoolTera/PurgeRite 说明传统水处理、HVAC、关键基础设施公司正在买入液冷核心能力。 |

### 2.2 挑战

| 挑战 | 为什么会卡订单 |
|---|---|
| 冷板热阻、流阻与良率 | GB300/Rubin/MI400 的热流密度高，冷板微通道需要低热阻和低压降；焊接、钎焊、skiving/CNC、清洁度和 100% leak/flow test 会限制爬坡。 |
| 快接头可靠性 | 单个机架可能有数百个连接点，任何滴漏/气泡/误插都可能造成停机；OCP 兼容、低压降、blind-mate 误差容忍和密封材料是核心。 |
| 水质与污染 | 冷板微通道对颗粒、腐蚀和生物膜敏感，冲洗、过滤、PG25/DI water 配方、在线监测会成为交付的一部分。GF 2026 白皮书明确把 coolant purity 和 corrosion resistance 列为管路战略设计变量。 |
| 存量机房改造 | 很多机房没有 FWS/TCS、地板承重、二次侧管路或热拒绝能力；L2A CDU 与 RDHx 能过渡，但无法完全释放 500kW rack 潜力。 |
| 现场交付人才 | 冷却系统要在带电、带水、满负荷 IT 设备附近运行，安装、冲洗、压力测试、commissioning、漏液定位、维护 SOP 缺一不可。 |
| 标准碎片化 | NVIDIA、Google/OCP、AMD/UALink、AWS/Trainium、Microsoft/Meta 自研架构都会带来接口与验证差异，供应商需要多平台认证。 |
| PFAS 与两相流体 | 3M 已在 2025 年底退出 PFAS 制造，Novec/Fluorinert 体系不再是长期确定解；PFAS-free 两相/浸没流体仍需材料兼容和可靠性验证。 |

### 2.3 当前在用技术

| 技术路线 | 2026 状态 | 典型组件 | 适用场景 |
|---|---|---|---|
| 单相 direct-to-chip 冷板液冷 | 主流放量 | 冷板、TIM、GPU/CPU cold plate loop、UQD/UQDB、manifold、CDU、泵阀传感器 | 新建 GB200/GB300、MI350、TPU、Trainium、Maia/MTIA 机架。 |
| 液液 CDU, L2L | 新建高密机房主流 | 0.3-3MW CDU、板换、双泵/N+1、过滤、水质监测 | 有 facility water loop 的新建 AI Factory。 |
| 液气 CDU, L2A | 过渡/改造 | rack/row CDU、风扇、散热排、局部循环 | 存量空气机房、pilot cluster、边缘/企业 AI。 |
| RDHx 后门换热器 | 辅助放量 | rear door heat exchanger、风扇/无风扇、管路 | 捕获 CPU/内存/网络/PSU 残余热，降低机房空调负担。 |
| 浸没式单相 | 小规模商业 | 槽体、介电液、泵、板换、过滤 | 边缘、HPC、空间受限、特殊高密度机房。 |
| 两相直触/浸没 | 早期导入 | dielectric cold plate、蒸发/冷凝回路、end-of-row CDU | 未来 2kW-4kW+ 芯片、缺水/极端密度场景。 |
| 智能流体控制 | 由附加项转刚需 | 流量/压差/温度/电导率/颗粒传感器、阀阵列、DCIM | 大规模液冷机群的预测性维护和能效优化。 |

## 3. 新技术成熟与放量时间预测

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|
| 单相冷板 direct-to-chip | 2026 已成熟，GB200/GB300、MI350、TPU、Trainium 大规模使用；2027 成为 >100kW AI rack 默认方案。 | 2026 H2 伴随 GB300 和 ASIC racks 快速放量，2027 attach rate 达 70%+。 | 2026 H2 就对 80kW+ AI rack 接近强制配置，2027 新建高端 AI rack 90%+ 使用。 |
| L2L CDU, 1-3MW | 2026 1-2MW CDU 放量；2027 Project Deschutes 类 2MW 标准进入主流。 | 2026 H2 2MW/3MW CDU 成为大客户标配，2027 开始平台化采购。 | 2026 Q4 起 2MW+ CDU 紧缺，2027 多 GW 园区按标准 CDU 模块复制。 |
| L2A CDU | 2026 是存量改造窗口，2027 增速降于 L2L。 | 如果存量机房抢时间，2026-2027 仍高增长。 | 在电力/土建慢于 GPU 交付时，L2A 成为“先上电再优化”的应急方案。 |
| OCP UQD/LQC, blind-mate QD | 2026 标准化加速；2027 high-flow/low-pressure-drop 成主流。 | 2026 H2 开始由头部 OEM 统一接口，快接头 ASP 和毛利维持高位。 | 连接器成为显性瓶颈，低压降、盲插、微型光模块 QD 出现结构性溢价。 |
| 高级微通道/喷射/生成式冷板 | 2026 高端样品与定制，2027 进入 2kW+ 芯片批量。 | 2026 H2 在 GB300/Rubin/MI400 供应链提前锁定，2027 大规模导入。 | 2027 前即被 4kW 级 Feynman/后续芯片设计拉入 NPI，冷板供应商估值按半导体设备逻辑重估。 |
| 两相 direct-to-chip | 2026 试点，2027 低个位数渗透。 | 2027 在缺水、高温回水、极端密度场景形成 5-10% 渗透。 | 2027 成为 Rubin Ultra/MI500/未来 Feynman rack 的提前配置，供应链提前扩产。 |
| 浸没式 | 2026 边缘/HPC/特殊场景，主流 hyperscaler 慎用。 | PFAS-free 单相流体通过更多验证后，2027 渗透率 5-8%。 | 若 PFAS-free 两相流体验证成功且 rack 密度快速迈向 500kW-1MW，2027 开始进入 hyperscaler 小规模 pod。 |
| 液冷交换机/光模块 | 2026 早期；2027 随 1.6T/CPO/高功耗交换芯片上量。 | 2027 网络侧热管理成为新增价值池，Mini QD 与板级冷却增长。 | 2027 1.6T/3.2T、CPO 和高功耗 switch trays 使“计算+网络全液冷”提前。 |
| 数字孪生/自适应液冷控制 | 2026 附加价值，2027 与 DCIM/AI Mission Control 结合。 | 大客户把温度/压差/水质数据接入 AI factory orchestration，服务收入占比上升。 | 流体系统变成高毛利 SaaS/服务合同，降低硬件周期性。 |

## 4. 市场规模总锚：三种口径

| 口径 | 2026/未来 12 个月读数 | 含义 |
|---|---:|---|
| 保守第三方设备收入 | Dell'Oro 预计 data center liquid cooling 到 2029 接近 **$7B manufacturer revenue**。 | 偏窄设备厂商收入，不完全覆盖服务器内 cold plate loop、OEM 整柜集成、现场工程和订单提前。 |
| 项目既有美国 AI DC 冷却订单池 | `AI数据中心建设规模...` 中冷却与热管理 2026 务实 **$25-45B**，2027 **$40-70B**；乐观 2026 **$35-65B**，2027 **$65-105B**。 | 广义冷却/热管理，包含冷却塔、冷机、CDU、冷板、二次侧和工程。 |
| 本报告液冷小组件与流体控制池 | 未来 12 个月基准 **$10-18B**，乐观 **$16-28B**，极超 **$26-45B**。 | 聚焦冷板、CDU、manifold、QDs、泵阀传感器、换热器、工质和服务，不含大型建筑/HVAC 全额。 |

本报告的大胆乐观假设：2026 美国 AI 可交付新增 IT 负载按项目既有务实/乐观区间，且高密 AI rack 中液冷 attach rate 快速提升；对于看不到外部售价的自用 ASIC 项目，以“每 kW 液冷组件价值量”估算。基准情景下，80kW+ 新建 AI rack 的冷板液冷渗透率从 2026Q2 的约 55-65% 升至 2027 的 70-80%；乐观情景达 80-90%；极超情景中，100kW+ rack 近乎全部液冷。

## 5. 已开始放量的关键产品

### 5.1 放量产品总表

市场规模为从 2026-05-08 起的未来窗口订单/发货收入池，单位为十亿美元。B/O/X = 基准/乐观/极度超预期乐观。

| 产品/细分技术 | 放量证据 | 未来 3 个月 | 未来 1 年 | 未来 2 年累计 | 渗透率路径 | 毛利率预测 |
|---|---|---:|---:|---:|---|---|
| GPU/CPU 冷板与 cold plate loop | Boyd 宣布已向 hyperscaler 交付 **500 万片**液冷冷板；CoolIT 称每月生产 **1 万+ server coldplate loops**；Delta 展示 **6,200W** 冷板。 | B 0.7-1.2 / O 1.1-1.8 / X 1.8-3.0 | B 3.2-5.5 / O 5.0-8.5 / X 8.0-14.0 | B 8-15 / O 14-25 / X 25-45 | 高端 AI rack 2026 45-65%，2027 65-80%，2028 75-90%。 | B 22-32%，O 28-40%，X 35-50%；定制高热流冷板溢价最高。 |
| CDU, L2L/L2A, rack/row/in-row | Delta **3MW L2L CDU 已 shipping**；Schneider/Motivair CDU 覆盖 **105kW-2.5MW**；Nidec 2MW in-row CDU 支持 GB200/GB300。 | B 0.5-1.0 / O 0.9-1.6 / X 1.6-2.8 | B 2.3-4.2 / O 4.0-7.0 / X 7.0-12.0 | B 5.5-10 / O 10-18 / X 18-35 | 新建高密优先 L2L；改造使用 L2A。2027 2MW+ CDU 标准化。 | B 20-32%，O 28-40%，X 35-48%；2MW+、低 ATD、冗余泵、服务绑定毛利更高。 |
| Manifold、二次侧管路、rack plumbing | CoolIT 每月 **1,000+ rack manifolds**；Envicool、Boyd、GF 均把 manifold/二次侧管路列入全链条方案。 | B 0.25-0.55 / O 0.45-0.85 / X 0.8-1.5 | B 1.3-2.4 / O 2.2-4.0 / X 4.0-7.0 | B 3.3-6.0 / O 6-11 / X 11-20 | 从项目定制转向标准 rack manifold；聚合到 CDU/整柜供应商。 | B 18-30%，O 25-38%，X 32-45%；现场预制化和低污染材料提高议价。 |
| UQD/UQDB/LQC 快接头、软管、接头 | CEJN 披露 UQD 四尺寸、10 bar；LQC 19mm、12 bar；Stäubli 2026 LQD 在 UQD04 尺寸实现接近 UQD08 流量并大幅降低压损；CPC Everis UQD 主打 hyperscale volume。 | B 0.20-0.45 / O 0.40-0.75 / X 0.75-1.4 | B 0.9-1.8 / O 1.6-3.0 / X 3.0-5.5 | B 2.2-4.5 / O 4.5-8.5 / X 8.5-16 | OCP 兼容从“加分项”变成“采购门槛”；blind-mate 在 2027 放量。 | B 35-50%，O 45-60%，X 55-70%；低压降、零滴漏、认证件最有定价权。 |
| 泵、阀、传感器、过滤、漏液检测 | Danfoss 2026 强化 CDU 生态组件；Xylem/Flojet 强调 D5/DDC/diaphragm pump；Nidec 强项是高性能泵和响应控制。 | B 0.22-0.50 / O 0.45-0.85 / X 0.80-1.5 | B 1.0-2.0 / O 1.8-3.5 / X 3.5-6.5 | B 2.5-5.0 / O 5-9 / X 9-17 | 每 rack 从温度控制走向压差/流量/电导率/颗粒/漏液闭环。 | B 28-42%，O 35-52%，X 45-65%；高可靠传感+控制软件可服务化。 |
| 板式换热器、skid、冷却液处理 | Danfoss B3-260C 支持 CDU、最高 **1MW**、约 **2K LMTD**；Alfa Laval FreeWaterLoop 集成泵、换热、过滤；Boyd ROL2300/4000 与 Alfa Laval 合作。 | B 0.30-0.70 / O 0.60-1.1 / X 1.1-2.0 | B 1.4-2.8 / O 2.5-5.0 / X 5.0-9.0 | B 3.5-7.0 / O 7-14 / X 14-25 | CDU 容量上移使板换/过滤/水处理从隐性件变成性能瓶颈。 | B 25-38%，O 32-45%，X 40-55%；低 LMTD 与低压降溢价高。 |
| 冷却液、缓蚀剂、水质监测与流体服务 | NVIDIA 技术博客提到 DI water/PG25 闭环；Ecolab 3D TRASAR 直触液冷监测；Envicool SoluKing 全链条工质。 | B 0.10-0.25 / O 0.20-0.45 / X 0.40-0.8 | B 0.45-0.9 / O 0.8-1.6 / X 1.6-3.2 | B 1.0-2.4 / O 2.4-5.0 / X 5-10 | 2026 从一次性耗材转为在线监测/补液/维护合同；2027 服务 attach rate 快升。 | B 35-55%，O 45-65%，X 55-75%；化学+数据服务毛利最强。 |
| RDHx/残余热捕获 | Schneider/Motivair、Vertiv、Lenovo/HPE 等均把 RDHx/air-liquid hybrid 纳入方案。 | B 0.15-0.35 / O 0.30-0.60 / X 0.60-1.1 | B 0.7-1.4 / O 1.3-2.5 / X 2.5-4.5 | B 1.8-3.5 / O 3.5-6.5 / X 6.5-12 | 随 direct-to-chip 只能捕获芯片热，RDHx 负责 PSU/内存/网络/残余热。 | B 20-32%，O 25-38%，X 32-45%。 |

### 5.2 价格与单位价值量假设

| 单位 | 基准 | 乐观 | 极超 |
|---|---:|---:|---:|
| 高密 AI rack 液冷组件价值量，不含 GPU/服务器主体 | $120k-250k/rack | $220k-450k/rack | $450k-900k/rack |
| 100kW rack 对应组件价值量 | $1,200-2,500/kW | $2,200-4,500/kW | $4,500-9,000/kW |
| 2MW CDU 单台项目价，含控制/服务但不含大型冷源 | $250k-600k | $500k-1.0M | $0.9M-1.8M |
| 单 GPU/CPU 冷板 loop 价值量 | $150-450 | $300-800 | $700-1,500 |
| 单个高端快接头/盲插连接器 | $30-120 | $80-250 | $180-500 |

单位价值量会随标准化下降，但 2026-2027 大客户抢交付时，瓶颈产品反而具备阶段性涨价能力。极超情景假设高端 rack 不再按传统冷却 BOM 议价，而按“上电确定性/停机风险降低”议价。

## 6. 在研与未来快速增长技术

| 在研/早期产品 | 当前阶段与一手线索 | 未来 3 个月 | 未来 1 年 | 未来 2 年累计 | 渗透率路径 | 毛利率预测 |
|---|---|---:|---:|---:|---|---|
| Project Deschutes/OCP 2MW CDU 与 3MW CDU 平台 | OCP Project Deschutes 规范定义 2MW next-gen CDU、3°C ATD、80 PSI；Delta 3MW L2L CDU shipping；Nidec/Google OCP 规格原型。 | B 0.2-0.6 / O 0.5-1.0 / X 1.0-2.0 | B 1.0-2.5 / O 2.0-5.0 / X 5.0-10 | B 4-10 / O 9-20 / X 20-45 | 2026 标准导入，2027 成大规模 AI pod 的默认 CDU 单元。 | B 25-38%，O 35-50%，X 45-60%。 |
| 4kW+ 高热流冷板、喷射/3D 微结构 | CoolIT 4000W coldplate 技术简报面向 GB300/后续 2kW+ 芯片；Frore LiquidJet 面向未来 4.4kW 级芯片；2026 论文显示生成式冷板可显著降低热点温度。 | B 0.08-0.25 / O 0.2-0.5 / X 0.5-1.0 | B 0.8-1.8 / O 1.5-3.5 / X 3.5-8.0 | B 3-7 / O 7-15 / X 15-35 | 2026 NPI，2027 随 Rubin/MI400/TPU8 进入量产。 | B 35-50%，O 45-60%，X 55-75%。 |
| 两相 direct-to-chip, waterless DLC | ZutaCore HyperCool 两相直触；Trane 收购 LiquidStack 扩展 direct-to-chip/immersion；PFAS 监管推动非水/非 PFAS 体系。 | B 0.03-0.15 / O 0.10-0.35 / X 0.35-0.9 | B 0.3-0.9 / O 0.8-2.0 / X 2.0-5.0 | B 1.5-4 / O 4-10 / X 10-28 | 2026 试点，2027 高密/缺水场景放量，2028 可能进入主流 rack 评估。 | B 40-55%，O 50-68%，X 65-80%；专利与流体壁垒强。 |
| PFAS-free 浸没流体与浸没槽 | 3M 已在 2025 年底完成 PFAS 制造退出；LiquidStack、Submer、GRC、Engineered Fluids 等推动单相浸没，PFAS-free 两相仍在验证。 | B 0.03-0.12 / O 0.10-0.30 / X 0.30-0.8 | B 0.2-0.7 / O 0.6-1.6 / X 1.6-4.0 | B 0.8-2.5 / O 2.5-7 / X 7-20 | 2026 特殊场景；2027 如果材料兼容/保修通过，渗透率进入 5% 附近。 | B 35-55%，O 45-65%，X 60-80%。 |
| 液冷交换机、CPO/光模块冷却、Mini QD | Stäubli 提到与 Ciena 开发 Mini QD；NVIDIA Spectrum-6/SPX 与 CPO 方向使网络侧散热上升。 | B 0.02-0.08 / O 0.06-0.20 / X 0.20-0.6 | B 0.2-0.7 / O 0.6-1.8 / X 1.8-5.0 | B 1.2-3.5 / O 3.5-9 / X 9-25 | 2026 工程导入，2027 随 1.6T/CPO 放量。 | B 40-55%，O 50-65%，X 60-78%。 |
| 负压/漏液抑制、智能漏液预测 | Chilldyne 类负压液冷、Ecolab/Envicool/Vertiv 监测服务、2025-2026 论文推进 AI leak forecasting。 | B 0.04-0.12 / O 0.10-0.30 / X 0.30-0.7 | B 0.3-0.8 / O 0.7-1.8 / X 1.8-4.5 | B 1.2-3 / O 3-8 / X 8-18 | 2026 被大客户纳入风险控制；2027 服务合同化。 | B 45-60%，O 55-70%，X 65-80%。 |
| 热回收/高温水/无冷机 AI DC | Alfa Laval FreeWaterLoop、GF polymer piping、Danfoss CDU 生态、Motivair chillerless 讨论。 | B 0.05-0.20 / O 0.15-0.45 / X 0.45-1.0 | B 0.4-1.2 / O 1.0-3.0 / X 3.0-8.0 | B 2-5 / O 5-13 / X 13-35 | 2026 欧洲/北美新园区试点；2027 与 PUE、水权、热回收政策联动。 | B 25-40%，O 35-50%，X 45-60%。 |

## 7. 供给侧：产能结构、瓶颈、成本与价格传导

### 7.1 主要产能结构

| 区域 | 公司/能力 | 竞争要点 |
|---|---|---|
| 北美 | CoolIT/Ecolab、Motivair/Schneider、Vertiv、Boyd、Parker/CPC、Xylem、nVent、Modine、Eaton | 最接近 hyperscaler 与 NVIDIA/AMD OEM 验证，服务网络强，能拿高端系统和长期服务合同。 |
| 台湾 | Delta、Auras、AVC、Cooler Master、QCT/Wiwynn/Foxconn 生态 | 贴近 AI server ODM，冷板、manifold、in-rack CDU、风扇/电源/整柜协同强。 |
| 中国大陆 | Envicool、Sanhua、Yinlun、Feirongda、Goaland、高澜、同飞、申菱、KRES 等 | 成本、交期、全链条集成和本土智算客户强；海外认证和极高端可靠性仍是关键门槛。 |
| 欧洲 | Stäubli、CEJN、Danfoss、Alfa Laval、GF、Rittal、Asetek、Submer、Asperitas、Kelvion | 高可靠流体连接、阀泵、板换、聚合物管路、HVAC/热回收和绿色合规能力强。 |
| 日本/韩国 | Nidec、Fujikura、MinebeaMitsumi、LG、Samsung ecosystem | 泵、电机、精密加工、冷板/散热件、系统工程能力强，适合进入亚洲大客户供应链。 |

### 7.2 供给瓶颈

1. **冷板加工和检测**：高纯铜/铝、CNC/skiving/钎焊/扩散焊、微通道清洁、100% leak/flow/thermal test 都需要专用产线。
2. **低压降快接头**：UQD/UQDB/LQC 既要 OCP 互配，又要低压降、低插拔力、零滴漏、耐 PG25/DI water、盲插容差；密封材料和精密加工是核心。
3. **2MW+ CDU 关键部件**：泵、板换、阀、传感器、控制器、过滤器、机柜结构、冗余电源和出厂测试能力同时受限。
4. **水质/冷却液体系**：颗粒、电导率、腐蚀、微生物、气泡会造成冷板堵塞或停机；现场冲洗和在线监测常被低估。
5. **认证与客户锁定**：NVIDIA RVL、OEM design guide、OCP、hyperscaler 内部标准、UL/CE/压力容器/材料兼容测试会使供应商切换成本极高。
6. **现场交付和服务队伍**：大规模 AI rack 安装要 pressure test、flush、commission、leak localization、thermal monitoring；服务短缺会拖慢收入确认。
7. **设施水环与热拒绝**：不是买 CDU 就能上液冷；FWS、dry cooler、cooling tower、chiller、楼板承重、管路路由、消防/漏水策略都可能卡项目。
8. **区域供应链与关税**：美国/欧洲客户要求本地化生产和服务；中国供应商要解决出口、认证和客户信任问题。

### 7.3 成本结构

| 产品 | 典型成本构成 | 毛利决定因素 |
|---|---|---|
| 冷板/loop | 铜/铝/TIM 25-35%；加工/焊接 20-30%；QDs/软管/密封 15-25%；测试清洁 15-20%；工程/QA 10-15%。 | 热阻、压降、良率、GPU 平台认证、是否提供 loop 级总成。 |
| CDU | 泵 15-25%；板换 15-25%；阀/传感器/控制 15-25%；机柜/管路/过滤/膨胀罐 15-20%；电气/软件/测试 15-20%；服务 5-10%。 | 容量、ATD、冗余、控制软件、现场服务、是否绑定大客户框架协议。 |
| Manifold/管路 | 不锈钢/聚合物材料 20-35%；加工/焊接/预制 25-35%；阀和连接件 15-25%；清洁/测试 15-25%。 | 低污染、低压降、预制化、安装速度、OCP/客户接口。 |
| 快接头 | 不锈钢/黄铜/聚合物 20-30%；精密加工 25-40%；密封件 10-20%；装配/测试 20-30%；认证 5-10%。 | OCP 互配、blind-mate、低压降、插拔寿命、零滴漏记录。 |
| 泵阀传感器 | 电机/泵头/阀体 25-40%；传感器/电子控制 20-30%；机械件 15-25%；测试和软件 15-25%。 | 动态响应、N+1 冗余、在线维护、数据接口、长期可靠性。 |
| 冷却液/水处理 | 基础液/添加剂 30-50%；监测与测试 20-30%；包装/物流 10-20%；服务 20-30%。 | 材料兼容、保修责任、在线监测、耗材复购和服务合同。 |

### 7.4 价格传导机制

| 阶段 | 价格特征 |
|---|---|
| 2026 上半年 | 设计验证和 NPI 阶段，高端件按项目议价，供应商用交期和认证拿溢价。 |
| 2026 下半年 | GB300/ASIC rack 放量，冷板、2MW CDU、快接头、现场服务有阶段性供不应求，毛利上行。 |
| 2027 | 标准化压低普通冷板和通用 CDU ASP，但高端 blind-mate、低压降、智能监测、服务合同维持高毛利。 |
| 2028 | 低端硬件趋向 OEM 化/中国化，高 ROIC 转向高热流冷板、流体控制软件、两相/水处理和认证供应链。 |

## 8. 竞争格局与壁垒

### 8.1 市场结构估计

| 环节 | 集中度判断 | 头部公司 |
|---|---|---|
| 整体液冷系统/CDU | Hyperscale 高端项目 CR5 约 45-65%；区域项目分散。 | Vertiv、Schneider/Motivair、CoolIT/Ecolab、Boyd、Delta、Nidec、Envicool、LiquidStack/Trane。 |
| 冷板/冷板回路 | CR5 约 35-55%，ODM/OEM 自制与外购并存。 | Boyd、CoolIT、Auras、AVC、Delta、Envicool、Feirongda、Cooler Master、Asetek、JetCool/Frore。 |
| 快接头 | 高端 OCP/低压降 CR5 可达 60-80%。 | CPC/Dover、Stäubli、CEJN、Parker、Faster、KRES、GF。 |
| 泵阀板换 | 头部工业公司强，但应用分散。 | Danfoss、Alfa Laval、Xylem、Nidec、Sanhua、Parker、Grundfos、GF、Eaton。 |
| 冷却液/水质服务 | 化学品和服务网络决定集中度。 | Ecolab/Nalco、Chemours、Engineered Fluids、LiquidStack、ZutaCore、Envicool、MicroCare、Shell/Castrol 等。 |

### 8.2 壁垒清单：为什么能定价

| 壁垒 | 定价逻辑 |
|---|---|
| GPU/ASIC 平台认证 | 一旦进 NVIDIA/AMD/OEM/hyperscaler AVL/RVL，客户不会为小幅降价冒漏液和停机风险。 |
| 系统热阻与压降 | 高端冷板和快接头直接决定芯片温度、泵功耗、rack 可用功率和 token/W，性能可量化。 |
| 量产良率与测试数据 | 500 万片冷板或数千台 CDU 的 field record 比实验室指标更值钱；客户买的是停机概率下降。 |
| 现场服务网络 | 液冷系统不是一次性交付，冲洗、补液、监测、维修和扩容都需要服务，服务粘性高。 |
| 标准接口与切换成本 | OCP 标准降低行业门槛，但同一客户内的接口、控制软件和维护 SOP 会形成事实锁定。 |
| 水化学/材料兼容 | 一次腐蚀、堵塞、密封膨胀或污染事故会放大到整机房；化学与材料验证形成隐性壁垒。 |
| 交付速度 | AI rack 上电时间直接影响云厂商收入和训练/推理窗口，能按期交付者可获得价格优先权。 |

### 8.3 长期最可能高 ROIC 的层

1. **认证冷板/loop 平台**：直接贴近 GPU/ASIC，进入 design guide 后生命周期长；普通铜件会被压价，但高热流冷板会继续高毛利。
2. **快接头与盲插连接器**：单价不高但失效成本极高，低压降和零滴漏可量化，客户对可靠性付费。
3. **CDU 控制与服务**：硬件可被竞争压价，但控制算法、水质监测、现场服务和远程运维能形成 recurring revenue。
4. **流体化学/水处理**：Ecolab 收购 CoolIT 的战略逻辑就在于把水处理、化学、监测和冷却硬件打包；这类模式更接近高 ROIC 服务平台。
5. **两相/非水直触专利路线**：如果 2kW-4kW+ 芯片普及，ZutaCore、JetCool、Frore 等有机会获得技术溢价；风险是验证周期长、保修责任重。

## 9. 2026 关键变化

1. **液冷从 GPU rack 向全 AI Factory rack 扩散**：GB300/Rubin 不只冷 GPU，CPU rack、LPU rack、storage/context rack、交换机 rack 都开始纳入液冷规划。
2. **2MW+ CDU 与 OCP 接口标准进入采购语言**：Project Deschutes、UQD/LQC、Open Rack 让客户从“定制项目”转向“标准模块复制”；有利于头部量产供应商，也会淘汰手工作坊式集成商。
3. **产业资本并购加速**：Ecolab/CoolIT、Schneider/Motivair、Trane/LiquidStack、Vertiv 扩产和收购液冷服务商说明行业从实验期进入工业化期。2026 年供应紧张与估值重估会并存。

## 10. 2027 关键变化

1. **Rubin/MI400/TPU8/Trainium3 拉高热流密度**：冷板从 1kW-1.5kW 级向 2kW-4kW 级演进，常规微通道会让位于喷射、3D 流道、两相直触等更高阶技术。
2. **网络与光模块也开始液冷化**：1.6T、CPO、高功耗交换芯片和光模块密度上升，Mini QD、液冷 switch tray、光模块温控成为新增子方向。
3. **高端液冷供应链分层**：普通冷板、通用管路、低端 CDU 毛利下降；认证件、服务化、两相/高热流、低压降连接器、智能控制维持高毛利。PFAS-free 流体会决定浸没/两相路线能否真正放量。

## 11. 头部公司与细分技术全景

### 11.1 系统/CDU/整柜液冷

| 公司 | 优势 |
|---|---|
| Vertiv | 电力+冷却+模块化基础设施全栈，360AI、CoolTera、PurgeRite、ThermoKey/BMarko 等能力增强；2025 年底 backlog $15B。 |
| Schneider Electric / Motivair | 端到端液冷、电力和控制；CDU 105kW-2.5MW，NVIDIA 协同，全球服务扩张。 |
| CoolIT / Ecolab | 直触液冷纯玩家，CDU、冷板、loop、manifold；Ecolab 收购后结合水处理/化学/监测。 |
| Boyd | NVIDIA GB200 RVL 相关冷板、manifold、CDU；5M cold plate 出货记录。 |
| Delta Electronics | 2MW/3MW CDU、in-rack CDU、cold plate、HVDC、风扇/电源/网络整合。 |
| Nidec | 2MW in-row CDU、泵和电机控制，Lenovo Neptune 合作，OCP Deschutes 原型。 |
| Envicool | Coolinside 全链条：冷板、快速接头、Manifold、CDU、管路、工质、漏液检测、智能平台。 |
| Supermicro/Dell/HPE/Lenovo/ASUS | 整机/整柜液冷集成，能把冷却直接绑定 AI server 和 rack 交付。 |
| LiquidStack / Trane | direct-to-chip 与 immersion，Trane 收购后有 HVAC 与全球渠道。 |
| Asetek / Rittal / Modine-Airedale / nVent / Eaton | 机房级冷却、CDU、机柜、热拒绝和工程能力。 |

### 11.2 冷板、冷板回路、散热模组

| 公司 | 优势 |
|---|---|
| Boyd | 高 volume 冷板、100% inline test、hyperscaler 客户。 |
| CoolIT | OMNI/Split-Flow、4000W coldplate 原型、NVIDIA/AMD 协同。 |
| Auras | 台湾 AI server 冷板/manifold 供应商，受益 NVIDIA/AWS/ASIC 路线。 |
| Asia Vital Components, AVC | 风冷+液冷热管理，2025 收入高增，进入 AI server cooling 供应链。 |
| Delta | 冷板最高 6,200W 展示，rack/CDU/电力协同。 |
| Envicool / Feirongda / Yinlun / Goaland / Tongfei | 中国冷板、管路、CDU、服务器液冷模组、储能热管理外溢。 |
| JetCool / Frore / ZutaCore | 微喷射、3D jet-channel、两相直触等高热流新路线。 |
| Asetek / Cooler Master / EK | 水冷模组和服务器/工作站液冷经验，可切入边缘和企业 AI。 |

### 11.3 快接头、软管、manifold、管路

| 公司 | 优势 |
|---|---|
| CPC / Dover | Everis UQD/UQDB，hyperscale liquid cooling connector 代表供应商。 |
| Stäubli | UQD/UQDB/TDU，大流量低压降；2026 LQD 主打 UQD04 尺寸与 UQD08 流量性能结合。 |
| CEJN | UQD/LQC，OCP 参与者；UQD02/04/06/08，LQC 适用于 CDU。 |
| Parker Hannifin | 快接头、软管、流体连接、工业客户基础。 |
| Faster | OCP UQD 系列，数据中心液冷接口。 |
| GF | LiquidCore 聚合物管路、IR welding、低污染/低腐蚀、预制化。 |
| KRES | OCP UQD 产品，进入 OCP 产品生态。 |
| Swagelok / Norma / SMC / TE Connectivity | 管件、密封、传感和连接能力，可在局部环节切入。 |

### 11.4 泵阀、换热器、传感器、水处理

| 公司 | 优势 |
|---|---|
| Danfoss | CDU 生态、板式换热器、CoolTrain 阀组、低 LMTD/低压降组件。 |
| Alfa Laval | 板换、FreeWaterLoop、Boyd CDU 合作。 |
| Xylem / Flojet | D5/DDC/diaphragm pumps、glycol charging/top-up。 |
| Nidec | 高性能泵、电机、响应控制、CDU。 |
| Sanhua | 阀、泵、板换、微通道、外机/冷媒侧和服务器端延伸。 |
| Ecolab / Nalco | 3D TRASAR、冷却水化学、水质监测、数据中心服务网络。 |
| Sensata / Honeywell / TE / Amphenol | 温度、压力、流量、漏液、连接传感器。 |
| Grundfos / Wilo / ITT | 数据中心/工业泵与水系统。 |

### 11.5 浸没、两相、非水/介电流体

| 公司 | 优势 |
|---|---|
| ZutaCore | HyperCool waterless two-phase direct-to-chip。 |
| LiquidStack / Trane | 直触液冷与浸没式系统，全球 HVAC 平台加持。 |
| Submer / GRC / Asperitas / Iceotope | 单相浸没、槽体、边缘/HPC 场景。 |
| Engineered Fluids / Chemours / MicroCare / Solvay-Syensqo / Daikin | 介电流体、PFAS 替代、材料兼容与化学能力。 |
| 3M | 已完成 PFAS manufacturing exit；历史 Novec/Fluorinert 供应商，不再是长期新增产能锚。 |
| FluxZero / SuperLiq 等 | PFAS-free 替代流体探索，2026 处于验证/导入期。 |

## 12. 投资判断

### 12.1 最看好的子方向

| 排名 | 子方向 | 原因 |
|---:|---|---|
| 1 | OCP 兼容高端快接头、盲插、mini QD | 单价小但故障代价极大；低压降能直接降低泵功耗；认证后切换成本高。 |
| 2 | 高热流冷板与 loop 总成 | 贴近 GPU/ASIC，2027 芯片功耗继续上升；普通冷板会被压价，高端冷板仍稀缺。 |
| 3 | 2MW+ CDU 与控制系统 | AI pod 标准化后复制速度快；硬件+软件+服务形成平台收入。 |
| 4 | 流体监测/水处理/服务 | 长期 recurring，Ecolab/CoolIT 是明确信号；水质事故风险让客户愿意付费。 |
| 5 | 两相直触和 PFAS-free 流体 | 短期不确定，长期期权价值高；若 4kW+ 芯片提前，溢价极高。 |

### 12.2 风险

| 风险 | 影响 |
|---|---|
| AI CapEx 放缓或 GPU/HBM 延迟 | 订单可能从 2026 H2 推到 2027，普通组件库存压力上升。 |
| 标准化导致价格下行 | 冷板、管路、普通 CDU 可能快速商品化，只有认证和服务能保毛利。 |
| 漏液/腐蚀事故 | 单次大事故会影响客户信心和供应商准入。 |
| 两相/浸没流体监管 | PFAS-free 替代品未通过大规模验证前，浸没路线难以成为主流。 |
| 现场工程瓶颈 | 没有 FWS/TCS、热拒绝和施工服务，再多组件也无法上电。 |

## 13. 核心资料索引

| 类别 | 来源 |
|---|---|
| NVIDIA 路线 | [GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/), [GB200 NVL72](https://www.nvidia.com/en-us/data-center/gb200-nvl72/), [Vera Rubin 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/), [Vera Rubin 新闻稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) |
| 市场报告 | [Dell'Oro / PRNewswire liquid cooling 2029 $7B](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html), [TrendForce liquid cooling penetration](https://www.trendforce.com/presscenter/news/20250821-12682.html), [Uptime 2026 liquid cooling niche view](https://journal.uptimeinstitute.com/liquid-cooling-will-not-outgrow-its-high-density-niche/) |
| OCP/标准 | [OCP Project Deschutes 2MW CDU specification](https://ocpprodweb3.opencompute.org/documents/ocp-specification-deschutes-final-2025-09-05-pdf), [OCP UQD product example](https://www.opencompute.org/products/624/kres-universal-quick-disconnect-uqd), [OCP Cold Plate Requirements](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) |
| 头部公司 | [Ecolab to acquire CoolIT](https://www.ecolab.com/news/2026/03/ecolab-to-acquire-coolit-systems-a-global-leader-in-advanced-liquid-cooling-for-next-gen-ai-data-ce), [CoolIT 25 years growth](https://www.coolitsystems.com/resources/news/coolit-25-years-liquid-cooling/), [Schneider/Motivair portfolio](https://www.motivaircorp.com/news/schneider-electric-unveils-liquid-cooling-portfolio/), [Vertiv Q1 2026](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx), [Vertiv Q4 2025](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-with-Organic-Orders-Growth-of-252-and-Diluted-EPS-Growth-of-200-Adjusted-Diluted-EPS-37/default.aspx) |
| 组件一手资料 | [Boyd GB200 collaboration](https://www.boydcorp.com/boyds-collaboration-with-nvidia.html), [Boyd 5M cold plates](https://www.boydcorp.com/about-boyd/resources/news-and-events/boyd-delivered-5-millionth-liquid-cold-plate-for-ai-cooling.html), [Delta 3MW CDU shipping](https://www.deltapowersolutions.com/en/mcis/news-2026-gocool-3mw-cdu-now-shipping-powering-the-next-generation-of-ai-data-centers.php), [Nidec liquid cooling](https://www.nidec.com/en/product/news/2026/news0407-01/), [Envicool Coolinside](https://www.envicool.com/en/solutioninfo41/solution.html) |
| 快接头 | [CPC Everis UQD](https://www.cpcworldwide.com/Liquid-Cooling/Products/Universal-Quick-Disconnects-UQDs), [Stäubli LQD 2026](https://www.staubli.com/global/en/news/global/2026/lqd-coupling-data-center-liquid-cooling.html), [CEJN UQD](https://www.cejn.com/en-sg/products/thermal-control/uqd-couplings/), [CEJN LQC](https://www.cejn.com/en-us/products/thermal-control/opc-lqc-couplings/), [Parker CDB](https://www.parker.com/content/dam/Parker-com/Literature/Quick-Coupling/CDB%20Series%20Bulletin.pdf) |
| 泵阀/板换/管路 | [Danfoss B3-260C](https://www.danfoss.com/en-us/about-danfoss/news/dcs/danfoss-launches-new-brazed-plate-heat-exchanger-for-data-center-cooling/), [Danfoss CDU ecosystem](https://www.danfoss.com/en/about-danfoss/news/dcs/danfoss-strengthens-its-support-for-next-generation-liquid-cooling-in-data-centers/), [Alfa Laval FreeWaterLoop](https://www.alfalaval.com/media/news/investors/2026/alfa-laval-launches-freewaterloop-to-support-efficient-data-center-cooling/), [GF polymer piping](https://www.gfps.com/com/en/about-us/media-center/news-details.html/news/gfps/2026/hq/ai-data-centers-why-polymer-piping-matters-in-direct-liquid-cooling), [Xylem Flojet pumps](https://www.xylem.com/en-us/info/flojet-liquid-cooling-pumps/) |
| 两相/浸没/流体 | [3M PFAS exit](https://www.3m.com/3M/en_US/pfas-stewardship/operations-innovation/), [LiquidStack/Trane](https://liquidstack.com/news/trane-technologies-to-acquire-liquidstack-to-accelerate-end-to-end-data-center-thermal-management-solutions), [ZutaCore](https://zutacore.com/), [LiquidStack immersion](https://liquidstack.com/immersion-cooling), [FluxZero PFAS-free](https://fluxzerofluid.com/) |
| OEM/服务器 | [Dell XE8712 GB200](https://infohub.delltechnologies.com/en-us/p/poweredge-xe8712-with-nvidia-gb200-a-high-density-foundational-server-for-rack-scale-ai-2/), [Dell AI Factory](https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2025~05~dell-technologies-and-nvidia-unveil-next-generation-enterprise-ai-solutions.htm), [HPE GB200](https://www.hpe.com/us/en/newsroom/press-release/2025/02/hpe-announces-shipment-of-its-first-nvidia-grace-blackwell-system.html), [Lenovo Neptune](https://www.lenovo.com/us/en/servers-storage/neptune/index.html), [Supermicro FY26 deck](https://ir.supermicro.com/files/doc_financials/2026/q1/FQ126-SMCI-Earnings-Deck.pdf) |

非投资建议。本报告数字大量依赖 2026 AI 基础设施继续超预期扩张的乐观假设；若 hyperscaler CapEx、GPU/HBM 供给或电力并网节奏下修，液冷小组件订单会延后，但技术渗透方向不变。
# 行业调研：【中压直流、800VDC与固态变压器】

> 截至日期：2026-05-08  
> 研究口径：本报告聚焦 AI 计算中心/AI Factory 的高压直流配电、800VDC rack/sidecar 架构、中压固态变压器（MVSST）和中压直流（MVDC）园区级配电。市场规模为设备/模块/工程订单口径，不含 GPU/服务器本体，不构成投资建议。  
> 核心假设：对 2026-2027 AI 基础设施建设保持非常乐观。对于尚无直接订单披露的子方向，按 NVIDIA 800VDC 路线图、Rubin/Kyber 节奏、美国 AI 数据中心建设模型和供应链可交付性做大胆但可解释的推演。

## 0. 一页结论

1. **800VDC 已经从“论文/标准讨论”进入“头部生态产品化”阶段。** NVIDIA 在 2025 OCP/2026 GTC 后把 800VDC 定义为下一代 AI Factory 电力底座；合作名单覆盖 ABB、Eaton、GE Vernova、Hitachi Energy、Schneider、Siemens、Vertiv、Delta、TI、ST、Infineon、onsemi、Renesas、Navitas、AOS 等。NVIDIA 明确写到 800VDC 数据中心 full-scale production 会与 2027 Kyber rack-scale 系统同步，Vertiv 的 800VDC 组合计划 2026H2 发布以支持 2027 Rubin Ultra。
2. **2026 最可能先放量的是“rack-level 800V sidecar / power rack + 800V 到 48/12/6V DC/DC + 保护/储能”，不是园区级 MVDC。** Schneider 的白皮书直接把 800VDC power racks/sidecars 称为 immediate enabler；Delta 已在 GTC 2026 展示 660kW 800VDC In-Row Power Rack、80kW BBU shelf、3MW/2.4MW CDU 和 SST/SOFC 微电网组合；TI/ST/Renesas 已给出 800V 到 6V/12V/48V 的参考设计和效率指标。
3. **MVSST 是 2026-2027 的高赔率方向，但大规模商用节奏比 sidecar 慢 6-18 个月。** Eaton 已有 MVSST 页面，声称直接把 MVAC 转 LVAC/DC、800VDC 效率 >97%、安装周期最多快 50%；Enphase 2026-04-28 发布 IQ SST，单 rack 1.25MW、342 个模块、目标 98.5% 效率、99.999% 可用性，15/35kV 输入直接输出 800VDC/±400VDC。PNNL/DOE 2026-01 模型把 MVSST 列为下一代设计，但也明确 MVDC data center 比 LVDC/SST 更远。
4. **MVDC 园区级配电的投资价值在 2027 后更大，2026 主要看标准、断路器、保护、绝缘和多端口控制。** MVDC 需要 DC cable、busbar、switchgear、breaker、grounding、fault isolation 全链条成熟。当前最可能先在 1.5kVDC 以下 LVDC/HVDC、800VDC/±400VDC 和 MVSST 层面验证，真正 5-35kV DC 园区环网更像 2028+ 放量。
5. **价值捕获排序：高压保护/控制半导体与 DC breaker > MVSST/多端口 SST 平台 > 800V DC/DC 高密模块 > 800V sidecar/power rack > 金属箱体/低差异 busway。** 原因是失效成本极高、认证周期长、与 NVIDIA/hyperscaler reference design 深绑定、且从“卖设备”升级为“卖可用性和功率动态控制”。

## 1. 技术地图：现在在用什么，为什么要变

### 1.1 传统 AI 数据中心电力链

当前主流新建数据中心仍是：

`13.8-35kV MVAC utility -> 变压器 -> 415/480VAC -> AC UPS -> PDU/RPP/busway -> rack PSU -> 54VDC/48VDC -> 12V/6V/1V core rails`

这个架构成熟、认证和运维体系完整，但面对 GB300、Vera Rubin、Rubin Ultra、MI400/Helios、Trainium3、Maia 200、TPU v7/v8 等高功率 rack，瓶颈从“能不能供电”变为“能不能在有限灰空间、铜、冷却和瞬态负载下稳定供电”。NVIDIA 的 800VDC 技术博客指出，传统端到端效率可低于 90%，且在 415/480VAC 转 54VDC 再逐级降压时存在多重转换损失和大量铜/连接器/空间占用。

### 1.2 800VDC 的三条实际路径

| 路径 | 2026 成熟度 | 典型架构 | 适用场景 | 投资含义 |
|---|---:|---|---|---|
| Rack-level / sidecar 800VDC | 高，2026 design-in 到小批量 | 480VAC/415VAC 输入 sidecar，AC/DC 生成 800VDC，IT rack 内 800V->48/12/6V | 既有数据中心改造、新 AI hall、GB300/Rubin 过渡 | 最快放量，利好 Delta/Vertiv/Schneider/Eaton/TI/ST/Renesas/Infineon/Navitas |
| Facility-level 800VDC | 中，2026 参考设计，2027 新建园区主线 | MVAC 在 power room/perimeter 一次转 800VDC，数据厅内 DC busway 分配 | 新建 AI Factory、100kW-1MW rack、高密集群 | 利好 DC breaker、DC busway、BESS 接入、集中整流器 |
| MVSST：MVAC->800VDC | 中低，2026 产品发布/试点，2027 early field | 15/35kV AC 直接进固态变压器，输出 800VDC/±400VDC | 超高密 AI hall、缺变压器/UPS 空间、微电网 | 高壁垒高毛利，核心在 SiC/GaN、控制、保护、认证 |

### 1.3 MVDC 的位置

MVDC 是更远一步：`MVAC utility -> MV AC/DC -> 5-35kV DC campus bus -> DC/DC/SST block -> 800VDC racks`。DOE/PNNL 2026-01 对六类数据中心电力设计建模时，把 MVSST 作为 Design 5、MVDC distribution 作为 Design 6，并写明供应商预计未来几年会开始部署 LVDC 与 SST，但 MVDC data center 由于需要 DC cable、busbars、switchgear、circuit breakers 等大量产品开发，field service 更远。

我的判断：**2026 MVDC 是研发/标准/保护器件订单，2027 是少量园区 pilot，2028-2029 才有可见批量项目。**

## 2. 2026 AI 大建设下的机会、挑战与技术路线

### 2.1 AI 芯片路线对电力架构的直接拉动

项目已有芯片底稿显示，2026 出货/价值最大的主线是 NVIDIA B300/GB300 Blackwell Ultra、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon 590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200、Alibaba T-Head、AMD MI400/Helios 首批。2027 的增量更靠 NVIDIA Rubin/Kyber/Rubin Ultra、AMD MI400、TPU8、Trainium3/4 和 Broadcom XPU。

| 芯片/平台背景 | 对 800VDC/MVSST 的影响 | 2026 技术路径判断 |
|---|---|---|
| GB300/B300、GB200 延续放量 | 单 rack 功率从几十/百 kW 继续上行，液冷、48V/54V 已到边界 | 仍以 AC+UPS+54V 与 800V sidecar 混合交付 |
| Vera Rubin 2026H2、Rubin Ultra/Kyber 2027 | NVIDIA 明确 Kyber rack 设计使用 800VDC；64:1 LLC 直接到 12V | 2026 设计冻结/样机，2027 新建 AI Factory 主线 |
| Trainium2/3、TPU v7/v8、MTIA、Maia | Hyperscaler 自研 ASIC 强调 TCO 和能效，愿意改基础设施 | Google/AWS/Microsoft/Meta 更可能做内部 DC bus 与定制 power shelf |
| AMD MI400/Helios、HBM4 rack | 72 GPU rack、HBM4 高功率密度，需高压直流/液冷协同 | 2026H2 早期项目，2027 放量时拉动 800V sidecar |
| 中国 Ascend/Cambricon/T-Head | 受制程约束，系统靠并联和超节点堆规模，更吃电力/冷却 | 2026 以传统 AC/48V 与国产高压 DC 试点并行 |

### 2.2 三情景：技术成熟和放量时间

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|
| 800V rack sidecar / power rack | 2026Q2-Q4 design-in，2027 随 Kyber/Rubin Ultra 批量；2026 渗透新高密 AI rack 2-5% | 2026H2 已进入多个 GW 级 AI Factory basis of design；2027 新建高密 rack 渗透 15-25% | 2026Q4 客户提前锁单，2027 新建高密 rack 渗透 35-45% |
| 800V->48V DC/DC | 2026 小批量，复用 48V 生态；2027 主流过渡产品 | 2026H2 服务器 ODM 进入量产验证，2027 大量出货 | 2027 上半年成为多数 Rubin/MI400 rack 默认 |
| 800V->12V/6V 直接转换 | 2026 参考设计/样机，2027 高端 GPU tray 小规模 | 2027 在 Kyber/Rubin 部分节点导入 | 2027H2 直接到 12/6V 大规模替代 48V 中间级 |
| 高压 DC breaker/eFuse/hot-swap | 2026 认证/设计入，2027 伴随 800V 扩张放量 | 2026H2 开始成为 sidecar/rack 标配 | 2027 形成高 ASP 标准件，供不应求 |
| MVSST 15/35kV->800VDC | 2026 产品/试点，2027 早期 field，2028 批量 | 2027 多个 AI 园区采用 1-10MW blocks | 2027H2 MVSST 在缺变压器地区成为抢工期方案 |
| MVDC campus distribution | 2026-2027 标准和 pilot，2028+ 商用 | 2027H2 小规模园区支路试运行 | 2027 只在极少数 hyperscaler/军工/主权 AI 项目部署，收入弹性来自保护器件和工程 |
| 多时间尺度储能：supercap/BESS/flywheel | 2026 先作为 UPS/BESS 与 rack CBU 附属 | 2027 与 800VDC bus 深度耦合 | 2027 形成“动态功率缓冲”新 BOM，GPU 调度直接联动 |

### 2.3 机会

- **转换级数减少带来的效率增益。** NVIDIA 800VDC 页面强调一次 AC-to-800VDC、数据厅内分配到 rack；ST 博客引用 800V 相对当前 54V 系统最高可改善效率约 5%。若一个 500MW AI campus 年负载率 60%、电价 $70/MWh，1% 全链路效率就是约 $18M/年电费和冷却负担，5% 对应 $90M/年级别经济价值。
- **铜、空间、施工周期减少。** NVIDIA 写到同线径 800VDC 可比 415VAC 承载 157% 更多功率，且三线 DC 替代四线 AC；AOS 口径给出最高 45% 铜需求下降。ABB 也强调 800VDC 减小 conductor size 和材料用量。
- **AI 负载瞬态成为新刚需。** NVIDIA 把毫秒到秒级 supercapacitor/高功率电容放在 compute rack 附近，把秒到分钟级 BESS 放在 utility interconnection；ZincFive 2026 调研里 UPS 受 AI GPU transients/load spikes、battery stress 和 faster control loops 影响已成为明确痛点。
- **变压器/开关柜长交期给 MVSST 创造窗口。** IEA 指出 transformer/cable 等关键电网部件等待时间三年内翻倍，Wolfspeed 白皮书称 MV transformer lead time 拉长到最高 3 年，SST 可用模块化半导体方案压缩部署周期。

### 2.4 挑战

- **DC fault protection 比 AC 难。** 800VDC 与 MVDC 没有自然过零，断弧、选择性保护、ground fault detection、pre-charge/discharge、maintenance hot-swap 都是认证和安全核心。
- **标准未完全冻结。** 800V、±400V、2-wire、3-wire、grounding、connector、touch-safe、arc flash、UL/IEC/OCP/ODCA/Current/OS 的接口需要继续统一。
- **WBG 半导体可靠性。** 1200V SiC、650V/100V GaN、3.3kV/6.5kV/10kV SiC 在高温、高海拔、宇宙射线 FIT、部分放电和 24/7 工况下需验证。
- **运维人才缺口。** 传统数据中心电工熟悉 AC UPS/PDU，但 800VDC/MVDC 需要电力电子、控制、绝缘、固件与系统级保护协调能力。
- **客户不愿拿 uptime 冒险。** AI 服务器价值可达传统服务器几十倍，Infineon 指出 AI server 成本可达传统 server 30 倍，任何电力架构变更必须证明 uptime 和 serviceability。

## 3. 已开始放量/接近放量的关键产品：市场、渗透率、利润率

### 3.1 市场模型口径

本报告把“800VDC/MVSST/MVDC 相关市场”定义为：800V sidecar/power rack、AC/DC power shelf、800V DC/DC、HV hot-swap/eFuse/DC breaker、DC busway/connector、supercap/CBU、MVSST/MV rectifier、MVDC protection/control，不包括传统 UPS/变压器/开关柜全市场，也不包括 GPU/服务器。

基准锚点：

- 本地 AI 数据中心底稿估算 2026 美国 AI DC 电力与能源订单 $80-125B、冷却 $25-45B、AI 服务器与机架 $240-360B。
- NVIDIA/Vertiv/Delta/TI/ST 等公开信息显示，2026 800VDC 主要处于 reference design、GTC 展示、早期 design-in 和 H2 产品组合发布阶段；2027 随 Kyber/Rubin Ultra 放量。
- 因此 2026 收入口径不能按“所有 AI power”乘高渗透率，而应按高密新 rack 的小比例、并给 2027/2028 更陡的 S 曲线。

### 3.2 已开始放量产品总表

| 产品/细分技术 | 关键公司 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| 800V sidecar / power rack / In-row power rack | Delta、Vertiv、Schneider、Eaton、ABB、Flex、Lite-On、Megmeet | 基准 $0.3-0.8B；乐观 $0.8-1.8B；极乐观 $1.8-3.5B | 基准 $4-8B；乐观 $8-16B；极乐观 $16-30B | 基准 $15-30B；乐观 $30-60B；极乐观 $60-110B | 2026 新高密 AI rack 2-5%；2027 12-25%；2028 25-45% | 24-32% / 32-42% / 42-55% |
| 800V->48/54V DC/DC 模块 | Renesas、ST、TI、Infineon、Delta、Lite-On、Vicor、MPS | $0.15-0.4B / $0.4-0.9B / $0.9-1.8B | $2-5B / $5-10B / $10-18B | $8-18B / $18-35B / $35-65B | 复用 48V 生态，是 2026-2027 最稳过渡路径 | 30-42% / 42-55% / 55-65% |
| 800V->12V/6V 高密转换板 | TI、ST、Renesas、Navitas、AOS、Infineon、MPS | $0.05-0.2B / $0.2-0.5B / $0.5-1.2B | $1-3B / $3-7B / $7-14B | $6-14B / $14-30B / $30-55B | 2026 样机/小量；2027 高端 tray 渗透 5-15%；2028 20-35% | 35-48% / 48-60% / 60-70% |
| 800V hot-swap/eFuse/pre-charge/protection IC | Infineon、TI、ADI、onsemi、ST、Renesas、Littelfuse、MPS | $0.08-0.2B / $0.2-0.5B / $0.5-1.0B | $1.2-2.5B / $2.5-5B / $5-9B | $4-9B / $9-18B / $18-30B | 每个 800V tray/rack 必配；serviceability 约束强 | 45-58% / 58-68% / 68-75% |
| 800V DC busway、connector、cable、busbar | ABB、Schneider、Eaton、Siemens、Vertiv、nVent、Legrand、Amphenol、TE、Molex、BizLink | $0.2-0.6B / $0.6-1.2B / $1.2-2.5B | $3-7B / $7-14B / $14-26B | $10-25B / $25-50B / $50-90B | 与 sidecar 同步，但认证/安装服务占比高 | 25-35% / 35-45% / 45-55% |
| Rack 侧 CBU/supercap/fast buffer | TI、Eaton、Skeleton、Nichicon、Nippon Chemi-Con、Yageo/KEMET、Cornell Dubilier、Maxwell/Tesla、Vishay | $0.05-0.15B / $0.15-0.4B / $0.4-0.9B | $0.8-2B / $2-4.5B / $4.5-8B | $3-8B / $8-18B / $18-35B | 2026 从示范走向必选；2027 随 power orchestration 上升 | 28-40% / 40-55% / 55-65% |
| 800V 兼容 BBU/BESS/DC UPS | Delta、Vertiv、Schneider、Eaton、Saft、Tesla、Fluence、CATL、Powin、ZincFive | $0.4-1.0B / $1-2.5B / $2.5-5B | $5-12B / $12-24B / $24-40B | $18-40B / $40-75B / $75-130B | BESS 本来放量，800VDC 让其更靠近 DC bus | 18-28% / 28-38% / 38-50% |
| 1200V SiC、650V/100V GaN、drivers/controllers | Infineon、ST、onsemi、TI、Renesas、Navitas、AOS、Wolfspeed、ROHM、Innoscience、EPC、Power Integrations | $0.2-0.6B / $0.6-1.3B / $1.3-2.8B | $3-8B / $8-16B / $16-30B | $12-30B / $30-60B / $60-100B | 每个转换级价值量提升；早期由 design-in 决定份额 | 40-52% / 52-62% / 62-72% |

### 3.3 产品细节与一手信息

- **Delta 800VDC In-Row Power Rack。** Delta 在 NVIDIA GTC 2026 展示 800VDC power、liquid cooling、microgrid 组合；重点包括 660kW In-Row Power Rack，每个 shelf 内嵌 80kW BBU、合计 480kW，AC-DC 效率最高 98%；同时展示 3,000kW 与 2,400kW CDU，后者支持 800VDC 和 N+1 pump。Delta 4/20/2026 又在 Data Center World 2026 宣布 800VDC rack power distribution 可达每 rack 1.1MW、最高 98% 效率。
- **Vertiv 800VDC power portfolio。** Vertiv 2025-11 宣布与 NVIDIA 推进 800VDC platform designs，从 concept 到 engineering readiness，计划 2026H2 发布，支持 2027 Rubin Ultra；公司称其 800VDC reference architecture 已在几个大型 AI Factory 早期设计中作为 basis of design，并按 gigawatt-scale demand 缩放。
- **TI 800VDC complete architecture。** TI 2026-03-16 在 GTC 2026 展示完整 800VDC 方案：800V hot-swap、800V->6V isolated bus converter，97.6% peak efficiency、>2000W/in³；6V-><1V multiphase buck；30kW 800V AC/DC PSU；800V capacitor bank unit；800V->12V bus converter。
- **ST 800VDC 12V/6V portfolio。** ST 2026-03-17 宣布 800VDC->12V 与 800VDC->6V 架构，补足 800VDC->50V；ST 博客给出 6kW、850kHz LLC，800V->12V，峰值效率 97.5%、功率密度 2,500W/in³；20kW、650kHz eight-level stacked LLC，800V->6V，峰值效率 96.5%。
- **Infineon hot-swap/serviceability。** Infineon 2025-10 支持 NVIDIA 800VDC，强调 CoolSiC JFET hot-swap 技术，让 server board 可在 800VDC bus 上安全 pre-charge/discharge 并更换，rack 其他 server 继续运行；同时估计 AI rack 从约 120kW 增至 500kW，并在十年末到 1MW。
- **Eaton MVSST。** Eaton MVSST 页面列出直接 MVAC 到 LVAC/DC，800VDC conversion efficiency >97%，solution cost 最多降 46%，footprint 最多降 40%，installation cycles 最多快 50%，应用包括 hyperscale、modular、edge、enterprise data centers 和 AI training/inference clusters。

## 4. 在研关键产品与高增长技术

### 4.1 在研产品预测

| 在研方向 | 阶段 | 关键公司 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率/放量判断 | 毛利率：基准/乐观/极度乐观 |
|---|---|---|---:|---:|---:|---|---|
| 15/35kV MVSST -> 800VDC/±400VDC | 产品发布/试点 | Eaton、Enphase、ABB、GE Vernova、Hitachi Energy、Schneider、Siemens、Delta、DG Matrix、Heron | $0.05-0.2B / $0.2-0.6B / $0.6-1.5B | $1-3B / $3-8B / $8-18B | $6-18B / $18-45B / $45-90B | 2026 低渗透；2027 新建 AI hall 1-5%；2028 5-12% | 28-40% / 40-55% / 55-68% |
| Distributed / multi-port SST | 样机/客户验证 | Enphase、DG Matrix、Heron、Eaton、Delta | $0.02-0.1B / $0.1-0.3B / $0.3-0.8B | $0.5-1.5B / $1.5-4B / $4-10B | $3-10B / $10-25B / $25-55B | 与 BESS/generator/utility 共同优化，2027 后高弹性 | 35-50% / 50-65% / 65-75% |
| MVDC campus bus（1.5kV+ 到 35kV DC） | 标准/pilot | ABB、Hitachi Energy、Siemens、Schneider、GE Vernova、Eaton、Mitsubishi、Current/OS 生态 | <$0.1B / $0.1-0.3B / $0.3-0.8B | $0.5-2B / $2-6B / $6-14B | $3-12B / $12-35B / $35-80B | 2027 仍主要 pilot，真正规模化 2028+ | 30-45% / 45-60% / 60-75% |
| 10kV SiC MOSFET / MV SiC modules | 早期商用/设计入 | Wolfspeed、Infineon、onsemi、ROHM、Mitsubishi Electric、Hitachi、ST | $0.02-0.1B / $0.1-0.25B / $0.25-0.6B | $0.4-1.2B / $1.2-3B / $3-7B | $2-7B / $7-18B / $18-40B | SST/MVDC 的核心瓶颈器件 | 45-60% / 60-70% / 70-80% |
| DC solid-state breaker / hybrid breaker | 认证/产品化 | ABB、Eaton、Schneider、Siemens、Mitsubishi、Littelfuse、Mersen、Sensata | $0.05-0.2B / $0.2-0.5B / $0.5-1B | $1-2.5B / $2.5-6B / $6-12B | $5-15B / $15-35B / $35-70B | 每个 DC 区段必配，标准锁定后高 ASP | 40-55% / 55-68% / 68-78% |
| AI power orchestration / dynamic power control | 软件+控制系统 | NVIDIA、Schneider/ETAP/AVEVA、Vertiv、Delta、Emerald AI、EPRI/PJM 生态 | $0.02-0.1B / $0.1-0.25B / $0.25-0.6B | $0.5-1.5B / $1.5-4B / $4-8B | $3-8B / $8-20B / $20-45B | 从电力设备附加功能变为 AI Factory 操作系统 | 50-70% / 70-80% / 80%+ |

### 4.2 重点在研技术解释

**MVSST：**  
核心价值是把 `13.8/15/35kV AC -> 800VDC/±400VDC` 集成为模块化电力电子系统，减少 MV transformer、LV switchgear、AC UPS、PDU 等多级链条。Enphase 的 IQ SST 走分布式 supercluster，1.25MW rack、342 个模块、内置冗余，声称 90% 模块参与也能继续运行。Eaton 走传统电气巨头路线，用 MVSST 嵌入数据中心/EV charging 场景。DG Matrix 进一步强调 multi-port，把 utility、generator、BESS、LVAC sources 做并行功率共享，避免单一集中 MV-SST 成为 single point of failure。

**10kV SiC：**  
Wolfspeed 2026-03 白皮书称 800VDC bus 需要 1200V SiC 做 AC/DC 与 DC/DC，conversion losses 可降 25-40%；对于 >5kV blocking voltage 的高压 SST，可用 10kV SiC MOSFET 简化 cell architecture。其 CPM3-10000-0300A 声称 conversion efficiency 99%，相比传统 HV silicon IGBT 可减少 50% thermal cooling system，并能 >10kHz switching，而 6500V IGBT 通常受限于几百 Hz。

**800V->12V/6V 直接转换：**  
这是利润率最高的“芯片附近电力”方向。NVIDIA Kyber 图示采用 64:1 LLC 从 800V 直接到 12V，NVIDIA 博客称该单级转换比传统多级方式更高效且面积少 26%。TI/ST/Renesas 都在推 800V 到 12V/6V/48V 的不同架构；短期 48V 复用生态最稳，长期 12V/6V 更能释放面积和瞬态响应。

**多时间尺度储能：**  
AI training/inference 的 synchronized load 会带来 grid-scale oscillations。800VDC 让 storage 可以接在最适合的位置：rack 附近 supercap/CBU 管毫秒到秒级 spikes，facility BESS 管秒到分钟级 workload ramp 与 generator transfer。这个方向将把传统 UPS 从“备电”升级成“动态功率缓冲和收益优化资产”。

## 5. 供给侧：产能、瓶颈、成本与毛利

### 5.1 产能结构

| 环节 | 主要产能/能力地区 | 关键公司 | 工艺/能力 |
|---|---|---|---|
| 数据中心电力系统集成 | 美国、欧洲、中国、台湾、印度/东南亚 | Vertiv、Schneider、Eaton、ABB、Siemens、GE Vernova、Hitachi Energy、Delta、Huawei Digital Power | UPS、switchgear、busway、PDU、power rack、controls、service network |
| 800V power shelves / sidecar | 台湾、中国大陆、美国、墨西哥、泰国 | Delta、Lite-On、Flex、Megmeet、AcBel、Bel Fuse、Vicor、Vertiv、Schneider | AC/DC rectifier、DC/DC brick、BBU、rack integration |
| WBG 半导体 | 欧洲、美国、日本、韩国、中国、台湾 | Infineon、ST、onsemi、Wolfspeed、ROHM、Mitsubishi、Navitas、AOS、Renesas、Innoscience、EPC、TI | 1200V SiC、650V/100V GaN、drivers、controllers、hot-swap |
| SST / MV power electronics | 美国、欧洲、日本 | Eaton、Enphase、ABB、GE Vernova、Hitachi Energy、Siemens、Schneider、DG Matrix、Heron、Delta | MV insulation、cascaded cells、DAB、AFE、SiC modules、controls |
| DC breakers/protection | 欧洲、美国、日本、中国 | ABB、Schneider、Eaton、Siemens、Mitsubishi、Littelfuse、Mersen、Sensata | Solid-state/hybrid DC interruption、arc suppression、selective coordination |
| Passives/magnetics/capacitors | 日本、台湾、中国、欧洲、美国 | TDK、Murata、Taiyo Yuden、Sumida、Yageo/KEMET、Nichicon、Nippon Chemi-Con、Vishay、Cornell Dubilier、Würth、Bel | 高频磁件、薄膜电容、EDLC、低 ESL/ESR 封装 |
| Busway/connector/cable | 美国、欧洲、中国、墨西哥、东南亚 | nVent/Starline、Legrand、Schneider、Eaton、ABB、Siemens、Amphenol、TE、Molex、Prysmian、Southwire、BizLink | 高压 DC busbar、touch-safe connector、liquid-cooled cable、monitoring |

### 5.2 供给瓶颈：至少 10 条

1. **认证与标准瓶颈。** 800VDC/±400VDC、2-wire/3-wire、grounding、connector、touch-safe、arc flash、maintenance procedure 需要 UL/IEC/OCP/ODCA/Current/OS 协同。
2. **DC fault interruption。** DC 没有自然过零，短路能量、选择性保护、半导体断路器散热和误动作成本高。
3. **WBG 器件良率与可靠性。** SiC wafer 缺陷、cosmic ray FIT、GaN dynamic Rds(on)、短路耐量、封装热循环都会影响 24/7 AI 工况。
4. **高频磁件与绝缘材料。** SST/LLC/DAB 需要高频 transformer、nanocrystalline/ferrite core、partial discharge 控制、灌封和绝缘寿命。
5. **电容/超级电容供给。** 800V CBU 需要低 ESR、高功率密度和长寿命，EDLC/薄膜电容的安全认证和热管理重要性上升。
6. **系统级测试工时。** 每个 rack/sidecar/SST 不是单板测试，而是功率、热、固件、保护、BESS、liquid cooling、load transient 的系统 burn-in。
7. **软件与控制算法。** 800VDC/MVSST 必须做 fast loop、droop control、fault isolation、grid ride-through、BESS dispatch；传统电气公司软件能力需补强。
8. **现场服务人才。** 数据中心运维团队需要 HVDC lockout/tagout、pre-charge/discharge、固件升级、SiC/GaN 故障诊断能力。
9. **长交期传统设备。** 即使 800VDC 减少部分设备，MV interconnection、transformer、switchgear、gas turbines 仍是项目开工瓶颈。
10. **客户设计冻结周期。** NVIDIA/hyperscaler reference design 一旦锁定，供应商进入窗口有限；错过 design-in 可能两代产品没有份额。
11. **安规与保险。** 保险商、AHJ、消防、NFPA、OSHA 对 800VDC 和 rack-level energy storage 的要求可能拖慢部署。
12. **国产替代链条不完整。** 中国/亚洲公司在电源制造强，但 MVDC breaker、10kV SiC、MVSST 控制认证和全球 hyperscaler 服务网络仍需爬坡。

### 5.3 BOM / 成本拆分

| 产品 | 成本构成估算 | 毛利决定因素 |
|---|---|---|
| 800V sidecar / power rack | WBG/Si power semis 15-25%；magnetics 10-18%；capacitors/CBU 8-15%；busbar/connector/protection 15-25%；control/sensing 5-10%；enclosure/thermal 10-18%；assembly/test/warranty 10-18% | NVIDIA/客户认证、功率密度、效率、冗余、交期、现场服务 |
| 800V->48/12/6 DC/DC module | GaN/SiC/MOSFET 25-40%；magnetics 15-25%；drivers/controllers 8-15%；substrate/thermal/package 10-20%；test 8-15%；其他 5-10% | 效率、W/in³、热阻、瞬态响应、良率、封装专利 |
| MVSST | MV SiC modules 20-35%；HF transformer/magnetics 10-18%；DC-link capacitors 10-18%；MV insulation/enclosure 10-20%；control/software 5-12%；thermal 5-10%；certification/test 8-15% | 可用性、冗余、MV 认证、并网/微电网控制、模块更换速度 |
| DC breaker / eFuse / hot-swap | Semiconductor interrupter 25-45%；sensors/control 10-18%；arc/insulation/enclosure 15-25%；mechanical/contact 10-20%；certification/test 8-15% | 选择性保护、分断速度、寿命、误动作概率、UL/IEC 认证 |
| Supercap/CBU | Cells 35-55%；BMS/control 8-15%；thermal/enclosure 10-20%；busbar/protection 10-18%；test 5-10% | 功率密度、安全、循环寿命、与 GPU 调度联动能力 |

### 5.4 价格传导机制

- **短期：按交期溢价。** 2026-2027 真实瓶颈是“能否通过认证并按时交付”，不是最低成本。供不应求产品可通过 expedited delivery、工程服务、冗余配置和 extended warranty 提价。
- **中期：按效率分享收益。** 若 800VDC 全链路提高 2-5% 效率，客户愿意把部分电费/容量收益让给供应商，尤其在电力受限地区。
- **长期：模块标准化后硬件毛利下行，控制/保护/服务毛利上行。** 普通 power shelf 会被 Delta/Lite-On/Megmeet/Flex 等制造能力压毛利；DC breaker、hot-swap、MVSST controls、AI power orchestration 更持久。

## 6. 竞争格局与壁垒

### 6.1 市场结构

| 层级 | 2026 竞争结构 | 头部集中度判断 | 说明 |
|---|---|---:|---|
| 数据中心电力系统 | Vertiv/Schneider/Eaton/ABB/Siemens/Delta/GE/Hitachi | CR5 55-70% | 客户看全球交付、服务和认证，头部优势明显 |
| 800V sidecar/power rack | Delta/Vertiv/Schneider/Eaton/Flex/Lite-On/Megmeet | CR5 45-65% | 早期由 reference design 与产能决定，后期制造竞争加剧 |
| WBG 半导体 | Infineon/ST/onsemi/Wolfspeed/ROHM/Navitas/Renesas/AOS/TI | CR6 60-75% | SiC/GaN 工艺、封装和可靠性壁垒高 |
| MVSST | Eaton/Enphase/ABB/GE/Hitachi/DG Matrix/Heron/Delta | 暂无稳定 CR | 新市场，客户认证会迅速拉开差距 |
| DC breaker/protection | ABB/Schneider/Eaton/Siemens/Mitsubishi/Littelfuse/Mersen | CR5 60-80% | 认证和 failure liability 极高，集中度高 |
| Power orchestration 软件 | NVIDIA/Schneider ETAP AVEVA/Vertiv/Delta/Emerald AI | 高不确定 | 与 AI workload scheduler、电网模型和设备遥测绑定 |

### 6.2 可量化壁垒清单：为什么能定价

| 壁垒 | 量化/验证指标 | 为什么能定价 |
|---|---|---|
| 效率 | 单级 96.5-98.5%，系统提升 2-5% | 电力受限时，1MW rack 节省的电和冷却可资本化 |
| 功率密度 | ST 2,500W/in³，TI >2,000W/in³，Delta 1.1MW/rack | 白空间可多放 GPU，客户按 token/MW 付费 |
| 认证 | UL/IEC/OCP/客户 AVL/AHJ/保险 | 没认证不能进站；认证周期 12-24 个月构成排他 |
| 可用性 | Enphase 目标 99.999%，90% 模块参与仍运行 | AI rack downtime 的机会成本极高 |
| 服务网络 | 130+ 国家、24/7 现场响应、备件 SLA | Hyperscaler 要全球复制，不愿用无服务供应商 |
| 控制算法 | sub-ms response、pre-charge、selective trip、BESS dispatch | 保护误动作或不动作都会造成数千万美元级损失 |
| 供应能力 | MW/GW 级产线、系统 burn-in、质量追溯 | AI Factory 同时开工，客户为确定性交订金 |
| 生态绑定 | NVIDIA reference design、OCP、Schneider/ETAP/Omniverse | 进入 reference design 后复制性强、切换成本高 |

### 6.3 价值捕获判断

长期高 ROIC/高毛利最可能在三层：

1. **保护与控制半导体/模块。** hot-swap/eFuse/DC breaker/isolated driver/MCU/BMS 是 800VDC 安全边界，单价占比不一定最高，但 ASP、毛利和粘性最高。
2. **MVSST / multi-port SST 平台。** 如果能证明可用性与认证，MVSST 可以吃掉传统 transformer + UPS + PDU 的部分价值，并叠加软件控制和服务。
3. **AI power orchestration。** 当 GPU workload scheduler、BESS、supercap、SST 和电网响应联动，软件层可按 MW、rack 或收益分成收费。

普通 rack metalwork、低差异 busbar、低压电源装配更容易被规模制造竞争压毛利，但在 2026-2027 供不应求窗口仍有价格弹性。

## 7. 2026 关键变化：3 个最可能拐点

### 7.1 从“800V 概念”进入“GTC/OCP 产品化”

NVIDIA 已发布 800VDC page、技术博客和白皮书，合作公司跨电气系统、power component 和 silicon 三层。TI、ST、Delta 在 GTC 2026 直接展示产品；Schneider 在 2026-03 发布 Vera Rubin reference design 和 800VDC 白皮书；Vertiv 计划 2026H2 产品组合发布。**这意味着 2026 的订单不是大规模收入，而是 design-in、AVL、样机和预订单。**

### 7.2 Rack-level sidecar 成为立即可落地方案

Schneider 明确把 800VDC power racks/sidecars 作为 immediate enabler。原因很实用：它可以接入现有 415/480VAC 基础设施，把转换移出 IT rack，同时不给整个园区改 MVDC。**2026 最可能赚钱的是 sidecar/power shelf/DC-DC/protection，不是完整 MVDC。**

### 7.3 动态功率管理成为电力设备新规格

NVIDIA、PNNL、ZincFive 等资料都指向同一问题：AI workload 不是平稳负载。2026 之后，UPS/BESS/CBU/超级电容/SST 控制器需要按毫秒到分钟多时间尺度响应。**这会把电力设备从“静态容量件”变成“高速控制件”。**

## 8. 2027 关键变化：3 个最可能拐点

### 8.1 Kyber/Rubin Ultra 让 800VDC 进入新建 AI Factory 主设计

NVIDIA 明确 full-scale 800VDC data centers 与 2027 Kyber rack-scale 系统同步。若 Rubin Ultra/Kyber 交付按计划推进，2027 新建高密 AI Factory 会把 800VDC 从可选项变成默认讨论项。乐观情景下，高密新 rack 800VDC 渗透率可到 15-25%；极度乐观可到 35-45%。

### 8.2 MVSST 从样机进入 field pilot

Eaton、Enphase、DG Matrix、Wolfspeed 的 2026 信息说明 MVSST 已从实验室转向产品定义。2027 的关键观察点是：单个 1-10MW block 是否在真实 AI hall 连续运行、是否通过 AHJ/保险/客户 SLA、是否能和 BESS/generator 并行运行。若能，2028 收入会陡峭上升。

### 8.3 MVDC 标准和 DC breaker 开始成为稀缺资产

MVDC 大规模商用仍偏后，但 2027 会先体现为 DC breaker、DC switchgear、insulation monitoring、ground fault detection、protection coordination 的标准和小批量订单。这个环节一旦标准锁定，头部电气公司和保护器件公司将拿到高毛利窗口。

## 9. 头部公司与完整公司图谱

### 9.1 标准与平台牵引

- **NVIDIA**：800VDC reference architecture、Kyber/Rubin 绑定、OCP 推动者。
- **OCP、ODCA、Current/OS、EPRI、PJM、PNNL/DOE**：标准、模型、grid interaction、负载动态研究。

### 9.2 数据中心电力系统与集成

- **Vertiv**：UPS、DC power、thermal、integrated modular solutions；800VDC portfolio 2026H2；全球数据中心服务网络强。
- **Schneider Electric / APC / ETAP / AVEVA**：validated reference design、EcoStruxure、ETAP electrical modeling、Omniverse digital twin；800VDC sidecar 白皮书。
- **Eaton**：MVSST、UPS、switchgear、busway、breaker；MVSST 页面给出成本/面积/效率/安装周期指标。
- **ABB**：与 NVIDIA 合作 800VDC；DC breaker、MV UPS、solid-state electronics；SACE Infinitus DC breaker 方向关键。
- **GE Vernova Grid Solutions**：与 NVIDIA 800VDC reference design；grid interconnection、MV equipment、AI factory power。
- **Hitachi Energy**：grid-to-rack 800VDC 架构；transformer/HV/grid 数字化全球龙头，宣布 $9B 全球扩产。
- **Siemens、Mitsubishi Electric、Legrand、Socomec、Huawei Digital Power、nVent/Starline、PDI**：switchgear、busway、UPS、DC protection、rack power distribution。

### 9.3 800V power shelf、sidecar、服务器电源

- **Delta Electronics**：GTC 2026 800VDC power rack、BBU、CDU、microgrid/SST/SOFC；美国数据中心 UPS 累计部署 >6.5GW。
- **Lite-On、Flex、Megmeet、AcBel、Bel Fuse、Vicor、Murata Power、Advanced Energy、TDK-Lambda、Artesyn/Advanced Energy、FSP**：服务器 PSU、DC/DC、power shelves、模块化电源。
- **BizLink、Lead Wealth、Amphenol、TE Connectivity、Molex、Samtec、Hubbell、Panduit**：高压/高速连接、cable、busbar、rack wiring。

### 9.4 功率半导体、控制与保护

- **Texas Instruments**：800V hot-swap、800V->6V、6V-><1V、30kW 800V PSU、CBU、isolated modules、MCU/driver。
- **STMicroelectronics**：800V->50V/12V/6V，6kW 12V PDB、20kW 6V PDB，GaN/SiC/analog/MCU。
- **Infineon**：CoolSiC JFET hot-swap、Si/SiC/GaN complete solution、IBC、TLVR、400/800V protection。
- **onsemi**：Si/SiC for SST、PSU、800VDC distribution、core power，intelligent monitoring/control。
- **Renesas**：OCP whitepaper，800V->48V 16:1 LLC DCX、800V->12V 64:1、mid-voltage GaN sidecar。
- **Navitas**：100V GaN、650V GaN、high-voltage SiC，13.8kVAC->800VDC 和 800V->54/12V 路线。
- **AOS**：1200V SiC、650V/100V GaN、stacked-die MOSFET、16-phase controllers；声称 5% 效率改善、45% 铜需求下降。
- **Wolfspeed**：1200V/10kV SiC、SST 白皮书；10kV MOSFET 支持 >10kHz、99% conversion efficiency 级别路线。
- **ROHM、Mitsubishi Electric、Toshiba、Fuji Electric、Power Integrations、EPC、Innoscience、MPS、Analog Devices、Vishay、Littelfuse、Nexperia、Qorvo/UnitedSiC**：WBG、drivers、controllers、protection、power modules。

### 9.5 SST / MVDC 专门玩家

- **Enphase**：IQ SST，1.25MW rack、342 modules、98.5% efficiency、99.999% availability、15/35kV->800VDC，利用 87.8M microinverter 出货制造平台。
- **DG Matrix**：Interport multi-port SST，MV utility/generator/BESS/LVAC concurrent power sharing，block-level pulse energy。
- **Heron Power**：NVIDIA 800VDC partner list 中的数据中心 power systems 公司，定位高功率电力电子。
- **Eaton、ABB、GE Vernova、Hitachi Energy、Schneider、Siemens、Delta、Mitsubishi Electric**：从传统 MV/LV 电气向 MVSST/MVDC 延伸。

### 9.6 储能、超级电容、飞轮与电能质量

- **BESS/UPS**：Vertiv、Schneider、Eaton、Delta、Saft、Tesla Megapack、Fluence、CATL、BYD、Powin、Samsung SDI、LG Energy Solution、ZincFive。
- **超级电容/薄膜电容**：Skeleton Technologies、Eaton、Maxwell/Tesla、Nichicon、Nippon Chemi-Con、Cornell Dubilier、KEMET/Yageo、Kyocera AVX、Vishay、TDK、Panasonic。
- **飞轮 UPS/动态储能**：Piller、Active Power、Vycon、ABB、Schneider、Eaton。飞轮更适合秒级 ride-through 和 power quality，超级电容更贴近 rack 级毫秒响应。

### 9.7 磁性元件、绝缘、热管理和材料

- **磁件/电感/变压器**：TDK、Murata、Sumida、Würth Elektronik、Pulse/Yageo、Bel Fuse、Coilcraft、Vishay、Eaton、Delta。
- **电容/绝缘/材料**：DuPont、3M、Rogers、Hitachi Chemical/Showa Denko、Toray、Mitsubishi Chemical、KEMET/Yageo、TDK、Nichicon。
- **液冷/热管理协同**：Vertiv、Delta、CoolIT、Boyd、Modine、nVent、Danfoss、Parker、Aavid/Boyd、Asetek、Johnson Controls、Stulz。

## 10. 情景化投资结论

### 10.1 市场规模汇总

| 口径 | 未来 3 个月 | 未来 1 年 | 未来 2 年 |
|---|---:|---:|---:|
| 基准：800VDC/MVSST/MVDC 相关订单 | $1.5-4B | $20-45B | $70-160B |
| 乐观 | $4-10B | $45-100B | $160-350B |
| 极度超预期乐观 | $10-20B | $100-220B | $350-700B |

解释：极度乐观情景不是说所有设备已经成熟，而是假设 2026H2-2027 的 hyperscaler 新建 AI Factory 把 800V sidecar、DC/DC、DC protection、BESS/CBU 和 MVSST 预订单全部前置锁定，订单先于收入 6-18 个月出现。

### 10.2 最值得跟踪的 15 个指标

1. NVIDIA Kyber/Rubin Ultra 是否按 2027 节奏进入客户新建 hall。
2. Vertiv 800VDC portfolio 是否按 2026H2 发布，并披露首批客户/项目。
3. Delta 660kW/1.1MW 800VDC rack 方案是否从展示转为量产交付。
4. Schneider 800VDC sidecar reference design 是否进入 hyperscaler 标准图纸。
5. Eaton MVSST 是否拿到真实 AI data center pilot。
6. Enphase IQ SST 是否公布样机、认证、首个客户和制造节奏。
7. TI/ST/Renesas 800V->6V/12V 是否进入服务器 ODM 量产验证。
8. Infineon hot-swap/eFuse 是否成为 NVIDIA 800V maintenance 标准件。
9. DC breaker 是否出现 OCP/IEC/UL 认可的标准化规格。
10. 800V connector/busway 是否有统一接口和 touch-safe 规范。
11. AI workload power transients 是否被写入 UPS/BESS/CBU 招标要求。
12. 10kV SiC/MV SiC modules 是否完成长期可靠性测试。
13. 保险商/AHJ 是否接受 800V rack-level energy storage。
14. Hyperscaler capex 是否继续上修，尤其美国 2026-2027 GW 项目是否落地。
15. 电网/变压器交期是否继续拉长，若继续拉长，MVSST 溢价上升。

### 10.3 最强 alpha 与 beta

- **最强 alpha：DC protection/hot-swap/eFuse、MVSST 控制平台、power orchestration 软件。** 这些环节决定安全和 uptime，客户愿意付高价。
- **最强 beta：800V sidecar/power rack、800V->12/6V DC/DC、WBG semiconductors、supercap/CBU。** 与 Rubin/Kyber/MI400 高密 rack 数量高度相关。
- **最确定现金流：传统电力巨头的 800VDC/MVSST 延伸。** Schneider、Eaton、Vertiv、ABB、Delta、Hitachi Energy 等在传统 UPS/switchgear/busway 订单中已经受益，800VDC 是额外期权。

## 11. 主要来源与数字锚点

| 来源 | 关键事实 |
|---|---|
| [NVIDIA 800 VDC Architecture](https://www.nvidia.com/en-us/data-center/technologies/800-vdc-architecture/) | 800VDC 减少转换/配电体积，降低 current、copper use、cable bulk；合作名单覆盖电气系统、power component、silicon |
| [NVIDIA 800VDC technical blog](https://developer.nvidia.com/blog/building-the-800-vdc-ecosystem-for-efficient-scalable-ai-factories/) | 800VDC 同线径比 415VAC 多承载 157% 功率；传统端到端效率可低于 90%；Kyber 采用 64:1 LLC，面积少 26%；OCP 2025 发表白皮书 |
| [NVIDIA 800VDC path forward blog](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) | full-scale 800VDC data centers 与 2027 Kyber rack-scale systems 同步 |
| [Vertiv + NVIDIA 800VDC](https://www.vertiv.com/en-us/about/news-and-events/corporate-news/from-vision-to-readiness-vertiv-collaborates-with-nvidia-to-advance-800-vdc-platform-designs-to-power-the-next-generation-of-ai-factories/) | 800VDC portfolio 计划 2026H2 发布，支持 2027 Rubin Ultra；已参与多个 GW 级 AI Factory early design |
| [Delta GTC 2026 800VDC](https://www.deltapowersolutions.com/en/mcis/news-2026-delta-exhibits-energy-saving-solutions-for-800-vdc-at-nvidia-gtc-2026.php) | 660kW In-Row Power Rack、每 shelf 80kW BBU、AC-DC 效率最高 98%、3MW/2.4MW CDU、SST/SOFC microgrid |
| [Delta Data Center World 2026](https://www.delta-americas.com/en-US/news/delta-unveils-integrated-power%2C-cooling%2C-and-infrastructure-architecture-for-ai-data-centers-at-data-center-world-2026) | 美国数据中心 UPS 部署 >6.5GW；800VDC rack distribution 最高 1.1MW/rack、最高 98% efficiency |
| [TI 800VDC with NVIDIA](https://www.ti.com/about-ti/newsroom/news-releases/2026/2026-03-16-ti-unveils-complete-800-vdc-power-architecture-for-future-generation-ai-data-centers-with-nvidia.html) | 800V hot-swap、800V->6V 97.6% peak efficiency、>2000W/in³、30kW 800V PSU、CBU |
| [ST 800VDC portfolio](https://newsroom.st.com/media-center/press-item.html/t4766.html) / [ST technical blog](https://blog.st.com/800-v-hvdc-data-center/) | 800V->12V/6V；6kW 12V board 97.5%、2,500W/in³；20kW 6V board 96.5% |
| [Infineon 800VDC](https://www.infineon.com/press-release/2025/INFXX202510-003) | CoolSiC JFET hot-swap；AI rack 从 120kW 到 500kW、十年末 1MW；单级最高 98% efficiency 目标 |
| [onsemi 800VDC](https://www.onsemi.com/company/news-media/press-announcements/en/onsemi-collaborates-with-nvidia-to-accelerate-transition-to-800-vdc-power-solutions-for-next-generation-ai-data-centers) | Si/SiC 支持 SST、PSU、800VDC distribution、core power，全路径 intelligent monitoring/control |
| [Renesas/OCP power architecture](https://www.opencompute.org/documents/power-architecture-evolution-in-data-centers-pdf) | 800V 2/3-wire；16:1 800V->48V LLC DCX 98%；sidecar AC/DC building block 约 20kW+；800V 可减少近 50% copper weight |
| [Navitas 800VDC](https://ir.navitassemi.com/node/11116/pdf) | 100V GaN、650V GaN、650-6500V SiC；13.8kVAC->800VDC；Rubin Ultra 相关 |
| [AOS 800VDC](https://www.aosmd.com/sites/default/files/2025-10/SiC-and-GaN-for-Next-Gen-AI-Factories-using-800-VDC-Architecture.pdf) | 1200V SiC、650V/100V GaN；声称最高 5% end-to-end efficiency improvement、45% copper reduction |
| [Eaton MVSST](https://www.eaton.com/us/en-us/catalog/medium-voltage-power-distribution-control-systems/medium-voltage-solid-state-transformer.html) | MVSST 直接 MVAC->LVAC/DC；最多 46% solution cost reduction、40% footprint reduction、50% faster installation、>97% 800VDC efficiency |
| [Enphase IQ SST](https://investor.enphase.com/news-releases/news-release-details/enphase-energy-announces-development-iq-solid-state-transformer) | 1.25MW rack、342 modules、98.5% efficiency、99.999% availability、15/35kV->800VDC/±400VDC、2031 美国 AI DC TAM >11GW |
| [Wolfspeed SiC SST whitepaper](https://assets.wolfspeed.com/uploads/2026/03/Wolfspeed_Powering_AI_with_reliable_SiC-based_solid-state_transformers_white_paper.pdf) | 1200V SiC 支持 800V bus；conversion losses 降 25-40%；10kV SiC >10kHz，99% conversion efficiency，冷却系统可减 50% |
| [DOE/PNNL Data Center EMT Models](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) | Design 5 MVSST；Design 6 MVDC；LVDC/SST 数年内部署，MVDC field service 更远 |
| [DG Matrix multi-port SST whitepaper](https://media.datacenterdynamics.com/media/documents/Transforming_Data_Centers_into_AI_Factories_Multi-Port_Solid-State_Transformer_OrJ5uMb.pdf) | 对比集中 MV-SST 与 multi-port Interport，强调 utility/generator/BESS concurrent power sharing 和 block-level pulse energy |
| [ABB + NVIDIA](https://resources.news.e.abb.com/attachments/published/129805/en-US/D1659BBF0D16/20251013_ABB_to_develop_next-generation_AI_data_centers_with_NVIDIA_EN.pdf) / [ABB 800VDC whitepaper](https://resources.news.e.abb.com/attachments/published/129788/en-US/3515A12A5C51/ABB_800_VDC_NVIDIA_white_paper.pdf) | 800VDC 支持 1MW server rack；全球 DC demand 80GW(2024)->220GW(2030)；AI 约占增长 70%；marine 1000VDC 系统节能 20-40% |
| [Hitachi Energy 800V architecture](https://www.hitachi.com/content/dam/hitachi/global/en/press/articles/2025/10/1015c/251015c.pdf) | 支持 NVIDIA 800VDC；2025-2030 AI DC capacity 可达 125GW；Hitachi Energy 全球 $9B 扩产 |
| [Schneider + NVIDIA GTC 2026](https://www.se.com/us/en/about-us/newsroom/news/press-releases/schneider-electric-teams-with-nvidia-to-develop-validated-blueprints-to-design-simulate-build-operate-and-maintain-gigawattscale-ai-factories-69b82f61aa1027e04205d273/) / [Schneider WP213](https://www.se.com/us/en/download/document/SPD_WP213_EN/) | Vera Rubin reference design；800VDC sidecar 是 immediate enabler；ETAP/AVEVA/Omniverse digital twin |
| [McKinsey 2026 $7T AI DC buildout](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-7-trillion-dollar-data-center-build-out-how-industrials-can-capture-their-share) | 设备商要应对高密、高动态 compute；transformers、switchgear、cooling、skilled labor 成为 buildout bottlenecks |
| [IEA Energy and AI](https://www.iea.org/reports/energy-and-ai/executive-summary%C2%A0) / [IEA Key Questions 2026](https://www.iea.org/reports/key-questions-on-energy-and-ai) | 2024 数据中心用电 415TWh、全球 1.5%；美国占 45%；约 20% planned DC projects 有 delay 风险；transmission 4-8 年，transformer/cable waits 三年翻倍 |
| [Uptime Institute 2026 giant data center report](https://intelligence.uptimeinstitute.com/sites/default/files/2026-01/UI%20Field%20report%20194_Giant%20data%20center%20power%20plans%20reach%20extreme%20levels.pdf) | >100MW 数据中心 proposal 350+；2025 proposed power 181GW；预计仅 25% planned provisioned power 会 active utilized；AI 占 planned power 近 60% |
| [Vertiv Frontiers 2026](https://www.vertiv.com/48d902/globalassets/content---assets-2025/documents/vertiv-frontiers-2026-report-en-gl-web.pdf) | 高压 DC 预计随 AI densification 提升；挑战包括 safety procedures、qualified staff、higher upfront costs；未来集成 MV/BESS/UPS/advanced controls |
| [ZincFive 2026 Energy Storage report](https://zincfive.com/wp-content/uploads/2026/03/2026-Data-Center-Energy-Storage-Industry-Insights-Report.pdf) | AI dynamic power 对 UPS 的影响集中在 transients/load spikes、battery stress、faster controls；battery chemistry 选择关注 power density/safety/uptime/serviceability |

---

一句话总结：**2026 年买的是 800VDC 生态的“设计位”和“瓶颈件”，2027 年看 Kyber/Rubin Ultra 把新建 AI Factory 推到 800VDC 主线，2028 年之后才真正考验 MVSST/MVDC 能否从高赔率期权变成园区电力标准。**
