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
