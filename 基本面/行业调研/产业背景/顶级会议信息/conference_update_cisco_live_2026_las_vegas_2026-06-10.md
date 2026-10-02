# Cisco Live 2026 Las Vegas会议追踪：核心变化、产品爆发和市场预期差

会议对象：Cisco Live 2026 Las Vegas  
会议日期：2026-05-31 至 2026-06-04  
会议地点：Mandalay Bay Convention Center, Las Vegas, Nevada  
材料检索截止日期：2026-06-10 20:42 PT（UTC 2026-06-11）  
报告完成日期：2026-06-10 PT  
资料边界：本报告独立追踪公开会议材料、Cisco/ Splunk/ Webex/投资者资料、公开视频入口、二手分析与非官方分享；未读取、引用或继承项目内既有公司/行业/日度/量化/临时资料。

## 结论摘要

1. 最大变化：Cisco Live 2026 的主轴不是单个交换机、路由器或安全盒子的升级，而是 Cisco 把 Networking、Security、Compute、Observability/Splunk、Collaboration 和 Support Services 统一到 Cisco Cloud Control，并用 AgenticOps 把“人+AI agent 共同运维”定义成新的控制平面。Cisco 于 2026-06-02 宣布 Cloud Control 在美国进入 Controlled Availability，全球可用性随后推进；合作伙伴资料明确称对符合条件的 Cisco 产品订阅客户“无新增 license、无新增成本”，所以短期更像订阅留存、服务效率和跨域 attach 工具，而不是立刻新增一条大额 SaaS 账单。

2. 最大可验证需求信号来自财报而不是展台：Cisco Q3 FY2026（截至 2026-04-25，2026-05-13 发布）收入 158.41 亿美元、同比 +12%；产品订单同比 +35%、剔除 hyperscaler 后 +19%；Networking 产品订单同比超过 +50%；AI infrastructure 年初至今订单 53 亿美元，FY2026 预期订单从 50 亿美元上调到 90 亿美元、预期收入从 30 亿美元上调到 40 亿美元；Campus networking 订单同比超过 +25%，Data center switching 订单同比超过 +40%。会议叙事的可信度主要由这些订单数据支撑。

3. 最可能在 3-12 个月放量的不是“通用 AI agent”，而是 5 条更窄的产品/服务线：Cloud Control/AI Canvas 早期部署与 partner lifecycle services、Splunk Machine Data Lake/Agent Builder/AI Canvas 数据底座、Nexus 9000/Live Protect 与数据中心交换、Campus/branch smart switch 更新与量子安全 secure boot、Cisco IQ/Quantum Ready Assessment/Resilient Infrastructure Services。它们共同特点是：靠既有 Cisco 装机、订阅和维护预算切入，先节省运维/安全成本，再推动硬件刷新和服务 attach。

4. 最大分歧：市场容易把 Cloud Control 当成“新 SaaS ARR 产品”，但 Cisco 自己把商业模型描述为包含在合资格订阅中，并由 partner 通过 adoption、assessment、managed services、Agent Builder IP、Marketplace 扩展变现。短期收入弹性更可能体现在 Cisco 订阅续约率、服务毛利、跨域产品 attach、渠道服务 GMV，而不是 Cloud Control 单独披露 ARR。

5. 最大机会：AI 数据中心 Ethernet switching 和 campus refresh 是最接近“现在就有订单”的主链条。IDC 公开资料显示，2025 年全球 Ethernet switch 市场收入 551 亿美元、同比 +31.5%；4Q25 数据中心 Ethernet switch 收入 99 亿美元、同比 +63.0%，总 Ethernet switch 4Q25 收入 162 亿美元、同比 +35.1%。Cisco 的 FY2026 AI infra 订单上修说明它在 AI Ethernet、Silicon One、Nexus/optics/AI-ready data center 上已经进入订单期。

6. 最大风险：AgenticOps 仍处 Controlled Availability 和路线图阶段；Splunk Agent Builder 计划 2026 年秋季在 Splunk Cloud Platform GA，Machine Data Lake 仍为 Alpha；Quantum Ready Assessments 计划 2026 年 7 月全球可用，核心产品组合多数实现 quantum-safe communications 的承诺节点是 2026 年 12 月。若这些节点延迟，会议带来的软件/服务估值重估应下修。

7. 最值得跟踪的指标：Cisco Q4 FY2026 product orders、AI infrastructure orders/revenue conversion、Networking/ Security/ Observability 增速差、非 GAAP product gross margin、Cloud Control 从 Controlled Availability 到 GA 的地区节奏、Cloud Control Marketplace 是否出现可收费 partner IP、Splunk Machine Data Lake 是否从降低索引成本转化为更高数据留存和 AI workflow attach。

## 会议重点和方向变化

### 主题 1：Cloud Control 成为 Cisco 全组合入口，AgenticOps 从概念进入早期部署

核心事实：

- 官方发布日：2026-06-02，Cisco Live US。
- 产品状态：美国 Controlled Availability；全球可用性随后推进，二手 partner 信息多称美国先行、其他地区受数据主权工作节奏影响。
- 覆盖域：Cisco networking、security、compute、observability、collaboration 和 support/professional services。
- 关键组件：Cloud Control 单一管理平面、AI Canvas、Cloud Control Studio、Agent Builder、App Builder、Unified AI Assistant、Cloud Control Marketplace。
- 生态连接：官方新闻稿列出 AWS、Linear、Microsoft、PagerDuty、ServiceNow、Slack、Google Cloud（含 Wiz）等；新闻稿称 Agent Builder 可连接 50+ 第三方平台/工具或通过 MCP 扩展。
- 商业模型：partner 博客明确“eligible Cisco product subscriptions 的 Essential 和 Advantage tiers 包含 Cloud Control，无新增 license/成本”。这使短期投资判断应从“新增订阅收入”转向“留存率、服务效率、跨域 attach、partner IP”。

变化性质：

- 真实变化：Cloud Control 已进入 Controlled Availability；AI Canvas/Studio/Agent Builder 有可演示工作流；Cisco 将多域管理入口从若干控制器聚合到统一前门。
- 仍需验证：生产环境覆盖率、非美国地区可用性、与第三方工具的深度、Agent Builder 交付质量、Marketplace 是否形成可计费生态。
- 与 2025/过去 6-12 个月相比：2025 年更多是 AI Canvas、AI Defense、Splunk 整合、Cisco Data Fabric 等模块化叙事；2026 年 Las Vegas 的变化是把这些模块汇入一个统一操作层，并明确“human-in-control + trusted agents”的治理范式。

投资含义：

- 3 个月：看早期客户/partner cohort、On-Demand demo、Cisco Q4 FY26 订单/毛利是否延续。
- 1 年：看 Cloud Control 是否成为 Cisco 订阅续约和多域扩容的默认入口。
- 2 年：若 Marketplace 和 Agent Builder 形成可复用 partner IP，利润池会从硬件转向 managed agentic operations、workflow design、assessment、agent certification。

### 主题 2：AI 数据中心和 Ethernet switching 进入订单验证期

核心事实：

- Cisco Q3 FY2026 披露 AI infrastructure 年初至今订单 53 亿美元，FY2026 预期订单从 50 亿美元上修到 90 亿美元，预期收入从 30 亿美元上修到 40 亿美元。
- Data center switching orders 同比超过 +40%。
- Cisco 官方投资者页强调 Silicon One、AI-native security 和 operating systems 是 AI era critical infrastructure。
- Cisco Live 的会议页面把 Data Center 列为 Keynote Deep Dive 重点之一；Diamond sponsor 包括 NVIDIA、NetApp、Equinix，说明 AI 数据中心生态不是旁支。

变化性质：

- 真实变化：订单和收入上修是硬证据；IDC 2025 Ethernet switch 数据证明行业级需求强。
- 仍需验证：Cisco 的 AI infrastructure 订单是否集中在少数 hyperscaler、是否持续到 FY2027、是否损害 product gross margin。
- 与主流路径相比：市场仍把 AI networking 高 beta 主要给 Arista/NVIDIA/Broadcom；Cisco Live 2026 的反差在于 Cisco 用财报数字证明自己已经拿到大额 AI infra 订单，但估值叙事仍偏“旧网络设备商”。

### 主题 3：Live Protect 和“运行时防护”把安全从补丁窗口推到基础设施控制面

核心事实：

- Cisco 称 AI 使 vulnerability-to-exploit 窗口从数周压缩到数分钟。
- Live Protect 面向支持平台在 runtime shield 新漏洞，不要求 reboot、upgrade 或 downtime。
- 2026-06-02 官方新闻稿称 Live Protect 已在 N9000 series switches 可用，并包含在 Nexus One product entitlement；未来数月扩展到 campus/branch smart switches，随后在 2026 年晚些时候扩展到 secure routers。
- Hybrid Mesh Firewall 扩展跨网络、应用、Cisco 与第三方防火墙的统一保护。

变化性质：

- 真实变化：N9000/Nexus One 有明确可用性；扩展路线有时间顺序。
- 仍需验证：覆盖漏洞类型、对性能/误报的影响、客户是否愿意把自动屏蔽/隔离动作交给平台。
- 投资含义：更像高毛利软件 entitlement、维护续费和硬件产品差异化，而不是单独安全 appliance 放量。它提高 Nexus One/Cisco 安全订阅的 stickiness。

### 主题 4：Cisco IQ 从支持门户变成“风险画像+量子安全+韧性服务”入口

核心事实：

- Keynote summary 称 Cisco IQ 已 GA，并有 2,000+ customers onboarded。
- Cisco 新闻稿列出 Resilient Infrastructure Services：Exposure Assessment、Infrastructure Modernization、Defense Resiliency 三步法。
- Cisco IQ 新增 Quantum Ready Assessments，计划 2026 年 7 月全球可用，用于识别最暴露于 “harvest now, decrypt later” 攻击的资产。
- Cisco IQ 还计划支持 on-premises deployment options，并提供 Peer Benchmarking，用匿名数据比较 LDOS 风险暴露和安全漏洞率。

变化性质：

- 真实变化：Cisco IQ 客户导入数、服务方法、7 月可用性节点清楚。
- 仍需验证：客户是否为 assessment/modernization 单独付费，还是仅作为 support/professional services 的包装；服务毛利是否改善。
- 投资含义：看似“服务支持”，实际可能拉动旧设备替换、Zero Trust、secure boot、quantum-safe 产品更新。

### 主题 5：Splunk 被定位为 AgenticOps 的 intelligence layer，而不是单纯日志/SIEM

核心事实：

- 2026-06-02 Splunk 文章宣布 AI-powered Data Management、expanded Federated Search、Machine Data Lake、built-in Data Catalog、Agent Builder、Cisco Time Series Model 更新、AI Canvas 结合 Splunk Platform/ITSI/Observability Cloud。
- Machine Data Lake 当前为 Alpha，目标是更低成本保存、目录化、治理 full-fidelity machine data，不要求立即 indexing。
- Splunk Agent Builder 是 AI Toolkit 功能，计划 2026 年秋季在 Splunk Cloud Platform GA。
- Splunk 称 Autodesk 使用 Federated Search 后成本下降 28%、MTTR 降到 30 分钟以内，并维持关键应用指标 15-30 秒延迟；一家全球保险公司模拟用 Machine Data Lake 在 full-fidelity retention 下约降低 50% spend。

变化性质：

- 真实变化：Data Management、Federated Search、Agent Builder、Machine Data Lake 均有产品路线和客户示例。
- 仍需验证：Machine Data Lake 是否会稀释 Splunk 传统 ingest/indexing 单位经济，还是扩大留存数据量与 AI workflow attach。
- 投资含义：利润池从“每 GB 索引收费”向“数据治理、federated query、AI workflow、agent runtime、security/observability bundle”迁移。短期可能压低单位价格叙事，长期扩大数据面。

### 主题 6：Campus/branch 不是老旧存量，而是 AI、身份、量子安全和能源网络的落点

核心事实：

- Cisco Q3 FY2026 披露 campus networking orders 同比超过 +25%，next-generation portfolio ramping faster than prior product launches。
- Cisco Live session/blog 强调 Meraki Dashboard 管理员访问自动化、Meraki 与 cloud-managed Catalyst firmware automation。
- Security/campus blog 将 Cisco Cloud Control 作为 secure campus network 的统一管理面，引入 AgenticOps，把传统数小时 troubleshooting 缩短到秒级。
- Learn with Cisco 发布 Energy Networking Systems training（与 Panduit），并把 Cisco Silicon One for AI Networking、Agentic Operations、Industrial IoT Security 等列入新 learning paths。

变化性质：

- 真实变化：订单增长和 training/session 密度显示 campus refresh 不是纯会议叙事。
- 仍需验证：refresh 是否来自疫情后/库存周期补偿，还是可持续 2-3 年；Wi-Fi/PoE/Class 4 power/secure boot 是否真正带来 ASP 上行。
- 投资含义：Campus refresh 的毛利通常优于激烈竞争的 hyperscaler AI networking，但增速低于 AI data center；适合看 Cisco 的利润稳定器。

### 主题 7：Collaboration 从 Webex 单域走向 Cloud Control 跨域排障

核心事实：

- 2026-06-03/04 Webex blog 称 Webex Calling 支持 1,800 万+用户、200+ markets。
- Cisco Live 引入 AI Agents for Collaboration，将 Webex Contact Center 的 orchestration technology 扩展到更多业务、团队和用户。
- Collaboration Control Hub 进入 Cisco Cloud Control；AI Canvas 可用自然语言从 Control Hub 和其他 Cisco 平台取证，并结合 ThousandEyes 和 Meraki 数据定位通话质量问题，例如建议调整 Meraki QoS policy。
- Webex Calling/Cloud Control 集成处于 Controlled Availability。

变化性质：

- 真实变化：18M+ users 是规模基础，跨域排障有明确场景。
- 仍需验证：Collaboration Q3 FY2026 收入同比 -1%，说明 AI calling 还没变成增长项；要看 AI Receptionist、AI Assistant for UCM、Calling Plans for UCM 等 2026 年内更新能否改善 ARPU/retention。

### 主题 8：Quantum-ready 从远期概念变成 2026 年产品和 assessment 节点

核心事实：

- Cisco 承诺到 2026 年 12 月在其 majority core portfolio 启用 quantum-safe communications capabilities。
- 从 2026-06-02 起，新推出的 campus、branch、data center routers/switches/firewall series 默认具备 quantum-safe secure boot。
- Quantum Ready Assessments 通过 Cisco IQ 提供，计划 2026 年 7 月全球可用。
- Quantum Resilience Framework 给出 quantum-safe communications 和 quantum-safe products 两个支柱。

变化性质：

- 真实变化：时间点、产品范围、assessment 路径明确。
- 仍需验证：客户是否把 “harvest now, decrypt later” 纳入 2026/2027 预算；assessment 是否转化成硬件刷新和软件订阅。
- 投资含义：直接 TAM 不大，但可能成为旧设备替换、政府/金融/关键基础设施预算的合规触发器。

## 产品和技术路线三情景预测

说明：以下市场规模为 2026-06-10 公开资料口径和本报告估算。Cisco 未披露 Cloud Control、Live Protect、Quantum Ready Assessment、Agent Builder 等单项收入，本报告将“事实数字”和“估算链条”分开；所有估算均为低到中等置信度，需用后续财报和 GA 节点更新。

| 产品/方向 | 会议证据与成熟度 | 当前市场/收入口径 | 未来 3 个月节点 | 未来 1 年基准 | 未来 1 年乐观 | 未来 1 年超预期乐观 | 2 年判断与利润池 |
|---|---|---:|---|---:|---:|---:|---|
| Cisco Cloud Control / AI Canvas / AgenticOps | 2026-06-02 美国 Controlled Availability；50+ 第三方连接/MCP；AI Canvas/Studio/Agent Builder/App Builder；符合条件订阅无新增 license | 直接新 license 当前近似 0；可影响 Cisco RPO 435 亿美元、年化 services revenue 约 149 亿美元、product subscription attach | 早期美国 cohort、partner enablement、On-Demand demo、GA 地区路线 | FY2027 可形成 2-5 亿美元 adoption/assessment/managed services 间接服务池；主要体现为续费和 attach | 8-12 亿美元 partner/Cisco lifecycle services 与扩展订阅影响 | >20 亿美元生态 IP/managed agentic operations，Marketplace 有可付费 agent | 长期价值在服务效率、跨域 attach、agent/workflow IP；硬件收入被拉动但不是 Cloud Control 单项 ARR |
| AI data center switching / Silicon One / Nexus / AI infra | Cisco FY26 AI infra orders 预期 90 亿美元、收入 40 亿美元；DC switching orders +40%；IDC 2025 Ethernet switch 551 亿美元，4Q25 DC switch 99 亿美元 | Cisco AI infra FY26 revenue guide 40 亿美元；全球 Ethernet switch 2025 551 亿美元 | Q4 FY26 orders/revenue conversion；hyperscaler concentration；毛利 | Cisco AI infra revenue 50-55 亿美元；全球 Ethernet switching 2026/27 年化 600-660 亿美元 | Cisco 60-70 亿美元；全球 700 亿美元附近 | Cisco 80-100 亿美元；全球 750 亿美元+，AI Ethernet 继续挤压传统 switch mix | 利润池在 ASIC/系统设计、光互联、Nexus One/management entitlement、服务集成；竞争主要 Arista/NVIDIA/Broadcom/HPE-Juniper |
| Campus/branch smart switching、Meraki/Catalyst automation、quantum-safe secure boot | Campus orders +25%；new-generation portfolio ramping faster；Live Protect 后续扩到 campus/branch smart switches；firmware/admin automation sessions | 非数据中心 Ethernet/campus 2026 估算约 180-230 亿美元；Cisco Networking Q3 product 增速 +25% | 新 smart switches/secure boot 可用性、客户 refresh pipeline、tariff/ASP | 市场 +5%-8%；Cisco campus 高个位数到低双位数增长 | 市场 +10%-15%；安全/量子/AI readiness 拉动 ASP | 市场 +20% 左右，若旧设备量子/AI 安全风险触发提前替换 | 利润池在 access switch、wireless、Meraki dashboard、managed services；比 AI DC 增速低但毛利/稳定性更好 |
| Live Protect / Hybrid Mesh Firewall / Agentic Security | Live Protect 已支持 N9000 并随 Nexus One entitlement；扩展 campus/branch，后到 secure routers；Hybrid Mesh Firewall；AI Defense/ZT for agents/Agentic SOC | SASE 2026 市场外部估算 >130 亿美元；Cisco Security Q3 FY26 收入同比 flat | N9000 客户部署、campus/branch 支持、误报/性能案例 | Cisco security 重回 +3%-6%；Live Protect 主要提高 Nexus/Security subscription attach | +8%-12%，若 AI-scale vulnerability 预算提前 | +15%+，若 runtime shielding 成为关键基础设施采购门槛 | 利润池在安全订阅、runtime policy、identity/NHI、firewall mesh、SOC workflow；硬件安全盒子不是唯一受益层 |
| Splunk Machine Data Lake / Federated Search / Agent Builder / Data Fabric | MDL Alpha；Agent Builder 计划 Fall 2026 在 Splunk Cloud GA；Autodesk 成本 -28%、MTTR <30min、15-30s latency；保险客户模拟 spend -50% | Observability 市场口径冲突：窄口径约 33.5 亿美元（2026），广义 observability/data platform 约 341 亿美元（2026）；Cisco Observability Q3 +3% | MDL Alpha 反馈、Agent Builder GA、AI Canvas/Splunk in Cloud Control | 广义数据/observability spend +15%-20%；Splunk attach 先改善留存和数据量 | +25%-35%，Data Lake 降低成本后扩大 full-fidelity retention | +40%+，如果 agent workflow 让 Splunk 成为 IT/security AI runtime | 价值从 per-GB indexing 迁移到 data catalog、federated query、governed AI agents、SOC/ITSI workflow；短期 ASP 可能承压 |
| Cisco IQ / Resilient Infrastructure Services / Quantum Ready Assessments | Cisco IQ GA 且 2,000+ customers；Quantum Ready Assessments 2026-07 GA；多数核心 portfolio quantum-safe by 2026-12 | 直接 assessment 市场未披露；本报告估 2026 quantum/network resilience 服务池 5-15 亿美元，低置信度 | 7 月全球可用、on-prem IQ、peer benchmarking | 10-30 亿美元服务/assessment/modernization 影响，主要拉动旧设备替换 | 30-50 亿美元，如果金融/政府/关键基础设施形成预算 | >50 亿美元，若 PQC 合规提前成为大型 RFP 必要条件 | 利润池在服务、assessment、硬件 refresh、secure boot/communications entitlement；不是纯量子计算投资 |
| Webex Calling AI / Collaboration Control Hub in Cloud Control | Webex Calling 1,800 万+用户、200+ markets；AI Agents for Collaboration；Control Hub 并入 Cloud Control；AI Canvas 排障调用 ThousandEyes/Meraki | UCaaS 2026 市场外部估算 705.6 亿美元；Cisco Collaboration Q3 FY26 -1% | AI Receptionist/UCM、AI Assistant for UCM、Calling Plans for UCM 节点 | Webex calling 用户增至 1,950-2,050 万，collaboration 收入恢复 0%-3% | 用户 2,100 万+，AI attach 拉 ARPU +3%-5% | 用户 2,300 万+，contact center/calling agents 带来双位数软件增长 | 利润池在 cloud calling seat、contact center workflow、AI receptionist/agent、跨域 SLA；竞争 Microsoft Teams Phone/Zoom/RingCentral |
| Partner-built Cloud Control IP / Managed Agentic Operations | Cisco partner blog 强调 year 1 positioning，years 2-3 Marketplace/IP；NTT DATA 示例；WWT/Equinix/NetApp/NVIDIA 为重要赞助商 | 直接市场未披露；以 Cisco partner managed services 和 enterprise IT ops services 的极小切片估算 | CA cohort、partner certification、首批 vertical agent | 2-5 亿美元可见项目收入 | 8-15 亿美元，若 MSP 把 agentic ops 产品化 | >30 亿美元，若 Marketplace 把 workflow/agent 做成可复用 SKU | 价值捕获可能在 WWT/CDW/SHI/NTT DATA/Presidio 等服务商；上市弹性弱于纯软件但现金流更稳 |

## 市场规模和利润池

### 1. Ethernet switching / AI data center networking

事实口径：

- IDC 公开资料：2025 年全球 Ethernet switch 市场收入 551 亿美元，同比 +31.5%；2025 年 4Q 总市场 162 亿美元，同比 +35.1%；数据中心部分 4Q25 收入 99 亿美元，同比 +63.0%。
- Cisco Q3 FY2026：AI infrastructure FY26 预期订单 90 亿美元、收入 40 亿美元；Data center switching orders +40%。

估算：

- 2026-2027 年全球 Ethernet switch 年化规模基准 600-660 亿美元，乐观 700 亿美元附近，超预期乐观 750 亿美元+。逻辑：2025 高基数后增速从 +31.5% 回落，但 AI data center 仍拉动 mix。
- Cisco AI infra revenue FY2027 基准 50-55 亿美元，乐观 60-70 亿美元，超预期 80-100 亿美元。逻辑：FY26 revenue 40 亿美元、orders 90 亿美元，若 50%-70% backlog 在 12-18 个月转 revenue 则有上行；风险是 hyperscaler timing 和毛利折扣。

利润率：

- Cisco Q3 FY2026 product gross margin 61.9% GAAP、64.3% non-GAAP；total non-GAAP gross margin 66.0%，operating margin 34.2%。
- AI data center 交换机可能因 hyperscaler 议价和 optics/ASIC 成本压低毛利，但系统、software entitlement、Nexus One/Live Protect 可以补偿。

价值捕获：

- 短期：Cisco/Arista/NVIDIA/Broadcom 等系统、ASIC、fabric software；光模块/线缆/测试为配套。
- 中期：AI fabric observability、intent verification、runtime security、power/thermal-aware operations。
- 伪受益：只卖“AI networking 概念”但无 hyperscaler/enterprise fabric 订单的边缘厂商。

### 2. Cloud Control / AgenticOps / IT operations platform

事实口径：

- Cisco 未披露 Cloud Control 单独价格或 ARR。
- Partner 资料显示 Cloud Control 对符合条件的 Essential/Advantage subscription 客户无新增 license/成本。
- Cisco Q3 FY2026 RPO 435 亿美元；services revenue Q3 37.24 亿美元，年化约 149 亿美元。

估算：

- 2026-2027 直接 license TAM 不应建模为新增数十亿美元 ARR；合理建模是：Cloud Control 影响 Cisco subscription retention、services attach、support productivity、partner managed services。
- FY2027 间接收入/服务池基准 2-5 亿美元，乐观 8-12 亿美元，超预期 >20 亿美元。置信度中低，等待 CA cohort、GA、Marketplace 数据。

利润率：

- 如果作为软件/服务 attach，毛利应高于硬件；如果以无新增 license 方式嵌入，短期利润率改善来自 churn 降低、服务自动化和交叉销售，而非可单独观察的 gross margin。

价值捕获：

- 长期最可能赚钱：IP/软件控制平面、Agent Builder/Marketplace、assessment/managed service、cross-domain telemetry data layer。
- 短期最确定赚钱：Cisco 订阅续约、partner lifecycle services、客户环境梳理项目。

### 3. Security / SASE / runtime infrastructure defense

事实口径：

- Dell'Oro 旧预测：SASE 市场 2026 年超过 130 亿美元；Gartner 旧预测 2025 年约 147 亿美元。公开口径存在时间和定义差异。
- Cisco Q3 FY2026 Security revenue 同比 flat；这说明会议安全叙事还未直接反映成增长。
- Live Protect 已落到 N9000/Nexus One，扩展 campus/branch 和 secure routers 有 2026 年内路线。

估算：

- SASE/secure access/runtime protection 2026 spend pool 130-160 亿美元；未来一年基准 +15%-20%，乐观 +25%，超预期 +30%+。Agentic security 会拉高 identity、policy、runtime enforcement、SOC automation 的占比。

利润率：

- 软件安全订阅毛利通常高；硬件 firewall/router 取决于 appliance mix。
- Live Protect 随 entitlement 嵌入，短期更多提升 Nexus One/Cisco portfolio 差异化和续费质量。

价值捕获：

- 最可能赚钱：policy/control plane、identity/NHI、runtime shielding、SOC automation、firewall mesh。
- 低弹性环节：单纯卖传统 firewall box、没有 AI/agent/workload context 的工具。

### 4. Splunk / Observability / machine data layer

事实口径：

- Splunk 2026-06-02 发布：Machine Data Lake Alpha，Agent Builder 计划 Fall 2026 Splunk Cloud GA，AI Canvas/Splunk Platform/ITSI/Observability Cloud 将进入 Cisco Cloud Control。
- 市场口径冲突：窄口径 observability 市场 2026 约 33.5 亿美元；广义 observability tools/platforms 2026 约 341 亿美元。差异来自是否包括 data platform、log analytics、security telemetry、AI data management。

估算：

- 对 Cisco/Splunk 更有意义的是广义 machine data + observability + security analytics pool，2026 可用 250-350 亿美元作为宽口径约束。
- 未来一年基准 +15%-20%，乐观 +25%-35%，超预期 +40%+；但 Splunk 的单位价格可能因为 Machine Data Lake 降低存储/indexing 成本而重新定价。

利润率：

- 高毛利软件，但 cloud storage/compute、数据保留成本、客户压价会影响 gross margin。
- Machine Data Lake 若把低价值日志从 expensive indexing 移出，短期 revenue per GB 可能下降，长期保留更多数据、驱动 AI agents 和 cross-domain workflow。

价值捕获：

- 最可能赚钱：data catalog、federated search、governed AI agents、SIEM/observability workflow、AI Canvas persistent context。
- 被低估环节：数据管道治理、schema/context enrichment、cost optimization。

### 5. Collaboration / UCaaS / Contact Center agents

事实口径：

- Webex Calling 1,800 万+用户、200+ markets。
- UCaaS 2026 市场外部估算约 705.6 亿美元，2031 年 2,211.4 亿美元，CAGR 25.67%；另有更保守口径从 371.7 亿美元起步。定义差异很大。
- Cisco Q3 FY2026 Collaboration revenue 同比 -1%。

估算：

- Webex AI Calling 的未来一年基准不是爆发，而是止跌：Collaboration 收入 0%-3% 增长；乐观 5%-8%；超预期 10%+，需 AI agents/contact center attach 明显拉升 ARPU。

利润率：

- Cloud calling seat 和 AI add-on 软件毛利高，但竞争强；PSTN/运营商/硬件 endpoint 价值捕获较弱。

价值捕获：

- 更可能赚钱：AI receptionist、contact center workflow、cross-domain SLA assurance、Control Hub/Cloud Control integration。
- 伪受益：单纯会议终端/硬件 endpoint，除非绑定高价值服务。

### 6. Quantum-ready infrastructure

事实口径：

- Quantum Ready Assessments 计划 2026 年 7 月全球可用；多数核心 portfolio 量子安全通信能力承诺节点 2026 年 12 月；新基础设施系列默认 quantum-safe secure boot。

估算：

- 2026 年直接软件/assessment spend pool 可能只有 5-15 亿美元，低置信度；但它可触发数十亿美元级别的网络/security hardware refresh 和 services modernization。
- 未来一年基准 10-30 亿美元相关预算影响；乐观 30-50 亿美元；超预期 >50 亿美元，条件是政府、金融、关键基础设施把 PQC readiness 纳入采购硬性要求。

利润率：

- Assessment 和软件高毛利；硬件 refresh 毛利看产品 mix。

价值捕获：

- 最可能赚钱：Cisco IQ/services、secure boot/communications enabled hardware、crypto inventory/assessment、身份和证书管理。
- 风险：客户把 PQC 当长期合规议题，2026/2027 不急于花钱。

## 反共识洞见和重要更新

### 洞见 1：Cloud Control 的短期收入弹性可能被高估，但战略粘性可能被低估

过度乐观处：把 Cloud Control 直接当成一个新 SaaS 大单品。官方/partner 资料显示它对合资格订阅客户无新增 license/成本，并处 Controlled Availability。

被低估处：它把 Cisco 原本分散的 Catalyst/Meraki/Intersight/Security/Control Hub/Splunk/ThousandEyes/Cisco IQ 入口收进统一操作层，能提高多域 attach 和续费。真正弹性不是第一年收费，而是第二、三年 partner IP、Marketplace、managed agentic operations 和 cross-sell。

反证条件：2026 年底前无清晰 GA 路线、无生产客户案例、无 Marketplace 交易或 partner case、Cisco subscription/RPO 无改善。

### 洞见 2：AI data center 是硬订单，AgenticOps 是平台叙事；两者不要混为一谈

会议最“AI”的语言来自 AgenticOps，但最硬的收入来自 AI infrastructure orders。Cisco 把 FY2026 AI infrastructure expected orders 提到 90 亿美元，这是比任何 demo 更强的信号。

反证条件：Q4 FY2026 或 FY2027 指引中 AI infra orders/revenue conversion 不达预期；product gross margin 明显低于 64% 附近；客户集中导致订单波动。

### 洞见 3：Splunk Machine Data Lake 可能同时利空旧计费、利多新数据面

市场通常把“降低数据存储/索引成本”理解为客户省钱、vendor 降价。但对 Splunk/Cisco 来说，若客户原先因成本不愿保存 full-fidelity telemetry，Machine Data Lake 可以扩大被 AI agents 可访问的数据面。短期 ASP/GB 可能承压，长期 agentic workflow attach 可能扩大。

反证条件：Machine Data Lake GA 延迟；客户只用它降本而不增加 AI/SOC/ITSI workflow；Splunk Observability/Security 增速仍低个位数。

### 洞见 4：Quantum-ready 不是量子计算交易，而是网络资产替换交易

Quantum Ready Assessments 和 quantum-safe secure boot 的投资意义不在量子计算本身，而在给政府、金融、医疗、关键基础设施客户提供一条更容易写进预算和 RFP 的替换理由。若 Cisco IQ 能把 LDOS、漏洞率、PQC 暴露一并量化，会把“风险画像”变成硬件和服务订单。

反证条件：2026 年 7 月 assessment 只是轻量报告，不能转化成 modernization；客户 PQC 预算推迟到 2028 年以后。

### 洞见 5：Cisco Security 的会议叙事强，但财报仍弱

Security 主题在会议上非常密集，Live Protect、AI Defense、Zero Trust for agents、Agentic SOC、Hybrid Mesh Firewall 都有路线。但 Q3 FY2026 Security revenue flat，说明商业化仍未验证。市场若只看会议热度可能过度乐观。

反证条件和上修条件：若 Q4/FY2027 Security 恢复中高个位数增长，且 Live Protect 带动 Nexus/Security subscription attach，需上修；若继续 flat，应把安全会议叙事降权。

### 洞见 6：真正的小弹性可能在 partner 服务与垂直 agent IP，不在纯概念软件

Cisco partner 博客明确指出 year one 是 positioning/learning，years two and three 随 Marketplace 成熟可把 partner expertise 变成 reusable IP。WWT、NTT DATA、Presidio、CDW、SHI 等服务商更可能在早期项目中捕获现金流；上市标的弹性不一定高，但渠道反馈会先反映客户真实预算。

反证条件：合作伙伴只做免费 adoption，没有可收费 assessment/managed service/agent package；客户把 Cloud Control 当免费工具而不扩大 Cisco footprint。

## 公司和产业链映射

### 头部直接受益

| 公司/环节 | 会议相关度 | 收入暴露 | 投资弹性 | 关键观察 |
|---|---:|---:|---:|---|
| Cisco / CSCO | 极高 | Networking、Security、Observability/Splunk、Collaboration、Services 全部暴露 | 中高 | AI infra orders 90 亿美元 FY26、Cloud Control GA、Security 是否从 flat 恢复 |
| NVIDIA / NVDA | 中高 | Diamond sponsor；AI data center 生态；与 Cisco AI infra 相关 | 中 | Cisco Live 不是 NVIDIA 新 GPU 发布会，更多是生态背书 |
| NetApp / NTAP | 中 | Diamond sponsor；数据中心/AI 数据管理生态 | 中 | AI data pipeline、storage attach、Cisco partner motion |
| Equinix / EQIX | 中 | Diamond sponsor；hybrid/multicloud/AI interconnect 场景 | 中 | Multicloud Fabric、enterprise AI hosting、network-as-a-service |
| ServiceNow / NOW | 中 | Cloud Control 第三方 workflow 连接；ITSM/ITOM | 中 | AgenticOps 是否把 incident/change workflow 导向 ServiceNow |
| Microsoft / AWS / Google Cloud-Wiz | 中 | Cloud Control connectors、multicloud、安全/云集成 | 低到中 | 生态入口强，但 Cisco Live 对其收入弹性稀释 |

### 竞争和替代映射

| 方向 | Cisco 方案 | 主要竞争/替代 | 判断 |
|---|---|---|---|
| AI data center Ethernet | Silicon One、Nexus、AI infra、Cloud Control | Arista、NVIDIA Spectrum-X、Broadcom ecosystem、HPE-Juniper | Cisco 有订单验证，但 hyperscaler share 需逐季跟踪 |
| Campus/branch | Catalyst/Meraki、smart switches、Cloud Control | HPE Aruba/Juniper Mist、Ubiquiti、Extreme | Cisco 有装机和服务优势；AI/quantum 安全可拉动 refresh |
| Security/SASE | AI Defense、Live Protect、Hybrid Mesh Firewall、Zero Trust for agents | Palo Alto、Fortinet、Zscaler、Cloudflare、CrowdStrike、CyberArk/SailPoint | Cisco 叙事完整但 Security revenue flat，需验证执行 |
| Observability/Data Fabric | Splunk Platform、Machine Data Lake、Federated Search、AI Canvas | Datadog、Dynatrace、Elastic、Grafana、New Relic | Cisco/Splunk 适合 machine data/security/networking 跨域，APM 纯软件竞争仍强 |
| UCaaS/CCaaS | Webex Calling、AI Agents for Collaboration、Control Hub in Cloud Control | Microsoft Teams Phone、Zoom Phone、RingCentral、Genesys/NICE | Webex 用户规模大但 Collaboration revenue -1%，需看 AI attach |
| Partner services | Cloud Control adoption、Agent Builder、Marketplace IP | WWT、NTT DATA、Presidio、CDW、SHI、regional MSPs | 早期现金流可能先在私有/渠道服务商体现 |

### 上游瓶颈和配套环节

- ASIC/系统设计：Silicon One、merchant silicon、switch system design。受 AI fabric 和高速 Ethernet 拉动。
- 光互联/线缆/测试：800G/1.6T optics、DAC/AEC、fabric validation、interoperability testing。Cisco Live 不是光通信会议，不能把 OFC 逻辑硬套，但 AI switching 放量会间接拉动。
- Telemetry/data pipeline：日志、metrics、traces、network telemetry 的采集、清洗、catalog、federated query 是 Splunk/Cisco Data Fabric 的关键瓶颈。
- Identity/NHI：agent 身份、权限、行为审计和 policy enforcement 是 agentic security 的前置条件。
- Services/certification：Quantum Ready Assessment、resilience assessment、Cloud Control readiness、agent workflow validation 可能成为高毛利服务。

### 伪受益公司/弱暴露公司

- 只做“AI agent”应用但没有 network/security/observability telemetry 和 enforcement point 的公司：与 Cisco Live 主线相关性弱。
- 只卖传统网络硬件、没有 controller/telemetry/security entitlement 的厂商：可能受益 refresh，但利润弹性低。
- 泛数据中心地产/电力公司：Cisco Live 对其只是间接确认 AI infra 需求，不能单独作为买入依据。
- 单纯会议终端/视频硬件供应商：Webex 的重点在 calling AI、contact center orchestration、Cloud Control 排障，不是 endpoint refresh。

## 风险、反证条件和后续跟踪

### 关键风险

1. 可用性风险：Cloud Control 仍处 Controlled Availability；AI Canvas/Studio/Agent Builder/Marketplace 的 GA 和地区覆盖不确定。
2. 商业化风险：无新增 license 对客户友好，但降低短期 ARR 可见度；投资者若预期立刻新增 SaaS 收入会失望。
3. 毛利风险：AI infra/hyperscaler 订单可能拉低 product gross margin；Cisco Q3 FY2026 non-GAAP product gross margin 64.3%，需盯是否跌破 62%-63%。
4. 安全增长风险：Security revenue Q3 FY2026 flat，与会议安全叙事不匹配。
5. Splunk 定价风险：Machine Data Lake 降本可能压低 ingest/indexing revenue per unit，需靠更大数据量和 AI workflow 抵消。
6. 量子安全预算风险：PQC readiness 可能被客户视为长期合规事项，短期 assessment 转订单慢。
7. 数据主权和隐私风险：Cloud Control/Splunk/Cisco IQ 的跨域 telemetry 在欧洲、政府、金融等场景可能需要 on-prem 或区域化，拖慢全球 GA。
8. 竞争风险：Arista/NVIDIA/Broadcom 在 AI networking、Palo Alto/Zscaler/Fortinet 在 security、Datadog/Dynatrace 在 observability、Microsoft/Zoom 在 calling 都有强替代。

### 立即下修判断的反证条件

- Cisco Q4 FY2026 披露 AI infrastructure orders 或 revenue conversion 低于 FY26 90 亿/40 亿美元预期路径。
- Networking orders 从 +50% 迅速回落到个位数，且 campus/data center orders 同时放缓。
- Cloud Control 到 2026 年 12 月仍无美国以外清晰 GA 或 production customer case。
- Splunk Agent Builder 未在 2026 年秋季 GA，Machine Data Lake 仍停留 Alpha 且无新增客户案例。
- Security revenue 连续两个季度 flat/decline，Live Protect 未显示对 Nexus One 或 security subscription attach 的贡献。
- Cisco product gross margin 因 AI/hyperscaler mix、tariff、discounting 降到 60% 附近。
- Partner 反馈显示 Cloud Control adoption 主要是免费 enablement，客户不为 assessment、workflow、managed service 付费。

### 后续跟踪日历

| 时间 | 节点 | 需要刷新什么 |
|---|---|---|
| 2026-06-19 前后 | Cisco Live On-Demand Library 剩余 sessions 上线 | Data Center、Security、Campus/Branch、Splunk deep dive 的技术细节和 demo 参数 |
| 2026-07 | Quantum Ready Assessments 全球可用计划 | 是否按期上线；pricing/服务包/客户案例 |
| 2026-08 前后 | Cisco Q4 FY2026 earnings | AI infra orders/revenue、Networking/Security/Observability/Collaboration 增速、gross margin |
| 2026 Fall | Splunk Agent Builder planned GA on Splunk Cloud Platform | 是否 GA；是否有客户从 Alpha 转付费/生产 |
| 2026-09-14 至 2026-09-17 | Splunk .conf26 Denver | Machine Data Lake、Cisco Data Fabric、Agent Builder、AI Canvas 最新路线 |
| 2026-12 | Cisco majority core portfolio quantum-safe communications 承诺节点 | 覆盖产品范围、实际启用方式、客户采用 |
| 2027-02 | CCNA 2.0 exam go-live | AI/networking skills 生态是否形成 |
| 2027-03-23 | CCIE Automation v1.2 exam launch | AgenticOps/automation 能力是否进入高端认证体系 |
| 2027-06-06 至 2027-06-10 | Cisco Live 2027 Las Vegas | Cloud Control 是否从路线图变成默认生产平台 |

### 刷新频率

- Cisco/CSCO 投资跟踪：每季度财报后刷新一次，若 Q4 FY2026 数据大幅偏离则立即刷新。
- Cloud Control/Splunk product 跟踪：2026 年 7 月、9 月、12 月各刷新一次。
- Partner/channel 反馈：每 4-6 周抽样一次，重点问是否有付费 assessment/managed service，而不是只问 demo 热度。
- 竞争对手对照：Arista、Palo Alto、Datadog/Dynatrace、Microsoft/Zoom 财报后同步对比。

## 来源清单

### 一手官方：会议官网与会议材料

1. Cisco Live 2026 Las Vegas FAQ，日期页面显示会议为 2026-05-31 至 2026-06-04，地点 Las Vegas / Mandalay Bay Convention Center。来源类型：会议官方；可信度：高；一手验证：是。URL: https://www.ciscolive.com/global/faqs.html
2. Cisco Live 2026 Las Vegas Broadcast Agenda，2026-06-02 至 2026-06-04 免费全球 broadcast；keynotes、Center Stage、Keynote Deep Dive。来源类型：会议官方；可信度：高；一手验证：是。URL: https://www.ciscolive.com/global/attend/broadcast-agenda.html
3. Cisco Live 2026 Keynote Summaries，Opening Keynote/Wednesday Keynote 摘要；Cisco AI Assistant 生成。来源类型：会议官方但 AI 摘要；可信度：中高；一手验证：部分。URL: https://www.ciscolive.com/global/broadcast/keynote-summaries.html
4. Cisco Live 2026 Session Catalog，AI、Security、Campus & Branch、Data Center、Collaboration 为 Keynote Deep Dive 重点；Cisco AI Assistant 可用于 session planning。来源类型：会议官方；可信度：高；一手验证：是。URL: https://www.ciscolive.com/global/learn/session-catalog.html
5. Cisco Live 2026 Sponsor List，Premier sponsor WWT，Diamond sponsors Equinix、NetApp、NVIDIA。来源类型：会议官方；可信度：高；一手验证：是。URL: https://www.ciscolive.com/global/sponsor/sponsor-list.html
6. Cisco global events page，说明 Keynotes/Deep Dives/Center Stage 已上线，剩余 sessions by 2026-06-19 增加。来源类型：Cisco 官方；可信度：高；一手验证：是。URL: https://www.cisco.com/site/us/en/learn/events/index.html

### 一手官方：Cisco / Splunk / Webex 产品与公司材料

1. Cisco Newsroom, "Cisco Unveils Agentic Platform for Operating and Defending Critical IT Infrastructure", 2026-06-02。Cloud Control、Live Protect、Quantum Ready Assessments、Cisco IQ、50+ connectors/MCP、availability。来源类型：Cisco 官方新闻稿；可信度：高；一手验证：是。URL: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m06/cisco-unveils-agentic-platform-for-operating-and-defending-critical-it-infrastructure.html
2. Cisco Newsroom, "Cisco Live U.S.: Leading in the agentic AI age", 2026-06。Cloud Control、Cisco IQ、Live Protect、20,000+ customers/partners/analysts/press、product demos。来源类型：Cisco 官方；可信度：高；一手验证：是。URL: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m06/cisco-live-u-s-leading-in-the-agentic-ai-age.html
3. Cisco Newsroom, "Cisco Live 2026 keynotes: TL;DR edition", 2026-06。Cloud Control demo、zero trust、identity intelligence、AI guardrails、Codex。来源类型：Cisco 官方摘要；可信度：中高；一手验证：部分。URL: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m06/cisco-live-2026-keynotes-tldr-edition.html
4. Cisco Blogs, "Cisco Cloud Control: The Secure Harness for the Agentic Era", 2026-06-02。AI Canvas、Studio、App Builder、Agent Builder、Marketplace。来源类型：Cisco 官方博客；可信度：高；一手验证：是。URL: https://blogs.cisco.com/ai/cisco-cloud-control-the-secure-harness-for-the-agentic-era
5. Cisco Blogs, "Cisco Unveils Multicloud Fabric in Cloud Control", 2026-06。Multicloud Fabric through Cloud Control。来源类型：Cisco 官方博客；可信度：高；一手验证：是。URL: https://blogs.cisco.com/networking/cisco-unveils-multicloud-fabric-in-cloud-control-network-ready-for-the-ai-era
6. Cisco Blogs, "Security at Cisco Live: Going Shields Up for the Agentic Era", 2026-06。Cloud Control、AgenticOps、安全/身份/网络/基础设施共用 operating environment。来源类型：Cisco 官方博客；可信度：高；一手验证：是。URL: https://blogs.cisco.com/security/security-at-cisco-live-going-shields-up-for-the-agentic-era
7. Cisco Blogs, "Trust at machine speed: Building secure campus networks for the AI era", 2026-06。Cloud Control、AgenticOps、campus/branch。来源类型：Cisco 官方博客；可信度：高；一手验证：是。URL: https://blogs.cisco.com/networking/trust-at-machine-speed-building-secure-campus-networks-for-the-ai-era
8. Cisco Blogs, "Cisco Live 2026 Las Vegas: Explore AI and automation across the network", 2026-05。Meraki admin access automation、firmware automation sessions。来源类型：Cisco 官方博客；可信度：高；一手验证：是。URL: https://blogs.cisco.com/networking/cisco-live-2026-las-vegas-explore-ai-and-automation-across-the-network
9. Cisco Blogs, "How Cisco Cloud Control Changes the Partner Motion", 2026-06-02。无新增 license/no cost、Essential/Advantage tiers、year 1 adoption、years 2-3 Marketplace/IP。来源类型：Cisco 官方 partner 博客；可信度：高；一手验证：是。URL: https://blogs.cisco.com/partner/cisco-cloud-control-a-new-operating-layer-for-cisco-partners
10. Cisco Blogs, "Cisco Cloud Control: The opportunity for our partners", 2026-06-02。partner service、10 engineers/50-100 customer environments 示例、Marketplace 机会。来源类型：Cisco 官方 partner 博客；可信度：高；一手验证：是。URL: https://blogs.cisco.com/ai/cisco-cloud-control-the-opportunity-for-our-partners
11. Splunk Blog, "Accelerating the Agentic Enterprise: New Splunk Platform Innovations at Cisco Live Las Vegas 2026", 2026-06-02。Machine Data Lake Alpha、Agent Builder Fall 2026 GA、Autodesk/insurance examples。来源类型：Splunk 官方博客；可信度：高；一手验证：是。URL: https://www.splunk.com/en_us/blog/platform/new-splunk-platform-innovations-cisco-live-2026.html
12. Webex Blog, "Cisco Live 2026: Advancing Cisco Calling with AI, Hybrid Flexibility, and Resilience", 2026-06-03/04。Webex Calling 18M+ users、200+ markets、AI Agents for Collaboration、Cloud Control/AI Canvas integration。来源类型：Webex/Cisco 官方博客；可信度：高；一手验证：是。URL: https://blog.webex.com/collaboration/cisco-live-2026-advancing-cisco-calling-with-ai-hybrid-flexibility-resilience/
13. Cisco Blogs, "The Skills Payload: What's Landing at Cisco Live 2026", 2026-05-31。CCNA v2.0、CCIE Automation v1.2、Energy Networking Systems、Cisco Silicon One for AI Networking learning path。来源类型：Cisco 官方博客；可信度：高；一手验证：是。URL: https://blogs.cisco.com/learning/the-skills-payload-whats-landing-at-cisco-live-us-2026

### 一手官方：投资者材料

1. Cisco Investor Relations, "Cisco Reports Third Quarter Earnings", 2026-05-13。Q3 FY2026 收入 158 亿美元、orders、AI infra、campus/DC switching、gross margin、guidance、RPO、restructuring。来源类型：公司投资者材料；可信度：高；一手验证：是。URL: https://investor.cisco.com/news/news-details/2026/CISCO-REPORTS-THIRD-QUARTER-EARNINGS/default.aspx
2. Cisco Investor Relations overview，Q3 FY2026 press release/slides/webcast/10-Q 入口，Cisco 对 Silicon One、AI-native security、critical infrastructure for AI era 的投资者定位。来源类型：公司 IR；可信度：高；一手验证：是。URL: https://investor.cisco.com/overview/default.aspx

### 技术/市场材料

1. IDC, "Ethernet Switch Market Growth Driven by AI Demand", 2026 年公开文章。2025 Ethernet switch 市场 551 亿美元、4Q25 总市场 162 亿美元、4Q25 data center segment 99 亿美元。来源类型：市场研究机构公开摘要；可信度：中高；一手验证：二手市场数据。URL: https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/
2. Light Reading / Dell'Oro SASE forecast，2026 SASE 市场超过 130 亿美元、Gartner 2025 147 亿美元旧预测。来源类型：二手市场研究报道；可信度：中；一手验证：否。URL: https://www.lightreading.com/sd-wan/bolstered-by-security-demand-sase-market-to-surpass-13b-by-2026-report
3. Mordor Intelligence, UCaaS market 2026 estimate 705.6 亿美元、2031 2,211.4 亿美元。来源类型：市场研究公开摘要；可信度：中；一手验证：否。URL: https://www.mordorintelligence.com/industry-reports/unified-communication-as-a-service-ucaas-market
4. Mordor Intelligence, Observability market 2026 estimate 33.5 亿美元。来源类型：市场研究公开摘要；可信度：中；一手验证：否。URL: https://www.mordorintelligence.com/industry-reports/observability-market
5. Research Nester, Observability tools/platforms market 2026 estimate 341 亿美元。来源类型：市场研究公开摘要；可信度：中；一手验证：否。URL: https://www.researchnester.com/reports/observability-tools-and-platforms-market/8139
6. AudioCodes blog, UCaaS user counts including Webex Calling 18M+ users、Zoom Phone 10M+。来源类型：行业博客；可信度：中；一手验证：Webex 官方材料交叉验证 Webex 18M+。URL: https://www.audiocodes.com/blog/the-5-ucaas-trends-set-to-shape-2026

### 非官方分享和二手分析

1. Presidio, "Cisco Live 2026: The Agentic Era Has Arrived", 2026-06。对 Cloud Control、AI Canvas、quantum readiness、acquisition stack 的 partner 解读。来源类型：Cisco partner 非官方/二手分析；可信度：中；一手验证：核心事实已由 Cisco 官方交叉验证，观点降权使用。URL: https://www.presidio.com/blogs/cisco-live-2026-the-agentic-era-has-arrived/
2. TechTarget, "Cisco advances AI infrastructure services at Cisco Live", 2026-06-09。对 AI-ready data centers、digital resilience、Cloud Control 的 analyst 解读。来源类型：二手分析；可信度：中；一手验证：部分。URL: https://www.techtarget.com/searchnetworking/opinion/Cisco-advances-AI-infrastructure-services-at-Cisco-Live
3. Futurum Group, "Cisco Live 2026: Platform, Silicon, and Security for the Agentic Era", 2026-06-08。对 Cisco Live 2026 平台、silicon、安全的 analyst take。来源类型：二手分析；可信度：中；一手验证：观点降权使用。URL: https://futurumgroup.com/insights/cisco-live-2026-platform-silicon-and-security-for-the-agentic-era/
4. Techstrong TV Cisco Live 2026 video index，2026-06-05 至 2026-06-08 包括 Cisco AI Infrastructure、Cloud Control、Splunk Data Fabric、Security 等会后访谈入口。来源类型：公开视频/访谈索引；可信度：中低；一手验证：未逐条转录，作为非官方线索。URL: https://techstrong.tv/videos/cisco-live-2026
