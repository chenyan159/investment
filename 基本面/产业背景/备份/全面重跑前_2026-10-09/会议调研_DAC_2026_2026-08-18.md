# 会议追踪：DAC 2026

> **会议**：第 63 届 Design Automation Conference（DAC，Chips to Systems Conference）  
> **会议日期**：2026-07-26 至 2026-07-29  
> **地点**：美国加州长滩（Long Beach, California），Long Beach Convention Center  
> **材料检索截止日期**：2026-08-18（America/Los_Angeles）  
> **报告完成日期**：2026-08-18  
> **研究范围**：EDA、芯片设计、先进封装、chiplet、验证、设计—制造协同、AI 辅助设计、RISC-V、汽车与边缘芯片  
> **研究原则**：本报告从外部公开资料独立重建，不读取、不引用、不继承项目内既有研究结论。金额如无特别说明均为美元。

## 结论摘要

### 核心判断

1. **DAC 2026 最重要的变化不是“生成式 AI 进入 EDA”，而是 AI 从问答、代码补全和单点优化，转向可长时间运行、调用多种工具并由确定性求解器自校验的闭环工作流。** 2025 年 DAC 已经讨论 reasoning agents、agentic AI 和“生成式 AI 是否在幻觉”；2026 年三大 EDA 厂商同时把竞争焦点放在 orchestration、golden signoff、物理场校验、权限审计和跨工具状态管理。模型本身不再是唯一瓶颈，真正难点变成上下文、工具接口、设计数据、可靠性和企业部署。

2. **AI 生产率已有真实客户数据，但“50×”“100×”不能横向比较。** Cadence 前代 Cerebrus 已用于超过 1,000 个量产设计，Samsung 客户披露 4× 整体生产率、8%–11% PPA 改善；Cadence/TSMC 的基板自动布线披露 100× 生产率且结果接近人工，FORVIA HELLA 披露 300 个器件布局从最多 4 天缩短到 4 分钟。相比之下，Synopsys 在 DAC 披露的 50× 验证闭环仍处客户评估、计划 2026 年下半年可用；Siemens Fuse 的新增能力标注为后续版本，STMicroelectronics 也只是“计划测试验证”。因此，**已有商用能力集中在设计空间探索、物理实现、求解器加速和受约束的重复任务；端到端自主设计仍处试用阶段。**

3. **生成式 AI 在未来一年更可能扩大 EDA 的收入池，而不是压缩席位。** 设计复杂度、验证覆盖、算力消耗和方案探索数量同步增长，客户会把节省的工程时间投入更多设计点、更多场景和更早的物理验证。商业模式将从单一订阅席位扩展为“平台订阅 + agent/orchestration 加价 + GPU/云用量 + 私有部署与治理”。短期风险不是工程师被替代，而是 AI 推理和仿真成本吞噬增量毛利、客户用自研 agent 把价值留在内部。

4. **EDA 的护城河从“算法和单点工具”上移到五层组合：** 经晶圆厂认证的签核引擎、跨流程设计图谱与 API、客户专有数据的安全使用、可审计的 agent runtime、以及 GPU 加速的确定性物理求解。自然语言界面和通用 RTL 生成会迅速同质化；PDK/PADK 认证、signoff correlation、历史 tapeout 经验和跨域闭环不会同速商品化。

5. **Chiplet 的主要瓶颈已从“有没有 die-to-die 标准”转向“能否把多颗已知良品裸片可靠、可测试、可散热地做成系统”。** UCIe 3.0 已支持 48/64 GT/s，UCIe 2.0 已覆盖 3D 混合键合与 DFx，但 2026 年最明确的跨厂商实物证据仍是 Intel 与 Cadence 的 16G UCIe-S 演示。协议带宽领先于多厂商量产生态；热—机械—电耦合、known-good-die、封装内可观测性、模型交换、良率归因和责任边界更可能决定采用速度。

6. **先进封装最被低估的利润池是测试、量测、失效分析、多物理场软件和设计数据基础设施。** DAC 官方议程中的产业专题估计先进 multi-die 封装测试可占总制造成本的 30%–50%；该数字不是审计后的行业平均值，但与 SEMI 对测试设备 2026 年增长 31% 至 153 亿美元的预测方向一致。封装设备同期预计仅增长 9.6%，说明价值正在向“确保每颗昂贵 die 和每条互连可用”的测试与良率环节倾斜。

7. **硅光/CPO 已越过“只有实验室样机”的门槛，但尚未越过“广泛规模化”的门槛。** NVIDIA 称 Spectrum-X Ethernet Photonics CPO 交换机已进入生产，首批采用者包括 CoreWeave、Lambda 和 OCI，系统出货计划从 2026 年秋季开始；TSMC 称基于 COUPE 的真正 CPO 方案于 2026 年开始生产。与此同时，DAC 的电子—光子设计自动化专题仍指出协同仿真、自动布局、验证、DFM、光纤耦合与良率工具链碎片化。未来两年受益顺序更可能是仿真/EDA、光子封装、精密装配与测试先于纯 CPO 组件收入全面爆发。

8. **RISC-V、汽车和边缘芯片在 DAC 2026 是重要的工具需求来源，但不是本届最强的即时商业发布主线。** Qualcomm 的 keynote 把设计空间从低于 5W 的个人/边缘设备延伸到最高约 500W 的云服务器，强调共用 CPU/GPU/AI/连接/安全 IP 库和自动化 SoC 组装；DAC 的 RISC-V 内容更多集中在验证、模糊测试、安全和可配置性。Infineon 的汽车 RISC-V AURIX 家族仍是“未来数年推出”并以虚拟原型提前建生态，说明其近期利润影响主要落在验证、虚拟平台、功能安全和 IP 集成工具，而非大规模 MCU 出货。

9. **未来三个月的直接兑现点是软件可用性和客户试用转商用；一年期兑现点是 AI 模块的续约附加率、多物理场 attach rate、封装/测试设备订单；两年期兑现点是 64G UCIe 多厂商产品、CPO 规模出货和超大 CoWoS。** TSMC 已生产 5.5 倍光罩尺寸 CoWoS，14 倍光罩、约可容纳 10 颗大型计算 die 和 20 组 HBM 的版本计划 2028 年生产。若这些路线图按期，EDA、测试和先进封装的需求将延续；若只看到封装面积变大而良率、功耗和测试时间不改善，利润率会先于收入见顶。

10. **投资上最值得跟踪的是“可信闭环”和“制造可兑现性”，不是发布会上的 autonomy 等级。** 直接受益者是拥有签核/多物理场/验证全栈的 Synopsys、Cadence、Siemens，以及 GPU 求解层的 NVIDIA；制造端是 TSMC、先进封装与测试设备、量测和高端 OSAT。过度乐观方向包括没有签核资产的通用 AI-EDA agent、立即形成的开放 chiplet 现货市场、2027 年前 CPO 全面替代可插拔光模块，以及大幅削减设计工程师席位的假设。

### 一页式投资结论

| 方向 | 当前结论 | 未来一年 | 主要证伪指标 |
|---|---|---|---|
| EDA agentic AI | 加速，已从助手转向闭环；成熟度高度分化 | 增量收入大于席位侵蚀，先在验证、实现、调试和多物理场落地 | H2 2026 产品延迟；无新增具名量产客户；推理成本高于节省价值 |
| EDA/IP 利润池 | 高质量、经常性收入；SIP 增速快于部分传统物理设计类别 | 基准情景 ESD 收入约增长 11% | EDMD 连续两季低于 6%；大客户转向自研且减少厂商用量 |
| Chiplet/3D-IC | 架构确定，开放生态仍早 | 工具、DFx、热/机械、substrate 和 KGD 优先兑现 | 只有同厂商垂直整合，没有 32/64G 多厂商量产互操作 |
| 先进封装 | 结构性增长，AI/HBM 驱动 | 广义市场基准增长约 10%，高端 2.5D/3D 约 23% | CoWoS/HBM 利用率下降、良率恶化、客户延后加速器项目 |
| 测试/量测 | 被低估，复杂度增长快于封装设备台数 | 测试设备基准增长约 18%（本报告情景） | 测试时长/成本随代际下降、设备订单增速明显低于封装产能 |
| 硅光/CPO | 已有生产点，产业链尚未规模化 | 光子封装先受益，CPO 收入低基数高波动 | 秋季出货延迟、现场可靠性不达标、1.6T/3.2T 可插拔方案延寿 |
| RISC-V/汽车/边缘 | 标准和虚拟原型加速，量产节奏慢 | 增量先体现在验证、功能安全、虚拟平台和 IP 集成 | 无 AEC-Q/ASIL 工具链、无样片/具名车型、软件生态继续碎片化 |

## 研究口径、证据等级与已知资料缺口

### 事实、估算和观点的分界

- **事实**：官方议程、标准、产品可用性、具名客户陈述、财报和协会统计；正文尽量注明材料发布日期。厂商新闻稿中的数字仍是“厂商披露事实”，不等同于第三方审计。
- **估算**：本报告根据公开基数和明确公式推导的年化规模、插值市场规模和未来一年三情景。估算均在表格中单列，不能与来源原始预测混称。
- **观点/判断**：对产业节奏、竞争壁垒、利润池和公司影响的解释；均给出可观察的证伪指标。

### 证据等级

| 等级 | 定义 | 使用方式 |
|---|---|---|
| A1 | 官方量产/正式可用；具名客户、订单、出货或财务数据可核验 | 可作为“已商业化”依据 |
| A2 | 官方认证或具名客户试用/部署，但结果由供应商发布，未独立审计 | 可作为采用证据，不外推为全客户平均值 |
| B | 厂商 benchmark、会议演示、论文原型或未具名客户案例 | 仅说明技术可行性和上限，不视作收入证明 |
| C | 专业媒体、分析机构预测或供应链线索 | 用于市场口径和交叉验证，明确不确定性 |

### 资料覆盖与冲突说明

1. DAC 官网在检索快照中称 **55% 的 program 覆盖 AI & Design**、Research submissions 增长 **26.34%**、Engineering submissions 增长 **26%**；2026-05-04 官方新闻稿则称 **40% 的 technical program 聚焦 AI and design**，并另写 Research Track submissions 为 **30.7%**。这很可能来自页面版本、分母和“program/technical program/session/submission”定义差异。本报告只把它们用作 **40%–55% 的主题密度区间**，不计算精确同比百分点。[DAC 2026 官网，检索于 2026-08-18](https://dac.com/2026)；[DAC 2026 新闻稿，2026-05-04](https://dac.com/2026/press-release/the-2026-dac-chips-to-systems-conference-comes-to-long-beach-for-the-first-time-with-record-growth-as-ai-reshapes-chip-and-system-design)
2. 2025 年官方口径是 **AI-related sessions 占 32%**，而 2026 年口径是 **AI & Design**，两者并非同一分类。因此可以判断 AI/设计加速，但不能严谨地写成“上升 23 个百分点”。[DAC 2025 会后新闻稿，2025-07-15](https://archive.dac.com/media-center/dac-press-releases/ai-reshapes-the-future-at-dac-2025-a-breakthrough-year-for-innovation.html)
3. 2026 年官方称 550+ technical sessions、120+ exhibitors；2025 年页面称约 130 家展示/套房提供商，另有 25 个首次参展商。session、presentation、exhibitor、suite provider 的定义不同，**不能用总数直接推断需求增速**。
4. 截至检索截止日，DAC 官网已经转为“Thank You for Attending”，但尚未找到同等口径的 2026 最终参会人数、完整获奖结果公告或所有视频的稳定索引。报告不猜测这些数据，也不把候选论文写成最终 Best Paper 获奖者。[DAC Media Center，检索于 2026-08-18](https://dac.com/2026/media-center)

## 会议重点和相较 2025 年的变化

### 官方信号

**事实（材料日期 2026-05-04；官网检索 2026-08-18）**：第 63 届 DAC 在长滩首次举办，官方列出 550+ 技术 session、120+ 参展企业、15 家首次参加的 AI-focused 公司；Research 和 Engineering submissions 均创高。Keynote/SKYTalk 的产业主线由 Qualcomm 的端—云 AI 设计自动化、NVIDIA 的 AI supercomputing + EDA、Intel 的异构集成、IBM 的先进节点与封装、Microsoft 的 AI accelerator EDA 组成。[官方新闻稿](https://dac.com/2026/press-release/the-2026-dac-chips-to-systems-conference-comes-to-long-beach-for-the-first-time-with-record-growth-as-ai-reshapes-chip-and-system-design)；[官方完整 PDF 议程，2026-07-22 版本](https://confcats-siteplex.s3.amazonaws.com/dac/images/dac-2026_program_july-22.pdf)

**判断**：会名中的 “Chips to Systems” 在 2026 年不再只是品牌扩展，而是产品边界实质变化。三大 EDA 厂商的发布都跨越 chip、package、PCB、热/机械/电磁和系统仿真；这会扩大可服务市场，也会增加并购、整合和算力成本。

### 十个关键变化

| 变化 | 2025 年/会前预期 | DAC 2026 公开证据 | 方向判断 |
|---|---|---|---|
| 1. 从 copilot 到 long-running agent | 2025 已有 reasoning agent 和 agentic AI 讨论，核心争议仍是“幻觉还是创新” | Synopsys、Siemens、Cadence 均发布多 agent 编排、闭环验证和跨流程 autonomous workflow | **加速**；新意在执行深度与自校验，不在“有无 LLM” |
| 2. 从代码生成到验证闭环 | 会前市场更关注 spec-to-RTL/代码生成 | DAC 议程大量转向 test plan、coverage closure、RCA、formal、waveform、mutation-based benchmark | **转向**；价值重心由生成转到证明正确 |
| 3. 从单点 PPA 到系统多物理场 | 2025 AI + chiplet + sustainability 已是三大主题 | Synopsys/Ansys、Cadence AuraStack、Siemens Fuse 都把 thermal/EM/PI/SI/mechanical 纳入 agent 回路 | **加速**；多物理场成为平台 attach，而非独立后处理 |
| 4. 从“chiplet 可行”到“chiplet 可制造” | 2025 Chiplet Pavilion 强调架构、标准、模块化 | 2026 重点是 KGD、测试访问、DFx、热—机械—电耦合、封装模型和跨厂商责任 | **转向**；瓶颈从 PHY 逐步移到制造与系统工程 |
| 5. UCIe 从标准到有限实物互操作 | UCIe 3.0 已于 2025-08 发布 48/64 GT/s | 2026 首个 Intel/Cadence 16G UCIe-S 跨厂商 live demo | **加速但低于规格速度**；生态成熟落后于协议路线图 |
| 6. CPO 从路线图到生产起点 | 2025 仍以 Broadcom 低量、试验和 2028 后放量预期为主 | NVIDIA 称 CPO 交换机已生产；TSMC COUPE-on-substrate 2026 开始生产 | **加速**；但通用 EPDA、耦合、封装、良率仍不成熟 |
| 7. GPU 变成横向 EDA 基础设施 | 会前主要视作仿真加速 | NVIDIA 同时进入模型、agent toolkit、secure runtime、稀疏求解器和 EDA benchmark | **加速并改变价值分配**；EDA 厂商可能把部分增量毛利让给计算层 |
| 8. Shift-left 由方法论变成并购标的 | 架构探索长期重要，但工具链分散 | Siemens 连续收购 Precision Innovations 和 Defacto，补 early planning、SoC assembly/power intent | **加速**；表明 incumbent 仍有端到端缺口 |
| 9. 开放数据与 benchmark 成为约束 | 市场容易把模型能力当作瓶颈 | NotSoTiny、VeriScore、CVDP 等强调真实任务、污染、formal/mutation 评估；DAC 专题指出 academia/startup 缺数据和算力 | **转向基础设施竞争**；benchmark 质量决定营销数字可信度 |
| 10. RISC-V/汽车/边缘更偏工程化 | 会前预期开放 ISA、SDV、edge AI 会带来新产品潮 | DAC 以验证、安全、配置、虚拟平台和模块 IP 为主，缺少同量级量产发布 | **稳步推进而非爆发**；近期受益是工具与 IP 集成，而非终端出货突增 |

### 相对 2025 年，哪些加速、放缓或没有发生

**加速**：AI 驱动的验证闭环、GPU 求解器、多物理场融合、package/PCB agent、设计数据治理、测试与 DFT、先进封装容量和 CPO 生产准备。

**放缓/低于会前叙事**：开放 chiplet marketplace、多厂商 64G UCIe 量产、完全 autonomous tapeout、RISC-V 汽车大规模出货、对设计岗位的快速替代。

**未发生的关键事项**：没有足够公开证据表明某一新 agent 已独立完成复杂商用芯片从规格到签核并实现首轮流片成功；没有公开、可比、跨供应商的全流程成本/功耗/正确率 benchmark；没有证据证明新一代 AI 功能已经形成独立的大额订单池。

## 生成式 AI 对 EDA：生产率、商业模式与壁垒

### 已有客户数据支持的能力

| 能力/发布 | 公开数据 | 成熟度 | 研究解读 |
|---|---|---|---|
| Cadence Cerebrus（前代 block-level AI） | 已用于 1,000+ 量产设计；Samsung SARC 披露 4× 整体生产率，Samsung India 披露 SoC subsystem PPA 改善约 8%–11% | **A2：量产采用、具名客户** | 这是 AI-PPA 商业化最强基线；新一代 agent 不应把前代成绩全部归为自身 |
| Synopsys Multiphysics Fusion | 2026-06-17 已可部署；MediaTek 披露运行速度 10×；NVIDIA 披露 selected pilot 设计 closure 最快 5×、IR fix rate 最多 86%；Cisco/Samsung 提供采用或认证陈述 | **A2：正式可用、具名客户** | Synopsys 收购 Ansys 后最先兑现的协同，价值来自 golden solver 嵌入设计闭环 |
| Cadence/TSMC substrate autorouting | 多年合作，TSMC 披露客户生产率最多 100×，结果质量接近人工 | **A2：具名生态伙伴，但项目分布未披露** | 证明约束清晰的封装布线可高度自动化；不能等同整个 package 设计 100× |
| FORVIA HELLA AI-assisted placement | 300 个汽车电子器件布局由最多 4 天降至 4 分钟 | **A2：具名客户、单任务案例** | 重复布局任务可显著提效；未披露后续审核、EMC/可靠性签核总周期 |
| Synopsys AgentEngineer L4 | 2026-03 称客户一般 2×、部分 5×；DAC 的全自主 DV 称 validated RTL 最快 50×且 coverage 多 20% | **A2/B：前者客户使用，后者 benchmark/评估** | 50×的基准是“相对未使用 AgentEngineer 的传统流程”，缺少设计规模和客户名；不可作为平均值 |
| Synopsys + AMD + Microsoft Discovery | 早期评估 debug cycle 缩短 25%–40%，节省数周；AMD 正在积极评估 | **A2：具名试用，evaluation access** | 已越过纯 demo，但尚非大规模生产部署或订单 |
| Siemens Fuse/Solido | Library characterization TAT 超过 10×，token cost 降 5×–10×；ST 称有望少花数周调试，但计划测试验证 | **B/A2 混合：底层流程有生产基础，新能力待发布** | “生产 proven”描述针对 characterization 结果；ST 的 analyzer 仍是未来测试，不应写成已节省数周 |
| Bronco AI DV | 厂商在 DAC TechTalk 称生产 DV 问题可在 15 分钟内完成 RCA/修复，端到端首轮成功率 70% | **B：未具名客户、厂商演示** | 说明 startup 上限，但缺基准集、错误严重度和独立复核 |
| PRO-V-R1 论文 | 开源 agentic RTL verification：functional correctness 57.7%，robust fault detection 34.0%，高于基座模型 25.7%/21.8% | **B：研究 benchmark** | 绝对正确率仍不足以无人监督签核，反证“模型已不是瓶颈”不能被无限外推 |
| NotSoTiny 论文 | 以数百个 TinyTapeout 设计构造持续更新、formal/simulation 校验 benchmark，结论是现实任务显著难于既有基准 | **B：研究 benchmark** | 现有营销数据可能受任务过小、数据污染和验证宽松影响 |

来源：[Cadence Cerebrus 产品与客户陈述，检索于 2026-08-18](https://www.cadence.com/en_US/home/tools/digital-design-and-signoff/soc-implementation-and-floorplanning/cadence-cerebrus-ai-studio.html/)；[Synopsys Multiphysics Fusion，2026-06-17](https://news.synopsys.com/2026-06-17-Synopsys-Announces-Availability-of-the-First-Wave-of-Multiphysics-Fusion-Solutions)；[Cadence AuraStack，2026-07-16](https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-introduces-aurastack-ai-super-agent-the-worlds-first.html)；[Synopsys DAC 发布，2026-07-26](https://news.synopsys.com/2026-07-26-Synopsys-Showcases-Comprehensive-Autonomous-Engineering-Workflows-from-Silicon-to-Systems%2C-Developed-with-NVIDIA-Technology)；[Synopsys/AMD/Microsoft，2026-07-27](https://investor.synopsys.com/news/news-details/2026/Synopsys-Advances-Agentic-AI-Chip-Design-with-AMD-and-Microsoft/default.aspx)；[Siemens/NVIDIA，2026-07-26](https://news.siemens.com/en-us/siemens-nvidia-dac-2026/)；[DAC TechTalk speakers](https://dac.com/2026/program/2026-techtalks-speakers)；[PRO-V-R1](https://63dac.conference-program.com/presentation/?id=RESEARCH142&sess=sess163)；[NotSoTiny](https://63dac.conference-program.com/presentation/?id=RESEARCH2760&sess=sess166)。

### 为什么“求解器 18×”不等于“工程团队 18×”

**事实**：Synopsys 披露 PrimeSim SPICE 在 GPU 上墙钟时间约 18×、Lumerical FDTD 10×；NVIDIA 披露 Keysight 电磁仿真最高 10×、Samsung 计算光刻最高 20×、cuEST 关键量子化学工作负载最高 50×。这些是特定计算内核或 workload 的速度，不是完整项目周期。[NVIDIA Agent Toolkit，2026-07-26](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Expands-NVIDIA-Agent-Toolkit-With-NVIDIA-PhysicsNeMo-and-CUDA-X-Libraries-to-Transform-How-the-World-Engineers-Designs-and-Builds/default.aspx)

**估算框架**：若某求解步骤占完整设计周期的 20%，其加速 18×，按 Amdahl 定律，其他步骤不变时端到端上限约为 `1 / (80% + 20%/18) = 1.23×`。只有当 agent 同时减少排队、setup、debug、返工和人工交接，项目级生产率才会接近多倍改善。

**判断**：未来一年应优先要求厂商披露四类数据：同一设计前后的人时、端到端墙钟时间、最终 PPA/coverage/escape、以及新增 GPU/云成本。缺任一项，都不能把“up to”指标直接转成利润率或订单预测。

### 商业模式变化

1. **基础订阅仍是锚**：签核工具、仿真器、emulator 和 IP 库依旧按多年协议采购，agent 是扩大套件覆盖率和续约价格的入口。
2. **从 seat 向 workflow/outcome/usage 混合计价**：长时间 agent 会消耗模型 token、GPU solver、emulation hour 和云存储，适合用容量包、credit 或闭环任务计价。客户会要求成本上限和可重现性。
3. **私有部署成为价格层级**：RTL、PDK、波形和缺陷数据不可轻易进入公共云；on-prem、VPC、模型微调、访问控制、审计记录和数据驻留将成为高价企业功能。
4. **服务利润池重新分配**：重复脚本、报告和初级 debug 服务承压；流程迁移、知识图谱、模型治理、tool API、benchmark、signoff correlation 和企业集成服务上升。
5. **计算成本成为新 COGS**：传统 EDA 软件的高增量毛利可能被 GPU、模型推理和云编排部分稀释。能用小模型、缓存、确定性工具调用和 token-efficient agent 降本的厂商更有议价力。

### 竞争壁垒排序

| 壁垒 | 强度 | 原因 | 潜在破坏者 |
|---|---|---|---|
| Foundry PDK/PADK 认证与 golden signoff | 很高 | 错误成本是重流片，相关性需多年积累 | 晶圆厂自研平台、开放认证接口 |
| 跨工具设计图谱、状态和可追溯性 | 高 | agent 必须理解 spec—RTL—testplan—coverage—layout—signoff 因果链 | 客户内部数据平台、开放 ontology |
| 客户专有数据与反馈 | 高但不归厂商独占 | 最有价值数据由芯片公司掌握，需安全使用 | Hyperscaler/大型芯片公司自研 agent |
| 物理求解器与 GPU 优化 | 高 | 准确度、数值稳定性和规模化难复制 | NVIDIA 横向库、学术 surrogate、开源 solver |
| Agent orchestration/UI | 中低 | SDK、模型和 tool-calling 快速开放 | 开源模型、Microsoft/Google/NVIDIA 平台 |
| 通用 RTL/脚本生成 | 低至中 | 模型能力趋同，benchmark 易被污染 | 开源模型、内部 fine-tune、startup |

**判断**：EDA 龙头不会因为通用大模型而立即失去护城河，但“谁拥有用户界面”不再等于“谁捕获全部价值”。NVIDIA、Microsoft/Google 云和客户内部平台会争夺 orchestration 与计算层；EDA 龙头需要通过认证工具、数据闭环和 suite bundling 保持定价权。

## Chiplet、先进封装、硅光和 3D-IC 的新瓶颈

### 瓶颈—工具需求矩阵

| 环节 | 新瓶颈 | 需要的工具/标准 | 商业含义 |
|---|---|---|---|
| 架构切分 | 不同节点、IP、memory、I/O 如何分 die；NRE 与性能权衡 | Early floorplanning、架构探索、成本/良率模型、IP assembly、软件 workload co-design | Shift-left EDA 和设计服务受益；错误切分无法靠后端补救 |
| Die-to-die PHY | 64G 信号完整性、通道、bump map、功耗和延迟 | UCIe compliance、channel/package co-sim、IBIS/AMI/EM、协议验证 | PHY IP 有收入，但不是唯一瓶颈 |
| 3D 电热耦合 | TSV、背面供电、HBM、局部热点相互作用 | Concurrent PI/thermal/timing/stress、fast surrogate + golden solver | Multiphysics attach rate 上升，Synopsys/Cadence/Siemens 受益 |
| 热—机械可靠性 | warpage、CTE mismatch、疲劳、TIM、微凸点/混合键合应力 | Mechanical FEA、thermal cycling、材料数据库、digital twin、early screening | CAE/材料/量测价值提升；只做电设计的流程不足 |
| Known-good-die 与测试 | 封装后故障代价高、内部访问受限、mixed technology、repair/telemetry 不统一 | Wafer sort、DFT、boundary scan、UCIe UDA、BIST、probe、system-level test | 测试设备和 DFT 是高弹性利润池 |
| 数据与责任边界 | 各 die 供应商不愿公开完整模型；版本、许可、安全、保修不统一 | CDXML、3Dblox、machine-readable thermal/electrical/mechanical/test/security model、IP lifecycle | 开放 marketplace 的真正门槛，数据平台和治理受益 |
| 制造协同 | 设计规则、substrate routing、assembly window 和良率反馈滞后 | PADK、DFM、virtual process、yield analytics、design-to-fab digital thread | Foundry/OSAT 与 EDA 绑定更深，小型 point tool 承压 |
| 光电协同 | Maxwell 仿真昂贵，PIC/EIC/laser/fiber attach/thermal/yield 跨域 | EPDA、photonic PDK、inverse design、co-simulation、auto-layout、optical DFM/test | CPO 工具收入可先于大规模 CPO 组件收入 |
| 软件与 bring-up | 多 die firmware、telemetry、security、故障隔离和升级 | Virtual prototype、early firmware download、runtime health monitoring、system emulation | Automotive/edge 尤其需要，验证周期拉长 |

### UCIe：标准速度领先于生态速度

**事实**：UCIe 3.0 支持 48/64 GT/s，为 2.0 的 32 GT/s 两倍，并增加最长 100 mm sideband、early firmware download、priority packets、fast throttle/emergency shutdown 和运行时节能。UCIe 2.0 引入跨 chiplet 的 manageability/DFx，并为混合键合支持约 10–25 µm 到 1 µm 以下的 pitch。[UCIe Specifications，检索于 2026-08-18](https://www.uciexpress.org/specifications)

**事实**：2026 Chiplet Summit 展示 Intel/Cadence 独立设计的 chiplet 以 16G UCIe-S PHY 实现首个 live interoperability demo。[UCIe Consortium，2026-03-05](https://www.uciexpress.org/post/chiplet-summit-2026-ucie-momentum-across-a-growing-ecosystem)

**判断**：这证明“跨厂商 PHY 可以工作”，但尚未证明 64G、不同工艺/封装、长期可靠性、现场管理、完整 software stack 和商业责任可以同时工作。开放 chiplet 生态的关键里程碑应是 **具名量产系统中的跨厂商 32/64G chiplet**，不是又一次 booth demo。

### 模型交换和 marketplace

**事实**：OCP 的 CDXML 已定义电、机械、热、I/O、assembly 等机器可读交换基础，目标是跨工具、跨公司自动化设计与商业流程；OpenHBI 则定义与 HBM3 兼容、兼顾互操作/制造/测试的高带宽 die-to-die 接口。[OCP CDXML](https://www.opencompute.org/chiplets/31/chiplet-data-exchange-in-xml-format-cdxml)；[OCP OpenHBI](https://www.opencompute.org/chiplets/30/openhbi-specification)

**判断**：Marketplace 的约束不是目录网站，而是供应商愿意交付到何种精度的 thermal map、power state、failure rate、test coverage、security/firmware 和模型版本，并为模型偏差承担何种责任。短期更现实的是同一 hyperscaler、foundry 或 IP 联盟内部的受控 chiplet 组合，而非完全开放现货市场。

### 热设计：fast model 与 golden signoff 将共存

**事实**：DAC 2026 的 ACM TODAES Best Paper Award 论文 MFIT 在 16/36/64-chiplet 2.5D 和 16×3-chiplet 3D 系统上，将部分热仿真从数天降到秒或毫秒、同时报告可忽略精度损失；代码已开源。FLASH3D 论文相对 COMSOL 披露超过四个数量级加速、最大绝对误差低于 0.5 K；LightningFNO 在 4×4 光子 MVM 逆向设计相对 adjoint optimization 披露约 1,245,550×，并制作 3×3 原型、RMSE 0.043。[MFIT 论文](https://arxiv.org/abs/2410.09188)；[MFIT 代码](https://github.com/AlishKanani/MFIT)；[FLASH3D DAC 页面](https://63dac.conference-program.com/presentation/?id=RESEARCH1065&sess=sess314)；[LightningFNO DAC 页面](https://63dac.conference-program.com/presentation/?id=RESEARCH2358&sess=sess169)

**判断**：这些结果说明 early exploration 可获得数量级提速，但不能把 surrogate/analytical model 当作最终签核。DAC 的产业专题反而强调，在 chiplet/3D/HBM 的制造分辨率下，非确定性、近似误差和 workflow variability 本身可能成为 failure mode。最有价值的平台应自动选择保真度：早期用 fast model 扫描，关键点调用 deterministic golden solver，最后保留 traceable correlation。

### 测试为什么可能成为最大瓶颈

**事实**：DAC 专题 “Stacked, Packed, Fully Tested” 将有限物理访问、互连密度爆炸、mixed technology、KGD 和标准缺失列为主要障碍，并估计先进 multi-die package 的测试成本可能占总制造成本 30%–50%。该 session 有 AMD、TSMC 和学术界参与，但此比例仍是议程级产业估计，不是所有产品的统一平均值。[DAC 2026 完整议程](https://confcats-siteplex.s3.amazonaws.com/dac/images/dac-2026_program_july-22.pdf)

**判断**：当一套封装包含多个昂贵 compute die 和 HBM stack 时，后段才发现一个坏互连会损失整个 module。因而 tester throughput、probe accuracy、thermal stress、repair、system-level test 和失效定位的经济价值随 package BOM 非线性上升。测试设备 2026 年预期增速显著高于 assembly/packaging equipment，正是这一结构的外部验证。

### 硅光与 CPO：商用起点和工具缺口同时成立

**事实**：

- TSMC 于 2026-04-22 称 COUPE-on-substrate 真正 CPO 方案 2026 年开始生产，并给出相对板上可插拔方案 2× 能效、10× 延迟改善的公司指标。[TSMC 2026 Technology Symposium](https://pr.tsmc.com/english/news/3302)
- NVIDIA 于 2026-05-31 称 Spectrum-X Ethernet Photonics CPO 交换机已进入生产，CoreWeave、Lambda、OCI 为首批采用者；Vera Rubin 系统生产出货计划从 2026 年秋季开始。[NVIDIA Vera Rubin/CPO](https://nvidianews.nvidia.com/news/vera-rubin-full-production-agentic-ai-factory)
- DAC EPDA 专题仍将电子—光子 co-design/co-simulation、自动布局、验证、DFM、封装和 PDK/PCO 碎片化列为核心缺口，并讨论 100+ Tb/s DWDM CPO 的系统仿真、yield-aware inverse design 和 AIM Photonics 的制造/封装生态。[DAC 2026 完整议程](https://confcats-siteplex.s3.amazonaws.com/dac/images/dac-2026_program_july-22.pdf)

**判断**：两家公司的“生产”是明确里程碑，但一款垂直整合网络产品不能代表通用 CPO 市场成熟。未来 12 个月更可靠的量化指标是实际 shipment、端口数、field failure、激光/光纤装配良率、每 bit 功耗和客户复购，而不是 announced design win。

## 发布的商用成熟度：量产、部署、试用与概念展示

| 项目 | 材料日期 | 公开状态 | 成熟度结论 | 不应误读为 |
|---|---:|---|---|---|
| Cadence Cerebrus block-level AI | 页面检索 2026-08-18 | 1,000+ production designs、Samsung/ST 客户 | **已商用/量产采用** | 新一代全 SoC agent 已达到相同覆盖 |
| Synopsys Multiphysics Fusion 首批方案 | 2026-06-17 | available today；Cisco、MediaTek、NVIDIA、Samsung | **已可部署，具名早期采用** | 所有客户均达到 10× |
| Cadence AuraStack | 2026-07-16 | “will be available in 2026”；客户数据部分来自底层既有工具 | **路线图/部署合作** | AuraStack 整套已普遍 GA 并实现 15× |
| Synopsys 全自主 DV/CAE agent | 2026-07-26 | customers evaluating；H2 2026 planned availability | **评估/路线图** | 已形成广泛生产订单 |
| Synopsys + AMD + Microsoft workflows | 2026-07-27 | AMD actively evaluating；客户可申请 evaluation access | **具名试用** | AMD 已全面量产部署 |
| Siemens Fuse 新增 self-verifying 能力 | 2026-07-26 | forthcoming releases；ST plans to test | **演示/后续版本** | 已由 ST 验证节省数周 |
| Rapidus Raads + Cadence InnoStack | 2026-07-16 | target up to 2× TAT | **合作目标** | 已实现 2× 或已有量产客户 |
| Intel 14A + Synopsys flow/IP | 2026-07-27 | certified/expanding 14A support；18A/18A-P IP 更成熟 | **设计就绪/路线图** | 14A 已有公开量产 tapeout/订单 |
| UCIe Intel/Cadence 16G demo | 2026-03-05 | independently designed chiplets live interoperable | **实物验证** | 64G 多厂商产品已量产 |
| TSMC 5.5-reticle CoWoS | 2026-04-22 | in production | **量产** | 14-reticle 已量产；后者是 2028 路线图 |
| TSMC COUPE-on-substrate | 2026-04-22 | beginning production in 2026 | **生产导入** | 已形成大规模、可审计收入 |
| NVIDIA Spectrum-X Ethernet Photonics | 2026-05-31 | CPO switches “now in production”；系统秋季开始出货 | **生产/首批采用** | 当前已大规模交付 |
| Infineon 汽车 RISC-V AURIX | 2025-03-06；2026 虚拟平台推进 | within coming years，虚拟原型先行 | **路线图/生态建设** | 已有汽车量产 MCU 收入 |
| Bronco AI/ChipAgents/Architect Labs demos | DAC 2026 | vendor case/demo，数据集披露有限 | **概念到早期试用** | 可替代签核流程或具备广泛收入 |

## RISC-V、汽车与边缘芯片

### 事实

1. Qualcomm keynote 把 emerging AI 设计范围定义为低于 5W 的电池设备到最高约 500W 的云服务器，主张复用 CPU、GPU、AI accelerator、connectivity、security 等模块 IP，但指出当前 IP 适配和 SoC 集成仍高度依赖人工，chiplet 又增加 3DIC floorplan、package 和 thermal 工具需求。[Qualcomm keynote 页面](https://dac.com/2026/design-automation-for-emerging-ai-from-ai-pins-to-datacenter)
2. RISC-V International 的 ratified library 截至 2026 年已包含 RVA23、RVB23，以及 2026-05 的 Server Platform；汽车页面强调 RVA23/RVB23、未来 MCU profile、功能安全和供应链多源化，但标准组织本身不设计或销售 core。[RISC-V Ratified Specifications Library](https://docs.riscv.org/reference/home/index.html)；[RISC-V Automotive](https://riscv.org/industries/automotive/)
3. Infineon 已宣布未来数年推出 RISC-V AURIX 汽车 MCU 家族，并以虚拟原型让软件/工具伙伴在硬件前开发；这是一条明确产品路线图，但不是现有量产产品。[Infineon，2025-03-06](https://www.infineon.com/press-release/2025/infatv202503-067)
4. UCIe Automotive Working Group 于 2026-07-23 讨论 ADAS、central/zonal compute、功能安全、可靠性、成本和长生命周期需求；仍属于标准需求与生态协调阶段。[UCIe Webinars](https://www.uciexpress.org/webinars)
5. TSMC 称汽车 N3A 于 2026 年进入生产、已有 10+ 产品计划采用，并通过 N2P “Auto-Use” PDK 提前启动 N2A 设计；N2A 计划 2028 年完成 AEC-Q100 qualification。[TSMC，2026-04-22](https://pr.tsmc.com/english/news/3302)

### 估算与判断

- **未来三个月**：RISC-V 对 EDA 收入的主要影响是更多 virtual prototype、compiler/debug、formal/fuzzing、安全和功能安全验证，不是 royalty 大迁移。
- **未来一年**：若 Infineon 和 Quintauris 等生态按期提供稳定 profile、toolchain 和 safety artifacts，RISC-V 会增加汽车 MCU 设计数量并压低专有 ISA/IP 的议价；但多架构并存会先增加验证支出。
- **未来两年**：RISC-V 的最大机会在 zonal controller、专用 accelerator、管理/安全 core 和可定制 edge AI，而不是立即替代所有 central compute。具名样片、AEC-Q/ASIL 证据、AUTOSAR/Linux 软件可移植性和 OEM 平台定点才是投资级里程碑。

**反向影响**：开放 ISA 有利于定制芯片和 EDA workload 数量，却可能压低通用 CPU core royalty；Arm 等专有 IP 供应商的防守点会转向完整 compute subsystem、软件生态、验证和快速 tapeout，而不是仅靠 ISA 许可。

## 技术路线与未来一年三情景

### 情景定义

| 情景 | AI-EDA | Chiplet/封装 | CPO/光子 | 宏观与资本开支 |
|---|---|---|---|---|
| 熊市 | 安全、正确率和成本阻碍 agent 扩展；H2 产品延期 | HBM/CoWoS 约束缓解但客户延后项目；多厂商互操作继续停留 demo | 秋季出货延迟，pluggable 继续延寿 | AI capex 下修、设备订单削减，价格竞争加剧 |
| 基准 | 新 agent 作为现有 suite 附加模块，验证/实现/多物理场率先落地 | 5.5-reticle CoWoS 与 HBM 扩产；32G UCIe 产品增加，64G 仍在验证 | 首批网络 CPO 出货，光子封装/测试先增长 | TSMC/SEMI 路线大体兑现，EDA 维持双位数附近增长 |
| 牛市 | 多个具名量产项目证明闭环、覆盖和 PPA，usage pricing 成功 | 64G 跨厂商产品、hybrid bonding、KGD/repair 标准快速成熟 | CPO 在 scale-out 与 scale-up 同时放量 | AI/HBM capex 再上修，测试与封装设备供给受限 |

## 市场规模和利润池：当前基线与未来一年三情景预测

> **单位：十亿美元。** “当前/2026E”混合使用最新实际年化与协会/分析机构 2026 预测，性质在“口径”列注明。子市场存在包含关系，**不可把各行相加**。三情景为本报告估算，不是来源机构预测。

| 市场/利润池 | 当前或 2026E | 熊市：未来一年 | 基准：未来一年 | 牛市：未来一年 | 口径、材料日期和计算 |
|---|---:|---:|---:|---:|---|
| ESD 总市场（EDA+SIP+服务） | 23.0 | 24.4（+6%） | 25.5（+11%） | 26.7（+16%） | SEMI 2026Q1 57.478 亿美元 ×4 年化；实际季度年化，不是官方全年预测 |
| EDA 工具（CAE+IC physical/verification+PCB/MCM） | 12.8 | 13.4（+5%） | 14.0（+10%） | 14.7（+15%） | SEMI 2026Q1 三类别合计 31.889 亿美元 ×4 |
| Semiconductor IP（SIP） | 9.3 | 10.0（+7%） | 10.6（+14%） | 11.2（+20%） | SEMI 2026Q1 23.325 亿美元 ×4；Q1 同比 +14.1% |
| 广义 advanced packaging | 55.3 | 58.6（+6%） | 60.8（+10%） | 64.1（+16%） | Yole/SEMI：2024 461 亿→2030 794 亿；按隐含 CAGR 约 9.5% 插值 2026 |
| 高端 2.5D/3D performance packaging（广义市场子集） | 12.2 | 13.7（+12%） | 15.0（+23%） | 16.1（+32%） | Yole/SEMI 2025 deck：2024 80 亿→2030 285 亿、CAGR 23%；插值 2026 |
| Semiconductor test equipment | 15.3 | 16.5（+8%） | 18.1（+18%） | 19.6（+28%） | SEMI 2026 官方预测；2026 同比 +31%，2028 208 亿 |
| Assembly & packaging equipment | 6.7 | 7.0（+5%） | 7.6（+13%） | 8.2（+22%） | SEMI 2026 官方预测；2026 同比 +9.6%，2028 86 亿 |
| Photonics packaging（含 transceiver、CPO 等） | 4.5 | 5.0（+12%） | 5.5（+22%） | 5.9（+32%） | Yole 经 optics.org，2026-04 称当前约 45 亿、2031 144 亿；CPO 目前接近零起点 |

来源与计算说明：

- SEMI EDMD 于 2026-07-13 公布 2026Q1 ESD 收入 57.478 亿美元，同比 +12.7%；CAE 20.184 亿、IC physical design/verification 7.513 亿、PCB/MCM 4.192 亿、SIP 23.325 亿、services 2.264 亿。[SEMI Q1 2026 EDMD](https://www.semi.org/jp/news-resources/press/20260714)
- 2025Q4 ESD 总收入 54.663 亿美元，同比 +10.3%；SIP +18.3%，而 IC physical design/verification -2.6%，显示增长并非所有传统类别均匀。[SEMI Q4 2025 EDMD，2026-04-13](https://www.semi.org/en/semi-press-release/esd-alliance-reports-electronic-system-design-industry-posts-5.5-billion-dollars-in-revenue-in-q4-2025)
- Advanced packaging 使用 Yole 在 SEMI 会议公开的 2024/2030 端点；本报告用 `46.1 × (79.4/46.1)^(2/6)` 得到 2026 插值 55.3。[SEMI，2025-12-16](https://www.semi.org/eu/technology-trends/topic/advanced-packaging)
- 高端封装使用 Yole/SEMI deck 的 2024 80 亿、2030 285 亿和 23% CAGR；本报告插值得 2026 122 亿。[Yole/SEMI 3D & Systems Summit 2025](https://www.semi.org/sites/semi.org/files/2025-06/21_Vishal%20Saroha.pdf)
- Photonics packaging 是连接 photonic device 与外界的封装价值，当前主要仍为可插拔 transceiver；它不等于纯 CPO 市场。[optics.org 转述 Yole，2026-04-08](https://optics.org/news/photonics-packaging-market-to-triple-in-value-by-2031)

### 利润池质量，而非仅看市场规模

| 利润池 | 收入质量 | 资本强度 | 竞争结构 | 本报告判断 |
|---|---|---|---|---|
| EDA signoff/verification/multiphysics | 高经常性、切换成本高 | 低至中，AI 后算力成本上升 | 三大平台主导 | **高质量、最先兑现 AI 溢价** |
| SIP/接口 IP | 许可+royalty，设计复用强 | 中，需持续节点认证 | 集中但受 RISC-V/open IP 影响 | **增长快，接口/内存/chiplet IP 优于通用 core** |
| Foundry 内部高端封装 | 稀缺容量、与先进节点/HBM绑定 | 很高 | TSMC/Samsung/Intel 为主 | **收入与议价强，但折旧、良率和客户集中风险高** |
| OSAT advanced packaging | 量大、客户多元 | 高 | ASE/Amkor/JCET 等竞争 | **受益外溢，利润率低于稀缺高端平台且需防 foundry 内制** |
| 测试、量测、失效分析 | 与复杂度、价值 at risk 同增 | 中高 | 技术/客户认证壁垒高 | **被低估；增速可能高于封装设备** |
| CPO/光子封装 | 当前低基数，未来高增长 | 高，装配/良率/可靠性难 | 生态未定型 | **工具和精密封装先受益，纯 CPO 收入波动最大** |
| GPU/云计算层 | 用量随 agent 与 solver 增长 | 很高 | NVIDIA/云平台集中 | **横向受益，但会分走 EDA 新增价值** |

### 外部资本开支基线

**事实（SEMI，2026-07-14）**：2026 年全球半导体设备销售预计 1,659 亿美元、同比 +23.2%；WFE 1,439 亿、同比 +23.1%；foundry/logic WFE 780 亿、同比 +18.9%；DRAM 388 亿、同比 +39%；测试设备 153 亿、同比 +31%；assembly/packaging equipment 67 亿、同比 +9.6%。2028 年总设备预计 2,295 亿、测试 208 亿、assembly/packaging 86 亿。[SEMI Mid-Year Equipment Forecast](https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-dollars-in-2028-semi-reports)

**事实（TSMC，2026Q2，2026-07-16）**：Q2 收入 402 亿美元、毛利率 67.7%、营业利润率 60.3%；Q3 指引 446–458 亿美元。公司把 2026 年资本预算提高到 600–640 亿美元，约 70%–80% 用于先进工艺、约 10% 用于 specialty、约 10%–20% 用于先进封装、测试、光罩及其他；最后一项对应约 60–128 亿美元，但**不能把整个区间当作先进封装支出**。[TSMC 2026Q2 官方结果及 transcript 入口](https://investor.tsmc.com/english/quarterly-results/2026/q2)

**判断**：EDA 是 AI capex 的小额但必需税收；测试/多物理场是复杂度税收；先进封装是容量税收。三者都受益于 AI，但周期和利润率不同。若前端 WFE 增长而测试/封装订单不跟随，说明系统瓶颈叙事被高估或库存正在累积。

## 三个月、一年和两年影响

### 未来三个月：2026-08-18 至 2026-11-18

**事实可观察项**：Synopsys H2 2026 agentic EDA/CAE availability、NVIDIA Vera Rubin/CPO 秋季 shipments、Siemens forthcoming Fuse releases、Cadence AuraStack 2026 availability、Precision Innovations 交易预计 Q3 完成。

**判断**：

- EDA 厂商会优先把 agent 作为现有 enterprise agreement 的 pilot、credit 或 premium module，而非立即改变全公司定价。
- 客户采购关注 security review、on-prem/VPC、tool permissions、reproducibility、token/GPU 成本和责任归属；因此销售周期可能长于 demo 周期。
- 最直接的收入来自 solver capacity、cloud/emulation usage、consulting/integration 和已有多物理场产品，而非无人值守 tapeout。
- 封装和测试设备的订单/交付仍受 HBM、CoWoS 和先进逻辑扩产支撑；需监测 lead time 是否从紧缺转为库存。

### 未来一年：至 2027-08-18

**基准判断**：

1. ESD 总市场约 255 亿美元，SIP 增长快于纯 physical design 类别；AI agent 通过 suite attach 和用量计费贡献，而非公开拆分为独立大市场。
2. 验证将是 agent 最大落地场景，因为其占设计周期高、反馈可由 simulator/formal/coverage 自动判定；layout、thermal 和 package routing 次之。
3. 多物理场分析从 signoff 后置环节前移，Synopsys/Ansys 协同、Cadence 系统分析并购资产、Siemens digital twin/Innovator3D 将争夺同一预算。
4. 先进封装收入基准约增 10%，高端 2.5D/3D 子市场约增 23%；test equipment 增速可能继续高于 assembly tool。
5. UCIe 的关键不是再发布一版规格，而是 32/64G compliance、cross-vendor production silicon、field manageability 和可交换模型。
6. CPO 将由首批生产转入客户验证和有限规模部署，光子封装/测试/仿真供应链比广义网络设备更早确认收入。

### 未来两年：至 2028-08-18

**基准判断**：

- TSMC 14-reticle CoWoS、A14、N2A 汽车资格、更多 hybrid bonding 和 3D stacking 把设计对象从 chip 推向 system-in-package；若按期，package-aware EDA 和 DFT 的 TAM 会结构性上移。
- SEMI 对 2028 年设备 2,295 亿美元、测试 208 亿、封装设备 86 亿的预测意味着 back-end 仍增长，但测试弹性更高。
- 64G UCIe 可望进入真实产品，开放 chiplet 仍更可能先在受控联盟内形成，而不是完全通用市场。
- CPO 若解决光源、fiber attach、thermal、repair 和 field reliability，将从交换芯片扩展到 scale-up/compute I/O；若未解决，可插拔/NPO 会延长主导期。
- AI 将减少每个设计点的人工作业，但同时增加探索点和验证场景；EDA 收入可能与工程师人数脱钩，按 compute/outcome 增长。

## 反共识洞见

### 1. AI 不会先减少验证预算，反而会扩大验证预算

生成的 RTL、testbench 和 constraint 越多，需要证明其正确的状态空间越大。PRO-V-R1 的绝对 fault-detection rate 和 NotSoTiny 的现实任务难度表明，生成能力提升并未消除验证缺口。短期赢家不是最会“写 Verilog”的模型，而是能把 specification、assertion、simulation、formal、coverage、waveform 和 revision history 连成可审计闭环的平台。

### 2. Chiplet 的超额利润不一定主要留在封装代工

封装收入规模最大，但资本密集且良率风险高；测试、量测、DFT、thermal/EM solver、substrate routing 和模型治理可用更轻资产方式对每个复杂 package 收费。SEMI 的 test equipment 增速与 DAC 的测试成本讨论都支持这一点。

### 3. 开放标准会先增加 EDA 工作量，再降低集成成本

UCIe/CDXML 让更多供应商能够参与，但每增加一个可替换 die，就增加更多 version、model、security、DFx、firmware 和 corner 组合。开放生态成熟前，验证组合数和治理成本上升；成熟后才体现复用和议价优势。

### 4. CPO 的第一波利润可能属于“让它可制造”的公司

光学引擎 headline 最高，但早期最稀缺的是 photonic/electronic co-design、EM/FDTD、精密贴装、fiber attach、thermal、test 和良率学习。NVIDIA/TSMC 的垂直整合产品可以先生产，通用生态仍需工具链。因此 EDA、制造设备和高精度封装的风险收益可能优于单押纯 CPO 组件量。

### 5. 开源 agent 会削弱界面壁垒，却可能强化 signoff 龙头

OpenROAD、开源模型和通用 SDK 会降低脚本/编排门槛，使客户可以自建 agent；但 agent 要得到可信结果，仍会调用经认证的 Calibre、PrimeTime/RedHawk、Cadence signoff 等引擎。界面价值被压低，工具调用量反而上升。

### 6. RISC-V 对 Arm 的近期威胁主要是议价，不是销量替代

汽车平台需要十年以上生命周期、ASIL/AEC-Q、软件兼容和供应保障。虚拟原型和标准 profile 会让 OEM 更有多源选择，从而压低专有 ISA 的议价；但量产切换速度受安全认证和软件资产约束。短期更确定的是 EDA/验证工作量增加。

### 7. 会场热度不能替代订单验证

2026 官方主题占比、投稿和 AI-first 展商很强，但 120+ exhibitors 并不高于 2025 页面约 130 的口径，且 2026 最终 attendance 尚未发布。会议密度证明研发方向，不证明预算已经同比同幅增长。财报、RPO/backlog、GA 日期和具名生产客户才是收入证据。

## 公司及产业链映射

> 下表是产业暴露映射，不是买卖建议。Ticker 仅用于识别；公司基本面、估值和股价需另行更新。直接证据以 2026-08-18 前公开材料为限。

### 直接 EDA、IP 与计算平台

| 公司 | 代码 | DAC/产业证据 | 受益逻辑 | 风险/证伪 |
|---|---|---|---|---|
| Synopsys | SNPS | AgentEngineer、Multiphysics Fusion、Ansys、Intel 14A、AMD/Microsoft 试用 | EDA+IP+golden multiphysics 一体化，最能把 3DIC/AI 转为 suite attach | H2 agent 延期；Ansys 整合/渠道成本；客户指标停留 pilot |
| Cadence | CDNS | Cerebrus 1,000+ production designs；AuraStack；TSMC substrate、NVIDIA、HELLA 具名数据 | 从 silicon 扩到 package/PCB/mechanical；客户证据当前最丰富 | 新 super-agent 把既有工具成绩重复计入；GPU/并购成本；价格兑现不足 |
| Siemens | SIE.DE / SIEGY | Fuse、Calibre、Questa、Innovator3D；收购 Precision Innovations/Defacto | 验证、DFT、signoff、3DIC 与工业 digital twin/制造链结合 | 新能力多为 forthcoming；EDA 对集团利润贡献被稀释；并购整合 |
| NVIDIA | NVDA | Nemotron、Agent Toolkit、OpenShell、CUDA-X solver；三大 EDA 厂商采用 | 捕获模型、GPU、solver 和 runtime 的横向计算需求 | EDA 厂商/客户多云或自研以降低依赖；推理 ROI 不足 |
| Microsoft | MSFT | Discovery 上首批 Synopsys EDA workflow，AMD 评估 | Azure/Discovery 成为工程 agent 编排和计算平台 | 设计数据不愿上云；客户偏 on-prem；EDA 厂商保持中立 |
| Silvaco | SVCO | NVIDIA 披露 32 GPU 完成 32 亿 mesh-node photonic edge-coupler 仿真 | 小型 EDA/TCAD 在 photonics、device simulation 获 GPU 杠杆 | 规模、客户集中、与大平台竞争；benchmark 未必转收入 |
| Arm | ARM | Chiplet/edge/automotive compute subsystem 暴露 | 模块 IP、软件生态、快速集成仍有价值 | RISC-V 多源化压低 royalty/议价；客户自研 core |
| Rambus | RMBS | HBM/PCIe/CXL/安全与 chiplet 接口相关 IP | 高速 memory/interface 验证和 IP 需求 | 大客户内制、标准 IP 价格竞争、设计周期波动 |
| Qualcomm | QCOM | DAC keynote 明确端—云共同模块 IP 与 3DIC 工具缺口 | Edge AI、汽车、连接和自有 IP 复用带来设计效率 | 终端需求、定制 NRE、跨产品复用低于预期 |

**财务交叉验证**：Cadence 2026Q2 收入 15.84 亿美元、core EDA 同比 +18%、期末 backlog 81 亿、non-GAAP operating margin 45.5%，并把 2026 收入增长指引上调至 19%；这支持 AI/系统设计需求已经进入财务数据，但并未单列 agentic AI 收入。[Cadence 2026Q2，2026-07-27](https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx)

### Foundry、先进封装与设计服务

| 公司 | 代码 | 暴露 | 受益 | 主要风险 |
|---|---|---|---|---|
| TSMC | TSM / 2330.TW | CoWoS、SoIC、COUPE、3DFabric、先进节点 | 稀缺高端封装与晶圆制造协同，能定义 PADK/生态 | 高 capex、客户集中、地缘、海外成本、良率/供给执行 |
| Intel | INTC | EMIB/Foveros、UCIe、14A、system foundry | 标准与异构集成资产深，若外部客户采用有估值弹性 | 14A/Foundry 客户和量产证据不足；资本强度 |
| Samsung Electronics | 005930.KS | HBM、2nm、3DIC、hybrid bonding；Cadence/Synopsys 认证 | memory+foundry+package 垂直整合 | HBM/先进节点良率、外部客户、认证不等于 tapeout |
| ASE Technology | ASX / 3711.TW | 高端 OSAT、VIPack、CPO/2.5D/3D | Foundry 产能外溢、系统级 assembly/test | TSMC/Samsung 内制、资本强度、mix/价格竞争 |
| Amkor | AMKR | 先进 SiP、2.5D/3D、汽车封装 | 客户多元、美国/区域化供应链 | 高端能力与量产规模追赶、利用率、客户集中 |
| GUC / Alchip | 3443.TW / 3661.TW | ASIC design service、先进封装协同 | Hyperscaler 定制 silicon 和 chiplet NRE | 客户集中、EDA/IP/CoWoS 成本、项目 timing |

### 设备、测试、量测和光子链

| 公司 | 代码 | 暴露 | 本报告判断 | 证伪 |
|---|---|---|---|---|
| Advantest | 6857.T | SoC/HBM test | **直接受益且可能被低估**：测试复杂度、并行度和时长上升 | Tester utilization/订单下滑，测试时间快速下降 |
| Teradyne | TER | SoC test、system test | AI accelerator、chiplet KGD/系统测试受益 | 市占、客户 capex、产品 mix 不及预期 |
| KLA | KLAC | inspection、metrology、process control | Hybrid bonding、微凸点、先进封装良率需要更多量测 | 缺陷密度改善快于预期、封装 capex 下修 |
| Onto Innovation | ONTO | advanced packaging inspection/metrology | RDL、bump、panel/wafer-level package 增量 | 订单集中、竞争、项目延后 |
| BE Semiconductor | BESI.AS | hybrid bonding、die attach | 3D stacking 和混合键合放量的高弹性标的 | 量产节奏延后、客户集中、替代工艺 |
| ASMPT | 0522.HK | TCB、die bonding、先进封装装配 | HBM/2.5D/3D 装配量增长 | 周期、价格、客户内制和中国设备竞争 |
| Keysight | KEYS | high-speed I/O、EM、channel、protocol validation | 64G UCIe/CPO/RF/SerDes 需要更强仿真和测试 | 标准进度慢、客户整合工具、设备预算下修 |
| Broadcom | AVGO | switch ASIC、CPO、SerDes | 规模网络 silicon 与 CPO 先发 | NVIDIA 垂直栈、客户自研、pluggable 延寿 |
| Marvell | MRVL | optical/DSP、custom silicon、chiplet | AI interconnect、CPO/optics 和定制 ASIC | 客户集中、竞争、CPO 节奏 |
| Coherent / Lumentum | COHR / LITE | laser、optical component、photonics | CPO/光子封装增加高性能光源和耦合需求 | 光源架构变化、价格下降、良率/客户认证 |
| Fabrinet | FN | 精密 optical manufacturing/packaging | 光子封装复杂度和外包制造受益 | 大客户集中、垂直整合、产能/良率 |

### 受益、受损、过度乐观与被低估方向

**受益方向**：

- Golden signoff、多物理场、verification/emulation、agent governance、GPU solver。
- HBM/CoWoS/SoIC 的设计—封装—测试协同。
- Tester、DFT、inspection/metrology、失效分析、thermal/mechanical simulation。
- UCIe/HBM/PCIe/CXL/SerDes 等已标准化且需节点认证的接口 IP。
- Photonics packaging、fiber attach、optical/EM/thermal co-design 与测试。

**潜在受损方向**：

- 依靠手工脚本、报告和低端 debug 的设计服务。
- 没有 PDK/signoff/客户数据的单点通用 AI-EDA 工具。
- 长期看，若 CPO 放量，部分可插拔光模块、front-panel optics 和相关 DSP/connector 价值承压；但时间可能晚于市场预期。
- 专有 CPU ISA/IP 的议价在 RISC-V 多源化下承压，但完整 subsystem 和软件生态可缓冲。

**过度乐观方向**：

1. 2027 年前完全 autonomous tapeout 成为主流。
2. 把所有“up to 50×/100×”直接转为项目人力下降和 EDA 毛利提升。
3. UCIe 3.0 发布即等于开放 chiplet marketplace 成熟。
4. CPO 在两年内全面取代 pluggable optics。
5. 所有 OSAT/封装设备公司同比例分享 CoWoS/HBM 利润。

**被低估方向**：

1. 测试访问、KGD、repair/telemetry 和 system-level test。
2. Thermal-mechanical-electrical co-design、early high-fidelity model 和 solver correlation。
3. Machine-readable chiplet model、IP lifecycle、版本/许可/安全治理。
4. Secure on-prem agent runtime、audit trail、benchmark 和 mutation/formal evaluation。
5. Substrate/PCB 自动化和 silicon-package-board 的 continuous signoff。

## 风险、证伪指标与后续跟踪

### 主要风险

1. **证据风险**：大部分生产率数字由供应商发布，常用“up to”，设计规模、基线和失败样本未公开。
2. **安全与责任风险**：agent 修改 RTL、constraint 或 signoff setup 后，错误责任仍需人承担；访问控制和审计缺失会阻止量产使用。
3. **经济性风险**：GPU、token、仿真和 storage 用量可能大于节省的人力，尤其在无限探索或 agent loop 失控时。
4. **数据壁垒风险**：客户拥有最优训练/反馈数据，不愿跨项目或跨云共享；vendor learning flywheel 可能弱于软件行业常规模型。
5. **封装良率风险**：更大 package、更多 HBM 和更细 pitch 会提高价值 at risk；收入增长不一定等于利润增长。
6. **Capex 周期风险**：SEMI/TSMC 当前预测非常强，任何 hyperscaler 项目延后都会沿 HBM、foundry、test、package equipment 放大。
7. **标准碎片风险**：UCIe、OpenHBI、proprietary die-to-die、不同 foundry model 并存，互操作和许可可能长期受限。
8. **CPO 可靠性风险**：光源、耦合、热、维修和 field service 若不达标，pluggable/NPO 会延寿。
9. **地缘与出口控制**：先进 EDA、GPU、设备、foundry 和 IP 均受政策影响，区域化会增加重复 capex，也会限制可服务市场。

### 跟踪仪表盘

| 主题 | 未来数据点 | 基准情景确认 | 证伪/转熊阈值 |
|---|---|---|---|
| Agent 产品可用性 | Synopsys H2、Cadence AuraStack、Siemens Fuse release notes | 2026 年内 GA/limited GA，2027Q1 出现新增具名生产客户 | 连续两个季度延迟，或只有 demo 无 production reference |
| AI 生产率 | 同设计人时、墙钟、coverage/PPA、GPU/token 成本 | 至少 3 个具名客户披露端到端净收益 | 速度提高但 coverage/PPA/成本恶化，或大量人工返工 |
| EDA 变现 | CDNS/SNPS backlog、RPO、AI attach/usage、margin | EDMD 未来四季约 10%–12% 增长，margin 稳定 | EDMD 连续两季 <6%，AI COGS 压低增量利润 |
| Multiphysics | Fusion/AuraStack/Fuse 具名 tapeout/package | 从 pilot 扩到多客户 signoff，减少 late ECO/respins | 只用于可视化或 early screening，最终流程仍割裂 |
| UCIe | 32/64G compliance、跨厂商 production silicon | 2027 年出现具名量产系统和 field manageability | 仍只有 16G booth demo；供应商只支持自家 die |
| CoWoS/3DIC | 5.5-reticle 利用率/良率、14-reticle 工程样品 | 2028 路线按期，HBM/thermal/test 同步扩容 | 路线滑动 >2 个季度或 package margin/良率显著恶化 |
| Test/设备 | Advantest/Teradyne/KLA/ONTO/BESI/ASMPT 订单和 lead time | 测试订单增速高于 assembly，book-to-bill 健康 | 测试设备预测大幅下修、客户库存上升 |
| CPO | Spectrum-X 实际 shipment、端口、功耗、field reliability | 2026 秋出货、2027 有复购和第二批客户 | 出货延期、现场故障、每 bit 成本无优势 |
| RISC-V 汽车 | Infineon 样片、profile、ASIL/AEC-Q、OEM/Tier-1 design win | 2027 前出现具名样片/工具链/客户项目 | 仍停留虚拟原型，无认证或软件兼容进展 |
| Capex | TSMC 600–640 亿预算、SEMI 设备预测、HBM capacity | 预算维持或上修，back-end share 稳定 | 全年 capex 下修 >10% 或先进封装利用率下降 |

### 建议的后续更新时间点

- **2026-09 至 2026-11**：核验 Synopsys/Cadence/Siemens 正式 availability、NVIDIA CPO shipment、Precision Innovations 交易完成。
- **每季**：SEMI EDMD、TSMC capex/先进封装评论、Cadence/Synopsys backlog/RPO、主要测试与封装设备订单。
- **2027H1**：寻找 32/64G UCIe 跨厂商量产、具名 AI-agent tapeout、CPO 复购和 field reliability。
- **2027H2–2028**：14-reticle CoWoS、hybrid bonding 量产、汽车 RISC-V 样片/AEC-Q/ASIL、开放 chiplet 模型和商业责任标准。

## 来源清单

### DAC 官方、议程与 2025 对照

1. [DAC 2026 官网](https://dac.com/2026)，会议官方，检索于 2026-08-18，A1（日期、地点、keynote、投稿/主题快照）。
2. [The 2026 DAC Comes to Long Beach with Record Growth](https://dac.com/2026/press-release/the-2026-dac-chips-to-systems-conference-comes-to-long-beach-for-the-first-time-with-record-growth-as-ai-reshapes-chip-and-system-design)，会议官方新闻稿，2026-05-04，A1。
3. [DAC 2026 Full Program PDF](https://confcats-siteplex.s3.amazonaws.com/dac/images/dac-2026_program_july-22.pdf)，会议官方完整议程，2026-07-22 版本，A1/B（session 描述与论文摘要）。
4. [DAC 2026 Research Topics](https://dac.com/2026/research-topics)，会议官方，检索于 2026-08-18，A1。
5. [DAC 2026 TechTalk Speakers](https://dac.com/2026/program/2026-techtalks-speakers)，会议官方/厂商演讲，检索于 2026-08-18，B。
6. [Design Automation for Emerging AI: From AI Pins to Datacenter](https://dac.com/2026/design-automation-for-emerging-ai-from-ai-pins-to-datacenter)，Qualcomm keynote 摘要，2026，A2。
7. [DAC 2026 Media Center](https://dac.com/2026/media-center)，会议官方，会后视频入口，检索于 2026-08-18，A1。
8. [AI Reshapes the Future at DAC 2025](https://archive.dac.com/media-center/dac-press-releases/ai-reshapes-the-future-at-dac-2025-a-breakthrough-year-for-innovation.html)，DAC 官方会后新闻稿，2025-07-15，A1。
9. [DAC 2025: AI, Chiplets, and Sustainable Innovation](https://archive.dac.com/media-center/dac-blog/dac-2025-navigating-the-intersection-of-ai-chiplets-and-sustainable-innovation.html)，DAC 官方会前博客，2025，A2。

### EDA、AI、客户与产品

10. [Synopsys Autonomous Engineering Workflows at DAC](https://news.synopsys.com/2026-07-26-Synopsys-Showcases-Comprehensive-Autonomous-Engineering-Workflows-from-Silicon-to-Systems%2C-Developed-with-NVIDIA-Technology)，厂商官方，2026-07-26，A2/B。
11. [Synopsys Advances Agentic AI with AMD and Microsoft](https://investor.synopsys.com/news/news-details/2026/Synopsys-Advances-Agentic-AI-Chip-Design-with-AMD-and-Microsoft/default.aspx)，厂商/具名客户，2026-07-27，A2。
12. [Synopsys Multiphysics Fusion Availability](https://news.synopsys.com/2026-06-17-Synopsys-Announces-Availability-of-the-First-Wave-of-Multiphysics-Fusion-Solutions)，厂商/具名客户，2026-06-17，A2。
13. [Synopsys Converge 2026](https://news.synopsys.com/2026-03-11-Synopsys-Outlines-Vision-for-Engineering-the-Future)，厂商官方，2026-03-11，A2。
14. [Synopsys and Intel Foundry on Intel 14A](https://news.synopsys.com/2026-07-27-Synopsys-and-Intel-Foundry-Fast-Track-Customer-Readiness-from-Silicon-to-Systems-on-Intel-14A)，厂商/晶圆厂合作，2026-07-27，A2。
15. [Cadence Cerebrus AI Studio](https://www.cadence.com/en_US/home/tools/digital-design-and-signoff/soc-implementation-and-floorplanning/cadence-cerebrus-ai-studio.html/)，产品与客户页面，检索于 2026-08-18，A2。
16. [Cadence AuraStack](https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-introduces-aurastack-ai-super-agent-the-worlds-first.html)，厂商/具名客户，2026-07-16，A2/B。
17. [Rapidus and Cadence Agentic AI Collaboration](https://newsroom.cadence.com/press-releases/press-release-details/2026/Rapidus-and-Cadence-Partner-on-Agentic-AI-for-Advanced-SoC-Design/default.aspx)，厂商合作，2026-07-16，A2/B。
18. [Cadence and Samsung 2nm/3DIC Collaboration](https://www.cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-and-samsung-foundry-deepen-2nm-and-3dic-collaboration-to.html)，厂商/晶圆厂，2026-05-28，A2。
19. [Cadence 2026Q2 Results](https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx)，公司财报，2026-07-27，A1。
20. [Siemens Self-Verifying Agentic AI Workflows](https://news.siemens.com/en-us/siemens-nvidia-dac-2026/)，厂商/具名客户，2026-07-26，A2/B。
21. [Siemens to Acquire Precision Innovations](https://news.siemens.com/en-us/siemens-to-acquire-precision-innovations/)，公司官方，2026-07-20，A1/A2。
22. [Siemens to Acquire Defacto Technologies](https://news.siemens.com/fr-fr/siemens-to-acquire-defacto-technologies/)，公司官方，2026-07-21，A1/A2。
23. [NVIDIA Agent Toolkit for Engineering](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Expands-NVIDIA-Agent-Toolkit-With-NVIDIA-PhysicsNeMo-and-CUDA-X-Libraries-to-Transform-How-the-World-Engineers-Designs-and-Builds/default.aspx)，公司/合作伙伴官方，2026-07-26，A2/B。
24. [NVIDIA and TSMC Bring AI Into Fabs](https://nvidianews.nvidia.com/news/nvidia-and-tsmc-bring-ai-into-fabs-to-advance-semiconductor-design-and-manufacturing)，公司/晶圆厂合作，2026-05-31，A2。

### Chiplet、封装、光子、标准与汽车

25. [UCIe Specifications 1.0–3.0](https://www.uciexpress.org/specifications)，标准组织，检索于 2026-08-18，A1。
26. [UCIe Chiplet Summit 2026 Interoperability Demo](https://www.uciexpress.org/post/chiplet-summit-2026-ucie-momentum-across-a-growing-ecosystem)，标准组织，2026-03-05，A2。
27. [UCIe Automotive and Technical Webinars](https://www.uciexpress.org/webinars)，标准组织，2026-07-23 等，A1/A2。
28. [OCP Chiplet Data Exchange in XML Format](https://www.opencompute.org/chiplets/31/chiplet-data-exchange-in-xml-format-cdxml)，开放标准，检索于 2026-08-18，A1。
29. [OCP OpenHBI Specification](https://www.opencompute.org/chiplets/30/openhbi-specification)，开放标准，检索于 2026-08-18，A1。
30. [TSMC 2026 North America Technology Symposium](https://pr.tsmc.com/english/news/3302)，晶圆厂官方，2026-04-22/23，A1/A2。
31. [TSMC 2026Q2 Results and Transcript](https://investor.tsmc.com/english/quarterly-results/2026/q2)，公司财报，2026-07-16，A1。
32. [TSMC 3DFabric Alliance](https://www.tsmc.com/english/dedicatedFoundry/oip/3dfabric_alliance)，晶圆厂生态页面，检索于 2026-08-18，A1。
33. [TSMC 3Dblox Introduction](https://www.tsmc.com/english/news-events/blog-article-20221108)，晶圆厂官方，2022-11-08，A1/A2。
34. [NVIDIA Vera Rubin and Spectrum-X Ethernet Photonics](https://nvidianews.nvidia.com/news/vera-rubin-full-production-agentic-ai-factory)，公司官方，2026-05-31，A2。
35. [RISC-V Ratified Specifications Library](https://docs.riscv.org/reference/home/index.html)，标准组织，检索于 2026-08-18，A1。
36. [RISC-V Automotive Hub](https://riscv.org/industries/automotive/)，标准组织/产业推广，检索于 2026-08-18，A2。
37. [Infineon Automotive RISC-V AURIX Roadmap](https://www.infineon.com/press-release/2025/infatv202503-067)，公司官方，2025-03-06，A2。

### 论文、市场与资本开支

38. [MFIT: Multi-Fidelity Thermal Modeling](https://arxiv.org/abs/2410.09188)，论文公开稿，2024-10-11；ACM TODAES 2025/2026 DAC award，B。
39. [MFIT Open-Source Repository](https://github.com/AlishKanani/MFIT)，作者代码，检索于 2026-08-18，B。
40. [FLASH3D DAC 2026 Manuscript](https://63dac.conference-program.com/presentation/?id=RESEARCH1065&sess=sess314)，DAC 论文摘要，2026-07，B。
41. [LightningFNO DAC 2026 Manuscript](https://63dac.conference-program.com/presentation/?id=RESEARCH2358&sess=sess169)，DAC 论文摘要/原型，2026-07，B。
42. [PRO-V-R1 DAC 2026 Manuscript](https://63dac.conference-program.com/presentation/?id=RESEARCH142&sess=sess163)，DAC 论文摘要，2026-07，B。
43. [NotSoTiny DAC 2026 Manuscript](https://63dac.conference-program.com/presentation/?id=RESEARCH2760&sess=sess166)，DAC 论文摘要，2026-07，B。
44. [SEMI ESD Market Data Q1 2026](https://www.semi.org/jp/news-resources/press/20260714)，行业协会统计，2026-07-13/14，A1。
45. [SEMI ESD Market Data Q4 2025](https://www.semi.org/en/semi-press-release/esd-alliance-reports-electronic-system-design-industry-posts-5.5-billion-dollars-in-revenue-in-q4-2025)，行业协会统计，2026-04-13，A1。
46. [SEMI Global Semiconductor Equipment Forecast](https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-forecast-to-reach-a-record-229-billion-dollars-in-2028-semi-reports)，行业协会预测，2026-07-14，A1/C（实际统计+预测）。
47. [SEMI/Yole Advanced Packaging Market](https://www.semi.org/eu/technology-trends/topic/advanced-packaging)，协会转述分析机构，2025-12-16，C。
48. [Yole/SEMI High-End Performance Packaging and CPO Deck](https://www.semi.org/sites/semi.org/files/2025-06/21_Vishal%20Saroha.pdf)，分析机构公开演示，2025，C。
49. [Photonics Packaging Market to 2031](https://optics.org/news/photonics-packaging-market-to-triple-in-value-by-2031)，专业媒体转述 Yole，2026-04-08，C。

## 最终判断

DAC 2026 证明 EDA 已进入“AI 原生但物理约束更强”的阶段：agent 能显著减少可验证、重复且接口清晰的工作，但芯片、封装和系统越复杂，越需要可信工具、确定性求解、跨域数据和制造反馈。未来两年的最佳产业判断框架不是追问“AI 会不会设计芯片”，而是逐项验证：**它能否在真实客户设计上减少总人时和返工、保持或改善 coverage/PPA、控制计算成本、通过 foundry/signoff、并最终提高封装良率和出货。** 能同时回答这些问题的 EDA、测试、量测、多物理场和先进封装平台，才有资格获得持续的利润池扩张；其余多数发布仍应按路线图或期权估值。
