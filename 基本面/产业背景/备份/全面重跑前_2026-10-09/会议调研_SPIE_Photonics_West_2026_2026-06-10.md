# SPIE Photonics West 2026会议追踪：核心变化、产品爆发和市场预期差

会议日期：2026-01-17 至 2026-01-22  
会议地点：Moscone Center, San Francisco, CA, USA  
材料检索截止日期：2026-06-10（America/Los_Angeles）  
报告完成日期：2026-06-10（America/Los_Angeles；对应 UTC 日期约为 2026-06-11）  
研究边界：本报告为独立会议追踪底稿，只使用公开会议、公司、技术和二手市场资料；未读取或继承项目内旧报告、索引、缓存或中间结论。

## 结论摘要

1. SPIE Photonics West 2026 的最大变化不是某一个单点产品，而是“光子技术从展示性能进入量产工程约束”。官方会后信息显示，本届会议有超过 23,000 名注册参会者、来自 40 个国家，约 1,600 家展商，4,200 场技术报告，100 个 conference，49 门课程，覆盖 Photonics West、BiOS、Quantum West、AR | VR | MR 和首届 Vision Tech 五个 expo。SPIE 同期发布的行业数据称，2024 年全球 optics and photonics core components 生产收入达到 3,810 亿美元，同比 +10%。这给会议结论定了基调：光子产业不是小众科研赛道，而是大制造链条，但投资机会集中在少数量产瓶颈。

2. 最强产业信号来自 CPO/PIC/硅光，不是“CPO 已经大规模出货”，而是“热、测、封装、仿真、外置光源、wafer/die 级测试”开始成为显性利润池。Coherent 在会期发布 bondable diamond，宣称可将热界面电阻降低最高 99%、适配最大 100 mm square die；Quantifi Photonics 在 2026-01-21 发布 PXI ELSFP 外置连续波光源，8 通道、1311 nm、最高 25 dBm/channel、面向 CPO/PIC 量产测试；AIM Photonics 披露 300 mm silicon photonics 微环调制器和自动 EO/RF 测试方法。判断：未来 12 个月真正受益的不是泛“硅光概念”，而是 CPO 可靠性、外置激光、生产测试、PIC 封装和热材料。

3. AR | VR | MR 的会议重心明显从“FOV/亮度 demo”转向“高折射率材料、TiOx 刻蚀、波导量产、光学计量、镜片集成和防水/处方适配”。Tokyo Electron 展示 AR 波导 TiOx etch、ALD TiO2、高折射率 grating 的 wafer-scale fab tool 议题；Pixelligent 讨论 n~2.0 纳米材料；Dispelix 讨论与 AAC 的下一代 AR device 能力和 metrology 从 fab lab 到 fab；Tobii 展示 lens casting，把光学元件、电子、处方支持和 ingress protection 集成进轻薄镜片。判断：AR 光学链条在 2026 年仍是客户验证/小批量阶段，最大预期差是“市场容易高估整机放量速度，低估材料、检测和良率工具的价值”。

4. 工业激光的关键更新是高亮度和应用端工艺窗口，而不是单纯功率堆叠。IPG Photonics 的 YLR-8000-SM 获 Prism Lasers 奖，核心参数是 8 kW compact single-mode、M2 < 1.1；Coherent 同场展示 266 nm picosecond DUV laser + DUV optics、CO2 EOM for via drilling、Sapphire XT compact visible laser。判断：2026-2027 年工业激光总盘子温和增长，但高亮度单模、半导体/显示精密加工、PCB via drilling、激光功率/能量计量会比通用切割焊接更有利润弹性。

5. BiOS/生命科学方向的反共识点是：广义 biophotonics 市场数字很大，2026 年公开二手研究口径约 940 亿至 1,020 亿美元，但会议里可投的短期利润池并不在“所有医疗光学”，而在 OCT specialty fiber assemblies、regulated OEM photonic modules、point-of-care photonic diagnostics、手术/成像设备组件和可制造检测。Coherent、G&H、Helix Surgical、DoseOptics、Ramona Optics 等材料显示，真实放量受 FDA/CE、临床数据、报销和 OEM 设计周期约束，12 个月内更像高毛利小品类，而不是平台级爆发。

6. Vision Tech 首次加入 Photonics West 是被低估的结构变化。机器视觉、3D sensing、hyperspectral、SPAD/InGaAs APD、metasurface imaging、wafer-level spectral image sensors 同时出现，说明 photonics 正在进入制造、机器人、汽车、生命科学和农业的“感知层”。短期更确定的盈利环节是工业相机、3D ToF/LiDAR 传感、InGaAs APD、wafer-level spectral sensor、检测软件和校准，不是所有“AI 视觉”。

7. Quantum West 的投资含义应降温处理。会议证据支持的是 quantum clocks、quantum sensors、quantum entropy/security、SiN/photonic platform、低温/光学仪器和供应链 readiness；不支持把 2026 年视为 fault-tolerant quantum computing 大规模收入拐点。Coherent/Quside 的 6-inch VCSEL quantum entropy demo 和 TOPTICA TOPTICLOCK Prism 奖更像“量产光子平台嵌入安全/计量功能”的早期信号。

8. 最大机会：CPO/PIC 测试与封装、外置激光源、热材料、AR 波导制造与计量、工业高亮度激光、InGaAs/SPAD/ToF 传感、BiOS regulated modules。最大分歧：CPO 大规模部署时间、AR display glasses 出货、医疗光子设备监管周期、工业激光价格战。最大风险：市场把会议展示误读为客户订单，把可制造性 demo 误读为规模交付。

## 会议重点和方向变化

### 1. CPO/PIC/硅光：从“带宽叙事”进入“系统工程叙事”

| 会议信号 | 公司/机构 | 参数和材料日期 | 变化性质 | 投资含义 |
|---|---:|---:|---|---|
| CPO 讨论从光学性能转向热、测试、仿真、封装和可靠性 | Coherent、Quantifi Photonics、AIM Photonics、Ansys/Synopsys、Ayar Labs、BAE、Tesla、Imec、PHIX | 2026-01-19 至 2026-01-27 | 真实变化，但仍处 pilot/qualification | 价值捕获从“模块 ASP”扩散到外置激光、测试仪器、热界面材料、PIC 封装、仿真软件 |
| Bondable diamond 热管理 | Coherent | 2026-01-19；最高降低热界面电阻 99%；die 尺寸最高 100 mm square；适配 Si/SiC/GaN/AlGaN/GaAs/InP | 产品发布，客户协作中 | 若 CPO/AI accelerator 热密度继续上升，diamond/ceramic/advanced thermal interface 会成为小而贵的瓶颈品 |
| PXI ELSFP 外置激光源 | Quantifi Photonics（Teradyne 旗下） | 2026-01-21；8 channels；1311 nm；最高 25/23/20 dBm per channel；ELSFP Power Class 6 future-proof | 产品发布，直接面向 CPO/PIC DVT 和高容量制造测试 | 高通道数测试是 CPO 放量的前置 capex，毛利率可能高于模块本体 |
| 300 mm silicon photonics 微环与测试 | AIM Photonics | 2026-01-19/21；8 V heater；trenched modulator resonance shift 约 13.7 nm，non-trenched 约 1.7 nm；300 mm CMOS-compatible EO/RF test | 技术一手材料 | 300 mm 制程和 wafer/die 自动测试是从 MPW/prototype 走向量产的必要条件 |
| 5 GHz spectral control | Coherent Waveshaper 1000A Sharp | 2026-01-20；5 GHz FWHM | 产品展示 | CPO、量子、精密测试的共同工具层，单品市场小但高毛利 |

和过去 6-12 个月预期相比，2025 年市场更容易把硅光等同于 800G/1.6T 光模块和 AI 数据中心流量；Photonics West 2026 的增量是把“系统级可部署”问题摆到台前：外置 CW laser、热界面、可靠性、批量测试、simulation workflow。该变化已有产品发布和具体参数支撑，但还缺少明确 hyperscaler 规模订单披露。因此结论是“进入工程化前夜”，不是“CPO 已经全面替代 pluggable”。

### 2. AR | VR | MR：从光学架构竞赛转向可制造性

| 会议信号 | 公司/机构 | 参数和材料日期 | 变化性质 | 投资含义 |
|---|---:|---:|---|---|
| AR | VR | MR conference 聚焦下一代 smart glasses/HMD 的 optics、display、sensors | SPIE、Tokyo Electron | 2026-01-19 至 2026-01-22 | 会议主线 | 光学硬件仍是智能眼镜从无显示 AI glasses 走向 display glasses 的核心瓶颈 |
| TiOx etch、TiO2 ALD、高折射率 grating wafer-scale tools | Tokyo Electron | 2026-01-19、20、22 | 半导体设备链介入 AR 波导制造 | AR 波导从光学设计走向半导体工艺，TEL 等设备商收入弹性较小但技术地位重要 |
| n~2.0 nanomaterials for XR | Pixelligent | 2026-01-20；Booth #6611 | 材料一手线索 | 高折射率低损耗材料是轻薄波导/FOV/亮度平衡的瓶颈 |
| Dispelix + AAC 下一代 AR device 能力、AR/VR metrology 从 fab lab 到 fab | Dispelix | 2026-01-21、22；Booth #6514 | 产业协同和计量能力线索 | 波导制造的量产难点在良率、均匀性、检测，而不是单片 demo |
| Lens casting 集成光学、电气、处方、防水 | Tobii | 2026-01-20 至 2026-01-22；Booth #6332 | 样品/原型展示 | 智能眼镜真实量产会把光学供应链和眼镜供应链合并，低估镜片集成环节可能错过价值 |

判断：2026 年 AR 光学链条更像“设计 win + 工艺认证 + 小批量”而不是整机百万级 display waveguide 确定放量。非官方参会分享倾向认为 SPIE AR/VR/MR 参会内容主要集中在 optical see-through head-worn displays，会议规模也在扩张；该线索与官方和公司材料方向一致，但仍应低于一手材料权重。

### 3. 工业激光和半导体/显示精密加工：高亮度、短脉冲、计量进入主线

| 会议信号 | 公司/机构 | 参数和材料日期 | 变化性质 | 投资含义 |
|---|---:|---:|---|---|
| 8 kW compact single-mode fiber laser | IPG Photonics YLR-8000-SM | 2026 Prism Lasers winner；M2 < 1.1 | 商业化产品获奖 | 高亮度单模可打开更精细切割、焊接、远程加工和新材料应用；但通用工业激光仍面临价格竞争 |
| DUV film cutting and semi-cap display process | Coherent | 266 nm picosecond DUV laser + DUV optics；2026-01-20 | 产品 demo | 半导体/显示加工对波长、脉宽、光学材料和可靠性要求高，利润率通常优于普通切割 |
| CO2 EOM for via drilling | Coherent | Germanium-free high-power beam switching；2026-01-20 | 产品公告 | PCB via drilling 和先进封装/电子制造中的 throughput 工艺窗口 |
| 1 kHz pulse energy handheld meter | Coherent FieldMax Touch Pro | 2026-01-20 | 生产计量 | 激光装备放量时，计量/校准/安全设备同步受益 |
| 70 kW ultra-high-power laser sensor | MKS Ophir | Photonics Spectra 2026 product list；Booth #927 | 展商产品线索 | 超高功率激光普及推动功率计、热管理和保护光学件需求 |

工业激光市场的反共识：会议热点不是“所有激光公司复苏”，而是“更高亮度、更高工艺确定性、更强计量闭环”的子品类。若中国供应链继续压低通用光纤激光价格，IPG、Coherent、nLIGHT、MKS/Ophir 的相对优势应来自难替代应用，而不是低端功率堆叠。

### 4. BiOS 和医疗/生命科学：临床部署能力比科研新颖性更值钱

| 会议信号 | 公司/机构 | 参数和材料日期 | 变化性质 | 投资含义 |
|---|---:|---:|---|---|
| OCT specialty fiber assemblies | Coherent | 2026-01-20；OCT/NIRS/multimodal catheter imaging | 产品公告 | 高价值临床应用需要可靠 fiber assemblies，OEM 导入周期长但粘性高 |
| Regulated OEM photonic modules、OCT、point-of-care | G&H | 2026-01；BiOS Expo 2026-01-17/18；Photonics West 2026-01-20/22 | 公司一手展示 | 生命科学收入暴露更靠近 OEM module/system integration，不是单一科研器件 |
| Biophotonic Instruments Prism | Helix Surgical Rx、DoseOptics BeamSite、Ramona Optics Vireo | 2025-11 finalists；2026-01 winner Helix Surgical Rx | 商业化产品线索 | 手术、剂量/成像、显微成像可能形成小市场高毛利，但受监管和临床 adoption 限制 |

广义 biophotonics 市场口径很大，公开研究给出 2026 年约 940 亿至 1,020 亿美元区间；但会议可映射到股票的短期收入，主要是 photonic OEM module、光源、探测器、光纤组件、OCT 子系统、医学成像仪器和检测服务。报告估算 2026 年与会议高相关的“可捕获组件/模块池”为 60 亿至 100 亿美元，未来 12 个月基准增速约 8%-12%。

### 5. Vision Tech、机器视觉和 3D sensing：感知层成为新增 audience

| 会议信号 | 公司/机构 | 参数和材料日期 | 变化性质 | 投资含义 |
|---|---:|---:|---|---|
| 首届 Vision Tech Expo | SPIE | 2026-01；应用覆盖制造、汽车、生命科学、农业、机器人 | 会议结构变化 | photonics 正在进入工业 AI 的传感输入层 |
| Polar ID | Metalenz | 2026 Prism Cameras and Imaging Systems winner | metasurface/polarization imaging 商业化线索 | wafer-level optics + sensor fusion 可能压低 3D/身份识别硬件体积和成本 |
| Stella-2 | NAMUGA + Lumotive | 2026 Prism Sensors finalist | sensor/beam-steering 线索 | 固态 beam steering/programmable optics 用于机器人、智能基础设施 |
| Aura Noiseless InGaAs APD | Phlux Technology | 2026 Prism Sensors winner | 近红外探测器线索 | InGaAs APD 是 lidar、量子、通信和生命科学的上游瓶颈之一 |
| Wafer-level spectral image sensors | imec | 2026-01-20 Vision Tech stage | wafer-level spectral imaging | 光谱成像若从科研相机进入工业 wafer-level sensor，BOM 和出货弹性会显著变化 |

判断：机器视觉不是一个单一市场，利润池分为工业相机/镜头、照明、传感器、3D ToF/LiDAR、hyperspectral、软件算法和系统集成。2026 年可交易线索集中在 sensor、InGaAs/SPAD、wafer-level optics、校准/测试和工业自动化客户导入，而不是泛 AI 图像算法。

### 6. Quantum West：真实收入在仪器、传感、安全和平台，不在 2026 年通用量子计算

| 会议信号 | 公司/机构 | 参数和材料日期 | 变化性质 | 投资含义 |
|---|---:|---:|---|---|
| VCSEL quantum entropy source | Coherent + Quside | 2026-01-20；6-inch VCSEL manufacturing；runtime entropy verification；development kits | 一手 demo | 量子安全可以借成熟 VCSEL 平台嵌入 mainstream hardware，短期商业化概率高于量子计算整机 |
| TOPTICLOCK | TOPTICA | 2026 Prism Quantum Tech winner | 商业化产品 | 精密时钟/频率/激光源是 quantum sensing/computing 的卖铲人 |
| Integrated photonic technologies for quantum systems | imec、G&H | 2026-01-21；SiN photonics、quantum supply chain panel | 平台和供应链 | 规模化需要标准化光子平台、封装和供应链 readiness |

判断：2026-2027 年 quantum photonics 的可投资落点是激光源、探测器、时钟、entropy/security、SiN/PIC platform、低温/光学仪器和封装服务。若后续公司只讲“量子计算 TAM”而无 instrument/order/revenue，会议材料不足以支持高估值。

## 产品和技术路线三情景预测

说明：下表为“会议材料 + 公开二手市场口径 + 本报告估算”的投资底稿，不是公司指引。市场规模均为美元口径，数据日期以 2026-06-10 检索到的公开资料和材料发布日期为准。置信度：高=有一手材料和可交叉验证市场口径；中=有一手产品但市场口径需估算；低=早期赛道或市场定义差异大。

| 方向 | 2026 当前规模口径 | 成熟度 | 3 个月节点 | 1 年基准 | 1 年乐观 | 1 年超预期乐观 | 2 年判断 | 利润率和价值捕获 |
|---|---:|---|---|---:|---:|---:|---|---|
| CPO/PIC/硅光 AI interconnect | Silicon photonics 公开口径约 23 亿至 40 亿美元；若叠加 PIC test/package/外置激光，本报告估 35 亿至 55 亿美元 | pluggable 量产、CPO pilot/qualification、PIC test 扩产 | 关注 OFC 后订单、hyperscaler qualification、ELSFP adoption | 45 亿至 70 亿美元，+25%-35% | 70 亿至 90 亿美元，+50%-70% | 90 亿至 120 亿美元，+90% 以上 | 2028 年若 CPO 在 AI switch/accelerator 进入生产集群，测试和热材料先于 CPO 模块利润释放 | 模块 GM 25%-40%；测试/外置激光 GM 50%-65%；热材料 GM 40%-60%；价值捕获：测试、packaging、external laser、thermal interface、foundry/IP |
| CPO/PIC 量产测试和外置光源 | 本报告估 4 亿至 7 亿美元；Quantifi ELSFP 属于新增高密度测试子类 | 产品发布，客户验证/生产导入前期 | 看 PXI ELSFP 设计 win、Teradyne/Keysight/Coherent optical test 动向 | 6 亿至 10 亿美元，+35%-45% | 10 亿至 14 亿美元，+70%-100% | 15 亿至 20 亿美元，+150% | 高通道数 CPO 测试可能成为 2027 年最早兑现的 CPO capex | 仪器 GM 55%-70%；价值捕获：ATE、laser source、probe/alignment、calibration software |
| Bondable diamond/先进热材料 | 目标可寻址市场估 2 亿至 5 亿美元； broader electronics thermal management 远大于此 | 产品发布，客户联合开发 | 看 reliability、bonding process、AI GPU/optical engine 设计采纳 | 3 亿至 7 亿美元，+30%-50% | 6 亿至 10 亿美元，+80%-120% | 10 亿至 15 亿美元，+150% 以上 | 若 high-power ASIC + CPO 同封装加速，diamond/ceramic 从 niche 变为必选热层 | 材料 GM 40%-60%；价值捕获：diamond growth、surface finishing、bonding/coating know-how |
| AR waveguide/optical stack | Smart glasses 公开口径 2026 约 32 亿美元；本报告估 display optics/waveguide/light-engine 相关 6 亿至 10 亿美元 | 客户验证、小批量、设计 win | 看 OEM 2026 H2 产品路线图、waveguide yield、metrology adoption | 9 亿至 14 亿美元，+35%-45% | 15 亿至 22 亿美元，+80%-120% | 25 亿至 35 亿美元，+200% | 2028 年若消费 OEM 放量，材料/波导/计量先吃利润；若整机延后，工具商仍有研发/小批量收入 | 波导/材料 GM 30%-60%；设备/计量 GM 45%-65%；价值捕获：high-index materials、nanoimprint/etch、metrology、prescription integration |
| 高亮度单模 fiber laser 和 semicap 精密激光 | 工业激光系统公开口径 2026 约 65 亿美元；fiber laser 2025 约 63 亿至 76 亿美元；高亮度/semicap 子类估 8 亿至 15 亿美元 | 商业化产品，小批量到量产 | 看 IPG 8 kW 单模订单、semicap/display DUV 需求、PCB via drilling | 子类 9 亿至 17 亿美元，+10%-15% | 12 亿至 22 亿美元，+25%-40% | 18 亿至 30 亿美元，+70% | 通用激光价格战持续，高端工艺窗口更抗压 | 高端 lasers GM 35%-50%；低端受中国价格战压缩；价值捕获：laser source、optics、power/energy metrology、process IP |
| Vision/3D sensing/hyperspectral | Machine vision 公开口径 2025/26 约 158 亿至 261 亿美元；3D sensors 2026 约 78 亿美元；hyperspectral 2026 约 3 亿至 9 亿美元 | 工业视觉量产，3D/hyperspectral 分化 | 看 Vision Tech 后产品 design-in、机器人/汽车/工厂客户 | 相关 photonics hardware 估 30 亿至 45 亿美元，+10%-18% | 45 亿至 60 亿美元，+25%-35% | 65 亿至 85 亿美元，+60% | wafer-level optics 和 spectral sensors 若进入工业规模，会重估小型传感器公司 | Sensors GM 35%-60%；系统 GM 25%-45%；价值捕获：InGaAs/SPAD、metasurface optics、illumination、calibration/software |
| Biophotonics/OCT/regulated photonic modules | 广义 biophotonics 2026 约 940 亿至 1,020 亿美元；会议高相关组件/模块估 60 亿至 100 亿美元 | regulated OEM，小批量到量产 | 看 FDA/CE、OEM design-in、临床/报销节点 | 65 亿至 112 亿美元，+8%-12% | 75 亿至 130 亿美元，+18%-25% | 90 亿至 160 亿美元，+40% | 2 年内高端 OCT、catheter imaging、point-of-care photonic diagnostics 更清晰 | OEM modules GM 40%-55%；系统集成 25%-45%；价值捕获：光纤组件、探测器、激光源、regulated manufacturing |
| Quantum photonics/security/sensors | Quantum photonics 公开口径 2026 约 7 亿至 11 亿美元；quantum sensors 2026 约 5 亿至 9 亿美元 | 仪器/传感/安全商业早期，QC 远期 | 看 VCSEL entropy kit adoption、clock/sensor orders、政府项目 | 12 亿至 18 亿美元，+25%-40% | 18 亿至 25 亿美元，+60%-90% | 30 亿美元以上，政府/安全客户加速 | 2028 年前更像 instrument/component market，不是通用量子计算大收入 | Instruments GM 50%-70%；价值捕获：激光源、detectors、SiN/PIC、clock、QRNG/security chips |

## 市场规模和利润池

### 1. 光子产业总盘子：大市场，小瓶颈

SPIE 在 2026-01-19 Global Business Forum 发布的行业数据称，2024 年全球 optics and photonics core components 年收入为 3,810 亿美元，同比 +10%。这个数字说明 Photonics West 不是单纯学术会议，但股票研究必须避免把 3,810 亿美元直接套到单一技术主题上。会议新增信息集中在以下 7 个利润池：

1. CPO/PIC 工程化利润池：外置激光、wafer/die test、alignment、packaging、thermal、simulation。
2. AR 光学制造利润池：high-index materials、TiOx/TiO2 工艺、nanoimprint、waveguide metrology、lens casting。
3. 高端工业/semicap 激光利润池：8 kW 单模、高功率 CO2 EOM、266 nm DUV、功率/能量计量。
4. 生物医疗 OEM photonic modules：OCT/NIRS/catheter imaging、point-of-care、regulated production。
5. Vision sensing：metasurface imaging、InGaAs APD、SPAD/ToF、hyperspectral、wafer-level spectral sensors。
6. Quantum instrumentation/security：clock、laser、QRNG/entropy、SiN/PIC、sensors。
7. 软件和仿真：CPO、AR waveguide、metrology workflow 里的 design/verification layer。

### 2. 当前市场规模和未来一年情景

| 利润池 | 当前规模和来源口径 | 2027 基准 | 2027 乐观 | 2027 超预期 | 置信度 |
|---|---:|---:|---:|---:|---|
| Silicon photonics/PIC | 2026 约 23 亿至 40 亿美元，公开二手研究口径差异较大 | 45 亿至 70 亿美元 | 70 亿至 90 亿美元 | 90 亿至 120 亿美元 | 中 |
| CPO/PIC test + external laser | 2026 估 4 亿至 7 亿美元，会议一手产品明确但市场需拆分 | 6 亿至 10 亿美元 | 10 亿至 14 亿美元 | 15 亿至 20 亿美元 | 中低 |
| Industrial laser systems | 2026 公开口径约 65 亿美元；laser processing broader 约 280 亿美元 | 70 亿至 75 亿美元 | 78 亿至 85 亿美元 | 90 亿美元以上 | 中 |
| Fiber lasers | 2025 公开口径约 63 亿至 76 亿美元 | 80 亿至 90 亿美元 | 95 亿至 110 亿美元 | 120 亿美元以上 | 中 |
| Smart glasses and AR optics | 2026 smart glasses 约 32 亿美元；AR optical stack 估 6 亿至 10 亿美元 | 9 亿至 14 亿美元 | 15 亿至 22 亿美元 | 25 亿至 35 亿美元 | 中低 |
| Machine vision | 2025/26 公开口径约 158 亿至 261 亿美元 | 175 亿至 290 亿美元 | 200 亿至 330 亿美元 | 240 亿至 380 亿美元 | 中 |
| 3D sensors | 2026 约 78 亿美元 | 86 亿至 93 亿美元 | 95 亿至 105 亿美元 | 110 亿至 125 亿美元 | 中 |
| Hyperspectral imaging | 2026 约 3 亿至 9 亿美元，定义差异大 | 3.4 亿至 10.5 亿美元 | 4 亿至 12 亿美元 | 5 亿至 15 亿美元 | 中低 |
| Biophotonics broad | 2026 约 940 亿至 1,020 亿美元 | 1,020 亿至 1,120 亿美元 | 1,120 亿至 1,250 亿美元 | 1,300 亿美元以上 | 中 |
| Quantum photonics/sensors | 2026 quantum photonics 约 7 亿至 11 亿美元；quantum sensors 约 5 亿至 9 亿美元 | 12 亿至 18 亿美元 | 18 亿至 25 亿美元 | 30 亿美元以上 | 低中 |

### 3. 利润率走向

1. 最容易扩张利润率的环节：CPO/PIC 测试仪器、external laser、生产级 alignment、仿真/软件、advanced thermal material、AR metrology。这些环节有客户认证壁垒、低 BOM 占比但高失败成本，毛利率可在 50%-70% 区间。

2. 利润率有上行但受竞争影响的环节：AI optical modules、high-speed transceiver、silicon photonics chips。若 800G/1.6T 需求强，产能紧张会推高毛利；但模块客户集中、ASP 下行和中国供应商进入会压制长期利润率。估算毛利率 25%-45%，头部和良率领先者高于行业均值。

3. 利润率被低估的环节：diamond/ceramics/特殊光学材料、高折射率 XR 材料、InGaAs APD、OCT specialty fiber assemblies。这些不是最大市场，但若成为客户架构关键路径，可形成 40%-60% 毛利的小瓶颈。

4. 利润率可能被市场高估的环节：AR waveguide 整体制造、通用工业光纤激光、泛 quantum computing 概念公司。原因分别是良率/整机需求不确定、低端价格战、收入兑现周期长。

## 反共识洞见和重要更新

### 过度乐观方向

1. CPO：会议材料说明 CPO 的量产门槛很真实，但并没有证明 2026 年 CPO 已大规模替代 pluggable。若后续 OFC/财报仍只出现 demo、pilot、qualification，没有明确客户批量订单，应该把 CPO 收入兑现从 2026 推到 2027-2028。

2. AR display glasses：会议确认波导、材料、刻蚀和计量在加速，但这也说明量产问题尚未完全解决。AI glasses 的无显示需求已经被验证，不等于带显示 waveguide glasses 会在 2026 年爆发。真正要跟踪的是 OEM product launch、waveguide yield、FOV/亮度/功耗、整机重量、BOM 和退货率。

3. Biophotonics broad TAM：广义 1,000 亿美元市场不能直接映射到 photonics component 股票。很多收入在整机、医院系统、耗材、服务和软件；可投组件链条更小，且受临床和监管约束。

4. Quantum computing：Quantum West 热度高，但会议可验证收入主要在 clock、sensor、entropy、laser、detector 和 platform。把 2026 年会议材料直接解释为通用量子计算收入拐点是过度乐观。

### 被市场低估方向

1. CPO/PIC production test：Quantifi 的 ELSFP 1000、AIM 的 300 mm EO/RF test、Coherent 的 high-resolution filter 和 power meters 共同指向一个结论：CPO 放量前先放量的是测试、外置激光和 alignment。Teradyne/Quantifi、Keysight、Coherent、EXFO、Santec、PI 等比纯 CPO 概念更接近确定 capex。

2. 热材料：Coherent bondable diamond 的 99% thermal interface resistance reduction 和 100 mm square die 支持说明，AI accelerator + photonic engine 的热接口可能形成新材料利润池。市场更关注 transceiver 数量，可能低估了 thermal material 的 ASP 和认证壁垒。

3. AR optical metrology/materials：Dispelix、Pixelligent、Tokyo Electron、Tobii 的材料说明，AR 波导要跨过量产，必须先解决材料、工艺、检测、镜片集成。小公司或上游材料设备的弹性可能高于整机 OEM。

4. InGaAs/APD/SPAD and spectral sensors：Phlux Aura、Metalenz Polar ID、imec spectral sensors、ams OSRAM/Lumotive 线索说明，近红外和 wafer-level sensing 正在从科研进入机器视觉/机器人/汽车/消费电子。小市场高增速可能比大而分散的机器视觉系统更有投资弹性。

5. 高亮度单模工业激光：IPG 8 kW single-mode M2 < 1.1 不是简单功率参数，而是可加工材料、精度、速度和应用窗口的变化。若传统切割需求弱，高亮度单模和 semicap/display laser processing 仍可能独立增长。

### 看起来相关但收入弹性不强

1. 大型半导体设备公司：Tokyo Electron 的 AR waveguide 工艺研究很重要，但 AR optical revenue 对 TEL 总收入短期占比很小，除非出现明确专用 tool order。

2. 大型显示/消费电子公司：有整机叙事不等于 photonics 利润弹性；如果关键 waveguide、材料、光机和检测来自外部供应商，整机 OEM 可能只是需求放大器。

3. 泛 photonics distributor：Photonics West 展商多，但没有自有材料/器件/测试能力的分销商难以捕获结构性利润率。

4. Quantum pure-play 概念股：若没有可销售的 photonic instrument、sensor、QRNG/security module 或政府订单，会议热度不能支撑短期收入。

### 立刻下修判断的反证条件

1. 2026 H2 仍没有 CPO/PIC test equipment 的订单增速、客户 qualification 或 high-channel-count test capex。
2. 800G/1.6T pluggable 供应过剩导致 optical module ASP 跌幅超过 25%，同时 CPO 订单未补位。
3. Bondable diamond/advanced thermal materials 未通过可靠性或成本门槛，客户改用传统 cold plate/TIM/ceramic 方案。
4. AR display glasses 2026 H2 主要 OEM 延期，waveguide 良率和光效无改善，材料/计量订单停留在研发量级。
5. Biophotonics 新产品无法获得监管批准、临床数据或 OEM design-in，收入仍停留在科研仪器。
6. Quantum entropy/sensor/clock 无真实客户订单，仅作为 booth demo。

## 公司和产业链映射

### 头部和较高相关公司

| 公司 | 会议相关证据 | 收入暴露 | 投资弹性判断 |
|---|---|---:|---|
| Coherent (COHR) | Photonics West 发布 bondable diamond、Sapphire XT、OCT fiber assemblies、CO2 EOM、FieldMax、Waveshaper；与 Quside 展示 6-inch VCSEL quantum entropy | AI optical、materials、lasers、life sciences、test/metrology 多线 | 高。不是单一 CPO 标的，而是 AI optics + thermal + lasers + quantum/security platform 组合；风险是估值和 optical module 周期 |
| IPG Photonics (IPGP) | YLR-8000-SM 获 2026 Prism Lasers；8 kW single-mode、M2 < 1.1 | 工业光纤激光，高端应用 | 中高。高亮度单模有技术弹性，但通用工业激光需求和价格战压制总盘 |
| Teradyne / Quantifi Photonics (TER) | Quantifi ELSFP 1000 Series：8 channel、1311 nm、最高 25 dBm/channel、CPO/PIC test | Quantifi 占 Teradyne 总收入小，但方向关键 | 中高。若 CPO test capex 启动，收入弹性先在小基数业务出现；总公司层面需看半导体 ATE 周期 |
| MKS Instruments / Ophir (MKSI) | Photonics Spectra 列出 Ophir 70 kW high-power laser sensor；Ophir 在激光计量强 | 激光功率计量、semicap、industrial | 中。受益于高功率激光和生产计量，但公司收入更分散 |
| G&H (LON:GHH) | Photonics West/BiOS 展示 integrated photonics platforms、OCT、Psyros point-of-care、quantum supply chain | 小型 photonics integrator，life sciences/defense/industrial | 中高。小公司收入弹性好，但流动性、客户集中和项目制风险更高 |
| Hamamatsu | 展商和产品材料；BiOS/传感/探测器核心供应商 | 探测器、光源、医疗/工业传感 | 中。真实暴露强但股票弹性取决于估值和日元/医疗周期 |
| ams OSRAM | TMF8829 Prism Sensors finalist；3D sensing/optical semis | 传感、LED/laser、consumer/auto | 中。3D/ToF exposure 有弹性，但公司整体业务复杂 |
| Tokyo Electron | AR waveguide TiOx etch、TiO2 ALD、高折射率 grating 会议报告 | 半导体设备 | 低到中。技术重要，但 AR 收入占比短期很小 |
| Keysight/EXFO/Santec/PI | 展商和 test/metrology 生态 | 光通信测试、alignment、metrology | 中。受益于 CPO/PIC test，但需验证订单 |

### 私有或小型高弹性公司/环节

| 公司/环节 | 会议证据 | 可能弹性 |
|---|---|---|
| Dispelix / AAC | 下一代 AR device capabilities、metrology panel | AR waveguide design win 和量产良率改善 |
| Pixelligent | n~2.0 XR nanomaterials | 高折射率材料若进入 OEM 供应链，BOM 小但毛利高 |
| Tobii Lens Technology | lens casting、处方/防水/电子/光学集成 | AR 智能眼镜工业化的镜片集成环节 |
| Metalenz | Polar ID Prism winner | metasurface imaging 可用于身份识别、3D sensing、mobile/IoT |
| Phlux Technology | Aura Noiseless InGaAs APD Prism winner | InGaAs APD 在 lidar、量子、生命科学中可能是瓶颈器件 |
| TOPTICA | TOPTICLOCK Prism winner | quantum/precision instrumentation 卖铲者 |
| PHIX / imec / AIM Photonics | PIC packaging、200/300 mm Si/SiN、300 mm testing | 硅光走向量产的 foundry/package/test 基础设施 |

### 伪受益或低弹性公司

1. 只提供通用光学件、无专有工艺或客户认证的展商：受益于流量，但难以体现结构性利润率。
2. 只在 investor deck 写“AI photonics”但没有 CPO/PIC test、packaging、thermal、800G/1.6T 或 hyperscaler qualification 证据的公司。
3. 只讲 AR 整机概念但没有 waveguide yield、light engine、材料或 metrology 能力的公司。
4. 只讲 quantum computing TAM 但没有 instrument/sensor/security order 的公司。
5. 广义医疗设备公司：如果没有 OCT、NIRS、光子诊断或 photonic module 暴露，BiOS 热度对收入影响有限。

### 市场和交易线索

1. 2026 年 AI optical networking 股票情绪已经很热。2026-05 的公开市场报道提到 Coherent、Lumentum、Applied Optoelectronics、Corning 等 optical networking/AI data-center 相关股票年内显著上涨，Applied Optoelectronics 年内涨幅曾被报道为约 +440%；报道还提到 Coherent first 6-inch fab transceiver 和 BofA 将 2030 AI data-center TAM 预测提高到 1.7 万亿美元。该信息是二手市场情绪线索，不能替代公司订单验证。
2. 交易上要区分三类：第一类是已被 AI 光模块行情定价的 COHR/LITE/AAOI；第二类是可能被低估的 test/metrology/thermal/materials；第三类是会议热度高但收入尚早的 AR/quantum。Photronics West 对第一类是“验证供需叙事”，对第二类是“发现利润池”，对第三类是“设跟踪清单”。
3. 后续如果 2026 Q2/Q3 财报中 optical test、thermal material、AR material/metrology 没有订单语言，应该下修本报告中“低估环节”的 2027 乐观情景。

## 风险、反证条件和后续跟踪

### 未来 3 个月跟踪

1. OFC 2026 和后续公司材料：800G/1.6T、CPO、ELSFP、external laser、high-channel-count test、optical module ASP。
2. Coherent、Lumentum、AAOI、IPG、MKS、Teradyne、Keysight 财报：是否出现订单、backlog、gross margin、capacity utilization 的一致验证。
3. AR supply chain：Dispelix/AAC、Pixelligent、Tobii、Eulitha、TEL 是否披露 design win、量产工具、材料认证、客户样机。
4. BiOS：Helix Surgical、DoseOptics、Ramona、G&H、Coherent OCT/NIRS 是否有监管、OEM、临床、量产节点。
5. Quantum：Coherent/Quside development kits 是否进入客户试用；TOPTICA、G&H、imec 是否披露订单或政府项目。

### 未来 1 年跟踪

1. CPO/PIC test revenue 是否先于 CPO shipment 增长。若 test equipment order 增长，而 CPO module 仍小，这是正向信号。
2. AI optical module ASP 和毛利：若需求强但 ASP 快速下行，利润池会向测试/材料/封装迁移。
3. AR display glasses 是否出现百万级整机计划和明确 optical BOM supplier。
4. 工业激光高端子类是否独立于通用制造周期增长。
5. Vision Tech 是否从首届 expo 变成持续扩张的 SPIE 板块。

### 未来 2 年跟踪

1. CPO 是否进入生产级 AI switch/accelerator cluster，而不是 booth demo。
2. Diamond/ceramic/thermal interface 是否成为 AI optical engine 或 high-power die 的标准层。
3. AR waveguide 是否从小批量客户测试进入消费电子或企业市场持续交付。
4. Biophotonics 是否出现可复用的 regulated OEM module platform，而不是一次性项目。
5. Quantum photonics 是否从政府/科研仪器走向安全芯片、PNT、医疗或 telecom synchronization 的商业采购。

### 刷新频率

1. CPO/PIC/AI optics：每月刷新，重大会议和财报后即时刷新。
2. AR optics：每季度刷新，重点看整机发布和供应链 design win。
3. Industrial lasers：每季度财报刷新，重点看订单、价格和高端应用 mix。
4. Biophotonics：季度到半年刷新，重点看监管和 OEM 节点。
5. Quantum photonics：半年刷新，避免被概念新闻过度扰动。

## 来源清单

### 一手官方和会议材料

| 来源 | 日期 | 类型 | 用途 | 可信度 |
|---|---:|---|---|---|
| Moscone Center, “SPIE PHOTONICS WEST” https://www.moscone.com/events/spie-photonics-west-1 | 2026 | 场馆/会议页面 | 会议日期、地点、主题范围 | 高 |
| SPIE 官方会后新闻镜像，“The global photonics community converges in San Francisco...” https://www.automateshow.com/exhibitor-news/the-global-photonics-community-converges-in-san-francisco-as-more-than-23-000-register-for-photonics-west-2026 | 2026-01/02 | 官方新闻转载 | >23,000 registrants、40 countries、4,200 presentations、100 conferences、49 courses、~1,600 exhibitors、2024 core components revenue 3,810 亿美元 | 高 |
| Photonics Spectra, “SPIE Photonics West 2026” https://www.photonics.com/Events/SPIE-Photonics-West-2026/ie3607 | 2025-12/2026 | 行业媒体/会议页 | 会议覆盖技术、产品列表、展商线索 | 中高 |
| optics.org, “PW2026: SPIE announces best new products at its 18th annual Prism Awards” https://optics.org/news/pw2026-spie-announces-best-new-products-at-its-18th-annual-prism-awards | 2026-01-28 | 行业媒体转述官方奖项 | Prism winners：Helix、Metalenz、IPG、Seagate、TOPTICA、Phlux、4D、LightTrans、Cerca | 中高 |
| Photonics Spectra, “SPIE Announces Prism Awards Finalists” https://www.photonics.com/Articles/SPIE-Announces-Prism-Awards-Finalists/a71625 | 2025-11 | 行业媒体/官方奖项 | 24 个 finalists 和产品分类 | 中高 |

### 一手公司材料

| 来源 | 日期 | 类型 | 用途 | 可信度 |
|---|---:|---|---|---|
| Coherent, “Coherent Highlights Photonics and Advanced Materials Innovation at Photonics West 2026” https://www.coherent.com/news/press-releases/coherent-highlights-photonics-and-advanced-materials-innovation-at-photonics-west-2026 | 2026-01-20 | 公司新闻稿 | bondable diamond、Sapphire XT、OCT assemblies、CO2 EOM、FieldMax、Waveshaper、CPO panel | 高 |
| Coherent, “High-Performance Bondable Diamond Solutions” https://www.coherent.com/news/press-releases/thermal-management-portfolio-with-high-performance-bondable-diamond-solutions | 2026-01-19 | 公司新闻稿 | 99% thermal interface resistance reduction、100 mm square die、材料适配 | 高 |
| Coherent + Quside, “Verifiable Entropy for Quantum-Safe Encryption” https://www.coherent.com/news/press-releases/coherent-and-quside-demonstrate-verifiable-entropy-for-quantum-safe-encryption | 2026-01-20 | 公司新闻稿 | 6-inch VCSEL quantum entropy、development kits、mass-manufacturable QRNG/security | 高 |
| Quantifi Photonics, “First ELSFP Solution in PXI for Scalable CPO and PIC Testing” https://www.quantifiphotonics.com/quantifi-photonics-introduces-pxi-external-laser-built-on-elsfp-standard/ | 2026-01-21 | 公司新闻稿 | ELSFP 1000、8 channel、1311 nm、25 dBm/channel、PXI、CPO/PIC test | 高 |
| Quantifi Photonics, “ELSFP External Laser Source” https://www.quantifiphotonics.com/products/lasers-amplifiers/pxi-elsfp-external-laser-source/ | 2026 | 产品页 | ELSFP 产品参数 | 高 |
| AIM Photonics, “AIM Photonics at Photonics West 2026” https://www.aimphotonics.com/news/aim-photonics-at-photonics-west-2026 | 2026-01 | 公司/机构材料 | 300 mm silicon photonics、微环调制器、EO/RF wafer/die test | 高 |
| IPG Photonics, “IPG Wins 2026 SPIE Prism Award in Laser Category” https://www.ipgphotonics.com/newsroom/news/ipg-wins-2026-spie-prism-award-lasers-category | 2026 | 公司新闻稿 | YLR-8000-SM，8 kW compact single-mode，M2 < 1.1 | 高 |
| Tokyo Electron, “SPIE Photonics West 2026” https://www.tel.com/news/event/2026/20260113_001.html | 2026-01-13 | 公司活动页 | AR waveguide TiOx etch、TiO2 ALD、wafer-scale high-index gratings | 高 |
| G&H, “G&H to Demonstrate Integrated Photonics Platforms...” https://gandh.com/news-and-resources/spie-photonics-west-2026 | 2026-01 | 公司新闻稿 | BiOS/OCT、Psyros、industrial/telecom/quantum/aerospace integrated photonics | 高 |
| imec IC-Link, “SPIE Photonics West 2026” https://www.imeciclink.com/en/events/spie-photonics-west-2026 | 2026-01 | 公司/机构活动页 | 200/300 mm Si/SiN photonics、wafer-level spectral sensors、FMCW LiDAR、quantum | 高 |
| Dispelix, “SPIE AR | VR | MR @Photonics West 2026” https://dispelix.com/resources/events/spie-a/ | 2026-01 | 公司活动页 | AR waveguide demos、AAC collaboration、metrology from fab lab to fab | 高 |
| Pixelligent, “SPIE AR | VR | MR Conference” https://www.pixelligent.com/event/spie-ar-vr-mr-conference-photonics-west/ | 2026-01 | 公司活动页 | n~2.0 XR nanomaterials | 高 |
| Tobii, “SPIE AR | VR | MR Expo 2026” https://www.tobii.com/events/spie-ar-vr-mr-2026 | 2026-01 | 公司活动页 | lens casting、optical/electronic/prescription/ingress integration | 高 |
| PHIX, “Photonics West 2026” https://www.phix.com/event/photonics-west-2026/ | 2026-01 | 公司活动页 | PIC packaging experts、NL Pavilion、PIC Summit USA | 中高 |

### 技术和二手市场材料

| 来源 | 日期 | 类型 | 用途 | 可信度 |
|---|---:|---|---|---|
| Futurum Group, “Did SPIE Photonics West 2026 Set the Stage for Scale-up Optics?” https://futurumgroup.com/insights/did-spie-photonics-west-2026-set-the-stage-for-scale-up-optics/ | 2026-01-27 | 分析师会后文章 | CPO 系统工程、thermal、test、simulation、vendor moves | 中；有商业关系披露，作为交叉验证 |
| Fortune Business Insights, Silicon Photonics Market https://www.fortunebusinessinsights.com/industry-reports/silicon-photonics-market-101438 | 2026 检索 | 二手市场数据 | 2026 silicon photonics 市场规模和 CAGR | 中 |
| Global Market Insights, Silicon Photonics/Industrial Laser Systems/Fiber Laser public pages https://www.gminsights.com/ | 2026 检索 | 二手市场数据 | silicon photonics、industrial laser systems、photonic quantum computing 数字 | 中 |
| MarketsandMarkets, Machine Vision / Hyperspectral public pages https://www.marketsandmarkets.com/ | 2025/2026 检索 | 二手市场数据 | machine vision、hyperspectral imaging systems 市场规模 | 中 |
| Mordor Intelligence, 3D Sensor and Quantum Sensors public pages https://www.mordorintelligence.com/ | 2026 检索 | 二手市场数据 | 3D sensor、quantum sensors 市场规模 | 中 |
| Grand View Research, Smart Glasses / Fiber Laser / Machine Vision / Biophotonics public pages https://www.grandviewresearch.com/ | 2025/2026 检索 | 二手市场数据 | smart glasses、fiber laser、machine vision、biophotonics 市场规模 | 中 |
| Coherent Market Insights / Precedence Research / Persistence public pages | 2026 检索 | 二手市场数据 | biophotonics、laser processing、hyperspectral、quantum 交叉口径 | 中低；用于区间，不单独支撑结论 |

### 非官方分享和市场情绪

| 来源 | 日期 | 类型 | 用途 | 可信度 |
|---|---:|---|---|---|
| KGOnTech, “AR Conferences 2026 and Laser Display” https://kguttag.com/2025/12/18/ar-conferences-2026-and-laser-display/ | 2025-12-18 | 独立 AR 行业观察 | SPIE AR/VR/MR 重点偏 optical see-through HWD，作为方向线索 | 中低；非官方，不能单独支撑核心结论 |
| Barron's / MarketWatch 等公开市场报道 | 2026-05 至 2026-06 | 二级市场情绪 | AI optical networking 股票涨幅和市场叙事 | 中低；只作交易情绪，不作基本面事实 |
| YouTube/SPIE/Photonics Media 公开视频 | 2026-01 至 2026-04 | 视频线索 | 会议产品展示、采访、展商 demo 线索 | 低至中；需一手材料验证 |

