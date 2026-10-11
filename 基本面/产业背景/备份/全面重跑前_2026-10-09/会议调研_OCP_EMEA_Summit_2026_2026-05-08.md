# OCP EMEA Summit 2026 高密度调研：AI 数据中心从“买 GPU”进入“重构电力、散热、互连、标准”的阶段

> 截至 2026-05-08。报告只使用公开网页、官方议程、公开 PPTX/链接和公开市场资料，未参考项目内文件。  
> 会议：2026 OCP EMEA Summit，2026-04-29 至 2026-04-30，Barcelona, Spain。官方说明称本届重点是 EMEA 区域的数据中心可持续性、能效、热复用，以及 OCP 认可设备的区域部署。

## 0. 信息源与口径

- 官方入口：[OCP EMEA Summit 2026](https://www.opencompute.org/summit/emea-summit)，[官方会务 App](https://2026ocpemea.fnvirtual.app/)，[Full Schedule](https://2026ocpemea.fnvirtual.app/a/schedule)。
- 解析官方会务 App 的公开嵌入数据：208 个 session、303 位 speaker、34 个 track、157 条公开 `PresentationMediaUpload`，其中约 142 份 PPTX 可直接提取文本。
- 高频一手材料：IDC/OCP 采用与支出报告、Open Data Center for AI、LVDC/HVDC、冷板/浸没/UQD/TCO、UALink/ESUN/SUE-T、800G/1.6T、硅光/OCS/多芯光纤、FCSA/chiplet、Caliptra/LOCK/SOLID/openSFI。
- 市场规模使用公开市场资料校准：TrendForce、Cignal AI、Grand View Research、BCC Research、Dell'Oro 经媒体转述、OCP/IDC 会场材料。以下预测为研究估算，不是投资建议。

## 1. 一页结论

OCP EMEA 2026 的主线非常清楚：AI 数据中心的瓶颈已经从“有没有 GPU”扩展为“电力能否到位、热能否带走、互连能否保持 GPU 利用率、供应链能否多厂商化、固件和硅根信任能否被审计”。会议不像传统服务器会议，更像 AI 工厂基础设施标准化会议。

最重要的变化是六个：

- **开放 AI 数据中心成为顶层项目**：Google、Meta、AMD、NVIDIA、Microsoft 等推动 Open Data Center for AI。会场材料给出 Open DC Spec 路线：2026-05 25% 完成、2026-06 50%、2026-07 75%、2026-08 社区反馈、2026-09 OCP Steering Committee 批准与网站发布、2026-10 OCP Global Summit 展示。
- **机架功率从 40-100 kW 直接跳到 500 kW 至 1 MW 叙事**：Open DC 材料称 Top 5 超算约每年 1-2 台、今天 400 kW/rack；AI supercomputers 正向每周约 1 套推进，600 kW 在路上，目标路径到 1 MW。Schneider/Rittal keynote 均强调超过 500 kW/rack 已不再是理论。
- **电力架构转向 HVDC/LVDC 和电网协同**：ORv3/HPR 从 33 kW、72 kW 走向 100 kW/160 kW HVDC power shelf；800 VDC、700/1400 V、750/1500 V 的互操作和保护问题成为核心议题。电力不再是设施后端，而是 AI 系统架构的一部分。
- **冷板先爆发，浸没进入标准化深水区**：Promersion/OCP 材料称 2025 年 cold plate 市场突破 50 亿美元，immersion 约 8 亿美元；冷板、UQDv2、CDU/TCO 工具在 2026 年明显成熟，浸没仍有信号完整性、材料兼容、供电安全和运维标准问题。
- **AI 网络从 scale-out 进入 scale-up/scale-across 多层体系**：UALink 2.0 规格完成，800 Gbps port 可拆为 1x800G、2x400G、4x200G；ESUN 1.0 已获批，SUE-T 提出 scale-up Ethernet transport。800G 是当前主战场，1.6T 是 2026-2027 的新增长。
- **开放硅、开放固件、开放安全从“理念”变成采购门槛**：FCSA 1.0.0 2026-02 发布；Caliptra 2.2 目标 Q4 2026，2027 进入 NEXT；OCP S.O.L.I.D. 要求 2026-10-01 起进入 OCP S.A.F.E. long-form report；openSFI 0.5 正在推进并目标 OCP Global 0.7。

## 2. 重点与相较此前市场/技术的转折

### 2.1 Open Data Center for AI：从服务器标准变成“AI 工厂接口标准”

IDC 会场材料给出一个关键基准：OCP-recognized IT infrastructure and solutions 支出将从 2025 年 1320 亿美元增长到 2029 年 2950 亿美元，CAGR 22.2%；hyperscalers 当前占 OCP-specified infrastructure 超过 60%。这意味着 OCP 不是边缘开源硬件兴趣小组，而正在变成 AI 基础设施采购和设计语言。

Open DC for AI 的核心接口包括：spatial/rack form factor、network、power、cooling、power quality、security、telemetry。Open DC Spec v0.5、Project Deschutes、CDU Spec v1.0、Mt. Diablo +/-400VDC Sidecar Spec v0.7、Clean Backup Spec v0.3 都被列入基础设施组件标准化对象。

相较之前：过去 OCP 主要围绕服务器、机架、供电、BMC 等模块化规范；今年明显转向“从园区电网到 rack 到 xPU fabric 的端到端 AI data center standard”。

### 2.2 电力：800 VDC/LVDC 是本届最硬的增量方向

会议直接出现多个强数字：

- HPRv1：33 kW shelf，5.5 kW PSU，峰值效率 97.5%，满载效率 96.5%。
- HPRv2：72 kW shelf，12 kW PSU，50 Vdc 输出，1470 A nominal，峰值 97.5%，满载 96.5%。
- HPRv4 HVDC：100 kW/160 kW 讨论，输入 ±380 Vdc 至 ±420 Vdc，18 kW rectifier，50 Vdc 输出，367 A，峰值效率 98.5%，满载 97.5%。
- LVDC workstream 明确排除 >1500 VDC 的 MVDC，把当前工作聚焦在低压直流、800 VDC/700 VDC/750/1500 VDC 的互操作、安全保护、极性/接地、EMC、控制运行。
- 800 V 设备若设计为可在 750 V 下运行，可兼容 700/1400 V TN-S 系统，有利于完整使用 1500 V 低压 DC 范围。

关键变化：电力系统开始被当成“动态负载网络”设计。HPRv2 72 kW 的 abnormal voltage ride-through 演示覆盖 0.8 pu 3s、0.75 pu 3s、0.65 pu 2s、0.5 pu 0.5s、0.45 pu 0.3s 等电网暂降要求，目标 fast recovery <500 ms。AI 负载的高 slew rate 和电网稳定性已经进入 PSU 和 BBU 固件开发。

### 2.3 散热：冷板量产，浸没标准化，TCO 从“散热成本”变成“上架速度成本”

Cooling track 的关键数字：

- Promersion/OCP：2024 Q3 cold plate inflection 由 NVIDIA GPU 推动；cold plate 市场相较 2023 年约四倍增长；2025 年 cold plate 突破 50 亿美元；immersion 达 8 亿美元。
- UQDv2 draft 在 2026-04-20 技术内容冻结，UQD08 hybrid 测试中 spec max dP 1.7 psi，3 家样品约 1.0 psi ±0.2；插拔力 spec max 30 lbf，样品约 22 lbf ±4。
- Coldplate Base Specification 目标是建立 single-phase D2C cold plate 的事实行业基线，解决定义不一致、验证碎片化、供应商评价不可比的问题。
- TCO Tool v1.3 发布，Excel、无宏、无隐藏逻辑，可比较 air、DLC、RDHX、side-car、L2L CDU 等架构。材料给出例子：若电价 0.1 EUR/kWh，在 L3 rPDU outlet 计量，巴黎 breakeven 0.352 EUR/kWh、巴塞罗那 0.354 EUR/kWh，巴塞罗那 breakeven hosting rate 每年高约 879,382 欧元。
- Modular TCS panel 给出“100 kW to 1 MW per rack”路线；一次 100 MW、600 racks 部署中，若每 rack 成本 500 万美元、收入 7500 万美元，延误 1 周可能损失 2 亿至 4 亿美元业务。

关键变化：冷却不再只看 PUE，而看“time to power/time to deployment”。液冷管路、冲洗、过滤、盲插快接、CDU 位置和运维流程的标准化，直接影响收入确认速度。

### 2.4 网络与互连：Ethernet 正进入 scale-up，UALink/ESUN/SUE-T 并行

会议材料显示 AI 网络被拆为三层：

- Scale-up：single xPU node，约 8 至 1k xPUs，约 12 kW 至 1 MW，HBM bandwidth per xPU 约 100 Tb/s。
- Scale-out：single data center cluster，约 50k m²、约 100k xPUs、约 180 MW。
- Scale-across：multiple data centers，约 5 km²、1M+ xPUs、1+ GW。

UALink 材料强调 800 Gbps ports 可做 1x800G、2x400G 或 4x200G，目标是数百 accelerator、最多 1K 的 pod 内低延迟 load/store/atomic 共享内存。ESUN 1.0 已批准，166 名成员，核心是 Ethernet scale-up network 的 operator/end-user requirements、低头开销 header、LLR、PFC/CBFC、lossless 和 link reliability。

Celestica/Hedgehog/OCP Open Cluster Design 给出 2026-2027 路线：2026 H1 参考架构草案和 artifacts，2026 H1 1.6T architecture revision，2026 H2 扩展 xPU 支持，2027 继续开放集群设计。其 open fabric 支持 SONiC、1.6T Celestica DS6000、800G DS5000、Day 0/1/2 lifecycle automation。

关键变化：过去市场把 AI 网络理解为 InfiniBand vs Ethernet；本届更像“scale-up memory semantics + scale-out Ethernet + scale-across optics”的多协议现实。Ethernet 不只做大二层/三层网络，正在被压入 GPU 近端。

### 2.5 光互连：800G/1.6T 是 2026 主线，OCS/CPO/MCF 是下一层变化

TrendForce 认为 800G 及以上光模块出货占比将从 2024 年 19.5% 提升到 2026 年超过 60%；全球光收发模块出货量从 2023 年 2650 万只到 2026 年超过 9200 万只。Google Ironwood TPU 相关 800G+ 光模块需求预计超过 600 万只。

会议材料中的关键事实：

- iPronics 32x32 silicon photonic OCS 已向客户出货，1024 optical interconnects，400G LWDM 下 BER 1e-5 和 1e-7 演示，sub-ms reconfiguration，系统功耗 30 W + 0.78 W/active channel，宣称至少较传统 switch 降低 10x 功耗。
- TrendForce 给的 Google Apollo OCS 对比：单台 OCS switch 约 100 W，传统 switch 约 3000 W，功耗下降约 95%。
- imec 材料演示 400G/lane CPO：212.5 GBaud PAM4，HD-FEC threshold 6.25% OH，net 400 Gbps/lane；若 400G/lane CPO 能达 5 pJ/bit，光学部分总功耗约 1.25 kW。
- Sumitomo 多芯光纤材料：从 H200 约 320 fibers/rack 到 GB200/NVL72 约 1440 strands，再到 Rubin/NVL144 约 2880 strands；4-core MCF 示例中 6912 芯 cable 外径从单芯约 37 mm 降至 4-core 约 13 mm，截面积 1075 mm² 至 133 mm²，节省 60-80% 管道空间。

关键变化：光模块从“网络设备 BOM”变成 AI 产能节奏瓶颈，价值从组装转向硅光 wafer process、2.5D/3D packaging、electro-optical test 和 CPO 平台。

### 2.6 Chiplet：FCSA 让开放 chiplet 从 PHY 走向系统架构

OCP 在 2026-02 发布 FCSA。Arm/OCP 说 FCSA 是 vendor-neutral、ISA-neutral 的 chiplet specification，目标是把 monolithic SoC 拆成可互操作 chiplets，覆盖 memory、I/O、accelerator 等。

会场材料的关键数字：

- Qualcomm 材料：D2D interconnect silicon-proven Gen1 24 Gbps、Gen2 36 Gbps、Gen3 64 Gbps；off-chip IO reference 中 PCIe7/8 走 128G 至 248G，UALink/ESUN/Ethernet 走 200G 至 400G。
- Arm FCSA 材料：FCSA 1.0.0 于 2026-02 发布，ACSA 1.0.0 于 2026-03 发布，目标 2026-10 发布 FCSA 1.1.0。
- Cadence/Arm 材料：UCIe 1.1 32Gx16、PCIe 6.0 x8、CXL 3.2 Type-2、DDR5-9600 memory subsystem 被放入 pre-silicon verification flow。

关键变化：此前 chiplet 标准更多停在 UCIe/BoW 等物理互连；今年的 OCP Open Chiplet Economy 强调 system-level interoperability：management、security、firmware、software abstraction、threat model 和 verification。

### 2.7 安全与固件：供应链信任成为欧洲 AI 基础设施的核心接口

Microsoft keynote 将 EU Data Boundary、Caliptra、OCP S.A.F.E.、Confidential Computing 放在“Scaling Trusted AI Infrastructure”中。EMEA 的 sovereign cloud 讨论也强调真正主权不是 data residency，而是 supply chain、firmware、lifecycle、auditability 和 vendor swap。

关键一手事实：

- Caliptra roadmap：2.0/2.1 覆盖 RTL、ROM、FW；加入 NIST PQC ML-DSA/Dilithium 与 ML-KEM/Kyber；Caliptra 2.2 目标 Q4 2026；NEXT 在 2027，包含 security hardening、area/power reduction、generic key derivation/distribution 等。
- OCP L.O.C.K.：1.0 已于 2025-09 发布，1.1 计划 2026-05，KMB ROM/FW 完成，MCU reference implementation 进行中，新增 attested crypto-erasure 和 epoch key purge。
- OCP S.O.L.I.D.：面向 datacenter hardware/firmware security requirements，约 80% 覆盖 hyperscaler 重复采购要求；2026-10-01 起 OCP S.A.F.E. long-form report 必须包含 S.O.L.I.D. requirement analysis。
- openSFI：从 2025 Q1 启动 v0.3，到 2025 Q3 发布 v0.3，2026 推进 v0.5；目标是 vendor-agnostic interface between host firmware and silicon firmware，减少 host firmware 对 silicon implementation 的硬耦合。
- Arm SBMR：Arm SystemReady band 已有 56 servers、18 partners，SBMR 3.0 ALP 将在 EMEA Summit 后贡献到 OCP HW Management Project。

## 3. 哪些产品和技术会爆发：成熟与量产路线三情景

| 方向 | 会议证据 | 基准口径 | 乐观口径 | 超预期乐观口径 |
|---|---|---|---|---|
| Open Data Center for AI | Open DC Spec 2026-09 目标发布；接口覆盖 rack/network/power/cooling/security/telemetry | 2026 成为 RFP/设计参考；2027 进入 hyperscaler 与 OCP Ready v2 colocation 项目 | 2027 上半年成为大型 AI campus 的标准接口，带动 CDU、HVDC、telemetry 联合采购 | 2026 Q4 起被 Microsoft/Google/Meta 级项目写入采购条款，2027 形成事实标准 |
| 800 VDC/LVDC/HVDC rack power | 72 kW HPRv2、100/160 kW HPRv4，98.5% peak efficiency，800V/750/1500V 互操作 | 2026 以 sidecar、pilot、new-build 为主；2027 小批量 AI factory 部署 | 2027 大型 AI campus 新建电力架构优先考虑 HVDC/LVDC，rack power shelf 和 BBU 放量 | 电网 ride-through 和 power flexibility 要求加速采用，2027 800 VDC 成为 500 kW+ rack 默认选项 |
| Cold plate/D2C liquid cooling | 2025 cold plate >50 亿美元，UQDv2 内容冻结，coldplate base spec 推进 | 2026 GB300/Rubin 新机架标配冷板；2027 企业/colo 进入规模迁移 | 2026 下半年冷板、CDU、manifold 供应链紧张，毛利提升 | 500 kW+ rack 加速，冷板与 RDHX/door HX 组合成为 100-300 kW rack 的默认工程方案 |
| Immersion cooling | Immersion 2025 约 8 亿美元，15 个 active workstreams，1467 unique participants | 2026-2027 仍在 neocloud、edge、改造项目中分散采用 | 单相浸没 ORv3、power distribution、ITE guidelines 完成后，2027 部分 AI neocloud 批量采用 | 若 1 kW+ devices 与水资源限制同时加剧，浸没作为差异化方案在 2027 进入多区域标杆项目 |
| UALink/ESUN/SUE-T scale-up interconnect | UALink 2.0 complete，IP/TME ready；ESUN 1.0 approved；SUE-T 定义 scale-up transport | 2026 design-in，2027 第一批多厂商 accelerator pod | 2027 UALink switch/accelerator 开始生产验证，ESUN 用于 Ethernet scale-up 标准化 | Ethernet 在 scale-up 取得突破，up to 2048 XPUs、<1 us RTT 的架构成为推理集群关键卖点 |
| 800G/1.6T switching and optics | 800G+ optical share 2026 >60%；1.6T architecture revision 2026 H1/H2 | 2026 800G 主流，1.6T 小批量；2027 1.6T 放量 | 2026 1.6T 在 spine/scale-across 先放量，光模块紧缺 | 1.6T 端口和 CPO/OCS 带动交换芯片、DSP、硅光封装一起涨价 |
| Silicon photonics OCS/CPO | OCS 32x32 shipping；100 W OCS vs 3000 W traditional；400G/lane CPO 演示 | 2026 OCS pilot；2027 在 Google 类架构中扩大 | 2027 OCS + pluggable 1.6T 成为 scale-across/scale-up 重要形态 | 2026-2027 出现“OCS 绕过电交换”的标杆设计，显著压缩传统电交换预算 |
| Multi-core fiber | 4-core MCF 节省 60-80% duct space，NVL72 到 NVL288 光纤数量指数级增加 | 2026 布线规划采用 MCF 试点；2027 高纤芯 trunk 放量 | MCF/FIFO 与 MCF-native transceiver 配套，2027 大型 AI campus 批量使用 | CPO to ASIC 与 MCF 打通，光纤基础设施成为 AI campus 关键瓶颈投资 |
| Open chiplet/FCSA | FCSA 1.0 2026-02；FCSA 1.1 目标 2026-10；UCIe/CXL/PCIe 进入验证 | 2026 标准设计和验证工具成熟，2027 被部分 ASIC RFP 引用 | 2027 出现可复用 accelerator/IO/memory chiplet 目录 | 2028 前形成开放 chiplet marketplace，降低小厂/欧洲自研 AI silicon 门槛 |
| Caliptra/LOCK/SOLID/openSFI | Caliptra 2.2 Q4 2026；LOCK 1.1 2026-05；SOLID 2026-10 进入 SAFE long-form | 2026-2027 成为 hyperscaler/security RFP 加分项 | 欧洲 sovereign cloud 把 Caliptra/SOLID/openSFI 写入合规 baseline | 供应链风险与 CRA 触发安全审计刚需，固件/硅根信任服务利润率提升 |

## 4. 重要产品和技术的市场规模、未来一年增速、利润率

> 口径说明：当前规模优先采用 2025A 或 2026E run-rate。未来一年指从 2026 年中至 2027 年中附近的增速估计。利润率为产业链粗口径，硬件供应商、ODM、IP、系统集成之间差异很大。

| 方向 | 当前市场规模 | 未来一年增速：基准 / 乐观 / 超预期 | 当前利润率与趋势 |
|---|---:|---:|---|
| OCP-recognized IT infrastructure | 2025 年约 1320 亿美元，IDC 会场材料预测 2029 年 2950 亿美元，CAGR 22.2% | +22% / +28% / +35% | 混合毛利约 10-25%。服务器/机柜集成偏低，电力/冷却/管理软件更高。趋势：AI 设施瓶颈让非 GPU 层议价能力提升 |
| AI server/rack-scale GPU/ASIC systems | TrendForce：AI server 2025 约 2980 亿美元；2026 收入再增 30%+，约 3900 亿美元级 | +25-35% / +40% / +50% | GPU/ASIC 硅片与系统平台高，ODM rack integration 低；混合毛利约 15-25%。HBM/先进封装紧缺维持上游高毛利，整机价格压力上升 |
| Data center power infrastructure，含 UPS、busway、PDU、rack power、HVDC/LVDC | GVR：data center power 2025 约 227.7 亿美元；BCC：power infrastructure 2024 年 287 亿美元，2030 年 473 亿美元 | +12-18% / +22-25% / +30% | 电力电子、switchgear、busway 毛利约 25-40%，项目集成较低。趋势：800 VDC、ride-through、BBU/ESS 使高端产品毛利上行 |
| Liquid cooling，cold plate、CDU、manifold、immersion | GVR：2025 年 data center liquid cooling 约 66.5 亿美元；OCP/Promersion：2025 cold plate >50 亿美元、immersion 约 8 亿美元 | +25-30% / +40% / +60% | 冷板/CDU/快接/服务毛利约 25-45%。短期供需紧张和标准化不足推高毛利，2027 后随多厂商化可能分化 |
| High-speed optics，800G/1.6T、OCS、CPO、DSP | Cignal AI：2025 optical components 近 250 亿美元，其中 datacom >180 亿美元、coherent 近 60 亿美元；TrendForce：2026 transceiver >9200 万只，800G+ 占比 >60% | +20-30% / +35-45% / +50%+ | 标准 pluggable 毛利 15-30%，硅光/CPO/OCS/高端 DSP 可达 35-55%。趋势：高端上行、标准模块受中国供应链压价 |
| AI Ethernet/data center switch、NIC/DPU、cables | 数据中心交换机 2025 约 150 亿美元级；Dell'Oro 称 2025 AI back-end Ethernet switch sales 增长超过 3 倍，800G ports 三年超 2000 万 | +30-40% / +50% / +70% | Branded switch 毛利 40-65%，whitebox 10-20%，merchant silicon/NIC 更高。趋势：1.6T 和 scale-up Ethernet 提高 silicon/NIC 价值 |
| Chiplet/advanced packaging/open chiplet ecosystem | Chiplet 市场 2025 约 130 亿美元级，open chiplet direct revenue 仍小但附着于 AI ASIC/HPC | +30-45% / +50% / +70% | IP/EDA 毛利 70%+，advanced packaging 20-35%，custom silicon 项目利润高度集中。趋势：FCSA 降低 vendor lock-in，但初期服务/IP 溢价高 |
| Silicon root-of-trust、secure firmware、attestation、SAFE audit | 直接市场可能只有数十亿或更小，但附着在 3000 亿美元级 AI server 和 sovereign cloud 采购上 | +30% / +50% / +80% | IP/审计/安全服务毛利高，硬件 RoT 单价低但 attach rate 高。趋势：欧洲 CRA、sovereign cloud 和 hyperscaler RFP 会把它变成准入条件 |
| Data center storage for AI cold/archive tier | 传统 enterprise storage/HDD/NAND 是百亿美元级；Cerabyte 类“零能耗保留”仍是早期 | +5-15% / +20% / +35% | HDD/SSD 毛利受周期影响大；新型归档介质若验证成功毛利高。趋势：AI 数据保留、训练数据 lineage、合规归档扩大需求 |

## 5. 与当前市场共识相违背或容易被低估的洞见

### 5.1 不是只有 GPU 缺，真正卡量产的是“power to rack”和“time to power”

市场常把 AI capex 直接等同 GPU。OCP 会场却反复强调：超过 500 kW/rack 已经临近，100 MW 级部署延误一周可对应 2-4 亿美元业务损失。电网暂降穿越、BBU 协同、800 VDC 电压带、现场冲洗和过滤，都是 GPU 之前的“产能闸门”。

### 5.2 冷板最先商业爆发，浸没不会立刻替代冷板

会议数据支持 cold plate 先爆：2025 年 >50 亿美元，immersion 约 8 亿美元。浸没的问题不是热性能，而是电气信号完整性、材料兼容、power distribution、ITE guidelines、清洗/维护/保险/合规。超预期情景需要 1 kW+ device、供水限制和新建 AI neocloud 三个条件同时出现。

### 5.3 Ethernet 不是简单替代 InfiniBand，而是在吞掉更多层级

ESUN、SUE-T 与 UALink 的共存说明 scale-up 不是单一协议赢家通吃。Ethernet 的优势是生态、运维、供应商多样性；UALink 的优势是 memory semantics 和低延迟。更可能出现的是：rack/pod 内 UALink 或 ESUN，cluster 内 800G/1.6T Ethernet，campus 间 coherent/OCS/optical fabric。

### 5.4 光互连的利润池会从模块组装前移到硅光、封装和测试

TrendForce 明确指出 SiPh/CPO 重点在 wafer-level process 和 advanced co-packaging，而不是传统模块组装。台湾/东南亚 OSAT、PIC process、server ODM 的一体化能力会成为新入口。传统低毛利 transceiver 供应商可能不一定是最大赢家。

### 5.5 主权云不是“在本国机房跑 hyperscaler stack”

ScaleUp Germany 材料直说：很多所谓 sovereign cloud 只是美国 hyperscaler stack 在德国数据中心，属于 data residency，不是真主权。真正主权要求控制 supply chain、firmware、lifecycle、整栈可审计、可换供应商。这会放大 OCP、open firmware、Caliptra、SBMR、openSFI 的欧洲价值。

### 5.6 循环利用从 ESG 叙事变成供应链对冲

Meta circularity 材料称 2026 Big-5 hyperscaler data-center capex 6000 亿美元+，AI 占 72%；DDR5 16Gb spot price 在 Q1 至 Q4 2025 从 6.84 美元涨到 27.20 美元，涨幅 298%；server lifecycle carbon 中 78% 在制造环节，单台服务器每次 reuse 可避免约 1500 kg CO2e。旧硬件和再制造 OCP rack 的价值将不仅是碳，而是缩短 lead time 和对冲内存/电源供应。

### 5.7 安全合规的商业价值可能被低估

Caliptra、OCP L.O.C.K.、OCP S.O.L.I.D.、openSFI、SBMR 都在 2026 出现明确版本和审计路径。欧洲 CRA、云主权、硬件供应链风险会把这些从“开源基础组件”推到采购 gating factor。直接收入小，但它能决定服务器、SSD、GPU、NIC、BMC、firmware 是否进入高端客户 RFP。

## 6. 核心材料索引

会议与市场源：

- [OCP EMEA Summit 2026 官方页](https://www.opencompute.org/summit/emea-summit)
- [OCP EMEA Summit 2026 会务 App](https://2026ocpemea.fnvirtual.app/)
- [OCP Full Schedule](https://2026ocpemea.fnvirtual.app/a/schedule)
- [TrendForce：AI server 2025 产业价值 2980 亿美元](https://www.trendforce.com/presscenter/news/20250106-12433.html)
- [TrendForce：2026 AI server 出货 +28% 以上，ASIC AI server 约 27.8%](https://www.trendforce.com/presscenter/news/20260120-12887.html)
- [TrendForce：八大 CSP 2026 capex 超 5200 亿美元](https://www.trendforce.com/presscenter/news/20251013-12741.html)
- [TrendForce：800G+ 光模块 2026 占比超过 60%](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- [DRAMeXchange/TrendForce：光收发模块 2026 超 9200 万只](https://www.dramexchange.com/WeeklyResearch/Post/2/12686.html)
- [Cignal AI：2025 optical components 近 250 亿美元](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)
- [OCP：FCSA 公开发布](https://www.opencompute.org/index.php/blog/ocp-open-chiplet-economy-is-leading-the-next-wave-of-ai-inference)
- [Grand View Research：data center liquid cooling market](https://www.grandviewresearch.com/industry-analysis/data-center-liquid-cooling-market-report)
- [BCC Research via GlobeNewswire：data center power infrastructure](https://www.globenewswire.com/news-release/2026/04/30/3284618/0/en/Power-Infrastructure-for-Data-Centers-Market-to-Reach-47-3-Billion-by-2030-Driven-by-AI-Intensive-Computing-Expansion.html)
- [SDxCentral：Dell'Oro AI back-end Ethernet switch sales tripled](https://www.sdxcentral.com/news/ethernet-switch-sales-triple-as-hyperscale-ai-demand-soars/)

重点一手 PPTX：

- [IDC：Understanding the EMEA Adoption of OCP Designs](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7986/5265c5cc-296a-4d3e-86c7-2640a67fc7f3-idc-ocp-emea-regional-summit-slides-042226-76a376caae31d772d1a5c91270efa0ff.pptx)
- [Open Data Center for AI](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8069/1582675c-5782-4bc5-abd5-5531b27d3212-emea-summit-presentation-combined-9cd0a618bbd8155db966bb4ab334b462.pptx)
- [ORv3 and HVDC Power Systems](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7959/dac565c0-6ed3-4921-9748-0f7bd6ee299d-ocp-barcelona2026-requirements-considerations-of-next-generation-ai-power-shelves-a1fe41e844a1e7d1f59171f4c702a15e.pptx)
- [LVDC Power Distribution](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8109/90ea68d8-1d2a-45f2-a1c6-9f5d3c5e7767-emea-summit-lvdc-power-distribution-breakout-apr-2026-1-5e54c577caa1055218ce4b65befd4b6e.pptx)
- [DC Microgrids and 800V/750V/1500V](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8113/4d9e2248-81b4-4b2b-a4cd-a8a5fd2b37ee-emea-summit-bridging-the-worlds-of-data-centers-and-direct-current-microgrids-april-2026-e692412e6dba44a1ce3c44ce76b9ab35.pptx)
- [Cooling Environments and Cold Plate](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7923/d53d3b7f-b935-4ead-9af8-31db4337a606-ce-industry-analytics-project-progress-and-cold-plate-developments-5507e512d35bc1739f9f67c18ff4f7e2.pptx)
- [Coldplate Base Specification](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8210/15b3228c-7568-4d4d-ae35-e8a1816d9d0a-ocp26e-presentation-template-breakouts-final-260301-1-18206612699d5a86c8e715fb22abc3bc.pptx)
- [UQDv2 Interoperability](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7997/066da0b3-e950-45d7-bc9d-bd0d7f78ec58-2026-emea-summit-uqdv2-interoperability-langer-final-cbefc92fd305764961b54c8aad649598.pptx)
- [Liquid Cooling TCO Tool v1.3](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8130/89e632e4-5d21-46bf-8488-0e4123d28d34-tco-model-for-liquid-cooled-dcs-final-9c0a24a4c8b0144afd82c37765b1ad9a.pptx)
- [Immersion Cooling in 2026](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/7929/28c7d464-47b2-4c20-bb0a-263129481bbb-immersion-cooling-in-2026-project-progress-industry-adoption-and-the-path-ahead-f3e2789e48ddc21620e4b968cc7f5442.pptx)
- [UALink and OCP](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8020/5ec17fde-a9c6-41ae-aa9d-a47592627aa7-ualink-ocp-emea-2026-presentation-v3-2f696567e0e8035e72bc91bd8bb29dcf.pptx)
- [ESUN 1.0](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8167/8d2fdc59-a74c-40aa-8176-e8ca1bb4b2d1-ocp-esun-ethernet-for-scale-up-network-final-cb64e37dce850945d9dc444b0784021a.pptx)
- [SUE-T](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8303/8c05a8bf-356c-43d4-922c-266498c210a5-lamb-sue-t-barcelona-april-2026-final-ebd957466b2d9c4f55fd5f4d47b8ceb4.pptx)
- [800G and 1.6T Open AI Fabrics](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8133/35a23685-896a-4b24-8098-af5e51b98711-high-performance-ai-fabrics-built-on-open-standards-ocp26e-afcf29264b11ba69ef36c4cba82712f3.pptx)
- [Silicon Photonics Switching](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8389/fe72d64c-44d5-44e3-b7d7-78a41a40b026-ocp-2026-ipronics-final-dcb5cba6b3949c687b3d569d3c5c197e.pptx)
- [400G/lane CPO and wafer-scale optical interconnect](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8386/984c946b-194e-4668-ba72-b5c5ee49a865-ocp26e-presentation-possieur-towardswaferscaleoi-relyingonsiliconphotonicsandadvanced3dassembly-final-2fa5516b0edaf6c6a8de9ccae4bf2f3b.pptx)
- [Multi-Core Fiber](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8343/b28513f2-989b-49ab-a4e3-34fc51f510d6-sel-041726-ocp-emea-presentation-v1-with-notes-5db05222a5d401ca94187823329ae26a.pptx)
- [FCSA and composable chiplets](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8176/61eeb8da-47cf-41c3-a774-06ef0cd6b97c-ocp26e-accelerating-composable-chiplets-knight-thur-0910-v2-21fd76d43631a1cb7feaf87e9841ae89.pptx)
- [Chiplet electrical-optical connectivity](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8259/0f93eaac-e8fe-432c-98cb-a8735c1f0e15-ocp-2026-enginnering-the-chiplet-era-letizia-giuliano-final-987b3d911cbf91da313dde9654174ddc.pptx)
- [Caliptra Update](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8282/822259d7-f1b0-42c6-8c21-362e7fbaf5f1-ocp26e-caliptra-update-c0d90babac26c4cc4c77dc1c755b630c.pptx)
- [OCP S.O.L.I.D.](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8077/75859441-fb86-4b3b-b420-fb06554d5960-introducing-ocp-solid-af93c4c38d6ef5ba51cacac84a44f2c1.pptx)
- [OCP L.O.C.K.](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8071/546465f7-d7d2-402b-a908-5a8cbb428cc7-ocp-emea-2026-lock-update-6af03716383450784be20acf7aade56b.pptx)
- [openSFI Update](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8090/5933d80c-f1d8-44ff-aeca-f53160c7dc9a-ocp26e-presentation-opensfi-update-d0e0136381b413f6c4239a13fbe0d29e.pptx)
- [Meta Hardware Circularity](https://fntech.sfo2.digitaloceanspaces.com/PresentationMediaUploads/70/8211/3b15125e-1d29-482f-93f5-bea131a5d458-hardware-circularity-at-scale-ocp-emea-2026-1-ab7602f6c32d1886a4e1cfaa3e1440f8.pptx)
