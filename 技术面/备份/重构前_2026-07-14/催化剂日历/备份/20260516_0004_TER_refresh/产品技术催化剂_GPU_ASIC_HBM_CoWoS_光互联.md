# 产品技术催化剂：GPU / ASIC / HBM / CoWoS / 光互联 / AI Power

> 研究日期：2026-05-15 美西时间  
> 覆盖范围：Blackwell / GB300 / Rubin、custom ASIC、HBM3E / HBM4、CoWoS / SoIC、800G / 1.6T、CPO / LPO / AEC、retimer / CXL、AI power。  
> 结论属性：产业链与产品节点研究，不构成投资建议。

## 核心结论

2026 年 AI 硬件的主线不是“哪一颗芯片最强”，而是“哪一条系统链路能按期交付”。从项目内资料看，真正可交易的产品催化剂有两层：

1. **2026 现金流主线：GB300 / B300 Blackwell Ultra + HBM3E + CoWoS-L/S + 800G/1.6T + 48V/54V 机柜供电。** 这些已经进入订单、产能和客户认证阶段，是当下收入和毛利的核心。
2. **2027 期权主线：Rubin / Rubin Ultra / Kyber + HBM4/HBM4E + SoIC/混合键合 + CPO/NPO/OCI + PCIe Gen6/7 fabric + 800VDC。** 这些决定下一轮估值上修，但 2026 年仍以 design-in、样机、认证和预订单为主。

一句话判断：**GB300 是 2026 的确定性，Rubin 是 2027 的预期差；HBM 和 CoWoS 是算力交付阀门，1.6T/retimer/AEC 是网络阀门，48V/800V 是上架阀门。** 如果这些阀门同步顺利，NVDA、TSM、MU、AVGO、MRVL、COHR、LITE、CRDO、ALAB、VRT、ETN 等链条仍有基本面上修空间；如果任一阀门延迟，最先受伤的通常不是收入最稳的大票，而是估值里已经提前计入 2027-2028 放量的小型高 beta 公司。

## 技术节点日历与关键指标

| 技术节点 | 2026-2027 时间判断 | 关键指标 | 正面触发 | 负面触发 |
|---|---|---:|---|---|
| Blackwell / GB300 / B300 | 2026 主力交付，2027 上半年仍大量延续 | GB300 NVL72、288GB HBM3E、整柜约 142kW；项目资料引用 TrendForce 判断 Blackwell 在 NVIDIA 高端 GPU 出货占比从 61% 上修至 71% | GB300 集群按期交付、NVDA 数据中心收入和毛利率保持强势、networking attach 上修 | GB300 交付延迟、HBM/CoWoS/液冷/电力任一瓶颈卡住，或客户库存消化 |
| Rubin / Rubin Ultra / Kyber | 2026H2 伙伴可用和小批量，2027 才是主放量 | HBM4、NVLink 6、CX9、Spectrum-6、CPO、800VDC / 1MW rack 路线 | HBM4 多供应商认证完成，Rubin 平台样机与客户 hall 设计冻结 | HBM4 良率、功耗、液冷或 CX9 调校延后，导致 2027 预期下修 |
| Hyperscaler custom ASIC | 2026 从单点 TPU 扩散为多客户多 GW 订单，2027 斜率更大 | AWS Trainium2/3、Google TPU 8t/8i、Microsoft Maia 200、Meta MTIA、OpenAI/Broadcom 10GW | AVGO/MRVL AI revenue guide 上修，多客户多代项目确认，云厂 TCO 叙事兑现 | 客户路线变化、软件迁移失败、HBM/CoWoS 被 GPU 挤占，或 ASIC 被证明只适合窄 workload |
| HBM3E / HBM4 | HBM3E 是 2026 主力；HBM4 是 2026H2-2027 最大弹性 | 项目 HBM 底稿估 2026 HBM 单品收入 $52-65B 基准；HBM3E 约占 2026 出货三分之二；HBM4 2026Q2 验证是核心 | MU / Samsung / SK hynix HBM4 认证、HBM ASP 和毛利率维持高位、客户长期锁量 | HBM4 认证慢、良率不稳、客户压价或非头部客户拿不到 allocation |
| CoWoS / SoIC / 先进封装 | CoWoS-L/S 2026 吃满；SoIC/混合键合更偏 2027 | 项目资料估 TSMC CoWoS 2026 年底月产能约 11.5-14 万片、2027 约 17 万片 | TSMC 先进封装扩产仍供不应求，OSAT 外溢和设备订单上修 | 名义扩产转为过剩预期，或 interposer、ABF、测试、载板卡住有效产出 |
| 800G / 1.6T 光模块 | 800G 是 2026 存量高峰，1.6T 是 2026H2-2027 斜率 | TrendForce 估 800G+ 出货占比 2026 超 60%；Cignal 口径 2026 1.6T 超 500 万只 | 1.6T OSFP / DR8 批量订单、200G/lane EML/SiPh/DSP 缺货、Cisco/Arista/云厂网络订单上修 | 800G/1.6T ASP 快速下滑，客户延后上电，模块库存上升 |
| CPO / NPO / LPO / LRO | 2026 pilot 和小批量，2027 高端 switch 开始商业化 | CPO 主要看 Spectrum-X Photonics、Broadcom Tomahawk 6-Davisson、Open CPX；LRO/TRO 比纯 LPO 更可能先放量 | CPO/NPO 进入 hyperscaler qual，LRO/TRO 在 1.6T 中渗透率提升 | CPO field service 不成熟，纯 LPO 互通失败，标准碎片化导致库存风险 |
| AEC / DAC / retimer / CXL | 2026 retimer/AEC 确定性强，2027 Gen6 fabric switch 和 CXL 池化弹性大 | PCIe 5/6 retimer、1.6T AEC、CXL Type-3 memory、260/320 lane fabric switch | CRDO/ALAB 高增长高毛利延续，Broadcom/Marvell Gen6 产品进入 AI rack BOM | NVIDIA 封闭 NVLink 份额过强压低开放 fabric 弹性，CXL 软件栈成熟慢 |
| AI power：48V/54V 与 800VDC | 48V/54V 是 2026 确定收入；800VDC 是 2027 期权 | GB300 NVL72 约 142kW，8 个 33kW power shelf；800VDC 面向 Rubin Ultra/Kyber 和 1MW rack | 33kW shelf、5.5kW PSU、DC/DC、VRM、eFuse 订单上修；Vertiv/Delta/Schneider/TI/ST 800V 方案 design-in | 800V 安规、保险、AHJ、DC protection 未成熟；数据中心并网和社区许可拖慢上电 |

## 产业链结论：瓶颈决定利润池

AI 产品催化剂的传导顺序是：

GPU/ASIC 平台规格 -> HBM stack allocation -> CoWoS/SoIC 有效产出 -> 服务器/整柜 burn-in -> 800G/1.6T 网络 -> 机柜供电与液冷 -> 数据中心上电 -> 云服务收入确认

这条链的投资含义很直接：**最赚钱的环节通常不是“看起来最大的 BOM”，而是“缺一不可且难以替代的认证瓶颈”。** 2026 年瓶颈仍集中在 HBM3E、CoWoS、1.6T 器件、retimer/AEC、48V power shelf 和电力上电；2027 年若 Rubin、MI400、TPU8、Trainium3/4、OpenAI/Broadcom ASIC 同步放大，瓶颈会向 HBM4、SoIC/混合键合、CPO/NPO、Gen6 fabric switch、800VDC 保护与转换迁移。

## 公司受益与受损映射

这里的“受损”不是简单做空结论，而是指在该技术路径兑现时，相关公司或业务线可能面临相对增长放缓、ASP 压力、份额迁移或估值压缩。

| 技术催化剂 | 核心受益公司 | 第二层受益 | 潜在承压 / 受损 | 传导逻辑 |
|---|---|---|---|---|
| GB300 / Blackwell Ultra 顺利交付 | NVDA、TSM、MU | VRT、ETN、COHR、LITE、ANET、CSCO、CRDO、ALAB、DELL、SMCI | 没有差异化的二线 GPU / AI 加速卡、无法拿到 HBM/CoWoS 的客户 | GB300 放量直接拉动 GPU、HBM、CoWoS、整柜电源、800G/1.6T 和网络 attach |
| Rubin / HBM4 平台前置 | NVDA、TSM、MU、Samsung、SK hynix | KLAC、AMAT、LRCX、TER、FORM、ONTO、CAMT、MPWR、VICR | 只受益 HBM3E 存量、缺 HBM4 认证的供应商；无法跟进液冷/800V 的整机厂 | Rubin 把内存、封装、功耗和网络规格再抬一档，认证领先者获得溢价 |
| Custom ASIC 多 GW 化 | AVGO、MRVL、TSM、SNPS、CDNS | RMBS、ALAB、CRDO、AMKR、ASX、FN、APH、TEL | 只讲“GPU 替代”但缺软件生态的小型 AI 芯片公司；部分 merchant GPU ASP 预期 | ASIC 不一定替代 GPU，但会把增量 CapEx 分散到 Broadcom/Marvell/EDA/IP/HBM/封装/以太网 |
| HBM3E 继续紧、HBM4 认证 | MU、SK hynix、Samsung | AMAT、LRCX、KLAC、TER、FORM、COHU、ONTO、CAMT、RMBS | 云厂和服务器 OEM 毛利；拿不到 allocation 的 AI 芯片客户 | HBM 是高端 xPU 可交付前置条件，价格能向整柜和云服务传导 |
| CoWoS / SoIC 继续瓶颈 | TSM | AMKR、ASX、KLAC、ONTO、CAMT、ASML、AMAT、LRCX、BESI / ASMPT 生态 | 普通 OSAT、低端 fan-out、低差异基板 | 高端 2.5D/3D 封装和测试决定有效产出，客户切换成本高 |
| 800G/1.6T 光模块放量 | COHR、LITE、FN、AAOI、ANET、CSCO、AVGO、MRVL | GLW、APH、TEL、VIAV、KEYS、MTSI、SMTC | 400G/低速模块、纯组装且无器件优势的模块厂 | 800G 做量，1.6T 做斜率，真正高毛利集中在 EML/SiPh/DSP/测试/高密连接 |
| LPO/LRO / CPO / NPO | AVGO、NVDA、COHR、LITE、MRVL、ANET、CSCO | FN、GLW、APH、TEL、POET、LWLG、KEYS、VIAV | 传统 pluggable 模块中低端 ASP；只依靠完整 DSP 模块的供应商 | LRO/TRO 先降功耗，CPO/NPO 后改变交换侧价值分配，利润向 ASIC/光引擎/ELS/连接迁移 |
| AEC / retimer / CXL | CRDO、ALAB、AVGO、MRVL | APH、TEL、Molex/TE 生态、MCHP、RMBS、SNPS、CDNS、MU | 被动低速 DAC、无固件/遥测能力的连接器和线缆厂；CXL 软件栈慢会压制 CXL 纯题材 | AI rack 内短距铜升级，PCIe Gen6/CXL 把 retimer 从信号补偿变成系统级部件 |
| 48V/54V 与 800VDC AI power | VRT、ETN、Schneider、ABB、Delta、MPWR、VICR、IFNNY、ON、STM、TXN | PWR、GEV、HUBB、NVT、APH、TEL、VST、CEG、FLNC | 低密度传统 PSU、没有高压 DC 保护能力的低端电源装配；云厂 CapEx 和折旧压力 | 100kW+ rack 让供电从配套件变为交付约束，800VDC 把价值推向保护、DC/DC、SiC/GaN 和控制软件 |

## 重点技术拆解

### 1. Blackwell / GB300 / Rubin：2026 看交付，2027 看平台迁移

项目内《商用 AI 加速芯片》底稿给出的最重要判断是：2026 年出货和收入最大权重仍在 B300/GB300 Blackwell Ultra，而不是 Rubin。GB300/B300 使用 HBM3E、CoWoS-L/S、NVLink / NVL72 和液冷整柜，直接拉动 HBM、先进封装、power shelf、光互联和整柜测试。Rubin 则把 HBM4、NVLink 6、CX9、Spectrum-6/CPO 和更高功耗平台带入 2027。

对股价的含义：

- **正面：** GB300 数据中心集群公开上线、NVDA 数据中心收入和毛利率稳定、客户没有显著库存消化、networking attach 率继续上修。
- **负面：** GB300 交付被 HBM/CoWoS/液冷/电力卡住，或市场把 Rubin 延迟理解为路线图可信度下降。
- **最容易被重估：** NVDA、TSM、MU 是主线；COHR/LITE/ANET/CSCO/CRDO/ALAB/VRT/ETN 是系统外溢链条。

### 2. Custom ASIC：不是替代 GPU，而是第二条算力产能线

云厂自研 ASIC 的核心变化是从 Google TPU 单点领先，变成 AWS Trainium、Google TPU、Microsoft Maia、Meta MTIA、OpenAI/Broadcom accelerator 和 Broadcom/Marvell custom silicon 同时进入量产或导入窗口。项目内 ASIC 底稿判断，2026 年自研 ASIC 等效市场基准可达 $70B-$110B，2027 基准 $140B-$220B。

这个方向的关键不是“GPU 会不会被替代”，而是 hyperscaler 把高重复、高利用率、高 token 量的推理、推荐、MoE serving、后训练和内部 agent workload 迁移到定制硬件。它给 AVGO/MRVL/TSM/SNPS/CDNS/RMBS 带来长期订单，也给 HBM、CoWoS、SerDes、以太网和光互联制造第二条需求曲线。

### 3. HBM3E / HBM4：2026 现金流在 HBM3E，2027 弹性在 HBM4

HBM 底稿的结论非常明确：2026 年不是 HBM4 全面替代，而是 HBM3E 12Hi 继续统治，同时 HBM4 在 Rubin、MI400、TPU8 和下一代 ASIC 上抢先导入。HBM 单品收入池 2026 基准估算为 $52B-$65B，乐观 $65B-$85B，极度乐观 $85B-$110B；HBM3E 约占 2026 出货三分之二。

需要盯的指标：

| 指标 | 正面解释 | 负面解释 |
|---|---|---|
| HBM4 qualification | MU / Samsung / SK hynix 均能进入 Rubin / MI400 / ASIC 供应链 | 某一家认证延迟导致客户单源风险或 Rubin 节奏下修 |
| HBM ASP 与毛利 | AI 内存仍是紧缺资源，价格能向整柜转嫁 | 扩产过快或客户压价，市场开始交易内存周期顶部 |
| HBM tester / probe / TC bonder 订单 | 2027 HBM4/HBM4E 需求前置 | 设备订单放缓，说明客户对 HBM4 需求或资本开支更谨慎 |

### 4. CoWoS / SoIC：名义产能不等于有效产出

CoWoS 是 GPU 和 ASIC 共用瓶颈。项目内先进封装底稿估算，AI 2.5D 封装未来 12 个月收入池基准 $34B-$48B，乐观 $45B-$65B；高端数据中心 GPU/ASIC 先进封装渗透率 2026 已高于 85%。但实际产出取决于 interposer、RDL、HBM KGD、ABF 载板、测试、热翘曲和系统级 burn-in，任何一项不足都会让名义产能打折。

2026 最确定的是 CoWoS-L/S 和 HBM3E 封装；2027 的期权是 SoIC、混合键合、EMIB-T、I-Cube/X-Cube、CoPoS/玻璃基板和 photonic interposer。TSM 的定价权最强，AMKR/ASX/ASE 等 OSAT 能承接外溢但议价弱于 TSM；KLAC/ONTO/CAMT/TER/FORM 等测试量测和探针卡链条在“隐形瓶颈”中更有弹性。

### 5. 800G / 1.6T / CPO / LPO / AEC：网络从 GPU 附属品变成第二约束

800G/1.6T 底稿给出的主线是：2026 是 800G 高峰年，也是 1.6T 从验证转向规模交付的第一年。TrendForce 估 AI 专用光收发模块市场 2026 达 $26B，同比 +57% 以上；800G 及以上模块出货占比从 2024 年 19.5% 升至 2026 年 60%+。Cignal 口径下，2026 年 1.6T 出货超过 500 万只。

不同路线的结论要分清：

| 路线 | 2026 判断 | 受益层 |
|---|---|---|
| 800G pluggable | 仍是实际收入主体，但 ASP 压力开始上升 | 模块、光器件、交换系统 |
| 1.6T pluggable | 最强新增斜率，2026H2-2027 进入主流 | COHR、LITE、FN、AAOI、AVGO、MRVL、测试设备 |
| LRO/TRO | 比纯 LPO 更容易在 2026-2027 放量 | 低功耗 DSP、TIA/driver、EML/SiPh、客户调参能力 |
| 纯 LPO | 期权更大，但对 host SerDes、FEC、互通和测试要求更高 | Broadcom、NVIDIA、Marvell、Cisco 等 host ASIC / switch 侧 |
| CPO/NPO/CPX | 2026 以 pilot、ELS、optical engine 和资格认证为主，2027 看高端 switch | switch ASIC、laser/ELS、光引擎、连接器、测试 |
| AEC/ACC/DAC | 短距铜不会消失，1.6T/224G 让 AEC/ACC 价值提升 | CRDO、APH、TEL、Molex/TE 生态、Broadcom、Marvell |

### 6. Retimer / CXL：开放 AI rack 的高毛利小核心

PCIe/CXL retimer 底稿认为，Retimer 是 2026 确定性单品，Fabric Switch 是 2027 最大弹性品类，CXL 则从“技术正确”走向“商业压力正确”。原因是 HBM 和 DDR5 都贵，长上下文和 KV cache 推高内存占用，云厂愿意用 CXL 扩展和池化降低闲置资本。

关键公司是 ALAB、CRDO、AVGO、MRVL、MCHP、RMBS、SNPS、CDNS、Montage 等。需要注意反面情景：如果新增 AI CapEx 绝大部分继续进入 NVIDIA 封闭 NVLink 域，开放 PCIe/CXL fabric switch 的斜率会推迟，但 retimer、AEC、SCM 和周边 I/O 仍会受益。

### 7. AI Power：2026 是 48V/54V，2027 看 800VDC

机柜级供电底稿的核心判断是：2026 年确定性最高的不是 800VDC，而是 48V/50V/54V ORv3/MGX power shelf 大规模放量。GB300 NVL72 约 142kW，8 个 33kW power shelf，每个 power shelf 含 6 个 5.5kW PSU。800VDC 是 2027 年随 Rubin Ultra/Kyber 和 1MW rack 路线推进的增量期权。

对公司映射：

- **最确定现金流：** VRT、ETN、Schneider、ABB、Delta、Flex、Lite-On、Dell/ODM 链条。
- **高毛利部件：** MPWR、VICR、IFNNY、ON、STM、TXN、ADI、Renesas、MCHP 等 DC/DC、VRM、eFuse、GaN/SiC、控制器。
- **长期期权：** 800VDC sidecar、MVSST、DC breaker、power orchestration、supercap/CBU、BESS。
- **最大风险：** 800VDC 安规和认证慢于预期，且数据中心项目被变压器、并网、社区许可和电价政治拖慢。

## 5/15 市场状态：技术催化剂需要和拥挤度一起看

common daily 面板显示，2026-05-15 当天半导体高 beta 明显回撤，但中期涨幅仍很大：

| 指标 | 2026-05-15 状态 |
|---|---:|
| QQQ | 1 日 -1.5%，21 日 +10.7%，距 252 日高点 -1.5% |
| SOXX | 1 日 -4.1%，21 日 +25.3%，63 日 +43.5%，252 日 +138.3%，距 252 日高点 -4.5% |
| SMH | 1 日 -3.8%，21 日 +22.3%，63 日 +36.5%，252 日 +125.0%，距 252 日高点 -3.8% |
| NVDA | 1 日 -4.4%，5 日 +4.7%，21 日 +13.6%，252 日 +66.5%，距 252 日高点 -4.4% |

这意味着产品催化剂对股价的作用会更二元：**强确认可以消化高估值，弱确认会放大回撤。** 在这种市场位置上，应该把“发布会叙事”与“收入确认、毛利率、客户认证、产能和上电”分开看。

## 正面触发清单

1. **NVDA / 供应链确认 GB300 按期交付。** 重点看 GB300 NVL72 大客户集群、数据中心收入、毛利率、networking attach。
2. **HBM4 多供应商认证完成。** MU、Samsung、SK hynix 的 HBM4 / 16Hi / HBM4E 进度决定 Rubin/MI400/TPU8 斜率。
3. **TSM CoWoS / SoIC 继续供不应求。** 如果扩产仍被客户预付款锁满，TSM 及设备、测试、载板链条继续有定价权。
4. **AVGO / MRVL custom ASIC 从单客户变多客户多代。** OpenAI、Meta、Google、Microsoft、AWS 相关信号越具体，ASIC 链条越能重估。
5. **1.6T 与 AI network 订单继续上修。** Cisco hyperscaler AI 订单上修、Acacia optics、Coherent/Lumentum 1.6T ramp、CRDO AEC 增速都是强验证。
6. **CPO/NPO 从展示进入客户 qual。** NVIDIA Spectrum-X Photonics、Broadcom Tomahawk 6 CPO、Open CPX、Coherent socketed CPO 的客户进度是 2027 期权。
7. **48V/800V 电源从参考设计变成订单。** Vertiv/Delta/Schneider/Eaton/TI/ST/Infineon 披露 design-in、AVL、样机、量产时间表。

## 反面触发清单

1. **Rubin / HBM4 延迟被确认。** 如果 2027 平台因为 HBM4、功耗、液冷或 CX9 调校延后，HBM4、SoIC、800V、CPO 期权会被压缩。
2. **光模块 ASP 下行快于出货增长。** 800G/1.6T 多供扩散后，纯模块厂收入增长可能无法转化为利润增长。
3. **CoWoS 从瓶颈转为供给松动。** 名义扩产一旦被市场理解为过剩，先进封装外溢链条估值会先承压。
4. **云厂 CapEx 或上电进度放缓。** 电力、社区许可、并网、变压器和施工人力会把硬件订单变成延期收入。
5. **Custom ASIC 软件迁移慢。** ASIC 硬件可用但模型、编译器、调度和 goodput 不达标，会让 AVGO/MRVL 的远期乐观预期打折。
6. **NVIDIA 封闭生态继续扩大份额。** 这不一定伤害 NVDA，但会推迟开放 PCIe/CXL/UALink fabric switch 的弹性。
7. **客户集中风险暴露。** CRDO、ALAB、AAOI、LITE、COHR、部分 OSAT 或测试设备公司若被发现单一客户/单一 SKU 占比过高，估值容错会下降。

## 风险

| 风险 | 影响 |
|---|---|
| 时间错配 | 很多 2027 技术在 2026 只有样品、NRE、design-in 和预订单，收入确认可能晚于股价交易 |
| 估值拥挤 | SOXX/SMH/NVDA 已有大幅中期涨幅，弱验证会导致高 beta 链条先回撤 |
| 技术路线分叉 | LPO、CPO、NPO、XPO、OCI、AEC、retimer、CXL 并行推进，押单一路线容易遇到库存和研发错配 |
| 供给扩张 | HBM、CoWoS、1.6T、AEC 若扩产速度超过上电速度，ASP 和毛利会先被压 |
| 客户集中 | 多数 AI 硬件链条由少数 hyperscaler 和 NVIDIA 生态决定，客户节奏变化会放大季度波动 |
| 政策与地缘 | H200 中国许可僵局说明，批准、采购、交付和当地审查可能互相冲突 |
| 电力与社会许可 | 数据中心项目受变压器、并网、社区反对、许可和电价外部性制约，可能慢于硬件出货 |

## 后续跟踪框架

| 跟踪频率 | 要看什么 | 关键公司 / 来源 |
|---|---|---|
| 每周 | 最新 AI 产业链新闻、客户订单、政策/出口管制、数据中心上电进展 | 最新AI新闻、NVDA、CSCO、云厂、Reuters/TrendForce |
| 每月 | HBM4 认证、CoWoS 扩产、1.6T 订单和 ASP、AEC/retimer design-in | MU、TSM、COHR、LITE、CRDO、ALAB、AVGO、MRVL |
| 每季 | 财报中的 AI revenue、毛利率、CapEx、库存、客户集中度 | NVDA、AVGO、MRVL、MU、TSM、ANET、CSCO、VRT、ETN |
| 半年 | Rubin / MI400 / TPU8 / Trainium3 / Maia / MTIA 平台是否如期 | NVIDIA GTC/OCP/OFC/DesignCon、云厂发布 |
| 2027 重点 | CPO/NPO 商业化、HBM4E/cHBM、SoIC、800VDC、Gen6 fabric switch | NVDA、AVGO、MRVL、TSM、MU、VRT、Schneider、Delta、ALAB |

## 资料来源

主要读取和交叉参考了以下项目内资料：

- 催化剂日历/备份/20260515_143349/产品技术催化剂_GPU_ASIC_HBM_CoWoS_光互联.md
- AI产业和股票研究结果/行业调研_AI服务器_存储_芯片/行业调研_商用AI加速芯片_2026.md
- AI产业和股票研究结果/行业调研_AI服务器_存储_芯片/行业调研_云厂自研AI_ASIC_2026.md
- AI产业和股票研究结果/行业调研_AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026.md
- AI产业和股票研究结果/行业调研_AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026.md
- AI产业和股票研究结果/行业调研_晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-05-08.md
- AI产业和股票研究结果/行业调研_AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-05-08.md
- AI产业和股票研究结果/行业调研_AI网络_光互联_铜互联/行业调研_LPO_LRO线性光模块_2026-05-08.md
- AI产业和股票研究结果/行业调研_AI网络_光互联_铜互联/行业调研_CPO_NPO与交换侧光引擎_2026-05-08.md
- AI产业和股票研究结果/行业调研_AI网络_光互联_铜互联/行业调研_AEC_DAC与高速铜缆_2026.md
- AI产业和股票研究结果/行业调研_AI网络_光互联_铜互联/行业调研_PCIe_CXL高速IO交换与Retimer_2026-05-08.md
- AI产业和股票研究结果/行业调研_AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026.md
- AI产业和股票研究结果/行业调研_AI园区电力_机电_冷却/行业调研_中压直流_800VDC与固态变压器_2026-05-08.md
- AI产业和股票研究结果/AI产业链信息/最新AI新闻/每日AI产业链新闻_2026-05-15.md
- AI产业和股票研究结果/AI产业链信息/最新AI新闻/每日AI产业链新闻_2026-05-15_补充更新.md
- 股票基本面和价格历史研究/data/common_daily/features/common_research_daily_panel_full.csv

