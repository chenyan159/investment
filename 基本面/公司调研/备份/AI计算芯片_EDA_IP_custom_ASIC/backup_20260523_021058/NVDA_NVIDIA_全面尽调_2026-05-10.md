# NVDA / NVIDIA Corporation（英伟达）全面尽调（2026-05-15 重做）

> 研究口径：本版按《公司调研方案》9 项要求重做；旧版仅作为目录结构参考，核心财务、估值、出口管制、产品路线、供应链读穿均重新核验。  
> 动态数据截止：2026-05-15 美股收盘；公司最新已披露完整财报为 FY2026 Q4 / FY2026 全年（财年截至 2026-01-25，2026-02-25 披露）。下一次财报预定 2026-05-20 美股盘后。  
> 投资结论先行：NVDA 仍是 AI 算力链的最高质量资产之一，但 2026 年以后胜负手已经从“GPU 单卡领先”升级为“AI factory 机架级系统 + 网络 + HBM/CoWoS 供给 + 推理软件栈 + 电力约束”的综合交付能力。中国 H20/H200 恢复销售不能作为基准情景，只能作为政策期权。

---

## 0. 一页结论

### 0.1 投资判断

- 公司定位变化：NVIDIA 已不再是单纯 GPU 公司，而是在 10-K 中把自己定义为 “data center scale AI infrastructure company”。FY2026 Data Center 收入 $193.7B，同比 +68%，占总收入约 89.7%；其中 Q4 FY2026 Data Center 单季 $62.3B，Compute $51.3B，Networking $11.0B。核心竞争力已经是 GPU、NVLink、Spectrum-X/InfiniBand、Grace/Vera CPU、DPU/NIC、软件和机架级液冷系统的组合。
- 近 12 个月基本盘：公司 Q1 FY2027 指引收入 $78.0B ±2%，且明确不假设来自中国的 Data Center compute 收入。以此年化已经接近 $312B 收入口径，说明 Blackwell/Blackwell Ultra/GB300 不是概念订单，而是正在进入主收入曲线。
- 政策变量：H20 在 FY2026 Q1 触发 $4.5B 存货/采购承诺相关费用，Q1 另有 $2.5B H20 收入无法发货，Q2 指引反映约 $8.0B H20 收入损失。FY2026 10-K 披露美国政府在 2026-02 给了少量 H200 对特定中国客户许可证，但截至披露日无 H200 收入，且 NVIDIA 不确定中国是否允许进口；2026-05-14/15 新闻流继续显示“美国批准/许可”与“实际交付”之间存在断点。因此中国恢复不是模型基准，只能列入上行情景。
- 供给约束读穿：FY2026 末库存 $21.4B、供应相关承诺 $95.2B、云服务协议承诺 $27.0B。这不是普通芯片公司库存周期，而是 AI factory 交付链锁定：HBM3E/HBM4、CoWoS/先进封装、ABF、液冷、交换机/NIC、供电和数据中心电力共同决定可交付收入。
- 估值状态：2026-05-15 收盘价 $225.32，市值约 $5.46T，P/E 48.11x，Forward P/E 28.13x，P/S 26.44x，Forward P/S 15.19x。估值已经反映 FY2027 高增长延续；股价进一步上行需要 Q1/Q2 证明 GB300/Blackwell Ultra 爬坡、Networking 继续超线性增长、Rubin 2026H2/2027 可见度提高，而不是只靠中国许可新闻。

### 0.2 最重要的结论变化

1. 从“GPU 缺货”升级为“机架级 AI factory 供给链缺口”：NVDA 的收入增量越来越绑定 GB200/GB300 NVL72、NVLink 域、Spectrum-X/InfiniBand、ConnectX、BlueField、Grace/Vera CPU 和液冷机柜；传统按 GPU ASP × 数量的模型会低估 Networking 与系统级内容量。
2. 中国收入恢复概率低于 headline 观感：H200 政策从“美国侧可个案许可”到“实际进口/交付/客户接收/收费”还有多道门槛；10-K 与 2026-05 新闻流均支持“未交付/未确认收入”的判断。
3. Rubin 不是远期 PPT，而是下一轮系统迭代的核心观察项：官方 Vera Rubin NVL72 页面已经披露 HBM4、NVLink 6、ConnectX-9、BlueField-4、72 GPU/36 CPU 机架规格；但商业收入节奏仍应放在 2026H2-2027，不能提前并入 FY2027 上半年基准。
4. Networking 已成为独立高弹性业务：Q4 FY2026 Networking 收入 $11.0B，同比 +263%，FY2026 $31.4B，同比 +142%。NVLink/Spectrum-X/InfiniBand 的 attach rate 是 2026 年 EPS 超预期的关键。
5. 估值容错率下降：Forward P/E 约 28x 看似不贵，但 P/S 和市值体量要求未来 12 个月收入继续跃迁到 $330B-$400B 区间；任何 HBM/CoWoS/电力/中国政策/客户 capex 放缓都会放大波动。

---

## 1. 公司整体业务、近三年变化、定位与估值财务

### 1.1 公司业务与战略定位

NVIDIA 当前核心业务可以按“AI factory 分层”理解：

| 层级 | 代表产品/能力 | 投资含义 |
|---|---|---|
| 加速计算芯片 | Hopper、Blackwell、Blackwell Ultra、GB200、GB300、Rubin GPU | 仍是收入主体，但竞争不再只是单卡性能，而是系统吞吐/能效/供货 |
| CPU + GPU 模组 | Grace-Blackwell、GB200、GB300、Vera Rubin | 提升整机 ASP 与客户锁定，扩大 NVIDIA 在服务器 BOM 中的内容量 |
| Scale-up 网络 | NVLink、NVLink Switch、NVLink 6 | 大模型训练/推理的核心护城河，决定 72 GPU/更大域的效率 |
| Scale-out 网络 | Quantum-X800 InfiniBand、Spectrum-X Ethernet、ConnectX-8/9、BlueField DPU | Networking 从配套件变成收入弹性来源 |
| 软件与模型平台 | CUDA、Dynamo、NIM、AI Enterprise、Omniverse、Nemotron、Cosmos | 提高切换成本；财报未单列完整软件收入，但决定客户粘性和毛利韧性 |
| 生态/垂直应用 | Cloud、enterprise AI、robotics、autonomous driving、industrial digital twins | 中长期 TAM 扩展，短期财务贡献仍远低于 Data Center |

### 1.2 近三年变化

| 维度 | FY2024 前后 | FY2025 | FY2026 / 2026 年现状 |
|---|---|---|---|
| 增长驱动 | Hopper 训练需求爆发 | Hopper 延续 + Blackwell 开始放量 | Blackwell/Blackwell Ultra/GB300 与 Networking 成为主引擎 |
| 客户结构 | CSP 和互联网大客户主导 | 大型 CSP 约占 Data Center 一半上下 | Q4 FY2026 hyperscaler 仍略高于 Data Center 50%，但非 hyperscaler DC 客户增长更快 |
| 产品形态 | GPU/加速卡为主 | GB200 NVL72 机架级系统开始进入收入 | GB300 NVL72 “available now”，Rubin/Vera Rubin 进入下一代机架平台 |
| 供应瓶颈 | GPU/HBM/CoWoS | HBM3E、CoWoS、网络、液冷 | HBM3E 12Hi、HBM4、CoWoS、ABF、液冷、电力并列瓶颈 |
| 地缘政策 | A100/H100 中国限制 | H20 作为合规替代 | H20 许可证限制；H200 个案许可但未确认收入，中国市场实质受限 |

### 1.3 最新股价与估值

截至 2026-05-15 美股收盘：

| 指标 | 数值 | 备注 |
|---|---:|---|
| 收盘价 | $225.32 | StockAnalysis / Yahoo chart API，2026-05-15 |
| 盘后价 | $224.41 | StockAnalysis |
| 市值 | 约 $5.46T | StockAnalysis |
| Enterprise Value | 约 $5.66T | StockAnalysis statistics |
| P/E | 48.11x | TTM |
| Forward P/E | 28.13x | 市场一致预期口径 |
| P/S | 26.44x | StockAnalysis statistics |
| Forward P/S | 15.19x | StockAnalysis statistics |
| P/FCF | 59.06x | StockAnalysis statistics |
| 52 周区间 | $129.16-$236.54 | StockAnalysis |

估值判断：Forward P/E 28x 对一个 FY2027 收入仍可能 >50% 增长、净利率 >50% 的公司并不离谱，但 P/S 约 26x 表明市场已经把“AI factory capex 超周期”作为基准。当前估值的边际风险不是 FY2026 财报，而是 FY2027 后半段和 FY2028 的持续性。

### 1.4 收入增长、利润率与资产负债表健康度

| 指标 | FY2026 | 变化/读法 |
|---|---:|---|
| 总收入 | $215.938B | 同比 +65% |
| GAAP 毛利率 | 71.1% | Q4 回到 75.0%，H20 charge 压低全年 |
| Non-GAAP 毛利率 | 71.3% | 同上 |
| GAAP 净利润 | $120.067B | 同比约 +65% |
| GAAP 稀释 EPS | $4.90 | 同比 +66.7%（StockAnalysis） |
| 净利率 | 55.6% | $120.067B / $215.938B |
| 自由现金流率 | 44.77% | StockAnalysis statistics |
| 现金 + 有价证券 | $62.556B | FY2026 10-K |
| 应收账款 | $38.466B | DSO 约 51 天，Q4 CFO commentary |
| 存货 | $21.403B | Blackwell/Rubin 供给链锁定与爬坡风险并存 |
| 流动资产 / 流动负债 | $125.605B / $32.163B | 流动比率约 3.9x |
| 长期债务 | $7.469B | 债务压力低 |
| 股东权益 | $157.293B | 资产负债表很强 |
| 供应相关承诺 | $95.2B | 基本覆盖 FY2027 供给锁定；也是需求波动时的固定承诺风险 |
| 云服务协议承诺 | $27.0B | 支持自身 AI/软件/云服务，但也增加长期采购承诺 |

结论：资产负债表不是风险点；真正的财务风险在于供应链承诺与客户需求节奏错配。一旦 hyperscaler capex 放缓或产品切换延迟，库存与预付款会先放大营运资本波动。

---

## 2. 最新及最近四次财报：五季度对比

NVIDIA 未披露标准意义的 backlog/bookings。以下用公司已披露的供应承诺、库存、云服务承诺、H20 未发货/损失、下一季指引和管理层表述作为订单/交付紧张度 proxy。

| 财季 | 披露日 | 总收入 | GAAP GM | GAAP 净利润 | Data Center | DC Compute | DC Networking | Gaming | ProViz | Auto | backlog / bookings / lead-time proxy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Q4 FY2025 | 2025-02-26 | $39.331B | 73.0% | $22.091B | $35.580B | $32.556B | $3.024B | $2.544B | $0.511B | $0.570B | Blackwell Q4 收入 $11B，公司称最快产品爬坡；供应承诺 $30.8B，云服务承诺 $10.9B |
| Q1 FY2026 | 2025-05-28 | $44.062B | 60.5% | $18.775B | $39.112B | $34.155B | $4.957B | $3.763B | $0.509B | $0.567B | H20 许可证导致 $4.5B charge；Q1 有 $2.5B H20 无法发货；Q2 指引反映约 $8B H20 损失 |
| Q2 FY2026 | 2025-08-27 | $46.743B | 72.4% | $26.422B | $41.096B | $33.844B | $7.252B | $4.287B | $0.601B | $0.586B | DC Compute q/q -1% 主要因 $4.0B H20 reduction；无对中国客户 H20 销售；采购承诺 $45.8B |
| Q3 FY2026 | 2025-11-19 | $57.006B | 73.4% | $31.910B | $51.215B | $43.028B | $8.187B | $4.265B | $0.760B | $0.592B | Blackwell Ultra 成为客户主架构；H20 销售不重要；供应承诺 $50.3B，Q4 指引 $65B |
| Q4 FY2026 | 2026-02-25 | $68.127B | 75.0% | $42.960B | $62.314B | $51.334B | $10.980B | $3.727B | $1.321B | $0.604B | FY2026 末供应相关承诺 $95.2B；库存 $21.4B；Q1 FY2027 指引 $78B 且不含中国 DC compute |

### 2.1 五季度关键读法

- Data Center 占比极高：Q4 FY2026 Data Center 占收入约 91.5%；FY2026 Data Center 占收入约 89.7%。Gaming、ProViz、Auto 都还在增长，但已不决定公司估值主线。
- Networking 弹性超过 Compute：Q4 FY2026 DC Networking 同比 +263%，FY2026 同比 +142%，明显快于 DC Compute。GB200/GB300/Rubin 机架化会持续提高网络 attach rate。
- 毛利率恢复但需盯产品切换：Q1 FY2026 H20 charge 使毛利率降至 60.5%；Q4 已恢复至 75.0%。未来毛利率取决于 Blackwell Ultra/GB300 良率、HBM 成本传导、系统级 ASP 和 Rubin 初期良率。
- 供应承诺暴增是双刃剑：$95.2B supply commitments 支撑未来 12 个月收入可见度，但也意味着 NVIDIA 对 HBM、CoWoS、先进封装、板卡/系统和产能的锁定非常重。

---

## 3. 最新指引、收入结构、业务占比与产品地图

### 3.1 最新公开指引

截至本报告日期，最新公司指引为 2026-02-25 公布的 Q1 FY2027：

| 项目 | 指引 |
|---|---:|
| 收入 | $78.0B ±2% |
| GAAP / Non-GAAP gross margin | 74.9% / 75.0% ±50bps |
| GAAP / Non-GAAP opex | $7.7B / $7.5B |
| 税率 | 17%-19% |
| 中国假设 | 不假设来自中国的 Data Center compute 收入 |

对模型的含义：Q1 FY2027 指引较 Q4 FY2026 实际收入 $68.1B 中值环比约 +14.5%。在不含中国 DC compute 的前提下仍能给出 $78B，说明 Blackwell/GB300 及网络需求是足以支撑 near-term growth 的主变量。

### 3.2 FY2026 收入结构

| 业务 | FY2026 收入 | 同比 | 占总收入 |
|---|---:|---:|---:|
| Data Center | $193.737B | +68% | 89.7% |
| 其中：DC Compute | $162.361B | +59% | 75.2% |
| 其中：DC Networking | $31.376B | +142% | 14.5% |
| Gaming | $16.042B | +41% | 7.4% |
| Professional Visualization | $3.191B | +70% | 1.5% |
| Automotive | $2.349B | +39% | 1.1% |

低增长/低相关业务处理：本报告不把 Gaming/ProViz/Auto 作为核心估值驱动，只在总收入和尾部上行情景中保留。NVDA 的投资主线几乎完全由 Data Center compute + networking + AI factory 系统决定。

### 3.3 产品/模型映射

| 产品/平台 | 当前阶段 | 对应客户/工作负载 | 投资关键点 |
|---|---|---|---|
| Hopper / H100 / H200 | 成熟/存量升级 | 训练、推理、存量集群扩容 | H200 中国许可是政策变量；非中国市场逐步让位 Blackwell |
| H20 | 中国合规产品，政策受限 | 中国 DC compute | FY2026 Q1/Q2 已体现重大收入损失；不再作为基准增长引擎 |
| GB200 NVL72 | Blackwell 第一代机架平台 | 大模型训练/推理，72 GPU NVLink 域 | 证明机架级系统商业化路径 |
| GB300 NVL72 / Blackwell Ultra | 当前主增量 | reasoning AI、agentic AI、video generation、推理吞吐 | 官方页面标注 available now；Q1/Q2 FY2027 主要收入弹性 |
| Spectrum-X / Quantum-X800 / ConnectX-8 | 当前主增量 | scale-out AI 网络 | Networking 高增长的核心，attach rate 提升 |
| Vera Rubin NVL72 | 下一代平台 | trillion-parameter model、长上下文推理、训练/推理一体 | HBM4、NVLink 6、ConnectX-9、BlueField-4；收入应主要看 2026H2/2027 |
| LPX / SRAM 推理机架 | 下一代推理扩展 | 超长上下文、低延迟推理 | 可能提高推理侧系统 ASP 和能效，但当前缺少收入拆分 |
| Dynamo / NIM / CUDA / AI Enterprise | 软件栈 | 推理服务、企业部署、模型优化 | 不单独披露完整收入，主要体现在客户锁定、毛利和生态壁垒 |

---

## 4. 关键产品当前贡献、增长、AI 基建重要性、紧缺度与定价权

评分：5 = 最高，1 = 最低。收入贡献为研究估算或公司披露口径，未披露项不做虚假精确化。

| 产品/业务 | 当前收入贡献 | 未来 12 个月增长 | AI 基建重要性 | 紧缺度 | 垄断/议价力 | 结论 |
|---|---:|---:|---:|---:|---:|---|
| Blackwell / Blackwell Ultra / GB200 / GB300 compute | 5 | 5 | 5 | 5 | 5 | 当前主收入曲线；Q1 FY2027 $78B 指引的核心支撑 |
| DC Networking：NVLink、Spectrum-X、InfiniBand、ConnectX、BlueField | 4 | 5 | 5 | 4 | 4 | Q4 单季 $11B；机架级 AI factory 越大，网络内容量越高 |
| HBM/CoWoS 绑定的系统供给 | 不是 NVDA 单独收入项 | 5 | 5 | 5 | 4 | 决定 NVDA 能确认多少收入；也是供应链利润外溢方向 |
| Rubin / Vera Rubin / LPX | 1-2 | 4-5 | 5 | 4 | 5 | 2026H2/2027 关键；当前不宜过早确认为 FY2027 上半年收入 |
| H20/H200 中国产品 | 0-1 | 1-4 | 3 | 政策紧缺 | 2-4 | 政策期权，不是基准；美国许可和中国进口是两套约束 |
| Gaming RTX | 2 | 2-3 | 1 | 2 | 3 | 仍优质，但不决定估值 |
| Automotive | 1 | 3 | 2-3 | 2 | 3 | 中长期可选项，短期规模太小 |
| Software / CUDA / NIM / Dynamo | 财报未完整拆分 | 4 | 5 | 3 | 5 | 护城河极深；短期利润主要嵌入硬件系统和服务 |

---

## 5. 一年后产品收入贡献三情景

以下为研究模型，不是公司指引。基准从 Q4 FY2026 单季 $68.1B、Q1 FY2027 指引 $78B 和 FY2026 全年 $215.9B 出发，并结合项目内 AI 数据中心 capex、HBM/CoWoS 供应链资料。

### 5.1 未来 12 个月收入框架

| 情景 | 未来 12 个月总收入 | Data Center 收入 | 毛利率 | 核心假设 |
|---|---:|---:|---:|---|
| 基准 | $330B-$360B | $300B-$325B | 74%-76% | GB300/Blackwell Ultra 按 Q1 指引继续爬坡；Networking attach rate 提升；中国 DC compute 近似为零 |
| 乐观 | $385B-$430B | $350B-$395B | 75%-77% | GB300 供给超预期，HBM3E/CoWoS 释放，Spectrum-X 大规模替代传统以太网；Rubin 2026H2 开始有可见收入 |
| 极端上行 | $460B-$520B | $420B-$480B | 76%-79% | AI capex 继续上修，Rubin/LPX 预付款和早期交付强，部分 H200/H20 中国交付恢复，电力/液冷瓶颈未明显拖累 |

### 5.2 按产品/业务拆分

| 产品/业务 | 当前基准 | 未来 12 个月基准 | 乐观 | 极端上行 |
|---|---:|---:|---:|---:|
| Blackwell/GB300 DC Compute | Q4 FY2026 DC Compute 年化约 $205B | $220B-$260B | $275B-$330B | $350B-$410B |
| DC Networking | Q4 FY2026 年化约 $44B | $55B-$70B | $75B-$95B | $105B-$125B |
| Rubin/Vera Rubin/LPX/STX/DSX 相关 | 尚未形成披露级收入 | $15B-$30B | $40B-$75B | $90B-$130B |
| H20/H200 中国 | 10-K 口径 H200 无收入；H20 受限 | $0-$5B | $10B-$20B | $25B-$40B |
| Gaming/ProViz/Auto/其他 | FY2026 合计约 $21.6B | $22B-$28B | $30B-$35B | $40B+ |

关键敏感性：

- 每 10% GB300 系统出货差异会同时影响 compute、networking、HBM/CoWoS 拉动和毛利。
- Networking attach rate 比 GPU 单价更可能带来超预期，因为机架级系统和 AI Ethernet/InfiniBand 升级具有结构性提升。
- Rubin 何时从样机/认证进入规模收入是 2026H2-2027 的最大上行或失望来源。
- 中国收入在模型中折现很高：即使美国许可放松，仍需中国进口许可、客户采购意愿、关税/检查和本土替代政策配合。

---

## 6. BOM、单位含量、价格传导、产能、采纳与认证

### 6.1 GB300 NVL72 官方规格与 BOM 读法

NVIDIA GB300 NVL72 官方页面（2026-05-15 抓取）显示：

| 项目 | GB300 NVL72 |
|---|---:|
| GPU / CPU | 72 Blackwell Ultra GPUs + 36 Grace CPUs |
| 系统形态 | 全液冷 rack-scale 架构 |
| NVLink bandwidth | 130 TB/s |
| Fast memory | 37 TB |
| GPU memory | 20 TB，最高 576 TB/s |
| CPU memory | 17 TB LPDDR5X，14 TB/s |
| CPU cores | 2,592 Arm Neoverse V2 cores |
| 网络 | 每 GPU 800 Gb/s ConnectX-8 SuperNIC，可接 Quantum-X800 InfiniBand 或 Spectrum-X Ethernet |
| 性能表述 | 较 Hopper AI factory output 最高 50x；DeepSeek-R1 benchmark 口径下 TPS/user 10x、TPS/MW 5x；视频生成较 Hopper 30x |

BOM 与投资含义：

- 每 rack 72 颗 GPU 意味着 NVIDIA content 不只是 GPU，还包括 NVLink switch、NIC/DPU、Grace CPU、系统板、电源/液冷相关设计与软件。
- 每 GPU 约 278GB HBM3E 等效容量（20TB / 72）对应项目内 HBM 报告中的 12Hi HBM3E 瓶颈，HBM 价格上涨可部分由系统 ASP 传导，但会影响毛利率弹性。
- 每 GPU 800Gb/s 网络连接使 ConnectX/Spectrum-X/InfiniBand 的内容量从可选升级变成 AI factory 标配。
- 液冷 rack-scale 交付使服务器 ODM、冷板/CDU、快速接头、机房水系统、供电和数据中心施工周期成为收入确认前置条件。

### 6.2 Vera Rubin NVL72 官方规格与 BOM 读法

NVIDIA Vera Rubin NVL72 官方页面（2026-05-15 抓取）显示：

| 项目 | Vera Rubin NVL72 |
|---|---:|
| GPU / CPU | 72 Rubin GPUs + 36 Vera CPUs |
| 关键芯片 | Rubin GPU、Vera CPU、ConnectX-9、BlueField-4、NVLink 6 switch |
| GPU memory | 20.7TB HBM4，1,580TB/s |
| NVLink | 260TB/s；每 GPU scale-up bandwidth 3.6TB/s |
| CPU | 3,168 custom NVIDIA Olympus cores |
| CPU memory | 54TB LPDDR5X |
| NVIDIA + HBM4 chips | 1,296 |
| 网络 | ConnectX-9 每 GPU 1.6Tb/s |
| 代际目标 | 官方称训练可用 Blackwell 1/4 GPU，推理每百万 token 成本为 Blackwell 1/10（projected） |

BOM 与投资含义：

- HBM4 从容量到带宽全面升级，供应链门槛高于 HBM3E。Rubin 放量将把瓶颈从 HBM3E 12Hi 逐步推到 HBM4 良率、TSV、base die、KGD test 与 CoWoS/interposer。
- ConnectX-9 1.6Tb/s / GPU 说明网络内容量继续翻倍，Networking 收入增速可能继续高于 Compute。
- BlueField-4 与 DPU/存储路径强化推理场景下 context memory/storage 的系统价值。
- 1,296 NVIDIA + HBM4 chips / rack 体现供应链复杂度：任何 HBM4、advanced packaging、substrate 或电力/液冷短板都会限制 Rubin 收入确认。

### 6.3 LPX / 长上下文推理机架

NVIDIA LPX 页面（2026-05-15 抓取）显示：

| 项目 | LPX rack |
|---|---:|
| LPU 数量 | 256 |
| SRAM | 128GB，即每 LPU 约 500MB |
| DDR5 | 12TB |
| SRAM bandwidth | 40PB/s |
| Scale-up bandwidth | 640TB/s |
| 官方性能目标 | trillion-parameter models 口径下 35x throughput/MW、10x revenue opportunity/watt（相对 Blackwell，projected） |

读法：如果长上下文 agentic AI 成为主要推理负载，LPX 类 SRAM 推理机架会提高 NVIDIA 在推理系统中的内容量。但当前缺少收入拆分、客户订单和大规模交付节奏，模型中只能作为 Rubin 上行情景的一部分。

### 6.4 每 MW / 每 rack / 每 GPU 内容量估算

以下为研究估算，用于理解订单弹性，不是公司披露数字：

| 单位 | GB300 NVL72 估算 | Rubin NVL72 估算 |
|---|---:|---:|
| 每 rack GPU | 72 | 72 |
| 每 rack CPU | 36 Grace | 36 Vera |
| 每 rack HBM | 20TB HBM3E 等效 | 20.7TB HBM4 |
| 每 rack NVLink | 130TB/s | 260TB/s |
| 每 GPU 网络 | 800Gb/s | 1.6Tb/s |
| 假设 rack IT 功耗 | 120-150kW | 150-200kW |
| 每 1MW 可容纳 rack | 约 6.5-8.3 | 约 5.0-6.7 |
| 每 1MW GPU | 约 470-600 | 约 360-480 |
| 每 1MW HBM 容量 | 约 130-165TB | 约 104-138TB |

价格传导判断：

- NVIDIA 对 GPU/HBM/CoWoS/系统稀缺性有强定价权，但不是无限定价权；客户最终约束是每 token 成本、每 MW 吞吐和现金回收期。
- HBM/CoWoS 成本上涨在 Blackwell/GB300 阶段大概率可以部分传导，因为客户瓶颈是可用算力而非单机价格；但 Rubin 初期若良率偏低，毛利率可能先承压。
- 在 AI 数据中心 capex 中，NVIDIA content 与服务器/网络/电力/冷却强绑定；项目内 AI DC 订单映射给出美国 2026 AI DC 建设现实口径 $400B-$490B，其中 GPU/server compute $144B-$211B、networking $36B-$59B、HBM/SRAM $80B-$132B。这与 NVIDIA FY2027 指引年化方向一致。

---

## 7. 一年后产能、采纳、认证三情景

### 7.1 产能情景

| 情景 | HBM/CoWoS | 系统/液冷 | 网络 | 收入影响 |
|---|---|---|---|---|
| 基准 | HBM3E 12Hi 和 CoWoS 继续紧，但可支撑 GB300 逐季放量；HBM4 以认证/早期量产为主 | ODM/液冷交付紧张但可改善 | ConnectX-8/Spectrum-X 供应随系统 attach 提升 | FY2027 上半年收入按 Q1 指引延续，H2 增速略降但仍高 |
| 乐观 | HBM3E 供给释放快，HBM4 良率顺利 | GB300 NVL72 交付和数据中心水电配套同步 | Spectrum-X 大规模替换传统 Ethernet | Networking 与系统收入超预期，毛利率维持 75%+ |
| 下行 | HBM/CoWoS 或 ABF 卡住，电力/液冷施工延迟 | 机柜交付与客户验收滞后 | 网络设备供给/部署滞后 | 收入从订单转为延迟确认，库存和承诺压力上升 |

### 7.2 客户采纳情景

| 情景 | Hyperscaler | Neo-cloud / sovereign / enterprise | AI labs | 结论 |
|---|---|---|---|---|
| 基准 | Microsoft/Amazon/Google/Meta/Oracle 等继续高 capex | CoreWeave 等继续扩建，但融资成本和电力制约更明显 | OpenAI/xAI/Anthropic/Meta 等持续训练与推理扩容 | NVDA 仍供不应求，收入高可见 |
| 乐观 | Capex 继续上修，GB300 成为 2026 标准配置 | 主权 AI 和企业私有 AI 加速 | reasoning/agentic/video 推理商业化提升 | Rubin 预付款/早期交付增强 2027 可见度 |
| 下行 | 单个大客户放缓或推迟机房验收 | Neo-cloud 资金链压力或租赁价格下行 | 推理单位经济性改善慢 | 订单不一定取消，但收入确认延后，估值先压缩 |

### 7.3 认证/政策情景

| 情景 | 美国出口政策 | 中国进口/客户政策 | 影响 |
|---|---|---|---|
| 基准 | H200 个案许可存在但范围小；H20/H200 均需许可证 | 中国安全/自主可控约束强，实际进口不确定 | 中国 DC compute 近似为零或低个位数十亿美元 |
| 乐观 | 美国扩大 H200/H20 许可证，第三方测试流程顺畅 | 中国允许部分进口，客户恢复采购 | 增量 $10B-$20B，更多是估值情绪和毛利率改善 |
| 极端上行 | 批量许可与中方接受同时发生 | 大客户集中补单 | 增量 $25B-$40B，但概率低且可持续性差 |
| 下行 | 美国/中国任一侧收紧 | 已许可订单也无法交付 | 维持零收入；公司需继续吸收中国专用库存/设计成本 |

---

## 8. 基于订单/供给的未来一年业务增长预测

### 8.1 真实 backlog 不披露，如何推断

NVIDIA 不披露完整 backlog/bookings，因此只能用以下硬指标推断未来 12 个月收入：

1. Q1 FY2027 指引 $78B：这是最强的 near-term demand 证据，且不含中国 DC compute。
2. FY2026 末供应相关承诺 $95.2B：说明公司已经锁定大量制造、供应和产能，且“substantially all paid through FY2027”。
3. 库存 $21.4B：支持 Blackwell/GB300/Rubin 供应链爬坡，但也需要客户验收和数据中心建设匹配。
4. 云服务协议承诺 $27.0B：反映 NVIDIA 自身 AI/云/软件服务基础设施需求，也可能支持生态内算力供给。
5. Data Center Q4 run-rate：Q4 DC $62.3B，年化 $249B；Q1 指引对应总收入年化 $312B。
6. 项目内 AI DC capex 映射：2026 美国 AI DC 建设现实口径 $400B-$490B、2027 $520B-$650B，GPU/server compute 和 networking 是最大半导体增量。

### 8.2 未来一年收入预测

| 项目 | 基准预测 | 关键依据 |
|---|---:|---|
| FY2027 Q1 | $78B 指引中值 | 公司已披露 |
| FY2027 Q2-Q4 单季区间 | $80B-$98B | GB300/Blackwell Ultra 爬坡，Networking attach 提升；假设中国为零 |
| 未来 12 个月总收入 | $330B-$360B | Q1 指引 + Q4 run-rate + supply commitments |
| Data Center 收入 | $300B-$325B | Compute $220B-$260B，Networking $55B-$70B，Rubin/other $15B-$30B |
| EPS 方向 | 约 $7.0-$8.0 | 粗略基于 74%-76% GM、opex 增长、税率 17%-19%、股份稳定；非精确模型 |

### 8.3 订单取消/延迟风险

- 电力和施工延迟：客户买 GPU 不等于数据中心能按时上电；电力接入、变压器、开关设备、液冷和施工许可都可能拖延收入确认。
- HBM/CoWoS 良率和排产：HBM3E 12Hi 与 HBM4 初期良率决定 GB300/Rubin 放量速度。
- 客户 capex 消化：Microsoft、Meta、Amazon、Alphabet、Oracle、CoreWeave 等 capex 仍在上修，但市场会开始追问每 token 收入、租赁价格和投资回报。
- 中国政策：H200 许可 headlines 容易被股价提前交易，但公司 10-K 和最新新闻都显示未形成收入。
- 自研 ASIC 替代：Google TPU、AWS Trainium、Meta MTIA、Microsoft Maia、Broadcom/Marvell custom ASIC 会分走部分推理和内部 workload，但不太可能在一年内替代最高性能训练/通用生态。

---

## 9. 竞争格局、替代方案、风险与替换成本

### 9.1 竞争对手与替代路径

| 类型 | 代表 | 对 NVDA 威胁 | 判断 |
|---|---|---:|---|
| 商用 GPU | AMD MI300/MI350/MI400，Intel Gaudi/Falcon Shores | 中 | AMD 会拿到部分性价比/供应多元化订单，但 CUDA/系统/网络生态差距仍大 |
| 云厂自研 ASIC | Google TPU，AWS Trainium/Inferentia，Microsoft Maia，Meta MTIA | 中-高 | 对内部推理 workload 有真实替代价值；对通用训练和生态外销售威胁较小 |
| Custom ASIC 供应链 | Broadcom、Marvell、Alchip、GUC、世芯等 | 中 | 受益于 hyperscaler 自研，但项目周期长、软件生态弱、灵活性不如 NVIDIA |
| 网络替代 | Broadcom Ethernet、Arista、Cisco、Marvell DSP/交换芯片 | 中 | Ethernet 会增长，但 NVIDIA 的 Spectrum-X + NIC + GPU 协同在 AI cluster 中仍有优势 |
| 中国本土 AI 芯片 | 华为昇腾、寒武纪等 | 区域高 | 中国市场因政策被迫替代，全球性能/生态短期仍难全面替代 |

### 9.2 替换成本

NVIDIA 替换成本不只在硬件：

- 软件栈：CUDA、cuDNN、TensorRT、NIM、Dynamo、profiling/debugging、生态模型优化形成多年沉没成本。
- 系统架构：GB200/GB300/Rubin 是 rack-scale 架构，替代方需要同时解决 GPU/CPU/NIC/DPU/switch/liquid cooling/firmware/cluster management。
- 开发者与模型生态：主流框架、模型、推理引擎优先适配 NVIDIA；替代方案需要客户承担迁移和性能调优成本。
- 供应链与交付：即使替代芯片可用，也需要 HBM、封装、ODM、网络、机房和运维体系匹配。

结论：未来一年，替代更多表现为“客户将部分内部推理 workload 分流给自研 ASIC”，而不是“全面替代 NVIDIA”。真正影响 NVDA 估值的是替代是否压低增量订单增长率和系统 ASP，而非短期份额归零。

### 9.3 核心风险

| 风险 | 触发信号 | 影响 |
|---|---|---|
| AI capex 回报率被质疑 | CSP 下调 capex、GPU 租赁价格持续下跌、推理收入不及预期 | 估值倍数先压缩 |
| Blackwell/GB300 供应或良率问题 | 毛利率低于指引、库存升高、交付延迟 | 收入确认延后，市场重估供应链可靠性 |
| Rubin 延迟 | 2026H2 无明确客户/量产进展 | 2027 增长可见度下降 |
| HBM/CoWoS/电力瓶颈 | HBM4 良率慢、CoWoS 排产紧、数据中心上电延迟 | 订单变收入的速度下降 |
| 中国政策反复 | 美国扩大限制或中国拒绝进口 | 中国收入长期归零，H20/H200 库存风险 |
| 客户集中 | 单一 hyperscaler 或 neo-cloud 放缓 | 短期收入/股价波动大 |
| 自研 ASIC | TPU/Trainium/MTIA/Maia 在推理上大规模替代 | 长期推理 ASP 和份额承压 |

---

## 10. 跟踪清单与主要资料来源

### 10.1 接下来 90 天最该盯

1. 2026-05-20 Q1 FY2027 财报：是否超过 $78B 指引；Q2 指引是否继续上修；是否仍不含中国 DC compute。
2. GB300/Blackwell Ultra 出货节奏：客户案例、ODM 交付、液冷部署、毛利率指引。
3. Networking 收入：Q1/Q2 DC Networking 是否继续高于 Compute 增速；Spectrum-X attach rate 是否提升。
4. H200/H20 中国实际交付：不仅看美国批准，还要看中国进口、客户验收、NVIDIA revenue recognition。
5. Rubin/Vera Rubin 里程碑：HBM4 供应、NVLink 6、ConnectX-9、BlueField-4、客户公开部署和 2026H2 收入可见度。
6. CSP capex 更新：Microsoft、Meta、Amazon、Alphabet、Oracle、CoreWeave、OpenAI/Stargate 等是否继续上修或延迟。

### 10.2 外部公开来源

- NVIDIA FY2026 Form 10-K，2026-02-25，SEC accession 0001045810-26-000021，primary doc nvda-20260125.htm。
- NVIDIA Q4 FY2026 press release / CFO commentary，2026-02-25，SEC accession 0001045810-26-000019，q4fy26pr.htm、q4fy26cfocommentary.htm。
- NVIDIA Q3 FY2026 CFO commentary，2025-11-19，SEC accession 0001045810-25-000228，q3fy26cfocommentary.htm。
- NVIDIA Q2 FY2026 CFO commentary，2025-08-27，SEC accession 0001045810-25-000207，q2fy26cfocommentary.htm。
- NVIDIA Q1 FY2026 CFO commentary，2025-05-28，SEC accession 0001045810-25-000115，q1fy26cfocommentary.htm。
- NVIDIA Q4 FY2025 CFO commentary，2025-02-26，SEC accession 0001045810-25-000021，q4fy25cfocommentary.htm。
- Federal Register / BIS，2026-01-15，Revision to License Review Policy for Advanced Computing Commodities，document 2026-00789。
- NVIDIA GB300 NVL72 official product page，抓取日期 2026-05-15：https://www.nvidia.com/en-us/data-center/gb300-nvl72/。
- NVIDIA GB200 NVL72 official product page，抓取日期 2026-05-15：https://www.nvidia.com/en-us/data-center/gb200-nvl72/。
- NVIDIA Vera Rubin NVL72 official product page，抓取日期 2026-05-15：https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/。
- NVIDIA LPX official product page，抓取日期 2026-05-15：https://www.nvidia.com/en-us/data-center/lpx/。
- StockAnalysis NVDA quote/statistics，抓取日期 2026-05-15：收盘价、市值、P/E、Forward P/E、P/S、Forward P/S、P/FCF、利润率、现金债务等。
- Yahoo chart API，抓取日期 2026-05-15：交叉核验收盘价、成交量和日内高低。
- Google News RSS，抓取日期 2026-05-15/16：Reuters 2026-05-14 “US clears H200 chip sales to 10 China firms...”、Digitimes 2026-05-15 “Nvidia H200 sales to China stall despite US approval”、Global Times 2026-04-23 “no Nvidia H200 chips sold to China yet”等新闻标题与日期。注：部分正文受限，报告仅使用可核验标题/日期与公司 10-K 披露交叉确认，不把新闻标题当作已确认收入。

### 10.3 项目内资料

- 日度资料/顶级conference纪要/nvidia_gtc_2026_research.md
- 行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI_ASIC_2026.md
- 行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026.md
- 行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-05-08.md
- 行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md
- 旧版备份：公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/backup_20260515_232955/NVDA_NVIDIA_全面尽调_2026-05-10.md，仅作旧版参考，不作为未核验事实来源。

### 10.4 当前缺口

- H200 中国名单和实际发货量：新闻流显示美国侧可能批准部分企业，但公司尚未披露客户名单、数量、ASP、交付和收入确认；中国进口许可也未清晰。
- GB300/Rubin 真实 ASP 与 rack 功耗：官方披露了规格和性能目标，但未披露标准价格、客户折扣和实际 rack 功耗；本报告的每 MW 内容量为估算。
- 软件收入拆分：CUDA/NIM/Dynamo/AI Enterprise 的经济价值很高，但公司未完整单列 AI 软件收入，难以独立估值。
- 客户级订单与 backlog：NVIDIA 不披露标准 backlog/bookings；只能用指引、供应承诺、库存、客户 capex 和供应链信息推断。
- 2026-05-20 财报前时点差：本报告在 Q1 FY2027 财报前完成，财报发布后应立即刷新 Q1 实际、Q2 指引、H200/H20 口径和 GB300/Rubin 进展。


