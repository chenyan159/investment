# 会议追踪：Robotics: Science and Systems 2026

> **会议日期**：2026-07-13 至 2026-07-17  
> **会议地点**：澳大利亚悉尼  
> **材料检索截止日期**：2026-08-18  
> **报告完成日期**：2026-08-18  
> **研究范围**：RSS 2026 会后已公开材料；机器人基础模型、具身智能、学习与控制、感知、操作、导航、人形机器人、数据与仿真、真实部署及产业链影响  
> **研究原则**：从外部公开资料独立重建证据，不继承项目内既有研究结论；优先使用会议、论文、项目、代码、客户与公司披露的一手来源。

## 结论摘要

### 投资判断先行

RSS 2026 的核心变化不是“通用人形机器人已经成熟”，而是机器人学习栈开始从单一模型竞赛，转入一套更工程化的组合：**视觉语言动作模型（VLA）负责语义与跨任务先验，模仿学习负责把高质量行为压缩成技能，强化学习负责后训练与在线适应，世界模型负责生成数据、评测和想象式训练，模型预测控制、力控、阻抗/导纳控制和安全过滤器继续掌管高频、接触和约束层。** 这意味着近期最确定的价值并不只在“最大模型”，而在数据闭环、仿真/评测基础设施、可靠性工程、末端执行器、力觉/触觉、边缘算力和售后服务。

本届会议最值得产业研究关注的九项变化如下。括号内分别为事实、估算或本报告判断。

1. **后训练和真实经验闭环取代“只靠预训练规模”成为增量焦点。**（事实＋判断）RSS 2026 的 Outstanding Paper 为 FlashSAC，强调高速、稳定的强化学习；Physical Intelligence 的 π*0.6 用示范、策略 rollout 和人工在线纠错组成 RECAP；多个 workshop 直接讨论 post-training、RL for VLA、失败恢复和从模仿到认证。基础模型仍重要，但决定现场可用性的环节向后训练、纠错和持续学习后移。
2. **世界模型从“会生成视频”转向可操作的训练、评测和策略改进工具。**（事实）RISE 用组合世界模型做想象式强化学习；Interactive World Simulator 可在单张 RTX 4090 上以约 15 FPS 维持超过 10 分钟的交互；PolaRiS 将短视频扫描转换为交互环境并用 600 次真实 rollout 校准模拟排序；MolmoSpaces 用大规模可交互场景验证策略排名。路线在加速，但接触、材料、破坏和长尾动力学仍远未解决。
3. **数据竞争从“越多越好”转向“目标、具身和质量是否对齐”。**（事实＋判断）EgoVerse、Ψ0、TactAlign 和人类到机器人表征涌现研究共同说明：人类视频、遥操作、仿真和机器人数据并非天然可互换；只有任务目标、视角、动作空间和具身覆盖足够对齐，规模才转化为泛化。数据清洗、分层采样、纠错轨迹和失败数据的边际价值上升。
4. **安全和评测从附属指标变为独立研究对象。**（事实）LIBERO-X 显示 VLA 在累积扰动下显著退化；OopsieVerse 说明“任务成功”不等于没有机械、热或液体损伤；UPS 发现视觉语言验证器会过度自信；TAIL-Safe 直接处理模仿学习的分布内漂移。高基准分数等同现场可靠性的假设被明显削弱。
5. **传统控制没有被端到端学习淘汰，而是边界更清楚。**（事实＋判断）Force Policy 把视觉策略放在高层和自由空间，把高频局部接触交给力控；Minimalist Compliance 仅用电流、电压、雅可比矩阵和导纳控制实现跨多种机械臂/灵巧手/人形的柔顺行为；GPU 鲁棒 MPC 把大规模约束优化推进到毫秒级。近期可部署架构更可能是分层系统，而非一个模型控制所有频率和安全约束。
6. **力觉、触觉与执行器模型从“可选增强”变为精细操作的基础设施。**（事实）NeuralActuator 将摩擦、迟滞、回差和热状态纳入执行器代理模型；TactAlign、LightTact、电容层析传感器等工作扩展了触觉数据、轻柔接触和接近感知。相机解决“看见什么”，但连接器插拔、柔性物、滑移、装配公差和人机接触仍需要力/触觉闭环。
7. **人形运动能力继续加速，生产经济性没有同步证明。**（事实＋判断）RSS 论文中出现 Unitree G1 滑板/推车、近身高障碍跑酷等强演示；BMW 则披露 Figure 02 在十个月内参与超过 3 万辆 BMW X3、搬运约 9 万个零件、运行约 1,250 小时。前者证明能力边界，后者证明窄任务可重复运行；两者都没有给出足以计算大规模回报率的完整数据，例如机器人数量、净节拍、干预率、维护工时和总拥有成本。
8. **专用机器人仍是规模化部署主体。**（事实）Amazon 披露其移动机器人已超过 100 万台、覆盖 300 多个设施；DHL 与 Boston Dynamics 签署最多追加 1,000 台 Stretch 的合作备忘录；Locus 自报累计超过 70 亿次拣选。相比之下，国际机器人联合会（IFR）在 2026 年仍将人形机器人描述为主要处于试验和原型阶段。未来一年物流 AMR、工业机械臂、机器视觉和工作站集成的收入确定性仍高于通用人形。
9. **“出货量”与“生产性部署”必须拆开统计。**（事实＋判断）IDC 称 2025 年人形机器人出货超过 1.8 万台，但其中超过 85% 用于展示、教育、数据采集和导览；Counterpoint 给出约 1.6 万台安装量。两者定义不同，且均不能代表连续生产工时。对上市公司利润的领先指标应改为：付费生产单元、连续运行小时、每千小时干预次数、每件成本、续单率和服务毛利。

### 时间维度结论

| 时间 | 人形机器人 | 工业机器人 | 物流机器人 | 服务机器人 | 关键硬件与基础设施 |
|---|---|---|---|---|---|
| **未来 3 个月** | 更多汽车/仓储窄任务试点与视频；论文代码复现会筛掉部分演示；对大多数上市公司 EPS 影响极小 | 中国电子与汽车需求、北美再自动化订单仍是主变量 | AMR、卸货/码垛、拣选继续扩容；客户更重视系统级吞吐而非单机智能 | 医疗、清洁、配送等既有场景优先 | GPU 仿真、数据标注、力/触觉样机、边缘计算开发套件需求先行，尚非大规模量产 |
| **未来 1 年** | 基准情景为约 9 万台广义出货，但大量仍是演示/数据采集；生产部署集中在重复搬运、上料、分拣 | 传统机械臂与协作机器人受益于更容易编程、快速换线和视觉/力控升级 | 专用系统继续跑赢人形；RaaS 和软件支持收入占比上升 | 手术机器人和专业服务机器人的闭环商业模式最可验证 | 执行器状态估计、末端执行器、触觉、机器视觉、边缘算力和维护软件的单机价值量上升；电池是续航瓶颈但不是近年电芯需求大池 |
| **未来 2 年** | 若能证明班次级可靠性和回收期，汽车/3PL 可能出现千台级生产性集群；若失败，出货仍以教育、展示和内部研发为主 | 学习方法成为工作站配置与维护工具，而非替代整套控制栈 | AMR＋固定机械臂＋视觉的混合系统仍可能是最低成本方案 | 医疗、实验室、商用清洁等监管和流程清晰场景继续形成利润池 | 利润更可能沉淀在软件/服务、集成、可靠性数据、关键精密部件，而不是同质化本体组装 |

### 受益、受损、过热与被低估方向

- **相对受益**（判断）：有真实客户运行数据的工业/物流自动化；手术机器人闭环；仿真与机器人数据工具；机器视觉、力觉/触觉、末端执行器；边缘计算；能把安装、维护和软件订阅转为经常性收入的公司。
- **相对受损**（判断）：只卖单次硬件且缺乏服务网络的本体厂商；依赖纯视觉却需要精密接触的方案；没有现场纠错/回退机制的端到端策略；把通用演示直接定价为量产订单的供应链公司。
- **过度乐观**（判断）：用“人形出货”替代生产工时；按每台 30—40 个高价减速器线性推算利润；把所有数据中心 AI 收入映射为机器人收入；假设现有电池续航能覆盖全天班次；把 sponsor demo 当作客户验收。
- **可能被低估**（判断）：失效检测、介入/回退、安全认证、遥操作支持、执行器热与回差建模、柔顺机构、夹具和工装、跨品牌车队编排、维修备件、现场数据治理。

## 研究口径与证据强度

### 事实、估算和观点的标记

- **事实**：可由会议、作者、代码仓库、研究机构、客户、监管/行业组织或上市公司披露直接核验。
- **估算**：本报告基于明确数量、单价或增长假设计算；不是机构预测或公司指引。
- **判断**：从多项事实推导的产业含义。判断不改变底层事实的证据等级。
- 所有市场和公司易变数据均标注披露日期或以本报告检索截止日 **2026-08-18** 为准；币种未特别说明时为美元。

### 证据等级

| 等级 | 定义 | 可支持的结论 | 不能支持的结论 |
|---|---|---|---|
| **A** | 客户或运营方披露的重复生产运行，且至少包含规模、时长、吞吐或收入之一 | 场景真实、任务已进入运营 | 若缺成本/干预率，仍不能证明单位经济性 |
| **B** | 多次真实硬件实验；有论文、代码/数据或第三方机构交叉验证 | 技术可在作者定义范围内重复 | 不能直接推导客户付费和规模复制 |
| **C** | 作者受控实验或供应商演示，缺乏完整复现或外部运行数据 | 能力存在、值得继续跟踪 | 不能视为产品成熟或商业部署 |
| **D** | 仅仿真、离线基准或数据集 | 方法和相对排名有研究价值 | 不能证明真实世界安全、耐久和经济性 |
| **E** | 参会者分享、媒体转述、营销口径，未取得对应一手细节 | 仅作线索 | 不进入核心结论或市场模型 |

本报告对“部署”的使用也作三层区分：**实验室真实机器人**、**客户现场试点**、**连续生产运营**。只有后两类才属于产业验证；只有披露净节拍、干预、维护、成本和续单中的多个指标，才接近商业验证。

## 会议重点和相较 2025 年的变化

### 官方会议结构的量化变化

根据 RSS 官方 accepted papers 页面逐条去重，本报告计算 2026 年共 **210 篇论文、21 个论文 session**，2025 年为 **163 篇、17 个 session**，论文数同比增加约 **28.8%**。这是对官方网页的统计，不是 RSS 发布的投稿/录用率数据。

主题标签显示了更有意义的重分配：

| 官方 session 标签的本报告计数 | RSS 2025 | RSS 2026 | 变化及含义 |
|---|---:|---:|---|
| 模仿学习 | 18 | 28 | **+56%**；行为克隆、数据质量、纠错、长时序成为主战场 |
| 人形机器人 | 10 | 13 | **+30%**；运动能力显著进步，但生产经济性仍不在论文证据内 |
| 控制 | 10 | 13 | **+30%**；学习没有挤出控制，反而推动鲁棒优化和分层接口 |
| 操作 | 28 | 27 | 基本持平；从单纯成功率转向接触、柔顺、安全和泛化 |
| VLA | 10 | 9 | 数量近似持平；路线从模型架构本身转向后训练、评测和系统组合 |

2025 年的“Scaling Robot Learning”在 2026 年被更明确地拆为 **Datasets and Benchmarks、World Models、Reinforcement Learning、Modeling** 等 session。分类口径由组委会决定，不能机械当作研究投入份额；但与 2026 年 **32 个官方 workshop** 的主题一致：post-training、数据中心方法、robot world models、RL for VLA、可信基础模型、失败恢复、sim-to-real、触觉和从实验室到生产均成为显性议题。

### 2026 年奖项传递的信号

- **Outstanding Paper：FlashSAC**。重点不是更大的基础模型，而是通过权重、特征和梯度范数约束，以及并行仿真/回放/探索，提升 off-policy 强化学习的速度和稳定性。官方摘要覆盖 50 多个任务和 10 个仿真器；项目仓库后续扩展到 100 多个任务，并报告人形步态 sim-to-real 的墙钟训练从小时级降到分钟级。证据等级 **B**：仿真覆盖广，真实验证仍主要是单类步态。
- **Outstanding Student Paper：Muninn**。用训练外缓存包装器加速机器人基础模型推理，最高报告 **4.6 倍**速度，同时提供风险/偏差证书，并展示真实导航和操作闭环。证据等级 **B**：真实硬件和理论约束兼具，但公开仓库的开箱复现实例仍以离线环境适配为主。
- **Outstanding Systems Paper：NeuralActuator**。以可学习执行器模型表示摩擦、迟滞、回差和热状态，并将模型用于控制和本体状态理解。作者开放模型、数据和部分硬件配置，覆盖约 500 美元级 OpenManipulator-X、SO-101 及 Franka 离线数据。证据等级 **B-**：系统性强，但主要仍是实验室规模。

相比之下，RSS 2025 的突出论文包含快速探索规划、形式化安全多智能体控制、复杂机器人系统构建，以及作为 finalist 的 FAST/VLA 动作 tokenization。**本报告判断**：奖项重心从“基础模型能做什么”移向“怎样让学习更快、更可控、更接近真实系统”，不是 VLA 退潮，而是系统瓶颈开始主导边际进展。

### 2025 年路线中加速、放缓和被证伪的部分

| 路线/假设 | 2026 状态 | 核心证据 | 结论 |
|---|---|---|---|
| VLA 架构和动作 tokenization | **由高速扩张转为工程化** | 2025 有 π0、OpenVLA-OFT、UniVLA、FAST；2026 VLA session 数量基本持平，而 Muninn、π*0.6、RL4VLA 和安全评测增多 | VLA 成为上层接口和先验，竞争转向推理、后训练、数据闭环和安全 |
| 强化学习 | **加速** | FlashSAC、RISE、真实飞行快速适应、多个 post-training workshop | RL 从“大规模从零训练”转为后训练、残差和现场适应工具 |
| 模仿学习 | **加速但质量门槛上升** | session 18→28；Ψ0、EgoVerse、TAIL-Safe、纠错数据 | 高质量示范仍是核心，但必须处理漂移、失败和具身错配 |
| 世界模型 | **显著加速** | RISE、Interactive World Simulator、PolaRiS、MolmoSpaces | 从生成视觉转向训练、评测、数据扩增；物理真实性仍是主要约束 |
| 大规模仿真 | **继续加速，但“光真实”路线放缓** | GS-Playground、MolmoSpaces 对比 NeuralActuator、力控和触觉工作 | 几何/视觉覆盖容易扩张，接触、执行器和材料模型决定最后一公里 |
| 纯端到端控制所有层级 | **被明显限定** | Force Policy、Minimalist Compliance、GPU 鲁棒 MPC、keynote 系统观 | 高层可学习，低层高频控制和安全约束仍适合显式模型/控制器 |
| 高干净基准分数＝现场泛化 | **被证伪** | LIBERO-X 的累积扰动、OopsieVerse 的损伤维度 | 必须用扰动、干预、伤害和长时序指标重测 |
| 数据量自然带来跨具身泛化 | **被证伪为不充分条件** | EgoVerse、Ψ0、人类到机器人表征工作 | 对齐、覆盖和数据质量是规模生效的前提 |
| 人形演示＝可经济部署 | **尚未成立** | 强运动 demo 与 BMW/GXO 等有限运营披露之间仍有指标缺口 | 需要生产工时、干预率、维护和回收期证据 |

这里的“被证伪”针对具体强假设，而不是宣判 VLA、端到端学习、仿真或人形路线整体无效。

## 技术路线与边界变化

### 一套更可能落地的分层栈

| 层级 | 主要方法 | 2026 年最合适的职责 | 当前不应强行承担的职责 |
|---|---|---|---|
| 任务与语义层 | VLM/VLA、语言规划器 | 理解指令、识别对象/场景、跨任务迁移、调用技能 | 毫秒级接触控制、硬安全保证、未知故障恢复 |
| 技能策略层 | 模仿学习、diffusion/flow policy、行为库 | 把示范压缩为连续动作、完成中短时序技能 | 在稀有危险状态中自行探索 |
| 后训练与适应层 | RL、残差策略、在线纠错、RECAP | 提高成功率/速度，学习恢复，适应场景和本体 | 在无护栏生产线中无限制在线更新 |
| 预测与数据层 | 世界模型、数字孪生、Real2Sim、生成式仿真 | 数据扩增、策略筛选、反事实评测、想象式训练 | 替代所有真实接触/磨损/破坏数据 |
| 高频执行层 | MPC、阻抗/导纳、力控、状态估计 | 稳定、柔顺、接触、约束处理、低延迟响应 | 复杂开放语义推理 |
| 独立安全层 | 安全过滤器、异常检测、形式化/统计校准、人工介入 | 约束动作、触发询问/回退/急停、记录失效 | 被主策略的成功率指标吞并 |

这不是理论上唯一架构，而是截至 2026-08-18 证据最强的工程折中。Karen Liu 的 keynote 将机器人未来描述为模拟器、几何、动力学、人类先验、规划器与预训练 VLA 组成的生态；Salah Sukkarieh 强调现场伙伴、失败和长期运行会改变科学问题；Wenzhen Yuan、Pulkit Agrawal 分别把触觉规模化和“force intelligence＋部署中终身学习”置于核心。五场 keynote/spotlight 共同削弱了“单一通用模型足以解决机器人”的叙事。

### 基础模型与 VLA：仍是入口，不再是完整答案

2025 年 OpenVLA-OFT 在 LIBERO 报告成功率从 76.5% 提升到 97.1%，推理吞吐提高 26 倍，真实 ALOHA 任务最多提升 15 个百分点；这代表当年围绕动作表示和微调效率的显著进展。2026 年 LIBERO-X 则通过外观、物体位置、动力学和多项累积扰动，显示多个 VLA 的性能会明显下滑。

**事实**：Muninn 证明推理缓存可以在保留任务/安全约束下显著加速；π*0.6 证明 rollout 与人工纠错能把强基础策略推进到更困难任务；Ψ0 证明约 800 小时人类数据与 30 小时机器人数据的分阶段组合，可以在九项真实任务中超过使用十倍以上机器人数据的基线；人类到机器人表征研究则显示，足够的机器人具身和任务多样性可让只在人类数据中出现的对象泛化接近翻倍。

**判断**：VLA 的核心价值正在从“直接控制一切”转为三点：语义先验、数据引擎和技能编排。其商业壁垒更可能来自专有现场数据、纠错闭环和安全接口，而不是仅靠公共数据上的参数规模。

### 强化学习与模仿学习：由二选一变为流水线

模仿学习适合从昂贵、高质量示范快速得到可用行为，但 TAIL-Safe 说明其即使在看似分布内状态也会因闭环漂移进入危险区域。强化学习能在奖励明确、仿真并行或有安全护栏时优化速度、能耗和恢复，但真实探索成本高。

π*0.6 的 RECAP 提供了一条更现实的流程：先用示范训练，再让策略执行，收集失败附近的人工纠错，最后继续优化。作者在最困难任务中报告吞吐最高提升超过两倍、失败约减半；并展示约 13 小时连续咖啡制作、超过 2 小时陌生家庭洗衣，以及真实工厂箱体装配。证据等级 **B**：时长和环境显著强于普通 demo，但均为开发者自证的有限任务，未披露客户 OEE、操作员配置和成本。

**判断**：未来一年，IL 更像技能初始化器，RL 更像后训练器，人工纠错/遥操作更像长尾保险。谁能降低每次纠错成本、将失败数据结构化并安全回放，谁更可能拥有数据飞轮。

### 世界模型与仿真：价值从合成图像转向排序可信度

关键成果不是“做出了更漂亮的画面”，而是能否回答：在仿真中表现更好的策略，到了真实世界是否仍更好。

- **PolaRiS（B-/D）**：用手机/短视频扫描构建交互环境，建立 **600 次真实 rollout 与 9.3 万次仿真 rollout** 的配对评测，并报告比现有模拟器更强的真实策略排序相关性。重要性在校准，而不只在生成。
- **MolmoSpaces（D，数据/基准层）**：发布超过 **23 万个环境、13 万个资产、4.8 万个可操作资产、4,200 万个抓取样本**，覆盖八类任务；在其受控范围内，模拟与真实结果报告 Pearson 相关系数 0.96、排名相关系数 0.98。相关性不等于复杂接触任务的普遍 sim-to-real。
- **EgoVerse（D/B-）**：收集 **1,362 小时、8 万个 episode、1,965 个任务、240 个场景、2,087 名参与者** 的第一视角人类活动数据；实验强调只有充分对齐时规模才生效。仓库在截止日仍提示缓存/模式变更和重新下载，数据可用性在演进。
- **GS-Playground（D）**：项目报告 640×480 下最高约 **10⁴ FPS** 的 Gaussian Splatting 渲染，并支持 Real2Sim。截止日仓库清单显示渲染、基准与若干 Real2Sim 子项已开放，但完整端到端集成、PPO/视觉策略脚本及部分资产/评测仍未全部勾选，不能称为“完整开源系统”。
- **Interactive World Simulator（B-/D）**：作者报告单张 RTX 4090 上约 15 FPS、稳定交互超过 10 分钟，并开放代码、检查点和数据；在作者任务中，生成数据训练的策略接近等量真实数据。仍缺跨机器人、材料与破坏事件的独立复现。
- **RISE（C/D）**：组合世界模型加想象式 RL，在真实砖块、背包、箱体三项任务中分别提高约 35、45、35 个百分点。三项作者环境不足以外推到开放世界。

**判断**：世界模型近期最可能产生收入的形式是测试覆盖、仿真服务、合成数据、数字孪生和模型回归平台，而不是直接替代机器人控制器。企业采购时应要求“与真实策略排名的相关性”和“失败模式覆盖率”，而不是只看视觉逼真度。

### 传统控制、执行器与本体：软件进步反而暴露物理层

NeuralActuator 的获奖说明，摩擦、迟滞、回差和热状态不是可以被无限数据掩盖的噪声。Tune to Learn 进一步发现，柔顺和过阻尼可帮助离线模仿学习；强化学习在不同增益区间都能工作，但增益选择仍显著影响 sim-to-real，刚性且过阻尼的配置尤其不利。

Force Policy 采用视觉高层决策＋高频局部力控；Minimalist Compliance 不依赖力/矩传感器、专用电流环或学习，也能在机械臂、手和人形上提供柔顺能力；GPU 鲁棒 MPC 的实验报告相对 CPU 快 97.7%、相对既有 GPU 实现快 71.8%，在 61/75 维系统、约 20 万变量和 8 万约束下平均约 34 ms，并报告经验测试中 100% 满足安全约束。

**判断**：这组结果对产业链的含义是：

- 高质量电机电流/温度/位置数据、执行器可辨识性和热管理的价值上升；
- 力/矩传感器并非每个自由度都必需，但精细末端接触仍需要直接或间接力估计；
- 机械柔顺与软件阻抗需要共同设计，不能只堆高扭矩和刚度；
- 可解释的低层控制与独立安全层仍是客户验收、认证和故障定位的重要资产。

## 瓶颈：从论文成功率到班次级生产

### 数据获取与数据质量

1. **真实机器人数据昂贵且长尾稀疏。** 遥操作需要设备、操作员和安全环境；成功示范远多于故障恢复数据。
2. **人类视频并不自带机器人动作。** 视角、手部自由度、接触力和目标函数错配，需要表征对齐或少量机器人后训练。
3. **失败数据有安全和责任成本。** 生产线上无法像仿真那样随意探索；必须有沙盒、数字孪生、回退和人工介入。
4. **数据产权与客户场景绑定。** 工厂布局、产品、节拍和异常日志往往不能外传，公共数据难以复制壁垒。

### Sim-to-real 与世界模型

视觉/几何扩张速度已明显快于物理扩张速度。当前仍缺：摩擦和磨损随时间变化、柔性和液体、多体接触、传感器污染、执行器热衰减、线缆/背隙、碰撞后的结构损伤，以及人与机器动态交互。PolaRiS 代表更正确的方向——用真实 rollout 校准模拟排序；NeuralActuator 则说明执行器本身也需进入仿真。

**证伪指标**：若模型在随机化外观中领先，却不能在真实策略排名、接触失败和跨班次漂移上保持领先，则其 sim-to-real 价值被证伪。

### 长时序、泛化与恢复

长任务的总成功率近似由每一步可靠性连乘决定。即使单步骤成功率为 99%，连续 100 步无失败概率也只有约 36.6%（本报告数学示例：0.99¹⁰⁰）。因此长时序不是增加上下文窗口就能解决，还需：状态检查点、可重试技能、异常分类、局部恢复、人类介入和任务级事务管理。

π*0.6 的连续咖啡/洗衣展示是重要进步，但未公开每千次动作介入数；LIBERO-X 和 OopsieVerse 进一步说明，完成任务可能同时积累不可接受的偏差或损伤。

### 安全、责任与认证

UPS 显示 VLM 验证器会过度自信，因此把另一个大模型当“安全裁判”并不足够；其 conformal calibration 与 act/ask/intervene 框架更接近可审计系统。TAIL-Safe 用不变安全集和数字孪生约束模仿策略，代表学习控制必须有外部护栏。

IFR 在 2025—2026 年的人形机器人材料中明确列出安全标准尚在发展、传统机器人仍更快/精确/可靠/可重复。对客户而言，安全认证、风险评估和责任划分可能比模型能力晚 12—24 个月形成规模约束。

### 执行器、传感器、算力与电池

| 瓶颈 | 会议/产业证据 | 近期含义 |
|---|---|---|
| 执行器热、摩擦、回差 | NeuralActuator、Tune to Learn；人形厂商很少公开持续扭矩和寿命曲线 | 单次峰值扭矩不是可用性；需要热模型、寿命测试、模块化维修 |
| 触觉/力觉覆盖 | TactAlign 约 5 分钟人类触觉数据即可做未见物体迁移；LightTact 面向超轻液体/薄膜；ECT 同时感知接近、方向和材料 | 精细操作传感器内容量会上升，但耐久、布线、标定和成本仍未证明 |
| 边缘算力与延迟 | Muninn 最高 4.6×推理提速；NVIDIA Jetson Thor 为 128 GB、40—130 W、2,070 FP4 TFLOPS | 推理优化可减少模块数、功耗和控制延迟；机器人收入不能等同数据中心收入 |
| 电池 | Unitree G1 官方标称约 2 小时、9,000 mAh、54 V；Agility Digit 标称最长约 4 小时并可自动回充；IFR 指出续航不足整班 | 续航是运营约束，但近期人形电芯需求量很小，不能形成 EV 级利润池 |

以 G1 规格计算，单包名义能量约 **0.49 kWh**（9 Ah×54 V，本报告估算）。即使 10 万台机器人、每台两包，也仅约 **0.10 GWh**。即便按更高端人形每包 3 kWh、每台两包计算，也只有 **0.60 GWh**。因此电池目前是停机、换电和热管理问题，不是足以显著改变全球电芯供需的需求量。

### 会议没有解决、但产业必须回答的问题

- 连续一个班次的净运行时间与有效吞吐，而不是最佳视频；
- 每千小时安全停机、人工介入、零部件更换和软件回滚次数；
- 机器人数量、操作员/遥操作员配比和场地改造成本；
- 维护服务收入对应的真实履约成本；
- 跨客户迁移需要多少新增示范和工程周；
- 电池更换/充电是否打断节拍；
- 出现人员、液体、灰尘、反光、遮挡和工件偏差时的损失上限。

## 从真实验证到产品部署

### 已经在真实环境重复验证或运营的案例

| 案例 | 截至日期的一手披露 | 证据等级 | 可得结论 | 仍缺什么 |
|---|---|---:|---|---|
| **Amazon 移动机器人** | Amazon 于 2025-07 披露超过 **100 万台**、覆盖 **300 多个设施**；DeepFleet 声称将车队行程效率提高 10% | **A** | 专用 AMR 已经规模化，车队软件能产生系统收益 | 单独机器人业务收入和利润未披露 |
| **Figure 02 / BMW Spartanburg** | BMW 2026-02 披露十个月内支持超过 **3 万辆 X3**、搬运约 **9 万个零件**、约 **1,250 小时**、约 120 万步；工作为钣金车间窄任务 | **A-** | 人形在真实汽车生产中的重复窄任务成立 | 机器人数量、达成的干预率、维护成本和回收期 |
| **Boston Dynamics Stretch / DHL** | 双方 2026-02 披露从 2023 年开始商业使用，并签署最多新增 **1,000 台**的 MOU；供应商称最高约 700 箱/小时 | **A-/B+** | 专用卸货方案获得大型客户扩张意向 | MOU 不等于交付；缺净吞吐、站点数和项目 ROI |
| **Digit / GXO / Spanx** | GXO 2024-06 披露多年期 RaaS 商业协议，用于搬运周转箱 | **B+** | 客户付费与真实仓库运营成立 | 单位数、运行小时、吞吐、干预和续单规模未披露 |
| **Locus AMR** | Locus 在 2026 年公司材料中自报超过 **1.7 万台、360 多个站点、70 亿次拣选、1.9 亿运行小时** | **B+** | 供应商口径显示成熟 AMR 的数量级远高于人形生产部署 | 需客户逐项审计，且无公开分部利润 |
| **Intuitive da Vinci** | 2026-Q2 末装机 **11,710 台**，季度收入 28.92 亿美元，器械耗材收入 17.35 亿美元 | **A** | 封闭临床流程、监管、培训、耗材和服务可形成高质量机器人利润池 | 不代表开放环境通用机器人可复制该模式 |

BMW/Figure 的数字是本届会议外最重要的人形交叉验证之一。Figure 自己提出“整班成功率超过 99%、零干预”等目标，但没有披露已经实现这些目标；本报告只采用 BMW 已确认的运行数字，不把目标当事实。

### 真实硬件研究，但仍属于受控实验

| 成果 | 真实验证 | 证据等级 | 产业化边界 |
|---|---|---:|---|
| π*0.6 / RECAP | 咖啡、洗衣、箱体装配；最长约 13 小时连续运行 | B | 作者环境、少数任务；缺客户运营和成本 |
| NeuralActuator | 多类低成本机械臂及 Franka 数据；开放检查点/数据 | B- | 执行器和数据规模仍小，耐久/批量一致性未知 |
| Muninn | 真实导航与操作闭环，带风险/偏差证书 | B | 缓存对不同模型架构、动态场景和长任务的收益需复现 |
| TactAlign | 未配对触觉数据、未见物体/任务、灯泡旋拧 | C+ | 受控桌面实验；传感器耐久、标定漂移和集成成本未知 |
| HAIC | Unitree G1 滑板、推拉车、箱体地形 | C | 展示动态适应，不代表工业节拍或人机安全 |
| Perceptive Parkour | G1 跨越约 1.25 米、约机器人身高 96%的障碍并组合运行 | C | 强运动演示；能耗、摔倒率、硬件寿命未公开 |
| 真实飞行快速适应 | 约 100 秒真实飞行中从 1.9 m/s 提升至 7.3 m/s | C+ | 有力证明快速在线适应，但航空安全和重复性要求更高 |
| CRAFT Hand | 低于 600 美元、15 个执行器、覆盖 Feix 33/33 抓握类型，设计公开 | C+ | 原型成本和能力有吸引力；寿命、良率、量产和触觉闭环未知 |

### 仅为仿真、基准或演示，不应计为部署

PolaRiS、MolmoSpaces、EgoVerse、GS-Playground、RISE 的核心价值是数据、评测或仿真；它们不是产品部署。RSS sponsor demo 页面列出 Unitree、AGIBOT、Spirit AI、Anduril、Toyota Research Institute、Sharpa、Robbyant 等短讲/展示，这只能证明厂商在场和愿意演示，**不能证明客户验收、可靠性或收入**。

Amazon 的 Blue Jay 也是重要反例：Amazon 在 2026-02 更新中明确表示已不再在运营中使用 Blue Jay，但保留底层技术用于其他项目。它说明即便大型运营商公开过强演示，系统也可能因运营经济性、集成或优先级变化而退出；“曾经试点”不应永久计入部署基数。

## 未来 3 个月、1 年和 2 年的产业影响

### 未来 3 个月：复现和指标重构，收入影响有限

**事实基础**：FlashSAC、Muninn、NeuralActuator、MolmoSpaces、EgoVerse、Interactive World Simulator、CRAFT Hand 等已开放不同程度的代码、模型、数据或设计文件；GS-Playground 则仍有若干未完成发布项。会后最先发生的不是大规模采购，而是实验室和企业研发团队复现、迁移和压力测试。

**判断**：

- 人形厂商会继续发布汽车、仓储和导览试点；投资者应只把客户确认、付费、运行小时和续单计入订单证据。
- VLA 排名会因 LIBERO-X 一类累积扰动测试重排，干净基准的营销价值下降。
- 机器人公司会增加“失败恢复、干预率、连续运行”措辞，但除非给出分母和测试协议，否则信息价值有限。
- 触觉、力控、执行器建模与边缘算力开发套件订单会先增长，绝对规模仍不足以改变大型元件公司的季度利润。
- 工业和物流客户的采购仍由产能利用率、工资、利率、关税、项目回收期和系统集成能力主导，RSS 论文不是短期订单的主要变量。

### 未来 1 年：窄任务人形开始分化，专用机器人继续兑现

**基准情景判断**：到 2027 年三季度前，广义人形机器人出货可接近 9 万台/年，但生产性部署远低于出货；汽车和 3PL 的重复搬运、排序、上料、空箱流转是优先场景。需要精密触觉、复杂工具使用、随机人流或全天候户外运行的任务仍以试点为主。

工业机器人不会因人形出现而萎缩。更现实的变化是：VLA/语言接口缩短示教和换线时间，世界模型用于离线测试，RL 优化局部技能，原有机械臂、PLC、安全控制器和工装继续承担生产。物流中，AMR、输送、固定机械臂和专用卸货机器人凭借速度、能耗和可靠性继续占主导。

硬件需求的方向性强弱预计为：

1. **强**：边缘 GPU/内存、机器视觉、关节位置/温度/电流采集、末端执行器、工业网络和车队软件；
2. **中等**：力/矩和触觉传感器、可快速维修的执行器模块、精密减速器、遥操作设备；
3. **场景化**：LiDAR、非接触材料识别、多指灵巧手；
4. **数量被高估**：人形电池电芯、按自由度线性外推的高价减速器、只用于训练展示的昂贵传感器。

### 未来 2 年：商业结果取决于可靠性曲线，而非能力曲线

到 2028 年三季度前，若领先厂商能在客户侧同时达到以下本报告研究门槛——**单机累计生产运行超过 5,000 小时、计划内可用率超过 95%、平均每个八小时班次人工介入不超过一次、总拥有成本回收期不超过三年，并获得同一客户的批量续单**——则汽车、电子和大型 3PL 中可能形成千台级生产性集群。上述阈值是研究筛选标准，不是当前行业已达成事实。

若这些指标无法披露或连续两个产品代际仍未改善，产业会回到更模块化的组合：专用 AMR 承担移动，固定机械臂承担高速操作，人类处理长尾。人形本体仍可增长，但利润池会偏向教育、研发、数据采集、娱乐和政府项目，估值应显著低于生产自动化平台。

## 市场规模、利润池与未来一年三情景

### 当前可核验的市场锚点

| 市场 | 最新可比事实（材料日期） | 口径限制 |
|---|---|---|
| **工业机器人安装硬件** | IFR：2024 年全球安装 **542,076 台**，运行存量约 **466.4 万台**、同比 +9%；2026-01 给出的全球年度安装市场价值约 **167 亿美元** | 价值口径通常不含软件、外围设备和系统集成；2025 完整实绩在本报告截止日尚非同口径公开基准 |
| **专业服务机器人** | IFR 样本：2024 年销量约 **19.9 万台**、同比 +9%；其中运输/物流约 **10.29 万台**、同比 +14%；RaaS 车队超过 **2.45 万台**、同比 +31% | IFR 明确这是报告企业样本，不是全市场总体或预测；年度样本变化，不能直接做长期同口径序列 |
| **人形机器人** | Counterpoint：2025 年约 **1.6 万台安装**；IDC：2025 年**超过 1.8 万台出货**，其中超过 85% 用于展示、教育、数据采集和导览 | 安装与出货定义不同；产品边界、低价教育机和生产机混合；不能当作生产机器人规模 |
| **医疗机器人可观察龙头** | Intuitive Surgical：2026-Q2 收入 **28.92 亿美元**、GAAP 毛利 **19.60 亿美元**、期末装机 **11,710 台**；季度年化收入约 **115.7 亿美元**、毛利约 **78.4 亿美元**（本报告简单乘四） | 是单一龙头 run-rate，不是全球医疗机器人 TAM；季节性会造成偏差 |
| **物流系统可观察样本** | Symbotic：2026 财年 Q2 收入 **6.76 亿美元**，70 套系统处于部署；系统销售毛利率约 21.9%，软件支持约 73.9%，运营服务约 5.0%（本报告按分项收入/成本计算） | 软件支持仅占该季收入约 1.9%，高毛利率不能直接套用于全部收入 |

IFR 曾预测 2025 年工业机器人安装约 57.5 万台，并预计 2028 年超过 70 万台。由于截止日缺少同口径 2025 最终全球安装数，本报告未来一年模型从 IFR 的 2024 实绩和 2026 年市场价值锚点出发，不把预测冒充实绩。

### 2027 年三情景：市场收入与利润敏感性

以下全部为**本报告估算**，目标是暴露关键假设，而非给出精确点预测。未来一年指 2027 全年附近的年度化水平。

| 市场 | 悲观情景 | 基准情景 | 乐观情景 | 关键公式与利润池假设 |
|---|---:|---:|---:|---|
| **工业机器人安装硬件收入** | 55.5 万台×2.9 万美元＝**161 亿美元** | 63 万台×3.05 万美元＝**192 亿美元** | 70 万台×3.2 万美元＝**224 亿美元** | 单价为安装硬件平均值；不含集成。若供应商经营利润率分别为 8%/11%/14%，对应经营利润敏感性约 **13/21/31 亿美元** |
| **物流机器人硬件收入** | 14 万台×2.5 万美元＝**35 亿美元** | 15.5 万台×3.5 万美元＝**54 亿美元** | 17 万台×4.5 万美元＝**77 亿美元** | 从 IFR 2024 样本销量外推，不代表全市场；AMR、卸货、拣选价格差异大。按 15%/25%/35%毛利率，毛利敏感性约 **5/14/27 亿美元** |
| **广义人形机器人硬件收入** | 5 万台×1.6 万美元＝**8 亿美元** | 9 万台×2 万美元＝**18 亿美元** | 14 万台×2.5 万美元＝**35 亿美元** | 混合低价展示/教育机和较昂贵工业机；按 0%/10%/20%毛利率，硬件毛利约 **0/1.8/7 亿美元**；生产性部署远小于出货 |
| **Intuitive 可观察机器人闭环收入** | **108 亿美元** | **132 亿美元** | **150 亿美元** | 非市场 TAM；按 65%/68%/70% GAAP 毛利率，毛利约 **70/90/105 亿美元**，用于展示耗材＋服务闭环的利润量级 |

#### 情景假设

- **悲观**：全球制造资本开支偏弱；人形客户试点不转批量；安全/可靠性指标无改善；价格竞争快于降本；系统集成和售后拖累毛利。
- **基准**：工业机器人恢复温和增长；物流自动化维持两位数附近增长；人形由 2026 年约 5—6 万台的广义出货基数升至约 9 万台，但生产任务仍集中；软件/服务占比缓慢提升。
- **乐观**：电子、汽车和仓储同步扩产；世界模型和后训练显著缩短部署周期；至少两家人形厂商取得大客户批量续单；关键部件良率和现场维护改善。

#### 口径冲突与处理

1. **人形 2025 数字**：Counterpoint 的“安装约 1.6 万台”低于 IDC 的“出货超过 1.8 万台”，合理差异来自出货未安装、产品定义和样本。报告采用区间，不做算术平均。
2. **2026 半年数字**：Smart Analytics Global（SAG）的详细报告未能从公开页面完整取得；专业媒体在 2026-08-10 转述其上半年约 **1.91 万台、同比 +272%**，并称全年可能约 6 万台。该线索仅用于校验基准情景，证据等级 **E+/中等置信度**，没有当作市场事实锚点。
3. **专业服务机器人**：IFR 每年参与公司不同，19.9 万台和 10.29 万台均为样本汇总，不能据此宣称全球市场完整规模。本报告场景明确称为“被跟踪供应商硬件敏感性”。
4. **市场价值与公司收入**：IFR 工业机器人安装价值不包含全部集成；Symbotic、Intuitive 等公司收入含软件、耗材或服务，不能直接相加。

### 利润池会落在哪里

| 利润池 | 当前证据 | 一年判断 | 需要警惕 |
|---|---|---|---|
| **耗材、服务、装机闭环** | Intuitive Q2 GAAP 毛利率约 67.8%，器械耗材占季度收入约 60% | 最成熟、最可持续；专业医疗/实验室优先 | 监管、手术量、竞争系统、定价压力 |
| **软件支持、车队编排、数据** | Symbotic Q2 软件支持分项毛利率约 73.9%，但收入占比仅约 1.9%；Amazon 称 DeepFleet 提升行程效率 10% | 高毛利潜力高，绝对规模取决于装机基数和合同拆分 | 把小分项高毛利外推至整家公司 |
| **标准工业机器人本体** | ABB Robotics 2024 收入约 23 亿美元、运营 EBITA 率 12.1%；业务以 53.75 亿美元企业价值出售给 SoftBank | 周期复苏可带来经营杠杆，盈利确定性高于早期人形 | 中国价格竞争、汽车/电子资本开支周期 |
| **物流系统集成** | Symbotic 系统销售毛利率约 21.9%，70 套系统部署；DHL 过去三年在自动化投入超过 10 亿欧元 | 收入池大，项目管理和交付节奏决定利润 | 营运资金、验收延迟、客户集中和现场成本 |
| **机器人 LiDAR/感知** | Hesai 2026-Q1 机器人 LiDAR 出货 **118,282 台、同比 +137.8%**；总收入 6.806 亿元人民币、毛利率 39.1%，同时披露 ASP 下降 | 量先于利；专用 AMR、割草/服务机器人是近期主体 | 单价下降、客户集中、把人形叙事误当现有销量来源 |
| **人形本体** | 大部分市场出货仍为展示、教育、数据和导览；单位经济性极少公开 | 基准情景硬件毛利池仍小，研发/售后可能吞噬毛利 | 补贴、关联交易、试点转化率、保修和遥操作成本 |
| **精密执行器/减速器** | NeuralActuator 和 IFR 均说明可靠性/热/维修是核心；Harmonic Drive 管理层称现实落地节奏与旧计划假设存在偏差 | 有量产选择权，但订单需按客户、型号、良率验证 | 按关节数×目录价外推；降本、替代和集成设计会压缩单机价值 |

### 为什么机器人边缘算力不是 NVIDIA 数据中心收入的等量映射

NVIDIA Jetson Thor 官方规格为 128 GB 内存、40—130 W、最高 2,070 FP4 TFLOPS；T5000 模块公开价格在千台量级约 2,999 美元。若 2027 年基准情景 9 万台人形每台使用一个该价位模块，理论采购额约 **2.70 亿美元**（本报告估算），且还没有扣除竞争芯片、客户自研、折扣和低端机型。这足以形成有意义的机器人边缘业务，但与数据中心数百亿美元级收入不是一个数量级。

## 公司及产业链映射

### 已有经营数据的上市公司

| 公司/业务 | 与 RSS 2026 主题的连接 | 最新公开经营信号 | 投资解读 | 关键证伪指标 |
|---|---|---|---|---|
| **Intuitive Surgical** | 精细操作、视觉、力反馈替代、封闭工作流和安全认证 | 2026-Q2 收入 28.92 亿美元、+19%；装机 11,710 台、+12%；器械耗材 17.35 亿美元 | 机器人利润池来自装机＋高频耗材＋服务＋培训，不来自一次性本体 | 手术量增速、耗材单价、竞争装机、毛利率 |
| **ABB Robotics（拟售予 SoftBank）** | 工业机械臂、控制、数字化与集成 | 2024 收入约 23 亿美元、运营 EBITA 率 12.1%；交易 EV 53.75 亿美元 | 提供成熟本体业务的估值与利润率锚；不等于人形估值锚 | 交易完成、订单周期、软硬件服务占比 |
| **FANUC** | 工业机器人、CNC、伺服和现场可靠性 | 2026 财年第一季度机器人销售约 **961 亿日元、同比 +18.7%**，但环比 -12.1% | 工业周期与中国需求仍比基础模型新闻更影响盈利 | 订单、价格、产能利用率、中国本土竞争 |
| **Teradyne Robotics（Universal Robots、MiR）** | 协作臂、AMR、易编程与车队 | 2026-Q2 Robotics 收入约 **1 亿美元**，同比高于 7,500 万美元、环比高于 9,100 万美元；公司未在新闻稿拆分利润 | 能验证协作/移动机器人需求回升，但集团利润仍由半导体测试主导 | 分部毛利、重组后盈利、渠道库存和大客户 |
| **Symbotic** | 仓储自动化、视觉、车队调度、软件支持 | 2026 财年 Q2 收入 6.76 亿美元、净利 900 万美元、调整 EBITDA 7,800 万美元、70 个部署中系统 | 系统收入大而软件收入小；长期利润取决于支持/运营标准化 | 验收节奏、客户集中、现金流、软件收入占比 |
| **Hesai** | 机器人 LiDAR 与感知 | 2025 全年机器人 LiDAR 23.93 万台、+425.8%；2026-Q1 11.83 万台、+137.8%；公司称机器人 LiDAR毛利率高于 ADAS，但未给出精确分部率 | 当前销量更多来自各类机器人而非只靠人形；量增需对照 ASP 和回款 | 机器人分部收入/毛利、ASP、客户集中、库存 |
| **Harmonic Drive Systems** | 精密减速器、关节 | 管理层在现行规划说明中承认现实世界落地节奏与旧中期计划假设出现偏差 | 是执行器量产选择权，不宜把人形单位含量当已实现收入 | 人形相关订单、产线利用率、降价、客户自制/替代 |
| **Nabtesco** | 精密减速器、工业机器人与 AGV/AMR | 2026-02 规划预期工业机器人资本开支复苏，并拓展 AGV/AMR 等非传统机器人用途 | 近期仍由传统工业机器人周期驱动，人形为额外选择权 | 精密减速机订单、份额、价格和非机器人占比 |
| **NVIDIA** | 仿真、训练、世界模型、Jetson Thor 边缘计算 | Thor 已商业发布；但公司没有把机器人收入单独披露 | 基础设施受益明确，财务贡献应按可见模块数而非总体 AI 收入估算 | Jetson 出货、客户自研 ASIC、功耗/成本、软件变现 |

### 私营公司与客户验证

| 主体 | 已验证内容 | 未验证内容 | 投资/竞争含义 |
|---|---|---|---|
| **Figure / BMW** | 窄任务、真实生产、累计小时和产量 | 机器人数量、付费价格、干预率、维护、ROI | 当前最强人形生产证据之一；仍不足以证明通用化和高毛利 |
| **Agility / GXO** | 多年 RaaS 协议、仓库周转箱任务 | 规模、吞吐、续单和毛利 | RaaS 可降低客户初始门槛，但遥操作/维护可能藏在服务成本中 |
| **Boston Dynamics / DHL** | 商业运行历史、最高 1,000 台扩张意向 | 实际交付量、客户净 ROI | 专用形态比人形更快证明卸货经济性 |
| **Amazon** | 百万 AMR、跨 300 多站点车队、内部算法优化 | 独立机器人收入和外部销售 | 最大事实是专用车队规模，不是对外本体市场 |
| **Locus** | 大规模 AMR 运行口径 | 客户审计和利润 | 拣选/车队数据壁垒可能高于本体壁垒 |
| **Physical Intelligence** | π*0.6 长时序作者实验和工厂任务 | 独立客户运营、商业模式和成本 | 强技术先验提供软件价值，但尚未形成可计量利润池 |
| **Unitree** | G1 公开起售价含税 8.5 万元人民币、约 2 小时电池，论文生态活跃 | 生产任务小时、售后成本、工业安全和批量客户 ROI | 低价加快开发者/教育数据飞轮，也会压低广义出货 ASP |

### 产业链的“确认收入、可选性、叙事”三分法

1. **确认收入**：公司披露中已经有机器人分部收入/销量或客户运营，例如 Intuitive、ABB Robotics、FANUC、Teradyne Robotics、Symbotic、Hesai，以及 Amazon/Locus 等运营端。
2. **可选性**：产品技术上匹配执行器、减速器、视觉、触觉、边缘计算，但尚未披露机器人客户收入或量产 design win。估值模型只应给概率加权期权，不应计入基准利润。
3. **叙事**：仅出现在供应商名单、意向协议、展示、媒体供应链传闻或“每台含量”测算中。没有客户、型号、数量、价格、交付和收入确认前，不进入盈利预测。

对任何中国或海外上市的伺服、丝杠、减速器、轴承、热管理、连接器和电池公司，至少核对以下五项后再认定受益：**客户名称是否由双方确认、产品是否进入量产 BOM、年化数量、价格下降曲线、机器人收入占公司总收入比例**。缺一项不必排除，但必须降低置信度。

## 风险、反例与证伪指标

### 技术和产品风险

| 风险 | 为什么重要 | 最早可观测指标 | 证伪/确认阈值（本报告研究门槛） |
|---|---|---|---|
| 长时序误差累积 | 单步 99% 不等于百步可靠 | 每任务重试、每班干预、恢复成功率 | 八小时平均干预仍 >1 次，且两个季度无改善，则“无人化”假设被否定 |
| 世界模型错误自信 | 视觉逼真可掩盖错误物理 | 仿真—真实策略排名、长尾失败覆盖 | 仅报告图像指标，不报告真实排序/失败相关性，则不计部署价值 |
| 执行器热和耐久 | 峰值动作演示无法说明班次能力 | 持续扭矩、温升、关节更换、保修 | 5,000 小时前出现高频大修，三年 ROI 难成立 |
| 触觉成本与耐久 | 传感器容易在论文中成功、在工厂中污染/漂移 | 标定周期、破损率、线缆和清洁 | 维护节省不能覆盖传感器与停机成本，则只适合高价值任务 |
| 安全与责任 | 大模型验证器也会过度自信 | 事件率、近失、独立安全认证 | 缺少独立安全层或无法审计策略更新，不进入人机共域规模部署 |
| 数据飞轮失效 | 数据多但错配时收益饱和 | 每新增 100 小时数据的成功率/迁移增益 | 边际增益持续低于采集成本，预训练规模叙事应下调 |

### 商业和估值风险

- **出货口径膨胀**：展示、教育、样机、内部数据采集被计入“商业化”。追踪生产任务占比，而不是总出货。
- **MOU 当订单**：DHL/Stretch 的最多 1,000 台属于意向上限，实际交付和收入确认必须后续核验。
- **收入没有利润**：早期本体的质保、驻场、遥操作和定制工程可能吞噬硬件毛利；要求披露服务成本和自由现金流。
- **供应链重复计算**：整机出货×自由度×目录价会忽略集成关节、降价、国产替代、自研和不同产品配置。
- **宏观周期错配**：FANUC、ABB 等近期仍受汽车、电子、汇率和中国资本开支影响，人形论文无法抵消工业周期。
- **客户集中**：物流系统和人形试点常集中于少数巨头，延期或策略变化会使单季收入波动。
- **监管滞后**：在公共空间、医疗和人机共域中，安全责任可能推迟部署，或增加认证/保险成本。

### 需要持续追踪的高价值指标

| 频率 | 指标 | 数据源优先级 | 为什么比视频/论文成功率更重要 |
|---|---|---|---|
| 月度/季度 | 客户确认的付费机器人数量、生产小时、站点数 | 客户公告、财报、采购/验收文件 | 区分试点与生产 |
| 月度/季度 | 每千小时干预、近失、停机、关节更换 | 客户/厂商可靠性报告、监管记录 | 连接技术能力与总拥有成本 |
| 季度 | 本体、软件、服务收入及毛利 | 上市公司分部披露 | 判断利润沉淀环节 |
| 每次产品更新 | 持续扭矩、热降额、电池有效班次、维护时间 | 数据表、独立耐久测试 | 检验硬件是否支持连续运营 |
| 每次模型发布 | 累积扰动、未见环境、危险失败和恢复指标 | 官方 benchmark＋第三方复现 | 防止干净基准饱和误导 |
| 半年 | 同一客户续单、跨站点复制所需工程周 | 客户双方披露 | 衡量可复制性和销售效率 |
| 年度 | 安全标准、认证和保险条款 | ISO/监管/IFR/保险机构 | 决定人机共域扩张速度 |

## 对六个必须回答问题的直接回答

1. **最重要变化及与 2025 对比**：九项变化见结论摘要。加速的是后训练、RL、世界模型、数据质量、安全评测、触觉/力觉和执行器建模；VLA 由架构扩张转向系统工程；纯视觉 sim-to-real、干净基准等同泛化、数据量自然产生跨具身能力和演示等同部署等强假设被限定或证伪。
2. **方法边界**：VLA 负责语义和任务先验，IL 负责技能初始化，RL 负责后训练/适应，世界模型负责数据和评测，传统控制负责高频接触/约束，独立安全层负责阻断和介入。边界在协同中更清晰，而非某一路线完全取代另一条。
3. **主要瓶颈**：对齐的真实数据、接触和执行器物理、长时序恢复、扰动泛化、安全责任、执行器热/回差/寿命、耐用触觉、边缘延迟和班次续航。电池是运营瓶颈，但不是近期电芯大市场。
4. **真实验证与演示**：Amazon AMR、BMW/Figure 02 窄任务、GXO/Digit、DHL/Stretch、Locus 和 Intuitive 属于不同程度真实运营；π*0.6、NeuralActuator、Muninn 等是强真实硬件研究；G1 跑酷/滑板、CRAFT Hand 和触觉样机主要是受控演示；世界模型/数据集主要是仿真与基准。
5. **3 个月、1 年、2 年影响**：三个月看复现和指标重构；一年看人形窄任务分化与专用机器人继续扩张；两年看班次级可靠性和三年回收期能否成立。关键硬件需求优先落在计算、视觉、执行器状态、末端和服务，电池 GWh 影响有限。
6. **市场与利润池**：当前最可靠锚为工业安装硬件约 167 亿美元、IFR 服务机器人样本、人形 1.6—1.8 万台 2025 口径及 Intuitive/Symbotic 等公司分部。2027 基准估算为工业硬件约 192 亿美元、物流硬件约 54 亿美元、广义人形硬件约 18 亿美元；人形生产性部署和毛利远小于出货叙事。高质量利润池优先在耗材/服务、软件支持、集成和可靠性数据。

## 二手线索及验证状态

本报告没有把参会者社交媒体分享作为核心证据。唯一进入情景校验的专业媒体线索如下：

| 日期 | 来源 | 来源类型 | 线索 | 一手验证状态 | 置信度 | 在报告中的用途 |
|---|---|---|---|---|---|---|
| 2026-08-10 | Yahoo Finance 转述 Smart Analytics Global | 专业媒体对付费研究的转述 | 2026 上半年人形约 1.91 万台、同比 +272%，全年或约 6 万台 | SAG 公开页面未提供相同粒度的完整底表；未取得公司逐项数据 | **中** | 只用于检查 2027 基准情景是否数量级合理，不作为当前市场事实 |

IDC、Counterpoint、IFR 的数字均来自其自身公开页面/报告，属于研究机构直接发布，但仍受定义和样本限制；因此报告保留冲突，不以“机构权威”替代口径核对。

## 来源清单

以下链接均在 **2026-08-18** 检索或复核。论文成果优先链接 RSS 官方条目，再附项目/代码；产业数据优先链接客户、公司投资者关系或行业组织原文。

### RSS 官方会议材料与 2025 对照

1. RSS 2026，[Accepted Papers](https://roboticsconference.org/program/papers/)：论文、作者、session 和摘要的主索引。
2. RSS 2026，[Awards](https://roboticsconference.org/program/awards/)：Outstanding、Student、Systems 及 finalists。
3. RSS 2026，[Workshops](https://roboticsconference.org/program/workshops/)：32 个 workshop 的最终公开清单。
4. RSS 2026，[Keynotes and Spotlights](https://roboticsconference.org/program/keynotes-spotlights/)：Salah Sukkarieh、Karen Liu、Wenzhen Yuan、Pulkit Agrawal、Hongyang Li 等内容简介。
5. RSS 2026，[Sponsor Demos](https://roboticsconference.org/program/demos/)：厂商展示清单；仅用于确认展示，不用于验证部署。
6. RSS 2026，[Attending RSS](https://roboticsconference.org/attending/attending-rss/) 与 [Call for Participation](https://roboticsconference.org/information/cfp/)：会议日期、地点及官方范围。
7. RSS 2025，[Accepted Papers](https://roboticsconference.org/2025/program/papers/) 与 [Awards](https://roboticsconference.org/2025/program/awards/)：年度对照。
8. RSS 2025，[π0: A Vision-Language-Action Flow Model for General Robot Control](https://roboticsconference.org/2025/program/papers/10/)、[OpenVLA-OFT](https://roboticsconference.org/2025/program/papers/17/)、[UniVLA](https://roboticsconference.org/2025/program/papers/14/)、[Unified World Models](https://roboticsconference.org/2025/program/papers/15/)、[CASHER](https://roboticsconference.org/2025/program/papers/25/)、[ManiSkill3](https://roboticsconference.org/2025/program/papers/21/) 与 [RoboVerse](https://roboticsconference.org/2025/program/papers/22/)：2025 路线基线。

### 关键论文、项目、代码和数据

1. RSS 2026，[FlashSAC](https://roboticsconference.org/program/papers/99/)；[项目页](https://holiday-robot.github.io/FlashSAC/)；[代码](https://github.com/Holiday-Robot/FlashSAC)。
2. RSS 2026，[Muninn](https://roboticsconference.org/program/papers/160/)；[代码](https://github.com/gokulp01/Muninn)。
3. RSS 2026，[NeuralActuator](https://roboticsconference.org/program/papers/159/)；[项目页](https://frank-zy-dou.github.io/projects/NeuralActuator/index.html)；[模型与数据](https://huggingface.co/frankzydou/NeuralActuator)。
4. RSS 2026，[π*0.6 / RECAP](https://roboticsconference.org/program/papers/87/)；[论文 PDF](https://www.physicalintelligence.company/download/pistar06.pdf)。
5. RSS 2026，[PolaRiS](https://roboticsconference.org/program/papers/62/)；[项目页](https://polaris-evals.github.io/)；[环境代码](https://github.com/polaris-evals/compose-environments)。
6. RSS 2026，[MolmoSpaces](https://roboticsconference.org/program/papers/91/)；[代码与数据入口](https://github.com/allenai/molmospaces)。
7. RSS 2026，[EgoVerse](https://roboticsconference.org/program/papers/92/)；[代码与数据入口](https://github.com/GaTech-RL2/EgoVerse)。
8. RSS 2026，[GS-Playground](https://roboticsconference.org/program/papers/93/)；[代码与发布状态](https://github.com/discoverse-dev/gs_playground)。
9. RSS 2026，[RISE](https://roboticsconference.org/program/papers/12/)；[论文](https://arxiv.org/abs/2602.11075)。
10. RSS 2026，[Interactive World Simulator](https://roboticsconference.org/program/papers/18/)；[代码、模型与数据](https://github.com/WangYixuan12/interactive_world_sim)。
11. RSS 2026，[Ψ0](https://roboticsconference.org/program/papers/21/)；[代码与数据](https://github.com/physical-superintelligence-lab/Psi0)。
12. RSS 2026，[TactAlign](https://roboticsconference.org/program/papers/6/) 与 [Human-to-Robot Embodiment-Agnostic Representation](https://roboticsconference.org/program/papers/72/)。
13. RSS 2026，[HAIC / Humanoid Adaptive Interactions](https://roboticsconference.org/program/papers/13/) 与 [Perceptive Humanoid Parkour](https://roboticsconference.org/program/papers/20/)。
14. RSS 2026，[Rapid Real-World Quadrotor Adaptation](https://roboticsconference.org/program/papers/135/)。
15. RSS 2026，[Minimalist Compliance](https://roboticsconference.org/program/papers/123/)、[Tune to Learn](https://roboticsconference.org/program/papers/139/)、[Force Policy](https://roboticsconference.org/program/papers/128/) 与 [GPU Robust MPC](https://roboticsconference.org/program/papers/103/)。
16. RSS 2026，[LIBERO-X](https://roboticsconference.org/program/papers/97/)、[OopsieVerse](https://roboticsconference.org/program/papers/98/)、[UPS](https://roboticsconference.org/program/papers/142/) 与 [TAIL-Safe](https://roboticsconference.org/program/papers/207/)。
17. [CRAFT Hand 项目页](https://craft-hand.github.io/) 与 [论文](https://arxiv.org/abs/2603.12120)。
18. RSS 2026，[LightTact](https://roboticsconference.org/program/papers/193/) 与 [Electrical Capacitance Tomography Sensor](https://roboticsconference.org/program/papers/197/)。

### 客户、产品和真实部署材料

1. BMW Group，2026-02，[BMW Group to deploy humanoid robots in production in Germany for the first time](https://www.press.bmwgroup.com/united-kingdom/article/detail/T0455870EN_GB/bmw-group-to-deploy-humanoid-robots-in-production-in-germany-for-the-first-time)：Figure 02 的美国生产数据及 Leipzig 后续部署。
2. Figure，[Production at BMW](https://www.figure.ai/news/production-at-bmw)：动作节拍和厂商目标；目标与实绩分开使用。
3. Amazon，2025-07，[Amazon deploys its 1 millionth robot](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model)：车队数量、站点和 DeepFleet；以及 2026-02 更新的 [Blue Jay](https://www.aboutamazon.com/news/operations/new-robots-amazon-fulfillment-agentic-ai) 状态。
4. Boston Dynamics / DHL，2026-02，[DHL signs MOU for additional 1,000 robot deployment](https://bostondynamics.com/news/dhl-signs-mou-for-additional-1000-robot-deployment/)：Stretch 商业历史、吞吐口径与 MOU。
5. GXO / Agility Robotics，2024-06，[Industry-first multi-year agreement](https://investors.gxo.com/news-releases/news-release-details/gxo-signs-industry-first-multi-year-agreement-agility-robotics)：Digit RaaS 与 Spanx 场景。
6. Mercedes-Benz / Apptronik，[Humanoid robots at Mercedes-Benz Digital Factory Campus](https://group.mercedes-benz.com/unternehmen/produktion/produktionsnetzwerk/mbdfc-humanoide-roboter.html)：低两位数百万欧元投入及试验/数据定位。
7. Locus Robotics，[The next era of autonomous fulfillment](https://locusrobotics.com/blog/next-era-autonomous-fulfillment)：供应商披露的装机、站点、拣选和运行小时。
8. Unitree，[G1 产品页](https://www.unitree.com/cn/g1/)：价格、电池和产品限制说明。
9. Agility Robotics，[Digit product innovations](https://www.agilityrobotics.com/content/agility-robotics-announces-new-innovations-for-market-leading-humanoid-robot-digit)：续航和自动回充。
10. NVIDIA，2025-08，[Jetson Thor technical introduction](https://developer.nvidia.com/blog/introducing-nvidia-jetson-thor-the-ultimate-platform-for-physical-ai/) 与 [commercial availability](https://nvidianews.nvidia.com/news/nvidia-blackwell-powered-jetson-thor-now-available-accelerating-the-age-of-general-robotics)：规格和价格锚。

### 市场、行业组织和公司财务材料

1. IFR，2026-01，[Top 5 Global Robotics Trends 2026](https://ifr.org/ifr-press-releases/news/top-5-global-robotics-trends-2026)；[World Robotics 2025 Industrial Robots Executive Summary](https://ifr.org/img/worldrobotics/Executive_Summary_WR_2025_Industrial_Robots.pdf)；[World Robotics 2025 Service Robots Executive Summary](https://ifr.org/img/worldrobotics/Executive_Summary_WR_2025_Service_Robots.pdf)；[2025—2028 installation forecast](https://ifr.org/news/global-robot-demand-in-factories-doubles-over-10-years/1st-quarterly-newsletter-2016)。
2. IFR，2026-06，[Executive Roundtable market presentation](https://ifr.org/downloads/press_docs/2026_06_24_IFR_Executive_Roundtable_market_presentation.pdf)；IFR，2025，[Humanoids position infographic](https://ifr.org/downloads/press_docs/Humanoids_Position_Infograph_2025.pdf)。
3. IDC，2026，[Humanoid Robotics Commercialization 2026](https://www.idc.com/resource-center/blog/humanoid-robotics-commercialization-2026/)；Counterpoint，2026，[Global Humanoid Robot Installations Reach 16,000 Units in 2025](https://counterpointresearch.com/en/insights/Global-Humanoid-Robot-Installations-Reach-16%2C000-Units-in-2025-as-Mass-Production-Picks-Pace)。
4. Yahoo Finance，2026-08-10，[Chinese companies winning humanoid robot shipments](https://finance.yahoo.com/technology/ai/articles/chinese-companies-winning-humanoid-robot-003124500.html)：SAG 数据二手线索，未作为一手事实。
5. Intuitive Surgical，2026-07，[Second-quarter 2026 earnings](https://isrg.intuitive.com/news-releases/news-release-details/intuitive-announces-second-quarter-earnings-6)。
6. Symbotic，2026-05，[Second-quarter fiscal 2026 results](https://ir.symbotic.com/news-releases/news-release-details/symbotic-reports-second-quarter-fiscal-year-2026-results)。
7. ABB，2025-10，[ABB to divest Robotics division to SoftBank Group](https://new.abb.com/news/detail/129776/abb-to-divest-robotics-division-to-softbank-group)。
8. Teradyne，2026-07，[Second-quarter 2026 results](https://investors.teradyne.com/news-events/press-releases/detail/445/teradyne-reports-second-quarter-2026-results)。
9. Hesai，2026-05，[First-quarter 2026 results](https://investor.hesaitech.com/news-releases/news-release-details/hesai-group-reports-first-quarter-2026-unaudited-financial)；2026-03，[Full-year 2025 results](https://investor.hesaitech.com/news-releases/news-release-details/hesai-group-reports-fourth-quarter-and-full-year-2025-unaudited)。
10. FANUC，2026-07，[FY2026 first-quarter reference material](https://www.fanuc.co.jp/en/ir/announce/pdf/2026/reference202606_e.pdf)。
11. Harmonic Drive Systems，[Top Message / management policy](https://www.hds.co.jp/english/ir/management_policy/top_message/)；Nabtesco，2026-02，[Long-term vision and medium-term plan](https://www.nabtesco.com/en/news/20260218-17670/)。

## 最终判断

RSS 2026 对机器人产业最重要的启示，是把“智能上限”和“商业下限”同时暴露出来。智能上限确实提高：更快的 RL、更好的长时序后训练、更可交互的世界模型、更强的人形运动和更低成本的灵巧硬件已经出现。商业下限也更清晰：接触物理、执行器热和寿命、累积误差、安全介入、班次续航、维护网络和客户回收期没有被一个更大的模型消除。

因此，未来一年最可信的投资主线不是笼统的“所有人形供应链”，而是三类可验证对象：

1. **已有规模和利润的机器人闭环**：医疗耗材/服务、工业本体、物流自动化和车队软件；
2. **被 RSS 2026 明确抬升的工程瓶颈**：后训练/仿真评测、执行器状态与热模型、力觉/触觉、末端执行器、边缘推理和安全系统；
3. **以客户数据而非视频定价的人形公司**：只有当生产小时、干预、维护、续单和毛利同时改善，出货量才应进入长期利润模型。

最关键的证伪问题只有一句：**机器人是否能在客户现场，以可接受的人工介入和维护成本，连续完成足够多的付费工作？** RSS 2026 让完成这件事的技术路径更清楚，但截至 2026-08-18，除了少数专用机器人和封闭场景，行业尚未给出普遍肯定的答案。
