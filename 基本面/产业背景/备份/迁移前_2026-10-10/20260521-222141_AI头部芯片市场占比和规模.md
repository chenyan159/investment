# 全球 AI 芯片路线图与 2026-2027 产能释放预测

截至日期：2026-05-08  
口径：本报告把“产能释放金额”定义为 AI 加速器芯片、加速器模块、rack-scale 计算托盘以及直接绑定的计算互连/内存子系统的发货或内部转移价值，单位为十亿美元。不包括数据中心土建、电力接入、长期云服务收入，也尽量不重复计算服务器 OEM 加价。对 Google TPU、AWS Trainium、Meta MTIA、Microsoft Maia、OpenAI/Broadcom 等自用 ASIC，按“等效外部采购/内部转移价”估算。

## 1. 摘要

2026 年的主线仍是 NVIDIA Blackwell/Blackwell Ultra 放量，Rubin 从下半年进入首批量产；同时，Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA、OpenAI/Broadcom 等 hyperscaler ASIC 开始从“替代 GPU 的局部补充”变成“单独的产能池”。中国市场则由 Huawei Ascend、Cambricon、Alibaba T-Head、Baidu Kunlun 以及若干 GPU 初创公司承接被出口管制挤出的需求。

三个核心判断：

| 判断 | 务实情形 | 乐观情形 | 极度乐观情形 |
|---|---:|---:|---:|
| 2026 全球 AI 计算芯片/模块产能释放金额 | 约 $300B-$360B | 约 $390B-$470B | 约 $520B-$650B |
| 2027 全球 AI 计算芯片/模块产能释放金额 | 约 $430B-$520B | 约 $590B-$720B | 约 $850B-$1,050B |
| 2026-2027 最大约束 | HBM3E/HBM4、CoWoS/先进封装、液冷/供电、客户机房上电节奏 | HBM4 多供应商验证顺利，CoWoS 外包与 OSAT 承接加速 | GW 级订单按公告节奏快速转化，推理需求继续指数式扩张 |

这些区间与公开资料的关系：

- Gartner 预计 2026 全球半导体收入 $1.320T，2027 为 $1.555T；其中 AI 半导体约占 2026 总量 30%，即约 $396B，并且 hyperscaler AI 基建支出 2026 年增长超过 50%。这给“芯片级收入”提供了上限校验，但 Gartner 口径包含内存、网络、存储控制等更广类别。
- NVIDIA 在 GTC 2026 称 Blackwell 与 Vera Rubin 相关产品到 2027 年有“至少 $1T”收入机会；本报告把它放在乐观到极度乐观区间，不直接作为基准收入。
- Broadcom 在 2026 年初表示 2027 AI 芯片收入有望超过 $100B，且六大客户包括 Google、Meta、Anthropic、OpenAI 以及可能的 Fujitsu/ByteDance；这验证 ASIC 份额上移。
- TrendForce 预计 2026 NVIDIA 高端 GPU 出货结构中 Blackwell 占比由 61% 升至 71%，Rubin 因 HBM4、CX9、功耗与液冷调校等因素从 29% 下修至 22%。这意味着 2026 “真正放量”的仍是 B300/GB300，而 Rubin 的 2026 收入更偏尾端。
- TSMC CoWoS 月产能公开估计到 2026 年底约 11.5-14 万片、2027 年约 17 万片；HBM4 三大供应商预计 2026 Q2 前后完成 NVIDIA Rubin 验证。两者是所有高端 GPU/ASIC 的共同阀门。

## 2. 方法与校验框架

| 校验角度 | 使用方法 | 对预测的约束 |
|---|---|---|
| 自上而下半导体收入 | 以 Gartner 2026/2027 总半导体和 AI 半导体占比为锚，扣除通用 DRAM/NAND、网络、CPU、存储控制等非加速器部分 | 2026 务实情形不宜远高于 $400B 级别；极度乐观才允许把 rack 内网络和内存价值更多计入 |
| 厂商订单与路线图 | NVIDIA $1T Blackwell/Rubin 机会、Broadcom 2027 $100B AI 芯片目标、Meta >1GW MTIA、OpenAI 10GW Broadcom、AWS Rainier >50 万到 >100 万 Trainium2 | 决定乐观和极度乐观上沿 |
| 供应链瓶颈 | CoWoS/SoIC、HBM3E/HBM4、ABF/BT 载板、液冷 CDU/冷板、800G/1.6T 光模块、CPO | 决定务实情形下的出货延迟和芯片组合 |
| 功率/GW 换算 | 1GW IT power 大致对应 60-110 万颗高端 ASIC/GPU 等效芯片，取决于单芯片功耗、冗余、CPU/网络/冷却 overhead | 检查 Meta、OpenAI、Anthropic、Google 等 GW 级承诺是否落入合理单位数量 |
| HBM stack 换算 | 高端 GPU/ASIC 通常 6-12 个 HBM stack；HBM4 初期良率和基底 die 供应决定 Rubin/MI400/TPU8 节奏 | 2026 下半年 Rubin/MI400/TPU8 放量不宜过激 |

## 3. 主要 AI 芯片全景清单与产能释放预测

单位：十亿美元。数字为产能释放金额区间，不是公司总收入；自用 ASIC 用等效内部转移价。阶段以 2026-05-08 可得公开资料判断。

| 公司/生态 | 芯片/平台 | 2026-05 阶段 | 主要用途 | 2026 务实 | 2026 乐观 | 2026 极度乐观 | 2027 务实 | 2027 乐观 | 2027 极度乐观 | 关键依据/校验 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| NVIDIA | H100/H200/H20/Hopper 系列 | 在产成熟，Hopper 占比下滑 | 训练、推理、存量扩容 | 8 | 14 | 22 | 2 | 6 | 12 | TrendForce 预计 Hopper 2026 高端出货占比降至约 7%；中国 H20/H200 受政策影响大 |
| NVIDIA | B200/GB200 Blackwell | 大规模量产，部分订单延续到 2026 下半年 | 训练、推理 | 25 | 45 | 70 | 8 | 20 | 35 | Blackwell 平台成熟度高，但被 GB300 挤占新增份额 |
| NVIDIA | B300/GB300 Blackwell Ultra | 大规模量产，2026 主力 | 推理、长上下文、后训练 | 90 | 130 | 180 | 45 | 80 | 130 | NVIDIA 官方 GB300 NVL72；TrendForce 称 2026 Blackwell 占高端 GPU 出货 >70%，由 GB300/B300 主导 |
| NVIDIA | Vera Rubin / Rubin GPU / VR NVL72 | 已宣布 full production，2026 H2 出货 | 下一代训练、agentic inference | 15 | 35 | 70 | 110 | 180 | 280 | NVIDIA 官方称 Vera Rubin 七类芯片 full production、合作伙伴 2026 H2 可用；TrendForce 下修 Rubin 2026 份额至 22% |
| NVIDIA | Rubin Ultra / Kyber NVL144 | 设计/工程导入，预计 2027 H2 | 2027 下一代 rack-scale | 0 | 2 | 8 | 15 | 45 | 90 | 公开路线图指向 2027 H2；HBM4E 与 NVLink 7 是主要风险 |
| NVIDIA/Groq | Groq 3 LPU / LPX rack | 2026 H2 可用，NVIDIA 平台化 | 低延迟 decode/agentic inference | 2 | 5 | 9 | 5 | 11 | 22 | NVIDIA 官方称 LPX 256 LPU/rack、2026 H2 可用；TrendForce 称 LPU 2026 需求数十万、2027 翻倍 |
| NVIDIA | RTX PRO 4500/6000、T4000/T5000、边缘/工作站 AI | 量产/扩产 | 中低端数据中心、边缘推理、物理 AI | 5 | 10 | 18 | 8 | 18 | 35 | TrendForce 称中低端产品 2026 出货占比升至 32% 以上 |
| AMD | MI300X/MI325X/MI300A | 成熟在产，逐步让位 | 训练、HPC、云推理 | 3 | 6 | 10 | 1 | 3 | 6 | MI325X 2024-2025 放量，2026 转为存量与价格敏感客户 |
| AMD | MI350X/MI355X/MI350P | 在产放量 | 训练、推理、企业 PCIe | 12 | 22 | 36 | 5 | 12 | 25 | AMD 官方 MI350 系列，HBM3E、MXFP4/MXFP6，企业部署门槛低于 rack-scale |
| AMD | MI430X/MI440X/MI455X、Helios/MI400 | 2026 H2 目标放量，早期系统验证 | Rack-scale 训练/推理、主权 AI | 2 | 8 | 18 | 18 | 40 | 75 | AMD CES 2026 确认 Helios、MI400 系列、MI455X；Meta-AMD up to 6GW 协议从 2026 H2 首批部署 |
| AMD | MI500 系列 | 设计阶段，计划 2027 | 下一代 2nm/HBM4E | 0 | 0 | 1 | 2 | 8 | 22 | AMD 称 MI500 2027、CDNA 6、2nm、HBM4E，2027 更多是试产/首批 |
| Intel | Gaudi 3 | 在产但需求较弱 | 以太网 AI 加速、成本敏感训练/推理 | 0.4 | 1 | 2 | 0.1 | 0.5 | 1.5 | Intel 官方仍销售 Gaudi 3；Falcon Shores 取消削弱客户信心 |
| Intel | Jaguar Shores / 下一代 AI rack solution | 设计/测试车阶段 | 2027 以后 AI/HPC | 0 | 0 | 0.5 | 1 | 4 | 10 | Falcon Shores 取消后转向 Jaguar Shores；可能使用 HBM4、EMIB-T/Foveros 类封装 |
| Google/Broadcom | TPU v6e/Trillium、v5p 存量 | 在产/云端部署 | 训练与推理 | 5 | 9 | 15 | 2 | 5 | 10 | Google Cloud 存量 TPU 队列，逐步被 Ironwood 与 TPU8 替代 |
| Google/Broadcom | TPU v7 Ironwood | 大规模部署/云端 GA | 推理优先，也可训练 | 18 | 32 | 55 | 28 | 50 | 85 | Google 官方：192GB HBM、7.37TB/s；Anthropic 2026 TPU 扩容最高约 100 万级别 |
| Google/Broadcom | TPU 8t / TPU 8i | 已发布，早期导入/设计验证 | 8t 训练、8i 推理 | 0.5 | 2 | 6 | 8 | 25 | 55 | Google Cloud Next 2026 发布第八代 TPU，训练/推理分化；2nm/HBM 供应决定节奏 |
| AWS | Trainium2 | 大规模部署，Rainier 主力 | Claude 训练/推理 | 15 | 25 | 40 | 5 | 12 | 22 | AWS 官方：Project Rainier 近 50 万颗 Trainium2，Anthropic 年底目标 >100 万颗 |
| AWS | Trainium3 / Trn3 UltraServer | GA/放量初期 | 训练、推理 | 6 | 12 | 24 | 20 | 35 | 60 | AWS 官方：Trn3 UltraServer 144 颗 Trainium3、362 FP8 PFLOPs、4.4x Trainium2 compute |
| AWS | Trainium4 | 设计阶段 | 下一代训练/推理，与 NVLink Fusion | 0 | 0 | 1 | 1 | 5 | 15 | AWS 官方称正在开发 Trainium4，目标 FP4 6x、FP8 3x、带宽 4x |
| Microsoft | Maia 100 | 小规模在产/存量 | Azure/OpenAI/Copilot 推理 | 0.5 | 1 | 2 | 0.2 | 0.5 | 1 | 主要被 Maia 200 替代 |
| Microsoft | Maia 200 | 量产导入 Azure | 推理 | 4 | 8 | 15 | 10 | 22 | 45 | Microsoft 官方：TSMC 3nm、216GB HBM3E、7TB/s、272MB SRAM，推理性价比提升 30% |
| Meta/Broadcom | MTIA 300 | 已在生产 | 推荐/排序训练，部分推理 | 1.5 | 3 | 6 | 2 | 5 | 10 | Meta 官方称 MTIA 300 已生产，数十万 MTIA 存量部署 |
| Meta/Broadcom | MTIA 400/450/500 | 2026-2027 分批部署 | GenAI inference 为主 | 1 | 4 | 10 | 10 | 25 | 55 | Meta/Broadcom 公告：超过 1GW 首期，未来多 GW；四代 MTIA 两年内推出 |
| OpenAI/Broadcom | OpenAI 自研 accelerator | 设计完成/2026 H2 rack 起步 | 推理优先，OpenAI/伙伴数据中心 | 0.5 | 2 | 5 | 8 | 25 | 60 | OpenAI/Broadcom 官方：10GW，2026 H2 开始，2029 完成；Broadcom 称 2027 OpenAI 芯片 >1GW |
| Broadcom 其他 XPU | ByteDance/Fujitsu/Anthropic 等定制 ASIC | 设计/小规模试产到量产 | 定制训练/推理 | 3 | 8 | 18 | 12 | 35 | 80 | Broadcom 2027 AI 芯片 >$100B 目标；部分已含 Google/Meta/OpenAI，注意避免重复 |
| Huawei | Ascend 910B/910C、CloudMatrix/Atlas 900 A3 | 大规模量产，受 SMIC/HBM 约束 | 中国训练/推理替代 | 8 | 14 | 24 | 5 | 10 | 18 | Ascend 910C Q1 2025 量产；系统靠大规模互连弥补单芯片差距 |
| Huawei | Ascend 950PR/950DT、Atlas 950 | 950PR 2026 Q1，950DT 2026 Q4 路线图 | 推理/训练、超节点 | 4 | 9 | 18 | 14 | 28 | 55 | Huawei 路线图：950PR/DT、内置自研 HBM、Atlas 950 SuperPoD/Cluster |
| Huawei | Ascend 960/970 | 设计阶段，960 预计 2027 Q4 | 下一代中国 AI 集群 | 0 | 0 | 1 | 2 | 8 | 20 | Huawei 路线图：960 Q4 2027、970 Q4 2028 |
| Cambricon | Siyuan/MLU 590 | 在产放量 | 中国训练/推理 | 2.5 | 4.5 | 8 | 2 | 4 | 7 | TrendForce/Bloomberg：2026 目标约 50 万颗，含 590/690；SMIC N+2 约束 |
| Cambricon | Siyuan/MLU 690 | 测试/小规模试产，2026 H2 可能放量 | 下一代中国 AI 加速 | 0.5 | 1.5 | 3.5 | 2 | 5 | 10 | 大规模量产可能推迟到 2026 H2 后 |
| Alibaba T-Head | Zhenwu 810E / PPU、Hanguang 后继 | 已超过 10 万颗级别交付/扩张 | 云推理、训练/推荐 | 2 | 4 | 8 | 3 | 7 | 15 | SCMP：Zhenwu 810E 已交付 >10 万颗；T-Head 可能分拆上市 |
| Baidu Kunlunxin | Kunlun P800/M100/M300 | P800 存量，M100 2026，M300 2027 | 推理、训练/多模态 | 0.5 | 1.5 | 3 | 2 | 5 | 12 | Baidu 路线图：M100 2026、M300 2027，Tianchi 超节点 |
| Biren | BR100/BR104 与后继 | 小规模在产/国产替代 | GPGPU 训练/推理 | 0.4 | 1 | 2 | 0.8 | 2 | 5 | IPO 后融资改善，先进制程/HBM/出口限制仍是瓶颈 |
| Iluvatar CoreX | Tiangai/Big Island 与后继 | 在产/路线图 | 中国 GPGPU | 0.4 | 1 | 2 | 0.8 | 2.5 | 6 | 中国首批量产通用 GPU 平台之一，2026-2028 路线图对标 H200/B200 |
| MetaX/Moore Threads/Enflame/Hygon | C500/MTT/CloudBlazer/DCU 等 | 小规模量产、试点集群 | 国产替代、推理/通用 GPU | 0.8 | 2 | 5 | 1.5 | 5 | 12 | 中国国产供应链扩张，但软件生态、良率、HBM 与先进节点是核心限制 |
| Cerebras | WSE-3 / CS-3 | 小批量生产、项目制交付 | Wafer-scale 训练/推理 | 1 | 2 | 4 | 1.5 | 4 | 9 | WSE-3 4 万多 mm²、4T transistor；客户集中度高 |
| SambaNova | SN40L/SN50 | 小规模生产/新一代融资后导入 | 企业/主权推理 | 0.4 | 1 | 2.5 | 0.8 | 2.5 | 6 | SN40L 已商品化，SN50 面向更快推理，SoftBank 等客户 |
| Tenstorrent | Wormhole/Blackhole/Galaxy | 2026 GA，规模仍早期 | 开放生态推理/边缘到集群 | 0.3 | 0.8 | 2 | 0.8 | 2 | 5 | Galaxy Blackhole 32 芯片系统 GA；软件生态仍需验证 |
| d-Matrix/Etched/MatX/Rebellions/Furiosa 等 | 推理 ASIC/专用 LLM 芯片 | 小规模试产/设计 | 专用推理、低延迟、低成本 | 0.3 | 1 | 3 | 1 | 4 | 12 | 主要靠单一客户或云服务切入，2027 前仍偏小体量 |
| Edge/PC/车端 AI SoC | Qualcomm/Apple/NVIDIA/AMD/Intel/Tesla 等 NPU/AI SoC | 大规模量产但单价较低 | 端侧推理、车载、机器人 | 8 | 15 | 25 | 12 | 25 | 45 | 单位数量最大，但与数据中心 AI 加速器口径不同；此处只计高算力 AI SoC 增量 |
| Tesla | AI5/AI6/Dojo3 | AI5 tape-out/样片，AI6/Dojo3 设计 | 车端 FSD、机器人、训练集群 | 0 | 0.5 | 2 | 3 | 8 | 18 | AI5 预计 2027 高量产，TSMC/Samsung 双源；AI6/Dojo3 更靠后 |

## 4. 2026 至 2027 年初出货量最大的 12 种芯片/平台技术拆解

排序按“2026-2027 年初可见的等效芯片出货数量 + 价值权重”综合判断。对 rack-scale 平台，一颗 GPU/LPU/TPU/ASIC 按一颗加速器芯片计；NVIDIA GB300/GB200 按 Blackwell GPU 颗数计，不按整 rack 计。

| 排名 | 芯片/平台 | 预计出货逻辑 | 2026 务实/乐观/极度乐观 | 2027 初延续性 | 光刻/掩膜 | 外部存储与片内存储 | 光互联/CPO | AI 芯片级供电 | 制造设备与检测 | 散热 | 计算芯片基板与封装 | 超级电容器/飞轮储能 |
|---:|---|---|---:|---|---|---|---|---|---|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | 2026 Blackwell 主力，GB300/B300 领先出货结构 | $90/$130/$180B | 2027 上半年仍大量交付 | TSMC 4NP/先进 DUV+EUV，多 reticle 级芯片/封装协同；掩膜成本高、工程改版周期长 | 每 GPU 最高 288GB HBM3E；rack 内 Grace LPDDR 与 NVLink 共享内存池 | Rack 内以铜/NVLink 为主，scale-out 用 800G/1.6T 光模块；CPO 主要在 Spectrum-6 代开始上量 | 高电流 VRM、48V 机柜供电、动态功率调度；瞬态负载由板级/封装去耦承担 | EUV scanner、CoWoS-L、HBM bonding、ABF 载板；检测重点是 HBM known-good-die、interposer、NVLink/SerDes burn-in | 全液冷，冷板/CDU 成为交付节奏约束 | CoWoS-L/大尺寸 ABF，GB300 NVL72 机柜级集成 | 数据中心侧用 UPS/电池为主；NVIDIA DSX 提到 rack-level energy storage，超级电容可用于毫秒级功率平滑，飞轮用于园区级短时稳频 |
| 2 | AWS Trainium2 | Project Rainier 近 50 万颗，Anthropic 目标 >100 万颗 | $15/$25/$40B | 2027 被 Trainium3 接续但仍有存量扩容 | 先进制程未完全公开，通常由 AWS/Annapurna 与代工厂定制；掩膜成本被大规模自用摊薄 | HBM + NeuronLink；单 UltraServer 64 颗 Trainium2 | 以 EFA/以太网 scale-out，rack 内 NeuronLink；未见 CPO 作为主特征 | 自研服务器电源架构，强调垂直集成和低延迟 fabric | 代工、先进封装、HBM 测试由供应链完成；AWS 侧做系统级 burn-in | 液冷/风液混合，Rainier 多数据中心部署对冷却工程要求高 | Trainium2 UltraServer，64 芯片 scale-up | GW 级部署需要园区级储能；飞轮/超级电容更偏电网瞬态和 UPS 补充，不是芯片 BOM 核心 |
| 3 | Google TPU v7 Ironwood | Google 自用 + Cloud + Anthropic TPU 扩容，最高百万级目标 | $18/$32/$55B | 2027 继续放量并被 TPU8 替代部分新需求 | 公开资料指向先进 3nm 级别；与 Broadcom/TSMC 生态强相关 | 192GB HBM、7.37TB/s；片内 SRAM/矩阵阵列为推理优化 | TPU pod scale-up/scale-out 自研互连；云端以光模块为主，CPO 不是已公开核心卖点 | Google 从机柜到数据中心协同供电，AI Hypercomputer 优化整体利用率 | HBM3E 测试、wafer probe、package test、pod 级互连测试 | 大规模液冷趋势明显，Google 自有数据中心可内化热设计 | 2.5D 先进封装、大尺寸有机载板 | Google 数据中心已有电力调度经验；超级电容/飞轮更可能用于园区侧功率质量 |
| 4 | NVIDIA B200/GB200 Blackwell | 既有订单延续，成本敏感客户继续采购 | $25/$45/$70B | 2027 逐步降为存量/低价配置 | TSMC 4NP，双 die Blackwell 设计 | HBM3E，GB200 NVL72 rack 内形成统一 GPU fabric | NVLink 5/铜互连为主，光模块用于 scale-out | 48V rack、板级 VRM、高速负载瞬态管理 | CoWoS、HBM3E KGD、NVSwitch 检测 | 液冷为主，部分 HGX 形态仍有风冷/风液 | CoWoS-L/S，NVL72 rack 级封装系统 | 与 GB300 类似，储能主要在 rack/园区侧 |
| 5 | Huawei Ascend 910C/950PR/950DT | 中国国产替代第一梯队，系统级 SuperPoD 弥补单芯片差距 | $12/$23/$42B | 2027 950/960 延续并上量 | SMIC N+2/N+3 级 DUV 多重曝光为主；掩膜层数、重工和良率压力高 | 910C 约 3.2TB/s 带宽；950 系列强调自研 HBM/低精度格式 | Huawei 自研 UB/互连，SuperPoD/Cluster 强依赖电互连和光模块 | 高功耗下以板级供电和大规模并联弥补制程弱势 | DUV scanner、刻蚀/沉积/量测受设备限制；HBM 与先进封装测试是瓶颈 | 液冷/风液结合；超节点密度提高后液冷必需 | 2.5D/先进封装、本土 ABF/载板能力爬坡 | 中国 AI 园区电力波动与并网压力大，飞轮/超级电容可用于短时稳频和削峰，但部署取决于园区 EPC |
| 6 | Cambricon Siyuan/MLU 590/690 | 2026 目标约 50 万颗，ByteDance 等订单驱动 | $3/$6/$11.5B | 2027 690 若顺利会接棒 | SMIC N+2 级 DUV；690 可能受 N+3/N+4 良率约束 | 590/690 使用 HBM，片内 SRAM/MLU-Link 改善系统效率 | MLU-Link + 数据中心光模块；无 CPO 主流应用 | 单卡功耗低于顶级 GPU，但国产电源/VRM 与大规模互连仍需验证 | SMIC 先进节点、HBM 封装、OAM 模块测试；低良率会放大测试成本 | 风冷到液冷过渡，OAM 集群需液冷选项 | OAM 模块，2.5D 封装/有机载板 | 大规模国产集群若上 GW，储能需求同华为，但芯片侧不直接受益 |
| 7 | AMD MI350X/MI355X/MI350P | 2026 AMD 最确定放量产品，PCIe 与 UBB 形态覆盖企业 | $12/$22/$36B | 2027 被 MI400 接替但仍有企业需求 | 公开资料未逐项披露；市场普遍按 TSMC 3nm/先进封装看待 | HBM3E，MI355X 平台约 2.3TB HBM3E/8 GPU；支持 MXFP4/MXFP6 | Infinity Fabric/以太网 scale-out；非 CPO 主线 | 8-GPU UBB 高电流供电，企业 PCIe 卡相对易部署 | HBM3E 测试、ROCm 兼容性测试、UBB 系统 burn-in | 液冷选项增加，PCIe 形态可风冷/风液 | 2.5D 封装、OAM/UBB/PCIe 多形态 | 主要影响数据中心级电力架构，不是芯片 BOM |
| 8 | AWS Trainium3 | 3nm Trainium3 UltraServer GA，144 芯片 scale-up | $6/$12/$24B | 2027 主力放量 | AWS 称 3nm；掩膜/NRE 高但由 AWS 自用量摊薄 | HBM3E 级别，UltraServer 4x 内存带宽提升 | NeuronSwitch-v1、Neuron Fabric；Trainium4 计划支持 NVLink Fusion | 强调 4x 能效，rack 内供电与网络垂直集成 | 3nm wafer、HBM、先进封装和系统级测试；AWS 控制系统栈 | 高密度训练/推理需要液冷 | Trn3 UltraServer 144 芯片系统 | 大规模云部署同样需要园区级 UPS/储能，飞轮更可能用于电网侧 |
| 9 | Meta MTIA 300/400/450/500 | Meta 已部署数十万 MTIA，2026-2027 四代迭代 | $2.5/$7/$16B | 2027 受 >1GW Broadcom 协议推动 | Broadcom XPU 平台，TSMC 先进制程；MTIA 500 可能迈向更先进节点 | 400/450/500 强调 compute、内存带宽和效率提升；具体 HBM 未完全公开 | Broadcom Ethernet/SerDes 强项；未来 CPO/硅光可接入 | Meta OCP rack 标准，供电设计围绕低 TCO 推理 | Broadcom 设计、先进封装、网络芯片、系统测试一体化 | OCP 机架与液冷/风液混合；GenAI inference 密度上升后液冷占比提高 | XPU chiplet/先进封装，OCP rack 可复用 | Meta >1GW 首期需要园区侧储能和功率调度；超级电容用于瞬态平滑可能性高 |
| 10 | Microsoft Maia 200 | Azure 推理自研芯片，服务 Copilot/OpenAI/Foundry | $4/$8/$15B | 2027 扩大 Azure 内部部署 | TSMC 3nm，>140B transistor 级别；掩膜成本高但推理规模大 | 216GB HBM3E、7TB/s、272MB SRAM | Azure 后端网络 + scale-up interconnect；未公开 CPO 为核心特性 | 750W SoC TDP，第二代闭环液冷 HEU，板级/封装去耦要求高 | 3nm wafer、HBM3E、package test、Azure rack burn-in | Microsoft 明确闭环液冷 | 先进封装 + HBM3E + Azure rack 集成 | Azure 数据中心可用电池/UPS/需求响应；飞轮/超级电容偏设施层 |
| 11 | Alibaba T-Head Zhenwu 810E/PPU | 已交付超过 10 万颗，国产云需求推动 | $2/$4/$8B | 2027 继续在中国云端扩容 | 可能使用 SMIC N+2/国产可得先进节点；DUV 多重曝光良率是约束 | 面向训练/推理，HBM/高带宽显存配置未完全公开 | 国内以太网/光模块 + 自研集群互连 | 面向云端 PPU，供电密度低于顶级 rack GPU 但规模大 | 国内先进节点、封装、测试、整机适配 | 10k 卡集群级别需要液冷/风液混合 | ASIC/PPU 模块，国产载板和封装爬坡 | 集群规模扩大后需要园区储能，同上 |
| 12 | AMD MI400/MI455X Helios | 2026 H2 首批，Meta up to 6GW 是最大潜在拉动 | $2/$8/$18B | 2027 可能成为 AMD 主力 | 市场公开资料指向 TSMC 2nm/3nm 组合；MI400 compute chiplet 可能为 N2 级别 | MI455X 目标 432GB HBM4、约 19.6TB/s；Helios rack 约 31TB HBM4 | UALink/以太网 scale-up、Pensando/Vulcano NIC；CPO 不是首批核心 | 72 GPU rack，HBM4 高功耗，48V/高压直流和动态功率管理很关键 | N2、HBM4、CoWoS-L/先进封装、Samsung HBM4 供应、ROCm 系统测试 | 全液冷，rack 级冷却验证是关键 | Helios open rack、2.5D/CoWoS-L、HBM4 载板要求高 | GW 级 AMD rack 部署会提高 UPS、超级电容、飞轮、储能系统需求；更偏数据中心侧投资 |

## 5. 关键技术环节对产业链的含义

| 环节 | 2026-2027 变化 | 受益/受压环节 | 投资观察点 |
|---|---|---|---|
| 光刻掩膜 | 高端 GPU/ASIC 继续集中在 TSMC 4NP/3nm/2nm；中国国产 AI 芯片以 SMIC N+2/N+3 DUV 多重曝光为主 | EUV/DUV、掩膜版、OPC、EDA signoff、量测 | 2nm 节点先被 MI400/TPU8/后续 ASIC 抢占；掩膜改版次数决定试产成本 |
| 先进封装 | CoWoS-L/CoWoS-S、SoIC、EMIB-T、3.5D/F2F 增长；TSMC CoWoS 2026 年底约 11.5-14 万片/月，2027 约 17 万片/月 | TSMC、ASE/Amkor/OSAT、ABF 载板、bonding、underfill | CoWoS 外包比例、HBM4 base die 良率、CPO switch 封装良率 |
| HBM | 2026 HBM3E 仍主力，HBM4 从 Rubin/MI400/TPU8/ASIC 开始；HBM4 三大厂商 2026 Q2 验证 | SK hynix、Samsung、Micron、TC bonding、HBM tester | HBM4 是否多供成功；HBM 与常规 DRAM 产能切换导致价格波动 |
| 光互联 | 800G 到 1.6T，scale-out 光模块继续高增长；CPO 从交换芯片侧先进入 Spectrum-6/SPX、Broadcom Tomahawk/Jericho 生态 | 光模块、硅光、激光器、DSP、交换芯片 | CPO 的量产节奏、可维护性和失效率；光模块是否从 pluggable 过渡 |
| 芯片级供电 | 48V rack、板级 VRM、高密度电容、封装内/中介层去耦、背面供电和 semi-IVR 成为先进封装设计变量 | 电源模块、功率 IC、电感、电容、封装去耦 | AI 负载瞬态电流越来越大，功率平滑将从设施层下沉到 rack/board |
| 检测 | HBM KGD、interposer、SerDes、NVLink/UALink/NeuronLink、rack burn-in 成本上升 | 探针卡、ATE、老化炉、HBM tester、光电测试 | 测试时间可能成为非显性瓶颈，尤其 HBM4 和 CPO |
| 散热 | GB300、Rubin、MI400、Trainium3、Maia200 等进入全液冷/闭环液冷常态 | 冷板、CDU、快接头、泵阀、漏液检测、浸没/冷却液 | 单 rack 功耗和机房水/电能力决定真实交付 |
| 计算芯片基板 | ABF 载板层数和面积上升，chiplet + HBM 对翘曲、阻抗、热膨胀要求更高 | ABF、BT、高阶 PCB、IC substrate 设备 | 载板良率会影响从 wafer 到 rack 的有效产出 |
| 超级电容/飞轮储能 | 不是 AI 芯片 BOM 的主流，但在 rack/园区侧用于毫秒到秒级功率平滑、UPS 过渡、削峰 | 超级电容、飞轮 UPS、锂电 UPS、电力电子 | NVIDIA DSX 类动态功率调度若普及，会放大短时储能价值 |

## 6. 情景假设

| 情景 | 供应链假设 | 需求假设 | 价格/ASP 假设 |
|---|---|---|---|
| 务实 | HBM4 验证和 CoWoS 扩产有 1-2 个季度摩擦；Rubin/MI400/TPU8 以小批量为主，Blackwell Ultra 与 Ironwood/Trainium2 承担主力 | AI capex 增长但客户开始看 token ROI，推理需求增长快但训练集群分批上电 | 高端 GPU ASP 稳中略降；ASIC 内部转移价低于同算力 GPU |
| 乐观 | HBM4 三大供应商进入稳定供货；CoWoS 外包与 OSAT 承接顺利；液冷/光模块交付跟上 | Hyperscaler 公告的 GW 级订单按原计划推进；agentic inference token 增长继续超预期 | Blackwell/Rubin/ASIC 都维持高 ASP，内存涨价被客户接受 |
| 极度乐观 | HBM、CoWoS、ABF、光模块、冷却全部进入“供应被预定但可交付”状态；客户机房上电加速 | OpenAI/Meta/Anthropic/Google/AWS 把 2027 需求前置，主权 AI 追加订单 | 高端 rack 溢价维持，ASIC 与 GPU 同时放量而非互相挤出 |

## 7. 主要来源

| 来源 | 用途 |
|---|---|
| [NVIDIA Vera Rubin 官方新闻稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | Rubin、Vera CPU、Groq 3 LPU、BlueField-4、Spectrum-6、CPO、DSX 等路线图 |
| [NVIDIA Vera Rubin 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | NVL72、LPX、SPX、CPO、rack energy/cooling 细节 |
| [NVIDIA GB300 NVL72 官方页面](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) | GB300/Blackwell Ultra 技术定位 |
| [TrendForce：2026 Blackwell 占 NVIDIA 高端 GPU 出货 >70%](https://www.trendforce.com/presscenter/news/20260408-13003.html) | NVIDIA 2026 芯片结构、Rubin 延迟风险、LPU 数十万级需求 |
| [TrendForce：HBM4 预计 2026 Q2 验证](https://www.trendforce.com/presscenter/news/20260213-12929.html) | Rubin/HBM4 供应链假设 |
| [TrendForce：TSMC CoWoS 2026/2027 产能](https://www.trendforce.com/news/2026/04/16/news-tsmc-says-cowos-offers-industrys-largest-reticle-size-packaging-amid-intel-emib-rivalry-copos-advances/) | CoWoS 约束 |
| [Gartner 2026/2027 半导体收入预测](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | 自上而下市场规模校验 |
| [AMD Instinct 官方页面](https://www.amd.com/en/products/accelerators/instinct.html) | MI350/MI300 产品状态 |
| [AMD CES 2026 官方新闻稿](https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-and-its-partners-share-their-vision-for-ai-ev.html) | MI400、Helios、MI500 路线图 |
| [AWS Trainium3 官方公告](https://www.aboutamazon.com/news/aws/trainium-3-ultraserver-faster-ai-training-lower-cost/) | Trainium3、Trainium4 性能与路线图 |
| [AWS Project Rainier 官方文章](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster) | Trainium2 近 50 万颗、Anthropic >100 万颗目标 |
| [Google Ironwood TPU 官方博客](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/) | TPU v7 Ironwood 内存/带宽/推理定位 |
| [Google TPU 8t/8i 公告线索](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/eighth-generation-tpu-agentic-era/) | TPU8 训练/推理分化路线图 |
| [Microsoft Maia 200 官方博客](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/) | Maia 200 3nm、HBM3E、SRAM、推理定位 |
| [Meta MTIA 路线图官方文章](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/) | MTIA 300/400/450/500、数十万部署 |
| [Meta/Broadcom 官方合作公告](https://about.fb.com/news/2026/04/meta-partners-with-broadcom-to-co-develop-custom-ai-silicon/) | MTIA >1GW 首期、多 GW 路线图、Broadcom XPU |
| [OpenAI/Broadcom 官方公告](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/) | OpenAI 10GW 自研加速器，2026 H2 开始部署 |
| [TrendForce：Broadcom 2027 AI 芯片收入目标](https://www.trendforce.com/news/2026/03/05/news-broadcom-reportedly-eyes-100b-ai-chip-revenue-in-2027-backed-by-six-key-clients-including-google-meta/) | Broadcom >$100B、六大客户、OpenAI/Anthropic GW 线索 |
| [TrendForce：Huawei Ascend 950 路线图](https://www.trendforce.com/news/2025/09/18/news-huawei-unveils-ascend-950-with-in-house-hbm-in-2026-touts-superpod-to-rival-nvidia/) | Ascend 910C/950/960、Atlas SuperPoD/Cluster |
| [TrendForce：Cambricon 2026 产量与 SMIC 约束](https://www.trendforce.com/news/2025/12/15/insights-cambricon-remains-chinas-top-ai-chip-startup-rumored-2026-triple-output-faces-smic-limits/) | Siyuan 590/690、50 万颗目标、SMIC N+2 |
| [TrendForce：Baidu Kunlun M100/M300 路线图](https://www.trendforce.com/news/2025/11/13/news-baidu-rolls-out-kunlun-roadmap-m100-m300-ai-chips-arrive-2026-2027/) | Baidu M100/M300、Tianchi 超节点 |
| [SCMP：Alibaba Zhenwu 810E >10 万颗](https://www.scmp.com/tech/article/3341860/alibaba-ai-chip-push-hits-100000-mark-beating-local-rival-cambricon-sources) | Alibaba/T-Head 出货线索 |
| [Intel Gaudi 官方页面](https://www.intel.com/content/www/us/en/products/details/processors/ai-accelerators/gaudi.html) | Gaudi 3 状态 |
| [CRN：Intel 取消 Falcon Shores，转向 Jaguar Shores](https://www.crn.com/news/components-peripherals/2025/intel-cancels-falcon-shores-ai-chip-to-focus-on-system-level-solution) | Intel 下一代 AI 芯片路线图风险 |
| [Tenstorrent Galaxy Blackhole 官方公告](https://tenstorrent.com/newsroom/tenstorrent-enables-ai-at-scale-with-industry-leading-performance) | Blackhole/Galaxy GA |
| [Cerebras WSE-3 官方页面](https://www.cerebras.ai/chip) | WSE-3 规格与阶段 |
| [SambaNova SN40L 官方页面](https://sambanova.ai/products/sn40l-rdu-ai-chip) | SN40L 阶段 |

## 8. 读数注意事项

1. 自用 ASIC 的“美元金额”不是公开售价，而是按芯片、HBM、封装、载板、系统集成和可替代 GPU 价值估出来的内部转移价。因此 Google TPU、AWS Trainium、Meta MTIA、Microsoft Maia 与 NVIDIA/AMD merchant GPU 不能简单相加为公开市场销售额。
2. Broadcom XPU、Google TPU、Meta MTIA 和 OpenAI custom accelerator 有供应链重叠，表格中“Broadcom 其他 XPU”已经尽量扣除已单列项目，但仍可能和公开口径出现重合。
3. 中国国产 AI 芯片的单位数量可能很大，但 ASP 与单芯片算力通常低于 Blackwell/Rubin；系统级竞争力更多依赖超节点互连、软件栈和本地客户适配。
4. 2027 的极度乐观情形本质上是假设“AI 推理需求继续吞掉所有新增电力与先进封装产能”。如果 hyperscaler 开始用 ROI 严格压制 capex，真实值会更接近务实情形。
