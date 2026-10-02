# ECTC 2026会议追踪：核心变化、产品爆发和市场预期差

会议对象：2026 IEEE 76th Electronic Components and Technology Conference（ECTC 2026）  
会议日期：2026-05-26 至 2026-05-29  
会议地点：Orlando, Florida；JW Marriott & The Ritz-Carlton Grande Lakes Resort  
材料检索截止日期：2026-06-10 20:57 PDT / 2026-06-11 UTC  
报告完成日期：2026-06-11（文件名使用会话当前日期；本机本地日期为 2026-06-10 PDT）  
资料边界：本报告为独立会议追踪底稿，只使用公开联网资料、会议材料、公司材料和明确标注的二手/非官方材料；未读取或引用项目内既有公司、行业、日度、量化、tmp、data 或缓存结论。

## 结论摘要

ECTC 2026的主线不是“又一次先进封装热”，而是先进封装从单点互连能力升级为 AI/HPC 系统架构约束：单包尺寸逼近或超过 100 mm x 100 mm，功耗逼近或超过 1,000 W，逻辑-HBM-CPO-电源-散热-基板必须同时优化。ASE CEO keynote、数据中心能耗 plenary、AI 数据中心总统 panel、8个 special sessions 和官方技术 tipsheet 的共同信号是：未来2年利润池不只在 CoWoS/OSAT 产能，也在混合键合、panel/glass/organic substrate、CPO 可插拔/可维护耦合、直接液冷、低损耗材料、面板级 CMP/曝光、overlay/metrology 和多物理 EDA。

最大技术变化：W2W 混合键合从“微米级可用”向“亚0.5微米可验证”推进。官方 tipsheet 将 Applied Materials/EV Group 的 450 nm pitch Cu-Cu hybrid bonding、20 million interconnect links、single-via chain 98% yield、double-via chain 100% yield 列为高亮；KIOXIA 展示面向多层 CBA 3D Flash 的 sub-800 nm pitch direct bonding；imec/TEL/Applied/EVG 等论文覆盖 140 nm、200 nm、300 nm pitch 和 50 nm overlay 等方向。判断：W2W 在 CIS/3D NAND/未来 DRAM 方向比 D2W chiplet 更接近确定量产；D2W 的最大瓶颈仍是 die distortion、placement、overlay、rework 和 KGD 经济性。

最大产业变化：panel-level integration、glass core 和 ultra-fine organic substrate 从“未来路线”变为会议核心议题。ASE 会前发布自动化 310 mm panel-level packaging；Resonac 报告 320 x 320 mm glass panel 上 2/2 um L/S organic polymer damascene wiring 和 <100 nm coplanarity；USHIO 报告 510 x 515 mm glass substrate 上 18-reticle area stitching-free exposure 和 1.5 um L/S；Intel、Samsung、DNP、Georgia Tech、Corning、Amkor 等都把 glass/TGV/large-body reliability 拉到 AI/HPC 语境。判断：2026-2027最先放量的可能不是完整“玻璃基板替代”，而是设备、材料、RDL、CMP、曝光、检测和小规模高端试产。

最大预期差：CPO 被市场当作“即将大规模替代 pluggable optics”的交易主题，但 ECTC 2026显示真正拐点在可制造、可测试、可维护的 optical I/O packaging。AIST 的 AOP substrate 达到 112 Gbps PAM4 演示和 6.4 Tbps/substrate 估算容量；GlobalFoundries/Corning 的 detachable glass waveguide connector 做到 <1.5 dB/facet 和 280 mW power handling；Intel 的 fan-out glass coupler/expanded-beam connector 显示约 -1.55 dB coupling loss、>100次插拔、性能漂移远小于 0.01 dB 且无失效。判断：2026是工程验证和早期导入年，真正大规模收入更可能在2027-2028以后；但连接器、玻璃耦合器、硅光工艺、CPO封装测试的价值捕获已经提前开始。

最大利润池变化：先进封装正在从“低毛利后段服务”向“瓶颈资产+工艺know-how+平台绑定”抬升。TrendForce 2026-04-28转述市场资料称 CoWoS 单片 ASP 约 10,000美元、2026容量约130万片、2027或到200万片，且 advanced packaging 有望成为TSMC利润驱动之一；但OSAT公开毛利率仍显著低于前道/设备。Applied Materials FY2026 Q2 GAAP gross margin 49.9%、operating margin 31.9%；ASE Q1 2026 gross margin约20.1%；Amkor Q1 2026 gross margin约14.2%。因此，更高确定性的利润池在设备、材料、检测、良率控制和客户锁定的平台型foundry，而不是所有“封装产能”。

最大风险：会议材料有大量“first demonstration”“prototype”“simulation”“early results”，不能等同于量产节奏。需要把 3个月、1年、2年分开：3个月看客户design-in和设备订单；1年看HBM4/HBM4E、CPO pilot、PLP良率、CoWoS外溢产能；2年看14-reticle CoWoS、A14/A12 SoIC、Marvell/Celestial收入里程碑、glass-core高端AI包的真实量产。

## 会议重点和方向变化

| 主题 | 会议证据与公司 | 关键数字/参数 | 变化性质 | 投资含义 | 置信度 |
|---|---|---:|---|---|---|
| 系统级优化替代单点封装 | ASE CEO keynote；数据中心能耗 plenary；AI数据中心 panel | 大包体超过100 mm x 100 mm、功耗接近/超过1,000 W被会议列为系统集成挑战 | 已经从技术讨论变成客户架构约束 | 先进封装、供电、散热、光互连、材料要合并建模；单一封装产能故事不够 | 高 |
| 亚微米混合键合 | Applied/EVG、KIOXIA、imec、TEL、ASML、Intel、CEA-Leti | 450 nm Cu-Cu pitch、20M links、98% single-via yield；sub-800 nm CBA；D2W <80 nm overlay simulation | W2W接近更高密度量产前夜；D2W仍在工程化 | 设备/表面处理/CMP/overlay/metrology优先受益；D2W chiplet收入需折现 | 高 |
| HBM4/高速电互连 | Intel EMIB-T、Samsung HBM4e、SK hynix HBM metrics、University of Florida Cu/Co metaconductor | HBM4E 12+ Gb/s；HBM4e up to 12 Gb/s；112G向224G/400G lane迁移；0.065 dB/mm at 37.5 GHz | 电互连仍在延寿，不是立刻被CPO完全替代 | 低损耗RDL、organic interposer、substrate材料、SI/PI设计仍有高弹性 | 高 |
| Panel-level / glass / organic substrate | ASE 310 mm PLP；Resonac 320 x 320 mm panel CMP；USHIO 510 x 515 mm large-field exposure；Intel glass core | 2/2 um L/S、<100 nm coplanarity、18-reticle area、1.5 um L/S、310/320/510 mm级面板 | 从“概念路线”进入设备/材料/工艺验证密集期 | 面板级曝光/CMP/干膜/低翘曲材料比“玻璃基板概念”更早兑现 | 中高 |
| CPO/optical I/O serviceability | AIST、GF/Corning、Intel、Marvell/Celestial、Lightmatter、Celestial AI | 112 Gbps PAM4、6.4 Tbps/substrate；<1.5 dB/facet；280 mW；-1.55 dB；>100插拔 | 从“能传光”转向“可装配、可维护、可量产” | CPO 2026收入小，但可维护耦合器/硅光平台/封装测试提前重估 | 中高 |
| 直接液冷与热管理 | TSMC CoWoS-R liquid cooling、imec jet impingement、Adeia DTC、diamond-on-chip、TIM材料 | CoWoS-R直接到硅液冷；AI server系统热验证；数据中心液冷2026市场约40-82亿美元区间 | 热不再是后端附件，而是package架构输入 | 冷板/微通道/TIM/diamond/仿真工具受益；验证周期和漏液可靠性是门槛 | 中高 |
| 材料和临时键合/解键合 | Brewer Science、Resonac、Mitsui、Sumitomo Bakelite、Nopion、CEA-Leti | Brewer LRL 600 nm film <1% UV transmittance；Indium 3 um bump / 5 um pitch；nanosolder ~1 um joint | 工艺窗口和材料洁净度成为yield变量 | 小材料公司有弹性，但需客户qualified；概念材料必须经过可靠性验证 | 中 |
| AI-enabled EDA/DfR | Special session on AI-enabled EDA；TU Delft physics-constrained multi-agent DfR | 多物理域：thermal/mechanical/SI/EM；agentic DfR用于结构化知识和实验建议 | 仍是工具和流程早期，但客户痛点明确 | 价值在EDA/仿真/可靠性数据库，不是短期封装收入主线 | 中 |
| Quantum packaging | Quantum infrastructure special session；IonQ/Google/Microsoft/PsiQuantum/IBM等参与 | cryogenic interconnect、EMI、thermal、control electronics | 长期选项，不是2026收入主线 | 可作为低温材料、indium bump、光子封装线索，不宜直接上升为投资主线 | 中低 |

与ECTC 2025相比，2026的变化不是主题完全替换，而是成熟度提高：2025官方和会后材料已经集中讨论CPO、1 um hybrid bonding、glass/RDL、cooled chiplets、advanced power delivery；2026则把这些主题压到更具体的量产障碍上，包括sub-0.5 um W2W yield、D2W overlay、2/2 um panel RDL、510 mm级大面积曝光、detachable optical connector、CoWoS-R板级可靠性和数据中心能耗。也就是说，市场热点从“先进封装能不能支撑AI”转向“谁能把良率、尺寸、散热、可维护性和客户导入同时做出来”。

## 产品和技术路线三情景预测

以下预测把会议事实、外部市场规模和估算假设分开。美元口径均为公开材料可得数据或基于公开数据的估算，日期为材料检索截止日2026-06-11。

| 技术/产品方向 | 当前成熟度 | 3个月节点 | 1年基准/乐观/超预期 | 2年判断 | 当前市场规模与口径 | 利润率与价值捕获 |
|---|---|---|---|---|---|---|
| W2W / D2W hybrid bonding | W2W在CIS/NAND已有量产基础，先进pitch仍在demo/qualification；D2W为pilot/工程验证 | 看AMAT/EVG/TEL/ASML/BESI订单、HBM/3D NAND客户验证、sub-300 nm paper后续 | 基准：bonding equipment 2027约6.2-6.5亿美元；乐观：AI/HBM推动+15-25%；超预期：HBM4/D2W提前，hybrid相关工具+30% | 2028前W2W更确定；D2W若overlay/rework解决，才会进入大规模chiplet | Semiconductor bonding equipment 2026约5.96亿美元；hybrid bonding技术市场口径差异大，公开估算从1.6亿美元到数十亿美元不等 | 设备和工艺材料毛利最高，AMAT类平台毛利约50%；OSAT装配毛利低得多；关键是surface prep、CMP、bond chamber、metrology |
| CoWoS/large 2.5D AI package | 已量产且供给紧张；从5.5 reticle向9.5/14 reticle演进 | 看TSMC/ASE/Amkor/SPIL外溢产能、BGA/board reliability、HBM供给 | 基准：AI 2.5D封装服务2027较2026 +30-45%；乐观：CoWoS单位容量和ASP同步上行；超预期：客户接受更高ASP且良率不降 | 2028 14-reticle CoWoS若按TSMC路线进入生产，价值进一步上移到foundry package platform | TrendForce转述：CoWoS wafer ASP约1万美元，2026 capacity约130万片；TSMC advanced packaging 2025收入占比约10% | Foundry平台最强；先进封装毛利当前低于TSMC平均但改善；OSAT毛利受客户议价和良率约束 |
| Panel-level packaging / glass / organic interposer | 消费fan-out已有基础；AI/HPC large panel仍在试产/验证 | 看ASE 310 mm平台客户样品、Resonac/USHIO/EVG设备材料导入、panel warpage/yield数据 | 基准：PLP 2027约5.5亿美元；乐观：6.5-7.5亿美元；超预期：AI/HPC pilot拉动至8亿美元以上 | 2028-2029才可能看到高端AI包的规模切换；短期利润在工具/材料 | PLP 2025约3.5亿美元、2026约4.4亿美元、2031约13.7亿美元；2.5D/3D panel CAGR约29.2%；glass core CAGR约28.9% | 早期设备/材料/检测利润优于代工封装；大规模后OSAT/基板厂靠良率和客户绑定赚钱 |
| CPO / optical I/O / detachable glass coupling | 2026为demo、pilot和小规模deployment；量产可维护性是核心 | 看OCP、Broadcom/Marvell/NVIDIA/TSMC/Intel客户路线、connector reliability、laser attach良率 | 基准：CPO 2027约2.2-2.4亿美元；乐观：3-4亿美元；超预期：特定hyperscaler scale-up采用后5亿美元以上 | Marvell/Celestial披露FY2028 H2开始有意义收入、FY2028 Q4年化5亿美元、FY2029 Q4年化10亿美元 | Mordor估算CPO 2026约1.65亿美元、2031约7.64亿美元；Cignal认为规模化更可能2027/2028以后 | 价值在switch/XPU平台、silicon photonics foundry、optical engine、玻璃/连接器、测试；传统可插拔模块利润可能被压缩 |
| Advanced thermal / direct liquid / TIM | 数据中心液冷量产加速，package内直接冷却仍在工程验证 | 看rack功率密度、微软/Google/Meta数据中心水/电指标、CoWoS-R直接液冷可靠性 | 基准：data center liquid cooling 2027约50-90亿美元；乐观：AI server渗透率提升至90-110亿美元；超预期：大客户强制液冷新建集群，120亿美元以上 | 2028后直接到芯片/到封装的协同设计成为高端AI平台默认选项之一 | 2026 data center liquid cooling公开估算约40.7-81.7亿美元；全球TIM 2026约28.1-38亿美元；semiconductor TIM 2026约13.1亿美元 | 冷却系统规模大但竞争分散；package级TIM/diamond/microchannel/仿真若被平台锁定，毛利和粘性更好 |
| HBM4/HBM4E package interconnect / PDN / low-loss wiring | HBM3E量产；HBM4/HBM4E package SI/PI处于验证和客户导入 | 看12 Gb/s HBM4E、UCIe 32 GT/s、224/400G lane材料/互连验证 | 基准：HBM市场2027约50亿美元以上；乐观：60-80亿美元；超预期：ASP和供应短缺共振至90亿美元以上 | 2028仍供给偏紧，利润更多在HBM供应商和CoWoS/HBM封装瓶颈 | HBM 2026市场口径分歧大：Mordor约39.8亿美元，Precedence约91.8亿美元；共同点是20%+ CAGR | HBM供应商和先进封装平台捕获最大；RDL/low-loss材料、测试和良率控制为二阶高弹性 |
| AI EDA / multi-physics reliability automation | early workflow；真实商业化在特定工具链和客户数据库中 | 看EDA vendors与foundry/OSAT的ADK、可靠性数据库、自动DOE落地 | 基准：作为EDA附加模块增长；乐观：先进封装sign-off刚需；超预期：客户把package sign-off预算前移 | 2年后可能成为先进封装设计门槛，但不是独立大TAM主线 | 无可靠会议直接TAM；可归入EDA/仿真/可靠性工具增量 | 软件毛利高，壁垒在数据和foundry认证；独立小工具若无生态认证难捕获利润 |

## 市场规模和利润池

### 1. 先进封装整体

事实：Yole 2025资料显示 advanced packaging 市场2024年约460亿美元，预计2030年超过794亿美元，2024-2030 CAGR约9.5%；Yole 2026 monitor摘要显示2025 Q4 advanced packaging revenue接近150亿美元，2026 Q1预计环比回落。若用2024年460亿美元和9.5% CAGR粗算，2026年整体先进封装约550亿美元；若按2025 Q4年化口径，2026运行率接近600亿美元。

估算：2026-2027增量主要来自AI/HPC的2.5D/3D、HBM封装、large body substrate、CPO前置研发、panel/glass pilot，而不是传统手机fan-out。基准口径下2027先进封装整体约600-650亿美元；乐观口径约680-720亿美元；超预期乐观口径若AI accelerator出货和HBM供给同步上修，可接近750亿美元运行率。

利润池：TSMC/Intel/Samsung这类foundry-integrated packaging平台掌握客户设计入口；ASE/Amkor/SPIL等OSAT承接外溢和区域化产能；AMAT/EVG/BESI/TEL/ASML/USHIO/Onto/Camtek等设备检测公司享受较高毛利；Resonac/Ajinomoto/Corning/Brewer/Indium/Sumitomo Bakelite等材料公司享受qualification后的粘性。利润率排序通常是：关键设备/EDA/材料 > foundry平台型先进封装 > 高端OSAT > 普通封装代工。

### 2. CoWoS、大尺寸2.5D和HBM封装

事实：TSMC 2026-04-23技术发布称已经在生产5.5-reticle CoWoS，并计划2028生产14-reticle CoWoS，可集成约10个大compute dies和20个HBM stacks；2029进一步超过14 reticles，并有40-reticle SoW-X。TrendForce 2026-04-28转述市场资料称CoWoS wafer ASP约1万美元、2026容量约130万片、2027约200万片；TSMC advanced packaging 2025收入占比约10%。

估算：如果以CoWoS capacity 130万片、ASP 1万美元粗算，2026 CoWoS相关年化服务收入可达约130亿美元；考虑不同package类型、良率、客户结构和ASP差异，合理区间为100-150亿美元。2027若容量至200万片且ASP不塌，收入区间可到160-220亿美元。此估算是投资口径，不等同于公司正式披露。

观点：会议新增证据支持CoWoS生态的“可靠性和散热成本上升”而非单纯产能扩张。TSMC在ECTC 2026中强调CoWoS可靠性、CoWoS-R板级可靠性和直接液冷，说明未来价值不只是更多片数，而是更大包体、更高功耗、更复杂材料栈下的良率与寿命模型。

### 3. Panel-level packaging、glass core 和大面积RDL

事实：Mordor 2026资料估算PLP市场2025年约3.5亿美元、2026年约4.4亿美元、2031年约13.7亿美元，2026-2031 CAGR约25.58%；2.5D/3D panel integration CAGR约29.2%；glass core substrate材料口径在2025占PLP约12.3%，但CAGR约28.9%。ECTC 2026的具体进展包括：ASE自动化310 mm PLP；Resonac 320 x 320 mm glass panel上的2/2 um L/S和<100 nm coplanarity；USHIO 510 x 515 mm glass substrate上18-reticle exposure和1.5 um L/S。

估算：2026-2027 PLP收入仍小，基准2027约5.5亿美元，乐观6.5-7.5亿美元，超预期8亿美元以上。真正对大股票有意义的不是PLP自身TAM，而是它对CoWoS成本、interposer尺寸、substrate utilization和HBM4 RDL密度的影响。若高端AI包体从300 mm wafer限制转向panel流程，设备和材料的边际收入会先于OSAT封装收入出现。

观点：市场容易把“glass substrate”交易成单一材料替代，但ECTC 2026显示真正难点是整套工艺：TGV形成、低翘曲、RDL精度、dry film、panel CMP、large-field exposure、inspection、warpage model和可靠性。只卖普通玻璃或普通基板的公司不是自动受益方。

### 4. CPO / photonic I/O

事实：Mordor 2026资料估算CPO市场2025年约1.21亿美元、2026年约1.65亿美元、2031年约7.64亿美元，2026-2031 CAGR约35.92%；Cignal AI 2025观点认为2026可能有少量CPO出现，但规模化更可能在2027/2028以后。Marvell收购Celestial AI材料披露，Photonic Fabric第一代scale-up chiplet提供16 Tbps/chiplet，并预期FY2028下半年开始有意义收入，FY2028 Q4 annualized run rate 5亿美元，FY2029 Q4达到10亿美元。

会议事实：AIST的active optical package substrate展示112 Gbps PAM4和6.4 Tbps/substrate估算；GF/Corning detachable glass connector展示<1.5 dB/facet和280 mW；Intel fan-out glass coupler方案展示约-1.55 dB、>100次插拔、性能漂移极小且无失效。TSMC 2026-04-23发布称COUPE on substrate将在2026开始生产，较board-level pluggable有2x power efficiency和10x latency reduction，并以200 Gbps micro-ring modulator为特征。

观点：CPO的市场规模2026仍小，但技术路线在从“光学可行性”跨向“运维可行性”。最大价值不一定在传统可插拔模块厂，而在switch/XPU平台、silicon photonics foundry、optical engine、外部激光/连接器、玻璃耦合器、封装测试和可靠性。短期股价若按“2026全面替代pluggable”定价，需要降权。

### 5. 散热、TIM和数据中心能耗

事实：ECTC 2026把数据中心能耗设为plenary和President's Panel，技术论文覆盖CoWoS-R direct-to-silicon liquid cooling、jet impingement、two-phase cooling、diamond-on-chip、direct-to-chip liquid cooling integration、thermal-aware PDN/IVR和AI server thermal validation。公开市场资料对2026 data center liquid cooling市场估算差异较大，约40.7-81.7亿美元；全球TIM市场2026约28.1-38亿美元，半导体封装TIM约13.1亿美元。

估算：2027液冷市场基准50-90亿美元，乐观90-110亿美元，超预期120亿美元以上；半导体封装TIM 2027约14-16亿美元，若AI/HPC premium TIM占比提升可更快。直接到硅、到interposer、到package lid的解决方案市场规模尚未标准化披露，需要用具体design win和BOM估算。

观点：散热不再是“数据中心建设配套”，而是AI封装架构输入。利润池可能从传统机房冷却设备向package-level材料、冷板、微通道、泵/歧管、仿真、可靠性测试迁移。风险是客户会把系统级冷却压价成基础设施采购，而高端TIM/微通道若没有平台认证也难以获得高溢价。

## 反共识洞见和重要更新

1. CPO不是2026的全面收入爆发，真正反共识是“可维护连接器”变成核心瓶颈。会议高亮的不是单纯更高速光器件，而是detachable glass waveguide、expanded beam、passive alignment、plug/unplug reliability和package-level test flow。若后续客户仍不愿接受现场维护复杂度，CPO会继续延后。

2. Hybrid bonding的亚0.5微米W2W进度强于D2W chiplet量产进度。AMAT/EVG 450 nm和KIOXIA sub-800 nm更偏W2W memory/CBA；ASML D2W <80 nm overlay仍是simulation和方法论。市场若把所有hybrid bonding paper都直接映射到AI chiplet 2026收入，会高估D2W节奏。

3. Organic substrate没有被CoWoP或glass完全替代。ECTC 2026的organic substrate seminar强调，在NVIDIA提出CoWoP等新路径后，organic substrates仍连接chiplets、wafers、large panels和system board。更可能的路线是organic、glass、silicon interposer、bridge和panel工艺共存，而不是单一材料胜出。

4. PLP/glass短期受益者更像“设备+材料+检测”，不是所有基板厂。Resonac、USHIO、EVG、Brewer、Corning、DNP、Sumitomo Bakelite、Mitsui等材料/设备/工艺节点，比普通PCB或传统封装公司更接近会议新增信息。

5. 数据中心能耗主题给散热公司带来叙事，但会议真正强调的是package/system co-design。只有能进入CoWoS/large 2.5D/AI server验证流程的TIM、direct liquid、diamond、thermal via、仿真和可靠性供应商才有高弹性；泛冷却设备公司可能只拿到低差异化基建收入。

6. Amkor/ASE是实际产能与客户合作受益方，但利润弹性不能简单等同于收入弹性。Amkor ECTC会后材料强调AI、HPC、photonics、advanced memory和Arizona扩产；ASE强调310 mm PLP和hyperscale customers。但从公开毛利看，OSAT仍低于设备和foundry平台。投资上应同时追踪收入mix、utilization、yield、客户集中度和折旧。

7. 3D Flash / NAND方向被AI叙事遮住，但KIOXIA multi-stacked CBA bonding可能更接近真实W2W规模应用。若NAND周期修复和3D Flash层数继续上行，direct bonding设备/材料需求可能早于某些AI chiplet D2W应用兑现。

8. 会议中大量“AI-enabled EDA”和“agentic DfR”不是短期收入主线，但可能改变先进封装设计入口。先进封装的失败模式跨材料、热、机械、SI/PI和板级可靠性，单靠传统EDA或封装厂经验不足。谁能把ADK、foundry rule、reliability database和multi-physics sign-off绑定，谁可能获得软件利润池。

## 公司和产业链映射

| 层级 | 公司/机构 | ECTC 2026暴露 | 收入暴露与弹性判断 |
|---|---|---|---|
| Foundry / platform | TSMC | CoWoS-R cooling/reliability；技术 symposium披露5.5-reticle、14-reticle、COUPE on substrate | 最大平台型价值捕获；会议进一步验证先进封装从服务变成平台壁垒 |
| Foundry / platform | Intel Foundry | EMIB-T、glass core、CPO glass coupler、hybrid bonding、PoINT scaling | 技术覆盖面强；商业化取决于foundry客户和执行节奏 |
| OSAT | ASE | Keynote；310 mm PLP；wafer-to-panel panel；co-design panel | 高相关；受益于PLP、AI/HPC、hyperscale需求；毛利弹性需看mix |
| OSAT | Amkor | ECTC会后称AI/HPC/photonics/advanced memory讨论强，Arizona U.S. capacity受关注 | 高相关；美国本土先进封装是差异点；2028产能节点更关键 |
| Equipment/process | Applied Materials | 450 nm hybrid bonding；300 nm SiCN；hybrid bonding process flow；Q2 FY2026 49.9% GAAP GM | 高弹性；混合键合、CMP、deposition、surface prep、metrology贯穿全流程 |
| Equipment/process | EV Group | 与AMAT/imec/Asahi Kasei/Intel多项合作；GEMINI FB等bonding生态 | 私有公司但产业指向强；可作为AMAT/BESI/TEL/ASML之外的关键设备风向标 |
| Equipment/process | ASML/TEL/BESI/SUSS/USHIO | D2W grid/overlay、W2W misalignment、large-area exposure、bond/litho co-optimization | 设备链高价值；USHIO大面积曝光是PLP/glass关键线索 |
| Materials/substrate | Resonac | 2/2 um panel damascene organic interposer、panel CMP、dry-film process | 高相关；材料+工艺方案绑定，受益早于大规模封装收入 |
| Materials/substrate | Ajinomoto/Shinko/Unimicron/Samsung Electro-Mechanics | organic substrate seminar和panel sessions | 受益于organic substrate继续作为系统连接底座；需看ultra-fine line能力 |
| Glass/optics | Corning | GlassBridge、glass waveguide、GF合作、CPO connector | 高相关但收入占总公司比例需折现；价值在高密度可维护连接器 |
| Silicon photonics | GlobalFoundries | GF Fotonix + Corning detachable fiber connector | CPO foundry暴露明确；量产收入取决于客户采用节奏 |
| Optical interconnect | Marvell/Celestial AI | Photonic Fabric chiplet；ECTC paper with Celestial/Marvell；SEC披露FY2028/FY2029收入目标 | 中长期高弹性；2026主要是design-in和验证，不是大收入年 |
| AI photonics | Lightmatter / AIST / AIM Photonics / SCINTIL | photonic-based systems special session、AOP substrate、prototype packaging | 技术指向强；私人/研究机构更多是生态验证线索 |
| Thermal | Adeia / TSMC / imec / material suppliers | direct liquid cooling、jet impingement、two-phase cooling、diamond、TIM | 需区分系统冷却和封装级热管理；封装级认证后粘性更强 |
| 伪受益或弱受益 | 普通PCB、传统低端OSAT、泛光模块厂、无TGV/无fine-line能力玻璃供应商 | 会议标题相关但技术纯度不足 | 不应因“先进封装/CPO/玻璃”标签直接上修收入或估值 |

## 风险、反证条件和后续跟踪

### 会推翻或下修本报告判断的反证

1. Hybrid bonding：2026-2027若sub-300 nm或sub-500 nm W2W无法在客户可靠性/良率中重复，或D2W overlay、die distortion、rework成本没有改善，应下修D2W chiplet放量节奏。

2. CPO：若2026-2027 OCP/hyperscaler仍偏好1.6T/3.2T pluggable、linear-drive pluggable或near-packaged optics，而非true CPO，应下修CPO收入预测，但保留玻璃耦合器/硅光封装的远期可选性。

3. PLP/glass：若320 mm/510 mm panel的2/2 um或1.5 um线宽无法在量产良率、warpage、TGV可靠性中站住，PLP/glass应从“1-2年放量”改为“2-4年工艺储备”。

4. CoWoS：若HBM供给、客户ASIC/GPU需求或AI capex下修导致CoWoS utilization低于预期，CoWoS ASP和advanced packaging利润率预期应同步下修。

5. 散热：若客户把液冷标准化成低毛利基础设施采购，且package-level direct cooling没有规模design win，应下修材料和系统冷却公司的估值弹性。

6. OSAT：若ASE/Amkor先进封装收入增长但毛利率不能持续改善，说明客户议价和折旧吞噬价值，应降低OSAT利润池权重。

### 后续跟踪节点

| 时间窗口 | 跟踪事项 | 需要看的证据 |
|---|---|---|
| 2026-06 至 2026-08 | ECTC论文后续公开视频、公司技术博客、客户访谈 | 是否出现客户名、sample qualification、yield/reliability补充数据 |
| 2026 Q2/Q3财报季 | AMAT、AMKR、ASE、MRVL、GFS、INTC、TSM、GLW | advanced packaging订单、capex、毛利、客户导入、CPO/AI packaging措辞变化 |
| 2026 H2 | HBM4/HBM4E、CoWoS扩产、CPO pilot | HBM stack数量、CoWoS产能利用率、lead time、ASP、OCP/CPO标准 |
| 2026 H2 至 2027 H1 | PLP/glass panel试产 | 310/320/510/600 mm panel良率、warpage、line/space、TGV失效率、客户design-in |
| 2027 | Celestial/Marvell、TSMC COUPE、Intel Foundry CPO | 是否从demo进入客户系统；是否出现可量化收入或采购承诺 |
| 2028 | TSMC 14-reticle CoWoS、Marvell FY2028 revenue target | 10 compute dies + 20 HBM stacks是否按期；Photonic Fabric是否达到5亿美元年化run rate |

刷新频率建议：会议后3个月每月刷新一次；2026 Q2/Q3财报后做一次公司映射更新；2026年底结合IEDM、OFC 2027预告、TSMC/Intel/Marvell/ASE/Amkor财报再做一次路线图修订。

## 来源清单

### 一手官方会议材料

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| ECTC官网首页：https://ectc.net/ | 2026-06-11检索 | 官方会议网站 | 高 | 会议日期、地点、会后record-setting描述、2027会议信息 |
| ECTC 2026 Final Program PDF：https://ectc.net/wp-content/uploads/2026/05/76-ECTCFinal-Web.v2.pdf | 2026-05 | 官方最终手册 | 高 | session、paper、keynote、plenary、panel、exhibitor、技术参数 |
| ECTC 2026 Press Kit：https://ectc.net/press/ | 2026-05-21更新 | 官方press kit | 高 | 官方高亮论文和技术tipsheet入口 |
| ECTC 2026 Technical Tipsheet PDF：https://ectc.net/wp-content/uploads/2023/03/2026-ECTC-REVISED-Technical-Tipsheet-with-images.pdf | 2026-05-20 | 官方技术tipsheet | 高 | 450 nm hybrid bonding、CPO connector、panel CMP、USHIO、CoWoS可靠性等高亮 |
| ECTC 2026 Exhibition：https://ectc.net/exhibitors/ | 2026-06-11检索 | 官方展商页 | 高 | 130+/135+展商、展览日期、展商范围 |
| ECTC 2025 Highlights：https://ectc.net/75th-ectc-highlights/ | 2025-07 | 官方会后聚合 | 中高 | 与上一届会议主题对比 |
| ECTC 2025 Final Program PDF：https://ectc.net/wp-content/uploads/2025/06/75-ECTCFinal-Web.pdf | 2025-06 | 官方手册 | 高 | 2025 CPO、glass、power delivery等基线 |

### 公司一手材料

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| ASE 310 mm panel-level packaging：https://ase.aseglobal.com/press-room/310x310/ | 2026-05 | 公司新闻稿 | 高 | ASE PLP发布、keynote、panel参与、hyperscale需求 |
| Amkor ECTC 2026 blog：https://amkor.com/blog/amkor-ectc-2026-advanced-packaging/ | 2026-06-05 | 公司会后材料 | 高 | 2700+参会者、AI/HPC/photonics/advanced memory、Arizona扩产 |
| Brewer Science ECTC 2026：https://www.brewerscience.com/news-ectc-2026/ | 2026-05-18 | 公司新闻稿 | 高 | 材料panel、laser release layer、Cu/polymer hybrid bonding |
| EV Group ECTC 2026：https://www.evgroup.com/company/news/detail/ev-group-highlights-hybrid-bonding-layer-transfer-and-maskless-lithography-technologies-for-heterogeneous-integration-and-advanced-packaging-at-ectc-2026 | 2026-05 | 公司新闻稿 | 高 | EVG与AMAT/imec/Intel合作、hybrid bonding工具生态 |
| TSMC 2026 Technology Symposium：https://pr.tsmc.com/english/news/3302 | 2026-04-23 | 公司新闻稿 | 高 | CoWoS 5.5/14 reticle、SoW-X、SoIC、COUPE |
| Marvell/Celestial AI SEC exhibit：https://www.sec.gov/Archives/edgar/data/1835632/000119312525305289/d34367dex991.htm | 2025-12 | SEC附件 | 高 | Photonic Fabric 16 Tbps、收入run-rate里程碑、交易金额 |
| GlobalFoundries/Corning collaboration：https://gf.com/news-and-events/news/globalfoundries-and-corning-collaborate-to-deliver-detachable-fiber-connector-solutions-to-scale-next-generation-optical-connectivity/ | 2025-09-29 | 公司新闻稿 | 高 | GF Fotonix与Corning GlassBridge合作 |
| Corning GlassBridge：https://www.corning.com/oem-solutions/worldwide/en/home/products-solutions/optical-communication-components/next-generation-optics/glassbridge-connector.html | 2026-06-11检索 | 产品页 | 高 | detachable fiber-to-PIC connector、wafer-based glass platform |
| Applied Materials hybrid bonding：https://www.appliedmaterials.com/us/en/semiconductor/markets-and-inflections/heterogeneous-integration/hybrid-bonding.html | 2026-06-11检索 | 产品/技术页 | 高 | hybrid bonding工艺链、AMAT与EVG/BESI合作 |
| Applied Materials Q2 FY2026 results：https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-second-quarter-2026-results | 2026-05-14 | 公司财报新闻稿 | 高 | AMAT收入、毛利率、营业利润率 |
| Intel OCI chiplet：https://newsroom.intel.com/artificial-intelligence/intel-unveils-first-integrated-optical-io-chiplet | 2024-06-26 | 公司新闻稿 | 高 | Intel CPO/OCI背景、64 x 32 Gbps、5 pJ/bit |

### 市场规模和二手研究

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| Yole via Edge AI Vision：https://www.edge-ai-vision.com/2025/09/advanced-packaging-market-set-to-reach-79-4-billion-by-2030/ | 2025-09-02 | 市场研究转载 | 中高 | advanced packaging 2024/2030规模 |
| Yole Advanced Packaging Market Monitor：https://www.yolegroup.com/product/quarterly-monitor/advanced-packaging-market-monitor/ | 2026-04 | 市场研究摘要 | 中高 | 2025 Q4/Q1 2026 advanced packaging run-rate线索 |
| Mordor CPO market：https://www.mordorintelligence.com/industry-reports/co-packaged-optics-market | 2026 | 市场研究页 | 中 | CPO 2025/2026/2031规模和CAGR |
| Mordor HBM market：https://www.mordorintelligence.com/industry-reports/high-bandwidth-memory-market | 2026 | 市场研究页 | 中 | HBM 2026/2031规模和CAGR |
| Mordor PLP market：https://www.mordorintelligence.com/industry-reports/panel-level-packaging | 2026 | 市场研究页 | 中 | PLP 2025/2026/2031、glass/2.5D CAGR |
| Mordor bonding equipment：https://www.mordorintelligence.com/industry-reports/semiconductor-bonding-equipment-market | 2026-01-16更新 | 市场研究页 | 中 | semiconductor bonding equipment 2026/2031 |
| TrendForce CoWoS：https://www.trendforce.com/news/2026/04/28/news-tsmc-cowos-wafer-asp-reportedly-nears-7nm-levels-advanced-packaging-poised-to-become-a-key-profit-driver/ | 2026-04-28 | 二手新闻/转述 | 中 | CoWoS ASP、capacity、margin方向、TSMC路线 |
| Cignal AI CPO update：https://cignal.ai/2025/02/co-packaged-optics-market-and-technology-update/ | 2025-02 | 行业分析 | 中 | CPO量产时间降权 |
| MarketsandMarkets data center liquid cooling：https://www.marketsandmarkets.com/Market-Reports/data-center-liquid-cooling-market-84374345.html | 2026 | 市场研究页 | 中 | 液冷2026/2033规模区间 |
| Grand View Research data center liquid cooling：https://www.grandviewresearch.com/industry-analysis/data-center-liquid-cooling-market-report | 2026 | 市场研究页 | 中 | 液冷2025/2026规模区间 |
| Fortune Business Insights TIM：https://www.fortunebusinessinsights.com/thermal-interface-materials-market-102950 | 2026 | 市场研究页 | 中 | 全球TIM 2025/2026/2034规模 |
| Intel Market Research semiconductor TIM：https://www.intelmarketresearch.com/semiconductor-thermal-interface-materials-market-35973 | 2026 | 市场研究页 | 中 | 半导体TIM 2025/2026/2034规模 |

### 非官方或会后分享

| 来源 | 日期 | 类型 | 可信度 | 使用方式 |
|---|---:|---|---|---|
| Semiconductor Engineering sponsor blog on Intel ECTC 2026：https://semiengineering.com/packaging-technologies-redefine-ai-and-hpc-scalability-limits-at-ectc-2026/ | 2026-06-05 | 公司赞助会后文章 | 中 | 作为Intel ECTC主题和参数补充，不单独支撑核心结论 |
| 3D InCites ECTC 2025 recap：https://www.3dincites.com/2025/06/ectc-2025-celebrates-seventy-five-years-of-pushing-the-connectivity-scale/ | 2025-06 | 会后媒体/参会记录 | 中 | 上届参会规模和主题背景 |
| LinkedIn/社交媒体参会分享 | 2026-05至2026-06 | 非官方分享 | 低 | 仅作市场情绪和“哪些paper被参会者关注”的线索，不用于核心结论 |
