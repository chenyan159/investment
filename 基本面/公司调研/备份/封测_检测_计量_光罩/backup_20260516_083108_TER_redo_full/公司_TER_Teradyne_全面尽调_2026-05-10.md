# TER / Teradyne, Inc. 全面尽调（2026-05-16 重做版）

撰写日期：2026-05-16 PDT。  
股票代码：NASDAQ: TER。  
分类目录：封测_检测_计量_光罩。  
研究边界：按公司调研目录流程重新做，不把旧版正文作为事实来源直接沿用；旧版已备份到本目录 备份/backup_20260516_0114_TER_redo/。本报告用 Teradyne 官方 Q1 2026 与 FY2025 新闻稿、SEC 10-Q 索引、2026 年产品/并购公告、Stooq 2026-05-15 收盘行情，以及项目内 ATE/HBM/先进封装/催化剂/可比公司研究交叉验证。金额默认美元，收入单位未注明时为百万美元。本文仅为研究，不构成投资建议。

## 0. 一页结论

Teradyne 现在不是普通半导体测试周期股，而是 AI 数据中心硬件复杂度上升的测试平台受益者。公司传统强项是 SoC ATE、Memory ATE、Product Test 和 Robotics；2025-2026 年投资逻辑已经迁移到 AI GPU/ASIC、HBM、224G/高速互连、硅光/CPO、AI 服务器板级测试和测试软件。

最新官方证据很强：Teradyne 2026Q1 收入 1,282.5M，同比 +87%，创历史新高；其中 Semiconductor Test 1,111M，占收入 86.6%；公司 CEO 明确说约 70% 收入与 AI-related demand 相关。Q2 2026 指引收入 1,150M-1,250M，Non-GAAP EPS 1.86-2.15。Q1 和 Q2 中点合计约 2.482B，如果管理层口径 H1 占全年 55%-60% 成立，隐含 2026 全年收入约 4.14B-4.51B，同比 2025 年 3.190B 增长约 30%-41%。

估值也已经非常高：Stooq 显示 2026-05-15 TER 收盘 337.88，较 5/8 的 359.77 回落约 -6.1%。用 2026Q1 稀释股数 157.6M 粗算，权益价值约 53.3B。TTM 收入约 3.787B，P/S 约 14.1x；TTM GAAP 净利润约 854M，P/E 约 62x；若按市场 forward PE 约 50x 左右，市场已经把 2026-2027 AI 测试增长前置定价。

投资判断：TER 是 AI 半导体测试链里质量最高的进攻仓之一，但不是低风险核心仓。核心买点是 AI SoC + HBM + 高速互连 + CPO/硅光 + board/system test 的多点扩张；核心风险是 2026H1 收入过于前置、H2 订单接续不够、Advantest 抢份额、Robotics 继续拖累、应收账款和自由现金流节奏恶化。回调后可以研究，但必须用订单、lead time、Q2/Q3 指引和现金流确认，不能只看 AI 叙事。

## 1. 公司业务、产业链位置、三年变化、估值与财务健康

### 1.1 业务概览

Teradyne 设计、制造和销售自动化测试设备 ATE、电子系统测试平台和先进机器人。按 2026Q1 披露，公司收入分三块：

| 板块 | 2026Q1 收入 | 占比 | 2025 收入 | 战略含义 |
|---|---:|---:|---:|---|
| Semiconductor Test | 1,111M | 86.6% | 2,524M | AI SoC、GPU/ASIC、networking ASIC、HBM/DRAM、SLT/IST 的核心平台 |
| Product Test | 80M | 6.3% | 358M | PCBA、AI data center board/sub-assembly、高速互连、硅光/CPO、无线/国防电子 |
| Robotics | 91M | 7.1% | 308M | Universal Robots 与 MiR，制造/仓储自动化；对 TER 当前估值不是主驱动 |
| 合计 | 1,282M | 100% | 3,190M | Q1 约 70% 收入与 AI 相关 |

Teradyne 的产业链位置是“质量门”和“良率税”：AI accelerator、HBM、chiplet、CPO/硅光和 AI 服务器板卡价值越来越高，任何一个坏 die、坏 stack、坏 package、坏板卡或高速互连缺陷都可能造成高额报废和现场失效。测试强度随芯片价值、HBM stack 数、SerDes 速度、封装复杂度和系统功耗非线性上升。

### 1.2 投资人心智变化

| 阶段 | 市场标签 | 估值核心变量 |
|---|---|---|
| 2021-2023 | 手机/汽车/工业 SoC ATE + Robotics 可选成长 | 半导体周期、手机 SoC、汽车电子、机器人利润率 |
| 2024-2025H1 | 半导体测试复苏 + HBM/AI 早期受益 | HBM 订单、AI accelerator 测试是否能抵消传统下行 |
| 2025H2-2026 | AI 数据中心测试平台 | AI SoC/HBM/224G/CPO/board/system test 的收入持续性和毛利率 |
| 2027 观察 | 从 wafer 到 data center 的测试数据平台 | 测试软件、硅光/CPO、rack/system test 是否成为第二曲线 |

### 1.3 最近三年重大变化

| 时间 | 事件 | 对 TER 的意义 |
|---|---|---|
| 2024-05 | 投资 Technoprobe 约 10% 股权 | 绑定高端 probe card / wafer probe 生态，补强 AI/HBM 测试接口 |
| 2025 | AI compute 成为 SoC 业务最大增量 | TER 从传统 SoC tester 转为 AI GPU/ASIC 量产测试受益者 |
| 2025-05 | 收购 Quantifi Photonics | 补齐 PIC、硅光、光电混合测试能力 |
| 2026-01 | 与 MultiLane 成立 MLTP JV | 面向 AI 数据中心高速 I/O 和互连测试，从 wafer 延伸到 system |
| 2026-03 | 发布 Omnyx | 针对 AI/data center PCBA 与 sub-assembly，整合结构、参数、高速互连和功能测试 |
| 2026-03 | 发布 Photon 100 | 面向硅光和 CPO 的 opto-electric automated test，覆盖 wafer、optical engine、CPO module 插入点 |
| 2026-04 | 收购 TestInsight | 强化 test program、pattern conversion、pre-silicon validation 和设计到测试软件流 |
| 2026Q1 | 收入 1.282B，约 70% AI 相关 | AI 测试主线从叙事转为财务结果 |

### 1.4 最新股价、估值与利润率

| 指标 | 数值 | 日期/口径 | 解读 |
|---|---:|---|---|
| 股价 | 337.88 | Stooq，2026-05-15 收盘 | 当日高 346.59、低 335.32、成交量 4.25M |
| 较 5/8 股价 | -6.1% | 359.77 到 337.88 | 半导体去杠杆中回调，但估值仍高 |
| 稀释股数 | 157.6M | 2026Q1 官方稀释股数 | 粗算市值使用该口径 |
| 权益价值 | 约 53.3B | 337.88 x 157.6M | 与净现金差距不大 |
| TTM 收入 | 约 3.787B | FY2025 3.190B + Q1 1.282B - 2025Q1 0.686B | 过去 12 个月收入已被 Q1 拉高 |
| TTM P/S | 约 14.1x | 市值 / TTM 收入 | 对测试设备公司属于高估值 |
| TTM GAAP 净利润 | 约 854M | FY2025 554.0M + Q1 398.9M - 2025Q1 98.9M | Q1 利润率极高 |
| TTM P/E | 约 62x | 市值 / TTM 净利润 | 已反映 AI 成长预期 |
| Forward PE | 约 50x | 参考 5/8 forward PE 约 53.7x、股价回落后估算 | 要求 2026-2027 持续兑现 |
| Q1 GAAP 毛利率 | 60.9% | 780.9M / 1,282.5M | AI mix 和规模杠杆显著 |
| Q1 GAAP 营业利润率 | 36.9% | 473.0M / 1,282.5M | Semiconductor Test 放量带来高杠杆 |
| Q1 GAAP 净利率 | 31.1% | 398.9M / 1,282.5M | 高峰季度利润率，不宜线性外推 |

### 1.5 资产负债表

| 项目 | 2026Q1 | 2025 年末 | 判断 |
|---|---:|---:|---|
| 现金及等价物 | 241.9M | 293.8M | Q1 偿还短债后现金下降 |
| 流动有价证券 | 3.7M | 28.2M | 小项 |
| 长期有价证券 | 148.4M | 126.3M | 现金缓冲补充 |
| 应收账款 | 1,107.5M | 786.9M | 强出货后显著上升，是现金流重点观察项 |
| 存货 | 362.8M | 379.6M | 收入高增但库存下降，周转改善 |
| 流动资产 | 2,173.2M | 1,949.3M | 健康 |
| 流动负债 | 1,012.2M | 1,115.2M | 短债已清零 |
| 短期债务 | 0 | 200.0M | Q1 已偿还 |
| 总负债 | 1,290.0M | 1,387.8M | 低杠杆 |
| 股东权益 | 3,143.8M | 2,795.8M | 盈利推动提升 |
| 经营现金流 | 265.1M | 2026Q1 | 尽管 A/R 增加，仍强劲为正 |

财务健康结论：资产负债表健康，短债清零，流动比率约 2.15x，经营现金流为正。真正风险不是偿债，而是收入前置后 A/R 回款、客户验收、H2 订单接续和高估值回撤。

## 2. 最近五个季度财报、订单、交期和 AI 占比

### 2.1 五季总表

| 季度 | 收入 | YoY / QoQ | GAAP EPS | Non-GAAP EPS | 分部收入 | AI 相关占比 | 订单/交期线索 |
|---|---:|---:|---:|---:|---|---:|---|
| 2026Q1 | 1,282M | +87% / +18% | 2.53 | 2.56 | Semi Test 1,111；Product Test 80；Robotics 91 | 约 70% | 官方称 wafer to AI data center 策略兑现；Q2 指引仍高 |
| 2025Q4 | 1,083M | +44% / +41% | 1.63 | 1.80 | Semi Test 883；Product Test 110；Robotics 89 | 高，未给精确 | AI compute、networking、memory 强；Q1 指引 1.15B-1.25B |
| 2025Q3 | 769M | 约 +5% / +18% | 0.75 | 0.85 | Semi Test 606；Product Test 88；Robotics 75 | 中高 | Q4 指引强，显示 AI/HBM 订单开始兑现 |
| 2025Q2 | 652M | 约 -11% / -5% | 0.43 | 0.57 | Semi Test 492；Product Test 85；Robotics 75 | 上升中 | 客户推迟和贸易不确定性仍有影响，但 AI compute forecast 转订单 |
| 2025Q1 | 686M | +14% / -9% | 0.61 | 0.75 | Semi Test 543；Product Test 74；Robotics 69 | 未披露 | HBM 客户消化前期产能，AI compute SLT 开始出现 |

### 2.2 分部利润率与经营杠杆

| 项目 | 2025 全年 | 2026Q1 | 变化 |
|---|---:|---:|---|
| 公司收入 | 3,190M | 1,282M 单季 | Q1 已达 2025 全年 40.2% |
| 公司 GAAP 毛利率 | 58.2% | 60.9% | AI mix 提升 |
| 公司 GAAP 营业利润率 | 20.4% | 36.9% | Semi Test 放量带来强杠杆 |
| Semiconductor Test 收入 | 2,524M | 1,111M | Q1 单季等于 2025 全年 44.0% |
| Product Test 收入 | 358M | 80M | 稳定但不是主驱动 |
| Robotics 收入 | 308M | 91M | 同比恢复，但利润弹性仍需观察 |

### 2.3 Backlog、bookings、lead time、取消率

Teradyne 不披露传统意义上可直接外推的 backlog/bookings 明细。SEC/公司风险提示也强调 backlog 可能被推迟或取消，因此本报告不用“虚构 backlog”作为结论。

| 项目 | 可验证事实 | 研究判断 |
|---|---|---|
| Backlog | 未按产品披露；公司提醒 backlog 对未来销售的代表性有限 | 不能把未披露订单当成确定收入 |
| Q2 指引 | 1,150M-1,250M，Non-GAAP EPS 1.86-2.15 | 说明 Q1 强度不是一次性，但 Q2 环比中点下降 |
| H1/全年节奏 | Q1+Q2 中点约 2.482B；若 H1 为全年 55%-60%，全年约 4.14B-4.51B | H2 可能低于 H1，必须看 Q3 指引是否接棒 |
| 需求来源 | 官方称约 70% Q1 收入与 AI 相关 | AI compute/HBM 是主因，不是传统手机周期 |
| 交期 | 旧版与项目内资料显示 UltraFLEXplus 交期约 12-16 周 | 供给紧但未完全失控，设备收入可能呈块状确认 |
| 取消率 | 未披露明确取消率 | AI 项目更可能推迟而非取消；估值对推迟也敏感 |
| A/R | Q1 A/R 增至 1.108B | 强出货后要看 Q2/Q3 回款和验收 |

## 3. 2026 指引、业务收入占比和产品映射

### 3.1 Q2 2026 指引和全年隐含

| 指标 | Q2 2026 指引 | 含义 |
|---|---:|---|
| 收入 | 1,150M-1,250M | 中点 1,200M，环比 Q1 -6.4%，但同比仍很强 |
| GAAP EPS | 1.83-2.12 | 盈利仍高 |
| Non-GAAP EPS | 1.86-2.15 | 中点 2.005 |
| H1 合计收入 | 约 2.482B | 按 Q2 中点 |
| 隐含全年收入 | 约 4.14B-4.51B | 若 H1 占全年 55%-60% |
| 隐含全年增速 | 约 +30%-41% | 相比 2025 年 3.190B |

### 3.2 产品与业务映射

| 业务 | 重点产品/技术 | 对应需求 | 重要性 |
|---|---|---|---|
| AI compute / networking SoC ATE | UltraFLEXplus、UltraPHY 112G/224G、IG-XL、TestInsight | GPU、custom ASIC、networking ASIC、CPU/XPU、SerDes、PCIe/CXL/UCIe | 最高 |
| Memory / HBM ATE | Magnum 7、Magnum 7H | HBM3E、HBM4、DRAM、KGD、stack/performance test | 最高 |
| IST / SLT | Titan HP、system-level test | 高价值 AI package 的 burn-in、mission-mode、可靠性测试 | 高 |
| Silicon photonics / CPO test | Photon 100、Quantifi Photonics | SiPh wafer、optical engine、CPO module、co-packaged optics | 高潜力 |
| Board / system test | Omnyx、Production Board Test | AI data center PCBA、sub-assembly、高速互连、功能测试 | 高潜力 |
| High-speed interconnect | MLTP / MultiLane Test Products | 224G/未来 448G、高速 I/O、data center interconnect | 高潜力 |
| Test software | TestInsight、pattern conversion、pre-silicon validation | AI 芯片复杂测试程序开发、缩短 debug 和 ramp | 高毛利期权 |
| Robotics | Universal Robots、MiR | 制造/仓储自动化，少量 AI 应用 | 中，非主线 |

### 3.3 可低权重处理的业务

| 业务 | 原因 |
|---|---|
| 传统手机 SoC ATE | 仍重要，但不是 2026 重估核心；受消费电子周期影响 |
| 传统汽车/工业测试 | 稳定但增速慢，AI 数据中心关联较弱 |
| 普通无线测试 | LitePoint 有稳定价值，但不是 TER 估值主因 |
| 国防航天电子测试 | 利基稳定，规模不够改变主线 |
| 传统 Robotics | 渠道恢复有价值，但利润率和 AI 纯度弱于 Semi Test |

## 4. 高增长关键产品：当前贡献、增长、重要性、供需和定价权

| 产品/业务 | 当前收入贡献估算 | 增长证据 | AI 重要性 | 供需紧张 | 垄断/溢价能力 |
|---|---:|---|---:|---:|---|
| AI SoC ATE | Q1 SoC/compute 是 Semi Test 主体，估算 650M-800M | Q1 Semi Test 1,111M，AI 相关收入约 70% 公司收入 | 5/5 | 4/5 | 4/5 |
| Memory/HBM ATE | Q1 约 200M 左右量级 | HBM/DRAM 需求拉动；项目内 HBM 测试设备为最强主线之一 | 5/5 | 4/5 | 4/5 |
| IST/SLT | 当前小于 SoC/HBM，几十 M 量级 | 高价值 package 的 system-level test 需求提升 | 4/5 | 4/5 | 3/5 |
| Photon 100 / CPO | 2026 仍早期，工程/NPI 量级 | 官方 2026-03 发布，覆盖 wafer、optical engine、CPO module | 4/5 | 3/5 | 4/5 |
| Omnyx board test | 2026 早期 | 官方定位 AI/data center PCBA 和 sub-assembly | 4/5 | 3/5 | 3/5 |
| MLTP 高速互连测试 | 2026H1 JV 成立阶段 | 官方称从 wafer level 到 data center 支持高速连接测试 | 4/5 | 3/5 | 3/5 |
| TestInsight 软件 | 收入小，但战略价值高 | 官方称用于 AI/data center device 的 test program 和 validation | 4/5 | 3/5 | 4/5 |
| Robotics AI 应用 | Q1 Robotics 91M，AI 应用仅部分 | Robotics 同比 +32%，但不是主驱动 | 2/5 | 2/5 | 2/5 |

## 5. 一年后收入情景：产品维度

### 5.1 基准、乐观、极度乐观

| 产品/业务 | 基准：一年后收入贡献 | 乐观：一年后收入贡献 | 极度乐观：一年后收入贡献 | 关键条件 |
|---|---:|---:|---:|---|
| AI SoC ATE | 2.4B-2.8B 年化 | 3.0B-3.5B | 3.8B+ | GPU/ASIC 客户继续扩产，H2 订单接续 |
| Memory/HBM ATE | 0.7B-0.9B | 1.0B-1.3B | 1.5B+ | HBM3E 维持高产能，HBM4 NPI 提前转量产 |
| IST/SLT | 0.15B-0.25B | 0.30B-0.45B | 0.60B+ | 高功耗 AI package 和 rack/system burn-in 渗透 |
| Photon 100 / CPO | 0.03B-0.08B | 0.10B-0.20B | 0.30B+ | CPO/SiPh 从工程导入到小批量 HVM |
| Omnyx / board test | 0.10B-0.15B | 0.20B-0.35B | 0.50B+ | AI server board 与 sub-assembly 测试被 ODM/EMS 批量采用 |
| MLTP / high-speed I/O | 0.05B-0.12B | 0.15B-0.30B | 0.45B+ | 224G/448G 互连测试成为量产瓶颈 |
| TestInsight / software | 低双位数 M | 50M-100M | 150M+ | ATE 流程绑定、订阅/授权模式扩大 |
| Robotics | 0.35B-0.45B | 0.50B-0.65B | 0.80B+ | 渠道恢复、AI 应用和大客户 program of record 落地 |

### 5.2 公司整体收入情景

| 情景 | 2026-2027 收入路径 | 增速判断 | 估值含义 |
|---|---:|---|---|
| 基准 | 2026 约 4.2B-4.5B，2027 约 4.5B-5.0B | 2026 高增，2027 放缓 | 当前估值基本合理但上行有限 |
| 乐观 | 2026 约 4.6B-5.0B，2027 约 5.5B-6.2B | AI SoC/HBM/CPO 接力 | 可支撑高 P/S，但要靠 Q3/Q4 订单确认 |
| 极度乐观 | 2026 >5.0B，2027 >7.0B | 多家 GPU/ASIC/HBM4/光互连同时扩产 | 当前估值仍有上修空间，但执行门槛很高 |

## 6. BOM、每 MW / rack / GPU / optical port 内容量与价格传导

TER 不披露每客户、每 GPU、每 rack 的真实设备内容量。以下为研究框架，不作为公司披露事实。

| 维度 | 测试内容 | TER 可能捕获 | 传导逻辑 |
|---|---|---|---|
| 每 GPU / ASIC | wafer sort、final test、SerDes、HBM attach 前后验证、SLT | AI SoC ATE、IST/SLT、TestInsight | 芯片价值越高、面积越大、HBM 越多，测试时间越长 |
| 每 HBM stack | KGD、speed bin、thermal、stack-level validation | Memory ATE、Magnum 7/7H | HBM3E/HBM4 需要更高并行、更高功率和更严良率筛选 |
| 每 optical port | 光电参数、BER、jitter、温漂、CPO module | Photon 100、Quantifi、MLTP | 1.6T/3.2T 和 CPO 使电光共测变成量产问题 |
| 每 board / tray | 结构、参数、高速互连、mission-mode functional test | Omnyx、Product Test | AI 服务器板卡价值高，早发现缺陷可减少整机报废 |
| 每 rack / system | burn-in、power transient、firmware、互连、热失效 | IST/SLT、board/system test、MLTP | Rack 价值几十万到数百万美元，field failure 成本极高 |
| 每 MW | 高密度 AI racks 对应更多 GPU/HBM/光口/板卡 | 间接捕获 | TER 不是电力设备商，但每 MW 算力密度上升会放大测试需求 |

价格传导：云厂 capex 和 AI 芯片项目预算先流向 NVDA/ASIC/HBM/封装/系统厂，再由 foundry、OSAT、IDM、ODM、EMS 采购 ATE、handler、probe、SLT、board test 和软件。TER 的收入不按“每台 GPU 固定 royalty”计，而按客户测试产能扩建和平台导入节奏确认。

## 7. 产能、采纳程度、认证阶段

| 产品 | 当前产能/采纳 | 认证阶段 | 一年后基准 | 一年后乐观 | 一年后极度乐观 |
|---|---|---|---|---|---|
| UltraFLEXplus / AI SoC | 已大规模量产，Q1 收入强 | 多个 AI compute/networking 客户量产 | 维持高利用率 | 新 GPU/ASIC 客户扩散 | 成为更多 merchant GPU/custom ASIC 标准平台 |
| Magnum 7 / 7H | HBM/DRAM 量产导入 | HBM3E 强，HBM4 NPI | HBM3E 持续 | HBM4 转早期量产 | HBM4 大规模提前 |
| IST/SLT | 已有 AI accelerator 应用 | 客户/平台逐步认证 | 高端 package 渗透提升 | ODM/OSAT 批量扩产 | Rack/system 数据闭环绑定 |
| Photon 100 | 新发布，2026 工程导入 | SiPh/CPO 客户验证 | 小批量工程收入 | 高端 CPO/SiPh HVM 初步采用 | 进入多客户量产流程 |
| Omnyx | 新发布，AI board test | ODM/EMS/系统厂验证 | 小批量导入 | AI server board 批量采用 | 成为 AI board test 新平台 |
| MLTP | JV 预计 2026H1 close | 高速 I/O 客户导入 | 产品整合 | 224G test 扩大 | 448G/下一代互连提前 |
| TestInsight | 已收购 | ATE 软件生态整合 | 内部工具+客户保留 | 形成设计到测试绑定 | 软件收入和平台粘性显著提高 |

## 8. 未来一年业务增速预测：订单积压与供给视角

| 情景 | 关键假设 | 收入增速 | 风险 |
|---|---|---:|---|
| 基准 | Q1/Q2 强，H2 有消化；AI SoC/HBM 继续但不再加速 | 2026 +30%-41% | H2 环比走弱被市场解读为周期见顶 |
| 乐观 | 新 GPU/ASIC、HBM4、CPO/SiPh、Omnyx/MLTP 在 H2 接棒 | 2026 +45%-55%，2027 继续双位数高增 | 需要多个客户项目同时成功 |
| 极度乐观 | OpenAI/Broadcom XPU、Rubin/MI400/TPU8/HBM4/224G/CPO 全部提前锁测试产能 | 2026 +60% 以上，2027 继续高增 | 估值上修但供应链执行风险也最高 |

最需要盯的不是静态 backlog，而是以下五个信号：

1. Q2 实际收入是否靠近或超过 1.25B 上沿。
2. Q3 指引是否能证明 H2 不断档。
3. Deferred revenue/customer advances 是否继续上升，且 A/R 能正常回款。
4. AI SoC/HBM 以外的 Photon 100、Omnyx、MLTP、TestInsight 是否出现客户量产/设计赢单。
5. Advantest 是否在高端 AI/HBM tester 中拿走更多增量份额。

## 9. 竞争格局、替代方案和客户替换成本

| 领域 | TER 主要竞争对手 | TER 优势 | TER 风险 |
|---|---|---|---|
| SoC ATE | Advantest V93000、Cohu、Chroma、SPEA、国产 ATE | UltraFLEXplus、IG-XL 生态、客户程序资产、全球服务 | Advantest 在高端 AI/HPC 与 HBM 周期中极强 |
| Memory/HBM ATE | Advantest、Chroma、国产存储 tester | Magnum 平台、HBM/DRAM know-how | HBM 客户可能多供应商化 |
| Probe/interface | FormFactor、Technoprobe、MJC、JEM、MPI 等 | 投资 Technoprobe、平台协同 | TER 不直接拥有完整 probe card 价值池 |
| Handler/SLT/burn-in | Cohu、Chroma、Aehr、Advantest、OSAT 自建 | 从 ATE 到 SLT/board/system 的组合 | 高功耗 thermal/handler 不是 TER 单独最强项 |
| 硅光/CPO test | Keysight、FormFactor、Chroma、Aehr、专用光测厂 | Photon 100 + UltraFLEXplus + Quantifi | CPO 大规模商业化时间不确定 |
| Board/system test | Keysight、NI/Emerson、Chroma、专用 ICT/functional test 厂 | Omnyx 针对 AI/data center 板卡重新定义测试 | ODM/EMS 可能使用自建或多供应商方案 |
| Test software | PDF Solutions、proteanTecs、Advantest ACS、客户自研 | TestInsight 连接设计到 ATE | 软件商业模式和独立收入仍需验证 |
| Robotics | ABB、Fanuc、Yaskawa、KUKA、MiR/UR 竞争者 | 协作机器人品牌和渠道 | 利润率、增长和 AI 相关性仍不足 |

客户替换成本较高，原因是测试程序、correlation、debug、yield learning、operator training、handler/prober/socket/interface、客户认证和量产数据都绑定平台。但替换并非不可能：新一代 GPU/ASIC/HBM4/CPO 项目如果重新做 NPI，客户会重新评估 Advantest、TER、Keysight、Chroma、Cohu 等组合。

## 10. 催化剂与风险

### 10.1 正面催化剂

| 催化剂 | 触发阈值 | 读穿 |
|---|---|---|
| Q2 2026 beat | 收入超过 1.25B 或 Non-GAAP EPS 超 2.15 | Q1 不是一次性，全年收入上修 |
| Q3 指引强 | Q3 收入高于市场担忧，H2 不断档 | H1 前置风险下降 |
| AI SoC 新客户 | merchant GPU/custom ASIC 多系统订单扩大 | TER 从单一客户/单一项目扩散 |
| HBM4 认证 | Magnum 7H/HBM4 NPI 转量产 | Memory ATE 第二轮上行 |
| Photon 100 客户 | SiPh/CPO 量产客户确认 | 2027 第二曲线提前 |
| Omnyx/MLTP design win | AI board/system/high-speed I/O 量产导入 | Product Test 从小业务变成 AI data center 延伸 |
| TestInsight 货币化 | 软件被打包进 ATE flow，缩短客户 ramp | 毛利率和客户粘性提升 |

### 10.2 负面风险

| 风险 | 影响 |
|---|---|
| H1 收入前置，H2 无接续 | 高估值最怕“增长见顶”叙事 |
| Advantest 抢份额 | AI/HBM tester 增量可能不全归 TER |
| AI capex 或 custom ASIC 项目推迟 | 测试设备订单会被推迟，哪怕不是取消 |
| A/R 和现金流恶化 | Q1 A/R 已大幅上升，需要回款验证 |
| Robotics 继续拖累 | 非核心业务占用管理层和费用 |
| CPO/SiPh 量产慢 | Photon 100 可能停留在工程收入 |
| 出口管制/中国限制 | 高端 semiconductor test 受政策影响 |
| 估值压缩 | 10Y/实际利率上行时，高 P/S 进攻仓优先被杀倍数 |

## 11. 投资分层结论

| 维度 | 结论 |
|---|---|
| 质量 | 高。AI 测试链条中少数收入已兑现、利润率高、平台粘性强的公司 |
| 弹性 | 高。AI SoC/HBM/CPO/board/system test 多条线都可能扩张 |
| 确定性 | 中高。Q1/Q2 强，但 H2 接续是最大问题 |
| 估值 | 高。337.88 美元仍约 14x TTM sales、62x TTM PE |
| 仓位属性 | 进攻仓，不是低估值核心仓 |
| 最佳买点 | 宏观利率稳定、Q2/Q3 指引确认 H2 不断档、股价回撤但订单不坏 |
| 应避免情形 | 只因股价跌就买；如果 Q3 指引弱或 A/R/现金流恶化，应等新证据 |

一句话排序：TER 是 AI 半导体测试中最值得认真跟踪的高 beta 标的之一；比纯 CPO/小盘测试题材更有收入兑现，比 ASML/KLAC/TSM 这类核心资产风险更高。当前研究结论是“基本面强、估值高、等待 H2 订单确认”。

## 12. 主要来源与研究限制

### 官方与外部来源

- Teradyne Reports First Quarter 2026 Results，2026-04-28：收入 1.282B、Semi Test 1.111B、Product Test 80M、Robotics 91M、约 70% AI 相关、Q2 指引。
- Teradyne Reports Fourth Quarter and Full Year 2025 Results，2026-02-02：Q4 收入 1.083B、FY2025 收入 3.190B、Q1 指引。
- Teradyne Acquires TestInsight，2026-04-16：test development、validation、pattern conversion、AI/data center time-to-market。
- Teradyne Introduces Photon 100，2026-03-17：SiPh/CPO opto-electric automated test，wafer、optical engine、CPO module。
- Teradyne Introduces Omnyx，2026-03-16：AI/data center PCBA 和 sub-assembly test。
- Teradyne and MultiLane Announce Formation of MLTP，2026-01-29：AI data center high-speed interconnect test。
- SEC EDGAR 10-Q 索引：TER 2026Q1 10-Q accession 0001193125-26-201058，period 2026-03-29，filed 2026-05-01。
- Stooq TER.US：2026-05-15 close 337.88，volume 4,251,855。

### 项目内来源

- 行业调研/晶圆制造_设备_材料_测试/行业调研_探针卡_ATE与系统级测试_2026-05-08.md。
- 行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-05-08.md。
- 行业调研/晶圆制造_设备_材料_测试/行业调研_高速互连与光学验证测试_2026-05-08.md。
- 行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026.md。
- 股票基本面和价格历史研究/催化剂日历/半导体财报催化剂_NVDA_TSM_AVGO_MU_ASML_KLAC.md。
- 股票基本面和价格历史研究/催化剂日历/个股催化剂矩阵.md。
- 可比公司：ONTO、FORM、COHU、CAMT、AMKR 等公司调研文件。
- 指标回归/合并指标_170家公司全指标_2026-05-11.md 与股价变动文件，用于历史口径参考；最新股价以 2026-05-15 Stooq 为准。

### 数据限制

Teradyne 没有披露按 AI 客户、GPU/ASIC 项目、HBM 客户、Photon 100、Omnyx、MLTP、TestInsight 的独立收入、订单、backlog、lead time、取消率、每 GPU/每 rack/每 optical port 内容量。因此本报告中涉及产品收入贡献、BOM/单位内容量和一年后情景的部分均为研究估算，已经和官方披露事实分开处理。
