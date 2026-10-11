# The Xcelerated Compute Show 2026：AI 工厂从 GPU 狂热转向“推理、内存墙、开放互联、吉瓦级供电”的系统级拐点

> 调研口径：仅使用公开外部资料；未参考本项目内既有文件。核心会议材料以 2026 年 3 月 23-24 日纽约场 The Xcelerated Compute Show 为主，辅以官方 stream 页面、SDxCentral/DCD 会前资料、标准组织公开资料、公司财报/新闻稿和市场研究公开摘要。金额均为美元，韩元按约 1,450 KRW/USD 粗略折算；预测为未来 12 个月/2026-2027 过渡期判断。

## 一句话结论

The Xcelerated Compute Show 2026 的信号不是“AI 服务器继续买 GPU”这么简单，而是 AI 基础设施进入第二阶段：训练集群仍然扩张，但主战场开始转向推理经济性、长上下文/KV cache、内存与存储、1.6T/3.2T 网络、开放 scale-up fabric、CXL 级内存池化、neocloud 融资与残值管理，以及吉瓦级电力和场址规划。市场共识仍在用“GPU 供需周期”解释所有增长，但会议议程和公开数据共同指向：2026-2027 年利润池会从单一 GPU 供应链扩散到 HBM/DDR/eSSD、以太网后端网络、AI server ODM/OEM、AI storage、功率/液冷/colo capacity 和推理专用芯片。

## 会议事实与一手材料框架

### 官方会议结构

- 时间/地点：2026 年 3 月 23-24 日，纽约 Marriott Marquis, Times Square。
- 官方 2026 生态画像：2027 页面回顾 2026 生态为 550+ hardware/software decision-makers、150+ speakers、50+ technology providers；参会结构约 37% enterprise、13% hyperscale、11% neocloud、14% colocation、7% supercomputing、18% vendor/channel reseller。
- 官网议程覆盖的轨道：AI Foundations、Building AI Factories、The Future of Hardware & Software、AI Impacts、Networking、Storage & Memory、Full Stack Perspective。
- 官方 stream 页面公开 45 条会后视频，覆盖主舞台、AI factories、networking、storage/memory、inference、quantum 等。
- 官方内容伙伴 SDxCentral 会前 deep-dive 直接列出 6 个议题：neocloud、AI-driven transfers 迫使网络栈重构、AI 如何“制造/打破”存储、sovereign storage、memory crunch、2026 AI inferencing market review。

### 最重要的会议 session 信号

- **AI Labs Are the New Hyperscalers**：SemiAnalysis 参与的开场主题把 AI lab/model builder 从“云上客户”提升为基础设施定价者和容量锚定方。
- **Planning for Gigawatts**：OpenAI infrastructure strategy/capacity planning 主题进入主舞台，说明算力采购已经从 GPU 盒子变成 GW 年度容量规划。
- **GP4U - How the next generation of AI models will impact GPU procurement**：OpenAI 参与，重点是下一代模型形态如何影响 GPU 采购，不再只是“越多越好”。
- **All-In on Inference**：Cerebras、Positron AI、Ampere、ZeroPoint 等出现在同一推理专场，会议明确给了“芯片 underdogs 可能赢”的舞台。
- **Solving for the AI Memory Wall / Context Memory Revolution**：WEKA 主题说明“上下文内存”开始成为独立叙事。
- **AI's Hidden Bottleneck - Memory, Storage Scarcity, and the Race for Sovereign Infrastructure**：Vultr、ZeroPoint、Supermicro、Equinix、MaxLinear 等参与，说明瓶颈已经横跨内存、存储、连接和主权部署。
- **CXL Special Presentation / UALink Special Presentation / Ultra Ethernet Consortium / Ethernet Alliance / Ethernet Wins Again**：标准组织集体进入核心议程，说明 2026 不是单一厂商互联，而是开放互联路线的制度化节点。
- **Neocloud Revolution / Neo kids on the block**：CoreWeave、TensorWave、WhiteFiber、Deep Infra、Vast.ai、FarmGPU、Ori、BluSky 等代表 neocloud 从“矿卡再利用”转为企业 AI 的供给侧。
- **AI Futures - Building the Financial Infrastructure of the AI Economy**：Ornn AI 的残值/互换产品说明 GPU/AI server 已经金融资产化，残值风险将影响 neocloud 的真实利润。

## 重点与发展方向：相比 2024-2025 的变化

### 1. 从训练中心论到推理中心论

2024-2025 年市场更关注大模型训练集群、H100/H200/Blackwell 供给和 hyperscaler capex。2026 年会议把“推理”放到主舞台：agentic AI、长上下文、企业落地、低成本 token、KV cache、边缘/分布式推理成为新约束。NVIDIA FY2026 财报称 Blackwell Ultra 相比 Hopper 在 agentic AI 上性能/成本有 50x/35x 级改进；但这类效率提升不会等同于 capex 下降，因为 agentic workflow 会把调用次数、上下文长度和实时数据访问显著放大。

判断：未来 12 个月，推理相关基础设施支出增速大概率高于训练专用支出增速；训练仍是大额订单来源，但 marginal dollar 更容易流向 inference rack、CPU:GPU 配比、KV cache storage、内存容量和网络带宽。

### 2. 从 GPU 稀缺到“内存/存储/网络/电力”系统稀缺

公开数据验证了会议主题：

- IDC：2025 年全球 AI infrastructure spending 为 $318B，2026 年预计 $487B，增速约 53%；Q4 2025 单季 $89.9B，其中 server 为 $87.7B，占 97.6%。
- IDC：全球 server market 2025 年 $453.5B，2026 年预计 $606.7B，2027 年预计 $873.1B。
- Dell'Oro：AI data center accelerator market 未来五年 CAGR 约 25%；同时明确 memory/storage supply chain 被 AI 增长压紧。
- Micron FQ2-2026：收入 $23.86B，GAAP gross margin 74.4%，FQ3 指引收入 $33.5B、gross margin 约 81%。
- Samsung Q1-2026：总收入 KRW 133.9T，经营利润 KRW 57.2T；DS 半导体收入 KRW 81.7T、经营利润 KRW 53.7T，经营利润率约 65.7%。
- SK hynix Q1-2026：收入 KRW 52.6T、经营利润 KRW 37.6T，经营利润率 72%。

这意味着 AI 供应链的高利润不再只在 GPU：HBM、server DRAM、SOCAMM、PCIe Gen6 eSSD、HBM base die、先进封装、网络 ASIC/交换机和高密度供电同样进入卖方市场。

### 3. 从 proprietary fabric 到开放 scale-up/scale-out 标准竞争

2025 之前，AI 网络叙事往往是 NVIDIA NVLink/NVSwitch + InfiniBand/RoCE。2026 年会议把 UALink、Ultra Ethernet、Ethernet Alliance、CXL 放在显眼位置。关键事实：

- UALink 200G 1.0：定义 accelerator-to-switch 的低延迟高带宽互联，200G per lane，单 AI pod 可扩展到 1,024 accelerators。
- UALink Common 2.0：加入 in-network compute，目标是降低 latency、节省 bandwidth、提升 distributed training/inference scaling efficiency。
- Ultra Ethernet Consortium 1.0/1.0.2：从 NIC、switch、optics、cables 到 transport 的 AI/HPC 以太网栈。
- Dell'Oro：2025 年 AI back-end Ethernet switch sales 超过 InfiniBand 两倍以上，Ethernet 在 AI cluster switch sales 中占超过 2/3；800G 已成主流，1.6T 预计 2026 下半年开始出货，2027 年成为重要收入驱动。

判断：市场仍把 NVLink 视为 scale-up 的默认答案，但会议信号显示，scale-up 也开始被“开放标准 + vendor diversity + 供应链多元化”侵蚀。最有爆发力的是 1.6T Ethernet、UALink switch/IP、co-packaged optics、AI NIC/DPU。

### 4. Neocloud 从 opportunistic GPU rental 变为资产/融资/企业采购通道

会议介绍中明确写到 GPU clouds 起点是 crypto mining GPU reuse，如今已成为 AI ecosystem pillar。变化在于：

- 需求端从少数 model lab 扩散到金融、医药、政府、企业研发。
- 供给端不只是“有 GPU”，而是 metal-to-model 平台、orchestration、SLA、compliance、data locality、financing。
- 残值风险显性化：Ornn AI 这类金融基础设施公司出现，说明 lender/neocloud 开始需要 GPU residual value swap。

判断：neocloud 爆发力度很大，但并非所有 neocloud 都能挣钱。赢家是具备电力/数据中心锁定、低成本融资、长期客户合同、异构硬件调度和残值对冲能力的公司；单纯 GPU 转租会被利用率波动、融资成本、芯片代际折价和内存涨价吞掉利润。

### 5. Sovereign AI 从政治口号变成区域 capex 增量

IDC Q4 2025 数据显示，美国占全球 AI infrastructure spending 的 77%，但 Middle East & Africa Q4 同比增长 535%，达到 $1.8B；中国因出口限制 Q4 同比下降 8.1% 至 $8.4B。会议中的 Canadian Compute、Government AI Future、Sovereign Infrastructure 等主题说明主权 AI 正在成为地区性容量建设逻辑。

判断：2026-2027 年非美国 AI infrastructure 的增速可能高于美国，虽然绝对规模仍小；这会利好可绕开单一出口约束、能做本地化交付/主权云/政府合规的供应商。

## 哪些产品和技术方向会爆发：路线图与爆发力度

### A. AI servers / rack-scale systems

当前事实：

- Dell FY2026 AI-optimized server revenue 为 $24.683B，同比增长 166%；全年 AI server orders 超过 $64B，FY27 期初 backlog $43B。
- Dell 指引 FY2027 AI-optimized server revenue 约 $50B，同比增长约 103%。
- IDC server market：2026 年 $606.7B，2027 年 $873.1B，2027 年同比约 43.9%。

路线：

- 2026：Blackwell/GB200/GB300、B300、MI355X/MI450 early ramps，rack-scale supply chain 继续受 HBM、power shelf、liquid cooling、networking 限制。
- 2027：Vera Rubin、AMD Helios/MI450 family、更多 custom ASIC racks、1.6T switching、HBM4 规模化。
- 2028：3.2T network、CXL/pooled memory 与更标准化 rack integration 普及，AI server 从“项目制”走向更模块化的 hyperscale SKU。

三档预测：

- 基准：未来一年 AI server/relevant server spending +35-45%；OEM operating margin 11-15%，Dell ISG Q4 14.8% 是可参考高位。
- 乐观：+50-60%；memory 供给改善、服务/存储/网络 attach 提升，领先 OEM operating margin 15-18%。
- 超预期乐观：+70% 以上；agentic inference 和 sovereign AI 叠加，Dell 类厂商 AI server revenue 翻倍变成行业常态，领先厂商 operating margin 18-20%。

### B. AI accelerators：GPU + custom ASIC + inference ASIC

当前事实：

- NVIDIA FY2026 Data Center revenue $193.7B，同比增长 68%；Q4 Data Center $62.3B，同比增长 75%；公司 FY2026 gross margin 71.1%，FY2027 Q1 gross margin 指引约 75%。
- Broadcom Q1 FY2026 AI revenue $8.4B，同比增长 106%，Q2 AI semiconductor revenue 指引 $10.7B；公司 adjusted EBITDA margin 约 68%。
- AMD Q1 2026 Data Center revenue $5.8B，同比增长 57%；Meta 计划部署最高 6GW AMD Instinct GPUs，第一阶段 1GW 使用 custom MI450-based GPU；AMD Q2 revenue 指引 $11.2B、non-GAAP gross margin 约 56%。

路线：

- 2026：NVIDIA Blackwell Ultra/GB300 仍是主流；Broadcom custom ASIC 受 hyperscaler 自研需求驱动；AMD MI355X/MI450/Helios 提供第二供应源。
- 2027：NVIDIA Vera Rubin、AMD MI450/MI455X、Google TPU/AWS Trainium/Inferentia/Meta silicon 等 custom ASIC 份额继续上升；inference ASIC 进入更清晰的商业窗口。
- 2028：GPU 仍控制通用训练和复杂推理；ASIC 在大规模稳定 workload 中吃份额；推理专用架构按 batch size、latency、上下文长度分化。

三档预测：

- 基准：AI accelerator/custom silicon revenue +30-40%；GPU 龙头 gross margin 70-75%，ASIC/网络龙头 EBITDA 65-70%，AMD gross margin 向 57-60% 改善。
- 乐观：+45-55%；HBM4 良率改善支撑出货，NVIDIA 维持 75% 左右 gross margin，Broadcom AI revenue 年化 $45-55B。
- 超预期乐观：+65% 以上；agentic inference 使推理算力需求非线性放大，custom ASIC 与 GPU 同时紧缺，利润率维持高位而非均值回归。

### C. HBM / server DRAM / SOCAMM / eSSD：最强利润池之一

当前事实：

- Micron FQ2-2026 revenue $23.86B，GAAP gross margin 74.4%；Cloud Memory revenue $7.749B，gross margin 74%；Core Data Center revenue $5.687B，gross margin 74%；FQ3 revenue 指引 $33.5B、gross margin 约 81%。
- Samsung Q1-2026 DS Division revenue 约 $56B，operating profit 约 $37B，经营利润率约 66%；公司称 memory business 创季度收入和经营利润纪录，并已开始 HBM4 与 SOCAMM2 的 mass product sales，用于 NVIDIA Vera Rubin platform。
- SK hynix Q1-2026 revenue 约 $36B，operating profit 约 $26B，经营利润率 72%，高附加值 HBM/server DRAM/eSSD 是主要驱动。
- TrendForce 公开摘要：2026 年 HBM shipments 预计超过 30 billion Gb，HBM4 在 2026 下半年逐步超过 HBM3E 成为主流；SK hynix 预计仍维持过半份额。

路线：

- 2026：HBM3E 仍贡献大量收入，HBM4 开始放量；SOCAMM、server DDR5、高容量 RDIMM、PCIe Gen5/Gen6 eSSD 被 AI server 拉动。
- 2027：HBM4/HBM4E、高容量 server memory、KV cache SSD 成为 AI rack 标配；供给扩张但仍受 TSV、先进封装、EUV DRAM 和良率制约。
- 2028：HBM4E/更高堆叠与定制 base die 扩大，内存厂从周期股逻辑转为 AI infrastructure bottleneck 资产。

三档预测：

- 基准：AI memory/HBM 相关 revenue +45-60%；领先厂 gross margin 65-75%，operating margin 55-70%，价格高位缓慢回落。
- 乐观：+70-90%；HBM4 价格 premium、AI server DRAM 短缺、eSSD 需求一起推高 ASP，Micron/Samsung/SK hynix 维持 70%+ gross/operating margin 的时间拉长。
- 超预期乐观：+100% 以上；长上下文/agentic workload 让 KV cache 与 memory capacity 需求超过 GPU 出货增速，HBM/DDR/eSSD 成为 AI capex 的最紧约束。

### D. AI backend networking：800G 到 1.6T/3.2T，Ethernet 继续赢

当前事实：

- Dell'Oro：AI back-end switch market 到 2030 年将超过 $100B；Ethernet 预计在 scale-up 和 scale-out 都占主导。
- 2025 年 AI back-end Ethernet switch sales 同比超过 3 倍，并在 Q4 和全年占 AI cluster data center switch sales 超过 2/3。
- 800G 已占 AI back-end Ethernet shipments/revenue 的大多数；1.6T 预计 2026 下半年开始出货，推动 2027 收入和份额变化。
- NVIDIA + Celestica 2025 年 AI cluster Ethernet switch sales 合计近 50% 份额，Arista 第三，Cisco、HPE/Juniper、新进入者加速。

路线：

- 2026：800G 主流，1.6T sampling/early deployments，RoCE/UEC 优化、多厂商 Ethernet AI fabric 成为 hyperscaler/neocloud 默认选项之一。
- 2027：1.6T 大规模收入化；co-packaged optics、silicon photonics、AI NIC/DPU 和 congestion control 成为差异点。
- 2028：3.2T 准备/早期部署，scale-up Ethernet/UALink/ESUN 与 proprietary fabric 长期共存。

三档预测：

- 基准：AI back-end switching/fabric revenue +50-70%；switch/NIC silicon gross margin 60-75%，box/system gross margin 25-45%。
- 乐观：+80-100%；1.6T 提前规模化，Ethernet 在 neocloud 和 hyperscaler 中继续替代 InfiniBand。
- 超预期乐观：+120% 以上；scale-up 也显著开放化，UALink/UEC/ESUN 共同把 proprietary fabric 溢价压缩，但整体 market size 放大。

### E. UALink / UEC / CXL：开放互联与解耦内存的制度化窗口

当前事实：

- UALink 200G 1.0 支持 200G per lane、最多 1,024 accelerators/pod。
- UALink Common 2.0 引入 in-network compute。
- CXL 4.0 在 2025 年发布，带宽从 64GT/s 到 128GT/s，并支持 bundled ports、native x2 link width、更长 channel reach 和 memory RAS。
- 会议把 CXL Consortium、UALink Consortium、UEC、Ethernet Alliance 放进正式议程，说明标准生态已经从 paper/spec 进入客户教育和产品化阶段。

路线：

- 2026：CXL memory expander/pooling 仍以 PoC、少量 production pilot 为主；UALink/UEC 产品进入 IP、switch silicon、reference design、early rack 方案。
- 2027：CXL 3.x/4.0 相关 switching、memory pooling、KV cache/large memory tiering 开始在 hyperscaler/AI lab 小规模生产化；UALink first-generation product ramps。
- 2028：CXL/UALink/UEC 从“架构选项”进入 procurement checklist。

三档预测：

- 基准：CXL/UALink/UEC 直接产品收入仍小，约 $1-5B 级，但增长 +100% 左右；IP/silicon 毛利 60%+，系统集成毛利 20-35%。
- 乐观：+200-300%；KV cache 与 memory pooling 成为推理成本优化刚需，CXL memory appliance 和 UALink switch 提前量产。
- 超预期乐观：+400% 以上；开放 scale-up fabric 被多个 hyperscaler/neocloud 同时采用，2027 年订单可见性超过市场预期。

### F. AI storage / KV cache / data platform

当前事实：

- IDC Q4 2025 AI infrastructure storage spending 为 $2.2B，仅占 AI infrastructure 的 2.4%，但会议中 storage/memory 相关 session 密集出现。
- Dell FY2026 storage revenue $16.631B，仅同比 +1%；但 AI server 出货越多，后续 checkpoint、training data、RAG、KV cache、model registry 和 data governance 的滞后需求越强。
- Samsung 明确提到 PCIe Gen6 SSDs 与 KV cache storage demand；Micron/Samsung/SK hynix 的高 margin 说明企业级 NAND/eSSD 也在被 AI 重新定价。

路线：

- 2026：高性能 parallel file/object、NVMe-oF、GPU-direct storage、AI-native data platform 从训练 checkpoint 扩展到推理 KV cache。
- 2027：PCIe Gen6 eSSD、CXL-attached memory tier、storage-aware scheduler 进入主流 AI factory。
- 2028：存储不再只是成本项，而成为 token latency/cost 的决定性路径。

三档预测：

- 基准：AI storage/eSSD/data platform spending +35-50%；存储软件 gross margin 70-80%，硬件/eSSD gross margin 45-70%，OEM operating margin 10-20%。
- 乐观：+60-80%；KV cache storage 成为推理 rack 必需品，Dell/NetApp/Pure/VAST/WEKA/CoreWeave storage attach 提升。
- 超预期乐观：+100% 以上；长上下文和 agentic memory 需求使 storage spending share 从 2-3% 提升到 5%+。

### G. Power / cooling / high-density colo

当前事实：

- 会议出现 AI Factory Playbook、Planning for Gigawatts、AI Factory Alliance、dense inference rack 等主题。
- NVIDIA 宣布与 CoreWeave 深化合作，支持到 2030 年超过 5GW AI factories buildout。
- DCD 报道 OpenAI 已声明其 2029 之前的 AI infrastructure capacity 目标涉及 10GW 级容量。
- IDC 将 power generation/grid capacity 视为 2026 年 AI infrastructure 的首要 operational bottleneck。

路线：

- 2026：70-120kW/rack 继续上升，liquid cooling、power shelf、onsite/substation、PPA、grid interconnection 成为订单前置条件。
- 2027：GW campus 的电力、冷却、水、土地、网络连通和融资同步锁定；推理 workload 向电力便宜、网络可达、合规允许的地区迁移。
- 2028：AI factory 运营效率从 PUE 转向 tokens/W、tokens/$、network utilization、memory utilization。

三档预测：

- 基准：AI-related power/cooling/colo capex +25-35%；成熟 colo EBITDA margin 40-60%，设备 gross margin 20-40%。
- 乐观：+40-55%；GW campus 能源协议加速，液冷与电力设备订单提前。
- 超预期乐观：+70% 以上；sovereign AI、model lab 与 hyperscaler 三方抢电，capacity 资产 re-rating。

## 市场规模、增速和利润率：三档汇总表

| 重要方向 | 当前可观测规模 | 基准：未来一年 | 乐观：未来一年 | 超预期乐观：未来一年 | 利润率判断 |
|---|---:|---:|---:|---:|---|
| AI infrastructure | 2025 $318B；2026 IDC 预测 $487B | +30-40%，至 $630-680B | +45-55%，至 $700-750B | +65%+，至 $800B+ | 上游芯片/内存高；系统集成低双位数；colo EBITDA 高但资本密集 |
| 全球 server market | 2026 IDC $606.7B；2027 IDC $873.1B | +35-45% | +50% | +60%+ | OEM operating margin 10-16%，AI attach 好的厂商更高 |
| AI-optimized server | Dell FY26 $24.7B，FY27 指引 $50B；全球为数百亿美元到千亿美元级 | +50% | +80% | +100%+ | Dell ISG FY26 11.7%、Q4 14.8%；未来 12-18% |
| GPU/custom AI accelerator | NVIDIA DC FY26 $193.7B；Broadcom AI Q1 annualized $33.6B/Q2 guide annualized $42.8B；AMD DC Q1 annualized $23B | +30-40% | +45-55% | +65%+ | NVIDIA GM 71-75%；Broadcom EBITDA 68%；AMD GM 55-60% |
| HBM/AI memory/DC memory | Micron FQ2 $23.9B；Samsung DS Q1 ~$56B；SK hynix Q1 ~$36B；HBM pure TAM 约 $70-100B 级推测 | +45-60% | +70-90% | +100%+ | 领先 memory 厂 GM/OPM 60-80%，短期强于历史周期 |
| AI backend networking | 2025 已为百亿美元级；Dell'Oro 2030 >$100B | +50-70% | +80-100% | +120%+ | Silicon GM 60-75%；box GM 25-45%；光模块/系统视供应紧缺而扩张 |
| CXL/UALink/UEC direct products | 2026 约 $1-5B early market | +100% | +200-300% | +400%+ | IP/silicon GM 60%+；系统 20-35% |
| AI storage/KV cache/eSSD | IDC Q4 2025 AI infra storage $2.2B；2026 年约 $10B+ 级 | +35-50% | +60-80% | +100%+ | 软件 GM 70-80%；eSSD/内存高景气 GM 45-75%；OEM OP 10-20% |
| Power/liquid cooling/colo capacity | AI facility/power/cooling 为数百亿美元级 capex；GW 项目成为核心 | +25-35% | +40-55% | +70%+ | 设备 GM 20-40%；colo EBITDA 40-60%，但 ROIC 受电力和融资成本约束 |

## 与当前市场可能相违背的重要洞见

### 1. “GPU 越贵越好”的简单逻辑会失效

下一阶段最大增量不一定全在 GPU ASP，而在整体系统利用率。GPU 仍然是最大利润池，但如果 memory、network、storage、power 任一环节不足，GPU 利用率下降，客户会优先采购能提升 tokens/$ 的系统部件。HBM、server DRAM、eSSD、NIC、switch、storage scheduler 的边际价值会被重估。

### 2. Ethernet 可能不只是 scale-out winner，也可能侵入 scale-up

市场通常认为 proprietary scale-up fabric 防线很强；但 Dell'Oro 已明确判断 Ethernet 将在 scale-up 和 scale-out 长期占优，UALink 也在争夺 accelerator pod 内部互联。供应链多元化、vendor diversity、成本、可运维性会驱动客户牺牲部分封闭生态极限性能，换取大规模可采购性。

### 3. 推理专用芯片不是“反 NVIDIA”，而是 workload segmentation

Cerebras、Positron、Ampere、ZeroPoint 等进入 All-In on Inference 专场，说明市场开始承认不同 batch size、latency、model size、context length、功耗约束下最优硬件不同。NVIDIA 仍会控制通用性和生态，但推理市场会比训练市场更碎片化，under-dog 的胜率更高。

### 4. Memory company 的利润率可能不是周期顶部，而是新定价框架

历史上 DRAM 高利润常被视为周期反转前兆；但 2026 年的不同是 HBM、server DRAM、SOCAMM、eSSD 被 AI infrastructure 绑定，且供给扩张受先进封装/TSV/EUV/yield 限制。Micron 81% gross margin 指引、Samsung DS 约 66% operating margin、SK hynix 72% operating margin 是非常强的信号：至少未来 12 个月，memory 利润率均值可能显著高于过去十年。

### 5. Neocloud 的赢家可能不是 GPU 最多者，而是资产负债表最像基础设施公司的玩家

GPU 租赁表面毛利可观，但 Blackwell/Rubin/MI450 迭代会制造残值风险。会议中出现 AI financial infrastructure 和 residual value 产品，说明融资成本、折旧、合同期限、利用率和客户信用质量会决定 neocloud 生死。CoreWeave 类公司如果能锁定长期客户/电力/供应链，价值更接近 AI utility；小型转租商则更像高 beta cyclical leasing。

### 6. Storage share 当前太低，反而可能是超额收益点

IDC Q4 2025 AI infra storage share 仅 2.4%，看起来不重要；但会议中 storage/memory session 密集，Samsung 也把 KV cache storage 写入未来需求。若 agentic/long-context workload 起量，storage share 从 2.4% 到 5% 就意味着数百亿美元增量，而市场目前更容易忽略。

### 7. Quantum 在会议中有存在感，但 2026-2027 不是主要商业爆发点

Quantum 被多场讨论覆盖，但标题本身包含“Accelerator or Science Project?”和“2 years or 20?”，说明行业仍在校准时间表。短期投资应把 quantum 视为 HPC/AI ecosystem 的可选长期 upside，而非未来一年 AI infrastructure capex 的主线。

## 投资/产业链排序

### 未来 12 个月最确定

1. HBM/HBM4、server DRAM、SOCAMM、AI eSSD：供给约束强，利润率最高，需求能见度强。
2. AI backend networking：800G 到 1.6T，Ethernet/UEC/UALink/CPO/NIC/DPU 是高增速。
3. AI-optimized servers/rack integration：收入规模大，Dell 指引可见度强，但利润率弹性低于上游。
4. Custom AI ASIC + GPU：仍是最大收入池；NVIDIA/Broadcom 是核心，AMD 有第二供应源弹性。
5. Power/liquid cooling/colo capacity：增长确定但项目、区域、电力接入和融资差异大。

### 未来 12-24 个月赔率最高

1. CXL/pooled memory：小基数，若 KV cache/内存池化生产化，弹性巨大。
2. Inference ASIC/alternative accelerators：不是全面替代 GPU，而是在明确 workload 中突破。
3. AI storage/data platform：当前 spending share 低，长上下文/agentic workflow 可能重定价。
4. Neocloud financial infrastructure：残值、利用率、融资产品会成为新赛道。

### 最大风险

- 电力/并网延迟导致硬件订单递延。
- HBM/DRAM/eSSD 价格过快上涨，挤压 OEM/neocloud 利润，拖慢企业部署。
- Export controls 改变地区需求和供应商份额。
- Agentic AI 商业化慢于预期，推理 capex 从“指数增长”回落到“线性增长”。
- Open standards 产品化节奏慢，proprietary ecosystem 继续锁定高端性能。

## 关键数字清单

- The Xcelerated Compute Show 2026 NY：2026 年 3 月 23-24 日；550+ decision-makers，150+ speakers，50+ technology providers。
- 官方 stream：45 条会后视频。
- IDC AI infrastructure：2025 年 $318B；2026 年预测 $487B；2029 年超过 $1T；Q4 2025 单季 $89.9B。
- IDC AI infrastructure Q4 2025：server $87.7B，占 97.6%；storage $2.2B，占 2.4%；美国 $69.2B，占 77%；中东/非洲 $1.8B，同比 +535%。
- IDC server market：2025 $453.5B；2026 $606.7B；2027 $873.1B。
- NVIDIA FY2026：总收入 $215.9B；Data Center $193.7B；gross margin 71.1%；Q4 Data Center $62.3B。
- Broadcom Q1 FY2026：AI revenue $8.4B，同比 +106%；Q2 AI semiconductor revenue 指引 $10.7B；adjusted EBITDA margin 68%。
- AMD Q1 2026：总收入 $10.253B；Data Center $5.8B，同比 +57%；Q2 revenue 指引 $11.2B；Meta 计划最高 6GW AMD Instinct GPU。
- Dell FY2026：AI-optimized server revenue $24.683B；orders 超过 $64B；backlog $43B；FY2027 AI server revenue 指引约 $50B。
- Micron FQ2 2026：收入 $23.86B；GAAP gross margin 74.4%；FQ3 revenue 指引 $33.5B，gross margin 约 81%。
- Samsung Q1 2026：总收入 KRW 133.9T；operating profit KRW 57.2T；DS revenue KRW 81.7T；DS operating profit KRW 53.7T。
- SK hynix Q1 2026：收入 KRW 52.6T；operating profit KRW 37.6T；operating margin 72%。
- Dell'Oro AI back-end switch：2030 年超过 $100B；2025 年 Ethernet AI back-end switch sales 超过 InfiniBand 两倍以上；800G 已是主流，1.6T 预计 2026H2 开始出货。
- UALink 200G 1.0：200G per lane，最多 1,024 accelerators/pod。
- CXL 4.0：128GT/s，较 3.x 64GT/s 翻倍；加入 bundled ports、native x2、memory RAS 等。
- CoreWeave/NVIDIA：到 2030 年支持超过 5GW AI factories buildout。
- OpenAI：公开报道显示已宣称锁定 10GW 级 AI infrastructure capacity，以支撑 2029 前目标。

## Sources

- The Xcelerated Compute Show 2026 agenda: https://www.xceleratedcompute.com/new-york/2026/2026-agenda/
- The Xcelerated Compute Show 2026 stream page: https://www.xceleratedcompute.com/new-york/2026/stream-the-2026-event/
- The Xcelerated Compute Show Knowledge & Insights: https://www.xceleratedcompute.com/new-york/2026/knowledge-insights/
- The Xcelerated Compute Show 2027 page with 2026 ecosystem recap: https://www.xceleratedcompute.com/new-york/2027/
- SDxCentral, Scaling AI Infrastructure from silicon to software: https://www.sdxcentral.com/resources/scaling-ai-infrastructure/
- DCD, The AI Week Supplement: https://www.datacenterdynamics.com/en/magazines/the-ai-week-supplement/
- IDC, AI infrastructure Q4 2025 / 2026 forecast: https://www.idc.com/resource-center/blog/ai-infrastructure-spending-caps-historic-year-at-90-billion-in-q4-2025-2029-spending-to-eclipse-1-trillion/
- IDC, Servers Market Insights: https://www.idc.com/promo/servers/
- Dell'Oro, AI back-end switch market forecast: https://www.prnewswire.com/news-releases/ai-back-end-switch-market-will-push-past-100-billion-by-2030-according-to-delloro-group-302678344.html
- Dell'Oro, accelerator-led infrastructure spending: https://www.prnewswire.com/news-releases/hyperscale-ai-investment-cycle-anchors-accelerator-led-infrastructure-spending-according-to-delloro-group-302684398.html
- Dell'Oro, Ethernet vs InfiniBand in AI back-end networks: https://newswire.telecomramblings.com/2026/03/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025-according-to-delloro-group/
- NVIDIA FY2026 results: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/
- AMD Q1 2026 results: https://ir.amd.com/news-events/press-releases/detail/1284/amd-reports-first-quarter-2026-financial-results
- Broadcom Q1 FY2026 results: https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial
- Dell FY2026 results PDF: https://investors.delltechnologies.com/node/19176/pdf
- Micron FQ2 2026 results: https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026
- Samsung Q1 2026 results: https://news.samsung.com/ca/samsung-electronics-announces-first-quarter-2026-results
- SK hynix Q1 2026 results: https://news.skhynix.com/q1-2026-business-results/
- UALink specifications: https://ualinkconsortium.org/specification/
- Ultra Ethernet Consortium 1.0 specification announcement: https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/
- CXL 4.0 specification announcement: https://www.businesswire.com/news/home/20251118275848/en/CXL-Consortium-Releases-the-Compute-Express-Link-4.0-Specification-Increasing-Speed-and-Bandwidth
- DCD, OpenAI 10GW AI infrastructure capacity report: https://www.datacenterdynamics.com/en/news/openai-claims-to-have-secured-10gw-of-ai-infrastructure-capacity-ahead-of-2029-target/
- TrendForce HBM4 manufacturing complexity / HBM shipment outlook: https://www.trendforce.com/presscenter/news/20250522-12589.html
- TrendForce AI server shipments 2026: https://www.trendforce.com/presscenter/news/20260120-12887.html
