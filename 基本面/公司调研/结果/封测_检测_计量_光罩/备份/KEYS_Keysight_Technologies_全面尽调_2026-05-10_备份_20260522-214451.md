# 公司：KEYS Keysight Technologies

> 写作日：2026-05-10（美西 2026-05-09 晚）。股价采用美股 2026-05-08 收盘价。  
> 口径说明：Keysight 不披露“AI 数据中心收入”“产品级 backlog”“客户项目订单金额”。本文把公司官方披露、公开产品发布、行业资料和项目内非“公司调研”资料交叉验证；所有产品级 AI 收入、每 MW / rack / port 内容量、未来一年产能均为推断口径。  
> 核心结论：KEYS 不是 AI 芯片公司，而是 AI 互连、光电、PCIe/CXL/UALink、网络协议和系统级验证的“量尺”。AI rack 越复杂、224G/1.6T 越难量产，Keysight 的测试设备、协议软件和验证平台越像出货 gate。

## 1. 公司业务、投资人认知与财务健康

Keysight Technologies 是高端电子设计、仿真、验证、测试与测量公司，源自 Agilent/HP 测量业务。公司产品覆盖示波器、信号源/分析仪、BERT、AWG、VNA、DCA、光电测试、网络流量测试、协议一致性、EDA/仿真软件、校准和支持服务。收入主要来自 R&D 验证，制造/运维测试占比较低，因此周期性弱于纯 ATE，但强依赖客户研发预算和新标准切换。

投资人眼中的 KEYS：高毛利、高 FCF、技术壁垒强的测试测量龙头，兼具“工业科技周期股”和“AI picks-and-shovels”属性。2025 之前市场更多把它看作 5G/半导体/汽车电子/国防复苏标的；2025H2-2026Q1 以后，AI 数据中心高速互连、1.6T、PCIe 7、CXL、UALink 和光电验证成为估值上修主线。

### 1.1 产业链定位

| 层级 | KEYS 的位置 | 价值来源 |
|---|---|---|
| AI 芯片/ASIC 设计 | PathWave、EDA、3DIC/Chiplet、光子/电源分析 | 芯片 tape-out 前的 SI/PI、SerDes、封装、光电链路仿真 |
| AI 服务器/rack 内互连 | PCIe/CXL/UALink/高速铜互连验证 | 128GT/s PCIe 7、64GT/s PCIe 6、CXL 3、UALink 200G 一致性与调试 |
| AI fabric/以太网网络 | Ixia/IxNetwork、AresONE 1600GE、KAI DC Builder | 1.6T/800G 端口、RoCEv2、拥塞、FEC、AI collective workload 仿真 |
| 光模块/硅光/CPO | DCA、BERT、VNA、LCA、224G IEEE 802.3dj 测试软件 | 224G PAM4、1.6T/3.2T 光电组件、TDECQ/TDECQ-CER、S 参数 |
| 量产与服务 | 自动化测试、校准、KeysightCare、专业服务 | 客户资格认证后形成长期软件、服务和升级收入 |

### 1.2 最近三年重大变化

| 时间 | 事件 | 投资含义 |
|---|---|---|
| 2024 | 收购 ESI Group，增强虚拟原型、CAE、汽车/航空仿真能力 | 从硬件仪器向“设计-仿真-测试闭环”扩展，提高软件和早期设计介入比例 |
| 2024-2025 | 逐步把商业通信里的 wireline/data-center ecosystem 提到战略中心 | AI 数据中心互连成为 CSG 增长驱动，弱化传统 5G 手机周期 |
| 2025-10 | 完成 Spirent Communications 收购；因监管要求，部分高速以太网/网络安全/信道仿真业务被出售给 VIAVI | 补强无线网络测试、定位/PNT、网络 assurance、客户关系；同时 VIAVI 在高速网络测试上更强 |
| 2025-10 | 从 Synopsys 收购 Optical Solutions Group，从 Ansys 收购 PowerArtist RTL 业务 | 补齐光子/硅光设计和芯片功耗分析，贴近 CPO、光 I/O、AI ASIC 设计流 |
| 2025 | 收购 Riscure、AnaPico | 增强嵌入式/IoT 安全测试和 RF/微波仪器能力 |

### 1.3 最新估值与利润指标

| 指标 | 数值 | 日期/口径 |
|---|---:|---|
| 股价 | **$360.30** | 2026-05-08 NYSE 收盘，Yahoo chart |
| 市值 | **约 $61-62B** | 2026-05-08，按公开统计页与收盘价估算 |
| TTM GAAP EPS | **约 $5.55** | FY25 Q2-Q4 + FY26 Q1 |
| TTM PE | **约 65x** | $360.30 / $5.55；StockAnalysis 同期约 63.7x |
| Forward PE | **约 38.7x** | StockAnalysis consensus 口径 |
| TTM PS | **约 10.7x** | 市值 / TTM 收入约 $5.68B |
| Forward PS | **约 8.8x** | StockAnalysis consensus 口径 |
| FY25 收入增速 | **+8%** | FY25 $5.375B vs FY24 $4.979B |
| FY26 Q1 收入增速 | **+23% reported，+14% core** | Q1 FY26；core 排除并购/汇率 |
| TTM GAAP 毛利率 | **约 62%** | Q1 FY26 GAAP GM 62.2%；FY25 GAAP GM 约 62.1% |
| Q1 FY26 非 GAAP 毛利率 | **68.5%** | 公司 Q1 FY26 presentation |
| TTM 净利率 | **约 16.9%** | TTM 净利约 $0.96B / TTM 收入约 $5.68B |

估值判断：按传统测试测量公司看，65x trailing PE / 39x forward PE 很贵；按“AI 互连验证瓶颈 + 高毛利软件/服务 + Q2 指引 30% 增长”看，市场正在给它更接近半导体 IP/EDA 的乘数。当前股价对 FY26/FY27 AI 互连订单持续性已经有较高预期。

### 1.4 资产负债表健康度

截至 2026-01-31：现金及等价物 $2.178B，长期债务 $2.534B，净债务约 $0.36B；流动资产 $4.701B，流动负债 $1.805B，流动比率约 **2.6x**；股东权益约 $6.205B，债务/权益约 **0.41x**。TTM FCF 约 $1.34B，净债务/TTM FCF 约 **0.3x**。财务状况很健康，短期偿债压力低。

需要注意的是，Spirent 等并购后 goodwill + intangibles 约 $4.7B，占总资产约 41%；若并购整合或增长不及预期，未来存在减值风险。债务从 FY24 的 $1.79B 上升到 FY25/FY26Q1 的 $2.53B，但在 FCF 规模下仍很温和。

## 2. 最新及最近四次财报

### 2.1 五个季度核心财报表

| 财报 | 披露日 | Orders | Revenue | Book-to-bill | EPS / FCF | 分部收入与利润率 | End market 收入 | Backlog / 交期 / 取消率 | AI 数据中心相关判断 |
|---|---:|---:|---:|---:|---|---|---|---|---|
| FY26 Q1，至 2026-01-31 | 2026-02-23 | **$1.645B，+30% YoY** | **$1.600B，+23% YoY；core +14%** | **1.03x** | Non-GAAP EPS **$2.17**；FCF **$407M** | CSG **$1.124B +27%**，GM 68%，OPM 27%；EISG **$476M +15%**，GM 62%，OPM 27% | Commercial Comm **$758M +33%**；ADG **$366M +18%**；EI **$476M +15%** | backlog 未披露；按 Q4 $2.697B + orders-revenue 粗推约 **$2.74B**；10-K 称多数 backlog 6 个月内转收入；取消率未披露 | 公司明确称商业通信订单受 AI data center、Edge AI、NTN/6G 推动；推断 AI/DC 相关收入 **$300-400M，约 19-25%** |
| FY25 Q4，至 2025-10-31 | 2025-11-24 | **$1.533B，+14% YoY** | **$1.419B，+10% YoY** | **1.08x** | Non-GAAP EPS **$1.91**；FCF **$188M** | CSG **$990M +11%**，GM 66%，OPM 27%；EISG **$429M +9%**，GM 60%，OPM 25% | Commercial Comm **$660M +12%**；ADG **$330M +9%**；EI **$429M +9%** | official backlog **$2.697B** vs FY24 $2.375B；增加来自 Spirent backlog + orders > revenue；多数 6 个月内转收入 | CSG 增长由 AI data center infrastructure、NTN、defense modernization 拉动；推断 AI/DC **$185-255M，13-18%** |
| FY25 Q3，至 2025-07-31 | 2025-08-19 | **$1.340B，+7% YoY** | **$1.352B，+11% YoY** | **0.99x** | Non-GAAP EPS **$1.72**；FCF **$291M** | CSG **$940M +11%**，GM 67%，OPM 26%；EISG **$412M +11%**，GM 57%，OPM 22% | Commercial Comm **$644M +13%**；ADG **$296M +8%**；EI **$412M +11%** | backlog 未披露；按 orders-revenue 粗推小幅消耗；交期仍以 6 个月内为主 | AI 互连和半导体复苏开始显性化；推断 AI/DC **$135-200M，10-15%** |
| FY25 Q2，至 2025-04-30 | 2025-05-20 | **约 $1.316B，+8% YoY** | **$1.306B，+7% YoY** | **1.01x** | Non-GAAP EPS **$1.70**；FCF **$457M** | CSG **$913M +9%**，GM 67%，OPM 26%；EISG **$393M +5%**，GM 59%，OPM 23% | Commercial Comm **$612M +9%**；ADG **$301M +9%**；EI **$393M +5%** | backlog 未披露；orders 略高于 revenue；取消率未披露 | 管理层称机会 funnel 健康；AI/DC 仍在早期，推断 **$105-155M，8-12%** |
| FY25 Q1，至 2025-01-31 | 2025-02-25 | **$1.263B，+4% YoY** | **$1.298B，+3% YoY** | **0.97x** | Non-GAAP EPS **$1.82**；FCF **$346M** | CSG **$883M +5%**，GM 68%；EISG **$415M -1%** | Commercial Comm **$572M +5%**；ADG **$311M +5%**；EI **$415M -1%** | backlog 未披露；Q1 book-to-bill <1，仍处渐进复苏 | AI 互连尚未成为财报叙事主线；推断 **$90-130M，7-10%** |

### 2.2 财报趋势判断

1. 订单恢复比收入更快：FY25 Q1 book-to-bill 0.97x，到 FY25 Q4 1.08x，FY26 Q1 仍 1.03x；说明不是单纯交付旧 backlog，而是新需求在补。
2. AI 相关叙事从“隐含需求”变成官方措辞：FY26 Q1 presentation 直接写到 AI data center、Edge AI、高速 PCB/interconnect、memory wafer test。
3. 毛利率强于一般硬件公司：Q1 FY26 非 GAAP GM 68.5%，说明高端仪器、软件、服务和应用方案占比较高。
4. backlog 可见度中等：官方只披露 FY25 期末 backlog $2.697B，多数 6 个月内转收入；这支持短期收入，但不是多年电力设备式 backlog。
5. Q2 FY26 指引明显高于历史 run-rate：公司指引 revenue **$1.690-1.710B**、Non-GAAP EPS **$2.27-2.33**，中点同比约 +30%。截至写作日，Q2 FY26 财报尚未发布，公司已公告将于 **2026-05-19** 披露。

## 3. FY26 最新指引、业务占比与重点产品

### 3.1 Q1 FY26 实际收入占比与 Q2 指引拆解

| 口径 | Q1 FY26 实际 | YoY | 收入占比 | Q2 FY26 指引推断 |
|---|---:|---:|---:|---|
| Commercial Communications | $758M | +33% | 47.4% | $800-860M；AI data center + Spirent + wireless/NTN 拉动 |
| Aerospace, Defense & Government | $366M | +18% | 22.9% | $375-410M；EMSO、space/satellite、PNT、欧洲/美国 primes |
| Electronic Industrial | $476M | +15% | 29.8% | $485-520M；semiconductor wafer test、memory、AI high-speed PCB |
| Total | $1.600B | +23% | 100% | 官方指引 $1.690-1.710B，中点 +30% YoY |

最突出的业务是 CSG 中的 commercial communications：Q1 +33%，同时也是 AI 数据中心 exposure 最集中的池子。EISG 虽然 headline 是 industrial，但 Q1 presentation 明确提到 semiconductor wafer test 因 memory 和 domestic semiconductor capacity expansion 双位数增长、general electronics orders 受 AI-related high-speed PCB and interconnect demand 推动，因此不能把 EISG 全部视为低速业务。

### 3.2 重点产品与跳过产品

**可跳过/低优先产品：**传统汽车电子测试、通用电子教育/实验室仪器、成熟 5G 手机终端测试、普通校准/维修服务、非 AI 工业自动化、电池/充电测试中的低速部分。这些业务稳定但不是当前估值弹性来源。

**重点产品/潜力小业务：**

| 业务/产品 | 对应产品型号或平台 | 目前状态 | 为什么重要 |
|---|---|---|---|
| 1.6T AI fabric / Ethernet workload emulation | **AresONE 1600GE**、**KAI DC Builder**、IxNetwork、INPT-1600GE | 2026-03 OFC 发布/展示 | 1.6T 以太网、RoCEv2、AI collective、拥塞控制从芯片样品走向系统验证 |
| 224G/1.6T 光电一致性测试 | **N1095DJCA**、**N1091DJPA**、**N1096 DCA-M**、DCA-X/DCA-M | 2026-03 推 224G IEEE 802.3dj-aligned 方案 | 1.6T 光模块从 R&D 到 HVM 必须测 TDECQ/TDECQ-CER、BER、FEC margin |
| 220GHz 光电组件分析 | **N4378A Lightwave Component Analyzer**、NA5305A/NA5307A extender、PNA/PNA-X | 2026 OFC 推出 | 面向 1.6T/3.2T 光组件、PIC、调制器、PD，属于高端光子测试小而高毛利业务 |
| PCIe/CXL/UALink scale-up validation | **M8050A 120 Gbd BERT**、Infiniium UXR、PCIe 7 Tx/Rx、PCIe 6 protocol compliance、CXL 3 exerciser/analyzer、UALink 200G receiver conformance | 2026 DesignCon/Scale-up portfolio | AMD Helios、自研 ASIC、CXL memory、开放 scale-up 都需要标准化合规和互操作 |
| 448G pathfinding | **M8199B AWG**、**N1046A electrical channel module**、UXR/DCA/VNA/PLTS | 2026 DesignCon demo | 448G 仍早，但 2026-2027 的研发订单会提前进入高端实验室 |
| Chiplet/3DIC/photonic EDA | Chiplet 3D Interconnect Designer、PathWave ADS/SystemVue/EMPro、Synopsys OSG、PowerArtist RTL | 2025-10 并购后交叉销售 | CPO/光 I/O/AI ASIC 需要“仿真-实测 correlation”，软件 attach 提高 recurring revenue |
| Semiconductor wafer / memory test | EISG wafer test、parametric/RF/optical probe、memory/HBM 相关验证 | Q1 FY26 双位数增长 | HBM4、SerDes、硅光、国内半导体扩产提高测试强度 |

## 4. 当前关键产品：收入贡献、增速、重要性与定价权

| 关键业务/产品 | 当前收入贡献估计 | 当前增速估计 | AI 基建重要性 | 时间紧急性 | 供需紧张度 | 垄断/溢价能力 |
|---|---:|---:|---|---|---|---|
| AresONE 1600GE / AI fabric emulation / IxNetwork | FY26 run-rate **$500-750M**，Q1 约 $110-160M | +35-60% | 很高：验证 AI Ethernet/1.6T fabric、RoCEv2、拥塞、job completion time | 很高：2026H2-2027 1.6T/UEC/AI Ethernet 导入前必须验证 | 高：1.6T 测试设备和资深应用工程稀缺 | 高：Keysight/Ixia 安装基数强，但 VIAVI 收购 Spirent HSE 后竞争加剧 |
| 224G/1.6T 光电 PHY 测试（DCA/BERT/VNA/LCA） | FY26 run-rate **$450-650M**，Q1 约 $90-140M | +40-70% | 很高：1.6T 光模块、CPO、silicon photonics 的量产 gate | 很高：OFC 2026 后客户进入 qual/HVM | 很高：高端 DCA/LCA/VNA 交期和应用支持紧张 | 很高：高带宽、校准、标准一致性壁垒强 |
| PCIe/CXL/UALink validation | FY26 run-rate **$250-380M**，Q1 约 $50-80M | +30-55% | 高：AI rack 内 CPU/GPU/NIC/retimer/CXL memory 互连 | 高：PCIe 6/7、CXL 3、UALink 200G 正在 design-in | 中高：协议和一致性软件稀缺，硬件可多供 | 高：PCI-SIG certified、协议深度和互操作数据库形成粘性 |
| EDA/Chiplet/Photonic/Power software | FY26 run-rate **$180-280M** | +20-40% | 中高：早期设计验证、光电 correlation、低功耗设计 | 中高：AI ASIC、CPO、光 I/O 设计提前 12-24 个月发生 | 中：软件交付不受硬件产能约束 | 中高：Cadence/Synopsys/Siemens 竞争强，但 Keysight 的测量闭环差异化 |
| Semiconductor wafer/memory/AI high-speed PCB test | FY26 run-rate **$300-450M** | +20-45% | 中高：HBM/SerDes/封装/PCB 良率与可靠性 | 高：HBM4、224G PCB、domestic semicap 扩张并行 | 中高：高端 probe/parametric/optical test 工程资源紧张 | 中：与 Advantest/Teradyne/FormFactor 等生态重叠，KEYS 更偏验证而非主 ATE |
| ADG/Space/PNT/EMSO（含 Spirent PNT） | FY26 run-rate **$1.5-1.7B** | +12-20% | 对 AI DC 间接，但对公司现金流和估值下限重要 | 高：美国/欧洲国防现代化、卫星通信、PNT | 中高：国防测试认证周期长、供应商少 | 高：认证、长期项目、系统级集成粘性强 |

合计看，FY26 AI 直接/邻近收入贡献估计 **$1.5-2.1B**，占公司 FY26E revenue 的 **22-30%**。这不是官方披露数字，而是由 commercial communications、EISG wafer/high-speed interconnect、产品发布节奏和项目内高速互连模型反推。

## 5. 一年后关键产品贡献：基准/乐观/极度乐观

| 产品/业务 | 未来一年基准 | 未来一年乐观 | 未来一年极度乐观 |
|---|---|---|---|
| AI fabric / AresONE 1600GE / IxNetwork | revenue **$650-850M**，+25-40%；重要性很高；供需中高；溢价高 | **$850M-1.1B**，+45-65%；1.6T/UEC/AI Ethernet 多客户并行验证；供不应求 | **$1.1-1.4B**，+75-100%；3.2T/400G-lane pathfinding 提前，客户抢实验室系统 |
| 224G/1.6T optical PHY test | **$600-800M**，+30-50%；测试成为光模块 HVM gate | **$800M-1.05B**，+60-85%；1.6T 短缺延续、LCA/DCA/BERT 交期拉长 | **$1.05-1.35B**，+90-120%；3.2T/CPO/448G 同时启动，设备 ASP 与软件 license 上行 |
| PCIe/CXL/UALink validation | **$320-470M**，+25-40%；PCIe6/CXL3 进入新平台 | **$470-650M**，+50-75%；AMD/custom ASIC/UALink 生态放大 | **$650-850M**，+85-120%；开放 scale-up 成第二标准，hyperscaler 多套 testbed |
| EDA/Chiplet/Photonic software | **$240-340M**，+25-35%；并购资产交叉销售 | **$340-480M**，+45-70%；CPO/光 I/O 设计密集 | **$480-650M**，+80-120%；光电协同设计成为高端 ASIC 标配 |
| Semiconductor wafer/memory/PCB test | **$380-550M**，+25-40%；HBM4 和 AI high-speed PCB | **$550-750M**，+55-75%；domestic semicap + memory 双拉动 | **$750M-1.0B**，+90-130%；测试时间成为先进封装/HBM 真实瓶颈 |
| ADG/Space/PNT/EMSO | **$1.7-1.9B**，+10-18%；防务预算稳定 | **$1.9-2.1B**，+20-28%；PNT/space/EMSO 项目加速 | **$2.1-2.4B**，+35%+；欧洲与美国多项目提前采购 |

## 6. BOM、每 MW/rack/GPU/port 内容量、价格传导、产能与认证

Keysight 不是数据中心 BOM 中的“每台服务器装一个”的零部件，而是供应链研发、认证、量产和客户验收的测试资本开支。合理的含量口径应按“测试设备/软件在光模块、交换机、ASIC、CPO、PCIe/CXL 产品收入中的摊销”测算。

### 6.1 内容量与价格传导

| 产品/业务 | BOM/测试站构成 | 每 optical port 内容量 | 每 rack 内容量 | 每 MW 内容量 | 价格传导链 |
|---|---|---:|---:|---:|---|
| 1.6T Ethernet / AI fabric emulation | AresONE 1600GE chassis、OSFP 1600 ports、KAI DC Builder、IxNetwork license、support | 客户实验室摊销约 **$20-80/port**；早期 qual 可更高 | 36-72 个 1.6T/800G 等效端口/rack，摊销约 **$1k-8k/rack** | 8-12 racks/MW，约 **$10k-90k/MW** | hyperscaler/NEM/silicon vendor 购买 testbed；若新标准风险高，客户愿意为缩短 bring-up 付费 |
| 224G/1.6T 光电 PHY 测试 | DCA-X/DCA-M、BERT、AWG、VNA/LCA、clock recovery、fixture、IEEE 802.3dj app、calibration | HVM 摊销 **$10-60/port**；早期 1.6T/3.2T **$50-150/port** | **$2k-15k/rack** | **$20k-150k/MW** | 光模块/硅光/PIC 厂先买 R&D/HVM 测试，测试成本随模块 ASP 传导；短缺期客户接受更高测试摊销 |
| PCIe/CXL/UALink validation | M8050A BERT、UXR scope、protocol exerciser/analyzer、compliance suite、CXL/PCIe/UALink software | 按 GPU/NIC/retimer 链路摊销，约 **$10-50/GPU** | 72 GPU rack 约 **$0.7k-4k/rack** | 600-900 GPU/MW，约 **$6k-45k/MW** | CPU/GPU/NIC/retimer/ODM 研发预算支付；进入 PCI-SIG/客户认证后形成软件续费 |
| EDA/Chiplet/Photonic software | license、solver、layout/thermal/power analysis、measurement correlation | 按 ASIC 项目 NRE，不适合 per port；每个高端项目 **$0.5-5M/年** | 间接 | 间接 | 设计阶段由 ASIC/光子/封装团队支付；若 tape-out 节省一次 respin，ROI 极高 |
| Semiconductor wafer/memory/PCB test | wafer parametric/RF/optical test、probe station、automation、application software | 按 chip/PCB 摊销约 **$5-30/GPU/XPU** | **$0.5k-3k/rack** | **$5k-30k/MW** | HBM/SerDes/PCB 良率越低，客户越愿意前置测试；价格由测试时间和良率收益决定 |

### 6.2 当前产能能力与认证阶段

| 产品/业务 | 当前产能能力（美元计，推断） | 供应链采纳程度 | 认证/标准阶段 |
|---|---:|---|---|
| AresONE 1600GE / AI fabric | FY26 可交付 **$0.6-0.8B** | NEM、silicon vendor、hyperscaler lab early deployment；Ixia 安装基础强 | 1.6T Ethernet / 224G SerDes / RoCEv2 workload emulation；非单一认证，属系统验证平台 |
| 224G optical/electrical test | FY26 可交付 **$0.5-0.7B** | 光模块、PIC、DSP、switch ASIC 供应链快速采纳 | IEEE 802.3dj-aligned；N1095/N1091/N1096 面向 conformance readiness/HVM |
| PCIe/CXL/UALink | FY26 可交付 **$0.3-0.4B** | PCIe/CXL 生态成熟；UALink 处早期验证 | PCIe 5 protocol link/transaction solution 已获 PCI-SIG certification；PCIe 6/7、CXL 3、UALink 200G 处验证/一致性阶段 |
| N4378A 220GHz LCA | FY26 可交付 **$50-120M** | 先进光器件/PIC/科研和头部模块厂早期采用 | 面向 1.6T/3.2T 光组件，OFC 2026 后进入客户 eval |
| EDA/photonic/power software | FY26 可交付 **$0.2-0.3B** | 并购资产需要交叉销售验证 | OSG/PowerArtist 已并入 KEYS；客户流转和工具链整合是关键 |

## 7. 一年后产能、采纳与认证情景

| 产品/业务 | 基准：一年后 | 乐观：一年后 | 极度乐观：一年后 |
|---|---|---|---|
| AresONE / AI fabric | 可交付 **$0.8-1.0B**；1.6T testbed 成头部 NEM/云厂标准配置 | **$1.1-1.3B**；UEC/UALink/AI Ethernet 并行，客户重复采购 | **$1.4-1.7B**；3.2T/400G-lane testbed 提前，交期成为瓶颈 |
| 224G/1.6T optical PHY | **$0.8-1.0B**；1.6T HVM 与 IEEE 802.3dj conformance 成常规配置 | **$1.1-1.4B**；1.6T + CPO + 3.2T 使 DCA/LCA/BERT 并行上量 | **$1.5-1.9B**；测试站短缺，客户按产能预订，软件 license 提价 |
| PCIe/CXL/UALink | **$0.45-0.6B**；PCIe6/CXL3 常规化 | **$0.65-0.85B**；UALink 200G 与 PCIe7 早期项目并行 | **$0.9-1.2B**；开放 scale-up 生态成型，客户平台测试矩阵扩大 |
| EDA/Photonic/Power software | **$0.3-0.4B**；并购工具进入 PathWave/EDA 销售 | **$0.45-0.6B**；CPO/optical I/O 项目带动 photonic design | **$0.65-0.85B**；光电协同设计成为 AI ASIC 标配，recurring license 上升 |
| Semiconductor wafer/memory/PCB test | **$0.5-0.7B**；HBM4 NPI、AI PCB 验证 | **$0.75-1.0B**；domestic semicap + HBM4 + SerDes 三重拉动 | **$1.1-1.4B**；前道/封装/系统测试全面瓶颈化 |

## 8. backlog、订单与供给推断：未来一年业务增速

### 8.1 总公司层面

| 情景 | 未来一年收入预测 | 增速判断 | 推理依据 |
|---|---:|---:|---|
| 基准 | **$6.7-7.1B** | +18-25% vs FY25 | Q1 $1.60B + Q2 guide $1.70B；backlog $2.7B，多数 6 个月内转收入；Spirent full-year contribution |
| 乐观 | **$7.2-7.7B** | +34-43% vs FY25 | Q2 beat、Q3/Q4 保持 book-to-bill >1.05；AI data center + defense + EISG memory 持续 |
| 极度乐观 | **$7.8-8.4B** | +45-56% vs FY25 | 1.6T/224G 测试设备交期拉长，客户抢购；并购交叉销售超预期 |

基准更可信。KEYS 的收入不是光模块/服务器那样随 AI 订单爆炸式线性放大，原因是高端测试仪器交付受应用工程、校准、客户验收和项目节奏影响；但其毛利和现金流弹性优于普通硬件。

### 8.2 关键业务层面

| 业务 | 基准增速 | 乐观增速 | 极度乐观增速 | 订单/供给验证方式 |
|---|---:|---:|---:|---|
| AI fabric / Ethernet emulation | +25-40% | +45-65% | +75-100% | 1.6T switch/NIC silicon validation、OFC/DesignCon 客户 demo、IxNetwork license 扩容 |
| 224G/1.6T optical test | +30-50% | +60-85% | +90-120% | 光模块厂 HVM station、DCA/BERT/LCA lead time、IEEE 802.3dj conformance adoption |
| PCIe/CXL/UALink | +25-40% | +50-75% | +85-120% | PCI-SIG/CXL/UALink test suite、AMD/custom ASIC/retimer 客户 design-in |
| EDA/photonic software | +25-35% | +45-70% | +80-120% | OSG/PowerArtist cross-sell、CPO/光 I/O 项目数、EDA recurring attach |
| EISG wafer/memory/PCB | +25-40% | +55-75% | +90-130% | memory wafer test orders、domestic semicap、AI high-speed PCB design win |

取消率判断：公司没有披露取消率。10-K 风险提示提到订单可能被取消或延迟，但过去五个季度未见公开异常取消信号。AI 验证设备的主要风险更可能是客户项目延期、标准路线变化或电力/服务器上电延迟，而非已下订单大规模取消。

## 9. 竞争格局、技术路线和替代风险

### 9.1 主要竞争对手

| 细分 | KEYS 竞争对手 | KEYS 优势 | 风险 |
|---|---|---|---|
| 高端示波器/DCA/BERT/AWG/VNA | Tektronix、Teledyne LeCroy、Anritsu、Rohde & Schwarz、Yokogawa、VIAVI | 测量精度、标准参与、全链路产品组合、校准服务 | 单点仪器可能被竞品替代；客户会多供应商配置 |
| 网络协议/以太网 traffic test | VIAVI、Spirent legacy assets、Xena/Teledyne、EXFO | Ixia installed base、IxNetwork、AresONE 1600GE | VIAVI 收购 Spirent HSE 后在高速以太网测试竞争力增强 |
| PCIe/CXL/协议测试 | Teledyne LeCroy、Tektronix、VIAVI、Synopsys/Cadence VIP、GRL/Allion | PHY + protocol + software + scope/BERT 一体化 | 认证实验室和 EDA VIP 可分流部分价值 |
| EDA/Chiplet/photonic | Cadence、Synopsys、Siemens EDA、Ansys residual assets、Rambus/Alphawave IP | 与真实测量设备结合，适合 simulation-to-measurement correlation | EDA 主平台仍由 Cadence/Synopsys/Siemens 主导 |
| Semiconductor production test | Advantest、Teradyne、Cohu、Chroma、FormFactor/MPI | 验证、parametric、RF/光电测试强 | 大规模 SoC/HBM ATE 不是 KEYS 主战场 |
| RF/无线/6G/NTN | Rohde & Schwarz、Anritsu、NI/Emerson、VIAVI | 6G/NTN/space/defense 应用和系统级方案强 | 5G 手机测试周期趋弱，价格竞争可能压制 |

### 9.2 新技术是否是主流

| 技术 | 是否会成为主流 | KEYS 受益确定性 | 替代风险 |
|---|---|---|---|
| 800G/1.6T pluggable | 2026-2027 主流，1.6T 在 2027 高端新增 AI fabric 占比提高 | 很高 | ASP 下行不影响测试需求，但可能影响客户 capex 节奏 |
| 224G electrical / IEEE 802.3dj | 1.6T 的核心接口，2026-2027 必测 | 很高 | 若 CPO/LPO 路线分化，测试项目改变但测试复杂度不降低 |
| 3.2T / 400G-per-lane | 2027 小批量/验证，2028 后更主流 | 高，且领先收入早于器件量产 | 时间可能推迟；但 pathfinding 仪器先卖 |
| PCIe 6/7、CXL 3、UALink 200G | 开放 AI rack 和内存池化的关键路线 | 高 | NVIDIA NVLink 封闭生态会分流，但 AMD/custom ASIC/云厂 ASIC 需要开放互连 |
| CPO/CPX/XPO | 2026 pilot，2027 高端 switch 小批量，2028 扩大 | 中高，测试需求一定存在 | 架构赢家未定；供应链价值可能被平台公司内化 |
| OCS | Google/TPU 强，GPU/Ethernet 生态仍早 | 中 | OCS 若不扩散到非 Google，市场较窄；但光链路测试仍受益 |

客户替换成本高。高端测试设备进入客户流程后，不只是硬件替换问题，还包括校准、脚本、自动化、历史 correlation 数据、工程师培训、合规报告模板和供应商 FAE 响应。对 hyperscaler、NEM、芯片厂而言，换测试平台可能导致重跑 qualification，成本远高于仪器价差。因此 KEYS 的溢价能力来自“标准参与 + 数据连续性 + 失败定位能力”，不只是仪器带宽。

### 9.3 主要风险

1. 估值风险：当前股价已反映 AI 互连验证高景气，若 Q2/Q3 orders 不持续，multiple 容易压缩。
2. AI capex 延期：电力、液冷、HBM、GPU 上电延迟会推迟客户测试扩容。
3. VIAVI/Spirent 竞争：VIAVI 获得 Spirent 高速以太网/网络安全/信道仿真资产后，对 Keysight/Ixia 构成更强制衡。
4. 并购整合风险：Spirent、OSG、PowerArtist、Riscure、AnaPico 需要整合销售、产品路线和成本。
5. 出口管制/关税：公司 Q1 FY26 outlook 明确排除 2026-02-20 IEEPA tariff ruling 及后续行政动作影响；中国/出口限制会影响客户采购。
6. 技术路线分裂：LPO/LRO/CPO/XPO/OCS/UALink/UEC 并行，客户库存和测试平台投资节奏可能波动。
7. 自研和替代：头部 hyperscaler、NVIDIA/Broadcom/Marvell 可能把部分测试/仿真内化或绑定自有生态。

## 10. 投资判断摘要

KEYS 的好处是“卖铲子但不卖通用铲子”：AI 互连每次从 800G 到 1.6T、从 112G 到 224G、从 PCIe 5 到 PCIe 7，客户都要重新买硬件、软件、夹具、校准和服务。它的收入弹性低于光模块和交换芯片，但利润质量更高，且需求领先量产 6-18 个月。

短期最关键跟踪项：

1. 2026-05-19 Q2 FY26 财报：收入是否超过 $1.70B、orders 是否继续大于 revenue。
2. Commercial Communications 增速是否继续 >30%，AI data center 是否仍是管理层第一顺位叙事。
3. Q2/Q3 是否披露 1.6T、224G、PCIe/CXL、Spirent 整合的更多数字。
4. Backlog 是否继续高于 $2.7B，且 deferred revenue 是否上升。
5. Q2 FY26 毛利是否维持高位；若并购摊销和整合成本压低 GAAP，但 non-GAAP GM 维持，质量仍可接受。

一句话：KEYS 是 AI 数据中心“验证瓶颈”的高质量受益者，核心增量来自 1.6T/224G 光电、AI Ethernet fabric、PCIe/CXL/UALink 和光子/Chiplet EDA；但当前估值已经把它从传统测试测量公司重新定价为 AI/EDA 邻近资产，后续股价最怕 orders 低于高预期。

## 资料来源

### 公司官方与财报

- Keysight FY26 Q1 results: https://investor.keysight.com/investor-news-and-events/financial-press-releases/press-release-details/2026/Keysight-Technologies-Reports-First-Quarter-2026-Results/default.aspx
- Keysight FY26 Q1 results presentation: https://s22.q4cdn.com/444849635/files/doc_earnings/2026/q1/presentation/Q1-26-Results-Presentation.pdf
- Keysight FY25 Q4 and FY2025 results: https://investor.keysight.com/investor-news-and-events/financial-press-releases/press-release-details/2025/Keysight-Technologies-Reports-Fourth-Quarter-and-Fiscal-Year-2025-Results/default.aspx
- Keysight FY25 Q3 results: https://investor.keysight.com/investor-news-and-events/financial-press-releases/press-release-details/2025/Keysight-Technologies-Reports-Third-Quarter-2025-Results/default.aspx
- Keysight FY25 Q2 results: https://investor.keysight.com/investor-news-and-events/financial-press-releases/press-release-details/2025/Keysight-Technologies-Reports-Second-Quarter-2025-Results/default.aspx
- Keysight FY25 Q1 results: https://investor.keysight.com/investor-news-and-events/financial-press-releases/press-release-details/2025/Keysight-Technologies-Reports-First-Quarter-2025-Results/default.aspx
- Keysight 2025 10-K / annual report summary: https://www.stocktitan.net/sec-filings/KEYS/10-k-keysight-technologies-inc-files-annual-report-114ddb39368a.html
- Spirent acquisition completion: https://investor.keysight.com/investor-news-and-events/financial-press-releases/press-release-details/2025/Keysight-Technologies-Completes-Acquisition-of-Spirent-Communications-PLC/default.aspx
- Q2 FY26 report date: https://investor.keysight.com/investor-news-and-events/financial-press-releases/press-release-details/2026/Keysight-Technologies-to-Report-Fiscal-Second-Quarter-Results-on-May-19-2026/default.aspx

### 产品、行业与会议

- Keysight AI data center scale-up validation solutions: https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0218-pr-026-keysight-introduces-scale-up-validation-solutions-for-ai-data-centers.html
- Keysight DesignCon 2026 AI data center/high-speed interconnect demos: https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0209-pr26-028-keysight-to-showcase-advanced-ai-data-center-and-high-speed-interconnect-validation-at-designcon-2026.html
- Keysight AresONE 1600GE / KAI DC Builder: https://www.keysight.com.cn/cn/zh/about/newsroom/news-releases/2026/0310_pr26-044-keysight-debuts-purpose-built-1-6t-ethernet-ai-workload-emulation-platform-to-validate-next-generation-ai-fabrics.html
- Keysight 224G / 1.6T optical network validation: https://www.design-reuse.com/news/202530231-keysight-introduces-new-224g-test-solutions-to-enable-1-6t-optical-network-validation/
- Keysight Lightwave Component Analyzers / N4378A 220GHz LCA: https://www.keysight.com/us/en/products/photonic-and-optical-test/photonic-component-analyzers/lightwave-component-analyzers.html

### 行情与估值

- Yahoo Finance chart API for KEYS close price: https://query1.finance.yahoo.com/v8/finance/chart/KEYS?range=5d&interval=1d
- StockAnalysis KEYS statistics and valuation: https://stockanalysis.com/stocks/keys/statistics/

### 项目内参考资料（未使用“公司调研”目录）

- `D:\drive\Investment\工作台v5\行业调研_晶圆制造_设备_材料_测试\行业调研_高速互连与光学验证测试_2026-05-08.md`
- `D:\drive\Investment\工作台v5\行业调研_AI网络_光互联_铜互联\行业调研_800G_1.6T可插拔光模块_2026-05-08.md`
- `D:\drive\Investment\工作台v5\行业调研_AI网络_光互联_铜互联\行业调研_PCIe_CXL高速IO交换与Retimer_2026-05-08.md`
- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\行业调研\行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\行业调研\行业调研/AI头部芯片市场占比和规模.md`
- `D:\drive\Investment\工作台v5\conference_update\ofc_2026_conference_update.md`
- `D:\drive\Investment\工作台v5\conference_update\designcon_2026_conference_update.md`

---

非投资建议。本文的产品级收入、AI 占比、每 MW/rack/port 内容量和一年后情景为研究推断，不是公司指引。

