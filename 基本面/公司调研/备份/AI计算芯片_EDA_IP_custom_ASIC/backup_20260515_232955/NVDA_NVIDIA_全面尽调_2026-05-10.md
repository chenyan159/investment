# 公司：NVDA NVIDIA Corporation

> 写作日期：2026-05-10；市场数据以最近可得公开行情和财务披露为准。  
> 最新正式财报：NVIDIA FY2026 Q4 与 FY2026 年报，季度截止日为 2026-01-25，披露日为 2026-02-25。下一次 FY2027 Q1 财报尚未披露。  
> 口径说明：NVIDIA 不披露公司级 backlog/bookings；本文对订单、交期、取消率、产品级收入和 BOM 做了“官方披露 + 客户项目 + 供应链约束 + 项目内非公司调研行业底稿”的推断，估算项均标注为“估算/推断”。未参考本目录下其他公司调研文件。

## 1. 公司整体业务、产业链位置与财务快照

NVIDIA 已经不再是投资人心中的“游戏 GPU 公司”，而是 AI 数据中心时代的核心基础设施公司：它控制 AI 加速器 GPU、Grace/Vera CPU、NVLink/NVSwitch scale-up 互连、InfiniBand/Spectrum-X Ethernet scale-out 网络、BlueField DPU、CUDA/AI Enterprise/Dynamo/Omniverse/DSX 软件栈，并通过 DGX、HGX、NVL72、Rubin POD 等形态把价值从单芯片推到 rack/POD/GW 级 AI factory。

产业链位置可以概括为：上游绑定 TSMC 先进制程与 CoWoS、SK hynix/Samsung/Micron HBM、ABF 基板、ODM/OEM 整柜制造；中游由 NVIDIA 设计 GPU/CPU/DPU/NIC/交换芯片和系统参考架构；下游面对 Microsoft、Amazon、Google、Meta、Oracle、CoreWeave、xAI、OpenAI、Anthropic、主权 AI、企业与机器人/汽车客户。NVIDIA 的稀缺性不只在 GPU，而在“CUDA + NVLink + 网络 + 系统认证 + 供应链优先级”形成的整体替换成本。

### 近 3 年重大变化

| 时间 | 事件 | 投资含义 |
|---|---|---|
| FY2024-FY2026 | Data Center 收入从 FY2024 的 $47.5B 增至 FY2025 的 $115.2B、FY2026 的 $193.7B | 公司收入主轴彻底转为 AI 数据中心；FY2026 Data Center 占总收入约 89.7% |
| 2024-2025 | Blackwell / Grace Blackwell / GB200 NVL72 进入量产 | 交付单位从 GPU/HGX 板卡升级到整柜液冷 AI supercomputer |
| 2025-04 | H20 对中国出口需许可证；FY2026 Q1 产生 $4.5B H20 库存和采购义务 charge，另有 $2.5B Q1 收入无法出货 | 中国风险从“需求问题”变成“政策许可问题”；Q1 FY2027 指引不包含中国 Data Center compute 收入 |
| 2025-08 | 董事会追加 $60B 回购授权 | 强现金流下继续资本回报，FY2026 回购与分红合计约 $41.1B |
| 2025-2026 | OpenAI 10GW、Anthropic 1GW、Meta 多代合作、CoreWeave 5GW by 2030、AWS/Intel/Arm/Fujitsu/Marvell NVLink Fusion 生态 | NVIDIA 正在把自研 ASIC、云客户和网络生态拉回自己的 AI factory 控制面 |
| 2026 | Rubin/Vera Rubin、BlueField-4 STX、Groq/LPX、Spectrum-6/CPO、DSX 等发布或进入客户导入 | 下一阶段重点从“训练 GPU”扩展到 agentic inference、context memory、低延迟 decode、AI factory 运营 |

### 最新估值与经营指标

| 指标 | 最新值 | 日期/口径 | 备注 |
|---|---:|---|---|
| 股价 | 约 $215/股 | 2026-05-08 附近最新可得行情 | 周末写作，最新交易日为 2026-05-08 |
| 市值 | 约 $5.2T | 按最新股价和约 24.4-24.5B 稀释股本估算 | 不同行情源会因股价日期有差异 |
| Trailing P/E | 约 44x-53x | 用 FY2026 GAAP EPS $4.90 得约 44x；部分行情源 TTM EPS 口径显示约 50x+ | 取决于 EPS/稀释股本更新时间 |
| Forward P/E | 约 24x-26x | Yahoo/TECHi 等 2026-05 初数据给 forward P/E 约 24x，下一年 EPS 估计约 $8.0-$8.4 | 高增长下 forward multiple 明显低于 trailing |
| P/S | 约 24x | 市值约 $5.2T / FY2026 收入 $215.9B | 若用 2026-05-05 较低市值，约 22x |
| FY2026 收入 | $215.938B，YoY +65% | FY2026 年报 | Data Center $193.737B，YoY +68% |
| Q4 FY2026 收入 | $68.127B，QoQ +20%，YoY +73% | FY2026 Q4 | Data Center $62.3B |
| FY2026 GAAP 毛利率 | 71.1% | FY2026 | 受 Q1 H20 $4.5B charge 和 Blackwell rack-scale 成本影响 |
| Q4 FY2026 GAAP 毛利率 | 75.0% | FY2026 Q4 | Q1 FY2027 指引 GAAP/Non-GAAP GM 约 74.9%/75.0% |
| FY2026 GAAP 净利率 | 55.6% | $120.067B / $215.938B | 接近平台型软件公司的利润率 |
| Q4 FY2026 GAAP 净利率 | 63.1% | $42.960B / $68.127B | 受高毛利与投资收益影响，单季偏高 |

### 资产负债表健康度

NVIDIA 财务状态极强。FY2026 年末现金、现金等价物和有价证券 $62.6B，总债务 $8.5B，净现金约 $54B；总资产 $206.8B，总负债 $49.5B，股东权益 $157.3B，负债/权益约 0.31x。FY2026 经营现金流 $102.7B，自由现金流 $96.6B，资本开支 $6.1B。当前主要财务风险不是偿债能力，而是：客户集中、供应链预付款/采购承诺、对 OpenAI/Anthropic/CoreWeave/Groq/Intel/Marvell 等生态投资或授权带来的资本配置风险，以及 AI CapEx 周期一旦放缓后的应收账款和库存波动。

## 2. 最近五个财报季度复盘

| 季度 | 总收入 / GAAP GM / GAAP净利 | Data Center：总额 / compute / networking / 占总收入 | 其他业务收入 | 订单、交期、取消率推断 | 关键解读 |
|---|---:|---:|---:|---|---|
| Q4 FY2026，截止 2026-01-25 | $68.127B；GM 75.0%；净利 $42.960B | $62.3B，QoQ +22%，YoY +75%；compute 约 $51.3B；networking 约 $11.0B；占比 91.5% | Gaming $3.7B；ProViz $1.3B；Auto $0.604B；OEM 约 $0.16B | 不披露 backlog。管理层称 inventory 和 supply commitments 可支持未来需求，shipments 延伸到 CY2027；先进架构供给仍紧。取消率：无公开大额取消，估算低；风险在 neocloud 融资与客户 ROI。 | Grace Blackwell 系统约占 Data Center 收入 2/3；networking 同比 >3.5x，NVLink、Spectrum-X、InfiniBand 同涨。 |
| Q3 FY2026，截止 2025-10-26 | $57.006B；GM 73.4%；净利 $31.910B | $51.2B，QoQ +25%，YoY +66%；compute $43.0B；networking $8.2B；占比 89.8% | Gaming 约 $4.3B；ProViz 约 $0.76B；Auto 约 $0.59B；OEM 约 $0.14B | 管理层称 Blackwell sales “off the charts”、cloud GPUs sold out；OpenAI 10GW、Anthropic initial 1GW、Meta/Microsoft/Oracle/xAI 大规模项目形成订单锚。交期：大客户 2026-2027 产能锁定；取消率低。 | GPU 已从单卡供给紧张变成 rack-scale+网络整体供给紧张；Spectrum-X Ethernet attach 接近 InfiniBand。 |
| Q2 FY2026，截止 2025-07-27 | $46.743B；GM 72.4%；净利 $26.422B | $41.1B，QoQ +5%，YoY +56%；compute 约 $33.8B；networking $7.3B；占比 87.9% | Gaming 约 $4.3B；ProViz 约 $0.60B；Auto 约 $0.59B；OEM 约 $0.15B | Blackwell Ultra full-speed ramp；无 H20 对中国客户销售，$650M 非中国 H20 销售释放 $180M 库存准备。H100/H200 云端仍售罄；推断 B300/GB300 交期多为 2-4 个季度。 | H20 冲击开始被 Blackwell 吸收；networking QoQ +46%，说明 NVL72/GB300 拉动网络 attach。 |
| Q1 FY2026，截止 2025-04-27 | $44.062B；GM 60.5%；净利 $18.775B | $39.1B，QoQ +10%，YoY +73%；compute 约 $34.1B；networking $5.0B；占比 88.8% | Gaming 约 $3.8B；ProViz $0.509B；Auto 约 $0.57B；OEM $0.111B | H20 Q1 已销售 $4.6B，但出口新规导致 $4.5B charge，另有 $2.5B 无法发货；Blackwell NVL72 已 full-scale production。取消率主要来自政策性不可交付，不是需求取消。 | 报表毛利被 H20 一次性冲击压低，剔除后 non-GAAP GM 约 71.3%；核心 AI 需求仍强。 |
| Q4 FY2025，截止 2025-01-26 | $39.331B；GM 73.0%；净利 $22.091B | Data Center 约 $35.6B，QoQ 约 +16%，YoY 约 +93%；compute 约 $32.5B；networking 约 $3.0B；占比约 90.5% | Gaming 约 $2.5B；ProViz $0.511B；Auto 约 $0.57B；OEM 约 $0.13B | Blackwell ramp 早期，需求超过供应；Hopper 仍大量出货。交期推断：Hopper/B200 多季度排产。 | 这是 Blackwell 切换前的高基数季度，之后 FY2026 每季收入继续上台阶，说明需求没有在 Blackwell 切换中断档。 |

## 3. 最新指引、业务占比与重点产品

NVIDIA 在 Q4 FY2026 财报中给出 Q1 FY2027 指引：收入 $78.0B ±2%，GAAP/Non-GAAP 毛利率 74.9%/75.0% ±50bps，Non-GAAP operating expense 约 $7.5B，且“不假设中国 Data Center compute 收入”。这是一条很强的信号：即使中国高端 compute 基本不计入，Blackwell/Blackwell Ultra 与 networking 仍足以驱动单季收入从 $68.1B 跳到约 $78B。

### FY2026 与 Q4 FY2026 收入结构

| 业务 | FY2026 收入 | FY2026 占比 | YoY | Q4 FY2026 收入 | Q4 占比 | Q4 同比/环比 |
|---|---:|---:|---:|---:|---:|---:|
| Data Center | $193.737B | 89.7% | +68% | $62.3B | 91.5% | +75% / +22% |
| Data Center compute | $162.361B | 75.2% | 约 +59% | 约 $51.3B | 75.4% | 约 +58% YoY |
| Data Center networking | $31.376B | 14.5% | +142% | 约 $11.0B | 16.1% | 约 +263% YoY / +34% QoQ |
| Gaming | $16.042B | 7.4% | +41% | $3.7B | 5.5% | +47% YoY，QoQ 季节性下降 |
| Professional Visualization | $3.191B | 1.5% | +70% | $1.3B | 1.9% | +159% YoY / +74% QoQ |
| Automotive | $2.349B | 1.1% | +39% | $0.604B | 0.9% | +6% YoY / +2% QoQ |
| OEM and Other | $0.619B | 0.3% | +59% | 约 $0.16B | 0.2% | 小体量 |

### 跳过或弱化分析的业务

以下业务不是没有价值，而是对未来 12 个月 NVDA 投资主线贡献较小：GeForce 消费游戏 GPU、Nintendo Switch/游戏主机相关、传统 OEM 显示芯片、非 AI 图形工作站的常规换机、短期车载 L2/L2+ 设计 win。Automotive/Robotics 长期空间大，但 FY2026 Automotive 仅 $2.349B，短期不决定估值弹性。

### 重点产品和业务清单

| 重点业务/产品 | 对应产品型号/系统 | 当前收入贡献估算 | 未来 12 个月重要性 |
|---|---|---:|---|
| Blackwell / Blackwell Ultra AI compute | B200、GB200、B300、GB300、GB300 NVL72、HGX B200/B300、DGX/HGX/Cloud instances | FY2026 Data Center compute $162.4B；Q4 compute 约 $51.3B，其中 Grace Blackwell 系统约占 Data Center 收入 2/3 | 仍是 FY2027 最大收入池，GB300/B300 是 2026 主力 |
| Data Center networking | NVLink/NVSwitch/NVL72、Quantum-X800 InfiniBand、Spectrum-X Ethernet、Spectrum-XGS、ConnectX-8/9、BlueField-3/4 | FY2026 $31.4B；Q4 约 $11.0B | 增速和利润弹性最突出之一，AI 集群越大，网络 attach 越高 |
| Vera Rubin / Rubin platform | Vera CPU、Rubin GPU、NVLink 6、ConnectX-9、BlueField-4、Spectrum-6、Vera Rubin NVL72 | 2026-05 当前收入仍小，已送样/导入；H2 2026 生产出货 | 2026H2-2027 最大新平台变量；决定 FY2027 下半年和 FY2028 斜率 |
| LPX/Groq 3 LPU + Dynamo | Groq 3 LPU、LPX rack、Dynamo inference OS | 当前近零或小体量，属于 FY2027 新增 | 高 ARPU reasoning / long-context / low-latency decode 的潜力小业务，不能漏 |
| BlueField-4 STX/CMX context memory | BlueField-4 DPU、STX storage rack、CMX context memory platform | 当前尚小，DPU/NIC 价值部分已在 networking 中 | 推理和 agent memory 使 storage/context tier 成为新 attach |
| AI software / enterprise stack | CUDA、NIM、NeMo、Dynamo、AI Enterprise、DGX Cloud、Omniverse/DSX、Mission Control | 公司不单列；估算 FY2026 直接收入低个位数十亿美元，但嵌入硬件高毛利 | 直接收入小于硬件，但决定锁定和硬件利用率 |
| ProViz / RTX PRO / edge physical AI | RTX PRO 6000/5000 Blackwell、DGX Spark、Jetson Thor、Isaac、Cosmos、Omniverse | ProViz FY2026 $3.2B；physical AI FY2026 管理层称已 >$6B | 小体量高增速，可成为机器人/企业 AI 工作站入口 |

## 4. 当前关键业务：收入贡献、增速、重要性、供需和定价权

评分：5 = 极强/极紧/极高。

| 业务/产品 | 当前收入贡献 | 收入增速 | AI 基建重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价能力 | 判断 |
|---|---:|---:|---:|---:|---:|---:|---|
| Blackwell/GB300 compute rack | FY2026 compute $162.4B；Q4 约 $51.3B | FY2026 compute 约 +59%；Q4 仍 QoQ 双位数 | 5 | 5 | 5 | 5 | GB300/B300 是 2026 主力，客户为了 token/GW 和 time-to-revenue 接受高价 |
| NVLink/Spectrum-X/InfiniBand networking | FY2026 $31.4B；Q4 $11.0B | FY2026 +142%；Q4 YoY 约 +263% | 5 | 5 | 5 | 4.5 | NVLink 是 NVIDIA 独有 scale-up；Spectrum-X 正在侵入 Ethernet scale-out |
| Vera Rubin / Rubin NVL72 | 当前收入小；H2 2026 出货 | 低基数，2027 高增 | 5 | 4.5 | 5 | 5 | 客户会提前锁产能，HBM4/CoWoS/液冷决定可交付量 |
| LPX/Groq LPU + Dynamo | 当前近零到小体量 | 2027 可能从零到十亿美元级 | 4 | 4 | 4 | 3.5 | 适合 premium reasoning，不是普及推理；但若验证成功，可提高 NVIDIA 对异构推理的控制 |
| STX/CMX context memory | 当前近零到小体量 | 2027 高增 | 4 | 4 | 4 | 4 | Agent 的 KV cache/context memory 可能变成新瓶颈，BlueField 是入口 |
| CUDA/AI Enterprise/DGX Cloud/DSX 软件 | 直接收入估算小个位数十亿美元；间接贡献巨大 | 高于传统软件但基数小 | 5 | 5 | 3 | 5 | 软件锁定使 GPU 替换成本极高，是毛利率护城河 |
| RTX PRO/Physical AI/Jetson/Automotive | ProViz $3.2B，Auto $2.35B，physical AI >$6B | ProViz +70%，Auto +39% | 3 | 3 | 3 | 4 | 长期可选项，短期不是核心估值驱动 |

## 5. 未来一年三情景预测

未来一年指 2026-05 至 2027-05 的滚动 12 个月。下表产品口径存在交叉，不能相加为公司总收入。

| 业务/产品 | 基准情景：收入/增速/判断 | 乐观情景：收入/增速/判断 | 极度乐观情景：收入/增速/判断 |
|---|---|---|---|
| 公司总收入 | $330-360B；约 +50-65%；Q1 FY27 $78B 后逐季增长但供应有摩擦 | $380-430B；约 +75-100%；GB300 稳定、Rubin H2 提前贡献 | $450-520B；约 +110-140%；客户提前锁 2027 需求，推理 token 爆发 |
| Data Center 总收入 | $300-330B；DC 占比约 91-92%；GM 74-76% | $350-400B；DC 占比 92-93%；GM 75-77% | $420-490B；DC 占比 93%+；GM 77% 附近或更高 |
| Blackwell/GB300 compute | $210-250B；仍是主力，供应链紧但可交付 | $260-320B；GB300 交付超预期，H20/H200 小额恢复是额外期权 | $330-390B；GB300/B300 与剩余 GB200 订单全部吃满产能 |
| Networking | $55-70B；约 +75-120%；NVLink+Spectrum-X 扩张 | $75-95B；1.6T/CPO/ConnectX-9 提前拉动 | $105-130B；网络从 attach 变成 AI factory 第二收入柱 |
| Rubin/Vera Rubin | $30-60B；2026H2 小批量，2027H1 加速 | $60-110B；H2 2026 贡献明显，客户快速切换 | $110-180B；HBM4 和液冷顺利，Rubin ramp 接近 Blackwell 初期速度 |
| LPX/Groq + Dynamo | $3-10B；premium reasoning early adopter | $10-25B；前沿模型与云推理 tier 接受 LPU 分工 | $25-50B；LPX 成为 Rubin POD 标配高端推理层 |
| STX/CMX context memory | $2-8B；从 DPU/存储合作切入 | $8-20B；agent memory/KV cache 成为显性采购项 | $20-45B；推理存储 rack 与 GPU rack 同步采购 |
| 软件/DSX/DGX Cloud/AI Enterprise | $5-10B 直接收入；间接提高硬件利用率 | $10-18B；Dynamo/DSX/AI Enterprise attach 上升 | $18-30B；AI factory OS 化，软件成为单独估值线索 |
| ProViz/Physical AI/Auto | $8-12B；ProViz/Jetson/Auto 稳定高增 | $12-18B；机器人数据工厂和 RTX PRO 放量 | $18-30B；physical AI 早期项目批量复制 |

## 6. BOM、每 MW / rack / GPU / optical port 内容量与价格传导

### 6.1 GB300 NVL72 / Blackwell Ultra 内容量

| 维度 | 内容量与价格链 | NVIDIA 捕获点 | 供应瓶颈 |
|---|---|---|---|
| 每 rack | GB300 NVL72：72 颗 Blackwell Ultra GPU、36 颗 Grace CPU、NVLink/NVSwitch fabric、全液冷 rack-scale 架构；项目底稿口径约 132-142kW/rack，GPU HBM 约 20TB 级，fast memory 约 37TB 级 | GPU、Grace CPU、NVSwitch/NVLink、NIC/DPU、部分系统软件和参考设计；估算 NVIDIA 每 rack 价值约 $3.5M-$5.0M，视配置和网络 attach | HBM3E、CoWoS-L、ABF 基板、NVSwitch、液冷、整柜 burn-in、上电 |
| 每 MW | 约 7-8 个 130-142kW rack；约 504-576 颗 GPU；按管理层“每 1GW 数据中心 NVIDIA 约 $35B”口径，约 $35M/MW NVIDIA 硬件价值 | compute 约 $27M-$30M/MW，networking/NIC/NVLink/软件约 $5M-$8M/MW（估算） | 电力、机房上电、冷却水侧、网络端口、光模块 |
| 每 GPU | 1 颗 Blackwell Ultra GPU + 最高 288GB HBM3E + CoWoS/interposer + ABF + VRM/去耦 + 冷板 + NVLink 连接 | 高 ASP GPU 与 HBM 打包售价；客户买的是 tokens/GW，不只是芯片 | HBM stack、KGD test、CoWoS、封装良率 |
| 每 optical port | GB300 scale-out 常见 800G 端口；价格链为 ConnectX/Spectrum ASIC + 800G/1.6T 光模块 + AEC/DAC/光纤 + switch port | NVIDIA 更主要捕获 NIC、DPU、Spectrum/Quantum switch、网络软件；光模块多由 Coherent/Lumentum/中际旭创/新易盛/Fabrinet 等捕获 | 800G/1.6T 模块、DSP/EML/SiPh、客户认证 |

### 6.2 Rubin / Vera Rubin 内容量

| 维度 | 内容量与价格链 | NVIDIA 捕获点 | 当前认证/采纳 |
|---|---|---|---|
| 每 rack | Vera Rubin NVL72：72 Rubin GPU + 36 Vera CPU + NVLink 6 + ConnectX-9 + BlueField-4 + Spectrum-6；官方/项目底稿显示每 GPU NVLink 6 约 3.6TB/s，rack 级 scale-up 约 260TB/s，HBM4 带宽约 1.6PB/s 级 | GPU、Vera CPU、NVLink 6、CX9、BF4、Spectrum-6、CPO/网络软件 | 2026-05 已送样/导入；合作伙伴 H2 2026 可用；HBM4、CX9、BF4、Spectrum-6 认证是主线 |
| 每 MW | 若单柜 150-200kW，约 5-7 rack/MW，360-504 Rubin GPU/MW；ASP/rack 估算 $4.5M-$7M | 更高系统 ASP 和软件 attach；若 LPX/STX/SPX 同时采购，NVIDIA 每 MW 收入密度可高于 GB300 | 电力密度、液冷、HBM4、CPO/1.6T、客户机房 readiness |
| 每 GPU | Rubin GPU + HBM4 + NVLink 6 + 更高带宽 CPU coherent coupling | HBM4 容量/带宽和 NVLink 6 是溢价核心 | 三大 HBM 厂验证、TSMC/CoWoS、液冷可靠性 |
| 每 optical port | ConnectX-9 1.6T SuperNIC、Spectrum-6/CPO、SPX Ethernet rack | NVIDIA 可能从 NIC/switch/CPO optical engine 捕获更多端口价值 | 2026 试点，2027 批量 |

### 6.3 Networking / NVLink / Spectrum-X 内容量

| 维度 | 内容量 | 价格传导 |
|---|---|---|
| 每 rack | NVL72 内部 NVSwitch/NVLink scale-up；rack 外 800G/1.6T InfiniBand 或 Ethernet；ConnectX/BlueField NIC/DPU；Spectrum-X/Quantum switch | GPU 集群规模扩大时，网络端口数、radix、冗余、telemetry、拥塞控制同步增加；Q4 FY2026 networking 约 $11B，说明 attach 率显著提高 |
| 每 MW | 500 颗 GPU 级别约对应数百个 800G/1.6T endpoint；networking 估算 $5M-$8M/MW NVIDIA 内容量，上行场景更高 | 网络成本不是简单线性：集群越大，spine/super-spine、OCS/CPO/scale-across 占比越高 |
| 每 optical port | 800G 可插拔模块约 $600-$1,200 量级，1.6T 早期约 $1,500-$3,000+；NVIDIA 捕获 switch/NIC/DPU，光模块供应商捕获 transceiver | NVIDIA 自研 Spectrum-X/CPO 会把一部分光电价值从第三方模块转向 switch/CPO 系统 |

### 6.4 产能能力、采纳程度和认证阶段

| 业务/产品 | 当前产能能力（美元计，估算） | 当前采纳程度 | 当前认证阶段 | 未来一年基准 | 乐观 | 极度乐观 |
|---|---:|---|---|---:|---:|---:|
| GB300/B300/Blackwell | Q4 FY2026 DC compute run-rate 约 $205B/年；FY2026 compute $162.4B | 所有主要 CSP、AI labs、neocloud、主权 AI | GB200/GB300 已进入大规模客户生产；OEM/ODM 整柜认证成熟 | $210-250B | $260-320B | $330-390B |
| Networking | Q4 FY2026 run-rate 约 $44B/年；FY2026 $31.4B | NVLink/NVL72 高端客户标配；Spectrum-X 被 Meta/Microsoft/Oracle/xAI 等采用 | Spectrum-X、InfiniBand、ConnectX/BlueField 客户量产；Spectrum-XGS/MRC 进入扩展 | $55-70B | $75-95B | $105-130B |
| Rubin/Vera Rubin | 当前 revenue 小，产能处于客户样品/导入 | AWS/GCP/Azure/OCI 计划首批，Anthropic/OpenAI/Meta 等下一代项目潜在 | HBM4/CX9/BF4/Spectrum-6/液冷整柜认证中，H2 生产出货 | $30-60B | $60-110B | $110-180B |
| LPX/Groq + Dynamo | 当前小体量，H2 2026 可用 | 前沿 AI labs 和高端 inference providers 有潜在需求 | LPX rack、Dynamo 调度、GPU/LPU 分工仍需真实 workload 验证 | $3-10B | $10-25B | $25-50B |
| STX/CMX | 当前小体量 | CoreWeave、OCI、Mistral、Vast/DDN/NetApp/WEKA 等生态线索 | H2 2026 partner availability，存储 OEM 认证中 | $2-8B | $8-20B | $20-45B |
| Software/DSX | 直接收入未单列，间接覆盖几乎所有 DC 客户 | CUDA、NIM、Dynamo、Omniverse/DSX、Mission Control | DSX 与 Eaton/Schneider/Siemens/Vertiv/Trane 等合作；Dynamo 被主要云验证 | $5-10B | $10-18B | $18-30B |

## 7. 未来一年基于订单和供给的增速推断

NVIDIA 不披露 backlog。可观察的订单/需求锚如下：OpenAI 至少 10GW NVIDIA systems；Anthropic initial 1GW Grace Blackwell/Vera Rubin；CoreWeave 与 NVIDIA 合作到 2030 年超 5GW AI factories；Meta 多代、多百万 GPU 合作；Q4 call 称 top 5 cloud/hyperscaler 2026 CapEx 预期接近 $700B，并且这些客户合计略高于 Data Center 收入 50%；公司称有 inventory 与 supply commitments 支持未来需求，shipments 延伸到 CY2027。

### 订单覆盖推断

| 项目 | 可观察锚 | 收入映射 |
|---|---|---|
| 现有运行率 | Q4 FY2026 总收入 $68.1B，Data Center $62.3B；Q1 FY2027 指引 $78B | 进入 FY2027 时公司季度收入 run-rate 已经接近 $300B/年 |
| 大客户 CapEx | top 5 cloud/hyperscaler 2026 CapEx 接近 $700B；项目底稿九大 CSP 2026 CapEx 约 $830B | 只要服务器/芯片占 AI CapEx 50%+，NVIDIA 可服务 TAM 足以支撑 FY2027 高增长 |
| GW 订单 | OpenAI 10GW、Anthropic 1GW、CoreWeave 5GW by 2030 | 管理层 Q2 call 曾用约 $35B/GW 的 NVIDIA 内容量作为量级参考；订单兑现取决于 2026-2029 上电节奏 |
| 供应承诺 | HBM、CoWoS、液冷、整柜测试、网络均被提前锁定 | backlog 不披露，但 supply commitments 延伸 CY2027 是强能见度信号 |
| 取消率 | 无公开大额取消 | 当前推断低；主要风险是融资、token ROI、ASIC 自研和出口许可 |

### 未来一年业务增速：三口径

| 口径 | 公司收入 | Data Center | 主要假设 |
|---|---:|---:|---|
| 基准 | $330-360B，YoY +50-65% | $300-330B，YoY +55-70% | Q1 FY27 $78B；之后逐季中高个位数增长；GB300 稳，Rubin H2 小批；GM 约 75% |
| 乐观 | $380-430B，YoY +75-100% | $350-400B，YoY +80-105% | GB300/B300 交付快于预期；networking attach 上升；Rubin H2 明显贡献；中国 H200 小额恢复 |
| 极度乐观 | $450-520B，YoY +110-140% | $420-490B，YoY +115-150% | 客户把 2027 需求前置，HBM/CoWoS/液冷同步扩，Rubin/LPX/STX 形成新收入层 |

## 8. 竞争格局、主流性、替代风险与客户替换成本

### 竞争对手分层

| 领域 | 主要竞争对手 | 对 NVIDIA 的威胁 | NVIDIA 护城河 |
|---|---|---|---|
| Merchant GPU | AMD MI350/MI400/MI500，Intel Gaudi/Jaguar，Huawei Ascend，Cambricon/Biren/Iluvatar | AMD 是美国合规第二供应源；Huawei/Cambricon 承接中国被管制需求 | CUDA、NVLink、HBM/CoWoS优先级、系统级交付、客户已调优模型 |
| Hyperscaler ASIC | Google TPU、AWS Trainium、Meta MTIA、Microsoft Maia、OpenAI/Broadcom XPU、Broadcom/Marvell custom ASIC | 内部 workload 可用 ASIC 降 TCO，压低 NVIDIA 议价 | NVIDIA 正通过 NVLink Fusion、Spectrum-X、DPU、Dynamo 把 ASIC 拉进自己网络/软件生态 |
| AI networking | Broadcom、Arista、Cisco、Marvell、AMD Pensando、UEC/UALink | Ethernet 生态会压缩 InfiniBand 溢价，开放 scale-up 可能削弱 NVLink | NVLink 是已验证 scale-up；Spectrum-X 证明 NVIDIA 也能吃 Ethernet |
| Software/runtime | ROCm、XLA/JAX、Neuron、Triton、vLLM、SGLang、ONNX、OpenXLA | 开源 runtime 降低硬件抽象门槛 | CUDA kernel、cuDNN、TensorRT、NIM、Dynamo、企业支持和性能工程深度 |
| 低延迟推理 | Groq、Cerebras、d-Matrix、Etched、MatX、TPU/Trainium inference | 单一推理 workload 成本可能低于 GPU | NVIDIA 通过 LPX/Groq 授权、Dynamo、STX 把异构推理纳入平台 |

### 新技术是否会成为主流

| 技术 | 主流性判断 | 风险和替代 |
|---|---|---|
| NVL72/rack-scale liquid-cooled AI supercomputer | 已经是高端 AI 训练和推理的主流采购单位 | 电力/液冷/整柜交付难度高；AMD Helios、TPU pod、Trainium UltraServer 会复制 rack-scale 路线 |
| GB300/B300 Blackwell Ultra | 2026 主流高端平台 | 若 Rubin 切换过快，部分客户可能延迟采购；若 HBM3E 受限，交付受压 |
| Vera Rubin | 2026H2-2027 高端新增主流候选 | HBM4、CoWoS、CX9、液冷认证风险；ASIC 可能截流部分推理 |
| Spectrum-X Ethernet | AI Ethernet 主流路线之一 | Broadcom/Arista/Cisco 的开放 Ethernet 生态竞争强；客户可能避免单供应商 |
| NVLink Fusion | 可能成为 NVIDIA 对 custom ASIC 的“开放式锁定”工具 | 若 UALink/UEC 生态成熟，客户可能选择更开放标准 |
| LPX/Groq | 高端推理小而潜力大，是否主流取决于真实 token economics | GPU-only、TPU/Trainium、专用推理 ASIC 都是替代 |
| STX/CMX context memory | Agent/long-context 推理下很可能成为新增层 | 传统高性能存储、CXL memory、云厂自研 KV cache 系统会竞争 |

### 客户替换成本

NVIDIA 客户替换成本极高，主要来自五层：第一，模型训练和推理 kernel 已针对 CUDA/NCCL/TensorRT 调优；第二，集群网络从 NVLink 到 Spectrum-X/InfiniBand 与调度软件强绑定；第三，AI factory 的电力、液冷、机架、网络、存储参考设计已经按 NVIDIA 平台认证；第四，开发者、企业软件、容器镜像、监控、安全和 MLOps 工具链围绕 NVIDIA 优化；第五，供应链和交期上，NVIDIA 拥有 HBM/CoWoS/ODM 优先级。替换不是“换一张卡”，而是重写性能工程、重做集群网络和重走客户认证。

## 9. 核心风险

| 风险 | 影响 |
|---|---|
| AI CapEx ROI 不及预期 | 云厂和 neocloud 若发现 token 收入覆盖不了折旧/电力/融资，订单节奏可能放缓 |
| HBM/CoWoS/ABF/液冷/电力瓶颈 | 需求不变也可能导致收入确认延后，或毛利被高成本侵蚀 |
| Hyperscaler ASIC 替代 | Google/AWS/Meta/Microsoft/OpenAI 可把内部稳定 workload 转向自研 ASIC，压低 NVIDIA 份额或议价 |
| 出口管制 | 中国 Data Center compute 收入不确定，H20/H200/后续合规产品都可能受政策波动 |
| 客户集中 | FY2026 一个 direct customer 占 22%，另一个占 14%；top 5 cloud/hyperscaler 略高于 DC 收入 50% |
| 毛利率结构 | Blackwell/Rubin rack-scale 系统 BOM 更复杂，HBM/液冷/网络成本高于 Hopper HGX，若溢价下降会压毛利 |
| 资本配置和生态投资 | 大额战略投资、授权和伙伴融资可能放大生态，但也可能带来减值或关联交易审视 |

## 10. 结论

NVDA 当前最核心的投资判断不是“GPU 还缺不缺”，而是：AI 工厂从训练走向 agentic inference 后，NVIDIA 能否继续把每一代新增复杂度变成自己的收费层。FY2026 已经证明它不仅吃 GPU compute，还把 networking 做到 $31.4B 年收入、Q4 $11B 单季收入；Q1 FY2027 $78B 指引且不含中国 Data Center compute，更证明欧美/中东/主权 AI 需求足以支撑下一轮增长。

未来 12 个月最重要的观察顺序是：GB300/B300 实际交付、Rubin H2 2026 ramp、HBM4 认证与供应、networking attach 率、OpenAI/Anthropic/Meta/CoreWeave 的 GW 级项目兑现、以及云厂 token ROI 是否能继续上修 CapEx。基准情形下，NVDA 仍能在 FY2027 维持高双位数增长；乐观到极度乐观情形下，NVIDIA 的收入密度会从“每 GPU”继续上移到“每 rack / 每 MW / 每 GW”，估值锚也会从芯片公司进一步向 AI factory 平台公司移动。

## 主要信息源

- NVIDIA FY2026 Q4 earnings release / 8-K: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm
- NVIDIA FY2026 Form 10-K: https://s201.q4cdn.com/141608511/files/doc_financials/2026/q4/10K-NVDA.pdf
- NVIDIA FY2026 Q4 earnings call transcript: https://s201.q4cdn.com/141608511/files/doc_financials/2026/q4/NVDA-Q4-2026-Earnings-Call-25-February-2026-5_00-PM-ET.pdf
- NVIDIA FY2026 Q3 earnings release: https://www.sec.gov/Archives/edgar/data/1045810/000104581025000228/q3fy26pr.htm
- NVIDIA FY2026 Q3 earnings call transcript: https://s201.q4cdn.com/141608511/files/doc_financials/2026/q3/NVDA-Q3-2026-Earnings-Call-19-November-2025-5_00-PM-ET.pdf
- NVIDIA FY2026 Q2 earnings release: https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2026/default.aspx
- NVIDIA FY2026 Q2 earnings call transcript: https://s201.q4cdn.com/141608511/files/doc_financials/2026/q2/NVDA-Q2-2026-Earnings-Call-27-August-2025-5_00-PM-ET.pdf
- NVIDIA FY2026 Q1 earnings release: https://www.sec.gov/Archives/edgar/data/1045810/000104581025000115/q1fy26pr.htm
- NVIDIA GB300 NVL72: https://www.nvidia.com/en-us/data-center/gb300-nvl72/
- NVIDIA Vera Rubin platform release: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx
- NVIDIA Vera Rubin technical blog: https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/
- NVIDIA Spectrum-X Ethernet / MRC: https://blogs.nvidia.com/blog/spectrum-x-ethernet-mrc/
- Yahoo Finance NVDA statistics, 2026-05 初：https://finance.yahoo.com/quote/NVDA/
- StockAnalysis NVDA financials/ratios: https://stockanalysis.com/stocks/nvda/
- Tom's Hardware FY2026 Q4 summary and segment discussion: https://www.tomshardware.com/pc-components/gpus/nvidia-posts-record-usd215-billion-annual-revenue-in-latest-quarterly-earnings-report-gaming-gpus-now-only-11-45-percent-of-revenue
- TrendForce AI capacity / CoWoS / supply-chain references, 2026: https://www.trendforce.com/presscenter/
- 项目内非公司调研底稿：`行业调研/AI头部芯片市场占比和规模.md`、`行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`、`conference_update/nvidia_gtc_2026_research.md`、`行业调研_AI服务器_存储_芯片/行业调研_AI服务器整机与机架集成_2026-05-08.md`、`行业调研_AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026.md`、`行业调研_AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-05-08.md`、`行业调研_AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-05-08.md`、`行业调研_AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026.md`

