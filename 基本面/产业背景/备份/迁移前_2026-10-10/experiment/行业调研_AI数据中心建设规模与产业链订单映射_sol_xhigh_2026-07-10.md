# AI数据中心建设规模与产业链订单映射（2026-2027，美国主导）

报告日期：2026-07-10（America/Los_Angeles）  
主要数据日期：2025-12-31 至 2026-07-09；公司最新季报主要截至 2026-03-31/2026Q1，个别产品与订单公告截至 2026-07-09  
估值/股价快照日期：2026-07-10 美股收盘；本报告不以估值作为规模模型输入  
方案版本：2026-06-04  

> **核心结论摘要：**本报告估算美国 AI 数据中心建设规模在 2026 年为悲观 `$300-360B`、务实 `$390-470B`、乐观 `$500-610B`；2027 年分别为 `$360-430B`、`$500-620B`、`$680-840B`。务实情景对应新增 AI IT load 约 `7.5-10.5GW` 与 `10.0-14.0GW`，综合 CapEx 强度约 `$42-58M/MW` 与 `$43-60M/MW`。2026 最大硬约束由 HBM/先进封装逐步转向**可按期获得的电力、变压器/switchgear、MEP 劳动力与液冷系统级验收**；2027 最大订单弹性来自自备电/微电网、1.6T/CPO、Rubin/定制 ASIC、HBM4、AI-native storage 与液冷。最确定的订单池是长交期电力设备、已预租的 EPC/MEP、已签 GPU/AI 系统 backlog；最大 beta 是 compute、网络、液冷与自备电；伪受益主要是没有数据中心 backlog、客户认证或产能兑现证据的泛电气/泛建筑/泛软件公司。

> **重要口径提示：**所有区间为本报告估算，不是公司指引。模块表采用“终端 CapEx 的经济内容”口径：GPU/ASIC、HBM、先进封装分别拆出，避免把同一颗 GPU 的完整售价同时计入 compute、HBM 和 CoWoS。订单子表中标注“子集”的行不可相加。区间端点来自独立敏感性组合，逐行低端或高端不应机械求和。

## 一、结论先行：总规模、最大瓶颈和最大订单弹性

### 1.1 美国 AI 数据中心建设总规模

| 年份 | 悲观 | 务实 | 乐观 | 务实同比中枢 | 置信度 |
|---|---:|---:|---:|---:|---|
| 2026（美国） | `$300-360B` | **`$390-470B`** | `$500-610B` | 约 `+25-35%` | 中高 |
| 2027（美国） | `$360-430B` | **`$500-620B`** | `$680-840B` | 约 `+27-34%` | 中 |

**为什么高于旧市场直觉。**截至 2026Q1/2026Q3 财年披露，Microsoft 给出 calendar 2026 CapEx 约 `$190B`，Amazon 的 2026 CapEx 计划约 `$200B`，Alphabet 为 `$175-185B`，Meta 为 `$125-145B`；Oracle FY2026 已发生 CapEx `$55.7B`，并以客户预付款/客户供货 GPU 降低现金融资压力。[R1-R5] 五者合计已达约 `$746-776B`（Oracle 仅用已发生 FY2026 数字），但其中含海外、非 AI、物流/办公、传统云、价格上涨和重复租赁，因此本报告只将约 `43-54%` 转化为 2026 美国 AI 建设，再加独立 NeoCloud/AI Factory/landlord-funded 部分并扣除重叠。

### 1.2 最大瓶颈、最高确定性与最大弹性

| 结论层 | 2026 | 2027 | 可验证指标 |
|---|---|---|---|
| 最大系统瓶颈 | 电力接入、变压器/switchgear、MEP 排期、142kW 级 rack 液冷验收 | 电力/发电机 slot、HBM4/大尺寸封装、1.6T 光学良率、现场调试 | utility service agreement、lead time、book-to-bill、rack acceptance |
| 确定性最高（alpha） | 变配电、UPS/busway、已预租 EPC/MEP、GB300/Rubin 供应链 | 同上，加燃气/燃料电池、HBM4、tester、AI storage | backlog、预付款、pre-lease、产能锁定 |
| 订单弹性最大（beta） | GPU/ASIC、rack-scale、800G/1.6T、液冷 | Rubin/MI450/定制 XPU、CPO、微电网、SSD/HDD | GPU allocation、端口数、CDU attach、MW 开通 |
| 2026 拐点 | Rubin 2H26 开始交付；GB300 NVL72 单 rack 最高约 `142kW`；电气订单加速 | — | NVIDIA 路线、Eaton/Vertiv/GEV orders [R20-R24] |
| 2027 拐点 | — | 1.6T 批量、HBM4/4E、更多自备电、AI Factory 转租金/收入 | 1.6T qualification、HBM bit shipment、leased MW |

### 1.3 五条最重要的可证伪判断

1. **CapEx 能转成物理量。**务实情景 `$390-470B` / `$42-58M/MW` 对应 `7.5-10.5GW` 2026 新增 AI IT load；CBRE 2025 年末八大市场已有 `5,994.4MW` 在建，Cushman 2026 年披露 Americas 约 `25.3GW` 在建，Applied Digital 单家公司 2026 年 4 月已有 `1GW` AI critical IT load 在建、`900MW` 已签长期租约。[R8-R11] 若 2026 实际美国 AI energization 低于 `6GW`，务实情景被否证。
2. **电力而非芯片将成为更持久约束。**ERCOT 2026 年 3 月收到约 `410GW` 大负荷接入意向、其中约 `87%` 为数据中心，但其调整后非加密数据中心预测从 2026 `7.4GW` 跳到 2027 `39.7GW`，说明“申请量”远大于“可交付量”。PJM 预计 2025-2030 数据中心负荷增量可达约 `30GW`。[R12-R14] 若 interconnection/PPA/现场发电转化率大幅高于预期，则乐观情景概率上升。
3. **HBM/CoWoS 仍紧，但不再是唯一硬墙。**Micron 已锁定全部 calendar 2026 HBM 价量，估计全球 HBM TAM 从 2025 `$35B` 以约 `40% CAGR` 增至 2028 `$100B`；HBM4 已进入量产，TSMC 仍以大尺寸 CoWoS 为主并扩产。[R25-R28] 若 HBM ASP 在高 bit growth 下仍连续两季下跌、或 GPU 交付不再受 memory/package 限制，HBM 稀缺溢价应下修。
4. **自备电是 2027 最大非线性项。**Bloom 与 Oracle 已签初始 `1.2GW`、框架上限 `2.8GW`；Caterpillar 相关项目计划 2027 达 `2GW`；GE Vernova 2026Q1 gas turbine backlog+slot 达 `100GW`，数据中心客户约占近期 gas turbine 合同 `20%`。[R29-R32] 若州排放许可、燃气管线或 turbine slot 延迟，自备电订单池将向 2028 后移。
5. **订单不等于收入。**Digital Realty 2026Q1 新租约到起租平均滞后 `19个月`；Eaton 新增 switchgear 工厂预计 2027H1 才投产；Vertiv Ohio 液冷扩产预计 2027Q2 投产。[R33-R35] 因而 2026 的 order/backlog 高峰可对应 2027-2028 收入，而不能全部塞进 2026。

## 二、研究口径、资料边界和估算方法

### 2.1 独立研究边界

- 本报告只使用本轮研究方案与公开联网资料；未读取、引用或继承任何旧报告、索引、缓存或中间结论。
- 主锚点优先级：公司财报/IR/监管文件 > 电网与政府文件 > 一手项目/产品文档 > CBRE/JLL 等行业数据 > 估算。
- 非正式线索仅用于设定敏感性，不作为总量主锚；所有估算均给出置信度与反证条件。

### 2.2 核心口径与去重规则

| 项目 | 本报告纳入 | 排除/另列 | 去重规则 |
|---|---|---|---|
| 美国 AI 建设 | 美国境内训练、推理、AI Factory、GPU/ASIC 集群、新建/改造与 AI colo | 海外项目、传统企业 IT refresh、非 AI colo、crypto | 以最终资产所在地为准 |
| Hyperscaler CapEx | server/GPU/ASIC/network/data center/AI power | 办公、物流、卫星、消费硬件、海外非美国 | 用 AI 占比×美国占比×当年转化率折减 |
| NeoCloud/AI Factory | 自有 GPU、设备、独立融资的 facility 与 power | 从 hyperscaler 转租而由后者已计 CapEx 的资产 | 客户供货 GPU 与 Oracle/CoreWeave CapEx只计一次 |
| REIT/colo | landlord-funded shell、MEP、供电与租户改善 | 租户自行采购 compute | 资产所有者 CapEx 与租户硬件分开 |
| 模块拆分 | 终端 CapEx 的经济内容 | 供应链内部转售重复值 | GPU售价拆出 HBM、package；rack-scale 子集不与整机相加 |

### 2.3 总量公式与情景参数

```text
US AI DC CapEx(y,s)
= Σ[客户总 CapEx × AI/DC 相关占比 × 美国资产占比 × 当年建设转化率]
+ 独立 NeoCloud / AI Factory / landlord-funded CapEx
- 海外、非AI、传统IT、办公物流、客户供货GPU与租赁重复项
```

| 参数 | 悲观 | 务实 | 乐观 | 主要证据/反证 |
|---|---:|---:|---:|---|
| 五大平台总 CapEx 中 AI/DC 相关 | `70-76%` | `78-84%` | `83-89%` | Microsoft Q3 约 `2/3` CapEx 为短寿命 GPU/CPU，另有DC长寿命资产；Alphabet机器约 `60%` [R1,R3] |
| AI/DC CapEx 中美国资产占比 | `52-60%` | `64-72%` | `70-78%` | 美国项目/MW、Stargate、Meta/AWS/Oracle建设；这是偏乐观参数，海外扩张降权 |
| 当年建设/设备转化率 | `78-85%` | `90-96%` | `94-99%` | 已下单短寿命设备、finance lease、prepayment；长周期facility按工程进度计 |
| NeoCloud/AI Factory 独立增量 | `$35-55B` | `$60-90B` | `$95-145B` | CoreWeave、Stargate、Applied Digital、xAI |
| 重复项扣减 | `-$45-70B` | `-$50-120B` | `-$80-155B` | Oracle 客户供货/预付、colo 租赁、GPU 系统内部价值 |

### 2.4 务实情景客户群桥接

| 客户群 | 2026 归一后投入 | 2027 归一后投入 | 估算重点 | 置信度 |
|---|---:|---:|---|---|
| Hyperscaler（MSFT/AMZN/GOOG/META/ORCL） | `$350-405B` | `$430-520B` | 公开 CapEx×AI/DC×美国×转化率 | 中高 |
| NeoCloud（CoreWeave 等） | `$35-50B` | `$50-75B` | 融资、active/contracted power、GPU backlog | 中 |
| AI Factory（Stargate、模型公司、专用园区） | `$25-40B` | `$50-80B` | 2026 首期，2027 更多园区/芯片进场 | 中低 |
| AI colo/REIT/developer 自有投入 | `$30-45B` | `$45-65B` | shell/MEP/power，不含租户 compute | 中 |
| 重复项与不可交付规划扣减 | `-$50-70B` | `-$75-120B` | 客户供货 GPU、租赁两端、未通电规划 | 中 |
| **净美国 AI 建设** | **`$390-470B`** | **`$500-620B`** | 归一后结果 | **中高/中** |

## 三、美国 AI 数据中心建设总规模：2026/2027 三情景

### 3.1 总规模与驱动

| 年份 | 悲观 | 务实 | 乐观 |
|---|---:|---:|---:|
| 2026（美国） | `$300-360B` | `$390-470B` | `$500-610B` |
| 2027（美国） | `$360-430B` | `$500-620B` | `$680-840B` |

| 驱动 | 悲观 | 务实 | 乐观 |
|---|---|---|---|
| GPU/ASIC 供给 | memory/package/融资使 rack 延后；GPU/ASIC `3.3-4.2M` 颗 | Blackwell Ultra+Rubin+ASIC；`4.6-6.2M` 颗 | Rubin/MI450/custom XPU 超预期；`6.4-8.2M` 颗 |
| HBM/CoWoS | HBM4 yield 与大尺寸 package 限制，allocation 集中 | HBM4量产、CoWoS扩张，仍偏紧 | 三家 HBM 与 OSAT/CoWoS 良率超预期 |
| 电力 | 新增 AI IT load 仅 `5.5-7.0GW` | `7.5-10.5GW` | `10.5-13.5GW`，需 BYOP 快速落地 |
| 融资 | NeoCloud 利率/担保恶化，未签约项目取消 `25-35%` | 预付款、take-or-pay、ABS/项目融资继续 | 客户预付款与长期租约令落地率 `80%+` |
| AI 需求 | utilization、token 收入落后 CapEx | 训练+推理+agentic workload 稳增 | 多模态/agent/企业推理使单位电力收入提升 |

### 3.2 证据锚与“为什么不能直接相加”

| 主锚 | 披露日期 | 原始数字 | 模型用途 | 调整 |
|---|---|---:|---|---|
| Microsoft FY26Q3 | 2026-04-29 | CY2026 CapEx 约 `$190B`；当季 `$31.9B`，约 `2/3` 为 GPU/CPU；新增 `1GW` capacity | 最大平台与机器/长寿命资产比例 | 扣海外、非 AI、价格上涨 `$25B` 部分 |
| Amazon 2026Q1 | 2026-04-29 | Q1 cash CapEx `$43.2B`；2026计划约 `$200B`；`2.1M+` AI chips/12月 | AWS/Trainium/NVIDIA 主锚 | 扣 fulfillment、海外；OpenAI/Anthropic合同不等于当年建设 |
| Alphabet 2025Q4 | 2026-02-04 | 2026 CapEx `$175-185B`；约 `60%` machines、`40%` DC+network | 机器/facility 比例 | 扣非 AI、海外、Other Bets |
| Meta 2026Q1 | 2026-04-29 | 2026 CapEx `$125-145B` | 自用 AI 与 MTIA/NVIDIA/AMD | 扣非美国与通用 infra |
| Oracle FY2026 | 2026-06-10 | CapEx `$55.7B`；RPO `$638B`；AI合同预付/客户供货硬件 `$75B` | Stargate/OCI 交付与融资 | `$75B` 不重复计入 Oracle CapEx和客户 CapEx |
| CoreWeave 2026Q1 | 2026-05-07 | active power `>1GW`、contracted `>3.5GW`、backlog 近 `$100B` | NeoCloud 转化率 | backlog 非当年收入，融资风险高 |
| OpenAI Stargate | 2025-09-23/2026-01-09 | 近 `7GW`、未来三年 `>$400B`；SB Energy 首期 `1.2GW` | AI Factory 物理/美元比 | 多年规划，扣 Oracle/CoreWeave 重叠 |

### 3.3 三情景的可证伪阈值

| 情景 | 成立条件 | 2026 年内否证 | 2027 年内否证 |
|---|---|---|---|
| 悲观 | energization `<7GW`、GPU/ASIC `<4.2M`、NeoCloud 违约上升 | 平台 CapEx 未下修且 H2 rack 交付加速 | AI load `>11GW` 且利用率/租约强 |
| 务实 | energization `7.5-10.5GW`、GPU/ASIC `4.6-6.2M`、pre-lease 高 | 连续两季平台 CapEx 下修 `>15%` 或 utility 延误 `>12月` | 2027 energization `<9GW` 或 AI 收入/CapEx 比恶化 |
| 乐观 | 2026 `>10.5GW`、2027 `>14GW`，BYOP、HBM4、Rubin 同时兑现 | 2026H2 turbine/fuel-cell/transformer 不能按期交付 | 2027 GPU/ASIC `<8M` 或 power pipeline 转化 `<25%` |

## 四、从 CapEx 到物理规模：MW、rack、GPU、建设周期交叉验证

### 4.1 物理规模总表

| 指标 | 2026 悲观 | 2026 务实 | 2026 乐观 | 2027 悲观 | 2027 务实 | 2027 乐观 |
|---|---:|---:|---:|---:|---:|---:|
| 新增 AI IT load | `5.5-7.0GW` | **`7.5-10.5GW`** | `10.5-13.5GW` | `7.0-9.0GW` | **`10.0-14.0GW`** | `14.0-19.0GW` |
| 综合 CapEx/MW | `$43-58M` | `$42-58M` | `$44-58M` | `$40-55M` | `$43-60M` | `$45-60M` |
| facility-only/MW | `$10-13M` | `$11-15M` | `$12-17M` | `$10-14M` | `$11-16M` | `$12-18M` |
| AI rack（全部密度） | `70-105k` | `95-145k` | `130-185k` | `85-125k` | `125-185k` | `175-250k` |
| NVL72/同类高密度 rack | `25-38k` | `38-58k` | `55-75k` | `32-48k` | `55-82k` | `80-115k` |
| GPU/ASIC | `3.3-4.2M` | `4.6-6.2M` | `6.4-8.2M` | `4.1-5.2M` | `6.3-8.5M` | `9.0-12.0M` |
| 平均 rack density | `65-95kW` | `80-120kW` | `95-140kW` | `70-100kW` | `90-130kW` | `110-160kW` |

**换算解释。**NVIDIA 官方参考架构给出 GB300 NVL72 单 rack `72 GPUs`、最高约 `142kW`，即满载约 `507 GPUs/MW IT`；但园区还包含 CPU、storage、network、管理节点及较低密度推理 rack，因此全园区按 `440-650 accelerators/MW`。Applied Digital 披露 facility CapEx 约 `$11-13M/MW`，JLL 2026 全球普通 data center construction 均值约 `$11.3M/MW`；AI compute 加 HBM、网络、存储后，综合强度升至 `$42-60M/MW`。[R11,R16,R20]

### 4.2 CapEx 与 MW 的双向校验

| 校验 | 公式 | 2026 务实结果 | 判断 |
|---|---|---:|---|
| 美元→MW | `$390-470B ÷ $42-58M/MW` | `6.7-11.2GW` | 与目标 `7.5-10.5GW` 重叠良好 |
| MW→GPU/ASIC | `7.5-10.5GW × 440-650颗/MW` | `3.3-6.8M` | 取交付/非GPU ASIC混合后 `4.6-6.2M` |
| GPU→NVL72 rack | `GPU ÷ 72`，再扣非NVL/ASIC | `38-58k rack` | 与 `142kW/rack` 和总 IT load 相容 |
| facility cost | `7.5-10.5GW × $11-15M/MW` | `$83-158B` | 其中本报告建筑+电力+冷却约 `$82-127B`，相容 |
| 市场在建 | CBRE `5.99GW` 八大市场+二三级市场/自建园区 | `>8GW` 可见 pipeline | 支撑务实低端，不足以单独证明乐观高端 |

### 4.3 rack 类型与密度

| 类型 | 2026 rack density | 2027 rack density | 主要配置 | 冷却/供电 |
|---|---:|---:|---|---|
| 传统云/CPU | `10-30kW` | `15-35kW` | CPU、通用 storage | 风冷为主，液冷少量 |
| AI inference 混合 | `30-80kW` | `40-100kW` | GPU/ASIC+大内存+NVMe | rear-door/液冷混合 |
| AI training scale-out | `60-120kW` | `80-140kW` | 8-GPU/HGX、400/800G | direct-to-chip+高容量 CDU |
| NVL72/Helios/Rubin | `100-142kW+` | `120-180kW+` | rack-scale、NVLink/scale-up | 液冷标配、busbar/HVDC演进 |
| 极端专用 rack | `150-200kW+` | `180-250kW+` | custom XPU、LPX、storage rack | 系统级液冷、800VDC 可选 |

### 4.4 建设与收入确认周期

| 阶段 | 典型周期 | 订单确认 | 收入/现金节点 | 主要延误 |
|---|---:|---|---|---|
| 土地/电力权利/PPA | `12-48月` | deposit、service agreement | utility/开发费 | queue、许可、输电 |
| 设计/土建/EPC | `12-24月` | NTP、GMP、EPC award | percentage-of-completion | 劳动力、钢材、消防 |
| 变压器/switchgear/UPS | `12-36月` | PO、slot reservation | 出货/验收 | 铜钢、认证、工厂产能 |
| server/rack/HBM/network | `3-12月` | allocation、预付款、LTAs | dock-to-live/客户验收 | HBM、package、memory价格 |
| liquid cooling | `6-18月` | CDU/cold plate订单 | FAT/SAT、现场验收 | 泄漏、流量、接口标准 |
| 租赁 | `12-24月` | pre-lease/take-or-pay | rent commencement | power-ready、tenant fit-out |

**年度错位。**2026 电力设备和工程订单可能在 2027-2028 才转收入；2026 H2 Rubin 系统交付则可能很快转 compute 收入。Digital Realty 的新签租约到起租平均 `19个月` 是最直接的错位证据，[R33] 因此本报告订单池不与当年供应商收入画等号。

## 五、CapEx 结构拆解：悲观/务实/乐观三情景

### 5.1 悲观情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU/ASIC/服务器/compute（扣HBM/package） | `$122-158B` | `40-44%` | `$146-189B` | `40-44%` | allocation集中、融资/需求压低交付 |
| 网络/光/铜互联 | `$28-39B` | `9-11%` | `$34-47B` | `9-11%` | 800G吸收放慢、1.6T延后 |
| 电力/UPS/BESS/配电/能源接入 | `$32-43B` | `10-12%` | `$38-52B` | `10-12%` | 开工少但长交期设备占比高 |
| 建筑/土建/MEP | `$28-40B` | `9-11%` | `$33-47B` | `9-11%` | 电力/审批限制新开工 |
| 冷却/液冷/HVAC | `$12-18B` | `4-5%` | `$14-22B` | `4-5%` | 液冷 attach 低于预期 |
| SSD/HDD/存储系统 | `$10-18B` | `3-5%` | `$12-22B` | `3-5%` | inference/RAG 延后 |
| HBM/DRAM/SRAM | `$22-32B` | `7-9%` | `$25-39B` | `7-9%` | HBM供给紧且GPU数量低 |
| 先进封装/设备/测试 | `$10-14B` | `3-4%` | `$11-17B` | `3-4%` | 扩产慢，WFE滞后 |
| 控制/安全/服务 | `$6-11B` | `2-3%` | `$7-13B` | `2-3%` | attach 延后 |

### 5.2 务实情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU/ASIC/服务器/compute（扣HBM/package） | `$152-202B` | `39-43%` | `$200-267B` | `40-43%` | GB300放量，Rubin 2H26，ASIC并行 |
| 网络/光/铜互联 | `$39-56B` | `10-12%` | `$55-81B` | `11-13%` | 800G主流、1.6T自H2/H1放量 |
| 电力/UPS/BESS/配电/能源接入 | `$35-52B` | `9-11%` | `$50-75B` | `10-12%` | 局部瓶颈，BYOP扩张 |
| 建筑/土建/MEP | `$31-47B` | `8-10%` | `$40-62B` | `8-10%` | 在建与预租项目转化 |
| 冷却/液冷/HVAC | `$16-28B` | `4-6%` | `$25-43B` | `5-7%` | `100kW+` rack 推动液冷 |
| SSD/HDD/存储系统 | `$16-28B` | `4-6%` | `$24-40B` | `5-7%` | inference、RAG、checkpoint共同拉动 |
| HBM/DRAM/SRAM | `$31-47B` | `8-10%` | `$45-68B` | `9-11%` | HBM4与DDR/SOCAMM扩张 |
| 先进封装/设备/测试 | `$16-24B` | `4-5%` | `$22-34B` | `4-6%` | CoWoS/测试扩产、WFE滞后2-6季 |
| 控制/安全/服务 | `$8-14B` | `2-3%` | `$10-19B` | `2-3%` | DCIM/BMS attach 提升 |

### 5.3 乐观情景 CapEx 拆解

| 模块 | 2026 美元规模 | 2026 占比 | 2027 美元规模 | 2027 占比 | 核心假设 |
|---|---:|---:|---:|---:|---|
| GPU/ASIC/服务器/compute（扣HBM/package） | `$210-287B` | `42-47%` | `$306-395B` | `45-47%` | rack-scale与custom XPU同时超预期 |
| 网络/光/铜互联 | `$55-79B` | `11-13%` | `$82-118B` | `12-14%` | 1.6T/CPO/高阶铜加速 |
| 电力/UPS/BESS/配电/能源接入 | `$40-61B` | `8-10%` | `$68-101B` | `10-12%` | 微电网/自备电批量落地 |
| 建筑/土建/MEP | `$35-55B` | `7-9%` | `$54-76B` | `8-9%` | 大型园区批量开工 |
| 冷却/液冷/HVAC | `$25-43B` | `5-7%` | `$41-67B` | `6-8%` | 液冷成为高密度标配 |
| SSD/HDD/存储系统 | `$20-37B` | `4-6%` | `$34-59B` | `5-7%` | 多模态/推理缓存爆发 |
| HBM/DRAM/SRAM | `$40-61B` | `8-10%` | `$68-92B` | `10-11%` | HBM4容量与ASP双升 |
| 先进封装/设备/测试 | `$15-31B` | `3-5%` | `$34-50B` | `5-6%` | CoWoS/CoPoS/OSAT/ATE放大 |
| 控制/安全/服务 | `$10-18B` | `2-3%` | `$14-25B` | `2-3%` | AI Factory运维复杂度提升 |

### 5.4 模块口径与证据强弱

| 模块 | 估算公式 | 主要证据 | 置信度 | 最大误差来源 |
|---|---|---|---|---|
| compute | accelerator数×ASP+CPU/OEM/rack集成，扣HBM/package | NVDA/AMD/Dell/HPE/SMCI订单与收入 | 中高 | GPU ASP、customer-supplied硬件 |
| network | accelerator×NIC/端口×拓扑×ASP | NVDA RA、Broadcom、Arista、Marvell | 中 | 每GPU端口与CPO替代 |
| power | MW×`$4.5-7.5M/MW` | Eaton/GEV/Vertiv backlog，BYOP项目 | 中高 | turbine/fuel cell是否计入园区CapEx |
| building/MEP | MW×`$3.5-5.5M/MW` | JLL/APLD/PWR、在建MW | 中 | 土地/地区人工差异 |
| cooling | rack×liquid attach×BOM + facility HVAC | 142kW rack、Vertiv/Modine订单 | 中 | server-side cold plate是否由OEM计入 |
| storage | GPU/推理负荷×NVMe/HDD容量 | MU/WDC/STX披露 | 中低 | AI专属与通用cloud难切分 |
| memory | accelerator×HBM stack/容量+CPU memory | Micron HBM TAM、HBM4量产 | 中高 | ASP与HBM4 attach |
| package/equipment/test | AI chip价值×package share+WFE/ATE滞后 | TSMC/AMAT/TER/KLAC | 中 | 设备全球产能、美国客户归属 |

## 六、产业链订单映射

> 本节默认给出**务实情景、美国项目归属的供应商订单池**。CAGR 是从 2026 区间中枢到 2027 区间中枢的隐含增长范围；“子集”行不可与母项相加。订单可在签约、预付款、allocation 或 PO 时确认，但收入取决于出货、现场验收或 percentage-of-completion。

### 6.1 电力与能源

#### 6.1.1 订单池

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | 主要公司 | 瓶颈 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| 变压器/中高压 switchgear | `$9-14B` | `$12-18B` | `25-35%` | Eaton、Schneider、GE Vernova/Prolec、Powell、Hubbell、Hitachi Energy | `18-36月`交期、取向硅钢/铜、认证 | backlog、book-to-bill、工厂扩产、utility award |
| UPS/dynamic UPS/BESS/飞轮 | `$8-12B` | `$11-17B` | `30-40%` | Vertiv、Eaton、Schneider、Tesla Energy、Fluence、ABB | 电芯/功率模块、短时大负荷、FAT | data-center orders、MW、DC architecture |
| busway/PDU/低压配电/保护 | `$7-10B` | `$9-14B` | `25-40%` | Vertiv、Eaton、nVent、Schneider、Hubbell | 高电流母线、connector、客户认证 | `$0.7-1.1M/MW`、rack power shelf |
| 微电网/燃机/往复式/燃料电池 | `$7-12B` | `$13-22B` | `55-85%` | GE Vernova、Caterpillar、Bloom、Cummins、utilities/IPP | turbine slot、燃气、排放/噪声许可 | PPA、slot reservation、MW合同、州审批 |
| HVDC/800VDC/固态变压器 | `$1.5-3.0B` | `$3-6B` | `70-110%` | Eaton、Vertiv、Schneider、ABB、Infineon、onsemi | 标准、保护、DC breaker、field reliability | 800V-ready shipment、reference design、deployment MW |

#### 6.1.2 订单证据与结构判断

- Eaton 2026Q1 Electrical Americas 滚动 12 月订单同比 `+42%`、总 backlog 同比 `+44%`，Electrical 总 book-to-bill `1.2x`；新 Nebraska switchgear 工厂 2027H1 才生产，说明 2026 紧张延续到 2027。[R22,R34]
- GE Vernova 2026Q1 单季 data-center electrification equipment orders `$2.4B`，超过 2025 全年；gas turbine backlog+slot 从 `83GW` 升至 `100GW`，目标年末至少 `110GW`。[R24,R31]
- Bloom/Oracle 首批 `1.2GW` 已部署、框架上限 `2.8GW`；Caterpillar 相关 Monarch 项目设备 2026-09 起交付、2027 计划 `2GW` 在线。这两项是 2027 微电网非线性上修的硬证据，但均受燃气与许可约束。[R29,R30]
- **价值捕获：**switchgear/transformer 的确定性高于 BESS；燃料电池/燃机的 beta 更高。800VDC 在 2026 主要是架构/早期订单，2027 才可能形成 `$3B+` 可见池，不能把路线图当已确认收入。

### 6.2 AI服务器与机架

| 子环节 | 2026 订单规模 | 2027 订单规模 | 2026-2027 CAGR | 主要公司 | 毛利/价值捕获 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| AI整机（含accelerator，母项） | `$145-195B` | `$190-270B` | `30-40%` | NVIDIA、AMD、Dell、SMCI、HPE、Quanta、Wiwynn、Foxconn | GPU/ASIC高毛利；OEM/ODM约 `5-15%` GM | orders、backlog、GPU allocation、revenue |
| rack-scale system（整机子集） | `$85-125B` | `$130-200B` | `50-60%` | NVIDIA、AMD、Dell、SMCI、HPE、Quanta、Foxconn | NVLink/scale-up、液冷与验收溢价 | NVL72/Helios/Rubin rack shipment |
| 管理/存储节点（整机外延） | `$8-14B` | `$12-20B` | `40-50%` | Dell、HPE、SMCI、Pure、NetApp、ODM | 低于GPU毛利、服务attach较高 | node/GPU、checkpoint/RAG需求 |
| 机柜级电源与液冷集成 | `$10-16B` | `$15-24B` | `45-55%` | Vertiv、Eaton、Schneider、nVent、SMCI | 系统验收与field service提高壁垒 | kW/rack、power shelf、CDU attach |

**订单确认节点。**accelerator allocation/预付款 → ODM/OEM component PO → rack FAT → 数据中心 SAT/dock-to-live → 收入。Dell FY27Q1（2026-05-28 披露）单季 AI orders `$24.4B`、AI server revenue `$16.1B`、期末 backlog `$51.3B`，且称 memory 是主要约束；HPE FY26Q1 AI backlog `>$5B`；Supermicro 2026-06 计划筹资 `$7B` 采购部件以满足新近 AI server orders。[R39,R40,R41]

**毛利判断。**NVIDIA/定制 ASIC 设计与scale-up fabric捕获最高；OEM/ODM收入大但 component pass-through 使毛利偏低。SMCI 2025Q4（FY26Q2）销售 `$12.7B`、GAAP GM仅 `6.3%`，是“收入 beta 大、利润池未必大”的反例。Dell 的工程、安装、融资与服务可提高单位价值，但 GPU 仍占 BOM 大头。

### 6.3 网络、光互联与铜互联

| 子环节 | 2026 订单规模 | 2027 订单规模 | CAGR | attach 假设 | 主要公司 | 验证指标 |
|---|---:|---:|---:|---:|---|---|
| 800G/1.6T optical | `$14-20B` | `$22-32B` | `50-60%` | `2.5-5.0` optical endpoints/GPU等效 | Coherent、Lumentum、Fabrinet、Innolight、Eoptolink、Broadcom、Marvell | module shipment、ASP、1.6T qualification |
| AI fabric switch/system | `$16-23B` | `$24-36B` | `45-55%` | leaf-spine+scale-up/scale-out `12-18%` compute BOM | NVIDIA、Arista、Cisco、Broadcom、HPE/Juniper | switch orders、Tomahawk/Spectrum port shipment |
| NIC/DPU/routing | `$6-10B` | `$9-15B` | `45-55%` | `1.2-2.0` NIC/DPU/GPU等效 | NVIDIA、Broadcom、Marvell、AMD/Pensando、Cisco | ConnectX/BlueField/NIC revenue |
| DAC/AEC/backplane/connector | `$3-6B` | `$5-9B` | `55-70%` | rack内铜、rack间短距，随142kW rack上升 | Amphenol、TE Connectivity、Credo、Astera Labs、Broadcom | NVL BOM、AEC orders、copper reach/power |
| CPO/LPO/XPO（上述子集） | `$1-3B` | `$4-8B` | `120-180%` | 2026早期，2027进入高端平台 | Broadcom、NVIDIA、Arista、Coherent、TSMC生态 | production yield、field replacement、客户认证 |

NVIDIA GB300 参考架构中每个 4-GPU tray 有 `4` 个 ConnectX-8 HCA，并配置 BlueField DPU；双 rack `144 GPU` 参考设计需要大量 `400G` uplink，说明端口不是“每GPU一根光模块”的简单线性，而由多层拓扑、rail optimization 与冗余决定。[R20] Broadcom FY26Q2 AI semiconductor revenue `$10.8B`、同比 `+143%`，并预计Q3 `$16B`；Arista 2026Q1 revenue `$2.709B`、同比 `+35.1%`，1.6T产品从 2026Q4/2027Q1 交付；Marvell FY2026 data-center revenue `>$6B`，其中 optical interconnect 约占一半。[R36-R38]

**反证：**若 1.6T module ASP 下降快于 shipment 增长、CPO field reliability 不达标、custom ASIC 集群使用更扁平拓扑，2027 optical/CPO 池下修 `15-25%`；反之 million-XPU fabrics 会把网络占比从 `11-13%` 推到 `13-15%`。

### 6.4 半导体上游

| 子环节 | 2026 订单规模 | 2027 订单规模 | 订单确认节奏 | 主要公司 | 主要瓶颈 | 验证指标 |
|---|---:|---:|---|---|---|---|
| GPU/ASIC（扣HBM/package） | `$125-175B` | `$160-240B` | allocation、预付款、wafer starts、系统交付 | NVDA、AMD、AVGO、MRVL、GOOG/AMZN/MSFT/META自研 | die、HBM、package、power | DC/AI revenue、GW承诺、shipment |
| HBM/DRAM/SRAM | `$35-50B` | `$48-70B` | LTA、bit shipment、ASP、客户qualification | SK hynix、Micron、Samsung；Rambus/IP | stack yield、base die、TSV、thermal | HBM bit growth、ASP、mix、capex |
| CoWoS/先进封装/基板/OSAT | `$12-18B` | `$17-26B` | wafer start后、package capacity reservation | TSMC、ASE、Amkor、Ibiden、Unimicron | 大尺寸interposer、基板、测试 | monthly capacity、yield、substrate lead time |
| 半导体设备/测试 | `$14-20B` | `$18-28B` | 对AI终端CapEx滞后 `2-6季` | AMAT、LRCX、KLAC、ASML、Advantest、TER | tool lead time、tester time、cleanroom | WFE、backlog、tester utilization |

**训练与推理差异。**训练对 GPU/HBM/scale-out network 的美元强度最高；推理在模型量化和 custom ASIC 渗透后可能降低每 token compute 成本，却提高 CPU/low-power memory、KV-cache storage、regional network 与单位电力效率的需求。因而“推理爆发”不等于 GPU 价值无限线性上升，更可能将 2027 增量从 HBM-only 向 SOCAMM/DDR、BlueField storage、NVMe/HDD 和网络分散。

**上游证据。**Micron 2025-12 披露 2026 HBM 价量全部锁定，HBM TAM 2025 `$35B`→2028约 `$100B`；2026-03/06 HBM4与PCIe Gen6 SSD量产。Samsung 2026-02称已量产并商业出货 HBM4。Applied Materials 预计其 semiconductor equipment 业务 calendar 2026增长 `>30%`、advanced packaging revenue `>50%`；Teradyne 2026Q1 semiconductor test revenue `$1.111B`、同比 `+105%`，约 `70%`公司收入与AI需求相关。[R25-R27,R44-R45]

### 6.5 建筑、工程、REIT 与开发商

| 子环节 | 2026 订单规模 | 2027 订单规模 | CAGR | 主要公司 | 价值捕获 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| EPC/MEP/土建/消防/弱电 | `$28-42B` | `$38-58B` | `35-40%` | Quanta、EMCOR、MTZ、AECOM、Jacobs、Fluor、Turner | backlog转收入；人工/排期溢价 | bookings、backlog、margin、NTP |
| 预制化模块/机房（EPC子集） | `$7-12B` | `$11-18B` | `50-55%` | Vertiv、Eaton/Fibrebond、Schneider、GE Vernova | time-to-power、工厂化质量 | factory capacity、MW delivery、FAT |
| REIT/colo/developer facility CapEx | `$22-35B` | `$35-55B` | `55-60%` | DLR、EQIX、QTS、Vantage、CyrusOne、APLD、IRM | power bank、pre-lease、rent escalator | leased MW、pipeline、rent commencement |
| 土地/电力权利/开发费 | `$4-8B` | `$6-11B` | `45-55%` | developer、utility、land owner | powered land稀缺 | land bank、service agreement、deposit |

Quanta 2026Q1 record backlog `$48.5B`，受 utility/generation/large-load convergence 支撑；Applied Digital 2026-04 披露 `1GW` critical IT load在建、`900MW`已签，facility CapEx约 `$11-13M/MW`。Digital Realty 2026Q1新签年化GAAP租金 `$707M`（100% share），signed-but-not-commenced annualized rent backlog `$1.8B`，新签至起租平均 `19月`；Iron Mountain 2026年前四个月已租 `32MW`，未来24个月约 `400MW`可通电/可用。[R10,R17,R18,R33,R43]

**REIT不是compute受益。**DLR/EQIX/APLD捕获的是租金、power bank、开发价差与服务，不拥有大部分租户 GPU。将租户 server CapEx 与 landlord facility CapEx 同时算入 REIT TAM 会重复；本报告只把 landlord-funded 部分放入本行。

### 6.6 冷却、存储、DCIM 和其他必要环节

| 环节 | 2026 订单规模 | 2027 订单规模 | CAGR | 关键假设 | 公司/价值捕获 | 验证指标 |
|---|---:|---:|---:|---|---|---|
| liquid cooling/CDU/cold plate/pump/valve | `$10-17B` | `$18-30B` | `70-80%` | 高密度AI rack液冷attach `55-70%`→`70-85%` | Vertiv、Modine、Eaton/Boyd、nVent、Schneider、CoolIT、Danfoss | CDU MW、$/rack、field failure、gross margin |
| chiller/HVAC/heat rejection | `$8-13B` | `$11-18B` | `35-40%` | facility cooling仍需，PUE `1.15-1.30` | Modine、JCI、Carrier、Trane、Vertiv、Schneider | `$0.8-1.3M/MW`、lead time、chiller bookings |
| coolant/water treatment/filter | `$1-3B` | `$2-4B` | `55-65%` | service attach、fluid replacement、water chemistry | Chemours、Honeywell、Kurita、Ecolab、Parker | installed base、consumable/service revenue |
| SSD/HDD/storage systems | `$16-28B` | `$24-40B` | `45-50%` | SSD用于checkpoint/KV/cache，HDD用于data lake/retention | MU、Kioxia/Sandisk、Samsung、WDC、STX、Pure、Dell | PB/EB shipment、ASP、mix、AI storage revenue |
| DCIM/BMS/energy control/digital twin | `$4-7B` | `$6-10B` | `40-50%` | software/control attach `65-80%`→`75-90%` | Schneider、Vertiv、Siemens、Honeywell、JCI、Cadence | ARR/service attach、PUE、alarm/uptime |
| fire/security/cable management | `$3-5B` | `$4-7B` | `35-45%` | `$0.35-0.65M/MW` | JCI、Honeywell、nVent、Hubbell、Motorola Solutions | project awards、$/MW、code approval |

#### 6.6.1 液冷渗透、单位经济与毛利

| 指标 | 2026 | 2027 | 口径/说明 |
|---|---:|---:|---|
| 高密度AI rack液冷attach | `55-70%` | `70-85%` | `>80kW/rack` 的 direct-to-chip、rear-door或混合方案 |
| NVL72/同类rack液冷attach | `90-100%` | `95-100%` | GB300 NVL72官方为全液冷；Rubin沿用rack-scale液冷架构 |
| CDU+cold plate+manifold+泵阀成本 | `$120-280k/rack` | `$130-320k/rack` | 取决于冗余、流量、二次侧与是否含server-side部件 |
| facility chiller/heat rejection等效 | `$80-180k/rack` | `$85-190k/rack` | 以 `80-160kW/rack`、共享facility设备折算 |
| 核心液冷硬件供应商毛利 | `25-40%` | `27-42%` | 认证/集成/服务高于通用泵阀；非公司指引，估算置信度中低 |
| 现场服务/耗材毛利 | `35-55%` | `38-58%` | installed base扩大后，fluid/filter/commissioning attach提升 |

#### 6.6.2 AI存储介质 mix

| 订单价值mix | 2026 | 2027 | 用途 |
|---|---:|---:|---|
| enterprise NVMe SSD/NAND | `58-70%` | `55-68%` | checkpoint、KV cache、RAG、hot tier、local scratch |
| nearline HDD | `18-28%` | `20-30%` | data lake、训练集、日志、长期retention；按容量仍占主导 |
| storage system/software/service | `10-16%` | `12-18%` | object/file、data orchestration、support |
| SSD:HDD 单位容量价格比 | `4-8x` | `3-7x` | 高度依赖NAND/HDD价格周期；不可用价值mix推容量mix |

Modine 2026-05 披露与某 hyperscaler 签订至2029约 `$4B` chiller capacity agreement，是冷却池从概念走向长期订单的强证据；Vertiv 2026Q1销售 `$2.65B`、同比 `+30%`，全年 organic sales 指引 `+29-31%`，并在北美推出支持 `50kW`至 `>100kW/rack` 的 modular liquid cooling。[R23,R42] WD 2026FQ3 revenue `$3.337B`、同比 `+45%`，称几乎所有AI工作负载都会形成需持久保存的数据；Seagate 2026FQ2 revenue `$2.825B`，强调AI推动exabyte-scale存储。[R46-R47]

**长尾瓶颈。**冷却液兼容、leak detection、接头、过滤、water chemistry、消防规范和现场 commissioning 的单项金额小，却可阻塞整排 rack 验收。投资研究应跟踪 warranty/field failure 与 FAT/SAT 周期，而非只跟踪“液冷渗透率”。

## 七、三情景敏感性分析：订单变化百分比和美元变化

### 7.1 情景变量矩阵

| 变量 | 悲观 | 务实 | 乐观 | 最敏感订单池 |
|---|---|---|---|---|
| GPU/ASIC供给 | 交付延后、集中少数客户 | GB300/Rubin/custom XPU并行 | 供给/良率超预期 | server、network、HBM、cooling |
| HBM | HBM4 yield/stack受限 | 逐季改善、ASP高位 | 三家供应与容量超预期 | GPU、memory、test |
| CoWoS/package | 大尺寸产能硬墙 | 扩产兑现仍偏紧 | CoWoS/OSAT/CoPoS协同 | accelerator、equipment |
| 电力 | 新增AI IT load低于 `7GW` | `7.5-10.5GW` | `>10.5GW` | EPC、power、cooling |
| 融资 | NeoCloud spread扩大、取消率高 | take-or-pay/预付/ABS持续 | 低成本资金与预付款加速 | developer、server |
| AI需求 | utilization/收入弱 | 训练+推理稳定 | agentic/多模态爆发 | compute、storage、network |

### 7.2 2027 订单池相对务实情景变化

| 产业链 | 悲观 vs 务实 | 悲观美元变化 | 乐观 vs 务实 | 乐观美元变化 | 主要敏感变量 |
|---|---:|---:|---:|---:|---|
| 电力与能源 | `-18% to -28%` | `-$10-20B` | `+28% to +45%` | `+$18-35B` | interconnection、BYOP、transformer |
| AI服务器与机架 | `-25% to -35%` | `-$50-90B` | `+30% to +45%` | `+$70-120B` | GPU/HBM/rack交付、融资 |
| 网络与光互联 | `-25% to -35%` | `-$12-22B` | `+35% to +55%` | `+$20-35B` | 1.6T、端口数、拓扑/CPO |
| 半导体上游 | `-22% to -32%` | `-$45-80B` | `+32% to +50%` | `+$75-125B` | XPU、HBM4、CoWoS、ATE |
| 建筑与工程 | `-15% to -25%` | `-$8-16B` | `+25% to +40%` | `+$14-28B` | 开工、MEP、电力许可 |
| 冷却 | `-20% to -30%` | `-$7-12B` | `+35% to +55%` | `+$13-23B` | kW/rack、liquid attach、验收 |
| 存储 | `-18% to -30%` | `-$5-10B` | `+35% to +60%` | `+$10-22B` | inference/RAG、SSD/HDD价格 |

### 7.3 关键单变量敏感性

| 单变量变化 | 对2027总规模 | 主要传导 |
|---|---:|---|
| 新增AI IT load每减少 `1GW` | `-$43-60B` | compute约 `-$25-34B`，network `-$5-7B`，facility/power/cooling `-$11-16B` |
| accelerator每减少 `1M` 颗 | `-$45-70B` | GPU/ASIC、HBM、package、network；不全等于MW下降 |
| facility-only成本每升 `$1M/MW` | `+$10-14B` 名义CapEx | 可能是价格而非实物量，压制项目IRR |
| 液冷attach每升 `10ppt` | `+$2.5-4.5B` | CDU/cold plate/pump/controls，部分替代风冷 |
| HBM ASP每升 `10%` | `+$4-7B` memory池 | 对GPU系统毛利/融资有负向挤压 |
| 1.6T渗透每升 `10ppt` | `+$2-4B` optical/network池 | 取决于ASP与端口复用 |

## 八、公司受益映射：核心受益、间接受益、伪受益

### 8.1 核心受益公司

| 公司 | 环节 | 2026-2027 暴露 | 订单弹性 | 确定性 | 主要证据 | 核心反证 |
|---|---|---|---|---|---|---|
| NVIDIA（NVDA） | GPU、NVLink、NIC/DPU、network、rack | compute/network双重价值捕获 | 极高 | 高 | FY26 DC revenue `$193.7B`；Rubin 2H26 [R21] | custom ASIC/AMD份额、供电限制 |
| Broadcom（AVGO） | custom XPU、switch ASIC、optics/DSP | hyperscaler ASIC+network | 极高 | 高 | FY26Q2 AI revenue `$10.8B`，+143% [R36] | 客户集中、项目时点 |
| AMD（AMD） | Instinct/EPYC/Helios | Meta首批1GW、上限6GW | 极高 | 中高 | 2026Q1 DC revenue `$5.8B`，+57% [R41] | rack交付/软件/供应 |
| Dell（DELL） | AI server/rack/integration | 大额backlog、低毛利高周转 | 高 | 高 | 2026-05 backlog `$51.3B` [R39] | memory供给、GM稀释 |
| Arista（ANET） | Ethernet AI fabric | 800G→1.6T | 高 | 高 | Q1 growth `35.1%`；1.6T Q4/Q1 [R37] | hyperscaler自研、CPO架构变化 |
| Micron（MU） | HBM4、DDR/SOCAMM、SSD | memory+storage双暴露 | 极高 | 高 | 2026 HBM全锁定；HBM TAM 40%CAGR [R25-R26] | 2027供给过量/ASP下跌 |
| Vertiv（VRT） | UPS、busway、liquid cooling、service | power+cooling系统 | 高 | 高 | 2026 organic sales +29-31% [R23] | 大客户议价、现场故障 |
| Eaton（ETN） | switchgear、UPS、busway、thermal | 长交期刚性 | 中高 | 极高 | orders +42%、backlog +44% [R22] | 扩产快于需求、价格正常化 |
| GE Vernova（GEV） | transformer/grid/gas turbine | grid+BYOP | 高 | 极高 | DC equipment orders `$2.4B`/Q [R24] | turbine/许可延误 |
| Modine（MOD） | chiller/liquid cooling | 冷却纯度较高 | 极高 | 中高 | hyperscaler `$4B`长期协议 [R42] | 客户集中、执行/扩产 |
| Quanta Services（PWR） | utility/EPC/large-load | 电网与MEP | 中高 | 高 | backlog `$48.5B` [R43] | 劳动力/项目margin |
| CoreWeave（CRWV） | NeoCloud | 利用率与融资的高beta | 极高 | 中 | backlog近 `$100B`、active `>1GW` [R6] | 客户集中、债务/残值 |

### 8.2 间接受益与需要折价的公司

| 类别 | 公司示例 | 为什么受益 | 为什么折价 |
|---|---|---|---|
| storage | WDC、STX、Pure Storage | inference/RAG/retention、EB增长 | AI专属收入难切分、价格周期 |
| test/WFE | AMAT、KLAC、TER、Advantest、LRCX | HBM/logic/package复杂度和测试时长 | 订单滞后 `2-6季`、全球而非美国收入 |
| REIT/colo | DLR、EQIX、IRM | power bank、pre-lease、租金 | 不捕获租户GPU；资本成本/建设风险 |
| connectors/copper | APH、TEL、CRDO、ALAB | 高速/高电流/scale-up密度 | attach与客户BOM透明度低 |
| HVAC/building controls | JCI、CARR、TT、HON | chiller/BMS/消防必需 | 公司体量大、AI收入占比可能低 |
| utilities | D、SO、AEP、DUK等 | load growth、rate base | 监管、客户信用、居民费率分摊风险 |

### 8.3 伪受益/排除规则

以下不是对单一公司的永久否定，而是**在没有订单证据时的降权规则**：

1. 只有“AI/data center”营销表述，却没有 `$`订单、MW、book-to-bill、backlog、客户认证或产能扩张；
2. 供应的是通用建筑/电气产品，但 data center revenue `<5%` 且竞争充分，订单增长不能覆盖估值溢价；
3. REIT/开发商把未获得电力的 land bank 当可租 MW；ERCOT `410GW` 申请量说明 queue 不是资产；
4. NeoCloud backlog 主要来自单一客户、缺少 take-or-pay/预付款，且 debt service 依赖 GPU residual value；
5. CPO、solid-state transformer、immersion 等只有 demo/roadmap，无量产良率、现场可靠性和付费客户；
6. 软件/DCIM 只按总园区CapEx比例套用，却没有 ARR、attach、seat/device 或服务收入证据。

### 8.4 股价快照（仅用于研究时点，不构成目标价）

| 公司 | 2026-07-10 收盘/最新价 | 公司 | 2026-07-10 收盘/最新价 |
|---|---:|---|---:|
| NVDA | `$210.96` | AMD | `$557.89` |
| AVGO | `$399.97` | ANET | `$186.96` |
| DELL | `$434.97` | VRT | `$318.86` |
| ETN | `$407.28` | GEV | `$1,091.57` |
| PWR | `$658.56` | MOD | `$245.91` |
| BE | `$244.61` | CRWV | `$88.88` |
| APLD | `$31.15` | MU | `$979.30` |
| WDC | `$582.59` | STX | `$910.34` |
| EQIX | `$1,051.21` | DLR | `$180.41` |

> 股价来自 2026-07-10 美股收盘附近的合并行情快照；未进行拆股历史重述核验，不用于模型计算。由于本报告目标是订单映射而非估值，未给单点目标价或PE结论。

## 九、投资视角总结：α、β、bottleneck 和 2026/2027 订单拐点

### 9.1 α 与 β 分层

| 分层 | 首选环节 | 务实→乐观的2027美元增量 | 原因 | 主要风险 |
|---|---|---:|---|---|
| 订单弹性最大（beta） | GPU/custom XPU/rack-scale | `+$70-120B`（整机池） | 每多1GW直接带动compute/HBM/network | 电力/需求/融资共同放大下行 |
| 高beta | 1.6T/CPO/AI fabric | `+$20-35B` | 端口与带宽随cluster规模非线性 | ASP下降、拓扑/铜替代 |
| 高beta | 微电网/自备电 | `+$12-25B` | 从备用电转主电源，2027基数低 | 许可、燃气、turbine slot |
| 高beta | liquid cooling | `+$13-23B` | rack density与attach双升 | 标准化压价、field failure |
| 确定性最高（alpha） | transformer/switchgear/busway | `+$8-15B` | 长交期、认证、backlog、扩产慢 | 2028供给正常化 |
| 高alpha | 已预租 EPC/MEP | `+$14-28B` | take-or-pay、NTP、backlog转收入 | 人工/固定价合同margin |
| 高利润池 | GPU、custom ASIC IP、switch ASIC、HBM、ATE | 不宜简单相加 | 技术/良率/认证/客户锁定 | 高集中与周期性 |
| 收入大但利润池薄 | OEM/ODM、普通土建、通用元件 | 收入随CapEx上升 | pass-through与竞争 | 营运资金、毛利稀释 |

### 9.2 Bottleneck 清单

| 瓶颈 | 2026状态 | 2027状态 | 受益环节 | 被压制环节 | 缓解窗口 | 反证指标 |
|---|---|---|---|---|---|---|
| 电力接入 | **明显** | **局部/仍明显** | utility、grid、BYOP | developer、server utilization | 2027-2029 | signed service MW、substation COD |
| transformer/switchgear | **明显** | **局部** | ETN/GEV/Schneider/POWL | project start | 新产能2027起 | lead time、book-to-bill `<1` |
| gas turbine/燃气 | **明显** | **明显** | GEV/CAT/BE | BYOP园区 | 2028+ | slot、pipeline、permit |
| HBM | **局部偏紧** | **局部** | MU/SKhynix/Samsung | GPU/rack | 2026H2-2027 | bit growth、ASP、yield |
| CoWoS/大尺寸package | **局部偏紧** | **局部/缓解** | TSMC/OSAT/WFE/ATE | GPU/ASIC | 2027 | monthly capacity、package yield |
| 1.6T optics/CPO | **认证/良率** | **局部** | optical/DSP/foundry | fabric deployment | 2027H1-H2 | qualified vendors、RMA |
| liquid cooling integration | **明显** | **局部** | VRT/MOD/ETN/nVent | 100kW+ rack | 2027 | FAT/SAT、leak/field failure |
| MEP/craft labor | **明显** | **明显/局部** | PWR/EME/MTZ | campus COD | 地区差异大 | backlog conversion、margin |
| financing | **NeoCloud局部** | **分化** | 预付款/高信用项目 | speculative developer | 取决于利率/利用率 | credit spread、DSCR、cancellation |

### 9.3 2026 vs 2027 订单拐点

| 年份 | 可能出现的订单拐点 | 最直接受益环节 | 跟踪指标 |
|---|---|---|---|
| 2026H2 | GB300持续、Rubin 2H26交付；Dell/ODM backlog转出货 | GPU、rack、HBM4、NIC/DPU | rack shipment、AI server revenue、memory constraint |
| 2026H2 | 800G高位、1.6T 2026Q4首批 | optical、switch、DSP、connector | 1.6T qualification/ASP、ANET availability |
| 2026全年 | Eaton/GEV/Vertiv orders/backlog高位 | switchgear、UPS、busway、cooling | book-to-bill、lead time、capacity |
| 2026H2-2027 | 液冷从attach到系统验收 | CDU/cold plate/pump/controls | liquid MW、FAT/SAT、warranty |
| 2027 | Rubin/MI450/custom XPU多平台放量 | GPU/ASIC、HBM4、CoWoS、ATE | hyperscaler deployment GW、HBM bit |
| 2027 | Bloom/CAT/GEV自备电扩大 | fuel cell、turbine、BESS、grid controls | contracted/online MW、permit |
| 2027 | inference/RAG/agentic数据累积 | SSD/HDD、storage system、network | EB shipment、enterprise SSD revenue |
| 2027-2028 | 2026 pre-lease进入rent commencement | REIT/colo/EPC | leased MW、19个月lag、NOI |

## 十、反证条件、风险和后续跟踪清单

### 10.1 总模型反证条件

| 反证条件 | 触发阈值 | 对模型动作 |
|---|---:|---|
| 平台CapEx下修 | 五大平台合计2026/2027 guide下修 `>15%` | 总量下修 `12-20%`，compute/network优先 |
| AI energization不足 | 2026美国新增AI IT load `<6GW` | 2026降至悲观；2027 facility订单后移 |
| 利用率/收入不兑现 | AI cloud/agent收入增速连续两季低于CapEx增速 `>20ppt` | NeoCloud落地率、GPU ASP、2027乐观权重下修 |
| 融资恶化 | NeoCloud/project debt spread扩大 `>300bp`、取消率 `>20%` | developer/server下修，alpha转向已预付项目 |
| HBM/package硬墙 | GPU system交付连续两季因memory/package延迟 `>20%` | compute收入后移，HBM/ATE稀缺溢价上修 |
| 电力硬墙 | utility promised COD延后 `>12月` 或 signed MW/queue `<10%` | 2027 MW下修，自备电池上修但不完全抵消 |
| 价格通胀假繁荣 | facility `$ /MW`升 `>15%` 而MW不增 | 名义CapEx不下修，实物订单/单位量下修 |
| 技术效率超预期 | Rubin/custom ASIC tokens/MW提升使需求不追加 | 每token CapEx下降；需观察需求弹性是否抵消 |

### 10.2 月度/季度跟踪清单

| 频率 | 指标 | 关键来源 | 情景切换信号 |
|---|---|---|---|
| 每季 | MSFT/AMZN/GOOG/META/ORCL CapEx、短/长寿命资产mix | IR/10-Q | 合计guide±10% |
| 每季 | NVDA/AMD/AVGO AI/DC revenue；Dell/HPE backlog | IR | GPU/rack orders与收入差 |
| 每季 | MU/Samsung/SKhynix HBM bit/ASP/yield；TSMC package | IR | HBM4 qualification、CoWoS缓解 |
| 每季 | ETN/VRT/GEV/MOD orders、backlog、book-to-bill | IR | `<1.0x`或lead time快速下降 |
| 每月/季 | ERCOT/PJM large load、service agreement、EIA load | ISO/EIA/FERC | signed/energized MW vs申请 |
| 每季 | CBRE/JLL inventory、under construction、pre-lease、rent | 行业报告 | vacancy、construction MW、租金 |
| 每季 | DLR/EQIX/APLD/IRM leased MW与COD | IR | rent commencement与延期 |
| 每季 | CoreWeave/NeoCloud backlog、active power、DSCR/融资 | IR/SEC | active/contracted转换、客户集中 |
| 每半年 | liquid cooling attach、RMA/field failure、CDU capacity | vendor/技术文档 | 100kW+ rack验收速度 |

### 10.3 风险排序

1. **电力/许可风险（高）：**queue中大量重复申请，ERCOT `410GW` 绝非可交付量；模型只认 signed/adjusted/energized。
2. **需求/资本回报风险（高）：**AI收入可能无法支撑 `$500B+` 年度美国建设；高性能/瓦效率也可能降低所需MW。
3. **融资与客户集中（中高）：**NeoCloud backlog可见但债务、单一客户、GPU残值风险高。
4. **供应链错配（中高）：**HBM、package、transformer、CDU任一短缺都会使其他设备闲置。
5. **价格与数量混淆（中）：**2026 memory/components涨价可推高名义CapEx而不增加物理量。
6. **重复计算（中）：**客户预付、客户供货GPU、colo租赁、OEM整机与HBM/package最易双算。
7. **地理归属（中）：**美国客户海外项目与美国供应链收入不等于美国境内建设；本报告优先按资产地计。
8. **技术替代（中）：**custom ASIC、CPO、800VDC、immersion改变模块份额，但不会同时都按乐观渗透。

## 十一、Reference 和数字来源附录

### 11.1 核心来源表

| ID | 来源 | 日期 | 层级 | 支持的数字/判断 | 一手 | 置信度 | 备注 |
|---|---|---|---|---|---|---|---|
| R1 | [Microsoft FY2026 Q3 earnings call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3) | 2026-04-29 | 公司IR | CY2026 CapEx约 `$190B`；Q3 `$31.9B`；约2/3短寿命GPU/CPU；新增1GW | 是 | 高 | transcript CapEx段 |
| R2 | [Amazon 2026Q1 results](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-First-Quarter-Results/) / [10-Q](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000014/amzn-20260331.htm) / [2025Q4 results](https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx) | 2026-02-05/04-29 | 公司IR/SEC | 2026 CapEx约 `$200B`；Q1 cash CapEx `$43.2B`；2.1M+ AI chips、OpenAI/Anthropic合同 | 是 | 高 | 扣fulfillment与海外 |
| R3 | [Alphabet 2025Q4 earnings call](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx) | 2026-02-04 | 公司IR | 2026 CapEx `$175-185B`；机器约60%、DC+network约40% | 是 | 高 | 机器仍含非AI |
| R4 | [Meta 2026Q1 results](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/) | 2026-04-29 | 公司IR | 2026 CapEx `$125-145B`，Q1 `$19.84B` | 是 | 高 | 含finance lease principal |
| R5 | [Oracle FY2026 results](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Record-Q4-and-FY-2026-Results-Driven-by-Cloud-Infrastructure--Cloud-Applications/) | 2026-06-10 | 公司IR | FY26 CapEx `$55.663B`、RPO `$638B`、预付/客户供货硬件 `$75B` | 是 | 高 | 去重关键 |
| R6 | [CoreWeave 2026Q1 results](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-First-Quarter-2026-Results/) | 2026-05-07 | 公司IR | active power `>1GW`、contracted `>3.5GW`、backlog近 `$100B` | 是 | 高 | backlog非当年收入 |
| R7 | [OpenAI five Stargate sites](https://openai.com/index/five-new-stargate-sites/) / [SB Energy partnership](https://openai.com/index/stargate-sb-energy-partnership/) | 2025-09-23/2026-01-09 | 项目一手 | 近7GW、未来三年 `>$400B`；Milam首期1.2GW | 是 | 中高 | 多年规划且有重叠 |
| R8 | [CBRE North America Data Center Trends H2 2025](https://www.cbre.com/insights/books/north-america-data-center-trends-h2-2025) | 2026-02-25 | 行业 | 八大市场供应 `9,432MW`、在建 `5,994.4MW`、vacancy `1.4%`、吸纳 `2,497.6MW` | 否 | 高 | 美国物理校验 |
| R9 | [Cushman Global Data Center Market Comparison 2026](https://www.cushmanwakefield.com/en/germany/news/2026/05/global-data-center-market-comparison) | 2026-05-29 | 行业 | Americas operational `43.4GW`、under construction `25.3GW`、pipeline `191.3GW` | 否 | 中 | pipeline大幅降权 |
| R10 | [Applied Digital 2026 investor presentation](https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-26-000036/apld_invxinvestorpresent.htm) | 2026-04 | 公司IR/SEC | `1GW` critical IT在建、`900MW`已签；facility `$11-13M/MW` | 是 | 中高 | 开发商自报 |
| R11 | [Applied Digital FY3Q26](https://ir.applieddigital.com/news-events/press-releases/detail/148/applied-digital-reports-fiscal-third-quarter-2026-results) | 2026-04-08 | 公司IR | 100MW运营、后续2026/2027交付，项目时间线 | 是 | 高 | COD校验 |
| R12 | [ERCOT Large Load Update](https://www.ercot.com/files/docs/2026/04/01/ERCOT_LargeLoad_Update_April2026_B-C_-Hearing.pdf) | 2026-04-01 | ISO一手 | 约 `410GW` large-load requests、约87%数据中心 | 是 | 中高 | 意向/重复，不是预测 |
| R13 | [ERCOT preliminary long-term forecast](https://www.ercot.com/files/docs/2026/04/15/12-CEO-Update.pdf) | 2026-04-15 | ISO一手 | adjusted non-crypto DC：2026 `7.4GW`、2027 `39.7GW` | 是 | 中 | 含项目概率调整仍很激进 |
| R14 | [PJM 2025 year in review](https://insidelines.pjm.com/2025-year-in-review-planning-prepares-for-burgeoning-electricity-demand/) | 2025-12 | ISO一手 | 2025-2030 数据中心负荷增量约 `30GW` | 是 | 高 | PJM区域 |
| R15 | [EIA March 2026 data-center load analysis](https://www.eia.gov/todayinenergy/detail.php?id=67344) | 2026-03-12 | 政府一手 | 2026/2027全美load增长、ERCOT/PJM为最快区域，高需求敏感性 | 是 | 高 | 电力总量约束 |
| R16 | [JLL 2026 Global Data Center Outlook](https://www.jll.com/en-ca/insights/data-center-outlook.html) | 2026-01 | 行业 | 2026全球建设成本约 `$11.3M/MW` | 否 | 中高 | 非AI/全球平均 |
| R17 | [Digital Realty 2026Q1 results](https://investor.digitalrealty.com/news-releases/news-release-details/digital-realty-reports-first-quarter-2026-results) | 2026-04-23 | 公司IR | bookings、`$1.8B` signed-not-commenced rent、19月lag | 是 | 高 | REIT收入时点 |
| R18 | [Iron Mountain 2026Q1 results](https://investors.ironmountain.com/news/news-details/2026/Iron-Mountain-Reports-First-Quarter-2026-Results/default.aspx) | 2026-05 | 公司IR | 2026年前四个月已租 `32MW`，24个月约 `400MW`可通电/可用 | 是 | 高 | colo pipeline校验 |
| R19 | [OpenAI-Oracle Stargate 4.5GW](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) | 2025-07-22 | 项目一手 | 新增4.5GW、合计超5GW开发中、可运行超2M chips | 是 | 中高 | 多年项目，需按COD折减 |
| R20 | [NVIDIA GB300 NVL72 reference architecture](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) | 2026-06 | 技术一手 | 72 GPU/rack、最高 `142kW`、8×33kW power shelf | 是 | 高 | 物理换算主锚 |
| R21 | [NVIDIA FY2026 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/) / [Rubin production](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Ramps-Into-Full-Production-to-Power-Agentic-AI-Factories-Worldwide/default.aspx) | 2026-02-25/05-31 | 公司IR | FY26 DC `$193.7B`；Rubin量产/2H26供货 | 是 | 高 | roadmap与收入 |
| R22 | [Eaton 2026Q1 results](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html) | 2026-05-05 | 公司IR | Electrical Americas orders +42%、backlog +44%、book-to-bill 1.2 | 是 | 高 | 电力设备强度 |
| R23 | [Vertiv 2026Q1 results](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx) / [MegaMod HDX](https://investors.vertiv.com/news/news-details/2026/Vertiv-Introduces-New-Modular-Liquid-Cooling-Infrastructure-Solution-to-Support-High-Density-Compute-Requirements-in-North-America-and-EMEA/default.aspx) | 2026-04-22/01-14 | 公司IR | sales +30%、FY organic +29-31%、50至100kW+ rack | 是 | 高 | cooling/power |
| R24 | [GE Vernova 2026Q1 results](https://www.gevernova.com/news/press-releases/ge-vernova-reports-first-quarter-2026-financial) | 2026-04-22 | 公司IR | DC electrification orders `$2.4B`、gas backlog+slot `100GW` | 是 | 高 | power订单主锚 |
| R25 | [Micron FY2026Q1 presentation](https://investors.micron.com/static-files/530bd7ed-a8c8-4687-af4a-8c129f740e09) | 2025-12-17 | 公司IR | 2026 HBM价量锁定；HBM TAM `$35B`→`$100B`，约40%CAGR | 是 | 高 | 全球TAM |
| R26 | [Micron FY2026Q3 results](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-record-results-third-quarter) | 2026-06-24 | 公司IR | HBM4量产、HBM4E 2027、DC SSD revenue `>$5B` | 是 | 高 | memory/storage |
| R27 | [Samsung HBM4 commercial shipment](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | 2026-02-12 | 公司一手 | HBM4量产与商业出货 | 是 | 高 | 供应缓解证据 |
| R28 | [TSMC 2026Q1 transcript](https://investor.tsmc.com/schinese/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf) | 2026-04-16 | 公司IR | 大尺寸CoWoS仍为主、CoPoS pilot | 是 | 中高 | 未给精确capacity |
| R29 | [Bloom-Oracle 2.8GW agreement](https://investor.bloomenergy.com/press-releases/press-release-details/2026/Bloom-Energy-and-Oracle-Expand-Strategic-Partnership-to-Deploy-up-to-2-8-GW-to-Accelerate-AI-Infrastructure-Build-Out/default.aspx) | 2026-04-13 | 项目/公司一手 | 初始1.2GW、框架2.8GW | 是 | 高 | BYOP硬订单 |
| R30 | [Caterpillar/AIP 2GW agreement](https://investors.caterpillar.com/news/news-details/2026/American-Intelligence--Power-Forms-Strategic-Alliance-with-Caterpillar-and-Boyd-CAT-to-Deploy-2-Gigawatts-of-Dedicated-Power-for-Hyperscale-AI-Infrastructure/default.aspx) | 2026-01-28 | 项目/公司一手 | 2026-09交付、2027 2GW在线计划 | 是 | 中高 | 项目执行待验证 |
| R31 | [GE Vernova gas turbine fleet/update](https://www.gevernova.com/news/press-releases/ge-vernova-ha-gas-turbine-fleet-surpasses-4-million) | 2026-05-26 | 公司一手 | 数据中心约占gas turbine合同20% | 是 | 中高 | 全球合同 |
| R32 | [Bloom 2026 Data Center Power Report](https://investor.bloomenergy.com/press-releases/press-release-details/2026/Data-Centers-Plan-to-Reduce-Reliance-on-Grid-Finds-Bloom-Energys-2026-Power-Report/default.aspx) | 2026-01-20 | 公司调研/行业 | 受访者预计2030约1/3数据中心全现场供电；utility时间差1.5-2年 | 否 | 中 | 152名决策者双盲调查，非订单 |
| R33 | [Digital Realty 2026Q1](https://investor.digitalrealty.com/news-releases/news-release-details/digital-realty-reports-first-quarter-2026-results) | 2026-04-23 | 公司IR | 19月租赁起租lag | 是 | 高 | 收入错位 |
| R34 | [Eaton Nebraska switchgear expansion](https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-expands-operations-in-nebraska-with-new-manufacturing-facility.html) | 2026-04-08 | 公司一手 | 2027H1投产、370k平方英尺 | 是 | 高 | 产能缓解窗口 |
| R35 | [Vertiv Ohio liquid-cooling expansion](https://investors.vertiv.com/news/news-details/2026/Vertiv-to-Expand-Ohio-Manufacturing-to-Boost-U-S--Production-of-Critical-Thermal-Management-Technologies-for-AI-Data-Centers/) | 2026-03-30 | 公司一手 | 约 `$50M`投资、2027Q2投产 | 是 | 高 | 产能缓解窗口 |
| R36 | [Broadcom FY2026Q2 results](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial) | 2026-06-03 | 公司IR | AI revenue `$10.8B`、+143%；Q3预期 `$16B` | 是 | 高 | XPU+network合计 |
| R37 | [Arista 2026Q1 results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-First-Quarter-2026-Financial-Results/default.aspx) / [1.6T portfolio](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Introduces-Next-Generation-1-6Terabit-Portfolio-for-AI-Fabrics/default.aspx) | 2026-05-05/06-09 | 公司IR | Q1 +35.1%；1.6T 2026Q4起 | 是 | 高 | 网络拐点 |
| R38 | [Marvell 2026 proxy](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001104659-26-060253/tm261486-1_def14a.htm) | 2026-05-13 | SEC | FY26 DC revenue `>$6B`，optical约一半 | 是 | 高 | 数据中心拆分 |
| R39 | [Dell FY2027Q1 transcript](https://investors.delltechnologies.com/static-files/b63ffff9-b729-403b-a231-c6af05667759) | 2026-05-28 | 公司IR | AI orders `$24.4B`、revenue `$16.1B`、backlog `$51.3B` | 是 | 高 | server订单主锚 |
| R40 | [HPE FY2026Q1 presentation](https://investors.hpe.com/~/media/Files/H/HP-Enterprise-IR/documents/q1-2026/q1-2026-earnings-presentation.pdf) | 2026-03-09 | 公司IR | AI backlog `>$5B`、pipeline multiples | 是 | 高 | enterprise/sovereign |
| R41 | [AMD 2026Q1 results](https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results) | 2026-05-05 | 公司IR | DC revenue `$5.8B`、+57%；Meta up to 6GW | 是 | 高 | 首1GW较确定，其余规划 |
| R42 | [Modine FY2026Q4 results](https://investors.modine.com/news/news-details/2026/Modine-Reports-Fourth-Quarter-Fiscal-2026-Results/default.aspx) | 2026-05-26 | 公司IR | hyperscaler chiller协议约 `$4B`至2029 | 是 | 高 | 客户未具名 |
| R43 | [Quanta Services 2026Q1](https://investors.quantaservices.com/news-events/press-releases/detail/396/quanta-services-reports-first-quarter-2026-results) | 2026-04-30 | 公司IR | record backlog `$48.5B` | 是 | 高 | 不全为data center |
| R44 | [Applied Materials FY2026Q2](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-second-quarter-2026-results) | 2026-05 | 公司IR | semi equipment CY26 growth `>30%` | 是 | 高 | AI+其他先进制程 |
| R45 | [Teradyne 2026Q1](https://investors.teradyne.com/news-events/press-releases/detail/440/teradyne-reports-first-quarter-2026-results) | 2026-04-29 | 公司IR | semiconductor test `$1.111B`、AI相关约70%公司收入 | 是 | 高 | test主锚 |
| R46 | [WD FY2026Q3](https://investor.wdc.com/news-releases/news-release-details/wd-reports-fiscal-third-quarter-2026-financial-results) | 2026-04 | 公司IR | revenue `$3.337B`、+45%；AI数据持久化判断 | 是 | 高 | HDD-only公司 |
| R47 | [Seagate FY2026Q2](https://investors.seagate.com/news/news-details/2026/Seagate-Technology-Reports-Fiscal-Second-Quarter-2026-Financial-Results/) | 2026-01-27 | 公司IR | revenue `$2.825B`、AI/exabyte需求 | 是 | 高 | 全球/非AI混合 |
| R48 | [Equinix 2026Q1](https://investor.equinix.com/news-events/press-releases/detail/1107/equinix-reports-first-quarter-results-and-raises-full-year) | 2026-04 | 公司IR | record backlog、2026 non-recurring CapEx约 `$3.8B`（不含xScale/land） | 是 | 高 | colo补充校验 |
| R49 | [CBRE Global Data Center Trends 2026](https://www.cbre.com/insights/reports/global-data-center-trends-2026) | 2026-06-17 | 行业 | 北美top4库存+33%、NoVA vacancy 0.3%、供给至2030受限 | 否 | 高 | 需求/租金校验 |
| R50 | [FERC large-load show-cause remarks](https://www.ferc.gov/news-events/news/commissioner-rosners-remarks-large-load-show-cause-orders-e-7-e-12-june-18-2026) | 2026-06-18 | 监管一手 | large-load重复“shopping”、灵活接入与成本分配问题 | 是 | 高 | queue折减依据 |
| R51 | 美股合并行情快照 | 2026-07-10 16:00-17:15 PT | 市场数据 | 第8.4节18家公司收盘/最新价 | 否 | 中高 | 仅定义研究时点；未用于模型，需在拆股后复核 |

### 11.2 估算链条、来源日期与置信度汇总

| 结论 | 估算链条 | 数据日期 | 置信度 | 首要反证 |
|---|---|---|---|---|
| 2026务实 `$390-470B` | 平台CapEx→AI/DC占比→美国占比→转化率+独立项目-重复 | 2026-04至06 | 中高 | energization `<6GW` 或CapEx下修>15% |
| 2027务实 `$500-620B` | 2026基数×27-34%+Rubin/ASIC/BYOP/AI Factory转化 | 截至2026-07-09 | 中 | power/financing导致项目后移>12月 |
| 2026 `7.5-10.5GW` | `$390-470B ÷ $42-58M/MW`，与在建/pre-lease/ISO校验 | 2026Q1/Q2 | 中 | signed/energized MW显著低于模型 |
| compute `$152-202B` | 4.6-6.2M accelerators×经济内容ASP+CPU/OEM | 2026Q1/Q2 | 中 | custom ASIC成本、customer-supplied重复 |
| power `$35-52B` | MW×`$4.5-7.5M/MW`，用ETN/GEV/VRT订单校验 | 2026Q1 | 中高 | onsite generation归属与交付时点 |
| cooling `$16-28B` | rack×liquid attach×BOM+facility HVAC | 2026-01至07 | 中 | cold plate/OEM重复、标准化降价 |
| memory `$31-47B` | accelerator×HBM容量/ASP+CPU memory | 2025-12至2026-06 | 中高 | HBM ASP/bit mix快速变化 |
| storage `$16-28B` | AI compute/data规模×SSD/HDD/storage mix | 2026Q1/Q2 | 中低 | AI专属与普通cloud无法精确拆分 |

---

**结论性判断：**2026-2027 不是单一“GPU周期”，而是 compute 先行、network/memory同步、power/MEP/cooling决定可交付上限、storage/energy在2027补涨的多层资本周期。最好的股票映射不是寻找最多“AI”标签，而是寻找同时满足 **可量化订单池、客户认证、产能/交期稀缺、backlog可转收入、毛利或服务attach可留存** 的公司；最危险的映射则是把 queue、pipeline、框架协议、整机销售额与嵌入式 HBM/package 重复相加。
