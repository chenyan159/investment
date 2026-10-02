# OFC 2026 光通信大会更新：AI 光互联从模块升级进入架构重写

> 资料口径：本报告只整理外部公开资料，包括 OFC 官方新闻/会议指南、厂商 OFC 发布、市场机构公开摘要、会后行业博客和少量非官方会后观察；未参考本项目目录内既有文件。时间口径为 2026 年 OFC，即 2026 年 3 月 15-19 日在洛杉矶举行的 Optical Fiber Communication Conference and Exhibition。

## 一句话结论

OFC 2026 的最大变化不是“800G 升到 1.6T”这么简单，而是 AI 集群把光互联从一个可插拔模块采购问题，推成了系统架构问题：1.6T 已进入规模部署窗口，3.2T/400G-per-lane 已从路线图变成样机和器件验证，CPO/CPX/NPO/XPO/OCS/多 rail 传输都在回答同一个问题：如何在功耗、面板密度、可维护性、光纤数量和跨数据中心距离之间重新分配价值。

最直接的数字信号：OFC 官方预计 2026 年会议有 16,000 名参会者、90 个国家、700+ 展商、130 位 invited/tutorial speaker 和 45 场展厅剧场报告；Cignal AI 估计 2025 年光通信组件收入接近 250 亿美元，其中 datacom 超过 180 亿美元、coherent module 接近 60 亿美元；400G+ datacom 模块 2025 年出货约 4,200 万只，800G 2026 年预测超过 2,000 万只，1.6T 2026 年预测超过 500 万只；TrendForce 估计 800G 及以上模块出货占比将从 2024 年 19.5% 升到 2026 年 60%+。

## 1. OFC 2026 的重点和发展方向

### 1.1 会议本身释放的信号

- OFC 2026 官方新闻稿称展厅售罄，预计 16,000 名参会者、90 个国家、700+ 展商。会议主席的表述很直白：AI-driven growth 正在加速更高带宽和更高能效需求。
- 三个 plenary 分别来自 Coherent CTO Julie Sheridan Eng、NVIDIA AI Infrastructure SVP Alexis Bjorlin、Tesat-Spacecom CTO Siegbert Martin，基本覆盖了三个主战场：数据中心光互联、AI 网络架构、空间光通信。
- 官方 conference guide 里高频议题包括：AI data center networks、CPO integration ready for AI pipelines、interconnect latency and distributed AI training、silicon photonics modulators、photonic AI computing、hollow-core fiber、800G/1.6T validation、quantum/QKD、space optical networks。

### 1.2 与过去两年的关键转折

**第一，1.6T 从“演示产品”进入“规模供货前夜”。**  
2024-2025 年市场争论的是 800G 是否能顺利放量、1.6T 何时可用；OFC 2026 上，Coherent、Lumentum、Eoptolink、OpenLight、Broadcom、NVIDIA 生态都围绕 1.6T OSFP/DR8/2xDR4/LRO/LPO/TRO 给出产品或样机。Cignal AI 公开摘要直接给出 2026 年 1.6TbE 模块出货超过 500 万只的预测。

**第二，3.2T 的核心不再是“会不会做”，而是 400G-per-lane 的器件、DSP、封装、测试能否按成本量产。**  
Broadcom 在 OFC 发布 Taurus 400G/lane optical DSP，配套 400G EML/PD，目标是低功耗 1.6T 并铺路 3.2T；Coherent 展示 400G/lane PAM4 optical links，包括 400G differential EML 和基于纯硅 PN junction Mach-Zehnder Modulator 的 SiPh PIC；OpenLight 发布 3.2T DR8 PIC，使用 448G EAM，约 90% active element 到 silicon waveguide 耦合效率、2V 低驱动摆幅，3.2T beta 样品预计 2026 年 Q4。

**第三，CPO 不再只是 Broadcom/NVIDIA 的“未来方向”，而开始变成标准、连接器、ELS、可维护性和供应链生态。**  
NVIDIA 官方 CPO 页面给出的卖点是 5x power efficiency、10x resiliency、5x sustained application runtime，并称 Spectrum-X Ethernet Photonics 2026H2 可用，最高 409.6Tb/s；Open CPX MSA 在 OFC 前夕成立，创始成员包括 Ciena、Coherent、Marvell、Molex、Samtec、TeraHop，目标是给 CPO/NPO optical engine 定义 socket、connector、thermal、electrical、optical、management 规范。

**第四，XPO 说明“可插拔”没有死亡，而是在液冷和更大 form factor 中自救。**  
Arista 发起 XPO MSA：12.8Tbps 液冷可插拔模块，64 lanes，每模块 12.8Tbps，每 OCP rack unit 面板密度 204.8Tbps，比 1.6T OSFP 提升 4x；内置 cold plate，单模块支持最高 400W 冷却，支持 linear、half-retimed、fully-retimed 接口。这个方向的含义是：CPO 会长大，但高密度可插拔也会并行存在。

**第五，AI scale-across 把 coherent、线路系统、光纤数量重新拉回主线。**  
Marvell 发布 COLORZ 1600，号称行业首个 1.6T ZR/ZR+ pluggable，2nm Electra coherent DSP，支持 MACsec，1.6T 覆盖 campus 20km、metro 120km、regional 1,000km，2026H2 采样。Ciena 推 1600ZR/ZR+、hyper-rail photonics 和 full spectrum transponder；Nokia 推 1.6T coherent pluggable、2.4T pluggable、3.2T coherent-lite、full-band transponder、多 rail ILA。Nokia 会后总结提到 Meta 演示的区域 DCI 光纤需求：传统 regional DCI 常见 16-48 对光纤，AI-driven regional DCI 需要 128+ 对。

## 2. 会上最重要的产品和技术事实

### 2.1 1.6T：规模爆发最确定

- Cignal AI：2025 年 400G+ datacom 模块预计 4,200 万只，800GbE 预测超过 2,000 万只，1.6TbE 2026 年超过 500 万只。
- TrendForce：800G 及以上模块全球出货占比从 2024 年 19.5% 到 2026 年 60%+；Google 2026 年约 400 万颗 TPU 将带来超过 600 万只 800G+ 光模块需求，Innolight + Eoptolink 预计拿到 Google 800G+ 订单近 80%。
- Lumentum 1.6T DR4 OSFP 原型：4x400Gbps 光口、8x200Gbps host electrical interface，使用 4 颗 400G differential EML，明确作为未来 3.2T stepping stone。
- Coherent 展示多种 1.6T transceiver：SiPh PIC、高功率 InP CW laser、200G InP EML、200G GaAs VCSEL，并接入三家行业领先 DSP。
- Lumentum 已有 1.6T 2xDR4 OSFP 产品页面：8 个 212.5Gbps PAM4 electrical/optical lane，500m reach，fully retimed 版本典型功耗 22W，TRO 版本典型功耗 16W。

判断：1.6T 的爆发力度为“确定性强、价格下行也挡不住总收入增长”。2026 是导入和短缺年，2027 是供应链扩散和价格竞争年。

### 2.2 3.2T/400G-per-lane：技术拐点已出现，但量产要等

- Broadcom：Taurus 400G/lane optical DSP + 400G EML/PD，用于低功耗 1.6T，并为未来 3.2T 模块和 204.8T switching platform 铺路。
- Coherent：3.2T 用 400G/lane PAM4 光链路，路线同时包含 400G differential EML 和 silicon photonics PIC。
- OpenLight：3.2T DR8 PIC 已 alpha，bare die 立即可用；flip-chip 448G modulator + driver evaluation board 预计 2026 年 3 月底；3.2T beta 样品预计 2026 年 Q4。
- VIAVI 会后判断：3.2T 会显著增加系统和测试复杂度，预计 2027 年出现 initial live demonstrations 是较合理判断。

判断：3.2T 是 2027-2028 的主线，不应把 2026 的器件样品误解成模块大规模收入。但 400G/lane EML、EAM、MZM、DSP、测试设备会先赚钱。

### 2.3 CPO / CPX / NPO / ELS：从技术展示进入生态标准化

- NVIDIA：CPO switch 集成 silicon photonics，替代 pluggable transceiver，官方宣称 5x power efficiency、10x resiliency、5x sustained application runtime；Quantum-X800 CPO switch 支持 144 个 800Gb/s InfiniBand ports，连接超过 10,000 GPUs 的 non-blocking two-level fat-tree；Spectrum-X Ethernet Photonics 最高 409.6Tb/s，2026H2 可用。
- Coherent：6.4T socketed CPO，32x200G，基于 silicon photonics，配外部 ELS；另有 multimode socketed CPO + high-speed VCSEL，以及 400G-per-lane InP modulator array。
- Lumentum：1310nm SHP laser 在 25C 输出 >1.0W、50C 输出 >800mW，>40dB SMSR；16-channel DWDM UHP laser 用两个 ELSFP 模块输出 16 个 200GHz-spaced channels，单 channel 入纤约 24dBm，瞄准 CPO 减少 fiber count。
- Open CPX MSA：LightCounting CEO 在 MSA 发布中预计 co-packaged / near-package interfaces 未来五年 annual port shipments 超过 1 亿。

判断：CPO 的难点已经从“能不能跑”转到“能不能维护、能不能多供应商、laser/ELS 怎么冗余、field failure 怎么换”。这会让 CPX/socketed CPO/NPO 比早期全封闭 CPO 更容易被采用。

### 2.4 XPO：12.8T 液冷可插拔，延长 pluggable 生命周期

- Arista XPO MSA：12.8Tbps per module、204.8Tbps per OCP rack unit、比 1.6T OSFP 面板密度 4x、integrated cold plate 支持最高 400W/module。
- Eoptolink OFC 展示：12.8T XPO、400G/lambda 1.6T DR4、200G/lambda 1.6T FRO/LRO/LPO。
- Linktel OFC 展示：12.8T liquid-cooled XPO、200G/lane 1.6T module、400G/lane optical engines。

判断：XPO 是“可插拔阵营”的关键反击。它不会取代 1.6T OSFP 的近期放量，但可能在 204.8T switch/大规模 AI fabric 上延后 CPO 的完全替代。

### 2.5 Coherent / 1600ZR / coherent-lite：AI scale-across 的第二条主线

- Marvell：COLORZ 1600 1.6T ZR/ZR+ pluggable，Electra 2nm coherent DSP，MACsec，OSFP，C/L band；1.6T 覆盖 20km/120km/1,000km；Libra 800G ZR/ZR+ 可在 800G 1,000km、600G 2,000km、400G 3,000km。
- Ciena：2nm single-carrier 1.6Tb/s coherent 用于 1600ZR/ZR+；hyper-rail photonics 最高 32x density、128 fiber pairs/rack、功耗降低最高 75%、空间降低 85%；Vesta 200 6.4T CPX optical engine。
- Nokia：四个新 DSP + InP/SiPh optical front ends；1.6T coherent pluggable、2.4T pluggable、3.2T coherent-lite、double-sided pluggables、full-band transponders、2.4T/3.2T embedded transponders；产品族预计 2027 年中采样、2027H2 GA。
- Nokia 会后技术总结：1600ZR targeted power 约 32-35W；1600ZR+ 约 38-40W；1600CL 目标约 30W、300ns latency、20-40km reach。

判断：市场容易只看“数据中心内部 1.6T”，但 scale-across 的 coherent pluggable、line system、multi-rail amplifier、full spectrum transponder 可能是更隐蔽且更高壁垒的增量。

### 2.6 OCS / 光交换：节能极强，但会改变交换机和模块价值分配

- TrendForce 对 Google Apollo OCS 的描述：MEMS micromirror 做 fiber-to-fiber direct connection，避免多次 O-E-O 转换；单台 OCS switch 功耗约 100W，而传统交换约 3,000W，功耗降低约 95%。
- Google Ironwood TPU 架构中，短距用高速铜，rack 间用全光网络；2026 年约 400 万 TPU 对应 800G+ 模块需求超过 600 万只。

判断：OCS 可能减少部分电交换芯片/retimer 的功耗和价值占比，但会显著拉动光模块、光纤管理、MEMS/光交换、测试和运维软件价值。

## 3. 成熟和量产路线预测：基准、乐观、超预期乐观

| 方向 | OFC 2026 状态 | 基准口径 | 乐观口径 | 超预期乐观口径 |
|---|---:|---:|---:|---:|
| 800G/1.6T datacom pluggables | 800G 已主流，1.6T 多厂商样机/产品化 | 2026 年 1.6T >500 万只，2027 年 1,200-1,800 万只；800G 继续放量但 ASP 快速下行 | 2027 年 1.6T 2,000-2,500 万只，主要 hyperscaler 大比例从 800G 切 1.6T | 1.6T 在 2027 年成为新增 AI 集群默认配置，出货 3,000 万只级别，短缺延续 |
| 3.2T / 400G-per-lane | DSP、EML/EAM/MZM、PIC 样品密集出现 | 2026 样品/验证，2027 live demo/客户 qual，2028 规模化 | 2027H2 小批量收入，2028 上半年开始较大客户导入 | 204.8T switch 平台提前拉动，2027 年形成 10 亿美元级早期市场 |
| CPO / CPX / NPO / ELS | NVIDIA/Broadcom/Coherent/Lumentum/CPX MSA 明确推进 | 2026-2027 以 NVIDIA/Broadcom 和少数云厂 pilot 为主，收入先来自 ELS/optical engine | 2027 年 socketed CPO/CPX 标准稳定，多个 AI cluster 部署 | pluggable 功耗瓶颈加速暴露，CPO/CPX 在 2027 年成为高端 AI switch 的默认路线之一 |
| XPO 12.8T liquid-cooled pluggable | Arista 发起 MSA，多家模块商展示 | 2026 展示/标准化，2027 小批量验证，2028 配合 204.8T switch | 2027H2 开始在高端 AI fabric 中导入 | XPO 成为 CPO 之外的主流高密度路径，2027 年即形成 20 亿美元级需求 |
| 1600ZR/ZR+ / coherent-lite | Marvell 2026H2 采样；Ciena/Nokia 2nm coherent 路线 | 800ZR/1600ZR 2026-2027 放量，1600ZR+ 2027 后规模化 | AI scale-across 建设快于预期，coherent pluggable 增速 40%+ | campus/metro AI DCI 爆发，coherent-lite 进入数据中心内部长距互联 |
| OCS / optical switching | Google Apollo 进入体系化讨论 | Google/少数自研 TPU 云厂优先采用，2026-2027 市场小但拉动模块 | Meta/Microsoft/Anthropic 相关集群跟进，OCS 成为 TPU-like cluster 标配 | GPU Ethernet fabric 也广泛吸收 OCS，电交换扩容路径被部分重写 |
| Multi-rail ILA / FST / hyper-rail | Nokia/Ciena 明确推多光纤/整 band/整 fiber pair | AI regional DCI 从 wavelength 部署转向 fiber-pair 部署，2026H2 起订单增长 | 128+ fiber pairs/rack 级需求成为大型 AI region 标配 | 线路系统成为 AI capex 的新瓶颈，放大 Ciena/Nokia/Cisco/Corning/Senko 价值 |
| Test & measurement | VIAVI/Keysight 等 1.6T/3.2T 验证平台受益 | 1.6T MAC/FEC/224G SerDes 测试 2026 高景气，3.2T 2027 接棒 | 供应商扩产和客户 qual 并行，测试设备增速 40%+ | 400G/lane 难度超预期，测试/验证成为卡点和高利润环节 |

## 4. 重要产品和技术的市场规模、增速、利润率

说明：公开市场机构通常给“整体光模块/光组件/datacom/coherent/CPO”的数字，很少把 1.6T、XPO、OCS、ELS 拆成完全独立口径。下面“已公开数字”直接引用公开资料；“测算”是基于公开出货、ASP、供应链利润率和 OFC 发布节奏的估算。

| 产品/技术 | 当前市场规模（美元） | 关键事实 | 未来一年收入增速：基准 / 乐观 / 超预期 | 当前利润率与未来方向 |
|---|---:|---|---:|---|
| 全部 optical transceiver | 2025 年约 238 亿美元（LightCounting） | AI datacenter 拉动 Q4 2025 供应商收入超预期；产能追上后 2026 年末可能价格竞争加剧 | +20-30% / +30-45% / +50%+ | 领先模块/器件商 gross margin 约 30-40%+；代工 EMS 约 12%。基准：ASP 下行使利润率小幅下滑；乐观：高端 mix 抵消降价；超预期：短缺延续，利润率上修 |
| Datacom optical components / 400G+ datacom modules | 2025 年 datacom optical component >180 亿美元；400G+ 单季收入已 >50 亿美元 | Cignal：2025 年 400G+ 模块 4,200 万只；datacom optical component 2024-2029 CAGR 20%+，2029 近 290-300 亿美元 | +30-40% / +45-60% / +70% | 800G/1.6T 领先供应商 gross margin 约 30-42%；Fabrinet 这类 EMS non-GAAP GM 约 12.4%。2026H1 强，2026H2 需防 ASP 加速下行 |
| 1.6T pluggable modules | 2026E 约 70-100 亿美元（测算：>500 万只 x $1,400-2,000 ASP） | Cignal 明确 2026 年 1.6TbE >500 万只；Coherent/Lumentum/Eoptolink/OpenLight 等 OFC 集中展示 | +80-120% / +120-180% / +200%+ | 早期 gross margin 可达 35-45%；随着中国/北美多供应商扩散，2027 年 ASP 压力明显。短缺环节是 200G/400G EML、SiPh PIC、DSP、isolator/filter、测试产能 |
| 3.2T / 400G-per-lane modules & engines | 2026 年商业收入 <2 亿美元（测算，主要样品/评估板/测试） | Broadcom Taurus、Coherent 400G/lane、OpenLight 448G EAM；OpenLight 3.2T beta Q4 2026 | 2027 年 +200% 但基数低 / 形成 10-20 亿美元早期市场 / 2027 年 30 亿美元+ | 模块利润率暂不可稳定测；稀缺器件和 DSP 毛利高，module 端会被良率和测试时间压制 |
| CPO / CPX / NPO / ELS | CPO 2026 年约 1.6 亿美元，2031 年约 7.5 亿美元，CAGR 35.92%（Mordor） | NVIDIA 2026H2 Spectrum-X Photonics；Open CPX MSA；Coherent 6.4T socketed CPO；Lumentum 高功率 ELS | +50-80% / +100-150% / +200-300% | ELS/laser/optical engine gross margin 可高于传统模块；但 CPO 系统早期 NRE、可靠性、服务成本高。利润率方向取决于是否形成多供应商标准 |
| XPO 12.8T liquid-cooled pluggable | 2026 年 <1 亿美元（测算，基本是样品/开发） | Arista MSA：12.8T per module、204.8T per OCP RU、4x OSFP density、400W cooling | 2027 年 2-5 亿 / 5-15 亿 / 20 亿+ | 早期 ASP 和毛利率高，但液冷、可靠性、field service 会吃掉部分利润；标准成熟后毛利率回落 |
| Coherent pluggables / DCI optics | 2025 年 coherent module 接近 60 亿美元（Cignal） | Marvell 1.6T ZR/ZR+ 2nm DSP 2026H2 采样；Ciena/Nokia 推 1600ZR/ZR+、coherent-lite、full-band | +20-35% / +35-50% / +60%+ | DSP/高端 coherent module 毛利通常高于普通 datacom module；未来一年 mix 向 800ZR/1600ZR 倾斜，利润率稳中有升 |
| OCS / optical circuit switching | 2026 年独立硬件约 2-6 亿美元（测算；Google 生态为主） | TrendForce：OCS 单机约 100W vs 传统 switch 约 3,000W，功耗 -95%；Google 2026 年 800G+ 模块需求 >600 万只 | +50% / +100% / +200% | MEMS/OCS 硬件 gross margin 约 35-50%（测算）。如果被云厂自研压价，利润在模块和系统集成侧分散 |
| Multi-rail ILA / hyper-rail / FST | AI scale-across 相关 dedicated DCI/line system 为低个位数十亿美元（测算） | Ciena：hyper-rail 32x density、-75% power、-85% space；Nokia：multi-rail ILA 160 fiber pairs/rack，2026H2 可用 | +20-30% / +40-60% / +80% | 系统厂 gross margin 多在 35-45% 区间；功耗/空间节省使客户愿意付溢价，短期利润率优于传统传输设备 |
| 高速测试与验证 | 2026 年约 5-10 亿美元（测算，1.6T/224G SerDes/3.2T 驱动） | VIAVI 1.6T TestCenter D2、ONE-1600ER 支持 1.6TE MAC、2x800GE、4x400GE、8x200GE、FEC、224G SerDes | +30-50% / +60% / +80%+ | 测试设备 gross margin 通常高，且 400G/lane 复杂度提升会延长高景气 |

## 5. 与市场主流认知可能相违背的洞见

### 5.1 CPO 会爆发，但不会马上杀死 pluggable

市场容易把 CPO 叙事讲成“pluggable 被淘汰”。OFC 2026 反而显示 pluggable 在进化：1.6T OSFP 继续规模化，XPO 用 12.8T + 液冷 + 400W cooling 把 pluggable 推向更高密度；CPX/socketed CPO 也在借鉴 pluggable 的可维护性。更可能的路线是：OSFP 负责近期主流，XPO 负责高密度过渡，CPO/CPX 负责功耗极限和高端 switch。

### 5.2 1.6T 不是单一技术路线的胜利

Coherent 同时展示 SiPh、InP、VCSEL；Lumentum 强调 400G differential EML；OpenLight 是 III-V integrated SiPh；Broadcom 用 EML/PD + DSP 推 400G/lane。结论：2026-2027 年不会只有“硅光赢”或“EML 赢”，而是不同 reach、功耗、成本、良率和客户偏好下多技术并行。

### 5.3 价格战可能比需求放缓更早出现

LightCounting 的公开摘要提醒：光芯片和 transceiver 产能正在追上需求，2026 年末可能带来更激烈竞争和更快价格下行。也就是说，即使 AI 光模块需求继续强，个别模块厂毛利率也可能在 2026H2-2027 面临 ASP 压力。

### 5.4 AI scale-across 可能比市场想象中更快放大 coherent 和线路系统

投资者常盯数据中心内部短距模块，但大型 AI region 的瓶颈在 campus/metro/regional DCI、光纤对数、放大站空间和功耗。Ciena/Nokia 的 hyper-rail、multi-rail ILA、FST 不是传统电信小修小补，而是在给 AI 区域网络做“整 fiber pair / 整 band”部署。

### 5.5 OCS 是光模块需求放大器，不只是交换机替代品

Google Apollo OCS 100W vs 3,000W 的功耗差距非常大，但 OCS 架构也要求 AI 集群一开始就配置足够 800G/1.6T 光模块。若 OCS 扩散，电交换芯片/retimer 的某些价值会被压缩，但光模块、fiber management、MEMS switch、测试和运维软件会受益。

### 5.6 3.2T 不能按“2026 大量出货”定价

OFC 上 3.2T 信号很强，但多是 400G/lane link、PIC、DSP、evaluation board、alpha/beta sample。合理节奏是 2026H2 客户 qual、2027 live demo/小批量、2028 才真正扩产。短期更可兑现的是 400G/lane 的上游器件、DSP、测试。

### 5.7 HCF 已经从科学展示走到低延迟网络候选，但商业化仍慢

Nokia 会后总结提到 hollow-core fiber state-of-the-art loss 已到 0.04dB/km。HCF 对低延迟 DCI、金融、分布式 AI 训练有吸引力，但连接器、部署成本、可维护性和供应链还会限制其近两年收入。

### 5.8 供应链瓶颈比“模块组装能力”更细

真正的瓶颈集中在：200G/400G EML/EAM/MZM、InP laser/PD、高功率 ELS、isolator/filter、3nm/2nm DSP、224G/448G SerDes、液冷封装、high-density connector、fiber management、测试时间。只看“谁能组装 OSFP”会漏掉利润更高、更难扩产的环节。

## 6. 产业链受益顺序和风险

### 6.1 优先受益环节

1. 高速光模块：800G 继续放量，1.6T 在 2026-2027 接棒；代表方向包括 Innolight、Eoptolink、Coherent、Lumentum、NVIDIA 自有/生态模块。
2. 光芯片和激光器：200G/400G EML、InP CW laser、ELSFP、VCSEL、SiPh PIC、III-V integrated SiPh，是 1.6T/3.2T/CPO 共用瓶颈。
3. DSP/SerDes/retimer/AEC：Broadcom Taurus、Marvell 2nm coherent DSP、200G lane retimer、PCIe Gen6/以太网 retimer；但 CPO/OCS 会在部分场景减少 retimer/DSP 价值。
4. CPO/CPX/XPO 连接和热管理：Samtec、Molex、TE、Amphenol、Senko、Corning、液冷 cold plate 和高密度光纤管理。
5. Coherent DCI 和 line system：Ciena、Nokia、Cisco/Acacia、Marvell 在 scale-across 中更受益。
6. 测试设备：VIAVI、Keysight 等受益于 1.6T MAC/FEC、224G SerDes、400G/lane 和 3.2T 验证复杂度提升。

### 6.2 主要风险

- 2026 年末产能追上后，800G/1.6T ASP 下行可能快于预期。
- CPO/CPX 的 field service、laser redundancy、thermal drift、可靠性验证时间可能拖慢客户量产。
- XPO/CPX/OCI/OIF 等标准并行，可能带来 form factor 分裂和库存风险。
- AI 数据中心电力/液冷/土地/并网约束会让光互联订单出现季度波动。
- 中美供应链和客户认证风险会影响中国模块厂份额和估值。
- 3.2T 过早资本化容易踩节奏：器件先于模块，模块先于交换机平台，交换机平台先于大规模集群部署。

## 7. 资料来源

- [OFC 官方新闻：OFC 2026 opens with sold-out exhibition](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-opens-next-week-in-los-angeles-with-sold-out-exhibition-as-ai-driven-network-demand-fuels/)
- [OFC 2026 Conference Guide PDF](https://ofc-web-afd-e8csdte4dubnfvfu.z02.azurefd.net/ofc/media/images/documents/2026/2026ofc_conference_guide.pdf)
- [OFC 官方新闻：AI-era data centers and networks exhibit](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-exhibit-connects-the-global-optical-ecosystem-powering-ai-era-data-centers-and-networks/)
- [NVIDIA Silicon Photonics](https://www.nvidia.com/en-in/networking/products/silicon-photonics/)
- [Broadcom OFC 2026 AI infrastructure release](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai)
- [Coherent 1.6T/3.2T/XPO OFC 2026 release](https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026)
- [Coherent CPO OFC 2026 release](https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026)
- [Lumentum OFC 2026 release](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx)
- [Marvell COLORZ 1600 / 2nm coherent DSP release](https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html)
- [Ciena OFC 2026 AI networking release](https://www.ciena.com/about/newsroom/press-releases/ciena-brings-ai-networking-expertise-to-ofc-2026)
- [Ciena high-speed connectivity innovations release](https://www.ciena.com/about/newsroom/press-releases/ciena-solidifies-ai-networking-leadership-unveils-new-innovations-for-high-speed-connectivity)
- [Nokia AI-era optical solutions release](https://www.nokia.com/newsroom/nokia-launches-suite-of-applicationoptimized-optical-solutions-for-ai-era-networks/)
- [Nokia OFC 2026 takeaways](https://www.nokia.com/blog/ofc-2026-takeaways-pluggables-multi-rail-hcf-and-ai/)
- [Arista XPO MSA release](https://www.arista.com/en/company/news/press-release/23697-pr-20260311)
- [Open CPX MSA](https://www.opencpxmsa.org/)
- [Eoptolink 12.8T XPO release](https://www.eoptolink.com/news/13-new-products/364-eoptolink-joins-xpo-msa-and-unveils-industry-first-12-8-tbps-liquid-cooled-pluggable-optics-for-ai-data-centers)
- [OpenLight 3.2T DR8 PIC release](https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants)
- [TrendForce: Google 800G+ and OCS architecture](https://www.trendforce.com/presscenter/news/20260210-12919.html)
- [Cignal AI: optical component revenue nearly $25B in 2025](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/)
- [Mordor / GlobeNewswire: CPO market 2026-2031](https://www.globenewswire.com/news-release/2026/01/29/3228606/0/en/Co-Packaged-Optics-Market-Growing-at-35-92-CAGR-to-Reach-USD-0-75-Billion-by-2031-Reports-Mordor-Intelligence.html)
- [LightCounting: optical transceiver sales reached $23.8B in 2025](https://www.lightcounting.com/newsletter/en/march-2026-quarterly-market-update-380)
- [VIAVI: OFC 2026 1.6T going mainstream and 3.2T emergence](https://blog.viavisolutions.com/2026/04/23/ofc-2026-1-6t-going-mainstream-the-emergence-of-3-2t/)
