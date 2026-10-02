# 公司：VSH Vishay Intertechnology, Inc.（威世科技）全面尽调

研究日期：2026-05-10。市场数据截至 2026-05-08 美股收盘。财报口径截至 Vishay 已发布的 2025Q4/FY2025；公司 2026Q1 财报安排在 2026-05-13 发布，因此本文所谓“2026 最新指引”指 2025Q4 财报中给出的 2026Q1 指引，而不是尚未发布的 2026Q1 实绩。

重要口径：Vishay 不披露 AI 数据中心收入、客户项目名、AI 订单金额或单独 AI backlog。本文把“已披露财务数字”和“AI 相关收入推算”分开；AI 推算基于公司公开提到的 AI server 初始出货、AI-related power demand、季度 book-to-bill/backlog、产品组合、项目内 AI 机柜供电产业链资料，以及公开产品资料交叉验证。

## 0. 核心结论

VSH 不是纯 AI 公司，而是全球离散半导体和无源器件的广谱供应商。它在 AI 基建中的真实位置不是 GPU、交换芯片或光模块主价值层，而是在电源、功率转换、保护、感测、磁性元件、薄膜基板这些“每个电源架构都需要、单颗价值低但可靠性要求高”的底层器件层。

截至 2025Q4，AI 相关业务已经从“初始出货”进入“订单拉动可见”阶段：2024Q4 管理层提到 AI server 初始出货；2025Q3 提到 AI-related power requirements；2025Q4 明确说工业和 AI-related power applications 推动收入增长，订单达到三年高点，book-to-bill 达 1.20，backlog 达 13.14 亿美元、4.9 个月。

但它仍有三个限制：第一，AI 收入占比大概率仍小，本文估算 2025 年直接 AI 数据中心收入约 0.8-1.5 亿美元，占公司收入 2.5%-5%；第二，毛利率只有约 19%-20%，说明公司仍处于周期恢复和产能投资消化期，不是高毛利 AI 组件商；第三，当前股价 34.26 美元、forward PE 约 65.4、PS 约 1.52，市场已经给了比传统周期零部件公司更高的复苏/AI 期权定价。

投资判断上，VSH 的关键不是“是不是 AI 概念”，而是三个更具体的问题：

1. 2025Q4 的 1.20 book-to-bill 和三年高订单，是不是能在 2026 年转化为持续发货，而非分销补库。
2. Newport、Itzehoe、Mexico、8 英寸二极管扩产等 capex，能否在 2026-2027 年降低 Newport 拖累并贡献收入。
3. Vishay 的 MOSFET、SiC、IHLP 电感、Power Metal Strip 电流检测电阻、薄膜光模块 submount，能否进入 AI rack PSU、48V/54V 供电、UPS/BESS、800G/1.6T 光模块的客户认证清单。

## 1. 公司整体业务、定位和财务状态

### 1.1 业务结构

Vishay 是全球最大级别的离散半导体和无源电子元件制造商之一。公司把业务分成六个产品板块：

| 板块 | 2025 收入 | 收入占比 | 2025 同比 | 2025 分部经营利润率 | 主要产品 | AI 基建相关性 |
|---|---:|---:|---:|---:|---|---|
| Resistors 电阻 | 7.593 亿美元 | 24.7% | +4.6% | 16.2% | 电流检测、分流器、厚膜/薄膜、电阻网络、热敏/浪涌限制 | 中高：PSU 电流检测、rack power 保护、光模块薄膜平台 |
| MOSFETs | 6.305 亿美元 | 20.5% | +4.7% | -4.8% | 低压 TrenchFET、高压 Super Junction、SiC MOSFET、Power IC | 高：服务器 PSU、48V/54V 供电、UPS/BESS、未来 800VDC |
| Diodes 二极管 | 5.928 亿美元 | 19.3% | +1.9% | 15.1% | 整流器、FRED、TVS、ESD、保护器件、功率模块 | 中高：电源整流、保护、浪涌、数据中心电力链 |
| Capacitors 电容 | 5.056 亿美元 | 16.5% | +10.1% | 16.4% | 钽、薄膜、陶瓷、铝电容、电力电容 | 中：PSU/DC-link/hold-up/UPS/BESS |
| Inductors 电感 | 3.644 亿美元 | 11.9% | +2.3% | 23.3% | IHLP 低剖面大电流电感、定制磁性元件 | 高：高功率 PSU、48V 中间母线、板级 POL |
| Optoelectronic 光电 | 2.166 亿美元 | 7.1% | +2.0% | 10.1% | 光耦、红外、传感器、LED 等 | 低到中；但 2026 年薄膜 submount 切入 800G/1.6T 光模块链 |
| 合计 | 30.690 亿美元 | 100% | +4.5% | 公司 GAAP 经营利润率约 1.9% | 离散半导体 + 无源器件 | AI 暴露是电源和光互连小组件，不是主系统 |

产业链位置：Vishay 位于电子硬件供应链的上游基础器件层，向 OEM、EMS、分销商、汽车 Tier-1、工业、电源、通信、航空航天、军工和医疗客户销售。对于 AI 数据中心，它更可能通过以下链条进入：

Vishay 元件 -> PSU/电源模块/BBU/UPS/光模块供应商 -> ODM/OEM/rack integrator -> hyperscaler 或 AI cloud。

### 1.2 投资人眼中的 VSH

传统视角下，VSH 是一家周期性工业/汽车电子元件公司：产品组合宽、客户分散、现金流长期尚可、有分红，但增长率和毛利率不高。投资人通常把它看成“工业和汽车周期复苏 + 产能周期 + 低估值/分红”的标的。

2025 下半年以后，市场关注点发生变化：公司连续提到 smart grid、AI-related power requirements、AI-related power applications，加上 Q4 订单达到三年高点，AI 电源链期权开始被定价。这个期权真实存在，但目前还没有足够披露证明 VSH 已经拿到大型 AI rack 平台的独家或准独家订单。

### 1.3 最近 3 年重大业务变化

| 时间 | 事件 | 影响 |
|---|---|---|
| 2023 | 新管理层推动 “Vishay 3.0” 战略 | 从传统周期元件公司转向更主动的客户工程、扩产、并购、渠道和 FAE 驱动，目标是提高增长率和资本回报。 |
| 2024 | 收购 Nexperia Newport 200mm 晶圆厂，交易现金约 1.775 亿美元 | 获得英国 Newport 车规 200mm wafer fab，产能超过 3 万片/月。短期拖累毛利率和现金流，长期用于 MOSFET、SiC MOSFET/diode 扩产和能力升级。 |
| 2024 | 收购 Ametherm，净现金约 3148 万美元 | 补强浪涌电流限制器和功率热敏电阻，归入 Resistors；与电源、UPS、工业和汽车电气化相关。 |
| 2024 | 收购 Birkelbach Kondensatortechnik，净现金约 1584 万美元 | 垂直整合电容介质金属化薄膜供应，增强 Capacitors 成本和供应控制。 |
| 2024 | MOSFET goodwill impairment 约 6649 万美元 | 说明 MOSFET 业务过去盈利能力和预期受压，Newport 和新一轮扩产还需要证明回报。 |
| 2025 | Q4 book-to-bill 1.20、半导体 1.27、backlog 4.9 个月 | 周期恢复更清晰；公司称订单达到三年高点，收入受工业和 AI-related power applications 推动。 |
| 2026 | 计划 growth capex 4.00-4.25 亿美元、maintenance capex 1.50-1.75 亿美元 | 继续重投入：Newport 200mm、Itzehoe 300mm MOSFET、Mexico 电感/非线性电阻、8 英寸二极管扩产。 |

### 1.4 最新股价、估值和经营指标

| 指标 | 最新值 | 日期/口径 |
|---|---:|---|
| 股价 | 34.26 美元 | 2026-05-08 收盘 |
| 52 周区间 | 10.35-34.48 美元 | 2026-05-08 |
| 市值 | 46.6 亿美元 | 2026-05-08 |
| 企业价值 EV | 52.2 亿美元 | 2026-05-08 |
| TTM 收入 | 30.69 亿美元 | FY2025/TTM |
| 收入增速 | +4.47% | FY2025 同比 |
| PE | 不适用 | TTM 净亏损 |
| Forward PE | 65.43 | 2026-05-08 数据源估算 |
| PS | 1.52 | 2026-05-08 |
| Forward PS | 1.35 | 2026-05-08 |
| 毛利率 | 19.38% | FY2025/TTM |
| 经营利润率 | 1.85% | FY2025/TTM |
| 净利率 | -0.29% | FY2025/TTM |
| 每股股息 | 0.40 美元 | 年化 |
| 股息率 | 1.17% | 按 2026-05-08 股价 |
| Beta | 1.37 | 5 年月度口径 |

估值解读：股价在过去一年大幅上涨，当前 forward PE 已明显高于传统离散/无源器件周期股常见估值。若 2026 只是普通补库周期，估值偏紧；若 AI 电源链订单持续、毛利率回到 23%-25%、Newport 拖累快速缩小，则估值可由“周期恢复 + AI 电源期权”支撑。

### 1.5 资产负债表健康程度

| 项目 | FY2025 数字 |
|---|---:|
| 现金及等价物 | 5.150 亿美元 |
| 短期投资 | 0.003 亿美元 |
| 应收账款 | 3.818 亿美元 |
| 存货 | 7.592 亿美元 |
| 流动资产 | 18.872 亿美元 |
| 流动负债 | 7.204 亿美元 |
| 流动比率 | 2.62 |
| 总资产 | 42.342 亿美元 |
| 长期债务及一年内到期债务合计 | 9.509 亿美元 |
| 净债务 | 4.357 亿美元 |
| 总权益 | 20.883 亿美元 |
| 经营现金流 | 1.843 亿美元 |
| Capex | 2.733 亿美元 |
| 自由现金流 | 约 -0.890 亿美元 |
| 股息 | 0.542 亿美元 |
| 回购 | 0.125 亿美元 |

判断：短期偿债压力不大，现金和流动资产足够覆盖流动负债，净债务相对权益也不高。但财务质量不是“轻资产高 FCF”型。2025 年自由现金流为负，原因是公司处在扩产/并购后整合期，Newport 仍拖累毛利率，2026 年 capex 计划进一步升至 5.50-6.00 亿美元区间。健康程度可以评为“流动性安全、杠杆可控、但资本开支和利润率修复压力较高”。

## 2. 最新和最近四次财报分析

以下五个季度为最新已发布财报 2025Q4 及前四个季度。

### 2.1 公司层面：收入、订单、backlog、交期和 AI 暴露

| 财报季度 | 发布时间 | 收入 | 环比 | 毛利率 | 经营利润率 | EPS | Book-to-bill | Backlog | 订单/交期/取消率解读 | AI 数据中心收入占比推算 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 2025Q4 | 2026-02-04 | 8.009 亿美元 | +1.3% | 19.6% | 1.8% | GAAP 0.01 美元 | 1.20；半导体 1.27；无源 1.13 | 13.141 亿美元；4.9 个月 | Q4 订单约 9.61 亿美元，达到三年高点。管理层称工业和 AI-related power applications 推动需求。公司仍说要保持 competitive lead times，说明供应紧张上升但未到普遍缺货。 | 约 3%-6%；直接 AI 收入估算 2500-5000 万美元/季 |
| 2025Q3 | 2025-11-05 | 7.906 亿美元 | +3.7% | 19.5% | 2.4% | GAAP -0.06；调整后 0.04 美元 | 0.97；半导体 0.96；无源 0.98 | 11.527 亿美元；4.4 个月 | Q3 收入增长但 B2B 低于 1，可能是前期订单消化或分销补库节奏波动。管理层提到 smart grid、AI-related power、汽车、航空防务。 | 约 2%-5% |
| 2025Q2 | 2025-08-06 | 7.623 亿美元 | +6.6% | 19.5% | 2.9% | GAAP 0.01；调整后 -0.07 美元 | 1.02；半导体 0.98；无源 1.06 | 11.749 亿美元；4.6 个月 | 市场恢复从分销、EMS、各终端扩散；无源订单强于半导体。Newport 拖累毛利率约 160 bps。 | 约 2%-4% |
| 2025Q1 | 2025-05-07 | 7.152 亿美元 | +0.1% | 19.0% | 0.1% | GAAP -0.03 美元 | 1.08；半导体 1.12；无源 1.04 | 11.243 亿美元；4.7 个月 | 管理层称渠道库存大部分正常化；给出 Q2 顺序增长约 6% 的指引。Newport 拖累毛利率约 200 bps。 | 约 1.5%-4% |
| 2024Q4 | 2025-02-05 | 7.147 亿美元 | 未列 | 19.9% | -7.9% | GAAP -0.49；调整后 0.00 美元 | 1.01；半导体 0.99；无源 1.03 | 10.515 亿美元；4.4 个月 | 九个季度后首次 B2B 转正；公司提到 smart grid 订单强、AI servers 初始出货。经营亏损主要受 impairment 和周期低谷影响。 | 约 1%-3% |

Backlog 质量：公司披露 backlog 只包括预计 12 个月内交付的 open orders，但许多订单可被客户取消或重排而不承担显著罚金。因此 13.141 亿美元 backlog 是强信号，但不能等同不可取消订单。正面因素是 Q4 订单三年高、B2B 1.20、半导体 B2B 1.27；风险是分销商补库可能放大短期订单。

### 2.2 分业务季度数据

单位：百万美元。括号内为该季度分部经营利润率。

| 财报季度 | MOSFETs | Diodes | Optoelectronic | Resistors | Inductors | Capacitors | 重点变化 |
|---|---:|---:|---:|---:|---:|---:|---|
| 2025Q4 | 172.6（-0.5%） | 154.2（15.3%） | 55.7（4.5%） | 189.4（14.3%） | 92.6（25.4%） | 136.5（16.6%） | MOSFET +3.3% q/q，Diodes +3.1%，Capacitors +4.5%；半导体订单强于无源。 |
| 2025Q3 | 167.1（-3.8%） | 149.6（15.2%） | 55.6（12.9%） | 195.7（15.3%） | 92.0（26.6%） | 130.6（15.2%） | MOSFET +12.4% q/q；Capacitors +7.8%；Inductors 环比回落但利润率最高。 |
| 2025Q2 | 148.6（-9.7%） | 147.9（15.0%） | 54.1（12.6%） | 194.8（17.9%） | 95.7（24.0%） | 121.1（16.3%） | 全板块环比增长，Inductors +13.7%，Resistors +8.5%。 |
| 2025Q1 | 142.1（-6.1%） | 141.0（15.0%） | 51.2（10.6%） | 179.5（17.4%） | 84.1（16.5%） | 117.4（17.5%） | 渠道库存正常化早期，半导体 B2B 1.12。 |
| 2024Q4 | 146.6（0.8%） | 141.4（16.1%） | 46.9（1.1%） | 177.0（12.7%） | 83.4（25.0%） | 119.3（20.0%） | AI servers 初始出货；Q4 B2B 首次转正。 |

观察：

1. 2025 年增长的质量不完全来自 AI，更多是周期恢复 + 分销/EMS/终端需求改善。真正有 AI 解释力的是 MOSFET Q4 订单弹性、Inductors 高利润率、Capacitors 同比高增、Resistors/Power Metal Strip 的电源链价值。
2. MOSFET 业务仍亏损，是最关键的转型压力点。AI 电源需要 MOSFET/SiC，但 Vishay 必须把 Newport 和 Itzehoe 的产能转成合格出货和毛利率改善。
3. Inductors 是利润率最好的板块之一，2025 分部经营利润率 23.3%，在 AI PSU、48V/54V 中间母线和板级电源里有更好的经济性。

## 3. 2026 指引、收入占比和重点产品

### 3.1 2026 最新指引

公司在 2025Q4 财报中给出的 2026Q1 指引：

| 指标 | 2026Q1 指引 | 解读 |
|---|---:|---|
| 收入 | 8.00-8.30 亿美元 | 中点 8.15 亿美元，较 2025Q1 的 7.152 亿美元同比约 +13.9%，较 2025Q4 环比约 +1.8%。 |
| 毛利率 | 19.9% +/- 50 bps | 比 2025Q4 19.6% 略升。 |
| Newport 拖累 | 50-75 bps | 明显小于 2025Q1 约 200 bps、Q4 约 130 bps，说明 Newport 的利润拖累在下降。 |

这份指引的核心不是毛利率大幅提升，而是“高 backlog + 高 B2B + Newport 拖累下降 + Q1 淡季仍同比双位数增长”。如果 2026Q1 实绩确认订单转收入，市场会继续把它作为 AI 电源链和工业周期复苏标的定价。

### 3.2 终端市场收入占比

按 2025 全年 30.690 亿美元收入估算：

| 终端市场 | 2025 占比 | 估算收入 | 2025 vs 2024 | AI 相关性 |
|---|---:|---:|---:|---|
| Industrial | 44% | 13.50 亿美元 | +4.4% | 高。数据中心电力、smart grid、工业电源、UPS/BESS 多归在这里。 |
| Automotive | 33% | 10.13 亿美元 | +6.5% | 中。电动车、车规 MOSFET/二极管/传感/电容支撑产能认证，但不直接等于 AI。 |
| Other | 12% | 3.68 亿美元 | +6.6% | 中高。公司定义包括 power supplies、consumer、computing、medical；AI server/PSU 最可能部分落在这里。 |
| Aerospace/Defense | 6% | 1.84 亿美元 | -1.4% | 低到中。高可靠元件利润好，但与 AI 数据中心弱相关。 |
| Telecommunications | 5% | 1.53 亿美元 | -1.8% | 中。800G/1.6T 光模块链条可能从 telecom/数据通信恢复受益。 |

### 3.3 重点产品和型号映射

| 业务 | 重点产品/型号/平台 | 官方或公开信号 | 对 AI 数据中心的推断 |
|---|---|---|---|
| MOSFETs | TrenchFET Gen IV/Gen V、SkyFET、PowerPAK、TO-Leadless、TOLL、D2PAK、TO-220/247、Super Junction E/EF/EM/EN 系列、SiC Gen IV 650V/1200V/1700V | Vishay 发布 “SiC & Silicon MOSFETs for AI Applications”资料，明确用途包括 server power、data storage、signal communication、battery management。 | 直接对应 AI server PSU、48V/54V bus、BBU/UPS、电源保护；但竞争激烈，Vishay 不是唯一核心供应商。 |
| Diodes | FRED、TVS/ESD、整流器、保护二极管、功率模块 | Vishay 10-K 称其是 rectifiers 领先供应商之一；2025Q4 半导体 B2B 1.27。 | 电源整流和保护是 AI rack power 的基础 BOM，单价低但设计认证有粘性。 |
| Inductors | IHLP 低剖面大电流电感、屏蔽功率电感、定制磁性元件 | 2026 年仍有高温、高电流 IHLP 新品；公司 2026 capex 包含 Mexico power inductors 扩产。 | AI PSU 和 48V/板级供电需要高电流、低 DCR、低损耗磁性元件；这是 VSH 最值得盯的小而美板块。 |
| Resistors | Power Metal Strip 超低阻电流检测电阻、薄膜/厚膜精密电阻、非线性电阻、Ametherm 浪涌限制/热敏电阻 | Resistors 是最大板块，custom/certified 占比较高；2026 capex 包含 Mexico non-linear resistors。 | 电源电流检测、保护、热管理、浪涌限制在高功率 rack 电源中不可缺；价值量低但验证周期长。 |
| Capacitors | 薄膜、钽、陶瓷、铝电容、电力电容；Birkelbach 金属化薄膜 | Capacitors 2025 同比 +10.1%，为六大板块最高。 | 对 PSU DC-link、hold-up、UPS/BESS、滤波有价值；但竞争比电感/电流检测更商品化。 |
| Thin-film optical submount | Vishay Sfernice 可定制薄膜 submount，AlN/氧化铝，microbumps、conductive epoxy、R/C/L、transmission lines、ground planes；DC 至 70GHz，支持最高 1.6 Tbit/s silicon photonics | 2026-04 官方新品，样品和量产可供，lead time 18 周。 | 小业务但潜在很有意思：如果进入 800G/1.6T 光模块，单件价值不高但增速可能远高于公司平均。 |
| SiC power modules | 1200V/1700V SOT-227 SiC MOSFET 模块，低至 5mΩ/7mΩ，连续电流最高 393A | 2026-02 官方新品，样品和量产可供，lead time 16 周。 | 更偏 EV、工业、UPS、储能和设施电力。对 AI 数据中心是“电力基础设施”暴露，不是 GPU rack 直接 BOM。 |

### 3.4 可以暂时降低权重的产品/业务

以下业务并非无价值，但对 AI 数据中心增量弹性较低，本文不作为重点估值驱动：

| 低权重业务 | 原因 |
|---|---|
| 通用红外、遥控、普通 LED、基础光电传感器 | 归属 Optoelectronic，但与 AI 数据中心功率/光互连主增量关系弱。 |
| 标准 commodity 电阻/电容/二极管 | 竞争充分、议价能力弱，更多跟随电子周期。 |
| 传统消费电子相关元件 | 终端增长弱，且 Vishay 的 AI 叙事不在这里。 |
| 非 AI 汽车 legacy 产品 | 汽车是重要基本盘，但不是本文重点；除非与 SiC、车规 MOSFET、高可靠电容等共享产能认证。 |
| 军工/航空高可靠元件 | 利润率和认证壁垒较好，但增长节奏与 AI rack power 不同步。 |

## 4. 当前高增长/关键业务的收入贡献、增速和供需判断

评分 1-5：5 为最高。收入为本文估算，不是公司披露值。

| 关键业务 | 当前公司总收入基底 | 当前 AI/数据中心相关收入估算 | 当前增速判断 | AI 基建重要性 | 时间紧急性 | 供需紧张度 | 垄断/溢价能力 | 结论 |
|---|---:|---:|---|---:|---:|---:|---:|---|
| Si/SJ/SiC MOSFET + rectifier/diode for AI power | MOSFETs 6.305 亿美元；Diodes 5.928 亿美元 | 4500-9000 万美元/年 | 低基数高增，估计 +30%-80%；总板块 2025 增速仅 +3%-5% | 4.5 | 4.5 | 3.5 | 2.5 | AI rack 电源最直接的 Vishay 半导体入口；但 MOSFET 竞争强、VSH 毛利率尚未证明。 |
| Power inductors / high-current magnetics | Inductors 3.644 亿美元 | 2000-4500 万美元/年 | 估计 +25%-60%；板块 2025 +2.3% 但 Q2/Q3 弹性强 | 4.5 | 4.0 | 4.0 | 3.0 | 48V/54V、5.5kW PSU、33kW shelf 越普及，磁性元件瓶颈越明显。VSH 利润率较好。 |
| Current sense resistors / Power Metal Strip / thermistors | Resistors 7.593 亿美元 | 2500-6000 万美元/年 | 估计 +20%-50%；板块 2025 +4.6% | 3.5 | 3.5 | 3.0 | 3.5 | 电流检测和保护价值量小，但在高功率电源中必须验证；Power Metal Strip 具备一定品牌和可靠性溢价。 |
| Capacitors for PSU/UPS/BESS | Capacitors 5.056 亿美元 | 2000-5000 万美元/年 | 估计 +20%-60%；板块 2025 +10.1% | 3.5 | 3.5 | 3.0 | 2.5 | 电容是 AI 电力链必要件，但替代供应多；Birkelbach 提升薄膜自供。 |
| Thin-film submount for 800G/1.6T optical transceivers | 体量未披露，可能归入 Sfernice/薄膜业务 | 当前小于 500 万美元/年 | 从小基数可高增 | 3.5 | 4.0 | 3.0 | 3.0 | 支持 1.6T silicon photonics 是亮点；需要看是否被光模块大厂认证。 |
| SiC modules for UPS/BESS/smart grid/data center power | SiC 在 MOSFET/模块内未单列 | AI 邻近收入小于 2000 万美元/年 | 低基数高增，但主要不在服务器 rack 内 | 3.5 | 3.0 | 3.0 | 2.5 | 更像设施侧电力期权；Newport 和 MaxPower 技术是长期变量。 |

当前直接 AI 数据中心收入合计估算：约 0.8-1.5 亿美元，占 2025 收入约 2.5%-5%。若把 smart grid、UPS、BESS、数据中心电力基础设施的间接 AI 暴露纳入，广义 AI/AI 电力链收入可估到约 1.5-2.5 亿美元，占比约 5%-8%。

## 5. 一年后收入贡献预测：基准、乐观、极度乐观

预测期：未来 12 个月，大致对应 2026 年收入贡献。以下均为 AI/数据中心相关收入估算，不是各板块总收入。

| 关键业务 | 基准情景 | 乐观情景 | 极度乐观情景 | 情景触发条件 |
|---|---:|---:|---:|---|
| Si/SJ/SiC MOSFET + diode/rectifier | 9000 万-1.50 亿美元；同比 +50%-90%；重要性 4.5；紧张度 3.5；溢价 2.5 | 1.60-2.60 亿美元；同比 +120%-200%；紧张度 4.0 | 3.00-4.50 亿美元；同比 +250%-400%；紧张度 5.0 | 基准：现有 PSU/工业电源订单延续。乐观：进入更多 AI server PSU/rack power BOM。极度乐观：Newport/Itzehoe 认证加速并拿到多个大平台。 |
| Power inductors / magnetics | 5500 万-9000 万美元；同比 +60%-100%；重要性 4.5；紧张度 4.0；溢价 3.0 | 1.00-1.80 亿美元；同比 +150%-300%；紧张度 4.5 | 2.00-3.20 亿美元；同比 +350%-600%；紧张度 5.0 | 取决于 33kW shelf、5.5kW PSU、48V/54V 中间母线订单和 Mexico 扩产。 |
| Current sense / Power Metal Strip / thermistors | 6000 万-1.00 亿美元；同比 +40%-80%；重要性 3.5；紧张度 3.5；溢价 3.5 | 1.10-1.70 亿美元；同比 +100%-220%；紧张度 4.0 | 1.80-2.50 亿美元；同比 +250%-400%；紧张度 4.5 | 需要高功率电源客户把 Vishay current sense/shunt 作为合格件，且 Ametherm/非线性电阻进入更多保护位点。 |
| Capacitors for PSU/UPS/BESS | 5500 万-9000 万美元；同比 +50%-100%；重要性 3.5；紧张度 3.5；溢价 2.5 | 1.00-1.60 亿美元；同比 +150%-250%；紧张度 4.0 | 1.80-2.60 亿美元；同比 +300%-500%；紧张度 4.5 | 取决于 UPS/BESS/BBU、PSU hold-up、薄膜电容和电力电容订单。 |
| Thin-film optical submount | 500 万-1500 万美元；同比高增；重要性 3.5；紧张度 3.0；溢价 3.0 | 2000 万-5000 万美元；重要性 4.0；紧张度 4.0 | 7000 万-1.20 亿美元；重要性 4.5；紧张度 5.0 | 需要 800G/1.6T 光模块客户设计定点。极度乐观要求多个头部 transceiver/silicon photonics 平台采用。 |
| SiC modules / data center power infrastructure | 2000 万-4000 万美元；重要性 3.5；紧张度 3.0；溢价 2.5 | 5000 万-1.00 亿美元；重要性 4.0；紧张度 4.0 | 1.20-2.00 亿美元；重要性 4.5；紧张度 4.5 | 取决于 UPS/BESS、on-site power、800VDC 前期系统试点，而不只取决于 GPU rack。 |

汇总预测：

| 情景 | 未来 12 个月直接 AI/数据中心相关收入 | 占公司收入估算 | 公司总收入推算 | 核心含义 |
|---|---:|---:|---:|---|
| 基准 | 1.7-3.0 亿美元 | 5%-9% | 33.5-35.0 亿美元；同比 +9%-14% | AI 是增量亮点，但公司仍主要是工业/汽车周期恢复。 |
| 乐观 | 3.5-6.0 亿美元 | 10%-16% | 36.5-38.5 亿美元；同比 +19%-25% | AI power 从“点状订单”变成多产品线共同拉动。 |
| 极度乐观 | 7.0-11.0 亿美元 | 17%-25% | 40.5-43.5 亿美元；同比 +32%-42% | 需要大客户平台化采用、产能认证顺利、Newport/Itzehoe/Mexico 扩产快速兑现；概率低但上行空间大。 |

## 6. BOM 拆分、单位内容量、价格传导、当前产能和认证

项目内 AI 机柜供电资料显示，2026 年高功率 AI rack 供电大概率以 480/415VAC 到 rack power shelf，再到 48V/50V/54V DC bus，再到计算托盘/板级 12V、6V、core conversion 为主；800VDC 在 2026 年进入设计和早期生态，收入确认更偏 2027。33kW ORv3 power shelf 的 BOM 中，功率半导体/控制/驱动/保护约占 25%-35%，磁性元件约 15%-25%，电容约 8%-15%。

单位假设：参考 GB300/NVL72 级别高功率机柜，单 rack 峰值约 100-142kW，本文用 142kW/72 GPU 做上限估算；1MW IT 约 7 个此类 rack。光互连按每 rack 100-150 个 800G 等效外部光口、每 MW 700-1100 个 800G 等效光口估算。真实内容量会随 OEM PSU 方案、供电架构、是否 800VDC、是否使用集成 power module 大幅变化。

| 产品/业务 | BOM 位置 | Vishay 可能内容量 | 价格传导链 | 当前产能能力推算 | 当前采用/认证阶段 |
|---|---|---:|---|---:|---|
| MOSFET/SiC/Diode/Rectifier | AC-DC、DC-DC、PFC、同步整流、保护、BBU/UPS | 每 33kW shelf 50-250 美元；每 rack 400-2000 美元；每 MW 2800-14000 美元；每 GPU 6-28 美元。若 SiC/高压方案占比提高，单 rack 可上行至 3000-6000 美元。 | Vishay -> PSU/power shelf 厂商 -> ODM/OEM/rack integrator -> cloud。功率半导体涨价可通过 PSU 传导，因其占整 rack 成本低但故障风险高。 | AI 可分配年化出货能力约 8000 万-1.5 亿美元；公司整体 Q4 年化收入约 32 亿美元，Newport 长期 wafer 产能超过 3 万片/月但仍在爬坡。 | 客户级 BOM/design-in；未看到公开 NVIDIA/GB300 直接认证。Newport/Itzehoe 需要车规/工业/电源客户 qualification。 |
| Power inductors / magnetics | PFC/LLC/多相电源、48V 中间母线、板级 POL、滤波 | 每 33kW shelf 40-180 美元；每 rack 320-1440 美元；每 MW 2200-10000 美元；每 GPU 4-20 美元。 | Vishay -> PSU/VRM/board vendor -> server/rack OEM -> cloud。磁性元件若成为交期瓶颈，议价优于普通被动件。 | AI 适用年化能力约 6000 万-1.2 亿美元；Mexico power inductors 扩产是关键。 | 主要是 PSU/ODM 平台认证；高温、低 DCR、高电流型号需随电源拓扑验证。 |
| Current sense / shunt / thermistor | 电流检测、过流保护、浪涌限制、温度补偿、保护网络 | 每 33kW shelf 15-75 美元；每 rack 120-600 美元；每 MW 800-4200 美元；每 GPU 2-8 美元。 | Vishay -> PSU/保护板/EMS -> rack OEM。可靠性验证后替换成本高于普通电阻。 | AI 适用年化能力约 8000 万-1.5 亿美元；Resistors 总收入基底最大。 | Power Metal Strip/热敏/浪涌限制多为客户 BOM 认证；Ametherm 加强 inrush limiting 产品。 |
| Capacitors | DC-link、hold-up、滤波、snubber、UPS/BBU 储能接口 | 每 33kW shelf 25-150 美元；每 rack 200-1200 美元；每 MW 1400-8400 美元；每 GPU 3-17 美元。 | Vishay -> PSU/UPS/BBU/EMS -> data center/rack。薄膜和电力电容涨价可部分传导。 | AI 适用年化能力约 7000 万-1.4 亿美元；Birkelbach 提升薄膜介质自供。 | PSU/UPS 供应商 qualification；电容寿命、温升、纹波电流是核心。 |
| Thin-film optical submount | 800G/1.6T silicon photonics 光模块内的基板/传输线/无源集成 | 每 optical port 0.5-5 美元；每 rack 50-750 美元；每 MW 350-5500 美元。 | Vishay -> 光模块/硅光封装厂 -> 交换机/AI cluster 网络。若进入定制封装，价格弹性好。 | 当前年化能力可能 500 万-2000 万美元；官方 lead time 18 周。 | 官方称 samples 和 production quantities available。需要光模块厂商设计认证，未见公开大客户定点。 |
| SiC modules / facilities power | UPS、BESS、on-site power、工业电源、未来 800VDC 配电 | 设施侧每 MW 5000-30000 美元 Vishay 内容量；rack 内直接内容量目前不高。 | Vishay -> UPS/BESS/电力设备厂 -> 数据中心电力 EPC/cloud。 | AI 邻近年化能力约 2000 万-6000 万美元；官方 SiC module lead time 16 周。 | 更多处于工业/UPS/能源客户认证，不等于 AI rack 平台认证。 |

## 7. 一年后产能能力、供应链采纳和认证阶段预测

以下为 AI/数据中心相关可服务收入能力估算。

| 产品/业务 | 基准：一年后产能与认证 | 乐观：一年后产能与认证 | 极度乐观：一年后产能与认证 |
|---|---|---|---|
| MOSFET/SiC/Diode/Rectifier | 1.5-2.5 亿美元年化 AI 可服务能力；进入若干 PSU/工业电源客户扩量；Newport 拖累继续下降。 | 3.0-5.0 亿美元；多个 AI PSU/rack power 客户设计定点，半导体 B2B 持续高于 1.1。 | 6.0-9.0 亿美元；Newport/Itzehoe 认证速度超预期，进入头部 AI rack 平台多供应商清单。 |
| Power inductors / magnetics | 1.0-1.8 亿美元；Mexico 扩产释放，主力是高功率 PSU 和 48V 电源。 | 2.0-3.5 亿美元；大客户将 IHLP/定制磁性件用于多个 rack power BOM。 | 4.0-6.0 亿美元；磁性元件成为 AI 电源瓶颈，Vishay 获得高优先级配额和价格。 |
| Current sense / thermistor | 1.2-2.0 亿美元；Power Metal Strip 和 Ametherm 进入更多电源保护位点。 | 2.2-3.5 亿美元；高可靠 shunt/浪涌限制跨 PSU、BBU、UPS 扩散。 | 4.0-5.5 亿美元；客户在高功率平台上倾向认证后锁定，替换成本显著提高。 |
| Capacitors | 1.2-2.2 亿美元；薄膜和电力电容与 PSU/UPS 需求同步成长。 | 2.5-4.0 亿美元；BESS/BBU 与 high-power shelf 双拉动。 | 4.5-6.5 亿美元；电容供应链再度紧张，Vishay 获得溢价和长单。 |
| Thin-film optical submount | 1500 万-4000 万美元；完成 1-2 家模块客户验证并小批量。 | 5000 万-1.2 亿美元；进入若干 800G/1.6T 模块平台量产。 | 1.5-2.5 亿美元；成为 1.6T silicon photonics 定制 submount 的重要供应商之一。 |
| SiC modules / facilities power | 5000 万-1.0 亿美元；UPS/BESS/工业客户小规模增长。 | 1.2-2.5 亿美元；AI data center power infrastructure 项目采用增加。 | 3.0-4.5 亿美元；800VDC/高压数据中心电力方案提前放量。 |

认证判断：目前没有公开证据表明 Vishay 某个 AI 产品已经获得 NVIDIA GB300/NVL72 级别平台“点名认证”。更现实的路径是通过 PSU、电源模块、ODM、EMS、光模块厂商的 BOM 认证间接进入平台。对于 Vishay 这类器件商，客户认证比公开营销更重要，也更难被外部验证。

## 8. 根据订单积压和供给推断未来一年业务增速

### 8.1 已知订单信号

| 信号 | 数字 | 含义 |
|---|---:|---|
| 2025Q4 收入 | 8.009 亿美元 | 年化约 32.04 亿美元。 |
| 2025Q4 book-to-bill | 1.20 | Q4 订单粗算约 9.61 亿美元。 |
| 2025Q4 半导体 book-to-bill | 1.27 | 半导体订单强于无源；MOSFET/Diodes/Opto Q4 收入合计约 3.825 亿美元，订单粗算约 4.86 亿美元。 |
| 2025Q4 无源 book-to-bill | 1.13 | 无源 Q4 收入合计约 4.184 亿美元，订单粗算约 4.73 亿美元。 |
| Backlog | 13.141 亿美元 | 同比 2024Q4 的 10.515 亿美元约 +25%；覆盖 Q4 年化收入约 41%。 |
| Backlog 月数 | 4.9 个月 | 高于 2025Q3 的 4.4 个月。 |
| 2026Q1 指引中点 | 8.15 亿美元 | 同比 2025Q1 约 +13.9%。 |

### 8.2 未来一年增速情景

| 情景 | 公司总收入增速 | AI/数据中心相关收入增速 | 供给约束 | 取消率/订单风险 | 判断 |
|---|---:|---:|---|---|---|
| 基准 | +9%-14%，收入 33.5-35.0 亿美元 | +60%-120%，收入 1.7-3.0 亿美元 | 可控；主要靠现有产线、Newport 拖累下降、Mexico 小幅释放 | 中等。分销补库可能回落，但 backlog 仍能支撑上半年 | 最可能。VSH 是复苏周期 + AI 电源小比例放量。 |
| 乐观 | +19%-25%，收入 36.5-38.5 亿美元 | +180%-350%，收入 3.5-6.0 亿美元 | MOSFET、磁性元件、电容、认证工程资源开始紧 | 中低。真实终端项目拉动大于渠道库存波动 | 需要 Q1/Q2 连续 B2B >1.05、backlog 维持 5 个月附近、毛利率上行。 |
| 极度乐观 | +32%-42%，收入 40.5-43.5 亿美元 | +500% 以上，收入 7.0-11.0 亿美元 | 高。Newport/Itzehoe/Mexico 产能、客户 qualification、测试封装成为瓶颈 | 中。若客户 double ordering 或平台延期，回撤大 | 概率低。需要 AI rack PSU 和 1.6T 光模块等多个产品线同时拿到大平台订单。 |

最重要的验证指标：

1. 2026Q1 实绩是否超过 8.15 亿美元中点，以及 Q2 指引是否继续环比增长。
2. Book-to-bill 是否连续高于 1.05，尤其半导体是否持续高于无源。
3. Backlog 是否维持或超过 5 个月，同时管理层是否仍说 lead times competitive；如果 backlog 升但 lead time 不拉长，说明扩产有效。
4. Newport 拖累是否从 50-75 bps 继续下降；若下降慢，AI 电源上行会被毛利吞掉。
5. 公司是否首次披露 AI server、power shelf、48V、800VDC、1.6T optical transceiver 相关设计定点或客户类别。

## 9. 竞争格局、技术主流性、替代风险和客户替换成本

### 9.1 分产品竞争格局

| 产品/业务 | 主要竞争对手 | VSH 优势 | 风险/替代方案 | 客户替换成本 |
|---|---|---|---|---|
| MOSFET/SiC/Diode | Infineon、onsemi、STMicroelectronics、Nexperia、Renesas、Toshiba、ROHM、Diodes Inc.；在 AI 电源模块还会遇到 MPS、TI、Vicor、ADI、Navitas、EPC、Power Integrations 等 | 产品线宽、全球制造、Newport 200mm、Itzehoe 300mm、低压到高压/SiC 组合；整流器地位强 | AI 电源价值可能向集成 power module、GaN、SiC 龙头、控制器/驱动集成商集中；VSH MOSFET 利润率仍弱 | 中。标准 MOSFET 可替换，但高功率电源认证、热设计、EMI 和可靠性测试会提高替换成本。 |
| Power inductors / magnetics | TDK/EPCOS、Murata、Yageo、Bourns、Panasonic、Taiyo Yuden、Cyntec、Coilcraft | IHLP 大电流低剖面产品线、较高分部利润率、Mexico 扩产 | ODM/PSU 厂商可多供应商认证；定制磁件可能被内部设计或其他磁性件厂替代 | 中高。若是定制磁件且完成热/损耗/EMI 验证，替换成本明显高。 |
| Current sense / shunt / thermistor | Bourns、KOA、Panasonic、Yageo、Susumu、Isabellenhütte、Viking 等 | Power Metal Strip 品牌、低阻电流检测经验、Ametherm 浪涌限制补强 | 标准电阻竞争激烈；客户可二供；价格压力常在 | 中高。电流检测精度、温漂、可靠性和板级热设计验证后，替换成本高于普通电阻。 |
| Capacitors | Murata、TDK、Kyocera/AVX、Yageo/KEMET、Nichicon、Panasonic、Taiyo Yuden、Rubycon 等 | 产品线全，Birkelbach 薄膜介质垂直整合 | 电容品类更商品化；MLCC/薄膜/铝电容各有强竞争者；供需周期波动大 | 中。高纹波、高寿命、车规/工业认证电容替换成本较高；普通电容较低。 |
| Thin-film optical submount | Kyocera、Coherent/II-VI、Materion、Rogers、各类陶瓷/薄膜/RF 基板和光模块封装供应商 | Vishay Sfernice 薄膜电阻/RF 衰减器工艺，可在 AlN/氧化铝上集成 R/C/L、传输线和 microbumps | 光模块客户可能采用自研基板、硅光封装厂内部方案或其他陶瓷/玻璃/有机基板 | 高。若进入 1.6T optical engine 设计，RF/热/贴装/可靠性验证复杂，替换成本较高。 |
| SiC modules / facilities power | Infineon、Wolfspeed、ROHM、onsemi、ST、Mitsubishi Electric、Semikron Danfoss 等 | Vishay 有 SiC MOSFET/模块产品和 Newport 长期潜力 | SiC 主流玩家强；UPS/BESS 也可能使用 IGBT、SiC 混合或 GaN；数据中心 800VDC 推进节奏不确定 | 中。设施级电力设备认证周期长，但供应商多。 |

### 9.2 新技术是否是主流

AI rack 的供电方向正在从传统服务器电源向更高功率密度、更高电压、更强瞬态管理演进。项目内行业资料指出，2026 年主流收入更可能在 480/415VAC 到 rack power shelf、48V/50V/54V bus、板级 12V/6V/core conversion；800VDC 更像 2026 设计锁定、2027 以后收入加速的方向。VSH 的 Si/SJ MOSFET、SiC、二极管、电感、电阻、电容都位于这个迁移的基础 BOM 中。

但是主流不等于垄断。真正溢价最高的可能是集成电源模块、控制器、数字电源管理、先进封装、液冷/电力系统集成，而 Vishay 更多是“关键但可多供应”的元件。因此 VSH 的最佳投资叙事不是单个产品颠覆，而是多条基础器件同时随 AI power TAM 扩张，并通过认证和供给可靠性获取份额。

### 9.3 最大风险

| 风险 | 影响 |
|---|---|
| AI 收入披露不足 | 市场可能把“AI-related power”过度外推，实际占比若只有低个位数，估值容易回落。 |
| 毛利率修复慢 | 19%-20% 毛利率无法支撑高估值；Newport 若继续拖累，AI 增量也未必转利润。 |
| Capex 高、FCF 为负 | 2026 capex 5.50-6.00 亿美元会继续压制自由现金流。 |
| 标准件竞争和价格压力 | 低端 MOSFET、二极管、电容、电阻仍会受周期和价格竞争影响。 |
| 客户平台不透明 | 没有公开客户项目、订单金额和交付窗口，外部只能通过 B2B/backlog/管理层语言推断。 |
| 替代技术 | GaN、SiC 龙头、集成 power module、800VDC 架构变化、PSU 内部设计变化，都可能降低 VSH 单位内容量。 |
| 分销补库误判 | B2B 和 backlog 的一部分可能来自渠道补库，若终端需求不跟上，后续订单会回落。 |

## 10. 需要继续跟踪的催化剂清单

| 时间/事件 | 应看什么 |
|---|---|
| 2026-05-13 2026Q1 财报 | 收入是否高于 8.15 亿美元中点；Q2 指引；book-to-bill；backlog 月数；Newport 拖累；是否新增 AI power 语言。 |
| 2026 年后续季度 | 半导体 B2B 是否持续高于 1；MOSFET 分部是否从亏损转正；Inductors/Capacitors 是否继续高毛利增长。 |
| Product news | 是否出现 AI server PSU、48V/54V、800VDC、1.6T optical transceiver 客户/应用的明确产品认证。 |
| Capex update | Newport/Itzehoe/Mexico/8 英寸二极管扩产是否按计划；2027 capex 是否下降。 |
| 竞争对手财报 | Infineon、onsemi、ST、ROHM、MPS、TDK、Murata、Yageo 等是否提到 AI power passives/semis 供需紧张。 |

## 11. 资料来源

公开来源：

1. Vishay FY2025 Form 10-K，SEC：<https://www.sec.gov/Archives/edgar/data/103730/000010373026000019/form10k.htm>
2. Vishay 2025Q4 earnings release，SEC Exhibit 99.1：<https://www.sec.gov/Archives/edgar/data/103730/000010373026000008/exhibit99-1.htm>
3. Vishay 2025Q3 earnings release，SEC Exhibit 99.1：<https://www.sec.gov/Archives/edgar/data/103730/000010373025000066/exhibit99-1.htm>
4. Vishay 2025Q2 earnings release，SEC Exhibit 99.1：<https://www.sec.gov/Archives/edgar/data/103730/000010373025000053/exhibit99-1.htm>
5. Vishay 2025Q1 earnings release，SEC Exhibit 99.1：<https://www.sec.gov/Archives/edgar/data/103730/000010373025000035/exhibit99-1.htm>
6. Vishay 2024Q4 earnings release，SEC Exhibit 99.1：<https://www.sec.gov/Archives/edgar/data/103730/000010373025000006/exhibit99-1.htm>
7. Vishay 2025Q4 investor presentation：<https://ir.vishay.com/static-files/f76b9dec-ed92-40b6-a2fa-6f235567b497>
8. Vishay quarterly results IR page：<https://ir.vishay.com/financial-information/quarterly-results>
9. StockAnalysis VSH quote/statistics：<https://stockanalysis.com/stocks/vsh/>
10. StockAnalysis VSH financial ratios：<https://stockanalysis.com/stocks/vsh/financials/ratios/>
11. Vishay SiC & Silicon MOSFETs for AI Applications PDF：<https://www.vishay.com/docs/47011/ai-mosfets.pdf>
12. Vishay 1.6 Tbit/s silicon photonics thin-film submount press release：<https://www.vishay.com/en/company/press/releases/2026/Submount-STF/>
13. Vishay SiC MOSFET modules press release：<https://www.vishay.com/en/company/press/releases/2026/VS-SF50LA120-et-al/>

项目内行业资料（未使用“公司调研”目录）：

1. `行业调研_AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026.md`
2. `行业调研/AI头部芯片市场占比和规模.md`
3. `行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`


