# 2026 IEEE VLSI Symposium 会议追踪：核心变化、产品爆发和市场预期差

会议日期：2026-06-14 至 2026-06-18  
会议地点：Hilton Hawaiian Village, Honolulu, Hawaii, USA  
材料检索截止日期：2026-06-20  
报告完成日期：2026-06-20  
研究边界：本稿按会议驱动的阶段性底稿处理，未读取、引用或继承项目内旧报告、索引、缓存和中间结论。证据来自会议官网、官方 program、官方 technical tipsheet、会议在线议程、公司公开材料和公开市场研究资料。  

## 结论摘要

本届 VLSI 2026 的主题名义上是“Advancing the AI Frontier through VLSI Innovation”，但真正的产业信号不是“AI 芯片更快”这么简单，而是 AI/HPC 的瓶颈已经从单个 compute die 的晶体管密度，扩展到背面供电、片上/封装内供电、HBM/DRAM 架构、2.5D/3D 封装、光互连、热管理、良率 ramp 和 EDA/制造协同。对股票研究最重要的变化是：利润池继续向能把复杂系统量产出来的节点、封装、存储、设备、材料、EDA 和测试环节集中，而不是平均扩散到所有“半导体 AI 概念”公司。

最可投资的 12 个月方向排序：

1. **先进制程 + 背面供电进入商业验证期**。TSMC A16 在 VLSI online session 中披露已开发并 qualified，较 N2P 提供 8%-10% 同功耗提速、15%-20% 同速降功耗、8%-10% 额外芯片密度提升，并称 Q4'26 量产；Intel 18A-P 于 2026-06-16 官宣进入 risk production，较 18A 提供 9% 同功耗性能提升或 18% 同性能降功耗。TSMC 的收入弹性更靠近 2027 高端 AI/HPC tapeout；Intel 的投资弹性更大，但反证条件也更直接：外部客户、良率、交付和 Foundry 损益。
2. **HBM/DRAM 的近端利润池仍大于远期 3D DRAM 科研热度**。会议上 Samsung 16-tier VS-DRAM、SK hynix 4F2 VG DRAM、Kioxia/SanDisk >1,000 WL 3D Flash、SAIMEMORY/Intel/PSMC/AP 9-layer 3D high-bandwidth DRAM 都指向存储架构纵向化，但 2026-2027 真正放量仍是 HBM3E/HBM4、TSV、混合键合、测试和良率。TrendForce 2025-05-09 指出 2026 HBM shipment 将超过 30B Gb，HBM4 价格 premium 预计超过 30%。
3. **CoWoS/2.5D 短缺交易可能从“缺口扩大”转向“缺口收窄但需求升级”**。TrendForce 2026-06-15 引述机构口径称 CoWoS 供需缺口可能从当前约 20% 缩小到 2026 年底约 10%，TSMC 月产能 2026 年可能达 120k-140k wafers，含 OSAT 新增后行业总能力接近 200k wafers/month。结论不是看空先进封装，而是利润池将从简单扩产转向大 reticle、SoIC、hybrid bonding、热/电源完整性、光引擎和测试。
4. **CFET/3D stacked FET 是远期路线，不是 2026 收入因子**。Samsung 42nm gate pitch triple-stacked nanosheet 3DSFET、Intel 45nm gate pitch CFET inverter 是重要路线图信号，但更像 2029+ 节点前置研发；对 2026-2027 财务影响主要通过设备、材料、工艺协同和 foundry 技术叙事。
5. **EDA/制造 AI 从“生成式设计故事”落到良率和诊断 ROI**。会议 W6 和 circuits short course 明确把 AI/ML 用于 defect reduction、virtual process emulation、memory development、floorplanning、diagnosis、DMCO 和 agentic EDA。这里的投资弹性比“AI 自动设计芯片”的叙事更实在：EDA 软件、emulation、DFT/diagnosis、process control、yield analytics 和制造虚拟化。
6. **市场对 AI 需求已经很乐观，但对非 AI 被挤出的副作用可能低估**。Gartner 2026-04-08 预测 2026 全球半导体收入 $1.320T、同比 +64%，其中 memory $633.3B，AI 半导体约占总收入 30%；WSTS Spring 2026 口径更激进，预测 2026 市场 $1.51T、memory >$800B。两个权威口径都说明 AI/memory 已不是反共识，反共识在于：非 AI、消费、汽车、工业的成本压力、交期挤压和毛利再分配。

一句话判断：VLSI 2026 把 2026-2027 的核心矛盾压缩成“AI 系统 PPAC 的量产约束”。受益弹性由高到低是：先进 foundry/先进封装/HBM 和 DRAM 设备材料/EDA 与良率工具/高端测试与热电源组件；单纯跟随会议热点但没有量产入口的公司应降权。

## 会议重点和方向变化

### 1. 十个核心主题、对应公司和证据等级

| 主题 | 会议证据 | 关键公司/机构 | 关键参数 | 客户需求 | 成熟度 | 投资判断 |
|---|---|---|---|---|---|---|
| GAA + backside power delivery 商业化 | TSMC A16 late news、Intel 18A-P、T2 Backside Power Delivery | TSMC、Intel、Samsung、IBM、imec、ASM | A16 vs N2P：+8%-10% speed、-15%-20% power、+8%-10% density、Q4'26 mass production；18A-P vs 18A：+9% iso-power perf 或 -18% iso-perf power | AI/HPC dense routing、IR drop、低压频率、功耗墙 | TSMC：量产前夕；Intel：risk production；Samsung/IBM/imec：研发/DTCO | 2026-2027 最重要主线，但收入确认滞后于技术发布 |
| CFET/3DSFET 纵向逻辑 | Samsung T1.1、Intel T5.2、IBM T5.4 | Samsung、Intel、IBM | Samsung 3DSFET：42nm gate pitch、triple nanosheet；Intel CFET：45nm gate pitch、PowerVia、DBC、MDI <10nm；IBM SiGe PFET >900C、SS约70mV/dec | 2nm 后继续密度提升 | 实验/研发 | 远期大方向，2026 股票催化更多是设备材料叙事 |
| DRAM/HBM 架构纵向化 | W5、T5.1、T8.5、T17.5、T18 | Samsung、SK hynix、Micron、NVIDIA、AMD、imec、SAIMEMORY、Intel、PSMC、Kioxia/SanDisk | Samsung 16-tier VS-DRAM；SK hynix 4F2 VG DRAM；SAIMEMORY 9-layer、3um Si/stack、~0.25Tb/s/mm2；Kioxia/SanDisk >1,000 WL 3D Flash | AI bandwidth、power、HBM capacity、DRAM scaling beyond 10nm | HBM4：近端；3D DRAM：中远期 | 近端看 HBM4、TSV、bonding、测试；远端看 4F2/VS-DRAM |
| Advanced packaging/3D integration | W3、SCT3、T17、TSMC 2026 Tech Symposium | TSMC、AMD、NVIDIA、Samsung、Intel、Murata、Dexerials、Panasonic、imec | TSMC 5.5-reticle CoWoS 已量产；14-reticle CoWoS 2028；COUPE on substrate 2026、2x power efficiency、10x latency；T17.1 face-down CoW bumpless interconnect | AI package size、HBM stacks、thermal、latency | 近端量产扩容 + 远端新架构 | 2026 仍高景气，但 capacity gap 收窄会改变交易逻辑 |
| Silicon photonics / electronic-photonic co-design | W3、C20、TSMC COUPE | NVIDIA、TSMC、Intel、AMD、Synopsys、Samsung、Ghent | NVIDIA C20.2：32Gb/s optical receiver、0.484pJ/b、-17.3dBm sensitivity、7nm EIC + 65nm SiPh PIC Cu-Cu hybrid bonding；TSMC COUPE 200Gbps micro-ring | rack-to-rack、scale-out、latency/power | 2026 开始 package 内光引擎生产，CPO 仍爬坡 | 中期强，但 2026 收入主力仍是可插拔和传统交换链 |
| Power delivery / thermal / telemetry | C2、C10.5、JFS6、T2 | Intel、TSMC、Samsung、AMD、Sony、设备/材料商 | Intel SCVR：20W/mm2、4.8V input、94.8% peak efficiency；Intel TV sensor：spacing <216um、3.1C/2.1mV in 18A、1.9C/1.3mV in Intel 3、DNN latency -24% | dense 3D AI processors、per-core throttling、vertical PDN | 近端可进入产品 | 低估方向：电源完整性、硅电容、封装电感、热传感/控制 |
| SRAM/embedded memory/CIM | W2、C8、C21、C29、T18 | TSMC、MediaTek、Intel、NVIDIA、IBM、NXP、RAAAM、imec | TSMC 2nm DCIM：234.4 TOPS/W、511.9 TOPS/mm2、VMIN <0.38V；TSMC 2nm SRAM：37.42Mbit/mm2、0.35-1.10V、2.28pJ/access；MediaTek 3nm TinyNPU：1.47 TOPS、256KB、smart glasses up to 10 days battery | edge inference、wearables、on-chip bandwidth | Edge/SoC 更近，datacenter 仍受软件和精度限制 | 不宜直接外推到大模型训练；更像端侧 AI 和 SRAM scaling 解法 |
| Process/materials for AI nodes | SCT4、T3、T6/T7、T13/T15 | Applied Materials、ASML、Lam、KLA、ASM、imec、IBM、Samsung | AMAT short course 强调 HAR capacitor etch、higher-k/lower-leakage films、wafer bonding/thinning、channel/contact/interconnect、CFET；imec 2D EUV：50nm contact pitch、75nm active width、EOT约2nm | 2nm 以下良率、RC delay、DRAM scaling | 设备/材料环节最接近订单 | 设备材料仍是高确定利润池，尤其 deposition/etch/metrology |
| AI for EDA/yield/manufacturing | W6、SCC | Lam、SK hynix、Micron、Winbond、imec、TSMC、MediaTek、Siemens、Rapidus、CMU | TSMC memory AI：IP productivity at least 2x annually；W6 聚焦 defect reduction、virtual process emulation、causal modeling、yield ramp；Rapidus Raads agentic design | shorten TTM、yield ramp、diagnosis、complex DRC | 正在导入 | 比“自动设计芯片”更可靠，收入落在 EDA、emulation、yield analytics |
| Cryo-CMOS / quantum | W1、W4、JFS1 | imec、IBM、CEA-Leti、Diraq、Quobly、Hitachi、SemiQon、Quantum Motion | sub-1K circuits、spin qubit 300mm platform、surface-code decoder 20.8ns at 4K | quantum scaling | 远期 | 2026 股票研究中只做 optionality，不应作为核心盈利假设 |

### 2. 相比过去 6-12 个月预期的变化

**变化一：背面供电从“路线图词汇”变成商业节点差异。** 2024-2025 市场已经知道 GAA/BSPDN 是 2nm 后主线，但 VLSI 2026 增量在于 TSMC A16 和 Intel 18A-P 都给出硅片/节点级指标。TSMC 的 Super Power Rail 直接把 A16 绑定 AI/HPC dense routing；Intel 则强调 18A-P risk production、Power Boost、20%-40% thermal resistance 改善、10%-30% via resistance 改善和 design-rule compatibility。市场原来更关注“谁先有 GAA”，现在应改看“谁能把 GAA+BSPD+PDK+IP+封装+良率组合成量产客户产品”。

**变化二：DRAM 的未来不再只靠 HBM stacking，而是 cell architecture 也进入拐点。** W5 把 Qualcomm、NVIDIA、AMD、imec、SK hynix、Micron 拉到同一个 DRAM/AI workshop；Samsung 16-tier VS-DRAM 和 SK hynix 4F2 VG DRAM说明，DRAM 厂已经把 10nm 后 scaling 从“继续 shrink 6F2”转向 4F2、vertical gate、wafer bonding、peri-on-cell 和 3D DRAM。投资上不能把这理解为 2026 立刻替代 HBM，而应理解为未来 2-5 年 DRAM capex 的结构变化：etch/deposition/bonding/thinning/metrology/test 的强度上升。

**变化三：CoWoS 缺口叙事进入第二阶段。** 2024-2025 的主线是“CoWoS 不够”，2026 年会后要跟踪“缺口收窄后，谁拥有下一代集成能力”。TrendForce 2026-06-15 的口径显示，行业可能在 2026 年底接近 200k wafers/month 能力，缺口从 20% 缩到 10%。若属实，简单 capacity scarcity 的估值溢价会下降；但大 reticle、SoIC、hybrid bonding、thermal/power integrity 和 CPO 会接棒成为新瓶颈。

**变化四：EDA/制造 AI 的真实 ROI 更偏制造和验证，不是科幻式自动 tapeout。** SCC 和 W6 显示 AI 已用于 memory development、floor planning、diagnosis、defect reduction、virtual process emulation 和 DMCO。VLSI 2026 的反共识是：AI 先提升工程 productivity 和良率学习速度，而不是立刻替代高端芯片设计团队。

**变化五：市场对 AI/memory 总量已经极度乐观。** Gartner 2026-04-08 给出 $1.320T 半导体市场、memory $633.3B、AI semis 约 30% 总收入；WSTS Spring 2026 甚至给出 $1.51T 和 memory >$800B。会议增量不是“AI 需求很强”，而是哪些环节会卡住 $1.3T-$1.5T 的兑现：先进封装、HBM4 qualification、DRAM EUV/TSV/bonding、2nm 良率、thermal/power integrity、EDA signoff 和测试。

### 3. 三个时间窗口的行业判断变化

| 时间窗口 | 会前主线 | VLSI 2026 后的更新 | 该跟踪的数据 |
|---|---|---|---|
| 未来 3 个月 | A16/18A-P 发布、HBM4 ramp、CoWoS 紧缺 | 重点不是 headline PPA，而是 PDK/IP/design win、HBM4 qualification、CoWoS gap 是否继续缩小 | TSMC A16/N2P tapeout 数；Intel 18A-P 外部客户；SK hynix/Samsung/Micron HBM4 认证；CoWoS 月产能和交期 |
| 未来 1 年 | AI accelerator 与 HBM 高景气 | 2027 产品节奏开始由 A16/18A-P、HBM4、CoWoS-L/SoIC、power/thermal 共同决定 | 2026Q4 A16 量产是否兑现；18A-P yield；Rubin/Feynman/ASIC 节点选择；HBM4 ASP premium 是否>30% |
| 未来 2 年 | 2nm/GAA、先进封装扩张 | 进入 3D DRAM、CFET、CPO/COUPE、14-reticle CoWoS、agentic EDA 工业化验证 | 3D DRAM pilot、CFET CPP/gate pitch/yield、TSMC 14-reticle CoWoS 2028 进度、COUPE 客户、EDA agent 续费和 signoff 认可 |

## 产品和技术路线三情景预测

以下三情景不是股价预测，而是“技术路线-产业放量-利润池”的可证伪框架。市场规模为美元口径，除特别说明外为 2026 年材料检索日可得公开资料和本稿估算。

### 1. A16 / 18A-P / 2nm GAA + backside power

**当前状态。** TSMC A16：VLSI T1.5 称 A16 已 developed and qualified，较 N2P +8%-10% speed 或 -15%-20% power，+8%-10% density，AI/HPC dense routing 适用，Q4'26 mass production。Intel 18A-P：2026-06-16 Intel 官宣 risk production，较 18A +9% iso-power performance 或 -18% iso-performance power，20%-40% thermal resistance 改善，10%-30% via resistance 改善，design rule compatible with 18A。

| 情景 | 2026-2027 路径 | 市场规模/利润池 | 爆发力度 |
|---|---|---|---|
| 务实 | 2026 年主收入仍由 N3/N2/N2P 与 Intel 内部 18A 承担；A16 Q4'26 少量量产/客户验证；18A-P risk production 转入客户评估 | Gartner 2026 nonmemory semis $686.9B；AI semis 约 $396B。先进 foundry wafer service 可投资口径估算 $140B-$190B，其中 A16/18A-P 2026 收入占比小 | 中：技术强，财务滞后 |
| 乐观 | A16 获得 2027 AI/HPC 旗舰 GPU/ASIC；18A-P 获得至少一个外部锚定客户或高价值 test vehicle；EDA/IP ecosystem 快速完善 | 2027 leading-edge foundry 和 advanced packaging 合计增量 $30B-$60B；TSMC 维持 60%+ gross margin；Intel Foundry 亏损收窄但仍需量产验证 | 高：对 TSMC、ASML/AMAT/Lam/KLA/EDA 有直接订单含义 |
| 极度乐观 | Backside power 成为高端 AI/HPC 必选，A16/18A-P 同时带来 higher wafer ASP、更多 advanced packaging attach 和更高 IP/tool spend | 2027-2028 AI semis 若接近 $500B-$600B，高端节点+封装可捕获 $100B+ 服务收入；但外部客户集中度风险高 | 很高，但依赖客户 tapeout 和良率 |

**反证条件。** A16 mass production 从 Q4'26 后移；N2P 已足够好导致 A16 初期 adoption 低；Intel 18A-P 无外部大客户、yield 不达标或 PDK/IP 生态不足；AI accelerator 预算被 memory/packaging 成本挤压。

### 2. HBM4、4F2/VS-DRAM、3D high-bandwidth memory

**当前状态。** VLSI W5 明确把 AI bandwidth/power/scalability 作为 DRAM 方向；Samsung 展示 16-tier VS-DRAM，SK hynix 展示 4F2 VG DRAM，SAIMEMORY/Intel/PSMC/AP 展示 9-layer 3D high-bandwidth DRAM，Kioxia/SanDisk 展示 multi-stacked 3D Flash beyond 1,000 WL。TrendForce 2025-05-09 指出 HBM4 I/O channels doubled to 2048，HBM4 price premium >30%，2026 HBM shipment >30B Gb，SK hynix 预计维持 >50% share。

| 情景 | 2026-2027 路径 | 市场规模/利润池 | 爆发力度 |
|---|---|---|---|
| 务实 | HBM3E 仍主力，HBM4 2026 出货/认证但 2H26 才 ramp；4F2/VS-DRAM 仍为研发/试产 | 本稿按 TrendForce >30B Gb shipments 与 $1.2-$2.0/Gb HBM ASP 估算 2026 HBM revenue $36B-$60B；Gartner memory total $633.3B，WSTS memory >$800B | 高：HBM 是近端利润池 |
| 乐观 | HBM4 premium >30% 保持，Samsung 认证改善，Micron TSV 和先进封装扩张；DRAM equipment 2026 同比 +15.1% | HBM revenue 2027 可上 $60B-$90B；DRAM equipment 2026 约 $25.9B、2027 约 $27.9B；HBM gross margin 维持显著高于 commodity DRAM | 很高：存储厂、TSV/bonding/test、EUV/etch/deposition 受益 |
| 极度乐观 | HBM4/4E 与 custom ASIC 同步大放量，HBM supply 仍紧，4F2/VS-DRAM pilot 提前 | HBM+先进 DRAM 相关 capex 和材料订单进入 2 年超级周期；2027 memory 仍 $700B+ | 很高，但最容易受价格周期反转影响 |

**反证条件。** HBM4 I/O upgrade 延误 qualification；CSP 自研 ASIC 放量低于预期；DRAM/NAND price relief 早于 Gartner 预期；Samsung/Micron yield 追上导致 HBM premium 下滑；先进封装供给改善快于 demand。

### 3. CoWoS、SoIC、hybrid bonding、large-reticle package

**当前状态。** TSMC 2026 技术论坛披露 5.5-reticle CoWoS 已在生产，14-reticle CoWoS 计划 2028，A14-to-A14 SoIC 2029，COUPE on substrate 2026。TrendForce 2026-06-15 指出 TSMC CoWoS 2026 月产能可能 120k-140k wafers，加 OSAT 总行业能力接近 200k wafers/month，供需缺口可能从当前约 20% 收窄到年末约 10%。

| 情景 | 2026-2027 路径 | 市场规模/利润池 | 爆发力度 |
|---|---|---|---|
| 务实 | 2026 继续扩 CoWoS-S/L/R 与 OSAT capacity；缺口收窄但交期仍紧 | 以 200k wafers/month、90% utilization、$8k-$15k/wafer-equivalent service ASP 估算，2026 industry AI advanced packaging service revenue $17B-$32B；高端 package ASP 上移可到 $35B+ | 高但已部分共识 |
| 乐观 | Rubin/ASIC/Feynman 等平台推动更大 interposer、更多 HBM stacks、SoIC attach；thermal/power/test 成为新瓶颈 | TSMC advanced packaging/3D silicon stacking 与 OSAT 高端封装收入 2027 增长 40%+；设备材料和 test handler 订单同步 | 很高 |
| 极度乐观 | 14-reticle、CoPoS、SoIC 和 CPO 形成新平台，AI package 由单产品扩成系统级集成 | 2028 前后大 package 单价和毛利率双升，但 2026 不应提前资本化过满 | 远期高，短期中 |

**反证条件。** CoWoS capacity gap 比预期更快消失；AI accelerator demand 被 power/cooling 或 CSP capex 约束；panel-level 或 OSAT 替代方案压低 TSMC/核心供应商溢价；大 package 良率/翘曲/热失败。

### 4. Silicon photonics / CPO / optical I/O

**当前状态。** W3 主题是 electronic-photonic co-design，参与者包括 Intel、Synopsys、AMD、Ghent、Samsung。NVIDIA C20.2 披露 32Gb/s optical receiver，0.484pJ/b，-17.3dBm sensitivity，7nm FinFET EIC stacked on 65nm SiPh PIC via Cu-Cu hybrid bonding。TSMC 2026 技术论坛称 COUPE on substrate 2026 production，200Gbps micro-ring modulator，较 board pluggable 方案 2x power efficiency、10x latency reduction。

| 情景 | 2026-2027 路径 | 市场规模/利润池 | 爆发力度 |
|---|---|---|---|
| 务实 | 光互连仍以 800G/1.6T pluggable、linear-drive、DSP/driver/TIA 升级为主；CPO/COUPE 先进入少量高端客户 | 2026 数据中心光互连链条可投资口径估算 $25B-$40B；SiPh/CPO 真正 package 内收入占比仍低 | 中 |
| 乐观 | 1.6T 和 3.2T 路线提前，CPO 在 switch/GPU pod 内开始被大客户验证 | CPO/SiPh/TIA/driver/DSP/laser/packaging 2027 增量 $5B-$10B | 高，但客户集中 |
| 极度乐观 | 光 I/O 从 rack-to-rack 进入 package-to-package，电互连 power wall 快速迫使架构迁移 | 2028+ 可形成 $20B+ 新市场，但 2026 证据仍偏 early production / demos | 远期高 |

**反证条件。** pluggable 继续通过 LPO/LRO 和 copper 改进延寿；CPO 可维修性、热、laser reliability 和供应链责任边界难解；GPU/ASIC 厂商不愿锁定单一封装生态。

### 5. Embedded memory、DCIM、端侧 AI NPU

**当前状态。** TSMC C8.1 2nm DCIM compiler 披露 234.4 TOPS/W、511.9 TOPS/mm2、VMIN <0.38V；C29.1 2nm dual-rail SRAM 披露 37.42Mbit/mm2、0.35-1.10V、125C、2.28pJ/access；MediaTek C21.1 TinyNPU 披露 3nm、1.47TOPS、512 8-bit MAC、256KB on-chip memory、smart glasses up to 10 days battery、transformer energy 31.8x lower than prior works。T18.1/T18.2 还展示 RRAM/IGZO/Si/CNT M3D 方向。

| 情景 | 2026-2027 路径 | 市场规模/利润池 | 爆发力度 |
|---|---|---|---|
| 务实 | DCIM 先用于 edge/wearables/sensor SoC，datacenter 训练仍由 GPU/ASIC+HBM 主导 | 端侧 AI SoC/NPU IP 和 embedded memory compiler 2026 可投资口径 $8B-$15B；EDA/IP、foundry SRAM compiler 捕获较多价值 | 中 |
| 乐观 | Always-on reasoning、AI glasses、机器人 sensor hub 推动 3nm/2nm low-power NPU 放量 | 2027 端侧 AI silicon 增量 $10B-$25B；MediaTek、Qualcomm、Apple/Android SoC 供应链受益 | 高，但消费产品周期风险大 |
| 极度乐观 | DCIM 成为推理主流补充结构，SRAM scaling 瓶颈被 compiler/assist circuits 缓解 | 2028 后 IP 和 advanced-node SRAM/compiler 价值显著提高 | 中高，需软件生态证伪 |

**反证条件。** 端侧 AI 用户需求低于预期；模型小型化不足；DCIM 精度、compiler、良率和测试成本抵消能效优势；wearables 出货不支撑 3nm 成本。

### 6. AI for EDA、yield ramp、manufacturing virtualization

**当前状态。** W6 由 Lam Research 组织，覆盖 AI/ML + physics-based process modeling、AI assisted memory development、virtual manufacturing、high-density 3D interconnect manufacturability、frontend virtual modeling。SCC 包括 analog EDA 的 ChatGPT moment、TSMC memory AI、MediaTek floorplanning、CMU diagnosis、Rapidus DMCO/Raads、Siemens Agent AI in EDA。

| 情景 | 2026-2027 路径 | 市场规模/利润池 | 爆发力度 |
|---|---|---|---|
| 务实 | AI 提升 layout/floorplan/diagnosis/yield learning，但 signoff 和 tapeout 仍靠传统流程 | EDA/IP/verification 2026 公开公司收入 proxy：Cadence FY2026 guide $6.125B-$6.225B，Synopsys Q1 FY2026 revenue $2.409B；行业 TAM 估算 $25B-$35B | 中高，稳健复利 |
| 乐观 | Agentic flows 嵌入大客户 reference flow，emulation/verification/DFT/diagnosis attach 上升 | Cadence non-GAAP operating margin guide 43.5%-44.5%；Synopsys Q1 non-GAAP net income $718.5M，利润率弹性高 | 高 |
| 极度乐观 | Foundry/EDA/设备三方闭环，virtual process emulation 缩短 yield ramp 数月 | 对先进节点和 HBM/3D 封装的 time-to-market 价值极大，但客户验证周期长 | 高但难量化 |

**反证条件。** Agent AI 不能通过 signoff/legal/IP responsibility；客户只把 AI 当 productivity feature 而非高价 SKU；foundry/EDA/设备数据无法共享；安全和模型可解释性限制部署。

## 市场规模和利润池

### 1. 总市场背景：AI/memory 不是反共识，非 AI 被挤出才是风险

| 指标 | 数据日期 | 数字 | 来源类型 | 读法 |
|---|---:|---:|---|---|
| 全球半导体收入 | Gartner, 2026-04-08 | 2025 $805.3B；2026 $1,320.2B；2027 $1,554.5B | 市场研究 | 2026 +64%，已反映极强 AI/memory 预期 |
| Memory revenue | Gartner, 2026-04-08 | 2025 $216.3B；2026 $633.3B；2027 $748.1B | 市场研究 | memory 2026 约 3x，价格 inflation 是核心 |
| Nonmemory revenue | Gartner, 2026-04-08 | 2025 $589.0B；2026 $686.9B；2027 $806.4B | 市场研究 | 逻辑/模拟/传感等增长远低于 memory |
| AI semis revenue share | Gartner, 2026-04-08 | 2026 约占总半导体收入 30%，即约 $396B | 市场研究 | AI 已是主流收入，不是边缘主题 |
| 全球半导体收入 | WSTS Spring 2026 | 2026 $1.51T；2027 ~$1.9T | 行业统计组织 | 比 Gartner 更激进，说明预测分歧大 |
| Memory revenue | WSTS Spring 2026 | 2026 >$800B，约 +250% YoY | 行业统计组织 | 若兑现，对非 AI/消费电子形成强烈成本挤压 |

Gartner 与 WSTS 的 2026 总市场差距约 $190B，memory 差距约 $170B+，这本身就是重要信号：当前市场处在 memflation 和 AI capex 过热区间，任何一条假设变动都会显著影响盈利和估值。报告后续所有情景都应使用区间，不应使用单点。

### 2. 利润池分层

| 层级 | 2026 市场规模/收入 proxy | 当前利润率/毛利率 | 未来一年方向 | 价值捕获判断 |
|---|---:|---:|---|---|
| Advanced foundry / leading edge wafers | 非存储 semis $686.9B；leading-edge foundry service 本稿估算 $140B-$190B | TSMC Q1 2026 gross margin 66.2%，operating margin 58.1%；Q2 gross margin guide 65.5%-67.5% | A16/N2/N2P mix 上升，先进封装 attach 增加，毛利维持高位但 capex 压力大 | TSMC 最高确定性；Intel 弹性高但需 design win/yield 验证；Samsung foundry 需客户验证 |
| HBM / advanced DRAM | TrendForce：2026 HBM shipments >30B Gb；本稿估算 HBM revenue $36B-$60B；Gartner memory $633.3B | Micron FY26 Q2 revenue $23.86B、gross profit $17.755B，计算 gross margin 约 74.4%；SK hynix/Samsung 需用最新财报复核 | HBM4 premium >30%，HBM3E 维持，DRAM equipment +15.1% | SK hynix、Micron、Samsung 及 TSV/bonding/test/EDA 捕获高价值 |
| Advanced packaging / CoWoS / SoIC | TrendForce：2026 TSMC CoWoS 120k-140k wpm，industry near 200k wpm；本稿估算 $17B-$35B service revenue | TSMC 综合 gross margin 66.2%；高端封装初期毛利通常受 ramp/折旧影响低于先进制程，但随着满载改善 | 缺口从 20% 缩到 10%，价格弹性可能下降，技术复杂度上升 | 简单 capacity owner 的溢价下降，SoIC/hybrid bonding/thermal/test 价值上升 |
| Semiconductor equipment | SEMI：2026 total equipment $145B，2027 $156B；WFE 2026 约 $126B；foundry/logic WFE 2026 约 $70B；DRAM equipment 2026 约 $25.9B | ASML Q1 2026 gross margin 53.0%；FY2026 net sales guide EUR36B-EUR40B、gross margin 51%-53% | AI/HBM/advanced logic 支撑，consumer/auto/industrial softness 抵消部分需求 | ASML、AMAT、Lam、KLA、ASM 受益；etch/deposition/metrology 与 bonding/thinning 强度上升 |
| EDA/IP/verification | Cadence FY2026 revenue guide $6.125B-$6.225B；Synopsys Q1 FY2026 revenue $2.409B；本稿估算行业 TAM $25B-$35B | Cadence FY2026 non-GAAP operating margin guide 43.5%-44.5%；Synopsys Q1 non-GAAP net margin约29.8% | AI/agentic EDA 提升 attach 与 seat usage，advanced node signoff 难度上升 | Cadence/Synopsys/Siemens 是“节点复杂度税”的收税者 |
| Optical interconnect / SiPh / CPO | 本稿估算 2026 AI data-center optical interconnect chain $25B-$40B，CPO/SiPh package-in revenue较小 | 高端 DSP/TIA/driver/laser/模块利润分化大，未用单一毛利假设 | 1.6T 放量、CPO/COUPE pilot，2027-2029 才可能大规模转移 | Broadcom/Marvell/Coherent/Lumentum/Innolight 等需按产品组合拆分 |
| Power integrity / thermal / package components | 本稿估算 AI server/package 电源完整性和热管理相关 $5B-$12B | 组件/材料分散，利润率取决于认证和客户绑定 | 3DIC、vertical PDN、liquid cooling、silicon capacitor、MLCC、package inductor 增长 | 低估链条，需跟踪具体 design-in |

### 3. 会后最需要重估的利润迁移

1. **从 wafer-only 到 wafer + package + power/thermal 的系统报价。** A16/18A-P 的价值不只是 wafer ASP，而是把背面供电、先进封装、热/电源 telemetry、HBM attach、EDA signoff 一起卖给 AI/HPC 客户。
2. **从 HBM bit growth 到 HBM qualification 和 packaging allocation。** 2026 的 HBM 价格和毛利来自紧供给，但能否持续取决于 HBM4 良率、base die、TSV、测试、CoWoS allocation。
3. **从设备周期 Beta 到工艺步骤 Alpha。** SEMI 的 $145B equipment forecast 已给总量强景气，超额收益要找 etch/deposition/metrology/bonding/thinning/HAR capacitor/wafer-level packaging 中的步骤暴露。
4. **从“AI EDA 概念”到“良率和 signoff 预算”。** 会议里最接近付费的 AI 工具是 manufacturing/yield/diagnosis/floorplanning，而不是完全替代工程师的自动芯片设计。

## 反共识洞见和重要更新

### 1. 过度乐观方向

**CFET/3DSFET 的短期商业化被高估。** Samsung 的 42nm gate pitch 3DSFET 和 Intel 的 45nm gate pitch CFET 都是关键节点，但它们还没有给出可量产客户产品、良率、成本和 design ecosystem。2026-2027 不应把 CFET 当成 foundry 收入驱动，只能作为设备材料/技术领先叙事。

**A16 headline PPA 不能直接等于 2026 收入。** VLSI 官方 session 写 Q4'26 mass production，但产品收入通常要经过客户 tapeout、wafer cycle、package、qualification 和系统交付。2026 财报大概率主要由 N3/N2/N2P、CoWoS 和 HBM 相关需求驱动，A16 更像 2027 产品节奏变量。

**CoWoS 简单扩产的稀缺性可能已过峰值。** 若 TrendForce 引述的 2026 年底缺口从 20% 缩到 10% 成立，市场会从“谁有产能”转向“谁有下一代封装良率、热、电源和客户绑定”。这对纯扩产叙事不利，对 SoIC/hybrid bonding/large-reticle/测试有利。

**CPO/SiPh 仍不能把 2026 光模块链全部重估为 package-in optics。** NVIDIA C20.2 和 TSMC COUPE 是强信号，但 2026 数据中心主力仍在 800G/1.6T 可插拔、LPO/LRO、DSP/driver/TIA 和交换 ASIC 周期。CPO 是 2027-2029 的架构迁移，不是 2026 全面替代。

### 2. 被低估方向

**电源完整性和 thermal telemetry 被低估。** Intel C2.1 的 20W/mm2、94.8% SCVR，C10.5 的 TV sensor 和 per-core throttling 带来 DNN latency -24%，说明 AI package 里的性能释放越来越依赖电源转换、IR drop、热感知和动态控制。这利好 silicon capacitor、MLCC、高频电源、package inductor、热界面材料、传感器 IP、EDA power integrity signoff。

**制造虚拟化和良率 AI 被低估。** W6 明确说 ML/AI 和 virtualization 用于 root-cause identification、process backtracking、causal modeling、predictive yield analysis。对于 2nm、HBM4、3D DRAM、hybrid bonding，良率 ramp 提前一个季度的价值可能高于单个设计工具 seat 的价格。

**DRAM equipment intensity 被低估。** VLSI 的 AMAT short course 指向 HAR capacitor etch、higher-k/lower-leakage films、wafer bonding、thinning、4F2 access device 和 3D DRAM。SEMI 预测 DRAM equipment 2026 +15.1%、2027 +7.8%，而这还未完全反映 4F2/VS-DRAM 量产前的复杂度上升。

**EDA/IP 是先进节点复杂度的稳定收税层。** Cadence 2026 non-GAAP operating margin guide 43.5%-44.5%，Synopsys Q1 FY2026 revenue $2.409B。会议里从 SCC 到 T2/JFS3 都在说 DTCO/STCO/DMCO，说明先进节点越复杂，foundry、EDA、IP、verification、emulation、DFT 的粘性越高。

### 3. 伪受益公司画像

1. **只有“AI”标签但没有先进节点、封装、HBM、供电/热、EDA/测试客户入口的公司。** VLSI 2026 的利润池非常集中，不会平均分配。
2. **只做传统封装或低端 OSAT，但没有 CoWoS/SoIC/hybrid bonding/large body package 良率能力的公司。** 先进封装 capacity headline 不等于高端 AI package 毛利。
3. **只讲 CPO 概念但没有 laser、SiPh process、EIC/PIC hybrid bonding、switch/GPU 客户认证的公司。** 会议强调 co-design 和 packaging，不是单点光器件替代。
4. **把 CFET/3D DRAM 实验结果包装成 12 个月收入的公司。** 这些路线是重要但远期，近端财务要看 HBM4、advanced DRAM capex、bonding/test。

### 4. 市场可能没有充分理解的更新

**A16 与 18A-P 的比较不应只看 PPA。** TSMC A16 的优势在量产生态、客户和封装配套；Intel 18A-P 的优势在 PowerVia 先发、design-compatible upgrade 和 potential US foundry optionality。市场若只比较“8%-10% vs 9%”会忽略最重要变量：客户 tapeout 和良率曲线。

**HBM4 的价值捕获可能从 memory die 扩散到 base die/foundry/package/test。** TrendForce 说 HBM4 使用 logic chip architecture、I/O doubling to 2048、wafer cost $7k-$8k 且是 traditional DRAM 的 3-4x，这意味着 HBM4 不只是 DRAM price story，而是 logic base die、advanced process、TSV、hybrid bonding 和 test 的综合利润池。

**良率 AI 是设备和 foundry 的共同话题。** Lam、SK hynix、Micron、imec 在 W6 同场，说明制造数据和物理模型正在成为先进制程竞争资产。对 KLA/metrology/process control、Lam/AMAT process chamber、EDA yield analytics 都是正向。

## 公司和产业链映射

| 公司/机构 | VLSI 2026 相关材料 | 近端受益 | 中远期受益 | 主要风险 |
|---|---|---|---|---|
| TSMC | A16 T1.5、2nm DCIM C8.1、2nm SRAM C29.1、SCT3、2026 Tech Symposium CoWoS/COUPE/SoIC | A16/N2/N2P、CoWoS、SoIC、COUPE、AI/HPC wafer + package | A12/A14、14-reticle CoWoS、A14-to-A14 SoIC | A16 量产节奏、客户集中、AI capex reversal、先进封装良率 |
| Intel / Intel Foundry | 18A-P T1.2、T2.3、T5.2 CFET、C2.1 SCVR、C10.5 TV sensor、Intel newsroom | 18A-P risk production、PowerVia、internal CPU/AI roadmap | 外部 foundry 客户、CFET、GaN+Si power | 无锚定外部客户、yield/交付、Foundry 亏损 |
| Samsung | T1.1 3DSFET、T5.1 VS-DRAM、T2.2 DAB BPD、W3 packaging、C28.5 | HBM/DRAM recovery、GAA/3DSFET 技术叙事 | VS-DRAM、3DSFET、foundry regain | HBM qualification、foundry 客户、良率 |
| SK hynix | W5 DRAM、T8.5 4F2 VG DRAM、W6 virtual manufacturing | HBM3E/HBM4 pricing、EUV/TSV/bonding capex | 4F2/vertical DRAM | HBM share 被 Samsung/Micron 稀释、价格周期 |
| Micron | W5、W6、FY26 Q2 财务 | HBM/DRAM 高毛利、AI memory | advanced DRAM + virtual manufacturing | HBM4 认证、memory price reversal |
| Kioxia/SanDisk | T1.4 >1,000 WL 3D Flash、SCC3 | NAND density roadmap、AI storage | multi-stacked 3D NAND | NAND price volatility、capex discipline |
| NVIDIA | W2/W5、C20.2 optical receiver | HBM/CoWoS allocation、optical I/O 技术验证 | package-in optics、memory-centric architecture | 供应链瓶颈、客户预算、替代 ASIC |
| AMD | W3 electronic-photonic co-design、W5 datacenter AI DRAM | MI/AI package、HBM demand | co-packaged optical transceiver | GPU share、software ecosystem |
| Qualcomm / MediaTek | W5 distributed AI、C21.1 TinyNPU | edge AI/always-on reasoning SoC | AI glasses/wearables/robotics | 端侧需求兑现 |
| ASML | 先进 GAA/DRAM EUV 强相关；官方 Q1 2026 gross margin 53% | EUV/DUV demand, HBM/advanced DRAM | High-NA and future nodes | 出口管制、客户 capex 波动 |
| Applied Materials | SCT4 materials/process for AI architectures | HAR capacitor, high-k films, deposition/etch/material engineering | CFET, 3D DRAM, interconnect | capex cycle、竞争 |
| Lam Research | W6 organizer, AI/ML process modeling | etch/deposition/yield ramp, HBM/DRAM | manufacturing virtualization | memory capex reversal |
| KLA | 未见核心论文，但 metrology/inspection 对 2nm/HBM/3D packaging 必需 | defect inspection, process control | AI yield analytics | 估值和 capex cyclicality |
| ASM | T2.1 imec/ASM backside contacting | ALD/epi/process modules | CFET/BSPDN | 节点 adoption |
| Synopsys / Cadence / Siemens | W3 Synopsys、SCC Siemens、Cadence 财务作为 EDA proxy | AI EDA、verification、emulation、IP | agentic EDA、DTCO/STCO/DMCO | AI feature monetization timing、客户预算 |
| Arm | A16/18A-P benchmark 常用 Arm core block | IP reuse and advanced node validation | AI/HPC custom CPU/IP | RISC-V/custom alternatives |
| imec / IBM | W2/W3/W4/W6/T1.3/T2.1/T5.4 | research-to-equipment ecosystem | 2D materials、CFET、spin qubit、3D integration | 商业化路径长 |

## 风险、反证条件和后续跟踪

### 1. 核心结论的反证条件

| 结论 | 反证数据 | 跟踪频率 |
|---|---|---|
| A16 是 2027 高端 AI/HPC 关键节点 | TSMC 将 A16 mass production 推迟；客户继续优先 N2P/N3P；A16 wafer ASP 或良率低于预期 | 月度/季度 |
| Intel 18A-P 有 foundry 可选性 | 无外部客户 tapeout；18A-P yield/PPAC 低于客户要求；Intel Foundry 亏损扩大 | 季度 |
| HBM4/HBM3E 维持高利润 | HBM4 premium 低于 20%；Samsung/Micron 快速扩供；CSP 库存累积；DRAM/NAND price relief 提前 | 月度 |
| CoWoS/advanced packaging 仍是瓶颈 | 供需缺口在 2026 年底前低于 5%；OSAT 替代良率追上；GPU/ASIC 出货被需求而非封装限制 | 月度 |
| EDA/yield AI 进入实用 ROI | 客户不为 agentic/AI add-on 付费；AI 不进入 signoff；制造数据共享受限 | 半年 |
| Silicon photonics/CPO 中期放量 | CPO 可靠性/维修/热问题无法解决；1.6T pluggable/LPO 延长电互连寿命；客户不愿改变系统架构 | 季度/半年 |

### 2. 后续必须追踪的 20 个数据点

1. TSMC A16：Q4'26 是否按期 mass production，首批客户和产品类型。
2. TSMC N2/N2P/A16：2026H2-2027 wafer starts、良率、wafer ASP。
3. Intel 18A-P：外部客户 tapeout、Power Boost adoption、risk production 到 HVM 时间。
4. Intel Foundry：quarterly operating loss、external revenue、customer prepayment。
5. Samsung foundry：2nm GAA 客户、3DSFET/CFET 路线公开节点。
6. SK hynix/Samsung/Micron：HBM4 qualification with NVIDIA/AMD/custom ASIC。
7. HBM ASP/Gb：HBM3E 与 HBM4 premium 是否维持 >30%。
8. HBM bit shipment：是否超过 TrendForce 2026 >30B Gb 口径。
9. CoWoS capacity：TSMC 120k-140k wpm 兑现程度和 OSAT 50k-60k wpm 兑现程度。
10. CoWoS lead time：缺口是否从 20% 缩到 10%，是否进一步低于 5%。
11. Large-reticle package：5.5-reticle 到 14-reticle 的 design win。
12. SoIC/hybrid bonding：HBM/base die/logic stacking 的良率和 throughput。
13. 3D DRAM/4F2：Samsung/SK hynix pilot timing、capex line item。
14. DRAM equipment：SEMI 2026 +15.1% 是否被上修。
15. ASML：EUV order backlog、memory EUV 订单、China 出口影响。
16. AMAT/Lam/KLA/ASM：HBM/DRAM/advanced packaging 相关订单占比。
17. EDA：Cadence/Synopsys/Siemens AI add-on 收入、emulation backlog、IP attach。
18. CPO/SiPh：TSMC COUPE 2026 production 客户、NVIDIA/AMD/Broadcom 采用情况。
19. Power/thermal：silicon capacitor、MLCC、package inductor、liquid cooling design-in。
20. AI capex：hyperscaler capex 增速是否仍 >50%，memory price 是否压缩非 AI 需求。

### 3. 证据分级

- **A级，一手会议/公司材料**：会议 official program、technical tipsheet、online session、Intel/TSMC/Samsung/imec 官方材料。用于核心事实和技术参数。
- **B级，权威市场研究/行业组织**：Gartner、WSTS、SEMI、TrendForce。用于市场规模、供需、设备 capex 和价格方向，但不同机构口径冲突时采用区间。
- **C级，媒体/券商/供应链报道**：用于市场情绪、交易线索、传闻客户和产能线索。不可单独支撑结论。
- **D级，社交媒体/参会者分享**：本次检索中仅作为弱线索处理；未用来支撑核心结论。

## 来源清单

| 编号 | 来源 | 日期 | 类型 | 置信度 | 本稿用途 |
|---|---|---:|---|---|---|
| S1 | IEEE/JSAP Symposium on VLSI Technology & Circuits 2026 官网，https://www.vlsisymposium.org/ | 2026 | 会议官方 | 高 | 会议主题、范围、会议构成 |
| S2 | VLSI 2026 Technical Program PDF，https://www.vlsisymposium.org/wp-content/uploads/2026/05/VLSI26_Program_Finalv2.pdf | PDF as of 2026-05-17 | 会议官方 | 高 | workshop、short course、technical session、论文标题和摘要 |
| S3 | VLSI 2026 Technical Tipsheet，https://www.vlsisymposium.org/wp-content/uploads/2026/04/2026-VLSI-Technical-Tipsheet-REVISED-FINAL-4.30.26-.pdf | 2026-04-30 | 会议官方 | 高 | 高亮论文参数：A16、18A-P、3DSFET、DRAM、CIM、SiPh、SCVR |
| S4 | VLSI 2026 Paper Images & Captions，https://www.vlsisymposium.org/images-captions/ | 2026 | 会议官方 | 高 | 高亮论文清单和图片/说明材料索引 |
| S5 | VLSI Online T1.5 TSMC A16 session，https://vlsi26.mapyourshow.com/8_0/sessions/session-details.cfm?ScheduleID=246 | 2026-06-16 aired | 会议官方在线议程 | 高 | A16 技术参数、适用场景、Q4'26 mass production |
| S6 | VLSI Online T5.1 Samsung VS-DRAM session，https://vlsi26.mapyourshow.com/8_0/sessions/session-details.cfm?ScheduleID=306 | 2026-06-17 aired | 会议官方在线议程 | 高 | 16-tier VS-DRAM 摘要 |
| S7 | Intel Newsroom, “Intel Foundry Details Process Milestones and Future Innovation at VLSI Symposium”，https://newsroom.intel.com/intel-foundry/intel-foundry-details-process-milestones-future-innovation-at-vlsi-symposium | 2026-06-16 | 公司官方 | 高 | 18A-P risk production、PPA、Power Boost、thermal/via resistance |
| S8 | Samsung Semiconductor Blog, “From GAA to 3D Stacked FET”，https://semiconductor.samsung.com/news-events/tech-blog/from-gaa-to-3d-stacked-fet-expanding-the-transistor-into-the-third-dimension/ | 2026-06 | 公司官方 | 高 | 3DSFET 42nm gate pitch、triple nanosheet、MDI、uniformity |
| S9 | imec VLSI 2026 event page，https://www.imec-int.com/en/events/2025-symposium-vlsi-technology-and-circuits | 2026 | 机构官方 | 高 | imec workshop/short course/technical session 参与 |
| S10 | TSMC 2026 North America Technology Symposium press release，https://pr.tsmc.com/english/news/3302 | 2026-04-23 | 公司官方 | 高 | A12/N2U、5.5-reticle CoWoS、14-reticle CoWoS、COUPE、SoIC |
| S11 | TSMC 2024 North America Technology Symposium press release，https://pr.tsmc.com/english/news/3136 | 2024-04-24 | 公司官方 | 高 | A16 原始路线图、SPR、PPA、2H26 目标 |
| S12 | Gartner, “Worldwide Semiconductor Revenue to Exceed $1.3 Trillion in 2026”，https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026 | 2026-04-08 | 市场研究 | 中高 | 2025-2027 半导体、memory、AI semis 市场规模 |
| S13 | WSTS Spring 2026 forecast，https://www.wsts.org/76/103/Global-Semiconductor-Market-Surges-Beyond-15T-2026 | 2026 | 行业统计组织 | 中高 | 与 Gartner 对照的激进市场规模口径 |
| S14 | SEMI equipment forecast，https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports | 2025-12 | 行业组织 | 高 | 2026/2027 equipment、WFE、DRAM、NAND、test、A&P 规模 |
| S15 | TrendForce, CoWoS supply-demand gap，https://www.trendforce.com/news/2026/06/15/news-tsmc-cowos-supply-demand-gap-reportedly-seen-narrowing-from-20-to-10-by-end-2026-as-capacity-expands/ | 2026-06-15 | 市场/供应链研究 | 中 | CoWoS gap、120k-140k wpm、industry near 200k wpm |
| S16 | TrendForce, HBM4 premium report，https://www.trendforce.com/research/download/RP250509XF | 2025-05-09 | 市场研究 | 中 | HBM4 >30% premium、2048 I/O、2026 HBM shipment >30B Gb |
| S17 | TSMC Q1 2026 quarterly results，https://investor.tsmc.com/english/quarterly-results/2026/q1 | 2026Q1 | 公司财务 | 高 | TSMC revenue、gross margin、operating margin、Q2 guidance |
| S18 | Micron FY2026 Q2 results，https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026 | 2026-03 | 公司财务 | 高 | Micron revenue、gross profit、memory margin proxy |
| S19 | ASML Q1 2026 results，https://www.asml.com/news/press-releases/2026/q1-2026-financial-results | 2026-04-15 | 公司财务 | 高 | ASML sales guide、gross margin、EUV equipment利润率 proxy |
| S20 | Cadence Q1 2026 results，https://investor.cadence.com/news/news-details/2026/Cadence-Reports-First-Quarter-2026-Financial-Results/default.aspx | 2026-05 | 公司财务 | 高 | Cadence revenue guide、non-GAAP operating margin |
| S21 | Synopsys FY2026 Q1 results，https://news.synopsys.com/2026-02-25-Synopsys-Posts-Financial-Results-for-First-Quarter-Fiscal-Year-2026 | 2026-02-25 | 公司财务 | 高 | Synopsys revenue、non-GAAP net income |
| S22 | Mordor Intelligence HBM market page，https://www.mordorintelligence.com/industry-reports/high-bandwidth-memory-market | 2026-05-06 updated | 市场研究 | 低-中 | 用于提示 HBM 市场口径分歧；未作为本稿基准估算 |

