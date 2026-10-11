# CICC 2026会议追踪：核心变化、产品爆发和市场预期差

> 会议对象：2026 IEEE Custom Integrated Circuits Conference, CICC 2026  
> 官方会议日期：2026-04-19 至 2026-04-22；CHISIC 2026为2026-04-22至2026-04-23；Internet of Bodies Workshop为2026-04-19  
> 官方会议地点：Hyatt at Olive 8, Seattle, WA, USA。用户提示中的 San Jose 与会议官网和公开议程不一致，本稿按官方地点 Seattle 处理。  
> 材料检索截止日期：2026-06-11  
> 报告完成日期：2026-06-11  
> 资料边界：本稿未使用项目内旧报告、索引、缓存或中间结论；只使用会议官网、公开议程/API、标准组织材料、公司公告和公开市场资料。CICC不是OFC式产品展会，论文更偏电路和系统原型；因此会议证据用于判断技术路线和瓶颈，订单、收入和利润池判断需由公司披露和产业数据交叉验证。

## 结论摘要

1. CICC 2026最重要的变化不是“又多了几个AI芯片论文”，而是AI计算系统的主瓶颈明显从单颗算力阵列外溢到供电、封装、die-to-die互连、光/电I/O、3DIC验证、可靠性和热管理。公开议程包含95个事件、187篇公开论文标题/track；论文数量最高的track是RF/mmWave 31篇、Power Management 27篇、Digital/SoC 25篇、Data Converters 22篇，说明会议仍是电路会议，但AI系统约束已经横向渗透。

2. 未来3个月最可交易的不是CICC论文里的实验芯片，而是已经进入公司财报和客户导入叙事的环节：AI optical transceiver、800G/1.6T光互连、custom AI ASIC/AI networking、48V/60V AI服务器供电、3DIC/EDA签核、UCIe/SerDes IP。Broadcom在2026-06-03披露FY2026 Q2收入221.87亿美元、AI半导体收入108亿美元、Q3 AI半导体收入预期160亿美元；Marvell在2026-05-27披露FY2027 Q1收入24.18亿美元，并把增长归因于800G/1.6T optics、51.2T Ethernet switch、NPO/CPO、custom XPU等。

3. 未来1年，CICC 2026最值得跟踪的“放量路线”是四条：48-60V intermediate bus converter和vertical power delivery；UCIe 32/48/64GT/s与短距XSR/Die-to-Die PHY；1.6T光模块、CPO/NPO和硅光子/薄膜铌酸锂驱动；2.5D/3D chiplet的multi-physics signoff、test、thermal和reliability。CICC给出的参数已经到可工程化区间，例如48-60V至0.8-1V 120A转换器、3001W/in3 IBC、0.57pJ/bit UCIe D2D、256Gb/s TFLN driver、100Gb/s burst-mode optical receiver、HBM接口10.7mV droop/1.4ns settling。

4. 未来2年，真正改变利润池的是“系统级协同设计”而非单点器件。价值捕获更可能流向：高端switch/ASIC/DSP厂商、EDA/IP/verification、先进封装和基板、供电模块与高电流密度电源器件、光电芯片和关键激光器。纯光模块装配、只会讲CPO概念但没有客户认证的公司、只展示TOPS/W但缺软件栈和客户工作负载的边缘AI/CIM公司，收入弹性可能被市场高估。

5. 最大反共识：CPO不是2026年利润池主战场。第三方模型口径下，2026年CPO市场约1.65亿美元，而TrendForce估计2026年AI-focused optical transceiver市场约260亿美元。也就是说，2026年可兑现的钱大部分仍在800G/1.6T pluggable、LPO/NPO/CPO准备链条、DSP/retimer/switch silicon、激光器和封装测试，而不是“CPO纯概念”本身。

6. 第二个反共识：AI服务器供电可能比光互连更容易在2026年体现为订单和毛利改善。Vicor在2026-04-21披露Q1收入1.13亿美元、毛利率55.2%、backlog 3.01亿美元，同比+75%、环比+70%；其表述指向高性能计算、自动测试设备、工业/航天国防和VPD power system。MPS在2025年实现收入27.90亿美元，非GAAP毛利率55.5%，并披露数据中心AI、server、memory、optical modules和switch power solution客户扩张。CICC Session 16的论文参数强化了这一判断。

## 会议重点和方向变化

| 主题 | 会议证据 | 公司/组织映射 | 关键参数和数字 | 变化性质 | 证据强度 |
|---|---|---|---|---|---|
| AI-era芯片设计和EDA自动化 | Keynote “Generative AI and Agentic AI for Chip Design”；CHISIC含Siemens 3DIC flow、Synopsys-Ansys multiphysics、Cadence/Secure-IC供应链透明度 | NVIDIA、Synopsys、Cadence、Siemens EDA、Ansys、Secure-IC | SEMI/ESD Alliance披露Q4 2025 ESD收入54.663亿美元，同比+10.3%；SIP收入20.832亿美元，同比+18.3% | AI从“被设计的芯片”进入“设计芯片的工具链”；3DIC使EDA从布局布线扩展到EMIR、thermal、mechanical、reliability | 高 |
| Chiplet/UCIe/3DIC | CHISIC 2026专门围绕chiplet/heterogeneous integration；Session 30为HPC Chiplet Systems；Session 19含UCIe D2D PHY | Intel、AMD、IBM、GlobalFoundries、Altera、NVIDIA、Synopsys、Cadence、Siemens、TSMC、ASE、Amkor | UCIe 3.0支持48/64GT/s；CICC 19-7展示32Gb/s/lane、0.83Tb/s/mm、25mm standard package、0.57pJ/bit量级D2D link；CHISIC含UCIe recent advancements和scale AI chiplet interfaces | 从“能不能做chiplet”转向“能否低成本、可测试、可互操作、可签核地规模部署” | 高 |
| AI compute power | Educational Session 1和Session 16 Compute Power；CHISIC含Vertical Power Delivery | Vicor、MPS、TI、ADI、Infineon、Renesas、onsemi、Murata、Delta/Lite-On、NVIDIA/AMD平台链 | 48-60V IBC达到3001W/in3；120A 48-60V至0.8-1V转换器；HBM接口供电抖动抑制10.7mV droop、1.4ns settling；VPD 5-8V至0.8-1.2V仅20mV undershoot | AI服务器功耗和电流密度使板级/封装级供电成为可见瓶颈；从传统VRM转向更高输入电压、分布式、垂直供电和本地LDO | 高 |
| 光互连、CPO/NPO和高速wireline | Educational Session 3；Session 12 High-speed Wireline；Session 19 High-performance Optical Transceivers and Die-to-die Interface；CHISIC silicon photonics keynote和100x reach optical panel | Broadcom、Marvell、Credo、Coherent、Lumentum、Intel、NVIDIA、ADI、TFLN/硅光子供应链、Fabrinet | 157Gb/s/mm、1.55pJ/bit PAM4；56Gb/s/wire、0.75pJ/b D2D；50GBaud+ VCSEL CPO；100Gb/s burst-mode optical receiver；256Gb/s TFLN modulator driver | 2026的收入在800G/1.6T和DSP/switch/laser，CPO是下一阶段架构选项；会议强调功耗、density、reach和packaging共优化 | 高 |
| PIM/CIM和边缘AI加速 | Session 9 Panel “GPU vs PIM”；Session 15 ML Accelerator；Session 22 sensing/media/AI；Session 33 CIM | Google共同作者、大学/研究机构、edge AI ASIC/IP、EDA/IP公司；公开上市纯受益标的少 | 64.5TFLOPS/W training accelerator、69.2TOPS/W continual learning、11.16uJ/token SLM decoder、53.3TFLOPS/W FlashMLA/LLM decoding CIM、92.5TOPS/W analog CIM | 能效数字亮眼，但大多仍是原型/论文阶段；缺客户模型、编译器、内存容量、可靠性和软件生态验证 | 中 |
| THz/mmWave/RF、Data Converter和IoB | RF/mmWave为最大track 31篇；Data Converter 22篇；IoB workshop和biomedical session | Apple/手机链、ADI、TI、Qualcomm、NXP、IBM、医疗/可穿戴芯片链 | mmWave/RF和ADC/DAC论文数量高；IoB强调neurotechnology、BMI/BCI、wearable/implantable sensing | 产业意义长期存在，但2026-2027股票弹性弱于AI互连/供电/EDA；更适合寻找IP、仪器、传感和医疗认证节点 | 中 |

### 和过去6-12个月预期相比的变化

1. 市场此前更关注GPU、HBM、CoWoS和800G/1.6T光模块本身；CICC 2026把“电源完整性、热、可靠性、D2D、signoff、test”提升为同等重要的系统瓶颈。Session 16的HBM供电抖动论文尤其说明，HBM带宽不只是内存供给问题，也受本地供电、droop、settling、strobe触发LDO和local replica regulator约束。

2. Chiplet路线从“架构叙事”进入“工程闭环”阶段。UCIe 3.0在2025-09公开48/64GT/s、100mm sideband reach、runtime recalibration和continuous transmission支持；CICC/CHISIC在2026-04展示32Gb/s/lane实测D2D、UCIe教程、multi-physics工具和test/reliability内容。变化不是单纯速率提升，而是从PHY到管理、测试、封装和可靠性的完整链条补齐。

3. 光互连出现分层：2026年的确定性在800G/1.6T pluggable、LPO/NPO/CPO准备链条和switch/ASIC/DSP；CPO仍是小市场和中长期架构选择。CICC材料支持“最终要靠更短电链路和更近光引擎降功耗”的方向，但还不能直接推出CPO大规模收入已经到来。

4. PIM/CIM的市场预期需要降温。GPU vs PIM被放进panel，本身说明它仍是争议议题；CIM论文参数非常激进，但多数是28nm/65nm研究原型，离客户主工作负载、软件栈、良率和可靠性还远。短期股票研究不应把TOPS/W直接映射成收入。

## 产品和技术路线三情景预测

> 口径说明：市场规模为美元口径。官方公司披露使用披露日期；第三方市场模型使用报告/新闻发布日期；未有直接披露的细分市场以底稿估算标注“估算”。三情景为未来一年，即大致2026年中至2027年中。

| 产品/技术方向 | 当前成熟度（2026-06-11） | 2026当前规模/口径 | 基准情景：未来一年 | 乐观情景：未来一年 | 超预期乐观情景：未来一年 | 利润率和价值捕获 |
|---|---|---:|---:|---:|---:|---|
| 48-60V AI compute power、IBC、VPD、HBM本地供电 | CICC有多篇原型；Vicor/MPS等公司层面已有AI server/HPC相关收入和backlog；客户认证通常以平台代际推进 | 估算AI服务器板级/封装级供电半导体和模块约20-35亿美元，不含数据中心设施电力；假设300-500万AI accelerator/server board等效出货、每等效单元400-700美元供电BOM | 规模26-44亿美元，+25%-35%；48V rack和更高电流密度平台继续渗透，但多供应商价格竞争 | 规模32-55亿美元，+45%-60%；VPD/高密度模块在新一代GPU/XPU平台快速导入 | 规模45-70亿美元，+80%+；若客户为避免供电瓶颈接受高ASP模块和授权/IP模式，毛利扩张 | 模块/控制器/功率级/磁性件赚钱；毛利率可在45%-60%区间，领先模块厂可能更高；风险是客户自研和第二供压价 |
| UCIe/D2D PHY、XSR SerDes、chiplet interface IP | 标准成熟到UCIe 3.0；CICC有32Gb/s/lane、25mm organic package公开实测；48/64GT/s进入IP/验证/客户设计阶段 | 半导体IP大盘Q4 2025 run-rate约83亿美元/年；D2D/SerDes/chiplet interface相关IP和测试估算6-12亿美元 | 7.5-16亿美元，+25%-35%；主要由ASIC、switch、accelerator、FPGA平台设计导入拉动 | 9-20亿美元，+50%上下；UCIe 64GT/s IP被主流AI ASIC和chiplet平台采用 | 12-24亿美元，+80%-100%；若organic/substrate封装可替代部分昂贵interposer并快速多源化 | IP授权和EDA验证毛利最高；PHY silicon/retimer毛利低于纯IP但收入更大；测试认证和compliance工具被低估 |
| 3DIC/2.5D advanced packaging、multi-physics EDA/signoff | 已规模用于AI/HBM/CoWoS类产品；CICC/CHISIC强调STCO、EMIR、thermal、mechanical、test/reliability | 第三方模型差异较大：2025 advanced packaging约417-516亿美元，2026约500-575亿美元；高端AI相关部分占比较小但增速更高 | 560-640亿美元，+9%-12%；高端先进封装仍受基板、HBM、封装产能约束 | 630-700亿美元，+15%-20%；2.5D/3D、hybrid bonding、silicon bridge和fan-out AI需求超预期 | 720亿美元以上，+25%+；若GPU/ASIC平台扩张且先进封装产能未过剩，价格和利用率维持高位 | Foundry/OSAT/基板/设备分享大收入；EDA/IP的增量毛利更高；封装产能资本开支重，周期反转风险高 |
| 800G/1.6T光模块、LPO/NPO/CPO、硅光子/TFLN | 800G/1.6T进入规模放量；NPO/CPO处于客户验证和早期部署；CICC支持VCSEL CPO、TFLN driver、burst receiver、DWDM clock-forward optical link等技术储备 | TrendForce 2026 AI-focused optical transceiver约260亿美元，2025为165亿美元；Mordor估算2026 CPO仅1.65亿美元 | AI光模块300-330亿美元，+15%-25%；CPO 2.5-3.5亿美元，仍小；1.6T设计定点决定份额 | AI光模块360-420亿美元，+40%-60%；CPO 4-6亿美元；EML/CW laser、alignment、packaging测试偏紧 | AI光模块450亿美元以上；CPO 8-10亿美元；若hyperscaler快速标准化CPO/NPO，switch silicon和光引擎协同放量 | 光模块装配毛利通常低于DSP/switch/laser/IP；高毛利更可能在Broadcom/Marvell等switch/DSP/custom ASIC、关键激光器和硅光子平台 |
| CIM/PIM/边缘LLM/SLM加速器 | 多数为研究芯片/样品；论文指标强，但产品化依赖软件栈、模型稳定性、内存容量、客户场景 | 商业CIM/PIM专用推理收入估算低于1-3亿美元；广义edge AI silicon大很多但不可等同 | 2-5亿美元，主要为IP、小批量和垂直场景；渗透率低 | 5-10亿美元，若SLM/视觉/机器人场景形成标准工作负载 | 10-20亿美元，需大客户把特定模型/算子固化到硬件并接受生态锁定 | 纯IP毛利高但收入小；芯片毛利受软件支持和客户集中度拖累；短期更像技术期权 |
| IoB/biomedical/wearable ultra-low-power SoC | IoB workshop和biomedical session证明研发活跃；受医疗认证和产品周期约束 | 与CICC直接相关的可穿戴/植入式感知芯片市场估算5-15亿美元；广义医疗电子不纳入 | +10%-20%；以低功耗AFE、wireless、sensing SoC小幅增长为主 | +30%左右；若BCI/神经接口或连续健康监测应用获得监管/客户节点 | +50%+，需要明确FDA/临床/平台级design win | 医疗认证壁垒高，单位利润可好，但周期长；更适合跟踪ADI/TI/MedTech客户链而非会议热点交易 |

## 市场规模和利润池

### 1. AI光互连：大市场在1.6T和光模块，CPO仍是期权

截至2026-04-20，TrendForce估计AI-focused optical transceiver市场从2025年165亿美元增至2026年260亿美元，增速约57%。其瓶颈指向EML、CW laser、光对准、功耗和热管理，并认为2026-2027年是1.6T供应链站位窗口。这个口径和CICC Session 19高度一致：会议不是在证明“光互连会增长”，而是在展示下一轮降功耗、提密度、缩短电链路、提高reach所需的电路和封装能力。

CPO的收入口径必须降权。Mordor 2026模型估算CPO市场仅1.6476亿美元，2031年7.6432亿美元，CAGR 35.92%。即使使用更乐观口径，2026年CPO仍远小于AI光模块大盘。结论：2026年更应买“已经进入订单和客户认证的800G/1.6T、DSP/switch silicon、关键激光器和封装测试”，而不是只买“CPO概念”。

价值捕获排序：switch ASIC/custom ASIC/DSP > 关键激光器/光芯片 > 硅光子foundry/封装平台 > 高良率模块封测 > 普通模块装配。普通模块厂可能收入增长快，但毛利率未必扩张；CPO如果由switch/ASIC厂商主导，独立模块厂反而可能被挤压。

### 2. AI compute power：从板级BOM小项变成系统瓶颈

CICC 2026 Session 16展示的参数组合值得重视：48-60V IBC、120A低压输出、高功率密度、VPD、HBM电源噪声抑制、本地数字LDO和快速瞬态恢复。这些论文对应的不是传统“电源管理小芯片”逻辑，而是AI服务器功率密度提升后的系统瓶颈。

Vicor 2026-04-21 Q1披露显示：收入1.13亿美元，同比+20.2%；毛利率55.2%；backlog 3.01亿美元，同比+75%、环比+70%；管理层提到高性能计算、自动测试、工业/航天国防等需求和VPD power system。MPS 2025披露收入27.90亿美元、非GAAP毛利率55.5%，并称数据中心客户覆盖AI、server、memory、optical modules和switch power。两者说明AI供电已经不是纯论文方向，而是可在订单、backlog、毛利率和产能计划里观察。

利润池判断：短期最赚钱的是高电流密度模块、控制器、DrMOS/功率级、磁性器件和系统级参考设计；中期会向封装内/封装背面供电、integrated passives、VPD和客户定制模块迁移。风险是大客户自研、第二供应商导入、专利/诉讼、以及传统模拟大厂用规模压价。

### 3. Chiplet/UCIe/3DIC：真正赚钱的不是“chiplet”三个字，而是可验证、可测试、可量产

UCIe Consortium在2025-09发布的UCIe 3.0支持48/64GT/s、100mm sideband reach、continuous transmission、runtime recalibration和更强manageability。CICC 19-7给出32Gb/s/lane、0.83Tb/s/mm、25mm standard package的UCIe-compliant D2D link，说明在标准封装/有机基板上做长一点reach、低一点能耗是重要方向。CHISIC 2026则把UCIe教程、3DIC设计流、thermal/power integrity、chiplet supply-chain transparency和test/reliability放在一起，显示产业瓶颈从单点PHY扩大到完整生态。

先进封装市场第三方模型差异很大：Grand View Research估计2025年advanced packaging约417亿美元、2033年660亿美元；Mordor估计2025年516亿美元、2026年575亿美元、2031年901亿美元；Yole口径显示2030年可达约794亿美元。口径差异来自是否包含广义先进封装、2.5D/3D、fan-out、embedded die和高端AI/HBM部分。对股票研究更重要的是：AI高端封装部分增速高于大盘，但资本开支和客户集中度也更高。

价值捕获排序：高端foundry/OSAT/基板/设备拿收入，EDA/IP/verification拿高毛利，测试认证和reliability工具是低估环节。长期看，如果UCIe和开放chiplet生态成熟，模块化设计会降低定制ASIC门槛，但也会把更多利润转移到接口IP、EDA签核和先进封装平台。

### 4. EDA/IP：AI设计工具和3DIC signoff的利润弹性被低估

SEMI/ESD Alliance在2026-04-13披露，Q4 2025 ESD收入54.663亿美元，同比+10.3%；SIP收入20.832亿美元，同比+18.3%；CAE收入18.874亿美元，同比+9.4%。如果按Q4 run-rate年化，ESD约219亿美元、SIP约83亿美元。CICC/CHISIC的变化是把EDA需求从传统IC设计扩到3DIC系统级：netlist creation、3DSTACK verification、EMIR、thermal、mechanical、reliability、chiplet provenance、security和test。

Synopsys、Cadence、Siemens EDA的长期利润池不只是“AI帮助写RTL”，而是“AI芯片复杂性迫使客户采购更多系统级签核、IP和multi-physics flow”。这类收入增速未必像光模块一样爆发，但毛利率、续费属性和客户粘性更好。

### 5. PIM/CIM：技术强，商业化证据弱

CICC 2026的CIM/PIM论文参数非常强：28nm 53.3TFLOPS/W LLM decoding CIM、92.5TOPS/W analog CIM、68.22TOPS/W eDRAM digital CIM、64.5TFLOPS/W 16nm AI training accelerator等。但这些数字不能直接变成市场规模。需要补齐的问题包括：模型精度、算子覆盖、compiler、memory hierarchy、良率、可测性、错误恢复、热、软件生态、客户是否愿意为固定硬件修改模型。

投资判断：CIM/PIM更像2年期技术期权，而不是2026年主利润池。可跟踪大学/研究机构成果、Google/Meta/NVIDIA/AMD是否将相关架构吸收进平台、以及EDA/内存/IP公司是否出现实际design win。没有客户工作负载和软件栈验证前，不应按GPU替代逻辑估值。

## 反共识洞见和重要更新

### 被市场低估的方向

1. AI电源完整性比“电源管理芯片”标签重要。CICC 16-6把HBM接口抖动、droop和settling直接连到本地LDO和replica regulator；这意味着HBM/AI accelerator性能释放不仅取决于HBM供给和先进封装，也取决于封装级/本地供电质量。跟踪指标：新GPU/XPU平台的48V/VPD设计、每颗加速器电源模块ASP、供电模块交期、Vicor/MPS/TI/ADI/Infineon相关订单。

2. UCIe在有机封装上的reach和能耗值得高看。25mm standard package、32Gb/s/lane、0.57pJ/bit级别的公开论文参数说明，部分chiplet互连未必只能依赖昂贵硅中介层。若后续量产验证通过，会改变高端封装成本曲线，并给D2D PHY/IP、substrate、test和EDA带来价值。

3. 3DIC multi-physics和test/reliability是“卖铲子”环节。CHISIC把Siemens、Synopsys-Ansys、Cadence/Secure-IC和NXP reliability/test放在核心议程，说明规模化chiplet的痛点不在“论文能不能跑”，而在全生命周期可验证、可追责、可测试、可修复。

4. 光互连的瓶颈不只在模块厂。TrendForce明确指出EML、CW laser、光对准、功耗和热是2026扩产瓶颈；CICC/CHISIC又把硅光子、TFLN driver、DWDM、CPO、100x reach optical放在一起。因此上游光芯片、激光器、封装测试和switch/DSP可能比普通模块装配更有利润弹性。

### 被市场过度乐观的方向

1. CPO近端收入被高估。2026年CPO市场模型仅约1-2亿美元量级，而AI-focused optical transceiver是260亿美元量级。即使CPO技术方向正确，2026年股票业绩更可能由800G/1.6T、LPO/NPO准备、DSP/switch silicon和关键光芯片驱动。

2. PIM/CIM被“TOPS/W幻觉”高估。论文指标没有覆盖客户模型、软件栈、可靠性、可测性、内存容量和系统集成成本。若后续没有大型客户公开design win或可复现的主流LLM/SLM workload，应该把PIM/CIM从主线机会降为技术观察项。

3. 只靠“AI data center”标签的公司未必受益。供电公司若没有高电流密度、封装级供电、客户认证和IP壁垒；光模块厂若没有关键激光器/光芯片/DSP能力；封装公司若只在低端封装而非高端2.5D/3D/HBM供应链，收入暴露和利润弹性都可能弱于叙事。

### 立即下修判断的反证条件

1. Broadcom/Marvell后续两个季度AI semiconductor、800G/1.6T、custom XPU、CPO/NPO相关订单或指引明显低于2026年6月披露的高增长预期。

2. Vicor/MPS等AI服务器供电公司backlog、book-to-bill或毛利率转弱，说明高密度供电没有形成持续瓶颈或客户第二供应压价快于预期。

3. UCIe 48/64GT/s量产IP认证延后，或32/40GT/s D2D在真实package、温度、电压、BER、可靠性条件下无法复现会议论文指标。

4. 1.6T光模块LTAs和激光器扩产没有兑现，EML/CW laser供给从短缺快速转为过剩，导致模块ASP和毛利率提前下行。

5. CICC/CHISIC展示的3DIC工具链不能转化为EDA订单、IP attach和客户signoff预算，说明复杂性增加没有变成商业化工具收入。

## 公司和产业链映射

| 层级 | 代表公司/组织 | 收入暴露 | 投资弹性 | CICC 2026关联判断 |
|---|---|---|---|---|
| AI custom ASIC / switch / DSP / networking | Broadcom、Marvell、NVIDIA、AMD、Intel | 高：Broadcom FY2026 Q2 AI半导体108亿美元；Marvell FY2027 Q1披露800G/1.6T、51.2T switch、NPO/CPO、custom XPU需求 | 高，但估值和预期也高 | 最直接承接光互连、D2D、custom silicon和AI networking利润池 |
| EDA/IP/verification | Synopsys、Cadence、Siemens EDA、Ansys、UCIe生态IP厂商 | 高：SEMI Q4 2025 ESD 54.663亿美元、SIP 20.832亿美元 | 中高，收入弹性慢但毛利和粘性强 | Agentic AI for chip design、3DIC flow、multi-physics、chiplet security/test是明确会议主线 |
| AI服务器供电 | Vicor、MPS、TI、ADI、Infineon、Renesas、onsemi、Murata | 中高：Vicor backlog 3.01亿美元；MPS 2025收入27.90亿美元且数据中心电源客户扩张 | 高，尤其是高电流密度模块和VPD | Session 16是本届最具短中期产业映射的技术session之一 |
| 光互连/光芯片/模块 | Coherent、Lumentum、Credo、Broadcom、Marvell、Fabrinet、AOI、Intel硅光子链 | 高：TrendForce估2026 AI optical transceiver 260亿美元 | 高但分化；普通装配利润可能被挤压 | CICC强化VCSEL CPO、TFLN driver、DWDM、burst receiver和D2D互连 |
| 先进封装/基板/OSAT/foundry | TSMC、Intel Foundry、Samsung、GlobalFoundries、ASE、Amkor、Ibiden、Unimicron、Shinko | 高，但资本开支重 | 中高；取决于高端AI/HBM产能利用率 | CHISIC把advanced packaging、STCO、thermal、test和reliability放到中心 |
| 测试认证/仪器 | Keysight、Teradyne、Advantest、FormFactor、UCIe compliance生态 | 中 | 中高，容易被主流叙事忽视 | UCIe/3DIC/chiplet规模化会提升测试、KGD、package reliability需求 |
| PIM/CIM/edge AI IP | 学术机构、Google共同作者、部分AI ASIC/IP创业公司 | 低到中；多数还非上市或未规模收入 | 高波动、长周期 | 技术期权，不宜作为2026主线收入判断 |
| 伪受益或弱受益 | 低端光模块装配、普通电源供应、没有高端封装能力的封装厂、只靠AI关键词的边缘AI芯片 | 低或不确定 | 容易被叙事放大 | 需要逐项核收入暴露、客户认证、毛利率和产能瓶颈 |

## 风险、反证条件和后续跟踪

### 后续3个月跟踪

1. 公司财报：Broadcom FY2026 Q3、Marvell FY2027 Q2、MPS/Vicor Q2 2026、Synopsys/Cadence最新EDA/IP订单、Coherent/Lumentum/Credo光互连订单和毛利率。刷新频率：每次财报后。

2. 1.6T光链：EML/CW laser扩产、LTAs、模块ASP、交期、客户认证数量、800G到1.6T切换比例。刷新频率：月度或重点公司公告后。

3. AI供电链：48V rack、VPD、IBC、高电流密度模块design win、供电模块ASP、backlog、客户第二供应导入。刷新频率：财报和客户平台发布后。

4. UCIe/Chiplet：UCIe 3.0 IP发布、64GT/s PHY认证、compliance workshop、真实package BER/功耗/距离数据。刷新频率：标准组织和EDA/IP公司发布后。

### 未来1年跟踪

1. Hot Chips 2026、OCP Global Summit 2026、SC26、OFC 2027、ISSCC 2027。重点看：AI accelerator平台是否明确采用新一代D2D/光互连/供电方案。

2. 客户侧反证：hyperscaler capex、AI服务器出货、GPU/ASIC平台节奏、交换机51.2T/102.4T迁移、CPO/NPO是否被列入采购规范。

3. 产业链利润率：模块厂和光芯片厂毛利是否扩张；电源模块厂毛利是否维持；EDA/IP是否出现AI/3DIC价格提升或seat expansion。

### 未来2年跟踪

1. CPO是否从小规模部署进入标准化采购，还是持续被LPO/NPO/更高效pluggable挤压。

2. UCIe是否真正打开多厂商chiplet市场，还是仍停留在大厂内部封闭生态。

3. PIM/CIM是否出现主流客户工作负载和软件栈锁定；若没有，应继续降权。

4. 先进封装供需是否从短缺变成阶段性过剩；若过剩，封装端利润率下修，但EDA/IP和测试需求可能仍维持。

## 来源清单

### 一手官方会议材料

| 来源 | 日期/访问日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| IEEE CICC 2026官网，https://www.ieee-cicc.org/ | 访问：2026-06-11 | 会议官网 | 高 | 会议日期、地点、venue、CHISIC日期、赞助商和会议定位 |
| CICC 2026 Technical Program，https://www.ieee-cicc.org/technicalprogram/ | 访问：2026-06-11 | 官方技术项目说明 | 高 | 说明CICC论文是技术论文，不是产品营销材料；online proceedings仅注册参会者可用 |
| CICC 2026 ExOrdo公开论文API，https://cicc2026.exordo.com/api/papers?limit=999 | 访问：2026-06-11 | 官方议程后端公开API | 高 | 187篇论文、track数量、Session 12/15/16/19/22/30/33公开标题和技术参数 |
| CICC 2026 ExOrdo公开日程API，https://cicc2026.exordo.com/api/schedule_events?limit=999 | 访问：2026-06-11 | 官方议程后端公开API | 高 | 95个日程事件、session和workshop安排 |
| CHISIC 2026页面，https://www.ieee-cicc.org/chisic/ | 访问：2026-06-11 | 官方workshop页面 | 高 | CHISIC 2026为chiplet/heterogeneous integration workshop |
| CHISIC 2026 PDF，https://www.ieee-cicc.org/wp-content/uploads/2026/02/CHISIC-2026-promo-Full-v6.pdf | 发布/访问：2026-02/2026-06-11 | 官方PDF | 高 | CHISIC议程、3DIC、UCIe、silicon photonics、VPD、chiplet security和test主题 |
| Internet of Bodies Workshop 2026，https://www.ieee-cicc.org/iob/ | 访问：2026-06-11 | 官方workshop页面 | 中高 | IoB/biomedical方向覆盖范围 |

### 标准组织和技术材料

| 来源 | 日期/访问日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| UCIe Specifications，https://www.uciexpress.org/specifications | 访问：2026-06-11 | 标准组织 | 高 | UCIe 1.0/1.1/2.0/3.0功能、48/64GT/s、100mm sideband、manageability |
| UCIe 3.0 blog，https://www.uciexpress.org/post/ucie-3-0-specification-redefining-chiplet-interconnects | 发布：2025-09-03；访问：2026-06-11 | 标准组织说明 | 高 | UCIe 3.0公开发布时间、速率和应用方向 |

### 公司一手材料

| 来源 | 日期/访问日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| Broadcom FY2026 Q2 results，https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial | 发布：2026-06-03 | 公司财报新闻稿 | 高 | FY2026 Q2收入221.87亿美元、AI半导体108亿美元、Q3 AI半导体160亿美元预期 |
| Marvell FY2027 Q1 results，https://investor.marvell.com/news-events/press-releases/detail/1023/marvell-technology-inc-reports-first-quarter-of-fiscal-year-2027-financial-results | 发布：2026-05-27 | 公司财报新闻稿 | 高 | FY2027 Q1收入24.18亿美元、Q2收入27亿美元指引、800G/1.6T、51.2T switch、NPO/CPO和custom XPU叙事 |
| Vicor Q1 2026 results，https://vicorcorporation.gcs-web.com/news-releases/news-release-details/vicor-corporation-reports-results-first-quarter-ended-march-13 | 发布：2026-04-21 | 公司财报新闻稿 | 高 | Q1收入1.13亿美元、毛利率55.2%、backlog 3.01亿美元、VPD/高性能计算需求 |
| Monolithic Power Systems FY2025/Q4 2025 SEC Exhibit，https://www.sec.gov/Archives/edgar/data/1280452/000143774926003191/ex_886152.htm | 发布：2026-02-05 | SEC附件/公司业绩说明 | 高 | 2025收入27.90亿美元、非GAAP毛利率55.5%、数据中心/AI/server/memory/optical/switch power solution客户扩张 |

### 市场规模和二手研究

| 来源 | 日期/访问日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| SEMI/ESD Alliance EDMD Q4 2025，https://www.semi.org/en/semi-press-release/esd-alliance-reports-electronic-system-design-industry-posts-5.5-billion-dollars-in-revenue-in-q4-2025 | 发布：2026-04-13 | 行业协会数据 | 高 | ESD、SIP、CAE市场规模和增速 |
| TrendForce AI optical transceiver report，https://www.trendforce.com/presscenter/news/20260420-13017.html | 发布：2026-04-20 | 二手产业研究 | 中高 | 2025/2026 AI optical transceiver市场、供应瓶颈和1.6T窗口 |
| Mordor Co-Packaged Optics Market，https://www.mordorintelligence.com/industry-reports/co-packaged-optics-market | 访问：2026-06-11 | 第三方市场模型 | 中 | CPO 2025/2026/2031市场规模和CAGR，作为量级判断 |
| Grand View Research Advanced Packaging Market，https://www.grandviewresearch.com/industry-analysis/advanced-packaging-market-report | 访问：2026-06-11 | 第三方市场模型 | 中 | advanced packaging 2025/2033市场规模 |
| Mordor Advanced Packaging Market，https://www.mordorintelligence.com/industry-reports/advanced-packaging-market | 访问：2026-06-11 | 第三方市场模型 | 中 | advanced packaging 2025/2026/2031市场规模，作为情景区间上沿 |
| Yole advanced packaging press release，https://www.yolegroup.com/press-release/advanced-packaging-market-set-to-reach-79-4-billion-by-2030/ | 发布：2025-08；访问：2026-06-11 | 第三方市场模型 | 中 | advanced packaging到2030年量级交叉验证 |

### 非官方材料和置信度说明

本轮检索未发现足以支撑核心结论的高质量公开参会者长文、工程师会后笔记或公开视频访谈。社交媒体和二手媒体只作为市场情绪背景，未单独支撑任何核心判断。所有市场规模中，会议/标准/公司披露为高置信度；第三方市场模型为中等置信度；本文自建细分市场估算为中低置信度，已在表格中标注“估算”和假设链条。
