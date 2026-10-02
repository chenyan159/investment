# APEC 2026会议追踪：核心变化、产品爆发和市场预期差

会议对象：APEC 2026，即 IEEE Applied Power Electronics Conference and Exposition，不是亚太经合组织会议。  
会议日期：2026-03-22 至 2026-03-26。  
会议地点：Henry B. Gonzalez Convention Center, San Antonio, Texas。  
材料检索截止日期：2026-06-10，美国太平洋时间。  
报告完成日期：2026-06-10，美国太平洋时间。  
研究边界：本报告只使用公开联网材料、会议官方材料、公司一手材料、公开视频/会后评论和公开市场研究口径；未读取、引用或继承本项目内既有公司调研、行业调研、日度资料、特征量化、tmp、data 或旧缓存。

## 结论摘要

APEC 2026 的最大变化不是“功率半导体继续增长”这个老结论，而是 AI 数据中心把电源从后台配套推到系统架构核心：会议官方 program book 显示本届包含 570+ 技术论文、170+ 行业报告、310+ 展商，AI 数据中心、800VDC、垂直供电、3D power packaging、GaN/SiC、电源数字控制、磁性件/电容和储能瞬态管理成为最密集的交叉主题。

最大机会：AI 机柜从 30-40kW、100-200kW 继续走向 600kW-1MW 级别时，54V/48V 机柜内配电的铜损、空间、热和动态响应开始成为平台约束。NVIDIA 在 2025-05-20 的 800VDC 架构材料中明确指向 2027 年开始支持 1MW IT racks and beyond，并列出 ADI、Infineon、MPS、Navitas、onsemi、Renesas、ROHM、ST、TI、Delta、Flex、LiteOn、Megmeet、Eaton、Schneider、Vertiv 等生态伙伴；APEC 2026 的变化是这些方向从架构白皮书进入多家公司 reference design、full-brick、IBC、VPD、TLVR、digital controller 和 BBU/ESS 讨论。

最大分歧：市场容易把“800VDC、GaN、AI 电源”合并成一个线性放量故事，但 2026 年仍主要是样品、参考设计、客户测试和 2027 平台前置设计。未来 12 个月真正可兑现收入的概率排序应为：AI 服务器 VR/PoL/TLVR/控制器和高功率 PSU > 48V/12V 中间母线模块 > 800VDC HV IBC 小批量 > 高压 GaN 1250V/1700V > 中压固态变压器/固态断路器。后两类技术弹性大，但收入确认更晚。

最大反共识：SiC 在本届 APEC 仍重要，但边际叙事从 EV 主导转向 AI 数据中心中压/高压、SST、BESS、PFC 和基础设施。由于 2025-2026 年 SiC 仍受 EV 放缓和产能吸收影响，AI 数据中心短期不足以完全抵消 SiC 周期压力。反而是低压大电流电源模块、磁性件、电容、热设计、测试认证、数字控制和系统电源厂商，在未来 12 个月的订单兑现度可能高于纯高压器件故事。

最值得跟踪的产品：1）800VDC to 50V/48V 或 12V HV IBC；2）AI xPU 核心电源的 VPD/TLVR/多相 buck 模块；3）1250V/1700V GaN 与 650V GaN 的高频高密度 DC/DC；4）12kW/8.5kW/4.5kW AI server PSU/OCP/CRPS；5）BBU/ESS 与热插拔 MOSFET；6）硅电容、嵌入式无源和高频磁性件；7）SST、固态断路器和中压电网接口；8）电源数字控制、PMBus telemetry、仿真和测试平台。

## 会议重点和方向变化

### 核心主题总表

| 主题 | 会议/公司证据 | 关键参数 | 变化性质 | 产业判断 |
|---|---|---:|---|---|
| AI 数据中心 800VDC 架构 | APEC IS04、IS07、IS30；NVIDIA 800VDC 生态；TI grid-to-gate；Infineon HV IBC；Navitas 800V-to-50V | 800VDC 或 +/-400V；1MW rack 目标；NVIDIA 称 54V 在 >200kW 后遇到物理限制 | 从架构讨论进入多公司参考设计和展会 demo | 2026 是设计导入年，2027 才是关键收入验证年 |
| 垂直供电 VPD / TLVR / 核心 rails | APEC IS30 Vertical Power for AI Data Centers；Empower Crescendo；Infineon TDM24745T/TDM2454xx | Infineon TLVR 模块 9x10x5mm、>2A/mm2、320A peak；Empower 目标 5A/mm2 | 从背板/PCB 侧向供电转向 processor-proximate 供电 | 未来 12 个月收入兑现度最高，赢家可能是模块/控制器/封装而非单颗 MOSFET |
| 高压 GaN 进入 800VDC | Power Integrations 1250V/1700V PowiGaN；Navitas 650V/100V GaNFast；Infineon 650V CoolGaN | PI 称 1250V/1700V 已量产，>98% 800VDC 主电源要求；Navitas 10kW full brick 98.5% peak、2.1kW/in3 | GaN 从消费快充/低压高频扩展到 AI DC/DC 和辅助电源 | 技术信号强，收入基数仍小；高压可靠性和客户认证是最大变量 |
| SiC 从 EV 扩展到 grid-to-rack | Navitas SiCPAK 2300V/3300V；Infineon Si/SiC/GaN grid-to-core；SST/solid-state breaker 议题 | 13.8-34.5kVAC 到 800/1500VDC，>98% 转换目标 | SiC 的新故事从车转向 AI 电网接口和中压电源 | 不是 2026 年快速爆发，更多是 2027-2028 产能吸收后的第二增长曲线 |
| BBU/ESS 与动态响应 | APEC exhibitor presentation：Nyobolt AI Data Centres Meet Dynamic Response Systems；Advanced Energy 会后总结 | 从 GPU chip/input bus BBU 到 building-scale ESS 和 front-of-meter MV | AI 负载突变成为电源/电网稳定性问题 | 储能、supercap、热插拔、保护器件的重要性上升 |
| 电源数字控制与 telemetry | Infineon XDPP1188-200C、XDPE1E、TDA49720/12/06；PMBus/AVSBus/SVID/SVI3 | 48V to 12V/lower；800VDC to 48/24/12V；6A/12A/20A PoL | 电源从 analog block 变成可观测、可调参、可诊断系统 | 软件/firmware、控制器和 telemetry 是利润池上移方向 |
| 磁性件、电容和封装 | APEC IS04：Murata silicon capacitors、Saras embedded passives、3D power packaging；PSMA magnetics/capacitor workshops | 高频化提高对 planar transformer、matrix transformer、低 ESL/ESR、嵌入式电容需求 | 被低估的配套瓶颈 | ASP 和认证粘性可能优于普通分立器件 |
| 双向 GaN | Advanced Energy 会后称 monolithic bidirectional GaN 在 APEC 获大量关注，已有一家大型 microinverter 厂商量产 | 单片双向开关替代多 die 方案 | 新品类 0 到 1 | 最先落在微逆、矩阵变换器、保护/切换，AI 数据中心短期是可选性 |
| AI tools / digital twin | APEC IS02、IS08；AI and Digital Twins Transforming Power Device Innovation | 设计自动化、仿真、控制优化 | 研发效率主题，不是直接产品爆发 | 对 EDA/仿真/测试设备是中期利好 |

### 和 APEC 2025、过去 6-12 个月相比的变化

2025 年 APEC 已出现 AI 数据中心电源和 800VDC 话题，官方 2025 program 的 AI 数据中心 power delivery 摘要已经提到单 AI/ML rack 功率从 30-40kW 走向 200kW 以上，并要求 800V DC bus、SiC/GaN、高压 AC/DC、DC/DC、48V 中间母线和多相 GPU/CPU 架构。因此 800VDC 不是 APEC 2026 才出现的新概念。

APEC 2026 的增量在三点：第一，NVIDIA 800VDC 架构发布后，生态伙伴名单和 2027 平台目标给供应商提供了明确设计锚，会议材料不再只是“为什么需要 800V”，而是“谁能把 800V 转成 50V/12V、谁能做 1MW rack 的保护、储能和控制”。第二，Infineon、Navitas、Power Integrations 等把性能数字拿到展台和发布稿中，参考设计进入 6kW/10kW/12kW 级别。第三，VPD/TLVR 从“先进封装讨论”变成 AI xPU 核心 rails 的工程瓶颈，电流密度、瞬态响应、输出电容减少和散热方式开始决定系统设计空间。

放缓或需要降温的方向：EV SiC 不是本届边际最强主题；传统快充 GaN 仍在，但市场关注转向数据中心和工业/电网；800VDC 基础设施不会在 2026 年大规模收入确认，主要原因是 rack 平台、保护标准、连接器、运维安全、认证和数据中心侧部署节奏仍未完全锁定。

### 真实变化与展会叙事分层

已经有产品/样品/参考设计支撑的真实变化：Infineon HV IBC 两个参考设计、TDM24745T TLVR 模块、XDPP1188-200C 控制器；Navitas 10kW 800V-to-50V full-brick 和 12kW AI data center PSU；Power Integrations 1250V/1700V PowiGaN 与 InnoMux2-EP；Empower VPD 平台和真实客户实现；TI 800V power architecture 与 IsoShield 隔离模块。

有生态/标准方向支撑但仍待订单验证的变化：NVIDIA 800VDC 从 2027 年开始的 1MW rack 方向；SST/solid-state breaker 从中压电网直连 AI 数据中心；BBU/ESS 从 UPS 后备电源转向 rack、row、building 和 front-of-meter 多层动态缓冲；AI tools/digital twin 对电源设计流程的实际缩短周期。

仍偏概念或远期可选性的变化：把所有 GaN 都映射成 AI 数据中心爆发；把 SiC 电动车产能压力完全转化成 AI 电源需求；把 800VDC 当成 2026 年通用数据中心标准；把非官方“会场爆满”直接等同订单爆满。

## 产品和技术路线三情景预测

以下市场规模为美元口径。外部市场口径与本报告估算分开：MarketsandMarkets 2025-09 口径下，全球 data center power market 为 2025 年 351.4 亿美元、2030 年 505.1 亿美元、2025-2030 CAGR 7.5%；Yole 2025 口径下，power GaN 从 2024 年 3.55 亿美元增长至 2030 年约 30 亿美元、2024-2030 CAGR 42%；Yole 2024/2025 口径下 power SiC 接近 2029/2030 年 100 亿美元级别。本报告对 APEC 相关细分市场的 2026/2027 估算，均基于这些公开口径、会议产品参数和 adoption 假设。

| 方向 | 2026 成熟度 | 2026 当前规模估算 | 未来 12 个月基准 | 乐观 | 超预期乐观 | 利润率/价值捕获 |
|---|---|---:|---:|---:|---:|---|
| 800VDC HV IBC、800V-to-50V/12V | reference design/样品/客户测试；部分 full-brick demo | 0.5-1.5 亿美元，主要为工程样品、评估板、小批量和 NRE | 1.5-4 亿美元，导入 2027 rack 设计，渗透 AI 高密 rack power BOM 1-3% | 4-8 亿美元，头部云厂和 OEM 提前小批量 | 8-15 亿美元，Kyber/Rubin 前置采购放大 | 器件毛利 40-60%，模块/系统 25-40%；短期价值在参考设计、控制器、磁性件、热结构 |
| AI xPU VPD/TLVR/核心电源模块 | 小批量/量产导入并存；平台绑定度高 | 10-18 亿美元，包含高端 AI accelerator VR、PoL、power stage/module | +30-50%，规模 13-27 亿美元 | +60-90%，规模 16-34 亿美元 | +100% 以上，若多 kW xPU 加速切换 VPD | 模块/控制器/封装利润池最大；纯低压 MOSFET 被集成模块压缩 |
| 高压 GaN 1250V/1700V 与 650V GaN AI DC/DC | 650V GaN 已较成熟；1250/1700V 少数供应商量产或客户认证 | 全球 power GaN 约 7-9 亿美元；AI 数据中心子市场 <1 亿美元 | 全球 power GaN 约 10-13 亿美元；AI 子市场 1-3 亿美元 | AI 子市场 3-5 亿美元 | AI 子市场 5-8 亿美元，若 800VDC 主变换器采用超预期 | 早期高毛利但认证慢；赢家在高压可靠性、驱动/保护集成和 reference design |
| SiC 中压模块、SST、solid-state breaker | 工业/EV 已成熟；AI grid-to-rack 仍样品/示范 | 全球 power SiC 约 45-60 亿美元；AI/数据中心相关 <3 亿美元 | 全球 +10-18%；AI/数据中心 3-6 亿美元 | 全球 +20-30%；AI/数据中心 6-10 亿美元 | AI/数据中心 >10 亿美元，但需中压架构落地 | EV 周期压制短期 ASP；中压 SiC 模块、驱动、绝缘和封装可获得更高附加值 |
| 12kW/8.5kW/4.5kW AI PSU、OCP/CRPS | 量产/平台升级阶段 | 数据中心电源市场 2026 推算约 378 亿美元；AI PSU/电源柜子集 80-120 亿美元 | +10-18%，AI PSU 90-140 亿美元 | +20-30%，AI PSU 100-155 亿美元 | +35% 以上，若 600kW rack 密度快速普及 | 系统厂、ODM、控制器、磁性件和热管理共同分利；硬件系统毛利通常低于器件 |
| BBU/ESS、热插拔 MOSFET、保护 | AI 机柜/row/building 多层导入早期 | AI 数据中心电源保护和储能子市场 10-25 亿美元 | +15-25%，BBU/ESS 从后备走向动态响应 | +30-50% | +70% 以上，若电网接入和负载突变成为强制设计项 | 电池系统毛利中等，控制/保护/监控和认证价值更高 |
| 硅电容、嵌入式无源、高频磁性件 | 已进入 demo/客户实现；供应链分散 | AI 电源相关无源/磁性件 5-10 亿美元 | +20-35% | +40-60% | +80% 以上，若 VPD 和高频 LLC 大量采用 | 被低估利润池；认证、材料、专有结构和交期形成壁垒 |
| 双向 GaN、单级矩阵/微逆/切换 | microinverter 有量产线索；AI 内部应用早期 | <1 亿美元 | 1-2 亿美元 | 2-4 亿美元 | >5 亿美元，取决于微逆、OBC、数据中心保护/切换采用 | 0 到 1 品类，高弹性但应用分散；需要跟踪真实设计 wins |
| 电源数字控制、telemetry、仿真测试 | 控制器量产/采样；测试设备需求明确 | AI 电源控制/监控/测试子市场 5-12 亿美元 | +15-30% | +35-50% | +60% 以上 | 软件、firmware、控制算法和测试认证更接近高质量利润池 |

### 爆发力度排序

主链条替代：800VDC HV IBC、VPD/TLVR、AI PSU。它们直接决定 rack power density 和系统可部署性，若 NVIDIA 2027 架构按时推进，2026 下半年至 2027 上半年会出现设计 win 和认证密集披露。

小品类高增速：高压 GaN、双向 GaN、嵌入式无源、硅电容、specialized hot-swap MOSFET。这些市场绝对规模小，但增速和技术弹性高，适合寻找小公司或上游瓶颈。

供给瓶颈涨价：高频磁性件、低剖面 transformer、低 ESL/ESR 电容、液冷兼容电源模块封装、800VDC 安全连接/保护组件。这些不一定有漂亮的 TAM，但可能在平台切换时出现交期和认证溢价。

新市场从 0 到 1：SST/solid-state breaker 进入 AI 数据中心中压配电、BBU/ESS 从后备电源变成动态负载缓冲、单片双向 GaN 用于更简单的单级拓扑。

## 市场规模和利润池

### 1. 数据中心电源基础设施

当前规模：MarketsandMarkets 2025-09 披露全球 data center power market 2025 年 351.4 亿美元、2030 年 505.1 亿美元、CAGR 7.5%，组件包括 UPS、PDU、generators & energy storage、power management software & DCIM。按 7.5% 年增速外推，2026 年约 377.8 亿美元。该口径是整个数据中心电源市场，不等于 AI 高密 rack 电源市场。

未来一年：基准情景 2027 年约 406 亿美元，其中 AI 高密度需求贡献增量但传统云/colo 仍占大头；乐观情景约 420-440 亿美元，假设 hyperscale AI 建设和电源升级超越行业均值；超预期乐观约 450 亿美元以上，假设电网接入、液冷和高功率 rack 项目集中落地。

利润率：系统级 power infrastructure 的长期毛利率通常低于高端电源 IC，估算 25-40%；DCIM、控制软件、监控、维护服务和高可靠系统集成可更高。价值捕获优先级为：系统集成与服务、控制软件/监控、UPS/PDU/switchgear、BESS、最后才是通用电力设备。

### 2. 800VDC 高压母线和 HV IBC

当前规模：2026 年仍是 early adoption。本报告估算 2026 年 800VDC AI data center 相关 HV IBC、评估板、样品、NRE 和小批量器件合计约 0.5-1.5 亿美元，置信度中低。假设链条：2026 年全球 data center power market 约 378 亿美元；AI 高密度相关占 20-30%；800VDC 真正采用率仅 0.5-2%；其中可归属于 HV IBC/控制/器件/参考设计的价值占早期系统 BOM 10-25%。

未来一年：基准 1.5-4 亿美元；乐观 4-8 亿美元；超预期乐观 8-15 亿美元。关键假设是 2027 NVIDIA 800VDC/Kyber/Rubin 相关平台是否按时进入系统设计冻结、云厂是否接受 800VDC 运维安全体系、以及 UL/IEC/数据中心内部标准是否及时匹配。

利润率：高压 GaN/SiC 器件和控制器早期可维持 40-60% 毛利率，但 reference design 期的 revenue quality 不稳定；模块和系统一般 25-40%；磁性件、封装和控制软件会吃掉大量价值。长期更赚钱的是“通过平台认证的模块+控制器+保护+热设计组合”，不是裸 die。

### 3. AI xPU 核心供电：VPD/TLVR/PoL/多相 buck

当前规模：本报告估算 2026 年 AI/HPC accelerator 核心供电、非核心 rail PoL、控制器和高端 power stage/module 合计约 10-18 亿美元，置信度中等偏低。估算链条：高端 AI accelerator 与交换芯片功耗继续上升；每颗多 kW xPU 需要数千安培核心电流、多个非核心 rails 和 telemetry；单系统 power delivery BOM 高于传统服务器一个数量级。

未来一年：基准增长 30-50%，乐观 60-90%，超预期乐观 100% 以上。爆发强度高于 800VDC，因为它不必等整个数据中心配电标准切换，现有 48V/54V AI 服务器也需要更强 VR、PoL、TLVR、低剖面电感、硅电容和数字控制。

利润率：高端控制器、integrated power stage 和专有封装模块可有 40-60% 毛利率；普通 MOSFET 和 commodity inductor 毛利较低。价值捕获层级为控制器/算法/telemetry、集成模块、低剖面磁性件、嵌入式/硅电容、最后是标准分立器件。

### 4. Power GaN

当前规模：Yole 2025 报告公开摘要显示 power GaN market 从 2024 年 3.55 亿美元增长至 2030 年约 30 亿美元，2024-2030 CAGR 42%。按该 CAGR 外推，2026 年全球 power GaN 约 7.2 亿美元，2027 年约 10.2 亿美元。AI 数据中心相关 GaN 目前仍小，2026 年估算低于 1 亿美元。

未来一年：基准情景全球 power GaN 到 2027 年约 10-13 亿美元，AI 子市场 1-3 亿美元；乐观情景 AI 子市场 3-5 亿美元；超预期乐观 5-8 亿美元。核心假设是 800VDC 主变换器、辅助电源、48V/12V DC/DC 和高频 PSU 是否采用 GaN，而不是只把 GaN 留在消费快充和低功率适配器。

利润率：高压 GaN 通过可靠性和平台认证后，单价和毛利率应好于成熟低压 silicon；但 2026-2027 年仍有客户验证、良率、封装、driver/protection 集成和供应商集中度风险。价值捕获更可能在高压 GaN IC/集成驱动/保护/参考设计，而不是离散裸开关。

### 5. Power SiC

当前规模：Yole 公开口径显示 power SiC device market 接近 2029/2030 年 100 亿美元级别，2023-2029 CAGR 约 24%；本报告估算 2026 年全球 power SiC 市场约 45-60 亿美元，仍以 EV traction inverter、OBC、DC fast charging、PV/BESS 和工业为主，AI 数据中心直接贡献小于 5%。

未来一年：基准情景全球增长 10-18%，乐观 20-30%，超预期乐观 35% 以上。APEC 2026 对 SiC 的真实增量是中压固态变压器、solid-state breaker 和 800/1500VDC grid interface；但这些多为 2027-2028 之后放量，不足以立刻解决 2025-2026 年 EV 节奏和产能吸收问题。

利润率：SiC 衬底/外延/器件/模块链条仍有制造壁垒，但产能过剩会压制部分标准器件 ASP。价值捕获更偏向高压/中压模块、可靠封装、驱动保护、系统认证和极端工况数据，而不是低附加值产能扩张。

### 6. 无源、磁性件、测试认证

当前规模：本报告估算 AI 数据中心电源相关高端无源和磁性件 2026 年约 5-10 亿美元，电源测试、HIL、认证和精密测量约 5-12 亿美元。置信度中低，但方向确定：高频化和 VPD 会减少传统大体积磁性件，同时提高对低剖面、高饱和、低损耗、可散热和可量产结构的要求。

未来一年：无源/磁性件基准增长 20-35%，乐观 40-60%，超预期 80% 以上；测试认证基准增长 15-30%，乐观 35-50%。利润率取决于是否具备专有材料、专有结构、客户认证和供货稳定性。长期价值捕获可能高于市场认知，因为这类环节更难被 AI 叙事直接看到，但最容易卡住量产。

## 反共识洞见和重要更新

### 市场可能过度乐观的方向

1. 800VDC 不是 2026 年规模收入。NVIDIA 明确目标是 2027 年开始支持 1MW racks and beyond，APEC 2026 的 reference design 是设计导入信号，不是大规模订单信号。若 2026 年公司把 800VDC 说成当年收入主因，需要警惕。

2. 高压 GaN 不会一夜替代 SiC。Power Integrations 的 1250V/1700V PowiGaN 信号很强，但客户会同时评估 stacked 650V GaN、1200V SiC、silicon superjunction、封装热阻、短路、EMI、驱动复杂度和供应安全。高压 GaN 更像高弹性新分支，不是确定性全替代。

3. SiC AI 数据中心叙事容易被高估。AI 数据中心会使用 SiC，但 SiC 2026 主市场仍是 EV/industrial/PV/BESS。若 EV 放缓、价格下行和产能爬坡压力持续，AI 方向短期无法完全抵消。

4. “会场爆满”不是订单。Advanced Energy 的会后总结称 AI power sessions 多次满场甚至排队，这是强情绪信号；但核心结论仍需要后续 design win、样品转量产、客户认证和财报订单验证。

### 市场可能低估的方向

1. VPD/TLVR 比 800VDC 更早兑现。AI xPU 核心 rails 的电流密度和瞬态响应是现有平台就需要解决的问题，Infineon TDM24745T 这类 320A、>2A/mm2、输出电容减少 50% 的模块，较 800VDC 基础设施更可能先进入收入。

2. 硅电容、嵌入式无源和磁性件是隐藏瓶颈。APEC IS04 将 Murata silicon capacitors、Saras embedded passives、Google Cloud AI/ML power and cooling、Infineon data center power 放在同一主题下，说明利润池不只在 MOSFET/GaN/SiC。低 ESL/ESR、近芯片去耦、低剖面 transformer 和 matrix transformer 会决定 VPD/IBC 能否量产。

3. Hot-swap MOSFET 和保护被低估。Nexperia 在 exhibitor presentation 中专门讨论 AI data center hotswap MOSFET 的 SOA、inrush、board insertion、fault response、thermal stress 和 expensive accelerator protection。AI 硬件价值越高，保护器件的规格和 ASP 越容易上移。

4. BBU/ESS 从“后备电源”变成“动态算力资产”。Nyobolt 的 APEC presentation 将 BBU/supercap/bulk ESS 从 GPU input bus 到 building-scale、front-of-meter 连接起来，说明 AI 负载突变和 power quality 可能带来新的储能控制利润池。

5. 数字控制和 telemetry 是系统级粘性。PMBus、AVSBus、SVID、SVI3、Digital Scope、Black Box recording、nonlinear fast transient response、phase shedding 等功能，会让电源 IC 从 commodity component 变成平台 bring-up 和运行监控的一部分。

### 看起来相关但弹性可能不强的公司/产品

普通低压 MOSFET、普通电感、普通电解电容、标准服务器 PSU 代工和传统工控电源公司，如果没有 AI rack 认证、VPD/800VDC reference design、液冷兼容封装、数字控制或 hyperscaler/OEM 平台绑定，收入暴露和利润弹性可能弱于表面叙事。

大型综合半导体公司如 TI、Infineon、ADI、onsemi、ST、Renesas 参与度高，但 AI 电源收入相对公司总收入的弹性不同。大公司胜在平台覆盖和客户信任，小公司如 Navitas、Power Integrations、Empower 类方向胜在单品弹性，但也承受客户集中、认证延期和现金流波动。

### 证伪后应下修的结论

如果 2026 年下半年至 2027 年上半年，NVIDIA/云厂/OCP 没有进一步披露 800VDC safety、connector、protection、sidecar/row-level 架构和供应链设计冻结，应下修 800VDC 收入斜率。

如果 AI accelerator 下一代功耗没有继续向多 kW 级上移，或芯片封装/供电架构选择保守，则 VPD/TLVR 的渗透率和 ASP 应下修。

如果高压 GaN 在 800VDC 主变换器中出现可靠性、EMI、认证或良率问题，则高压 GaN 的 2027 收入应从乐观情景降回基准，SiC 和 stacked silicon/GaN 方案会保留份额。

如果 EV SiC 价格继续下行且 AI 中压需求未形成订单，SiC 公司估值不应给太高 AI 数据中心期权。

## 公司和产业链映射

### 头部综合供应商

Infineon：本届 APEC 的产品密度最高之一，覆盖 HV IBC、XDPP1188-200C、XDPE1E、TDA49720/12/06、TDM24745T、TDM2454xx、Si/SiC/GaN、SST/solid-state breaker。收入暴露分散，投资弹性不如小公司，但技术路径最完整。最值得跟踪：TDM24745T/TDM2454xx design win、800VDC HV IBC 客户采用、AI data center revenue disclosure。

Texas Instruments：APEC 主推 IsoShield isolated power modules、800V grid-to-gate、EV/48V、SST 和 humanoid/industrial。TI 的机会在隔离、模拟、控制、gate driver、power module 和工业客户基础；弹性较低但确定性高。跟踪点：800V data center 参考设计、隔离电源模块出货、AI server 客户披露。

ADI：会议材料中以生态参与和电源/模拟能力为主；会后对 Empower Semiconductor 的收购公告若完成，将强化高密度 VPD/AI power portfolio。跟踪点：Empower 技术是否进入 ADI 大客户渠道、VPD 模块量产时间。

onsemi、ST、Renesas、ROHM、MPS、Nexperia：均在 NVIDIA 800VDC 或 APEC 展商/议题生态中出现。MPS 与 Renesas 在 AI server power controller/module 具备较直接弹性；Nexperia 的 hotswap MOSFET 和 WBG package 线索说明保护器件不是小事。

### 高弹性小公司和专业公司

Navitas：APEC 发布 10kW 800V-to-50V GaN full-brick、98.5% peak efficiency、2.1kW/in3、12kW AI PSU、8.5kW OCP、4.5kW CRPS，以及 2300V/3300V SiCPAK。优点是叙事纯度高、参数清楚；风险是量产客户、现金流和大公司竞争。投资弹性高，需严查 backlog、design win 和 gross margin。

Power Integrations：1250V/1700V PowiGaN 是差异化高压 GaN 线索，且公司称相关器件量产、GaN switches 累计 1.75 亿颗以上应用。优点是高压集成 IC、可靠性记录和辅助电源；风险是 AI 数据中心主电源采用速度和总可服务市场。更像中高确定性、高技术弹性标的。

Empower Semiconductor：Crescendo VPD、硅电容、5A/mm2 目标和真实客户实现，是 VPD 方向代表。若并入 ADI，单独股权弹性消失，但证明大模拟厂愿意为 VPD 买技术。对产业链含义大于单一标的交易价值。

Advanced Energy：会后总结强调 AI power sessions、VPD、800V、energy storage、1MW rack path。公司更偏精密电源和系统，受益于半导体设备、医疗和数据中心 power；不是纯器件弹性，但可作为行业验证样本。

### 上游瓶颈与配套环节

高频磁性件：planar transformer、matrix transformer、低剖面电感、TLVR inductor、integrated magnetics。瓶颈来自高频损耗、热、自动化制造和客户认证。关注 Murata、Payton、Pulse/Bel、Vishay、Coilcraft、Bourns、伍尔特、TDK 等公开产品节奏。

电容与嵌入式无源：硅电容、MLCC、电解/薄膜混用、低 ESL/ESR、近芯片去耦。APEC IS04 将 silicon capacitors 和 embedded passives 放在 AI power packaging 中，说明其不是普通 BOM。关注 Murata、TDK、Kyocera AVX、KEMET/Yageo、Saras Micro Devices、Empower silicon capacitors。

保护和连接：hotswap MOSFET、solid-state breaker、fuse/disconnect、800VDC connector、绝缘、arc fault、PMBus/telemetry。AI accelerator 单机价值上升，会拉高保护器件规格和认证粘性。

测试认证：Yokogawa、Keysight、Chroma、NI/Emerson、OPAL-RT、RTDS、OMICRON、Typhoon HIL 等。800VDC、SST、VPD、高频 GaN/SiC 都需要更复杂的效率、瞬态、EMI、热和安全测试。

### 伪受益或弱受益

仅有普通功率器件、普通服务器电源、普通工业电容/电感、没有 AI rack 认证、没有高密封装和没有数字控制能力的公司，可能在“AI power”叙事中被短期拉升，但实际收入弹性弱。需要从客户名单、design win、样品到量产时间、ASP、产能、毛利率四项交叉验证。

## 风险、反证条件和后续跟踪

### 核心风险

技术风险：800VDC safety/protection/connector 标准不成熟；高压 GaN 可靠性和 EMI 问题；VPD 热管理、可维修性和封装良率；SST/solid-state breaker 在数据中心运维体系中的保守采用。

需求风险：AI capex 节奏放缓；云厂从训练转向推理导致 rack 架构变化；下一代 xPU 功耗不及预期；电网接入延迟导致数据中心建设延期。

供给风险：GaN/SiC 产能、封装、磁性件、电容、液冷和测试资源错配；SiC 过剩压价；小公司融资和客户集中。

利润率风险：大客户议价强、参考设计期 NRE 高、模块化带来系统厂压价、竞争从器件效率转向平台认证后 ASP 下滑。

### 后续跟踪节点

2026-06 至 2026-08：APEC 2026 technical paper 在 IEEE Xplore 的正式收录和公司 presentation 是否公开；NVIDIA、OCP、Open Rack、PSMA 是否披露 800VDC 进一步标准细节。

2026-07 至 2026-10：Infineon、TI、ADI、MPS、onsemi、Renesas、Navitas、Power Integrations、Advanced Energy 等公司财报中是否出现 AI data center power、800VDC、VPD/TLVR、HV GaN 的订单或 design win。

2026-10：OCP Global Summit 2026，重点看 800VDC safety、connector、sidecar/row-level 架构、BBU/ESS、液冷和平台伙伴。

2027-03：APEC 2027，新奥尔良。若 800VDC 仍停留在 reference design，没有更多客户/标准/量产节点，需下修 2027-2028 渗透率。

刷新频率：800VDC/VPD/GaN 路线每月刷新公司发布和 OCP/NVIDIA 资料；市场规模和利润率每季度结合财报刷新；SiC 周期每季度关注价格、库存、capex 和 EV 需求。

## 来源清单

### 一手官方

1. APEC 2026 Conference Program Book，会议官方 PDF，2026-02-23 版本，可信度高。关键信息：会议日期/地点、570+ papers、170+ industry presentations、310+ exhibitors、IS04/IS07/IS30/IS08 等议题、展商列表。URL: https://apec-conf.org/wp-content/uploads/2026/03/APEC-2026-Program-Book-20260223.pdf

2. APEC 2026 官方网站，会议主页和 floor plan，2026 年会议页面后续已切换到 2027，但仍保留 APEC 2026 highlights 和 floorplan 入口，可信度高。URL: https://apec-conf.org/

3. NVIDIA Technical Blog: “NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories”，2025-05-20，可信度高。关键信息：2027 年开始支持 1MW IT racks and beyond、54V 在 >200kW 后受限、1MW rack 54V busbar 铜需求、800VDC 生态伙伴和 up to 5% end-to-end efficiency improvement。URL: https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/

4. APEC 2025 Program Book / Eventscribe AI data center power delivery 摘要，2025-02/2025-03，可信度高。用于比较：2025 已出现 800V DC bus、rack power beyond 200kW、SiC/GaN、48V intermediate bus 等主题。URL: https://apec-conf.org/wp-content/uploads/2025/03/APEC-2025-Program-Book-Web-Version-20250220A.pdf

### 一手公司

5. Texas Instruments APEC 2026 event page，2026 年会议材料，可信度高。关键信息：Booth #1819、IsoShield isolated power modules、3x higher power density、800V power architectures、grid-to-gate、EV/48V/SST/humanoid demos。URL: https://www.ti.com/about-ti/events/apec.html

6. Infineon APEC event page，2026 年会议材料，可信度高。关键信息：Booth #1619、AI and data center from grid to core、Si/SiC/GaN、power infrastructure、solid-state circuit breakers。URL: https://www.infineon.com/event/apec

7. Infineon: “CoolGaN-based HV IBC reference designs for 800 VDC architectures in AI data centers”，2026-03-17，可信度高。关键信息：800VDC/+/-400V to 50V、>98% full-load efficiency、6kW TDP、10.8kW 400us、60x60x11mm、2.5kW/in3；800V to 12V、8mm、130x40mm、98.2% peak、97.1% full load。URL: https://www.infineon.com/market-news/2026/infpss202603-067

8. Infineon: “XDPP1188-200C for custom HV/MV IBC designs up to 800 VDC”，2026-03-17，可信度高。关键信息：48V to 12V/lower、+/-400V or 800VDC to 48/24/12V、fast transient、bidirectional configuration、samples/volume timing。URL: https://www.infineon.com/market-news/2026/infpss202603-068

9. Infineon: “AI data center voltage regulation portfolio”，2026-03-17，可信度高。关键信息：XDPE1E 3/4-loop PWM controllers、PMBus/AVSBus/SVID/SVI3、TDA49720/12/06 6A/12A/20A PoL、3x3mm/3x3.5mm、-40C to 150C。URL: https://www.infineon.com/market-news/2026/infpss202603-070

10. Infineon: “TLVR quad-phase module exceeding 2 A/mm2”，2026-03-26，可信度高。关键信息：TDM24745T、9x10x5mm、4 power stages、TLVR inductor、decoupling capacitors、320A peak、output capacitance reduction up to 50%。URL: https://www.infineon.com/market-news/2026/infpss202603-076

11. Infineon AI power modules portfolio page，检索日期 2026-06-10，可信度高。关键信息：TDM2454xx 280A、10x9x5mm、>2A/mm2；TDM2354x 160A、8x8x4/5mm、>1.5A/mm2。URL: https://www.infineon.com/technology/ai/we-power-ai/vrm

12. Navitas: “Navitas to Exhibit Breakthrough Solutions ... at APEC 2026”，2026-02-26，可信度高。关键信息：10kW 800V-to-50V GaN full-brick、98.5% peak efficiency、2.1kW/in3、12kW AI data center PSU、8.5kW OCP、4.5kW CRPS、SiCPAK 2300V/3300V、13.8-34.5kVAC to 800/1500VDC。URL: https://navitassemi.com/navitas-to-exhibit-breakthrough-solutions-for-ai-data-center-grid-and-energy-infrastructure-performance-computing-and-industrial-electrification-at-apec-2026/

13. Power Integrations investor release: “1250 V and 1700 V PowiGaN Technology for Next-Generation 800 VDC AI Data Centers”，2025-10-13，可信度高。关键信息：与 NVIDIA 合作、1250V/1700V PowiGaN、>98% requirement、1700V InnoMux2-EP supports 1000VDC input、>90.3% 12V system efficiency、175 million GaN switches in use。URL: https://investors.power.com/news/news-details/2025/Power-Integrations-Details-1250-V-and-1700-V-PowiGaN-Technology-for-Next-Generation-800-VDC-AI-Data-Centers/default.aspx

14. Empower Semiconductor APEC 2026 press release，2026-03-10，可信度中高。关键信息：Crescendo VPD、multi-kilowatt AI/HPC processors、real customer implementations、Crescendo HD target 5A/mm2、silicon capacitor technology。URL: https://www.empowersemi.com/empower-semiconductor-showcases-vertical-power-delivery-innovations-at-apec-2026/

15. Power Integrations AI data center product page，检索日期 2026-06-10，可信度高。关键信息：1250V/1700V PowiGaN、800V to 12V、33% reduction in energy loss claim、volume production claim。URL: https://www.power.com/ai-data-center

### 技术材料和会后评论

16. Advanced Energy: “Key Takeaways from APEC 2026”，2026-04-23，来源类型为参展/行业从业者会后总结，可信度中高。关键信息：AI power sessions 满场、VPD 成焦点、bidirectional GaN 受关注、48V to 800V、1MW racks、energy storage。URL: https://www.advancedenergy.com/en-us/about/news/blog/key-takeaways-from-apec-2026/

17. EDN: “APEC 2026 showcases advances in power electronics”，2026-04，来源类型为媒体二次整理，可信度中。用于交叉验证 Infineon、Renesas、Toshiba 等产品参数，核心结论仍以公司一手材料为准。URL: https://www.edn.com/apec-2026-showcases-advances-in-power-electronics/

18. Power Electronics News: “APEC 2026: The Race to Deliver 800 VDC Power Straight Towards the GPU”，2026-03-27，来源类型为媒体会后报道，可信度中。用于观察会后产业叙事，不单独支撑核心结论。URL: https://www.powerelectronicsnews.com/apec-2026-the-race-to-deliver-800-vdc-power-straight-to-the-gpu/

19. Nexperia APEC exhibitor presentation abstract in APEC Program Book，2026-03，来源类型为会议展商材料，可信度中高。关键信息：AI data center hotswap MOSFET 的 SOA、inrush、board insertion、fault response、thermal stress、package selection。

20. Nyobolt APEC exhibitor presentation abstract in APEC Program Book，2026-03，来源类型为会议展商材料，可信度中。关键信息：GPU chip/input bus BBU、building-scale ESS、front-of-meter MV、AI data center dynamic response。需后续用客户案例验证。

### 市场研究和估算口径

21. MarketsandMarkets: Data Center Power Market，2025-09，可信度中。关键信息：2025 年 351.4 亿美元、2030 年 505.1 亿美元、CAGR 7.5%；本报告用于整体 data center power market 外部锚。URL: https://www.marketsandmarkets.com/Market-Reports/data-center-power-market-262148719.html

22. Yole Group: Power GaN 2025 press release，2025-10，可信度中高。关键信息：power GaN 2024 年 3.55 亿美元、2030 年约 30 亿美元、CAGR 42%；本报告用作 power GaN 外部锚。URL: https://www.yolegroup.com/press-release/from-chargers-to-data-centers-power-gan-market-set-for-rapid-sixfold-expansion-by-2030/

23. Yole Group: Power SiC market press release，2024/2025 公开口径，可信度中高。关键信息：power SiC device market 接近 2029 年 100 亿美元、2023-2029 CAGR 约 24%；本报告用作 SiC 外部锚。URL: https://www.yolegroup.com/press-release/yg-press-news-power-sic-a-10b-market-by-2029-facing-short-term-turbulence/

24. Yole Group Power SiC/GaN Compound Semiconductor Market Monitor Q1-2026 product page，2026-04，可信度中。关键信息：Power SiC 和 GaN 到 2031 年分别约 110 亿美元和 34 亿美元；用于交叉检查长期口径。URL: https://www.yolegroup.com/product/quarterly-monitor/power-sicgan-compound-semiconductor-market-monitor/

### 非官方分享和市场情绪

25. LinkedIn/YouTube 上的 APEC 2026 参会分享、Navitas/Infineon/Power Electronics News 视频采访，来源类型为非官方或半官方营销材料，日期多在 2026-03 至 2026-05，置信度低到中。用途：观察市场情绪、关键词密度和工程师关注点；不作为核心结论单一依据。典型线索包括“APEC 2026 AI power sessions 爆满”“800VDC moving fast”“GaN for data centers is here”。核心判断必须回到公司发布、官方 program 和后续财报验证。
