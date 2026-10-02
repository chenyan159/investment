# Chiplet Summit 2026 高密度更新：Chiplet 从“先进封装技术”转向“AI 系统级供应链”

> 调研日期：2026-05-08。  
> 方法说明：未参考项目内文件和信息；仅使用公开网络资料、Chiplet Summit 官方动态议程/演讲 PDF/参会者 XML、厂商公开材料、行业研究机构公开摘要，并在报告中标明关键来源。  
> 预测口径：文中的“未来一年”按 2026 年当前市场规模到 2027 年市场规模理解；利润率默认指毛利率，若为软件/IP 则补充经营利润率判断。预测为基于公开资料的归一化推演，不是会议方或单一机构的正式预测。

## 一页结论

Chiplet Summit 2026 的核心信号不是“chiplet 会不会起来”，而是“怎么把 chiplet 变成可采购、可验证、可管理、可量产的系统级供应链”。会议从 2 月 17-19 日在 Santa Clara 召开，官方动态参会者 XML 统计到 368 条演讲/主持/嘉宾记录、70 个唯一 session、105 个组织；Siemens 44 条、Synopsys 38 条、Cadence 25 条、Intel 22 条，是最密集的工具链/标准/验证/封装参与方。

本届会议的增量不是单点 PHY 或先进封装，而是六条线同时收敛：HBM4/Custom HBM、64 GT/s UCIe 3.0、AI XPU 多 chiplet、先进封装产能与良率、photonic interposer/CPO、以及安全/测试/数字孪生/SLM。真正的转折在于：开放 chiplet 经济不再只靠“标准接口”，还要靠 RoT、安全域、boot firmware、known-good-die、冗余 lane、热/电/机械协同和供应链商业规则。

数字上，HBM 是最确定的爆发点：Yole 在 Chiplet Summit 2026 的 HBM Markets 材料中给出 HBM 收入从 2025 年约 350 亿美元到 2026 年约 600 亿美元，2027 年约 800 亿美元，2031 年约 1700 亿美元；2026 年 YoY 约 +70%。先进封装总市场 2026 年约 575 亿美元，增速不如 HBM，但高端 CoWoS/EMIB/SoIC/2.5D/3D 是 AI 系统的真瓶颈，TSMC CoWoS 月产能被报道将在 2026 年底达到 11.5 万至 14 万片，2027 年约 17 万片。Chiplet 产品市场定义差异极大，窄口径 2026 年约 193 亿美元，广口径把 HBM/AI GPU/CPU 多芯粒产品收入都算进去会到数百亿美元以上。

投资和产业判断上，2026-2027 最强爆发不在“通用 chiplet marketplace”，而在“被系统瓶颈强制购买”的环节：HBM/HBM4E、Custom HBM base die、先进封装产能、64G UCIe/D2D IP、3DIC EDA/验证、SLM/DFT/test、CPO/photonic interposer 的早期设计卡位。

## 会议一手信号

### 官方议程和参与结构

Chiplet Summit 2026 官方站点显示会议时间为 2026 年 2 月 17-19 日，地点为 Santa Clara Convention Center。官方 program-at-a-glance 的动态 XML/iframe 数据显示：

| 指标 | 统计 |
|---|---:|
| 演讲/主持/嘉宾记录 | 368 |
| 唯一 session | 70 |
| 参与组织 | 105 |
| Tuesday 记录 | 122 |
| Wednesday 记录 | 140 |
| Thursday 记录 | 106 |
| Top 组织 | Siemens 44、Synopsys 38、Cadence 25、Intel 22、Arm/Marvell/Alphawave 各 9、Yole/Samsung/Daedaelus 各 7 |

议程结构也很清楚：10 个 pre-con tutorial、8 个 keynote、4 个 special presentation，以及大量 D2D/HBM/Packaging/Test/Security/Automotive/Optical/Design session。会议密度说明 chiplet 生态已经从“技术展示”进入“产业工作分解”：谁做标准、谁做 IP、谁做封装、谁做验证、谁做安全、谁做量产。

### Keynotes 的方向变化

Keynote 主题本身就是一张路线图：

- Synopsys：AI-driven multi-die design，强调 AI 自动化多 die 设计。
- Alphawave/Qualcomm：connectivity 是 system-level design 的基础。
- Siemens：3D IC for AI with AI，强调 3D IC 的 multiphysics、signoff、digital twin 和 AI-driven flow。
- UCIe Consortium：open chiplet ecosystem at package level。
- Cadence：Chiplets for Everyone，强调 off-the-shelf、plug-and-play chiplets 和 Physical AI。
- Arm：open chiplet ecosystem for converged AI datacenter。
- OCP：open ecosystems for next wave of AI inference。
- Marvell：custom memory/connectivity/power/optics chiplets for XPUs，并提出 power is the new currency of datacenter。

这意味着市场重心从“chiplet 作为封装结构”转为“chiplet 作为 AI 数据中心和边缘 AI 的供应链组织方式”。

### Best of Show 暗示产业评审标准

官方 Best of Show 三个获奖项也很有信号：

- Packaging Design：Siemens EDA “Innovator3D IC”。
- Packaging Hardware：Sarcina Technology “Advanced Packaging”。
- Connectivity & Interoperability：UCIe Consortium “UCIe 3.0 Specification”。

评审维度包括多厂商互操作、compliance/plugfest、lane repair、flow control、QoS、telemetry、设计套件、合规套件和量产路径。这说明会议认可的“好技术”不是单项性能，而是生态可落地程度。

## 重点发展方向和变化

### 1. HBM 从“配套内存”变成 AI XPU 架构中心

Yole 的 HBM Markets 会议材料给出非常直接的数字：HBM 市场 2025 年约 350 亿美元、2026 年约 600 亿美元、2027 年约 800 亿美元、2031 年约 1700 亿美元；2025 年 YoY +102%，2026 年 YoY +70%，2025-2031 年 CAGR 约 30%。Yole 同时判断 HBM 到 2031 年可能超过 DRAM 收入 40%。

Marvell 的 Custom HBM 材料把问题讲得更工程化：标准 HBM 对 XPU die 的可复用性、方向、tiling、3D SOIC footprint 都造成约束；HBM4E 每 2048-bit stack 带宽可超过 3.5 TB/s，而 LPDDR5X 只有约 68-85 GB/s，CXL 3.0 via PCIe 6.0 x16 约 128 GB/s。Marvell 还给出 PHY/base die 功耗量级：10G 下 PHY 约 8W、base die 约 25W；13.8G 下 PHY 约 11.2W、base die 约 35W。

关键变化：过去市场把 HBM 看成内存 ASP 暴涨；会议视角则是 Custom HBM base die、near-memory function、D2D optimized PHY 会改变 XPU 架构和供应链议价。

### 2. UCIe 3.0 的重点不是“更快”，而是“可管理、可信、可量产”

UCIe 3.0 已把数据率提升到 48/64 GT/s。Chiplet Summit 的 UCIe 3.0/RoT 材料强调 Management Director：它发现 chiplets 和 management elements，同时作为 manageability Root of Trust。材料明确列出多厂商 SiP 的威胁：不可信 chiplet 访问敏感数据、恶意 chiplet 破坏系统完整性、供应链攻击、side-channel、DoS 等。

Alphawave/Qualcomm 的 64G UCIe 材料显示其 UCIe D2D building blocks 已覆盖 7nm、6nm、5nm、4nm、3nm、2nm；并给出 package 类型差异：standard package 约 110-130 um bump pitch、25mm+ reach；silicon interposer/RDL interposer 约 25-55 um、1-5mm；silicon bridge 约 25-45 um、1-5mm。

关键变化：UCIe 从“PHY/协议标准”升级为“多供应商 chiplet 市场的管理和安全底座”。没有 RoT、访问控制、DFT、SLM、compliance，open chiplet 经济就不会发生。

### 3. “1000-chiplet challenge” 把问题从芯片设计推到系统编排

Pre-Con F 主题为 Meeting the 1000-Chiplet Challenge，议程包括 scalable security、pathfinding/prototyping/signoff、boot firmware、hardware/software verification。官方 session 摘要指出，千芯粒系统需要 ROM startup 和 orchestration software 来分配 chiplet ID、类型、安全状态、位置、尺寸、功耗和热状态等。

关键变化：此前 chiplet 叙事多是“把大 die 拆小、提升良率”；2026 年讨论已经进入“千级实体的启动、命名、认证、调度、监控、隔离和验证”。这更接近数据中心系统工程，不再只是 IC 后端工程。

### 4. 先进封装成为 AI 部署的 gating factor

Intel 的 Chiplet Packaging to Scale AI 材料给出几条硬事实：AI scaling 需要更多 compute 和 memory，也就需要把更多 Si 放到 package 上；EMIB-T 支持 >10x reticle complex，pitch scaling capability below 45 um，且“no limit to number of top die or EMIB on package”。同一材料指出，未来更大的 package/die complex 可能需要放弃传统 SMT，转向 mechanical clamping；热管理可能需要 immersion cooling；UCIe 3.0 每 32 条 data lane 有 2 条 redundant lane。

TSMC 方面，TrendForce 2026 年 4 月报道援引 TechNews 与机构投资者数据，TSMC CoWoS 月产能预计到 2026 年底达到约 11.5 万至 14 万片，2027 年约 17 万片；CoPoS panel-level packaging 有望 2028-2029 年开始量产。

关键变化：先进封装的瓶颈从“有没有 CoWoS”扩展到 warpage、power delivery、thermal、lane repair、yield redundancy、mechanical attach 和面板级生产效率。

### 5. 光互连从“未来方向”进入 package-level 架构候选

Lightmatter 的 Photonic Interposer 材料给出很激进的系统数字：其 reference design example M1000 可达 up to 114 Tbps Tx+Rx bandwidth、1024 SerDes、4000 mm² silicon die complex、256 fibers、34 chiplets。材料还指出，102T switch ASIC 若用铜连接会产生 2040 个 224G connections；AI supercomputer scale-up domain 从 2022 年 8 GPUs 到 2024 年 72 GPUs，再到 2025 年 576 GPUs。

关键变化：CPO/photonic interposer 目前收入很小，但问题正在从“交换机 optics”进入“chiplet 下方/旁边的可编程 optical fabric”。一旦 224G/448G electrical reach 继续缩短，光互连会从可选优化变成 rack-scale AI 的必要条件。

### 6. Automotive/Physical AI 是强主题，但量产节奏不会像数据中心

会议有 State of the Art in Automotive Chiplets、What Developers Must Know about Automotive Chiplets、Safety-Critical Physical AI Applications Using RISC-V 等内容。Cadence keynote 也把 Physical AI 作为 chiplet edge 需求。汽车半导体市场本身很大，S&P Global Mobility 预测从 2025 年约 900 亿美元到 2031 年约 1390 亿美元，CAGR 约 7.5%。

关键变化：汽车 chiplet 不是 2026-2027 的最大收入爆点，因为功能安全、车规验证、生命周期、供应链责任划分都会拉长周期；但它会推动 eFPGA chiplet、RISC-V safety island、ASIL 级监控、长期可维护 IP 的需求。

## 哪些产品和技术会爆发

### HBM4/HBM4E 和 Custom HBM：爆发力度最强

基准口径：2026 年 HBM 收入约 600 亿美元，2027 年约 800 亿美元，增速约 +33%。HBM4 在 2026 年进入主流 AI accelerator roadmap，HBM4E 在 2027-2028 年接棒，custom HBM base die 从顶级 hyperscaler/XPU 厂商开始。

乐观口径：HBM 供应继续紧缺，HBM4/4E ASP 维持高位，2027 年收入可达 950 亿美元左右，增速约 +58%。Custom HBM 的价值不止内存堆栈，还包括 base die、PHY、near-memory、memory expansion 和封装协同。

超预期乐观口径：agentic AI/physical AI 推动推理上下文和 KV cache 继续膨胀，HBM 2027 年可冲击 1100 亿美元，增速约 +80%。这种情形下，HBM 供应商和能拿到 Custom HBM 设计窗口的 ASIC/平台商利润率会维持极高水平。

### 64G UCIe/D2D IP：爆发不在数量，而在设计锁定

基准口径：2026 年是 UCIe 3.0 IP、VIP、compliance、simulation、interposer/package co-design 的设计导入年，2027 年进入更多 hyperscaler ASIC 和 AI accelerator tape-out。收入规模不如 HBM，但粘性和毛利率高。

乐观口径：64G UCIe 在 2027 年变成高端 AI package 的事实标准之一，尤其是 HBM streaming、DDR/CXL retimer、multi-IO die、optical chiplet 场景。Synopsys/Cadence/Siemens/Alphawave/Arteris/Keysight 等受益。

超预期乐观口径：UCIe 3.0 的 manageability/RoT/compliance 体系提前成熟，2027 年出现实质性多厂商 plug-and-play 设计流。真正受益的是“IP + VIP + EDA + test + reference design”的组合，而不是单独卖 PHY。

### 先进封装和 3DIC 设计平台：产能、良率、warpage 是价值来源

基准口径：CoWoS/EMIB/SoIC/2.5D/3D 保持高需求，先进封装 2027 年收入约 630 亿美元。封装环节收入增速没有 HBM 高，但供需紧张使高端产能具有强定价能力。

乐观口径：TSMC CoWoS、Intel EMIB-T、Samsung/OSAT 高端封装加速扩产，2027 年市场约 690 亿美元，AI 高端封装增速显著高于总市场。

超预期乐观口径：CoPoS/玻璃/面板级封装路线提前获得大客户验证，AI ASIC 和 GPU package size 继续放大，2027 年先进封装市场可接近 780 亿美元。

### Photonic interposer/CPO：短期小市场，长期高弹性

基准口径：CPO 市场 2026 年约 1.65 亿美元，2027 年约 2.2 亿美元。2026-2027 仍以 proof-of-concept、早期 switch、co-packaged optical engine、in-package optical fabric 评估为主。

乐观口径：NVIDIA/Meta/Google 等 AI scale-up 网络拉动 800G/1.6T/3.2T optics 和 CPO，2027 年 CPO 市场约 2.8 亿美元。

超预期乐观口径：224G electrical bottleneck 比预期更早触顶，photonic interposer 在 rack-scale AI 变成架构必选，2027 年 CPO/光 chiplet 可超过 4 亿美元，2028-2030 年加速曲线会陡峭很多。

### eFPGA chiplet：不是大众爆品，但适合高毛利利基

QuickLogic 的 eFPGA chiplet on Intel 18A 材料强调 performance、adaptability、longevity，支持 UCIe adapter/PHY，DSP 场景可到 60 GSps、30 GHz BW、约 70 dBc SFDR、约 1W/channel。

基准口径：2027 年主要在国防、通信、工业、航天、Physical AI sensor fusion 等小批量高价值领域放量。

乐观口径：UCIe chiplet reference flow 成熟，eFPGA chiplet 成为“长期可更新 ASIC”的标准选项。

超预期乐观口径：车规/工业生命周期压力把 eFPGA chiplet 推成可复用平台，供应商从 IP 授权转向 chiplet 产品和模块销售。

## 市场规模、增速和利润率预测

| 产品/技术 | 2026 当前市场规模 | 当前利润率判断 | 2027 基准 | 2027 乐观 | 2027 超预期乐观 |
|---|---:|---|---:|---:|---:|
| HBM/HBM4/HBM4E | 约 600 亿美元 | HBM 毛利率估计 55-65%；头部供应商显著高于通用 DRAM | 800 亿美元，+33%，毛利 55-60% | 950 亿美元，+58%，毛利 60-65% | 1100 亿美元，+83%，毛利 65-70% |
| 先进封装总市场 | 约 575 亿美元 | 高端 CoWoS/2.5D/3D 毛利 30-45%，传统 OSAT 混合后 20-35% | 630 亿美元，+10%，利润率小幅上行 | 690 亿美元，+20%，高端供需继续偏紧 | 780 亿美元，+36%，AI 高端封装强定价 |
| Chiplet 产品市场，窄口径 | 约 193 亿美元 | AI chiplet 产品毛利 45-70%，取决于是否含 GPU/ASIC/HBM | 280 亿美元，+45% | 330 亿美元，+70% | 400 亿美元，+108% |
| D2D/UCIe/3DIC EDA+IP 子市场 | 估计 15 亿美元 | 软件/IP 毛利 80-95%，经营利润率 25-45% | 19 亿美元，+25% | 22 亿美元，+45% | 26 亿美元，+75% |
| CPO/photonic chiplet | 约 1.65 亿美元 | 产业早期，模块/器件毛利 20-40%，公司 EBIT 多数仍低或为负 | 2.2 亿美元，+35% | 2.8 亿美元，+70% | 4.1 亿美元，+150% |
| Automotive chiplet/Physical AI chiplet | 真正 chiplet 收入估计 2-5 亿美元；汽车半导体约 900 亿美元 | 车规芯片毛利 25-45%；IP/软件更高 | 4-6 亿美元，+30-50% | 7-9 亿美元，+80% | 10-13 亿美元，+150% |
| Test/DFT/SLM/KGD for chiplets | 估计 8-12 亿美元 | ATE/软件/服务混合毛利 45-80% | 10-14 亿美元，+20% | 12-16 亿美元，+35% | 15-20 亿美元，+60% |

### 口径解释

HBM 使用 Yole 在 Chiplet Summit 2026 材料中的公开数字。先进封装使用 Mordor 2026 年 574.6 亿美元口径，并用 Yole 2024 年 460 亿美元、2030 年 794 亿美元作交叉校验。Chiplet 产品市场使用 2026 年 192.7 亿美元的窄口径市场研究，但需要强调，Jim Handy 在会议上也指出 chiplets 不创造新终端市场，而是用更经济的方式服务已有市场，所以广口径和窄口径差异会非常大。D2D/UCIe/3DIC EDA+IP 是我从 EDA+IP 市场和 semiconductor IP 市场中拆出的 chiplet 相关子集估计。

## 关键路线图

### 2026 年：设计导入和产能争夺

- HBM4 初期产品进入 AI accelerator roadmap，HBM3E 仍是收入主力。
- UCIe 3.0 设计/IP/VIP/仿真开始进入实际项目，64G 成为高端讨论焦点。
- CoWoS/EMIB/SoIC 等高端封装继续是 AI 供给约束。
- Digital twin、hardware-in-the-loop、SLM、DFT、RoT 从“nice to have”变成 open chiplet 的必要条件。
- Photonic interposer 以样机和 reference design 证明带宽密度，但收入仍小。

### 2027 年：HBM4E、UCIe 3.0 和 AI ASIC 扩散

- HBM 市场基准可到约 800 亿美元，HBM4E 开始为 2028 年主力做准备。
- UCIe 3.0 的 manageability/security/compliance 是否成熟，将决定开放 chiplet 生态是真突破还是继续停留在同厂商封闭集成。
- CoWoS 产能约 17 万片/月的规划若兑现，AI GPU/ASIC 供给瓶颈将从单一封装产能转向功耗、散热、HBM、基板材料和测试良率。
- Automotive/Physical AI 还不会大规模爆发，但会形成设计 win。

### 2028-2029 年：面板级封装、CPO 和 custom HBM 进入更大规模

- CoPoS/玻璃/面板级路线若量产，可能改变超大 package 成本曲线。
- HBM5、hybrid bonding、20Hi stack 等推动内存和封装协同更深。
- CPO/photonic interposer 若进入 AI scale-up 网络，会从小市场突然变成高弹性细分赛道。

## 可能违背当前市场共识的洞见

### 洞见 1：通用 chiplet marketplace 可能慢于预期

会议声量很大，但真正要跨厂商复用 chiplet，必须解决 RoT、compliance、thermal/power envelope、business model、test responsibility、known-good-die、failure liability。UCIe 3.0 是必要条件，不是充分条件。2026-2027 更容易落地的是同一大客户/同一平台内的可复用 chiplet，而不是像软件包管理器一样的开放市场。

### 洞见 2：HBM 的“利润爆发”可能比 AI accelerator 更纯

AI accelerator 需要承受软件生态、客户集中、迭代风险和供应链成本；HBM 则是所有高端 AI XPU 的共同刚需。Yole 给出的 2026 年 600 亿美元和 2027 年 800 亿美元意味着 HBM 已经不是配套市场，而是 AI 半导体利润池本身。

### 洞见 3：先进封装的下一瓶颈不是产能，而是物理可靠性

Intel 材料提到大 package warpage、mechanical clamping、vertical power delivery、immersion cooling、redundant lanes。这说明即使 CoWoS 产能上来，系统仍会在热、机械、电源完整性和测试处遇到瓶颈。只看“月产能”会低估后段工程复杂度。

### 洞见 4：UCIe 3.0 的 RoT 价值可能高于 64 GT/s

市场容易盯着 64 GT/s，但会议材料中最关键的其实是 Management Director/RoT、access control、security clearance group、prohibited access check。开放 chiplet 经济要解决的是“我能不能信任这个 die”，不是“这个 die 能跑多快”。

### 洞见 5：CPO 的 2026 收入小，不代表技术不重要

CPO 市场 2026 年只有约 1.65 亿美元量级，但 Lightmatter 会议材料已经把问题拉到 114 Tbps、1024 SerDes、256 fibers、34 chiplets 的系统层级。对于 AI rack，CPO/photonic interposer 的重要性会在收入曲线上明显滞后体现。

### 洞见 6：Automotive chiplet 会先是“架构权”而不是“收入权”

汽车半导体约 900 亿美元级别，但 chiplet 化受安全认证、供应链责任和生命周期约束。2026-2027 更重要的是谁定义车规 chiplet 的 safety/security/monitoring interface，而不是谁已经拿到大规模收入。

## 重点受益环节排序

1. HBM/HBM4E/Custom HBM：收入弹性最大、利润率最高、需求确定性最强。
2. 高端先进封装产能和材料：CoWoS/EMIB/SoIC/CoPoS、玻璃、基板、power delivery、thermal。
3. D2D/UCIe IP/VIP/3DIC EDA：市场规模小于硬件，但毛利和粘性极强。
4. Test/DFT/SLM/KGD：chiplet 量产越复杂，测试越从成本项变成架构项。
5. Photonic interposer/CPO：短期小，长期可能出现非线性放量。
6. eFPGA/RISC-V/Physical AI chiplets：利基高毛利，尤其适合车规、工业、国防和边缘 AI。

## 主要来源

- Chiplet Summit 2026 官方 Program at a Glance：<https://chipletsummit.com/2026-program-at-a-glance/>
- Chiplet Summit 2026 官方 Keynotes：<https://chipletsummit.com/2026-keynotes-and-special-presentations-2/>
- Chiplet Summit 2026 官方 speaker XML：<https://realintelligence.com/customers/expos/00D5f000000Kf85/SNS_xmlcreator/a0qVV0000032cp3_showspeakerlist.xml>
- Chiplet Summit 2026 detailed session iframe，2 月 17 日：<https://realintelligence.com/customers/expos/00D5f000000Kf85/index-Details-iframe-anchors.php?eventId=a0qVV0000032cp3&orgId=00D5f000000Kf85&eventdate=2026-02-17&trackCategory=Session>
- Chiplet Summit 2026 detailed session iframe，2 月 18 日：<https://realintelligence.com/customers/expos/00D5f000000Kf85/index-Details-iframe-anchors.php?eventId=a0qVV0000032cp3&orgId=00D5f000000Kf85&eventdate=2026-02-18&trackCategory=Session>
- Chiplet Summit 2026 detailed session iframe，2 月 19 日：<https://realintelligence.com/customers/expos/00D5f000000Kf85/index-Details-iframe-anchors.php?eventId=a0qVV0000032cp3&orgId=00D5f000000Kf85&eventdate=2026-02-19&trackCategory=Session>
- Yole Group, High Bandwidth Memory Markets, Chiplet Summit 2026 PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260217_PreConB_Bertolazzi.PDF>
- Jim Handy, Objective Analysis, The Chiplet Market Today, Chiplet Summit 2026 PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_PLEN_Handy.PDF>
- Marvell, Using Customized HBM Solutions in Data Center Applications PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260217_PreConB_Allman.PDF>
- Rebellions, Rebel100 2 PFLOPS Quad-Chiplet AI SoC with 4 TB/s UCIe PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260217_PreConD_Jin.PDF>
- Siemens/Avery, Scalable Chiplet Integration with UCIe 3.0 and RoT PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_A-101_Li.PDF>
- Alphawave Semi, Designing Reliable 64G UCIe Chiplet Interconnects PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_B-101_Cheruliyil.PDF>
- Intel, Chiplet Packaging to Scale AI PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260218_E-103_Hosseini.PDF>
- Lightmatter, Photonic Interposer Supports Terabit Chiplet-Based Systems PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260219_B-202_Nowroozi.PDF>
- QuickLogic, Building an eFPGA Chiplet Ecosystem PDF：<https://chipletsummit.com/proceeding_files/a0qVV0000032cp3/20260219_E-202_Peterson.PDF>
- Chiplet Summit 2026 Best of Show Awards：<https://chipletsummit.com/2026-best-of-show-awards/>
- UCIe 3.0 公开发布信息：<https://www.design-reuse.com/news/202529142-ucie-consortium-introduces-3-0-specification-with-64-gt-s-performance-and-enhanced-manageability/>
- TrendForce on TSMC CoWoS/CoPoS, 2026-04-16：<https://www.trendforce.com/news/2026/04/16/news-tsmc-says-cowos-offers-industrys-largest-reticle-size-packaging-amid-intel-emib-rivalry-copos-advances/>
- Mordor advanced packaging market 2026-2031：<https://www.mordorintelligence.com/industry-reports/advanced-packaging-market>
- Yole advanced packaging public summary：<https://www.edge-ai-vision.com/2025/09/advanced-packaging-market-set-to-reach-79-4-billion-by-2030/>
- Coherent Market Insights chiplet market 2026-2033：<https://www.coherentmarketinsights.com/industry-reports/chiplet-market>
- Mordor CPO market 2026-2031：<https://www.mordorintelligence.com/industry-reports/co-packaged-optics-market>
- Semiconductor Engineering, EDA and IP Q4 2025：<https://semiengineering.com/eda-and-ip-numbers-up-again-but-numbers-are-more-nuanced/>
- SIA, 2025 global semiconductor sales and 2026 outlook：<https://www.semiconductors.org/global-annual-semiconductor-sales-increase-25-6-to-791-7-billion-in-2025/>
- S&P Global Mobility, automotive semiconductor 2026 trends：<https://www.spglobal.com/automotive-insights/en/blogs/2026/04/automotive-semiconductor-market-trends>
