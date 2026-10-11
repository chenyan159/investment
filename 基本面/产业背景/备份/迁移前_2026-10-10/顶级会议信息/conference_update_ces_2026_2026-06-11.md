# CES 2026会议追踪：核心变化、产品爆发和市场预期差

> 会议对象：CES 2026  
> 会议日期：2026-01-06 至 2026-01-09  
> 会议地点：Las Vegas, Nevada, USA  
> 材料检索截止日期：2026-06-11（系统日期口径；本机 America/Los_Angeles 执行时为 2026-06-10 晚间）  
> 报告完成日期：2026-06-11  
> 写作边界：本报告为独立会议追踪，未读取、引用或继承项目内既有公司调研、行业调研、日度资料、特征量化、tmp、data、缓存或旧报告。

## 结论摘要

1. CES 2026最大的真实变化不是“更多消费电子加 AI”，而是“AI 从软件功能变成物理世界操作系统”。一手证据包括：CES 官方把 robotics 定义为 physical AI；NVIDIA 发布 Alpamayo 开源 reasoning VLA 自动驾驶模型；Siemens 和 NVIDIA 把 Digital Twin Composer、Omniverse、EDA、仿真、工厂自动化合并成 Industrial AI Operating System；Bosch 把 AI cockpit、by-wire、Radar Gen 7、Manufacturing Co-Intelligence 放在同一套软硬件叙事里。

2. 最值得跟踪的产业链不是展会上最热闹的消费机器人，而是有客户验证的工业数字孪生、自动驾驶数据工厂、机器人执行器和安全冗余硬件。Siemens 披露 PepsiCo 初始部署实现吞吐量提升 20%、识别最高 90% 潜在问题、Capex 下降 10%-15%；Boston Dynamics Atlas 2026 年部署已排满，但 Hyundai 正式工厂部署节奏指向 2028 年和 2030 年，不是 2026 年立即大规模收入化。

3. AI PC 是最大“话题热度和商业兑现不匹配”的方向。AMD 在 CES 发布 Ryzen AI 400/PRO 400，NPU 最高 60 TOPS，首批系统 2026-01 出货、Q1 扩大 OEM 供给；但 IDC 2026 年 PC 出货预测被内存短缺显著下修，PC 市场价值靠 ASP 上升支撑。投资上，AI PC 对 CPU/NPU、DRAM、SSD、散热、电池的成本拉动比对 OEM 利润更确定。

4. 自动驾驶从“单车智能炫技”转向“reasoning model + simulation + safety case + production-grade redundancy”。NVIDIA Alpamayo 的关键不是 10B 参数本身，而是开源 teacher model、AlpaSim、1,700+ 小时开放驾驶数据和 Halos 安全体系；Bosch 和 Kodiak 的重点也不是 demo 卡车，而是车规级冗余硬件、传感器、转向/制动执行组件和可量产供应链。

5. Humanoid robot 的短期爆发要按“工业试点转正式工位”看，而不是按家庭机器人叙事看。Atlas 的规格已经进入可评估阶段：56 DoF、50 kg 举升、-20 至 40 摄氏度工作、自动换电、MES/WMS 接入；但 2026 年更像 RMAC/Google DeepMind 等早期部署和任务学习验证，真正的收入放量窗口是 2028 年 Hyundai Metaplant America、2030 年部件装配扩展。

6. Smart glasses、smart rings 和 health wearables 是小基数高增速，但利润池更偏传感器、算法、订阅、医疗认证和生态入口。CES 官方称智能眼镜已加入生成式 AI 语音、实时翻译、录制和 QR 支付；IDC 披露 2025 年全球可穿戴出货 6.115 亿台；二手市场研究给 2026 年 smart glasses 约 31.6 亿美元、smart rings 约 5.2 亿美元。设备很小，数据和订阅更值钱。

7. 反共识：CES 2026 对 EV 整车本身偏冷，对 robotaxi、AI cockpit、by-wire、SDV、工业机器人偏热。这会削弱“所有车企都是 CES 直接受益者”的简单逻辑，强化 Qualcomm、NVIDIA、Bosch、Siemens、传感器、执行器、测试认证、仿真软件、车规安全平台的相对弹性。

8. 需要下修的条件很清晰：到 2026-Q3/Q4 若 Siemens Digital Twin Composer 没有更多具名客户、AMD Helios/MI400 没有明确云厂商或 OEM 订单、Atlas 没有公布稳定工位指标、Alpamayo 没有进入实际车队验证、AI PC 没有看到本地 agent 使用时长提升，则本届 CES 的“physical AI 已进入商业化”判断必须从加速期调回验证期。

## 会议重点和方向变化

### 会议规模与主题强度

| 指标 | 公开数字 | 日期 | 投资含义 |
|---|---:|---|---|
| 参会人数 | 148,392，较上年增长 4% | CES 官方审计，2026-03-31 | 展会恢复为大型 B2B 交易和融资场，不能只按消费电子发布会理解。 |
| 国际参会者 | 55,841，来自 141 个国家/地区，占 37.6% | 2026-03-31 | 全球供应链、渠道、政府和客户在同一场集中校准 2026 预算。 |
| 展商 | 4,100+，2.6M+ net sq ft；Eureka Park 约 1,200 家 startup | 2026-03-31 | 小公司线索很多，但必须回到客户验证和订单。 |
| Fortune 500 覆盖 | 307 家 2025 Fortune 500 公司参会 | 2026-03-31 | CES 2026 不是单纯媒体曝光，具备采购、合作和投融资场景。 |
| 媒体/内容创作者/分析师 | 7,037 | 2026-03-31 | 非官方内容多、噪声也大，适合做线索，不适合单独支撑核心判断。 |
| 高管比例 | senior-level executives 占 52% | 2026-03-31 | 供应商发布与客户预算周期同步，订单线索优先级高。 |
| AI 关注 | 39,929 名参会者，+22% YoY | 2026-03-31 | AI 已经横跨 PC、车、工业、健康、广告、家居和机器人。 |
| Robotics 关注 | 19,605 名参会者，+26% YoY | 2026-03-31 | physical AI 是 CES 2026 最明显增量主题。 |
| Innovation Awards 投稿变化 | AI +29%、robotics +32%、drones +32%；总投稿 3,600+ | CTA，2025-11/2026 会前 | 展会前置指标已显示硬件化 AI 需求上升。 |

### 主题 1：AI 从“功能”变成“物理世界操作系统”

CES 2026 会前议程已经把 AI agents、digital twins、on-device AI 作为核心趋势；会后材料则把这个主题从消费端扩展到工业端。核心变化是：AI 不再只放在应用层，而是被嵌入数据采集、仿真、控制、执行、验证和售后服务。

| 证据 | 公司/机构 | 参数和日期 | 变化性质 | 置信度 |
|---|---|---|---|---|
| AMD Helios rack-scale platform、MI440X、MI500 预告、Ryzen AI 400 | AMD | 2026-01-05；Helios 单 rack 最高约 3 AI exaflops；Ryzen AI 400 NPU 最高 60 TOPS；AI Halo Q2 2026 | AI 基础设施和端侧 AI 同台发布，AMD 从芯片供应商向系统方案叙事推进 | 高，一手公司材料 |
| Alpamayo 1、AlpaSim、Physical AI datasets | NVIDIA | 2026-01；10B 参数 VLA；1,700+ 小时开放驾驶数据；teacher model 可蒸馏 | L4 自动驾驶开始把 reasoning、仿真和安全验证打包 | 高，一手公司材料 |
| Digital Twin Composer、Industrial AI Operating System | Siemens/NVIDIA | 2026-01-06；Digital Twin Composer 2026 年中上 Siemens Xcelerator Marketplace；PepsiCo 初始部署 +20% throughput | 工业 AI 从 dashboard/仿真升级为连续优化和操作闭环 | 高，一手公司材料 |
| AI cockpit、Radar Gen 7、by-wire、Manufacturing Co-Intelligence | Bosch | 2026-01-05；Radar Gen 7 对小物体探测距离超 200 米；by-wire 累计收入目标至 2032 年超 70 亿欧元 | 车端 AI 与安全执行硬件绑定，而不是只做语音助手 | 高，一手公司材料 |

投资判断：2026 年更确定的利润池在硬件化 AI 的“底座”和“闭环”：GPU/ASIC、HBM、先进封装、网络、液冷、电源、传感器、执行器、仿真软件、PLM/MES 数据层、安全认证。纯应用 UI、概念产品和单次 demo 的持续利润率不确定。

### 主题 2：Robotics 进入 physical AI 叙事，但商业化节奏分化

CES 官方会后材料直接把 robotics 描述为 physical AI，并强调 analytical AI 和 generative AI simulation-based training。展商包括 Hyundai、Primech AI、Richtech Robotics、Sharpa、Tuya、Yarbo、Unitree；Innovation Awards 中 Doosan Robotics/Maple Advanced Robotics 的 Scan&Go 拿到 AI 类 Best of Innovation。

最关键一手进展是 Boston Dynamics Atlas：

| 项目 | Atlas 公开信息 | 投资解读 |
|---|---|---|
| 商业阶段 | 2026 年部署已排满，面向 Hyundai RMAC 和 Google DeepMind；更多客户计划 2027 | 不是概念机，但仍处早期客户验证期。 |
| 目标任务 | material handling、order fulfillment、parts sequencing，之后扩展到 component assembly | 首批场景是物流/搬运/排序，不是全能装配。 |
| 硬件参数 | 56 DoF；举升 50 kg；reach 2.3 m；-20 至 40 摄氏度；water-resistant；自动换电 | 参数足以进入工业 ROI 测算，但可靠性/节拍/维护成本仍缺披露。 |
| 系统集成 | 可通过 Orbit 接入 MES、WMS；任务可复制到 fleet | 真正价值在 fleet software 和工厂系统集成。 |
| Hyundai 节奏 | Hyundai 公开材料指向 2028 年在 HMGMA 部署，2030 年扩展至部件装配 | 2026 年不是量产收入年，2028/2030 是关键拐点。 |
| 供应链 | Hyundai Mobis 提供 Atlas 执行器；Hyundai 规划美国机器人产能 | 执行器、减速器、传感器、电池、控制器、整机集成是瓶颈。 |

结论：CES 2026 的机器人主线不是“家务机器人马上普及”，而是工业客户开始愿意给 humanoid 和 AMR 留试点预算。受益顺序更可能是执行器/运动控制/安全传感器/fleet orchestration/工厂集成，其次才是整机品牌。

### 主题 3：自动驾驶和车载 AI 从 EV 热度切换到 robotaxi、SDV 和冗余硬件

多家媒体会后观察称 CES 2026 的汽车焦点从 EV 新车转向 AI、robotaxi 和软件定义汽车。该观察有一手材料支撑：

| 方向 | CES 2026 证据 | 变化 |
|---|---|---|
| Reasoning-based autonomy | NVIDIA Alpamayo 1：10B 参数、VLA、video input、trajectory + reasoning trace、1,700+ 小时数据、AlpaSim | 自动驾驶从感知规划模块组合，转向 end-to-end + 可解释 reasoning + teacher distillation。 |
| 车规级量产硬件 | Bosch-Kodiak：Bosch 提供传感器、转向等车辆执行组件，双方做 production-grade redundant platform | 自动驾驶投资不只看算法，冗余硬件、供应链和 upfit/factory-line integration 更重要。 |
| 高阶 ADAS 量产 | Qualcomm/BMW Snapdragon Ride Pilot：BMW iX3 首发，支持 L2+ highway/urban NOA，已验证 60+ 国家，2026 年目标拓至 100+ 国家 | L2+/NOA 全球化比 L4 robotaxi 更快收入化。 |
| 车载娱乐和平台化 | Sony Honda AFEELA 1 2026 年 California 交付，AFEELA Prototype 2026 世界首秀；强调 co-creation、Sony 内容生态、LiDAR SPAD/图像传感器展示 | 高端 EV 被重新包装成软件/内容/感知平台，但销量和利润弹性仍待验证。 |
| by-wire 与高精 radar | Bosch brake-by-wire/steer-by-wire 至 2032 年累计收入目标超 70 亿欧元；Radar Gen 7 可探测 200 米外小物体 | 安全执行层和传感器层比概念车更直接。 |

投资判断：短期可兑现的是 L2+/NOA、车载 AI cockpit、by-wire、radar、compute SoC、仿真/验证工具；L4 robotaxi 是长期期权。高估风险在“把 robotaxi 新闻直接折成 2026 收入”，低估机会在验证、传感、执行冗余和自动驾驶数据工厂。

### 主题 4：AI PC 进入产品期，但被内存和软件体验拖慢兑现

AMD 在 CES 把 Ryzen AI 400/PRO 400、Ryzen AI Max+、AI Halo Developer Platform、embedded P100/X100 同台发布，代表 PC、developer desktop、embedded edge 和 physical AI 被纳入同一产品线。关键事实：

| 指标 | 数字和日期 | 解释 |
|---|---:|---|
| Ryzen AI 400 NPU | 最高 60 TOPS，2026-01 首批系统，2026-Q1 扩大 OEM | 达到 Copilot+ /本地模型体验的硬件门槛，但不自动创造换机需求。 |
| Ryzen AI Max+ | 支持最高 128B 参数模型、128GB unified memory | 面向开发者和高端本地推理，量小但 ASP 高。 |
| PC 市场冲突 | Gartner 2026-Q1 全球 PC 出货 6,280 万台，+4%；IDC 后续预测 2026 全年 PC 出货 -11.3%，ASP +18.3%，市场价值约 2,740 亿美元 | Q1 的提前采购不能外推全年，内存短缺改变 AI PC 利润分配。 |
| AI PC 渗透 | Omdia/行业口径曾预期 2026 AI-capable PC 达约 50% 出货 | 该口径受内存价格和软件使用场景验证影响，应降权。 |

投资判断：AI PC 的真实利好更偏半导体内容提升、DRAM/SSD 价值量、散热/电源和高端配置 ASP；OEM 是否增利取决于能否把 BOM 上升转嫁给用户。若 2026-H2 本地 agent 使用时长、离线推理工作流、企业管理功能没有明显提升，AI PC 会从成长叙事变成 ASP 压力叙事。

### 主题 5：Industrial AI 和 digital twin 的证据质量高于多数消费 AI 设备

Siemens/NVIDIA/PepsiCo 的材料是本届 CES 最有投资价值的一手证据之一，因为它同时给出产品、客户、收益指标和上线节奏：

| 证据 | 数字 | 含义 |
|---|---:|---|
| Digital Twin Composer | 2026 年中通过 Siemens Xcelerator Marketplace 提供 | 从 keynote 进入可销售软件产品。 |
| PepsiCo 初始部署 | 吞吐量 +20%；识别最高 90% 潜在问题；近 100% design validation；Capex -10% 至 -15% | ROI 口径具体，优于大多数 AI demo。 |
| Siemens/NVIDIA 合作 | NVIDIA 提供 AI infrastructure、simulation libraries、models、frameworks；Siemens 投入数百名 industrial AI experts | 平台级合作，不是单点插件。 |
| EDA/仿真 | Siemens 目标在关键 EDA 工作流实现 2-10x speedup | 先进芯片设计和 AI factory 规划可能直接受益。 |
| Adaptive factories | 从 Siemens Electronics Factory in Erlangen 作为 blueprint，2026 年开始 | 先内部验证再外部复制，节奏相对可信。 |

投资判断：工业 AI 的利润池不只属于 GPU。Siemens、Cadence/Synopsys/Ansys 类 EDA/CAE/PLM 资产，工业自动化、MES、传感器、边缘计算、工厂网络、安全和电气基础设施都更贴近客户预算。客户不是为“AI”付费，而是为 throughput、capex、良率、停机时间和上市周期付费。

### 主题 6：Smart glasses、wearables 和 digital health 从设备销量转向健康数据/订阅/认证

CES 官方称智能眼镜已加入生成式 AI 语音、实时翻译、录制、QR 支付，健康可穿戴覆盖 OTC hearing aid、ECG watches、smart rings，并且医生开始建议用这类设备跟踪健康数据。

投资判断分两层：

1. 硬件层：摄像头、MEMS、低功耗 SoC、microdisplay、waveguide、电池和连接模块是确定性更强的零部件机会。
2. 服务层：Oura、Ultrahuman、RingConn、Withings、Earflo 等真正的利润弹性在订阅、健康算法、医疗认证、保险/企业 wellness 渠道，不在单次硬件毛利。

二手市场数据提供量级：IDC 披露 2025 年全球可穿戴设备出货 6.115 亿台，+9.1%；Grand View Research 估算 smart glasses 市场 2026 年约 31.6 亿美元；Fortune Business Insights 估算 smart ring 市场 2026 年约 5.19 亿美元。结论是：smart rings 和 AI glasses 增速快，但 2026 年绝对 TAM 仍小，不能把它们当作手机级平台。

### 主题 7：Smart home 和 appliance AI 是大市场、低差异化，除非绑定 energy/security/subscription

CES 官方 smart home 展商包括 Bosch、Dreame、LG、Samsung、SwitchBot。主题是 AI-driven personalization、predictive automation、adaptive security、lighting、appliances、thermostats。市场规模很大：Fortune Business Insights 估算 smart home 2026 年约 1,801 亿美元，MarketsandMarkets 给 2026 年约 2,308 亿美元。

但投资结论偏保守：

1. 白电、扫地机、安防摄像头加 AI 后，硬件功能会快速同质化。
2. 真正能改善利润率的是订阅安防、家庭能源管理、设备联动平台、耗材/服务、售后维护和数据驱动保险/节能收益。
3. AI home robot 仍多是 demo 阶段，若没有交付量、任务成功率、退货率和服务收入披露，不应给高倍数。

## 产品和技术路线三情景预测

以下预测以 2026-06-11 可得公开资料为基准。美元数字包括一手披露、二手市场研究和本报告估算。凡属于估算的项目均列出假设链条，置信度不等同于事实披露。

### 重要方向总表

| 方向 | CES 2026 成熟度 | 未来 3 个月判断 | 未来 1 年判断 | 未来 2 年判断 | 2026 市场量级 | 爆发力度 |
|---|---|---|---|---|---:|---|
| Rack-scale AI infrastructure | 产品预告/平台化，AMD Helios、NVIDIA Rubin/physical AI 生态 | 2026-Q1/Q2 主要看 OEM/云客户设计赢单和供货排期 | 2026-H2/2027 看 HBM4、网络、液冷和 rack 交付 | 2028 进入多平台竞争，NVIDIA/AMD/ASIC 并存 | AI accelerator + AI server/rack 硬件估算约 2,000-3,300 亿美元，低至中置信 | 主链条替代和供给瓶颈涨价 |
| Industrial digital twin/AI factory | 有产品、有客户指标，Siemens DTC 2026 年中上架 | 2026-Q2/Q3 看 PepsiCo 外更多客户早期接入 | 2027 看 ARR、实施周期和可复制 ROI | 2028 可能沉淀为工厂 AI 操作层 | 2026 digital twin 市场约 380-540 亿美元，中置信 | 工业软件利润池扩容 |
| Humanoid/industrial physical AI | Atlas 进入早期部署，Unitree/Doosan 等展出，家庭场景偏概念 | 2026 年内看 RMAC/Google DeepMind 任务学习和 uptime | 2027 看首批外部客户、unit cost、服务合同 | 2028 Hyundai HMGMA 部署是关键商业节点 | Humanoid 2026 估算约 40-70 亿美元，低置信 | 小品类高增速，先工业后家庭 |
| L4 robotaxi/autonomy data factory | Alpamayo 开源、Bosch/Kodiak 冗余平台、Qualcomm/BMW L2+ 已量产 | 3 个月内更像开发者/车队验证，不是大规模乘客收入 | 2027 看 robotaxi 城市扩张、NOA 装车和安全 case | 2028 若监管/保险允许，L4 revenue 起量 | Robotaxi 2026 约 12.7 亿美元；autonomous driving software 约 30 亿美元，中置信 | 从 0 到 1，但高监管风险 |
| AI PC/local inference | AMD/Intel/Qualcomm 等硬件到位，应用未完全到位 | 2026-Q2/Q3 看 Copilot+/本地 agent 使用和 DRAM 价格 | 2027 若企业管理/离线推理落地，AI PC 渗透上行 | 2028 可能成为默认配置而非溢价功能 | 2026 PC 市场价值约 2,740 亿美元；AI-capable 出货口径约 40%-50%，中置信 | 主链条升级，但 OEM 利润不一定扩张 |
| Smart glasses/XR | 产品很多，生态未定；AI voice/translation/recording 是主卖点 | 2026-H2 看 Meta/Android XR/中国厂商新品和退货率 | 2027 若应用生态和续航改善，出货加速 | 2028 可能成为轻量 wearable 平台 | Smart glasses 2026 约 31.6 亿美元，中置信 | 小品类高增速 |
| Health wearables/smart rings | Oura/Ultrahuman/RingConn/Withings/Earflo 等热度高 | 3 个月看新品价格和订阅留存 | 1 年看 FDA/医疗/保险/企业 wellness 渠道 | 2 年看能否成为健康数据入口 | Wearables 2025 出货 6.115 亿台；smart ring 2026 约 5.2 亿美元，中置信 | 小基数高增速，订阅驱动 |
| Smart home AI/energy/security | 大量产品发布，差异化不足 | 3 个月看 Matter/平台接入和售后评价 | 1 年看安防/能源管理订阅收入 | 2 年看 household robot 是否真实交付 | Smart home 2026 约 1,800-2,300 亿美元，中置信 | 大市场低利润，平台化才有弹性 |
| Automotive by-wire/radar/AI cockpit | Bosch/Qualcomm/NVIDIA 等均有一手材料 | 2026-H2 看 design wins、车型 SOP | 2027 看 L2+/NOA 装车率和功能付费 | 2028 受益 robotaxi/eyes-off 进展 | Bosch by-wire 至 2032 累计收入目标超 70 亿欧元；autonomy software 2026 约 30 亿美元 | 配套环节比整车更稳 |

### 三情景预测

| 方向 | 基准情景 | 乐观情景 | 超预期乐观情景 | 核心反证 |
|---|---|---|---|---|
| Rack-scale AI infrastructure | 2027 年 AI server/rack 硬件池约 2,800-3,800 亿美元；利润集中在 GPU/ASIC、HBM、networking、advanced packaging、liquid cooling | 2027 年达到 4,000-4,800 亿美元，AMD Helios/MI400 和 ASIC 形成第二供给曲线，缓解 NVIDIA 供给约束 | 2027 年超过 5,000 亿美元，企业/主权 AI 拉动 on-prem rack，HBM4 与液冷供给继续紧张 | HBM4 产能释放导致价格快速下行；云厂商 capex 下修；MI400/ROCm 客户验证低于预期 |
| Industrial digital twin/AI factory | Digital twin 2027 年约 500-650 亿美元，增长 25%-30%；Siemens DTC 以少数大客户扩张 | 2027 年约 650-800 亿美元，PepsiCo 式 ROI 被制造、食品饮料、物流和半导体厂复用 | 2027 年约 800-950 亿美元，AI factory blueprint 成为数据中心、汽车、电子制造标配 | 2026-Q4 前没有新增具名客户或 ARR；实施周期过长；现场数据接入成本吞噬 ROI |
| Humanoid/industrial physical AI | Humanoid 2027 年约 60-90 亿美元，主要来自工业试点、物流搬运、零部件排序 | 2027 年约 100-140 亿美元，Atlas/Unitree/Agility/Apptronik 等从 pilot 转小批量生产 | 2027 年约 150-200 亿美元，汽车厂和仓储客户把 humanoid 纳入标准 capex | 单机成本仍高于人工/专用机器人；MTBF、任务学习和安全认证不达标；客户只试点不扩单 |
| Robotaxi/autonomy data factory | 2027 年 robotaxi + autonomy software 约 50-70 亿美元，NOA/L2+ 比 L4 更快 | 2027 年约 80-120 亿美元，多个城市开放 robotaxi，Alpamayo/DRIVE/Hyperion 生态扩大 | 2027 年约 150 亿美元以上，监管加速、保险模型成熟、货运和 passenger 同步放量 | 安全事故/监管暂停；干预率不降；传感器和冗余硬件成本无法下探 |
| AI PC/local inference | 2027 年 PC 市场价值约 2,800-3,100 亿美元，AI PC 成为中高端默认配置但增量利润有限 | 2027 年 AI-capable PC 渗透 55%-65%，企业本地 agent 和开发者场景拉动高端配置 | 2027 年渗透超过 70%，本地隐私/离线推理成为企业采购硬约束 | DRAM/SSD 价格继续挤压 OEM；消费者不为 NPU 付费；Copilot+/本地 agent 使用低 |
| Smart glasses/XR | 2027 年 smart glasses 市场约 40 亿美元，增长 25%左右 | 2027 年约 48-55 亿美元，AI 语音、翻译、拍摄和支付形成高频场景 | 2027 年约 60 亿美元以上，平台级生态出现，microdisplay/waveguide 紧缺 | 续航、隐私、重量、退货率不改善；应用生态低频；价格下探损害毛利 |
| Smart rings/health wearables | 2027 年 smart ring 约 7 亿美元；wearables 出货温和增长，订阅是利润重点 | 2027 年 smart ring 约 9-10 亿美元，企业 wellness 和保险合作提升留存 | 2027 年 smart ring 约 12 亿美元以上，医疗/睡眠/代谢指标认证打开新渠道 | 健康指标准确度/监管被质疑；订阅留存下滑；智能手表直接复制功能 |
| Smart home AI/energy/security | 2027 年 smart home 约 2,100-2,600 亿美元，增长 12%-18%；利润偏平台和订阅 | 2027 年约 2,600-3,000 亿美元，能源管理和安防订阅提高 ARPU | 2027 年超过 3,200 亿美元，家庭机器人和能源调度规模交付 | AI appliance 同质化；隐私和云成本压利润；Matter 接入不能带来实际使用频率 |
| Automotive by-wire/radar/AI cockpit | 2027 年收入主要来自 design win 转 SOP，Bosch by-wire 长期累计目标超 70 亿欧元支撑 | L2+/NOA 全球装车率提升，Radar Gen 7、AI cockpit、drive-by-wire 同步放量 | L4 truck/robotaxi 拉动冗余执行器和 sensor ASP 进一步上行 | 整车降本压制供应商 ASP；监管延后 eyes-off；硬件冗余被低成本方案替代 |

## 市场规模和利润池

### 1. AI 基础设施和 rack-scale systems

事实：

1. AMD 2026-01-05 发布 Helios rack-scale platform，称单 rack 最高约 3 AI exaflops，由 MI455X、EPYC Venice、Pensando Vulcano NIC 和 ROCm 组成。
2. AMD 同时发布 MI440X 企业 on-prem 8-GPU 形态，并预告 MI500 2027 年推出，目标相对 2023 年 MI300X 平台实现最高 1,000x AI performance 增幅。该 1,000x 是工程预测，不是实测。
3. NVIDIA 在 CES 重点从消费 GPU 转向 physical AI、autonomy、robotics、industrial AI 和数据中心平台。

估算：

1. 2026 年 AI accelerator、AI server、rack networking、liquid cooling、power delivery 相关硬件池，本报告估算约 2,000-3,300 亿美元。链条为：公开数据中心 GPU/accelerator 收入、AI server BOM、networking、HBM、rack-scale integration 和液冷电源配套加总，置信度低至中。
2. 未来一年基准增速 25%-35%，乐观 45%-60%，超预期乐观 70%+。驱动是模型推理需求、agentic AI、主权 AI、on-prem enterprise AI 和 HBM4 转换。

利润池：

| 层级 | 价值捕获 |
|---|---|
| GPU/ASIC | 仍是最高利润池，NVIDIA 最强，AMD 争取第二供给曲线，ASIC 分食 hyperscaler 内部需求。 |
| HBM/先进封装 | 供给瓶颈和 ASP 弹性强，短期利润池可能超过部分服务器 OEM。 |
| Networking/NIC/switch | Rack-scale 竞争从单 GPU 转向 scale-up/scale-out，Ethernet、UALink、NVLink、InfiniBand 相关公司受益。 |
| 液冷/电源/电气 | 单 rack 功率上行使液冷、CDU、busbar、UPS、变压器和电网接入成为 capex 瓶颈。 |
| 系统集成/OEM | 收入大但毛利率通常低于芯片和关键零部件，除非拥有标准化 rack 方案和服务合同。 |

### 2. Industrial digital twin 和 AI factory

事实：

1. Grand View Research 估算 digital twin 市场 2025 年 358 亿美元、2026 年 495 亿美元；Precedence/MarketsandMarkets 等口径给 2026 年约 318-536 亿美元区间。
2. Siemens Digital Twin Composer 2026 年中上架，处 early access/select customers 阶段。
3. PepsiCo 初始部署给出可量化 ROI：+20% throughput、识别 up to 90% potential issues、nearly 100% design validation、Capex -10% 至 -15%。

估算：

2026 年 digital twin/industrial metaverse 市场可用 380-540 亿美元区间。2027 年基准 500-650 亿美元，乐观 650-800 亿美元，超预期乐观 800-950 亿美元。

利润池：

1. 软件 ARR：PLM、MES、QMS、simulation、operations data backbone。
2. 数据接入：PLC、IIoT、视觉、传感器、edge compute、工业网络。
3. 仿真计算：GPU/OVX/Omniverse/PhysicsNeMo/CAE。
4. 系统实施：工业客户现场数据结构复杂，咨询和集成服务会吃掉一部分价值，但也构成进入壁垒。

### 3. Humanoid robot 和 industrial robot

事实：

1. Atlas 进入产品版本，2026 年部署已排满，但大规模工厂部署节点在 2028/2030。
2. Atlas 规格：56 DoF、50 kg 举升、2.3 m reach、-20 至 40 摄氏度、自动换电、Orbit 接入 MES/WMS。
3. MarketsandMarkets 估算 humanoid robot 市场 2025 年 29.2 亿美元、2030 年 152.6 亿美元；IDTechEx 估算 2036 年约 295 亿美元；不同机构差异大。

估算：

本报告用 2026 年 humanoid robot 约 40-70 亿美元作为较宽区间，置信度低。若只统计可实际交付工业 humanoid，口径会显著更小；若把服务机器人、AI robot、软件和维护纳入，口径会显著更大。

利润池：

| 层级 | 判断 |
|---|---|
| 执行器/电机/减速器 | 最先受益，因为整机扩产先卡运动部件可靠性和成本。 |
| 传感器/触觉/视觉 | 人形机器人从 demo 转工业工位需要安全、定位、抓取和 force feedback。 |
| 控制器/edge AI | 实时控制和低延迟推理刚需，AMD embedded、NVIDIA Jetson/Thor、Qualcomm robotics SoC 等受益。 |
| Fleet software | 任务学习、任务复制、遥操作、安全区域、MES/WMS 接入是规模化关键。 |
| 整机 OEM | 叙事强但早期可能低毛利，需看 unit economics、维护成本和客户续约。 |

### 4. Autonomy、robotaxi 和 SDV

事实：

1. Global Market Insights 估算 autonomous driving software 市场 2026 年约 30 亿美元。
2. Fortune Business Insights 估算 robotaxi 市场 2026 年约 12.7 亿美元，2034 年 963 亿美元；Goldman Sachs Research 2026-04 估算 2035 年 global robotaxi 约 4,150 亿美元。
3. Qualcomm/BMW Snapdragon Ride Pilot 已在 BMW iX3 量产首发，已验证 60+ 国家，并计划 2026 年扩大到 100+ 国家。
4. Bosch by-wire 至 2032 年累计收入目标超 70 亿欧元；Radar Gen 7 可识别 200 米外小型物体。

估算：

2026 年可商业化收入更偏 L2+/NOA、automated driving software、传感器、compute SoC、by-wire 和仿真/验证；robotaxi 乘客收入仍小。2027 年合计可达 50-70 亿美元基准、80-120 亿美元乐观、150 亿美元以上超预期。

利润池：

| 层级 | 价值捕获 |
|---|---|
| Safety-certified compute | 单车价值高，认证周期长，平台锁定强。 |
| Sensor suite | Radar/LiDAR/camera/ultrasonic 组合受益，价格受规模化压制。 |
| By-wire/redundancy | 从 L2+ 到 eyes-off/L4 的必要条件，Bosch 类 Tier 1 有优势。 |
| Simulation/data factory | 每扩一城、每增一车型都需要数据、仿真、标注、验证和安全 case。 |
| Mobility service | 长期空间最大，但短期被车队 capex、监管和 utilization 限制。 |

### 5. AI PC 和 local AI device

事实：

1. AMD Ryzen AI 400 NPU 最高 60 TOPS，2026-01 首批系统，Q1 扩大 OEM。
2. Gartner 2026-Q1 PC 出货 6,280 万台，+4%；Counterpoint 口径为 Q1 6,330 万台，+3.2%。
3. IDC 后续预测 2026 年 PC 出货 -11.3%，ASP +18.3%，PC 市场价值约 2,740 亿美元；核心原因是内存短缺和价格上行。

估算：

2026 年 AI-capable PC 出货占比可能处 40%-50% 区间，受内存价格、企业采购和操作系统功能影响。2027 年基准 50%-60%，乐观 60%-65%，超预期 70%+。

利润池：

1. CPU/NPU/GPU SoC、DRAM、SSD、散热、电池和高端屏幕是确定性价值增量。
2. OEM 毛利率未必提升，因为 DRAM/SSD 价格会吞噬配置溢价。
3. 企业端管理、安全、离线推理和开发者工具如果形成高频使用，才会改变换机周期。

### 6. Smart glasses、XR 和 display

事实：

1. CES 官方强调 smart glasses 的生成式 AI 语音、实时翻译、录制和 QR payment。
2. Grand View Research 估算 smart glasses 2026 年市场约 31.6 亿美元，2033 年约 143.8 亿美元。
3. IDC 口径显示 XR glasses 2025-2029 CAGR 约 29.3%，但 headset 和 glasses 口径差异大。

估算：

2027 年 smart glasses 市场基准约 40 亿美元，乐观 48-55 亿美元，超预期超过 60 亿美元。核心变量是续航、重量、隐私接受度、应用生态和渠道补贴。

利润池：

microdisplay、waveguide、低功耗 SoC、camera sensor、MEMS、battery、voice AI、developer ecosystem。整机硬件若缺少订阅或生态，毛利率会受价格竞争压制。

### 7. Health wearables 和 smart rings

事实：

1. IDC 披露 2025 年全球 wearable 出货 6.115 亿台，+9.1%。
2. Fortune Business Insights 估算 smart ring 市场 2026 年约 5.19 亿美元。
3. CES 官方列举 smart rings、ECG watches、OTC hearing-aid earbuds、doctor recommendation 等方向。

估算：

2027 年 smart ring 基准约 7 亿美元，乐观 9-10 亿美元，超预期 12 亿美元以上。整体 wearables 出货大概率温和增长，收入和利润增长更依赖高 ASP、订阅和医疗渠道。

利润池：

传感器、健康算法、睡眠/心率/代谢模型、FDA/医疗认证、云订阅、保险/企业 wellness。单纯硬件可被快速复制，差异化弱。

### 8. Smart home、energy management 和 home robotics

事实：

1. Fortune Business Insights 估算 smart home 2026 年约 1,801 亿美元；MarketsandMarkets 估算 2026 年约 2,308 亿美元。
2. CES 官方 smart home 主题包括 appliances、assistants、energy management、entertainment、robots、security。

估算：

2027 年 smart home 市场基准 2,100-2,600 亿美元，乐观 2,600-3,000 亿美元，超预期 3,200 亿美元以上。硬件出货增长和平台服务增长需要分开看。

利润池：

安防订阅、能源管理、家庭数据平台、耗材/服务、安装维护、传感器和边缘 AI 模块。白电和单功能 gadget 的毛利率弹性有限。

## 反共识洞见和重要更新

### 1. 市场可能过度乐观：AI PC 和家庭机器人

AI PC 过度乐观点：

1. 硬件达到 40-60 TOPS 并不等于用户愿意为 NPU 付费。
2. 2026 年内存短缺导致 ASP 上行，可能让 AI PC 成为成本压力而非利润弹性。
3. 企业部署需要安全、管理、离线推理和明确效率提升；否则换机只是 Windows/硬件周期，不是 AI 新周期。

家庭机器人过度乐观点：

1. 展示的家务机器人多数没有披露任务成功率、服务成本、退货率和交付量。
2. 家庭环境比工厂更非结构化，安全和售后难度更高。
3. 2026-2028 更可信的商业路径是工厂/仓储/物流，而不是家庭通用助手。

### 2. 市场可能低估：工业 AI 的 ROI 已经开始被量化

Siemens/PepsiCo 的 20% throughput、10%-15% capex reduction、90% issue identification 不是典型展会概念，它给了 CFO 可以理解的投资回报口径。市场若只把 CES 看成消费电子展，容易低估工业软件、自动化、仿真、EDA、工厂网络、电气和数据中心基础设施的联动机会。

### 3. 市场可能低估：自动驾驶的价值正在从整车转向验证体系和冗余硬件

NVIDIA Alpamayo 明确把 teacher model、open weights、simulation、datasets 和 Halos 安全架构放在一起；Bosch/Kodiak 把车规硬件和 supply chain 放在一起。若只比较哪家 robotaxi 上路数量，会漏掉更早收入化的：

1. 仿真和数据闭环；
2. 传感器和高精 radar；
3. by-wire 和 redundancy；
4. safety-certified compute；
5. upfit/factory-line integration。

### 4. 看起来相关但收入暴露弱的公司

| 类型 | 为什么可能是伪受益 |
|---|---|
| 只发布 AI appliance 的家电公司 | AI 功能会被快速复制，收入大但毛利弹性低。 |
| 只有 CES demo、无交付时间和客户的机器人 startup | 媒体曝光不能替代 unit economics。 |
| 概念 XR/rollable/display 设备 | 技术展示很强，但若无量产时间、价格和渠道，不能折成 2026 收入。 |
| EV 整车概念发布 | CES 2026 的主线已从 EV 本身转为 AI、SDV、sensor、by-wire、robotaxi。 |
| 单点 AI app | 若不掌握数据、硬件入口、工作流或订阅渠道，容易被平台内置。 |

### 5. 小公司和上游瓶颈可能更有投资弹性

1. 机器人执行器、关节模组、减速器、力控和 tactile sensing。
2. Automotive radar、LiDAR、camera sensor、SPAD、by-wire、safety MCU。
3. Industrial digital twin 的数据接入、边缘网关、工厂视觉、PLC/MES/QMS 连接器。
4. AI rack 的 HBM、先进封装、PCB、光模块、液冷、电源、电气基础设施。
5. Health wearable 的传感器、医疗认证、订阅运营和保险/企业 wellness 渠道。

### 6. 必须立刻下修判断的后续数据

| 方向 | 下修触发器 |
|---|---|
| Industrial AI | 2026-Q4 前没有更多具名客户；DTC 只是 demo/早期访问，未形成可销售 SKU；ROI 无法复制。 |
| Humanoid | Atlas/同类机器人未披露 uptime、task learning、MTBF、维护成本；2027 外部客户未增加。 |
| Autonomy | Alpamayo 未进入实际车队训练/验证；robotaxi 城市扩张停滞；安全事故引发监管暂停。 |
| AI PC | 2026-H2 AI PC sell-through 弱；DRAM/SSD 价格继续上行；本地 agent 使用频率低。 |
| Smart glasses | 退货率高、续航差、隐私争议、生态低频；2027 出货低于 2026 预期。 |
| Smart rings | 订阅留存下降；准确度被监管或医疗机构质疑；手表/手机复制核心功能。 |
| Smart home | AI 功能无法带来订阅 ARPU；Matter/平台互联提升不了使用频率。 |

## 公司和产业链映射

### 头部公司

| 公司 | CES 2026 相关证据 | 收入暴露 | 投资弹性判断 |
|---|---|---|---|
| NVIDIA | Alpamayo、physical AI、automotive/robotics/industrial AI ecosystem、Siemens partnership | GPU、networking、DRIVE、Omniverse、DGX/OVX、robotics tools | 收入和利润池最大，但估值通常已反映较高预期；关注 inference cost、supply 和竞争。 |
| AMD | Helios、MI400/MI500、Ryzen AI 400、AI Halo、embedded P100/X100 | Data center GPU、CPU、PC、embedded edge | 弹性在能否从 chip 进入 rack/system 和 enterprise AI；ROCm/客户验证是关键。 |
| Siemens | Digital Twin Composer、Industrial AI OS、EDA acceleration、factory blueprint | 工业软件、自动化、EDA/CAE、digital twin、Xcelerator | CES 2026 后叙事从传统工业软件升级为 industrial AI platform，质量较高。 |
| Bosch | AI cockpit、Radar Gen 7、by-wire、Kodiak、Manufacturing Co-Intelligence | Mobility Tier 1、sensor、by-wire、software/services、factory AI | 未上市普通股，但对同行和供应链有强参照；Bosch 数据说明 by-wire 和 sensor 是核心利润池。 |
| Hyundai/Boston Dynamics | Atlas 产品版、2026 部署排满、2028 HMGMA、2030 assembly | 工业机器人、汽车制造自动化、执行器供应链 | 长期期权大，短期需看工厂 ROI；整车股未必是纯 robotics 受益。 |
| Qualcomm | BMW Snapdragon Ride Pilot、AFEELA 合作出现、automotive SoC | Automotive SoC、ADAS software stack、AI PC/edge | 比纯手机周期更有汽车和 edge AI 弹性；量产车导入强于概念 demo。 |
| Samsung/LG | AI display、smart home、appliance、OLED/automotive display | Display、TV、home appliance、memory、sensor | 显示和内存更值得跟踪，AI appliance 本身毛利弹性偏低。 |
| Sony Honda Mobility | AFEELA 1 2026 California delivery、AFEELA Prototype 2026、Sony content/sensor | 高端 EV、车载娱乐、传感器、co-creation platform | 更多是生态/品牌试验，销量和利润弹性暂不强。 |
| Microsoft | Bosch Manufacturing Co-Intelligence、Siemens industrial copilot 合作 | AI cloud、enterprise Copilot、factory AI | 受益于企业 AI 预算，但 CES 证据偏合作层。 |
| Meta | Ray-Ban AI glasses、Siemens industrial AI to Meta Ray-Ban AI Glasses | Smart glasses、AI assistant、AR ecosystem | 眼镜平台可能低估，但隐私、续航和应用频率是约束。 |

### 小公司、上游瓶颈和配套环节

| 环节 | 代表公司/线索 | 为什么值得跟踪 |
|---|---|---|
| Autonomous trucking | Kodiak AI | Bosch 合作让其从算法走向车规冗余硬件量产；关注 route miles、客户和安全事件。 |
| Robotics awards/startups | Doosan Robotics/Maple、Unitree、Richtech、Primech AI、Yarbo | 展会热度强，但要看真实客户、ASP、毛利率和服务成本。 |
| Edge AI computer | DEEPX、Sixfab ALPON X5、AMD embedded、Qualcomm robotics | physical AI 需要低延迟本地推理，边缘 AI 模块有明确位置。 |
| Sensors | Bosch Radar Gen 7、Sony SPAD LiDAR IMX479、IMX623、Hesai/Innoviz/Aeva/Arbe 等生态线索 | 自动驾驶、机器人、smart glasses 都依赖感知硬件，客户验证周期长。 |
| Actuators | Hyundai Mobis/机器人关节供应链 | Humanoid 扩产瓶颈，可靠性和成本直接决定 ROI。 |
| Digital twin implementation | Siemens ecosystem、AWS、Microsoft、工业系统集成商 | 大客户落地需要数据清洗、现场接入、仿真和运营流程改造。 |
| Smart health devices | Oura、Ultrahuman、RingConn、Withings、Earflo、Naqi | 硬件小但数据/订阅/医疗认证弹性大。 |
| Authentication/counterfeit tech | Bosch Origify | 工业/消费品数字身份，属于小而实用的 AI+视觉/安全方向。 |

### 伪受益和低纯度暴露

1. 只把“AI”作为营销词的 appliance/gadget 公司：市场大但护城河弱。
2. 没有量产时间、客户、认证、价格的概念显示/概念车/概念机器人。
3. 传统 EV 整车公司：若没有 SDV、ADAS、robotaxi、by-wire、车载 AI 平台或数据闭环，CES 2026 暴露不强。
4. 单一智能硬件品牌：若没有订阅、生态、数据、医疗认证或企业渠道，收入弹性容易被竞争稀释。
5. 小型 robotics startup：媒体热度高，但缺少供应链、售后、维护网络和安全责任能力。

## 风险、反证条件和后续跟踪

### 需要持续跟踪的节点

| 时间 | 节点 | 看什么 |
|---|---|---|
| 2026-Q2/Q3 | Siemens Digital Twin Composer 上架和客户扩展 | 是否有 PepsiCo 之外的具名客户、ARR/seat/usage、实施周期、ROI 复用。 |
| 2026-Q2/Q4 | AMD Helios/MI400/MI440X/AI Halo | OEM 和云客户、供货时间、ROCm 生态、HBM4/先进封装供给。 |
| 2026-H2 | AI PC sell-through | NPU 使用率、本地 agent 使用时长、企业采购、DRAM/SSD 价格、OEM margin。 |
| 2026-H2 | NVIDIA Alpamayo/DRIVE ecosystem | 开源社区采用、车队验证、L4 partners、仿真里程、安全 case。 |
| 2026-H2/2027 | Bosch-Kodiak | Driverless routes、客户、硬件平台量产、upfit vs factory-line 集成进度。 |
| 2026-H2/2027 | Boston Dynamics Atlas | RMAC/Google DeepMind 任务、uptime、task learning、unit cost、外部客户。 |
| 2027 | Qualcomm/BMW Snapdragon Ride Pilot | 国家扩张、车型扩展、NOA 使用率、付费率和安全表现。 |
| 2027 | Smart glasses/rings | 出货、退货率、订阅留存、认证、保险/企业渠道。 |
| 2027-01 | CES 2027 | 检验 2026 年概念是否变成订单、客户和可复制 ROI。 |

### 风险清单

1. 宏观和消费电子周期：CTA 预测美国消费技术收入 2026 年 5,650 亿美元、+3.7%，但关税、利率、内存和消费者信心都可能改变出货结构。
2. 供应链：HBM、DRAM、先进封装、液冷、电源、电气接入、传感器和机器人执行器都可能成为 bottleneck；也可能因扩产过快导致价格下行。
3. 监管：robotaxi、health wearable、smart glasses privacy、AI data、医疗认证都会影响上市节奏。
4. 可靠性：industrial AI 和 robot 需要 uptime、MTBF、safety、maintenance；demo 和真实工厂差距大。
5. 竞争：AI appliance、smart home、AI PC 和 smart glasses 容易出现功能同质化和价格战。
6. 估值：NVIDIA、AMD、robotics 和 AI infrastructure 相关资产若估值已提前反映超预期情景，基本面兑现稍慢就会引发回撤。

## 来源清单

### 一手官方和会议材料

| 来源 | 日期 | 用途 | 可信度 |
|---|---|---|---|
| CES official, "What Not To Miss at CES 2026" https://www.ces.tech/press-releases/what-not-to-miss-at-ces-2026 | 2026-01-02 | 会前主题、议程、展区、AI/digital health/energy/mobility/wearables 重点 | 高 |
| CES official, "CES 2026: The Future is Here" https://www.ces.tech/press-releases/ces-2026-the-future-is-here | 2026-01-09 | 会后主题、keynote、Foundry、robotics、smart glasses、smart home | 高 |
| CES official, "CES 2026 Audit Shows Four Percent Growth..." https://www.ces.tech/press-releases/ces-2026-audit-shows-four-percent-growth-in-participation-as-innovators-showed-up-in-las-vegas | 2026-03-31 | 参会人数、展商、AI/robotics 参会兴趣、国际参会者、媒体数 | 高 |
| CES Innovation Awards 2026 Honorees https://www.ces.tech/press-releases/cta-announces-ces-innovation-awards-2026-honorees | 2025-11/2026 | Innovation Awards 投稿变化和 Best of Innovation 名单 | 高 |
| CES Exhibitor and Sessions Directory https://exhibitors.ces.tech/ | 2026 | 会议日期、地点、展商/议程入口 | 高 |
| CES video/session: NVIDIA physical AI session https://www.ces.tech/videos/physical-ai-and-the-big-bang-of-robotics-and-autonomous-vehicles-presented-by-nvidia/ | 2026-01-07 | physical AI 会议主题和三计算机体系线索 | 中高 |

### 公司一手材料

| 来源 | 日期 | 用途 | 可信度 |
|---|---|---|---|
| AMD IR, "AI Everywhere, for Everyone" https://ir.amd.com/news-events/press-releases/detail/1272/amd-and-its-partners-share-their-vision-for-ai-everywhere-for-everyone-at-ces-2026 | 2026-01-05 | Helios、MI440X、MI500、Ryzen AI 400、AI Halo、embedded P100/X100 | 高 |
| AMD CES 2026 event page https://www.amd.com/en/corporate/events/ces.html | 2026 | AMD keynote、2.9 exaflops per rack、AI PC/embedded highlights | 高 |
| NVIDIA Newsroom, Alpamayo https://nvidianews.nvidia.com/news/alpamayo-autonomous-vehicle-development | 2026-01 | Alpamayo 1、10B 参数、AlpaSim、1,700+ 小时数据、Halos | 高 |
| NVIDIA CES 2026 page https://www.nvidia.com/en-us/events/ces/ | 2026 | physical AI、robotics、automotive、partner ecosystem | 高 |
| NVIDIA autonomous vehicles page https://www.nvidia.com/en-us/solutions/autonomous-vehicles/ | 2026 | DRIVE Hyperion、Alpamayo、Halos、L4-ready platform | 中高 |
| Siemens press release https://press.siemens.com/global/en/pressrelease/siemens-unveils-technologies-accelerate-industrial-ai-revolution-ces-2026 | 2026-01-06 | Industrial AI OS、DTC、PepsiCo ROI、EDA speedup、Meta Ray-Ban | 高 |
| Siemens Digital Twin Composer https://news.siemens.com/en-us/digital-twin-composer-ces-2026/ | 2026-01-06 | DTC early access、PepsiCo 20% throughput、10%-15% capex | 高 |
| NVIDIA/Siemens partnership https://nvidianews.nvidia.com/news/siemens-and-nvidia-expand-partnership-industrial-ai-operating-system | 2026-01-06 | Industrial AI OS、2-10x EDA workflow target、AI factory blueprint | 高 |
| Bosch CES 2026 press release https://us.bosch-press.com/pressportal/us/en/press-release-29504.html | 2026-01-05 | AI cockpit、Radar Gen 7、by-wire revenue、AI investment、Manufacturing Co-Intelligence | 高 |
| Kodiak/Bosch announcement https://kodiak.ai/news/kodiak-bosch-scale-autonomous-trucking-hardware | 2026-01-05 | Autonomous trucking redundant platform、Bosch hardware supply、CES booth | 高 |
| Boston Dynamics Atlas announcement https://bostondynamics.com/blog/boston-dynamics-unveils-new-atlas-robot-to-revolutionize-industry/ | 2026-01-05 | Atlas product version、2026 deployments、56 DoF、50 kg、task/fleet software | 高 |
| Hyundai Motor Group Atlas award/update https://www.hyundaimotorgroup.com/en/news/boston-dynamics-atlas-named-best-robot-in-best-of-ces-2026-awards-by-cnet-group | 2026-01-12 | 2028 HMGMA 部署、2030 component assembly、Atlas specs | 高 |
| Sony Honda Mobility CES 2026 https://www.shm-afeela.com/en/news/2026-01-07/ | 2026-01-07 | AFEELA 1 2026 California delivery、Prototype 2026、sensor/content ecosystem | 高 |
| Qualcomm/BMW Snapdragon Ride Pilot https://www.qualcomm.com/news/releases/2025/09/qualcomm-and-bmw-group-unveil-groundbreaking-automated-driving-s | 2025-09 | BMW iX3 量产、60+ 国家验证、100+ 国家计划、L2+/NOA | 高 |

### 市场规模和二手研究

| 来源 | 日期 | 用途 | 可信度 |
|---|---|---|---|
| CTA/PRNewswire, U.S. consumer tech revenue forecast https://www.prnewswire.com/news-releases/cta-despite-tariffs-and-economic-headwinds-us-consumer-tech-revenue-to-hit-565-billion-in-2026-302652218.html | 2026-01-04 | 美国消费技术 2026 收入 5,650 亿美元、+3.7% | 中高 |
| IDC PC forecast page https://www.idc.com/promo/pcdforecast/ | 2026 | PC 出货下修、ASP 上升、内存短缺 | 中高 |
| Gartner PC shipments Q1 2026 https://www.gartner.com/en/newsroom/press-releases/2026-4-10-gartner-says-worldwide-pc-shipments-increased-4-percent-in-first-quarter-of-2026 | 2026-04-10 | 2026-Q1 PC 出货 6,280 万台、+4% | 中高 |
| Counterpoint PC shipments Q1 2026 https://counterpointresearch.com/en/insights/global-pc-shipments-q1-2026 | 2026-04-17 | 2026-Q1 PC 出货 6,330 万台、+3.2% | 中 |
| Grand View Research digital twin https://www.grandviewresearch.com/industry-analysis/digital-twin-market | 2026 | Digital twin 2025/2026/2033 市场规模 | 中 |
| MarketsandMarkets digital twin https://www.marketsandmarkets.com/Market-Reports/digital-twin-market-225269522.html | 2026 | Digital twin 2025-2030 规模和 CAGR 交叉验证 | 中 |
| Global Market Insights autonomous driving software https://www.gminsights.com/industry-analysis/autonomous-driving-software-market | 2026 | Autonomous driving software 2025/2026/2035 | 中 |
| Fortune Business Insights robotaxi https://www.fortunebusinessinsights.com/robo-taxi-market-103661 | 2026 | Robotaxi 2025/2026/2034 市场规模 | 中 |
| Goldman Sachs Research robotaxi forecast https://www.goldmansachs.com/insights/articles/robotaxis-to-become-a-400-billion-dollar-market-in-2035 | 2026-04-30 | 2035 global robotaxi 约 4,150 亿美元 | 中高 |
| IDC wearable tracker page https://www.idc.com/promo/wearablevendor/ | 2026 | 2025 wearable 出货 6.115 亿台、+9.1% | 中高 |
| Grand View Research smart glasses https://www.grandviewresearch.com/industry-analysis/smart-glasses-market-report | 2026 | Smart glasses 2025/2026/2033 市场规模 | 中 |
| Fortune Business Insights smart home https://www.fortunebusinessinsights.com/industry-reports/smart-home-market-101900 | 2026 | Smart home 2025/2026/2034 市场规模 | 中 |
| MarketsandMarkets smart home https://www.marketsandmarkets.com/Market-Reports/smart-homes-and-assisted-living-advanced-technologie-and-global-market-121.html | 2026 | Smart home 2026/2032 规模交叉验证 | 中 |
| MarketsandMarkets humanoid robot https://www.marketsandmarkets.com/Market-Reports/humanoid-robot-market-99567653.html | 2025/2026 | Humanoid robot 2025-2030 市场规模 | 中 |
| IDTechEx humanoid robots https://www.idtechex.com/en/research-report/humanoid-robots/1149 | 2026 | Humanoid robots 2036 市场规模和应用判断 | 中 |

### 非官方材料和媒体线索

| 来源 | 日期 | 用途 | 可信度和处理方式 |
|---|---|---|---|
| MarkLines CES 2026 automotive report https://www.marklines.com/en/report/rep2974_202602 | 2026-02-20 | BMW iX3/Snapdragon Ride Pilot、Geely G-ASD、robotaxi/ADAS 展会观察 | 中；用于交叉验证汽车方向，不单独支撑结论 |
| The Verge CES auto coverage https://www.theverge.com/tech/856503/ces-2026-robotaxi-ai-ev-car-concepts | 2026-01 | EV 热度下降、robotaxi/AI 上升的媒体观察 | 中；作为市场情绪和展会体感 |
| AP CES Day 1 coverage https://apnews.com/article/a3e6e4e582ff83a4aa331d1791140369 | 2026-01 | NVIDIA physical AI、AMD、Uber/Lucid/Nuro、Boston Dynamics 等展会综合观察 | 中；作为交叉验证 |
| Berg Insight CES takeaways https://www.berginsight.com/key-takeaways-from-ces-2026-in-las-vegas | 2026-02 | Autonomy、robotics、edge AI 会后观点 | 中低；用于辅助线索 |
| Business Insider/其他现场报道 | 2026-01 至 2026-06 | AFEELA、Atlas、humanoid/physical AI 市场情绪 | 中低；只作为非官方参会和市场预期差材料 |

