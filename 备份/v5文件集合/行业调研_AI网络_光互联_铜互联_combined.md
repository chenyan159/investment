# 行业调研：【800G/1.6T可插拔光模块】

> 截至日期：2026-05-08（美西）  
> 研究口径：全球 AI 数据中心/AI Factory 使用的 800G、1.6T 可插拔光模块及其关键器件、相干 DCI 模块、LPO/LRO/FRO/TRO、硅光/InP/VCSEL、DSP/CDR/retimer、AEC/ACC/DAC 铜互联、CPO/CPX/NPO/XPO、OCS 与高速测试验证。  
> 计量口径：美元名义值。市场规模为行业收入池或订单池，不等同单家公司收入；3 个月口径按 2026Q2-Q3 可兑现订单/收入 run-rate，1 年为 2026H2-2027H1，2 年为 2026H2-2028H1。  
> 方法：外部资料优先使用公司公告、财报、发布会、会议资料；行业报告多方交叉验证。AI 芯片出货背景引用本项目既有 `ai_chip_research_2026_2027.md`，不重复外搜。

## 0. 一页结论

1. **2026 是 800G 高峰年，也是 1.6T 从验证转向规模交付的第一年。** TrendForce 2026-04-20 估计全球 AI 专用光收发模块市场从 2025 年 **165 亿美元**增至 2026 年 **260 亿美元**，同比 **57%+**；2026-02-10 又估计 800G 及以上模块出货占比从 2024 年 **19.5%**升至 2026 年 **60%+**。这意味着 AI 数据中心已经把 800G+ 变成标准件，而不是可选升级。
2. **1.6T 可插拔不会被 CPO 立刻替代。** 2026-2027 最可能的主线是 `800G OSFP/QSFP-DD 放量 + 1.6T OSFP/DR8/2xDR4 导入 + LPO/LRO/TRO/FRO 分场景渗透 + AEC/ACC 铜短距补位`。CPO/CPX/NPO 是 2027-2028 的高端交换芯片路线，2026 收入主要来自 ELS、optical engine、试点和预研。
3. **订单正在兑现。** AOI 2026-03-09 宣布获得长期 hyperscale 客户 **超过 2 亿美元**的 1.6T 数据中心收发器首个批量订单，并计划 2026 年底达到 **800G+1.6T 合计 50 万只/月**产能；2026-05-07 披露 Q1 已完成 800G 首批大客户批量出货，退出 Q1 时 800G 月产能近 **10 万只**。Lumentum FY26Q3 收入 **8.084 亿美元**，同比 **+90.1%**，组件收入同比 **+77.3%**，系统收入同比 **+121.1%**，200G EML 收入环比翻倍，1.6T 收发器 Q4 ramp on track。Coherent FY26Q3 数据中心与通信收入 **13.616 亿美元**，Q4 收入指引 **19.1-20.5 亿美元**、非 GAAP 毛利率 **39-41%**。Fabrinet FY26Q3 称 datacom 新客户协议将强化增长；Credo FY26Q3 收入 **4.07 亿美元**、同比 **+201.5%**、非 GAAP 毛利 **68.6%**，验证 AEC/retimer/高速连接硅的高利润弹性。
4. **利润池不只在模块组装。** 传统可插拔模块长期毛利会受 ASP 下行压制，领先模块厂早期毛利约 **30-45%**；更高、更可持续的毛利集中在 `EML/CW-LD/VCSEL/SiPh PIC/光引擎`、`DSP/SerDes/retimer/AEC 芯片`、`OCS/MEMS/ELS/CPO optical engine`、`高速 T&M`、`高端相干 DSP/模块`。Lumentum FY26Q3 非 GAAP 毛利 **47.9%**、Credo **68.6%** 是当前最直接的高毛利样本。
5. **2026 最可能的技术路径：1.6T 可插拔 + 硅光/EML 并行 + AEC/ACC 短距铜 + Google OCS 局部爆发。** 2027 最可能的二次斜率：1.6T 成为新增 AI fabric 默认配置，1600ZR/ZR+ 进入 AI scale-across，CPO/CPX/XPO 在高端 102.4T/204.8T switch 上形成批量项目，3.2T/400G-per-lane 进入小批量客户验证。
6. **乐观假设下，光互联是 AI 数据中心 CapEx 中最强 beta 之一。** 本项目美国 AI DC 建设模型给出网络与光互联 2026 订单池：务实 **650-1,000 亿美元**、乐观 **1,050-1,650 亿美元**；其中光模块 2026 务实订单 **280-450 亿美元**、2027 **450-780 亿美元**。这高于纯“AI 光模块 260 亿美元”的市场机构窄口径，因为订单池还包含交换机、铜互联、相干 DCI、OCS、CPO 相关链条和提前锁单。

## 1. 2026 AI 计算中心建设下的机遇与挑战

### 1.1 需求端：为什么 2026 会非常强

| 需求锚点 | 关键事实 | 对 800G/1.6T 的含义 |
|---|---:|---|
| CSP CapEx | TrendForce 2026-05-06 将全球九大 CSP 2026 CapEx 上调至 **约 8,300 亿美元**；Microsoft 在 FY26Q3 电话会上称 CY2026 CapEx 约 **1,900 亿美元**；Meta Q1 2026 指引 2026 CapEx **1,250-1,450 亿美元**；Alphabet Q1 2026 transcript 将 2026 CapEx 提至 **1,800-1,900 亿美元**。 | AI 网络不再是 GPU 附属件，而是新集群必买层。CapEx 越向高功率密度机架集中，光模块 attach rate 越高。 |
| AI 芯片主线 | 本项目 AI 芯片研究显示：2026 主力为 NVIDIA GB300/B300、AWS Trainium2/3、Google Ironwood、AMD MI350、Microsoft Maia200、Meta MTIA、OpenAI/Broadcom ASIC；Rubin/MI400/TPU8 在 2026H2-2027 接棒。 | 2026 新增集群以 800G scale-out 为底座，1.6T 在 Google/NVIDIA/Broadcom ASIC/AI Ethernet 中提前导入。 |
| Google OCS | TrendForce 称 Google Ironwood 结合 3D Torus + Apollo OCS，全光网络处理跨机柜传输；近 **400 万颗 TPU**将在 2026 带来 **600 万只以上 800G+ 光模块**需求。 | OCS 不是减少光模块，反而要求从设计阶段配置足量 800G/1.6T 模块。 |
| NVIDIA Rubin/Spectrum-X Photonics | NVIDIA 技术博客称 Spectrum-6 SPX 采用 **102.4Tb/s switch、512 lanes、200Gb/s CPO**；SN6800 类系统可达 **409.6Tb/s**，CPO 带来 5x power efficiency/更高 resiliency。 | 2026 CPO 是高端网络验证窗口，pluggable 仍是量最大收入池；2027 起高端 switch 开始分流一部分 1.6T/3.2T 价值。 |
| AI scale-across | Marvell 2026-03-05 发布 COLORZ 1600，1.6T ZR/ZR+ pluggable + 2nm coherent DSP，2026H2 采样。Ciena/Nokia/Coherent 同步推 multi-rail、1600ZR、coherent-lite。 | 大型 AI region 从单园区走向多园区，推动 800ZR/1600ZR/ZR+ 和线路系统增长。 |

### 1.2 主要挑战

1. **EML/CW-LD/SiPh PIC/DSP 供给比模块组装更紧。** TrendForce 明确把 EML、CW-LD、光学对准、高精度制程、功耗散热列为扩产瓶颈。
2. **ASP 下行会早于需求放缓。** 800G 已进入多供，2026H2-2027 可能出现价格竞争；1.6T 早期短缺但 2027 多家进入后毛利回归。
3. **客户认证周期长。** Hyperscaler 端口、交换芯片、光模块、线缆、散热、固件、监控软件需要共同验证；新形态 LPO/CPO/XPO 认证周期通常 **6-18 个月**。
4. **功耗/热密度约束。** 1.6T retimed 模块典型功耗可在 16-22W+，CPO/CPX/XPO 则把热管理从模块推向 switch package、ELS 和液冷系统。
5. **地缘与供应链重构。** 中美客户认证、关税、出口管制、产地要求推动东南亚/美国/墨西哥产能加速，但短期增加成本与良率风险。

## 2. AI 芯片技术路径与光互联拉动

### 2.1 2026-2027 初出货量最大的 AI 芯片平台与光互联含义

| 排名 | 芯片/平台（本项目既有信息） | 2026 阶段 | 对 800G/1.6T 的拉动 |
|---:|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | 2026 主力，GB300 NVL72 大规模交付 | rack 内 NVLink/铜为主，scale-out 用 800G/1.6T；2026 最确定拉动 800G 和部分 1.6T。 |
| 2 | AWS Trainium2 | Rainier 主力，近 50 万颗到 >100 万颗目标 | EFA/Ethernet scale-out 拉动 800G；2027 Trainium3 提高 1.6T attach rate。 |
| 3 | Google TPU v7 Ironwood | 2026 大规模部署 | OCS 架构使跨机柜全光化，单一生态对 800G+/1.6T 模块拉动最直接。 |
| 4 | NVIDIA B200/GB200 | 2026 延续放量 | 800G 为主，部分升级 1.6T；成熟设计带来确定性但 ASP 更快下行。 |
| 5 | Huawei Ascend 910C/950 | 中国国产替代主线 | 国产 400G/800G 先放量，1.6T 2026-2027 在国产超节点中导入。 |
| 6 | Cambricon MLU 590/690 | 国产 AI 加速放量 | 国产 OAM/以太网集群拉动本土 800G/1.6T 与高速 PCB/铜互联。 |
| 7 | AMD MI350X/MI355X | 2026 AMD 最确定产品 | PCIe/OAM/UBB 形态拉动 800G Ethernet；2027 MI400/UALink 推动 1.6T。 |
| 8 | AWS Trainium3 | 2026 GA/早期放量 | 144 芯片 UltraServer 和 Neuron Fabric 提高 rack 间光连接强度。 |
| 9 | Meta MTIA 300/400/450/500 | 2026-2027 迭代部署 | Broadcom Ethernet/SerDes 生态强，1.6T、CPO、AEC 都有潜在 attach。 |
| 10 | Microsoft Maia 200 | 2026 Azure 推理导入 | 750W SoC + 闭环液冷，Azure 后端网络拉动 800G/1.6T 和 DCI。 |
| 11 | OpenAI/Broadcom ASIC | 2026H2 起步，10GW 路线 | 若按 2027 前置订单，1.6T/3.2T、CPO、coherent DCI 都会超预期。 |
| 12 | AMD MI400/MI455X Helios | 2026H2 首批，2027 主力化 | UALink/以太网开放路线对 1.6T switch、AEC/ACC、CPO 形成新增生态。 |

### 2.2 技术成熟与放量节奏

| 技术路径 | 2026 基准 | 2026-2027 乐观 | 极度超预期乐观 |
|---|---|---|---|
| 800G 可插拔 OSFP/QSFP-DD | 2026 出货和收入主峰，AI 新集群标配；800G+ 出货占比 60%+ | 由于 GB300/TPU/Trainium 同时拉货，2026 全年价格降幅低于预期 | 800G 因电力/服务器延期被动延长生命周期，2027 仍高毛利出货 |
| 1.6T 可插拔 | 2026 >500 万只，主要为高端客户导入；2027 1,200-1,800 万只 | 2027 2,000-2,500 万只，新增 AI fabric 默认配置 | 2027 3,000 万只级别，短缺延续到 2028H1 |
| LPO/LRO/FRO/TRO | LRO/TRO/FRO 在 1.6T 逐步试用；LPO 依赖 host tuning | 2027 在部分 hyperscaler 成为低功耗主流之一 | DSP 功耗压力使 LPO/LRO 渗透率提前到 30%+ |
| 800ZR/1600ZR/ZR+ | 800ZR 放量，1.6T ZR/ZR+ 2026H2 采样 | AI scale-across 推动 coherent pluggable 年增 40%+ | 多园区训练/推理把 coherent-lite 拉进 DC 内长距互联 |
| OCS | Google/TPU 生态为主，外部供应链有限 | 2027 其他云厂和 AI ASIC 生态试点 | GPU Ethernet fabric 也吸收 OCS，光模块和 MEMS 需求大幅提前 |
| CPO/CPX/NPO/ELS | 2026 pilot 和 ELS/engine 收入；pluggable 仍主流 | 2027 多个高端 AI switch 项目批量导入 | 2027 CPO/CPX 成为高端 switch 默认路线之一 |
| XPO 12.8T 液冷可插拔 | 2026 MSA/样品/展示，收入很小 | 2027H2 高端 AI fabric 小批量 | 2027 形成 20 亿美元级需求，延长 pluggable 生命周期 |
| 3.2T/400G-per-lane | 2026 器件、DSP、PIC、测试验证 | 2027H2 小批量收入，2028 较大客户导入 | 204.8T switch 提前拉动，2027 形成 10-30 亿美元早期市场 |

### 2.3 2026 最可能的技术路径

2026 最可能兑现的是 **“800G 做量、1.6T 做斜率、铜互联做短距、OCS 做 Google 局部爆发、CPO 做高端试点”**：

- 大量收入：800G DR8/FR4/2xFR4/SR8、800G OSFP/QSFP-DD、800G AOC/DAC/AEC。
- 增量斜率：1.6T OSFP DR8/2xDR4/LRO/TRO/FRO，200G/lane，硅光 + InP EML 并行。
- 低功耗突破：LPO/LRO 和 3nm/5nm DSP 降功耗，host tuning 能力成为客户粘性。
- 架构变化：Google OCS、NVIDIA Spectrum-X Photonics、Arista XPO、Open CPX MSA 推动 2027 之后 CPO/CPX/XPO 分化。

## 3. 已开始放量的关键产品

### 3.1 市场规模、渗透率、增长与利润率

| 已放量产品 | 当前事实 | 未来 3 个月市场 | 未来 1 年市场 | 未来 2 年市场 | 渗透率路径 | 增长：基准/乐观/极度乐观 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|---|
| 800G AI 可插拔光模块 | 2026 AI 数据中心标配；800G+ 占比 60%+；Cignal 估 2026 800GbE >2,000 万只 | $4.5-7.0B | $18-28B | $25-42B | 2026 高端 AI 新建 55-70%；2027 60-75%，但新增份额被 1.6T 分流 | +45-65% / +70-90% / +100% | 模块 28-38% / 35-45% / 45%+；成熟后 2027 下行 |
| 1.6T 可插拔 OSFP/DR8/2xDR4 | Cignal 估 2026 >500 万只；AOI 获 >$200M 批量订单；Lumentum Q4 FY26 ramp | $1.5-3.5B | $12-28B | $28-60B | 2026 AI 新建 8-18%；2027 25-45%；2028 45-65% | +100-150% / +180-250% / +300%+ | 35-45% / 42-52% / 50%+；EML/SiPh/DSP 紧缺时高溢价 |
| 200G/lane 光器件：EML、CW-LD、VCSEL、SiPh PIC | Lumentum FY26Q3 200G EML 收入环比翻倍；Coherent 展示 200G EML/VCSEL/SiPh | $2.0-4.0B | $10-20B | $22-45B | 2026 1.6T 关键物料 attach 率 80%+ | +50-80% / +100% / +150%+ | 45-60% / 55-65% / 65%+；瓶颈强于模块 |
| DSP/CDR/retimer/optical DSP | Marvell Ara/Electra、Broadcom Taurus、Credo DSP/retimer；1.6T 和 AEC 同步拉动 | $1.5-3.0B | $8-16B | $18-36B | 2026 retimed 1.6T 占主流，LPO 逐步分流 | +40-70% / +80-120% / +150% | 55-70% / 65-75% / 75%+；IP/SerDes 更高 |
| 800G/1.6T ZR/ZR+ 相干 DCI 模块 | Cignal 2025 coherent module 近 $6B；Marvell 1.6T ZR/ZR+ 2026H2 采样 | $1.0-1.8B | $6-12B | $14-30B | 2026 AI scale-across 10-20%；2027 20-35%；2028 35-50% | +25-40% / +50-70% / +90% | 35-45% / 40-50% / 50%+；coherent DSP 稀缺 |
| DAC/AEC/ACC 铜互联 | Credo FY26Q3 收入 $407M、毛利 68.6%；Luxshare 展示 1.6T OSFP AEC/ACC | $2.0-4.0B | $10-20B | $18-38B | rack 内短距 2026 35-55%；2027 45-65%；2028 视 CPO/光化分流 | +35-55% / +70% / +100% | AEC 芯片/方案 55-70%；线缆/连接器 30-50%；短缺时更高 |
| 光模块 EMS/封测/主动对准 | Fabrinet、Foxconn/FIT、Jabil、Luxshare、东南亚产能受益 | $1.0-2.0B | $5-10B | $9-18B | 高速模块外包比例上升，东南亚占比提高 | +20-35% / +45% / +65% | EMS 10-15%；高端主动对准/测试可 15-25% |
| 高速测试验证 | VIAVI、Keysight、Anritsu、Teledyne、R&S 受益 224G/1.6T/3.2T | $0.3-0.8B | $1.5-3.5B | $3-8B | 2026 1.6T/224G 主线；2027 3.2T/448G 接棒 | +25-45% / +60% / +90% | 60-70% 硬件毛利，软件/服务更高 |

### 3.2 已放量产品的投资判断

- **800G：量仍很大，但投资弹性从“有没有产品”转向“谁还能维持毛利”。** 800G 的产品和客户认证已成熟，领先中国模块厂和北美器件厂都受益；2026H2 要重点跟踪 ASP、良率、客户结构和是否被 1.6T 挤压。
- **1.6T：2026 最强新增斜率。** 1.6T 不是一个单一赢家路线，SiPh、InP EML、VCSEL、DSP-retimed、LRO/TRO、LPO 会并行，客户按 reach、功耗、FEC、可维护性和供应安全做组合。
- **上游器件利润优于模块。** EML/CW-LD、SiPh PIC、optical engine、DSP/retimer 的短缺更难缓解，价格传导强于模块总装。
- **铜互联是被低估的第二条线。** AI rack 内短距、near-ASIC、top-side、CPC、AEC/ACC 会随 224G/448G 升级继续放量，不会被光一夜替代。

## 4. 在研与将快速增长的关键产品/技术

| 在研/导入技术 | 当前阶段 | 未来 3 个月市场 | 未来 1 年市场 | 未来 2 年市场 | 成熟/放量时间 | 渗透率路径 | 增长与毛利判断 |
|---|---|---:|---:|---:|---|---|---|
| 3.2T pluggable / 400G-per-lane | Broadcom Taurus、Coherent 400G/lane、OpenLight 3.2T DR8 PIC；2026 样品/评估 | <$0.2B | $0.5-3B | $8-25B | 2026H2 qual，2027 demo/小批量，2028 扩产 | 2026 <1%；2027 3-8%；2028 10-25% | 器件/DSP 毛利 60%+；模块早期受良率/测试压制 |
| CPO / CPX / NPO / ELS | NVIDIA/Broadcom/Coherent/Lumentum/Open CPX MSA 推进 | $0.2-0.6B | $1-4B | $5-18B | 2026 pilot，2027 高端 switch 小批量，2028 扩大 | 2026 <2% 高端端口；2027 5-12%；2028 10-25% | ELS/optical engine 45-65%；系统毛利受服务成本影响 |
| XPO 12.8T 液冷可插拔 | Arista XPO MSA；Molex/Eoptolink/Linktel 展示 | <$0.1B | $0.2-2B | $3-12B | 2026 标准/样品，2027H2 小批量，2028 放量 | 2027 高端 switch <5%；2028 5-15% | 早期高 ASP、高毛利，但液冷和可维护性吃利润 |
| OCS/MEMS 光交换 | Google Apollo 已体系化；Cignal 上修 OCS 预测 | $0.3-1.0B | $2-8B | $8-25B | 2026 Google 主导，2027 外部小规模，2029 前 GPU 广泛采用有限 | Google TPU 2026 高，GPU 2027 仍低 | MEMS/OCS 35-55%；若云厂自研，外部利润分散 |
| 448G copper/CPC/top-side/flyover | DesignCon 2026 密集 demo；Samtec/Luxshare/Molex/Amphenol/TE | $0.2-0.7B | $1-5B | $5-18B | 2026 pathfinding，2027 design-in，2028 更广 | 2026 <3%；2027 5-15%；2028 15-30% | 高端连接器/线缆 35-55%；CPC 认证后粘性高 |
| LPO/LRO/FRO/TRO | Lumentum、Coherent、中际旭创、新易盛、华工科技等推进 | $0.5-1.5B | $4-12B | $12-32B | 2026 1.6T 导入，2027 客户分化 | 2026 1.6T 中 10-20%；2027 20-35%；2028 30-45% | 低功耗价值高，但 host tuning 增加客户锁定；毛利 35-50% |
| 1600ZR/ZR+ / coherent-lite | Marvell 2026H2 采样；Nokia 2027H2 GA；Ciena/Coherent 同步 | $0.2-0.8B | $2-6B | $8-22B | 2026H2 sampling，2027 scale-across，2028 加速 | AI DCI 新建 2026 5-10%；2027 15-25%；2028 30%+ | coherent DSP/模块毛利 40-55%；系统商 35-45% |
| 外部激光源 ELS / 高功率 CW laser | Lumentum UHP/SHP lasers，Coherent high-power InP/CW | $0.1-0.5B | $1-3B | $4-12B | 2026 CPO/硅光预备，2027 高端项目 | CPO/SiPh engine attach 2027 抬升 | 高壁垒，毛利 50-70% |

## 5. 供给侧：产能结构、瓶颈、成本与毛利

### 5.1 产能结构

| 地区/公司 | 主要能力 | 产能/路径判断 |
|---|---|---|
| 中国大陆 | 中际旭创、华工科技/华工正源、新易盛、光迅科技、海信宽带、博创科技、剑桥科技、长飞、亨通、源杰科技、仕佳光子等 | 模块组装/封测/硅光/部分激光器快速扩张；北美客户认证和产地要求是主要变量。 |
| 台湾/东南亚 | Fabrinet（泰国）、Foxconn/FIT、Luxshare、Jabil、Sanmina、联钧光电、华星光通、环球晶/台积电硅光生态 | 美国客户供应链去风险核心承接地；主动对准、封测、EMS、AEC/ACC 产能受益。 |
| 美国 | Coherent、Lumentum、AOI、Broadcom、Marvell、Credo、Molex、Samtec、TE、Amphenol、Cisco/Acacia、Ciena | 关键器件、DSP/SerDes、CPO、相干、OCS、客户认证强；AOI 扩 Sugar Land，Lumentum Greensboro 先进光器件厂计划 2028 ramp。 |
| 日本/欧洲 | Sumitomo、Furukawa、Mitsubishi、Nokia/Infinera、Adtran/ADVA、HUBER+SUHNER、Senko、Fujitsu | 高端激光器、相干传输、连接器、线路系统和运营商级可靠性强。 |
| 以色列/新兴 | DustPhotonics/Credo、Ayar Labs、Teramount、OpenLight、Ranovus、POET、HyperLight、Lightmatter | 硅光 PIC、CPO/NPO、TFLN、optical I/O 等新技术储备，2027 以后价值更大。 |

### 5.2 供给瓶颈

1. **EML/CW-LD/VCSEL/PD 光电芯片。** 1.6T 需要 200G/lane，3.2T 需要 400G/lane；晶圆、外延、良率、封装都不是简单扩线。
2. **DSP/SerDes/retimer 高端节点。** 3nm/5nm optical DSP 和 224G/448G SerDes 依赖先进节点与高端封装，交期和成本受半导体周期影响。
3. **主动对准与封装测试。** 光学耦合、FAU、透镜、滤波器、隔离器、热稳定和老化测试是模块有效产能关键。
4. **客户认证和现场可靠性。** Hyperscaler 一旦发生链路 flap、BER 超标、热漂移或批量 RMA，会冻结后续订单；认证壁垒强于设备投资。
5. **热设计和功耗。** 1.6T OSFP、XPO、CPO 都需要更强散热；液冷 switch 和光模块 form factor 会影响客户导入节奏。
6. **产地与关税/出口管制。** 北美客户可能要求美国、墨西哥、泰国、马来西亚或台湾产能，降低中国直接出货比例。
7. **人才与设备。** 光学工程、SI/PI、高速测试、封装工艺、自动化主动对准工程师都稀缺；高端 BERT/oscilloscope/VNA 也可能成为扩产瓶颈。

### 5.3 单位成本拆分与毛利决定因素

| 产品 | 典型成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 800G DSP/retimed 模块 | DSP/CDR 20-30%；光器件 25-35%；PCB/封装/连接器 10-15%；主动对准/测试 15-25%；散热/结构/良率 10-15% | 大客户份额、DSP 成本、良率、自动化测试时间、保修 | 2026H1 供需紧可传导，2026H2 多供后 ASP 下行 |
| 1.6T 模块 | DSP/retimer 25-35%；200G EML/SiPh/VCSEL/CW-LD 25-35%；封装/FAU/thermal 15-20%；测试/老化 15-25% | 200G 光器件、低功耗、客户认证、热稳定 | 早期按交期和良率溢价，2027 多供后价格开始分化 |
| LPO/LRO/TRO/FRO | DSP 成本下降或外移；host tuning/PHY 协同成本上升；光器件和测试仍高 | 是否绑定客户交换芯片/host；系统级调参能力 | 一旦进入客户架构，切换成本高，可保较好毛利 |
| AEC/ACC | retimer/redriver/MCU 30-50%；线缆连接器 25-35%；测试和组装 15-25% | 功耗、误码率、线径/长度、散热、firmware | 短距替代光模块时按节电/低延迟价值定价 |
| CPO/ELS/optical engine | 光引擎/PIC 25-40%；ELS/laser 20-35%；封装/连接器/热 20-30%；NRE/测试 10-25% | 可靠性、可维护性、laser redundancy、平台绑定 | 2026-2027 更像平台件，按系统节能/TCO 议价 |
| Coherent ZR/ZR+ | coherent DSP 25-40%；laser/modulator/receiver 25-35%；封装/测试 20-30% | DSP 领先、功耗、reach、MACsec、客户认证 | AI DCI 紧缺时价格坚挺，传统电信采购会压价 |

## 6. 竞争格局与壁垒

### 6.1 市场结构

| 层级 | 市场结构判断 | 头部集中度 |
|---|---|---|
| 800G/1.6T 模块 | 中际旭创、新易盛、Coherent、Lumentum/Cloud Light、Eoptolink、AOI、华工科技、Fabrinet 生态强 | AI 高速模块 CR5 约 55-70%，单一客户内集中度可更高 |
| EML/CW laser/光器件 | Lumentum、Coherent、Sumitomo、Mitsubishi、Furukawa、AOI、源杰科技等 | 高端 200G EML/CW-LD CR5 可达 60%+，瓶颈期更集中 |
| DSP/SerDes/retimer | Broadcom、Marvell、Credo、MACOM、Semtech、Astera、Synopsys/Cadence IP | 高端 DSP/SerDes CR3 很高，设计周期形成锁定 |
| AEC/ACC | Credo、Luxshare、Amphenol、TE、Molex、Samtec、FIT、BizLink | 系统方案和芯片集中，线缆/连接器较分散 |
| CPO/CPX/XPO/OCS | NVIDIA/Broadcom/Coherent/Lumentum/Marvell/Arista/Molex/Samtec/Open CPX 生态 | 早期由平台公司主导，外部供应商看认证卡位 |
| Coherent DCI | Ciena、Nokia/Infinera、Cisco/Acacia、Marvell、Coherent、Lumentum | 高端 coherent DSP 和系统集中度高 |

### 6.2 壁垒清单：为什么能定价

| 壁垒 | 为什么能定价 | 可量化指标 |
|---|---|---|
| 速率与功耗 | 1.6T/3.2T 每 lane 信号完整性、DSP 功耗和热设计决定客户 TCO | W/bit、BER、FEC latency、TDECQ、link flap-free uptime |
| 光学工艺 | EML/SiPh/PIC/FAU 主动对准良率决定有效产能 | coupling loss、良率、老化时间、RMA ppm |
| 客户认证 | 重新认证会影响数十亿美元集群上电 | 认证周期 6-18 个月；客户 SKU 数；10%+ 客户数量 |
| 供应安全 | Hyperscaler 会用长约锁关键物料，交期本身就是价值 | LTA 年限、预付款、capacity reservation |
| 系统协同 | LPO/CPO/OCS/AEC 需要 host、switch ASIC、固件、监控软件协同 | 客户平台 design win、firmware attach、诊断软件 |
| 规模制造 | 高速模块不是“能做样品”而是“能稳定月产几十万只” | 月产能、良率、自动化率、测试设备数量 |
| 现场可靠性 | 单个模块价格低于 GPU，但故障可拖垮整柜/整 pod | RMA、链路 flap、MTBF、客户 SLA 罚则 |

### 6.3 长期高 ROIC/高毛利层

长期最可能拥有高 ROIC/高毛利的是五层：

1. **高端光器件和光引擎：** 200G/400G EML、CW-LD、SiPh PIC、ELS、VCSEL array。原因是扩产慢、良率难、客户认证强。
2. **DSP/SerDes/retimer/AEC 芯片：** 先进节点、IP 积累和系统 firmware 绑定强，毛利可达 60-80%。
3. **CPO/OCS 平台件：** 一旦进入架构层，按节能、密度和可靠性定价，而不是按单模块 BOM 定价。
4. **高速测试验证：** 每一代 lane-rate 翻倍都会先买仪器，且软件/服务毛利高。
5. **高端相干 DCI：** AI scale-across 对低功耗、大容量、MACsec、线路系统协同要求高，传统电信竞争少一些。

纯模块组装短期弹性大，但长期可能被 ASP 和多供压缩；能同时拥有器件、模块、客户认证和产能的垂直一体化厂商更能保毛利。

## 7. 2026 关键变化：三个拐点

### 拐点 1：1.6T 从样品进入批量订单

AOI 的 1.6T 批量订单和 50 万只/月目标，Lumentum 1.6T Q4 FY26 ramp，Coherent/OFC 2026 多技术 1.6T 展示，共同说明 1.6T 已不是 2027 远期故事。2026 最可能放量子方向：

- 1.6T OSFP DR8/2xDR4；
- 200G EML/CW-LD/SiPh PIC；
- 1.6T retimed/LRO/TRO/FRO；
- 1.6T 测试、老化和主动对准设备。

### 拐点 2：Google OCS 把“光交换”从可选节能方案变成架构变量

TrendForce 称 OCS 单机约 100W、传统交换约 3,000W，功耗降低约 95%；Cignal AI 因 Google TPU 部署上修 OCS 市场，2026 addressable market 约为原估计 3 倍。2026 放量方向：

- MEMS OCS、OCS 优化光模块；
- 800G/1.6T 模块在 TPU/ASIC 集群中的提前配置；
- OCS 管理软件、光纤管理、测试。

### 拐点 3：铜互联从“被光替代”转为“短距升级”

DesignCon 2026 的 224G/448G、CPC、top-side、AEC/ACC 密集展示说明短距铜仍在升级。2026 放量方向：

- 1.6T OSFP AEC/ACC；
- 224G CPC/top-side connector；
- PCIe 6/7 retimer、CXL/UALink 相关连接；
- AI rack 内短距、低延迟、低功耗互联。

## 8. 2027 关键变化：三个拐点

### 拐点 1：1.6T 成为新增 AI fabric 默认配置

若 GB300/Rubin、Trainium3、TPU8、MI400、MTIA/OpenAI ASIC 同步上量，2027 新增 AI 集群会大比例从 800G 转向 1.6T。预计 2027 1.6T 出货基准 **1,200-1,800 万只**，乐观 **2,000-2,500 万只**，极度乐观 **3,000 万只级别**。

### 拐点 2：CPO/CPX/XPO 从展示进入高端 switch 小批量

NVIDIA Spectrum-X Photonics、Broadcom CPO、Open CPX MSA、Arista XPO 会在 2027 给出第一批可比较的客户数据。放量方向：

- 102.4T/204.8T switch；
- ELS、optical engine、fiber connector、liquid-cooled pluggable；
- 可维护 socketed CPO/CPX，而非全封闭 CPO。

### 拐点 3：AI scale-across 拉动 1600ZR/ZR+ 和线路系统

多园区 AI 训练/推理、区域 DCI、128+ fiber-pair/rack 级需求，会让 coherent DCI 从电信周期转成 AI capex 周期。放量方向：

- 800ZR/1600ZR/ZR+；
- coherent-lite；
- multi-rail ILA、full spectrum transponder、hyper-rail；
- Marvell/Ciena/Nokia/Coherent/Lumentum 相关 DSP、泵浦激光、线路系统。

## 9. 头部公司与细分产业链全景

| 细分环节 | 头部/优势公司 |
|---|---|
| 800G/1.6T 可插拔模块 | 中际旭创 Innolight、新易盛 Eoptolink、Coherent、Lumentum/Cloud Light、AOI、Fabrinet、华工科技/华工正源、光迅科技 Accelink、海信宽带、Source Photonics、Broadex、Cisco/Acacia、Nokia/Infinera、Ciena、Hisense Broadband、HG Genuine、Gigalight、Linktel |
| 硅光/PIC/光引擎 | Coherent、Intel、Broadcom、Marvell/Inphi、Cisco/Acacia、OpenLight、DustPhotonics/Credo、Ayar Labs、Ranovus、POET、HyperLight、Lightmatter、TSMC、GlobalFoundries、Tower、imec、Sicoya、源杰科技、仕佳光子 |
| EML/CW-LD/VCSEL/PD | Lumentum、Coherent、Sumitomo Electric、Mitsubishi Electric、Furukawa、AOI、Broadcom、MACOM、II-VI/Coherent、Finisar/Coherent、联钧光电、华星光通、源杰科技、索尔思、住友大阪水泥 |
| DSP/CDR/SerDes/retimer | Broadcom、Marvell、Credo、MACOM、Semtech、Astera Labs、Synopsys、Cadence、Alphawave Semi、MaxLinear、Microchip、Rambus |
| AEC/ACC/DAC/高速铜 | Credo、Luxshare、Amphenol、TE Connectivity、Molex、Samtec、FIT/Foxconn、BizLink、Hirose、Bel Fuse、3M、Gore、Semtech、MACOM、Broadcom |
| CPO/CPX/NPO/ELS/XPO | NVIDIA、Broadcom、Coherent、Lumentum、Marvell、Arista、Molex、Samtec、TE、Amphenol、Senko、Corning、Ayar Labs、Ranovus、OpenLight、DustPhotonics、TeraHop、Eoptolink、Linktel |
| OCS/MEMS 光交换 | Google/Apollo、Lumentum、Coherent、Molex、Calient、Telescent、HUBER+SUHNER Polatis、DiCon、iPronics、Drut、Triple-Stone、Senko、Corning |
| Coherent DCI/线路系统 | Ciena、Nokia/Infinera、Cisco/Acacia、Marvell、Coherent、Lumentum、Juniper、Adtran/ADVA、Fujitsu、NEC、PacketLight、Infinera/Nokia |
| 高速连接器/光纤管理 | Amphenol、TE、Molex、Samtec、Senko、Corning、HUBER+SUHNER、Rosenberger、Hirose、Luxshare、BizLink、FIT |
| 测试验证 | Keysight、VIAVI、Anritsu、Tektronix、Teledyne LeCroy、Rohde & Schwarz、MultiLane、EXFO、Spirent、Advantest、Teradyne、FormFactor |
| EMS/封测/制造 | Fabrinet、Foxconn/FIT、Jabil、Sanmina、Flex、Celestica、Luxshare、Coherent 自有、AOI 自有、华工/中际/新易盛自有 |
| AI 网络交换/系统 | NVIDIA Networking、Broadcom、Arista、Cisco、Marvell、HPE/Juniper、Dell、Celestica、Accton、Wiwynn、Quanta、Wistron、Inventec |

## 10. 三情景市场模型

### 10.1 光模块与互联收入池

| 收入池 | 2026 基准 | 2026 乐观 | 2026 极度乐观 | 2027 基准 | 2027 乐观 | 2027 极度乐观 |
|---|---:|---:|---:|---:|---:|---:|
| AI 高速光收发模块（窄口径） | $25-27B | $28-33B | $33-40B | $38-50B | $50-70B | $70-95B |
| 800G 可插拔 | $16-22B | $20-26B | $25-32B | $18-28B | $25-36B | $35-48B |
| 1.6T 可插拔 | $7-10B | $10-15B | $15-22B | $18-32B | $32-50B | $50-75B |
| 相干 DCI/scale-across | $6-9B | $8-12B | $12-16B | $10-18B | $18-28B | $28-42B |
| AEC/ACC/DAC 铜互联 | $8-15B | $12-20B | $18-28B | $12-22B | $22-35B | $35-55B |
| CPO/CPX/XPO/OCS/ELS | $2-5B | $5-10B | $10-18B | $8-20B | $20-45B | $45-80B |
| 高速 T&M | $1.5-3B | $3-5B | $5-8B | $3-6B | $6-10B | $10-16B |

### 10.2 渗透率路径

| 技术 | 2026 基准 | 2027 基准 | 2028 基准 | 乐观/极度乐观偏差 |
|---|---:|---:|---:|---|
| 800G+ 在 AI 光模块出货中占比 | 60-65% | 70-80% | 75-85% | 乐观下 2026 即 70%+ |
| 1.6T 在 AI 高速模块收入中占比 | 25-35% | 40-55% | 50-65% | 极度乐观 2027 可到 60%+ |
| LPO/LRO/TRO/FRO 在 1.6T 中占比 | 10-20% | 20-35% | 30-45% | 客户 host tuning 顺利则提前 |
| OCS 在非 Google GPU 集群中占比 | <2% | 3-8% | 8-15% | Google 内部远高于行业平均 |
| CPO/CPX/XPO 在高端 switch optical ports 中占比 | <3% | 5-12% | 12-25% | 若 pluggable 功耗瓶颈加剧，2027 可翻倍 |
| AEC/ACC 在 rack 内短距高速连接中占比 | 35-55% | 45-65% | 45-70% | 受 CPO 和光化分流，但短距仍强 |

## 11. 风险与跟踪指标

### 11.1 风险

- AI CapEx 增速放缓或融资环境恶化，导致光模块订单延后。
- 800G/1.6T 多供加速，ASP 下行快于出货增长。
- 1.6T LPO/LRO/CPO 可靠性或可维护性验证失败，客户延后导入。
- 电力、液冷、土地、并网瓶颈使服务器上电慢于光模块备货。
- 中国供应链被关税、出口管制或客户产地要求限制份额。
- 3.2T/CPO/XPO 过早资本化，实际收入落在 2028 以后。

### 11.2 未来 6-12 个月要盯的高频指标

1. AOI 800G/1.6T 月产能是否从 10 万只/月爬到 50 万只/月。
2. Lumentum 1.6T Q4 FY26 ramp、200G EML、UHP/CPO laser 出货和毛利率。
3. Coherent FY26Q4 数据中心与通信收入、1.6T/3.2T/XPO 客户导入。
4. 中际旭创、新易盛、华工科技 1.6T 收入占比和硅光/LPO 占比。
5. Google Ironwood/OCS 实际 TPU 部署、光模块订单供应商份额。
6. NVIDIA Spectrum-X Photonics / Quantum-X Photonics 商用出货节奏。
7. Arista XPO MSA 是否进入客户验证，1.6T switching 是否按 2027 production 节奏。
8. Credo AEC 增速、毛利率和 DustPhotonics 整合进展。
9. 800G/1.6T ASP 降幅、模块厂库存和客户取消/延期迹象。
10. 高速测试设备订单是否从 1.6T 转向 3.2T/448G。

## 12. 资料来源

### 公司一手资料

- NVIDIA: [Vera Rubin POD: Seven Chips, Five Rack-Scale Systems, One AI Supercomputer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- NVIDIA: [Inside the NVIDIA Vera Rubin Platform](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)
- NVIDIA: [Scaling Power-Efficient AI Factories with Spectrum-X Ethernet Photonics](https://developer.nvidia.com/blog/scaling-power-efficient-ai-factories-with-nvidia-spectrum-x-ethernet-photonics/)
- NVIDIA: [FY2026 Q4 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)
- Coherent: [OFC 2026 next-generation pluggable transceiver demonstrations](https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026)
- Coherent: [Scale-across multi-rail transport platform](https://www.coherent.com/news/press-releases/scale-across-networks-multi-rail-transport-platform)
- Coherent: [FY2026 Q3 results](https://www.globenewswire.com/news-release/2026/05/06/3289361/11543/en/coherent-corp-reports-third-quarter-fiscal-2026-results.html)
- Lumentum: [OFC 2026 AI infrastructure products](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx)
- Lumentum: [FY2026 Q3 results](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx)
- Marvell: [COLORZ 1600 1.6T ZR/ZR+ and 2nm coherent DSP](https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html)
- Broadcom: [OFC 2026 AI infrastructure optical solutions](https://investors.broadcom.com/node/64036/pdf)
- Arista: [Q1 2026 financial results](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-First-Quarter-2026-Financial-Results/)
- Arista: [XPO high-density liquid-cooled pluggable optics](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Announces-XPO-High-Density-Liquid-Cooled-Pluggable-Optics/default.aspx)
- AOI: [1.6T volume order from major hyperscale customer](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers)
- AOI: [Q1 2026 results](https://www.globenewswire.com/news-release/2026/05/07/3290613/9986/en/applied-optoelectronics-reports-first-quarter-2026-results.html)
- Fabrinet: [FY2026 Q3 results](https://investor.fabrinet.com/news-releases/news-release-details/fabrinet-announces-third-quarter-fiscal-year-2026-financial)
- Credo: [FY2026 Q3 results, SEC exhibit](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm)
- Credo: [DustPhotonics acquisition](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Agrees-to-Acquire-DustPhotonics-Accelerating-Expansion-into-Silicon-Photonics-and-Next-Generation-Optical-Connectivity/default.aspx)
- Luxshare-Tech: [DesignCon 2026 224G/448G and 1.6T AEC/ACC](https://en.luxshare-tech.com/company/resources/news/designcon-2026-unveiling-224g-448g.html)
- Molex: [OFC 2026 OCS and XPO roadmap](https://www.molex.com/en-us/news/molex-accelerates-ai-cluster-deployment-with-one-stop-optical-interconnect-architecture-and-debut-of-high-radix-optical-circuit-switch-platform)
- TE Connectivity: [DesignCon 2026](https://www.te.com/en/about-te/events/designcon-2026.html)
- Google Cloud: [Inside the Ironwood TPU codesigned AI stack](https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack/)
- Microsoft: [FY2026 Q3 earnings call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3)
- Meta: [Q1 2026 results](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/default.aspx)
- Alphabet: [Q1 2026 earnings transcript](https://s206.q4cdn.com/479360582/files/doc_events/2026/Apr/29/2026_Q1_Earnings_Transcript.pdf)

### 行业报告与会议资料

- TrendForce: [2026 AI optical transceiver market to reach $26B](https://www.trendforce.cn/presscenter/news/20260420-13018.html)
- TrendForce: [Google high-speed interconnect pushes 800G+ share past 60%](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- TrendForce / PRNewswire: [Top nine CSP 2026 CapEx to $830B](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html)
- Cignal AI: [Optical component revenue nearly $25B in 2025](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)
- Cignal AI: [Google AI buildout drives higher OCS forecast](https://cignal.ai/2026/02/googles-ai-buildout-drives-higher-optical-circuit-switching-forecast/)
- LightCounting: [Optical transceiver sales reached $23.8B in 2025](https://www.lightcounting.com/newsletter/en/march-2026-quarterly-market-update-380)
- 650 Group / IBTA: [RDMA networking and AI white paper](https://650group.com/wp-content/uploads/2024/06/650-Group-IBTA-RDMA-White-Paper-June-2024.pdf)
- OFC: [OFC 2026 official news](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-opens-next-week-in-los-angeles-with-sold-out-exhibition-as-ai-driven-network-demand-fuels/)
- Open CPX MSA: [Open CPX MSA](https://www.opencpxmsa.org/)
- OCP: [Optical Circuit Switching for AI and Data Centers, April 2026 white paper](https://www.opencompute.org/documents/ocp-ocs-white-paper-april-2026-final-pdf)

### 本地项目资料

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- `D:\drive\Investment\调研\v5\conference_update\ofc_2026_conference_update.md`
- `D:\drive\Investment\调研\v5\conference_update\designcon_2026_conference_update.md`

---

非投资建议。本文数字为产业研究和情景建模用途，尤其是自用 ASIC、OCS、CPO、XPO、3.2T 等细分市场，公开口径有限，已用公司公告、行业报告、订单/产能新闻和本项目 AI 芯片模型交叉校验；极度乐观情景隐含 AI 推理需求、融资、上电、HBM/CoWoS/光器件/液冷均顺利扩张。
# 行业调研：【AEC、DAC与高速铜缆】

> 截至日期：2026-05-08  
> 研究范围：AEC（Active Electrical Cable）、DAC（Direct Attach Copper）、ACC（Active Copper Cable）、高速 twinax/OSFP/QSFP-DD/OSFP-XD 铜缆、CPC/top-side/flyover copper、PCIe/CXL/以太网 retimer/redriver/DSP、相关连接器与线缆制造。  
> 基调：按要求对 2026-2027 AI 计算中心建设保持大胆乐观。直接数据缺失处采用“GB300/Blackwell Ultra、Rubin、Google TPU、AWS Trainium、Meta/OpenAI/Broadcom ASIC 同步拉动，rack 内短距铜和 rack 间光互联分层共存”的偏乐观假设。本文不是投资建议。

## 0. 高浓度结论

2026 年 AEC、DAC 与高速铜缆的核心判断是：**铜不会被光简单替代，铜的价值从“低价被动线缆”升级为“AI rack 内物理层系统件”。** 1.6T/224G、PCIe 6/7、CXL、UALink、NVLink 机柜化把 PCB 走线、连接器、retimer、redriver、DSP、线缆 skew、热设计和客户认证全部推到系统架构层。长距和跨 rack 会更光化，短距、低延迟、可维护、低功耗的 rack 内连接会更依赖高级铜。

最强一手信号：

- NVIDIA GB300 NVL72 是 72 颗 Blackwell Ultra GPU + 36 颗 Grace CPU 的液冷 rack，官方页面给出 130 TB/s NVLink、37 TB fast memory、每 GPU 800 Gb/s 网络连接；NVIDIA 2026 年 3 月 GB300 NVL72 参考架构还披露单 rack 最高 142 kW、每 GPU 18 条 NVLink 通过 copper backplane 连接 9 个 NVSwitch tray。[NVIDIA GB300](https://www.nvidia.com/en-us/data-center/gb300-nvl72/), [NVIDIA GB300 RA PDF](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory-with-gb300-nvl72-dual-plane-networking-architecture.pdf)
- NVIDIA Vera Rubin 平台在 GTC 2026 宣布七类芯片 full production，2026H2 伙伴可用；Vera Rubin NVL72、Vera CPU rack、Groq LPX、BlueField-4 STX、Spectrum-6 SPX 共同把 AI factory 变成多 rack、pod 级系统。技术博客明确提到 MGX ETL 采用预集成、预验证 copper cable cartridges，Spectrum-X Ethernet spine 后部接 copper spine，前部 32 个 OSFP cage 接光模块。[NVIDIA Vera Rubin](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx), [Vera Rubin POD 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- TrendForce 2026 年 5 月把全球前九大 CSP 2026 CapEx 上修到约 8,300 亿美元，同比增速从 61% 上修到 79%，并预计全球数据中心装机功率约 155 GW，同比 +29%。这给网络、线缆、连接器和 retimer 的需求提供了极乐观上限。[TrendForce/PRNewswire](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html)
- TrendForce 2026 年 2 月称 800G 及以上光模块出货占比将从 2024 年 19.5% 升至 2026 年 60%+，同时指出 Google Ironwood TPU 架构中“短距用高速铜，rack 间用全光网络”，Google 2026 年约 400 万 TPU 对应 800G+ 光模块需求超过 600 万只。[TrendForce 800G+](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- Molex AEC 官方页面给出 AEC 在 112G 下最高 7m、224G 下 2.5m+，支持 1.6T、26-34 AWG、小线径、pre-FEC BER 低于 1E-12，并列出 Broadcom、Marvell、Point2、Astera 等 retimer/DSP 方案。[Molex AEC](https://www.molex.com/en-us/products/connectors/high-speed-pluggable-io/active-electrical-cables-aec)
- Luxshare-Tech 在 DesignCon 2026 展示 1.6T OSFP AEC/ACC，其中 1.6T OSFP AEC 可在 27AWG 4m、30AWG 3m 稳定工作，并展示 224G/448G CPC 与 448G KOOLIO CPC-to-OSFP Airchannel。[Luxshare DesignCon 2026](https://en.luxshare-tech.com/company/resources/news/designcon-2026-unveiling-224g-448g.html)
- Broadcom OFC 2026 展示 200G/lane retimer 与 AEC，称 extended AEC 可达 6m，同时展示 PCIe Gen6 switch/retimer 和 3.2T VCSEL NPO。[Broadcom OFC 2026](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai)
- Credo 2026 财年 Q3 收入 4.07 亿美元，环比 +50% 以上、同比 +200%，GAAP/Non-GAAP 毛利率约 68.5%/68.6%，显示 AEC/高速连接 silicon 已经出现接近 AI 半导体的软件型毛利。[Credo Q3 FY26/SEC](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm)
- Astera Labs 2026 Q1 收入 3.084 亿美元，同比 +93%；Scorpio X-Series 320-lane AI Fabric switch 已 shipping，Q2 2026 指引 3.55-3.65 亿美元，说明 PCIe 6 fabric/retimer/SCM 已进入收入确认窗口。[Astera Scorpio](https://www.asteralabs.com/news/astera-labs-extends-leadership-in-open-ai-scale-up-networking-with-new-320-lane-scorpio-x-series-smart-fabric-switch/)

**一句投资判断：** 2026 最确定的是 800G AEC/DAC、1.6T OSFP AEC/ACC 初放量、PCIe 6/CXL AEC/Smart Cable Module、224G CPC/top-side/flyover copper；2027 的弹性来自 448G short-reach copper、OSFP-XD/3.2T、PCIe 7/UALink、hybrid AEC/ACC，以及 CPO 之前的“最后一代高价值铜”。

## 1. 2026 AI 计算中心机遇、挑战与技术路径

### 1.1 行业机会

1. **AI rack 内连接数量和带宽密度上升。** GB300 NVL72 每 rack 72 GPU、9 个 NVSwitch tray、每 GPU 18 条 NVLink copper backplane，rack 内铜链路数量从“服务器内部”扩展到“整柜系统”。Rubin/Kyber 会继续放大这个趋势。
2. **224G/1.6T 提前商业化。** 过去 112G PAM4 对应 800G 是主流，2026 年开始 224G PAM4 对应 1.6T。被动 DAC 在 224G 下 reach 大幅缩短，AEC/ACC 的 attach rate 上升。
3. **PCIe/CXL 从板级连接外溢到 cable/fabric。** PCIe 6 64GT/s PAM4、CXL 3.x、GPU/XPU 到 NIC/SSD/内存扩展需要 retimer 和 smart cable。Astera Aries/Scorpio、Marvell Alaska P、Broadcom PCIe Gen6 是代表。
4. **光模块短缺反而强化短距铜。** TrendForce 预计 2026 AI 光模块市场从 2025 年 165 亿美元增至 260 亿美元，同比 +57% 以上，但 EML/CW-LD、光学对准、散热、DSP 仍紧张。在 0.5-7m 场景，AEC/ACC 比 AOC/光模块有功耗、成本、时延和维护优势。
5. **客户从“买线”变成“买系统可靠性”。** AI 训练和推理集群的 downtime 成本很高，客户愿意为 BER、telemetry、fleet diagnostics、firmware、热插拔、认证过的 cable cartridge 付溢价。

### 1.2 主要挑战

| 挑战 | 2026 影响 | 投资含义 |
|---|---|---|
| 224G/448G 信号完整性 | 插损、回损、串扰、skew、抖动、FEC latency 和 BER 都快速恶化 | 连接器、twinax、retimer、T&M 议价力上升 |
| AEC 功耗和散热 | Retimer/DSP 放在 cable end，1.6T 下热密度高 | 低功耗 DSP、散热 housing、线缆风道设计是壁垒 |
| 客户认证周期 | Hyperscaler/OEM qualification 往往 6-12 个月，换线会影响整 rack 可靠性 | 先入 design-in 的供应商有锁定价值 |
| 光与铜分层不确定 | CPO/OCS/LPO 会压缩部分电连接价值，但 2026-2027 不会一夜替代 | 不押单一路线，押“短距铜 + 长距光”的分层 |
| 产能与测试时间 | 224G/448G 需要高端 BERT/VNA/oscilloscope、自动化 burn-in | T&M、自动化测试、SPC、量产工程能力形成瓶颈 |
| 贸易与地域 | 美国客户希望东南亚/墨西哥/美国本土二供，传统线缆产能集中在中国和东亚 | 具备全球制造和认证复制能力的厂商更值钱 |

### 1.3 2026-2027 出货量最大 AI 芯片背景下的铜互连推演

项目内 AI 芯片底稿显示，2026-2027 最大出货/价值权重平台包括 NVIDIA B300/GB300、AWS Trainium2/3、Google TPU v7/v8、NVIDIA B200/GB200、AMD MI350/MI400、Meta/OpenAI/Broadcom ASIC、Microsoft Maia 200、中国 Ascend/Cambricon/Alibaba/Baidu 等。对应高速铜路径如下：

| 芯片/平台 | 2026 铜互连需求 | 2027 变化 |
|---|---|---|
| NVIDIA GB300/B300 | NVLink rack 内 copper backplane、ConnectX-8/800G scale-out、OSFP/QSFP 管理与存储网络、液冷环境 cable cartridge | Rubin/Rubin Ultra 把 copper spine、direct chip-to-chip spine 与 rack-to-rack optics 同时系统化 |
| Google TPU v7 Ironwood / TPU8 | 短距高速铜 + Apollo OCS/800G+ 光模块；Google 2026 TPU 量级拉动大量短距 copper + rack 间光 | TPU8 训练/推理分化，1.6T/OCS 扩展，短距铜继续做 rack/pod 内低时延连接 |
| AWS Trainium2/3 | NeuronLink/Neuron Fabric、EFA/NIC、rack 内高密度铜、PCIe/CXL retimer | Trainium3 144-chip UltraServer 放大 active cable 和 fabric switch 需求 |
| AMD MI350/MI400 Helios | MI350 企业 PCIe/UBB 形态用 Gen5/6 retimer，MI400/Helios open rack 用 UALink/以太网和 1.6T NIC | 2027 若 Meta up to 6GW 节奏兑现，开放 scale-up fabric 会推高 merchant AEC/retimer 需求 |
| Meta/OpenAI/Broadcom ASIC | Broadcom SerDes/Ethernet 强，定制 XPU rack 需要 224G/1.6T copper/retimer 和白盒交换生态 | 多 GW ASIC 会强化非 NVIDIA 路线的 AEC/ACC、CPC、PCIe/CXL/UALink 需求 |
| 中国 AI 芯片 | 受 HBM/先进制程约束，系统级互连和超节点更重要，高速铜、连接器、国产 retimer/PHY 有国产替代需求 | 国产 SerDes、连接器、AEC/ACC、光模块同步推进，良率和认证是关键 |

### 1.4 技术成熟与放量时间

| 技术 | 当前状态 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---|---|---|
| 800G DAC | 成熟量产，短距低成本 | 2026 继续占 0.5-2m 短距主流，2027 逐步让位 1.6T | AI rack 扩建带动绝对量继续增长 | 光模块紧张导致更多 800G 短距留在铜 |
| 800G AEC | 已放量，112G PAM4，1-7m | 2026 高速增长，2027 与 1.6T 并存 | 2026H2 成为多家 AI rack 默认 3-7m 方案 | 供不应求延续到 2027，AEC ASP 和毛利高位 |
| 1.6T DAC | 224G PAM4，短距可用但 reach 受限 | 2026 小批量，主要 0.5-1.5m | 2026H2 在高端 switch/NIC 内短距放量 | 224G passive channel 超预期，延缓部分 AEC/optics |
| 1.6T AEC/ACC | DesignCon/OFC 2026 密集展示，Molex/TE/Amphenol/Luxshare 等已有产品 | 2026H2 设计导入，2027 主流 AI rack 放量 | 2026H2 开始千万端口级拉货 | 2027 成为新增 AI rack 的默认短中距方案 |
| PCIe 6/CXL AEC/SCM | Astera/Marvell/Broadcom 生态成熟，开始收入化 | 2026H2 GPU/XPU-to-NIC/SSD/JBOG 放量 | 2027 开放 scale-up rack 标配 | 2026H2 多家 hyperscaler 锁单，TAM 快速重估 |
| CPC/top-side/flyover copper | 224G 部署，448G demo | 2026 高端 switch/accelerator design-in，2027 放量 | 2027H1 448G CPC 小批量 | 成为 CPO 之前最强“延寿”方案，毛利保持高位 |
| 448G/3.2T copper | 2026 pathfinding | 2027 design-in，2028 放量 | 2027H2 小批量 | 2026H2 proprietary fabric 提前采用 |
| CPO/OIO/OCS | 光方向增强 | 2026-2027 pilot，不替代 AEC/DAC 主体 | 2027 高端 switch 局部导入 | 若功耗压力失控，2027 CPO/OCS 提前吃掉部分 AEC/retimer 链路 |

## 2. 已开始放量的关键产品：市场规模、渗透率、利润率

口径说明：以下市场规模是全球 AI 数据中心相关收入池，包含线缆成品、连接器/笼子、主动线缆 silicon、少量认证/测试服务，不含完整交换机和光模块。3 个月为 2026-05 至 2026-08 run-rate，1 年为未来 12 个月，2 年为未来 24 个月。由于公开口径分散，区间偏宽。

### 2.1 放量产品总表

| 产品 | 代表产品/公司 | 未来 3 个月市场 | 未来 1 年市场 | 未来 2 年市场 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 400G/800G passive DAC | OSFP/QSFP-DD DAC，Amphenol、TE、Molex、Samtec、Luxshare、FIT、BizLink、3M、Volex | B $0.45-0.75B / O $0.75-1.1B / X $1.1-1.6B | B $2.0-3.2B / O $3.3-5.0B / X $5.0-7.5B | B $4.0-6.5B / O $6.5-10B / X $10-15B | 0.5-2m AI rack 铜链路 2026 55-70%，2027 因 224G/AEC 上升降至 40-60%，但绝对量增长 |
| 800G AEC | Credo ZeroFlap、Molex/Marvell/Broadcom、TE、Amphenol、Luxshare、FIT、Broadex | B $0.35-0.55B / O $0.55-0.9B / X $0.9-1.3B | B $1.5-2.3B / O $2.4-3.8B / X $4.0-6.0B | B $3.5-6.0B / O $6.5-11B / X $12-20B | 3-7m AI rack/row 内连接 2026 20-35%，2027 35-55%，极度乐观 65%+ |
| 800G ACC / active copper | Broadcom/Marvell/MACOM/MaxLinear/Semtech redriver，Luxshare/Amphenol/TE/Molex | B $0.10-0.25B / O $0.25-0.45B / X $0.45-0.75B | B $0.5-1.0B / O $1.0-1.8B / X $1.8-3.0B | B $1.5-3.0B / O $3.0-6.0B / X $6.0-10B | 1-4m、功耗敏感链路 2026 5-12%，2027 15-30%，极度乐观 40% |
| 1.6T OSFP AEC/ACC | Luxshare 1.6T OSFP AEC/ACC、Molex 224G AEC、TE OSFP 224G、Amphenol 1.6T、Broadcom/Marvell AEC silicon | B $0.15-0.35B / O $0.35-0.7B / X $0.7-1.2B | B $0.8-1.8B / O $1.8-3.8B / X $4.0-7.0B | B $3.0-7.0B / O $7.0-15B / X $16-28B | 1.6T 端口中铜短中距 2026 5-15%，2027 20-40%，极度乐观 55% |
| PCIe 5/6 AEC/SCM | Astera Aries/Taurus SCM、Marvell Alaska P AEC/AOC、Broadcom PCIe Gen6 retimer、Molex OSFP-XD | B $0.25-0.45B / O $0.45-0.75B / X $0.8-1.2B | B $1.2-2.0B / O $2.2-3.8B / X $4.0-6.5B | B $3.5-7.0B / O $8.0-15B / X $16-28B | 高端 AI server/rack PCIe/CXL 外接链路 2026 20-35%，2027 45-70% |
| 224G CPC/top-side/flyover copper | Samtec Si-Fly/BE、Molex/Arista、Luxshare KOOLIO、TE、Amphenol、Hirose、JAE | B $0.20-0.45B / O $0.45-0.8B / X $0.8-1.4B | B $1.0-2.2B / O $2.2-4.5B / X $5.0-8.0B | B $3.0-7.0B / O $8.0-16B / X $18-30B | 高端 switch/accelerator 224G board 2026 10-25%，2027 30-55%，极度乐观 70% |
| AEC/ACC retimer/DSP/redriver silicon | Credo、Broadcom、Marvell、Astera、MaxLinear、MACOM、Semtech、Point2 | B $0.45-0.8B / O $0.8-1.3B / X $1.3-2.0B | B $2.0-3.5B / O $3.5-6.0B / X $6.5-10B | B $5.5-10B / O $11-20B / X $22-35B | AEC/ACC 端口 attach 2026 20-35%，2027 40-65%；高端 ASIC/GPU rack 更高 |

### 2.2 利润率情景

| 产品 | 当前利润率估计 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|---:|
| Passive DAC | 成品毛利 18-32%，高端 OSFP 可 30-38% | 价格竞争，GM 18-30% | AI 认证件溢价，GM 25-38% | 光模块短缺，短距 DAC 加急溢价，GM 32-42% |
| 800G AEC | 成品 GM 35-55%；silicon GM 60-75%；Credo Q3 FY26 non-GAAP GM 68.6% | GM 38-52% | 缺货和 design-in 锁定，GM 45-60% | 关键客户预付/长约，GM 55-68% |
| ACC | 成品 GM 30-48%；redriver silicon GM 55-70% | GM 30-45% | 低功耗替代 AEC，GM 40-55% | 大客户快速转向，GM 50-62% |
| 1.6T AEC/ACC | 早期成品 GM 40-60%；silicon 65-78% | 2026 良率爬坡，GM 38-55% | 1.6T 供不应求，GM 50-65% | 224G 认证稀缺，GM 60-72% |
| PCIe/CXL AEC/SCM | 模块 GM 40-60%；Astera 类 silicon GM 70%+ | GM 45-60% | Gen6 缺货，GM 55-70% | 开放 scale-up fabric 爆发，GM 65-78% |
| CPC/top-side/flyover | 连接器/组件 GM 35-55% | GM 35-50% | 客户共同设计，GM 45-60% | 448G design-in 稀缺，GM 55-68% |
| Retimer/DSP silicon/IP | 半导体 GM 60-78%，IP 80-95% | GM 60-72% | 头部 silicon 供给紧张，GM 68-80% | 224G/448G 硅验证窗口稀缺，GM 75-85% |

## 3. 在研关键产品与未来快速增长方向

### 3.1 重点在研产品

| 在研方向 | 代表公司 | 技术状态 | 放量判断 |
|---|---|---|---|
| 448G differential copper / 3.2T electrical | Samtec、Luxshare、Molex/Arista、TE、Synopsys、Marvell、Keysight | DesignCon 2026 已出现 448G demo、PCIe 8.0-class 256GT/s pathfinding | 2026 研发/客户验证，2027 小批量 design-in，2028 扩大 |
| 3.2T OSFP-XD / 16-lane copper | Amphenol、TE、Molex、Luxshare、FIT、BizLink | OSFP-XD 机械和热设计推进中，224G/448G lane 组合未完全标准化 | 2027 高端 switch/AI fabric 试量，2028 放量 |
| Hybrid AEC/ACC | Marvell + Luxshare 等 | OFC 2026 展示 1.6T Alaska A AEC DSP + 4x200G ACC redriver 混合线缆 | 2026H2 客户验证，2027 在 NIC/switch 异构端口放量 |
| PCIe 7 AEC / PCIe 8 pathfinding | Astera、Marvell、Broadcom、Credo、Synopsys、Keysight、Teledyne LeCroy、Anritsu | PCIe 7 128GT/s 验证，PCIe 8 256GT/s 预研 | 2027 PCIe 7 retimer/AEC design win，PCIe 8 收入先在 IP/T&M |
| 224G/448G low-power retimer/redriver | Broadcom Agera、Marvell Alaska A/P、MaxLinear Annapurna、Credo、MACOM、Semtech | 200G/lane AEC/retimer 已展示，MaxLinear Annapurna 面向 1.6T/3.2T AEC 和 on-board retimer | 2026-2027 高毛利 silicon 主线 |
| Near-package/top-side copper cartridge | NVIDIA MGX ETL、Samtec、Molex、TE、Luxshare、Hirose | NVIDIA Vera Rubin 技术博客明确 copper cable cartridge；DesignCon 2026 top-side 论文获奖 | 2026 高端 rack 平台化，2027 变成标准供应链 |
| Liquid-cooled/high-density cable housing | Amphenol、Molex、TE、Samtec、Luxshare、Senko、Arista XPO 生态 | 1.6T/3.2T 端口热密度推动 cage/heatsink/cold plate 设计 | 2027 前后随 204.8T switch 与 3.2T 光/电共同增长 |

### 3.2 在研方向市场规模和渗透率

| 产品/技术 | 未来 3 个月 | 未来 1 年 | 未来 2 年 | 渗透率路径 | 利润率判断 |
|---|---:|---:|---:|---|---|
| 448G copper/channel components | B <$50M / O $50-120M / X $120-250M | B $0.2-0.6B / O $0.6-1.5B / X $1.5-3.0B | B $1.0-3.0B / O $3.0-8.0B / X $8.0-15B | 2026 几乎全是验证，2027 高端 AI switch 5-15%，极度乐观 25% | 早期 GM 55-75%，因测试/材料/连接器壁垒高 |
| 3.2T/OSFP-XD copper | B <$30M / O $30-80M / X $80-180M | B $0.1-0.4B / O $0.4-1.2B / X $1.2-2.5B | B $0.8-2.5B / O $2.5-6.0B / X $6.0-12B | 2027 新 switch 平台 3-10%，2028 扩大 | 成品 GM 45-65%，早期 ASP 高但良率和退货风险高 |
| Hybrid AEC/ACC | B <$40M / O $40-120M / X $120-250M | B $0.3-0.8B / O $0.8-1.8B / X $1.8-3.5B | B $1.2-3.0B / O $3.0-7.0B / X $7.0-12B | 2026H2 验证，2027 NIC/switch 异构端口 10-25% | GM 45-65%，系统专利/架构壁垒高 |
| PCIe 7 AEC/retimer | B <$100M / O $100-250M / X $250-500M | B $0.5-1.2B / O $1.2-2.8B / X $3.0-5.0B | B $2.5-6.0B / O $6.0-14B / X $15-28B | 2027 高端平台 design-in，2028 更广泛 | Silicon/IP GM 65-85%；T&M 60-70% |
| Near-package/top-side copper cartridge | B $0.15-0.35B / O $0.35-0.7B / X $0.7-1.2B | B $1.0-2.5B / O $2.5-5.5B / X $6.0-10B | B $4.0-9.0B / O $10-22B / X $24-40B | 高端 rack 2026 10-20%，2027 35-60% | GM 45-65%；客户锁定强 |
| Optical-aware retimer / copper-to-optics bridge | B <$100M / O $100-250M / X $250-600M | B $0.5-1.2B / O $1.2-3.0B / X $3.0-6.0B | B $3.0-7.0B / O $8.0-18B / X $20-35B | CPO/OCS pilot 越多，该桥接层越重要 | GM 65-80%，但路线不确定性高 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 地区 | 主要公司 | 工艺/能力 | 供给特征 |
|---|---|---|---|---|
| AEC/ACC retimer/DSP/redriver silicon | 美国、以色列、新加坡、台湾设计；TSMC/Samsung 代工 | Credo、Broadcom、Marvell、Astera、MaxLinear、MACOM、Semtech、Point2 | 5nm/4nm/3nm/成熟节点混合，112G/224G PAM4 SerDes、DSP、FEC、telemetry | 高毛利、客户验证长、设计团队稀缺 |
| 高速连接器/cage/OSFP/QSFP-DD/OSFP-XD | 美国、日本、台湾、中国、东南亚 | Amphenol、TE、Molex、Samtec、Hirose、JAE、Luxshare、FIT、BizLink、Senko | 精密冲压、注塑、镀金、热设计、EMI shielding、high-density cage | 机械公差和量产一致性是壁垒 |
| Twinax/高速铜缆 | 中国、台湾、越南、马来西亚、泰国、墨西哥、美国 | Luxshare、FIT、BizLink、Amphenol、TE、Molex、3M、Volex、JPC、Broadex | 低损耗 twinax、25-34 AWG、屏蔽、阻抗控制、skew 控制 | 产能可扩，但高端 224G 良率和认证慢 |
| 线缆成品组装 | 中国和东南亚为主，北美近岸化增加 | Luxshare、FIT、BizLink、Molex、TE、Amphenol、Volex、Broadex、NADDOD、JPC | 端接、焊接/压接、EEPROM、PMIC、散热壳、自动测试 | 普通组装毛利低，高速认证件毛利高 |
| 测试与验证 | 美国、台湾、中国、日本、德国 | Keysight、Anritsu、Tektronix、Teledyne LeCroy、Rohde & Schwarz、VIAVI | 65GHz+ scope、BERT、VNA、145GHz/250GHz fixture、FEC/BER 软件 | 测试时间和仪器交期可能卡量产 |
| 系统集成/OEM/ODM | 台湾、美国、中国、墨西哥、东南亚 | Dell、HPE、Lenovo、Supermicro、QCT、Wiwynn、Foxconn、Inventec、Pegatron、Celestica、Accton | NVIDIA MGX/NVL、白盒 switch、AI rack cabling、液冷集成 | 认证供应商名单决定线缆份额 |

### 4.2 供给瓶颈

1. **224G/448G SerDes 和 DSP 人才。** 高速模拟/混合信号不是纯数字设计，能把 BER、FEC、功耗、热管理和客户 firmware 做到量产的团队很少。
2. **Retimer/DSP 热设计。** 1.6T AEC cable end 放入多颗高功耗芯片，OSFP cage、airflow、heatsink、liquid-cooled rack 环境都会影响失效率。
3. **Twinax 制造一致性。** 224G 下 impedance、skew、pair-to-pair coupling、shielding、bend radius 的分布比平均值更重要，良率决定毛利。
4. **连接器机械公差。** OSFP/QSFP-DD/OSFP-XD、CPC/top-side 的 mating interface、镀层、插拔寿命、EMI 和 thermal path 决定系统级 margin。
5. **客户认证与互操作。** NVIDIA、Google、Meta、AWS、Microsoft、Oracle、OEM/ODM 都有独立 qualification；同样是 1.6T AEC，通过一个客户不等于通吃市场。
6. **高端测试产能。** 224G/448G/PCIe 7/8 需要昂贵仪器和自动化夹具，测试时间拉长会吞噬线缆厂毛利。
7. **Firmware/telemetry。** AEC/SCM 已不只是物理线，CMIS/I2C/EEPROM、link training、fleet diagnostics、firmware update 都影响客户可维护性。
8. **地缘与关税。** 高速线缆产能集中在东亚，但北美 AI 数据中心要求供应链多元化，墨西哥、越南、马来西亚、泰国、美国本土产线会享受溢价。

### 4.3 BOM 和毛利决定因素

| 产品 | 典型 BOM 拆分 | 毛利决定因素 |
|---|---|---|
| Passive DAC | Twinax 铜缆 35-50%；连接器/cage/壳体 25-35%；EEPROM/小 PCB 1-5%；组装测试 10-20%；物流/损耗 5-10% | AWG、长度、OSFP/QSFP-DD form factor、客户认证、良率、铜价和加急交付 |
| 800G/1.6T AEC | Retimer/DSP/SerDes 35-55%；连接器/散热壳 15-25%；twinax 10-25%；PMIC/EEPROM/PCB 5-10%；组装测试 10-20% | Silicon 供应、功耗、BER、firmware、客户认证、测试时间、退货率 |
| ACC | Redriver/linear EQ 15-35%；twinax 20-30%；连接器/热结构 20-30%；PMIC/EEPROM 3-8%；组装测试 10-20% | 功耗低于 AEC、reach 低于 AEC，若客户接受，毛利弹性大 |
| CPC/top-side/flyover | 精密连接器/基座 35-50%；高速线缆 20-35%；结构/散热/EMI 10-20%；测试 10-20% | 是否进入 reference design、224G/448G margin、机械公差、平台锁定 |

价格传导机制：

- 原材料铜价对高端 AEC 总成本影响有限，真正的价格弹性来自 retimer/DSP、测试时间和客户认证。
- Hyperscaler 通常通过年度/半年度框架协议压价，但供不应求时会给 NRE、加急费、长约锁量、二供认证费。
- AEC/SCM 价格不是线性按长度定价，而是按速率、芯片、认证、热设计、telemetry 和失效率定价。
- 1.6T 初期 ASP 高，2027 产能扩散后会降价；但如果 GB300/Rubin/TPU/ASIC 同步拉货，降价可能被 mix 升级抵消。

## 5. 竞争格局与壁垒

### 5.1 市场结构估计

由于 AEC/DAC 公开份额口径很少，以下为基于公司收入、产品可见度、客户 design-in 和行业反馈的估算：

- **AEC active silicon：** Credo、Broadcom、Marvell、Astera、MaxLinear、MACOM 等 CR3 可能在 60-80%。Credo 是 AEC first mover，Broadcom/Marvell 更强在交换 ASIC、NIC、retimer 和客户 bundle。
- **高端 AEC/DAC 成品线缆：** Amphenol、TE、Molex、Luxshare、FIT、BizLink、Samtec、3M、Volex 等 CR5 约 45-65%，但按客户和 form factor 差异很大。
- **224G/448G CPC/top-side：** Samtec、Molex、TE、Amphenol、Luxshare、Hirose、JAE 等头部集中度高，且设计导入后切换成本大。
- **PCIe/CXL AEC/SCM/fabric：** Astera 在 PCIe/CXL connectivity 纯度最高，Marvell/Broadcom 有更广平台，Microchip/Montage/Parade/Rambus/Synopsys 等在 switch/controller/IP 中分食。

### 5.2 可量化壁垒和定价原因

| 壁垒 | 为什么能定价 |
|---|---|
| 112G/224G/448G SerDes 量产经验 | 眼图 demo 不等于百万端口可靠运行，客户愿意为低 BER、低功耗和少 downtime 付溢价 |
| Retimer/DSP firmware + telemetry | AEC/SCM 可被远程监控和诊断，减少 AI rack 维护成本，形成软件化价值 |
| 高速连接器机械公差 | 224G 下微小偏差会吃掉 channel margin，头部厂商的 SPC 和制程窗口本身就是壁垒 |
| 客户认证和 AVL | 一旦进入 NVIDIA/Google/Meta/AWS/Microsoft/OEM AVL，替换会触发整 rack 重新验证 |
| 专利与 IP | Credo 已就 AEC 专利与 TE/Molex 等达成 settlement/licensing，说明 active cable IP 有现实约束 |
| 全球制造网络 | 北美客户需要中国、东南亚、墨西哥、美国多地交付，具备复制认证和质量控制的公司议价强 |
| 测试自动化 | 224G/448G 测试时间贵，能把测试吞吐、误判率和追溯系统做好的厂商毛利更稳 |
| 与 switch/NIC/GPU 平台共同设计 | 线缆从 commodity 变成 reference architecture 一部分，价值按系统风险定价 |

### 5.3 价值捕获排序

长期高 ROIC/高毛利最可能在三层：

1. **Retimer/DSP/SerDes silicon 与 IP。** Credo、Astera、Broadcom、Marvell、MaxLinear、Synopsys/Rambus/Cadence 类资产毛利最高，且客户一旦 design-in，生命周期长。
2. **高端 CPC/top-side/OSFP-XD 连接器。** 机械公差、热设计、客户认证和平台锁定让头部连接器公司能维持 40-60% 的高端产品毛利。
3. **认证过的 AEC/ACC 成品。** 普通线缆毛利会被压低，但 1.6T/PCIe6/客户定制 AEC 在供不应求阶段有高溢价。

价值捕获较弱的是普通 copper raw cable、低速 DAC、纯代工组装。它们受铜价、人工、产能扩散和客户压价影响更大。

## 6. 2026 关键变化：三个最可能拐点

1. **1.6T/224G AEC/ACC 从 demo 进入 AI rack 设计导入。** Luxshare、Molex、TE、Amphenol、Broadcom、Marvell 的 1.6T/224G 产品已经具备公开可见度，2026H2 最可能在 GB300 后续、ASIC rack、800G/1.6T switch 端口进入实单。
2. **PCIe 6/CXL AEC/SCM 成为开放 AI rack 的核心 BOM。** Astera Scorpio/Aries、Marvell Alaska P、Broadcom PCIe Gen6 retimer 把 active cable 从以太网前面板扩展到 GPU/XPU/SSD/NIC/CXL fabric。
3. **短距铜和长距光分层被市场重新定价。** TrendForce 800G+ 光模块 60%+ 出货占比并不否定铜，反而定义了边界：Google Ironwood 明确短距高速铜、rack 间 OCS 光网络。2026 的正确组合是“rack 内铜升级 + rack 间光爆发”。

## 7. 2027 关键变化：三个最可能拐点

1. **224G 成为高端新增 AI fabric 标配，448G 开始小批量 design-in。** Passive DAC reach 受限，AEC/ACC/CPC attach rate 明显提升，3.2T/OSFP-XD 和 PCIe 7 周边先在 IP/T&M/retimer 兑现。
2. **Rubin/MI400/TPU8/Trainium3/Meta/OpenAI ASIC 把铜互连从 rack 内推进到 pod 级架构。** NVIDIA Vera Rubin 技术博客中的 copper cartridge 和 direct chip-to-chip spine 是强信号，开放平台也会用 PCIe/CXL/UALink/以太网复制类似思路。
3. **CPO/OCS 开始挤压部分电连接，但不会杀死高端铜。** CPO 先在 switch/scale-out 和少数 scale-up pilot 走量，短距低延迟、可维护、高良率的铜仍会留在 near-ASIC、rack 内、cable cartridge 和 PCIe/CXL 场景。

## 8. 头部公司与细分清单

### 8.1 AEC/ACC/DAC 线缆与连接器

- **Amphenol**：OSFP/QSFP-DD/OSFP-XD、AEC/DAC、1.6T 与 3.2T 路线，高端连接器规模优势强。
- **TE Connectivity**：OSFP 224G copper cable assemblies，支持 1.6T、25-32 AWG、EEPROM 管理，汽车/工业/数据中心质量体系强。
- **Molex**：AEC 产品线最完整之一，112G 最高 7m、224G 2.5m+，支持 Broadcom/Marvell/Point2/Astera retimer。
- **Samtec**：Si-Fly、BE、CPC/top-side、224G/448G pathfinding，在 DesignCon 技术影响力强。
- **Luxshare-Tech / 立讯精密体系**：224G/448G CPC、1.6T OSFP AEC/ACC、PCIe 6 OSFP-XD AEC，制造规模和客户响应强。
- **Foxconn Interconnect Technology (FIT)**：高速线缆、光/电互连、Marvell Golden Cable 生态中 1.6T AEC 快速设计案例。
- **BizLink**：高速 cable assembly、AI server 供应链、全球制造布局。
- **3M**：twinax/high-speed cable、AEC 相关授权/生态，材料和高速线缆历史深。
- **Volex**：数据中心高速线缆、全球制造。
- **Broadex、JPC Connectivity、NADDOD/专业模块厂**：1.6T AEC/DAC 产品可见，更多在渠道和区域客户。
- **Hirose、JAE、Lotes、Foxconn、Rosenberger、Huber+Suhner、Senko**：高速连接器、cage、光电连接和系统件。

### 8.2 AEC/ACC silicon、retimer、DSP、IP

- **Credo**：AEC first mover，ZeroFlap AEC 覆盖 100G-1.6T，FY26 高增长和 68%+ 毛利是最直接商业验证。
- **Broadcom**：Tomahawk/Jericho/Thor/Agera/PCIe Gen6/200G-lane retimer，OFC 2026 展示 up to 6m AEC，客户 bundle 能力极强。
- **Marvell**：Alaska A 1.6T AEC DSP、Alaska P PCIe 6 retimer、Golden Cable initiative、hybrid AEC/ACC，兼具 PCIe、以太网和光 DSP。
- **Astera Labs**：Aries/Taurus SCM、Scorpio PCIe 6 fabric switch、COSMOS telemetry，PCIe/CXL/AI fabric 纯度最高。
- **MaxLinear**：Annapurna 224G scale-up retimer，面向 1.6T/3.2T AEC 和 on-board retimer。
- **MACOM**：linear driver/redriver、LPO/ACC 相关模拟链路能力。
- **Semtech**：Signal integrity、PAM4/retimer/redriver、DesignCon copper cable 论文生态。
- **Point2 Technology**：AEC/retimer 供应商，Molex 产品表中可见。
- **Synopsys、Cadence、Rambus、Alphawave Semi、Siemens EDA、Arteris**：224G/448G SerDes IP、PCIe/CXL/UCIe PHY/VIP、EDA 验证。
- **Parade、Montage、Microchip**：PCIe/CXL retimer、switch、controller，服务器和中国替代链受益。

### 8.3 系统、交换机与平台拉动方

- **NVIDIA**：GB300/Rubin/MGX/DSX/Spectrum-X/NVLink 是高端 AI rack 铜互连的核心规则制定者。
- **Broadcom**：Tomahawk 6 102.4T、Davisson CPO、custom XPU、PCIe/以太网 retimer，开放 AI Ethernet 和 ASIC 的核心供应商。
- **Marvell**：Teralynx、custom silicon、Alaska、coherent DSP，连接 GPU/ASIC、NIC、光和铜。
- **Astera Labs**：开放 PCIe/CXL AI scale-up fabric 推动者。
- **Arista、Cisco、Juniper/HPE、Celestica、Accton、Edgecore、UfiSpace**：1.6T/102.4T switch 系统带动 OSFP224、AEC/DAC、ACC、光模块需求。
- **Dell、HPE、Lenovo、Supermicro、QCT、Wiwynn、Foxconn、Inventec、Pegatron、Aivres、ASUS、Gigabyte**：AI rack 集成和线缆 AVL 决策。
- **Google、AWS、Microsoft、Meta、Oracle、OpenAI、Anthropic、CoreWeave、xAI、Crusoe、Lambda、Nebius**：实际拉货和认证节奏决定行业收入。

### 8.4 中国和亚太供应链

- **立讯精密/Luxshare-Tech**：高端铜缆、CPC、AEC/ACC、系统线束，全球客户导入能力强。
- **FIT/鸿腾、鸿海/Foxconn、BizLink、正崴、贸联、良维、信邦、胡连、连展、宣德、凡甲、嘉泽、长盈精密、电连技术**：高速连接器、线束、服务器/数据中心线缆和制造能力。
- **中际旭创、天孚通信、新易盛、光迅、华工正源、源杰、仕佳光子、联亚、上诠**：主要是光互联，但与铜互联共同进入 AI 网络 BOM，客户认证和封装产能有协同。
- **深南电路、沪电股份、生益科技、台光电、联茂、金像电、欣兴、臻鼎**：高速 PCB/低损耗材料/载板，对 224G/448G channel 很重要。
- **澜起科技、瑞昱、谱瑞、祥硕、信骅、Nuvoton、ASPEED**：PCIe/CXL/管理控制/连接芯片生态，部分可承接国产替代。

## 9. 情景化总判断

| 维度 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 AI 高速铜互连广义市场（DAC/AEC/ACC/CPC/retimer） | $8B-$13B | $13B-$22B | $22B-$35B |
| 2027 广义市场 | $14B-$25B | $28B-$48B | $55B-$85B |
| 2026 窄 AEC 市场 | $1.3B-$2.2B | $2.3B-$4.0B | $4.0B-$6.5B |
| 2027 窄 AEC 市场 | $3B-$6B | $6B-$12B | $12B-$20B |
| 1.6T AEC/ACC 放量时间 | 2026H2 design-in，2027 放量 | 2026H2 明显收入化 | 2026H2 供不应求 |
| 448G 铜放量时间 | 2027 design-in，2028 放量 | 2027H2 小批量 | 2026H2 proprietary fabric 先上 |
| 最强毛利层 | Retimer/DSP/IP、CPC/top-side、认证 AEC | 同左，叠加 PCIe/CXL fabric | 同左，叠加 448G 和 optical-aware retimer |

## 10. 主要来源

- [NVIDIA GB300 NVL72 官方页面](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- [NVIDIA GB300 NVL72 Enterprise Reference Architecture PDF, 2026-03](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory-with-gb300-nvl72-dual-plane-networking-architecture.pdf)
- [NVIDIA Vera Rubin 官方新闻稿, 2026-03-16](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx)
- [NVIDIA Vera Rubin POD 技术博客, 2026-03-16](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)
- [NVIDIA/Microsoft Azure GB300 NVL72 production cluster for OpenAI](https://blogs.nvidia.com/blog/microsoft-azure-worlds-first-gb300-nvl72-supercomputing-cluster-openai/)
- [AMD CES 2026 Helios/MI400/MI500 新闻稿](https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-and-its-partners-share-their-vision-for-ai-ev.html)
- [TrendForce: 2026 前九大 CSP CapEx 约 8,300 亿美元](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html)
- [TrendForce: 800G+ 光模块 2026 占比 60%+，Google Ironwood 短距铜 + OCS](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- [TrendForce: 2026 AI 光收发模块市场 260 亿美元](https://www.trendforce.com.tw/presscenter/news/20260420-13016.html)
- [TrendForce: CPO 2026 约 0.5%，2030 约 35% 潜在渗透](https://www.trendforce.com/presscenter/news/20260311-12962.html)
- [Luxshare-Tech DesignCon 2026 224G/448G、1.6T OSFP AEC/ACC](https://en.luxshare-tech.com/company/resources/news/designcon-2026-unveiling-224g-448g.html)
- [Molex Active Electrical Cables](https://www.molex.com/en-us/products/connectors/high-speed-pluggable-io/active-electrical-cables-aec)
- [Amphenol Active Electrical Cables](https://www.amphenol-cs.com/cables/active-electrical-cables.html)
- [TE Connectivity OSFP 224G Copper Cable Assemblies PDF](https://www.te.com/content/dam/te-com/documents/consumer-devices/global/ddn-fly-osfp-224g-copper-cable-assemblies.pdf)
- [Credo ZeroFlap AEC](https://credosemi.com/products/zeroflapaec/)
- [Credo Q3 FY26 results, SEC exhibit](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm)
- [Astera Labs Scorpio X-Series 320-lane AI fabric switch](https://www.asteralabs.com/news/astera-labs-extends-leadership-in-open-ai-scale-up-networking-with-new-320-lane-scorpio-x-series-smart-fabric-switch/)
- [Astera Taurus Ethernet Smart Cable Modules](https://www.asteralabs.com/products/taurus-ethernet-smart-cable-modules/)
- [Broadcom OFC 2026 AI infrastructure release](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai)
- [Broadcom Tomahawk 6 102.4T production volume](https://investors.broadcom.com/news-releases/news-release-details/broadcom-now-shipping-worlds-first-1024-tbps-switch-production)
- [Marvell PCIe retimers adopted by AI/data center providers](https://www.marvell.com/company/newsroom/marvell-announces-pcie-retimers-adoption-by-ai-dc-providers.html)
- [Marvell Golden Cable initiative](https://www.marvell.com/blogs/golden-cable-initiative-hyperscale-cable-partner-ecosystem.html)
- [Marvell hybrid AEC/ACC OFC 2026 blog](https://www.marvell.com/blogs/hybrid-aec-acc-cables-for-optimizing-infrastructure.html)
- [MaxLinear Annapurna 224G scale-up retimer](https://www.maxlinear.com/news/press-releases/2026/maxlinear-unveils-annapurna-224g-scale-up-retimer-to-extend-copper-connectivity-in-ai-data-centers)
- [LightCounting PAM4 and Coherent DSPs newsletter summary, 2026-02](https://www.lightcounting.com/newsletter/en/february-2026-pam4-and-coherent-dsps-381)
- [Tom's Hardware/Bloomberg: 2026 美国数据中心电力设备瓶颈](https://www.tomshardware.com/tech-industry/artificial-intelligence/half-of-planned-us-data-center-builds-have-been-delayed-or-canceled-growth-limited-by-shortages-of-power-infrastructure-and-parts-from-china-the-ai-build-out-flips-the-breakers)

## 11. 项目内参考

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\conference_update\designcon_2026_conference_update.md`
- `D:\drive\Investment\调研\v5\conference_update\ofc_2026_conference_update.md`
- `D:\drive\Investment\调研\v5\conference_update\nvidia_gtc_2026_research.md`
- `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_AI服务器CPU与控制平面芯片_2026.md`
# 行业调研：【AI Fabric网络操作系统与遥测软件】

> 截至日期：2026-05-08  
> 研究对象：AI 计算中心后端网络/scale-up/scale-out/scale-across 的网络操作系统、fabric 管理、遥测、自动化、数字孪生、网络 AIOps、RDMA/拥塞控制软件与开源/闭源生态。  
> 重要口径：本文把“AI Fabric 软件收入池”定义为交换机/NIC/光模块之外的软件、支持与服务价值，包括 NOS 授权/订阅/支持、fabric controller、telemetry/observability、intent-based automation、digital twin、NetOps AI assistant、调优与认证服务。很多软件随硬件打包销售，公开财报不会单独披露，因此文中的市场规模是研究估算。

## 0. 一页结论

AI Fabric 网络软件正在从“交换机上的操作系统”升级为“AI 工厂的生产控制系统”。2026 年，AI 集群规模从几千/几万 GPU 走向 10 万 GPU 以上，网络故障不再只是丢包或延迟，而是直接变成 GPU 利用率下降、训练 job 重启、token 产能损失和机房电力浪费。因此，网络 OS、实时 telemetry、job-aware congestion control、digital twin 和自动化运维开始拥有独立定价权。

**最乐观的主判断：2026-2028 年 AI Fabric 软件收入池会比传统数据中心网络软件快 2-3 倍增长。**  
在本文模型中，全球 AI Fabric 网络 OS 与遥测软件的可见收入池为：

| 口径 | 未来 3 个月 | 未来 12 个月 | 未来 24 个月年化 run-rate |
|---|---:|---:|---:|
| 基准 | $1.8B-$3.0B | $7B-$11B | $14B-$24B |
| 乐观 | $3.0B-$4.8B | $11B-$17B | $25B-$40B |
| 极度超预期乐观 | $4.8B-$7.5B | $18B-$28B | $45B-$70B |

这个估算建立在三个硬锚上：

1. **AI 网络硬件池足够大**：项目内《AI数据中心建设规模与产业链订单映射》给出网络与光互联 2026 订单池基准 $65B-$100B、2027 $100B-$160B，乐观可到 $105B-$165B / $170B-$280B。
2. **软件 attach rate 正在抬升**：普通数据中心网络软件/支持可能只占交换系统价值的 5%-10%；AI backend 因为 telemetry、拥塞控制、job-level observability、变更验证和多厂商互通，软件/支持/服务价值可上升到 10%-18%，极端大型集群可到 20%+。
3. **第一手信息已验证方向**：OpenAI 2026-05-05 公开 MRC/SRv6，并称 MRC 已用于其最大的 NVIDIA GB200 supercomputer，包括 OCI Abilene 与 Microsoft Fairwater；NVIDIA 2026-01/03 把 Spectrum-X、Cumulus、NetQ、UFM/NMX、DSX 都纳入 AI Factory 软件栈；Arista、Cisco、Broadcom、HPE/Juniper、Nokia、Arrcus、Hedgehog 都在 2026 明确把 AI fabric telemetry、agentic operations 和 open Ethernet 写入产品发布。

**2026 最可能放量的技术路径**：  
`800G Ethernet/RoCE + InfiniBand/NVLink 存量 + NVIDIA Spectrum-X/Cumulus/NetQ/UFM + Arista EOS/CloudVision + Cisco Nexus One/Nexus Dashboard + SONiC/SAI + gNMI/OpenConfig/OpenTelemetry + job-aware telemetry`。  
也就是说，2026 是“可插拔 800G/1.6T 光互联硬件放量 + 管理软件补票”的年份，不是完全重写网络协议的年份。

**2027 最可能放量的技术路径**：  
`1.6T Ethernet + MRC/SRv6 + UEC/UET/CSIG + ESUN/UALink scale-up + CPO/OCS telemetry + closed-loop AIOps`。  
2027 的核心变化是：AI 网络控制从“packet/path 层”上升到“job/token/GPU 利用率层”，软件从监控工具变成调度和产能优化工具。

## 1. 行业定义：AI Fabric 软件栈分层

| 层级 | 典型产品/技术 | 2026 状态 | 价值来源 |
|---|---|---|---|
| Network OS / NOS | NVIDIA Cumulus Linux、SONiC、Arista EOS、Cisco NX-OS/Nexus One、Nokia SR Linux、Juniper/HPE Junos/Apstra、DriveNets DNOS、Arrcus ArcOS、Dell Enterprise SONiC | 已放量 | 稳定性、硬件抽象、ASIC/NIC feature 暴露、自动化 API、支持合同 |
| Fabric controller / lifecycle | NetQ、UFM、NMX、CloudVision/CV UNO、Nexus Dashboard/Nexus Hyperfabric、Juniper Apstra、Nokia EDA、Aviz ONES、Hedgehog Fabric、DriveNets Network Cloud-AI | 2026 快速放量 | Day 0/1/2 自动化、ZTP、变更验证、拓扑可视化、版本升级、故障隔离 |
| Telemetry / observability | gNMI、OpenConfig、OpenTelemetry、Prometheus/Grafana、Splunk、ThousandEyes、Kentik、Datadog、Riverbed、NETSCOUT、Gigamon、NetDL、NVIDIA UFM Telemetry | 从可选变必选 | 快速定位丢包、PFC storm、ECN/CNP、光模块 flapping、RDMA tail latency、GPU job slow node |
| AI transport / congestion control | RoCEv2/DCQCN、PFC/ECN、adaptive routing、packet spraying、MRC/SRv6、UEC UET、CSIG、ESUN header、LLR/CBFC | 2026 从超大客户生产验证向行业扩散 | 降低 tail latency、提高 all-reduce/collective throughput、提升 GPU 利用率 |
| Digital twin / validation | NVIDIA DSX Sim/Omniverse DSX、NVIDIA Air、Apstra digital twin、Nokia EDA Digital Sandbox、Forward Networks、Batfish、Keysight/VIAVI validation software | 2026 设计/验证环节先放量 | 减少变更失败、缩短上线周期、减少物理 lab 成本 |
| Agentic NetOps | Arista AVA、Cisco AgenticOps、Nokia EDA AIOps、HPE Mist/OpsRamp、Aviz Network Copilot、Selector AI、Arrcus AINF policy control | 2026 早期，2027 扩张 | 从“告警摘要”走向受控自动修复、自动调参、自动回滚 |

## 2. 最近半年与 2026 一手信号

| 日期 | 来源 | 关键信号 | 对投资判断的含义 |
|---|---|---|---|
| 2026-05-05 | [OpenAI：MRC supercomputer networking](https://openai.com/index/mrc-supercomputer-networking/) | OpenAI、AMD、Broadcom、Intel、Microsoft、NVIDIA 联合开发 MRC；MRC 已部署在 OpenAI 最大 GB200 supercomputer，含 OCI Abilene 与 Microsoft Fairwater；OCP 公开规格 | AI backend transport 进入“开放规格 + 生产验证”阶段，2027 可能成为高端 Ethernet fabric 的默认能力 |
| 2026-05-06 | [NVIDIA Spectrum-X with MRC](https://blogs.nvidia.com/blog/spectrum-x-ethernet-mrc/) | NVIDIA 称 MRC 已在 Spectrum-X 生产验证，并强调 purpose-built hardware、deep telemetry、intelligent fabric control | NVIDIA 不只是卖 switch/NIC，而是把 transport + telemetry + control 做成平台 |
| 2026-03-16 | [NVIDIA DSX reference design](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-Vera-Rubin-DSX-AI-Factory-Reference-Design-and-Omniverse-DSX-Digital-Twin-Blueprint-With-Broad-Industry-Support/default.aspx) | DSX 覆盖 compute、Spectrum-X networking、storage、power、cooling、controls；Switch EVO AI Factories/LDC EVO OS 接入实时 telemetry 与数字孪生 | AI factory 软件控制面开始横跨网络、电力和冷却，价值链向“运营系统”扩张 |
| 2026-01 | [NVIDIA Spectrum-X telemetry blog](https://developer.nvidia.com/blog/next-generation-ai-factory-telemetry-with-nvidia-spectrum-x-ethernet/) | Spectrum-X 集成 switch、SuperNIC、GPU 与 NetQ telemetry；支持 OpenTelemetry 与 gNMI | 真实生产问题需要跨 GPU/NIC/switch 的全栈遥测，传统 SNMP 不够 |
| 2026-05-05 | [Arista Q1 2026 results](https://www.arista.com/en/company/news/press-release/24017-pr-20260505) | Q1 收入 $2.709B，+35.1% YoY；non-GAAP operating margin 47.8%；XPO 高密液冷可插拔光学、AI Spine、VOQ、buffer/PFC storm 控制 | Arista 的 EOS/CloudVision 与硬件共同受益，软件稳定性是其高经营利润率的核心 |
| 2026-02-11 | [Cisco Q2 FY2026 earnings](https://investor.cisco.com/news/news-details/2026/CISCO-REPORTS-SECOND-QUARTER-EARNINGS/default.aspx) | Q2 收入 $15.3B，+10% YoY；AI infrastructure orders from hyperscalers $2.1B；Networking revenue +21% | Cisco 的 AI 订单开始转化，Nexus One/Nexus Dashboard/Splunk 是其差异化软件抓手 |
| 2026-03-04 | [Broadcom Q1 FY2026 SEC exhibit](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm) | Q1 AI revenue $8.4B，+106% YoY；Q2 AI semiconductor revenue 指引 $10.7B；增长来自 custom AI accelerator 和 AI networking | Broadcom 的交换芯片、NIC、SONiC/SAI/SDK 是开放 AI Ethernet 的底层税基 |
| 2026-03-10 | [OCP ESUN 1.0](https://www.opencompute.org/blog/the-ocp-esun-10-specification-has-been-released) | ESUN 1.0 发布，4-byte header、lossless、LLR/CBFC、PFC 等；参与公司从 12 家增至 175+ | scale-up Ethernet 从讨论变成规范，AMD/Meta/Microsoft/OpenAI 路线受益 |
| 2026-03/04 | [Nokia EDA](https://www.nokia.com/data-center-networks/data-center-fabric/event-driven-automation/) | EDA 通过 AIOps engine 实时关联 telemetry、topology、change data，可覆盖最大 AI fabrics | Nokia/SR Linux/EDA 是非美 hyperscaler、主权云和电信云的重要开源化替代路线 |
| 2026-03-16 | [Arrcus AINF + NVIDIA Dynamo](https://arrcus.com/news/arrcus-inference-network-fabric-ainf-announces-integration-with-nvidia) | AINF 接入 Dynamo 的 queue depth、KV-cache pressure、replica health，并做跨站点 model-aware routing | 推理网络控制会从训练 collective 扩展到全球 inference fabric |

## 3. 课题一：2026 机遇、挑战与技术路径

### 3.1 2026 机遇

1. **GPU 利用率变成可量化 ROI**：10 万 GPU 级集群的硬件 CapEx 往往是 $4B-$8B。网络软件只要提升 1% 有效利用率，就等价于释放 $40M-$80M 的硬件价值；如果按 token revenue/GW 看，价值更高。这使得 $5M-$50M/cluster 的 fabric 软件合同变得容易被客户接受。
2. **AI backend 网络从“工程定制”走向“产品化复制”**：GB300/Rubin、AWS Trainium、Google TPU、AMD Helios、Meta MTIA/OpenAI ASIC 都要求成套网络 reference design。Reference design 一旦固化，NOS、telemetry、automation 会跟着复制。
3. **Ethernet 替代/补充 InfiniBand 带来新软件栈**：NVIDIA Spectrum-X、Broadcom Tomahawk/Thor、Cisco Silicon One、Arista Etherlink、Nokia SR Linux、SONiC 等都在争夺“AI Ethernet 的控制面”。
4. **Agentic inference 推动网络从训练后端进入在线业务路径**：训练网络容忍离线调优；推理网络要按照 SLA、地理位置、KV cache、模型副本状态、token 成本做实时路由。Arrcus AINF + Dynamo 是早期样板。
5. **电力/冷却/网络统一遥测成为 AI 工厂标准**：NVIDIA DSX 把 network、power、cooling signals 纳入同一控制面，说明网络遥测不再只给网络团队用，而是给 AI factory operator、scheduler 和电力优化系统用。

### 3.2 2026 挑战

1. **多厂商互通仍旧脆弱**：RoCEv2、PFC、ECN、CNP、DCQCN、adaptive routing、NIC firmware、GPU collective library、switch ASIC feature 的组合非常多，任何一处版本不匹配都会拖慢 job。
2. **遥测数据量爆炸**：100k GPU 集群若按 GPU/NIC/switch/optic 每秒采样，metric cardinality 可以轻易进入亿级。数据湖、压缩、采样、保留期和成本会成为新瓶颈。
3. **故障定位难度从 device 变成 path/job**：传统网络 NOC 关注 interface down；AI fabric 要定位“哪个 rail、哪个 T0-T1 link、哪个 NIC port 让 NCCL all-reduce tail latency 变差”。
4. **开源 SONiC 的产品化 gap**：SONiC 能降低锁定，但客户仍需要硬件认证、ASIC SDK、optic/CMIS、warm reboot、ISSU、TAC 和安全 patch。真正赚钱的是“hardened SONiC + support + automation”。
5. **客户内部分工割裂**：网络、平台、GPU scheduler、storage、security、facility 团队的数据模型不同，AI fabric 软件必须跨团队，销售周期会变长。
6. **安全风险被低估**：agentic NetOps 可以自动改网络，也意味着 telemetry poisoning、错误自动修复、越权操作会变成生产风险。

### 3.3 当前正在被使用的核心技术

| 技术 | 当前用途 | 2026 成熟度 | 关键软件点 |
|---|---|---|---|
| InfiniBand / Quantum-X / UFM | NVIDIA 高端训练与 DGX SuperPOD | 成熟但增长更多绑定 NVIDIA 封闭栈 | UFM telemetry、congestion counters、SHARP、fabric health |
| NVLink/NVSwitch/NMX | GB200/GB300/Rubin rack 内 scale-up | 成熟放量 | NMX/NVML/NetQ、NVLink switch telemetry |
| RoCEv2 lossless Ethernet | AI backend Ethernet 主流 | 成熟但调优难 | PFC、ECN、DCQCN、CNP、队列/缓冲/拥塞观测 |
| Spectrum-X | NVIDIA AI Ethernet | 2025-2026 快速放量 | Cumulus、NetQ、BlueField/SuperNIC telemetry、adaptive routing |
| Arista Etherlink/EOS/CloudVision | Meta/Microsoft 等 hyperscaler 和企业 AI | 放量 | CLB、VOQ、CV UNO、NetDL、job-centric observability |
| Cisco Nexus One/Nexus Dashboard | Enterprise/NeoCloud AI POD 与 hyperscaler AI order | 放量初期 | Silicon One、AgenticOps、Splunk telemetry、Hyperfabric cloud-managed |
| SONiC/SAI | Hyperscaler/open networking/whitebox | hyperscaler 成熟，enterprise 产品化中 | ASIC abstraction、OpenConfig/gNMI、社区 feature 与商业 support |
| Apstra/EDA/intent-based automation | Day0/1/2 fabric lifecycle | 放量初期 | intent、digital twin、pre/post-check、rollback |
| MRC/SRv6 | OpenAI/Microsoft/OCI GB200 supercomputers | 生产验证，生态扩散初期 | packet spraying、source routing、multi-plane failover、Clustermapper |
| UEC/UET/CSIG | 下一代 Ethernet AI/HPC transport | spec/早期实现 | transport、congestion signaling、telemetry primitives |
| ESUN/UALink | Scale-up Ethernet / accelerator pod | 2026 规范，2027 产品化 | 4-byte header、LLR、CBFC、memory-semantics-like fabric |

### 3.4 结合项目内 2026/2027 前十大 AI 芯片路线的软件放量判断

项目内《全球 AI 芯片路线图与 2026-2027 产能释放预测》列出的 2026-2027 主力平台包括 NVIDIA B300/GB300、AWS Trainium2/3、Google TPU Ironwood/TPU8、NVIDIA Rubin、AMD MI350/MI400、Microsoft Maia、Meta MTIA、OpenAI/Broadcom XPU、Huawei Ascend、Cambricon/Alibaba/Baidu 等。对网络软件的映射如下：

| 芯片/平台 | 网络背景 | 2026 软件路径 | 2027 软件路径 | 基准/乐观/极度乐观放量时间 |
|---|---|---|---|---|
| NVIDIA B300/GB300 | NVLink scale-up + InfiniBand/Spectrum-X scale-out | UFM/NMX/NetQ/Cumulus 是主路径；AI telemetry 与液冷/电力联动 | 继续作为存量最大底座，MRC/Spectrum-X 软件向 scale-out 扩散 | 基准：2026H2；乐观：2026Q2-Q3；极度乐观：GB300 rack 标准化使软件随整柜绑定 |
| NVIDIA Vera Rubin | NVLink 6、CX9、Spectrum-6、CPO、DSX | 2026H2 先在 hyperscaler 试点，DSX/NetQ/NMX 价值提升 | 2027 成为 premium AI factory 默认 stack | 基准：2027H1；乐观：2026Q4；极度乐观：2027 全年接近 GB300 ramp |
| AWS Trainium2/3 | EFA/自研网络 + Ethernet scale-out | AWS 内部软件为主，外部供应商机会小 | Trainium3/4 可能吸收更多 open Ethernet/NVLink Fusion 接口 | 基准：内部化；乐观：AWS 供应链服务外溢；极度乐观：EFA-like 能力行业化 |
| Google TPU Ironwood/TPU8 | Google Jupiter/Apollo OCS/光电混合 | 内部 NOS/telemetry 为主，外部受益在 Broadcom/OCS/光模块与测试 | OCS + all-optical fabric 的运维软件价值上升 | 基准：外部软件少；乐观：OCS telemetry 生态放量；极度乐观：Google 架构被更多 TPU-like ASIC 复制 |
| AMD MI350/MI400/Helios | Ethernet/UALink/UEC/SONiC/open rack | 2026 MI350 以标准 Ethernet 为主；Helios 早期认证 | 2027 MI400/Helios 是开放 scale-up Ethernet 最大催化 | 基准：2027H1；乐观：2026Q4；极度乐观：Meta/主权 AI 把 Helios 作为非 NVIDIA 标准 rack |
| Meta MTIA/OpenAI/Broadcom XPU | Broadcom switch/NIC + MRC/SONiC/SRv6 | 内部与 Broadcom/NVIDIA/Microsoft 协同，MRC 已公开 | 2027 custom ASIC + open Ethernet 会推动开放控制面 | 基准：2027；乐观：2026H2；极度乐观：MRC 迅速成为 OCP default |
| Microsoft Maia | Azure 内部网络 + SRv6/MRC 研究 | Microsoft 是 SONiC/MRC/SRv6 核心推动者 | Maia + OpenAI workloads 将推动 SRv6/telemetry 商品化 | 基准：Azure 内部；乐观：Nexus/SONiC 生态受益；极度乐观：MRC 成为 Azure AI backend 标准 |
| Huawei/Cambricon/Alibaba/Baidu | 国产 Ethernet/自研互连/超节点 | 国内 iMaster/NCE、H3C、Ruijie、SONiC 改造、国产 telemetry 放量 | 2027 国产超节点和主权 AI 集群复制 | 基准：中国本地软件生态；乐观：规模化替代；极度乐观：国产 AI 芯片出货超预期带来独立大市场 |

**结论：2026 最可能的路线不是“某个开源协议一统天下”，而是三层并行：**  
1. NVIDIA 闭环：NVLink/UFM/NMX/NetQ/DSX。  
2. Merchant Ethernet 闭源高可靠：Arista EOS/CloudVision、Cisco Nexus One/Nexus Dashboard、Nokia SR Linux/EDA、HPE/Juniper Apstra。  
3. 开放 Ethernet：SONiC/SAI + Broadcom/NVIDIA/Cisco/Marvell silicon + MRC/UEC/ESUN。

## 4. 课题二：已经开始放量的关键产品、市场规模、渗透率和利润率

说明：未来 3 个月指 2026-05 至 2026-07 的收入池；未来一年指 2026-05 至 2027-04；未来两年指 2028 年左右年化 run-rate。渗透率指在“新增 AI backend/AI factory fabric 项目”中的采用率，不含传统企业园区网络。

| 已放量产品/细分技术 | 代表公司/产品 | 当前状态 | 未来 3 个月市场规模 | 未来一年市场规模 | 未来两年 run-rate | 渗透率路径 | 增长情景 | 毛利/利润率情景 |
|---|---|---|---:|---:|---:|---|---|---|
| AI NOS 与交换机系统软件 | Arista EOS、NVIDIA Cumulus、Cisco NX-OS/Nexus One、Nokia SR Linux、Dell Enterprise SONiC、DriveNets DNOS、Arrcus ArcOS | 已随 400G/800G/1.6T switch 出货 | 基准 $0.9B-$1.5B；乐观 $1.5B-$2.3B；极度 $2.3B-$3.5B | $3.8B-$7.5B / $7B-$11B / $11B-$18B | $8B-$15B / $16B-$26B / $28B-$45B | 55%-70% -> 70%-85% -> 80%-90% | 基准 +35%-55%；乐观 +70%；极度 +100%+ | 纯软件 GM 75%-90%；嵌入系统综合 GM 45%-70%；经营利润率头部可 30%-50% |
| Fabric lifecycle / intent automation | NetQ、UFM、NMX、CloudVision、Nexus Dashboard/Hyperfabric、Apstra、Nokia EDA、Aviz ONES、Hedgehog | Day0/1/2 已成大型 AI 集群标配 | $0.45B-$0.8B / $0.8B-$1.3B / $1.3B-$2.0B | $1.8B-$3.8B / $3.5B-$6.5B / $6B-$10B | $4B-$8B / $8B-$14B / $15B-$26B | 25%-40% -> 45%-65% -> 65%-80% | 基准 +50%；乐观 +90%；极度 +130%+ | GM 70%-88%；若按 cluster/platform 打包，价格弹性高 |
| AI telemetry / network observability | NetQ、CV UNO/NetDL、UFM Telemetry、Splunk、ThousandEyes、Kentik、Datadog、Grafana、Gigamon、Riverbed、NETSCOUT | 从 NOC 工具升级为 GPU job 产能工具 | $0.35B-$0.7B / $0.7B-$1.2B / $1.2B-$2.0B | $1.5B-$3.2B / $3B-$5.5B / $5B-$9B | $4B-$8B / $8B-$15B / $16B-$30B | 20%-35% -> 40%-60% -> 65%-80% | 基准 +45%；乐观 +80%；极度 +120% | SaaS/软件 GM 75%-90%；但 telemetry ingest COGS 会压缩 5-15pct |
| Hardened SONiC / SAI commercial distro | Broadcom Enterprise SONiC、Nexthop hardened SONiC、Aviz、Hedgehog、Dell SONiC、Edgecore/Accton/Celestica/UfiSpace 生态 | Hyperscaler 成熟，enterprise/NeoCloud 正在产品化 | $0.15B-$0.35B / $0.35B-$0.65B / $0.65B-$1.0B | $0.8B-$2B / $2B-$4B / $4B-$7B | $3B-$6B / $6B-$12B / $12B-$22B | 25%-35% -> 35%-50% -> 45%-65% | 基准 +60%；乐观 +100%；极度 +180% | Subscription/support GM 55%-80%；服务占比高时 GM 40%-60% |
| RDMA/拥塞控制与 AI transport 软件 | Spectrum-X adaptive routing、Arista CLB/VOQ、Cisco G300/Nexus telemetry、Broadcom Cognitive Routing、MRC/SRv6 早期 | 2026 已在头部集群生产验证 | $0.3B-$0.8B / $0.8B-$1.5B / $1.5B-$2.5B | $1.5B-$4B / $4B-$8B / $8B-$14B | $5B-$11B / $11B-$22B / $22B-$38B | 高端 Ethernet AI 新建集群 15%-25% -> 35%-55% -> 60%-80% | 基准 +80%；乐观 +140%；极度 +220% | 若嵌入 silicon/NIC，silicon GM 55%-75%；软件/IP GM 80%-95% |
| InfiniBand/NVLink fabric 管理 | NVIDIA UFM、NMX、Mission Control、Base Command Manager | NVIDIA rack-scale 强绑定 | $0.4B-$0.9B / $0.9B-$1.5B / $1.5B-$2.3B | $2B-$4.5B / $4B-$7B / $7B-$11B | $4B-$8B / $8B-$14B / $14B-$22B | NVIDIA scale-up attach 80%-95%；全 AI fabric 30%-45% | 基准 +35%；乐观 +70%；极度 +110% | 绑定硬件和 enterprise support，GM 75%-90%，平台溢价强 |
| Digital twin / validation / pre-check | NVIDIA DSX Sim/Air、Apstra digital twin、Nokia EDA Digital Sandbox、Forward Networks、Batfish、Keysight/VIAVI 软件 | 设计验证先放量 | $0.2B-$0.45B / $0.45B-$0.8B / $0.8B-$1.2B | $0.8B-$1.8B / $1.8B-$3.5B / $3.5B-$6B | $2.5B-$5B / $5B-$10B / $10B-$18B | 8%-15% -> 20%-35% -> 40%-60% | 基准 +50%；乐观 +100%；极度 +180% | GM 75%-90%；专业服务/仿真资产包提升 ASP |
| Fabric 专业服务、认证、调优 | NVIDIA NCP/ERA、Cisco CVD、HPE/Juniper services、Arista TAC、Hedgehog/Aviz/DriveNets deployment | 供不应求，人才瓶颈明显 | $0.4B-$0.8B / $0.8B-$1.4B / $1.4B-$2.2B | $1.8B-$4B / $4B-$7B / $7B-$12B | $4B-$8B / $8B-$15B / $15B-$25B | 40%-60% -> 55%-75% -> 70%-85% | 基准 +35%；乐观 +70%；极度 +110% | 服务 GM 30%-55%；但与软件绑定可提高续费和锁定 |

### 4.1 已放量产品的利润率判断

| 情景 | 供需与定价 | 软件 GM | 经营利润率 | 解释 |
|---|---|---:|---:|---|
| 基准 | 800G/1.6T 硬件供应紧张但多厂商逐步进入；客户愿意为可靠性付费 | 70%-82% | 20%-40% | 研发、TAC、现场服务和 telemetry ingest 成本较高 |
| 乐观 | 大型 AI cluster 复制，软件按 GPU/cluster 订阅，premium telemetry 成为 RFP 必选 | 78%-88% | 35%-55% | 软件复用率提高，support 随客户规模摊薄 |
| 极度超预期乐观 | 100k-1M XPU 级集群使 job-aware fabric control 变成产能系统，软件参与收益分成或按 token/Watt 定价 | 85%-92% | 45%-65% | 软件成为“GPU 利用率保险”，定价可脱离传统 per switch 支持费 |

## 5. 课题三：在研关键产品与未来快速增长方向

| 在研/早期产品或技术 | 当前证据 | 未来 3 个月市场规模 | 未来一年市场规模 | 未来两年 run-rate | 渗透率路径 | 放量时间：基准/乐观/极度乐观 | 毛利率判断 |
|---|---|---:|---:|---:|---|---|---|
| MRC/SRv6 multipath RDMA | OpenAI 已生产部署并 OCP 公开；NVIDIA、AMD 同步支持 | $50M-$150M / $150M-$300M / $300M-$600M | $0.5B-$1.5B / $1.5B-$3.5B / $3.5B-$7B | $3B-$8B / $8B-$18B / $18B-$35B | <5% -> 15%-30% -> 40%-65% 高端 Ethernet AI fabric | 2027H1 / 2026Q4 / 2026H2 大客户标准化 | 协议本身开源，价值由 NIC/switch silicon、controller、support 捕获；GM 70%-90% |
| UEC UET / CSIG congestion telemetry | UEC 1.0 已发布，CSIG 规划中 | $30M-$100M / $100M-$250M / $250M-$500M | $0.4B-$1.2B / $1.2B-$3B / $3B-$6B | $3B-$7B / $7B-$15B / $15B-$28B | 5%-10% -> 20%-35% -> 45%-70% | 2027 / 2026H2 / 2026H2 伴随 Tomahawk6/Spectrum-X/Cisco G300 | 软件/IP/validation GM 80%+；硬件 feature 由 silicon 端变现 |
| ESUN / Scale-up Ethernet | OCP ESUN 1.0 2026-03 发布，175+ 公司参与 | <$50M / $50M-$150M / $150M-$300M | $0.3B-$0.9B / $0.9B-$2B / $2B-$4B | $3B-$8B / $8B-$16B / $16B-$30B | <1% -> 5%-15% -> 20%-45% | 2027H2 / 2027H1 / 2026Q4 with Helios/MTIA pilots | 初期稀缺，IP/NOS/controller GM 80%-90%；服务验证成本高 |
| UALink 2.0 / accelerator pod fabric | UALink 2.0 2026 发布，目标开放 scale-up accelerator interconnect | <$30M / <$100M / $100M-$250M | $0.2B-$0.6B / $0.6B-$1.5B / $1.5B-$3B | $2B-$5B / $5B-$12B / $12B-$24B | 0%-2% -> 3%-8% -> 15%-35% | 2027H2 / 2027H1 / 2026H2 lab-to-pilot | 高壁垒 IP 和验证工具 GM 80%+ |
| Agentic NetOps / closed-loop remediation | Arista AVA、Cisco AgenticOps、Nokia EDA AIOps、HPE Mist/OpsRamp、Aviz Copilot | $50M-$150M / $150M-$350M / $350M-$700M | $0.5B-$1.2B / $1.2B-$2.8B / $2.8B-$5B | $3B-$7B / $7B-$15B / $15B-$30B | 2%-5% -> 8%-18% -> 25%-45% | 2027 / 2026H2 / 2026H2 bounded automation | GM 80%-92%；安全/审计/回滚能力决定能否高价 |
| Inference fabric routing | Arrcus AINF + Dynamo、global model-aware routing、KV cache telemetry | <$50M / $50M-$150M / $150M-$300M | $0.3B-$1B / $1B-$2.5B / $2.5B-$5B | $2B-$6B / $6B-$14B / $14B-$25B | <1% -> 5%-12% -> 15%-35% | 2027H1 / 2026Q4 / 2026H2 premium inference | 若按 inference SLA/token cost 定价，GM 80%-90% |
| CPO/OCS/optical telemetry OS | NVIDIA Spectrum-X Photonics、Google Apollo OCS、CPX/XPO/CMIS telemetry | $50M-$200M / $200M-$500M / $500M-$900M | $0.6B-$1.8B / $1.8B-$4B / $4B-$8B | $4B-$10B / $10B-$22B / $22B-$40B | 3%-8% -> 15%-30% -> 35%-60% | 2027 / 2026H2 / 2026H2 high-end AI switch | 硅光/系统软件高毛利，但 field service 风险大 |
| Open Data Center for AI telemetry/security | OCP Open DC for AI 2026 推进，接口含 network/power/cooling/security/telemetry | <$100M / $100M-$250M / $250M-$500M | $0.5B-$1.5B / $1.5B-$3B / $3B-$6B | $4B-$8B / $8B-$16B / $16B-$30B | 5%-10% -> 20%-40% -> 50%-75% | 2027 / 2026Q4 / 2026Q3 RFP 写入 | 标准免费，认证/测试/平台集成 GM 60%-85% |

## 6. 课题四：供给侧、产能结构、瓶颈、成本与毛利

### 6.1 产能结构

| 产能类型 | 主要地区 | 主要公司/组织 | 关键工艺/能力 |
|---|---|---|---|
| NOS 与控制面软件研发 | 美国湾区、西雅图、以色列、印度、芬兰、加拿大、中国深圳/杭州/北京 | NVIDIA/Mellanox、Arista、Cisco、Broadcom、HPE/Juniper、Nokia、Microsoft、Google、AWS、Meta、DriveNets、Arrcus、Hedgehog、Aviz、Huawei/H3C | 分布式系统、Linux NOS、ASIC SDK、RDMA、telemetry data plane、control-plane scale |
| ASIC SDK/SAI/firmware | 美国、以色列、印度、台湾 | Broadcom、NVIDIA、Cisco、Marvell、AMD Pensando、Intel、Nexthop | SDK、SAI、P4-like pipeline、packet trimming、telemetry counters、firmware |
| 白盒/交换机 ODM 集成 | 台湾、中国大陆、泰国、马来西亚、墨西哥 | Accton/Edgecore、Celestica、UfiSpace、Quanta、Wiwynn、Delta、Inventec、Foxconn、WNC、Alpha Networks | 800G/1.6T switch validation、SONiC porting、thermal、optics compatibility |
| 商业化 SONiC / 开放 fabric | 美国、以色列、印度、台湾 | Broadcom Enterprise SONiC、Nexthop、Aviz、Hedgehog、Dell、Edgecore、Celestica、PLVision | SONiC hardening、feature backport、gNMI/OpenConfig、TAC、certification |
| Observability/AIOps | 美国、以色列、欧洲、印度 | Cisco Splunk/ThousandEyes、Datadog、Dynatrace/Bindplane、Grafana Labs、Kentik、Gigamon、Riverbed、NETSCOUT、Selector AI、Augtera | telemetry pipeline、AI RCA、data lake、packet broker、LLM assistant |
| 数字孪生/验证 | 美国、加拿大、欧洲、印度 | NVIDIA DSX/Air、Apstra、Nokia EDA、Forward Networks、Batfish/Intentionet、Keysight、VIAVI、Anritsu | pre-check/post-check、topology simulation、traffic validation、compliance |

### 6.2 供给瓶颈

1. **AI fabric 专家稀缺**：懂 GPU collective、RoCE/IB、switch ASIC、Linux NOS、telemetry data engineering 的工程师很少。2026 最短缺的不是普通网工，而是能把 NCCL/all-reduce slow job 映射到 PFC/ECN/NIC/switch/optic 的系统工程师。
2. **大规模验证环境稀缺**：10k-100k GPU 级别的问题无法靠小 lab 复现。供应商即使代码成熟，也需要客户真实流量验证，认证周期可达 3-9 个月。
3. **ASIC SDK 与 firmware 交付节奏**：Tomahawk/Spectrum/Silicon One/Marvell/Thor/Pensando 等 feature 需要 SDK、SAI、firmware 同步。硬件 ready 不代表 NOS ready。
4. **光模块与 CMIS telemetry 互操作**：800G/1.6T 光模块供应商多，DSP/LPO/TRO/FR4/DR8 组合复杂。温度、误码、FEC、lane degradation、retimer 状态需要统一采集。
5. **Telemetry ingest 成本**：AI fabric 想要秒级/毫秒级观测，但 observability 平台按 ingest/retention 收费，客户会出现“数据越多越贵”的反弹。
6. **安全与变更审计**：AgenticOps 若能自动改配置，必须有权限边界、审批、回滚、proof of correctness；否则客户只敢用作聊天式查询。
7. **多厂商责任边界**：slow job 可能来自 GPU、NIC、switch、optic、storage、scheduler 或 application。没有 end-to-end contract 时，各厂商容易互相甩锅。
8. **现场交付与 runbook**：AI network 调优与液冷、电力、rack 上线同时发生，网络软件商需要现场/远程联动，服务产能会限制收入确认。

### 6.3 成本构成与毛利决定因素

以一个 100k GPU/XPU AI Ethernet 集群为例，网络硬件、光模块、NIC 和布线可能是 $0.6B-$1.5B；AI Fabric 软件与服务首年可达 $45M-$155M，极度乐观的 outcome-based 定价可达 $150M-$300M。

| 成本/价格项 | 占软件合同的比例 | 毛利含义 |
|---|---:|---|
| NOS license/support | 20%-35% | 高毛利、续费强；若随硬件打包则披露不透明 |
| Fabric manager / controller | 15%-30% | 可按 switch/port/GPU/site 定价，毛利高 |
| Telemetry/observability data pipeline | 10%-25% | 云端 ingest/storage 成本会压低毛利；本地部署毛利高但服务重 |
| Digital twin / validation | 5%-15% | 高毛利软件 + 仿真资产/专业服务 |
| Deployment/professional service | 15%-30% | 人力瓶颈，毛利 30%-55%，但帮助锁定长期订阅 |
| 24x7 TAC / premium support | 10%-20% | 稳定续费，客户越大越依赖 |

**毛利决定因素**：  
1. 是否能和硬件 reference design 绑定；  
2. 是否能证明 GPU utilization/job completion time 改善；  
3. telemetry 数据成本是否可控；  
4. 自动化是否从建议走到可执行；  
5. 是否是大客户标准化栈的一部分；  
6. 是否掌握 ASIC/NIC 私有 counters 与 firmware feature。

**价格传导机制**：  
HBM/GPU/光模块短缺会推高 AI rack ASP，客户更重视 uptime 和调优，软件定价反而更容易上调。相反，当 800G/1.6T 硬件 commoditize，硬件毛利下行，厂商会把利润迁移到 CloudVision/NetQ/Apstra/EDA/Nexus Dashboard/SONiC support 等订阅与服务。

## 7. 课题五：竞争格局、壁垒与价值捕获

### 7.1 市场结构

| 层级 | 集中度判断 | 头部 |
|---|---|---|
| NVIDIA 闭环 AI fabric | CR1 极高 | NVIDIA：NVLink、InfiniBand、Spectrum-X、Cumulus、NetQ、UFM、NMX、DSX |
| Merchant Ethernet NOS/管理软件 | CR5 约 65%-80% | Arista、Cisco、HPE/Juniper、Nokia、Dell/SONiC、Broadcom ecosystem |
| 开放 SONiC/whitebox 支持 | 分散但头部上升 | Broadcom/Nexthop、Aviz、Hedgehog、Dell、Edgecore/Accton、Celestica、UfiSpace |
| Hyperscaler 内部栈 | 内部化最高 | Microsoft SONiC/MRC/SRv6、Google Jupiter/Apollo、AWS EFA/SRD、Meta FBOSS/ESUN、OpenAI MRC/Clustermapper |
| Observability/AIOps | 更分散 | Cisco Splunk/ThousandEyes、Datadog、Dynatrace、Grafana、Kentik、Gigamon、Riverbed、NETSCOUT、Selector AI |

### 7.2 壁垒清单：为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| 大规模生产验证 | 是否跑过 10k/50k/100k GPU 级别 job | AI 网络 bug 只有在大规模同步训练中暴露，未验证产品风险极高 |
| ASIC/NIC 私有 telemetry | 是否能读到 packet trimming、ECN/CNP、queue occupancy、port health、GPU/NIC correlation | 只看 SNMP/generic counters 无法定位 slow job；私有 counters 是护城河 |
| 客户锁定与运维习惯 | EOS/CloudVision、Nexus、NetQ/UFM、Apstra 等续费率 | 网络团队 runbook、CI/CD、TAC、脚本都绑定平台，切换成本高 |
| 变更安全与 rollback | 是否支持 digital twin、pre-check、post-check、intent diff、instant rollback | AI 集群停机损失巨大，客户愿为低风险变更付费 |
| 多厂商认证 | 支持多少 switch/NIC/optic/GPU/storage 组合 | AI factory 是拼装系统，认证矩阵越大越有采购优势 |
| 人才与 TAC | 24x7 支持、P1 响应、现场调优能力 | 大客户买的是“出事有人负责”，不是单纯代码 |
| 标准影响力 | OCP/UEC/UALink/SONiC/OpenConfig 贡献度 | 能提前定义 feature，就能提前拿 design win |

### 7.3 价值捕获：哪一层最可能长期高 ROIC/高毛利

1. **第一梯队：掌握硬件 + NOS + telemetry + controller 的平台型公司**  
NVIDIA、Arista、Cisco、HPE/Juniper、Nokia。原因是它们能把硬件、软件、TAC、reference design 打包，客户采购路径短，故障责任清晰。

2. **第二梯队：控制 ASIC/NIC feature 与 SDK 的 silicon 平台**  
Broadcom、NVIDIA、Cisco、Marvell、AMD Pensando。AI transport 的关键能力越来越下沉到 NIC/switch silicon，但需要软件暴露。长期毛利由 silicon + software feature 一起捕获。

3. **第三梯队：hardened SONiC/open fabric 专业软件商**  
Aviz、Hedgehog、Arrcus、DriveNets、Nexthop。它们不一定最大，但如果开放 Ethernet/SONiC 在 NeoCloud、主权 AI、AMD Helios、custom ASIC 中扩散，会有很高收入弹性。

4. **第四梯队：observability/data pipeline 与 AIOps**  
Splunk、Datadog、Dynatrace、Grafana、Kentik、Gigamon、Riverbed、NETSCOUT、Selector AI。长期空间大，但必须接入真实 network/GPU/NIC counters，否则容易沦为通用仪表盘。

**最优投资暴露不是单纯“开源 SONiC”，而是“能把开源、多厂商硬件和生产级 support 合成一个可审计、可回滚、可调优系统的公司”。**

## 8. 课题六：2026 关键变化与最可能放量子方向

### 8.1 2026 三个最大拐点

1. **MRC/SRv6 从 OpenAI 生产环境走向 OCP 公开规格**  
这是 2026 年最重要的软件事件。它证明 AI backend 网络的核心竞争点不只是 800G/1.6T 端口，而是 multi-plane、packet spraying、source routing、failure bypass 和高频 probe/telemetry。

2. **AI telemetry 从“网络可观测”升级到“GPU job 可观测”**  
NVIDIA Spectrum-X telemetry、Arista CloudVision/CV UNO、Cisco Nexus Dashboard、Nokia EDA、Arrcus AINF 都在把 network counters 和 GPU/NIC/workload 状态绑定。2026 年客户采购会从“买交换机”变成“买可证明 job completion time 的 fabric”。

3. **Open Ethernet/SONiC/ESUN 成为第二生态**  
NVIDIA 闭环仍强，但 AMD Helios、Meta/OpenAI/Microsoft ASIC、Broadcom Tomahawk6/Thor Ultra、OCP ESUN 让开放 Ethernet 成为可投资主线。2026 最先受益的是 SONiC hardening、SAI、validation、TAC 和 automation。

### 8.2 2026 最可能放量子方向

| 排名 | 子方向 | 为什么 2026 放量 |
|---:|---|---|
| 1 | NetQ/UFM/NMX/CloudVision/Nexus Dashboard/Apstra/EDA 这类 fabric assurance | GB300、800G、1.6T、NeoCloud 上线压力大，客户必须买可视化和自动化 |
| 2 | Hardened SONiC + whitebox AI fabric | 客户想降低 NVIDIA/单一 OEM 锁定，Broadcom/Celestica/Accton/UfiSpace/Hedgehog/Aviz 形成供给 |
| 3 | RDMA/拥塞控制 telemetry | PFC storm、ECN/CNP、packet loss、slow node 是 AI backend 最大运维痛点 |
| 4 | Digital twin/pre-check/post-check | 100k GPU 集群不能靠人工 CLI 改配置，变更验证刚需 |
| 5 | AI inference routing | Agentic inference、多区域推理和 KV cache 让网络路由进入应用层 |

## 9. 课题七：2027 关键变化与最可能放量子方向

### 9.1 2027 三个最大拐点

1. **1.6T + MRC/UEC/ESUN 进入主流 AI Ethernet fabric**  
2026 是规格和头部部署，2027 是交换芯片、NIC、NOS、controller、TAC、OCP reference design 一起放量。

2. **Scale-up Ethernet/UALink/ESUN 让非 NVIDIA rack-scale 平台产品化**  
AMD MI400/Helios、Meta MTIA、OpenAI/Broadcom、Microsoft Maia 等 custom ASIC 都需要可替代 NVLink 的开放 fabric。软件机会在 scale-up fabric controller、telemetry、memory-like semantics validation。

3. **Agentic NetOps 从聊天助手变成受控自动运维**  
2026 大多数 AIOps 还是 query/RCA；2027 若能做到自动隔离坏链路、调 ECN/PFC、回滚配置、重排 job，客户会按 avoided downtime 和 utilization uplift 付费。

### 9.2 2027 最可能放量子方向

| 排名 | 子方向 | 2027 收入弹性 |
|---:|---|---|
| 1 | MRC/SRv6/UEC transport software 与 silicon feature enablement | 高端 Ethernet AI fabric attach rate 可能从 <10% 跳到 35%+ |
| 2 | Scale-up Ethernet / UALink / ESUN fabric management | AMD/ASIC rack 的非 NVIDIA 替代路线成型 |
| 3 | CPO/OCS/optical telemetry | 1.6T/CPO/OCS 让光层从 dumb optics 变成可管理对象 |
| 4 | Closed-loop AIOps | 大型集群人力跟不上，自动化从效率工具变成准入门槛 |
| 5 | Cross-DC scale-across fabric | OpenAI/Stargate、Microsoft、Google、Meta 多园区 AI factory 需要跨站点训练/推理网络 |

## 10. 课题八：头部公司与细分技术清单

### 10.1 闭源/平台型 AI Fabric 软件

| 公司 | 关键产品 | 优势 |
|---|---|---|
| NVIDIA | Cumulus Linux、SONiC support、NetQ、UFM、NMX、Mission Control、DSX、DOCA、Spectrum-X | GPU/NIC/switch/NVLink/IB 全栈遥测，AI factory reference design 最完整 |
| Arista | EOS、CloudVision、CV UNO、NetDL、AVA、Etherlink、CLB | EOS 稳定性、state database、CloudVision 运维体验、hyperscaler 客户强 |
| Cisco | NX-OS、Nexus One、Nexus Dashboard、Nexus Hyperfabric、AgenticOps、Splunk/ThousandEyes | Enterprise/NeoCloud AI POD、Silicon One、security/observability 联动 |
| HPE/Juniper | Apstra Data Center Director、Mist AI、OpsRamp、Junos、QFX/PTX | Intent-based networking、HPE server/storage/channel、Juniper data center fabric |
| Nokia | SR Linux、EDA、Digital Sandbox、SONiC support | Model-driven SR Linux、Kubernetes-native EDA、主权云/电信云可信度 |
| Dell | Enterprise SONiC、SmartFabric、OpenManage/PowerSwitch | 企业渠道、SONiC 产品化、服务器/存储集成 |
| Huawei | CloudEngine、iMaster NCE、AI Fabric、CloudMatrix 网络软件 | 中国国产替代、政企/运营商渠道、软硬件一体 |
| H3C / Ruijie / ZTE | AD-NET/SeerFabric、数据中心交换与控制软件 | 中国云/运营商/政企本土生态 |

### 10.2 开放 NOS、SONiC、whitebox 与软件初创

| 公司/组织 | 技术/产品 | 位置 |
|---|---|---|
| Microsoft / Linux Foundation / SONiC Foundation | SONiC、SAI、gNMI/OpenConfig、Azure production experience | 开源 NOS 基础 |
| Broadcom | SDK、SAI、Enterprise SONiC、Tomahawk/Jericho/Thor feature | 开放 Ethernet silicon 与 SONiC 生态核心 |
| Nexthop AI | Hardened SONiC + Broadcom CPO/Tomahawk systems | Hyperscaler/open AI networking |
| Aviz Networks | ONES、Network Copilot、Packet Broker、SONiC support | 商业化 SONiC 与 network observability |
| Hedgehog | Cloud-native fabric software、SONiC/Kubernetes API、Spectrum-X/Celestica support | NeoCloud/open AI cluster |
| DriveNets | DNOS、DN-SONiC、Network Cloud-AI | Disaggregated routing 与 AI backend fabric |
| Arrcus | ArcOS、ACE-AI、AINF、NVIDIA Dynamo/BlueField/Spectrum integration | Distributed inference fabric 与 open NOS |
| Pica8 / AmpCon | Commercial open networking NOS/automation | Enterprise open networking |
| Edgecore/Accton、Celestica、UfiSpace、Quanta、Wiwynn、Delta、Inventec、Foxconn、WNC | Open switches, 800G/1.6T/CPO systems, SONiC integration | 白盒/ODM 产能 |

### 10.3 Telemetry、observability、AIOps、数字孪生

| 公司/项目 | 产品/技术 | AI Fabric 相关性 |
|---|---|---|
| Cisco Splunk / ThousandEyes | Observability、安全、跨域 telemetry | Cisco AI fabric 的软件抓手 |
| Datadog | Infrastructure/network observability | 可接入 AI cluster metrics，但需 deeper network counters |
| Dynatrace / Bindplane | Open telemetry pipeline 与 AI observability | telemetry cost control 与治理 |
| Grafana Labs / Prometheus / OpenTelemetry | 开源 telemetry 标准与 dashboard | AI fabric 自建 observability 的事实基础 |
| Kentik | Network observability / flow analytics | 流量与路径可视化 |
| Gigamon | Deep observability pipeline / packet broker | network-derived telemetry 与安全可见性 |
| Riverbed / NETSCOUT | Network observability, packet/flow analytics | 高保真网络数据与故障分析 |
| Forward Networks | Network digital twin / verification | 变更验证、路径证明、合规 |
| Batfish / Intentionet | Open-source network verification | 大规模配置验证 |
| Selector AI / Augtera | AI for network operations | 告警降噪、RCA、事件关联 |
| Keysight / VIAVI / Anritsu / Teledyne LeCroy | 1.6T/3.2T/PCIe/以太网测试软件 | 认证、validation、fabric acceptance |

### 10.4 Hyperscaler 内部栈

| 公司 | 内部技术 | 外部影响 |
|---|---|---|
| Microsoft | SONiC、MRC/SRv6、Azure AI backend、Fairwater | 开源 SONiC 与 SRv6/MRC 行业扩散 |
| OpenAI | MRC、Clustermapper、Stargate/OCI/Fairwater supercomputer networking | 训练网络最佳实践外溢 |
| Google | Jupiter fabric、Apollo OCS、TPU pod telemetry | OCS/光交换与内部网络软件路线 |
| AWS | EFA/SRD、Trainium networking、Nitro telemetry | 内部化强，但会影响行业对低延迟网络的需求定义 |
| Meta | FBOSS、OCP、ESUN、MTIA fabric | OCP/open rack/open Ethernet 推动者 |
| Oracle/OCI | OpenAI/GB200/MRC/AI supercluster | 大规模部署与 cloud reference customer |
| Alibaba/Tencent/ByteDance/Baidu | 自研 AI cluster network、国产交换/SONiC 改造 | 中国 AI fabric 软件生态 |

## 11. 情景模型：2026-2028 收入与渗透率

### 11.1 总市场

| 指标 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 AI networking/optical global order pool | $65B-$100B | $105B-$165B | $165B-$260B |
| 软件/支持/服务 attach rate | 8%-12% | 11%-16% | 15%-22% |
| 2026 AI Fabric 软件收入池 | $7B-$11B | $11B-$17B | $18B-$28B |
| 2027 AI networking/optical global order pool | $100B-$160B | $170B-$280B | $280B-$430B |
| 2027 软件/支持/服务 attach rate | 10%-15% | 14%-20% | 20%-28% |
| 2027 AI Fabric 软件收入池 | $14B-$24B | $25B-$40B | $45B-$70B |

### 11.2 关键假设

| 假设 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---|---|
| GPU/XPU 出货 | GB300 主力，Rubin/MI400/TPU8 2026 尾端 | Rubin/Helios/ASIC 2026Q4 起贡献 | 2027 需求前置，多个 100k XPU cluster 同时上电 |
| Ethernet vs InfiniBand | NVIDIA 闭环与 Ethernet 并行 | Ethernet 在新建 backend 中加速 | Open Ethernet/MRC/UEC 成为高端新建默认路径 |
| 软件定价 | per switch/port/support | per cluster/GPU/fabric subscription | outcome-based，按 utilization/token/Watt 分享价值 |
| 客户预算 | 软件是网络硬件附属 | 软件是上线和 SLA 必选 | 软件是 AI factory revenue control plane |

## 12. 投资跟踪指标

1. NVIDIA networking revenue、Spectrum-X attach rate、NetQ/UFM/NMX/DSX 客户数。
2. Arista AI networking target 是否继续上调；CloudVision/CV UNO/AVA 的软件订阅披露。
3. Cisco AI infrastructure orders 转收入节奏；Nexus One、Hyperfabric、Splunk telemetry 是否绑定 AI POD。
4. Broadcom AI networking 在 AI revenue 中占比；Tomahawk6/Thor Ultra/Jericho4、SONiC/SAI 认证进度。
5. OpenAI/Microsoft/OCP MRC 是否进入非 OpenAI 大客户；MRC 是否被 NIC/switch 默认支持。
6. OCP ESUN/UEC/UALink specification 的 silicon support 和 compliance test。
7. Hedgehog、Aviz、Arrcus、DriveNets 是否拿到 NeoCloud/主权 AI/AMD Helios design win。
8. Telemetry 成本：客户是否从 Datadog/Splunk ingest 转向本地 OTel/Grafana/自建 pipeline。
9. AI cluster slow-job RCA 时间：是否从小时/天降到分钟级。
10. 1.6T switch/optics/CPO/OCS 的 telemetry 数据模型是否标准化。

## 13. 主要风险

1. AI 推理收入兑现低于预期，导致 hyperscaler 推迟 2027 capex。
2. 800G/1.6T 硬件价格战提前，压低随硬件打包的软件价值。
3. 开源 SONiC commoditize，商业 distro 无法证明 premium support 价值。
4. Agentic NetOps 发生安全事故，自动化从执行退回建议模式。
5. MRC/UEC/ESUN 标准分裂，客户继续自研闭源实现。
6. GPU/HBM/电力/液冷瓶颈使 AI network 软件订单延迟确认。
7. 大客户内部化过强，外部软件商只能拿低毛利服务收入。

## 14. 主要来源

| 来源 | 用途 |
|---|---|
| [OpenAI：Supercomputer networking to accelerate large scale AI training](https://openai.com/index/mrc-supercomputer-networking/) | MRC/SRv6、GB200 supercomputer、OCI Abilene、Microsoft Fairwater、OCP 公开规格 |
| [OpenAI PDF：Resilient AI Supercomputer Networking using MRC and SRv6](https://cdn.openai.com/pdf/resilient-ai-supercomputer-networking-using-mrc-and-srv6.pdf) | MRC multi-plane、Clustermapper、GB200/CX8、Broadcom Tomahawk5 等实验配置 |
| [NVIDIA：Spectrum-X with MRC](https://blogs.nvidia.com/blog/spectrum-x-ethernet-mrc/) | Spectrum-X、MRC、deep telemetry、intelligent fabric control |
| [NVIDIA：Next-generation AI Factory Telemetry with Spectrum-X](https://developer.nvidia.com/blog/next-generation-ai-factory-telemetry-with-nvidia-spectrum-x-ethernet/) | Switch/SuperNIC/GPU/NetQ telemetry、OpenTelemetry、gNMI |
| [NVIDIA：Vera Rubin DSX reference design](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-Vera-Rubin-DSX-AI-Factory-Reference-Design-and-Omniverse-DSX-Digital-Twin-Blueprint-With-Broad-Industry-Support/default.aspx) | DSX、AI factory digital twin、network/power/cooling/controls |
| [NVIDIA NetQ](https://www.nvidia.com/en-us/networking/ethernet-switching/netq/) | NetQ 功能与 AI factory 网络运维 |
| [NVIDIA UFM management software](https://www.nvidia.com/en-us/networking/management-software/) | InfiniBand fabric management 与 telemetry |
| [Arista Q1 2026 financial results](https://www.arista.com/en/company/news/press-release/24017-pr-20260505) | Q1 收入、operating margin、XPO、AI Spine |
| [Arista CloudVision](https://www.arista.com/en/eos/eos-cloudvision) | EOS/CloudVision automation 与 telemetry |
| [Arista-Broadcom AI Networking Solution Brief](https://www.arista.com/assets/data/pdf/Datasheets/Arista-Broadcom-AI-Networking-Solution-Brief.pdf) | CloudVision、AI Agent、NIC/EOS 统一视图 |
| [Cisco Q2 FY2026 earnings](https://investor.cisco.com/news/news-details/2026/CISCO-REPORTS-SECOND-QUARTER-EARNINGS/default.aspx) | Cisco revenue、AI infrastructure orders、Networking growth |
| [Cisco Nexus Hyperfabric AI](https://www.cisco.com/site/us/en/products/networking/data-center-networking/nexus-hyperfabric/hyperfabric-ai/index.html) | Cloud-managed AI infrastructure、Nexus Hyperfabric |
| [Cisco N9000 with Nexus One for AI](https://www.cisco.com/c/en/us/products/collateral/networking/cloud-networking-switches/nexus-9000-switches/nexus-9000-ai-networking-aag.html) | Silicon One G300、microsecond telemetry、job-level insights |
| [Broadcom Q1 FY2026 SEC exhibit](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm) | Broadcom AI revenue、Q2 guide、AI networking |
| [Broadcom Tomahawk 6](https://investors.broadcom.com/news-releases/news-release-details/broadcom-ships-tomahawk-6-worlds-first-1024-tbps-switch) | 102.4T、Cognitive Routing、high-resolution telemetry、SONiC |
| [Broadcom OFC 2026 AI infrastructure](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai) | 3.5D XPU、102.4T CPO switch、400G/lane DSP、retimer/AEC |
| [OCP ESUN 1.0](https://www.opencompute.org/blog/the-ocp-esun-10-specification-has-been-released) | ESUN header、lossless Ethernet、175+ companies |
| [Ultra Ethernet Consortium](https://ultraethernet.org/) | UEC goals：scale、bandwidth density、multipathing、fast congestion response |
| [UALink 2.0 specification PR](https://ualinkconsortium.org/wp-content/uploads/2026/04/UALink-2.0-Specification-PR_FINAL.pdf) | UALink 2.0 和开放 scale-up accelerator interconnect |
| [Nokia EDA](https://www.nokia.com/data-center-networks/data-center-fabric/event-driven-automation/) | EDA、AIOps、telemetry/topology/change correlation |
| [Nokia Data Center Fabric](https://www.nokia.com/networks/solutions/data-center-fabric/) | SR Linux、EDA、AI fabric automation |
| [Arrcus AINF + NVIDIA Dynamo](https://arrcus.com/news/arrcus-inference-network-fabric-ainf-announces-integration-with-nvidia) | Inference fabric、queue depth、KV cache pressure、replica health |
| [DriveNets AI Networking](https://drivenets.com/solutions/ai-networking/) | DNOS/DN-SONiC、AI fabric |
| [Hedgehog OCP EMEA 2026](https://hedgehog.cloud/ocp-emea-summit-2026) | Celestica DS5000/DS6000、open 800G/1.6T AI fabric |
| [SONiC 202505 release](https://sonicfoundation.dev/sonic-202505-powering-ai-fabrics-and-enterprise-networks-with-precision-and-insight/) | SONiC telemetry、AI backend fabric、enterprise features |
| [IDC Ethernet switch market 4Q25](https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/) | Data center Ethernet switch revenue +63%、800G revenue share |
| [Dell'Oro via PRNewswire：AI back-end switch >$100B by 2030](https://www.prnewswire.com/news-releases/ai-back-end-switch-market-will-push-past-100-billion-by-2030-according-to-delloro-group-302678344.html) | AI backend switch 长期市场校验 |
| [Appledore：Network Automation Software 2026-2030](https://appledoreresearch.com/report/network-automation-software-nas-market-forecast-2026-2030/) | 网络自动化软件 $7.1B 2026 到 $11.7B 2030 的外部校验 |
| [Broadcom 2026 State of Network Operations](https://networkobservability.broadcom.com/hubfs/ESD/ESD_Microsites/AOD_Microsites_FY26/AOD_Microsites_FY26_Network%20Observability/AOD_Microsites_FY26_Network%20Observability_Files/Broadcom-2026-State-of-Network-Operations-Report.pdf) | 网络可见性与 AI ops 需求校验 |

## 15. 最后判断

2026 的 AI Fabric 网络软件最像 2010 年代云数据中心里的 Kubernetes/observability/CI-CD：一开始被看作工具，最后变成生产系统。区别在于，AI 工厂的单位资产更贵、停机损失更大、网络 tail latency 对收益更直接，因此商业化会更快。

最值得优先跟踪的投资线索是：

1. **NVIDIA/Arista/Cisco/HPE-Juniper/Nokia 的平台软件 attach rate**：这些是最确定的高毛利。
2. **Broadcom + SONiC + whitebox + OCP 的开放 Ethernet 生态**：这是弹性最大的第二曲线。
3. **MRC/UEC/ESUN/UALink 的协议软件与验证工具**：这是 2027 的技术拐点。
4. **job-aware telemetry 与 Agentic NetOps**：这是从硬件订单走向长期订阅的关键。
5. **inference fabric routing**：如果 agentic inference 继续爆发，网络控制面会进入应用层，软件估值应按 AI 平台软件而不是传统网络管理工具定价。

在极度乐观情景下，AI Fabric 软件会成为 AI 数据中心除 GPU/HBM/光互联之外最好的“高毛利小票”：硬件订单越大、集群越复杂、客户越害怕浪费 GPU，网络操作系统与遥测软件的定价权越强。
# 行业调研：【AI以太网交换系统与Fabric芯片】

> 版本日期：2026-05-08  
> 研究口径：本报告聚焦 AI 数据中心后端网络、scale-up/scale-out/scale-across fabric、交换 ASIC、AI NIC/DPU/SuperNIC、PCIe/CXL/UALink fabric switch、光/铜互联与网络软件栈。市场规模采用“订单和可收入化硬件池”混合口径，部分光模块、NIC、线缆和交换机系统之间存在 BOM 重叠，表格不可简单相加。  
> 情景口径：基准、乐观、极度超预期乐观。用户要求对 2026 年 AI 基础设施建设抱有乐观预期，因此本报告的“基准”不是衰退情景，而是“供应链有摩擦但需求仍强”的正增长情景。

## 0. 高浓度结论

**一句话：2026 年 AI 以太网交换系统的核心机会不是“以太网替代 InfiniBand”这一个故事，而是 Ethernet 正在同时吃掉 scale-out、侵入 scale-up、扩展到 scale-across，并把交换 ASIC、NIC/DPU、CPO/1.6T 光、224G 铜、PCIe/CXL fabric switch 和网络软件一起重估。**

关键数字锚点：

| 事实 | 数字 | 投资含义 |
|---|---:|---|
| IDC 预计全球 AI infrastructure spending | 2025 年 $318B，2026 年 $487B，2029 年 >$1T | 网络和 fabric 是 GPU 利用率的放大器，AI 基建总盘子足以支撑网络收入池翻倍 |
| TrendForce 最新 CSP CapEx 口径 | 2026 年全球 Top 9 CSP CapEx 约 $830B，年增 79% | 对 2026 网络订单采用乐观上沿更合理，尤其 Meta、Google、AWS、Microsoft、Oracle、ByteDance |
| Gartner 半导体口径 | 2026 年全球半导体收入 >$1.3T，AI 半导体约占 30% | AI 网络 silicon、SerDes、DSP、retimer 不再是边角料，而是 AI 半导体高毛利组成 |
| Dell'Oro AI back-end switch | 2030 年 AI back-end switch market >$100B | 交换系统是独立大赛道，不只是服务器 BOM 配件 |
| Dell'Oro 2025 AI 后端网络 | Ethernet switch sales 超过 InfiniBand 两倍以上，AI cluster switch sales 占比 >2/3 | 2026 以太网已是 scale-out 主流，争议从“能不能用”变成“谁的 fabric 更好” |
| Broadcom Q1 FY2026 AI revenue | $8.4B，同比 +106%；Q2 AI semiconductor 指引 $10.7B | custom XPU + AI networking 同时爆发，Broadcom 是以太网 fabric silicon 最大受益层之一 |
| Broadcom Tomahawk 6 | 102.4Tb/s，224G SerDes，已 production volume | 102.4T 从样片进入收入化，2026H2 到 2027 是 1.6T 交换平台拐点 |
| NVIDIA Spectrum-X / Spectrum-6 | Rubin 体系集成 Spectrum-6 Ethernet、CPO，Spectrum-X Photonics 最高 409.6Tb/s | NVIDIA 不只是卖 GPU，也在把 Ethernet 做成自家 AI factory 控制平面 |
| Cisco Silicon One G300 | N9000/8000 系统支持 51.2T/102.4T，总端口 800G/1.6T | Cisco 用自研 ASIC + optics + AgenticOps 重返 AI 数据中心网络 |
| Arista Q1 2026 | 收入 $2.709B，同比 +35.1%；2026 AI fabrics 目标上调至 $3.5B | Arista 证明 Ethernet AI fabric 已可规模化变现，软件和客户锁定抬高价值 |
| OFC 2026 光互联 | Cignal AI 估计 2025 光组件近 $25B，400G+ 模块 4,200 万只，1.6T 2026 快速增长 | 800G/1.6T 光模块和交换系统同步上量，光瓶颈会反过来决定交换机交付 |

本报告对 2026-2027 的核心判断：

1. **2026 最确定的技术路径：800G Ethernet/RoCE + 51.2T/102.4T switch ASIC + 400G/800G NIC + 短距 DAC/AEC + 800G 光模块。** 1.6T 在 2026H2 开始收入化，但全年主收入仍来自 800G。
2. **2027 最可能的放量路径：1.6T Ethernet + 102.4T/204.8T 系统 + UEC/ESUN/UALink 早期产品 + CPO/CPX 小规模生产。** 3.2T/400G-per-lane 更像 2028 的主流收入，但 2027 会提前锁设计和测试设备订单。
3. **价值捕获最高的层：交换 ASIC、NIC/DPU/Fabric switch silicon、fabric 软件/遥测、CPO/ELS/高速 SerDes。** 交换机整箱也能赚钱，但白盒/ODM 组装毛利低，长期高 ROIC 更可能在 silicon + software + standards control。
4. **最大的 2026 风险不是需求，而是供应链和上线节奏：224G SerDes 良率、CPO 可靠性、800G/1.6T 光模块、AEC 线缆、液冷、电力、客户认证和系统 burn-in。**

## 1. AI 芯片路线图背景下的行业机遇、挑战和技术路径

### 1.1 为什么 2026 会成为 AI Ethernet 和 fabric 芯片的大年

本项目已有 AI 芯片路线图显示，2026-2027 年初出货价值最高的计算平台包括 NVIDIA B300/GB300、AWS Trainium2/3、Google Ironwood TPU、NVIDIA GB200/B200、Huawei Ascend 910C/950、AMD MI350/MI400、Meta MTIA、Microsoft Maia 200、OpenAI/Broadcom custom accelerator 等。它们的共同特征是：

| 芯片/平台 | 2026 主网络路径 | 对交换系统和 fabric 芯片的拉动 |
|---|---|---|
| NVIDIA GB300/B300 | rack 内 NVLink/NVSwitch 铜互联，scale-out 用 Spectrum-X Ethernet/InfiniBand，800G 主流，1.6T 导入 | 每个 NVL72 rack 需要高密度 scale-out 端口，NVIDIA 自家 Spectrum-X、ConnectX/BlueField 和 CPO 份额提高 |
| NVIDIA Rubin/Vera Rubin | NVLink 6 + ConnectX-9 + BlueField-4 + Spectrum-6 Ethernet + CPO | 2026H2 进入 Rubin 体系，2027 拉动 102.4T/409.6T 光交换系统和 CPO |
| Google Ironwood TPU / TPU8 | TPU 内部 ICI/3D Torus，短距高速铜，rack 间 OCS + 800G/1.6T 光 | OCS、800G+ 光模块、光纤管理、低功耗 fabric 受益，传统电交换部分价值被重分配 |
| AWS Trainium2/3 | NeuronLink/NeuronSwitch + EFA/Ethernet scale-out | Ethernet NIC、fabric management、短距铜和 hyperscaler 自研网络软件受益 |
| AMD MI350/MI400 Helios | UALink/UALoE scale-up，Pensando NIC，Ultra Ethernet scale-out，HPE/Celestica/Broadcom switch | 开放 Ethernet scale-up 的最大商业化实验，推动 UALink、Tomahawk Ultra、Tomahawk 6、Vulcano NIC |
| Meta MTIA | Broadcom XPU + Ethernet scale-up/out/across，FBOSS/OCP | Broadcom high-radix switch、optical connectivity、custom XPU 网络 IP 和 OCP switch ecosystem 受益 |
| OpenAI/Broadcom custom accelerator | Broadcom racks，Ethernet/PCIe/optical connectivity，2026H2 开始，10GW 至 2029 | 直接把 custom accelerator 与 Broadcom Ethernet fabric 绑定，是 merchant AI fabric 的大订单锚 |
| Microsoft Maia 200 | Azure 内部 scale-up/network，Ethernet/RoCE + 液冷 rack | Azure 自研 fabric、800G/1.6T 光、DPU/SmartNIC、液冷网络设备受益 |

**结论：2026 年最可能的主技术路径不是单一路线，而是“封闭 scale-up + 开放 scale-out”的混合。** NVIDIA 平台继续用 NVLink/NVSwitch 做 rack 内高带宽，Ethernet 负责 scale-out 和客户可运维性。非 NVIDIA 平台则用 UALink/ESUN/PCIe/CXL 等开放 scale-up 路线争夺 rack 内互联，同时用 UEC/RoCE/以太网做后端网络。

### 1.2 当前正在使用的关键技术

| 技术 | 2026 使用状态 | 成熟度 | 主要公司 |
|---|---|---:|---|
| RoCEv2 over Ethernet | 大规模使用，是 Meta、Arista、Cisco、Broadcom、NVIDIA Spectrum-X 等共同基础 | 高 | Arista、NVIDIA、Cisco、Broadcom、Meta FBOSS、SONiC 生态 |
| 800G Ethernet AI fabric | 2025 已主流，2026 是收入主力 | 高 | Arista 7060X6/Etherlink、NVIDIA Spectrum-X800、Cisco Nexus/8000、Broadcom TH5/TH6 白盒 |
| 51.2T switch ASIC | 64x800G 或 128x400G 主流平台 | 高 | Broadcom Tomahawk 5、NVIDIA Spectrum-4、Cisco G200 |
| 102.4T switch ASIC | 2026 进入 production volume 和系统导入 | 中高 | Broadcom Tomahawk 6、Cisco G300、NVIDIA Spectrum-6 |
| 400G/800G AI NIC/SuperNIC/DPU | 训练集群标配，2026 800G NIC 进入高端 | 高 | NVIDIA ConnectX/BlueField、Broadcom Thor Ultra、AMD Pensando、Intel、Marvell |
| DAC/AEC/ACC 高速铜 | rack 内和短距主力，112G 已成熟，224G 导入 | 高到中高 | Amphenol、TE、Molex、Credo、MaxLinear、Broadcom、Marvell |
| PCIe 5/6 retimer 与 fabric switch | AI 服务器内和开放 fabric 增长快，Astera 进入 320-lane switch | 中高 | Astera、Broadcom、Microchip、XConn、Montage、Marvell |
| InfiniBand / NVLink / NVSwitch | NVIDIA 训练与 rack 内 scale-up 强势，scale-out 份额被 Ethernet 挤压 | 高 | NVIDIA/Mellanox |
| UEC | 1.0/1.0.2 规格发布，产品化进入 2026-2027 | 中 | UEC 成员，Broadcom、AMD、Cisco、Arista、HPE、NVIDIA、Meta 等 |
| UALink / UALoE | 1.0 已定义 200G per lane、最多 1024 accelerators，2.0 规格已发布，2026 设计导入 | 中 | AMD、Intel、Broadcom、HPE、Celestica、Astera、Synopsys/Cadence IP |
| CPO/CPX/NPO/ELS | 2026 从 demo 到 pilot，NVIDIA/Broadcom 明确推 | 中低到中 | NVIDIA、Broadcom、Coherent、Lumentum、Marvell、Ciena、Molex、Samtec |
| OCS 光电路交换 | Google TPU/Ironwood 体系领先，其他客户观察 | 中 | Google、MEMS OCS 厂商、Coherent/Calient/Polatis 等 |

### 1.3 新技术成熟和放量时间：三情景

| 技术 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|
| 800G Ethernet AI fabric | 已成熟，2026 是收入主力，2027 仍大量存在 | 2026 客户从 InfiniBand 更快迁移，800G 订单延续到 2027 | 2026 新建训练集群几乎默认 Ethernet scale-out |
| 1.6T Ethernet | 2026H2 早期出货，2027 成为高端新增默认之一 | 2027H1 大客户批量采用，全年 1.6T 端口占新增高端端口 30-45% | 2027 1.6T 成为新增 AI 集群默认，短缺持续到 2028 |
| 102.4T switch ASIC | 2026 production volume，2027 大规模系统化 | 2026H2 进入多家 OEM/白盒，2027 快速替代 51.2T | 2026H2 供应仍被预定，102.4T 系统溢价维持 |
| 204.8T / 3.2T-ready switching | 2026 设计验证，2027 demo/小批量，2028 放量 | 2027H2 形成早期收入，2028H1 扩大 | 2027 就出现 $10B 级订单池，收入大头仍在 2028 |
| CPO/CPX/NPO | 2026-2027 pilot，收入先在 ELS/optical engine，2028+ 放量 | 2027 进入少数高端 AI cluster 标准 BOM | 2027 高端 102.4T/204.8T switch 默认采用 CPO/CPX，CPO 收入曲线前移 |
| UEC | 2026 规格和软件栈，2027 进入采购清单 | 2026H2 多家 NIC/switch 宣称 UEC-compliant，2027 规模化 | UEC 成为云厂异构 AI fabric 的事实标准，InfiniBand 溢价被明显压缩 |
| UALink / UALoE / ESUN | 2026 设计导入，AMD Helios 等首批平台；2027 小规模生产 | 2027 非 NVIDIA rack 大量采用，scale-up Ethernet 证明可用 | 2027 多家 hyperscaler 同时采用，开放 scale-up fabric TAM 被重估 |
| PCIe/CXL fabric switch | 2026 Scorpio/PCIe Gen6 切入少数 AI racks，2027 扩大 | 2027 成为 custom ASIC rack 和内存池化关键 BOM | PCIe/CXL/UALink 融合，fabric switch 获得类似 Ethernet switch 的战略估值 |
| OCS | 2026 Google/TPU-like 体系为主，2027 扩散有限 | 2027 Meta/Microsoft/Anthropic 部分跟进 | OCS 被 GPU Ethernet fabric 吸收，光交换成为 AI network power bottleneck 解法 |
| OCI MSA 光 scale-up | 2026 规格和样品，2027 评估 | 2027 进入多个平台的工程样机和少量量产 | 2027 optical scale-up 替代部分铜，2028 进入高端 rack 默认路径 |

### 1.4 2026 最可能的技术路径

按出货确定性排序：

1. **800G Ethernet scale-out fabric：** 51.2T/102.4T switch ASIC，RoCE/UEC-compatible transport，400/800G NIC，800G 光模块。
2. **NVIDIA proprietary scale-up + Ethernet scale-out：** GB200/GB300/NVL72 rack 内 NVLink/NVSwitch，rack 间 Spectrum-X/InfiniBand。Meta 2026 与 NVIDIA 的公告已经把 Spectrum-X 纳入大规模基础设施。
3. **Broadcom merchant Ethernet fabric：** Tomahawk 6、Tomahawk Ultra、Jericho 4、Thor Ultra NIC、Sian/Agera DSP/retimer 和 PCIe Gen6 产品组成端到端 portfolio。
4. **Arista/Cisco/HPE/Celestica 等系统化 AI Ethernet：** Arista Etherlink、Cisco G300/N9000/8000、HPE Juniper + Broadcom、Celestica Helios switch。
5. **PCIe/CXL/UALink fabric switch：** 2026 收入小于 Ethernet switch，但增速和毛利最像早期高壁垒芯片赛道。

## 2. 已开始放量的关键产品：市场规模、渗透率和利润率

### 2.1 总收入池判断

| 收入池，口径说明 | 未来 3 个月 | 未来 12 个月 | 未来 24 个月 | 基准增速 | 乐观增速 | 极度乐观增速 |
|---|---:|---:|---:|---:|---:|---:|
| AI 网络与 fabric 总订单池，交换机、NIC、光/铜、部分软件，可能与系统 BOM 重叠 | $18-30B | $75-120B | $140-240B | 40-60% | 70-100% | 120%+ |
| AI back-end 交换系统，箱体/机框/白盒，不含大部分光模块 | $7-12B | $30-50B | $55-100B | 45-65% | 75-100% | 120%+ |
| 交换 ASIC 和 fabric silicon，含 Ethernet switch ASIC、NIC/DPU、PCIe/CXL fabric switch | $5-9B | $22-38B | $45-85B | 45-70% | 80-110% | 130%+ |
| 光互联，800G/1.6T/CPO/scale-across | $9-16B | $38-70B | $75-145B | 50-70% | 80-110% | 140%+ |
| 铜互联、AEC、retimer、连接器 | $3-6B | $12-22B | $22-45B | 30-50% | 55-80% | 100%+ |

解释：Dell'Oro 给出 AI back-end switch market 到 2030 年超过 $100B 的方向性锚；本报告将 2026-2027 的 AI 网络订单池抬高，是因为 TrendForce 将 2026 Top 9 CSP CapEx 上修至 $830B，且 OpenAI、Meta、Anthropic、Google、AWS、Oracle 等 GW 级项目会提前锁网络和光互联供应。

### 2.2 已放量产品三情景表

| 已放量产品 | 当前状态和公开事实 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 800G AI Ethernet 交换系统 | Dell'Oro 称 2025 年 AI 后端 Ethernet 已超过 InfiniBand 两倍以上；Arista、NVIDIA、Cisco、Broadcom 白盒均放量 | 基准 $6-9B；乐观 $8-12B；极度 $11-16B | 基准 $25-38B；乐观 $36-55B；极度 $50-75B | 基准 $38-62B；乐观 $60-95B；极度 $90-140B | 2026 新增 AI Ethernet 端口 60-75%；2027 因 1.6T 切入降至 45-60%，但绝对量继续增 |
| 51.2T/102.4T switch ASIC | Broadcom Tomahawk 5/6、NVIDIA Spectrum-4/6、Cisco G200/G300；Tomahawk 6 已 production volume | $1.8-3.5B / $3-5B / $5-8B | $8-15B / $15-25B / $25-40B | $18-35B / $35-60B / $60-100B | 51.2T 2026 仍大，102.4T 在 2026H2 切入，2027 高端新增容量 35-60% |
| AI NIC/SuperNIC/DPU，400G/800G | NVIDIA ConnectX/BlueField、Broadcom Thor Ultra、AMD Pensando、Intel、Marvell；800G NIC 进入高端 | $2-4B / $3-5B / $5-7B | $9-16B / $15-24B / $22-35B | $16-30B / $28-50B / $45-75B | Ethernet AI 服务器 attach rate 从 2026 的 1-2 张/节点走向 2027 的更高端口密度 |
| NVIDIA NVLink/NVSwitch/InfiniBand fabric | GB200/GB300/NVL72 仍用 proprietary scale-up，InfiniBand 在高端训练保留，但 scale-out 份额下滑 | $4-8B / $6-10B / $9-14B | $18-35B / $28-48B / $40-70B | $25-55B / $45-85B / $70-120B | NVIDIA rack 内 scale-up 渗透 80%+，scale-out 中 Ethernet 份额提高 |
| PCIe/CXL retimer、fabric switch、smart cable silicon | Astera Scorpio 320-lane AI scale-up switch 已 shipping；PCIe Gen6 retimer/switch 进入 AI BOM | $0.8-1.6B / $1.2-2.4B / $2-3.5B | $4-8B / $7-12B / $10-18B | $9-20B / $16-32B / $28-55B | 2026 先在少数高端 rack，2027 成为 custom ASIC 和开放 rack 的关键 BOM |
| DAC/AEC/ACC 高速铜互联 | 112G 放量，224G 开始导入；TE、Molex、Amphenol、Credo、MaxLinear 均推 224G/1.6T 方案 | $2-4B / $3-5B / $4.5-7B | $9-16B / $14-24B / $22-35B | $15-30B / $25-48B / $40-75B | rack 内和短距仍以铜为主，2026-2027 50-75% 短距链路由 DAC/AEC/ACC 承担 |
| AI fabric 软件、遥测和运维 | Arista EOS/CloudVision、Cisco Nexus One、NVIDIA DOCA/Cumulus、SONiC/FBOSS；客户锁定增强 | $0.7-1.5B / $1.2-2.2B / $2-3.5B | $4-8B / $7-12B / $10-18B | $9-22B / $18-35B / $30-55B | 大型 AI cluster 2026 约 50-70% 需要专用 telemetry/congestion tuning，2027 上升 |

### 2.3 已放量产品利润率预测

| 产品 | 当前利润率判断，毛利率为主 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|---:|
| 交换 ASIC | 高端 fabless silicon 毛利通常 60-75%；Broadcom AI 半导体供不应求，整体 adjusted EBITDA 68% | 65-72% | 70-76% | 73-80% |
| AI 交换系统，品牌厂 | Arista Q4 2025 GAAP GM 62.9%，Q1 2026 收入高增；Cisco 混合毛利高，NVIDIA 系统溢价高 | 45-62% | 52-65% | 58-68% |
| AI 交换系统，ODM/白盒 | Celestica、Accton、Fabrinet 等更偏制造，毛利显著低 | 10-20% | 12-24% | 15-28% |
| AI NIC/DPU/SuperNIC | silicon + firmware + software，定价能力高 | 55-70% | 60-75% | 65-78% |
| PCIe/CXL fabric switch/retimer | Astera Q1 2026 GAAP GM 76.3%，供给紧张时可维持高位 | 65-74% | 70-77% | 73-80% |
| AEC/DAC/连接器 | 材料和组装占比高，但 224G/1.6T 初期有溢价 | 22-38% | 30-45% | 35-50% |
| 网络软件/遥测/运维 | 软件毛利高，实际收入常嵌入系统和订阅 | 70-85% | 78-90% | 82-92% |

## 3. 在研和即将快速增长的关键产品

### 3.1 在研产品和放量路径

| 在研/早期产品 | 当前状态 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 1.6T Ethernet 交换系统 | OFC 2026 已进入多厂商展示和早期产品；Cisco G300、Broadcom TH6、NVIDIA Spectrum-6 对齐 1.6T | $0.8-2B / $1.5-4B / $3-7B | $7-18B / $15-35B / $30-55B | $35-90B / $70-140B / $120-220B | 2026 高端新增端口 <15%；2027 20-45%；2028 45-70% |
| CPO/CPX/NPO/ELS 交换光引擎 | NVIDIA Spectrum-X Photonics、Broadcom Davisson、Open CPX MSA、Coherent/Lumentum ELS | $0.05-0.2B / $0.1-0.4B / $0.3-0.8B | $0.8-2B / $2-5B / $5-10B | $4-12B / $10-25B / $20-45B | 2026 高端 switch <2%；2027 3-10%；2028 10-30% |
| UALink/ESUN/UALoE scale-up Ethernet switch | UALink 2.0 规格发布；AMD Helios、HPE/Celestica/Broadcom 路径明确 | <$0.2B / $0.2-0.5B / $0.5-1B | $1-5B / $4-10B / $8-18B | $10-35B / $25-65B / $55-120B | 非 NVIDIA rack scale-up：2026 <5%，2027 10-30%，2028 25-55% |
| OCI MSA optical scale-up | 2026 年 AMD、Broadcom、Meta、Microsoft、NVIDIA、OpenAI 成立 OCI MSA | <$0.05B / $0.05-0.15B / $0.1-0.3B | $0.2-1B / $0.8-3B / $2-6B | $3-15B / $10-35B / $25-70B | 2027 主要是工程样机和头部客户，2028 开始进入标准 BOM |
| OCS 光电路交换 | Google Apollo/TPU 体系领先，MEMS 光交换节能显著 | $0.1-0.4B / $0.3-0.8B / $0.6-1.5B | $0.8-3B / $2-6B / $5-12B | $5-18B / $12-35B / $30-75B | TPU-like 架构 2026 已导入，GPU Ethernet fabric 2027-2028 扩散 |
| 3.2T/400G-per-lane 和 204.8T switching | Broadcom Taurus、OpenLight 3.2T PIC、Coherent 400G/lane，2026 样品为主 | <$0.1B / $0.1-0.3B / $0.3-0.8B | $0.3-2B / $1.5-6B / $5-12B | $6-25B / $18-55B / $45-110B | 2027 设计导入，2028 高端 switch 规模化 |
| PCIe over optics / optical-aware retimer | PCIe 6.4/7.0 optical-aware retimer 进入标准路径，2026 DevCon 强调 | <$0.1B / $0.1-0.3B / $0.3-0.8B | $0.5-2B / $1.5-5B / $4-10B | $4-15B / $12-35B / $30-80B | 2026 qualification，2027 小量，2028 进入跨 rack/pod |
| AI fabric digital twin、自动化调优 | NVIDIA DSX、Arista AVA、Cisco AgenticOps、SONiC/FBOSS 自动化 | $0.3-1B / $0.8-2B / $1.5-4B | $2-6B / $5-12B / $10-22B | $8-25B / $20-50B / $45-90B | 2026 绑定大客户项目，2027 开始平台化订阅 |

### 3.2 在研产品利润率预测

| 产品 | 利润率逻辑 | 基准 | 乐观 | 极度超预期乐观 |
|---|---|---:|---:|---:|
| 1.6T 交换系统 | 初期端口稀缺，系统和光模块联动，价格下行会滞后 | 系统 35-55%；ASIC 65-73% | 系统 45-62%；ASIC 70-76% | 系统 55-68%；ASIC 75-80% |
| CPO/CPX/NPO/ELS | 早期良率和服务成本拖累，但 ELS/optical engine 稀缺 | 25-45% | 35-60% | 50-70% |
| UALink/ESUN switch | 开放 scale-up 如果验证成功，switch silicon 议价能力极强 | 55-70% | 65-78% | 70-82% |
| OCI optical scale-up | 标准未定，早期 NRE 高，关键光引擎/IP 溢价高 | 30-50% | 45-65% | 55-75% |
| OCS | MEMS/光纤管理/运维软件组合，云厂自研会压价 | 30-48% | 40-58% | 50-68% |
| 3.2T/400G lane | 早期稀缺器件、DSP 和测试设备毛利高，模块良率压低系统毛利 | 35-55% | 45-65% | 55-75% |
| PCIe over optics | silicon + optics + compliance，若成为事实标准毛利上修 | 40-60% | 55-72% | 65-80% |
| AI fabric automation/software | 软件、遥测、调优和仿真毛利高 | 70-85% | 80-90% | 85-93% |

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/产品 |
|---|---|---|---|
| 高端交换 ASIC / NIC / DPU | 美国设计，台湾代工，部分韩国/美国替代 | Broadcom、NVIDIA、Cisco、Marvell、AMD Pensando、Intel、Astera、Credo | 5nm/4nm/3nm/2nm，112G/224G SerDes，800G/1.6T NIC，PCIe Gen6 fabric |
| 高端封装和基板 | 台湾、日本、韩国、中国大陆、东南亚 | TSMC、ASE、Amkor、Ibiden、Unimicron、Nanya PCB、Shinko、欣兴、景硕 | CoWoS/SoIC、FCBGA、ABF、高速 PCB |
| 交换机系统和白盒 | 台湾、泰国、马来西亚、墨西哥、美国 | Arista、Cisco、NVIDIA、Celestica、Accton/Edgecore、Foxconn、Quanta、Wistron、Jabil、HPE、Dell | 51.2T/102.4T switch，800G/1.6T ports，液冷/风冷机箱 |
| 光模块和光组件 | 中国、泰国、马来西亚、美国、日本、台湾 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、AOI、Fabrinet、Accelink、Source Photonics、Hisense | 800G/1.6T OSFP/QSFP-DD，EML、VCSEL、SiPh、InP laser |
| 光 DSP / coherent / silicon photonics | 美国、台湾、以色列、日本、欧洲 | Broadcom、Marvell、Cisco/Acacia、NVIDIA、Intel、Coherent、OpenLight、Ayar Labs、Lightmatter、TSMC、GF、Tower | 5nm/3nm/2nm DSP，SiPh PIC，CPO optical engine |
| 铜线缆/连接器/AEC | 美国、中国、台湾、东南亚、墨西哥 | Amphenol、TE、Molex、Samtec、Luxshare、BizLink、Credo、MaxLinear、MACOM | 112G/224G DAC/AEC/ACC，OSFP/QSFP-DD，near-chip connector |
| 测试与认证 | 美国、日本、欧洲、台湾 | Keysight、VIAVI、Anritsu、Tektronix、Teledyne LeCroy、Spirent、Teradyne、Advantest | 224G SerDes、1.6T/3.2T MAC/FEC、PCIe Gen6/7 compliance、光电测试 |

### 4.2 至少 5 条供给瓶颈

1. **224G SerDes 和封装信号完整性。** 102.4T switch、1.6T NIC 和 3.2T 光模块都需要 224G/400G lane 路线，BER、FEC、jitter、crosstalk、散热和可重复测试难度极高。
2. **高端 switch ASIC wafer 和先进封装。** 交换 ASIC 不像 GPU 那样消耗 HBM，但 die 面积、SerDes 数量、封装基板和高速 PCB 难度很高，TSMC/封装/ABF 同样受 AI accelerator 挤压。
3. **800G/1.6T 光模块和关键器件。** 200G/400G EML/EAM/MZM、SiPh PIC、InP laser、DSP、isolator/filter、FAU 和测试时间成为短缺点。
4. **CPO 可维护性和良率。** CPO 不只是把光放到 ASIC 旁边，还要解决 ELS 冗余、field replacement、热漂移、光纤管理、socket 标准、失效率和运维责任边界。
5. **高速铜线缆和连接器。** 224G AEC/DAC 不只是铜价问题，线径、插损、热、弯折半径、连接器一致性和机柜布线都会限制 rack 级交付。
6. **客户认证和系统级 burn-in。** AI fabric 需要在真实训练/推理集群验证 tail latency、拥塞、packet loss、collective operation、链路 flap，认证周期可达 2-4 个季度。
7. **网络软件和人才。** RoCE/UEC/UALink/ESUN 的真正价值在 congestion control、telemetry、job scheduler、failure recovery 和运维工具，顶级网络架构师是稀缺资源。
8. **液冷和电力约束。** 高密度 switch、CPO、800G/1.6T optics 和 AI rack 同时提高功耗，机房供电、冷板/CDU、漏液检测和 rack cable management 会影响网络设备上线。

### 4.3 成本构成和毛利决定因素

| 产品 | BOM 或单位成本拆分，估算 | 毛利决定因素 |
|---|---|---|
| 800G/1.6T 交换机系统 | switch ASIC 25-40%；PCB/backplane 10-18%；电源/散热 10-18%；光模块若随箱销售可达 30-50%；组装/测试 5-10%；软件支持 5-15% | ASIC allocation、端口速率代际、软件订阅、客户认证、是否绑定光模块 |
| 高端 switch ASIC | wafer/die 25-40%；封装/基板 15-25%；SerDes/IP/NRE 摊销 20-35%；测试 5-12%；SDK/firmware 5-10% | 224G SerDes 可用性、radix、功耗、SDK 粘性、客户设计周期 |
| NIC/DPU/SuperNIC | ASIC 35-50%；board/PHY/retimer 15-25%；光/电接口 15-25%；firmware/软件 5-15%；测试 5-10% | GPU 利用率提升能力、telemetry、storage/security offload、与交换机协同 |
| AEC/DAC/ACC | 铜缆和连接器 30-55%；retimer/linear IC 20-40%；组装 10-20%；测试 10-20% | 224G 量产良率、线缆长度、客户认证、模块替代比例 |
| CPO/CPX/ELS | photonic engine 25-40%；switch ASIC/package 25-35%；ELS/laser 15-25%；fiber/socket/thermal 10-20%；测试 10-20% | ELS 冗余和寿命、现场维护模型、CPO 标准化、多供应商生态 |

### 4.4 价格传导机制

| 供需状态 | 价格如何传导 |
|---|---|
| ASIC/光模块短缺 | switch silicon 和 optics 通过 LTA、capacity reservation、expedite fee 直接传给 hyperscaler，ODM 只保留低毛利 |
| 新代际导入前 6-12 个月 | 1.6T、102.4T、224G、CPO 等可以获得高 ASP 和更高毛利，客户为上电时间付溢价 |
| 多供应商认证完成后 | 模块和白盒 ASP 快速下行，价值回到 silicon、软件、客户锁定和运维效率 |
| 客户自研网络软件 | 压低白盒硬件毛利，但提高被认证 ASIC/SDK 的长期粘性 |
| 电力/液冷限制 | 即使硬件供给足，客户上线慢会造成收入确认延迟，订单不一定取消，但交付节奏后移 |

## 5. 竞争格局与壁垒

### 5.1 市场结构和头部集中度

| 层级 | 集中度判断 | 主要玩家 |
|---|---|---|
| 交换 ASIC | 高集中，Broadcom 和 NVIDIA 最强，Cisco 自用自研，Marvell/Intel/国内厂商局部 | Broadcom Tomahawk/Jericho/Thor，NVIDIA Spectrum/Quantum，Cisco Silicon One，Marvell，Intel/Barefoot，Huawei |
| AI 交换系统 | 中高集中，Arista、NVIDIA、Cisco、Celestica/白盒、HPE/Juniper 争夺 | Arista、NVIDIA、Cisco、Celestica、HPE Networking、Accton/Edgecore、Dell、Supermicro、Nokia |
| NIC/DPU/SuperNIC | 高集中，NVIDIA、Broadcom、AMD Pensando、Intel、Marvell | NVIDIA ConnectX/BlueField，Broadcom Thor，AMD Pensando，Intel IPU/NIC，Marvell OCTEON |
| PCIe/CXL fabric switch | 早期高集中，Astera 快速领先，Broadcom/Microchip/XConn/Montage 参与 | Astera、Broadcom、Microchip、XConn、Montage、Marvell、Rambus/Synopsys IP |
| 光模块 | 头部集中但竞争激烈，中美供应链都强 | Innolight、Eoptolink、Coherent、Lumentum、Fabrinet、AOI、Accelink、Source Photonics、Hisense、Broadex |
| 高速铜和连接器 | 高端较集中，客户认证强 | Amphenol、TE、Molex、Samtec、Luxshare、BizLink、Credo、MaxLinear |
| 网络软件 | 强锁定，商业 NOS 与云厂自研并存 | Arista EOS、Cisco NX-OS/Nexus One、NVIDIA DOCA/Cumulus、SONiC、FBOSS、Arrcus、DriveNets、Aviz |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 为什么能定价 | 可观察指标 |
|---|---|---|
| 224G/400G SerDes | 速度越高，能稳定跑、低功耗跑、批量测试跑的供应商越少 | port error rate、功耗/port、客户 qual 时间、SerDes IP 复用度 |
| 高 radix 和低延迟 | AI collective 通信需要高 radix、低 tail latency，不只是吞吐 | radix、hop count、JCT 改善、microburst 下 packet loss |
| 拥塞控制和遥测 | RoCE/UEC 的性能靠端到端调优，软件决定 GPU 利用率 | GPU utilization、P99/P999 latency、retransmission、flow-level telemetry |
| 客户认证 | 一个 AI fabric 失败会让数万 GPU 空转，客户倾向用已验证方案 | hyperscaler design win 数、qual 周期、bug burn-down |
| 生态锁定 | GPU/NIC/switch/DPU/NOS/SDK 一起工作，替换单点会带来系统风险 | NVIDIA Spectrum-X + ConnectX + DOCA，Arista EOS，Cisco Nexus One |
| 供应链锁定 | 102.4T ASIC、1.6T 光、224G AEC 的产能提前被锁 | LTA、capacity prepayment、lead time |
| 现场运维和可维护性 | 大规模 AI 网络的故障定位和替换成本高，运维工具可收费 | MTTR、link flap rate、自动恢复、digital twin |
| 标准参与权 | UEC/UALink/ESUN/OCI 等标准影响接口定义和产业利润分配 | 规格贡献、首批产品、interop demo、生态成员数 |

### 5.3 长期高 ROIC 和高毛利层

按长期价值捕获排序：

1. **交换 ASIC 和 fabric silicon：Broadcom、NVIDIA、Cisco Silicon One、Astera。** 这是最高壁垒层，SerDes、SDK、客户 qual 和供应链锁定共同定价。
2. **NIC/DPU/SuperNIC：NVIDIA、Broadcom、AMD Pensando、Marvell。** 它控制主机侧网络、storage/security offload、telemetry 和 congestion loop，直接影响 GPU 利用率。
3. **网络软件和运维平台：Arista、Cisco、NVIDIA、SONiC/FBOSS 服务生态。** 毛利最高，客户切换成本大，但云厂自研会压低外部收费。
4. **CPO/ELS/光 DSP/SiPh：Broadcom、Marvell、Coherent、Lumentum、Cisco/Acacia、OpenLight、Ayar。** 2026-2027 绝对收入较小，但一旦 CPO 标准化，弹性很大。
5. **品牌交换系统：Arista、Cisco、NVIDIA、HPE。** 高端品牌和软件可有较高毛利，但白盒化会压缩硬件箱体利润。
6. **ODM/EMS 和普通光模块组装：Celestica、Accton、Fabrinet 等。** 收入弹性大，利润率低于 silicon/software，但供不应求阶段也有上修空间。

## 6. 2026 关键变化：三个最可能拐点

### 拐点 1：Ethernet 成为 AI scale-out 默认，争议转向 scale-up

Dell'Oro 已经给出 2025 年 AI 后端 Ethernet 超过 InfiniBand 两倍以上的市场信号。2026 年，主流问题不再是“Ethernet 能不能跑大模型训练”，而是“Ethernet 能不能进一步进入 rack 内 scale-up”。UEC 1.0/1.0.2、OCP ESUN、UALink/UALoE 都是这个问题的标准化答案。

最可能放量子方向：800G Ethernet、102.4T switch、800G NIC、Arista/Cisco/NVIDIA/Broadcom AI fabric。

### 拐点 2：102.4T 和 1.6T 进入生产窗口

Broadcom Tomahawk 6 已 production volume，Cisco G300 指向 102.4T，NVIDIA Spectrum-6 随 Rubin 进入 2026H2 生态。1.6T 光模块和 102.4T switch 是同一个代际切换，2026H2 的订单和客户认证比收入更重要。

最可能放量子方向：102.4T switch ASIC、1.6T OSFP/LPO/LRO/TRO、224G AEC、1.6T NIC/SuperNIC。

### 拐点 3：custom ASIC/GW 订单把开放 fabric 从标准推向产品

OpenAI/Broadcom 10GW、Meta/Broadcom 1GW 起步并走向多 GW、Anthropic/AWS up to 5GW、Anthropic/Google/Broadcom 2027 多 GW，这些订单会需要非 NVIDIA 以太网 fabric。AMD Helios、HPE/Celestica/Broadcom 的 UALoE switch 是 2026 最值得跟踪的开放 scale-up 样板。

最可能放量子方向：Broadcom Tomahawk Ultra/Jericho/Thor，AMD Pensando Vulcano，UALink/ESUN switch，PCIe/CXL fabric switch。

## 7. 2027 关键变化：三个最可能拐点

### 拐点 1：1.6T 成为 AI 后端网络主收入驱动

2026 仍是 800G 主导，2027 新增高端 AI cluster 会更大比例采用 1.6T。若光模块和 102.4T switch 供应链顺利，1.6T 会从“头部客户项目”变成“高端默认配置”。

最可能放量子方向：1.6T switch systems、102.4T/204.8T platforms、1.6T NIC、1.6T coherent DCI。

### 拐点 2：开放 scale-up fabric 进入真实采购

Rubin/GB300 继续由 NVIDIA NVLink 主导，但 AMD Helios、Meta MTIA、OpenAI/Broadcom、Google TPU、AWS Trainium 需要更多开放 fabric。2027 是 UALink/UALoE/ESUN 从规格和样机进入生产采购的关键年。

最可能放量子方向：UALink switch、Tomahawk Ultra、PCIe/CXL fabric switch、OCI MSA optical scale-up。

### 拐点 3：CPO/OCS/scale-across 从 pilot 进入局部生产

CPO 不会在 2027 全面替代 pluggable，但高端 switch 功耗和光纤密度会迫使一部分平台采用 CPO/CPX/ELS。与此同时，Google OCS、NVIDIA Spectrum-XGS、Marvell/Ciena/Nokia 1.6T coherent 会让 scale-across 成为 AI network 第三增长层。

最可能放量子方向：CPO optical engine、ELS、OCS、1600ZR/ZR+、multi-rail line system、AI fabric digital twin。

## 8. 头部公司和细分领域公司全景清单

### 8.1 交换 ASIC 和 Ethernet fabric silicon

| 子领域 | 公司 |
|---|---|
| Merchant switch ASIC | Broadcom Tomahawk/Jericho/Tomahawk Ultra、NVIDIA Spectrum、Cisco Silicon One、Marvell、Intel/Barefoot、Huawei、H3C/新华三生态 |
| AI scale-up Ethernet | Broadcom Tomahawk Ultra、Cisco G300/G200、NVIDIA Spectrum-6、AMD/HPE/Celestica UALoE、OCP ESUN 生态 |
| Deep-buffer / routed fabric | Broadcom Jericho、Cisco Silicon One P/G 系列、Nokia/HPE/Cisco/Arista routed AI fabric |
| Domestic China | Huawei CloudEngine/昇腾网络、H3C、Ruijie、盛科通信、云豹智能、篆芯等本土网络芯片或系统生态 |

### 8.2 交换系统、白盒和集成

| 子领域 | 公司 |
|---|---|
| AI Ethernet branded switch | Arista、Cisco、NVIDIA、HPE Networking/Juniper、Nokia、Dell、Supermicro、Lenovo |
| Whitebox/ODM/OEM | Celestica、Accton/Edgecore、Foxconn/FIT、Quanta、Wistron、Inventec、Jabil、Delta、UfiSpace |
| Cloud self-designed switch | Meta FBOSS/Minipack/Wedge、Microsoft SONiC、Google、AWS、Oracle、ByteDance、Tencent、Alibaba、Baidu |
| Network OS and automation | Arista EOS/CloudVision/AVA、Cisco NX-OS/Nexus One、NVIDIA Cumulus/DOCA、SONiC、FBOSS、Arrcus、DriveNets、Aviz、Hedgehog |

### 8.3 NIC/DPU/SuperNIC 和主机侧 fabric

| 子领域 | 公司 |
|---|---|
| Ethernet NIC/SuperNIC | NVIDIA ConnectX、Broadcom Thor/NetXtreme、AMD Pensando Pollara/Vulcano、Intel E810/IPU、Marvell、Napatech |
| DPU/IPU | NVIDIA BlueField、AMD Pensando、Intel IPU、Marvell OCTEON、Fungible/Microsoft、AWS Nitro |
| Storage/network offload | NVIDIA BlueField-4 STX、Marvell OCTEON、Broadcom、Intel、AWS Nitro、Microsoft Azure SmartNIC |

### 8.4 Scale-up fabric、PCIe/CXL/UALink

| 子领域 | 公司 |
|---|---|
| Proprietary scale-up | NVIDIA NVLink/NVSwitch、AMD Infinity Fabric、Google ICI、AWS NeuronLink、Huawei UB/超节点 |
| UALink/UALoE/ESUN | AMD、Broadcom、HPE、Celestica、Arista、Cisco、Meta、Microsoft、OpenAI、Oracle、NVIDIA、Marvell、Arm |
| PCIe/CXL fabric switch | Astera Labs、Broadcom、Microchip Switchtec、XConn、Montage、Marvell、Rambus、Synopsys、Cadence、Alphawave Semi |
| Retimer/signal conditioning | Astera、Broadcom、Credo、MaxLinear、Marvell、MACOM、Parade、Montage、Renesas、Microchip |

### 8.5 光互联、CPO、DSP、硅光

| 子领域 | 公司 |
|---|---|
| Optical DSP / coherent | Marvell、Broadcom、Cisco/Acacia、Nokia、Ciena、Coherent、MaxLinear |
| CPO/CPX/NPO/ELS | NVIDIA、Broadcom、Coherent、Lumentum、Marvell、Ciena、Molex、Samtec、TeraHop、Open CPX MSA 成员 |
| Silicon photonics / optical engine | Intel、Cisco/Acacia、Ayar Labs、Lightmatter、OpenLight、POET、Ranovus、Coherent、Lumentum、TSMC COUPE、GlobalFoundries、Tower、Samsung Foundry |
| Optical modules | Innolight/中际旭创、Eoptolink/新易盛、Coherent、Lumentum、Fabrinet、Applied Optoelectronics、Accelink/光迅科技、华工科技、Source Photonics、Hisense Broadband、Broadex、Linktel、CIG、Sumitomo、Mitsubishi |
| Lasers/InP/EML/VCSEL | Coherent、Lumentum、Broadcom、MACOM、Sumitomo、Mitsubishi Electric、Sony、AXT、LandMark、II-VI/Coherent |

### 8.6 铜互联、连接器和高速线缆

| 子领域 | 公司 |
|---|---|
| DAC/AEC/ACC | Amphenol、TE Connectivity、Molex、Samtec、Luxshare、BizLink、Credo、MaxLinear、Broadcom、Marvell、MACOM |
| OSFP/QSFP-DD/224G connector | TE、Amphenol、Molex、Samtec、Foxconn/FIT、Luxshare、BizLink、Lotes、Rosenberger |
| Near-chip/co-packaged copper | Molex Impress、TE AdrenaLINE、Samtec、Amphenol、Luxshare、Broadcom/Credo/MaxLinear retimer ecosystem |

### 8.7 OCS、DCI、测试和认证

| 子领域 | 公司 |
|---|---|
| OCS/MEMS optical switching | Google Apollo、Calient、Polatis/Huber+Suhner、Glimmerglass、DiCon、Coherent、NTT、HYC、FiberSmart |
| DCI/scale-across optical | Ciena、Nokia、Cisco/Acacia、Marvell、Infinera/Nokia、Juniper/HPE、Corning、Senko |
| Test and measurement | Keysight、VIAVI、Anritsu、Tektronix、Teledyne LeCroy、Spirent/Ixia、EXFO、Teradyne、Advantest |
| Standards | Ultra Ethernet Consortium、UALink Consortium、OCP ESUN、OCI MSA、Ethernet Alliance、OIF、PCI-SIG、CXL Consortium |

## 9. 未来 6 个季度跟踪指标

1. Broadcom AI revenue 是否从 Q1 FY2026 $8.4B、Q2 指引 $10.7B 继续上修，且 networking 占比是否提高。
2. Tomahawk 6、Cisco G300、NVIDIA Spectrum-6 的 production volume 和客户设计 win。
3. Arista 2026 AI fabrics $3.5B 目标能否继续上调，1.6T 是否如管理层所说 2027 production scale。
4. Meta、OpenAI、Anthropic、Google、AWS 的 GW 级公告是否转化为网络设备、光模块和 ASIC 订单。
5. 1.6T 光模块 ASP 和出货，尤其 >500 万只 2026 预测是否上修。
6. 224G AEC/retimer 的良率、lead time 和客户认证。
7. UEC 1.0/1.0.2、UALink 2.0、OCP ESUN、OCI MSA 是否出现 interoperable silicon demo。
8. CPO/CPX 的 field service 方案、ELS 冗余、光引擎良率和首批客户。
9. Google OCS 是否从 TPU 体系外溢到更多 AI cluster。
10. AI 数据中心电力/液冷进度是否拖延网络收入确认。

## 10. 主要资料来源

### 市场和 CapEx

- [IDC AI Infrastructure Spending Q4 2025 / 2026 forecast](https://www.idc.com/resource-center/blog/ai-infrastructure-spending-caps-historic-year-at-90-billion-in-q4-2025-2029-spending-to-eclipse-1-trillion/)：2025 $318B，2026 $487B，2029 >$1T。
- [TrendForce / PRNewswire Top 9 CSP 2026 CapEx](https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html)：Top 9 CSP 2026 CapEx 约 $830B。
- [Gartner 2026 semiconductor forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)：2026 半导体 >$1.3T，AI 半导体约 30%。
- [Dell'Oro AI back-end switch market >$100B by 2030](https://www.prnewswire.com/news-releases/ai-back-end-switch-market-will-push-past-100-billion-by-2030-according-to-delloro-group-302678344.html)。
- [Dell'Oro Ethernet vs InfiniBand 2025 AI back-end](https://www.prnewswire.com/news-releases/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025-according-to-delloro-group-302708949.html)。

### 公司一手公告

- [Broadcom Q1 FY2026 results](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm)：AI revenue $8.4B，Q2 AI semiconductor 指引 $10.7B。
- [Broadcom OFC 2026 AI infrastructure portfolio](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai)：Tomahawk 6、Davisson CPO、Tomahawk Ultra、Jericho 4、Thor Ultra、400G/lane DSP。
- [Broadcom Tomahawk 6 production volume](https://investors.broadcom.com/news-releases/news-release-details/broadcom-now-shipping-worlds-first-1024-tbps-switch-production)。
- [NVIDIA Rubin platform press release](https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer)：Rubin、Spectrum-6、CPO、Rubin availability。
- [NVIDIA Vera Rubin GTC 2026](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)：七类芯片 full production，SPX Ethernet racks。
- [NVIDIA Spectrum-X Ethernet Photonics technical blog](https://developer.nvidia.com/blog/scaling-power-efficient-ai-factories-with-nvidia-spectrum-x-ethernet-photonics/)。
- [NVIDIA Meta AI infrastructure partnership](https://nvidianews.nvidia.com/news/meta-builds-ai-infrastructure-with-nvidia)：Meta 采用 Spectrum-X，Blackwell/Rubin 大规模部署。
- [Cisco Silicon One G300 / AI data centers](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx)。
- [Arista Q1 2026 results](https://www.arista.com/company/news/press-release/24017-pr-20260505)：Q1 2026 revenue $2.709B，同比 +35.1%。
- [Arista Etherlink AI networking platforms](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2024/Arista-Unveils-Etherlink-AI-Networking-Platforms/default.aspx)。
- [Arista Q1 2026 transcript summary](https://www.fool.com/earnings/call-transcripts/2026/05/05/arista-anet-q1-2026-earnings-transcript/)：AI fabrics 目标上调至 $3.5B。
- [Marvell 1.6T ZR/ZR+ and 2nm coherent DSP](https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html)。
- [Astera Labs Q1 2026 results](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results)。
- [OpenAI and Broadcom 10GW collaboration](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)。
- [Meta and Broadcom MTIA partnership](https://about.fb.com/news/2026/04/meta-partners-with-broadcom-to-co-develop-custom-ai-silicon/)。
- [Anthropic and Amazon up to 5GW compute](https://www.anthropic.com/news/anthropic-amazon-compute)。
- [Anthropic, Google and Broadcom multi-GW compute](https://www.anthropic.com/news/google-broadcom-partnership-compute)。
- [AMD and Celestica Helios rack-scale AI platform](https://www.amd.com/en/newsroom/press-releases/2026-3-16-amd-and-celestica-announce-collaboration-to-a.html)。
- [HPE AMD Helios with Broadcom scale-up networking](https://www.hpe.com/us/en/newsroom/press-release/2025/12/hpe-accelerates-ai-deployments-with-first-amd-helios-ai-rack-scale-architecture-with-open-scale-up-networking-built-with-broadcom.html)。

### 标准和会议

- [Ultra Ethernet Consortium 1.0 specification announcement](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/)。
- [Ultra Ethernet Consortium specification page](https://ultraethernet.org/)。
- [UALink specifications](https://ualinkconsortium.org/specification/)。
- [UALink 200G 1.0 overview](https://ualinkconsortium.org/blog/ualink-200g-1-0-specification-overview-802/)。
- [OCP ESUN workstream](https://www.opencompute.org/blog/introducing-esun-advancing-ethernet-for-scale-up-ai-infrastructure-at-ocp)。
- [OCP ESUN 1.0 specification release](https://www.opencompute.org/blog/the-ocp-esun-10-specification-has-been-released)。
- [OCI MSA optical scale-up consortium](https://www.businesswire.com/news/home/20260312254951/en/Optical-Scale-up-Consortium-Established-to-Create-an-Open-Specification-for-AI-Infrastructure-Led-by-Founding-Members-AMD-Broadcom-Meta-Microsoft-NVIDIA-and-OpenAI)。
- [PCI-SIG DevCon 2026](https://pcisig.com/pci-sig-developers-conference-2026)。
- [PCIe 8.0 Draft 0.5](https://pcisig.com/blog/pcier-80-specification-draft-05-now-available-track-2560-gts-transfer-speeds-2028)。

### 光互联和铜互联

- [TrendForce Google OCS and 800G+ optics share](https://www.trendforce.com/presscenter/news/20260210-12919.html)。
- [Cignal AI optical component revenue nearly $25B in 2025](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)。
- [LightCounting optical transceiver market update](https://www.lightcounting.com/newsletter/en/december-2025-quarterly-market-update-322)。
- [TE Connectivity 224G solutions for AI data centers](https://www.te.com/en/industries/data-centers-ai/technologies/224g-gigabit-ethernet-solution.html)。
- [Molex co-packaged copper 224G](https://www.molex.com/en-us/news/molex-launches-impress-co-packaged-copper-solutions-scaling-near-asic-connectivity-innovations-to-meet-next-gen-data-rate-demands.html)。
- [MaxLinear Annapurna 224G scale-up retimer](https://www.maxlinear.com/news/press-releases/2026/maxlinear-unveils-annapurna-224g-scale-up-retimer-to-extend-copper-connectivity-in-ai-data-centers)。
# 行业调研：【CPO/NPO与交换侧光引擎】

截至日期：2026-05-08  
研究范围：CPO、NPO、CPX/socketed optical engine、ELS、交换侧硅光/光引擎、800G/1.6T/3.2T pluggable、OCS、XPO、coherent DCI、光纤连接与测试，以及短距铜互联的替代/互补关系。  
口径说明：本文的市场规模为全球 AI 数据中心相关供应商收入池或等效收入池，产品之间存在上下游重叠，不能直接相加。利润率默认指毛利率；对自用云厂硬件用“等效外部采购价值”估算。本文按用户要求对 2026-2027 AI 基础设施建设采取明显乐观假设，对缺少直接数据的 CPO/NPO/OCI 早期市场给出大胆上沿。

## 一页结论

1. **2026 年最确定的不是 CPO 全面替代 pluggable，而是 800G 继续吃满、1.6T 开始规模放量、CPO/NPO 在交换侧进入战略卡位。** Cignal AI 估计 2025 年光通信组件收入接近 250 亿美元，其中 datacom 超过 180 亿美元；OFC 2026 口径下 400G+ datacom 模块 2025 年约 4,200 万只，800G 2026 年预测超过 2,000 万只，1.6T 2026 年预测超过 500 万只。TrendForce 估计 800G 及以上模块出货占比从 2024 年 19.5% 升到 2026 年 60%+。

2. **CPO/NPO 的拐点来自“交换机功耗和面板密度”，不是来自光模块厂主动自我替代。** NVIDIA 宣称 Spectrum-X Ethernet Photonics 相比传统 pluggable 可达 5x optical power efficiency、10x resiliency、5x sustained application runtime，并给出 409.6Tb/s 级 Spectrum-X Ethernet Photonics 2026H2 可用。Broadcom OFC 2026 同时展示 102.4T Tomahawk 6-Davisson CPO switch、Taurus 400G/lane optical DSP、PCIe Gen7 retimer 和 200G/lane LPO/1.6T FR4 光模块，说明交换芯片厂正把 optical engine 纳入平台。

3. **NPO/CPX/socketed CPO 比“全封闭 CPO”更可能率先商业化。** Open CPX MSA、Coherent 6.4T socketed CPO、Eoptolink 6.4T NPO optical engine、GF SCALE optical module solution 都指向同一需求：把光引擎尽量靠近交换 ASIC，同时保留可插拔/可维护/多供应商能力。2026-2027 的真实产业形态大概率是 pluggable、XPO、NPO/CPX、CPO 并存。

4. **2026 年 AI 后端网络订单池非常大。** 项目内美国 AI 数据中心建设模型给出网络与光互联订单池：2026 务实 $65-100B、2027 务实 $100-160B；乐观情景 2026 $105-165B、2027 $170-280B。若把 AI scale-across 的 coherent DCI、光纤、OCS、园区网络也计入，2027 上沿可以更高。

5. **最强价值捕获在 switch ASIC/DSP/SerDes、200G/400G EML/SiPh/ELS、CPO/NPO 光引擎平台和高可靠连接/测试。** 普通模块组装会被多供应商和 ASP 下行压制；但 1.6T 早期、CPO/ELS、400G/lane、224G/448G 测试和高密度连接仍有供不应求溢价。

6. **2027 才是 CPO/NPO 真正考验年。** 2026 是样品、资格认证、首批 switch 与供应链投资年；2027 若 Rubin、MI400、TPU8、Trainium3/4、OpenAI/Broadcom ASIC 和 Meta MTIA 同步放量，交换侧 1.6T/CPO/NPO 会被迫从“可选优化”变成“高端 AI fabric 的默认设计选项之一”。

## 信息源权重和关键事实

| 类型 | 关键来源 | 本文采用的主要事实 |
|---|---|---|
| 一手公司发布 | [NVIDIA silicon photonics](https://www.nvidia.com/en-us/networking/products/silicon-photonics/), [NVIDIA Spectrum-X Photonics blog](https://developer.nvidia.com/blog/using-spectrum-x-photonics-and-copackaged-optics-for-power-efficient-ai-data-center-networking/), [NVIDIA Vera Rubin platform](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform) | Spectrum-X Ethernet Photonics、Quantum-X800 CPO、409.6Tb/s、CPO 功耗/可靠性卖点、Rubin/Spectrum-6/SPX 方向 |
| 一手公司发布 | [Broadcom OFC 2026](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai), [Broadcom OFC 2026 PDF](https://docs.broadcom.com/doc/ofc-2026-broadcom-showcases-industry-leading-solutions-scaling-ai-infrastructure), [Broadcom Tomahawk 6-Davisson](https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm78900-series) | 102.4T CPO switch、Taurus 400G/lane DSP、200G/lane LPO、PCIe Gen7 retimer、1.6T FR4 |
| 一手公司发布 | [Coherent OFC CPO](https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026), [Coherent OFC pluggable](https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026), [Coherent Q3 FY2026](https://www.coherent.com/news/press-releases/coherent-announces-third-quarter-fiscal-2026-results) | 6.4T socketed CPO、1.6T/3.2T、400G/lane、datacenter comms 收入和 AI 需求 |
| 一手公司发布 | [Lumentum OFC 2026](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx), [Lumentum 1.6T 2xDR4](https://www.lumentum.com/en/products/16t-2xdr4-osfp), [NVIDIA-Lumentum partnership](https://www.lumentum.com/en/media-room/news-releases/lumentum-deepens-partnership-nvidia-accelerate-ai-infrastructure) | 1.6T DR4/2xDR4、TRO 低功耗、ELS/UHP laser、NVIDIA $1B 设备采购加 $500M 股权投资 |
| 一手公司发布 | [NVIDIA-Coherent partnership](https://www.coherent.com/news/press-releases/coherent-deepens-collaboration-with-nvidia-to-accelerate-ai-infrastructure), [NVIDIA-Corning partnership](https://www.corning.com/worldwide/en/about-us/news-events/news-releases/2026/05/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure.html) | NVIDIA 对 Coherent $500M 先进制造采购承诺加 $500M 股权投资；Corning 与 NVIDIA 扩建美国光纤/线缆产能 |
| 标准/生态 | [Open CPX MSA](https://www.opencpxmsa.org/), [OCI MSA](https://www.oci-msa.org/files/2026-OCI-MSA_Specification_Overview__1.0.pdf), [GF SCALE](https://www.design-reuse.com/news/202531380-globalfoundries-introduces-industry-s-first-silicon-photonics-based-reconfigurable-advanced-coupling-for-lightwave-engine-scale/) | socketed optical engine、CPO/NPO 标准化、optical compute interconnect、GF 可重构硅光耦合方案 |
| 一手公司发布 | [Arista XPO](https://www.arista.com/en/company/news/press-release/23697-pr-20260311), [Eoptolink 6.4T NPO](https://www.eoptolink.com/news/13-new-products/346-eoptolink-unveils-industry-first-6-4-tbps-optical-engine-achieving-highest-density-for-ai-datacenters), [Eoptolink XPO](https://www.eoptolink.com/news/13-new-products/364-eoptolink-joins-xpo-msa-and-unveils-industry-first-12-8-tbps-liquid-cooled-pluggable-optics-for-ai-data-centers) | 12.8T XPO、204.8T/RU 面板密度、400W 冷却、6.4T NPO optical engine |
| 一手公司发布 | [Marvell COLORZ 1600](https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html), [Ciena OFC AI networking](https://www.ciena.com/about/newsroom/press-releases/ciena-brings-ai-networking-expertise-to-ofc-2026), [Ciena Vesta 200](https://www.ciena.com/about/newsroom/press-releases/ciena-solidifies-ai-networking-leadership-unveils-new-innovations-for-high-speed-connectivity), [Nokia OFC 2026 takeaways](https://www.nokia.com/blog/ofc-2026-takeaways-pluggables-multi-rail-hcf-and-ai/) | 1.6T ZR/ZR+、2nm coherent DSP、Vesta 200 6.4T CPX、hyper-rail、multi-rail ILA、1600CL |
| 市场机构/交叉验证 | [Cignal AI](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/), [TrendForce OCS/optics](https://www.trendforce.com/presscenter/news/20260210-12919.html), [Mordor CPO](https://www.globenewswire.com/news-release/2026/01/29/3228606/0/en/Co-Packaged-Optics-Market-Growing-at-35-92-CAGR-to-Reach-USD-0-75-Billion-by-2031-Reports-Mordor-Intelligence.html), [VIAVI OFC 2026](https://blog.viavisolutions.com/2026/04/23/ofc-2026-1-6t-going-mainstream-the-emergence-of-3-2t/) | 光组件总量、800G/1.6T 出货、Google OCS、CPO 早期市场、3.2T 测试复杂度 |
| 在研光 I/O | [Lightmatter Passage M1000](https://www.lightmatter.co/blog/lightmatter-unveils-passage-m1000), [Ayar Labs optical I/O](https://www.ayarlabs.com/), [Marvell-Celestial AI transaction](https://www.marvell.com/company/newsroom/marvell-technology-to-acquire-celestial-ai.html), [OpenLight 3.2T PIC](https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants) | photonic interposer、optical I/O chiplet、Photonic Fabric、3.2T DR8 PIC、448G EAM |

## 1. 2026 AI 数据中心大建设下的机遇和挑战

### 1.1 行业机会：从“光模块升级”变成“AI fabric 架构权”

AI 集群网络有三条并行需求曲线：

| 需求曲线 | 2026 具体表现 | 对 CPO/NPO 与交换侧光引擎的含义 |
|---|---|---|
| Scale-out 带宽 | 800G 已主流，1.6T 从样机进入规模供应；AI 后端 Ethernet/IB port 数和 radix 快速上升 | Pluggable 仍是收入主体，但 1.6T 功耗、面板密度和信号完整性逼近 switch 前面板极限 |
| Scale-up domain 扩大 | NVL72、NVL576、TPU pod、Trainium UltraServer、MI400 Helios 和 MTIA/OpenAI ASIC 都把单集群域做大 | 短距铜继续用于 rack 内最短链路，rack 间和 pod 间需要更密集光 I/O；OCI、CPO/NPO、OCS 进入设计窗口 |
| Scale-across 区域互联 | AI campus/region 需要 20km、120km、1000km 级 800ZR/1600ZR/ZR+ 和多 fiber pair 线路系统 | Marvell/Ciena/Nokia/Cisco/Acacia 等 coherent 生态受益，交换侧光引擎不只存在于机柜内 |

最大投资机会不是“某个模块代际”，而是：交换 ASIC 厂、云厂、光器件厂和连接器厂共同重新定义 AI fabric。过去光模块是服务器/交换机外设；2026 以后高端交换机的可销售价值会越来越包含光引擎、ELS、fiber shuffle、CMIS/管理固件、可靠性监控和现场维护能力。

### 1.2 主要挑战

| 挑战 | 解释 | 2026-2027 风险 |
|---|---|---|
| 224G/448G 电接口 reach 变短 | PAM4 lane 速率越高，front-panel pluggable 从 ASIC 到模块的电通道损耗、均衡和 FEC 成本越高 | Retimer/DSP 功耗上升，推动 CPO/NPO，但也抬高测试成本和良率风险 |
| 可维护性和 field failure | CPO 把光电靠近交换 ASIC，失败后不能像普通 OSFP 那样直接拔换 | Socketed CPO/NPO/CPX 更可能率先商业化，全封闭 CPO 采用慢于宣传 |
| ELS/laser 冗余 | CPO/NPO 常把 laser 外置以降低热和提高可替换性，但外置激光源、fiber routing、耦合损耗和冗余机制复杂 | 高功率 CW/DFB/1310nm laser 成为供给瓶颈和高毛利点 |
| 标准碎片化 | OSFP/QSFP-DD、LPO/LRO/TRO、XPO、Open CPX、OCI、OIF、OCP、NVLink/UALink 各自推进 | 2026 订单会集中给“已经被 hyperscaler 认证”的方案，小厂技术好但可能拿不到资格 |
| 测试时间 | 1.6T/3.2T、224G SerDes、400G/lane optical、CPO thermal drift 需要更长系统级 burn-in | VIAVI/Keysight/Tektronix/Anritsu 等受益，模块厂良率和现金周转承压 |
| 客户集中和 ASP 下行 | Google、Meta、Microsoft、AWS、NVIDIA 生态掌握极强议价权 | 供不应求期毛利高，2026H2-2027 多供应商扩产后低壁垒模块利润率回落 |

### 1.3 当前正在使用的技术

| 层级 | 已在使用/正在放量 | 2026-2027 新变量 |
|---|---|---|
| Rack 内最短距 | DAC、AEC、ACC、PCB/背板、NVLink 铜互联、PCIe/CXL retimer | 224G lane 下铜 reach 继续缩短，高质量 cable/connector 和 retimer 仍高景气 |
| 后端 scale-out | 800G OSFP/QSFP-DD、1.6T OSFP/DR4/2xDR4/FR4、LRO/TRO/LPO、Spectrum-X/InfiniBand/Ethernet | 1.6T 从 early volume 转向主流，LRO/TRO 在功耗和可靠性间折中 |
| 交换侧光引擎 | CPO、NPO、CPX/socketed optical engine、ELS、SiPh PIC、InP/VCSEL/EML/EAM/MZM | 2026 首批 pilot，2027 进入高端 AI switch 小规模或中规模部署 |
| 光交换 | Google Apollo OCS/MEMS optical circuit switching | TPU-like 集群先用，GPU Ethernet fabric 2027 后可能选择性吸收 |
| 区域 DCI | 800ZR/ZR+、1600ZR/ZR+、coherent-lite、full-band/fiber-pair 线路系统 | AI scale-across 把 coherent 从电信市场拉回高增长 |
| 光 I/O chiplet | Lightmatter photonic interposer、Ayar Labs optical I/O、Celestial AI Photonic Fabric、GF SCALE | 2026 NRE/样品，2027 小量，2028 后若 scale-up optical 成功则弹性最大 |

## 1.4 与 2026-2027 出货最大 AI 芯片路线的关系

以下芯片/平台来自项目内《全球 AI 芯片路线图与 2026-2027 产能释放预测》底稿，未重新外部搜索芯片出货预测。

| AI 芯片/平台 | 2026-2027 状态 | 互连路径 | 对 CPO/NPO/光引擎的影响 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 最主力高端 GPU rack | Rack 内 NVLink/铜互连，scale-out 800G/1.6T IB/Ethernet | 2026 大头仍是 pluggable 800G/1.6T；Spectrum-X Photonics/CPO 开始被 GB300/Rubin 后端网络吸收 |
| NVIDIA Vera Rubin NVL72/Rubin | 2026H2 首批，2027 主力 | NVLink 6、ConnectX-9、Spectrum-6/SPX、CPO/Photonic Ethernet | 2027 对 CPO/NPO 最强拉动，尤其是高端 switch、ELS 和 1.6T/3.2T 光引擎 |
| AWS Trainium2/Trainium3 | Trainium2/Rainier 2026 大量部署，Trainium3 UltraServer 接棒 | NeuronLink/NeuronSwitch/EFA，自研以太网 scale-out | AWS 更可能先用 800G/1.6T pluggable 和自研 fabric，CPO 取决于自研交换机代际 |
| Google TPU v7 Ironwood/TPU8 | TPU v7 2026 主力，TPU8 2027 导入 | Rack 内短距高速铜，rack/pod 间全光，Apollo OCS | OCS、800G+ 模块、fiber management 最先受益；CPO 可能不是 Google 第一优先级 |
| AMD MI350/MI400 Helios | MI350 2026 放量，MI400/Helios 2027 增量 | Infinity Fabric、UALink、Pollara/Vulcano NIC、AI Ethernet | 2027 若 MI400 72-GPU rack 顺利，1.6T/OCI/高端 Ethernet 光引擎需求上修 |
| Microsoft Maia 200 | 2026 Azure 推理导入 | Azure 后端网络、液冷 rack、潜在 OCI 标准 | 推动 1.6T、coherent DCI 和 optical scale-up 标准化，但短期多为内部采购 |
| Meta MTIA 300/400/450/500 | 2026-2027 多代 ASIC、多 GW 路线 | Broadcom XPU/Ethernet/SerDes，OCI 生态相关 | Meta 是 CPO/NPO/OCI 的潜在最大边际客户之一，2027 后弹性大 |
| OpenAI/Broadcom ASIC | 2026H2 起步，10GW 长周期 | Broadcom custom XPU、可能混合 NVIDIA/AMD/OCI | 10GW 级项目将显著拉动 1.6T/3.2T、CPO/NPO、coherent DCI 和光纤供给 |
| Huawei Ascend 910C/950 | 中国国产替代主线 | 超节点、自研互连、国产 800G/1.6T 光模块 | 短期拉动国产光模块/光器件/电缆，CPO 较慢，NPO/板载光更可能先试 |
| Cambricon/Alibaba/Baidu 国产 ASIC | 2026-2027 扩张 | 国产以太网/自研互连、800G 光模块、DAC/AEC | 受益更多在国产模块、连接器、测试和 OAM 互连，不是最早 CPO 主线 |

### 1.5 新技术成熟和放量时间

| 技术 | 2026 状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|---|
| 800G pluggable | 主流放量 | 2026 继续高量，2027 仍有大量存量 | 2026-2027 持续供不应求 | 若 AI capex 超预期，800G 与 1.6T 同时缺货到 2027 |
| 1.6T pluggable | 规模供货前夜，2026 出货 >500 万只口径 | 2026H2 放量，2027 新增 AI 集群主流 | 2027 1.6T 2,000-2,500 万只 | 2027 3,000 万只级别，短缺和高毛利延续 |
| LPO/LRO/TRO | 2026 多厂商产品化 | LRO/TRO 因可靠性更强，先于极简 LPO 大规模 | 云厂为功耗强推 linear 方案 | Switch-NIC 生态统一验证，linear 方案成为 1.6T 低功耗主线 |
| CPO | NVIDIA/Broadcom/Coherent 等 pilot | 2026-2027 小量，高端 switch 试点 | 2027 多个 AI cluster 商用 | 2027 成为 102T/204T 高端 switch 默认路线之一 |
| NPO/CPX/socketed CPO | Open CPX、Coherent/Eoptolink/GF 样品 | 2026 标准/样品，2027 早期部署 | 2027 多供应商资格认证 | 2027 CPO 与 NPO 并行放量，NPO 率先拿到更高份额 |
| XPO 12.8T 液冷可插拔 | Arista MSA，Eoptolink 展示 | 2026 样品，2027 小批量，2028 放量 | 2027H2 高端 switch 导入 | 若 CPO field service 难题拖慢，XPO 2027 即成高端主路线 |
| 3.2T/400G per lane | DSP/PIC/EML/EAM 样品 | 2026 样品，2027 demo/qual，2028 放量 | 2027H2 小批量收入 | 204.8T switch 提前，2027 形成 $10B+ 早期市场 |
| OCS | Google 体系化采用 | 2026-2027 Google/TPU-like 主导 | 2027 Meta/Microsoft/Anthropic 试点 | GPU Ethernet fabric 也大范围吸收 OCS |
| 1600ZR/ZR+/coherent-lite | Marvell 2026H2 采样，Ciena/Nokia 路线明确 | 2027 规模化 | AI campus/metro DCI 提前爆发 | Scale-across 成为 AI 网络第二大瓶颈 |
| Optical I/O chiplet/photonic interposer | Lightmatter/Ayar/Celestial/GF 样品和设计赢单 | 2027 小量，2028 后更大规模 | 2027 大客户项目制导入 | 若铜 reach 触顶提前，2027 进入 rack-scale 架构必选 |

### 1.6 2026 最可能的技术路径

1. **收入主体：800G + 1.6T pluggable。** 800G 是 2026 的实际主力，1.6T 是 2026 下半年和 2027 的最强新增量。
2. **交换侧新平台：102.4T switch ASIC + 1.6T optical + CPO/NPO pilot。** NVIDIA/Broadcom 会把 CPO/NPO 作为高端 AI switch 平台卖点，但 2026 仍偏 pilot 与资格认证。
3. **可维护路线优先：NPO/CPX/socketed CPO 优先于全封闭 CPO。** 云厂不会为节能轻易接受不可维护的大规模故障风险。
4. **Google 路线独立：OCS + 800G/1.6T 光模块。** OCS 不是替代光模块，而是放大光模块和光纤管理需求。
5. **短距铜仍强：DAC/AEC/ACC 不会突然消失。** AI rack 内最短链路仍需要铜，且 224G AEC/ACC、连接器和 retimer 仍有高景气。

## 2. 已经开始放量的关键产品

### 2.1 市场规模和渗透率路径

时间口径：未来 3 个月为 2026-05 至 2026-08，未来 1 年为截至 2027-05，未来 2 年为截至 2028-05。B/O/X 分别为基准、乐观、极度超预期乐观。渗透率为对应细分场景的新建 AI 高端端口/系统渗透率。

| 已放量产品 | 2026-05 状态 | 未来 3 个月规模 | 未来 1 年规模 | 未来 2 年规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 800G pluggable 模块 | AI 后端主力，Google/Meta/Microsoft/NVIDIA 生态大规模使用 | B $7-11B / O $10-15B / X $14-20B | B $28-45B / O $42-65B / X $60-85B | B $40-70B / O $65-100B / X $90-140B | 2026 新建高端光口 55-70%；2027 因 1.6T 上升降至 35-55%，但总量仍大 |
| 1.6T OSFP/DR4/2xDR4/FR4 | 2026 >500 万只出货口径，Coherent/Lumentum/Eoptolink 等产品化 | B $1.5-3B / O $3-5B / X $5-8B | B $8-14B / O $14-25B / X $25-38B | B $25-45B / O $45-75B / X $75-120B | 2026 新建 AI 高端端口 10-25%；2027 35-60%；X 情景 70%+ |
| 200G/lane optical components | 1.6T 共同瓶颈，含 EML/VCSEL/SiPh PIC/driver/TIA/DSP | B $3-5B / O $5-8B / X $8-12B | B $14-24B / O $24-38B / X $38-55B | B $30-50B / O $50-80B / X $80-120B | 1.6T attach 近 100%；高端 800G/1.6T 组件价值占模块 ASP 45-65% |
| AI Ethernet/IB 交换机与 switch ASIC | Spectrum-X、Tomahawk/Jericho、Cisco Silicon One、Marvell/Ciena/Nokia 高端网络 | B $4-7B / O $7-11B / X $10-16B | B $20-35B / O $35-60B / X $60-90B | B $50-90B / O $90-150B / X $150-230B | AI 后端高端端口 2026 35-55%；2027 55-80% |
| LRO/TRO/LPO/linear optics | 低功耗路线从试点转产品化，TRO/LRO 更容易过可靠性 | B $0.8-1.5B / O $1.5-3B / X $3-5B | B $4-8B / O $8-15B / X $15-25B | B $12-25B / O $25-45B / X $45-75B | 2026 在 1.6T 端口 10-25%；2027 25-50%；X 情景 60%+ |
| DAC/AEC/ACC 铜互联 | Rack 内短距仍强，224G/PCIe6/以太网 AEC 受益 | B $2-4B / O $3-5B / X $5-7B | B $8-16B / O $14-24B / X $24-35B | B $15-30B / O $28-50B / X $50-75B | Rack 内短距 60-85%；跨 rack 被光替代，价值转向 AEC/ACC/连接器 |
| 800ZR/1600ZR coherent DCI | AI campus/metro/regional 拉动，Marvell 1600 2026H2 采样 | B $1-2B / O $2-3B / X $3-5B | B $5-9B / O $8-14B / X $14-22B | B $10-18B / O $18-32B / X $32-55B | AI scale-across DCI 新建端口 2026 15-25%；2027 30-55% |
| OCS/MEMS 光交换 | Google Apollo 代表路线，功耗优势极强 | B $0.1-0.3B / O $0.3-0.6B / X $0.6-1B | B $0.6-1.5B / O $1.5-3B / X $3-6B | B $2-6B / O $6-12B / X $12-25B | TPU-like 集群 2026 10-25%；2027 25-50%；GPU fabric 仍 <10%，X 情景 20%+ |

### 2.2 利润率和增速区间

| 产品 | 当前毛利率估计 | 基准情景 | 乐观情景 | 极度超预期乐观 |
|---|---:|---|---|---|
| 800G pluggable | 30-40%，领先厂可 40%+，EMS 约 12% | 增速 20-35%，毛利 28-38%，ASP 下行 | 增速 35-55%，毛利 32-42% | 增速 60%+，短缺延续，毛利 38-48% |
| 1.6T pluggable | 35-45%，早期 premium | 增速 80-120%，毛利 32-42% | 增速 120-180%，毛利 38-48% | 增速 200%+，毛利 45-55% |
| 光器件/laser/PIC/ELS | 40-55%，稀缺件更高 | 增速 35-55%，毛利 42-55% | 增速 60-90%，毛利 48-60% | 增速 100%+，毛利 55-68% |
| Switch ASIC/DSP/SerDes | 55-70%，系统设备 35-55% | 增速 35-55%，毛利 55-68% | 增速 60-90%，毛利 60-72% | 增速 100%+，CPO 溢价，毛利 65-76% |
| DAC/AEC/ACC | AEC/ACC 芯片 45-65%，线缆组装 20-35% | 增速 25-40%，毛利小幅下行 | 增速 40-60%，AEC 维持高毛利 | 增速 70%+，224G AEC 溢价 |
| Coherent DCI | DSP/高端模块 40-55%，系统 35-45% | 增速 20-35%，毛利 38-50% | 增速 35-55%，毛利 42-55% | 增速 60%+，毛利 48-60% |
| OCS | MEMS/系统硬件 35-50%，软件更高 | 增速 50%，毛利 35-45% | 增速 100%，毛利 40-55% | 增速 200%，毛利 50-65%，若云厂自研则外部毛利被压 |

## 3. 在研和即将快速增长的关键产品

### 3.1 关键技术和规模预测

| 在研/早期产品 | 关键事实 | 未来 3 个月 | 未来 1 年 | 未来 2 年 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| CPO switch optical engine | NVIDIA/Broadcom 推进，Coherent/Lumentum 供光引擎/ELS | B $0.05-0.15B / O $0.15-0.4B / X $0.4-1B | B $0.3-0.8B / O $0.8-2.5B / X $3-8B | B $1.5-4B / O $5-15B / X $20-45B | 高端 AI switch 2026 <5%；2027 B 5-12%，O 15-25%，X 35%+ |
| NPO/CPX/socketed optical engine | Open CPX MSA、Eoptolink 6.4T NPO、GF SCALE、Ciena Vesta 200 | B <$0.1B / O $0.1-0.3B / X $0.3-0.8B | B $0.2-0.7B / O $0.7-2B / X $2-6B | B $1-3B / O $4-12B / X $12-30B | 2027 比全封闭 CPO 更容易进入多供应商，X 情景高端 switch 20-35% |
| External Laser Source/ELSFP | Lumentum UHP laser、Coherent CPO、NVIDIA 对激光供应链投资 | B $0.1-0.3B / O $0.3-0.6B / X $0.6-1B | B $0.5-1.2B / O $1.2-3B / X $3-7B | B $2-5B / O $5-12B / X $12-25B | CPO/NPO attach 近 100%；也服务 future optical I/O |
| 3.2T/400G-per-lane | Broadcom Taurus、OpenLight 3.2T DR8 PIC、Coherent 400G/lane | B <$0.1B / O $0.1-0.2B / X $0.2-0.5B | B $0.2-1B / O $1-3B / X $3-8B | B $3-10B / O $10-25B / X $25-55B | 2027 主要样品/qual；2028 新建高端端口 B 10-20%，X 40%+ |
| XPO 12.8T 液冷可插拔 | Arista MSA、Eoptolink 12.8T XPO，400W/module cooling | B <$0.1B / O $0.1-0.2B / X $0.2-0.5B | B $0.1-0.5B / O $0.5-1.5B / X $1.5-4B | B $1-4B / O $4-12B / X $12-25B | 2027 高端 switch <5%；若 CPO 服务难题明显，XPO 2028 可 15-25% |
| OCI optical scale-up | AMD/Broadcom/Meta/Microsoft/NVIDIA/OpenAI 等推动开放光计算互连 | B <$0.1B / O $0.1-0.3B / X $0.3-0.8B | B $0.2-1B / O $1-3B / X $3-8B | B $2-8B / O $8-25B / X $25-70B | 2027 设计 win，2028 rack-scale AI 加速，X 情景成为多 ASIC 互连事实标准 |
| Photonic interposer/optical I/O chiplet | Lightmatter Passage M1000、Ayar optical I/O、Celestial Photonic Fabric | B <$0.1B / O $0.1-0.2B / X $0.2-0.5B | B $0.1-0.7B / O $0.7-2B / X $2-6B | B $1-5B / O $5-18B / X $18-50B | 2027 小量；2028 若铜 reach 触顶，scale-up domain 渗透 5-20%，X 30%+ |
| Advanced fiber/connector/fiber shuffle | Corning/NVIDIA 扩产，Senko/Molex/Samtec/US Conec/Amphenol 受益 | B $0.8-1.5B / O $1.5-2.5B / X $2.5-4B | B $4-8B / O $8-15B / X $15-25B | B $10-20B / O $20-40B / X $40-70B | CPO/NPO/XPO/OCS 都提高 fiber count 和连接复杂度 |
| 薄膜铌酸锂/聚合物高速调制器 | 400G/lane 低功耗候选，2026 以样品和设计为主 | B <$0.05B / O $0.05-0.1B / X $0.1-0.2B | B $0.1-0.4B / O $0.4-1B / X $1-2B | B $1-4B / O $4-10B / X $10-20B | 2028 后若成本/封装稳定，可切入 3.2T/6.4T |

### 3.2 在研产品利润率

| 产品 | 当前/早期利润率 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---|---|---|
| CPO optical engine | 30-45%，早期 NRE 和服务成本高 | 35-45%，规模小 | 45-60%，ELS/engine 稀缺 | 60-75%，若被写入高端 switch 标配 |
| NPO/CPX/socketed engine | 35-50% | 35-45%，标准成本高 | 45-60%，多供应商但高壁垒 | 55-70%，若替代全封闭 CPO 成主流 |
| ELS/高功率 laser | 45-60% | 45-55% | 55-65% | 60-75%，NVIDIA 类长期采购锁定 |
| 3.2T/400G-lane 器件/DSP | 45-65% | 45-55%，测试成本高 | 55-68% | 65-78%，若 2027 提前缺货 |
| XPO | 35-50% | 35-45%，液冷服务成本高 | 45-55% | 55-65%，若成为 CPO 替代高密度路线 |
| OCI/optical scale-up chiplet | IP/硅片 60-80%，系统初期低 | 50-65% | 60-75% | 70-85%，若形成生态锁定 |
| Photonic interposer | 早期项目制，毛利不稳定 | 30-45% | 45-60% | 60-80%，若进入 hyperscaler 核心平台 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 关键工艺/能力 |
|---|---|---|---|
| Switch ASIC/DSP/SerDes | 美国设计、中国台湾/韩国代工 | NVIDIA、Broadcom、Marvell、Cisco/Acacia、AMD/Pensando、Intel | 5/4/3/2nm SerDes-rich SoC、102.4T/204.8T switch、224G/448G PHY、coherent DSP |
| SiPh PIC/foundry | 美国、中国台湾、欧洲、新加坡 | GlobalFoundries、TSMC、Intel、Tower、STMicro、imec、AIM Photonics、OpenLight 生态 | Silicon photonics PDK、grating/edge coupler、MZM、ring modulator、Ge PD、3D integration |
| InP laser/EML/PD | 美国、日本、欧洲、中国 | Lumentum、Coherent、Broadcom、Mitsubishi Electric、Sumitomo、Accelink、Source Photonics、Hisense Broadband | 1310nm/1550nm laser、EML/EAM、DFB/CW laser、UHP laser、ELS |
| 模块设计和组装 | 中国、泰国、马来西亚、越南、美国 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、AAOI、Fabrinet、Accelink、华工正源、Hisense、Linktel、Luxshare/FIT | 800G/1.6T OSFP/QSFP-DD、LPO/LRO/TRO、coherent pluggable、自动耦合、burn-in |
| CPO/NPO/optical engine packaging | 美国、中国台湾、中国、泰国/马来西亚 | Coherent、Lumentum、Eoptolink、Ciena、GF、Molex、Samtec、TeraHop、Fabrinet、ASE/Amkor/TSMC 生态 | Optical engine socket、fiber attach、thermal path、ELS coupling、CPO substrate/assembly |
| Fiber/connectors | 美国、日本、中国、欧洲 | Corning、Senko、US Conec、Molex、Samtec、Amphenol、TE、Fujikura、Sumitomo、Furukawa、Prysmian、AFL | High-density fiber shuffle、MPO/MTP、co-packaged connector、multi-core fiber、bend-insensitive fiber |
| 测试与验证 | 美国、日本、德国 | VIAVI、Keysight、Tektronix、Anritsu、Rohde & Schwarz、EXFO、Spirent、Advantest、Teradyne、FormFactor | 1.6T MAC/FEC、224G SerDes、400G/lane optical、jitter/BER、thermal drift、CPO system burn-in |

### 4.2 供给瓶颈

1. **200G/400G EML/EAM/MZM 和高功率 CW laser。** 1.6T、3.2T、CPO、ELS 都共用高性能光源和调制器，NVIDIA 对 Lumentum、Coherent 的投资和采购承诺说明激光器已被视为战略瓶颈。
2. **224G/448G SerDes、DSP、retimer 人才和硅验证。** 这是模拟/混合信号能力，不是单纯数字逻辑，头部团队稀缺。
3. **SiPh PIC 良率、耦合损耗和封装自动化。** PIC 本身可代工，但高良率光纤耦合、主动/被动对准、热漂移控制仍是瓶颈。
4. **ELS 冗余和现场维护。** CPO/NPO 需要 laser 可替换、可监控、可冗余，否则云厂不愿承担大规模故障。
5. **高密度连接和光纤管理。** CPO/NPO/OCS/XPO 会大幅增加 fiber shuffle、connector、清洁、弯曲半径和标签管理复杂度。
6. **液冷与热机械可靠性。** CPO/XPO 把光、电、热集中到交换机前面板或封装周围，液冷漏液、热循环、warpage 和污染都会影响寿命。
7. **客户认证周期。** Hyperscaler 对 optics 的资格认证通常需要数季，供应商即使有样品也未必能快速进入批量。
8. **高速测试产能。** 400G/lane 和 CPO 系统级测试时间可能成为隐形产能瓶颈。
9. **地缘和供应链合规。** 中国模块厂份额高，但高端 DSP、laser、EDA、代工和美国客户认证受政策影响。
10. **人才。** 光封装、硅光设计、高速 SerDes、coherent DSP、云厂网络架构人才高度稀缺。

### 4.3 成本结构和价格传导

| 产品 | BOM/单位成本拆分估计 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 1.6T pluggable | Optical PIC/EML/laser/PD 30-40%；DSP/driver/TIA/retimer 20-30%；PCB/connector/cage 10-15%；组装耦合 8-12%；测试/burn-in 10-15%；良率/RMA 5-10% | 200G/400G 器件、DSP 功耗、良率、客户认证、ASP 下行速度 | 云厂年度框架价 + allocation；短缺时器件厂涨价可向模块端传导，供给扩散后模块端先被压 |
| CPO/NPO optical engine | PIC/光器件 25-35%；EIC/driver/TIA 20-30%；ELS/laser/fiber 15-25%；socket/connector/substrate/thermal 10-20%；测试/服务 10-20% | 可靠性、可维护性、ELS 方案、标准接口、多供应商认证 | 早期按 NRE + premium ASP；若被 switch ASIC 厂打包，利润向 ASIC/平台商集中 |
| CPO switch system | Switch ASIC 40-55%；optical engines/ELS 25-35%；板级/封装/液冷 10-20%；软件/管理 5-10% | ASIC radix、系统节能、客户网络锁定、良率和 field service | 按整机/AI fabric 价值定价，客户用 watts/port 和 cluster goodput 评估，不只看每光口价格 |
| OCS | MEMS/光学核心 30-45%；fiber array/connector 20-30%；控制电子/软件 15-25%；系统集成 10-20% | 功耗节省、重构速度、损耗、端口数、云厂架构依赖 | 云厂自研压低硬件利润，但系统软件/运维可能有高毛利 |
| DAC/AEC/ACC | 线缆/连接器 35-55%；redriver/retimer/AEC 芯片 25-45%；测试和组装 10-20% | 224G 稳定性、插损、热、长度、客户 rack 标准 | 铜价和连接器成本可传导有限，高端 AEC 芯片按性能溢价 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 子领域 | 头部集中度判断 | 竞争结构 |
|---|---|---|
| Switch ASIC | CR3 高，Broadcom/NVIDIA/Cisco 占据高端主导 | Broadcom 以 merchant Ethernet 强，NVIDIA 以 GPU/NVLink/Spectrum-X 生态强，Cisco Silicon One 和 Marvell 分食 |
| 800G/1.6T 模块 | CR5 中高，但中国供应商份额大且价格竞争强 | Innolight/Eoptolink/Coherent/Lumentum/AAOI/Fabrinet/Accelink/HG Genuine/Hisense 等 |
| Laser/EML/SiPh | CR5 高于模块，壁垒更强 | Lumentum、Coherent、Broadcom、Mitsubishi、Sumitomo、OpenLight/GF 等 |
| CPO/NPO 光引擎 | 早期，头部未定，但 switch ASIC 厂和光器件龙头优势大 | NVIDIA/Broadcom/Coherent/Lumentum/Ciena/Eoptolink/GF/Lightmatter/Ayar 等 |
| OCS | 早期且云厂自研强 | Google 主导应用，Calient/Polatis/Glimmerglass/DiCon 等潜在受益 |
| Coherent DCI | CR5 较高 | Ciena、Nokia/Infinera、Cisco/Acacia、Marvell、Coherent/Lumentum |
| 测试 | 寡头 | VIAVI、Keysight、Tektronix、Anritsu、EXFO 等 |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 可量化表现 | 为什么能定价 |
|---|---|---|
| 224G/448G SerDes 和 400G/lane optical | BER、jitter、FEC latency、power/bit、thermal drift 都需达标 | 一次链路不稳定会拖垮整个 AI cluster，客户愿为 proven silicon 支付溢价 |
| 客户资格认证 | 6-18 个月验证、双/三供策略、量产 PPM/FIT 要求 | 进入 cloud AVL 后订单黏性强，新供应商替换成本高 |
| 光器件良率 | EML/SiPh/PIC/耦合良率每提升 1-2pct 都改变成本曲线 | 早期短缺时良率领先者拥有产能和 ASP 双重溢价 |
| ELS/CPO field service | laser 可替换、冗余、监控、CMIS/固件、现场清洁流程 | 只有能把 OPEX 和宕机风险讲清楚的方案，才能进入大规模部署 |
| 系统生态绑定 | NVIDIA Spectrum-X/NVLink、Broadcom Tomahawk/Jericho、Google OCS、AWS EFA | 网络一旦与训练/推理软件栈绑定，客户切换成本极高 |
| 供应链规模 | 以百万只模块、数十万 rack 光口供货，要求自动化和现金周转 | 小厂难承受库存、预付款、RMA 和产线爬坡压力 |
| 标准和专利 | Open CPX/OCI/OIF/OCP 规格、SiPh PDK、DSP IP、connector IP | 标准参与方先拿设计窗口，并能影响接口定义 |

### 5.3 价值捕获判断

| 层级 | 2026-2027 价值捕获 | 长期 ROIC/毛利判断 |
|---|---|---|
| Switch ASIC + fabric 软件 | 最强，Broadcom/NVIDIA/Cisco/Marvell 能把 optics 纳入系统 | 长期最高之一，软件/生态锁定强，毛利 55-75% |
| Laser/ELS/SiPh/DSP | 最强瓶颈层，NVIDIA 对 Lumentum/Coherent/Corning 的投资说明战略价值 | 长期高，若技术持续领先毛利 45-70% |
| CPO/NPO optical engine 平台 | 2026 收入小，2027 后高弹性 | 若标准和可维护性胜出，长期高 ROIC；若被 ASIC 厂强集成，利润被平台商吸收 |
| Pluggable 模块 | 2026 1.6T 仍高景气 | 中期被 ASP 下行压制，只有高端产品和认证客户能保高毛利 |
| EMS/组装 | 量大但利润薄 | 稳定低毛利，Fabrinet 类优秀 EMS 可受益但 ROIC 低于器件/ASIC |
| Fiber/connector | 被低估，CPO/NPO/OCS/XPO 放大需求 | 头部连接器和高密 fiber management 长期好于普通线缆 |
| 测试设备 | 小而高毛利 | 1.6T/3.2T/CPO 越复杂，测试越高价值 |

结论：长期最优价值链层级是 **switch ASIC/系统平台、laser/ELS/SiPh/DSP、CPO/NPO 光引擎平台、高速测试与高密连接**。普通模块会有 2026-2027 的β，但长期容易被多供应商压价。

## 6. 2026 关键变化：最可能放量的子方向

1. **1.6T pluggable 从样品转规模供货。** 这是 2026 最确定收入增量。OFC 2026 的一手发布密集，Cignal 给出 2026 >500 万只 1.6TbE 口径。
2. **NVIDIA/Broadcom 把 CPO 放进 switch 平台叙事。** Spectrum-X Photonics、Quantum-X800 CPO、Broadcom 102.4T Tomahawk 6-Davisson CPO 说明 CPO 进入交换侧产品路线图。
3. **供应链投资从 GPU/HBM 延伸到光纤/激光。** NVIDIA 对 Lumentum、Coherent、Corning 的采购和股权动作，说明 AI 光互联已从可替换部件变成战略约束。

2026 最可能放量排序：1.6T pluggable、200G/lane EML/SiPh/laser/DSP、LRO/TRO、AI switch ASIC、coherent DCI、OCS 在 Google 生态、CPO/NPO pilot。

## 7. 2027 关键变化：最可能放量的子方向

1. **Rubin/MI400/TPU8/Trainium3/MTIA/OpenAI ASIC 同步放大，1.6T 成新增 AI 集群默认配置。** 这会让光口数量、radix 和 switch density 再上台阶。
2. **CPO/NPO/CPX 从 pilot 进入第一轮商业化。** 如果 socketed optical engine 的可维护性被证明，NPO/CPX 可能比全封闭 CPO 更快放量。
3. **3.2T/400G-lane 和 optical scale-up 进入早期收入。** 2027 不是 3.2T 全面量产年，但高端客户的 live demo、资格认证和小批量订单会驱动上游器件、DSP 和测试先赚钱。

2027 最可能放量排序：1.6T 主流化、CPO/NPO/ELS、OCS 扩散、1600ZR/ZR+、XPO 高密度可插拔、3.2T 器件/测试、OCI/optical I/O chiplet 设计 win。

## 8. 头部公司和潜在黑马清单

### 8.1 Switch ASIC、AI fabric、系统平台

| 公司 | 位置 |
|---|---|
| NVIDIA | Spectrum-X、Spectrum-6、Quantum-X800 CPO、NVLink、ConnectX/BlueField，AI factory 生态最强 |
| Broadcom | Tomahawk/Jericho、102.4T CPO、Taurus 400G/lane DSP、custom XPU/SerDes，merchant Ethernet 龙头 |
| Cisco/Acacia | Silicon One、coherent optics、路由/交换系统和 AI networking |
| Marvell | Teralynx、coherent DSP、custom silicon、Celestial AI Photonic Fabric 收购 |
| Arista | AI Ethernet switch 系统、XPO MSA 发起方，hyperscaler 关系强 |
| AMD/Pensando | UALink、Pollara/Vulcano、MI400/Helios 生态 |
| Intel | Ethernet/retimer/硅光历史积累，AI accelerator 较弱但互连 IP 仍有价值 |
| HPE/Juniper | AI networking 和 data center switching，NVIDIA/AMD 生态补充 |

### 8.2 Pluggable 光模块和光引擎

| 公司 | 优势 |
|---|---|
| Innolight/中际旭创 | 800G/1.6T AI 模块头部，hyperscaler 份额高 |
| Eoptolink/新易盛 | 800G/1.6T、6.4T NPO、12.8T XPO，技术迭代快 |
| Coherent | 垂直整合 InP/SiPh/laser/module/CPO，NVIDIA 投资合作 |
| Lumentum | Laser/ELS/1.6T/Cloud Light 资产，NVIDIA $1B 采购承诺和 $500M 投资 |
| Applied Optoelectronics | 800G/1.6T datacenter 模块，高增长但客户集中和毛利波动大 |
| Fabrinet | 高端光模块 EMS，泰国产能和大客户认证，毛利低但规模弹性强 |
| Accelink/光迅科技、HG Genuine/华工正源、Hisense Broadband、Source Photonics、Linktel、GIGALIGHT | 中国/亚洲供应链补充，受益国产和多供策略 |
| Cisco/Acacia、Ciena、Nokia/Infinera | Coherent DCI、line systems、CPX/optical engine |

### 8.3 Laser、SiPh、DSP、IP

| 公司 | 优势 |
|---|---|
| Lumentum、Coherent、Broadcom、Mitsubishi Electric、Sumitomo Electric | InP laser、EML、PD、CW laser、ELS |
| GlobalFoundries | Fotonix/SCALE silicon photonics platform，面向 CPO/OCI optical engine |
| TSMC、Intel、Tower、STMicro、imec、AIM Photonics | SiPh foundry/PDK/先进封装生态 |
| Marvell、Broadcom、MaxLinear、Credo、MACOM、Semtech | DSP、SerDes、retimer、AEC/ACC 芯片 |
| Synopsys、Cadence、Siemens EDA、Alphawave | SerDes/UCIe/3DIC/光电协同 IP 和验证 |
| OpenLight、Ayar Labs、Lightmatter、Celestial AI、Ranovus、POET Technologies、TeraHop | optical I/O、CPO/NPO、photonic interposer、硅光/III-V 集成黑马 |

### 8.4 OCS、连接、光纤、测试和制造

| 领域 | 公司 |
|---|---|
| OCS/MEMS | Google、Calient、Polatis/HUBER+SUHNER、Glimmerglass、DiCon、CrossFiber |
| Fiber/connector | Corning、Senko、US Conec、Molex、Samtec、Amphenol、TE Connectivity、Fujikura、Sumitomo、Furukawa、Prysmian、AFL、CommScope |
| 测试 | VIAVI、Keysight、Tektronix、Anritsu、Rohde & Schwarz、EXFO、Spirent、Advantest、Teradyne、FormFactor |
| EMS/封装 | Fabrinet、Foxconn/FIT、Luxshare、Jabil、ASE、Amkor、TSMC advanced packaging、JCET、KYOCERA、Ibiden、Unimicron、Shinko |

## 9. 投资判断和跟踪指标

### 9.1 2026-2027 投资优先级

| 排名 | 方向 | 理由 |
|---:|---|---|
| 1 | 1.6T 光模块与 200G/lane 器件 | 收入最确定，2026-2027 需求和短缺同时存在 |
| 2 | Laser/ELS/SiPh/DSP | 供给瓶颈更强，毛利和战略价值高于普通模块组装 |
| 3 | Switch ASIC + CPO/NPO 平台 | 长期架构权，若绑定 AI fabric，可获得最高 ROIC |
| 4 | 高密度连接、fiber shuffle、测试 | 被低估但必需，CPO/NPO/OCS/XPO 都会增加复杂度 |
| 5 | OCS 和 coherent DCI | Google/AI scale-across 先行，2027 后可能被重估 |
| 6 | Optical I/O chiplet/photonic interposer | 近期收入小，但一旦 scale-up optical 成立，弹性最大 |

### 9.2 需要持续跟踪的 15 个信号

1. NVIDIA Spectrum-X Photonics / Quantum-X800 CPO 是否出现大客户公开部署。
2. Broadcom Tomahawk 6-Davisson CPO switch 是否进入 hyperscaler 量产资格认证。
3. Lumentum/Coherent 对 NVIDIA 采购承诺的产能转换节奏。
4. 1.6T OSFP 实际出货是否超过 500 万只，且 ASP 是否快于预期下行。
5. Innolight/Eoptolink/Coherent/Lumentum/AAOI/Fabrinet 的 1.6T 订单和毛利率。
6. Open CPX MSA 是否形成可执行 compliance 和多供应商 plugfest。
7. Eoptolink 6.4T NPO、Coherent socketed CPO、GF SCALE 是否进入客户 qual。
8. XPO MSA 是否吸引更多 switch 系统厂和 hyperscaler。
9. OpenLight 3.2T DR8 PIC beta、Broadcom Taurus 和 Coherent 400G/lane 的客户验证。
10. Google OCS 是否从 TPU 扩散到更多内部网络，或被 Meta/Microsoft 采用。
11. OCI MSA 是否从规格走向 test chip/plugfest/客户样机。
12. Marvell 1600ZR/ZR+、Ciena Vesta 200、Nokia 1600CL 是否在 AI campus 获得订单。
13. Corning/NVIDIA 扩产是否缓解光纤/线缆供给。
14. 224G/448G 测试设备订单是否持续上修。
15. AI capex 是否因 ROI 或电力瓶颈在 2026H2 出现放缓。

## 10. 风险

1. **ASP 下行快于需求增长。** 光模块产能一旦追上，2026H2-2027 可能先出现价格战。
2. **CPO field service 不达标。** 节能很强但可维护性不够，会推迟大规模采购。
3. **标准碎片化。** CPO、NPO、CPX、XPO、OCI、OIF 并行，可能导致库存和研发投入分散。
4. **AI 数据中心电力/并网延期。** 光互联订单可能领先，但若上电延期，收入确认会波动。
5. **云厂自研压价。** OCS、NPO、optical engine 若被云厂深度定制，外部供应商毛利上限会被压。
6. **地缘风险。** 中国模块厂份额大，美国 AI 基础设施客户对供应链可控性会提高要求。

## 附录：核心来源链接

- NVIDIA silicon photonics: <https://www.nvidia.com/en-us/networking/products/silicon-photonics/>
- NVIDIA Spectrum-X Photonics blog: <https://developer.nvidia.com/blog/using-spectrum-x-photonics-and-copackaged-optics-for-power-efficient-ai-data-center-networking/>
- NVIDIA Vera Rubin platform: <https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform>
- Broadcom OFC 2026 release: <https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai>
- Broadcom Tomahawk 6-Davisson: <https://www.broadcom.com/products/ethernet-connectivity/switching/strataxgs/bcm78900-series>
- Coherent CPO OFC 2026: <https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026>
- Coherent 1.6T/3.2T OFC 2026: <https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026>
- Coherent NVIDIA partnership: <https://www.coherent.com/news/press-releases/coherent-deepens-collaboration-with-nvidia-to-accelerate-ai-infrastructure>
- Lumentum OFC 2026: <https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx>
- Lumentum NVIDIA partnership: <https://www.lumentum.com/en/media-room/news-releases/lumentum-deepens-partnership-nvidia-accelerate-ai-infrastructure>
- Corning NVIDIA partnership: <https://www.corning.com/worldwide/en/about-us/news-events/news-releases/2026/05/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure.html>
- Open CPX MSA: <https://www.opencpxmsa.org/>
- OCI MSA specification overview: <https://www.oci-msa.org/files/2026-OCI-MSA_Specification_Overview__1.0.pdf>
- GF SCALE: <https://www.design-reuse.com/news/202531380-globalfoundries-introduces-industry-s-first-silicon-photonics-based-reconfigurable-advanced-coupling-for-lightwave-engine-scale/>
- Arista XPO MSA: <https://www.arista.com/en/company/news/press-release/23697-pr-20260311>
- Eoptolink 6.4T NPO: <https://www.eoptolink.com/news/13-new-products/346-eoptolink-unveils-industry-first-6-4-tbps-optical-engine-achieving-highest-density-for-ai-datacenters>
- Eoptolink XPO: <https://www.eoptolink.com/news/13-new-products/364-eoptolink-joins-xpo-msa-and-unveils-industry-first-12-8-tbps-liquid-cooled-pluggable-optics-for-ai-data-centers>
- Marvell COLORZ 1600: <https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html>
- Marvell to acquire Celestial AI: <https://www.marvell.com/company/newsroom/marvell-technology-to-acquire-celestial-ai.html>
- Ciena OFC 2026: <https://www.ciena.com/about/newsroom/press-releases/ciena-brings-ai-networking-expertise-to-ofc-2026>
- Ciena Vesta 200: <https://www.ciena.com/about/newsroom/press-releases/ciena-solidifies-ai-networking-leadership-unveils-new-innovations-for-high-speed-connectivity>
- Nokia OFC 2026 takeaways: <https://www.nokia.com/blog/ofc-2026-takeaways-pluggables-multi-rail-hcf-and-ai/>
- Cignal AI optical component revenue: <https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/>
- TrendForce optics/OCS: <https://www.trendforce.com/presscenter/news/20260210-12919.html>
- Mordor CPO market: <https://www.globenewswire.com/news-release/2026/01/29/3228606/0/en/Co-Packaged-Optics-Market-Growing-at-35-92-CAGR-to-Reach-USD-0-75-Billion-by-2031-Reports-Mordor-Intelligence.html>
- VIAVI OFC 2026: <https://blog.viavisolutions.com/2026/04/23/ofc-2026-1-6t-going-mainstream-the-emergence-of-3-2t/>
- OpenLight 3.2T DR8 PIC: <https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants>
- Lightmatter Passage M1000: <https://www.lightmatter.co/blog/lightmatter-unveils-passage-m1000>
- Ayar Labs: <https://www.ayarlabs.com/>
# 行业调研：【InfiniBand与专有Scale-up互联】

截至日期：2026-05-08  
研究口径：本报告聚焦 AI 计算中心里连接加速器的高性能互联系统，重点覆盖 InfiniBand、NVIDIA NVLink/NVSwitch、NVIDIA Spectrum-X/Quantum-X、Broadcom 以太网 scale-up/scale-out、UALink/UEC、Google TPU ICI/Apollo OCS、AWS NeuronLink/EFA、AMD Infinity Fabric/UALoE、华为/寒武纪等超节点互联，以及配套的 NIC/DPU/SuperNIC、交换芯片、交换机系统、铜缆/DAC/AEC/LACC、CPO/硅光/ELS、测试认证和 fabric 管理软件。美元口径为名义收入或订单规模估算，`B`=十亿美元，`M`=百万美元。对于自用 ASIC 和内部互联，采用“等效外部采购/内部转移价值”估算。

## 0. 一页结论

1. **2026 年最确定的技术路径仍是“NVIDIA rack 内 NVLink/NVSwitch + rack 间 InfiniBand 或 Spectrum-X”。** GB200/GB300 已经把 NVLink fabric 变成每个 NVL72 rack 的默认 BOM，Vera Rubin NVL72 在 2026H2 接棒，NVLink 6 提升到每 GPU 3.6TB/s、单 rack 260TB/s。NVIDIA FY2026 Q4 数据中心 networking revenue 已达 $11.0B，同比 +263%，全年 networking $31.4B，同比 +142%，说明网络已经不是配角。
2. **InfiniBand 仍是 NVIDIA 大训练集群的“性能保险”，但市场份额压力来自 Ethernet。** Quantum-X800 已到 800G、144 ports/switch，并具备 SHARP v4、adaptive routing、telemetry congestion control。挑战是 Dell'Oro 已判断 Ethernet 在 AI back-end switch 中反超，2025 年 Ethernet AI back-end switch sales 超过 InfiniBand 两倍以上，且预计 AI back-end switch market 2030 年超过 $100B。
3. **专有 scale-up 的核心战场从“谁的链路最快”变为“谁能把 72-1,024 个 accelerator 当作可运营资产”。** NVLink 的壁垒是 GPU 原生集成、SHARP collective、CUDA/Dynamo/Mission Control 软件闭环；Broadcom/Meta/OpenAI 的路线是用 Ethernet scale-up/scale-out/across 做更开放、更可采购的 rack 级 fabric；UALink 则试图把 accelerator pod 内部互联标准化。
4. **2026 年的最大拐点是 Ethernet 开始侵入 scale-up，而不是只赢 scale-out。** Broadcom Tomahawk 6 已 production volume shipping，102.4T、512×200G/1024×100G SerDes，单芯片可连接 512 XPUs 做单跳 all-to-all；Tomahawk Ultra 主打 250ns latency；Jericho 4 面向 1M+ XPU lossless fabric。Meta >1GW MTIA 和 OpenAI 10GW Broadcom 均明确采用 Ethernet scale-up/scale-out。
5. **UALink 2026 仍是 early ramp，2027 才是商业放量窗口。** UALink 1.0 是 200G per lane、最多 1,024 accelerators/pod；2.0 计划 2026Q2 引入 in-network compute；3.0 目标 2027 面向更高带宽、跨 rack/row reach 和更强可靠性。2026 的收入主要来自 IP、switch silicon、验证、early rack；2027 才可能被 AMD Helios、Meta/Open Rack、部分云厂自研 ASIC 拉动。
6. **光互联和铜互联不是互斥，而是距离和功耗分层。** 2026 rack 内/短距 scale-up 仍大量依赖 NVLink 铜缆、LACC、DAC/AEC、高速 backplane 和 CPO 前的电连接；rack 间与 scale-out 继续由 800G/1.6T 光模块承接；CPO/CPX/NPO/OCI 是 2027-2028 的高端 switch 和 optical scale-up 方向。
7. **价值捕获排序：NVIDIA 全栈 proprietary fabric > switch/NIC/DPU silicon > 高端 CPO/1.6T 光器件/DSP > fabric 软件与认证 > 交换机白盒/线缆组装。** 但 2026-2027 的高 beta 来自 1.6T Ethernet、Broadcom/Marvell/ASIC 互联、UALink IP/switch、CPO/ELS、铜缆/AEC/retimer 和测试设备。

## 1. 行业定义：Scale-up、Scale-out、Scale-across

### 1.1 三层网络

| 层级 | 典型距离 | 目标 | 代表技术 | 2026 关键变化 |
|---|---:|---|---|---|
| Scale-up | 同机箱、同 rack、少数 rack | 把多个 GPU/XPU 变成一个近似共享内存/统一 accelerator domain | NVLink/NVSwitch、UALink、Broadcom Ethernet scale-up、Google ICI、AWS NeuronLink、AMD Infinity Fabric/UALoE、华为 UB/HCCS 类互联 | 从 NVIDIA proprietary 主导，进入 Ethernet/UALink 竞争窗口 |
| Scale-out | rack 间、pod 内、机房内 | 连接多台 accelerator server/rack，做分布式训练和推理 | InfiniBand、Spectrum-X/RoCE、UEC Ethernet、Arista/Cisco/HPE Ethernet、Google/AWS 自研网络 | 800G 主流化，1.6T 开始导入，Ethernet 份额扩大 |
| Scale-across | 楼宇、campus、metro、regional | 跨数据中心或跨园区把多个 AI factory 连接为容量池 | Spectrum-XGS、coherent pluggables、1600ZR/ZR+、Ciena/Nokia line system、OCS | 2026 从传统 DCI 升级为 AI regional fabric |

### 1.2 为什么 InfiniBand 与专有 Scale-up 仍值得单独研究

AI 网络不是普通数据中心 leaf-spine。训练和 agentic inference 的成本函数是 `GPU利用率 x tail latency x collective效率 x 故障恢复 x 每瓦 token`。因此互联能定价的原因不是端口数，而是它能否让一台价值数百万美元的 rack 多跑 1-5% 的有效 token 或缩短数周训练周期。

2026 年主要矛盾是：

- **性能极限：** NVLink/InfiniBand 仍有低延迟、collective offload、GPU 生态协同优势。
- **可采购性：** Ethernet/UEC/UALink 的多供应商、开放标准和运维熟悉度吸引 hyperscaler。
- **电力约束：** CPO、OCS、低功耗 copper、retimerless/LPO 都在争夺同一目标：用更低 bit/W 保持 accelerator 利用率。
- **客户锁定：** NVIDIA 把 GPU、NVLink、InfiniBand/Spectrum、DPU、软件、MGX rack 和 DSX 打包；Broadcom/Meta/OpenAI 则把 XPU、Ethernet、PCIe、optics、SerDes、retimer 打包成开放但高度定制的供应链。

## 2. 公开事实锚点

| 类别 | 关键数字/事实 | 产业含义 |
|---|---|---|
| NVIDIA networking | FY2026 Q4 Data Center Networking revenue $11.0B，同比 +263%，环比 +34%；FY2026 networking $31.4B，同比 +142%。 | NVLink、InfiniBand、Ethernet 已经成为 NVIDIA 数据中心收入的独立高增长引擎。 |
| NVIDIA NVLink 6 | 每 GPU 3.6TB/s，72 GPU all-to-all，单 Vera Rubin NVL72 rack 260TB/s。 | 2026H2 Rubin 后，rack 内 scale-up 价值继续上移。 |
| NVIDIA Quantum-X800 | 800Gb/s 端到端 InfiniBand；Quantum-X800 switch 144×800G；ConnectX SuperNIC up to 1.6Tb/s per GPU。 | 2026 大训练集群继续有 InfiniBand 高确定需求。 |
| NVIDIA Vera Rubin | 七类芯片 full production：Vera CPU、Rubin GPU、NVLink 6、ConnectX-9、BlueField-4、Spectrum-6、Groq 3 LPU；2026H2 伙伴供货。 | NVIDIA 从 GPU 出货转为 rack/POD/GW 级系统出货。 |
| Broadcom Tomahawk 6 | 102.4Tbps switch，production volume shipping；单芯片支持 512×200G 或 1024×100G SerDes；可连接 512 XPUs 做 scale-up。 | Ethernet 的 scale-up 可信度大幅上升。 |
| Broadcom OFC 2026 | 3.5D XPU production、102.4T CPO switch、400G/lane optical DSP、Thor Ultra 800G NIC、Agera 3 retimer、PCIe Gen6。 | Broadcom 提供 XPU + Ethernet + PCIe + optics + SerDes 的完整非 NVIDIA 互联栈。 |
| UALink 1.0 | 200G per lane、最多 1,024 accelerators/pod；93% effective peak bandwidth；成员超过 85 家。 | 开放 scale-up 标准进入 productization 阶段。 |
| UALink roadmap | 2.0 计划 2026Q2，加入 INC；Management/Chiplet spec 同步；3.0 目标 2027。 | 2026 是验证年，2027 是第一代商用 ramp。 |
| UEC | 1.0 规范发布，目标是完整 Ethernet AI/HPC communications stack。 | Ethernet 不只是 RoCE 微调，而是针对 AI/HPC 重构 transport/flow/control。 |
| IDC Ethernet switch | 2025 Ethernet switch revenue $55.1B，+31.5%；data center segment $32.5B，+53.5%；4Q25 data center $9.9B，+63%；NVIDIA 4Q25 data center Ethernet share 15.2%。 | AI 正把 Ethernet switch TAM 重新抬高，NVIDIA 也在 Ethernet 中拿份额。 |
| Dell'Oro AI back-end | 2030 AI back-end switch spending 超过 $100B；800G 已占 AI back-end 主流，2027 预计转向 1.6T，2030 走向 3.2T。 | 2026-2027 网络升级斜率可能高于服务器出货斜率。 |

## 3. 2026 机遇、挑战与正在使用的技术

### 3.1 机遇

| 机遇 | 量化判断 | 最受益方向 |
|---|---:|---|
| AI rack 从 8 GPU server 转向 72+ GPU rack-scale | GB200/GB300/Rubin/Helios/Trainium3 都在提高 rack 内 accelerator 数量 | NVSwitch/NVLink、UALink switch、Broadcom TH6/Tomahawk Ultra、铜缆/AEC/retimer |
| Back-end 网络从 400G/800G 转向 1.6T | OFC 2026 资料指向 2026 1.6T pluggable >500 万只，2027 进入大规模部署 | 1.6T optics、200G/400G SerDes、switch ASIC、NIC/DPU |
| Hyperscaler 自研 ASIC 拉动非 NVIDIA 互联 | OpenAI 10GW Broadcom、Meta >1GW MTIA、Google TPU、AWS Trainium | Broadcom、Marvell、AMD Pensando、UALink/UEC、PCIe/CXL/optics IP |
| Agentic inference 提高 tail-latency 和 KV cache 要求 | 长上下文、多轮 agent、test-time compute 让网络和存储成为 token cost 关键 | NVLink 6、LPX direct links、BlueField-4 STX、CPO、OCS |
| 电力紧缺放大 bit/W 价值 | CPO 5x optical power efficiency、OCS 功耗降低 90%+ 的故事进入采购讨论 | CPO/CPX/NPO、LPO/LACC、ELS、OCS、低功耗 SerDes |

### 3.2 挑战

1. **Ethernet 对 InfiniBand 的份额挤压。** InfiniBand 性能仍强，但 hyperscaler 对多供应商、SONiC/EOS/自研 NOS、成本和供应链弹性更敏感。
2. **Scale-up 标准碎片化。** NVLink、UALink、UALoE、Broadcom proprietary Ethernet extensions、Google ICI、AWS NeuronLink、华为超节点互联并存，软件与测试复杂度上升。
3. **铜互联物理极限。** 224G/448G PAM4、机架内高密布线、损耗、弯折半径、散热、连接器可靠性和可维护性成为真实瓶颈。
4. **CPO 的可维护性与良率。** CPO 能降功耗，但 field replace、ELS 冗余、热漂移、封装良率、测试时间会延迟规模化。
5. **客户认证周期长。** 一套 AI fabric 不是换交换机就行，需要训练框架、collective library、容错、调度、观测、运维 SOP 全栈验证。
6. **高端人才稀缺。** 224G/448G SerDes、switch ASIC、IB/RoCE congestion control、collective offload、硅光封装和大规模 fabric debug 都是小圈子人才。

### 3.3 2026 正在使用的技术全景

| 技术 | 已部署场景 | 2026 状态 | 投资判断 |
|---|---|---|---|
| NVLink 5 / NVSwitch | GB200/GB300 NVL72 rack | 大规模量产，绑定 NVIDIA rack | 2026 最确定、毛利最强，但纯 NVIDIA 暴露 |
| NVLink 6 | Vera Rubin NVL72 | full production，2026H2 伙伴供货 | 2027 大放量核心 |
| Quantum-X800 InfiniBand | NVIDIA 大规模训练/超级计算/neo cloud | 800G，144 ports/switch，ConnectX-8/9 | 高端训练稳，但份额受 Ethernet 压力 |
| Spectrum-X Ethernet | NVIDIA Ethernet scale-out/AI cloud | Spectrum-X800 到 Spectrum-6/SPX，CPO 路线明确 | NVIDIA 在 Ethernet 份额扩张的主线 |
| Broadcom Ethernet scale-up/out/across | Meta MTIA、OpenAI custom ASIC、非 NVIDIA XPU clusters | TH6 production，Tomahawk Ultra/Jericho 4/Thor Ultra | 非 NVIDIA AI fabric 最核心底座 |
| UALink / UALoE | AMD Helios、开放 accelerator pod | 1.0 产品化、2.0/management/chiplet spec 2026 | 2026 小，2027 弹性大 |
| UEC Ethernet | AI/HPC Ethernet transport | 1.0/1.0.2 规范，interop 演示推进 | 打开多厂商后端网络采购 |
| Google ICI / OCS | TPU pod/Ironwood | 内部成熟，OCS 方向强化 | 外部投资映射在 optics/OCS/line system |
| AWS NeuronLink/EFA | Trainium/Inferentia | 内部成熟，Trainium3/4 扩展 | 自研 ASIC 规模验证开放标准压力 |
| 华为 UB/HCCS/CloudMatrix 类互联 | Ascend 超节点/Cluster | 中国市场高确定需求 | 国产供应链替代和软件适配是关键 |

## 4. 2026-2027 头部 AI 芯片技术路径背景下的互联预测

以下表格使用项目内已有 AI 芯片路线图作为背景，不再外部重新搜索芯片出货量。

| 2026-2027 头部芯片/平台 | 互联路径 | 对 InfiniBand/Scale-up 行业的含义 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | Rack 内 NVLink 5/NVSwitch，rack 间 Quantum-X800 或 Spectrum-X，scale-out 800G/1.6T optics | 2026 收入主力。每个 NVL72 rack 自带高价值 scale-up fabric，拉动 NVSwitch、铜缆、ConnectX、BlueField、IB/Ethernet switch。 |
| AWS Trainium2 | Rack 内 NeuronLink，scale-out EFA/Ethernet | AWS 自研路线证明 proprietary scale-up 可以在封闭云内部大规模跑通；外部受益在 Ethernet、光模块、交换机、测试。 |
| Google TPU v7 Ironwood | TPU ICI、自研 pod fabric、短距铜 + rack 间光/OCS | Google 的 Apollo OCS 和 TPU 网络会提高光交换、800G/1.6T 模块和线路系统价值。 |
| NVIDIA B200/GB200 Blackwell | NVLink 5 + Quantum/Spectrum | 存量和延续订单继续贡献 NVLink/IB revenue。 |
| Huawei Ascend 910C/950 | 自研超节点互联 + 国产交换/光模块 | 中国市场绕开 NVIDIA，拉动国产以太网/光模块/连接器/交换芯片，但软件和 HBM 限制真实效率。 |
| Cambricon MLU 590/690 | MLU-Link/OAM + Ethernet/optics | 国产 AI 集群扩大后，标准 Ethernet 与国产 fabric 管理软件需求上升。 |
| AMD MI350/MI355 | 8-GPU UBB/Infinity Fabric + Ethernet scale-out | 2026 企业与云端第二供给源，但 scale-up domain 小于 NVL72。 |
| AWS Trainium3 | 144-chip UltraServer，NeuronSwitch/Neuron Fabric + EFA | 自研 ASIC scale-up domain 变大，验证非 NVIDIA fabric 的经济性。 |
| Meta MTIA 300/400/450/500 | Broadcom XPU + Ethernet scale-up/out/across | 2026-2029 多 GW 级部署，是 Broadcom Ethernet scale-up 的最强样板。 |
| Microsoft Maia 200 | Azure 自研后端网络 + 内部 scale-up | 对外少卖设备，但拉动 Azure 数据中心 Ethernet/optics/液冷/时钟/同步。 |
| OpenAI/Broadcom custom accelerator | Broadcom Ethernet + PCIe + optics，2026H2 起 10GW | 非 NVIDIA AI fabric 订单能见度最高的长期项目之一。 |
| AMD MI400/MI455X Helios | 72 GPU rack，UALink/UALoE scale-up + UEC/Ethernet scale-out | 2027 UALink/UALoE 商业化最重要载体。 |

### 4.1 新技术成熟和放量时间：三情景

| 技术 | 2026-05 成熟度 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|---|
| NVLink 5/NVSwitch | 成熟量产 | 2026 全年随 GB200/GB300 出货，2027 让位但仍高量 | GB300 需求延续至 2027H1 | 2026H2-2027H1 供应持续短缺，NVSwitch 溢价维持 |
| NVLink 6 | full production，2026H2 partner availability | 2026H2 小批，2027 主力 | 2026Q4 明显收入化，2027 快速接棒 GB300 | Rubin ramp 接近 Blackwell，2027 成为高端 AI rack 默认 |
| Quantum-X800 InfiniBand | 800G 产品化 | 2026-2027 在 NVIDIA 训练集群保持增长，份额被 Ethernet 稀释 | Blackwell/Rubin 大训练需求强，绝对收入继续扩张 | CPO Quantum-X 加速落地，InfiniBand 高端份额稳住 |
| Spectrum-X / Spectrum-6 Ethernet | 800G 放量，102.4T/CPO 路线明确 | 2026 放量，2027 1.6T/CPO 增速加快 | 成为 neocloud 和云厂新增 NVIDIA cluster 默认 scale-out | NVIDIA 在 Ethernet DC share 从 15% 级继续上行 |
| Broadcom Tomahawk 6 / Ultra / Jericho 4 | TH6 已量产，Ultra/Jericho 进入 AI 方案 | 2026 随 Meta/OpenAI/ASIC early rack 增长，2027 放大 | 2027 成为非 NVIDIA AI fabric 主导 silicon | scale-up Ethernet 被证明可替代部分 NVLink/IB 高端场景 |
| UALink 1.0/2.0 | 1.0 已公开，2.0 2026Q2 | 2026 IP/测试/样机，2027 first-gen switch/rack | 2027 被 AMD Helios/部分 hyperscaler ASIC 大量采用 | 2027 形成 $10B+ 直接产品市场，成为采购清单项 |
| UEC Ethernet 1.0/1.1 | 1.0/1.0.2 发布，interop 推进 | 2026 产品验证，2027 进入更多 AI fabric | 2027 成为多厂商 AI Ethernet 的事实规范 | 与 UALink/ESUN 共同压缩 InfiniBand 份额 |
| CPO/CPX/NPO/OCI | 多厂商样品/早期客户 | 2026 pilot，2027 高端 switch 小规模 | 2027 socketed CPO/CPX 被多个 AI cluster 采用 | 2027 高端 AI switch 默认 CPO/CPX，ELS/optical engine 供不应求 |
| 3.2T/400G-per-lane | DSP/EML/PIC 样品 | 2026 样品，2027 live demo/qual，2028 规模 | 2027H2 小批收入 | 2027 形成数十亿美元早期市场 |

### 4.2 2026 最可能的技术路径

1. **NVIDIA 新增 GPU rack：** NVLink 5/6 scale-up + Quantum-X800 InfiniBand 或 Spectrum-X Ethernet scale-out。基准情景中，InfiniBand 用于最高端训练和 supercomputer，Spectrum-X 用于 hyperscaler/cloud AI Ethernet。
2. **非 NVIDIA custom ASIC rack：** Broadcom Ethernet scale-up/out + PCIe/CXL/retimer/optics，典型客户是 Meta MTIA 和 OpenAI custom accelerator。
3. **AMD Helios/开放 rack：** 2026H2 以 UALoE/UALink early 方案出现，2027 才明显放量。
4. **自研云厂内部 fabric：** AWS NeuronLink/EFA、Google TPU ICI/OCS、Microsoft Maia/Azure fabric 继续扩张，对外部供应链映射在交换芯片、光模块、光交换、DPU/NIC、测试。

## 5. 已开始放量的关键产品：市场规模、渗透率和利润率

说明：下表把“产品市场规模”定义为相应产品或方案的年度化收入/订单池，不等同公司收入。渗透率为该产品在对应 AI back-end/scale-up 细分中的采用率估算。

### 5.1 市场规模与渗透率路径

| 已放量产品/细分 | 2026 当前状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| NVIDIA NVLink 5/NVSwitch rack fabric | GB200/GB300 NVL72 主力 | 基准 $5-8B；乐观 $8-12B；极乐观 $12-16B | 基准 $22-35B；乐观 $35-50B；极乐观 $50-70B | 基准 $30-50B；乐观 $55-80B；极乐观 $80-110B | NVIDIA rack-scale GPU 内部 attach 接近 100%；全球高端 AI rack scale-up 价值占比 45-60% |
| NVIDIA Quantum-X800 InfiniBand + ConnectX | 800G 高端训练/AI supercomputer | $4-7B / $6-9B / $8-12B | $18-30B / $26-42B / $38-58B | $24-40B / $38-65B / $55-85B | NVIDIA 大训练集群中 40-60%，全 AI back-end switch 份额 20-35% 但绝对额增长 |
| NVIDIA Spectrum-X/Spectrum-6 Ethernet | AI Ethernet scale-out，高速增长 | $3-6B / $5-8B / $8-11B | $18-32B / $30-48B / $45-65B | $40-70B / $65-105B / $95-145B | NVIDIA AI Ethernet data center switch share 已到 15% 级；2027 高速端口份额继续上行 |
| Broadcom Tomahawk/Jericho/Thor/Agera AI Ethernet silicon | TH6 volume shipping，Meta/OpenAI 拉动 | $4-8B / $7-11B / $10-15B | $22-40B / $36-60B / $55-85B | $50-90B / $85-135B / $125-190B | Merchant/specialized AI Ethernet silicon 在非 NVIDIA fabric 中 50-75%；scale-up Ethernet 2027 加速 |
| 800G AI Ethernet/IB switch systems | 800G 已成为 AI back-end 主流 | $8-14B / $12-18B / $16-24B | $38-60B / $55-85B / $80-120B | $45-75B / $70-110B / $95-150B | 800G 2026 为主流，2027 被 1.6T 稀释但仍大出货 |
| 1.6T pluggable optics for AI fabric | 2026 放量前夜，>500 万只年出货预期 | $2-4B / $3-6B / $5-8B | $9-16B / $15-28B / $25-40B | $22-40B / $40-70B / $70-110B | 2026 高端新增集群 10-20%；2027 新增 AI fabric 25-45%；极乐观 50%+ |
| DAC/AEC/LACC/高速铜缆与连接器 | Rack 内/短距继续刚需 | $2-4B / $3-5B / $4-7B | $10-18B / $15-25B / $22-35B | $16-30B / $25-45B / $40-65B | Rack 内短距 attach 70%+，但中长距逐步被光替代；AEC/retimer attach 上升 |
| NIC/DPU/SuperNIC | ConnectX、BlueField、Thor Ultra、Pensando、Marvell | $4-7B / $6-10B / $9-14B | $22-38B / $35-55B / $50-78B | $45-75B / $70-110B / $105-160B | 高端 AI server attach 近 100%；DPU/SmartNIC attach 从 35-55% 向 60-80% |

### 5.2 增长和毛利率预测

| 产品 | 基准增长 | 乐观增长 | 极度超预期增长 | 当前/未来毛利率判断 |
|---|---:|---:|---:|---|
| NVLink/NVSwitch rack fabric | 未来一年 +35-55%，两年 CAGR +25-40% | +60-85% | +100%+ | NVIDIA 系统级毛利参考 71-75%；NVLink 作为专有附加价值，估计 70-85%，极度短缺时更高。 |
| Quantum-X800 InfiniBand | +25-45% | +50-70% | +90% | Switch/NIC silicon 和系统综合 55-75%；高端训练客户愿付性能保险溢价。 |
| Spectrum-X Ethernet | +55-85% | +90-130% | +160%+ | NVIDIA Ethernet 高端 mix 毛利 60-75%；CPO/软件 attach 后上行。 |
| Broadcom AI Ethernet silicon | +60-90% | +100-140% | +180%+ | Switch/NIC/retimer/DSP silicon 60-75%；公司 adjusted EBITDA 高 60% 级说明议价强。 |
| 800G switch systems | +40-60% | +70-90% | +110% | Box 25-45%；使用自有 silicon/软件/客户认证的 Arista/NVIDIA/Cisco/HPE 更高。 |
| 1.6T optics | +80-120% | +150-220% | +300% | 早期高端模块 35-45%，上游 EML/SiPh/laser/DSP 可 45-65%；2027 多供后 ASP 压力。 |
| 高速铜缆/AEC/连接器 | +35-55% | +60-85% | +120% | 普通 DAC/connector 25-40%，AEC/retimer/高密连接 40-65%。 |
| NIC/DPU/SuperNIC | +45-70% | +80-110% | +150% | NIC/SuperNIC 55-70%，DPU/软件安全/存储 offload 可 60-75%。 |

## 6. 在研和快速增长产品：市场规模、渗透率和毛利率

### 6.1 产品路线与市场规模

| 在研/快速增长技术 | 2026 当前状态 | 未来 3 个月 | 未来 1 年 | 未来 2 年 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| UALink switch/IP/management/chiplet | 1.0 公开，2.0 计划 Q2，商业 early | $100-300M / $250-600M / $500M-1.2B | $1-3B / $3-7B / $7-14B | $6-15B / $15-35B / $35-70B | 2026 <5%；2027 在开放 XPU/AMD Helios 中 10-25%；极乐观 30%+ |
| UALoE / Ethernet scale-up rack | AMD Helios/Celestica/HPE 生态推进 | $200-600M / $500M-1.5B / $1-3B | $2-6B / $6-14B / $14-28B | $12-30B / $30-65B / $65-120B | 2027 开放 GPU/XPU rack 中 15-35%；极乐观成非 NVIDIA 默认 |
| NVLink Fusion | NVIDIA 半定制开放，AWS Trainium4/Marvell 等生态 | $200-500M / $500M-1B / $1-2B | $2-5B / $5-12B / $12-25B | $10-25B / $25-55B / $55-100B | Custom ASIC 接入 NVIDIA rack 的桥；2027 从少数客户扩大 |
| Spectrum-6/Quantum-X CPO switch | Spectrum-6 102.4T CPO，Quantum CPO 方向 | $100-400M / $300-900M / $800M-2B | $1-4B / $4-10B / $10-22B | $8-20B / $20-45B / $45-85B | 2026 pilot，2027 高端 switch 5-15%，极乐观 25%+ |
| Broadcom TH6-Davisson CPO / NPO | TH6-Davisson sampling，third-gen CPO | $100-300M / $300-800M / $800M-1.8B | $1-3B / $3-8B / $8-18B | $7-18B / $18-40B / $40-75B | 高端 AI Ethernet switch 中逐步替代部分 pluggable |
| OCI optical compute interconnect | MSA 成立，协议无关 optical scale-up | <$100M / $100-300M / $300-800M | $300M-1B / $1-3B / $3-8B | $2-8B / $8-25B / $25-60B | 2026 标准/样机，2027 pilot，2028 后规模化 |
| CPX/XPO 12.8T liquid-cooled pluggable | Arista XPO MSA，多家演示 | <$100M / $100-300M / $300-600M | $300M-1B / $1-4B / $4-10B | $3-10B / $10-25B / $25-50B | 作为 CPO 之外高密 pluggable 路线，2027 高端导入 |
| OCS optical circuit switching | Google Apollo 体系化采用讨论 | $100-300M / $300-800M / $800M-1.5B | $1-3B / $3-7B / $7-15B | $5-15B / $15-35B / $35-70B | TPU-like cluster 先行；GPU Ethernet fabric 若采用则放大 |
| 3.2T/400G-lane optics/DSP | Broadcom Taurus、OpenLight/Coherent 样品 | <$200M / $200-500M / $500M-1B | $0.5-2B / $2-6B / $6-12B | $8-20B / $20-45B / $45-85B | 2027 仍早期；2028 才更主流 |
| Fabric management / observability / congestion software | UFM、Mission Control、EOS、SONiC、Apstra 等升级 | $300-800M / $600M-1.5B / $1-3B | $2-5B / $5-10B / $10-18B | $6-15B / $15-30B / $30-60B | 高端 AI fabric attach 从 30-50% 到 60-80%，软件毛利高 |

### 6.2 毛利率预测

| 在研/快速增长技术 | 基准毛利率 | 乐观毛利率 | 极度乐观毛利率 | 为什么能有溢价 |
|---|---:|---:|---:|---|
| UALink IP/switch silicon | 55-70% | 65-78% | 75-85% | 标准初期 IP/验证/互操作稀缺，客户避免 NVIDIA 锁定愿意付设计导入费。 |
| UALoE rack system | 25-45% | 35-55% | 45-65% | 系统集成毛利较低，但低延迟验证、液冷 rack、fabric tuning 可溢价。 |
| NVLink Fusion | 65-80% | 75-85% | 80-90% | 本质是 NVIDIA 把专有 scale-up 收费边界扩到第三方 XPU。 |
| CPO/CPX optical engine/ELS | 35-55% | 50-70% | 65-80% | 早期良率和可靠性难，ELS 冗余、封装、测试、客户认证形成壁垒。 |
| Broadcom CPO/NPO switch silicon | 60-75% | 70-80% | 75-85% | TH6/Tomahawk/Jericho 生态、SerDes、DSP、optics 全栈掌控。 |
| OCI optical scale-up | 35-60% | 55-75% | 70-85% | 标准初期，optical PHY、connector、WDM、测试工具短缺。 |
| OCS | 35-50% | 45-60% | 60-75% | 如果从 Google 扩散到更多 AI fabric，MEMS/控制软件/运维集成变稀缺。 |
| 3.2T optics/DSP | 40-60% | 55-70% | 65-80% | 400G/lane 器件、DSP、测试和良率是少数厂商能力。 |
| Fabric 软件 | 70-85% | 80-90% | 85-95% | 软件直接影响 GPU 利用率，客户切换成本和运维依赖高。 |

## 7. 供给侧：产能结构、瓶颈、成本与毛利

### 7.1 产能结构

| 环节 | 主要地区 | 主要公司/资产 | 关键工艺/能力 |
|---|---|---|---|
| InfiniBand/NVLink/Spectrum silicon | 美国、以色列、台湾代工 | NVIDIA/Mellanox、TSMC、封测 OSAT | 先进 switch ASIC、NVSwitch、ConnectX/BlueField、224G SerDes、CoWoS/高阶封装 |
| Ethernet switch/NIC/retimer silicon | 美国、台湾、新加坡/马来西亚封测 | Broadcom、Marvell、Cisco Silicon One、AMD Pensando、Astera、Credo、MACOM、MaxLinear | 102.4T switch、200G/400G lane DSP、PCIe Gen6、retimer/AEC |
| 交换机系统/白盒 | 台湾、美国、墨西哥、泰国、东欧 | Arista、Cisco、HPE/Juniper、Celestica、Accton/Edgecore、Quanta、Wiwynn、Foxconn、Dell、Supermicro | 高密交换机主板、散热、液冷、SONiC/EOS/NOS 集成、客户 burn-in |
| 光模块/光器件 | 中国、泰国、马来西亚、美国、日本、台湾 | Coherent、Lumentum、Fabrinet、Innolight/中际旭创、Eoptolink/新易盛、AOI、光迅科技、华工科技、天孚通信、海信宽带、Marvell、Broadcom optics | 800G/1.6T OSFP/QSFP、EML/VCSEL/SiPh、DSP、TRO/LPO/LRO、CPO optical engine |
| 铜缆/连接器/AEC | 中国、台湾、美国、墨西哥、越南 | Amphenol、TE、Molex、Samtec、Luxshare、BizLink、Credo、Astera、Spectra7、Semtech、MACOM | DAC/AEC/LACC、high-density connector、224G channel、retimer/linear equalization |
| 测试认证 | 美国、日本、欧洲、中国 | Keysight、VIAVI、Spirent、Anritsu、Tektronix、Teradyne、Advantest | 800G/1.6T/3.2T、LLR/CBFC、SerDes eye、FEC、interop、thermal/reliability |
| 软件/fabric management | 美国、以色列、欧洲 | NVIDIA UFM/DOCA/Mission Control、Arista EOS、Cisco、Juniper Apstra、SONiC 社区、HPE Slingshot、Cornelis | 拥塞控制、telemetry、job-aware routing、collective library、fault isolation |

### 7.2 至少 10 个供给瓶颈

1. **224G/448G SerDes 设计与良率。** 102.4T/204.8T switch 和 1.6T/3.2T optics 都依赖超高良率高速 I/O，任何 jitter/BER 问题都会拖慢客户认证。
2. **高阶 switch ASIC 封装和基板。** 大 die switch、CPO、多 chiplet/optical engine 对 ABF、substrate warpage、供电和散热要求极高。
3. **CPO optical engine 与 ELS。** Laser source、field replaceable ELSFP、耦合、热漂移和冗余机制决定 CPO 能否从 demo 走到量产。
4. **1.6T 光模块关键器件。** 200G/400G EML/EAM/MZM、SiPh PIC、InP laser/PD、isolator/filter、DSP 仍是短缺点。
5. **铜缆和连接器 SI/热管理。** NVLink copper spine、LACC、DAC/AEC 的布线、插拔、弯折半径、散热和现场维护限制 rack 设计。
6. **UEC/UALink/ESUN 互操作认证。** 标准有了不等于可采购，客户需要跨 switch、NIC、accelerator、cable、NOS、framework 的完整 compliance。
7. **Fabric debug 人才。** 大规模训练失败可能由单个 flap、tail latency、PFC storm、ECN 配置、collective imbalance 引发，排障人才稀缺。
8. **DPU/NIC firmware 与安全认证。** SuperNIC/DPU 需要和 hypervisor、container、storage、RDMA、PTP、安全策略深度耦合。
9. **液冷交换机/光模块热设计。** 高端 switch 和 XPO/CPO 都在突破传统风冷面板密度，冷板、泵、快接、漏液检测成为网络设备的一部分。
10. **长交期测试设备。** 1.6T MAC/FEC、224G SerDes、LLR/CBFC、CPO optical test 需要高端仪器，测试时间本身会成为产能。
11. **客户集中导致产能锁定。** NVIDIA、Meta、OpenAI、Google、AWS、Microsoft 可以预定产能，二线 neocloud 或企业客户拿货成本上升。
12. **地缘和出口管制。** 中国 AI 集群需求强，但高端 switch ASIC、NIC、DPU、HBM、光器件和EDA/IP可得性受限，国产替代难度高。

### 7.3 成本结构与价格传导

| 产品 | BOM/单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| NVLink/NVSwitch tray | NVSwitch ASIC 35-50%，高速 PCB/连接器/铜缆 20-30%，散热/电源 10-20%，测试/软件 10-20%。 | 是否随 GPU rack 打包、NVLink domain 大小、软件/collective 效率、缺货程度。 | 不是按单独端口定价，而是嵌入 NVL72 rack ASP，以 GPU 利用率和系统性能转嫁。 |
| InfiniBand switch/NIC | Switch ASIC/NIC ASIC 35-50%，光/铜端口 20-35%，系统板/电源/风扇 10-20%，UFM/软件/支持 5-15%。 | 端口速率、SHARP、拥塞控制、认证拓扑、NVIDIA GPU 绑定。 | 高端训练客户按 job completion time 和 uptime 支付溢价。 |
| Ethernet AI switch | Merchant switch ASIC 25-45%，optics/cages/connectors 25-40%，system/thermal 15-25%，NOS/支持 5-15%。 | 102.4T/204.8T silicon、radix、latency、PFC/ECN/UEC、CPO。 | Hyperscaler 用多供应商压价，但高端 silicon 和认证软件仍能溢价。 |
| SuperNIC/DPU | ASIC 30-45%，SerDes/PHY/PCB 15-25%，DRAM/flash 10-20%，software/security/offload 15-30%。 | RDMA 性能、storage/KV offload、安全、DOCA/SDK、firmware 可靠性。 | 随 AI server attach；DPU 能提升 GPU 利用率和安全隔离则可独立定价。 |
| 1.6T 光模块 | DSP/driver/TIA 25-40%，laser/modulator/PD/PIC 25-40%，封装/光学件 10-20%，测试 10-20%。 | DSP vs LPO/TRO、EML/SiPh 良率、温度、客户认证、短缺程度。 | 2026 短缺可涨价，2027 多供后 ASP 下行，价值向器件/DSP/测试集中。 |
| DAC/AEC/LACC | 铜线/连接器 30-50%，retimer/linear EQ 0-40%，组装 10-20%，测试 10-20%。 | 距离、速率、热、插拔可靠性、是否需要 retimer。 | 与 rack design 绑定，认证后切换成本高；普通 DAC 更易价格竞争。 |
| CPO/CPX/ELS | Switch ASIC/光引擎 40-60%，ELS/laser 10-20%，封装/连接器/散热 15-25%，测试/服务 10-20%。 | 光引擎良率、现场可维护、ELS 冗余、link stability、客户 field data。 | 用节能、可靠性、端口密度换溢价；若标准化多供，毛利回落。 |

## 8. 竞争格局与壁垒

### 8.1 市场结构

| 细分 | 头部集中度 | 主要公司 | 判断 |
|---|---|---|---|
| InfiniBand AI fabric | 极高，NVIDIA/Mellanox 近乎唯一高端供应 | NVIDIA | 绝对高壁垒，但 TAM 被 Ethernet 分流。 |
| NVLink/NVSwitch | 极高，NVIDIA 独占 | NVIDIA | 和 GPU、CUDA、MGX rack 绑定，最强定价权。 |
| AI Ethernet switch silicon | 高，Broadcom 第一梯队，NVIDIA/Cisco/Marvell 等竞争 | Broadcom、NVIDIA、Cisco、Marvell | 高端 102.4T/204.8T silicon 壁垒强，客户也希望多供。 |
| Ethernet switch systems | 中高，Arista/Cisco/NVIDIA/HPE/Celestica/Accton | Arista、Cisco、NVIDIA、HPE/Juniper、Celestica、Accton | 软件/NOS 和客户关系决定毛利，白盒竞争会压价格。 |
| 800G/1.6T 光模块 | 中，头部集中但多厂商竞争 | Coherent、Lumentum、Innolight、Eoptolink、AOI、Fabrinet 等 | 需求强但 ASP 下行风险高，上游器件更稳。 |
| UALink/开放 scale-up | 早期，格局未定 | AMD、Broadcom、Astera、Synopsys、Cisco、Intel、HPE、Meta、Microsoft、Google、AWS 等 | 2027 以后可能出现新 oligopoly。 |
| 高速铜/AEC/retimer | 中，连接器和芯片分层 | Amphenol、TE、Molex、Samtec、Credo、Astera、MACOM | 连接器规模壁垒 + retimer 芯片壁垒并存。 |

### 8.2 壁垒清单：为什么能定价

| 壁垒 | 具体解释 | 定价逻辑 |
|---|---|---|
| 协议和 collective offload | SHARP、NVLink all-to-all、UEC/UALink INC、RDMA congestion control 直接影响训练效率。 | 能把 GPU 利用率提高 1% 就对应数亿美元级客户价值。 |
| GPU/XPU 原生集成 | NVLink 与 NVIDIA GPU package/rack/软件深耦合；Broadcom XPU 与 Ethernet/PCIe/optics 协同设计。 | 客户买的是可工作的 rack，不是单个端口。 |
| 高速 SerDes 和 SI | 224G/448G PAM4 的 BER、jitter、loss budget、connector/backplane 都是硬门槛。 | 高速端口稀缺时，switch ASIC、retimer、测试工具有高毛利。 |
| 软件与可观测性 | UFM、DOCA、Mission Control、EOS、Apstra、SONiC tuning、job-aware routing。 | 大规模 AI fabric 的故障成本极高，运维软件可形成持续收入。 |
| 客户认证 | Hyperscaler 一个 fabric 认证周期通常跨 silicon、box、cable、NOS、framework、facility。 | 认证后切换成本高，供应商可维持 multi-year 价格。 |
| 规模与供给锁定 | NVIDIA/Broadcom/头部模块厂能提前锁 TSMC、封测、光器件、连接器产能。 | 二线客户需要为交期付溢价。 |
| 生态锁定 | CUDA/NCCL/NVLink/UFM 与 ROCm/UALink/UEC、Google/AWS internal stack 互不完全兼容。 | 性能和开发生态锁定比硬件价差更重要。 |
| 现场可靠性 | Link flap、thermal drift、connector failure、PFC storm 直接导致训练中断。 | 高可靠设备和支持服务可按 uptime 定价。 |

### 8.3 长期高 ROIC/高毛利层

长期最可能拥有高 ROIC 的层级：

1. **NVIDIA proprietary rack-scale fabric。** NVLink/NVSwitch/Quantum/Spectrum/ConnectX/BlueField/Mission Control 与 GPU 销售打包，客户很难拆分采购。
2. **Broadcom 类 AI fabric silicon 平台。** Tomahawk/Jericho/Thor/Agera/Sian/PCIe/optics + XPU 定制，把非 NVIDIA ASIC 生态的关键 I/O 抓在手里。
3. **高端 SerDes/DSP/retimer/IP。** 224G/448G 和 1.6T/3.2T 需要长期研发积累，客户认证强，毛利可高。
4. **CPO/ELS/optical engine。** 如果可维护性跑通，能从模块价格竞争中上移到封装和光引擎控制点。
5. **Fabric 管理软件与诊断工具。** 毛利最高，但需要依附硬件 installed base。

毛利较容易被压缩的层级：

- 普通白盒交换机 assembly。
- 标准 DAC/低端铜缆。
- 多供应商充分后的 800G/1.6T 通用光模块。
- 无软件/认证能力的单一硬件 OEM。

## 9. 2026 关键变化：3 个最可能拐点

### 拐点 1：Ethernet 反超从 scale-out 延伸到 scale-up

2025-2026 的核心变化不是“Ethernet 比 InfiniBand 便宜”，而是 Broadcom TH6/Ultra、UALink、UEC、ESUN/OCI 等把 Ethernet 或 Ethernet-like 技术推向 accelerator pod 内部。基准情景下，2026 仍是 NVLink 主导 scale-up，但非 NVIDIA ASIC 新增 rack 会更倾向 Ethernet scale-up。

最可能放量子方向：Broadcom Tomahawk/Jericho/Thor、UEC Ethernet、800G switch、1.6T optics、AEC/retimer。

### 拐点 2：Vera Rubin 让 NVLink 6 和 CPO 进入新一代 AI rack 采购

Rubin 2026H2 partner availability 将把 NVLink 6、ConnectX-9、BlueField-4、Spectrum-6/CPO 放进同一 rack/POD 产品。2026 不是 Rubin 大量收入年，但会决定 2027 供应链谁进入 reference design。

最可能放量子方向：NVSwitch 6、ConnectX-9、BlueField-4、Spectrum-6/SPX、CPO/ELS、液冷高密交换机。

### 拐点 3：开放标准进入产品化和合规验证

UALink 1.0、2.0、UEC 1.0/1.0.2 的意义在于从“paper spec”进入 IP、switch silicon、test、compliance、reference rack。2026 年直接收入小，但设计导入决定 2027-2028 份额。

最可能放量子方向：UALink IP、switch silicon、测试设备、fabric management、AMD Helios/Celestica/HPE 生态。

## 10. 2027 关键变化：3 个最可能拐点

### 拐点 1：1.6T 成为新增 AI fabric 主流，800G 开始价格竞争

2027 年新增 AI rack 若继续高速增长，1.6T 会从 high-end option 变成主流采购项。800G 仍大出货，但 ASP 与毛利压力上升。

最可能放量子方向：1.6T OSFP、200G/400G EML/SiPh、switch ASIC 200G lane、coherent campus DCI。

### 拐点 2：UALink/UALoE 与 Broadcom Ethernet scale-up 开始规模化

AMD Helios、Meta MTIA、OpenAI/Broadcom、其他 XPU 订单若按计划推进，2027 会出现第一批真正大规模非 NVIDIA scale-up fabric。它不一定打败 NVLink，但会改变采购基准。

最可能放量子方向：UALink switch/IP、Broadcom Ethernet scale-up、PCIe Gen6/CXL、retimer/AEC、fabric compliance。

### 拐点 3：CPO/CPX/XPO 从 pilot 走向高端 switch 量产

如果 2026 的 CPO/ELS 可靠性验证顺利，2027 高端 102.4T/204.8T switch 会将 CPO、CPX、NPO、XPO 作为节能和密度工具。若进展慢，pluggable 继续主流，但 XPO 会延长可插拔路线寿命。

最可能放量子方向：CPO optical engine、ELSFP laser、high-density connector、liquid-cooled pluggable、CPO test。

## 11. 头部公司清单

### 11.1 全栈与专有互联平台

| 方向 | 头部公司 |
|---|---|
| NVIDIA proprietary fabric | NVIDIA/Mellanox：NVLink/NVSwitch、Quantum InfiniBand、Spectrum-X、ConnectX、BlueField、LinkX、UFM/DOCA/Mission Control。 |
| Broadcom custom XPU + Ethernet | Broadcom：XPU、Tomahawk、Jericho、Thor、Agera、Sian DSP、CPO、PCIe switch/retimer。 |
| AMD open rack | AMD：Infinity Fabric、Pensando/Vulcano NIC、Helios、MI400/MI455X、UALink/UEC 生态。 |
| Google TPU fabric | Google：TPU ICI、Apollo OCS、Jupiter/Aquila 类数据中心网络、TPU pod。 |
| AWS fabric | AWS/Annapurna：NeuronLink、NeuronSwitch、EFA、Trainium/Inferentia。 |
| Microsoft Azure fabric | Microsoft：Maia/Cobalt/Azure 内部 AI fabric。 |
| Meta MTIA fabric | Meta + Broadcom：MTIA、Open Rack Wide、Ethernet scale-up/out/across。 |
| OpenAI custom accelerator | OpenAI + Broadcom：10GW custom accelerator/network systems。 |
| 中国超节点 | Huawei、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Moore Threads、Enflame、Iluvatar、MetaX。 |

### 11.2 Switch/NIC/DPU/Retimer/SerDes/IP

| 细分 | 公司 |
|---|---|
| Switch ASIC | NVIDIA, Broadcom, Cisco Silicon One, Marvell, Intel, HPE/Juniper, Huawei, Innovium legacy/Marvell。 |
| NIC/SuperNIC/DPU | NVIDIA ConnectX/BlueField, Broadcom Thor/NetXtreme, Marvell, AMD Pensando, Intel Ethernet/IPU, Cisco, Napatech, Xilinx/AMD Alveo legacy。 |
| PCIe/CXL/Retimer/AEC | Astera Labs, Broadcom, Credo, Parade, Montage/LXT, Microchip, Diodes, Semtech, MACOM, Spectra7。 |
| SerDes/IP/EDA | Synopsys, Cadence, Alphawave Semi, Rambus, Marvell, Broadcom, MediaTek, GUC, Alchip。 |
| UALink/UEC/标准生态 | AMD, Apple, AWS, Cisco, Google, HPE, Intel, Meta, Microsoft, Synopsys, Alibaba, Astera Labs, Broadcom, Arista, NVIDIA, Dell, Lenovo 等。 |

### 11.3 交换机系统、OEM/ODM、NOS

| 细分 | 公司 |
|---|---|
| 高端品牌交换机 | Arista, Cisco, NVIDIA, HPE/Juniper, Dell, Huawei, Nokia, Ciena。 |
| 白盒/ODM/系统集成 | Celestica, Accton/Edgecore, Quanta, Wiwynn, Foxconn, Inventec, Wistron, Pegatron, QCT, Supermicro, Lenovo, Jabil, Flex。 |
| NOS/fabric 软件 | Arista EOS, NVIDIA UFM/DOCA/Mission Control, Cisco NX-OS/SONiC, Juniper Apstra, SONiC community, HPE Slingshot, Cornelis Omni-Path, Broadcom SDK。 |

### 11.4 光互联、CPO、硅光、激光器

| 细分 | 公司 |
|---|---|
| 光模块/收发器 | Coherent, Lumentum, Fabrinet, Innolight/中际旭创, Eoptolink/新易盛, Applied Optoelectronics, Accelink/光迅科技, 华工科技, Hisense Broadband, Source Photonics, Linktel/联特科技, Cambridge Industries, HG Genuine。 |
| 光芯片/激光器/器件 | Coherent, Lumentum, Broadcom, Marvell, Cisco/Acacia, MACOM, Semtech, MaxLinear, OpenLight, Ayar Labs, Ranovus, Celestial AI, Avicena, Lightmatter, POET, 天孚通信, 仕佳光子。 |
| CPO/CPX/NPO/OCI | NVIDIA, Broadcom, Coherent, Lumentum, Marvell, Ciena, Molex, Samtec, TeraHop, OpenLight, Ayar Labs, Ranovus, Celestial AI。 |
| Coherent/scale-across | Ciena, Nokia, Cisco/Acacia, Marvell, Infinera/Nokia, Lumentum, Coherent, Fujitsu。 |
| OCS/光交换 | Google Apollo ecosystem, Calient, Polatis/HUBER+SUHNER, Coherent, MEMS/optical switch suppliers, Ciena/Nokia line systems。 |

### 11.5 铜互联、连接器、线缆和热管理

| 细分 | 公司 |
|---|---|
| 连接器/高速线缆 | Amphenol, TE Connectivity, Molex, Samtec, Luxshare, BizLink, Foxconn Interconnect, JAE, Hirose, Rosenberger。 |
| DAC/AEC/LACC 芯片 | Credo, Astera Labs, Broadcom, MACOM, Semtech, Spectra7, Parade, MaxLinear。 |
| 高密光纤管理 | Corning, Senko, US Conec, AFL, CommScope, Panduit, Legrand, nVent。 |
| 液冷网络设备配套 | Vertiv, CoolIT, Boyd, Delta, Auras, Schneider, Eaton, nVent, Modine。 |

### 11.6 测试、认证与生产设备

| 细分 | 公司 |
|---|---|
| 高速网络测试 | Keysight, VIAVI, Spirent, Anritsu, Tektronix, EXFO。 |
| 半导体/封装测试 | Advantest, Teradyne, FormFactor, Chroma, Cohu, MPI。 |
| 光电测试/生产 | Coherent, Keysight, VIAVI, Luna, Santec, Yokogawa, Newport/MKS。 |
| 合规/互操作 | UALink Consortium, UEC, Ethernet Alliance, OCP, OIF, IEEE, PCI-SIG。 |

## 12. 投资排序与跟踪指标

### 12.1 未来 12 个月最确定

1. **NVIDIA networking stack：** NVLink/NVSwitch、Quantum-X800、Spectrum-X、ConnectX/BlueField，受益于 GB300 和 Rubin。
2. **Broadcom AI fabric silicon：** Tomahawk 6/Ultra、Jericho、Thor、Agera、Sian DSP、PCIe/retimer，受益于 Meta/OpenAI/custom XPU。
3. **1.6T 光模块与上游器件：** 2026 导入、2027 放量，器件/DSP/测试优于普通组装。
4. **高速铜/AEC/连接器：** rack 内 density 提升，NVL72/Helios/Trainium3 都需要更复杂铜互联。
5. **测试认证：** UEC/UALink/CPO/3.2T 的复杂度放大测试设备和服务价值。

### 12.2 未来 12-24 个月赔率最高

1. **UALink/UALoE switch/IP。** 小基数，若 AMD Helios 和非 NVIDIA XPU 规模化，弹性很大。
2. **CPO/CPX/NPO/OCI。** 若 field service 和 ELS 可靠性跑通，会从 pilot 变成高端 switch 默认选项。
3. **OCS/光交换。** 若从 Google TPU 扩散到通用 AI fabric，会重写部分电交换价值分配。
4. **Fabric software。** GPU 利用率和故障隔离直接影响 token revenue，软件价值会从“免费工具”变为 SLA 工具。

### 12.3 关键跟踪指标

- NVIDIA networking revenue 是否继续高于 Data Center compute 增速。
- Quantum-X800 与 Spectrum-X 在新建集群中的 mix。
- Broadcom Tomahawk 6/Ultra/Jericho 设计赢单数量，以及 Meta/OpenAI 项目实际 rack 出货。
- UALink 2.0 规范和合规计划是否按 2026Q2/Q3 落地。
- AMD Helios/Celestica/HPE 是否在 2026H2 交付 early customer rack。
- 1.6T 光模块出货是否从 2026 的 >500 万只走向 2027 的 1,500-2,500 万只。
- CPO/CPX/XPO 是否有真实 field deployment 和故障率数据。
- Ethernet AI back-end switch sales 是否继续超过 InfiniBand 两倍以上。
- OpenAI/Meta/Google/AWS/Microsoft capex 是否继续上修，以及是否前置 2027 需求。

## 13. 主要来源

| 来源 | 关键信息 |
|---|---|
| [NVIDIA Quantum-X800 InfiniBand Platform](https://www.nvidia.com/en-us/networking/products/infiniband/quantum-x800/) | 800G InfiniBand、144 ports、ConnectX SuperNIC、SHARP v4、CPO 方向。 |
| [NVIDIA NVLink and NVLink Switch](https://www.nvidia.com/en-us/data-center/nvlink/) | NVLink 6 每 GPU 3.6TB/s、NVL72 260TB/s、NVLink Fusion。 |
| [NVIDIA Vera Rubin Opens Agentic AI Frontier](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | 七类芯片 full production、NVL72、LPX、STX、SPX、DSX、2026H2 供货。 |
| [NVIDIA Vera Rubin POD 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | 40 racks、1,152 GPUs、60 exaflops、10PB/s scale-up、MGX copper spines、Spectrum-6 102.4T CPO。 |
| [NVIDIA NVLink Fusion](https://www.nvidia.com/en-us/data-center/nvlink-fusion/) | 第三方 CPU/XPU 接入 NVLink rack-scale architecture，72 XPUs all-to-all。 |
| [NVIDIA FY2026 Q4 CFO Commentary](https://s201.q4cdn.com/141608511/files/doc_financials/2026/Q426/Q4FY26-CFO-Commentary.pdf) | Q4 networking $11.0B、FY2026 networking $31.4B、毛利率与收入。 |
| [Broadcom OFC 2026 AI infrastructure release](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai) | 3.5D XPU、102.4T CPO、400G/lane DSP、Thor Ultra、Agera、PCIe Gen6、OCI MSA。 |
| [Broadcom Tomahawk 6 production volume](https://investors.broadcom.com/news-releases/news-release-details/broadcom-now-shipping-worlds-first-1024-tbps-switch-production) | 102.4T switch production、512 XPU single-hop scale-up、128K XPU two-tier scale-out。 |
| [Broadcom TH6-Davisson CPO](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-tomahawkr-6-davisson-industrys-first-1024) | 第三代 CPO、102.4Tbps、70% optical interconnect power reduction、512 XPU scale-up。 |
| [Broadcom-Meta MTIA partnership](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-extended-partnership-meta-deploy-technology) | Meta >1GW 首期、多 GW rollout、Ethernet scale-up/out/across。 |
| [OpenAI-Broadcom 10GW collaboration](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-announce-strategic-collaboration-deploy-10) | OpenAI 自研 accelerator + Broadcom Ethernet，2026H2 起部署，2029 完成。 |
| [UALink 200G 1.0 Specification PR](https://ualinkconsortium.org/wp-content/uploads/2025/04/UALink-1.0-Specification-PR_FINAL.pdf) | 200G per lane、1,024 accelerators/pod、93% effective peak bandwidth、成员和董事会。 |
| [UALink roadmap 2026](https://ualinkconsortium.org/blog/ualink-roadmap-insights-accelerating-open-scalable-ai-networking-1296/) | 2.0 计划 2026Q2、INC、management/chiplet spec、3.0 目标 2027。 |
| [Ultra Ethernet Consortium 1.0](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/) | UEC 1.0 specification、AI/HPC Ethernet stack、compliance/interop。 |
| [Ultra Ethernet Consortium FAQ](https://ultraethernet.org/) | UEC 目标、AI scale-out network、Ethernet interoperability。 |
| [Dell'Oro AI back-end switch forecast](https://www.prnewswire.com/news-releases/ai-back-end-switch-market-will-push-past-100-billion-by-2030-according-to-delloro-group-302678344.html) | AI back-end switch 2030 >$100B、Ethernet 预计在 scale-up/out 主导、800G/1.6T/3.2T。 |
| [Dell'Oro 2Q25 InfiniBand/Ethernet](https://www.prnewswire.com/news-releases/infiniband-switch-sales-surged-in-2q-2025-while-ethernet-maintains-market-lead-in-ai-back-end-networks-according-to-delloro-group-302546136.html) | InfiniBand 2Q25 增长但 Ethernet 领先，Celestica/NVIDIA/Arista 领先 Ethernet segment。 |
| [IDC Ethernet switch market 4Q25](https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/) | 2025 Ethernet switch $55.1B、data center $32.5B、NVIDIA data center Ethernet share 15.2%。 |
| [AMD-Celestica Helios](https://www.amd.com/en/newsroom/press-releases/2026-3-16-amd-and-celestica-announce-collaboration-to-a.html) | Helios scale-up switch 使用 UALoE，Celestica R&D/design/manufacturing。 |
| [AMD Helios OCP Open Rack](https://ir.amd.com/news-events/press-releases/detail/1261/amd-showcases-helios-rack-scale-platform-built-on-the-open-compute-project-open-rack-for-ai-introduced-by-meta) | Helios 使用 OCP、UALink、UEC，AMD Instinct/EPYC/Pensando。 |
| [HPE AMD Helios](https://www.hpe.com/us/en/newsroom/press-release/2025/12/hpe-accelerates-ai-deployments-with-first-amd-helios-ai-rack-scale-architecture-with-open-scale-up-networking-built-with-broadcom.html) | HPE 2026 提供 AMD Helios，open scale-up Ethernet networking with Broadcom。 |
| [OFC 2026 本地报告](../conference_update/ofc_2026_conference_update.md) | 1.6T、3.2T、CPO、XPO、coherent、OCS 和市场估算。 |
| [NVIDIA GTC 2026 本地报告](../conference_update/nvidia_gtc_2026_research.md) | Rubin、NVLink、Spectrum-X、LPX、STX、DSX 与财务/市场口径。 |
| [AI 芯片路线图本地报告](../ai_chip_research_2026_2027.md) | 2026-2027 头部 AI 芯片与平台的出货/技术路径背景。 |
| [Xcelerated Compute Show 2026 本地报告](../conference_update/xcelerated_compute_show_2026_report.md) | 开放互联、UEC/UALink、AI backend networking、memory wall、neocloud 信号。 |

## 14. 读数注意事项

1. 本报告把 NVLink/NVSwitch 等随 rack 出货的互联价值拆出估算，但现实收入中大量价值会被计入 NVIDIA GPU/rack 系统 ASP。
2. Broadcom 的 AI revenue 同时包含 custom XPU、networking、PCIe、optics 等，不应和本报告所有子项简单相加。
3. InfiniBand 和 Ethernet 的份额取决于口径：端口数、switch revenue、AI back-end switch revenue、完整 fabric revenue 可能给出不同结论。
4. 未来 3 个月数字偏订单/出货 run-rate；未来 1 年和 2 年数字是本报告在乐观 AI 基建假设下的市场池预测，不是保证收入。
5. 本报告有意采用偏乐观 AI 基建情景：假设 2026-2027 agentic inference、长上下文、多模态、主权 AI 和自研 ASIC 均继续推高算力需求。
# 行业调研：【LPO/LRO线性光模块】

> 截至日期：2026-05-08  
> 研究对象：Linear Pluggable Optics（LPO）、Linear Receive Optics（LRO/TRO/RTLR）及其在 800G、1.6T、3.2T、XPO、CPO/NPO/CPX、OCS 光网络中的位置。  
> 口径说明：本文优先采用公司发布会、OFC 2026 一手资料、LPO MSA/OIF 标准文件、财报/公告、高管或公司披露；市场规模用 Cignal AI、TrendForce、LightCounting 等公开摘要交叉校验。凡没有直接公开拆分的数据，采用“AI 计算中心建设极度乐观”的自建测算，并明确标注为测算。

## 0. 投资结论先行

**一句话判断：LPO/LRO 是 2026-2027 AI 网络降功耗、降时延、降成本的关键路线，但 2026 最可兑现的是 LRO/TRO，不是纯 LPO。** 纯 LPO 取消模块内 DSP/CDR，理论弹性最大；LRO 只取消接收侧 retimer/DSP，保留发送侧 retiming，在功耗、良率、互通和客户认证之间更均衡。OFC 2026 的一手信号显示，1.6T FRO/LRO/LPO 已经进入多厂商互通展示，200G/lane 是 2026 主战场；3.2T/400G/lane 已经开始样品和器件验证，但大规模收入更偏 2027H2-2028。

**2026 最可能的技术路径排序：**

| 排名 | 技术路径 | 2026 判断 | 投资含义 |
|---:|---|---|---|
| 1 | 1.6T OSFP FRO + LRO/TRO 并行 | 最确定放量。FRO 负责最稳互通，LRO 负责低功耗/低延迟/低 TCO。 | 模块厂、LRO DSP、TIA/driver、EML/SiPh PIC、测试设备最先兑现。 |
| 2 | 800G LPO/低功耗线性模块 | 在受控 host、短距、单客户环境率先放量，但总 ASP 低于 1.6T。 | 适合看功耗极限、低成本和客户定制，不适合简单按全市场替代。 |
| 3 | 1.6T 纯 LPO | 样品和局部导入明确，但互通、链路预算、host SerDes/PCB 损耗仍限制规模。 | 高弹性期权；真正利润在 host ASIC/SerDes、线性 TIA/driver 和测试调参。 |
| 4 | CPO/CPX/NPO/ELS | 2026 是 NVIDIA/Broadcom/Coherent/Lumentum 生态 pilot，收入更多来自 ELS、optical engine 和连接器。 | 长期壁垒高；短期不应替代 1.6T pluggable 的放量假设。 |
| 5 | 12.8T XPO | 2026 标准和演示，2027 小批量，2028 才可能广泛部署。 | 可插拔阵营的高密度延寿路线，连接器/液冷/FAU 价值上升。 |
| 6 | 3.2T/400G-per-lane | 2026 器件/PIC/DSP 样品，2027 客户 qual 和 live demo，2028 扩产。 | 先买上游器件、DSP、测试设备，后买模块放量。 |

**核心投资判断：**

1. **LRO 是 2026 线性光模块的主升浪。** Eoptolink 把 LRO 定义为 LPO 与 fully retimed optics 之间的中间路径，称取消接收路径 DSP 可使模块功耗约降 30%；Lumentum 1.6T 2xDR4 TRO 产品典型功耗为 16W，显著低于其 fully retimed 版本常见 20W+ 级别。
2. **纯 LPO 的确定性弱于 LRO，但期权更大。** LPO MSA 的逻辑是把 retiming、FEC、DAC/ADC、equalization 更多交给 host ASIC，模块端更便宜、更低功耗、更低延迟；但 OIF CEI-448G 框架也提醒，线性接口对 channel impairment 更敏感，448G/lane 纯 LPO 会面对更严苛约束。
3. **AI 集群需求足够大，能容纳多技术并行。** Cignal AI 预计 2026 年 800GbE 模块超过 2,000 万只，1.6TbE 超过 500 万只；TrendForce 预计 800G 及以上光模块出货占比从 2024 年 19.5% 升至 2026 年 60%+。这不是单一路线胜利，而是 FRO、LRO、LPO、OCS、CPO、coherent scale-across 一起放量。
4. **价值捕获不只在“组装模块”。** 长期高 ROIC 更可能在 224G/400G SerDes、LRO DSP、线性 TIA/MZM driver、EML/EAM/SiPh PIC、高功率 CW laser/ELS、FAU/连接器、自动化测试与客户认证层。纯模块组装会在 2026H2-2027 面临 ASP 下行。
5. **极度乐观情景下，LPO/LRO 收入池 24 个月可达 $45B-$75B。** 这里包括 800G/1.6T LPO/LRO 模块、LRO DSP、线性 TIA/driver、SiPh/InP 光引擎、ELS/连接器和测试服务；若只算模块出货收入，24 个月极度乐观区间约 $28B-$48B。

## 1. 技术定义：FRO、LRO/TRO、LPO 到底差在哪

| 路线 | 模块内 DSP/retimer | 功耗/时延 | 优点 | 主要约束 | 2026 适配场景 |
|---|---|---|---|---|---|
| FRO fully retimed optics | TX/RX 两侧都 retime，模块内完整 DSP | 功耗最高、时延最高但最稳 | 互通强、链路预算宽、客户认证容易 | BOM 高、热设计压力大 | 1.6T 早期大客户、多供应商互通、复杂链路 |
| LRO/TRO/RTLR | 发送侧 retime，接收侧 linear | 功耗/时延低于 FRO | 比 LPO 稳，比 FRO 省电；仍保留发送端信号整形 | 接收侧 host 能力、测试校准和链路损耗敏感 | 2026 最可能大规模采用的线性路线 |
| LPO | TX/RX 均 linear，模块不放 DSP/CDR | 功耗和时延最低 | 模块成本低、功耗低、适合 AI fabric 极高密度 | 强依赖 host ASIC/SerDes/FEC/NLC、互通和可插拔生态仍需成熟 | 800G 受控场景、1.6T 小批量/专用客户 |
| NPO/CPX/CPO | 光引擎靠近或共封装到 ASIC | 电通道最短，系统功耗最低 | 高密度、低时延、长期解决电通道瓶颈 | 可维护性、ELS 冗余、热漂移、标准和 field service | 2026 pilot，2027 高端 switch 导入 |
| XPO | 12.8T 液冷大 form-factor 可插拔 | 取决于 FRO/LRO/LPO 配置 | 保留可维护性，面板密度 4x OSFP，支持 400W/module 冷却 | 标准新、液冷服务和客户 qual 未成熟 | 2026 展示/生态，2027 小批量 |

LPO MSA 官方定义的关键点是：取消可插拔模块内 DSP，把电/光互通要求定义在模块和网络设备两侧，从 100Gb/s per lane 起步并延伸到 200Gb/s per lane；其收益是降低功耗、降低时延和降低模块成本，同时保留 pluggable 灵活性。OIF CEI-448G 框架则给出更保守的系统视角：LPO/RTLR 对 AI/HPC 有吸引力，但线性接口对通道损伤敏感，448G 时代的 connector、PCB、FEC、调制格式和测试方法会成为硬门槛。

## 2. AI 芯片路线背景下的光互联需求

本节沿用项目内已有 `ai_chip_research_2026_2027.md` 的 2026-2027 芯片路线，不再外搜。对 LPO/LRO 来说，真正重要的不是单芯片 FLOPS，而是 rack/pod 内 scale-up、rack 间 scale-out、园区 scale-across 的带宽和功耗约束。

| 2026-2027 主要 AI 芯片/平台 | 光互联相关路径 | 对 LPO/LRO 的含义 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | rack 内 NVLink/铜为主，scale-out 用 800G/1.6T；Spectrum-6/CPO 从交换侧进入 | 2026 拉动 1.6T OSFP/FRO/LRO；CPO 对 pluggable 形成长期替代压力。 |
| AWS Trainium2 | Rainier 大规模，EFA/以太网 scale-out，rack 内私有 NeuronLink | 以标准 800G/1.6T scale-out 模块为主，LRO 比 LPO 更容易进客户认证。 |
| Google TPU v7 Ironwood | 3D Torus + Apollo OCS；短距铜，rack 间全光网络 | OCS 架构放大 800G/1.6T 模块数量，且升级带宽可通过换模块实现。 |
| NVIDIA GB200/B200 | 既有 NVL72 存量延续，scale-out 光模块 | 800G 主力、1.6T 渗透，低功耗 LRO 有节能意义。 |
| Huawei Ascend 910C/950 | SuperPoD/Cluster 通过系统互连弥补单芯片差距 | 中国本土光模块、LPO/LRO/硅光、国产 DSP/驱动芯片有国产替代机会。 |
| Cambricon MLU590/690 | OAM/MLU-Link + 数据中心光模块 | 国产 AI 集群若上 10k 卡，光模块弹性高，但标准化和客户认证偏本土。 |
| AMD MI350/MI400 | MI350 2026 放量；MI400/Helios 2026H2-2027，UALink/以太网 | 以 1.6T scale-out + 未来 UALink optical scale-up 为主，LRO/XPO/OCI 受益。 |
| AWS Trainium3 | 144 芯片 UltraServer，Neuron Fabric | 更高密度 rack 将抬高 1.6T 端口数；LRO 是功耗和互通折中。 |
| Meta MTIA/Broadcom XPU | Broadcom Ethernet/SerDes 强，OCP rack 标准 | 自研 ASIC 更愿意共同定义 host 与 optics，纯 LPO 导入概率高于商用通用 GPU 客户。 |
| Microsoft Maia / OpenAI-Broadcom ASIC | 推理优先、GW 级规划、可能深度定制网络 | 2027 起会推动 OCI、CPO/NPO、LPO/LRO 共同标准化；但 2026 仍先买成熟 pluggable。 |

**结论：2026 LPO/LRO 的真实需求来自“1.6T 端口数膨胀 + 每瓦 token 经济性”，不是单纯替代 DSP。** Blackwell/GB300、Trainium、TPU、MI350、MTIA、Maia 等同时放量，会把 800G/1.6T 光互联从可选升级变成 AI rack 的供给约束之一。

## 3. 2026 机遇和挑战

### 3.1 需求锚点

| 来源 | 关键数字/事实 | 对 LPO/LRO 的含义 |
|---|---|---|
| Cignal AI 2026-01 | 2025 光通信组件收入接近 $25B，datacom 超过 $18B，coherent module 接近 $6B；400G+ datacom 模块 2025 年约 4,200 万只；2026 年 800GbE 超过 2,000 万只，1.6TbE 超过 500 万只。 | 1.6T 不是实验室阶段，2026 已有百万级出货基线。 |
| TrendForce 2026-02 | 800G 及以上光模块出货占比从 2024 年 19.5% 升至 2026 年 60%+；Google 近 400 万 TPU 对应 800G+ 模块需求超过 600 万只。 | TPU/OCS 让光模块 attach rate 上升，且每次升级只需换更高速模块。 |
| Semtech 2026-03 | 引用 LightCounting 口径称 linear optical transceivers 与 CPO/NPO optics for AI cluster networks 从 2024 年 $5B 到 2026 年超过 $10B。 | 线性光学已是百亿美元级赛道，不是边缘小品类。 |
| NVIDIA 2026 | Spectrum-X Ethernet Photonics 2026H2 可用，最高 409.6Tb/s；CPO 相对 pluggable 提供 5x 光功率效率、10x resiliency。 | 长期会压缩传统 pluggable，但短期同时验证“光互联进入系统架构层”。 |
| 本项目 AI DC 建设模型 | 美国主导网络与光互联订单 2026 务实 $65B-$100B，2027 $100B-$160B；乐观 2026 $105B-$165B，2027 $170B-$280B。 | 高速光模块和交换机订单弹性高于服务器 CapEx。 |

### 3.2 技术成熟和放量时间

| 技术 | 2026-05 状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|---|
| 800G FRO | 成熟量产 | 2026 继续主力；2027 ASP 下行 | 2026-2027 仍有大量 AI 追加 | 作为成本敏感和存量扩容继续高量 |
| 800G LPO | LPO MSA 100G/lane 规范已发布，Adtran/Infraeo/Innolight 等有产品/演示 | 2026 受控客户导入，2027 扩大 | 2026H2 进入更多 switch/NIC 白名单 | 若 host SerDes/FEC 成熟，2027 成为短距默认低功耗路线 |
| 1.6T FRO | Coherent/Lumentum/Eoptolink/Semtech/NVIDIA 生态明确展示 | 2026H2 快速爬坡，2027 主流 | 2026 500 万只以上，2027 2,000 万只级 | 2027 新增 AI 集群默认配置，短缺延续 |
| 1.6T LRO/TRO | Eoptolink、Lumentum、Credo、Semtech、ATOP、Coherent 等明确产品/演示 | 2026H2 商用导入，2027 占 1.6T 20%-35% | 2027 占 35%-50% | 2027 成为 1.6T 新项目主力之一 |
| 1.6T LPO | OpenLight 1.6T DR8 LRO/LPO beta sampling，Eoptolink OFC 2026 展示 1.6T LPO 系列 | 2026 小批量/客户 qual，2027 5%-15% 渗透 | 2027 15%-25% 渗透 | 大客户定制 host 通过认证，2027 25%-35% |
| 224G linear TIA/driver | Semtech CEI-224G-Linear/LPO-MSA compliant，Credo Cardinal/Bluebird | 2026 伴随 1.6T LRO/LPO 增长 | 2027 成为线性模块核心瓶颈 | 毛利率维持高位，客户预付锁产能 |
| 3.2T/400G/lane | Broadcom Taurus、Coherent 400G/lane、OpenLight 3.2T PIC alpha/beta 时间表 | 2026 样品，2027 qual/demo，2028 放量 | 2027H2 小批量收入 | 2027 形成 $1B-$3B 早期市场 |
| CPO/CPX/NPO/ELS | NVIDIA、Coherent、Lumentum、Open CPX MSA、TE 明确生态 | 2026 pilot，2027 高端 switch 小规模 | 2027 多个 AI cluster 部署 | 2027 成为高端 AI switch 默认路线之一 |
| XPO 12.8T | Arista XPO MSA、Eoptolink/Linktel 等展示 | 2026 标准，2027 小批量，2028 放量 | 2027H2 高端 AI fabric 导入 | 2027 形成 $2B+ 需求 |

### 3.3 2026 的关键挑战

1. **互通和客户认证。** LPO 把更多链路责任放到 host ASIC 和系统端，跨 switch、NIC、模块、FEC、CMIS、调参工具的互通难度高于 FRO。
2. **链路预算和 channel loss。** 224G/lane 已经需要很强的 PCB、connector、SerDes、equalization 能力；448G/lane 下 OIF 已经提示 PAM4、connector bandwidth 和更高阶调制会成为新瓶颈。
3. **测试时间。** LPO/LRO 不再是“模块独立黑盒”，需要系统级校准、BER、FEC margin、thermal drift、host startup protocol、field diagnostics，测试设备和工程师是瓶颈。
4. **客户偏好分裂。** NVIDIA/Broadcom/Arista/Google/Meta/Microsoft/AWS 对 host、switch、optics 的控制程度不同，导致 FRO/LRO/LPO/CPO 并行，库存风险上升。
5. **供应链细分瓶颈。** 200G/400G EML/EAM/MZM、InP laser/PD、高功率 CW laser/ELS、线性 TIA/driver、3nm/2nm DSP、FAU/高密连接器、液冷结构件、自动化测试都可能卡量。
6. **ASP 下行。** LightCounting/Cignal 类机构均提示供应追上后价格会下行。需求强不等于模块厂毛利必然上行，尤其是 2027 多供给扩散后。

## 4. 已开始放量或接近放量的关键产品

以下市场规模为本文测算，包含模块、关键芯片/器件和部分测试/封装价值；渗透率口径为“800G+ datacom/AI cluster 光互联收入池中的占比”。

### 4.1 已放量产品市场规模和渗透率

| 产品/技术 | 主要公司 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 800G FRO/传统 DSP 光模块 | Innolight、Eoptolink、Coherent、NVIDIA、AOI、Hisense、Accelink、Fabrinet | B $4B-$6B / O $6B-$8B / X $8B-$11B | B $18B-$25B / O $24B-$34B / X $32B-$45B | B $25B-$38B / O $35B-$55B / X $55B-$80B | 2026 仍为 800G+ 收入主力，但 2027 占比被 1.6T 吃掉 |
| 800G LPO/低功耗线性模块 | Adtran、Innolight、Infraeo、Eoptolink、Genuine Optics、Accelink、Hisense、Juniper/Arista 生态 | B $0.2B-$0.5B / O $0.5B-$0.9B / X $0.9B-$1.5B | B $1B-$2.5B / O $2.5B-$5B / X $5B-$8B | B $2B-$5B / O $5B-$10B / X $10B-$18B | 800G 线性渗透从低个位数到 2027 的 10%-25% |
| 1.6T FRO OSFP/DR8/2xDR4 | Coherent、Lumentum、Eoptolink、Innolight、NVIDIA、AOI、Hisense、CIG、Linktel、ATOP | B $1.2B-$2.2B / O $2.2B-$3.8B / X $3.8B-$6B | B $7B-$11B / O $11B-$18B / X $18B-$28B | B $14B-$25B / O $25B-$42B / X $42B-$65B | 1.6T 总量 2026 >500 万只，2027 从导入变主流 |
| 1.6T LRO/TRO | Eoptolink、Lumentum、Credo/Jabil、Coherent、Semtech 生态、ATOP、Genuine Optics、Infraeo | B $0.5B-$1.2B / O $1.2B-$2.2B / X $2.2B-$3.8B | B $3B-$6B / O $6B-$11B / X $11B-$18B | B $8B-$16B / O $16B-$30B / X $30B-$48B | 1.6T 内渗透 2026 10%-25%，2027 25%-50%，极超 60% |
| 1.6T LPO | OpenLight、Eoptolink、Infraeo、Genuine Optics、Innolight、Accelink、Hisense、Arista/Broadcom/NVIDIA 生态 | B $0.1B-$0.4B / O $0.4B-$0.9B / X $0.9B-$1.8B | B $0.8B-$2B / O $2B-$5B / X $5B-$10B | B $3B-$8B / O $8B-$18B / X $18B-$32B | 1.6T 内渗透 2026 <10%，2027 10%-25%，极超 35% |
| 224G 线性 TIA/MZM driver | Semtech、MACOM、MaxLinear、TI、Broadcom、Marvell、Credo、Lumentum 内部 | B $0.4B-$0.8B / O $0.8B-$1.3B / X $1.3B-$2B | B $1.8B-$3.2B / O $3.2B-$5.5B / X $5.5B-$8B | B $4B-$7B / O $7B-$12B / X $12B-$20B | 随 1.6T LRO/LPO 上升，attach 接近 100% |
| LRO DSP/低功耗 optical DSP | Credo Bluebird/Cardinal、Broadcom、Marvell、NVIDIA/内部、Cisco/Acacia | B $0.4B-$0.9B / O $0.9B-$1.6B / X $1.6B-$2.8B | B $2B-$4B / O $4B-$7B / X $7B-$11B | B $5B-$9B / O $9B-$16B / X $16B-$26B | LRO 渗透越高，DSP 从“完整模块 DSP”转向“发送侧/监控/低功耗 DSP” |
| 200G EML/EAM/SiPh PIC/InP laser | Coherent、Lumentum、Broadcom、OpenLight/Tower、Semtech、Innolight/Eoptolink 内部、POET、DustPhotonics | B $1B-$2B / O $2B-$3B / X $3B-$5B | B $5B-$8B / O $8B-$13B / X $13B-$20B | B $10B-$18B / O $18B-$32B / X $32B-$50B | 是 800G/1.6T/FRO/LRO/LPO 共用瓶颈 |

### 4.2 增速和利润率预测

| 产品/技术 | 未来 12 个月增长：基准/乐观/极超 | 未来 24 个月增长：基准/乐观/极超 | 当前利润率 | 未来利润率判断 |
|---|---:|---:|---|---|
| 800G FRO | +20%-40% / +40%-60% / +70% | +10%-30% / +30%-50% / +60% | 模块毛利 25%-40%，头部高端客户可更高 | 2027 ASP 下行，毛利向 22%-35% 回落 |
| 800G LPO | +80%-150% / +150%-250% / +300% | +100%-200% / +250%-400% / +500% | 早期 30%-45%，但价格低于 FRO | 若良率稳定，毛利 32%-48%；若互通差，返工吃掉利润 |
| 1.6T FRO | +100%-180% / +180%-280% / +350% | +120%-250% / +300%-500% / +700% | 早期 35%-45%，优质客户可更高 | 2026H2 强，2027 多供给后 28%-40% |
| 1.6T LRO/TRO | +200%-350% / +350%-600% / +800% | +300%-700% / +800%-1,200% / +1,500% | 35%-48%；Lumentum/Coherent 类垂直整合更高 | 2027 若成主流，领先供应商 40%-50%；二线模块厂 25%-35% |
| 1.6T LPO | +300%-600% / +700%-1,000% / +1,500% | +500%-1,000% / +1,200%-2,000% / +3,000% | 不稳定，样品期 30%-50% | 标准化后模块毛利会被压，host/IC/测试层更赚钱 |
| 线性 TIA/driver | +80%-150% / +150%-250% / +350% | +150%-350% / +400%-700% / +900% | 半导体毛利 55%-70% | 若供不应求，头部 60%-75% 可维持 |
| LRO DSP | +100%-220% / +250%-400% / +600% | +200%-500% / +600%-1,000% / +1,500% | 55%-70% | 低功耗/telemetry/diagnostics 形成定价权 |
| 光芯片/PIC/laser | +50%-100% / +100%-180% / +250% | +100%-250% / +300%-600% / +900% | 35%-55%，高功率/高良率产品 55%-70% | 产能和客户认证决定溢价；InP/EML/CW laser 是高壁垒 |

## 5. 在研关键产品和未来快增长细分

### 5.1 在研产品/技术市场预测

| 在研方向 | 2026-05 状态 | 未来 3 个月市场规模 | 未来 12 个月市场规模 | 未来 24 个月市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 3.2T DR8 / 400G-per-lane optical engine | Broadcom Taurus、Coherent 400G/lane、OpenLight 3.2T PIC alpha；OpenLight beta 预计 2026 Q4 | B <$0.1B / O $0.1B-$0.2B / X $0.2B-$0.4B | B $0.3B-$0.8B / O $0.8B-$2B / X $2B-$4B | B $2B-$6B / O $6B-$15B / X $15B-$30B | 2026 几乎 0，2027 小批量，2028 规模化 |
| XPO 12.8T 液冷可插拔 | Arista MSA，Eoptolink/Linktel/Coherent 等展示 | B <$0.05B / O $0.05B-$0.15B / X $0.15B-$0.3B | B $0.2B-$0.8B / O $0.8B-$2B / X $2B-$4B | B $2B-$5B / O $5B-$15B / X $15B-$28B | 2027 在 204.8T switch/高端 AI fabric 小批量 |
| CPO/CPX/NPO optical engines | NVIDIA CPO、Coherent 6.4T socketed CPO、Open CPX MSA、TE CPO/backplane 展示 | B $0.2B-$0.5B / O $0.5B-$1B / X $1B-$2B | B $1B-$3B / O $3B-$7B / X $7B-$12B | B $5B-$12B / O $12B-$30B / X $30B-$55B | 2026 pilot，2027 高端 switch 5%-15%，极超 25% |
| ELS/高功率 CW laser/ELSFP | Lumentum、Coherent、POET、Broadcom、Nubis 等推动 | B $0.2B-$0.5B / O $0.5B-$0.9B / X $0.9B-$1.5B | B $1B-$2B / O $2B-$4B / X $4B-$7B | B $3B-$8B / O $8B-$18B / X $18B-$30B | CPO/NPO attach 越高，ELS 成为必配 |
| OCI optical scale-up | AMD、Broadcom、Meta、Microsoft、NVIDIA、OpenAI 等 2026-03 成立 OCI MSA | B <$0.05B / O $0.1B / X $0.2B | B $0.2B-$0.7B / O $0.7B-$2B / X $2B-$5B | B $3B-$8B / O $8B-$20B / X $20B-$40B | 2027 起 high-end XPU/GPU scale-up 光化 |
| OCS/MEMS optical switching | Google Apollo 最明确，Lumentum/Coherent 等供应链受益 | B $0.3B-$0.8B / O $0.8B-$1.5B / X $1.5B-$2.5B | B $1.5B-$4B / O $4B-$8B / X $8B-$15B | B $5B-$12B / O $12B-$25B / X $25B-$45B | 从 TPU-like 架构扩散到 AI Ethernet fabric |
| 448G/lane 线性接口、PAM6/PAM8 | OIF CEI-448G framework 阶段 | 研发/测试为主 | B $0.1B-$0.3B / O $0.3B-$0.8B / X $0.8B-$1.5B | B $1B-$4B / O $4B-$10B / X $10B-$20B | 2027 仍偏上游 IP/测试，2028 后进入模块 |

### 5.2 在研产品利润率

| 技术 | 利润率：基准 | 利润率：乐观 | 利润率：极超 | 为什么能定价 |
|---|---:|---:|---:|---|
| 3.2T optical engine/PIC | 35%-50% | 45%-60% | 55%-70% | 400G/lane 器件良率、封装和测试极难，多客户急需样品。 |
| XPO 模块/连接器/液冷件 | 30%-45% | 40%-55% | 50%-65% | 新 form factor、400W 冷却、64 lane、field service 门槛高。 |
| CPO/CPX/NPO optical engine | 40%-55% | 50%-65% | 60%-75% | 可靠性、ELS 冗余、socket/connector/active alignment 绑定系统设计。 |
| ELS/高功率 laser | 45%-60% | 55%-70% | 65%-80% | 高功率、高温稳定、SMSR、耦合效率和寿命认证决定客户是否可部署。 |
| OCI optical scale-up | 50%-65% | 60%-75% | 70%-85% | hyperscaler 与芯片厂共同定义标准，早期 IP/ASIC/SerDes/光引擎议价强。 |
| OCS/MEMS switch | 35%-50% | 45%-60% | 55%-70% | 低功耗替代多级 O-E-O，控制软件和光纤管理复杂。 |
| 448G SerDes/线性 PHY/IP/测试 | 60%-75% | 70%-85% | 80%+ | IP、EDA、测试方法和量产 know-how 稀缺。 |

## 6. 供给侧：产能结构、瓶颈、成本与毛利

### 6.1 产能结构

| 环节 | 主要地区 | 代表公司 | 工艺/能力 |
|---|---|---|---|
| 高速模块设计与品牌 | 中国、美国、日本/中国台湾 | Innolight、Eoptolink、Coherent、Lumentum、NVIDIA、AOI、Accelink、Hisense、CIG、GIGALIGHT、Linktel、ATOP、Infraeo、Genuine Optics、Source Photonics、Formerica | 800G/1.6T OSFP、QSFP-DD、DR/FR/SR/ZR、FRO/LRO/LPO、硅光/EML/VCSEL |
| EMS/代工组装 | 泰国、中国、越南、马来西亚、墨西哥、美国 | Fabrinet、Jabil、Foxconn/FIT、Luxshare、Celestica、Sanmina、Plexus | 光模块组装、自动耦合、burn-in、洁净室和大客户 qual |
| 光芯片/激光器 | 美国、英国、德国、日本、中国、以色列 | Coherent、Lumentum、Broadcom、Semtech、MACOM、Mitsubishi、Sumitomo、OpenLight/Tower、DustPhotonics、POET、NewPhotonics、HyperLight、Lightwave Logic | InP EML/DFB/PD、EAM、CW laser、VCSEL、SiPh PIC、TFLN/EO polymer |
| 线性 TIA/driver/DSP/SerDes | 美国、中国台湾、以色列 | Semtech、Broadcom、Credo、Marvell、MACOM、MaxLinear、TI、Cisco/Acacia、NVIDIA、AMD、Intel | 224G/400G PAM4、3nm/2nm DSP、CEI-224G-Linear、LRO DSP、retimer/AEC |
| 连接器/FAU/光纤管理 | 美国、日本、中国台湾、中国 | TE Connectivity、Amphenol、Molex、Samtec、Senko、Corning、Sumitomo Electric、Fujikura、US Conec、TeraHop、RAM Photonics/TE | high-density FAU、ELSFP、blind-mate connector、MPO/MTP、fiber backplane |
| 测试设备 | 美国、日本、法国、中国 | VIAVI、Keysight、EXFO、Anritsu、Tektronix、MultiLane、Credo PILOT、O-Net/本土测试 | 1.6T MAC/FEC、224G/448G SerDes、BER、FEC margin、光眼图、系统级链路 |

### 6.2 供给瓶颈

1. **200G/400G 光器件良率。** EML/EAM/MZM、InP PD、SiPh modulator 的带宽、线性度、温漂和良率决定 1.6T/3.2T 成本。
2. **线性链路的 host 能力。** LPO 不是“少一个 DSP 就能卖”，它要求 switch/NIC/ASIC 端 SerDes、FEC、NLC、equalization、startup protocol、telemetry 足够强。
3. **高密封装和主动对准。** 1.6T/3.2T 模块中光纤耦合、FAU、lens array、flip-chip EAM/driver、热膨胀控制会显著影响良率。
4. **测试产能和测试时间。** FRO 可更多按模块黑盒测试，LPO/LRO 需要系统级 BER/FEC margin/host-module co-test；测试设备和测试工程师会卡量。
5. **客户认证和固件/CMIS。** hyperscaler 一旦认证某个组合，会锁定至少 2-4 个季度；二线厂商即使有样品，也不等于能进生产网络。
6. **高功率 laser/ELS。** CPO/NPO/CPX 需要外置光源冗余，光功率、温度、寿命和故障更换机制难度高。
7. **液冷与机械可靠性。** XPO、CPO、超高密 OSFP 对 cold plate、密封、插拔寿命、field service 有新增要求。
8. **地缘和出口管制。** 中国模块厂有成本和规模优势，但美系客户、先进 DSP/EDA、部分设备和客户认证受政策扰动。
9. **稀缺人才。** 高速模拟、光电封装、SI/PI、DSP/FEC、测试自动化、数据中心现场调试人才数量远小于订单弹性。

### 6.3 BOM 和单位成本拆分

以下为 1.6T OSFP 模块测算，具体随 DR8/2xDR4、SiPh/EML/VCSEL、FRO/LRO/LPO 差异很大。

| 成本项 | FRO 占比 | LRO/TRO 占比 | LPO 占比 | 说明 |
|---|---:|---:|---:|---|
| DSP/retimer/控制 IC | 25%-35% | 15%-25% | 3%-8% | LRO 保留发送侧能力；LPO 主要转移到 host。 |
| TIA/driver/线性模拟 IC | 8%-12% | 12%-18% | 18%-28% | 线性模块对 analog front-end 要求更高。 |
| 光芯片/PIC/激光器 | 20%-30% | 25%-35% | 28%-40% | SiPh PIC、InP EML/EAM、CW laser 是核心价值。 |
| PCB/OSFP cage/connector/散热 | 10%-15% | 10%-16% | 12%-18% | 线性链路更依赖低损耗连接和热稳定。 |
| 光纤组件/FAU/滤波/隔离器 | 8%-12% | 10%-14% | 10%-16% | 高密度耦合和低插损影响良率。 |
| 组装、测试、burn-in | 15%-25% | 18%-28% | 20%-32% | LPO/LRO 系统级测试复杂，初期占比更高。 |

**毛利决定因素：**

- ASP 取决于速度代际、客户急迫性、是否供不应求、是否需要系统级调参和现场支持。
- 毛利上行来自高端 mix、垂直整合（自有 EML/laser/PIC/DSP）、客户预付、良率爬坡和测试自动化。
- 毛利下行来自多供应商认证、ASP 年降、FRO/LRO/LPO 标准成熟后模块可替代性提高、客户把价值迁移到 host ASIC。

**价格传导机制：**

1. AI rack 供不应求时，客户接受高端 1.6T 溢价，模块厂可把 EML/DSP/测试成本上升向下游传导。
2. 进入多供应商阶段后，模块 ASP 先降，光芯片/DSP/测试瓶颈仍保留溢价。
3. LPO 成熟后，模块 ASP 下降更快，但 host ASIC、SerDes、线性模拟 IC、测试/校准软件获得价值。
4. CPO/NPO 若放量，传统 pluggable 模块池被压缩，但 ELS、optical engine、FAU、连接器和封装价值上升。

## 7. 竞争格局与壁垒

### 7.1 市场结构

| 细分 | 集中度判断 | 主要公司 |
|---|---|---|
| 800G/1.6T AI 光模块 | 头部集中度高，估计前 5 家占 60%-75%；Cignal 称 Innolight 仍为 800GbE leader，Eoptolink、Coherent、NVIDIA 差距缩小。 | Innolight、Eoptolink、Coherent、Lumentum、NVIDIA、AOI、Hisense、Accelink、CIG |
| LPO/LRO 线性模块 | 早期更集中，客户认证决定份额；估计前 5 家占 70%+。 | Eoptolink、Lumentum、Coherent、Innolight、ATOP、Infraeo、Genuine Optics、Adtran |
| LRO DSP/optical DSP | 高集中度，3nm/2nm 和 telemetry 是壁垒。 | Credo、Broadcom、Marvell、Cisco/Acacia、NVIDIA、Semtech |
| 线性 TIA/driver | 中高集中度，模拟性能和量产经验重要。 | Semtech、MACOM、MaxLinear、TI、Broadcom、Lumentum/Coherent 内部 |
| SiPh/InP/laser/PIC | 高壁垒但技术路线多元。 | Coherent、Lumentum、Broadcom、OpenLight/Tower、Semtech、DustPhotonics、POET、HyperLight、Lightwave Logic |
| CPO/NPO/XPO 连接与光纤管理 | 标准初期分散，头部连接器厂优势强。 | TE、Amphenol、Molex、Samtec、Senko、Corning、Sumitomo、US Conec、TeraHop |

### 7.2 可量化壁垒清单

| 壁垒 | 为什么能定价 |
|---|---|
| 224G/400G SerDes 与线性链路预算 | 每降低 1-2W/port，AI cluster 的电力和散热节省可放大到 MW 级；客户愿意为稳定链路付费。 |
| EML/EAM/MZM/PIC 良率 | 同一设计良率差 5-10pct 就足以改变 gross margin；高良率供应商可用交付确定性换溢价。 |
| 客户认证和白名单 | hyperscaler 网络不能频繁换 optics；一旦进 BOM，供应期通常覆盖多个季度甚至代际。 |
| 测试数据和现场 telemetry | LPO/LRO 需要系统级可观测性，能减少 link flap 和集群重训损失的供应商有定价权。 |
| 规模和自动化 | 大客户订单可能是百万只级；没有自动耦合、burn-in、供应链资金和多地工厂，很难接单。 |
| 垂直整合 | Coherent/Lumentum 等拥有激光器、光芯片、模块能力，供应紧张时可优先保障关键部件。 |
| 标准参与权 | LPO MSA、OIF、XPO、OCI、Open CPX 参与者能更早拿到系统规格，提前锁定 design-in。 |
| 切换成本 | 光模块看似可插拔，但 firmware、CMIS、FEC margin、温控、运维脚本、现场备件都形成隐性锁定。 |

### 7.3 价值捕获排序

| 排名 | 价值链层级 | 长期 ROIC/毛利判断 |
|---:|---|---|
| 1 | Host ASIC/SerDes/FEC/交换芯片 | LPO 把价值从模块转向 host，Broadcom/NVIDIA/Marvell/Cisco/AMD 等长期最强。 |
| 2 | 光芯片、激光器、SiPh/InP/TFLN/EO polymer 平台 | 技术壁垒高、认证慢、可跨 FRO/LRO/LPO/CPO 复用。 |
| 3 | LRO DSP、线性 TIA/driver、telemetry 芯片 | 半导体毛利高，且直接决定线性模块是否可靠。 |
| 4 | 头部模块厂 | 2026-2027 有量价弹性，但 2027 后 ASP 竞争加剧。 |
| 5 | 连接器/FAU/ELS/测试设备 | CPO/NPO/XPO 放量后壁垒提高，现金流稳健。 |
| 6 | EMS/组装 | 量大但毛利低，胜在产能周期和客户粘性。 |

## 8. 2026 关键变化：三个拐点

### 8.1 拐点一：1.6T LRO 从演示变成采购选项

Semtech 在 OFC 2026 展示了 224G/lane 102.4T Ethernet switch 通过多厂商 1.6T OSFP transceivers 跑 live traffic，覆盖 FRO、LRO、LPO。Eoptolink、Lumentum、ATOP、Credo 的产品口径都指向同一件事：LRO 是 1.6T 从 FRO 走向线性低功耗的第一站。2026H2 起，客户 RFQ 中 LRO 的权重会明显上升。

### 8.2 拐点二：Google OCS/TPU 架构把光模块 attach rate 拉高

TrendForce 预计 Google 2026 年近 400 万 TPU 对 800G+ 光模块需求超过 600 万只，且 Apollo OCS 用 100W 级光交换替代约 3,000W 级传统交换。这个信号的意义不是 Google 一家，而是“AI cluster 从设计阶段就配置足够光模块”。OCS 架构会增加光模块数量，同时使低功耗 LRO/LPO 更有吸引力。

### 8.3 拐点三：CPO/XPO/OCI 同时出现，pluggable 的远期边界被重写

NVIDIA CPO、Arista XPO、Open CPX MSA、OCI MSA 都在 2026 年密集出现。短期不是谁立刻取代谁，而是客户开始按 scale-up/scale-out/scale-across 分层采购：OSFP/FRO/LRO 解决 2026 上量，LPO 解决受控低功耗链路，XPO 延长可插拔高密度路线，CPO/NPO 解决 2027 以后交换侧功耗极限。

## 9. 2027 关键变化：三个拐点

### 9.1 拐点一：1.6T 从导入期进入价格竞争期，LRO 成为平衡点

2027 年，1.6T 供应商数量会明显增多。FRO 面临 ASP 下行，纯 LPO 仍受互通约束，LRO/TRO 最可能成为客户在功耗、时延、良率、认证和供应安全之间的均衡选择。乐观情景下，LRO 在 1.6T 新项目中的占比可达 35%-50%。

### 9.2 拐点二：3.2T 和 XPO 开始出现早期收入

Broadcom Taurus、Coherent 400G/lane、OpenLight 3.2T DR8 PIC Q4 2026 beta 样品会把 2027 变成 3.2T 客户 qual 年。若 204.8T switch 平台提前，3.2T optical engine、XPO 液冷模块、448G 测试设备会先形成 $1B-$3B 级早期市场。

### 9.3 拐点三：光 scale-up 标准进入 GPU/XPU 系统设计

OCI MSA 由 AMD、Broadcom、Meta、Microsoft、NVIDIA、OpenAI 等推动，核心是为 AI scale-up 定义开放 optical connectivity。2027 年若 Rubin、MI400、MTIA、OpenAI/Broadcom ASIC、Trainium3/4 同步扩张，光互联会从“rack 间网络”进一步进入“rack 内/scale-up 域”。这会把 LPO/LRO 的竞争从模块层提升到 host silicon 和系统架构层。

## 10. 头部公司与细分名单

### 10.1 模块与系统集成

| 公司 | 优势 |
|---|---|
| Innolight 中际旭创 | 800G 龙头，1.6T/硅光/Google 生态强，规模和客户认证优势明显。 |
| Eoptolink 新易盛 | 1.6T LRO/LPO/FRO、XPO 展示积极，AI 客户导入强，LRO 话语权高。 |
| Coherent | 垂直整合强，SiPh/InP/VCSEL/laser/模块/CPO 全栈，2026 Q3 收入 $1.81B，non-GAAP GM 39.6%。 |
| Lumentum | EML、laser、OCS、TRO/1.6T、CPO ELS 核心供应商，2026 Q3 non-GAAP GM 47.9%。 |
| NVIDIA Networking | 自有/生态 optics、CPO switch、Spectrum-X/Quantum-X，能用系统平台定义模块需求。 |
| AOI | 800G 与 1.6T 客户 engagement 强，美国/台湾产能扩张，2026 Q1 数据中心收入 $81.4M。 |
| Accelink 光迅科技 | 中国光模块、光芯片和系统客户基础，LPO MSA 成员。 |
| Hisense Broadband 海信宽带 | 高速 datacom 模块、VCSEL/光器件、海外客户。 |
| CIG 剑桥科技 | 800G/1.6T、LPO/LRO、AEC 等多路线储备。 |
| HG Tech 华工科技 | 中国光模块/激光加工/光电子平台，受益国产 AI 网络。 |
| GIGALIGHT 易飞扬 | 1.6T/3.2T NPO/线性硅光引擎、AI 互联布局积极。 |
| Linktel、ATOP、Infraeo、Genuine Optics | 二线/新兴高弹性供应商，重点在 1.6T LRO/LPO/XPO/AEC。 |
| Adtran | LiteWave800 LPO 超低功耗路线，800G 线性模块差异化。 |
| Source Photonics、Formerica、ColorChip、O-Net、Browave | 区域和细分客户供应商，可能在特定客户 qual 中胜出。 |

### 10.2 DSP、SerDes、TIA/driver、retimer

| 公司 | 优势 |
|---|---|
| Broadcom | Tomahawk/Jericho、Taurus 400G/lane optical DSP、400G EML/PD、CPO、custom XPU 生态。 |
| Credo | Bluebird/Cardinal 1.6T LRO DSP、AEC、PILOT telemetry，LRO 与可靠性叙事强。 |
| Marvell | PAM4/coherent DSP、AEC/retimer、COLORZ 1600、AI scale-across 和 custom silicon。 |
| Semtech | 224G TIA/MZM driver、linear optics era 关键模拟器件，OFC 2026 多厂商 live demo。 |
| MACOM | 线性驱动、TIA、laser/photonic IC、LPO MSA founding member。 |
| MaxLinear、TI、Altera/Intel | 高速模拟、SerDes/FPGA/测试生态，适合线性互通和系统调试。 |
| Cisco/Acacia | Coherent DSP、pluggable ZR、系统客户和网络软件强。 |
| NVIDIA、AMD、Intel | host SerDes/FEC/系统平台决定 LPO/LRO 是否可规模部署。 |

### 10.3 光芯片、SiPh、InP、TFLN、EO polymer

| 公司 | 优势 |
|---|---|
| Coherent | InP、VCSEL、SiPh、laser、CPO optical engine 全栈。 |
| Lumentum | EML、pump laser、narrow linewidth laser、OCS/ELS、TRO 模块。 |
| OpenLight/Tower Semiconductor | III-V integrated SiPh，1.6T LRO/LPO beta，3.2T DR8 PIC alpha/beta。 |
| Broadcom | EML/PD/CPO、switch silicon 绑定，scale-up/out/across 全覆盖。 |
| DustPhotonics/Credo | SiPh 与 optical engine 能力，Credo 收购后可垂直整合。 |
| POET Technologies | 光引擎、ELS、高集成低功耗平台，OFC 2026 关注度高但量产仍需验证。 |
| HyperLight | TFLN 调制器，适合高带宽低电压应用。 |
| Lightwave Logic | EO polymer，高速低功耗调制器潜在期权，商业化需要客户 tapeout/可靠性验证。 |
| Nubis、Ayar Labs、Celestial AI/Marvell、Lightmatter | optical I/O、photonic fabric、near-package/scale-up 光互联长期期权。 |

### 10.4 连接器、FAU、光纤、测试和制造

| 环节 | 公司 |
|---|---|
| 连接器/FAU/背板 | TE Connectivity、Amphenol、Molex、Samtec、Senko、US Conec、Corning、Sumitomo Electric、Fujikura、TeraHop |
| EMS/制造 | Fabrinet、Jabil、Foxconn/FIT、Luxshare、Celestica、Sanmina、Plexus |
| 测试设备 | VIAVI、Keysight、EXFO、Anritsu、Tektronix、MultiLane |
| 光纤/布线 | Corning、AFL、Fujikura、Prysmian、YOFC、亨通、CommScope |
| 交换机/系统 | Arista、NVIDIA、Broadcom、Cisco、Juniper/HPE、Ruijie、H3C、Celestica |

## 11. 极度乐观情景下的市场规模总表

| 收入口径 | 未来 3 个月 | 未来 12 个月 | 未来 24 个月 | 解释 |
|---|---:|---:|---:|---|
| LPO/LRO 线性模块收入 | B $0.8B-$1.8B / O $1.8B-$3.5B / X $3.5B-$6B | B $5B-$10B / O $10B-$18B / X $18B-$30B | B $14B-$28B / O $28B-$50B / X $50B-$80B | 800G LPO + 1.6T LRO/LPO 模块，含少量 3.2T 样品。 |
| 线性光学全价值链 | B $1.8B-$3.5B / O $3.5B-$6B / X $6B-$10B | B $9B-$16B / O $16B-$28B / X $28B-$45B | B $25B-$45B / O $45B-$75B / X $75B-$120B | 模块 + DSP/TIA/driver + 光芯片/PIC + 测试/连接器。 |
| 1.6T 全部模块 | B $1.5B-$3B / O $3B-$5B / X $5B-$8B | B $9B-$15B / O $15B-$25B / X $25B-$40B | B $25B-$45B / O $45B-$75B / X $75B-$120B | FRO/LRO/LPO 全部 1.6T，受 AI fabric 拉动。 |
| CPO/NPO/XPO/OCS 相邻池 | B $0.7B-$1.5B / O $1.5B-$3B / X $3B-$5B | B $4B-$9B / O $9B-$18B / X $18B-$30B | B $15B-$35B / O $35B-$70B / X $70B-$120B | 长期替代和增量架构，2027 后爆发概率提高。 |

**最重要的预期差：线性光模块不是单独看模块价格，而是看“AI rack 中每瓦网络带宽”。** 如果 1.6T LRO 能把单模块功耗从 20W+ 降到 16W 或更低，百万只级部署就是数 MW 到数十 MW 的功耗差；在 AI factory 电力被锁死的情况下，这部分节省可转化为更多 GPU/ASIC 上架容量。

## 12. 风险

1. **LPO 互通低于预期。** 若客户发现 host 端调参和 field failure 成本过高，纯 LPO 可能长期局限在少数封闭系统。
2. **1.6T 价格战提前。** 2026H2 若供应商集中放量，模块 ASP 可能比需求放缓更早下行。
3. **CPO/OCS 改变价值分配。** NVIDIA/Google/Broadcom 若把更多光功能拉进 switch/系统，独立 pluggable 模块厂长期估值会受压。
4. **供应链地缘风险。** 中国模块厂份额、美国本土产能、先进 DSP/EDA 和客户认证都可能受政策扰动。
5. **AI CapEx ROI 波动。** 若 hyperscaler 对推理 ROI 转谨慎，光模块订单可能出现季度拉货/库存波动。
6. **测试与可靠性黑天鹅。** LPO/LRO 初期如果出现 link flap、温漂、FEC margin 不足，会拖延客户量产。

## 13. 跟踪指标

| 指标 | 为什么重要 |
|---|---|
| 1.6T LRO 在 hyperscaler RFQ 中的占比 | 判断 LRO 是否从 demo 变成默认采购项。 |
| 1.6T LPO 客户白名单数量 | 纯 LPO 最大不确定性在客户认证。 |
| 224G linear TIA/driver 交期 | 直接反映线性光学供需紧张度。 |
| EML/EAM/SiPh PIC 良率和产能 | 决定 1.6T/3.2T 成本和毛利。 |
| Coherent/Lumentum/Innolight/Eoptolink 高速 datacom backlog | 判断供不应求是否延续到 2027。 |
| NVIDIA Spectrum-X Photonics、Broadcom CPO、Google OCS 实际部署 | 决定 pluggable 与 CPO/OCS 的价值分配。 |
| XPO MSA 成员和客户 demo | 判断 2027 是否会出现 12.8T 可插拔订单。 |
| 测试设备订单 | 1.6T/3.2T 难度越高，VIAVI/Keysight/MultiLane 越早体现景气。 |

## 14. 资料来源

- [LPO MSA Overview](https://www.lpo-msa.org/home.html)：LPO 定义、成员、低功耗/低时延/低成本目标。
- [LPO MSA formation](https://www.lpo-msa.org/news/twelve-industry-leaders-collaborate-to-define-specifications-for-linea)：Accelink、AMD、Arista、Broadcom、Cisco、Eoptolink、Hisense、Innolight、Intel、MACOM、NVIDIA、Semtech 等 founding members。
- [LPO MSA Specification v1.0 PDF](https://www.lpo-msa.org/files/live/sites/lpomsa/files/specs/LPO_MSA_Specification_v1p0_final.pdf)：100G-DR-LPO、53.125GBd PAM4、500m、host FEC 等规范。
- [OIF CEI-448G Framework](https://www.oiforum.com/wp-content/uploads/OIF-FD-CEI-448G-01.0.pdf)：LPO/RTLR 定义、224G/448G 线性接口挑战。
- [Eoptolink 1.6T LRO OFC 2025](https://www.eoptolink.com/news/360-eoptolink-demonstrates-1-6t-lro-modules-at-ofc-2025)：LRO 定义、接收路径取消 DSP、功耗降低约 30%。
- [Lumentum 1.6T 2xDR4 TRO OSFP](https://www.lumentum.com/en/products/16t-2dr4-tro-osfp-transceiver-module)：1.6T TRO 16W、8x212.5G PAM4、500m。
- [Semtech OFC 2026 live demos](https://www.semtech.com/company/press/showcases-ai-interconnect-leadership-with-live-1.6t-demos-ofc-2026)：多厂商 1.6T FRO/LRO/LPO live traffic。
- [Semtech 224G linear IC family](https://www.semtech.com/company/press/semtech-launches-224-gbps-ic-family-for-linear-optics-era)：CEI-224G-Linear/LPO-MSA compliant TIA/MZM drivers。
- [Credo Cardinal 1.6T optical DSP](https://s205.q4cdn.com/511065572/files/doc_news/Credo-Introduces-Cardinal-A-LowPower-1-6T-Optical-DSP-Family-Engineered-for-MassiveScale-AI-Fabrics-2026.pdf)：3nm 224G/lane LRO DSP、LRO <15W、<40ns latency。
- [Credo OFC 2026 optical demos](https://s205.q4cdn.com/511065572/files/doc_news/Credo-to-Showcase-Optical-Solutions-for-AI-Scale-Out-Fabrics-at-OFC-2026-2026.pdf)：1.6T LRO transceiver with Bluebird DSP。
- [Broadcom OFC 2026 release](https://investors.broadcom.com/node/64036/pdf)：Taurus 400G/lane optical DSP、400G EML/PD、Tomahawk 6、CPO、NPO。
- [Coherent OFC 2026 pluggable release](https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026)：1.6T/3.2T/XPO、SiPh/InP/VCSEL 多技术平台。
- [OpenLight 3.2T DR8 PIC and 1.6T LRO/LPO](https://www.ofcconference.org/news-media/exhibitor-news/openlight-introduces-3-2t-dr8-silicon-photonics-pic-s-as-well-as-1-6t-dr8-lro-and-lpo-variants/)：1.6T DR8 LRO/LPO beta sampling、3.2T Q4 2026 beta。
- [Eoptolink XPO/OFC 2026](https://eoptolink.com/news/13-new-products/364-eoptolink-joins-xpo-msa-and-unveils-industry-first-12-8-tbps-liquid-cooled-pluggable-optics-for-ai-data-centers)：12.8T XPO、1.6T DR4、FRO/LRO/LPO 展示。
- [Arista XPO MSA](https://www.arista.com/en/company/news/press-release/23697-pr-20260311)：12.8T liquid-cooled XPO、204.8Tbps/OCP RU、400W/module、支持 linear/half-retimed/fully-retimed。
- [TE Connectivity OFC 2026](https://www.te.com/en/about-te/news-center/te-ofc-2026.html)：1.6T LRO、3.2T CPO、FAU、CPO-to-optical backplane。
- [NVIDIA Silicon Photonics](https://www.nvidia.com/en-us/networking/products/silicon-photonics/)：CPO 5x power efficiency、10x resiliency、Spectrum-X Photonics 2026H2。
- [NVIDIA Vera Rubin platform](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform)：Spectrum-6 SPX、CPO、Vera Rubin 2026H2 partner availability。
- [Cignal AI optical component revenue 2026](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)：2025 光组件接近 $25B、800GbE >20M、1.6TbE >5M。
- [TrendForce Google OCS / 800G+](https://www.trendforce.com/presscenter/news/20260210-12919.html)：800G+ 占比 2026 超 60%、Google TPU 对 800G+ 模块需求超 600 万只、OCS 100W vs 3,000W。
- [Coherent FY2026 Q3 results](https://www.coherent.com/news/press-releases/third-quarter-fiscal-year-2026-results)：Q3 revenue $1.81B、GAAP GM 37.7%、non-GAAP GM 39.6%。
- [Lumentum FY2026 Q3 results](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx)：Q3 revenue $808.4M、non-GAAP GM 47.9%。
- [AAOI Q1 2026 8-K / press release mirror](https://www.stocktitan.net/sec-filings/AAOI/8-k-applied-optoelectronics-inc-reports-material-event-248b6c9a6862.html)：Q1 revenue、800G volume shipment、1.6T customer engagement。
- [Adtran LiteWave800 LPO](https://www.adtran.com/en/newsroom/press-releases/20260310-adtran-sets-intra-data-center-benchmark-with-all-new-ultra-low-power-litewave800-lpo-module)：800G LPO、1pJ/bit、OSFP、LPO MSA support。
# 行业调研：【OCI（光学计算互连）/ Open CPX / XPO】

> 截至日期：2026-05-08  
> 研究口径：全球 AI 数据中心/AI factory 的网络、光互联与铜互联收入池，重点覆盖 OCI MSA、Open CPX、XPO、CPO/NPO、800G/1.6T/3.2T 光模块、OCS、coherent scale-across、DSP/SerDes、DAC/AEC/ACC 与高密连接。`B` = 十亿美元。  
> 方法：优先采用公司公告、MSA 规格、OFC/GTC 2026 一手资料；行业报告用于交叉验证；对无法直接观察的数据采用“AI 基建极度乐观”假设估算。下文市场规模是订单/收入池估算，不等同于单家公司收入或客户 CapEx，且交换机、光模块、DSP、连接器可能在供应链中存在重复计入口径。

## 0. 一页结论

OCI、Open CPX、XPO 不是三个互斥标准，而是 AI 集群互连在 2026 同时出现的三种“绕开铜瓶颈”的工程答案：

- **OCI MSA**：把光从 scale-out 拉进 scale-up，目标是在 AI rack/row 内用开放光 PHY 承载 NVLink、UALink、Ethernet 等不同协议。2026 以规范和样品为主，2027 进入头部 XPU/GPU/ASIC 的 design-in，2028 才可能成为大规模收入池。
- **Open CPX**：给 CPO/NPO 的 optical engine 做开放 socket/connector/thermal/management 标准，核心是让 CPO 从 proprietary 一次性工程变成可替换、多供应商生态。2026 是 Ciena Vesta 200、Samtec CPX、Coherent/Marvell/Molex/TeraHop 等生态成形年。
- **XPO**：Arista 发起的 12.8T 液冷可插拔路线，每模块 12.8Tbps、每 OCP rack unit 204.8Tbps、单模块 400W 冷却能力。它是可插拔阵营对 CPO 的反击，2026 样品/标准，2027 小批量，2028 才有望成规模。

最确定的投资结论：**2026 真正放量的是 800G + 1.6T 可插拔光模块、高速铜缆/AEC、200G/lane DSP、AI Ethernet/InfiniBand 交换机、EML/VCSEL/SiPh/激光器和测试设备；OCI/Open CPX/XPO 是 2027-2028 的架构期权，但其上游器件会在 2026 先拿订单。**

关键数字锚点：

| 事实 | 投资含义 |
|---|---|
| TrendForce 估算 Top 9 CSP 2026 CapEx 约 **$830B**，同比从 +61% 上修到 **+79%**；2026 全球数据中心装机电力约 **155GW**。 | AI 网络/光互联的 TAM 上限继续上修，且电力瓶颈会强化“每瓦带宽”价值。 |
| OFC 2026 预计 **16,000** 名参会者、**90** 个国家、**700+** 展商；主题集中在 CPO、optical I/O、1.6T/3.2T、PIC、800G/1.6T 验证。 | 光互联已经从通信边角料变成 AI 工厂主赛道。 |
| TrendForce：800G 及以上光模块出货占比从 2024 的 **19.5%** 升到 2026 的 **60%+**；Google Ironwood 2026 近 **400 万** TPU 对应 **600 万+** 只 800G+ 模块需求。 | 800G/1.6T 是 2026 最确定的放量方向；Google OCS/TPU 是重要风向标。 |
| Cignal AI/LightCounting 公开口径：2025 光组件收入接近 **$25B**，datacom 超 **$18B**；LightCounting 估算 AI cluster optics 从 2025 **$16.5B** 增至 2026 **$26B**。 | 即使不算交换芯片和铜互联，AI 光学组件本身也已进入数百亿美元收入池。 |
| Cignal AI 预计 2026 年 **1.6TbE 模块出货 >500 万只**；Broadcom 称未来五年 **1.6T/3.2T transceiver >1 亿只**，近半使用 400G optics。 | 1.6T 不是概念验证，而是 2026-2027 的真实订单斜率；3.2T 是 2027-2028 接力棒。 |
| NVIDIA Spectrum-X Ethernet Photonics 最高 **409.6Tb/s**，H2 2026 可用；官方宣称 CPO 相比 pluggable **5x** 光功耗效率、**10x** resiliency。 | CPO 先从交换机侧放量，短期不替代全部 pluggable，但会重估高端光引擎、ELS、连接和热管理。 |
| Arista XPO：每模块 **12.8Tbps**、64 lanes、**204.8Tbps/OCP RU**、最高 **400W** 冷却，面板密度比 1.6T OSFP 高 **4x**。 | 可插拔不会死，XPO 会把 pluggable 的生命周期延长到 204.8T switch 时代。 |

## 1. 行业机会、挑战与最可能技术路径

### 1.1 三个标准/路线的定位

| 路线 | 解决的问题 | 2026 状态 | 最早放量窗口 | 与其他路线关系 |
|---|---|---|---|---|
| OCI MSA / Optical Compute Interconnect | AI scale-up 从铜线缆转向开放光 PHY，降低功耗、提升带宽密度、避免单一协议锁死 | 2026-03 发布 v1.0 200G line interface；创始成员 AMD、Broadcom、Meta、Microsoft、NVIDIA、OpenAI | 基准 2028；乐观 2027H2 小批量；极度乐观 2027 即被 OpenAI/Meta/Microsoft XPU 采用 | 可承载 NVLink/UALink/Ethernet 等上层协议；可落在 OBO、package integration、interposer integration |
| Open CPX | CPO/NPO optical engine 的机械、电气、热、管理接口开放化 | 2026-03 成立，Ciena、Coherent、Marvell、Molex、Samtec、TeraHop 为核心 | 2027 头部 switch/XPU 小批量；2028 扩散 | 是 CPO/NPO 的 socket/engine 层，帮助减少 vendor lock-in |
| XPO | 12.8T 液冷可插拔，用更大模块和液冷延长 pluggable | 2026-03 Arista 发起 MSA，Eoptolink/Linktel 等展示样品，Marvell 加入 | 2027H2 小批量；2028 204.8T switch 规模导入 | 与 CPO 竞争，也为不愿牺牲可维护性的客户提供过渡路径 |
| CPO/NPO/ELS | 把光引擎贴近 switch ASIC/XPU，减少电走线损耗和 DSP/retimer 功耗 | NVIDIA/Broadcom/Ciena/Lumentum/Coherent/GF 2026 全面推进 | 2026H2 NVIDIA switch；2027 多客户 pilot | Open CPX、OCI、ELSFP、OIF 是生态化关键 |
| 800G/1.6T pluggable | AI scale-out 主流互连，标准成熟、供应链可扩张 | 800G 主流；1.6T 从样品进入量产窗口 | 2026 全年 | 2026 最赚钱的现金流层，2027 与 CPO/XPO 并存 |
| 铜互联 DAC/AEC/ACC | rack 内和短距 lowest cost/lowest latency | 2026 仍是 rack 内主力 | 已放量 | 铜不会消失，但距离和功耗边界推动光进 rack |

### 1.2 2026 AI 计算中心建设的机遇

1. **AI CapEx 继续上修，网络占比上行。** 本项目《AI数据中心建设规模与产业链订单映射》给出的务实口径中，2026 全球/美国 AI 网络与光互联收入池已是数百亿美元级，2027 在 1.6T、CPO、OCS、scale-across 的拉动下继续提高。网络不再只是服务器附属项，而是决定 GPU/XPU 利用率的基础设施。
2. **scale-up 从专有铜域走向开放光域。** GB300/Rubin、MI400/Helios、TPU、Trainium、MTIA、OpenAI/Broadcom XPU 都把集群从服务器节点推到 rack/POD。铜在 200G/lane、224G/448G SerDes、高密液冷环境下功耗和可布线性受限，OCI 正是对这个趋势的标准化反应。
3. **1.6T 进入真实订单期。** 2024-2025 是 800G 主线，2026 开始 1.6T OSFP/DR4/2xDR4、LRO/LPO/TRO、400G/lane prototype 集中出现。1.6T 的 ASP 即使下行，总收入仍会被出货量放大。
4. **CPO 不再只是 NVIDIA/Broadcom proprietary 叙事。** Open CPX、GF SCALE、Ciena Vesta 200、Lumentum SHP/UHP laser、Coherent socketed CPO 等都在补 CPO 量产最薄弱的“多供、可维护、可测试、可替换”环节。
5. **AI scale-across 带来第二条光学主线。** 大型 AI region 不只是机房内短距，campus/metro/regional DCI 需要 800ZR、1600ZR、coherent-lite、multi-rail line system、hyper-rail、FST，Ciena/Nokia/Marvell/Cisco/Acacia 价值提高。
6. **铜互联也受益，而不是被光完全吃掉。** 2026 rack 内仍以 NVLink copper、DAC/AEC、linear redriver、active copper cable 为主；越多 GPU/XPU 放进机架，越需要高端连接器、线缆、retimer/redriver 和 SI 测试。

### 1.3 主要挑战

| 挑战 | 具体表现 | 投资含义 |
|---|---|---|
| 标准并行与客户分裂 | OCI、Open CPX、XPO、OIF、OCP、UALink、NVLink、ESUN 同时推进 | 避免押单一 form factor；更看好跨标准器件、测试、连接、ELS、SiPh foundry |
| CPO 可维护性 | 光引擎坏了怎么换、ELS 如何冗余、现场维修是否影响 switch ASIC | Socketed/CPX、external laser、flight recorder、CMIS 管理成为定价点 |
| 光电测试产能 | 1.6T/3.2T、224G/448G SerDes、400G/lane EML/PIC 都显著增加测试时间 | Keysight、VIAVI、Anritsu、MultiLane、FormFactor 等高景气 |
| 热管理 | XPO 单模块 400W；CPO switch 液冷；1.6T/3.2T 模块热密度上升 | 光模块热设计、液冷 cold plate、微型连接和热仿真形成新壁垒 |
| 供应链地域风险 | 中国模块厂规模强，美国厂商高价值组件强，客户要求 out-of-China 和多区域制造 | Fabrinet、台湾/东南亚 EMS、美国本土光器件/SiPh 产能溢价 |
| ASP 下行 | LightCounting 提醒 2026 中后期产能追上后可能出现价格竞争 | 模块组装利润承压，上游瓶颈器件和平台级芯片更稳 |
| 铜/光边界不清 | rack 内短距铜仍便宜，光进 scale-up 的节奏取决于 200G/400G lane 功耗 | 2026 最确定仍是铜+800G/1.6T scale-out，OCI 不宜按立即大规模出货定价 |

### 1.4 当前正在被使用的技术

| 技术层 | 2026 主流技术 | 代表公司/生态 | 状态 |
|---|---|---|---|
| AI scale-up | NVLink/NVSwitch、Google ICI、AWS NeuronLink、AMD Infinity Fabric、UALink design-in | NVIDIA、Google、AWS、AMD、Broadcom、Meta、Microsoft | 铜/电为主，光 scale-up 早期 |
| AI scale-out | 800G Ethernet/InfiniBand，1.6T 导入，fat-tree/dragonfly/3D torus | NVIDIA、Broadcom、Arista、Cisco、Marvell、Google | 800G 主流，1.6T 2026 开始放量 |
| 光模块 | 800G DR8/2xFR4、1.6T DR4/2xDR4/DR8、LRO/LPO/TRO | Innolight、Eoptolink、Coherent、Lumentum、AOI、Fabrinet、NVIDIA 生态 | 已放量/导入 |
| 高速铜 | DAC、AEC、ACC、linear redriver、retimer cable | Credo、Astera、Broadcom、Marvell、Amphenol、TE、Molex、Luxshare、BizLink | rack 内核心 |
| CPO/NPO | Switch CPO、socketed CPO、ELSFP、CPX connector、silicon photonics engine | NVIDIA、Broadcom、Ciena、Coherent、Lumentum、Marvell、Samtec、GF、TSMC | 早期商业化 |
| OCS | MEMS mirror fiber-to-fiber optical circuit switching | Google Apollo、Lumentum、Calient、Polatis/HUBER+SUHNER | Google 先行，外部扩散早期 |
| Coherent scale-across | 800ZR/ZR+、1600ZR/ZR+、coherent-lite、multi-rail ILA/FST | Marvell、Ciena、Nokia/Infinera、Cisco/Acacia、Coherent | 2026-2027 高增长 |
| Optical I/O chiplet | XPU/ASIC 旁 photonic I/O，remote laser，WDM | Ayar Labs、Lightmatter、Celestial AI、OpenLight、HyperLight、POET、Nubis | 研发/早期客户导入 |

### 1.5 结合 2026-2027 出货量最大的 AI 芯片路线

项目内芯片研究显示，2026-2027 出货和价值量最大的路线包括 NVIDIA B300/GB300、B200/GB200、Vera Rubin、AWS Trainium2/3、Google TPU v7 Ironwood/TPU8、AMD MI350/MI400 Helios、Meta MTIA、Microsoft Maia 200、OpenAI/Broadcom custom accelerator、Huawei Ascend、Cambricon、Alibaba T-Head 等。对 OCI/Open CPX/XPO 的含义如下：

| AI 芯片/平台 | 2026-2027 互连背景 | 对 OCI/Open CPX/XPO 的拉动 |
|---|---|---|
| NVIDIA B300/GB300 | rack 内 NVLink/copper，scale-out 800G/1.6T；GB300 是 2026 主力 | 2026 主要拉动 800G/1.6T、DAC/AEC、交换机；OCI 不是主力，CPO 在 Spectrum-6/SPX 前置 |
| NVIDIA Vera Rubin | 2026H2 partner availability；Spectrum-6 SPX、CPO、NVLink 6、ConnectX-9 | CPO/Open CPX 价值上升；2027 可能成为 CPO scale-out 和 optical scale-up 的最大锚 |
| AMD MI350/MI400 Helios | MI350 2026 放量；MI400/Helios 2026H2 起步，开放 rack/UALink/Ethernet | UALink + OCI 的潜在受益大；2027 若 Helios 放量，开放光 scale-up 有机会 |
| Google TPU Ironwood/TPU8 | Ironwood 短距铜，rack 间 Apollo OCS/all-optical；2026 TPU 需求极大 | OCS、800G/1.6T、SiPh、Lumentum MEMS/laser、Innolight/Eoptolink 直接受益 |
| AWS Trainium2/3 | NeuronLink scale-up，EFA/Ethernet scale-out；Trainium3 UltraServer 144 芯片 | 2026 更偏 800G/Ethernet；Trainium4 若接 NVLink Fusion/开放互连，OCI 机会后移 |
| Meta MTIA 300/400/450/500 | Broadcom XPU/网络生态，Meta 强推开放 rack 和大规模推理 | OCI/Open CPX/CPO 是最可能采用者之一；Meta 是 OCI 规格编辑核心来源之一 |
| OpenAI/Broadcom XPU | 10GW，2026H2 开始部署，Broadcom 网络/IP 深度绑定 | OCI、CPO、Open CPX 和 1.6T/3.2T 都有超预期弹性 |
| Microsoft Maia 200 | Azure 自研推理芯片，高密闭环液冷，后端网络规模大 | Microsoft 是 OCI/XPO 支持方，2027 可能推动开放 scale-up 光互连 |
| Huawei/Cambricon/Alibaba | 中国本土集群以电互连 + 国产/国内光模块为主 | OCI/Open CPX 受出口/生态限制；800G/1.6T 国产光模块、AEC、交换机更确定 |

### 1.6 成熟/放量时间：基准、乐观、极度乐观

| 技术 | 基准 | 乐观 | 极度超预期乐观 | 2026 最可能路径 |
|---|---|---|---|---|
| 800G pluggable | 2026 主流，2027 仍大量出货 | 2026 出货继续超预期，ASP 缓降 | 2026 高端模块仍供不应求 | 最高确定性 |
| 1.6T pluggable | 2026 >500 万只，2027 1,200-1,800 万只 | 2027 2,000-2,500 万只 | 2027 3,000 万只级，成为新增 AI fabric 默认 | 2026H2 最重要增量 |
| 224G/200G lane DSP/SerDes/AEC | 2026 主流，2027 与 400G lane 接续 | 200G lane 供给紧张持续到 2027H1 | Broadcom/Marvell/Credo/Astera 均锁产能到 2027 | 最高确定性 |
| CPO/NPO/ELS | 2026 NVIDIA/Broadcom pilot，2027 小批量 | 2027 多个 AI cluster 部署 | 2027 高端 switch 默认之一 | 2026 先赚 ELS、光引擎、测试、连接 |
| Open CPX | 2026 标准和样品，2027 小批量 | 2027 成为 CPO optical engine 主接口之一 | 2027H2 进入多个 100T/200T switch/XPU | 2026 设计导入 |
| OCI optical scale-up | 2026 规范，2027 design-in，2028 放量 | 2027H2 头部 XPU 小批量 | 2027 就在 OpenAI/Meta/Microsoft 高端 rack 中形成收入 | 2026 不是规模收入 |
| XPO 12.8T | 2026 样品/MSA，2027H2 小批量，2028 放量 | 2027 在 204.8T switch 先导入 | 2027 形成 $2B+ 需求 | 2026 观察 MSA 生态 |
| 3.2T/400G lane | 2026 器件样品，2027 live demo/qual，2028 规模化 | 2027H2 小批量收入 | 2027 形成 $3B+ 早期市场 | 2026 赚上游器件和测试 |
| OCS | Google 先行，2026-2027 扩散有限 | 2027 Meta/Microsoft/Anthropic 跟进 | GPU Ethernet fabric 也吸收 OCS | 2026 Google 生态最确定 |
| 1600ZR/coherent-lite | 2026H2 采样，2027 放量 | AI scale-across 超预期 | 1600ZR/CL 进入数据中心内部长距 | 2026 订单前置 |

## 2. 已开始放量的关键产品：市场规模、渗透率、利润率

### 2.1 已放量产品三情景

| 产品/细分技术 | 当前放量证据 | 未来3个月市场规模 | 未来12个月市场规模 | 未来24个月市场规模 | 渗透率路径 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| 800G pluggable 光模块 | TrendForce 称 800G+ 2026 出货占比 >60%；GB300/TPU/Trainium 都需要 | $6-10B / $8-14B / $12-18B | $25-40B / $35-55B / $50-75B | $35-55B / $50-80B / $75-110B | AI 高速端口 2026 55-70%，2027 因 1.6T 接棒降至 40-55% | 25-38% / 32-45% / 40-50% |
| 1.6T OSFP/DR4/2xDR4/LPO/LRO/TRO | Cignal 预计 2026 >500 万只；Lumentum/Coherent/Eoptolink/OpenLight 展示 | $1.5-3B / $2.5-5B / $4-8B | $8-14B / $14-25B / $25-40B | $22-45B / $45-80B / $80-130B | 新增高端 AI fabric 2026 5-12%，2027 18-35%，极度乐观 50% | 35-45% / 40-50% / 45-55% |
| 200G/lane PAM4 DSP、retimer、LRO/LPO host silicon | Broadcom、Marvell、Credo、Astera 争夺 1.6T/800G 生态 | $2-4B / $3-6B / $5-8B | $10-18B / $16-28B / $25-45B | $18-35B / $32-60B / $55-100B | 1.6T fully retimed/LRO/LPO 均需要 host/silicon 协同，2026 attach 高 | 55-70% / 60-75% / 65-80% |
| EML/VCSEL/PD/InP CW laser/SiPh PIC | Lumentum 400G EML、SHP/UHP laser；Coherent 1.6T/3.2T 多平台 | $3-6B / $5-9B / $8-13B | $16-28B / $25-40B / $38-60B | $28-55B / $45-85B / $75-130B | 800G/1.6T 模块核心瓶颈，SiPh 在 1.6T/3.2T/CPO 渗透持续提高 | 35-55% / 42-60% / 50-65% |
| AI Ethernet/InfiniBand 交换机、NIC/DPU、SuperNIC | Broadcom Tomahawk 6 production volume；NVIDIA Spectrum-X/Quantum-X、CX9 | $8-14B / $12-20B / $18-30B | $40-70B / $60-100B / $90-150B | $80-150B / $130-240B / $220-380B | AI 后端网络端口 2026 高速化，2027 102.4T/204.8T switch 接棒 | 芯片 55-70%；系统 35-55%；极度短缺可更高 |
| DAC/AEC/ACC、高速连接器、linear redriver | rack 内铜仍是最低成本；Ciena Nitro 2004 等 redriver 明确服务 AI scale-up | $3-6B / $5-8B / $7-12B | $14-25B / $22-38B / $35-60B | $25-50B / $45-85B / $80-140B | rack 内 attach 90-100%；2027 更高端、更短距、更厚线缆 | 25-40% / 30-45% / 35-55% |
| Coherent 800ZR/1600ZR/ZR+ scale-across | Marvell COLORZ 1600 2026H2 采样；Ciena/Nokia 推 1600ZR/CL | $1.5-3B / $2-4B / $3-6B | $8-14B / $12-20B / $18-32B | $18-35B / $30-55B / $50-90B | AI campus/metro/regional DCI 从 wavelength 转向 fiber pair/band 级部署 | 40-55% / 45-60% / 50-65% |
| OCS/MEMS 光交换、fiber management | Google Apollo OCS：单机约 100W vs 传统交换约 3,000W；Lumentum 供应关键器件 | $0.2-0.8B / $0.5-1.5B / $1-3B | $2-6B / $5-12B / $10-25B | $10-30B / $25-70B / $60-150B | 2026 Google TPU-like 集群为主，2027 向其他 ASIC/GPU fabric 扩散 | 35-50% / 40-55% / 50-65% |
| 光电测试、BERT、FEC/MAC、224G/448G SerDes 验证 | OFC 2026 800G/1.6T validation 和 3.2T 测试平台成显性主题 | $0.8-1.5B / $1.2-2.5B / $2-4B | $4-8B / $7-12B / $10-18B | $8-16B / $14-25B / $22-40B | 1.6T 2026 高景气，3.2T/400G lane 2027 接棒 | 55-70% / 60-75% / 65-80% |

### 2.2 增长预测区间与利润率判断

- **基准情景**：2026 年 1.6T 开始供货但仍以 800G 为主；2026H2 起部分产能追上，800G ASP 下行。模块厂毛利正常化，DSP/SerDes/高端激光器和测试设备保持高毛利。
- **乐观情景**：GB300、Rubin、Trainium、TPU、Meta/OpenAI ASIC 同时抢网络产能，800G 与 1.6T 不是替代关系而是叠加关系；光模块和高端铜缆均短缺。
- **极度乐观情景**：2027 需求提前到 2026H2 下单，1.6T、200G/lane DSP、EML、SiPh PIC、CPO ELS、AEC 全部被 hyperscaler 锁定，供应商获得预付款和价格保护。

利润率排序：**DSP/SerDes/IP > 测试设备 > 高功率激光/ELS/SiPh PIC > 交换芯片/NIC > CPO optical engine > 高端连接器/AEC > 光模块品牌商 > EMS/组装。** 2026 最容易被误判的是光模块：收入增速很高，但若 2026H2 供应追上，普通 800G 模块毛利率会先被 ASP 压缩。

## 3. 在研关键产品与未来快速增长方向

| 在研/早期技术 | 当前阶段 | 未来3个月市场规模 | 未来12个月市场规模 | 未来24个月市场规模 | 渗透率路径 | 毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| OCI optical scale-up PHY | 2026-03 v1.0；NRZ+WDM；500m SMF link model；OBO/package/interposer 三形态 | <$0.1B / $0.1-0.3B / $0.3-0.8B | $0.5-2B / $2-6B / $6-18B | $8-25B / $25-70B / $70-180B | 2026 <1%；2027 2-8%；极度乐观 2027 高端 XPU scale-up 10%+ | 45-65% / 50-70% / 60-80% |
| Open CPX / socketed CPO optical engine | Ciena Vesta 200 6.4T CPX；Open CPX MSA 覆盖机械/电气/热/管理 | $0.2-0.6B / $0.5-1.5B / $1-3B | $2-8B / $6-20B / $18-50B | $15-45B / $45-120B / $120-300B | 高端 100T/200T switch 2027 3-10%，乐观 10-25% | 40-60% / 45-65% / 55-75% |
| XPO 12.8T 液冷可插拔 | Arista MSA；Eoptolink/Linktel 样品；Marvell 加入 | <$0.1B / $0.1-0.4B / $0.3-1B | $0.3-1.5B / $1-5B / $5-15B | $4-15B / $15-50B / $50-150B | 204.8T switch 2027 <5%，乐观 5-15%，极度乐观 20-35% | 35-55% / 40-60% / 50-70% |
| 3.2T / 400G-per-lane 模块与光引擎 | Broadcom Taurus；Lumentum 400G EML；OpenLight 3.2T beta 预计 2026Q4 | $0.1-0.5B / $0.3-1B / $0.8-2.5B | $1-4B / $3-10B / $10-30B | $12-35B / $35-85B / $85-180B | 2026 样品，2027 qual，小批量，2028 规模化 | 器件/DSP 50-75%；模块早期 30-50% |
| CPO/NPO/ELS for switch/XPU | NVIDIA Spectrum-X H2 2026；Broadcom Tomahawk 6-Davisson CPO；GF SCALE | $0.5-1.5B / $1-3B / $3-8B | $5-15B / $12-35B / $35-90B | $30-90B / $80-220B / $220-500B | 2026 switch pilot，2027 高端 switch 5-20% | ELS 45-65%；engine 40-60%；系统取决于服务成本 |
| PCIe Gen6/7 over optics、CXL/optical I/O | OFC/PCI-SIG 讨论升温；Broadcom 展示 PCIe Gen6 over optics | <$0.1B / $0.2-0.5B / $0.5-1B | $0.5-2B / $2-8B / $8-25B | $8-25B / $25-80B / $80-200B | 2026 PoC，2027 storage/CXL/accelerator fabric 小批量 | 45-70% / 55-75% / 65-80% |
| Photonic I/O chiplet / wafer-scale optical fabric | Ayar Labs、Lightmatter Passage、Celestial Photonic Fabric、Nubis 等 | $0.2-1B / $0.5-2B / $1-5B | $3-10B / $8-25B / $25-70B | $25-80B / $70-200B / $200-500B | 2026 客户验证，2027 ASIC/XPU 设计导入，2028 量产 | 50-75%，但早期 NRE/良率波动大 |
| TFLN / advanced modulator | HyperLight、Lightwave Logic、薄膜铌酸锂与硅光混合集成 | $0.1-0.4B / $0.2-0.8B / $0.5-2B | $1-4B / $3-10B / $8-25B | $8-25B / $25-75B / $75-180B | 400G/lane 与低功耗 1.6T/3.2T 受益 | 45-70%，量产良率决定真实利润 |
| Hollow-core fiber / multi-rail line system | Nokia 提到 HCF loss 0.04dB/km；Ciena/Nokia hyper-rail/FST | <$0.1B / $0.2-0.6B / $0.5-1.5B | $0.5-2B / $2-8B / $6-18B | $6-20B / $20-60B / $60-150B | 2026 特定 DCI/HPC，2027 低延迟 AI region 试点 | 35-55%，系统集成和运维更高 |

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 层级 | 主要地区 | 代表公司 | 关键工艺/能力 |
|---|---|---|---|
| 光模块组装与高量制造 | 中国、泰国、马来西亚、越南、台湾、墨西哥 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、AOI、Fabrinet、Foxconn、Luxshare、Linktel、HG Genuine、Accelink | OSFP/QSFP-DD 封装、耦合、burn-in、CMIS、自动化测试 |
| 光芯片/激光器 | 美国、日本、中国、台湾、韩国 | Lumentum、Coherent、Broadcom、Mitsubishi Electric、Sumitomo Electric、Sony/Hamamatsu、Source Photonics、Hisense Broadband | InP EML/EAM/PD、GaAs VCSEL、CW laser、UHP/SHP ELS |
| 硅光/光引擎 foundry | 美国、台湾、新加坡、以色列、欧洲 | GlobalFoundries、TSMC COUPE、Intel Silicon Photonics、Tower、Samsung Foundry、UMC、OpenLight、Ayar Labs、Lightmatter、Celestial AI、POET、HyperLight | SiPh PIC、III-V on Si、TFLN、co-packaging、wafer-level test |
| DSP/SerDes/retimer | 美国、以色列、加拿大、台湾 | Broadcom、Marvell、Credo、Astera Labs、MaxLinear、MACOM、Alphawave Semi、Rambus、Synopsys/Cadence IP | 3nm/2nm DSP、224G/448G SerDes、FEC、LPO/LRO、AEC retimer |
| 交换芯片/NIC/DPU | 美国、台湾 | Broadcom、NVIDIA、Marvell、Cisco/Acacia、AMD/Pensando、Intel、Arista | 102.4T/204.8T switch、800G NIC、AI fabric telemetry |
| CPO/CPX/XPO 连接与光纤管理 | 美国、日本、欧洲、台湾、中国 | Samtec、Molex、Amphenol、TE Connectivity、Senko、US Conec、Corning、Sumitomo、TeraHop、MPO/MTP 生态 | 高密连接器、MT ferrule、fiber shuffle、surface-normal I/O、liquid-cooled cage |
| 测试与可靠性 | 美国、日本、德国、中国 | Keysight、VIAVI、Anritsu、Tektronix、EXFO、Spirent、MultiLane、FormFactor、Advantest、Teradyne | 224G/448G BERT、FEC/MAC、光谱、热循环、良率筛选 |

### 4.2 供给瓶颈

| 瓶颈 | 具体内容 | 影响 |
|---|---|---|
| 200G/400G EML/EAM/MZM 良率 | 400G/lane 对带宽、线性度、TDEC、温漂要求高 | 决定 1.6T 低功耗和 3.2T 节奏 |
| 高功率 ELS/UHP laser | CPO/OCI 需要外部激光、低 RIN、窄线宽、冗余 | ELS 可能成为 CPO 从 pilot 到量产的关键瓶颈 |
| 3nm/2nm DSP 产能 | Taurus、Electra/Libra 等需要先进节点和封装 | DSP 供给会决定 1.6T/1600ZR 的出货上限 |
| SiPh PIC 与 co-packaging | 光电混合集成、fiber attach、已知良品光引擎筛选 | 决定 CPO/CPX/OCI 可维护性和良率 |
| 高密连接器与 fiber management | XPO/CPX/CPO 需要高密光纤、surface-normal I/O、MT ferrule | 小部件失效会拖累整柜可靠性 |
| 液冷与热设计 | XPO 400W/module，CPO switch 液冷，1.6T/3.2T 模块热密度高 | 热设计决定可插拔是否继续扩展 |
| 测试时间 | 1.6T/3.2T、OCI bidirectional WDM、CMIS/flight recorder 都需更长测试 | 测试设备和工位成为隐形产能瓶颈 |
| 客户认证 | Hyperscaler 光模块认证 6-18 个月，CPO/OCI 更长 | 错过平台窗口就错过一代需求 |
| 人才 | 光电封装、SI/PI、热仿真、可靠性和现场运维工程师紧缺 | 制约新进入者扩产 |

### 4.3 成本构成与价格传导

| 产品 | 典型成本构成 | 毛利决定因素 | 价格传导 |
|---|---|---|---|
| 1.6T fully-retimed OSFP | DSP/retimer 20-30%；EML/SiPh/PIC/PD/laser 25-35%；PCB/connector/cage 8-12%；passive optics 10-15%；thermal/mechanical 8-12%；assembly/test/yield 12-20% | DSP 与 EML/SiPh 供给、测试良率、客户认证 | 早期可把短缺溢价传给云厂；2026H2 后普通模块 ASP 压力上升 |
| 1.6T LPO/LRO/TRO | 光器件占比更高，module DSP 降低或转移到 host；host silicon/ASIC 复杂度上升 | 是否能在客户 switch 上闭合链路预算和可靠性 | 客户愿为低功耗付费，但 host 适配失败会压低普及速度 |
| CPO/CPX optical engine | PIC 20-30%；driver/TIA 15-25%；ELS 15-25%；package/connector/fiber attach 15-25%；test 10-20%；thermal/reliability 5-10% | ELS 冗余、可替换性、良率、field failure 成本 | 若节省 switch 功耗和面板密度，客户可接受高 ASP |
| XPO 12.8T | 多个 optical engine 35-45%；DSP/retimer 20-30%；liquid cold plate/mechanical 10-15%；fiber connector 10-15%；test 10-20% | 400W 热管理、可插拔寿命、维修流程 | 早期高溢价，标准成熟后竞争加剧 |
| AEC/DAC/ACC | 铜缆/连接器 25-40%；retimer/redriver 30-45%；thermal/mechanical 5-10%；assembly/test 10-20% | 信号完整性、长度、功耗、客户平台认证 | 比光便宜，客户对低成本敏感；高端 AEC 仍有溢价 |
| 1600ZR/coherent pluggable | coherent DSP 25-35%；laser/modulator/receiver 25-35%；OSFP thermal/mechanical 10-15%；test/calibration 15-25% | DSP 功耗、MACsec、interop、生产测试 | AI DCI 缺纤/缺电时，功耗和密度节省可强传导 |

## 5. 竞争格局与壁垒

### 5.1 市场结构与集中度

| 环节 | 竞争格局 | 集中度判断 | 定价权 |
|---|---|---|---|
| AI switch ASIC / NIC | Broadcom、NVIDIA 双强，Marvell/Cisco/AMD/Intel 分领域竞争 | Top 2 高集中 | 极强 |
| PAM4 DSP/SerDes/retimer | Broadcom、Marvell、Credo、Astera、MaxLinear、MACOM | Top 3 约 70%+ | 强 |
| 800G/1.6T 模块 | Innolight/Eoptolink/Coherent/Lumentum/AOI/Fabrinet/中国厂商 | Top 5 约 55-70%，客户结构差异大 | 中高，ASP 会下行 |
| 高功率激光/EML/PD | Lumentum、Coherent、Broadcom、日本厂商与中国追赶者 | 高端件集中 | 强 |
| CPO/CPX/OCI 光引擎 | NVIDIA/Broadcom/Ciena/Coherent/Marvell/Lumentum/GF/TSMC/Ayar/Lightmatter/Celestial | 早期高度集中 | 很强，但需生态开放 |
| XPO | Arista 牵头，Marvell/Eoptolink/Lightmatter/TeraHop/Linktel 等 | 早期生态未定 | 早期强，量产后看 MSA 竞争 |
| Coherent DCI | Ciena、Nokia/Infinera、Cisco/Acacia、Marvell、Coherent | 技术与客户集中 | 强 |
| 连接器/光纤管理 | Amphenol、TE、Molex、Samtec、Senko、US Conec、Corning、Sumitomo | 高端集中 | 中高 |
| 测试设备 | Keysight、VIAVI、Anritsu、Tektronix、EXFO、MultiLane | 高端集中 | 强 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 为什么能定价 |
|---|---|---|
| 标准编辑权 | OCI v1.0 由 Meta/Broadcom/AMD 等编辑；Open CPX/XPO 创始成员定义接口 | 标准早期接口会进入客户 RFP 和 reference design |
| 客户认证 | 光模块、AEC、CPO engine 需在 hyperscaler switch/GPU/ASIC 上长期验证 | 一旦通过认证，替换成本高，错过窗口难补单 |
| 性能每瓦 | CPO、LPO、OCI 的核心价值是降低 pJ/bit 和网络功耗 | AI 工厂受电力限制，节能直接转化为更多 GPU/XPU |
| 良率与测试 | 1.6T/3.2T 需要大量光电测试和已知良品筛选 | 产能和测试工位短缺时，良率高者可拿溢价 |
| 光电封装 know-how | CPO/CPX/OCI 需要 co-design：ASIC、PIC、ELS、fiber、thermal | 单纯模块组装厂难复制 |
| 供应链锁定 | 大客户会预订 EML、DSP、laser、SiPh foundry、EMS 产能 | 供不应求产品可以获得预付款和价格保护 |
| 可维护性/可靠性数据 | CPO/XPO 若现场故障影响整个 switch/rack，客户会重视历史数据 | 低故障率比低 ASP 更重要 |
| 多区域制造 | 美国、台湾、东南亚、墨西哥和中国供应链切换能力 | 地缘风险下，out-of-China 产能可拿溢价 |

### 5.3 价值捕获：哪一层长期高 ROIC

长期高 ROIC 排序：

1. **交换芯片、DSP/SerDes、DPU/NIC、协议/IP**：Broadcom、NVIDIA、Marvell、Credo、Astera。原因是设计周期长、客户绑定强、毛利高。
2. **高功率激光器、EML/PD、SiPh PIC、CPO/OCI 光引擎**：Lumentum、Coherent、Broadcom、GF、TSMC、Ciena、Ayar Labs、Lightmatter。原因是瓶颈细、扩产慢、测试难。
3. **测试设备和高端连接器**：Keysight、VIAVI、Anritsu、Amphenol、TE、Molex、Samtec、Senko、Corning。原因是所有路线都要用，且不直接暴露于模块 ASP 战。
4. **coherent DCI 和 line system**：Ciena、Nokia/Infinera、Cisco/Acacia、Marvell。原因是 AI scale-across 比市场预期更大，系统软件和客户网络规划壁垒高。
5. **高端光模块品牌商**：Innolight、Eoptolink、Coherent、Lumentum、AOI。原因是收入弹性大，但 2027 后 ASP 和竞争会压缩普通模块利润。
6. **EMS/组装**：Fabrinet、Foxconn、Jabil、Celestica、Flex。原因是量大但毛利较低，除非绑定高端测试、液冷、系统集成。

## 6. 2026 关键变化：行业拐点与最可能放量方向

### 6.1 拐点一：1.6T 从“样品”变成“采购清单”

2026 最确定放量方向是 800G 继续高位 + 1.6T 快速导入。Cignal 的 >500 万只 1.6T 预测、TrendForce 的 800G+ >60% 出货占比、Lumentum/Coherent/Broadcom/Eoptolink/OpenLight 在 OFC 的密集展示，说明 1.6T 已进入客户 qual 和供应链锁单阶段。

最受益：1.6T OSFP 模块、200G/lane DSP、400G EML prototype、SiPh PIC、EML/PD、测试设备、热管理。

### 6.2 拐点二：CPO/CPX/OCI 标准化启动，光进入 scale-up 设计周期

OCI MSA 和 Open CPX 在 2026 同时出现，本质上是 hyperscaler 和芯片厂承认：未来 AI rack/row 的规模无法只靠铜和 proprietary 电互连。2026 不会大规模收入确认，但会决定 2027-2028 的 design-in 名单。

最受益：CPO optical engine、ELS、CPX connector、SiPh foundry、Broadcom/NVIDIA/Marvell/Ciena/GF/TSMC、Ayar/Lightmatter/Celestial 等 optical I/O 生态。

### 6.3 拐点三：Google OCS 和 NVIDIA Spectrum-X Photonics 把光互联从模块采购推向架构决策

Google Apollo OCS 用约 100W MEMS OCS 替代传统 3,000W 级电交换路径；NVIDIA Spectrum-X Ethernet Photonics 用 CPO 追求 5x power efficiency 和 10x resiliency。这意味着 AI 网络采购指标从“每端口多少钱”变成“每瓦多少带宽、每 GW 多少 token、多少 downtime”。

最受益：OCS/MEMS、fiber management、CPO switch、coherent scale-across、AI network telemetry、DCIM/网络运维软件。

## 7. 2027 关键变化：行业拐点与最可能放量方向

### 7.1 拐点一：1.6T 成为新增 AI fabric 主流，3.2T 进入客户 qual

2027 基准情景下 1.6T 出货 1,200-1,800 万只；乐观情景 2,000-2,500 万只；极度乐观 3,000 万只级。3.2T 则从 2026 器件样品进入 2027 live demo/客户 qual，小批量收入先来自 400G/lane DSP、EML、EAM/MZM、测试平台。

### 7.2 拐点二：Rubin/MI400/TPU8/OpenAI-Broadcom XPU 推动 optical scale-up pilot

2027 多路线 rack-scale AI 系统并行：Rubin、MI400/MI455X Helios、TPU8、Trainium3、MTIA、OpenAI/Broadcom XPU。非 NVIDIA 平台尤其需要开放 scale-up 生态，OCI/CPX/CPO 会从规范阶段进入少数头部客户实装。

### 7.3 拐点三：AI scale-across 和 1600ZR/coherent-lite 成为隐蔽大市场

当 AI 工厂从单楼、单园区扩展到 metro/regional，光纤对数、功耗、放大站空间、加密和低延迟成为瓶颈。Marvell COLORZ 1600、Ciena hyper-rail/FST、Nokia multi-rail ILA/3.2T coherent-lite 会在 2027 获得更高投资权重。

## 8. 头部公司与细分技术地图

### 8.1 标准、平台与系统定义

| 方向 | 公司 |
|---|---|
| OCI MSA 创始成员 | AMD、Broadcom、Meta、Microsoft、NVIDIA、OpenAI |
| Open CPX MSA | Ciena、Coherent、Marvell、Molex、Samtec、TeraHop |
| XPO MSA/生态 | Arista、Marvell、Eoptolink、Lightmatter、TeraHop、Linktel、Coherent 等主要模块/光引擎供应商 |
| AI network 系统 | NVIDIA、Broadcom、Arista、Cisco、Juniper/HPE、Celestica、Accton/Edgecore、UfiSpace、Wiwynn/QCT |
| Hyperscaler 架构牵引 | Google、AWS、Meta、Microsoft、OpenAI、Oracle、xAI、Anthropic、ByteDance、Alibaba、Tencent、Baidu |

### 8.2 光模块、光器件、硅光与 CPO

| 细分 | 代表公司 |
|---|---|
| 800G/1.6T 模块 | Innolight/中际旭创、Eoptolink/新易盛、Coherent、Lumentum、AOI、Fabrinet、Foxconn、Luxshare、Hisense Broadband、Accelink、HG Genuine、Linktel、Source Photonics |
| EML/EAM/PD/VCSEL/InP laser | Lumentum、Coherent、Broadcom、Mitsubishi Electric、Sumitomo Electric、Sony/Hamamatsu、中国 InP/VCSEL 供应链 |
| SiPh foundry/platform | GlobalFoundries Fotonix/SCALE、TSMC COUPE、Intel Silicon Photonics、Tower Semiconductor、Samsung Foundry、UMC、OpenLight |
| CPO/CPX/NPO optical engine | NVIDIA、Broadcom、Ciena Vesta、Coherent、Marvell、Lumentum、GF、Ayar Labs、Lightmatter、Celestial AI、TeraHop、Samtec、Molex |
| Photonic I/O startups | Ayar Labs、Lightmatter、Celestial AI、Nubis Communications、Xscape Photonics、POET、HyperLight、Lightwave Logic、Sicoya、DustPhotonics、Ranovus、Enosemi/AMD、Scintil Photonics |
| ELS/高功率光源 | Lumentum、Coherent、Broadcom、Ayar Labs 生态、OIF ELSFP 生态 |

### 8.3 芯片、交换、DSP、铜互联

| 细分 | 代表公司 |
|---|---|
| Switch ASIC | Broadcom Tomahawk/Jericho、NVIDIA Spectrum/Quantum、Cisco Silicon One、Marvell、Intel Tofino 生态存量 |
| NIC/DPU/SuperNIC | NVIDIA ConnectX/BlueField、Broadcom Thor、Marvell、AMD Pensando、Intel IPU、AWS Nitro |
| PAM4 DSP/retimer | Broadcom Taurus/Sian、Marvell、Credo Bluebird、Astera Labs、MaxLinear、MACOM、Alphawave Semi |
| Coherent DSP | Marvell Electra/Libra、Cisco/Acacia、Ciena WaveLogic、Nokia/Infinera ICE、Coherent |
| AEC/DAC/ACC | Credo、Astera Labs、Broadcom、Marvell、Parade、Amphenol、TE Connectivity、Molex、Luxshare、BizLink、Samtec、Carlisle、FIT/Foxconn |
| PCIe/CXL optical | Broadcom、Marvell、Astera Labs、Credo、Synopsys、Cadence、Rambus、Ayar Labs、Celestial AI |

### 8.4 连接、光纤、热管理、测试与制造

| 细分 | 代表公司 |
|---|---|
| 光连接器/高密 fiber | Corning、Senko、US Conec、Sumitomo Electric、Amphenol、TE、Molex、Samtec、Fujikura、OFS |
| XPO/CPX 机械与液冷 | Arista、Molex、Samtec、TE、Amphenol、nVent、Boyd、CoolIT、Vertiv、Schneider、Danfoss、Parker/CPC |
| OCS/MEMS/WSS | Google Apollo、Lumentum、Calient、Polatis/HUBER+SUHNER、Coherent、Nokia、Ciena、NTT/日本光交换生态 |
| Coherent line system | Ciena、Nokia/Infinera、Cisco/Acacia、Juniper、NEC、Marvell、Coherent、Lumentum |
| 测试设备 | Keysight、VIAVI、Anritsu、Tektronix、EXFO、Spirent、MultiLane、FormFactor、Advantest、Teradyne |
| EMS/组装 | Fabrinet、Foxconn、Jabil、Celestica、Flex、Sanmina、Pegatron、Wistron、Quanta/QCT、Wiwynn |

## 9. 投资跟踪指标

1. **1.6T 出货与 ASP**：Cignal/LightCounting/Dell'Oro/TrendForce 口径是否继续上修；2026H2 是否出现价格战。
2. **NVIDIA Spectrum-X Photonics H2 2026 交付**：SN6800/SN6810、Quantum-X800 CPO switch 客户和量。
3. **OCI MSA 新成员与 v1.1/v2.0**：是否加入 Google/AWS/Arista/Cisco/Marvell/Ciena/Lightmatter/Ayar 等更多生态。
4. **Open CPX 规格落地**：Ciena Vesta 200、Samtec/Molex connector、TeraHop engine 是否被 100T/200T switch 采用。
5. **XPO MSA 扩员与 204.8T switch 路线**：Arista 是否给出 2027 量产平台，Marvell/Lightmatter/Eoptolink 是否形成 reference design。
6. **400G/lane 器件良率**：Broadcom Taurus、Lumentum 400G EML、OpenLight 3.2T PIC、Coherent 400G/lane link 的量产进展。
7. **CPO 现场维护案例**：ELS 冗余、field replacement、CMIS/flight recorder、故障率是否过关。
8. **Google Apollo OCS 扩散**：是否从 TPU/Ironwood 扩到其他云厂或 GPU Ethernet fabric。
9. **coherent scale-across 订单**：Marvell COLORZ 1600、Ciena hyper-rail/FST、Nokia 1600ZR/CL 的 hyperscaler 采用。
10. **铜互联边界**：DAC/AEC 在 200G/lane 下可覆盖的长度、功耗和误码率；OCI 是否提前替代部分 rack 内铜。

## 10. 主要资料来源

- [OCI MSA 官方网站与目标](https://oci-msa.org/)
- [OCI 200G Optical Compute Interconnect Line Interface Specification v1.0](https://oci-msa.org/assets/files/200G-OCI-Optical-Phy-Specification-v1.0.pdf)
- [GlobalFoundries SCALE CPO/OCI MSA capable platform](https://gf.com/gf-press-release/globalfoundries-accelerates-adoption-of-co-packaged-optics-for-advanced-ai-data-centers-with-scale-optical-module-solution/)
- [Arista XPO MSA 12.8T liquid-cooled pluggable optics](https://www.arista.com/en/company/news/press-release/23697-pr-20260311)
- [Marvell joins XPO MSA](https://www.marvell.com/blogs/marvell-joins-xpo-msa-to-accelerate-innovation-in-ai-optical-modules.html)
- [Open CPX MSA overview](https://convergedigest.com/open-cpx-msa-aims-to-standardize-co-packaged-optical-engines/)
- [Ciena Vesta 200 6.4T CPX optical engine](https://www.ciena.com/about/newsroom/press-releases/ciena-unveils-the-industrys-highest-density-lowest-power-pluggable-optical-engine-to-meet-data-center-ai-demands)
- [NVIDIA Silicon Photonics](https://www.nvidia.com/en-in/networking/products/silicon-photonics/)
- [NVIDIA Spectrum-X Ethernet Photonics technical blog](https://developer.nvidia.com/blog/scaling-power-efficient-ai-factories-with-nvidia-spectrum-x-ethernet-photonics/)
- [NVIDIA Vera Rubin platform release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx)
- [Broadcom OFC 2026 AI infrastructure release](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai)
- [Broadcom Taurus 400G/lane optical DSP](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next)
- [Lumentum OFC 2026 demonstrations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx)
- [Marvell COLORZ 1600 / 2nm coherent DSP](https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html)
- [OpenLight 3.2T DR8 and 1.6T LRO/LPO PICs](https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants)
- [OFC 2026 official exhibit release](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-exhibit-connects-the-global-optical-ecosystem-powering-ai-era-data-centers-and-networks/)
- [TrendForce: Google OCS / 800G+ modules over 60% by 2026](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- [TrendForce: Top nine CSP 2026 CapEx to US$830B](https://www.trendforce.com/presscenter/news/20260506-13033.html)
- [TrendForce: optical interconnect boom and Southeast Asia outsourcing](https://www.trendforce.com/presscenter/news/20260505-13031.html)
- [LightCounting: AI optics for AI clusters, 2025-2026 market](https://www.lightcounting.com/newsletter/en/january-2026-optics-for-ai-clusters-366)
- [Lightwave/Cignal AI summary of 2025 optical component revenue](https://www.lightwaveonline.com/home/article/55343202/ai-driven-datacenter-and-transport-builds-drove-optical-component-revenue-to-almost-25b-in-2025)
# 行业调研：【OCS光路交换】

> 研究日期：2026-05-08  
> 研究范围：最近半年，重点覆盖 2026 年 OFC / OCP / 头部公司发布会、订单、公告、高管表述、技术白皮书与行业报告。  
> 核心口径：本文的 OCS 指 Optical Circuit Switching / Optical Path Switching，即光路交换、光交叉连接、光电路交换及其控制平面。为避免高估，本文区分三类市场：
>
> 1. **商用 OCS 硬件收入**：第三方 OCS 设备、光学引擎、控制机箱与运维软件可确认收入。
> 2. **AI-OCS 部署价值**：Google 等 hyperscaler 自研/定制 OCS、光纤、光模块、控制平面、集成服务等合计价值；这部分对产业趋势很重要，但不一定全部流向上市供应商。
> 3. **OCS 关联光互联市场**：800G/1.6T 光模块、铜互联、连接器、光纤管理、CPO/CPX/ELS 等，不全部计入 OCS，但会被 OCS 架构显著放大。

## 0. 一页结论

2026 年是 OCS 从 Google TPU 网络的“架构级验证”走向 AI 数据中心生产侧扩散的拐点年。TrendForce 对 Google Apollo OCS 的描述显示，OCS 通过 MEMS 微镜实现光纤到光纤的直接连接，避免传统交换机的 O-E-O 转换；单台 OCS 约 100W，而传统交换机约 3000W，功耗降幅约 95%。这个量级的能耗差，在 2026 年百万卡级 AI 集群建设中足以改变网络层设计权重。

最可能在 2026 年放量的路径不是“CPO 直接替代一切”，而是更务实的组合：**rack 内短距铜互联 / DAC / AEC + scale-out 800G/1.6T 可插拔光模块 + MEMS/free-space OCS 光路重构 + packet switch 继续承担弹性转发**。Google Ironwood/TPU 网络最适合 OCS；NVIDIA GPU、AWS Trainium、AMD MI350 等体系在 2026 年仍以 InfiniBand/Ethernet packet fabric 为主，但会在大规模训练集群、推理池重分区、跨机房/跨楼栋 scale-across 链路中开始引入 OCS。

从可投资角度，OCS 的价值不只在替换交换机端口，而在三件事：**降低网络功耗、减少 packet hop 与光电转换、把 AI 集群拓扑从固定布线变成可调度资产**。如果 2026-2027 AI 基础设施建设按极度乐观情景推进，OCS 有机会从“Google 内部架构优势”变成 hyperscaler 标配组件。

本文给出的核心市场判断如下：

| 口径 | 未来 3 个月 | 未来 12 个月 | 未来 24 个月 |
|---|---:|---:|---:|
| 商用 OCS 硬件收入，基准 | 1.5-3.5 亿美元 | 8-16 亿美元 | 18-40 亿美元 |
| 商用 OCS 硬件收入，乐观 | 3.5-7.0 亿美元 | 16-32 亿美元 | 40-80 亿美元 |
| 商用 OCS 硬件收入，极度超预期 | 7-12 亿美元 | 32-55 亿美元 | 80-140 亿美元 |
| AI-OCS 部署价值，含自研/光模块/集成，基准 | 5-12 亿美元 | 30-80 亿美元 | 80-180 亿美元 |
| AI-OCS 部署价值，乐观 | 12-25 亿美元 | 80-180 亿美元 | 180-400 亿美元 |
| AI-OCS 部署价值，极度超预期 | 25-45 亿美元 | 180-350 亿美元 | 400-700 亿美元 |

行业投资优先级排序：

1. **高 radix MEMS/free-space OCS 与控制平面**：2026 年最接近生产放量，供需紧、客户集中、认证壁垒高，毛利弹性最大。
2. **OCS 关联 800G/1.6T 光模块、DSP、激光器、硅光、EML**：OCS 会放大端口和光纤需求，是最大收入池。
3. **高密度光纤管理、连接器、MPO/MTP、MCF、多芯光纤与自动化配线**：AI rack 光纤数量暴涨后，工程交付成为瓶颈。
4. **铜互联、AEC/ACC、retimer、linear drive 生态**：rack 内短距仍由铜承担，和 OCS 不是替代关系，而是共同组成低功耗网络。
5. **SiPh OCS、CPO/CPX/NPO/XPO、ELS 外置激光源**：2026 年更多是验证和早期采购，2027-2028 年可成为第二阶段弹性。

最大风险是：Google 等头部客户的 OCS 架构可能高度自研/captive，第三方供应商只能获得部分光学组件和代工收入；同时 Broadcom/NVIDIA/Arista/Cisco 等 packet switching 生态有能力通过 102.4T/204.8T 交换芯片、CPO、XPO 和更强调度软件继续捕获大部分网络价值。

## 1. 2026 AI 数据中心大规模建设中的机遇、挑战与技术路线

### 1.1 AI 芯片路线对 OCS 的牵引

本项目已有 AI 芯片研究显示，2026 年出货量和建设强度最大的 AI 芯片/系统大概率集中在 NVIDIA B300/GB300、B200/GB200 延续版本、Google Ironwood/TPU、AWS Trainium2/3、AMD MI350、Microsoft Maia、Meta MTIA、华为昇腾、寒武纪等；2027 年 Rubin、MI400/Helios、TPU8/TPU 8t/8i、Trainium4、OpenAI/Broadcom 自研芯片等接力。

OCS 对不同芯片平台的适配强弱不同：

| AI 芯片/系统 | 2026 网络技术背景 | OCS 适配度 | 2026-2027 判断 |
|---|---|---:|---|
| Google Ironwood / TPU | rack 内短距铜连接，rack 间 all-optical，Google 已公开强调 co-designed AI stack | 极高 | 2026 年最可能生产放量。Apollo OCS 是行业风向标，可能驱动 OCS 从单客户向多客户扩散 |
| NVIDIA B300/GB300 | rack 内 NVLink/NVLink Switch，scale-out 800G InfiniBand/Ethernet，Spectrum-X / Quantum-X | 中高 | 2026 年仍以 packet fabric 为主，OCS 先用于大集群重构、跨 pod/campus、训练池分区；2027 年 Rubin 之后提升 |
| AWS Trainium2/3 | NeuronLink + EFA/Ethernet，大规模自研网络调度能力 | 中高 | AWS 有自研基础设施能力，若训练/推理集群分区频繁，2027 年可能采用 OCS 或类 OCS 光交叉 |
| AMD MI350 / MI400 Helios | Ethernet/UALink/open accelerator fabric，800G/1.6T scale-out | 中 | 2026 年以 Ethernet scale-out 为主，OCS 更多是超大客户定制；MI400/Helios 后潜力提高 |
| Microsoft Maia / Meta MTIA | 自研 AI 芯片 + Ethernet/custom fabric | 中高 | 2026 年多为内部验证，2027 年若推理池大规模扩张，OCS 可用于资源池重分区 |
| OpenAI/Broadcom 自研 ASIC | 高度定制网络，预计重视能效和可调拓扑 | 高 | 2027 年是观察点，极度乐观情景下会把 OCS 作为非 NVIDIA 集群差异化网络 |
| 华为昇腾 / 寒武纪 / 阿里平头哥 | 国内光模块、交换机、光纤产业链完整，但高端 OCS 控制和认证周期较长 | 中 | 2026 年以传统光互联和交换机为主，2027-2028 年国产 OCS 进入试点和局部放量 |

### 1.2 2026 正在使用的关键技术

| 技术 | 当前位置 | 优点 | 挑战 | 2026 判断 |
|---|---|---|---|---|
| MEMS/free-space OCS | Google Apollo、Lumentum/DiCon/Calient/Polatis/Molex 等 | 大 radix、低功耗、无 O-E-O、适合拓扑重构 | 光学对准、插损、控制调度、客户认证 | 最可能商业放量的 OCS 主线 |
| 硅光 OCS / PIC switch | iPronics 32x32 等早期出货与验证 | 小型化、低功耗、可集成 | 插损、串扰、规模化良率、大端口扩展 | 2026 早期放量，2027 进入更多 pilot |
| Packet switch：InfiniBand/Ethernet | NVIDIA、Broadcom、Arista、Cisco 等主导 | 纳秒级动态转发、生态成熟、运维成熟 | 功耗高、层级多、AI 流量下利用率压力 | 2026 仍是主流，OCS 是补充而非完全替代 |
| 800G/1.6T OSFP/QSFP-DD 光模块 | AI scale-out 主力 | 供应链成熟度最高、可插拔易维护 | DSP/激光器/散热/良率压力 | 2026 最大收入池 |
| CPO/CPX/NPO/XPO/ELS | OFC 2026 展示密集 | 降低电通道损耗，面向 102.4T/204.8T | 可维护性、激光源、标准、客户导入 | 2026 验证，2027+ 才能显著放量 |
| DAC/AEC/ACC 铜互联 | rack 内、near rack 低成本低延迟 | 成本低、功耗低、部署快 | 距离受限，线缆管理复杂 | 与 OCS 共存，2026 强放量 |
| 高密度光纤/MCF/连接器 | GB200/NVL72、Rubin/NVL144 后需求暴涨 | 解决光纤数量和空间问题 | 施工、清洁、测试、标准化 | 2026 开始成为显性瓶颈 |

### 1.3 新技术成熟和放量时间：三情景

| 技术 | 2026 状态 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|---|
| MEMS/free-space OCS | Google 生产部署，商用订单开始变大 | 2026H2 头部云厂规模采购，2027 年进入多云厂 | 2026H2 第二家/第三家 hyperscaler 明确订单，2027 年商用收入 40-80 亿美元 | 2026 年底成为百万卡集群标配，2027 年部署价值 400 亿美元以上 |
| OCS 控制平面/调度软件 | Google 内部最成熟，外部生态刚起步 | 2026 年随硬件绑定销售，2027 年形成可独立报价软件层 | 2026H2 进入 SONiC/开放接口生态，客户切换成本上升 | 调度软件成为 AI 集群“拓扑编译器”，软件毛利接近 80-90% |
| 硅光 OCS | iPronics 32x32 出货/展示 | 2027 年小规模用于边缘 pod、测试平台、特定推理池 | 2026H2 128x128/更高 radix 样机被云厂验证 | 2027 年成为 MEMS 的高速/小型化补充，24 个月市场 70-150 亿美元 |
| 800G 光模块 | 已大规模放量 | 2026 年 AI 光模块主力，800G+ 占比超过 60% | 2026 年 Google/Meta/Microsoft 拉货超预期 | 2026 年供不应求延续，ASP 与高端毛利保持强势 |
| 1.6T 光模块 | 2026 主流化开始 | 2026 出货超过 500 万只，2027 年成为新建集群主力 | 2026H2 1.6T 占新采购 25-35% | 2027 年 1.6T 成为默认端口，3.2T 提前验证 |
| CPO/CPX/ELS | OFC 2026 高密度展示 | 2027 年交换机侧早期生产，2028 年明显放量 | 2026H2 102.4T/204.8T 平台启动批量验证 | 2027 年部分 hyperscaler 直接把 CPO/XPO 纳入 AI 网络主线 |
| XPO 12.8T pluggable | Arista/Coherent 等推动 | 2027 年先在高端交换机验证 | 2027H1 进入云厂小批量 | 2027 年形成 CPO 替代路径，抢占可维护性更强的份额 |
| MCF/光纤自动化 | OCP/供应链高度关注 | 2026 年随 GB300/TPU 机房工程增量采购 | 2026H2 成为大机房设计规范 | 2027 年 MCF/自动配线成为 OCS 架构的关键供给瓶颈 |

2026 年最可能的技术路径：**MEMS OCS + 800G/1.6T pluggable + copper rack-scale + packet fabric hybrid**。极度乐观情况下，OCS 不会完全替代 packet switch，而是替代一部分 spine/aggregation hop、固定跨 pod 布线和低利用率网络冗余。

## 2. 已经开始放量的关键产品：市场规模、渗透率与利润率

### 2.1 高 radix MEMS/free-space OCS 系统

已放量证据包括：Google Apollo OCS 架构公开、OCP 2026 OCS 白皮书、Lumentum 2026 财年 Q2 提到 OCS 出货超过 1000 万美元且增长路径明确，Q3 又公告与一家领先 hyperscale cloud/AI data center operator 签署 advanced OCS 的多年、数十亿美元采购协议。OFC 2026 上，OCS 从论文概念变成展商、白皮书和订单共同指向的生产级方向。

| 时间 | 基准市场规模 / 渗透率 | 乐观市场规模 / 渗透率 | 极度超预期市场规模 / 渗透率 |
|---|---:|---:|---:|
| 未来 3 个月 | 1.5-3.5 亿美元；新建 AI xPU/rack OCS 渗透率 3-6% | 3.5-7.0 亿美元；6-10% | 7-12 亿美元；10-16% |
| 未来 12 个月 | 8-16 亿美元；6-12% | 16-32 亿美元；12-22% | 32-55 亿美元；22-35% |
| 未来 24 个月 | 18-40 亿美元；12-22% | 40-80 亿美元；22-40% | 80-140 亿美元；40-60% |

利润率判断：

| 情景 | 毛利率区间 | 逻辑 |
|---|---:|---|
| 基准 | 38-50% | 客户集中、定制化强，但早期良率/服务成本较高 |
| 乐观 | 45-58% | 供不应求，认证通过后 ASP 强，软件/服务附加值上升 |
| 极度超预期 | 55-68% | 高端 radix、低插损、控制平面能力稀缺，客户按节能和 GPU 利用率定价 |

### 2.2 OCS 关联 800G/1.6T 光模块

OFC 2026 与本项目本地报告交叉验证后，2026 年 800G+ 光模块是 AI 光互联最大放量产品。Cignal AI/行业数据指向 2025 年光器件收入接近 250 亿美元、datacom 超过 180 亿美元、coherent 模块接近 60 亿美元；本地 OFC 报告统计 2026 年 800G 出货量可超过 2000 万只，1.6T 超过 500 万只。TrendForce 认为 800G+ 光模块占比可从 2024 年 19.5% 提升至 2026 年超过 60%，且 Google 2026 年 TPU 相关部署可能驱动超过 600 万只 800G+ 光模块需求。

| 时间 | 基准市场规模 / 渗透率 | 乐观市场规模 / 渗透率 | 极度超预期市场规模 / 渗透率 |
|---|---:|---:|---:|
| 未来 3 个月 | 30-50 亿美元；800G+ 占 AI 光模块 60-70% | 50-80 亿美元；65-75% | 80-120 亿美元；70-80% |
| 未来 12 个月 | 160-280 亿美元；1.6T 新增端口 10-20% | 280-450 亿美元；1.6T 20-35% | 450-700 亿美元；1.6T 35-50% |
| 未来 24 个月 | 320-550 亿美元；1.6T 30-45% | 550-950 亿美元；1.6T 45-60% | 950-1500 亿美元；1.6T 60-75%，3.2T 进入早期 |

利润率判断：

| 情景 | 光模块整机毛利率 | 高端核心器件/激光/DSP/SiPh 毛利率 |
|---|---:|---:|
| 基准 | 25-38% | 40-55% |
| 乐观 | 32-45% | 50-65% |
| 极度超预期 | 38-50% | 60-75% |

OCS 对光模块的影响不是简单替代，而是增加“可重构光纤 fabric”中的端口密度、测试需求、可靠性要求和高端规格比例。

### 2.3 OCS 控制平面、拓扑调度与运维软件

OCS 真正的壁垒不是“把光路接通”这么简单，而是把 AI job scheduler、网络遥测、光路重构、故障隔离、拥塞预测和 GPU/TPU 利用率联动起来。Google 的优势很大程度来自软硬一体化。

| 时间 | 基准市场规模 / 渗透率 | 乐观市场规模 / 渗透率 | 极度超预期市场规模 / 渗透率 |
|---|---:|---:|---:|
| 未来 3 个月 | 0.3-1.0 亿美元；主要随硬件绑定 | 1-2 亿美元；部分独立软件报价 | 2-4 亿美元；云厂按集群订阅 |
| 未来 12 个月 | 2-7 亿美元；商用 OCS 软件 attach rate 30-50% | 7-15 亿美元；50-70% | 15-30 亿美元；70-90% |
| 未来 24 个月 | 7-25 亿美元；进入多云厂运维体系 | 25-60 亿美元；成为 OCS 采购核心 | 60-120 亿美元；AI fabric OS 化 |

利润率判断：基准 65-80%，乐观 75-88%，极度超预期 85-92%。控制平面越接近 AI 调度器，越能定价。

### 2.4 高密度光纤管理、连接器、MCF-ready trunk

Sumitomo/OCP 生态的公开材料和本地报告显示，AI rack 光纤数量正在指数级增加：H200 rack 级别约数百根光纤，GB200/NVL72 可达到约 1440 strands，Rubin/NVL144 可能达到约 2880 strands。多芯光纤可节省 60-80% duct space。OCS 会进一步提高光纤管理复杂度，因为更多链路从“固定交换机端口”变成“可重构光路资产”。

| 时间 | 基准市场规模 / 渗透率 | 乐观市场规模 / 渗透率 | 极度超预期市场规模 / 渗透率 |
|---|---:|---:|---:|
| 未来 3 个月 | 2-6 亿美元；新 AI 机房高密度光纤渗透 20-35% | 6-10 亿美元；35-50% | 10-18 亿美元；50-65% |
| 未来 12 个月 | 12-35 亿美元；35-55% | 35-70 亿美元；55-75% | 70-120 亿美元；75-90% |
| 未来 24 个月 | 35-100 亿美元；50-70% | 100-180 亿美元；70-90% | 180-300 亿美元；接近标配 |

利润率判断：普通连接器/跳线 20-35%，高密度/低损耗/MCF/自动化配线 35-55%，极度紧缺时核心厂商可达 55-65%。

### 2.5 铜互联、DAC/AEC/ACC、retimer 与 OCS 的共生

Google Ironwood 一类系统说明 rack 内短距仍会大量使用铜，OCS 主要处理 rack 间、pod 间和可重构光路。2026 年 AI 网络不是“光完全替代铜”，而是“铜缩短到 rack 内，光承担 scale-out，OCS 负责拓扑重构”。

| 时间 | 基准市场规模 / 渗透率 | 乐观市场规模 / 渗透率 | 极度超预期市场规模 / 渗透率 |
|---|---:|---:|---:|
| 未来 3 个月 | 15-35 亿美元；rack 内高速铜 50-65% | 35-55 亿美元；65-75% | 55-80 亿美元；75-85% |
| 未来 12 个月 | 70-150 亿美元；高速铜/AEC attach 55-70% | 150-260 亿美元；70-85% | 260-400 亿美元；85%+ |
| 未来 24 个月 | 120-280 亿美元；仍为 rack 内主力 | 280-500 亿美元；AEC/linear drive 占比提升 | 500-750 亿美元；铜+光混合成为默认架构 |

利润率判断：连接器/线缆 20-38%，AEC/retimer 芯片 55-75%，极度超预期下高端短距互联芯片可阶段性超过 75% 毛利。

## 3. 在研关键产品与快速增长子技术

### 3.1 SiPh OCS / PIC 光交换阵列

iPronics 在 OCP/行业活动中展示 32x32 silicon photonics OCS，具备 1024 optical interconnects、sub-ms reconfiguration、低功耗等特征。SiPh OCS 的长期优势是小型化、潜在低成本和可与硅光/ELS/CPO 生态整合；短期瓶颈是插损、串扰、thermal tuning、良率和大 radix 扩展。

| 时间 | 基准市场规模 / 渗透率 | 乐观市场规模 / 渗透率 | 极度超预期市场规模 / 渗透率 |
|---|---:|---:|---:|
| 未来 3 个月 | 小于 5000 万美元；试点 | 0.5-1.5 亿美元；云厂验证 | 1.5-3 亿美元；小批量部署 |
| 未来 12 个月 | 1-6 亿美元；OCS 端口 1-3% | 6-15 亿美元；3-8% | 15-30 亿美元；8-15% |
| 未来 24 个月 | 8-30 亿美元；5-10% | 30-70 亿美元；10-20% | 70-150 亿美元；20-35% |

利润率：基准 45-60%，乐观 55-70%，极度超预期 65-80%。如果 SiPh OCS 与控制平面、外置激光、光 backplane 绑定，长期价值捕获会显著高于普通模块装配。

### 3.2 CPO/CPX/NPO/XPO 与 OCS 协同

OFC 2026 的重要信号是：1.6T 已经主流化，3.2T/400G-per-lane 开始进入验证；Broadcom、NVIDIA、Coherent、Marvell、Arista、Open CPX MSA 等都在围绕 CPO/CPX/XPO/ELS 给出路径。OCS 与 CPO 的关系是协同：CPO 降低交换 ASIC 到光的电通道损耗，OCS 减少部分 packet switching 层级和固定布线。

| 时间 | 基准市场规模 / 渗透率 | 乐观市场规模 / 渗透率 | 极度超预期市场规模 / 渗透率 |
|---|---:|---:|---:|
| 未来 3 个月 | 1-4 亿美元；demo/样机 | 4-8 亿美元；客户验证 | 8-15 亿美元；首批系统订单 |
| 未来 12 个月 | 8-25 亿美元；102.4T/204.8T 早期 | 25-50 亿美元；多云厂 pilot | 50-100 亿美元；部分生产导入 |
| 未来 24 个月 | 40-90 亿美元；交换机侧明显放量 | 90-180 亿美元；CPO/XPO 双路径 | 180-350 亿美元；高端 AI 网络标配之一 |

利润率：CPO 光引擎/ELS 45-65%，XPO 高端模块 35-55%，系统级整合 30-50%。极度超预期时，ELS/激光安全/热插拔维护能力是高毛利点。

### 3.3 多芯光纤、光纤自动化与机房级光 backplane

OCS 的规模化会把“光纤施工和维护”从低价值配套变成关键瓶颈。AI rack 的 fiber count、清洁、插损测试、极性管理、弯曲半径、标签和自动化运维会直接影响 GPU/TPU 上线速度。

| 时间 | 基准市场规模 / 渗透率 | 乐观市场规模 / 渗透率 | 极度超预期市场规模 / 渗透率 |
|---|---:|---:|---:|
| 未来 3 个月 | 小于 1 亿美元；MCF/自动化专项 | 1-3 亿美元 | 3-6 亿美元 |
| 未来 12 个月 | 2-10 亿美元；AI 新机房 5-10% | 10-25 亿美元；10-25% | 25-50 亿美元；25-40% |
| 未来 24 个月 | 10-40 亿美元；15-30% | 40-90 亿美元；30-50% | 90-200 亿美元；50-70% |

利润率：普通光纤光缆 15-30%，高密度低损耗连接器 30-50%，MCF/自动化配线/测试系统 45-65%。

### 3.4 AI fabric scheduler 与 workload-aware topology compiler

OCS 对 AI 集群价值最大的一点，是把网络拓扑从静态结构变成可随训练任务、专家并行、pipeline 并行、推理流量峰谷调整的动态资源。未来真正高壁垒产品可能不是单台 OCS，而是“OCS + packet fabric + job scheduler + telemetry”的系统。

| 时间 | 基准市场规模 | 乐观市场规模 | 极度超预期市场规模 |
|---|---:|---:|---:|
| 未来 3 个月 | 小于 5000 万美元 | 0.5-1 亿美元 | 1-3 亿美元 |
| 未来 12 个月 | 1-5 亿美元 | 5-15 亿美元 | 15-40 亿美元 |
| 未来 24 个月 | 5-20 亿美元 | 20-70 亿美元 | 70-150 亿美元 |

利润率：70-90%。它能定价的原因是直接提升 GPU/TPU 利用率。百万卡集群中，即便利用率提升 1-2 个百分点，也可能对应数十亿美元级别资本效率。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 主要产能和能力分布

| 环节 | 地区/公司 | 能力特点 |
|---|---|---|
| MEMS/free-space OCS | Google 自研生态、Lumentum、DiCon Fiberoptics、Calient、Polatis/HUBER+SUHNER、Molex、Eoptolink 等 | 光学设计、MEMS 微镜、准直器、低插损对准、机箱和控制平面 |
| SiPh/PIC OCS | iPronics、Ayar Labs、Celestial AI、Lightmatter、OpenLight、imec、GlobalFoundries、TSMC、Tower、Intel Silicon Photonics 等 | 硅光工艺、片上交换矩阵、外置激光、封装和测试 |
| AI 光模块 | 中际旭创、光迅科技、新易盛、Coherent、Lumentum、Fabrinet、AOI、海信宽带、华工科技、Source Photonics 等 | 800G/1.6T 模块、EML/SiPh、DSP、光引擎、封装测试 |
| DSP/SerDes/交换芯片 | Broadcom、Marvell、NVIDIA、Credo、MACOM、Astera Labs、Cisco/Acacia 等 | 224G/400G SerDes、retimer、DSP、switch ASIC、coherent DSP |
| 铜互联/AEC/连接器 | Credo、Astera、Amphenol、TE、Molex、Samtec、Luxshare、BizLink、Leoni、Bel Fuse 等 | rack 内高速铜缆、AEC/ACC、连接器和背板 |
| 光纤/连接器/MCF | Corning、Sumitomo Electric、Fujikura、Furukawa/OFS、Prysmian、Senko、US Conec、AFL、CommScope、长飞、亨通等 | 多芯光纤、高密度连接器、MPO/MTP、低损耗配线 |
| 测试与认证 | VIAVI、Keysight、EXFO、Anritsu、Tektronix、Luna、FormFactor 等 | 800G/1.6T/3.2T 测试、BER、插损、相干链路、可靠性 |

### 4.2 供给瓶颈

1. **MEMS 微镜与光学引擎良率**：高 radix 下微镜一致性、反射镀膜、角度控制和长期可靠性决定交付能力。
2. **光纤阵列、准直器和被动对准**：OCS 不是普通盒子，低插损和通道一致性需要大量精密装调。
3. **插损预算与 800G/1.6T 链路裕量**：OCS 加入链路后，光模块、连接器、光纤长度、温漂都会压缩 link budget。
4. **控制平面和调度算法**：OCS 切换速度虽可到 ms/sub-ms，但 AI 流量调度要避免抖动、拥塞和 job 干扰。
5. **客户认证周期**：hyperscaler 会做高温、振动、寿命、误码、故障恢复、现场可维护性等长期验证。
6. **800G/1.6T 光模块供应**：EML、SiPh、DSP、CW laser、封装、测试设备紧缺会反向限制 OCS fabric 部署。
7. **高密度光纤工程交付**：清洁、标签、极性、弯曲半径、插拔寿命、现场测试都可能拖慢机房上线。
8. **人才瓶颈**：同时懂 MEMS、自由空间光学、硅光、网络调度和 hyperscaler 运维的人极少。
9. **系统集成责任边界**：OCS 故障可能表现为 GPU job 掉速或误码，供应商需要承担跨硬件/软件/运维问题。
10. **客户集中与 captive 设计**：最大需求方可能自研架构，供应商扩产需要承担订单集中风险。

### 4.3 OCS 成本结构与毛利决定因素

高端 OCS 系统的 BOM/单位成本可粗略拆分为：

| 成本项 | 占比区间 | 说明 |
|---|---:|---|
| MEMS 微镜/自由空间光学引擎 | 20-35% | 核心性能来源，决定端口数、插损、可靠性 |
| 光纤阵列、准直器、连接器、fiber shuffle | 20-30% | 高密度端口和低损耗对准成本很高 |
| 机箱、电源、控制板、散热 | 12-20% | 功耗低但可靠性要求高 |
| 校准、测试、老化和良率损耗 | 20-30% | 早期放量最大成本项之一 |
| 控制软件、遥测、运维接口 | 5-15% | 长期最有毛利弹性的部分 |
| 质保、现场服务和备件 | 5-10% | hyperscaler 生产环境要求高 |

ASP 粗略假设：64x64 OCS 约 3-8 万美元，128x128 约 7-18 万美元，320/384 端口级约 18-50 万美元，1024+ 高端系统早期可达 80-200 万美元。实际价格高度取决于端口速率、插损、冗余、控制平面和采购规模。

OCS 的价格传导机制不是传统 cost-plus，而是“按节能、减少交换层级、提高 GPU/TPU 利用率、缩短交付周期”定价。如果 OCS 让一部分 3kW 级 packet switch 层被 100W 级光路重构替代，同时减少光电转换和机房供电压力，客户愿意为可靠、可调度、可运维的 OCS 支付高溢价。

## 5. 竞争格局与可量化壁垒

### 5.1 市场结构

2026 年 OCS 市场会呈现“两层集中”：

1. **部署价值高度集中在 Google 及少数 hyperscaler**。按 AI-OCS 部署价值，Google 相关内部/captive 架构可能占 2026 年 60-75%；如果 Lumentum 多年大单对应同一或相近客户，第三方可确认收入也会高度集中。
2. **商用硬件 CR3 预计 55-75%**。Lumentum、DiCon/Calient/Polatis/Molex/Eoptolink/iPronics 等各有专长，但真正能进入 hyperscaler 生产环境的供应商不会多。

在 OCS 关联光模块市场，CR5 也较高，中际旭创、新易盛、Coherent、Lumentum、Fabrinet/代工体系、光迅科技、海信宽带等会争夺 800G/1.6T 高端份额；DSP/SerDes 和 switch silicon 则由 Broadcom、Marvell、NVIDIA、Credo、Astera、MACOM 等捕获高毛利。

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 量化/表现 | 为什么能定价 |
|---|---|---|
| 低插损与端口一致性 | 高 radix 下每增加 0.1-0.5 dB 插损都会挤压 800G/1.6T 链路预算 | 客户按可用端口和误码风险付费，低插损直接减少昂贵重传和光模块冗余 |
| 切换速度与稳定性 | ms/sub-ms 重构、长期漂移和重复切换寿命 | AI job 重分区不能引发大面积抖动，稳定性是生产门槛 |
| 控制平面 | 与 job scheduler、telemetry、SONiC/gNMI、故障恢复集成 | 一旦进入客户运维栈，切换成本高，软件 attach 和服务收入可持续 |
| hyperscaler 认证 | 高温、振动、误码、寿命、现场维护、供应链审查 | 认证周期长，新进入者即使有样机也难抢生产份额 |
| 精密制造和校准规模 | 光学装调、自动测试、老化产线 | 扩产不是简单 SMT，良率和交付决定真实产能 |
| 客户定制与联合设计 | 端口数、拓扑、机柜、光纤管理、API 都可能定制 | 进入早的供应商可锁定下一代架构 |
| 与光模块/光纤生态绑定 | 需要共同满足链路预算和维护规范 | 能提供系统级责任的供应商议价力更强 |

### 5.3 价值链中最可能长期高 ROIC 的环节

最可能长期高 ROIC/高毛利的是三层：

1. **OCS 控制平面和 AI fabric scheduler**：直接影响 GPU/TPU 利用率，软件毛利高，客户切换成本强。
2. **高 radix OCS 光学引擎**：MEMS/free-space 与 SiPh OCS 都有深工艺壁垒，早期供不应求，认证后生命周期长。
3. **DSP/SerDes/激光器/硅光/ELS 等核心光电器件**：单位价值高，设计门槛高，供应商集中。

相对容易被压价的是普通光模块装配、普通光纤跳线和纯机箱集成；但在 800G/1.6T 供不应求阶段，即使装配环节也会出现阶段性高毛利。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点一：Google Apollo/Ironwood 把 OCS 从实验架构推到生产验证

Google 的公开信号很强：Ironwood 是为推理时代 co-designed 的 TPU stack，TrendForce 又明确提到 Apollo OCS 的低功耗和光路直连架构。2026 年如果 Google TPU 建设达到数百万颗级别，OCS 会成为“非 NVIDIA AI 网络”的标杆。

最可能放量子方向：MEMS OCS、OCS 控制平面、800G+ 光模块、高密度光纤配线。

### 拐点二：Lumentum 多年数十亿美元 OCS 协议确认商用化收入通道

Lumentum 2026 财年 Q3 公告称，已与一家领先 hyperscale cloud and AI data center operator 签署 advanced optical circuit switches 的多年、数十亿美元采购协议。这是 OCS 从技术叙事变成供应链订单的关键证据。

最可能放量子方向：高端 OCS 光学引擎、校准测试产线、光纤阵列、低插损连接器。

### 拐点三：800G/1.6T 光模块供给主线与 OCS 形成正反馈

2026 年 800G+ 占 AI 光模块比例超过 60%、1.6T 超过 500 万只出货的预期，让 OCS 有了足够高速的光接口基础。OCS 不需要等待 CPO 大规模成熟即可先放量。

最可能放量子方向：800G/1.6T OSFP、EML/SiPh、DSP、光测试、铜互联 AEC/ACC。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点一：OCS 从 Google 扩散到第二波 hyperscaler

2027 年 Rubin、MI400/Helios、TPU8、Trainium3/4、OpenAI/Broadcom 自研 ASIC 和更多推理集群会同时建设。如果 2026 年 Google 证明 OCS 能显著提高能效和集群利用率，Meta、Microsoft、AWS、OpenAI、Oracle、xAI 等都有动力做 OCS 或类 OCS pilot。

最可能放量子方向：商用 OCS 系统、开放控制 API、fabric scheduler、跨 pod 光路调度。

### 拐点二：1.6T 成为默认端口，3.2T/400G-per-lane 进入验证

2027 年新建 AI 集群会更偏向 1.6T，3.2T 开始进入高端验证；这会让传统 packet switch 的功耗和散热压力更大，也提高 OCS 减少 O-E-O 转换的吸引力。

最可能放量子方向：1.6T/3.2T 光模块、CPO/XPO/CPX、ELS、coherent scale-across。

### 拐点三：光纤数量和工程交付成为 AI 机房硬约束

GB300、Rubin/NVL144、TPU pod 扩张会让 fiber count、连接器密度、清洁和现场测试成为交付瓶颈。OCS 架构如果扩大，会进一步提高对自动化配线和光纤生命周期管理的需求。

最可能放量子方向：MCF、多芯连接器、自动化光纤管理、现场测试设备、机柜级光 backplane。

## 8. 头部公司与细分领域完整清单

### 8.1 OCS 系统、MEMS/free-space 光交换

| 公司 | 位置 | 优势 |
|---|---|---|
| Google | 自研/内部部署 | Apollo OCS、TPU 网络、软硬一体化调度，是行业最重要参考架构 |
| Lumentum | 美国 | advanced OCS 多年数十亿美元订单，激光/光器件/OCS 协同 |
| DiCon Fiberoptics | 美国 | MEMS optical switch、光学组件经验深 |
| Calient | 美国 | 大规模 photonic switch/3D MEMS OCS 历史积累 |
| Polatis / HUBER+SUHNER | 英国/瑞士 | 光交叉连接、低损耗光交换、运营商和数据中心经验 |
| Molex | 美国 | 光互联、连接器、系统集成和 hyperscaler 客户基础 |
| Eoptolink / 新易盛 | 中国 | 高端光模块与 OCS 相关产品推进，Google 生态预期强 |
| iPronics | 西班牙 | 32x32 SiPh OCS，sub-ms reconfiguration，硅光 OCS 代表公司 |
| Glimmerglass | 美国 | 光路交换历史厂商，更多偏运营商/光交叉连接经验 |
| NTT / NEC / Fujitsu | 日本 | 光网络、光电融合、IOWN/photonic networking 研发实力 |

### 8.2 硅光、光计算互联、光 fabric

iPronics、Ayar Labs、Celestial AI、Lightmatter、OpenLight、Intel Silicon Photonics、Broadcom、Marvell、Coherent、Ranovus、DustPhotonics、Sicoya、imec、GlobalFoundries、TSMC、Tower Semiconductor、Cisco/Acacia。

这些公司未必都直接卖 OCS，但在 SiPh OCS、ELS、CPO、chip-to-chip optical I/O、光 backplane、硅光平台上有关键技术和客户资源。

### 8.3 800G/1.6T 光模块与核心光器件

| 领域 | 公司 |
|---|---|
| 中国高端光模块 | 中际旭创、新易盛、光迅科技、华工科技、海信宽带、天孚通信、太辰光、仕佳光子、源杰科技、长芯盛 |
| 海外光模块/器件 | Coherent、Lumentum、AOI、Fabrinet、Source Photonics、Cisco/Acacia、Marvell、Broadcom |
| DSP/SerDes/coherent DSP | Broadcom、Marvell、NVIDIA、Credo、MACOM、Cisco/Acacia |
| 激光器/EML/SiPh 光引擎 | Lumentum、Coherent、Broadcom、Marvell、Intel Silicon Photonics、OpenLight、Eoptolink、Innolight 生态 |

### 8.4 交换芯片、网络设备与系统集成

NVIDIA/Mellanox、Broadcom、Marvell、Cisco、Arista、Juniper、Nokia、Celestica、Edgecore、Accton、Inventec、Wiwynn、Supermicro、HPE/Juniper、Dell、Lenovo、Foxconn、Quanta。

这些公司决定 OCS 是成为 packet fabric 的补充、旁路，还是深度整合到 AI network OS 中。Broadcom Tomahawk/Jericho、NVIDIA Spectrum-X/Quantum-X 和 Cisco/Arista 网络操作系统是 OCS 商业化必须面对的生态。

### 8.5 铜互联、AEC/ACC、连接器和线缆

Credo、Astera Labs、MACOM、Broadcom、Marvell、Amphenol、TE Connectivity、Molex、Samtec、Luxshare 立讯精密、BizLink、Leoni、Bel Fuse、安费诺、鼎通科技、沃尔核材。

### 8.6 光纤、连接器、MCF 与测试设备

| 领域 | 公司 |
|---|---|
| 光纤/光缆/MCF | Corning、Sumitomo Electric、Fujikura、Furukawa/OFS、Prysmian、长飞光纤、亨通光电、中天科技 |
| 高密度连接器 | Senko、US Conec、Molex、Amphenol、AFL、CommScope、TE Connectivity、太辰光、天孚通信 |
| 测试设备 | VIAVI、Keysight、EXFO、Anritsu、Tektronix、Luna、FormFactor、MPI |

## 9. 投资结论：用非常乐观的 AI 建设预期看 OCS

在非常乐观的 AI 基建假设下，OCS 的投资价值来自“网络能效瓶颈”和“拓扑可重构”两条主线。2026 年最确定的收入弹性来自高端 OCS 硬件订单、800G/1.6T 光模块、低损耗连接器、DSP/激光器和高速铜互联；2027 年更有想象力的是 OCS 控制平面、SiPh OCS、CPO/XPO/ELS 与机房级光 fabric。

基准情景下，OCS 在 2026 仍是 AI 网络中的高增长小市场，商用硬件收入 8-16 亿美元级别，但增速和毛利显著高于普通网络硬件。乐观情景下，第二波 hyperscaler 在 2026H2-2027H1 确认订单，商用 OCS 硬件 24 个月可到 40-80 亿美元。极度超预期情景下，OCS 被证明能显著提高百万卡集群利用率并降低功耗，24 个月商用硬件可达 80-140 亿美元，AI-OCS 部署价值可达 400-700 亿美元。

最值得跟踪的 2026 信号：

1. Lumentum OCS 订单转收入节奏、客户范围是否扩大、是否出现第二个多年大单。
2. Google Ironwood/TPU 2026 实际部署量、Apollo OCS 是否被更多公开材料确认。
3. Meta/Microsoft/AWS/OpenAI/Broadcom 自研 ASIC 网络是否出现 OCS/optical circuit switching 采购或工程岗位信号。
4. 1.6T 光模块价格和交期是否继续紧张，是否推动客户减少 packet hop、增加 OCS 光路。
5. OCP/SONiC/开放接口是否让 OCS 控制平面从单客户定制走向多客户标准。

## 10. 主要信息源与交叉验证

### 第一手/准第一手公开资料

- TrendForce：Google Apollo OCS、800G+ 光模块、Google TPU 相关需求判断。  
  <https://www.trendforce.com/presscenter/news/20260210-12919.html>
- OCP：2026 Optical Circuit Switching White Paper。  
  <https://www.opencompute.org/documents/ocp-ocs-white-paper-april-2026-final-pdf>
- Lumentum：2026 财年 Q3 业绩公告，披露 advanced optical circuit switches 多年、数十亿美元采购协议。  
  <https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx>
- Lumentum：OFC 2026 AI infrastructure 光互联展示。  
  <https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx>
- Google Cloud：Inside the Ironwood TPU co-designed AI stack。  
  <https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack/>
- Broadcom：OFC 2026 AI networking solutions。  
  <https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai>
- Broadcom：102.4T switch production shipping。  
  <https://investors.broadcom.com/news-releases/news-release-details/broadcom-now-shipping-worlds-first-1024-tbps-switch-production>
- NVIDIA：Silicon Photonics networking。  
  <https://www.nvidia.com/en-us/networking/products/silicon-photonics/>
- NVIDIA：Vera Rubin rack-scale systems。  
  <https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/>
- Open CPX MSA：co-packaged optics ecosystem。  
  <https://www.opencpxmsa.org/>
- Arista：XPO / 12.8T pluggable optics 相关发布。  
  <https://www.arista.com/en/company/news/press-release/23697-pr-20260311>
- Coherent：OFC 2026 1.6T/3.2T/XPO 展示。  
  <https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026>
- Coherent：CPO technologies at OFC 2026。  
  <https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026>
- Marvell：1.6T ZR/ZR+ coherent DSP for AI interconnects。  
  <https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html>
- VIAVI：OFC 2026 observation, 1.6T mainstream and 3.2T emergence。  
  <https://blog.viavisolutions.com/2026/04/23/ofc-2026-1-6t-going-mainstream-the-emergence-of-3-2t/>
- OFC：2026 exhibition and AI-driven network demand。  
  <https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-opens-next-week-in-los-angeles-with-sold-out-exhibition-as-ai-driven-network-demand-fuels/>
- OFC：AI-era data centers and optical ecosystem。  
  <https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-exhibit-connects-the-global-optical-ecosystem-powering-ai-era-data-centers-and-networks/>
- Cignal AI：2025 光器件收入接近 250 亿美元。  
  <https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/>

### 本项目内交叉引用资料

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- `D:\drive\Investment\调研\v5\conference_update\ofc_2026_conference_update.md`
- `D:\drive\Investment\调研\v5\conference_update\OCP_EMEA_Summit_2026_高密度调研报告.md`

### 口径说明

行业报告数据之间存在口径差异：有的统计 optical component，有的统计 transceiver module，有的统计 switch/optical interconnect system，有的统计云厂内部部署价值。本文所有预测均按“AI 基础设施建设非常乐观”假设推演，并对找不到直接数据的细分环节采用大胆但可追溯的区间假设；正式投资建模时应把商用收入、内部自研价值和关联光互联市场拆开估值。
# 行业调研：【Optical Interposer与新型光引擎】

> 截至日期：2026-05-08  
> 研究范围：Optical Interposer、Photonic Interposer、Optical I/O Chiplet、CPO/NPO/CPX/XPO 光引擎、外置激光源 ELS、3.2T/400G/lane 下一代光器件、MicroLED 光互联、OCI 光计算互联、相关光纤/连接器/测试/封装供应链。  
> 口径说明：市场规模为全球 AI 数据中心相关收入池或等效收入池，产品之间存在上下游重叠，不能简单相加。利润率默认指毛利率。预测采用“基准/乐观/极度超预期乐观”三情景，且按用户要求对 2026-2027 AI 基础设施建设采用偏乐观假设。

## 0. 一页结论

Optical Interposer 与新型光引擎的投资主线要分两层看：2026 年真正放量的是“1.6T 可插拔 + 200G/lane 器件/DSP + 外置激光源 + 交换机侧 CPO/NPO/CPX 试点 + 高密光纤连接 + OCS/光路调度”；而把 optical I/O chiplet 或 photonic interposer 放进 GPU/ASIC 封装内、重构 scale-up fabric 的大规模商业化，更像 2027-2028 年的高赔率期权。

最强一手信号来自几件事：

- NVIDIA 已把 Spectrum-X/Quantum-X Photonics 放入路线，宣称 CPO 可带来 5x optical power efficiency、10x resiliency，Spectrum-X Ethernet Photonics 最高 409.6Tb/s，计划 2026H2 可用。
- Broadcom 在 OFC 2026 展示 102.4T Ethernet switch with CPO、Taurus 400G/lane optical DSP、200G/lane retimer/AEC 等，说明“交换 ASIC + DSP/SerDes + 光引擎”的平台化节奏已经明确。
- Marvell 以约 $3.25B 收购 Celestial AI，并指引 Celestial Photonic Fabric 在 FY2028 下半年开始贡献收入，Q4 FY2028 年化 run-rate 约 $500M，Q4 FY2029 约 $1B。这是 photonic fabric 从创业公司叙事进入大厂收入指引的标志。
- Lightmatter Passage M1000 已公开 114Tbps total optical bandwidth、4000mm2 photonic interposer、256 fibers、1024 SerDes；2026 又宣布 Passage CPO chiplet 与 Qualcomm 112G PAM4 optical SerDes 集成达到 1.6Tbps/fiber。
- Ayar Labs TeraPHY 公开指标为 8Tbps 双向、10ns per chiplet、UCIe package electrical interface、mm-to-km reach；它代表封装内 optical I/O chiplet 路线。
- OCI MSA 在 2026-03 成立，创始成员包括 AMD、Broadcom、Meta、Microsoft、NVIDIA、OpenAI，目标是为 AI scale-up optical connectivity 定义开放规范。
- NVIDIA 分别与 Lumentum、Coherent、Corning 签订战略合作或长期供应/产能扩张安排，说明激光器、光纤、先进光连接已经从“普通配套件”变成 AI factory 的战略约束。

本报告的投资判断：

| 方向 | 2026 投资确定性 | 2027-2028 弹性 | 毛利/ROIC 质量 | 结论 |
|---|---:|---:|---:|---|
| 1.6T pluggable、200G/lane 器件、DSP/TIA/driver | 极高 | 高 | 中高到高 | 2026 业绩主线，注意 2027 ASP 下行 |
| ELS、InP laser、SiPh PIC、400G/lane 光器件 | 高 | 很高 | 高 | 最稀缺瓶颈之一，优先级高于普通模块组装 |
| switch-side CPO/NPO/CPX 光引擎 | 中高 | 很高 | 高 | 2026 试点，2027 放量早期，胜负取决于可维护性 |
| Optical Interposer / Optical I/O Chiplet | 中低 | 极高 | 极高但不确定 | 2026 多为 NRE/样机/设计 win，2027-2028 进入真正考验 |
| OCS/光路调度 | 中 | 很高 | 高 | 若与 AI scheduler 绑定，价值按 GPU 利用率定价 |
| 高密光纤、连接器、fiber shuffle、测试 | 高 | 高 | 中高 | 被低估的“卖铲子”环节，随光纤密度爆炸放大 |
| 高端铜互联/AEC/ACC/CPC | 极高 | 中高 | 中高 | 不会被光立刻替代，2026-2027 仍是 rack 内主力 |

## 1. 定义与方法

### 1.1 本文如何定义 Optical Interposer 与新型光引擎

| 名称 | 定义 | 代表形态 | 2026 状态 |
|---|---|---|---|
| Optical Interposer / Photonic Interposer | 把光波导、调制/探测、fiber attach、SerDes/EIC 与大 ASIC/chiplet complex 在封装或近封装层集成，突破传统芯片边缘 I/O shoreline | Lightmatter Passage M1000、Celestial Photonic Fabric、POET Optical Interposer、TSMC COUPE | 样机、EVK、设计导入；少数客户 NRE |
| Optical I/O Chiplet | 作为 chiplet 放入 GPU/ASIC/交换芯片封装，承担 package-to-package 或 rack-scale 光 I/O | Ayar TeraPHY、Intel optical I/O chiplet、Ranovus ODIN、Nubis engine | 2026 仍偏 early access/lead customer |
| CPO optical engine | 光引擎与 switch ASIC 近距离共封装，减少 ASIC 到前面板的长电链路 | NVIDIA Spectrum-X/Quantum-X Photonics、Broadcom Tomahawk CPO、Coherent 6.4T socketed CPO | 2026H2 试点，2027 早期放量 |
| NPO/CPX/socketed optical engine | 更靠近 ASIC 的光引擎，但保留插座、连接器、可维护性 | Open CPX MSA、Coherent 6.4T socketed CPO、Eoptolink 6.4T NPO、GF SCALE | 比 fully sealed CPO 更可能先规模化 |
| XPO | 高密度、液冷、可插拔大 form-factor 光模块 | Arista XPO 12.8Tbps/module、204.8Tbps/OCP RU | 2026 标准/样品，2027 小批量 |
| ELS/ELSFP | 外置激光源，给 CPO/光引擎供光，把热和寿命风险从 ASIC package 中分离 | Lumentum UHP laser、Coherent ELS、Genuine Optics comb ELS | 2026 战略瓶颈，附着 CPO/NPO 增长 |
| MicroLED optical interconnect | 用 microLED+PD+multi-core fiber 替代部分短距铜/激光硅光链路 | Avicena LightBundle eKit | 2026 evaluation kit，偏 2027+ |

### 1.2 关键外部锚点

- AI 数据中心网络/光互联口径：项目内美国 AI 数据中心模型给出 2026 网络与光互联订单池，务实 $65-100B、乐观 $105-165B；2027 务实 $100-160B、乐观 $170-280B。
- AI 芯片口径：项目内 AI 芯片研究给出 2026 全球 AI 计算芯片/模块产能释放金额，基准 $300-360B、乐观 $390-470B、极度乐观 $520-650B；2027 为 $430-520B、$590-720B、$850B-$1.05T。
- 光模块/器件口径：Cignal AI 指出 2025 年 datacom optical component revenue 超 $19B，400G+ datacom modules 出货超 4200 万只；TrendForce 预计 800G+ 光模块出货占比从 2024 年 19.5% 升至 2026 年 60%+。
- CPO 行业报告口径：Mordor 估计 CPO 市场 2026 约 $164.8M、2031 约 $764M，CAGR 35.92%。本文认为该口径偏保守，未充分计入 NVIDIA/Broadcom/OCI/ELS/CPX/XPO 在 2026-2027 的 AI 订单加速。

## 2. 2026 机会、挑战与技术路径

### 2.1 2026 行业机会

| 机会 | 核心事实 | 投资含义 |
|---|---|---|
| 1.6T 从样品转向规模供货 | Cignal 口径显示 2026 年 1.6TbE modules 超 500 万只；Lumentum、Coherent、OpenLight、Broadcom、Eoptolink 均在 OFC 2026 密集发布 | 最确定收入池，不用等封装内光 I/O |
| 交换机侧 CPO 进入平台路线 | NVIDIA Spectrum-X Photonics 2026H2，Broadcom 102.4T CPO switch 与 400G/lane DSP | CPO 首先吃的是 switch ASIC 周边价值，不是 GPU package 内 NVLink |
| ELS 成为战略瓶颈 | Lumentum 1310nm UHP laser 在 25C >1W、50C >800mW；Coherent socketed CPO 配 ELS | 激光器从 commodity 转为高可靠、高毛利、长单锁定环节 |
| 光纤密度爆炸 | Coherent 提到未来 5 年 AI DC 可能使用超过 10 亿米光纤；Corning/NVIDIA 2026 合作将美国光连接产能扩 10x、光纤产能扩 50%+ | 高密 fiber shuffle、MPO/MTP/MCF/HCF、连接器、清洁/测试工具被重估 |
| Optical Interposer 进入设计窗口 | Rubin/MI400/Trainium3/TPU8/Meta MTIA/OpenAI ASIC 会定义 2027-2028 封装形态 | 2026 看 design win/NRE，不应只看当年收入 |
| OCI 标准化 | OCI MSA 创始成员覆盖 GPU、ASIC、hyperscaler 与 Broadcom/NVIDIA | 降低 optical scale-up 生态碎片化，有利于 2027-2028 多供应商导入 |

### 2.2 2026 主要挑战

| 挑战 | 为什么关键 | 乐观假设下的解决路径 |
|---|---|---|
| 可维护性 | 可插拔坏了可换；封装内光 I/O 坏了可能导致整板/整机报废 | CPO 先落在 switch，NPO/CPX/socketed engine 先于 fully sealed CPO 放量 |
| 激光源寿命和热 | 激光器与高温 ASIC 绑定会放大热漂移和维修问题 | 外置 ELS + 冗余 + 监控成为主流 |
| 光电混合测试 | 需要 wafer probe、PIC/EIC test、fiber attach、BER、眼图、温循、burn-in | Keysight/VIAVI/Anritsu/EXFO/ficonTEC 等受益，测试时间成为瓶颈 |
| 标准分裂 | OCI、UCIe、OIF、Open CPX、XPO、CMIS、OCP 等并行 | hyperscaler 事实标准先走，MSA 后续收敛 |
| 铜互联仍强 | 机架内 224G/448G copper、AEC、ACC、CPC 成本/可维护性更好 | 光只替代“铜 reach/功耗/密度失效区”，不是 2026 全面替代 |
| 先进封装资源竞争 | CoWoS/SoIC/2.5D 产能已被 GPU/HBM 挤满 | 光 chiplet 先抢高价值 ASIC/switch 封装窗口，GPU 大规模导入更晚 |
| 客户认证周期 | CSP qualification 通常 6-18 个月，且要第二来源 | 2026 锁定战略供应，2027-2028 才体现量产份额 |

### 2.3 目前正在使用的技术栈

| 层级 | 2026 正在使用/放量 | 2026-2027 新变化 |
|---|---|---|
| Rack 内最短距 | DAC/AEC/ACC、CPC/flyover、PCIe/CXL retimer、NVLink copper | 224G/448G 铜链路继续增长，但长度缩短、测试更难 |
| Scale-out 网络 | 800G OSFP/QSFP-DD、1.6T OSFP/DR4/2xDR4/FR4、LRO/TRO/LPO | 1.6T 从 early volume 转向主流，400G/lane 器件先于 3.2T 模块放量 |
| 交换机侧光引擎 | CPO、NPO、CPX/socketed engine、ELS、SiPh PIC、InP laser | 2026 pilot，2027 在 102.4T/204.8T/409.6T switch 中早期放量 |
| 光路交换 | Google Apollo OCS/MEMS optical circuit switching | TPU-like 集群先用，GPU Ethernet fabric 可能逐步吸收 |
| Scale-across DCI | 800ZR/ZR+、1600ZR/ZR+、coherent-lite、multi-rail ILA | AI campus/metro/regional 需求让 coherent DSP、line system 回到高增长 |
| 封装内/近封装光 I/O | Ayar TeraPHY、Lightmatter Passage、Celestial Photonic Fabric、TSMC COUPE、GF SCALE | 2026 NRE/样机，2027 小量，2028 若架构验证成功则高弹性 |

## 3. 与 2026-2027 出货量最大 AI 芯片的关系

> 本节沿用项目内 `ai_chip_research_2026_2027.md` 里的芯片排序与价值量假设，不重新外搜芯片出货量。

| AI 芯片/平台 | 2026-2027 状态 | 主要互联路径 | 对 Optical Interposer/新光引擎的影响 |
|---|---|---|---|
| NVIDIA B300/GB300 | 2026 最大放量高端 GPU rack | NVLink/铜 scale-up + 800G/1.6T scale-out | 2026 GPU package 内光 I/O 概率低，交换机侧 CPO/ELS 和光模块直接受益 |
| NVIDIA Rubin/Vera Rubin | 2026H2 首批，2027 主力 | NVLink 6、CX9、Spectrum-6/SPX、CPO/Photonic Ethernet | 2027 对 CPO/NPO/ELS、1.6T/3.2T、OCS 拉动最强 |
| Google TPU v7 Ironwood/TPU8 | Ironwood 2026 主力，TPU8 2027 导入 | TPU pod、Google 自有网络、Apollo OCS、800G+ optics | Google 最可能推动 OCS、定制光互联、后续 optical I/O |
| AWS Trainium2/3 | Trainium2/Rainier 2026 大量，Trainium3 接棒 | NeuronLink/EFA、自研 fabric、外部以太网/光 | 2026 先拉动光模块和交换网络，CPO 取决于 AWS 自研 switch 代际 |
| AMD MI350/MI400 Helios | MI350 2026 放量，MI400/Helios 2027 增量 | Infinity Fabric、UALink、Pollara/Vulcano NIC、AI Ethernet | AMD 参与 OCI，MI400 若顺利将推动 UALink+optics 生态 |
| Microsoft Maia 200 | Azure 推理自研导入 | Azure 后端网络、液冷 rack、潜在 OCI 标准 | 出货量不如 NVIDIA，但更容易尝试定制 optical scale-up |
| Meta MTIA 300/400/450/500 | 2026-2027 多代 ASIC、多 GW 路线 | Broadcom XPU/Ethernet/SerDes，潜在 OCI | 成本敏感，先用成熟光模块；2027 后可能导入低成本 optical I/O |
| OpenAI/Broadcom ASIC | 2026H2 起步，10GW 长周期目标 | Broadcom custom XPU、以太网/CPO/OCI 资源强 | 最值得关注的 optical chiplet 设计窗口之一 |
| Huawei Ascend 910C/950 | 中国国产替代主线 | 超节点、自研互联、国产 800G/1.6T 光模块 | 国内短期受益更多在模块、光器件、连接器、测试；封装内光 I/O 较慢 |
| Cambricon/Alibaba/Baidu 国产 ASIC | 2026-2027 扩张 | 国产以太网/自研互联、光模块、DAC/AEC | 带动国产光模块/连接器/高端铜缆，CPO/Optical Interposer 仍是后续期权 |

### 3.1 新技术成熟与放量时间表

| 技术 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观/极度超预期 |
|---|---|---|---|---|---|
| 800G pluggable | 已大规模放量，>20M units | AI cluster 超配 | 800G 与 1.6T 同时缺货 | 成熟，ASP 下行 | 总量大但价值向 1.6T 转移 |
| 1.6T pluggable | >5M units，收入 $7-10B | 6-8M units | 9-12M units，ASP 坚挺 | 12-18M units | 20-30M units，成为新增高端默认配置 |
| 400G/lane / 3.2T 器件 | 样品、alpha/beta、测试导入 | lead customer qual | 头部客户提前锁单 | 小批量/early revenue | 2027H2 形成 $10B+ 早期收入池 |
| CPO switch optical engine | 2026H2 pilot | 多个 CSP 认证 | NVIDIA/Broadcom 提前拉货 | 5-12% 高端 AI switch 端口 | 15-35% 高端 AI switch 端口 |
| NPO/CPX/socketed engine | 标准和样品 | 多供应商 qual | 作为可维护 CPO 替代路线放量 | 早期部署 | 比 fully sealed CPO 更快放量 |
| ELS/ELSFP | 与 CPO/NPO 同步导入 | laser 长单锁定 | 激光源成为瓶颈品 | 标准化和冗余成熟 | 供不应求，高毛利延续 |
| OCS | Google/TPU-like 主导 | Meta/Microsoft/AWS 试点 | GPU Ethernet fabric 部分采用 | 大型集群 5-15% | 极度情景 20%+ |
| Optical I/O chiplet | NRE、样机、小量验证 | 1-2 个 lead customer 小量 | ASIC/switch 提前导入 | 1-5% accelerator/package | 极度情景 8-12% |
| Photonic interposer | Lightmatter/Celestial 等验证 | 大客户 reference architecture | 大额 NRE/design win | 第一批规模部署 | 2028 前夜进入高赔率窗口 |
| MicroLED optical interconnect | eKit/评估 | 板级/内存 demo 增多 | 低成本短距场景试用 | 小批量 | 成为短距光 I/O 分支 |
| MCF/HCF/高密连接 | 部分项目导入 | Rubin/NVL144 布线压力推动 | 成为布线瓶颈解决方案 | 快速扩容 | 与 OCS/CPO 共同放量 |

### 3.2 2026 最可能发生的技术路径排序

1. 1.6T 可插拔和 200G/lane 生态：DSP、EML、SiPh、PD、TIA、driver、模块封装、测试。
2. LRO/TRO 等低功耗光模块路线：比极简 LPO 更容易通过系统可靠性和互通验证。
3. 交换机侧 CPO/NPO/CPX：先在 switch ASIC 周边导入，外置激光源和 socketed 形态降低维护风险。
4. OCS 与高密光纤管理：Google Apollo 证明能耗优势，AI cluster 越大越需要重构光路。
5. Optical Interposer/Optical I/O chiplet：2026 以设计 win/NRE/早期 EVK 为主，重在看客户名单而不是收入。

## 4. 已经开始放量的关键产品

### 4.1 市场规模、渗透率与利润率

| 产品 | 当前状态 | 未来 3 个月收入池 | 未来 1 年收入池 | 未来 2 年收入池 | 渗透率路径 | 毛利率三情景 |
|---|---|---:|---:|---:|---|---|
| 800G AI 光模块 | 2025-2026 主力，TrendForce 预计 800G+ 2026 份额 60%+ | B $4.5-6B / O $6-8B / X $8-10B | B $18-24B / O $25-32B / X $33-43B | B $22-30B / O $32-45B / X $48-65B | 2026 高端 AI optics 45-55%，2027 被 1.6T 分流但总量仍大 | B 25-38% / O 32-45% / X 38-48% |
| 1.6T 可插拔 | 2026 进入规模，Cignal 口径 >5M units | B $1.5-2.5B / O $2.5-3.5B / X $3.5-5B | B $7-10B / O $10-14B / X $15-22B | B $14-22B / O $25-38B / X $42-65B | 2026 高端 AI optics 15-25%，2027 30-45% | B 30-42% / O 38-48% / X 45-55% |
| 200G/lane 光器件、DSP、TIA、driver | 1.6T 核心瓶颈，Broadcom/Marvell/Coherent/Lumentum/MACOM 布局 | B $2-3.5B / O $3.5-5B / X $5-7B | B $9-14B / O $14-20B / X $21-30B | B $15-24B / O $25-38B / X $40-60B | 随 1.6T 渗透提高，2027 向 400G/lane 过渡 | B 45-60% / O 50-68% / X 60-75% |
| LPO/LRO/TRO 低功耗光模块 | 2026 部分 AI 网络导入，LRO/TRO 更现实 | B $0.5-1B / O $1-1.8B / X $1.8-3B | B $2.5-4.5B / O $4.5-7.5B / X $8-12B | B $5-9B / O $10-16B / X $18-26B | AI optics 5-10% 到 15-25% | B 25-35% / O 30-42% / X 38-50% |
| OCS/光路交换 | Google Apollo 标杆，多云厂开始评估 | B $0.1-0.2B / O $0.2-0.4B / X $0.4-0.8B | B $0.5-1.2B / O $1.2-2.5B / X $2.5-4.5B | B $1.5-3.5B / O $4-8B / X $9-15B | 大型 AI cluster 2026 <5%，2027 5-15%，X 20%+ | B 35-50% / O 40-60% / X 50-65% |
| 高端铜互联/AEC/ACC/CPC | 2026 rack 内仍主力；224G/448G 继续升级 | B $2-3.5B / O $3.5-5.5B / X $5.5-8B | B $9-14B / O $15-22B / X $23-33B | B $13-22B / O $24-36B / X $38-55B | Rack 内短距 60-80% 链路依赖铜 | AEC/ACC 25-45%；retimer/connector 40-60%；线缆装配 15-30% |
| AI DCI coherent/ZR/ZR+ | AI campus/metro/region 拉动；Marvell 1600ZR/ZR+ 2026H2 sampling | B $0.5-0.8B / O $0.8-1.2B / X $1.2-1.8B | B $2.5-4B / O $4-6.5B / X $7-10B | B $5-8B / O $9-14B / X $15-22B | AI DCI 中 800G/1.6T coherent 逐步替代低速方案 | DSP/系统 45-65%；模块 30-45% |
| 光纤/连接器/高密布线 | Corning/NVIDIA 长期合作、AI rack fiber count 上升 | B $1-2B / O $2-3B / X $3-5B | B $5-9B / O $9-14B / X $15-23B | B $9-16B / O $17-28B / X $30-45B | GB200/Rubin、OCS、CPO 均提高 fiber count | 光纤 25-45%；高密连接器/定制组件 35-55% |

### 4.2 增长预测区间

| 产品 | 基准增长 | 乐观增长 | 极度超预期增长 |
|---|---:|---:|---:|
| 800G AI 光模块 | 未来 1 年 +20-35%，未来 2 年 +10-25% | +35-55%，+25-45% | +60%+，+50%+ |
| 1.6T 可插拔 | 未来 1 年 +80-120%，未来 2 年 +80-150% | +120-180%，+150-250% | +200%+，+300%+ |
| 200G/lane 器件/DSP | +35-55%，+45-70% | +60-90%，+80-120% | +100%+，+150%+ |
| OCS | +50-100%，+100-200% | +100-200%，+200%+ | +200%+，+300%+ |
| 高端铜互联 | +25-40%，+25-45% | +40-60%，+45-65% | +70%+，+80%+ |
| 光纤/连接器 | +35-60%，+50-80% | +70-100%，+90-140% | +120%+，+150%+ |

### 4.3 目前最可能拥有高溢价的产品

1. 400G/lane optical DSP、224G/448G SerDes、coherent DSP：模拟/混合信号能力稀缺，客户认证深，毛利率 55-75%。
2. ELS 与高功率 InP CW laser：CPO/NPO/Optical I/O 共同依赖，NVIDIA/Lumentum/Coherent 合作验证其战略稀缺性，极度情景毛利率 60-75%。
3. 1.6T 头部供应商模块：2026 供不应求时可达 40%+，但 2027 多供应商扩产后有 ASP 下行风险。
4. OCS + 调度软件：若提升 GPU 利用率，定价依据不是 BOM，而是 cluster goodput。
5. CPO/NPO socket、fiber attach、光电混合测试：量未必最大，但客户失效成本极高，早期议价权好。

## 5. 在研关键产品与未来快速增长方向

| 在研/早期产品 | 代表公司 | 未来 3 个月收入池 | 未来 1 年收入池 | 未来 2 年收入池 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| 封装内 Optical I/O Chiplet | Ayar Labs、Intel、TSMC COUPE、Marvell/Celestial、Ranovus、Nubis、POET | B $20-50M / O $50-150M / X $150-300M | B $0.2-0.5B / O $0.5-1.5B / X $1.5-3B | B $1-2.5B / O $2.5-6B / X $6-12B | 2026 AI accelerator/package <1%；2027 1-5%；X 8-12% | IP/chiplet/NRE 55-75%；封装制造 25-45% |
| Photonic interposer / optical fabric | Lightmatter、Celestial/Marvell、Xscape Photonics、Ayar | B $10-30M / O $30-100M / X $100-200M | B $0.1-0.4B / O $0.4-1.2B / X $1.2-2.5B | B $0.8-2B / O $2.5-7B / X $8-15B | 先在 proprietary AI cluster 试点，2027 design win 关键 | 系统差异化强，GM 50-70%，但前期现场支持重 |
| CPO switch optical engine | NVIDIA、Broadcom、Coherent、Lumentum、Ciena、Eoptolink、GF | B $50-150M / O $150-400M / X $400M-1B | B $0.3-0.8B / O $0.8-2.5B / X $3-8B | B $1.5-4B / O $5-15B / X $20-45B | 高端 AI switch 2026 <5%，2027 B 5-12%、O 15-25%、X 35%+ | B 35-45% / O 45-60% / X 60-75% |
| NPO/CPX/socketed engine | Open CPX、Coherent、Eoptolink、GF SCALE、Ciena Vesta、Molex/Samtec | B <$100M / O $100-300M / X $300-800M | B $0.2-0.7B / O $0.7-2B / X $2-6B | B $1-3B / O $4-12B / X $12-30B | 可维护性强于 fully sealed CPO，2027 更可能多供应商放量 | GM 35-60%，极度情景 55-70% |
| ELS/ELSFP | Lumentum、Coherent、Broadcom、MACOM、三菱、住友、OpenLight、Genuine Optics | B $100-300M / O $300-600M / X $600M-1B | B $0.5-1.2B / O $1.2-3B / X $3-7B | B $2-5B / O $5-12B / X $12-25B | CPO/NPO/Optical I/O attach 接近 100% | 45-65%，缺货时 60-75% |
| 3.2T/400G-per-lane | Broadcom Taurus、OpenLight 3.2T DR8 PIC、Coherent 400G/lane、Lumentum、Marvell | B <$50M / O $50-150M / X $150-300M | B $0.2-1B / O $1-3B / X $3-8B | B $3-10B / O $10-25B / X $25-55B | 2026 sample，2027H2 early revenue，2028 规模化 | DSP/器件 50-75%；模块早期受良率和测试压制 |
| XPO 12.8T 液冷可插拔 | Arista、Marvell、Eoptolink、Linktel、Molex/Samtec/US Conec | B <$100M / O $100-200M / X $200-500M | B $0.1-0.5B / O $0.5-1.5B / X $1.5-4B | B $1-4B / O $4-12B / X $12-25B | 2027 高端 switch <5%，若 CPO 维护困难则更快 | 35-55%，极度 55-65% |
| MicroLED optical interconnect | Avicena、Fabric.AI/Kopin、OCI MicroLED 生态 | B <$10M / O $10-30M / X $30-80M | B $50-200M / O $200-600M / X $600M-1.2B | B $0.5-1.5B / O $1.5-4B / X $4-8B | 先切短距、低成本、laser-free 场景 | 早期 45-65%，成熟后下行 |
| MCF/HCF、高密光纤/connector | Corning、OFS、Sumitomo、Fujikura、Furukawa、Prysmian、YOFC、Hengtong、Senko | B $50-150M / O $150-300M / X $300-600M | B $0.5-1.2B / O $1.2-2.5B / X $2.5-5B | B $2-5B / O $5-10B / X $10-18B | Rubin/OCS/CPO 布线密度驱动，2027 起加速 | 标准光纤中等，定制高密组件 35-55% |
| TFLN/聚合物调制器 | HyperLight、Liobate、Lightium、Polariton、Lumiphase、Lightwave Logic | B <$10M / O $10-30M / X $30-80M | B $50-200M / O $200-500M / X $500M-1B | B $0.3-1B / O $1-2.5B / X $2.5-6B | 400G/lane 和 2028+ 低功耗调制器候选 | IP/器件 GM 高，量产良率和封装风险高 |

### 5.1 在研方向的关键判断

- Optical Interposer 的价值不只是“把电变成光”，而是重新定义 scale-up domain。Lightmatter/Celestial 这类方案如果能让几百到几千颗 XPU 进入同一低时延域，价值捕获会按 GPU 利用率和训练 wall-clock time 定价。
- 2026 年看收入会低估该赛道，真正要跟踪的是：NRE、design win、OCI/CPX 标准参与度、封装平台绑定、第二来源、hyperscaler qualification。
- POET/Celestial/Marvell 的订单取消事件是重要风险提醒：光引擎设计 win 可能在客户并购、供应链重组、保密条款、技术路线切换中失效，小公司订单需要打折看。

## 6. 供给侧：产能结构、瓶颈、成本与价格传导

### 6.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/能力 | 2026 判断 |
|---|---|---|---|---|
| Switch ASIC/DSP/SerDes | 美国设计、台韩代工 | Broadcom、NVIDIA、Marvell、Cisco/Acacia、AMD/Pensando、Intel、Credo、Alphawave、Astera Labs、MACOM | 5/4/3/2nm SerDes-rich SoC、102.4T/204.8T switch、224G/448G PHY、coherent DSP | 价值最高，客户认证深 |
| SiPh PIC/foundry | 美国、台湾、新加坡、欧洲 | TSMC、GlobalFoundries/AMF、Intel Foundry、Tower、Samsung、imec、AIM Photonics、OpenLight、Ligentec | SOI SiPh、MZM/ring/EAM、Ge PD、III-V integration、PDK | wafer 不是唯一瓶颈，良率/耦合/测试更关键 |
| InP laser/EML/PD | 美国、日本、欧洲、中国 | Lumentum、Coherent、Broadcom、MACOM、三菱、住友、Fujitsu Optical、Sivers、OpenLight、Accelink | DFB/CW laser、EML/EAM、PD、UHP laser、ELS | 战略瓶颈，被 NVIDIA 长单锁定 |
| 光模块/光引擎组装 | 中国、泰国、马来西亚、越南、美国 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、AOI、Fabrinet、Accelink、Hisense、Luxshare/FIT、Foxconn、Celestica、Jabil、Sanmina | 800G/1.6T OSFP/QSFP-DD、LRO/TRO/LPO、coherent pluggable、自动耦合、burn-in | 800G/1.6T 最直接放量，但 2027 价格竞争加剧 |
| CPO/NPO/CPX 连接与封装 | 美国、台湾、中国、泰国、马来西亚 | Coherent、Lumentum、GF、Molex、Samtec、US Conec、Yamaichi、Amphenol、TE、Rosenberger、TeraHop、Fabrinet、ASE/Amkor/TSMC | socket、fiber attach、thermal path、ELS coupling、CPO substrate | socketed optics 可能先放量 |
| 光纤/连接器/布线 | 美国、日本、中国、欧洲 | Corning、OFS、Sumitomo、Fujikura、Furukawa、Prysmian、YOFC、Hengtong、ZTT、Senko、US Conec、Molex、Samtec | MCF/HCF、bend-insensitive fiber、MPO/MTP、fiber shuffle | AI rack fiber count 上升带来结构性成长 |
| 测试与自动化 | 美国、日本、德国 | Keysight、VIAVI、Anritsu、EXFO、Tektronix、Rohde & Schwarz、Spirent、ficonTEC、PI、SUSS、EVG、ASMPT、BESI、FormFactor、MPI、Teradyne、Cohu | 1.6T MAC/FEC、224G/448G SerDes、400G/lane optical、BER/jitter/thermal drift、CPO burn-in | 隐性瓶颈，设备毛利高 |

### 6.2 供给瓶颈

1. 高功率、长寿命、低噪声激光源：CPO/Optical I/O 依赖 ELS，激光源寿命、功率、温度稳定性、冗余和可替换性决定客户导入速度。
2. 光纤耦合和 active/passive alignment：微米级甚至亚微米级耦合良率决定 CPO/NPO 成本曲线。
3. 光电混合测试时间：每个 PIC/EIC/光引擎都要做 BER、眼图、温循、湿热、老化，测试时间可能成为产能上限。
4. 224G/448G SerDes 人才：模拟/混合信号团队稀缺，头部芯片公司议价权强。
5. 先进封装窗口：CoWoS/SoIC/2.5D 资源被 GPU/HBM 占满，光 chiplet 必须证明高价值才能抢封装产能。
6. 标准和互通：OCI、UCIe、Open CPX、XPO、OIF 并行；大客户要求多供应商和现场可维护，拖慢单一技术放量。
7. 现场可维护性：封装内光 I/O 失效成本远高于可插拔模块，socketed optical engine 会先获得客户信任。
8. 高密光纤管理：线缆半径、清洁、标签、弯折、连接器可靠性和安装人工都可能变成 rack 交付瓶颈。
9. 地缘和合规：高端 DSP、laser、模块组装大量跨中美日台欧供应链，关税/出口管制可能改变份额。
10. 资金和预付款：头部客户可预付锁产能，小公司若没有大客户背书，难以承受扩产、库存、RMA 和测试资本开支。

### 6.3 BOM 与单位成本拆分

| 产品 | 典型 BOM/单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 1.6T pluggable | Optical PIC/EML/laser/PD 30-40%；DSP/driver/TIA/retimer 20-30%；PCB/cage/thermal 10-15%；组装耦合 8-12%；测试/burn-in 10-15%；良率/RMA 5-10% | 200G/400G 器件、DSP 供应、良率、客户认证、ASP 下行速度 | 短缺时器件涨价可传导到模块；供给扩散后模块端先被压价 |
| CPO/NPO optical engine | PIC/光器件 25-35%；EIC/driver/TIA 20-30%；ELS/laser/fiber 15-25%；socket/substrate/thermal 10-20%；测试/服务 10-20% | 可维护性、ELS 冗余、field failure、标准接口、第二来源 | 早期按 NRE+premium ASP；若被 ASIC 厂打包，利润向平台商集中 |
| Optical I/O chiplet | PIC/EIC chiplet 25-35%；ELS 10-20%；advanced packaging/interposer 20-30%；fiber/connector 10-20%；测试/yield 15-25%；NRE/IP 5-15% | 设计绑定、封装良率、系统拓扑收益、客户是否愿意承担切换风险 | NRE + chiplet ASP + IP 授权 + 长单锁定；价值按节省的 power/latency/GPU idle 定价 |
| Photonic interposer | photonic wafer/interposer 25-35%；SerDes/EIC 20-30%；fiber attach 15-25%；封装/供电/散热 15-25%；测试 10-20% | topology 是否提升 XPU 利用率、软件栈适配、封装良率 | 若提升训练效率，按系统收益定价，非简单 BOM 加成 |
| OCS | MEMS/光学核心 30-45%；fiber array/connector 20-30%；控制电子/软件 15-25%；系统集成 10-20% | 功耗节省、重构速度、插损、端口数、调度软件绑定 | 云厂自研会压硬件价；调度软件和运维工具可高毛利 |
| 高端 AEC/ACC/CPC | 线缆/连接器 35-55%；redriver/retimer/AEC 芯片 25-45%；测试和组装 10-20% | 224G/448G 稳定性、长度、散热、客户 rack 标准 | 铜价传导有限，高端 AEC 芯片按性能溢价 |

## 7. 竞争格局与壁垒

### 7.1 市场结构

| 细分 | 头部集中度 | 竞争格局 |
|---|---|---|
| Switch ASIC/DSP/SerDes | CR3 高 | Broadcom merchant Ethernet 强，NVIDIA 绑定 GPU/NVLink/Spectrum-X，Marvell/Cisco/Acacia 分食 |
| 800G/1.6T 模块 | CR5 中高但价格竞争强 | Innolight/Eoptolink/Coherent/Lumentum/AOI/Fabrinet/Accelink/Hisense 等 |
| Laser/EML/SiPh PIC | CR5 高于模块 | Lumentum、Coherent、Broadcom、三菱、住友、OpenLight/GF 等 |
| CPO/NPO/Optical Engine | 早期，未定型 | NVIDIA/Broadcom/Coherent/Lumentum/GF/Lightmatter/Ayar/Marvell/Celestial |
| Photonic Interposer | 极早期，少数公司领先 | Lightmatter、Celestial/Marvell、POET、TSMC COUPE、GF/AMF、Xscape |
| OCS | 早期且云厂自研强 | Google Apollo 标杆；Calient、Polatis/HUBER+SUHNER、Lumentum、Coherent、Ciena/Nokia/Cisco |
| Fiber/connector | 中高 | Corning/OFS/Sumitomo/Fujikura/Furukawa/Prysmian/YOFC/Hengtong/Senko/US Conec/Molex/Samtec/Amphenol/TE |
| 测试 | 寡头 | Keysight、VIAVI、Anritsu、Tektronix、R&S、EXFO 等 |

### 7.2 可量化壁垒：为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| power/bit | pJ/bit、W/Tb、W/port | AI DC 电力是硬瓶颈，省下网络功耗可转化为更多 XPU 或更低 TCO |
| 带宽密度 | Tbps/mm、Tbps/RU、fibers/rack | rack 功率进入 600kW-1MW 后，面板、布线、冷却空间同样稀缺 |
| 可靠性 | BER、FIT、MTBF、RMA、10 年寿命 | AI 训练停机成本极高，客户愿为低故障率付溢价 |
| 认证周期 | CSP qual 6-18 个月 | 通过 AVL 后订单粘性强，新供应商替换成本高 |
| 系统拓扑绑定 | NVLink、Spectrum-X、UALink、OCI、OCS scheduler | 客户买的不是器件，而是可用 GPU 小时和训练效率 |
| 先进封装 | CoWoS/SoIC/COUPE/fiber attach 良率 | 良率领先者拥有成本、交期和客户信任优势 |
| 激光器和材料 | InP wafer、CW laser、EML、TFLN、MCF/HCF | 供应有限且验证长，长期合同和产能锁定支持溢价 |
| 第二来源能力 | 多 foundry、多封装、多模块厂互通 | 大客户要求供应安全，能提供开放生态者更容易进入主供应链 |

### 7.3 价值捕获判断

长期最可能拥有高 ROIC/高毛利的是：

1. Switch ASIC + fabric 软件平台：Broadcom/NVIDIA/Marvell/Cisco 最可能把 optical engine 纳入系统级定价，毛利 55-75%。
2. 高速 DSP/SerDes/coherent DSP：技术迭代快、认证深、客户绑定强。
3. Laser/ELS/SiPh/400G-lane 器件：CPO、NPO、Optical I/O 共同瓶颈，供应受限时毛利可极高。
4. Optical Interposer/Photonic Fabric IP：一旦证明提升 XPU 利用率和降低 wall-clock time，价值按系统收益捕获。
5. 高速测试和高密连接：小而高毛利，复杂度随 1.6T/3.2T/CPO 上升。
6. 普通可插拔模块：2026-2027 收入弹性强，但长期 ASP 下行和多厂竞争会压 ROIC。

## 8. 2026 关键变化：3 个拐点

### 拐点 1：1.6T 从“展示品”进入“量产前台”

OFC 2026 的共同信号是 1.6T 已从路线图进入供货窗口。Cignal 的 >5M units 口径、Coherent/Lumentum/OpenLight/Broadcom/Eoptolink 的密集产品发布，说明 2026 最确定的不是封装内光 I/O，而是 200G/lane 生态先赚钱。

### 拐点 2：CPO/NPO 从概念转为交换机侧产品路线

NVIDIA Spectrum-X/Quantum-X Photonics、Broadcom 102.4T CPO switch、Coherent 6.4T socketed CPO、GF SCALE、Open CPX MSA 共同说明，CPO 的第一批商业化形态大概率在 switch ASIC 周边。fully sealed CPO 会慢，socketed/near-package 更快。

### 拐点 3：光纤、激光器、ELS 从配套件变成战略产能

NVIDIA-Lumentum、NVIDIA-Coherent、NVIDIA-Corning 的合作，把光器件/光纤从传统通信周期拉入 AI infrastructure 战略采购周期。2026 年若出现缺货，最强溢价可能在 laser/ELS、200G/400G 器件、测试产能和高密连接器，而不只是模块组装。

## 9. 2027 关键变化：3 个拐点

### 拐点 1：Rubin/MI400/TPU8/Trainium3/MTIA/OpenAI ASIC 同步扩大，1.6T 成为新增 AI fabric 默认配置

2027 的核心不是单个 GPU 代际，而是多条 ASIC/GPU 路线同时放量，推高端口数、radix、fiber count 和 scale-across DCI。1.6T 将从“高端可选”变成“新增 AI 集群默认选项”。

### 拐点 2：CPO/NPO/CPX 进入第一轮商业化验证

如果 socketed optical engine 能证明 field service、ELS 冗余和多供应商互通，2027 年 CPO/NPO/CPX 会从 pilot 进入早期量产，尤其是在 102.4T/204.8T switch 和高端 AI fabric 中。

### 拐点 3：Optical Interposer/Optical I/O chiplet 从 demo/NRE 进入 early revenue

Ayar、Lightmatter、Marvell/Celestial、Intel、TSMC COUPE、GF/AMF、OCI MSA 已把技术生态拼齐。2027 年关键不是“能不能做出 4Tbps/10pJ/bit demo”，而是能否通过 hyperscaler 的可靠性、运维、供应连续性和第二来源审查。

## 10. 公司雷达：按细分列出头部与潜力公司

### 10.1 Switch ASIC、DSP、SerDes、AI fabric

NVIDIA、Broadcom、Marvell、Cisco/Acacia、AMD/Pensando、Intel、Arista、Credo、Alphawave Semi、Astera Labs、MACOM、Achronix、Synopsys IP、Cadence IP、Rambus、Semtech。

### 10.2 Optical Interposer / Optical I/O Chiplet / Photonic Fabric

Lightmatter、Ayar Labs、Celestial AI/Marvell、Intel Silicon Photonics、TSMC COUPE、GlobalFoundries/AMF、POET Technologies、Xscape Photonics、Nubis Communications、Ranovus、Avicena、OpenLight、Enosemi/AMD、Eliyan、HyperLight、Lightelligence、Sivers Photonics、Teramount、Ligentec、PsiQuantum。

### 10.3 CPO/NPO/CPX/XPO 光引擎与连接

NVIDIA、Broadcom、Marvell、Coherent、Lumentum、GlobalFoundries、Ciena、Arista、Eoptolink、新易盛、Molex、Samtec、US Conec、Yamaichi、TeraHop、TE Connectivity、Amphenol、Rosenberger、Luxshare/FIT、Fabrinet、Linktel。

### 10.4 Laser、EML、PD、TIA、driver、调制器

Lumentum、Coherent、Broadcom、MACOM、Mitsubishi Electric、Sumitomo Electric、Fujitsu Optical Components、Furukawa/FITEL、OpenLight、Sivers Photonics、Accelink、Source Photonics、HyperLight、Liobate、Lightium、Polariton、Lumiphase、Lightwave Logic、Nokia Bell Labs、NTT。

### 10.5 光模块与组装

中际旭创/Innolight、新易盛/Eoptolink、Coherent、Lumentum、AOI、Fabrinet、Accelink/光迅科技、Hisense Broadband/海信宽带、Source Photonics、华工正源、剑桥科技、太辰光、天孚通信、Luxshare/FIT、Foxconn、Celestica、Jabil、Sanmina、Molex、Amphenol、TE Connectivity、Linktel、Lessengers、POET/LITEON。

### 10.6 SiPh foundry、PDK、先进封装、EDA

TSMC、GlobalFoundries/AMF、Intel Foundry、Tower Semiconductor、Samsung Foundry、imec、AIM Photonics、OpenLight、Ligentec、Synopsys、Cadence、Siemens EDA、Ansys/Lumerical、Luceda、SUSS MicroTec、EVG、BESI、ASMPT、ficonTEC、PI、ASE、Amkor、FormFactor、MPI、Teradyne、Cohu。

### 10.7 OCS、coherent DCI、光传输系统

Google Apollo、Calient、Polatis/HUBER+SUHNER、Lumentum、Coherent、iPronics、Ciena、Nokia/Infinera、Cisco/Acacia、Marvell、Fujitsu、NEC、ADVA/Adtran、Juniper/HPE。

### 10.8 光纤、连接器、布线

Corning、OFS、Prysmian、Sumitomo Electric、Fujikura、Furukawa、YOFC/长飞、Hengtong/亨通、ZTT/中天、Senko、US Conec、Molex、Samtec、Amphenol、TE Connectivity、Rosenberger、Panduit、CommScope、HUBER+SUHNER。

### 10.9 测试与量测

Keysight、VIAVI、Anritsu、Tektronix、Rohde & Schwarz、EXFO、Spirent、Advantest、Teradyne、Cohu、FormFactor、MPI、ficonTEC、PI、SUSS、EVG、ASMPT、BESI。

## 11. 投资结论与跟踪指标

2026 年不要把“Optical Interposer”当成单一概念股行情。更优框架是：

- 当年业绩层：1.6T 可插拔、200G/lane 器件、DSP/SerDes、ELS、光模块代工、高密连接/光纤、测试设备、高端铜互联。
- 架构拐点层：CPO/NPO/CPX/XPO、OCS、coherent scale-across、光纤管理。
- 远期高赔率层：Optical I/O chiplet、Photonic Interposer、OCI optical scale-up、MicroLED optical interconnect、TFLN/聚合物调制器。

最值得跟踪的 10 个指标：

1. NVIDIA Spectrum-X/Quantum-X Photonics 是否在 2026H2 按期出货，以及首批客户是谁。
2. Broadcom Taurus 400G/lane DSP 从样品到量产的节奏，以及 Tomahawk/Jericho 平台是否绑定 CPO/NPO。
3. Coherent/Lumentum 的 ELS、laser 和 1.6T/3.2T 产品是否继续出现供不应求和毛利上行。
4. Marvell/Celestial 的 FY2028 $500M run-rate 指引是否提前或上修。
5. Lightmatter Passage M1000、Ayar TeraPHY 是否从 EVK/lead customer 进入可验证量产订单。
6. OCI MSA、Open CPX、XPO 是否形成云厂可接受的多供应商规范。
7. Google Apollo OCS 是否被更多非 Google 生态复制。
8. Corning/NVIDIA 的光纤产能扩张是否引发高密连接器、MCF/HCF、fiber shuffle 订单上修。
9. POET/Celestial/Marvell 类订单变动是否继续出现，提示小公司 design win 的可兑现风险。
10. 1.6T 模块 ASP 何时开始明显下行：若 2026H2 价格战提前，普通模块 ROIC 会比器件/ELS/DSP 更先受压。

## 12. 主要资料来源

项目内资料：

- `ai_chip_research_2026_2027.md`
- `AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- `行业调研_AI网络_光互联_铜互联/行业调研_封装内光IO与Optical_Chiplet_2026-05-08.md`
- `行业调研_AI网络_光互联_铜互联/行业调研_CPO_NPO与交换侧光引擎_2026-05-08.md`
- `conference_update/ofc_2026_conference_update.md`
- `conference_update/nvidia_gtc_2026_research.md`
- `conference_update/designcon_2026_conference_update.md`
- `conference_update/OCP_EMEA_Summit_2026_高密度调研报告.md`
- `conference_update/chiplet_summit_2026_update.md`

外部一手与交叉验证来源：

- NVIDIA Silicon Photonics: https://www.nvidia.com/en-in/networking/products/silicon-photonics/
- NVIDIA CPO technical blog: https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/
- Broadcom OFC 2026: https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai
- Coherent OFC 2026 CPO: https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026
- Coherent FY2026 Q3: https://www.coherent.com/news/press-releases/third-quarter-fiscal-year-2026-results
- NVIDIA/Coherent strategic partnership: https://nvidianews.nvidia.com/_gallery/download_pdf/69a58a503d6332d72ae626b5/
- NVIDIA/Marvell NVLink Fusion partnership: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-AI-Ecosystem-Expands-as-Marvell-Joins-Forces-Through-NVLink-Fusion/default.aspx
- Lumentum NVIDIA partnership: https://investor.lumentum.com/financial-news-releases/news-details/2026/NVIDIA-Announces-Strategic-Partnership-With-Lumentum-to-Develop-State-of-the-Art-Optics-Technology/default.aspx
- Lumentum OFC 2026: https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx
- Lumentum FY2026 Q3: https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx
- NVIDIA/Corning partnership: https://investor.corning.com/news-and-events/news/news-details/2026/NVIDIA-and-Corning-Announce-Long-Term-Partnership-To-Strengthen-U-S--Manufacturing-for-AI-Infrastructure/default.aspx
- Marvell/Celestial acquisition: https://investor.marvell.com/news-events/press-releases/detail/1000/marvell-to-acquire-celestial-ai-accelerating-scale-up-connectivity-for-next-generation-data-centers
- Marvell completes Celestial AI acquisition: https://investor.marvell.com/news-events/press-releases/detail/1005/marvell-completes-acquisition-of-celestial-ai
- Lightmatter Passage M1000: https://lightmatter.co/products/m1000/
- Lightmatter 1.6Tbps/fiber 2026: https://lightmatter.co/press-release/lightmatter-achieves-record-1-6-tbps-per-fiber-to-accelerate-ai-optical-interconnect/
- Ayar Labs TeraPHY: https://ayarlabs.com/teraphy
- OCI MSA: https://oci-msa.org/
- OCI 200G optical PHY specification: https://oci-msa.org/assets/files/200G-OCI-Optical-Phy-Specification-v1.0.pdf
- Arista XPO: https://www.arista.com/company/news/press-release/23697-pr-20260311
- OpenLight 3.2T DR8 PIC: https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants
- GlobalFoundries SCALE CPO: https://investors.gf.com/news-releases/news-release-details/globalfoundries-accelerates-adoption-co-packaged-optics-advanced
- Avicena LightBundle eKit: https://avicena.tech/avicena-launches-the-worlds-first-microled-optical-interconnect-eval-kit/
- TrendForce 800G+ and Google OCS: https://www.trendforce.com/presscenter/news/20260210-12919.html
- Cignal AI datacom optical components: https://cignal.ai/2026/04/datacom-optical-component-revenue-surpasses-19b-in-2025/
- LightCounting Optics for AI: https://www.lightcounting.com/newsletter/en/january-2026-optics-for-ai-clusters-366
- Mordor CPO market: https://www.mordorintelligence.com/industry-reports/co-packaged-optics-market
- POET purchase order update: https://www.poet-technologies.com/news/poet-technologies-provides-purchase-order-update
# 行业调研：【PCIe/CXL高速I/O交换与Retimer】

> 截至时间：2026-05-08。  
> 研究口径：PCIe/CXL Switch、Retimer、Signal Conditioning Module、AEC/CopprLink、Optical-aware Retimer、CXL Memory Controller、CXL Fabric Switch、相关IP/VIP/测试认证与云端软件管理层。AI芯片路线图引用项目内已有材料 `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`，本文不重新外部搜索芯片出货排序，只用其作为需求侧背景。  
> 核心假设：对2026-2027 AI计算中心建设取非常乐观口径；对缺乏直接披露的数据使用“可解释的乐观假设”，并在表格中分为基准 / 乐观 / 极度超预期乐观三档。所有美元口径均为年度化或指定期间收入规模，不同子行业之间可能存在少量价值链重叠。

## 0. 投资结论摘要

1. **PCIe/CXL高速I/O交换与Retimer正在从“服务器外设配套”升级为“AI机柜/集群扩展层”。** 2026年，AI服务器的高带宽GPU/ASIC、NIC、SSD、CXL内存扩展、机柜内铜缆/背板互联同时提高PCIe链路长度、误码、功耗、可观测性和一致性需求，Retimer、PCIe/CXL Switch、SCM/AEC、CXL Controller的价值量显著抬升。
2. **2026最确定放量方向：PCIe Gen5/Gen6 Retimer、智能线缆/SCM/AEC、PCIe Gen6 / CXL 2.0 Switch、CXL Type-3内存扩展控制器、IP/VIP/合规测试。** 2027更大的弹性来自PCIe Gen6 AI Fabric Switch、CXL 3.x动态内存池化、Optical-aware Retimer / PCIe over optics、UALink/ESUN/以太网多协议Scale-up Retimer。
3. **价值捕获最强的是“高速连接芯片+固件/软件+客户认证”层。** Astera Labs 2026Q1收入3.084亿美元、GAAP毛利率76.3%；Credo FY2026 Q3收入4.079亿美元、GAAP毛利率65.9%。这些数字说明高端互联芯片在供不应求和设计绑定期具备高毛利。线缆/连接器规模大但长期毛利低于芯片，CXL内存模块收入大但受DRAM周期影响。
4. **AI芯片路线差异决定PCIe/CXL机会分布。** NVIDIA GB200/GB300内部Scale-up更多被NVLink/NVSwitch吸收，但仍拉动CPU-host、NIC、SSD、CXL、铜缆和光模块周边I/O；AMD MI350/MI400、AWS Trainium、Google TPU、Meta MTIA、Microsoft Maia、OpenAI/Broadcom ASIC、中国国产AI芯片更可能增加开放PCIe/CXL/UALink/以太网互联价值量。
5. **极度乐观情景下，2027该赛道可出现“Retimer/SCM 60-90亿美元、PCIe/CXL Fabric Switch 100-160亿美元、CXL控制器/交换/内存池化120-300亿美元”的组合弹性。** 关键前提是：72/128 XPU开放Scale-up域真实量产、CXL 3.x池化由PoC转产线、云厂商把内存利用率提升视为与HBM同等重要的资本效率工具。

## 1. 2026机遇、挑战与技术路径

### 1.1 需求侧背景：2026/2027十大AI芯片平台如何映射I/O需求

项目内AI芯片研究给出的2026-2027主线是：NVIDIA Blackwell/Blackwell Ultra仍是最大收入池，AWS Trainium2/3、Google TPU v7 Ironwood、AMD MI350/MI400、Meta MTIA、Microsoft Maia、华为昇腾、寒武纪、阿里自研芯片等共同扩张。对应到PCIe/CXL高速I/O：

| AI芯片/平台 | 2026-2027 I/O含义 | 对PCIe/CXL交换与Retimer的影响 |
|---|---|---|
| NVIDIA B200/GB200、B300/GB300 | GPU Scale-up核心由NVLink/NVSwitch封闭生态承担；CPU、NIC、SSD、管理面、扩展卡仍依赖PCIe；机柜内铜缆和高密服务器板级链路复杂度提升 | Retimer/SCM/AEC确定性强；PCIe/CXL Fabric Switch在NVIDIA主域内机会较少，但在周边I/O和第三方系统中有机会 |
| AWS Trainium2/3 | 自研ASIC集群，EFA/NeuronLink体系，追求低成本大规模部署 | 开放Scale-out/Scale-up互联、PCIe管理面、CXL内存扩展、机柜内线缆均受益；供应商认证价值高 |
| Google TPU v7 Ironwood | 自研TPU Pod，内部网络和软件栈强绑定 | 外部可见份额有限，但大规模Pod对Retimer、线缆、测试、SerDes IP有间接拉动 |
| AMD MI350/MI400 Helios | 更开放的XPU生态，预计更积极使用标准互联和商用部件 | PCIe Gen6 Switch、CXL、UALink、Retimer的弹性高于封闭NVLink域 |
| Meta MTIA、Microsoft Maia、OpenAI/Broadcom ASIC | 2026/2027从验证转向更大规模部署 | 对多供应商互联、PCIe/CXL、CXL内存扩展、可观测性软件需求高 |
| 华为昇腾、寒武纪、阿里等中国平台 | 供应链国产化与标准化压力并存 | 国产/亚洲供应商在Retimer、PCIe Switch、连接器、测试替代上有增量，但高端SerDes和先进工艺仍是瓶颈 |

### 1.2 2026正在使用的关键技术

| 技术 | 2026状态 | 主要用途 | 投资判断 |
|---|---|---|---|
| PCIe 5.0 Retimer / Redriver / SCM | 已规模量产 | GPU/CPU/NIC/SSD链路延长，板级损耗补偿 | 现金流最确定，价格逐步竞争但AI高端仍有溢价 |
| PCIe 6.0 Retimer | 2026进入AI服务器设计导入和早期出货 | 64GT/s PAM4、FLIT/FEC链路，下一代CPU/GPU/NIC/SSD | 2026H2-2027H1是放量窗口 |
| PCIe Gen6 Switch / Fabric Switch | 2026从通用Switch升级到AI Fabric/Scale-up Switch | 多GPU/多ASIC、NIC、SSD、CXL设备扇出和集合通信辅助 | 2027弹性最大，毛利率可接近高端Retimer |
| CXL 2.0 Type-3 Memory / Controller | 2026已有云端私有预览和客户出货 | 内存扩展、内存分层、容量型AI推理/数据库 | 2026是验证年，2027是规模年 |
| CXL 3.0/3.1 Switch / Pooling | 2026采样/设计导入 | Rack-level内存池化、动态容量分配 | 软件栈成熟速度决定放量 |
| CopprLink / AEC / SCM | 2026快速上量 | 机柜内1-2米高损耗铜缆、背板替代、GPU托盘连接 | 单位价值低于芯片，但数量弹性极大 |
| Optical-aware Retimer / PCIe over optics | 2026标准和验证升温 | 机柜间/长距离PCIe透明扩展 | 2027小规模，2028后更大 |
| UALink / ESUN / 多协议Scale-up Retimer | 2026产品发布与设计导入 | 开放XPU Scale-up互联，PCIe/CXL协议栈复用 | 非NVIDIA AI ASIC生态的重要期权 |

### 1.3 新技术成熟与放量时间表

| 技术/产品 | 2026成熟度 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---:|---|---|---|
| PCIe 5.0 Retimer/SCM | 量产成熟 | 2026继续高增长，2027增速放缓 | AI服务器高配化使2027仍增长30%+ | PCIe 5长尾叠加中国替代，2027仍供需紧张 |
| PCIe 6.0 Retimer | 早期量产/客户认证 | 2026H2小批量，2027H1规模 | 2026Q3进入头部AI平台BOM，2027放量 | 2026H2成为高端AI服务器默认配置 |
| PCIe Gen6 / CXL Fabric Switch | 采样与首批出货 | 2027规模收入 | 2026H2已有多客户部署，2027爆发 | 开放72 XPU机柜提前量产，2026Q4收入陡增 |
| CXL 2.0 Controller/Type-3 Memory | 已有生产/云预览 | 2026验证，2027批量 | 2026H2云实例GA，2027成为容量型AI推理标配 | 内存利用率压力触发超大规模采购，2026就显著放量 |
| CXL 3.x Dynamic Pooling/Switch | 采样/软件验证 | 2027H2试点，2028放量 | 2027H1头部云厂商产线部署 | 2026Q4-2027Q1进入新建AI园区标准设计 |
| Optical-aware Retimer | 标准/验证 | 2027试点，2028收入 | 2027多客户小批量 | 2027因机柜间互联瓶颈提前商用 |
| PCIe 7.0/8.0 IP与Retimer | PCIe 7规格完成，PCIe 8 Draft 0.5 | 2027-2028 IP收入，2029芯片 | 2027高端SerDes IP/NRE显著增长 | 头部ASIC提前锁定供应商，2026-2027即产生大量NRE |

## 2. 已经开始放量的关键产品：规模、渗透率与利润率

### 2.1 当前放量产品清单

| 细分 | 代表产品/公司 | 第一手信号 |
|---|---|---|
| PCIe/CXL Retimer | Astera Aries、Broadcom BCM85667/85668、Microchip XpressConnect、Marvell、Kandou、Parade、Montage等 | Broadcom发布端到端Gen6 PCIe组合，含Gen6 Switch、Retimer与IP；Astera 2026Q1收入同比高增 |
| PCIe/CXL Switch / AI Fabric Switch | Astera Scorpio P/X、Broadcom PEX89000、Marvell Structera S、Microchip Switchtec、Montage、XConn/Marvell | Astera称Scorpio X 320-lane AI Scale-up Switch已出货并预计H2扩大；Marvell Structera S 30260为260-lane CXL 3.0 Switch，预计2026Q3采样 |
| SCM/AEC/CopprLink | Credo HiWire/AEC、Amphenol、Molex、TE、Samtec、Luxshare、Foxconn FIT、BizLink等 | Credo FY2026 Q3收入4.079亿美元，同比+134.5%，并强调1.6T/3.2T AEC团队 |
| CXL Memory Controller / Type-3 Module | Astera Leo、Micron CZ120/CZ122、Samsung CMM-D、Marvell Structera X/A、Montage、Microchip | Astera Leo用于Microsoft Azure M-series私有预览；Micron CZ120已量产出货、CZ122提供资格样品 |
| IP/VIP/Compliance/Test | Synopsys、Cadence、Siemens EDA/Avery、Rambus、Keysight、Teledyne LeCroy、Tektronix、Anritsu、GRL、UNH-IOL、Allion | PCIe 6/7、CXL 3/4和Optical-aware Retimer提高验证矩阵复杂度 |

### 2.2 市场规模与渗透率预测

| 产品 | 未来3个月市场规模 | 未来一年市场规模 | 未来两年市场规模 | 渗透率路径 | 利润率预测 |
|---|---:|---:|---:|---|---|
| PCIe 5/6 Retimer与Signal Conditioning芯片 | 基准3.5-5.5亿美元；乐观5.5-7.5亿美元；极度8-11亿美元 | 基准16-24亿美元；乐观22-32亿美元；极度30-45亿美元 | 基准22-32亿美元；乐观35-55亿美元；极度60-90亿美元 | 高端AI服务器PCIe链路渗透率2026约35-55%，2027达55-75%，极度情景80%+ | 基准GAAP毛利65-74%；乐观70-77%；极度74-80% |
| PCIe/CXL Switch与AI Fabric Switch | 基准2.5-4.5亿美元；乐观4-7亿美元；极度7-10亿美元 | 基准14-26亿美元；乐观25-45亿美元；极度45-70亿美元 | 基准30-55亿美元；乐观60-110亿美元；极度100-160亿美元 | 通用PCIe Switch已成熟；AI Scale-up/Fabric Switch渗透率2026 <10%，2027基准15-25%、乐观30-45%、极度50%+ | 基准60-72%；乐观68-76%；极度72-80% |
| AEC/SCM/CopprLink与高端铜缆 | 基准3.5-6.5亿美元；乐观6-9亿美元；极度9-13亿美元 | 基准16-28亿美元；乐观25-42亿美元；极度40-65亿美元 | 基准30-55亿美元；乐观55-95亿美元；极度90-140亿美元 | AI机柜内1-2米高损耗链路渗透率2026约25-40%，2027约40-65%，极度75%+ | 芯片型AEC/SCM 45-65%；线缆模组25-45%；连接器20-40% |
| CXL Controller与Type-3内存扩展 | 基准5-9亿美元；乐观8-14亿美元；极度14-22亿美元 | 基准25-45亿美元；乐观45-80亿美元；极度80-120亿美元 | 基准55-100亿美元；乐观100-180亿美元；极度180-300亿美元 | 2026主要是内存容量敏感型云实例/数据库/推理；AI服务器渗透率基准2-5%、乐观5-10%、极度15%+；2027基准8-15%、极度30%+ | Controller 60-76%；Memory Module 35-60%；若DRAM紧张且客户刚需，短期可达60-70% |
| PCIe/CXL IP/VIP与合规测试 | 基准1-2亿美元；乐观2-3亿美元；极度3-5亿美元 | 基准6-11亿美元；乐观10-18亿美元；极度18-30亿美元 | 基准10-20亿美元；乐观20-35亿美元；极度35-60亿美元 | 每一代PCIe/CXL升级都要验证；渗透率接近100%，但按项目/NRE确认收入 | 软件/IP毛利80-90%；设备/实验室45-70% |

### 2.3 已放量产品的关键判断

1. **Retimer是2026最强确定性单品。** AI服务器链路越来越长、PCB层数和损耗越来越高，PCIe 6.0从NRZ转PAM4后，均衡、FEC、链路训练、误码调试复杂度大幅提升，Retimer不只是“放大器”，而是带固件、遥测和兼容性数据库的系统级部件。
2. **Fabric Switch是2027最大弹性品类。** PCIe Switch历史上用于扇出；AI时代的Fabric Switch会增加集合通信、组播、隔离、可观测性和CXL语义，单芯片Lane数从几十条向260/320 lane级别提升，价值量非线性增加。
3. **CXL从“技术正确”走向“商业压力正确”。** 当HBM和DDR5都昂贵、AI推理KV cache/数据库/向量检索需要大容量内存时，云厂商会更愿意接受10-15%的远端访问性能折损，以换取更高的内存利用率和更低的闲置资本。

## 3. 在研关键产品与未来快速增长方向

| 在研/早期产品 | 2026状态 | 未来3个月 | 未来一年 | 未来两年 | 渗透率与利润率 |
|---|---|---:|---:|---:|---|
| Optical-aware Retimer / PCIe over optics | PCI-SIG已将Optical Aware Retimer作为ECN方向，DevCon 2026议程集中讨论光电Retimer验证 | 产品收入<0.5亿美元，验证/测试/NRE 1-3亿美元 | 基准2-8亿美元；乐观8-15亿美元；极度15-30亿美元 | 基准10-25亿美元；乐观25-50亿美元；极度50-90亿美元 | 2027渗透率仍低，主要用于机柜间/长距PCIe；毛利35-60%，若Retimer+固件闭环可达60%+ |
| CXL 3.x Dynamic Pooling / DCD / MLD | Marvell Structera S 30260预计2026Q3采样；软件栈仍在成熟 | 收入以NRE/样品为主，<1亿美元 | 基准5-15亿美元；乐观15-35亿美元；极度35-70亿美元 | 基准20-60亿美元；乐观60-120亿美元；极度120-220亿美元 | 2027是关键年；芯片毛利60-76%，Fabric管理软件可提升长期ROIC |
| UALink/ESUN/以太网多协议Scale-up Retimer | Credo发布224G多协议AI Scale-up Retimer，支持UALink、ESUN、Ethernet，host侧支持64GT/s PCIe/CXL | 样品/NRE 0.5-1.5亿美元 | 基准3-10亿美元；乐观10-25亿美元；极度25-50亿美元 | 基准15-45亿美元；乐观45-90亿美元；极度90-160亿美元 | 非NVIDIA开放XPU生态若起量，渗透率从个位数快速提升；毛利65-80% |
| In-network Compute / Hypercast Fabric Switch | Astera Scorpio X强调集合通信加速和In-Network Compute | 0.5-2亿美元 | 基准5-15亿美元；乐观15-35亿美元；极度35-70亿美元 | 基准20-70亿美元；乐观70-140亿美元；极度140-250亿美元 | 适合72/128 XPU开放域；若进入云厂商标准拓扑，毛利70-80% |
| PCIe 7.0/8.0 Retimer、SerDes IP、新连接器 | PCIe 7.0规格已发布；PCIe 8.0 Draft 0.5于2026-05-01发布，目标256GT/s、x16双向1TB/s、2028完成 | IP/NRE 0.5-1.5亿美元 | 基准2-6亿美元；乐观6-12亿美元；极度12-25亿美元 | 基准8-20亿美元；乐观20-45亿美元；极度45-80亿美元 | 硅片收入多在2028后；IP/VIP毛利80-90%，早期设计绑定价值高 |
| CXL-PNM/NDP、混合DRAM+NAND CXL内存 | 三星CMM-H、内存侧计算、近内存处理仍偏试点 | <0.5亿美元 | 基准1-5亿美元；乐观5-12亿美元；极度12-25亿美元 | 基准5-30亿美元；乐观30-70亿美元；极度70-140亿美元 | 取决于软件生态和应用改造；高壁垒产品毛利55-75% |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司/工艺 | 供给特征 |
|---|---|---|---|
| 高速Retimer/Switch芯片 | 美国设计，台积电/三星代工，马来西亚/台湾/中国大陆封测 | Astera、Broadcom、Marvell、Microchip、Credo、Kandou、Montage、Parade等；5/4/3nm和先进SerDes工艺 | 设计能力和客户认证比晶圆产能更稀缺 |
| SerDes/IP/VIP | 美国、以色列、欧洲、印度、中国台湾 | Synopsys、Cadence、Siemens EDA/Avery、Rambus、Alphawave等 | 毛利高、规模小、提前2-3年锁定 |
| CXL内存模块 | 韩国、美国、日本、中国台湾/大陆 | Samsung、Micron、SK hynix、SMART Modular、Netlist、Kioxia/Solidigm等 | 受DDR5/DRAM供需周期影响最大 |
| 高速铜缆/连接器/AEC | 美国、日本、中国大陆/台湾、东南亚、墨西哥 | Amphenol、Molex、TE、Samtec、Credo、Luxshare、Foxconn FIT、BizLink、Bel Fuse等 | 产能扩张较快，但认证和一致性良率限制短期供应 |
| 测试认证设备/实验室 | 美国、欧洲、中国台湾/大陆 | Keysight、Teledyne LeCroy、Tektronix、Anritsu、GRL、UNH-IOL、Allion、Advantest、Teradyne、FormFactor | 标准升级时供给紧，客户排队验证 |

### 4.2 关键供给瓶颈

1. **64/128/224G SerDes模拟混合信号人才稀缺。** PCIe Gen6的64GT/s PAM4、Gen7的128GT/s、Scale-up的224G链路都要求高速模拟、DSP、封装、电源完整性协同设计，人才不可快速复制。
2. **合规认证和互操作矩阵爆炸。** CPU、GPU/XPU、NIC、SSD、CXL内存、Switch、Retimer、线缆、BIOS、Linux内核、Kubernetes插件都可能形成组合问题，客户认证周期常见6-18个月。
3. **先进工艺和大Die NRE压力。** 260/320 lane级Switch和高端Retimer需要先进节点、大量SerDes PHY和复杂验证，掩膜、EDA、验证平台投入高，失败一次代价巨大。
4. **高速封装、PCB、连接器和线缆损耗预算紧。** 机柜内1-2米铜缆在64G/112G/224G速率下接近物理极限，连接器一致性、弯折半径、插损、回损、散热都影响良率。
5. **固件、遥测和现场调试能力不足。** AI数据中心要求可观测、可隔离、可热更新。没有软件闭环的Retimer/Switch难以进入头部云厂商标准BOM。
6. **CXL软件栈成熟度瓶颈。** 内存池化不仅是硬件问题，还需要OS内存管理、NUMA策略、Kubernetes NRI、Fabric Manager、RAS、安全隔离和计费系统。
7. **DRAM/HBM/DDR5资源挤压。** CXL内存扩展的核心BOM是DDR5，若HBM和服务器DDR5持续紧张，CXL模块供给也会被DRAM分配限制。
8. **功耗和散热。** Retimer、Switch、AEC在机柜内数量极大，单颗几瓦到几十瓦的差异会累积成机柜级电力/散热约束。

### 4.3 成本与毛利拆分

| 产品 | 典型成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| Retimer/SCM芯片 | 晶圆Die 25-40%；封装测试15-25%；IP/NRE摊销10-20%；固件/支持5-10%；渠道/库存5-10% | SerDes性能、客户认证数量、故障率、遥测软件、供货稳定性 | 头部AI平台设计锁定后，供应商议价强；第二供应商成熟后价格下行 |
| PCIe/CXL Fabric Switch | 大Die/先进封装35-50%；SerDes/IP/验证10-20%；固件/管理软件10-15%；板级电源散热5-10% | Lane数、延迟、组播/集合通信能力、CXL一致性、可管理性 | 2026-2027供给稀缺时可高溢价；长期由Broadcom/Marvell/Astera等多强竞争压缩 |
| AEC/高速铜缆 | Twinax/铜材/连接器30-45%；主动芯片20-35%；组装测试15-25%；认证5-10% | 线长、良率、功耗、弯折可靠性、客户现场退货率 | 铜价/连接器价格可部分传导；云厂商量大压价，差异化AEC芯片可保毛利 |
| CXL内存模块 | DRAM 60-80%；Controller 8-18%；PCB/EDSFF/电源5-12%；测试/固件5-10% | DDR5价格、容量密度、带宽/延迟、RHEL/Windows/Linux认证、云端实例售价 | DRAM紧张时售价上行；云厂商若把CXL作为省DRAM工具，会接受较高控制器溢价 |
| IP/VIP/测试 | 人力研发和验证资产为主，硬件设备折旧 | 标准代际领先、覆盖协议深度、客户项目绑定 | 新标准早期定价强，后期随工具普及平滑下降 |

## 5. 竞争格局、壁垒与价值捕获

### 5.1 市场结构

| 细分 | 竞争格局 | 2026-2027变化 |
|---|---|---|
| PCIe Switch | 历史上Broadcom/PLX、Microchip/Switchtec强；Astera和Marvell在AI Fabric/CXL切入 | 从通用PCIe扇出转向AI Scale-up、CXL内存语义和软件管理 |
| Retimer/SCM | Astera在云AI PCIe/CXL Retimer品牌最强；Broadcom、Marvell、Microchip、Credo、Kandou、Parade、Montage等竞争 | Gen6/Gen7和多协议Scale-up提高门槛，头部集中度可能提升 |
| CXL Controller/Switch | Astera Leo、Marvell Structera、Montage、Microchip、三星/美光模块生态 | 2026是客户验证，2027谁拥有云端软件和互操作矩阵谁胜出 |
| AEC/线缆/连接器 | Credo在AEC芯片/线缆方案强；Amphenol/Molex/TE/Samtec/Luxshare/Foxconn FIT等制造强 | 量增快但价格竞争更快，靠认证、良率和交付保利润 |
| IP/VIP/测试 | Synopsys/Cadence/Siemens/Rambus/Keysight/LeCroy等寡头 | 标准升级带来持续NRE和工具升级收入 |

### 5.2 可量化壁垒：为什么能定价

1. **速率壁垒：** PCIe Gen6 64GT/s PAM4、Gen7 128GT/s、PCIe 8.0目标256GT/s，误码、抖动、FEC和延迟预算极小。能在真实机柜内稳定工作的供应商数量远少于PPT供应商。
2. **Lane数壁垒：** 260/320 lane级Switch需要数百个高速SerDes同时稳定工作，功耗、散热、封装和固件复杂度远高于普通PCIe Switch。
3. **互操作壁垒：** 一个Retimer/Switch要与Intel/AMD/NVIDIA/Arm CPU、不同GPU/ASIC、NIC、SSD、CXL内存、线缆、BIOS和OS互通。兼容性数据库本身就是资产。
4. **认证周期壁垒：** AI服务器平台生命周期18-36个月，一旦进入BOM和线缆拓扑，替换会触发重测、重做SI/PI、重跑可靠性，切换成本高。
5. **软件壁垒：** 头部客户不只买芯片，还买链路遥测、故障定位、热插拔、固件更新、机柜级管理和可观测性。软件越深，毛利越稳。
6. **规模交付壁垒：** 高速互联的现场故障可能造成整柜降级，云厂商愿意为低RMA、快FAE响应和稳定供货付费。
7. **标准参与壁垒：** PCI-SIG、CXL、UALink、OCP等组织的早期参与可提前影响规格并锁定生态伙伴。

### 5.3 长期高ROIC层级

| 排名 | 价值链层级 | ROIC/毛利判断 | 原因 |
|---:|---|---|---|
| 1 | Retimer / Fabric Switch / CXL Controller芯片+固件软件 | 最高，毛利60-80% | 技术壁垒高、客户锁定强、软件和认证形成复利 |
| 2 | IP/VIP/验证工具 | 毛利最高但TAM较小，80-90% | 标准代际升级驱动，几乎每家芯片/系统公司都需要 |
| 3 | CXL内存模块与池化系统 | 收入大，毛利中高且周期性强 | DRAM占BOM大头，软件化后可提升毛利 |
| 4 | AEC/SCM/高端连接器 | 收入弹性高，毛利中等 | 量很大但制造竞争激烈；主动芯片方案更优 |
| 5 | ODM/系统集成 | 毛利较低但战略地位高 | 负责整柜调试和交付，议价受云厂商压制 |

## 6. 2026关键变化：行业拐点与最可能放量子方向

1. **PCIe Gen6从“规范/验证”进入AI服务器BOM。** Broadcom已经发布端到端Gen6 PCIe组合，Microchip XpressConnect Gen6/CXL Retimer家族进入市场教育，Astera与头部云厂商收入说明PCIe/CXL连接芯片已进入高景气周期。
2. **AI Fabric Switch开始从PCIe Switch分化。** Astera Scorpio X强调320 lane、集合通信和In-Network Compute；Marvell认为72 XPU Scale-up域是2026/2027 AI互联核心方向，并展望2027 128 XPU、2028 256 XPU。2026最可能放量的是“开放AI ASIC/AMD生态的PCIe Gen6 Fabric Switch”。
3. **CXL 2.0从实验室进入云端私有预览/生产出货。** Astera Leo进入Microsoft Azure M-series私有预览，美光CZ120量产、CZ122提供资格样品，说明CXL已进入真实客户验证期。2026最可能兑现的是Type-3容量扩展，不是完全动态池化。

## 7. 2027关键变化：行业拐点与最可能放量子方向

1. **Gen6 Fabric Switch规模化，72/128 XPU开放Scale-up域成为主战场。** 若AMD MI400、Trainium3、Meta MTIA、Maia 200、OpenAI/Broadcom ASIC出货兑现，开放互联会给PCIe/CXL/UALink相关芯片创造比2026更大的增量。
2. **CXL 3.x Rack-level Memory Pooling进入生产。** 2027的关键不是“能不能插上CXL内存”，而是云厂商能否把内存池化纳入Kubernetes、计费、故障隔离和资源调度。如果可以，CXL Switch、Controller、Fabric Manager会从硬件销售变成平台能力。
3. **铜缆极限推动Optical-aware Retimer和PCIe over optics试点放量。** 机柜功耗、散热、线缆密度和1-2米铜缆损耗会把部分链路推向线性光学/DSP光学/Retimer-based optics。2027更可能是小批量高ASP，2028后决定是否成为主流。

## 8. 头部公司与潜在受益公司清单

### 8.1 标准与生态

PCI-SIG、CXL Consortium、UALink Consortium、OCP、DMTF、JEDEC、Linux Kernel社区、Red Hat、Kubernetes生态。

### 8.2 PCIe/CXL Switch与AI Fabric Switch

Broadcom/PLX、Astera Labs、Marvell/XConn、Microchip/Switchtec、Montage Technology、Rambus（IP/Controller）、Synopsys、Cadence、Siemens EDA/Avery、Alphawave Semi、UnifabriX、H3 Platform、Liqid、GigaIO、NVIDIA（NVSwitch为封闭竞争路径）、AMD/Pensando。

### 8.3 Retimer、Redriver、Signal Conditioning与多协议Scale-up Retimer

Astera Labs（Aries）、Broadcom（BCM85667/85668）、Marvell、Microchip（XpressConnect）、Credo（224G多协议Scale-up Retimer、HiWire/AEC）、Kandou、Parade Technologies、Diodes/Pericom、MaxLinear、Renesas/IDT、Texas Instruments、Montage Technology、Rambus、Synopsys、Cadence、Alphawave Semi。

### 8.4 CXL Memory Controller、CXL内存模块与池化系统

Astera Labs（Leo）、Marvell（Structera X/A/S）、Montage Technology、Microchip、ScaleFlux、Samsung（CMM-D/CMM-H）、Micron（CZ120/CZ122）、SK hynix、SMART Modular、Netlist、Kioxia、Solidigm、UnifabriX、MemVerge、H3 Platform、Liqid、GigaIO、Dell、HPE、Lenovo、Supermicro、Gigabyte、AIC。

### 8.5 AEC、CopprLink、高速铜缆与连接器

Credo、Amphenol、Molex、TE Connectivity、Samtec、Luxshare Precision、Foxconn FIT、BizLink、Bel Fuse、Huber+Suhner、Leoni、Broadcom、Astera、Credo、Semtech（光/信号链相关）、Marvell（DSP/互联相关）。

### 8.6 IP、EDA、测试认证与设备

Synopsys、Cadence、Siemens EDA/Avery、Rambus、Alphawave Semi、Keysight、Teledyne LeCroy、Tektronix、Anritsu、Granite River Labs、UNH-IOL、Allion、Advantest、Teradyne、FormFactor。

### 8.7 需求侧与系统集成

Intel、AMD、NVIDIA Grace、Ampere、Fujitsu、Microsoft Azure、AWS、Google Cloud、Meta、Oracle Cloud、CoreWeave、xAI、OpenAI、Anthropic、Dell、HPE、Lenovo、Supermicro、Quanta、Wiwynn、Inventec、Foxconn、Gigabyte、AIC。

### 8.8 中国与亚洲替代观察名单

Montage Technology、Luxshare Precision、Foxconn FIT、BizLink、Parade Technologies、ASMedia（消费/企业PCIe控制器经验，需观察高端AI服务器切入）、Unimicron/欣兴与高速PCB供应链、深南电路/沪电股份等高速板供应商、立讯/富士康/纬创/广达/英业达/纬颖等服务器与线缆/整机链条。中国本土高端PCIe Gen6/Gen7 Retimer和260/320 lane Switch仍存在SerDes、IP、先进工艺和客户认证缺口，但国产AI集群建设会给替代供应商提供验证机会。

## 9. 风险与反证指标

1. **NVIDIA封闭生态继续扩大份额。** 若2026/2027新增AI资本开支绝大部分进入GB300/Rubin NVLink生态，开放PCIe/CXL Fabric Switch弹性会被推迟，但Retimer、SCM、AEC和周边I/O仍受益。
2. **CXL软件栈成熟慢于硬件。** 如果云厂商无法在调度、隔离、计费和故障处理上闭环，CXL 3.x池化收入会从2027推迟到2028。
3. **PCIe Gen6功耗/成本过高导致平台延后。** 若客户继续用Gen5加并行链路过渡，Gen6 Retimer和Switch放量节奏会放缓。
4. **供给快速增加导致价格压力。** Retimer和AEC若出现多家供应商通过认证，毛利可能从70%+回落到55-65%。
5. **光互联替代路径变化。** 若CPO、线性光学或以太网Scale-up更快成熟，PCIe over optics的形态和价值分配可能变化。

## 10. 信息来源与交叉验证

### 公司公告与第一手材料

- Astera Labs 2026Q1业绩：收入3.084亿美元，GAAP毛利率76.3%，Q2收入指引3.35-3.45亿美元；管理层称处于重要增长周期早期。[Astera Labs Q1 2026 Results](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results)
- Astera Labs 2025全年业绩：2025收入8.525亿美元，同比+115%，GAAP毛利率75.7%，产品包括Aries、Taurus、Leo、Scorpio。[Astera Labs FY2025 Results](https://asteralabs.gcs-web.com/news-releases/news-release-details/astera-labs-reports-fourth-quarter-and-full-year-2025-financial)
- Astera Leo CXL用于Microsoft Azure M-series私有预览，单控制器最高2TB，服务器内存容量可提升超过1.5倍。[Astera Leo on Microsoft Azure](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-leo-cxl-smart-memory-controllers-microsoft-azure-m)
- Credo FY2026 Q3业绩：收入4.079亿美元，同比+134.5%，GAAP毛利率65.9%，并上调FY2026展望至约10.5亿美元。[Credo FY2026 Q3 SEC Exhibit](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm)
- Credo发布224G多协议AI Scale-up Retimer，支持UALink、ESUN、Ethernet，host侧支持64GT/s PCIe/CXL。[Credo 224G Multiprotocol AI Scale-up Retimer](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Introduces-Industrys-First-224G-Multiprotocol-AI-Scale-Up-Retimer-Supporting-UALink-ESUN-and-Ethernet/default.aspx)
- Broadcom发布端到端Gen6 PCIe产品组合，包括PEX89000 Gen6 Switch、BCM85667/BCM85668 Gen6 Retimer，并支持CXL 3.1生态。[Broadcom Gen6 PCIe Portfolio](https://investors.broadcom.com/news-releases/news-release-details/broadcom-extends-pcie-industry-leadership-end-end-gen-6)
- Marvell Structera S CXL Switch：30260为260-lane CXL 3.0 Switch，聚合带宽最高4TB/s，预计2026Q3采样；20256 CXL 2.0 Switch已生产。[Marvell Structera S](https://investor.marvell.com/news-events/press-releases/detail/1017/marvell-launches-next-generation-cxl-switch-enabling-memory-pooling-to-break-through-the-ai-memory-wall)
- Marvell PCIe Scale-up Fabric观点：72 XPU是2026/2027关键规模，2027可能到128 XPU，2028到256 XPU；Gen6 260-lane Switch可支持72+ XPU方向。[Marvell PCIe Scale-up Fabrics for AI](https://www.marvell.com/blogs/the-next-step-for-pcie-scale-up-fabrics-for-ai.html)
- Marvell Structera X/A互操作：与AMD EPYC、Intel Xeon以及Micron/Samsung/SK hynix DDR4/DDR5验证。[Marvell Structera Interoperability](https://www.marvell.com/company/newsroom/marvell-extends-cxl-ecosystem-leadership-with-structera-interoperability-across-platforms.html)
- Micron CZ120已量产出货，CZ122提供资格样品；容量128GB/256GB，约37GB/s带宽，PCIe 5.0 x8、CXL 2.0，并获RHEL 9.3认证。[Micron CZ122 and Red Hat Certification](https://www.micron.com/about/blog/applications/data-center/introducing-micron-cz122-and-red-hat-certification-of-memory-expansion-portfolio)
- Microchip XpressConnect PCIe Gen6/CXL Retimer家族资料：支持PCIe Gen6 64GT/s与CXL 3.1/2.0/1.1，覆盖16/8/4/2/1 lane。[Microchip XpressConnect PDF](https://www.microchip.com/content/dam/mchp/documents/DCS/ProductDocuments/Brochures/XpressConnect-PCIe-Gen-6-and-CXL-Retimer-Family-DS00006433.pdf)

### 标准、会议与行业技术材料

- PCI-SIG 2026-05-01发布PCIe 8.0 Draft 0.5，目标256GT/s、x16双向1TB/s、2028完成。[PCIe 8.0 Draft 0.5](https://pcisig.com/blog/pcier-80-specification-draft-05-now-available-track-2560-gts-transfer-speeds-2028)
- PCI-SIG DevCon 2026议程覆盖PCIe 6.x/7.0、CEM、Cable、PCIe 8.0技术面板、AI基础设施面板、PCIe 7 over optics、光/电Retimer验证、AEC vs DSP Optics vs LPO。[PCI-SIG DevCon 2026 Agenda](https://pcisig.com/pci-sig-developers-conference-2026-agenda)
- PCI-SIG Optical Aware Retimer ECN页面。[PCI-SIG Optical Aware Retimer](https://pcisig.com/PCIExpress/ECN/Base/OpticalAwareRetimer)
- CXL 4.0规格：带宽较3.x翻倍至128GT/s，零新增延迟、Memory RAS、Bundled Ports、向后兼容，基于PCIe 7.0。[CXL 4.0 Specification Release](https://www.businesswire.com/news/home/20251118275848/en/CXL-Consortium-Releases-the-Compute-Express-Link-4.0-Specification-Increasing-Speed-and-Bandwidth)

### 项目内材料

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\conference_update\pci_sig_devcon_2026_update.md`
- `D:\drive\Investment\调研\v5\conference_update\cxl_vertical_optimization_2026.md`
- `D:\drive\Investment\调研\v5\conference_update\designcon_2026_conference_update.md`
- `D:\drive\Investment\调研\v5\conference_update\ofc_2026_conference_update.md`
- `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_CXL内存扩展与内存池化_2026.md`
# 行业调研：【封装内光I/O与Optical Chiplet】

> 截至日期：2026-05-08  
> 研究口径：本文把“封装内光 I/O / Optical Chiplet”放在 AI 数据中心互联全栈里看，覆盖 GPU/ASIC 封装内光 I/O、交换芯片侧 CPO、外置激光源 ELS、硅光 PIC/EIC、光电共封装连接器、OCS、1.6T/3.2T 光模块、高端铜互联和相关供应链。  
> 情景定义：基准 = AI CapEx 高增长但主要沿既有架构扩张；乐观 = 1.6T、CPO、OCS 认证顺利且 hyperscaler 提前锁产能；极度超预期乐观 = 2026-2027 年 GPU/ASIC 供给、数据中心电力与网络同时放大，客户愿意为了功耗/密度/时延提前导入更激进光互联。

## 0. 一页投资结论

封装内光 I/O 与 Optical Chiplet 的投资判断不能孤立看。2026 年 AI 计算中心最确定的放量仍在“高端铜互联 + 800G/1.6T 可插拔光模块 + 交换机侧 CPO/ELS + OCS/光纤管理”，真正把光 I/O 放进 GPU/ASIC 封装内的大规模出货大概率在 2027 以后。也就是说，2026 年最强业绩弹性来自已经出货的 800G/1.6T 光模块、200G/lane 光电器件、InP/硅光、测试封装、OCS、线缆和连接器；Optical Chiplet 是 2027-2028 年的高赔率期权。

本文对 AI 数据中心光互联收入池的极乐观假设如下：2026 年 AI 光互联相关产品收入池约 350-450 亿美元基准、450-600 亿美元乐观、650-800 亿美元极度超预期；2027 年约 500-750 亿美元基准、800-1100 亿美元乐观、1200-1600 亿美元极度超预期。其中“封装内光 I/O/Optical Chiplet 本体”2026 年仍以样机、NRE、小批量验证为主，收入可能只有 2-5 亿美元基准、5-15 亿美元乐观、15-30 亿美元极度超预期；到 2027 年有望达到 10-25 亿美元基准、25-60 亿美元乐观、60-120 亿美元极度超预期。

2026 年最可能兑现的路径排序：

1. 1.6T 可插拔光模块、200G/lane EML/SiPh/VCSEL/PD/DSP、LPO/LRO/TRO 等围绕现有交换架构的升级。
2. NVIDIA、Broadcom 等交换芯片侧 CPO/CPO-like 方案，外置激光源、光引擎、CPX/XPO 形态先在网络交换层导入。
3. OCS、空分/波分/多芯光纤、低损连接器解决 AI 集群里的“光纤爆炸”。
4. 封装内光 I/O/Optical Chiplet 在少数 hyperscaler ASIC、AI switch、memory fabric 和 photonic interposer 项目中设计导入。
5. GPU package 内全面光 I/O 不是 2026 主菜。Blackwell/Blackwell Ultra/Rubin、MI350/MI400、Trainium、TPU、Maia、MTIA 的 2026-2027 主体仍是封装内电互联 + 机架内铜 + scale-out 光。

## 1. 2026 AI 计算中心建设下的机遇、挑战与技术路径

### 1.1 第一手信号：2026 不是概念年，而是客户开始锁路线的年份

| 来源/公司 | 关键信息 | 对行业的含义 |
|---|---:|---|
| NVIDIA GTC 2026 / silicon photonics | Spectrum-X/Quantum-X silicon photonics CPO switch 标称 5x optical power efficiency、10x resiliency、3.5x system power efficiency，交换容量到约 100Tb/s；本地 GTC 材料显示 Spectrum-X Ethernet Photonics 计划 2026H2，最高 409.6Tb/s 级系统形态 | CPO 先在交换机侧放量，而不是先替代 GPU 封装内 NVLink |
| Broadcom OFC 2026 | 展示 200G/channel optical interconnect、3.2Tbps CPO module、400G/lane optical DSP、200G/400G EML/PD 组合 | Broadcom 的技术路线是“DSP/SerDes/交换 ASIC + CPO 光引擎 + 高速光器件”平台化 |
| Marvell 收购 Celestial AI | 约 32.5 亿美元对价收购 Celestial AI，Photonic Fabric 面向 scale-up optical interconnect；Marvell 指引 Q4 FY2028 年化收入 >5 亿美元、Q4 FY2029 >10 亿美元 | 光互联 Chiplet 已经从 VC 叙事进入大型芯片公司并购和收入指引 |
| Ayar Labs | TeraPHY Optical I/O Chiplet：双向 4Tbps、<5ns latency、<10pJ/bit、BER <1e-15、reach up to 2km、支持 2D/2.5D/3D 封装、UCIe-ready；Series E 超 5 亿美元、估值超 38 亿美元；与 Wiwynn 合作 rack-scale AI CPO | 最接近“封装内光 I/O 商品化”的独立公司之一，但 2026 仍偏设计导入和早期量产验证 |
| Intel optical I/O chiplet | Intel 2024 年展示 fully integrated optical I/O chiplet，64 channels x 32Gbps，双向 4Tbps，reach up to 100m，DWDM silicon photonics + CMOS EIC | 大厂证明路线可行，但从 demo 到云客户量产仍需要可靠性、封装、供应链认证 |
| Lightmatter Passage/L200 | 公开材料显示单 fiber 双向 1.6Tbps、每芯片 114Tbps bisection、每 fiber bundle 450Tbps；Chiplet Summit 材料中 M1000 photonic interposer 示例为 1024 SerDes、256 fibers、64 chiplets | Photonic interposer 不是简单“光模块替换”，而是可能重构 scale-up topology |
| TSMC COUPE | 通过 SoIC-X 集成 EIC/PIC，并与 CoWoS/SoIC 结合，目标是低时延、低功耗、高带宽光互联；TrendForce 称 TSMC/Broadcom 指向 2026 CPO 量产目标 | Foundry/advanced packaging 开始把硅光纳入先进封装平台，而不是外部模块 |
| Coherent/Lumentum/Corning 与 NVIDIA | 2025 年 NVIDIA 分别对 Coherent、Lumentum 战略投资 5 亿美元；Coherent 提到未来 5 年 AI 数据中心可能使用超过 10 亿米光纤，短距链路占 AI 数据中心光纤需求 70%+；2026-05-07 NVIDIA 与 Corning 宣布长期合作，强化美国 AI 光纤制造 | 上游光器件、激光器、光纤已被 AI 服务器厂商当成战略资源 |
| OCI MSA | 成员包括 AMD、Ayar、Celestial AI、Google、Intel、Lightmatter、Meta、Microsoft、NVIDIA、TSMC 等；OFC 2026 发布 optical link L1/L2 interoperability 与 form factor / MicroLED Interconnect draft specs | 封装内/近封装光 I/O 标准化启动，降低 2027-2028 年生态碎片化风险 |

### 1.2 2026 的机会

AI 数据中心从“几千卡训练集群”进入“十万卡到百万卡 AI factory”后，网络不再只是成本项，而是决定 GPU 利用率的生产设备。2026 年美国 AI 数据中心建设在本地项目口径下可达约 4000-4900 亿美元务实情景、5400-6500 亿美元乐观情景；四大美国 hyperscaler 资本开支约 7000 亿美元量级，Top 9 CSP 合计约 8300 亿美元。网络/光互联若按 CapEx 的 7-14% 估算，2026 年就是数百亿美元级增量市场。

主要机会来自五条线：

1. 800G/1.6T 放量：Cignal 指出 2025 年 optical communication component revenue 近 250 亿美元，其中 datacom 超 180 亿美元；400G+ datacom modules 约 4200 万只，2026 年 800G 预计超过 2000 万只、1.6T 超 500 万只。TrendForce 预计 800G+ 光模块占比从 2024 年 19.5% 提升到 2026 年 60%+。
2. Switch-side CPO：NVIDIA、Broadcom、Marvell、Coherent 等不再只讲 demo，而是把 CPO 放入 102.4T/204.8T/409.6T 交换平台路线。
3. OCS/光路调度：Google Apollo OCS 公开数据约 100W 对比传统交换机约 3000W，功耗降幅约 95%；AI 训练网络的长尾流量和局部重构需求会让 OCS 从研究项目变成数据中心架构件。
4. 光纤密度爆炸：本地 OCP EMEA 2026 材料显示，H200 约 320 fibers/rack，GB200/NVL72 约 1440 strands，Rubin/NVL144 可能约 2880 strands；多芯光纤可把 6912-fiber cable 直径从约 37mm 降到 13mm、横截面积从约 1075mm² 降到 133mm²。
5. 封装内光 I/O 进入设计窗口：2026 年 Rubin、MI400、Trainium3、TPU v7/v8、OpenAI/Broadcom ASIC、Meta MTIA、Microsoft Maia 200 等项目会决定 2027-2028 的封装和系统形态。

### 1.3 2026 的挑战

| 挑战 | 为什么关键 | 乐观假设下的解决路径 |
|---|---|---|
| 封装可靠性 | GPU/ASIC 封装内光 I/O 一旦失效，维修成本远高于换光模块 | 先从 switch-side CPO、socketed optical engine、ELS 冗余开始，GPU package 内光 I/O 推迟到 2027+ |
| 激光源与热管理 | 激光器不适合与高温大芯片完全绑定；ELS 光功率、冗余、fiber management 复杂 | 外置激光源成为主流，Lumentum/Coherent/Broadcom/MACOM/三菱/住友等受益 |
| 测试与良率 | PIC/EIC/封装/光纤 attach 都要测试，且需要 burn-in、BER、温循、湿热认证 | 自动化光电测试、known-good optical engine、socketed CPX/XPO 降低系统报废风险 |
| 标准未完全收敛 | UCIe、OCI、CPX、XPO、OIF、Open Compute 方案并存 | Hyperscaler 会先以事实标准推动，MSA 解决多供应商准入 |
| 与铜互联竞争 | 机架内 224G/448G copper、AEC/ACC/flyover/coplanar cable 成本更低、可维修性更好 | 光只吃掉铜的功耗/距离/密度失效区；铜在机架内继续增长 |
| 产能与认证周期 | SiPh foundry、InP laser、COUPE/SoIC/CoWoS、fiber attach、客户认证均可能卡住 | 2026 先锁战略供应，2027 再批量爬坡 |

### 1.4 2026-2027 出货量最大 AI 芯片背景下的技术路径

项目中已有 AI 芯片研究显示，2026 年 AI 计算芯片/模组价值量可达 3000-3600 亿美元基准、3900-4700 亿美元乐观、5200-6500 亿美元极度乐观；2027 年可达 4300-5200 亿美元基准、5900-7200 亿美元乐观、8500 亿-1.05 万亿美元极度乐观。出货量最大的 10 类平台技术路线判断如下：

| AI 芯片/平台 | 2026 主技术路径 | 对封装内光 I/O 的含义 | 2027-2028 判断 |
|---|---|---|---|
| NVIDIA B300/GB300 | GPU/HBM CoWoS；NVLink/NVLink Switch 机架内高端铜；scale-out 800G/1.6T optics | 2026 GPU package 内光 I/O 概率低，交换侧 CPO 概率高 | Rubin/NVL144 后，CPO/OCS/光纤密度先受益；GPU 光 I/O 需等下一代封装窗口 |
| NVIDIA B200/GB200 | NVL72 scale-up 铜 + InfiniBand/Ethernet scale-out 光 | 已安装基础决定 2026 光模块需求 | 升级到 Rubin 时拉动 1.6T/3.2T、OCS |
| NVIDIA Rubin/Vera Rubin | 2026H2 起量；NVLink 6，rack 级带宽显著提升 | 对低功耗短距互联压力最大，但首批仍以电/铜/可插拔为主 | 2027 是 optical chiplet 进入下一轮设计的关键节点 |
| Google TPU v7 Ironwood | TPU pod + Google 自有网络；大量 800G+ optics；Apollo OCS | Google 是 OCS、定制光互联最积极客户之一 | TPU v8/后续 ASIC 可能较早采用 optical I/O/photonic fabric |
| AWS Trainium2/3 | NeuronLink/EFA；自研 ASIC + 外部以太网/光 | 2026 重点仍是光模块与网络交换 | 2027 若 Trainium3 集群规模扩大，CPO/OCS 优先于 GPU 封装光 I/O |
| AMD MI350/MI400 Helios | Infinity Fabric/UALink 方向；机架内铜，scale-out optics | AMD 参与 OCI MSA，长期开放光 I/O 生态 | MI400/Helios 2027 或推动 UALink + optics 标准化 |
| Microsoft Maia 200 | 自研 ASIC + 云内网络 | 2026 出货不及 NVIDIA，但有自定义封装窗口 | 可能成为 optical I/O early adopter，取决于 Azure AI cluster topology |
| Meta MTIA | 推理/推荐场景，成本敏感 | 更可能先用成熟光模块/以太网 | 2027-2028 在推理内存/scale-out 上采用低成本光 I/O |
| OpenAI/Broadcom ASIC | Broadcom 网络/SerDes/DSP/CPO 资源强 | 最值得关注的 optical chiplet 早期设计窗口之一 | 若 2027 大规模落地，Broadcom CPO/硅光价值捕获很高 |
| 华为昇腾 910C/950、寒武纪等中国平台 | 国产封装/网络/光模块；高端光器件国产替代 | 国内短期以 800G/1.6T 光模块、硅光、CPO 交换侧为主 | 封装内光 I/O 受 EDA/设备/光器件供应限制，节奏可能慢于美国 hyperscaler |

### 1.5 新技术成熟与放量时间表

| 技术 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观/极度超预期 |
|---|---|---|---|---|---|
| 800G 可插拔 | 已大规模放量，20M+ units 口径可信 | CSP 继续超配 | 价格坚挺，缺货溢价 | 成熟、ASP 下行 | 向 1.6T 切换但总量继续大 |
| 1.6T 可插拔 | 5M+ units，收入约 70-100 亿美元 | 6-8M units | 9-12M units，ASP 维持高位 | 主流高端 | 1.6T 成为 AI spine/leaf 常规配置 |
| 3.2T/400G/lane | 样品/验证 | 少量客户评估 | 头部客户提前锁单 | 认证和小批量 | 2027H2 开始实质放量 |
| Switch-side CPO | 2026H2 试点/小量 | 头部客户认证 | NVIDIA/Broadcom 平台提前拉货 | 放量早期 | 204.8T/409.6T 交换推动数十亿美元收入池 |
| ELS | 与 CPO/Optical engine 一起导入 | 战略供应锁定 | 激光器成为瓶颈品 | 标准化和冗余成熟 | 高毛利，供应紧缺 |
| OCS | Google 等继续扩容 | 多家 CSP 复制 | 成为大型 AI cluster 标配 | 进入规模采购 | 与 AI 调度软件深度绑定 |
| 封装内 optical I/O chiplet | 样机、NRE、小批量 | 1-2 个 lead customer 小量 | 少数 ASIC/AI switch 提前导入 | 设计导入+早期量产 | 进入部分 hyperscaler ASIC/photonic interposer |
| Photonic interposer | 以 Lightmatter 等 lead customer 验证为主 | 32K+ accelerator topology demo | 大额订单签署 | 第一批规模部署 | 若软件/topology 验证成功，2028 前夜放量 |
| MicroLED optical interconnect | eval kit/低成本短距验证 | 内存/板级 demo 增多 | 边缘 AI/推理场景试用 | 小批量 | 成为低成本短距光 I/O 分支 |
| 多芯光纤/高密连接 | 部分项目导入 | GB200/Rubin 机房压强推动 | 成为布线瓶颈解决方案 | 快速扩容 | 与 OCS/CPO 共同放量 |

## 2. 已开始放量的关键产品：市场规模、渗透率与利润率

### 2.1 当前已经在放量的产品

| 产品/技术 | 当前状态 | 未来 3 个月收入池 | 未来 1 年收入池 | 未来 2 年收入池 | 渗透率路径 | 毛利率/利润率判断 |
|---|---|---:|---:|---:|---|---|
| 800G AI 光模块 | 2025-2026 主力放量产品；TrendForce 称 800G+ 2026 占比 60%+ | 基准 45-60 亿美元；乐观 60-80 亿；极度 80-100 亿 | 基准 180-240 亿；乐观 250-320 亿；极度 330-430 亿 | 基准 220-300 亿；乐观 320-450 亿；极度 480-650 亿 | 2026 高端 AI optics 中 45-55%，2027 被 1.6T 分流但数量继续大 | 模块厂 GM 25-38%；缺货/头部客户认证产品 35-45%；器件/激光器 40-60% |
| 1.6T 可插拔光模块 | 2026 开始规模放量；Cignal 口径 2026 >5M units | 基准 15-25 亿；乐观 25-35 亿；极度 35-50 亿 | 基准 70-100 亿；乐观 100-140 亿；极度 150-220 亿 | 基准 140-220 亿；乐观 250-380 亿；极度 420-650 亿 | 2026 高端 AI optics 15-25%，2027 30-45% | 初期 GM 30-45%；200G/lane 良率高者 45%+；2027 竞争加剧后回落 |
| 200G/lane 光器件、DSP、TIA、Driver | 800G/1.6T 的核心瓶颈件；Broadcom、Marvell、Coherent、Lumentum、MACOM 等布局 | 基准 20-35 亿；乐观 35-50 亿；极度 50-70 亿 | 基准 90-140 亿；乐观 140-200 亿；极度 210-300 亿 | 基准 150-240 亿；乐观 250-380 亿；极度 400-600 亿 | 随 1.6T 渗透提升；2027 进入 400G/lane 准备期 | DSP/高速模拟 GM 50-70%；激光/PD 40-60%；先进 EML/SiPh 供不应求时更高 |
| LPO/LRO/TRO 低功耗光模块 | 2026 在部分 AI 网络中验证并放量；仍受互通、运维、BER 约束 | 基准 5-10 亿；乐观 10-18 亿；极度 18-30 亿 | 基准 25-45 亿；乐观 45-75 亿；极度 80-120 亿 | 基准 50-90 亿；乐观 100-160 亿；极度 180-260 亿 | AI optics 中 5-10% 到 15-25% | 毛利率 25-40%；若省去 DSP 但系统调试复杂，价值向交换芯片/系统商转移 |
| OCS/光路交换 | Google Apollo 等验证；2026 多家云厂商开始认真采购 | 基准 1-2 亿；乐观 2-4 亿；极度 4-8 亿 | 基准 5-12 亿；乐观 12-25 亿；极度 25-45 亿 | 基准 15-35 亿；乐观 40-80 亿；极度 90-150 亿 | 大型 AI cluster 中 2026 <5%，2027 5-15%，极度情景 20%+ | 系统 GM 40-60%；软件/调度绑定后 ROIC 可高 |
| 高端铜互联：224G/448G、AEC/ACC、CPC/flyover | 2026 仍是 rack 内互联主力；DesignCon 2026 已展示 448G KOOLIO CPC、1.6T OSFP AEC、PCIe6 AEC | 基准 20-35 亿；乐观 35-55 亿；极度 55-80 亿 | 基准 90-140 亿；乐观 150-220 亿；极度 230-330 亿 | 基准 130-220 亿；乐观 240-360 亿；极度 380-550 亿 | rack 内短距 2026-2027 仍 60-80% 链路依赖铜 | AEC/ACC GM 25-45%；高端连接器/retimer 40-60%；线缆装配 15-30% |
| AI DCI coherent/ZR/ZR+ | AI campus、regional cluster、训练/推理分布式部署拉动；Marvell COLORZ 1600 H2 2026 sampling | 基准 5-8 亿；乐观 8-12 亿；极度 12-18 亿 | 基准 25-40 亿；乐观 40-65 亿；极度 70-100 亿 | 基准 50-80 亿；乐观 90-140 亿；极度 150-220 亿 | AI DCI 中 800G/1.6T coherent 逐步替代低速方案 | DSP/系统 GM 45-65%；模块 30-45% |
| 光纤、连接器、高密布线 | Coherent 指出未来 5 年 AI DC 光纤可能超过 10 亿米；Corning/NVIDIA 2026 合作强化美国制造 | 基准 10-20 亿；乐观 20-30 亿；极度 30-50 亿 | 基准 50-90 亿；乐观 90-140 亿；极度 150-230 亿 | 基准 90-160 亿；乐观 170-280 亿；极度 300-450 亿 | GB200/Rubin 机架密度提升带来结构性增长 | 光纤 GM 25-45%；高密连接器/定制组件 35-55%；工程交付服务较低但现金流好 |

### 2.2 2026 最可能的高利润产品

1. 高速 DSP/SerDes/retimer、400G/lane optical DSP：高技术壁垒、认证周期长、客户粘性高，毛利率可维持 55-70%。
2. ELS 与高可靠 InP laser：CPO 和 optical chiplet 都绕不开激光源，且外置激光源需要冗余、监控、寿命认证，毛利率可达 45-65%。
3. 1.6T 头部客户认证光模块：2026 供不应求时头部供应商具备溢价，GM 可达 35-45%，但 2027 后价格压力上升。
4. OCS 与网络调度软件：硬件价值不一定最大，但一旦和 AI job scheduler / topology manager 绑定，ROIC 可能比普通模块高。
5. CPO optical engine/socket/connector：2026-2027 工程壁垒高、供给稀缺，毛利率有机会 45-60%。

## 3. 在研和即将快速增长的关键产品

| 在研产品/细分技术 | 代表公司 | 未来 3 个月收入池 | 未来 1 年收入池 | 未来 2 年收入池 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| 封装内 Optical I/O Chiplet | Ayar Labs、Intel、TSMC COUPE、Marvell/Celestial、Lightmatter、AMD/Enosemi、Nubis、Ranovus、POET | 基准 0.2-0.5 亿；乐观 0.5-1.5 亿；极度 1.5-3 亿 | 基准 2-5 亿；乐观 5-15 亿；极度 15-30 亿 | 基准 10-25 亿；乐观 25-60 亿；极度 60-120 亿 | 2026 <1% AI accelerator/package；2027 1-5%；极度 8-12% | 若按 chiplet/IP/NRE 捕获，GM 55-75%；封装制造端 25-45% |
| Photonic interposer / optical fabric | Lightmatter、Celestial/Marvell、Ayar、Xscape Photonics | 基准 0.1-0.3 亿；乐观 0.3-1 亿；极度 1-2 亿 | 基准 1-4 亿；乐观 4-12 亿；极度 12-25 亿 | 基准 8-20 亿；乐观 25-70 亿；极度 80-150 亿 | 先在 proprietary AI cluster 试点；2027 若 topology 成功，渗透率快速上行 | 系统级差异化强，GM 50-70%；但前期 NRE 和现场支持重 |
| ELS 外置激光源平台 | Lumentum、Coherent、Broadcom、MACOM、三菱电机、住友电工、OpenLight、Sivers | 基准 0.5-1 亿；乐观 1-3 亿；极度 3-5 亿 | 基准 5-10 亿；乐观 10-25 亿；极度 25-45 亿 | 基准 20-45 亿；乐观 50-90 亿；极度 100-160 亿 | 与 CPO/Optical Chiplet 强绑定；2027 可能成为瓶颈件 | 供给紧缺时 GM 50-70%；长期仍高于普通模块 |
| 3.2T 光模块/400G per lane | Broadcom、Marvell、Coherent、Lumentum、Innolight、Eoptolink、Arista XPO 生态 | 基准 <0.5 亿；乐观 0.5-1.5 亿；极度 1.5-3 亿 | 基准 2-8 亿；乐观 8-20 亿；极度 20-40 亿 | 基准 25-60 亿；乐观 70-130 亿；极度 150-250 亿 | 2026 sample；2027 H2 高端网络导入；2028 可能规模化 | 初期 GM 40-55%；良率不足时头部厂商溢价明显 |
| CPX/XPO socketed optics | Open CPX MSA、Arista XPO、Ciena、Coherent、Marvell、Molex、Samtec、US Conec、Yamaichi、TeraHop | 基准 <0.2 亿；乐观 0.2-0.6 亿；极度 0.6-1.2 亿 | 基准 1-4 亿；乐观 4-12 亿；极度 12-25 亿 | 基准 10-25 亿；乐观 25-70 亿；极度 70-140 亿 | 介于 pluggable 与 fully co-packaged 之间，是 2026-2027 最现实 CPO 形态 | 连接器/插座/光引擎 GM 40-60%；系统商捕获更多架构价值 |
| MicroLED optical interconnect | Avicena、OCI MicroLED 生态 | 基准 <0.1 亿；乐观 0.1-0.3 亿；极度 0.3-0.8 亿 | 基准 0.5-2 亿；乐观 2-6 亿；极度 6-12 亿 | 基准 5-15 亿；乐观 15-40 亿；极度 40-80 亿 | 先切低成本短距、内存/板级互联；替代部分 copper/AEC | 成本潜力好，早期 GM 45-65%，成熟后下行 |
| 多芯光纤 MCF/HCF、高密光缆 | Sumitomo、Fujikura、Furukawa、Corning、OFS、YOFC、Hengtong、Prysmian | 基准 0.5-1.5 亿；乐观 1.5-3 亿；极度 3-6 亿 | 基准 5-12 亿；乐观 12-25 亿；极度 25-50 亿 | 基准 20-50 亿；乐观 50-100 亿；极度 100-180 亿 | Rubin/NVL144、OCS、CPO 布线密度推动；2027 起加速 | 标准光纤 GM 中等；定制高密组件/连接器 GM 35-55% |
| 薄膜铌酸锂 TFLN/聚合物调制器 | HyperLight、Liobate、Lightium、Polariton、Lumiphase、Nokia Bell Labs 生态 | 基准 <0.1 亿；乐观 0.1-0.3 亿；极度 0.3-0.8 亿 | 基准 0.5-2 亿；乐观 2-5 亿；极度 5-10 亿 | 基准 3-10 亿；乐观 10-25 亿；极度 25-60 亿 | 高速低功耗调制器候选；更偏 2028+ | IP/器件 GM 高，但量产良率和封装是核心风险 |

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区/公司 | 2026 判断 |
|---|---|---|
| SiPh foundry / PIC | TSMC、GlobalFoundries/AMF、Intel Foundry、Tower、Samsung、imec、AIM Photonics、OpenLight | TSMC COUPE 与 GF 收购 AMF 说明 SiPh 产能进入战略整合；2026 仍不是纯 wafer 产能瓶颈，而是良率、PDK、封装和测试瓶颈 |
| EIC/DSP/SerDes | Broadcom、Marvell、NVIDIA、AMD、Intel、Credo、Alphawave、Astera Labs、MACOM | 先进 SerDes 和 DSP 是价值最高环节之一，客户认证周期长 |
| InP laser/PD/TIA/driver | Lumentum、Coherent、Broadcom、MACOM、三菱电机、住友电工、Fujitsu Optical Components、Sivers、OpenLight | 2025-2026 NVIDIA 投资 Coherent/Lumentum 说明激光器和光器件是战略瓶颈 |
| 光模块/光引擎组装 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、Accelink、Hisense Broadband、Source Photonics、Fabrinet、Luxshare、Foxconn/FIT、Celestica、Jabil、Sanmina | 800G/1.6T 放量最直接受益；但 2027 可能出现价格竞争 |
| CPO/CPX/XPO 连接与封装 | Molex、Samtec、US Conec、Yamaichi、Amphenol、TE、Rosenberger、TeraHop、Arista XPO 生态 | socketed optics 可能成为完全 CPO 前的现实折中，连接器壁垒上升 |
| 光纤/连接器/布线 | Corning、Prysmian、OFS、Sumitomo、Fujikura、Furukawa、YOFC、Hengtong、Senko、US Conec | AI 机架光纤密度提升带来结构性成长，Corning/NVIDIA 合作强化美国本土供应 |
| 测试设备/自动化 | Keysight、VIAVI、Anritsu、EXFO、Tektronix、Rohde & Schwarz、ficonTEC、PI、SUSS、EVG、ASMPT、BESI、FormFactor、MPI、Teradyne、Cohu | 光电混合测试和 burn-in 是被低估的瓶颈，收入弹性跟随 CPO/Optical Chiplet |

### 4.2 供给瓶颈：至少 10 条

1. 高可靠激光源：CPO/Optical Chiplet 依赖 ELS，激光寿命、冗余、功率稳定性、温控都是客户认证核心。
2. Fiber attach 与 active alignment：封装内/近封装光 I/O 需要微米级对准，速度、良率和返修难度决定成本曲线。
3. 光电混合测试：每个 PIC/EIC/光引擎都要进行 BER、眼图、温循、湿热、老化、端口级诊断；测试时间可能成为产能上限。
4. 先进封装窗口：CoWoS/SoIC/EMIB/2.5D/3D 封装本来已被 HBM 和大 GPU 占满，光 chiplet 进入同一封装体系会争夺资源。
5. 热管理：GPU/ASIC 热通量上升，光引擎和激光源必须避开高温区；液冷、冷板、fiber routing 需要协同设计。
6. 标准与互通：OCI、UCIe、CPX、XPO、OIF、OCP 并行，客户不愿被单一供应商锁死，互通认证拖慢导入。
7. 现场可维护性：可插拔模块坏了可换，封装内光 I/O 坏了可能导致整板/整机报废，因此 socketed optical engine 更容易先放量。
8. 高速 PCB/连接器材料：224G/448G 铜互联要求低损耗材料、精密连接器和 retimer，铜路线本身也会挤占供应链。
9. 人才与 know-how：硅光设计、封装、光测试、系统网络拓扑跨学科人才稀缺。
10. 客户认证周期：AI 数据中心客户不会只看单点指标，会要求 MTBF、可维修、软件监控、供应连续性和第二来源。

### 4.3 成本构成与毛利决定因素

| 产品 | 典型成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 1.6T 可插拔光模块 | DSP/EIC 25-35%；光器件/激光器/PD/TIA 25-35%；PCB/cage/散热 10-15%；组装/光纤 10-18%；测试/burn-in 10-18%；质保 3-8% | 200G/lane 良率、DSP 供应、头部客户认证、交期 | 客户按端口功耗和交付确定溢价；缺货时 ASP 坚挺，供给追上后模块厂让利 |
| CPO/CPX optical engine | PIC/EIC 20-30%；ELS 15-25%；封装/基板/插座 15-25%；fiber attach 10-20%；测试 15-25%；散热/监控 5-10% | 良率、ELS 冗余、可维修性、交换 ASIC 绑定 | 价值从模块转向交换系统，系统商和核心器件商拿更多利润 |
| 封装内 Optical I/O chiplet | PIC/EIC chiplet 25-35%；ELS 10-20%；interposer/advanced packaging 20-30%；光纤/connector 10-20%；测试/yield 15-25%；NRE/IP 5-15% | 设计绑定、封装良率、系统拓扑、客户愿意承担切换风险 | 以 NRE + chiplet ASP + IP 授权 + 长单锁定为主，单价由节省的 GPU idle/power 决定 |
| OCS | MEMS/硅光/光开关核心 25-40%；控制软件 10-25%；光纤矩阵/连接器 20-35%；系统集成/测试 15-25% | 调度软件、可靠性、插损、端口数、与集群编排绑定 | 若能提升 GPU 利用率，客户按系统收益付费，而非只按硬件 BOM 砍价 |
| 高端铜 AEC/ACC/CPC | cable/connector 25-45%；retimer/linear redriver 20-40%；材料/屏蔽/散热 10-20%；组装测试 10-20% | 高速信号完整性、长度、功耗、认证 | 在 rack 内继续具备成本优势；光方案只有在功耗/密度/距离失效时替代 |

## 5. 竞争格局与可量化壁垒

### 5.1 市场结构

1. 可插拔光模块：头部集中度高。中际旭创、Eoptolink/新易盛、Coherent、Lumentum、Accelink、Hisense、Source Photonics、Fabrinet 等在 800G/1.6T 中竞争。TrendForce 口径显示 Google 2026 约 400 万 TPU 可能拉动 600 万只以上 800G+ 光模块，Innolight+Eoptolink 在 Google 800G+ 订单份额可超过 80%。
2. 高速 DSP/交换 ASIC：Broadcom、Marvell、NVIDIA、Cisco/Acacia、Intel、AMD、Credo、Alphawave 等集中度高，长期 ROIC 强。
3. CPO/Optical Chiplet：NVIDIA、Broadcom、Marvell/Celestial、Ayar、Intel、Lightmatter、TSMC、GF/AMF、Coherent、Lumentum 是核心玩家，市场仍早期，高不确定但高壁垒。
4. OCS/光交换：Google Apollo 是标杆；iPronics、Lumentum、Coherent、Polatis/HUBER+SUHNER、Calient、Ciena/Nokia/Cisco 等具备产品或系统能力。
5. 光纤/连接器：Corning、Prysmian、OFS、Sumitomo、Fujikura、Furukawa、YOFC、Hengtong、US Conec、Senko、Molex、Samtec、Amphenol、TE、Rosenberger 等。

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| 功耗/bit | pJ/bit、端口 W/Tb、系统 PUE 影响 | AI cluster 电力是硬瓶颈，节省 1W 网络功耗可能释放更多 GPU/ASIC 功耗预算 |
| 带宽密度 | Tbps/mm、Tbps/RU、fiber count/rack | Rack 进入 600kW-1MW 后，空间、冷却、布线同样稀缺 |
| 可靠性 | BER、FIT、MTBF、10 年加速寿命、可插拔/可维修性 | AI 训练停机成本极高，客户愿为低故障和可运维付溢价 |
| 认证周期 | CSP qualification 6-18 个月 | 通过认证后供应商切换成本高，形成订单粘性 |
| 系统拓扑绑定 | NVLink、Spectrum-X、UALink、Ethernet、OCS scheduler | 一旦进入 topology 和软件栈，客户不是买器件，而是买可用 GPU 小时 |
| 先进封装 | CoWoS/SoIC/EMIB/COUPE、fiber attach 良率 | 封装能力不可快速复制，良率领先者拥有成本和交期优势 |
| 激光器与材料 | InP wafer、EML、CW laser、TFLN、MCF/HCF | 材料和工艺供给有限，长期合同和产能锁定支持溢价 |
| 第二来源能力 | 多 foundry、多封装、多模块厂互通 | 大客户要求供应安全；能提供第二来源或开放生态的供应商更易进入主供应链 |

### 5.3 价值捕获排序

长期最可能拥有高 ROIC/高毛利的层级：

1. 系统级 optical fabric / photonic interposer IP：如果能证明提升 GPU 利用率、降低训练 wall-clock time，价值按系统收益计价，不按单颗器件 BOM 计价。
2. 高速 DSP/SerDes/交换 ASIC/CPO 平台：技术迭代快、客户认证深、生态绑定强，Broadcom/Marvell/NVIDIA 最具代表性。
3. ELS 与高可靠 InP/SiPh 核心光器件：CPO 与 Optical Chiplet 都必须依赖，且供给有限。
4. OCS + 网络调度软件：AI cluster 越大，重构网络越有价值，软硬结合后壁垒强。
5. 先进封装/测试/连接器：虽然制造属性较强，但良率和认证壁垒能支撑高于普通制造的毛利。
6. 普通可插拔模块：2026-2027 收入弹性极强，但长期面临 ASP 下行和多厂竞争，ROIC 取决于客户结构和器件自给率。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点 1：1.6T 从样品进入实质放量，800G+ 成为 AI 网络默认配置

OFC 2026 与 Cignal/TrendForce 的共同指向很清楚：800G 已经不是早期产品，1.6T 正在进入规模 ramp。2026 年最确定的投资主线是 200G/lane 生态，包含 DSP、EML、SiPh、PD、TIA、driver、模块封装、测试和散热。

### 拐点 2：CPO 先从交换机侧突破，而不是从 GPU 封装内突破

NVIDIA、Broadcom、Open CPX MSA、Arista XPO 的方向都说明，CPO 的第一批商业化形态会在 switch ASIC 周边。原因是交换机更适合集中光引擎、散热和维护；GPU/ASIC 封装内光 I/O 则牵涉计算芯片良率和整机维修，导入更慢。

### 拐点 3：光纤、激光器、OCS 从配套件变成战略资源

NVIDIA 对 Coherent/Lumentum 的投资和与 Corning 的合作，说明 AI 数据中心客户正在把光器件当成“产能安全”问题。2026 年除了光模块厂，激光器、光纤、连接器、OCS、测试设备都可能出现比传统周期更强的订单可见度。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点 1：Rubin/MI400/Trainium3/TPU 后续代际把 rack-scale 网络推到临界点

2027 年更大的 GPU/ASIC 集群会让电互联的功耗、距离、布线和散热压力同时上升。基准情景下，3.2T/400G lane、OCS、CPO switch 会放量；乐观情景下，少数 hyperscaler ASIC 开始把 optical I/O chiplet 放进真实生产系统。

### 拐点 2：Optical Chiplet 从 demo/NRE 进入 early revenue

Ayar、Lightmatter、Celestial/Marvell、Intel、TSMC COUPE、GF/AMF 和 OCI MSA 的组合，已经把生态拼齐。2027 年的关键不是“能不能做出 4Tbps/10pJ/bit demo”，而是能否通过 hyperscaler 的可靠性、运维、供应链和第二来源审查。

### 拐点 3：数据中心内外网络边界模糊，coherent-lite、OCS、MCF/HCF 共同放量

AI 训练从单园区走向多园区、多区域后，DCI coherent、OCS、低损光纤、高密连接器会一起增长。Ciena/Nokia/Marvell/Coherent 等 1.6T ZR/ZR+ 方案和 OCS 架构会受益，AI 网络 CapEx 不再只落在 ToR/spine 光模块。

## 8. 公司雷达：按细分领域列头部与潜力公司

### 8.1 AI 芯片、网络 ASIC 与系统平台

NVIDIA、Broadcom、Marvell、AMD、Intel、Google、AWS/Annapurna、Microsoft、Meta、OpenAI/Broadcom、Cisco/Acacia、Arista、HPE/Juniper、Ciena、Nokia、Huawei、Cambricon、Alibaba 平头哥、Biren、Moore Threads。

### 8.2 Optical I/O / Optical Chiplet / Photonic Interposer

Ayar Labs、Lightmatter、Celestial AI/Marvell、Intel Silicon Photonics、TSMC COUPE、GlobalFoundries/AMF、Avicena、Xscape Photonics、Nubis Communications、Ranovus、POET Technologies、OpenLight、DustPhotonics、TeraHop、Enosemi/AMD、Eliyan、Alphawave Semi、HyperLight、Lightelligence、PsiQuantum、Sivers Photonics。

### 8.3 CPO、CPX/XPO、光引擎与交换侧光互联

NVIDIA、Broadcom、Marvell、Coherent、Lumentum、Molex、Samtec、US Conec、Yamaichi、TeraHop、Arista、Ciena、Cisco/Acacia、Intel、Ayar、Nubis、POET、Ranovus、TE Connectivity、Amphenol、Rosenberger、Luxshare。

### 8.4 硅光 foundry、PDK、EDA 与先进封装

TSMC、GlobalFoundries、AMF、Intel Foundry、Tower Semiconductor、Samsung Foundry、imec、AIM Photonics、OpenLight、Ligentec、Synopsys、Cadence、Siemens EDA、Ansys/Lumerical、Luceda、SUSS MicroTec、EVG、BESI、ASMPT、ficonTEC、PI、FormFactor、MPI。

### 8.5 激光器、调制器、探测器、TIA/driver

Lumentum、Coherent、Broadcom、MACOM、Mitsubishi Electric、Sumitomo Electric、Fujitsu Optical Components、Furukawa/FITEL、Sivers Photonics、OpenLight、POET、HyperLight、Liobate、Lightium、Polariton、Lumiphase、Eblana Photonics、Innolume、NeoPhotonics/Lumentum。

### 8.6 光模块与代工组装

中际旭创/Innolight、新易盛/Eoptolink、Coherent、Lumentum、Accelink/光迅科技、Hisense Broadband/海信宽带、Source Photonics、AOI、Fabrinet、Luxshare/立讯精密、Foxconn/FIT、Celestica、Jabil、Sanmina、Amphenol、Molex、TE Connectivity、华工正源、剑桥科技、太辰光。

### 8.7 OCS、光交换、coherent DCI

Google Apollo、iPronics、Lumentum、Coherent、Polatis/HUBER+SUHNER、Calient、Ciena、Nokia、Cisco/Acacia、Marvell、Infinera/Nokia、Broadcom、Fujitsu、NEC。

### 8.8 光纤、连接器、布线与测试

Corning、Prysmian、OFS、Sumitomo Electric、Fujikura、Furukawa、YOFC/长飞、Hengtong/亨通、ZTT/中天、Senko、US Conec、Molex、Samtec、Amphenol、TE Connectivity、Rosenberger、Keysight、VIAVI、Anritsu、EXFO、Tektronix、Rohde & Schwarz、Teradyne、Cohu。

## 9. 情景汇总：市场规模、渗透率、毛利率

| 2026-2027 收入池 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观 | 2027 极度超预期 |
|---|---:|---:|---:|---:|---:|---:|
| AI 光互联总收入池 | 350-450 亿美元 | 450-600 亿 | 650-800 亿 | 500-750 亿 | 800-1100 亿 | 1200-1600 亿 |
| 800G/1.6T 可插拔 | 250-340 亿 | 350-460 亿 | 480-650 亿 | 360-520 亿 | 550-780 亿 | 800-1100 亿 |
| CPO/CPX/XPO/ELS | 5-15 亿 | 15-35 亿 | 35-70 亿 | 30-80 亿 | 90-180 亿 | 200-350 亿 |
| Optical Chiplet/封装内光 I/O | 2-5 亿 | 5-15 亿 | 15-30 亿 | 10-25 亿 | 25-60 亿 | 60-120 亿 |
| OCS/光交换 | 5-12 亿 | 12-25 亿 | 25-45 亿 | 15-35 亿 | 40-80 亿 | 90-150 亿 |
| 高端铜互联 | 90-140 亿 | 150-220 亿 | 230-330 亿 | 130-220 亿 | 240-360 亿 | 380-550 亿 |
| 光纤/连接器/布线 | 50-90 亿 | 90-140 亿 | 150-230 亿 | 90-160 亿 | 170-280 亿 | 300-450 亿 |

| 技术 | 2026 渗透率 | 2027 渗透率 | 2026 毛利率 | 2027 毛利率 |
|---|---|---|---|---|
| 800G/1.6T 可插拔 | 高端 AI optics 60%+；1.6T 15-25% | 1.6T 30-45%，3.2T 少量 | 25-45% | 22-40%，头部仍较高 |
| CPO/CPX/XPO | 高端交换端口 <3% 基准，极度 5-8% | 5-15%，极度 20%+ | 40-60% | 35-55% |
| Optical Chiplet | AI accelerator/package <1% | 1-5%，极度 8-12% | 55-75% IP/chiplet；制造 25-45% | 50-70% |
| OCS | 大型 AI cluster <5% | 5-15%，极度 20%+ | 40-60% | 40-60% |
| 高端铜互联 | rack 内短距 60-80% | rack 内仍 50-70% | 25-60% 取决于 retimer/connector | 22-55% |

## 10. 投资结论与跟踪指标

2026 年应把“封装内光 I/O 与 Optical Chiplet”拆成现实业绩和远期期权两层。现实业绩层看 1.6T 光模块、200G/lane 器件、DSP/SerDes、ELS、OCS、光纤连接器和高端铜；远期期权层看 Ayar、Lightmatter、Marvell/Celestial、Intel、TSMC COUPE、GF/AMF、Avicena、Xscape、Nubis、Ranovus、POET 等能否拿到 hyperscaler 真实量产项目。

最重要的跟踪指标：

1. NVIDIA Spectrum-X/Quantum-X Photonics 是否在 2026H2 真实出货，以及客户是谁。
2. Broadcom 3.2Tbps CPO module、400G/lane DSP 和 200G/400G 光器件从 demo 到订单的节奏。
3. Marvell/Celestial 的 >5 亿美元 FY2028 run-rate 指引是否提前兑现。
4. Ayar TeraPHY/SuperNova 是否从 partner demo 进入可验证的 volume shipment。
5. OCI MSA、Open CPX、Arista XPO 是否形成云厂商可接受的多供应商生态。
6. Coherent/Lumentum/Corning 与 NVIDIA 的产能扩张是否带来光器件和光纤交付紧缺。
7. Google/AWS/Microsoft/Meta/OpenAI/Broadcom ASIC 下一代设计是否公开采用 optical I/O、OCS 或 CPO。

如果 AI 基础设施建设在 2026-2027 年极度超预期，最优先受益不是单一“光 chiplet 概念股”，而是拥有真实客户认证、产能、良率和交付能力的链条：高速 DSP/SerDes、InP/ELS、1.6T/3.2T 光模块、OCS、CPO socket/connector、光纤布线、光电测试和先进封装。封装内光 I/O 一旦跨过可靠性与可维修性门槛，会从“降低互联功耗”升级为“重构 AI 计算系统边界”，那时价值捕获会明显向 chiplet IP、系统拓扑和平台型芯片公司集中。

## 11. 主要资料来源

本报告结合项目内已有材料：`ai_chip_research_2026_2027.md`、`AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`、`conference_update/ofc_2026_conference_update.md`、`conference_update/nvidia_gtc_2026_research.md`、`conference_update/designcon_2026_conference_update.md`、`conference_update/OCP_EMEA_Summit_2026_高密度调研报告.md`、`conference_update/chiplet_summit_2026_update.md`，并参考以下公开来源：

- Ayar Labs TeraPHY: https://ayarlabs.com/teraphy
- Ayar Labs and Wiwynn partnership: https://ayarlabs.com/news/ayar-labs-and-wiwynn-partner-to-bring-co-packaged-optics-to-rack-scale-ai-systems/
- QIA investment in Ayar Labs: https://www.qia.qa/en/Newsroom/Pages/QIA-Invests-in%C2%A0Ayar-Labs-to%C2%A0Advance-Next-Generation%C2%A0AI%C2%A0Infrastructure.aspx
- Intel optical I/O chiplet PDF: https://download.intel.com/newsroom/archive/2025/en-us-2024-06-26-intel-demonstrates-first-fully-integrated-optical-io-chiplet.pdf
- Lightmatter high concentration blog: https://lightmatter.co/blog/high-concentration
- Marvell to acquire Celestial AI: https://www.marvell.com/company/newsroom/marvell-technology-to-acquire-celestial-ai.html
- NVIDIA silicon photonics / CPO: https://www.nvidia.com/en-in/networking/products/silicon-photonics/
- NVIDIA Vera Rubin announcement: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx
- Broadcom OFC 2026 solutions: https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai
- TSMC 2025 technology highlights / COUPE: https://www.tsmc.com/static/abouttsmcaz/2025na/tech_highlights.htm
- GlobalFoundries to acquire AMF: https://gf.com/gf-press-release/globalfoundries-to-acquire-advanced-micro-foundry/
- Avicena microLED eval kit: https://avicena.tech/avicena-launches-the-worlds-first-microled-optical-interconnect-eval-kit/
- OCI MSA: https://oci-msa.org/
- Open CPX MSA: https://www.opencpxmsa.org/
- Coherent and NVIDIA strategic partnership: https://www.coherent.com/news/press-releases/nvidia-and-coherent-announce-strategic-partnership
- Lumentum and NVIDIA strategic partnership: https://investor.lumentum.com/news/news-details/2025/NVIDIA-and-Lumentum-Announce-Strategic-Partnership-to-Develop-Next-Generation-Optical-Technologies-for-AI-Infrastructure/default.aspx
- Corning and NVIDIA long-term partnership: https://www.corning.com/worldwide/en/about-us/news-events/news-releases/2026/05/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure.html
- TrendForce 800G/OCS market note: https://www.trendforce.com/presscenter/news/20260210-12919.html
- Cignal AI optical component revenue: https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/
- LightCounting March 2026 market update: https://www.lightcounting.com/newsletter/en/march-2026-quarterly-market-update-380
- OFC 2026 official release: https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-opens-next-week-in-los-angeles-with-sold-out-exhibition-as-ai-driven-network-demand-fuels/
- UCIe 3.0 specification note: https://www.design-reuse.com/news/202529142-ucie-consortium-introduces-3-0-specification-with-64-gt-s-performance-and-enhanced-manageability/
- Arista XPO MSA: https://www.arista.com/en/company/news/press-release/23697-pr-20260311
# 行业调研：【高速连接器、背板与结构化布线】

截至日期：2026-05-08  
研究范围：AI 计算中心内部与园区内部的高速电连接器、背板/中板/线缆背板、DAC/ACC/AEC、近 ASIC 铜互联、PCIe/CXL/CopprLink/UALink 物理连接、OSFP/QSFP-DD/OSFP-XD/XPO 等前面板连接、结构化光纤布线、MPO/MTP/SN/CS/MDC/SN-MT、高密度配线、线缆管理与相关 retimer/DSP/SerDes 芯片。  
口径说明：所有市场规模均为产业链收入或可服务市场的估算区间，单位为美元。公司自用 ASIC/Rack 的互联需求按等效外部采购价估算。对找不到直接公开口径的细分产品，按 AI rack 数量、端口数、线缆/连接器 attach rate、公开订单和上市公司收入反推，并按用户要求使用偏乐观假设。

## 0. 核心结论

**一句话：2026 年高速连接器、背板与结构化布线会从“服务器配套小件”变成 AI rack 交付的硬瓶颈之一。** GPU/HBM/CoWoS 仍是最大价值池，但 GB300、Rubin、Trainium、TPU、MI350/MI400、MTIA、Maia 等平台把单 rack 内数据移动推到 800G、1.6T、224G PAM4、PCIe 6/7、NVLink/UALink/CXL 多协议共存，铜互联和光纤布线的单位价值、认证难度、交付周期都会同步上行。

最强的一手信号：

| 信号 | 关键事实 | 对本行业的含义 |
|---|---:|---|
| NVIDIA GB300 | 官方称 GB300 NVL72 由 72 颗 Blackwell Ultra GPU、36 颗 Grace CPU 组成，单 rack NVLink 130TB/s，每 GPU 800Gb/s 网络吞吐。 | 2026 最确定的路径是液冷 NVL72 + rack 内高密铜互联 + scale-out 800G 光/铜端口。 |
| NVIDIA Vera Rubin | Vera Rubin POD 为 40 racks、1,152 Rubin GPUs、60 exaflops、10PB/s 带宽，包含 NVL72、Groq LPX、STX、Spectrum-6 SPX 硅光网络。 | 2026H2-2027 把 1.6T、CPO/CPX、224G/448G、光纤密度和机柜线缆管理提前到设计主线。 |
| Amphenol | 2026Q1 销售 $7.6B，同比 +58%，订单 $9.4B，book-to-bill 1.24，IT datacom organic growth exceptional，并完成 CommScope CCS 收购。 | 连接器龙头的订单已经反映 AI datacom 超景气，且 Amphenol 通过 CCS 补强数据中心光纤/结构化布线。 |
| TE Connectivity | FY2026Q2 销售 $4.744B，同比 +15%，订单 $5.3B，同比 +25%，管理层称 record orders 由 AI、下一代交通、电网现代化驱动。 | 高速数据、AI 服务器、电力连接同步拉动，TE 的 OSFP 224G DAC/ACC/AEC、STRADA/Sliver 等进入 AI 机架口径。 |
| Credo | FY2026Q3 收入 $407M，环比 +52%，同比 +200%+，GAAP 毛利约 68.5%，主因 AEC/hyperscaler。 | AEC 已从小众线缆变为 AI rack 内高毛利“主动互联系统”。 |
| Astera Labs | 2026Q1 收入 $308.4M，同比 +93%，Scorpio X-Series 320-lane AI fabric switch shipping，Aries/Scorpio/Leo/Taurus 覆盖 PCIe/CXL/Ethernet/NVLink Fusion。 | PCIe/CXL/retimer/fabric switch 从配套芯片变成 rack-scale AI 互联核心价值层。 |
| Broadcom OFC 2026 | 展示 3.5D XPU、102.4T CPO switch、400G/lane optical DSP、200G/lane retimer/AEC、PCIe Gen6 switch/retimer；AEC 可到 6m。 | Broadcom 把 XPU、SerDes、AEC、CPO、PCIe 打成一套 AI infrastructure portfolio，客户锁定增强。 |
| Molex | 2026-02 推 Impress co-packaged copper，224Gbps PAM4 及以上；AEC 支持 112G 到 7m、224G 到 2.5m+。 | 224G 铜互联正在从“板上走线”迁移到近 ASIC、上基板、线缆化、可维护化。 |
| Samtec | DesignCon 2026 展示 224G Si-Fly HD CPC、224G backplane、448G prototype/test assembly。 | 224G 是 2026 可设计导入，448G 已进入工程探路。 |
| Corning/Meta/NVIDIA | Meta 与 Corning 签最高 $6B 多年光纤/线缆/连接产品协议；NVIDIA 与 Corning 2026-05 宣布长期光连接制造伙伴关系。 | 结构化布线、光纤、连接器正在成为 AI capex 被提前锁定的供给瓶颈。 |

**2026 最可能放量的技术路径：**

1. `800G scale-out + 112G PAM4 OSFP/QSFP-DD + DAC/AEC/光模块并存`。800G 仍是 2026 主战场，1.6T 开始进入头部新增集群。
2. `GB300/Blackwell Ultra NVL72 内部高密铜互联 + 结构化光纤 scale-out`。Copper 在 rack 内不死，反而更高端化。
3. `PCIe Gen5/6 内部线缆化、CopprLink、MCIO/Sliver/EDSFF、retimer/smart cable attach rate 上升`。
4. `224G PAM4 OSFP/AEC/CPC/背板 connector design-in`。2026 设计导入，2027 大量贡献收入。
5. `高密度结构化光纤布线从项目工程品变成可预制、可追踪、可快速维护的产品系统`，SN-MT、MPO16/32、Base-16、颜色索引、预端接 trunk、fiber management 价值上移。

## 1. 行业机会、挑战与当前技术

### 1.1 AI 计算中心对连接的变化

传统云服务器时代，连接器和布线的核心指标是成本、标准兼容、交期。AI rack 时代，核心指标变成：每 bit 功耗、误码率、FEC latency、可维护性、线缆半径/风道/液冷干涉、拓扑可扩展性、现场可追踪、机柜预制和系统级认证。

AI 集群连接分为三层：

| 层级 | 典型距离 | 2026 主流介质 | 2027 弹性方向 | 本行业受益点 |
|---|---:|---|---|---|
| Scale-up, GPU/XPU pod 内 | cm 到 3m | NVLink/UALink/PCIe/CXL 铜互联、背板、flyover、AEC/ACC | 224G/448G CPC、光学 scale-up、OCI/MSA、CPO/CPX | 高速背板、近 ASIC 铜缆、CPC、retimer、低损耗材料 |
| Scale-out, rack 到 rack/leaf-spine | 1m 到 100m | 800G OSFP/QSFP-DD、DAC/AEC、DR/FR 光模块、结构化光纤 | 1.6T、LPO/TRO、XPO、高密 patching | OSFP 连接器/cage、AEC、光纤 trunk、配线架、SN/MPO |
| Scale-across, campus/metro | 100m 到 1,000km | 400G/800G/1.6T coherent、DCI 光纤 | 1600ZR/ZR+、OCS、multi-rail、MCF | 光纤、光缆、连接器、线缆管理、测试与运维 |

### 1.2 当前正在使用的核心技术

| 技术 | 2026 状态 | 关键产品/形态 | 投资判断 |
|---|---|---|---|
| 112G PAM4 | 成熟量产 | 400G/800G OSFP/QSFP-DD、112G backplane、800G AEC | 仍是 2026 出货主力，ASP 下行但量最大。 |
| 224G PAM4 | 设计导入到早期量产 | 1.6T OSFP DAC/ACC/AEC、224G backplane、CPC、near-ASIC cable | 2026H2 头部客户 design-in，2027 放量，利润率高。 |
| 448G electrical | 工程探路 | 448G test fixture、CPC prototype、224/448G co-packaged channel | 2026 不看收入，看样机、测试设备和材料订单。 |
| DAC | 大量使用 | 800G/1.6T 短距被动铜缆 | 成本低、功耗低，受长度限制；AI rack 内继续高 attach。 |
| ACC | 放量上升 | linear redriver copper cable | 介于 DAC 与 AEC，适合 1-2.5m，毛利高于 DAC。 |
| AEC | 已开始爆发 | retimer/DSP active electrical cable | Credo/Marvell/Broadcom/Molex/Amphenol/TE 等受益，AI rack 短距高增长。 |
| 背板/中板连接器 | 112G 量产，224G 导入 | TE STRADA、Amphenol Paladin/ZettaMAX、Molex Impel/Impress、Samtec Si-Fly | 从普通连接器变成系统架构件，认证壁垒高。 |
| Flyover/top-side/near-ASIC copper | 高端导入 | UltraPass、NearStack、Si-Fly HD、KOOLIO CPC/NPC | 绕开 PCB 损耗，是 224G/448G 的关键路径。 |
| PCIe Gen5/6 CopprLink/MCIO/Sliver | Gen5/6 放量，Gen7 准备 | 内部/外部 PCIe 铜缆、EDSFF/U.2/M.2、JBOG/JBOM | AI 服务器内部连接线缆化，带动 connector/cable/retimer。 |
| 结构化光纤布线 | 新建 AI campus 主流 | OS2/OM4/OM5、MPO/MTP、SN/CS/MDC/SN-MT、预端接 trunk、配线架 | 光模块之外最容易被低估的基础层，Corning/Meta/NVIDIA 信号很强。 |
| 高密度可管理配线 | 2026 快速产品化 | Legrand Chroma Link、Panduit/CommScope/Corning/Siemon/Senko 系统 | 人工追线成为瓶颈，颜色索引/预制化/自动文档化创造溢价。 |
| CPO/CPX/XPO | 2026 pilot/标准化 | Broadcom/NVIDIA CPO、Open CPX、Arista XPO、Molex/Samtec socket | 长期方向强，但 2026 收入仍小；先利好连接器、ELS、测试和光纤管理。 |

### 1.3 基于 2026/2027 大出货 AI 芯片的技术路径映射

项目内 `ai_chip_research_2026_2027.md` 已给出 2026-2027 出货/价值最大的 AI 芯片平台。对连接行业的映射如下：

| 芯片/平台 | 2026-2027 互联背景 | 对高速连接器/背板/布线的拉动 |
|---|---|---|
| NVIDIA B300/GB300 | 2026 主力，NVL72、72 GPU、130TB/s NVLink、800Gb/s per GPU network | rack 内 NVLink 铜互联、NVSwitch tray、OSFP 800G、结构化光纤、冷却/线缆空间管理。 |
| AWS Trainium2 | Rainier 大规模部署，64 chip UltraServer/NeuronLink，EFA scale-out | 自研机柜内互联、以太网/光纤 scale-out、定制线缆和 backplane。 |
| Google TPU v7 Ironwood | pod 规模大，Google 式 OCS/全光网络、短距高速铜 | 800G+ 光模块、光纤 trunk、OCS/fiber management、短距铜。 |
| NVIDIA B200/GB200 | 存量订单延续 | 与 GB300 类似但 112G/800G 占比更高。 |
| Huawei Ascend 910C/950 | 中国超节点，系统级互联弥补单芯片差距 | 国产高速连接器、PCB/背板、光模块、结构化布线、本土认证链。 |
| Cambricon MLU590/690 | 中国 ASIC/GPU 替代，OAM/集群 | OAM baseboard、PCIe/CXL、以太网光互联、国产连接器。 |
| AMD MI350 | 2026 AMD 最确定放量，PCIe/OAM/UBB | UBB 背板、PCIe Gen5/6、OCP/UALink 路线、OSFP 800G。 |
| AWS Trainium3 | 3nm、144 chip UltraServer | 更高密度机柜内互联、1.6T 准备、定制 backplane/cable。 |
| Meta MTIA | 2026-2027 Broadcom XPU，多 GW 路线 | OCP/ORv3、Ethernet/SerDes、结构化光纤、定制铜缆和连接器。 |
| Microsoft Maia 200 | Azure 自研推理芯片，HBM3E、液冷 | Azure 内部网络、PCIe/CXL、800G/1.6T 光纤和机柜内铜连接。 |
| NVIDIA Rubin/Vera Rubin | 2026H2 起步，2027 主力，NVL72、Spectrum-6 SPX silicon photonics | 1.6T、CPO/CPX、224G/448G、CPC、结构化光纤密度升级。 |
| AMD MI400/Helios | 2026H2 首批，2027 放量，open rack/UALink/以太网 | UALink/scale-up Ethernet、UBB/ORW 背板、1.6T 端口、开放连接生态。 |

### 1.4 新技术成熟和放量时间

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|
| 800G DAC/AEC/OSFP | 2026 已大规模放量，2027 与 1.6T 共存 | 2026 继续紧缺，AEC attach 上升 | 2026H2 因 GB300/TPU/Trainium 同时拉货，ASP 高位延续到 2027 |
| 1.6T OSFP DAC/ACC/AEC/光纤布线 | 2026 design-in/小批量，2027 主流 | 2026H2 大客户批量部署，2027 新增 AI 集群默认 | 2026 年内成为头部 AI spine/scale-out 标配，1.6T 布线和测试产能短缺 |
| 224G 背板/CPC/near-ASIC copper | 2026 样机/导入，2027 放量 | 2026H2 进入多个 hyperscaler rack design | 224G 铜互联提前成为 Rubin/Helios/ASIC 平台缺口，毛利率显著上行 |
| 448G copper/test fixtures | 2026 pathfinding，2027 小批量设计导入，2028 放量 | 2027H1 部分 proprietary AI fabric pilot | 2026H2 头部客户预标准采用，测试设备/连接器订单先爆发 |
| PCIe Gen6 CopprLink/MCIO/Sliver | 2026 高端服务器放量，2027 扩散 | AI rack 线缆化成为默认 BOM | 客户为了缩短 PCB 通道，CopprLink/AEC 先于标准周期放量 |
| PCIe 7.0/Gen7 connector | 2026 验证，2027 design-in，2028 后收入放大 | 2027 高端 AI 服务器局部采用 | 2026 已锁定关键连接器形态，供应商拿到高 ASP 前置订单 |
| UALink/scale-up Ethernet | 2026 生态验证，2027 非 NVIDIA 平台放量 | MI400/Helios/自研 ASIC 快速采用 | 2027 成为开放 XPU pod 的事实标准之一 |
| CPO/CPX/NPO/ELS | 2026 pilot/小收入，2027 部分 switch 平台采用 | 2027 高端 AI switch 批量 | 光模块功耗瓶颈提前暴露，2026H2 CPO/CPX 订单显性化 |
| XPO 12.8T liquid-cooled pluggable | 2026 标准化/样机，2027 小批量 | 2027H2 进入 204.8T switch | 成为 CPO 外的高密度主路径，2027 形成 $2B+ 市场 |
| SN-MT/VSFF/MCF 高密光纤布线 | 2026 单点采用，2027 扩散 | AI campus 预制化项目快速采用 | 光纤/管道空间成为瓶颈，MCF/VSFF 被提前纳入 RFP |

## 2. 已经开始放量的关键产品

### 2.1 已放量产品清单

| 产品 | 细分技术 | 2026 放量证据 | 主要厂商 |
|---|---|---|---|
| 800G DAC/AEC/ACC | OSFP/QSFP-DD，112G PAM4，retimer/redriver | Credo FY2026Q3 收入同比 +200%+；TE/Molex/Amphenol 均给出 800G/1.6T AEC 产品；AI rack 短距连接激增。 | Credo、Amphenol、TE、Molex、Luxshare、BizLink、FIT、Broadcom、Marvell、Spectra7、Semtech |
| 800G/1.6T OSFP connectors/cages | 前面板 pluggable IO | TE OSFP 224G 支持 1.6T、DAC/ACC/AEC；Amphenol ExtremePort OSFP 224G 支持 1.6T per port。 | TE、Amphenol、Molex、FIT、Luxshare、JAE、Hirose、Yamaichi |
| 112G backplane connectors | STRADA/Paladin/Impel/ExaMAX/NovaRay | 112G 在交换机、NIC、AI server 已成熟，仍是 2026 主力。 | TE、Amphenol、Molex、Samtec、HARTING、ERNI、Yamaichi |
| PCIe Gen5/6 internal cabling | MCIO、Sliver、SlimSAS、CopprLink、EDSFF | PCI-SIG DevCon 2026 明确 CopprLink internal up to 1m/external up to 2m，PCIe 6/7 电气验证成为会议主线。 | TE、Amphenol、Molex、Samtec、BizLink、Luxshare、JAE、Foxconn/FIT |
| Retimer/signal conditioning | PCIe/CXL retimer、AEC DSP、SCM | Astera Q1 2026 +93%，Broadcom/Marvell 推 200G lane retimer/AEC，Credo AEC 爆发。 | Astera、Credo、Broadcom、Marvell、Parade、Montage、Microchip、MaxLinear、Semtech |
| 结构化光纤 trunk 与高密 patch | OS2/OM4/OM5、MPO/MTP、SN/CS/MDC、预端接 | Meta-Corning up to $6B；Legrand Chroma Link 1RU 2,304 fibers/2RU 4,608 fibers；AI 集群需要更多 fiber pairs。 | Corning、CommScope/Amphenol、Legrand、Panduit、Belden、Siemon、Senko、Rosenberger OSI、R&M、Furukawa、Prysmian、Nexans |
| 光纤管理和配线系统 | patch panel、raceway、trunk harness、颜色索引 | AI rack 追线/维护时间变成瓶颈，Legrand/Senko、Panduit、CommScope 等推出 AI 高密方案。 | Legrand、Panduit、CommScope/Amphenol、Corning、Belden、Siemon、Senko、Rittal、nVent |

### 2.2 未来 3 个月、一年、两年规模和渗透率

| 产品 | 未来 3 个月规模 | 未来 1 年规模 | 未来 2 年规模 | 渗透率路径 |
|---|---:|---:|---:|---|
| 800G DAC/AEC/ACC | B: $0.8-1.2B；O: $1.2-1.8B；X: $1.8-2.6B | B: $4-6B；O: $6-9B；X: $9-13B | B: $8-14B；O: $14-24B；X: $24-40B | AI rack 内短距铜连接 attach 2026 55-75%，2027 65-85%，2028 70-90%；AEC 在长于 DAC 可达距离的链路中 2026 25-40%，2027 40-60%。 |
| OSFP/QSFP-DD 800G/1.6T connector/cage/cable assemblies | B: $0.6-1.0B；O: $1.0-1.5B；X: $1.5-2.2B | B: $3-5B；O: $5-8B；X: $8-12B | B: $7-12B；O: $12-22B；X: $22-35B | 800G port 2026 为新增 AI 后端网络主流；1.6T port 2026 <10%，2027 15-30%，2028 30-50%。 |
| 112G 高速背板/中板连接器 | B: $0.5-0.8B；O: $0.8-1.2B；X: $1.2-1.8B | B: $2.5-4B；O: $4-6B；X: $6-9B | B: $4-7B；O: $7-12B；X: $12-20B | 112G 在 2026 仍占高速背板价值 60-75%；2027 被 224G 逐步挤压但总量继续增长。 |
| PCIe Gen5/6 internal cables/CopprLink/MCIO/Sliver | B: $0.4-0.7B；O: $0.7-1.1B；X: $1.1-1.7B | B: $2-3.5B；O: $3.5-6B；X: $6-9B | B: $4-8B；O: $8-14B；X: $14-25B | 高端 AI server 内部线缆化 2026 30-45%，2027 45-65%，2028 60-80%。 |
| Retimer/AEC DSP/signal conditioning | B: $0.8-1.2B；O: $1.2-1.8B；X: $1.8-2.8B | B: $4-6.5B；O: $6.5-10B；X: $10-16B | B: $9-16B；O: $16-28B；X: $28-45B | PCIe/CXL/以太网高端链路 retimer attach 2026 25-40%，2027 40-60%；AEC DSP 随 1.6T 升级。 |
| AI 数据中心结构化光纤布线 | B: $1.3-2.2B；O: $2.2-3.5B；X: $3.5-5.0B | B: $6-10B；O: $10-16B；X: $16-24B | B: $14-24B；O: $24-42B；X: $42-70B | 新建 hyperscale AI campus 预端接/高密布线 2026 50-70%，2027 70-85%，2028 80-90%；高密 VSFF/SN-MT 2026 2-5%，2027 8-18%，2028 20-35%。 |
| 光纤管理、配线架、raceway、标识文档系统 | B: $0.5-0.9B；O: $0.9-1.4B；X: $1.4-2.2B | B: $2.5-4.5B；O: $4.5-7B；X: $7-11B | B: $6-11B；O: $11-20B；X: $20-35B | AI 项目中可维护高密配线从 2026 30-45% 提升到 2028 60-80%。 |

说明：B=基准，O=乐观，X=极度超预期乐观。结构化光纤口径与 Grand View 的 data center wire/cables 2026 $21.51B、Research and Markets 的 structured cabling 2026 $16.29B 有重叠，本报告只取 AI/DC 可归因的增量和高端部分，极度乐观情景允许 NVIDIA/Meta/Google/OpenAI 等提前锁定光纤和连接产能。

### 2.3 已放量产品利润率预测

| 产品 | 当前典型毛利率 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|---:|
| 被动 DAC/普通高速线缆 | 18-30% | 18-28%，铜价和竞争压制 | 25-35%，高端 AI 线缆 mix 上升 | 30-40%，短期供给紧缺和客户认证溢价 |
| ACC/AEC cable assembly | 25-42% | 25-38% | 35-48% | 45-58%，retimer/DSP 与可靠性溢价强 |
| AEC/retimer/DSP 芯片 | 60-75% | 60-70% | 68-76% | 72-80%，若客户锁定少数供应商 |
| OSFP/QSFP-DD connector/cage | 25-40% | 25-35% | 35-45% | 40-52%，224G/1.6T 初期 |
| 112G 背板连接器 | 28-42% | 28-38% | 35-45% | 42-50%，若客户急需交付 |
| 结构化光纤 trunk/patch panel | 25-40% | 25-35% | 32-45% | 40-55%，预制化/高密/认证项目 |
| 配线管理/文档/颜色索引系统 | 30-45% | 30-40% | 40-50% | 48-60%，人力节省可量化时 |
| 安装与现场服务 | 12-25% | 12-22% | 20-30% | 28-40%，项目延误成本极高时 |

## 3. 在研和即将快速增长的关键产品

### 3.1 在研/早期导入产品

| 产品/技术 | 当前阶段 | 成熟时间 | 放量时间 | 关键厂商 |
|---|---|---:|---:|---|
| 224G co-packaged copper/CPC/NPC | Molex Impress、Samtec Si-Fly HD、Amphenol XtremePass/UltraPass、Luxshare KOOLIO 已展示 | 2026H2 | 2027 | Molex、Samtec、Amphenol、Luxshare、TE、FIT、JAE、Yamaichi |
| 224G 背板/线缆背板 | Amphenol Paladin HD2/ZettaMAX、Samtec 224G Si-Fly backplane、Molex 224G portfolio | 2026H2 | 2027 | Amphenol、Samtec、Molex、TE、Luxshare、Shennan、TTM |
| 448G copper channel/test fixtures | Samtec 448G prototype、DesignCon 448G papers、PCIe 8 pathfinding | 2027 | 2028，极乐观 2027H2 | Samtec、Amphenol、Molex、Luxshare、Keysight、Anritsu、Synopsys |
| PCIe 7 connector/cable | PCIe 7.0 已发布，128GT/s；DevCon 聚焦电气和 CopprLink/SFF | 2027 | 2028 | PCI-SIG 生态、TE、Amphenol、Molex、Samtec、JAE、Yamaichi |
| PCIe 8/256GT/s connector pathfinding | Draft 0.5/标准 2028 目标；Amphenol ZettaMAX 指向 PCIe Gen7/8 | 2028 | 2029+，但 2026 起有研发订单 | Amphenol、TE、Molex、Samtec、Synopsys、Marvell、Keysight |
| 1.6T/3.2T AEC | 1.6T AEC 已有产品，3.2T 仍在研发 | 2026/2027 | 2027/2028 | Credo、Marvell、Broadcom、Molex、Amphenol、TE、Luxshare |
| XPO 12.8T liquid-cooled pluggable | Arista MSA，OFC 2026 展示 | 2027 | 2027H2-2028 | Arista、Molex、Eoptolink、Linktel、Coherent、Senko |
| CPO/CPX socket/ELS/fiber attach | Broadcom/NVIDIA/Coherent/Lumentum/Open CPX | 2027 | 2027-2028 | Broadcom、NVIDIA、Coherent、Lumentum、Molex、Samtec、Senko、Corning |
| VSFF/SN-MT/MCF 高密光纤 | Legrand Chroma Link、Senko SN-MT，OCP 多芯光纤讨论 | 2026H2-2027 | 2027-2028 | Senko、Legrand、Corning、Sumitomo、Furukawa、Rosenberger OSI、Panduit |
| 智能布线/自动文档 | 颜色索引、DCIM/telemetry、电子标签 | 2026 | 2027 | Legrand、Panduit、CommScope/Amphenol、Corning、Belden、Raritan/Legrand |

### 3.2 在研产品市场规模和渗透率预测

| 产品 | 未来 3 个月规模 | 未来 1 年规模 | 未来 2 年规模 | 渗透率路径 |
|---|---:|---:|---:|---|
| 224G CPC/NPC/near-ASIC copper | B: $0.10-0.25B；O: $0.25-0.50B；X: $0.50-0.90B | B: $0.8-1.8B；O: $1.8-3.5B；X: $3.5-6.5B | B: $4-8B；O: $8-16B；X: $16-30B | 高端 AI switch/accelerator tray 中 2026 5-12%，2027 20-40%，2028 45-70%。 |
| 224G 背板/线缆背板 | B: $0.15-0.35B；O: $0.35-0.65B；X: $0.65-1.1B | B: $1.0-2.2B；O: $2.2-4.5B；X: $4.5-8B | B: $5-10B；O: $10-20B；X: $20-36B | 新设计中 224G backplane 2026 8-18%，2027 25-45%，2028 50-75%。 |
| 448G copper/test ecosystem | B: $0.03-0.10B；O: $0.10-0.25B；X: $0.25-0.50B | B: $0.2-0.6B；O: $0.6-1.4B；X: $1.4-3B | B: $1-3B；O: $3-8B；X: $8-18B | 2026 几乎全是研发/测试，2027 1-5% pilot，2028 10-25%。 |
| PCIe 7 connector/cable/retimer ecosystem | B: $0.15-0.35B；O: $0.35-0.70B；X: $0.70-1.2B | B: $1-2.5B；O: $2.5-5B；X: $5-9B | B: $5-12B；O: $12-25B；X: $25-45B | AI server 新平台 2026 设计验证，2027 5-15%，2028 25-45%。 |
| CPO/CPX socket/ELS/fiber attach | B: $0.05-0.15B；O: $0.15-0.35B；X: $0.35-0.80B | B: $0.5-1.5B；O: $1.5-4B；X: $4-10B | B: $3-10B；O: $10-28B；X: $28-70B | AI switch 新增端口中 2026 <1%，2027 2-8%，2028 8-20%；极乐观 2027 即 10%+。 |
| XPO 12.8T | B: <$0.05B；O: $0.05-0.15B；X: $0.15-0.35B | B: $0.2-0.8B；O: $0.8-2B；X: $2-5B | B: $1-4B；O: $4-12B；X: $12-25B | 2026 样机，2027 高端 switch pilot，2028 若 CPO 慢则可快速上升。 |
| VSFF/SN-MT/MCF 高密结构化布线 | B: $0.10-0.25B；O: $0.25-0.50B；X: $0.50-0.90B | B: $0.8-2B；O: $2-5B；X: $5-10B | B: $4-10B；O: $10-24B；X: $24-50B | 新建 AI campus 中 2026 2-5%，2027 8-18%，2028 20-35%；极乐观 2028 50%。 |
| 智能布线/自动文档/可视化运维 | B: $0.05-0.15B；O: $0.15-0.35B；X: $0.35-0.70B | B: $0.5-1.2B；O: $1.2-3B；X: $3-6B | B: $2-5B；O: $5-12B；X: $12-25B | 大型 AI campus 2026 10-20%，2027 25-45%，2028 50-75%。 |

### 3.3 在研产品利润率预测

| 产品 | 当前/早期毛利率 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|---:|
| 224G CPC/NPC | 45-60% | 40-55% | 50-65% | 60-75%，若成为唯一可量产路径 |
| 224G 背板/线缆背板 | 35-50% | 35-48% | 45-58% | 55-68% |
| 448G test/connector prototype | 50-70% | 45-60% | 55-70% | 65-80%，测试和工程服务更高 |
| PCIe 7/8 connector/cable | 35-55% | 35-48% | 45-60% | 58-72% |
| CPO/CPX socket/ELS | 40-65% | 35-55% | 50-65% | 60-75%，但 field service 成本可能侵蚀 |
| XPO | 45-65% | 40-55% | 50-65% | 60-75% |
| VSFF/SN-MT/MCF 布线 | 35-55% | 32-45% | 42-58% | 55-70% |
| 智能布线/自动文档软件化硬件 | 45-70% | 40-55% | 55-70% | 65-80% |

## 4. 供给侧：产能、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/能力 |
|---|---|---|---|
| 高速连接器设计和精密制造 | 美国、墨西哥、中国、马来西亚、越南、台湾、日本、欧洲 | Amphenol、TE、Molex、Samtec、Luxshare、FIT、Hirose、JAE、Yamaichi、Rosenberger、HARTING、ERNI | 冲压、电镀、注塑、自动组装、精密公差、SI 仿真、系统认证 |
| 高速铜缆和 cable assembly | 中国、台湾、越南、泰国、马来西亚、墨西哥、美国 | Amphenol、TE、Molex、Luxshare、BizLink、FIT、Volex、Nvidia ecosystem、Credo partners | twinax、低 skew、屏蔽、端接、EEPROM、retimer 模块集成、自动测试 |
| 背板/PCB/线缆背板 | 中国大陆、台湾、日本、韩国、美国 | Shennan、TTM、Unimicron、Tripod、Compeq、Gold Circuit、Wus、Ibiden、Shinko、Molex、Amphenol | 高层低损耗 PCB、backdrill、via/fanout、cabled backplane、orthogonal backplane |
| AEC/retimer/DSP 芯片 | 美国、以色列、中国台湾、中国大陆 | Credo、Broadcom、Marvell、Astera、MaxLinear、Parade、Montage、Microchip、Semtech、Spectra7 | SerDes、PAM4 DSP、retimer、linear redriver、CXL/PCIe/Ethernet switch |
| 结构化光纤/光缆/连接 | 美国、中国、墨西哥、欧洲、日本、印度 | Corning、CommScope/Amphenol、Prysmian、Nexans、Furukawa、Sumitomo、YOFC、Hengtong、STL、Legrand、Panduit、Belden、Siemon、Senko、Rosenberger OSI | 光纤拉丝、ribbon/slotted cable、预端接、MPO/SN/CS/MDC、配线架、fiber raceway |
| 安装和交付 | 美国、欧洲、中东、亚洲本地 | Hyperscaler 自有团队、EPC、数据中心集成商、Anixter/Wesco、Graybar、Legrand/Panduit/Corning partners | 预制化、现场熔接/测试、OTDR、标签、文档、DCIM 集成 |

### 4.2 供给瓶颈

1. **224G/448G 信号完整性人才和验证设备。** 高速连接器不是机械件，仿真、S 参数、de-embedding、BER/FEC、热漂移、串扰统计都需要稀缺工程师和高端仪器。
2. **精密冲压、电镀和塑胶公差。** 224G/1.6T 时代，微小公差、电镀厚度、接触电阻、插拔磨损都会变成 BER 和返修风险。
3. **低损耗 twinax 与端接工艺。** 线缆 skew、屏蔽、弯折半径、焊接/压接一致性决定 AEC/DAC 良率，不能简单靠扩线解决。
4. **Retimer/DSP 芯片供应。** AEC 需要 Marvell/Broadcom/Credo 等芯片，200G/lane/1.6T/3.2T 还受先进制程、封装和测试约束。
5. **高密光纤连接器和预端接产能。** MPO/SN-MT/VSFF、超高纤芯数 trunk、颜色索引、预端接 harness 的自动化和检测产能不足。
6. **客户认证周期。** Hyperscaler/NVIDIA/AMD/Google/AWS/Meta/Azure 的平台认证可能长达 6-18 个月，认证通过后才有强定价权。
7. **现场安装和文档瓶颈。** 大型 AI campus 线缆数量巨大，追线、标签、OTDR 测试、变更管理会限制上电速度。
8. **光纤/铜/镀金/树脂材料价格。** 铜价、金价、低损耗树脂和氟材料波动会影响 BOM，短缺时可传导，宽松时压毛利。
9. **地缘和关税。** 高速连接器产能在中国、东南亚、墨西哥、美国间重新分配，客户要求区域化备份。
10. **液冷和线缆空间冲突。** 100kW+ rack 内冷板、manifold、电源母线、线缆路径互相挤占，连接器设计需要与机柜/冷却协同。

### 4.3 成本结构和毛利决定因素

| 产品 | 典型成本构成 | 毛利决定因素 |
|---|---|---|
| 被动 DAC | 铜/twinax 35-50%；连接器/cage 15-25%；组装测试 15-25%；包装/物流 5-10%；良率损耗 5-10% | 铜价、长度/AWG、客户认证、批量自动化、ASP 下行速度 |
| ACC/AEC | twinax 20-35%；连接器 10-20%；retimer/redriver/DSP 25-45%；PCB/散热/EEPROM 5-15%；测试 10-20% | 芯片供应、BER 可靠性、功耗、长度、现场故障率、客户锁定 |
| 高速背板连接器 | 金属端子/电镀 25-35%；塑胶/壳体 15-25%；精密制造 20-30%；测试/认证 10-20%；研发摊销 5-15% | 代际速度、信号余量、插拔可靠性、平台认证、可替换供应商数量 |
| CPC/near-ASIC copper | 精密连接器/压接 25-40%；低损耗线缆 20-35%；定制 substrate/fixture 10-20%；测试 15-25% | 是否进入 reference design、是否绕开 PCB 损耗、可维护性、良率 |
| 结构化光纤 trunk | 光纤/光缆 30-50%；连接器/扇出 15-30%；预端接和测试 15-25%；配线硬件 10-20% | fiber count、连接器密度、预制化、安装节省、交付周期 |
| 高密配线架/管理系统 | 金属/塑胶 20-35%；连接器/cassette 25-40%；标识/管理 10-20%；组装 15-25% | 密度、维护时间节省、人为错误降低、是否绑定 DCIM/标准 |

价格传导机制：

| 成本/短缺 | 传导能力 | 原因 |
|---|---|---|
| 铜、金、光纤材料涨价 | 中 | 大客户有年度价格框架，但短交期项目可 surcharge。 |
| Retimer/DSP 短缺 | 高 | AEC 没有芯片不能交付，且可替换供应商少。 |
| 224G/448G 认证件短缺 | 很高 | 客户更关注 GPU 利用率和上电时间，愿为已认证件付溢价。 |
| 现场安装人力短缺 | 中高 | 延迟上电损失巨大，预制化和交付服务可溢价。 |
| 普通结构化布线竞争 | 低到中 | 供应商多，若不具备高密/预制/认证优势，价格竞争强。 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分市场 | 头部集中度估计 | 竞争状态 |
|---|---:|---|
| 全球连接器整体 | CR10 约 55-65% | Amphenol、TE、Molex 三强，Samtec 等高端细分强。 |
| AI 高速背板/224G 连接 | CR5 约 60-75% | 需要 SI 和平台认证，集中度高。 |
| AEC retimer/DSP 芯片 | CR5 约 75-90% | Credo、Broadcom、Marvell、Astera/MaxLinear 等少数玩家。 |
| 高速线缆 assembly | CR10 约 50-70% | 大厂和亚洲制造强者并存，认证后粘性高。 |
| 数据中心结构化布线 | CR10 约 45-60% | Corning、CommScope/Amphenol、Legrand、Panduit、Belden、Siemon、Senko 等。 |
| 高密 VSFF/SN-MT/MCF | CR5 约 60-80% | 连接器 IP、标准参与和客户验证决定份额。 |

### 5.2 可量化壁垒

| 壁垒 | 为什么能定价 | 可量化指标 |
|---|---|---|
| 信号完整性 | BER/FEC margin 直接影响 GPU 利用率和集群稳定性，客户不敢用未验证替代品。 | 112G/224G eye margin、pre-FEC BER、S 参数、串扰、skew、温漂。 |
| 平台认证 | 进入 NVIDIA/AMD/Google/AWS/Meta/Azure rack BOM 后，切换会触发重新验证。 | 认证周期 6-18 个月；field failure penalty 高。 |
| 规模和自动化 | 高速线缆/连接器需要百万级一致性制造，手工组装良率不可控。 | 良率、PPM、交期、自动测试吞吐。 |
| 客户协同设计 | 近 ASIC/CPC/背板必须在芯片、PCB、散热、机柜阶段共同设计。 | design-in 提前 12-24 个月；NRE 和仿真数据沉淀。 |
| 供应链垂直整合 | 端子、电镀、塑胶、线缆、组装、测试、全球交付一体化可控交期。 | 是否有多地区产能、是否自有关键工艺。 |
| 标准参与 | OSFP、OIF、PCI-SIG、OCP、UALink、CPX/XPO MSA 中有话语权能提前锁定形态。 | 是否为 MSA/标准成员、是否有 demo/参考设计。 |
| 现场交付和文档 | AI campus 不是卖完硬件就结束，错误连接会拖延上电。 | 每 1RU fiber density、追线时间、OTDR pass rate、变更文档自动化。 |

### 5.3 价值捕获排序

| 价值链环节 | 长期 ROIC/毛利潜力 | 原因 |
|---|---|---|
| Retimer/DSP/SerDes/fabric switch 芯片 | 最高 | 芯片/IP 毛利高，attach rate 上行，客户锁定强。 |
| 224G/448G CPC、near-ASIC、背板连接器 | 很高 | 技术壁垒高、认证强、替代风险低。 |
| 高密结构化光纤连接与管理系统 | 高 | 直接缩短部署和维护时间，AI campus fiber count 暴增。 |
| 高速线缆 assembly | 中高 | 认证后有粘性，但制造竞争和铜价影响较大。 |
| 普通 DAC/标准 connector | 中 | 量大但竞争激烈。 |
| 安装服务/EPC 布线 | 中 | 项目周期强，区域性强，规模化利润率有限；但短缺期可溢价。 |

## 6. 2026 关键变化：3 个行业拐点

### 6.1 800G 从高端变默认，1.6T 从样品变导入

2026 年新增 AI 后端网络中 800G 成为主流，GB300/TPU/Trainium/MTIA/MI350 都会拉动 800G 端口。1.6T 的收入还小于 800G，但 2026H2 大客户会开始把 1.6T 写入新建集群设计。连接器、cage、AEC、光纤 trunk、配线架都会提前拿到订单。

投资含义：800G 是确定收入，1.6T 是估值弹性；OSFP 224G、AEC DSP、预制光纤和测试设备最受益。

### 6.2 铜互联叙事反转：铜不消失，而是高端化

市场容易把 AI 互联理解为“光替代铜”。实际 2026 的路径是：跨 rack/campus 光化，rack 内和 near-ASIC 铜高端化。Molex、Samtec、Amphenol、TE、Luxshare 都在推 224G/CPC/top-side/flyover/AEC，说明铜互联的形态从 PCB 长走线转向线缆化、上基板和主动化。

投资含义：CPC、AEC、ACC、low-skew twinax、高速背板连接器比普通 DAC 更有 alpha。

### 6.3 结构化布线成为 AI 上电速度约束

Corning 与 Meta 最高 $6B 协议、NVIDIA-Corning 合作、Legrand Chroma Link 的 2,304 fibers/1RU 和 4,608 fibers/2RU，说明高纤芯密度、预端接、追线和维护正成为 AI campus 的关键门槛。

投资含义：结构化布线不是低毛利工程活，头部高密系统可拿硬件+服务+长期维护溢价。

## 7. 2027 关键变化：3 个行业拐点

### 7.1 224G 和 1.6T 成为新增高端 AI 平台主线

Rubin、MI400/Helios、Trainium3、TPU8、OpenAI/Broadcom、Meta MTIA 等平台会把 224G PAM4、1.6T OSFP、1.6T AEC/光模块、PCIe Gen6/7 推入更大规模部署。2027 的高端连接器/线缆价值会明显高于 2026。

### 7.2 开放 scale-up 生态开始兑现

UALink 200G 1.0 已可用，OCP/ESUN/SUE-T/PCIe/CXL 生态在 2026 验证，2027 会在非 NVIDIA XPU、custom ASIC、AMD Helios、部分 hyperscaler 自研系统中兑现。开放互联会提高 merchant 连接器、retimer、fabric switch、线缆背板的 TAM。

### 7.3 CPO/CPX/XPO 与高密光纤从 pilot 进入局部商业化

2027 不会全面替代 pluggable，但 Spectrum-6/SPX、Broadcom CPO、Open CPX、XPO 等会进入部分高端 AI switch。与此同时，VSFF/SN-MT/MCF、高密配线和光纤管理会从可选升级变成头部 AI campus RFP 项。

## 8. 头部公司和细分公司清单

### 8.1 高速连接器和背板

| 方向 | 公司 |
|---|---|
| 综合连接器龙头 | Amphenol、TE Connectivity、Molex、Samtec、Luxshare Precision/Luxshare-Tech、Foxconn Interconnect Technology/FIT Hon Teng、Hirose、JAE、Yamaichi、Rosenberger、HARTING、ERNI、Kyocera AVX |
| 高速背板/中板/orthogonal | Amphenol Paladin/ExaMAX/ZettaMAX、TE STRADA Whisper、Molex Impel/Impact/Mirror Mezz/Inception、Samtec ExaMAX/NovaRay/Si-Fly、HARTING har-modular、ERNI、Yamaichi |
| Near-ASIC/top-side/CPC | Molex Impress/NearStack/CX2、Samtec Si-Fly HD、Amphenol UltraPass/XtremePass/Celerity、Luxshare KOOLIO CPC/NPC、TE AdrenaLINE/near-chip programs、FIT CPO/high-speed connector |
| OSFP/QSFP-DD/OSFP-XD | Amphenol、TE、Molex、Luxshare、FIT、JAE、Hirose、Yamaichi、Senko、NVIDIA ecosystem |
| PCIe/EDSFF/MCIO/Sliver/CopprLink | TE、Amphenol、Molex、Samtec、Luxshare、BizLink、JAE、Yamaichi、Foxconn/FIT、3M legacy、Hirose |

### 8.2 高速铜缆、AEC、ACC、DAC

| 方向 | 公司 |
|---|---|
| AEC/ACC/DAC cable assembly | Amphenol、TE、Molex、Luxshare、BizLink、FIT Hon Teng、Volex、NVIDIA/Mellanox ecosystem、FS、NADDOD、Linktel、Eoptolink、Innolight |
| AEC/retimer/DSP 芯片 | Credo、Marvell、Broadcom、MaxLinear、Astera Labs、Semtech、Spectra7、Parade、Montage Technology、Microchip、Rambus、Synopsys/Cadence IP |
| 高性能 twinax/材料 | Sumitomo Electric、Fujikura、Hitachi Metals/Proterial、3M、Gore、Carlisle Interconnect、Prysmian、Leoni、LS Cable、Hengtong、Luxshare、BizLink |

### 8.3 结构化布线、光纤、连接和管理

| 方向 | 公司 |
|---|---|
| 光纤/光缆 | Corning、Prysmian、Nexans、Furukawa Electric/OFS、Sumitomo Electric、YOFC、Hengtong、FiberHome、STL、Fujikura、LS Cable |
| 数据中心结构化布线 | CommScope/Amphenol、Corning、Legrand、Panduit、Belden、Siemon、R&M、Rosenberger OSI、Nexans、Prysmian、Furukawa/OFS、Schneider、Leviton |
| 高密光连接器 | Senko、US Conec、Corning、CommScope/Amphenol、Molex、TE、Rosenberger、Fujikura、Sumitomo、Hirose |
| 配线架/raceway/cable management | Legrand、Panduit、CommScope/Amphenol、Corning、Belden、Siemon、R&M、nVent、Rittal、Schneider、Hubbell、Chatsworth Products |
| 智能布线/文档/DCIM 接口 | Panduit、Legrand/Raritan、CommScope、Corning、Belden、Siemon、Schneider、Vertiv、Sunbird、Nlyte/Carrier |

### 8.4 光互联/CPO/XPO/OCS 相关连接

| 方向 | 公司 |
|---|---|
| CPO/CPX socket/connector | Broadcom、NVIDIA、Coherent、Molex、Samtec、Senko、TE、Amphenol、Lumentum、Marvell、Ayar Labs、Intel Silicon Photonics |
| XPO/liquid-cooled pluggable | Arista、Molex、Eoptolink、Linktel、Coherent、Senko、Amphenol、TE、Lumentum |
| OCS/fiber switching | Google/Apollo ecosystem、iPronics、Polatis/HUBER+SUHNER、Calient、Coherent、Nokia、Ciena、Broadcom |
| 测试与验证 | Keysight、Anritsu、Teledyne LeCroy、VIAVI、Rohde & Schwarz、Tektronix、MultiLane、Spirent、Synopsys、Cadence、Ansys |

### 8.5 亚洲和中国弹性公司

| 方向 | 公司 |
|---|---|
| 中国/台湾高速连接器与线缆 | Luxshare Precision、Luxshare-Tech、FIT Hon Teng、BizLink、Alltop、Aces Electronics、SpeedTech、Bellwether、LOTES、Longwell、Cheng Uei/Foxlink |
| 中国 PCB/背板 | Shennan Circuits、Wus Printed Circuit、Victory Giant、SCC、Founder PCB、Kinwong、Huatong/Compeq、Tripod、Gold Circuit、Unimicron |
| 中国光模块/光连接/布线 | Innolight、中际旭创、新易盛、Eoptolink、光迅科技、华工科技、剑桥科技、天孚通信、太辰光、长飞、亨通、烽火通信、博创科技 |
| 日本连接和线缆 | Hirose、JAE、Yamaichi、Sumitomo Electric、Fujikura、Furukawa、Mitsubishi Cable、Proterial |

## 9. 投资排序

| 排名 | 子方向 | 2026 确定性 | 2027 弹性 | 毛利潜力 | 核心风险 |
|---:|---|---:|---:|---:|---|
| 1 | AEC/ACC/retimer/DSP | 很高 | 很高 | 高 | 客户集中、ASP 竞争、CPO/光化替代部分场景 |
| 2 | 224G 背板/CPC/near-ASIC copper | 中高 | 很高 | 很高 | 技术路线分裂、认证周期 |
| 3 | 高密结构化光纤布线/管理 | 高 | 很高 | 中高到高 | 工程服务占比高、项目周期 |
| 4 | OSFP 800G/1.6T connector/cage/cable assembly | 很高 | 高 | 中高 | 多供应商价格竞争 |
| 5 | PCIe Gen6/7 CopprLink/MCIO/Sliver | 高 | 高 | 中高 | 平台采用节奏和标准形态 |
| 6 | CPO/CPX/XPO 连接生态 | 中 | 很高 | 高 | 2026 收入小、可靠性和可维护性 |
| 7 | 448G/PCIe8 测试和连接 pathfinding | 低收入高信号 | 高 | 很高 | 节奏偏远、标准未定 |

## 10. 风险提示

1. **AI capex 延迟。** 电力、土地、并网、液冷和监管可能导致 GPU 已订但 rack 延迟上电，连接器和布线收入确认滞后。
2. **ASP 快速下行。** 800G/1.6T 多供应商产能追上后，普通模块和线缆会出现价格竞争。
3. **技术路线分裂。** CPO、CPX、XPO、LPO、AEC、ACC、PCIe optical、UALink 等并行，库存和研发押注风险上升。
4. **客户集中。** Credo/Astera 等高成长公司高度依赖少数 hyperscaler，订单节奏影响季度波动。
5. **良率和现场故障。** 高速连接器现场失效成本巨大，一次质量事故可能导致客户资格丢失。
6. **中国供应链和出口限制。** AI 芯片、光模块、retimer、先进制造设备限制会改变区域份额。

## 11. 主要来源

### 公司一手信息

| 来源 | 关键信息 |
|---|---|
| [NVIDIA Blackwell Ultra 技术博客](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-for-the-era-of-ai-reasoning/) | GB300 NVL72：72 GPU、36 Grace CPU、130TB/s NVLink、每 GPU 800Gb/s 网络吞吐。 |
| [NVIDIA Vera Rubin POD 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | Vera Rubin POD：40 racks、1,152 Rubin GPUs、60 exaflops、10PB/s bandwidth、Spectrum-6 SPX 硅光。 |
| [Amphenol 2026Q1 业绩](https://www.nasdaq.com/press-release/amphenol-reports-record-first-quarter-2026-results-2026-04-29) | 销售 $7.6B、订单 $9.4B、book-to-bill 1.24、IT datacom 强增长、完成 CommScope CCS。 |
| [TE Connectivity FY2026Q2 业绩](https://www.te.com/en/about-te/news-center/corporate-news/2026/2026-04-22-te-connectivity-delivers-results-above-guidance-with-15-sales-growth-and-over-20-eps-growth-in-second-quarter-of-fiscal-2026.html) | 销售 $4.744B、订单 $5.3B，同比 +25%，AI 驱动 record orders。 |
| [Credo FY2026Q3 业绩](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx) | 收入 $407M，环比 +52%，同比 +200%+，毛利高，AEC/hyperscaler 拉动。 |
| [Astera Labs 2026Q1 业绩](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results) | 收入 $308.4M，同比 +93%，Scorpio X-Series 320-lane AI fabric switch shipping。 |
| [Broadcom OFC 2026](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai) | 3.5D XPU、102.4T CPO switch、400G/lane DSP、200G/lane retimer/AEC、PCIe Gen6 switch/retimer。 |
| [Molex AEC](https://www.molex.com/en-us/products/connectors/high-speed-pluggable-io/active-electrical-cables-aec) | 112G AEC 到 7m，224G 到 2.5m+，1.6T AEC 用 Broadcom/Marvell DSP。 |
| [Molex Impress 224G co-packaged copper](https://www.molex.com/en-us/news/molex-launches-impress-co-packaged-copper-solutions-scaling-near-asic-connectivity-innovations-to-meet-next-gen-data-rate-demands.html) | 2026-02 发布上基板/近 ASIC 224Gbps PAM4 铜连接。 |
| [Amphenol 224G High-Speed Solutions](https://www.amphenol-cs.com/224g-high-speed-solutions) | Celerity 224G BGA mezzanine、ExtremePort OSFP 224G、UltraPass。 |
| [Amphenol DesignCon 2026](https://www.amphenol-cs.com/events/designcon) | ZettaMAX 指向 300Gb/s 和 PCIe Gen7/8 高密背板系统。 |
| [TE OSFP 224G](https://www.te.com/en/products/connectors/high-speed-pluggable-io-connectors-and-cages/osfp.html) | OSFP 支持 200G 到 1.6T；DAC 到 1.3m、ACC 1.2-2.5m、AEC 超过 2.5m。 |
| [Samtec DesignCon 2026](https://blog.samtec.com/post/samtec-at-designcon-2026/) | 224G/448G、Si-Fly HD CPC、backplane、BE71A/BE130 测试。 |
| [Corning-Meta up to $6B](https://investor.corning.com/news-and-events/news/news-details/2026/Corning-and-Meta-Announce-Multiyear-up-to-6-Billion-Agreement-to-Accelerate-US-Data-Center-Buildout/default.aspx) | Corning 向 Meta 供应 AI 数据中心光纤、线缆、连接产品，最高 $6B。 |
| [NVIDIA-Corning 2026-05](https://www.corning.com/worldwide/en/about-us/news-events/news-releases/2026/05/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure.html) | 长期商业和技术伙伴关系，扩大美国 AI 光连接制造。 |
| [Legrand Chroma Link](https://www.prnewswire.com/news-releases/legrand-launches-industrys-first-color-indexed-hyper-density-fiber-solution-for-ai-data-centers-302715580.html) | 1RU 2,304 fibers、2RU 4,608 fibers，SN-MT 和颜色索引用于 AI 高密布线。 |
| [FIT Hon Teng DesignCon 2026](https://www.fit-foxconn.com/main/modules/MySpace/index.php?xmlid=28184) | 高速连接器、线缆、液冷 manifold、高电流方案布局 AI 供应链。 |
| [Luxshare-ICT AI data center infrastructure](https://br.advfn.com/noticias/PRNUS/2026/artigo/98356304) | 224G KOOLIO CPC/NPC、224G Intrepid NEXUS 背板、DAC/ACC/Lite Active Cable 等。 |

### 标准、会议和报告

| 来源 | 关键信息 |
|---|---|
| [UALink specifications](https://ualinkconsortium.org/specification/) | UALink 200G 1.0 支持 200G per lane、最多 1,024 accelerators；Common 2.0、DL/PL 2.0、Chiplet 1.0。 |
| [PCI-SIG DevCon 2026 agenda](https://pcisig.com/pci-sig-developers-conference-2026-agenda) | PCIe 6/7 电气、CopprLink internal 1m/external 2m、PCIe 7/8 连接器和光互联验证。 |
| [Grand View Data Center Wire & Cables 2026](https://www.grandviewresearch.com/industry-analysis/data-center-wire-cables-market-report) | Data center wire and cables 2026 市场规模 $21.51B，AI/HPC 和 800G 需求驱动。 |
| [Research and Markets Structured Cabling 2026](https://www.researchandmarkets.com/reports/5767260/structured-cabling-market-report) | Structured cabling 从 2025 $14.8B 到 2026 $16.29B，2030 $23.82B。 |
| [TrendForce CPO/AI high-speed interconnect 2026](https://www.trendforce.com/presscenter/news/20260311-12962.html) | NVIDIA 架构推动 CPO 渗透，2026 AI 数据中心 CPO 占比仍低但稳步上升。 |
| 项目内 `conference_update/ofc_2026_conference_update.md` | OFC 2026：1.6T、3.2T、CPO/CPX/XPO、OCS、coherent scale-across。 |
| 项目内 `conference_update/designcon_2026_conference_update.md` | DesignCon 2026：224G 部署、448G 探路、CPC/top-side、PCIe 7/8、高速 T&M。 |
| 项目内 `conference_update/pci_sig_devcon_2026_update.md` | PCI-SIG 2026：PCIe 7/8、CopprLink、optical-aware retimer、Gen6/Gen7 compliance。 |
| 项目内 `conference_update/OCP_EMEA_Summit_2026_高密度调研报告.md` | OCP EMEA 2026：Open DC for AI、800G/1.6T、UALink/ESUN/SUE-T、多芯光纤和高密机柜。 |
| 项目内 `ai_chip_research_2026_2027.md` | 2026-2027 大出货 AI 芯片/平台路线图和互联背景。 |
# 行业调研：【光DSP、TIA与CDR芯片】

版本日期：2026-05-08  
研究范围：光模块/光引擎中的 PAM4 光 DSP、相干 DSP、TIA、激光/调制器 Driver、CDR/retimer/redriver/AEC/ACC 芯片。为便于投资研究，本报告把“CDR 芯片”扩展到承担时钟恢复、均衡、重定时和链路诊断功能的高速连接 IC。  
口径说明：市场规模主要按“芯片与关键 IC 收入”估算，不等同于光模块总收入；若使用光模块市场数字，会单独说明。用户要求对 2026 年 AI 基础设施建设抱乐观预期，本报告在基准/乐观/极度超预期三个情景中均采用偏积极假设。

## 0. 高浓度结论

1. **2026 年是 1.6T 光互联从样品进入规模放量的第一年，光 DSP/TIA/CDR 的 beta 强于普通半导体周期。** TrendForce 预计全球 AI 专用光收发模块从 2025 年 **165 亿美元**增至 2026 年 **260 亿美元**，同比 **57%+**；Cignal AI 预计 2026 年 **800GbE 模块超过 2,000 万只、1.6TbE 模块超过 500 万只**。这意味着 1.6T PAM4 DSP、200G/lane TIA/Driver、AEC/ACC retimer 在 2026 年同步进入大客户拉货窗口。
2. **本报告估算 2026 年全球“光 DSP + TIA/Driver + CDR/retimer/AEC/ACC”芯片口径市场约为 58-96 亿美元，极度乐观可达 125 亿美元；2027 年基准 85-115 亿美元，乐观 120-170 亿美元，极度乐观 180-260 亿美元。** 该口径宽于 LightCounting 的“optical communications IC chipset”口径，因为纳入了数据中心 AEC/ACC/retimer/CDR 芯片，但不含完整光模块、激光器/EML 全部收入和交换芯片。
3. **2026 年最确定的技术路径不是单一 LPO 或 CPO，而是“1.6T fully-retimed optics/FRO + TRO/LRO 降功耗 + 200G/lane TIA/Driver + AEC/ACC 短距铜互联”并行。** Broadcom、Marvell、MaxLinear、Cisco/Acacia、Credo 都在 3nm/5nm 1.6T DSP 上给出量产或采样信号；Semtech、MACOM 则把 224G/448G TIA/Driver 和线性光学推到前台。
4. **DSP 不会在 2026 年被 LPO 消灭。** 1.6T 的大规模部署仍需要可靠的 FEC、均衡、遥测、BER/SNR/eye 监测、loopback 和客户可维护性；LPO/LRO/TRO 会先吃掉短距、低延迟、功耗敏感链路的 DSP 功耗预算，而不是立刻取代所有 retimed optics。
5. **TIA/Driver 是被低估的“每端口税”。** 只要 800G/1.6T 模块继续增长，接收端 TIA 和发射端 driver 必须同步增加；若 LPO/LRO 渗透率上升，DSP 内容量下降的一部分反而会转移到更高线性度、更低噪声、更强遥测的 TIA/Driver。
6. **CDR/retimer/AEC 是铜互联保命线。** AI rack 内 1-6 米链路仍优先用 DAC/AEC/ACC/near-ASIC copper，因为光电转换有功耗、延迟、成本和热管理惩罚。Credo Q3 FY2026 收入 **4.07 亿美元**、同比 **201.5%**、non-GAAP gross margin **68.6%**，是短距 active copper 与连接 IC 供不应求的最直接财务信号。
7. **供应瓶颈从“谁能封装模块”细化到 3nm/5nm DSP 晶圆、224G/448G SerDes、200G/400G EML/PD、CW laser、TIA-to-PD 寄生控制、光学对准、ATE/BERT 测试时间和客户认证。** TrendForce 明确指出 EML、CW-LD、光学对准、功耗散热是扩产瓶颈；Coherent Q3 FY2026 也称在强需求可见度下扩充资本投入。
8. **长期价值捕获最强的是：Broadcom/Marvell/Cisco-Acacia 这类“SerDes + DSP + switch/NIC + optics”平台型公司，其次是 Credo/MaxLinear/Semtech/MACOM 这类高弹性连接 IC 公司。** 通用模块组装规模大但毛利更容易被 ASP 下行压缩；真正能长期高 ROIC 的是有固件、算法、客户验证数据和系统级 reference design 的芯片层。
9. **2027 的关键不是 1.6T 是否存在，而是 3.2T/400G-per-lane、CPO/NPO/ELS、coherent-lite 与 OCS 是否从演示进入大客户设计。** Broadcom Taurus 400G/lane DSP、Semtech/MACOM 448G Driver/TIA、Marvell/Celestial AI Photonic Fabric、NVIDIA/Broadcom CPO、Google Apollo OCS 是最值得跟踪的技术拐点。
10. **投资视角：2026 看“1.6T 量产与缺货溢价”，2027 看“DSP-light 架构、CPO/NPO 和 3.2T 上游器件的第二曲线”。** 最强 beta 在 Credo、MaxLinear、Semtech、MACOM、Coherent、Lumentum、AOI、中国 800G/1.6T 模块链；最强 alpha 在 Broadcom、Marvell、Cisco/Acacia 这种把芯片、网络和客户锁定合在一起的平台。

## 1. AI 计算中心大规模建设下的机会、挑战与技术路径

### 1.1 产业链位置：光 DSP、TIA、CDR 到底赚哪一段钱

| 环节 | 典型位置 | 2026 主流速率 | 核心功能 | 价值属性 |
|---|---|---:|---|---|
| PAM4 光 DSP | 800G/1.6T OSFP/QSFP-DD、AOC、部分 AEC | 100G/lane、200G/lane，向 400G/lane 探路 | 均衡、FEC、retiming、gearbox、遥测、链路诊断、driver 集成 | 高毛利、高认证壁垒、强客户粘性 |
| 相干 DSP | 400ZR/800ZR/ZR+、1.6T ZR/ZR+、campus/metro/regional DCI | 400G、800G、1.6T | 相干调制/解调、FEC、MACsec、长距损伤补偿 | 算法与工艺壁垒最高，客户集中但生命周期长 |
| TIA | 光模块接收端，PD/SiPh/VCSEL/EML 后级 | 100G/lane、200G/lane、448G/lane 样品 | 光电流转电压、低噪声放大、线性化、均衡、遥测 | 模拟性能和封装寄生决定成败，单价小但 attach 率接近 100% |
| Driver | 光模块发射端，EML/MZM/SiPh/TFLN/VCSEL 前级 | 100G/lane、200G/lane、448G/lane 样品 | 驱动调制器/激光器、摆幅控制、预加重、线性度 | LPO/LRO 下价值上升，是 DSP-light 架构的关键 |
| CDR/retimer/redriver | 光模块内部、AEC/ACC 两端、交换机前面板、PCIe/CXL/以太网链路 | 100G/lane、200G/lane、256GT/s PCIe pathfinding | 时钟恢复、重定时、均衡、链路训练、BER 降低 | AI rack 内短距连接刚需，电互联距离越长价值越高 |

### 1.2 2026 年机会与挑战

| 维度 | 机会 | 挑战 |
|---|---|---|
| AI 集群规模 | GB300/B300、Trainium2/3、Ironwood TPU、MTIA、Maia、MI350 同时放量，端口数随 XPU 数量和网络层数非线性增长 | 电力、液冷、HBM 和机房交付可能让光模块订单出现季度波动 |
| 速率升级 | 800G 已成主流，1.6T 进入规模爬坡；102.4T switch 推动 200G/lane，204.8T switch 预热 400G/lane | 224G electrical/optical channel margin 小，测试、良率和散热压力高 |
| 架构变化 | FRO/TRO/LRO/LPO、AEC/ACC、OCS、CPO/NPO 并行，给不同芯片公司创造多条切入路径 | 技术路线碎片化，可能导致库存、认证和客户平台绑定风险 |
| 毛利与定价 | 供不应求产品可以通过长约、优先供货、firmware/telemetry 加价 | 2027 起模块 ASP 下行会向上游传导，低差异化 IC 毛利会承压 |
| 竞争格局 | 先进 DSP 供应商有限，TIA/Driver 需要模拟经验，客户切换成本高 | 大客户推动多供应商以降低 Broadcom/Marvell 单点依赖，MaxLinear/Credo/Cisco/Acacia 受益 |
| 供应链 | 3nm/5nm DSP、200G/400G EML/PD、CW laser、光学对准和测试是高溢价瓶颈 | 前道晶圆、封装测试、模块良率、客户现场可靠性同时限制放量速度 |

### 1.3 目前正在被使用的主要技术

| 技术 | 2026 状态 | 适用场景 | 对 DSP/TIA/CDR 的影响 |
|---|---|---|---|
| 800G FRO | 成熟放量 | 主流 AI scale-out、400G/800G switch 互联 | DSP、TIA、Driver attach 率高；ASP 开始下行但数量巨大 |
| 1.6T FRO | 进入量产爬坡 | 102.4T switch、GB300/TPU/ASIC 集群 | 3nm/5nm DSP 与 200G TIA/Driver 同步放量 |
| TRO | 2025-2026 快速导入 | 5-500m 中短距，降低模块功耗 | 只处理发射侧；接收端交给 TIA，DSP 内容量下降但 TIA 要求更高 |
| LRO | 2026 样品到小批量 | rack/row 内低功耗互联 | DSP 保留部分重定时，接收侧线性化，TIA/Driver 与 host SerDes tuning 价值上升 |
| LPO | 2026 试点，2027 扩大 | 短距、低延迟、功耗敏感链路 | 模块内 DSP 被移除，CDR/均衡压力转移到交换芯片/retimer/TIA/Driver |
| AEC/ACC | 已大规模使用，1.6T 加速 | rack 内 1-6m 铜互联 | CDR/retimer/redriver 是核心价值；Credo、Broadcom、Marvell、Astera、MACOM 受益 |
| 400ZR/800ZR/ZR+ | 400ZR 成熟，800ZR 放量 | DCI、campus、metro、regional | 相干 DSP 高壁垒，Marvell/Cisco-Acacia/Ciena/Nokia 主导 |
| 1.6T ZR/ZR+ | 2026H2 采样/导入 | AI scale-across | 2nm coherent DSP + MACsec，2027 后高利润增长 |
| CPO/NPO/ELS | 2026 demo/pilot，2027 早期部署 | 高端 switch、scale-up、near-package | 可能减少 pluggable DSP，但增加 optical engine、TIA/Driver、external laser、封装测试价值 |
| OCS | Google/少数云厂先行 | TPU-like all-optical inter-rack fabric | 减少 O-E-O 功耗，增加 800G/1.6T 模块需求和光纤管理价值 |

### 1.4 在 2026-2027 出货量最大的 AI 芯片技术路径背景下的互联推导

以下芯片/平台来自项目内既有 AI 芯片路线图，未用外部搜索重排。排序按项目内“2026-2027 年初可见等效出货数量 + 价值权重”理解。

| 排名 | AI 芯片/平台 | 2026-2027 互联背景 | 对光 DSP/TIA/CDR 的直接推导 |
|---:|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | rack 内 NVLink/铜为主，scale-out 用 800G/1.6T InfiniBand/Ethernet；102.4T switch 与 200G/lane 端口需求上升 | 2026 最强拉动 1.6T FRO/TRO、200G TIA/Driver、AEC/ACC retimer；NVIDIA 生态带动 Broadcom/Marvell/Semtech/Coherent/Lumentum |
| 2 | AWS Trainium2 | Project Rainier 级别部署，EFA/以太网 scale-out，rack 内 NeuronLink | AEC/ACC 和 800G/1.6T Ethernet optics 同时受益；自研系统会压低模块 ASP，但保留高可靠 CDR/retimer 需求 |
| 3 | Google TPU v7 Ironwood | 3D Torus + Apollo OCS；短距铜，跨 rack 全光网络 | TrendForce 估算 2026 近 400 万 TPU 带来 800G+ 模块需求超过 600 万只；利好 Innolight/Eoptolink、SiPh、TIA/Driver、OCS；LPO/低功耗方案优先 |
| 4 | NVIDIA B200/GB200 | 存量大，逐步让位 GB300；scale-out 仍大量消耗 800G | 800G DSP/TIA/Driver 延续高量；1.6T 渗透取决于客户升级到 102.4T switch 的节奏 |
| 5 | Huawei Ascend 910C/950 | 国产超节点/集群互联，受国内模块、DSP/TIA、EML/SiPh 供应约束 | 800G 先放量，1.6T 2027 更现实；国产替代带动海思/光迅/中际旭创/新易盛/华工/博创等链条 |
| 6 | Cambricon MLU 590/690 | 中国云/互联网客户，MLU-Link + 数据中心光模块 | 主要拉动 400G/800G，1.6T 在客户大集群中导入；低价国产 DSP/TIA 机会存在但可靠性认证较长 |
| 7 | AMD MI350 | PCIe/UBB/Infinity + Ethernet scale-out；企业和云均有需求 | 800G/1.6T Ethernet optics 与 AEC/ACC；若 MI400/Helios 2027 加速，1.6T 渗透上修 |
| 8 | AWS Trainium3 | 3nm、144 芯片 UltraServer，2026 放量初期 | 更高 rack/row 网络密度，拉动 1.6T AEC/ACC 与 Ethernet optics；CDR/retimer attach rate 上升 |
| 9 | Meta MTIA 300/400/450/500 | Broadcom XPU/以太网生态，>1GW 起步 | Broadcom DSP/SerDes/交换芯片强绑定；Meta 可能推动 1.6T DSP、LRO/LPO 和 custom optics 早期验证 |
| 10 | Microsoft Maia 200 | Azure 自研推理芯片，TSMC 3nm、HBM3E，后端网络与 Azure fabric | 以太网 scale-out、coherent DCI、AEC/ACC 同时受益；Microsoft 有多供应商策略，Marvell/Cisco/Acacia/Arista 生态机会大 |

### 1.5 新技术成熟和放量时间预测

| 技术 | 2026-05 状态 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|---|
| 800G FRO/TRO | 已规模放量 | 2026 继续增长，2027 被 1.6T 分流但保有大存量 | 价格下行但数量更高，2027 仍为二线/存量集群主力 | 因电力/交付分批，800G 与 1.6T 同时缺货到 2027H1 |
| 1.6T 200G/lane FRO | 多厂商量产/采样，2026 OFC 展示密集 | 2026H2 明显放量，2027 成 AI 新建集群默认高端配置 | 2026Q4 即进入大客户主力；2027 单年 1,500-2,500 万只模块级别 | 2026 下半年短缺延续，2027 进入 3,000 万只级别，并推高 DSP/TIA 价格 |
| TRO/LRO | Marvell/Credo 等明确产品化 | 2026 小批，2027 在 5-500m 场景 15-25% 新增 1.6T 模块采用 | 2027 渗透 30-45%，成为降功耗主力 | 2027 大客户默认配置之一，DSP 内容量从 FRO 向 TX-only/linear RX 重分配 |
| LPO | 多厂商 demo，客户仍谨慎 | 2026 pilot，2027 10-20% 短距新增端口 | 2027 25-35%，Google/Meta/ASIC 集群推动 | 2027 40%+ 短距新增端口，host SerDes/retimer/TIA 价值大幅上移 |
| AEC/ACC 1.6T | Credo/Marvell/Broadcom/MACOM/Semtech 已商业化或演示 | 2026 快速增长，2027 随 rack 内 200G/lane 扩散 | 2027 1.6T AEC/ACC 成为 rack 内标配，3.2T 进入设计 | 448G/3.2T ACC 2027 提前小批，CDR/redriver 单价维持高位 |
| 400G/lane 光 DSP / 3.2T | Broadcom Taurus 400G/lane 已发布；器件样品密集 | 2026 样品/客户验证，2027H2 小批收入，2028 规模化 | 2027H1 高端平台设计赢单，2027H2 形成 10-20 亿美元模块级早期市场 | 204.8T switch 提前，2027 3.2T optical engine/DSP/TIA 形成明显收入 |
| 448G/lane TIA/Driver | Semtech/MACOM 展示 | 2026-2027 工程验证，2028 大量 | 2027 小批量服务 3.2T/XPO/CPO | 2027 形成高 ASP 稀缺器件，TIA/Driver 毛利上修 |
| CPO/NPO/ELS | NVIDIA/Broadcom/Coherent/Marvell/Celestial AI 推进 | 2026-2027 pilot，2028 放量 | 2027 多个 hyperscaler 高端 switch design-in | 2027 高端 AI switch 默认导入之一，ELS/optical engine 成新瓶颈 |
| 1.6T coherent / coherent-lite | Marvell 2nm coherent DSP、Aquila M 等推出 | 2026H2 采样，2027 scale-across 放量 | 2027 DCI/园区 AI 网络显著增长 | 大模型跨园区训练/推理使 1.6T ZR/ZR+ 提前成为高端 DCI 主流 |

## 2. 已经开始放量的关键产品：规模、渗透率、利润率

### 2.1 建模假设

- “未来 3 个月”指 2026 年 5 月至 2026 年 7 月左右的出货/订单 run-rate。
- “未来一年”指 2026 年 5 月至 2027 年 4 月的滚动收入机会。
- “未来两年”指 2026 年 5 月至 2028 年 4 月的滚动收入机会。
- 渗透率指在 AI 数据中心新增高速互联端口/模块中的采用率，不是全球存量端口。
- 市场规模为芯片/IC 内容量；若是模块级市场会在表中注明。

### 2.2 已放量产品预测总表

| 产品/细分技术 | 2026 可验证信号 | 未来 3 个月芯片市场规模 | 未来一年芯片市场规模 | 未来两年芯片市场规模 | 渗透率路径 | 毛利率/溢价能力 |
|---|---|---:|---:|---:|---|---|
| 800G PAM4 DSP/FRO/TRO | 800GbE 2026 出货预计 >2,000 万只；Broadcom Sian2/Sian3、Marvell Spica/Nova/Ara、MaxLinear Keystone、Credo 800G | 基准 $0.45-0.70B；乐观 $0.70-0.95B；极度 $0.95-1.25B | 基准 $1.8-2.6B；乐观 $2.6-3.4B；极度 $3.4-4.2B | 基准 $2.6-3.8B；乐观 $3.8-5.0B；极度 $5.0-6.5B | 2026 新增 AI 800G/1.6T 端口中 800G 仍 45-60%；2027 降至 25-40% | DSP 芯片 GM 55-70%；成熟 800G ASP 下降，极度情景靠短缺和高端 TRO 保持 60%+ |
| 1.6T 200G/lane PAM4 DSP | Marvell Ara mass volume；Broadcom Sian3 2025Q3 ramp，Taurus/400G lane 预热；MaxLinear Rushmore、Cisco Kibo、Credo Bluebird/Cardinal | 基准 $0.30-0.55B；乐观 $0.55-0.85B；极度 $0.85-1.20B | 基准 $1.2-2.0B；乐观 $2.0-3.0B；极度 $3.0-4.2B | 基准 $2.8-4.5B；乐观 $4.5-7.0B；极度 $7.0-10.0B | 1.6T 占 800G+ 新增模块 2026 15-25%；2027 35-55%；极度 60%+ | 3nm/5nm 高端 DSP GM 60-75%；供不应求可有 5-15pct 价格溢价 |
| 200G/lane TIA + Driver | Semtech GN183x/GN1887、MACOM PURE DRIVE、MaxLinear Washington、Marvell LPO TIA/Driver | 基准 $0.22-0.40B；乐观 $0.40-0.65B；极度 $0.65-0.90B | 基准 $0.9-1.5B；乐观 $1.5-2.4B；极度 $2.4-3.4B | 基准 $1.9-3.2B；乐观 $3.2-5.0B；极度 $5.0-7.5B | 200G TIA/Driver 在 1.6T 模块 attach 接近 100%；LPO/LRO 渗透越高，线性 TIA/Driver 单价越坚挺 | 高性能模拟 IC GM 55-75%；2.5D/flip-chip TIA、低噪声线性件可享高溢价 |
| 800G/1.6T AEC/ACC CDR/retimer/redriver | Credo AEC 爆发；Marvell Alaska A 1.6T；Broadcom Agera 3；Semtech GN8234/GN8304；MACOM 1.6T ACC demo | 基准 $0.35-0.65B；乐观 $0.65-0.95B；极度 $0.95-1.35B | 基准 $1.4-2.5B；乐观 $2.5-3.8B；极度 $3.8-5.5B | 基准 $3.0-5.5B；乐观 $5.5-8.5B；极度 $8.5-13.0B | rack 内 1-6m 新增高速链路 2026 35-55% 用 active copper；2027 45-65% | Credo Q3 non-GAAP GM 68.6% 是参照；头部 retimer/CDR GM 60-75%，AEC 系统毛利 40-60% |
| 400/800ZR/ZR+ coherent DSP | Cisco/Acacia 400ZR leadership；Marvell COLORZ 800/Libra/Orion；Ciena/Nokia 800ZR+ | 基准 $0.25-0.45B；乐观 $0.45-0.70B；极度 $0.70-0.95B | 基准 $1.0-1.8B；乐观 $1.8-2.8B；极度 $2.8-4.0B | 基准 $2.2-3.8B；乐观 $3.8-6.0B；极度 $6.0-8.5B | AI scale-across 带动 800ZR/ZR+；2026 DCI 高速端口中 coherent 60%+ 带宽占比 | 相干 DSP/模块 GM 55-75%/35-50%；算法和 field data 壁垒强，价格韧性优于普通 datacom |
| 光模块内部管理/telemetry/clock recovery 辅助 IC | CMIS 5.x、PILOT/RELIANT 类遥测、PRBS/loopback/eye monitor 成为客户认证重点 | 基准 $0.08-0.15B；乐观 $0.15-0.25B；极度 $0.25-0.40B | 基准 $0.35-0.60B；乐观 $0.60-0.95B；极度 $0.95-1.40B | 基准 $0.8-1.3B；乐观 $1.3-2.0B；极度 $2.0-3.0B | 高端 800G/1.6T 模块 attach 率 60-90%，随可靠性要求上升 | 单价低但毛利可高；若绑定 DSP/retimer 平台，软件和诊断功能可加价 |

### 2.3 细分利润率判断

| 环节 | 当前毛利率估算 | 基准情景 | 乐观情景 | 极度超预期情景 |
|---|---:|---|---|---|
| 顶级 PAM4 DSP | 58-70% | 2026H2 1.6T 供需偏紧，维持 60%+ | 3nm 产能和客户 qual 约束，65-75% | 客户用长约锁货，少数 SKU 75% 附近 |
| Coherent DSP | 60-75% | 800ZR/ZR+ 放量，稳定高毛利 | 1.6T ZR/ZR+ 提前，mix 上移 | MACsec/安全/长距算法形成稀缺溢价 |
| TIA/Driver | 55-75% | 普通 100G TIA 压价，200G/线性件高毛利 | 200G/448G 稀缺，头部 65-75% | LPO/LRO 爆发导致高线性 TIA/Driver 成瓶颈 |
| AEC/ACC retimer/CDR | 60-75% 芯片，40-60% 系统 | AI rack 内 active copper 刚需，毛利稳定 | Credo/Marvell/Broadcom 持续缺货，价格强 | 3.2T/448G 提前，客户预付款与长约推高利润 |
| 光模块组装 | 25-45%；EMS 10-15% | 800G ASP 下行，毛利分化 | 1.6T mix 抵消 ASP 下行 | 关键器件缺货，优先供货商毛利短期上修 |

## 3. 在研和即将快速增长的关键产品

### 3.1 在研产品预测表

| 在研/早期技术 | 2026 状态 | 未来 3 个月市场 | 未来一年市场 | 未来两年市场 | 渗透率路径 | 毛利率/投资含义 |
|---|---|---:|---:|---:|---|---|
| 400G/lane 光 DSP / 3.2T 模块 DSP | Broadcom Taurus BCM83640 发布，3nm 1.6T 8:4 DSP，支持 1.6T 到 3.2T；Eoptolink 等展示 448G/lane transceiver | 基准 <$0.05B；乐观 $0.05-0.10B；极度 $0.10-0.20B | 基准 $0.2-0.6B；乐观 $0.6-1.4B；极度 $1.4-3.0B | 基准 $1.5-3.5B；乐观 $3.5-7.0B；极度 $7.0-12.0B | 2026 基本验证；2027 高端 switch 设计 5-15%；极度 20%+ | 早期 GM 65-80%，但良率/测试成本极高；最大受益是 Broadcom 与具备 400G optics 的光器件链 |
| 448G/lane TIA/Driver | Semtech TN622/TN14740、MACOM 448G drivers | 基准 <$0.03B；乐观 $0.03-0.08B；极度 $0.08-0.15B | 基准 $0.1-0.4B；乐观 $0.4-0.9B；极度 $0.9-1.8B | 基准 $0.8-1.8B；乐观 $1.8-3.5B；极度 $3.5-6.0B | 2027 在 3.2T/XPO/CPO optical engine 中 3-10%；极度 15% | 最高壁垒模拟 IC，性能验证先于模块量产，毛利可高于普通 TIA |
| LPO/LRO 高线性 TIA/Driver | Semtech 224G family、MACOM PURE DRIVE、Marvell light engine | 基准 $0.10-0.20B；乐观 $0.20-0.35B；极度 $0.35-0.55B | 基准 $0.5-1.0B；乐观 $1.0-1.8B；极度 $1.8-3.0B | 基准 $1.5-3.0B；乐观 $3.0-5.5B；极度 $5.5-9.0B | 2026 pilot；2027 短距 1.6T 新增端口 15-35%；极度 40%+ | LPO 减少 DSP 但抬高 TIA/Driver 和 host tuning 价值；Semtech/MACOM/Marvell/MaxLinear 受益 |
| CPO/NPO/ELS optical engine IC | NVIDIA Spectrum-X Photonics、Broadcom Tomahawk CPO、Coherent 6.4T CPO、Marvell/Celestial AI Photonic Fabric | 基准 <$0.10B；乐观 $0.10-0.25B；极度 $0.25-0.50B | 基准 $0.4-1.0B；乐观 $1.0-2.5B；极度 $2.5-5.0B | 基准 $2.0-5.0B；乐观 $5.0-10.0B；极度 $10.0-18.0B | 2026 demo/pilot；2027 高端 switch/scale-up 5-15%；极度 20% | 初期系统/封装服务成本高，但 ELS、optical engine、TIA/Driver 和 photonic chiplet 可能高 ROIC |
| Coherent-lite O-band campus DSP | Marvell Aquila/Aquila M，MACsec 版本采样 | 基准 $0.05-0.15B；乐观 $0.15-0.30B；极度 $0.30-0.50B | 基准 $0.3-0.8B；乐观 $0.8-1.5B；极度 $1.5-2.5B | 基准 $1.0-2.5B；乐观 $2.5-5.0B；极度 $5.0-8.0B | 2-20km AI campus/metro links，2027 渗透 10-25% | 相干-lite 兼具低功耗和长 reach，若 AI campus 爆发，Marvell/MACOM/Cisco 生态受益 |
| 3.2T AEC/ACC CDR/redriver | Semtech GN8304 448G ACC demo，MACOM 3.2T optical/copper roadmap | 基准 <$0.05B；乐观 $0.05-0.12B；极度 $0.12-0.25B | 基准 $0.2-0.7B；乐观 $0.7-1.5B；极度 $1.5-3.0B | 基准 $1.2-3.0B；乐观 $3.0-6.0B；极度 $6.0-10.0B | 2027 高端 rack 内短距 3-10%；极度 15% | 若铜继续延寿，CDR/retimer 是最高弹性之一；但热和线缆机械风险高 |
| OCS/MEMS optical switching 相关 IC | Google Apollo OCS；Lumentum MEMS/OCS 角色重要 | 基准 $0.05-0.15B；乐观 $0.15-0.35B；极度 $0.35-0.60B | 基准 $0.3-0.8B；乐观 $0.8-1.8B；极度 $1.8-3.5B | 基准 $1.0-2.5B；乐观 $2.5-5.0B；极度 $5.0-8.0B | TPU-like cluster 先行；2027 可扩散到更多 ASIC 集群 | OCS 本身减少电交换功耗，但放大光模块、光纤管理、监控 IC 和 MEMS 控制价值 |

### 3.2 对“未来会快速增长”的判断

1. **未来 3 个月最快增长：1.6T 200G/lane DSP、200G TIA/Driver、1.6T AEC/ACC。** 因为这些已经在 OFC 2026 进入多厂商 demo 和客户验证，且能直接服务 GB300/TPU/Trainium/ASIC 的 2026 交付。
2. **未来一年最强弹性：TRO/LRO/LPO 高线性 TIA/Driver 与 AEC/ACC CDR。** 这两类都能降低功耗、延长铜/可插拔生命周期，符合 AI rack 的电力约束。
3. **未来两年最大预期差：400G/lane DSP、448G TIA/Driver、CPO/NPO/ELS。** 这些技术 2026 还小，但一旦 204.8T switch 或高端 ASIC scale-up 提前，单价和毛利都会显著高于成熟 800G。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/能力 |
|---|---|---|---|
| PAM4 DSP 设计 | 美国、以色列、加拿大、中国 | Broadcom、Marvell、Cisco/Acacia、MaxLinear、Credo、HiSilicon/国内 PHY 团队 | 3nm/5nm/7nm CMOS，224G/400G SerDes，PAM4 DSP/FEC/telemetry |
| DSP 晶圆制造 | 台湾、韩国、美国 | TSMC、Samsung Foundry、Intel Foundry 可能承接部分先进封装/代工 | 3nm/5nm 为 1.6T 主力；MaxLinear 强调 Rushmore 完全基于 Samsung 技术，提供 second source |
| TIA/Driver 设计 | 美国、加拿大、欧洲、中国 | Semtech、MACOM、Marvell、MaxLinear、Broadcom、Coherent、Lumentum、国内模拟 IC 厂 | SiGe BiCMOS/CMOS/定制模拟工艺，flip-chip/2.5D TIA，低噪声线性化 |
| 激光/PD/光芯片 | 美国、日本、中国台湾、中国大陆、欧洲 | Broadcom、Coherent、Lumentum、AOI、ELASER、LuxNet、Sumitomo、Mitsubishi、光迅、华工 | 200G/400G EML、VCSEL、CWL、PD、SiPh PIC、InP、TFLN |
| 封装测试 | 台湾、马来西亚、泰国、中国大陆、越南、美国 | ASE、Amkor、JCET、SPIL、Fabrinet、Jabil、Foxconn/FIT、Innolight、新易盛 | 高速 BGA/裸 die、光电混合封装、光学对准、burn-in、BERT/ATE |
| 模块组装与系统验证 | 中国、泰国、马来西亚、越南、美国 | Innolight、中际旭创、新易盛、Coherent、Lumentum、Eoptolink、Fabrinet、AOI、Jabil、Hisense Broadband、光迅 | OSFP/QSFP-DD、1.6T DR8/FR8/2xDR4、LPO/LRO/TRO、CPO/NPO |
| AEC/ACC/retimer | 美国、中国台湾、中国大陆、东南亚 | Credo、Marvell、Broadcom、Astera Labs、MACOM、Semtech、Amphenol、Molex、TE、Luxshare | 200G/lane retimer/CDR/redriver、线缆 assembly、链路训练/遥测 |

### 4.2 关键瓶颈

1. **先进晶圆产能：** 1.6T DSP 普遍转向 3nm/5nm，和 AI ASIC、GPU、switch ASIC 争抢先进节点；Broadcom、Marvell、Cisco/Acacia、Credo、MaxLinear 都需要稳定先进晶圆供应。
2. **224G/400G SerDes IP 与验证：** 200G/lane 已经很难，400G/lane 需要更高线性度、更强 FEC 和更复杂测试；SerDes 团队、仿真模型、版图经验是人才瓶颈。
3. **200G/400G EML/PD/CW laser：** TrendForce 明确指出 EML 和 CW-LD 供应吃紧；Broadcom 称 200G EML/PD 已 volume shipping，但 400G EML/PD 仍是早期稀缺件。
4. **TIA-to-PD 封装寄生：** 200G/448G 下 photodiode 到 TIA 的寄生电容/电感会直接吃掉眼图余量，flip-chip、2.5D mounting、pitch 和光电共封装能力成为瓶颈。
5. **光学对准和测试时间：** 1.6T/3.2T 的通道数和 BER 要求提高，主动对准、burn-in、BERT、FEC/PRBS/eye monitor 测试时间拉长，导致“有料但出不来货”。
6. **模块散热与功耗预算：** 1.6T FRO 功耗若在 20W+，交换机前面板热密度非常高；LRO/TRO/LPO 的导入节奏取决于 host SerDes 和系统散热能否协同。
7. **客户认证和现场可靠性：** AI 集群一旦链路 flap 会影响大规模训练/推理作业，客户更看重 field data、telemetry 和故障定位能力，认证周期压缩但不能省略。
8. **长约和产能锁定：** NVIDIA、Google、Microsoft、Meta 等开始通过长期协议锁关键物料，小客户可能拿不到优先级；这会放大头部供应商议价权。
9. **出口管制与地域替代：** 中国高端 AI 集群对国产 DSP/TIA/CDR 有需求，但先进节点、EDA/IP、光器件和测试设备受限，短期更可能先在 400G/800G 起量。
10. **人才与系统协同：** DSP、模拟前端、光器件、封装、固件、模块、交换机需要联合调参，单一芯片团队难以闭环，平台型公司优势更大。

### 4.3 1.6T 模块 BOM 与利润决定因素

| BOM 环节 | 典型成本占比 | 价格/毛利决定因素 |
|---|---:|---|
| PAM4 DSP/retimer/CDR | 12-22%；LPO 中可下降到 0-8%，TRO/LRO 介于中间 | 3nm/5nm 成本、FEC/telemetry、功耗、客户认证、是否绑定 switch/NIC |
| TIA/Driver | 6-12%；LPO/LRO 中可能升至 10-16% | 线性度、噪声、带宽、封装寄生、是否支持多种 optics |
| 激光/PD/PIC | 18-30% | 200G/400G EML、CWL、SiPh PIC、InP/VCSEL 良率和产能 |
| 光学封装/FAU/透镜/隔离器 | 10-18% | 主动对准能力、良率、fiber management、可靠性 |
| PCB/connector/cage/power/MCU | 8-14% | OSFP/QSFP-DD form factor、散热、CMIS、供电 |
| 组装、测试、burn-in、良率损耗 | 15-25% | BERT/ATE 时间、返修率、客户现场失效率 |
| EMS/制造服务利润 | 8-15% | 规模、良率、客户锁定、地缘和交付能力 |

价格传导机制：

- 当 EML/CW laser 或 3nm DSP 短缺时，模块厂先提高 1.6T 报价，芯片厂通过 allocation 和长约保价。
- 当 2027 产能追上，模块 ASP 会更快下行；真正有固件、遥测、FEC、系统认证的 DSP/CDR 芯片 ASP 下行较慢。
- LPO/LRO 会把成本从模块 DSP 转移到 host ASIC/retimer/TIA/Driver，模块 ASP 下降不等于芯片总价值消失。
- 大客户用 LTA 换交期，供应商用 capacity reservation、NRE、工程支持费和绑定固件提高真实毛利。

## 5. 竞争格局与壁垒

### 5.1 市场结构估算

| 细分市场 | 头部集中度判断 | 主要玩家 | 2026 格局 |
|---|---|---|---|
| 1.6T PAM4 光 DSP | Top 5 约 80%+ | Broadcom、Marvell、Cisco/Acacia、MaxLinear、Credo | Broadcom/Marvell 技术和客户最强；MaxLinear 提供 Samsung second source；Credo/Cisco 提供多供应商弹性 |
| 800G PAM4 DSP | Top 5 约 75-85% | Broadcom、Marvell、MaxLinear、Credo、Cisco/Acacia | 成熟放量，ASP 下行；规模和客户 qual 是关键 |
| 200G TIA/Driver | Top 5 约 70-85% | Semtech、MACOM、Marvell、MaxLinear、Broadcom、Coherent/Lumentum | Semtech/MACOM 在高线性 analog 前端上存在稀缺性 |
| AEC/ACC retimer/CDR | Top 5 约 75-90% | Credo、Marvell、Broadcom、Astera、MACOM、Semtech | Credo 领先短距 AEC；Marvell/Broadcom 依靠平台；Astera 在 PCIe/CXL/SCM 强 |
| Coherent DSP | Top 4 约 70-85% | Cisco/Acacia、Marvell、Ciena、Nokia/Infinera、Huawei/ZTE | 算法、field deployment、系统客户强锁定；1.6T ZR/ZR+ 2027 加速 |
| CPO/NPO optical engine | 早期，集中度未定 | Broadcom、NVIDIA、Marvell/Celestial AI、Coherent、Cisco/Acacia、Ayar、Lightmatter、DustPhotonics/Credo、OpenLight | 2026-2027 谁拿到 hyperscaler design-in 谁锁定 3-5 年路线 |

### 5.2 可量化壁垒与“为什么能定价”

| 壁垒 | 量化/事实锚 | 为什么能定价 |
|---|---|---|
| 先进节点和 SerDes | 1.6T DSP 已进入 3nm/5nm；PCIe 8.0-class 256GT/s、400G/lane 都在 pathfinding | 客户不愿为每个平台重新验证 PHY；谁能先跑稳定，谁可拿高 ASP 和长约 |
| FEC/BER/遥测算法 | 1.6T AI 链路需要低 flap、SNR/eye/FEC/BER 实时监控 | AI 训练/推理集群链路故障代价远高于芯片差价，可靠性可直接定价 |
| 多供应商互操作 | OIF/IEEE/CMIS/OSFP/800GAUI/CEI-224G 认证周期长 | 模块厂和云厂愿意为“少踩坑、快上线”付工程溢价 |
| 客户现场数据 | Broadcom 200G VCSEL 称有 >5 万亿 field device hours、<1 FIT；Acacia 有大量 400G/800G coherent 端口数据 | field reliability 是最难复制的资产，新进入者很难靠低价替代 |
| 供应链锁定 | Broadcom Q1 FY2026 AI revenue 84 亿美元，客户通过多年协议锁晶圆/HBM/基板；Credo 也进入大客户 active copper 长约 | 供应短缺时，能保证交付比低价更重要 |
| 系统级组合 | Broadcom/Marvell 同时有 switch/NIC/SerDes/DSP/retimer/optics；Cisco/Acacia 有系统和 coherent | 客户采购的不只是芯片，而是 reference architecture、debug 资源和 roadmap |
| 封装与模拟能力 | 2.5D TIA、flip-chip、448G driver 对寄生极敏感 | 设计图纸之外的制程经验决定良率，低价竞争者难以复制 |
| 软件和固件 | Marvell RELIANT、Credo PILOT、DSP telemetry/diagnostics | 固件持续升级可延长产品生命周期，提高客户粘性 |

### 5.3 长期高 ROIC/高毛利最可能在哪一层

1. **第一层：SerDes/DSP/CDR 平台。** Broadcom、Marvell、Cisco/Acacia、Credo、MaxLinear 这层毛利最高，客户认证最重，且通过固件、算法和遥测形成长期锁定。
2. **第二层：高端 TIA/Driver 与 optical engine。** Semtech、MACOM、Marvell、Coherent、Lumentum 在 200G/448G、LPO/LRO/CPO 中有强壁垒；如果 LPO 扩散，价值反而向这层转移。
3. **第三层：相干 DSP 与 DCI 系统。** Cisco/Acacia、Marvell、Ciena、Nokia 受益于 AI scale-across，生命周期长、客户切换慢。
4. **第四层：模块组装与 EMS。** 收入规模大，但长期毛利取决于客户集中度、良率、器件自供能力和是否有硅光/激光器优势。纯组装 ROIC 通常低于芯片层。

## 6. 2026 年关键变化：3 个拐点与最可能放量子方向

### 拐点一：1.6T 从样品/展示进入大客户规模采购

证据链：Marvell 称 Ara 已 mass volume，1.6T solutions 在 FY2026 Q4 进入 production；Broadcom Sian3 生产 ramp、Taurus 发布；MaxLinear Rushmore、Cisco Kibo、Credo Cardinal/Bluebird、Semtech 1.6T demo 都集中在 OFC 2026。  
最可能放量：1.6T FRO/TRO DSP、200G/lane TIA/Driver、1.6T OSFP DR8/2xDR4、1.6T AEC/ACC。

### 拐点二：LRO/TRO/LPO 让“DSP 内容量”从简单增加转为重新分配

2026 年客户的痛点不只是带宽，而是每个 OSFP 的功耗和前面板散热。TRO/LRO 以较低风险降低功耗，LPO 则更激进。  
最可能放量：TRO DSP、LRO DSP、CEI-224G-Linear TIA/Driver、host-side retimer/CDR、module telemetry。

### 拐点三：AI scale-across 把 coherent DSP 拉回高增长

当单园区电力受限，AI workload 要跨 campus/metro/regional 数据中心协同，800ZR/1.6T ZR/ZR+ 和 coherent-lite 会成为新的高毛利连接层。  
最可能放量：800ZR/ZR+ coherent DSP、1.6T ZR/ZR+ 早期采样、O-band coherent-lite、MACsec coherent DSP。

## 7. 2027 年关键变化：3 个拐点与最可能放量子方向

### 拐点一：3.2T/400G-per-lane 从工程验证进入高端设计赢单

Broadcom Taurus 400G/lane、Semtech/MACOM 448G TIA/Driver、Coherent/OpenLight 400G/lane 光链路会在 2027 年由“展示”转为“平台设计”。  
最可能放量：400G/lane optical DSP、448G driver/TIA、3.2T optical engines、204.8T switch 配套测试设备。

### 拐点二：CPO/NPO/ELS 从少数 demo 进入 hyperscaler pilot

2027 年如果 102.4T/204.8T switch 前面板功耗过高，CPO/NPO 会在高端 AI fabric 中提前。  
最可能放量：socketed CPO、external laser source、NPO optical engine、CPO TIA/Driver、photonic chiplet、high-density fiber management。

### 拐点三：开放 scale-up 与自研 ASIC 扩张，削弱单一 NVLink 路线

AWS Trainium3/4、Google TPU8、Meta MTIA、Microsoft Maia、AMD Helios/MI400 都会推动 Ethernet/UALink/自研 fabric 的高速连接需求。  
最可能放量：1.6T/3.2T AEC/ACC、Ethernet retimer/CDR、coherent-lite campus links、LPO/LRO 在非 NVIDIA rack 的设计导入。

## 8. 头部公司与细分清单

### 8.1 PAM4 光 DSP

| 公司 | 代表产品/路线 | 竞争点 |
|---|---|---|
| Broadcom | Sian3/Sian2M、Taurus BCM83640、200G/400G optical DSP | 3nm/5nm、200G/400G lane、switch/NIC/SerDes 一体化，Meta/Google/云厂生态强 |
| Marvell | Nova、Ara、Ara T、Ara X、Petra、Aquila M | 1.6T mass volume、TRO/LRO/gearbox/coherent-lite 全覆盖，TIA/driver/light engine 配套 |
| Cisco/Acacia | Kibo 1.6T PAM4 DSP、coherent DSP | 3nm Kibo sampling，coherent 端口数据和系统客户强 |
| MaxLinear | Rushmore 1.6T、Keystone 400G/800G、Washington TIA | Samsung advanced node second source，Keystone millions shipped，Rushmore sub-25W |
| Credo | Bluebird、Cardinal 800、Cardinal family | 低功耗 224G/lane、LRO/FRO、sub-40ns latency、AEC 客户基础 |
| Huawei/HiSilicon/国内 PHY 厂 | 800G/1.6T 国产 DSP 路线 | 国产替代需求强，但先进节点和客户认证是关键 |
| Alphawave Semi、Synopsys、Cadence、Rambus | SerDes/PHY/IP | 不一定卖完整 DSP，但在 224G/448G PHY/IP 中价值高 |

### 8.2 TIA、Driver、模拟前端

| 公司 | 代表产品/路线 | 竞争点 |
|---|---|---|
| Semtech | GN1832/GN1834/GN1834D/GN1836/GN1838DL TIA，GN1887/GN1878/GN1877 Driver，TN622/TN14740 448G | 200G/224G 线性 TIA/Driver，2.5D TIA，LPO/LRO/CPO/XPO 全覆盖 |
| MACOM | PURE DRIVE TIA/Driver、200G/448G modulator drivers、ACC/equalizer | LPO/ACC/retimed optics 生态，模拟和微波经验深 |
| Marvell | LPO TIA/laser driver chipset、Silicon Photonics Light Engine | DSP + TIA/Driver + SiPh + telemetry 平台化 |
| MaxLinear | Washington 224G TIA | 与 Rushmore DSP 配套，提供 1.6T PHY chipset |
| Broadcom | 200G/400G EML/PD、VCSEL、集成 driver DSP | 光器件 + DSP 一体化，200G EML/PD volume shipping |
| Coherent | InP/SiPh/VCSEL、CPO optical engine、400G/lane modulator | 光器件和模块垂直能力强 |
| Lumentum | EML、CW laser、ELS、OCS/MEMS 相关 | 高功率 laser/ELS 和 OCS 供应链关键 |
| AOI、三安、光迅、华工、仕佳光子、源杰科技、长光华芯 | 激光器/PD/部分模拟前端 | 国产与区域替代，受益于 EML/CW laser 紧张 |

### 8.3 CDR、retimer、redriver、AEC/ACC

| 公司 | 代表产品/路线 | 竞争点 |
|---|---|---|
| Credo | ZeroFlap AEC、retimers、PILOT diagnostics、Bluebird/Cardinal | AEC 领先，FY2026 高增长，高毛利，收购 DustPhotonics 补 SiPh |
| Broadcom | Agera 3 200G/lane retimer、AEC、PCIe Gen6 retimer | 与 switch/NIC/optics 联动，客户平台绑定强 |
| Marvell | Alaska A 1.6T AEC retimer、PCIe 8.0 SerDes、CXL/Structera | 200G PAM4 DSP retimer，40dB insertion loss，>3m copper |
| Astera Labs | Aries PCIe/CXL retimer、Taurus Ethernet Smart Cable Modules、Scorpio switches | PCIe/CXL/AI rack smart cable 强，Amazon 关系和软件能力 |
| MACOM | 1.6T ACC、onboard equalization、CDR/OCR | 高速模拟 equalization 与 copper/optical 双线 |
| Semtech | GN8234/GN8304 redriver、Tri-Edge CDR、ClearEdge | 1.6T ACC 和 3.2T/448G redriver demo |
| MaxLinear | Rushmore electrical DSP/AEC applications | DSP + electrical validation，Samsung second source |
| Parade、Montage、Kandou、Spectra7、Analog Devices、TI | PCIe/USB/以太网 retimer/redriver/linear driver | 部分进入 AI rack 周边，高速标准升级受益 |

### 8.4 相干 DSP、coherent-lite 与 DCI

| 公司 | 代表路线 | 竞争点 |
|---|---|---|
| Cisco/Acacia | Greylock、Delphi、Jannu、Kibo、800G ZR+ | coherent port share、系统客户、400G/800G 现场数据 |
| Marvell | COLORZ 800/1600、Orion、Libra、Electra 2nm、Aquila/Aquila M | 1.6T ZR/ZR+、2nm coherent DSP、MACsec、coherent-lite |
| Ciena | WaveLogic、1600ZR/ZR+、Vesta CPX、Hyper-rail | DCI/transport 系统强，AI scale-across 直接受益 |
| Nokia/Infinera | ICE/PSE/DSP、1.6T/2.4T/3.2T coherent-lite/embedded | Infinera 并入后 coherent portfolio 扩张 |
| Huawei、ZTE、Fujitsu、NEC、NTT Electronics | coherent DSP/transport | 中国/日本/运营商和长距网络市场 |

### 8.5 光模块、硅光、CPO/NPO、模块制造

| 细分 | 公司 |
|---|---|
| AI 高速模块 | Innolight/中际旭创、新易盛/Eoptolink、Coherent、Lumentum、AOI、Fabrinet、Jabil、Foxconn/FIT、Hisense Broadband、光迅、华工、博创、索尔思 |
| 硅光/PIC | Intel Silicon Photonics、Marvell、Cisco/Acacia、DustPhotonics/Credo、Coherent、OpenLight、Ayar Labs、Lightmatter、POET、Ranovus、Scintil、Enosemi、Sivers、GlobalFoundries SiPh ecosystem |
| CPO/NPO/ELS | Broadcom、NVIDIA、Marvell/Celestial AI、Coherent、Lumentum、Cisco/Acacia、Ayar Labs、Molex、Samtec、TeraHop、Open CPX MSA 成员 |
| 连接器/线缆/高密互联 | Amphenol、TE Connectivity、Molex、Samtec、Luxshare、BizLink、FIT、Hirose、Senko、US Conec、Corning |
| 测试 | Keysight、VIAVI、Anritsu、Rohde & Schwarz、Tektronix、Teledyne LeCroy、FormFactor、Advantest、Teradyne |

## 9. 投资价值判断与跟踪指标

### 9.1 最值得跟踪的 10 个指标

| 指标 | 为什么重要 |
|---|---|
| 1.6T 模块季度出货量是否超过 Cignal 2026 >500 万只全年路径 | 决定 1.6T DSP/TIA 真实放量斜率 |
| 800G+ 模块出货占比是否按 TrendForce 到 2026 超过 60% | 验证 AI DC 是否将高速光模块标准化 |
| Broadcom AI networking 占 AI revenue 比例 | 判断 DSP/switch/retimer 是否在 AI 半导体收入中继续扩张 |
| Marvell 1.6T PAM revenue 与 interconnect growth | 判断 Ara/Aquila/Alaska 是否超预期 |
| Credo AEC/optical revenue 和毛利 | 判断 active copper 和 optical DSP 是否持续供不应求 |
| Semtech/MACOM 200G/448G TIA/Driver design win | 判断 LPO/LRO/CPO 是否真的把价值转给 analog 前端 |
| EML/CW laser 交期和价格 | 这是 1.6T 扩产最显性瓶颈之一 |
| NVIDIA/Google/Meta/Microsoft/AWS 的网络架构公告 | 大客户采用 OCS/LPO/CPO 会重排价值链 |
| 3.2T/400G lane 的客户 qual 时间 | 判断 2027 是否出现第二增长曲线 |
| 模块 ASP 与芯片 ASP 剪刀差 | 判断光模块利润是否被价格战压缩而芯片层仍保持 |

### 9.2 投资结论

- **确定性最高：Broadcom、Marvell、Cisco/Acacia。** 它们掌握 DSP/SerDes/retimer/switch/coherent 的系统能力，能把 AI 网络从单芯片卖成平台。
- **弹性最高：Credo、MaxLinear、Semtech、MACOM。** Credo 直接受益 AEC/retimer 和 optical DSP；MaxLinear 若 Rushmore 作为 Samsung second source 被大客户采用，弹性大；Semtech/MACOM 是 LPO/LRO/448G analog 前端的核心受益者。
- **供应瓶颈受益：Coherent、Lumentum、AOI、ELASER、LuxNet、中国 EML/SiPh/模块链。** 2026 年 EML、CW laser、光学对准和高端模块产能紧，供应链强者有定价权。
- **中国产业链机会：中际旭创、新易盛、光迅、华工、海信宽带、博创、仕佳光子、源杰科技、三安光电等。** 机会来自全球 800G/1.6T 模块增量和国产 AI 集群替代，但风险是客户集中、出口管制和 2027 ASP 下行。
- **最大风险：模块 ASP 快速下行、CPO/LPO 路线变化快于预期、单一大客户订单延期、3nm DSP 晶圆紧张、EML/CW laser 产能扩张后过剩。** 但在 2026 极度乐观 AI capex 情景下，前两年的主矛盾仍是交付而非需求。

## 10. 关键事实与来源链接

| 主题 | 关键事实 | 来源 |
|---|---|---|
| AI 光模块规模 | 2026 全球 AI 专用光收发模块预计 **260 亿美元**，2025 为 **165 亿美元**，同比 **57%+**；EML、CW-LD、光学对准、功耗散热是瓶颈 | [TrendForce 中文稿](https://www.trendforce.cn/presscenter/news/20260420-13018.html) |
| 800G+ 渗透率 | 800G 及以上模块出货占比从 2024 年 **19.5%**升至 2026 年 **60%+**；Google 2026 近 400 万 TPU 对应 **600 万只以上** 800G+ 模块；OCS 单机约 100W vs 传统 3,000W | [TrendForce Google/Ironwood](https://www.trendforce.com/presscenter/news/20260210-12919.html) |
| 光组件规模 | 2025 optical component 近 **250 亿美元**；datacom revenue **>180 亿美元**；coherent module 近 **60 亿美元**；2025 年 400G+ 模块 **4,200 万只**，2026 年 1.6T **>500 万只** | [Cignal AI](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/) |
| Broadcom AI 收入 | Q1 FY2026 AI revenue **84 亿美元**，同比 **106%**；Q2 AI semiconductor revenue 指引 **107 亿美元** | [Broadcom SEC 8-K](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm) |
| Broadcom OFC 2026 | 展示 3.5D XPU、102.4T Ethernet switch with CPO、400G/lane optical DSP、200G/lane retimers/AEC、PCIe Gen6 retimers | [Broadcom OFC 2026](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai) |
| Broadcom Taurus | Taurus BCM83640：3nm monolithic 1.6T 8:4 PAM4 DSP，integrated laser driver，支持 1.6T 到 3.2T；LightCounting 评论未来五年 1.6T/3.2T transceivers **1 亿只+** | [Broadcom Taurus](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next) |
| Broadcom Sian3/Sian2M | Sian3 3nm 200G/lane PAM4 DSP，sub-23W 1.6T；Sian2M 5nm 200G/lane with VCSEL driver；200G EML/PD volume shipping | [Broadcom Sian3](https://investors.broadcom.com/news-releases/news-release-details/broadcom-extends-200glane-dsp-phy-leadership-next-generation-ai) |
| Marvell 1.6T | Ara 已 mass volume；Ara T、Ara X、Petra、Aquila M Q1 2026 sampling；portfolio 包括 DSP、SerDes、switching、drivers、TIAs、telemetry | [Marvell 1.6T DSP portfolio](https://www.marvell.com/company/newsroom/marvell-1-6t-optical-dsp-ai-data-center-connectivity.html) |
| Marvell OFC 2026 | OFC 2026 展示 20+ demos；Ara T、Ara 1.6T、Photonic Fabric、Teralynx、COLORZ、RELIANT | [Marvell OFC 2026](https://www.marvell.com/company/newsroom/marvell-ai-data-center-connectivity-ofc-2026.html) |
| Marvell TRO | Ara T 1.6T transmit-only DSP，5-500m，模块功耗可降低 **35%+**；TIA 处理接收侧 | [Marvell Ara T blog](https://www.marvell.com/blogs/ara-t-improving-ai-roi-with-dsps.html) |
| Marvell AEC | Alaska A 1.6T AEC retimer：8x200G，40dB insertion loss，>3m copper，FEC/SNR/eye monitor | [Marvell Alaska A product brief](https://www.marvell.com/content/dam/marvell/en/public-collateral/phys-transceivers/marvell-alaska-a-1-6t-pam4-dsp-product-brief.pdf) |
| MaxLinear | Rushmore 1.6T DSP + Washington 224G TIA；Rushmore 是首个完全基于 Samsung 技术的 major high-speed DSP；Keystone 已出货 millions | [MaxLinear OFC 2026](https://www.maxlinear.com/news/press-releases/2026/maxlinear-to-showcase-next%E2%80%91generation-1-6t-rushmore-dsp-live-at-ofc-2026) |
| Cisco/Acacia | Kibo 3nm 1.6T PAM4 DSP sampling，1.6T 模块功耗较现有实现低 20%，支持 TRO/gearbox/retimer | [Acacia Kibo at OFC](https://www.ofcconference.org/news-media/exhibitor-news/blog-acacia-samples-1-6t-pam4-dsp-for-scaling-ai-architectures/) |
| Acacia coherent | coherent port shipments：100k Jannu、750k 400G Greylock、25k 800G Delphi；Kibo 3nm 1.6T PAM4 demo | [Acacia OFC 2026](https://www.ofcconference.org/news-media/exhibitor-news/blog-acacia-demonstrates-coherent-technology-market-leadership-at-ofc-2026/) |
| Semtech 224G TIA/Driver | GN1834L/GN1834DL/GN1838DL TIA，GN1877/GN1887 Driver；CEI-224G-Linear/LPO-MSA，支持 LPO/NPO/CPO/XPO | [Semtech 224G IC family](https://www.semtech.com/company/press/semtech-launches-224-gbps-ic-family-for-linear-optics-era) |
| Semtech TIA | GN1834D 200G TIA for 1.6T，GN1818 100G TIA power reduction up to 20%；Cignal 引用 high-speed datacom transceiver market 2024 **90 亿美元**到 2026 **170 亿美元+** | [Semtech 1.6T TIAs](https://www.semtech.com/company/press/semtech-unveils-high-performance-tias-for-1.6t-ai-data-centers) |
| Semtech OFC 2026 | NVIDIA 1.6T DR8 OSFP transceiver powered by Semtech GN1834D TIA/GN187N1 driver；multi-vendor 1.6T FRO/LRO/LPO；448G TN622/TN14740 demo | [Semtech OFC 2026](https://www.semtech.com/company/press/showcases-ai-interconnect-leadership-with-live-1.6t-demos-ofc-2026) |
| MACOM | OFC 2026 展示 3.2T optical transmit、1.6T retimed optics/ACC/LPO、800G LR2 coherent-lite、75/100mW CW laser、onboard equalization | [MACOM OFC 2026](https://www.macom.com/updates/news/2026/macom-to-showcase-innovative-connectivity-solutions-at-ofc-2026) |
| Credo Bluebird | Bluebird 224Gbps/lane PAM4 DSP，支持 800G/1.6T，full DSP 与 LRO variants | [Credo Bluebird](https://credosemi.com/products/optical-dsp/bluebird/) |
| Credo Cardinal | Cardinal 3nm 224G/lane optical DSP，1.6T modules below 22W，sub-40ns latency；Cardinal family LRO 可低于 15W | [Credo Cardinal product brief](https://credosemi.com/wp-content/uploads/Cardinal.800.Product-Brief.3.23.2026.pdf)、[Credo Cardinal release](https://s205.q4cdn.com/511065572/files/doc_news/Credo-Introduces-Cardinal-A-LowPower-1-6T-Optical-DSP-Family-Engineered-for-MassiveScale-AI-Fabrics-2026.pdf) |
| Credo 财务 | Q3 FY2026 revenue **4.07 亿美元**，QoQ +51.9%，YoY +201.5%，non-GAAP GM **68.6%**；Q4 revenue guide **4.25-4.35 亿美元** | [Credo SEC 8-K](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm) |
| Credo 收购 DustPhotonics | 收购 DustPhotonics，补足 SiPh PIC；portfolio 覆盖 400G/800G/1.6T，roadmap 到 3.2T；目标 FY2027 optical revenue **>5 亿美元** | [Credo SEC 8-K DustPhotonics](https://www.sec.gov/Archives/edgar/data/1807794/000162828026024892/april20268-kex991.htm)、[TrendForce](https://www.trendforce.com/news/2026/04/17/news-ma-in-optical-communications-field-credo-to-acquire-dustphotonics/) |
| Coherent 财务 | Q3 FY2026 revenue **18.06 亿美元**，同比 +20.5%，non-GAAP GM **39.6%**；公司称 AI datacenter 需求强并扩产 | [Coherent Q3 FY2026](https://www.coherent.com/content/dam/coherent/site/en/documents/investors/financial-releases/2026/may-6/earnings-release-fy26-q3.pdf) |
| Marvell 财务/展望 | FY2027 data center revenue 预计 +40%，interconnect +50%+；1.6T revenue FY2027 快速 ramp，FY2028 继续增长；1.6T coherent DSP later 2026 sampling | [Marvell Q4 FY2026 transcript](https://www.fool.com/earnings/call-transcripts/2026/03/05/marvell-mrvl-q4-2026-earnings-call-transcript/) |
| LightCounting 芯片市场 | 光通信 IC chipset 从 2022 年约 **26 亿美元**到 2028 年近 **70 亿美元**，CAGR 18%；800G/1.6T Ethernet transceivers、AOC/AEC 拉动 PAM4 DSP | [Fibre Systems / LightCounting](https://www.fibre-systems.com/news/ic-chipset-sales-double-2028-says-lightcounting) |

## 11. 读数注意事项

1. 本报告对“光 DSP、TIA、CDR”采用宽口径：包含 driver、retimer、redriver、AEC/ACC 中承担 CDR/均衡/重定时的 IC。若只看狭义“光模块内 DSP + TIA”，市场规模应下调约 25-40%。
2. 2026-2027 的高端 AI 光互联需求有大量客户长约和路线图信息，但各公司很少披露单项芯片 ASP 与出货；表格中的芯片市场规模为基于模块出货、ASP、BOM 占比和公司收入的估算。
3. LPO/LRO/TRO 的渗透率不会线性替代 FRO。大型云厂会按距离、功耗、可靠性、可维护性、供应链和 host SerDes 能力分层部署。
4. 极度超预期情景的核心假设是：AI 推理 token 需求继续指数增长，GB300/TPU/Trainium/MTIA/Maia/MI350 交付不被电力和 HBM 严重拖慢，且客户愿意为网络瓶颈支付溢价。
5. 非投资建议。本报告用于产业链研究和情景分析，实际投资需结合估值、订单兑现、客户集中度、库存周期和政策风险。
# 行业调研：【激光器、EML与光器件】

版本日期：2026-05-08  
研究范围：AI 数据中心相关激光器、EML、VCSEL、CW/ELS 光源、硅光 PIC、光模块、CPO/NPO/CPX、OCS、coherent DCI、光纤与高密连接件。  
预测口径：除特别注明外，市场规模为“全球 AI 数据中心相关年度收入池/订单池”，不是单家公司收入；“未来 3 个月”按 2026Q2-Q3 年化运行率理解，“未来 1 年/2 年”分别指 2027Q2/2028Q2 附近的年化收入池。  
情景口径：基准 = 需求强但供给/认证/电力仍约束；乐观 = hyperscaler 公告按计划转订单；极度超预期乐观 = 推理需求继续吃掉全部新增 GPU/ASIC、电力、光互联产能，短缺溢价延续。

## 0. 高浓度结论

1. 2026 年 AI 光互联已经从“800G 光模块放量”升级为“系统架构重写”。OFC 2026 的核心不是单纯从 800G 到 1.6T，而是 1.6T pluggable、CPO/CPX/NPO、OCS、XPO、coherent scale-across 同时进入客户设计窗口。
2. 公开数字最硬的三条：TrendForce 预计 800G 及以上光收发模块出货占比从 2024 年 19.5% 升至 2026 年 60%+；Cignal AI 公开摘要显示 2025 年 400G+ datacom 模块出货约 4,200 万只、2026 年 800G 超 2,000 万只、1.6T 超 500 万只；Broadcom 引用 LightCounting 称未来五年 1.6T/3.2T 光收发器出货超过 1 亿只，接近一半使用 400G optics。
3. NVIDIA 已经用资本和订单锁定光器件供应链：2026-03-02 分别与 Lumentum、Coherent 签多年度协议并各投资 $2B，包含多十亿美元采购承诺和先进 laser/optical networking 产能访问权；2026-03-31 投资 Marvell $2B 并推进 NVLink Fusion/硅光；2026-05-06 与 Corning 合作，把美国 optical connectivity 产能扩 10x、fiber 产能扩 50%+、建设 3 座新厂。
4. 2026 最可能放量的技术路径：800G/1.6T OSFP 可插拔模块仍是主线，底层是 200G/lane 或早期 400G/lane，光源和调制路线并行：InP EML、硅光 PIC + InP CW laser、GaAs/1060nm VCSEL、coherent DSP。CPO 是高端交换机试点，2026 不会大面积替代 pluggable。
5. 2027 的关键变化：1.6T 从短缺导入转为主流 AI fabric；3.2T/400G-per-lane 进入客户 qual 和小批量收入；CPO/CPX/NPO 与 XPO 同时争夺 204.8T switch 以后形态；1600ZR/ZR+、coherent-lite、multi-rail line system 在 AI scale-across 中放量。
6. 最有长期定价权的不是普通模块组装，而是上游高壁垒器件：200G/400G InP EML、CW/ELS 高功率激光器、硅光 PIC、coherent/optical DSP、224G/448G SerDes、CPO 光引擎、高端测试。模块厂 β 高，但 2026H2-2027 可能出现 ASP 下行。
7. Lumentum Q3 FY26 收入 $808.4M，同比 +90%，non-GAAP GM 47.9%；components 收入 $533.3M，同比 +77%，100G/200G EML 出货创新高，200G EML 收入环比翻倍以上，1.6T transceiver 计划 Q4 FY26 ramp。Coherent Q3 FY26 收入 $1.81B，同比 +21%，non-GAAP GM 39.6%，Datacenter & Communications 收入 $1.362B，称年底 internal InP output 翻倍、2027 再翻倍以上。AAOI Q1 2026 已完成 800G 首个 hyperscale 客户 volume shipment，退出 Q1 时 800G transceiver 月产能接近 10 万只。
8. 我的三情景总判断：AI 光互联/光器件订单池 2026 基准 $55-85B、乐观 $85-125B、极度乐观 $125-180B；2027 基准 $90-150B、乐观 $150-230B、极度乐观 $230-360B。其中光模块是最大美元池，激光器/EML/硅光/光引擎是利润率和瓶颈更好的池。

## 1. AI 芯片路线背景下的行业机遇、挑战与技术路径

### 1.1 2026 机遇

AI 集群扩张把光器件从服务器外围件变成算力交付瓶颈。项目内已有 AI 芯片报告显示，2026-2027 出货价值和数量最大的加速器平台包括 NVIDIA GB300/B300、AWS Trainium2/3、Google TPU v7 Ironwood、NVIDIA GB200/B200、Huawei Ascend 910C/950、Cambricon MLU、AMD MI350、Meta MTIA、Microsoft Maia 200 等。它们的共同点不是都使用同一种互连协议，而是都把 scale-out 网络推向 800G/1.6T，且在跨机柜、跨园区、跨 region 时快速增加光纤、光模块和 coherent DCI 消耗。

| 芯片/平台 | 2026-2027 出货逻辑 | 对光互联的直接拉动 | 2026 最可能采用的光路径 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主力，GB300 NVL72 大规模交付 | rack 内 NVLink/铜为主，scale-out 用 800G/1.6T；Rubin/Spectrum-6 引出 CPO | 800G/1.6T OSFP + Spectrum-X/InfiniBand；CPO 先在 switch 侧 pilot |
| AWS Trainium2 | Project Rainier 近 50 万颗，Anthropic 目标 >100 万颗 | EFA/以太网 scale-out，超大集群带来大量 optics；rack 内 NeuronLink | 800G 先行，1.6T 在新区域逐步导入 |
| Google TPU v7 Ironwood | 3D Torus + Apollo OCS，Google/Anthropic TPU 扩容 | TrendForce 称 Google 2026 约 400 万 TPU 可带来 >600 万只 800G+ 光模块需求 | 短距铜、跨机柜全光网络、OCS、800G/1.6T |
| NVIDIA GB200/B200 | 存量和成本敏感客户延续 | 800G 继续吃量，部分新集群转 1.6T | 800G pluggable 主流 |
| Huawei Ascend 910C/950 | 中国国产替代第一梯队 | 国产 400G/800G/1.6T 光模块和光芯片需求上行 | 400G/800G 优先，1.6T 在头部集群导入 |
| Cambricon MLU 590/690 | 2026 目标约 50 万颗级别 | MLU-Link + 数据中心光模块，国内光模块链受益 | 400G/800G 为主，1.6T 取决于客户集群规模 |
| AMD MI350/MI400 | MI350 2026 放量，MI400/Helios 2026H2 初期 | Ethernet/UALink scale-out，Meta/Oracle/主权 AI 带动开放以太网光互联 | 800G/1.6T pluggable；OCI optical scale-up 进入路线图 |
| AWS Trainium3 | 144 芯片 UltraServer，2027 主力 | 机架级/跨机架 fabric 更密，光链路随集群扩大 | 800G 到 1.6T 过渡 |
| Meta MTIA/Broadcom XPU | >1GW 首期、多 GW 计划 | Broadcom Ethernet/SerDes/Optical Connectivity 强绑定，未来 OCI/CPO 可接入 | 800G/1.6T + Broadcom switching/optics |
| Microsoft Maia 200 | Azure 推理自研芯片，3nm/HBM3E | Azure 后端网络与 scale-up interconnect 带动 optics | 800G/1.6T pluggable，OCI/光 scale-up 中期导入 |

### 1.2 2026 挑战

1. 供给瓶颈从“能否组装模块”转向 200G/400G EML、CW/ELS、SiPh PIC、DSP、TIA/driver、224G SerDes、主动耦合和测试时间。
2. 1.6T 早期短缺与 800G 后期价格竞争并存。AI 需求强不等于所有模块厂毛利率都升，进入 2026H2 后需防 ASP 追降。
3. CPO 商业化难点不是实验室带宽，而是 laser redundancy、field replacement、thermal drift、良率、系统级责任归属和多供应商标准。
4. 电力和液冷会影响光模块订单确认节奏：GPU/ASIC 已订但机房未上电时，光模块可能被拉货后延后消化。
5. 地缘政治会改变份额：美国客户锁 Lumentum/Coherent/Corning/Marvell，Google 等仍大量依赖中国模块厂，供应链会走向“双源+本土化+关键器件锁定”。

### 1.3 新技术成熟与放量时间表

| 技术 | 2026-05 状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|---|
| 800G pluggable | 已主流，AI 集群标准件 | 2026 继续放量，2027 仍有大体量但 ASP 下行 | 2026H2 出货高位延续 | 与 1.6T 同时短缺，ASP 下行慢 |
| 1.6T pluggable | 多厂商样机/初期量产；Cignal 预计 2026 >500 万只 | 2026H2 ramp，2027 主流，2028 成熟竞争 | 2027H1 成为新建 AI 集群默认 | 2027 出货 3,000 万只级别，短缺延续 |
| 200G/lane EML/CW/VCSEL | Lumentum/Coherent/Broadcom/中国模块厂均布局 | 2026 主力器件，2027 产能扩散 | 2026H2 短缺，2027 仍高溢价 | 被 1.6T/OCS/CPO 同时拉动，毛利率继续上修 |
| 400G/lane EML/EAM/MZM | Broadcom Taurus、Coherent 400G EML/SiPh link | 2026 样品，2027 qual，2028 放量 | 2027H2 小批量收入 | 2027 形成 $1B+ 器件/DSP 市场 |
| 3.2T pluggable | 2026 多为 link/PIC/DSP/eval board | 2027 demo/qual，2028 放量 | 2027H2 小规模商用 | 204.8T switch 提前，2027 即 $3B+ |
| CPO/CPX/NPO/ELS | NVIDIA/Broadcom/Coherent/Lumentum 推进，Open CPX/OCI 标准化 | 2026-2027 pilot，2028 扩大 | 2027H2 高端 switch 商用 | 2027 成为高端 AI switch 默认路线之一 |
| XPO 12.8T 液冷 pluggable | Arista MSA，12.8T/400W/204.8T per RU | 2027 小批量验证，2028 配 204.8T switch | 2027H2 高端 AI fabric 导入 | 2027 形成 $2B+ 新形态市场 |
| OCS/MEMS 光交换 | Google Apollo 架构最明确 | Google/少数自研集群 2026-2027 先用 | 2027 更多 TPU-like cluster 采用 | 以太网 GPU fabric 也吸收 OCS |
| 1600ZR/ZR+/coherent-lite | Marvell 2026H2 采样，Ciena/Nokia 2nm coherent | 2027 采样/初量，2028 规模化 | 2027H2 scale-across 显著放量 | campus/metro AI DCI 爆发，提前成为瓶颈 |

## 2. 已开始放量的关键产品：市场规模、渗透率与利润率

### 2.1 已放量产品总表

| 产品/技术 | 2026-05 关键事实 | 未来 3 个月市场/渗透 | 未来 1 年市场/渗透 | 未来 2 年市场/渗透 | 收入增速区间：基准/乐观/极度乐观 | 毛利率判断：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---:|---|
| 800G pluggable 光模块 | 2026 AI 集群主流；Cignal 预计 2026 800G >2,000 万只 | $14-22B；新增 AI 高速端口 45-60% | $15-26B；35-50% | $12-24B；25-40% | +15-30% / +30-45% / +50% | 模块 23-35% / 28-40% / 35-45%；EMS 10-14% |
| 1.6T pluggable 光模块 | Cignal 预计 2026 >500 万只；Lumentum Q4 FY26 ramp；Coherent 多路线演示 | $4-9B；8-15% | $18-38B；25-45% | $32-75B；35-65% | +80-120% / +120-180% / +200%+ | 早期 35-48%；2027 基准 30-42%，极度乐观 42-55% |
| 200G InP EML / PD / driver-TIA | Lumentum 100G/200G EML 出货创新高，200G EML 收入环比翻倍以上 | $2.5-4.5B；1.6T 光引擎 30-45% | $5-10B；45-65% | $7-15B；40-60% | +50-80% / +80-120% / +150% | 器件 45-60% / 50-65% / 55-70% |
| InP CW/UHP/SHP/ELS 光源 | Lumentum 1310nm SHP >1W@25C、>800mW@50C；Coherent CPO ELS | $1.5-3B；CPO/SiPh 早期 | $4-8B；CPO/SiPh/OCS 共振 | $8-18B；CPO 与硅光扩散 | +40-70% / +80-130% / +200% | 45-60% / 50-65% / 60%+，短缺时高溢价 |
| 硅光 PIC + 外置 CW laser | Coherent 1.6T SiPh、400G SiPh link；Tower/NVIDIA 1.6T optical 生态 | $2-4B；800G/1.6T 20-30% | $5-11B；30-45% | $10-22B；40-60% | +40-70% / +80-120% / +150% | PIC/光引擎 35-50%；CW laser 更高 |
| GaAs/1060nm VCSEL 短距/scale-up | Lumentum 1060nm VCSEL co-packaged demo，累计 3DS emitters >100 亿；Coherent VCSEL 也用于 1.6T/CPO | $1-2B；scale-up <5% | $2-5B；5-15% | $5-12B；10-30% | +20-40% / +50-90% / +150% | 35-50% / 45-55% / 55%+ |
| 800ZR/ZR+ coherent DCI | 2025 coherent module 接近 $6B；AI scale-across 增长 | $5.5-7.5B；AI DCI 20-30% | $8-12B；30-45% | $12-20B；40-60% | +20-35% / +35-55% / +70% | 35-50%，DSP/高端 coherent module 定价强 |
| OCS/MEMS optical switching | Google Apollo OCS；TrendForce 称 OCS 约 100W vs 传统交换约 3,000W | $0.2-0.7B；AI cluster <5% | $0.8-2.5B；5-12% | $2.5-8B；10-25% | +50% / +100% / +200% | 35-50%，但云厂自研会压系统利润 |
| AI 数据中心光纤/高密连接 | Meta-Corning up to $6B；NVIDIA-Corning 美国 connectivity 10x、fiber +50% | $6-11B；新 AI 园区高配 | $12-22B；scale-out 光纤密度上行 | $22-45B；scale-across 放大 | +30-50% / +60-90% / +120% | 25-40%，连接器/高密管理优于普通光缆 |

### 2.2 对已放量产品的投资解释

800G 是 2026 的“现金流底座”，但不是利润率最性感的环节。1.6T 是 2026H2-2027 的核心弹性，早期 ASP 和毛利率更好，之后供应扩散带来价格竞争。最值得追踪的是 1.6T 模块内部价值分配：retimed 版本 DSP 成本高、功耗高；TRO/LRO/LPO 等低功耗方案减少 DSP/retimer 价值，但对高质量 EML、TIA、equalization、host SerDes 和系统验证提出更高要求。

激光器与 EML 是真正的卡点。Lumentum 和 Coherent 的最新财报都在说同一件事：AI 数据中心需求强到要预投 InP 产能。Lumentum Q3 FY26 non-GAAP GM 47.9%，Q4 指引 revenue $960M-$1.01B、operating margin 35%-36%；Coherent 指引 Q4 FY26 revenue $1.91B-$2.05B、non-GAAP GM 39%-41%。这说明上游光器件正在享受比普通模块组装更好的定价环境。

## 3. 在研关键产品与细分技术：成熟节奏、市场规模与利润率

| 在研技术/产品 | 2026-05 状态 | 未来 3 个月市场/渗透 | 未来 1 年市场/渗透 | 未来 2 年市场/渗透 | 增长预测：基准/乐观/极度乐观 | 利润率判断 |
|---|---|---:|---:|---:|---:|---|
| 3.2T pluggable module | Coherent/Broadcom/OpenLight 已展示关键 link/PIC/DSP | <$0.2B；样品 | $1-3B；1-3% 新增 AI 高速端口 | $8-25B；8-20% | 基数低 +200% / 2027 $10B+ / 2027 $30B+ | 初期模块 35-50%，器件/DSP 50-70% |
| 400G/lane EML/EAM/MZM | Broadcom Taurus + 400G EML/PD；Coherent 400G differential EML/SiPh link | <$0.1B | $0.5-2B | $4-10B | +200% / +400% / +800% | 50-70%，良率/测试稀缺 |
| CPO/CPX/NPO 光引擎 | NVIDIA Spectrum-X Photonics 2026H2；Coherent 6.4T socketed CPO；Open CPX MSA | $0.1-0.4B | $1-5B | $6-22B | +100% / +200% / +300%+ | ELS/光引擎 45-65%；系统早期成本高 |
| External Laser Source/ELSFP | Lumentum 16-channel DWDM UHP laser、CPO laser source | $0.2-0.6B | $1.5-4B | $5-14B | +80% / +150% / +300% | 50-70%，可靠性和冗余决定溢价 |
| XPO 12.8T 液冷可插拔 | Arista MSA，12.8T、204.8T/RU、400W cooling | <$0.1B | $0.5-2B | $3-14B | +200% / +500% / $20B 级 | 早期 35-55%，液冷/field service 分摊成本 |
| OCI optical scale-up | AMD/Broadcom/Meta/Microsoft/NVIDIA/OpenAI 成立 OCI MSA，200G optical PHY spec | <$0.05B | $0.2-1.5B | $3-12B | 低基数 / 2027 pilot / 2028 前倒 | PHY/光引擎 45-65%，MSA 后价格下降 |
| 1600ZR/ZR+ / coherent-lite | Marvell COLORZ 1600 2026H2 sampling，Ciena/Nokia 2nm coherent | <$0.3B | $1-3B | $5-15B | +100% / +200% / +400% | coherent DSP 和 line card 40-60% |
| TFLN / EO polymer / SOH / BTO 调制器 | 200G/400G 低功耗调制器验证，仍在客户 qual | <$0.05B | $0.1-0.8B | $1-5B | +100% / +300% / +700% | 若进主供应链可 50%+，但量产风险高 |
| Hollow-core fiber 低延迟 DCI | OFC 2026 讨论升温，loss 与部署成本仍待验证 | <$0.05B | $0.1-0.5B | $0.5-3B | +50% / +150% / +400% | 高端项目毛利好，但商业化慢 |

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 头部公司/工艺 | 2026 变化 |
|---|---|---|---|
| InP EML/CW/PD | 美国、日本、中国、部分欧洲 | Lumentum、Coherent、Mitsubishi Electric、Sumitomo Electric、Furukawa、Source Photonics、光迅、源杰科技等；3-inch 向 6-inch InP 过渡 | Lumentum Greensboro 240,000 sqft InP fab，mid-2028 ramp；Coherent 称 2026 年底 InP output 翻倍、2027 再翻倍以上 |
| GaAs/VCSEL | 美国、欧洲、亚洲 | Coherent、Lumentum、Broadcom、ams-OSRAM、Sony 等；6-inch GaAs VCSEL、1060nm/850nm | 3D sensing 产能迁移到 AI scale-up 是弹性来源 |
| 硅光 PIC | 美国、以色列、台湾、新加坡、欧洲 | Intel、Cisco/Acacia、Marvell、Broadcom、Coherent、Tower PH18、GlobalFoundries Fotonix、TSMC、OpenLight、Ayar Labs、Lightmatter、Ranovus | NVIDIA/Tower、Marvell/NVIDIA、Coherent/SiPh 推动 1.6T 与 CPO |
| 模块组装与测试 | 中国、泰国、台湾、马来西亚、美国 | Innolight、中际旭创、新易盛、Eoptolink、Fabrinet、Coherent、Lumentum、AAOI、Accelink、Hisense Broadband、Source Photonics | AAOI 退出 Q1 2026 时 800G 月产能近 10 万只；Fabrinet 受益但也受 component constraints |
| 光纤/连接器 | 美国、中国、日本、欧洲 | Corning、YOFC、OFS、Prysmian、Fujikura、Sumitomo、Senko、US Conec、Molex、Samtec、Amphenol、TE | Corning 与 Meta up to $6B，NVIDIA 合作使美国 connectivity 10x、fiber +50% |
| DSP/SerDes/retimer | 美国、以色列、台湾代工 | Broadcom、Marvell、MACOM、MaxLinear、Credo、Semtech、Astera Labs、Alphawave | Broadcom 3nm Taurus 400G/lane；Marvell 2nm coherent DSP；200G/400G SerDes 成为测试瓶颈 |
| 测试与设备 | 美国、日本、欧洲、中国 | VIAVI、Keysight、Anritsu、EXFO、Advantest、Teradyne、Aixtron、Veeco、ASM 等 | 1.6T/3.2T、224G/448G、CPO burn-in 拉长测试时间 |

### 4.2 供给瓶颈

1. InP 外延、DFB/EML 量产良率和 6-inch 转换。200G/400G EML 不是简单扩线，速率、温度、线宽、chirp、可靠性一起卡良率。
2. 3nm/2nm optical DSP、coherent DSP、224G/448G SerDes 供给。先进制程也被 AI ASIC/GPU 抢产能。
3. 高速光封装：TOSA/ROSA、FAU、微透镜阵列、isolator、filter、TEC、PM fiber、V-groove、active alignment，任何小件缺货都会拖整机。
4. 测试和 burn-in 时间。1.6T/3.2T 的 BER/FEC/thermal margin/aging 测试显著增加，设备和工程师都紧。
5. 热管理：OSFP 20W+ 已不轻松，XPO 400W/module、CPO 贴近 switch ASIC 后，液冷、冷板、热漂移补偿都会变成产品可靠性问题。
6. Hyperscaler 认证周期。进入 AVL 后才有定价权，认证失败或延迟会让产能空转。
7. 光纤管理和连接密度。OCS、multi-rail、128+ fiber pairs/rack 让连接器、布线、清洁、现场维护成为瓶颈。
8. 人才。InP process、硅光版图/封装、光电协同测试、CPO 系统工程师是稀缺工种。

### 4.3 BOM 与单位成本拆分

| 产品 | BOM/成本结构测算 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 800G retimed OSFP/QSFP-DD | DSP/retimer 20-30%；光引擎/EML/SiPh/VCSEL 30-40%；driver/TIA/PD 10-15%；PCB/壳体/散热/连接 10-15%；组装测试 10-20% | 客户 AVL、良率、DSP 采购价、测试时间、是否自有光芯片 | 大客户 LTA 定价，短缺时通过 expedite fee、mix、季度重定价传导 |
| 1.6T DR8/2xDR4 | 光源/调制/PD 35-45%；DSP/host electrical 20-30%；driver/TIA 10-15%；热设计/连接/测试 15-25% | 200G/400G lane 良率、功耗、客户 qual、能否做到 TRO/LRO/LPO | 早期供不应求，上游 EML/CW laser 可拿更多溢价 |
| EML/CW laser/ELS | 外延/晶圆 25-35%；fab process 20-30%；封装/TEC/isolator 20-30%；测试老化 15-25% | 线宽、温漂、可靠性、良率、6-inch 产出 | 短缺产品直接涨价或绑定长期容量承诺 |
| 硅光 PIC/光引擎 | foundry wafer 20-30%；III-V laser coupling/flip-chip 20-35%；封装/FAU 20-30%；测试 15-25% | 耦合效率、封装良率、laser sourcing、thermal drift | CPO/CPX 早期以 NRE + 长约锁价为主 |
| coherent ZR/ZR+ | coherent DSP 30-40%；laser/modulator/receiver 25-35%；封装测试 20-30%；系统软件/安全 5-10% | DSP 节点、功耗、MACsec、OIF/OpenZR+ interoperability | 高端客户按 power/bit、reach、security 支付溢价 |

## 5. 竞争格局、壁垒与价值捕获

### 5.1 市场结构

高端 AI 光模块是“需求广阔但客户极集中”的市场。Google 800G+ 订单中，TrendForce 预计 Innolight 与 Eoptolink 合计接近 80%；NVIDIA 通过对 Lumentum/Coherent 的投资和采购承诺锁激光器、光网络产品与先进 optics 产能；Marvell/Broadcom 在 DSP/SerDes/交换芯片上处于寡头；Fabrinet 是高端 optical packaging/EMS 的关键产能；Corning 在美国光纤和连接产能上被 Meta/NVIDIA 直接锁定。

### 5.2 可量化壁垒

| 壁垒 | 为什么能定价 | 量化观察 |
|---|---|---|
| 200G/400G EML/SiPh/CW laser 技术壁垒 | 良率和可靠性直接决定客户能否交付 AI 集群，不合格供应商无法进 AVL | Lumentum 200G EML 收入 Q3 FY26 环比翻倍以上；Coherent 计划 InP output 2026 年底翻倍 |
| 规模壁垒 | hyperscaler 需要百万级模块、长期一致性、跨区域供货，产能小的厂商只能做样品 | AAOI 800G 月产能近 10 万只仍只是追赶；Corning connectivity 直接 10x 扩产 |
| 客户锁定 | 一旦进客户架构和固件/测试/运维体系，替换要重新 qual | NVIDIA 对 Lumentum/Coherent 各 $2B 投资与多十亿美元采购承诺 |
| 标准/生态壁垒 | XPO、OCI、Open CPX、OIF、CW-WDM MSA 参与者影响接口和形态 | Arista XPO MSA、OCI MSA、Open CPX MSA 都在 2026 成立/强化 |
| 切换成本 | 光模块涉及 switch ASIC、cage、热设计、FEC、DSP、firmware、现场维护 | 低价替换可能造成 link flap、BER、热失效，客户愿意为稳定付溢价 |
| 认证和可靠性 | GR-468、Telcordia、hyperscaler internal qual、burn-in 周期长 | 1.6T/3.2T 测试时间提高，VIAVI/Keysight 等验证设备受益 |

### 5.3 长期高 ROIC/高毛利价值捕获排序

1. optical DSP/coherent DSP/SerDes：Broadcom、Marvell、MACOM、Credo 等，毛利率和设计锁定强。
2. InP EML/CW/ELS 高端激光器：Lumentum、Coherent、Mitsubishi、Sumitomo、Furukawa、部分中国追赶者，供给短缺时定价权强。
3. 硅光 PIC/CPO 光引擎：Coherent、Marvell、Broadcom、Intel、Cisco/Acacia、Ciena/Nubis、OpenLight、Ayar/Lightmatter/Ranovus，若进入量产会有高壁垒。
4. coherent DCI 系统与 pluggable：Marvell、Ciena、Nokia、Cisco/Acacia，AI scale-across 让长期需求可见。
5. 高密连接/光纤管理：Corning、Senko、US Conec、Molex、Samtec、Amphenol、TE，毛利不一定最高，但客户协议和扩产确定性强。
6. 模块组装：Innolight/Eoptolink/Coherent/Lumentum/AAOI/Accelink/Fabrinet 等，收入 β 最大，毛利取决于是否自有关键光芯片、是否处于短缺代际。

## 6. 2026 关键变化：最可能发生的 3 个拐点

1. 1.6T 从样品转为可交付订单。Lumentum 明确 1.6T transceivers Q4 FY26 ramp，Coherent/Lumentum/Eoptolink/AAOI 均展示或交付 1.6T；2026H2 将验证谁能稳定交付。
2. NVIDIA 锁定光器件供给并带动美国本土化。Lumentum、Coherent、Corning、Marvell 的 2026 战略合作显示，光器件已是 AI factory 的关键战略资源，不再是普通采购件。
3. OCS/CPO/OCI 从“技术方向”变成“系统架构选项”。Google Ironwood/Apollo OCS、NVIDIA Spectrum-X Photonics、OCI MSA、Open CPX/XPO MSA 同时出现，说明 AI 网络开始从电交换堆叠转向光电协同。

## 7. 2027 关键变化：最可能发生的 3 个拐点

1. 1.6T 成为新增大型 AI 集群默认配置，800G 进入价格竞争期。收入继续增长，但利润从普通模块转向 EML/CW/SiPh/DSP/测试等瓶颈层。
2. 3.2T/400G-per-lane 开始小批量收入。2027H2 可能出现 3.2T 客户 qual、小批量模块/engine 订单，以及 400G EML/EAM/MZM、Taurus 类 DSP、224G/448G 测试设备高景气。
3. AI scale-across 把 coherent DCI、multi-rail、光纤对数推成新瓶颈。Marvell COLORZ 1600、Ciena 1600ZR/hyper-rail、Nokia multi-rail/3.2T coherent-lite 将在 2027-2028 形成第二条增长曲线。

## 8. 头部公司与细分技术公司清单

| 细分 | 头部/优势公司 |
|---|---|
| 800G/1.6T AI 光模块 | Innolight/中际旭创、Eoptolink/新易盛、Coherent、Lumentum、Applied Optoelectronics、Accelink/光迅科技、Hisense Broadband、Source Photonics、Fabrinet、华工科技、剑桥科技、博创科技、Linktel、FS、Luxshare |
| InP EML / DFB / CW laser / PD | Lumentum、Coherent、Mitsubishi Electric、Sumitomo Electric、Furukawa、Broadcom、MACOM、Source Photonics、光迅科技、源杰科技、长光华芯、仕佳光子、华工科技、住友/古河生态 |
| VCSEL / 短距光源 | Coherent、Lumentum、Broadcom、ams-OSRAM、Sony、Trumpf Photonic Components、长光华芯、纵慧芯光、华芯半导体等 |
| 硅光 PIC / 光引擎 | Intel、Cisco/Acacia、Marvell、Broadcom、Coherent、Ciena/Nubis、Tower Semiconductor、GlobalFoundries、TSMC、OpenLight、Ayar Labs、Lightmatter、Ranovus、POET、DustPhotonics、Sicoya、Scintil、Quintessent、Celestial AI |
| Optical DSP / coherent DSP / SerDes | Broadcom、Marvell、MACOM、MaxLinear、Credo、Semtech、Astera Labs、Alphawave Semi、Synopsys/Cadence IP |
| CPO / CPX / NPO / ELS | NVIDIA、Broadcom、Coherent、Lumentum、Marvell、Ciena/Nubis、Molex、Samtec、TeraHop、Ayar Labs、Lightmatter、Ranovus、OpenLight、Celestial AI、Intel、Cisco/Acacia |
| XPO / 高密可插拔 | Arista、Eoptolink、Lightmatter、TeraHop、Linktel、Marvell、Coherent、Molex、Samtec、Amphenol、TE |
| OCS / optical switching | Google Apollo、Coherent、Calient、Polatis/HUBER+SUHNER、MEMS/LCOS 光交换生态、Ciena/Nokia line system 生态 |
| coherent DCI / 1600ZR | Marvell、Ciena、Nokia、Cisco/Acacia、Infinera/Nokia、Coherent、Lumentum、NEC、Fujitsu |
| 光纤/连接器/高密布线 | Corning、YOFC/长飞、OFS、Prysmian、Fujikura、Sumitomo、Senko、US Conec、Molex、Samtec、Amphenol、TE Connectivity、Hirose、康普、亨通光电、中天科技、太辰光、天孚通信 |
| 光学元件/无源器件 | 天孚通信、腾景科技、仕佳光子、光库科技、太辰光、Senko、US Conec、Coherent、Lumentum、Molex |
| EMS / advanced optical packaging | Fabrinet、Celestica、Jabil、Foxconn、Flex、Sanmina、Coherent internal manufacturing、AAOI、Innolight/Eoptolink 自有产线 |
| 测试设备 | VIAVI、Keysight、Anritsu、EXFO、Tektronix、Rohde & Schwarz、Advantest、Teradyne、FormFactor |
| 制程设备/材料 | Aixtron、Veeco、ASM、Applied Materials、Lam Research、KLA、Tokyo Electron、Entegris、II-VI/Coherent materials、Sumitomo/Mitsubishi/Furukawa InP/GaAs 生态 |

## 9. 资料来源与关键锚点

| 来源 | 关键锚点 |
|---|---|
| [TrendForce：Google 高速互连推动 800G+ 光模块占比 2026 超 60%](https://www.trendforce.com/presscenter/news/20260210-12919.html) | 800G+ 占比 2024 年 19.5% 到 2026 年 60%+；Google 800G+ 需求和 Innolight/Eoptolink 份额 |
| [Coherent OFC 2026 1.6T/3.2T 可插拔技术](https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026) | 1.6T 多路线：SiPh PIC、高功率 InP CW laser、200G InP EML、200G GaAs VCSEL；3.2T 400G EML/SiPh link |
| [Coherent Q3 FY26 results](https://www.coherent.com/news/press-releases/third-quarter-fiscal-year-2026-results) / [investor deck](https://www.coherent.com/content/dam/coherent/site/en/documents/investors/investor-presentations/2026/may-6/investor-presentation-20260506.pdf) | Q3 FY26 revenue $1.81B，non-GAAP GM 39.6%，Datacenter & Communications $1.362B，InP output 扩产 |
| [Lumentum OFC 2026](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx) | 1.6T DR4 OSFP 使用 4 颗 400G differential EML；SHP laser >1W@25C；16-channel DWDM UHP laser |
| [Lumentum VCSEL scale-up demo](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Showcases-Breakthrough-Optical-Scale-Up-Demonstration-at-OFC-2026-Using-VCSEL-Technology/default.aspx) | 1060nm VCSEL array co-packaged with host ASIC；3DS base 累计 >100 亿 emitters |
| [Lumentum Q3 FY26 results](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx) / [deck](https://s21.q4cdn.com/377324469/files/doc_financials/2026/q3/Q3-FY26-Earnings-Presentation_final.pdf) | Revenue $808.4M，non-GAAP GM 47.9%，200G EML revenue 环比翻倍以上，1.6T Q4 FY26 ramp |
| [NVIDIA-Lumentum strategic partnership](https://investor.lumentum.com/financial-news-releases/news-details/2026/NVIDIA-Announces-Strategic-Partnership-With-Lumentum-to-Develop-State-of-the-Art-Optics-Technology/default.aspx) | NVIDIA 投资 $2B，包含多十亿美元采购承诺和 advanced laser capacity access |
| [Lumentum Greensboro InP fab](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-New-U-S--Manufacturing-Facility-to-Produce-Advanced-Lasers-for-the-Worlds-Largest-AI-Data-Centers/default.aspx) | 240,000 sqft，6-inch InP，mid-2028 ramp，>400 jobs |
| [NVIDIA-Coherent strategic partnership](https://www.coherent.com/news/press-releases/nvidia-and-coherent-announce-strategic-partnership) | NVIDIA 多十亿美元采购承诺和 $2B 投资，锁 advanced laser/optical networking products |
| [Broadcom Taurus 400G/lane DSP](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next) | 3nm Taurus BCM83640，400G/lane optical PAM4 DSP，支持 1.6T 到 3.2T；LightCounting 1.6T/3.2T 五年 >1 亿只 |
| [Broadcom OFC 2026 AI infrastructure](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai) | Tomahawk 6 102.4T production volume；200G/lane VCSEL/EML/CWL/CPO；OCI MSA |
| [Marvell COLORZ 1600](https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html) | 1.6T ZR/ZR+ OSFP，2nm Electra coherent DSP，20km/120km/1000km，2026H2 sampling |
| [NVIDIA Spectrum-X Ethernet Photonics](https://developer.nvidia.com/blog/scaling-power-efficient-ai-factories-with-nvidia-spectrum-x-ethernet-photonics/) / [NVIDIA silicon photonics](https://www.nvidia.com/en-us/networking/products/silicon-photonics/) | CPO/silicon photonics，409.6Tb/s，5x power efficiency、10x resiliency |
| [Arista XPO MSA](https://www.arista.com/en/company/news/press-release/23697-pr-20260311) | 12.8T liquid-cooled pluggable，204.8Tbps per OCP RU，400W cooling，4x OSFP density |
| [Ciena OFC 2026 high-speed connectivity](https://www.ciena.com/about/newsroom/press-releases/ciena-solidifies-ai-networking-leadership-unveils-new-innovations-for-high-speed-connectivity) | hyper-rail 32x density、-75% power、-85% space；1600ZR/ZR+ 2nm coherent |
| [Corning-NVIDIA partnership](https://www.corning.com/worldwide/en/about-us/news-events/news-releases/2026/05/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure.html) | 美国 optical connectivity 产能 10x、fiber +50%、3 座新厂、3,000+ jobs |
| [Corning-Meta up to $6B agreement](https://investor.corning.com/news-and-events/news/news-details/2026/Corning-and-Meta-Announce-Multiyear-up-to-6-Billion-Agreement-to-Accelerate-US-Data-Center-Buildout/default.aspx) | Meta up to $6B，最新光纤/光缆/连接方案，Hickory NC 新设施 |
| [AAOI Q1 2026 results](https://www.globenewswire.com/news-release/2026/05/07/3290613/9986/en/applied-optoelectronics-reports-first-quarter-2026-results.html) | Q1 revenue $151.1M；datacenter $81.4M；首个 hyperscale 800G volume shipment；800G 月产能近 10 万只 |
| 本项目文件：`ai_chip_research_2026_2027.md` | 2026-2027 出货量最大的 AI 芯片/平台及其光互联路径 |
| 本项目文件：`conference_update/ofc_2026_conference_update.md` | OFC 2026 光通信会议整理、Cignal/LightCounting/VIAVI/Nokia 等二手锚点 |
| 本项目文件：`AI数据中心建设规模与产业链订单映射_2026-2027_美国.md` | 网络与光互联订单池、AI 数据中心 CapEx 情景 |

## 10. 最终投资判断

基准情形下，2026 年投资优先级是 1.6T 光模块、200G EML/CW laser、硅光 PIC、coherent DCI 和测试设备；2027 年优先级转向 3.2T/400G-per-lane、CPO/CPX/NPO/ELS、XPO、1600ZR/ZR+ 和 OCS。若采用极度乐观 AI 基建假设，最强弹性来自同时满足三点的公司：已经进入 hyperscaler AVL、掌握关键光芯片/激光器或 DSP、并且正在扩 6-inch InP/SiPh/高端测试产能。

最需要警惕的是“需求很好但股价买错层级”：普通模块组装会先放量，但一旦产能追上，ASP 下行可能压利润；长期高 ROIC 更可能留在激光器/EML、DSP/SerDes、CPO 光引擎、coherent DSP、测试和被大客户长约锁定的高密连接/光纤产能。
# 行业调研：【开放Scale-up互联】

截至日期：2026-05-08  
研究口径：本报告把“开放Scale-up互联”定义为 AI rack / pod 内把 GPU、XPU、ASIC、NIC、CPU、memory/cache 节点连接成低延迟、高带宽、近似统一内存/统一计算域的开放或半开放互连体系。核心包括 UALink / UALink over Ethernet、ESUN / SUE / UEC、PCIe 6/7 / CXL fabric、scale-up switch ASIC、NIC / DPU / retimer、AEC / ACC / CPC / top-side copper、1.6T/3.2T optics、CPO / NPO / OCS、互连 IP / EDA / 测试与管理软件。NVIDIA NVLink / NVSwitch、Google ICI、AWS NeuronLink、Huawei UB 等封闭互连作为对照和需求上限，不计入“开放”主体收入，NVLink Fusion 归为“半开放授权生态”。

## 0. 一页结论

开放 Scale-up 互联的投资机会不是“2026 年 UALink 一夜替代 NVLink”，而是 **AI 基础设施从单机 8-GPU 走向 72/128/256/1024 XPU rack/pod 后，非 NVIDIA 生态必须补齐一个可采购、可验证、可多供应商化的近端互连层**。2026 年最确定放量的是 UALoE / SUE / ESUN 类 Ethernet scale-up、PCIe 6 fabric switch / retimer、AEC / CPC / top-side copper、800G/1.6T optics；native UALink switch 和 accelerator port 进入设计导入与小批量，2027 年才更像真正的量产年。

核心判断：

| 判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 开放 Scale-up 互联相关收入 | 约 180-260 亿美元 | 约 280-390 亿美元 | 约 450-600 亿美元 |
| 2027 开放 Scale-up 互联相关收入 | 约 380-550 亿美元 | 约 650-900 亿美元 | 约 1100-1500 亿美元 |
| 2028 开放 Scale-up 互联相关收入 | 约 650-950 亿美元 | 约 1200-1700 亿美元 | 约 2000-2800 亿美元 |
| 2026 最可能路径 | UALoE/SUE/ESUN + PCIe 6 fabric + AEC/CPC + 1.6T optics | AMD Helios、Broadcom SUE、Astera Scorpio X 同时带动 | 多家 hyperscaler custom ASIC rack 抢先开放互连 |
| 2027 主升浪 | native UALink 交换芯片、scale-up Ethernet、多厂商 switch/NIC、CPO/OCS pilot | UALink 合规生态稳定，非 NVIDIA rack 大批量出货 | 开放互连成为 30%+ 新增 AI rack 的默认配置 |

为什么我对 2026-2027 非常乐观：

- 本项目已有芯片路线图显示，2026-2027 出货价值最大的 10-12 款 AI 芯片/平台中，除 NVIDIA Blackwell / Rubin 外，Google TPU、AWS Trainium、AMD MI350/MI400、Meta MTIA、Microsoft Maia、OpenAI/Broadcom XPU、Huawei Ascend、Cambricon、Alibaba PPU 都需要自己的 scale-up / scale-out fabric。只要非 NVIDIA ASIC/GPU 的 GW 级建设兑现，开放互连会从“标准讨论”变成“rack BOM 必选件”。
- UALink 200G 1.0 已公开，支持每 lane 200G、pod 内最多 1024 accelerator；2026-04 UALink 又发布 Common 2.0、200G DL/PL 2.0、Manageability 1.0、Chiplet 1.0，加入 In-Network Compute、管理平面、UCIe 3.0 chiplet 集成。
- OCP ESUN 1.0 于 2026-03 发布，四个月内从 12 家创始成员扩到 175+ 参与公司；它用 4B ESUN Header 替代 20-40B IP header，并要求 switch 支持 CBFC、LLR、ECN、CoS、Flow Label、TTL。
- Astera Labs 2026-05 发布 Scorpio X-Series 320-lane AI fabric switch，已向 hyperscaler 出货，2H26 ramp；公司称 merchant scale-up switch silicon 市场到 2030 年可达 200 亿美元。
- Broadcom 已在 2025-2026 把 Tomahawk Ultra、Tomahawk 6、Thor Ultra、Agera retimer、Sian / Taurus DSP、CPO、3.5D XPU 串成开放 AI fabric 组合。Tomahawk Ultra 可 250ns switch latency、77B packets/s、SUE 下 XPU-to-XPU <400ns；Tomahawk 6 单芯片 102.4Tbps，支持 512 XPU scale-up、100k+ XPU two-tier scale-out、CPO、UEC。
- AMD Helios 是第一条最可见的开放 rack 量产路径：72 MI450 / MI455X GPU、31TB HBM4、260TB/s scale-up、43TB/s Ethernet scale-out，2026 年 release 给 OEM/ODM，HPE、Celestica 已公开合作，Celestica 负责 Helios scale-up switches，使用 UALink over Ethernet。

## 1. 行业机会、挑战与 2026/2027 技术路线

### 1.1 需求本质：从 8-GPU server 到 1K-XPU pod

Scale-up 的价值来自“让多个 accelerator 像一个更大的 accelerator 工作”。AI 模型进入 MoE、long-context、agentic inference、distributed inference、KV cache / context memory 后，通信模式从大块 all-reduce 变成更小、更频繁、更 tail-latency-sensitive 的消息。OCP ESUN 1.0 明确写到，下一代 scale-up 网络预计从 8 GPU box 扩到 >=1K GPU，且 20% bandwidth drop 在 128 accelerator domain 里可造成约 5% end-to-end performance loss。

这意味着互连不再是配件，而是 GPU 利用率、tokens/watt、time-to-first-token、训练稳定性和客户 ROI 的核心变量。一个 72-GPU rack 如果因 fabric 故障或尾延迟损失 5%-10% 利用率，损失的算力价值远高于互连 BOM 本身。

### 1.2 2026 可用技术地图

| 技术路径 | 2026 状态 | 优点 | 约束 | 2026 结论 |
|---|---|---|---|---|
| NVIDIA NVLink / NVSwitch | GB200/GB300 已量产，Rubin NVLink 6 H2 2026 | 性能、软件、NCCL、系统验证最成熟 | 封闭，绑定 NVIDIA GPU/rack | 市场上限与标杆，不是开放互连主体 |
| NVLink Fusion | 2025 发布，2026 Marvell 深度合作 | 允许 custom XPU/CPU 接入 NVIDIA rack-scale 架构 | 授权式半开放，仍由 NVIDIA 控制 | 对开放标准构成“高性能半开放”压力 |
| UALink native | 1.0/2.0 规格成熟，芯片/IP 导入 | 200G lane、load/store/atomic、1024 endpoint、低协议开销、多厂商 | switch silicon、accelerator port、合规、软件生态仍早 | 2026 设计导入，2027 放量 |
| UALink over Ethernet / UALoE | AMD Helios、HPE、Celestica 已公开 | 可借 Ethernet silicon/SerDes/optics 更快落地 | 性能低于 native UALink，协议/封装仍需验证 | 2026 最可能先放量的开放 scale-up 路线 |
| ESUN / SUE / UEC Ethernet scale-up | ESUN 1.0、UEC 1.0、Broadcom Tomahawk Ultra/6 | 供应链成熟、运维熟悉、多厂商、可同时 scale-up/out | small-message overhead、拥塞控制、lossless 调试复杂 | 2026 现实主线 |
| PCIe 6 / CXL fabric | Astera Scorpio P/X、retimer、switch 已出货 | 生态大、CPU/SSD/NIC/accelerator attach 率高 | lane 数、reach、软件语义、跨 rack 拓扑受限 | 2026 收入确定性高 |
| AEC / ACC / CPC / top-side copper | Credo、Broadcom、Luxshare、Samtec、Molex、TE 等放量 | rack 内低成本、低延迟、低功耗、可维护 | 224G/448G SI、skew、插损、热密度、测试 | 2026-2027 被低估的高景气方向 |
| 800G / 1.6T optics | 800G 主流，1.6T 进入规模导入 | rack 间 / pod 间必要，供应链明确 | DSP/laser/PIC/测试短缺，ASP 2027 可能下降 | 2026 收入最大 |
| CPO / NPO / OCS / OCI | OFC/OCP 2026 样机和标准密集 | 功耗、密度、光纤数量优势大 | 维护、ELS、可靠性、多供应商、现场更换 | 2026 pilot，2027 小批，2028 大规模 |

### 1.3 结合 2026/2027 最大 AI 芯片路线的成熟和放量时间

| AI 平台 | 2026-2027 互连背景 | 对开放 Scale-up 的含义 | 基准 | 乐观 | 极度超预期 |
|---|---|---|---|---|---|
| NVIDIA GB300 / B300 | NVLink/NVSwitch 闭环，scale-out 用 Spectrum-X / Ethernet / optics | 开放互连主要吃 scale-out optics / copper，不吃 rack 内核心 | 开放 scale-up 份额低 | NVLink Fusion 带动第三方 IP | 半开放 NVLink Fusion 吃掉部分 ASIC 互连 |
| NVIDIA Rubin | NVLink 6，NVL72 / NVL576，CPO switch | 继续抬高性能标杆，倒逼 UALink/ESUN | native 开放路线追赶 | Marvell / custom XPU 接入 Fusion | Fusion 成为 custom ASIC 高端路线 |
| AMD MI350 / MI400 / Helios | MI350 开放 rack，MI400/Helios 支持 UALink/UALoE/UEC | 最直接的开放 scale-up 量产驱动 | 2026 H2 小批，2027 ramp | 2026 H2 多 OEM 交付 | 2027 成为非 NVIDIA rack 标准样板 |
| Google TPU Ironwood / TPU8 | 自研 ICI/OCS/光网络，Broadcom silicon | 标准化会更多外溢到 optics/OCS/UEC 而非 UALink | 封闭为主 | OCS / optical scale-up 扩散 | Google 供应链把开放光交换推成行业标准 |
| AWS Trainium2/3/4 | NeuronLink/NeuronSwitch，自研系统；Trainium4 可能与 NVLink Fusion 关联 | 近期封闭，中期可能采用半开放接口 | 封闭 | NIC/UEC/optics 外溢 | Fusion/UEC 进入 AWS 新代际 |
| Meta MTIA | Broadcom XPU + OCP/ORW/开放硬件 | 最适合 ESUN/SUE/UEC 和开放 rack | 2026 推理 rack 导入 | 2027 多 GW | MTIA 变成开放 ASIC rack 范式 |
| Microsoft Maia | Azure 自研，推理优先 | ESUN/UEC、PCIe/CXL、optics 受益 | 内部定制 | 2027 扩大开放供应链 | Azure 推动 ESUN 采购标准 |
| OpenAI/Broadcom XPU | 10GW 2026 H2 起步、2029 完成 | 需要可供应、可多厂商的 scale-up/out fabric | 2027 才明显 | 2026 H2 开始拉动 Broadcom fabric | OpenAI 订单把 SUE/UEC 推成事实标准 |
| Huawei Ascend / 中国 ASIC | 自研超节点/CloudMatrix/UB，国产 Ethernet/optics | 中国会发展本土开放/半开放等价物 | 封闭超节点为主 | Ethernet/PCIe/CXL 国产替代扩张 | 国产 UALink-like / CXL fabric 出现 |

### 1.4 2026 最可能的技术路径

按“2026 实际交付概率”排序：

1. **Broadcom SUE / UEC / ESUN Ethernet scale-up**：Tomahawk Ultra、Tomahawk 6、Thor Ultra、Agera、Sian/Taurus、CPO/optics 已形成端到端组合，且 AMD/HPE/Celestica/Arista/Juniper/Celestica/UfiSpace 等生态齐。
2. **AMD Helios 的 UALink over Ethernet**：native UALink switch 还未全面成熟，Helios 首批更可能用 UALoE 把 2026 交付风险降下来。
3. **Astera Scorpio P/X + PCIe 6 fabric / retimer / COSMOS**：Scorpio X 320-lane 已 shipping，2H26 ramp；P-Series 32-320 lane 多客户 2H26 出货、2027 大量 ramp。
4. **AEC / CPC / top-side copper**：224G 已部署、448G 工程验证，rack 内短距仍优先铜，尤其是 near-ASIC / switch-to-module / GPU tray。
5. **800G/1.6T optics + LPO/TRO/DSP**：规模最大但更多覆盖 scale-out / scale-across；在 open scale-up 中用于跨 tray、跨 rack、pod 扩展。
6. **native UALink**：规格成熟、成员豪华，但 2026 更像 early design-in；2027 才是交换芯片、IP、合规、软件真正放量。

## 2. 已开始放量的关键产品：市场规模、渗透率、利润率

说明：下面“未来 3 个月”指 2026 Q2/Q3 过渡期内可确认或可发货收入窗口；“一年”指 2027 年度 run-rate；“两年”指 2028 年度 run-rate。市场规模只计开放/半开放 scale-up 相关产品，不把 NVIDIA NVLink/NVSwitch 闭环收入整体计入。

### 2.1 产品拆分与增长预测

| 已放量产品/技术 | 代表产品/公司 | 未来3个月：基准/乐观/极度乐观 | 2027：基准/乐观/极度乐观 | 2028：基准/乐观/极度乐观 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| Scale-up Ethernet switch ASIC / 系统 | Broadcom Tomahawk Ultra、Tomahawk 6、HPE/Juniper、Arista、Celestica、Accton、UfiSpace | $1.5-2.5B / $2.5-4B / $4-6B | $10-16B / $18-28B / $35-50B | $22-35B / $45-70B / $80-120B | 非 NVIDIA 新增 AI rack：2026 8-15%，2027 25-40%，2028 45-65% |
| PCIe 6 fabric switch / retimer | Astera Scorpio P/X、Aries 6；Broadcom PCIe Gen6；Microchip Switchtec；Synopsys/Cadence IP | $0.8-1.4B / $1.4-2.3B / $2.3-3.5B | $5-8B / $9-14B / $16-24B | $9-16B / $18-30B / $35-50B | 高端 AI server attach：2026 25-35%，2027 40-60%，2028 55-75% |
| AEC / ACC / active copper / CPC / top-side | Credo HiWire / ZeroFlap、Broadcom Agera、Luxshare、Amphenol、TE、Molex、Samtec、BizLink、FIT | $1-1.8B / $1.8-3B / $3-4.5B | $6-10B / $12-18B / $22-32B | $11-20B / $24-40B / $45-70B | rack 内短距高速链路：2026 30-45%，2027 45-65%，2028 55-75% |
| 800G / 1.6T optics 用于 AI fabric | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、Fabrinet、Cisco/Acacia、Marvell/Broadcom DSP | $5-8B / $8-12B / $12-16B | $30-42B / $45-60B / $70-90B | $45-65B / $75-110B / $130-180B | AI optical 中 800G+：2026 60%+；1.6T：2026 5-10%，2027 20-35%，2028 40-55% |
| UEC/ESUN NIC / DPU / SuperNIC | Broadcom Thor Ultra、AMD Pensando Pollara/Vulcano、NVIDIA ConnectX、Marvell、Cisco | $0.8-1.5B / $1.5-2.5B / $2.5-4B | $6-10B / $12-18B / $22-30B | $12-20B / $25-40B / $50-75B | 新增开放 AI rack：2026 15-25%，2027 35-55%，2028 55-75% |
| 互连 IP / EDA / compliance / T&M | Synopsys、Cadence、Siemens EDA、Keysight、Teledyne LeCroy、Anritsu、VIAVI、R&S | $0.4-0.8B / $0.8-1.3B / $1.3-2B | $2-3.5B / $4-6B / $7-10B | $4-7B / $8-13B / $15-22B | 224G/448G/PCIe7/UALink 项目 attach：2026 20-35%，2027 45-65%，2028 70%+ |

### 2.2 利润率三情景

| 产品/技术 | 当前毛利率判断 | 基准 | 乐观 | 极度超预期 |
|---|---:|---:|---:|---:|
| Scale-up Ethernet switch ASIC | merchant ASIC 60-75%；switch system 15-45% | ASIC 62-68%，系统 20-35% | ASIC 68-74%，高端系统 35-45% | ASIC 72-78%，短缺系统 40-50% |
| PCIe/CXL fabric switch / retimer | Astera Q1 2026 GAAP GM 约 76%；高端连接芯片 65-76% | 68-74% | 72-77% | 75-80% |
| AEC/ACC/CPC | 线缆/连接器 25-45%；active IC 55-70% | 28-40% | 35-48% | 40-55%，高端 IC 70%+ |
| 800G/1.6T optics | 模块 25-40%；laser/DSP/PIC 45-65% | 模块 28-38%，上游 50-60% | 模块 35-45%，上游 55-68% | 模块 40-50%，稀缺器件 65-75% |
| NIC/DPU/SuperNIC | 高端 silicon 55-75%；网卡系统 25-45% | 55-65% | 62-72% | 68-78% |
| IP/EDA/T&M | IP/EDA 80-90%；仪器 55-68% | 60-85% | 65-88% | 70-90% |

利润率最有弹性的不是传统白牌 switch，也不是普通光模块组装，而是 **switch / NIC / retimer silicon、200G/400G SerDes、DSP、硅光/laser、互连 IP、测试与管理软件**。开放标准会长期降低单一 vendor lock-in，但短期因为“合格供应商稀缺 + 认证周期长 + 客户抢机架上电”，利润率不会立刻被压平。

## 3. 在研关键产品和细分技术

### 3.1 技术成熟与放量路线

| 在研/早期产品 | 2026 状态 | 未来3个月 | 2027 | 2028 | 投资含义 |
|---|---|---:|---:|---:|---|
| native UALink switch ASIC / endpoint IP | 规格 1.0/2.0 完成，promoter 覆盖 Alibaba、AMD、Apple、Astera、AWS、Cisco、Google、HPE、Intel、Meta、Microsoft、Synopsys | 样片/IP/license 为主，$0.1-0.4B | $4-12B | $12-35B | 2027 最关键新技术，若 AMD/Meta/Microsoft/OpenAI 跟进，弹性巨大 |
| UALink Chiplet 1.0 / UCIe 3.0 集成 | UALink Chiplet 1.0 完全兼容 UCIe 3.0 | $0.05-0.2B | $1-3B | $3-8B | 高毛利 IP/EDA/验证先赚钱，chiplet 量产滞后 |
| ESUN multi-hop / SUE-T / scale-up UEC | ESUN 1.0、SUE 框架、UEC scale-up transport 工作中 | $0.3-0.8B | $5-15B | $18-45B | 比 native UALink 更快落地，靠 Ethernet 供应链放量 |
| In-Network Compute / collectives in switch | UALink 2.0、Astera Hypercast、Broadcom Tomahawk Ultra 均强调 | $0.2-0.6B | $3-8B | $8-20B | 定价能力强，能把 switch 从转发芯片变成 AI collective 加速器 |
| 448G electrical / PCIe 7 / PCIe 8 pathfinding | DesignCon/PCI-SIG 2026 密集验证；PCIe 8 Draft 0.5 | $0.2-0.6B | $2-5B | $8-18B | 仪器、IP、connector 先于终端收入 |
| Optical-aware PCIe / UALink optics | PCI-SIG optical-aware retimer ECN，OFC 演示增多 | <$0.2B | $1-4B | $5-15B | 若 rack/pod reach 不够，光化会提前 |
| CPO / NPO / CPX / OCI / OCS | NVIDIA/Broadcom/Coherent/Lumentum/iPronics/Google 推进 | $0.2-0.8B | $2-6B | $8-25B | 2026 小，2028 可能非线性；ELS、光引擎、测试是先行利润池 |
| 3.2T / 400G-per-lane optics | Broadcom Taurus、OpenLight 3.2T PIC、Coherent 400G/lane | <$0.3B | $2-8B | $12-35B | 2027 小批，2028 主升浪 |
| photonic interposer / chiplet optical fabric | Ayar Labs、Lightmatter、Celestial AI、Broadcom OCI | <$0.2B | $0.8-3B | $5-20B | 成功时改变 scale-up 物理边界，但工程风险高 |

### 3.2 在研产品利润率预测

| 技术 | 基准利润率 | 乐观利润率 | 极度超预期利润率 | 为什么能高毛利 |
|---|---:|---:|---:|---|
| native UALink switch ASIC | 60-70% | 68-76% | 75-82% | 早期合格 switch 硅片少、协议/软件/telemetry 绑定 |
| UALink / UCIe IP | 80-90% | 85-92% | 90%+ | license + VIP + compliance，边际成本低 |
| ESUN/SUE switch features | 55-70% | 65-78% | 75%+ | 低延迟、lossless、small-message goodput 可直接转化 GPU 利用率 |
| In-Network Compute | 65-75% | 72-82% | 80%+ | 不是 commodity switching，而是 collective offload |
| 448G / PCIe7/8 T&M | 58-68% | 62-72% | 68-78% | 标准前期仪器/软件刚需，供应商少 |
| CPO / OCI / photonic interposer | 25-45% | 40-60% | 55-70% | 若进入 hyperscaler design-in，光引擎/ELS/PIC 有稀缺性 |
| 3.2T optics | 25-40% | 35-50% | 45-60% | 400G/lane DSP/EML/PD/SiPh 良率和测试壁垒高 |

## 4. 供给侧：产能、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 地区 | 主要公司 | 工艺/能力 |
|---|---|---|---|
| switch / NIC / retimer silicon | 美国 fabless + 台积电/三星代工 | Broadcom、Astera、Marvell、NVIDIA、AMD Pensando、Cisco、Credo、Intel、Microchip、MaxLinear、Parade、Montage | 5/4/3nm 高端 SerDes ASIC，112G/224G PAM4，PCIe 6/7，UEC/ESUN/UALink |
| 光 DSP / SerDes / CDR | 美国/以色列/台湾 | Broadcom、Marvell、Credo、MaxLinear、Semtech、Marvell/Inphi、Cisco/Acacia | 200G/400G lane DSP、coherent DSP、LPO/TRO/CDR |
| 光模块/光引擎 | 中国、泰国、马来西亚、美国、日本 | 中际旭创、Eoptolink/新易盛、Coherent、Lumentum、Fabrinet、Cisco/Acacia、Accelink/光迅、华工科技、海信宽带、天孚通信、OpenLight、Ayar、Lightmatter | 800G/1.6T OSFP/QSFP-DD、SiPh PIC、EML、VCSEL、CPO/NPO/OCS |
| 铜缆/连接器/CPC | 美国、中国、台湾、日本、东南亚 | Amphenol、TE、Molex、Samtec、Luxshare/立讯、BizLink、FIT/Foxconn、Hirose、3M、Credo | 224G/448G connector、AEC/ACC、top-side、flyover、OSFP-XD、CPC |
| switch system / ODM | 台湾、中国、北美 | Celestica、Accton/Edgecore、Delta、UfiSpace、Quanta/QCT、Wiwynn、Wistron、Inventec、Foxconn、Supermicro、Dell、HPE、Lenovo、Arista、Cisco、Nokia | 51.2T/102.4T/1.6T switch、liquid-cooled chassis、SONiC/Junos/EOS |
| 测试与验证 | 美国/日本/德国 | Keysight、Teledyne LeCroy、Anritsu、VIAVI、Tektronix、Rohde & Schwarz、Synopsys、Cadence、Siemens | 800GE/1.6TE、PCIe 6/7/8、LLR/CBFC、224G/448G BERT/VNA/scope |

### 4.2 主要供给瓶颈

1. **224G/448G SerDes 与 retimer ASIC**：先进节点、模拟团队、封装、功耗同时受限；可以做出来不等于能在 hyperscaler rack 里稳定跑。
2. **LLR/CBFC/PFC/ESUN/UALink 合规与互操作**：标准刚发布，真正的多供应商 plugfest、failover、telemetry、firmware update 仍需时间。
3. **200G/400G optical lane 器件**：EML/EAM/MZM、PD、CW laser、SiPh PIC、FAU、isolator/filter、coherent DSP 都会在 1.6T/3.2T 转换中变成局部瓶颈。
4. **高速铜互连制造良率**：CPC/top-side/AEC 在 224G/448G 下对 skew、crosstalk、return loss、via/fan-out、机械公差极敏感，测试时间上升。
5. **交换机系统级热与电**：102.4T switch、CPO、1.6T front panel、liquid cooling、busbar、PSU、BBU 需要一起验证。
6. **rack 级 burn-in 与现场可维护性**：一个 switch / cable / optic 故障会闲置几十到几百颗 GPU/XPU，客户会把可靠性认证拉得很长。
7. **软件生态**：ROCm、NCCL-equivalent collectives、MPI/libfabric、runtime、telemetry、SONiC/SAI/Redfish/gNMI/YANG 等要贯通，否则硬件带宽无法转为利用率。
8. **客户认证窗口和工程人才**：SI/PI、firmware、协议验证、光电封装、液冷可靠性人才不足，尤其是能跨 chip-board-rack-network 调试的人。

### 4.3 BOM 与价格传导

| 产品 | BOM 粗拆 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| scale-up switch box | switch ASIC 35-45%；PCB/连接器/retimer 15-25%；optics/copper 10-30%；电源/散热 10-20%；制造测试 5-15%；软件 5-10% | ASIC 稀缺、SerDes 良率、系统验证、客户认证 | GPU/XPU rack 订单锁定后，客户更关心准时交付和 uptime，短期可传导 |
| PCIe/UALink/CXL fabric switch silicon | die + package 35-50%；IP/NRE 10-20%；测试 10-20%；软件/firmware 10-15% | 端口数、延迟、telemetry、软件栈 | 以每 GPU/XPU attach 价值定价，不按普通 switch chip 定价 |
| AEC/ACC/CPC | DSP/retimer/redriver 30-45%；连接器/cable 25-35%；assembly 10-20%；测试 10-20% | reach、功耗、BER、field failure | 光模块短缺或功耗过高时，AEC/CPC 可按节能/低延迟溢价 |
| 1.6T optics | DSP/CDR 20-30%；laser/PIC/PD 30-45%；FAU/TOSA/ROSA 15-25%；assembly/test 10-20% | 200G/400G lane 良率、功耗、客户 qual | 初期短缺强传导；2027 多供应商后 ASP 下行 |
| CPO/NPO/OCS | optical engine/PIC/ELS 35-55%；switch package 20-35%；连接/光纤管理 10-20%；测试/维护 10-20% | ELS 冗余、可维护、封装良率、现场更换 | 若节省功耗/光纤/面板密度，可按 TCO 分成式定价 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

- **标准层**：UALink、OCP ESUN、UEC 三条路线并行。UALink promoter 成员包括 Alibaba、AWS、AMD、Apple、Astera、Cisco、Google、HPE、Intel、Meta、Microsoft、Synopsys；ESUN 创始成员包括 AMD、Arista、Arm、Broadcom、Cisco、HPE Networking、Marvell、Meta、Microsoft、NVIDIA、OpenAI、Oracle，2026-03 已扩大到 175+ 参与公司。
- **switch ASIC**：Broadcom 是 Ethernet scale-up/out 的绝对核心供应商之一；Astera 在 PCIe / memory-semantic fabric switch 上快速进入头部；NVIDIA 通过 Spectrum-X / NVLink Fusion 做半开放防守；Marvell、Cisco Silicon One、AMD Pensando、Intel、Cornelis 等分食细分。
- **互连芯片**：Astera、Broadcom、Credo、Marvell、MaxLinear、Semtech、Parade、Montage、Microchip、Renesas 是高端 retimer / AEC / PCIe / CXL / SerDes 重点公司。
- **光模块/光器件**：中际旭创、新易盛、Coherent、Lumentum、Fabrinet、Cisco/Acacia、光迅、华工科技、天孚通信、海信宽带、OpenLight、Ayar Labs、Lightmatter、Marvell/Broadcom DSP 形成多层竞争。
- **系统/ODM**：Celestica、Accton/Edgecore、Delta、UfiSpace、Quanta/QCT、Wiwynn、Wistron、Inventec、Foxconn、Supermicro、Dell、HPE/Juniper、Arista、Cisco、Nokia 是把 silicon 变成 rack-ready 产品的关键。

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 具体表现 | 为什么能定价 |
|---|---|---|
| SerDes/PHY | 112G->224G->448G，BER、FEC、equalization、功耗每代恶化 | 端口速率决定 rack 密度，失败会拖延整机上市 |
| 协议/语义 | load/store、atomic、DMA、memory semantic、LLR/CBFC、PFC、small-header | 能减少 GPU idle time，客户按利用率而非芯片面积付费 |
| 系统验证 | 机柜级 SI/PI/thermal/firmware/telemetry/burn-in | qualification 周期长，合格后切换成本高 |
| 软件栈 | collectives、runtime、SAI/SONiC/gNMI/YANG/Redfish、diagnostics | 没软件的带宽没有价值，软件绑定形成粘性 |
| 客户锁定 | hyperscaler 定制 firmware、rack reference design、现场维护流程 | 一旦进入 reference design，生命周期 2-4 年 |
| 供应链规模 | TSMC wafer、substrate、DSP、laser、connector、test fixture | 能承诺交期的供应商更少，短缺期有溢价 |
| 故障成本 | 一个链路故障可闲置百万美元级 compute | 客户愿意为低 flap rate、telemetry、hot-swap 支付溢价 |

### 5.3 长期价值捕获

最可能长期高 ROIC / 高毛利的是：

1. **switch / NIC / retimer / SerDes silicon**：直接控制性能、延迟和可靠性，毛利 60-75% 可持续。
2. **互连 IP / EDA / compliance / test software**：标准越多、速率越高，验证越复杂，毛利 80%+。
3. **光 DSP / laser / SiPh PIC / CPO optical engine**：1.6T/3.2T/CPO 的共同瓶颈，技术迭代快。
4. **管理和诊断软件**：大规模 AI rack 的 uptime 价值高，可能从硬件附属变成独立收费。
5. **少数高端连接器/铜互连平台**：如果进入 top-side/CPC reference design，可获得高毛利；普通线缆会被竞争压价。

较难长期高毛利的是普通白牌 switch 组装、普通光模块 assembly、低端线缆和标准 PCB。它们收入很大，但会被多供应商和 hyperscaler 采购压价。

## 6. 2026 关键变化：三个拐点

### 拐点一：标准从纸面进入产品

2026-03 ESUN 1.0 发布，2026-04 UALink 2.0 系列规格发布，2026-05 Astera Scorpio X 320-lane shipping。三者叠加说明开放 scale-up 已从概念进入 silicon / switch / rack 交付窗口。

### 拐点二：AMD Helios 把开放 rack 变成商业产品

AMD Helios 72 GPU、31TB HBM4、260TB/s scale-up、43TB/s scale-out，HPE 将全球提供 Helios 架构，Celestica 负责 scale-up networking switches，并使用 UALoE。2026 年即使只是低量出货，也会给供应链一个真实 BOM。

### 拐点三：Ethernet 证明可承接 AI 后端和 scale-up

Broadcom Tomahawk Ultra 的 250ns switch latency、77B pps、SUE <400ns XPU-to-XPU，以及 Keysight/Broadcom 在 OFC 2026 做 800GE UEC LLR/CBFC 公共互操作演示，标志 Ethernet 正从 scale-out 网络压进 scale-up。

2026 最可能放量的子方向：

- UALoE / SUE / ESUN switch / NIC / retimer。
- PCIe 6 fabric switch、retimer、SCM。
- 224G AEC/CPC/top-side copper。
- 800G/1.6T optical module、DSP、laser、测试。
- Rack-scale management / telemetry / compliance。

## 7. 2027 关键变化：三个拐点

### 拐点一：native UALink 从 design-in 到 production ramp

如果 2026 年 IP、switch silicon、accelerator port、合规计划顺利，2027 年 native UALink 将从“Helios/ASIC rack 的下一代选项”变成真正出货。基准假设 2027 native UALink 只占非 NVIDIA 新增 rack 的 10-20%；乐观可到 25-35%；极度超预期可到 40%+。

### 拐点二：1.6T 成为新增 AI fabric 默认配置，3.2T/CPO 开始抢 design win

2027 年 1.6T 不再是样机，而是高端 spine / backend / scale-up extension 的默认选项；3.2T/400G-lane、CPO/CPX/NPO、OCS 开始在少数 hyperscaler 中形成第一批可复制 design win。

### 拐点三：custom ASIC rack 带来“非 NVIDIA fabric 空间”

OpenAI/Broadcom、Meta MTIA、Microsoft Maia、Google TPU8、AWS Trainium3/4、AMD MI400 都会在 2027 提高出货权重。只要这些平台不完全封闭，开放/半开放 scale-up silicon、NIC、retimer、copper、optics 的价值量会按每 rack 成倍增长。

2027 最可能放量的子方向：

- native UALink switch / endpoint / IP / compliance。
- ESUN/SUE multi-hop scale-up。
- PCIe 7 early design-in 与 optical-aware retimer。
- 1.6T optics、大规模 AEC/CPC、CPO pilot。
- In-Network Compute / collective offload switch。

## 8. 头部公司与细分清单

### 8.1 标准、生态与云厂

| 方向 | 公司/组织 |
|---|---|
| UALink promoter | Alibaba、AMD、Apple、Astera Labs、AWS、Cisco、Google、HPE、Intel、Meta、Microsoft、Synopsys |
| UALink contributors | Broadcom、Marvell、Arm、Cadence、Credo、Amphenol、Samtec、TE、Keysight、Lenovo、Dell、Fujitsu、ByteDance、H3C、ZTE、XConn、Montage、Lightmatter、Ayar Labs、Nokia、Qualcomm、Renesas 等 |
| ESUN / OCP | Meta、Microsoft、AMD、Arista、Arm、Broadcom、Cisco、HPE Networking、Marvell、NVIDIA、OpenAI、Oracle、OCP Networking Project |
| UEC | AMD、Arista、Broadcom、Cisco、HPE、Intel、Meta、Microsoft 等，以及大量 NIC/switch/optics/test 成员 |

### 8.2 Switch / NIC / retimer / connectivity silicon

- Broadcom：Tomahawk Ultra、Tomahawk 6、Jericho 4、Thor Ultra 800G NIC、Agera retimer、Sian/Taurus DSP、3.5D XPU、SUE/UEC/OCI。
- Astera Labs：Scorpio X 320-lane scale-up switch、Scorpio P PCIe 6 switch、Aries retimer、Leo CXL controller、Taurus SCM、COSMOS。
- Marvell：Teralynx / Prestera / Alaska / custom silicon、coherent DSP、NVLink Fusion custom XPU、CPO/SiPh。
- NVIDIA：Spectrum-X、ConnectX、BlueField、NVLink Fusion、CPO switch。
- AMD Pensando：Pollara、Vulcano UEC NIC / DPU。
- Cisco：Silicon One、Acacia optics、AI fabric 系统。
- Intel：IPU、Ethernet、Gaudi/Jaguar Shores 生态，UEC/UALink 参与。
- Credo：HiWire/ZeroFlap AEC、SerDes、DSP、OmniConnect、ALC、optics。
- 其他：Microchip、MaxLinear、Semtech、Parade、Montage、Renesas、Rambus、Alphawave、XConn、Cornelis Networks、Enfabrica、Celestial AI、Ayar Labs、Lightmatter。

### 8.3 光互联、硅光、CPO、OCS

- 模块/光器件：中际旭创、Eoptolink/新易盛、Coherent、Lumentum、Fabrinet、Cisco/Acacia、光迅科技、华工科技、海信宽带、天孚通信、剑桥科技、源杰科技、仕佳光子、博创科技。
- DSP/SiPh/光引擎：Broadcom、Marvell、Coherent、Lumentum、OpenLight、Ayar Labs、Lightmatter、Ranovus、Celestial AI、TeraHop、Molex、Samtec、Cisco/Acacia。
- OCS/光交换：Google Apollo 生态、iPronics、Calient、Polatis/HUBER+SUHNER、Nokia、Ciena。
- 光纤/连接/管理：Corning、Sumitomo、Senko、US Conec、Amphenol、Molex、TE、Samtec。

### 8.4 铜互连、连接器、PCB

- 连接器/线缆：Amphenol、TE Connectivity、Molex、Samtec、Luxshare/立讯精密、BizLink、FIT/Foxconn、Hirose、3M、Gore、Yamaichi。
- AEC/active copper silicon：Credo、Broadcom、Marvell、Semtech、MaxLinear、Spectra7。
- PCB/基板：Shennan/深南电路、沪电股份、胜宏科技、Ibiden、Unimicron、欣兴、Nan Ya PCB、AT&S、TTM。

### 8.5 系统/OEM/ODM/网络软件

- ODM / switch system：Celestica、Accton/Edgecore、Delta、UfiSpace、Quanta/QCT、Wiwynn、Wistron、Inventec、Foxconn、Supermicro。
- OEM / networking：Dell、HPE/Juniper、Lenovo、Cisco、Arista、Nokia、Ciena、H3C、ZTE、锐捷、新华三。
- 网络 OS / fabric 软件：SONiC、SAI、Broadcom SDK、Arista EOS、Cisco NX/IOS-XR、Juniper Junos/Apstra/Mist、DriveNets、Arrcus、Hedgehog、Nexthop。

### 8.6 EDA/IP/测试

- EDA/IP：Synopsys、Cadence、Siemens EDA、Alphawave、Rambus、Arteris、Avery、Ansys、Keysight EDA。
- 测试：Keysight、Teledyne LeCroy、Anritsu、VIAVI、Tektronix、Rohde & Schwarz。

## 9. 投资跟踪指标

1. UALink compliance / plugfest 是否在 2026H2 明确，是否出现第一批 native UALink switch silicon 客户。
2. AMD Helios 真实交付：HPE、Celestica、Oracle、Meta 或其他客户是否在 2026H2 形成可见出货。
3. Astera Scorpio X / P 出货节奏：2H26 ramp 是否兑现，2027 是否从单客户转多客户。
4. Broadcom Tomahawk Ultra / Tomahawk 6 / Thor Ultra 的客户数量、switch vendor design win、UEC/ESUN 功能启用程度。
5. 1.6T optics ASP 与交期：如果 2026H2 仍短缺，光器件利润率可继续上修。
6. AEC/CPC/top-side copper 的 224G/448G design win：尤其是 Luxshare、Samtec、Molex、TE、Amphenol、Credo。
7. PCIe 7 / PCIe 8 pathfinding：IP license、test equipment、connector standard 是否提前放量。
8. CPO/OCI/OCS 的现场可维护性：ELS 冗余、光引擎可插拔、故障率、客户 pilot。
9. 软件栈：ROCm / collective libraries / libfabric / SONiC / SAI / telemetry 是否支持 open scale-up。
10. 非 NVIDIA ASIC/GPU GW 级订单：OpenAI/Broadcom、Meta MTIA、Microsoft Maia、Google TPU、AWS Trainium、AMD MI400 的出货节奏是最大上游变量。

## 10. 主要来源

- 本项目：[全球 AI 芯片路线图与 2026-2027 产能释放预测](../ai_chip_research_2026_2027.md)
- 本项目：[OFC 2026 光通信大会更新](../conference_update/ofc_2026_conference_update.md)
- 本项目：[DesignCon 2026 更新](../conference_update/designcon_2026_conference_update.md)
- 本项目：[OCP EMEA Summit 2026 高密度调研](../conference_update/OCP_EMEA_Summit_2026_高密度调研报告.md)
- 本项目：[PCI-SIG DevCon 2026 更新](../conference_update/pci_sig_devcon_2026_update.md)
- [UALink 规格页](https://ualinkconsortium.org/specification/)
- [UALink 2026-04 规格更新新闻稿 PDF](https://ualinkconsortium.org/wp-content/uploads/2026/04/UALink-2.0-Specification-PR_FINAL.pdf)
- [UALink 2026 white paper](https://ualinkconsortium.org/wp-content/uploads/2026/01/UALink_White_Paper_Publication_Candidate_FINAL_VERSION.pdf)
- [UALink members](https://ualinkconsortium.org/members/)
- [OCP ESUN 1.0 发布博客](https://www.opencompute.org/blog/the-ocp-esun-10-specification-has-been-released)
- [OCP ESUN 1.0 specification PDF](https://www.opencompute.org/documents/ocp-esun-network-operator-requirements-base-specification-rev-1-0-final-pdf)
- [UEC 1.0 specification release](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/)
- [UEC expanding vision / scale-up transport / INC](https://ultraethernet.org/accelerating-ai-with-open-standards-uecs-expanding-vision/)
- [Astera Scorpio X 320-lane announcement](https://www.asteralabs.com/news/astera-labs-extends-leadership-in-open-ai-scale-up-networking-with-new-320-lane-scorpio-x-series-smart-fabric-switch/)
- [Astera Q1 2026 results](https://www.globenewswire.com/news-release/2026/05/05/3288259/0/en/astera-labs-reports-first-quarter-2026-financial-results.html)
- [Broadcom Tomahawk Ultra](https://investors.broadcom.com/news-releases/news-release-details/broadcom-ships-tomahawk-ultra-reimagining-ethernet-switch-hpc)
- [Broadcom Tomahawk 6 PDF](https://investors.broadcom.com/node/63146/pdf)
- [Broadcom OFC 2026 portfolio PDF](https://investors.broadcom.com/node/64036/pdf)
- [Broadcom Q1 FY2026 results / SEC 8-K](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm)
- [AMD open rack-scale AI infrastructure](https://www.amd.com/en/blogs/2025/amd-delivering-open-rack-scale-ai-infrastructure-to-unlock-agentic-ai.html)
- [AMD Helios built on Meta OCP design](https://www.amd.com/en/blogs/2025/amd-helios-ai-rack-built-on-metas-2025-ocp-design.html)
- [AMD rack-scale AI and agentic AI](https://www.amd.com/en/solutions/data-center/insights/rack-scale-ai-and-the-promise-of-agentic-ai.html)
- [Celestica and AMD Helios collaboration PDF](https://corporate.celestica.com/node/17196/pdf)
- [AMD and HPE Helios collaboration PDF](https://d1io3yog0oux5.cloudfront.net/_82bea3dbebc803d58a0640ab0620fe45/amd/news/2025-12-02_AMD_and_HPE_Expand_Collaboration_to_Advance_Open_1269.pdf)
- [NVIDIA NVLink Fusion](https://nvidianews.nvidia.com/news/nvidia-nvlink-fusion-semi-custom-ai-infrastructure-partner-ecosystem)
- [NVIDIA / Marvell NVLink Fusion 2026](https://nvidianews.nvidia.com/news/nvidia-ai-ecosystem-expands-as-marvell-joins-forces-through-nvlink-fusion)
- [IDC Ethernet switch market 2025](https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/)
- [Dell'Oro via SDxCentral: AI back-end Ethernet switch sales tripled](https://www.sdxcentral.com/news/ethernet-switch-sales-triple-as-hyperscale-ai-demand-soars/)
- [650 Group: Data Center AI Networking nearly $20B in 2025](https://650group.com/press-releases/data-center-ai-networking-to-surge-to-nearly-20b-in-2025-according-to-650-group/)
- [Credo Q3 FY2026 results via SEC](https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm)
- [Credo ZeroFlap AEC](https://credosemi.com/products/zeroflapaec/)
- [Keysight 800GE UEC LLR/CBFC OFC 2026](https://www.keysight.com/se/en/about/newsroom/news-releases/2026/0316_pr26-051-keysight-advances-ai-networking-with-ultra-ethernet-llr-and-cbfc-interoperability-demonstration-at-ofc-2026.html?wcmmode=disabled)

# 行业调研：【宽带接入、PON、DOCSIS 4.0与Wi-Fi 7】

> 版本日期：2026-05-08  
> 研究口径：本报告聚焦固定宽带接入设备、PON、DOCSIS 4.0、家庭/企业 Wi-Fi 7、运营商网关与接入侧软件平台。美元区间主要为设备、软件、CPE、运营商采购订单或可归因收入池，不等同于运营商宽带服务总收入。  
> 投资假设：对 2026-2027 AI 计算中心建设、推理流量、AI PC/手机、企业 AI 应用和边缘 AI 采用极度乐观的上行情景；对没有直接披露的数据，采用“公开锚点 + 单位出货/ASP + 运营商节奏”的乐观推导。

## 0. 一句话结论

宽带接入不是 AI 数据中心硬件的最直接上游，但在 2026 会被三股力量同时推高：第一，AI 数据中心和云推理把骨干、城域、企业园区和边缘节点的流量基线抬高；第二，家庭与企业端的 AI PC、4K/8K 视频、实时协作、云游戏、视频生成和安全摄像头，使“上行、低时延、室内覆盖和稳定性”从可选卖点变成续约/留存工具；第三，运营商在 fiber overbuild、BEAD、DOCSIS 4.0、Wi-Fi 7 CPE 和托管 Wi-Fi 上开始重新进入资本开支周期。

最现实的 2026 主线是 **XGS-PON + Wi-Fi 7 + DOCSIS 3.1 high-split/DAA + Comcast 型 DOCSIS 4.0 FDX 扩围**。50G PON、25GS-PON、DOCSIS 4.0 ESD 大规模化、6GHz 标准功率 AFC、AI-native gateway 是 2027 预期差。极度超预期情景下，2027 年 50G PON 与 DOCSIS 4.0 会从“高端试点”变成“运营商防御 fiber overbuild 的战略采购”，Wi-Fi 7 则会成为新装家庭网关和企业 AP 的默认配置。

最值得跟踪的投资层级不是低毛利 CPE 组装，而是：**PON/DOCSIS/Wi-Fi 芯片与参考设计、25G/50G PON 光器件、DOCSIS 4.0 放大器/节点/RPD/vCMTS、云管 Wi-Fi/AIOps 平台、运营商深度认证网关、BEAD/FTTH 被动光网络材料和施工交付**。

## 1. 资料锚点与校验

| 公开锚点 | 数字/事实 | 对本报告的含义 |
|---|---:|---|
| Dell'Oro 2026-03 宽带接入报告 | 2025Q4 全球 broadband access equipment 收入 $4.8B，QoQ +7%、YoY +2%；报告覆盖 cable、DSL、PON 设备的收入、ASP、端口/单位出货。来源：[Dell'Oro/PRNewswire](https://www.prnewswire.com/news-releases/broadband-access-equipment-to-return-to-growth-in-2026-according-to-delloro-group-302709983.html) | 2026 接入设备从三年压制周期回到增长，全球年化设备池约 $18B-$21B，是 PON/DOCSIS 设备预测的总锚。 |
| Dell'Oro 2026 预测摘录 | 宽带接入设备 2025-2030 CAGR 约 0.3%，2028 收入峰值约 $18.8B；PON 设备 2025-2030 CAGR 约 1.9%；PON ONT 2025 全球出货 158M。来源：[Electronics Weekly](https://www.electronicsweekly.com/news/business/0-3-growth-2025-30-for-broadband-access-equipment-market-2026-01/)、[Advanced Television](https://www.advanced-television.com/2026/03/12/forecast-broadband-access-equipment-return-to-growth-in-2026/) | 总市场不是爆炸式，但结构性爆点在 XGS-PON、Wi-Fi 7、DOCSIS 4.0、FWA CPE 和高端网关。 |
| 美国 FTTH | 2025 年美国新增 FTTH passings 11.8M，总 passings 98.3M；2026 100% bonus depreciation 可能推动 FTTH CapEx +5%-15%。来源：[Fiber Broadband Association](https://fiberbroadband.org/2025/12/16/fiber-broadband-association-reports-historic-fiber-deployment-highs/) | 美国 fiber build 继续强，XGS-PON、ONT、光缆、分光器、施工和 Wi-Fi 7 网关受益。 |
| BEAD 进度 | 截至 2026-05-04，56 个州/地区已全部提交 Final Proposal，54 个获 NTIA 批准，52 个获 NIST 批准可用资金，50 个完成 award agreement。来源：[NTIA BEAD dashboard](https://www.ntia.gov/funding-programs/internet-all/broadband-equity-access-and-deployment-bead-program/progress-dashboard) | BEAD 从规划进入采购/施工，2026 H2 开始有订单，2027 放量更明显。 |
| CableLabs DOCSIS 2026 | 截至 2024-12，美国 cable HFC 住宅位置中 98% 可获得 1Gbps+ 下行；100Mbps+ 上行从约 1% 升到 32%，1Gbps+ 上行升到 9%；DOCSIS 4.0 已展示 10G-class 下行、3Gbps/5.5Gbps 上行，正在研究 3GHz 和 6GHz HFC 扩展。来源：[CableLabs](https://www.cablelabs.com/blog/docsis-technology-whats-changed-in-the-past-year-and-why-it-matters) | Cable 短期主线是 high-split、DAA、vCMTS、DOCSIS 3.1+，DOCSIS 4.0 是 2026-2027 高弹性增量。 |
| DOCSIS 4.0 互通 | 2026-03 CableLabs 第 16 次 DOCSIS 4.0 Interop·Labs 验证了多厂商安全、认证和加密机制，2026-05 继续互通测试。来源：[CableLabs](https://www.cablelabs.com/blog/authentication-and-privacy-docsis-4-0-interop-focuses-on-security) | 认证/互通仍是节奏阀门，但 D4.0 已从实验室速度转向部署可信度。 |
| Comcast/CommScope | Comcast 2023 推出全球首个 DOCSIS 4.0 商用；2024 已扩至 6 个市场、100 万+ homes；CommScope 2025 称下一代 unified FDX/ESD RPD、amps 支持 1.8GHz ESD 与 FDX。来源：[Comcast](https://corporate.comcast.com/press/releases/comcast-commscope-notch-milestone-next-generation-connectivity-millions-across-us)、[CommScope](https://commscopeholdingcompanyinc.gcs-web.com/news-releases/news-release-details/commscope-and-comcast-accelerate-rollout-docsis-40-amplifiers) | Comcast 是 D4.0 FDX 第一条实战曲线；FDX amps、nodes、RPD、网关是 2026 最明确 D4.0 订单。 |
| Charter | 2026Q1 Charter 有 29.6M Internet customers，Q1 CapEx $2.9B，FY2026 CapEx 预期约 $11.4B；10-K 称当前把频谱扩到 1.2GHz、high split 与 DAA，之后部署 DOCSIS 4.0 并扩至 1.8GHz。来源：[Charter Q1 2026](https://ir.charter.com/static-files/8f4715b9-1c59-4a03-8829-05e75fdbb368)、[Charter 10-K](https://www.sec.gov/Archives/edgar/data/0001091667/000109166726000017/chtr-20251231.htm) | Charter 2026 更像“D3.1 high-split + DAA 的大采购年”，D4.0 收入更偏 2027。 |
| Wi-Fi 7 | WBA 预计 Wi-Fi 7 AP 出货从 2024 年 26.3M、2025 年 66.5M 增至 2026 年 117.9M；WBA 调研中 38% 受访者计划 2026 部署 Wi-Fi 7，32% 计划 AI/Cognitive networks。来源：[WBA 2026 predictions](https://wballiance.com/wireless-broadband-alliance-reveals-its-wi-fi-predictions-for-2026-and-beyond/)、[WBA Industry Report](https://wballiance.com/wba-industry-report-2026-finds-62-of-survey-respondents-more-confident-to-invest-in-wi-fi-than-12-months-ago/) | Wi-Fi 7 是 2026 最确定的 CPE/AP 量产升级；AI AIOps 是软件毛利来源。 |
| Wi-Fi 7 企业 WLAN | IDC 4Q25 显示企业 WLAN 增长由 Wi-Fi 7 带动，全球企业 WLAN 支出 60% 已流向 Wi-Fi 6E/7。来源：[IDC](https://www.idc.com/resource-center/blog/worldwide-enterprise-wlan-grew-13-9-driven-by-wi-fi-7-deployments/) | 企业端 2026 是 Wi-Fi 7 ROI 验证年，AFC、6GHz、MLO、AIOps 决定溢价。 |
| Nokia PON | Nokia 50G/25G PON 可在现有 Lightspan MF / Quillion line card 上支持 GPON、XGS、25G、50G 和未来光模块；2026Q1 Fixed Networks 收入 -13%，但公司称转向高毛利产品。来源：[Nokia 50G PON](https://www.nokia.com/newsroom/nokia-unveils-worlds-first-50g-pon-solution-for-post-quantum-enterprise-connectivity/)、[Nokia Q1 2026](https://www.nokia.com/newsroom/nokia-corporation-interim-report-for-q1-2026/) | 25G/50G PON 不是完全替换 XGS-PON，而是在同一平台上卖高端端口、企业 SLA 和投资保护。 |
| 中国 50G PON | ZTE 与中国移动江苏 2025-06 推出 50G PON FMC 社区，三代五模 Combo，支持对称 50Gbps 和 50G FTTR。来源：[ZTE](https://www.zte.com.cn/global/about/news/china-mobile-and-zte-take-the-lead-in-launching-a-50G-PON-based-FMC-residential-community-in-China.html) | 中国会是 50G PON 初期最大示范市场，但 2026 仍以 10G/XGS 与 FTTR 为主。 |
| PON 互通 | Broadband Forum 2025 Plugfest 测试 50G PON、25GS-PON、XGS-PON，参加者包括 Airoha、Calix、Nokia、Sagemcom、Evolution Digital、Hitron、MT2。来源：[Broadband Forum](https://www.broadband-forum.org/news/record-vendor-turnout-powers-high-speed-fiber-device-compatibility/) | 25G/50G PON 生态已进入多厂商互通阶段，2026 是认证和小批部署窗口。 |
| Calix | 2025 全年收入 $1B、非 GAAP 毛利率 58%；2026Q1 收入 $280M、YoY +27%、非 GAAP 毛利率 57.2%。来源：[Calix Q4 2025](https://investor-relations.calix.com/sec-filings/all-sec-filings/content/0001406666-26-000004/ex992stockholderletter25q4.htm)、[Calix Q1 2026](https://www.stocktitan.net/sec-filings/CALX/8-k-calix-inc-reports-material-event-2c5a13d94a83.html) | 平台化/云管/托管 Wi-Fi 比纯硬件更能定价，区域宽带商升级周期恢复。 |
| Qualcomm Wi-Fi 7/Edge AI | Wi-Fi 7 平台支持 320MHz、4K QAM、MLO，平台容量最高 33Gbps；Networking Pro A7 Elite 把 Wi-Fi 7 与 edge AI 整合。来源：[Qualcomm Wi-Fi 7](https://www.qualcomm.com/wi-fi/wi-fi-7)、[Qualcomm A7 Elite](https://www.qualcomm.com/news/releases/2024/10/qualcomm-unveils-the-networking-pro-a7-elite-platform--the-first) | AI gateway 不是概念题，芯片平台已把 NPU/AIOps/网关融合成产品方向。 |
| Broadcom/Comcast DOCSIS AI chipset | Broadcom/Comcast 统一 DOCSIS 4.0 芯片支持 FDX、ESD 或两者同时运行，并在 node、amp、modem 中嵌入 AI/ML。来源：[Comcast/Broadcom](https://corporate.comcast.com/press/releases/comcast-broadcom-develop-ai-powered-access-network-pioneering-new-chipset) | D4.0 芯片的核心价值是统一 FDX/ESD 生态、降低库存碎片，并把 telemetry/AI 变成运营商网络能力。 |
| 内存成本 | TrendForce 预计 AI server 需求推动 2026Q2 DRAM/NAND 合约价继续上涨，2026 供应短缺明显，实质扩产要到 2027 年末或 2028。来源：[TrendForce](https://www.trendforce.com/presscenter/news/20260331-12995.html) | AI 数据中心会反向挤压路由器、网关、ONT 的 DRAM/NAND 成本，是 2026 CPE 毛利最大不确定性。 |

## 2. 2026 AI 计算中心建设下的机遇、挑战与技术路径

### 2.1 这个行业为什么会被 AI 拉动

1. **上行与低时延从小众需求变成留存工具。** AI 视频会议、云桌面、代码/设计协作、家庭安全摄像头、边缘 NAS、云备份和实时生成式应用都提高上行与低抖动需求。DOCSIS high-split、D4.0 FDX、XGS-PON、25G/50G PON 的共同卖点都是“更高上行 + 更低延迟 + 更高稳定性”。
2. **企业 AI 与 AI PC 让企业 WLAN 进入更新周期。** 2026 年 Wi-Fi 7 的价值不是理论峰值，而是 6GHz、MLO、QoS、AIOps、AP cloud telemetry、智能漫游和高密会议室/工厂/学校场景。
3. **AI 数据中心挤占城域光纤、施工、光器件和电力交付资源。** 这对接入行业既是机会也是挑战：有数据中心/企业园区资源的运营商会升级城域与接入，纯住宅 overbuild 项目则可能被光缆、施工和融资成本挤压。
4. **运营商 CPE 从“成本中心”变成“家庭入口”。** Qualcomm、Broadcom、Calix、Plume、Charter 等方向都指向一个现实：网关/AP 将承担安全、家宽体验、设备画像、AI AIOps、家庭边缘推理和移动融合。
5. **AI 带来存储/内存成本传导。** 高端网关需要更多 DRAM/NAND、10G/2.5G LAN、Wi-Fi 7 RF FEM 和更强 CPU/NPU。AI 数据中心抢内存会压缩低端 CPE 毛利，利好有价格传导能力和平台收入的厂商。

### 2.2 当前正在使用的主流技术

| 技术 | 2026 状态 | 典型用途 | 投资含义 |
|---|---|---|---|
| GPON / EPON | 存量巨大，新增主要在低 ARPU 和海外新建市场 | 1Gbps 以下/低成本 FTTH | 收入稳定但 ASP 低，替换周期会给低价 ONT 和兼容 OLT 带来量。 |
| XGS-PON / 10G EPON | 全球 FTTH 新建主力，北美、欧洲、中东、拉美继续扩张 | 1-10Gbps residential/SMB，BEAD，fiber overbuild | 2026 最确定 PON 设备收入池；ONT 量大、OLT 端口和 combo card 利润更好。 |
| 25GS-PON | Nokia 生态领先，Google Fiber、Frontier、enterprise/wholesale/MDU 场景试点 | 10Gbps+ premium broadband、企业接入、mobile xHaul | 2026 小批高毛利，2027 随 10G 套餐竞争和企业 SLA 放量。 |
| 50G PON / HS-PON | 中国、Nokia/ZTE/Huawei/Calix/Airoha 等进入互通和示范 | enterprise、campus、FTTR、premium residential、切片 | 2026 仍是 trial/flagship，2027 是商业化预期差；ONU optics 成本决定节奏。 |
| DOCSIS 3.1 high-split / mid-split | Cable 主流升级；Charter 2026 核心 | 提升上行到 100Mbps-1Gbps+，延长 HFC 资产寿命 | 2026 cable 采购大头在 amps、taps、RPD、vCMTS、3.1+ modem。 |
| DOCSIS 4.0 FDX | Comcast 领先，FDX amps/nodes/gateway 扩围 | 对称 multi-gig over existing HFC | 2026 最明确 D4.0 订单来自 Comcast 生态；后续看 unified chips。 |
| DOCSIS 4.0 ESD/FDD | Charter/Cox/欧洲 cable 更偏该方向，但大规模节奏慢于 high-split | 1.8GHz 扩频、5-10Gbps 下行、上行增强 | 2026-2027 高弹性，但受 1.8GHz plant、passives、CPE 认证约束。 |
| DAA / Remote PHY / Remote MACPHY / vCMTS | Comcast、Charter、Cox、Liberty 等长期方向 | 分布式接入、降低 headend、软件化 capacity | Harmonic、CommScope、Vecima、Cisco/legacy 受益；软件和 RPD 价值更高。 |
| Wi-Fi 6E / Wi-Fi 7 | 2026 Wi-Fi 7 进入运营商网关和企业 AP 主流 | 6GHz、MLO、320MHz、4K QAM、低时延 | 2026 最确定 CPE/AP 升级；芯片、RF、cloud-managed Wi-Fi 价值上移。 |
| Standard Power 6GHz / AFC | 美国/加拿大进展快，2026 大型场馆、教育、工业加速 | 室外/大空间 6GHz Wi-Fi 7 覆盖 | 使 enterprise Wi-Fi 7 从“近距离峰值”走向可规划覆盖。 |

### 2.3 项目内 AI 芯片路线对本行业的映射

项目内 AI 芯片资料显示，2026-2027 价值和出货权重最高的平台大致是 NVIDIA GB300/B300、GB200/B200、Vera Rubin、AWS Trainium2/3、Google TPU Ironwood/TPU8、AMD MI350/MI400、Microsoft Maia 200、Meta MTIA、OpenAI/Broadcom custom accelerator、中国 Ascend/Cambricon 等。它们对本行业的影响不是直接消耗 PON/DOCSIS/Wi-Fi 芯片，而是通过 **流量、企业园区、边缘节点、运营商城域网和客户体验指标** 传导。

| AI 芯片/平台 | 2026-2027 技术背景 | 对宽带接入行业的拉动 |
|---|---|---|
| NVIDIA GB300/B300、GB200 | 2026 主力，AI 数据中心网络以 800G/1.6T、NVLink/InfiniBand/Ethernet 为核心 | 拉动城域光纤和运营商企业专线；住宅端主要通过 AI 应用提高上行和低时延要求。 |
| NVIDIA Rubin / Rubin Ultra | 2026 H2 起步、2027 放量，HBM4/液冷/高密集群 | 若推理多模态爆发，运营商会加速 fiber backhaul、edge cloud 和企业 Wi-Fi 7。 |
| Google TPU Ironwood/TPU8 | 推理优先、TPU8 训练/推理分化，Google/Anthropic 多云 | Google Fiber/云边协同更可能验证 25G/50G PON、OCS/光网络和 AI home use cases。 |
| AWS Trainium2/3/4 | Rainier/Anthropic GW 级，云端推理成本下降 | 推理价格下降会扩大端侧用户调用频率，增加家庭/SMB 上行、Wi-Fi 与 CDN/edge 需求。 |
| AMD MI350/MI400 Helios | 2026 H2-2027 机架级竞争增强 | 多供应商 GPU 降低 AI 服务成本，间接推高 AI 应用流量。 |
| Microsoft Maia 200 | Azure/Copilot 推理，自研芯片 + HBM/SRAM | 企业 Copilot/AI PC 使用强度提升，企业 WLAN/Wi-Fi 7 和 SD-Branch 升级受益。 |
| Meta MTIA / OpenAI-Broadcom | 自研 ASIC 从 2026 H2 起步，2027 可能 GW 级 | 社交/视频/agentic 推理爆发会提升消费者宽带流量；Broadcom 同时在接入/DOCSIS/Wi-Fi 芯片有生态协同。 |
| 中国 Ascend/Cambricon | 国产 AI 云与政企推理集群放量 | 中国 10G/50G PON、FTTR、Wi-Fi 7/7+、政企园区网升级更快。 |

### 2.4 技术成熟与放量时间：三情景

| 子方向 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观 | 2027 极度超预期 |
|---|---|---|---|---|---|---|
| XGS-PON | FTTH 新建默认技术，北美/欧洲/拉美/中东继续扩张 | BEAD 订单 H2 明显落地 | 运营商因 cable 竞争加速把 2G/5G 套餐推为主流 | 继续主导 PON 收入 | XGS-PON + Wi-Fi 7 网关成新装标配 | XGS-PON ONT 量价齐升，50G 推迟但 XGS 赚满 |
| 25GS-PON | 企业、MDU、Google Fiber/Nokia 生态小批 | 高端住宅 10G+ 套餐驱动 | 若 50G optics 成本高，25G 成为过渡主线 | 小规模商用放量 | 北美/澳洲/欧洲多运营商采用 | 25G 成为 premium PON 默认路线之一 |
| 50G PON | 中国/企业示范，Nokia/ZTE/Huawei/Calix 试点 | 中国运营商加速 50G PON + FTTR | 50G Combo optics 成本快速下降，新增端口超预期 | 企业/园区/高端住宅商用初期 | 50G 端口收入进入 $2B-$6B 池 | 中国 + 中东 + 北美高端客户形成 $8B-$12B 订单池 |
| DOCSIS 3.1 high-split/DAA | Charter、Cox、欧洲 cable 主线，RPD/vCMTS/amps 订单 | Cable 面对 fiber 抢客加速高上行升级 | 供应商交付顺利，high-split 覆盖率跃升 | 继续放量但逐步让位 D4 | 高上行套餐显著降低 churn | D3.1+ 与 D4 混合网络快速覆盖大多数 cable homes |
| DOCSIS 4.0 FDX | Comcast 扩围，FDX amps/gateway 供货 | Comcast 从百万 homes 级迈向多百万 homes | FDX unified chipset 多 ODM 供货，市场感知加速 | Comcast 规模化、其他 FDX operator 跟进 | D4.0 FDX 对称 2G/5G 套餐常态化 | D4 FDX 成 cable 防御 FTTH 的关键叙事 |
| DOCSIS 4.0 ESD/FDD | 认证/设备准备，Charter 仍以 1.2GHz/high split 为主 | Charter/Cox 1.8GHz 采购提前 | Cox/Charter 合并后统一路线加速 | 2027 开始规模部署 | ESD/FDD 进入大规模 HFC upgrade | D4.0 ESD + DAA 在北美/欧洲形成 $5B+ 年订单 |
| Wi-Fi 7 residential CPE | 新装高端网关/路由器主流 | 运营商把 Wi-Fi 7 作为降 churn 工具 | AI PC/手机换机拉动用户主动升级 | 中高端网关默认 Wi-Fi 7 | 低端双频 Wi-Fi 7 下沉 | Wi-Fi 7 CPE 收入峰值提前到 2027 |
| Enterprise Wi-Fi 7 | 高密办公室、教育、医疗、酒店、工厂升级 | 6GHz/AFC 与 AI AIOps 形成 ROI | 企业 AI app + AI PC 让 Wi-Fi 7 预算前置 | Wi-Fi 7 成 enterprise AP 新主流 | SP 6GHz/AFC 大规模化 | Wi-Fi 7 + AI/Cognitive WLAN 支出超过 Wi-Fi 6/6E |
| AI-native gateway / AIOps | Qualcomm/Broadcom/Calix/Plume 平台化 | 运营商开始把安全、诊断、边缘 AI 打包收费 | 网关 NPU/AI service 形成 ARPU 增量 | 托管 Wi-Fi 软件 attach 上升 | 家庭 AI agent、安全、能耗管理成为套餐 | 网关从低毛利硬件变成高毛利 platform endpoint |

### 2.5 2026 最可能赚钱的技术路径

1. **XGS-PON OLT/ONT + Wi-Fi 7 HGS 网关。** 这是最大量、最少争议的路线，适配 FTTH 新建、overbuild、BEAD、MDU 和 2G/5G 家宽套餐。
2. **DOCSIS high-split/DAA/vCMTS + DOCSIS 4.0 FDX 扩围。** 2026 cable 不会等待 D4.0 全面完美化，会先买 1.2GHz、high-split、RPD、amps、vCMTS 和 D3.1+ CPE；Comcast 型 FDX 是 D4.0 第一条实战曲线。
3. **Wi-Fi 7 AP/CPE + cloud-managed Wi-Fi/AIOps。** 运营商把 Wi-Fi 体验作为留存和 upsell 入口，企业把 Wi-Fi 7 当作 AI PC/IoT/视频协作的底座。
4. **PON/DOCSIS/Wi-Fi 芯片和高端光器件。** 50G PON、D4.0 unified chipset、Wi-Fi 7/8、10G LAN、2.5G/10G switch PHY、FEM、burst-mode optics 属于小体量高壁垒。

## 3. 已经开始放量的关键产品：规模、渗透率与利润率

> 口径说明：以下“3个月/1年/2年市场规模”为从 2026-05-08 起的全球累计设备/软件/订单收入池估算；不是运营商宽带服务收入。渗透率为该子技术在对应新增采购或装机升级中的占比。

### 3.1 已放量产品市场规模与渗透率

| 已放量产品/技术 | 当前放量证据 | 未来3个月：基准/乐观/极超 | 未来1年：基准/乐观/极超 | 未来2年：基准/乐观/极超 | 渗透率路径：基准/乐观/极超 |
|---|---|---:|---:|---:|---|
| XGS-PON OLT/ONT/Combo PON | Dell'Oro 称 XGS-PON 仍主导，FBA 美国 2025 新增 FTTH passings 11.8M | $2.4-3.2B / $3.2-4.0B / $4.0-5.0B | $9-13B / $13-17B / $17-22B | $19-28B / $28-38B / $38-52B | 新增 FTTH PON 端口 45%-60% -> 55%-70% -> 65%-80%；极超 2027 新装高端区域 85%+ |
| GPON/EPON 低成本 ONT 与替换 | 158M PON ONT 年出货中仍大量为 GPON/EPON | $1.2-1.8B / $1.8-2.2B / $2.2-2.8B | $4.5-6.5B / $6.5-8.5B / $8.5-11B | $8-12B / $12-16B / $16-21B | 新增低 ARPU PON 仍 30%-45%，两年后降至 20%-35%；极超因新兴市场维持 40% |
| FTTR / 室内光网络 / 高端家庭网关 | 中国运营商 FTTR 推动，50G PON 社区把 FTTR 作为示范 | $0.5-1.0B / $1.0-1.6B / $1.6-2.5B | $2.5-5B / $5-8B / $8-13B | $6-12B / $12-22B / $22-35B | 中国新装中高端 FTTH 15%-25% -> 25%-40%；海外仍 <5%-10%；极超海外 MDU 采用 |
| DOCSIS 3.1 high-split / 1.2GHz upgrade | Charter 10-K 明确 1.2GHz/high split/DAA，CableLabs 显示上行覆盖快速提升 | $0.8-1.3B / $1.3-1.8B / $1.8-2.5B | $3.5-5.5B / $5.5-8B / $8-11B | $7-11B / $11-17B / $17-25B | Cable 新增升级节点 35%-50% -> 50%-65% -> 60%-75%；极超大 MSO 加速 |
| DAA/RPD/vCMTS/Remote PHY | Comcast 100k digital nodes 历史基础，Charter/CableLabs DAA 主线 | $0.7-1.2B / $1.2-1.8B / $1.8-2.6B | $3-5B / $5-8B / $8-12B | $7-12B / $12-20B / $20-30B | 大型 cable upgrade 中 40%-55% -> 55%-70%；极超 DAA 成所有新增 D4 项目前置 |
| DOCSIS 4.0 FDX amps/nodes/gateways | Comcast 商用领先，CommScope 推 FDX/unified amps 和 RPD | $0.3-0.8B / $0.8-1.5B / $1.5-2.5B | $1.5-3.5B / $3.5-6.5B / $6.5-10B | $4-9B / $9-16B / $16-28B | 北美 cable homes D4.0 active availability 低个位数 -> 8%-15%；极超 2027 达 20%-30% |
| DOCSIS 3.1+/4.0 CPE 与 Wi-Fi 7 cable gateway | XB10、Hitron CODA6021、Vantiva/Sercomm/CommScope/Hitron 供应链 | $0.4-0.9B / $0.9-1.4B / $1.4-2.2B | $2-4B / $4-7B / $7-11B | $5-10B / $10-18B / $18-30B | Cable 新发高端 CPE 中 Wi-Fi 7 25%-40% -> 50%-70%；D4 modem <5% -> 10%-25% |
| Residential Wi-Fi 7 router/AP/mesh | WBA/ABI 预计 Wi-Fi 7 AP 2026 出货 117.9M | $1.8-2.8B / $2.8-4.0B / $4.0-5.5B | $8-12B / $12-17B / $17-24B | $18-28B / $28-42B / $42-60B | 新发中高端住宅 CPE 25%-40% -> 45%-65% -> 65%-80%；极超 2027 低端下沉 |
| Enterprise Wi-Fi 7 AP + WLAN controller/cloud | IDC：企业 WLAN 支出 60% 流向 Wi-Fi 6E/7；WBA：Wi-Fi 7 为 2026 最可能部署技术 | $1.2-2.0B / $2.0-2.8B / $2.8-4.0B | $6-9B / $9-13B / $13-18B | $14-22B / $22-32B / $32-45B | 企业 AP 新采购 Wi-Fi 7 20%-35% -> 40%-60% -> 60%-75%；极超高密场景 80%+ |
| Cloud-managed Wi-Fi / AIOps / home security services | Calix 57%+ GM，Plume/Charter、Juniper Mist、Cisco/Meraki 等 | $0.5-0.9B / $0.9-1.4B / $1.4-2.2B | $2.5-4.5B / $4.5-7B / $7-11B | $6-11B / $11-18B / $18-30B | 新装运营商 CPE software attach 35%-50% -> 50%-70%；极超 80%+ |
| BEAD/FTTH 被动光网络材料：光缆、分路器、closures、cabinets | NTIA 资金释放，Corning 称 BEAD 从规划转采购 | $2-4B / $4-6B / $6-9B | $10-18B / $18-28B / $28-42B | $25-45B / $45-70B / $70-100B | 美国未覆盖区域 fiber 项目 2026 H2 起动，2027 是主放量；极超取决于劳动力和 BABA 供应 |

### 3.2 已放量产品增长与利润率

| 已放量产品/技术 | 未来1年收入增速：基准/乐观/极超 | 当前毛利率区间 | 1年毛利率：基准/乐观/极超 | 2年毛利率：基准/乐观/极超 | 主要毛利决定因素 |
|---|---:|---:|---:|---:|---|
| XGS-PON OLT/ONT/Combo | +8%-18% / +18%-30% / +30%-45% | OLT 35%-50%，ONT 15%-28%，平台厂 blended 35%-58% | 35%-52% / 40%-55% / 45%-60% | 34%-50% / 40%-55% / 45%-62% | OLT 端口密度、combo optics、运营商认证、软件管理、ONT 价格竞争。 |
| GPON/EPON 低成本 | -5%-+5% / +5%-12% / +12%-20% | 10%-22% | 9%-20% / 12%-22% / 15%-25% | 8%-18% / 10%-20% / 12%-24% | 低端 ASP、内存涨价、ODM 规模、国家补贴项目。 |
| FTTR / 室内光网络 | +25%-45% / +45%-70% / +80%+ | 25%-45% | 28%-48% / 35%-55% / 45%-65% | 25%-45% / 35%-55% / 45%-65% | 套餐绑定、室内施工能力、光模块/分光器成本、运营商补贴。 |
| DOCSIS high-split/1.2GHz | +20%-35% / +35%-55% / +60%+ | 25%-40% | 28%-42% / 32%-46% / 38%-52% | 25%-40% / 30%-45% / 35%-50% | 放大器/节点短缺、field hardened 认证、MSO 长单价格。 |
| DAA/RPD/vCMTS | +25%-45% / +45%-70% / +80%+ | 硬件 30%-45%，软件 55%-75% | 35%-50% / 40%-55% / 50%-65% | 35%-50% / 45%-60% / 55%-70% | vCMTS 软件占比、RPD 认证、operator lock-in。 |
| DOCSIS 4.0 FDX/ESD ecosystem | +80%-150% / +150%-250% / +300%+ | 早期硬件 35%-50%，芯片 55%-70% | 38%-55% / 45%-60% / 55%-70% | 35%-50% / 42%-58% / 50%-68% | 供不应求、统一芯片、多运营商认证、现场返修率。 |
| DOCSIS/Wi-Fi 7 cable gateway | +50%-100% / +100%-180% / +200%+ | ODM 10%-18%，品牌/CPE 平台 20%-35%，芯片 55%-70% | 12%-25% / 20%-35% / 30%-45% | 10%-22% / 18%-32% / 25%-42% | DRAM/NAND、Wi-Fi 7 RF、10G PHY、运营商租赁模式。 |
| Residential Wi-Fi 7 | +60%-100% / +100%-160% / +180%+ | 芯片 50%-65%，品牌 25%-40%，ODM 8%-15% | 25%-38% / 30%-42% / 35%-48% | 22%-35% / 28%-40% / 32%-45% | 初期价格低、内存涨价、6GHz/tri-band 配置、渠道竞争。 |
| Enterprise Wi-Fi 7 | +35%-55% / +55%-80% / +100%+ | 品牌 AP 45%-65%，cloud 70%-85% | 45%-65% / 50%-68% / 55%-72% | 42%-62% / 48%-68% / 55%-75% | AIOps/cloud license、AFC、PoE/switch attachment、客户认证。 |
| Cloud-managed Wi-Fi/AIOps | +25%-45% / +45%-70% / +90%+ | 65%-90% | 68%-88% / 72%-90% / 78%-92% | 68%-88% / 75%-90% / 80%-93% | 软件 attach、数据规模、运营商 churn reduction、AI 模型成本。 |
| BEAD/FTTH passive | +15%-30% / +30%-50% / +70%+ | 光纤/线缆 20%-35%，连接器/closures 25%-45% | 22%-38% / 28%-45% / 35%-55% | 20%-35% / 25%-42% / 30%-50% | BABA 约束、光纤预制化、施工节奏、原材料和运费。 |

## 4. 在研关键产品与细分技术：规模、渗透率与利润率

### 4.1 未来快速增长技术清单

| 在研/早期商业化技术 | 当前状态 | 未来3个月：基准/乐观/极超 | 未来1年：基准/乐观/极超 | 未来2年：基准/乐观/极超 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 50G PON OLT/ONU/Combo optics | Nokia/ZTE/Huawei/Calix/Airoha 等互通与示范，中国已有 50G 社区 | $0.08-0.20B / $0.20-0.45B / $0.45-0.80B | $0.6-1.5B / $1.5-3B / $3-6B | $2-6B / $6-12B / $12-22B | PON 新增端口 <1% -> 2%-5% -> 5%-12%；极超 2027 中国/中东高端端口 15%-20% |
| 25GS-PON mass-market CPE | Nokia 生态较成熟，Google Fiber/Frontier/altafiber/enterprise 方向 | $0.10-0.25B / $0.25-0.50B / $0.50-0.90B | $0.8-1.8B / $1.8-3.5B / $3.5-6B | $2.5-6B / $6-10B / $10-16B | 高端 FTTH/企业 PON 2%-4% -> 5%-10% -> 10%-20% |
| PON slicing / deterministic PON / enterprise SLA | BBF/Omdia 讨论 50G PON slicing，运营商企业专线化 | $0.03-0.10B / $0.10-0.25B / $0.25-0.50B | $0.3-0.8B / $0.8-1.8B / $1.8-3.5B | $1-3B / $3-7B / $7-12B | 新增企业 PON 5%-10% -> 15%-30%；极超 50% |
| Remote OLT / distributed PON | Vecima R-OLT 领先，适合 cable-to-fiber、rural、MDU | $0.15-0.30B / $0.30-0.55B / $0.55-0.90B | $0.8-1.6B / $1.6-2.8B / $2.8-4.5B | $2-5B / $5-9B / $9-15B | 新增 fiber access nodes 5%-10% -> 12%-20% -> 20%-35% |
| DOCSIS 4.0 unified FDX/ESD SoC | Broadcom/Comcast 已发布方向，MaxLinear Puma 8 生态 | $0.05-0.15B / $0.15-0.35B / $0.35-0.70B | $0.6-1.2B / $1.2-2.5B / $2.5-4.5B | $2-5B / $5-9B / $9-15B | 新发 DOCSIS modem SoC 中 D4.0 <5% -> 10%-25% -> 25%-45% |
| DOCSIS 3GHz / 6GHz HFC extension | CableLabs 研究和 PoC，规格未规模化 | <$0.03B / $0.03-0.08B / $0.08-0.15B | $0.1-0.4B / $0.4-0.8B / $0.8-1.5B | $0.5-2B / $2-5B / $5-10B | 2027 仍偏 PoC/field trial；极超为 3GHz taps/amps 预采购 |
| Low Latency DOCSIS / app-aware QoE | LLD 已进入 D3.1/D4.0，Comcast 等部署 | $0.05-0.15B / $0.15-0.35B / $0.35-0.70B | $0.4-1B / $1-2B / $2-4B | $1.5-4B / $4-8B / $8-14B | Cable broadband premium tiers 5%-15% -> 20%-40%；极超 60% |
| Standard Power 6GHz / AFC Wi-Fi 7 | 美国 AFC 运营成熟，Cisco 等支持；FCC GVP 扩展 | $0.20-0.50B / $0.50-0.90B / $0.90-1.5B | $1.5-3B / $3-6B / $6-10B | $5-10B / $10-18B / $18-30B | 企业/场馆 Wi-Fi 7 中 AFC 10%-20% -> 30%-50%；极超 70% |
| Wi-Fi 8 / 802.11bn prototype | Broadcom/Qualcomm 2026 推早期芯片/样机，标准未最终 | <$0.03B / $0.03-0.08B / $0.08-0.20B | $0.1-0.4B / $0.4-0.9B / $0.9-1.8B | $1-3B / $3-7B / $7-12B | 2027 仍 <5% 企业新 AP；极超为高端预标准 AP |
| AI-native gateway / router NPU | Qualcomm A7 Elite、Broadcom AI access chipset、Calix One | $0.10-0.30B / $0.30-0.70B / $0.70-1.2B | $0.8-2B / $2-4B / $4-8B | $3-8B / $8-16B / $16-30B | 高端网关 NPU attach 5%-10% -> 15%-30% -> 30%-50%；极超 70% |
| Wi-Fi HaLow / IoT access | WBA 预计 2026 继续加速，适合低功耗远距 IoT | $0.05-0.15B / $0.15-0.35B / $0.35-0.60B | $0.4-0.9B / $0.9-1.8B / $1.8-3B | $1.5-4B / $4-8B / $8-14B | 工业/智慧城市 IoT 低个位数 -> 5%-10%；极超 15% |
| OpenRoaming / Wi-Fi offload platform | WBA 推动，移动运营商需要降低 cellular traffic cost | $0.05-0.15B / $0.15-0.35B / $0.35-0.70B | $0.4-1B / $1-2.5B / $2.5-5B | $1.5-4B / $4-9B / $9-16B | 公共 Wi-Fi/城市/venue 10%-20% -> 25%-45%；极超 60% |

### 4.2 在研技术利润率预测

| 技术 | 当前/早期毛利率 | 未来1年：基准/乐观/极超 | 未来2年：基准/乐观/极超 | 为什么能高溢价 |
|---|---:|---:|---:|---|
| 50G PON optics/line cards | 35%-60% | 35%-55% / 45%-65% / 55%-75% | 32%-50% / 40%-60% / 50%-70% | Burst-mode 50G optics、combo coexistence、PON timing、认证难；早期客户买的是未来 proofing。 |
| 25GS-PON | 35%-55% | 35%-55% / 42%-60% / 50%-68% | 32%-50% / 38%-58% / 45%-65% | 25G 与 XGS/GPON 共纤，CPE 少但高端用户愿付费，Nokia 生态领先。 |
| PON slicing/deterministic PON | 60%-85% 软件/功能毛利 | 65%-85% / 70%-88% / 75%-90% | 65%-85% / 72%-90% / 78%-92% | SLA、切片、QoE、OSS/BSS 集成是软件和控制面，不是低价硬件。 |
| Remote OLT | 35%-55% | 35%-55% / 40%-60% / 48%-65% | 35%-52% / 40%-58% / 45%-62% | Cable-to-fiber 和 rural 场景节省机房/馈线成本，设备认证和远端运维壁垒高。 |
| D4.0 unified SoC | 55%-70% | 58%-72% / 62%-75% / 68%-80% | 55%-70% / 60%-75% / 65%-80% | FDX/ESD 双路线统一、AI telemetry、CableLabs 认证、多年 operator design-in。 |
| DOCSIS 3GHz/6GHz | 早期 NRE/试验，毛利不可比 | 40%-60% / 50%-70% / 60%-80% | 35%-55% / 45%-65% / 55%-75% | 新 passives/amps/taps/measurement 工具，规格制定参与方可优先卡位。 |
| LLD/QoE software | 65%-90% | 68%-88% / 72%-90% / 78%-92% | 68%-88% / 75%-90% / 80%-93% | 降低延迟和投诉，可按 premium tier、gaming、business SLA 收费。 |
| SP 6GHz/AFC | AP 硬件 45%-65%，AFC service 70%-90% | 45%-65% / 55%-72% / 65%-85% | 42%-62% / 50%-70% / 60%-82% | 监管数据库、场景规划、enterprise validation、Cisco/Meraki/venue 锁定。 |
| Wi-Fi 8 early AP/chip | 芯片 55%-70%，AP 50%-65% | 50%-68% / 58%-72% / 65%-80% | 45%-65% / 55%-70% / 60%-75% | 预标准高端客户为了 reliability/AIOps 提前付费；但量产后 ASP 会降。 |
| AI-native gateway | 芯片 55%-70%，平台软件 70%-90% | 55%-75% / 65%-85% / 75%-90% | 55%-75% / 68%-88% / 78%-92% | 运营商买“少上门、少投诉、少 churn、增 ARPU”，可按软件/安全/AI 服务收费。 |
| Wi-Fi HaLow | 芯片 45%-60%，模块 25%-45% | 35%-55% / 45%-65% / 55%-75% | 32%-52% / 42%-62% / 50%-70% | 低功耗远距 IoT 替代专网，工业/公用事业认证周期形成锁定。 |
| OpenRoaming/offload | 平台 70%-90% | 70%-88% / 75%-90% / 80%-92% | 70%-88% / 75%-90% / 80%-93% | 运营商 offload 成本下降、漫游身份、SIM/eSIM/Passpoint 集成。 |

## 5. 供给侧：产能结构、瓶颈、成本与价格传导

### 5.1 产能结构

| 环节 | 主要产能地区 | 主要公司/生态 | 工艺/能力 |
|---|---|---|---|
| PON OLT/ONT 系统 | 中国、越南、泰国、台湾、墨西哥、东欧、美国少量 final assembly | Huawei、ZTE、FiberHome、Nokia、Calix、Adtran、DZS、Ubiquiti、Ciena/Cisco 部分，ODM Sercomm/Arcadyan/Sagemcom/Hitron | OLT line card、PON MAC/PHY、burst-mode optics、combo PON、ONT/HGS。 |
| 25G/50G PON optics | 中国、台湾、日本、韩国、东南亚 | Hisense Broadband、Accelink、Source Photonics、Lumentum、Coherent、Innolight、Eoptolink、Broadex、AIO Core optics 生态 | 25G/50G burst-mode laser/APD/TIA、BOSA、symmetric/asymmetric optics。 |
| DOCSIS nodes/amps/RPD/vCMTS | 北美、墨西哥、中国、台湾、欧洲 | CommScope/Vistance、Harmonic、Vecima、Cisco、Casa legacy、Teleste、ATX、Technetix | 1.2/1.8GHz amps、RPD/RMD、vCMTS software、field-hardened RF。 |
| DOCSIS/PON/Wi-Fi SoC | 台积电/三星/成熟逻辑代工，封测在台湾/中国/东南亚 | Broadcom、MaxLinear、Qualcomm、MediaTek、Airoha、Realtek、Intel/MaxLinear legacy、Celeno/Imagination 等 | 6-16nm 级 cable/fiber SoC，Wi-Fi 7 RF/baseband，10G/2.5G Ethernet PHY。 |
| Wi-Fi 7 AP/CPE | 中国、台湾、越南、泰国、马来西亚、墨西哥 | TP-Link、Netgear、Ubiquiti、Cisco/Meraki、HPE Aruba、Huawei、Juniper Mist、Extreme、CommScope Ruckus、Zyxel、Vantiva、Sercomm、Arcadyan | Tri-band RF、FEM、antenna tuning、PoE/2.5G/10G LAN、cloud firmware。 |
| 光纤/线缆/被动件 | 美国、中国、欧洲、日本、印度、东南亚 | Corning、Prysmian、CommScope、AFL、YOFC、Furukawa、Fujikura、Sumitomo、Hengtong、FiberHome、Clearfield、Belden、Panduit | 光纤预制、MPO/LC/SC/APC、closures、splitters、cabinets、BABA 合规。 |
| 测试认证 | 美国、欧洲、中国台湾、中国、日本 | CableLabs、Broadband Forum/UNH-IOL、Wi-Fi Alliance、Keysight、VIAVI、R&S、Anritsu、EXFO | DOCSIS 4.0 security/interop、PON plugfest、Wi-Fi 7/6GHz/AFC、field meters。 |

### 5.2 供给瓶颈

1. **DRAM/NAND/eMMC/LPDDR。** AI 数据中心把 DRAM/NAND/HBM 价格和产能吸走，高端 Wi-Fi 7 网关、DOCSIS 4.0 gateway、企业 AP 的内存成本 2026 最难控。
2. **25G/50G PON burst-mode optics。** OLT 侧连续发送容易，ONU 侧 burst-mode 高速上行、定时、温漂、功率预算和低成本量产更难，是 50G PON 放量阀门。
3. **DOCSIS 4.0 field hardware。** 1.8GHz/FDX amps、taps、passives、RPD、nodes 需要现场可靠性、温度、供电、噪声和长级联验证；实验室速度不等于可规模施工。
4. **认证与互通。** CableLabs、Broadband Forum、Wi-Fi Alliance、AFC、运营商自有测试周期会把芯片样片到收入确认拉长 6-18 个月。
5. **施工与许可。** FTTH trenching、make-ready、pole attachment、splicing technicians、MDU access、municipal permits 会比 OLT/ONT 更慢。
6. **BEAD/BABA 合规供应。** 美国 BEAD 项目对国产化和合规链条要求高，可能造成“有资金但缺合规光缆/closures/人力”的局面。
7. **Wi-Fi 7 客户端生态和 6GHz 监管。** 没有 6GHz 客户端、AFC 或标准功率覆盖，Wi-Fi 7 的 MLO/320MHz 价值会被削弱。
8. **运营商库存与预算周期。** 2021-2022 供应链紧张后运营商曾过度备货，2023-2025 去库存压制采购；2026 复苏仍会呈季度波动。
9. **中国设备地缘政治。** Huawei/ZTE 在欧洲/美国受限，利好 Nokia/Calix/Adtran/Cisco/Juniper/HPE，但也减少低价供给、提高项目成本。
10. **10G LAN/PoE/家庭布线短板。** 10G PON 或 D4.0 网关若家内只有 1G/2.5G LAN，用户感知不足，会延迟高端套餐渗透。

### 5.3 BOM 与单位成本拆分

| 产品 | 典型 BOM/成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| XGS-PON OLT line card/port | PON MAC/ASIC 20%-30%，optics 25%-35%，PCB/电源/散热 10%-15%，chassis allocation 10%-20%，软件/许可 10%-20%，测试 5%-10% | 端口密度、combo optics、平台锁定、OSS/BSS 集成 | 大运营商年度框架价；高端 combo/25G/50G 可按端口溢价。 |
| XGS-PON ONT/HGS | PON SoC 15%-25%，Wi-Fi/CPU/RF 20%-35%，DRAM/NAND 10%-20%，optics 10%-18%，LAN PHY/ports 5%-10%，电源/外壳/天线 15%-25%，软件 5%-10% | Wi-Fi 7 配置、内存价格、运营商定制、远程管理 | CPE 租赁/补贴可转嫁给用户月费；硬件厂常需接受年度降价。 |
| 50G PON ONU/OLT optics | Laser/APD/TIA/driver 30%-45%，PON SoC/PHY 20%-30%，thermal/calibration 10%-15%，封装/测试 15%-25% | 良率、burst-mode timing、功率预算、温度等级 | 初期按 high-end enterprise SLA 定价，量产后向 XGS-PON 靠拢。 |
| DOCSIS 4.0 gateway | Cable SoC 20%-30%，RF tuner/FEM/amps 15%-25%，Wi-Fi 7 20%-30%，DRAM/NAND 10%-15%，10G/2.5G ports 5%-10%，电源/热/外壳 10%-15%，软件 5%-10% | Broadcom/MaxLinear 芯片供应、Wi-Fi 7 tri-band、运营商认证、返修率 | 运营商租赁网关月费和高端套餐吸收；ODM 毛利低，芯片/品牌毛利高。 |
| DOCSIS amps/nodes/RPD | RF components 20%-30%，RPD/SoC 20%-30%，power/hardened enclosure 20%-30%，thermal/sealing 10%-15%，测试/认证 10%-15% | 1.8GHz/FDX 性能、级联噪声、现场可靠性、安装效率 | MSO 项目制采购，供不应求时按交期和服务能力溢价。 |
| Enterprise Wi-Fi 7 AP | Wi-Fi SoC/RF/FEM 35%-50%，CPU/switch/PoE 10%-20%，DRAM/NAND 8%-15%，antenna/mechanics 10%-20%，cloud license/support 5%-15% | Cloud AIOps、AFC、security license、PoE switch attachment | 硬件可低溢价，软件订阅和 support contract 保毛利。 |
| Cloud-managed Wi-Fi/AIOps | 云 infra 10%-20%，R&D/AI model 25%-40%，support/CS 15%-25%，sales/channel 20%-35% | 数据规模、运营商集成、降低 truck roll/churn 的 ROI | 按 subscriber、AP、site、feature tier 收费；最容易提价。 |
| FTTH passive/BABA | 光纤/线缆 35%-50%，closures/cabinets 15%-30%，连接器/分路器 10%-20%，物流 5%-10%，施工辅材 10%-20% | 合规产能、项目批量、预制化、施工效率 | BEAD 和运营商项目可做 escalation clause，短缺时交期溢价。 |

## 6. 竞争格局与壁垒

### 6.1 市场结构与头部集中度

| 细分市场 | 头部结构 | 集中度判断 | 说明 |
|---|---|---|---|
| 全球 PON OLT | Huawei、ZTE、Nokia、FiberHome、Calix、Adtran、DZS | 全球 top 4 约 65%-80%；排除中国后 Nokia/Calix/Adtran 份额更高 | 中国设备商强在规模和成本；北美/欧洲受地缘政治影响，Nokia/Calix/Adtran 受益。 |
| ONT/HGS/CPE | Sercomm、Arcadyan、Vantiva、Sagemcom、Hitron、ZTE、Huawei、Nokia、Calix/Adtran 生态 | 分散但运营商项目高度锁定 | ODM 毛利低，平台/云管/运营商认证决定粘性。 |
| 25G/50G PON | Nokia、ZTE、Huawei、Calix、Adtran、Airoha、Sagemcom/Hitron 等 | 早期集中度高 | Nokia 25G/50G 同卡演进有先发；中国 50G 由 Huawei/ZTE/FiberHome 牵引。 |
| DOCSIS network equipment | CommScope/Vistance、Harmonic、Vecima、Cisco legacy、Teleste、ATX/Technetix | 北美高度集中 | Field-proven amps/nodes/RPD/vCMTS 认证壁垒高，新进入者难。 |
| DOCSIS silicon | Broadcom、MaxLinear | 接近双寡头 | D4.0 unified chipset 和 Puma 8 等决定 modem/node 生态。 |
| Wi-Fi 7 chipset | Broadcom、Qualcomm、MediaTek/Airoha、MaxLinear、Realtek | 高集中，三强主导高端 | Tri-band、RF FEM、MLO、power、reference design 是壁垒。 |
| Enterprise WLAN | Cisco/Meraki、HPE Aruba、Huawei、Ubiquiti、Juniper Mist、Extreme、CommScope Ruckus、TP-Link Omada | 中高集中，区域差异大 | 北美企业偏 Cisco/HPE/Juniper/Ubiquiti；中国 Huawei 强；SMB TP-Link/Ubiquiti 强。 |
| Managed Wi-Fi/AIOps | Calix、Plume、Cisco/Meraki、Juniper Mist、HPE Aruba Central、ExtremeCloud、CommScope、TP-Link Omada | 平台 lock-in 明显 | 一旦接入 OSS/BSS、app、support 和数据湖，切换成本高。 |
| FTTH passive | Corning、Prysmian、CommScope、AFL、Clearfield、YOFC、Fujikura、Sumitomo、Hengtong | 区域性集中 | 美国 BEAD 合规和产能可形成局部稀缺。 |

### 6.2 壁垒清单：为什么能定价

| 壁垒 | 体现 | 为什么能定价 |
|---|---|---|
| 标准与认证 | CableLabs D4.0、BBF PON Plugfest、Wi-Fi CERTIFIED 7、AFC、operator lab | 认证失败会延迟运营商上线，客户愿意为“已验证、可互通、少返修”付费。 |
| 运营商切换成本 | OSS/BSS、TR-069/TR-369 USP、OpenSync/prpl/RDK-B、远程诊断、app、库存 | 替换 CPE/OLT 平台会影响客服、truck roll、库存和固件安全，成本远高于硬件差价。 |
| 规模与供应链 | 大客户需要百万级 ONT/AP、长期 firmware、全球 RMA | 交期、质量和售后是运营商 KPI，规模厂可在短缺时优先拿料。 |
| 高速模拟/RF/光器件 | DOCSIS 1.8GHz RF、50G burst-mode optics、Wi-Fi 7 6GHz FEM | 这是工程良率壁垒，不是简单软件复制；调试周期长。 |
| 平台数据 | AIOps 需要大量 AP/网关 telemetry、故障标签、家庭拓扑 | 数据越多，模型越准，能减少投诉和上门，形成正反馈。 |
| 监管/地缘政治 | BEAD BABA、美国/欧洲对 Huawei/ZTE 限制、6GHz AFC | 合规供应商池缩小后，剩余厂商议价提升。 |
| 渠道与客户锁定 | Cisco/HPE/Juniper/Calix/Plume 与企业/运营商销售体系 | 采购不是只买 AP，而是买安全、support、controller、cloud 和 SLA。 |
| 现场施工能力 | FTTH splicing、pole attachment、HFC amps/taps 施工 | 有设备也要能施工和验收，EPC/材料一体化能力可溢价。 |

### 6.3 价值捕获排序

| 排名 | 价值链层级 | 长期 ROIC/毛利判断 | 原因 |
|---:|---|---|---|
| 1 | Cloud-managed Wi-Fi/AIOps/运营商体验平台 | 最高，毛利 70%-90% | 直接降低 churn、truck roll、客服成本，可按 subscriber/site 收费。 |
| 2 | PON/DOCSIS/Wi-Fi 高端芯片与参考设计 | 很高，毛利 55%-75% | 认证周期长、客户 design-in 长、FDX/ESD/MLO/6GHz/50G PHY 壁垒高。 |
| 3 | DOCSIS 4.0 amps/nodes/RPD/vCMTS | 高，毛利 35%-60% | MSO 采购集中、现场可靠性要求高、供应商少。 |
| 4 | 25G/50G PON optics/OLT line cards | 高，毛利 35%-65% | 高端 optics 和 combo 端口早期稀缺，企业 SLA 支撑溢价。 |
| 5 | Enterprise Wi-Fi 7 AP + cloud license | 高，毛利 45%-70% | 硬件竞争激烈但 cloud/security/AIOps 抬高 blended margin。 |
| 6 | FTTH passive + 合规材料 | 中高，毛利 20%-45% | 周期性强，但 BEAD/BABA/光缆短缺会形成局部高价。 |
| 7 | 低端 ONT/CPE ODM | 低，毛利 8%-18% | 客户强势、竞争充分、内存涨价难完全传导。 |

## 7. 2026 关键变化：3 个最可能拐点

### 拐点一：Wi-Fi 7 从高端消费电子进入运营商默认 CPE

WBA/ABI 对 2026 Wi-Fi 7 AP 117.9M 出货的预测，叠加 Charter 2026 推 Invincible WiFi、Comcast XB10、Hitron/Vantiva/Sagemcom/Sercomm 的 Wi-Fi 7 gateway，使 Wi-Fi 7 从零售路由器故事变成运营商 CPE 采购故事。AI PC、手机和 XR 设备换机一旦增加 6GHz/MLO 客户端，运营商会更愿意把 Wi-Fi 7 用于高端套餐留存。

**最可能放量子方向：** residential Wi-Fi 7 HGS、enterprise tri-band AP、cloud-managed Wi-Fi、AIOps、安全订阅。

### 拐点二：Cable 升级从“等待 DOCSIS 4.0”转为“high-split + DAA + D4.0 并行”

Charter 2026 的主线仍是 1.2GHz/high-split/DAA；Comcast 的 FDX 证明 D4.0 可以商用；CableLabs 互通从速度转向安全和多厂商。结果是 cable 运营商不再二选一，而是按 plant 条件分层采购：D3.1+ 和 high-split 负责大范围上行，D4.0 FDX/ESD 负责 premium 区域。

**最可能放量子方向：** RPD/RMD、vCMTS、1.2GHz/1.8GHz amps、FDX amps、D4.0 gateway、LLD/QoE software。

### 拐点三：BEAD 与 FTTH overbuild 进入采购，但瓶颈从 OLT 转向合规材料和施工

NTIA 数据显示 BEAD 已从审批推进到资金可用和 award agreement，2026 H2 会产生更多真实订单。但短期瓶颈不是 PON 芯片，而是 BABA 光缆、closures、cabinets、施工队、pole attachment、许可和项目融资。

**最可能放量子方向：** XGS-PON、remote OLT、预制光缆组件、closures/cabinets、施工软件、Calix/Adtran/Nokia 平台。

## 8. 2027 关键变化：3 个最可能拐点

### 拐点一：50G PON 从示范走向高价值商业化

2026 的 50G PON 更像“技术可信度建立年”，2027 才是商业化分水岭。若中国运营商、中东高端园区、Google Fiber/Nokia 生态和企业 SLA 同时推进，50G PON 可能提前形成 $6B-$12B 级两年订单池。若成本下降慢，则 25GS-PON 会吃掉一部分过渡需求。

**最可能放量子方向：** 50G OLT line card、50G ONU optics、50G FTTR、enterprise PON slicing、25G/50G combo card。

### 拐点二：DOCSIS 4.0 ESD/FDX 进入多运营商规模部署

Comcast FDX 扩围、Charter/Cox 交易后网络路线收敛、欧洲 cable operator 面对 fiber overbuild，将共同推动 D4.0 从“单一领先运营商”走向多运营商采购。2027 年 D4.0 的最大弹性不在 modem 数量，而在 amps、nodes、RPD、vCMTS、field meter 和认证服务。

**最可能放量子方向：** unified FDX/ESD chipset、1.8GHz ESD amps/taps、D4.0 RPD、vCMTS capacity license、D4.0 Wi-Fi 7/8 gateways。

### 拐点三：Wi-Fi 7 主流化与 Wi-Fi 8 预标准并行

2027 Wi-Fi 7 将成为 enterprise 和高端 residential 的默认采购，SP 6GHz/AFC 在场馆、教育和工业中更常见；同时 Wi-Fi 8 预标准样机开始进入高端试点。Wi-Fi 8 的投资点不是更高峰值，而是可靠性、漫游、mesh、拥塞环境和 AI QoE。

**最可能放量子方向：** Wi-Fi 7 AFC AP、AI/Cognitive WLAN、OpenRoaming/offload、Wi-Fi 8 early silicon、gateway NPU。

## 9. 头部公司与细分技术清单

### 9.1 PON / FTTH / 光接入

- **全球 OLT/PON 系统**：Huawei、ZTE、Nokia、FiberHome、Calix、Adtran、DZS、Ciena、Cisco、Ubiquiti、Tibit/Coherent PON transceiver ecosystem。
- **25G/50G PON**：Nokia、ZTE、Huawei、FiberHome、Calix、Adtran、Airoha、Sagemcom、Hitron、Evolution Digital、MT2、Broadcom/MaxLinear/Realtek/Airoha chipset ecosystem。
- **Remote OLT / distributed access fiber**：Vecima Entra、Harmonic、Adtran、Nokia、Calix、Casa legacy、Tibit/Coherent pluggable OLT。
- **ONT/HGS/CPE ODM**：Sercomm、Arcadyan、Vantiva、Sagemcom、Hitron、Technicolor/Vantiva、Gemtek、Zyxel、CIG、Foxconn/Accton ecosystem、TP-Link。
- **PON optics / BOSA / burst-mode components**：Hisense Broadband、Accelink、Lumentum、Coherent、Source Photonics、Innolight、中际旭创、新易盛、Eoptolink、Broadex、AOI、Fujitsu Optical Components、Sumitomo Electric、Furukawa。
- **FTTH passive / 光缆与连接**：Corning、Prysmian、CommScope、AFL、Clearfield、Belden、Panduit、YOFC、Hengtong、FiberHome、Fujikura、Sumitomo、Furukawa、Senko、US Conec、Huber+Suhner。

### 9.2 DOCSIS / Cable access

- **DOCSIS DAA / nodes / amps / RPD / vCCAP**：CommScope/Vistance Networks、Harmonic、Vecima、Cisco、Casa Systems legacy、Teleste、ATX Networks、Technetix、Gainspeed/Nokia legacy。
- **DOCSIS 4.0 chipset**：Broadcom、MaxLinear。
- **DOCSIS CPE / gateways**：Comcast XB10 ecosystem、Vantiva、Sercomm、Hitron、CommScope/Home Networks、Sagemcom、Ubee、Netgear、Arris legacy。
- **Cable software / vCMTS / orchestration**：Harmonic cOS、CommScope vCCAP、Vecima Entra vCMTS、CableLabs FMA/DAA ecosystem、OpenSync/RDK-B/prpl。
- **Cable test and field tools**：VIAVI、Keysight、Rohde & Schwarz、Anritsu、EXFO、VeEX、SCTE/CableLabs labs。

### 9.3 Wi-Fi 7 / Wi-Fi 8 / WLAN

- **Wi-Fi silicon**：Broadcom、Qualcomm、MediaTek、Airoha、MaxLinear、Realtek、NXP、Infineon、Synaptics、Celeno/Intel legacy。
- **Consumer/SMB Wi-Fi 7 routers/mesh**：TP-Link、Netgear、ASUS、Eero/Amazon、Ubiquiti、Linksys、Zyxel、D-Link、Xiaomi、Huawei、Honor。
- **Enterprise WLAN**：Cisco/Meraki、HPE Aruba、Huawei、Juniper Mist、Ubiquiti UniFi、Extreme Networks、CommScope Ruckus、TP-Link Omada、Fortinet、Cambium、Zyxel、EnGenius。
- **运营商托管 Wi-Fi / home platform**：Calix、Plume、Airties、OpenSync ecosystem、CommScope HomeVantage、Vantiva、Sagemcom、Assia/DZS CloudCheck、RouteThis、Cujo AI。
- **AFC / 6GHz / OpenRoaming**：Wi-Fi Alliance Services、Wireless Broadband Alliance、Federated Wireless、Comsearch/CommScope、Qualcomm AFC、Cisco/Meraki AFC、Broadcom ecosystem。

### 9.4 AI-native gateway / edge intelligence

- **AI gateway silicon/platform**：Qualcomm Networking Pro A7 Elite / Dragonwing、Broadcom AI access chipset、MediaTek Filogic/Airoha、MaxLinear Wi-Fi 7/Puma ecosystem。
- **运营商 AI/AIOps 平台**：Calix One、Plume、Juniper Mist AI、Cisco/Meraki AI、HPE Aruba Central、ExtremeCloud IQ、Huawei iMaster NCE、ZTE AI network solutions。
- **安全与家庭服务**：Cujo AI、F-Secure/Sense、Bitdefender BOX/operator security、Allot、Akamai/Guardicore、Cloudflare for families/zero trust edge。

## 10. 投资排序与风险

### 10.1 优先级排序

| 优先级 | 子方向 | 2026 确定性 | 2027 弹性 | 结论 |
|---:|---|---|---|---|
| 1 | Wi-Fi 7 enterprise/residential + cloud-managed Wi-Fi | 极高 | 高 | 已进入规模出货，AI/AIOps 提升软件毛利。 |
| 2 | XGS-PON + HGS 网关 | 极高 | 中高 | FTTH/BEAD/overbuild 主力，量大但硬件 ASP 有压力。 |
| 3 | DOCSIS high-split/DAA/vCMTS | 高 | 高 | Cable 运营商 2026 必做，D4.0 前置投资。 |
| 4 | DOCSIS 4.0 FDX/ESD ecosystem | 中高 | 极高 | 2026 Comcast 明确，2027 多运营商放量可能带来估值弹性。 |
| 5 | 25G/50G PON optics/line cards | 中 | 极高 | 2026 小批高毛利，2027 预期差大。 |
| 6 | AI-native gateway / AIOps platform | 中 | 极高 | 若运营商能把 AI 服务打包进 ARPU，是最高 ROIC 方向。 |
| 7 | BEAD passive materials/施工 | 中高 | 高 | 项目可见度上升，但受劳动力、合规和许可约束。 |

### 10.2 主要风险

1. **AI 流量不兑现为消费者/企业付费升级。** AI 数据中心 CapEx 很强，但家庭宽带 ARPU 不一定同步上行。
2. **内存涨价压缩 CPE 毛利。** DRAM/NAND 若继续紧张，低端网关/ONT/路由器最受伤。
3. **DOCSIS 4.0 认证与现场复杂度。** FDX/ESD 两路线、1.8GHz plant、legacy QAM、taps、amps、modem certification 会拖慢收入确认。
4. **50G PON 过早资本化。** 50G PON 技术成立，但 XGS-PON 已足够满足大多数家庭，50G 放量必须靠企业/园区/高端差异化。
5. **Wi-Fi 7 价格战。** Dell'Oro 已提示 Wi-Fi 7 初期价格异常低；若内存成本不能传导，AP 厂商毛利可能受压。
6. **BEAD 延迟。** 资金获批不等于施工开始，pole attachment、NEPA、BABA、州级合同和劳动力会把收入推到 2027。
7. **中国设备地缘限制。** 可能利好非中国厂商，但也会抬高成本、延长交期。

## 11. 可跟踪的 2026-2027 高频指标

1. Comcast DOCSIS 4.0 FDX availability 从百万 homes 到多百万 homes 的披露，以及 XB10/FDX gateway 供应。
2. Charter network evolution 的 quarterly CapEx 中 network evolution spending、1.2GHz/high-split 完成比例、1.8GHz/D4 采购信号。
3. CableLabs D4.0 Interop、Cable-Tec Expo 2026 中 FDX/ESD unified modem、RPD、vCMTS 认证数量。
4. Nokia、Calix、Adtran、Vecima 的 book-to-bill、BEAD 订单、gross margin 和 25G/50G PON 客户披露。
5. Wi-Fi 7 AP 出货、6GHz 客户端 attach、AFC 标准功率部署、enterprise WLAN 中 Wi-Fi 7 收入占比。
6. DRAM/NAND 合约价和 CPE 厂商 memory surcharge 是否被运营商接受。
7. 50G PON optics ASP、ONU 量产良率、BBF Plugfest 参与厂商和运营商试商用名单。
8. BEAD 项目 award agreement 后的采购公告、BABA 合规光缆交期、splicing crew 单价。

## 12. 来源索引

- Dell'Oro / PRNewswire, Broadband Access Equipment to Return to Growth in 2026: <https://www.prnewswire.com/news-releases/broadband-access-equipment-to-return-to-growth-in-2026-according-to-delloro-group-302709983.html>
- Electronics Weekly, broadband access forecast 2025-2030: <https://www.electronicsweekly.com/news/business/0-3-growth-2025-30-for-broadband-access-equipment-market-2026-01/>
- Fiber Broadband Association, 2025 FTTH deployment highs: <https://fiberbroadband.org/2025/12/16/fiber-broadband-association-reports-historic-fiber-deployment-highs/>
- NTIA BEAD Progress Dashboard: <https://www.ntia.gov/funding-programs/internet-all/broadband-equity-access-and-deployment-bead-program/progress-dashboard>
- CableLabs, DOCSIS technology 2026 update: <https://www.cablelabs.com/blog/docsis-technology-whats-changed-in-the-past-year-and-why-it-matters>
- CableLabs, DOCSIS 4.0 Interop security: <https://www.cablelabs.com/blog/authentication-and-privacy-docsis-4-0-interop-focuses-on-security>
- Comcast + Broadcom AI-powered access network / unified DOCSIS 4.0 chipset: <https://corporate.comcast.com/press/releases/comcast-broadcom-develop-ai-powered-access-network-pioneering-new-chipset>
- Comcast + CommScope DOCSIS 4.0 rollout milestone: <https://corporate.comcast.com/press/releases/comcast-commscope-notch-milestone-next-generation-connectivity-millions-across-us>
- CommScope DOCSIS 4.0 amplifiers: <https://commscopeholdingcompanyinc.gcs-web.com/news-releases/news-release-details/commscope-and-comcast-accelerate-rollout-docsis-40-amplifiers>
- Charter Q1 2026 results: <https://ir.charter.com/static-files/8f4715b9-1c59-4a03-8829-05e75fdbb368>
- Charter 2025 10-K: <https://www.sec.gov/Archives/edgar/data/0001091667/000109166726000017/chtr-20251231.htm>
- Wireless Broadband Alliance 2026 predictions: <https://wballiance.com/wireless-broadband-alliance-reveals-its-wi-fi-predictions-for-2026-and-beyond/>
- WBA Industry Report 2026 findings: <https://wballiance.com/wba-industry-report-2026-finds-62-of-survey-respondents-more-confident-to-invest-in-wi-fi-than-12-months-ago/>
- IDC enterprise WLAN Wi-Fi 7 blog: <https://www.idc.com/resource-center/blog/worldwide-enterprise-wlan-grew-13-9-driven-by-wi-fi-7-deployments/>
- Qualcomm Wi-Fi 7: <https://www.qualcomm.com/wi-fi/wi-fi-7>
- Qualcomm Networking Pro A7 Elite: <https://www.qualcomm.com/news/releases/2024/10/qualcomm-unveils-the-networking-pro-a7-elite-platform--the-first>
- Nokia 50G PON solution: <https://www.nokia.com/newsroom/nokia-unveils-worlds-first-50g-pon-solution-for-post-quantum-enterprise-connectivity/>
- Nokia Q1 2026 interim report: <https://www.nokia.com/newsroom/nokia-corporation-interim-report-for-q1-2026/>
- Nokia selected by altafiber: <https://www.nokia.com/about-us/news/releases/2026/01/19/nokia-selected-by-altafiber-for-fiber-network-expansion-across-ohio-and-hawaii/>
- ZTE + China Mobile 50G PON FMC community: <https://www.zte.com.cn/global/about/news/china-mobile-and-zte-take-the-lead-in-launching-a-50G-PON-based-FMC-residential-community-in-China.html>
- Broadband Forum PON Plugfest: <https://www.broadband-forum.org/news/record-vendor-turnout-powers-high-speed-fiber-device-compatibility/>
- Broadband Forum State of PON 2026: <https://www.broadband-forum.org/events/state-of-pon-2026-industry-reality-check-vbase-webinar/>
- Calix Q4 2025 shareholder letter: <https://investor-relations.calix.com/sec-filings/all-sec-filings/content/0001406666-26-000004/ex992stockholderletter25q4.htm>
- Calix Q1 2026 results: <https://www.stocktitan.net/sec-filings/CALX/8-k-calix-inc-reports-material-event-2c5a13d94a83.html>
- MaxLinear Wi-Fi 7 / Puma / broadband access demos: <https://www.maxlinear.com/news/press-releases/2024/maxlinear-highlights-leading-end-to-end-broadband-access-and-connectivity-solutions-with-low-power>
- TrendForce memory contract price pressure from AI servers: <https://www.trendforce.com/presscenter/news/20260331-12995.html>

---

非投资建议。本报告用于产业链研究和情景分析。关键不确定性包括 AI 应用流量兑现、运营商资本开支周期、CPE 内存成本、DOCSIS/PON 认证节奏、BEAD 施工延迟、地缘政治和设备价格竞争。
# 行业调研：【网卡、DPU与SmartNIC】

> 截至：2026-05-08  
> 口径：本文覆盖 AI 数据中心里的高端 NIC/SuperNIC、DPU/IPU/SmartNIC、云厂自研 Nitro/EFA/IPU/Azure Boost 等等效基础设施处理器、AI 后端 scale-out 网络端点、前端/存储/安全 offload 网卡、以及与 UEC/UALink/PCIe Gen6/CXL/片上 NIC 相关的在研技术。  
> 重要说明：公开市场报告常把“DPU 市场”定义得很窄，2026 仅约 30-45 亿美元；但 AI 计算中心实际采购和内部转移价值更大，因为每个 GPU/XPU rack 都需要高速 endpoint、DPU/IPU、telemetry、RDMA/congestion offload、storage/security offload。本文将“纯 DPU 小口径”和“AI NIC/DPU/SmartNIC 端点大口径”分开。所有美元为名义美元，`B`=十亿美元，`M`=百万美元。

## 0. 结论先行

2026 年，网卡、DPU 与 SmartNIC 行业的主线不是普通服务器从 25G/100G 升级到 200G/400G，而是 AI 集群把网络端点从“可替换的 I/O 卡”升级成**决定 GPU/XPU 利用率、作业完成时间、KV cache 吞吐、租户隔离和安全边界的基础设施处理层**。最强判断如下：

| 维度 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---:|---:|---:|
| 2025 可观测锚点 | Crehan 称 server-class Ethernet NIC 收入两年翻倍，2025 超过 $13B；200G/400G NIC 收入过去一年增长超 3 倍并超过总收入一半。[Crehan](https://www.globenewswire.com/news-release/2026/03/09/3251924/0/en/Server-Class-Ethernet-NIC-Revenues-Have-Doubled-in-Just-Two-Years-Reports-Crehan-Research.html) | 同左 | 同左 |
| 2026 AI NIC/DPU/SmartNIC 端点大口径收入池 | $32-48B | $48-70B | $70-95B |
| 2027 AI NIC/DPU/SmartNIC 端点大口径收入池 | $55-85B | $85-130B | $130-190B |
| 2026 纯 DPU/IPU/SmartNIC 小口径 | $4-7B | $7-11B | $11-17B |
| 2027 纯 DPU/IPU/SmartNIC 小口径 | $7-12B | $12-20B | $20-35B |
| 最强放量产品 | NVIDIA ConnectX-7/8/9、BlueField-3/4、Broadcom 400G/800G Thor、AMD Pensando Pollara 400、AWS EFA/Nitro、Google/Intel IPU | 再加 Broadcom Thor Ultra 800G、AMD Vulcano 800、BlueField-4 STX | 1.6T SuperNIC、UEC 全功能 UET、UALink/ESUN scale-up endpoint、AI-native storage DPU |
| 2026 最可能技术路径 | 400G/800G RoCE/InfiniBand 并行；UEC-ready 先于 full UEC；DPU 继续做 front-end/storage/security；AI 后端 endpoint 以 NIC/SuperNIC 为主 | Ethernet 后端份额快速追 InfiniBand；800G NIC 进入 hyperscaler/ASIC 集群 | 800G 成新建高端 AI 默认，1.6T/PCIe Gen6 在 Rubin/MI400/MTIA/OpenAI ASIC 中提前拉量 |
| 长期高 ROIC 环节 | 高速 endpoint ASIC、SerDes/PHY、RDMA/congestion/offload 软件、云厂自研 IPU | 同左，外加 UEC/UALink 认证生态 | 同左，外加 AI-native storage/KV-cache DPU 与 CXL/PCIe fabric 端点 |

我的核心观点：

1. **2026 是“AI Ethernet endpoint”真正进入投资视野的一年**。NVIDIA 仍掌握 InfiniBand、NVLink 与 ConnectX/BlueField/Spectrum-X 的闭环优势，但 Broadcom Thor Ultra、AMD Pensando Pollara/Vulcano、UEC 1.0、Meta/Broadcom、OpenAI/Broadcom、Google/Intel IPU 说明 hyperscaler 正在把 NIC/DPU 从附属 BOM 变成开放 AI fabric 的战略入口。
2. **DPU 的叙事从虚拟化/安全 offload 升级到 AI 数据路径**。NVIDIA BlueField-4 STX 把 DPU、ConnectX-9、Vera CPU 组合成 context memory/KV cache storage 平台；Microsoft Maia 200 直接把 2.8 TB/s 双向片上 NIC 做进推理加速器；AWS EFA/Nitro、Google IPU、Azure Boost 则把商用 DPU 的许多价值内化到云厂自研硬件。
3. **短期最确定是 400G/800G NIC，利润率最高是头部 ASIC/软件栈，不是普通卡厂**。卡级代工和板卡毛利通常 10-25%；高端 NIC/DPU silicon 与软件绑定可达 50-75%；NVIDIA/Broadcom 这种平台型公司在供不应求时还能吃到系统级溢价。
4. **2027 弹性最大是 UEC full-compliance、1.6T/PCIe Gen6、UALink/ESUN 与 AI-native storage DPU**。如果 2027 进入 Rubin、MI400/MI450、Trainium3/4、TPU8、MTIA/OpenAI ASIC 多平台并行扩产，NIC/DPU 的收入弹性会高于服务器台数增长，因为每个 XPU 的网络带宽、端口数量、遥测、安全、重传与存储访问都在升阶。

## 1. 2026 机遇与挑战：AI 计算中心建设下的 NIC/DPU 重估

### 1.1 为什么 2026 是拐点

公开数据的锚点已经很清楚：

- **服务器级 Ethernet NIC 收入**：Crehan Research 称 server-class Ethernet NIC 收入从 2023 年低于 $6B 增至 2025 年超过 $13B；200G/400G NIC 销售额一年内增长超 3 倍，并已超过总收入一半。[Crehan](https://www.globenewswire.com/news-release/2026/03/09/3251924/0/en/Server-Class-Ethernet-NIC-Revenues-Have-Doubled-in-Just-Two-Years-Reports-Crehan-Research.html)
- **数据中心交换机侧验证网络强度**：IDC 称 2025 全年 Ethernet switch 收入 $55.1B，同比增长 31.5%；其中数据中心 segment $32.5B，同比增长 53.5%，4Q25 数据中心 Ethernet switch 收入 $9.9B，同比增长 63.0%，800G 占 4Q25 收入 25.8%。[IDC](https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/)
- **NVIDIA 网络成为数据中心增长主轴之一**：NVIDIA FY2026 数据中心收入 $193.7B，同比增长 68%；FY2026 Q4 数据中心收入 $62.3B，同比增长 75%；公司披露 Data Center networking 在 FY2026 前九个月同比增长 105%，由 GB200/GB300 的 NVLink fabric、XDR InfiniBand 和 Ethernet for AI 带动。[NVIDIA FY26](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/)、[NVIDIA 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm)
- **Broadcom 把 AI networking 与 custom AI accelerator 放在同一增长曲线**：Broadcom FY2026 Q1 收入 $19.3B，同比增长 29%；AI 收入 $8.4B，同比增长 106%，由 custom AI accelerators 与 AI networking 驱动；公司预计 FY2026 Q2 AI semiconductor 收入 $10.7B。[Broadcom Q1 FY26](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm)
- **标准侧已经到可商用前夜**：UEC 1.0 在 2025-06 发布，覆盖 NIC、switch、optics、cables 与软件栈，目标是面向 AI/HPC 的现代 RDMA、开放互操作和百万 endpoint 扩展。[UEC 1.0](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/) UALink 200G 1.0 已公开，可支持单 AI pod 内最多 1,024 个 accelerator；UALink 路线图称 2026-2027 面向商业部署。[UALink](https://ualinkconsortium.org/specification/)、[UALink roadmap](https://ualinkconsortium.org/blog/ualink-roadmap-insights-accelerating-open-scalable-ai-networking-1296/)

结论：2026 的 AI 网络端点不再是“服务器 NIC 总量增长”的普通周期，而是**GPU/XPU 利用率提升、开放 Ethernet 替代/补充 InfiniBand、云厂自研 ASIC 拉动、DPU 变成 AI 数据路径处理器**的多重共振。

### 1.2 2026 正在使用的技术路径

| 技术路径 | 2026 状态 | 代表产品/公司 | 适用场景 | 投资含义 |
|---|---|---|---|---|
| InfiniBand / NVIDIA Quantum + ConnectX | 最成熟的高端训练后端网络之一 | ConnectX-7/8/9、BlueField、Quantum-X/XDR | NVIDIA GPU 集群、frontier training、低延迟 collectives | NVIDIA 闭环锁定强，毛利高，替代难度大 |
| RoCEv2 / Ethernet AI back-end | 2025 已爆发，2026 高速扩张 | NVIDIA Spectrum-X、Broadcom Tomahawk/Thor、AMD Pensando、Arista/Cisco/HPE | hyperscaler/ASIC/GPU 混合后端 | 开放生态扩大，Broadcom/AMD/Marvell/Arista 受益 |
| UEC / UET 现代 RDMA | 规范发布，2026 UEC-ready/partial，2027 full-compliance 放量 | Broadcom Thor Ultra、AMD Pollara/Vulcano、UEC members | 大规模 AI 后端，解决传统 RDMA 的 ECMP/乱序/拥塞问题 | 2026 先看 NIC 与 switch 同平台验证，2027 看互操作 |
| DPU/IPU offload | 已在云厂和企业云成熟，AI 场景扩大 | NVIDIA BlueField-3/4、AMD Pensando Elba/Salina、Intel IPU E2100、Marvell OCTEON、AWS Nitro、Google IPU、Azure Boost | 租户隔离、VPC、NVMe-oF、crypto、telemetry、storage/security | 云厂自研吞掉部分 merchant TAM，但也验证长期价值 |
| AI SuperNIC / GPU-direct endpoint | 2026 进入 800G/1.6T 代际 | NVIDIA ConnectX-9 up to 1.6Tb/s、Broadcom Thor Ultra 800G、AMD Vulcano 800 | XPU-to-XPU scale-out、后端集群 | 每 accelerator endpoint 价值量上升 |
| 片上 NIC / accelerator-integrated NIC | hyperscaler ASIC 先行 | Microsoft Maia 200 integrated NIC 2.8TB/s 双向、Google TPU interconnect、AWS NeuronLink + EFA | 自研 ASIC rack/pod 内部通信 | 减少部分 merchant NIC，但提高外部 scale-out/前端需求 |
| UALink / ESUN scale-up | 2026 lab/pilot，2027 起量 | AMD MI400/Helios 生态、Marvell/XConn、Astera Scorpio、Broadcom/Meta 等 | rack/pod 内 accelerator scale-up | 与 NIC/DPU 部分边界融合，长期可能重估“网卡”定义 |
| CXL/PCIe fabric 与 Smart Cable | 导入期 | Astera Scorpio/Aries、Marvell/XConn、Credo、Broadcom retimer | host-NIC-GPU-SSD 连接、CXL memory pooling | 与 DPU/CXL memory/storage 形成下一代数据路径 |

### 1.3 机遇

1. **每颗 XPU 对外带宽上升**：GB300/Rubin、MI400、TPU、Trainium、MTIA、Maia 都把单节点性能推高，后端网络端口价值不随服务器台数线性增长，而随 accelerator 数量、带宽、radix、冗余和作业可靠性放大。
2. **Ethernet 重新夺回 AI 后端话语权**：InfiniBand 在 2023-2024 训练集群强势，但 hyperscaler 为避免单一供应商、兼容自研 ASIC、降低 TCO，推动 UEC、RoCE、Spectrum-X、Tomahawk、Thor、Pollara、Vulcano。
3. **DPU 从“云虚拟化税”变成“AI 数据路径收益”**：BlueField-4 STX/CMX、KV cache、NVMe-oF、inline compression/encryption、telemetry、agent session state 等让 DPU 在推理时代的价值上升。
4. **端点安全变成必须项**：AI 工厂的租户、模型权重、训练数据、agent 工具调用都需要 line-rate encryption、device attestation、secure boot、policy enforcement。Broadcom Thor Ultra 已把 line-rate encryption/decryption、PSP offload、secure boot、device attestation列为特性。[Broadcom Thor Ultra](https://investors.broadcom.com/news-releases/news-release-details/broadcom-introduces-industrys-first-800g-ai-ethernet-nic)
5. **云厂自研反而提高“端点 IP”价值**：AWS Nitro/EFA、Google/Intel IPU、Microsoft Maia on-die NIC 都说明网络端点是系统级差异化资产；不能只看 merchant NIC 出货，还要看 IP/NRE、custom silicon、软件栈和内部转移价值。

### 1.4 挑战

1. **标准碎片化**：InfiniBand、RoCEv2、UEC/UET、UALink、NVLink Fusion、ESUN、云厂私有 fabric 并行，供应商要做多协议、多客户、多认证。
2. **DPU 的“可编程性”与确定性延迟冲突**：P4/ARM/FPGA 使功能灵活，但大规模 AI 后端更看重 tail latency、JCT、BER、拥塞收敛和可观测性，软件错误会放大为集群级事故。
3. **价值可能被云厂内化**：AWS、Google、Microsoft 的 IPU/Nitro/Boost 不会形成完整 merchant TAM，第三方投资机会转移到 Broadcom/Marvell/Intel/NVIDIA 的定制芯片、IP 和制造服务。
4. **800G/1.6T 对功耗和散热很苛刻**：PCIe Gen6 x16、224G/112G SerDes、OCP 3.0、OSFP/铜缆/光模块会把 endpoint 从“插卡”变成热设计和信号完整性工程。
5. **供应链有隐性瓶颈**：高速 PCB、low-loss material、retimer、connector、cage、EEPROM/secure element、固件签名、测试时间、客户 lab qualification 都可能卡住放量。

## 2. 十大 AI 芯片平台背景下的技术成熟与放量时间

项目内已有 AI 芯片排序中，2026-2027 出货/价值权重最高的 10 条主线可归纳为：NVIDIA GB300/B300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA GB200/B200、Huawei Ascend 910C/950、Cambricon 590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200。它们对 NIC/DPU/SmartNIC 的拉动如下：

| AI 芯片/平台 | 2026 网络端点路线 | 对 NIC/DPU/SmartNIC 的需求 | 2026-2027 成熟/放量判断 |
|---|---|---|---|
| NVIDIA GB300/B300 | NVLink scale-up + ConnectX/SuperNIC + InfiniBand/Ethernet scale-out + BlueField | 高端 ConnectX/BlueField attach rate 极高，NVL72/GB300 推动 800G/1.6T、DPU telemetry/security、存储 offload | 2026 H2 大放量；2027 继续与 Rubin 并行 |
| AWS Trainium2 | NeuronLink within UltraServer + EFA across UltraServers + Nitro offload | EFA/Nitro 等效 DPU/NIC 内部需求巨大；Project Rainier 把 EFA 扩到多数据中心 | 2026 稳定扩张；Anthropic/AWS 进一步锁定容量 |
| Google TPU v7 Ironwood | TPU 内部互联 + OCS/光网络 + Intel/Google IPU | 自研 IPU/OCS/800G+ 光模块拉动大，但 merchant NIC 曝光较少 | 2026 大规模部署，2027 TPU8 延续 |
| NVIDIA GB200/B200 | ConnectX-7/8、BlueField-3、InfiniBand/Ethernet | 现有 Blackwell 网络订单延续，是 2026 上半年最成熟收入池 | 2026 继续放量，2027 让位给 GB300/Rubin |
| Huawei Ascend 910C/950 | HCCS/自研集群互联 + RoCE/Ethernet + 国产交换/网卡 | 中国本土 400G/800G 网卡、DPU、安全网卡、光模块、交换芯片机会 | 2026 国产替代拉动，受制于先进制程与生态 |
| Cambricon 590/690 | OAM/PCIe/RoCE + 国产集群网络 | 需要低成本、高可靠 200G/400G/800G endpoint；软件栈是瓶颈 | 2026 H2 起量，2027 看大客户集群 |
| AMD MI350 | Pensando Pollara 400 AI NIC + Ethernet/RoCE + UEC-ready | AMD rack 与 Oracle/企业云集群拉动 Pollara；400G 是确定性收入 | 2026 放量，2027 被 Vulcano/MI400 升级 |
| AWS Trainium3 | Neuron Fabric + EFA/Nitro 下一代 | 3nm Trainium3 UltraServer 提高 EFA 端点密度和带宽 | 2026-2027 放量，Trainium4 进入设计 |
| Meta MTIA | Broadcom XPU + Broadcom Ethernet scale-up/out/across | Meta/Broadcom multi-GW MTIA 直接拉动 Broadcom Ethernet NIC/switch/IP | 2026 开始，2027 多 GW 放大 |
| Microsoft Maia 200 | 片上 Ethernet NIC 2.8TB/s 双向 + Maia AI transport + Azure Boost | on-die NIC 减少部分卡级需求，但集群间网络、DPU/Boost、存储端点增加 | 2026 美国 Azure 部署，2027 扩大内部推理 |

### 2.1 技术成熟与放量三情景

| 技术 | 2026-05 状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|---|
| 400G AI NIC / SuperNIC | 已规模化，200G/400G NIC 收入快速增长 | 2026 全年仍主力；2027 降为中端/企业 AI | 2026 在 MI350、TPU、Trainium、国产集群保持强需求 | ASP 下行慢，400G 被海量推理和企业 AI 吸收 |
| 800G AI NIC | Broadcom Thor Ultra 发布；NVIDIA/AMD 进入路线图 | 2026 H2 hyperscaler pilot，2027 主流 | 2026 Q4 即明显贡献收入，2027 高端新建默认 | 2026 H2 供应短缺，2027 800G endpoint 收入超过 400G |
| 1.6T SuperNIC / PCIe Gen6 | ConnectX-9 文档和固件已出现；NVIDIA 称 up to 1.6Tb/s | 2026 H2/Rubin 早期，2027 高端 | 2027 成为 Rubin/MI400/ASIC premium cluster 主力 | 2027 前半即大规模采购，1.6T 抢占高毛利 |
| UEC/UET full-compliance | UEC 1.0/1.0.2 发布；Pollara 为 UEC-ready，Thor Ultra 称 full feature compliant | 2026 partial，2027 full compliance 集群 | 2026 H2 Meta/OpenAI/AMD/Google 相关集群导入 | 2027 UEC 成为 Ethernet AI backend 默认语义 |
| DPU/IPU for cloud offload | 已成熟，BlueField/Intel IPU/Pensando/Nitro/Boost | 2026 持续增长，企业渗透慢于云 | AI storage/security 让 DPU attach rate 上行 | DPU 成为每台 AI server 标配，甚至每 storage/context 节点多卡 |
| BlueField-4 STX / KV cache DPU | 2026 GTC 发布，partner availability 2026 H2 | 2026 H2 小批，2027 premium inference | 2027 成为长上下文/agent 推理标配 | 2027 形成 $10B+ 新收入池，DPU 估值逻辑上移 |
| UALink scale-up endpoint | 规范公开，商业部署目标 2026-2027 | 2026 lab，2027 小批 | MI400/Helios 2027 带动 UALink switch/endpoint | 2027 H2 成为 AMD/自研 ASIC 开放 scale-up 主路线 |
| CXL/PCIe fabric SmartNIC | Astera/Marvell/XConn/AEC/SCM 在扩产 | 2026 作为 host-side 辅助连接 | 2027 与 memory/storage pooling 结合 | DPU + CXL memory + storage 端点合流 |
| FPGA programmable SmartNIC | Napatech/Altera、Corigine 等成熟但小众 | 电信/安全/监控稳定增长 | AI inference preprocessing、UPF、security 增量 | 可编程拥塞/流处理被 AI 网络引入，利基高毛利 |

### 2.2 2026 最可能技术路径

2026 最可能不是“一条标准统治”，而是四条并行：

1. **NVIDIA 闭环**：GB200/GB300/早期 Rubin 继续用 NVLink scale-up + ConnectX/BlueField + InfiniBand/Ethernet。ConnectX-9、BlueField-4、Spectrum-6 与 CPO 是 2026-2027 的高端路径。
2. **开放 Ethernet AI 后端**：Broadcom Tomahawk/Thor、AMD Pollara/Vulcano、Arista/Cisco/HPE/Nokia 等承接 ASIC 与多供应商 GPU 集群，UEC-ready 先走，full UEC 2027 更明确。
3. **云厂自研 IPU/NIC**：AWS Nitro/EFA、Google/Intel IPU、Microsoft Azure Boost/Maia on-die NIC 内化端点价值，但会向 Broadcom/Marvell/Intel/NVIDIA 释放 ASIC/NRE/IP/制造机会。
4. **DPU 走向 AI-native storage/security**：BlueField-4 STX、CMX、NVMe-oF、KV cache、agent memory、confidential AI 让 DPU 从传统 IaaS offload 扩到推理数据路径。

## 3. 已开始放量的关键产品：市场规模、渗透率、利润率

> 口径：未来 3 个月为 2026-05 至 2026-08 收入池估算；未来一年为 2026-05 至 2027-05；未来两年为 2026-05 至 2028-05。这里包括 merchant 销售与 hyperscaler 自研内部等效价值，但在公司收入识别上不能简单相加。

### 3.1 已放量产品总表

| 已放量产品/技术 | 关键事实 | 未来3个月市场规模：B/O/X | 未来一年市场规模：B/O/X | 未来两年市场规模：B/O/X | 渗透率路径 | 毛利率/利润率判断 |
|---|---|---:|---:|---:|---|---|
| 400G/800G AI back-end NIC / SuperNIC | Crehan：server-class Ethernet NIC 2025 >$13B；200G/400G 收入一年超 3x。Broadcom Thor Ultra 800G 发布；NVIDIA ConnectX-9 up to 1.6Tb/s。 | $5-7B / $7-10B / $10-14B | $24-34B / $34-50B / $50-70B | $55-85B / $85-130B / $130-190B | 400G 在 2026 仍主力；800G 在高端新建 AI 后端 2026 10-25%，2027 35-60%，2028 55-75% | Silicon/IP 55-75%；NVIDIA/Broadcom 供不应求可 70%+；卡厂/ODM 10-25% |
| NVIDIA ConnectX/BlueField/SuperNIC | BlueField-4 800Gb/s；ConnectX-9 SuperNIC 最高 1.6Tb/s；Vera Rubin 包含 ConnectX-9 与 BlueField-4。[NVIDIA BlueField-4](https://blogs.nvidia.com/blog/bluefield-4-ai-factory/)、[ConnectX-9](https://www.nvidia.com/en-us/networking/infiniband-adapters/) | $2.5-4B / $4-6B / $6-9B | $13-20B / $20-32B / $32-48B | $28-45B / $45-75B / $75-110B | NVIDIA GPU rack attach rate 极高；Ethernet/IB 双栈继续扩张 | 公司 FY26 Q4 GAAP GM 75.0%；网络端点估计 65-78%，极端缺货 78-82% |
| Broadcom 400G RoCE/RDMA + Thor Ultra 800G NIC | Thor Ultra 称行业首款 800G AI Ethernet NIC，UEC compliant，PCIe Gen6 x16，packet-level multipathing、OOO、selective retransmission。[Broadcom Thor](https://investors.broadcom.com/news-releases/news-release-details/broadcom-introduces-industrys-first-800g-ai-ethernet-nic) | $1.0-1.8B / $1.8-3.0B / $3.0-5.0B | $6-10B / $10-18B / $18-30B | $15-28B / $28-55B / $55-90B | Meta/OpenAI/Google/ASIC 集群拉动；2027 UEC full-compliance 提升份额 | Broadcom Q1 FY26 adjusted EBITDA 68%；AI NIC/switch silicon 60-75%，极端 75%+ |
| AMD Pensando Pollara 400 AI NIC | Pollara 400 为 UEC-ready、OCP 3.0、P4 programmable，最高 400Gb/s；AMD 称可改善部分应用 runtime 约 15%、网络 uptime 约 10%。[AMD Pollara](https://www.amd.com/en/products/network-interface-cards/pensando.html) | $0.25-0.45B / $0.45-0.8B / $0.8-1.2B | $1.5-2.5B / $2.5-4.5B / $4.5-7B | $4-8B / $8-14B / $14-25B | MI350/企业 AI/Oracle 等用 400G；2027 向 Vulcano 800 迁移 | AMD 公司 Q1 2026 GAAP GM 53%、Q2 non-GAAP GM 指引约 56%；Pensando 高端 45-62%，捆绑 MI400 可 55-68% |
| 云厂自研 EFA/Nitro/IPU/Azure Boost | AWS EFA 支持 AI/ML/HPC，Nitro v4+ 支持 RDMA read/write；Project Rainier 用 EFA 连接 UltraServers。Google 与 Intel 2026 扩大 custom ASIC IPU；Azure Boost 清除 I/O/network/storage bottleneck。 | $3-5B / $5-8B / $8-12B | $15-24B / $24-38B / $38-55B | $35-60B / $60-95B / $95-150B | hyperscaler 内部 AI server 几乎标配；merchant 不可直接获得全部收入 | 不作为供应商 GM；云服务通过 TCO/利用率捕获价值，等效 ROIC 高 |
| Intel IPU E2100 / Google custom IPU | Intel E2100 200GbE、NVMe/compression/crypto accelerators、Arm Neoverse N1；Intel-Google 2026 多年合作继续 co-develop custom ASIC IPU。[Intel E2100](https://www.intel.com/content/www/us/en/products/details/network-io/ipu/adapter-e2100.html)、[Intel-Google](https://newsroom.intel.com/data-center/intel-google-deepen-collaboration-to-advance-ai-infrastructure) | $0.3-0.7B / $0.7-1.2B / $1.2-2B | $2-4B / $4-7B / $7-12B | $5-10B / $10-18B / $18-30B | merchant 200G 企业/云小口径，Google custom 大口径 | Intel Q1 2026 non-GAAP GM 41.0%；IPU/custom 估计 30-50%，定制 NRE 可更高 |
| Microsoft Maia 200 片上 NIC/AI transport | Maia 200 on-die NIC 2.8 TB/s 双向，Ethernet scale-up interconnect，可扩到 6,144 accelerators。[Microsoft deep dive](https://techcommunity.microsoft.com/blog/azureinfrastructureblog/deep-dive-into-the-maia-200-architecture/4489312) | $0.2-0.5B / $0.5-1B / $1-2B | $2-5B / $5-9B / $9-15B | $7-15B / $15-28B / $28-45B | 内部推理 ASIC 先导；外部前端/存储网络仍增加 | 片上 NIC 无独立 GM；价值体现为推理性能/美元、Azure 毛利与 GPU 替代 |
| FPGA/可编程 SmartNIC/DPU | Napatech F3070X/F3076X 400G DPU，Altera Agilex FPGA + Xeon 6 SoC；Corigine Agilio NFP 等。[Napatech](https://www.napatech.com/) | $0.3-0.6B / $0.6-0.9B / $0.9-1.4B | $1.5-2.8B / $2.8-4.5B / $4.5-7B | $3.5-6.5B / $6.5-10B / $10-16B | 安全/监控/电信/UPF/定制 offload；AI 后端不是主流 | 硬件 35-55%；含软件/IP 50-70%；量小但利基高 |
| SmartNIC/DPU 软件栈 | DOCA、Pensando P4、DPDK/SPDK、EFA/libfabric、UET、telemetry/congestion control | $0.4-0.8B / $0.8-1.4B / $1.4-2.5B | $2-4B / $4-7B / $7-12B | $6-12B / $12-22B / $22-40B | 软件 attach 随 DPU/NIC 增长；可随云服务内化 | 软件/订阅/支持 70-90%；但常被硬件捆绑隐藏 |

### 3.2 细分产品增长区间

| 产品/技术 | 当前位置 | 未来一年增长：基准/乐观/极超 | 未来两年增长：基准/乐观/极超 | 定价能力 |
|---|---|---:|---:|---|
| 400G foundational AI NIC | 成熟放量，企业/NeoCloud/MI350/国产集群主力 | +25-45% / +45-70% / +70-100% | +50-90% / +90-150% / +150-220% | 中等，ASP 下行但量足 |
| 800G AI Ethernet NIC | 2026 高端导入 | +80-150% / +150-250% / +250%+ | +250-500% / +500-900% / +900%+ | 高，UEC/PCIe Gen6/SerDes 瓶颈支撑溢价 |
| 1.6T SuperNIC | 早期，NVIDIA ConnectX-9/Rubin 先行 | +100%+ 但基数低 | 2027-2028 可成 $10-30B 早期池 | 极高，认证和供给壁垒强 |
| DPU/IPU cloud offload | 成熟但云厂内化 | +30-50% / +50-80% / +80-120% | +70-120% / +120-220% / +220%+ | 高于普通 NIC，低于 GPU |
| AI-native storage DPU | 刚发布/导入 | +200% 低基数 / $1.5-4B / $4-8B | $8-20B / $20-45B / $45B+ | 早期极高，取决于 BlueField-4 STX/CMX 真实采用 |
| Programmable FPGA SmartNIC | 利基成熟 | +10-25% / +25-45% / +45-70% | +30-60% / +60-100% / +100-160% | 软件/IP 支撑较好，但量受限 |

## 4. 在研关键产品与快速增长技术

### 4.1 在研/导入期产品总表

| 在研产品/技术 | 当前状态 | 未来3个月市场规模：B/O/X | 未来一年市场规模：B/O/X | 未来两年市场规模：B/O/X | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| NVIDIA BlueField-4 STX / CMX context memory | GTC 2026 发布；Supermicro 等推出 STX storage server；2026 H2 partner availability。[Supermicro](https://www.supermicro.com/en/pressreleases/supermicro-among-first-unveil-nvidia-bluefield-4-stx-storage-server-improve-ai) | $0.05-0.15B / $0.15-0.35B / $0.35-0.7B | $1.2-3B / $3-6B / $6-12B | $8-18B / $18-35B / $35-60B | 长上下文/agent/KV cache 推理 2026 低个位数，2027 10-25%，2028 25-45% | 60-80%；软件/系统绑定极强 |
| Broadcom Thor Ultra 800G full UEC | 2025-10 发布；2026 与 Tomahawk 6/UEC 生态验证 | $0.2-0.6B / $0.6-1.2B / $1.2-2.2B | $3-7B / $7-15B / $15-25B | $12-28B / $28-55B / $55-85B | 2026 高端 ASIC/GPU Ethernet；2027 成主流候选 | 60-78%；供不应求阶段高 |
| AMD Pensando Vulcano 800 AI NIC | AMD 2026-05 博客称 Vulcano 800 正在为 MI400 clusters qualification，GA 计划面向 Vulcano 800 platforms。[AMD Vulcano/MRC](https://www.amd.com/en/blogs/2026/next-gen-networking-transport-for-large-scale-ai-training.html) | $0.03-0.12B / $0.12-0.3B / $0.3-0.6B | $0.8-2B / $2-5B / $5-10B | $6-14B / $14-30B / $30-55B | MI400/Helios 2026 H2 qual，2027 放量 | 50-68%；与 MI400 rack 捆绑后议价增强 |
| UEC/UET hardware compliance | UEC 1.0/1.0.2 规范，compliance program 和实现推进 | $0.2-0.5B / $0.5-1.0B / $1-2B | $2-5B / $5-12B / $12-20B | $18-40B / $40-80B / $80-130B | 2026 UEC-ready，2027 full-compliance，2028 成 AI Ethernet 默认 | 标准本身不变现，silicon/software 55-75% |
| UALink scale-up NIC/switch endpoint | 1.0 可用，2.0 2026 发布；目标 2026-2027 商用 | $0.02-0.08B / $0.08-0.2B / $0.2-0.5B | $0.5-1.5B / $1.5-4B / $4-8B | $5-15B / $15-35B / $35-70B | 2026 lab/qualification，2027 MI400/ASIC pod 初量产，2028 扩散 | 早期 60-80%，但互操作失败会拖慢 |
| Enfabrica ACF-S 3.2Tbps Multi-GPU SuperNIC | 官方称 3.2Tbps multi-GPU SuperNIC，multi-port 800GbE、PCIe Gen5、CXL2.0+，目标降低 CapEx/OpEx。[Enfabrica](https://enfabrica.net/solution/acf-s) | $0.02-0.06B / $0.06-0.15B / $0.15-0.3B | $0.3-0.8B / $0.8-2B / $2-4B | $2-6B / $6-15B / $15-30B | 2026 niche pilot，2027 若大客户验证则快速放大 | 55-75%；startup NRE/软件价值高但执行风险大 |
| Marvell/XConn/Astera PCIe/CXL/UALink fabric endpoint | Marvell 2026-01 收购 XConn 强化 PCIe/CXL/UALink switching；Astera Scorpio 32-320 lane AI fabric switches。[Marvell-XConn](https://www.marvell.com/company/newsroom/marvell-to-acquire-xconn-technologies-expanding-leadership-in-ai-data-center-connectivity.html)、[Astera Scorpio](https://www.asteralabs.com/products/scorpio-smart-fabric-switch/) | $0.2-0.5B / $0.5-0.9B / $0.9-1.5B | $2-4B / $4-8B / $8-14B | $8-18B / $18-35B / $35-60B | 先是 PCIe/CXL fabric，随后接 UALink/CXL memory | 55-75%；Retimer/fabric silicon 高毛利 |
| 片上 NIC / accelerator-integrated NIC | Microsoft Maia 200 已公开；Google TPU/AWS Trainium 私有化 | $0.3-0.8B / $0.8-1.5B / $1.5-3B | $4-8B / $8-16B / $16-28B | $15-35B / $35-70B / $70-120B | 自研 ASIC 内部采用高；merchant NIC 部分被替代 | 不独立售卖；价值由云厂 TCO/毛利捕获 |
| CPO/optical I/O near NIC/DPU | 交换机侧更早，endpoint 侧 2027+ | <$0.05B / <$0.1B / $0.2B | $0.2-0.8B / $0.8-2B / $2-5B | $3-8B / $8-20B / $20-45B | 先在 switch/CPO，后向 endpoint/optical I/O 扩散 | 光引擎/laser 50-75%，系统服务成本高 |

### 4.2 关键技术放量时间线

| 时间 | 最可能发生 | 受益产品 |
|---|---|---|
| 2026 Q2-Q3 | GB300/Blackwell Ultra 与 MI350/Trainium2/Ironwood 持续拉 400G/800G endpoint；Thor Ultra/Vulcano/ConnectX-9 进入更多客户 qual | ConnectX、BlueField、Pollara、Thor、EFA/Nitro、Google IPU |
| 2026 Q4 | Rubin/BlueField-4 STX/Vulcano 800 早期出货，UEC-ready 产品进入首批大集群；Maia 200 美国区域扩容 | 800G NIC、DPU/STX、UEC software/telemetry |
| 2027 H1 | 1.6T/PCIe Gen6 endpoint、UEC full-compliance、UALink lab-to-production 过渡 | ConnectX-9、Thor Ultra、Vulcano、Marvell/Astera/XConn |
| 2027 H2 | Rubin/MI400/MTIA/OpenAI ASIC/TPU8 并行，open Ethernet + proprietary fabric 同时放量 | AI Ethernet NIC/DPU、scale-up fabric、CXL/PCIe fabric |
| 2028 | DPU + storage + CXL memory + optical I/O 融合，端点从 NIC 卡演进为 AI data movement subsystem | BlueField-4/5、Pensando、Marvell OCTEON/XConn、Astera、Enfabrica |

## 5. 供给侧：产能结构、瓶颈、成本与毛利

### 5.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/能力 |
|---|---|---|---|
| 高端 NIC/DPU/SmartNIC silicon 设计 | 美国、以色列、印度、英国、中国 | NVIDIA、Broadcom、AMD Pensando、Intel、Marvell、AWS Annapurna、Google、Microsoft、Meta、Enfabrica、Astera、Napatech、Corigine | ASIC/SoC、P4 pipeline、ARM cores、crypto/compression/NVMe/RDMA offload、SerDes |
| 晶圆制造 | 台湾、美国、韩国、中国大陆 | TSMC、Samsung、Intel Foundry、GlobalFoundries、SMIC | 7/6/5/4/3nm 高速 SerDes SoC；部分成熟节点 PHY/控制器；FPGA 依赖 Intel/TSMC |
| 封装与测试 | 台湾、中国大陆、马来西亚、新加坡、美国 | ASE、Amkor、SPIL、KYEC、JCET、Unimicron/AT&S/Ibiden 等 | 高速 BGA/FCBGA、ABF substrate、SerDes/BER/thermal/burn-in test |
| 板卡/系统集成 | 台湾、中国大陆、墨西哥、美国、东欧、东南亚 | Foxconn、Jabil、Flex、Celestica、Wistron、Quanta、Wiwynn、UfiSpace、Supermicro、Dell、HPE | OCP 3.0/PCIe CEM 卡、散热器、cage、EEPROM、固件烧录、系统 qualification |
| 连接器/线缆/光模块配套 | 美国、台湾、中国大陆、日本、东南亚 | Amphenol、TE、Molex、Samtec、Credo、Astera、Coherent、Lumentum、Fabrinet、Innolight、Eoptolink | DAC/AEC、OSFP/QSFP cage、retimer、光模块、ELS/CPO 相关 |
| 软件/验证 | 美国、以色列、印度、欧洲、中国 | NVIDIA DOCA、AMD Pensando P4、Intel IPDK、AWS EFA/libfabric、UEC/UALink/OCP 社区、DPDK/SPDK | RDMA/congestion、telemetry、secure boot、attestation、Kubernetes/CNI/storage plugin |

### 5.2 供给瓶颈

1. **高速 SerDes 与 PCIe Gen6 PHY**：800G/1.6T endpoint 需要 112G/224G SerDes、PCIe Gen6 x16、超低 BER。SerDes IP、验证向量、封装 SI/PI 是核心瓶颈。
2. **低损耗 PCB/连接器/cage/线缆**：OCP 3.0 与 PCIe Gen6 让板级损耗、crosstalk、散热和机械公差变得更难，Amphenol/TE/Molex/Samtec、Megtron/low-loss materials 等价值上升。
3. **测试与 burn-in 时间**：AI NIC 的真实瓶颈常在 BER、FEC、RDMA congestion、packet drop、link flap、firmware rollback 和百万 endpoint soak test，而不是芯片 tape-out。
4. **客户认证周期**：hyperscaler 对 firmware、secure boot、attestation、telemetry、Redfish/OCP、驱动、内核版本和故障恢复要求极高，认证可达 6-18 个月。
5. **软件人才与协议栈复杂度**：UEC/UET、RoCE、P4、DPDK/SPDK、NVMe-oF、Kubernetes CNI、storage plugin、congestion control 需要少数资深团队，人才比产线更稀缺。
6. **高端晶圆与封装排产**：DPU/NIC 不是 GPU/HBM 那样最大客户，但 5/4/3nm、ABF substrate 与高速封装仍会被 GPU/ASIC 挤压。
7. **光模块/DAC/AEC 配套短缺**：800G/1.6T NIC 端点没有足够 optical/copper links 就无法出货；Credo/Astera/Coherent/Lumentum/Innolight/Fabrinet 等会同步瓶颈化。
8. **安全与合规认证**：line-rate encryption、secure boot、PSP offload、device attestation、FIPS/CC/云厂 internal compliance 都会延迟量产。

### 5.3 成本构成与毛利决定因素

| 产品 | 典型成本构成 | 毛利决定因素 | 价格传导 |
|---|---|---|---|
| 400G/800G foundational NIC | Controller ASIC/SerDes 30-45%；PCB/VRM/thermal 10-15%；connector/cage 8-15%；memory/flash 5-10%；test/burn-in 10-15%；组装 5-10%；固件支持 5-10% | SerDes 领先性、BER、PCIe/OCP 认证、客户 volume、是否绑定 switch/software | AI 集群上线延迟成本远高于 NIC 溢价，短缺时可向客户传导 |
| DPU/IPU/SmartNIC | DPU SoC 35-50%；DDR/flash/secure element 8-15%；network PHY/cage 10-15%；board/power/thermal 10-15%；software/qualification 10-20%；test 8-12% | offload 功能、软件生态、租户隔离、安全认证、云厂 design-in | 一旦进入云厂 rack design，生命周期长、切换成本高 |
| AI SuperNIC / 1.6T endpoint | ASIC/SerDes 40-55%；retimer/gearbox 5-10%；高端 PCB/connector 10-15%；散热 5-10%；测试 15-20%；固件/telemetry 5-10% | PCIe Gen6、224G SerDes、UEC/IB/NVLink 生态、散热与可靠性 | 高端 GPU idle cost 支撑高溢价；极端情景毛利率可接近 GPU 平台 |
| FPGA programmable SmartNIC | FPGA 35-55%；DDR/QDR/HBM 可选 10-20%；board/thermal 15-20%；软件/IP 15-30%；测试 10-15% | 客户定制 IP、软件包、5G/security/monitoring 认证 | 量小价高，按项目/NRE/软件订阅传导 |
| 片上 NIC / custom IPU | NRE/验证/IP 授权高；unit cost 内含在 ASIC SoC | 云厂 TCO、面积/功耗、IP 授权、代工良率 | 不以独立 ASP 出现，价值转化为云服务毛利和 custom ASIC NRE |

## 6. 竞争格局与壁垒

### 6.1 市场结构

| 口径 | 结构判断 |
|---|---|
| 高端 AI back-end endpoint silicon | NVIDIA 与 Broadcom 双强，AMD Pensando 在 AMD/Oracle/企业 AI 生态补位，云厂自研在 AWS/Google/Microsoft 内部占大头。前四大/自研体系合计可超过 80%。 |
| Ethernet server NIC | 2025 收入已超 $13B；高端 200G/400G 超过一半。Broadcom、NVIDIA、Intel、AMD、Marvell 等占据主要份额。 |
| DPU/IPU/SmartNIC | NVIDIA BlueField、AMD Pensando、Intel/Google IPU、AWS Nitro、Azure Boost、Marvell OCTEON、Napatech/Corigine 等分层竞争；云厂内部方案占用大量等效价值。 |
| FPGA/可编程 SmartNIC | Napatech、Altera/Intel、Corigine/Netronome lineage、Xilinx/AMD Alveo/Pensando 生态，更多是安全/电信/监控利基市场。 |
| 新兴 scale-up/fabric endpoint | Marvell/XConn、Astera、Enfabrica、Broadcom、AMD、NVIDIA、UALink/UEC/OCP 成员并行。 |

### 6.2 壁垒清单：为什么能定价

| 壁垒 | 具体含义 | 为什么能定价 |
|---|---|---|
| SerDes/PHY 壁垒 | 112G/224G、PCIe Gen6、CXL、OSFP/QSFP、low BER | link flap 会直接拖慢/中断训练作业；客户愿为稳定性付溢价 |
| RDMA/congestion 壁垒 | multipathing、OOO、selective retransmission、receiver/sender congestion、telemetry | Job Completion Time 对尾延迟极敏感；好的拥塞控制节省 GPU idle 成本 |
| 软件生态壁垒 | DOCA、Pensando P4、EFA/libfabric、IPDK、DPDK/SPDK、K8s/CNI/storage plugin | 软件集成后切换成本很高，客户不愿为便宜卡重写和重测 |
| 客户认证壁垒 | hyperscaler/OEM/rack-level qualification、firmware signing、security attestation | 进入 AVL/RVL 后生命周期长，新供应商导入周期慢 |
| 系统绑定壁垒 | NVIDIA GPU+NVLink+ConnectX+BlueField+Spectrum；AMD GPU+Pensando；Broadcom XPU+Tomahawk+Thor | endpoint 不单独卖卡，而是卖 AI fabric 的可用性和系统性能 |
| 标准参与壁垒 | UEC/UALink/OCP/PCI-SIG/CXL/OIF 的早期参与和实现 | 标准落地前就影响客户 design，形成事实标准 |
| 规模与供应链壁垒 | 高速芯片流片、测试平台、光模块/线缆配套、全球 field support | 2026 需求陡增时，能交付比低价更重要 |
| 安全/可信壁垒 | secure boot、device attestation、line-rate crypto、tenant isolation | AI 权重和数据安全高价值，安全事故成本巨大 |

### 6.3 价值捕获

长期最可能拥有高 ROIC/高毛利的是：

1. **高速 NIC/DPU ASIC + 协议软件栈**：NVIDIA、Broadcom、AMD Pensando、Marvell、Intel/custom IPU。原因是 SerDes、RDMA、firmware、security、客户认证和系统绑定共同形成壁垒。
2. **云厂自研 IPU/NIC**：AWS Nitro/EFA、Google IPU、Azure Boost/Maia on-die NIC 不一定产生外部收入，但会让云厂把利用率、隔离和 TCO 优势转化为云服务毛利。
3. **AI-native storage/KV cache DPU**：如果 agentic inference 长上下文爆发，BlueField-4 STX/CMX 这类产品可能从“网卡”变成“token throughput 处理器”，毛利率和估值逻辑都会上移。
4. **SerDes/retimer/fabric switch IP**：Astera、Credo、Marvell/XConn、Broadcom 等在 PCIe/CXL/UALink/optical I/O 的瓶颈环节利润率会优于板卡。

低 ROIC 环节主要是普通板卡组装、通用低速 NIC、没有软件/IP 的代工和白牌卡。

## 7. 2026 关键变化：三个最可能拐点

### 拐点一：800G AI Ethernet NIC 从“演示/发布”进入 hyperscaler qualification

Broadcom Thor Ultra 800G、NVIDIA ConnectX-9、AMD Vulcano 800 都把 2026 下半年变成 800G endpoint 的真实导入窗口。2026 的“量”仍会由 400G 承担大头，但高端新建 AI cluster 的设计窗口会转向 800G/PCIe Gen6。

投资方向：Broadcom、NVIDIA、AMD Pensando、Marvell/SerDes、Astera/Credo、Amphenol/TE/Molex/Samtec、800G 光模块/AEC。

### 拐点二：DPU 从 front-end/security 走向 AI-native storage/KV cache

NVIDIA BlueField-4 STX 与 CMX 是 2026 最关键的一手信号。它说明 DPU 不只是虚拟网卡、安全和 NVMe-oF offload，而是开始服务 agentic AI 的 context memory、KV cache 复用、长会话状态和 storage-to-GPU throughput。

投资方向：NVIDIA BlueField/DOCA、VAST/DDN/WEKA/NetApp/Dell/HPE/Supermicro 生态、NVMe SSD、CXL memory、storage software。

### 拐点三：云厂自研 ASIC 迫使开放端点生态成形

Meta/Broadcom multi-GW MTIA、OpenAI/Broadcom 10GW、Google/Intel IPU、AWS Trainium/EFA、Microsoft Maia 200 共同说明：AI 计算不会只在 NVIDIA 闭环里扩张。开放 Ethernet、UEC、UALink、custom IPU/NIC、片上 NIC 会共同放量。

投资方向：Broadcom、Marvell、AMD Pensando、Intel custom IPU、Astera/XConn/Enfabrica、UEC/UALink test equipment、Arista/Cisco/HPE/Nokia。

## 8. 2027 关键变化：三个最可能拐点

### 拐点一：UEC full-compliance 进入真实生产，Ethernet AI 后端份额继续上升

2027 年最重要的不是“Ethernet 是否能跑 AI”，而是 UEC/UET 能否让多供应商 NIC/switch/optics 在 100k+ endpoint 集群中稳定运行。如果成功，Broadcom/AMD/Marvell/Arista/Cisco/HPE 会共享比 2026 更大的开放 AI fabric 池。

### 拐点二：1.6T / PCIe Gen6 / 224G SerDes 成为高端 endpoint 的新稀缺

Rubin、MI400/MI450、TPU8、Trainium3/4、MTIA/OpenAI ASIC 进入并行扩产后，800G 会从高端变成主流，1.6T 则成为高毛利、高认证门槛的新前沿。

### 拐点三：UALink/ESUN/CXL fabric 让“网卡”边界扩展

2027 的新产品不一定长得像传统 NIC。scale-up endpoint、CXL memory fabric、PCIe 6 fabric switch、optical I/O、AI storage DPU 会把网络、存储、内存和 accelerator fabric 合并为 data movement subsystem。Marvell/XConn、Astera、Broadcom、AMD、NVIDIA、Enfabrica 都会在这里争夺定义权。

## 9. 头部公司与细分技术公司清单

### 9.1 高端 AI NIC / SuperNIC / DPU / IPU

| 公司 | 位置与优势 |
|---|---|
| NVIDIA | ConnectX、BlueField、SuperNIC、InfiniBand、Spectrum-X、DOCA、NVLink 生态；AI 网络端点最强闭环。 |
| Broadcom | Thor/Thor Ultra NIC、Tomahawk/Jericho/Tomahawk Ultra、UEC、optical DSP、custom XPU；AI Ethernet 开放生态核心。 |
| AMD Pensando | Pollara 400、Vulcano 800、Elba/Salina DPU、P4 programmable；与 EPYC/Instinct/Helios 绑定。 |
| Intel | IPU E2100、FPGA IPU、Google custom ASIC IPU、Xeon 服务器生态；优势是云厂 CPU/IPU co-design。 |
| Marvell | OCTEON DPU、custom ASIC、NVLink Fusion partnership、UALink/scale-up、XConn PCIe/CXL、optical DSP。 |
| AWS Annapurna | Nitro、EFA、Trainium/Inferentia 网络与 offload；内部价值巨大。 |
| Google | TPU pod 网络、OCS、custom IPU with Intel、Jupiter/Apollo 网络；内部 scale 和架构领先。 |
| Microsoft | Azure Boost、Maia 200 on-die NIC/AI transport、Azure AI networking；内部推理端点价值高。 |
| Meta | MTIA 与 Broadcom Ethernet、OCP/open rack、AI fabric 架构需求方和共同定义者。 |
| Enfabrica | ACF-S 3.2Tbps Multi-GPU SuperNIC，startup 高风险高弹性。 |
| Napatech | FPGA SmartNIC/DPU，400G 可编程安全/监控/电信/AI pipeline 利基。 |
| Corigine | Agilio SmartNIC/Netronome NFP 传承，OVS/DPDK/cloud offload。 |

### 9.2 AI Ethernet / switch / fabric 配套

| 公司 | 位置与优势 |
|---|---|
| Arista | hyperscaler AI Ethernet switch、EOS、XPO MSA 参与；AI 后端 Ethernet 龙头设备商之一。 |
| Cisco | Silicon One、Ethernet AI fabric、UALink/UEC/OCP 参与，企业与云网络渠道强。 |
| HPE Juniper | HPE/Juniper AI networking、Slingshot/UEC 知识、企业/HPC 渠道。 |
| Nokia | AI-ready data center network、UEC、coherent/line system、multi-rail DCI。 |
| Celestica | AI switch ODM/white-box 供应链受益。 |
| UfiSpace/Edgecore/Micas | 白牌/开放交换机、OCP/SONiC 生态。 |
| Broadcom | Tomahawk 6/Ultra/Jericho 4 与 Thor Ultra 形成端到端 Ethernet silicon。 |
| NVIDIA | Spectrum-X、Spectrum-6、Quantum-X、CPO Ethernet/IB。 |

### 9.3 PCIe/CXL/UALink/retimer/AEC/连接

| 公司 | 位置与优势 |
|---|---|
| Astera Labs | Aries retimer/Smart Cable、Scorpio PCIe/CXL/AI fabric switch、UALink 2.0 生态。 |
| Credo | AEC、retimer、SerDes connectivity，AI rack 铜连接受益。 |
| Marvell/XConn | PCIe/CXL/UALink switching、custom compute platform。 |
| Broadcom | PCIe Gen6 switches/retimers、SerDes、AEC、optical DSP。 |
| Synopsys/Cadence/Alphawave Semi | UEC/UALink/PCIe/CXL/SerDes IP 与验证。 |
| Amphenol | OSFP/QSFP、cable、connector、high-speed interconnect。 |
| TE Connectivity | 高速连接器、copper interconnect、cage。 |
| Molex | CPO/CPX/optical connector、high-speed cable。 |
| Samtec | high-speed board/cable/socket interconnect，CPX/CPO 生态。 |

### 9.4 光/铜互联与测试

| 公司 | 位置与优势 |
|---|---|
| Coherent | 800G/1.6T optics、SiPh/InP/laser、CPO optical engine。 |
| Lumentum | EML、laser、ELS、1.6T/CPO 关键光源。 |
| Fabrinet | 光模块 EMS，AI datacom 代工。 |
| Innolight / 中际旭创 | 800G/1.6T 光模块龙头，Google/AI 客户高弹性。 |
| Eoptolink / 新易盛 | 800G/1.6T/XPO 等高端光模块。 |
| AOI | datacom optics，AI 客户带动恢复。 |
| Marvell | PAM4/coherent DSP、COLORZ、optical interconnect。 |
| Broadcom | 200G/400G lane DSP、optical PHY、CPO。 |
| VIAVI | 1.6T/3.2T Ethernet、FEC、MAC、224G SerDes 测试。 |
| Keysight | UALink/PCIe/SerDes compliance、high-speed validation。 |
| Spirent | 网络测试、traffic generation、AI fabric validation。 |

### 9.5 板卡/OEM/ODM/系统集成

| 公司 | 位置与优势 |
|---|---|
| Supermicro | NVIDIA BlueField-4 STX、AI server/rack 快速导入。 |
| Dell | AI factory、Azure/NVIDIA/enterprise 服务器渠道。 |
| HPE | NVIDIA/AMD AI rack、HPC/Cray/Slingshot 经验。 |
| Lenovo | AI server、Neptune liquid cooling、企业渠道。 |
| Foxconn/Hon Hai | AI server/rack ODM、大规模制造。 |
| Quanta/Wiwynn/Wistron/Inventec | hyperscaler AI server/rack ODM。 |
| Jabil/Flex/Celestica | NIC/switch/server EMS 与区域制造。 |
| Delta/Accton/Edgecore | switch/网络设备制造与开放网络。 |

## 10. 投资跟踪指标

| 指标 | 为什么重要 |
|---|---|
| Crehan/IDC/Dell'Oro 对 NIC、DPU、Ethernet switch 的季度收入和端口速率拆分 | 验证 800G/1.6T 是否真正从发布走向收入 |
| NVIDIA Data Center networking 增速与 ConnectX/BlueField/Spectrum 出货 | 判断 NVIDIA 闭环是否继续高溢价 |
| Broadcom AI revenue 中 networking vs custom accelerator 贡献 | 判断 Thor/Tomahawk/UEC 是否成为第二曲线 |
| AMD Pensando Vulcano 800 qualification 与 MI400/Helios 客户 | 判断 AMD 是否能把 GPU + NIC 绑成 rack-scale 平台 |
| Intel-Google IPU 合作进展 | 判断 custom IPU 是否继续内化 merchant DPU TAM |
| UEC compliance/interoperability plugfest | 判断 2027 Ethernet AI 后端能否跨供应商大规模部署 |
| UALink silicon lab/production 节点 | 判断 2027 open scale-up 能否实质替代部分 NVLink lock-in |
| BlueField-4 STX/CMX 客户案例 | 判断 DPU 是否从 cloud offload 升级为 AI storage/KV cache 处理器 |
| 光模块/AEC/DAC/connector 交期 | endpoint 端口价值必须靠物理链路交付兑现 |
| AI rack GPU/XPU attach rate 与每 XPU 网络带宽 | NIC/DPU TAM 的核心驱动变量 |

## 11. 风险

1. AI CapEx 或 token 需求低于预期，导致 NIC/DPU 订单从 2026 H2 延后到 2027。
2. 800G/1.6T 端口 ASP 下行快于预期，量增无法完全抵消价格压力。
3. UEC/UALink 互操作和软件成熟慢，2027 仍以私有/闭环 fabric 为主。
4. 云厂自研 IPU/NIC 继续内化价值，merchant DPU 小口径 TAM 低于乐观情景。
5. 高速 SerDes、光模块、AEC、连接器、PCIe Gen6 认证任一环节延期，影响整机交付。
6. 出口管制改变中国市场节奏，国产 NIC/DPU 放量路径和海外供应商份额均可能波动。

## 12. 主要资料来源

| 类别 | 来源 |
|---|---|
| NVIDIA 一手资料 | [NVIDIA FY2026 results](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/), [Vera Rubin platform](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform), [BlueField-4](https://blogs.nvidia.com/blog/bluefield-4-ai-factory/), [ConnectX-9](https://www.nvidia.com/en-us/networking/infiniband-adapters/), [Vera Rubin technical blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) |
| Broadcom 一手资料 | [Thor Ultra 800G AI NIC](https://investors.broadcom.com/news-releases/news-release-details/broadcom-introduces-industrys-first-800g-ai-ethernet-nic), [OFC 2026 AI infrastructure](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai), [Q1 FY2026 results](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000011/avgo-02012026x8kxex99.htm), [Meta partnership](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-extended-partnership-meta-deploy-technology) |
| AMD/Pensando | [Pollara 400 AI NIC](https://www.amd.com/en/products/network-interface-cards/pensando.html), [Pensando DPU](https://www.amd.com/en/products/data-processing-units/pensando.html), [Vulcano/MRC blog](https://www.amd.com/en/blogs/2026/next-gen-networking-transport-for-large-scale-ai-training.html), [AMD Q1 2026](https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results) |
| Intel/Google/Microsoft/AWS | [Intel IPU E2100](https://www.intel.com/content/www/us/en/products/details/network-io/ipu/adapter-e2100.html), [Intel-Google 2026 IPU](https://newsroom.intel.com/data-center/intel-google-deepen-collaboration-to-advance-ai-infrastructure), [AWS EFA](https://docs.aws.amazon.com/us_en/AWSEC2/latest/UserGuide/efa.html), [AWS Project Rainier](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster), [Microsoft Maia 200](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/), [Maia architecture deep dive](https://techcommunity.microsoft.com/blog/azureinfrastructureblog/deep-dive-into-the-maia-200-architecture/4489312) |
| 标准 | [UEC 1.0](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/), [UEC 1.0.2](https://ultraethernet.org/), [UALink specs](https://ualinkconsortium.org/specification/), [UALink roadmap](https://ualinkconsortium.org/blog/ualink-roadmap-insights-accelerating-open-scalable-ai-networking-1296/) |
| 市场数据 | [Crehan server-class Ethernet NIC](https://www.globenewswire.com/news-release/2026/03/09/3251924/0/en/Server-Class-Ethernet-NIC-Revenues-Have-Doubled-in-Just-Two-Years-Reports-Crehan-Research.html), [IDC Ethernet switch](https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/), [IDC semiconductor 2026](https://www.idc.com/resource-center/blog/semiconductor-market-to-surge-past-the-trillion-dollar-threshold-ai-infrastructure-drives-market-growth/), [Deloitte 2026 data center spending](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-telecom-outlooks/hardware-consumer-tech-outlook.html) |
| 新兴公司/配套 | [Marvell-XConn](https://www.marvell.com/company/newsroom/marvell-to-acquire-xconn-technologies-expanding-leadership-in-ai-data-center-connectivity.html), [Marvell-NVIDIA NVLink Fusion](https://www.marvell.com/company/newsroom/nvidia-ai-ecosystem-expands-marvell-joins-forces-through-nvlink-fusion.html), [Astera Scorpio](https://www.asteralabs.com/products/scorpio-smart-fabric-switch/), [Enfabrica ACF-S](https://enfabrica.net/solution/acf-s), [Napatech](https://www.napatech.com/), [Supermicro BlueField-4 STX](https://www.supermicro.com/en/pressreleases/supermicro-among-first-unveil-nvidia-bluefield-4-stx-storage-server-improve-ai) |

非投资建议。本报告有意采用对 2026-2027 AI 计算中心建设非常乐观的情景，并对缺少直接披露的数据做了大胆估算；若 AI CapEx、GPU/HBM/电力交付、客户 ROI 或网络标准成熟度低于预期，实际收入和利润率会显著低于乐观与极超情景。
