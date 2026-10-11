# ISSCC 2026：AI 算力系统化拐点、存储/互连/供电瓶颈与未来一年产品爆发路线

> 资料范围：截至 2026-05-08，整理 ISSCC 2026 官方 Advance Program/CFP、公开新闻与公开市场资料；未参考本项目内已有文件或内部信息。会议官方主题为 **“Advancing AI with IC & SoC Innovations”**，会期 2026-02-15 至 2026-02-19，地点为 San Francisco Marriott Marquis。  
> 关键外部资料：ISSCC 2026 官方 Advance Program、ISSCC 2026 CFP、Gartner 2026 半导体市场预测、TrendForce 光互连资料、IBM/imec 等公开论文新闻。文末列源。

## 一句话结论

ISSCC 2026 的最大变化不是“又多了几个 AI 加速器”，而是 **AI 算力从单芯片 FLOPS 竞争，转向系统级约束竞争**：HBM4/LPDDR6/GDDR7、UCIe/D2D、800G/1.6T 光互连、CPO、48V/近负载供电、3D/Chiplet 封装、AI for EDA 与硬件安全被统一放进 AI/HPC 的同一张路线图里。  

市场上最容易被低估的地方有四个：

1. **半导体总收入被 AI 与存储提前“拉大”**：Gartner 预测 2026 全球半导体收入 **1.32 万亿美元**，2025 为 **8053 亿美元**，2027 为 **1.5545 万亿美元**；其中存储从 2025 年 **2163 亿美元**跳到 2026 年 **6333 亿美元**，2027 年 **7481 亿美元**。
2. **AI 半导体不再只是 GPU**：按 Gartner 2026 年 AI 半导体约占总半导体 **30%**测算，AI 相关芯片/存储/互连/电源链条已经是 **约 3960 亿美元**级别的大赛道。
3. **未来一年最强 beta 不是单一“边缘 AI”概念，而是 HBM、先进封装/D2D、AI 光互连、AI 供电、EDA 自动化**；CIM/片上 LLM/6G FR3 是更长周期、更高波动的期权。
4. **利润池会从“只看算力芯片毛利”转向稀缺环节毛利**：HBM、先进封装、CPO 光引擎、D2D PHY/IP、AI 电源模块、EDA/IP 会吸走一部分过去只归属于 GPU/ASIC 的超额收益。

## 1. ISSCC 2026 的重点与发展方向

### 1.1 会议结构本身已经说明主线：AI/HPC/Chiplet/Optics/Power 被并列处理

ISSCC 2026 官方 Advance Program 首页给出的核心配置：

- 会议主题：**Advancing AI with IC & SoC Innovations**。
- 10 个 Tutorial 中，直接相关主题包括 Compute-in-Memory、High-Speed DAC、Beyond FinFET memory/digital、Clocking/CDR、Doherty PA 等。
- Sunday Forum：
  - **Power Efficient Circuits and Systems for Next-Gen Agentic AI and Robotics**
  - **Electrical and Optical Links Towards 400G+ Connectivity**
- Thursday Forum：
  - **Powering the Future of AI, HPC, and Chiplet Architectures**
  - **The Race for 6G FR3 (7-24GHz)**
  - **Analog for AI and AI for Analog**
  - **Calibration & Dynamic Matching Techniques for Data Converters**
- Short Course：
  - **Circuits for Optical Subsystems: Communications and Beyond**

这相当于把 AI 算力的问题从“处理器 session”扩展到 **存储、互连、光、电源、模拟、RF、EDA、安全**。如果对照 2023-2025 的市场叙事，2026 的显著变化是：产业不再把“模型变大”看成唯一变量，而是开始把 **功耗密度、I/O 能耗、内存带宽、封装良率、链路延迟、EDA 设计复杂度**视为同等重要的约束。

### 1.2 处理器与 AI 芯片：从单 die 到 chiplet、reticle-scale、可量产软件栈

官方 Processor / Highlighted AI Chip Release / AI Accelerator session 里，最值得关注的公开题名和指标：

| 方向 | ISSCC 2026 公开材料中的硬指标/事实 | 投资和产品含义 |
|---|---:|---|
| 数据中心 GPU | AMD Instinct MI350：**CDNA 4、3D-stacked 3nm XCD + 6nm IOD** | 高端 GPU 已经默认 chiplet + 先进封装，单颗 SoC 迭代变成系统封装迭代。 |
| AI SoC chiplet | Rebellions：Quad-Chiplet AI SoC，**16Gb/s UCIe-Advanced D2D**，题名披露 **30-60 TOPS/W** | 初创/区域 AI ASIC 开始用标准化 D2D 缩短与大厂差距。 |
| 端侧/车载视觉 | UniC-Vision：**14.4Gb/s、7.3pJ/b** ViT/OFDM AI-RAN accelerator | Vision Transformer、AI-RAN、车载推理开始共用低功耗数据搬运架构。 |
| IBM AI 推理 | IBM Spyre：Inference-Optimized Scalable AI Accelerator | 企业级 AI 推理开始走“可扩展、可部署”的 ASIC 产品路线，而不只是研究 demo。 |
| 扩散模型 | MediaTek MADiC：**3nm、7.4 TOPS/mm2、17.4 TOPS/W** generative diffusion accelerator | 端侧生成式 AI 从 CNN/NPU 时代进入 diffusion/transformer 专用优化。 |
| 3D Gaussian Splatting | 3D GS processor：**1286fps、0.39mJ/frame** | AR/VR、数字孪生、机器人视觉的轻量 3D 表征开始进入硬件优化窗口。 |
| 微软 AI 加速器 | MAIA：Reticle-Scale AI Accelerator | 云厂自研芯片进入“系统产品”阶段，影响 GPU 独占利润池。 |
| NVIDIA | GB10：SoC built for AI acceleration | AI PC/工作站/边缘开发者平台继续下沉。 |

变化判断：2024-2025 市场主要看 GPU 出货与 HBM 供给；ISSCC 2026 说明 2026-2027 的关键是 **谁能把 chiplet、HBM、D2D、供电、散热、软件编译器栈一起量产**。

### 1.3 存储：HBM4、LPDDR6、GDDR7 同时出现，说明 AI 内存路线分叉

ISSCC 2026 Memory session 公开题名非常集中：

| 产品/技术 | ISSCC 2026 指标 | 含义 |
|---|---:|---|
| HBM4 | **36GB、3.3TB/s HBM4 DRAM**，per-channel TSV RDQS auto calibration | HBM4 已进入公开电路实现阶段，2026-2027 重点从 HBM3E 产能转向 HBM4 资格认证、良率、封装协同。 |
| LPDDR6 | **16Gb LPDDR6，14.4Gb/s/pin**；另有 **16Gb 12.8Gb/s LPDDR6** | 端侧 AI、手机、AI PC 会用 LPDDR6 提升能效，而不是简单移植服务器 HBM。 |
| GDDR7 | **24Gb GDDR7，48Gb/s**，题名明确指向 **mid-range inference AI** | 中端推理卡/边缘服务器可能用 GDDR7 做“低成本推理内存层”，压低部分 HBM-only 预期。 |
| SRAM | 2nm nanosheet **350mV single-rail SRAM** | 低压 SRAM 是端侧 AI 与 always-on 计算的底层门槛。 |
| eMRAM/STT-MRAM | 16nm **168Mb embedded STT-MRAM、51.2Gb/s read throughput**，车载/edge AI | 非易失嵌入式存储在车规和低功耗 AI 上的商业化继续推进。 |
| 3D NAND | **2Tb 4b/cell、37.6Gb/mm2** | AI 不是只推 DRAM；数据湖、训练集、推理日志继续拉动 NAND 层级。 |

变化判断：市场以前常把“AI 内存”直接等同于 HBM；ISSCC 2026 更像是 **三层内存爆发**：

- 训练/高端推理：HBM3E -> HBM4。
- 中端推理/高性价比卡：GDDR7。
- 端侧/AI PC/手机/机器人：LPDDR6 + 低压 SRAM/eMRAM。

### 1.4 D2D 和高密度电互连：UCIe 进入能效竞争

Die-to-Die and High-Speed Electrical Transceivers session 披露的关键指标：

| 指标 | 论文题名披露 |
|---|---:|
| UCIe-compliant D2D | **48Gb/s/lane、1.24Tb/s/mm** |
| UCIe-like D2D | **32Gb/s、12.35Tb/s/mm2、0.36pJ/b**，3nm active LSI |
| modular D2D | **0.23pJ/b、24Gb/s、zero wake penalty** |
| single-ended SBD | **112Gb/s/wire** |
| PAM-4 CDR | **112Gb/s、0.76pJ/b** |
| XSR SBD | **56Gb/s/wire、0.292pJ/b** |
| PAM transmitter | **180-240Gb/s、0.70pJ/b analog power efficiency** |
| PAM-8 transmitter | **168Gb/s、1.06pJ/b** |

这组数字说明 D2D 的竞争焦点已从“能不能连上”变成 **每 bit 能耗、每 mm 带宽、唤醒延迟、PVT/失配跟踪、与 UCIe 的互操作**。  
对市场的含义是：高端 AI 芯片的稀缺不只在计算 die，还在 **有经验的 D2D PHY/IP、封装基板、interposer、active bridge、测试与良率管理**。

### 1.5 光互连/CPO：从 400G+ 论坛走向 6.4Tb/s ASIC 和 500Gb/s 光通道

官方材料中，光互连被放在 Forum、Short Course 和论文 session 三层：

- Forum：Electrical and Optical Links Towards **400G+ Connectivity**。
- Short Course：Optical subsystems，包括 optical link architecture、VCSEL、silicon photonics、emerging optical applications。
- Next-Generation Optical Transceivers session：
  - **2-channel 800Gb/s coherent-lite transceiver**
  - **2x500Gb/s monolithic silicon-photonic DWDM PAM-4 transceiver in 45nm CMOS SOI**
  - **6.4Tb/s、4.2pJ/b co-packaged optics ASIC with direct-drive**
  - **212Gb/s/lambda、0.91pJ/b direct-drive O-band monolithic coherent**
  - **112Gb/s NRZ heterodyne burst-mode receiver，23ns settled**

变化判断：2024-2025 市场主要押 800G 光模块放量；ISSCC 2026 的信号是 **光互连正在向低延迟、短距、高密度、CPO/near-package 方向迁移**。但这不代表 pluggable 模块立刻消失，更可能是：

- 2026：800G/1.6T pluggable 继续爆发；
- 2027：CPO 在超大集群/专用网络里 pilot；
- 2028 以后：如果可靠性、维修、热管理、激光源策略成熟，CPO 进入更大规模。

### 1.6 供电：AI/HPC 的下一条硬约束

官方 Thursday Forum 直接出现 **Integrated Voltage Regulator Solutions to Enable 5kW GPUs**，并讨论 AI data-center power delivery、3D vertical power delivery、package-integrated regulators、HBM power delivery、integrated magnetics。  

Compute Power session 披露：

| 技术 | ISSCC 2026 指标 |
|---|---:|
| coupled-OSC converter | **89.5% peak efficiency @61MHz、1.82W/mm2 @360MHz** |
| resonant sigma converter | **4Vin、93.4% peak efficiency、12A load、20mV undershoot** |
| 12-to-1V converter | **90.5% peak efficiency、721A/cm3 current density** |
| 48V hybrid converter | **48V to 0.8-1.6V、92.4% peak efficiency** |
| LLC resonant converter | **100A、93.4% peak efficiency** |
| symbol power tracking | **1.2us、1-to-12V** supply modulator |

变化判断：AI 芯片从 700W/1000W 走向 rack-scale 后，**48V 到 sub-1V 的转换链、垂直供电、封装内/近封装电源、HBM 供电完整性**会成为性能释放条件。市场容易只看 GPU ASP，但供电是未来一年更确定的配套增量。

### 1.7 CIM、片上 LLM 与 always-on AI：很热，但商业化节奏要分层

Compute-in-Memory session 指标密度极高：

| 论文方向 | ISSCC 2026 指标 |
|---|---:|
| MXFP CIM | **28nm、127.54TFLOPS/W MXFP6、117.42TFLOPS/W MXFP8** |
| charge-trap CIM | **12nm、4Mb、104.56-137.75TFLOPS/W** |
| ReRAM CIM | **22nm、96Mb、50.6-90.2TFLOPS/W**，支持 Mamba/Transformer/CNN |
| gain-cell CIM | **16nm、72kb、120.5TFLOPS/W** |
| near-memory DRAM | **1.2GHz、12.77GB/s/mm2、3D two-DRAM-one-logic**，edge LLM |
| SRAM digital CIM | **16nm、1Mb、1-8b configurable、444.21TOPS/W** |
| fully synthesizable digital CIM | **147TOPS/W、250TOPS/mm2、INT8xINT8** |

AI Accelerator session 端侧 LLM/视觉指标：

| 产品/论文方向 | ISSCC 2026 指标 |
|---|---:|
| ReRAM-on-logic LLM | **14.08-135.69 token/s** |
| dual-quantized LLM | **51.6uJ/token** |
| mobile personalization | SoulMate：**9.8mW** on-device LLM personalization SoC |
| VLM | Tri-Oracle：**17.78uJ/token** |
| SSM | LUT-SSM：**99.3TFLOPS/W** |
| speculative decoding | **105-685us/token**，billion-parameter models |
| always-on vision | ALPhA-Vision：**787us face detection latency，<5mW** |

变化判断：端侧 AI 的真实商业路径不是“手机跑满云端大模型”，而是 **小模型、个人化、always-on、传感器前处理、低功耗 token 生成**。CIM 指标很亮眼，但量产要跨过可编程性、精度、编译器、良率、工艺兼容、温漂校准等门槛。

### 1.8 6G FR3、雷达、Ambient IoT：标准前夜的硬件储备期

ISSCC 2026 将 **6G FR3 7-24GHz**单独设论坛。公开议程包括 FR3 FEM architectures、spectrum sensing/sharing、direct RF sampling ADC、ambient IoT、site-specific MIMO channel optimization。  
论文侧出现：

- Ku-band 6G FR3 Doherty PA：**25.3dBm Psat、29.7% PAE6dB**。
- FR3 source-follower PA：**4:1 VSWR resilience**。
- 24-27.5GHz load-modulated balanced amplifier。
- 330-344GHz GaN PA：**86mW output @340GHz**。
- Radar/UWB：**128mW 2x4 radar-on-chip**；60/77GHz 4T/4R radar RFIC；**234-252GHz** dual-polarized transceiver；UWB transmitter **0.0523mm2、11.4mW**。

变化判断：6G FR3 还没有商业收入爆发，但 RF 前端、PA、ADC、MIMO 测试平台会在 2026-2028 先投入；真正 handset 大规模收入更可能在 2029-2031。

### 1.9 安全：FHE/PQC 从算法议题进入电路议题

Hardware Security session 里：

- HERACLES：**8192-way SIMD programmable scalable** security processor。
- FHE processor：**28nm、0.48mJ/boot**。
- PQC KEM：**16nm、0.042mm2、0.66uJ/op**。
- OmniCrypt：**435.86M-GOPS/W bootstrappable multi-scheme FHE accelerator**。
- SQIsign accelerator：**0.05mm2、1.19-7.34mW**，IoT。
- Chip-to-chip probing attack detector：**166um2/lane、8Gb/s/lane**。
- TRNG：**0.066pJ/bit**，resilient to power-noise injection attacks。

变化判断：AI agent、云端隐私、车载 OTA、IoT 长寿命设备会把 PQC/FHE/PUF/TRNG 从“安全团队问题”变成 SoC baseline feature。商业爆发不如 HBM/光模块快，但安全 IP attach rate 会持续提高。

## 2. 哪些产品/技术方向会爆发：力度、成熟和量产路线

### 2.1 爆发优先级总表

| 优先级 | 方向 | 未来 12 个月爆发力度 | 主要催化 | 主要风险 |
|---|---|---:|---|---|
| S | HBM3E/HBM4 与 AI DRAM | 极强 | AI 训练/推理集群、Gartner 存储收入跳升、HBM4 公开电路指标 | 良率、封装瓶颈、客户集中、价格周期反转 |
| S | 800G/1.6T 光模块、硅光、CPO pilot | 极强 | AI 集群 scale-out、TrendForce 预计 800G+ 份额 2026 超 60% | CPO 维修/热/激光源，模块 ASP 下滑 |
| S | 先进封装、D2D/UCIe、interposer/bridge | 很强 | AMD MI350、reticle-scale MAIA、UCIe D2D 能效指标密集 | 产能/良率、标准碎片化、客户自研 |
| S | AI/HPC 供电：48V、IVR、vertical power、HBM power | 很强 | 5kW GPU、48V-to-1V、100A converter | 电源模块价格竞争、客户定制化高 |
| A | 数据中心 AI ASIC/GPU 与自研加速器 | 很强 | hyperscaler capex、AMD/NVIDIA/Microsoft/IBM/MediaTek 等 chip release | 竞争加剧、HBM 分配、毛利回落 |
| A | EDA/AI for Design | 强 | Cadence plenary、Analog for AI forum、设计复杂度上升 | 客户预算、AI 生成结果可验证性 |
| B+ | GDDR7 中端推理卡 | 强 | ISSCC 明确“mid-range inference AI”，性价比需求 | HBM 降价、云端产品路线改变 |
| B | Edge LLM/always-on vision/CIM | 中到强 | uJ/token、mW 级 SoC 指标密集 | 软件生态、模型变化快、量产精度与良率 |
| B | PQC/FHE/secure chip-to-chip IP | 中 | 后量子标准、agentic AI 安全、车载/IoT 长寿命 | 商业付费节奏慢，IP 议价不强 |
| C+ | 6G FR3/Radar/Ambient IoT | 中低，长期强 | FR3 forum、PA/ADC/radar 硬件储备 | 标准和终端量产时间晚 |

### 2.2 三种情景：成熟和量产路线

#### HBM4 / AI DRAM

- 基准：2026 仍以 HBM3E 放量为收入主力；HBM4 进入客户验证和小批量，2027 放量。HBM 价格保持高位，但客户会要求长期供货协议。
- 乐观：2026 下半年 HBM4 在头部 GPU/ASIC 平台开始较明显 revenue contribution；HBM3E 供需仍紧，HBM 毛利保持行业高位。
- 超预期乐观：HBM4 良率爬坡快于预期，同时 2027 平台提前锁单；HBM 供应商获得类似先进封装的“准产能溢价”，年度收入增速超过 80%。

#### 800G/1.6T 光模块、硅光、CPO

- 基准：2026 爆发核心是 800G/1.6T pluggable；CPO 以 ASIC/光引擎试点为主，2028 前大规模替代比例有限。
- 乐观：AI 集群横向扩展速度继续高于市场预期，1.6T 从高端云厂向更多客户扩散；CPO 在 2027 年进入特定超大集群。
- 超预期乐观：大客户统一 CPO/near-package optical 规格，可靠性和维修模型快速成熟；2027-2028 CPO 收入斜率明显前移。

#### D2D/UCIe/先进封装

- 基准：D2D 先在 GPU、AI ASIC、网络芯片、CPU-chiplet 中放量，UCIe 更多是互联参考框架，实际产品仍有私有 PHY。
- 乐观：UCIe-compatible IP 生态形成，第三方 chiplet 在部分 AI/网络/存储控制器平台上可采购。
- 超预期乐观：hyperscaler 把 D2D/Chiplet 作为供应链多元化工具，更多 ASIC 采用标准 chiplet 采购，IP/测试/封装公司获得高弹性。

#### AI/HPC 供电

- 基准：48V rack power、近负载 converter、package-aware HBM power delivery 在 2026 明显增量；IVR/vertical power 多为高端平台。
- 乐观：5kW GPU/加速器路线确认，电源模块、磁性元件、先进封装电源协同进入平台级 design-in。
- 超预期乐观：供电/散热成为 AI 集群上限，客户愿意为 1-2 个百分点系统效率付高溢价；高端电源 IC/模块毛利上修。

#### 数据中心 AI ASIC/GPU

- 基准：GPU 仍是最大收入池，自研 ASIC 占比上升但不会短期替代 GPU；AMD/ASIC/云厂产品拉高非 NVIDIA 份额。
- 乐观：推理需求和 agentic workflow 推动多个云厂 ASIC 大规模投产，AI 加速器收入增速继续 50%+。
- 超预期乐观：推理 token 成本下降释放需求弹性，GPU + ASIC 同时爆发，算力芯片全年供不应求。

#### Edge LLM / CIM

- 基准：2026 量产收入来自传统 NPU、AI MCU、视觉 SoC；CIM 主要在研究芯片、少数专用 IP 和传感器前处理。
- 乐观：always-on vision、语音、个人化小模型在手机/眼镜/可穿戴进入差异化卖点，CIM/SRAM near-memory 被部分 SoC 采用。
- 超预期乐观：端侧隐私和低延迟需求推动本地 LLM 常驻，uJ/token 成为终端芯片新 KPI，CIM 进入第一批商业 AI MCU/edge SoC。

#### EDA / AI for Design

- 基准：2026 收入体现为 AI-assisted verification、layout、PPA optimization、analog/RF automation seat uplift。
- 乐观：agentic EDA 工作流显著缩短部分模块设计周期，按算力/使用量收费推高 ARPU。
- 超预期乐观：AI for Design 成为先进节点和 chiplet 设计刚需，EDA/IP 公司同时吃到 seat、compute、IP 三重增长。

## 3. 市场规模、增速、利润率：基准/乐观/超预期

口径说明：  
Gartner 的总半导体、存储、非存储为公开预测；细分市场如 HBM、CPO、AI 电源、D2D IP 没有统一官方口径，下表为基于公开总盘子、供应链结构和 ISSCC 2026 技术成熟度的区间推算。利润率以 **毛利率**为主；若是模块/封装类，利润率低于芯片/IP 类。

### 3.1 总盘子

| 市场 | 当前/2026 规模 | 未来一年基准 | 乐观 | 超预期乐观 | 当前利润率与趋势 |
|---|---:|---:|---:|---:|---|
| 全球半导体 | **1.32 万亿美元**，Gartner 2026 | +18%-25% 到 2027 | +25%-32% | +35%+ | 行业平均毛利分化极大；AI/EDA/IP/HBM 高，消费/通用芯片低。 |
| 存储半导体 | **6333 亿美元**，Gartner 2026；2025 为 **2163 亿美元** | +15%-25% | +25%-35% | +40%+ | DRAM/HBM 处于高景气，毛利率上行；周期反转风险从 2027 起加大。 |
| 非存储半导体 | **6869 亿美元**，Gartner 2026；2025 为 **5890 亿美元** | +10%-15% | +15%-22% | +25%+ | AI ASIC/GPU/IP 高，传统 MCU/模拟恢复较慢。 |
| AI 相关半导体 | Gartner 称 2026 约占总半导体 **30%**，约 **3960 亿美元** | +35%-50% | +50%-70% | +80%+ | 头部 GPU/ASIC 毛利高，但竞争和客户自研会压制部分超额毛利。 |

### 3.2 重点产品和技术市场

| 方向 | 2026 市场规模估计 | 基准：未来 1 年增速 | 乐观：未来 1 年增速 | 超预期乐观 | 当前利润率 | 未来利润率走向 |
|---|---:|---:|---:|---:|---:|---|
| HBM/HBM4 及 AI 高端 DRAM | **800-1100 亿美元**推算；包含 HBM3E/HBM4 及 AI 服务器高端 DRAM | +35%-55% | +55%-75% | +80%-110% | HBM 毛利约 **55%-70%**，高于普通 DRAM | 2026 仍上行；2027 若供给释放，毛利高位震荡。 |
| GDDR7 中端 AI 推理内存 | **80-150 亿美元**推算 | +25%-40% | +40%-65% | +80% | 毛利约 **35%-50%** | 若中端推理卡放量，ASP 和毛利好于普通 GDDR；但 HBM 降价会压制。 |
| 数据中心 AI 加速器 GPU/ASIC | **1800-2300 亿美元**推算，不含全部存储 | +35%-50% | +50%-70% | +80%-100% | 头部公司毛利可达 **65%-75%**；ASIC 供应链平均 **35%-60%** | 头部仍高，但客户自研、AMD/ASIC 竞争会使行业平均毛利略降。 |
| 先进封装/Chiplet/D2D 相关 | 先进封装 **500-700 亿美元**推算；D2D PHY/IP/测试为其中小但高增部分 | +20%-35% | +35%-55% | +60%-80% | OSAT/封装 **15%-30%**；foundry advanced packaging **35%-55%**；IP **70%+** | 稀缺产能维持高价，IP/测试利润率好于纯封装。 |
| 800G/1.6T 光模块与 AI 光互连 | **120-180 亿美元**推算；CPO 仍小 | +45%-65% | +65%-90% | +100%+ | 光模块 **25%-40%**；DSP/光引擎/硅光可 **40%-60%** | 模块 ASP 会降，但 1.6T/CPO mix 改善利润结构。 |
| CPO/near-package optical | 2026 约 **5-15 亿美元**推算，主要 pilot/早期产品 | +80%-150% | +150%-250% | +300%+ | 早期毛利 **40%-60%**，系统集成不稳定 | 2026-2027 取决于客户规格锁定；成熟后模块化竞争会压毛利。 |
| AI/HPC 电源 IC、模块、48V/IVR | **40-70 亿美元**AI 相关增量推算；整体 PMIC/电源管理更大 | +20%-35% | +35%-55% | +60%-80% | 模拟 IC **45%-65%**；电源模块 **25%-45%** | 高端平台 design-in 提升毛利，通用模块价格竞争仍强。 |
| EDA/IP/AI for Design | **180-240 亿美元**推算 | +10%-15% | +15%-25% | +30%+ | 软件/IP 毛利 **80%-90%**，运营利润率 **30%-45%** | AI seat/usage pricing 可能推高 ARPU，利润率稳中上行。 |
| Edge AI SoC/AI MCU/端侧 NPU | **500-800 亿美元**推算，含手机/PC/汽车/IoT AI 芯片价值 | +12%-20% | +20%-35% | +40%-55% | SoC 毛利 **35%-55%**；MCU/传感器低一些 | 量大但竞争激烈；真正高毛利来自差异化 IP 和软件生态。 |
| CIM/near-memory AI IP | **<10 亿美元**直接商业收入推算，研究和试产为主 | +30%-60% | +60%-120% | +150%+ | IP/专用芯片可 **50%-80%**，但收入基数小 | 2026 更多是技术期权；量产突破会带来非线性重估。 |
| 6G FR3/RF 前端前置研发 | FR3 直接商业 **<10 亿美元**；相邻 RFFE/测试市场约 **数百亿美元** | +5%-15% | +15%-25% | +30%+ | PA/RFFE **35%-50%** | 2026-2028 多为研发和测试设备，终端量产前利润贡献有限。 |
| PQC/FHE/security IP | **10-30 亿美元**推算，含 IP、secure MCU、加速器小市场 | +15%-30% | +30%-50% | +60%+ | IP **70%+**；secure MCU **35%-55%** | 标准和法规推动 attach rate，付费节奏慢但粘性强。 |

## 4. 与当前市场可能相违背的重要洞见

### 4.1 “半导体 2026 超高增长”不等于全行业健康

Gartner 的 2026 总半导体 **1.32 万亿美元**预测非常惊人，但结构上主要由 **存储从 2163 亿美元跳到 6333 亿美元**拉动。  
这意味着：广义半导体 ETF 或通用芯片公司未必都受益；收益会高度集中在 **HBM/DRAM、AI ASIC/GPU、先进封装、光互连、EDA/IP、电源**。消费 MCU、传统模拟、低端逻辑可能仍是弱复苏。

### 4.2 HBM 不是唯一 AI 内存，GDDR7/LPDDR6 可能改变中低端推理成本曲线

ISSCC 2026 同时出现 HBM4、LPDDR6、GDDR7，而且 GDDR7 题名直接写明 **mid-range inference AI**。  
这与“所有 AI 推理都只能走 HBM”的市场直觉相反。未来一年：

- 高端训练/大模型推理继续 HBM；
- 中端推理卡可能大量采用 GDDR7；
- 端侧 AI 主要依靠 LPDDR6/低压 SRAM/eMRAM。

若 GDDR7 推理卡形成规模，会对部分 HBM 需求外推、低端 GPU ASP、边缘服务器 BOM 产生重新定价。

### 4.3 CPO 很重要，但 2026 不是“一夜替代光模块”

ISSCC 2026 的 **6.4Tb/s、4.2pJ/b CPO ASIC**和 direct-drive 光电指标说明方向明确；TrendForce 资料也显示 800G+ 光模块份额会在 2026 明显提升。  
但 CPO 的量产难题不是单一芯片指标，而是：

- 激光源放置与可靠性；
- 现场可维修性；
- 热耦合；
- 交换 ASIC、光引擎和封装良率绑定；
- 客户网络架构统一程度。

所以 2026 最确定的是 **800G/1.6T pluggable 爆发**，CPO 更像 2027-2028 的高弹性期权。

### 4.4 AI 芯片毛利可能被“系统瓶颈环节”重新分配

市场常把 AI 利润池等同于 GPU 毛利。ISSCC 2026 更强调系统：D2D、HBM power、48V-to-1V、电光互连、EDA。  
未来一年，若 GPU/ASIC 供给被封装、HBM、光模块、电源拖住，利润池会转向：

- HBM stack 与 TSV/测试；
- CoWoS/SoIC/active bridge/interposer；
- D2D PHY/IP；
- optical DSP/硅光/激光器；
- 高端电源 IC/模块；
- EDA/IP。

### 4.5 “端侧 AI 爆发”要看 uJ/token 和 mW，而不是只看 TOPS

ISSCC 2026 端侧论文写的是 **51.6uJ/token、17.78uJ/token、9.8mW、<5mW、787us**，而不是单纯 TOPS。  
这说明真实产品指标将从“宣传 TOPS”转为：

- token 能耗；
- 常驻功耗；
- 首 token 延迟；
- memory footprint；
- 小模型个性化；
- 传感器到模型的端到端延迟。

这对 AI PC/手机 SoC 厂商是挑战：如果没有模型/编译器/系统功耗协同，单独堆 NPU TOPS 很难转化为用户体验。

### 4.6 Analog/RF 不是 AI 时代的配角，反而变成基础设施瓶颈

ISSCC 2026 里 high-speed ADC/DAC、PLL/CDR、PA、RF front-end、calibration、analog for AI 都被重点安排。典型指标包括：

- 7b **175GS/s** time-interleaved slope ADC；
- 12b **12GS/s** pipeline ADC in 5nm；
- 14b **20GS/s** RF-sampling DAC；
- 112Gb/s electrical transceiver；
- 212Gb/s/lambda coherent optical；
- FR3 PA 和 direct RF sampling ADC。

结论：AI 基建不是纯数字芯片工程，analog/mixed-signal/RF 人才和 IP 会更稀缺。

### 4.7 6G FR3 的投资窗口在设备/测试/RF，不在 2026 终端放量

ISSCC 2026 的 FR3 论坛和论文说明 6G 已经进入电路储备期；但这不等于 2026 出现 handset 大规模换机。更合理路线：

- 2026-2027：PA、FEM、ADC、测试平台、channel sounding、spectrum sharing；
- 2028-2029：预商用基站/终端原型；
- 2029-2031：标准和终端量产收入。

这与“6G 马上爆发”的叙事相反；短期更该看 RF 测试、PA/FEM、材料与高频封装。

## 5. 投资/产业链映射

### 5.1 最强确定性链条

1. **HBM/HBM4**：存储厂、TSV/测试、HBM PHY、HBM power integrity、先进封装配套。
2. **先进封装/Chiplet/D2D**：CoWoS/SoIC、interposer、active bridge、UCIe PHY、D2D verification、known-good-die 测试。
3. **AI 光互连**：800G/1.6T 光模块、DSP、硅光、VCSEL/EML、激光器、CPO optical engine、低延迟光交换。
4. **AI 电源**：48V 到低压 converter、IVR、vertical power、integrated magnetics、HBM power delivery。
5. **EDA/IP**：AI-assisted verification/layout/PPA、analog/RF design automation、chiplet/package co-design、security IP。

### 5.2 高弹性但更不确定的链条

1. **CIM/near-memory AI**：指标惊艳，但产品化路径依赖特定模型、编译器和良率。
2. **端侧 LLM SoC**：需要真实应用拉动；手机/眼镜/机器人比 AI PC 更可能先体现 always-on 价值。
3. **PQC/FHE**：法规和云隐私会推，但商业收入爬坡慢。
4. **6G FR3**：标准前夜，先看测试和 RF，不应提前按终端放量估值。

## 6. 未来一年跟踪指标

### HBM/存储

- HBM4 qualification 节点：头部 GPU/ASIC 平台是否在 2026 下半年确认。
- HBM ASP、bit growth、yield、TSV 良率。
- GDDR7 是否进入中端推理卡大规模设计。
- LPDDR6 是否在 2027 手机/AI PC 平台锁定。

### 光互连/CPO

- 800G+ 模块出货占比是否如 TrendForce 所称在 2026 超过 60%。
- 1.6T 模块实际 ASP 下降速度。
- CPO 的 laser strategy：external laser source 还是 co-packaged laser。
- CPO 是否从 demo 进入 cloud design-in。

### D2D/封装

- UCIe-compatible PHY 是否进入量产产品，而不仅是论文。
- D2D 能耗是否稳定低于 0.5pJ/b。
- Advanced packaging 交期和价格。
- known-good-die 测试覆盖率和良率损失。

### 电源

- 5kW GPU/rack-scale AI 平台是否成为主流路线。
- 48V-to-1V conversion efficiency 是否稳定在 90%+。
- IVR/vertical power 是否进入头部 AI 加速器。
- HBM power integrity 是否成为平台良率和稳定性问题。

### 端侧 AI/CIM

- 端侧产品是否开始披露 uJ/token、首 token 延迟、always-on mW，而非只披露 TOPS。
- CIM 是否进入量产 SoC 的一部分，而不是单独 test chip。
- 小模型个人化是否形成付费应用。

## 7. 资料来源

- [ISSCC 2026 Advance Program PDF](https://submissions.mirasmart.com/ISSCC2026/PDF/ISSCC2026AdvanceProgram.pdf)
- [ISSCC 2026 Call for Papers PDF](https://submissions.mirasmart.com/ISSCC2026/PDF/ISSCC2026CFP.pdf)
- [Gartner: Worldwide Semiconductor Revenue to Exceed $1.3 Trillion in 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- [TrendForce: AI-Driven Data Centers Drive Strong Growth in Optical Communications Market](https://www.trendforce.com/presscenter/news/20250630-12614.html)
- [IBM Research: On-chip power breakthrough for next-generation AI chips](https://research.ibm.com/blog/power-management-circuit-isscc)
- [imec: Analog-to-digital conversion at speed and scale](https://www.imec-int.com/en/articles/analog-digital-conversion-speed-and-scale)

