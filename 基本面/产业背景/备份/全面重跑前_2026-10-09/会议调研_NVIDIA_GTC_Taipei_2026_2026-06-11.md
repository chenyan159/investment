# NVIDIA GTC Taipei 2026会议追踪：核心变化、产品爆发和市场预期差

会议日期：2026-06-01 至 2026-06-04  
会议地点：Taipei Music Center（2026-06-01 keynote）与 Taipei International Convention Center（2026-06-02 至 2026-06-04 workshops、conference、demo showcase）  
材料检索截止日期：2026-06-11  
报告完成日期：2026-06-11  
资料边界：本报告独立追踪公开会议和公开公司材料，未读取或继承项目内旧报告、旧索引、缓存和中间结论。  
证据等级：A=公司/会议/监管一手资料；B=合作方一手材料或专业市场机构；C=媒体/券商/论坛/社交分享；C级只做线索，不单独支撑核心结论。

## 结论摘要

1. 本届 GTC Taipei 不是单一 GPU 发布会，而是 NVIDIA 把“AI factory”从芯片叙事推进到可施工、可运营、可计量的基础设施体系：Vera Rubin 已进入 full production，Vera Rubin 系统从 2026 年秋季开始出货；DSX 把设计、仿真、液冷、电力、运维、租户隔离和 token/MW 统一进平台；Spectrum-X Ethernet Photonics 已投产，CPO 从“未来概念”变成 2026-2027 年 AI 网络的实物路线。证据等级 A。

2. 最重要的短期投资变化在“GPU 之外”：NVIDIA FY2027 Q1（截至 2026-04-26）Data Center 收入 752 亿美元，同比增长 92%；其中按旧口径 Data Center compute 为 604 亿美元，networking 为 148 亿美元，同比增长 199%，networking 已相当于年化 592 亿美元收入池。会议进一步把利润池扩到 CPO/交换、BlueField-4/STX 安全存储、800Gb/s DPU、800V DC 电力、45 摄氏度液冷和 DSX 运维软件。

3. Vera Rubin 的真实变化不是“下一代 GPU 又快了”，而是推理/agentic workload 的系统级成本函数变了：NVIDIA 宣称 Vera Rubin 在 agent throughput 上较 Grace Blackwell 提升 10 倍；Vera CPU 为 88 个 Olympus cores、LPDDR5X 带宽最高 1.2TB/s，任务完成速度较 x86 CPU 快 1.8 倍；BlueField-4/DOCA 可在 800Gb/s 数据路径上做隔离和安全策略，STX 平台预计 2026 年下半年由合作伙伴供货。核心看点从“每张 GPU”转为“每 MW、每 token、每 agent 工单”的收益。

4. CPO/硅光是本届会议最值得上修的硬件方向。NVIDIA 把 Spectrum-X Ethernet Photonics 定义为 CPO-based switches、200Gb/s SerDes、已投产，并宣称相对传统 transceiver 网络可提供 5 倍能效、5 倍 AI uptime、1.3 倍部署速度。TrendForce 2026-04-20 预计 2026 年 AI optical transceiver 市场达 260 亿美元；Dell'Oro 2026-02-04 预计 AI back-end switch 市场 2030 年超过 1000 亿美元。会议后的判断：2026-2027 年不会是 pluggable 被 CPO 立刻替代，而是 800G/1.6T pluggable、LPO 与 CPO 并行，CPO 先进入超大规模/百万 GPU 级别 fabric。

5. 电力和液冷不再是机房工程配套，而是 AI 工厂产能瓶颈。DSX MaxLPS 使用 45 摄氏度液冷和 rack 内功耗优化，在固定电力预算内最多可运行 40% 更多 GPU。液冷市场的 2026 年公开口径差异较大：GMI 为 60 亿美元、Grand View 为 81.7 亿美元、MarketsandMarkets 为 40.7 亿美元，合理基准区间取 50-80 亿美元；TrendForce 预计 2026 年 AI chip 液冷渗透率可达 47%。800V DC 仍处早期，但 TI 与 NVIDIA 的 800V DC 方案显示高压直流将从 white paper 进入参考设计和供应链验证。

6. RTX Spark 与 DGX Station for Windows 打开了“local agent / personal AI computer”新产品线，但 2026 年不应按普通 PC 全量替代来估值。RTX Spark 规格很强：1 PFLOP AI 性能、最高 128GB unified memory、6144 CUDA cores、20-core Grace CPU、MediaTek 共同设计，首批笔记本 2026 年秋季上市；DGX Station for Windows 则为 GB300 桌面超算，最高 748GB coherent memory、20 PFLOPS FP4、Q4 2026 上市。短期更像高端开发者/创作者/企业 agent 节点，而不是立刻改变 2026 年 PC 大盘。

7. Physical AI/robotics 的会议声量高，但收入兑现节奏要分层。Cosmos 3、Isaac GR00T 1.7、Isaac Sim 6.0、Isaac ROS 4.4、Jetson Thor、Unitree G1 参考工作流构成了机器人开发栈；GR00T 模型下载 27.4 万次、GR00T X Embodiment Sim 数据集下载超过 1000 万次，是生态扩散证据。但 Gartner 2026-01-21 预计到 2028 年能在制造/供应链生产阶段规模化 humanoid 的公司少于 20 家。未来 12 个月更强的投资弹性可能在传感器、执行器、边缘算力、仿真、遥操作、数据集和验证工具，而不是 humanoid 整机收入。

8. 反共识判断：市场容易把“Ethernet 开放”理解为 NVIDIA 护城河弱化，但本届会议显示 NVIDIA 正在用 Spectrum-X、CPO、BlueField、DSX OS、NVLink 与 secure agent runtime 把 Ethernet 纳入自己的 full-stack AI factory 控制面。真正需要上修的是“非 GPU 价值占比”，不是简单下修 NVIDIA。

9. 最大风险是 AI 工厂建设的资金、电力、交付和客户 ROI 同时受压。若 2026 年下半年 hyperscaler/AI cloud capex 指引下修、Vera Rubin 秋季出货推迟、CPO 良率/成本不达标、GB300/NVL72 token 经济性未能兑现，或 agentic AI 进入企业生产后的有效需求低于会场预期，应下修本报告对 2027 年硬件放量的乐观情景。

## 会议重点和方向变化

| 核心主题 | 会议证据与技术参数 | 关联公司/生态 | 变化性质 | 投资含义 |
|---|---|---|---|---|
| Agentic AI factory 从 GPU 集群转为完整工厂 | Vera Rubin full production；五个 purpose-built racks 作为 POD-scale AI supercomputer；相对 Grace Blackwell agent throughput 10x；2026 年秋季开始 production shipments | NVIDIA、Dell、HPE、Lenovo、Supermicro、ASUS、Foxconn、GIGABYTE、Pegatron、QCT、Wistron、Wiwynn、CoreWeave、Oracle、Lambda 等 | 真实变化，已有生产和合作伙伴名单，但出货/收入仍看秋季节点 | GPU 之外的 rack、networking、DPU、storage、power/cooling、software attach 上修 |
| AI back-end network 与 CPO | Spectrum-X Ethernet Photonics：CPO-based switches、200Gb/s SerDes、已投产；宣称 5x 能效、5x uptime、1.3x 部署速度；BlueField-4 支持 800Gb/s | NVIDIA、CoreWeave、Lambda、OCI；潜在受益还包括高速光模块、硅光、激光器、连接器、测试设备 | 真实变化，CPO 从预期进入生产；但 2026 年仍是局部部署 | 高速光、交换、SerDes、封装/测试的利润池被重新定价 |
| DSX、液冷、电力与 token/MW | DSX MaxLPS 使用 45 摄氏度液冷，在固定 power budget 中最多运行 40% 更多 GPU；DSX OS 开源模块覆盖 lifecycle、health automation、multi-tenant operations | NVIDIA、CoreWeave、Crusoe、Firmus、IREN、Lambda、Nebius、Nscale、Yotta；Dell/HPE/Lenovo/SMCI 与台系 ODM | 真实变化，架构和软件公布；经济性需看客户部署 | 电力、液冷、运维软件从 capex 配套变成 token 成本控制核心 |
| CPU 与 storage/security 成为 agentic workload 瓶颈 | Vera CPU：88 Olympus cores、LPDDR5X 1.2TB/s、较 x86 任务完成 1.8x；BlueField-4 STX：DOCA Vault/Argus/Flow、800Gb/s、runtime threat detection 最高 1000x faster | NVIDIA、Anthropic、OpenAI、SpaceXAI、ByteDance、CoreWeave、OCI、NYSE、DDN、VAST、WEKA、NetApp、Cloudian、MinIO 等 | 真实变化，Vera full production；STX partner platforms 2026H2 | agent 运行时代价从 GPU token 扩到 CPU sandbox、文件访问、context memory 安全 |
| Secure agent runtime 与 open model | Nemotron 3 Ultra：550B MoE、复杂 agentic tasks 推理最高 5x faster、成本最高降 30%；NemoClaw/OpenShell 为安全 runtime；Build-a-Claw 在 Taipei 展示 | NVIDIA、Perplexity、Palantir、ServiceNow、Glean、Harvey、Dataiku、OpenClaw、Hermes、LangChain 等 | 部分真实，模型/软件已发布；商业 monetization 仍早期 | 软件本身未必直接大收入，但会拉动 token、local GPU、secure workspace 和 enterprise deployment |
| AI PC / personal agents | RTX Spark：1 PFLOP、最高 128GB unified memory、6144 CUDA cores、20-core Grace CPU、MediaTek 协作；Adobe Photoshop/Premiere 针对 Spark 2x AI/graphics；首批设备秋季 | NVIDIA、Microsoft、MediaTek、Adobe、ASUS、Dell、HP、Lenovo、Microsoft Surface、MSI、Acer、GIGABYTE | 产品化明确，但 sell-through 待验证 | 高端 AI PC/desktop agent hub 新品类；不要按全 PC 市场立即兑现 |
| DGX Station for Windows | GB300 Grace Blackwell Ultra Desktop Superchip；72-core Grace CPU；最高 748GB coherent memory、20 PFLOPS FP4；ConnectX-8 最高 800Gb/s；Q4 2026 | NVIDIA、Microsoft、ASUS、Dell、GIGABYTE、HP、MSI、Supermicro | 真实产品，Q4 供货节点明确 | 企业 deskside AI supercomputer，单价高、量小但毛利和开发者锁定价值高 |
| Physical AI / robotics | Cosmos 3 fully open omnimodel；GR00T 1.7 基于 20,000 小时 egocentric data，early access；Isaac Sim 6.0 GA、1000+ simulation-ready assets；Jetson Thor 部署 | Agility、Boston Dynamics、Dyna、Figure、FieldAI、Noble、Richtech、Skild、Foxconn、Lightwheel、PICO、Techman、Unitree | 技术栈加速，收入放量滞后 | 上游传感、执行、边缘算力、仿真和数据 flywheel 比整机更可跟踪 |
| Robotaxi/AV 平台 | DRIVE Hyperion L4-ready；Foxconn 计划台湾高雄先行、2028 年 airport-to-city 路线；Uber 整合多支 Hyperion fleets；Alpamayo 2 Super 为 32B VLA | NVIDIA、Foxconn/Foxtron、Uber、Autobrains、VinFast、HUMAIN | 中长期路线，订单/城市部署尚未兑现 | 2026-2027 主要看 design win 和试运营，不应提前按 2030+ TAM 兑现 |

本届与过去 6-12 个月市场预期相比的变化：

- 由“GPU 供不应求”升级为“AI 工厂全栈供不应求”：Q1 FY2027 数据显示 networking 增速远高于 compute，会议再把 CPO、BlueField、DSX、liquid cooling 推到前台。
- 由“training cluster”转为“agentic inference factory”：Vera Rubin、Vera CPU、Nemotron、NemoClaw、OpenShell 的共同指向是长时运行 agent 的推理、工具调用、文件访问、沙盒执行和安全治理。
- 由“机房设施跟随 IT”转为“电力/冷却决定 GPU 可用产能”：DSX MaxLPS 的核心不是节能形象，而是在固定 MW 下多跑 GPU，等价于提高数据中心“有效算力产能”。
- 由“物理 AI 概念”转为“机器人开发流水线”：Cosmos 3、Isaac Teleop、Isaac Lab、Isaac Sim、Isaac ROS、Jetson Thor、Unitree G1 reference workflow 打通了数据、仿真、训练、验证、部署。
- AI PC 的确定性上升，但它首先是高端开发者/agent runtime 新品类，不能简单套用普通 PC replacement cycle。

对未来判断的改变：

- 未来 3 个月：重点跟踪 Vera Rubin 供应链订单、CPO/800G/1.6T optics 交期、liquid cooling 排产、GB300/DGX Station 渠道预订、hyperscaler Q2 capex 指引。
- 未来 1 年：AI factory 的利润池将从 GPU 卡扩展到 rack-scale system、networking、DPU/storage security、power/cooling 和 software operations；台系 ODM、光模块、硅光、液冷、电源和测试验证环节的经营数据更可能出现弹性。
- 未来 2 年：若 agentic workload 真正进入企业生产，token/MW、secure workspace、context memory storage、local agent PC 与机器人数据 flywheel 会成为新的基础设施需求；若企业 ROI 不成立，则 Vera Rubin 之后的增长斜率会被电力和资金约束钝化。

## 产品和技术路线三情景预测

说明：以下数字把公开事实与本报告估算分开。市场规模均为美元口径；“当前规模”优先使用 2025/2026 公开口径，缺少直接口径时用 NVIDIA 已披露收入或 BOM 假设估算。三情景为 2027 年相对 2026 年的一年期判断，不是长期 TAM。

| 方向 | 当前成熟度与关键证据 | 当前市场规模/基准 | 2027 基准情景 | 2027 乐观情景 | 2027 超预期乐观情景 | 利润率/价值捕获 | 置信度 |
|---|---|---:|---:|---:|---:|---|---|
| Vera Rubin / AI factory rack-scale system | Full production；2026 年秋季 production shipments；150 家台湾 partners、350+ factories、30 countries ramping | NVIDIA Data Center FY2027 Q1 年化 3008 亿美元；其中 compute 年化 2416 亿美元、networking 年化 592 亿美元。该数字是 NVIDIA run-rate，不等于全市场 TAM | NVIDIA DC run-rate 增至 3800-4300 亿美元，Vera Rubin 占新增出货主力；GB300/NVL72 和 Rubin 并行 | 4600-5200 亿美元，AI cloud 与 sovereign/enterprise ACIE 拉动，hyperscaler capex 不减速 | 5700 亿美元以上，百万 GPU 工厂与 agentic inference 需求同时兑现 | NVIDIA 系统级毛利率参考公司 Q1 FY2027 non-GAAP gross margin 75.0%；ODM/系统集成毛利率明显低但营收弹性强；最高价值在 GPU、NVLink、networking、software attach | 中高 |
| Spectrum-X Ethernet Photonics / CPO / AI optics | CPO switches 已投产；200Gb/s SerDes；宣称 5x 能效、5x uptime、1.3x deployment speed；CoreWeave/Lambda/OCI 首批生态 | TrendForce：2026 AI optical transceiver 260 亿美元；Dell'Oro：AI back-end switch 2030 年超过 1000 亿美元 | AI optics 320-360 亿美元；CPO 仍低个位数十亿美元，主要在极大集群导入 | AI optics 380-420 亿美元；CPO 在 800G/1.6T 高端端口中加速渗透 | AI optics 450 亿美元以上；CPO 提前成为百万 GPU 网络标配，硅光/激光器/封装测试短缺 | 模块毛利率估算 25-45%；硅光/激光器/高速 SerDes/IP/测试良率环节弹性更高；NVIDIA 捕获 switch+CPO system value | 中 |
| Vera CPU / BlueField-4 / STX secure storage | Vera CPU full production；88 cores、1.2TB/s；BlueField-4 800Gb/s；STX partner platforms 2026H2 | 直接市场未披露。估算：若按 AI factory 硬件 BOM 5-10% 为 CPU/DPU/storage acceleration，对 2026 NVIDIA DC run-rate 形成约 150-300 亿美元关联池 | 220-350 亿美元关联池；先在 hyperscale 和 AI cloud 新集群导入 | 350-500 亿美元；enterprise agent workspace 拉动 secure storage attach | 500 亿美元以上；agent context memory 和文件访问治理成为强制配置 | NVIDIA 通过 CPU/DPU/DOCA 软件栈捕获高毛利；storage OEM/软件伙伴捕获中高毛利；传统存储若未集成 agent security 可能被稀释 | 中 |
| DSX / liquid cooling / 800V DC power | DSX MaxLPS、DSX OS 发布；45 摄氏度液冷、固定电力预算中最多 40% 更多 GPU；TI 800V DC 参考设计 | 2026 liquid cooling 公开口径约 40.7-81.7 亿美元，基准取 50-80 亿美元；TrendForce 预计 AI chip 液冷渗透率 2026 年 47% | 液冷 80-110 亿美元；800V DC 以试点/参考设计为主 | 液冷 120-150 亿美元；power shelf、busbar、PDU、冷板和 CDU 交期拉长 | 液冷 160 亿美元以上；高压直流在新建 AI factory 中提前标准化 | 组件毛利率估算 25-45%；工程集成 10-25%；长期价值在标准件、控制软件、可靠性认证和数据中心运维 | 中 |
| RTX Spark / AI PC / local agent hub | RTX Spark 发布；1 PFLOP、128GB unified memory、6144 CUDA cores、20-core Grace CPU；首批 laptop fall 2026；Microsoft/OpenShell/Adobe 支持 | Gartner：2025 AI PC 7700 万台，2026 AI PC share 55%；FMI：2026 AI PC market 1034 亿美元。Spark 属高端子集，不等于全 AI PC | Spark 类高端 AI PC/desktop 100-200 万台，收入池 20-40 亿美元，主要开发者/创作者 | 300-500 万台，收入池 60-120 亿美元，企业 local agent 节点开始采购 | 800 万台以上，收入池 180 亿美元以上，memory 供给缓和且 Windows agent 生态爆发 | NVIDIA/MediaTek 捕获 SoC/IP；OEM 毛利薄；DRAM/LPDDR/SSD 单机价值上升；软件生态决定溢价 | 中低 |
| DGX Station for Windows / deskside AI supercomputer | GB300 desktop superchip；748GB coherent memory；20 PFLOPS FP4；Q4 2026；ASUS/Dell/GIGABYTE/HP/MSI/SMCI | 直接市场未披露。本报告估算 2026 早期市场小于 10 亿美元，因 Q4 才开始 | 1-3 万台、20-60 亿美元，面向企业 AI 团队、设计/仿真/科研 | 5-8 万台、80-150 亿美元，Windows 企业 agent 开发节点扩张 | 10 万台以上、200 亿美元以上，若本地/私有模型开发成为标准预算 | 单价高、毛利率高于普通工作站；NVIDIA 捕获 GB300/软件，OEM 捕获整机和服务 | 中低 |
| Cosmos 3 / Isaac GR00T / Physical AI stack | Cosmos 3 open；GR00T 1.7 early access；Isaac Sim 6.0 GA；Unitree G1 workflow soon；reference humanoid late 2026 | Humanoid 2026 市场口径差异大：Grand View 42 亿美元、Fortune BI 62.4 亿美元；service robotics 2026 约 311-724.6 亿美元 | humanoid 60-90 亿美元；主要为试点、教育/科研和低速场景 | humanoid 100-150 亿美元；工业/仓储封闭场景小规模部署 | 200 亿美元以上；整机降价和数据 flywheel 明显改善 | 上游传感器、执行器、减速器、边缘算力、仿真软件、数据采集工具优于整机；NVIDIA 通过 Jetson/Isaac/Omniverse 抽取平台价值 | 中低 |
| DRIVE Hyperion / robotaxi platform | Foxconn 高雄 2028 计划；Uber 将整合 Hyperion fleets；Alpamayo 2 Super 32B VLA；OmniDreams/AlpaGym | 2025 robotaxi 口径：Grand View 6.1 亿美元；Coherent 2026 53 亿美元；Goldman Sachs 2035 4150 亿美元 | 2027 10-25 亿美元，主要试运营和城市扩张 | 30-60 亿美元，多个城市商业化路线稳定 | 100 亿美元以上，监管/安全/保险同时放行 | 近期价值在车端算力、传感器、仿真验证、fleet ops；长期平台价值高但证伪风险大 | 低 |

## 市场规模和利润池

### AI factory compute 与 rack-scale system

事实：NVIDIA FY2027 Q1（截至 2026-04-26）收入 816 亿美元，同比增长 85%；Data Center 收入 752 亿美元，同比增长 92%；GAAP gross margin 74.9%、non-GAAP gross margin 75.0%；GAAP operating income 535 亿美元，对收入比率约 65.6%。旧口径中 Data Center compute 604 亿美元、networking 148 亿美元。

估算：若把 Q1 FY2027 Data Center 年化，NVIDIA 已处在约 3008 亿美元数据中心收入 run-rate；这不是 2026 全年指引，也不是全行业 TAM，但足以说明 AI factory 已进入数千亿美元级年化硬件周期。按 2027 基准 30-40% 同比增长，Data Center run-rate 可达 3900-4200 亿美元；乐观 50-70% 增长，对应 4500-5100 亿美元以上。

利润池判断：最高利润仍在 GPU/NVLink/系统级软件；第二层是 networking、DPU/security、storage acceleration；第三层是 ODM rack assembly、power/cooling integration、facility EPC。台系 ODM 的收入弹性大，但利润率通常低于 NVIDIA 和关键部件商，需用订单/毛利率/库存周转验证。

### AI back-end networking、CPO 与 optics

事实：NVIDIA networking 已年化 592 亿美元，且同比增速 199%，是本届会议后最强的“GPU 外”数据点。Spectrum-X Ethernet Photonics 已投产，意味着 NVIDIA 不是等待开放 Ethernet 生态来替代自己，而是在 Ethernet fabric 上继续做系统级捆绑。

市场规模：TrendForce 2026-04-20 预计 2026 年 AI optical transceiver 市场达 260 亿美元；Dell'Oro 2026-02-04 预计 AI back-end switch 市场 2030 年超过 1000 亿美元。若 AI optical 2027 增速 25-60%，对应 325-416 亿美元；若 CPO 提前渗透，超预期可超过 450 亿美元。

利润率：高速光模块成熟后竞争会压毛利，但 800G/1.6T、硅光、CPO、laser、DSP/LPO、测试和可靠性验证仍有高端毛利窗口。若 CPO 与 switch 深度集成，NVIDIA/交换平台捕获的系统价值高于独立模块商；独立光模块厂需要证明自己仍在 CPO BOM 或 pluggable 长尾中有份额。

### DSX、电力和液冷

事实：DSX MaxLPS 的关键指标是 token performance per megawatt，不是传统 PUE。45 摄氏度液冷加 rack 内优化可在固定电力预算内最多运行 40% 更多 GPU。TI 与 NVIDIA 的 800V DC 架构材料显示，AI rack 从 100kW 级走向 1MW 级时，48V/传统配电的铜耗、重量和效率成为物理约束。

市场规模：2026 年 data center liquid cooling 市场公开口径差异明显：GMI 为 60 亿美元，Grand View 为 81.7 亿美元，MarketsandMarkets 为 40.7 亿美元，Mordor 为 67.7 亿美元。基准使用 50-80 亿美元区间；2027 基准 80-110 亿美元，乐观 120-150 亿美元，超预期 160 亿美元以上。

利润池：冷板、CDU、泵、快接头、manifold、漏液检测、facility controls、PDU、busbar、HVDC 转换、电源管理芯片和工程验证都可能受益。长期最赚钱的不一定是安装施工，而是标准化模块、可靠性认证、控制软件和可规模复制的 DSX-ready 资产。

### CPU、DPU、安全存储和 agent context memory

事实：Vera CPU 强调 Python runtime、sandboxed code execution、orchestration logic 和 analytics pipelines；BlueField-4 STX 强调 agent、data、context memory 的 inline policy enforcement。NVIDIA 把 agentic AI 的瓶颈定义从 GPU 推理扩展到 CPU 执行、文件访问和存储安全。

市场规模估算：没有直接可验证的“agentic storage acceleration”市场口径。本报告用 AI factory BOM 的 5-10% 作为 CPU/DPU/storage-security 关联池估算，对 NVIDIA Data Center 当前年化 run-rate 形成约 150-300 亿美元潜在硬件/软件关联池。该估算置信度中等偏低，后续需要用 STX partner 平台订单和 DPU attach rate 验证。

利润池：如果企业 agent 必须访问文件、数据库、代码库、context memory 和长期任务状态，则安全策略会从应用层下沉到 storage/network silicon。NVIDIA 通过 BlueField/DOCA 捕获高毛利，传统 storage 厂商若能绑定 STX 可提升 AI-native storage 溢价；若只卖通用存储，利润弹性不强。

### AI PC、RTX Spark 与 DGX Station

事实：RTX Spark 的硬件规格足以把 120B 参数 LLM、百万 token context、4K AI video、90GB+ 3D scene 和 12K 4:2:2 video editing 拉到本地高端设备。MediaTek 2026-06-01 确认参与 RTX Spark，首批笔记本 2026 年秋季上市；NVIDIA 称 ASUS、Dell、HP、Lenovo、Microsoft Surface、MSI 先行，Acer/GIGABYTE 后续。

市场规模：Gartner 2025-08-28 预计 AI PC 2025 年 7700 万台、2026 年占 PC 市场 55%。FMI 口径下 AI PC market 2026 年约 1034 亿美元。但 Spark 不是全部 AI PC，基准按 2027 年 100-200 万台高端设备、20-40 亿美元收入池估算；若 Windows agent 生态和 Adobe 创作负载验证，乐观 60-120 亿美元。

利润池：NVIDIA/MediaTek/内存供应商捕获更高增量价值，OEM 仍可能面对薄毛利和库存风险。2026 年 PC 大盘还受到 DRAM/NAND 价格和供给约束，AI PC 渗透提升不等于 PC 总量走强。

### Physical AI、humanoid 与 robotaxi

事实：NVIDIA 的 physical AI 证据更像“开发工具链成熟”，不是“终端销量已爆发”。Cosmos 3、GR00T、Isaac Sim/ROS/Lab、Jetson Thor、Unitree G1 workflow 加速机器人研发；DRIVE Hyperion 则在 robotaxi 生态中拿到 Foxconn、Uber、VinFast/Autobrains、HUMAIN 线索。

市场规模：humanoid 2026 公开口径从 Grand View 的 42 亿美元到 Fortune BI 的 62.4 亿美元不等；robotaxi 口径更分散，Grand View 给 2025 年 6.1 亿美元，Coherent 给 2026 年 53 亿美元，Goldman Sachs 给 2035 年约 4150 亿美元。口径冲突说明近期商业化仍不稳，不宜用远期 TAM 直接贴现。

利润池：2026-2027 更可能兑现的是传感器、执行器、机器人控制器、Jetson Thor、仿真软件、数据采集、遥操作和安全验证。整机和 fleet operation 的收入规模可能大，但要等真实部署、维修成本、保险、安全事故和利用率数据。

## 反共识洞见和重要更新

1. 市场低估 NVIDIA networking 的独立重要性。Q1 FY2027 networking 148 亿美元单季收入已经接近许多独立网络设备公司的年收入，本届 CPO/photonic Ethernet 进一步说明 NVIDIA 在 AI fabric 上不是被动受益，而是在重新定义 back-end network 标准。

2. 市场可能高估“开放 Ethernet 会削弱 NVIDIA”的短期影响。Ethernet 确实扩大了生态参与者，但 Spectrum-X、CPO switch、BlueField、DSX 和 NVLink 共同形成的是一套由 NVIDIA 定义的 AI factory fabric。受益者不是所有 Ethernet 厂商，而是能进入 AI back-end、CPO、可靠性验证和 DSX-ready 体系的厂商。

3. CPO 的爆发不是全行业平均机会，而是少数高端集群先行。NVIDIA 已说“now in production”，但 2026 年 CPO 的约束仍在良率、热、可维护性、laser、测试和现场运维。若市场把所有光模块厂都按 CPO 受益重估，是过度乐观；若只看 pluggable 价格竞争而忽视 CPO 先导订单，是低估。

4. Power/cooling 是 AI 工厂的“隐性产能”。DSX MaxLPS 的 40% more GPUs within fixed power budget 等价于在电力稀缺地区增加有效 GPU 产能。市场若只跟踪 GPU 交期而不跟踪 MW 接入、液冷 CDU、冷板、PDU、HVDC 和并网周期，会漏掉真正的出货瓶颈。

5. AI PC 是真实新产品，但 2026 年不要按消费 PC 爆款定价。RTX Spark 更像 local agent runtime 与创作/开发工作站平台，ASP 高、早期量有限；若 Microsoft/Adobe/OpenShell 生态不能形成高频工作流，普通用户不会因“agent”概念支付大幅溢价。

6. Humanoid 方向会继续热，但下一年最有弹性的不是整机收入。Gartner 对 2028 年生产化公司数的判断很保守，说明真实部署仍少。更可投资的是“让机器人开发更快”的工具链：仿真、teleop、数据、传感、安全、edge compute、actuator 供应链。

7. Secure storage 和 context memory 可能是被忽视的利润池。企业 agent 的失败常发生在权限、文件访问、凭证、长期上下文和审计，而非单纯模型能力。BlueField-4 STX 把 security policy 拉进 silicon/data path，若 enterprise agent 进入生产，这一层可能比通用 agent 应用更有确定性。

8. “台系供应链全受益”需要拆开看。Foxconn/QCT/Wistron/Wiwynn/Inventec/Compal 等可吃到 rack-scale system 订单，但毛利率、现金转换周期、库存风险不同；真正利润弹性要看是否拥有液冷、电源、整机设计、rack integration、测试验证和客户认证能力，而不是只看是否出现在合作伙伴名单。

9. 需要立即下修的证伪条件：Vera Rubin 秋季出货延期；GB300/Vera Rubin 订单没有带来 networking attach 上升；CPO 客户从“first adopters”没有扩大到更多 hyperscalers；2026H2 hyperscaler/AI cloud capex 指引下修；agentic AI 企业生产项目因 ROI/security 大规模回撤；液冷/800V DC 标准推进慢于预期。

## 公司和产业链映射

| 层级 | 代表公司/组织 | 与本届会议的关系 | 收入暴露与弹性判断 | 证据强度 |
|---|---|---|---|---|
| 平台核心 | NVIDIA | Vera Rubin、Vera CPU、BlueField-4、Spectrum-X Photonics、DSX、RTX Spark、DGX Station、Cosmos/Isaac/Drive | 直接收入和毛利捕获最高；风险是客户 capex、出口管制和自研 ASIC 替代 | A |
| 云/AI factory 客户 | CoreWeave、Lambda、OCI、Microsoft Azure、Nebius、Nscale、Firmus、GMI Cloud、IREN、Vultr、Yotta 等 | CPO、confidential computing、DSX、Vera/Vera Rubin 采用或部署 | 受益于 AI capacity 稀缺，但债务、融资成本、电力约束和 utilization 是核心风险 | A/B |
| 系统 OEM/ODM | Dell、HPE、Lenovo、Supermicro、ASUS、Foxconn、GIGABYTE、Pegatron、QCT、Wistron、Wiwynn、Compal、Inventec、MiTAC、MSI、ASRock Rack、AIC | Vera Rubin、DSX-ready、STX、DGX Station/RTX Spark 设备 | 收入弹性大，毛利弹性取决于 rack integration、液冷、电源、认证和售后服务 | A |
| 网络/光互连 | NVIDIA Spectrum-X、潜在高速光模块/硅光/激光器/SerDes/IP/测试设备供应链 | Spectrum-X Ethernet Photonics now in production；AI optics 260 亿美元市场口径 | 高端 CPO/1.6T/800G 先受益；普通模块竞争激烈 | A/B |
| 电力/液冷 | NVIDIA DSX、TI、Schneider、Eaton、Vertiv、Delta 等电力/冷却生态 | DSX MaxLPS、800V DC、45 摄氏度液冷、rack power 密度提升 | 2026-2027 高增长；标准件和控制系统优于一次性工程 | B |
| AI PC/本地 agent | Microsoft、MediaTek、Adobe、ASUS、Dell、HP、Lenovo、Surface、MSI、Acer、GIGABYTE | RTX Spark、OpenShell、Windows security primitives、Adobe 2x 优化 | 高端设备和内存 BOM 上升；普通 PC OEM 利润弹性有限 | A/B |
| AI workstation/deskside supercomputer | ASUS、Dell、GIGABYTE、HP、MSI、Supermicro | DGX Station for Windows Q4 2026 | 低量高 ASP，高毛利，适合企业 AI 开发和仿真 | A |
| Physical AI/robotics | Unitree、Foxconn、Techman、PICO、Lightwheel、Agility、Boston Dynamics、Dyna、Figure、FieldAI、Noble、Richtech、Skild、Flexion、RLWRLD、Robotiq、Lyte | Isaac GR00T、Teleop、Sim、ROS、Jetson Thor、Cosmos | 上游和开发工具先于整机兑现；整机需验证 ROI 和可靠性 | A/B |
| Robotaxi/AV | Foxconn/Foxtron、Uber、Autobrains、VinFast、HUMAIN | DRIVE Hyperion、Alpamayo 2 Super、Kaohsiung 2028 计划 | 2026-2027 是 design win/试运营，不是大规模收入期 | A |
| 伪受益或弱弹性 | 仅有普通服务器组装、普通 PC 品牌、未进入 CPO/AI back-end 的通用网络厂、泛 humanoid 概念公司 | 会议主题相关但缺订单、规格或认证 | 收入暴露低，容易被概念估值拉高后证伪 | C |

## 风险、反证条件和后续跟踪

### 关键风险

- 需求风险：agentic AI 企业生产 ROI 低于预期，长时 agent 的 token 消耗无法转化为付费收入。
- 资金风险：hyperscaler 和 AI cloud 资本开支依赖债务/权益融资，利率、信用利差或股价回撤会影响订单节奏。
- 电力风险：MW 接入、并网审批、变压器、HVDC、备用电源和液冷交付慢于 GPU 出货。
- 供应链风险：HBM、CoWoS/advanced packaging、800G/1.6T optics、CPO 良率、冷板/CDU、PDU 供应不足。
- 技术风险：CPO 可维护性、现场替换、laser 寿命、热管理和测试成本压低经济性。
- 竞争风险：hyperscaler 自研 ASIC、开放 Ethernet/UALink、AMD/Intel/ASIC 方案在部分 workload 中替代。
- 政策风险：美国出口管制、中国市场缺口、台湾地缘风险和主权 AI 采购政策变化。
- 估值风险：会议后股价/估值若已充分反映“AI factory full-stack”，后续必须靠订单和利润率验证。

### 反证条件

| 判断 | 反证数据 | 触发后的下修 |
|---|---|---|
| Vera Rubin 将驱动 2026H2-2027 rack-scale 放量 | 2026 年秋季出货延期、主要 OEM 未确认订单、NVIDIA DC sequential growth 放缓 | 下修 AI factory system 增速和 ODM 弹性 |
| CPO 是 2026-2027 真实增量 | Spectrum-X Photonics 客户不扩展、CPO 交期/良率差、客户继续大量使用传统 pluggable | 下修 CPO，保留 800G/1.6T pluggable/LPO |
| DSX/液冷提高有效 GPU 产能 | AI rack 因液冷/电力事故延迟，客户未采用 45C liquid cooling 或 MaxLPS | 下修液冷和 power component 超预期情景 |
| RTX Spark 会形成新高端 AI PC 品类 | Fall 2026 设备定价过高、软件生态少、sell-through 弱 | 下修 AI PC 对 NVIDIA/MediaTek/OEM 增量 |
| Physical AI stack 会带动 edge compute 和仿真 | GR00T/Cosmos 下载不转化为企业项目，Jetson Thor 设计导入少 | 保留长期方向，下修 1 年收入 |
| Robotaxi 平台进入工业扩张 | Kaohsiung/Autobrains/Uber 项目无进展或监管受阻 | robotaxi 只保留长期可选性 |

### 后续跟踪节点

- 2026 年 6-8 月：NVIDIA GTC Taipei 会后 session replay、partner booth material、OEM 订单和渠道反馈。
- 2026 年 7-9 月：hyperscaler/AI cloud Q2 财报 capex 指引、NVIDIA Q2 FY2027 财报和 networking attach 数据。
- 2026 年秋季：Vera Rubin production shipments、RTX Spark 首批设备上市、OEM/ODM 交付周期。
- 2026 年下半年：BlueField-4 STX partner platforms、CPO switch 扩大客户、liquid cooling 交期、800V DC 试点。
- 2026 年 Q4：DGX Station for Windows 上市、GB300 桌面超算订单。
- 2026 年末：Isaac GR00T reference humanoid from Unitree、Unitree G1 workflow、机器人开发者生态数据。
- 2028 年：Foxconn/Foxtron Taiwan robotaxi service 计划是否如期进入 airport-to-city routes。

建议刷新频率：2026H2 每月跟踪一次 Vera Rubin/CPO/液冷/ODM 订单；NVIDIA 和主要 hyperscaler 财报后立即刷新一次；RTX Spark 和 DGX Station 上市后按月跟踪 sell-through、ASP、库存和软件生态。

## 来源清单

### 一手官方会议材料

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| [NVIDIA GTC Taipei 2026 official page](https://www.nvidia.com/en-tw/gtc/taipei/) | 2026-06 检索 | 会议官网 | A | 会议主题、keynote、AI factories、agentic AI、physical AI、RTX Spark、Build-a-Claw |
| [NVIDIA GTC Taipei FAQ](https://www.nvidia.com/en-tw/gtc/taipei/faq/) | 2026-06 检索 | 会议 FAQ | A | 确认 keynote 为 2026-06-01 Taipei Music Center，conference/workshops 为 2026-06-02 至 2026-06-04 TICC |
| [GTC Taipei Schedule at a Glance](https://www.nvidia.com/en-tw/gtc/taipei/conference-schedule/) | 2026-06 检索 | 会议日程 | A | 50+ sessions、70+ training labs、certifications、sessions/workshops |
| [NVIDIA GTC Taipei at COMPUTEX live updates](https://blogs.nvidia.com/blog/nvidia-gtc-taipei-computex-2026-news/) | 2026-05-21 至 2026-06-04 | 官方 live blog | A | Nemotron 3 Ultra、Build-a-Claw、Isaac GR00T、secure agent workspaces、RTX Spark、Cosmos 3、Vera Rubin keynote recap |
| [NVIDIA GTC Taipei 2026 Keynote replay](https://www.youtube.com/watch?v=wSp6AiNIrsY) | 2026-06 | 官方视频 | A | keynote 产品节奏和管理层表述 |
| [NVIDIA Developer Forums: Community Guide to GTC Taipei](https://forums.developer.nvidia.com/t/a-community-guide-to-nvidia-gtc-taipei-at-computex-2026/370571) | 2026-05-19 | 官方论坛/社区材料 | B | Physical AI Days、robotics、industrial AI、simulation、semiconductor workflow session clues |

### 一手公司和产品发布

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| [NVIDIA Vera Rubin full production](https://nvidianews.nvidia.com/news/vera-rubin-full-production-agentic-ai-factory) | 2026-05-31 | NVIDIA Newsroom | A | Vera Rubin full production、10x agent throughput、CPO/Spectrum-X Photonics、partner list、fall shipments |
| [NVIDIA DSX AI factory platform](https://nvidianews.nvidia.com/news/dsx-infrastructure-ai-factory) | 2026-05-31 | NVIDIA Newsroom | A | DSX MaxLPS、45C liquid cooling、40% more GPUs、DSX OS、DSX ecosystem |
| [NVIDIA Vera CPU](https://nvidianews.nvidia.com/news/nvidia-unveils-vera-the-cpu-for-agents) | 2026-05-31 | NVIDIA Newsroom | A | 88 cores、1.2TB/s、1.8x x86、Grace 2.5M shipments、customer/manufacturer list |
| [NVIDIA Vera BlueField-4 STX](https://nvidianews.nvidia.com/news/nvidia-vera-bluefield-4-stx-brings-agentic-ai-storage-processing-with-in-silicon-security) | 2026-05-31 | NVIDIA Newsroom | A | DOCA Vault/Argus/Flow、800Gb/s、1000x runtime threat detection、H2 2026 availability |
| [NVIDIA and Microsoft RTX Spark Windows PCs](https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark) | 2026-05-31 | NVIDIA Newsroom | A | RTX Spark specs、128GB unified memory、1 PFLOP、6144 CUDA cores、20-core CPU、fall availability |
| [NVIDIA DGX Station for Windows](https://nvidianews.nvidia.com/news/nvidia-dgx-station-for-windows-puts-a-trillion-parameter-ai-supercomputer-on-every-enterprise-desk) | 2026-05-31 | NVIDIA Newsroom | A | GB300 desktop superchip、748GB memory、20 PFLOPS FP4、800Gb/s ConnectX-8、Q4 2026 |
| [NVIDIA Cosmos 3](https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai) | 2026-05-31 | NVIDIA Newsroom | A | open physical AI omnimodel、mixture-of-transformers、benchmarks、Cosmos Coalition |
| [NVIDIA DRIVE Hyperion robotaxi ecosystem](https://nvidianews.nvidia.com/news/nvidia-drive-hyperion-becomes-the-global-platform-for-a-robotaxi-ready-world) | 2026-05-31 | NVIDIA Newsroom | A | Foxconn、VinFast/Autobrains、Uber、HUMAIN、Kaohsiung 2028 plan |
| [NVIDIA Alpamayo 2 Super](https://nvidianews.nvidia.com/news/nvidia-alpamayo-2-super-robotaxis) | 2026-05-31 | NVIDIA Newsroom | A | 32B VLA、AlpaGym、OmniDreams、NuRec skills |
| [NVIDIA Isaac GR00T Reference Humanoid Robot](https://nvidianews.nvidia.com/news/nvidia-open-humanoid-robot-reference-design) | 2026-05-31 | NVIDIA Newsroom | A | Unitree availability late 2026、G1 workflow、Jetson Thor、Isaac stack |
| [NVIDIA FY2027 Q1 financial results](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2027) | 2026-05-20 | 公司财报新闻稿 | A | 816 亿美元收入、752 亿美元 Data Center、604 亿美元 compute、148 亿美元 networking、75% gross margin |
| [NVIDIA Investor Relations events](https://investor.nvidia.com/events-and-presentations/events-and-presentations/default.aspx) | 2026-05-31 | 投资者材料入口 | A | GTC Taipei keynote 和 Financial Analyst Q&A |
| [MediaTek RTX Spark product page](https://www.mediatek.com/products/personal-computing/nvidia-rtx-spark) | 2026-06 检索 | 合作方产品页 | B | MediaTek 与 NVIDIA 协作、CPU/SoC/连接能力、RTX Spark 定位 |
| [MediaTek RTX Spark press release](https://www.mediatek.com/press-room/mediatek-collaborates-with-nvidia-on-rtx-spark-to-power-the-next-wave-of-windows-pc-experiences) | 2026-06-01 | 合作方新闻稿 | B | 首批 RTX Spark laptops fall 2026、MediaTek 每年 20 亿连接设备背景 |
| [TI 800 VDC with NVIDIA](https://www.ti.com/about-ti/newsroom/news-releases/2026/2026-03-16-ti-unveils-complete-800-vdc-power-architecture-for-future-generation-ai-data-centers-with-nvidia.html) | 2026-03-16 | 合作方新闻稿 | B | 800V DC power architecture、AI data center power delivery |
| [TI 800V HVDC collaboration with NVIDIA](https://www.ti.com/about-ti/newsroom/news-releases/2025/ti-teams-with-nvidia-to-bring-efficient-power-distribution-to-ai-infrastructure.html) | 2025-05-23 | 合作方新闻稿 | B | rack power 从 100kW 向 1MW、48V 铜耗约束、800V rationale |
| [Lambda silicon photonics for AI clusters](https://lambda.ai/blog/silicon-photonics-for-ai-clusters-performance) | 2025-12 检索口径 | AI cloud 技术博客 | B | CPO networking、Quantum-X/Spectrum-X Photonics deployment clue |

### 技术材料、标准和市场规模

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| [TrendForce: AI optical transceiver market to reach US$26B in 2026](https://www.trendforce.com/presscenter/news/20260420-13017.html) | 2026-04-20 | 市场研究 | B | AI optical transceiver 市场规模、800G+ 需求 |
| [Dell'Oro: AI back-end switch market will push past $100B by 2030](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/) | 2026-02-04 | 市场研究 | B | AI back-end switch 长期市场规模 |
| [Dell'Oro AI back-end networks report page](https://www.delloro.com/market-research/data-center-infrastructure/data-center-switch-ai-back-end-networks/) | 2026-06 检索 | 市场研究入口 | B | Ethernet/InfiniBand/UALink/NVLink scale-up/scale-out framework |
| [LightCounting: optics for AI clusters](https://www.lightcounting.com/newsletter/en/january-2025-optics-for-ai-clusters-319) | 2025-01 | 市场研究摘要 | B | LPO/CPO 2026-2027 部署、2028 high volume 线索 |
| [GMI data center liquid cooling market](https://www.gminsights.com/industry-analysis/data-center-liquid-cooling-market) | 2026 检索 | 市场研究 | B | 2025 48 亿美元、2026 60 亿美元、2035 271 亿美元 |
| [Grand View data center liquid cooling market](https://www.grandviewresearch.com/industry-analysis/data-center-liquid-cooling-market-report) | 2026 检索 | 市场研究 | B | 2025 66.5 亿美元、2026 81.7 亿美元、2033 294.6 亿美元 |
| [MarketsandMarkets data center liquid cooling market](https://www.marketsandmarkets.com/Market-Reports/data-center-liquid-cooling-market-84374345.html) | 2026 检索 | 市场研究 | B | 2026 40.7 亿美元、2033 276.5 亿美元 |
| [TrendForce 2026 tech landscape](https://www.trendforce.com/presscenter/news/20251127-12805.html) | 2025-11-27 | 市场研究 | B | AI chip TDP 从 700W 到 1000W+、2026 液冷渗透率 47% |
| [Gartner AI PC share 2026](https://www.gartner.com/en/newsroom/press-releases/2025-08-28-gartner-says-artificial-intelligence-pcs-will-represent-31-percent-of-worldwide-pc-market-by-the-end-of-2025) | 2025-08-28 | 市场研究 | B | 2025 AI PC 7700 万台、2026 55% share |
| [Gartner Q1 2026 PC shipments](https://www.gartner.com/en/newsroom/press-releases/2026-4-10-gartner-says-worldwide-pc-shipments-increased-4-percent-in-first-quarter-of-2026) | 2026-04-10 | 市场研究 | B | Q1 2026 PC shipments 6280 万台 |
| [Gartner humanoid robots production prediction](https://www.gartner.com/en/newsroom/press-releases/2026-01-21-gartner-predicts-fewer-than-20-companies-will-scale-humanoid-robots-for-manufacturing-and-supply-chain-to-production-stage-by-2028) | 2026-01-21 | 市场研究 | B | 2028 年 humanoid production deployment 保守判断 |
| [IDC humanoid robotics commercialization 2026](https://www.idc.com/resource-center/blog/humanoid-robotics-commercialization-2026/) | 2026-05 | 市场研究 | B | 2030 年 humanoid robot shipments >510,000 units、CAGR nearly 95% |
| [Goldman Sachs robotaxi market forecast](https://www.goldmansachs.com/insights/articles/robotaxis-to-become-a-400-billion-dollar-market-in-2035) | 2026-04-30 | 市场研究 | B | 2035 robotaxi market 约 4150 亿美元，美国 480 亿美元 |
| [Grand View humanoid robot market](https://www.grandviewresearch.com/industry-analysis/humanoid-robot-market-report) | 2026 检索 | 市场研究 | B | 2025 24 亿美元、2026 42 亿美元、2033 405 亿美元 |
| [Grand View robotaxi market](https://www.grandviewresearch.com/industry-analysis/robotaxi-market-report) | 2026 检索 | 市场研究 | B | 2025 robotaxi 6.1 亿美元、2033 1472.5 亿美元 |
| [Fortune BI agentic AI market](https://www.fortunebusinessinsights.com/agentic-ai-market-114233) | 2026 检索 | 市场研究 | B | 2025 72.9 亿美元、2026 91.4 亿美元、2034 1391.9 亿美元 |
| [Gartner task-specific AI agents in enterprise apps](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025) | 2025-08-26 | 市场研究 | B | 2026 年 40% enterprise apps embedded task-specific AI agents |

### 非官方、媒体和情绪线索

| 来源 | 日期 | 类型 | 可信度 | 用途 |
|---|---:|---|---|---|
| [Tom's Hardware: how to watch NVIDIA Computex/GTC Taipei keynote](https://www.tomshardware.com/tech-industry/nvidia-keynote-computex-2026-gtc-taipei-where-to-watch) | 2026-06 | 媒体预热 | C | 市场会前关注点：AI factories、N1/N1X/PC rumors、consumer GeForce 预期较低 |
| [The Verge: how to watch NVIDIA Computex keynote](https://www.theverge.com/tech/940540/how-to-watch-nvidias-computex-keynote) | 2026-06 | 媒体预热 | C | 市场会前对 Microsoft/NVIDIA PC 合作的预期 |
| [Reddit r/nvidia GTC Taipei keynote thread](https://www.reddit.com/r/nvidia/comments/1ttft8a/nvidia_gtc_taipei_2026_keynote/) | 2026-06 | 社区讨论 | C | 只作散户/开发者情绪观察，不用于核心事实 |
| [IDC: PC market volatile as memory shortage persists](https://www.idc.com/resource-center/blog/pc-market-enters-volatile-territory-as-memory-shortage-persists-through-2027/) | 2026-06 | 市场研究/原始机构页面 | B | AI PC/普通 PC 大盘压力线索，内存短缺和价格压力 |

## 附：事实、估算和观点边界

- 事实：会议日期/地点、NVIDIA 产品规格、财报数字、官方 partner list、公开市场机构给出的市场规模数字。
- 估算：2027 三情景规模、Vera CPU/BlueField STX 关联池、RTX Spark/DGX Station 出货和收入区间、各环节利润率区间。
- 观点：AI factory 利润池向 networking/CPO/power/cooling/storage security 扩散；AI PC 和 humanoid 短期不宜按全量爆发估值；Ethernet 开放不等于 NVIDIA 护城河短期削弱。
- 需后续复核：Vera Rubin 出货、CPO 客户扩展、AI cloud capex 融资、液冷/800V DC 真实采用率、RTX Spark sell-through、机器人和 robotaxi 生产部署。
