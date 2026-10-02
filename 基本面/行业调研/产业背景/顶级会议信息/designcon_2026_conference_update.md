# DesignCon 2026：AI 数据中心把电子设计推入 224G 部署、448G 探路和 1.6T 互连时代

> 调研范围：截至 2026-05-08 可检索的 DesignCon 2026 官方议程、获奖论文、展商发布、媒体会后报道、公司新闻稿及少量非官方讨论。未参考本地项目内既有文件或信息。DesignCon 2026 于 2026-02-24 至 2026-02-26 在 Santa Clara Convention Center 举行。

## 0. 核心结论

DesignCon 2026 的最大变化是：它已经从“高速板级 SI/PI 工程会议”转成“AI 数据中心物理层系统大会”。会场不再只讨论 PCB 上一条差分线怎么跑，而是在讨论从 die、interposer、package、top-side connector、copper flyover、optical module、switch ASIC、rack power、liquid cooling 到 agentic EDA 的整条链路。

最强信号有 7 个：

1. **224G 已从验证进入部署，448G 已从概念进入工程探路。** Samtec、Luxshare、Molex/Arista、Marvell、Keysight 等都围绕 224G/448G 做展台演示或技术论文；Best Paper 里直接出现“448Gbps scale-up/scale-out”“448Gbps via/fan-out”“400G PAM6 SerDes”等主题。
2. **PCIe 7.0 是 2026 验证主战场，PCIe 8.0 已开始 256 GT/s pathfinding。** Keysight/Teledyne/Anritsu/Synopsys 聚焦 PCIe 7.0 128 GT/s 测量，Marvell 和 Synopsys展示 PCIe 8.0-class 256 GT/s 电气性能。Marvell 明确称 PCIe 8.0 预计 2028 完成，x16 可达 1 TB/s 双向带宽。
3. **铜没有死，但铜的形态变了。** 传统长 PCB 走线继续被压缩，机会转向 co-packaged copper、near-ASIC copper、top-side interconnect、active copper cable、active electrical cable、retimer/redriver。Luxshare 展示 448G KOOLIO CPC-to-OSFP Airchannel 链路，支持超过 90 GHz 带宽；1.6T OSFP AEC 可在 27AWG 4 米、30AWG 3 米稳定工作；OSFP-XD PCIe 6.0 AEC 配 Marvell Alaska P retimer 可到 7 米、PCIe 6 x16、256 GB/s。
4. **光互连进入 1.6T 量产前夜，但 CPO/OIO 不是立刻替代 pluggable。** 2026 年 800G+ 光模块成为 AI 数据中心标准件，1.6T 从小基数进入大规模爬坡；但会场同时强调 LPO、AEC/ACC、CPC、CPO/OIO 并存，短距铜和中远距光会分层。
5. **AI 网络瓶颈从“有没有 GPU”外溢到“数据如何移动、供电如何送达、热如何拿走”。** ConnectorSupplier 会后报道提到 AI 机柜功耗继续上行，单个下一代 Rubin Ultra/Kyber rack 预期约 600 kW，2030 年前 1 MW rack 被专家视为可能情景。这直接把 power integrity、busbar、liquid cooling、leak detection、cold plate、high-current connector 拉成 DesignCon 主角。
6. **Agentic AI 从展会话题变成设计工具路线。** 2025 年还是早期讨论，2026 年已经有 keynote、panel 和“Multi-Agent AI Systems for Autonomous Signal Integrity Analysis of PCB & Package Designs”技术论文。短期不是替代工程师，而是压缩 SI/PI 建模、仿真设置、debug、测试脚本和跨工具联动时间。
7. **中国/亚洲供应链在高端互连论文与展台上的存在感显著上升。** Best Paper 里 Alibaba Group/Alibaba Cloud/Synopsys/Shennan Circuit/New H3C 的 PCIe 7.0 PCB 技术论文获奖，Alibaba/Luxshare/Synopsys 的 top-side interconnect 论文获奖；Luxshare、FIT、BizLink 等在展商和 sponsor 里位置靠前。

## 1. 公开材料地图：会场规模、议题和一手信号

### 1.1 会场事实

- 官方页面称 DesignCon 2026 有 **100+ sessions、15 tracks**，覆盖 signal integrity、power integrity、high-speed link design、machine learning。
- ConnectorSupplier 会后报道给出更细数字：2026 年为第 26 届，会议有 **183 篇 technical papers、3 场 keynote、tutorials、boot camps、poster reviews**，技术论文和 panels 分布在 **15 个深度技术 track**；展商从 2025 年 **173 家增至 2026 年 202 家**，增幅约 **16.8%**；其中 **40+ 家**供应 copper/fiber connectors 和 cable assemblies。
- 赞助结构本身就是行业热度表：Host 是 Amphenol；Diamond 为 Keysight、Molex、Samtec；Platinum 为 Cadence、Luxshare、Rohde & Schwarz、TE Connectivity、Tektronix；Gold 包括 Anritsu、Bellwether、BizLink、FIT、Hirose、Synopsys、Teledyne LeCroy。

### 1.2 Keynotes：三条主线

- Purdue Joseph Lukens：“From Spooky Action at a Distance to the Quantum Internet”，对应长期通信/网络物理极限。
- Agentrys Mark Ren：“Agentic AI for Chip Design”，对应 EDA 工作流自动化。
- NASA Goddard Bhanu Sood：“Designing for Discovery”，对应高可靠 mission-critical system design。

这三个 keynote 拼起来的含义是：DesignCon 的技术半径已经从单板信号完整性，扩展到“下一代计算系统如何被设计、验证、供电、散热、互连和长期可靠运行”。

### 1.3 2026 Best Paper：获奖题目透露的重点

2026 Best Paper 获奖题目高度集中在 AI data center channel、PCIe 7.0、448G、PAM6、EMI 和 top-side interconnect：

- 400G Channels for AI Applications: Passive & Active Copper Cable Assemblies to Enable Scale Up/Scale Out，作者来自 TE Connectivity 和 Semtech。
- 448Gbps: Challenges for Scale-Up & Scale Out Applications，作者来自 Meta、Arista Networks、Molex。
- Analytical Derivation of P/N Skews in Coupled Channels: Impact on 400G PAM6 SerDes，作者来自 Cisco。
- Breakthroughs in PCB Technology for PCIe 7.0 Interconnects，作者来自 Alibaba Group、Alibaba Cloud、Synopsys、Shennan Circuit、New H3C。
- Targeted EMI Mitigation Using Emission Source Imaging & 3D-Printed Absorbers，作者来自 Missouri S&T、Molex、HPE、Juniper。
- Top Side Interconnect Enabling for PCIe 7.0 & Beyond，作者来自 Alibaba Group、IEEE、Synopsys、Luxshare。
- Via & Fan-Out Designs for 448Gbps: SI vs Technology，作者 Mike Tucker，Shennan Circuits。

关键词不是“单一速度升级”，而是 **channel architecture 重构**：skew、via/fan-out、PCB材料、top-side connector、copper cable、PAM6/FEC/measurement、EMI mitigation 全部在同一张图里。

## 2. 重点方向和相对过去的转折

### 2.1 从 112G/800G 过渡到 224G/1.6T，448G 被提前拉进工程视野

过去两年行业主线是 112G PAM4、400G/800G 光模块、PCIe 5/6、CXL 早期生态。DesignCon 2026 的主线变成：

- **112G**：成熟量产，仍是很多 active optics、LPO、DDR/高速测试和 legacy AI fabric 的基础。
- **224G**：进入部署和生态互操作阶段。Samtec 展示 Si-Fly HD CPC 224G；Synopsys 224G PHY 与 Hirose、Luxshare、Samtec 平台互操作；Luxshare 展示 224G CPC-to-CPC cable。
- **448G**：不再只是 roadmap。Samtec 展示 BE130 test assembly 跑 448G differential signals；Luxshare 展示 448G KOOLIO CPC-to-OSFP Airchannel，带宽超过 90 GHz；Molex/Arista 的 224G/448G skew management 论文入围 Best Paper；Shennan 的 448G via/fan-out 论文获奖。
- **1.6T**：光模块和电互连系统开始进入量产前夜。Keysight 展示 1.6T interconnect benchmark；Luxshare 展示 1.6T OSFP AEC/ACC；Anritsu 做 224/448G electrical/optical 到 145 GHz 以上测试。

结论：AI cluster 的 scale-up/scale-out 需求让 lane-rate 路线被明显前置。2026 年不再是“800G 刚起来，1.6T 慢慢看”，而是 800G 成为标配、1.6T 进入部署、448G/3.2T 的测试和材料问题提前暴露。

### 2.2 PCIe 7.0/8.0：标准周期还长，但资本开支已经在买 pathfinding

Keysight 展示 PCIe 7.0 PHY/protocol validation，使用 UXR oscilloscope、M8050A BERT、PCIe test software。Teledyne LeCroy 展示 live PCIe 7.0 transmitter measurements，用 65 GHz 12-bit oscilloscope 和 Anritsu MP1900A BERT 测 Synopsys PCIe 7.0 device operating at 128 GT/s。Anritsu 展示 PCIe 7.0 over optics，SiPhx 800G LPO module，64 Gbaud PAM4，128 GT/s TDECQ。

更重要的是 PCIe 8.0 已提前进入展示：

- Marvell 展示 PCIe 8.0 SerDes at **256 GT/s**，并称 PCIe 8.0 预计 **2028** 完成，x16 可达 **1 TB/s bidirectional bandwidth**。
- Synopsys 展示 PCIe 8.0-class **256 GT/s electrical performance**，包括 eye diagram 和 receiver performance。

这意味着短期收入不一定来自 PCIe 8.0 终端设备，而来自更早环节：SerDes IP、PHY IP、retimer/redriver、connector、test fixture、BERT、oscilloscope、VNA、channel modeling、compliance software。DesignCon 上“工程探路”的钱比标准完成早 18-30 个月花出去。

### 2.3 Copper vs optics：不是二选一，而是距离、功耗、延迟和可维护性的分层

市场常见叙事是“光会替代铜”。DesignCon 2026 给出的更细结论是：**长距和跨 rack 的确定性向光迁移，短距和 near-ASIC 的确定性向更高级铜迁移。**

- Copper 的新位置：CPC、top-side connector、flyover cable、AEC/ACC、retimerized OSFP-XD、near-chip cable。
- Optics 的新位置：800G/1.6T pluggable、LPO、CPO/OIO、OCS、coherent ZR/ZR+、scale-across DCI。
- 两者的共同瓶颈：BER、FEC latency、equalization power、thermal density、mechanical tolerances、manufacturing metrology。

Luxshare 的 7 米 PCIe 6/CXL OSFP-XD AEC 和 448G CPC-to-OSFP 演示，是“铜还没死”的强信号；TrendForce 的 800G+ 模块 2026 年出货占比超过 60%，是“光进入 AI 标配”的强信号。这两个信号不冲突。

### 2.4 PCB 不再只是成本件：材料、via、fan-out、top-side 成为系统性能变量

2026 Best Paper 把 PCB 推到中心位置：

- Alibaba/Alibaba Cloud/Synopsys/Shennan/New H3C 的 PCIe 7.0 PCB breakthrough 获奖。
- Alibaba/Synopsys/Luxshare 的 top-side interconnect for PCIe 7.0 & beyond 获奖。
- Shennan 的 448G via/fan-out 设计获奖。

这说明 AI 数据中心高端 PCB 的竞争点从层数、HDI、低损耗材料，继续推进到：

- connector footprint 和 mating interface 的 return loss/crosstalk 容差；
- via stub、backdrill、fan-out geometry；
- PCB 材料 Dk/Df 与铜粗糙度模型；
- top-side cable connector 绕开长板走线；
- 测量去嵌、S-parameter manipulation、statistical process control。

工程含义：高速 PCB/基板/连接器供应商的价值不再是“按平方米报价”，而是按 channel margin、yield 和系统架构自由度定价。

### 2.5 Power integrity 和 thermal 从配角变成限制条件

ConnectorSupplier 报道称，2026 会场大量展示 liquid-cooled bus bars、leak detection、plumbing hardware、cold plate cooling。其判断是：AI rack 的电力消耗继续上行，600 kW rack 与 1 MW rack 的讨论让传统供电/散热体系必须重构。

DesignCon 2026 的 power 相关议题包括：

- “Powering the Future: AI's Role in Next-Generation Power Integrity Solutions” panel；
- “AI-Driven Emulation of Power Supply Ripple via HSS Jitter Analysis & TIE-Based Source Isolation for PI-SI Co-Design”；
- advanced packaging 里的 distributed capacitor characterization；
- package 内 embedded silicon capacitor、stackable POL converter、busbar/cooling integration。

结论：GPU/ASIC 的性能竞争会外溢到电源完整性、机柜电力分配、散热部件、冷却液监测和结构件。未来一年这些“非芯片”环节可能出现比传统半导体更高的订单弹性。

### 2.6 Agentic AI：短期价值不是“替代设计师”，而是让 SI/PI debug 变成半自动闭环

DesignCon 2026 的 AI 设计方向不是泛泛的 chat assistant，而是具体落在：

- multi-agent SI analysis for PCB/package；
- natural-language to HFSS simulation；
- AI-assisted RF/microwave design automation；
- AI-driven transient thermal solver for 3DIC；
- PI-SI co-design 的 source isolation 和 jitter analysis；
- Synopsys/Cadence/Ansys/MathWorks/Intel/Simberian/JITX 等工具生态。

可落地路径大概率是：

1. 2026：自动生成仿真 setup、rule checking、fixture/de-embedding 流程、报告摘要。
2. 2027：对 via/fan-out、equalization、PDN decap、thermal boundary condition 做 design-space exploration。
3. 2028 以后：在受限设计域内形成闭环优化，但 sign-off 和 failure analysis 仍由工程师负责。

## 3. 会爆发的产品和技术方向：成熟与量产路线

### 3.1 三情景路线表

| 产品/技术 | 基准路线 | 乐观路线 | 超预期乐观路线 |
|---|---|---|---|
| 224G copper/optical channel | 2026 年成为 AI switch、NIC、cable、CPC 的部署主线；112G 继续存量 | 2026H2 大型 hyperscaler 新 rack 默认 224G；224G AEC/ACC 供应紧张 | 224G 生命周期被压缩，2027H1 开始被 448G pilot 挤压高端新增设计 |
| 448G differential channel | 2026 年 pathfinding，2027 年小批量 design-in，2028 年较广泛部署 | 2027H1 在 scale-up/near-ASIC 短距铜链路出现低量部署 | 2026H2 某些 proprietary AI fabric 先采用 448G short-reach，带动测试设备和连接器订单提前爆发 |
| 1.6T optical module / 1.6T electrical interface | 2026 年量产爬坡，2027 年成为高端 AI fabric 标配 | 800G 与 1.6T 并行，1.6T 端口 2026 年从小基数升至千万级 | 1.6T 被 Google/NVIDIA/ASIC cluster 同时拉动，2026 供不应求延续到 2027 |
| CPC / top-side interconnect / flyover copper | 2026 年作为缩短 PCB channel 的主流解决方案进入高端交换机和加速器系统 | 224G CPC 广泛部署，448G CPC 在 2027 年提前商业化 | 短距铜可靠性超预期，推迟部分 CPO 替代，CPC/AEC/ACC 毛利保持高位 |
| CPO / OIO / silicon photonics | 2026-2027 以 demo、switch linecard pilot、特定 hyperscaler 为主；pluggable 仍是收入主体 | 2027 年部分 AI switch 平台开始批量采用 | 若 power/latency 压力过大，CPO/OIO 从“下一代”变成“本代 late-cycle upgrade” |
| PCIe 7.0 | 2026 年 validation/compliance/test 主战场，端设备逐步跟进 | PCIe 7 PHY/retimer 2026H2 design win 加速 | PCIe 7 在 AI rack 内部连接比传统服务器更快放量 |
| PCIe 8.0 256 GT/s | 2026-2027 为 IP、SerDes、connector、test pathfinding；标准预计 2028 | 2027 年 hyperscaler pre-standard prototype | 专有协议先采用 PCIe 8.0-class electrical，带动 256 GT/s 测试和 IP 收入提前 |
| UALink / Scale-up Ethernet | 2026 年生态验证，2027 年随非 NVIDIA AI rack 进入商业化 | 大型 ASIC/GPU 替代平台采用 UALink，形成多供应商生态 | UALink 成为 AI scale-up 的事实开放标准之一，迫使 retimer、switch、EDA 生态提前扩张 |
| Agentic EDA / autonomous SI | 2026 年工具辅助，2027 年局部闭环 | 高速 channel setup/debug 时间下降 20-30% | 工具公司把 AI workflow 变成高 ASP 模块，EDA 增速显著高于半导体设计开支 |
| Liquid cooling / high-current power delivery | 100 kW+ rack 默认液冷，电源完整性和冷却部件随 AI rack 扩产 | 300-600 kW rack 加速，使 busbar、manifold、leak detection、冷板供不应求 | 600 kW-1 MW rack 路线提前，液冷和高压配电成为 AI capex 的硬瓶颈 |

### 3.2 爆发力度排序

按 2026-2027 订单弹性和确定性排序：

1. **800G+/1.6T optical transceivers 和 optical components**：确定性最高，市场已有明确收入口径。TrendForce 估计 AI 专用光收发模块市场从 2025 年 **165 亿美元**增至 2026 年 **260 亿美元**，同比 **57%+**；800G+ 模块出货占比从 2024 年 **19.5%**升至 2026 年 **60%+**。
2. **high-speed copper interconnect：CPC/AEC/ACC/top-side connector**：收入口径分散，但 DesignCon 信号最强。224G 进入部署，448G demo 密集，直接受益于 AI rack 内短距连接和 PCB 路径缩短。
3. **retimer/redriver/SerDes PHY/DSP/active cable chipset**：因为 PCIe 6/7、CXL、UALink、1.6T、AEC/ACC 同时需要。Marvell、Synopsys、MACOM、Astera、Broadcom、Semtech 等都在受益链条。
4. **high-end test & measurement**：65 GHz/145 GHz/250 GHz、BERT、VNA、AWG、sampling oscilloscope、de-embedding、IEEE 370、PCIe 7/8 software。每一次 lane-rate 翻倍都会先买仪器和仿真。
5. **advanced packaging / 2.5D / 3DIC / chiplets / UCIe**：长期空间最大，但受 CoWoS/EMIB/Foveros/hybrid bonding 产能、良率和客户集中度约束。
6. **liquid cooling / high-current power distribution**：爆发由 AI rack 功耗驱动，硬件价值量快速提升，但竞争者更多，利润率分化大。
7. **agentic EDA / SI automation**：收入弹性取决于工具公司能否把 AI workflow 包装成高价值 license，而不是免费功能。

## 4. 市场规模、增速和利润率预测

### 4.1 当前可引用市场规模

| 市场/产品口径 | 当前规模与事实 | 备注 |
|---|---:|---|
| 全球 electronic connector market | 2025 年 **991.646 亿美元**，同比 **+14.7%**；其中北美 **219.756 亿美元**、欧洲 **188.741 亿美元**、日本 **41.543 亿美元**、中国 **328.418 亿美元**、亚太 **178.827 亿美元**、ROW **34.361 亿美元** | Bishop & Associates 口径；2026 预测增速 **+11.5%**，隐含 2026 约 **1,105-1,110 亿美元** |
| AI optical transceiver market | 2025 年约 **165 亿美元**，2026 年约 **260 亿美元**，同比 **+57%+** | TrendForce 口径，专指 AI 高速光收发模块 |
| Optical components market | 2025 年接近 **250 亿美元**；datacom revenue **>180 亿美元**，coherent module revenue 近 **60 亿美元** | Cignal AI 口径，较 AI optical transceiver 更宽 |
| Data center AI networking | 2025 年接近 **200 亿美元** | 650 Group 口径，包含 Ethernet、InfiniBand、800G optical transceivers 等 |
| EDA market | 2025 年约 **190 亿美元** | Synopsys、Cadence、Siemens EDA 高集中度；AI/multiphysics 推高 ASP |
| Advanced packaging | 2026 年约 **490-550 亿美元**；其中 2.5D/3D packaging 从 2025 年 **111.5 亿美元**到 2026 年 **127.3 亿美元**，2031 年 **241.8 亿美元** | 先进封装宽口径与 2.5D/3D 窄口径差异大 |
| Semiconductor/electronics test & measurement | 2025 年约 **77.135 亿美元**，CAGR **5.4%** | 高速 SerDes/PCIe/optical T&M 子品类增速显著高于总体 |
| Data center liquid cooling | Dell'Oro manufacturer revenue 口径：2025 年接近 **30 亿美元**；Grand View 宽口径：2025 年 **66.5 亿美元**；AI data center liquid cooling 2026 年约 **37 亿美元** | 口径差异来自是否包含 solution、services、facility integration |
| 全球半导体 | 2025 年 **7,917 亿美元**，同比 **+25.6%**；2026 年 SIA 预期约 **1 万亿美元** | DesignCon 相关需求主要来自 AI logic、memory、networking、custom ASIC |

### 4.2 未来一年三情景预测：规模、增速、利润率

> “未来一年”按 2026 全年到 2027H1 的订单和收入 run-rate 判断。利润率为行业典型毛利率/经营利润率区间，因公司结构差异很大，重点看方向。

| 产品/技术 | 当前市场规模 | 当前利润率 | 基准情景 | 乐观情景 | 超预期乐观情景 |
|---|---:|---:|---|---|---|
| 800G+/1.6T optical transceiver | AI 模块 2025 **165 亿美元**；2026 预测 **260 亿美元** | 模块毛利 **25-40%**；激光/DSP/SiPho 上游 **45-65%** | 2026 同比 **+55-60%**，规模 **250-265 亿美元**；毛利 +1-3pct，供需偏紧 | 同比 **+70-85%**，规模 **280-305 亿美元**；优质供应商毛利 **40%+** | 同比 **+100%+**，规模 **330 亿美元+**；1.6T/OCS/Google TPU/NVIDIA 同时拉货，上游激光和 DSP 最紧 |
| Optical components broader market | 2025 接近 **250 亿美元** | 混合毛利 **30-50%** | 2026 **+25-35%**，规模 **310-340 亿美元** | **+40-50%**，规模 **350-375 亿美元** | **+60%+**，规模 **400 亿美元+**，coherent + datacom 同时供给紧张 |
| CPC/AEC/ACC/top-side/high-speed connector cable | 宽口径 connector 2025 **991.6 亿美元**；DesignCon 相关高速 datacom 子市场估计 **100-150 亿美元** | 高速连接器/线缆毛利 **35-50%**；普通连接器 **25-35%** | 子市场 **+20-25%**；224G 放量、448G 仍 pilot；毛利稳定或 +1-2pct | **+35-45%**；top-side/CPC 进入更多 AI rack；毛利 **40-50%**维持 | **+50-70%**；铜短距能力超预期，部分原本光化链路延后，CPC/AEC/ACC ASP 高位 |
| PCIe/CXL/UALink retimer/redriver/SerDes PHY/DSP | 窄 retimer/redriver 估计 **15-25 亿美元**；高速 connectivity silicon/IP 估计 **50-80 亿美元** | 半导体毛利 **55-75%**；IP 可 **80%+** | **+30-40%**；PCIe 6/7、CXL、AEC 同步拉动；毛利稳定 | **+50-70%**；UALink 和 PCIe 7 design win 加速；高端 retimer 缺货 | **+90%+**；PCIe 8.0-class pre-standard 设计和 1.6T active cable chipset 同时提前 |
| PCIe 7/8、448G、1.6T 高速 T&M | 半导体/电子 T&M 2025 **77.1 亿美元**；高速子集估计 **10-20 亿美元** | 仪器毛利 **60-68%**；软件/服务更高 | 总体 **+6-10%**，高速子集 **+15-20%**；毛利稳定 | 高速子集 **+25-35%**；65GHz/145GHz/250GHz 仪器和 BERT/AWG 升级 | 高速子集 **+40%+**；448G/PCIe8 pathfinding 预算前置，T&M 先于终端放量 |
| Advanced packaging / 2.5D / 3DIC / chiplets / UCIe | advanced packaging 2026 **490-550 亿美元**；2.5D/3D 2026 **127 亿美元** | foundry/OSAT gross **25-45%**；受良率和 capex 影响 | **+15-20%**；CoWoS/EMIB/Foveros 继续瓶颈；利润率持平 | **+25-35%**；HBM4/ASIC/HPC 多客户拉动；稀缺产能毛利上行 | **+45%+**；chiplet/UCIe 标准化超预期，AI ASIC 爆量；但良率风险同步上升 |
| EDA / AI-assisted SI/PI / multiphysics | 2025 EDA 约 **190 亿美元** | 软件毛利 **75-85%**；经营利润 **25-35%** | **+12-15%**；AI 功能提高续费和 seat value；利润率 +1-2pct | **+20-25%**；agentic workflow 成为付费模块；利润率 +3-4pct | **+30%+**；AI design automation 直接缩短 tapeout/channel debug 周期，被高端客户按价值付费 |
| Liquid cooling / power delivery / rack thermal | manufacturer revenue 2025 近 **30 亿美元**；宽口径 2025/26 **60-66 亿美元**；AI 专用 2026 **37 亿美元** | 冷板/系统 gross **20-35%**；高定制可 **35-40%** | **+25-35%**；100kW+ rack 液冷默认化；利润率略升后趋稳 | **+50-60%**；300-600kW rack 带动 busbar/manifold/leak detection | **+75%+**；600kW-1MW rack 节奏提前，供电/散热成为 AI capex 第一瓶颈 |

## 5. 重要产品的投资/产业链判断

### 5.1 光模块：确定性最高，但注意“赢家不只模块厂”

800G/1.6T 光模块是最明确的爆发市场。TrendForce 给出 2025 到 2026 **165 亿美元到 260 亿美元**的市场跃迁，且 800G+ 模块在 2026 年占比 **60%+**。这说明 2026 年不是“渗透率刚起步”，而是高端 AI 数据中心从 400G/800G 过渡到 800G+/1.6T 的标准化阶段。

但利润最大的未必是最终 module assembly。更值得跟踪：

- EML/SiPh/InP 激光与光引擎；
- DSP/CDR/retimer；
- 1.6T test equipment；
- LPO 的 host tuning 和 validation；
- 低功耗封装、thermal design、FAU/optical connector；
- coherent ZR/ZR+ for scale-across DCI。

### 5.2 铜互连：最容易被市场低估

会场上最强反共识是：**448G 时代铜没有退出，反而在短距、near-ASIC、top-side、CPC、AEC/ACC 中变得更战略。**

原因：

- 光电转换有功耗、成本、延迟和热管理代价；
- rack 内短距链路对 latency 和 serviceability 敏感；
- PCB 走线太长时，top-side/copper flyover 反而是最直接的 SI 解决方案；
- AEC/ACC 用 retimer/redriver 把铜从“被动器件”变成系统级产品。

Samtec、Luxshare、Molex、TE、Amphenol、FIT、BizLink、Hirose 等的机会不只是连接器 ASP 提升，而是从零件进入 reference architecture。

### 5.3 Retimer/SerDes/IP：PCIe 8.0 的收入会早于 PCIe 8.0 标准

Marvell 和 Synopsys 在 DesignCon 2026 展示 PCIe 8.0-class 256 GT/s，是典型的“pre-standard revenue signal”。即使 PCIe 8.0 标准预计 2028 完成，2026-2027 年仍会产生：

- SerDes IP 授权；
- test chip；
- channel modeling；
- connector 与 cable fixture；
- retimer/redriver roadmaps；
- hyperscaler prototype；
- compliance software。

所以不能只盯“PCIe 8.0 endpoint 什么时候量产”。更早的受益环节是 IP 和验证生态。

### 5.4 Advanced packaging：UCIe/3DIC 是长期大方向，但短期瓶颈是产能和良率

DesignCon 的 3D interconnect、advanced packaging、HBM、chiplet、interposer、thermal solver 议题增加，说明 chiplet/3DIC 已经进入系统设计主战场。Mordor 口径下 2.5D/3D packaging 2026 年 **127.3 亿美元**，2031 年 **241.8 亿美元**，CAGR **13.69%**；更宽的 advanced packaging 口径 2026 年约 **490-550 亿美元**。

短期瓶颈不在需求，而在：

- CoWoS/EMIB/Foveros/advanced substrate 产能；
- HBM 堆叠良率；
- interposer warpage/thermal stress；
- die-to-die test；
- UCIe 生态互操作和责任边界；
- system-level EDA flow。

### 5.5 T&M 和 EDA：卖铲子，但要看是否绑定新标准

Keysight、Teledyne LeCroy、Anritsu、Rohde & Schwarz 在会场最活跃。原因很简单：224G/448G/PCIe 7/8/1.6T 都不是“做出来就行”，而是需要：

- 65 GHz+ real-time oscilloscope；
- 145 GHz+ electrical/optical interface testing；
- 250 GHz extender；
- BERT/AWG/sampling oscilloscope；
- BER/FEC/link quality benchmark；
- de-embedding 和 S-parameter metrology；
- PCIe/USB/DDR/GDDR compliance software。

EDA 同理。真正有弹性的不是普通 license，而是把 AI、multiphysics、3DIC、SI/PI/thermal、system validation 绑定的新 flow。

## 6. 可能与当前市场叙事相违背的重要洞见

### 6.1 “光替代铜”过于粗糙

DesignCon 2026 的事实是：光和铜都在升级。800G+/1.6T 光模块会爆发，但 448G short-reach copper、CPC、top-side interconnect、AEC/ACC 也会爆发。短距低延迟场景里，铜可能比市场预期活得更久、更贵、更战略。

### 6.2 CPO/OIO 短期不会马上吃掉 pluggable 模块收入

CPO/OIO 是长期方向，但 2026-2027 年收入主体仍是 pluggable、LPO、AEC/ACC、CPC 和 retimerized electrical links。CPO 更像下一代 switch architecture 的系统工程，不是简单把 OSFP/QSFP 一夜替换。

### 6.3 448G 的难点不只是 SerDes，而是制造统计和机械公差

Molex/Arista 的 224G/448G skew management、Intel/TE/Synopsys 的 PCIe 7 crosstalk sensitivity、Shennan 的 via/fan-out 448G 论文说明，448G 的核心问题会从“能否仿真出眼图”变成“能否稳定量产出 channel margin”。这会提高 metrology、SPC、材料和制造控制的价值。

### 6.4 PCIe 8.0 还未标准化，但供应链不能等到 2028

PCIe 8.0 预计 2028 完成，听上去很远；但 256 GT/s SerDes、connector、fixture、oscilloscope、retimer 的研发周期要求 2026 年就开始投入。市场若只按标准发布日期估值，可能低估 IP、T&M、connector 的前置订单。

### 6.5 Agentic AI 的第一桶金在“工程流程压缩”，不是“AI 自动设计芯片”

短期最值钱的是把 SI/PI/thermal/debug 流程从大量手工设置变成可复用、可审计的半自动 workflow。能节省 20-30% debug cycle 的工具，对 hyperscaler 和 ASIC 团队的价值远高于普通代码助手。

### 6.6 高速 PCB/连接器/冷却件可能比部分芯片环节更紧

AI 计算芯片的供应固然重要，但 DesignCon 2026 显示 bottleneck 正在扩散到：

- high-speed connector/cable；
- advanced PCB and substrate；
- optical module and DSP；
- liquid cooling；
- power delivery；
- T&M capacity。

这些“物理层铲子”公司在订单弹性上可能跑赢传统半导体周期。

### 6.7 中国供应链在高端互连上不只是制造承接

Alibaba、Luxshare、Shennan、New H3C 出现在 Best Paper 和关键 session 中，说明中国供应链已经在 PCIe 7.0 PCB、top-side interconnect、448G fan-out、CPC 结构上做 engineering leadership，而不仅是后端制造。对高端 PCB、连接器、光模块、线缆、AI rack 供应链格局影响很大。

## 7. 需要持续跟踪的指标

### 7.1 800G/1.6T 光模块

- 800G+ 出货占比是否按 TrendForce 路线在 2026 到 **60%+**；
- 1.6T 端口是否从小基数进入千万级；
- Google Ironwood TPU、NVIDIA Rubin/GB300/后续平台实际拉货；
- EML/InP/SiPh、DSP、LPO 良率与供应；
- 800G/1.6T ASP 是否因竞争快速下滑。

### 7.2 Copper/CPC/AEC/ACC

- 224G CPC 是否进入主流 AI switch reference design；
- 448G copper demo 是否转为 2027 design win；
- OSFP-XD PCIe/CXL AEC 在 JBOG/JBOM/JBOX 架构中的采用；
- top-side interconnect 是否从定制方案变成平台化产品；
- high-speed connector 交期和毛利率。

### 7.3 PCIe/CXL/UALink/retimer

- PCIe 7.0 compliance ecosystem 成熟度；
- PCIe 8.0 256 GT/s pre-standard demo 是否增加；
- UALink 是否获得非 NVIDIA AI rack 的真实 design win；
- CXL memory pooling 是否从概念走向部署；
- retimer/redriver 在 AI rack 中的 attach rate。

### 7.4 Power/thermal

- 100 kW、300 kW、600 kW rack 的实际部署节奏；
- cold plate、manifold、CDU、leak detection、liquid-cooled busbar 供应商订单；
- 800VDC/HVDC 或高压机柜配电路线是否被 hyperscaler 批量采用；
- 每 rack cooling BOM，从 GB300/NVL72 级别向 Rubin 级别如何变化。

### 7.5 EDA/T&M

- AI-assisted SI/PI 是否从 demo 变成付费模块；
- Synopsys/Cadence/Siemens/Ansys/Keysight/MathWorks 是否形成闭环 flow；
- 65GHz+ scope、145GHz+ optical/electrical test、250GHz extender 的订单和交期；
- 448G/PCIe 8.0 test fixture 标准化进度。

## 8. 结论：DesignCon 2026 的投资含义

DesignCon 2026 给出的最大投资线索不是“AI 继续拉动半导体”这种宽泛结论，而是：**AI cluster 的瓶颈正在从 GPU die 扩散到整个物理层。**

未来一年最强的确定性在 800G/1.6T 光模块和 optical components；最容易被低估的是 224G/448G copper interconnect、CPC、AEC/ACC、top-side connector；最前置受益的是 SerDes IP、retimer、T&M 和 EDA；中长期空间最大但约束最多的是 advanced packaging/chiplets/UCIe；最可能突然变成硬瓶颈的是液冷和高功率配电。

一个高度压缩的判断：

- **2026 年收入最确定**：800G/1.6T 光模块、光器件、AEC/ACC、retimer、PCIe 7 测试。
- **2026 年订单弹性最大**：1.6T optical、224G/448G CPC/top-side copper、liquid cooling、high-end T&M。
- **2027 年开始兑现**：448G short-reach、PCIe 7 endpoints/retimers、UALink rack-scale、CPO/OIO pilot、agentic SI/PI workflow。
- **2028 年及以后兑现**：PCIe 8.0 标准化设备、3.2T/400G-per-lane、CPO/OIO 规模化、UCIe merchant chiplet ecosystem。

市场若继续只按“GPU/ASIC/HBM”给 AI 基建定价，会低估 DesignCon 2026 暴露出来的物理层短板：连接、测量、封装、供电、散热、自动化验证。这些环节正在从后端配套变成 AI 数据中心的核心 alpha 来源。

## 9. 主要公开来源

- [DesignCon 官方页面：100+ sessions、15 tracks、sponsor、venue 信息](https://www.designcon.com/en/home.html)
- [DesignCon 2026 Best Paper Awards and Engineer of the Year，GlobeNewswire, 2026-05-06](https://www.globenewswire.com/news-release/2026/05/06/3289177/0/en/DesignCon-Crowns-2026-Winners-for-Best-Paper-Awards-and-Engineer-of-the-Year.html)
- [ConnectorSupplier 会后报道：183 technical papers、202 exhibitors、224G/448G、PCIe 8.0、600kW rack](https://connectorsupplier.com/designcon-2026/)
- [Signal Integrity Journal 会后总结：AI-driven infrastructure、448G、1.6T、system-level design](https://www.signalintegrityjournal.com/articles/4262-designcon-2026-ai-driven-infrastructure-and-system-level-design)
- [Keysight DesignCon 2026 发布：PCIe 7、448G PAM4/PAM6/PAM8、1.6T、UALink](https://www.keysight.com/it/en/about/newsroom/news-releases/2026/0209-pr26-028-keysight-to-showcase-advanced-ai-data-center-and-high-speed-interconnect-validation-at-designcon-2026.html)
- [Samtec DesignCon 2026：448 Gbps、130 GHz、CPC/CPO、Si-Fly、BE130](https://blog.samtec.com/designcon-2026/)
- [Luxshare-Tech DesignCon 2026：224G/448G CPC、1.6T OSFP AEC/ACC、PCIe 6.0 OSFP-XD AEC](https://en.luxshare-tech.com/company/resources/news/designcon-2026-unveiling-224g-448g.html)
- [Marvell DesignCon 2026：PCIe 8.0 SerDes 256 GT/s、1 TB/s x16、2028 标准预期](https://www.streetinsider.com/Business%2BWire/Marvell%2Bto%2BShowcase%2BPCIe%2B8.0%2BSerDes%2BDemonstration%2Bat%2BDesignCon%2B2026/26047870.html)
- [Synopsys DesignCon 2026：PCIe 8.0-class 256 GT/s、224G PHY、PCIe 7.0 PHY partner demos](https://www.synopsys.com/events/designcon.html)
- [Anritsu DesignCon 2026：PCIe 7.0 over optics、SiPhx 800G LPO、64 Gbaud PAM4](https://www.anritsu.com/en-us/test-measurement/news/news-releases/2026/2026-02-20-us01)
- [Cadence DesignCon 2026：EM/electronic/thermal system analysis、HBM PHY、UALink IP](https://www.cadence.com/en_US/home/company/events/industry-events/designcon-2026.html)
- [DesignNews：5 Hot Topics at DesignCon 2026](https://www.designnews.com/electronics/five-hot-topics-at-designcon-2026)
- [Bishop & Associates World Connector Market Handbook 2026 sample：2025 connector market 991.646 亿美元、+14.7%](https://bishopinc.com/wp-content/uploads/2026/03/M-700-26-B.pdf)
- [Bishop Report news brief：2026 connector sales forecast +11.5%](https://bishopinc.com/wp-content/uploads/2026/02/nb-10-26.pdf)
- [Cignal AI：2025 optical components 接近 250 亿美元，datacom >180 亿美元](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)
- [TrendForce：2026 年 AI 光收发模块 260 亿美元、800G+ 出货占比 60%+](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- [650 Group：Data Center AI Networking 2025 接近 200 亿美元](https://650group.com/press-releases/data-center-ai-networking-to-surge-to-nearly-20b-in-2025-according-to-650-group/)
- [Grand View Research：semiconductor/electronics T&M 2025 77.135 亿美元](https://www.grandviewresearch.com/horizon/statistics/test-and-measurement-equipment-market/end-use/semiconductor-and-electronics/global)
- [Grand View Research：data center liquid cooling 2025 66.5 亿美元](https://www.grandviewresearch.com/industry-analysis/data-center-liquid-cooling-market-report)
- [Dell'Oro/PRNewswire：liquid cooling 2025 接近 30 亿美元，2029 接近 70 亿美元](https://www.prnewswire.com/news-releases/data-center-liquid-cooling-market-to-approach-7-billion-by-2029-as-ai-deployments-accelerate-according-to-delloro-group-302655848.html)
- [Mordor Intelligence：2.5D/3D semiconductor packaging 2025-2031](https://www.mordorintelligence.com/industry-reports/global-25d-and-3d-semiconductor-packaging-market)
- [TMT IB Guide：EDA 2025 约 190 亿美元](https://ibinterviewquestions.com/guides/tmt-investment-banking/eda-ip-semiconductor-design-tools)
