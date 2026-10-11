# 公司：AMD Advanced Micro Devices, Inc.（AMD）全面尽调

> 研究日期：2026-05-10。市场数据使用美股 2026-05-08 盘后/2026-05-09 00:15 UTC 附近可得数据；财务数据以 AMD FY2026 Q1（季度结束 2026-03-28，公告 2026-05-05）为最新口径。除特别说明外，金额单位为美元。本文为产业和公司研究，不构成投资建议。

## 核心结论

1. **AMD 已从“PC CPU/GPU 周期股”转成“AI 数据中心第二供应源 + x86 服务器份额扩张 + 开放 rack-scale 平台”公司。** 最新 Q1 2026 收入 $10.253B，同比增长 38%；Data Center 收入 $5.775B，同比增长 57%，占总收入 56.3%，已是主引擎。
2. **估值已经在提前定价 MI450/Helios 成功。** 最新股价约 $455.19，市值约 $751.1B，TTM P/E 约 149x，forward P/E 约 47x，TTM P/S 约 20.1x。这个估值不再只靠 EPYC/MI350 解释，核心押注是 OpenAI 与 Meta 两个 6GW 协议、2026H2 MI450/Helios 爬坡和 2027 “tens of billions” Data Center AI revenue。
3. **真实订单能见度显著提高，但不是传统 backlog 披露。** AMD 不披露 backlog/bookings。可验证订单信号包括：OpenAI 6GW、Meta up to 6GW、两个客户各自最多 160M 股权证且按 Instinct GPU 采购里程碑归属；Q1 2026 10-Q 显示 OpenAI/Meta warrant 截至 2026-03-28 尚未 vest，说明大额收入仍在前方。
4. **最大瓶颈是 HBM4/HBM3E、先进封装、rack 级液冷/供电、UALoE/以太网 scale-up 互操作和 ROCm 生态成熟度。** 项目内 AI/HBM/封装底稿显示，2026 主线仍是 HBM3E 12Hi，2026H2-2027 高端增量转向 HBM4；MI455X/Helios 的斜率由 HBM4 allocation、CoWoS/ABF、rack burn-in 和客户上电共同决定。
5. **未来一年最值得跟踪的不是 PC，也不是传统 Radeon，而是五条线：MI350/MI355/MI350P、MI450/MI455X/Helios、EPYC Venice/Verano、Pensando Pollara/Vulcano AI networking、ROCm/Enterprise AI software。**

## 1. 业务、市场认知、产业链位置和估值

### 1.1 AMD 是什么公司

AMD 是 fabless 高性能计算芯片公司，核心资产是 CPU/GPU/DPU/FPGA/Adaptive SoC 设计、系统级参考架构、软件栈和客户工程能力。制造依赖 TSMC、先进封装、HBM 供应商、OSAT、ODM/OEM 和云客户认证。

| 业务分部 | 最新 Q1 2026 收入 | 占比 | 主要产品 | 投资人如何看 |
|---|---:|---:|---|---|
| Data Center | $5.775B | 56.3% | EPYC 服务器 CPU、Instinct AI GPU、Pensando DPU/AI NIC、FPGA/Adaptive SoC、AI rack 方案 | AI 基建第二供应源；x86 server share gainer；对 NVIDIA 的开放生态挑战者 |
| Client and Gaming | $3.605B | 35.2% | Ryzen CPU/APU、Radeon GPU、游戏主机 semi-custom SoC | 现金流和份额扩张，但内存涨价/PC 周期波动较大 |
| Embedded | $873M | 8.5% | Xilinx FPGA、Versal Adaptive SoC、嵌入式 CPU/GPU/APU/SOM | 高毛利、周期修复慢；边缘 AI/网络/工业是可选弹性 |

产业链位置：

| 层级 | AMD 的位置 | 关键上游 | 关键下游 |
|---|---|---|---|
| 算力芯片 | Merchant AI GPU + server CPU + DPU/NIC | TSMC 3nm/5nm/6nm、HBM、CoWoS/先进封装、ABF | Microsoft、Meta、OpenAI、Oracle、OCI、HPE/Dell/Supermicro、主权 AI、企业 AI |
| Rack-scale 平台 | Helios 开放 rack 设计，不直接做全部制造 | ZT Systems 设计团队、Sanmina/Celestica、液冷/电力/网络供应链 | Hyperscaler 和 OEM 整柜采购 |
| 软件生态 | ROCm、Enterprise AI Suite、Silo AI/Nod.ai 软件能力 | 开源框架、compiler/runtime、模型优化团队 | AI lab、云服务商、企业私有 AI |
| 网络互联 | Pensando Pollara/Vulcano、UALoE/Ultra Ethernet 方向 | Broadcom/Celestica/UEC/UALink/OCP 生态、800G/1.6T optics | 非 NVIDIA 开放 AI fabric |

### 1.2 最近三年重大变化、转型和收购

| 时间 | 事项 | 对业务的含义 |
|---|---|---|
| 2023-10 | 收购 Nod.ai | 补开源 AI compiler/runtime，增强 ROCm 和模型部署能力。 |
| 2024-07/08 | 宣布并完成收购 Silo AI，交易约 $665M | 把模型、客户工程和企业 AI 服务能力补进 AMD AI stack。 |
| 2024-08 至 2025-03 | 宣布并完成收购 ZT Systems，交易约 $4.9B | 获得 hyperscale AI 服务器/rack 设计能力，服务 Helios 和端到端系统设计。 |
| 2025-05 至 2025-10 | 宣布并完成将 ZT Systems 数据中心制造业务出售给 Sanmina，交易约 $3B | AMD 保留系统设计与客户工程，减少低毛利制造资产负担。 |
| 2025-10 | OpenAI 6GW AMD Instinct GPU 协议，首个 1GW 从 MI450/2026H2 开始 | AMD 从“替代 GPU”进入 frontier AI lab 的核心算力供应商名单。 |
| 2025-11 | Financial Analyst Day：提出 >35% revenue CAGR、>$20 non-GAAP EPS 战略目标 | 管理层把公司重新锚定在 $1T compute market 和 Data Center AI 长周期。 |
| 2026-02 | Meta up to 6GW AMD Instinct GPU 协议，首个 1GW 2026H2，Helios/MI450/custom GPU | 第二个超大 GW 级客户，强化订单能见度和 Helios 路线。 |
| 2026-03 | Celestica 合作 Helios scale-up switch；Samsung HBM4 合作 MI455X | 证明 Helios 不是单芯片，而是 rack/network/HBM 共同验证项目。 |
| 2026-05 | Q1 2026：Data Center 首次站稳 $5.8B 季度收入；MI450 已向 lead customers sampling | 市场关注点切到 2026H2 initial volume、Q4 ramp、2027 annual AI revenue。 |

### 1.3 最新估值和财务健康

| 指标 | 最新值 | 日期/口径 | 解读 |
|---|---:|---|---|
| 股价 | $455.19 | 2026-05-09 00:15 UTC 附近市场数据 | Q1 后高位，已明显定价 AI ramp。 |
| 市值 | $751.1B | 同上 | 相当于 TTM revenue 约 20x。 |
| TTM P/E | 约 149x | 以 TTM GAAP EPS/市场数据 | GAAP EPS 被摊销、投资收益、税项影响；仍属高估值。 |
| Forward P/E | 约 47x | 2026-05-07 左右第三方共识数据 | 市场押注 2026H2-2027 EPS 快速上行。 |
| TTM P/S | 约 20.1x | 市值 / Q2 2025-Q1 2026 TTM 收入 $37.454B | 高于传统半导体周期股，接近平台型 AI 预期。 |
| Q1 2026 收入增速 | +38% YoY | AMD Q1 2026 | Data Center 和 Client/Gaming 拉动。 |
| TTM 收入增速 | 约 +35% YoY | Q2 2025-Q1 2026 vs Q2 2024-Q1 2025 | 增长已从 2025 延续到 2026。 |
| Q1 2026 毛利率 | GAAP 53%；non-GAAP 55% | AMD Q1 2026 | Data Center mix 提升带动。 |
| TTM GAAP 毛利率 | 约 50.3% | 四季度 gross profit / revenue | Q2 2025 MI308 出口管制 charge 压低 TTM。 |
| Q1 2026 净利率 | 13.5% GAAP | net income $1.383B / revenue $10.253B | Non-GAAP 盈利能力更强。 |
| TTM 净利率 | 约 13.4% GAAP | TTM net income $5.009B / revenue $37.454B | 收入增长快于 GAAP 利润改善。 |

资产负债表健康度：**强。** Q1 2026 现金、现金等价物和短期投资 $12.347B，总债务 $3.224B，净现金约 $9.123B；流动资产 $28.628B，流动负债 $10.506B，current ratio 约 2.7x；Q1 free cash flow $2.566B，TTM FCF 约 $7.36B。主要风险不在偿债，而在 **为 AI ramp 提前锁供应**：Q1 10-Q 披露 total purchase commitments 约 $25.7B，其中 2026 剩余期间约 $18.3B。若 MI450/Helios 客户上电或认证推迟，预付款和长协会放大库存/毛利波动。

## 2. 最新五个财报季度拆解

AMD 不披露 backlog/bookings/B2B/lead time/cancel rate。下表的订单与交期为基于官方披露、客户协议、供应链瓶颈和项目内 AI/HBM/封装模型的推断。

| 财报季度 | 总收入 / 增速 | 毛利率 | 分部收入 | 分部利润率 | AI 数据中心收入占比估算 | 订单、交期、取消率/风险推断 |
|---|---:|---:|---|---|---|---|
| Q1 2026 | $10.253B，+38% YoY，QoQ flat | GAAP 53%；non-GAAP 55% | Data Center $5.775B；Client $2.885B；Gaming $0.720B；Embedded $0.873B | DC 27.7%；C&G 15.9%；Embedded 38.7% | Instinct/AI 系统约 $2.2-3.0B，占总收入 22-30%，占 DC 40-52% | MI450 已 sampling；Helios 2026H2 production shipments。OpenAI/Meta 6GW 协议提供多年能见度，但 warrants 尚未 vest。HBM4/CoWoS/Helios burn-in 是主交期约束；已签首 GW 取消率估计低于 10-15%，延期风险高于取消风险。 |
| Q4 2025 | $10.270B，+34% YoY，+11% QoQ | GAAP 54%；non-GAAP 57% | DC $5.380B；Client $3.097B；Gaming $0.843B；Embedded $0.950B | DC 32.6%；C&G 18.4%；Embedded 37.6% | 约 $2.0-2.7B，占总收入 19-26% | MI350 部署加速，Q1 2026 指引含约 $100M MI308 China revenue。订单从 MI350 转向 MI450 规划，lead time 约 2-4 个季度。 |
| Q3 2025 | $9.246B，+36% YoY，+20% QoQ | GAAP 52%；non-GAAP 54% | DC $4.341B；Client $2.750B；Gaming $1.298B；Embedded $0.857B | DC 24.7%；C&G 21.4%；Embedded 33.0% | 约 $1.4-2.0B，占总收入 15-22% | 未包含 MI308 China shipments；DC 增长来自 5th Gen EPYC 与 MI350。OpenAI 6GW 刚公布，pipeline 明显提高但未转收入。 |
| Q2 2025 | $7.685B，约 +32% YoY，+3% QoQ | GAAP 40%；non-GAAP 43%，剔除 $800M MI308 charge 后约 54% | DC $3.240B；Client $2.499B；Gaming $1.122B；Embedded $0.824B | DC -4.8%；C&G 21.2%；Embedded 33.4% | 约 $0.8-1.4B，占总收入 10-18% | 美国出口管制导致 MI308 inventory and related charges $800M，是订单/供给错配的显性风险案例。AI GPU 中国敞口被压缩，客户转向非中国大客户。 |
| Q1 2025 | $7.438B，+36% YoY | GAAP 50%；non-GAAP 54% | DC $3.674B；Client $2.294B；Gaming $0.647B；Embedded $0.823B | DC 25.4%；C&G 16.9%；Embedded 39.9% | 约 $1.0-1.6B，占总收入 13-22% | MI300/MI325 与 EPYC 同步贡献；Data Center YoY +57%。当时订单能见度弱于 2026，更多依赖 hyperscaler 试点转量产。 |

关键观察：

- **Data Center 占比从 Q2 2025 的 42.2% 升到 Q1 2026 的 56.3%。** Q2 2025 受 MI308 出口管制 charge 扰动，Q3 后恢复增长。
- **C&G 虽然收入高，但不再是估值核心。** Q1 2026 管理层提示 2026H2 gaming demand 可能受 memory/component cost 影响。
- **Embedded 毛利/利润率高，但收入增长弱。** 它是质量资产和边缘 AI 期权，不是未来一年主 EPS 斜率。

## 3. 2026 最新指引、业务占比和产品映射

### 3.1 Q2 2026 指引和收入占比估算

AMD 指引 Q2 2026 收入约 $11.2B +/- $0.3B，non-GAAP gross margin 约 56%。管理层口径是 Data Center 强增长，Client/Gaming modest growth，Embedded double-digit growth。

| 项目 | Q2 2026 指引/估算 | 占比估算 | 增长判断 |
|---|---:|---:|---|
| 总收入 | $10.9-11.5B，中点 $11.2B | 100% | YoY 约 +46%，QoQ 约 +9% |
| Data Center | $6.4-6.8B | 57-61% | 继续最突出；EPYC + Instinct 共同增长，MI450 暂以 sampling/早期贡献为主 |
| Client and Gaming | $3.6-3.8B | 32-34% | 低到中个位数增长，2026H2 受内存/组件成本压力 |
| Embedded | $0.95-1.05B | 8-9% | double-digit growth，库存消化后恢复 |
| Non-GAAP GM | 约 56% | - | Data Center mix、MI350/EPYC mix 改善，但 HBM/先进封装成本仍高 |

### 3.2 产品矩阵：重点、潜力小业务和可跳过业务

| 业务/产品 | 型号/平台 | 2026 状态 | 投资重要性 | 备注 |
|---|---|---|---|---|
| AI GPU：MI350 系列 | MI350X、MI355X、MI350P；8-GPU UBB/OAM；PCIe 企业形态 | 量产放量，2026 最确定收入 | 极高 | 288GB HBM3E、8TB/s，8-GPU 平台 2.3TB HBM3E/64TB/s。MI350P/PCIe 是企业和较低部署门槛的小弹性。 |
| AI rack：MI450/MI455X/Helios | MI450 custom、MI455X、Helios 72-GPU rack、MI400 family | sampling，2026H2 initial volume，Q4 ramp | 最高 | OpenAI/Meta up to 12GW 合计意向；HBM4、UALoE、全液冷、rack burn-in 决定斜率。 |
| Server CPU | EPYC 9005 Turin、6th Gen EPYC Venice、Verano | EPYC 持续份额扩张，Venice 2026 lead customer validation | 很高 | CPU 是 AI rack host/control plane 与传统云服务器份额双线；毛利通常高于系统集成。 |
| AI networking | Pensando Pollara 400、Vulcano 800、Elba/Salina DPU、Helios scale-up switch/UALoE | Pollara/400G 已部署，Vulcano/800G 与 Helios 绑定 | 高 | 小而关键；决定 AMD 能否从 GPU 单品进入完整 AI fabric。 |
| ROCm/AI software | ROCm 7、Enterprise AI Suite、Nod.ai/Silo AI 能力 | 快速成熟但收入多随硬件打包 | 高 | 不一定单独高收入，但直接影响 GPU attach、客户切换成本和毛利。 |
| Adaptive/Embedded AI | Versal AI Edge/Prime/Premium、Alveo、FPGA/SmartNIC | 收入修复慢，边缘 AI/电信/国防有期权 | 中 | 不能漏掉，但未来一年对公司收入增速贡献低于 DC AI。 |
| Client AI PC | Ryzen AI 300/400、Ryzen AI Max | 有份额和 ASP 改善 | 中低 | AI PC 叙事强，但美元弹性远低于 Data Center。 |
| 可跳过/低优先级 | Radeon consumer GPU、semi-custom console SoC、传统嵌入式工业 FPGA、普通 PC chipset | 成熟/周期/低增速 | 低 | 可提供现金流和品牌，但不是 AI 基建核心。 |

## 4. 高增长/关键产品的当前贡献和战略评分

评分：5 为最高。收入为 AMD 口径估算，不含 OEM/ODM 对整机的全部加价，避免把同一 rack BOM 重复算进 AMD 收入。

| 产品/业务 | 当前收入贡献估算 | 收入增速 | AI 基建重要性 | 时间紧急性 | 供需紧张程度 | 垄断/溢价能力 | 交叉验证 |
|---|---:|---:|---:|---:|---:|---:|---|
| MI350X/MI355X/MI350P | Q1 2026 约 $2.2-3.0B；2026 年化约 $10-14B | YoY 约 +70-120% | 5 | 5 | 4 | 3 | Q1 DC +57%；MI350 官方 288GB HBM3E；项目底稿把 MI350 列为 2026 AMD 最确定放量产品。 |
| MI450/MI455X/Helios | Q1 2026 收入很小，主要是 sampling/NRE；订单可见度来自 OpenAI/Meta | 从 0 到多十亿美元 | 5 | 5 | 5 | 4 | OpenAI 6GW、Meta up to 6GW、首 GW 均指向 2026H2；Celestica Helios switch；Samsung HBM4 for MI455X。 |
| EPYC server CPU | DC remainder 中约 $2.7-3.3B/quarter；TTM 约 $11-13B | Q2 2026 server CPU revenue 指引 >70% YoY | 4 | 4 | 3 | 4 | EPYC 9005/5th Gen share gains；Meta 为 Venice lead customer；AI rack 需要 CPU host/control。 |
| Pensando AI NIC/DPU | 约 $0.2-0.5B/quarter，更多随系统绑定 | +50% 以上潜力 | 4 | 4 | 4 | 3 | Pollara/Vulcano 与 Helios、Ultra Ethernet/UALoE 绑定；但独立份额低于 NVIDIA/Broadcom。 |
| ROCm/AI software/services | 直接收入小，估计 <$0.5B/quarter；间接影响 GPU 销售 | 高但难拆 | 5 | 5 | 2 | 3 | ROCm 是客户从 CUDA 转入 AMD 的门票；Silo AI/Nod.ai 加强客户工程。 |
| Adaptive/Embedded AI | Embedded Q1 $0.873B，AI 子集估计 <$0.2B/quarter | 中低 | 2-3 | 2 | 2 | 3 | Xilinx/Versal 高毛利，但库存周期和应用碎片化导致未来一年主线不强。 |

## 5. 一年后收入贡献三情景

时间口径：从 2026-05 往后约 12 个月，到 2027Q2 前后形成的年化贡献。重要性/紧张度/溢价仍按 1-5 评分。

| 产品/业务 | 基准情景 | 乐观情景 | 极度乐观情景 |
|---|---|---|---|
| MI350X/MI355X/MI350P | 年化 $11-14B，增速 +20-40%；重要性 5，紧张 3-4，溢价 3 | 年化 $16-22B，增速 +50-80%；MI350P/企业推理超预期；紧张 4，溢价 3-4 | 年化 $25-32B，增速 +100%+；HBM3E allocation 强，NVIDIA 供给不足外溢；紧张 5，溢价 4 |
| MI450/MI455X/Helios | 年化 $12-18B；Q3 initial、Q4/Q1 ramp，首 GW 分批收入；重要性 5，紧张 5，溢价 4 | 年化 $25-40B；OpenAI/Meta 首 GW 都按期上电，新增 multi-GW customer；紧张 5，溢价 4 | 年化 $45-65B；2027 需求前置、HBM4/CoWoS/液冷均可交付；紧张 5，溢价 4-5 |
| EPYC server CPU | 年化 $18-22B，增速 +40-60%；Venice 带动 cloud/AI host；重要性 4，紧张 3，溢价 4 | 年化 $23-28B，增速 +70-100%；AI rack attach + traditional server share 双击 | 年化 $30-35B，增速 +120% 左右；Intel/Arm 竞争弱化，Venice/Verano 大客户锁量 |
| Pensando AI NIC/DPU | 年化 $1.5-3B；随 MI350/Helios attach | 年化 $3-5B；Vulcano 800 与 Helios/UEC/UALoE design win 扩大 | 年化 $5-8B；开放 AI fabric 变成采购清单，AMD 把 NIC/DPU 与 GPU 打包销售 |
| ROCm/software/services | 直接 $0.5-1.5B，更多体现在 GPU 毛利和赢单 | $1.5-3B，企业 AI Suite、Silo AI 服务与云托管扩大 | $3-5B，ROCm 成为非 NVIDIA AI stack 的事实标准之一 |
| Adaptive/Embedded AI | $3.8-4.2B segment 年收入，AI 子集小 | $4.5-5.2B，工业/国防/边缘 AI 恢复 | $6B+，但仍非公司主线 |

合并判断：基准情景下 AMD Data Center 未来 12 个月可从 TTM 约 $18.7B 提升到约 $32-38B；乐观 $42-55B；极度乐观 $60-75B。这个区间的核心差异来自 MI450/Helios 可交付容量，而不是传统 PC。

## 6. BOM、单位内容量、价格传导、当前产能和认证

### 6.1 MI350/MI355/MI350P

| 维度 | 内容量 / 价格链 |
|---|---|
| 每 GPU | MI355X：288GB HBM3E、8TB/s memory bandwidth、10.1 PFLOPs MXFP4/MXFP6、约 1.0-1.4kW OAM 级功耗区间；MI350P PCIe 形态按 144GB HBM3E 级别看，是企业/边缘数据中心更容易部署的补充。 |
| 每 8-GPU 平台 | 2.3TB HBM3E，64TB/s aggregate memory bandwidth，约 80.5 PFLOPs MXFP4/MXFP6；Infinity Fabric scale-up。 |
| 每 rack | 官方披露 MI350 系列可支持最多 64 GPU air-cooled rack、128 GPU direct liquid-cooled rack；128 GPU DLC 对应约 36.9TB HBM3E、约 1.3 exaFLOPS MXFP4/MXFP6。 |
| 每 MW | 若 128-GPU DLC rack 约 200-250kW 全系统，1MW 可容纳约 4-5 rack、512-640 GPU、约 147-184TB HBM3E。GPU-only 理论上 1MW/1.4kW 约 714 GPU，但真实部署需扣除 CPU、NIC、switch、PSU、液冷和冗余。 |
| 每 optical port | MI350 scale-out 多以 400G/800G Ethernet/InfiniBand/RoCE 接入；估算每 GPU 1-2 个 400G/800G 外联端口。800G 光模块/端口约 $800-2,000，AEC/DAC 较低；AMD 捕获 NIC/DPU/部分系统 silicon，光模块利润主要在光互联供应链。 |
| HBM 成本传导 | 项目 HBM 底稿估 HBM3E 12Hi 36GB stack 基准 $450-650、乐观 $600-800、极度 $750-1,000。MI355X 288GB 约 8 stack，仅 HBM 成本约 $3.6-8.0k/GPU，再加 logic die、CoWoS/基板、测试、良率损失。 |
| AMD ASP/毛利推断 | 批量 GPU ASP 估 $18-28k；GPU gross margin 约 45-60%。高内存容量支撑定价，但 NVIDIA CUDA/NVLink 生态限制 AMD 溢价。 |
| 当前产能能力 | 2026 年 MI350 系列 AMD 收入能力估 $12-22B；若 HBM3E/CoWoS 顺畅和企业 PCIe 放量，可到 $30B+。 |
| 供应链采纳/认证 | MI350 已量产并进入 OEM/CSP 平台；Dell/HPE/Supermicro/OCI 等生态支持，Upstage 等主权/企业 AI 使用 MI355。认证阶段：量产部署 + 客户 burn-in。 |

### 6.2 MI450/MI455X/Helios

| 维度 | 内容量 / 价格链 |
|---|---|
| 每 GPU | MI455X/MI450 family 面向 HBM4，项目底稿按约 432GB HBM4、约 19.6TB/s 级 memory bandwidth 估算；具体最终规格以 AMD 量产资料为准。 |
| 每 rack | Helios 72-GPU rack；公开口径为约 31TB HBM4、约 1.4PB/s aggregate bandwidth、最高约 2.9 FP4 exaFLOPS/1.4 FP8 exaFLOPS；搭配 EPYC Venice、Pensando Vulcano/AI networking、UALoE scale-up switches。 |
| 每 MW | 若 Helios 全系统 rack 约 180-220kW，1MW 约 4.5-5.5 rack、324-396 GPU、约 140-170TB HBM4、约 13-16 FP4 exaFLOPS。若客户按更高冗余/冷却 overhead，GPU/MW 会低于该区间。 |
| 每 optical port | Scale-up 以 UALoE/以太网架构和 rack 内铜/AEC/retimer 为主，rack-to-rack scale-out 使用 800G/1.6T optics。估算每 GPU 1-2 个 800G/1.6T 外联等效端口；72-GPU rack 外联 72-144 个高速端口，另有 scale-up switch 内部端口。 |
| HBM4 BOM | HBM4 12Hi 36GB stack 项目底稿估基准 $650-950、乐观 $900-1,250、极度 $1,200-1,600。若 432GB/GPU 约 12 stack，仅 HBM4 成本约 $7.8-19.2k/GPU。HBM4 base die、KGD、TC bonding、CoWoS/ABF、burn-in 使总 BOM 敏感度高。 |
| AMD ASP/毛利推断 | MI450/MI455 GPU ASP 估 $35-60k；Helios AMD 可捕获 GPU+CPU+NIC+部分系统价值，单 rack AMD silicon/system revenue 估 $2.8-4.5M，完整 OEM rack 成本/售价更高。若首 GW 约 4,500-5,500 rack，单 GW 对 AMD 可对应 $12-22B 级收入池，取决于收入确认、GPU ASP 和客户折扣。 |
| 当前产能能力 | Q1 2026 主要是 sampling，无显著收入；2026H2 初始收入能力估 $2-8B，2027 放大到 $18-40B 基准/乐观区间。 |
| 供应链采纳/认证 | OpenAI、Meta 首 GW 2026H2；Celestica 负责 Helios scale-up switches，late 2026 可用；Samsung 合作 MI455X HBM4；认证阶段：lead customer qualification、HBM4 allocation/validation、rack burn-in、UALoE interop。 |

### 6.3 EPYC、Pensando 和 ROCm

| 产品 | BOM/内容量 | 当前产能和采纳 | 价格传导 |
|---|---|---|---|
| EPYC 9005/Venice/Verano | CPU die/chiplet + I/O die + DDR5/MRDIMM/SOCAMM2 ecosystem；AI rack host/control plane，一般每 4-8 GPU 节点配 1-2 CPU | EPYC cloud instance 和 server share 持续增长；Meta 为 Venice lead customer | CPU 单价低于 GPU，但毛利高、供给相对可控；AI rack 绑定提高 attach。 |
| Pensando Pollara/Vulcano | AI NIC/DPU、P4 programmable、RDMA/congestion/security/offload；每 GPU 1-2 个高端 endpoint 端口或每节点数个 NIC | Pollara 400 已进入 AI NIC；Vulcano 800 与 Helios/UEC/UALoE 绑定 | 单卡/芯片 ASP 远低于 GPU，但高端 NIC gross margin 可 55-70%；可提高 AMD rack 粘性。 |
| ROCm/Enterprise AI Suite | Compiler/runtime/library/container/Kubernetes/model optimization；Silo AI/Nod.ai 客户工程 | ROCm 成熟度是客户从 CUDA 转移的核心认证项 | 软件直接收入小，但可把 GPU ASP 折扣压力转成“总拥有成本”和部署效率收益。 |

## 7. 一年后产能能力、采纳程度和认证阶段三情景

| 产品/业务 | 基准 | 乐观 | 极度乐观 |
|---|---|---|---|
| MI350 系列 | 年收入产能 $12-16B；HBM3E 仍紧但可交付；CSP/OEM 认证稳定 | $18-24B；MI350P/企业推理扩展，更多 sovereign AI | $30B+；NVIDIA 供应不足和 AMD 价格优势导致额外 allocation |
| MI450/MI455X/Helios | 年收入产能 $12-18B；OpenAI/Meta 首 GW 分批，late 2026-early 2027 rack 认证完成 | $25-40B；两大客户首 GW 按期，新增 multi-GW pipeline 转 purchase order | $45-65B；HBM4、CoWoS、Celestica switch、液冷/电力均可交付，客户把 2027 需求前置 |
| EPYC Venice/Verano | $18-22B CPU 年化收入；Meta/云客户 validation 后量产 | $23-28B；Venice 在 AI host 和 general purpose cloud 同时抢份额 | $30B+；Intel 供给/性能不及预期、Arm 渗透放慢 |
| Pensando/Vulcano | $1.5-3B；Helios attach，仍以配套为主 | $3-5B；800G NIC/UEC/UALoE 成为 AMD rack 标配 | $5-8B；开放 AI fabric 大规模替代部分封闭 NVLink/IB 体系 |
| ROCm/software | 直接 $0.5-1.5B；认证重点是 PyTorch、Triton、vLLM、Megatron/DeepSpeed、K8s | $1.5-3B；Enterprise AI Suite 与 Silo AI 客户工程商业化 | $3-5B；ROCm 成为大模型推理多供应商部署标准选项 |

## 8. 订单积压和供给推断下的未来一年业务增速

AMD 无 backlog 披露。以下将“订单积压”拆成四类：已签/带 warrant 的 GW 协议、公开客户部署、供应链采购承诺、pipeline/论坛和会议线索。

| 证据类型 | 真实度 | 已知事实 | 对未来一年收入的含义 |
|---|---:|---|---|
| OpenAI 6GW | 高 | 首个 1GW MI450 in 2H 2026；warrant up to 160M shares，按 Instinct GPU purchase milestones vest | 是 MI450/Helios 最硬订单之一；2026H2 开始收入，2027 放大。 |
| Meta up to 6GW | 高 | 首个 1GW 2026H2，custom MI450-based GPU + EPYC Venice + ROCm + Helios；warrant up to 160M shares | 第二个 GW 级锚定客户；强化 HBM4/Helios 供应链锁定。 |
| Q1 2026 10-Q purchase commitments | 高 | 总 purchase commitments 约 $25.7B，2026 剩余约 $18.3B | 证明 AMD 正提前锁 wafer/package/HBM/供应，但不是客户 backlog；若需求错配会转库存风险。 |
| Q1 2026 commentary | 中高 | MI450 sampled to lead customers，Helios production shipments 2026H2；lead customer forecasts exceeding initial expectations | 指向 Q3 initial volume、Q4 ramp、Q1 2027 继续爬坡。 |
| OCI/HPE/Celestica/Samsung/Upstage 等 | 中高 | MI350 deployment、Helios OEM/ODM/switch/HBM4 生态 | 说明从芯片到 rack 的 partner network 已搭建，降低执行风险。 |
| 论坛/散户/渠道讨论 | 低到中 | AMD_Stock/硬件社区讨论集中在 MI450/Helios 和 “tens of billions” 叙事 | 可作为情绪/关注度信号，不作为订单核心证据。 |

未来一年增速预测：

| 情景 | Data Center 收入 | 公司总收入 | 关键假设 | 最大风险 |
|---|---:|---:|---|---|
| 基准 | $32-38B，较 TTM $18.7B 增长约 +70-100% | $55-62B，较 TTM $37.5B 增长约 +47-65% | MI350 稳定，MI450 Q3 initial/Q4 ramp，EPYC server CPU +70% Q2 后维持高增 | Helios 认证延迟、HBM4 初期良率、客户上电分批 |
| 乐观 | $42-55B，+125-195% | $65-80B，+75-115% | OpenAI/Meta 首 GW 同步推进，新增 sovereign/neo-cloud 订单，HBM4 多供顺利 | 光/网络/液冷/电力工程延迟；NVIDIA 降价 |
| 极度乐观 | $60-75B，+220-300% | $90-105B，+140-180% | 2027 需求前置，MI450/Helios 成为第二个规模化 rack 平台，ROCm 推理效率被广泛接受 | 数据中心电力、融资、token ROI、供应链全部需要同时顺利，难度很高 |

## 9. 竞争格局、技术主流性、替代风险和客户切换成本

### 9.1 MI350/MI355/MI350P

| 维度 | 判断 |
|---|---|
| 主要竞争对手 | NVIDIA H200/B200/GB200/GB300；部分自研 ASIC；Intel Gaudi/Jaguar Shores 长线。 |
| AMD 优势 | HBM 容量高，MI355X 288GB 对大模型推理/长上下文有吸引力；价格/性能更激进；开放生态利于 multi-vendor。 |
| AMD 劣势 | CUDA 生态、NVIDIA NVLink/NVSwitch、软件工具链和客户经验仍强于 ROCm；高端训练集群默认仍偏 NVIDIA。 |
| 是否主流 | 2026 可成为非 NVIDIA 的主力 merchant GPU，但更像“第二供应源 + 推理性价比方案”，不是默认唯一主流。 |
| 替代方案 | NVIDIA Blackwell、云厂 ASIC、低成本推理 ASIC、GPU 租赁/云服务替代自建。 |
| 切换成本 | 中高。客户需重测模型、kernel、通信库、监控和运维；但若使用 PyTorch/Triton/vLLM 等抽象层，切换成本低于 CUDA 原生深度绑定场景。 |

### 9.2 MI450/MI455X/Helios

| 维度 | 判断 |
|---|---|
| 主要竞争对手 | NVIDIA GB300 NVL72/Vera Rubin NVL72、Broadcom custom XPU + Ethernet fabric、Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA。 |
| AMD 优势 | OpenAI/Meta co-engineering 给出真实 workload feedback；Helios 是开放 rack-scale 架构，绑定 EPYC + Instinct + Pensando + ROCm；HBM4/31TB per rack 对推理和训练都重要。 |
| AMD 劣势 | NVLink/NVSwitch 的 scale-up 成熟度、NVIDIA 全栈软件和客户信任仍是壁垒；Helios/UALoE 初代量产验证风险高。 |
| 是否主流 | 若 OpenAI/Meta 首 GW 按期交付，Helios 会成为 2027 非 NVIDIA rack-scale 主流之一；若延迟，则仍是高潜力第二平台。 |
| 替代方案 | NVIDIA Rubin/GB300、Broadcom/OpenAI/Meta ASIC、云厂内部 TPU/Trainium/MTIA、租赁 NVIDIA 集群。 |
| 切换成本 | 高。GW 级 rack 涉及电力、液冷、网络、模型优化、运维和长期供应协议；一旦进入客户机房，替换不是换 GPU 卡，而是改整套 AI factory。 |

### 9.3 EPYC server CPU

| 维度 | 判断 |
|---|---|
| 主要竞争对手 | Intel Xeon、Arm Neoverse/Grace CPU、AWS Graviton、自研 Arm。 |
| AMD 优势 | EPYC 在核心数、能效、TCO 和 cloud share 上持续领先；AI rack 需要 x86 host/control，AMD 可与 Instinct 打包。 |
| 风险 | Arm 自研在 hyperscaler 内部渗透；Intel 若在先进节点和定价上反击，会压缩 EPYC share gain。 |
| 切换成本 | 中。服务器平台认证、BIOS/firmware、虚拟化、云实例生态有迁移成本，但低于 AI GPU 软件栈。 |

### 9.4 Pensando/Vulcano/AI networking

| 维度 | 判断 |
|---|---|
| 主要竞争对手 | NVIDIA ConnectX/BlueField/Spectrum-X、Broadcom Thor/Tomahawk、Marvell、Intel IPU、AWS Nitro/EFA、Google IPU。 |
| AMD 优势 | 与 EPYC/Instinct/Helios 同架构绑定；开放 Ethernet/UALoE 方向顺应 hyperscaler vendor diversity。 |
| 风险 | Broadcom/NVIDIA 在交换芯片、NIC、软件和客户认证上更强；AMD 的独立网络份额仍小。 |
| 切换成本 | 高。AI fabric 的 congestion control、telemetry、RDMA、security、firmware、Kubernetes/CNI 和故障处理都要重新验证。 |

### 9.5 ROCm/software

| 维度 | 判断 |
|---|---|
| 主要竞争对手 | NVIDIA CUDA/cuDNN/TensorRT/NCCL/Triton、Google TPU software stack、AWS Neuron、OpenAI/Meta 内部框架。 |
| AMD 优势 | 开源和供应多元化符合大客户诉求；Silo AI/Nod.ai 增强客户工程；推理场景较训练更容易优化迁移。 |
| 风险 | 生态惯性巨大；客户不愿为省 GPU ASP 承担上线延迟。 |
| 切换成本 | 最高之一。软件、模型、kernel、监控、debug、性能归因和工程人才都绑定。 |

## 10. 需要持续跟踪的监控指标

| 优先级 | 指标 | 为什么重要 |
|---:|---|---|
| 1 | Q3/Q4 2026 MI450/Helios revenue ramp 和 management 对 2027 Data Center AI revenue 的更新 | 验证 OpenAI/Meta 是否从订单叙事进入收入确认。 |
| 1 | HBM4 supply：Samsung/Micron/SK hynix 对 MI455X/Rubin/ASIC 的 qualification、yield、bit allocation | 决定 MI450/MI455X 真实出货上限。 |
| 1 | Helios rack certification：Celestica switch、UALoE interop、液冷、rack burn-in、现场上电 | 这是 AMD 从 GPU 卖方变成 rack 平台卖方的关键。 |
| 2 | EPYC Venice launch 和 server CPU revenue 是否维持 >70% YoY 附近 | CPU 是高毛利、相对低风险的第二增长腿。 |
| 2 | ROCm 在 vLLM、Triton、PyTorch、Megatron/DeepSpeed、K8s 生态的 benchmark 和客户案例 | 决定 AMD GPU 能否从“便宜替代”变成“可规模化默认选项”。 |
| 2 | Purchase commitments、inventory、prepayment 和 gross margin 变化 | 判断 AMD 是否为 AI 过度锁供应。 |
| 3 | Gaming/Client 2026H2 内存成本压力 | 会影响总公司 margin，但不是主线。 |
| 3 | 出口管制变化，尤其中国 AI GPU | Q2 2025 MI308 charge 说明监管冲击可以直接打毛利和库存。 |

## 资料来源

公开资料：

- AMD Q1 2026 earnings release: <https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results>
- AMD Q1 2026 10-Q: <https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000076/amd-20260328.htm>
- AMD Q4/FY2025 earnings release: <https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results>
- AMD FY2025 10-K/A: <https://www.sec.gov/Archives/edgar/data/2488/000000248826000021/amd-20251227.htm>
- AMD Q3 2025 earnings release: <https://ir.amd.com/news-events/press-releases/detail/1265/amd-reports-third-quarter-2025-financial-results>
- AMD Q2 2025 earnings release: <https://www.amd.com/en/newsroom/press-releases/2025-8-5-amd-reports-second-quarter-2025-financial-results.html>
- AMD Financial Analyst Day 2025: <https://ir.amd.com/news-events/press-releases/detail/1266/amd-unveils-strategy-to-lead-the-1-trillion-compute-market-and-accelerate-next-phase-of-growth>
- AMD Advancing AI 2025 / MI350 and Helios preview: <https://ir.amd.com/news-events/press-releases/detail/1255/amd-unveils-vision-for-an-open-ai-ecosystem-detailing-new-silicon-software-and-systems-at-advancing-ai-2025>
- AMD MI350 Series official page: <https://www.amd.com/en/products/accelerators/instinct/mi350.html>
- AMD MI355X official page: <https://www.amd.com/en/products/accelerators/instinct/mi350/mi355x.html>
- AMD OpenAI 6GW partnership: <https://ir.amd.com/news-events/press-releases/detail/1260/amd-and-openai-announce-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus>
- AMD Meta 6GW partnership: <https://ir.amd.com/news-events/press-releases/detail/1279/amd-and-meta-announce-expanded-strategic-partnership-to-deploy-6-gigawatts-of-amd-gpus>
- AMD/Celestica Helios collaboration: <https://www.amd.com/en/newsroom/press-releases/2026-3-16-amd-and-celestica-announce-collaboration-to-a.html>
- AMD/Samsung HBM4 collaboration: <https://www.amd.com/en/newsroom/press-releases/2026-3-18-samsung-and-amd-expand-strategic-collaboratio.html>
- AMD/Silo AI acquisition: <https://www.amd.com/en/newsroom/press-releases/2024-7-10-amd-to-acquire-silo-ai-to-expand-enterprise-ai-sol.html>
- AMD/ZT Systems divestiture to Sanmina: <https://ir.amd.com/news-events/press-releases/detail/1252/amd-announces-agreement-to-divest-zt-systems-data-center-infrastructure-manufacturing-business-to-sanmina>
- StockAnalysis AMD valuation/statistics page: <https://stockanalysis.com/stocks/amd/statistics/>

项目内行业底稿：

- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\行业调研\行业调研/AI头部芯片市场占比和规模.md`
- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\行业调研\行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- `D:\drive\Investment\工作台v5\行业调研_AI服务器_存储_芯片\行业调研_商用AI加速芯片_2026.md`
- `D:\drive\Investment\工作台v5\行业调研_AI服务器_存储_芯片\行业调研_HBM与高带宽内存_2026.md`
- `D:\drive\Investment\工作台v5\行业调研_AI服务器_存储_芯片\行业调研_AI芯片先进封装_2026.md`
- `D:\drive\Investment\工作台v5\行业调研_AI网络_光互联_铜互联\行业调研_网卡_DPU与SmartNIC_2026.md`

