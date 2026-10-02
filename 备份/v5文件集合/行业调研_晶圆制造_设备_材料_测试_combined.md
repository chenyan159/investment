# 行业调研：【AI芯片前道制造设备】

> 截至日期：2026-05-08  
> 研究口径：本文聚焦 AI 数据中心加速器、云厂自研 ASIC、HBM/先进 DRAM 以及相关先进逻辑/存储产能扩张所拉动的**前道晶圆制造设备**，包括光刻/EUV/DUV、涂胶显影 Track、刻蚀、薄膜沉积 ALD/CVD/PVD/Epi、离子注入/退火/热处理、CMP/清洗、电镀/湿法、过程控制量测/检测、掩膜/reticle 制造检测、自动化和服务升级。先进封装设备只在与前道工艺或 AI 芯片有效出货强绑定时作为外延提及。  
> 预测原则：对 2026-2027 年 AI 计算中心建设保持乐观。直接数据缺失处，用 SEMI WFE/300mm equipment、头部设备公司财报和项目内 AI 芯片出货路线做自上而下与自下而上交叉估算。市场规模为研究估算，美元口径；利润率默认指毛利率。

## 0. 高浓度结论

### 0.1 一句话判断

AI 芯片前道制造设备在 2026 年进入第二轮重估：第一轮是 2023-2025 年 Blackwell/HBM 把 CoWoS/HBM 变成瓶颈；第二轮是 2026 年开始，GB300/B300、Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA、OpenAI/Broadcom XPU、AMD MI400 和 Rubin/TPU8/Trainium3/4 共同把**先进逻辑、HBM DRAM、2nm/GAA、EUV/DUV、多重图形化、ALD/Epi、刻蚀、过程控制和服务升级**全部拉成一个更长周期的设备超级周期。

最值得押注的不是单一设备品类，而是“所有 AI 高端芯片都绕不开、且客户切换成本最高”的几层：**ASML EUV/DUV 与 installed-base service、TEL 涂胶显影、Lam/TEL/AMAT 刻蚀、AMAT/ASM/TEL/Lam 沉积、KLA/Nova/Onto/Lasertec 过程控制、HBM DRAM 相关前道设备、以及 GAA/背面供电/4F² DRAM 的下一代工艺设备组合**。

### 0.2 总盘子预测

| 指标 | 2025/当前锚点 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 基准 | 2027 乐观 | 2027 极度超预期乐观 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 全球半导体收入 | SIA：2026 Q1 $298.5B；Gartner：2026 超 $1.3T | $1.30T-$1.36T | $1.38T-$1.48T | $1.50T+ | $1.50T-$1.60T | $1.65T-$1.80T | $1.90T+ |
| 全球总半导体制造设备销售 | SEMI：2025 $133B，2026 $145B，2027 $156B | $145B | $150B-$158B | $160B-$175B | $156B | $165B-$180B | $185B-$210B |
| 全球 WFE 销售 | SEMI：2025 WFE $115.7B；2026/2027 继续增长 | $124B-$128B | $130B-$140B | $145B-$160B | $135B-$140B | $145B-$160B | $165B-$185B |
| 全球 300mm fab equipment spending | SEMI：2026 $133B、2027 $151B | $133B | $140B-$150B | $155B-$175B | $151B | $160B-$175B | $180B-$205B |
| AI 相关前道设备收入池 | 本报告估算：advanced logic + HBM DRAM + AI ASIC/GPU direct pull | $58B-$74B | $75B-$95B | $95B-$125B | $76B-$105B | $105B-$135B | $135B-$170B |
| AI 相关设备服务/升级/field solutions | Lam/TEL/ASML service 均增长，fab utilization 抬升 | $24B-$32B | $32B-$42B | $42B-$55B | $30B-$42B | $42B-$58B | $58B-$75B |

关键事实锚点：

- SEMI 2026-04 预计全球 300mm fab equipment spending 2026 年增长 18% 到 **$133B**，2027 年再增长 14% 到 **$151B**，并称 AI 正在重置半导体制造投资规模。
- SEMI 2025-12 预计总半导体制造设备销售 2025/2026/2027 分别约 **$133B / $145B / $156B**；其中 WFE 2025 年 **$115.7B**，并预计 2026、2027 继续增长。
- ASML 2026Q1 官方披露总净销售 **€8.8B**、毛利率 **53.0%**、EPS **€7.15**，并指引 2026 年总净销售约 **€36B-€40B**、毛利率 **51%-53%**。
- Applied Materials 2026 财年 Q1 收入 **$7.012B**、GAAP 毛利率 **49.0%**、非 GAAP 毛利率 **49.1%**；管理层称 AI 计算投资推动 leading-edge foundry/logic、HBM DRAM、advanced packaging 成为最快增长市场，并预计 calendar 2026 半导体设备业务增长 **20%+**。
- Lam Research 2026 年 3 月季度收入 **$5.841B**、非 GAAP 毛利率 **49.9%**，6 月季度收入指引 **$6.60B +/- $0.40B**，CEO 明确称 AI-driven demand 正在重塑半导体行业。
- KLA 2026 财年 Q3 对 2026 年 6 月季度收入指引 **$3.575B +/- $0.2B**，非 GAAP 毛利率 **61.75% +/- 1%**，是过程控制高毛利的最好财务锚。
- Tokyo Electron FY2026 全年净销售 **¥2.4435T** 创新高；FY2027 H1 预计受 AI server demand 驱动创纪录；公司称 FY2027 SPE new equipment sales 同比增长 **41%**，涂胶显影市场份额 **>90%**，advanced packaging revenue FY2027 预计 **+60%+**。
- ASM International 2026Q1 收入 **€863M**、毛利率 **53.3%**、调整后经营利润率 **33.1%**；公司称 AI-led demand 加速，先进逻辑/foundry 与 HBM 相关先进 DRAM 需求强，ALD 市占 **>55%**。

### 0.3 2026 最可能放量的技术路径

1. **低 NA EUV + ArFi DUV 多重图形化仍是 2026 主收入。** 2026 年真正量大的 AI 芯片是 GB300/B300、B200/GB200、MI350、TPU Ironwood、Trainium2/3、Maia200 和 MTIA，核心制程集中在 TSMC 4NP/3nm、三星/Intel/部分 3nm、先进 DRAM 1b/1c。High-NA EUV 是 2027-2028 弹性，2026 主要贡献工具出货、验证和少量收入。
2. **HBM/先进 DRAM 设备比传统 DRAM 周期更强。** HBM3E 12Hi 继续主导，HBM4 进入 Rubin/MI400/TPU8/下一代 ASIC 验证；这拉动 DRAM EUV、HARC etch、ALD/CVD、清洗、CMP、量测和 KGD 前移。
3. **2nm/GAA 是 2026 H2-2027 的逻辑设备主线。** GAA nanosheet 带来 ALD/Epi layer intensity、选择性沉积、选择性刻蚀、inner spacer、work-function metal、低损伤清洗和多物理场量测的价值上升。
4. **背面供电 BSPDN/PowerVia/Super Power Rail 由研发进入 pilot。** 2026 年规模还不大，但会拉动 wafer bonding/debonding、背面薄化、背面 litho/etch/deposition/CMP、对准与量测。
5. **过程控制从“良率保险”变成 AI 芯片放量瓶颈。** EUV stochastic defects、GAA 3D 形貌、HBM DRAM、背面供电、advanced packaging 前移，使 inspection/metrology spending 占 WFE 的份额继续上升，KLA/Nova/Onto/ASML HMI/Hitachi/Lasertc 具备更强定价权。

## 1. 2026 机遇、挑战、正在使用的技术与放量时间

### 1.1 2026 机遇

| 机遇 | 为什么 2026 更强 | 对前道设备的含义 |
|---|---|---|
| AI 半导体总量直接抬升 | Gartner 预计 AI 半导体约占 2026 半导体收入 30%；SIA 2026Q1 半导体销售 $298.5B，3月同比 +79.2% | 先进逻辑、HBM DRAM、网络芯片、功率管理都会追加 wafer capacity |
| CSP capex 与 AI 芯片出货双上修 | 项目内 AI 芯片报告估算 2026 AI 芯片/模块 $300B-$650B 三情景 | 设备订单从单一 NVIDIA 供应链扩散到 GPU + ASIC + HBM |
| HBM 变成前道设备超级驱动 | HBM3E/HBM4 需要先进 DRAM 节点、更多 EUV/刻蚀/沉积/量测 | DRAM 设备从周期品变成 AI 资源品；Lam/TEL/AMAT/ASM/KLA/ASML 受益 |
| GAA/2nm/N2/14A/A16 进入 HVM 准备 | 2nm 与 GAA 对 ALD/Epi、刻蚀、清洗、量测强度显著高于 FinFET | 单位 100k WSPM 对设备 SAM 上升，ASM 等已强调 1.4nm 将进一步提高 ALD/Epi SAM |
| 服务、改造和 spares 周期更长 | AI fab 利用率高、设备瓶颈不能停机 | ASML installed base management、Lam customer support、TEL field solutions、KLA service 均有高质量收入 |
| 国产替代和地缘分层 | 中国无法获取完整高端 EUV/部分高端设备，转向 DUV 多重曝光和本土设备 | AMEC/Naura/ACM/SMEE 等获得本土需求；同时国外设备对非中国高端客户供给更紧 |

### 1.2 2026 挑战

| 挑战 | 表现 | 设备侧风险 |
|---|---|---|
| EUV/High-NA 供给周期长 | Zeiss optics、光源、stage、系统集成和客户验收均需长周期 | ASML 订单能见度强，但短期产能不是无限；客户排队和预付款强化 |
| 客户 cleanroom 和安装验收 | TEL 明确提示 cleanroom space、零部件、材料和劳动力是变量 | 工具发货不等于 revenue/acceptance，Q 季节性和安装延迟会波动 |
| 复杂工艺良率风险 | GAA、背面供电、HBM4、4F² DRAM 都是 3D integration 问题 | 量测/检测/工艺控制订单增加，但新节点 ramp 可能延迟 |
| 出口管制和关税 | 中国先进节点设备受限，美国/荷兰/日本政策不确定 | 中国收入占比高的公司承受政策折扣；本土设备估值上行但技术差距仍在 |
| 供应链关键部件瓶颈 | 真空泵、RF power、MFC、ESC、陶瓷件、光学部件、激光器 | 设备交期延长，毛利受零部件涨价压力影响 |
| 价格高企导致客户 ROI 检验 | EUV/High-NA、先进刻蚀/沉积/量测工具 ASP 上升 | 若 2027 AI capex 放缓，最边际的扩产项目会递延 |

### 1.3 当前正在被使用的关键技术

| 技术层 | 2026 已用主路线 | 代表设备/供应商 | 2026 放量确定性 |
|---|---|---|---|
| Low-NA EUV lithography | N5/N4/N3/N2 关键层，DRAM EUV 层增加 | ASML NXE:3600/3800/4000 系列、EUV source/IBM upgrades | 极高 |
| ArFi DUV 多重图形化 | TSMC 4NP/3nm 多层、成熟节点、中国国产 AI 芯片多重曝光 | ASML NXT immersion、Nikon/Canon 部分成熟 DUV | 极高 |
| Coater/developer track | 所有光刻前后处理，EUV resist 工艺窗口更难 | Tokyo Electron CLEAN TRACK/涂胶显影，SCREEN/SEMES 等 | 极高，TEL >90% share |
| Dry etch/HARC etch | GAA、DRAM capacitor、HBM、interconnect、via/trench | Lam Kiyo/Akara/Sense.i、TEL etch、AMAT etch、AMEC/Naura | 极高 |
| ALD/CVD/PVD/Epi | 高-k、work-function metal、molybdenum、barrier/liner、DRAM capacitor、GAA epi | AMAT、ASM、TEL、Lam、Kokusai、Applied Centura/Producer/Endura 等 | 极高 |
| Wet clean/CMP | EUV 后清洗、GAA 低损伤清洗、interconnect CMP、DRAM/HBM | SCREEN、TEL、Lam、AMAT、Ebara、ACM Research | 高 |
| Process control | EUV stochastic、GAA 3D CD、overlay、defect inspection、mask inspection | KLA、ASML HMI、Applied PROVision、Hitachi、Nova、Onto、Lasertec | 极高 |
| Implant/anneal/thermal | FinFET/GAA channel/doping、power devices、DRAM | Applied Varian、Axcelis、TEL/Kokusai thermal、Veeco | 中高 |
| Dry resist / metal oxide resist | EUV/High-NA 图形化降成本和降随机缺陷 | Lam Aether dry resist、imec/ASML ecosystem、JSR/TOK等 resist | 2026 研发/早期，2027+弹性 |
| Backside power delivery | Intel PowerVia、TSMC A16/Super Power Rail 相关 | bonding/debonding、backside etch/deposition/CMP/metrology | 2026 pilot，2027-2028 放量 |

### 1.4 基于项目内 AI 芯片路线的设备映射

以下芯片排序来自项目内 `ai_chip_research_2026_2027.md`，本文只映射对前道设备的拉动。

| 2026-2027 大出货平台 | 前道制造路径 | 直接拉动设备 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | TSMC 4NP/advanced EUV+DUV、HBM3E 供应链、CoWoS 约束 | Low-NA EUV、ArFi DUV、track、etch/deposition、process control、HBM DRAM WFE、服务升级 |
| AWS Trainium2/3 | Trainium2 成熟，Trainium3 3nm；HBM + custom ASIC | 3nm foundry tools、HBM DRAM tools、KLA/Nova/Onto 量测、etch/deposition |
| Google TPU v7 Ironwood / TPU8 | Ironwood HBM3E/advanced node；TPU8 训练/推理分化，可能迈向 2nm/HBM4 | N3/N2 capacity、HBM4 DRAM tools、process control、mask/reticle |
| NVIDIA B200/GB200 | 4NP + HBM3E，2026 存量/延续 | 维持 EUV/DUV/etch/deposition/HBM3E 利用率 |
| Huawei Ascend 910C/950、Cambricon 590/690 | 中国可得 DUV 多重曝光、SMIC N+2/N+3、国产 HBM/高带宽内存爬坡 | DUV、etch/deposition/clean 国产设备，过程控制国产替代，高端设备受限 |
| AMD MI350/MI355 | 先进 foundry + HBM3E，OAM/UBB 多形态 | TSMC/DRAM/HBM WFE，GAA 前置技术验证 |
| Microsoft Maia 200 | TSMC 3nm + HBM3E | N3 capacity、HBM3E DRAM equipment、wafer probe/process control |
| Meta MTIA 300/400/450/500 | Broadcom XPU 平台，2026-2027 快速迭代 | Custom ASIC tape-out 带来 mask/EDA/reticle/wafer capacity，3nm/2nm 设备 |
| NVIDIA Rubin / AMD MI400 / OpenAI-Broadcom XPU | HBM4、2nm/3nm、GAA/更高带宽封装 | HBM4 DRAM WFE、N2/GAA ALD/Epi/etch、高 NA 预研、process control、BSPDN pilot |

### 1.5 新技术成熟与放量时间：三情景

| 新技术 | 基准 | 乐观 | 极度超预期乐观 | 2026 判断 |
|---|---|---|---|---|
| Low-NA EUV productivity upgrade | 2026 全年主力，IBM/service 增长 | EUV utilization 满载，客户购买更多升级包 | EUV 工具/服务被 HBM+logic 双线挤满，价格/服务溢价扩大 | 最高确定性 |
| ArFi DUV 多重图形化 | 2026 受先进节点补充和中国国产替代支撑 | China mature/advanced DUV 需求维持高位 | 受出口限制下客户抢购允许范围内 DUV 和本土替代 | 高 |
| High-NA EUV EXE | 2026 tool qualification，2027-2028 小批量生产导入 | Intel/Samsung/SK hynix 2027 更积极导入 | 2027 前成为少数高端 AI/HBM platform 的战略产能 | 2026 收入小、期权大 |
| Dry resist / MOR | 2026 imec/IBM/Lam 等验证，低 NA 28nm pitch 和 High-NA 工艺开发 | 2027 进入部分 high-NA/low-NA 关键层 | 若随机缺陷/剂量瓶颈恶化，2027 提前商业导入 | 2026 研发/小收入 |
| GAA nanosheet equipment suite | 2026 N2/3nm ramp，2027 N2/N2P/1.4nm pilot | 2nm AI ASIC tape-out 增多，ALD/Epi/etch SAM 上修 | AI ASIC 抢 N2/N1.4 pilot，工具产能被预定 | 高 |
| Backside power delivery | 2026 pilot/early production，2027-2028 明显放量 | 2027 头部 AI ASIC/CPU 提前采用 | 若功耗/PDN 成为 AI 限制，BSPDN 设备订单前置 | 2026 低到中 |
| 4F² DRAM / HBM4 DRAM front-end | 2026 开始验证/扩产，2027 放量 | 三大内存厂 HBM4 扩产顺利，DRAM WFE 上修 | HBM4/HBM4E 缺货导致 DRAM EUV/etch/deposition 再上修 | 中高 |
| Selective Mo/Ru interconnect | 2026 N2/advanced interconnect design-in | 2027 高端 logic/ASIC 采用率提升 | 若铜互连 RC 成为瓶颈，选择性金属沉积提前放量 | 中 |
| AI-driven process control | 2026 已在 leading-edge fab 使用 | 2027 defect review/metrology 自动化成标配 | 工艺复杂度使 process control spend share 非线性上升 | 高 |

## 2. 已经开始放量的关键产品：市场规模、渗透率、增长和利润率

说明：下表是全球口径收入池估算，不等于单家公司收入；未来 3 个月为 2026-05 至 2026-08，未来 1 年为 2026-05 至 2027-05，未来 2 年为 2026-05 至 2028-05。渗透率为该技术在相关 AI/先进逻辑/HBM 设备采购中的价值或工艺使用份额。

### 2.1 已放量产品总表

| 产品/细分技术 | 当前放量证据 | 未来 3 个月规模：基准 / 乐观 / 极度 | 未来 1 年规模：基准 / 乐观 / 极度 | 未来 2 年规模：基准 / 乐观 / 极度 | 渗透率路径 | 毛利率：基准 / 乐观 / 极度 |
|---|---|---:|---:|---:|---|---|
| Low-NA EUV scanner + EUV service/upgrades | ASML Q1 2026 €8.8B、FY26 €36B-€40B 指引；AI/HBM 需求强 | $4.5B-$6.5B / $6.5B-$8.5B / $8.5B-$11B | $18B-$25B / $25B-$33B / $33B-$45B | $40B-$58B / $58B-$80B / $80B-$110B | 先进逻辑关键层 100%；DRAM EUV 层数继续升 | 51%-55% / 54%-58% / 57%-61% |
| ArFi DUV immersion + KrF/i-line | 先进节点多重图形化、中国 DUV 替代、成熟节点复苏 | $3B-$5B / $5B-$7B / $7B-$9B | $13B-$20B / $20B-$28B / $28B-$38B | $25B-$42B / $42B-$62B / $62B-$85B | 先进逻辑大量非 EUV 层；中国国产 AI 芯片依赖 DUV | 44%-52% / 50%-55% / 54%-58% |
| Coater/developer track | TEL 披露 coater/developer share >90%，FY2027 revenue >+50% YoY | $1.2B-$2B / $2B-$3B / $3B-$4B | $5.5B-$8.5B / $8.5B-$12B / $12B-$17B | $12B-$22B / $22B-$34B / $34B-$48B | EUV/DUV 每层必需；EUV resist 工艺窗口提升价值 | 45%-52% / 50%-56% / 55%-60% |
| Dry etch 系统：dielectric/conductor/HARC/GAA | Lam 3月季度 record revenue；TEL etch FY2027 +25%+；AI/HBM/GAA 拉动 | $6B-$9B / $9B-$12B / $12B-$16B | $25B-$36B / $36B-$50B / $50B-$68B | $55B-$85B / $85B-$125B / $125B-$170B | 先进 logic/DRAM/HBM 关键工序高 attach；GAA/HARC 强度上升 | 48%-54% / 52%-58% / 56%-62% |
| Deposition：ALD/CVD/PVD/Epi/selective metal | AMAT 预计 CY26 半导体设备 +20%+；ASM ALD share >55%、Q1 GM 53.3% | $7B-$11B / $11B-$15B / $15B-$20B | $30B-$46B / $46B-$62B / $62B-$85B | $68B-$110B / $110B-$160B / $160B-$220B | GAA/DRAM/HBM4/4F² 增加 ALD/Epi/metal layers | 49%-56% / 54%-60% / 58%-64% |
| Wet clean / CMP / plating | HBM/GAA/背面供电/先进互连均提升清洗和 CMP 强度 | $4B-$6.5B / $6.5B-$9B / $9B-$12B | $17B-$26B / $26B-$38B / $38B-$52B | $36B-$60B / $60B-$95B / $95B-$135B | 先进 logic 和 memory 几乎全流程 attach；BSPDN 增量 | 38%-48% / 45%-54% / 52%-58% |
| Process control：inspection/metrology/defect review | KLA 6月季指引 $3.575B、非GAAP GM 61.75%；EUV/GAA/HBM 提升缺陷成本 | $4.5B-$7B / $7B-$9.5B / $9.5B-$13B | $20B-$30B / $30B-$42B / $42B-$58B | $45B-$72B / $72B-$110B / $110B-$150B | 高端 fab WFE 中价值占比从约 15%-18% 向 20%+ 上升 | 58%-64% / 62%-68% / 66%-72% |
| Mask/reticle write、inspection、repair | EUV mask 成本、OPC/curvilinear、stochastic defect 增加 | $0.8B-$1.5B / $1.5B-$2.2B / $2.2B-$3B | $4B-$6.5B / $6.5B-$9.5B / $9.5B-$14B | $8B-$15B / $15B-$25B / $25B-$38B | 高端 AI ASIC tape-out 增多；re-spin 和多平台 ASIC 增加 reticle 需求 | 50%-62% / 58%-68% / 65%-75% |
| Ion implant / anneal / thermal | GAA 和功率器件复苏、memory migration 支撑 | $1.5B-$2.5B / $2.5B-$3.5B / $3.5B-$5B | $6.5B-$10B / $10B-$15B / $15B-$22B | $13B-$22B / $22B-$36B / $36B-$55B | 先进 logic 必需但增长低于 etch/deposition；power AI 外延拉动 | 40%-50% / 48%-55% / 52%-60% |
| Installed-base service / spares / upgrades | Lam customer support $2.11B/季；TEL FY2026 field solutions ¥626B、+16.3% | $8B-$12B / $12B-$16B / $16B-$22B | $34B-$48B / $48B-$65B / $65B-$88B | $75B-$110B / $110B-$160B / $160B-$220B | 高利用率 fab 和 EUV/etch/deposition upgrades 提升 recurring mix | 45%-58% / 55%-65% / 60%-70% |

### 2.2 已放量产品增长排序

| 增长确定性 | 方向 | 逻辑 |
|---|---|---|
| S | EUV/DUV lithography + track + process control | 所有先进 AI 芯片都绕不开；ASML/TEL/KLA 集中度最高 |
| S | HBM DRAM 相关 etch/deposition/clean/CMP/metrology | HBM3E/HBM4 是 AI 算力共同瓶颈，DRAM WFE 周期被拉长 |
| S- | GAA 2nm ALD/Epi/selective etch/deposition | 2026 H2-2027 进入更大规模，技术强度高 |
| A+ | Etch/deposition service upgrades | 存量设备利用率高，升级和 spares 高利润 |
| A | DUV/国产替代设备 | 中国需求强，但受出口管制和本土技术能力制约 |
| A- | CMP/clean/plating | 成长确定，但竞争分散、毛利略低 |
| B+ | Implant/thermal | 必需但 AI 直接弹性弱于 litho/etch/deposition/metrology |

## 3. 在研关键产品和未来快速增长技术

### 3.1 在研/导入期技术预测

| 在研产品/技术 | 2026-05 阶段 | 未来 3 个月规模：基准 / 乐观 / 极度 | 未来 1 年规模：基准 / 乐观 / 极度 | 未来 2 年规模：基准 / 乐观 / 极度 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| High-NA EUV EXE:5000/5200 | Imec 2026-03 接收 EXE:5200；客户研发/早期 production prep | $0.4B-$1.2B / $1.2B-$2B / $2B-$3B | $2B-$6B / $6B-$10B / $10B-$16B | $8B-$20B / $20B-$35B / $35B-$55B | 2026 <5% EUV spend；2027-2028 在 Intel/Samsung/SK 等加速 | ASML 系统 GM 50%+，High-NA 稀缺可更高 |
| Dry resist / Aether / MOR EUV ecosystem | Lam/IBM 2026 合作 sub-1nm logic；Lam/imec 28nm pitch dry resist | $0.05B-$0.2B / $0.2B-$0.5B / $0.5B-$1B | $0.5B-$1.5B / $1.5B-$3B / $3B-$5B | $2B-$6B / $6B-$12B / $12B-$20B | 2026 工艺验证，2027 高端层导入；若随机缺陷严重则加速 | 新工艺设备/材料组合 GM 55%-70% |
| GAA 2nm/1.4nm process suite | N2/N2P/A16/14A 量产准备；ASM 称 GAA 提高 ALD/Epi layers | $2B-$4B / $4B-$6B / $6B-$9B | $10B-$18B / $18B-$28B / $28B-$42B | $35B-$65B / $65B-$100B / $100B-$145B | 2026 先进逻辑 10%-20%，2027 25%-45%，2028 50%+ | 高端 ALD/Epi/etch/process control GM 50%-65% |
| Backside power delivery equipment | PowerVia/A16/Super Power Rail pilot | $0.2B-$0.8B / $0.8B-$1.5B / $1.5B-$3B | $2B-$6B / $6B-$12B / $12B-$22B | $10B-$25B / $25B-$45B / $45B-$75B | 2026 pilot，2027 high-end CPU/AI ASIC 小批，2028 放量 | 早期高毛利但良率风险高，45%-65% |
| 4F² DRAM / next-gen HBM front-end | DRAM cell/peri 架构迁移，HBM4/4E 驱动 | $0.5B-$1.5B / $1.5B-$3B / $3B-$5B | $4B-$10B / $10B-$18B / $18B-$30B | $18B-$45B / $45B-$80B / $80B-$120B | 2026 HBM4 验证，2027 先进 DRAM CAPEX 主线 | DRAM 设备 GM 45%-60%，稀缺 HBM 工艺更强 |
| Selective Mo/Ru / low-R interconnect | AMAT Spectral ALD/selective molybdenum 等进入客户验证 | $0.1B-$0.4B / $0.4B-$1B / $1B-$2B | $1B-$4B / $4B-$8B / $8B-$14B | $8B-$20B / $20B-$38B / $38B-$60B | 2026 N2/advanced DRAM 小量，2027 高端逻辑增加 | 50%-65%，材料工程壁垒高 |
| Multi-beam e-beam inspection / AI defect review | EUV stochastic/GAA 复杂度推动 | $0.4B-$1B / $1B-$2B / $2B-$3B | $3B-$8B / $8B-$14B / $14B-$22B | $10B-$28B / $28B-$50B / $50B-$80B | 2026 高端 EUV fab 采用，2027 量测占比继续升 | 60%-75%，软件/算法 attach 提升 |
| Curvilinear mask / computational lithography hardware acceleration | EUV/High-NA mask 数据量暴涨 | $0.1B-$0.3B / $0.3B-$0.8B / $0.8B-$1.5B | $0.8B-$2.5B / $2.5B-$5B / $5B-$9B | $3B-$10B / $10B-$20B / $20B-$35B | 2026 design flow，2027 mask shop equipment/software spend 上升 | 软件/IP 70%+，mask writer 45%-60% |
| Wafer bonding/debonding 前道化 | BSPDN、3D integration、hybrid bonding 前移 | $0.3B-$0.8B / $0.8B-$1.5B / $1.5B-$2.5B | $2B-$5B / $5B-$10B / $10B-$18B | $8B-$22B / $22B-$45B / $45B-$70B | 2026 advanced packaging/pilot，2027 logic backside 增量 | 45%-65%，EVG/SUSS/TEL/Besi/AMAT 等 |

### 3.2 未来 24 个月最可能超预期的 6 条路线

1. **High-NA EUV 不是 2026 收入主线，但会重新定价 ASML 的长期垄断。** 如果 Intel 14A、Samsung 2nm/1.4nm、SK hynix/Samsung HBM4E 为减少多重曝光提前采用 High-NA，2027-2028 High-NA 单机价格约 $350M-$400M 的收入弹性会非常高。
2. **Dry resist/MOR 可能成为 EUV 成本曲线的关键补丁。** AI 芯片大 die、多层 EUV 使 dose、stochastic、line-edge roughness 和 defect review 成本上升，若 dry resist 能减少步骤或改善缺陷，Lam/材料/track/etch 的组合价值会放大。
3. **BSPDN 是 2027 后 AI 芯片功耗瓶颈的设备答案。** Rubin/MI400/TPU8 后单封装功耗上升，正面 routing 拥堵和 IR drop 会把背面供电从高端 CPU 延伸到 AI ASIC。
4. **Process control spend share 上行几乎不可逆。** GAA、HBM4、EUV stochastic、multi-die 让“良率时间”比单台设备价格更重要，KLA/Nova/Onto/ASML HMI 的高毛利更持久。
5. **4F² DRAM 和 HBM4E 会把 DRAM 设备周期推长。** 过去 DRAM capex 强周期会快速反转，但 HBM 与数据中心内存绑定后，先进 DRAM 设备投资更接近多年 AI 基础设施建设。
6. **中国 DUV 多重曝光与国产设备会形成独立 beta。** 即便性能不及 EUV 路线，中国 AI 芯片需求足够大，国产刻蚀/沉积/清洗/量测/涂胶显影会获得政策和客户容忍度。

## 4. 供给侧：产能结构、瓶颈、成本和价格传导

### 4.1 产能结构

| 层级 | 主要地区 | 主要公司 | 工艺/产品 |
|---|---|---|---|
| EUV/DUV lithography | 荷兰为核心，德国/美国/日本供应链 | ASML、Zeiss、Cymer；Nikon/Canon 在 DUV/成熟光刻 | EUV NXE/EXE、ArFi、KrF/i-line、scanner upgrades |
| Track / coater developer | 日本/韩国 | Tokyo Electron、SCREEN、SEMES、DNS | EUV/DUV 涂胶显影、post-exposure bake、developer |
| Etch | 美国、日本、中国 | Lam Research、Tokyo Electron、Applied Materials、Hitachi High-Tech、AMEC、Naura | dielectric/conductor/HARC/GAA/DRAM etch |
| Deposition | 美国、荷兰、日本、中国 | Applied Materials、ASM International、Tokyo Electron、Lam、Kokusai、Piotech、Naura | ALD/CVD/PVD/Epi/selective deposition |
| Clean/CMP/Plating | 日本、美国、中国 | SCREEN、TEL、Lam、Applied Materials、Ebara、ACM Research、Hwatsing | single-wafer clean、wet bench、CMP、electroplating |
| Process control | 美国、日本、以色列/欧洲 | KLA、ASML HMI、Applied Materials、Hitachi、Nova、Onto、Lasertec、Camtek | optical/e-beam inspection、metrology、mask inspection |
| Implant/Thermal | 美国、日本 | Applied Varian、Axcelis、TEL、Kokusai、Veeco | ion implant、RTP、anneal、oxidation/diffusion |
| Mask/reticle tools | 日本、美国、奥地利/德国 | NuFlare、IMS Nanofabrication、JEOL、Lasertec、KLA、Applied | e-beam/multi-beam writer、actinic mask inspection、repair |
| 客户端先进逻辑产能 | 台湾、韩国、美国、中国 | TSMC、Samsung Foundry、Intel Foundry、SMIC | N4/N3/N2/A16/14A/GAA/DUV multi-pattern |
| 客户端 HBM/DRAM 产能 | 韩国、美国、日本、台湾、中国 | SK hynix、Samsung、Micron、CXMT、Nanya | HBM3E/HBM4、1b/1c/1γ DRAM、TSV/HBM base die |

### 4.2 供给瓶颈

1. **EUV 光学和系统集成**：High-end optics、light source、stage、控制软件和整机调试周期极长，ASML 垄断带来强定价和高 backlog，但短期供给非弹性。
2. **客户 cleanroom / utilities / installation**：设备厂能发货不代表客户能安装；cleanroom space、电力、冷却、化学品、field engineer、验收会卡收入确认。
3. **关键零部件**：RF generators、vacuum pumps、MFC、valves、ESC、ceramics、precision stages、metrology optics、laser source 交期拉长。
4. **HBM DRAM 工艺迁移**：HBM4/4E 需要先进 DRAM 前道、更多 EUV/etch/deposition/量测，DRAM 厂同时要平衡 commodity DRAM 供应。
5. **EUV 随机缺陷和 mask 复杂度**：stochastic defect、mask 3D effect、pellicle、curvilinear mask data 爆炸，使 mask shop 和 defect review 成为隐性瓶颈。
6. **GAA 与背面供电 integration**：nanosheet 厚度、inner spacer、selective deposition/etch、背面 wafer thinning/bonding 都是良率风险点。
7. **出口管制**：ASML EUV 和部分先进 DUV/美国设备无法自由流向中国，造成全球供给分层；中国本土设备替代需求强，但高端良率与生态不足。
8. **人才与应用工程**：先进设备销售本质是 process recipe + field support，应用工程师、装机团队、良率 debug 人才紧缺。
9. **前道材料联动**：photoresist、CMP slurry、湿化学品、特气、硅片、mask blank 若紧张，会让设备有效产出打折。
10. **客户集中与排产优先级**：TSMC、Samsung、SK hynix、Micron、Intel、SMIC 等少数客户决定大部分高端设备排产，非头部客户交期和价格更差。

### 4.3 典型设备成本和毛利结构

| 成本项 | 普通 etch/deposition/CMP 工具占比 | Lithography/EUV 特殊占比 | 毛利影响 |
|---|---:|---:|---|
| 精密机械、真空、腔体、机器人 | 20%-35% | 10%-20% | 供应链稳定后可规模降本 |
| 光学/source/stage | 5%-15% | 35%-55% | EUV 最大成本和最大壁垒 |
| RF、电源、控制电子、传感器 | 15%-25% | 10%-18% | 关键零部件涨价会压毛利 |
| 软件、算法、recipe、APC | 5%-15% | 8%-15% | 软件/升级 attach 提升毛利 |
| 直接人工和装配测试 | 8%-15% | 10%-15% | High-end 工具验收周期影响收入 |
| 质保、物流、field support | 5%-12% | 5%-10% | installed base 越大服务越优质 |
| 公司固定成本/R&D 摊销 | 10%-20% | 10%-20% | 高端工具需要持续高 R&D |

毛利锚点：ASML Q1 2026 毛利率 53.0%；AMAT Q1 FY26 非 GAAP 毛利率 49.1%；Lam 2026年3月季度非 GAAP 毛利率 49.9%；KLA 2026年6月季度非 GAAP 毛利率指引 61.75%；TEL FY2026 毛利率 45.3%；ASM Q1 2026 毛利率 53.3%。这说明最强定价层大致排序为：**过程控制/软件化量测 > EUV/高端光刻 > ALD/Epi/选择性沉积 > 高端刻蚀 > CMP/clean/传统设备**。

### 4.4 价格传导机制

| 机制 | 如何发生 | 受益者 |
|---|---|---|
| 工具 ASP 上行 | High-NA、EUV、GAA/HBM 工艺复杂度提升，单台工具价值量上升 | ASML、KLA、ASM、Lam、AMAT、TEL |
| 长交期和 capacity reservation | 客户用预付款、长单、优先装机换产能 | ASML、Lam、AMAT、TEL、KLA |
| Installed-base upgrades | 提高 throughput、overlay、defect review、recipe、automation，不一定买新工具 | ASML IBM、Lam service、TEL field solutions、KLA service |
| Process of record 锁定 | 一旦客户节点 POR 使用某设备/recipe，切换成本极高 | 所有进入 leading-edge POR 的设备厂 |
| 供不应求下客户更看重 time-to-market | AI 芯片迟一季损失大于设备溢价 | 光刻、量测、etch/deposition 龙头 |
| 出口限制造成区域溢价 | 中国本土客户愿为可获得设备/国产替代付出更高价格或容忍较低效率 | 国内设备厂、成熟 DUV 供应链 |

## 5. 竞争格局、可量化壁垒与价值捕获

### 5.1 市场结构

| 细分 | 集中度/份额判断 | 头部公司 |
|---|---|---|
| EUV lithography | CR1 = 100% | ASML |
| DUV immersion | ASML 绝对主导，Nikon/Canon 在部分 DUV/成熟节点 | ASML、Nikon、Canon |
| Coater/developer | TEL 披露市场份额 >90% | Tokyo Electron、SCREEN、SEMES |
| ALD | ASM 披露 single-wafer ALD share >55% | ASM、AMAT、TEL、Lam、Kokusai |
| Dry etch | Lam、TEL、AMAT 三强，AMEC/Naura 在中国替代 | Lam Research、Tokyo Electron、Applied Materials、AMEC、Naura |
| Deposition 综合 | AMAT 最大，ASM/TEL/Lam/Kokusai 分占强项 | AMAT、ASM、TEL、Lam、Kokusai、Piotech |
| Process control | KLA 绝对领先，细分由 ASML HMI/Nova/Onto/Lasertec 补充 | KLA、ASML HMI、Applied、Hitachi、Nova、Onto、Lasertec |
| Mask inspection | Lasertec 在 EUV mask inspection 极强，KLA 补充 | Lasertec、KLA、Applied、NuFlare/JEOL/IMS |
| Clean/CMP | SCREEN/TEL/Applied/Ebara/Lam/ACM/Hwatsing 分散 | SCREEN、TEL、AMAT、Ebara、Lam、ACM、Hwatsing |
| Ion implant | Applied Varian 和 Axcelis 核心 | Applied Materials、Axcelis、Nissin |
| 中国国产设备 | 成长快但高端完整性不足 | Naura、AMEC、ACM Research、Piotech、Hwatsing、SMEE、Kingsemi、Mattson China |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 可量化/事实线索 | 为什么能定价 |
|---|---|---|
| 技术壁垒 | EUV 单台数亿美元，High-NA 约 $350M-$400M 级别；GAA/DRAM/HBM 工艺窗口窄 | 客户无法用低价设备替代良率；失败一次节点 ramp 会损失数十亿美元机会 |
| 规模壁垒 | 全球领先设备厂年 R&D 多为数十亿美元级；TEL FY2027 R&D 计划 ¥330B | 只有头部能持续跟进 2nm/1.4nm/HBM4/High-NA |
| POR 锁定 | 设备和 recipe 在客户节点开发早期进入 process of record | 换设备要重做 recipe、可靠性、良率和客户认证，时间可达 6-18 个月 |
| 客户渠道壁垒 | TSMC/Samsung/Intel/SK/Micron 少数客户决定高端设备路线 | 进入头部客户后生命周期和服务收入长，反之很难切入 |
| 服务网络壁垒 | 高端 fab 24/7 运行，field engineer 和 spares 必须全球到位 | 客户为 uptime 付费，installed base service 形成高粘性 |
| 量测数据壁垒 | KLA/Nova/ASML HMI 等积累大量 defect/yield 数据 | 过程控制不是单台硬件，而是算法、数据库、recipe 和客户数据闭环 |
| 供应链组织壁垒 | ASML 依赖 Zeiss/Cymer/数千家供应商，Lam/AMAT/TEL 依赖全球精密零部件 | 组织复杂供应链本身成为稀缺能力 |
| 合规/出口壁垒 | 美国/荷兰/日本出口限制改变设备可获得性 | 可卖给高端非中国客户的产能更稀缺；中国本土替代获得政策溢价 |

### 5.3 长期高 ROIC / 高毛利最可能在哪里

| 层级 | 价值捕获判断 | 原因 |
|---|---|---|
| EUV/High-NA lithography | 最高 | ASML 垄断，客户路线强绑定，服务和升级长期高价值 |
| Process control / inspection / metrology | 最高之一 | 良率瓶颈强化，高毛利、软件算法和数据壁垒强 |
| ALD/Epi/selective deposition | 很高 | GAA、HBM、4F² DRAM、1.4nm 继续提高 layer intensity |
| 高端 etch | 很高 | HARC、GAA、interconnect、DRAM capacitor 是 AI 芯片和 HBM 必需 |
| Track/coater-developer | 高 | TEL >90% share，EUV/High-NA resist 工艺窗口更复杂 |
| Installed-base service | 高 | 收入递延性、客户锁定和高 fab utilization 支撑 |
| Clean/CMP | 中高 | 工艺必需且量大，但竞争比 EUV/量测更分散 |
| 中国国产替代设备 | 高 beta、分化大 | 政策和本土需求强，但技术、良率、客户国际化仍是约束 |

## 6. 2026 关键变化：三个拐点与最可能放量方向

### 拐点一：AI 设备需求从 NVIDIA 单线扩散为 GPU + ASIC + HBM 三线

2026 年 Blackwell Ultra 仍是最大主线，但 Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA、OpenAI/Broadcom XPU 都进入或接近 GW/百万颗级扩张。前道设备不再只跟 TSMC/NVIDIA，而是与 **TSMC N3/N2、Broadcom custom ASIC、AWS/Google/Microsoft/Meta 内部芯片、SK/Samsung/Micron HBM** 同时绑定。

最可能放量：Low-NA EUV、ArFi DUV、track、etch/deposition、HBM DRAM WFE、process control。

### 拐点二：HBM 把 DRAM 设备周期从“周期品”拉成“AI 瓶颈品”

HBM3E 主力、HBM4 验证、HBM4E 期权，使 DRAM 工艺设备从传统内存周期中脱钩一部分。AI 训练和推理都需要高带宽内存，客户对 HBM allocation 的价格敏感度低于传统 PC/手机 DRAM。

最可能放量：DRAM EUV、HARC etch、ALD/CVD、clean/CMP、HBM/DRAM metrology、services。

### 拐点三：2nm/GAA 和背面供电把设备价值量继续推高

2026 H2 到 2027，N2/N2P/A16/14A/1.4nm pilot 将让 GAA 相关 ALD/Epi/etch、选择性工艺、BSPDN、wafer bonding/debonding、背面 CMP/量测进入设备采购高峰。

最可能放量：ASM/AMAT/TEL/Lam 的 ALD/Epi/etch，KLA/Nova/Onto 的 3D 量测，EVG/SUSS/TEL/AMAT 的 bonding/debonding 相关设备。

## 7. 2027 关键变化：三个拐点与最可能放量方向

### 拐点一：Rubin/MI400/TPU8/OpenAI ASIC 进入 HBM4 + 2nm/GAA 时代

2027 的增量设备不再只是扩产 GB300，而是新平台切换。HBM4、N2/GAA、更多 custom ASIC tape-out 让前道设备订单的技术含量上升。

最可能放量：HBM4 DRAM WFE、N2/GAA equipment suite、High-NA early production、process control。

### 拐点二：High-NA EUV 从研发工具变成战略产能

基准情景下 High-NA 2027 仍是小比例；乐观情景下 Intel/Samsung/SK hynix 等客户会把 High-NA 写进部分高端路线，以降低多重曝光复杂度或抢先掌握 1.4nm/HBM4E 工艺窗口。

最可能放量：ASML EXE 系统、High-NA track/resist、metrology/overlay、mask ecosystem。

### 拐点三：中国和非中国高端设备链进一步分层

出口限制、主权 AI 和中国国产替代会让全球 WFE 市场出现两个并行周期：非中国高端 EUV/GAA/HBM 周期，以及中国 DUV 多重曝光/国产 etch-deposition-clean-metrology 周期。

最可能放量：中国本土刻蚀/沉积/清洗/CMP/涂胶显影/量测设备，以及成熟/可出口 DUV 设备。

## 8. 头部公司和细分技术地图

### 8.1 光刻、Track、掩膜

| 细分 | 公司 |
|---|---|
| EUV / High-NA EUV | ASML、Zeiss SMT、Cymer/ASML、Trumpf、Berliner Glas/ASML 生态 |
| DUV immersion / mature litho | ASML、Nikon、Canon、SMEE（中国替代） |
| Coater/developer track | Tokyo Electron、SCREEN、SEMES、SUSS MicroTec、Kingsemi |
| EUV resist / dry resist / MOR 生态 | Lam Research、JSR、TOK、Shin-Etsu、Fujifilm、Inpria/Japan ecosystem、imec、IBM Research |
| Mask writer / reticle | NuFlare、IMS Nanofabrication、JEOL、DNP、Toppan Photomask |
| Mask inspection/repair | Lasertec、KLA、Applied Materials、Carl Zeiss、Bruker/Rave、Park Systems |

### 8.2 刻蚀、沉积、热处理、注入

| 细分 | 公司 |
|---|---|
| Dielectric/conductor etch | Lam Research、Tokyo Electron、Applied Materials、Hitachi High-Tech、AMEC、中微公司、Naura、Oxford Instruments |
| ALD | ASM International、Applied Materials、Tokyo Electron、Lam Research、Kokusai Electric、Beneq、Piotech |
| CVD | Applied Materials、Lam Research、Tokyo Electron、ASM、Kokusai、Piotech、Naura |
| PVD / metal | Applied Materials、Lam Research、Ulvac、Canon Anelva、Naura |
| Epi | ASM、Applied Materials、Tokyo Electron、Veeco、LPE、Aixtron |
| Ion implant | Applied Materials/Varian、Axcelis、Nissin Ion Equipment、SMIT、Kingstone |
| RTP/anneal/oxidation/diffusion | Applied Materials、Tokyo Electron、Kokusai、ASM、Centrotherm、Naura |

### 8.3 清洗、CMP、湿法、电镀

| 细分 | 公司 |
|---|---|
| Single-wafer clean / wet station | SCREEN、Tokyo Electron、Lam Research、ACM Research、SEMES、Naura、Kingsemi |
| CMP tools | Applied Materials、Ebara、Hwatsing、Revasum、Logitech、Lapmaster |
| Plating / electrochemical deposition | Applied Materials、Lam Research、TEL、ClassOne、ACM Research |
| CMP slurry / pad / chemical materials | Entegris/CMC、Fujimi、DuPont、Cabot、Resonac、JSR、Fujifilm、Merck |

### 8.4 过程控制、量测、检测、良率软件

| 细分 | 公司 |
|---|---|
| Optical inspection / e-beam inspection | KLA、ASML HMI、Applied Materials、Hitachi High-Tech、Onto Innovation、Camtek |
| CD/overlay/metrology | KLA、ASML、Nova、Onto Innovation、Applied Materials、Hitachi、Bruker |
| Mask/reticle inspection | Lasertec、KLA、Applied Materials、NuFlare、JEOL |
| X-ray / 3D / materials metrology | Bruker、Thermo Fisher、Rigaku、ZEISS、Nova、Onto |
| Yield management / APC / analytics | KLA Klarity、Applied E3、Onto、PDF Solutions、Synopsys、Siemens EDA、Cadence、proteanTecs |

### 8.5 前道设备国产替代

| 细分 | 中国公司 |
|---|---|
| 刻蚀 | 中微公司 AMEC、北方华创 Naura、屹唐半导体、盛美上海部分湿法/等离子 |
| 沉积 | 北方华创、拓荆科技 Piotech、中微公司、盛美上海、微导纳米 |
| 清洗/湿法 | 盛美上海 ACM Research、北方华创、芯源微、至纯科技、芯碁微装相关 |
| CMP | 华海清科 Hwatsing、鼎龙股份 CMP 材料、安集科技材料 |
| 涂胶显影/Track | 芯源微、沈阳芯源、Kingsemi、SCREEN/TEL 仍强 |
| 光刻 | 上海微电子 SMEE、芯碁微装（直写/封装/PCB 更强）、华卓精科等生态 |
| 量测检测 | 中科飞测、上海精测、睿励科学仪器、东方晶源、天准科技、赛腾股份相关 |
| 离子注入/热处理 | 万业企业/凯世通、中科信、北方华创、屹唐半导体 |

### 8.6 关键零部件、材料和供应链

| 细分 | 公司 |
|---|---|
| 真空泵/真空阀/系统 | Edwards/Atlas Copco、Pfeiffer、Ebara、VAT、ULVAC、Kashiyama、Leybold |
| RF power / MFC / gas delivery | MKS Instruments、Advanced Energy、Horiba、Brooks、Ichor、Ultra Clean、Fujikin |
| ESC / ceramics / quartz | Kyocera、CoorsTek、NGK、Ferrotec、TOTO、Shin-Etsu Quartz、Heraeus |
| 光学/精密机构 | Zeiss、Trumpf、ASML ecosystem、Aerotech、Newport/MKS、THK、NSK |
| 硅片/wafer | Shin-Etsu Handotai、SUMCO、GlobalWafers、Siltronic、SK Siltron、沪硅产业 |
| Photoresist / chemicals / gases | JSR、TOK、Shin-Etsu、Fujifilm、Merck/EMD、Entegris、Air Liquide、Linde、SK Materials、Kanto Chemical |

## 9. 投资排序和跟踪指标

### 9.1 未来 3-12 个月最确定

1. **ASML EUV/DUV 与 installed-base management**：AI 先进逻辑和 HBM DRAM 双轮驱动，High-NA 作为长期期权。
2. **TEL Track + Lam/TEL/AMAT etch + AMAT/ASM/TEL/Lam deposition**：直接受益 GB300、ASIC、HBM、GAA。
3. **KLA/Nova/Onto/Lasertec process control**：工艺越复杂，量测检测越像刚需保险。
4. **HBM DRAM 设备链**：DRAM EUV、HARC etch、ALD/CVD、clean/CMP、metrology。
5. **Service/spares/upgrades**：高利用率和升级需求带来比新机更稳的利润。

### 9.2 未来 12-24 个月赔率最高

1. **High-NA EUV ecosystem**：ASML、Zeiss、High-NA track/resist/metrology/mask。
2. **BSPDN/backside processing equipment**：bonding/debonding、backside etch/CMP/metrology。
3. **4F² DRAM/HBM4E equipment**：内存厂 capex 上修最敏感。
4. **Dry resist/MOR 与 EUV stochastic control**：若被客户验证，可从小基数快速放量。
5. **中国国产设备替代**：政策 beta 强，但应优先看已进入量产线和关键 POR 的公司。

### 9.3 需要持续跟踪的指标

1. ASML quarterly net bookings、EUV/DUV mix、High-NA shipments、2026/2027 revenue guidance 是否继续上修。
2. Lam/AMAT/TEL/ASM 对 CY2026 WFE 增长、DRAM/HBM、leading-edge logic 的表述是否继续加强。
3. KLA/Nova/Onto 的 backlog、process control revenue、e-beam inspection 增速和毛利率。
4. TSMC N2/A16、Samsung 2nm、Intel 14A 的真实 ramp 进度和 High-NA 采用节奏。
5. SK hynix/Samsung/Micron HBM4/HBM4E capex、EUV orders、DRAM equipment intensity。
6. 中国出口管制变化：DUV、etch、deposition、metrology 的许可范围和国产替代订单。
7. 客户 cleanroom/装机验收周期是否成为收入确认瓶颈。
8. EUV resist/dry resist/MOR 在 SPIE/imec/客户节点的缺陷率、剂量、throughput 指标。

## 10. 主要来源与交叉验证

### 一手公司与行业组织

| 来源 | 本文使用的信息 |
|---|---|
| [SEMI 300mm Fab Equipment Spending 2026/2027](https://www.semi.org/en/semi-press-release/semi-projects-double-digit-growth-in-global-300mm-fab-equipment-spending-for-2026-and-2027) | 2026 300mm equipment spending $133B、2027 $151B，AI 和先进节点驱动 |
| [SEMI Total Semiconductor Equipment Forecast](https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports) | 总设备销售 2025/2026/2027 为 $133B/$145B/$156B；WFE 2025 $115.7B，2027 $135.2B |
| [SEMI Silicon Wafer Shipments Q1 2026](https://www.semi.org/en/semi-press-release/semi-reports-worldwide-silicon-wafer-shipments-increase-13-percent-year-on-year-in-q1-2026) | Q1 2026 硅片出货 3,275 MSI，同比 +13.1%；AI logic/memory/power demand 强 |
| [SIA Q1 2026 Semiconductor Sales](https://www.semiconductors.org/global-semiconductor-sales-increase-25-from-q4-2025-to-q1-2026/) | 2026Q1 全球半导体销售 $298.5B；3月 $99.5B，同比 +79.2% |
| [Gartner 2026 Semiconductor Forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | 2026 半导体收入超 $1.3T，AI 半导体约占 30% |
| [ASML Q1 2026 results](https://www.asml.com/en/investors/financial-results/q1-2026) | Q1 2026 销售 €8.8B、毛利率 53.0%、EPS €7.15；FY2026 指引 |
| [Applied Materials Q1 FY2026 results](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-announces-first-quarter-2026-results) | Q1 收入 $7.012B、非 GAAP GM 49.1%；AI/HBM/advanced logic 最快增长；CY26 半导体设备 +20%+ |
| [Lam Research March 2026 quarter results](https://www.prnewswire.com/news-releases/lam-research-corporation-reports-financial-results-for-the-quarter-ended-march-29-2026-302750629.html) | 3月季度收入 $5.841B、非 GAAP GM 49.9%、6月季度指引 $6.60B +/- $0.40B |
| [KLA FY2026 Q3 results](https://ir.kla.com/news-events/press-releases/detail/514/kla-corporation-reports-fiscal-2026-third-quarter-results) | 6月季度收入指引 $3.575B +/- $0.2B，非 GAAP GM 61.75% +/- 1% |
| [Tokyo Electron FY2026 results presentation](https://www.tel.com/ir/) | FY2026 净销售 ¥2.4435T；FY2027 H1 AI server demand 驱动；coater/developer >90% share；SPE new equipment +41% |
| [ASM International Q1 2026 results](https://www.globenewswire.com/news-release/2026/04/21/3278259/0/en/ASM-reports-first-quarter-2026-results.html) | Q1 revenue €863M、GM 53.3%、AI-led demand、HBM DRAM 和先进逻辑驱动 |
| [ASM Q1 2026 investor presentation](https://www.asm.com/media/olsd33sa/asm_q126_investor_presentation.pdf) | ALD share >55%；GAA 和 4F² DRAM 提高 ALD/Epi SAM |
| [TSMC Q1 2026 results](https://investor.tsmc.com/english/quarterly-results/2026/q1) | Q1 revenue $35.90B、GM 66.2%、Q2 revenue guide $39.0B-$40.2B、HPC/advanced nodes 强 |
| [Lam / IBM Aether dry resist collaboration](https://newsroom.lamresearch.com/ibm-lam-sub-1nm-logic-aether-dry-resist) | Dry resist、High-NA EUV、etch/deposition 工艺合作 |
| [Lam: Deposition and Etch for AI Era](https://newsroom.lamresearch.com/how-deposition-and-etch-are-reshaping-chips-for-the-ai-era?blog=true) | HBM、GAA、backside power delivery 增加沉积/刻蚀需求 |
| [imec receives ASML EXE:5200 High NA EUV](https://www.imec-int.com/en/press/imec-receives-worlds-most-advanced-high-na-euv-system) | 2026-03 imec 接收 EXE:5200 High-NA EUV |
| [ASML EUV lithography systems](https://www.asml.com/en/products/euv-lithography-systems) | EUV/High-NA 技术路线和产品说明 |

### 项目内资料

| 项目内文件 | 用途 |
|---|---|
| `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md` | 2026-2027 出货量最大 AI 芯片平台与技术路线 |
| `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_商用AI加速芯片_2026.md` | AI 芯片市场规模、GPU/ASIC/HBM 需求锚 |
| `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_云厂自研AI_ASIC_2026.md` | Google/AWS/Microsoft/Meta/OpenAI custom ASIC 需求 |
| `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_HBM与高带宽内存_2026.md` | HBM3E/HBM4 和 DRAM capex 约束 |
| `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_AI芯片先进封装_2026.md` | CoWoS/HBM/测试与前道设备外延约束 |
| `D:\drive\Investment\调研\v5\conference_update\nvidia_gtc_2026_research.md` | Rubin、GB300、LPX、STX、AI factory 路线 |
| `D:\drive\Investment\调研\v5\conference_update\chiplet_summit_2026_update.md` | HBM4/custom HBM、UCIe、先进封装和 3DIC 会议信号 |

---

**最终判断：**  
2026 年 AI 芯片前道制造设备的投资价值来自“AI 算力需求比先进制程和 HBM 产能扩张更快”。基准情景下，最强确定性是 Low-NA EUV/DUV、track、etch、deposition、HBM DRAM WFE 和 process control；乐观情景下，GB300 与 ASIC/HBM 同时放量，设备服务和升级形成第二利润池；极度超预期情景下，2027 Rubin/MI400/TPU8/OpenAI ASIC 需求提前，High-NA、BSPDN、4F² DRAM、dry resist 和 multi-beam inspection 被市场提前定价。长期看，最优质的价值捕获层是 ASML、KLA、TEL track、ASM ALD/Epi、Lam/AMAT/TEL 高端 etch/deposition，以及能进入中国本土先进逻辑/HBM 量产线 POR 的国产设备龙头。
# 行业调研：【HBM与存储测试设备】

> 写作截点：2026-05-08  
> 研究口径：本报告把“HBM与存储测试设备”拆为两条强绑定产业链：1）HBM/HBM4/SOCAMM/AI DDR5/企业级SSD等高带宽存储本体；2）支撑 HBM 和 AI xPU 量产的测试设备，包括 memory ATE、SoC ATE、probe card、wafer probe、handler/contactor/socket、burn-in/SLT、HBM inspection/metrology、SSD/HDD/board/system test、测试软件与良率分析。  
> 情景口径：基准 / 乐观 / 极度超预期乐观。用户要求对 2026 AI 基础设施建设采用非常乐观预期；因此本报告在缺少直接公司披露时，用本项目 AI 芯片出货底稿、HBM stack 数、Advantest/Teradyne/Cohu/FormFactor 一手披露、HBM 厂商公告与数据中心 CapEx 做大胆推演。  
> 注意：HBM 成品、封装测试服务、ATE、探针卡、socket/handler、SLT 之间存在上下游嵌套，表中市场规模不能简单相加。

## 0. 一页结论

**核心判断：2026 年这个行业的投资价值不在“内存周期复苏”，而在“AI xPU 交付被 HBM 与测试共同卡住”。** B300/GB300、TPU Ironwood、Trainium2/3、Maia200、MTIA、MI350 等 2026 主力平台普遍绑定 HBM3E；Rubin、MI400/MI455X、TPU8、OpenAI/Broadcom、Meta/Broadcom 下一代 XPU 从 2026H2 开始把 HBM4/HBM4E、KGD、probe、package test、burn-in 和高功率 SLT 推成新瓶颈。

最重要的 8 个事实锚点：

1. **Advantest 把 CY2026 SoC tester TAM 估到约 $8.7-9.5B，memory tester TAM 估到 $2.2-2.7B。** 公司 FY2025 销售额 JPY1.1286T、营业利润率 44.2%，并给 FY2026 销售额 JPY1.42T、营业利润率 44.2% 指引；其 FY2025 SoC tester 份额约 66%、memory tester 份额约 61%。
2. **Teradyne Q1 2026 收入 $1.282B，同比 +87%；Semiconductor Test 单季 $1.111B，首次超过 $1B。** 公司称约 70% 收入 tied to AI；10-Q 明确 memory test 近纪录，来自 HBM/DRAM；电话会披露 memory revenue $203M，SoC $882M。
3. **FormFactor Q1 2026 收入 $226.1M，同比 +32%，创纪录；非 GAAP 毛利率 49.0%。** 公司明确称 DRAM revenue 创纪录，HBM application 需求增加，Foundry & Logic 受 AI networking probe cards 拉动。
4. **Cohu Q1 2026 收入 $125.1M、非 GAAP 毛利率 46.5%，把 AI-driven compute addressable market 上调到约 $750M，把 FY2026 HPC revenue outlook 上调到约 $80-100M。** Cohu 2026 年 3-4 月连续披露 Eclipse AI/HPC test order、$30M follow-on orders；Neon HBM inspection 2025 revenue outlook 已上调到 $10-11M。
5. **HBM 成品 2026 已是 $50B+ 收入池。** 本项目 HBM 底稿锚定 SK hynix 新闻室引用的 BofA 估算：2026 HBM 市场约 $54.6B、同比 +58%；在极度乐观情形下，若 AI 推理需求继续吞掉所有新增供给，2026 HBM 单品收入可冲 $85-110B。
6. **测试设备是 HBM4 放量的隐性瓶颈。** HBM4 2048-bit I/O、10-11Gbps+ speed-per-pin、12Hi/16Hi、logic base die、CoWoS/SoIC/EMIB、ULFF package 和 700W-1200W 级 xPU 会显著增加 test insertion、test time、socket force、thermal control 和良率分析复杂度。
7. **价值捕获顺序：HBM 成品 > ATE/probe card/test software > thermal handler/socket/SLT > OSAT 测试服务。** HBM 厂商毛利在短缺期可达 60-80%；测试设备毛利多在 50-65%，软件/IP/良率分析可更高；OSAT 收入弹性大但毛利和 ROIC 通常低于设备/IP。
8. **2026 最可能放量路径：HBM3E 12Hi + high-parallel memory ATE + HBM KGD probe card + AI xPU SoC ATE + high-power thermal test。** 2027 最大弹性路径：HBM4/4E + 16Hi + custom HBM + hybrid bonding + wafer-level burn-in + rack/system-level test。

## 1. 2026 AI 计算中心建设下的机遇、挑战与技术路径

### 1.1 机会：AI 算力从“买 GPU”变成“买可交付的 HBM-xPU-test stack”

2026 年 AI 计算中心大规模建设对 HBM 与测试设备有四层放大效应：

| 放大层 | 机制 | 对 HBM 的影响 | 对测试设备的影响 |
|---|---|---|---|
| 芯片数量 | GPU/ASIC/LPU/TPU 同时扩产，AI 推理 token 增速高于训练 | HBM3E 12Hi 继续满载，HBM4 被提前锁产能 | memory ATE、probe card、SLT 同步扩张 |
| 单芯片内存容量 | B300/GB300 最高 288GB HBM3E，Maia200 216GB HBM3E，MI455X 目标 432GB HBM4 | 单 xPU stack 数/容量/ASP 上升 | KGD、parallel test、HBM stack test time 增加 |
| 封装复杂度 | CoWoS-L/S、2.5D、interposer、large organic substrate、HBM base die | 良率与可测性决定有效供给 | inspection/metrology、warpage、micro-pillar AOI 增量 |
| 系统级可靠性 | NVL72、Trainium UltraServer、TPU pod、OCP rack、closed-loop liquid cooling | HBM 与 xPU 故障成本从芯片级放大到 rack 级 | burn-in、SLT、board test、rack test、thermal cycling 价值上升 |

### 1.2 挑战：2026 的瓶颈不是单一设备，而是测试链复合瓶颈

1. **HBM KGD 约束：** HBM 在堆叠前必须尽可能筛出 known-good die；12Hi/16Hi 使单 stack 失效率杠杆放大。
2. **测试时间变长：** HBM4 带宽、I/O 数、低功耗模式、ECC、temperature corner 变多；xPU package 还要测 SerDes/NVLink/UALink/NeuronLink/PCIe/CXL。
3. **高功率热控：** AI package 从传统 socket test 走向 active thermal control、liquid-cooled SLT、ultra-large form factor package 支撑。
4. **探针卡和 space transformer：** HBM pitch、pad 数、parallelism、planarity、cleaning cycle 和寿命成为良率变量。
5. **设备供应链反向被内存卡住：** Advantest Q&A 提到 tester 自身也使用大量 memory semiconductors，受供应约束影响。
6. **客户认证周期：** NVIDIA/AMD/Google/AWS/Microsoft/Meta/OpenAI/Broadcom 的 test flow 一旦导入，切换平台通常需要多季度验证。
7. **人才与软件：** DFT/BIST、test program conversion、yield analytics、failure diagnostics 和 package/thermal co-design 人才不足。
8. **出口管制与区域化：** 中国 AI 芯片、国产 HBM、国产 ATE/探针卡会形成替代市场，但先进测试能力仍有缺口。

### 1.3 项目内 2026-2027 出货量最大 AI 芯片路径对测试设备的含义

以下芯片路径来自项目内 `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`，本节只抽取对 HBM/测试设备的含义。

| 排名 | AI 芯片/平台 | 2026-2027 出货逻辑 | HBM/内存路径 | 最关键测试需求 |
|---:|---|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | 2026 Blackwell 主力 | 每 GPU 最高 288GB HBM3E，NVL72 rack | SoC ATE、HBM3E KGD、CoWoS package test、NVLink/NVSwitch、rack burn-in |
| 2 | AWS Trainium2 | Project Rainier 近 50 万颗，Anthropic 目标百万级 | HBM + NeuronLink | ASIC ATE、HBM KGD、UltraServer SLT、EFA/NeuronLink 系统测试 |
| 3 | Google TPU v7 Ironwood | Google Cloud + Anthropic 扩容 | 192GB HBM、7.37TB/s | Broadcom/Google XPU test、HBM3E、pod 级互连与高良率筛选 |
| 4 | NVIDIA B200/GB200 | 既有订单延续 | HBM3E，GB200 NVL72 | 成熟 CoWoS/HBM3E test flow 延续，价格压力低于产能压力 |
| 5 | Huawei Ascend 910C/950 | 中国国产替代第一梯队 | 910C/950 受国产 HBM 与封装约束 | 国产 ATE、国产 probe card、OAM/system burn-in、先进节点良率诊断 |
| 6 | Cambricon MLU 590/690 | 2026 目标约 50 万颗级别 | HBM + MLU-Link | 本土 memory/logic test、OAM module test、国产供应链认证 |
| 7 | AMD MI350X/MI355X/MI350P | 2026 AMD 最确定放量 | HBM3E，UBB/PCIe/OAM | HBM3E KGD、PCIe/OAM 多形态 SLT、ROCm compatibility test |
| 8 | AWS Trainium3 | 3nm UltraServer，144 芯片 scale-up | HBM3E 级别，2027 主力 | 3nm ASIC ATE、HBM、high-speed fabric、large system burn-in |
| 9 | Meta MTIA 300/400/450/500 | 2026-2027 四代迭代，Broadcom XPU | GenAI inference，内存带宽上升 | Broadcom XPU test、Ethernet/SerDes、HBM/controller、OCP rack test |
| 10 | Microsoft Maia 200 | Azure/Copilot/OpenAI 推理导入 | 216GB HBM3E、7TB/s、272MB SRAM | 3nm SoC ATE、HBM3E、closed-loop liquid cooling SLT |
| 关键补充 | NVIDIA Rubin / AMD MI400 / OpenAI-Broadcom XPU | 2026H2 小批量，2027 主力增量 | HBM4/HBM4E，MI455X 目标 432GB HBM4 | HBM4 memory ATE、16Hi probe、thermal SLT、custom ASIC test program |

### 1.4 新技术成熟与放量时间：三情景

| 技术 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 | 2026 最可能路径 |
|---|---|---|---|---|
| HBM3E 12Hi | 已成熟，2026 全年主力；2027 仍在中高端推理延续 | 2026 ASP 高位、供给被 B300/GB300/ASIC 锁定 | 2026 全年缺货，客户接受溢价换交期 | **第一主线** |
| HBM4 12Hi | 2026Q2 多客户验证，2026H2 Rubin/MI400/ASIC 小批量，2027 放量 | 2026Q3/Q4 多供应商稳定出货 | 2026Q4 成最高端新增默认配置 | **第二主线，2027 主力** |
| HBM4 16Hi | 2026 样品，2027H2 放量 | 2027H1 高端训练平台采用 | 2026Q4 最高端客户小批量 | 2026 看 design-win |
| HBM4E / cHBM | 2026H2 样品，2027H2 放量 | 2027H1 随 Rubin Ultra/下一代 ASIC 提前 | 2027Q1 客户定制 base die 商业化 | 2026 是订单和验证期 |
| memory ATE for HBM4 | 2026 新 tester/module 投入，2027 二次扩产 | 2026H2 交期拉长、价格上行 | 2026Q3 即成为 HBM4 ramp 的排产瓶颈 | 2026 HBM4 tester 供需偏紧 |
| HBM probe card / space transformer | 2026 随 HBM3E/HBM4 满产 | HBM4/16Hi 带来替换周期 | 探针卡交期成为局部瓶颈 | 2026 确定放量 |
| active thermal handler/socket | 2026 AI/HPC package test 加速 | Cohu Eclipse 类平台快速多客户导入 | 2026H2 大客户急单，价格溢价 | 2026 从边缘环节变主线 |
| SLT / burn-in / rack test | 2026 system-level test 比重上升 | 2027 rack 级 test cell 规模化 | 2026Q4 NVL72/UltraServer/AI rack 交付瓶颈 | 2026 后半段放量 |
| SiPh/CPO test | 2026 初步量产，Advantest/Teradyne 均有量产订单/产品 | 2027 >2x，2028 再 >2x | 2027 CPO 提前进入高端 AI switch | 2026 收入小但弹性大 |
| AI yield analytics / virtual test | 2026 TestInsight、Tignis 类资产进入主流 | 2027 SLM/DFT/analytics 与 ATE 捆绑 | 2027 软件毛利池显著扩大 | 2026 开始商业化 |

## 2. 已开始放量的关键产品：市场规模、渗透率、利润率

本节“未来 3 个月 / 未来 1 年 / 未来 2 年”均从 2026-05-08 向后滚动计算。

### 2.1 HBM 与 AI 高带宽存储本体

| 已放量产品 | 主要公司 | 未来 3 个月市场规模：基准/乐观/极度乐观 | 未来 1 年市场规模：基准/乐观/极度乐观 | 未来 2 年市场规模：基准/乐观/极度乐观 | 渗透率路径 | 毛利率三情景 |
|---|---|---:|---:|---:|---|---|
| HBM3E 8Hi/12Hi | SK hynix、Samsung、Micron | $12-18B / $18-24B / $25-32B | $42-55B / $55-70B / $70-90B | $55-80B / $80-120B / $110-160B | 2026 AI HBM bit 60-70%；2027 35-50%；2028 20-35% | 58-70% / 68-78% / 75-85% |
| HBM4 12Hi | Samsung、Micron、SK hynix | $2-6B / $6-10B / $10-16B | $18-32B / $35-55B / $60-85B | $65-105B / $100-160B / $150-230B | 2026 8-18%；2027 35-55%；2028 45-65% | 62-75% / 72-82% / 80-88% |
| SOCAMM2 / AI LPDDR server module | Micron、Samsung、SK hynix | $0.8-2B / $2-4B / $4-7B | $5-12B / $12-22B / $22-35B | $15-35B / $35-65B / $65-110B | AI CPU/Vera/Grace 类节点 2026 5-15%；2027 20-45%；2028 35-60% | 45-58% / 55-68% / 65-75% |
| AI DDR5 / RDIMM / MRDIMM | Samsung、SK hynix、Micron、Montage、Rambus | $6-12B / $12-20B / $20-30B | $35-65B / $65-100B / $100-150B | $70-130B / $130-220B / $220-350B | AI CPU/推理 prefill 内存 attach 2026 25-40%；2027 40-60%；2028 55-75% | 42-58% / 55-68% / 65-78% |
| 企业级 SSD / PCIe Gen5-6 SSD / AI cache storage | Samsung、SK hynix/Solidigm、Micron、Kioxia、Western Digital/SanDisk、Phison、Marvell、Silicon Motion | $8-16B / $16-25B / $25-40B | $50-90B / $90-150B / $150-230B | $100-180B / $180-300B / $300-500B | AI data lake、KV cache、RAG 存储 2026 15-30%；2027 30-50%；2028 45-70% | 35-55% / 50-65% / 60-75% |

### 2.2 已放量测试设备与测试耗材

| 已放量产品/技术 | 龙头/优势公司 | 一手证据与状态 | 未来 3 个月市场规模：基准/乐观/极度乐观 | 未来 1 年市场规模：基准/乐观/极度乐观 | 未来 2 年市场规模：基准/乐观/极度乐观 | 渗透率路径 | 毛利率三情景 |
|---|---|---|---:|---:|---:|---|---|
| Memory ATE：HBM/DRAM/NAND tester | Advantest、Teradyne、Chroma、长川科技/华峰测控等 | Advantest CY2026 memory tester TAM $2.2-2.7B；Teradyne Q1 memory revenue $203M，Magnum 7 ramp | $0.6-0.8B / $0.8-1.0B / $1.0-1.3B | $2.4-3.2B / $3.2-4.2B / $4.2-5.8B | $5-8B / $8-12B / $12-18B | 高端 HBM/DRAM 测试 attach 近 100%；HBM4 tester 占 memory tester 新增 2026 15-25%、2027 35-55% | 55-65% / 60-68% / 65-72% |
| SoC ATE：AI GPU/ASIC/CPU/XPU | Advantest V93000、Teradyne UltraFLEXplus/UltraFLEX、Cohu Diamondx/Eclipse、Chroma 3680 | Advantest CY2026 SoC tester TAM $8.7-9.5B；Teradyne Semi Test Q1 $1.111B | $2.2-2.7B / $2.7-3.3B / $3.3-4.2B | $9-11B / $11-14B / $14-18B | $20-25B / $25-35B / $35-50B | AI/HPC/compute 占 SoC tester 新增 2026 70-85%；2027 75-90% | 58-65% / 62-68% / 66-72% |
| HBM/DRAM probe card、space transformer、advanced probe | FormFactor、Micronics Japan、Technoprobe、MPI、TSE、CHPT、Japan Electronic Materials、LEENO/ISC | FormFactor Q1 2026 record DRAM revenue，HBM demand 增加；MJC 受 HBM4 probe card outlook 拉动 | $0.6-0.9B / $0.9-1.3B / $1.3-1.8B | $3-4.5B / $4.5-6.5B / $6.5-9B | $7-11B / $11-16B / $16-25B | HBM wafer probe attach 100%；HBM4/16Hi 换代使高端 probe card 渗透 2026 25-40%、2027 45-65% | 45-58% / 55-65% / 60-70% |
| HBM package inspection/metrology：micro-pillar、6-sided AOI、warpage | Cohu Neon、KLA、Onto、Camtek、Chroma、Nova、Lasertec | Cohu Neon 2025 HBM revenue 估 $10-11M，并称该类 inspection/metrology 系统 opportunity >$100M | $0.08-0.15B / $0.15-0.25B / $0.25-0.40B | $0.4-0.8B / $0.8-1.3B / $1.3-2.0B | $1-2B / $2-3.5B / $3.5-6B | HBM3E 后段 inspection 2026 30-50%；HBM4/16Hi 2027 60-80% | 45-55% / 52-62% / 60-68% |
| High-power thermal handler、socket、contactor | Cohu Eclipse/handler、Advantest、Teradyne、WinWay、ISC、LEENO、Smiths、Yamaichi、Hon Precision | Cohu 2026 Eclipse 第二客户、多客户订单、$30M follow-on；AI/HPC package 需要 active thermal control | $0.2-0.4B / $0.4-0.6B / $0.6-0.9B | $1-1.8B / $1.8-3B / $3-5B | $2.5-4.5B / $4.5-8B / $8-14B | AI xPU package test active thermal attach 2026 35-55%；2027 60-80% | 40-55% / 50-62% / 58-68% |
| Burn-in / SLT / module-board-rack test | Teradyne IST/Product Test/Omnyx、Advantest、Aehr、Cohu、Chroma、NI/Emerson、Keysight | Teradyne 推 Omnyx board test、IST 进入 SLT compute；AI rack defects 需要更早发现 | $0.4-0.8B / $0.8-1.2B / $1.2-1.8B | $2-3.5B / $3.5-5.5B / $5.5-8.5B | $5-8B / $8-13B / $13-22B | Rack-scale AI 平台 SLT attach 2026 40-60%；2027 65-85% | 42-55% / 50-62% / 58-70% |
| SSD/NAND/HDD/storage test | Teradyne、Advantest、Chroma、Keysight、Cohu、Phison/Marvell ecosystem | Teradyne 称 flash test demand 由 SSD 驱动，HDD exabyte growth >20% 拉长 test time | $0.2-0.5B / $0.4-0.8B / $0.8-1.2B | $1.5-2.5B / $2.5-4B / $4-6B | $3.5-6B / $6-10B / $10-15B | AI storage/nearline/HDD/SSD test 2026 15-25%；2027 25-40% | 35-48% / 45-55% / 52-62% |
| Test software、DFT/SLM、yield analytics、virtual test | Teradyne TestInsight、Cohu Tignis、Advantest ACS/Cloud、PDF Solutions、proteanTecs、Synopsys、Cadence、Siemens EDA | Teradyne 2026 收购 TestInsight；Cohu 推 analytics；复杂 AI devices 需要 design-to-test | $0.15-0.3B / $0.3-0.5B / $0.5-0.8B | $0.8-1.5B / $1.5-2.5B / $2.5-4B | $2-4B / $4-7B / $7-12B | 高端 AI tape-out/test flow 2026 20-35%；2027 40-60%；2028 60-80% | 70-85% / 80-90% / 85-95% |

### 2.3 增长预测区间：已放量产品

| 产品/技术 | 基准增长 | 乐观增长 | 极度超预期乐观增长 |
|---|---|---|---|
| HBM3E | 未来 12 个月 +35-55%，2027 被 HBM4 分流 | +55-80%，B300/ASIC 同步上修 | +80-130%，全年缺货且 ASP 上调 |
| HBM4 | 未来 12 个月从低基数 +3-5x | +5-8x，多供应商验证顺利 | +8-12x，2026H2 成新增高端默认 |
| memory ATE | +20-35%，HBM4 tester 开始贡献 | +35-60%，HBM4/DDR5/SSD 共同扩产 | +60-100%，test time 增长导致设备需求非线性放大 |
| SoC ATE | +25-45%，AI xPU 复杂度提高 | +45-70%，Rubin/ASIC/MI400 多客户导入 | +70-120%，GPU+ASIC 不互相挤出 |
| probe card | +30-55%，HBM4 替换周期 | +55-85%，HBM4/16Hi/AI networking 共振 | +85-140%，probe card 交期成为出货瓶颈 |
| thermal handler/socket | +50-90%，AI package 高功耗化 | +90-140%，active thermal 成标配 | +140-220%，rack-scale test cell 缺货 |
| SLT/rack test | +40-80%，NVL72/UltraServer 拉动 | +80-130%，云厂强化早期筛错 | +130-220%，系统缺陷成本迫使更多 test insertion |
| test software/analytics | +60-100%，复杂设备带动 | +100-180%，与 ATE 捆绑销售 | +180-300%，virtual test/SLM 成大客户标准 |

## 3. 在研关键产品与细分技术：未来放量预测

| 在研/早期产品 | 代表公司 | 成熟/放量判断 | 未来 3 个月市场规模：基准/乐观/极度乐观 | 未来 1 年市场规模：基准/乐观/极度乐观 | 未来 2 年市场规模：基准/乐观/极度乐观 | 渗透率路径 | 利润率三情景 |
|---|---|---|---:|---:|---:|---|---|
| HBM4E 16Gbps/pin、4TB/s+ stack | Samsung、Micron、SK hynix | 2026H2 sampling，2027 放量 | $0-1B / $1-3B / $3-6B | $8-20B / $20-45B / $45-75B | $60-120B / $120-220B / $220-350B | 2026 <5%；2027 10-25%；2028 30-50% | 65-78% / 75-85% / 82-90% |
| 16Hi HBM4 / 48GB stack | Micron、Samsung、SK hynix | 2026 样品，2027H1-H2 最高端采用 | $0.5-2B / $2-4B / $4-8B | $10-25B / $25-50B / $50-85B | $70-140B / $140-250B / $250-420B | 高端训练/长上下文平台 2027 15-35%；2028 35-60% | 65-80% / 75-86% / 82-90% |
| custom HBM / cHBM / custom base die | Samsung、SK hynix+TSMC、Micron、Broadcom/Marvell ecosystem | 2027 sample/早期量产，2028 扩散 | $0-0.5B / $0.5-1.5B / $1.5-3B | $4-12B / $12-30B / $30-60B | $40-100B / $100-220B / $220-400B | 自研 ASIC attach 2027 5-15%；2028 20-40% | 65-80% / 78-88% / 85-92% |
| hybrid copper bonding for HBM/3D memory | Besi、ASMPT、EVG、SUSS、TEL、Applied Materials | 2026 qualification，2027 高端 HBM4E/16Hi 放量 | $0.1-0.3B / $0.3-0.6B / $0.6-1B | $0.8-1.8B / $1.8-3.5B / $3.5-6B | $3-7B / $7-14B / $14-25B | 高端 HBM/3D stack 2027 10-25%；2028 25-45% | 55-65% / 62-70% / 68-75% |
| wafer-level burn-in / known-good-stack flow | Aehr、Advantest、Teradyne、FormFactor、memory IDM 自研 | HBM4/16Hi 失效率成本推动 | $0.05-0.15B / $0.15-0.3B / $0.3-0.6B | $0.5-1.2B / $1.2-2.5B / $2.5-5B | $2-5B / $5-10B / $10-18B | HBM4/4E 2027 10-25%；2028 30-50% | 50-62% / 58-68% / 65-75% |
| CPO/SiPh ATE and optical package test | Advantest、Teradyne Photon 100、Keysight、Chroma、FormFactor、MPI | 2026 初量产，2027>2x，2028 再>2x | $0.1-0.3B / $0.3-0.5B / $0.5-0.9B | $0.8-1.5B / $1.5-3B / $3-5B | $3-7B / $7-14B / $14-25B | AI switch/CPO 2026 <5%；2027 5-12%；2028 10-25% | 55-68% / 65-75% / 70-82% |
| Rack-level AI system test and digital twin | Teradyne Omnyx/MultiLane、Keysight、NI/Emerson、Chroma、NVIDIA/ODM internal | 2026 board/tray test，2027 rack factory 标准化 | $0.2-0.5B / $0.5-0.9B / $0.9-1.5B | $1.5-3B / $3-6B / $6-10B | $5-12B / $12-25B / $25-45B | NVL72/UltraServer/OCP rack 2026 20-35%；2027 45-70% | 45-58% / 55-68% / 65-75% |
| AI-native test data platform / closed-loop yield | Teradyne TestInsight、Cohu Tignis、Advantest、PDF Solutions、proteanTecs、Synopsys/Cadence SLM | 2026 进入大客户 flow，2027 高端 xPU 标配 | $0.1-0.25B / $0.25-0.5B / $0.5-0.8B | $0.8-1.5B / $1.5-3B / $3-5B | $3-7B / $7-14B / $14-25B | 高端 AI chip test flow 2026 20-35%；2027 45-65%；2028 65-85% | 75-88% / 82-92% / 88-95% |
| HBF / high bandwidth flash test | SanDisk/WD、SK hynix/Solidigm、Kioxia、Micron、Samsung；test by Advantest/Teradyne/Chroma | 2026-2028 标准/研发，主放量更靠 2029+ | $0-0.05B / $0.05-0.1B / $0.1-0.2B | $0.2-0.5B / $0.5-1B / $1-2B | $1-3B / $3-6B / $6-12B | 2027 <3%；2028 3-8%；长期用于 KV cache | 45-60% / 55-68% / 65-75% |

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 核心公司 | 产能/工艺特征 |
|---|---|---|---|
| HBM DRAM die | 韩国、美国、日本、中国潜在 | SK hynix、Samsung、Micron、CXMT 潜在 | 1bnm/1c/1-gamma 等 DRAM 节点，TSV、薄化、stack bonding；HBM4 logic base die 引入 foundry 协同 |
| HBM assembly / stack / P&T | 韩国、日本、台湾、美国、马来西亚 | SK hynix、Samsung、Micron、Hana Micron、PTI、ASE 等 | MR-MUF、TC bonding、hybrid bonding、KGD；P&T capacity 决定 effective bit |
| Memory ATE | 日本、美国、台湾、中国 | Advantest、Teradyne、Chroma、长川科技、华峰测控 | 高并行、高速 memory channel、temperature corner、repair/ECC test |
| SoC ATE | 日本、美国、台湾、中国 | Advantest、Teradyne、Cohu、Chroma、SPEA、长川科技、华峰测控 | V93000/UltraFLEXplus/Diamondx/3680 等；AI xPU 高速 I/O、power、thermal 复杂 |
| Probe card | 美国、日本、意大利、台湾、韩国、中国 | FormFactor、MJC、Technoprobe、MPI、TSE、CHPT、JEM、LEENO、ISC | MEMS/probe head、space transformer、fine pitch、高平行度 |
| Handler/socket/contactor | 美国、日本、台湾、韩国、中国 | Cohu、Advantest、Teradyne、WinWay、LEENO、ISC、Smiths、Yamaichi、Hon Precision | ULFF package、高 socket force、active thermal、液冷接口 |
| Inspection/metrology | 美国、以色列、日本、台湾 | KLA、Onto、Camtek、Cohu、Nova、Lasertec、Chroma | micro-pillar、warpage、6-sided AOI、hybrid bonding defect |
| OSAT/test houses | 台湾、韩国、中国、马来西亚、新加坡、美国 | TSMC、ASE/SPIL、Amkor、PTI、KYEC、JCET、Tongfu、Huatian、UTAC、ChipMOS | package test、final test、SLT、burn-in；最高端 CoWoS 仍由 TSMC 主导 |

### 4.2 供给瓶颈：至少 5 条

1. **HBM die 与 stack 良率：** 12Hi/16Hi stack 中任一 die 缺陷都会放大损失，KGD 测试越充分，前段 test time 越长。
2. **Memory tester module 供应：** HBM4 高速 pin、并行度和温控要求提高，tester channel 与 load board 配置上升；设备交期可能从 3-6 个月拉到 6-12 个月。
3. **Probe card 和 space transformer：** fine pitch、pad 数、planarity、清针/寿命、substrate 良率决定可用产能，且客户认证粘性强。
4. **Thermal handler / socket / contactor：** AI xPU package 面积大、功耗高，必须同时满足高 socket force、精准温控、低接触电阻和量产稳定性。
5. **HBM inspection/metrology：** micro-pillar 高度/共面性、warpage、void、underfill、hybrid bonding defect 都会导致后段报废。
6. **SLT/rack burn-in 场地、电力和冷却：** NVL72/UltraServer 级别测试消耗大量电力和冷却资源，测试 cell 本身像小型数据中心。
7. **Test program / DFT / yield engineer：** 高端 AI xPU 的测试方案要和设计、封装、系统、软件联合开发；人才比设备更难临时扩张。
8. **客户认证与 long-term allocation：** NVIDIA/AMD/Google/AWS/Microsoft/Meta/OpenAI/Broadcom 认证后不会频繁换平台，后进入者即使有设备也难抢份额。
9. **出口管制：** 中国客户需要国产替代，但先进 ATE、probe card 和高端 memory test 技术仍受限制，形成两套供应链和重复 CapEx。

### 4.3 成本构成与毛利决定因素

**高端 HBM 成品成本拆分，粗略估算：**

| 成本项 | 占比 | 说明 |
|---|---:|---|
| DRAM die wafer + yield | 30-45% | die 数、节点、良率、wafer allocation 决定 |
| TSV / thinning / stacking / bonding | 15-25% | 12Hi/16Hi、MR-MUF/TCB/HB 工艺差异大 |
| logic base die / foundry | 5-15% | HBM4 开始更重要，cHBM 会提高占比 |
| test / KGD / repair / burn-in | 8-15% | HBM4 test time 上升，极端情形可到 15%+ |
| substrate/interposer/CoWoS attach 相关 | 5-12% | 与 xPU 封装强绑定，口径会和 CoWoS 重叠 |
| depreciation / overhead / warranty | 10-20% | 良率、客户退货、长协定价影响 |

**ATE 系统成本拆分，粗略估算：**

| 成本项 | 占比 | 毛利影响 |
|---|---:|---|
| 高速仪表板卡、数字/模拟/RF/电源模块 | 35-45% | 模块复用和配置溢价决定毛利 |
| test head、load board、interface、calibration | 15-25% | 高速/高 pin count 价值量高 |
| handler/thermal/socket/automation | 10-20% | AI 高功率化使该项上升 |
| 软件、test program、diagnostics、service | 10-20% | 毛利最高，客户粘性最强 |
| 供应链、总装、质保 | 10-15% | 内存和精密零部件短缺会压毛利 |

**Probe card 成本拆分，粗略估算：**

| 成本项 | 占比 | 毛利影响 |
|---|---:|---|
| MEMS probe head / needle / contact structure | 25-40% | 寿命、接触稳定性决定定价 |
| space transformer / ceramic/organic substrate | 25-35% | fine pitch 与共面性是壁垒 |
| design / simulation / DFM | 10-20% | 客户定制、切换成本高 |
| assembly / planarity / QA / repair | 15-25% | 良率和交期决定利润 |

### 4.4 价格传导机制

1. **HBM 涨价直接传导到 GPU/ASIC module 价格。** 云厂为交期愿意签 LTA 和预付款，测试设备价格也因交期和配置升级上行。
2. **测试设备不是按芯片 ASP 定价，而按“避免良率损失和系统故障”的价值定价。** 一个 HBM stack 或 xPU package 报废的机会成本越高，测试插入点越多。
3. **probe card 与 socket 是耗材化设备。** 随 wafer starts、parallelism 和清针/磨损周期增长，收入比主机设备更平滑。
4. **软件/良率分析由工程时间节省和 ramp 速度定价。** 对 Rubin/MI400/TPU/ASIC 这种时间窗口敏感产品，少一个季度 ramp delay 的价值远高于软件 license。
5. **供不应求产品有溢价。** HBM4 memory ATE、HBM probe cards、active thermal handlers、SiPh/CPO test cell、rack-level test cell 都可在 2026-2027 出现高于常态的毛利。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 环节 | 市场集中度 | 龙头 | 结构判断 |
|---|---|---|---|
| HBM 成品 | 三寡头 | SK hynix、Samsung、Micron | 认证、良率、LTA 决定份额；2026 SK hynix 仍强，Samsung/Micron 用 HBM4 追赶 |
| Memory ATE | 双寡头为主 | Advantest、Teradyne | Advantest 公开口径 CY2025 memory tester share 约 61%；Teradyne HBM/DRAM 强劲追赶 |
| SoC ATE | 双寡头+区域厂商 | Advantest、Teradyne、Cohu、Chroma | Advantest 公开口径 CY2025 SoC tester share 约 66%；Teradyne 在 merchant GPU、SiPh、board test 发力 |
| Probe card | 多强但高端集中 | FormFactor、MJC、Technoprobe、MPI、TSE、CHPT、JEM | HBM/AI networking 高端比普通 probe card 更集中 |
| Handler/socket/contactors | 分散但高端紧缺 | Cohu、WinWay、LEENO、ISC、Smiths、Advantest、Teradyne | active thermal 和 ULFF package 会提高集中度 |
| Inspection/metrology | 高端集中 | KLA、Onto、Camtek、Cohu、Nova、Lasertec、Chroma | HBM micro-pillar/warpage/AI package 缺陷检测壁垒高 |
| Test software/analytics | 正在集中 | Teradyne TestInsight、Cohu Tignis、Advantest、PDF Solutions、proteanTecs | 与 ATE 和客户 flow 捆绑后切换成本高 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 具体表现 | 为什么能定价 |
|---|---|---|
| 技术壁垒 | HBM4 2048-bit、10-11Gbps+、12Hi/16Hi、低功耗、多温区、高并行 | 测试误差会导致良品误杀或坏品漏检，客户愿意为确定性付溢价 |
| 平台壁垒 | V93000、UltraFLEXplus、Magnum、T58xx、probe card/test program 生态 | test program、load board、DFT、OSAT flow 一旦建好，切换成本极高 |
| 认证壁垒 | NVIDIA/AMD/Google/AWS/Microsoft/Meta/OpenAI/Broadcom 认证周期长 | 量产爬坡期没有时间换平台，已认证供应商有交期和价格权 |
| 规模壁垒 | Advantest 规划 SoC tester 年产能从 5,000 台级别向 10,000 台推进 | 能同时供货和服务全球 OSAT/IDM 的公司少 |
| 可靠性壁垒 | AI package 和 HBM stack 失效成本高，rack 级返修代价极大 | 客户看 total cost of failure，不只看设备单价 |
| 耗材壁垒 | probe card、socket、contactor、load board 周期性更换 | 进入客户后形成 recurring revenue，抗周期更强 |
| 数据壁垒 | 良率数据库、failure signature、test program conversion | 数据越多越能缩短 ramp，软件/IP 可高毛利收费 |
| 供应链壁垒 | 精密零部件、memory components、陶瓷/有机 substrate、高速连接器 | 短缺时交付能力本身就是产品价值 |

### 5.3 长期高 ROIC/高毛利环节

1. **Test software / SLM / DFT / yield analytics：** 轻资产、毛利 75-95%，随 AI xPU 复杂度提高而增值。
2. **高端 ATE 平台和模块：** 设备毛利 55-70%，客户锁定强，服务和模块升级提高生命周期价值。
3. **HBM probe card / space transformer：** 既有技术壁垒又有耗材属性，HBM4/16Hi 提高 ASP 和替换频率。
4. **HBM 成品：** 2026-2027 供需最紧，毛利可达 60-80%+；但资本开支和周期风险高于软件/设备。
5. **active thermal handler/socket/SLT：** 受益于 high-power AI package，弹性强，但竞争比 ATE 更分散。
6. **OSAT 测试服务：** 收入弹性大，但折旧、客户集中和价格谈判使长期 ROIC 通常低于设备/IP。

## 6. 2026 关键变化：最可能发生的 3 个拐点

### 拐点一：HBM3E 12Hi 从 GPU 供应链变成全 AI xPU 供应链

B300/GB300、MI350、TPU Ironwood、Trainium2/3、Maia200、MTIA 等都在消耗 HBM3E 或同等级高带宽内存。2026 的现实主线不是 HBM4 全面替代，而是 **HBM3E 12Hi 长时间缺货 + HBM4 抢最高端新增**。

最可能放量子方向：HBM3E、memory ATE、DRAM probe card、HBM KGD、CoWoS package test、DDR5/MRDIMM。

### 拐点二：测试设备从“配套 CapEx”变成“AI xPU 出货阀门”

Advantest、Teradyne、FormFactor、Cohu 的 Q1/FY2025-FY2026 材料已经同时验证：AI compute、HBM/DRAM、networking probe、HPC package test 都在加速。测试不再只是后周期设备，而是决定 AI rack 可交付性的前置资源。

最可能放量子方向：SoC ATE、memory ATE、HBM probe card、active thermal handler/socket、SLT、test software。

### 拐点三：系统级测试开始吞并更多价值

NVL72、Trainium UltraServer、TPU pod、Maia closed-loop liquid cooling、MTIA OCP rack 让故障成本从芯片级变成 rack 级。Teradyne Omnyx、MultiLane Test Products、TestInsight 说明测试设备公司正在沿着 **wafer to AI data center** 扩张。

最可能放量子方向：board/tray/rack test、high-speed interconnect test、SiPh/CPO test、AI data center operations test。

## 7. 2027 关键变化：最可能发生的 3 个拐点

### 拐点一：HBM4/HBM4E 成为高端新增 xPU 默认选项

Rubin、Rubin Ultra、MI400/MI455X、TPU8、Trainium4、OpenAI/Broadcom、Meta/Broadcom 后续 XPU 将把 HBM4/4E 推向主力。2027 年 HBM4 不是“新产品”，而是最高端 AI compute 的 **allocation currency**。

最可能放量子方向：HBM4 memory tester、16Hi probe card、custom base die test、hybrid bonding inspection、wafer-level burn-in。

### 拐点二：custom ASIC 带来第二条测试设备需求曲线

2026 仍由 NVIDIA Blackwell/Blackwell Ultra 主导高价值出货；2027 若 OpenAI/Meta/Anthropic/Google/AWS 的 ASIC 订单按公告节奏推进，测试设备需求会从 GPU 单主线扩散到多客户 ASIC。测试平台将同时服务 NVIDIA、AMD、Broadcom、Marvell、云厂自研 ASIC 和中国国产 AI 芯片。

最可能放量子方向：AI ASIC SoC ATE、DFT/SLM、Ethernet/SerDes test、UCIe/chiplet test、OSAT test capacity。

### 拐点三：CPO/SiPh 与 rack-level test 从期权变成真实订单

Advantest 已披露 silicon photonics high-volume ATE order，Teradyne 推 Photon 100 并估 SiPh/CPO test midterm TAM 可达 $300-700M/年。2027 年若 1.6T/3.2T、CPO switch 和 rack-scale optical interconnect 提前，光电测试会成为测试设备行业的新 beta。

最可能放量子方向：SiPh/CPO ATE、optical probe、co-packaged optics SLT、high-speed I/O test、board/rack digital twin。

## 8. 头部公司与细分领域全景清单

### 8.1 HBM / 高带宽内存

| 细分 | 公司 | 优势 |
|---|---|---|
| HBM3E/HBM4 | SK hynix | HBM3E 领先、MR-MUF、NVIDIA 客户份额、Cheongju/M15X/P&T7 后道 |
| HBM3E/HBM4/HBM4E/cHBM | Samsung Electronics | memory + foundry + packaging 一体化，4nm logic base die，HBM4/HBM4E/cHBM 路线 |
| HBM3E/HBM4/SOCAMM/SSD | Micron | 美国供应链、HBM4 36GB 12H volume shipment、16H samples、SOCAMM2/Gen6 SSD |
| 中国替代 | CXMT、Huawei 生态、长江存储/国内封测链 | 国产 AI 芯片需求驱动，但高端 HBM 与先进封装仍爬坡 |
| AI DDR5/MRDIMM/SOCAMM | Samsung、SK hynix、Micron、Montage、Rambus | AI CPU/推理内存层级扩散 |
| NAND/SSD/HBF 潜在 | Samsung、SK hynix/Solidigm、Micron、Kioxia、Western Digital/SanDisk、YMTC、Phison、Marvell、Silicon Motion | AI data lake、KV cache、企业 SSD 与未来 high bandwidth flash |

### 8.2 Memory ATE / SoC ATE

| 细分 | 公司 | 优势/状态 |
|---|---|---|
| SoC ATE 龙头 | Advantest | V93000 生态，FY2025 SoC tester share 约 66%，AI accelerator 客户份额强 |
| Memory ATE 龙头 | Advantest | T58xx/T5801 等 memory test，FY2025 memory tester share 约 61%，HBM/高性能 DRAM 受益 |
| SoC/Memory ATE 龙头 | Teradyne | Q1 2026 Semi Test $1.111B；memory revenue $203M；Magnum 7、UltraFLEXplus、merchant GPU orders |
| HPC package/test cell | Cohu | Eclipse active thermal、Diamondx、handler/contactor/inspection 一体，FY2026 HPC outlook $80-100M |
| 台湾 ATE | Chroma ATE | 3680 SoC test、AI chip/power/photonics/semiconductor test；Q1 2026 testing equipment business 大幅增长 |
| 中国 ATE | 长川科技、华峰测控、精测电子、联动科技等 | 国产替代、模拟/SoC/功率/存储测试逐步扩张 |
| 其他 ATE | SPEA、TESEC、Accretech、Keysight、NI/Emerson | 特定模拟、功率、board/system、HDD/SSD/通信测试优势 |

### 8.3 Probe card / prober / interface

| 细分 | 公司 | 优势 |
|---|---|---|
| 高端 probe card | FormFactor | DRAM/HBM、Foundry & Logic、AI networking；Q1 2026 record revenue |
| Memory probe card | Micronics Japan | memory/HBM probe card 强，受 HBM4 换代拉动 |
| Advanced probe card | Technoprobe | SoC/advanced probe、收购/扩张，规划进入 HBM testing |
| 台湾 probe card | MPI、CHPT、WinWay、Gudeng 相关生态 | HBM/SoC/advanced package interface、TSMC/OSAT proximity |
| 韩国 probe/socket | TSE、LEENO、ISC、Korea Instrument | memory/logic test interface、本土 HBM 客户 proximity |
| 日本 probe card | Japan Electronic Materials、MJC、Nidec/相关材料 | memory probe card、fine pitch |
| Prober | Tokyo Electron、Accretech/Tokyo Seimitsu、FormFactor Cascade、MPI、Tokyo Electron Device | wafer probe、temperature probing、advanced package probing |

### 8.4 Handler、socket、burn-in、SLT

| 细分 | 公司 |
|---|---|
| Handler / thermal test | Cohu、Advantest、Teradyne、Epson、TESEC、Hon Precision、Chroma |
| Socket / contactor | WinWay、ISC、LEENO、Smiths Interconnect、Yamaichi、Cohu、FormFactor、Ironwood Electronics |
| Burn-in / reliability | Aehr Test Systems、Advantest、Teradyne、Cohu、Chroma、ESPEC、in-house IDM/OSAT |
| SLT / board / rack test | Teradyne Omnyx/IST/MultiLane、Keysight、NI/Emerson、Chroma、Cohu、Celestica/Jabil/Flex/ODM internal |
| HDD/SSD/storage test | Teradyne、Advantest、Chroma、Keysight、Cohu、Phison/Marvell/Silicon Motion ecosystem |

### 8.5 Inspection/metrology、软件/IP

| 细分 | 公司 |
|---|---|
| HBM/advanced package inspection | KLA、Onto Innovation、Camtek、Cohu Neon、Nova、Lasertec、Chroma、Applied Materials |
| Bonding/metrology tools | Besi、ASMPT、EV Group、SUSS MicroTec、Tokyo Electron、Applied Materials、K&S |
| DFT/SLM/IP | Synopsys、Cadence、Siemens EDA、Ansys、Rambus、PDF Solutions、proteanTecs、Arteris |
| Test development/analytics | Teradyne TestInsight、Cohu Tignis、Advantest、PDF Solutions、NI/Emerson、Optimal+ 相关资产 |
| HBM controller/PHY | Rambus、Synopsys、Cadence、Siemens EDA、Marvell、Broadcom、Alphawave |

### 8.6 OSAT / IDM / 客户生态

| 细分 | 公司 |
|---|---|
| Foundry/advanced packaging | TSMC、Samsung Foundry/AVP、Intel Foundry、ASE、Amkor、JCET、Tongfu、Huatian |
| Memory IDM test | SK hynix、Samsung、Micron、CXMT |
| OSAT test houses | ASE/SPIL、Amkor、PTI、KYEC、Hana Micron、UTAC、ChipMOS、JCET、Tongfu、Huatian、Nepes |
| AI xPU 客户 | NVIDIA、AMD、Google/Broadcom、AWS/Annapurna、Microsoft、Meta/Broadcom、OpenAI/Broadcom、Huawei、Cambricon、Alibaba T-Head、Baidu Kunlun、Broadcom/Marvell custom ASIC customers |

## 9. 投资观察框架

### 9.1 2026 最确定方向

| 排名 | 方向 | 理由 | 跟踪指标 |
|---:|---|---|---|
| 1 | HBM3E/HBM4 已认证份额 | AI xPU 共同瓶颈，价格弹性最大 | SK hynix/Samsung/Micron HBM4 qualification、ASP、bit allocation |
| 2 | Advantest/Teradyne 高端 ATE | SoC + memory tester 同时受益，客户锁定强 | CY2026 SoC/memory TAM、订单、lead time、gross margin |
| 3 | HBM probe card | 耗材属性 + HBM4 换代 + 客户认证 | FormFactor/MJC/Technoprobe/MPI revenue、HBM mix、交期 |
| 4 | Active thermal socket/handler | AI package 功耗和面积上升 | Cohu Eclipse/WinWay/ISC/LEENO 订单、ULFF package design-in |
| 5 | SLT/rack test | rack-scale AI 交付要求更高可靠性 | Teradyne Omnyx/IST、ODM rack burn-in capacity、故障率 |

### 9.2 2027 弹性最大方向

| 排名 | 方向 | 逻辑 |
|---:|---|---|
| 1 | HBM4E/16Hi/cHBM | 平台换代、单 stack 价值上升、客户定制化提高溢价 |
| 2 | HBM4 memory ATE + probe card | HBM4/4E test time 和 pin count 提升，设备需求可能非线性增长 |
| 3 | AI ASIC test flow | Broadcom/Marvell/云厂 ASIC 把测试需求从 NVIDIA 单主线扩散 |
| 4 | SiPh/CPO test | 1.6T/3.2T/CPO switch 进入量产后 TAM 快速打开 |
| 5 | Test software/SLM/analytics | 轻资产高毛利，复杂 AI package 的“保险层” |

## 10. 主要来源与交叉验证

### 一手公司材料

| 来源 | 本报告使用的信息 |
|---|---|
| [Advantest FY2025 financial briefing slides](https://www.advantest.com/document/en/investors/ir-library/result/JE_BIZ_260427_slide.pdf) | FY2025/FY2026 指引、CY2026 SoC tester TAM $8.7-9.5B、memory tester TAM $2.2-2.7B、SoC/memory tester share、产能扩张 |
| [Advantest FY2025 Q&A](https://www.advantest.com/document/en/investors/ir-library/result/JE_BIZ_260427_QA.pdf) | V93000 de facto standard、inferencing/CPU demand、SiPh ATE 量产订单、SoC tester capacity、margin 与 memory components supply |
| [Teradyne Q1 2026 results](https://investors.teradyne.com/news-events/press-releases/detail/440/teradyne-reports-first-quarter-2026-results) | Q1 revenue $1.282B、Semi Test $1.111B、约 70% revenue tied to AI、Q2 guidance |
| [Teradyne Q1 2026 10-Q](https://investors.teradyne.com/sec-filings/all-sec-filings/content/0001193125-26-201058/ter-20260329.htm) | Semi Test 超过 $1B、HBM/DRAM memory test 近纪录、MLTP/TestInsight acquisition、区域收入 |
| [Teradyne Q1 2026 transcript](https://www.fool.com/earnings/call-transcripts/2026/04/29/teradyne-ter-q1-2026-earnings-transcript/) | memory revenue $203M、SoC $882M、Magnum 7、merchant GPU orders、Photon 100、Omnyx、SiPh/CPO TAM $300-700M |
| [FormFactor Q1 2026 results](https://investors.formfactor.com/news-releases/news-release-details/formfactor-inc-reports-2026-first-quarter-results) | Q1 revenue $226.1M、record DRAM revenue、HBM demand、Foundry & Logic networking probe card、non-GAAP GM 49.0%、Q2 outlook |
| [Cohu Q1 2026 results](https://ir.cohu.com/news-releases/news-release-details/cohu-reports-first-quarter-2026-results) | Q1 sales $125.1M、non-GAAP GM 46.5%、AI-driven compute TAM ~$750M、FY2026 HPC revenue outlook ~$80-100M |
| [Cohu press releases page](https://ir.cohu.com/news-events/press-releases) | 2026 年 4 月 $30M HPC test follow-on orders、Eclipse AI/HPC test 订单节奏 |
| [Cohu Eclipse AI datacenter processor order](https://ir.cohu.com/news-releases/news-release-details/cohu-receives-second-multi-unit-order-testing-next-generation-ai) | Eclipse multi-unit order、ULFF package、active thermal/high socket force、HPC segment $65-80M internal projection |
| [Cohu Neon HBM inspection orders](https://ir.cohu.com/news-releases/news-release-details/cohu-secures-additional-neon-orders-raises-2025-forecasted-hbm) | HBM inspection/metrology、6-sided AOI、micro-pillar metrology、2025 HBM revenue $10-11M、opportunity >$100M |
| [Chroma 2026 Q1 presentation mirror](https://www.marketscreener.com/news/chroma-ate-2026-04-30-quarterly-results-presentation-ce7f58dbda8ef62d) | Q1 2026 sales NTD11.859B、testing equipment business +79% YoY、semiconductor/photonics segment NTD3.410B |
| [Chroma 3680 product page](https://www.chroma.com.tw/en/product/advanced_SoC_analog_test_system_3680_36) | SoC tester 3680 技术规格、2048 pins、1Gbps、high-parallel test |
| [Chroma AI chip test SEMICON Taiwan 2025](https://www.chromaate.com/en/newsroom/news1039) | AI-driven Chroma 3680 semiconductor test positioning |
| [Chroma AI-era test/validation note](https://www.chromaate.com/en/newsroom/news1129) | AI infrastructure 四大测试能力：compute/data、cooling/thermal、high-speed communications、power/energy |

### HBM、AI 芯片与行业报告材料

| 来源 | 本报告使用的信息 |
|---|---|
| [Samsung HBM4 press release](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing) | HBM4 商用出货、1c DRAM、4nm base die、HBM4E/cHBM 路线 |
| [Micron HBM4 for NVIDIA Vera Rubin](https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin) | 36GB 12H HBM4 volume shipment、16H samples、SOCAMM2/Gen6 SSD |
| [SK hynix HBM4 development](https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/) | HBM4 开发完成、2048 I/O、功耗效率、MR-MUF |
| [SK hynix 2026 HBM supercycle outlook](https://news.skhynix.com/2026-market-outlook-focus-on-the-hbm-led-memory-supercycle/) | BofA 2026 HBM market $54.6B、HBM3E 约占 2026 出货三分之二 |
| [TrendForce HBM4 validation 2026Q2](https://www.trendforce.com/presscenter/news/20260213-12929.html) | 三大 HBM 厂商进入 NVIDIA HBM4 供应链的验证节奏 |
| [TrendForce memory wall](https://www.trendforce.com/insights/memory-wall) | 2026 HBM consumption +70% 以上、memory wall、DDR5/HBM 供需扩散 |
| [Gartner 2026 semiconductor forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | 2026 半导体与 memory revenue、AI infra spending、DRAM price |
| [NVIDIA Vera Rubin GTC 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | Rubin/Vera/BlueField/Spectrum/CPO/DSX 与 2026H2 可用 |
| [NVIDIA Vera Rubin technical blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | NVL72、LPX、SPX、CPO、rack energy/cooling |
| [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) | GB300/Blackwell Ultra、HBM3E、rack-scale 形态 |
| [AMD/Samsung HBM4 collaboration](https://www.amd.com/en/newsroom/press-releases/2026-3-18-samsung-and-amd-expand-strategic-collaboratio.html) | AMD MI455X/HBM4 合作 |
| [OpenAI/Broadcom 10GW collaboration](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/) | OpenAI custom accelerator 10GW、2026H2 开始部署 |
| [Meta/Broadcom custom AI silicon](https://about.fb.com/news/2026/04/meta-partners-with-broadcom-to-co-develop-custom-ai-silicon/) | Meta/Broadcom XPU、>1GW、多 GW 路线 |

### 项目内底稿

| 本地文件 | 用途 |
|---|---|
| `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md` | 2026-2027 出货量最大 AI 芯片路线、B300/GB300、TPU、Trainium、MI350、Maia、MTIA、Rubin/MI400 |
| `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_HBM与高带宽内存_2026.md` | HBM 市场规模、HBM3E/HBM4/HBM4E/cHBM、SOCAMM2、DDR5、HBM 供应链和毛利假设 |
| `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_AI芯片先进封装_2026.md` | CoWoS/SoIC/EMIB、HBM KGD、ATE、probe card、burn-in、先进封装测试与设备材料 |
| `D:\drive\Investment\调研\v5\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md` | AI 数据中心 CapEx、HBM/DRAM/SRAM、GPU/ASIC、先进封装、液冷/供电的三情景约束 |

---

**最终判断：** HBM 与存储测试设备是 2026-2027 AI 基础设施建设中少数“需求扩张、单价提升、客户切换困难、供给扩张慢”同时成立的环节。2026 年看 HBM3E 现金流、HBM4 验证、ATE/probe card 订单、active thermal test 导入；2027 年看 HBM4E/16Hi/cHBM、AI ASIC test flow、SiPh/CPO test 和 rack-level SLT。若 AI 数据中心建设按极度乐观路径推进，测试设备并不会只是 HBM 的影子行业，而会成为和 HBM 本体并列的算力交付瓶颈。
# 行业调研：【半导体高纯水、气体与化学流体系统】

> 截至日期：2026-05-08  
> 研究口径：本报告把“半导体高纯水、气体与化学流体系统”定义为晶圆厂、存储厂、先进封装厂和配套材料厂中的 UPW 超纯水系统、水回收/废水系统、UHP 大宗气体与特气供应系统、气柜/VMB/阀组/MFC/净化器/尾气处理、Bulk Chemical Delivery System、化学品混配/输送、CMP slurry/光刻胶/湿化学品供应、PFA/PVDF/EP 管阀件、在线分析与运维服务。  
> 预测原则：对 2026-2027 AI 基础设施建设采用明显乐观假设。凡缺少直接公开数据的细分项，使用“AI 芯片出货、先进逻辑/HBM/先进封装产能、300mm fab 建设、公司订单与长期供气/供水合同”做大胆推演，并明确为估算。B/O/X = 基准/乐观/极度超预期乐观。

## 0. 一页结论

这个行业不是“AI 数据中心里的水冷系统”，而是 AI 算力扩张传导到晶圆制造端之后的“厂务与工艺流体闸门”。2026 年 AI 数据中心 capex 爆发，先推高 NVIDIA Blackwell/GB300、Google TPU、AWS Trainium、Meta/Microsoft/OpenAI/Broadcom ASIC、AMD MI350/MI400、HBM3E/HBM4 和 CoWoS/先进封装需求；这些产能要落地，必须同步建设 UPW、UHP 气体、湿化学品与化学流体系统。

核心判断：

| 判断 | 结论 |
|---|---|
| 2026 最大机会 | 先进逻辑、HBM/DRAM、先进封装新线和扩线带来一次性 EPC/系统订单；气体、湿化学品、过滤器、净化器、管阀件、运维服务随后进入多年经常性收入。 |
| 2026 最可能技术路径 | 成熟高可靠路线放量：18.2 MΩ·cm UPW + >80% 水回收、现场 UHP N2/O2/Ar/H2 大宗气体长协、全自动特气/化学品输送、点位过滤/净化、F-GHG/NF3 尾气治理、先进封装湿法清洗和 CMP/slurry 供应。 |
| 2027 新增弹性 | Rubin/MI400/TPU8/OpenAI ASIC/HBM4 放量后，DRAM/HBM 和封装湿法步骤增加，UPW 与湿化学品单位强度上升；美国、日本、欧洲 CHIPS fab 进入厂务调试与 ramp，服务收入可见度提升。 |
| 最强定价权 | 现场供气长协、先进 UPW 回收/运维、超低金属/超低颗粒过滤与净化、气体/化学品安全交付系统、PFAS/F-GHG 合规方案。能直接影响良率、停线和安全许可的环节最能定价。 |
| 最大挑战 | 交付瓶颈不是单一设备，而是工程设计、洁净材料、阀件/MFC、树脂/膜、特气产能、危化品许可、客户认证、现场施工人才、废水/排放法规的复合瓶颈。 |
| 2026 核心收入池估算 | 核心系统与服务约 $13-18B；若把电子气体、高纯湿化学品和相关耗材纳入，经常性材料收入池约 $28-42B；极度乐观情形下 2027 年相关订单和收入池可上探 $55-75B。 |

## 1. 最近半年关键事实与一手信号

| 时间 | 来源 | 关键事实 | 对本行业含义 |
|---|---|---|---|
| 2025-10 | SEMI 300mm Fab Outlook | 2026-2028 年全球 300mm fab 设备支出预计合计 $374B；2025 年 300mm 设备支出首次超过 $100B。 | 新建/扩建 fab 不只买 WFE，也要提前 12-30 个月锁 UPW、气体、化学品输送与废水系统。 |
| 2025-12 | Ecolab/Ovivo | Ecolab 以约 $1.8B 收购 Ovivo Electronics；Ovivo Electronics 2025 年预计销售约 $500M，员工 900+。 | 头部水处理公司用高倍数买半导体 UPW 资产，验证 UPW 从传统水务变为 AI 半导体链条资产。 |
| 2026-02 | Nomura Micro Science 3Q FY2026 | 半导体 UPW 装置需求带动 3Q 累计销售 410.46 亿日元、同比 +28.9%；受注高 274.9 亿日元、同比 +55.9%；营业利润 46.40 亿日元、同比 +18.0%。 | UPW 系统订单已随生成式 AI、云基础设施和美国大型项目显著前置。 |
| 2026-03 | SIA Senate EPW testimony | SIA 强调 fab 使用高度受控、封闭、自动化的化学品输送系统，以降低人员暴露和环境释放。 | 危化品/特气系统不是低端管道，EHS、自动化和法规合规是壁垒。 |
| 2026-04 | Gartner | 2026 全球半导体收入预计超过 $1.3T，AI 半导体约占 2026 总量 30%，hyperscaler AI 基建支出 2026 年增长超过 50%。 | AI 芯片需求足够大，可把先进逻辑、HBM、封装和材料系统的订单同时推高。 |
| 2026-04 | Air Liquide | 在日本广岛投资 2 亿欧元，为下一代 AI 芯片生产建设、拥有并运营两套工业气体生产装置，绑定长期协议。 | 头部气体商把“AI chips”写入供气投资逻辑，UHP 气体转为客户扩产的同步资本项目。 |
| 2026-04 | Air Liquide Q1 activity | Q1 材料披露日本项目为先进 AI 芯片提供 UHP N2/O2/Ar；集团在亚洲有大量 dedicated units。 | 大宗气体现场装置和区域网络是供给瓶颈，也是长协护城河。 |
| 2025-04 到 2026 | Linde/Samsung | Linde 宣布扩大向三星平泽半导体园区供应 UHP atmospheric、process、specialty gases，预计 2026 年中开始供应。 | 韩国 HBM/先进存储扩产直接拉动 onsite gas 和特气交付。 |
| 2026-04 | Entegris 1Q26 | Advanced Purity Solutions 仍是增长核心；管理层强调 AI 相关需求、先进逻辑/存储 content per wafer、液体过滤持续强。 | 先进节点对液体过滤、FOUP、CMP、选择性刻蚀和微污染控制的价值量上升。 |
| 2026-04/05 | UCT / Ichor / MKS | UCT 称处于多年 AI 驱动扩张早期；Ichor 是半导体关键流体输送子系统供应商；MKS Q1 受 AI 相关半导体制造和先进封装需求拉动。 | WFE 子系统和厂务流体系统订单同步回暖，gas/liquid delivery、remote plasma、dissolved gas、flow control 变成 AI 间接受益环节。 |
| 2026-04 | CMC Conference | TECHCET/CMC 会议主题是“Critical Materials at the Crossroads”，覆盖湿法刻蚀、过滤、化学品、材料供应链、AI-enabled materials discovery。 | 半导体材料供应链的瓶颈已经从“买得到化学品”升级为“供应链、纯度、替代材料和合规一起优化”。 |
| 2026-05 | TrendForce/PRNewswire | 北美 AI 数据中心扩张推动全球 Top 9 CSP 2026 capex 上修至约 $830B。 | 这是晶圆端的需求β。即使只有一小部分转化为当年 wafer/HBM/packaging 扩产，也足以让厂务流体系统维持紧张。 |

## 2. AI 芯片技术路径如何传导到 UPW、气体与化学流体

项目内已有 AI 芯片路线图显示，2026-2027 出货/价值权重最高的平台大致是 GB300/B300、AWS Trainium2、Google TPU Ironwood、GB200/B200、Huawei Ascend、Cambricon MLU、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia，以及 2026H2 后的 Rubin/MI400/OpenAI-Broadcom ASIC。对本行业的直接含义如下：

| AI 芯片/平台 | 制造路径 | 对 UPW 的拉动 | 对气体的拉动 | 对化学流体系统的拉动 |
|---|---|---|---|---|
| NVIDIA GB300/B300、GB200/B200 | TSMC N4/N3 类逻辑 + HBM3E + CoWoS-L/S | 先进逻辑和 CoWoS 扩产使用大量湿法清洗、CMP、显影/剥离；新厂 UPW 主系统和回收系统同步扩容。 | N2/O2/Ar/H2 大宗气体、CVD/etch/clean 特气、NF3/F2/fluorocarbon 清腔需求增加。 | HBM3E、CoWoS、ABF/封装湿法需要 slurry、Cu plating、清洗化学品和超低颗粒过滤。 |
| Google TPU Ironwood / TPU8、AWS Trainium2/3、Meta MTIA、Microsoft Maia | Broadcom/Annapurna/Microsoft 自研 ASIC + HBM + 2.5D | 把需求从 NVIDIA 单线外溢到 CSP 自研 ASIC，增加 TSMC/三星/Intel/OSAT 多点厂务订单。 | 长协 onsite gas 更重要，因为客户不希望自研 ASIC ramp 被 N2/Ar/H2/特气供应卡住。 | 定制 ASIC 的化学品规格、过滤等级和交付路径更早绑定设计与工艺，客户锁定更强。 |
| AMD MI350/MI400、Rubin | HBM3E 转 HBM4，2027 放量 | HBM4/DRAM 层数、TSV、bonding、advanced package 提高 UPW 与湿法清洗强度。 | DRAM/HBM 扩产提高 WF6、NH3、SiH4/DCS、NF3、N2O、H2、Ar 等需求。 | HBM4 带动 TSV/CMP/plating/cleaning、hybrid bonding 化学品和点位过滤升级。 |
| Huawei Ascend / Cambricon / 国产 AI | SMIC 可得先进节点 + 国产封装 + 本土材料替代 | 中国本土 UPW、废水、回收系统和国产化运维需求提高。 | 国产特气、电子大宗气体、尾气治理和气柜阀组国产替代空间放大。 | 国产湿电子化学品、PFA/PVDF 管阀件、化学品混配/CDS 认证需求提高。 |

### 2.1 2026 最可能的技术路径

1. UPW 主系统：RO + EDI/IX + UV TOC + 膜脱气 + UF + polishing mixed bed，维持 18.2 MΩ·cm、TOC 1 ppb 级、金属 ppt 级和超低颗粒。Organo 的半导体资料给出前沿 fab 可做到“1 ppt 或更低”杂质浓度，并强调 1000 ton/hour 级水量和 >80% 回收率。
2. 水回收与闭环：先进 fab 因用水许可和 ESG，把 UPW 回收、酸碱/含氟/含铜/含氨废水分流、浓水回用、valuable resource recovery 从可选变为标配。Kurita 指出 300mm fab 用水可达每分钟 2000 加仑级，单靠市政供水不现实。
3. 大宗气体 onsite：N2/O2/Ar/H2 由 Air Liquide、Linde、Air Products、Nippon Sanso 等建设现场装置和管网，长协、take-or-pay、客户厂区绑定。
4. 特气与气体输送：SiH4、DCS、NH3、HCl、Cl2、BCl3、NF3、WF6、N2O、CO2、PH3/AsH3、fluorocarbon、rare gases 使用全自动 gas cabinet、VMB/VMP、MFC、purifier、leak detection、scrubber。
5. 化学流体：H2SO4/H2O2/NH4OH/HF/HCl/HNO3/IPA/TMAH/NMP、EUV/ArF 光刻胶与 ancillary chemicals、CMP slurry、Cu plating、stripper/developer 需要 BCDS/CDS、混配、温控、过滤、在线浓度与颗粒监测。

### 2.2 技术成熟与放量时间表

| 技术方向 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观/极度超预期 |
|---|---|---|---|---|---|
| UPW 主系统与分配 loop | 成熟满载，随新 fab EPC 放量 | 美国/日本/韩国项目提前采购 | 客户为抢工期预付长交期泵、膜、树脂、管阀件 | CHIPS 项目进入调试，O&M 收入爬坡 | UPW 从 EPC 转为长期水管理服务，服务毛利上行。 |
| 水回收、ZLD、含氟/含铜/含氨分流 | >80% 回收成为前沿 fab 常态 | 用水紧张地区把回收率和废水回用作为开工条件 | 数据中心和 fab 同区竞争水资源，回收系统订单提前 | PFAS/含氟废水治理进入更多量产 fab | PFAS 捕集/破坏和资源回收形成高毛利服务。 |
| onsite UHP bulk gas | 头部气体商 2026-2027 项目密集启动 | 长协覆盖更多亚太/美国新厂 | AI/HBM 客户愿意用更高固定费锁产能 | 新厂 ramp 后气体销量和服务费上台阶 | 大宗气体现场装置成为半导体园区基础设施，合同期 10-20 年。 |
| 自动特气/气柜/VMB/MFC | 成熟技术，但交付受 MFC、阀件、认证限制 | 高危特气自动化和冗余配置提升单 fab 价值 | 工程商一次性锁定多厂区标准平台 | HBM4/2nm/High-NA 节点增加特气种类和流量精度 | AI-driven fab digital twin 接入气体系统，升级收入增加。 |
| 高纯化学品 BCDS/CDS | 成熟放量，先进封装和 HBM 拉动 | slurry/photochem/湿法清洗系统提前采购 | 先进封装厂把湿法化学系统做成独立瓶颈投资 | hybrid bonding、TSV、RDL、CMP 增加系统价值量 | 按化学品配方和客户 fab 绑定，切换成本继续升高。 |
| 点位过滤/净化/在线分析 | 液体过滤、气体净化、TOC/金属/颗粒监测放量 | sub-2nm 颗粒和 ppt 金属控制成为先进节点标配 | 良率压力让客户多点冗余安装 | HBM4、2nm、EUV/High-NA 继续提高过滤等级 | 单 wafer content 上升，耗材和滤芯经常性收入高弹性。 |
| F-GHG/NF3/N2O abatement | 已成熟，法规和客户碳目标推动 | SEMI/SCC 推动低排放气体和 abatement 标准化 | 客户把 abatement 作为 fab 开工和融资必要条件 | 低-GWP 替代气体局部导入 | 替代气体 + scrubber + 监测形成高壁垒组合销售。 |
| PFAS-free/低 PFAS 材料与废水破坏 | 2026 多为评估/试点 | 特定清洗/蚀刻/容器材料开始替代 | 法规压力导致头部客户提前 qualification | 2027 进入小批量/局部工艺 | 真正大规模放量更可能在 2028-2030，但 2027 design-in 价值高。 |

## 3. 已经开始放量的关键产品：规模、渗透率与利润率

口径说明：未来 3 个月为 2026Q2-Q3 订单/收入年化片段；未来 1 年为 2026-05 至 2027-05；未来 2 年为 2026-05 至 2028-05。市场规模是全球收入/订单池估算，包含系统、关键部件、服务和相关耗材，避免与整套 fab capex 简单相加。

| 已放量产品 | 2026 事实基础 | 未来 3 个月规模 B/O/X | 未来 1 年规模 B/O/X | 未来 2 年规模 B/O/X | 渗透率路径 | 利润率假设 B/O/X |
|---|---|---:|---:|---:|---|---|
| UPW 主系统 EPC、distribution loop、polishing | 2026 专用半导体 UPW 系统外部报告约 $1.8-2.3B；Ecolab/Ovivo 2025 销售约 $500M | $0.6-0.8B / $0.8-1.1B / $1.1-1.6B | $2.6-3.4B / $3.4-4.7B / $4.7-6.5B | $5.7-7.5B / $7.5-11B / $11-16B | 前沿逻辑/HBM 新厂 attach rate 近 100%；老厂升级 20-35% | EPC 毛利 18-30% / 25-35% / 32-42%；运维服务更高。 |
| UPW 回收、废水分流、资源回收、ZLD | 前沿 fab >80% 回收率成为常态；用水许可驱动 | $0.4-0.7B / $0.7-1.0B / $1.0-1.5B | $2.0-3.2B / $3.2-5.0B / $5.0-7.5B | $4.8-7.5B / $7.5-12B / $12-19B | 先进厂 2026 50-70%，2027 65-85%；水紧地区接近必选 | 系统 22-35% / 30-42% / 40-50%；PFAS/资源回收服务可更高。 |
| onsite UHP bulk gas 供应和现场装置 | Air Liquide 日本 €200M、VSMC 新装置 2026、Linde Samsung 2026 中启动 | $1.7-2.3B / $2.3-3.2B / $3.2-4.5B | $8-10B / $10-13B / $13-17B | $17-23B / $23-32B / $32-45B | 先进 300mm fab onsite/pipeline 近 100%；先进封装和材料厂渗透率提升 | 气体毛利 35-55%，EBIT 18-32%；长协 ROIC 稳定。 |
| 电子特气、rare gases、前驱体供气 | TechInsights/TECHCET 口径 2026 电子气体约 $6.8-6.9B；特气 2026 增速高于 bulk | $1.5-2.0B / $2.0-2.7B / $2.7-3.6B | $7-9B / $9-12B / $12-16B | $15-20B / $20-28B / $28-40B | 先进节点和 HBM 工艺步骤增加；rare gas recovery 从少数厂扩散 | 大宗 30-45%；特气/稀有气 45-65%；短缺时溢价显著。 |
| gas cabinet、VMB/VMP、MFC、purifier、leak detection | 2026 半导体 gas delivery system 外部口径约 $1.64B | $0.35-0.50B / $0.50-0.75B / $0.75-1.05B | $1.7-2.2B / $2.2-3.0B / $3.0-4.2B | $3.8-5.2B / $5.2-7.5B / $7.5-11B | 新工具和新厂 attach rate 近 100%；智能监测升级 25-40% | 25-40% / 35-50% / 45-60%；MFC/净化器/高危气柜最高。 |
| 高纯化学品 BCDS/CDS、混配与分配 | 2026 high-purity CDS 约 $1.48B，BCDS 约 $1.0-1.25B | $0.45-0.65B / $0.65-0.90B / $0.90-1.25B | $2.1-2.8B / $2.8-3.9B / $3.9-5.6B | $4.5-6.2B / $6.2-9.0B / $9.0-13B | 先进湿法/光刻/CMP/封装线 attach rate 90%+；自动化升级 30-50% | 24-36% / 32-45% / 42-55%；客户认证后价格粘性强。 |
| 高纯湿电子化学品、酸碱溶剂、specialty cleans | 2026 高纯湿化学品口径约 $7.8B；半导体化学品更宽口径约 $17.5B | $1.7-2.3B / $2.3-3.1B / $3.1-4.2B | $7.8-10.5B / $10.5-14.5B / $14.5-21B | $17-24B / $24-34B / $34-50B | 先进 wafer starts 增长 + HBM/CMP/clean steps 增加；国产替代提高本土渗透 | Commodity acids 15-28%；UHP/specialty cleans 35-55%；专有配方 60%+。 |
| CMP slurry delivery、点位过滤、化学品净化 | Entegris 液体过滤连续创纪录；HBM/CoWoS/CMP 强相关 | $0.7-1.1B / $1.1-1.6B / $1.6-2.3B | $3.2-4.7B / $4.7-6.8B / $6.8-9.5B | $7-10B / $10-16B / $16-24B | 先进逻辑/HBM/封装 CMP attach rate 近 100%；更高等级滤芯替换周期缩短 | 40-55% / 50-65% / 60-70%；耗材经常性收入最优。 |
| PFA/PVDF/PTFE/EP 管阀件、泵、流量/压力传感 | fluid management subsystems 2025 约 $5.3B，2032 约 $7.8B | $1.3-1.7B / $1.7-2.3B / $2.3-3.2B | $5.8-7.2B / $7.2-9.8B / $9.8-14B | $12-16B / $16-23B / $23-33B | 新厂全量配置；旧厂因 PFAS/安全/颗粒控制升级 15-30% | 28-42% / 38-52% / 48-62%；高纯阀件和一次性/耗材更高。 |
| 尾气处理、湿式/干式 scrubber、F-GHG abatement | SEMI/SCC 2025-2026 聚焦 F-GHG/N2O abatement；NF3 99% 级治理已可行 | $0.4-0.7B / $0.7-1.0B / $1.0-1.5B | $2.2-3.5B / $3.5-5.5B / $5.5-8.0B | $5-8B / $8-13B / $13-21B | 新 etch/deposition tool attach rate 高；存量 fab retrofit 2026 15-25%、2027 25-40% | 30-45% / 40-55% / 50-65%；服务和耗材提高生命周期利润。 |
| 在线分析、TOC/颗粒/金属/气体监测、facility digital twin | SEMICON West 2026 smart manufacturing 把 water management、toxic gas waste reduction 纳入主题 | $0.25-0.45B / $0.45-0.75B / $0.75-1.1B | $1.4-2.2B / $2.2-3.5B / $3.5-5.5B | $3.5-5.5B / $5.5-9B / $9-15B | 先进新厂 2026 40-60%，2027 60-80%；老厂 retrofit 更慢 | 硬件 35-55%；软件/服务 60-85%；客户锁定强。 |

### 3.1 已放量产品的增长区间

| 产品组 | 未来 1 年基准增长 | 乐观增长 | 极度超预期增长 |
|---|---:|---:|---:|
| UPW EPC + 回收 | +20-35% | +35-60% | +65-100% |
| onsite bulk gas + 电子气体 | +12-25% | +25-45% | +45-75% |
| gas/chemical delivery systems | +15-30% | +30-55% | +60-90% |
| 高纯湿化学品/过滤/净化 | +20-40% | +40-70% | +75-120% |
| abatement/PFAS/F-GHG | +25-50% | +50-85% | +90-150% |

## 4. 在研和即将快速增长的关键产品

| 在研/早期导入技术 | 当前阶段 | 成熟/放量时间 B/O/X | 未来 3 个月规模 B/O/X | 未来 1 年规模 B/O/X | 未来 2 年规模 B/O/X | 利润率假设 |
|---|---|---|---:|---:|---:|---|
| PFAS 捕集、浓缩、破坏与低 PFAS 材料替代 | 试点、法规评估、客户 qualification | 2027-2028 / 2027 / 2026H2 急单 | $0.05-0.15B / $0.15-0.35B / $0.35-0.70B | $0.4-1.0B / $1.0-2.0B / $2.0-4.0B | $1.5-4B / $4-8B / $8-15B | 早期 35-60%；成功进入 fab 标准后 50%+。 |
| 低-GWP 工艺气体、F2 清腔、NF3/N2O/F-GHG 高效 abatement | 部分成熟，替代气体仍需工艺验证 | abatement 2026；替代气 2027-2029 | $0.2-0.4B / $0.4-0.7B / $0.7-1.0B | $1.2-2.0B / $2.0-3.5B / $3.5-6.0B | $3-6B / $6-11B / $11-18B | 设备 35-55%；替代气/催化材料 45-65%。 |
| rare gas/He/Ne/Kr/Xe 回收净化 | 少数客户试点，受地缘与供应风险驱动 | 2027 / 2026H2 / 2026 急速导入 | $0.05-0.10B / $0.10-0.25B / $0.25-0.50B | $0.3-0.8B / $0.8-1.6B / $1.6-3.0B | $1-2.5B / $2.5-5B / $5-9B | 稀缺时 50-70%；回收系统受客户验证影响。 |
| hybrid bonding/advanced packaging 专用功能水、低损伤清洗 | HBM/CoWoS/SoIC/先进封装早期放大 | 2026H2 / 2026 / 2026 快速放量 | $0.15-0.30B / $0.30-0.55B / $0.55-0.90B | $0.8-1.5B / $1.5-2.8B / $2.8-5.0B | $2.5-5B / $5-9B / $9-16B | 35-55%；配方/设备绑定后 60%+。 |
| sub-2nm 颗粒过滤、ppt 金属去除树脂、point-of-use purifier | 先进逻辑/存储已导入，高端产品供给紧 | 2026 全年 / 2026H2 更快 / 2026 供不应求 | $0.3-0.6B / $0.6-0.9B / $0.9-1.4B | $1.6-2.8B / $2.8-4.5B / $4.5-7.0B | $4-7B / $7-12B / $12-20B | 45-65%；耗材替换周期形成高 ROIC。 |
| AI/数字孪生驱动的厂务水气化学系统控制 | NPI/greenfield 设计导入 | 2027 / 2026H2 / 2026 大客户试点 | $0.10-0.25B / $0.25-0.50B / $0.50-0.85B | $0.7-1.4B / $1.4-2.6B / $2.6-4.5B | $2-4B / $4-8B / $8-14B | 软件 70-90%；系统集成 25-45%。 |
| 化学品浓度/混配闭环控制、slurry reclaim 与 defect analytics | CMP/HBM/advanced packaging 需求推动 | 2026H2 / 2026 / 2026 快速拉动 | $0.15-0.30B / $0.30-0.60B / $0.60-1.0B | $0.9-1.6B / $1.6-3.0B / $3.0-5.5B | $2.5-5B / $5-9B / $9-16B | 35-60%；与客户 recipe 数据绑定后强。 |

## 5. 供给侧：产能结构、瓶颈、成本与价格传导

### 5.1 产能结构

| 层级 | 主要地区 | 主要公司 | 产能/工艺特点 |
|---|---|---|---|
| UPW EPC 与回收 | 日本、美国、欧洲、中国、台湾、韩国、新加坡 | Organo、Kurita、Nomura Micro Science、Ovivo/Ecolab、Veolia、Gradiant、Xylem/Evoqua、Aquatech、中国本土水处理/EPC | 以客户项目制为主，靠历史良率、工程经验、树脂/膜/分析能力和现场运维取胜。 |
| 大宗气体 onsite | 美国、日本、韩国、台湾、新加坡、中国、欧洲 | Air Liquide、Linde、Air Products、Nippon Sanso/Taiyo Nippon Sanso、Messer、SK Materials、盈德/杭氧等 | 现场 ASU/管网/液体槽车，通常长协、take-or-pay，客户厂区嵌入后切换极难。 |
| 特气与电子材料 | 日本、韩国、美国、德国、台湾、中国 | Merck/EMD、Entegris、Air Liquide Electronics、Linde、Air Products、SK Specialty、Soulbrain、Hansol、Kanto Denka、Resonac、Fujifilm、ADEKA、Stella Chemifa、Mitsubishi Gas Chemical、Showa Denko/Resonac、中国电子特气公司 | 纯度、杂质谱、批次稳定性和合规认证决定份额；先进气体/前驱体通常由少数公司垄断。 |
| 气体/化学品输送系统 | 美国、日本、台湾、中国、韩国、马来西亚、新加坡 | Ichor、Ultra Clean、MKS、Entegris、Kinetics、Exyte Technology、Critical Process Systems Group、Ceres Technologies、Diversified Fluid Solutions、JST、Mega Fluid Systems、Jewellok 等 | 气柜、VMB、chemical distribution、tool gas/liquid panels，与 WFE/OEM 和 fab spec 绑定。 |
| 高纯管阀件/过滤/传感 | 美国、日本、德国、瑞士、法国、中国台湾 | Swagelok、Parker、Fujikin、CKD、SMC、IDEX、Saint-Gobain、Georg Fischer、Entegris、Pall、Mott、Porvair、Horiba、Brooks、Bronkhorst、VAT、MKS | PFA/PVDF/PTFE/EP stainless、MFC、purifier、filter、pressure/flow/TOC/particle analytics，认证周期长。 |
| 尾气/废水/abatement | 欧洲、日本、韩国、美国、中国 | Edwards/Atlas Copco、Ebara、DAS Environmental Expert、CS Clean Solutions、MKS、GST、Kanken Techno、Centrotherm、Organo、Kurita、Ecolab/Ovivo、Veolia | F-GHG/NF3/N2O、酸碱、含氟、含铜、PFAS 废水处理，法规与客户碳目标驱动。 |

### 5.2 至少 10 条供给瓶颈

1. 项目工程人才：UPW、特气和化学系统需要跨工艺、EHS、自动控制、洁净施工和调试，不能靠普通水务/管道队伍快速替代。
2. 客户认证周期：先进 fab 的 UPW/化学品/特气供应商认证通常以月到年计；换供应商会影响良率数据、EHS 许可和 tool recipe。
3. UHP 材料：PFA/PTFE/PVDF、EP stainless、超低析出树脂、膜、filter media、MFC 关键部件供给集中。
4. onsite gas 长交期：ASU、purifier、compressor、cryogenic storage、pipeline 需要早期设计和施工，错过土建窗口会拖慢 fab ramp。
5. 特气原料和地缘风险：He、Ne、Kr、Xe、WF6、NF3、SiH4、DCS、BCl3 等受上游化工、稀有气和贸易限制影响。
6. 危化品许可与安全：毒性、腐蚀性、可燃/爆炸性气体和化学品需要本地审批、HAZOP、SEMI S2/S6、消防和应急体系。
7. 废水与 PFAS 监管：PFAS、含氟废水、N/P、重金属、F-GHG 让 fab 的开工、扩产和排水许可变成不确定变量。
8. 现场调试瓶颈：系统安装完还要清洗、passivation、particle flush、leak test、UPW/TOC/金属稳定，调试失败会延迟 wafer starts。
9. 分析检测能力：ppt 金属、1 ppb TOC、纳米颗粒、痕量离子和气体杂质需要高端实验室与在线监测，分析能力本身是瓶颈。
10. 价格传导不均：头部气体/过滤/净化/特气可转嫁成本，普通管道/EPC 和本土低端集成商更容易被客户压价。
11. 区域化重复建设：美国、日本、欧洲、印度和东南亚建厂要求本地化服务，供应商必须复制工程团队和备件网络。
12. 多项目并发：2026-2027 多个 AI/HBM fab 同时抢同一批设计院、施工队、长交期阀件和大宗气体装置。

### 5.3 成本构成与毛利决定因素

| 产品 | 成本构成估算 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| UPW EPC | 设备/膜/树脂/泵阀 35-45%；管道施工 25-35%；仪表自动化 10-15%；调试/项目管理 10-20% | 回收率、稳定水质、项目交付、客户历史数据 | 项目制报价 + change order；长交期和水许可紧张时可提价。 |
| UPW 运维/回收服务 | 人员/备件/耗材 40-55%；能耗/化学品 15-25%；监测与软件 10-20% | uptime、用水节省、良率责任、长期合同 | 按水量、节水收益分成、O&M 固定费。 |
| onsite gas | ASU/纯化/压缩/储存折旧 35-45%；能耗 25-35%；运维 10-15%；资本成本 10-20% | 客户信用、合同期、利用率、电价、供应冗余 | take-or-pay、成本转嫁、长期供气合同。 |
| 特气/前驱体 | 原料 25-45%；纯化/灌装 15-25%；检测 10-20%；安全/物流 10-20% | 杂质谱、批次稳定性、客户认证、上游稀缺性 | 长协 + pass-through；短缺品种可现货溢价。 |
| gas/chemical delivery systems | 高纯阀件/MFC/管路 35-50%；控制与安全 15-25%；集成测试 20-30% | 认证、EHS、自动化、冗余、安全记录 | 与 tool/fab spec 绑定，NPI 后价格粘性强。 |
| 湿化学品/过滤耗材 | 原料 25-45%；纯化/过滤/包装 20-30%；检测 10-20%；物流 5-15% | ppb/ppt 纯度、颗粒控制、客户 recipe、耗材替换 | 按 volume + purity premium；耗材由良率和更换周期驱动。 |

## 6. 竞争格局与壁垒

### 6.1 市场结构

| 细分 | 集中度判断 | 头部公司 |
|---|---|---|
| onsite bulk gas | 高集中，CR4 估计 70%+ | Air Liquide、Linde、Air Products、Nippon Sanso/TNSC |
| 电子特气/前驱体 | 中高集中，按品种高度集中 | Merck/EMD、Air Liquide、Entegris、SK Specialty、Resonac、Kanto Denka、Stella、ADEKA、Soulbrain、Hansol |
| UPW EPC | 中高集中，亚洲前沿 fab 由日系和欧美头部主导 | Organo、Kurita、Nomura Micro、Ovivo/Ecolab、Veolia、Gradiant、Xylem/Evoqua、Aquatech |
| 高纯化学品 delivery/CDS | 中等集中，项目制和客户 spec 强 | Ichor、Ultra Clean、MKS、Entegris、Kinetics、Exyte、CPS Group、Ceres、DFS、JST、Jewellok |
| 管阀件/MFC/filter/purifier | 单品类高集中，整体分散 | Swagelok、Parker、Fujikin、CKD、SMC、Entegris、Pall、Mott、Horiba、Brooks、MKS、VAT |
| abatement/wastewater | 中等集中，法规驱动本地玩家多 | Edwards、Ebara、DAS、CS Clean、MKS、GST、Kanken、Organo、Kurita、Ecolab/Ovivo、Veolia |

### 6.2 壁垒清单：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| 纯度壁垒 | 前沿制程的污染窗口是 ppt/ppb 级，1 次颗粒、金属或有机物异常就可能损失整批 wafer，客户愿意为确定性付费。 |
| 认证壁垒 | UPW、化学品、特气、过滤器与 tool recipe、yield history 绑定，替换供应商需要重新验证，机会成本很高。 |
| on-site 绑定 | onsite gas plant 和 fab 管网物理嵌入客户厂区，合同期长，切换等同重建基础设施。 |
| 安全/EHS 壁垒 | 毒性/腐蚀/可燃气体和化学品的事故代价巨大，安全记录、HAZOP、SEMI 标准和许可经验直接影响客户选择。 |
| 数据与运维壁垒 | 长期运行数据能优化水质、回收率、滤芯寿命和故障预测，后来者缺少真实 fab 数据。 |
| 规模壁垒 | 多 fab 同时施工需要全球项目管理、备件、现场工程师和区域化制造，不是小公司拿到图纸就能复制。 |
| 供应链壁垒 | UHP 树脂、膜、MFC、阀件、稀有气、特气原料和高纯包装材料都有上游卡点，头部供应商优先获得分配。 |
| 法规壁垒 | PFAS、F-GHG、废水、危化品和地方排放标准提高，合规系统可直接决定项目能否按期投产。 |

### 6.3 长期高 ROIC/高毛利层级

1. onsite gas 长协：资本密集但合同期长、客户切换成本极高，Air Liquide/Linde/Air Products 模式最稳。
2. 过滤/净化/分析耗材：与 wafer starts 和良率绑定，经常性收入、毛利高、替换周期短。
3. 特气/高纯化学品专有配方：客户认证后粘性强，短缺时有溢价。
4. UPW 回收/O&M：EPC 一次性收入之后，运维、水回收、废水合规服务可变成长期收入。
5. gas/chemical delivery 安全集成：不一定毛利最高，但客户认证和 EHS 风险让头部玩家可持续定价。

## 7. 2026 关键变化：3 个最可能拐点

1. AI/HBM fab utility 抢单从“规划”转向“采购与施工”。SEMI 的 300mm fab 支出和 TrendForce 的 CSP capex 同时上修，意味着厂务系统在 2026H2 会看到更多长交期订单。
2. 水回收和 PFAS/F-GHG 合规从 ESG 叙事变成开工约束。美国、日本、欧洲新厂选址越来越受水权、排放和社区许可影响，UPW 回收、废水分流、尾气治理的价值上移。
3. onsite gas 长协和本地化供给加速。Air Liquide 日本 €200M、Linde/Samsung 平泽、VSMC Singapore 等显示气体供应商正在跟随 AI/存储客户建设本地固定资产。

## 8. 2027 关键变化：3 个最可能拐点

1. HBM4/Rubin/MI400/TPU8 量产把需求从逻辑厂扩散到 DRAM/HBM 和先进封装厂。湿法、CMP、清洗、bonding、plating、UPW 和高纯化学品需求强度上行。
2. CHIPS 相关美国/欧洲/日本 fab 进入 commissioning，EPC 收入转换为 O&M、耗材、gas volume 和 chemical volume。真正利润释放从一次性设备转向长期服务。
3. Fab facility digital twin 和自动化进入水气化学系统。SEMICON West 2026 已把水管理、液体化学品和 toxic gas waste reduction 放入 smart manufacturing 主题，2027 会形成批量 retrofit。

## 9. 头部公司与细分公司清单

| 细分 | 公司 |
|---|---|
| UPW EPC/回收/水管理 | Organo、Kurita Water Industries、Nomura Micro Science、Ovivo Ultrapure Water+ by Ecolab、Veolia、Gradiant、Xylem/Evoqua、Aquatech、DuPont Water Solutions、Toray、Asahi Kasei、Mitsubishi Chemical、Lanxess/Purolite、苏州晶瑞/中国本土水处理工程商 |
| onsite bulk gas | Air Liquide、Linde、Air Products、Nippon Sanso/Taiyo Nippon Sanso、Messer、SK Materials、盈德气体、杭氧股份、液化空气中国、林德中国 |
| 电子特气/前驱体 | Merck KGaA/EMD Electronics、Air Liquide Electronics、Entegris、Linde、Air Products、SK Specialty、Soulbrain、Hansol Chemical、Kanto Denka、Resonac、ADEKA、Stella Chemifa、Mitsubishi Gas Chemical、Fujifilm Electronic Materials、JSR、TOK、DuPont、UP Chemical、DNF、Mecaro、Yoke Technology、金宏气体、华特气体、昊华科技、雅克科技 |
| 湿电子化学品 | Kanto Chemical、Stella Chemifa、Mitsubishi Chemical、Mitsubishi Gas Chemical、Morita、Fujifilm、TOK、JSR、Shin-Etsu Chemical、Sumitomo Chemical、Merck/EMD、DuPont、Entegris、Soulbrain、Dongjin Semichem、晶瑞电材、江化微、上海新阳、安集科技 |
| CMP slurry/清洗/过滤 | Entegris、Cabot Microelectronics/CMC Materials、Fujimi、Resonac、Merck、DuPont、Versum/EMD、Pall、Mott、Porvair、Donaldson、3M、Anji Microelectronics、Soulbrain |
| gas/chemical delivery 系统 | Ichor、Ultra Clean Holdings、MKS Instruments、Entegris、Kinetics、Exyte Technology、Critical Process Systems Group、Ceres Technologies、Diversified Fluid Solutions、JST Manufacturing、Mega Fluid Systems、Cambridge Fluid Systems、Jewellok、Advanced Plastic Services |
| 高纯管阀件/MFC/传感 | Swagelok、Parker Hannifin、Fujikin、CKD、SMC、IDEX、Saint-Gobain、Georg Fischer、Entegris、Pall、Mott、Porvair、Horiba、Brooks Instrument、Bronkhorst、MKS、VAT、Ham-Let、Gemu、Fitok |
| abatement/scrubber/废气废水 | Edwards Vacuum/Atlas Copco、Ebara、DAS Environmental Expert、CS Clean Solutions、MKS、GST、Kanken Techno、Centrotherm、Busch、Pfeiffer、Organo、Kurita、Ecolab/Ovivo、Veolia、Gradiant、Aquatech |
| fab EPC/厂务集成 | Exyte、Jacobs、DPR Construction、M+W legacy/Exyte、Kinetics、Hoffman Construction、Bechtel、Fluor、Samsung Engineering、Kajima、Obayashi、清水建设、中国电子系统工程、中电二公司、亚翔集成 |

## 10. 投资价值排序

| 排名 | 子方向 | 投资逻辑 | 核心风险 |
|---:|---|---|---|
| 1 | onsite gas 长协与电子气体 | 长合同、客户嵌入、AI/HBM 新厂直接拉动，收入和 ROIC 可见度最高 | 电价、上游稀有气、项目延期 |
| 2 | UPW 回收/O&M 与高端 EPC | 水许可和良率刚需，Ecolab/Ovivo 交易抬高行业认知 | 项目制收入波动、施工人才不足 |
| 3 | 过滤/净化/分析耗材 | content per wafer 上升，经常性收入，高毛利 | 客户库存周期、替代供应商认证 |
| 4 | gas/chemical delivery 与高纯管阀件 | 先进 fab 和 WFE 子系统同时受益，EHS 与认证壁垒强 | 毛利低于耗材，部分环节竞争分散 |
| 5 | PFAS/F-GHG/PFAS wastewater | 法规期权大，若成为开工门槛，弹性极高 | 技术路线未完全收敛，验证周期长 |
| 6 | 高纯湿化学品/特气国产替代 | 中国 AI 芯片和本土 fab 扩产打开增量 | 先进制程认证、批次稳定性和价格竞争 |

## 11. 主要参考来源

| 编号 | 来源 | 链接 |
|---:|---|---|
| 1 | Gartner：2026 全球半导体收入超过 $1.3T、AI 基建支出增长 | https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026 |
| 2 | TrendForce/PRNewswire：Top 9 CSP 2026 capex 约 $830B | https://www.prnewswire.com/news-releases/north-american-ai-data-center-expansion-drives-2026-capex-of-top-nine-csps-to-us830-billion-says-trendforce-302764269.html |
| 3 | SEMI：2026-2028 300mm fab equipment spending $374B | https://www.semi.org/en/semi-press-release/semi-reports-global-300mm-fab-equipment-spending-expected-to-total-374-billion-dollars-over-next-three-years |
| 4 | TSMC 1Q26 earnings release | https://investor.tsmc.com/english/encrypt/files/encrypt_file/qr/phase4_reports/2026-04/bd8eb0403902fdea59a2f5e390e48d010b50edc9/1Q26%20EarningsRelease_WoG.pdf |
| 5 | Air Liquide：日本广岛 €200M AI 芯片气体项目 | https://www.airliquide.com/group/press-releases-news/2026-04-16/air-liquide-invests-200-million-euros-japan-support-leading-semiconductor-manufacturer-production |
| 6 | Air Liquide：VSMC Singapore 长期供气协议 | https://electronics.airliquide.com/air-liquide-signs-long-term-gas-supply-agreement-vsmc-support-singapores-semiconductor-industry |
| 7 | Linde：扩大向 Samsung Pyeongtaek 供应半导体气体 | https://www.linde.com/news-and-media/2025/linde-to-expand-supply-of-industrial-gases-to-samsung-in-south-korea |
| 8 | Ecolab：收购 Ovivo Electronics UPW 业务 | https://investor.ecolab.com/news/news-details/2025/Ecolab-to-Acquire-Ovivos-Electronics-Ultra-Pure-Water-Business/default.aspx |
| 9 | Organo：半导体与水、1 ppt、1000 ton/hour、>80% 回收率 | https://www.organo.co.jp/english/wp-content/uploads/2025/11/Financial-Results-for-First-Half-of-Fiscal-Year-Ending-March-31-2026.pdf |
| 10 | Kurita America：300mm fab 用水、UPW 与回收 | https://www.kuritaamerica.com/industries/microelectronics |
| 11 | Nomura Micro Science：公司与 R&D/UPW 技术 | https://www.nomura-nms.co.jp/english/about/ |
| 12 | Nomura Micro Science 2026 Q3 摘要 | https://www.gyokaidigest.com/companies/nomura-micro/report/2026-Q3 |
| 13 | TechInsights/TECHCET：2026 electronic gases 市场约 $6.8B | https://www.techinsights.com/blog/electronic-gases-market-reach-681b-2026-driven-advanced-node-demand |
| 14 | Gasworld/TECHCET：2026 semiconductor electronic gases revenue 约 $6.87B | https://www.gasworld.com/story/specialty-gases-to-grow-8-7-in-2026-forecasts-techcet/2171265.article/ |
| 15 | Grand View Research：semiconductor chemicals 2026 约 $17.46B | https://www.grandviewresearch.com/industry-analysis/semiconductor-chemicals-market-report |
| 16 | 360iResearch：semiconductor UPW system 2026 约 $1.82B | https://www.360iresearch.com/library/intelligence/semiconductor-ultrapure-water-system |
| 17 | LP Information/MarketResearch：semiconductor UPW system 2025 $1.939B 到 2032 $3.244B | https://www.marketresearch.com/LP-Information-Inc-v4134/Global-Semiconductor-Ultrapure-Water-System-43353425/ |
| 18 | Business Research Insights：semiconductor gas delivery system 2026 约 $1.64B | https://www.businessresearchinsights.com/market-reports/semiconductor-gas-delivery-system-market-114529 |
| 19 | SemiconductorInsight：high purity chemical delivery systems 2026 约 $1.48B | https://semiconductorinsight.com/report/high-purity-chemical-delivery-systems-market/ |
| 20 | DataInsights：bulk chemical delivery system 2026 约 $1.026B | https://www.datainsightsmarket.com/reports/bulk-chemical-delivery-system-bcds-for-semiconductor-853261 |
| 21 | Entegris 1Q26 results | https://investor.entegris.com/news/news-details/2026/Entegris-Reports-Results-for-First-Quarter-of-2026/default.aspx |
| 22 | Ultra Clean 1Q26 results | https://www.prnewswire.com/news-releases/ultra-clean-reports-first-quarter-2026-financial-results-302756140.html |
| 23 | Ichor 1Q26 results | https://www.sec.gov/Archives/edgar/data/1652535/000165253526000028/ex-991_26q1xearnings.htm |
| 24 | MKS 1Q26 results | https://www.globenewswire.com/news-release/2026/05/06/3289424/16396/en/mks-inc-reports-first-quarter-2026-financial-results.html |
| 25 | TECHCET/CMC Conference 2026 | https://www.techinsights.com/2026-cmc-conference |
| 26 | UltraFacility 2026 UPW forum | https://www.ultrafacility.io/ultrapure-water/ |
| 27 | SEMICON West 2026 smart manufacturing call for abstracts | https://www.semiconwest.org/programs/call-for-abstracts/smart-manufacturing-2026 |
| 28 | SEMI SMC 2026：Materials Innovation in the AI Era | https://www.semi.org/en/connect/events/strategic-materials-conference-smc |
| 29 | SIA PFAS Consortium | https://www.semiconductors.org/pfas/ |
| 30 | SIA Senate EPW testimony on chemical controls | https://www.semiconductors.org/wp-content/uploads/2026/03/Senate-EPW-testimony-3.4.2026.pdf |
| 31 | SEMI Semiconductor Climate Consortium | https://www.semi.org/en/industry-groups/semiconductor-climate-consortium |

非投资建议。以上估算用于产业链研究和情景分析，关键风险包括 AI capex 兑现不及预期、客户 fab 延期、水权和排放许可受阻、特气/稀有气短缺、PFAS/F-GHG 法规变化、工程人才不足、价格竞争和地缘贸易限制。
# 行业调研：【半导体检测量测设备】

> 截至日期：2026-05-08  
> 研究范围：晶圆制造与先进封装中的检测、量测、过程控制与相邻测试设备，包括光学缺陷检测、电子束检测/复检、CD-SEM、overlay/OCD/薄膜/材料/X-ray量测、reticle/mask检测、HBM/CoWoS/2.5D/3D先进封装检测量测、IC substrate/PLP检测、探针/ATE/SLT等广义测试环节。  
> 核心假设：对2026-2027 AI计算中心建设采取明显乐观假设。若缺少直接公开数据，采用“AI芯片出货、HBM stack、CoWoS/先进封装产能、WFE capex、设备公司订单/指引、客户良率经济性”推演，并标注为模型估算。非投资建议。

## 0. 一页结论

半导体检测量测设备是2026年AI算力扩张中最容易被低估的“良率税”和“产能保险”。AI GPU/ASIC不是普通芯片：单颗/单封装价值高、die size大、HBM stack多、CoWoS/SoIC/EMIB/有机载板/玻璃基板/液冷/高速互连共同决定最终良率。每多一个chiplet、每多一层HBM、每多一次hybrid bonding，都会把检测量测需求从线性增加变成接近非线性增加。

关键判断：

| 判断 | 结论 |
|---|---|
| 2026最确定的技术路径 | 光学缺陷检测 + CD/overlay/OCD量测 + e-beam复检 + HBM/CoWoS先进封装2D/3D检测 + 数据分析软件。最先放量的是成熟2.5D/HBM3E/GB300/MI350/TPU/Trainium链条，不是最激进的全3D封装。 |
| 2027主线 | HBM4、Rubin/MI400/TPU8/OpenAI-Broadcom XPU、Meta MTIA后续、CPO/硅光和panel-level packaging推动multi-beam e-beam、X-ray hybrid metrology、hybrid bonding inspection、PLP/glass-core检测进入放量。 |
| TAM锚点 | Gartner预计2026全球半导体收入$1.320T、AI半导体约占30%；SEMI预计半导体制造设备$145B/$156B分别对应2026/2027。按KLA年化收入、份额和设备结构推算，2026全球检测量测/过程控制/相邻测试收入池约$36-48B，其中狭义process control约$21-27B，广义测试约$12-18B。 |
| 最强定价权 | KLA式前道过程控制、ASML/HMI多束e-beam、Lasertec/KLA EUV mask检测、Hitachi CD-SEM、Onto/Nova/Rigaku X-ray/混合量测、Advantest/Teradyne高端ATE、FormFactor/Technoprobe高端探针卡。 |
| 最强弹性 | 先进封装检测量测、HBM KGD/stack test、multi-beam e-beam、X-ray CD/材料量测、panel/glass-core检测、AI defect classification软件。 |
| 最大瓶颈 | 精密光学与激光、电子光学柱/高速stage、X-ray源和探测器、图像计算服务器内存/AI加速卡、客户recipe/算法数据、现场应用工程师、出口管制和客户认证周期。 |

近期一手事实锚：

- Gartner 2026-04：预计2026全球半导体收入$1.320T，2027为$1.555T；2026内存收入$633B，DRAM价格预计+125%，AI半导体约占总收入30%。
- SEMI 2025-12：全球半导体制造设备销售预计2025 $133B、2026 $145B、2027 $156B，增长主要由AI相关leading-edge logic、memory和advanced packaging驱动；测试设备2025预计$11.2B，2026/2027继续+12.0%/+7.1%。
- KLA 2026-04：FY26 Q3收入$3.415B，其中Semiconductor Process Control $3.084B；公司称受益AI生态、foundry/logic、memory、advanced packaging和services，下一季收入指引$3.575B。电话会口径显示先进封装process-control收入从2025约$635M增至2026约$1B。
- Onto 2026-05：Q1收入$291.9M，Q2指引$320-330M；Dragonfly G5已在2.5D logic和HBM客户获得资格；Atlas G6获得GAA量测客户；公司拟以约$710M买入Rigaku 27%权益，补X-ray/AI Diffract混合量测。
- Onto 2026-03/04：HBM厂商为HBM4 ramp选择Dragonfly G5，G5+3Di承诺双位数订单，Q2开始发货；Dragonfly平台2026收入预计同比增长>50%。
- Nova 2026-02：2025收入$880.6M，同比+31%，GAA、DRAM、advanced packaging创纪录；Q1 2026收入指引$222-232M。
- Camtek 2026-02：公司定位高端inspection/metrology，覆盖Advanced Interconnect Packaging、Heterogeneous Integration、Memory/HBM、compound semiconductor、MEMS/RF，并明确将AI、HBM、chiplet需求作为业务驱动。
- ASML eScan 1100：面向3nm及以后，25束multi-beam e-beam，吞吐相对单束最高15倍，支持电压对比与物理缺陷检测。
- Applied Materials 2025-10/2026论坛：GAA、HBM、advanced packaging推动3D结构量测挑战；公司强调eBeam在3D架构高吞吐高分辨成像中的重要性。
- SEMICON Korea 2026：先进封装论坛直接提出传统封装线MI工具已不足，需要类似前道fab的检测量测系统。

## 1. AI芯片路线对检测量测的拉动

项目内`ai_chip_research_2026_2027.md`显示，2026-2027出货/价值权重最高的平台包括NVIDIA B300/GB300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon MLU590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200、Alibaba Zhenwu 810E、AMD MI400/MI455X，以及2027更强的Rubin/TPU8/OpenAI-Broadcom XPU。它们对检测量测的影响如下：

| AI芯片/平台 | 制造与封装路线 | 对检测量测设备的增量 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | TSMC 4NP + CoWoS-L/S + HBM3E + NVL72整柜 | 光学patterned inspection、reticle/mask检测、overlay/OCD、HBM KGD、interposer/RDL、microbump、warpage、NVLink/SerDes burn-in。 |
| NVIDIA Rubin/Vera Rubin | HBM4 + 新一代CoWoS/SoIC/大尺寸封装 + SOCAMM/LPDDR CPU侧 | HBM4 16H/定制base die量测、multi-beam e-beam、X-ray/3D metrology、hybrid bonding、系统级SLT。2026H2小批，2027放量。 |
| AWS Trainium2/3 | 自研ASIC + HBM + UltraServer scale-up | 内部供应链不全公开，但会消耗先进逻辑、HBM、封装后测试、系统级burn-in；Trainium3 3nm/HBM带来更高前道和封装过程控制强度。 |
| Google TPU v7 Ironwood/TPU8 | Broadcom/Google定制XPU + HBM + pod互连 | 推理ASIC量大，强调2.5D、HBM、advanced substrate、package test、pod级互连测试；TPU8在2027提高HBM4/X-ray量测需求。 |
| AMD MI350/MI400 Helios | MI350 HBM3E；MI400/MI455X HBM4、72 GPU rack | MI350拉动成熟2.5D和HBM3E检测；MI400 2026H2-2027拉动HBM4、large package、open rack互连、UALink/Ethernet测试。 |
| Meta MTIA / OpenAI-Broadcom XPU / Maia 200 | 云厂自研ASIC，2.5D/HBM/高密推理 | 设计start数量增加，使process control不只跟GPU，还跟每个hyperscaler ASIC节点/封装recipe绑定；SerDes、silicon photonics、CPO测试增量上升。 |
| Huawei/Cambricon/Alibaba等国产AI芯片 | DUV多重曝光、本土封装、HBM/替代内存、OAM/超节点 | 低良率会放大检测价值；国产检测量测在光学、CD-SEM、overlay、缺陷复检、ATE、探针卡出现替代机会，但高端仍受光学/e-beam/算法/客户认证约束。 |

### 1.1 2026的机遇和挑战

**机遇：**

1. AI芯片价值密度上升。若单个高端AI package价值按$30k-70k估算，1%良率改善在100万颗级别就是$300M-700M价值回收，足以支撑$3M-20M/台的高端检测量测工具和长期服务合同。
2. 先进封装从后道走向“前道化”。传统封装AOI不足以覆盖CoWoS/HBM/SoIC，OSAT和foundry必须引入前道级MI系统。
3. HBM4/16H stack和custom base die让X-ray、e-beam、bonding inspection、KGD test变成刚需。
4. Hyperscaler自研ASIC增加design start数量，扩大recipe、mask、first silicon debug和ramp inspection需求。
5. 2026客户更关心“排队拿slot”。KLA电话会中提到客户对2027 slot和capacity planning的紧迫感，说明设备交付本身可能成为上游瓶颈。

**挑战：**

1. 设备供应链瓶颈会从“整机”拆成光源、镜头、stage、电子光学、计算服务器、DRAM、FPGA/GPU、x-ray source、探测器、真空件。
2. 工具不是买来即用，recipe开发、匹配、false positive/false negative调参、ADC模型训练通常需要数月。
3. 客户导入周期长。先进节点和HBM/AP客户认证常为6-18个月，错过平台窗口很难补单。
4. 出口管制会改变中国大陆订单结构，高端光学/e-beam/reticle工具受影响更大。
5. AI内存价格上涨反过来提高检测设备BOM成本。KLA已提示图像处理计算机中的DRAM成本对毛利形成约100bp压力。

### 1.2 新技术成熟和放量时间

| 技术路径 | 2026基准 | 2026乐观 | 2026极度超预期 | 2027基准 | 2027乐观/极度超预期 |
|---|---|---|---|---|---|
| 光学patterned wafer inspection | 成熟放量，继续绑定N3/N2、HBM DRAM、GB300 | Sampling更多，AI defect classifier减少误报 | 客户为良率抢装，lead time延长 | 稳定增长 | 与e-beam/X-ray融合，软件订阅占比上升 |
| e-beam review / single-beam inspection | 复检和热点分析为主 | 更多inline层使用e-beam | HBM4/2nm缺陷痛点提前扩大 | 多束系统扩大HVM应用 | multi-beam在先进逻辑/DRAM关键层形成小规模放量 |
| multi-beam e-beam inspection | ASML eScan 1100等进入高端HVM资格验证 | 25-beam工具在3nm/2nm关键层加速导入 | 客户以高ASP换交期，成为EUV/2nm缺陷发现核心工具 | 小批量收入明确 | 若Rubin/TPU8/ASIC强于预期，2027H2进入多客户批量 |
| CD-SEM / high-res SEM | GAA、DRAM、HBM继续需求强 | AI算法改善throughput和重复性 | 国产/中国客户用更多测点弥补良率 | 稳定增长 | 3D CD、tilt、sidewall、hybrid data fusion升级 |
| OCD/overlay/film/metals | Atlas/SpectraShape/YieldStar/Archer/Nova方案继续放量 | GAA和DRAM量测强度上升 | 2nm和HBM4抢产能，量测成为ramp瓶颈 | 高速增长 | 混合X-ray/optical成为高端标配 |
| X-ray/CD-SAXS/XRR/XRF | 2026上半年验证加速，Onto/Rigaku、KLA Axion、Nova受益 | HBM/DRAM/GAA推动从实验室到inline | X-ray被更多内存厂直接列入HVM recipe | 2027明显放量 | 先进封装、HBM4、GAA、玻璃基板共同推高TAM |
| HBM/CoWoS先进封装检测 | 已经放量，Onto/KLA/Camtek/Nova受益 | Dragonfly G5、KLA AP组合、Camtek OSAT订单继续扩 | 2026H2 AP设备供不应求，OSAT超前下单 | 2027继续高增 | PLP/glass core/hybrid bonding把检测需求再抬一阶 |
| Reticle/EUV mask检测 | EUV mask/blank继续高壁垒 | AI ASIC设计start增加mask检查需求 | N2/Rubin/ASIC mask改版密集，Lasertec/KLA满载 | 稳定高景气 | High-NA EUV进一步提升mask inspection难度 |
| Panel-level/glass-core检测 | qualification为主 | AI封装供应链开始pilot | 2026H2少量订单拉动 | 2027小批量生产 | 极度乐观下成为2.5D产能外溢主线之一 |
| CPO/硅光检测与测试 | 2026订单小但增长快 | CPO switch/1.6T optics设计导入 | 1.6T/3.2T功耗压力推动提前导入 | 2027开始小批 | 若CPO进入AI交换机主流，光电检测弹性很大 |

**2026最可能的技术路径：** 光学inspection + e-beam review + CD-SEM + overlay/OCD + X-ray材料/结构量测 + HBM/CoWoS 2D/3D先进封装检测。  
**2027最可能放量的新路径：** multi-beam e-beam、HBM4/X-ray hybrid metrology、hybrid bonding inspection、panel/glass-core检测、CPO/硅光检测。

## 2. 已经开始放量的关键产品：规模、渗透率、利润率

口径：未来3个月约为2026-05至2026-08收入/订单池；未来12个月为2026H2-2027H1；未来24个月为2026H2-2028H1。以下为全球收入池/订单池模型估算，存在分类重叠；不应简单加总。

| 已放量产品/技术 | 主要公司 | 未来3个月规模：基准/乐观/极度 | 未来12个月规模：基准/乐观/极度 | 未来24个月规模：基准/乐观/极度 | 渗透率路径 | 毛利率/利润率判断 |
|---|---|---:|---:|---:|---|---|
| 光学patterned wafer缺陷检测 | KLA、Applied、Onto、Hitachi、部分国产厂 | $1.8-2.5B / $2.4-3.2B / $3.2-4.2B | $7.5-10.5B / $10-13.5B / $13-18B | $15-21B / $21-30B / $30-42B | 先进逻辑/DRAM关键层70-90%；先进封装前道化后AP层渗透率从25-40%升至45-65% | 高端系统毛利58-68%；极缺时服务/软件拉高综合利润率。 |
| unpatterned wafer/particle/edge inspection | KLA、Onto、SCREEN、Hitachi、国产替代 | $0.7-1.0B / $0.9-1.3B / $1.2-1.8B | $3-4.5B / $4-6B / $5.5-8B | $6-9B / $8-13B / $12-18B | EUV/3nm/2nm wafer quality、HBM DRAM wafer扩产推动采样密度上升 | 毛利45-60%；硅片/外延/wafer incoming环节客户分散，定价弱于patterned inspection。 |
| e-beam defect review与热点检测 | ASML/HMI、KLA、Applied、Hitachi、JEOL | $0.7-1.1B / $1.0-1.5B / $1.5-2.2B | $3.2-4.8B / $4.5-6.5B / $6.5-9B | $7-11B / $10-16B / $16-24B | 关键缺陷复检近100%；inline e-beam面积覆盖仍低，2027从<5%向8-15%提升 | 毛利55-70%；电子光学和算法壁垒高，服务粘性强。 |
| CD-SEM/e-beam metrology | Hitachi High-Tech、Applied、ASML/HMI、KLA、JEOL、国产追赶 | $0.6-0.9B / $0.9-1.2B / $1.2-1.8B | $2.7-3.8B / $3.7-5.2B / $5.2-7.5B | $5.5-8B / $8-12B / $12-18B | GAA、DRAM、HBM、EUV layers采样点上升；先进客户渗透率高，国产替代从成熟节点向先进节点追赶 | 毛利50-65%；top CD-SEM客户锁定强。 |
| overlay / registration / scanner feed-forward量测 | KLA Archer、ASML YieldStar、Onto、Nova、Nikon/Canon生态 | $0.8-1.2B / $1.1-1.6B / $1.6-2.3B | $3.5-5.2B / $5-7.5B / $7-10B | $8-12B / $12-18B / $18-27B | EUV多重图形、N2、GAA、HBM DRAM使overlay测点密度提高；高阶scanner correction成为标配 | 毛利55-70%；与scanner/recipe/数据闭环绑定，切换成本高。 |
| OCD/shape/film/material/metals metrology | KLA、Onto、Nova、Applied、Rigaku、Bruker、Semilab | $1.2-1.8B / $1.7-2.4B / $2.3-3.2B | $5.5-8B / $7.5-10.5B / $10-15B | $12-18B / $17-25B / $25-38B | GAA nanosheet、DRAM/HBM、3D NAND、hybrid bonding材料堆叠推动从2D CD到3D profile/material composition | 毛利55-70%；软件模型/IP和recipe沉淀带来高ROIC。 |
| Reticle/mask blank/mask shop检测量测 | Lasertec、KLA、ASML/HMI、NuFlare、JEOL、Carl Zeiss SMT | $0.8-1.2B / $1.1-1.6B / $1.5-2.2B | $3.5-5.2B / $5-7.2B / $7-10B | $7-11B / $10-16B / $15-24B | AI ASIC design start和EUV mask复杂度上升；High-NA前夜继续提高mask缺陷容忍度要求 | 毛利60-75%；EUV mask blank检测壁垒极高。 |
| HBM/CoWoS/先进封装wafer-level inspection/metrology | KLA、Onto、Camtek、Nova、Koh Young、ViTrox、UnitySC | $0.9-1.4B / $1.3-2.0B / $2.0-3.0B | $4.5-7B / $7-11B / $11-16B | $10-18B / $17-28B / $28-42B | 2.5D/HBM/AP产线渗透率从2025约30-45%升至2027约60-80%；OSAT导入前道级MI | 毛利50-65%；供不应求产品有5-15%溢价。 |
| IC substrate / panel RDL / glass-core AOI与3D量测 | KLA Lumina/Zeta、Koh Young、ViTrox、Camtek、Orbotech/KLA | $0.3-0.6B / $0.5-0.9B / $0.8-1.3B | $1.5-2.8B / $2.5-4.5B / $4-7B | $4-8B / $7-14B / $12-24B | 先进IC substrate渗透率2026 10-20%，2027 20-35%；glass-core/PLP若起量会跃升 | 毛利35-55%；高端玻璃基板/PLP工具毛利更高。 |
| ATE、probe card、SLT、burn-in | Advantest、Teradyne、Cohu、Chroma、FormFactor、Technoprobe、MPI、Keysight | $3.0-4.0B / $3.7-5.0B / $4.8-6.2B | $12-16B / $15-20B / $20-28B | $26-36B / $36-50B / $50-70B | 高端GPU/ASIC/HBM测试attach接近100%；SLT和burn-in时间随功耗/互连复杂度上升 | ATE毛利55-65%；探针卡35-55%；高端HBM探针和SLT稀缺时更高。 |
| 过程控制软件、ADC/AI defect classification、yield analytics | KLA、Onto、Applied、ASML、Siemens、PDF Solutions、Synopsys/Cadence连接生态 | $0.4-0.7B / $0.6-1.0B / $0.9-1.5B | $2-3.5B / $3-5.5B / $5-8B | $5-9B / $8-14B / $13-22B | 2026多为设备随附和服务合同；2027开始成为跨工具数据层 | 软件毛利75-90%；一旦绑定fab数据，切换成本极高。 |

### 2.1 三情景增长判断

| 技术 | 基准增长 | 乐观增长 | 极度超预期增长 |
|---|---|---|---|
| 前道process control整体 | 2026 +15-25%，2027 +15-25% | 2026 +25-35%，2027 +25-40% | 2026 +35-50%，2027 +45-70% |
| 先进封装检测量测 | 2026 +40-60%，2027 +30-50% | 2026 +60-90%，2027 +50-80% | 2026翻倍，2027再+80%至+120% |
| HBM/DRAM相关量测测试 | 2026 +35-60%，2027 +35-55% | 2026 +60-90%，2027 +60-90% | 2026 +100%，2027 +100%+ |
| e-beam/multi-beam | 2026 +20-35%，2027 +30-50% | 2026 +40-60%，2027 +60-90% | 2026 +80%，2027 +100%+ |
| X-ray/hybrid metrology | 2026 +30-50%，2027 +40-70% | 2026 +60-90%，2027 +80-120% | 从小基数翻倍以上，2027进入高端fab标配 |

## 3. 在研和即将快速增长的关键产品

| 在研/早期放量技术 | 当前阶段 | 未来3个月规模：基准/乐观/极度 | 未来12个月规模：基准/乐观/极度 | 未来24个月规模：基准/乐观/极度 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| Multi-beam e-beam inline inspection | ASML eScan 1100已明确25束/15x吞吐；KLA/Applied也在推进eBeam portfolio | $0.2-0.5B / $0.4-0.8B / $0.8-1.3B | $1.2-2.2B / $2.2-4B / $4-7B | $4-8B / $8-15B / $15-28B | 2026关键层pilot，2027高端逻辑/DRAM/HBM关键层5-15%渗透 | 毛利60-75%；电子光学、stage、数据吞吐壁垒极高。 |
| Optical + X-ray hybrid metrology / AI Diffract | Onto-Rigaku、KLA Axion、Nova materials/chemical metrology已进入客户验证 | $0.2-0.4B / $0.4-0.8B / $0.8-1.2B | $1.2-2.5B / $2.5-4.5B / $4.5-8B | $4-8B / $8-16B / $15-30B | 2026 memory/logic evaluation，2027在GAA/DRAM/HBM4部分HVM化 | 软件毛利近80-95%；X-ray硬件毛利50-65%。 |
| Hybrid bonding / die-to-wafer / wafer-to-wafer inspection | SoIC、HBM、3D chiplet需要post-bond void/overlay/particle检测 | $0.2-0.5B / $0.4-0.8B / $0.8-1.5B | $1.5-3B / $3-6B / $6-10B | $6-12B / $11-22B / $20-38B | 2026在HBM/SoIC early ramp，2027高端AI package渗透10-25% | 毛利50-70%；良率事故成本极高，客户愿意付溢价。 |
| Panel-level packaging / glass-core substrate inspection | Onto JetStep、KLA Lumina/Zeta、Koh Young/ViTrox等进入资格验证 | <$0.2B / $0.3-0.6B / $0.6-1B | $0.8-1.8B / $1.8-3.5B / $3.5-7B | $4-9B / $8-18B / $16-35B | 2026 pilot；2027 AI device packaging供应商小批；2028可能真正放量 | 早期毛利不稳，成熟后45-60%；设备/材料先受益。 |
| CPO/硅光wafer inspection与光电测试 | 800G/1.6T光互联已放量，CPO/OIO仍早期 | $0.1-0.3B / $0.2-0.5B / $0.5-1B | $0.8-1.8B / $1.8-4B / $4-8B | $3-7B / $7-16B / $15-35B | 2026设计导入，2027随CPO switch/1.6T AI network小批 | 高端光电测试毛利45-65%；若CPO变主流，弹性巨大。 |
| In-situ metrology、virtual metrology、agentic APC | R2R/APC已有基础，AI fab运营开始进入论坛主题 | $0.2-0.4B / $0.4-0.8B / $0.8-1.3B | $1.5-3B / $3-6B / $6-10B | $5-10B / $10-20B / $18-35B | 2026从单工具/单module开始，2027跨tool/fab数据闭环 | 软件毛利80%+；但数据接入和客户IT/OT安全是瓶颈。 |
| AI foundation model for defect images / recipe automation | 现有ADC升级，训练数据来自设备商历史图库和客户fab | $0.1-0.3B / $0.3-0.6B / $0.6-1B | $0.8-1.8B / $1.8-3.5B / $3.5-7B | $3-7B / $7-15B / $14-28B | 2026设备随附，2027成为服务合同和yield analytics增值项 | 极高毛利；数据壁垒和客户信任决定定价。 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能和公司结构

| 层级 | 主要地区 | 代表公司 | 关键工艺/产品 |
|---|---|---|---|
| 前道光学/过程控制龙头 | 美国为核心，全球制造与服务 | KLA、Applied Materials、Onto、Bruker | patterned/unpatterned inspection、overlay、OCD、film、wafer geometry、AI analytics |
| e-beam/CD-SEM | 日本、美国、荷兰/台湾、以色列 | Hitachi High-Tech、ASML/HMI、Applied、KLA、JEOL、Nova | CD-SEM、e-beam review、multi-beam inspection、voltage contrast |
| EUV mask/reticle | 日本、美国、荷兰、德国 | Lasertec、KLA、ASML/HMI、NuFlare、JEOL、Carl Zeiss SMT | EUV mask blank inspection、actinic inspection、reticle registration、mask writer/metrology |
| X-ray/材料量测 | 日本、美国、以色列、欧洲 | Rigaku、KLA、Nova、Bruker、Semilab、Onto | XRF、XRD/XRR、CD-SAXS、3D NAND/DRAM高深宽比结构量测、contamination |
| 先进封装检测量测 | 美国、以色列、韩国、台湾、中国大陆、马来西亚 | KLA、Onto、Camtek、Nova、Koh Young、ViTrox、UnitySC、中科飞测、精测电子 | bump/RDL/TSV、warpage、macro defect、PLP/glass core、6-side package inspection |
| ATE/探针/SLT | 美国、日本、欧洲、台湾、韩国、中国大陆 | Advantest、Teradyne、Cohu、Chroma、FormFactor、Technoprobe、MPI、Keysight、长川科技、华峰测控 | SoC/memory tester、HBM probe、wafer probe card、system-level test、burn-in |
| 国产替代 | 中国大陆 | 中科飞测、上海睿励、精测电子、东方晶源、长川科技、华峰测控、精智达、华海清科相关量测生态 | 明暗场光学检测、膜厚/OCD、overlay、CD-SEM追赶、ATE/存储测试、先进封装AOI |

### 4.2 供给瓶颈

1. **精密光学/激光/探测器**：broadband plasma、DUV laser、high-NA成像、低噪声sensor、高速camera高度依赖少数供应链。
2. **电子光学柱与高速stage**：multi-beam e-beam需要高稳定电子源、beamlet一致性、低串扰、真空、纳米级stage和实时数据处理。
3. **X-ray源、探测器和安全/屏蔽工程**：CD-SAXS/XRR/XRF要同时满足穿透力、分辨率、吞吐和fab级维护。
4. **图像计算硬件**：检测工具需要大量CPU/GPU/FPGA/DRAM/高速存储；AI导致DRAM涨价，直接压设备厂毛利。
5. **算法/recipe/训练数据**：设备性能的一半来自算法、模型、defect library和客户工艺数据；没有数据很难复制。
6. **客户认证周期**：先进节点、HBM、CoWoS工具从evaluation到POR通常6-18个月；一旦进入POR，切换也困难。
7. **现场应用和服务人才**：每台高端工具都需要应用工程师驻场调recipe，人才比机械产能更难短期扩张。
8. **出口管制和地缘风险**：中国先进节点客户对高端光学/e-beam/reticle工具可得性不确定，国产替代受益但高端性能追赶慢。
9. **OSAT工艺升级经验不足**：先进封装线需要前道级洁净度、SPC和失效分析文化，学习曲线会放大工具需求。

### 4.3 成本结构与毛利决定因素

| 成本项 | 高端检测量测工具BOM占比估算 | 决定因素 |
|---|---:|---|
| 光学/e-beam/X-ray核心模块 | 25-45% | 光源、镜头、电子柱、X-ray源/探测器、真空、传感器良率 |
| 精密stage、机电、隔振、环境控制 | 15-25% | 纳米级运动控制、热稳定、洁净、throughput |
| 计算/图像处理/存储/AI硬件 | 10-20% | GPU/FPGA/DRAM/SSD价格；2026 DRAM涨价是毛利逆风 |
| 软件、算法、recipe、ADC模型 | 5-15%会计成本，价值占比更高 | 研发摊销、客户数据、模型精度、false positive控制 |
| fab自动化、EFEM、机器人、vacuum、safety | 8-15% | 晶圆/面板/封装件搬运复杂度 |
| 装配、校准、测试、质保、现场安装 | 10-20% | 调试周期、现场应用工程师、客户验收 |

价格传导机制：

- 先进AI芯片客户更关注time-to-yield，而不是工具单价。若一台工具缩短一个月ramp，价值可能超过工具价格。
- 设备厂通过高ASP系统、软件选件、服务合同、capacity reservation、长期维护提高综合毛利。
- KLA/Onto/Nova等的毛利锚分别约在60%+、55%上下、57%上下；Camtek/先进封装AOI通常低于KLA但高于普通后道设备。
- 下游缺产能时，最稀缺的不是普通AOI，而是“已被客户POR认证且能处理特定HBM/CoWoS缺陷”的系统，溢价能力最强。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | 集中度判断 | 头部公司 |
|---|---|---|
| 前道process control总盘 | 高度集中。KLA口径显示其process control份额约为最近竞争者7倍；模型估计KLA广义份额约50-60% | KLA、Applied、ASML、Hitachi、Onto、Nova |
| 光学patterned inspection | 极高，KLA绝对领先 | KLA、Applied、Onto、Hitachi、少数国产厂 |
| e-beam inspection/review | 高，ASML/HMI、KLA、Applied、Hitachi、JEOL分层竞争 | ASML/HMI、KLA、Applied、Hitachi、JEOL |
| CD-SEM | 高，Hitachi传统强势，Applied/ASML/KLA/JEOL参与 | Hitachi High-Tech、Applied、ASML/HMI、KLA、JEOL |
| Reticle/EUV mask | 极高，Lasertec/KLA/ASML相关生态寡头 | Lasertec、KLA、ASML/HMI、NuFlare、JEOL、Carl Zeiss |
| OCD/overlay/film/material | 中高，按技术分散 | KLA、Onto、Nova、ASML、Applied、Rigaku、Bruker、Semilab |
| 先进封装inspection/metrology | 中高且快速变化 | KLA、Onto、Camtek、Nova、Koh Young、ViTrox、UnitySC |
| ATE/探针卡 | 高，ATE双寡头，探针卡多强并存 | Advantest、Teradyne、Cohu、Chroma、FormFactor、Technoprobe、MPI |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| 分辨率 + 吞吐同时满足 | 单纯看得清没有价值，必须在HVM吞吐下看得清。ASML eScan 1100的25束/15x吞吐就是把e-beam从R&D推向inline的关键。 |
| false positive/false negative控制 | 误报会拖垮产线，漏报会毁良率；设备商的defect library和客户recipe是长期积累。 |
| 与scanner/APC闭环 | overlay/CD/wafer geometry数据会反馈给光刻机和制程工具，切换设备等于重建控制环。 |
| 客户POR认证 | 进入TSMC/Samsung/SK hynix/Micron/Intel/OSAT POR后，生命周期可持续多年；替换需重做qualification。 |
| 高端服务网络 | 工具宕机会影响百万美元级wafer lot和昂贵AI封装，24/7服务和备件本身可收费。 |
| 软件和数据粘性 | ADC、yield analytics、hybrid metrology模型越用越准，客户历史数据越多，切换成本越高。 |
| 供应链和制造know-how | 光学、电子光学、stage、热稳定、震动控制、计算架构要系统集成，无法靠采购清单快速复制。 |

### 5.3 价值捕获

长期高ROIC/高毛利最可能出现在四层：

1. **KLA式前道process control平台**：设备、服务、软件、客户数据全绑定，规模最大、护城河最深。
2. **EUV mask/reticle和multi-beam e-beam**：物理壁垒极高，客户替代少，ASP高。
3. **HBM4/3D封装X-ray/混合量测和hybrid bonding inspection**：2026-2027从小市场变成高端AI封装刚需，增长弹性最大。
4. **高端ATE/探针卡/SLT**：HBM、GPU、ASIC、SerDes测试时间上升，测试设备从后道成本项变成交付瓶颈。

普通后道AOI、成熟节点膜厚/缺陷检测、低端PCB检测会增长，但长期ROIC弱于上述四层。

## 6. 2026关键变化：三个最可能拐点

1. **先进封装检测量测前道化。**  
   KLA把先进封装process-control收入从2025约$635M看向2026约$1B；Onto预计advanced packaging 2026增长>50%；Camtek、Koh Young、ViTrox、Nova也受益。最可能放量方向：HBM bump/TSV/RDL、CoWoS interposer、warpage、2.5D logic package inspection。

2. **HBM4验证把X-ray、e-beam、KGD测试提前拉进订单。**  
   Rubin/MI400/TPU8/OpenAI-Broadcom XPU都指向HBM4，2026H2即使终端出货有限，也会先拉动设备订单。最可能放量方向：X-ray CD/profile、HBM stack inspection、advanced probe card、memory tester、burn-in。

3. **客户从“买工具”转向“抢slot和服务能力”。**  
   2026设备需求不是只看WFE总额，而是看先进工具交付、安装、recipe和服务能力。最可能放量方向：KLA/ASML/Applied/Onto/Nova高端工具、服务合同、软件选件、field application capacity。

## 7. 2027关键变化：三个最可能拐点

1. **Rubin/MI400/TPU8/ASIC进入HBM4时代。**  
   2027核心增量是HBM4 + large package + multi-die + high-speed interconnect，最可能拉动multi-beam e-beam、X-ray hybrid metrology、SoIC/hybrid bonding inspection和SLT。

2. **Panel-level packaging和glass-core从demo走向小批量。**  
   2.5D大封装成本压力会推动PLP和玻璃基板路线。KLA Lumina/Zeta、Onto JetStep/Firefly、Koh Young/ViTrox等会受益，但良率和翘曲控制决定放量速度。

3. **CPO/硅光使检测从“电缺陷”扩展到“光电协同缺陷”。**  
   1.6T/3.2T网络、CPO switch和silicon photonics要求光学、电学、热学、封装可靠性一起测。2027小批，极度乐观下成为新设备池。

## 8. 公司与技术地图

### 8.1 全球头部和细分强者

| 细分 | 公司 |
|---|---|
| 前道process control综合 | KLA、Applied Materials、Onto Innovation、Nova、ASML/HMI、Hitachi High-Tech |
| 光学缺陷检测 | KLA、Applied、Onto、Hitachi High-Tech、SCREEN、Camtek、国产中科飞测/精测电子/东方晶源等 |
| e-beam inspection/review/CD-SEM | ASML/HMI、KLA、Applied、Hitachi High-Tech、JEOL、Thermo Fisher/FEI实验室分析生态 |
| overlay/OCD/film/wafer geometry | KLA、ASML YieldStar、Onto、Nova、Applied、Bruker、Semilab、Rigaku |
| X-ray / materials / CD-SAXS / XRF / XRD/XRR | Rigaku、KLA、Nova、Onto、Bruker、Semilab、Park Systems、Oxford Instruments |
| Reticle/mask | Lasertec、KLA、ASML/HMI、NuFlare、JEOL、Carl Zeiss SMT、Nikon/Canon相关生态 |
| 先进封装/2.5D/3D/HBM检测 | KLA、Onto、Camtek、Nova、Koh Young、ViTrox、UnitySC、SUSS MicroTec、EVG、ASMPT、Besi相邻 |
| IC substrate/PCB/PLP | KLA Orbotech/Lumina、Koh Young、ViTrox、Camtek、Onto、Orbotech生态、台湾/韩国AOI厂 |
| ATE | Advantest、Teradyne、Cohu、Chroma、SPEA、Keysight、National Instruments/Emerson、长川科技、华峰测控 |
| 探针卡/prober | FormFactor、Technoprobe、MPI、Japan Electronic Materials、Micronics Japan、Wentworth、Tokyo Electron/Accretech prober生态 |
| 软件/yield analytics | KLA 5D Analyzer/ICON、Onto software、Applied、ASML、PDF Solutions、Siemens、Synopsys、Cadence、Keysight |

### 8.2 中国大陆公司

国产替代的最强逻辑不在“全面替代KLA”，而在三条线：

1. 成熟节点和特色工艺检测量测国产替代：中科飞测、精测电子、上海睿励、东方晶源等。
2. 后道/先进封装AOI、存储测试、模组测试、探针/ATE：长川科技、华峰测控、精智达、联动科技、华兴源创等。
3. 国产AI芯片低良率环境下的“以更多检测换良率”：若华为、寒武纪、阿里、壁仞等国产AI链条上量，本土检测/ATE会获得比传统消费电子更强的战略采购支持。

风险是高端光学、e-beam、reticle、CD-SEM、X-ray高吞吐、算法数据和客户POR仍需要多年追赶。

## 9. 投资价值排序

| 排名 | 子方向 | 投资价值 | 主要风险 |
|---:|---|---|---|
| 1 | KLA式前道process control | 最大、最稳、最强定价权，AI/HBM/GAA/advanced packaging全受益 | 估值高、出口管制、光学/e-beam供应链 |
| 2 | HBM/先进封装检测量测 | 2026-2027最高弹性，Onto/Camtek/Nova/KLA/Koh Young/ViTrox均受益 | CoWoS/HBM4延期、客户集中、工具竞争加剧 |
| 3 | X-ray/混合量测 | HBM4/GAA/3D结构刚需，Onto-Rigaku、KLA、Nova等受益 | 吞吐、recipe、客户导入慢 |
| 4 | Multi-beam e-beam | 3nm/2nm/DRAM关键层高壁垒，ASML/HMI、KLA、Applied受益 | 价格高、throughput和可靠性验证 |
| 5 | ATE/探针/SLT | SEMI预计测试设备继续增长，AI芯片测试时间和复杂度上升 | ATE周期性、客户砍单、测试并行效率改善 |
| 6 | 国产替代 | 中国AI芯片和成熟节点扩产给长周期机会 | 高端追赶难、出口管制双刃剑、客户验证慢 |

## 10. 主要风险和观察指标

| 风险/指标 | 需要跟踪什么 |
|---|---|
| AI capex回落 | hyperscaler capex、GB300/Rubin/MI400/TPU/Trainium订单、CoWoS/HBM排产 |
| HBM4延期 | SK hynix/Samsung/Micron资格验证、HBM4良率、base die供应、tester/probe订单 |
| CoWoS/advanced packaging产能释放慢 | TSMC/OSAT capex、ASE/Amkor/JCET外包比例、KLA/Onto/Camtek advanced packaging订单 |
| 工具交付瓶颈 | KLA/Onto/Nova/Camtek backlog、lead time、毛利中DRAM/物流/关税影响 |
| 出口管制 | 美国BIS规则、KLA/Applied/ASML中国收入、国产替代订单 |
| 客户良率数据 | TSMC/Samsung/Intel/SK hynix/Micron的ramp commentary，AI package yield传闻与设备pull-in |

## 11. 资料来源

| 来源 | 关键信息 |
|---|---|
| [Gartner 2026全球半导体收入预测](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | 2026半导体收入$1.320T、2027 $1.555T、AI半导体约30%、DRAM价格+125%。 |
| [SEMI 2025-2027设备销售预测](https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports) | 半导体制造设备2025 $133B、2026 $145B、2027 $156B；测试和A&P继续增长。 |
| [KLA FY2026 Q3结果](https://ir.kla.com/news-events/press-releases/detail/514/kla-corporation-reports-fiscal-2026-third-quarter-results) | Q3收入$3.415B、SPC $3.084B、Q4收入指引$3.575B、AI生态受益。 |
| [KLA Investor Day 2026](https://ir.kla.com/news-events/investor-day-2026) | Process Control for the AI Era、2030模型、先进封装和服务战略。 |
| [KLA Metrology产品页](https://www.spts.com/products/chip-manufacturing/metrology) | Archer、SpectraShape、Axion、PWG等overlay/OCD/X-ray/wafer geometry产品。 |
| [KLA IC substrate/PLP检测量测](https://www.spts.com/products/pcb-ic-substrate-manufacturing/inspection-metrology) | Lumina、ICOS、Zeta面向advanced IC substrate、glass core、PLP。 |
| [Onto 2026 Q1结果](https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Reports-2026-First-Quarter-Results/default.aspx) | Q1收入$291.9M、Q2指引$320-330M、Dragonfly G5/Atlas G6/Rigaku投资。 |
| [Onto Dragonfly G5 HBM4发布](https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Launches-Dragonfly-G5-Inspection-System/default.aspx) | HBM厂商为HBM4 ramp选择Dragonfly G5；G5+3Di双位数订单，2026Q2发货。 |
| [Onto Dragonfly G5 2.5D AI Packaging资格](https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovations-Dragonfly-G5-System-Qualified-for-Applications-in-2-5D-AI-Packaging/default.aspx) | 2.5D AI封装客户qualification，Dragonfly平台2026增长>50%。 |
| [Nova Q4/FY2025结果PDF](https://www.novami.com/wp-content/uploads/2026/02/nova-pr-q4-2025-february-12-2026.pdf) | 2025收入$880.6M、同比+31%，GAA/DRAM/AP记录表现。 |
| [Camtek Q4/FY2025结果PDF](https://www.camtek.com/wp-content/uploads/Camtek-Q425_FY2025.pdf) | 高端inspection/metrology，覆盖AP、HBM、heterogeneous integration等。 |
| [ASML HMI eScan 1100](https://www.asml.com/en/products/metrology-and-inspection-systems/hmi-escan-1100) | 3nm及以后、25束multi-beam、相对单束最高15x吞吐。 |
| [Applied Materials AI芯片制造新品](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-next-gen-chipmaking-products/) | GAA、HBM、advanced packaging与3D结构量测挑战；eBeam high-throughput imaging。 |
| [SEMICON Korea 2026先进封装过程控制论坛](https://www.semiconkorea.org/en/node/13566) | 传统封装MI不足，advanced packaging需要前道级metrology/inspection。 |
| [Rigaku SEMICON Korea 2026](https://rigaku.com/resources/events/semicon-korea-2026) | X-ray metrology支持AI memory、HBM和advanced packaging。 |
| 项目内`ai_chip_research_2026_2027.md` | 2026-2027 AI芯片出货与技术路径锚：GB300、Trainium2、Ironwood、MI350、Rubin、MI400、TPU8等。 |

# 行业调研：【半导体设备子系统与真空/RF/流体模块】

> 截至日期：2026-05-08  
> 研究口径：本文研究对象不是整机 WFE，而是安装在刻蚀、CVD/ALD/PVD、EUV/DUV、离子注入、清洗、CMP、电镀、先进封装和测试/老化设备里的关键子系统：真空泵/阀/规/泄漏检测、RF/微波/脉冲 DC plasma power、MFC/气体柜/液体前驱体 vapor delivery、化学液输送与过滤、UHP 阀件管件、温控/chiller、尾气处理、精密机加/清洗/涂层和模块集成。  
> 情景标记：`B/O/X` = 基准/乐观/极度超预期乐观。本文按用户要求，对 2026-2027 AI 计算中心建设采用非常乐观假设；找不到直接披露的细分数字时，用 WFE、300mm fab、公司订单、产品 attach rate 和 BOM 占比交叉推导。

## 0. 高浓度结论

### 0.1 一句话判断

2026 年这个行业的投资价值在于：AI 芯片产能扩张已经从“买整机设备”传导到“设备里的设备”。真空、RF、MFC、UHP 流体、化学输送、过滤、温控和尾气处理过去常被当成二级供应链，但在 2nm/GAA、HBM3E/HBM4、CoWoS/混合键合、先进 DRAM/NAND 高深宽比刻蚀中，它们直接决定良率、throughput、颗粒污染、能耗和工具 uptime。  

最强价值捕获层不是低毛利模块代工，而是 **高端真空阀/压力控制、RF plasma power、先进 MFC/气液输送、污染控制/过滤、泵+abatement 服务**。这些环节“单价不如整机大”，但客户切换成本极高，认证周期长，失效一次就是整批晶圆报废，因此在 AI/HBM 扩产期有比传统周期更强的定价权。

### 0.2 公开锚点

| 来源/时间 | 关键数字/事实 | 对本行业含义 |
|---|---:|---|
| SEMI，2026-04-01 | 300mm fab equipment spending 预计 2026 年 +18% 至 $133B，2027 年 +14% 至 $151B；2028 年 $155B，2029 年 $172B。 | 子系统需求的最大上游锚。真空/RF/流体模块通常随新 WFE、tool upgrade、spares/service 同步增长。 |
| SEMI，2025-12 | 全球半导体制造设备销售预计 2025 年 $133B，2026 年 $145B，2027 年 $156B。 | 用于校验本文对“设备子系统”收入池的上限。 |
| Gartner，2026-04 | 全球半导体收入预计 2026 年 $1.320T，2027 年 $1.555T；AI 半导体约占 2026 总量 30%；hyperscaler AI infra spending 2026 年 +50%+。 | AI 不只是短期 GPU 单点需求，而是推动先进逻辑、HBM、NAND、先进封装同时扩产。 |
| ASML，2026Q1 | Q1 销售 EUR 8.8B、毛利率 53.0%；2026 全年收入指引 EUR 36-40B；Q2 指引 EUR 8.4-9.0B。 | Lithography 工具交付和 installed-base upgrade 继续支撑真空、温控、传感、洁净子系统需求。 |
| MKS，2026Q1 | 收入 $1.078B，调整后 EBITDA $277M；管理层称需求由 AI 相关投资推动，半导体和先进电路板制造复杂度快速上升。 | MKS 横跨真空、压力/流量、RF power、specialty chemicals，是本行业最直接的一手温度计之一。 |
| VAT，2026Q1 | 订单 CHF 356M，同比 +47%，book-to-bill 1.6；半导体订单环比 +38%；Q2 销售指引 CHF 265-295M。 | 高端真空阀从 2025 恢复转向 2026 明显加速，且已有供给/物流扰动。 |
| Atlas Copco Vacuum Technique，2026Q1 | 订单 SEK 11.053B，同比 +17%，organic +32%；收入 SEK 9.066B；营业利润率 20.5%；半导体/FPD 真空设备需求显著增长。 | Edwards/Leybold 等真空泵、service、abatement 链条已进入订单上行。 |
| Ichor，2026Q1 | 收入 $256.1M，Q2 指引 $290-310M；公司定义其核心产品为 gas/chemical delivery subsystems。 | 气液输送模块开始反映 WFE 上行，Q2 指引环比明显提高。 |
| Ultra Clean，2026Q1 | 收入 $533.7M，Q2 指引 $565-605M；管理层称处于 multi-year AI driven expansion 早期。 | 子系统代工、精密清洗、parts services 正在从早周期恢复进入扩张。 |
| Entegris，2026Q1 | 收入 $811.9M；Advanced Purity Solutions 销售 $463.6M、segment profit $133.6M；总 GAAP gross margin 约 46.9%。 | 高纯过滤、污染控制、化学品和流体部件是高毛利价值层。 |
| INFICON，2026Q1 | 销售 $181.0M，同比 +14.4%；Semiconductor & Vacuum Coating $95.0M，同比 +23.5%；2026 指引上调至 $710-750M。 | 真空规、泄漏检测、传感与智能制造软件随设备上行和 uptime 需求放大。 |
| Advanced Energy，2026Q1 | 总收入 $511.0M；Semiconductor Equipment $219.4M；Data Center Computing $194.2M；non-GAAP gross margin 40.1%。 | RF/plasma power 和系统电源同时受益：一头在晶圆厂，一头在 AI 数据中心。 |
| Comet，2026Q1/年报 | Q1 订单 CHF 144.9M，同比 +22.3%，book-to-bill 1.4；公司称 GAA、HBM、先进 DRAM 提升 tool intensity，利好 RF generators、matching networks、vacuum capacitors。 | RF matching 和真空电容是小而硬的高壁垒环节。 |

## 1. AI 计算中心大规模建设下的 2026 机遇、挑战与技术路径

### 1.1 需求传导链条

```text
AI 计算中心 CapEx
  -> GPU/ASIC/HBM/网络/存储需求
  -> TSMC/Samsung/Intel/SMIC 先进逻辑 + SK hynix/Samsung/Micron HBM/DRAM + NAND 扩产
  -> EUV/DUV、刻蚀、沉积、清洗、CMP、先进封装、测试设备采购
  -> 真空泵/阀/规、RF power、MFC/气体柜、化学液输送、UHP 管阀件、过滤、温控、尾气处理、精密清洗/涂层
```

2026 年最强的不是单一工具，而是 **刻蚀/沉积/清洗/封装每一步的“受控环境复杂度”上升**：

- GAA/nanosheet 和 2nm 节点需要更多 ALD、选择性沉积、低损伤刻蚀、molybdenum contact、背面供电准备，对 RF、MFC、真空和温控稳定性要求上升。
- HBM3E/HBM4 需要先进 DRAM、电镀、TSV、hybrid bonding、wafer thinning、clean、package test，拉动化学液输送、过滤、真空和等离子清洁。
- CoWoS/SoIC/InFO/混合键合把“前道级洁净控制”延伸到后道，过去 OSAT 可接受的污染和温控窗口不够用了。
- NAND/DRAM 高深宽比结构推高 cryo etch、pulsed RF、fast match、低温 chiller、dry pump 与 abatement 配套需求。

### 1.2 与 2026-2027 出货量最大的 AI 芯片路径映射

项目既有报告已经给出 2026-2027 年初出货/价值权重最大的 AI 平台：GB300/B300、Trainium2/3、TPU Ironwood/TPU8、GB200/B200、Rubin、MI350/MI400、Meta MTIA、Microsoft Maia、OpenAI/Broadcom ASIC、Huawei Ascend/Cambricon 等。本文只使用这些既有结论，不重新外部搜索排序。

| 芯片/平台 | 制程/封装方向 | 对真空/RF/流体模块的拉动 | 2026-2027 节奏 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | TSMC 4NP、HBM3E、CoWoS-L/S、NVL72 液冷 rack | 4NP 逻辑、HBM3E DRAM、CoWoS/RDL/ABF、HBM KGD/test 同时拉动；2026 最确定。 | 2026 全年主线，2027 H1 仍强。 |
| AWS Trainium2/3 | Trainium2 大规模；Trainium3 3nm/HBM3E/144-chip UltraServer | Broadcom/Annapurna/代工供应链扩大非 NVIDIA ASIC 产能池；HBM 和 3nm 增加工艺复杂度。 | Trainium2 2026 大量，Trainium3 2026 H2-2027 接棒。 |
| Google TPU Ironwood/TPU8 | TPU v7 Ironwood HBM；TPU8 训练/推理分化 | TSMC/Broadcom 路径，先进逻辑、HBM、2.5D packaging、先进测试需求扩张。 | Ironwood 2026，TPU8 2026 H2 NPI、2027 放量。 |
| AMD MI350/MI400 | MI350 HBM3E；MI400/Helios HBM4、open rack | MI350 是 2026 确定需求，MI400 将在 2027 加速 HBM4、CoWoS-L、封装测试和供电/冷却。 | MI350 2026，MI400 2026 H2 样品/早期，2027 主力。 |
| NVIDIA Rubin/Vera Rubin | HBM4、更多 chiplet、先进封装、CPO/硅光路线准备 | 2026 贡献 NPI 设备和预订，2027 对 HBM4、RF/etch/ALD/packaging 设备拉动更强。 | 2026 H2 early，2027 放量。 |
| Meta MTIA / Microsoft Maia / OpenAI-Broadcom ASIC | TSMC 3nm/先进封装/HBM3E 或后续 HBM4 | 自研 ASIC 让 AI 产能需求不再只围绕 NVIDIA；代工、HBM、气液/真空/RF 工具利用率更高。 | 2026 导入，2027 形成第二增长曲线。 |
| Ascend/Cambricon/国产 AI | DUV 多重曝光、国产封装、国产 HBM/高速互连 | 中国本土设备子系统国产化加速；MFC、真空泵、RF power、气体柜、尾气处理国产替代弹性最大。 | 2026 替代需求强，2027 工艺能力决定上限。 |

### 1.3 新技术成熟和放量时间

| 技术路径 | 基准情景 | 乐观情景 | 极度超预期乐观情景 | 2026 投资结论 |
|---|---|---|---|---|
| GAA/N2/N2P 相关 ALD、低损伤 etch、moly contact | 2026 H2 NPI/初量，2027 放量 | 2026 H2 多客户导入，2027 全年高增长 | 2026 Q4 即出现明显设备追加单 | RF、MFC、ALD valve、温控、真空阀优先受益。 |
| A16/背面供电 BSPDN | 2027 pilot，2028 规模化 | 2027 H2 开始贡献设备收入 | 2027 H1 提前拉动关键子系统备货 | 2026 主要是技术储备，不是收入主力。 |
| HBM4 相关 DRAM/TSV/TCB/hybrid bonding | 2026 验证，2027 放量 | 2026 H2 小批量，2027 H1 明显放量 | 2026 H2 关键客户提前拉货 | 2026 设备订单和 NPI 最强，2027 收入弹性最大。 |
| CoWoS-L/RDL/SoIC/hybrid bonding | 2026 已放量，2027 加速 | 2026 H2 成为主力新增方向 | 2026 全年供不应求、OSAT 外溢 | 化学液输送、过滤、plasma activation、真空搬运需求上行。 |
| 高深宽比 NAND/DRAM cryo etch | 2026 选择性采用，2027 扩大 | 2026 H2 扩大到更多客户 | 2026 即形成温控/真空/RF 紧缺 | 低温 chiller、dry pump、RF match 是关键配套。 |
| 低 GWP/高效率 abatement | 2026 工艺线标配升级，2027 加速 | 2026 就出现 green fab 订单 | 监管/客户 ESG 使设备强制升级 | 泵+尾气一体化和 service 合同价值上升。 |
| CPO/硅光进入 CoWoS | 2026-2027 NPI，2028 后大规模 | 2027 小批量 | 2026 H2 高端客户提前导入 | 对真空沉积、刻蚀、光子封装清洗/贴装有期权。 |

### 1.4 2026 最可能的技术路径

2026 最可能放量的不是最科幻路线，而是以下五条：

1. **HBM3E/HBM4 准备线 + 先进 DRAM 工具链**：HBM3E 仍是大货，HBM4 是订单弹性；拉动刻蚀、沉积、电镀、清洗、测试、pump/abatement。
2. **CoWoS-L/RDL/SoIC/hybrid bonding**：2.5D/3D packaging 从封装产能瓶颈变成前道级洁净制造；流体/化学/过滤/真空模块价值上移。
3. **GAA/N2/N2P 设备 NPI**：Applied 2026 发布的 GAA/2nm 新系统指向 atomic-level surface treatment、angstrom-level conductor etch、moly ALD contact；这些都需要更复杂 RF、MFC、真空和温控。
4. **pulsed RF + fast match + multi-zone plasma control**：高深宽比和低损伤窗口变窄，传统 RF generator/match 被更高频、更快响应、更强数字控制替代。
5. **dry pump + integrated abatement + uptime service**：AI fabs 不能容忍非计划停机，泵、尾气、泄漏检测和预测维护会从一次性 CAPEX 变成长期服务收入。

## 2. 已经开始放量的关键产品：市场规模、渗透率和利润率

说明：下表是全球收入池估算，未来 3 个月指 2026Q2-Q3 可确认/可交付收入，1 年指 2026-05 至 2027-05，2 年指 2026-05 至 2028-05。各行存在 BOM 重叠，例如 gas box 中的 MFC、UHP valve、管件和子系统集成不能简单相加；本文在总盘子处做了剔重。

### 2.1 总盘子

| 口径 | 未来3个月 B/O/X | 未来1年 B/O/X | 未来2年 B/O/X | 核心假设 |
|---|---:|---:|---:|---|
| 真空/RF/流体/温控/尾气/洁净子系统剔重总收入池 | $6.5-10B / $9-13B / $12-18B | $27-40B / $36-52B / $50-72B | $64-92B / $90-132B / $132-190B | 约占 WFE+先进封装/测试设备相关子系统与服务的 16-24%；极超情景假设 HBM4、CoWoS、N2 和国产替代同时加速。 |
| 与 AI/HBM/先进逻辑直接相关部分 | $3.5-5.5B / $5-8B / $7-12B | $15-23B / $22-34B / $32-48B | $36-55B / $54-82B / $82-125B | 2026 AI/HBM/先进逻辑占比约 50-60%，2028 提高到 60-70%。 |

### 2.2 产品拆分

| 已放量产品 | 当前事实基础 | 未来3个月市场规模 B/O/X | 未来1年市场规模 B/O/X | 未来2年市场规模 B/O/X | 渗透率路径 | 增长预测 | 毛利/利润率 B/O/X |
|---|---|---:|---:|---:|---|---|---|
| Dry vacuum pump、booster、turbopump、pump service、abatement | Atlas Vacuum Q1 订单 organic +32%；半导体真空需求显著增长；Ebara/Edwards/ULVAC/Kashiyama 受益。 | $1.0-1.5B / $1.4-2.1B / $2.0-3.0B | $4.5-6.5B / $6-8.5B / $8.5-12B | $10-15B / $15-22B / $22-34B | 先进 etch/CVD/ALD/implant/EUV attach 近 100%；HBM/DRAM/NAND 工具强度 2026-2028 +20-45%。 | 2026 +15-30%，2027 +25-45%；极超 +60%+。 | 毛利 35-48% / 42-55% / 50-62%；service/abatement retrofit 更高。 |
| Vacuum valves、APC pressure control、gate valves、vacuum gauges、leak detection | VAT Q1 book-to-bill 1.6；半导体订单环比 +38%；INFICON 半导体/真空镀膜收入 +23.5%。 | $0.5-0.8B / $0.75-1.1B / $1.0-1.6B | $2.0-3.2B / $3.0-4.7B / $4.5-7.0B | $5-8B / $8-13B / $13-20B | 每个真空 chamber 必配，先进节点对 repeatability、颗粒、cycle life 要求提高；VAT 半导体真空阀长期高份额。 | 2026 +20-40%，2027 +25-50%。 | 高端阀/规毛利 45-60% / 50-65% / 55-70%；系统件低一些。 |
| RF generator、match network、pulsed DC、microwave/remote plasma、vacuum capacitor | AE 半导体收入 $219.4M；Comet 称 GAA/HBM/advanced DRAM 提升 RF generator/match/vacuum capacitor tool intensity；MKS RF/remote plasma 强。 | $0.6-1.0B / $0.9-1.4B / $1.3-2.0B | $2.8-4.2B / $4-6B / $6-9B | $7-11B / $11-17B / $17-26B | Etch/PECVD/ALD/plasma clean attach 70-95%；多频、脉冲、fast match 渗透率从 2026 约 20-30% 升至 2028 35-55%。 | 2026 +18-35%，2027 +30-55%；极超 +70%。 | 毛利 40-52% / 45-58% / 50-65%；真空电容和高端 match 定价强。 |
| MFC、digital gas box、liquid precursor vaporizer、gas panel | 半导体 MFC 2026 市场约 $1.2B；gas delivery system 2026 约 $1.64B；HORIBA、MKS、Fujikin、Brooks、Ichor 受益。 | $1.0-1.6B / $1.4-2.2B / $2.0-3.2B | $4.5-6.8B / $6.5-9.5B / $9-14B | $10-16B / $16-24B / $24-36B | 先进沉积/刻蚀/清洗气体通道数上升；digital MFC 和低 vapor pressure precursor delivery 渗透率从 2026 25-35% 升至 2028 45-65%。 | 2026 +12-28%，2027 +20-40%；极超 +55%。 | MFC/阀件毛利 35-55%，gas box 集成 12-24%；紧缺时组件毛利上沿提高。 |
| Chemical delivery、slurry/clean/electroplating delivery、purification/filtration | Entegris APS Q1 $463.6M；Ichor 化学输送用于 CMP、电镀、clean；HBM/advanced packaging 需要更多湿法和过滤。 | $1.0-1.6B / $1.5-2.4B / $2.2-3.4B | $4.2-6.5B / $6-9.5B / $9-14B | $9-15B / $15-24B / $24-36B | 高纯过滤在 advanced logic/HBM/CoWoS 中接近刚需；先进封装湿法洁净 attach 由 2026 45-55% 升至 2028 65-80%。 | 2026 +15-35%，2027 +25-50%。 | Entegris 型材料/过滤毛利 45-60%；系统集成 15-30%；极超 55-65%。 |
| UHP valves/fittings/tubing、VMB/VMP、regulators | 多个市场报告给出 2026 半导体阀件/管件约 $3.3-4.3B；Swagelok、Fujikin、Parker、Entegris、KITZ SCT、CKD 领先。 | $0.8-1.3B / $1.2-1.8B / $1.6-2.7B | $3.3-5.2B / $5-7.5B / $7.5-11B | $8-13B / $13-20B / $20-30B | Fab/工具连接密度上升；welded UHP connection 在关键气体/化学路线占比 40%+；新 fab 扩建直接拉动。 | 2026 +8-20%，2027 +12-28%；极超 +40%。 | 毛利 30-50%；特殊合金、FFKM、快速交付产品 50%+。 |
| Chiller、wafer temperature control、heat exchanger、thermal sensors | Cryo etch、EUV、PECVD/ALD、implant 和先进封装均需要更窄温控窗口；SMC、Shinwa、ATS、Mydax、Daikin 等受益。 | $0.5-0.9B / $0.8-1.2B / $1.1-1.8B | $2.2-3.5B / $3.2-5B / $5-8B | $5-8B / $8-13B / $13-20B | 先进 etch/deposition 温控 attach 接近 100%；cryo/多区温控渗透率从 2026 10-15% 升至 2028 25-40%。 | 2026 +10-25%，2027 +20-45%。 | 毛利 25-45%；高端低温/快速响应系统 40-55%。 |
| Subassembly build-to-print、precision machining、weldment、parts cleaning/coating | UCT Q1 $533.7M，Q2 指引 $565-605M；Ichor Q2 指引 $290-310M；Ferrotec、Foxsemicon、KoMiCo 等受益。 | $1.5-2.4B / $2.2-3.5B / $3.2-5B | $6-9B / $9-14B / $14-22B | $14-22B / $22-34B / $34-52B | OEM 外包率继续上升；NPI 复杂度提高；critical chamber cleaning/coating attach 随 uptime 服务增长。 | 2026 +15-30%，2027 +25-45%；极超 +60%。 | 模块代工毛利 12-25%；清洗/涂层/服务 25-45%；短缺期改善 300-600bp。 |

## 3. 在研和将快速增长的关键产品/细分技术

| 在研/早期放量方向 | 技术含义 | 成熟/放量时间 | 未来3个月市场 B/O/X | 未来1年市场 B/O/X | 未来2年市场 B/O/X | 渗透率路径 | 毛利率/利润率判断 |
|---|---|---|---:|---:|---:|---|---|
| Multi-frequency pulsed RF、VHF RF、fast digital matching、plasma sensor feedback | 高深宽比刻蚀、GAA/nanosheet、低损伤 plasma 需要更窄工艺窗口和毫秒级匹配。 | 2026 NPI/高端工具，2027 扩大 | $0.15-0.3B / $0.25-0.5B / $0.5-0.9B | $0.8-1.5B / $1.5-2.5B / $2.5-4B | $2-4B / $4-7B / $7-12B | 高端 etch/deposition 2026 5-10%，2028 20-40%。 | 45-65%；先进入 OEM 的供应商有高 ASP。 |
| Remote plasma/microwave radicals、low-damage chamber clean、plasma ALD | 降低薄膜损伤和 chamber downtime，用于先进逻辑、DRAM、HBM 和 clean。 | 2026 已放量，2027 加速 | $0.3-0.6B / $0.5-0.9B / $0.8-1.3B | $1.5-2.8B / $2.5-4.5B / $4-7B | $4-7B / $7-12B / $12-20B | Leading-edge deposition/clean 2026 15-25%，2028 35-55%。 | 40-60%；RF/微波源、MFC、特殊阀件共同受益。 |
| Cryogenic etch 配套真空、低温 chiller、低温密封材料 | 用低温提高 etch selectivity 和 HAR profile control，尤其 3D NAND/DRAM。 | 2026 客户选择性采用，2027 更大范围 | <$0.2B / $0.2-0.4B / $0.4-0.7B | $0.5-1.2B / $1.0-2.0B / $1.8-3.5B | $2-4B / $4-7B / $7-12B | 先进 NAND/HBM/DRAM etch 2026 5-10%，2028 20-35%。 | 35-55%；低温可靠性认证是核心壁垒。 |
| Hybrid bonding/plasma activation/wafer-level packaging fluid modules | HBM4、SoIC、CoWoS、chiplet 需要更洁净的 plasma activation、清洗、电镀、RDL 化学输送。 | 2026 已开始，2027 主升浪 | $0.5-0.9B / $0.8-1.4B / $1.2-2.2B | $2.5-4.5B / $4-7B / $7-11B | $6-11B / $11-19B / $19-32B | 先进封装产线 2026 30-45%，2028 55-75%。 | 35-60%；过滤/污染控制和特殊化学输送毛利最高。 |
| Low-GWP/PFAS/GHG high-efficiency abatement、pump-abatement integrated skid | Fab 可持续性和法规压力提升，PFC/NF3/CF4/CH4/F-gas 处理升级。 | 2026 工具升级，2027 新 fab 标配 | $0.3-0.6B / $0.5-0.9B / $0.8-1.3B | $1.5-3B / $2.5-4.5B / $4-7B | $4-8B / $8-13B / $13-22B | 新 advanced fab 2026 40-55%，2028 65-85%。 | 30-50%；service/consumables 提供持续利润。 |
| Smart vacuum/智能传感、leak detection automation、tool digital twin、predictive maintenance | AI fabs 看重 uptime，传感器从安全监控变成良率/维护数据入口。 | 2026 软件+硬件打包，2027 放量 | $0.15-0.35B / $0.25-0.5B / $0.4-0.8B | $0.8-1.5B / $1.3-2.5B / $2.2-4B | $2-4B / $4-7B / $7-12B | 高端工具 attach 2026 10-20%，2028 30-50%。 | 硬件 35-50%，软件/服务 60%+。 |
| ALD liquid precursor vaporizer、zero-dead-volume valve、high-speed purge gas manifold | 2nm/GAA/high-k/metal gate 和低 vapor pressure precursor 需要更稳定输送和更低污染。 | 2026 NPI，2027 扩大 | $0.2-0.5B / $0.4-0.8B / $0.7-1.2B | $1.0-2.0B / $1.8-3.5B / $3-5.5B | $3-6B / $6-10B / $10-16B | ALD/advanced CVD 2026 20-30%，2028 40-60%。 | 40-60%；客户验证后粘性极强。 |

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要产能/公司/地区 | 结构判断 |
|---|---|---|
| Dry pump、turbopump、abatement | Edwards/Atlas Copco：英国、捷克、美国、韩国、中国等；Ebara：日本/亚洲；ULVAC、Kashiyama、Pfeiffer/Busch/Leybold、Agilent、Shimadzu、Hanbell、KYKY。 | 高端先进制程仍由 Edwards/Ebara/ULVAC/Kashiyama 等主导；中国在成熟节点和本土 fab 供应链加速替代。 |
| Vacuum valves/APC/gauges | VAT 瑞士/马来西亚/罗马尼亚等；MKS/Granville-Phillips、INFICON、Pfeiffer、SMC、CKD、Fujikin、KITZ SCT。 | VAT 在半导体高端真空阀长期高份额；压力控制和真空规由 MKS/INFICON/Pfeiffer 等分割。 |
| RF/plasma power | Advanced Energy 美国/亚洲/墨西哥/泰国扩产；MKS ENI/Alter；Comet 瑞士/马来西亚；DAIHEN、TRUMPF Huettinger、Kyosan、ADTEC Plasma、XP Power、新电元/日本供应商；中国英杰电气等。 | 高端 RF generator/match 认证非常深，先发供应商难替换；亚洲产能扩张更多承担量产和成本优化。 |
| MFC/gas delivery | HORIBA STEC 日本；MKS、Brooks Instrument、Fujikin、Azbil、Bronkhorst、Parker、SMC、CKD、Ichor、UCT；中国七星/北方华创体系、正帆科技、至纯科技等。 | MFC 核心传感、阀芯、校准和气体模型是壁垒；gas box 集成可外包但客户认证长。 |
| Chemical delivery/filtration | Entegris、Ichor、UCT、Kinetics、Mega Fluid Systems、MKS、Pall/Danaher、Parker、Saint-Gobain、Nippon Pillar、GEMU；中国正帆、至纯、盛剑环境等。 | 高纯过滤/耗材毛利最高；系统集成受工程交付和客户集中度影响。 |
| UHP valves/fittings/tubing | Swagelok、Fujikin/Carten、Parker Veriflo/Tescom、Entegris、KITZ SCT、CKD、SMC、Ham-Let、Hy-Lok、DK-Lok、Valex、Dockweiler、Fitok。 | 材料洁净度、内表面粗糙度、电解抛光、焊接认证决定份额；welded systems 增长快。 |
| 温控/chiller | SMC、Shinwa Controls、Daikin、ATS/Mydax、Ferrotec、Boyd/Lytron、LAUDA、Julabo、Kanto/日本供应商；中国同飞股份等。 | 高端低温和多区稳定性比普通工业 chiller 壁垒高得多。 |
| 精密机加/清洗/涂层/模块代工 | UCT、Ichor、Ferrotec、Foxsemicon、KoMiCo、CoorsTek、Kyocera、Morgan Advanced Materials、Sanmina、Jabil、Benchmark、VAT/子公司。 | 毛利低于核心部件，但产能和客户工程协同决定 ramp 能力。 |

### 4.2 供给瓶颈

1. **OEM 认证周期**：关键子系统通常要随 Applied、Lam、TEL、ASML、KLA、ASM 等整机平台验证，NPI 到 HVM 可能 12-36 个月；新进入者很难因短期缺货立刻切入。
2. **高纯材料和洁净制造**：316L/高镍合金、electropolished tubing、VCR/VCO 面密封、PFA/PTFE/PVDF、FFKM seals、ceramic、SiC coating、特殊铝合金表面处理都可能成为短缺点。
3. **精密机加工与焊接**：真空 chamber、gas box manifold、weldment、rotor、valve body 对颗粒、泄漏、表面粗糙度和尺寸稳定性要求极高，产能扩张不能简单外包。
4. **RF 关键件**：高功率 RF 半导体、真空电容、磁性件、冷却结构、快速匹配算法、EMI/EMC 测试能力都限制高端 RF generator/match 扩产。
5. **MFC 校准和气体数据库**：corrosive/toxic/low vapor pressure gas 的标定、安全、材料兼容和长期 drift 数据是隐性壁垒。
6. **泵+abatement 现场服务人才**：先进 fab uptime 要求 24/7，field service、spares、remote monitoring 比一次性交付更稀缺。
7. **出口管制和本地化要求**：中国高端设备子系统替代加速，但先进零部件、软件、传感器和材料仍有断点。
8. **物流与地缘扰动**：VAT 2026Q1 已提到中东冲突造成供应链/物流影响，导致销售确认被延后；高端子系统交付缓冲库存会上升。

### 4.3 成本与毛利决定因素

| 产品 | 典型 BOM/单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| Dry pump/abatement | 精密转子/铸件/机加 25-35%；电机/轴承/控制 20-25%；密封/涂层 10-15%；装配测试 20%；保修服务 5-10%。 | 可靠性、mean time between service、腐蚀气体适配、energy efficiency、service 网络。 | 整机 OEM 和 fab 通过 long-term agreement 锁量；短缺时可涨价或提高服务包价值。 |
| Vacuum valve/APC | 高纯金属 body/plate 25-35%；actuator/控制 15-25%；seal/coating 10-20%；洁净装配/particle test 20-30%。 | 颗粒、cycle life、leak rate、pressure stability、客户工具平台认证。 | VAT 型龙头可按性能/交期定价；客户为避免 requalification 接受 price increase。 |
| RF generator/match | 功率半导体/电源 25-40%；真空电容/匹配网络 15-25%；冷却/机箱 10-15%；控制软件 10-15%；测试校准 15-20%。 | 响应速度、稳定性、wafer uniformity、plasma repeatability、算法/IP。 | 先进制程良率收益远大于部件价差，供应商可价值定价。 |
| MFC/gas box | MFC/阀/调压器 45-60%；管件/焊接 15-20%；控制电气 10-15%；洁净装配/泄漏测试 15-25%。 | 气体模型、响应速度、材料兼容、zero drift、leak/particle 规格。 | MFC 厂商毛利高；Ichor/UCT 式模块集成毛利低但随量放大。 |
| Chemical delivery/filtration | 膜材/树脂/高纯材料 30-45%；housing/阀件 15-25%；洁净制造 20%；QA/traceability 10-15%。 | defect reduction、filter lifetime、chemical compatibility、客户良率数据。 | Consumables 和 replacement cycle 支撑复购；涨价随化学品复杂度和良率价值传导。 |
| UHP 管阀件 | 材料 35-50%；机加/抛光/焊接 20-30%；洁净包装 10-15%；认证/检验 10-15%。 | 表面处理、内洁净、焊接可靠性、供应稳定性。 | 新 fab/EPC 项目前置锁量；关键规格供应短缺时按交期溢价。 |

## 5. 竞争格局、壁垒与价值捕获

### 5.1 市场结构

| 细分 | 头部集中度判断 | 代表性龙头 | 为什么能定价 |
|---|---|---|---|
| 高端半导体真空阀 | 极高，VAT 在半导体相关真空阀长期约 70% 级份额口径 | VAT、MKS、SMC、CKD、Fujikin、KITZ SCT | Chamber 认证深、颗粒/泄漏/寿命直接影响良率，换供应商风险远高于节省金额。 |
| Dry pump/abatement | 高，Edwards/Ebara/ULVAC/Kashiyama/Pfeiffer 等 | Edwards/Atlas, Ebara, ULVAC, Kashiyama, Pfeiffer/Busch/Leybold | Pump failure 会停整线；服务网络和 installed base 形成锁定。 |
| RF power/match/vacuum capacitor | 高，少数美欧日厂商 | Advanced Energy, MKS, Comet, DAIHEN, TRUMPF Huettinger, Kyosan, ADTEC | Plasma 稳定性与良率绑定；匹配算法和工艺 recipe 耦合，客户不愿切换。 |
| MFC/气体输送 | 中高，MFC 核心件集中，gas box 集成分散 | HORIBA, MKS, Fujikin, Brooks, Azbil, Parker, Ichor, UCT | 气体模型、腐蚀气适配、校准数据和工具认证带来高切换成本。 |
| 高纯过滤/污染控制 | 高，Entegris/Pall 等强 | Entegris, Pall/Danaher, MKS, Parker, Saint-Gobain | 缺陷密度降低价值可量化，耗材复购和客户数据锁定强。 |
| 模块代工/精密机加 | 中，客户集中但竞争者较多 | UCT, Ichor, Ferrotec, Foxsemicon, Sanmina, Jabil, Benchmark | 定价不如核心部件强，但 NPI 协同、产能、洁净制造和交付记录带来份额粘性。 |

### 5.2 壁垒清单

| 壁垒 | 量化/可观察指标 | 为什么能定价 |
|---|---|---|
| 认证标准 | OEM tool platform qualification 12-36 个月；fab process qualification 更长。 | 客户为了避免重新认证，不会为 5-10% 价格差替换关键部件。 |
| 可靠性/寿命 | Vacuum valve cycle life、leak rate、pump MTBS、RF uptime、MFC drift ppm/年。 | 失效成本是 wafer scrap + downtime，远高于部件价格。 |
| 颗粒/污染控制 | Particle adders、metal ion contamination、outgassing、filter defect reduction。 | 先进逻辑/HBM 良率提升 0.1pct 都可能价值巨大。 |
| 工艺 know-how | RF waveform、matching algorithm、gas model、precursor compatibility、abatement recipe。 | 子系统与整机 recipe 深度耦合，形成隐性 IP。 |
| 规模与服务网络 | 全球 field service、spares hub、installed base、24/7 support。 | Fab 更愿意向可保 uptime 的供应商支付高价。 |
| 客户锁定 | 与 AMAT/Lam/TEL/ASML/KLA/ASM 等共同 NPI；供应商进入 AVL。 | 进入 AVL 后长期供货，退出成本高。 |
| 供应链安全 | 多地制造、合规、出口管制、ESG/traceability。 | AI fab 项目抢交期，客户愿为可交付供应链付溢价。 |

### 5.3 长期高 ROIC/高毛利层

最可能长期高 ROIC 的排序：

1. **高端真空阀/pressure control**：VAT 型份额和认证壁垒最强，产品价值小但失效代价大，毛利和现金回报能力最好。
2. **RF power/match/vacuum capacitor**：GAA/HBM/DRAM/NAND 都提高 plasma complexity；算法和工艺耦合让替代难。
3. **污染控制/过滤/高纯材料**：Entegris 型业务既有高毛利，又有耗材复购，且价值可用良率缺陷直接证明。
4. **MFC/ALD vapor delivery/UHP valve**：随着 ALD/低蒸气压 precursor 增长，核心件价值上移；gas box 集成毛利较低。
5. **pump+abatement service**：硬件毛利中高，service 合同和 spares 提升周期韧性。
6. **模块代工/精密制造**：最受益于量，但 ROIC 取决于产能利用率和客户集中度，长期毛利通常不如核心部件。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 6.1 2026 三个最可能拐点

1. **AI/HBM 把 WFE 从“周期恢复”推向“订单加速”**  
   SEMI 的 300mm equipment spending 2026/2027 双位数增长和 Gartner 的 AI 半导体 30% 占比共同验证：AI 需求已经足够大，能拉动先进逻辑、HBM DRAM、NAND、先进封装同步投资。

2. **子系统供应链开始出现一手订单确认**  
   VAT book-to-bill 1.6、Atlas Vacuum organic order +32%、Comet book-to-bill 1.4、Ichor/UCT Q2 指引上行、INFICON 上调全年指引，说明二级供应链已经不是“等整机厂发号施令”，而是在提前备产。

3. **先进封装洁净要求前道化**  
   CoWoS/SoIC/hybrid bonding/RDL/HBM4 使后道工艺需要前道级别的真空、plasma activation、化学液洁净、过滤和泄漏控制。2026 最可能超预期的子方向是 advanced packaging fluid/vacuum/plasma 模块。

### 6.2 2026 最可能放量子方向

| 子方向 | 放量确定性 | 头部公司 |
|---|---|---|
| HBM/advanced DRAM 相关 RF/真空/MFC | 很高 | Advanced Energy, MKS, Comet, Edwards, Ebara, VAT, HORIBA, Fujikin |
| CoWoS/SoIC/hybrid bonding 化学液/过滤/真空 | 很高 | Entegris, Ichor, UCT, MKS, SCREEN/TEL/ASMPT 生态, VAT, INFICON |
| Pump + abatement + service | 高 | Edwards/Atlas, Ebara, ULVAC, Kashiyama, Busch/Pfeiffer/Leybold, DAS/abatement 供应商 |
| MFC/digital gas box/ALD precursor delivery | 高 | HORIBA STEC, MKS, Fujikin, Brooks, Azbil, Parker, Ichor, UCT |
| RF pulsed power/fast match | 高 | Advanced Energy, MKS, Comet, DAIHEN, TRUMPF Huettinger, Kyosan, ADTEC |
| 中国本土化子系统 | 高弹性 | 北方华创体系、七星、正帆科技、至纯科技、英杰电气、汉钟精机、中科仪、盛剑环境等 |

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 7.1 2027 三个最可能拐点

1. **HBM4/Rubin/MI400/TPU8 从验证转向规模收入**  
   2026 是 HBM4 认证和 NPI，2027 才是高端 AI 芯片新一代的真实量产年。对应子系统弹性在 HBM DRAM、TSV、电镀、混合键合、package test、pump/abatement。

2. **2nm/GAA 和背面供电进入更大客户面**  
   2027 A16/BSPDN、N2/N2P 及其 derivatives 会显著提高 ALD、etch、metrology、clean 工艺复杂度；RF/MFC/真空/温控的单 tool 价值量继续上升。

3. **绿色制造和本地化从口号变成设备规格**  
   新 fab 会把 abatement 效率、energy-efficient pump、化学品回收、低泄漏 UHP 系统写进招标；中国、美国、欧洲本地化也会重塑二级供应商份额。

### 7.2 2027 最可能放量子方向

| 子方向 | 2027 放量逻辑 | 观察指标 |
|---|---|---|
| HBM4 设备子系统 | Rubin/MI400/TPU8/Broadcom ASIC 需要更多 HBM4 | HBM4 qualification、多供应商份额、HBM tester/bonder 交期 |
| Hybrid bonding 和 wafer-level system | SoIC/CoWoS/SoW、C2W/W2W 更高洁净要求 | TSMC/OSAT capex、Besi/ASMPT/EVG/Applied packaging 订单 |
| Pulsed RF/fast match | GAA、DRAM、NAND 高深宽比 etch 更难 | AE/MKS/Comet semi order growth、客户 NPI wins |
| Integrated pump-abatement | 绿色 fab 和 uptime 驱动 | Edwards/Ebara/ULVAC service backlog、abatement retrofit |
| Digital MFC/advanced gas box | ALD/etch gas routes 更复杂 | HORIBA/MKS/Fujikin/Ichor/UCT 订单和交期 |
| 中国国产替代 | 出口管制和本土 fab 扩产 | 国产 MFC、RF power、干泵、尾气、气体柜验证进度 |

## 8. 头部公司与细分玩家清单

### 8.1 真空泵、尾气处理、真空服务

Edwards Vacuum/Atlas Copco、Leybold/Atlas Copco、Ebara、ULVAC、Kashiyama Industries、Pfeiffer Vacuum/Busch、Busch Vacuum、Agilent Vacuum、Shimadzu、Osaka Vacuum、Hanbell Precise Machinery、KYKY/中科仪、SKY Technology、EVP Vacuum、DAS Environmental、Ecosys/Edwards、CS Clean Solutions、Centrotherm、GST、盛剑环境。

### 8.2 真空阀、压力控制、真空规、泄漏检测

VAT Group、MKS Instruments/Granville-Phillips、INFICON、Pfeiffer、Edwards、SMC、CKD、Fujikin、KITZ SCT、ULVAC、HVA、Nor-Cal Products、Kurt J. Lesker、V-Tex、Azbil、Brooks Instrument、Sevenstar/七星、正帆科技、至纯科技。

### 8.3 RF/plasma power、match network、真空电容

Advanced Energy、MKS/ENI/Alter、Comet Plasma Control Technologies、DAIHEN、TRUMPF Huettinger、Kyosan Electric、ADTEC Plasma Technology、XP Power、New Power Plasma、Seren IPS、Coaxial Power Systems、Pearl Kogyo、英杰电气、北方华创相关电源供应链。

### 8.4 MFC、气体柜、气液输送模块

HORIBA STEC、MKS Instruments、Fujikin、Brooks Instrument/ITW、Azbil、Bronkhorst、Alicat/Halma、Parker、SMC、CKD、Ichor Systems、Ultra Clean Holdings、SEMI-GAS、High Purity Systems、Kinetics、Mega Fluid Systems、Pivotal Systems、正帆科技、至纯科技、七星/北方华创体系、金宏气体/华特气体等特气生态。

### 8.5 化学液输送、过滤、污染控制、UHP 材料

Entegris、Pall/Danaher、Parker、Saint-Gobain、Nippon Pillar、GEMU、Swagelok、Fujikin/Carten、KITZ SCT、CKD、SMC、Ham-Let、Hy-Lok、DK-Lok、Valex、Dockweiler、Fitok、Ichor、UCT、Kinetics、Mega Fluid Systems、MKS、正帆科技、至纯科技。

### 8.6 温控、chiller、热管理

SMC、Shinwa Controls、Daikin、Advanced Thermal Sciences/Mydax、Ferrotec、Boyd/Lytron、LAUDA、Julabo、Thermo Fisher、Kanto/日本温控供应链、同飞股份、高澜股份及本土半导体温控供应商。

### 8.7 精密机加、陶瓷/涂层、清洗和子系统代工

Ultra Clean Holdings、Ichor Systems、Ferrotec、Foxsemicon Integrated Technology、KoMiCo、CoorsTek、Kyocera、Morgan Advanced Materials、NGK、Momentive、TOTO ceramics、Sanmina、Jabil、Benchmark、Celestica、Shibaura Mechatronics 供应链、Marketech International。

## 9. 投资排序与监控指标

### 9.1 最值得优先跟踪

| 排名 | 环节 | 理由 |
|---:|---|---|
| 1 | 高端真空阀/APC/真空规 | 高集中度、高毛利、高切换成本；VAT/INFICON 已有订单确认。 |
| 2 | RF power/match/vacuum capacitor | GAA/HBM/DRAM/NAND 都提升 tool intensity，产品小但定价强。 |
| 3 | 高纯过滤/污染控制/化学液输送 | 先进封装和 HBM 把良率控制从前道延伸到后道，Entegris 型复购好。 |
| 4 | Pump + abatement + service | 新 fab 和 uptime 共同拉动，服务收入抗周期。 |
| 5 | MFC/digital gas box/ALD precursor delivery | ALD/etch 气体路线增加，国产替代弹性大。 |
| 6 | 子系统集成/精密清洗/涂层 | 量弹性大，但需警惕毛利率和客户集中度。 |

### 9.2 需要持续观察的 12 个指标

1. SEMI 300mm fab equipment spending 是否继续上修 2026/2027。
2. TSMC、Samsung、Intel、SK hynix、Micron 的 HBM/2nm/advanced packaging capex。
3. ASML、Applied、Lam、TEL、KLA 的 leading-edge logic/HBM/advanced packaging 订单措辞。
4. VAT book-to-bill 是否连续高于 1.2，半导体订单是否继续环比增长。
5. MKS 半导体与 advanced electronics 订单中 remote plasma/RF/chemistry 的增长。
6. Advanced Energy 半导体 revenue 是否在 2026 创纪录，gross margin 是否维持 40%+。
7. Comet PCT 订单和 Synertia RF 平台客户导入速度。
8. Atlas Copco Vacuum Technique organic order growth 和 operating margin。
9. Ichor/UCT Q2-Q4 指引是否持续环比提高，毛利是否随产能利用率修复。
10. Entegris APS/filtration 是否连续创高，Advanced Purity segment profit margin 是否维持 25%+。
11. INFICON 半导体/真空镀膜收入增速和软件/传感器 attach。
12. 中国本土 MFC、RF power、dry pump、gas cabinet 是否进入头部 fab AVL。

## 10. 风险

- AI capex 若在 2027 因 token ROI、融资成本或电力约束放缓，子系统订单会滞后 1-2 个季度反映。
- 先进封装/HBM4 若验证延迟，2026 H2 到 2027 的极超情景会回落到基准。
- 子系统公司客户集中度高，整机 OEM 改设计或库存调整会放大收入波动。
- 中国国产替代一方面带来本土公司弹性，另一方面压低成熟规格 ASP。
- 物流、关税、出口管制、稀有材料和高纯聚合物供给可能影响毛利。

## 11. 主要来源

- [SEMI：2026/2027 300mm fab equipment spending 预计 $133B/$151B](https://www.semi.org/en/semi-press-release/semi-projects-double-digit-growth-in-global-300mm-fab-equipment-spending-for-2026-and-2027)
- [SEMI：全球半导体制造设备销售 2025/2026/2027 预计 $133B/$145B/$156B](https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports)
- [Gartner：2026 全球半导体收入预计 $1.320T，AI 半导体约占 30%](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- [ASML 2026Q1 财报](https://www.asml.com/en/news/press-releases/2026/q1-2026-financial-results)
- [Applied Materials/SK hynix HBM R&D 合作，2026-03](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-and-sk-hynix-announce-long-term-rd-partnership)
- [Applied Materials 2nm/GAA transistor and wiring innovations，2026-02](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-transistor-and-wiring-innovations/)
- [TSMC 2026 Technology Symposium](https://www.tsmc.com/static/english/campaign/Symposium2026/index.htm)
- [TSMC CoWoS/SoIC/SoW/COUPE 官方技术发布](https://pr.tsmc.com/english/news/3136)
- [Semiconductor Engineering：TSMC Tech Symposium 2026 by the numbers](https://semiengineering.com/tsmc-tech-symposium-2026-by-the-numbers/)
- [MKS Instruments 2026Q1 财报](https://www.globenewswire.com/news-release/2026/05/06/3289424/16396/en/mks-inc-reports-first-quarter-2026-financial-results.html)
- [VAT Group 2026Q1 订单摘要](https://www.webdisclosure.com/article/vat-group-ag-etr-vat-group-ag-experiences-strong-q1-2026-order-intake-amid-supply-chain-challenges-yKmeyj7BGmA)
- [Atlas Copco 2026Q1 报告，Vacuum Technique](https://www.atlascopcogroup.com/content/dam/atlas-copco/group/documents/investors/financial-publications/english/20260428-en-q1-2026-ib.pdf)
- [Ichor 2026Q1 财报 SEC 8-K](https://www.sec.gov/Archives/edgar/data/1652535/000165253526000028/ex-991_26q1xearnings.htm)
- [Ultra Clean 2026Q1 财报 SEC 8-K](https://www.sec.gov/Archives/edgar/data/1275014/000162828026027952/q12026pressrelease.htm)
- [Entegris 2026Q1 财报](https://investor.entegris.com/news/news-details/2026/Entegris-Reports-Results-for-First-Quarter-of-2026/default.aspx)
- [INFICON 2026Q1 财报与指引上调](https://www.inficon.com/en/news/inficon-reports-strong-first-quarter-and-raises-guidance)
- [Advanced Energy 2026Q1 call transcript](https://www.fool.com/earnings/call-transcripts/2026/05/05/advanced-energy-aeis-q1-2026-earnings-transcript/)
- [Advanced Energy 2026Q1 results data](https://www.marketscreener.com/news/advanced-energy-reports-first-quarter-2026-results-ce7f58dfdb8cf426)
- [Comet 2026Q1 订单摘要](https://www.webdisclosure.com/article/comet-holding-ag-etr-comet-reports-strong-order-intake-amidst-sales-decline-in-q1-2026-cHzhtQAylGI)
- [Comet 2025 Annual Report：GAA/HBM/advanced DRAM 对 RF/match/vacuum capacitor 的拉动](https://comet.tech/getmedia/39e7122c-a09f-4363-9a09-0b3685bec85f/Comet_Annual-Report-2025-en.pdf?disposition=attachment)
- [HORIBA semiconductor MFC product page](https://www.horiba.com/sgp/semiconductor/products/mass-flow-controller-and-module/)
- [Lam Research DRAM/HBM process solution page](https://www.lamresearch.com/products/our-solutions/dram/)
- 市场规模辅助校验：Fortune Business Insights、Mordor、GlobalGrowthInsights、DIResearch、360iResearch、IndustryResearch、MicroMarketInsights 等对 MFC、gas delivery、vacuum pump、vacuum valve、UHP valve/fittings、plasma generator 的 2026-2035 市场测算。本文未直接照搬单一报告，而是用多方口径和上市公司收入交叉约束。

---

非投资建议。本报告用于产业链研究和情景建模；实际投资仍需结合估值、订单持续性、客户集中度、资产负债表、出口管制与下游 capex 修正风险。
# 行业调研：【玻璃基板、TGV与玻璃检测】

> 截至日期：2026-05-08  
> 研究口径：聚焦 AI/HPC 先进封装中的 glass core substrate、glass interposer、TGV（Through Glass Via）成孔/金属化、玻璃面板级封装、玻璃检测量测，以及与它们竞争或互补的 ABF/FC-BGA、硅中介层、RDL interposer、陶瓷 core。  
> 预测原则：对 2026-2027 AI 计算中心建设采用明显乐观假设。公司未披露的市场规模、渗透率和利润率均为研究估算，不代表公司指引。

## 0. 一页结论

玻璃基板在 2026 年的投资价值不是“已经替代 CoWoS/ABF 大规模出货”，而是 **AI 封装尺寸继续膨胀后，玻璃从验证线进入供应链卡位的前夜**。2026 年真实确定性最高的收入来自三类：TGV 成孔/金属化设备与服务、玻璃面板/载板样品线、玻璃缺陷与 TGV 检测量测。AI xPU 量产主线仍是 CoWoS-L/S/R + HBM3E + 高阶 ABF/FC-BGA；玻璃更像 2027-2028 年的期权，但这个期权已经被 Intel、Samsung Electro-Mechanics、SKC/Absolics、DNP、AGC、TOPPAN、LPKF、Onto、SCHOTT、JNTC、TSMC CoPoS 等一手动作推到产业化窗口。

最可投资的顺序：

| 顺位 | 方向 | 2026 收入确定性 | 2027-2028 弹性 | 判断 |
|---|---:|---:|---:|---|
| 1 | 玻璃/TGV 检测量测、缺陷分类、3D metrology | 高 | 高 | 每条 pilot/HVM 线都要 100% panel + via + RDL + warpage 检测，且良率越低检测价值越高。Onto Firefly/Dragonfly、KLA、Camtek、ViTrox/精测类玩家受益。 |
| 2 | TGV 成孔、边缘/切割、SeWaRe 防裂、玻璃加工设备 | 中高 | 很高 | LPKF LIDE、SCHMID 全流程 lab、Philoptics/韩国设备、激光/湿法/蚀刻平台会先于基板本体放量。 |
| 3 | TGV 金属化、铜填孔、种子层/电镀/浆料 | 中 | 很高 | 高 AR TGV 的 void、裂纹和热循环可靠性是量产瓶颈。Elephantech 2026-04 推出铜纳米浆料说明材料路线开始收敛。 |
| 4 | AI-grade glass core substrate 样品与低量产 | 低到中 | 极高 | 2026 多为 NPI/qualification；2027 小批量；2028 才是更可信的 HVM 节点。 |
| 5 | glass interposer / CoPoS / photonic glass substrate | 低 | 极高 | 若 2027-2028 package 进入 8x-10x reticle、1.6T/3.2T/CPO 压力提前，玻璃 interposer 会被提前重估。 |

最关键的反直觉结论：**2026 最可能赚钱的不是“玻璃基板出货量”，而是“玻璃量产前的工艺控制权”。** 一旦客户把某种 TGV 几何、RDL overlay、裂纹检测和可靠性模型写进 package design rule，后续切换成本会非常高。

## 1. 事实锚点：最近半年与 2026 一手信息

| 公司/机构 | 时间 | 关键信息 | 对投资判断的含义 |
|---|---:|---|---|
| Intel | 2023-09 发布，2024-08 product brief 仍作为路线锚 | Intel 称玻璃基板目标是本十年后半段进入市场；官方 brief 给出 glass-core 可带来 50% 更多 die content、最高 10x through-hole density、448Gbps 信号路径、75um through-hole test vehicle、约 20:1 AR、116x113mm 到 240x240mm 路线图。 | Intel 是最明确把 glass-core substrate 和 AI/HPC advanced packaging 绑定的 IDM/foundry。2026 不等于 HVM，但说明 design rule、EMIB、供电和光互连协同已经进入客户服务阶段。 |
| TrendForce / NEPCON Japan 2026 线索 | 2026-01/2026-05 | Intel 在 NEPCON Japan 2026 展示 EMIB + glass substrate 样品，报道提到 45um bump pitch、约两倍 reticle size、No SeWaRe 微裂纹结果。 | 这是一条产业情绪拐点：玻璃从“概念材料”进入“封装样品可展示”。仍需客户可靠性数据。 |
| SKC/Absolics / NIST CHIPS | 2024-2026 | Absolics Covington, Georgia：$75M CHIPS direct funding，项目 capex $343M，120,000 sq ft；客户首批交付 expected in 2025，production capacity expected in 2027；另获 $100M NAPMP direct funding 与 $89M co-investment，建设 glass-core packaging ecosystem。 | 这是美国本土最清晰的 glass substrate 产能锚。2026 是样品/认证，2027 产能启动。 |
| Samsung Electro-Mechanics | 2026-04-30 Q1 | Q1 revenue KRW 3.2091T，op profit KRW 280.6B；Package Solution revenue KRW 725B，YoY +45%，AI accelerators/server CPU/network 高端 FCBGA 拉动；Q2 强需求延续。 | 传统高端 FC-BGA 已经被 AI 拉爆，玻璃是下一代路线；2026 的现实主线仍是 high-layer large-area embedded FCBGA。 |
| Samsung Electro-Mechanics / CES 2025 | 2025-01 | Sejong pilot line 已建立，2025 推客户样品，计划 2027 mass production。 | Samsung 把 glass substrate 明确放在 server CPUs 和 AI accelerators 方向。 |
| Samsung Electro-Mechanics + Sumitomo Chemical/Dongwoo Fine-Chem | 2025-11 | 签署 glass core JV MOU；Samsung 为 majority investor，Pyeongtaek 为初始基地；mass production planned after 2027。 | 韩国路线从研发转向材料 JV 和量产准备，2027 后商业化更可信。 |
| DNP | 2025-12 | Kuki Plant 新建 TGV glass core substrate pilot line，2025-12 phased operation，2026 early sample shipments；510x515mm；filled type 和 conformal type；FY2028 建立 full mass production 结构。 | 日本印刷/光刻/精密加工生态进入 glass core。DNP 的 FY2028 HVM 时间比多数媒体 hype 更保守、更可信。 |
| AGC | CES 2026 / product page | TGV glass substrate 支持 Chiplet、CPO substrate、RF；厚度 0.1-1.1mm+；TGV >=50um，AR up to 20:1 at 1.0mm；panel 510x515mm；产品页列 hole diameter 20-150um、pitch 约 hole diameter x2。 | AGC 是材料+加工能力锚，尤其在可调 CTE、面板尺寸、精密孔形上具备早期议价权。 |
| SCHOTT | 2026 页面 | Glass panels 覆盖 carrier、glass core substrate、structured wafer；advanced IC packaging 页面提到 CTE 3-10ppm/K、TTV <0.5um、surface roughness <1nm。 | 高端玻璃原片、TTV、表面粗糙度是量产底层瓶颈。SCHOTT/AGC/Corning/NEG 这类材料商最早受益。 |
| LPKF | 2025-10 至 2026 Q1 | LIDE 可做 crack-free TGV；技术页给出 up to 1:50 AR、via down to 5um、+/-1um position accuracy over 515x510mm；Q1 2026 披露 advanced packaging 尚未计入 volume orders，目标 2027 ramp-up、2028 HVM/双位数 EBIT。 | LPKF 是 TGV 成孔/玻璃处理最纯的上市工具链之一；2026 订单可能是验证线，真正爆发看 2027-2028。 |
| Onto Innovation + LPKF | 2025-04 / SEMICON West 2025 | Onto Firefly 进入 LPKF Vitrion cleanroom；用于 advanced IC substrates 和 panel-level packaging 的 automated inspection and 3D metrology；Onto 演讲强调 100% panel TGV CD、missing/abnormal TGV、microcrack、post metallization、RDL/bump height、panel warpage。 | 玻璃检测不是可选项，而是 HVM 前提。检测环节的收入会早于玻璃基板本体。 |
| Camtek | 2026-03 | $31M multi-system OSAT order，Q1 2026 leading OSAT orders >$90M，主要面向 CoWoS-like AI packaging。 | 虽然不是玻璃专属，但 AI advanced packaging inspection 已经订单化，玻璃会进一步抬高检测强度。 |
| JNTC | 2025-07 | 发布 TGV glass substrate；称 2025-06 完成国内产线，2025-08 full-scale manufacturing；自称 0% microcrack、void-free metallization、yield >90%、16 家 global partners。 | 需要折价看待单方声明，但韩国中小厂在 TGV 样品和设备自研上更激进，可能带来供应链 alpha。 |
| Elephantech | 2026-04-30 | 发布 SAphire G copper nano-paste for high-AR TGV filling；50um via、0.5mm glass、AR=10:1；-50C/+125C 250 cycles 后未见裂纹；铜材料成本约为银的 1/60；客户联合评估中。 | 金属化是 TGV HVM 的关键瓶颈。若 paste filling 可靠性过关，材料端会比基板端更早放量。 |
| Kyocera | 2026-04-27 | ECTC 2026 展示 multilayer ceramic core substrate；via diameter 75um、via pitch 200um；目标 AI data center xPU/switch ASIC。 | 陶瓷 core 是玻璃 core 的强竞争路线，主打刚性和细线化。它会分流部分“低翘曲 core”估值。 |
| TSMC CoPoS / TrendForce | 2026-04/05 | CoPoS pilot line 预计 2026 mid-year 完成，2027 small-volume trial，2028-2029 mass production。 | TSMC 不一定最早用 glass-core substrate，但 panel-level、glass/sapphire panel、CoPoS 是 2028+ 最大需求弹性。 |

## 2. AI 计算中心 2026 的机遇、挑战与最可能技术路径

### 2.1 为什么 AI 计算中心会拉动玻璃/TGV

2026 AI 集群的瓶颈从单颗 GPU 扩散到 package、基板、HBM、互连、供电和检测。项目内 `ai_chip_research_2026_2027.md` 和 `行业调研_AI芯片先进封装_2026.md` 的共同结论是：2026 最大量平台仍是 GB300/B300、Trainium2、Ironwood TPU、GB200/B200、Ascend、MI350、Trainium3、MTIA、Maia200；这些平台大多还是 CoWoS/2.5D + HBM + 大面积 ABF。玻璃的机会来自下一步：

1. Package area 继续变大：HBM4、12 stack HBM、更多 chiplet、CPO/光 I/O、更多电源/去耦都要求更大的 substrate/interposer。
2. Organic substrate 受限：大尺寸封装下 warpage、层间 overlay、fine line/space、低损耗、CTE 不匹配越来越难。
3. Silicon interposer 成本和尺寸受限：硅中介层适合高密度，但 300mm wafer 面积利用率和成本在超大 package 上恶化。
4. Panel-level manufacturing 诱惑很大：510x515mm、600x600mm、750x620mm 等面板路线理论上能提高面积利用率，但前提是检测、overlay 和裂纹控制过关。
5. CPO/光互连需要低损耗和光学结构：玻璃天然适配 waveguide、V-groove、光纤耦合、CPO substrate。

### 2.2 2026 正在使用的主流技术

| 技术 | 2026 状态 | 主要使用场景 | 玻璃/TGV 关系 |
|---|---|---|---|
| 高端 ABF/FC-BGA organic substrate | 已大规模量产且紧缺 | GB300/B300、GB200、MI350、CPU、switch ASIC、custom ASIC | 玻璃 core 的直接替代对象，但 2026 不会被大规模替代。 |
| CoWoS-S/L/R + silicon/RDL interposer | 高端 AI 默认路径 | NVIDIA、AMD、TPU、Trainium、Maia、MTIA 等 | 玻璃 interposer/CoPoS 是 2027-2029 的潜在补充。 |
| EMIB / bridge-in-substrate | Intel 差异化路线，2026 客户验证加强 | HPC/AI chiplet、foundry packaging | 玻璃 core + EMIB 是 Intel 最明确的玻璃路线之一。 |
| Fan-out / RDL on substrate / panel-level RDL | 2026 设计导入、switch/ASIC 渗透提升 | 大尺寸 ASIC、network switch、低成本 interposer | 可与玻璃 carrier/core 结合。 |
| Glass core substrate + TGV | 2026 pilot/sample/qualification | 服务器 CPU、AI accelerator、switch ASIC、CPO substrate | 本报告核心。2026 重在客户认证与设备材料订单。 |
| Glass interposer | 更早期 | RF、CPO、特殊 AI/photonic interposer | 2028+ 弹性更大。 |
| Ceramic core substrate | 2026 展示/开发 | AI xPU、switch ASIC、军工/高可靠 | 玻璃替代/互补路线，Kyocera 2026 ECTC 是新锚点。 |

### 2.3 2026-2027 出货量最大的 10 款 AI 芯片/平台对玻璃路线的影响

| 排名 | 平台 | 2026-2027 主流封装路径 | 对玻璃基板/TGV的拉动 |
|---:|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | CoWoS-L/S + HBM3E + 大面积 ABF + NVL72 液冷 | 2026 不是玻璃主线；但 package 尺寸、HBM attach 和 ABF 紧缺为 2027-2028 玻璃替代创造理由。 |
| 2 | AWS Trainium2 | 定制 ASIC + HBM + NeuronLink/EFA + 高端基板 | 自用 ASIC 规模大，若 AWS 寻求非 CoWoS/ABF 第二路径，玻璃 core 可能先在 ASIC 而非 GPU 导入。 |
| 3 | Google TPU v7 Ironwood | Broadcom/Google XPU + HBM + 2.5D/RDL/高端基板 | TPU 的大规模推理需求适合成本优化路线，2027-2028 是 glass interposer/CoPoS 候选。 |
| 4 | NVIDIA B200/GB200 | CoWoS + HBM3E + ABF | 存量订单延续，不是玻璃切入点。 |
| 5 | Huawei Ascend 910C/950 | 国产先进封装 + HBM/自研互连 + 有机/国产载板 | 中国玻璃/TGV 更可能先在国产 ASIC/先进封装试点验证，而非最顶级 HBM GPU。 |
| 6 | Cambricon MLU 590/690 | 国产先进节点 + HBM/OAM + 高端基板 | 国产供应链有玻璃导入动力，但可靠性和产线成熟度更慢。 |
| 7 | AMD MI350/MI355 | 2.5D + HBM3E + OAM/UBB/PCIe | 2026 主线仍为 ABF/CoWoS；MI400/HBM4 才是玻璃期权更强的平台。 |
| 8 | AWS Trainium3 | 3nm + HBM3E + 144-chip UltraServer | 2027 放量后对 panel-level、open packaging、检测提出更高要求。 |
| 9 | Meta MTIA 300/400/450/500 | Broadcom XPU + OCP rack + 推理 ASIC | 推理 ASIC 若追求低成本/大面积，极适合作为 2027 玻璃 core 小批量候选。 |
| 10 | Microsoft Maia 200 | TSMC 3nm + HBM3E + 先进封装 + 闭环液冷 | 2026 Azure 自用，不大概率玻璃化；2027 后续版本可关注。 |

补充：NVIDIA Rubin、AMD MI400/MI455X、Google TPU8、OpenAI/Broadcom custom accelerator 才是玻璃路线的强 beta。它们的共同特征是 HBM4、更大 interposer、更多 chiplet、更高供电和光互连压力。

### 2.4 新技术成熟与放量时间：三情景

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 | 2026 最可能性 |
|---|---|---|---|---|
| AI-grade glass core substrate | 2026 样品/认证；2027 小批量；2028 HVM | 2027 H2 有头部 ASIC/switch 小量收入；2028 明显放量 | 2027 H2 被 CSP custom ASIC 拉进量产 BOM，2028 成为高端 ASIC 第二路径 | 中低，偏 NPI |
| TGV laser/etch 成孔 | 2026 设备验证和 pilot 订单；2027 ramp | 2026 H2 多条 pilot 线下单，2027 HVM 工具提前锁单 | 2026 内出现多个客户 production order | 高 |
| TGV 铜金属化/ECP/paste filling | 2026 联合评估；2027 客户认证；2028 随基板放量 | 2027 小批量收入，铜 paste/电镀共存 | 2026 H2 高 AR via 金属化方案被大客户设计锁定 | 中高 |
| 玻璃检测量测 | 2026 pilot 必配；2027 随客户验证线放量 | 2026 下半年检测订单显著增加，工具交期拉长 | 玻璃缺陷库和 AI 分类软件成为客户锁定点，2027 前收入翻倍 | 很高 |
| Glass interposer | 2026-2027 小样；2028 后量产 | 2027 在 CPO/switch/ASIC 小批量 | 224G/448G electrical reach 提前触顶，CPO glass interposer 2027 放量 | 中低 |
| CoPoS / panel-level on glass | 2026 pilot；2027 trial；2028-2029 HVM | 2027 H2 特定客户小量，2028 开始规模 | 2027 被 NVIDIA/custom ASIC 提前锁产能 | 中低，长期高 |
| Embedded passives/power in glass | 2026 test vehicle；2027 design-in | 2027 成为 2kW+ package 选项 | GB300/Rubin successor 设计提前拉动 | 中 |
| Ceramic core 替代 | 2026 展示；2027 pilot；2028+ | 2027 高可靠 switch/ASIC 采用 | 2027 抢走部分 glass core 估值 | 中 |

2026 最可能的技术路径：**高端 ABF/CoWoS 继续主导量产，玻璃/TGV 围绕 pilot line、sample shipment、metrology、TGV process、客户可靠性认证先放量。**

## 3. 已经开始放量的关键产品：市场规模、渗透率、利润率

这里“已放量”分两层：一是 AI 封装真实量产路径，二是玻璃/TGV 相关已经有商业订单或样品线的产品。未来 3 个月指 2026-05 到 2026-08，1 年指到 2027-05，2 年指到 2028-05。

| 已放量/准放量产品 | 当前状态 | 未来 3 个月市场规模，基准/乐观/极度乐观 | 未来 1 年市场规模，基准/乐观/极度乐观 | 未来 2 年市场规模，基准/乐观/极度乐观 | 渗透率路径 | 毛利率/利润率估算 |
|---|---|---:|---:|---:|---|---|
| 高端 AI ABF/FC-BGA substrate | 2026 真实主线，Samsung EM Package Solution Q1 2026 YoY +45%，AI/server/network 拉动 | $1.8-3.0B / $3-4.5B / $4.5-6.5B | $8-13B / $13-20B / $20-30B | $14-24B / $24-40B / $40-60B | AI xPU attach rate 95-100%；高阶 ABF 占整体 substrate 约 35-45%，2028 可到 50-65% | 22-32% / 30-42% / 40-55%；高端满载和客户预付款可推高。 |
| 玻璃 carrier / temporary bonding carrier / reusable glass panel | 先进封装和 wafer thinning 已成熟使用，玻璃不是新材料 | $0.15-0.35B / $0.35-0.55B / $0.55-0.8B | $0.7-1.4B / $1.4-2.2B / $2.2-3.5B | $1.5-3B / $3-5B / $5-8B | 先进封装 carrier 中玻璃持续提升；AI/HBM/3DIC 会增加可重复使用 carrier 和检测需求 | 25-45%；高端 TTV/低粗糙度 carrier 可 45%+。 |
| TGV glass wafers/panels for RF/MEMS/3D IPD | 小规模成熟，不完全依赖 AI；AGC/SCHOTT/Corning/3DGS 等已有供应 | $0.08-0.18B / $0.18-0.3B / $0.3-0.5B | $0.35-0.8B / $0.8-1.4B / $1.4-2.3B | $0.8-1.8B / $1.8-3.5B / $3.5-6B | RF/MEMS 较成熟；AI glass core 前置验证会把 TGV 面板需求从 wafer 扩到 panel | 30-50%；定制 TGV/小批高难度可 50-60%。 |
| TGV 成孔/玻璃加工设备与服务 | LPKF、SCHMID、Philoptics 等验证线和客户项目活跃 | $0.10-0.25B / $0.25-0.45B / $0.45-0.8B | $0.6-1.2B / $1.2-2.5B / $2.5-5B | $1.8-4B / $4-8B / $8-15B | 2026 pilot line 渗透 20-40%；2027 进入量产线 50-70%；2028 高端玻璃线几乎必配 | 45-65%；软件/process recipe/IP 可更高，整线设备 35-55%。 |
| 先进封装检测量测：Firefly/Dragonfly/KLA/Camtek 等 | 已有 CoWoS/HBM/2.5D 订单，玻璃会增加检测步骤 | $0.35-0.7B / $0.7-1.1B / $1.1-1.8B | $1.8-3.2B / $3.2-5.5B / $5.5-9B | $4-8B / $8-14B / $14-24B | AI advanced packaging 工具渗透持续上升；glass pilot 线检测 attach rate 接近 100% | 50-65% gross margin，软件/defect management 70%+；高端 AOI/3D metrology 受益最大。 |
| Glass-core substrate 样品与 low-volume sample shipment | Absolics/JNTC/DNP/Samsung 等进入样品/原型阶段 | $0.02-0.08B / $0.08-0.2B / $0.2-0.5B | $0.2-0.6B / $0.6-1.5B / $1.5-3.5B | $1.5-3.5B / $3.5-8B / $8-18B | 高端 AI xPU substrate 中 2026 <1%；2027 1-5%；2028 基准 5-10%、极度乐观 15%+ | 早期账面毛利波动大：0-30% / 25-45% / 45-65%；样品价高但良率和折旧重。 |

增长预测区间：

| 产品群 | 未来 12 个月基准增长 | 乐观 | 极度超预期 |
|---|---:|---:|---:|
| 高端 AI ABF/FC-BGA | +25-45% | +50-75% | +90%+ |
| 玻璃 carrier / panel | +15-30% | +30-55% | +70%+ |
| TGV wafer/panel | +25-50% | +60-100% | +150%+ |
| TGV 设备/服务 | +40-80% | +100-180% | +250%+ |
| 玻璃检测量测 | +35-70% | +80-140% | +200%+ |
| Glass-core sample/low volume | +100%+ | +300%+ | +700%+，但从极低基数出发 |

## 4. 在研关键产品和细分技术：市场规模、渗透率、利润率

| 在研产品/技术 | 技术状态 | 未来 3 个月市场规模，基准/乐观/极度乐观 | 未来 1 年市场规模，基准/乐观/极度乐观 | 未来 2 年市场规模，基准/乐观/极度乐观 | 渗透率路径 | 利润率估算 |
|---|---|---:|---:|---:|---|---|
| AI glass-core FC-BGA for xPU/server CPU | Intel/Samsung/Absolics/DNP/JNTC 样品与 pilot；客户认证中 | $0.01-0.05B / $0.05-0.15B / $0.15-0.4B | $0.15-0.5B / $0.5-1.2B / $1.2-3B | $1-3B / $3-7B / $7-15B | 2026 <1%；2027 1-3%；2028 5-12% | 早期 0-35%；供不应求后 40-60%；失败线可能亏损。 |
| Glass interposer replacing silicon interposer | RF/CPO/特殊应用先行；AI 主流仍早 | <$0.03B / $0.05-0.12B / $0.12-0.3B | $0.1-0.4B / $0.4-1B / $1-2.5B | $0.8-2.5B / $2.5-6B / $6-14B | 2.5D AI interposer 中 2026 近 0；2028 基准 2-5%、极度乐观 10%+ | 35-60%；若替代 silicon interposer 且良率稳定，ROIC 很高。 |
| CoPoS / panel-level packaging on glass/sapphire | TSMC/VisEra pilot、Rapidus探索，2028-2029 HVM 更可信 | <$0.05B / $0.05-0.15B / $0.15-0.4B | $0.2-0.8B / $0.8-2B / $2-5B | $2-6B / $6-14B / $14-30B | 2027 前 <2%；2028 若首批 AI 客户导入 3-8% | 初期低毛利或负毛利；成熟后 35-55%，平台方更高。 |
| High-AR TGV copper metallization materials | Elephantech、ECP、paste filling、seedless/seeded 方案并行 | $0.03-0.08B / $0.08-0.18B / $0.18-0.35B | $0.2-0.6B / $0.6-1.2B / $1.2-2.5B | $0.8-2B / $2-4.5B / $4.5-9B | 在 glass-core BOM 中 2026 是验证，2028 attach rate 接近 100% | 35-60%；特种铜浆/化学品 45-65%，但客户压价快。 |
| Embedded passives/power delivery in glass | Intel brief 提到 integrated power options；仍早 | <$0.02B / $0.03-0.08B / $0.08-0.2B | $0.1-0.3B / $0.3-0.8B / $0.8-1.5B | $0.5-1.5B / $1.5-4B / $4-8B | 高端 glass package 中 2028 10-25% 可选；2kW+ package 拉动 | 40-65%；专利/客户共设计强。 |
| Glass optical waveguide/CPO substrate | AGC/LPKF/SCHOTT/Ayar/Lightmatter 生态，AI switch 先行 | $0.03-0.1B / $0.1-0.25B / $0.25-0.6B | $0.3-0.8B / $0.8-2B / $2-5B | $2-6B / $6-15B / $15-35B | CPO 在 AI switch 中 2026 <5%，2027 5-12%，2028 10-25% | 35-60%；光引擎/IP/测试软件 50-75%。 |
| In-package glass microfluidic cooling | LPKF 等展示可能性，商业化更晚 | 近 0 / <$0.03B / $0.05B | <$0.1B / $0.1-0.3B / $0.3-0.8B | $0.5-1.5B / $1.5-4B / $4-10B | 2028 前非主流；极端高功耗 ASIC 有试点 | 高定制毛利 45-70%，但可靠性风险极高。 |
| Ceramic core substrate | Kyocera 2026 ECTC，替代/互补玻璃 | <$0.05B / $0.05-0.15B / $0.15-0.3B | $0.1-0.4B / $0.4-0.9B / $0.9-1.8B | $0.8-2B / $2-5B / $5-10B | 高可靠/AI switch/军工先行，2028 1-5% | 40-65%；材料 know-how 与仿真服务增强定价。 |

最值得跟踪的“快速增长关键产品”：

1. **TGV 检测量测工具**：TGV CD、sidewall、missing via、microcrack、void、RDL defect、warpage、panel distortion 都会成为 HVM 前置数据。
2. **High-AR TGV 金属化**：若铜填孔方案在 10:1 到 20:1 AR 上跑通热循环，玻璃路线的商业化时间会提前 2-4 个季度。
3. **Glass core substrate 样品线**：2026 的样品 shipment 数量不大，但客户名单、失效数据、认证周期会决定 2027-2028 市值弹性。
4. **Panel-level RDL/CoPoS**：规模化难，但一旦 TSMC 或 CSP ASIC 锁路线，设备和检测环节会先涨。

## 5. 供给侧：产能结构、瓶颈、成本与价格传导

### 5.1 产能结构

| 地区 | 公司/机构 | 工艺/能力 | 2026 判断 |
|---|---|---|---|
| 美国 | Intel, Absolics, Corning, Onto, KLA, Applied Materials, 3DGS, Amkor Arizona | glass-core design rule、EMIB/advanced packaging、Covington glass substrate、fusion glass、inspection/metrology、材料设备 | 美国在玻璃基板上有政策倾斜，Absolics 是最清晰的本土产能锚。 |
| 韩国 | Samsung Electro-Mechanics, SKC/Absolics, JNTC, LG Innotek, Philoptics, Dongwoo Fine-Chem/Sumitomo JV | FCBGA、glass core pilot、TGV、玻璃/显示加工、设备 | 韩国速度最快，目标在 2027 后建立量产阵地。 |
| 日本 | AGC, DNP, TOPPAN, Kyocera, SCHOTT Japan ecosystem, Sumitomo Chemical, NEG, NGK, Shinko, Ibiden | 玻璃材料、TGV panel、印刷/光刻/精密加工、陶瓷 core、高端基板 | 日本在材料和基板工艺最强，DNP/TOPPAN/AGC/Kyocera 是 2026 新增重点。 |
| 台湾 | TSMC/VisEra, Unimicron, Kinsus, Nan Ya PCB, ITRI, Innolux/AUO 相关能力 | CoWoS/CoPoS、panel-level、ABF、显示面板制造经验 | 2026 仍以 CoWoS/ABF 为主；CoPoS 2027-2029 是关键。 |
| 欧洲 | LPKF, SCHMID, Fraunhofer IZM GPTG, SUSS, EV Group, SCHOTT, ZEISS/光学检测生态 | TGV 成孔、整线 lab、玻璃面板 consortium、bonding/lithography、材料 | 欧洲在工具链和 process IP 上极重要，量产地未必在欧洲。 |
| 中国大陆 | BOE, Visionox, TCL CSOT, JCET, Tongfu, Huatian, Shennan, WUS, 深科技/精测/中科飞测等检测生态 | 显示玻璃/面板制造、OSAT、国产基板、检测替代 | 2026 多为规划/试点，国产 AI 需求提供内需，但高端可靠性认证是瓶颈。 |

### 5.2 供给瓶颈

1. **TGV 成孔质量**：玻璃脆性导致 microcrack、chipping、sidewall roughness；孔径、孔形、pitch、AR 同时收窄后良率难度非线性上升。
2. **TGV 金属化**：ECP 在高 AR 细孔底部均匀性差，paste filling 有 shrinkage/void 风险；热循环后裂纹和电阻漂移是量产杀手。
3. **Panel handling 与 singulation**：510x515mm 或 600x600mm 面板搬运、边缘保护、切割、清洗、临时贴合都可能引入隐性裂纹。
4. **RDL lithography overlay**：玻璃虽低翘曲，但大面板仍有局部 distortion；RDL 2/2um 或更细时需要 feed-forward overlay control。
5. **检测量测吞吐**：HVM 需要 100% panel surface、TGV CD、3D profile、microcrack、void、warpage、RDL defect；检测慢会直接卡产能。
6. **玻璃材料规格**：CTE、TTV、roughness、厚度、低 alkali、化学耐受、热冲击和可加工性必须同时满足，供应商少。
7. **客户认证周期**：高端 AI 封装客户通常需要 9-24 个月可靠性、热循环、湿敏、跌落/振动、SLT、系统级 burn-in 数据。
8. **EDA/PDK 与 design rule**：glass-core 不只是换材料，BGA/LGA、FLI bump、TGV pitch、RDL、embedded passives、thermal model 都要重建。
9. **人才与 process know-how**：它横跨显示玻璃、半导体封装、PCB、光刻、化学镀铜、AOI/3D metrology，单一团队很难快速复制。
10. **量产经济性**：样品可以高价，HVM 必须证明单位面积成本低于 silicon/organic 的组合方案；否则只会留在高端小众。

### 5.3 单位成本拆分

AI-grade glass-core substrate 量产后的长期成本结构估算：

| 成本项 | 成本占比 | 价格/毛利决定因素 |
|---|---:|---|
| 高规格玻璃原片/面板 | 10-20% | CTE/TTV/roughness、panel size、低 alkali、供应商稀缺性。 |
| TGV 成孔/蚀刻/清洗 | 15-25% | via AR、孔径/pitch、裂纹率、throughput、设备折旧。 |
| TGV 金属化/填孔/平坦化 | 20-35% | void-free yield、电阻、热循环可靠性、铜/化学品成本。 |
| RDL/ build-up / lithography | 20-35% | L/S、层数、overlay、材料、SAP/damascene/embedded trace 路线。 |
| 检测量测/电测 | 8-18% | 缺陷密度、100% 检测要求、AI 分类软件、返工流程。 |
| Handling/singulation/edge protection | 5-15% | 面板破片率、物流、防潮/防颗粒、防翘曲夹具。 |
| Yield loss / scrap | 10-40% early，成熟后 5-15% | 初期最大变量；面积越大，单个 killer defect 价值损失越高。 |

价格传导机制：

| 场景 | 传导路径 |
|---|---|
| AI 高端基板紧缺 | 玻璃 core 以“可靠性/供给安全/大面积能力”定价，客户愿意支付 NPI premium 和预付款。 |
| TGV 设备/检测短缺 | 设备商按产线节拍和良率改善收费，软件、recipe、defect library 形成 recurring/service 收入。 |
| 玻璃材料紧缺 | 高端 glass panel 的 TTV/CTE/roughness 溢价传导到基板厂，再传导到 ASIC/GPU package。 |
| 量产良率不足 | 基板厂先吃 scrap；一旦客户急需第二路径，部分成本通过 NRE、样品费、qualification fee 转嫁。 |
| 供给释放过快 | 普通玻璃、低端 TGV、无差异化 panel 先降价；检测、TGV recipe、材料 IP 更抗跌。 |

## 6. 竞争格局与壁垒

### 6.1 市场结构

| 环节 | 2026 集中度判断 | 头部/重点公司 |
|---|---|---|
| 高端 AI ABF/FC-BGA | 高，且已经量产紧缺 | Ibiden、Shinko、Unimicron、Samsung Electro-Mechanics、Kinsus、Nan Ya PCB、AT&S、TOPPAN、Kyocera、LG Innotek |
| Glass raw panel / specialty glass | 高，材料 know-how 形成寡头 | Corning、AGC、SCHOTT、Nippon Electric Glass、HOYA、Ohara、Sumitomo/Dongwoo |
| Glass-core substrate full process | 早期分散，尚无绝对赢家 | Intel、Absolics、Samsung Electro-Mechanics、DNP、TOPPAN、JNTC、LG Innotek、TSMC/VisEra、Rapidus |
| TGV 成孔 | 中高，LPKF 最突出 | LPKF、Philoptics、SCHMID、Mitsubishi/日本激光加工生态、Trumpf、3DGS、AGC/DNP/JNTC 自建 |
| TGV 金属化/电镀/浆料 | 分散，2026 仍在路线竞争 | SCHMID、MKS/Atotech、MacDermid Alpha、Elephantech、Tanaka/DOWA/日本化学品、AnyCasting GSI |
| 检测量测 | 高端集中 | Onto Innovation、KLA、Camtek、Hitachi High-Tech、Nova、Bruker、Keyence、ViTrox、Koh Young、精测电子/中科飞测/华兴源创 |
| Bonding/lithography/panel equipment | 中高 | SUSS、EV Group、ASMPT、Kulicke & Soffa、Besi、DISCO、Tokyo Electron、SCREEN、Manz、SCHMID |

### 6.2 可量化壁垒与“为什么能定价”

| 壁垒 | 量化指标 | 为什么能定价 |
|---|---|---|
| TGV 几何与可靠性 | 5-50um via、10:1-50:1 AR、pitch 50-150um、sidewall Ra、0 microcrack 目标 | via defect 是 package killer defect；客户愿为良率和可靠性买单。 |
| 大面板 overlay | 510x515mm / 600x600mm / 750x620mm，RDL L/S 2/2um 级 | 大面板越大，局部 distortion 越难；软件和检测闭环可锁客户。 |
| 玻璃材料规格 | TTV <0.5-2um、roughness <1nm、CTE 3-10ppm/K、厚度 0.1-1.1mm | 原片不合格会使后续所有工序报废，材料商有前置定价权。 |
| 客户认证 | 9-24 个月 qualification，热循环/湿敏/机械/系统 burn-in | 换供应商意味着重新验证，客户不愿在一代 AI chip 内频繁切换。 |
| 缺陷数据库 | TGV CD、microcrack、void、RDL、warpage、edge chip 数据积累 | 检测不只是硬件，算法和 defect taxonomy 会变成客户锁定。 |
| 资本与学习曲线 | 产线 capex 数亿美元级，pilot 到 HVM 需多轮迭代 | 新进入者即使有玻璃经验，也缺半导体良率和客户数据。 |
| 生态接口 | EMIB/CoWoS/CoPoS/UCIe/HBM/CPO/thermal design rule | 玻璃供应商若进入 design rule 和 EDA flow，就能按平台定价。 |

### 6.3 长期价值捕获

长期高 ROIC/高毛利最可能出现在：

1. **检测量测 + 良率软件**：硬件毛利高，软件和 defect library 更高；客户一旦用某套数据闭环做 HVM，切换成本非常高。
2. **TGV 成孔/金属化 recipe 与设备**：工艺窗口窄，设备、化学品、recipe 和服务绑定，收入早于基板 HVM。
3. **平台型 advanced packaging integrator**：Intel/TSMC/Samsung 若把 glass-core 和 EMIB/CoPoS/turnkey 封装绑定，可收设计、封装、基板和测试多层价值。
4. **高规格玻璃原片**：Corning/AGC/SCHOTT/NEG 有材料 know-how 和规模，但长期毛利可能低于设备/软件。
5. **Full glass-core substrate manufacturer**：成功者会有高毛利，但 capex、良率和客户集中风险也最大；更像高 beta 制造资产。

## 7. 2026 关键变化：三个拐点与最可能放量子方向

### 7.1 三个最可能拐点

1. **玻璃从展示技术进入客户认证技术**  
   Intel EMIB + glass-core 样品、DNP early-2026 sample shipment、Absolics first deliveries/2027 capacity、Samsung-Sumitomo JV after 2027，意味着 2026 是客户 sample、design rule、失效分析和供应链选择年。

2. **检测和 TGV 工艺成为先行收入池**  
   Onto + LPKF、Fraunhofer GPTG、LPKF NEXAR/LIDE、SCHMID full TGV lab、Camtek AI packaging orders 都显示“先买工具、后买量产基板”。玻璃越难，检测越值钱。

3. **AI ASIC 比 merchant GPU 更可能先用玻璃**  
   2026 量产 GPU 已锁 CoWoS/ABF；custom ASIC、switch ASIC、CPO substrate 更愿意尝试新 substrate 来换成本、尺寸和系统功耗。

### 7.2 2026 最可能放量子方向

| 子方向 | 放量逻辑 | 观察指标 |
|---|---|---|
| TGV 成孔设备/服务 | 多条样品线和 pilot 线需要 TGV process | LPKF 是否拿到 production order；韩国/日本/中国 pilot 线设备招标。 |
| TGV 检测量测 | 100% panel 检测是客户认证前提 | Onto Firefly/Dragonfly、KLA、Camtek、ViTrox 等 glass/panel 订单。 |
| TGV 铜金属化材料 | 高 AR void/crack 是 HVM 瓶颈 | Elephantech SAphire G、ECP 化学品、void-free data、热循环数据。 |
| Glass-core sample shipment | DNP/Absolics/Samsung/JNTC 样品进入客户 | 客户名单、样品尺寸、yield、可靠性 fail mode。 |
| 高端 ABF/FC-BGA | 玻璃未量产前，AI 基板真实主线 | Samsung EM、Unimicron、Ibiden、Shinko、AT&S 的 AI substrate revenue 和 capex。 |

## 8. 2027 关键变化：三个拐点与最可能放量子方向

### 8.1 三个最可能拐点

1. **第一批高端 ASIC/switch ASIC glass-core 小批量确认**  
   基准情形下 2027 是小批量和 design-in；乐观情形下 CSP custom ASIC 或 AI switch 把 glass-core 放进量产 BOM。

2. **CoPoS/panel-level 从 pilot 进入 trial production**  
   TSMC/VisEra、Rapidus、Samsung、TOPPAN/DNP 的 panel-level 路线会把 glass substrate 的讨论从“基板材料”变成“先进封装产能结构”。

3. **HBM4/Rubin/MI400/TPU8 放大封装尺寸，倒逼低翘曲路线**  
   2027 若 HBM4 平台按乐观节奏放量，package area 和 power integrity 压力会明显抬高 glass/ceramic core 的战略价值。

### 8.2 2027 最可能放量子方向

| 子方向 | 2027 放量逻辑 | 关键指标 |
|---|---|---|
| Glass-core substrate low volume | 2026 样品通过，2027 小批量 | Absolics capacity kick-in、Samsung JV 主协议、DNP FY2028 前客户进展。 |
| TGV metallization | 成孔后最难的 HVM 工序 | void-free yield、电阻、热循环、plating/paste cycle time。 |
| Inspection software/defect library | 客户需要量产判废规则 | AOI/3D metrology 工具的 repeat orders 和软件 attach rate。 |
| CoPoS/panel-level RDL | 2027 trial run，2028-2029 mass | TSMC pilot line 节点、NVIDIA/custom ASIC 早期客户。 |
| Glass/CPO substrate | 1.6T/3.2T 和 CPO 把光学结构拉进 package | AI switch CPO design win、glass waveguide/V-groove 订单。 |

## 9. 头部公司与细分公司清单

### 9.1 Glass core substrate / glass interposer / panel

| 地区 | 公司 |
|---|---|
| 美国 | Intel、Absolics/SKC、Corning、3D Glass Solutions、Amkor（封装生态）、Applied Materials（材料/设备投资生态） |
| 韩国 | Samsung Electro-Mechanics、SKC/Absolics、JNTC、LG Innotek、Philoptics、Dongwoo Fine-Chem、Samsung Electronics AVP |
| 日本 | AGC、DNP、TOPPAN、Kyocera、Nippon Electric Glass、HOYA、Ohara、Sumitomo Chemical、NGK、Shinko Electric、Ibiden |
| 台湾 | TSMC/VisEra、Unimicron、Kinsus、Nan Ya PCB、Zhen Ding、Innolux/AUO 相关 panel know-how、ITRI |
| 欧洲 | SCHOTT、LPKF/Vitrion、SCHMID、Fraunhofer IZM GPTG、SUSS、EV Group |
| 中国大陆 | BOE、Visionox、TCL CSOT、JCET、Tongfu Microelectronics、Huatian、Shennan Circuits、WUS、深科技、兴森科技及本土玻璃/检测生态 |

### 9.2 TGV 成孔、切割、边缘保护、玻璃加工

| 细分 | 公司 |
|---|---|
| Laser induced deep etching / TGV | LPKF、Philoptics、SCHMID、AGC、DNP、JNTC、3DGS、Trumpf、Coherent、Disco/激光切割生态 |
| Wet etch / cleaning / glass chemistry | SCHMID、SCREEN、Tokyo Electron、MKS/Atotech、MacDermid Alpha、JSR、TOK、Merck、Entegris |
| Singulation / dicing / edge coating | DISCO、LPKF Tensor Ablation、SCHMID、Tokyo Seimitsu、K&S、ASMPT 相关装备 |
| Panel handling / automation | Manz、ASMPT、SUSS、EVG、SCHMID、Applied Materials/自动化生态、RORZE、HIRATA |

### 9.3 TGV 金属化与材料

| 细分 | 公司 |
|---|---|
| Copper plating / ECP / chemistry | MKS/Atotech、MacDermid Alpha、Uyemura、JCU、SCHMID、SCREEN、DOW、Entegris |
| Copper paste / conductive paste | Elephantech、Tanaka、DOWA、Heraeus、Namics、Resonac、DuPont、AnyCasting GSI |
| Build-up/RDL/insulation materials | Ajinomoto、Resonac、Sumitomo Bakelite、Mitsubishi Gas Chemical、Namics、Shin-Etsu、JSR、TOK、DuPont、Nittobo、Nan Ya Plastics、Taiwan Glass |

### 9.4 玻璃检测量测

| 检测对象 | 公司 |
|---|---|
| TGV CD/3D profile/missing via/microcrack | Onto Innovation Firefly/Dragonfly、KLA、Camtek、Keyence、Bruker、Hitachi High-Tech、Nova、ViTrox、Koh Young、CyberOptics/Nordson |
| Glass panel incoming defect/TTV/warpage | Onto PrimaScan/Firefly、KLA、Camtek、Keyence、ZEISS、Olympus/Evident、精测电子、中科飞测 |
| RDL/overlay/bump height | Onto、KLA、Camtek、Nova、FormFactor/MPI 探针、Koh Young、ViTrox |
| X-ray/CT/void inspection | Rigaku + Onto partnership、Nordson DAGE、YXLON/Comet、Nikon Metrology、Waygate、Viscom |
| Electrical test/probe | Teradyne、Advantest、FormFactor、MPI、Cohu、ISC、Yokowo、LEENO |

### 9.5 先进封装平台和客户

| 层级 | 公司 |
|---|---|
| Foundry / advanced packaging | TSMC、Intel Foundry、Samsung Foundry/AVP、ASE、Amkor、JCET、Tongfu、Huatian、Powertech、Nepes |
| AI chip/customer | NVIDIA、AMD、Broadcom、Google TPU、AWS Annapurna、Microsoft Maia、Meta MTIA、OpenAI/Broadcom、Huawei、Cambricon、Alibaba T-Head、Baidu Kunlunxin |
| CPO/photonic ecosystem | Broadcom、NVIDIA/Spectrum-X/CPO、Marvell、Coherent、Lumentum、Ayar Labs、Lightmatter、Celestial AI、Tower/GF silicon photonics、AGC/SCHOTT/LPKF glass photonics |

## 10. 情景化总市场预测

这里用“玻璃/TGV/检测直接相关收入池”口径，不含完整 GPU/ASIC/HBM 销售额。

| 收入池 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观 | 2027 极度超预期 | 2028 基准 | 2028 乐观 | 2028 极度超预期 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Glass-core substrate / samples / low volume | $0.2-0.6B | $0.6-1.5B | $1.5-3.5B | $1-3B | $3-7B | $7-15B | $4-9B | $9-20B | $20-35B |
| TGV equipment/services | $0.6-1.2B | $1.2-2.5B | $2.5-5B | $1.5-4B | $4-8B | $8-15B | $3-7B | $7-15B | $15-28B |
| TGV metallization/materials | $0.2-0.6B | $0.6-1.2B | $1.2-2.5B | $0.8-2B | $2-4.5B | $4.5-9B | $2-5B | $5-11B | $11-20B |
| Glass/panel advanced packaging inspection | $1.8-3.2B | $3.2-5.5B | $5.5-9B | $3-6B | $6-11B | $11-18B | $5-9B | $9-17B | $17-30B |
| Glass interposer / CPO substrate / CoPoS direct glass content | $0.2-0.8B | $0.8-2B | $2-5B | $1-3B | $3-8B | $8-16B | $4-10B | $10-25B | $25-45B |
| 合计 | $3-6.4B | $6.4-12.7B | $12.7-25B | $7.3-18B | $18-38.5B | $38.5-73B | $18-40B | $40-88B | $88-158B |

解释：极度超预期情形相当于假设 OpenAI/Meta/Google/AWS/主权 AI 的 custom ASIC 设计在 2027 前就把玻璃 core、TGV 和 panel-level 路线拉进量产验证，并且客户为了 2028-2029 产能提前买设备和材料。这个情形很乐观，但在 AI capex 持续上修、CoWoS/ABF/HBM 同时紧缺时并非零概率。

## 11. 投资结论与跟踪清单

### 11.1 投资结论

1. **2026 年不要把玻璃基板当作已经大规模替代 ABF 的收入主线。** 主线仍是 ABF/CoWoS/HBM；玻璃是下一代封装期权。
2. **要把 2026 当作玻璃供应链“定标准、定客户、定设备”的一年。** 一旦 TGV 几何、金属化、检测算法和可靠性模型被客户锁定，后续切换成本会很高。
3. **设备与检测优先于基板制造。** LPKF、Onto、KLA、Camtek、SCHMID、SUSS/EVG/ASMPT 等的订单可见性早于 glass substrate HVM。
4. **韩国和日本会是 2027 前最密集的 alpha 区。** Samsung-Sumitomo/Dongwoo、DNP、AGC、TOPPAN、JNTC、Kyocera、SKC/Absolics 的动作比多数地区更具体。
5. **最可能的第一批 AI 玻璃应用不是 GB300，而是 custom ASIC、switch ASIC、CPO substrate、server CPU 或非 NVIDIA 的超大封装。**

### 11.2 未来 6-12 个月跟踪指标

| 指标 | 为什么重要 |
|---|---|
| Absolics 是否披露客户 first deliveries 和 2027 capacity milestones | 美国本土 glass substrate HVM 最关键锚点。 |
| Samsung-Sumitomo JV 是否在 2026 签署主协议并披露 capex/产能 | 韩国玻璃 core 量产时间表会更清晰。 |
| DNP 2026 early sample shipments 的客户反馈 | 日本 TGV glass core 从 pilot 走向 FY2028 HVM 的验证。 |
| LPKF 是否拿到 advanced packaging volume production order | 判断 TGV 成孔是否从验证线进入量产线。 |
| Onto/KLA/Camtek 是否披露 glass/panel/TGV inspection repeat orders | 检测订单是最早的量产前信号。 |
| Elephantech/电镀化学品是否拿到 OSAT/基板厂认证 | TGV 金属化如果被解决，玻璃路线会提前。 |
| Intel Foundry advanced packaging 外部客户 | 若 Google/AWS/Broadcom 类客户采用 EMIB-T/glass path，行业时间表会前移。 |
| TSMC CoPoS pilot/trial 节点 | 决定 glass/panel 机会是 2028 还是 2030。 |
| HBM4/Rubin/MI400/TPU8 package size | 封装越大，玻璃/陶瓷 core 越有战略价值。 |

## 12. 主要来源

### 公司与机构一手资料

- Intel Newsroom, glass substrates announcement: <https://newsroom.intel.com/artificial-intelligence/intel-unveils-industry-leading-glass-substrates>
- Intel Foundry glass-core substrate product brief: <https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2024-08/foundry-glass-core-substrates-pb.pdf>
- Intel Newsroom, glass substrate engineering background: <https://newsroom.intel.com/new-technologies/in-glass-view-future-of-powerful-chips>
- NIST CHIPS, Absolics Georgia award: <https://www.nist.gov/chips/absolics-georgia-covington>
- NIST CHIPS NAPMP, Absolics SMART Packaging Program: <https://www.nist.gov/chips/absolics-inc-covington>
- Samsung Electro-Mechanics Q1 2026 business performance: <https://m.samsungsem.com/global/newsroom/news/view.do?id=10266>
- Samsung Electro-Mechanics CES 2025 CEO press meeting: <https://sem.samsung.com/jp/newsroom/news/view.do?id=8923>
- Samsung Electro-Mechanics + Sumitomo Chemical glass core JV MOU: <https://www.prnewswire.com/news-releases/samsung-electro-mechanics-signs-mou-with-sumitomo-chemical-group-to-establish-a-joint-venture-for-glass-core-used-in-package-substrates-302605068.html>
- DNP TGV glass core substrate pilot line: <https://www.global.dnp/en/news/detail/2025/12/1216_20177773/>
- AGC CES 2026 semiconductor solutions: <https://www.agc.com/en/ces/semiconductor.html>
- AGC TGV product page: <https://www.agc.com/en/products/electoric/detail/tgv.html>
- SCHOTT semiconductor/datacom glass: <https://www.schott.com/en-us/markets/semiconductor-and-datacom>
- SCHOTT advanced IC packaging glass panels: <https://www.schott.com/en-be/markets/semiconductor-and-datacom/advanced-ic-packaging-and-integration>
- Corning TGV substrate technical paper: <https://www.corning.com/content/dam/corning/media/worldwide/global/documents/semi%20Development%20of%20Substrates%20Featuring%20TGV%20and%203D-IC%20Integration.pdf>
- LPKF 2025 results / glass advanced packaging comments: <https://www.lpkf.com/en/news-press/press-releases-teaser/lpkf-reports-slight-improvement-in-earnings-in-2025-and-initiates-group-realignment>
- LPKF LIDE technology: <https://lide.lpkf.com/en/technology/lide>
- LPKF glass advanced packaging solutions: <https://lide.lpkf.com/en/>
- LPKF Q1 2026 earnings call PDF: <https://www.lpkf.com/fileadmin/mediafiles/EARNINGS_Call_Q1_2026.pdf>
- LPKF + Fraunhofer Glass Panel Technology Group: <https://www.lpkf.com/en/news-press/press-releases-teaser/lpkf-delivers-key-strategic-technology-to-fraunhofers-glass-panel-technology-group>
- Onto Innovation Firefly G3: <https://ontoinnovation.com/products/firefly-g3/>
- Onto Innovation TGV process control event: <https://ontoinnovation.com/events/semicon-west/enabling-yield-and-reliability-in-next-gen-hbm-packaging-through-laser-based-glass-carrier-inspection-2/>
- Onto Innovation TGV analysis PDF: <https://ontoinnovation.com/wp-content/uploads/2025/10/Rigorous-Analysis-of-TGVs_SemiDigest_Oct25.pdf>
- KLA advanced packaging process control: <https://www.spts.com/solutions/advancedpackaging>
- Camtek $31M OSAT order / Q1 2026 OSAT orders: <https://www.camtek.com/news-and-events/camtek-receives-31-million-multi-system-order-from-a-leading-osat/>
- JNTC TGV glass substrate launch: <https://www.prnewswire.com/news-releases/jntc-unveils-next-generation-glass-substrate-for-semiconductors-302503956.html>
- LG Innotek advanced package substrate insight: <https://www.lginnotek.com/news/insightsView.do?idx=225&locale=en&rowSize=9>
- LG Innotek CES 2026 glass substrate comments: <https://koreajoongangdaily.joins.com/news/2026-01-11/business/industry/LG-Innotek-positions-physical-AI-expansion-as-core-growth-strategy/2497571>
- Elephantech SAphire G copper nano-paste for TGV: <https://elephantech.com/pdf/pressrelease/Elephantech_2026_0430_en.pdf>
- Kyocera multilayer ceramic core substrate: <https://global.kyocera.com/newsroom/news/2026/001185.html>
- SCHMID full TGV lab / glass cores: <https://www.semiconductorpackagingnews.com/uploads/1/Press_Release_SCHMID_GROUP_TAKES_NEXT_STEP_TOWARDS_ADVANCED_PACKAGING_FOR_INTEGRATED_CIRCUITS_WITH_GLASS_CORES.pdf>

### 行业报告与二手验证

- IDTechEx, Glass in Semiconductors 2026-2036 article: <https://www.idtechex.com/en/research-article/glass-in-semiconductors-the-next-inflection-in-semiconductors/33714>
- IDTechEx report page: <https://www.idtechex.com/en/research-report/glass-in-semiconductors/1117>
- TrendForce, TSMC CoPoS pilot/ramp: <https://www.trendforce.com/news/2026/04/13/news-tsmc-advances-panel-level-packaging-copos-pilot-line-reportedly-set-for-june-completion-2028-29-ramp-eyed/>
- TrendForce, Intel No SeWaRe glass substrates preview: <https://img.trendforce.com/Report/2026/04/20260430_143249_RP260224KD_preview.pdf>
- TrendForce Insights, glass substrates and AI packaging bottleneck: <https://insights.trendforce.com/p/glass-substrate-development>
- Tom's Hardware, Rapidus glass panel-level packaging: <https://www.tomshardware.com/tech-industry/semiconductors/rapidus-explores-panel-level-packaging-on-glass-substrates-for-next-generation-processors-aggressive-plan-would-help-it-leapfrog-rivals>

### 项目内资料

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_AI芯片先进封装_2026.md`
- `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_封装基板_中介层与RDL_2026-05-08.md`
- `D:\drive\Investment\调研\v5\conference_update\chiplet_summit_2026_update.md`
- `D:\drive\Investment\调研\v5\conference_update\designcon_2026_conference_update.md`
# 行业调研：【存储晶圆制造】

> 截至日期：2026-05-08  
> 研究口径：本文把“存储晶圆制造”定义为 AI 数据中心直接拉动的 DRAM/HBM/NAND 前道晶圆制造，以及与其不可分割的 TSV/RDL、logic base die、晶圆探针、KGD、堆叠键合、先进封装、关键材料和测试设备。企业级 SSD、SOCAMM2、CXL 内存等只在它们反向拉动 DRAM/NAND wafer starts 和良率/价格时纳入。  
> 情景口径：未来 3 个月为 2026-05-08 至 2026-08-08；未来 1 年至 2027-05-08；未来 2 年至 2028-05-08。市场规模为全球收入池估算，美元口径，不建议把表格各行简单相加，因 HBM、base die、CoWoS、设备和终端 SSD 之间存在重复价值链。  
> 立场：按用户要求，对 2026-2027 AI 计算中心建设采取偏乐观假设；找不到直接披露的数据时，用 AI 芯片出货、HBM stack 数、晶圆面积、ASP、CapEx 和客户 LTA 进行大胆但可解释的推算。

## 0. 高浓度结论

1. **2026 年存储晶圆制造的核心不是“周期复苏”，而是 AI 把存储晶圆变成算力交付阀门。** Gartner 在 2026-04-08 把 2026 全球半导体收入预测上调到 **1.3202 万亿美元**、2027 到 **1.5545 万亿美元**；其中 memory 从 2025 年 **2163 亿美元**跳到 2026 年 **6333 亿美元**、2027 年 **7481 亿美元**，并预计 2026 DRAM / NAND 年均价格分别上涨 **125% / 234%**，实质性缓解要到 **2027 年底**以后才可能出现。这个口径比 WSTS 2025 秋季预测的 2026 memory **2948 亿美元**大幅上修，说明 2025Q4-2026Q2 的“memflation”已经改变市场锚。
2. **2026 主线产品是 HBM3E 12Hi + DDR5/MRDIMM + 218L-321L QLC/TLC NAND；2026H2 起 HBM4 12Hi 进入真正商业放量。** Samsung 已于 2026-02-12 宣布 HBM4 量产和商业出货，采用 **1c DRAM + 4nm logic base die**，稳定 **11.7Gbps/pin**、最高 **13Gbps/pin**。Micron 在 GTC 2026 宣布 **HBM4 36GB 12H** 已于 2026Q1 量产出货，带宽 **>2.8TB/s/stack**，同时量产 **192GB SOCAMM2** 和 **PCIe Gen6 9650 SSD**。SK hynix 已在 2025-09 宣布完成 HBM4 开发和量产体系，且 2026Q1 公告继续提高 HBM、高容量 server DRAM 与 eSSD 销售。
3. **HBM 的真实供给瓶颈是复合瓶颈：DRAM wafer starts、EUV/1b-1c-1γ 节点、TSV/减薄、TC bonding、underfill、KGD/probe、HBM4 logic base die、CoWoS/interposer、ABF 和客户认证同时约束。** 单看晶圆厂月产能会低估瓶颈；单看先进封装也会低估前道 DRAM 面积损耗。一个 HBM stack 占用的高端 DRAM 晶圆资源远高于普通 DDR5 bit，AI 订单会持续挤出 PC、手机、汽车和工业存储。
4. **利润率最强的 2026 环节是 HBM 成品、先进 DRAM wafer allocation、HBM probe/test、TC bonder、HBM PHY/IP、关键材料；2027 弹性最大的是 HBM4E/cHBM、logic base die foundry、hybrid copper bonding、CXL/LPDDR server memory 和高容量 QLC NAND。** Micron FY2026 Q2 已实现 **238.6 亿美元收入、74.4% GAAP gross margin**，并指引 FY2026 Q3 **335 亿美元收入、约 81% gross margin**，这虽然不是纯 HBM 毛利，但足以证明供不应求下 memory 公司整体毛利可达到平台型硬件区间。
5. **基准情景下，2026 HBM 单品收入池约 520-650 亿美元，2027 到 800-1150 亿美元；极度超预期乐观下，2027 HBM/HBM4E/cHBM 可冲 1700-2400 亿美元。** 若把 AI server DDR5/MRDIMM、SOCAMM2、enterprise QLC/TLC NAND、Gen6 SSD、CXL memory、HBM 相关设备/材料/封装一起看，存储晶圆制造及其直接支撑链在 2026 已是 **数千亿美元级**投资主题。

## 1. 2026 AI 计算中心建设下的机遇、挑战与技术路径

### 1.1 机会

| 机会 | 2026 触发因素 | 对存储晶圆制造的影响 |
|---|---|---|
| HBM 从 GPU 配件变成 AI 平台准入项 | B300/GB300、MI350、TPU Ironwood、Trainium2/3、Maia、MTIA/OpenAI XPU 均需要高带宽近端存储 | HBM3E 12Hi 全年高稼动，HBM4 12Hi 争夺 2027 份额；1b/1c/1γ DRAM wafer、TSV、KGD 和 TC bonder 变成瓶颈资产 |
| 自研 ASIC 分散单一 GPU 风险，但扩大 HBM 总需求 | Google/Broadcom、AWS、Microsoft、Meta/Broadcom、OpenAI/Broadcom 同时放量 | HBM 不再只看 NVIDIA；memory 厂商可通过多客户 LTA 锁定价格和产能 |
| Agentic inference 与长上下文 | KV cache、RAG、checkpoint、embedding、工具调用让内存层级从 HBM 外溢到 DDR5/SOCAMM2/CXL/SSD | DDR5/MRDIMM、SOCAMM2、LPDDR server、Gen6 SSD 与高容量 QLC NAND 获得与 HBM 同方向的 price umbrella |
| Memflation 改变客户采购行为 | 大客户预付、take-or-pay、2026-2027 LTA 锁货 | 厂商从按季度议价转向 allocation 定价；二线客户即使出高价也未必拿到货 |
| 设备与材料升级 | SEMI 预计 2026 全球设备支出 **1430.6 亿美元**、2027 **1593.2 亿美元**，memory 由 AI 需求驱动 | EUV、刻蚀/沉积、HBM bonding、wafer thinning、probe card、underfill、ABF film 和高纯材料订单延长 |

### 1.2 挑战

| 挑战 | 为什么卡行业 | 2026-2027 影响 |
|---|---|---|
| 高端 DRAM 晶圆面积不足 | HBM die 大、KGD 要求高、stack 层数高，等效 bit 供给效率低于普通 DDR5 | HBM 与 DDR5/MRDIMM 相互挤产能，非 AI 终端涨价、降配或延后 |
| 1c / 1γ 节点切换良率 | Samsung HBM4 用 1c，Micron 1γ 是 2026 bit growth 主力，SK hynix 推 1c LPDDR6/SOCAMM2 | 早期良率 5-10pct 差距会决定客户 allocation 和毛利 |
| HBM4 logic base die | HBM4 起 base die 更像逻辑芯片，Samsung 内部 4nm；Micron 已披露 HBM4E 将与 TSMC 合作；SK hynix 依赖外部 foundry 协同 | “memory + foundry + package”能力成为新壁垒，TSMC/Samsung Foundry 重要性上升 |
| 堆叠键合 throughput | 12Hi/16Hi 堆叠、TSV、减薄、MR-MUF/NCF/HCB 工艺节拍慢 | Hanmi、Hanwha、ASMPT、BESI、AMAT/TEL 等设备交期决定 HBM 有效出货 |
| KGD、probe、burn-in | HBM stack 任一 die 失效都会拖累良率，HBM4 I/O 翻倍后测试复杂度上升 | Advantest、Teradyne、FormFactor、Technoprobe 等测试和探针卡环节获得高议价 |
| NAND 高层数/QLC 良率 | 245TB/256TB SSD 需要 2Tb QLC、32-die stack、CBA/wafer bonding 与高可靠固件 | AI 数据湖推动 QLC，但 endurance、WAF 和客户认证周期限制短期放量 |
| 地缘与出口管制 | 中国高端 DRAM/HBM/先进封装设备受限，海外客户也担忧供应链地缘风险 | 国产替代具备长期期权，但 2026 高端 HBM 仍难完全替代三大厂 |

### 1.3 项目已有 AI 芯片路线对存储晶圆的映射

以下 AI 芯片顺序来自项目内 `ai_chip_research_2026_2027.md` 的“2026-2027 出货量/价值权重最大平台”，不重新外搜。

| 排名 | AI 平台 | 2026-2027 出货逻辑 | 对存储晶圆技术路径的直接拉动 |
|---:|---|---|---|
| 1 | NVIDIA B300/GB300 Blackwell Ultra | 2026 高端 GPU 主力 | 每 GPU 最高 **288GB HBM3E**；拉动 HBM3E 12Hi、1b/1c DRAM、CoWoS-L、ABF、KGD |
| 2 | AWS Trainium2 | Project Rainier 和 Anthropic 百万级芯片目标 | 云厂 ASIC 证明 HBM/高端 DRAM 不再只由 NVIDIA 定价；HBM3E 与 DDR5/NAND 数据管线同步紧张 |
| 3 | Google TPU v7 Ironwood | Google Cloud + Anthropic 扩容 | **192GB HBM、7.37TB/s** 级别；推理优先但仍重 HBM |
| 4 | NVIDIA B200/GB200 | 存量订单延续 | HBM3E/CoWoS 继续消耗 2026 wafer 和封装产能 |
| 5 | Huawei Ascend 910C/950 | 中国国产替代主线 | 国产 HBM/高端 DRAM、2.5D 封装、国产测试设备长期期权；2026 仍受先进 DRAM 与封装约束 |
| 6 | Cambricon MLU 590/690 | 2026 中国放量目标 | HBM + 国产集群互连；拉动非美高带宽存储供应链 |
| 7 | AMD MI350 | AMD 2026 最确定放量 | HBM3E、UBB/OAM、2.5D 封装；对 SK/Samsung/Micron allocation 构成边际需求 |
| 8 | AWS Trainium3 | 2026 早期、2027 主力 | 3nm ASIC + HBM3E/后续 HBM4 级内存，验证云厂自研芯片持续吃掉 HBM 产能 |
| 9 | Meta MTIA 300/400/450/500 | Meta 数十万颗存量、Broadcom XPU 扩大 | GenAI inference ASIC 对 HBM、LPDDR server、DDR5 和 NAND 层级同时有需求 |
| 10 | Microsoft Maia 200 | Azure 推理导入 | **216GB HBM3E、7TB/s、272MB SRAM**；HBM3E 进入 hyperscaler 自研芯片标配 |
| 11 | NVIDIA Vera Rubin | 2026H2 初批，2027 主力 | HBM4 12Hi 的最大验证/放量源；SOCAMM2 与 Gen6 SSD 进入 Vera 系统 |
| 12 | AMD MI400/MI455X Helios | 2026H2 初批，2027 放量 | 目标 **432GB HBM4、约 19.6TB/s**，将 HBM4 从 NVIDIA 单点需求扩到第二平台 |

### 1.4 新技术成熟与放量时间

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 | 2026 最可能路径 |
|---|---|---|---|---|
| HBM3E 12Hi | 已成熟，2026 全年主力；2027 被 HBM4 逐步替代 | 2026 供给偏紧、ASP 持续高位 | B300/GB300、MI350、ASIC 全部上修，全年缺货 | **最确定主线** |
| HBM4 12Hi | 2026Q2 完成多家验证，2026H2 小批量，2027 放量 | 2026Q3 三大厂均稳定供货 | 2026Q4 已成高端新增平台默认配置 | **第二主线，2027 主力** |
| HBM4 16Hi | 2026 样品，2027H2 放量 | 2027H1 进入高端训练平台 | 2026Q4 少量进最高端客户 | 2026 看 design-win，不押收入 |
| HBM4E | 2026H2 样品，2027H2 放量 | 2027H1 随 Rubin Ultra/下一代 ASIC 放量 | 2027Q1 即进入部分平台量产 | 2026 是期权，2027 是弹性 |
| cHBM / custom HBM base die | 2027 样品，2028 放量 | 2027H2 OpenAI/Meta/Google/Broadcom 开始批量导入 | 2027Q2 被大客户写入标准采购 | 2026 先看 memory+foundry 联合定义 |
| 1c / 1γ DRAM | 2026 成为 HBM4、LPDDR6、SOCAMM2 和 server DRAM 核心节点 | 2026H2 先进节点良率稳定 | 先进节点 bit growth 覆盖大部分 AI 内存 | 决定 wafer 竞争力 |
| SOCAMM2 / LPDDR5X server | 2026 量产导入 Vera/Rubin，2027 扩散 | 2027 进入更多 CPU/推理 rack | 2027 成为 AI CPU 默认形态之一 | HBM 外第一层高带宽内存 |
| LPDDR6 / DDR6 / MRDIMM Gen2 | 2026 样品/验证，2027-2028 放量 | 2027 高端 AI CPU 和边缘 AI 采用 | 2027H2 服务器低功耗内存大量替代 RDIMM | 2026 主要是节点和 IP 期权 |
| 321L/332L+ QLC NAND | 2026 高容量 SSD 放量，2027 扩张 | Kitakami K2、Micron G9、SK 321L 快速爬坡 | AI warm tier 把 NAND 产能锁到 2028 | 2026 QLC 从数据湖切入 |
| Hybrid copper bonding | 2026 验证，2027-2028 用于 16Hi+ | 2027 高端 HBM4E 采用率快速提升 | 2027 成为 16Hi 高端主流 | 2026 看设备订单和良率 |
| CXL memory / pooled memory | 2026 pilot，2027 production-limited | 2027 多家云公开 SKU | 2027 因 DRAM/HBM 极紧而提前扩张 | 辅助 HBM，不替代 HBM |
| HBF / high bandwidth flash | 2026-2028 标准与研发 | 2028-2029 样品 | 2028 小批量 KV cache | 更偏 2030 前后机会 |

**2026 最可能的实际技术路径：** B300/GB300/MI350/云厂 ASIC 继续吃掉 HBM3E 12Hi 和 server DDR5；Rubin/MI400/TPU8/OpenAI-Broadcom 等高端新增平台在 2026H2 把 HBM4 12Hi 推入商业供货；SOCAMM2 和 Gen6 SSD 成为 Vera/Rubin 体系的外层 memory/storage；NAND 侧以 218L/321L QLC/TLC + 122TB-256TB eSSD 服务 AI 数据湖和 KV/cache warm tier。

## 2. 已经开始放量的关键产品：规模、渗透率、利润率

### 2.1 产品拆分与三情景市场规模

| 已放量产品/技术 | 主要供应商 | 关键状态与证据 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 毛利率情景 |
|---|---|---|---:|---:|---:|---|---|
| HBM3E 8Hi/12Hi | SK hynix、Samsung、Micron | 2026 Blackwell Ultra/MI350/ASIC 主力；TrendForce 指向 HBM3E 仍主导 2026 | B $12-18B / O $18-24B / X $25-32B | B $42-55B / O $55-70B / X $70-90B | B $55-80B / O $80-120B / X $110-160B | 2026 HBM bit 60-70%；2027 降至 35-50% | B 58-70%；O 68-78%；X 75-85% |
| HBM4 12Hi | Samsung、Micron、SK hynix | Samsung 2026-02 商业出货；Micron 2026Q1 volume shipment；SK 已建量产体系 | B $2-6B / O $6-10B / X $10-16B | B $18-32B / O $35-55B / X $60-85B | B $65-105B / O $100-160B / X $150-230B | 2026 8-18%；2027 35-55%；2028 45-65% | B 62-75%；O 72-82%；X 80-88% |
| AI server DDR5 / RDIMM / MRDIMM | 三大 DRAM 厂、Montage、Rambus 生态 | Gartner 指出 DRAM 价格 2026 +125%；TrendForce 指出 DDR5 与 HBM3E 盈利快速收敛 | B $12-22B / O $22-35B / X $35-50B | B $55-95B / O $95-145B / X $145-220B | B $110-190B / O $190-320B / X $320-500B | AI/server DRAM 先进节点收入占比 2026 40-55%，2027 55-70% | B 45-60%；O 58-72%；X 68-80% |
| SOCAMM2 / LPDDR5X server modules | Micron、SK hynix、Samsung | Micron 192GB SOCAMM2 量产；SK hynix 2026-04 量产 192GB SOCAMM2 | B $0.8-2B / O $2-4B / X $4-7B | B $5-12B / O $12-22B / X $22-35B | B $15-35B / O $35-65B / X $65-110B | 2026 AI CPU/Vera 节点 5-15%；2027 20-45%；2028 35-60% | B 45-58%；O 55-68%；X 65-75% |
| GDDR7 / 高带宽分立 DRAM | Samsung、SK hynix、Micron | AI 边缘、工作站、低成本推理和部分 CPX/显示卡使用 | B $1-2B / O $2-3.5B / X $3.5-5B | B $5-9B / O $9-15B / X $15-25B | B $12-25B / O $25-45B / X $45-70B | 高端推理替代/补充，2027 在非 HBM AI 加速器中 10-20% | B 35-50%；O 45-60%；X 55-70% |
| 3D NAND TLC/QLC wafer for enterprise SSD | Samsung、Kioxia/SanDisk、SK hynix/Solidigm、Micron、YMTC | Kioxia LC9 245.76TB、Micron 6600 ION 245TB、SanDisk UltraQLC 256TB、SK 321L QLC | B $3-7B / O $7-12B / X $12-18B | B $20-40B / O $40-70B / X $70-110B | B $45-90B / O $90-160B / X $160-260B | AI warm NVMe PB 占比 2026 8-15%；2027 18-30%；2028 30-45% | B 30-50%；O 45-60%；X 55-70% |
| PCIe Gen6 data center SSD | Micron、Samsung、Kioxia、controller 生态 | Micron 9650 Gen6 量产，最高 **28GB/s** 顺序读、**5.5M IOPS**；Samsung PM1763 进入高端路径 | B $0.4-1B / O $1-2B / X $2-4B | B $3-7B / O $7-13B / X $12-22B | B $10-22B / O $22-38B / X $36-60B | 2026 高端 AI eSSD 3-8%；2027 15-30%；2028 30-50% | B 38-55%；O 48-65%；X 58-72% |
| HBM probe/test/KGD/TC bonding 设备 | Advantest、Teradyne、FormFactor、Technoprobe、Hanmi、Hanwha、ASMPT、BESI、AMAT、TEL | HBM4 I/O 翻倍、16Hi 堆叠和 KGD 需求上升；SK/AMAT 已宣布长期 AI memory R&D | B $1-3B / O $3-5B / X $5-8B | B $8-18B / O $18-32B / X $32-50B | B $22-50B / O $50-95B / X $95-150B | 新增 HBM 产线绑定率接近 100% | B 42-60%；O 55-70%；X 65-78% |
| HBM base die / CoWoS / interposer / ABF | Samsung Foundry、TSMC、Intel、ASE、Amkor、Ibiden、Shinko、Unimicron、Nan Ya、AT&S | HBM4 起 logic base die 和 2.5D 封装成为有效出货阀门 | B $3-6B / O $6-10B / X $10-16B | B $18-35B / O $35-60B / X $60-95B | B $45-95B / O $95-170B / X $170-280B | 高端 AI 加速器 2026 80%+ 依赖先进封装 | B 30-48%；O 42-58%；X 55-68% |

### 2.2 增长预测区间

| 产品 | 基准增长 | 乐观增长 | 极度超预期乐观增长 | 主驱动 |
|---|---:|---:|---:|---|
| HBM3E 12Hi | 2026 +45-65%，2027 -10% 至 +20% | 2026 +60-85%，2027 +10-35% | 2026 +90-120%，2027 +25-50% | GB300/B300、MI350、ASIC 继续消化 |
| HBM4 12Hi | 2026 从低基数到 $20B+，2027 +150-250% | 2027 +180-300% | 2027 +220-350% | Rubin/MI400/TPU8/ASIC 同步导入 |
| DDR5/MRDIMM | 2026 收入 +80-130% | +130-200% | +200-300% | 价格上涨 + server content 增加 |
| SOCAMM2 | 2026 从接近零到 $5B+，2027 +80-150% | 2027 +120-220% | 2027 +200-320% | Vera CPU、AI CPU、推理内存池 |
| AI QLC/TLC NAND | 2026 +70-120% | +120-200% | +200-320% | 数据湖、RAG、checkpoint、warm tier |
| Gen6 SSD | 2026 小基数高增，2027 +200-350% | 2027 +300-500% | 2027 +500%+ | Rubin/BlueField-4 STX/CMX、高端 inference rack |
| HBM test/bonding equipment | 2026 +60-110% | +100-180% | +180-300% | HBM4/16Hi/hybrid bonding 产线扩建 |

## 3. 在研关键产品和高增长技术

| 在研/早期导入技术 | 代表公司 | 成熟时间 | 放量时间 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率/利润率判断 |
|---|---|---|---|---:|---:|---:|---|
| HBM4 16Hi 48GB | Micron、SK hynix、Samsung | 2026 样品/客户验证 | 2027H1-H2 | B <$0.5B / O $0.5-1B / X $1-2B | B $4-10B / O $10-20B / X $20-35B | B $25-70B / O $70-120B / X $120-190B | 2027 高端 HBM placement 10-25%；GM 65-88% |
| HBM4E | Samsung、Micron、SK hynix | 2026H2 样品 | 2027H2，乐观 2027H1 | B $0.2-0.8B / O $0.8-1.5B / X $1.5-3B | B $4-12B / O $12-25B / X $25-45B | B $35-90B / O $90-170B / X $170-280B | Rubin Ultra/MI500/ASIC；GM 70-90% |
| cHBM / custom base die | Samsung、SK hynix+TSMC、Micron+TSMC、Broadcom/Google/Meta/OpenAI 生态 | 2026 联合定义 | 2027H2-2028 | B $0.1-0.5B / O $0.5-1B / X $1-2B | B $2-6B / O $6-15B / X $15-30B | B $18-55B / O $55-120B / X $120-220B | 初期 NRE+premium；IP/设计服务 70-90%，成品 65-85% |
| Hybrid copper bonding for HBM | BESI、ASMPT、SUSS、AMAT、TEL、Samsung/SK/Micron | 2026 验证 | 2027-2028 | B $0.2-0.6B / O $0.6-1.2B / X $1.2-2B | B $1.5-4B / O $4-8B / X $8-14B | B $6-18B / O $18-40B / X $40-75B | 16Hi/更薄 die 驱动；设备 GM 45-70% |
| LPDDR6 / SOCAMM3 / server LPDRAM | SK hynix、Micron、Samsung、JEDEC/IP 生态 | 2026 验证 | 2027-2028 | B $0.2-0.8B / O $0.8-1.5B / X $1.5-3B | B $3-8B / O $8-18B / X $18-35B | B $12-40B / O $40-85B / X $85-150B | AI CPU/Vera 后续平台；GM 45-75% |
| CXL memory expansion/pooling | Samsung、Micron、Montage、Astera、Rambus、Marvell、Microchip | 2026 pilot | 2027 production-limited | B $0.4-0.8B / O $0.8-1.4B / X $1.4-2B | B $2-4.5B / O $4-7B / X $7-10B | B $6-12B / O $12-22B / X $22-35B | 2027 高内存 AI server 3-8% attach；controller GM 65-78% |
| 332L/400L+ NAND、512TB SSD | Kioxia/SanDisk、Samsung、Micron、SK hynix/Solidigm、YMTC | 2026 样品/产线准备 | 2027-2028 | B <$0.5B / O $0.5-1B / X $1-2B | B $2-6B / O $6-14B / X $14-25B | B $15-45B / O $45-90B / X $90-160B | AI warm SSD PB 2028 5-15%；early GM 45-70% |
| HBF / high bandwidth flash | SanDisk、SK hynix、Kioxia、controller/IP 生态 | 2026-2028 标准/研发 | 2028+ | 接近 0 | B <$0.5B / O $0.5-1B / X $1-2B | B $1-5B / O $5-12B / X $12-25B | 2030 前后更大；若 KV cache 落地 GM 50-75% |
| 3D DRAM / vertical DRAM / 4F2 cell | Samsung、SK hynix、Micron、imec、TEL/AMAT/Lam/KLA 生态 | 2027-2029 工艺验证 | 2029+ | 研发/NRE | B $0.2-1B / O $1-2B / X $2-4B | B $3-10B / O $10-25B / X $25-50B | 长期替代平面 DRAM 缩放；设备/材料期权最强 |
| 国产 HBM/高端 DRAM 替代 | CXMT、YMTC、Huawei 生态、JCET、Tongfu、国内设备材料 | 2026-2027 小批验证 | 2028+ 更大规模 | B <$0.5B / O $0.5-1B / X $1-2B | B $1-4B / O $4-10B / X $10-20B | B $6-20B / O $20-50B / X $50-100B | 受设备/良率/认证约束；国产溢价但不确定性高 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 关键工艺/能力 | 2026-2027 判断 |
|---|---|---|---|---|
| 先进 DRAM wafer | 韩国、美国、日本、台湾、中国大陆 | Samsung、SK hynix、Micron、CXMT、Nanya、Winbond | 1b/1c/1γ、EUV 多层、DDR5/HBM die、LPDDR5X/6 | 高端份额集中在三大厂；中国先进 DRAM 具长期替代期权 |
| HBM DRAM die + TSV | 韩国、美国/日本、台湾后道 | SK hynix、Samsung、Micron | HBM3E/4 DRAM die、TSV、wafer thinning、microbump | 2026 三大厂几乎锁定高端供给 |
| HBM logic base die | 韩国、台湾、美国 | Samsung Foundry、TSMC、潜在 Intel Foundry | HBM4 起 4nm/12nm/先进逻辑 base die、PDN、PHY | Samsung 一体化优势增强；Micron/SK 需外部 foundry 协同 |
| HBM stacking/package | 韩国、台湾、马来西亚/东南亚、日本 | 三大内存厂、ASE、Amkor、PTI、JCET、Tongfu、Hana Micron | TC bonding、MR-MUF、TC-NCF、hybrid bonding、underfill | 设备节拍和良率是隐性瓶颈 |
| 3D NAND wafer | 韩国、日本、中国、新加坡、美国 | Samsung、Kioxia/SanDisk、SK hynix/Solidigm、Micron、YMTC | 176L-321L+ TLC/QLC、CBA/wafer bonding、Xtacking、G9 NAND | AI 数据湖让 QLC 从低价产品变成产能紧缺品 |
| Wafer equipment | 荷兰、日本、美国、韩国 | ASML、AMAT、Lam、TEL、KLA、ASM、SCREEN、EBARA、DISCO、Accretech | EUV/DUV、etch、deposition、CMP、metrology、thinning | ASML 2026 指引收入 **360-400 亿欧元**，客户加速扩产 |
| Probe/test/KGD | 日本、美国、台湾、韩国、欧洲 | Advantest、Teradyne、FormFactor、Technoprobe、JEM、MPI、Cohu、Chroma | 高速 probe、burn-in、probe card、HBM KGD | HBM4 与 16Hi 让测试时间和探针卡复杂度上升 |
| 材料 | 日本、美国、欧洲、台湾、韩国 | Shin-Etsu、SUMCO、GlobalWafers、Siltronic、JSR、TOK、Fujifilm、Merck/EMD、Entegris、Resonac、Ajinomoto、Namics、Henkel、DuPont、Dow | wafer、photoresist、CMP slurry、wet chemicals、underfill、ABF film、specialty gases | 小材料占 BOM 低但失效成本高，认证后定价力强 |

### 4.2 关键供给瓶颈

1. **先进 DRAM wafer starts：** HBM 抢占 1b/1c/1γ 产能；普通 DDR5、LPDDR、GDDR 也受益涨价，厂商必须在高毛利产品之间分配 wafer。
2. **EUV 与 cleanroom：** SK hynix Yongin 第一座 fab 总投资约 **31 万亿韩元**，首个 cleanroom 提前到 **2027 年 2 月**；但 cleanroom 和设备导入无法在 3-6 个月内快速释放。
3. **HBM4 base die：** Samsung 用自家 4nm logic base die，Micron HBM4E 已披露与 TSMC 合作；base die 供应链会把 HBM 从纯 memory 竞争推向 foundry-memory 绑定。
4. **TSV/减薄/堆叠：** 12Hi/16Hi 对 die 厚度、翘曲、热阻、underfill、reflow stress 要求更高，bonding 设备 throughput 成为产能上限。
5. **KGD 和测试：** HBM stack 是多 die 串联良率问题，wafer-level high-speed probe、burn-in 和 final test 时间增加。
6. **CoWoS/interposer/ABF：** HBM 出货不等于 GPU/ASIC 可交付，xPU+HBM 还要排先进封装队列。
7. **NAND 2Tb QLC 和高容量 SSD 认证：** Kioxia/SanDisk Kitakami Fab2 2025-09 开始运营、2026H1 有意义产出，但 245TB/256TB SSD 仍受 QLC endurance、32-die stack、控制器和客户 fleet 认证限制。
8. **客户认证与 LTA：** NVIDIA/AMD/Google/AWS/Microsoft/Broadcom 认证后才可大规模供货；大客户预付款和长期协议让未认证产能无法等价替代。
9. **人才：** HBM 是 DRAM、logic、thermal、package、SI/PI、test 的跨学科工程，韩国、美国、日本和台湾的人才短缺会限制 ramp 速度。
10. **地缘与出口管制：** 对中国高端 DRAM/HBM 和先进封装设备的限制，会让国产 AI 芯片扩产的内存路径更不确定。

### 4.3 成本构成与毛利决定因素

| 产品 | 成本拆分估算 | 毛利决定因素 |
|---|---|---|
| HBM3E/4 stack | DRAM die wafer 35-45%；logic/base die 8-15%；TSV/RDL/microbump 10-15%；stacking/bonding/underfill 12-18%；probe/KGD/test 8-15%；interposer/substrate allocation 5-10%；隐含良率损失 10-25% | 良率、客户认证、HBM generation、stack 层数、allocation、base die 供应、CoWoS 排队 |
| Server DDR5/MRDIMM | DRAM wafer/折旧 45-60%；封装测试 10-15%；module PCB/PMIC/SPD/thermal 10-20%；验证/质保/库存 8-15% | 合约价、容量颗粒、RDIMM/MRDIMM premium、客户 LTA、节点良率 |
| SOCAMM2/LPDRAM module | LPDDR die 45-60%；module/连接器/基板 15-25%；测试认证 10-18%；热设计/机械 5-10% | Vera/AI CPU attach、低功耗 premium、标准化速度、可维护性 |
| QLC/TLC enterprise SSD | NAND 55-78%；controller/PHY 3-15%；DRAM/PLP/PMIC 5-12%；PCB/connector/thermal 4-8%；firmware/test/warranty 8-18% | NAND 合约价、QLC 良率、endurance、OCP/FDP、容量 premium、客户认证 |
| HBM test/bonding equipment | 精密机械/光学/电子部件 35-50%；软件/控制 15-25%；服务/安装 10-20%；R&D 摊销 10-20% | 客户锁定、吞吐量、良率改善、装机基数、升级服务 |
| 关键材料 | 原材料/纯化 30-50%；配方和质量体系 20-35%；客户认证 10-20%；物流/库存 5-10% | 认证周期、失效成本、供应稳定、替代难度 |

### 4.4 价格传导机制

| 上游变化 | 传导路径 | 谁最能留住利润 |
|---|---|---|
| DRAM/HBM wafer 紧缺 | HBM/DDR5 合约价季度重定价，大客户通过 LTA 锁量但接受高 ASP | 已认证 HBM 供应商、先进 DRAM 产能拥有者 |
| HBM4 良率低于预期 | 可交付 stack 减少，GPU/ASIC 客户为交期支付 premium | 良率领先者、KGD/test、probe card、TC bonder |
| CoWoS/ABF 瓶颈 | xPU 可交付量下降，封装和基板分配被写入整机交付条款 | TSMC/先进封装、ABF 龙头、高端材料 |
| NAND 合约价上涨 | SSD ASP 跟涨，尤其 122TB-256TB 高容量盘 | NAND+SSD 一体化厂、已进 hyperscaler AVL 的 QLC 产品 |
| Gen6 SSD/controller 稀缺 | 高端 inference rack 为低延迟和带宽支付 premium | 控制器/IP/fabric silicon、系统级 storage 软件 |
| 设备交期延长 | 产能扩张推迟，二手/升级和服务价值上升 | ASML、AMAT/Lam/TEL、KLA、Advantest、Hanmi/Hanwha/BESI |

## 5. 竞争格局与壁垒：可量化判断

### 5.1 市场结构

| 细分 | 集中度判断 | 头部公司 | 2026 变化 |
|---|---|---|---|
| DRAM/HBM 成品 | DRAM CR3 约 95%+；HBM 近乎三寡头 | SK hynix、Samsung、Micron | SK 仍大概率 HBM 份额第一；Samsung 通过 HBM4 快速追赶；Micron 以 HBM4/1γ/美国供应链提高份额 |
| HBM4 for NVIDIA/Rubin | 三家都争取认证 | Samsung、Micron、SK hynix | TrendForce 预计三家 2026Q2 前后进入/完成 NVIDIA HBM4 验证格局 |
| NAND wafer | CR5 约 90%+ | Samsung、Kioxia/SanDisk、SK hynix/Solidigm、Micron、YMTC | AI QLC/eSSD 提高 SK/Solidigm、Micron、Kioxia/SanDisk 的数据中心权重 |
| EUV lithography | 几乎单一供应 | ASML | DRAM 先进节点 EUV 层数增加，memory 客户订货变强 |
| Etch/deposition/CMP | 高集中 | Lam、AMAT、TEL、ASM、SCREEN、EBARA | DRAM/HBM 与 3D NAND 层数上升提高工艺强度 |
| HBM bonding | 头部集中但多路线 | Hanmi、Hanwha、ASMPT、BESI、SUSS、AMAT、TEL | TC bonding 到 hybrid bonding 的代际切换带来替换周期 |
| Probe/test | 高端集中 | Advantest、Teradyne、FormFactor、Technoprobe、JEM、MPI | HBM4 和 Gen6 SSD 增加测试复杂度 |
| HBM IP/EDA | 高集中、轻资产 | Rambus、Synopsys、Cadence、Siemens EDA | HBM4/4E、D2D、SI/PI/thermal signoff 提高 license/NRE |
| Advanced packaging / ABF | 头部强，产能重 | TSMC、Samsung、Intel、ASE、Amkor、Ibiden、Shinko、Unimicron、Nan Ya、AT&S | 先进封装成为 HBM 有效需求的第二阀门 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 量化/验证方式 | 为什么能定价 |
|---|---|---|
| 技术壁垒 | HBM 12Hi/16Hi、2048-bit HBM4、1c/1γ、TSV、warpage、thermal、PDN | 良率差 5-10pct 就会造成可交付 bit 和毛利巨大差异，客户愿为稳定供货付 premium |
| 规模壁垒 | 单座先进 memory fab/cleanroom+设备常为百亿美元级；SK Yongin 首 fab 建设总投资约 31 万亿韩元 | 小厂无法承担跨周期 capex 和客户违约风险 |
| 客户认证 | NVIDIA/AMD/Google/AWS/Microsoft/Broadcom 平台认证通常 6-18 个月，且涉及 SI/PI/thermal/test | 一旦进入 AVL 和平台 reference design，切换成本高且会拖慢 GPU/ASIC 上市 |
| 供应链整合 | HBM 需要 memory、foundry、package、substrate、test 同步 | 能掌握完整链条的公司可按“交付确定性”定价，而不是按成本加成 |
| 材料认证 | photoresist、CMP slurry、underfill、ABF film、gas/chemicals 需长周期认证 | 小材料失效会毁掉大价值芯片，客户不愿轻易替换 |
| 设备认证 | TC bonder、probe card、ATE、EUV/etch/deposition tool 一旦导入产线，很难快速更换 | 设备商可通过升级、服务、耗材和下一代工艺绑定长期 ROIC |
| LTA 和预付款 | 大客户 2026-2027 锁 supply，take-or-pay 或预付 | 新客户即使高价也不一定获得 allocation，现有供应商掌握稀缺权 |
| IP/专利 | HBM PHY/controller、memory training、DFT/KGD、封装热机械模型 | 每一代标准升级都要重新授权和验证，IP 毛利接近软件 |

### 5.3 价值链长期高 ROIC / 高毛利层

| 层级 | 2026 毛利/ROIC 判断 | 长期质量 | 原因 |
|---|---|---|---|
| HBM 成品供应商 | 2026-2027 利润池最大 | 高但周期性仍在 | 供不应求时产品毛利 60-80%+，但 capex 重且未来可能过度扩产 |
| HBM PHY/IP/EDA | 毛利最高 | 极高 | 低 BOM 占比、高失败成本、客户锁定、每代标准升级重购 |
| Test/probe/TC bonder/hybrid bonding 设备 | 高 ROIC | 高 | 认证设备切换难，工艺迭代带来换机周期 |
| 关键材料 | 高 ROIC | 高 | 小金额、大风险、认证后粘性强 |
| Logic base die / advanced foundry | 中高毛利 | 高 | HBM4 后 base die 成为差异化核心，Samsung/TSMC 最受益 |
| CoWoS/advanced packaging | 中高毛利 | 中高 | 需求强，但 capex 重、客户议价强 |
| ABF/基板 | 中高毛利 | 中 | 大尺寸/低翘曲壁垒高，但周期性强 |
| SSD 整盘 | 分化 | 中 | 高容量 QLC 盘有 premium；普通盘仍受 NAND 周期压制 |
| 模组/普通封测代工 | 较低 | 中低 | 若无专利、认证、固件或客户平台绑定，容易被压价 |

## 6. 2026 关键变化：最可能发生的 3 个拐点

### 拐点一：HBM3E 全年紧缺，HBM4 从样品叙事转为商业出货

2026 上半年仍由 HBM3E 12Hi 承担 B300/GB300、MI350、Ironwood、Trainium、Maia、MTIA 等主力需求；Samsung 和 Micron 已分别披露 HBM4 商业/量产出货，SK hynix 已建立 HBM4 量产体系。2026 的关键不是谁先宣布，而是谁能拿到最大 **bit allocation + good die yield + platform qualification**。

### 拐点二：memflation 外溢到 DDR5、SOCAMM2 和 NAND

Gartner 的 DRAM/NAND 价格预测和 Micron 的 81% gross margin 指引，意味着 2026 存储已经不是传统 PC/手机周期。DDR5/MRDIMM、SOCAMM2 和高容量 QLC SSD 从“配套件”升级为 AI factory 的系统预算项；客户会为了 GPU 利用率、token/s 和数据管线确定性支付溢价。

### 拐点三：新建产能已启动，但 2026 实际增量仍被工艺和认证吃掉

SK hynix Yongin 加速到 2027-02 首个 cleanroom，Kioxia/SanDisk Kitakami Fab2 2026H1 有意义产出，Micron 美国扩张和日本/台湾节点迁移继续推进，ASML 指出客户加速 2026 及以后扩产。但对 2026 来说，新增 shell 不是新增合格 HBM4，真正瓶颈仍是设备导入、良率爬坡、KGD 和客户认证。

## 7. 2027 关键变化：最可能发生的 3 个拐点

### 拐点一：HBM4/HBM4E 成为高端新增平台主流

Rubin、Rubin Ultra、MI400/MI500、TPU8、Trainium4、Meta/OpenAI/Broadcom ASIC 会把 HBM4 和 HBM4E 推到新增高端平台核心位置。基准情景下 2027 HBM4/HBM4E 收入可达 **800 亿美元+**；乐观情景 **1500 亿美元+**；极度超预期乐观情景 **2200 亿美元+**。

### 拐点二：竞争从 memory process 转向 foundry + memory + package 联合设计

HBM4 起 logic base die 重要性上升，cHBM 进一步要求客户定制 base die、接口、电源、热和测试。Samsung 的一体化模式、SK hynix + TSMC 模式、Micron + TSMC/美国供应链模式会形成三种竞争结构。2027 起，谁越早参与大客户架构定义，谁越能获得溢价和锁定份额。

### 拐点三：NAND 和 CXL/SOCAMM 进入 AI memory hierarchy

2027 高端推理 rack 不只看 HBM。SOCAMM2/LPDDR server、MRDIMM、CXL memory、Gen6 SSD、高容量 QLC SSD 和早期 HBF/near-memory offload 会形成分层：HBM 保证近端带宽，DDR/SOCAMM/CXL 承担容量和 CPU 侧内存，QLC/Gen6 SSD 承担 warm KV/cache、RAG、checkpoint 和数据湖。存储晶圆制造会从“卖 bit”向“卖 AI memory hierarchy 的交付确定性”升级。

## 8. 头部公司与细分技术全景清单

### 8.1 DRAM / HBM / 高带宽内存

| 细分 | 公司 | 优势 |
|---|---|---|
| HBM3E/HBM4 | SK hynix | HBM 份额和客户关系领先，MR-MUF，HBM4 量产体系，Cheongju/M15X/P&T7/Yongin 扩产 |
| HBM4/HBM4E/cHBM | Samsung Electronics | 1c DRAM、4nm logic base die、memory+foundry+packaging 一体化，HBM4 早期商业出货 |
| HBM4/SOCAMM2/Gen6 SSD | Micron | 1γ DRAM、HBM4 36GB 12H volume shipment、16H samples、美国供应链、SOCAMM2 与 SSD 组合 |
| 高端/国产 DRAM | CXMT、Nanya、Winbond、Etron、ISSI | 中国替代、specialty DRAM、legacy/server 辅助供给 |
| GDDR7/LPDDR | Samsung、SK hynix、Micron | AI 边缘、GPU、server LPDRAM 和低功耗内存 |

### 8.2 NAND / SSD / 控制器

| 细分 | 公司 | 优势 |
|---|---|---|
| NAND wafer | Samsung、Kioxia/SanDisk、SK hynix/Solidigm、Micron、YMTC | 全球 NAND 主产能；AI 高容量 QLC/TLC 供给核心 |
| 高容量 QLC eSSD | Solidigm、Kioxia、Micron、SanDisk、Samsung | 122TB-256TB 产品、AI data lake、warm tier |
| Gen6 / performance eSSD | Micron、Samsung、Kioxia、Solidigm、Phison | 高带宽/低延迟，面向 AI inference、checkpoint、context storage |
| SSD controller | Silicon Motion、Phison、Microchip、Marvell、FADU、InnoGrit、Maxio、DapuStor、ScaleFlux | PCIe Gen5/6 PHY、NVMe/OCP/FDP/ZNS、firmware 和客户认证 |
| Storage fabric / CXL | Astera Labs、Broadcom、Marvell、Microchip、Montage、Rambus、XConn、Credo | PCIe/CXL retimer、switch、memory expander、fabric |

### 8.3 Foundry / advanced packaging / substrate

| 细分 | 公司 | 优势 |
|---|---|---|
| HBM base die / foundry | Samsung Foundry、TSMC、Intel Foundry | HBM4 logic base die、先进节点、客户联合设计 |
| CoWoS/2.5D/advanced packaging | TSMC、Samsung、Intel、ASE、Amkor、PTI、JCET、Tongfu、Huatian、Hana Micron | xPU+HBM 有效交付瓶颈 |
| ABF/BT substrate | Ibiden、Shinko、Unimicron、Nan Ya PCB、Kinsus、Samsung Electro-Mechanics、AT&S、LG Innotek、Daeduck | 大尺寸、低翘曲、高层数基板 |

### 8.4 前道设备、后道设备、测试

| 环节 | 公司 |
|---|---|
| EUV/DUV lithography | ASML、Canon、Nikon |
| Etch/deposition/CMP/clean | Applied Materials、Lam Research、Tokyo Electron、ASM International、SCREEN、EBARA、SEMES、Wonik IPS、Jusung、PSK |
| Metrology/inspection | KLA、Hitachi High-Tech、Onto Innovation、Nova、Camtek、Lasertec、ASML metrology |
| Wafer thinning/dicing/grinding | DISCO、Tokyo Seimitsu/Accretech |
| TC bonder / hybrid bonding | Hanmi Semiconductor、Hanwha Semitech、ASMPT、BESI、SUSS MicroTec、Kulicke & Soffa、Applied Materials、TEL |
| ATE / burn-in | Advantest、Teradyne、Cohu、Chroma、UniTest |
| Probe card | FormFactor、Technoprobe、Japan Electronic Materials、MPI、Microfriend、TSE、Will Technology |
| EDA/IP/test IP | Synopsys、Cadence、Siemens EDA、Rambus、Alphawave、GUC、Alchip、Faraday |

### 8.5 材料

| 材料 | 公司 |
|---|---|
| Silicon wafer | Shin-Etsu Handotai、SUMCO、GlobalWafers、Siltronic、SK Siltron |
| Photoresist / chemicals | JSR、TOK、Fujifilm、DuPont、Merck/EMD、Shin-Etsu Chemical、Dongjin Semichem、Soulbrain |
| CMP slurry/pad | Entegris、Fujifilm、DuPont、Resonac、Merck、Cabot |
| Gases | Air Liquide、Linde、Air Products、Taiyo Nippon Sanso、SK Materials |
| Underfill / molding / adhesives | Namics、Resonac、Henkel、Dow、Shin-Etsu、Panasonic Industry |
| ABF film / substrate materials | Ajinomoto、Resonac、Panasonic、Mitsubishi Gas Chemical、Taiyo Ink |
| Photomask / mask blank | Toppan、DNP、Photronics、Hoya、AGC、Lasertec |

### 8.6 中国及国产替代相关

| 细分 | 公司 |
|---|---|
| DRAM/NAND | CXMT、YMTC、GigaDevice、Winbond/Nanya 在部分供应链中的替代参考 |
| AI 芯片客户 | Huawei/HiSilicon、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Iluvatar、Moore Threads、Enflame、MetaX、Hygon |
| 封测/基板 | JCET、Tongfu Microelectronics、Huatian、Shennan Circuits、Zhuhai ACCESS、Fastprint |
| 设备材料 | Naura、AMEC、Piotech、ACM Research、Hwatsing、Kingsemi、SMEE、Anji、Nata、Sinyang、Jiangfeng、Yoke |
| 控制器/模组/SSD | Maxio、DapuStor、Longsys、BIWIN、Netac、Montage、InnoGrit |

## 9. 投资观察框架

### 9.1 2026 最确定方向

| 排名 | 方向 | 理由 | 验证指标 |
|---:|---|---|---|
| 1 | HBM3E 12Hi 份额与 ASP | GB300/B300/MI350/ASIC 全年主力 | 三大厂 HBM revenue、NVIDIA/AMD/ASIC allocation、HBM3E 合约价 |
| 2 | HBM4 12Hi 认证与良率 | 2027 主平台前置采购 | Rubin/MI400/TPU8 qualification、yield、客户公告 |
| 3 | HBM test/probe/TC bonding | 所有 HBM generation 都绕不开 | Advantest/Teradyne/FormFactor/Hanmi/Hanwha/BESI 订单和交期 |
| 4 | SOCAMM2/DDR5/MRDIMM | AI memory hierarchy 从 HBM 外溢 | Vera CPU/SOCAMM2 attach、server DRAM 价格、LPDDR6 进展 |
| 5 | 高容量 QLC NAND/eSSD | AI 数据湖和 warm tier 从 HDD 转向 SSD+HDD 分层 | 122TB/245TB/256TB 出货、NAND 合约价、hyperscaler LTA |

### 9.2 2027 最大弹性

| 方向 | 为什么弹性大 | 风险 |
|---|---|---|
| HBM4E/cHBM | 下一代 GPU/ASIC 共同需求，custom base die 提高溢价 | 标准化、良率、TSMC/Samsung foundry 排产 |
| Hybrid copper bonding | 16Hi+ 与更薄 die 的关键工艺 | 量产节拍、成本、客户路线选择 |
| CXL/SOCAMM/LPDDR6 server memory | 推理容量和功耗约束增强 | 软件栈、NUMA/tiering、客户 SLA |
| 332L/400L+ QLC NAND | 512TB/1PB SSD 和 AI 数据湖 | QLC endurance、PLC 经济性、HDD 价格竞争 |
| 国产 HBM/DRAM 替代 | 中国 AI 芯片需求确定但供应受限 | 设备限制、良率、认证、生态 |

## 10. 主要来源与交叉验证

- [Gartner：2026 全球半导体收入超过 1.3 万亿美元，memory 6333 亿美元，DRAM/NAND 价格 +125%/+234%](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- [Micron：HBM4 36GB 12H、SOCAMM2、PCIe Gen6 SSD 量产，面向 NVIDIA Vera Rubin](https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin)
- [Micron FY2026 Q2：238.6 亿美元收入、Q3 指引 335 亿美元收入与约 81% gross margin](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026)
- [Samsung：HBM4 量产和商业出货，1c DRAM + 4nm logic base die，11.7Gbps/pin](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)
- [SK hynix：完成 HBM4 开发并建立量产体系](https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/)
- [SK hynix：Yongin Semiconductor Cluster 新设施投资，首 cleanroom 提前至 2027-02](https://news.skhynix.com/new-facility-investment-for-yongin-semiconductor-cluster/)
- [SK hynix：1c LPDDR6 开发，2026H2 开始供货](https://news.skhynix.com/1c-lpddr6-development-2026/)
- [SK hynix：192GB SOCAMM2 量产](https://news.skhynix.com/mass-production-socamm2-192gb/)
- [Kioxia/SanDisk：Kitakami Fab2 开始运营，218-layer 3D flash 和未来节点，2026H1 有意义产出](https://www.kioxia.com/en-jp/about/news/2025/20250930-1.html)
- [Kioxia：245.76TB LC9 enterprise SSD，2Tb BiCS QLC、32-die stack、CBA](https://americas.kioxia.com/en-us/business/news/2025/ssd-20250721-1.html)
- [Micron：245TB 6600 ION SSD 出货，G9 QLC NAND，AI workload 能效/吞吐改善](https://investors.micron.com/news-releases/news-release-details/industry-leading-245tb-micron-6600-ion-data-center-ssd-now)
- [SanDisk：UltraQLC 256TB enterprise SSD，2026H1 U.2 形态](https://shop.sandisk.com/company/newsroom/press-releases/2025/2025-08-05-sandisk-showcases-ultraqlc-technology-platform-with-milestone-enterprise-ssd-capacity-at-fms-2025)
- [TrendForce：HBM4 验证预计 2026Q2，三大供应商进入 NVIDIA 供给格局](https://www.trendforce.com/presscenter/news/20260213-12929.html)
- [TrendForce：DDR5 高获利放大产能排挤，HBM3E 2026 定价动能增强](https://www.trendforce.com/presscenter/news/20251218-12843.html)
- [TrendForce：NAND Flash 2Q25 收入与 SK/Solidigm enterprise SSD 拉动](https://www.trendforce.com/presscenter/news/20250828-12688.html)
- [SEMI World Fab Forecast 1Q26：2026/2027 设备支出与产能增长](https://www.semi.org/en/products-services/market-data/world-fab-forecast)
- [ASML Q1 2026：客户加速 2026 及以后扩产，全年收入指引 360-400 亿欧元](https://www.asml.com/en/news/press-releases/2026/q1-2026-financial-results)
- [Applied Materials + SK hynix：长期 R&D 合作，面向下一代 DRAM/HBM 材料、集成与先进封装](https://ir.appliedmaterials.com/node/28986/pdf)
- [JEDEC HBM4 标准解读：2048-bit interface、up to 2TB/s/stack](https://www.edn.com/jedec-finalizes-hbm4-standard/)
- 项目内参考：`D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- 项目内参考：`D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_HBM与高带宽内存_2026.md`
- 项目内参考：`D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_企业级SSD与高速存储控制器_2026-05-08.md`
# 行业调研：【存储前道制造设备】

> 写作截点：2026-05-08  
> 研究口径：本报告的“存储前道制造设备”主要指 DRAM/HBM core die、HBM4 base die 相关 DRAM 前道、3D NAND 前道 wafer process 设备，包括光刻、涂胶显影、刻蚀、沉积、清洗、CMP、离子注入/热处理、量测/检测、厂务级装机服务与 productivity upgrade。HBM 后道堆叠/TC bonding/混合键合只在其拉动前道产能或与前道设备交叉时纳入。  
> 市场规模口径：未来 3 个月/1 年/2 年均为自 2026-05-08 起的滚动设备收入或订单窗口估算；各细分环节存在交叉，不能简单相加为总市场。  
> 情景口径：基准 / 乐观 / 极度超预期乐观。极度乐观假设 AI 计算中心建设继续超预期、HBM/DRAM/NAND 价格高位、客户用预付款和 LTA 锁设备槽位。  
> 非投资建议。

## 0. 一页结论

**核心判断：存储前道设备从“记忆体周期品 Beta”变成 2026-2027 AI 算力扩产的上游刚需阀门。** 2026 年最确定的是 DRAM/HBM 的 EUV/DUV 光刻、ALD/CVD/epi、conductor/dielectric etch、process control；2027 年弹性最大的是 HBM4/HBM4E 对 1γ/1c/1δ DRAM、HBM4 base die、4F²/vertical DRAM pilot、300+ 到 400+ layer NAND 转换的设备拉动。

### 0.1 总量锚

| 口径 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 基准 | 2027 乐观 | 2027 极度超预期乐观 |
|---|---:|---:|---:|---:|---:|---:|
| 全球 WFE 总市场 | $126B-$132B | $132B-$142B | $142B-$155B | $135B-$145B | $145B-$160B | $160B-$185B |
| 全球存储前道设备：DRAM+NAND | $42B-$48B | $48B-$58B | $58B-$72B | $46B-$55B | $55B-$70B | $70B-$95B |
| 其中 DRAM/HBM 前道设备 | $26B-$31B | $31B-$39B | $39B-$52B | $29B-$36B | $36B-$50B | $50B-$72B |
| 其中 3D NAND 前道设备 | $16B-$18B | $18B-$23B | $23B-$32B | $17B-$21B | $21B-$30B | $30B-$45B |
| 存储前道设备占全球 WFE | 32%-36% | 35%-41% | 40%-46% | 33%-38% | 38%-44% | 44%-51% |

**公开锚点：**

- SEMI 2025 年底预测全球半导体设备销售额 2026 年 **$145B**、2027 年 **$156B**；其中 WFE 在 2025 年 $115.7B 后，2026/2027 继续增长，DRAM 设备 2025 年 $22.5B 后 2026 年 +15.1%、2027 年 +7.8%，NAND 设备 2026 年约 $15.7B、2027 年约 $16.9B。[SEMI 2025-12-16](https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports)
- SEMI 2026 年 4 月把全球 300mm fab equipment spending 上修为 2026 年 **$133B**、2027 年 **$151B**；2027-2029 年 memory 设备支出合计 **$175B**，其中 DRAM **$111B**、3D NAND **$62B**。[SEMI 2026-04-01](https://www.semi.org/en/semi-press-release/semi-projects-double-digit-growth-in-global-300mm-fab-equipment-spending-for-2026-and-2027)
- ASML Q1 2026 净系统销售 **€6.3B**，memory/logic 几乎对半，memory 为 **51%**；公司将 2026 收入指引上调至 **€36B-€40B**，并称 memory 客户 2026 已售罄且供给限制会延续到 2026 之后。[ASML Q1 2026 transcript](https://ourbrand.asml.com/asset/8e1f7393-33dd-4737-a436-cfe1b68cc577/2026_04_15-ASML-Transcript-investor-call-Q1-2026.pdf)
- Applied Materials 称 HBM DRAM die 更大、同等 bit 需要 **3-4 倍 wafer starts**，HBM stack 从 12 die 走向 16 die、20+ die；2026 增长最快的设备市场包括 HBM 与 3D chiplet-stacking。[AMAT Q1 FY2026 prepared remarks](https://ir.appliedmaterials.com/static-files/8beb86c0-2533-4d20-ba09-41fab41fc451)
- Lam Q3 FY2026 系统收入中 DRAM **27%**、NVM **12%**；其 2026 SAM 可略高于 WFE 的 mid-30%，并称多数 **$40B NAND conversion** 投资会在 2027 年底前发生。[Lam Q3 FY2026 transcript](https://www.fool.com/earnings/call-transcripts/2026/04/22/lam-research-lrcx-q3-2026-earnings-transcript/)
- Micron FQ2 2026 称 DRAM/NAND 供需 tight beyond calendar 2026；FY2026 capex 提高到 **>$25B**，FY2027 设备支出还会同比增加；HBM4 12H 已在 2026Q1 volume shipment，HBM4E 2027 ramp。[Micron FQ2 FY2026 remarks](https://investors.micron.com/static-files/e089f8c0-065d-47b8-9d02-bfa863cdb357)
- Samsung Q1 2026 DS 收入 **KRW 81.7T**、营业利润 **KRW 53.7T**；memory 已开始 HBM4/SOCAMM2 面向 NVIDIA Vera Rubin 的 mass product sales，Q2 计划 advanced-node line full utilization，并提升 HBM4 base-die supply。[Samsung Q1 2026 results](https://news.samsung.com/ca/samsung-electronics-announces-first-quarter-2026-results)
- SK hynix 披露到 2027 年底采购 **KRW 11.95T / $7.97B** ASML EUV 设备，用于新产品量产；市场估计约 30 台 EUV，服务 M15X HBM 与 Yongin advanced DRAM。[Reuters/MarketScreener 2026-03-24](https://www.marketscreener.com/news/sk-hynix-to-buy-euv-scanners-for-8-billion-from-asml-korea-ce7e5edddd8df222)

### 0.2 投资结论排序

| 排名 | 子方向 | 2026 确定性 | 2027 弹性 | 长期毛利/ROIC | 核心原因 |
|---:|---|---|---|---|---|
| 1 | EUV/DUV lithography + installed-base productivity upgrade | 极高 | 高 | 极高 | ASML 垄断 EUV；advanced DRAM/HBM 增加 critical litho exposures；memory 客户已进入抢槽位模式 |
| 2 | DRAM/HBM ALD/CVD/epi + conductor etch | 极高 | 极高 | 高 | HBM wafer-start trade ratio 3-4x；1γ/1c/1δ、HBM4 base die、4F² DRAM 都提高沉积/刻蚀强度 |
| 3 | 3D NAND high-aspect-ratio etch/deposition | 高 | 极高 | 高 | AI inference/KV cache 推动 eSSD/NAND；300+ layer 与 conversion 重新加速 |
| 4 | Process control / e-beam / overlay / defect inspection | 高 | 极高 | 极高 | 良率窗口变窄，HBM4 与 HAR NAND 缺陷成本高；KLA/AMAT e-beam 的价值捕获强 |
| 5 | 国产 memory equipment：etch/deposition/clean/CMP | 中高 | 极高 | 中高 | YMTC/CXMT 国产替代确定，但价格竞争与认证周期压毛利 |

## 1. AI 计算中心大规模建设下的机遇、挑战与技术路径

### 1.1 2026 的机遇

1. **HBM 把 DRAM wafer starts 放大成设备需求。** HBM 不是简单把普通 DRAM 切成 stack：die 更大、KGD 要求更高、12H/16H 堆叠导致同等 bit 需要更多 wafer starts。Applied 明确提到 HBM DRAM 需要 3-4x wafer starts per delivered bit，这意味着 HBM 收入增长对前道设备是高弹性的。
2. **AI inference 把 NAND 从弱周期拉回资本开支主线。** Micron 指出 AI inference 的 vector database、KV cache offload 与容量层 SSD 需求使 data center NAND demand 明显超过可得供给；Lam 则把 NAND conversion 的大部分 $40B 投资前移到 2027 年底前。
3. **内存厂盈利创纪录，设备支付能力极强。** Micron FQ2 2026 gross margin 74.4%、FQ3 指引约 81%；Samsung DS Q1 2026 operating margin 约 65.7%；SK hynix Q1 2026 新闻流显示 capex 会显著同比增加。设备厂可以把“交期、良率、throughput、服务升级”打包定价。
4. **客户 LTA 向上游传导。** ASML 称 memory/logic 客户扩产由其客户长期协议支持。云厂/HBM/AI ASIC 的锁量会让内存厂提前锁 EUV、etch、deposition、metrology 槽位。
5. **中国形成并行设备市场。** YMTC、CXMT、SMIC 因出口管制提高国产设备比例，3D NAND 的 etch/deposition/clean/CMP 是最先出现大额本土替代的方向。

### 1.2 2026 的挑战

| 挑战 | 对设备行业的影响 | 乐观解读 |
|---|---|---|
| Cleanroom 与厂房交付慢于设备订单 | 设备收入确认可能从订单滞后 1-4 个季度 | 订单锁定更早，设备商 backlog 更长，服务与安装队伍议价提高 |
| EUV/DUV、HAR etch、ALD chamber 槽位有限 | 交期拉长，客户排队 | 高端工具涨价能力和预付款增强 |
| HBM4/1γ/1c 良率爬坡 | 初期设备调试、返工与 process control 强度提高 | KLA/AMAT/Lam/ASM 的 learning-rate 工具价值提升 |
| NAND 若价格过热后需求波动 | NAND WFE 可能从新增产能转向 conversion | Conversion 仍吃刻蚀/沉积/清洗/CMP，设备强度不低 |
| 出口管制与中国路线分化 | 海外龙头中国收入受限，本土厂商毛利承压 | 中国 memory tools 形成独立高增长市场，尤其 YMTC/CXMT |
| 安装工程师与 field service 人才 | 设备装机、qual、ramp 可能成为瓶颈 | 服务合同、升级包、备件与 AI 远程诊断变成利润池 |

### 1.3 当前正在使用的关键技术

| 技术路径 | 2026 状态 | 对前道设备的拉动 |
|---|---|---|
| Advanced DRAM 1β/1γ/1c + EUV | HBM3E/4、DDR5、SOCAMM2 的主线 | Low-NA EUV、immersion DUV、track、CD-SEM、overlay、ALD high-k/metal、conductor etch |
| HBM3E 12H / HBM4 12H core die | HBM3E 全年主力，HBM4 在 Rubin/MI400/TPU/ASIC 导入 | DRAM wafer starts、KGD 前量测、EUV 层数、低缺陷 etch/deposition |
| HBM4 base die / logic base die | 2026 HBM4 初期供应差异化关键 | Foundry/logic 前道 + memory 协同，EUV、Cu/RDL、process control |
| 6F² DRAM cell scaling | 2026 大规模扩产 | Capacitor high-k ALD、bitline spacer low-k、conductor etch、CMP |
| 4F² / vertical DRAM | 2026 R&D，2027 pilot | 新 ALD/epi 层、vertical channel etch、selective deposition、High-NA 评估 |
| 232/294/300+ layer 3D NAND | 2026 conversion 与扩产并行 | HAR channel-hole etch、cryo etch、stack deposition、staircase etch、tungsten/moly gap fill、CMP |
| 400+ layer NAND | 2027 pilot/早期量产 | 更高功率密度 etch、低 damage plasma、wafer bonding、stress management |
| EUV dry resist | 已被 leading memory manufacturer 选为 advanced DRAM production tool of record | 降低 EUV dose/defect/pattern collapse，提升 scanner productivity |
| AI process control / connected chamber | Applied 已有 30,000+ chambers 连接 AIx | 缩短响应时间、提高 output、设备服务软件化 |

### 1.4 项目内 AI 芯片路线对存储前道设备的映射

项目已有 `ai_chip_research_2026_2027.md` 显示，2026-2027 年初出货量/价值权重最大的 AI 平台包括 NVIDIA B300/GB300、AWS Trainium2、Google TPU v7 Ironwood、GB200/B200、Huawei Ascend、Cambricon MLU、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200，并在 2026H2-2027 引入 Vera Rubin、AMD MI400/MI455X、TPU8、OpenAI/Broadcom ASIC。

| AI 芯片/平台 | 2026-2027 节奏 | 存储技术路径 | 对前道设备的增量 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主力放量 | HBM3E 12H，高 HBM 容量 | DRAM/HBM wafer starts、EUV/DUV、ALD/etch、KGD metrology |
| AWS Trainium2/3 | Trainium2 百万级目标，Trainium3 2026-2027 | HBM + 私有 ASIC 内存层级 | 非 NVIDIA HBM allocation 增加，扩大 DRAM equipment TAM |
| Google TPU v7 / TPU8 | Ironwood 2026 放量，TPU8 2027 | TPU v7 192GB HBM；TPU8 转下一代 HBM | HBM 不再只随 GPU，ASIC 同样消耗高端 DRAM wafer |
| AMD MI350/MI400 | MI350 2026，MI400/MI455X 2026H2-2027 | HBM3E 转 HBM4，MI455X 目标 432GB HBM4 | 2027 HBM4 core die 与 base die 设备弹性 |
| Microsoft Maia 200 / Meta MTIA / OpenAI ASIC | 2026 导入，2027 放量 | HBM3E/HBM4 + 大 SRAM/DDR5/SOCAMM2 | 进一步拉动 HBM4、DRAM 和高带宽系统内存 |
| Huawei Ascend / Cambricon / 国产 AI | 2026 中国替代主线 | 国产 HBM/DRAM + 3D NAND 本土供应 | 国产 DUV、etch、deposition、clean、CMP、metrology 认证加速 |

### 1.5 新技术成熟与放量时间：三情景

| 技术 | 基准 | 乐观 | 极度超预期乐观 | 2026 最可能路径 |
|---|---|---|---|---|
| Low-NA EUV for DRAM/HBM | 2026 全年扩产，2027 继续增 | 2026H2 客户加单，2027 Low-NA EUV output 至 80+ 台 | Memory 抢占更多 EUV/DUV 槽位，ASML memory share 维持 45%-55% | **最确定主线** |
| Immersion DUV + multi-patterning | 2026 需求恢复，接近 2025 单位出货 | DRAM/NAND 双双拉动，track/overlay 同步 | 中国与韩国同时抢 DUV，二手/翻新工具溢价 | **短交期补产能主线** |
| HBM4 前道 | 2026H2 小批量，2027 主力 | 2026Q3 多供应商稳定交付，2027 大规模扩产 | 2026Q4 已经把 2027 工具槽位全部锁满 | **2027 最大弹性** |
| EUV dry resist | 2026 advanced DRAM 量产导入 | 2027 成为部分 DRAM EUV 层默认工艺 | 2026H2 多家 memory 客户复制 | 2026 是从 POR 到量产扩散 |
| 4F² / vertical DRAM | 2026 R&D，2027 pilot，2028+ HVM | 2027 多家客户 pilot line | 2027H2 首个高端 HBM 客户提前导入 | 2026 先看 equipment design-in |
| 300+ layer 3D NAND | 2026 conversion，2027 主流 | 2026H2 inference SSD 订单推动加速 | 2026-2027 NAND 价格持续高位，新增产能+conversion 双击 | 2026 已开始放量 |
| 400+ layer NAND / next HAR etch | 2027 pilot，2028 HVM | 2027H2 部分量产 | 2027Q2 提前锁大额 etch/deposition 订单 | 2026 是技术认证 |
| High-NA EUV in DRAM | 2026 product wafer test，2027 工程导入，2028+ HVM | 2027 少量 DRAM critical layers 评估 | 2027H2 与 4F² DRAM pilot 绑定 | 2026 不是收入主线，但会锁 2028 份额 |

**2026 最可能的技术路径：** DRAM/HBM 侧是 **Low-NA EUV + immersion DUV + ALD/CVD + conductor etch + KLA/AMAT e-beam process control**；NAND 侧是 **300+ layer conversion + high-aspect-ratio etch + dielectric stack deposition + wet clean/CMP**；中国侧是 **3D NAND 和 DRAM 前道设备国产化率上行**。

## 2. 已经开始放量的关键产品：规模、渗透率、利润率

### 2.1 已放量产品总表

| 已放量产品/技术 | 代表供应商 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 设备毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| DRAM/HBM Low-NA EUV scanner + upgrade | ASML | $3.5-5.5B / $5.5-7.5B / $7.5-10B | $14-20B / $20-28B / $28-38B | $28-42B / $42-62B / $62-90B | 高端 DRAM/HBM critical layers：2026 35%-50%，2027 50%-70% | 52%-57% / 56%-60% / 58%-63% |
| Memory immersion DUV + dry DUV + track | ASML、TEL、SCREEN、Canon、Nikon | $2.0-3.5B / $3.5-5.0B / $5.0-7.5B | $8-13B / $13-20B / $20-30B | $17-28B / $28-45B / $45-68B | DRAM/NAND 全节点必需；中国/成熟 NAND 占比高 | 40%-50% / 48%-56% / 54%-62% |
| DRAM/HBM ALD/CVD/epi + capacitor/high-k/bitline spacer | AMAT、Lam、ASM、TEL、Kokusai、Piotech | $2.2-3.5B / $3.5-5.0B / $5.0-7.0B | $9-13B / $13-18B / $18-25B | $20-32B / $32-48B / $48-70B | HBM/advanced DRAM wafer starts：2026 55%-70%，2027 70%-85% | 45%-55% / 52%-62% / 58%-68% |
| DRAM conductor etch / dielectric etch | Lam、AMAT、TEL、AMEC、NAURA | $1.5-2.6B / $2.6-3.8B / $3.8-5.5B | $6-10B / $10-15B / $15-22B | $13-24B / $24-38B / $38-58B | 1γ/1c/HBM4：2026 35%-50%，2027 55%-75% | 46%-55% / 53%-62% / 60%-70% |
| 3D NAND HAR channel-hole/staircase etch | Lam、TEL、AMAT、AMEC、NAURA | $2.0-3.3B / $3.3-5.0B / $5.0-7.0B | $8-13B / $13-20B / $20-29B | $18-32B / $32-50B / $50-76B | 200+ layer：2026 50%-65%；300+ layer：2027 45%-65% | 48%-58% / 55%-65% / 62%-72% |
| 3D NAND stack deposition / gap fill / metallization | Lam、AMAT、TEL、Kokusai、ASM、Piotech | $1.8-3.0B / $3.0-4.5B / $4.5-6.5B | $7-12B / $12-18B / $18-26B | $16-28B / $28-45B / $45-68B | 高层数 NAND conversion 2026 40%-55%，2027 60%-75% | 44%-54% / 52%-62% / 58%-68% |
| Wet clean / strip / ashing | SCREEN、TEL、Lam、SEMES、ACM Research、NAURA、Kingsemi | $0.8-1.4B / $1.4-2.2B / $2.2-3.2B | $3.5-5.5B / $5.5-8.0B / $8.0-12B | $8-14B / $14-22B / $22-34B | 层数和工序数增加，clean steps/wafer 上升 | 35%-47% / 43%-55% / 50%-62% |
| CMP / planarization | Ebara、AMAT、Hwatsing、KCTech | $0.6-1.0B / $1.0-1.6B / $1.6-2.4B | $2.5-4.0B / $4.0-6.2B / $6.2-9.0B | $5.5-9.5B / $9.5-16B / $16-25B | DRAM metal/CAP/NAND stack：2026 30%-45%，2027 45%-60% | 35%-45% / 42%-52% / 48%-58% |
| Process control：inspection/CD-SEM/overlay/e-beam | KLA、AMAT、Hitachi High-Tech、Onto、Nova、Camtek、Lasertec | $1.3-2.2B / $2.2-3.4B / $3.4-5.0B | $5.5-8.5B / $8.5-13B / $13-20B | $12-20B / $20-34B / $34-55B | HBM4/3D NAND 良率 ramp：2026 设备强度提升 15%-25%，2027 +25%-40% | 55%-65% / 62%-72% / 68%-78% |
| Ion implant / anneal / furnace / RTP | Axcelis、AMAT、TEL、Kokusai、Mattson、NAURA | $0.5-0.9B / $0.9-1.4B / $1.4-2.0B | $2.0-3.5B / $3.5-5.2B / $5.2-7.5B | $4.5-8B / $8-13B / $13-20B | DRAM/NAND 通用强度稳定，先进节点略增 | 38%-48% / 45%-55% / 52%-62% |
| Installed base service / productivity upgrade | ASML、Lam、AMAT、KLA、TEL | $2.5-4.0B / $4.0-6.0B / $6.0-8.5B | $10-16B / $16-24B / $24-35B | $22-38B / $38-60B / $60-90B | 紧缺期客户优先买 output；2026-2027 持续上升 | 55%-70% / 65%-78% / 72%-85% |

### 2.2 已放量产品的增长预测

| 产品/技术 | 基准增长 | 乐观增长 | 极度超预期乐观增长 | 关键驱动 |
|---|---:|---:|---:|---|
| DRAM/HBM EUV | 2026 +15%-25%，2027 +10%-20% | 2026 +25%-40%，2027 +20%-35% | 2026 +45%-65%，2027 +35%-55% | SK hynix $8B EUV、ASML memory 51%、Micron/Samsung HBM4 ramp |
| DRAM ALD/etch | 2026 +18%-30%，2027 +18%-28% | 2026 +30%-45%，2027 +30%-45% | 2026 +50%-75%，2027 +45%-70% | HBM wafer-start trade ratio、1γ/1c、4F² R&D |
| 3D NAND HAR etch/deposition | 2026 +15%-25%，2027 +20%-35% | 2026 +25%-40%，2027 +35%-55% | 2026 +45%-70%，2027 +60%-90% | Lam $40B NAND conversion 前移、YMTC 扩产、AI SSD |
| Process control | 2026 +20%-30%，2027 +20%-35% | 2026 +30%-45%，2027 +35%-55% | 2026 +50%-75%，2027 +55%-85% | KLA process control >20% 增长；HBM4/NAND 良率爬坡 |
| Service/upgrade | 2026 +20%-35%，2027 +20%-30% | 2026 +35%-55%，2027 +30%-45% | 2026 +60%-90%，2027 +45%-70% | 装机慢、客户想立刻提高 wafer output |

## 3. 在研关键产品与未来快速增长方向

### 3.1 在研/早期技术市场规模、渗透率、利润率

| 在研/早期技术 | 2026 状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 设备毛利率：基准/乐观/极度乐观 |
|---|---|---:|---:|---:|---|---|
| High-NA EUV for DRAM | Product wafer test；ASML 称 DRAM/logic 可从 3-4 次 Low-NA 曝光降到 1 次 High-NA | $0.1-0.3B / $0.3-0.6B / $0.6-1.0B | $0.5-1.5B / $1.5-3B / $3-5B | $3-8B / $8-15B / $15-28B | 2026 <1%，2027 工程导入，2028-2029 HVM | 50%-58% / 56%-62% / 60%-66% |
| EUV dry resist / dry develop | Lam Aether 已成为 leading memory manufacturer advanced DRAM POR | $0.2-0.5B / $0.5-0.9B / $0.9-1.5B | $1-2.5B / $2.5-5B / $5-8B | $3-7B / $7-14B / $14-24B | DRAM EUV 层 2026 5%-12%，2027 20%-40% | 50%-62% / 60%-70% / 68%-78% |
| 4F² DRAM / vertical DRAM ALD+epi+etch | ASM/AMAT/Lam/TEL 客户 R&D engagement 增加 | $0.05-0.2B / $0.2-0.5B / $0.5-1B | $0.3-1B / $1-2.5B / $2.5-5B | $2-6B / $6-12B / $12-25B | 2027 pilot，2028+ 部分 high-end DRAM | 45%-58% / 55%-68% / 65%-78% |
| HBM4E / cHBM 对前道的工艺包 | Micron HBM4E 2027 ramp；customization options 加深客户 R&D | $0.1-0.4B / $0.4-1B / $1-2B | $1-3B / $3-8B / $8-15B | $8-20B / $20-45B / $45-80B | 2027 高端 xPU HBM 新增 10%-25%，2028 30%-50% | 48%-60% / 58%-70% / 68%-80% |
| 400+ layer NAND cryo/HAR etch | 2026 qualification，Lam/AMEC/TEL/AMAT 争夺 | $0.3-0.8B / $0.8-1.5B / $1.5-2.5B | $2-5B / $5-9B / $9-15B | $7-16B / $16-30B / $30-55B | 2027 10%-25%，2028 35%-55% high-layer NAND | 50%-60% / 58%-68% / 65%-75% |
| Wafer bonding / CMOS-array bonding for NAND | YMTC Xtacking、peripheral CMOS bonding、未来 3D DRAM/stacked memory | $0.2-0.6B / $0.6-1.2B / $1.2-2B | $1-2.5B / $2.5-5B / $5-9B | $3-8B / $8-18B / $18-35B | 2026 NAND 局部，2027 中国/高层数 NAND 采用上行 | 42%-55% / 52%-65% / 60%-72% |
| Molybdenum/Ru/selective metal ALD/CVD | AMAT Spectral ALD 宣称 selective monocrystalline Moly；NAND/DRAM 低阻互连需求 | $0.1-0.4B / $0.4-0.9B / $0.9-1.6B | $1-3B / $3-6B / $6-10B | $4-10B / $10-20B / $20-36B | 2026 少量，2027 advanced DRAM/NAND metal stack 10%-25% | 48%-60% / 58%-70% / 66%-78% |
| AI chamber control / predictive service / fab digital twin | Applied AIx 30,000+ chambers connected；KLA/ASML/Lam service data闭环 | $0.3-0.8B / $0.8-1.5B / $1.5-2.5B | $2-5B / $5-9B / $9-15B | $6-16B / $16-32B / $32-60B | 2026 high-end memory fabs 20%-35%，2027 40%-60% | 60%-75% / 70%-82% / 78%-88% |

### 3.2 最值得跟踪的在研方向

1. **High-NA EUV in DRAM：** ASML 在 2026 SPIE 后披露 High-NA 已处理超过 50 万片 wafer、availability 超 80%；客户展示 DRAM/logic 使用场景，可用一次 High-NA 曝光替代 3-4 次 Low-NA 曝光，部分关键层工序数可大幅下降。2027 的收入还小，但一旦 DRAM 客户锁定 High-NA layer，ASML、resist、metrology、mask inspection 会提前反映订单。
2. **EUV dry resist：** Lam Aether 2025 年已被 leading memory manufacturer 选为 advanced DRAM production tool of record，2026 年变成“降低 EUV dose + 提高 scanner throughput + 降缺陷”的刚需补丁。若 memory 客户 2026 已售罄，任何能让同一台 EUV 多出 wafer 的技术都会有高溢价。
3. **4F² / vertical DRAM：** 这是 2027-2029 DRAM 设备强度的期权。它需要更多 ALD/epi、selective deposition、vertical etch、High-NA/low-NA 协同，毛利结构更像 logic advanced node。
4. **400+ layer NAND cryo etch：** NAND 的 bit growth 不再仅靠价格恢复，而是由 inference storage、KV cache、QLC/eSSD 和中国扩产共同推动。高层数 NAND 的 channel-hole etch 是最难替代设备之一。
5. **AI process control：** HBM4 和 300+ layer NAND 的良率损失太贵，客户愿意用更高 process control intensity 换学习速度。KLA、AMAT CFE e-beam、Hitachi CD-SEM、Onto/Nova 的价值会高于传统 WFE beta。

## 4. 供给侧

### 4.1 产能结构：地区/公司/工艺

| 维度 | 主要地区 | 主要公司/资产 | 工艺与设备需求 |
|---|---|---|---|
| HBM/advanced DRAM wafer | 韩国、美国、日本、台湾、新加坡 | SK hynix M15X/Yongin、Samsung Pyeongtaek、Micron Boise/Hiroshima/Tongluo | 1β/1γ/1c/1δ DRAM，EUV/DUV、ALD/CVD、conductor etch、KGD metrology |
| 3D NAND wafer | 韩国、日本、美国/新加坡、中国 | Samsung、Kioxia/WD、Micron Singapore、YMTC Wuhan | 232/294/300+ layer，HAR etch、stack deposition、clean、CMP、bonding |
| 中国本土 memory fabs | 武汉、合肥、长鑫/长江存储生态 | YMTC、CXMT、SMIC 支撑链 | DUV 多重曝光、国产 etch/deposition/clean/CMP/metrology 验证 |
| Lithography equipment | 荷兰、日本 | ASML、Nikon、Canon、TEL/SCREEN track | EUV 垄断，DUV/track 受 memory 和中国需求拉动 |
| Etch/deposition equipment | 美国、日本、欧洲、中国 | Lam、AMAT、TEL、ASM、Kokusai、AMEC、NAURA、Piotech | DRAM/HBM ALD/etch、NAND HAR etch/deposition |
| Metrology/inspection | 美国、日本、以色列/欧洲、中国 | KLA、AMAT、Hitachi、Onto、Nova、Camtek、Lasertec、精测电子/中科飞测 | defect/overlay/CD/e-beam/probe learning |
| Clean/CMP/thermal/implant | 日本、美国、韩国、中国 | SCREEN、TEL、Lam、ACM、Ebara、AMAT、Axcelis、Kokusai、Hwatsing、Mattson、NAURA | 层数和工序数增加，国产替代空间大 |

### 4.2 供给瓶颈

1. **EUV/DUV scanner 出货与升级窗口。** ASML 2026 计划至少 60 台 Low-NA EUV，2027 能力提到 80+ 台；memory 与 logic 同时抢，advanced DRAM 需求不再是边角料。
2. **Cleanroom readiness。** Micron 明确 cleanroom constraints、long construction lead time 限制 DRAM/NAND bit supply；设备订单可能提前，但收入确认依赖厂房就绪。
3. **HAR etch chamber throughput。** 300+ layer NAND 的 channel-hole etch 时间长，plasma uniformity、mask selectivity、低 damage 都影响每小时 wafer。
4. **ALD/CVD precursor 与 critical modules。** 高 k、low-k spacer、metal ALD、moly/Ru、SiC 等材料和 chamber 供应链都可能成为局部瓶颈。
5. **Metrology/inspection 学习速度。** HBM4、4F² DRAM、300+ layer NAND 对 defect budget 更敏感，e-beam/optical inspection 排队会延长 ramp。
6. **设备零部件：RF power、MFC、vacuum pump、ESC、ceramic/quartz、precision stage。** 多数龙头已给供应商更长需求可见度，但供应链扩产仍慢于订单。
7. **客户认证。** Memory 工艺 recipe 与设备高度绑定，切换设备通常需要 6-18 个月，先进节点甚至更久。
8. **安装与 field service 人才。** 2026-2027 新厂、扩建、升级并行，装机工程师比设备硬件更难快速复制。
9. **出口管制。** 中国客户被迫提高国产替代，但先进工具可得性受限；海外龙头中国收入的高端部分有政策风险。
10. **价格传导滞后。** 设备交付长，涨价常通过配置、升级、服务、备件与 priority slot 体现，不一定立刻反映在 ASP。

### 4.3 成本构成与毛利决定因素

| 成本项 | 高端前道设备成本占比估算 | 毛利影响 |
|---|---:|---|
| 精密机械/真空腔体/机器人/wafer handling | 20%-30% | 产能扩张期模块供应紧，采购议价弱 |
| 光学/源/RF power/plasma/温控/气体系统 | 20%-35% | EUV、etch、deposition 的核心差异化，决定 ASP |
| 控制软件、recipe、AI diagnostics | 5%-12% | 低边际成本、高粘性，服务毛利高 |
| 制造/装配/测试人工 | 8%-15% | 装机复杂度上升，field labor 稀缺 |
| 供应链、物流、关税、保修 | 8%-15% | 跨境摩擦增加，但可部分转嫁 |
| R&D amortization | 10%-18% | High-NA、4F²、HAR NAND、AI service 前置投入大 |
| 安装、qual、售后服务 | 5%-12% | 紧缺期服务可独立定价，毛利高于系统硬件 |

**毛利锚：** ASML 2026 指引 gross margin 51%-53%；Lam 2026Q2 指引约 50.5%；Applied Q1 FY2026 non-GAAP gross margin 49.1%；KLA Q3 FY2026 call 给下季度 gross margin 61.75% ±1ppt。高端 process control、EUV upgrade、installed-base service 的长期毛利最强；国产替代设备高增长但可能因价格竞争、验收周期和付款条款导致毛利分化。

**价格传导机制：**

- 内存厂与云厂签 HBM/DRAM/NAND LTA，内存厂先锁设备 slot。
- 设备厂通过 down payment、configuration、priority installation、service bundle、upgrade package 传导价格。
- 对客户而言，设备提价只要能换来更高 yield/throughput，就可以被 HBM/DRAM/NAND 高 ASP 吸收。
- 供不应求时，最容易涨价的是 EUV/DUV upgrade、HAR etch、ALD、e-beam/process control、critical spares。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | 集中度 | 主要玩家 | 竞争判断 |
|---|---|---|---|
| EUV lithography | ASML 100% | ASML | 绝对垄断，memory 客户只能排队 |
| Immersion DUV | 高 | ASML、Nikon、Canon | ASML 强势，DUV 受中国和 memory 补产能拉动 |
| Track / coat-develop | 高 | TEL、SCREEN、SEMES、Kingsemi | 与 litho recipe 绑定，国产替代从 mature/China 进入 |
| DRAM/NAND etch | 高 | Lam、AMAT、TEL、AMEC、NAURA | Lam 在 3D NAND HAR 与 DRAM dielectric/conductor 份额强；AMEC/NAURA 中国弹性大 |
| Deposition/ALD/CVD/Epi | 中高 | AMAT、Lam、ASM、TEL、Kokusai、Piotech、NAURA | AMAT memory process 组合最全，ASM ALD/Epi 高端增速强 |
| Process control | 极高 | KLA、AMAT、Hitachi、Onto、Nova、Lasertec | KLA 长期高毛利，e-beam 和 defect inspection 受益于 HBM4 |
| Wet clean | 中高 | SCREEN、TEL、Lam、ACM、SEMES、NAURA | 工序数增加，ACM/NAURA 中国份额提升 |
| CMP | 中 | Ebara、AMAT、Hwatsing | DRAM/NAND 稳定需求，国产替代可见 |
| Implant/thermal | 中高 | Axcelis、AMAT、TEL、Kokusai、Mattson、NAURA | 增速低于 etch/deposition，但毛利稳定 |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 量化/事实 | 为什么能定价 |
|---|---|---|
| 工艺认证周期 | 先进 memory tool 从 eval 到 HVM 通常 6-18 个月 | 客户不能在供不应求时冒险换设备，recipe lock-in 强 |
| 良率杠杆 | HBM4 / NAND 高层数任一关键缺陷都会放大到整 stack/整 die 损失 | 工具若提高 1%-2% 良率，价值远高于设备 ASP 差异 |
| Throughput 稀缺 | ASML NXE:3800E upgrade 立刻提高 10 wph；Lam dry resist 可提高 EUV patterning productivity | 客户买的是 wafer output，不只是硬件 |
| Installed base | 龙头在 memory fabs 有多年装机基础 | 后续工艺升级、备件、服务、软件都沿 installed base 变现 |
| 供应槽位 | KLA 管理层称客户急于锁 2027 slot；ASML/Lam/AMAT 都提高产能/供应链可见度 | Slot 本身有稀缺溢价 |
| 出口管制 | 中国 advanced memory 设备可得性受限 | 可供货厂商具备政策稀缺性，国产厂商在本土有替代溢价 |
| 跨学科 know-how | DRAM/HBM/NAND 同时涉及 litho、plasma、materials、thermal、metrology | 单点设备难以替代整套工艺协同 |

### 5.3 长期价值捕获

**长期高 ROIC/高毛利最可能在四层：**

1. **ASML EUV + installed-base upgrade：** EUV 垄断、客户不具备替代方案，服务升级可直接卖 output。
2. **KLA/高端 process control：** 缺陷预算收缩，AI/HBM 使 process control intensity 上升，且软件/算法/数据库复用性强。
3. **Lam/AMAT/ASM 的 memory critical module：** HAR etch、DRAM ALD/conductor etch、dry resist、selective deposition 绑定关键良率。
4. **国产设备中率先通过 YMTC/CXMT HVM 的 etch/deposition/clean/CMP：** 增速可能最高，但长期毛利取决于是否从替代采购走向 recipe 定义权。

## 6. 2026 关键变化：三个最可能拐点

### 拐点一：Memory WFE 从“复苏”变成“抢产能”

ASML Q1 2026 memory 达净系统销售 51%，客户称 2026 已售罄；Micron FY2026 capex 提到 >$25B；SK hynix 用近 $8B 锁 ASML EUV；Samsung HBM4/SOCAMM2 已开始面向 Rubin 的 mass product sales。2026 年最可能放量的子方向是 **DRAM/HBM EUV/DUV、ALD/CVD、conductor etch、process control、installed-base upgrade**。

### 拐点二：NAND 由 AI inference/KV cache 触发第二增长曲线

SEMI 预计 NAND equipment 2026/2027 继续增长；Lam 指出 NAND conversion 的多数 $40B 投资会在 2027 年底前发生；Micron data center NAND revenue FQ2 环比翻倍且 demand 超过 available supply。2026 最可能放量的 NAND 子方向是 **300+ layer conversion、HAR channel etch、stack deposition、wet clean、CMP、NAND metrology**。

### 拐点三：中国 memory equipment 国产化从试点进入大额订单

YMTC Phase 3 设备安装中本土工具比例据报道超过 50%，并计划更多 Wuhan fabs；Macquarie 估计新增两座 100k wpm fab 需要 RMB 160B-180B capex，etch/deposition 是最大受益方向。2026 最可能放量的是 **AMEC/NAURA/Piotech/ACM/Hwatsing/Kingsemi 在 3D NAND 与 DRAM mature/selected advanced steps 的订单**。

## 7. 2027 关键变化：三个最可能拐点

### 拐点一：HBM4/HBM4E 进入真正设备放量年

Rubin、MI400/MI455X、TPU8、OpenAI/Meta/Broadcom ASIC 会把 HBM4 从 2026 的导入变成 2027 的主力。Micron 已指向 HBM4E 2027 ramp、FY2027 equipment spend 增加；Samsung/SK hynix 同样会围绕 HBM4 和 base die 扩大 advanced DRAM 工具。2027 最可能放量的是 **1γ/1c/1δ DRAM EUV、ALD、conductor etch、base-die foundry equipment、HBM KGD/process control**。

### 拐点二：High-NA EUV 与 4F² DRAM 决定 2028 订单排队

High-NA 2027 仍不一定大规模收入确认，但会进入 DRAM product wafer 与 pilot line 决策。4F²/vertical DRAM 需要新增 ALD/Epi/etch 层，ASM Q1 2026 已提到 4F² DRAM ALD/Epi application R&D。2027 的订单价值在于 **提前锁 2028-2029 设备份额**。

### 拐点三：3D NAND 400+ layer 与中国扩产叠加

2027 AI inference 的存储需求若继续吞掉 eSSD/NAND，NAND 厂商会从 conversion 走向新增产能。高层数 NAND 的 HAR etch/deposition 难度非线性上升，中国 YMTC/CXMT 生态会把国产设备验证强行推进。2027 最可能放量的是 **cryo/HAR etch、stress management、wafer bonding、NAND process control、国产 clean/CMP**。

## 8. 头部公司与潜在受益公司清单

### 8.1 全球设备龙头

| 环节 | 头部公司 | 细分优势 |
|---|---|---|
| EUV/DUV lithography | ASML、Nikon、Canon | ASML EUV 100%；immersion DUV 和 productivity upgrade 是 2026 memory 抢产能核心 |
| Track / coat-develop | Tokyo Electron、SCREEN、SEMES、Kingsemi | EUV/DUV recipe 绑定；TEL 在 track 和 etch/deposition 组合强 |
| Etch | Lam Research、Applied Materials、Tokyo Electron、AMEC、NAURA | Lam 在 3D NAND HAR 和 DRAM dielectric/conductor etch 强；AMEC/NAURA 是中国替代核心 |
| Deposition / ALD / CVD / Epi | Applied Materials、Lam Research、ASM International、Tokyo Electron、Kokusai Electric、Piotech、NAURA | AMAT memory process 覆盖广；ASM ALD/Epi 受益 advanced DRAM；Piotech/NAURA 受益国产 DRAM/NAND |
| Furnace / thermal / anneal | Kokusai Electric、Tokyo Electron、Applied Materials、Mattson、NAURA | DRAM/NAND 扩产稳定受益 |
| Wet clean | SCREEN、Tokyo Electron、Lam、SEMES、ACM Research、NAURA、Kingsemi | NAND 层数增加带来 cleaning step/wafer 增长；ACM 中国客户强 |
| CMP | Ebara、Applied Materials、Hwatsing、KCTech | DRAM/NAND planarization 稳定需求，Hwatsing 国产替代 |
| Ion implant | Axcelis、Applied Materials、Nissin Ion Equipment、NAURA | memory 需求稳定，先进节点/中国扩产受益 |
| Metrology/inspection | KLA、Applied Materials、Hitachi High-Tech、Onto Innovation、Nova、Camtek、Lasertec、中科飞测、精测电子 | KLA 价值捕获最强；AMAT CFE e-beam 2026 目标 >$1B；Lasertec mask inspection 受 EUV 强度提升 |
| Wafer bonding / advanced memory integration | EV Group、SUSS MicroTec、Tokyo Electron、Applied Materials、ASMPT、BESI、ASMPT | NAND CMOS bonding、future 3D DRAM、HBM 先进封装交叉受益 |

### 8.2 存储制造客户：设备订单来源

| 公司 | 地区/资产 | 2026-2027 关注点 |
|---|---|---|
| SK hynix | 韩国 M15X、Yongin | $7.97B ASML EUV 订单；HBM4/advanced DRAM 扩产 |
| Samsung Electronics | Pyeongtaek、韩国/美国 foundry/memory | HBM4/SOCAMM2 for Rubin，HBM4 base die，advanced-node full utilization |
| Micron | Boise、Hiroshima、Tongluo、Singapore、Idaho/New York | FY2026 capex >$25B；HBM4 volume、HBM4E 2027、NAND Singapore |
| Kioxia / Western Digital | 日本 | 3D NAND conversion 和 high-layer NAND，AI storage 价格改善后 capex 弹性 |
| YMTC | Wuhan | 232/294+ layer、Xtacking、Phase 3 本土设备、潜在两座 100k wpm fab |
| CXMT | Hefei | DDR5/LPDDR/HBM 国产路线，DUV 多重曝光与国产 etch/deposition |
| Nanya / Winbond / Powerchip | 台湾 | specialty DRAM 与成熟 memory，部分设备扩产 |

### 8.3 中国设备链

| 环节 | 公司 | 观察点 |
|---|---|---|
| Etch | 中微公司 AMEC、北方华创 NAURA | 3D NAND etch、DRAM etch、YMTC/CXMT 验证；AMEC 是 YMTC 扩产最直接弹性之一 |
| Deposition | 北方华创、拓荆科技 Piotech、中微公司 | PECVD/ALD/CVD 进入 domestic 3D NAND、DRAM、advanced packaging |
| Clean | 盛美上海 ACM Research、北方华创、芯源微 Kingsemi | 单片/槽式清洗、涂胶显影、湿法工艺国产替代 |
| CMP | 华海清科 Hwatsing、烁科/相关国产 CMP 生态 | DRAM/NAND planarization 国产替代 |
| Metrology/inspection | 中科飞测、精测电子、上海睿励、东方晶源 | 国产 defect/overlay/CD-SEM 起步，先进 memory 认证周期长 |
| Thermal/implant | 北方华创、万业企业/凯世通、烁科 | mature memory 与国内产线替代 |

## 9. 监测清单：未来 6-12 个月最该盯的信号

1. **ASML memory end-use mix 是否维持 45%+，Low-NA EUV 2027 output 是否确认 80+ 台。**
2. **SK hynix M15X/Yongin 的 EUV 装机节奏，以及 HBM4/1c DRAM 良率披露。**
3. **Micron FY2027 equipment spend 是否继续上修，Idaho/Hiroshima/Tongluo/Singapore 设备招标节奏。**
4. **Samsung HBM4 base die 与 foundry 4nm memory product 的实际客户放量。**
5. **Lam NAND conversion 中 $40B 投资是否继续前移，3D NAND 高层数订单是否超出 SEMI 基准。**
6. **KLA process control memory mix 是否从 18% 继续上升，DRAM/NAND 良率学习是否增加 e-beam/inspection 强度。**
7. **YMTC Phase 3 与后续两座 fab 的本土设备比例；AMEC/NAURA/Piotech/ACM/Hwatsing 的 memory 客户验收收入。**
8. **EUV dry resist 是否从单一 leading memory manufacturer 扩散到第二、第三家。**
9. **High-NA EUV 在 DRAM product wafer 的客户 paper 和 pilot line 决策。**
10. **AI inference 对 PCIe Gen6 eSSD/KV cache 的订单是否让 NAND 厂从 conversion 转新增产能。**

## 10. 主要来源

| 来源 | 关键用途 |
|---|---|
| [SEMI：2026/2027 全球 300mm fab equipment spending $133B/$151B](https://www.semi.org/en/semi-press-release/semi-projects-double-digit-growth-in-global-300mm-fab-equipment-spending-for-2026-and-2027) | 总量锚、memory 2027-2029 $175B |
| [SEMI：全球半导体设备 2026/2027 $145B/$156B](https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports) | DRAM/NAND WFE 增长锚 |
| [ASML Q1 2026 investor call transcript](https://ourbrand.asml.com/asset/8e1f7393-33dd-4737-a436-cfe1b68cc577/2026_04_15-ASML-Transcript-investor-call-Q1-2026.pdf) | Memory 51%、2026 指引、Low-NA EUV output、High-NA DRAM use case |
| [ASML Q1 2026 press release](https://www.asml.com/en/news/press-releases/2026/q1-2026-financial-results) | €8.8B Q1 revenue、FY2026 €36B-€40B |
| [Applied Materials Q1 FY2026 prepared remarks](https://ir.appliedmaterials.com/static-files/8beb86c0-2533-4d20-ba09-41fab41fc451) | HBM wafer-start trade ratio、HBM/3D stacking、CFE e-beam |
| [Lam Research Q3 FY2026 transcript](https://www.fool.com/earnings/call-transcripts/2026/04/22/lam-research-lrcx-q3-2026-earnings-transcript/) | DRAM/NVM revenue mix、NAND conversion、Stryker/etch/deposition |
| [Lam Aether dry resist memory POR](https://newsroom.lamresearch.com/2025-01-29-Breakthrough-EUV-Dry-Photoresist-Technology-from-Lam-Research-Adopted-by-Leading-Memory-Manufacturer) | EUV dry resist 在 advanced DRAM 的量产导入 |
| [KLA Q3 FY2026 transcript](https://www.fool.com/earnings/call-transcripts/2026/04/29/kla-klac-q3-2026-earnings-call-transcript/) | Process control 增速、memory mix、2027 slot urgency |
| [ASM Q1 2026 results](https://www.globenewswire.com/news-release/2026/04/21/3278259/0/en/ASM-reports-first-quarter-2026-results.html) | Advanced DRAM/HBM ALD/Epi 与 4F² DRAM R&D |
| [Tokyo Electron IR results page](https://www.tel.com/ir/library/report/index.html) | TEL FY2026 annual results 与设备组合入口 |
| [Micron FQ2 FY2026 prepared remarks](https://investors.micron.com/static-files/e089f8c0-065d-47b8-9d02-bfa863cdb357) | HBM4/HBM4E、capex >$25B、DRAM/NAND tight beyond 2026 |
| [Micron HBM4 / SOCAMM2 / PCIe Gen6 SSD GTC 2026 announcement](https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin) | HBM4 12H volume shipment、16H sample、AI storage |
| [Samsung Q1 2026 results](https://news.samsung.com/ca/samsung-electronics-announces-first-quarter-2026-results) | HBM4/SOCAMM2 for Rubin、HBM4 base die、DS 财务 |
| [SK hynix $7.97B ASML EUV order - Reuters via MarketScreener](https://www.marketscreener.com/news/sk-hynix-to-buy-euv-scanners-for-8-billion-from-asml-korea-ce7e5edddd8df222) | SK hynix EUV 设备订单、M15X/Yongin |
| [ASMPT Q1 2026 results](https://www.asmpt.com/en/investor-relations/news-events/asmpt-announces-2026-first-quarter-results/) | HBM4 16H TCB/HB 交叉验证，作为 HBM 设备链参考 |
| [YMTC expansion / AMEC / NAURA - Investing.com](https://www.investing.com/news/stock-market-news/ymtc-expansion-to-benefit-amec-and-naura-says-macquarie-93CH-4615620) | 中国 3D NAND 扩产、国产设备比例、etch/deposition capex |
| 项目内 `ai_chip_research_2026_2027.md` | 2026-2027 AI 芯片路线与出货节奏映射 |

## 11. 读数注意事项

1. 本报告把 equipment revenue、orders、fab equipment spending 混合用于建模，已尽量区分，但不同公司确认收入时点不同。
2. DRAM/HBM 和 NAND 设备存在交叉。例如 metrology、clean、CMP、service 可能同时服务多个工艺段，表格不可简单加总。
3. 极度超预期乐观情景并不是行业报告基准，而是假设 AI inference/token demand、HBM4、SOCAMM2、PCIe Gen6 SSD、eSSD/NAND 同步超预期，且内存厂盈利足以覆盖高强度 capex。
4. 中国国产设备的收入确认高度依赖客户验收、出口管制变化、国内价格竞争和产线良率；增速可能极高，但毛利不一定线性扩张。
# 行业调研：【高端光罩与先进封装掩模】

> 截至日期：2026-05-08  
> 研究口径：本文把“高端光罩/掩模”分成两层：1）晶圆制造用 photomask/reticle，包括 EUV、ArF immersion、KrF/i-line 高端及主流节点光罩、mask blank、pellicle、OPC/ILT、写入、检测、修补、清洗和 AIMS 资格验证；2）先进封装用掩模，包括 CoWoS/RDL/interposer/fan-out/WLP/PLP/玻璃或陶瓷 core/CPO/硅光/纳米压印模具等所需的 reticle、大尺寸玻璃 mask、RDL mask、stepper/aligner mask、direct imaging 配套数据与工艺。  
> 情景原则：按要求对 2026-2027 AI 计算中心建设采取明显乐观假设。所有缺少直接公开数字的市场规模、渗透率和利润率均为基于 AI 芯片出货、tape-out 数量、HBM/CoWoS/先进封装产能、公司公告和设备订单的估算。

## 0. 一页结论

高端光罩不是半导体材料里的“小耗材”，而是 2026-2027 AI 芯片供给链中最早被消耗、最难临时补、且最能体现客户技术锁定的环节之一。GPU/ASIC 量产前先消耗 mask set；先进封装放量前先消耗 RDL/interposer/封装 mask；HBM4、2nm、CoWoS-L、glass core、CPO 进入 NPI 前先消耗写入、检测、AIMS、pellicle 和 blank 产能。

**最核心判断：**

| 判断 | 结论 |
|---|---|
| 2026 主线 | GB300/B300、GB200/B200、MI350、TPU Ironwood、Trainium2/3、Maia200、MTIA 300/400 和国产 AI 芯片使 4/5/3nm、HBM3E、2.5D/RDL、OAM/FC-BGA 掩模需求维持高景气。 |
| 2026 新增弹性 | Rubin、MI400、TPU8、OpenAI/Broadcom XPU、Meta/Broadcom MTIA 多代迭代，使 2nm EUV、HBM4 base die、CoWoS-L/RDL interposer、UCIe/chiplet、CPO 相关 mask 进入锁产能阶段。 |
| 2027 主线 | 2nm、HBM4、Rubin/MI400/TPU8 与更多 CSP ASIC 共同放大 mask 层数、mask set 价格、改版次数和设备利用率；High-NA EUV 即使不是 TSMC 主线，也会通过 Intel/Samsung/R&D 带来高端 mask 资格验证需求。 |
| 供给瓶颈 | 不是玻璃基板一个点，而是 EUV blank defect、multi-beam writer、actinic inspection/AIMS、EUV pellicle、OPC/ILT 数据处理、客户认证和高端 mask 工程师组成的复合瓶颈。 |
| 最强定价权 | EUV/2nm 光罩、EUV mask blanks、pellicles、multi-beam writers、actinic inspection/AIMS、OPC/ILT/EDA、与 TSMC/Intel/Samsung/DNP/Tekscend/Photronics 绑定的高端 mask shop。 |
| 2026 全球 photomask 总市场估算 | 基准 $5.9-6.7B；乐观 $6.7-7.8B；极度超预期 $7.8-9.2B。公开市场报告给出的 2025 photomask 规模约 $5.28B，2023 约 $5.11B，本文上修来自 AI/HBM/ASIC tape-out 与先进封装增量。 |
| 2026 先进封装掩模市场估算 | 基准 $0.45-0.80B；乐观 $0.75-1.15B；极度超预期 $1.1-1.8B。若把封装用 lithography/direct imaging 设备和服务也计入，收入池更接近 $1.5-3.0B。 |
| 投资排序 | 1）EUV blank/pellicle/inspection；2）multi-beam writer、AIMS、mask repair；3）EUV/2nm merchant mask；4）先进封装 RDL/interposer mask；5）OPC/curvilinear/ILT 软件；6）普通 mature-node mask。 |

## 1. 最近半年关键事实与一手锚点

| 日期 | 来源 | 关键事实 | 对本行业含义 |
|---|---|---|---|
| 2026-02 | Photronics 1Q26 | 营收 $225.1M，YoY +6.1%；IC revenue $165.3M，YoY +7%；公司称 high-end IC revenue 连续第二个季度创新高；毛利率 35.0%，经营利润率 24.4%，季度 capex $47.6M。 | 高端 IC 光罩已从消费电子低谷恢复，AI/区域化驱动高端和地缘本地化产能。Photronics 是可量化的 merchant mask 温度计。 |
| 2026-02 | DNP/Rapidus | DNP 参与 Rapidus 融资，明确支持 Rapidus 2027 年 2nm 逻辑量产；DNP 要实现 2nm EUV 光罩高良率、短交期，并把 EUV 光罩列为半导体业务增长引擎。 | 日本 2nm/EUV mask 供应链进入“研发转准量产”阶段，DNP 的 2nm mask 能力不只是实验室项目。 |
| 2026-03 | Tekscend Photomask | Tekscend 与韩国利川市签 MOU，规划第三工厂：2027 完工，2028-2029 启动 14nm 及以下 advanced photomasks 量产。 | 韩国本土高端 mask 第二来源战略加速，服务 Samsung/SK hynix/韩国 fab 与 AI memory/HBM 生态。 |
| 2025-10 | Tekscend Singapore | 新加坡厂 15,200 平方米用地、8,849.53 平方米建筑面积；公司称新加坡此前没有 photomask 制造设施，新厂引入 AI 调度和自动化产线，靠近 HOYA 等材料供应商。 | 东南亚/印度半导体扩产需要近场 mask 供应；mask 区域化比晶圆厂更早进入布局。 |
| 2025-07 | Tekscend Europe | 在法国 Corbeil 安装 Mycronic SLX1，是 SLX1 欧洲首台部署；Tekscend 称自己是全球最大 merchant photomask supplier，欧洲 Corbeil 与 Dresden AMTC 覆盖 laser mask 到 eBeam 高端 mask。 | 欧洲 Chips Act 不只补 wafer fab，也需要 mask writer 和本地 mask shop；“No masks, no chips”成为供应链政治口号。 |
| 2026-01 至 2026-04 | Mycronic | 2026-04 获 customized SLX mask writer 订单 $27-30M、2028 交付；2026-03 SLX 订单 $5-7M、2027Q2 交付；2026-02 Prexision 8 Evo $21-24M；2026-01 MMX metrology $2-4M；2025-12 FPS 6100 Evo $4-5M，应用含 electronic packaging。 | mask writer 订单从成熟半导体、显示、电子封装到定制平台全面活跃；交期跨到 2027-2028，说明关键设备不是即买即用。 |
| 2026-04 | Lasertec 3Q FY2026 | 9 个月营收 ¥169.5B，经营利润 ¥78.2B，经营利润率约 46.1%；公司称 AI 投资推动 GPU、HBM 等先进半导体需求强劲，device maker capex 提高；服务收入 YoY +35.5%。 | EUV mask blank/actinic inspection 类设备具备非常高经营杠杆，装机后的服务收入也受益。 |
| 2026-02 | ZEISS SMT | AIMS EUV 3.0 全球部署，支持 Low-NA 与 High-NA EUV；吞吐量较前代提升 3 倍，2026 向 pilot customers 推出 wafer-level critical-dimension option。 | EUV mask 资格验证成为独立瓶颈。High-NA 即使慢，也会推高 AIMS/actinic qualification 价值。 |
| 2026 | NuFlare | MBM-2000 支持 3nm，MBM-2000PLUS 支持 3nm+；multi-electron beam writer 控制 260,000 beams；公司继续面向 2nm 以后、EUV/nanoimprint 开发。 | advanced EUV/curvilinear mask 必须依靠 multi-beam writer，提高设备稀缺度。 |
| 2025/2026 | SEMI photomask report sample | SEMI 样本指出 captive mask houses 仍占 photomask 最大份额；merchant suppliers 自 2022 起恢复部分份额；EUV pellicles 已可用并成为关键芯片 HVM 要求；multi-beam mask writers 对 EUV Manhattan 和 curvilinear mask 都是 essential。 | 高端 mask 市场不是纯 merchant 市场，投资判断必须把 captive/merchant 产能都算进去；curvilinear 是 2026-2027 的真实技术变量。 |
| 2026-05 | Veeco 1Q26 | 公司给出 advanced packaging wet processing and lithography SAM：2026 约 $600M、2030 约 $1.0B；IBD EUV mask blanks & pellicles 是新增前端机会。 | 先进封装 lithography 和 EUV mask blank/pellicle 设备市场正在被设备公司单独列为 AI/HBM/advanced packaging 驱动项。 |

## 2. AI 计算中心建设给行业带来的机遇、挑战与技术路径

### 2.1 2026 机会

1. **AI 芯片 tape-out 数量上升，比 wafer 出货更早拉动光罩。**  
   NVIDIA、AMD、Google/Broadcom、AWS、Meta/Broadcom、Microsoft、OpenAI/Broadcom、Huawei/Cambricon 等路线并行，意味着 mask set 数量和改版频率上升。一个先进逻辑 tape-out 可能消耗几十到上百张 reticle，先进节点 mask set 价值可达数百万到数千万美元；AI ASIC 的多客户并行比单一 GPU 周期更有利于 merchant mask shop。

2. **HBM 与 base die 把 memory mask 重新变成高端市场。**  
   HBM3E/HBM4 不只增加 DRAM wafer，也增加 TSV、base die、测试结构、先进封装相关 mask。SK hynix、Samsung、Micron 的 HBM4 验证与扩产使 EUV/ArF mask、blank、pellicle、inspection 同步受益。

3. **先进封装从“封测后段”变成“第二套光刻系统”。**  
   CoWoS-L/RDL interposer、InFO-oS、fan-out、silicon interposer、glass/ceramic core、CPO/硅光都需要 photolithography 或 mask-like master。单颗 AI XPU 的前端 mask 之外，还会产生 interposer/RDL/封装层 mask。

4. **低 NA EUV 多重图形化可能比 High-NA 更利好 mask 数量。**  
   如果 TSMC 在 A16/A14 继续偏向 0.33NA EUV + 多重 patterning 而非快速导入 High-NA，单层或关键层 mask 次数、OPC/ILT 复杂度和 mask recut 可能增加。High-NA 更利好单张 mask 难度；低 NA 延寿更利好 mask 数量。

5. **区域化带来冗余 mask 产能。**  
   Tekscend 新加坡、韩国、欧洲投资；DNP/Rapidus；Photronics 美国/欧洲/亚洲/中国布局；各大 foundry captive mask shop 扩张，说明客户愿意为区域韧性付费。

### 2.2 2026 挑战

1. **EUV mask blank defect 与供应集中。** HOYA、Shin-Etsu、AGC、S&S Tech 等少数供应商决定 EUV blank 良率和交期。缺陷一旦进入 blank，后续写入/检测/修补成本极高。  
2. **multi-beam writer 和 actinic inspection 设备稀缺。** IMS/NuFlare、Lasertec/KLA/ZEISS、Mycronic 等设备交期长，且客户认证不可压缩。  
3. **EUV pellicle 材料极限。** 高透过率、耐 EUV 功率、低粒子、低热变形同时满足很难；High-NA 和高功率 EUV 会继续提高难度。  
4. **OPC/ILT 数据爆炸。** Curvilinear/ILT mask 对数据量、fracturing、写入时间和计算基础设施提出新要求，mask shop 的 IT/EDA 能力变成产能。  
5. **先进封装 mask 单价低于 EUV，但交付窗口更碎。** CoWoS/RDL/PLP 的 mask 层数、版图变化、客户 NPI 节奏频繁，运营复杂度高。  
6. **客户认证锁死供应商。** 一套 mask 工艺绑定 foundry design rule、OPC model、defect spec、cleaning recipe、pellicle、inspection tool 和数据安全流程，切换成本通常是 6-18 个月。  
7. **中国本土高端光罩受设备限制。** DUV 多重曝光、国产 AI 芯片、成熟制程扩张会拉动本土 mask，但 EUV writer、actinic inspection、blank 和 pellicle 的短板仍明显。

### 2.3 2026-2027 出货最大 AI 芯片路径对光罩/封装掩模的拉动

以下 AI 芯片技术路径来自项目内 `ai_chip_research_2026_2027.md`，本文只抽取其对光罩/掩模的含义。

| AI 芯片/平台 | 2026-2027 出货逻辑 | 前端光罩需求 | 先进封装掩模需求 | 对行业结论 |
|---|---|---|---|---|
| NVIDIA B300/GB300 | 2026 Blackwell Ultra 主力，GB300 NVL72 放量 | TSMC 4NP/EUV+ArF，多 reticle 级复杂设计，工程改版价值高 | CoWoS-L/S、HBM3E landing、RDL/LSI、大尺寸 ABF/OAM | 2026 最确定收入池，推动 mature EUV mask + RDL mask 同时满载。 |
| AWS Trainium2 | Rainier/Anthropic 百万颗级目标 | 定制 ASIC，mask NRE 被 AWS 自用规模摊薄 | HBM + NeuronLink + 64 芯片 UltraServer；系统级测试 mask/治具需求 | 自用 ASIC 也消耗高端 mask；merchant 收入不透明，但供应链产能被占用。 |
| Google TPU v7 Ironwood | Google Cloud/Anthropic 扩容，推理优先 | Broadcom/Google 先进节点 mask，ASIC 多代迭代 | 2.5D/HBM、large substrate、pod interconnect 测试 | CSP ASIC 从补充 GPU 变成独立 mask demand pool。 |
| NVIDIA B200/GB200 | 存量订单延续 | TSMC 4NP 成熟 mask | CoWoS/HBM3E | 给 2026 mask shop 利用率打底。 |
| Huawei Ascend 910C/950 | 中国国产替代第一梯队 | SMIC N+2/N+3 DUV 多重曝光，mask 层数和重工压力高 | 本土 2.5D/OAM/高带宽内存替代 | 中国本土 mask 量大但技术上限受设备限制。 |
| Cambricon MLU590/690 | 2026 目标几十万颗级 | SMIC 可得先进节点 DUV mask | HBM/OAM/本土封装 mask | 本土成熟/先进 DUV mask 与封装 mask 受益。 |
| AMD MI350 | 2026 AMD 最确定放量 | TSMC 先进节点，HBM3E 相关 mask | 2.5D、UBB/OAM/PCIe 多形态封装 mask | 非 NVIDIA 高端 GPU 分散 mask 客户结构。 |
| AWS Trainium3 | 2026-2027 接棒 | AWS 称 3nm，mask set 复杂度上升 | 144 芯片 UltraServer，封装与系统验证复杂 | 3nm ASIC 把 mask set 单价推高。 |
| Meta MTIA 300/400/450/500 | 2026-2027 四代迭代，>1GW 首期 | Broadcom XPU 平台，多代 tape-out | FC-BGA/RDL/chiplet/OCP rack | 高迭代频率直接利好 mask recut 与 OPC/ILT 服务。 |
| Microsoft Maia 200 | Azure 内部推理放量 | TSMC 3nm，>140B transistor 级别 | HBM3E + 液冷 rack + advanced package | 云厂自研 ASIC 成为稳定高端 mask 客户。 |
| NVIDIA Rubin/AMD MI400/TPU8/OpenAI XPU | 2026H2 小批量，2027 放量 | 2nm/3nm、HBM4、更多 chiplet；mask set 难度上升 | CoWoS-L/SoIC/EMIB-T/RDL/HBM4 | 2027 二次紧缺主因。 |

### 2.4 技术成熟与放量时间表

| 技术 | 当前状态 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准/乐观/极超 |
|---|---|---|---|---|---|
| 0.33NA EUV masks for N5/N4/N3 | 已 HVM | GB300、MI350、TPU/ASIC 拉满 | 低 NA EUV 多重 patterning 延寿，提高 mask 数量 | AI ASIC 重复 tape-out，mask set 价格维持高位 | 2nm 前仍是最大收入池；TSMC 若延后 High-NA，则数量继续受益。 |
| ArF immersion high-end masks | 已 HVM | DRAM/HBM、N4/N3 非 EUV 层、先进 DUV 多重曝光拉动 | 中国国产 AI 芯片 DUV 多重曝光增加 | HBM/国产替代叠加导致交期紧张 | 仍是最大 unit pool，价格不如 EUV 但规模稳。 |
| 2nm EUV masks | DNP/Rapidus、IBM/Tekscend 等进入研发/准量产 | 2026 完成工艺开发/试产 mask | 2026H2 进入更多 pilot line 和 AI ASIC NPI | 2nm AI ASIC 提前 tape-out，NRE 爆发 | 2027 Rapidus/Intel/Samsung/部分 foundry 早期 HVM，收入显著上升。 |
| High-NA EUV masks | R&D/pilot | 主要是 Intel/Samsung/imec/IBM 资格验证 | ZEISS AIMS 3.0、MBMW、pellicle 订单提前 | 客户为 2028 量产提前锁 writer/inspection | 2027 仍偏小批量；若 TSMC 延后，收入不如 0.33NA 多重 patterning，但单张价值极高。 |
| Curvilinear / ILT masks | 从局部走向更多 EUV 层 | multi-beam writer 成为必需，OPC/ILT 算力需求上升 | 全芯片 curvilinear 在关键层增加 | AI 用 ILT 缩短 PPA 优化周期，mask 数据服务溢价 | 2027 成为高端 EUV 默认能力之一。 |
| EUV pellicles | 已可用并走向 HVM 要求 | critical chips 上升至较高 attach | 高功率 EUV 与 HBM/AI 产线提高消耗 | Pellicle 供应成为 EUV mask 交期瓶颈 | 2027 High-NA/power 上升继续拉高 ASP。 |
| RDL/interposer/CoWoS-L masks | 已放量 | GB300/CoWoS-L、HBM3E、InFO/CoWoS-R 拉动 | OSAT 外溢，RDL mask 改版频率提高 | Rubin/MI400/HBM4 提前锁产能 | 2027 由 HBM4 与更大 package 带动二次增长。 |
| PLP/glass/ceramic core masks | 验证/小批量 | 2026 pilot | 2026H2 部分 ASIC/玻璃 core 试产 | 客户为 2028 提前 design-in | 2027 小批量收入，2028-2029 才大规模。 |
| CPO/硅光/NIL molds | 小规模 | switch/硅光/波导侧先行 | Spectrum-6/SPX、Broadcom switch 侧设计加速 | 光 I/O 提前导入 AI rack | 2027 小批量，2028 后放量。 |

## 3. 已经开始放量的关键产品：规模、渗透率与利润率

> 口径：未来 3 个月约等于 2026Q2-Q3 可确认收入/订单；未来 1 年为 2026-05 至 2027-05；未来 2 年为 2026-05 至 2028-05。金额为全球收入/订单池估算，含 captive transfer value 时已特别说明。

| 已放量产品 | 2026 状态 | 未来 3 个月市场规模：基准/乐观/极超 | 未来 1 年市场规模：基准/乐观/极超 | 未来 2 年市场规模：基准/乐观/极超 | 渗透率路径 | 毛利/利润率情景 |
|---|---|---:|---:|---:|---|---|
| EUV/先进逻辑 photomask | N5/N4/N3 HVM，2nm pilot | $0.35-0.55B / $0.50-0.75B / $0.75-1.05B | $1.7-2.4B / $2.3-3.2B / $3.0-4.3B | $3.8-5.5B / $5.2-7.5B / $7.0-10.5B | 先进逻辑关键层 EUV mask attach 接近 100%；2nm 占 EUV mask revenue 2026 <10%，2027 升至 15-30%。 | 高端 mask shop 毛利 40-60%；极缺时单 mask/NRE/expedite 可带 10-25% 溢价。 |
| ArF immersion/DUV 高端 mask | HBM/DRAM、N4/N3 非 EUV 层、国产 DUV 多重曝光 | $0.70-1.05B / $0.95-1.35B / $1.25-1.75B | $3.1-4.4B / $4.2-5.8B / $5.5-7.5B | $6.5-9.0B / $8.8-12.5B / $12.0-16.5B | 高端节点除 EUV critical layers 外仍大量使用 ArF；中国国产先进 DUV 使多重曝光层数提升。 | 毛利 30-50%；成熟产能有价格压力，高端/紧急交付可 45%+。 |
| HBM/DRAM 用 mask set | HBM3E 大量，HBM4 试产 | $0.25-0.45B / $0.40-0.65B / $0.60-0.95B | $1.2-1.9B / $1.8-2.8B / $2.6-4.2B | $2.5-4.0B / $4.0-6.5B / $6.0-9.5B | HBM wafer 与 EUV DRAM 层数增加；HBM4 base die/logic die 使高端 mask 占比提升。 | 与 memory 长协绑定，毛利 35-55%；HBM4 早期 50-65%。 |
| CoWoS/RDL/interposer/先进封装 mask | CoWoS-L/RDL 已进主线 | $0.12-0.25B / $0.20-0.35B / $0.35-0.55B | $0.55-0.95B / $0.85-1.35B / $1.25-2.05B | $1.2-2.3B / $2.0-3.8B / $3.2-6.0B | 高端 AI package 中 RDL/interposer mask 2026 渗透 55-70%，2027 70-85%；PLP/glass 小比例。 | 单价低于 EUV，但周转快；毛利 25-45%，紧缺或大尺寸低缺陷可 45-60%。 |
| Fan-out/WLP/PLP 大尺寸玻璃 mask | 手机/PMIC 迁移到 AI ASIC/硅光/PLP | $0.06-0.12B / $0.10-0.18B / $0.18-0.30B | $0.25-0.45B / $0.40-0.70B / $0.70-1.10B | $0.55-1.0B / $0.9-1.7B / $1.6-3.0B | 2026 仍以 WLP/fan-out 为主；PLP/glass core 2027 设计导入，2028 才大规模。 | 毛利 20-40%；大尺寸/高 overlay 要求可 40%+。 |
| EUV/ArF mask blanks | HOYA、Shin-Etsu、AGC 等供应集中 | $0.35-0.60B / $0.50-0.80B / $0.75-1.10B | $1.6-2.4B / $2.2-3.4B / $3.2-4.8B | $3.4-5.2B / $4.8-7.2B / $7.0-10.0B | EUV blank 随 advanced logic/HBM4/2nm 上升；多供趋势存在但认证慢。 | 高端 blank 毛利 45-65%；缺陷率领先者有高 ROIC。 |
| EUV/DUV pellicles | EUV pellicle 逐步成为 critical HVM 要求 | $0.10-0.15B / $0.13-0.20B / $0.18-0.28B | $0.43-0.60B / $0.55-0.85B / $0.80-1.20B | $0.90-1.25B / $1.20-1.80B / $1.70-2.60B | 2026 全球 pellicle 市场外部报告约 $433M；EUV/High-NA 占比上升。 | 普通 pellicle 30-45%；EUV 高性能 pellicle 45-70%。 |
| Mask writer、inspection、AIMS、repair 设备 | Mycronic/NuFlare/IMS/Lasertec/ZEISS/KLA 订单跨到 2027-2028 | $0.50-0.90B / $0.80-1.30B / $1.20-1.80B | $2.2-3.5B / $3.2-5.2B / $4.8-7.5B | $4.8-7.5B / $7.0-11.5B / $10.5-17.0B | EUV/curvilinear/2nm/High-NA 使 multi-beam writer 与 actinic inspection attach 上升。 | 设备毛利 45-65%；Lasertec 9M FY2026 operating margin 约 46%，说明高端检测具备极高利润弹性。 |
| OPC/ILT/curvilinear mask 数据与 EDA | 全芯片 ILT、curvilinear、AI OPC 渗透上升 | $0.12-0.22B / $0.18-0.32B / $0.28-0.50B | $0.55-0.90B / $0.85-1.35B / $1.3-2.2B | $1.2-2.0B / $2.0-3.4B / $3.2-5.5B | 高端 EUV tape-out 中渗透 2026 30-50%，2027 50-70%；先进封装 SI/PI/thermal co-design 也拉动。 | 软件/IP 毛利 80-95%，经营利润 25-45%；客户粘性极强。 |

### 3.1 已放量产品的增长区间

| 产品 | 未来 12 个月基准增长 | 乐观增长 | 极度超预期增长 |
|---|---|---|---|
| EUV/先进逻辑 photomask | +20-35% | +35-60% | +70-110% |
| ArF/DUV 高端 mask | +10-25% | +25-45% | +50-80% |
| HBM/DRAM mask | +35-60% | +60-100% | +100-160% |
| 先进封装 RDL/interposer mask | +45-80% | +80-130% | +140-220% |
| Mask blanks/pellicles | +25-55% | +50-90% | +90-150% |
| Mask equipment/inspection | +30-70% | +70-120% | +120-200% |

## 4. 在研和即将快速增长的关键产品

| 在研/早期导入技术 | 当前阶段 | 成熟/放量时间 | 未来 3 个月市场规模：基准/乐观/极超 | 未来 1 年市场规模：基准/乐观/极超 | 未来 2 年市场规模：基准/乐观/极超 | 渗透率路径 | 利润率判断 |
|---|---|---|---:|---:|---:|---|---|
| 2nm EUV photomask | DNP/Rapidus、IBM/Tekscend、Intel/Samsung/R&D | 2026 pilot，2027 初量产，2028 广泛 | $50-120M / $100-200M / $180-350M | $0.4-0.8B / $0.7-1.3B / $1.2-2.0B | $1.2-2.4B / $2.2-4.0B / $3.8-7.0B | 2026 EUV mask revenue <10%，2027 15-30%，2028 30%+ | 毛利 50-70%，NRE/快速交付溢价强。 |
| High-NA EUV mask/AIMS/pellicle | ZEISS AIMS 3.0、High-NA pilot、Intel/Samsung/imec | 2026 qualification，2027 pilot，2028+ HVM | $80-180M / $150-300M / $300-550M | $0.5-1.0B / $0.9-1.8B / $1.6-3.0B | $1.4-3.0B / $2.6-5.5B / $5.0-9.0B | 2027 前晶圆量小，但设备/资格验证先行 | 设备与材料毛利 50-70%；mask shop 初期良率风险大。 |
| Full-chip curvilinear/ILT mask | Multi-beam writer 与 EDA 进入可量产阶段 | 2026 关键层增加，2027 主流化 | $40-100M / $80-180M / $150-300M | $0.25-0.55B / $0.50-1.0B / $0.9-1.8B | $0.8-1.8B / $1.5-3.2B / $2.8-5.5B | EUV high-end tape-out 2026 30-50%，2027 50-70% | EDA/IP 80-95% 毛利；写入/检测设备 45-65%。 |
| EUV low-defect blanks + next-gen absorber | HOYA/Shin-Etsu/AGC/S&S Tech 等 | 持续迭代，2nm/High-NA 2027 抬升 | $80-160M / $150-280M / $250-450M | $0.6-1.0B / $0.9-1.6B / $1.5-2.6B | $1.4-2.6B / $2.4-4.5B / $4.0-7.5B | EUV mask blank 中 next-gen 占比 2026 <20%，2027 30-45% | 高端 blank 50-70% 毛利可能，缺陷率领先者高 ROIC。 |
| 玻璃/陶瓷 core 与 panel-level packaging masks | TOPPAN、DNP、Intel、Samsung、Kyocera、Corning/AGC 等验证 | 2026 eval，2027 pilot，2028-2029 放量 | <$50M / $50-120M / $120-250M | $0.15-0.35B / $0.30-0.70B / $0.70-1.30B | $0.6-1.4B / $1.2-2.8B / $2.5-5.5B | 2027 先进封装 mask 中 <10%，2028 可到 10-25% | 初期亏损/低毛利，量产成熟后 35-55%。 |
| CPO/硅光/光波导/NIL molds | Tekscend 扩展 nanoimprint molds/waveguides，EVG/Tekscend 早有合作 | 2026 小批，2027 switch side，2028+ | <$50M / $50-100M / $100-180M | $0.1-0.25B / $0.25-0.55B / $0.50-1.0B | $0.5-1.2B / $1.0-2.5B / $2.0-5.0B | CPO 在交换芯片侧 2026 <5%，2027 5-12%，2028 10-25% | 模具/高精度 mask 40-65%，但良率和生态风险高。 |
| AI 自动化 mask shop | Tekscend Singapore 明确 AI scheduling/automation | 2026 建设，2027-2028 复制 | $20-80M / $50-150M / $100-300M | $0.2-0.5B / $0.4-0.9B / $0.8-1.5B | $0.6-1.2B / $1.0-2.2B / $2.0-4.0B | 先在新厂/高端产线导入，2027 成为降成本工具 | 软件/自动化 40-70% 毛利；收益体现为 mask shop 交期和良率。 |
| 大尺寸 6x12 英寸/替代 reticle 研究 | High-NA 半场曝光和 stitching 问题引发讨论 | 2026-2027 研究，HVM 不确定 | 极小 | <$0.2B | $0.2-1.0B 期权 | 不是 2027 主线，但若行业改变 reticle format，弹性巨大 | 高风险高壁垒，短期不作为基准投资主线。 |

## 5. 供给侧：产能结构、瓶颈、成本与价格传导

### 5.1 产能结构

| 层级 | 主要地区 | 主要公司 | 工艺/产品 |
|---|---|---|---|
| Captive mask shop | 台湾、韩国、美国、日本、中国 | TSMC、Samsung、Intel、SK hynix、Micron、SMIC、Rapidus 生态 | 最先进节点、内部 tape-out、快速改版、保密项目。SEMI 样本称 captive mask houses 仍占最大份额。 |
| Merchant photomask | 日本、美国、台湾、中国、欧洲、新加坡、韩国 | Tekscend/Toppan、DNP、Photronics、Taiwan Mask、SK Electronics、Compugraphics、清溢光电、路维光电等 | EUV/ArF/KrF/i-line、mature-node、FPD、advanced packaging、MEMS/硅光。 |
| EUV/DUV blanks | 日本、新加坡、韩国、美国 | HOYA、Shin-Etsu、AGC、S&S Tech、FST、Applied/Veeco 相关材料设备生态 | EUV multilayer blanks、quartz blank、low-defect substrate、absorber、pellicle。 |
| Mask writers | 日本、奥地利/欧洲、瑞典、德国 | NuFlare、IMS Nanofabrication、Mycronic、Vistec | Multi-beam eBeam、variable-shape eBeam、laser writer、display/packaging writer。 |
| Inspection/qualification/repair | 日本、美国、德国、以色列 | Lasertec、KLA、ZEISS SMT、Applied Materials、NuFlare、Bruker/RAVE、Park Systems、JEOL/Hamamatsu 等 | Actinic inspection、blank inspection、CD-SEM、AIMS、repair、cleaning、metrology。 |
| OPC/EDA/data | 美国、欧洲、以色列、日本 | Synopsys、Cadence、Siemens EDA、ASML Brion、D2S、KLA、PDF Solutions、Ansys/Keysight | OPC、ILT、curvilinear、mask data prep、fracturing、litho simulation、process window control。 |
| Advanced packaging mask | 台湾、日本、韩国、中国、东南亚、美国 | TSMC、ASE/SPIL、Amkor、JCET、Samsung、Intel、Powertech、Nepes、Tongfu、Huatian、DNP/TOPPAN/Tekscend/Photronics | RDL/interposer/fan-out/WLP/PLP/glass core/CPO/NIL molds。 |

### 5.2 至少 8 条供给瓶颈

1. **Multi-beam writer 交期和良率爬坡**：EUV/curvilinear/2nm mask 依赖 IMS/NuFlare 高端 writer；Mycronic 2026 订单交付已排到 2027-2028。  
2. **EUV blank defect density**：EUV blank 是反射式多层膜结构，mask 缺陷比 DUV 更难发现和修补；低缺陷 blank 决定高端 mask 有效产出。  
3. **Actinic inspection/AIMS 吞吐**：ZEISS AIMS EUV 3.0 虽提升吞吐 3 倍，但关键芯片的 defect printability 仍需要资格验证，设备数量少。  
4. **Pellicle 热稳定与透过率**：高功率 EUV/High-NA 使 pellicle 更接近材料极限，缺货会直接卡 HVM。  
5. **OPC/ILT 数据和工程人才**：curvilinear/ILT 带来数据量和写入时间上升，mask shop 需要 EDA、HPC、工艺模型和资深工程师。  
6. **客户认证不可压缩**：新 mask shop、新 blank、新 pellicle、新 writer 要经过 design rule、defect spec、清洗、运输、寿命和 wafer print 验证。  
7. **区域化导致重复建设但短期低效率**：新加坡、韩国、欧洲、美国本地 mask 产能增加韧性，但早期良率/稼动率不如成熟基地。  
8. **先进封装 mask 的碎片化订单管理**：RDL/interposer/fan-out 层数多、版图改动频繁、客户 NPI 周期短，排产难度高。  
9. **数据安全和出口管制**：先进 mask 数据本质上是芯片版图核心 IP，跨境数据、设备出口和客户保密会限制供应弹性。  
10. **清洗/修补/物流**：高端 reticle 对粒子极敏感，跨境运输、pellicle 安装、清洗次数和修补能力都会影响交期。

### 5.3 成本与单位价格拆分

| 产品 | 典型单价区间 | 成本构成 | 毛利决定因素 |
|---|---:|---|---|
| EUV reticle | $300k-$1.2M+ / 张；整套先进节点 mask set 可达 $15-50M+ | EUV blank 25-45%；writer 折旧/写入 20-30%；inspection/AIMS/repair 15-25%；OPC/data 5-15%；良率/清洗/人工 10-20% | blank defect、写入时间、AIMS 瓶颈、客户加急、2nm/High-NA 难度。 |
| ArF immersion high-end mask | $50k-$300k / 张 | quartz blank 15-30%；eBeam/laser 写入 20-30%；检测/修补 15-25%；OPC 10-20%；折旧/人工 15-25% | 多重曝光层数、CD/overlay spec、成熟稼动率、区域供应。 |
| Mature-node mask | $5k-$80k / 张 | blank 和写入设备折旧占比高 | 竞争更激烈，毛利低于先进 mask。 |
| Advanced packaging RDL/interposer mask | $5k-$150k / 张；大尺寸/高精度可更高 | glass mask substrate/Cr 20-35%；laser/eBeam/LDI 数据 20-30%；inspection 10-20%；良率/清洗/物流 15-25% | 大尺寸 overlay、低缺陷、快速改版、与 OSAT/foundry 认证绑定。 |
| Panel-level/glass-core mask | $20k-$300k / 套/项目，取决于尺寸和层数 | 大尺寸基板、写入/检测、翘曲与热稳定控制 | PLP 良率和客户设计导入，2026-2027 初期项目制毛利分化大。 |
| EUV blank/pellicle | blank 单价可达数万至十万美元级；pellicle 数千至数万美元级 | 基板/多层膜/absorber/膜材料/缺陷检测/认证 | 缺陷率、透过率、热寿命、客户认证数量。 |

### 5.4 价格传导机制

- AI 客户先看交期和良率，再看单张 mask 价格；mask 成本在先进 AI 芯片总成本中占比很小，但 delay 会影响数十亿美元芯片/机架收入。  
- Foundry/IDM 可通过 mask set NRE、expedite fee、engineering change order、capacity reservation 和 long-term agreement 传导成本。  
- Merchant mask shop 在 mature-node 上传导弱，在 EUV/2nm/curvilinear/RDL 大尺寸上更强。  
- Blank、pellicle、inspection 设备供应商因认证周期长、替代少，价格传导强于普通 mask shop。  
- 如果 2027 新产能过快释放，低端/普通 mask 会先降价；EUV blank、actinic inspection、2nm mask、先进封装大尺寸 RDL 仍偏紧。

## 6. 竞争格局与壁垒

### 6.1 市场结构

| 细分 | 集中度判断 | 主要公司 |
|---|---|---|
| Captive high-end mask | 极高，先进节点由 foundry/IDM 自有 mask shop 主导 | TSMC、Samsung、Intel、SK hynix、Micron、SMIC、Rapidus 生态 |
| Merchant semiconductor photomask | 高度集中，Tekscend/DNP/Photronics 是全球核心，区域厂补充 | Tekscend/Toppan、DNP、Photronics、Taiwan Mask、SK Electronics、Compugraphics、清溢光电、路维光电 |
| EUV mask blanks | 极高 | HOYA、Shin-Etsu、AGC、S&S Tech、FST 等 |
| Multi-beam/eBeam mask writers | 极高，几乎双寡头/少数供应 | NuFlare、IMS Nanofabrication、Mycronic、Vistec |
| Actinic/blank inspection/AIMS | 极高 | Lasertec、KLA、ZEISS SMT、Applied Materials、NuFlare |
| OPC/ILT/EDA | 极高 | Synopsys、Cadence、Siemens EDA、ASML Brion、D2S、KLA |
| Advanced packaging masks | 中等集中，客户认证后集中度提升 | TSMC、ASE、Amkor、JCET、DNP、Tekscend、Photronics、TOPPAN、Samsung、Intel、Nepes |

### 6.2 可量化壁垒：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| 设备资本壁垒 | 一台高端 writer/inspection/AIMS 设备动辄数百万到数千万美元，Mycronic 2026 单台 customized SLX 订单 $27-30M，交期到 2028；产能无法快速复制。 |
| 缺陷率壁垒 | EUV blank 和 reticle defect 会直接变成 wafer yield loss，客户愿意为更低 defect 和更短 debug 时间付溢价。 |
| 数据和模型壁垒 | OPC/ILT model、process window、defect database、repair recipe 来自长期量产数据，后进入者无法用价格复制。 |
| 客户认证壁垒 | 换 mask shop 意味着重新验证 CD、overlay、cleaning、pellicle、inspection、shipping 和 wafer print，可能错过整代芯片窗口。 |
| IP/安全壁垒 | Photomask 数据包含完整版图，客户更愿意绑定少数可信供应商。 |
| 区域交付壁垒 | 高端 mask 需要近场支持，Tekscend 新加坡/韩国/欧洲扩产说明地理位置本身能定价。 |
| 规模壁垒 | 高端 mask shop 需要大量设备摊薄折旧；低稼动率会迅速侵蚀利润。 |
| 生态壁垒 | 与 foundry PDK、EDA、scanner、resist、pellicle、inspection tool 的协同决定能否量产。 |

### 6.3 价值捕获判断

长期高 ROIC/高毛利最可能出现在五层：

1. **EUV blank / pellicle / actinic inspection**：供应少、认证长、单点卡线，价格弹性最大。  
2. **Multi-beam writer、AIMS、mask repair/inspection 设备**：订单领先收入，设备和服务利润率高，2026-2028 能见度强。  
3. **先进 EUV/2nm merchant mask shop**：DNP、Tekscend、Photronics 等若进入客户核心供应链，可享受 NRE、加急和区域化溢价。  
4. **OPC/ILT/EDA 和 mask data platform**：收入体量小于硬件，但毛利最高、粘性最强。  
5. **先进封装 RDL/interposer mask**：短期毛利不如 EUV，但 CoWoS-L、HBM4、PLP、CPO 会提升技术含量和周转频率。

普通成熟节点 mask、低端显示 mask、非 AI 普通 packaging mask 的 ROIC 较弱，除非绑定本土替代或区域化政策。

## 7. 2026 关键变化：3 个最可能拐点

### 拐点 1：GB300/Blackwell Ultra 把“成熟 EUV + RDL mask”同时打满

2026 真正能确认的大量不是 High-NA，而是 N4/N3/4NP 级低 NA EUV、ArF immersion 和 CoWoS-L/RDL 的组合。GB300/B300、GB200、MI350、Ironwood、Trainium2/3 会让 photomask 从前端到封装端同时高稼动。最直接受益是 EUV/ArF mask、HBM mask、RDL/interposer mask、blank、pellicle、inspection。

### 拐点 2：Custom ASIC 从 GPU 补充变成独立 mask 需求池

Meta/Broadcom、OpenAI/Broadcom、Google TPU、AWS Trainium、Microsoft Maia 的共同特征是多代并行、快速 tape-out、内部规模大但对供应链保密。它们对 merchant mask 的公开收入未必完全可见，但会实实在在占用 advanced node mask、OPC/ILT、HBM base die 和封装 mask 产能。

### 拐点 3：高端 mask 区域化从口号进入 capex

Tekscend 韩国第三工厂、新加坡新厂、法国 SLX1、DNP/Rapidus、Photronics 区域布局，说明客户不再只追求最低 mask 成本，而是追求“靠近 fab、靠近材料、靠近客户工程”的供应韧性。区域化会抬高行业 capex，但也使高端供应商议价权提升。

## 8. 2027 关键变化：3 个最可能拐点

### 拐点 1：2nm/HBM4/Rubin/MI400/TPU8 触发第二轮高端 mask 紧缺

2027 的核心不是 photomask 总量线性增长，而是难度结构上移：2nm EUV、HBM4、更多 chiplet、更大 RDL/interposer、更多 recut 和更长 qualification。DNP/Rapidus 2027 量产目标、Rubin/MI400/TPU8/MTIA/OpenAI XPU 放量，会使 2nm EUV mask、HBM4 mask 和 actinic inspection 成为二次瓶颈。

### 拐点 2：Curvilinear/ILT 与 multi-beam writer 从“技术亮点”变成产能前提

随着低 NA EUV 多重 patterning 延寿和 2nm 设计复杂度提升，full-chip curvilinear/ILT 的经济性上升。multi-beam writer 不只是更快，而是能写传统 VSB 难以经济完成的复杂图形。OPC/ILT 数据处理会成为 mask shop 的新产能指标。

### 拐点 3：先进封装 mask 从 RDL 扩展到 glass/PLP/CPO

2027 不是 glass core/PLP/CPO 最大收入年，但可能是 design-in 胜负年。拿到头部 GPU/ASIC/switch 的 glass core、CPO optical package、panel-level RDL 掩模资格的公司，2028-2029 赔率很高。

## 9. 头部公司与技术地图

### 9.1 光罩制造：merchant 与 captive

| 类别 | 公司 |
|---|---|
| 全球 merchant photomask | Tekscend Photomask/Toppan Photomask、Dai Nippon Printing/DNP、Photronics、Taiwan Mask、SK Electronics、Compugraphics、Hoya Photomask legacy、AMTC Dresden ecosystem |
| Captive/准 captive | TSMC、Samsung、Intel、SK hynix、Micron、SMIC、UMC、GlobalFoundries、Rapidus/IBM Albany 生态、Texas Instruments、Sony Semiconductor、Renesas |
| 中国大陆 | 清溢光电、路维光电、无锡中微掩模、深圳龙图光罩、华润微/中芯/华虹相关内部或配套 mask 生态 |
| FPD/大尺寸 mask | DNP、Photronics、HOYA、LG Innotek 相关、SKE、清溢光电、路维光电 |

### 9.2 Mask blanks、pellicles、材料

| 领域 | 公司 |
|---|---|
| EUV/DUV mask blanks | HOYA、Shin-Etsu Chemical、AGC、S&S Tech、FST、Applied Materials ecosystem、DNP/TOPPAN 相关材料能力 |
| Quartz/glass substrate | HOYA、AGC、Shin-Etsu、Tosoh、Nikon glass ecosystem、Corning、Schott、Ohara |
| EUV pellicle | ASML ecosystem、Mitsui Chemicals、Shin-Etsu、S&S Tech、FST、IMEC partners、Samsung/SK ecosystem |
| Absorber/multilayer/IBD | Veeco、Ion Beam deposition ecosystem、Shin-Etsu、HOYA、AGC、Applied Materials |
| Cleaning/chemicals | Entegris、Merck/EMD、DuPont、JSR、TOK、Kanto Chemical、Stella Chemifa、Kuraray 等 |

### 9.3 写入、检测、修补、资格验证设备

| 环节 | 公司 |
|---|---|
| Multi-beam eBeam writer | NuFlare Technology、IMS Nanofabrication |
| Variable-shape eBeam writer | NuFlare、JEOL、Vistec |
| Laser mask writer | Mycronic、Heidelberg Instruments、Durham/legacy laser writer ecosystem |
| Display/advanced packaging writer | Mycronic Prexision/FPS/SLX、Heidelberg Instruments、EV Group/NIL ecosystem、SUSS MicroTec、Onto/JetStep ecosystem |
| Blank/reticle inspection | Lasertec、KLA、Applied Materials、NuFlare、Onto Innovation、Camtek、Lasertec EUV actinic ecosystem |
| AIMS/actinic qualification | ZEISS SMT AIMS EUV、ASML/ZEISS ecosystem |
| Repair/cleaning | Bruker/RAVE、ZEISS、KLA、Park Systems、PVA TePla、SCREEN、Tokyo Electron、SUSS/EVG 相关 |
| CD-SEM/metrology | KLA、Applied Materials、Hitachi High-Tech、JEOL、Nova、Onto Innovation |

### 9.4 EDA、OPC、ILT、mask data

| 环节 | 公司 |
|---|---|
| OPC/RET/ILT | Synopsys、Cadence、Siemens EDA、ASML Brion、D2S、KLA、Mentor Calibre ecosystem |
| Lithography simulation | ASML Brion、Synopsys Proteus/Sentaurus、Cadence、Siemens、Ansys、Fraunhofer/imec/IBM ecosystem |
| Mask data prep/fracturing | Synopsys、Siemens EDA、Cadence、D2S、Aselta Nanographics、KLA |
| AI mask shop scheduling/automation | Tekscend internal systems、Applied/KLA/Siemens/MES ecosystem、PDF Solutions、Onto/Factory analytics |

### 9.5 先进封装掩模与应用客户

| 领域 | 公司 |
|---|---|
| CoWoS/RDL/interposer | TSMC、ASE/SPIL、Amkor、Samsung、Intel、JCET、Tongfu、Powertech、Nepes、Huatian、DNP、Tekscend、Photronics |
| Fan-out/WLP/PLP | TSMC InFO、ASE FOCoS、Amkor SWIFT/SLIM、JCET XDFOI、Samsung、Powertech、Nepes、Deca、SUSS/EVG/Mycronic ecosystem |
| Glass/ceramic core | Intel、Samsung Electro-Mechanics、TOPPAN、DNP、Kyocera、Corning、AGC、Schott、Absolics、NGK、CoorsTek |
| CPO/硅光/光波导/NIL molds | Broadcom、Coherent、Lumentum、Ayar Labs、Lightmatter、GlobalFoundries/AMF、Intel Silicon Photonics、Tekscend nanoimprint/waveguide、EV Group、SUSS |
| 主要 AI 客户 | NVIDIA、AMD、Broadcom、Marvell、Google、AWS、Meta、Microsoft、OpenAI、Huawei、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Cerebras、Groq、Tenstorrent、d-Matrix、Etched |

## 10. 情景模型汇总

### 10.1 2026-2027 市场规模

| 收入池 | 2026 基准 | 2026 乐观 | 2026 极超 | 2027 基准 | 2027 乐观 | 2027 极超 |
|---|---:|---:|---:|---:|---:|---:|
| 全球 photomask 总市场 | $5.9-6.7B | $6.7-7.8B | $7.8-9.2B | $6.5-7.8B | $7.8-9.8B | $9.8-12.5B |
| EUV/先进逻辑 mask | $1.7-2.4B | $2.3-3.2B | $3.0-4.3B | $2.2-3.4B | $3.2-5.0B | $5.0-7.5B |
| ArF/DUV 高端 mask | $3.1-4.4B | $4.2-5.8B | $5.5-7.5B | $3.4-4.8B | $4.8-6.8B | $6.8-9.5B |
| 先进封装 mask | $0.45-0.80B | $0.75-1.15B | $1.10-1.80B | $0.75-1.30B | $1.20-2.20B | $2.20-3.80B |
| Mask blanks + pellicles | $2.0-3.0B | $2.7-4.2B | $4.0-6.0B | $2.6-4.0B | $4.0-6.5B | $6.2-9.5B |
| Mask equipment/inspection/AIMS/repair | $2.2-3.5B | $3.2-5.2B | $4.8-7.5B | $2.6-4.5B | $4.5-7.8B | $7.5-12.5B |
| OPC/ILT/mask data | $0.55-0.90B | $0.85-1.35B | $1.3-2.2B | $0.75-1.3B | $1.3-2.4B | $2.4-4.0B |

### 10.2 关键假设

| 变量 | 基准 | 乐观 | 极度超预期 |
|---|---|---|---|
| AI demand | GB300/ASIC 稳定，Rubin/MI400 2027 放量 | Blackwell Ultra、ASIC、HBM4 均顺利 | 2027 需求提前到 2026H2，客户愿意用高价锁 mask/blank/inspection |
| 先进节点 | N3/N4 仍主力，2nm pilot | 2nm mask 在 2026H2 明显增加 | 多个 AI ASIC 2nm 提前 tape-out |
| High-NA | R&D/pilot，不是 2026 收入主力 | Intel/Samsung/imec 拉动资格验证 | 设备/材料/资格验证订单提前，虽然 wafer volume 仍小 |
| 先进封装 | CoWoS-L/RDL 放量 | OSAT 外溢、PLP/glass design-in | Rubin/MI400/HBM4 提前拉爆 RDL/interposer mask |
| 价格 | 高端稳定，普通 mask 平 | 高端 mask/blank/pellicle 加价 | 加急费、NRE、capacity reservation 普遍化 |

## 11. 投资观察清单

| 优先级 | 子方向 | 看多理由 | 主要风险 |
|---:|---|---|---|
| 1 | EUV blank/pellicle/actinic inspection | 单点卡线，认证长，利润率最高 | 客户多供、High-NA 放量晚于预期 |
| 2 | Multi-beam writer/AIMS/mask repair | 订单已排到 2027-2028，curvilinear/2nm 必需 | 设备验收延迟、客户 capex 波动 |
| 3 | DNP/Tekscend/Photronics 高端 mask | 直接受 AI/2nm/区域化拉动 | Captive mask shop 挤压 merchant 份额 |
| 4 | 先进封装 RDL/interposer mask | CoWoS-L/HBM4/PLP/CPO 带来高增速 | 单价低、竞争者较多、部分被 maskless/LDI 替代 |
| 5 | OPC/ILT/EDA | 毛利高、粘性强，curvilinear 提升 ASP | 体量小，集成在大 EDA 公司里弹性被稀释 |
| 6 | 中国本土 photomask | 国产替代、DUV 多重曝光、成熟制程扩产 | 高端设备/blank 受限，毛利和技术上限分化 |

## 12. 风险提示

1. AI capex 或 token ROI 不及预期，导致 2027 ASIC/GPU tape-out 延后。  
2. 2nm、HBM4、High-NA、curvilinear、PLP/glass core 技术验证慢于预期。  
3. Captive mask shop 扩张后压缩 merchant mask 可见市场。  
4. 普通 mature-node mask 产能过剩，掩盖高端结构性紧缺。  
5. 出口管制、数据跨境和客户 IP 安全限制 merchant 供应弹性。  
6. 本文对先进封装 mask、CPO/NIL、2nm AI ASIC 的市场规模做了乐观推演，不能与公开公司营收简单相加。

## 13. 主要来源

| 类别 | 来源 |
|---|---|
| Photronics 2026Q1 | [Photronics Reports First Quarter Fiscal 2026 Results](https://photronicsinc.gcs-web.com/news-releases/news-release-details/photronics-reports-first-quarter-fiscal-2026-results), [Photronics 10-Q, filed 2026-03-11](https://photronicsinc.gcs-web.com/node/19296/html) |
| DNP/Rapidus | [DNP Invests in Rapidus, 2026-02-27](https://www.global.dnp/en/news/detail/2026/02/0227_20177963/), [DNP FY2025 financial results PDF](https://www.global.dnp/content/dam/dnp-global/pdf/en/ir/library/result/dnp_e_24Q4fin.pdf) |
| Tekscend/Toppan | [Tekscend Korea Icheon MOU PDF, 2026-03-30](https://www.photomask.com/en/news/file/20260330Tekscend%20Photomask%20and%20Icheon%20City%2C%20South%20Korea.pdf), [Singapore Factory PDF, 2025-10-31](https://www.photomask.com/en/news/file/Groundbreaking%20Ceremony_20251031.pdf), [Europe SLX1 investment, 2025-07-21](https://www.photomask.com/en/news/topic/20250721163246.html), [IBM EUV joint R&D, 2024-02-07](https://www.photomask.com/en/news/press/20240207155645.html) |
| Mycronic | [Q1 2026 interim report](https://www.mycronic.com/news-events/our-press-releases/interim-report-january-march-2026/), [SLX order $27-30M, 2026-04-14](https://www.mycronic.com/product-areas/photomask-equipment/press-releases/mycronic-receives-order-for-an-slx-mask-writer10/), [SLX order $5-7M, 2026-03-27](https://www.mycronic.com/product-areas/photomask-equipment/press-releases/mycronic-receives-order-for-an-slx-mask-writer9/), [Prexision 8 Evo order, 2026-02-04](https://www.mycronic.com/product-areas/photomask-equipment/press-releases/mycronic-receives-order-for-a-prexision-8-evo2/), [MMX metrology order, 2026-01-23](https://www.mycronic.com/product-areas/photomask-equipment/press-releases/mycronic-receives-order-for-an-mmx-metrology-system/), [FPS 6100 Evo electronic packaging order, 2025-12-30](https://www.mycronic.com/product-areas/photomask-equipment/press-releases/mycronic-receives-order-for-an-fps-6100-evo/) |
| Lasertec | [Lasertec consolidated results for 3Q FY2026](https://ca.marketscreener.com/news/lasertec-consolidated-financial-results-for-the-third-quarter-ended-march-31-2026-japanese-gaap-ce7f58dbda89fe2c) |
| ZEISS | [AIMS EUV 3.0 press release, 2026-02-04](https://www.zeiss.com/semiconductor-manufacturing-technology/news-and-events/smt-press-releases/2026/aims-euv-3-0-global-footprint.html) |
| NuFlare | [NuFlare EB Mask Writer product roadmap](https://www.nuflare.co.jp/english/products/beam/) |
| SEMI | [Photomask Market Characterization Report page](https://www.semi.org/en/products-services/market-data/photomask-characterization), [SEMI Market Data Pulse sample PDF](https://www.semi.org/sites/semi.org/files/2024-07/Market-Data-Pulse-Newsletter-2Q24-01.pdf) |
| HOYA | [HOYA Integrated Report 2025](https://www.hoya.com/ir/2025/en/common/files/online_report2025.pdf), [HOYA Information Technology review](https://www.hoya.com/ir/2023/en/review/it.html) |
| Veeco | [Veeco Q1 2026 earnings presentation](https://s1.q4cdn.com/522285864/files/doc_financials/2026/q1/Q12026EarningsPresentation2026-05-05FINAL.pdf) |
| 市场规模交叉验证 | [IMARC Photomask Market 2026-2034](https://www.imarcgroup.com/global-photomask-market), [Grand View Research Photomask Market](https://www.grandviewresearch.com/industry-analysis/photomask-market-report), [Fact.MR Pellicle Market](https://www.factmr.com/report/pellicle-market), [SemiconductorInsight Advanced Packaging Photomask Market](https://semiconductorinsight.com/report/advanced-packaging-photomask-market/) |
| 项目内资料 | `ai_chip_research_2026_2027.md`, `AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026.md`, `AI服务器_存储_芯片/行业调研_封装基板_中介层与RDL_2026-05-08.md` |
# 行业调研：【高速互连与光学验证测试】

截至日期：2026-05-08  
研究口径：本报告研究 AI 计算中心内外的高速互连与光学验证测试产业，覆盖 800G/1.6T/3.2T 光模块、光芯片、硅光、CPO/CPX/NPO/XPO、OCS、coherent DCI、AEC/ACC/DAC、CPC/top-side/flyover 铜互连、PCIe/CXL/UALink/UEC、Retimer/Fabric Switch/SerDes/DSP、光电验证测试设备与量产测试。  
核心假设：对 2026-2027 AI 基础设施建设保持非常乐观；对于无法直接公开验证的数据，采用“从 GPU/XPU 出货、交换端口、光模块 attach rate、ASP 与测试工时”反推的乐观估计。项目内 AI 芯片路线图已经给出 2026/2027 出货主力，本报告不再外部搜索芯片路线，只把它作为需求侧背景。

## 0. 高浓度结论

2026 年高速互连与光学验证测试的主线是：AI 数据中心从“买 GPU/ASIC”进入“让 XPU 持续满载”的物理层扩建期。算力芯片价值越高，客户越愿意为网络、光模块、Retimer、连接器、测试设备付溢价，因为互连故障、抖动、FEC 重传、光链路 flap、端口拥塞会直接降低 GPU 利用率和 token 产能。

最核心的判断：

| 判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 全球 AI 高速互连与光学验证测试收入池 | $75B-$105B | $105B-$145B | $150B-$210B |
| 2027 全球 AI 高速互连与光学验证测试收入池 | $120B-$170B | $180B-$260B | $300B-$430B |
| 2026 最确定放量 | 800G 光模块、1.6T 初期、224G 电接口、AEC/ACC、PCIe Gen6 Retimer/Switch、1.6T/224G 测试 | 1.6T 更快替代 800G，Google/Ironwood、NVIDIA GB300、AWS Trainium2 同时拉货 | 1.6T 和 224G 长时间供不应求，测试设备和关键光芯片成为真实瓶颈 |
| 2027 最大弹性 | 3.2T/400G-per-lane、CPO/CPX、XPO、OCS、1600ZR/ZR+、UALink/UEC scale-up | Rubin、MI400/Helios、TPU8、Trainium3 把 CPO/XPO/3.2T 验证前置 | 204.8T 交换平台提前，3.2T 在 2027 形成十亿美元级早期收入 |

关键公开数字：

- NVIDIA FY2026 数据中心收入 $193.7B，Q4 数据中心收入 $62.3B，同比增长 75%；NVIDIA 称 agentic AI 拐点已到，客户正在投资 AI factories。
- Dell FY2026 关闭超过 $64B AI-optimized server 订单，全年出货超过 $25B，FY27 期初 backlog $43B，并指引 FY2027 AI server revenue 约 $50B。
- Broadcom Q1 FY2026 AI revenue $8.4B，同比增长 106%，Q2 AI semiconductor revenue 指引 $10.7B；同时在 OFC 2026 展示 3.5D XPU、102.4T Ethernet switch with CPO、400G/lane Taurus optical DSP、200G/lane Retimer/AEC、PCIe Gen6 Switch/Retimer。
- TrendForce 预计 AI 专用光收发模块市场从 2025 年 $16.5B 增至 2026 年 $26B，同比超过 57%；800G 及以上模块出货占比从 2024 年 19.5% 升至 2026 年 60%+。
- Cignal AI 预计 2025 optical components revenue 接近 $25B，其中 datacom 超过 $18B、coherent module 接近 $6B；400G+ datacom module 2025 出货约 4,200 万只，1.6TbE 2026 快速增长。
- Dell'Oro 预计 AI back-end switch market 到 2030 年超过 $100B；AI 后端交换端口已经以 800G 为主，预计 2027 转向 1.6T、2030 转向 3.2T。
- PCI-SIG 2026-05-01 发布 PCIe 8.0 draft 0.5，目标 256.0GT/s、x16 双向 1.0TB/s、2028 完成，并明确评估新连接器技术；PCIe 7.0 已在 2025-06-11 发布，128.0GT/s、x16 双向 512GB/s。
- Keysight 2026-03 推 224G/1.6T optical network validation 方案，覆盖 IEEE 802.3dj 光/电发送端一致性、TDECQ/TDECQ-CER、DCA sampling oscilloscope，从 R&D 到高量产测试。
- VIAVI 在 OFC 2026 推 TestCenter D2 1.6T Appliance；其 ONE-1600ER 支持 IEEE 802.3dj 的 1.6TE MAC、2x800GE、4x400GE、8x200GE、FEC、224G SerDes。
- NVIDIA Spectrum-X Ethernet Photonics 宣称相对传统 pluggable，CPO/硅光每 1.6Tb/s 端口功耗降低 5x、link flap-free uptime 提高 5x、network resiliency 提高 10x，SN6800 总带宽 409.6Tb/s。

一句投资结论：2026 年收入确定性最高的是 800G/1.6T 光模块、224G/1.6T 测试、AEC/ACC、PCIe Gen6 Retimer/Switch；2027 年赔率最高的是 3.2T/400G-lane、CPO/CPX/XPO、OCS、coherent scale-across、UALink/UEC scale-up，以及把这些东西量产化的测试与校准设备。

## 1. 2026 AI 计算中心建设中的机遇、挑战与技术路径

### 1.1 需求侧背景：项目内 AI 芯片路线对互连的牵引

项目内 AI 芯片路线图显示，2026-2027 年初出货量和价值权重最大的 AI 平台包括：

| 需求主力 | 2026/2027 节奏 | 对高速互连/验证测试的直接拉动 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主力放量，2027 上半年仍有大量交付 | NVLink/rack 内铜互连、800G/1.6T scale-out 光模块、Spectrum-X/IB 交换、液冷下光电可靠性、1.6T 测试 |
| AWS Trainium2/Trainium3 | Trainium2 2026 大规模，Trainium3 2026 起步、2027 放量 | EFA/以太网 scale-out、NeuronLink/NeuronSwitch、PCIe/CXL 周边、800G/1.6T 光模块、rack burn-in |
| Google TPU v7 Ironwood/TPU8 | Ironwood 2026 放量，TPU8 2027 扩张 | 3D Torus、Apollo OCS、800G+ 光模块、短距铜 + 跨机柜全光网络、OCS 测试 |
| NVIDIA GB200/B200 | 2026 存量订单延续 | 800G、NVLink、PCIe Gen5/6、Retimer、光模块持续需求 |
| Huawei Ascend 910C/950、Cambricon 590/690 | 中国国产替代，2026-2027 高增长 | 国产光模块、800G/1.6T、PCIe/以太网 Retimer、国产测试设备、OAM 模组测试 |
| AMD MI350/MI400 Helios | MI350 2026 放量，MI400/Helios 2026H2-2027 接棒 | UALink/UALoE、开放 Ethernet fabric、1.6T、CPO/XPO 可选、PCIe Gen6/7 生态 |
| Meta MTIA、Microsoft Maia、OpenAI/Broadcom ASIC | 2026 小到中量，2027 放大 | Broadcom/Marvell custom XPU + Ethernet/PCIe/SerDes/DSP 绑定，CPO/OCS/光模块需求上升 |

核心推论：2026 真正大规模交付的芯片仍以 Blackwell Ultra、Trainium2、Ironwood、GB200/B200、MI350、国产替代为主，所以 2026 互连最可能的收入路径不是 3.2T/CPO 一步到位，而是 800G+1.6T pluggable、224G lane、AEC/ACC、PCIe Gen6 Retimer/Switch、1.6T 验证设备。2027 因 Rubin、MI400/Helios、TPU8、Trainium3、custom ASIC 增量，CPO/CPX/XPO、3.2T/400G/lane、UALink/UEC、OCS 才会明显放量。

### 1.2 2026 机遇

| 机遇 | 为什么在 2026 放大 | 受益环节 |
|---|---|---|
| 800G 到 1.6T 的光模块升级 | AI 后端网络从 400G/800G 走向 800G/1.6T；Google OCS 架构要求从设计阶段配置足够 800G/1.6T 光模块 | Innolight、Eoptolink、Coherent、Lumentum、Fabrinet、Foxconn Industrial Internet、Accelink、Hisense、Source Photonics |
| 224G electrical lane 成为主流验证对象 | 1.6T OSFP 通常需要 8x200G/224G host electrical interface；IEEE 802.3dj 推动 224G 光/电一致性 | Keysight、VIAVI、Anritsu、Tektronix、Teledyne LeCroy、Rohde & Schwarz |
| AEC/ACC 与 CPC/top-side 铜互连延长铜的生命 | 近 ASIC、板内、柜内 2-7m 场景，铜比光更低延迟、更易维护、更低成本 | Credo、Astera、Broadcom、Marvell、Luxshare、Amphenol、TE、Molex、Samtec、BizLink、FIT |
| Retimer/Fabric Switch 从配套件变成 AI rack 核心件 | PCIe Gen6/7、CXL、JBOG/JBOM、scale-up fabric 提高 attach rate；Astera Scorpio X 320-lane 已出货 | Astera、Broadcom、Microchip、Marvell、Credo、Montage、Parade、Synopsys IP |
| CPO/CPX/NPO/ELS 进入架构选型期 | NVIDIA、Broadcom、Coherent、Lumentum、Open CPX/OCI 生态推动；功耗和面板密度压力显性化 | NVIDIA、Broadcom、TSMC COUPE、Coherent、Lumentum、Marvell、Molex、Samtec、TeraHop、Ciena |
| coherent scale-across 成为 AI 区域网络隐形增量 | 训练/推理跨 campus/metro/regional DCI，Marvell/Ciena/Nokia 推 1.6T/2.4T/3.2T coherent | Marvell、Ciena、Nokia/Infinera、Cisco/Acacia、Coherent、Lumentum |
| 验证测试设备成为瓶颈资产 | 224G/448G/1.6T/3.2T 需要 BERT、DCA、VNA、AWG、采样示波器、协议压测、FEC/BER/抖动/温漂/量产测试 | Keysight、VIAVI、Anritsu、Tektronix、Teledyne LeCroy、R&S、EXFO、Yokogawa、MPI、FormFactor |

### 1.3 2026 挑战

| 挑战 | 具体表现 | 投资含义 |
|---|---|---|
| 1.6T 价格与良率波动 | 早期 1.6T 供不应求但多供应商扩张快，2026H2-2027 可能 ASP 下行 | 上游 DSP、EML/EAM、激光器、测试设备比 module assembly 更有定价权 |
| 224G/448G 信号完整性难度上升 | TDECQ-CER、BER、FEC、SNDR/RLM、skew、crosstalk、fixture 去嵌复杂化 | 测试设备和高端连接器议价能力提高 |
| CPO 可维护性和良率 | ELS 冗余、光纤连接、热漂移、field replacement、known-good optical engine 是量产门槛 | CPO 的收入先从 ELS/optical engine/封装测试/连接器开始 |
| OCS 架构改变价值分配 | OCS 减少部分电交换功耗，但增加光模块、光纤管理和运维软件要求 | 不应把 OCS 看成“少买光模块”，反而是“更多光链路前置配置” |
| 标准并行导致形态分裂 | OSFP/QSFP-DD、LPO/LRO/TRO、XPO、CPX、NPO、OCI、OIF、UEC、UALink 并存 | 供应商需多平台适配；库存和认证风险增加 |
| AI 数据中心电力/液冷限制 | 光模块、交换机和高速铜缆也被液冷、机柜布局、上电节奏影响 | 高速互连订单可能季度波动，但全年需求仍高 |

### 1.4 新技术成熟与放量时间：三情景

| 技术/产品 | 2026 当前状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观成熟/放量 |
|---|---|---|---|---|
| 800G pluggable | 已大规模，AI 后端标准件 | 2026 继续最高出货，2027 ASP 下行但量继续增 | 2026 800G+ 成新增 AI 集群默认；低价吸收更多 neocloud | 2026 出货被 Google/Ironwood、国产 AI 集群继续拉爆，利润率回落慢 |
| 1.6T OSFP/QSFP-DD/LPO/LRO/TRO | OFC 2026 多厂商展示与早期量产 | 2026 出货 500-800 万只，2027 1,200-1,800 万只 | 2026 800-1,200 万只，2027 2,000-2,500 万只 | 2026 1,500 万只级，2027 3,000 万只级，短缺延续 |
| 224G electrical/optical lane | IEEE 802.3dj 验证主线 | 2026 验证/HVM，2027 成 1.6T 默认 | 2026H2 头部客户新平台默认 224G | 224G 生命周期被压缩，2027H1 即被 448G pilot 挤压高端新增 |
| AEC/ACC/DAC 1.6T | 1.6T AEC/ACC 已展示，PCIe/CXL AEC 增长 | 2026 Gen6/AEC 放量，2027 继续增长 | 2026H2 AI rack 内短距铜默认化 | 铜短距表现超预期，推迟部分光化，AEC/ACC 毛利维持高位 |
| CPC/top-side/flyover copper | Samtec/Luxshare/Molex/TE 等 224G/448G 展示 | 2026 设计导入，2027 量产平台增加 | 2027 成高端交换机/AI rack 标配 | 448G short-reach 2026H2 proprietary fabric 先用 |
| PCIe Gen6 Retimer/Switch | 已量产/出货，Astera Scorpio P/X 初期发货 | 2026 放量，2027 高 radix switch 扩大 | 2026H2 开放 AI fabric 增速高于 Retimer | 每 XPU connectivity dollar content 快速上升，高端 switch 毛利不降 |
| PCIe Gen7 | 2025 发布，2026 验证和 IP design-in | 2026-2027 IP/测试/样品，2028 后端设备 | 2027 高端 AI rack 开始预标准/早期平台 | 专有协议借用 PCIe7-class 电气提前商用 |
| PCIe Gen8/256GT/s | 2026-05 draft 0.5 | 2026-2027 pathfinding，2028 标准 | 2027 hyperscaler prototype | 256GT/s 测试设备和连接器订单 2026 即前置 |
| UALink/UEC scale-up | UALink 2.0 2026、UEC 1.0 已发布 | 2026 design-in，2027 第一批多厂商 pod | 2027 UALink/UEC switch 生产验证 | 开放 scale-up 成事实第二标准，2027 订单显著超预期 |
| OCS | Google/Apollo、iPronics 等 pilot/出货 | 2026 少数云厂，2027 扩到 TPU-like 架构 | 2027 被更多 AI cluster 采用 | GPU Ethernet fabric 也吸收 OCS，电交换预算部分重写 |
| CPO/CPX/NPO/ELS | NVIDIA/Broadcom/Coherent/Lumentum 已给路线 | 2026 pilot/ELS 收入，2027 小批量 | 2027 socketed CPO/CPX 多客户部署 | 2027 高端 AI switch 默认 CPO/CPX |
| XPO 12.8T | Arista MSA，OFC 2026 亮相 | 2026 展示，2027 小批量，2028 放量 | 2027H2 进入高端 AI fabric | 2027 即形成 $2B+ 需求，延长 pluggable 生命周期 |
| 3.2T/400G-per-lane | DSP/PIC/EML/EAM 样品和评估板 | 2026 sample/qual，2027 live demo，小量，2028 规模 | 2027H2 小批量收入 | 204.8T switch 提前，2027 $3B+ 早期市场 |
| 1600ZR/ZR+ | Marvell 1.6T ZR/ZR+ 2nm DSP 2026 | 2026H2 采样，2027 scale-across 放量 | 2027 AI region DCI 大量采购 | campus/metro/regional AI DCI 抢产能，coherent 毛利上行 |
| 光学验证测试 HVM | Keysight/VIAVI/Anritsu 等 224G/1.6T 产品化 | 2026 高景气，2027 3.2T 接棒 | 客户 qualification 并行，收入 +40-60% | 测试成为卡点，仪器交期与毛利上行 |

### 1.5 2026 最可能的技术路径

1. Rack 内近距：被动铜 + AEC/ACC + CPC/top-side/flyover，224G electrical lane 是主线，448G 是 pathfinding。
2. Rack 间/cluster 内：800G 继续主流，1.6T OSFP/DR8/2xDR4/LRO/LPO/TRO 从头部客户开始明显爬坡。
3. Scale-out 网络：Ethernet/RoCE/UEC 与 InfiniBand 并存；NVIDIA Spectrum-X、Broadcom Tomahawk/Jericho、Arista/Celestica whitebox、Marvell/AMD/UALink 生态都受益。
4. Scale-across：800ZR/1600ZR/ZR+、coherent-lite、multi-rail line systems 开始从电信设备逻辑转向 AI region 逻辑。
5. 验证测试：1.6T/224G 一致性、FEC/BER、光电混合链路、PCIe Gen6/Gen7、CXL/UALink/UEC、OCS/CPO 热可靠性，是客户出货 gate。

## 2. 已经开始放量的关键产品：市场规模、渗透率、增长和利润率

以下“未来 3 个月”指 2026-05 至 2026-08 附近的收入/订单 run-rate；“一年”指 2026H2-2027H1；“两年”指 2026H2-2028H1。市场规模为全球收入机会，含 merchant market 和 hyperscaler 自用采购，单位美元。

### 2.1 已放量产品市场预测

| 已放量产品 | 当前事实 | 未来 3 个月市场规模与渗透率 | 一年市场规模与渗透率 | 两年市场规模与渗透率 |
|---|---|---:|---:|---:|
| 800G 光模块 | 2026 AI 数据中心标准件；800G+ 占比 2026 预计 60%+ | 基准 $6B-$8B、乐观 $8B-$11B、超预期 $11B-$15B；新增 AI 光端口 45-55% | 基准 $24B-$32B、乐观 $32B-$42B、超预期 $42B-$55B；新增 AI 光端口 45-60% | 基准 $35B-$45B、乐观 $45B-$60B、超预期 $65B-$80B；占比被 1.6T 稀释但总量仍高 |
| 1.6T pluggable 光模块 | Cignal/OFC 信号显示 2026 快速增长；Coherent/Lumentum/Eoptolink 多厂商展示 | 基准 $1.5B-$2.5B、乐观 $2.5B-$4B、超预期 $4B-$6B；新增 AI 光端口 5-10% | 基准 $9B-$14B、乐观 $14B-$22B、超预期 $22B-$35B；新增高端端口 12-25% | 基准 $25B-$40B、乐观 $45B-$70B、超预期 $80B-$110B；新增高端端口 30-55% |
| 200G/224G optical DSP/CDR/Retimer | Broadcom/Marvell/Credo 3nm/2nm/400G lane 路线明确 | 基准 $1.5B-$2.5B、乐观 $2.5B-$4B、超预期 $4B-$6B；1.6T attach 上升 | 基准 $8B-$12B、乐观 $12B-$18B、超预期 $18B-$28B | 基准 $18B-$28B、乐观 $30B-$45B、超预期 $55B+ |
| EML/VCSEL/CW laser/PIC 光器件 | Lumentum SHP laser、Coherent SiPh/InP/VCSEL，Broadcom 400G EML/PD | 基准 $2B-$3B、乐观 $3B-$4.5B、超预期 $4.5B-$7B | 基准 $10B-$15B、乐观 $15B-$22B、超预期 $22B-$35B | 基准 $20B-$32B、乐观 $35B-$50B、超预期 $60B+ |
| AEC/ACC/DAC 高速铜缆 | 1.6T OSFP AEC/ACC、PCIe6 OSFP-XD AEC 已展示；Credo/Luxshare 受益 | 基准 $0.8B-$1.2B、乐观 $1.2B-$1.8B、超预期 $1.8B-$2.6B；AI rack 内短距 20-30% | 基准 $4B-$6B、乐观 $6B-$9B、超预期 $9B-$14B；短距 25-40% | 基准 $8B-$12B、乐观 $14B-$22B、超预期 $28B+ |
| PCIe Gen6 Retimer/Smart Cable Module | Astera、Broadcom、Microchip、Credo 放量；PCIe Gen6 从测试转量产 | 基准 $0.6B-$1B、乐观 $1B-$1.5B、超预期 $1.5B-$2.2B | 基准 $3B-$5B、乐观 $5B-$8B、超预期 $8B-$12B | 基准 $7B-$11B、乐观 $12B-$20B、超预期 $25B+ |
| PCIe/CXL/Fabric Switch | Astera Scorpio X 320-lane shipping；AI scale-up merchant TAM 被重估 | 基准 $0.5B-$0.9B、乐观 $0.9B-$1.5B、超预期 $1.5B-$2.5B | 基准 $3B-$6B、乐观 $6B-$10B、超预期 $10B-$16B | 基准 $10B-$18B、乐观 $20B-$35B、超预期 $45B+ |
| 高速连接器/CPC/top-side/flyover | Samtec 224G CPC、448G test assembly；Luxshare 448G CPC-to-OSFP；Molex/TE/Amphenol 跟进 | 基准 $1B-$1.6B、乐观 $1.6B-$2.5B、超预期 $2.5B-$4B | 基准 $6B-$9B、乐观 $9B-$14B、超预期 $14B-$22B | 基准 $14B-$22B、乐观 $25B-$38B、超预期 $50B+ |
| 800ZR/400ZR/ZR+ coherent DCI | AI scale-across、campus/metro DCI；coherent module 2025 近 $6B | 基准 $1.5B-$2.2B、乐观 $2.2B-$3B、超预期 $3B-$4B | 基准 $7B-$10B、乐观 $10B-$14B、超预期 $14B-$20B | 基准 $14B-$22B、乐观 $25B-$38B、超预期 $45B+ |
| 1.6T/224G 光电验证测试设备 | Keysight、VIAVI、Anritsu、Tektronix、Teledyne、R&S 产品化 | 基准 $0.4B-$0.8B、乐观 $0.8B-$1.2B、超预期 $1.2B-$1.8B | 基准 $2B-$3.5B、乐观 $3.5B-$5.5B、超预期 $5.5B-$8B | 基准 $5B-$8B、乐观 $8B-$13B、超预期 $16B+ |

### 2.2 已放量产品增长率与利润率

| 产品 | 未来一年增长：基准 / 乐观 / 极度超预期 | 当前利润率：基准 / 乐观 / 极度超预期 | 毛利驱动因素 |
|---|---:|---:|---|
| 800G 光模块 | +25-40% / +45-60% / +70%+ | 25-35% / 32-42% / 40-48% | AI 客户认证、交付能力、DSP/激光器成本、ASP 下降速度 |
| 1.6T 光模块 | +100-160% / +180-260% / +300%+ | 32-42% / 40-50% / 48-58% | 早期短缺、HVM 良率、DSP/EML 供应、客户 qualification |
| optical DSP/CDR | +45-70% / +80-120% / +150%+ | 55-70% / 65-75% / 70-80% | 3nm/2nm 稀缺、IP 复用、客户锁定、固件/telemetry |
| EML/laser/PIC | +35-60% / +70-100% / +120%+ | 35-55% / 45-60% / 55-70% | 200G/400G lane 良率、InP/SiPh 工艺、ELS 高功率需求 |
| AEC/ACC/DAC | +35-55% / +60-90% / +100%+ | 25-40% / 35-48% / 45-55% | Retimer/DSP 成本、线缆良率、reach、客户平台绑定 |
| PCIe Retimer/SCM | +30-50% / +60-90% / +100%+ | 60-72% / 68-76% / 72-80% | attach rate、PAM4 均衡、诊断软件、开放平台 design win |
| Fabric Switch | +50-80% / +100-150% / +200%+ | 60-72% / 68-78% / 75-82% | 320-lane/radix、in-network compute、firmware、客户认证 |
| 高速连接器/CPC | +25-45% / +50-75% / +90%+ | 30-45% / 40-55% / 50-60% | 机械公差、材料 Df/Dk、客户 reference design、量产一致性 |
| coherent DCI | +25-40% / +45-65% / +80%+ | 35-48% / 42-55% / 50-60% | 2nm DSP、MACsec、传输距离、光纤资源、系统软件 |
| 验证测试设备 | +25-40% / +50-70% / +90%+ | 55-68% / 62-72% / 68-78% | 高带宽仪器稀缺、软件 license、自动化测试流程、客户认证 |

## 3. 在研与即将快速增长的关键产品

### 3.1 在研/早期导入产品市场预测

| 在研/早期产品 | 2026 证据 | 未来 3 个月 | 一年 | 两年 |
|---|---|---:|---:|---:|
| 3.2T pluggable / 400G-per-lane | Broadcom Taurus 400G/lane DSP；Coherent 400G/lane PAM4；OpenLight 3.2T DR8 beta Q4 2026 | 基准 $50M-$150M、乐观 $150M-$300M、超预期 $300M-$600M；以样品和测试为主 | 基准 $0.5B-$1.5B、乐观 $1.5B-$3B、超预期 $3B-$6B | 基准 $6B-$12B、乐观 $15B-$25B、超预期 $35B+ |
| 400G EML/EAM/MZM/TFLN 调制器 | Lumentum 400G differential EML；OpenLight 448G EAM；Coherent 400G SiPh MZM | 基准 $100M-$250M、乐观 $250M-$500M、超预期 $500M-$900M | 基准 $1B-$2B、乐观 $2B-$4B、超预期 $4B-$7B | 基准 $6B-$10B、乐观 $12B-$20B、超预期 $25B+ |
| CPO/CPX/NPO optical engine | NVIDIA Spectrum-X Photonics、Broadcom Tomahawk CPO、Coherent 6.4T CPO、CPX/OCI MSA | 基准 $100M-$300M、乐观 $300M-$600M、超预期 $600M-$1B | 基准 $1B-$2.5B、乐观 $2.5B-$5B、超预期 $5B-$9B | 基准 $8B-$15B、乐观 $18B-$35B、超预期 $50B+ |
| External laser source / ELSFP / UHP laser | Lumentum 1310nm SHP >1W@25C、16-channel DWDM UHP 24dBm/channel | 基准 $80M-$200M、乐观 $200M-$450M、超预期 $450M-$800M | 基准 $0.7B-$1.5B、乐观 $1.5B-$3B、超预期 $3B-$5B | 基准 $4B-$8B、乐观 $9B-$16B、超预期 $20B+ |
| XPO 12.8T liquid-cooled pluggable | Arista XPO MSA：12.8Tbps/module、204.8Tbps/OCP RU、400W cooling | 基准 <$100M、乐观 $100M-$250M、超预期 $250M-$500M | 基准 $0.3B-$1B、乐观 $1B-$2.5B、超预期 $2.5B-$5B | 基准 $5B-$10B、乐观 $12B-$25B、超预期 $35B+ |
| PCIe optical-aware Retimer / PCIe over optics | PCI-SIG optical interconnect path、DesignCon/DevCon 议题升温 | 基准 $30M-$100M、乐观 $100M-$250M、超预期 $250M-$500M | 基准 $0.4B-$1B、乐观 $1B-$2.5B、超预期 $2.5B-$5B | 基准 $4B-$8B、乐观 $10B-$18B、超预期 $25B+ |
| UALink switch/IP/chiplet | UALink 2.0 增加 in-network compute、chiplet、manageability | 基准 $50M-$150M、乐观 $150M-$350M、超预期 $350M-$800M | 基准 $0.8B-$2B、乐观 $2B-$5B、超预期 $5B-$10B | 基准 $8B-$16B、乐观 $20B-$40B、超预期 $60B+ |
| OCS/MEMS/SiPh optical switching | Google Apollo、iPronics 32x32 SiPh OCS、AI 全光网络 | 基准 $100M-$300M、乐观 $300M-$700M、超预期 $700M-$1.2B | 基准 $0.8B-$2B、乐观 $2B-$5B、超预期 $5B-$9B | 基准 $6B-$12B、乐观 $15B-$30B、超预期 $45B+ |
| 多芯光纤/高密度 fiber management | Rubin/NVL144 光纤数量上升，多芯光纤节省 duct space | 基准 $50M-$150M、乐观 $150M-$300M、超预期 $300M-$600M | 基准 $0.5B-$1.2B、乐观 $1.2B-$2.5B、超预期 $2.5B-$5B | 基准 $4B-$8B、乐观 $9B-$18B、超预期 $25B+ |
| 448G/PCIe8 测试设备 | PCIe8 256GT/s draft 0.5；Samtec/Luxshare/Keysight/Anritsu 448G pathfinding | 基准 $100M-$250M、乐观 $250M-$500M、超预期 $500M-$900M | 基准 $0.8B-$2B、乐观 $2B-$4B、超预期 $4B-$7B | 基准 $5B-$9B、乐观 $10B-$18B、超预期 $25B+ |

### 3.2 在研产品利润率预测

| 产品 | 利润率：基准 | 利润率：乐观 | 利润率：极度超预期 | 为什么能高溢价 |
|---|---:|---:|---:|---|
| 3.2T module/engine | 30-42% | 40-52% | 50-62% | 400G/lane 良率低、测试时间长、客户认证早期稀缺 |
| 400G EML/EAM/MZM/TFLN | 45-60% | 55-70% | 65-78% | 上游器件瓶颈、工艺/IP 难复制、良率学习曲线 |
| CPO/CPX/NPO optical engine | 40-55% | 50-65% | 60-75% | 系统级设计、封装测试、热可靠性和客户平台绑定 |
| ELS/UHP laser | 45-60% | 55-70% | 65-80% | CPO 可靠性核心件，高功率窄线宽/多通道 DWDM 难度高 |
| XPO | 35-48% | 45-58% | 55-65% | 12.8T + 液冷 + 高密度 form factor，早期供应商少 |
| PCIe over optics | 40-55% | 50-65% | 60-75% | 标准、Retimer、光模块、系统验证跨域融合，认证周期长 |
| UALink switch/IP | 60-75% | 70-80% | 78-85% | 交换芯片/IP/固件/管理软件绑定，生态早期 |
| OCS | 35-50% | 45-60% | 55-70% | MEMS/SiPh/控制软件和架构锁定，节能价值可量化 |
| 448G/PCIe8 T&M | 60-70% | 68-78% | 75-85% | 客户必须先买仪器才能研发，软件 license 和夹具耗材高粘性 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 工艺/能力 |
|---|---|---|---|
| 光模块组装与量产 | 中国、泰国、马来西亚、越南、墨西哥、美国 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、Fabrinet、FII、Accelink、Hisense、Source Photonics、Linktel、AOI | 800G/1.6T OSFP/QSFP-DD/LPO/LRO/TRO，高速自动耦合、光电测试、burn-in |
| 光芯片/激光器 | 美国、日本、中国台湾、中国大陆、欧洲 | Lumentum、Coherent、Broadcom、MACOM、Sumitomo、Furukawa、Mitsubishi、II-VI/Coherent、Innolight/Eoptolink 自研部分 | InP EML/DFB/CW laser、VCSEL、PD、driver/TIA |
| 硅光/PIC | 美国、中国台湾、欧洲、以色列、新加坡 | TSMC COUPE、GlobalFoundries、Tower/OpenLight、Intel、Ayar Labs、DustPhotonics/Credo、POET、imec、Lightmatter、Celestial AI | SiPh PIC、EIC/PIC co-packaging、integrated laser、EAM/MZM、wafer-level test |
| Optical DSP/CDR/SerDes | 美国、中国台湾、以色列 | Broadcom、Marvell、Credo、MaxLinear、Semtech、MACOM、MediaTek、Realtek、NVIDIA | 3nm/2nm/5nm DSP、200G/400G lane、Retimer/CDR、telemetry |
| Retimer/Fabric Switch | 美国、以色列、中国台湾、中国大陆 | Astera、Broadcom、Marvell、Microchip、Credo、Montage、Parade、Synopsys IP、Cadence IP | PCIe Gen5/6/7、CXL、32-320 lane switch、Smart Cable Module |
| 高速连接器/线缆 | 美国、欧洲、中国、中国台湾、日本、东南亚 | Amphenol、TE、Molex、Samtec、Luxshare、BizLink、FIT/Foxconn、Hirose、JAE、Yamaichi | 224G/448G CPC、top-side、backplane、OSFP/OSFP-XD、flyover、AEC/ACC |
| 交换机/系统 | 美国、中国台湾、中国大陆 | NVIDIA、Broadcom、Arista、Cisco、Juniper/HPE、Celestica、Accton、Delta、FII、Supermicro、Wiwynn | 800G/1.6T Ethernet、IB、UEC、SONiC、CPO/XPO/液冷 |
| 光电验证测试 | 美国、日本、德国、瑞士、中国 | Keysight、VIAVI、Anritsu、Tektronix、Teledyne LeCroy、Rohde & Schwarz、EXFO、Yokogawa、Luna、FormFactor、MPI、Advantest、Teradyne | BERT、DCA、VNA、AWG、sampling scope、protocol analyzer、FEC/BER、wafer/module HVM test |

### 4.2 至少 12 条关键瓶颈

1. 200G/400G EML/EAM/MZM 良率：1.6T/3.2T 的核心瓶颈，上游器件出问题会直接拖累 module HVM。
2. 3nm/2nm optical DSP 产能：Broadcom/Marvell/Credo 等共享先进制程、封装和测试资源，AI ASIC/GPU 也抢先进节点。
3. 224G/448G 测试时间：TDECQ-CER、BER、FEC、jitter、SNDR/RLM、温循和长时间压力测试显著拉长测试瓶颈。
4. 自动光耦合与 FAU 产能：1.6T/3.2T、CPO/CPX 要求更高通道数和更低插损，耦合/固化/校准影响良率。
5. CPO/ELS 可维护性：外置激光源冗余、光纤连接、现场更换、热漂移补偿没有完全标准化。
6. 高速连接器材料与公差：224G/448G 对 Dk/Df、铜粗糙度、skew、via/fan-out、mating tolerance 极敏感。
7. Retimer/Switch 固件与互操作：PCIe/CXL/UALink/UEC 不只是硅片，客户需要 telemetry、链路训练、故障定位和 fleet management。
8. 认证周期：Hyperscaler qualification 往往 6-18 个月；一旦进入 AVL，替换成本高，但新供应商爬坡慢。
9. 光纤管理与施工：高密度 AI rack 的光纤数量上升，多芯光纤、shuffle、配线和现场测试会成为部署卡点。
10. 液冷对光模块/电缆的机械约束：XPO/CPO/高密度 OSFP 与冷板、manifold、盲插接口共存，物理空间紧张。
11. 人才瓶颈：224G/448G SI/PI、硅光封装、coherent DSP、光模块 HVM、量产测试工程师供给不足。
12. 地缘与供应链认证：光模块供应链中美分布、先进制程、EDA/IP、云厂安全审计都会影响份额。

### 4.3 成本结构与毛利决定因素

| 产品 | 典型成本构成 | 毛利决定因素 | 价格传导 |
|---|---|---|---|
| 800G/1.6T 光模块 | DSP/CDR 20-35%，EML/VCSEL/laser/PD/TIA 20-30%，PCB/连接器/散热 10-15%，组装耦合测试 15-25%，质保/良率 5-15% | 客户认证、良率、测试时间、上游器件短缺、ASP 下行速度 | GPU/XPU 集群总价巨大，短期可向客户传导；多供应商成熟后 ASP 下行 |
| optical DSP | 晶圆/封装/测试 25-40%，IP/R&D amortization 20-30%，软件/firmware 低边际成本 | 制程领先、SerDes IP、功耗、telemetry、客户 socket 锁定 | 绑定模块和交换平台，早期议价强 |
| laser/PIC | 外延/wafer 20-35%，加工 20-30%，封测/筛选 20-30%，良率损失 10-20% | 高功率、窄线宽、温度稳定性、Telcordia 可靠性、CPO 适配 | 供不应求时直接涨价；客户更重视可用性而非单价 |
| AEC/ACC | Retimer/DSP 30-50%，线缆/连接器 20-35%，组装测试 15-25% | reach、功耗、BER、热、可弯折、客户平台绑定 | 比光模块便宜但价值高，短距场景可保持较好 ASP |
| Retimer/Fabric Switch | 硅片/封测 25-40%，R&D/IP/软件 25-40%，系统验证 10-20% | lane count、低延迟、链路诊断、in-network compute、标准生态 | 客户按每 XPU/rack 价值定价，不按传统桥片定价 |
| 高速连接器/CPC | 精密冲压/电镀/绝缘材料 25-40%，线缆/材料 20-35%，模具/设备折旧 10-20%，测试 10-20% | 224G/448G margin、机械可靠性、客户 reference design | 一旦进入平台，按系统架构自由度定价 |
| 测试设备 | 高带宽前端/ADC/采样头/光模块 35-50%，软件 10-25%，校准/服务 10-20%，R&D 20-30% | 频率带宽、自动化软件、标准一致性、服务网络 | 客户研发/HVM gate，价格弹性低，软件续费高 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | 市场结构 | 头部集中度判断 |
|---|---|---|
| 高速光模块 | 中国双龙头 + 美日光器件厂 + EMS/ODM 多点扩散 | 800G/1.6T 头部 5-8 家大概率占 60-75%；客户认证高度集中 |
| Optical DSP | Broadcom/Marvell/Credo 三强，部分 MACOM/Semtech/MaxLinear | 前三占高端 1.6T/3.2T DSP 大部分份额，毛利高 |
| 激光器/EML/PIC | Lumentum/Coherent/Broadcom/MACOM/Sumitomo 等，SiPh 新进入者增加 | 高端 200G/400G 器件集中度高，CPO ELS 更高 |
| Retimer/Fabric Switch | Astera、Broadcom、Marvell、Microchip、Credo、Montage | AI rack 高端份额向少数 IP/固件领先者集中 |
| 高速连接器/线缆 | Amphenol、TE、Molex、Samtec、Luxshare、BizLink、FIT | 全球巨头 + 亚洲制造；客户平台进入后切换难 |
| CPO/CPX/XPO/NPO | NVIDIA/Broadcom/Arista 主导架构，Coherent/Lumentum/Marvell/连接器厂供关键件 | 2026-2027 仍是生态卡位，最终结构未定 |
| coherent DCI | Ciena、Nokia/Infinera、Cisco/Acacia、Marvell、Coherent | 系统层高集中，DSP 和 pluggable 也高集中 |
| 验证测试 | Keysight、VIAVI、Anritsu、Tektronix、Teledyne LeCroy、R&S | 高端 224G/448G/1.6T/3.2T 测试高度集中，毛利稳定 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| 信号完整性 | 224G/448G、128/256GT/s、90-250GHz 测试带宽 | 能不能稳定量产出可用 eye/FEC margin 决定客户上架速度 |
| 光学性能 | TDECQ、TDECQ-CER、BER、光功率、温漂、插损 | AI 集群不能接受高 link flap，客户为 uptime 付溢价 |
| 功耗 | 每 1.6T port W 数、pJ/bit、CPO 5x power reduction 目标 | 电力是 AI 数据中心最大约束，节省功耗可直接换 GPU |
| 客户认证 | Hyperscaler AVL、6-18 个月 qualification、系统 burn-in | 认证后切换供应商会带来调试和停机风险 |
| 量产良率 | 光耦合良率、DSP 封装良率、HVM test throughput | 良率决定真实交付，短缺期客户优先买确定性 |
| 标准参与 | IEEE/OIF/PCI-SIG/UEC/UALink/OCP/OCI/XPO/CPX | 参与标准能提前锁定 form factor 与测试方法 |
| 软件/telemetry | Link training、FEC、故障定位、fleet monitoring | 互连芯片从硬件变成可管理资产，软件提高粘性 |
| 供应链规模 | 多工厂、多区域、自动化耦合、测试机台 | 大客户要求月度百万端口交付，规模本身是门槛 |
| 生态绑定 | 与 NVIDIA/AMD/Google/AWS/Meta/Microsoft 平台绑定 | 互连不是通用零件，而是平台架构的一部分 |

### 5.3 价值捕获判断

长期最可能拥有高 ROIC/高毛利的层级：

1. Optical DSP/SerDes/Retimer/Fabric Switch：毛利 60-80%，IP 可复用，客户平台绑定强，AI rack 每 XPU 互连价值量上升。
2. 高端测试与验证设备：毛利 55-75%，研发和量产都需要，标准升级会持续触发换机和软件升级。
3. 激光器/PIC/ELS/高端光器件：在 1.6T/3.2T/CPO 中是瓶颈，尤其 400G/lane 和 ELS。
4. CPO/CPX/XPO 核心 optical engine 与连接生态：若标准稳定，会成为交换平台准入件。
5. 高速连接器/CPC/top-side：毛利不如芯片，但平台锁定和机械/材料壁垒强。
6. 光模块 assembly：收入最大、确定性高，但长期可能受多供应商和 ASP 下行压制；赢家必须上移到光芯片、测试、系统设计。

## 6. 2026 关键变化：三个最可能拐点

### 拐点一：1.6T 从展示进入规模交付，800G+ 成 AI 数据中心标准件

2026 年 800G 及以上占比预计超过 60%，AI 光收发模块市场预计达到 $26B。1.6T 仍处于早期高价期，但已经不是 PPT；Coherent、Lumentum、Broadcom、Marvell、Credo、Eoptolink、Arista XPO 生态都在 OFC 2026 给出产品/样机/平台。

最可能放量：1.6T OSFP DR8/2xDR4/LPO/LRO/TRO、200G/224G DSP/CDR、200G EML/VCSEL/SiPh PIC、1.6T HVM 测试。

### 拐点二：验证测试成为出货节奏 gate

224G lane、IEEE 802.3dj、PCIe Gen7、FEC/BER/TDECQ-CER、OCS/CPO 系统验证让测试复杂度明显上升。Keysight、VIAVI、Anritsu 等在 2026 年集中发布新方案，说明客户痛点已经从“能不能做出样品”转向“能不能可重复、高良率、可审计地量产”。

最可能放量：DCA sampling oscilloscope、BERT、VNA、AWG、protocol analyzer、1.6T Ethernet traffic appliance、自动化合规软件、量产测试夹具。

### 拐点三：铜互连被重新定价

2026 不是“光替代铜”，而是“短距铜变得更高级、更贵、更靠近 ASIC”。Luxshare 展示 448G CPC-to-OSFP、1.6T OSFP AEC/ACC、PCIe 6 OSFP-XD AEC 7m；Samtec 展示 224G Si-Fly HD CPC 和 448G test assembly。铜在 rack 内、near-ASIC、top-side、PCIe/CXL/JBOG/JBOM 中仍有强生命力。

最可能放量：AEC/ACC、CPC/top-side connector、flyover cable、PCIe Gen6 Retimer、CXL/PCIe cable module。

## 7. 2027 关键变化：三个最可能拐点

### 拐点一：1.6T 成新增高端 AI fabric 默认，3.2T 开始 live demo 和小批量收入

VIAVI 判断 3.2T initial live demonstrations 2027 合理；OpenLight 3.2T DR8 beta 样品预计 2026 Q4；Broadcom Taurus、Coherent 400G/lane 链路会在 2027 转为客户 qualification。2027 的高端交换平台会开始把 3.2T 当作下一轮采购前置变量。

最可能放量：400G/lane DSP、448G EAM/EML/MZM、3.2T validation、3.2T optical engines。

### 拐点二：CPO/CPX/XPO 从标准和样机进入高端交换平台

NVIDIA Rubin/Spectrum-X Photonics、Broadcom Tomahawk CPO、Arista XPO、Open CPX/OCI 的路径在 2027 会开始分化：CPO/CPX 解决功耗极限，XPO 保留可插拔服务性，NPO 解决 near-package 过渡。赢家未定，但高功耗 AI rack 会迫使客户至少试点。

最可能放量：ELS/UHP laser、socketed optical engine、XPO liquid-cooled module、fiber shuffle/high-density connector、CPO test。

### 拐点三：开放 scale-up fabric 开始真实商用

UALink 2.0 已加入 in-network compute、chiplet 和 manageability；UEC 1.0 已覆盖 NIC、switch、optics、cables 的完整 Ethernet 栈。2027 若 AMD MI400/Helios、custom ASIC、Meta/Microsoft/OpenAI/Broadcom 生态扩张，非 NVIDIA 封闭 fabric 会要求开放 scale-up 的可采购性。

最可能放量：UALink switch/IP、UEC-compliant NIC/switch、PCIe/CXL/Fabric Switch、optical-aware Retimer、AI fabric validation。

## 8. 头部公司与细分公司清单

### 8.1 光模块与光组件

| 细分 | 公司 |
|---|---|
| 800G/1.6T 光模块 | Innolight/中际旭创、Eoptolink/新易盛、Coherent、Lumentum、Fabrinet、Foxconn Industrial Internet、Accelink/光迅、Hisense Broadband、Source Photonics、AOI、Linktel、FS、HG Genuine、Hengtong、Broadex |
| 1.6T/3.2T 关键光器件 | Lumentum、Coherent、Broadcom、MACOM、Sumitomo Electric、Furukawa、Mitsubishi Electric、II-VI/Coherent、Innolight、Eoptolink、Accelink |
| 硅光/PIC | TSMC COUPE、GlobalFoundries、Tower/OpenLight、Intel、Ayar Labs、DustPhotonics/Credo、POET、Lightmatter、Celestial AI、Ranovus、Rockley、imec、Skorpios、Sicoya |
| CPO/CPX/NPO/ELS | NVIDIA、Broadcom、Coherent、Lumentum、Marvell、Molex、Samtec、TeraHop、Ciena、OpenLight、TSMC、Ayar Labs、Enosemi/AMD、POET |
| XPO | Arista、Eoptolink、Linktel、Coherent、Lumentum、Molex、Samtec、Luxshare、Senko、Corning、major optical module suppliers |
| OCS | Google/Apollo、iPronics、Coherent、Calient、Polatis/HUBER+SUHNER、NTT/various SiPh OCS players |
| coherent DCI | Ciena、Nokia/Infinera、Cisco/Acacia、Marvell、Coherent、Lumentum、Fujitsu、NEC、Juniper、ADVA/Adtran |

### 8.2 芯片、协议与高速铜互连

| 细分 | 公司 |
|---|---|
| Ethernet switch ASIC | Broadcom、NVIDIA、Marvell、Cisco/Silicon One、AMD/Pensando、Intel、Nephos、Centec |
| Optical DSP/CDR | Broadcom、Marvell、Credo、MACOM、Semtech、MaxLinear、MediaTek、Realtek |
| PCIe/CXL Retimer | Astera、Broadcom、Microchip、Marvell、Credo、Montage、Parade、Diodes、Texas Instruments、Analog Devices |
| Fabric Switch/Smart Cable | Astera、Broadcom、Microchip、Marvell、Credo、Montage、Synopsys/Cadence IP、Celestica/Accton platform |
| SerDes/IP/EDA | Synopsys、Cadence、Alphawave Semi、Rambus、Siemens EDA、Ansys、Keysight EDA、Marvell、Broadcom |
| AEC/ACC/DAC | Credo、Luxshare、Amphenol、TE Connectivity、Molex、BizLink、FIT/Foxconn、Samtec、Broadcom、Marvell、FS |
| CPC/top-side/flyover/backplane | Samtec、Luxshare、Molex、TE Connectivity、Amphenol、Hirose、JAE、Yamaichi、BizLink、FIT、Shennan Circuits |
| PCB/材料 | Shennan Circuits、Tripod、Unimicron、TTM、AT&S、MEGTRON/Panasonic、Isola、Rogers、ITEQ、Elite Material |

### 8.3 验证测试、量产测试与自动化

| 细分 | 公司 |
|---|---|
| 高速示波器/DCA/BERT/AWG/VNA | Keysight、Tektronix、Anritsu、Rohde & Schwarz、Teledyne LeCroy、VIAVI、Yokogawa |
| Ethernet/网络协议压测 | VIAVI、Keysight/Ixia、Spirent assets under VIAVI、Xena/Teledyne LeCroy、EXFO |
| 光模块量产测试 | Keysight、VIAVI、Anritsu、EXFO、Yokogawa、Santec、Luna、Kingfisher、Teradyne、Advantest、Chroma |
| 晶圆/封装探针与自动化 | FormFactor、MPI、Tokyo Electron、Advantest、Teradyne、Cohu、Hon Precision、MueTec |
| SI/PI/仿真/自动化 | Keysight EDA、Cadence、Synopsys、Siemens EDA、Ansys、MathWorks、Simberian、JITX |

### 8.4 系统与客户生态

| 细分 | 公司 |
|---|---|
| AI 网络系统 | NVIDIA、Arista、Broadcom、Cisco、Juniper/HPE、Celestica、Accton、Delta、FII、Wiwynn、Supermicro |
| 云厂/AI lab 需求锚 | Microsoft、Google、AWS、Meta、OpenAI、Anthropic、Oracle、CoreWeave、xAI、ByteDance、Alibaba、Tencent、Baidu |
| 标准组织/MSA | IEEE 802.3dj、OIF、PCI-SIG、UEC、UALink、OCP、Open CPX MSA、OCI MSA、XPO MSA、LPO MSA、CW-WDM MSA |

## 9. 未来跟踪指标

1. 1.6T module 单季出货量、ASP、良率、客户集中度。
2. 800G+ 光模块占比是否在 2026 达到 60%+，以及 2027 1.6T 是否成为新增高端默认。
3. Keysight/VIAVI/Anritsu/Tektronix 等 224G/1.6T/3.2T 设备订单、交期和软件 license 增长。
4. Broadcom/Marvell/Credo optical DSP 的 3nm/2nm 供应、400G/lane tapeout 和客户认证。
5. Astera/Broadcom/Marvell/Credo Retimer/Fabric Switch revenue growth 和每 XPU attach rate。
6. CPO/CPX/XPO 的客户 pilot 数量、ELS 冗余方案、现场可维护性和故障率。
7. OCS 是否从 Google TPU-like 架构扩散到 GPU/Ethernet fabric。
8. UALink/UEC 是否在 2027 产生真实 switch/NIC/IP 订单。
9. 高速连接器/CPC 的 224G 量产和 448G design win。
10. AI 数据中心电力/液冷上电延误是否导致互连订单季度波动。

## 10. 主要来源

### 公司一手信息

- NVIDIA FY2026 results: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/
- NVIDIA Spectrum-X Ethernet Photonics: https://developer.nvidia.com/blog/scaling-power-efficient-ai-factories-with-nvidia-spectrum-x-ethernet-photonics/
- Broadcom Q1 FY2026 results: https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial
- Broadcom OFC 2026 AI infrastructure: https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai
- Dell FY2026 results: https://www.dell.com/en-us/dt/corporate/newsroom/announcements/detailpage.press-releases~usa~2026~2~dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-2026-results.htm
- Arista Q1 2026 results: https://www.arista.com/en/company/news/press-release/24017-pr-20260505
- Arista XPO MSA: https://www.arista.com/company/news/press-release/23697-pr-20260311
- Astera Labs Q1 2026 results: https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-reports-first-quarter-2026-financial-results
- Credo Q3 FY2026 results: https://www.sec.gov/Archives/edgar/data/1807794/000162828026013205/credoq32026ex-9911.htm
- Credo DustPhotonics acquisition: https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Agrees-to-Acquire-DustPhotonics-Accelerating-Expansion-into-Silicon-Photonics-and-Next-Generation-Optical-Connectivity/default.aspx
- Marvell 1.6T ZR/ZR+ and 2nm coherent DSP: https://www.marvell.com/company/newsroom/marvell-1-6t-zr-zr-plus-pluggable-2nm-coherent-dsp-ai-interconnects.html
- Coherent OFC 2026 pluggable optics: https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026
- Coherent CPO at OFC 2026: https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026
- Lumentum OFC 2026: https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx
- OpenLight 3.2T DR8 PIC: https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants
- Keysight 224G/1.6T validation: https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0313-pr26-049-keysight-introduces-new-224g-test-solutions-to-enable-1-6t-optical-network-validation.html
- Keysight DesignCon 2026: https://www.keysight.com/it/en/about/newsroom/news-releases/2026/0209-pr26-028-keysight-to-showcase-advanced-ai-data-center-and-high-speed-interconnect-validation-at-designcon-2026.html
- VIAVI OFC 2026: https://blog.viavisolutions.com/2026/04/23/ofc-2026-1-6t-going-mainstream-the-emergence-of-3-2t/
- Anritsu DesignCon 2026: https://www.anritsu.com/en-us/test-measurement/news/news-releases/2026/2026-02-20-us01
- Anritsu/Semtech OFC 2026 224G/448G: https://www.anritsu.com/en-us/test-measurement/news/news-releases/2026/2026-03-16-us01
- Luxshare-Tech DesignCon 2026: https://en.luxshare-tech.com/company/resources/news/designcon-2026-unveiling-224g-448g.html
- Samtec DesignCon 2026: https://blog.samtec.com/post/samtec-at-designcon-2026/

### 标准、会议与行业报告

- PCIe 8.0 draft 0.5: https://pcisig.com/blog/pcier-80-specification-draft-05-now-available-track-2560-gts-transfer-speeds-2028
- PCIe 7.0 release: https://pcisig.com/newsroom/pci-sig%C2%AE-releases-pcie%C2%AE-70-specification-support-bandwidth-demands-artificial-intelligence
- UALink 2.0 update: https://ualinkconsortium.org/wp-content/uploads/2026/04/UALink-2.0-Specification-PR_FINAL.pdf
- UEC 1.0: https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/
- TrendForce 800G+ share and Google OCS: https://www.trendforce.com/presscenter/news/20260210-12919.html
- TrendForce AI optical transceiver market: https://www.trendforce.com.tw/presscenter/news/20260420-13016.html
- Cignal AI optical components 2025: https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/
- LightCounting March 2026 update: https://www.lightcounting.com/report/march-2026-quarterly-market-update-380
- Dell'Oro AI back-end switch market: https://www.prnewswire.com/news-releases/ai-back-end-switch-market-will-push-past-100-billion-by-2030-according-to-delloro-group-302678344.html

# 行业调研：【硅光材料、光子材料与电光聚合物】

截至日期：2026-05-08  
研究口径：本报告聚焦 AI 数据中心光互连中的材料、器件、光子集成与电光调制层，包括硅光 PIC、InP/EML/EAM/VCSEL/激光器、TFLN 薄膜铌酸锂、BTO 钛酸钡、电光聚合物/硅有机混合 SOH、等离激元调制器、CPO/CPX/NPO/XPO 光引擎、外置激光源 ELS、光 I/O chiplet 与部分光交换/OCS。市场规模以美元收入计，若无公开拆分，采用公开出货量、ASP、BOM 占比、供应链毛利与 AI 芯片/网络放量节奏测算。

## 0. 高密度结论

**核心判断：2026 年不是“光计算替代 GPU”的年份，而是 AI 集群把光互连从模块采购推向材料和封装架构重写的年份。** 2026 最确定的商业兑现是 800G/1.6T 光模块、200G/lane 光器件、硅光 PIC、InP EML/EAM/DFB、VCSEL、DSP/driver/TIA、LPO/LRO/TRO、coherent ZR/ZR+；最高弹性的期权是 CPO/CPX/NPO/XPO、TFLN、EO polymer/SOH、BTO、plasmonic modulator、光 I/O chiplet。

**2026 主流技术路径：**

1. **800G 继续标配，1.6T 进入规模爬坡。** TrendForce 预计 AI 专用光收发模块市场从 2025 年 **165 亿美元**增至 2026 年 **260 亿美元**，同比 **57%+**；800G 及以上模块出货占比从 2024 年 **19.5%**升到 2026 年 **60%+**。LightCounting 也给出 2025 年 AI cluster optical transceiver **165 亿美元**、2026 年 **260 亿美元**的口径。
2. **硅光不是唯一赢家，但会成为默认集成底座。** 2026 的 1.6T/3.2T 路线是 SiPh、InP、TFLN、EO polymer、BTO 多材料叠加到硅光 foundry/封装生态，而不是单材料路线一统天下。
3. **CPO 在 2026 是 high-end switch pilot/早期产品，2027 才可能真正放量。** NVIDIA 官方称 Spectrum-X Ethernet Photonics/CPO 相比传统可插拔方案可达 **5x optical power efficiency**、**10x resiliency**，并指向 2026H2；Broadcom 在 OFC 2026 展示 102.4T CPO switch、3.5D XPU、400G/lane Taurus DSP。
4. **TFLN 已经从实验室进入 foundry/模块级验证。** HyperLight 2026 年 3 月连续发布：UMC/Wavetek 6-inch 与 8-inch TFLN 高量产合作、Jabil 数据中心规模部署合作、20W fully retimed 1.6T-DR8 参考模块、400G/lane TFLN PIC、145GHz packaged intensity modulator。
5. **电光聚合物进入 PDK 与客户验证年，但收入要谨慎外推。** Lightwave Logic 在 2026 年 3 月分别把 EO polymer modulator 接入 SilTerra/Luceda、Tower PH18、GlobalFoundries/GDSFactory PDK 路线；NLM Photonics 2026 年开始向部分客户 sampling 1.6T/3.2T SOH PIC，并与 Tower PH18M 做 MPW 验证。基准情形下 2026 仍以 NRE/样品/PDK 验证为主，乐观情形 2027 出现模块级设计赢单，极度乐观情形 2027H2 在 3.2T 或 CPO/NPO 中成为稀缺材料。
6. **BTO 是更远的“硅光 Pockels 材料”期权。** Veeco 与 imec 2026-01 宣布 300mm high-volume-manufacturing-compatible BTO-on-silicon photonics process；Lumiphase 已开发商业 200mm BTO-silicon platform。基准节奏仍是 2027 工程样品、2028 后商业化。
7. **利润池从模块总装向“光芯片/激光器/材料 IP/PDK/测试”上移。** 模块收入最大，但会在 2026H2-2027 面临 ASP 竞争；长期高 ROIC 更可能在高功率 CW/DFB/EML、DSP/SerDes、TFLN/EO polymer/BTO 材料与器件 IP、CPO optical engine/ELS、wafer-level optical test、foundry PDK 生态。

## 1. 2026 AI 计算中心机遇、挑战与技术路径

### 1.1 AI 芯片放量背景对光子材料的需求映射

项目内 AI 芯片路线图判断 2026 最大出货/价值权重平台包括 NVIDIA B300/GB300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA B200/GB200、Huawei Ascend 910C/950、Cambricon MLU 590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200；2026H2-2027 的下一层弹性来自 NVIDIA Rubin、AMD MI400/Helios、Google TPU8、OpenAI/Broadcom ASIC、Meta 后续 MTIA。

| AI 芯片/平台 | 2026-2027 光互连需求 | 对硅光/光子材料/EO polymer 的直接含义 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | Rack 内以 NVLink/铜为主，scale-out 依赖 800G/1.6T；GB300/后续 Rubin 接入 Spectrum-X Photonics/CPO | 2026 最大确定需求仍是 800G/1.6T pluggable、SiPh/InP/VCSEL；2026H2-2027 CPO/ELS/CPX 变成高端 switch 增量 |
| AWS Trainium2/Trainium3 | EFA/以太网 scale-out、NeuronLink scale-up；GW 级集群需要大量 800G/1.6T optics | 模块与硅光 PIC 收入确定，CPO 未公开为核心，但 1.6T/linear optics 将受益 |
| Google TPU v7 Ironwood | 3D Torus + Apollo OCS，全光跨柜；TrendForce 称 2026 Google 800G+ 模块需求超过 600 万只 | OCS 是光模块放大器；Google 订单利好 Innolight/Eoptolink、SiPh、LPO/LRO、光纤管理 |
| NVIDIA B200/GB200 | 2026 存量/延续订单，scale-out optics 继续消耗 800G | 800G 价格下行但量大；1.6T 替代从新增集群开始 |
| Huawei Ascend 910C/950 | 国产替代与超节点，光模块从 400G/800G 向 1.6T 追赶 | 中国模块厂、国产激光器/驱动/TIA/TFLN 有替代弹性，但高端 DSP/测试/材料仍是瓶颈 |
| Cambricon MLU 590/690 | 国产 AI 集群，2026 目标几十万颗级别 | 更偏 400G/800G/部分 1.6T；带动国产 SiPh、LPO、光模块与封测 |
| AMD MI350 | 以太网/Infinity Fabric scale-out，企业与云混合部署 | 800G/1.6T 模块确定；Helios/MI400 才会更强推动 1.6T/CPO/NPO |
| AWS Trainium3 | 3nm、144 chip UltraServer，2027 接棒 Trainium2 | 1.6T pluggable、LRO/LPO、800ZR/1600ZR DCI；若功耗受限，CPO pilot 提前 |
| Meta MTIA | Broadcom custom ASIC + 多 GW 推理集群 | Broadcom optics/DSP/CPO/SerDes、SiPh、OCS/光纤管理；Meta 参与 OCI MSA 推动光 scale-up 标准 |
| Microsoft Maia 200 | Azure 推理，216GB HBM3E、闭环液冷 | Azure scale-out/scale-across 拉动 800G/1.6T 与 coherent optics，Microsoft 参与 OCI MSA |

**推论：** 2026 光子材料收入主要跟随“交换机/光模块/数据中心互连”而不是直接跟随 GPU 封装。只有 CPO、NPO、光 I/O chiplet 和 OCI optical scale-up 进入量产后，光子材料才会从网络设备层进一步贴近 XPU package。

### 1.2 三情景技术成熟与放量时间

| 技术路径 | 2026 状态 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|---|
| 800G pluggable | 已放量，AI 集群标准件 | 2026 全年高量，2027 数量继续高但 ASP 下行 | 800G 与 1.6T 并行到 2027，800G 成成本敏感默认 | 需求太强导致 800G 短缺延长到 2027H1 |
| 1.6T pluggable 200G/lane | 多厂商产品/样机，2026 规模爬坡 | 2026 出货 >500 万只，2027 1,200-1,800 万只 | 2027 2,000-2,500 万只 | 2027 新增 AI 集群默认 1.6T，3,000 万只级别 |
| SiPh + InP EML/EAM/DFB | 1.6T 主力技术组合之一 | 2026-2027 持续放量 | SiPh foundry 产能和良率改善，替代更多 discrete optics | CPO/NPO 同时启动，SiPh wafer 与 InP active die 成瓶颈 |
| LPO/LRO/TRO linear optics | 800G 有部署，1.6T 推动 224G IC | 2026H2-2027 扩散 | 2027 成高端 AI module 标配之一 | DSP power wall 迫使 LPO/NPO 提前规模化 |
| CPO/CPX/NPO + ELS | NVIDIA/Broadcom/Coherent/Open CPX 推动 | 2026H2 pilot，2027 高端 switch 小规模，2028 更大放量 | 2027 socketed CPX/ELS 多客户部署 | 2027 成 102T/204T AI switch 默认高端选项 |
| 3.2T / 400G/lane | Broadcom/Coherent/OpenLight/HyperLight/NLM 样品密集 | 2026 验证，2027 小批量/现场 demo，2028 规模化 | 2027H2 小批量收入，2028H1 放量 | 204.8T switch 提前，2027 形成 30 亿美元+早期市场 |
| TFLN | HyperLight 20W 1.6T 参考模块、400G PIC、UMC/Jabil 量产路径 | 2026 低量/高端模块，2027 进入 1.6T/3.2T 部分 design-in | 2027 在 400G/lane 与 CPO/NPO 光引擎形成亿美元级收入 | 2027H2 在 3.2T 与低功耗 1.6T 中被多家头部模块厂采用 |
| EO polymer / SOH | Lightwave/NLM 进入 PDK、MPW、sampling | 2026 验证，2027 小批量，2028 才较大收入 | 2027H2 模块级 design win，200G/400G lane 先落地 | 2027 在 CPO/NPO/3.2T 中以低功耗优势快速切入 |
| BTO-on-Si | Veeco/imec 300mm process，Lumiphase 200mm platform | 2027 工程验证，2028 后量产 | 2027 有客户样片/NRE，2028 初收入 | 300mm 兼容性让 2028 前进入特定 CPO design-in |
| Optical I/O chiplet / Photonic Fabric | Lightmatter sampling，Marvell/Celestial 并购完成，Ayar 持续推进 | 2027 仍 pilot/NRE，2028 开始 meaningful revenue | 2027H2 开始 XPU/switch co-package 早期收入 | 2027 光 scale-up 被 OCI/客户需求前置，chiplet 市场提前数十亿美元化 |

### 1.3 2026 最可能兑现的技术路径排序

| 排名 | 方向 | 投资确定性 | 原因 |
|---:|---|---|---|
| 1 | 800G/1.6T 光模块、200G/lane optics | 极高 | 直接跟随 GB300、Ironwood、Trainium、MI350、MTIA；已有明确 2026 市场规模和出货占比 |
| 2 | SiPh/InP optical engine、EML/EAM/DFB/CW laser | 极高 | 1.6T/3.2T/CPO 共用瓶颈，Coherent/OpenLight/Broadcom/Tower/GF 都在加速 |
| 3 | DSP/driver/TIA/retimer/linear optics IC | 高 | 224G/448G 电光转换需要更高端 IC；LPO/LRO/TRO 改变价值分配但不消灭 analog front-end |
| 4 | CPO/CPX/NPO/ELS | 中高 | NVIDIA/Broadcom 官方路线明确，2026 是 design-in 和 pilot，2027 弹性大 |
| 5 | TFLN | 中高 | 有 6/8 英寸 foundry、模块演示、400G/lane PIC；但与 SiPh/InP/EO polymer 的成本/良率竞争未结束 |
| 6 | EO polymer/SOH | 中 | PDK 事件密集，但高温稳定、封装、可靠性、客户资格认证还需跑完 |
| 7 | BTO | 中低但长期弹性高 | 300mm 兼容性重要，但量产产品和客户规格仍早 |
| 8 | 光 I/O chiplet/photonic fabric | 高弹性但时点后移 | 价值巨大，Celestial/Lightmatter/Ayar 路线清晰；真实大收入更像 2028+ |

## 2. 已开始放量的关键产品：市场规模、渗透率、利润率

说明：未来 3 个月指 2026-05 至 2026-08 的收入窗口；未来 1 年指至 2027-05；未来 2 年指至 2028-05。渗透率按对应细分口径估算，例如“AI 光模块 value share”“高端 AI switch port share”“400G/lane transmitter share”。

### 2.1 产品拆分与三情景市场规模

| 已放量产品/技术 | 2026 当前状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| AI 专用 800G/1.6T 光收发模块合计 | 2026 市场已高速增长，TrendForce/LightCounting 均指向 260 亿美元级全年市场 | 基准 $6B-$8B；乐观 $8B-$10B；极度 $10B-$13B | 基准 $28B-$34B；乐观 $34B-$42B；极度 $45B-$55B | 基准 $45B-$60B；乐观 $65B-$85B；极度 $90B-$120B | 800G+ 占 AI 模块出货 2026 >60%，2027 70%-85%，2028 85%+ |
| 800G pluggable | 主流出货，Google/NVIDIA/国产集群均大量采购 | 基准 $4B-$6B；乐观 $5B-$7B；极度 $7B-$9B | 基准 $16B-$22B；乐观 $22B-$28B；极度 $28B-$36B | 基准 $16B-$25B；乐观 $25B-$35B；极度 $35B-$45B | AI 新增端口中 2026 约 50%-70%，2027 35%-55%，2028 20%-40% |
| 1.6T pluggable 200G/lane | 2026 从样机/早期部署进入规模爬坡，OFC 多厂商展示 | 基准 $1.2B-$2.5B；乐观 $2.5B-$4B；极度 $4B-$6B | 基准 $8B-$14B；乐观 $14B-$24B；极度 $24B-$35B | 基准 $18B-$35B；乐观 $35B-$55B；极度 $55B-$80B | AI 高端新增端口中 2026 10%-25%，2027 30%-55%，2028 45%-70% |
| 硅光 PIC/SiPh foundry 与光引擎 | Tower/GF/TSMC/Intel/Coherent/OpenLight 等持续放量，SiPh 市场 2026 约 $2.3B-$4.0B 取决口径 | 基准 $0.7B-$1.2B；乐观 $1.2B-$1.7B；极度 $1.7B-$2.4B | 基准 $3.2B-$5B；乐观 $5B-$7B；极度 $7B-$10B | 基准 $5.5B-$10B；乐观 $10B-$16B；极度 $16B-$25B | 800G+ 高速模块/PIC 价值中 2026 35%-50%，2027 45%-65%，2028 55%-75% |
| InP EML/EAM/DFB/CW laser/PD/VCSEL | 200G/lane 与 CPO/ELS 共用瓶颈，Coherent/Lumentum/OpenLight 高景气 | 基准 $1.5B-$2.5B；乐观 $2.5B-$3.5B；极度 $3.5B-$5B | 基准 $7B-$11B；乐观 $11B-$15B；极度 $15B-$22B | 基准 $10B-$18B；乐观 $18B-$28B；极度 $28B-$42B | 高端 1.6T/3.2T 发射端中 2026 50%+；2027 因 TFLN/EO polymer 上量仍保持 40%-60% |
| DSP/driver/TIA/retimer/linear optics IC | Broadcom Taurus、Semtech 224G、MACOM 448G、Credo/Marvell 等推进 | 基准 $1B-$1.8B；乐观 $1.8B-$2.8B；极度 $2.8B-$4B | 基准 $5B-$8B；乐观 $8B-$12B；极度 $12B-$18B | 基准 $8B-$15B；乐观 $15B-$25B；极度 $25B-$40B | 1.6T 模块 attach 高；LPO/LRO 改变结构但 analog IC attach 继续上升 |
| 800ZR/1.6T ZR/ZR+ coherent optics | AI scale-across/DCI 从 campus 到 metro，Marvell/Ciena/Nokia/Coherent/Cisco 受益 | 基准 $1.5B-$2.2B；乐观 $2.2B-$3B；极度 $3B-$4B | 基准 $7B-$10B；乐观 $10B-$14B；极度 $14B-$20B | 基准 $11B-$18B；乐观 $18B-$28B；极度 $28B-$40B | AI regional DCI 中 800ZR/1600ZR 2026 20%-35%，2027 35%-55%，2028 55%+ |
| 高速测试与验证设备 | 224G/448G、1.6T/3.2T、wafer optical test、FEC/MAC/BERT 需求旺 | 基准 $0.3B-$0.6B；乐观 $0.6B-$0.9B；极度 $0.9B-$1.3B | 基准 $1.5B-$2.5B；乐观 $2.5B-$4B；极度 $4B-$6B | 基准 $2.5B-$5B；乐观 $5B-$8B；极度 $8B-$12B | 3.2T 与 CPO qual 把测试时长/设备 attach 推高 |

### 2.2 已放量产品利润率三情景

| 产品/技术 | 当前毛利率判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|---:|
| 800G/1.6T 光模块 | 头部模块厂 25%-40%，EMS 约 10%-15% | 2026H2 ASP 下行，25%-35% | 1.6T mix 抵消降价，32%-42% | 供不应求持续，优质客户/高端规格 40%-50% |
| 硅光 PIC/光引擎 | 35%-55%，取决是否自有 IP/封装 | 35%-45% | 45%-55% | 55%-65%，若 foundry slot/PDK 稀缺 |
| InP 激光器/EML/EAM/PD | 40%-60%+ | 40%-50% | 50%-60% | 60%-70%，高功率 CW/ELS/400G lane 缺货 |
| DSP/driver/TIA/retimer | 芯片商 55%-75%，模块内 IC 价值高 | 55%-65% | 65%-72% | 70%-78%，若 3nm/224G/448G 供给紧 |
| Coherent optics | 系统/模块 35%-50%，DSP/IP 更高 | 35%-45% | 45%-55% | 55%-65%，若 AI DCI 急单拉动 |
| 测试设备 | 通常高毛利，软件/探针/夹具附加值高 | 50%-60% | 60%-68% | 68%-75%，若 448G qual 成瓶颈 |

## 3. 在研/即将快速增长的关键产品与细分技术

### 3.1 三情景市场规模、渗透率与利润率

| 在研/早期产品 | 2026 关键信号 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 | 毛利率三情景 |
|---|---|---:|---:|---:|---|---|
| CPO/CPX/NPO optical engine + ELS | NVIDIA 2026H2 Spectrum-X Photonics；Broadcom 102.4T CPO；Open CPX MSA；Coherent 6.4T socketed CPO | 基准 $50M-$200M；乐观 $200M-$500M；极度 $500M-$1B | 基准 $0.5B-$2B；乐观 $2B-$5B；极度 $5B-$10B | 基准 $3B-$10B；乐观 $10B-$25B；极度 $25B-$45B | 高端 AI switch port 2026 <2%，2027 5%-15%，2028 15%-35% | 基准 35%-50%；乐观 50%-60%；极度 60%-70% |
| 3.2T/400G-per-lane module/engine | Broadcom Taurus、Coherent 400G SiPh/EML、OpenLight 3.2T DR8 PIC alpha、HyperLight 400G TFLN | 基准 <$100M；乐观 $100M-$300M；极度 $300M-$700M | 基准 $0.3B-$1B；乐观 $1B-$3B；极度 $3B-$6B | 基准 $3B-$10B；乐观 $10B-$25B；极度 $25B-$45B | 400G/lane 发射端 2026 <1%，2027 3%-10%，2028 15%-35% | 基准 30%-45%；乐观 45%-60%；极度 60%+ |
| TFLN PIC/modulator | HyperLight 6/8 英寸 foundry、Jabil、20W 1.6T、400G PIC、145GHz packaged IM | 基准 $20M-$80M；乐观 $80M-$200M；极度 $200M-$500M | 基准 $0.2B-$0.8B；乐观 $0.8B-$2B；极度 $2B-$4B | 基准 $1B-$5B；乐观 $5B-$10B；极度 $10B-$18B | 1.6T/3.2T Tx PIC 2026 1%-3%，2027 5%-15%，2028 10%-30% | 基准 45%-55%；乐观 55%-70%；极度 70%-80% |
| EO polymer / SOH modulator | Lightwave 接入 SilTerra/Tower/GF PDK；NLM sampling 1.6T/3.2T SOH PIC | 基准 <$20M；乐观 $20M-$80M；极度 $80M-$200M | 基准 $30M-$200M；乐观 $200M-$800M；极度 $0.8B-$2B | 基准 $0.3B-$2B；乐观 $2B-$6B；极度 $6B-$12B | 400G/lane modulator 2026 <0.5%，2027 1%-5%，2028 5%-20% | 基准 40%-55%；乐观 55%-70%；极度 70%-85%（材料/IP 口径） |
| Plasmonic modulator | Marvell 2026-04 收购 Polariton；Polariton 2025/2026 展示 448G/lane 与 ultra-fast modulator sampling | 基准 <$20M；乐观 $20M-$100M；极度 $100M-$300M | 基准 $50M-$300M；乐观 $300M-$1B；极度 $1B-$2.5B | 基准 $0.5B-$3B；乐观 $3B-$8B；极度 $8B-$15B | 3.2T/6.4T 光引擎 2026 极低，2027 1%-5%，2028 5%-15% | 基准 45%-60%；乐观 60%-75%；极度 75%+ |
| BTO-on-Si modulator | Veeco/imec 300mm process；Lumiphase 200mm commercial BTO-silicon platform | 基准 <$10M；乐观 $10M-$50M；极度 $50M-$150M | 基准 $10M-$100M；乐观 $100M-$400M；极度 $400M-$1B | 基准 $0.1B-$1B；乐观 $1B-$3B；极度 $3B-$8B | 高端 modulator/PIC 2026 接近 0，2027 <3%，2028 3%-10% | 基准 35%-50%；乐观 50%-65%；极度 65%-80% |
| Optical I/O chiplet / Photonic Fabric | Lightmatter Passage 1.6Tbps/fiber、L20 6.4Tbps；Marvell 完成 Celestial AI 并购；Ayar TeraPHY | 基准 $50M-$200M；乐观 $200M-$600M；极度 $600M-$1.2B | 基准 $0.4B-$1.5B；乐观 $1.5B-$4B；极度 $4B-$8B | 基准 $2B-$10B；乐观 $10B-$25B；极度 $25B-$50B | XPU/switch package attach 2026 <1%，2027 1%-5%，2028 5%-15% | 基准 45%-60%；乐观 60%-70%；极度 70%+ |
| XPO 12.8T liquid-cooled pluggable | Arista XPO MSA，12.8T/module、204.8T/RU、最高 400W cooling | 基准 <$50M；乐观 $50M-$150M；极度 $150M-$400M | 基准 $0.2B-$0.8B；乐观 $0.8B-$2B；极度 $2B-$5B | 基准 $2B-$8B；乐观 $8B-$18B；极度 $18B-$30B | 204.8T switch interconnect 2027 小比例，2028 有望 10%-20% | 基准 30%-45%；乐观 45%-55%；极度 55%-65% |

### 3.2 在研技术的投资含义

**TFLN 的优势在低驱动电压、低光损耗、高带宽和减少激光数量。** HyperLight 1.6T-DR8 fully retimed 参考模块做到 **20W**，并称比替代技术低约 **20%**，还可用单颗 CW laser 替代常规两到四颗激光器。若在 1.6T/3.2T 中成为模块厂的低功耗设计选项，价值捕获会从“材料 wafer”扩到“Tx PIC + 封装 + KGD + 参考设计”。

**EO polymer/SOH 的价值在极低 VπL、高速、可 BEOL/slot waveguide 集成。** NLM 公开论文与公司资料显示 1.6T SOH PIC 已实现 224G PAM4，VπL <0.5 V-mm、>80GHz 3dB bandwidth，400G/λ 变体 >110GHz。Lightwave 2026 的商业信号不是收入，而是 PDK 与 foundry 路线：SilTerra/Luceda、Tower PH18、GF/GDSFactory 同时出现，说明客户试错成本下降。真正拐点是 2026H2-2027 的 engineering tapeout 是否能通过性能、可靠性、封装、良率四关。

**BTO 的价值在“硅光上做强 Pockels 效应”。** 如果 300mm BTO process 可靠，BTO 可能在长期兼具 EO polymer 的低功耗和硅光 foundry 的规模。但它还需要解决薄膜质量、晶向/畴控制、工艺热预算、长期漂移与量产均匀性。

**CPO/CPX/NPO 的收入弹性不只来自 optical engine。** 外置激光源 ELS、detachable fiber connector、光纤阵列、热管理、wafer-level test、system-level burn-in 都会变成新瓶颈。Open CPX MSA 的价值在于把“不可维护的封闭 CPO”推向 socketed/connectorized/多供应商生态。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构：地区、公司、工艺

| 地区 | 主要公司/机构 | 核心工艺与能力 | 投资观察 |
|---|---|---|---|
| 美国 | NVIDIA、Broadcom、Marvell、Coherent、Lumentum、Lightmatter、Ayar Labs、Lightwave Logic、NLM Photonics、MACOM、Semtech、Credo、Keysight/VIAVI | CPO/switch/DSP/SerDes/激光器/EO polymer/optical I/O chiplet/测试设备 | IP 与系统定义能力最强；制造多依赖 Tower/GF/TSMC/UMC/OSAT |
| 台湾 | TSMC、UMC、Wavetek、VisEra、ASE、Foxconn/FIT、Wiwynn 生态 | COUPE/SoIC/CoWoS、TFLN 6/8 英寸、光电封装、模块制造 | 先进封装和 SiPh/TFLN scale-up 的关键地区 |
| 以色列 | Tower Semiconductor | PH18/PH18DA/PH18M 硅光、InP-on-Si、SiPh foundry | NVIDIA 1.6T optical module、OpenLight、Coherent、Lightwave/NLM 路线交汇点 |
| 新加坡 | GF/Advanced Micro Foundry、TeraHop | SiPhab、200mm silicon photonics、MCF/光连接 | GF 收购 AMF 后，Singapore SiPh 产能战略价值上升 |
| 中国大陆 | Innolight、中际旭创、Eoptolink、新易盛、Accelink、TFC、Liobate、Ori-Chip、Linktel、Acon、华工正源等 | 光模块、LPO、TFLN、部分 SiPh、封装组装 | 模块规模强，但高端 DSP/激光器/测试设备/先进材料仍需补短板 |
| 欧洲 | imec、Ciena 欧洲研发、LIGENTEC、SMART Photonics、Sicoya、Sivers、OneTouch、Fraunhofer/CEA-Leti | BTO 300mm、SiN、InP foundry、TFLN/SiPh heterogeneous integration | 研发和 specialty foundry 强，量产需与美国/亚洲链条结合 |
| 日本/韩国 | Samsung Foundry、Sumitomo Electric、Furukawa、Fujitsu、NTT、Mitsubishi | 300mm SiPh、InP/光纤/连接器/光通信器件 | Samsung 2026 OFC 宣布 300mm SiPh PDK/production readiness，长期可能挑战 Tower/GF/TSMC |

### 4.2 关键供给瓶颈

1. **200G/400G-per-lane 光调制器良率。** SiPh PN MZM、InP EAM/EML、TFLN、EO polymer、BTO 都能在实验指标上讲出故事，但 1.6T/3.2T 要求 lane-to-lane 一致性、低 Vπ、低插损、低啁啾、低热漂、可测试性同时达标。
2. **激光器与 ELS。** CPO/NPO 把 laser 从模块内移到外置或共享架构，高功率 CW laser、DFB laser array、ELSFP、laser redundancy、fiber connector 可靠性会成为供给瓶颈。
3. **光电封装与耦合。** Flip-chip driver+modulator、fiber array attach、detachable fiber connector、high-density optical backplane、CPO socket、热漂移补偿、active alignment 自动化决定良率和产能。
4. **PDK 与 foundry qualification。** 新材料必须进入商业 foundry PDK、紧贴 design rule、compact model、wafer run、test structure；从 PDK 到客户 tapeout 到产品认证通常需要 6-18 个月。
5. **材料 wafer 规模化。** TFLN 从 6 英寸到 8 英寸、BTO 200mm/300mm、EO polymer spin-coating/poling/ALD encapsulation、SiPh SOI wafer 厚度/均匀性都会影响成本和可复制性。
6. **测试时间与设备。** 224G/448G PAM4、1.6T/3.2T FEC/MAC、wafer-level optical probing、thermal cycling、Telcordia GR-468、CPO system burn-in 会把测试变成隐形瓶颈。
7. **标准分裂。** OSFP/QSFP-DD、LPO/LRO/TRO、XPO、Open CPX、OCI、OIF CEI-224G/448G、UCIe optical 等并行，若客户规格不收敛，会增加库存和 NRE 风险。
8. **人才与跨学科集成。** 需要同时懂材料、光波导、RF、封装、热、系统网络、AI cluster workload 的团队，人才稀缺会限制初创公司交付。
9. **地缘与供应链认证。** 中国模块厂份额高，但高端云厂认证、出口管制、客户安全审查、美国本土制造要求可能影响订单分配。

### 4.3 BOM/单位成本拆分与价格传导

| 产品 | 典型成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 1.6T pluggable | DSP/retimer 25%-35%；光引擎/激光/PD/调制器 25%-35%；driver/TIA 10%-15%；封装耦合/FA 10%-20%；PCB/散热/壳体 5%-10%；测试/良率 10%-20% | 1.6T 早期良率、客户认证、DSP 与激光器稀缺、是否 LPO/LRO 降功耗 | 模块厂对云厂年度降价，但若关键器件短缺，激光/DSP/SiPh/TFLN 上游可保价 |
| SiPh PIC/optical engine | SOI wafer/processing 15%-25%；active/passive device 20%-30%；激光/III-V die 15%-25%；封装耦合 20%-30%；测试 10%-20% | PDK 锁定、光损耗、耦合效率、wafer-level yield、客户 reference design | foundry/设计平台通过 PDK 和 KGD 议价，客户换平台需重做设计和认证 |
| TFLN Tx PIC | TFLN wafer 10%-20%；刻蚀/电极/RF 20%-30%；KGD/test 20%-30%；封装/光纤耦合 20%-30%；IP/NRE 10%+ | 低插损、低驱动、减少 laser count、8-inch scale、Telcordia qualification | 若能减少激光数量和 DSP/driver power，可从客户 TCO 中抽取溢价 |
| EO polymer/SOH modulator | polymer/chromophore 材料低个位数到 10%；BEOL process/poling/encapsulation 20%-30%；SiPh foundry 20%-30%；test/reliability 20%-30%；license/IP 10%-30% | 高温稳定、封装可靠性、PDK adoption、低 VπL、3.2T/CPO 适配 | 材料 IP 可按 wafer/design/license 取费；若成为 PDK cell，切换成本高 |
| CPO/CPX optical engine | PIC/optical engine 25%-35%；ELS/laser 10%-20%；substrate/socket/connector 15%-25%；thermal/mechanical 10%-20%；test/burn-in 15%-25% | 可靠性、可维护性、field replaceability、与 switch ASIC 良率解耦能力 | 以系统 TCO、power saving、GPU 利用率定价；初期可有高溢价 |
| Optical I/O chiplet | PIC 20%-30%；EIC/SerDes/driver 25%-35%；先进封装/中介层 20%-30%；fiber attach/ELS 10%-20%；test 10%-20% | XPU package attach、UCIe/OCI 标准、CPO thermal co-design、良率 | 一旦进入 XPU reference design，随 AI 芯片平台代际锁定，议价最强 |

## 5. 竞争格局与壁垒

### 5.1 市场结构与集中度

| 层级 | 头部公司 | 集中度判断 | 竞争特点 |
|---|---|---|---|
| AI 光模块 | Innolight、Eoptolink、Coherent、Lumentum、Accelink、Fabrinet/Jabil/FIT、Cisco/Acacia、Marvell ecosystem | 高；Google 800G+ 订单中 Innolight+Eoptolink 被 TrendForce 估计接近 80% | 规模、客户认证、良率、成本下降速度决定份额；ASP 竞争风险高 |
| 硅光 foundry/PIC | Tower、TSMC、GF/AMF、Intel、Samsung、UMC/Wavetek、imec/CEA-Leti | 高；可量产 PDK 和客户 tapeout slot 稀缺 | PDK、design enablement、active integration、wafer-level test 是壁垒 |
| DSP/SerDes/driver/TIA | Broadcom、Marvell、Credo、Semtech、MACOM、MaxLinear、Alphawave、Synopsys IP | 高；3nm/224G/448G 设计门槛极高 | 功耗、FEC、link training、客户生态、先进节点供应 |
| InP/laser/EML/EAM/VCSEL | Coherent、Lumentum、Broadcom、OpenLight、Sony/II-VI legacy、Sumitomo、Furukawa、MACOM | 中高 | 高功率、可靠性、耦合和封装能力定价强 |
| TFLN | HyperLight、Liobate、OneTouch、Ori-Chip、Ciena/internal、Fujitsu/R&D、若干中国公司 | 早期高集中 | 8-inch foundry、low-loss etch、RF electrode、KGD、模块合作是核心 |
| EO polymer/SOH | Lightwave Logic、NLM Photonics、SilOriX、Polariton/Marvell、科研生态 | 极早期，IP 集中 | 材料稳定性、poling、PDK/BEOL、可靠性认证、客户 design win |
| BTO | Lumiphase、imec/Veeco、La Luce Cristallina、研究机构 | 极早期 | 300mm/200mm 薄膜质量、畴控制、CMOS thermal budget |
| Optical I/O chiplet | Lightmatter、Ayar Labs、Celestial AI/Marvell、Ranovus、Xscape Photonics、POET、Enosemi/AMD | 早期高集中 | XPU/switch co-design、package attach、software/network protocol lock-in |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 量化/验证方式 | 为什么能定价 |
|---|---|---|
| 客户认证周期 | Hyperscaler/module qual 常见 6-18 个月；Telcordia GR-468、thermal cycling、high-temp storage、burn-in | 认证后替换供应商要重做 link budget、FEC、thermal、firmware，切换成本高 |
| Lane-rate 性能 | 200G/lane 需要 70GHz+ 光电带宽；400G/lane 往往需要 110GHz-145GHz+ | 高频性能不只是材料指标，还要 RF packaging、驱动、损耗、均匀性；能过系统测试者少 |
| 功耗/TCO | 1.6T 模块每降低 3-5W，百万级模块对应 MW 级电力；CPO 宣称 5x optical power efficiency | AI 数据中心电力是硬瓶颈，节能可直接转化为更多 GPU/ASIC 上架，客户愿付溢价 |
| 激光数量与可靠性 | TFLN 参考设计可用 1 颗 CW laser；常规设计可能 2-4 颗 | 激光器是成本、功耗、失效率和供应瓶颈；减少 laser count 同时改善 BOM 和可靠性 |
| Foundry PDK 锁定 | PCell、compact model、design rule、MPW/tapeout；Tower/GF/SilTerra 等 PDK 接入 | 一旦设计在 PDK 中复用，供应商从单次样品变成客户设计流程的一部分 |
| 光电封装良率 | active alignment 时间、fiber attach yield、CPO socket/connector field failure | 量产中封装良率比器件峰值指标更重要；高良率供应商拿 premium allocation |
| 系统级架构绑定 | NVIDIA Spectrum-X、Broadcom Tomahawk/CPO、Google OCS、OCI MSA | 光互连不再是独立模块，而是 AI fabric 架构的一部分；架构绑定提高长期份额 |
| IP/专利 | Lightwave 70+ patents，HyperLight TFLN Chiplet，Marvell/Polariton/Celestial IP | 材料和器件结构若进入标准/PDK，许可费与设计锁定带来高 ROIC |

### 5.3 长期高 ROIC/高毛利层级

1. **高端 DSP/SerDes/driver/TIA 与 link training/FEC IP。** 高速模拟混合信号 + 先进节点 + 客户系统调试，毛利最稳定。
2. **激光器/ELS/高端 InP active devices。** 1.6T、CPO、coherent、TFLN/EO polymer 都需要高可靠光源；高功率 CW/DFB/EML 是共用瓶颈。
3. **材料 IP + PDK cell：TFLN、EO polymer、BTO。** 原材料本身 BOM 占比不高，但一旦作为 foundry PDK 的标准 modulator cell，利润可按 license/NRE/KGD/wafer platform 捕获。
4. **CPO/CPX/NPO optical engine 与 optical I/O chiplet。** 贴近 switch ASIC/XPU package，若进入平台参考设计，生命周期和议价远高于可插拔模块。
5. **wafer-level optical test 与系统验证设备。** 不随单一材料路线押注，3.2T/448G/CPO 越难，测试越有定价权。
6. **传统模块总装。** 收入最大、周转快，但 2027 后多供应商竞争和 ASP 下行会压缩 ROIC；只有深度绑定 hyperscaler 且掌握 SiPh/TFLN/packaging 的头部模块厂能保持较高利润。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点 1：1.6T 从展示进入“AI 新增集群默认升级项”

OFC 2026 的关键不是 800G 刚起来，而是 1.6T 已经进入多厂商产品化与客户验证。Cignal/本地 OFC 整理给出 2026 年 1.6T 出货 **>500 万只**的口径；TrendForce 给出 2026 AI 光模块 **260 亿美元**、800G+ 出货占比 **60%+**。最可能放量：

| 子方向 | 2026 放量逻辑 |
|---|---|
| 1.6T OSFP/DR8/2xDR4 | GB300/Ironwood/Trainium/MTIA 新增集群带动 |
| 200G/lane EML/EAM/SiPh | 1.6T Tx/Rx 共用瓶颈 |
| 224G driver/TIA/LRO/LPO | 降功耗，减少 DSP/retimer power |
| Wafer-level optical test | 1.6T/3.2T qual 提高测试复杂度 |

### 拐点 2：NVIDIA/Broadcom 把 CPO 从“概念”推入 2026H2 design-in

NVIDIA 官方在 Rubin/Spectrum-X Photonics 中明确 CPO，Broadcom 在 OFC 2026 展示 102.4T CPO switch、400G/lane Taurus DSP、3.5D XPU；Open CPX MSA 在 2026-03 成立，成员包括 Ciena、Coherent、Marvell、Molex、Samtec、TeraHop。最可能放量：

| 子方向 | 2026 放量逻辑 |
|---|---|
| ELS/高功率 CW laser | CPO 需要外置/共享光源，激光器是共用瓶颈 |
| Socketed CPX/NPO optical engine | 解决传统 CPO 可维护性问题 |
| CPO connector/fiber array/thermal | switch ASIC 旁边的光电封装变成新 BOM |
| CPO test/burn-in | 良率与 field service 决定是否从 pilot 进量产 |

### 拐点 3：TFLN/EO polymer 同时进入 foundry/PDK 工程化

HyperLight-UMC/Wavetek/Jabil/TFC/Broadcom/Eoptolink 的连续公告说明 TFLN 已进入模块级工程化；Lightwave/NLM 的 PDK、Tower/GF/SilTerra 路线说明 EO polymer/SOH 也在争取 200G/400G lane 的 foundry 入口。最可能放量：

| 子方向 | 2026 放量逻辑 |
|---|---|
| TFLN 1.6T Tx PIC | 20W 1.6T 参考模块和减少 laser count 是直接经济账 |
| TFLN 400G/lane PIC | 3.2T 与 CPO/NPO 的 2027 先行指标 |
| EO polymer PDK/tapeout | 2026 不是大收入年，但 PDK 事件是商业化前置条件 |
| Hybrid SiPh/TFLN/EO polymer | 硅光平台叠加新材料，而非替代硅光平台 |

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点 1：Rubin/MI400/TPU8/Trainium3 推动 1.6T 成新增 AI fabric 默认，3.2T 开始小批量

2027 的 GPU/ASIC 平台从 Blackwell Ultra 延展到 Rubin、MI400、TPU8、Trainium3/4、Meta/OpenAI/Broadcom ASIC。高端 AI fabric 将从“800G+少量 1.6T”切换到“1.6T 默认+3.2T 验证”。最可能放量：

| 子方向 | 2027 放量逻辑 |
|---|---|
| 1.6T pluggable | 新增 AI cluster 默认升级，2027 出货可达千万级到两千万级 |
| 400G/lane optics | 3.2T 模块、204.8T switch、CPO optical engine 前置需求 |
| 1600ZR/ZR+ | AI campus/metro scale-across 需求增强 |

### 拐点 2：CPO/CPX/NPO 从 pilot 转向高端 switch SKU

若 NVIDIA Spectrum-X Photonics、Broadcom Tomahawk/CPO、Open CPX 规格在 2026H2 跑通，2027 会出现第一批可重复采购的 CPO/CPX/NPO high-end AI switch SKU。最可能放量：

| 子方向 | 2027 放量逻辑 |
|---|---|
| 6.4T CPX optical engine | 200G/lane CPO/NPO 可先于 400G/lane 规模化 |
| ELSFP/laser bank | 激光器从模块内转到共享/外置，功率和可靠性定价上升 |
| Optical backplane/fiber management | AI rack/row scale 光连接密度大幅上升 |

### 拐点 3：EO polymer/TFLN/BTO 进入客户资格认证分化期

2027 会把 2026 的 PDK/样片故事筛掉一部分：只有通过客户温度、寿命、良率、封装和系统 link budget 的材料路线会进入 design win。最可能放量：

| 子方向 | 2027 放量逻辑 |
|---|---|
| TFLN | 具备最清晰 foundry + module assembly 路径，最可能先成亿美元级收入 |
| EO polymer/SOH | 若 Tower/GF/SilTerra tapeout 成功，2027H2 可能进入小批量模块/CPO |
| BTO | 工程样品/NRE，真正大收入更可能 2028+ |
| Plasmonic modulator | Marvell/Polariton 带来大厂资源，可能在 3.2T/6.4T optical engine 中验证 |

## 8. 头部公司与细分技术全景清单

### 8.1 模块、系统与 AI 网络平台

| 细分 | 公司 |
|---|---|
| AI 光模块/收发器 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、Accelink、Fabrinet、Jabil、FIT/Foxconn Interconnect、Cisco/Acacia、Hisense Broadband、AOI、Source Photonics、TFC、Linktel、Acon、POET ecosystem |
| AI switch/CPO 平台 | NVIDIA、Broadcom、Marvell、Cisco、Arista、Coherent、Ciena、Nokia、Molex、Samtec、TeraHop |
| Coherent DCI/线路系统 | Ciena、Nokia、Cisco/Acacia、Marvell、Coherent、Infinera/Nokia、Lumentum、NeoPhotonics legacy、NEC/Fujitsu |
| OCS/光交换/光纤管理 | Google Apollo ecosystem、Molex、Coherent、Calient、Polatis/HUBER+SUHNER、TeraHop、Corning、Senko、US Conec、Sumitomo、Furukawa |

### 8.2 硅光 foundry、PIC、集成平台

| 细分 | 公司/机构 |
|---|---|
| Silicon photonics foundry | Tower Semiconductor、TSMC、GlobalFoundries/AMF、Intel、Samsung Foundry、UMC/Wavetek、imec、CEA-Leti、AIM Photonics、VTT、Cornerstone/Southampton |
| InP-on-Si / heterogenous SiPh | OpenLight、Tower PH18DA、Coherent、Broadcom、Intel、GlobalFoundries ecosystem、Scintil Photonics、Sivers Photonics |
| SiN/low-loss photonics | LIGENTEC、imec、LioniX、VLC Photonics/Hitachi High-Tech、Anello Photonics、Lumentum/Coherent internal |
| Optical I/O chiplet | Lightmatter、Ayar Labs、Celestial AI/Marvell、Ranovus、POET Technologies、Xscape Photonics、Enosemi/AMD、Teramount、DustPhotonics、Avicena |

### 8.3 调制器与新材料

| 材料/技术 | 公司/机构 |
|---|---|
| InP EML/EAM/DFB/PD | Coherent、Lumentum、Broadcom、OpenLight、Sumitomo Electric、Furukawa Electric、MACOM、Sivers、三菱电机、Sony、Source Photonics |
| Silicon PN/MZM/ring modulator | Tower、Coherent、Intel、Broadcom、TSMC、GF/AMF、Samsung、imec、Cisco/Acacia、Marvell |
| TFLN | HyperLight、Liobate、OneTouch Technology、Ori-Chip Photonics、Ciena/R&D、Fujitsu/NTT/R&D、Eoptolink ecosystem、TFC ecosystem、中国多家 TFLN 初创/材料商 |
| EO polymer / SOH | Lightwave Logic、NLM Photonics、SilOriX、Polariton/Marvell、KIT/ETH/University of Washington ecosystem、Lumiphase adjacent material ecosystem |
| BTO | Lumiphase、imec/Veeco、La Luce Cristallina、EPFL/IBM research lineage、McGill/Lumiphase OFC papers、若干中国/欧洲研究团队 |
| Plasmonics | Polariton/Marvell、ETH Zurich lineage、Lightwave/NLM material ecosystem、科研机构 |
| VCSEL/多模 CPO | Lumentum、Coherent、Broadcom ecosystem、Sony、ams OSRAM、II-VI legacy、Molex/US Conec packaging ecosystem |

### 8.4 电芯片、驱动、测试、封装

| 细分 | 公司 |
|---|---|
| DSP/SerDes/retimer | Broadcom、Marvell、Credo、Semtech、MACOM、MaxLinear、Alphawave Semi、Synopsys、Cadence、Rambus、Astera Labs |
| Driver/TIA/CDR/linear optics IC | Semtech、MACOM、Broadcom、Marvell、Credo、MaxLinear、TI、Analog Devices、Renesas、Inphi/Marvell |
| 封装/连接器/光纤阵列 | Molex、Samtec、TE Connectivity、Amphenol、Senko、US Conec、Corning、Furukawa、Sumitomo、Jabil、Fabrinet、TFC、Foxconn/FIT、ASE、Amkor |
| 测试设备 | Keysight、VIAVI、Anritsu、Tektronix、Teledyne LeCroy、FormFactor、MPI、Teradyne、Advantest、MultiLane、EXFO |
| 材料/设备 | Soitec、SÜSS MicroTec、EV Group、Veeco、Applied Materials、Lam Research、ASMPT、KLA、Onto Innovation、DISCO、Entegris、DuPont、Corning |

## 9. 投资结论：更乐观的 AI 基建假设下如何排序

| 优先级 | 方向 | 2026-2027 beta | 核心理由 | 主要风险 |
|---:|---|---:|---|---|
| S | 1.6T 光模块 + 上游激光/SiPh/DSP | 高 | 收入当年兑现，AI 芯片出货强相关 | 2026H2-2027 ASP 下行，客户集中 |
| S | InP/laser/ELS/EML/EAM | 高 | 所有路线共用光源和 active device，CPO 进一步放大 | 激光可靠性、替代材料减少 laser count |
| A+ | CPO/CPX/NPO optical engine | 很高 | NVIDIA/Broadcom 官方路线明确，2027 弹性大 | 可维护性、封装良率、标准分裂 |
| A+ | TFLN | 很高 | HyperLight 已有 foundry+Jabil+模块演示，低功耗经济性清晰 | 成本、良率、与 SiPh/InP/EO polymer 竞争 |
| A | EO polymer/SOH | 极高 | PDK 接入密集，400G/lane/CPO 若成功弹性巨大 | 可靠性、客户认证、收入时点 |
| A | DSP/driver/TIA/测试 | 高 | 224G/448G 与 3.2T 越难，越有定价权 | LPO/模拟直驱路线可能改变芯片结构 |
| B+ | BTO | 极高但远期 | 300mm 兼容性和强 Pockels 效应有想象力 | 商业化最早也偏 2028，技术不确定 |
| B+ | Optical I/O chiplet | 极高但后移 | 若贴近 XPU package，长期价值最大 | 标准/客户/封装/软件栈复杂，收入 2028+ 更确定 |

**一句话排序：** 2026 买确定性看 1.6T 模块、InP/SiPh、DSP/driver/TIA、测试；2027 买弹性看 CPO/CPX/ELS、TFLN、EO polymer/SOH、光 I/O chiplet；2028+ 买长期颠覆看 BTO、plasmonics、XPU package optical scale-up。

## 10. 主要来源与交叉验证

| 来源 | 关键信息 |
|---|---|
| [TrendForce：Google 高速互连架构推动 800G+ 光模块 2026 占比 >60%](https://www.trendforce.com/presscenter/news/20260210-12919.html) | 800G+ 出货占比从 2024 年 19.5% 升至 2026 年 60%+；Google 订单结构 |
| [TrendForce：2026 AI 光收发模块市场 260 亿美元](https://www.trendforce.cn/presscenter/news/20260420-13018.html) | AI 专用光模块从 2025 年 165 亿美元到 2026 年 260 亿美元，YoY 57%+ |
| [LightCounting：Optics for AI clusters](https://www.lightcounting.com/newsletter/en/january-2026-optics-for-ai-clusters-366) | AI cluster optical transceiver 2025 165 亿美元、2026 260 亿美元 |
| [NVIDIA Silicon Photonics](https://www.nvidia.com/en-us/networking/products/silicon-photonics/) | Quantum-X800 CPO、Spectrum-X Photonics 2026H2、144x800G 等 |
| [NVIDIA Vera Rubin 官方新闻稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | Spectrum-X Ethernet Photonics CPO、5x optical power efficiency、10x resiliency |
| [NVIDIA Vera Rubin technical blog](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | Spectrum-6 SPX、102.4Tb/s、512 lanes、200Gb/s CPO |
| [Broadcom OFC 2026 AI infrastructure](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai) | 3.5D XPU、102.4T CPO switch、400G/lane DSP、200G/lane retimers/AEC |
| [Broadcom Taurus 400G/lane DSP](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next) | 400G/lane optical DSP、400G EML/PD、3.2T optical module foundation |
| [Coherent OFC 2026 pluggable technologies](https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026) | 1.6T/3.2T/XPO，400G differential EML 与 SiPh MZM |
| [Coherent OFC 2026 CPO](https://www.coherent.com/news/press-releases/coherent-co-packaged-optics-cpo-technologies-ofc-2026) | 6.4T socketed CPO、SiPh + ELS、VCSEL CPO、400G InP modulator |
| [OpenLight 3.2T DR8 PIC 与 1.6T LRO/LPO](https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants) | 448G EAM、3.2T DR8 alpha、bare die、evaluation board |
| [OpenLight volume production orders](https://openlightphotonics.com/newsroom/openlight-receives-first-volume-production-orders) | NewPhotonics 800G/1.6T laser-integrated PIC volume production orders on Tower PH18DA |
| [Tower + NVIDIA 1.6T SiPh modules](https://towersemi.com/2026/02/05/02052026/) | Tower 为 NVIDIA networking protocols 扩展 1.6T data center optical modules |
| [Tower + Coherent 400Gbps/lane silicon modulator](https://www.globenewswire.com/news-release/2026/03/23/3260248/0/en/tower-semiconductor-and-coherent-demonstrate-400gbps-lane-data-transmission-with-a-silicon-modulator-in-a-production-ready-sipho-process.html) | production-ready SiPh process 中 400Gbps/lane silicon modulator |
| [HyperLight + UMC/Wavetek TFLN HVM](https://www.businesswire.com/news/home/20260311544174/en/HyperLight-UMC-and-Wavetek-Announce-Strategic-Partnership-for-High-Volume-Foundry-Production-of-TFLN-Chiplet-Platform) | TFLN Chiplet 6/8 英寸高量产 foundry 路径 |
| [HyperLight + Jabil data-center deployment](https://www.businesswire.com/news/home/20260313758941/en/HyperLight-and-UMC-Collaborate-with-Jabil-to-Bring-TFLN-Photonics-to-Data-Center-Scale-Deployment) | TFLN 进入 hyperscale AI data center module deployment |
| [HyperLight 20W 1.6T-DR8](https://www.businesswire.com/news/home/20260316857906/en/HyperLight-Demonstrates-Low-Power-1.6T-DR8-TFLN-based-Reference-Transceiver-Assembled-by-TFC) | fully retimed 1.6T-DR8 20W，约低 20% power，单 CW laser |
| [HyperLight 400G/lane TFLN PIC](https://www.businesswire.com/news/home/20260317190165/en/HyperLight-Introduces-400G-per-lane-TFLN-PICs-on-its-Chiplet-Platform-for-Next-Generation-AI-Interconnects) | 400G/lane TFLN PIC，Broadcom/Eoptolink 认可其低功耗意义 |
| [Lightwave Logic + SilTerra/Luceda PDK](https://www.lightwavelogic.com/press-releases/silterra-silicon-photonics-platform-enables-integration-of-lightwave-logic-high-speed-polymer-modulators-through-luceda-photonics-pdk) | EO polymer modulator 接入 SilTerra PDK，目标 200G/400G lane |
| [Lightwave Logic + Tower PH18](https://www.nasdaq.com/press-release/lightwave-logic-and-tower-semiconductor-announce-development-agreement-enable-high) | 110GHz+ EO polymer modulator reference design、2026 multiple engineering tapeouts |
| [Lightwave Logic + GF/GDSFactory](https://www.nasdaq.com/press-release/lightwave-logic-high-speed-modulator-platform-now-available-gds-factory-pdk) | EO polymer modulator 接入 GF silicon photonics PDK，200G/400G lane validation |
| [NLM Photonics 1.6T/3.2T SOH PIC sampling](https://www.optica.org/about/newsroom/corporate_member_news/2026/nlm_photonics_initiates_sampling_of_1_6t_and_3_2t_silicon_organic_hybrid_pics/) | 1.6T/3.2T SOH PIC 向部分客户 sampling |
| [NLM + Tower PH18M validation](https://www.optica.org/about/newsroom/corporate_member_news/2026/nlm_photonics_validates_silicon_organic_hybrid_modulator_technology_with_tower_semiconductor_s_high-/) | SOH modulator 与 Tower PH18M MPW 初始处理完成 |
| [NLM SOH paper](https://arxiv.org/abs/2509.24825) | 224G PAM4、VπL <0.5 V-mm、>80GHz、400G/λ 变体 >110GHz |
| [Veeco + imec BTO 300mm process](https://www.imec-int.com/en/press/veeco-and-imec-develop-300mm-compatible-process-enable-integration-barium-titanate-silicon) | 300mm HVM-compatible BTO-on-SiPh process |
| [Marvell completes Celestial AI acquisition](https://www.marvell.com/company/newsroom/marvell-completes-acquisition-of-celestial-ai.html) | Photonic Fabric；H2 FY2028 revenue、$500M run-rate、FY2029 $1B run-rate |
| [Marvell acquires Polariton](https://www.marvell.com/company/newsroom/marvell-acquires-polariton-advancing-future-of-optical-connectivity.html) | plasmonics + Marvell silicon photonics/DSP for next-gen data center optical interconnect |
| [Lightmatter Passage 1.6Tbps/fiber](https://lightmatter.co/press-release/lightmatter-achieves-record-1-6-tbps-per-fiber-to-accelerate-ai-optical-interconnect/) | Passage CPO chiplet sampling，16-wavelength DWDM，1.6Tbps/fiber |
| [Lightmatter Passage L20](https://lightmatter.co/press-release/lightmatter-expands-photonic-interconnect-roadmap-with-passage-l20-unified-optical-engine-for-npo-and-obo-applications/) | 6.4Tbps optical engine for NPO/OBO，BiDi 降低 50% fiber management |
| [Open CPX MSA](https://www.opencpxmsa.org/) | Ciena、Coherent、Marvell、Molex、Samtec、TeraHop 发起 CPX/NPO optical engine 标准 |
| [Mordor/GlobeNewswire CPO market](https://www.globenewswire.com/news-release/2026/01/29/3228606/0/en/Co-Packaged-Optics-Market-Growing-at-35-92-CAGR-to-Reach-USD-0-75-Billion-by-2031-Reports-Mordor-Intelligence.html) | CPO 2026 $0.16B，2031 $0.75B，CAGR 35.92%；本报告对 AI 高端口径另作更乐观测算 |
| [GlobalFoundries acquires AMF](https://investors.gf.com/news-releases/news-release-details/globalfoundries-acquires-advanced-micro-foundry-accelerating) | GF 扩展 silicon photonics leadership 与 AI infrastructure portfolio |
| [GMI silicon photonics market](https://www.gminsights.com/industry-analysis/silicon-photonics-market) | Silicon photonics 2026 $2.3B、2031 $7B、2035 $17.8B，CAGR 25.3% |
| [IMARC silicon photonics market](https://www.imarcgroup.com/silicon-photonics-market-statistics) | Silicon photonics 2025 $2.6B、2034 $16.9B，CAGR 22.9% |
# 行业调研：【硅片、光刻胶与前道材料】

截至日期：2026-05-08  
研究口径：本报告把“硅片、光刻胶与前道材料”定义为晶圆制造前道消耗性材料和关键工艺材料，包括 300mm 硅片、外延/退火/SOI 硅片、EUV/ArF/KrF/i-line 光刻胶、显影/底涂/清洗等光刻辅助材料、CMP slurry/pad、湿电子化学品、电子气体、ALD/CVD 前驱体、PVD 靶材/电镀化学品、光掩膜基板/EUV pellicle 及高纯过滤/容器等。先进封装材料只在其与前道工艺强耦合时讨论，例如 hybrid bonding CMP/清洗和 HBM 相关前道 DRAM 材料。

本报告使用非常乐观的 AI 数据中心建设假设：2026 年 AI 芯片、HBM、CoWoS 与先进逻辑仍供不应求，2027 年 Rubin/HBM4/MI400/Trainium3/TPU8/自研 ASIC 接棒。缺少直接数据的地方，用“先进节点晶圆开工、EUV 层数、HBM wafer intensity、客户认证周期和材料单片价值量”做自下而上推演。

## 1. 核心结论

1. **2026 最确定的材料主线是 300mm 先进逻辑/DRAM 硅片、EUV/ArFi 光刻材料、CMP、电子气体和先进前驱体同步扩张。** SEMI 2026Q1 全球硅片出货 3,275 MSI，同比 +13.1%；SEMI 2025 年中材料展望给出 2026 晶圆厂材料市场约 `$48.9B`，其中硅片 `$14.3B`、CMP `$3.9B`、电子气体 `$6.8B`、湿化学品 `$4.1B`、光刻胶约 `$3.0B`。
2. **AI 对材料的拉动不是“单颗 GPU 很贵”，而是“先进节点 wafer starts + HBM DRAM wafer intensity + EUV 层数 + 良率保险”一起上升。** Gartner 2026 半导体收入预测 `$1.320T`，AI 半导体约占 `30%`，hyperscaler AI 基建支出预计 +50% 以上；这会把上游材料从周期复苏推向结构性偏紧。
3. **硅片行业出现分裂：300mm 高端紧，200mm 和部分成熟节点仍弱。** Siltronic 2026 指引仍谨慎，但 CEO 明确 AI 端市场支撑 300mm volume；SUMCO 也强调 300mm leading-edge demand 将继续增长。投资上应买“高端 300mm/epi/SOI/客户认证”，不是泛硅片 beta。
4. **EUV 光刻胶 2026 是低 NA EUV 放量年，High-NA 是 2027-2028 期权。** TOK 指引 2026 EUV photoresist 销售双位数增长，HBM using TOK resists 已进入量产；ASML 说 High-NA 已处理超过 50 万片 wafer、可用率超过 80%，但真正 HVM 仍更可能从 2027-2028 开始。
5. **MOR 和 dry resist 是 2026 最值得跟踪的新材料。** imec 在 SPIE 2026 报告：MOR 在 PEB 中把氧浓度从 21% 提到 50%，photo-speed 提升 15-20%；JSR/Inpria 与 Lam 2025 年签 cross-license，Lam Aether dry resist 已被一家领先存储厂选为先进 DRAM tool of record，IBM/Lam 2026 年又把 Aether 推向 sub-1nm/high-NA 流程。
6. **毛利最有可能长期保持高位的层级：EUV/MOR/dry resist、先进 ALD/CVD 前驱体和 selective etch、hybrid bonding CMP/clean、高端 300mm epi/SOI、光掩膜 blank/EUV pellicle。** 这些环节的共同点是认证周期长、缺陷代价巨大、客户共研深、二供切换慢。
7. **供给瓶颈不止设备。** ppb/ppt 级纯化、金属杂质控制、容器/过滤/超净物流、客户认证、PFAS 替代、稀有气体/氦气、钌/钼/钴前驱体可得性、EUV mask/pellicle 和材料工程师都是瓶颈。
8. **中国材料国产化会同时带来量和价格压力。** 中国在成熟硅片、湿化学品、电子气体、CMP 部分环节快速推进，但 EUV/ArFi 高端胶、300mm leading-edge prime/epi、先进前驱体和 EUV mask blank 仍高度依赖海外头部。

## 2. 关键一手信息与交叉验证

| 时间 | 来源 | 关键事实 | 对本报告的含义 |
|---|---|---|---|
| 2026-04 | [SEMI 硅片出货](https://www.semi.org/en/semi-press-release/semi-reports-worldwide-silicon-wafer-shipments-increase-13-percent-year-on-year-in-q1-2026) | 2026Q1 全球硅片出货 `3,275 MSI`，同比 +13.1%，环比 -4.7% 符合季节性。 | 2026 已从库存周期走向 AI/HBM/先进逻辑拉动的 300mm 恢复。 |
| 2025-09 | [SEMI Materials Outlook PDF](https://www.semi.org/sites/semi.org/files/2025-09/5%20Clark%20Tseng_Building%20the%20Future-AI%20Investment%2C%20Equipment%20%26%20Materials%20Market%20Outlook.pdf) | 2026 WFM `$48.9B`；硅片 `$14.3B`；湿化学品 `$4.1B`；photomasks `$6.2B`；CMP `$3.9B`；电子气体 `$6.8B`；光刻胶 `$3B`，advanced PR 占比 2024 约 80%，2028 约 84%。 | 用作本报告市场规模底座。 |
| 2026-04 | [Gartner 半导体预测](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | 2026 半导体收入 `$1.320T`，2027 `$1.555T`；2026 memory `$633.3B`；AI 半导体约占 2026 总收入 30%；hyperscaler AI 基建支出 +50% 以上。 | 支撑极乐观 AI capex 假设，也解释 HBM/DRAM 对材料需求的挤出效应。 |
| 2026-04 | [TSMC 2026Q1](https://investor.tsmc.com/english/quarterly-results/2026/q1) | 2026Q1 revenue `$35.90B`，毛利率 66.2%，2Q26 指引 `$39.0B-$40.2B`、毛利率 65.5-67.5%。 | 先进逻辑需求仍强，材料客户的议价和产能利用率受 TSMC 节奏牵引。 |
| 2026-04 | [Samsung 2026Q1 presentation](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_1Q_conference_eng.pdf) | DS 业务 2026Q1 sales `KRW 81.7T`，OP margin 42.8%；memory 指出 AI 产品、HBM4、SOCAMM2、PCIe Gen6 eSSD，H2 继续 AI 产品中心策略；foundry advanced node lines full utilization，4nm memory products and LPU for AI/HPC ramp。 | HBM4 和 AI memory 会继续拉动 DRAM EUV、CMP、前驱体、电子气体。 |
| 2026-02/04 | [Siltronic 2026 指引](https://www.siltronic.com/en/press/press-releases/siltronic-releases-its-guidance-for-financial-year-2026.html) / [Q1](https://www.siltronic.com/en/press/press-releases/siltronic-closes-q1-2026-in-line-with-expectations.html) | 2026 仍有汇率、200mm、价格压力，但“AI-driven end markets clearly supporting 300mm volume”；Q1 sales `EUR 306.5M`，EBITDA margin 21.2%。 | 硅片不是全面短缺，高端 300mm 与 200mm 成熟市场分化很大。 |
| 2026-05 | [GlobalWafers Q1](https://www.sas-globalwafers.com/en/gwc_news_en_20260505/) | AI/HPC demand 支撑上游 wafer shipments 逐步改善；Missouri 12-inch SOI 新设备完成部分认证，RF 与 silicon photonics 产品 2026Q1 量产。 | SOI/硅光硅片可能成为 AI 光互联和 CPO 的 2026-2027 期权。 |
| 2026-02 | [SUMCO management policy](https://www.sumcosi.com/english/ir/financial/managementpolicy.html) | 300mm leading-edge semiconductors demand 预期继续增长；200mm AI data center related demand 增加但总体持平；150mm 以下长期收缩。 | 300mm/200mm/150mm 的投资逻辑不同。 |
| 2026-02 | [TOK FY2025 Q&A](https://www.tok.co.jp/application/files/4017/7097/4316/q4_QA_Summary_en.pdf) | EUV photoresist 2026 预期双位数增长；HBM using TOK photoresists 已量产；某客户 2025 销售同比翻倍且 TOK share 超 50%；WHS materials 2025 年约 +40%。 | EUV 胶和 HBM DRAM 已经不是实验室主题，而是材料收入增长源。 |
| 2025-09 | [JSR/Inpria + Lam](https://www.jsr.co.jp/jsr_e/news/2025/20250916.html) | 双方围绕 MOR、High-NA EUV patterning、Lam Aether dry resist、etch/deposition 集成协作。 | MOR/dry resist 进入产业链共研窗口。 |
| 2026-02 | [imec SPIE 2026](https://www.imec-int.com/en/press/imec-unlocks-lever-euv-dose-reduction-oxygen-injection-during-metal-oxide-resist-post) | MOR 在高氧 PEB 下 photo-speed 提升 15-20%，可降低 EUV dose、提高 scanner throughput。 | 如果工程化成功，MOR 的价值不仅是分辨率，还有 EUV 设备吞吐提升。 |
| 2026-03 | [Lam + IBM Aether](https://newsroom.lamresearch.com/ibm-lam-sub-1nm-logic-aether-dry-resist) | IBM/Lam 五年合作，Aether dry resist 用于 high-NA EUV sub-1nm logic flow；2025 年 Lam Aether 已被领先存储厂选为先进 DRAM tool of record。 | Dry resist 2026-2027 先在 DRAM/HBM critical layers 放量概率高于先进逻辑全面放量。 |
| 2026-04 | [Fujifilm fluorine-free ArFi](https://www.fujifilm.com/de/en/news/hq/13549) | Fujifilm 开发全球首个 fluorine-free negative ArF immersion resist，面向 AI semiconductors advanced nodes，已向客户提供样品，并计划向 EUV 材料扩展。 | PFAS/含氟替代是 2026 新增监管和客户 RFP 变量。 |
| 2026-02 | [Qnity Eon EUV](https://www.qnityelectronics.com/news/qnity-expands-offerings-for-extreme-ultraviolet-lithography.html) | Qnity 推出 Eon EUV photoresist，并配套 AR EUV underlayer、EUVSolv cleans。 | DuPont/Qnity 正从 ancillary 扩到 EUV 胶本体，竞争格局可能多极化。 |
| 2026-04 | [Entegris Q1](https://investor.entegris.com/news/news-details/2026/Entegris-Reports-Results-for-First-Quarter-of-2026/default.aspx) | Q1 sales `$811.9M`，gross margin 46.9%；公司称 AI demand reflected in strengthening order patterns；MS 包括 CVD/ALD 材料、CMP、etch/clean、implant gases。 | 前道材料龙头的订单已经能看到 AI 传导。 |
| 2026-04 | [Air Liquide Q1 PDF](https://www.airliquide.com/sites/airliquide.com/files/2026-04/air-liquide-presentation-q1-growth-performance-and-record-investments-air-liquide-continues-on-its-successful-trajectory-in-q1-2026.pdf) | Electronics Q1 sales `EUR 628M`，carrier gases +9%，advanced materials 亚洲显著增长；investment backlog `EUR 5.5B`，>40% 在 Electronics。 | 电子气体和 advanced materials 是长期合同型高确定性收入。 |
| 2026-03 | [TechInsights electronic gases](https://www.techinsights.com/blog/electronic-gases-market-reach-681b-2026-driven-advanced-node-demand) | 2026 半导体电子气体收入约 `$6.81B`，同比 +5.5%；specialty gases +5.8%，bulk gases +4.9%；半导体用氦约占全球供应 21%。 | 氦、稀有气体和超高纯 specialty gases 是材料端隐性瓶颈。 |
| 2026-04 | [ASML Q1 transcript](https://ourbrand.asml.com/asset/8e1f7393-33dd-4737-a436-cfe1b68cc577/2026_04_15-ASML-Transcript-investor-call-Q1-2026.pdf) | High-NA 已处理超过 50 万片 wafer、可用率超过 80%；单次 High-NA exposure 可替代 3-4 次 Low-NA exposure，某些 critical layers 工序数可降 10 倍；resist 进展支持 18nm logic L/S、28nm DRAM contacts。 | High-NA 材料选择在 2026 定局，收入在 2027-2028 加速。 |

## 3. AI 芯片路线对材料需求的映射

项目内《全球 AI 芯片路线图与 2026-2027 产能释放预测》显示，2026-2027 年初出货/价值权重最高的平台大致为：NVIDIA GB300/B300、AWS Trainium2、Google TPU v7 Ironwood、NVIDIA GB200/B200、Huawei Ascend 910C/950、Cambricon 590/690、AMD MI350、AWS Trainium3、Meta MTIA、Microsoft Maia 200、Alibaba Zhenwu、AMD MI400/MI455X。对材料行业的含义如下。

| 芯片/平台 | 2026-2027 制程与封装背景 | 对硅片的拉动 | 对光刻胶的拉动 | 对前道材料的拉动 |
|---|---|---|---|---|
| NVIDIA B300/GB300 | TSMC 4NP/先进 DUV+EUV，HBM3E，CoWoS-L，2026 主力 | 高端 300mm prime/epi，极低缺陷密度，高 flatness | Low-NA EUV + ArFi 仍主流，critical layers 胶和 underlayer 价值高 | CMP、Cu/barrier、low-k、Hf/Zr/Si 前驱体、清洗和过滤；HBM3E 间接拉动 DRAM EUV |
| AWS Trainium2 | 自研 ASIC，Rainier 百万颗级目标，HBM + advanced packaging | 先进 300mm logic wafer starts，客户锁量 | 先进 DUV/EUV 多供应链，外部可见度低 | ALD/CVD、CMP、selective etch、电子气体，供应链被 AWS/代工厂内化 |
| Google TPU v7 Ironwood | 先进节点，192GB HBM，AI inference pod | 先进逻辑 300mm，长期预留 capacity | EUV/ArFi intensity 随 TPU scale 走高 | 前驱体、CMP、wet cleans、HBM DRAM 材料；Google 对材料供应商可见度低但量大 |
| NVIDIA GB200/B200 | Blackwell 现有平台，2026 延续交付 | 300mm 先进节点仍大量消耗 | Low-NA EUV/ArFi 成熟胶 | 与 GB300 类似但新增弹性低于 GB300 |
| Huawei Ascend 910C/950 | SMIC N+2/N+3，DUV 多重曝光，国产替代 | 中国 300mm 国产/进口高端 wafer 双线紧张 | ArFi/KrF/i-line 用量高，EUV 受限；国产 ArF 胶验证加速 | DUV 多重曝光放大 CMP、湿化学品、etch、清洗和 metrology 消耗 |
| Cambricon 590/690 | 中国先进 DUV 节点，HBM/封装受限 | 国产 300mm 高端硅片和进口高端硅片并用 | 国产 ArF/KrF 胶导入窗口 | 国产电子气体、CMP、湿化学品受益；良率压力提升材料价值 |
| AMD MI350 | HBM3E，企业 PCIe/UBB，2026 AMD 确定产品 | 先进逻辑 300mm | EUV/ArFi 成熟胶 | HBM3E、CMP、前驱体、ultra-clean fluids |
| AWS Trainium3 | 3nm UltraServer，2026 初期/2027 主力 | 3nm class 300mm wafer | EUV 层数更高，胶和 underlayer ASP 上升 | GAA/3nm 前驱体、CMP、electronics gases，系统级 burn-in |
| Meta MTIA / Broadcom XPU | TSMC/Broadcom 定制 ASIC，>1GW 初期 | 长协锁定 leading-edge wafers | EUV/ArFi，客户定制流程 | Broadcom 体系拉动 Ethernet/ASIC 先进节点材料，客户锁供应 |
| Microsoft Maia 200 | TSMC 3nm，216GB HBM3E，Azure 液冷推理 | 3nm 300mm | EUV/ArFi | HBM3E、SRAM/cache、CMP、selective deposition |
| AMD MI400/MI455X | 2026H2 首批，HBM4，2027 放量 | 2nm/3nm 组合，N2 wafer starts 增量 | EUV 层数和 MOR/high-NA eval 增量 | HBM4 DRAM、GAA/BSPD、advanced CMP、Mo/Ru/Co precursors |

**2026 最可能的技术路径：** Low-NA EUV + ArF immersion 仍是绝对主线；300mm leading-edge prime/epi 硅片供给偏紧；HBM3E/早期 HBM4 带动 DRAM EUV 和 dry resist/MOR 评估；GAA/N2/A16 只在少数高端 AI/HPC 芯片开始形成增量；High-NA EUV 主要是 customer product wafer test 和材料 stack 定点。

## 4. 机遇、挑战与新技术成熟时间

| 技术/材料路线 | 目前使用状态 | 基准情景成熟/放量 | 乐观情景成熟/放量 | 极度超预期情景成熟/放量 |
|---|---|---|---|---|
| 300mm leading-edge prime/polished wafer | 已大规模使用，先进逻辑和 HBM DRAM 必需 | 2026 全年恢复，2027 随 N2/HBM4 加速 | 2026H2 出现明显 allocation 和高端 wafer ASP 上行 | 2026Q3 开始客户重新签 2027-2028 LTA，现货溢价扩大 |
| 300mm epi/annealed wafer | 先进逻辑、电源管理、部分 DRAM/CMOS image sensor 用 | 2026 稳步增长，2027 GAA 与 power management 增量 | 2026H2 先进 epi 产能紧张 | 2027 高端 epi 供给成为部分 AI ASIC wafer start 瓶颈 |
| SOI/硅光硅片 | RF、硅光、部分 CPO/optical I/O | 2026 小规模，2027 受 1.6T/CPO 拉动 | 2026H2 CPO 供应链提前锁单，2027 明显放量 | 2027 硅光 I/O 被大客户 AI switch/ASIC 设计采用，SOI 需求跳升 |
| EUV CAR 光刻胶 | 当前先进逻辑/DRAM 主力 | 2026 双位数增长，2027 随 HBM4/2nm 继续 | 客户为降低 EUV dose 接受更高 ASP | EUV 胶成为 ASML throughput 的经济杠杆，供应商议价大幅增强 |
| ArF immersion 胶和 ancillary | 使用最广的先进光刻材料 | 2026 稳定增长，PFAS-free 进入客户 eval | PFAS-free/fluorine-free 2027 大客户导入 | 2026H2 即被头部客户列入绿色采购/废水成本优化项目 |
| MOR 金属氧化物 EUV resist | DRAM/logic eval，Inpria/JSR、imec 进展快 | 2027 少数 DRAM/logic critical layers 量产，2028 扩大 | 2026H2 DRAM/HBM 进入小批量，2027 主流化 | 2026Q4 头部客户把 MOR 作为部分高分辨层默认方案 |
| Lam Aether dry resist | 领先存储厂 advanced DRAM tool of record，IBM 2026 共研 high-NA logic | 2027 DRAM/HBM critical layers 贡献收入，logic 2028 后 | 2026H2 在 HBM4/1c/1d DRAM 前置放量 | 2027 成为 high-NA 早期 HVM 的核心 stack |
| High-NA EUV resist stack | 2026 product wafer test，ASML 平台成熟中 | 2027-2028 HVM 插入，先 DRAM 和 Intel/Samsung selected logic | 2027H1 部分客户 HVM，材料订单提前 2-3 季 | 2026H2 材料定点导致高端 resist/underlayer 订单先爆发 |
| GAA/high-k/metal gate precursors | 2nm/GAA 必需，Hf/Zr/Si/Ti/Ta/W 等成熟但规格升级 | 2026H2 随 N2/A16 增量，2027 快速增长 | 2026 即因 N2/18A/2nm 预留产能偏紧 | 2027 先进 precursor 成为供给瓶颈，毛利率上修 |
| Backside power delivery 材料 | A16/Intel 18A 等导入期 | 2027 初步量产，2028 扩大 | 2026H2 AI/HPC 芯片导入 BSPD | 2027 BSPD 工艺材料成为先进节点差异化定价来源 |
| Mo/Ru/Co interconnect/liner/barrier | 高端逻辑和 DRAM eval 到量产过渡 | 2027 增量明显 | 2026H2 selected layers 放量 | 2027 大客户批量切换，precursor/target 紧缺 |
| Hybrid bonding CMP/clean | HBM/3D bonding、SoIC、逻辑到内存互联 | 2026 已放量，2027 加速 | 2026H2 与 CoWoS/SoIC 一起偏紧 | 2027 HBM4 和 3D logic 让 ultra-flat CMP/clean 成高毛利 bottleneck |

## 5. 已经开始放量的关键产品：市场规模、渗透率、利润率

口径说明：市场规模为全球半导体用材料收入池，单位为美元；“未来 3 个月”为 2026-05 至 2026-08 累计收入/订单兑现；“一年”为 2026-05 至 2027-05 累计；“两年”为 2026-05 至 2028-05 累计。渗透率指在 AI/HPC 相关先进逻辑、先进 DRAM/HBM 和高端数据中心相关晶圆制造中的采用/暴露度，不是全半导体渗透率。

| 已放量产品 | 3 个月规模：基准/乐观/极超 | 一年规模：基准/乐观/极超 | 两年规模：基准/乐观/极超 | 渗透率路径 | 毛利率：基准/乐观/极超 |
|---|---:|---:|---:|---|---|
| 300mm prime/polished 硅片 | `$2.7-3.2B / $3.2-3.8B / $3.8-4.6B` | `$11-13B / $13-16B / $16-20B` | `$24-29B / $30-37B / $38-48B` | AI/HPC advanced wafer starts 2026 85-95%，2027 接近 100%；全行业 300mm 份额继续上升 | 28-36% / 34-43% / 42-52% |
| 300mm epi/annealed/high-spec wafer | `$0.7-1.0B / $1.0-1.4B / $1.4-1.9B` | `$3.0-4.2B / $4.2-5.8B / $5.8-8.0B` | `$7-10B / $11-15B / $16-23B` | 先进逻辑/电源/DRAM 2026 25-35%，2027 35-50%，2028 45-60% | 35-48% / 42-55% / 50-62% |
| SOI/硅光硅片 | `$0.18-0.35B / $0.35-0.55B / $0.55-0.85B` | `$0.8-1.4B / $1.4-2.3B / $2.3-3.5B` | `$2.0-3.8B / $4.0-7.0B / $7.5-12B` | AI 光互联/硅光/CPO 2026 3-8%，2027 8-18%，2028 15-30% | 35-50% / 45-58% / 55-68% |
| EUV photoresist + EUV underlayer/clean | `$0.35-0.55B / $0.55-0.85B / $0.85-1.25B` | `$1.6-2.4B / $2.4-3.4B / $3.4-5.0B` | `$4.0-6.5B / $6.5-10B / $10-15B` | 先进逻辑 EUV 层 2026 高渗透；HBM DRAM EUV 2026 20-35%，2027 35-55% | 55-68% / 60-72% / 65-78% |
| ArF immersion photoresist + BARC/topcoat/developer | `$0.9-1.2B / $1.2-1.6B / $1.6-2.1B` | `$3.8-4.8B / $4.8-6.2B / $6.2-8.0B` | `$8.0-10.5B / $11-15B / $16-22B` | AI/HPC advanced layers 2026 90%+，中国 DUV 多重曝光提升用量 | 42-55% / 48-60% / 52-65% |
| KrF/i-line 胶和成熟光刻材料 | `$0.45-0.65B / $0.60-0.85B / $0.80-1.15B` | `$1.8-2.5B / $2.5-3.4B / $3.4-4.8B` | `$3.8-5.4B / $5.5-7.8B / $8-11B` | 先进封装、功率、成熟逻辑、中国扩产支撑；AI 直接相关低但间接受益 | 32-45% / 38-50% / 45-55% |
| CMP slurry & pads | `$0.95-1.15B / $1.15-1.45B / $1.45-1.85B` | `$4.0-4.8B / $4.8-6.0B / $6.0-7.8B` | `$8.5-10.5B / $11-14B / $15-20B` | 先进逻辑/HBM/3D bonding 2026 55-70%，2027 65-80%，2028 75-90% | 38-50% / 45-55% / 50-62% |
| 高纯湿化学品、post-CMP/etch cleans | `$1.0-1.25B / $1.25-1.6B / $1.6-2.1B` | `$4.3-5.3B / $5.3-6.8B / $6.8-9.0B` | `$9-12B / $12-16B / $17-24B` | 所有 wafer 必配；先进节点用量和纯度同步上升，AI/HBM 2026 35-45%，2027 45-60% | 20-35% / 25-40% / 30-45% |
| 电子气体：bulk + specialty | `$1.75-2.05B / $2.05-2.45B / $2.45-3.0B` | `$7.0-8.3B / $8.4-10.2B / $10.5-13B` | `$14.5-17.5B / $18-23B / $24-32B` | 先进节点和 HBM 2026 35-50%，2027 50-65%；bulk 气体合同锁定，specialty 溢价高 | 30-45% blended；specialty 40-60%；极超 45-65% |
| ALD/CVD 前驱体 | `$0.75-1.05B / $1.05-1.45B / $1.45-2.0B` | `$3.2-4.4B / $4.5-6.2B / $6.2-8.8B` | `$7.5-11B / $12-17B / $18-28B` | GAA、high-k、DRAM capacitor、Mo/Ru/Co 2026 25-40%，2027 40-60% | 45-60% / 50-65% / 55-72% |
| PVD 靶材、电镀化学品、barrier metals | `$0.65-0.9B / $0.9-1.2B / $1.2-1.7B` | `$2.8-3.8B / $3.8-5.2B / $5.2-7.2B` | `$6-8.5B / $9-13B / $14-21B` | Cu/Ru/Co/Mo interconnect、HBM TSV/electroplating、2026 30-45%，2027 45-60% | 25-42% / 35-50% / 42-58% |
| Photomask blanks、EUV mask、pellicle | `$1.4-1.7B / $1.7-2.1B / $2.1-2.7B` | `$6.2-7.4B / $7.5-9.2B / $9.5-12B` | `$13-16B / $17-22B / $23-32B` | EUV mask 层数、2nm/High-NA eval、工程改版；2026 20-35%，2027 35-55% | 40-58% / 48-62% / 55-70% |
| 高纯过滤、FOUP、chemical delivery/containers | `$0.75-1.0B / $1.0-1.3B / $1.3-1.8B` | `$3.3-4.3B / $4.3-5.8B / $5.8-8.0B` | `$7-9.5B / $10-14B / $15-22B` | 先进节点污染控制要求提高，2026 45-60%，2027 55-70% | 42-55% / 48-60% / 55-65% |

**增长预测区间：**

| 产品组 | 2026-2027 基准增速 | 乐观增速 | 极度超预期增速 | 主要驱动 |
|---|---:|---:|---:|---|
| 300mm 高端硅片 | +8-15% | +15-25% | +25-40% | AI/HPC wafer starts、HBM DRAM、N2/A16/3nm |
| EUV 胶与 ancillary | +15-25% | +25-40% | +40-65% | DRAM EUV、2nm、客户为 EUV throughput 付费 |
| ArFi/KrF | +5-12% | +12-22% | +22-35% | 中国 DUV、多重曝光、成熟电源管理 |
| CMP | +10-18% | +18-30% | +30-50% | HBM、hybrid bonding、GAA、BSPD |
| 电子气体 | +5-10% | +10-18% | +18-30% | On-site gas、specialty gases、氦/稀有气体紧张 |
| ALD/CVD 前驱体 | +12-22% | +22-38% | +38-60% | GAA、DRAM、Mo/Ru/Co、high-k |
| 湿化学品/清洗 | +8-15% | +15-25% | +25-40% | 层数、清洗次数、缺陷容忍度下降 |

## 6. 在研关键产品与快速增长技术

| 在研/早期放量技术 | 3 个月规模：基准/乐观/极超 | 一年规模：基准/乐观/极超 | 两年规模：基准/乐观/极超 | 渗透率路径 | 毛利率：基准/乐观/极超 |
|---|---:|---:|---:|---|---|
| MOR 金属氧化物 EUV resist | `$40-120M / $120-250M / $250-450M` | `$0.35-0.8B / $0.8-1.6B / $1.6-3.0B` | `$1.2-3.0B / $3.0-6.5B / $6.5-12B` | EUV critical layers 2026 3-8%，2027 10-25%，2028 25-50% | 60-75% / 65-80% / 70-85% |
| Dry resist/Aether stack | `$20-80M / $80-180M / $180-350M` | `$0.2-0.7B / $0.7-1.6B / $1.6-3.5B` | `$0.9-2.5B / $2.5-6B / $6-12B` | 先 DRAM/HBM，后 logic；2026 1-5%，2027 8-20%，2028 20-40% | 55-70% / 63-78% / 70-85% |
| High-NA EUV resist + underlayer + developer | `<$50M / $50-150M / $150-350M` | `$0.15-0.5B / $0.5-1.2B / $1.2-2.5B` | `$0.8-2.2B / $2.5-6B / $6-13B` | 2026 product wafer test，2027 selected HVM，2028 多客户扩散 | 60-75% / 68-82% / 75-88% |
| PFAS-free/fluorine-free ArFi/EUV materials | `$30-100M / $100-220M / $220-450M` | `$0.4-1.0B / $1.0-2.2B / $2.2-4.5B` | `$1.5-4B / $4-8B / $8-15B` | 2026 eval，2027 环保/废水成本驱动，2028 大客户 RFP 化 | 45-60% / 55-68% / 60-75% |
| BSPD 背面供电 CMP/etch/deposition 材料 | `$50-150M / $150-350M / $350-700M` | `$0.5-1.5B / $1.5-3.5B / $3.5-7B` | `$2-5B / $5-11B / $12-25B` | 2026 N2/A16/18A 初期，2027 AI/HPC 放量，2028 主流先进节点 | 50-65% / 58-72% / 65-80% |
| Mo/Ru/Co selective deposition 和新 barrier/liner | `$80-180M / $180-350M / $350-650M` | `$0.7-1.8B / $1.8-3.8B / $3.8-7B` | `$2.5-6B / $6-13B / $14-28B` | 2026 eval/selected layers，2027 量产层数增加，2028 扩散 | 45-62% / 55-70% / 62-78% |
| Hybrid bonding ultra-flat CMP/clean | `$150-350M / $350-650M / $650M-1.1B` | `$1.0-2.5B / $2.5-5.0B / $5.0-8.0B` | `$4-8B / $8-15B / $15-28B` | HBM/SoIC/C2W 2026 10-20%，2027 25-45%，2028 45-70% | 45-60% / 55-68% / 60-75% |
| Silicon photonics SOI/SiN wafer materials | `$100-250M / $250-500M / $500-900M` | `$0.8-1.8B / $1.8-3.5B / $3.5-6B` | `$2.5-5B / $5-10B / $10-20B` | CPO/optical I/O 2026 pilot，2027 premium switch/ASIC，2028 broader | 40-55% / 50-65% / 60-75% |
| EUV pellicle high-transmission membrane | `$50-150M / $150-300M / $300-600M` | `$0.5-1.2B / $1.2-2.5B / $2.5-5B` | `$1.5-3.5B / $3.5-8B / $8-16B` | 2026 Low-NA 高端层，2027 High-NA/DRAM，2028 多层化 | 50-65% / 60-75% / 65-82% |

**最值得关注的新产品排序：**

1. **MOR/dry resist。** 直接改善 EUV dose、stochastics 和 pattern collapse，且与设备/etch/deposition 共优化，定价能力强。
2. **High-NA EUV stack。** 2026 选型，2027-2028 收入。供应商一旦进入客户 process of record，替换很难。
3. **BSPD/GAA 前驱体与 CMP/清洗。** 2nm/A16/18A/1.4nm 的材料强度显著高于 3nm。
4. **Hybrid bonding CMP/clean。** HBM4、SoIC、3D logic 和 memory-close-to-logic 会把它从后道辅助变成前道良率核心。
5. **硅光 SOI/SiN 材料。** 1.6T/CPO/optical I/O 若提前，SOI 和高质量 SiN wafer/薄膜会比市场预期更快放量。

## 7. 供给侧：产能结构、瓶颈、成本与价格传导

### 7.1 产能结构

| 材料 | 主要产能地区 | 头部公司 | 主要工艺/产品 | 供给状态 |
|---|---|---|---|---|
| 300mm 硅片 | 日本、台湾/新加坡、韩国、德国、美国、中国 | Shin-Etsu Handotai、SUMCO、GlobalWafers、Siltronic、SK Siltron、Soitec、Wafer Works、Okmetic、NSIG、Eswin、Zhonghuan、Lion | CZ/FZ 拉晶、切片、研磨、抛光、退火、外延、SOI | 高端 300mm 偏紧，成熟/200mm 分化 |
| EUV/ArFi 光刻胶 | 日本、美国、韩国、台湾、中国部分 | TOK、JSR/Inpria、Shin-Etsu、Fujifilm、Sumitomo、DuPont/Qnity、Merck/AZ、Dongjin、Soulbrain、Nanda Opto、Kehua、Shanghai Sinyang | CAR、MOR、negative-tone、PFAS-free、underlayer/topcoat/developer | EUV/ArFi 高端高度集中，国产替代在中低端加速 |
| CMP slurry/pads | 美国、日本、韩国、中国、台湾 | Entegris/CMC、DuPont、Fujimi、Resonac、Fujifilm、Merck、AGC、JSR、Anji Micro、KC Tech、Soulbrain | Oxide/Cu/W/barrier/CeO2/silica slurry，polyurethane pads，post-CMP clean | 先进 CMP 配方和 pad stack 认证壁垒高 |
| 湿化学品/清洗 | 日本、美国、欧洲、韩国、中国、台湾 | Kanto Chemical、Stella Chemifa、Mitsubishi Chemical、BASF、Honeywell、Fujifilm、Entegris/KMG、Solvay、Merck、Technic、Soulbrain、Dongjin、Jianghua、Runma | H2SO4、H2O2、HF、HCl、NH4OH、TMAH、solvents、post-etch/post-CMP clean | 区域化强，高纯等级是壁垒 |
| 电子气体 | 美国、欧洲、日本、韩国、中国、台湾、中东氦源 | Linde、Air Liquide、Air Products、Nippon Sanso、SK Materials、Kanto Denka、Resonac、Merck/Versum、Wonik、Foosung、Jinhong、Huate、PERIC | Bulk N2/O2/Ar/H2/He，NF3、WF6、SiH4、NH3、ClF3、C4F6、rare gases | 长协和 on-site 绑定强，氦/稀有气体风险高 |
| ALD/CVD 前驱体 | 美国、德国、法国、日本、韩国、中国 | Merck/EMD、Air Liquide、Entegris、ADEKA、Tri Chemical、DNF、Hansol、UP Chemical/Soulbrain、Gelest/Mitsubishi、JSR/Yamanaka Hutech、SK Materials、Nata/Yoke | Hf/Zr/Si/Ti/Ta/W/Mo/Ru/Co 前驱体，low-k/high-k | GAA/DRAM/HBM4 使先进 precursor 偏紧 |
| PVD 靶材/电镀 | 日本、美国、欧洲、中国、韩国 | JX Advanced Metals、Mitsui Mining、Tosoh、Materion、Plansee、Honeywell、ULVAC、Konfoong/Jiangfeng、Grikin | Cu/Ta/Ti/W/Ru/Co/Mo targets，plating chemistries | 高纯金属和大尺寸 targets 认证慢 |
| Mask blanks/EUV pellicle | 日本、韩国、美国、欧洲 | HOYA、AGC、Shin-Etsu、S&S Tech、Mitsui Chemicals、Canatu、ASML ecosystem、FST、DNP、Toppan Photomasks、Photronics | EUV mask blank、quartz、absorber、pellicle membrane | EUV/High-NA 稀缺，良率和光学性能难度高 |

### 7.2 供给瓶颈

1. **300mm 高端硅片认证和缺陷密度。** 先进逻辑客户对 COP、金属杂质、flatness、edge roll-off、氧碳含量窗口极严，新增产能需要 12-24 个月客户认证。
2. **EUV 胶的 stochastics 和 dose trade-off。** 胶不是单独配方，必须与 EUV scanner、PEB、etch、underlayer、developer 共同优化；低 dose、低 LER、低 defect 之间互相拉扯。
3. **MOR/dry resist 的工艺集成。** 需要新型 deposition/development/etch 工艺，客户要重新建立 defect learning 和 process window。
4. **PFAS/含氟化学品替代。** ArFi/EUV 胶、topcoat、surfactant、清洗剂涉及环保、废水和工艺性能，替代不是简单换原料。
5. **稀有气体和氦。** TechInsights 指出半导体约消耗全球氦供应 21%；中东/卡塔尔扰动、运输和液氦低温物流都会影响成本。
6. **高纯前驱体原料和配体。** Hf/Zr/Ru/Mo/Co 等金属源、超高纯配体、低金属杂质合成和安瓿填充能力有限。
7. **CMP 配方和 pad stack 认证。** Hybrid bonding 和 BSPD 对纳米级平坦度、dishing、scratch、残留要求极高，不能用低端 slurry 替代。
8. **EUV mask blank/pellicle。** High transmission、热稳定、颗粒控制和 mask lifetime 决定 EUV yield。
9. **高纯过滤、容器和化学品物流。** 材料做到高纯还不够，运输、储存、bottle/valve/filter 的 extractables 和 particles 也会污染。
10. **客户共研人力。** 高端材料供应商的瓶颈常常是能驻厂调配方、做 failure analysis、快速响应 PDK 变更的工程师。
11. **中国出口管制和国产替代。** 海外高端材料对中国先进节点供应不确定，国内客户可能为供应安全接受较低良率材料，但先进工艺仍受制约。
12. **产能错配。** 200mm/成熟材料有库存，300mm/EUV/HBM 材料偏紧，表观行业产能利用率会掩盖真实瓶颈。

### 7.3 成本构成与毛利决定因素

| 材料 | 成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 硅片 | 半导体级多晶硅、拉晶能耗、切片损耗、抛光耗材、外延/退火设备折旧、检测、洁净包装 | 300mm 利用率、长期协议价格、良率、外延/SOI 占比、汇率和电力 | LTA 锁量锁价，短缺时高端 spec 加价；成熟规格受库存压价 |
| EUV/ArFi 胶 | 树脂、PAG/quencher、溶剂、添加剂、超纯过滤、洁净灌装、QC、客户工程 | 客户 POR、EUV dose 节省、defect 降低、批间一致性、供应安全 | 新节点定点后议价强，客户用材料溢价换 scanner throughput 和良率 |
| CMP | Abrasive particles、化学添加剂、pad 原料、conditioning disc、过滤、客户配方服务 | 平坦度、缺陷、dishing、throughput、pad life、post-CMP residue | 以工艺良率和 cost-of-ownership 定价，先进 layer 可溢价 |
| 湿化学品 | 基础化工原料、纯化、超净容器、废液/安全、物流 | ppb/ppt 纯度、local supply、客户认证、废水处理成本 | 低端随化工周期，高端按纯度和本地稳定供应加价 |
| 电子气体 | 空分/合成、稀有气体采购、纯化、钢瓶/管束/管道、on-site plant capex | 长协、on-site 绑定、纯度、供应安全、稀有气体成本 | 客户长期 take-or-pay，原料和能源部分传导 |
| ALD/CVD 前驱体 | 金属源、配体、有机合成、纯化、安瓿、hazmat、IP | 新材料 POR、沉积窗口、残碳/残氯、稳定性、设备兼容 | 高端 precursor 定价按 device performance 和良率，不按公斤成本 |
| 靶材/电镀 | 高纯金属、冶炼、热机械加工、bonding、检测 | 大尺寸均匀性、纯度、grain control、客户 tool matching | 稀缺金属可传导，先进 target 认证后价格粘性高 |
| Mask blank/pellicle | 超低缺陷基板、multilayer deposition、absorber、膜材料、检测 | EUV 反射率、缺陷、热稳定、寿命、透过率 | 与 mask 良率和 scanner uptime 绑定，高端产品议价强 |

## 8. 竞争格局与壁垒

### 8.1 市场结构

| 子领域 | 集中度 | 竞争格局 |
|---|---|---|
| 300mm 硅片 | 极高，前五大约 82-85% 的 300mm capacity/revenue | Shin-Etsu、SUMCO、GlobalWafers、Siltronic、SK Siltron 主导；中国厂商在成熟规格提升快，高端先进节点仍需追赶 |
| EUV/ArFi 光刻胶 | 极高，Top 6 约 80%+ | TOK、JSR/Inpria、Shin-Etsu、Fujifilm、Sumitomo、DuPont/Qnity、Merck、Dongjin；EUV 高端更集中 |
| CMP slurry/pads | 中高 | Entegris/CMC、DuPont、Fujimi、Resonac、Fujifilm、Merck、Anji Micro 等，按材料层分散但高端客户定点粘性强 |
| 电子气体 | 中高 | Bulk gas 由 Linde、Air Liquide、Air Products、Nippon Sanso 等长协/管道绑定；specialty gas 有 SK Materials、Kanto Denka、Merck、Wonik、Foosung、中国气体厂 |
| 湿化学品 | 中等，区域化 | 高纯技术集中在日本/欧美/韩国/台湾，中国在成熟规格增长快；物流半径和本地服务重要 |
| ALD/CVD 前驱体 | 中高，按元素和工艺分割 | Merck、Air Liquide、Entegris、ADEKA、DNF、Hansol、Tri Chemical、UP Chemical、Gelest 等各有细分优势 |
| Mask blank/EUV pellicle | 极高 | HOYA、AGC、Shin-Etsu、Mitsui/ASML ecosystem、Canatu、S&S Tech 等，EUV/High-NA 良率门槛高 |

### 8.2 可量化壁垒与“为什么能定价”

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| 纯度和颗粒 | 金属杂质 ppb/ppt，颗粒 nm 级，批间 Cpk | 一颗粒子可报废上万美元 wafer，客户愿付良率保险费 |
| 客户认证 | 12-36 个月 qualification，数百到数千片 wafer learning | 切换材料会重做良率曲线，机会成本远高于材料价差 |
| Process of Record | 进入 POR 后覆盖一个 node 2-4 年 | 节点量产期间客户不愿改配方，供应商可维持 ASP |
| Co-optimization | 材料与 scanner/etch/deposition/CMP tool 联调 | 材料不是 commodity，性能来自配方和设备 recipe 的组合 |
| 供应安全 | LTA、on-site gas plant、local production for local consumption | 缺货导致 fab idle，客户愿用长期合同换不断供 |
| IP 和数据 | 分子结构、合成路线、缺陷数据库、客户 wafers 数据 | 后发者不仅缺配方，也缺数年 defect learning |
| 资本与规模 | 300mm 硅片、EUV blank、on-site gas 需高 capex | 高固定成本行业在高利用率时经营杠杆和涨价弹性强 |
| 环保/安全许可 | 危化、PFAS、废水、氟气/氨气/金属有机物许可 | 可合规供应本身就是壁垒，尤其在美国/欧盟/日本/台湾 |

### 8.3 价值捕获判断

长期高 ROIC/高毛利最可能出现在：

1. **EUV/MOR/dry resist。** 小美元、大杠杆，客户愿为 EUV scanner throughput 和 defect 降低付费。
2. **先进 ALD/CVD 前驱体和 selective etch chemistries。** GAA/BSPD/Mo/Ru/Co 路线让材料成为性能工具，而非消耗品。
3. **Hybrid bonding CMP/clean。** 直接决定 HBM4/SoIC/3D bonding yield，材料价值占整机低但失效代价高。
4. **Mask blank/EUV pellicle。** 高端 EUV/High-NA 对缺陷和光学性能极敏感，供应商少。
5. **高端 300mm epi/SOI。** 比普通 polished wafer 更有规格壁垒和客户绑定，但 capex 重、周期性更强。

## 9. 2026 关键变化：最可能发生的 3 个拐点

1. **300mm 高端硅片和 200mm 成熟硅片彻底分化。** 2026 全行业不一定“硅片全面牛市”，但 AI/HBM/先进逻辑相关 300mm wafer 会继续改善，200mm/功率/工业库存出清慢。投资上看产品 mix 和客户，不看硅片总量。
2. **EUV 光刻胶从逻辑扩到 DRAM/HBM 收入主线。** TOK 已明确 HBM using its photoresists 量产，Samsung/SK hynix/SK EUV 订单和 HBM4 量产会提高 DRAM EUV layer intensity。2026 的主流仍是 Low-NA EUV CAR + underlayer，而 MOR/dry resist 开始抢 critical layers。
3. **材料公司从“化学品供应商”变成“节点共研伙伴”。** JSR/Inpria + Lam、Fujifilm PFAS-free ArFi、Qnity Eon EUV、Entegris advanced deposition/selective etch 增长，说明客户采购逻辑正在从单价转向 yield、throughput、环保和供应安全。

## 10. 2027 关键变化：最可能发生的 3 个拐点

1. **High-NA EUV 的材料 winner 开始显形。** 2026 product wafer test 和材料 stack eval 后，2027-2028 HVM 插入会锁定 MOR、dry resist、underlayer、developer、PEB/etch recipe 的 winners。
2. **HBM4/Rubin/MI400/Trainium3/TPU8 推动 DRAM 前道材料再次加速。** HBM4 不只是封装问题，也会增加先进 DRAM EUV、dry resist/MOR、CMP、前驱体和电子气体需求。
3. **GAA/BSPD/Mo-Ru-Co 材料从 R&D 进入可见收入。** 2026 N2/A16/18A 先导，2027 高端 AI/HPC 芯片进入更明确的 wafer starts，BSPD CMP/etch/deposition、Mo/Ru/Co precursor/target 和超净清洗会进入高增长。

## 11. 头部公司与可跟踪标的清单

### 11.1 硅片

| 细分 | 公司 |
|---|---|
| 全球 300mm prime/polished | Shin-Etsu Handotai、SUMCO、GlobalWafers、Siltronic、SK Siltron |
| 外延/退火/高端 300mm | Shin-Etsu、SUMCO、GlobalWafers、Siltronic、SK Siltron、Wafer Works、Okmetic、Ferrotec |
| SOI/硅光 | Soitec、GlobalWafers、Shin-Etsu、SUMCO、Okmetic、Wafer Works、Simgui |
| 中国 300mm 和国产替代 | NSIG/上海硅产业、上海新昇、Eswin 奕斯伟、中环领先、杭州立昂微、麦斯克、超硅半导体、Ferrotec 中国 |
| 关键观察 | 300mm 高端客户认证、epi/SOI 占比、LTA、台湾/韩国/美国本地化产能、中国高端良率 |

### 11.2 光刻胶和光刻辅助材料

| 细分 | 公司 |
|---|---|
| EUV/ArFi 高端光刻胶 | TOK、JSR/Inpria、Shin-Etsu Chemical、Fujifilm、Sumitomo Chemical、DuPont/Qnity、Merck/EMD AZ、Dongjin Semichem |
| MOR/新型 EUV | JSR/Inpria、TOK/Irresistible Materials、Lam Aether ecosystem、Fujifilm、Merck/Gelest、imec ecosystem、IBM/NY Creates research |
| ArF/KrF/i-line 中低端和国产替代 | Dongjin、Soulbrain、ENF Technology、Nanda Opto、Beijing Kehua、Shanghai Sinyang、Jingrui、Rongda、Xuzhou B&C、Red Avenue、Eternal Materials |
| Underlayer/BARC/topcoat/developer/cleans | Brewer Science、Nissan Chemical、JSR、TOK、DuPont/Qnity、Merck、Fujifilm、Shin-Etsu、Kanto Chemical、Dongjin、Soulbrain |
| 关键观察 | EUV POR share、HBM DRAM 使用层数、MOR dose/defect、PFAS-free 客户认证、台湾/韩国本地生产 |

### 11.3 CMP、湿化学品、清洗

| 细分 | 公司 |
|---|---|
| CMP slurry/pads | Entegris/CMC Materials、DuPont、Fujimi、Resonac、Fujifilm、Merck/Versum、AGC、JSR、3M、Anji Micro、KC Tech、Soulbrain |
| Post-CMP/etch clean | Fujifilm、Entegris、DuPont/Qnity、BASF、Merck、Kanto Chemical、Soulbrain、Dongjin、Technic、Anji Micro |
| 高纯湿化学品 | Kanto Chemical、Stella Chemifa、Mitsubishi Chemical、BASF、Honeywell、Solvay、Fujifilm、Entegris/KMG、Merck、Soulbrain、Dongjin、Jiangyin Jianghua、Runma、Crystal Clear、Kaisn |
| 关键观察 | Hybrid bonding CMP、BSPD CMP、post-CMP residue、CeO2/silica abrasive 供给、国产客户认证 |

### 11.4 电子气体和前驱体

| 细分 | 公司 |
|---|---|
| Bulk/onsite gas | Linde、Air Liquide、Air Products、Nippon Sanso/Taiyo Nippon Sanso、Messer、Iwatani、中国工业气体区域龙头 |
| Specialty gases | SK Materials、Kanto Denka、Resonac、Merck/Versum、Linde、Air Liquide、Air Products、Wonik Materials、Foosung、Jinhong Gas、Huate Gas、PERIC、Haohua |
| ALD/CVD precursors | Merck/EMD、Air Liquide、Entegris、ADEKA、Tri Chemical Laboratories、DNF、Hansol Chemical、UP Chemical/Soulbrain、Gelest/Mitsubishi Chemical、JSR/Yamanaka Hutech、SK Materials、Wonik、Nata Opto、Yoke |
| 关键观察 | Hf/Zr/Ru/Mo/Co precursor POR、氦/稀有气体价格、on-site gas backlog、advanced materials 亚洲增长 |

### 11.5 靶材、mask blank、pellicle、过滤/容器

| 细分 | 公司 |
|---|---|
| PVD targets/金属材料 | JX Advanced Metals、Mitsui Mining & Smelting、Tosoh、Materion、Plansee、Honeywell、ULVAC、Konfoong Materials/Jiangfeng、GRIKIN、有研新材 |
| Mask blanks/EUV masks | HOYA、AGC、Shin-Etsu、S&S Tech、DNP、Toppan Photomasks、Photronics |
| EUV pellicle | Mitsui Chemicals、ASML ecosystem、Canatu、FST、S&S Tech、Asahi Kasei related materials |
| 过滤/FOUP/容器 | Entegris、Pall/Danaher、Mott、Donaldson、Nippon Pillar、CKD、Miraial、Gudeng Precision、Chung King Enterprise |
| 关键观察 | EUV/High-NA blank 良率、pellicle transmission/thermal load、FOUP/chemical bottle contamination、advanced fab tool qualification |

## 12. 投资优先级

| 排名 | 子方向 | 2026-2027 吸引力 | 原因 |
|---:|---|---|---|
| 1 | EUV/MOR/dry resist | 极高 | AI/HBM/2nm/High-NA 共振，材料小但决定 scanner throughput 和良率 |
| 2 | ALD/CVD 前驱体、selective etch | 极高 | GAA/BSPD/Mo/Ru/Co 让材料成为节点性能核心 |
| 3 | Hybrid bonding CMP/clean | 极高 | HBM4、SoIC、3D bonding 直接拉动，认证和缺陷壁垒高 |
| 4 | 300mm 高端 epi/SOI | 高 | 硅片 oligopoly 强，但 capex 重、周期性仍在 |
| 5 | Specialty gases/onsite gas | 高 | 长协稳定、氦/稀有气体偏紧，但 bulk gas 毛利不如高端化学品 |
| 6 | 高纯湿化学品 | 中高 | 本地化和纯度升级确定，但部分品类价格竞争强 |
| 7 | 成熟 KrF/i-line 和普通硅片 | 中 | 中国国产化有量，但价格压力和壁垒低于先进材料 |

## 13. 风险

1. AI capex 突然放缓、GPU/HBM 订单取消或推迟，会先冲击高端 wafer starts 和材料备货。
2. HBM/CoWoS 或电力瓶颈若无法缓解，材料需求可能“订单强、实际消耗慢”。
3. High-NA EUV 插入晚于 2028，会推迟 MOR/dry resist 的大规模收入。
4. PFAS/环保监管可能导致配方切换失败、客户认证延迟或成本上升。
5. 中国国产化带来中低端价格竞争，高端材料也可能被政策性采购替代一部分。
6. 氦、稀有气体、金属有机前驱体原料受地缘冲突影响，短期毛利可能被成本吞噬。
7. 大客户集中度高，单一 foundry/IDM 的 POR share 变化会显著影响材料公司收入。

## 14. 参考资料

- [SEMI: Worldwide silicon wafer shipments increase 13% YoY in Q1 2026](https://www.semi.org/en/semi-press-release/semi-reports-worldwide-silicon-wafer-shipments-increase-13-percent-year-on-year-in-q1-2026)
- [SEMI: Building the Future, AI Investment, Equipment & Materials Market Outlook](https://www.semi.org/sites/semi.org/files/2025-09/5%20Clark%20Tseng_Building%20the%20Future-AI%20Investment%2C%20Equipment%20%26%20Materials%20Market%20Outlook.pdf)
- [Gartner: Worldwide semiconductor revenue to exceed $1.3T in 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026)
- [TSMC 2026 Q1 quarterly results](https://investor.tsmc.com/english/quarterly-results/2026/q1)
- [Samsung Electronics 1Q 2026 earnings presentation](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_1Q_conference_eng.pdf)
- [Siltronic 2026 guidance](https://www.siltronic.com/en/press/press-releases/siltronic-releases-its-guidance-for-financial-year-2026.html)
- [Siltronic Q1 2026 results](https://www.siltronic.com/en/press/press-releases/siltronic-closes-q1-2026-in-line-with-expectations.html)
- [GlobalWafers Q1 2026 results](https://www.sas-globalwafers.com/en/gwc_news_en_20260505/)
- [SUMCO management policy](https://www.sumcosi.com/english/ir/financial/managementpolicy.html)
- [TOK FY2025 Q&A summary](https://www.tok.co.jp/application/files/4017/7097/4316/q4_QA_Summary_en.pdf)
- [JSR/Inpria and Lam collaboration](https://www.jsr.co.jp/jsr_e/news/2025/20250916.html)
- [imec: EUV dose reduction via oxygen injection during MOR PEB](https://www.imec-int.com/en/press/imec-unlocks-lever-euv-dose-reduction-oxygen-injection-during-metal-oxide-resist-post)
- [Lam Research and IBM Aether dry resist collaboration](https://newsroom.lamresearch.com/ibm-lam-sub-1nm-logic-aether-dry-resist)
- [Lam Aether dry photoresist adopted by leading memory manufacturer](https://investor.lamresearch.com/2025-01-29-Breakthrough-EUV-Dry-Photoresist-Technology-from-Lam-Research-Adopted-by-Leading-Memory-Manufacturer?asPDF=1)
- [Fujifilm fluorine-free negative ArF immersion resist](https://www.fujifilm.com/de/en/news/hq/13549)
- [Fujifilm investment in Rapidus and semiconductor materials expansion](https://www.fujifilm.com/us/en/news/fujifilm-completes-investment-in-rapidus)
- [Qnity Eon EUV photoresist](https://www.qnityelectronics.com/news/qnity-expands-offerings-for-extreme-ultraviolet-lithography.html)
- [Entegris Q1 2026 results](https://investor.entegris.com/news/news-details/2026/Entegris-Reports-Results-for-First-Quarter-of-2026/default.aspx)
- [Air Liquide Q1 2026 activity presentation](https://www.airliquide.com/sites/airliquide.com/files/2026-04/air-liquide-presentation-q1-growth-performance-and-record-investments-air-liquide-continues-on-its-successful-trajectory-in-q1-2026.pdf)
- [TechInsights: Electronic gases market to reach $6.81B in 2026](https://www.techinsights.com/blog/electronic-gases-market-reach-681b-2026-driven-advanced-node-demand)
- [ASML Q1 2026 investor call transcript](https://ourbrand.asml.com/asset/8e1f7393-33dd-4737-a436-cfe1b68cc577/2026_04_15-ASML-Transcript-investor-call-Q1-2026.pdf)
- 本地项目底稿：[ai_chip_research_2026_2027.md](../ai_chip_research_2026_2027.md)

非投资建议。本报告用于产业链研究和情景推演；所有预测区间都应随 TSMC/Samsung/SK hynix/Micron/NVIDIA/AMD/Broadcom/AWS/Google/Microsoft/Meta 的 2026H2 订单、capex、HBM4 验证、High-NA 插入节奏和材料供应商财报持续更新。
# 行业调研：【晶圆厂洁净室与厂务系统】
> 截至日期：2026-05-08  
> 研究口径：本报告研究晶圆厂和先进封装厂的洁净室与厂务系统，覆盖洁净室 EPC/MEP、洁净室围护、MAU/AHU/FFU/HEPA/ULPA、AMC 控制、UPW/废水回用、工艺气体/化学品输送、PCW/冷水机组、真空/废气/尾气处理、FMCS/BMS/SCADA、tool hook-up、认证调试和运维服务。不包含光刻机、刻蚀机、沉积机等主工艺设备；高纯工艺材料只在其与厂务系统绑定时讨论。  
> 情景口径：对 2026-2027 年 AI 基础设施建设保持非常乐观。缺少直接披露的产品级市场规模时，使用 AI 芯片路线、HBM/CoWoS 产能、晶圆厂 capex、SEMI fab forecast、头部公司订单/扩产公告和工程交付瓶颈交叉推导。本文不是投资建议。

## 0. 一页结论

**最核心判断：2026 年晶圆厂洁净室与厂务系统不是传统“半导体土建后周期”，而是 AI 算力供给的隐性闸门。** GB300/B300、Trainium、TPU Ironwood、Maia、MTIA、华为 Ascend、寒武纪、AMD MI350 这些 2026 年主力 AI 芯片共同指向三类增量：先进逻辑晶圆、HBM DRAM 晶圆、CoWoS/SoIC/先进封装与测试。它们都必须先变成“可投片、可装机、可验收”的洁净空间、超纯水、气体化学品、废气处理和 FMCS 产能。

| 判断 | 基准 | 乐观 | 极度超预期乐观 |
|---|---:|---:|---:|
| 2026 全球晶圆厂洁净室与厂务系统广义订单池 | $55-75B | $75-105B | $105-145B |
| 2027 全球晶圆厂洁净室与厂务系统广义订单池 | $65-95B | $95-140B | $140-210B |
| 2026-2028 年 CAGR | 12-18% | 20-30% | 35%+ |
| 最强定价环节 | 高纯工艺系统、AMC/过滤耗材、UPW 回用、subfab 真空/尾气处理、FMCS/认证服务 | 同左，外加模块化预制厂务 skids | 所有能缩短 3-6 个月交付周期的供应商均有溢价 |
| 最弱环节 | 纯土建 EPC、低端彩钢板、通用风管、电缆桥架 | 仍有量，但毛利受总包压制 | 若项目争抢交付，低端环节也能短期涨价 |

关键事实锚点：

- SEMI 预计全球 300mm fab equipment spending 2026 年约 **$133B**、同比 **+18%**，2027 年约 **$151B**、同比 **+14%**；SEMI OEM 设备销售口径预计 2026 年总半导体制造设备销售约 **$145B**、2027 年约 **$156B**。设备支出只是主工艺设备口径，洁净室与厂务通常领先或伴随设备 6-24 个月下单。
- Gartner 预计 2026 年全球半导体收入 **$1.320T**、2027 年 **$1.555T**，AI 半导体约占 2026 年总收入 **30%**，hyperscaler AI 基建支出 2026 年增长 **50%+**。这是本报告乐观需求底座。
- TSMC 1Q26 收入 **$35.9B**、毛利率 **66.2%**，并把 2026 capex 指向 **$52-56B** 区间，HPC/AI 需求和先进封装紧缺是核心驱动。先进节点、CoWoS、N2/A16 和海外厂同步扩建，会持续拉动洁净室、厂务、UPW、气体和 subfab 系统。
- Micron FY26Q2 指出 HBM/AI 需求强劲，并称 2026 年供应会受到 wafer capacity 和 **cleanroom space** 约束；这是一手信号，说明洁净空间本身已经从“工程背景板”变成产出瓶颈。
- SK hynix、Samsung、Micron、TSMC、GlobalFoundries、Intel、SMIC/CXMT/YMTC、中国成熟制程厂共同扩产，且美国、欧洲、日本、东南亚的区域化建厂把同一份需求复制到更多地点，工程成本和交付难度明显高于台湾/韩国本土扩产。

我的结论排序：

1. **2026 最确定放量：洁净室 EPC/MEP、tool hook-up、UPW、气体化学品输送、真空/尾气处理、HVAC/FFU/过滤。** 这批产品已经是量产技术，需求来自 GB300/GB200/HBM3E/TPU/Trainium/MI350/国产替代的同步扩张。
2. **2026 最有利润弹性：高纯工艺系统、AMC 化学过滤、UPW 回用和 subfab abatement。** 它们占整厂 capex 比例不如主设备大，但认证、事故风险、良率损失和切换成本让客户对价格不敏感。
3. **2027 最大新斜率：HBM4/先进封装洁净室、N2/A16/GAA/背面供电厂务规格、模块化厂务 skids、AI 节能 FMCS。** 这些方向会把厂务从“工程采购”推向“良率、能耗、ESG、交期共同优化”的高壁垒系统。

## 1. 2026 AI 计算中心建设对晶圆厂洁净室与厂务系统的机会和挑战

### 1.1 需求传导链条

AI 数据中心本身不在晶圆厂里，但 AI 数据中心的 GPU/ASIC/HBM/先进封装订单会反向锁定上游晶圆厂与封测厂扩建。传导关系如下：

```text
AI 数据中心 CapEx 上修
-> GB300/B300、TPU、Trainium、Maia、MTIA、Ascend、MI350/MI400 等芯片订单
-> 先进逻辑 wafer、HBM wafer、CoWoS/SoIC/先进封装、测试 burn-in 扩产
-> 新建/扩建 fab、cleanroom、subfab、utility plant、UPW、gas/chemical、exhaust/abatement
-> 洁净室与厂务系统订单领先主设备 6-24 个月释放
```

项目内 `ai_chip_research_2026_2027.md` 给出的 2026-2027 年出货/价值权重最高的 AI 芯片平台，对洁净室与厂务的含义如下：

| AI 芯片/平台 | 2026 技术路径 | 对洁净室和厂务系统的直接拉动 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | TSMC 4NP + HBM3E + CoWoS-L/S，2026 主力 | TSMC 先进逻辑、CoWoS、HBM3E 供应链持续满载；高阶洁净室、UPW、气体、AMC、subfab 尾气处理、先进封装洁净厂房一起受益 |
| AWS Trainium2 | 定制 ASIC + HBM + 大规模 UltraServer，Rainier 主力 | 私有 ASIC 把 HBM/先进封装需求从 NVIDIA 外溢到云厂；厂务订单更分散但更长期 |
| Google TPU v7 Ironwood | Broadcom/Google XPU + HBM，推理优先 | TPU/ASIC 放量提高 Broadcom/TSMC/先进封装厂务需求，推理芯片也不再是低洁净度、低功耗故事 |
| NVIDIA B200/GB200 | Blackwell 存量继续交付 | 维持 2026 上半年 CoWoS/HBM3E/先进逻辑厂务利用率 |
| Huawei Ascend 910C/950 | 中国本土先进节点 + HBM/高带宽内存 + 超节点 | 中国洁净室集成、高纯系统、国产气体/化学品/UPW/尾气处理供应链订单弹性大 |
| Cambricon MLU 590/690 | SMIC 可得先进节点 + HBM/OAM | 量可能大，先进封装和测试洁净室、tool hook-up、国产高纯系统受益 |
| AMD MI350 | TSMC 先进节点 + HBM3E + 2.5D | 2026 AMD 最确定放量产品，补充 TSMC/HBM/先进封装厂务负荷 |
| AWS Trainium3 | 3nm + HBM3E 级内存，144 芯片 scale-up | 2026-2027 接棒 Trainium2，强化云厂 ASIC 自建产能池 |
| Meta MTIA 300/400/450/500 | Broadcom XPU，推理优先，两年多代迭代 | Meta/Broadcom >1GW 首期订单意味着 2027 ASIC 厂务不再是小批试产 |
| Microsoft Maia 200 | TSMC 3nm + HBM3E，Azure 推理 | 云厂自研芯片把高阶洁净室、液冷测试、HBM 和先进封装绑定 |
| 补充：Rubin/MI400/OpenAI-Broadcom XPU | HBM4 + 大尺寸 2.5D/3D 封装，2026H2 起量 | 2027 HBM4、CoWoS-L/SoIC、先进封装洁净室和 subfab 规格上移 |

### 1.2 目前正在使用的关键技术

| 技术/系统 | 2026 使用状态 | 为什么 AI 芯片会放大需求 |
|---|---|---|
| ISO 3-5 级核心洁净区 + mini-environment/FOUP | 300mm 先进制程主流 | N2/N3/A16、HBM base die、先进封装都需要稳定洁净度、温湿度和 AMC 控制 |
| MAU/AHU + FFU + HEPA/ULPA | 已成熟，能耗大 | 洁净室风量巨大，AI 晶圆扩产使低压损、高效率、可变风量方案有明确 ROI |
| AMC 控制和化学过滤 | 先进逻辑/光刻区关键 | GAA、EUV、先进封装材料更敏感，酸碱、有机物、硼/胺、硫化物都可能影响良率 |
| UPW + POU polishing + 废水回用 | 先进晶圆厂标配 | 单座 mega fab 用水量巨大，地方政府审批和 ESG 直接卡项目进度 |
| 高纯气体/化学品输送 | bulk gas、specialty gas、VMB/VMP、PFA/EP 管路 | HBM/先进逻辑扩产需要更多 NH3、H2、NF3、WF6、SiH4、Cl2、CMP/湿法化学品等 |
| subfab 真空、排风、scrubber、abatement | 所有前道 fabs 必需 | 高密度工艺设备带来 PFC、酸碱、有毒/可燃气体排放；法规和客户 ESG 要求提高 |
| PCW、冷水机组、热回收 | fabs 能耗大户 | EUV、刻蚀、沉积、HBM/先进封装设备热负载提高；稳定温度比单纯降温更重要 |
| FMCS/BMS/SCADA/洁净监测 | 大厂自建标准化平台 | 2026 后项目跨国家复制，数字化调试、远程运维和能耗优化成为交付条件 |
| tool hook-up 与认证调试 | 工程瓶颈 | 新 fab 真正放量取决于主设备 hook-up、leak check、particle/AMC qualification 和 process sign-off |

### 1.3 新技术成熟和放量时间：三情景

| 新技术/方向 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观成熟/放量 | 2026 最可能路径 |
|---|---|---|---|---|
| HBM/先进封装洁净室模块 | 2026 已放量，2027 明显加速 | 2026H2 随 HBM4/Rubin/MI400 提前锁单 | 2026Q4 即出现多地缺工程队、缺高纯系统 | **最确定主线之一**，先进封装不再是低规格后道 |
| N2/GAA/背面供电洁净与厂务规格 | 2026 以 TSMC/Intel/Rapidus/三星验证为主，2027 扩大 | 2027H1 多厂进入批量 tool install | 2026H2 为抢 AI 订单提前扩建 | 2026 收入来自土建/MEP/UPW/Gas 先行 |
| High-NA EUV 微振动、热稳定、AMC 升级 | 2026 试点，2027 进入更多先进逻辑项目 | 2026H2 与 N2/A16 扩产绑定 | 2027 前半形成独立高毛利改造包 | 2026 偏小批量高价值 |
| AI/传感器驱动的动态风量洁净室 | 2026 以 retrofit 和新 fab 局部区为主 | 2027 新建 fabs 渗透 15-30% | 客户因电力紧张，2026H2 就把节能 FMCS 作为标配 | 2026 会放量，但多数打包在 FMCS/HVAC 中 |
| 低压损 ULPA + 高寿命 AMC 滤材 | 2026 已量产并涨价 | 2026 全年因 FFU 能耗和 AMC 敏感性加速 | 供应商凭认证型号短期 10-20% 溢价 | 2026 高确定性，耗材属性好 |
| 模块化预制 utility skids | 2026 在美国/欧洲/日本加速 | 2027 成为区域化建厂交付主流 | 2026H2 工程队短缺导致预制化渗透跳升 | 2026 最受海外建厂拉动 |
| 高 DRE PFC/PFAS/有害气体 abatement | 2026 新 fab 标配升级 | 2027 法规和客户 ESG 共同推高单机价值 | 2026 即出现紧缺与服务合同涨价 | 2026 确定放量，2027 利润更好 |
| UPW/废水选择性回收、ZLD、资源化 | 2026 水紧张地区率先采用 | 2027 台湾/美国/中国新项目渗透上行 | 若审批以水回用率为条件，2026H2 提前导入 | 2026 以改造和新厂核心包为主 |

## 2. 已经开始放量的关键产品：市场规模、渗透率、利润率

口径说明：下面的市场规模是全球订单/收入池估算，时间窗口从 2026-05-08 起算：未来 3 个月约为 2026-05 至 2026-08，未来 1 年为 2026-05 至 2027-05，未来 2 年为 2026-05 至 2028-05。各细分之间存在总包、分包和设备材料重复，不可简单相加。

| 已放量产品/系统 | 当前状态 | 未来 3 个月市场规模：基准/乐观/极度乐观 | 未来 1 年市场规模：基准/乐观/极度乐观 | 未来 2 年市场规模：基准/乐观/极度乐观 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| 洁净室 EPC/MEP、tool hook-up | 新建 fabs 与扩建项目最先下单，交付周期 12-36 个月 | $7-10B / $10-15B / $15-22B | $28-42B / $42-62B / $62-90B | $55-85B / $85-130B / $130-200B | 新建/扩建 fab 接近 100%；海外项目预制化和本地总包渗透上行 | 总包毛利 6-14%，专业分包 12-25%；极缺交付时高端 hook-up 可到 25-35% |
| 洁净室围护：墙板、顶棚、架空地板、密封门窗 | 成熟放量，随洁净面积增长 | $1.8-2.8B / $2.6-4.0B / $4.0-6.0B | $8-12B / $12-18B / $18-28B | $15-24B / $24-38B / $38-60B | 300mm 与先进封装厂 100%；高承载/低释气材料占比提高 | 普通产品 15-25%；高规格材料/认证供应 25-40% |
| HVAC、MAU/AHU、FFU、HEPA/ULPA | 已成熟，fabs 能耗核心 | $2.5-4.0B / $3.8-6.0B / $6.0-9.0B | $10-16B / $16-25B / $25-38B | $20-34B / $34-55B / $55-85B | FFU/ULPA 在洁净区高渗透；EC motor、变风量、低压损滤材从 30-45% 提升到 55-75% | 设备 20-35%；滤材耗材 30-45%；低压损/AMC 认证型号 45%+ |
| AMC 化学过滤和实时污染监测 | EUV、GAA、先进封装敏感区已必配 | $0.5-0.9B / $0.8-1.4B / $1.4-2.2B | $2.5-4.0B / $4.0-6.5B / $6.5-10B | $5-8B / $8-14B / $14-24B | 先进逻辑/存储核心区 70-90%；先进封装从 20-35% 升至 45-65% | 滤材 35-55%；监测仪器 45-65%；服务合同 25-40% |
| UPW、POU polishing、废水回用 | 水资源和审批刚需 | $2.5-4.0B / $4.0-6.5B / $6.5-10B | $12-20B / $20-32B / $32-48B | $25-42B / $42-70B / $70-115B | 新建先进 fab 100%；高回用率方案从 35-50% 升至 60-80% | EPC 10-20%；膜/树脂/仪表 30-55%；运维耗材 25-45% |
| 高纯气体/化学品输送、VMB/VMP、UHP 管阀件 | HBM、先进逻辑、湿法工艺共同拉动 | $2.0-3.5B / $3.5-5.5B / $5.5-8.5B | $9-16B / $16-26B / $26-40B | $18-32B / $32-55B / $55-90B | 新 fab 100%；国产替代在中国成熟制程和部分先进项目持续提升 | 系统集成 18-35%；UHP 阀件/仪表 35-60%；认证紧缺品可 60%+ |
| 真空、排风、scrubber、POU abatement | subfab 标配，ESG 推高规格 | $1.5-2.8B / $2.8-4.5B / $4.5-7.0B | $7-13B / $13-22B / $22-35B | $15-28B / $28-50B / $50-85B | 先进 fab 100%；高 DRE、低能耗、服务绑定渗透加速 | 主机 30-50%；服务/备件 35-55%；POU 特种 abatement 可 45-60% |
| PCW、冷水机组、热交换、热回收 | 与 EUV/刻蚀/沉积/先进封装热负载同步 | $1.2-2.2B / $2.2-3.8B / $3.8-6.0B | $5-10B / $10-18B / $18-30B | $12-24B / $24-45B / $45-75B | 新 fab 100%；热回收和高效机组从 20-35% 升至 45-60% | 标准机组 15-30%；高效控制/热回收 25-45% |
| FMCS/BMS/SCADA、洁净监测、数字化调试 | 大厂标准化，海外复制更需要 | $0.6-1.2B / $1.2-2.0B / $2.0-3.2B | $3-6B / $6-10B / $10-16B | $7-14B / $14-26B / $26-45B | 新 fab 基础监控 100%；AI 节能优化从 10-20% 提升至 35-55% | 软件/算法 50-80%；系统集成 20-35%；长期服务 30-50% |
| 运维服务、过滤耗材、树脂、备件、认证复测 | 随 installed base 增长，收入更平滑 | $2.0-3.5B / $3.5-5.5B / $5.5-8.0B | $9-15B / $15-24B / $24-36B | $20-36B / $36-60B / $60-95B | installed base 越大越稳；先进 fab 耗材单价更高 | 20-45%；高认证耗材和应急服务可 45%+ |

已放量产品增长判断：

| 产品/系统 | 基准增长 | 乐观增长 | 极度超预期乐观增长 | 主要驱动 |
|---|---:|---:|---:|---|
| 洁净室 EPC/MEP/tool hook-up | 未来 12 个月 +15-25% | +30-45% | +55-80% | SEMI fab capex 上行、海外建厂、HBM/CoWoS 扩产 |
| HVAC/FFU/ULPA/AMC | +15-30% | +35-55% | +60-90% | 洁净面积、能耗约束、AMC 敏感性上升 |
| UPW/废水回用 | +20-35% | +40-65% | +70-110% | 新 fab 用水审批、台湾/美国/中国多地水风险 |
| 高纯气体/化学品系统 | +20-35% | +40-65% | +70-100% | HBM/先进逻辑工艺步骤多，国产替代和海外扩建共振 |
| 真空/尾气处理 | +18-30% | +35-60% | +65-100% | PFC/有害气体治理、subfab 服务、ESG 和法规 |
| FMCS/数字调试 | +25-45% | +50-80% | +90-140% | 多地复制、节能 ROI、工程师短缺推动自动化 |

## 3. 在研和即将快速增长的关键产品与细分技术

| 在研/早期产品 | 2026 阶段 | 未来 3 个月市场规模：基准/乐观/极度乐观 | 未来 1 年市场规模：基准/乐观/极度乐观 | 未来 2 年市场规模：基准/乐观/极度乐观 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| HBM4/先进封装专用洁净室和 subfab 套包 | 2026H2 起随 Rubin/MI400/TPU8 early ramp 加速 | $1.0-2.0B / $2.0-3.5B / $3.5-6.0B | $6-12B / $12-22B / $22-35B | $18-35B / $35-65B / $65-110B | 先进封装厂高规格洁净室从 2026 的 30-45% 升至 2027 的 55-75% | 20-40%；高端 hook-up/验证服务可 40%+ |
| 动态风量、AI FMCS、洁净室能耗优化 | retrofit + 新厂局部导入 | $0.3-0.8B / $0.8-1.5B / $1.5-2.5B | $1.5-3.5B / $3.5-7B / $7-12B | $5-10B / $10-20B / $20-35B | 新建先进 fab 渗透 2026 10-20%，2027 25-45%，2028 45-65% | 软件 60-85%；系统集成 25-40%；节能分成模式 ROIC 高 |
| 模块化预制 utility skids | 海外建厂、工人短缺推动 | $0.8-1.8B / $1.8-3.0B / $3.0-5.0B | $5-10B / $10-18B / $18-28B | $14-28B / $28-55B / $55-90B | 美国/欧洲/日本项目渗透从 20-35% 升至 45-65% | 20-35%；若能缩短工期，项目溢价 10-20% |
| 高 DRE、低能耗 PFC/PFAS/有毒气体 abatement | 新 fab 标配升级，法规驱动 | $0.4-1.0B / $1.0-1.8B / $1.8-3.0B | $2-5B / $5-9B / $9-15B | $7-15B / $15-30B / $30-55B | 先进 fab 2026 40-60%，2027 60-80%，高 ESG 客户 90%+ | 主机 35-55%；耗材服务 40-60%；认证后粘性强 |
| UPW 选择性回收、ZLD、铜/氟/氨资源化 | 水紧张地区先导入 | $0.3-0.8B / $0.8-1.4B / $1.4-2.5B | $2-4B / $4-8B / $8-14B | $6-14B / $14-30B / $30-55B | 新建 fab 高回用方案 2026 35-50%，2027 55-75% | 膜/树脂/仪表 35-55%；工程 12-25%；服务耗材 25-45% |
| High-NA EUV/GAA/背面供电微环境与微振动控制 | 2026 先进节点项目验证 | $0.4-1.0B / $1.0-2.0B / $2.0-3.5B | $3-6B / $6-12B / $12-20B | $8-18B / $18-38B / $38-70B | 只覆盖先进逻辑核心区，但单平方米价值极高 | 25-45%；特殊传感器/控制软件 50%+ |
| 实时 AMC、粒子、金属离子、UPW TOC/silica 传感网络 | 传感器加密与数据闭环 | $0.2-0.6B / $0.6-1.0B / $1.0-1.8B | $1-3B / $3-6B / $6-10B | $4-8B / $8-16B / $16-28B | 从关键区采样走向全厂数字孪生，2027 加速 | 仪器 45-65%；软件/数据服务 60-85% |
| 低压损 ULPA、可再生 AMC 滤材、长寿命 FFU | 已有产品，2026 加速升级 | $0.5-1.0B / $1.0-1.8B / $1.8-3.0B | $2.5-5B / $5-9B / $9-15B | $7-14B / $14-26B / $26-45B | 新建先进 fab 渗透 2026 30-45%，2027 50-70% | 35-55%；认证耗材可 55%+ |
| 氢气/EUV/特气安全联锁、泄漏检测与防爆排风 | EUV/H2 与高危特气使用增加 | $0.2-0.5B / $0.5-0.9B / $0.9-1.5B | $1-2.5B / $2.5-5B / $5-8B | $3-7B / $7-15B / $15-25B | 先进逻辑和存储厂 2026 50%+，2027 更接近标配 | 30-50%；安全认证供应商议价强 |

最值得押注的在研方向：

1. **HBM4/先进封装洁净室套包。** 先进封装洁净室的洁净、湿度、翘曲、应力、AMC、subfab 需求向前道靠拢，2027 会成为单独大市场。
2. **AI FMCS + 动态风量。** 洁净室 HVAC 是 fabs 最大能耗来源之一，节能 5-15% 对 mega fab 是千万美元级年化收益；软件和控制系统长期 ROIC 高。
3. **高 DRE abatement 与 UPW 回用。** 法规和水资源审批会把“可持续厂务”从 ESG 口号变成开工条件。
4. **模块化预制。** 美国/欧洲/日本工程队短缺，预制化的价值不只是降成本，而是锁交期。
5. **实时污染监测网络。** 先进节点良率对 AMC 和金属离子更敏感，传感器 + 数据闭环会从关键工段扩展到全厂。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 地区 | 主要需求方 | 主要供应链/公司 | 供给特点 |
|---|---|---|---|
| 台湾 | TSMC N3/N2/A16、CoWoS、OSAT | 汉唐/L&K、亚翔/Acter、洋基/UIS、帆宣/Marketech、汉科/Wholetech、CTCI、日系/美系设备材料 | 最成熟的先进 fab 洁净室与厂务工程集群，速度和经验强，客户集中度高 |
| 韩国 | Samsung、SK hynix HBM/DRAM/foundry | Samsung E&A、SK ecoplant、Hyundai Engineering、Wonik、GST、CSK、DAS、local gas/chemical firms | HBM cleanroom 和 subfab 需求强，DRAM/HBM 工程经验深 |
| 美国 | TSMC Arizona、Micron Idaho/New York、Intel、Samsung Taylor、GF | Exyte、Jacobs、Fluor、Bechtel、DPR、Burns & McDonnell、McCarthy、local union contractors | 需求大但人工、许可、供应链和工期风险最高；预制化和项目管理溢价高 |
| 欧洲 | Intel/GF/ESMC/Rapidus 相关供应链、Bosch/ST/Infineon | Exyte、Jacobs、Mercury Engineering、M+W legacy、local EPC | 工程标准高、能源/环保约束强，补贴驱动但审批周期长 |
| 日本 | TSMC Kumamoto、Rapidus、Kioxia、Micron Japan | Taikisha、Shinryo、Takasago Thermal、Obayashi、Kajima、Shimizu、Takenaka | 洁净室/空调/厂务技术强，先进逻辑复兴和材料设备本土化带来增量 |
| 中国大陆 | SMIC、CXMT、YMTC、华虹、长鑫、士兰、众多成熟制程项目 | 亚翔集成、圣晖集成、柏诚股份、正帆科技、至纯科技、新莱应材、广钢气体、金宏气体、中巨芯等 | 国产替代、成熟制程、存储和本土 AI 芯片推动订单；价格竞争更强但量大 |
| 东南亚 | Micron Singapore、GlobalFoundries、UMC/Vanguard、OSAT | Exyte、Jacobs、local EPC、日台工程商、气体水处理供应链 | 后道、存储和成熟制程扩产多，成本与地缘分散优势明显 |

### 4.2 至少 10 条供给瓶颈

1. **洁净室设计和项目经理。** 先进 fab 厂务工程经验难复制，海外项目尤其缺懂半导体标准的 PM、QA/QC 和 commissioning 团队。
2. **UHP 管路焊接和安装工人。** 高纯气体、化学品、UPW 的 orbital welding、electropolished stainless、PFA 管路安装需要认证工人，不能临时用普通机电队替代。
3. **FFU/ULPA/AMC 滤材交期。** 先进节点需要低释气、低压损、可追溯滤材，认证型号少，换供应商要重新验证。
4. **高纯阀件、调压器、质量流量、VMB/VMP。** 这些小部件一旦缺货会阻塞 tool hook-up，且洁净度、安全、泄漏风险让客户不敢随意换料。
5. **UPW 树脂、膜、TOC/硅/金属离子监测仪。** 水质不达标会直接影响良率，水回用率又关系到地方审批。
6. **真空泵、scrubber、POU abatement 服务能力。** 主机只是开始，备件、预防性维护、DRE 验证和 EHS 文档决定长期可用率。
7. **subfab 空间和排风能力。** 先进工艺设备增加后，subfab 设备密度、热负载和有害气体排放常常比 cleanroom 上层更先卡住。
8. **电力、冷水、PCW 和热回收系统。** fab 不是数据中心，但同样受电力接入、冷源、冷却塔、水权和噪音许可约束。
9. **认证和客户标准。** ISO 14644 洁净等级只是底线，真正难的是台积电/三星/英特尔/美光/设备商自己的 particle、AMC、振动、压差、EHS 规格。
10. **工程现金流和履约担保。** 大型洁净室项目金额高、周期长、变更多，工程公司需要强资产负债表才能承接多项目并行。
11. **地缘和本地化。** 美国 CHIPS、欧洲补贴、日本半导体复兴、中国国产替代都要求本地施工、材料审查和供应链合规。
12. **调试窗口。** 主设备到厂后，hook-up、leak check、particle clean-up、UPW/gas qualification、FMCS 联调和 process sign-off 会把产能释放拉长。

### 4.3 成本构成与毛利决定因素

典型 300mm 新建/扩建 fab 的洁净室与厂务系统成本拆分，按不含主工艺设备的 facility/cleanroom package 估算：

| 成本项 | 占比区间 | 毛利/议价因素 |
|---|---:|---|
| 洁净室围护、架空地板、顶棚、结构适配 | 8-15% | 材料认证、抗静电、低释气、结构承载和工期 |
| HVAC、MAU/AHU、FFU、HEPA/ULPA/AMC | 18-28% | 能耗、低压损、AMC 过滤效率、滤材寿命 |
| UPW、废水回用、化学品处理 | 12-22% | 水质、回用率、地方审批、耗材锁定 |
| 高纯气体/化学品输送 | 12-22% | UHP 阀件、泄漏安全、焊接质量、客户认证 |
| 真空、排风、scrubber、abatement | 8-16% | DRE、EHS、服务网络、备件 |
| PCW、冷源、热交换、热回收 | 6-12% | 能效、稳定温度、冗余和热回收 ROI |
| 电气、仪控、FMCS/BMS/SCADA | 8-15% | 数据闭环、可靠性、网络安全、复制能力 |
| 工程管理、调试、验证、施工人工 | 12-25% | 交期、工人短缺、变更管理、客户验收 |

价格传导机制：

- **交期溢价。** 主设备、HBM 和 AI 芯片订单已经锁定时，洁净室晚 3 个月会冻结更高价值的 wafer/output，客户会为工期确定性付费。
- **良率溢价。** 粒子、AMC、金属离子、UPW、气体泄漏造成的损失远高于滤材、阀件、传感器价格，认证供应商可涨价。
- **安全/EHS 溢价。** 特气、PFC、PFAS、酸碱废气处理一旦事故停线，损失不可接受，客户倾向买成熟方案。
- **切换成本。** 一套 VMB、UPW、AMC 或 FMCS 方案通过客户认证后，替换通常要重新做材料兼容、泄漏、安全和 process qualification。
- **服务锁定。** 真空/尾气处理、UPW 树脂、滤材、传感器校准和 FMCS 维护具备耗材/服务复购属性，长期毛利好于一次性总包。

## 5. 竞争格局与壁垒

### 5.1 市场结构和头部集中度

| 细分层 | 集中度判断 | 代表公司 | 定价权 |
|---|---|---|---|
| 全球半导体洁净室总包/EPC | 项目制，头部在先进 fabs 份额高，但区域差异大 | Exyte、Jacobs、Fluor、Bechtel、DPR、CTCI、Taikisha、Shinryo、Takasago、Samsung E&A、SK ecoplant | 中等到强，取决于客户历史和工期 |
| 台湾先进 fab 厂务工程 | 高集中，TSMC 供应链经验壁垒强 | 汉唐/L&K、亚翔/Acter、洋基/UIS、帆宣/Marketech、汉科/Wholetech | 强，尤其 tool hook-up、高纯系统和长期客户关系 |
| 中国大陆洁净室集成 | 分散但头部快速集中 | 亚翔集成、圣晖集成、柏诚股份、正帆科技、至纯科技 | 中等，先进客户认证后较强，成熟制程价格竞争更强 |
| AMC/HEPA/ULPA/滤材 | 认证型号集中 | Camfil、AAF/Daikin、MANN+HUMMEL、Donaldson、Nippon Muki、Pall、Entegris、MayAir、苏净等 | 强，耗材属性和认证锁定 |
| UPW/水处理 | 工程商分散，关键材料设备集中 | Veolia、Ovivo、Kurita、Organo、Ecolab/Nalco、DuPont、Toray、Pall、Entegris、正帆/至纯等 | 中强，材料耗材和 O&M 好于工程 |
| 高纯气体/化学品系统 | 认证壁垒高，区域供应链强 | Air Liquide、Linde、Air Products、Merck、Entegris、Swagelok、VAT、新莱应材、正帆科技、至纯科技 | 强，小件卡交付，认证后粘性高 |
| 真空/尾气处理 | 头部集中、服务网络重要 | Edwards/Atlas Copco、Ebara、Busch、Pfeiffer、DAS、CS Clean、GST、CSK、Kanken Techno | 强，主机 + 服务 + EHS 锁定 |
| FMCS/BMS/自动化 | 平台和客户标准粘性强 | Siemens、Schneider Electric、Honeywell、Johnson Controls、Yokogawa、Emerson、Rockwell、ABB、本地系统集成商 | 强，软件和长期维护毛利高 |

### 5.2 壁垒清单：为什么能定价

1. **技术壁垒：污染控制不是“更干净一点”而是良率函数。** 粒子、AMC、UPW TOC、金属离子、微振动、温湿度波动都会影响先进节点和 HBM/先进封装良率，客户愿意为确定性付费。
2. **规模壁垒：mega fab 同时管理数千个系统接口。** 总包需要整合土建、洁净室、subfab、utility plant、FMCS、EHS、tool hook-up 和设备商要求，小公司很难独立承接。
3. **渠道/客户锁定：头部 fab 会复用合格供应商。** 台积电、三星、美光、SK hynix、Intel、SMIC 等客户一旦形成标准库，后续项目倾向复制。
4. **认证标准：ISO/SEMI 只是入门，客户私有规范更难。** 供应商要通过材料、泄漏、粒子、AMC、安全、软件权限和追溯体系验证。
5. **切换成本：换供应商会引入停线和重新验证。** 对 UPW、气体、真空、过滤、FMCS 这类系统，价格节省远小于停产风险。
6. **交付壁垒：工期就是客户的 AI 芯片上市窗口。** 2026-2027 客户买的不只是设备，而是“确定在某个季度通过验收”。
7. **服务壁垒：installed base 会转化为耗材和备件。** 滤材、树脂、真空泵保养、scrubber 维护、传感器校准和 FMCS 升级使收入可持续。

### 5.3 哪一层最可能长期高 ROIC/高毛利

长期价值捕获排序：

| 排名 | 环节 | 原因 |
|---:|---|---|
| 1 | FMCS/污染监测软件、传感器、数据服务 | 软件毛利高，客户切换成本高，节能和良率 ROI 可量化 |
| 2 | AMC/ULPA 滤材、UPW 膜/树脂、关键耗材 | 认证后复购，单位价值不大但停线风险高 |
| 3 | UHP 阀件、管件、气体化学品安全系统 | 小部件卡大项目，洁净和安全认证壁垒高 |
| 4 | 真空/尾气处理主机 + 服务 | 设备 + 备件 + EHS 文档 + 现场服务，生命周期收入好 |
| 5 | 高端 UPW/废水回用和资源化 | 水审批和 ESG 提高定价，材料耗材和运维可持续 |
| 6 | 专业洁净室 tool hook-up 与验证服务 | 工程人力密集但交付窗口有溢价，海外建厂尤其强 |
| 7 | 纯 EPC/土建总包 | 订单大但毛利和现金流压力大，除非具备半导体专门 know-how 和长期客户 |

## 6. 2026 关键变化：行业拐点与最可能放量的子方向

### 拐点 1：洁净室空间本身成为 HBM 和 AI 芯片产能约束

Micron 已经把 cleanroom space 与 wafer capacity 并列为供应限制，TrendForce 也持续跟踪 Samsung/SK hynix/Micron 的 HBM cleanroom race。2026 年 HBM3E 仍是主力，HBM4 从 Rubin/MI400/TPU8/ASIC 进入早期导入，这意味着 HBM cleanroom、TSV/stacking、测试和先进封装厂务会一起紧。

最可能放量：HBM/DRAM 洁净室扩建、先进封装洁净室、UPW、气体、tool hook-up、测试区 HVAC/洁净厂务。

### 拐点 2：美国/日本/欧洲区域化建厂从公告进入工程消化期

TSMC Arizona、Micron Idaho/New York、Samsung Taylor、Intel、GlobalFoundries Dresden/美国、Rapidus、JASM 等项目把原本集中在台韩的工程需求复制到高成本地区。海外 fabs 的洁净室单位成本和工期风险高于台湾/韩国本土扩建，模块化预制、数字化调试和有经验工程队价值提升。

最可能放量：预制 utility skids、半导体专业 EPC、FMCS、UHP 管路安装、当地服务团队。

### 拐点 3：厂务系统从“合规成本”变成“开工许可和客户 ESG 条件”

水、电、PFC、PFAS、特气安全和能耗管理都直接影响 fab 许可和客户 ESG 审查。2026 新建 fab 不再只看洁净度，还看用水回收率、尾气破坏去除效率、能耗优化、碳排数据和可审计性。

最可能放量：UPW/废水回用、PFC/PFAS abatement、AMC/污染监测、能耗优化 FMCS、热回收。

## 7. 2027 关键变化：行业拐点与最可能放量的子方向

### 拐点 1：HBM4、Rubin/MI400/TPU8/OpenAI-Broadcom ASIC 把先进封装厂务推成主战场

2026 是 HBM4 验证和早期放量，2027 才是多平台并行消化。先进封装和测试厂房会更接近前道 fabs：更严格洁净度、更高温湿度稳定、更复杂化学品/气体、更多测试 burn-in 和更高 subfab 负载。

最可能放量：CoWoS/SoIC/2.5D/3D 相关洁净室、HBM4 测试区、液冷测试厂务、高洁净封装材料环境控制。

### 拐点 2：N2/A16/GAA/背面供电和 High-NA EUV 提高微环境门槛

先进逻辑进入 GAA、背面供电和更复杂 EUV patterning 后，微振动、热稳定、AMC、粒子和 UPW/化学品一致性会进一步上移。洁净室系统从“洁净等级”竞争转向“全厂稳定性和 process window”竞争。

最可能放量：微振动控制、EUV/H2 安全排风、高等级 AMC、实时分子污染监测、温湿度精密控制。

### 拐点 3：节能厂务和数字化运维成为利润池

2027 若 AI 芯片产能继续被预定，fab 业主会更愿意为节能、稳定和快速复制付费。洁净室 HVAC 的能耗足够大，5-15% 的节能足以支撑软件、传感器和控制改造。工程师短缺会推动自动 commissioning、远程运维和异常预测。

最可能放量：AI FMCS、动态风量控制、digital twin commissioning、预测性维护、过滤/UPW/真空服务合同。

## 8. 头部公司和细分公司清单

### 8.1 洁净室 EPC、MEP、tool hook-up、总包

| 区域 | 公司 |
|---|---|
| 全球/欧美 | Exyte、Jacobs、Fluor、Bechtel、DPR Construction、Burns & McDonnell、McCarthy、Mercury Engineering、M+W legacy teams、Worley、HDR |
| 日本 | Taikisha、Shinryo、Takasago Thermal Engineering、Obayashi、Kajima、Shimizu、Takenaka、Taisei、Kyudenko、JGC |
| 韩国 | Samsung E&A、SK ecoplant、Hyundai Engineering、Wonik、SFA Engineering、local cleanroom/subfab specialists |
| 台湾 | L&K Engineering/汉唐、Acter/亚翔、United Integrated Services/洋基、Marketech/帆宣、Wholetech/汉科、CTCI、中鼎、Kedge、NOVA |
| 中国大陆 | 亚翔集成、圣晖集成、柏诚股份、正帆科技、至纯科技、中国电子系统、中建系机电、上海建工、太极实业/十一科技、盛剑环境、仕净科技 |

### 8.2 HVAC、FFU、HEPA/ULPA、AMC

Camfil、AAF/Daikin、MANN+HUMMEL、Donaldson、Parker、Freudenberg、Nippon Muki、Nippon Air Filter、Pall、Entegris、MayAir、苏净安泰、金海高科、Airtech Japan、Yamato、Taikisha、Shinryo、Takasago、Johnson Controls、Trane、Carrier、Daikin Applied。

### 8.3 UPW、废水回用、化学品处理

Veolia、Ovivo、Kurita、Organo、Ecolab/Nalco、DuPont Water、Toray、Asahi Kasei、Pall、Entegris、Gradiant、Aquatech、Evoqua/Xylem、正帆科技、至纯科技、沃顿科技、碧水源、景津装备、盛剑环境、仕净科技。

### 8.4 高纯气体、化学品输送、UHP 管阀件

Air Liquide、Linde、Air Products、Taiyo Nippon Sanso、Merck、Entegris、Swagelok、Parker、VAT、MKS Instruments、CKD、Fujikin、SMC、KITZ SCT、Ham-Let、AP Tech、Rotarex、新莱应材、正帆科技、至纯科技、富瑞特装、金宏气体、广钢气体、华特气体、昊华科技、中巨芯、雅克科技。

### 8.5 真空、排风、scrubber、尾气处理

Edwards/Atlas Copco、Ebara、Busch、Pfeiffer Vacuum、Leybold、Kanken Techno、DAS Environmental Expert、CS Clean Solutions、GST、CSK、Global Standard Technology、Unisem、Centrotherm、MKS、盛剑环境、仕净科技、华海清科相关配套、正帆科技。

### 8.6 FMCS/BMS/SCADA、传感、自动化

Siemens、Schneider Electric、Honeywell、Johnson Controls、Yokogawa、Emerson、Rockwell Automation、ABB、Azbil、E+H、Mettler Toledo、Particle Measuring Systems、Lighthouse Worldwide、PMS/Hach、Horiba、Thermo Fisher、Picarro、MKS、INFICON、本地自动化系统集成商。

### 8.7 先进封装/HBM 洁净厂务相关

TSMC、ASE、Amkor、JCET、Powertech、Samsung、SK hynix、Micron、Intel Foundry、SPIL、Tongfu Micro、Huatian、King Yuan Electronics，以及对应洁净室/高纯系统供应商：Exyte、L&K、Acter、UIS、Marketech、Taikisha、Shinryo、DAS、Edwards、Ebara、Kurita、Organo、Entegris、Swagelok、VAT。

## 9. 投资观察框架

**短期 3-6 个月最该跟踪：**

1. TSMC、Micron、SK hynix、Samsung、Intel、SMIC/CXMT/YMTC 的 capex 和 cleanroom/tool-install 节点。
2. Exyte、Jacobs、Acter、UIS、L&K、亚翔、圣晖、柏诚、正帆的订单、在手合同、毛利率和应收账款。
3. HBM4 验证进展和 HBM cleanroom race，特别是 Samsung Pyeongtaek P5、SK hynix Yongin/M15X、Micron Idaho/Singapore/Japan。
4. UPW 回用和 PFC/PFAS abatement 是否成为地方审批/客户采购硬条件。
5. 美国/欧洲项目是否因劳工、许可、电力、水和材料延误，若延误则利好有本地交付能力的工程商和预制化供应商。

**估值更应给高倍数的类型：**

- 认证耗材和高纯部件：AMC/ULPA、UPW 膜树脂、UHP 阀件、气体安全、传感器。
- 主机 + 服务：真空泵、scrubber、POU abatement、UPW 运维。
- 软件/控制：FMCS、污染监测网络、节能优化、digital twin。
- 有半导体专门 know-how 的工程商：能绑定 TSMC/三星/美光/SK hynix/Intel/SMIC 的长期供应商。

**风险：**

1. AI capex 下修，晶圆厂扩产从极度乐观回到基准。
2. HBM/CoWoS 或先进节点需求延后，厂务订单滞后确认。
3. 海外 fab 补贴和许可延误导致项目拉长，工程商现金流承压。
4. 低端洁净室组件产能过剩，价格竞争侵蚀毛利。
5. 中国成熟制程扩产若受政策或融资影响放缓，本土洁净室工程商订单弹性下降。
6. 客户集中度高，单一大客户项目验收或变更会显著影响收入确认。

## 10. 主要来源和校验

| 来源 | 用途 |
|---|---|
| SEMI：[300mm Fab Outlook](https://www.semi.org/en/products-services/market-data/300mm-fab-outlook) | 2026/2027 300mm fab equipment spending、capacity 扩张锚点 |
| SEMI：[total semiconductor equipment sales forecast](https://www.semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports) | 2026/2027 半导体制造设备销售总量校验 |
| Gartner：[2026/2027 semiconductor revenue forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | AI 半导体和 hyperscaler capex 大盘校验 |
| TSMC：[1Q26 quarterly results](https://investor.tsmc.com/english/quarterly-results/2026/q1) / [1Q26 transcript PDF](https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf) | TSMC 收入、毛利、capex、AI/HPC 和先进封装扩产判断 |
| Micron：[FY26Q2 earnings release](https://investors.micron.com/news-releases/news-release-details/micron-technology-inc-reports-results-second-quarter-fiscal-2026) | HBM/AI 需求、cleanroom space/wafer capacity 约束 |
| Samsung：[1Q26 results](https://news.samsung.com/ca/samsung-electronics-announces-first-quarter-2026-results) | HBM3E/HBM4、memory/foundry outlook 和 AI server demand |
| SK hynix：[2025 financial results](https://news.skhynix.com/sk-hynix-reports-2025-financial-results/) | HBM 需求、AI memory 和 capex/产能方向 |
| TrendForce：[HBM cleanroom race](https://www.trendforce.com/news/2026/02/26/news-memory-giants-hbm-cleanroom-race-samsung-sk-hynix-fast-track-micron-acquires/) | Samsung/SK hynix/Micron HBM cleanroom 供应链媒体口径 |
| GlobalFoundries/Exyte：[Fab 1 SPRINT contract](https://www.exyte.net/Newsroom/Press-releases/Exyte-awarded-contract-for-Fab-1-capacity-expansion) | Exyte 半导体 cleanroom 工程订单一手信息 |
| Exyte：[Semiconductor market page](https://www.exyte.net/en/Markets/Semiconductors) | Exyte 半导体洁净室能力和累计交付面积 |
| Acter：[2025 annual results](https://www.acter.com.tw/index.php/en/news/A11) | 台湾/亚洲洁净室机电工程商订单和半导体客户验证 |
| ResearchAndMarkets：[UPW market 2026](https://www.researchandmarkets.com/report/ultrapure-water) | UPW 市场规模外部校验 |
| DAS Environmental Expert：[SEMICON Southeast Asia 2026](https://www.das-ee.com/en/news-events/news/2026/das-environmental-expert-at-semicon-southeast-asia-2026/) | 半导体尾气/废气处理供应商技术方向 |
| Ebara：[semiconductor vacuum product release](https://www.ebara.com/global-en/newsroom/2025/20251217-01/) | subfab dry vacuum pump 技术和节能趋势 |
| 亚翔集成、圣晖集成、柏诚股份、正帆科技、至纯科技公开年报/交易所公告 | 中国洁净室、厂务、高纯工艺系统公司订单、收入和毛利交叉验证 |

## 11. 读数注意事项

1. 本报告的“洁净室与厂务系统广义订单池”是工程、设备、材料、服务口径，部分与 fab capex、EPC 合同和供应商收入存在时间差，不能与 SEMI 设备投资直接相加。
2. 细分表中各产品之间存在总包/分包/材料重复，例如 HVAC 已包含部分 FFU 和滤材，EPC 又可能包含 HVAC 和 UPW，因此表格用于判断斜率和利润弹性，不用于逐项求和。
3. 极度超预期乐观情景的本质是假设 AI 推理需求继续吞掉所有新增 HBM、CoWoS、先进逻辑和区域化建厂产能，客户愿意用预付款和溢价换交期。
4. 若 hyperscaler 从 2026H2 开始严格压制 token ROI 或延迟数据中心上电，上游晶圆厂厂务订单会从极度乐观回到基准，但 HBM、先进封装、UPW、尾气处理和高纯系统的结构性升级方向不变。
# 行业调研：【探针卡、ATE与系统级测试】

> 截至日期：2026-05-08。  
> 研究口径：覆盖 AI/HPC 芯片量产所需的 wafer sort、probe card、probe station、ATE、memory tester、SoC tester、test handler、socket/contactor/interface board、burn-in、system-level test、光电/CPO 测试、测试服务与测试数据软件。金额均为美元名义值，`B` = 十亿美元；`B/O/X` = 基准/乐观/极度超预期乐观。  
> 方法说明：芯片路线引用项目内既有 `ai_chip_research_2026_2027.md`，外部资料侧重 2025H2-2026 年公司公告、财报、法说、会议资料和行业报告摘要。对 2026-2027 AI 基础设施建设采取明显乐观假设：需求端按 hyperscaler 继续锁电、锁 HBM、锁 CoWoS、锁测试产能处理；缺少直接公开数字的细分项用 AI 芯片出货量、HBM stack、测试时间、ATE 装机、OSAT 测试收入做大胆推演。

## 0. 一页结论

探针卡、ATE 与系统级测试在 2026 年从“半导体周期配套设备”升级为 **AI 芯片有效交付的瓶颈层**。原因很直接：GB300/B300、Trainium2/3、TPU Ironwood/TPU8、MI350/MI400、MTIA、Maia、OpenAI/Broadcom XPU 等都在把单颗芯片价值、HBM 数量、chiplet 数量、SerDes 带宽、功耗和封装报废成本推高。以前少测一点只是良率问题；2026 年少测一点可能导致几万美元到几十万美元级别的 2.5D/HBM package 报废，甚至让整柜 burn-in 失败。

| 判断 | 结论 |
|---|---|
| 2026 最确定主线 | HBM3E KGD/wafer sort、DRAM/HBM probe card、AI/HPC SoC ATE、high-power thermal handler、package-level burn-in、SLT handler、测试数据软件。 |
| 2026 最可能放量的新技术 | HBM4 early KGD、V93000/UltraFLEX 类高端 SoC 测试扩容、5Gbps 级 scan/DFT 测试卡、120mm 大封装 SLT、2-3kW 级 thermal control、CPO/silicon photonics wafer/package test。 |
| 2027 最大弹性 | Rubin/MI400/TPU8/OpenAI XPU/MTIA 450-500 把 HBM4、224G/448G SerDes、optical I/O、chiplet KGD、rack-scale burn-in 推到更高强度。 |
| 供给瓶颈本质 | 不是“买几台测试机”这么简单，而是 pin electronics、MEMS 探针、space transformer/MLC、测试程序、HBM/SerDes correlation、thermal control、socket 寿命、OSAT floor space、测试工程师共同构成的复合瓶颈。 |
| 长期价值捕获 | 高端 ATE 平台、HBM/AI probe card、socket/thermal handler、burn-in/SLT、测试数据软件/DFT/SLM。测试服务收入大但毛利不如设备/软件，除非绑定高端 AI 客户认证。 |
| 投资排序 | 1. Advantest/Teradyne 高端 ATE；2. FormFactor/Technoprobe/MJC/JEM/MPI 高端探针卡；3. Cohu/Chroma/Aehr 高功耗 handler/SLT/burn-in；4. KYEC/ASE/Amkor/PTI/JCET 等高端测试服务；5. PDF Solutions/proteanTecs/Advantest ACS/Cohu PAICe 测试数据软件。 |

**核心数字锚点：**

- Advantest FY2025 净销售额 **1.1286 万亿日元**、同比 **+44.7%**，营业利润 **4991 亿日元**、同比 **+118.8%**；FY2026 指引净销售额 **1.42 万亿日元**、营业利润 **6275 亿日元**。公司称 2026 年半导体 tester 市场预计达到最大规模，AI 相关半导体复杂度和产量增长驱动需求。
- Teradyne 2026Q1 收入 **$1.282B**、同比 **+87%**；其中 Semiconductor Test **$1.111B**。CEO 称约 **70%** 收入与 AI 需求相关，Q2 指引 **$1.15-1.25B**。
- FormFactor 2026Q1 收入 **$226.1M**、同比 **+32.0%**；DRAM probe card **$82.933M**、同比 **+69.7%**；Foundry & Logic **$111.188M**、同比 **+30.4%**；Probe Cards 分部毛利率 **50.5%**。
- Technoprobe 2025 收入 **€628.4M**、同比 **+15.7%**，EBITDA **€201.4M**、margin **32.1%**；公司称约 **38%** 收入来自 AI 相关应用，并计划 2026-2027 年底前把产能翻倍，2027 年收入目标 **€850-900M**、EBITDA margin **38-40%**。
- Cohu 2026Q1 收入 **$125.1M**，毛利率 **46.3%**，把 AI-driven compute addressable market 估计上调到 **约 $750M**，FY2026 HPC 收入展望上调到 **$80-100M**；2026-04 公布两家客户 **$30M** HPC follow-on orders，用于带主动热控的 Eclipse 平台。
- Aehr 2026 财年 Q3 bookings **$37.2M**、book-to-bill **>3.5x**，有效 backlog **$50.9M**；Q2 时公司预计 FY2026 下半年 bookings **$60-80M**，并强调 AI processor WLBI/PLBI、Sonoma ultra-high-power burn-in、silicon photonics。
- Chroma 2025-08 发布 SLT handler 组合：3210-A 支持 **120 x 120mm** 大封装、**-40C 至 150C**、最高 **2,900W** 散热；3200 平台支持 **4-24 test sites**、最高 **1,800W** thermal engine，CVOT 可提升 retest yield **最高 8%**、测试周期降低 **最高 10%**。

## 1. 2026 AI 计算中心大建设下的机遇、挑战与技术路线

### 1.1 为什么 AI 数据中心把测试行业推到前台

2026 年 AI 芯片测试强度上升来自四个乘数：

1. **HBM 乘数**：高端 GPU/ASIC 几乎 100% attach HBM，HBM3E 仍是 2026 主力，HBM4 从 Rubin/MI400/TPU8/ASIC early ramp。HBM 是多 die、多 TSV、多 I/O、多温度条件的良率问题，必须做 KGD。
2. **Chiplet 乘数**：2.5D/3D package 里任何一个坏 die 都会放大报废损失。Technoprobe CMD 里把逻辑讲得很直白：advanced packaging 的 yield loss 不是简单相加，而是乘法；解决方案是 more test at probe。
3. **功耗乘数**：GB300、Rubin、MI400、Maia200 等进入 750W-2kW+ 单器件/模块热设计区间，final test 和 SLT 必须接近真实功耗环境。
4. **系统乘数**：AI rack 不只测 die，还要测 HBM、NVLink/UALink/NeuronLink、PCIe/CXL、SerDes、thermal throttling、firmware、power transient 和整柜 burn-in。

### 1.2 2026-2027 主力 AI 芯片路径对测试的映射

| 平台，来自项目内 AI 芯片路线 | 2026-2027 阶段 | 对 probe/ATE/SLT 的拉动 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 主力放量 | HBM3E KGD、GPU wafer sort、NVLink/NVSwitch/SerDes final test、高功耗 handler、整柜 burn-in。 |
| AWS Trainium2 | Rainier 主力，近百万级别潜在需求 | 自研 ASIC + HBM + NeuronLink；测试服务更偏 AWS/OSAT 定制，SLT 与数据中心级 burn-in 价值高。 |
| Google TPU v7 Ironwood | 2026 大规模部署 | HBM3E、Broadcom XPU、云端 pod 级验证；HBM KGD、package test、系统互连测试强。 |
| NVIDIA B200/GB200 | 2026 延续交付 | 成熟 CoWoS/HBM3E，支撑测试产线利用率，部分测试程序复用到 GB300。 |
| Huawei Ascend 910C/950 | 中国国产替代 | 国产 wafer sort、OAM 模块、HBM/高带宽内存、国产 SLT/ATE 替代需求强，但受先进制程和 HBM 约束。 |
| Cambricon MLU 590/690 | 2026 国产训练/推理放量 | SMIC 可得节点 + HBM/OAM，测试瓶颈在本土高端 ATE、probe card、burn-in 和客户认证。 |
| AMD MI350 | 2026 AMD 最确定放量 | HBM3E、UBB/OAM/PCIe 多形态，ROCm 兼容性与系统级 burn-in 重要。 |
| AWS Trainium3 | 2026-2027 接棒 | 3nm、HBM3E、144-chip UltraServer，拉动 ASIC ATE、memory tester、scale-up fabric SLT。 |
| Meta MTIA 300/400/450/500 | 2026-2027 四代迭代 | 推理 ASIC 大规模云端部署，volume learning、DFT/SLM、test data feedback 价值上升。 |
| Microsoft Maia 200 | 2026 Azure 推理导入 | TSMC 3nm、216GB HBM3E、闭环液冷，package final test 与 Azure rack burn-in 强绑定。 |
| OpenAI/Broadcom XPU | 2026H2 起步，2027 弹性 | 10GW 路线若兑现，将直接争抢高端 ATE、HBM KGD、SLT 和测试服务产能。 |
| NVIDIA Rubin / AMD MI400 / TPU8 | 2026H2 early，2027 放量 | HBM4、更多 HBM stack、更多高速互连，触发第二轮 tester/probe card/thermal handler 升级。 |

### 1.3 当前正在使用的关键技术

| 技术 | 当前使用状态 | 2026 价值判断 |
|---|---|---|
| MEMS vertical probe card | DRAM/HBM、foundry/logic 主流高端方案 | HBM 与 AI logic 的最直接受益品，pin count、pitch、planarity、cleaning、repair 决定稼动。 |
| Advanced cantilever / blade / cobra probe | 模拟、RF、功率、成熟逻辑仍大量使用 | 增速低于 MEMS，但功率与 RF/CPO 仍有利基。 |
| Space transformer / MLC / MLO / high-density PCB | 高端 probe card 核心 BOM | 大封装、高 pin count 和高速 I/O 使 ceramic/MLC 价值上升。 |
| SoC ATE：V93000、UltraFLEX/IG-XL 等 | AI/HPC wafer sort/final test 主力 | 2026 最强设备收入池，客户愿为 coverage 和 test time 付费。 |
| Memory ATE：HBM/DRAM/NAND tester | HBM3E/DDR5/GDDR/enterprise SSD 测试 | HBM4 I/O 与速度上升后再度升级。 |
| High-power handler/thermal control | AI package final test 和 SLT 必需 | 2kW+ 散热、tri-temp、contact force、socket life 成为差异化。 |
| Burn-in：WLBI、PLBI、HTOL | AI processor、silicon photonics、SiC、memory 需求上升 | Aehr 的订单说明 AI 客户开始把 reliability screen 前移到 wafer/die。 |
| System-level test | GPU/ASIC 模块、整板、整柜 | 2026 从工程验证变成量产瓶颈，尤其高功率与互连相关 failure。 |
| Adaptive test / SLM / test analytics | Advantest ACS、Cohu PAICe、PDF/proteanTecs 等 | 数据闭环可减少 test time、定位早期失效、提升 OEE，毛利率最高。 |
| CPO/silicon photonics test | 早期但加速 | 800G/1.6T/CPO/optical I/O 使 wafer-level photonics + electrical co-test 成为 2027 期权。 |

### 1.4 新技术成熟与放量时间表

| 技术 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观/极超 |
|---|---|---|---|---|---|
| HBM3E KGD/probe/test | 满载放量，SK hynix/Samsung/Micron 扩产同步买 probe/test | HBM3E 价格高位，测试设备订单跟随扩产 | 2026 H2 需求前置，测试产能成为比 HBM wafer 更硬的约束 | 仍大规模出货，但被 HBM4 分流 | HBM3E 用于中高端推理，生命周期延长。 |
| HBM4/HBM4E probe/test | 2026H2 NPI/小批量 | Q4 出现明显订单 | 三大 HBM 厂验证顺利，tester/probe card 订单提前 | 2027 主力导入 | HBM4E 2027H2 提前锁单，probe/test ASP 上升。 |
| 5Gbps+ scan/DFT digital test | Advantest Pin Scale 5000B ramping with key customers | 高端 AI SoC 标配深 vector memory | AI 芯片 test time 压力使客户批量升级 tester cards | 更多 AI ASIC 使用 | DFT/ATE 协同成为设计约束。 |
| 120mm 大封装 SLT | Chroma/Cohu/Aehr 等提供产品，2026 开始拉动 | AI package final test 转向高功率真实负载 | 2-3kW thermal SLT 成为高端 xPU 默认 | 2027 扩到更多 ASIC/GPU | rack-level SLT 与 chip/package SLT 数据打通。 |
| Wafer-level burn-in for AI | Aehr 已有 AI processor customer 与 benchmark | WLBI 成为 CoWoS/HBM package 前筛选工具 | 高价值 package 报废压力使 WLBI 激进导入 | 2027 放量 | 适用于 AI accelerator、silicon photonics、HBF/新存储。 |
| CPO/silicon photonics test | 2026 小批量/工程收入 | FormFactor Triton、Chroma photonics、Aehr WLBI 加速 | Optical I/O 被 AI rack 提前采用 | 2027 高端 switch/CPO 小批量 | 2028 才是更大收入，但 2027 design-in 关键。 |
| Test data AI/analytics | OEE、adaptive test、yield learning 已部署 | AI 测试复杂度提高，订阅收入上升 | 测试数据成为客户良率与 field failure 的核心资产 | 渗透 OSAT/IDM | 与 DFT/SLM/数字孪生深度绑定，软件毛利最强。 |

## 2. 已经开始放量的关键产品：市场规模、渗透率与利润率

> 说明：以下为全球可服务收入池估算，包含设备、耗材、部分服务和软件；不同项之间存在少量重叠。未来 3 个月按 2026Q2-Q3 可确认订单/收入，未来 12 个月按 2026H2-2027H1，未来 24 个月按 2026H2-2028H1。

| 已放量产品/技术 | 当前状态 | 未来3个月市场规模 B/O/X | 未来12个月市场规模 B/O/X | 未来24个月市场规模 B/O/X | 渗透率路径 | 增长预测 | 毛利率/利润率 B/O/X |
|---|---|---:|---:|---:|---|---|---|
| HBM/DRAM MEMS probe card 与 KGD wafer sort interface | FormFactor DRAM 2026Q1 +69.7%；Technoprobe 明确进入 HBM；HBM3E 满载 | $0.45-0.75B / $0.7-1.0B / $1.0-1.5B | $2.0-3.3B / $3.2-5.0B / $5.0-7.5B | $4-7B / $7-12B / $12-20B | HBM wafer sort attach rate 近 100%；HBM4 在高端 HBM probe/test 中占比 2026 <10%，2027 25-45%，2028 45-65%。 | 2026 +50-90%，2027 +45-100%。 | 45-58% / 55-68% / 62-75%；头部 MEMS+space transformer 溢价最强。 |
| Foundry/Logic AI/HPC probe card | FormFactor F&L 2026Q1 +30.4%，网络和 HPC microprocessor 拉动；Technoprobe AI 收入 38% | $0.65-1.0B / $0.9-1.4B / $1.3-2.0B | $2.8-4.5B / $4.0-6.2B / $6.0-9.0B | $5-8B / $8-13B / $13-21B | 高端 AI GPU/ASIC wafer sort 中 advanced probe card 2026 75-85%，2028 85-95%。 | 2026 +25-55%，2027 +35-75%。 | 42-55% / 52-64% / 60-72%。 |
| AI/HPC SoC ATE 平台与 pin electronics | Advantest FY2026 指引 1.42T 日元；Teradyne 2026Q1 semitest $1.111B | $3.2-4.8B / $4.5-6.5B / $6.0-8.5B | $13-18B / $18-25B / $25-35B | $24-36B / $36-55B / $55-80B | 先进 AI/HPC SoC wafer/final test 近 100%；AI 专用高端 ATE 占 SoC tester 新增需求 2026 50-65%，2027 60-75%。 | 2026 +30-60%，2027 +25-70%。 | 55-65% GM，35-45% OPM / 60-68% GM，40-50% OPM / 65-72% GM，45-55% OPM。 |
| Memory ATE：HBM/DDR5/GDDR/NAND/enterprise SSD | AI HBM 和 server DRAM 拉动；Teradyne memory near-record，Advantest memory tester elevated | $1.6-2.5B / $2.3-3.6B / $3.4-5.0B | $6.5-10B / $10-15B / $15-22B | $12-20B / $20-32B / $32-52B | HBM4/DDR5/MRDIMM/CXL memory test 强度上升；HBM4 tester attach 从 2026 NPI 到 2027 主力。 | 2026 +40-90%，2027 +35-85%。 | 52-62% / 58-68% / 65-75%。 |
| High-power handler、thermal control、test cell automation | Advantest M4872、Cohu Eclipse、Chroma 3100/3200；功耗和封装尺寸驱动 | $0.75-1.2B / $1.1-1.7B / $1.7-2.6B | $3.2-5.0B / $5.0-7.5B / $7.5-11B | $6-10B / $10-16B / $16-26B | 高端 AI package final test 中主动热控 handler 渗透 2026 40-60%，2028 65-85%。 | 2026 +30-70%，2027 +45-90%。 | 35-48% / 45-56% / 55-65%；热控、自动化和软件订阅提高混合毛利。 |
| Test socket、contactor、interface board、DIB | Advantest Services & Others 高性能 SoC interface board 增长；Cohu contactor 强 | $0.9-1.4B / $1.3-2.0B / $2.0-3.0B | $3.8-6.0B / $6.0-9.0B / $9-14B | $7-12B / $12-20B / $20-35B | 高端 AI final test/SLT 中 socket/contactors 属消耗件，随测试时长和并行数提升。 | 2026 +25-60%，2027 +35-80%。 | 40-55% / 50-65% / 60-75%；稀缺高功率 socket 可有高溢价。 |
| Package-level burn-in、HTOL、WLBI/PLBI 设备 | Aehr Sonoma/FOX-XP，AI processor 与 silicon photonics 订单加速 | $0.35-0.7B / $0.6-1.1B / $1.0-1.8B | $1.8-3.2B / $3.0-5.5B / $5.0-9.0B | $4-7B / $7-13B / $13-24B | 高端 AI package burn-in 渗透 2026 25-40%，2028 50-70%；WLBI 在 CoWoS 前筛选渗透更低但增速最高。 | 2026 +40-120%，2027 +60-150%。 | 40-55% / 50-65% / 60-75%；小公司规模利润波动大。 |
| System-level test handler/cell/SLT software | Chroma 3200、Cohu、Advantest SLT；ODM/OSAT/云厂自建 burn-in | $0.8-1.4B / $1.2-2.2B / $2.0-3.5B | $3.5-6B / $6-10B / $10-18B | $8-14B / $14-25B / $25-45B | 高端 AI accelerator module SLT 渗透 2026 35-55%，2028 60-80%；rack-level burn-in 由整机厂另行放大。 | 2026 +35-90%，2027 +50-120%。 | 30-45% / 42-55% / 52-65%；自动化和数据软件拉高。 |
| 高端 OSAT/IDM 测试服务：wafer sort/final test/SLT | ASE、Amkor、KYEC、PTI、JCET、Tongfu、Huatian、TSMC/Intel/Samsung internal | $2.0-3.5B / $3.0-5.0B / $5.0-8.0B | $8-14B / $14-24B / $24-40B | $16-30B / $30-55B / $55-90B | AI/HBM/advanced package 测试服务在 OSAT test revenue 中占比 2026 15-25%，2028 30-45%。 | 2026 +25-60%，2027 +35-90%。 | 20-35% / 30-42% / 40-50%；认证产能可接近设备毛利，但折旧重。 |
| Test analytics / adaptive test / SLM 数据软件 | Advantest ACS、Cohu PAICe、PDF、proteanTecs、yieldHub 等 | $0.25-0.45B / $0.4-0.7B / $0.7-1.1B | $1.2-2.0B / $2.0-3.5B / $3.5-6.0B | $2.8-5B / $5-9B / $9-16B | 高端 AI test cell 2026 30-45% 使用 advanced analytics，2028 60-80%。 | 2026 +25-70%，2027 +45-100%。 | 软件 GM 70-90%，OPM 20-45%；极超情景 OPM 50%+。 |
| CPO/silicon photonics wafer/package test | FormFactor Triton 过渡、Aehr silicon photonics、Chroma photonics | $0.15-0.35B / $0.3-0.6B / $0.6-1.0B | $0.8-1.5B / $1.5-3B / $3-5B | $2-5B / $5-10B / $10-20B | CPO/optical I/O 在 AI switch/xPU 中 2026 <5%，2028 10-25%；测试设备先于收入。 | 2026 +50-150%，2027 +80-200%。 | 35-55% / 50-65% / 60-75%；早期良率风险高。 |

### 2.1 已放量产品的利润率判断

利润率最强的不是简单“测试服务”，而是 **高端专用硬件 + 消耗件 + 软件闭环**：

- **高端 probe card**：FormFactor 2026Q1 Probe Cards 分部毛利率 50.5%，AI/HBM 产品 mix 继续改善时可上行；Technoprobe EBITDA margin 2025 为 32.1%，2027 目标 38-40%。
- **高端 ATE**：Advantest FY2025 operating margin 44.2%，FY2026 指引 implied operating margin 约 44.2%；Teradyne semitest 在 AI cycle 下规模杠杆强。行业景气上行时，高端 tester 的议价能力可维持。
- **handler/socket/contactor**：Cohu 当前混合毛利 46% 左右，高端 HPC thermal handler 和 contactor 可能显著高于公司平均。
- **SLT/burn-in**：设备毛利好于服务，服务毛利受折旧、场地、电力、人工压制；但 AI 客户认证产能紧缺时可出现价格重估。
- **软件/analytics**：毛利最高，但收入确认慢，依赖测试机装机量、客户数据权限和 OSAT/IDM 组织流程。

## 3. 在研和早期导入关键产品：未来增长区间

| 在研/早期产品 | 当前阶段 | 成熟/放量时间 | 未来3个月市场 B/O/X | 未来12个月市场 B/O/X | 未来24个月市场 B/O/X | 渗透率路径 | 利润率假设 |
|---|---|---|---:|---:|---:|---|---|
| HBM4/HBM4E probe card、memory tester、KGD program | 2026H1 验证/NPI | 2026H2 early，2027 放量 | $0.2-0.5B / $0.4-0.8B / $0.8-1.4B | $1.5-3B / $3-6B / $6-10B | $5-10B / $10-20B / $20-35B | 高端 HBM 新增中 HBM4 2027 30-50%，2028 50-70%。 | 55-75%；NPI 工程费、首发 probe/test 溢价高。 |
| 16-high/20-high HBM WLBI 与 stack-level burn-in | HBM4 相关早期 | 2027 放量，2028 扩大 | $0.05-0.2B / $0.1-0.4B / $0.4-0.8B | $0.5-1.5B / $1.5-3B / $3-6B | $2-5B / $5-12B / $12-24B | 2026 <5%，2028 20-40%。 | 45-70%，但良率与throughput风险高。 |
| 224G/448G SerDes、PCIe 7/8、UCIe 3.0 test | PCIe DevCon 2026 已进入系统级相关性讨论 | 2026 设计导入，2027 小量产 | $0.15-0.35B / $0.3-0.6B / $0.6-1B | $0.8-1.8B / $1.8-3.5B / $3.5-6B | $3-7B / $7-14B / $14-25B | 高端 switch/retimer/XPU 2027 渗透 10-25%，2028 25-45%。 | 仪器/ATE 55-70%，IP/software 80-90%。 |
| Photonic wafer-level co-test、CPO optical engine tester | 2026 工程导入 | 2027 高端 switch/CPO early volume | $0.1-0.3B / $0.2-0.5B / $0.5-0.9B | $0.6-1.5B / $1.5-3.5B / $3.5-7B | $2-5B / $5-12B / $12-25B | CPO 与 optical I/O 测试 attach 先行，2028 前仍小但增长最快。 | 45-75%，取决于良率、光学校准自动化和客户锁定。 |
| 2.5D/3D package pre-bond/post-bond KGD flow | Chiplet Summit 2026 强调 True KGD | 2026-2027 从工具链变成量产流程 | $0.2-0.5B / $0.4-0.8B / $0.8-1.5B | $1.2-2.5B / $2.5-5B / $5-9B | $4-8B / $8-18B / $18-35B | 高端 AI chiplet 2026 50%+ 需要更严格 KGD，2028 接近标配。 | 硬件 45-65%，软件/IP 75-90%。 |
| AI rack-level burn-in/digital twin test | 整机 ODM/云厂内部快速扩张 | 2026 GB300/NVL72，2027 Rubin/Helios | $0.3-0.8B / $0.7-1.5B / $1.5-3B | $2-5B / $5-10B / $10-20B | $6-15B / $15-35B / $35-70B | AI rack 出货中 rack-level burn-in 2026 40-60%，2028 70-90%。 | 20-40% 服务，40-60% 自动化/软件。 |
| AI-assisted test program generation/debug | Advantest SmarTest 8 已展示 AI 工具方向 | 2026 工程生产力，2027 商业化增强 | $0.05-0.15B / $0.1-0.3B / $0.3-0.6B | $0.4-1B / $1-2B / $2-4B | $1.5-4B / $4-8B / $8-15B | 高端 ATE 客户从试用到流程绑定，2028 渗透 30-50%。 | 软件 75-90%，但需与 ATE 平台绑定。 |
| Full-wafer high-power contactor / WaferPak 类产品 | Aehr 已用于 300mm WLBI；AI benchmark 进行中 | 2026H2-2027 放量 | $0.1-0.25B / $0.2-0.5B / $0.5-0.9B | $0.6-1.3B / $1.3-3B / $3-6B | $2-5B / $5-12B / $12-22B | CoWoS 前坏 die 筛选需求提升，2028 可成高端 AI 流程选项。 | 45-70%，耗材与系统组合好。 |
| 国产高端 ATE/probe/SLT 替代 | 中国 AI 芯片国产替代推进 | 2026 政策订单，2027 更大规模 | $0.2-0.6B / $0.5-1B / $1-2B | $1.5-3B / $3-6B / $6-12B | $4-8B / $8-18B / $18-35B | 国产 AI wafer/package test 中国产设备渗透 2026 10-20%，2028 25-45%。 | 初期 25-45%，成熟后 40-60%；认证壁垒高。 |

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能和能力集中在哪里

| 环节 | 主要地区 | 代表公司 | 关键能力 |
|---|---|---|---|
| SoC/Memory ATE | 日本、美国、台湾/中国大陆补充 | Advantest、Teradyne、Cohu、Chroma、SPEA、Hangzhou Changchuan、Huafeng Test、Beijing Huafeng、AccoTEST 等 | Pin electronics、DPS、高速数字、混合信号、test OS、tester fleet、客户程序生态。 |
| 高端 probe card | 美国、意大利、日本、台湾、韩国、中国大陆 | FormFactor、Technoprobe、Micronics Japan/MJC、Japan Electronic Materials/JEM、MPI、TSE、Microfriend、Korea Instrument、WinWay、SV Probe、Feinmetall、Wentworth、Will Technology、强一、精测电子等 | MEMS 探针、fine pitch、space transformer、MLC/MLO、repair/cleaning、HBM/logic 客户认证。 |
| Probe station/prober | 日本、台湾、德国/奥地利、美国 | Tokyo Seimitsu/Accretech、TEL、MPI、FormFactor/Cascade、Wentworth、Micromanipulator、SUSS MicroTec、Semics | wafer handling、temperature chuck、high parallelism、RF/photonic alignment。 |
| Handler/thermal/socket | 美国、德国、日本、台湾、中国大陆/东南亚 | Cohu、Advantest、Chroma、Seiko Epson、Hon Precision、Yamaichi、Enplas、Yokowo、Smiths Interconnect、Leeno、TSE、WinWay、ISC、Ironwood、Plastronics | 大封装、高 contact force、tri-temp、active thermal control、socket寿命。 |
| Burn-in/SLT | 美国、台湾、日本、德国、中国大陆 | Aehr、Chroma、Cohu、Advantest、Teradyne、Micro Control、ESPEC、Thermotron、Incal/Aehr、Exatron、Nidec、Hon Precision | WLBI、PLBI、HTOL、SLT automation、高功率散热、电源可靠性。 |
| 测试服务/OSAT | 台湾、马来西亚、新加坡、韩国、中国大陆、美国 | ASE/SPIL、Amkor、KYEC、Powertech/PTI、ChipMOS、UTAC、JCET、Tongfu、Huatian、Hana Micron、Sigurd、Giga Solution、TSMC/Intel/Samsung internal | wafer sort、final test、burn-in、SLT、客户认证、测试 floor space 和工程师。 |
| 测试仪器/高速合规 | 美国、德国、日本、中国台湾 | Keysight、Rohde & Schwarz、Anritsu、Tektronix、Teledyne LeCroy、NI/Emerson、Spirent、Viavi | BERT、VNA、oscilloscope、protocol analyzer、PCIe/CXL/Ethernet/optical compliance。 |
| 测试数据/DFT/SLM | 美国、以色列、欧洲、日本 | PDF Solutions、proteanTecs、Advantest ACS、Cohu PAICe/Tignis、Synopsys、Siemens EDA、Cadence、yieldHUB | Adaptive test、traceability、SLM sensor、yield analytics、AI test debug。 |

### 4.2 至少 12 条供给瓶颈

1. **高端 pin electronics ASIC 和 tester card**：AI/HPC SoC 需要更多数字通道、深 vector memory、功率/模拟控制，高端 tester card 供应不是短期可复制。
2. **MEMS 探针和 fine-pitch 制造**：HBM/AI logic 的 pitch、平面度、接触电阻、寿命要求高，良率和 repair 能力决定产能。
3. **Space transformer / MLC / MLO**：高 pin count 的 fan-out 依赖陶瓷/多层互连，交期和良率容易成为 probe card 交付瓶颈。
4. **大功率 thermal control**：1-3kW 器件测试要求 active liquid/TEC/LN2/air 混合热控，温度均匀性和响应速度难。
5. **Socket/contact 寿命**：高电流、大封装、高 contact force 使 socket 消耗快，消耗件供应紧张会限制 test cell uptime。
6. **HBM correlation**：HBM wafer sort、stack test、package test、系统失效之间要建立 correlation，工程数据积累无法靠买设备跳过。
7. **测试程序开发**：每代 AI 芯片 DFT、scan、BIST、SerDes、HBM、thermal throttle、firmware 流程复杂，test engineer 稀缺。
8. **测试时间上升**：AI chip test coverage 增加，若 test time 翻倍，需要的 tester 数量近似翻倍，除非 adaptive test 抵消。
9. **OSAT floor space 和电力/冷却**：SLT/burn-in 占地、耗电、散热远高于传统 final test，测试厂扩产受基础设施限制。
10. **客户认证周期**：更换 probe card、ATE platform、socket、burn-in flow 往往需要 6-18 个月数据，AI 芯片代际窗口很短。
11. **地缘和出口管制**：高端 ATE、测试软件、维修备件、probe card 技术对中国先进 AI 芯片构成约束，国产替代需要时间。
12. **CPO/硅光测试方法未完全标准化**：光学校准、温漂、老化、electrical-optical correlation 仍在演进，早期良率风险大。
13. **维修和 uptime**：探针卡清洗、socket 更换、handler 校准、ATE uptime 对产出影响变大，服务网络本身成为竞争壁垒。
14. **安全/数据隔离**：云厂 ASIC 和高端 GPU 测试数据敏感，测试服务商需要满足客户数据安全和供应链审计。

### 4.3 成本构成和毛利决定因素

| 产品 | 成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 高端 probe card | MEMS needles/probe head 20-30%；space transformer/MLC 25-40%；PCB/stiffener 10-20%；assembly/calibration 15-25%；repair/test 5-15%。 | pin count、pitch、planarity、接触电阻、寿命、客户认证、交期。 | NPI 工程费 + 项目制报价 + repeat order；HBM/AI 稀缺时交期溢价。 |
| SoC/Memory ATE | pin cards/DPS/digitizer/analog 35-50%；机柜/冷却/电源 10-20%；software/test OS 10-20%；服务/安装/备件 10-15%；供应链/折旧 10-20%。 | 测试覆盖率、并行度、test time、fleet software、客户程序生态、装机基数。 | 大客户 capex + 长周期服务；客户更看 cost-of-test 而不是单机价格。 |
| Handler/SLT | 机械/自动化 20-30%；thermal engine/冷却 20-35%；socket/contactor 15-30%；电源和传感 10-20%；软件 5-15%。 | 热控能力、contact stability、UPH、socket life、维护时间。 | 与 test cell OEE、retest yield、UPH 绑定，客户愿为减少停机付费。 |
| Burn-in 设备 | chamber/thermal 20-30%；power supply/load board 25-35%；socket/fixture 15-25%；automation 10-20%；software 5-15%。 | 高功率密度、并行数、可靠性标准、客户认证、耗材寿命。 | AI package 价值高，客户按避免报废和 field failure 的 ROI 付费。 |
| 测试服务 | 设备折旧 25-40%；人工/工程 15-25%；耗材/socket/probe 10-20%；电力/冷却/floor 10-20%；良率/返工 5-15%。 | 稼动率、客户 mix、设备折旧、认证产能、测试时间。 | LTA/预付款/产能预订；高端 AI 客户可能接受 premium slot。 |
| 测试软件/analytics | R&D 40-60%；云/部署 5-15%；销售支持 15-25%；数据工程 10-20%。 | 数据接入、ATE/OSAT 集成、模型有效性、客户流程锁定。 | 订阅 + license + per-test-cell；按 OEE/test time/yield 改善分享价值。 |

## 5. 竞争格局与壁垒：谁能长期定价

### 5.1 市场结构

| 细分 | 市场结构 | 头部公司 |
|---|---|---|
| 高端 ATE | 双寡头最强，Advantest 与 Teradyne 占高端 SoC/Memory 核心份额；Cohu/Chroma/SPEA/国产厂补充。 | Advantest、Teradyne、Cohu、Chroma、SPEA、Changchuan、Huafeng、AccoTEST。 |
| HBM/DRAM probe card | 头部集中，客户认证强；FormFactor、Technoprobe、MJC/JEM 等最强。 | FormFactor、Technoprobe、MJC、JEM、MPI、TSE、Microfriend、WinWay。 |
| Logic/HPC probe card | 高端集中但比 HBM 分散，foundry/logic 客户定制多。 | FormFactor、Technoprobe、MJC、MPI、JEM、SV Probe、TSE、Korea Instrument。 |
| Handler/thermal/socket | Cohu、Advantest、Chroma 强；socket/contactors 供应商更分散但高端认证强。 | Cohu、Advantest、Chroma、Hon Precision、Yamaichi、Enplas、Leeno、Smiths、TSE、WinWay。 |
| Burn-in/SLT | 传统分散，AI 高功耗方向出现专业化。 | Aehr、Chroma、Cohu、Advantest、Teradyne、Micro Control、ESPEC、Incal/Aehr。 |
| 测试服务 | 大而分散，台湾/东南亚/中国大陆/韩国集群；高端 AI 认证产能集中。 | ASE/SPIL、Amkor、KYEC、PTI、JCET、Tongfu、Huatian、ChipMOS、UTAC、Hana Micron、TSMC internal。 |
| 高速仪器/合规 | 高端仪器寡头，协议和光电测试壁垒高。 | Keysight、Rohde & Schwarz、Anritsu、Tektronix、Teledyne LeCroy、NI/Emerson。 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| 技术壁垒 | AI/HBM 测试要同时满足 fine pitch、高电流、高速、热控和并行度。单一指标达标不够，客户买的是稳定 yield。 |
| 认证壁垒 | Probe card、socket、ATE program、SLT flow 一旦进入量产，切换会重新跑 correlation 和可靠性，可能错过整代芯片窗口。 |
| 规模壁垒 | 高端 ATE 装机、备件、软件生态和全球服务网络使客户不愿切换平台；probe card 需要大量应用工程和 repair 网络。 |
| 数据壁垒 | 测试厂和设备商掌握失效模式、binning、probe mark、test time、field return 数据，后发者没有历史学习曲线。 |
| 客户锁定 | AI 芯片在设计阶段就决定 DFT、scan chain、HBM test strategy、SLT coverage，测试供应商越早参与越能锁定。 |
| 耗材锁定 | Socket、contactor、probe head、interface board 是重复消耗，进入平台后生命周期收入远大于首套设备。 |
| 产能壁垒 | 高端测试机、SLT cell 和 burn-in floor space 可以被大客户预订；稀缺时客户按交付时点付溢价。 |
| 人才壁垒 | Test engineer、DFT engineer、failure analysis、thermal/mechanical test 人才稀缺，无法通过资本开支快速补齐。 |

### 5.3 价值捕获：哪一层最可能高 ROIC/高毛利

1. **ATE 平台与软件生态**：Advantest/Teradyne 的高端平台拥有 installed base、程序生态、服务网络和高端 pin electronics，ROIC 质量最好。
2. **HBM/AI probe card 龙头**：FormFactor、Technoprobe、MJC/JEM 等直接吃 HBM 和 AI logic wafer sort，定制化和耗材属性兼具。
3. **Socket/contactors/thermal handler**：单价不如 ATE，但消耗频率高，且高功耗 AI 器件会让 socket 寿命和 thermal control 变成刚需。
4. **测试数据软件/SLM**：毛利最高，长期锁定最强，但收入基数还小，落地依赖客户数据权限。
5. **高端测试服务**：规模和订单弹性大，但资本密集、人工和折旧重；高 ROIC 只属于拿到 AI 客户长期认证和高稼动率的厂商。

## 6. 2026 关键变化：三个拐点与最可能放量子方向

### 拐点一：HBM KGD 从“内存厂环节”变成 AI 出货瓶颈

2026 主力仍是 HBM3E，但 HBM4 early ramp 已经提前拉动 probe card、memory tester、TC bonding 和 burn-in 预算。FormFactor 和 Technoprobe 的 2026 数据已经验证这一点。最可能放量的子方向是 HBM/DRAM MEMS probe card、memory tester、HBM wafer sort interface、KGD data analytics。

### 拐点二：AI SoC ATE 需求从周期复苏变成结构扩容

Advantest FY2025/FY2026 指引和 Teradyne 2026Q1 同时说明，高端 tester 不是普通半导体库存修复，而是 AI/HPC 复杂度、产量和 supply chain expansion 的结果。最可能放量的是 V93000 EXA Scale、Pin Scale 5000B 类高端 digital card、UltraFLEX/SoC test、mixed-signal/PMIC/PAC test。

### 拐点三：SLT/burn-in 从后段补充变成 AI package 经济性核心

AI package 报废成本太高，客户会把筛选前移到 wafer/die，也会把 final test 后移到真实系统负载。Aehr 的 WLBI/PLBI 订单、Cohu 的 Eclipse 高功耗热控订单、Chroma 的 120mm/2.9kW SLT handler 都指向同一趋势。最可能放量的是 high-power thermal handler、package-level burn-in、WLBI、SLT automation、rack burn-in。

## 7. 2027 关键变化：三个拐点与最可能放量子方向

### 拐点一：HBM4 + Rubin/MI400/TPU8/OpenAI XPU 把测试强度再抬一阶

2027 高端新增平台会从 HBM3E 迁移到 HBM4，I/O、stack、功耗、base die、chiplet 数量都更高。最可能放量的是 HBM4 probe card、HBM4 memory tester、pre-bond/post-bond KGD、high-current socket、2kW+ thermal SLT。

### 拐点二：224G/448G SerDes 与 CPO/optical I/O 进入量产前夜

PCIe 7/8、UCIe 3.0、800G/1.6T/3.2T、CPO/optical-aware retimer 会把测试从 electrical-only 扩展到 electrical-optical co-test。最可能放量的是 photonics wafer probe、CPO optical engine test、BERT/VNA/protocol compliance、silicon photonics burn-in。

### 拐点三：测试数据闭环成为 chiplet 供应链责任边界

Chiplet 量产需要回答“谁保证 KGD、谁承担坏 die、谁定位 field failure”。2027 以后客户会要求 traceability、SLM sensor、adaptive test、fleet analytics。最可能放量的是 ACS/PAICe/PDF/proteanTecs 类软件，以及 OSAT 与云厂共同建立的 test data lake。

## 8. 公司清单：按产品和技术拆分

### 8.1 ATE 与核心测试平台

| 细分 | 公司 |
|---|---|
| 高端 SoC ATE | Advantest、Teradyne、Cohu、Chroma、SPEA、Hangzhou Changchuan、Huafeng Test、AccoTEST、中科飞测相关生态 |
| Memory/HBM ATE | Advantest、Teradyne、Chroma、Cohu、UniTest、YIK、Exicon、Changchuan、Huafeng、TESEC |
| Power/analog/RF/mixed-signal ATE | Teradyne、Advantest、Cohu、Chroma、SPEA、Keysight、NI/Emerson、AccoTEST、Huafeng |
| 测试软件/OS | Advantest SmarTest、Teradyne IG-XL/UltraFLEX ecosystem、Cohu PAICe/Tignis、PDF Solutions Exensio、proteanTecs、yieldHUB |

### 8.2 探针卡、探针台与 wafer sort

| 细分 | 公司 |
|---|---|
| 高端 MEMS probe card | FormFactor、Technoprobe、Micronics Japan/MJC、Japan Electronic Materials/JEM、MPI、TSE、Microfriend、Korea Instrument、WinWay、SV Probe、Feinmetall |
| DRAM/HBM probe card | FormFactor、Technoprobe、JEM、MJC、Microfriend、TSE、MPI、WinWay、Korea Instrument、Will Technology |
| Logic/HPC probe card | FormFactor、Technoprobe、MJC、MPI、JEM、SV Probe、TSE、Feinmetall、Wentworth、Korea Instrument |
| RF/photonic probe | FormFactor/Cascade、MPI、GGB Industries、SUSS MicroTec、Keysight probe solutions、Wentworth、TeraView/optical specialty vendors |
| Probe station/prober | TEL、Tokyo Seimitsu/Accretech、MPI、FormFactor、SUSS MicroTec、Semics、Wentworth、Micromanipulator、Electroglas legacy |

### 8.3 Handler、socket、contactor、interface board

| 细分 | 公司 |
|---|---|
| Test handler / pick-and-place | Cohu、Advantest、Chroma、Epson、Hon Precision、TESEC、MCT、Boston Semi Equipment、Exatron、ASMPT |
| High-power thermal handler | Cohu Eclipse、Advantest M4872、Chroma 3100/3200、Aehr Sonoma ecosystem、ESPEC/Thermotron thermal ecosystem |
| Socket/contactor | Cohu、Yamaichi、Enplas、Yokowo、Smiths Interconnect、Leeno、ISC、Ironwood Electronics、Plastronics、TSE、WinWay、Hon Precision、JF Microtechnology |
| DIB / load board / probe interface | Advantest Interconnect Solutions、Technoprobe DIS Tech、FormFactor、WinWay、Harbor/Technoprobe、AT&S、TSE、Cohu、ISC、KYEC/OSAT in-house |

### 8.4 Burn-in、SLT、可靠性和整机测试

| 细分 | 公司 |
|---|---|
| WLBI / wafer-level burn-in | Aehr FOX-XP/FOX-NP/WaferPak、Advantest、Chroma、Cohu、TEL/Accretech prober ecosystem |
| PLBI / HTOL / burn-in systems | Aehr Sonoma/Tahoe、Micro Control、ESPEC、Thermotron、Chroma、Cohu、Advantest、Incal/Aehr、Exatron |
| System-level test | Chroma、Cohu、Advantest、Teradyne、Aehr、Hon Precision、Foxconn Industrial Internet、Quanta/QCT、Wiwynn、Jabil/Celestica/Sanmina test cells |
| Rack burn-in / AI server validation | Foxconn、Quanta/QCT、Wiwynn、Wistron、Inventec、Supermicro、Dell、HPE、ZT Systems/AMD、Jabil、Celestica、Sanmina、Flex、云厂内部测试团队 |

### 8.5 OSAT/测试服务

| 区域 | 公司 |
|---|---|
| 台湾 | ASE/SPIL、KYEC、Powertech/PTI、ChipMOS、Sigurd、Giga Solution、Ardentec、Walton Advanced |
| 中国大陆 | JCET/星科金朋、Tongfu Microelectronics、Huatian、Chipmore、Tianshui Huatian、Forehope、Sanan IC test ecosystem、华岭股份 |
| 韩国 | Hana Micron、LB Semicon、SFA Semicon、Nepes、TESNA/Douzone test ecosystem |
| 东南亚/美国/欧洲 | Amkor、UTAC、Carsem、ASE Malaysia、Intel test/assembly、TSMC backend、Samsung/Amkor Vietnam、ASE/Amkor Arizona expansion |
| 高端 AI 内部测试 | TSMC、Intel、Samsung、SK hynix、Micron、NVIDIA/ODM labs、Google/AWS/Microsoft/Meta internal labs |

### 8.6 高速仪器、协议合规、光电测试

| 细分 | 公司 |
|---|---|
| Oscilloscope/BERT/VNA | Keysight、Rohde & Schwarz、Anritsu、Tektronix、Teledyne LeCroy、NI/Emerson |
| PCIe/CXL/Ethernet protocol analyzer | Teledyne LeCroy、Keysight、Synopsys、Cadence、Rohde & Schwarz、Protocol Insight vendors |
| Optical/CPO/silicon photonics test | Keysight、Anritsu、Viavi、EXFO、FormFactor、MPI、Chroma、Aehr、Coherent/Lumentum internal test、FiconTEC |
| Compliance lab | UNH-IOL、PCI-SIG workshops、Keysight/R&S/Anritsu labs、各大云厂/ODM 内部实验室 |

## 9. 情景模型汇总

### 9.1 核心收入池

| 收入池 | 2026 基准 | 2026 乐观 | 2026 极超 | 2027 基准 | 2027 乐观 | 2027 极超 |
|---|---:|---:|---:|---:|---:|---:|
| 高端 SoC ATE | $12-16B | $16-22B | $22-32B | $15-22B | $22-34B | $34-50B |
| Memory/HBM ATE | $6-9B | $9-14B | $14-20B | $8-13B | $13-22B | $22-35B |
| Probe card + wafer sort interface | $5-8B | $8-12B | $12-18B | $7-12B | $12-20B | $20-32B |
| Handler/socket/DIB/contactors | $6-10B | $10-15B | $15-23B | $9-15B | $15-26B | $26-42B |
| Burn-in/SLT equipment | $4-8B | $8-14B | $14-24B | $8-15B | $15-30B | $30-55B |
| AI/HBM/advanced package 测试服务 | $8-14B | $14-24B | $24-40B | $12-22B | $22-42B | $42-75B |
| Test analytics/SLM/software | $1.2-2B | $2-3.5B | $3.5-6B | $2-4B | $4-8B | $8-14B |

### 9.2 关键假设

| 变量 | 基准 | 乐观 | 极度超预期 |
|---|---|---|---|
| AI 芯片需求 | GB300/Trainium/TPU/MI350/ASIC 稳定放量，Rubin/MI400 2026H2 小量 | Blackwell Ultra 与 ASIC 同时满载，Rubin/MI400 early ramp 顺利 | 2027 需求前置，OpenAI/Meta/Anthropic/Google/AWS 抢测试产能 |
| HBM | HBM3E 主力，HBM4 2026H2 NPI | HBM4 验证顺利，测试订单 2026H2 明显 | HBM4 供给好于预期但测试更紧，probe/test ASP 上行 |
| Test time | AI SoC test time 上升 20-50% | Adaptive test 抵消部分，但 coverage 继续上升 | field reliability 要求极严，burn-in/SLT 时间显著拉长 |
| SLT/burn-in | 高端 AI package 逐步标配 | 客户因报废成本接受更多 WLBI/PLBI | 大客户预订测试 floor，测试服务涨价 |
| 国产替代 | 中国高端 ATE/probe 逐步补位 | 国产 AI 芯片量增带来本土测试订单 | 出口管制加剧，国产替代溢价上升 |

## 10. 风险与反共识观点

### 10.1 最大风险

1. AI capex ROI 被审视，GPU/ASIC 订单递延，测试设备订单存在 1-2 季度波动。
2. HBM/CoWoS/ABF 任一瓶颈未解决时，测试设备虽有订单但客户验收和装机可能延后。
3. 高端 ATE 2026 增长太快，若客户 2027 消化库存，收入会周期性回落。
4. SLT/burn-in 产能扩张重资产，若客户自建/ODM 内化，独立设备和服务商收入分配可能变化。
5. 国产替代长期确定，但短期高端技术差距和出口限制会造成订单兑现不稳定。

### 10.2 可能违背市场共识的洞见

1. **测试行业的 beta 可能比先进封装更滞后但更持久。** 先进封装产能一旦扩出来，瓶颈会向 KGD、test time、burn-in 和 field reliability 迁移。
2. **HBM probe/test 是 HBM 投资里被低估的乘数。** 市场盯 HBM ASP，但 HBM4 的 I/O、堆叠和 KGD 要求会让 probe card 和 memory tester 获取超额增长。
3. **SLT 不是低毛利后段服务，而是 AI package 的保险费。** 当 package 价值足够高，客户会为更长测试时间和更强热控付费。
4. **测试数据软件会成为长期最高毛利层。** ATE/probe/SLT 硬件增长快，但长期定价权会部分迁移到能缩短 test time、预测失效和打通 wafer-to-field 数据的系统。
5. **CPO 测试的收入曲线会晚于订单曲线。** 2026 收入小，但一旦光 I/O/CPO 进入 AI switch 或 XPU，测试方法和设备认证会提前 4-8 个季度卡位。

## 11. 主要来源

| 类别 | 来源 |
|---|---|
| 项目内芯片路线 | `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md` |
| Advantest 财报 | [Advantest FY2025 Consolidated Financial Results](https://www.advantest.com/en/news/2026/a81o6o0000000hgw-att/E_FR_FY2025_FN.pdf) |
| Advantest 产品 | [Pin Scale 5000B / V93000 EXA Scale](https://www.advantest.com/en/news/2026/20260422.html), [SEMICON Southeast Asia 2026 showcase](https://www.advantest.com/en/news/2026/20260428.html) |
| Teradyne | [Teradyne Reports First Quarter 2026 Results](https://investors.teradyne.com/news-events/press-releases/detail/440/teradyne-reports-first-quarter-2026-results) |
| FormFactor | [FormFactor Reports 2026 First Quarter Results](https://investors.formfactor.com/news-releases/news-release-details/formfactor-inc-reports-2026-first-quarter-results), [FormFactor Q1 2026 10-Q segment data via SEC filing mirror](https://www.stocktitan.net/sec-filings/FORM/10-q-formfactor-inc-quarterly-earnings-report-fd4f2595365c.html) |
| Technoprobe | [Technoprobe FY2025 results press release](https://www.technoprobe.com/wp-content/uploads/2026/03/PR-FY-2025_.pdf), [Technoprobe CMD 2025](https://www.technoprobe.com/wp-content/uploads/2025/04/Technoprobe-CMD2025.pdf), [WinWay/MS Sun TPEG agreement](https://www.technoprobe.com/wp-content/uploads/2025/12/PR-Strategic-Agreement.pdf) |
| Cohu | [Cohu Q1 2026 Results](https://ir.cohu.com/news-releases/news-release-details/cohu-reports-first-quarter-2026-results), [Cohu $30M HPC follow-on orders](https://ir.cohu.com/news-releases/news-release-details/cohu-announces-30-million-follow-orders-high-performance) |
| Aehr | [Aehr FY2026 Q3 SEC filing exhibit](https://www.sec.gov/Archives/edgar/data/1040470/000165495426003310/aehr_ex991.htm), [Aehr FY2026 Q2 release](https://www.aehr.com/2026/01/aehr-test-systems-reports-fiscal-2026-second-quarter-financial-results-and-reinstates-guidance-driven-by-improved-visibility-for-ai-processor-and-data-center-semiconductor-test-and-burn-in-systems/) |
| Chroma | [Chroma SLT Solutions, 2025-08](https://www.chromaate.com/en/newsroom/news1041) |
| 宏观半导体 | [Gartner 2026 semiconductor revenue forecast](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) |
| Chiplet/KGD | 项目内 `conference_update\chiplet_summit_2026_update.md`，含 Chiplet Summit 2026、Yole HBM、UCIe/DFT/KGD 材料 |
| PCIe/高速测试 | 项目内 `conference_update\pci_sig_devcon_2026_update.md`，含 PCI-SIG DevCon 2026、PCIe 7/8、optical-aware retimer、compliance/test sources |
| HBM/先进封装交叉验证 | 项目内 `AI服务器_存储_芯片\行业调研_HBM与高带宽内存_2026.md`、`AI服务器_存储_芯片\行业调研_封装基板_中介层与RDL_2026-05-08.md` |
# 行业调研：【特种晶圆代工】

截至日期：2026-05-08  
研究口径：本文把“特种晶圆代工”定义为不以最先进数字逻辑节点为唯一卖点、而以差异化器件/材料/工艺模块定价的晶圆代工：硅光与薄膜铌酸锂光子、III-V-on-Si、SiGe/RF、BCD/高压/PMIC、功率分立/SiC/GaN、eNVM/MRAM/RRAM、MEMS/传感、CMOS+光/热/电源协同工艺。TSMC N3/N2/N4 这类先进逻辑 wafer 只在“配套影响”中引用，不纳入本报告的特种代工 TAM，避免和项目内 AI 芯片、先进封装报告重复计算。

核心立场：对 2026-2027 AI 计算中心建设保持明显乐观。AI 主芯片本身大多仍由先进逻辑 + HBM + CoWoS 决定，但每一个高功率 AI rack 都会外溢出大量“非先进逻辑、但必须可靠放量”的晶圆需求：1.6T/3.2T 光互联、CPO 光引擎、48V/800V 电源控制、BMC/PMIC/MCU、液冷/漏液/压力/流量传感、高压 SiC/GaN 和中国国产替代成熟节点。这正是特种晶圆代工在 2026 年重新获得定价权的原因。

## 0. 结论先行

### 0.1 2026 最有投资价值的四条主线

1. **硅光/光子特种代工从“小众平台”变成 AI 光互联产能瓶颈。** Tower 2026 年 2 月宣布与 NVIDIA 推进 1.6T 数据中心光模块，并在 2025 年报中披露 SiPho/SiGe 累计 $920M 投资、2026 年底目标 SiPho wafer starts 超过 2025Q4 出货 run-rate 的 5 倍，且超过 70% 产能已被预留或正在预留至 2028 年。GF 2025 年 11 月收购 AMF，称成为收入口径最大的 pure-play silicon photonics foundry；GF 2026Q1 又在 OFC 推出 SCALE CPO 生态和 200G/lane silicon photonic receiver 合作。UMC/HyperLight/Wavetek 2026 年 3 月把 TFLN chiplet 平台推向 6 英寸 + 8 英寸高量制造。TSMC 年报则把 COUPE/CPO 指向 2026 量产。

2. **成熟节点功率/模拟代工由“周期复苏”升级为 AI power bottleneck。** AI rack 从 48V power shelf 走向 800VDC/HVDC，拉动 BCD、hot-swap/eFuse、digital power MCU、isolated sensing、BMIC、MOSFET/IGBT、SiC/GaN。TrendForce 2026 年多次强调 AI server power IC 推高 8 英寸代工稼动率和价格；DRAMeXchange/TrendForce 5 月称全球 top 10 8 英寸 foundry 平均稼动率 2026 年接近 90%，1H27 仍高于 80%。

3. **特种代工的定价权来自“客户验证 + PDK + 产能预留”，不是单纯 wafer capacity。** 硅光、SiGe、BCD、eNVM、MEMS、SiC/GaN 的切换成本远高于普通成熟逻辑：客户要重做版图、光电协同、封装、可靠性、软件/固件、系统认证。Tower 的客户预付款锁产能、UMC 的 22nm 平台 50+ 客户 tape-out、GF 的 SiGe oversubscription、X-FAB 的数据中心电源管理 design win 都是信号。

4. **2026 主流技术是“成熟特种平台极限放大”，2027 弹性来自 CPO/TFLN/III-V-on-Si/800VDC/GaN。** 2026 确定放量的是 1.6T pluggable silicon photonics、SiGe/driver/TIA、BCD/PMIC、8 英寸功率模拟、SiC 数据中心电源；CPO、TFLN、3.2T、vertical GaN、photonic interposer 和 MEMS OCS 是 2027-2028 弹性。

### 0.2 总量判断

以下是 AI 数据中心相关的特种晶圆代工/工艺服务收入池，不含完整光模块、完整功率器件系统收入，也不含 GPU/ASIC 主 die 和 HBM 销售额。

| 收入池 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 基准 | 2027 乐观 | 2027 极度超预期乐观 |
|---|---:|---:|---:|---:|---:|---:|
| AI 相关特种晶圆代工合计 | $18B-28B | $28B-42B | $42B-62B | $30B-48B | $48B-75B | $75B-115B |
| 硅光/SiGe/TFLN/III-V-on-Si 光子代工 | $4B-7B | $7B-11B | $11B-17B | $8B-15B | $15B-26B | $26B-42B |
| BCD/HV/PMIC/analog/eNVM 成熟节点 | $9B-15B | $14B-22B | $22B-32B | $14B-24B | $24B-38B | $38B-58B |
| SiC/GaN/power discrete foundry | $2B-4B | $4B-7B | $7B-11B | $5B-10B | $10B-18B | $18B-30B |
| MEMS/传感/微流控/OCS 相关 foundry | $1B-2B | $2B-3B | $3B-5B | $2B-5B | $5B-9B | $9B-16B |

判断：如果 2026 年 AI capex 按项目内乐观口径推进，特种代工不是“先进制程替代品”，而是先进制程的交付放大器。最强 ROIC 不一定在所有 8 英寸厂，而在 **硅光/SiGe 平台、TFLN/III-V 异质集成、AI 电源 BCD/SiC/GaN、光电测试与 PDK/IP**。

## 1. AI 计算中心大规模建设带来的机遇、挑战与技术路径

### 1.1 2026 机遇

| 机遇 | 对特种代工的直接含义 | 关键事实 |
|---|---|---|
| 1.6T 光模块进入规模供货窗口 | SiPh PIC、SiGe driver/TIA、Ge PD、EML/PD、InP-on-Si、TFLN modulator 都需要特种工艺 | OFC 2026 本地报告引用 Cignal AI：2026 年 1.6TbE 模块出货超过 500 万只；1.6T 2026E 模块收入约 $7B-10B |
| CPO/CPX/NPO 从展示进入生态 | CPO 需要 wafer-level optical probing、fiber attach、ELS、photonic engine、热/机械/可维护性工艺 | NVIDIA Spectrum-X Photonics 2026H2；GF SCALE；TSMC COUPE/CPO 目标 2026 量产 |
| 48V AI rack 变成主流 | 0.18um/90nm/40nm BCD、hot-swap、eFuse、PMBus、digital power MCU、BMIC 放量 | TSMC 0.18um Gen-2 BCD 扩到 100V 支持 AI server 48V power；X-FAB Q1 提到 180nm/110nm BCD-on-SOI 数据中心 design wins |
| 800VDC/HVDC 进入新建 AI factory 设计 | 650V/1200V SiC/GaN、isolated sensing、solid-state breaker、arc detection、HV gate driver 提前设计导入 | 项目内 800VDC 报告显示 ABB/Eaton/Delta/Infineon/onsemi/ST/Renesas/Navitas 均在 2025-2026 推 AI data center 800V 架构 |
| BMC/PMIC/MCU 从小料变成交付瓶颈 | 40/55/90/110/180nm mixed-signal、eNVM/MRAM/RRAM、secure MCU、SiP 配套 | 项目内 BMC/MCU 报告引用 TrendForce/The Register：PMIC 与 BMC 交期拖慢 2026 服务器预测 |
| 中国国产替代 | SMIC/Hua Hong/士兰/华润微/积塔/粤芯等成熟节点承接电源、MCU、模拟、功率分立 | Hua Hong 2025Q4 Analog & PM 同比 +40.7%，Embedded NVM +31.3%，12 英寸收入占比升至 61.7% |

### 1.2 2026 挑战

| 挑战 | 为什么难 | 对利润率/交付的影响 |
|---|---|---|
| 光子工艺良率和测试 | 光损耗、相位漂移、耦合、热漂移、偏振、Ge PD 暗电流、modulator bandwidth 都会导致系统性能波动 | wafer-level optical test 和 KGD 价值上升；低良率会推高 ASP，但拖慢交付 |
| 1.6T/3.2T 多路线并行 | SiPh、EML、InP、VCSEL、TFLN、III-V-on-Si 同时存在，客户不会押单一路线 | 工艺平台和 PDK 粘性强，但错误路线会有空置产能风险 |
| 8 英寸 mature-node 结构性紧张 | TSMC/Samsung 减少部分 8 英寸成熟节点，AI power IC、工业/汽车恢复同时抢产能 | 价格上行更可能发生在高压/模拟/功率，而不是普通低端逻辑 |
| BCD/功率器件可靠性 | AI rack 对 uptime、热循环、电源瞬态要求严，高压器件失效成本远高于消费电子 | 认证周期长，已认证供应商可定价 |
| 材料瓶颈 | SOI/HR-SOI、SiC substrate/epi、GaN engineered substrate、TFLN wafer、InP/GaAs epitaxy、低损耗介质材料都不是无限供给 | 上游材料商可能截留大部分利润；foundry 要通过长期锁料保障交付 |
| 封装耦合 | CPO/TFLN/III-V-on-Si 不止是 wafer，光纤连接、ELS、thermal、socket、repairability 都决定量产 | 特种 foundry 必须和 OSAT/光模块/交换芯片客户共设工艺窗口 |
| 地缘与客户多源 | CSP 想要美国/新加坡/台湾/欧洲/中国多源，但每条特种工艺多源都要重新 qual | 多地布局的 GF/Tower/UMC/VIS/X-FAB 具备溢价 |

### 1.3 2026-2027 出货量最大 AI 平台对特种代工的拉动

下表的芯片排序沿用项目内 AI 芯片研究，不重新外搜“出货量最大 10 款”。

| AI 平台 | 主技术路径 | 对特种晶圆代工的拉动 | 2026 最可能放量子方向 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | TSMC 4NP + HBM3E + NVLink/NVL72 + 液冷 | 1.6T scale-out optics、SiPh/SiGe、48V power PMIC、BMC/MCU、温度/漏液传感 | 1.6T pluggable、SiGe driver/TIA、BCD/PMIC |
| AWS Trainium2 | 自研 ASIC + HBM + NeuronLink/EFA | AWS/EFA 网络光模块、power shelf、BMC/secure control、PMIC | 800G/1.6T 光模块与成熟电源 IC |
| Google TPU v7 Ironwood | 推理优先 TPU + HBM + TPU pod/AI Hypercomputer | Google 光网络、OCS、800G/1.6T 模块、TFLN/SiPh 期权 | 800G+ 光模块，OCS/MEMS 观察 |
| NVIDIA B200/GB200 | Blackwell 首代 rack-scale | 同 GB300，但更多为存量订单和成熟供应链 | 成熟 SiPh/SiGe 与 48V PMIC |
| Huawei Ascend 910C/950 | 国产先进节点 + 超节点互连 + 国产 HBM 路线 | 中国 mature node power/MCU、国产光模块、国产功率分立/模拟 | Hua Hong/SMIC/华润微/士兰系成熟节点 |
| Cambricon MLU590/690 | 国产 AI 加速器 + HBM/OAM | OAM 电源、BMC、光模块、国产 eNVM/MCU | 28/40/55/90nm 混合信号与电源 |
| AMD MI350/MI355 | CDNA + HBM3E + UBB/PCIe/OAM | 第二供应源拉动 optics、PMIC、BMC、液冷传感 | 48V power 与光互联 |
| AWS Trainium3 | 3nm + HBM3E + 144-chip UltraServer | 更高 rack 密度推动 power IC、光互联和 burn-in 控制 | 2026 导入，2027 放量 |
| Meta MTIA 300/400/450/500 | Broadcom XPU + OCP rack + GenAI inference | Meta/Broadcom Ethernet optics、CPO 期权、PMIC/MCU | 自研 ASIC 量产带来的 optics 外溢 |
| Microsoft Maia 200 | TSMC 3nm + 216GB HBM3E + 闭环液冷 | Azure 内部推理 rack 的 power/thermal/optics/sensor | 液冷传感 + 48V power + 光互联 |

### 1.4 新技术成熟和放量节奏

| 技术 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 基准/乐观/极超 | 2026 最可能性 |
|---|---|---|---|---|---|
| 1.6T silicon photonics / optical PIC | 规模导入，受 200G/lane、DSP、测试约束 | 大客户锁产能，Tower/GF/TSMC/UMC 扩产顺利 | 1.6T 新增 AI 集群默认，短缺延续 | 2027 成为新增主流，3.2T 开始 qual | 极高 |
| SiGe BiCMOS driver/TIA | GF/Tower 等产能紧，支持 200G/lane | 产能扩张仍跟不上 | oversubscribed 到 2027，涨价 | 2027 400G/lane 继续抬高性能门槛 | 高 |
| CPO/CPX/socketed optical engine | NVIDIA/GF/TSMC/Broadcom/Coherent 生态 pilot | 2026H2 高端 switch 试点 | 客户提前锁 2027 CPO 工程产能 | 2027 小批量，高端 AI switch 渗透 5%-15% | 中 |
| TFLN photonics | UMC/HyperLight 6/8 英寸 HVM 平台建立，收入小 | 1.6T/3.2T modulator 客户 qual 加快 | 2026H2 出现大客户预付款 | 2027 进入 1.6T/3.2T 光模块和 CPO 供应链 | 中高 |
| III-V-on-Si / InP-on-Si | OpenLight/Tower PH18DA 有 volume production orders 线索 | 激光集成 PIC 用于 800G/1.6T | 3.2T beta 提前转量产 | 2027 成为 CPO/3.2T 重要路线 | 中 |
| BCD/HV PMIC | 48V AI rack 主力，8 英寸/12 英寸成熟节点紧 | wafer 价格继续上行 | PMIC/BMC 成为服务器交付硬约束 | 800VDC 控制带来二次增长 | 极高 |
| SiC power foundry | 数据中心 power + EV + renewable 共振，X-FAB WBG 快速增长 | 1200V SiC 被 800VDC/SST 提前 design-in | 数据中心从 EV 之后成为第二主需求 | 2027 800VDC/solid-state transformer 试点放量 | 中高 |
| GaN-on-Si/vertical GaN | 650V/1200V 样品和项目开发，收入小 | 200mm engineered substrate 进客户验证 | AI PSU 高密度需求迫使提前采用 | 2027 小量，2028-2029 才大规模 | 中低但期权大 |
| MEMS/OCS/微流控/传感 | 液冷、OCS、压力/流量/漏液传感增长 | Google/OCS 生态扩散 | 2027 前客户把 MEMS switch 纳入 AI fabric | 2027 高端集群小批量，2028 放量 | 中 |

## 2. 已开始放量的关键产品：市场规模、渗透率与利润率

口径：未来 3 个月指 2026-05 至 2026-08；未来 1 年指 2026-05 至 2027-05；未来 2 年指 2026-05 至 2028-05。市场规模为全球 AI 数据中心相关的特种代工/工艺服务收入池，不是下游成品收入。

| 已放量产品/技术 | 当前事实基础 | 未来3个月市场规模 B/O/X | 未来1年市场规模 B/O/X | 未来2年市场规模 B/O/X | 渗透率路径 | 毛利率/利润率假设 B/O/X |
|---|---|---:|---:|---:|---|---|
| 1.6T/800G silicon photonics PIC 与 optical engine wafer | Tower/NVIDIA 1.6T；GF/AMF；TSMC COUPE；OFC 2026 多厂展示 | $0.7-1.2B / $1.2-1.8B / $1.8-2.8B | $3-5B / $5-8B / $8-12B | $8-15B / $15-25B / $25-40B | AI 高速光模块中 SiPh/PIC wafer 价值渗透 2026 20%-35%，2027 30%-50%，CPO 导入后继续升 | 35%-50% / 45%-60% / 55%-70%；若产能预付款和独占 PDK，实际项目回报更高 |
| SiGe BiCMOS / high-speed analog drivers, TIAs, clock/RF | GF 管理层称 SiGe 为增长引擎且 capacity oversubscribed into 2027；Tower 持续投 SiGe | $0.25-0.50B / $0.50-0.80B / $0.80-1.20B | $1.2-2.2B / $2.0-3.5B / $3.5-5.0B | $3-6B / $5-9B / $9-14B | 200G/lane 和 400G/lane 光链路 attach rate 2026 50%-70%，2027 70%+ | 35%-50% / 45%-58% / 55%-65%；关键是 fT/fMAX、噪声和客户共设计 |
| BCD/HV PMIC/hot-swap/eFuse/digital power wafer | TSMC 0.18um BCD 100V 支持 AI servers；X-FAB BCD-on-SOI data center design wins；VIS/PSMC/SMIC 涨价 | $1.0-2.0B / $1.8-3.0B / $3.0-4.5B | $5-9B / $8-14B / $14-22B | $10-20B / $18-32B / $32-50B | 高端 AI rack 48V power IC attach 2026 60%-80%，2027 80%+；800V 控制 2027 起 | 25%-38% / 35%-45% / 45%-55%；8 英寸紧缺和客户认证带来涨价 |
| eNVM/MRAM/RRAM/secure MCU/BMC control wafers | GF Auto Grade 1 eMRAM on FDX；TSMC MRAM/RRAM 车规/消费级 qual；AI rack secure control 增长 | $0.25-0.45B / $0.45-0.75B / $0.75-1.1B | $1.2-2.2B / $2.0-3.5B / $3.5-5.5B | $3-7B / $6-11B / $11-18B | BMC/MCU/secure control 中 eNVM/MRAM/RRAM 渗透 2026 15%-25%，2027 25%-40% | 30%-45% / 40%-55% / 50%-65%；安全认证和固件绑定提升定价 |
| 8英寸/12英寸 analog/mixed-signal 成熟特种节点 | UMC 22/28nm 占 34%，22nm 占 14%；VIS Q2 指引 ASP +2%-4%；Hua Hong 稼动率 >100% | $2.5-4.0B / $4.0-6.0B / $6.0-8.5B | $10-16B / $16-24B / $24-36B | $20-36B / $36-58B / $58-85B | AI server power/management/optics 周边成熟节点需求占比从 2026 低双位数升至 2027 中高双位数 | 22%-35% / 30%-42% / 40%-52%；普通成熟逻辑低，差异化 HV/analog 高 |
| SiC power foundry / power discrete wafer | X-FAB 2026Q1 宽禁带收入 $15.1M、同比 +152%，SiC wafer shipments 14,300 片、同比 +195% | $0.20-0.40B / $0.40-0.70B / $0.70-1.0B | $1.0-2.0B / $2.0-3.5B / $3.5-5.5B | $3-6B / $6-10B / $10-18B | 数据中心 PSU/SST/UPS 中 SiC 2026 仍低个位数，2027 5%-15%，800VDC 试点更高 | 20%-35% / 30%-45% / 40%-55%；substrate/epi 分走利润，良率领先者溢价大 |
| MEMS/传感/微系统 foundry | X-FAB microsystems & photonics Q1 $33.7M、同比 +42%；TSMC PiezoMEMS 被验证用于 HPC AI cooling | $0.15-0.30B / $0.30-0.55B / $0.55-0.85B | $0.8-1.5B / $1.5-2.8B / $2.8-4.5B | $2-5B / $5-9B / $9-16B | 高密 AI rack 的压力/流量/漏液/振动/OCS 传感 attach 2026 30%-50%，2027 50%-75% | 25%-40% / 35%-50% / 45%-60%；定制 MEMS/NRE 可更高 |

增长区间汇总：基准情景下未来一年 AI 相关特种代工收入池同比 +25%-45%；乐观情景 +50%-80%；极度乐观情景 +90% 以上。硅光和 BCD/HV 是 2026 可兑现双主线，SiC/GaN、TFLN、CPO 是 2027 弹性。

## 3. 在研/导入期关键产品：市场规模、渗透率与利润率

| 在研或早期导入产品/技术 | 2026 阶段 | 未来3个月市场规模 B/O/X | 未来1年市场规模 B/O/X | 未来2年市场规模 B/O/X | 渗透率路径 | 利润率假设 B/O/X |
|---|---|---:|---:|---:|---|---|
| CPO/CPX/socketed optical engine foundry | NVIDIA 2026H2，GF SCALE，TSMC COUPE，Open CPX MSA | $0.10-0.25B / $0.25-0.50B / $0.50-0.90B | $0.8-1.8B / $1.8-3.8B / $3.8-7B | $4-9B / $9-18B / $18-35B | AI switch 中 CPO 2026 <5%，2027 5%-15%，2028 15%-30% | 初期项目毛利波动大；成熟后 foundry/engine 45%-65%，系统责任会压低 |
| TFLN photonics chiplet | UMC/HyperLight/Wavetek 6/8 英寸 HVM，Jabil 做系统部署路径 | $50-150M / $150-300M / $300-600M | $0.3-0.8B / $0.8-1.8B / $1.8-3.5B | $1.5-4B / $4-9B / $9-18B | 1.6T/3.2T modulator 中 2026 低个位数，2027 5%-15%，2028 15%-30% | 35%-55% / 45%-65% / 60%-75%；若 400G/lane 低功耗优势被验证，溢价高 |
| III-V-on-Si laser-integrated PIC | OpenLight/Tower PH18DA volume orders；3.2T beta 样品 2026Q4 线索 | $0.10-0.25B / $0.25-0.50B / $0.50-0.90B | $0.5-1.3B / $1.3-2.8B / $2.8-5B | $2-6B / $6-12B / $12-24B | integrated laser PIC 在高端 optical engine 2026 <10%，2027 10%-25% | 35%-55% / 45%-65% / 60%-75%；异质集成良率是核心风险 |
| 400G/lane / 3.2T optical wafer platforms | OFC 2026 多为样机、evaluation board、alpha/beta | $50-150M / $150-300M / $300-600M | $0.4-1.0B / $1.0-2.5B / $2.5-5B | $3-8B / $8-18B / $18-35B | 3.2T 2027 小批，2028 放量；400G/lane 先进入器件/测试 | 40%-60% / 50%-70% / 65%+；早期 NRE 和测试费高 |
| 650V/1200V GaN-on-Si / vertical GaN foundry | X-FAB Q1 交付 1200V GaN 原型，下一代 vertical GaN 客户项目启动 | <$50M / $50-120M / $120-250M | $0.1-0.4B / $0.4-0.9B / $0.9-1.8B | $0.7-3B / $3-7B / $7-14B | AI PSU/800VDC 中 2026 试样，2027 小批，2028 后才大规模 | 早期低到负毛利；成熟后 35%-55%，高压可靠性验证成功者更高 |
| MEMS OCS / optical switching | Google OCS 生态、MEMS switch、AI fabric 能耗压力 | $30-100M / $100-250M / $250-500M | $0.2-0.7B / $0.7-1.8B / $1.8-3.5B | $1-4B / $4-10B / $10-20B | 2026 <5% 高端集群，2027 5%-15%，2028 若架构胜出 20%+ | 30%-50% / 40%-60% / 55%-70%；系统软件和运维分走价值 |
| PiezoMEMS/微流控冷却器件 | TSMC 年报称 PiezoMEMS 平台用于 HPC AI cooling 应用验证；X-FAB AlScN production line | $20-80M / $80-180M / $180-350M | $0.15-0.5B / $0.5-1.2B / $1.2-2.5B | $0.8-3B / $3-7B / $7-15B | 2026 工程验证，2027 rack thermal sensing/actuation 小量 | 25%-45% / 40%-60% / 55%-70%；可靠性和封装是关键 |
| Photonic interposer / electronic-photonic 3D stack | TSMC COUPE、CPO、CoWoS+optics 方向 | $50-150M / $150-350M / $350-700M | $0.4-1.2B / $1.2-3B / $3-6B | $2-7B / $7-16B / $16-32B | 2027 高端 switch/ASIC 小量，2028 进入更广设计 | 45%-65%；但责任边界跨 foundry/OSAT/模块商 |

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 地区 | 主要公司/产能 | 工艺重点 | 2026 观察 |
|---|---|---|---|
| 台湾 | TSMC、UMC、VIS、PSMC、Wavetek、Episil、台系 OSAT | COUPE/CPO、BCD/HV、22/28nm specialty、TFLN、PMIC/DDIC/CIS、power discrete | TSMC 高端平台最强；UMC 22nm specialty 和 TFLN；VIS 8 英寸 power/PMIC 受 AI server 带动涨价 |
| 美国 | GlobalFoundries Malta/Vermont、Tower 美国、X-FAB Texas、SkyWater、Intel Silicon Photonics | silicon photonics、SiGe、FDX/eMRAM、SiC、aerospace/defense specialty | GF/AMF 后成为 SiPh 核心；美国本土供应链对 CSP 有战略溢价 |
| 新加坡 | GF/AMF、VIS-NXP VSMC、SSMC/Wavetek 生态 | silicon photonics、300mm specialty analog/power、TFLN | AMF 200mm SiPh，GF 计划 300mm 扩展；VSMC $7.8B 300mm fab 2027 起量 |
| 以色列/日本/意大利 | Tower Israel/TPSCo/ST Agrate | SiPh、SiGe、BCD、700V power、CIS/MEMS | Tower 是 1.6T SiPh 最强纯特种 foundry 之一 |
| 欧洲 | X-FAB Germany/France/Belgium、ST、Infineon、Bosch、imec、SMART Photonics、Ligentec | SiC/GaN、MEMS、TFLN/SiN/InP photonics、automotive power | 欧洲在材料/功率/车规和研发强，AI 数据中心带来新需求 |
| 中国大陆 | Hua Hong/HHGrace、SMIC、华润微、士兰微、积塔、粤芯、晶合集成、燕东微、中芯集成等 | eNVM、power discrete、Analog & PM、BCD、MCU、CIS/DDIC、国产 PMIC | 国产 AI 集群和出口管制推动本土 mature specialty 满载与涨价 |
| 韩国 | Samsung Foundry/SEMCO、DB HiTek、SK key materials | foundry/advanced packaging、analog/BCD、substrate | DB HiTek 是模拟/BCD 重要 foundry；Samsung 侧更偏先进逻辑+封装+HBM |

### 4.2 供给瓶颈

1. **8 英寸高压/模拟产能**：AI power IC 与传统汽车/工业共享产线，新增产能慢，设备和老工艺人才稀缺。
2. **SOI/HR-SOI/Photonics-SOI wafer**：硅光、RF-SOI、SiPh 对 substrate 电阻率、厚度、缺陷和热氧化质量要求高。
3. **TFLN wafer 与 bonding/etch 工艺**：薄膜铌酸锂高速低功耗，但量产工具链和 wafer supply 仍早期。
4. **SiC substrate/epi**：SiC 仍受 6/8 英寸 substrate、epi 缺陷、晶圆成本和良率影响，foundry 毛利容易被上游材料吞噬。
5. **GaN engineered substrate 和高压可靠性**：1200V GaN/vertical GaN 要跨越 dynamic Rds(on)、陷阱、击穿、热和长期可靠性。
6. **wafer-level optical testing**：1.6T/3.2T/CPO 需要光电同步 probe、fiber attach 可重复性、温控和高吞吐测试，测试产能可能比 wafer starts 更紧。
7. **PDK/IP/EDA maturity**：光子 PDK、SiGe compact model、BCD HV device model、electro-thermal co-simulation 不成熟会拖慢 tape-out。
8. **客户 qual 与可靠性认证**：CSP、车规、工业和数据中心安全认证周期长，foundry 一旦进入合格名单就很难被替换。
9. **封装和连接器协同**：CPO 需要与 SENKO/Corning/EXFO、OSAT、交换芯片、ELS、冷板一起定义可维护性，单独 wafer 不能交付系统。
10. **特殊化学品/气体与能源成本**：GF Q1 2026 管理层已提示供应成本和地缘带来的 margin 压力；特种工艺批量小，更难摊薄。
11. **人才**：SiPh、SiGe、BCD、MEMS、SiC/GaN 都是经验曲线工艺，不能靠买设备快速复制。
12. **地缘和出口管制**：中国先进节点与 HBM 受限会增加本土特种需求；美国/欧洲客户则更偏好本土或可信供应链。

### 4.3 成本拆分和毛利决定因素

| 产品 | 单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| Silicon photonics PIC | SOI wafer 10%-20%；front-end process 30%-45%；optical/electrical test 15%-25%；yield loss 10%-20%；PDK/NRE/工程服务 5%-15% | 光损耗、耦合良率、modulator/PD 性能、客户锁定、wafer-level test | 预付款锁产能、NRE、工程 tape-out、按 wafer + test + yield premium 定价 |
| SiGe driver/TIA | wafer/process 40%-55%；mask/NRE 5%-10%；test 15%-25%；yield/trim 10%-20% | fT/fMAX、噪声、带宽、功耗、模型准确性 | 光模块/交换芯片客户为 200G/400G lane 性能付溢价 |
| BCD/HV PMIC | wafer/process 45%-60%；HV/eNVM module 10%-20%；probe/test 10%-20%；qualification 5%-10% | 电压等级、Rdson、集成度、认证、长期供货 | wafer price hike + LTA 续签 + 客户转换成本 |
| SiC MOSFET/diode foundry | substrate/epi 35%-55%；device fab 20%-35%；test/yield 10%-20%；packaging 15%-25% | substrate 成本、缺陷密度、良率、可靠性 | 上游材料涨价先传导；高可靠 AI power 项目愿意预付 |
| GaN power | engineered substrate 20%-40%；epi/device 30%-45%；reliability/test 15%-25%；yield loss 10%-25% | dynamic resistance、thermal、击穿、封装寄生 | 初期工程收入 + 客户共研；量产后按功率密度和效率节省定价 |
| MEMS/传感 | wafer process 35%-50%；cap/bonding 15%-25%；calibration/test 20%-35%；packaging 10%-20% | 校准算法、封装应力、长期漂移、客户认证 | 不是按 die 面积定价，而按可靠性、NRE、生命周期和系统集成价值定价 |

毛利判断：普通成熟 foundry 毛利可能只有 20%-30%；但特种工艺如果具备 **客户认证 + PDK/IP + 产能紧缺 + 系统失效风险高**，毛利可上到 40%-60%；早期硅光/TFLN/III-V-on-Si/CPO 项目甚至可用 NRE 和预付款把项目 IRR 做得更高。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分市场 | 头部集中度 | 头部公司 |
|---|---|---|
| AI SiPh/SiGe foundry | 高，前 3-5 家决定高端客户供给 | Tower、GlobalFoundries/AMF、TSMC、Intel Silicon Photonics、UMC/Wavetek、ST |
| TFLN photonics foundry | 早期集中，技术平台未完全标准化 | UMC/Wavetek/HyperLight、Ligentec/EPFL 生态、LioniX/SMART/LN foundry 生态、imec/研发平台 |
| BCD/HV/PMIC foundry | 中高，地域分散但客户认证强 | TSMC、UMC、VIS、Tower、X-FAB、DB HiTek、Hua Hong、SMIC、PSMC、Silan、CR Micro |
| SiC/GaN foundry | 中高，IDM 强、pure-play foundry 少 | X-FAB、Wolfspeed/materials、ST、Infineon、onsemi、ROHM、Episil、Silan、CR Micro、Navitas/Innoscience ecosystem |
| MEMS/传感 foundry | 分散但客户强绑定 | X-FAB、TSMC、Silex Microsystems、Teledyne DALSA、Bosch、Sony/IDM、Tower、SMIC/Hua Hong 部分平台 |
| 中国特种代工 | 高稼动、政策与国产替代驱动 | Hua Hong、SMIC、华润微、士兰微、积塔、粤芯、晶合集成、中芯集成 |

### 5.2 可量化壁垒：为什么能定价

| 壁垒 | 量化/事实线索 | 为什么能定价 |
|---|---|---|
| 客户认证周期 | 光模块/CPO/车规/电源可靠性通常需要 6-24 个月 | 客户不能为了 5%-10% wafer 价差冒系统失效率风险 |
| PDK 与模型 | TSMC 2025 年已提供约 4,000 PDK、58,000+ tech files；特种 PDK 更依赖实测 | 客户版图、器件模型、仿真和 IP 被平台锁定 |
| 产能预留 | Tower SiPho >70% 总产能已预留或正在预留到 2028 | 预付款让客户锁交付，foundry 获得现金流和价格保护 |
| 光电测试能力 | 1.6T/3.2T 要做 optical + electrical + thermal 测试 | 仅有 wafer starts 不够，测试吞吐和 KGD 决定有效产能 |
| 工艺 know-how | SiPh 光损耗、SiGe 噪声、高压 BCD、SiC/GaN 缺陷都是经验曲线 | 新进入者良率低，短期无法用低价替代 |
| 可靠性责任 | AI rack 断链/失电/过热会造成整柜或整 pod 停机 | 客户愿为高可靠器件和长期供应付溢价 |
| 多地供应 | 美国/新加坡/台湾/欧洲/中国各自有供应安全诉求 | 多地 qualified capacity 本身就是产品 |

### 5.3 价值捕获排序

1. **最高长期 ROIC：光子/SiGe/特种 PDK 平台。** Tower、GF/AMF、TSMC COUPE、UMC/Wavetek TFLN 这类平台一旦进入 1.6T/CPO/3.2T 客户路线，后续 tape-out、NRE、测试和产能预留会形成复利。
2. **高确定性现金流：BCD/HV/PMIC 成熟节点。** 不像先进制程那样 ASP 惊人，但 AI rack 数量、48V/800V、电源瞬态和 BMC/PMIC 交期使其 2026-2027 具备涨价基础。
3. **高赔率：SiC/GaN for AI power。** 2026 收入仍小，但如果 800VDC/固态变压器/1MW rack 进入 2027 设计冻结，1200V SiC 和 GaN 会从 EV 周期转向 AI power 周期。
4. **中期高壁垒：光电测试、探针、PDK/IP、EDA。** 客户规模上来后，测试和模型比 wafer 本身更难短期扩张。
5. **传统普通成熟代工 ROIC 较低。** 若没有 HV/analog/SiPh/SiC/MEMS 差异化，只靠 8 英寸普通逻辑涨价，周期性风险较大。

## 6. 2026 关键变化：3 个拐点与最可能放量方向

### 拐点一：1.6T 光互联把 silicon photonics 产能拉成硬约束

Tower/NVIDIA 1.6T、Tower $920M SiPho/SiGe 扩产、GF/AMF、GF SCALE、TSMC COUPE、UMC/HyperLight TFLN 同时出现，说明 2026 年不是“硅光概念年”，而是客户开始抢 foundry capacity 的第一年。

最可能放量：1.6T pluggable SiPh PIC、SiGe driver/TIA、wafer-level optical testing、fiber attach、200G/lane photonics。

### 拐点二：AI power IC 使 mature-node foundry 价格重估

2026 年 AI server 的限制从 GPU/HBM/CoWoS 扩散到 PMIC、BMC、power MCU、hot-swap、BMIC、SiC/GaN。VIS Q2 2026 指引 wafer shipments +11%-13%、ASP +2%-4%、gross margin 31%-33%；TrendForce/DRAMeXchange 称 8 英寸 foundry 稼动率 2026 接近 90%，AI power IC 是核心推力之一。

最可能放量：0.18um/90nm/40nm BCD、22/28nm specialty、power MCU、eNVM secure control、AI rack PMIC。

### 拐点三：特种 foundry 从 spot 订单转向预付款/长约

Tower 披露超过 70% SiPho 产能被预留或预留中；UMC 22nm 2026 年底预计 50+ 客户完成 tape-out；GF 2026Q1 design wins 同比提升并强调 silicon photonics/SiGe；X-FAB 尽管汽车疲软，但数据中心电源管理和 WBG 明显增长。这说明客户正在把特种工艺当成战略产能，而不是普通代工服务。

最可能放量：客户共设产线、NRE、multi-year LTA、capacity reservation、工程 tape-out。

## 7. 2027 关键变化：3 个拐点与最可能放量方向

### 拐点一：CPO/TFLN/III-V-on-Si 从 pilot 转小批量

2027 年若 1.6T 新增 AI 集群成为默认、3.2T 进入客户 qual，CPO/CPX、TFLN modulator、III-V-on-Si integrated laser PIC 会从演示进入小批量。2027 不是 CPO 替代所有 pluggable 的年份，但会是高端 AI switch 和 co-packaged optical engine 的设计胜出年。

最可能放量：CPO optical engine、ELS、TFLN high-speed modulator、InP-on-Si laser PIC、400G/lane test。

### 拐点二：800VDC/1MW rack 把 SiC/GaN 与 BCD/HV 推上第二曲线

2026 主流还是 48V；2027 新建 AI factory 会更积极把 800VDC、solid-state breaker、hot-swap、isolation sensing、arc detection、SST 放入设计。若 Rubin Ultra/Kyber、MI400/MI455X、TPU8、Trainium4 带动 500kW-1MW rack，1200V SiC 和高压 GaN 的收入弹性会显著高于传统 EV 单一周期。

最可能放量：1200V SiC、650/1200V GaN、HV gate driver、isolated sensing、solid-state protection controller。

### 拐点三：区域化供应链形成多核心，而不是单一台湾成熟节点

GF/AMF 新加坡 + 美国、VIS/NXP VSMC 新加坡、Tower 日本/美国/以色列/意大利、X-FAB 美国/德国/法国/马来西亚、UMC/TFLN 台湾，使特种代工供应链更分散。2027 重要的不是谁有最低 wafer price，而是谁能提供“可信地缘 + 已验证工艺 + 可扩产测试 + 客户工程”。

最可能放量：美国/新加坡 photonics capacity、欧洲 SiC/GaN/MEMS、中国国产 power/MCU/analog、跨区域 second source。

## 8. 头部公司与细分清单

### 8.1 硅光、TFLN、III-V-on-Si、CPO

| 环节 | 公司 |
|---|---|
| Silicon photonics foundry | TSMC、GlobalFoundries、Advanced Micro Foundry、Tower Semiconductor、Intel Silicon Photonics、UMC/Wavetek、STMicroelectronics、AIM Photonics、SkyWater、Silex Microsystems、imec pilot lines |
| TFLN/SiN/InP photonics foundry | UMC/Wavetek/HyperLight、Ligentec、LioniX、SMART Photonics、imec、CEA-Leti、VTT、Applied Nanotools、CompoundTek |
| III-V-on-Si / integrated laser PIC | OpenLight、Tower PH18DA、Ayar Labs、Celestial AI、Lightmatter、POET、Coherent、Lumentum、Broadcom ecosystem |
| CPO/ELS/optical engine | NVIDIA、Broadcom、Marvell、Coherent、Lumentum、Cisco/Acacia、Ciena、Nokia、Molex、Samtec、SENKO、Corning、EXFO、Fabrinet |
| 光模块/系统客户 | Innolight、中际旭创、Eoptolink、新易盛、Coherent、Lumentum、Fabrinet、Flex、Jabil、Lessengers、POET、AOI、Source Photonics、Hisense Broadband |
| 光子设计/材料 | Lightwave Logic、HyperLight、LightIC、Siluxtek、Xscape Photonics、Ayar Labs、Celestial AI、Lightmatter、Avicena、Ansys Lumerical、Luceda/IPKISS、Synopsys/Cadence photonics flows |

### 8.2 BCD/HV/PMIC/Analog/eNVM 特种代工

| 环节 | 公司 |
|---|---|
| 全球 foundry | TSMC、UMC、VIS、Tower、GlobalFoundries、X-FAB、DB HiTek、Samsung Foundry、Intel Foundry、PSMC、Nexchip |
| 中国 foundry | Hua Hong/HHGrace、SMIC、华润微、士兰微、积塔半导体、粤芯、晶合集成、中芯集成、燕东微、上海先进、比亚迪半导体 |
| 主要芯片客户/IDM | TI、ADI、Infineon、STMicroelectronics、Renesas、NXP、onsemi、Microchip、MPS、Vishay、Rohm、Power Integrations、Nuvoton、Richtek、uPI、Silergy、矽力杰、圣邦微、南芯、杰华特 |
| eNVM/MRAM/RRAM | TSMC、GF、UMC、Hua Hong、SMIC、Samsung、Tower、Everspin、Avalanche、Weebit Nano、Rambus/SST/Microchip SuperFlash |

### 8.3 SiC/GaN 与功率分立 foundry

| 环节 | 公司 |
|---|---|
| SiC foundry / IDM | X-FAB、Wolfspeed、STMicroelectronics、Infineon、onsemi、ROHM、Sanan IC、Silan、CR Micro、BYD Semiconductor、Bosch、Fuji Electric、Mitsubishi Electric |
| GaN foundry / IDM | X-FAB、Episil、TSMC GaN licensing ecosystem、GlobalFoundries/TSMC GaN license、Navitas、Innoscience、EPC、Power Integrations、Infineon/GaN Systems、Transphorm、Texas Instruments、ROHM |
| Substrate/epi/equipment | Wolfspeed、Coherent、SK siltron CSS、Soitec、SICC、TankeBlue、IQE、AIXTRON、Veeco、Agnitron、Nuflare、Applied Materials |

### 8.4 MEMS、传感、微流控、OCS

| 环节 | 公司 |
|---|---|
| MEMS foundry | X-FAB、Silex Microsystems、Teledyne DALSA、TSMC、Tower、Bosch、Sony Semiconductor、ST、SMIC MEMS、Hua Hong、MEMSCAP |
| OCS/MEMS optical switch | Google/Apollo ecosystem、Calient、Polatis/HUBER+SUHNER、Coherent、Lumentum、II-VI/Coherent、Nistica/Fujikura、TeraHop |
| 液冷/传感客户 | Sensirion、TE Connectivity、Honeywell、Amphenol、Bosch Sensortec、TDK/InvenSense、Omron、First Sensor、Ametek、Delta、Vertiv、CoolIT、Boyd |

### 8.5 上游材料与测试

| 环节 | 公司 |
|---|---|
| Silicon/SOI/HR-SOI | Soitec、Shin-Etsu、SUMCO、GlobalWafers、Siltronic、SK siltron、Okmetic、Simgui、ZingSemi |
| TFLN/LN/photonic materials | NanoLN、HyperLight ecosystem、Sumitomo/Crystal Technology、G&H、Coherent materials、Corning、AGC、Schott |
| Optical test / ATE | Keysight、VIAVI、EXFO、Teradyne、Advantest、FormFactor、MPI、Chroma、Cohu、Onto Innovation、Camtek |
| Packaging/fiber attach | ASE、Amkor、JCET、PTI、Fabrinet、Jabil、Flex、SENKO、Corning、Molex、Samtec、TE、Amphenol |

## 9. 投资判断与跟踪指标

### 9.1 优先级排序

| 排名 | 方向 | 2026 确定性 | 2027 弹性 | 关键风险 |
|---:|---|---|---|---|
| 1 | Tower/GF/TSMC/UMC 代表的 SiPh/SiGe/TFLN 平台 | 很高 | 很高 | CPO 维护性、1.6T ASP 下行、客户路线分化 |
| 2 | BCD/HV/PMIC/analog mature specialty | 很高 | 高 | 2027 普通成熟节点扩产过快，价格回落 |
| 3 | SiC/GaN for AI power | 中高 | 很高 | 800VDC 节奏慢、材料成本、可靠性验证 |
| 4 | MEMS/OCS/传感/微流控 | 中 | 高 | 架构 adoption 不确定，客户自研 |
| 5 | 中国国产特种代工 | 高 | 中高 | 价格管制、先进设备限制、客户集中 |

### 9.2 未来 6-12 个月最该盯的信号

1. Tower SiPho/SiGe $920M 扩产是否如期 2026Q4 fully qualified，2027 full starts 是否兑现。
2. GF silicon photonics 2026 revenue 是否接近翻倍、2028 是否能接近 $1B+ run-rate。
3. NVIDIA Spectrum-X Photonics/CPO 2026H2 是否真实出货，而不只是展示。
4. UMC/HyperLight TFLN 是否拿到 hyperscaler/Jabil 后续量产订单。
5. 1.6T 模块 2026 出货是否超过 500 万只，2027 订单是否上调到 1,500-2,500 万只。
6. VIS/PSMC/SMIC/Hua Hong 成熟节点涨价是否持续到 2H26。
7. X-FAB WBG revenue 和 SiC wafer shipments 是否继续环比增长，GaN prototype 是否转客户 qual。
8. 800VDC reference design 是否从 ABB/Eaton/Delta/Infineon/ST/onsemi 演示进入 CSP 项目设计冻结。
9. BMC/PMIC lead time 是否继续拖累 AI server 出货。
10. 中国国产 AI 集群拉动本土 PMIC/MCU/功率器件订单是否外溢到 Hua Hong/SMIC/华润微/士兰。

## 10. 关键来源

| 来源 | 关键信息 |
|---|---|
| [TSMC 2025 Annual Report, Business Activities](https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf) | N4C RF、N6 RF+、16MRAM、N12e RRAM、40SOI、40BCD、0.18um BCD 100V 支持 AI servers、COUPE/CPO 目标 2026 量产、PiezoMEMS for HPC AI cooling |
| [TSMC Q1 2026 Quarterly Results](https://investor.tsmc.com/english/quarterly-results/2026/q1) | Q1 revenue $35.90B、gross margin 66.2%、Q2 revenue guide $39.0B-$40.2B、gross margin 65.5%-67.5% |
| [GlobalFoundries Q1 2026 SEC release](https://www.sec.gov/Archives/edgar/data/1709048/000170904826000111/globalfoundries1q2026earni.htm) | Q1 revenue $1.634B、gross margin 27.6%；OFC SCALE/CPO ecosystem、Siluxtek 200G/lane SiPh receiver、Auto Grade 1 eMRAM on FDX |
| [GF acquires Advanced Micro Foundry](https://investors.gf.com/node/10161/pdf) | GF 成为收入口径最大 pure-play silicon photonics foundry；AMF 200mm Singapore，计划随需求扩到 300mm；AI datacenter 光通信需求 |
| [TrendForce: GF SiPh revenue doubling in 2026](https://www.trendforce.com/news/2026/05/07/news-globalfoundries-reportedly-sees-silicon-photonics-revenue-doubling-in-2026-passing-1b-by-2028/) | GF silicon photonics 2026 翻倍、2028 >$1B 线索 |
| [Tower + NVIDIA 1.6T SiPh release](https://ir.towersemi.com/node/16511/pdf) | Tower 支持 NVIDIA networking protocols 1.6T 数据中心光模块，SiPh 平台面向 AI infrastructure |
| [Tower Q4/FY2025 release](https://towersemi.com/wp-content/uploads/2026/02/TSEM_Q4FY_2025_PR_FINALF_isa.pdf) | 2025 revenue $1.57B；$920M SiPho/SiGe 投资；2026Q4 完成安装/qual；2027 full starts；>70% SiPho capacity reserved/pre-reserved to 2028 |
| [Lightwave Logic + Tower PH18](https://www.nasdaq.com/press-release/lightwave-logic-and-tower-semiconductor-announce-development-agreement-enable-high) | 110GHz+ EO polymer modulator reference designs into Tower PH18 PDK；2026 engineering tapeouts；200G/400G modulator architectures |
| [UMC Q1 2026 report](https://www.umc.com/upload/media/08_Investors/Financials/Quarterly_Results/Quarterly_2020-2029_English_pdf/2026/Q1_2026/UMC26Q1_report.pdf) | Revenue NT$61.04B/US$1.93B；gross margin 29.2%；22/28nm 34%，22nm 14%；50+ customers tape-outs by year-end；TFLN AI infrastructure partnership |
| [UMC/HyperLight/Wavetek TFLN partnership](https://www.umc.com/en/News/press_release/Content/corporate/20260312) | HyperLight TFLN Chiplet Platform 在 6/8 英寸 wafer 高量制造，UMC/Wavetek 支持 AI infrastructure scale |
| [UMC/HyperLight/Jabil TFLN deployment](https://www.umc.com/en/News/press_release/Content/corporate/20260313) | Jabil 加入，推动 TFLN photonics 进入 hyperscale AI data center interconnects |
| [X-FAB Q1 2026 results](https://www.xfab.com/securedl/sdl-eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NzgxNjE0NDEsImV4cCI6MTc3ODI1MTQ0MSwidXNlciI6MCwiZ3JvdXBzIjpbMCwtMV0sImZpbGUiOiJmaWxlYWRtaW4vWC1GQUIvSW52ZXN0b3JfUmVsYXRpb25zL1ByZXNzX1JlbGVhc2VfWC1GQUJfUTFfMjAyNl9SZXN1bHRzXzMwQXByMjAyNl9FTkcucGRmIiwicGFnZSI6Nn0.WovUCfUYKjAKKuYMSvtqUbR7kamsWM2UXE90PSpQSyQ/Press_Release_X-FAB_Q1_2026_Results_30Apr2026_ENG.pdf) | Q1 revenue $195.6M；microsystems & photonics $33.7M +42% YoY；WBG $15.1M +152%；SiC wafers 14,300 +195%；data center power management demand |
| [Hua Hong 4Q25 presentation](https://cdn.prod.nntech.io/company-events/reports/b3067ffd-8770-3f5c-8c78-331be182be92/presentation.pdf) | 4Q25 capacity 486K 8-inch equivalent/month；utilization 103.8%；12-inch revenue 61.7%；Analog & PM +40.7%、Embedded NVM +31.3% |
| [VIS Q1 2026 MarketScreener summary](https://www.marketscreener.com/news/vanguard-international-semiconductor-vis-quarterly-sales-report-a-the-first-quarter-2026-ce7f58dfd18bf52d) | Q1 revenue NT$12.532B；Q2 shipment +11%-13%、ASP +2%-4%、gross margin 31%-33% |
| [NXP/VIS VSMC Singapore fab](https://investors.nxp.com/news-releases/news-release-details/vsmc-celebrates-breaking-ground-300mm-fab-singapore) | $7.8B Singapore 300mm fab，mixed-signal/power/analog，2027 mass production |
| [TrendForce foundry 2026 growth](https://www.trendforce.com/presscenter/news/20260319-12979.html) | Foundry revenue 2026 +24.8%；AI custom chips；mature-node 8-inch reductions and AI power-management demand lift utilization |
| [TrendForce/DRAMeXchange 8-inch utilization](https://www.dramexchange.com/WeeklyResearch/Post/2/12691.html) | Top 10 foundries 8-inch utilization 2026 接近 90%，1H27 >80%；AI servers/general servers/edge AI power IC demand |
| [TrendForce mature-node price hikes](https://www.trendforce.com/news/2026/01/27/news-ai-demand-to-lift-mature-node-prices-smic-reportedly-up-10-vanguard-estimated-up-4-8-from-q1/) | AI data center HVDC/power components 推动 mature node price hike；SMIC/Vanguard 价格线索 |
| [OFC 2026 项目内会议更新](../conference_update/ofc_2026_conference_update.md) | 1.6T >500 万只、CPO/CPX/XPO/ELS、3.2T、光模块/测试/OCS 本地整理 |
| [项目内 AI 芯片路线图](../ai_chip_research_2026_2027.md) | 2026-2027 出货量最大 AI 芯片平台和供应链约束 |

## 11. 最终判断

特种晶圆代工在 2026 年的投资逻辑不是“成熟制程周期修复”，而是 **AI 数据中心把光、电、热、控制和可靠性全部推到晶圆层**。GPU/ASIC 仍是最大价值池，但 1.6T/CPO 光互联、48V/800V power、BMC/PMIC、SiC/GaN、MEMS/OCS 正在把特种工艺变成 AI rack 可交付性的瓶颈。

2026 最确定的是 **Tower/GF/TSMC/UMC 的硅光/SiGe/TFLN，叠加 VIS/UMC/Hua Hong/SMIC/X-FAB 的 BCD/HV/PMIC/SiC**；2027 最大预期差是 **CPO/TFLN/III-V-on-Si + 800VDC/SiC/GaN** 同时进入大客户设计冻结。极度乐观情景下，AI 基建不会只吃满 CoWoS/HBM，也会吃满高端 8 英寸特种工艺、光电测试、SOI/TFLN/SiC 材料和客户认证过的区域化 foundry capacity。
# 行业调研：【先进封装设备与混合键合】

> 截至日期：2026-05-08  
> 口径：本报告研究 AI 数据中心加速器相关的先进封装设备、关键工序和混合键合产业链。重点包括 Hybrid Bonding、TCB/fluxless TCB、高精度 flip-chip、临时键合/解键合、晶圆薄化/切割、RDL/电镀/CMP/刻蚀/沉积、检测量测、探针/ATE/老化、CPO/硅光封装设备，以及这些设备绑定的材料、客户认证和产能瓶颈。  
> 预测原则：对 2026-2027 AI 基础设施建设采用明显乐观假设；缺少直接公开数据的环节，用项目内 AI 芯片出货路线、HBM stack、CoWoS/SoIC 产能、设备订单、客户 GW 级订单和一手公司发言倒推。

## 0. 结论先行

先进封装设备与混合键合不是“封测设备小周期”，而是 2026-2027 AI 算力交付的上游阀门。2026 年最大确定性来自 **CoWoS-L/S + HBM3E/HBM4 early ramp + TCB/fluxless TCB + KGD/test + 大尺寸载板/RDL**；2027 年估值弹性来自 **D2W/W2W hybrid bonding、16H/20H HBM、SoIC/3D chiplet、EMIB-T/I-Cube/X-Cube、CPO/photonic package、玻璃/面板级封装**。

一手信号很强：

- TSMC 1Q26 美元收入 `$35.9B`、毛利率 `66.2%`、HPC 占收入 `61%`；公司把 2026 capex 指向 `$52-56B` 区间高端，并称 AI demand extremely robust，N3 扩产明确包含 HPC/AI 与 HBM base die。[TSMC 1Q26 release](https://pr.tsmc.com/system/files/newspdf/attachment/d9d0df84c45bffa6e19e247d152e6c1f8239390d/1Q26%20%28E%29_with%20gudiance_final_wmn.pdf)、[TSMC transcript](https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf)。
- Besi 1Q26 订单 `EUR269.7M`，同比 `+104.5%`；hybrid bonding system unit orders 环比超过翻倍，HB adoption 到 `20` 个客户，Q2 revenue guidance 环比 `+30-40%`，毛利率指引 `64-66%`。[Besi 1Q26](https://www.globenewswire.com/news-release/2026/04/23/3279584/0/en/BE-Semiconductor-Industries-N-V-Announces-Q1-26-Results.html)。
- ASMPT 1Q26 bookings `HK$5.67B / US$727M`，环比 `+46%`、同比 `+71.6%`，book-to-bill `1.43`；TCB/HB、CPO、1.6T 光模块、HBM4 16H qualification 都在正式口径中出现。[ASMPT 1Q26](https://www.asmpt.com/en/investor-relations/news-events/asmpt-announces-2026-first-quarter-results/)。
- SUSS 1Q26 order intake `EUR149.3M`，同比 `+69.5%`，创公司季度纪录；Advanced Backend order intake `EUR99.7M`，bonding tools for HBM/AI modules 明显高于 2025 上半年总量；公司称临时键合/解键合市场份额约 `45%`，需求高位可延续到 2030。[SUSS Q1 2026](https://www.marketscreener.com/news/suss-microtec-interim-statement-as-of-march-31-2026-ce7f58d3d98bf325)、[SUSS Annual Report 2025](https://www.suss.com/tw/content/download/3228/47132?version=3)。
- Applied Materials 1Q FY26 称 2026 半导体设备业务有望增长 `>20%`，最快增长环节是 HBM 与 3D chiplet-stacking；HBM 每 bit 需要标准 DRAM `3-4x` wafer starts，stack 从 12H 走向 16H/20H。[Applied Q1 FY26 script](https://ir.appliedmaterials.com/static-files/8beb86c0-2533-4d20-ba09-41fab41fc451)。
- Micron 在 GTC 2026 宣布 HBM4 36GB 12H 已于 2026Q1 volume shipment、面向 NVIDIA Vera Rubin；48GB 16H HBM4 已送样，容量同 footprint 提升 `33%`。[Micron HBM4](https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin)。

我的核心判断：**2026 最赚钱的是“传统高精度工艺的极限放大”，2027 最有估值弹性的是“混合键合从认证走向量产”。** 短期应重视 TCB、临时键合/薄化、检测量测、HBM test 和 RDL/电镀/CMP；中期重视 Besi/Applied Kinex、EVG、SUSS/SET、ASMPT fluxless TCB、KLA/Onto/Camtek、Advantest/FormFactor/Technoprobe 这类能把良率、overlay、清洁度和 throughput 锁住的公司。

## 1. 2026 AI 计算中心建设下的机遇、挑战和技术路径

### 1.1 机遇

| 机遇 | 产业含义 | 设备侧最直接受益 |
|---|---|---|
| Blackwell Ultra/GB300 是 2026 主力 | 需要成熟 CoWoS-L/S、HBM3E、ABF 大载板、KGD 和高吞吐 TCB | TCB、flip-chip、RDL/电镀/CMP、probe/ATE、3D metrology |
| Rubin/MI400/TPU8/OpenAI XPU 2026H2-2027 导入 | HBM4、16H、更多 chiplet 和更大 package，推动 HB/SoIC/EMIB 替代路线 | hybrid bonding、fluxless TCB、D2W overlay、X-ray/IR/e-beam inspection |
| 云厂 ASIC 从补充变成独立产能池 | Broadcom/Marvell/Google/AWS/Meta/Microsoft/OpenAI 使先进封装需求不再只看 NVIDIA | 2.5D/3D 封装整线、KGD、RDL、custom HBM base die 相关设备 |
| AI 推理进入 agentic/长上下文 | HBM 容量、bandwidth、package 功耗继续上升，封装内互连比单 die 缩放更重要 | HBM4/HBM4E 设备、CPO/硅光封装、热/翘曲检测 |
| CoWoS 和 HBM 供给长期紧 | 客户愿意预付、锁产能、接受高端设备和材料溢价 | 高端设备毛利率维持，服务/备件/field support 变成隐形利润池 |

### 1.2 挑战

| 挑战 | 为什么难 | 投资含义 |
|---|---|---|
| HB 良率不是单机问题 | 表面粗糙度、颗粒、pad profile、oxide activation、queue time、overlay、void 都会吃良率 | 能提供 clean + activation + metrology + bonder 整线的公司定价权更强 |
| HBM4 16H/20H 把薄化、翘曲、测试放大 | stack 越高，TSV、微凸点/混合键合、热应力和 KGD 损失越贵 | 临时键合、薄化、dicing、ATE、probe card 的价值量上升 |
| CoWoS 名义产能不等于有效产出 | interposer/RDL、substrate、HBM KGD、final test、客户认证任一环节卡住都会拖 rack 交付 | 检测量测和 test 工序从成本项变成交付瓶颈 |
| 设备交期和应用工程师稀缺 | HB/TCB/overlay recipe 需要客户现场磨合，不能临时扩产 | service network 在台湾/韩国/美国/马来西亚/新加坡的公司更值钱 |
| AI 客户改版快 | Rubin/MI400/ASIC 的 HBM、substrate、interconnect、power/thermal design 仍在迭代 | flexible platform、software control、closed-loop metrology 溢价提升 |

### 1.3 项目内 2026-2027 出货量最大 AI 芯片路径对设备的映射

以下芯片排序来自项目内 `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md` 和既有先进封装底稿；本报告只抽取对设备和混合键合的含义。

| 2026-2027 价值/出货权重最高平台 | 封装与互连路径 | 对设备的直接拉动 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | TSMC 4NP + CoWoS-L/S + HBM3E，大尺寸 ABF，NVL72 液冷 rack | 2026 最大收入池；TCB、HBM KGD、RDL/电镀、ABF inspection、ATE/SLT、warpage metrology 满载 |
| AWS Trainium2/3 | 定制 ASIC + HBM + NeuronLink，Trainium3 进入 3nm/高密度 rack | 自用 ASIC 不公开封装细节，但消耗 HBM、2.5D、KGD、system burn-in 和高密度互连测试 |
| Google TPU v7 Ironwood / TPU8 | Broadcom/Google XPU + HBM，Ironwood 已主打 inference | Broadcom XPU 平台放量，增加非 NVIDIA 的 2.5D、RDL、custom substrate 和 test 需求 |
| NVIDIA B200/GB200 | CoWoS + HBM3E，存量订单延续 | 成熟 2.5D 产能继续满载，2026 仍是 TCB/ATE 的大盘底座 |
| Huawei Ascend 910C/950 | 国产先进封装 + HBM/高带宽内存替代 + 超节点 | 国产封装设备、OAM、载板、测试、良率改进需求上升 |
| Cambricon MLU 590/690 | SMIC 可得先进节点 + HBM/OAM + 本土封装 | 本土 2.5D、probe、ATE、HBM KGD、国产材料替代受益 |
| AMD MI350 / MI400 Helios | MI350 HBM3E，MI400/MI455X 转 HBM4 与 72 GPU rack | MI350 拉动成熟 2.5D；MI455X + Samsung HBM4 推动 16H、HBM4 test 和封装替代产能 |
| Meta MTIA / OpenAI-Broadcom XPU / Microsoft Maia | 云厂定制 ASIC + HBM + 以太网/自研 scale-up | Broadcom/Marvell 定制 silicon 将 advanced packaging demand 扩散到更多客户和 OSAT |
| NVIDIA Rubin / Vera Rubin NVL72 | HBM4、NVLink 6、Vera CPU + Rubin GPU，2026H2 出货 | 2026H2 小批，2027 放量；HBM4、hybrid bonding、SoIC、KGD、CPO switch package 的核心催化 |

### 1.4 新技术成熟时间和放量时间：三情景

| 技术 | 基准情景 | 乐观情景 | 极度超预期乐观情景 |
|---|---|---|---|
| CoWoS-S/L + TCB + HBM3E | 已成熟，2026 全年满载；2027 继续被 Rubin/ASIC 消耗 | 2026H2 外包/周边工序承接顺利，良率改善 | 客户预付款锁产能，设备订单提前到 2027/2028，ASP 不降反升 |
| HBM4 12H + flux/fluxless TCB | 2026Q2-Q3 完成更多客户验证，2026Q4 小批，2027 主力 | 三大 HBM 厂 2026Q2 通过 NVIDIA/AMD 关键验证，2026H2 贡献明显 | HBM4 成为 2026H2 高端新增默认配置，带动 TCB/HB/test 急单 |
| HBM4 16H / HBM4E | 2026 样品与 qualification，2027H2 小批，2028 放量 | 2027H1 高端 Rubin/MI400/ASIC 采用 | 2026Q4 16H HBM4 被头部客户锁单，2027 形成十亿美元级设备订单池 |
| D2W hybrid bonding 逻辑 chiplet | 2026 以 pilot/qualification 为主，2027-2028 渗透到高端 XPU | 2026H2 个别 ASIC 量产案例，2027 渗透 10-20% | CoWoS 太紧 + 性能压力驱动，2027 high-end XPU 30% 以上采用 HB |
| W2W hybrid bonding for memory/3D DRAM | 3D NAND/CMOS image 等成熟，DRAM/HBM 仍验证；HBM5 更可能主流 | HBM4E/16H 先导项目 2027 进入量产 | 内存厂为降低功耗和 pitch，2027 即把 HB 用于高端 HBM 主流项目 |
| Integrated HB line / Applied-Besi Kinex | 2026-2027 客户验证，2027-2029 渗透 | 2027 多家 foundry/memory 客户导入 HVM line | 2026H2 高端 AI chiplet 量产需求提前，整线模式成为行业 POR |
| EMIB-T/Foveros / Samsung I-Cube/X-Cube | 2026 design-in，2027 份额提升 | CoWoS 过紧让 Intel/Samsung 获得第二供应源订单 | 美国/韩国替代产能获 hyperscaler 战略订单，2027 份额 20%+ |
| CoPoS/FOPLP/玻璃基板 | 2026-2027 pilot，2028 后放量 | 2027H2 特定 ASIC 小批 | 若大尺寸 organic substrate 良率持续卡住，2027 即出现高端试产急单 |
| CPO/photonic package | 2026 在 1.6T 光模块和 CPO pilot，2027 switch 侧小批 | Spectrum-6/Broadcom switch 需求把 CPO 设备提前 | 1.6T/3.2T 功耗压力爆发，2027 高端 AI switch CPO 渗透 15%+ |

### 1.5 2026 最可能的技术路径

2026 最可能大量出货的不是最激进的全 hybrid bonding，而是 **成熟 2.5D 的极限放大 + HBM4 早期导入 + 关键设备前置下单**：

1. CoWoS-L/S、同类 2.5D、HBM3E、ABF 大载板仍是收入最大主线。
2. TCB、fluxless TCB、high-precision flip-chip、embedded bridge die bonding 是 2026 设备订单确定性最高环节。
3. 临时键合/解键合、薄化、切割、CMP、清洗、warpage control 因 HBM/大 package 继续紧缺。
4. Hybrid bonding 在 2026 的主流商业状态是“客户验证 + 小批 + 设备订单提前”，2027 才更像放量年。
5. Metrology/inspection/ATE/probe card 是非显性瓶颈，尤其是 HBM4 KGD、D2W overlay、void detection、interposer/RDL defect、SerDes/NVLink/UALink burn-in。

## 2. 已开始放量的关键产品：规模、渗透率、增长和利润率

说明：未来 3 个月按 2026Q2-Q3 可确认收入/订单，未来 1 年按 2026H2-2027H1，未来 2 年按 2026H2-2028H1。市场规模为全球设备/工序收入或订单池估算，不等于单一公司收入。

### 2.1 已放量产品与技术

| 已放量产品/技术 | 当前状态 | 未来 3 个月市场规模：基准/乐观/极超 | 未来 1 年：基准/乐观/极超 | 未来 2 年：基准/乐观/极超 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| TCB / high-precision flip-chip / C2S-C2W bonding | GB300、MI350、HBM3E、2.5D 量产主力；ASMPT 披露 C2W ultrafine-pitch TCB 新订单 | `$1.1-1.8B / $1.6-2.5B / $2.5-3.8B` | `$5-7.5B / $7-11B / $11-16B` | `$8-13B / $13-22B / $22-35B` | 高端 AI 2.5D attach rate 2026 `80-95%`，2027 仍 `70%+`，部分被 HB 替代 | 设备毛利 `45-65%`；头部供应商因客户认证和交期可有 `5-15%` 溢价 |
| HBM3E/HBM4 early stack assembly equipment | HBM3E 满载，HBM4 12H 2026Q1-Q2 开始量产/验证；Micron HBM4 36GB 12H 已 volume shipment | `$1.5-2.4B / $2.1-3.4B / $3.2-5.0B` | `$7-11B / $10-16B / $16-25B` | `$13-22B / $20-35B / $35-55B` | AI accelerator HBM attach 接近 `100%`；HBM4 在高端新增中 2026 `5-20%`，2027 `35-60%` | HBM memory 毛利极高；设备毛利 `50-70%`，服务/备件高可见度 |
| 临时键合/解键合、薄化、dicing、carrier systems | HBM 和薄 die stack 刚需；SUSS 称 TBDB 市占约 `45%`，需求高位到 2030 | `$0.8-1.2B / $1.2-1.8B / $1.8-2.6B` | `$3.5-5.5B / $5-8B / $8-12B` | `$6-10B / $9-15B / $15-24B` | HBM/2.5D 相关 wafer attach `70-90%`；16H/20H 后强度上升 | SUSS 当前集团 GM `36.1%`、产品 mix 波动；龙头产品线稳态 GM 可 `40-55%` |
| RDL/电镀/CMP/刻蚀/沉积/表面处理 | CoWoS、fan-out、bridge、hybrid bonding pad stack 的底层工艺 | `$1.5-2.4B / $2.2-3.5B / $3.5-5.5B` | `$7-11B / $10-16B / $16-25B` | `$12-20B / $20-32B / $32-50B` | 高端 2.5D package 覆盖 `>85%`，2027 package size 增大推高步骤数 | AMAT/Lam/TEL/ASM 等设备 GM 通常 `45-60%+`；材料和 service 提升稳定性 |
| 3D metrology、macro inspection、D2W overlay、X-ray/IR inspection | Onto Dragonfly G5 已在 2.5D logic 和 HBM 客户 qualification；KLA/Onto/Camtek 受益 | `$0.9-1.4B / $1.3-2.0B / $2.0-3.0B` | `$4.5-7B / $6.5-10B / $10-15B` | `$8-13B / $12-20B / $20-32B` | AI package test/inspection 成本占比从低个位数升至 `5-8%`，HB/CPO 后继续上行 | Onto 1Q26 non-GAAP GM `55.7%`；KLA/高端 process control 具备 `60%+` GM 潜力 |
| Probe card、ATE、HBM KGD、SLT/burn-in | HBM4、SerDes、NVLink/UALink、CPO 需要更长测试 | `$1.5-2.3B / $2.2-3.3B / $3.3-5.0B` | `$7-11B / $10-16B / $16-24B` | `$12-20B / $18-30B / $30-48B` | HBM KGD attach `100%`；AI package final test 时间 2026-2027 继续增加 | Advantest/Teradyne/FormFactor/Technoprobe 高端产品 GM `45-65%`，probe card 周期性较高 |
| CPO/硅光封装、1.6T optical transceiver assembly | ASMPT photonics revenue 1Q26 同比 `5x`，1.6T transceiver bulk orders 已出现 | `$0.4-0.8B / $0.7-1.2B / $1.2-2.0B` | `$2-3.5B / $3.5-6B / $6-10B` | `$5-10B / $9-18B / $18-32B` | 2026 CPO 在 AI switch <`5%`，2027 `5-12%`，pluggable 仍主体 | 光封装设备/核心光引擎 GM `40-65%`；CPO 初期良率波动大 |

### 2.2 已放量环节增长预测

| 环节 | 基准增长 | 乐观增长 | 极度超预期增长 |
|---|---:|---:|---:|
| TCB/高精度 flip-chip | 未来 12 个月 `+35-55%` | `+60-90%` | `+100%+` |
| HBM stack assembly/test 设备 | `+45-70%` | `+80-120%` | `+150%+` |
| 临时键合/薄化/切割 | `+25-45%` | `+50-80%` | `+90%+` |
| RDL/电镀/CMP/刻蚀/沉积 | `+25-45%` | `+50-75%` | `+90%+` |
| 检测量测 | `+35-60%` | `+70-100%` | `+120%+` |
| ATE/probe/burn-in | `+30-55%` | `+60-90%` | `+100%+` |
| CPO/光封装设备 | `+60-100%` | `+120-180%` | `+200%+`，但基数小 |

### 2.3 利润率三情景

| 产品/技术 | 基准利润率 | 乐观利润率 | 极度超预期利润率 |
|---|---:|---:|---:|
| Hybrid bonding/TCB 设备 | GM `50-62%`，OPM `25-35%` | GM `58-68%`，OPM `32-45%` | GM `65-72%`，OPM `40-50%` |
| 临时键合/薄化/切割 | GM `35-50%`，OPM `10-25%` | GM `42-55%`，OPM `18-32%` | GM `50-60%`，OPM `25-38%` |
| RDL/沉积/刻蚀/CMP | GM `45-58%`，OPM `25-35%` | GM `50-62%`，OPM `30-40%` | GM `58-68%`，OPM `38-48%` |
| Metrology/inspection | GM `55-65%`，OPM `25-35%` | GM `60-70%`，OPM `32-45%` | GM `68-75%`，OPM `40-50%` |
| ATE/probe card | GM `45-60%`，OPM `20-35%` | GM `55-68%`，OPM `30-45%` | GM `62-75%`，OPM `40-55%` |
| CPO/光封装设备 | GM `40-55%`，OPM `10-25%` | GM `50-65%`，OPM `20-35%` | GM `60-70%`，OPM `30-45%` |

## 3. 在研关键产品和细分技术：未来放量产品

### 3.1 在研/导入期产品与技术

| 在研产品/技术 | 当前阶段 | 未来 3 个月：基准/乐观/极超 | 未来 1 年：基准/乐观/极超 | 未来 2 年：基准/乐观/极超 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| D2W hybrid bonding AI chiplet | Besi adoption 20 客户；Applied-Besi Kinex、EVG/SUSS/SET 推进 | `$0.4-0.7B / $0.7-1.1B / $1.1-1.8B` | `$2.2-3.5B / $3.5-5.5B / $5.5-8.5B` | `$6-10B / $10-16B / $16-26B` | AI accelerator package 渗透 2026 `<5%`，2027 `10-20%`，2028 `20-35%` | 设备 GM `55-70%`，整线/service 溢价最强 |
| W2W hybrid bonding for DRAM/HBM/3D DRAM | EVG/SUSS/TEL 等供给；memory 客户验证中 | `$0.2-0.5B / $0.5-0.9B / $0.9-1.5B` | `$1-2B / $2-4B / $4-7B` | `$4-8B / $8-15B / $15-25B` | HBM4E/HBM5 才最可能主流；2027 仍小批 | 早期良率风险高，但一旦 POR 锁定，GM 可 `60%+` |
| Fluxless TCB / AOR for HBM4 16H | ASMPT 披露 memory player sampling/qualifying | `$0.3-0.6B / $0.6-1B / $1-1.6B` | `$1.5-3B / $3-5B / $5-8B` | `$5-9B / $8-14B / $14-22B` | HBM4 16H 2026 样品，2027 进入 premium XPU | 高端设备 GM `50-65%`，认证后定价强 |
| Integrated HB line: clean + activation + metrology + bonder | Applied Kinex 把 Besi bonder与前后段模块整合 | `$0.1-0.3B / $0.3-0.7B / $0.7-1.2B` | `$1-2.5B / $2.5-5B / $5-8B` | `$5-10B / $10-18B / $18-30B` | 2027 起从 pilot line 到 HVM line；2028 加速 | 整线 GM `55-70%`，service attach 提高 ROIC |
| CoPoS / panel-level advanced packaging | 2026 pilot/qualification | `<$0.2B / $0.3-0.6B / $0.8-1.5B` | `$0.5-1.5B / $1.5-3B / $3-6B` | `$3-8B / $7-15B / $15-30B` | 2027 前 `<3%`，2028 若良率过关 `5-12%` | 初期低毛利，设备/材料先受益 |
| 玻璃基板/玻璃 interposer 设备 | Intel/Samsung/Absolics/Corning/LPKF 等验证 | `<$0.1B / $0.2-0.4B / $0.5-1B` | `$0.5-1B / $1-2.5B / $2.5-5B` | `$3-7B / $6-14B / $12-25B` | 2026-2027 以试产为主，2028 后看 AI package 面积 | 技术壁垒高，材料/设备 GM `40-60%` |
| Photonic interposer / optical I/O package | Lightmatter、Ayar Labs、Broadcom、NVIDIA switch 侧推进 | `$0.1-0.3B / $0.3-0.6B / $0.6-1B` | `$0.7-1.5B / $1.5-3B / $3-6B` | `$3-8B / $7-18B / $15-35B` | CPO 2026 `<5%`，2027 `5-12%`，OIO 更晚 | 核心光引擎/封装设备 GM `45-65%` |
| Package-level power delivery / semi-IVR / embedded decap | 高电流瞬态驱动封装协同设计 | `$0.2-0.5B / $0.4-0.8B / $0.8-1.3B` | `$1.5-3B / $2.5-5B / $5-8B` | `$5-10B / $8-16B / $15-28B` | GB300/Rubin/MI400 高端模块优先，2027 扩散到 ASIC | 功率 IC/材料/检测 GM `30-60%` |

### 3.2 未来最快增长方向排序

1. **D2W hybrid bonding 整线。** 2026 订单领先收入，2027-2028 真放量；一旦进入 NVIDIA/AMD/Broadcom/TSMC/Samsung/Intel 的 POR，切换成本极高。
2. **HBM4 16H/20H 的 fluxless TCB、薄化、测试和 metrology。** HBM4 不是单个 memory 产品，而是推动整条后段设备链升级。
3. **D2W overlay/void/IR/X-ray/e-beam inspection。** HB 的 yield loss 太贵，检测密度会非线性上升。
4. **CPO/photonic package。** 2026 收入小，但 1.6T/3.2T 功耗压力会推动高端 switch 侧加速。
5. **玻璃/面板级封装。** 2027 前更多是期权，但若有机载板翘曲和尺寸瓶颈持续，会被提前重估。

## 4. 供给侧：产能结构、瓶颈、成本与毛利

### 4.1 产能结构

| 环节 | 主要地区 | 主要公司 | 关键工艺/资源 |
|---|---|---|---|
| Foundry + CoWoS/SoIC | 台湾为核心，美国/日本扩产中 | TSMC | CoWoS-S/L/R、SoIC、InFO、3DFabric、N3/N2、HBM base die |
| IDM 替代 advanced package | 美国、韩国、马来西亚 | Intel Foundry、Samsung Foundry/AVP | EMIB/EMIB-T、Foveros、I-Cube、X-Cube、turnkey HBM+foundry+package |
| HBM stack 与 memory packaging | 韩国、美国、日本、台湾 | SK hynix、Samsung、Micron | HBM3E/HBM4、TCB、16H/20H、logic base die、KGD |
| Hybrid bonding / TCB 设备 | 荷兰、美国、奥地利、德国、新加坡/香港、日本、法国 | Besi、Applied、EVG、SUSS/SET、ASMPT、TEL、K&S、Shibaura、Hanmi | W2W/D2W HB、activation/cleaning、TCB、fluxless TCB、ultra-fine pitch |
| 临时键合/薄化/切割 | 德国/奥地利/日本/美国 | SUSS、EVG、TEL、DISCO、Accretech、Brewer Science、3M | carrier bonding/debonding、grinding、dicing、laser release |
| 检测量测 | 美国、日本、以色列、荷兰 | KLA、Onto、Camtek、Nova、Applied、Bruker、Hitachi High-Tech、JEOL、Lasertec | overlay、macro defect、3D bump、IR/X-ray、e-beam、film metrology |
| ATE/probe/burn-in | 美国、日本、台湾、意大利/法国、韩国 | Advantest、Teradyne、Cohu、FormFactor、Technoprobe、MPI、Chroma、Aehr、TSE、Japan Electronic Materials | HBM KGD、probe card、SLT、burn-in、SerDes test |
| OSAT advanced package | 台湾、韩国、马来西亚、中国大陆、新加坡、美国 | ASE/SPIL、Amkor、JCET、Tongfu、Huatian、PTI、KYEC、Siliconware、UTAC | 2.5D/FOWLP/SiP/test/assembly 外溢 |
| 高阶载板与材料 | 日本、台湾、韩国、中国大陆、美国 | Ibiden、Shinko、Unimicron、Nan Ya、Kinsus、AT&S、Semco、Daeduck、Shennan、Ajinomoto、Resonac、Namics、Shin-Etsu、DuPont、Entegris | ABF/BT、underfill、dielectric、CMP slurry、photoresist、bonding adhesive |

### 4.2 至少 10 条供给瓶颈

1. **HB/TCB 设备交期与客户认证。** Besi/ASMPT/SUSS 订单已明显上行，但从工具交付到稳定 HVM 需要 recipe、field support 和良率爬坡。
2. **HB 表面清洁和颗粒控制。** D2W hybrid bonding 对颗粒和表面活性极敏感，queue time 会直接影响 void 和 bond yield。
3. **HBM KGD 和 16H/20H 良率。** 单颗坏 die 损失会放大到整 stack，测试时间和 probe card 数量成为隐形产能。
4. **临时键合/薄化/解键合能力。** 高层 HBM 和超薄 chiplet 需要 carrier、adhesive、laser/IR release、wafer handling 同时成熟。
5. **大尺寸 ABF/载板翘曲和供应。** GB300/Rubin/MI400/ASIC package 面积上升，substrate 良率和热机械稳定性约束有效产出。
6. **RDL/interposer defect density。** 大面积中介层和 RDL 任一缺陷都会导致高价值 package 报废，检测密度上升。
7. **高级 metrology/inspection 产能。** D2W overlay、3D bump、void、warpage、X-ray/IR inspection 都需要更长 cycle time。
8. **ATE/SLT/burn-in 时间。** HBM4、NVLink/UALink、SerDes、CPO、rack-scale fabric 使 final test 从“出货前检查”变成交付瓶颈。
9. **应用工程师和本地服务。** 设备不是标准商品；台湾、韩国、美国、马来西亚现场支持能力决定 ramp 速度。
10. **地缘集中。** 台湾 CoWoS、韩国 HBM、日本材料、荷兰/美国/日本设备高度集中；任何地区扰动都会放大。
11. **cleanroom 和厂务。** Applied 指出客户 cleanroom availability 会 pace investment；工具订单不等于即时产能。
12. **化学品/气体/耗材。** TSMC 1Q26 电话会专门谈到 helium、hydrogen、specialty chemicals 和 energy 风险，说明材料安全库存已经是管理层议题。

### 4.3 成本结构

#### 先进封装设备 BOM/单位成本拆分

| 成本项 | 典型占比 | 决定因素 |
|---|---:|---|
| 精密 stage、运动控制、机器人、wafer/die handling | `20-30%` | nm/sub-micron overlay、throughput、die damage rate |
| process module：plasma、wet clean、thermal、vacuum、degas、activation | `15-25%` | 表面活性、queue time、contamination、recipe 稳定性 |
| optics / IR / X-ray / e-beam / sensor / metrology | `10-20%` | D2W overlay、void detection、3D bump、closed-loop control |
| mini-environment、particle control、chemical delivery | `5-12%` | Class-1 clean、chemical purity、wafer marathon 稳定性 |
| software、traceability、analytics、factory automation | `5-12%` | yield learning、predictive maintenance、客户 MES 集成 |
| assembly、calibration、field support、warranty | `15-25%` | 客户现场调机周期、uptime SLA、应用工程师密度 |
| 供应链缓冲和库存 | `5-10%` | 长交期部件、客户加急、区域化库存 |

#### 高端 AI package 成本拆分

| 成本项 | 典型占比 | 价格弹性 |
|---|---:|---|
| HBM stacks | `30-45%` | 2026-2027 最强，长协和预付款支撑 |
| advanced package / CoWoS/SoIC/EMIB service | `8-15%` | TSMC/IDM 最强，OSAT 次之 |
| substrate/interposer/RDL | `15-25%` | 大尺寸、低翘曲、高层数 ABF 溢价 |
| bonding/assembly/materials | `5-10%` | TCB/HB、underfill、TIM、stiffener |
| test/probe/burn-in | `5-10%` | KGD、SerDes/HBM/CPO test 时间上升 |
| yield loss / scrap reserve | `5-15%` | HB/large package 初期可能显著高于成熟工艺 |

### 4.4 毛利决定因素和价格传导

- **最紧环节拿最大溢价。** 2026 是 HBM、CoWoS/2.5D、TCB/HB、KGD/test、ABF 共同紧，客户无法只压单一环节价格。
- **设备端的溢价来自客户认证和良率责任。** 一台设备的 ASP 不只看硬件 BOM，而看它能否提升 final package yield、缩短 cycle time 和减少报废。
- **TSMC/HBM/头部设备商更能传导成本。** OSAT 和普通材料商议价弱，除非进入高端 POR 或客户长协。
- **service attach 是长期 ROIC 关键。** 高端 HB/TCB/metrology 设备装机后，spares、field service、software analytics 和 process upgrade 会带来更稳定毛利。
- **若 2027 供给释放过快，低端封装和普通载板先承压。** 但 HB、HBM4 16H、D2W overlay、probe card、CPO 初期仍会稀缺。

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 细分 | 头部集中度判断 | 核心玩家 | 备注 |
|---|---|---|---|
| 高端 2.5D/CoWoS 服务 | TSMC 在 AI 高端份额估计 `75-90%` | TSMC、Intel、Samsung、ASE/Amkor 承接外溢 | 先进节点 + package + HBM base die 一体化最强 |
| D2W hybrid bonding | 高集中，仍在早期 | Besi、Applied+Besi、EVG、SUSS/SET、ASMPT、TEL | Besi 披露 20 客户 adoption；整线能力是下一阶段差异 |
| W2W wafer bonding | 高集中 | EVG、SUSS、TEL、Applied、Canon/相关生态 | memory/3D integration 先行 |
| TCB/fluxless TCB | 中高集中 | ASMPT、Besi、K&S、Shibaura、Hanmi | ASMPT 在 HBM4 16H AOR/fluxless 上有明确一手进展 |
| 临时键合/解键合 | 高集中 | SUSS、EVG、TEL | SUSS 自称市占约 `45%` |
| Advanced package metrology/inspection | 高集中 | KLA、Onto、Camtek、Nova、Applied、Bruker | 检测密度随 HB/大 package 上升 |
| ATE/probe card | 中高集中 | Advantest、Teradyne、FormFactor、Technoprobe、MPI、Chroma、Cohu | HBM KGD 和高端 probe card 供应紧 |
| RDL/电镀/CMP/刻蚀/沉积 | 中高集中 | Applied、Lam、TEL、ASM、Ebara、ACM Research、SCREEN | 与前道设备平台和 service network 绑定 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 解释 | 为什么能定价 |
|---|---|---|
| 技术壁垒 | HB 需要表面化学、颗粒、overlay、bond strength、void、thermal stress 同时达标 | 客户买的是良率和 time-to-volume，不是单机参数 |
| 工艺整合壁垒 | clean、activation、degas、metrology、bonding、anneal、inspection 之间 queue time 影响产出 | 能做整线和 closed-loop 的公司可收集成溢价 |
| 规模/服务壁垒 | 台湾/韩国/美国现场支持、备件、应用工程师决定 ramp | 客户不能把高价值 AI package 放在无服务保障工具上 |
| 客户锁定 | 封装 design rule、材料、test recipe、carrier、probe card 从设计阶段绑定 | 切换供应商会重做 qualification，损失季度级时间 |
| 认证周期 | foundry/memory/HBM/云厂认证通常 6-18 个月甚至更久 | 已在 POR 的设备商有天然续单权 |
| 数据和软件壁垒 | overlay/defect/traceability/yield analytics 需要历史数据 | 软件闭环会把设备商嵌入客户 MES 和良率模型 |
| 供应链壁垒 | 精密部件、光学、stage、motion control、真空、化学品不是短期可复制 | 上游长交期使新进入者难以快速放量 |
| 责任壁垒 | HB/TCB 失效会造成整包报废，单颗 package 价值极高 | 客户愿意为低 scrap 和确定交期付费 |

### 5.3 价值捕获：长期高 ROIC/高毛利在哪

1. **TSMC 型“先进节点 + 先进封装 + 生态”一体化。** 同时收 wafer、HBM base die、CoWoS/SoIC、设计生态和 turnkey 费用，客户替代难。
2. **Hybrid bonding / TCB / metrology 设备。** 设备 ASP 高、毛利高、service attach 强，且客户认证后复购概率高。
3. **HBM 龙头与 HBM test/probe。** 所有高端 XPU 共同刚需，2026-2027 价格和良率均支持高毛利。
4. **封装 EDA/IP/DFT/UCIe/HBM PHY。** 轻资产、高毛利、切换成本高，但投资标的更集中在 Synopsys/Cadence/Rambus/Marvell/Broadcom 等。
5. **高端材料。** ABF、underfill、dielectric、CMP slurry、temporary bonding adhesive 若进入 POR，毛利和持续性强。

相对而言，传统 OSAT 装配和普通载板长期 ROIC 较低，除非拿到 AI 2.5D/HBM/test 的高端认证并形成产能稀缺。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 拐点 1：Blackwell Ultra/GB300 把成熟 2.5D 设备推到满载

最可能放量：TCB、high-precision flip-chip、RDL/电镀/CMP、HBM3E KGD、probe card、SLT/burn-in、大尺寸 package inspection。

投资含义：2026 收入确定性最强的不一定是 hybrid bonding 纯概念，而是 TCB、临时键合、薄化、检测、probe/ATE 这些“所有 AI package 都绕不开”的瓶颈。

### 拐点 2：HBM4 从验证转为锁产能和锁设备

TrendForce 预计三大 HBM 厂 2026Q2 完成 NVIDIA Rubin HBM4 验证；Micron 已宣布 HBM4 12H volume shipment 与 16H sampling。[TrendForce HBM4](https://www.trendforce.com/presscenter/news/20260213-12929.html)、[Micron HBM4](https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin)。

最可能放量：HBM4 12H TCB、fluxless TCB、16H sample line、thin wafer handling、HBM tester、probe card、warpage/void inspection。

### 拐点 3：Hybrid bonding 从“技术路线”变成“客户预下单”

Besi hybrid bonding unit orders 环比超过翻倍，Applied-Besi Kinex 推整线，EVG/SUSS/SET 在 W2W/D2W 上加速。2026 的收入贡献可能不如 TCB 大，但订单、客户验证和估值弹性会很强。

最可能放量：D2W HB pilot line、integrated HB line、EVG40 D2W overlay metrology、surface activation/cleaning、IR/X-ray void inspection。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 拐点 1：Rubin/MI400/TPU8/MTIA 450/500/OpenAI XPU 进入 HBM4 时代

2027 最可能爆发的是 HBM4、HBM4E/16H、CoWoS-L、SoIC、EMIB-T、I-Cube/X-Cube、HB test 和大尺寸载板。D2W hybrid bonding 在基准情景下从 `<10%` 渗透率走到 `10-20%`，极度乐观可超过 `30%`。

### 拐点 2：第二供应源和替代封装路线获得战略估值

如果 TSMC CoWoS 继续满载，Intel EMIB-T/Foveros、Samsung turnkey packaging、ASE/Amkor 高端 OSAT、SUSS/EVG/ASMPT/Besi、玻璃/面板级路线都会获得更高战略价值。客户会为供给确定性付费。

### 拐点 3：CPO/硅光封装从网络侧反推封装设备升级

1.6T/3.2T 交换功耗上升，CPO/photonic package 需要高精度贴装、光电对准、热管理和可靠性测试。ASMPT 1Q26 已披露 photonics revenue 同比 `5x`、1.6T bulk orders，说明光封装设备先于 CPO 大规模采用受益。

## 8. 头部公司和细分玩家清单

### 8.1 平台、foundry、OSAT、封装服务

- TSMC：CoWoS-S/L/R、SoIC、InFO、3DFabric、HBM base die、N3/N2。
- Intel Foundry：EMIB、EMIB-T、Foveros、PowerVia 相关封装、美国 advanced packaging。
- Samsung Foundry / AVP：I-Cube、X-Cube、HBM4、4nm logic base die、turnkey AI package。
- ASE/SPIL、Amkor、JCET/STATS ChipPAC、Tongfu Microelectronics、Huatian、PTI、KYEC、UTAC：2.5D/FOWLP/SiP/test 外包与外溢产能。
- 云厂/平台 ASIC：NVIDIA、AMD、Broadcom、Marvell、Google TPU、AWS Annapurna Trainium/Inferentia、Microsoft Maia、Meta MTIA、OpenAI/Broadcom、Huawei Ascend、Cambricon、Alibaba T-Head、Baidu Kunlun。

### 8.2 Hybrid bonding、TCB、die attach、SMT/光封装设备

- Besi：D2W hybrid bonding、advanced packaging assembly；1Q26 HB 订单和客户 adoption 领先。
- Applied Materials：Kinex integrated D2W hybrid bonding、CVD/PVD/ECD/CMP/surface prep、e-beam、advanced packaging development centers。
- EV Group：GEMINI FB、W2W/D2W hybrid/fusion bonding、EVG40 D2W overlay、IR LayerRelease、LITHOSCALE XT。
- SUSS MicroTec + SET：XBC300 Gen2 D2W/W2W、temporary bonding/debonding、hybrid bonding portfolio、mask aligner/coater。
- ASMPT / ASM AMICRA：TCB、HB、C2S/C2W、AOR fluxless、photonics/CPO、1.6T transceiver assembly、SMT for AI servers。
- Kulicke & Soffa：thermo-compression、flip-chip、advanced dispense/die attach、wedge/wire legacy cash flow。
- Tokyo Electron、Shibaura Mechatronics、Hanmi Semiconductor、Palomar Technologies、Finetech、Toray Engineering、Yamaha Robotics：bonding、die attach、packaging automation、specialty assembly。

### 8.3 临时键合、薄化、切割、载体和解键合

- SUSS、EVG、Tokyo Electron：temporary bonding/debonding、carrier systems、hybrid/wafer bonding。
- DISCO、Accretech/Tokyo Seimitsu：grinding、dicing、CMP-like thinning、wafer saw/laser processing。
- Brewer Science、3M、Mitsui Chemicals、Shin-Etsu、TOK、JSR：temporary bonding adhesives、release layers、photoresist、process chemicals。

### 8.4 RDL、沉积、刻蚀、CMP、清洗、封装 lithography

- Applied Materials：PVD/CVD/ECD/CMP、surface prep、e-beam、advanced packaging integrated process。
- Lam Research：etch/deposition/clean、HBM/advanced packaging related process。
- Tokyo Electron：coater/developer、etch、clean、bonding adjacent tools。
- ASM International：ALD/epitaxy/materials deposition。
- Ebara：CMP、plating/clean adjacent。
- SCREEN、ACM Research、SEMES、Ulvac、Veeco、Canon、Nikon、SUSS、EVG、Onto JetStep：clean、lithography、RDL、fan-out、plating ecosystem。

### 8.5 检测量测、过程控制和软件

- KLA：process control、wafer/package inspection、overlay、reticle、metrology。
- Onto Innovation：Dragonfly G5、3D metrology、macro defect、lithography for advanced packaging；1Q26 revenue `$292M`，Q2 guide `$320-330M`。
- Camtek：2D/3D inspection/metrology for advanced packaging、HBM、compound semis。
- Nova：optical/CD/X-ray metrology、advanced nodes and packaging adjacent。
- Applied eBeam、Hitachi High-Tech、JEOL、Bruker、Lasertec、Nearfield Instruments、Nordson/CyberOptics：e-beam、X-ray、surface, bump, warpage, package inspection。

### 8.6 ATE、probe card、burn-in、SLT

- Advantest、Teradyne、Cohu、Chroma：ATE、memory/HBM、SoC、SLT、high-speed interface test。
- FormFactor、Technoprobe、MPI、TSE、Japan Electronic Materials、Feinmetall、Smiths Interconnect/IDI、Wentworth：probe card、probe station、high-end contactors。
- Aehr Test Systems、inTEST、Boston Semi Equipment、ESPEC：burn-in、wafer-level test、thermal stress。

### 8.7 HBM、载板、关键材料

- HBM/DRAM：SK hynix、Samsung、Micron；中国追赶包括 CXMT 等。
- HBM PHY/controller/IP：Rambus、Synopsys、Cadence、Marvell、Broadcom、Alphawave。
- 高阶载板：Ibiden、Shinko、Unimicron、Nan Ya、Kinsus、AT&S、Samsung Electro-Mechanics、LG Innotek、Daeduck、Shennan Circuits、Fastprint、Zhuhai Access。
- ABF/介质/underfill/TIM/CMP/化学品：Ajinomoto、Resonac、Namics、Shin-Etsu、Sumitomo Bakelite、Toray、DuPont、Entegris、Merck/EMD、JSR、TOK、Fujifilm Electronic Materials、Brewer Science、3M、Indium、Henkel、Dow。

### 8.8 CPO/硅光封装与光互连相关

- 芯片/交换：NVIDIA、Broadcom、Marvell、Intel、Cisco、Astera Labs。
- 硅光/OIO：Lightmatter、Ayar Labs、Celestial AI、POET、Ranovus、DustPhotonics。
- 光模块/封装制造：Coherent、Lumentum、Fabrinet、Foxconn Interconnect、Innolight、Eoptolink、Accelink、Hisense Broadband、TFC、AOI。
- 设备与测试：ASMPT、ficonTEC、PI、Keysight、Anritsu、EXFO、FormFactor、Chroma、Teradyne。

## 9. 投资排序与观察指标

### 9.1 投资排序

| 排名 | 方向 | 2026 投资含义 | 主要风险 |
|---:|---|---|---|
| 1 | TCB/fluxless TCB + HBM4 设备 | 最确定订单池，直接受益 GB300/HBM4 | HB 替代节奏、客户 capex 延后 |
| 2 | Hybrid bonding 整线与 D2W overlay | 2027-2028 最大技术弹性，2026 订单提前 | 良率、throughput、客户验证慢 |
| 3 | Metrology/inspection/process control | HB/大 package 良率刚需，毛利和 ROIC 强 | 客户集中、设备交期 |
| 4 | ATE/probe/HBM KGD | 隐性瓶颈，出货越大 test time 越贵 | 周期波动、客户内制 |
| 5 | 临时键合/薄化/切割 | HBM stack 和薄 die 刚需，SUSS/DISCO/EVG 受益 | 产品 mix 与单季收入波动 |
| 6 | RDL/电镀/CMP/沉积/刻蚀 | AI package 面积和层数提升，前道大厂受益 | 大厂业务太多，纯度不如 bonding |
| 7 | CPO/photonic package | 2027 弹性大，光模块 1.6T 已先放量 | CPO 标准和良率不确定 |
| 8 | 玻璃/面板级封装 | 2028+ 期权，估值弹性强 | 2026-2027 收入可能很小 |

### 9.2 未来 6-12 个月最重要观察指标

- Besi hybrid bonding order value、customer count、Q2/Q3 交付与毛利率是否维持高位。
- ASMPT C2W ultrafine-pitch TCB、AOR fluxless、HBM4 16H qualification 是否转 repeat orders。
- SUSS bonding tools order intake 是否连续高于 revenue，Advanced Backend book-to-bill 是否维持 `>1.5`。
- TSMC advanced packaging revenue 占比、CoWoS-L 良率、CoWoS 外包比例、N3/HBM base die 扩产。
- Micron/Samsung/SK hynix HBM4 12H/16H 验证、良率、capex 和长协。
- NVIDIA Rubin、AMD MI455X、Google TPU8、AWS Trainium3/4、Meta MTIA、OpenAI/Broadcom XPU 的真实出货节奏。
- Onto/KLA/Camtek 在 2.5D/HBM/advanced packaging 的订单和先进封装 revenue guide。
- Advantest/Teradyne/FormFactor/Technoprobe 对 HBM KGD、probe card、AI accelerator test 的交期和价格。

## 10. 资料来源

### 公司一手信息

- TSMC 1Q26 results release：<https://pr.tsmc.com/system/files/newspdf/attachment/d9d0df84c45bffa6e19e247d152e6c1f8239390d/1Q26%20%28E%29_with%20gudiance_final_wmn.pdf>
- TSMC 1Q26 earnings transcript：<https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf>
- TSMC Advanced Packaging Services：<https://www.tsmc.com/english/dedicatedFoundry/services/advanced-packaging>
- Besi 1Q26 results：<https://www.globenewswire.com/news-release/2026/04/23/3279584/0/en/BE-Semiconductor-Industries-N-V-Announces-Q1-26-Results.html>
- ASMPT 1Q26 results：<https://www.asmpt.com/en/investor-relations/news-events/asmpt-announces-2026-first-quarter-results/>
- EV Group SEMICON Korea 2026：<https://www.evgroup.com/company/news/detail/ev-group-highlights-hybrid-and-fusion-bonding-layer-transfer-and-maskless-lithography-technologies-for-advanced-semiconductor-memory-and-packaging-at-semicon-korea-2026>
- SUSS Q1 2026 interim statement mirror：<https://www.marketscreener.com/news/suss-microtec-interim-statement-as-of-march-31-2026-ce7f58d3d98bf325>
- SUSS Annual Report 2025：<https://www.suss.com/tw/content/download/3228/47132?version=3>
- SUSS XBC300 Gen2 D2W/W2W：<https://www.suss.com/en/news/corporate-news/2024/suss-microtec-presents-hybrid-bonding-all-rounder-xbc300-gen2-d2w-w2w?languageChanged=en>
- Applied Materials Q1 FY26 script：<https://ir.appliedmaterials.com/static-files/8beb86c0-2533-4d20-ba09-41fab41fc451>
- Applied Materials / Futurum hybrid bonding whitepaper：<https://www.appliedmaterials.com/content/dam/site/prod-tech/semi/doc/hybrid_bonding_scalev4.pdf.coredownload.inline.pdf>
- Onto Innovation 1Q26 results：<https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Reports-2026-First-Quarter-Results/default.aspx>
- KLA FY2026 Q3 results：<https://ir.kla.com/news-events/press-releases/detail/514/kla-corporation-reports-fiscal-2026-third-quarter-results>
- Micron HBM4 for Vera Rubin：<https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin>
- NVIDIA Vera Rubin official：<https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx>
- NVIDIA Vera Rubin technical blog：<https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/>
- AMD/Samsung HBM4 collaboration：<https://news.samsung.com/global/samsung-and-amd-expand-strategic-collaboration-on-next-generation-ai-memory-solutions>

### 行业报告、会议与多方验证

- TrendForce HBM4 validation 2Q26：<https://www.trendforce.com/presscenter/news/20260213-12929.html>
- TrendForce CoWoS/CoPoS update：<https://www.trendforce.com/news/2026/04/16/news-tsmc-says-cowos-offers-industrys-largest-reticle-size-packaging-amid-intel-emib-rivalry-copos-advances/>
- Gartner semiconductor 2026 outlook：<https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026>
- Chiplet Summit 2026 program：<https://chipletsummit.com/2026-program-at-a-glance/>
- Chiplet Summit 2026 keynote schedule：<https://chipletsummit.com/wp-content/uploads/2026/02/CS2026_NR_-2.2.26-Keynote-Schedule-Announced.pdf>
- SEMICON Korea 2026 advanced packaging sessions：<https://www.semiconkorea.org/en/node/5441>

### 项目内底座

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_AI芯片先进封装_2026.md`
- `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_封装基板_中介层与RDL_2026-05-08.md`
- `D:\drive\Investment\调研\v5\AI服务器_存储_芯片\行业调研_先进封装材料与热界面材料_2026.md`
- `D:\drive\Investment\调研\v5\conference_update\chiplet_summit_2026_update.md`
- `D:\drive\Investment\调研\v5\conference_update\nvidia_gtc_2026_research.md`

## 11. 风险提示

1. 本报告对 AI 数据中心建设采用非常乐观假设；若 hyperscaler 开始严格压 token ROI、推迟 capex，设备订单会先反映。
2. Hybrid bonding 从 pilot 到 HVM 可能比资本市场预期慢，尤其是 D2W throughput、surface cleanliness、void 和 repair/rework 问题。
3. HBM4/HBM4E 若验证延迟，2027 设备放量会推后，但 TCB/test/probe 的短期需求仍较强。
4. TSMC/Samsung/Intel/OSAT 的产能释放可能改变设备订单节奏；名义产能释放不等于良率产出。
5. 地缘、出口管制、台湾电力/水/气体、日本材料、韩国 HBM 任何扰动都会放大先进封装链条波动。
# 行业调研：【先进封装湿化学与表面处理材料】

> 截至日期：2026-05-08  
> 研究口径：聚焦 AI GPU/XPU、HBM、2.5D/3D、CoWoS/CoWoS-like、RDL/PLP、IC 载板、hybrid bonding、TGV/玻璃基板相关的湿化学与表面处理材料。包括电镀液与添加剂、化学镀/浸镀、RDL/UBM seed etchant、厚胶剥离与残胶清洗、post-CMP clean、CMP slurry/pad 中先进封装增量、临时键合解胶/残胶清洗、IC 载板 SAP/mSAP 湿制程、ENIG/ENEPIG/EPIG/贵金属表面处理、玻璃/陶瓷/硅表面活化及清洗。  
> 不包括：前道大宗湿电子化学品的全市场、普通 PCB 通用化学品、纯设备收入、TIM/underfill/EMC 等已在项目内其他材料报告覆盖的非湿制程材料。  
> 方法说明：AI 芯片技术路径和出货排序引用本项目已有 `ai_chip_research_2026_2027.md`、先进封装/基板/材料报告；外部检索重点放在最近半年公司公告、产品页、论坛信息、行业报告摘要。缺少直接公开数据的细分环节，用 CoWoS/HBM/AI 载板产能、单位工艺消耗、供应商公告和 TECHCET/SEMI/公司财报做乐观推演。

## 0. 一页结论

先进封装湿化学与表面处理材料是 2026 AI 算力扩建里最容易被低估的“微小但不可替代”的耗材层。它不直接决定 GPU 算力，却决定 HBM、RDL、Cu pillar、micro-bump、IC 载板、TSV/TGV、hybrid bonding 表面能不能做到足够低缺陷、低离子污染、低 void、低翘曲和可量产。2026 最确定的放量路径不是遥远的玻璃基板，而是：

1. **RDL / micro-via / Cu pillar 的铜电镀和添加剂**：CoWoS-L/S、FOWLP、PLP、FC-CSP、HBM package 的共同基础。
2. **UBM/RDL seed layer 铜/钛刻蚀、厚胶剥离、post-plating clean**：细线 RDL、microbump、Cu/Ni/Au RDL 和 Ni/Au pad 进入高密度窗口后，CD loss、undercut、金属残留变成良率变量。
3. **IC 载板 SAP/mSAP 湿制程**：AI 载板层数、面积、线宽线距、via-in-pad、铜粗糙度要求提升，带动 desmear、electroless Cu、acid Cu via fill、etch/roughening、表面粗化和 final finish。
4. **CMP slurry + post-CMP clean 在先进封装中的再定价**：TSV Cu reveal、RDL/interposer planarization、Cu hybrid bonding 表面平坦度和颗粒控制使 CMP 从前道逻辑延伸到先进封装核心。
5. **ENIG/ENEPIG/EPIG/贵金属表面处理**：高频、高可靠、可焊/可键合界面需求增长；金、钯、银价格传导与客户认证共同决定利润。
6. **hybrid bonding / HBM4 / TGV 相关表面处理**：2026 是验证和小量导入，2027 开始放量，是赔率最高方向。

### 0.1 核心数字

| 指标 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 方向 |
|---|---:|---:|---:|---|
| 全球 AI 计算芯片/模块产能释放金额，项目内锚点 | $300B-$360B | $390B-$470B | $520B-$650B | 2027 极超可达 $850B-$1,050B |
| AI/HPC 先进封装服务收入池，项目内锚点 | $32B-$45B | $45B-$62B | $65B-$85B | 2028 可到 $90B-$140B |
| 全球先进封装湿化学与表面处理材料收入池，不含普通 PCB | $4.2B-$5.3B | $5.5B-$7.0B | $7.5B-$9.5B | 2027 基准 $6B-$8B，极超 $12B-$16B |
| 其中，先进封装金属电镀/化学镀/表面处理 | $0.85B-$1.15B | $1.1B-$1.55B | $1.55B-$2.15B | HBM4、PLP、TGV 拉动，2027 可到 $1.5B-$3.5B |
| 其中，IC 载板 SAP/mSAP 湿制程化学品 | $1.2B-$1.8B | $1.7B-$2.5B | $2.4B-$3.5B | 高端 ABF/FC-BGA 载板紧缺时最直接受益 |
| 其中，CMP/post-CMP/清洗/剥离/刻蚀先进封装增量 | $1.6B-$2.4B | $2.2B-$3.2B | $3.0B-$4.5B | hybrid bonding 和 TGV 会扩大单位价值 |
| 湿化学与表面处理材料价值量/高端 AI GPU 或 XPU package | $80-$220 | $160-$420 | $300-$800 | HBM4、12-16H、panel RDL、Cu bonding 后继续上升 |
| 领先配方型材料毛利率 | 45%-60% | 55%-68% | 65%-75% | 高壁垒添加剂、post-CMP clean、hybrid bonding clean 最强 |
| 大宗酸碱溶剂/低壁垒清洗剂毛利率 | 15%-30% | 20%-35% | 30%-45% | 仅在本土替代或短缺时有超额利润 |

公开市场锚点：TECHCET 2025-2026 Metal Chemicals 报告公开摘要显示，2025 年全球 plating chemicals 市场约 **$1.381B**，其中铜电镀化学品分为 device interconnect 约 **$495M** 与 advanced packaging 约 **$509M**；其报告明确覆盖 Cu pillar、micro-bump、WLP、RDL、TSV。这个数字只覆盖金属电镀化学品，不含 seed etchant、stripper、post-CMP clean、IC 载板大部分湿制程、临时键合解胶和 final finish 贵金属 pass-through，因此本文对“先进封装湿化学与表面处理材料”的总收入池估算显著大于单一 plating chemicals 报告。

### 0.2 最近半年一手/准一手信号

| 时间 | 来源 | 关键信号 | 对本行业含义 |
|---|---|---|---|
| 2026-05-06 | MKS Q1 2026 | Q1 revenue $1.078B；Electronics & Packaging revenue $321M，同比 +27%；公司称 AI-related applications 投资拉动 semiconductor 与 advanced circuit board manufacturing 复杂度上升。 | Atotech 的湿化学、电镀、PCB/IC substrate process chemistry 与 ESI laser drilling 同处 AI 载板/先进封装扩张链条。 |
| 2026-04-28 | Element Solutions / MacDermid Alpha Q1 2026 | 公司称 high-end electronics demand strong，datacenter hardware 技术要求提升，业务提供 thermal management、power density、advanced packaging 关键方案；2026 完成 Micromax 与 EFC Gases & Advanced Materials 收购。 | MacDermid Alpha 在 IC substrate、PLP、Cu pillar、SAP、final finish 和 assembly materials 的组合更完整；AI 载板和 advanced packaging 是其最高价值 niche。 |
| 2026-04-30 | Entegris Q1 2026 | Q1 net sales $812M；Materials Solutions 包括 CMP slurries/pads、formulated etch and clean；APS 提供 filtration、purification 和 contamination control。 | 先进封装湿制程从“化学品”升级为“化学品 + 过滤/纯化 + defect control”系统；post-CMP/hybrid bonding clean 对颗粒和金属离子极敏感。 |
| 2026-02 至 2026-05 | Qnity 独立上市后材料组合 | Qnity 由 DuPont semiconductor/interconnect 业务分拆，2025 full-year net sales $4.75B；AI/HPC 相关页面列出 CMP slurries、EKC removers/clean chemistries、WLP photoresist removers & TSV cleaners、copper pillar plating、copper RDL、solder bump、TSV copper、UBM 等产品。 | Qnity 是先进封装湿化学/光刻/介质/组装材料最完整的平台型供应商之一。 |
| 2026-03 | IMAPS Device Packaging Conference 2026 | 主题覆盖 AI data center workloads、AMD future AI hardware enabled by advanced packaging、Hybrid Bonding、Advanced Fan-Out in wafer-to-panel、glass core substrates、TIM reliability 等。 | 会议议题表明先进封装技术主战场已经从单一封装服务转向材料、清洗、表面准备、基板、热和可靠性一体化。 |
| 2026-02 | SEMICON Korea 2026 | 韩国 HBM、advanced packaging、smart manufacturing 成为技术路线核心；Merck 展示面向 GAA、DRAM、3D NAND、HBM、advanced packaging 的材料方案。 | 韩国 HBM 扩产会同步拉动 Cu plating、CMP、clean、surface prep、temporary bonding 和 contamination control。 |
| 2026-04 | Resonac US-JOINT / JOINT3 | Resonac 牵头材料/设备公司开发 next-generation semiconductor packaging，JOINT3 的 APLIC 原型线计划 2026 运营；US-JOINT 在硅谷启动。 | 日本材料公司把 advanced packaging 研发从单点材料推向“共创工艺线”，湿化学/表面处理必须和设备、基板、bonding、检测协同。 |
| 2025-11 | TECHCET Metal Chemicals | 全球 plating chemicals 2025 约 $1.381B，advanced packaging 铜电镀约 $509M；MKS/Atotech 泰国 $40M chemical plant、Moses Lake Industries Arizona $100M 高纯电解质/Cu plating R&D、MacDermid Alpha MICROFAB SC-40 PLUS 为公开提及产业动向。 | 电镀化学品已从成熟 PCB/前道辅材转为 AI/HPC advanced packaging 的增量耗材池。 |
| 2026 产品页 | Atotech、MacDermid Alpha、Technic、Uyemura、Chemleader、Anji、Shanghai Sinyang | Atotech Spherolyte 覆盖 Cu/Ni/Sn/Au pillar/RDL；MacDermid Alpha Systek SCP 100 指向 AI/HPC PLP；Chemleader 称台湾 packaging Cu/Ti etchant 年处理超 20M wafers；Anji 公开 TSV/RDL/bumping ECP、hybrid bonding polishing slurry；上海新阳公开 Bump/TSV/RDL 湿法设备与电镀添加剂。 | 先进封装湿化学不是单一配方，而是围绕 RDL、pillar、TSV、载板、表面刻蚀和清洗形成工艺包。 |

## 1. AI 计算中心大规模建设下的机遇、挑战与技术路径

### 1.1 为什么 AI 放量会直接拉动湿化学与表面处理

AI GPU/XPU 的先进封装价值量上升，本质是四个物理量同时上升：**HBM stack 数、RDL/bridge 面积、micro-bump/Cu pillar 数量、IC 载板层数与面积**。每一个变量都需要更多湿制程：

- HBM 与 GPU/XPU 之间需要 RDL、UBM、micro-bump、Cu pillar、SnAg cap、Ni barrier、Cu seed etch、photoresist strip、defect clean。
- CoWoS-L/CoWoS-R/RDL interposer 需要更大面积电镀、湿刻、CMP 和聚合物残留清洗；大面积后厚度均匀性、应力、dishing、void、undercut 被放大。
- 高端 ABF/FC-BGA 载板需要 SAP/mSAP：desmear、electroless copper、acid copper via fill、pattern plating、flash etch、roughening、final finish。
- Hybrid bonding 需要极低颗粒、低金属残留、低有机残留、可控 Cu recess/protrusion；post-CMP clean 和表面活化前清洗价值显著上升。
- 玻璃基板/TGV 需要玻璃表面活化、种子层沉积后的电镀、TGV 填充、玻璃/金属界面 adhesion promotion、湿刻与清洗。

### 1.2 2026 正在使用的关键湿化学/表面处理技术

| 技术 | 2026 使用状态 | 核心材料/化学品 | 关键性能指标 |
|---|---|---|---|
| RDL 铜电镀 | CoWoS、FOWLP、PLP、FC-CSP 主流 | Cu sulfate/MSA base、accelerator/suppressor/leveler、wetting agent、grain refiner | 厚度均匀性、低应力、低 impurity、2/2 到 5/5 um 级 L/S 兼容、低 void |
| Cu pillar / micro-bump 电镀 | Flip-chip/HBM/WLP 大量使用 | Cu plating、Ni barrier、SnAg solder cap、Au/Pd/Ni 选择性镀层 | pillar coplanarity、flat/domed profile、Kirkendall void 抑制、低 ppm impurity |
| UBM/RDL seed etch | 晶圆级封装刚需 | Cu etchant、Ti/TiW etchant、residue remover、inhibitor | 低 undercut、低 CD loss、无金属残留、兼容 Cu/Ni/Au RDL 和 Ni/Au pad |
| 厚胶剥离与 post-plating clean | bumping/RDL/TSV 后必需 | Bump PR stripper、semi-aqueous stripper、amine/solvent/low-metal formulations、rinse | 去除厚 PR、plasma-hardened residue、兼容 Cu/SnAg/Ni/Au/PI/PBO |
| CMP / post-CMP clean | TSV Cu reveal、RDL planarization、hybrid bonding 前处理 | Cu/barrier/polymer slurry、pads、brush clean、chelating cleaner、corrosion inhibitor | 平坦度、低 scratch、低 Cu corrosion、低 particles、Cu recess/protrusion 控制 |
| IC 载板 SAP/mSAP | AI ABF/FC-BGA 满载 | permanganate/plasma desmear 配套、electroless Cu、acid Cu via fill、flash etch、roughening、solder mask developer | via fill void-free、fine line uniformity、低粗糙度/低损耗、强 adhesion |
| ENIG/ENEPIG/EPIG/final finish | IC 载板、memory/power/package pad 使用 | electroless Ni/Pd/Au、immersion Au/Ag/Sn、anti-tarnish、Pd activator/inhibitor | wire bonding/solderability、HF loss、Ni corrosion 控制、gold thickness |
| 临时键合解胶/残胶清洗 | 2.5D/3D、thin wafer handling | debond cleaner、adhesive residue remover、edge bead/remover、low-metal solvent | 对薄晶圆低应力、低残胶、低离子污染、设备配套 |
| Hybrid bonding 表面准备 | 2026 验证/小批量，2027 放量 | post-CMP clean、Cu oxide control、surface conditioning、DI/megasonic clean | sub-nm roughness、颗粒密度、Cu dishing/recess、表面亲水性 |
| TGV/玻璃基板湿制程 | 2026 pilot，2027 design-in | glass surface activation、seed adhesion promoter、Cu/Ti etch、via fill plating、clean | 玻璃-金属 adhesion、CTE/应力、TGV void-free、panel uniformity |

### 1.3 出货量最大的 AI 芯片路径与湿化学映射

以下芯片排序和技术路径来自项目内已有 AI 芯片研究，本报告只抽取对湿化学/表面处理的影响。

| AI 芯片/平台 | 2026-2027 阶段 | 封装/内存路径 | 直接拉动的湿化学与表面处理 |
|---|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | 2026 最大主力 | TSMC 4NP + CoWoS-L/S + HBM3E + 大 ABF | RDL Cu plating、Cu pillar/SnAg/Ni、UBM seed etch、thick PR strip、post-plating clean、IC substrate SAP/mSAP、ENEPIG、post-CMP clean |
| AWS Trainium2 | 2026 大规模部署 | HBM + custom ASIC package + 64-chip UltraServer | HBM/WLP metallization、RDL/载板湿制程、系统级高可靠 final finish |
| Google TPU v7 Ironwood | 2026 云端放量 | Broadcom/TSMC XPU + HBM3E | ASIC 2.5D/RDL、Cu plating、CMP clean、IC substrate final finish |
| NVIDIA B200/GB200 | 存量大，2026 继续交付 | CoWoS + HBM3E | 成熟 CoWoS 湿制程打底，维持 plating/etch/strip 高稼动 |
| Huawei Ascend 910C/950 | 中国国产替代主力 | 本土 2.5D/HBM/超节点 | 国产 Bump/TSV/RDL 电镀液、清洗剂、刻蚀剂、载板化学品进口替代 |
| Cambricon MLU 590/690 | 2026 目标上量 | 国产先进封装 + HBM/OAM | 本土 OSAT/基板湿制程、RDL/bump 试产到量产爬坡 |
| AMD MI350 | 2026 AMD 最确定放量 | 2.5D + HBM3E + OAM/UBB/PCIe | 与 GB200/GB300 类似，另拉动 UBB/PCIe 载板湿制程 |
| AWS Trainium3 | 2026 初放量，2027 主力 | 3nm + HBM + 144-chip UltraServer | high-density ASIC package 的 RDL/载板/清洗/表面处理升级 |
| Meta MTIA 300/400/450/500 | 2026-2027 多代 ASIC | Broadcom XPU + advanced packaging | 大规模推理 ASIC 让湿化学需求从 NVIDIA 单客户外溢到 CSP ASIC |
| Microsoft Maia 200 | 2026 Azure 推理导入 | TSMC 3nm + 216GB HBM3E + 液冷 | HBM3E 封装湿制程、RDL、UBM、clean、substrate finish |
| NVIDIA Rubin / AMD MI400 / TPU8 / OpenAI-Broadcom XPU | 2026H2 小量，2027 放量 | HBM4 + 更大 2.5D/3D + 部分 hybrid bonding | HBM4 相关 microbump/hybrid、post-CMP clean、Cu recess control、CoWoS-L/RDL 大面积电镀、TGV/玻璃基板期权 |

### 1.4 新技术成熟与放量时间表：三情景

| 技术 | 2026 基准 | 2026 乐观 | 2026 极度超预期乐观 | 2027 基准/乐观 |
|---|---|---|---|---|
| CoWoS/RDL 铜电镀化学品 | GB300/GB200/MI350/TPU/Trainium 已满载；新增需求主要来自 CoWoS-L/RDL 面积扩大 | OSAT 与载板厂承接更多 RDL/PLP 工艺，Cu additive 订单提前锁到 2027 | 客户为交期接受高价配方、专线供应和 bath analytics 服务，供应商提价 10%-25% | 2027 随 Rubin/MI400/OpenAI ASIC 放量，市场继续 +40%-80% |
| Cu pillar/micro-bump/SnAg/Ni | 2026 高端封装标准配置，pitch 继续缩小 | HBM4 early ramp 对低 void/低 impurity 配方提出更高要求 | 16H HBM 和高 I/O ASIC 同步上量，供应链出现局部短缺 | 2027 HBM4 主力化，Cu pillar 与 hybrid bonding 并存 |
| UBM/RDL seed etch + thick PR strip | 成熟放量；细线 RDL 下 CD loss 和金属残留成为痛点 | 先进 RDL 与 PLP 使高选择性 etchant/stripper 单价提高 | 若 panel-level 早量产，低缺陷 etch/strip 用量超线性增长 | 2027 随 RDL/PLP/CoWoS-R/L 扩大，成为高增长耗材 |
| Advanced packaging CMP/post-CMP clean | TSV/RDL/hybrid bonding 早期应用扩大 | Cu hybrid bonding 认证顺利，post-CMP clean 进入关键材料清单 | HBM4/SoIC/ASIC 多平台提前采用，缺陷控制供应商获得溢价 | 2027 成为高端 3DIC/hybrid bonding 默认流程 |
| IC 载板 SAP/mSAP 湿制程 | 高端 ABF/FC-BGA 满载，载板湿化学跟随放量 | AI substrate 涨价传导至化学品，客户愿意买整套 process package | AI 载板短缺严重，via fill/roughening/final finish 产能与化学品被锁定 | 2027 高端 ABF 继续紧，普通载板分化 |
| Hybrid bonding surface prep | 2026 多为验证、小量生产 | Rubin/MI400/TPU8/SoIC 带动 Q4 明显收入 | 客户把 Cu-Cu bonding 当作 HBM4 后下一代架构核心，提前锁材料 | 2027 渗透率从个位数走向 10%-25% |
| Glass substrate/TGV wet chem | 2026 pilot 和客户认证 | 2027H1 有少量 ASIC/switch design-in | 2027H2 进入高端 AI ASIC 小批量，TGV plating/etch/clean 起量 | 真正大规模更可能在 2028-2029，但 2027 是设计胜出年 |
| PFAS-free/低 VOC/低氰贵金属体系 | 法规与客户 ESG 推动，短期替代慢 | 高端客户为供应链安全付溢价 | 欧盟/美国监管加速，老配方切换带来再认证机会 | 2027-2028 绿色配方成为差异化壁垒 |

### 1.5 2026 最可能的技术路径

2026 最可能放量的不是最激进的 full hybrid bonding，而是“成熟湿制程的高规格化”：

1. **Cu RDL + Cu pillar + SnAg/Ni cap/barrier + UBM seed etch + thick PR strip**：确定性最高，贯穿 GB300、GB200、MI350、Ironwood、Trainium、Maia、MTIA。
2. **IC 载板 SAP/mSAP + final finish**：受 AI ABF 载板面积和层数直接驱动，MKS/Atotech、MacDermid Alpha、Uyemura、JCU、Okuno、Chemleader、上海新阳等均在该链条。
3. **CMP/post-CMP clean for TSV/RDL/hybrid bonding**：2026 订单弹性来自 HBM4 和 SoIC/3DIC 认证，2027 才是大收入。
4. **大面积 RDL/PLP 湿制程**：从晶圆级向 panel-level 迁移，要求高均匀性、bath lifetime、在线分析和低缺陷。
5. **国产替代链**：中国 AI 芯片在先进节点受限，系统级并联和本土封装需求反而使 Bump/TSV/RDL 湿化学品成为进口替代重点。

## 2. 已经开始放量的关键产品：市场规模、渗透率、利润率

以下市场规模为全球 advanced packaging 相关收入池估算，不等同于单家公司营收。“未来 3 个月”按 2026-05-08 至 2026-08-08，“未来 1 年”按至 2027-05，“未来 2 年”按至 2028-05。

### 2.1 已放量产品总表

| 已放量产品/细分技术 | 当前状态 | 未来 3 个月市场规模：基准/乐观/极超 | 未来 1 年市场规模：基准/乐观/极超 | 未来 2 年市场规模：基准/乐观/极超 | 渗透率路径 | 主要公司 |
|---|---|---:|---:|---:|---|---|
| Advanced packaging Cu RDL / micro-via / TSV plating chemicals | CoWoS、FOWLP、PLP、TSV 均已用；TECHCET 2025 AP 铜电镀约 $509M 为锚 | $170-240M / $230-330M / $330-470M | $0.75-1.05B / $1.05-1.50B / $1.50-2.10B | $1.35-2.00B / $2.0-3.0B / $3.1-4.6B | 高端 2.5D/RDL attach 2026 70%-85%，2028 85%-95%；fine-line RDL 单价上升 | MKS/Atotech、MacDermid Alpha、Qnity、Technic、JCU、Uyemura、Okuno、Shanghai Sinyang、Anji、Jiangsu Aisen |
| Cu pillar / micro-bump / SnAg / Ni barrier plating | Flip-chip、HBM、WLP 主流；AI 高 I/O 密度抬升要求 | $120-200M / $180-280M / $260-420M | $0.55-0.90B / $0.85-1.35B / $1.30-2.00B | $1.0-1.7B / $1.6-2.8B / $2.6-4.3B | 高端 AI package 几乎 100% 使用金属凸点或等价互连；HBM4 后向 finer pitch/hybrid 迁移 | MacDermid Alpha、MKS/Atotech、Qnity、Technic、Uyemura、TANAKA、Mitsubishi Materials、JCU、Anji |
| IC 载板 SAP/mSAP 湿制程：desmear、electroless Cu、acid Cu via fill、flash etch、roughening | AI ABF/FC-BGA 满载，载板厂高稼动 | $300-460M / $430-650M / $620-900M | $1.25-1.85B / $1.85-2.70B / $2.70-3.90B | $2.2-3.5B / $3.4-5.5B / $5.2-8.0B | 高端 AI substrate attach 接近 100%；mSAP/fine-line 在 AI substrate 占比从 2026 35%-50% 到 2028 55%-75% | MKS/Atotech、MacDermid Alpha、Uyemura、JCU、Okuno、Meltex、DuPont/Qnity、Chemleader、Shanghai Sinyang、Guangzhou Sanfu |
| UBM/RDL Cu/Ti/TiW seed etchants | RDL、Cu pillar、microbump、Ni/Au pad 必需 | $95-160M / $140-230M / $210-340M | $0.42-0.72B / $0.70-1.10B / $1.05-1.65B | $0.80-1.45B / $1.35-2.35B / $2.10-3.60B | 先进 RDL 2026 50%-65%，2028 70%-85%；fine-line RDL 提高高选择性 etchant 渗透 | Chemleader、MKS/Atotech、Qnity、Kanto Chemical、Mitsubishi Chemical、Shanghai Sinyang、Jianghua Micro、Crystal Clear |
| Bump/RDL thick PR stripper、post-plating residue remover、wet clean | Bumping、RDL、TSV 后段高频使用 | $120-210M / $180-300M / $280-450M | $0.55-0.95B / $0.90-1.45B / $1.40-2.25B | $1.05-1.90B / $1.8-3.1B / $3.0-5.0B | 先进封装 wafer-level process 近 100%；高端低金属/低腐蚀配方渗透提升 | Qnity/EKC、Entegris、Merck/EMD、Fujifilm、TOK、JSR、Brewer Science、Anji、PhiChem、Shanghai Sinyang |
| CMP slurry/pad/post-CMP clean for TSV/RDL/advanced packaging | TSV Cu reveal、RDL planarization、hybrid bonding 前处理开始放量 | $150-250M / $220-360M / $330-520M | $0.70-1.15B / $1.05-1.70B / $1.60-2.60B | $1.4-2.5B / $2.4-4.2B / $4.0-7.0B | 先进封装 CMP attach 2026 20%-35%，2028 45%-65%；hybrid bonding 节点几乎 100% 依赖 | Entegris/CMC、Qnity、Fujimi、Resonac、Merck、Fujifilm、Anji、Soulbrain、KC Tech materials |
| ENIG/ENEPIG/EPIG/immersion Au/Ag/Sn final finish | IC 载板、memory、power、wire bond/flip chip 使用 | $130-240M / $190-340M / $300-520M | $0.60-1.10B / $0.95-1.70B / $1.55-2.80B | $1.1-2.0B / $1.9-3.4B / $3.2-5.8B | AI substrate 可靠性要求提高，ENEPIG/EPIG 在高频/高可靠占比上升；贵金属 pass-through 增加金额弹性 | Uyemura、MKS/Atotech、MacDermid Alpha、JCU、Okuno、TANAKA、Japan Pure Chemical、Umicore、Mitsubishi Materials |
| 临时键合解胶/残胶清洗、edge clean | 薄晶圆、2.5D/3D、fan-out 量产线使用 | $45-90M / $80-140M / $130-220M | $0.22-0.45B / $0.40-0.75B / $0.70-1.20B | $0.55-1.10B / $1.0-2.0B / $1.8-3.5B | advanced packaging thin wafer handling 2026 30%-50%，2028 60%-75% | Brewer Science、3M、TOK、JSR、Qnity、Merck、Fujifilm、Shin-Etsu、Resonac |
| 高纯化学品过滤/纯化/在线分析与 bath control 消耗品 | 与湿化学配套，缺陷控制要求上升 | $120-220M / $180-320M / $300-500M | $0.55-1.0B / $0.9-1.6B / $1.5-2.6B | $1.1-2.1B / $2.0-3.6B / $3.4-6.2B | 高端封装湿线 attach 2026 40%-60%，2028 70%-85%；客户从单买化学品转向 process control package | Entegris、MKS、Pall/Danaher、Merck、Nippon Pillar、Organo、Kurita、RION/Particle Measuring Systems |

### 2.2 三情景增长与利润率

| 产品 | 基准：未来 1 年增长/利润率 | 乐观：未来 1 年增长/利润率 | 极度超预期：未来 1 年增长/利润率 | 为什么能定价 |
|---|---|---|---|---|
| Cu RDL/TSV plating additives | +35%-60%；GM 45%-60%，OPM 18%-30% | +60%-95%；GM 55%-68% | +110%+；GM 65%-75% | 添加剂配方决定 void、grain、stress、uniformity；客户换配方要重新跑可靠性和 bath window |
| Cu pillar/SnAg/Ni/Au plating | +30%-55%；GM 40%-58% | +55%-85%；GM 50%-65% | +100%+；GM 60%-72% | pillar coplanarity、SnAg cap、Ni barrier 直接影响焊点和 HBM package 可靠性 |
| IC substrate SAP/mSAP 湿制程 | +25%-45%；GM 30%-48%，高端添加剂更高 | +45%-75%；GM 40%-58% | +90%+；GM 55%-68% | AI 载板良率是硬瓶颈，化学品占成本低但影响 via fill、adhesion、roughness |
| Seed etchant | +35%-65%；GM 35%-55% | +65%-100%；GM 45%-62% | +120%+；GM 55%-70% | fine-line RDL 下 undercut/CD loss 是直接良率指标，台湾/韩国/中国本土化供应链各有锁定 |
| PR stripper / residue remover | +35%-60%；GM 38%-58% | +60%-95%；GM 50%-65% | +100%-150%；GM 60%-72% | 厚胶、plasma-hardened residue、金属兼容性难，低金属/低腐蚀配方壁垒高 |
| CMP slurry/post-CMP clean | +40%-70%；GM 45%-62% | +75%-120%；GM 55%-70% | +150%+；GM 65%-78% | hybrid bonding 表面颗粒和平坦度要求极严，客户锁定和认证周期长 |
| ENEPIG/贵金属表面处理 | +25%-50%；headline GM 15%-35%，不含金属 pass-through 的配方/服务 GM 40%-60% | +45%-75%；GM 25%-45% | +90%+；GM 35%-55% | Au/Pd/Ni 厚度、腐蚀、wire bond/solderability 认证强；贵金属价格可传导 |
| Temporary bonding/debond cleaners | +45%-80%；GM 45%-65% | +80%-130%；GM 58%-72% | +150%+；GM 70%+ | 胶材、设备、晶圆厚度和客户流程强耦合，一旦认证切换难 |
| Bath analytics / filtration consumables | +30%-55%；GM 40%-60% | +55%-90%；GM 50%-65% | +100%+；GM 60%-72% | 高端湿线的缺陷来源越来越微小，在线监控和过滤从可选变必选 |

## 3. 在研关键产品和快速增长技术

### 3.1 在研/早期导入总表

| 在研或即将快速增长技术 | 当前阶段 | 未来 3 个月市场规模：基准/乐观/极超 | 未来 1 年市场规模：基准/乐观/极超 | 未来 2 年市场规模：基准/乐观/极超 | 渗透率路径 | 利润率判断 |
|---|---|---:|---:|---:|---|---|
| Hybrid bonding surface prep：Cu CMP clean、oxide clean、Cu recess control、pre-bond clean | 2026 多平台验证/小量生产 | $30-70M / $70-130M / $120-220M | $0.20-0.45B / $0.45-0.90B / $0.85-1.60B | $0.90-1.80B / $1.8-3.6B / $3.5-6.5B | AI package 中 2026 <8%，2027 10%-25%，2028 25%-45% | GM 60%-78%；缺陷率和客户认证赋予定价权 |
| HBM4/16H microbump/hybrid plating & clean | HBM4 2026H2 early ramp | $40-90M / $90-170M / $160-300M | $0.30-0.65B / $0.65-1.20B / $1.1-2.0B | $1.2-2.5B / $2.4-4.8B / $4.5-8.0B | HBM4 在高端新增 HBM 中 2026 5%-15%，2027 35%-60% | 早期 GM 60%-75%，HBM 客户认证强 |
| Panel-level RDL/PLP high-uniformity plating/etch/strip | MacDermid Alpha、MKS/Atotech、ASMPT NEXX、RENA 等配套推动 | $50-120M / $100-220M / $200-380M | $0.35-0.75B / $0.70-1.40B / $1.3-2.5B | $1.3-2.8B / $2.7-5.5B / $5.0-9.0B | 2026 以 fan-out/PLP 为主，2027 在 ASIC/大 RDL 中占比提高 | GM 50%-70%；panel 均匀性和 bath stability 是壁垒 |
| TGV/玻璃基板 via fill plating、玻璃表面活化、adhesion promotion | AGC/Intel/Samsung/SKC/TOPPAN/玻璃基板链验证 | <$30M / $40-90M / $90-180M | $0.12-0.35B / $0.35-0.80B / $0.75-1.50B | $0.8-1.8B / $1.8-4.0B / $3.8-7.5B | 2026 几乎全为 pilot，2027 design-in，2028 后才大规模 | 成功配方 GM 60%+，但早期良率和客户导入风险高 |
| Low-PFAS / low-VOC / cyanide-free Au/Ag/Pd 表面处理 | ESG 与法规推动，客户验证中 | $30-80M / $70-140M / $130-260M | $0.25-0.55B / $0.50-1.0B / $0.95-1.8B | $0.8-1.7B / $1.6-3.2B / $3.0-5.5B | 2026 5%-15%，2028 25%-45%，取决于法规和可靠性数据 | GM 45%-65%；环保合规可带来替代溢价 |
| CPO/硅光封装湿法清洗、Au/Sn/Ni metallization、光学界面清洁 | 交换芯片/硅光封装早期 | $20-60M / $50-110M / $110-220M | $0.20-0.45B / $0.45-0.90B / $0.85-1.7B | $0.8-2.0B / $1.8-4.5B / $4.0-8.5B | CPO 在 AI switch 2026 <5%，2027 5%-12%，2028 10%-25% | 毛利 45%-70%；失效成本高但量产节奏不确定 |
| Backside power / embedded power substrate wet chem | 设计导入与高端载板早期应用 | $20-50M / $50-100M / $100-200M | $0.15-0.35B / $0.35-0.75B / $0.70-1.40B | $0.7-1.6B / $1.5-3.2B / $3.0-6.0B | 2027 起随 2nm/AI package PDN 压力上升 | GM 50%-70%；材料/工艺共设带来锁定 |
| AI 国产封装湿化学替代：Bump/TSV/RDL/清洗/刻蚀整包 | 中国本土客户验证加速 | $70-140M / $120-240M / $220-420M | $0.45-0.90B / $0.85-1.60B / $1.5-2.8B | $1.1-2.3B / $2.2-4.5B / $4.0-7.5B | 中国高端封装国产化率 2026 10%-25%，2028 25%-45% | 局部 GM 50%+；最大风险是稳定性和头部客户认证 |

### 3.2 未来最可能快速增长的关键产品

1. **Hybrid bonding post-CMP clean / pre-bond surface prep**  
   这是 2027 最像“新电镀添加剂”的品类。Cu-Cu hybrid bonding 对颗粒、氧化层、有机残留、Cu recess/protrusion 的容忍度比传统 micro-bump 小很多；客户愿意为减少 void、提高 bond yield 和长期可靠性付高价。

2. **HBM4 相关 plating/cleaning package**  
   Rubin、MI400/MI455X、TPU8、OpenAI/Broadcom XPU 都指向 HBM4。即使 2026 只有小量收入，2026H2 的材料认证会决定 2027 供应商份额。

3. **Panel-level RDL wet process**  
   如果 AI ASIC 为降低成本和扩大封装面积采用 PLP/large panel RDL，湿化学的挑战会从“单 wafer 精度”变成“大 panel 均匀性 + bath control + 低缺陷 + 低应力”。MacDermid Alpha Systek SCP 100 这类面向 PLP 的高纯 Cu pillar/RDL 电镀产品就是方向信号。

4. **TGV/玻璃基板 via fill plating 与玻璃表面活化**  
   玻璃基板 2026 不是收入主线，但一旦 2027 获得高端 ASIC 或 CPO switch design-in，湿法金属化、TGV 填充、表面活化、Cu/Ti etch 会快速从试剂变成工艺包。

5. **低污染、低腐蚀、低金属离子的 stripper/cleaner**  
   RDL、Cu/Ni/Au、SnAg、PI/PBO、temporary bonding 胶材共存，普通强剥离剂容易伤金属或介质。高端配方会按“少一个缺陷点”定价。

## 4. 供给侧：产能结构、瓶颈、成本与价格传导

### 4.1 产能结构：地区、公司、工艺

| 环节 | 主要地区 | 主要公司 | 工艺/产品 |
|---|---|---|---|
| 先进封装电镀/化学镀材料 | 美国、德国、日本、台湾、中国、韩国 | MKS/Atotech、MacDermid Alpha、Qnity、Technic、Uyemura、JCU、Okuno、TANAKA、Mitsubishi Materials、Japan Pure Chemical、Anji、Shanghai Sinyang、Jiangsu Aisen | Cu RDL、Cu pillar、SnAg、Ni barrier、Au/Pd、TSV/TGV plating、electroless/immersion final finish |
| IC 载板 SAP/mSAP 湿制程 | 日本、德国/美国、台湾、中国、韩国 | MKS/Atotech、MacDermid Alpha、Uyemura、JCU、Okuno、Meltex、Chemleader、Shanghai Sinyang、Guangzhou Sanfu、Jiangsu Aisen | desmear、electroless Cu、acid Cu via fill、flash etch、roughening、adhesion promotion、final finish |
| Etchants/strippers/cleaners | 美国、日本、德国、台湾、中国、韩国 | Qnity/EKC、Entegris、Merck/EMD、Fujifilm、TOK、JSR、Kanto Chemical、Chemleader、Anji、Shanghai Sinyang、PhiChem、Jianghua Micro、Crystal Clear、Soulbrain、Dongjin | Cu/Ti/TiW etch、PR strip、post-etch clean、post-plating clean、post-CMP clean、TSV cleaner |
| CMP slurry/pad/post-CMP clean | 美国、日本、德国、中国、韩国 | Entegris/CMC、Qnity、Fujimi、Resonac、Fujifilm、Merck、Anji、Soulbrain、KC Tech materials | TSV Cu reveal、RDL planarization、hybrid bonding CMP/post-CMP clean |
| Temporary bonding/debonding chemicals | 美国、日本、德国 | Brewer Science、3M、TOK、JSR、Qnity、Merck、Fujifilm、Shin-Etsu、Resonac | temporary bond adhesive remover、debond cleaner、residue remover、edge bead remover |
| 高纯化学品供应/过滤/纯化 | 美国、日本、德国、中国台湾、中国大陆、韩国 | Entegris、Merck/EMD、Kanto Chemical、FUJIFILM、Mitsubishi Chemical、Stella Chemifa、Jianghua Micro、Crystal Clear、Soulbrain、ENF、Dongjin、Organo、Kurita | UP acids/bases/solvents、filtration、purification、chemical delivery、bath monitoring |
| 先进封装湿法设备配套 | 美国、德国、日本、韩国、中国 | ASMPT NEXX、MKS/Atotech、ClassOne、RENA、ACM Research、SCREEN、TEL、SUSS/EVG 配套、上海新阳设备 | ECD/plating tools、single wafer clean、batch clean、develop/strip/etch/plating wet bench、bath analytics |

### 4.2 供给瓶颈：至少 10 条

1. **客户认证周期 6-18 个月**：plating additive、etchant、stripper、post-CMP clean 改动会影响电性、可靠性和失效率，客户不愿在一代 AI 芯片中频繁换料。
2. **高纯原料和低金属离子控制**：RDL/hybrid bonding 对 Na/K/Cl、过渡金属、颗粒、有机残留敏感；普通电子级化学品不能直接上高端封装线。
3. **电镀添加剂 know-how**：accelerator/suppressor/leveler 的配方和在线控制决定 void、grain、stress、dishing、uniformity；不是简单购买 Cu sulfate。
4. **Bath lifetime 与在线分析**：AI 载板/PLP 面积大，batch variation 会造成大面积报废；CVS、TOC、金属离子、颗粒监控成为产能一部分。
5. **高端 IC substrate 良率**：化学品只是成本小项，但 desmear、electroless Cu、via fill、roughening 一旦失控，会报废高价值 ABF 载板。
6. **贵金属供应与价格传导**：Au/Pd/Ag/Ni 价格波动影响 ENEPIG/EPIG/immersion finish，合同是否允许 pass-through 决定账面毛利。
7. **PFAS、氰化物、溶剂与废水法规**：高性能表面处理和清洗剂面临环保替代压力，合规能力弱的供应商会被淘汰。
8. **与设备强绑定**：同一配方在不同 ECD/wet bench/clean tool 上的流场、温控、过滤、搅拌窗口不同；设备-材料共同认证形成锁定。
9. **区域化供应链**：台湾 CoWoS/OSAT、韩国 HBM、日本材料、中国本土替代、美国 advanced packaging 回流并行，化学品需要在客户所在地建技术服务和危化物流能力。
10. **应用工程人才短缺**：先进封装湿化学卖的是配方 + 工艺窗口 + 失效分析，懂电化学、封装、可靠性和客户线体的 FAE 稀缺。
11. **TGV/玻璃基板技术不确定**：玻璃金属化 adhesion、TGV via fill、面板级均匀性、湿刻窗口未完全成熟，早期扩产有报废风险。
12. **国产替代的稳定性验证**：国内企业产品进入试产较快，但高端客户最关心 batch-to-batch、金属污染、长期可靠性和全球现场支持。

### 4.3 单位成本/BOM 拆分

#### 高端 AI package 对应湿化学与表面处理价值量

| 项目 | 2026 基准/颗 package | 乐观/极超 | 说明 |
|---|---:|---:|---|
| RDL/Cu pillar/UBM plating chemistry 分摊 | $20-$70 | $60-$180 | 包括 Cu、Ni、SnAg、Au/Pd 局部工艺；按 wafer/panel 消耗折算 |
| UBM/RDL etchant、stripper、post-plating clean | $15-$50 | $45-$130 | fine-line RDL 和 thick PR 越复杂越高 |
| CMP slurry/pad/post-CMP clean | $10-$45 | $40-$160 | hybrid bonding/TSV/RDL planarization 显著抬升 |
| IC substrate SAP/mSAP wet chemistry 分摊 | $25-$80 | $70-$220 | AI ABF 面积、层数、via fill、final finish 决定 |
| ENIG/ENEPIG/EPIG/immersion Au/Pd/Ag 分摊 | $5-$45 | $30-$140 | 受贵金属价格和 pad 面积影响大 |
| Filtration/bath analytics/chemical delivery consumables | $5-$30 | $25-$80 | 高端线体更像 process control package |
| 合计 | $80-$220 | $300-$800 | 不含封装服务费、载板主体材料、underfill、TIM、设备折旧 |

#### 配方型电镀/清洗材料成本构成

| 成本项 | 占比区间 | 毛利含义 |
|---|---:|---|
| 基础化学品：酸、盐、溶剂、氧化剂/还原剂 | 20%-40% | 大宗部分可多源，定价权弱 |
| 专有有机添加剂/络合剂/抑制剂/表面活性剂 | 10%-25% | 配方 know-how 集中，是超额毛利来源 |
| 高纯化、过滤、质量控制、批次追溯 | 10%-20% | 高端客户愿意为低缺陷付费 |
| 贵金属 pass-through：Au/Pd/Ag/Ni，视产品而定 | 0%-70% | 会抬高收入但压低 headline GM，需要看不含金属的服务/配方毛利 |
| 包装、危化物流、现场服务、废液支持 | 8%-18% | 区域服务能力决定客户锁定 |
| 研发、FAE、失效分析 | 8%-15% | 先进封装项目制开发费用可通过 NRE 或高价配方回收 |

### 4.4 毛利决定因素与价格传导机制

- **最强定价点**：专有电镀添加剂、post-CMP/hybrid bonding clean、低 undercut seed etchant、临时键合解胶、高端 ENEPIG/EPIG 工艺包。
- **中等定价点**：IC 载板 SAP/mSAP 常规制程化学品、成熟 Cu plating bath、普通 strippers。
- **弱定价点**：大宗酸碱、通用溶剂、普通 PCB 化学品，除非本土供应短缺或危化物流受限。
- **价格传导**：贵金属按公式传导；高端配方通过 LTA、NRE、process package、现场服务费和独家/半独家认证提价；大宗化学品通过季度价格调整和能源/物流附加费传导。
- **客户接受涨价的逻辑**：湿化学占高端 AI package 成本低于 1%-2%，但一次失效可能报废数万美元封装或延误整柜交付，因此客户更买“良率确定性”而不是最低单价。

## 5. 竞争格局、壁垒与价值捕获

### 5.1 市场结构：集中度估算

| 细分 | 市场集中度判断 | 头部公司 | 定价权 |
|---|---|---|---|
| Advanced packaging plating chemicals | CR5 约 55%-70%，高端客户更集中 | MKS/Atotech、MacDermid Alpha、Qnity、Uyemura、JCU/Okuno/Technic、TANAKA | 强，高端添加剂和客户认证锁定 |
| IC substrate SAP/mSAP wet chem | CR5 约 50%-65%，区域差异大 | MKS/Atotech、MacDermid Alpha、Uyemura、JCU、Okuno、Meltex、Chemleader | 中强，受载板厂和工艺包绑定 |
| Cu/Ti seed etchant | 台湾/韩国/中国区域龙头显著 | Chemleader、Qnity、Kanto、MKS、Shanghai Sinyang、Jianghua | 中强，fine-line RDL 高选择性配方有溢价 |
| Stripper / residue remover / clean | CR5 约 45%-60%，产品高度定制 | Qnity/EKC、Entegris、Merck、Fujifilm、TOK、JSR、Anji | 强，高端低金属配方粘性高 |
| CMP slurry/post-CMP clean | CR5 约 65%-80% | Entegris/CMC、Qnity、Fujimi、Resonac、Fujifilm、Merck、Anji | 很强，hybrid bonding 后更强 |
| ENIG/ENEPIG/final finish | CR5 约 55%-70% | Uyemura、MKS/Atotech、MacDermid Alpha、JCU、Okuno、TANAKA、Japan Pure Chemical | 中强，贵金属 pass-through 影响账面毛利 |
| 高纯大宗湿化学品 | 区域分散，前道更集中 | Kanto、Mitsubishi Chemical、Stella Chemifa、BASF/Merck、Jianghua、Crystal Clear、Soulbrain、ENF | 中低，纯度和物流带来区域壁垒 |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 可量化指标 | 为什么能定价 |
|---|---|---|
| 技术壁垒 | RDL L/S、pillar coplanarity、via fill void rate、Cu impurity ppm、particles/cm2、post-CMP defect density | 这些指标直接决定 package yield；客户愿意为低缺陷配方付费 |
| 认证壁垒 | 6-18 个月 qualification；多轮 reliability、thermal cycling、HAST、power cycling | 换料会错过 AI 芯片代际窗口，节省材料钱不值得 |
| 规模壁垒 | 全球/区域技术服务、危化仓储、批次追溯、在线分析能力 | 高端客户需要本地 FAE 和快速 failure analysis，不只是供货 |
| 客户锁定 | TSMC/ASE/Amkor/Samsung/SK hynix/载板厂 AVL | 一旦进入 AVL，生命周期内切换概率低，除非出现重大缺陷 |
| 设备绑定 | ECD/wet bench/CMP/clean tool 的流场、温度、过滤、CVS 控制 | 配方和设备共同形成 process window，后来者很难复制 |
| 数据壁垒 | bath aging、defect map、reliability database、客户失效案例 | 历史数据能缩短客户 ramp，形成隐性护城河 |
| 环保与合规 | PFAS、氰化物、重金属废水、危化运输许可 | 合规能力强的供应商在欧美/日韩/台湾高端线更有优势 |
| 原料控制 | 高纯 organics、贵金属盐、特殊络合剂、过滤膜 | 上游短缺时，拥有配方与供应链的厂商先保头部客户 |

### 5.3 价值链里最可能长期高 ROIC/高毛利的层

1. **专有电镀添加剂和整套 plating process package**：材料成本低、客户认证强、现场服务粘性高；MKS/Atotech、MacDermid Alpha、Qnity、Uyemura、Technic 等最具代表性。
2. **Hybrid bonding post-CMP / pre-bond clean**：市场仍小，但缺陷容忍度最低，毛利和客户粘性可能接近前道关键材料。
3. **高选择性 seed etchant + low-metal stripper/cleaner**：细线 RDL 和 Cu/Ni/Au 多金属体系下，配方失误直接带来 undercut、残留和可靠性问题。
4. **CMP slurry/post-CMP clean for TSV/RDL/hybrid bonding**：受益于 HBM4、SoIC、3DIC；Entegris、Qnity、Fujimi、Anji 等具备平台化优势。
5. **IC substrate SAP/mSAP 高端工艺包**：收入规模大，和 AI ABF 载板紧缺同频，但部分产品竞争比 hybrid bonding clean 更激烈。
6. **大宗高纯湿化学品**：规模大但 ROIC 较低，除非绑定区域供应链或成为国产替代唯一合格供应商。

## 6. 2026 关键变化：行业拐点与最可能放量子方向

### 6.1 2026 最可能发生的 3 个拐点

1. **GB300/B300 把 CoWoS-L/RDL 湿制程拉成全年主线**  
   Blackwell Ultra 是 2026 最确定出货池。其带来的不是单一化学品增量，而是 RDL plating、Cu pillar、UBM etch、stripper、post-CMP clean、substrate SAP/mSAP 的组合放量。

2. **AI 载板从“周期复苏”转为“高规格卖方市场”**  
   ABF/FC-BGA 大尺寸、高层数、低粗糙度、mSAP fine-line 让湿制程质量成为载板良率核心。MKS/Atotech、MacDermid Alpha、Uyemura、JCU、Okuno 等载板湿化学供应商的价值被重新定价。

3. **HBM4/hybrid bonding 的材料认证提前决定 2027 份额**  
   2026H2 Rubin/MI400/TPU8/ASIC early ramp 即使收入不大，也会锁定 2027 的 post-CMP clean、Cu surface prep、microbump/hybrid plating 供应商。

### 6.2 2026 最可能放量的子方向排序

1. RDL/Cu pillar/SnAg/Ni plating chemicals。
2. IC substrate SAP/mSAP wet process chemicals。
3. UBM/RDL Cu/Ti seed etchants。
4. Bump/RDL thick PR stripper 和 post-plating clean。
5. CMP/post-CMP clean for TSV/RDL。
6. ENEPIG/EPIG/final finish。
7. Temporary bonding/debond cleaning。
8. Hybrid bonding surface prep 小批量高溢价。

## 7. 2027 关键变化：行业拐点与最可能放量子方向

### 7.1 2027 最可能发生的 3 个拐点

1. **Rubin/MI400/TPU8/OpenAI XPU 把 HBM4 和 hybrid bonding 相关清洗拉入主赛道**  
   HBM4 对 bonding、CMP、表面颗粒和 metal contamination 的容忍度更低，post-CMP clean 和 surface conditioning 将从“工艺辅助”变成“良率瓶颈”。

2. **Panel-level / large-area RDL 从成本优化选项变成 ASIC 扩产工具**  
   若 CoWoS 仍紧缺，CSP ASIC 会更积极尝试 PLP、CoPoS、organic RDL interposer。湿化学的收入弹性来自更大 panel 面积、更高 bath volume 和更难的均匀性控制。

3. **玻璃基板/TGV 的 design-in 决定 2028 收入弹性**  
   2027 仍不是玻璃基板大收入年，但 TGV plating、玻璃表面活化、Cu/Ti etch、adhesion promotion 一旦进入头部 ASIC/switch 客户 AVL，材料估值会提前反映。

### 7.2 2027 最可能放量的子方向排序

1. Hybrid bonding post-CMP clean / pre-bond clean。
2. HBM4 microbump/hybrid plating/cleaning。
3. Panel-level RDL plating/etch/strip。
4. TGV/玻璃基板湿法金属化。
5. Low-PFAS / cyanide-free final finish。
6. CPO/硅光封装 wet clean/metallization。

## 8. 头部公司与细分技术地图

### 8.1 电镀、化学镀、RDL/Cu pillar/TSV

- **MKS / Atotech**：Spherolyte Cu/Ni/Sn/Au；RDL、micro-via、pillar、pad metallization、ENEPIG、dual damascene；同时有 process equipment、software、ESI laser 系统。
- **Element Solutions / MacDermid Alpha**：IC substrate、PLP、SAP、Cu pillar/RDL、final finishes；Systek SCP 100 面向 AI/HPC PLP 的高纯高速 Cu pillar plating。
- **Qnity Electronics**：Copper pillar plating、Copper RDL、Solderon tin/solder bump、TSV copper、UBM、CMP、EKC clean/removers。
- **Technic**：Elevate Cu 系列，覆盖 tight RDL、standard pillar、mega pillar、bump-on-passivation、FOWLP/2.5D/3D。
- **Uyemura**：ENIG/ENEPIG/EPIG、Cu via fill、electroless Ni/Pd/Au、immersion Au/Ag/Sn、semiconductor/pad finish。
- **JCU Corporation**：PCB/IC substrate/semiconductor plating chemicals，SAP/mSAP、via fill、final finish。
- **Okuno Chemical**：semiconductor wafer、package substrate、PCB surface treatment；TORYZA wafer acid copper additives、IC substrate electroless copper。
- **TANAKA Precious Metals、Mitsubishi Materials、JX Advanced Metals、Japan Pure Chemical、Umicore**：贵金属盐、Au/Pd/Ni plating、金属材料与表面处理。
- **Shanghai Sinyang**：Bump/TSV/RDL 湿法设备与电镀添加剂、铜互连电镀液、封装清洗与剥离。
- **Anji Microelectronics**：Cu/Ni/NiFe/SnAg ECP products，TSV、bumping、RDL；CMP slurry、post-CMP clean、PERR、stripper。
- **Jiangsu Aisen Semiconductor、Guangzhou Sanfu、PhiChem、Jianghua Micro、Crystal Clear Electronic Materials**：中国本土 wet chemicals、plating/etching/cleaning/packaging photoresist 相关布局。

### 8.2 Etchants、strippers、cleaners、post-CMP clean

- **Qnity / EKC**：post-CMP cleans、post-etch residue removers、removers/rinses、WLP photoresist removers & TSV cleaners。
- **Entegris**：formulated etch and clean、CMP slurries/pads、post-CMP contamination control、filtration/purification。
- **Merck / EMD Electronics**：surface prep & cleansing、packaging、specialty gases、semiconductor materials；SEMICON Korea 2026 展示 AI-era semiconductor materials。
- **Fujifilm Electronic Materials、TOK、JSR、Shin-Etsu、Kanto Chemical、Mitsubishi Chemical、Stella Chemifa**：photoresist ancillary、developers、strippers、etchants、高纯化学品。
- **Chemleader / CLC**：台湾 packaging Cu/Ti etchants；公开称每年超 20M wafers 使用其 Cu etchant，覆盖 fine-line RDL、microbump、Cu/Ni/Au RDL、Ni/Au pad。
- **Anji、Shanghai Sinyang、PhiChem、Jianghua Micro、Crystal Clear、Soulbrain、Dongjin Semichem、ENF Technology、Duksan**：中韩本土 wet clean/stripper/etchant 供应链。

### 8.3 CMP、hybrid bonding surface prep、temporary bonding/debonding

- **Entegris / CMC Materials**：CMP slurry/pad、post-CMP clean、contamination control。
- **Qnity**：CMP pads/slurries、EKC clean/removers、packaging materials。
- **Fujimi、Resonac、Fujifilm、Merck、Anji、Soulbrain**：CMP slurry、post-CMP、advanced packaging planarization。
- **Brewer Science、3M、TOK、JSR、Qnity、Merck、Fujifilm、Shin-Etsu、Resonac**：temporary bonding/debonding、residue removal、thick resist ancillary。
- **Resonac / Namics ecosystem**：JOINT/JOINT2/JOINT3/US-JOINT 先进封装材料共创平台，覆盖材料、设备、封装可靠性。

### 8.4 载板 wet process / final finish / 表面粗化

- **MKS/Atotech、MacDermid Alpha、Uyemura、JCU、Okuno、Meltex、Chemleader**：IC substrate SAP/mSAP、via fill、surface roughening、electroless Cu、ENEPIG/final finish。
- **Ajinomoto、Ibiden、Shinko、Unimicron、Nan Ya、Kinsus、AT&S、SEMCO、Kyocera、TOPPAN、Daeduck、LG Innotek、Simmtech、Shennan Circuit、WUS、Fastprint、Xingsen**：湿化学下游的高端载板与 ABF/FC-BGA 客户/生态。
- **TANAKA、Umicore、Mitsubishi Materials、JX Advanced Metals**：贵金属和表面处理供应。

### 8.5 设备与工艺平台相关公司

- **ASMPT NEXX、ClassOne、RENA、MKS/Atotech、ACM Research、SCREEN、Tokyo Electron、SUSS MicroTec、EV Group、Applied Materials、Lam、KLA/Onto/Camtek**：plating、wet clean、wafer bonding、RDL、CMP、metrology 的设备/工艺配套。
- **TSMC、ASE/SPIL、Amkor、Samsung、Intel Foundry、JCET、Tongfu、Huatian、Powertech/PTI、SK hynix、Micron、Samsung Memory、Ibiden、Unimicron、SEMCO**：湿化学材料最关键客户和认证入口。

## 9. 投资结论与跟踪指标

### 9.1 投资排序

短期最确定：

1. **Cu RDL/Cu pillar plating additives + UBM etch/strip/clean 工艺包**：跟 GB300/CoWoS/AI ASIC 同步放量，收入弹性和毛利弹性兼具。
2. **IC substrate SAP/mSAP wet chemistry**：AI 高端 ABF/FC-BGA 载板紧缺，化学品受益于面积和层数提升。
3. **CMP/post-CMP clean for TSV/RDL**：订单来自 HBM、CoWoS、TSV、RDL，2027 hybrid bonding 后更强。
4. **ENEPIG/EPIG/final finish**：AI substrate 高可靠、高频化，贵金属 pass-through 抬高收入；需看不含金属毛利。

未来 12-24 个月赔率最高：

1. **Hybrid bonding surface prep**：小基数、高毛利、高客户粘性。
2. **HBM4 相关 plating/cleaning**：2026H2 认证，2027 收入。
3. **Panel-level RDL wet process**：若 CSP ASIC 为扩产和降本采用 PLP，弹性极大。
4. **TGV/玻璃基板 wet metallization**：2027 design-in，2028-2029 才可能大收入，但估值会提前。
5. **中国本土替代链**：上海新阳、安集科技、艾森、飞凯、江化微、晶瑞等在先进封装 wet process 的验证进度值得持续跟踪。

### 9.2 需要持续跟踪的指标

- TSMC CoWoS-L/CoWoS-R 月产能、外包比例、RDL/CoWoS-like 外溢至 ASE/Amkor/Samsung/Intel 的速度。
- NVIDIA GB300/Rubin、AMD MI400、Google TPU8、AWS Trainium3、Meta MTIA、OpenAI/Broadcom XPU 的真实出货和 HBM4 认证节奏。
- MKS Electronics & Packaging revenue、Element/MacDermid Alpha high-end electronics organic growth、Qnity advanced packaging materials 增速、Entegris MS/APS advanced packaging pull-through。
- TECHCET/SEMI 对 plating chemicals、CMP consumables、packaging materials 的更新；特别是 advanced packaging Cu plating 是否连续上修。
- IC substrate 厂 Ibiden、Shinko、Unimicron、Nan Ya、Kinsus、SEMCO、AT&S、TOPPAN 的高端 ABF 扩产、稼动率和涨价。
- Hybrid bonding 的实际良率、post-CMP defect density、Cu recess/protrusion spec；Besi/ASMPT/EVG/SUSS 订单可作为先行指标。
- 玻璃基板/TGV 在 Intel/Samsung/AGC/TOPPAN/SKC/Corning 生态中的客户 design-in。
- 中国国产 AI 封装链中，上海新阳、安集科技、艾森、江化微、飞凯/光刻胶和清洗材料供应商进入头部 OSAT/晶圆厂 AVL 的进度。

## 10. 主要来源

### 项目内资料

- `D:\drive\Investment\调研\v5\ai_chip_research_2026_2027.md`
- `D:\drive\Investment\调研\v5\行业调研_AI服务器_存储_芯片\行业调研_AI芯片先进封装_2026.md`
- `D:\drive\Investment\调研\v5\行业调研_AI服务器_存储_芯片\行业调研_先进封装材料与热界面材料_2026.md`
- `D:\drive\Investment\调研\v5\行业调研_AI服务器_存储_芯片\行业调研_封装基板_中介层与RDL_2026-05-08.md`

### 公司一手/产品资料

- MKS Q1 2026 results: <https://www.globenewswire.com/news-release/2026/05/06/3289424/16396/en/mks-inc-reports-first-quarter-2026-financial-results.html>
- MKS/Atotech semiconductor wet chemical processes: <https://www.atotech.com/products/electronics/semiconductor/>
- MKS/Atotech Spherolyte: <https://www.atotech.com/products/electronics/semiconductor/spherolyte/>
- MKS/Atotech CPCA 2026: <https://www.atotech.com/mks-atotech-unveils-next%E2%80%91gen-pcb-manufacturing-technologies-at-cpca-2026/>
- Element Solutions Q1 2026 results: <https://ir.elementsolutionsinc.com/Investors/news/news-details/2026/Element-Solutions-Inc-Reports-Record-Quarterly-Results-and-Increases-2026-Full-Year-Guidance/default.aspx>
- MacDermid Alpha Systek SCP 100: <https://www.macdermidalpha.com/products/circuitry-solutions/ic-substrates/panel-level-packaging/systek-scp-100>
- MacDermid Alpha IMAPS DPC 2026: <https://www.macdermidalpha.com/events/imaps-22nd-annual-device-packaging-conference-dpc-2026>
- Entegris Q1 2026 results: <https://investor.entegris.com/news/news-details/2026/Entegris-Reports-Results-for-First-Quarter-of-2026/default.aspx>
- Entegris advanced packaging CMP: <https://www.entegris.com/en/home/our-science/by-industry/microelectronics/semiconductor/advanced-packaging/cmp.html>
- Qnity advanced computing and AI materials portfolio: <https://www.qnityelectronics.com/advanced-computing-and-artificial-intelligence.html>
- Qnity FY2025 results: <https://ir.qnityelectronics.com/press-releases/detail/50/qnity-reports-fourth-quarter-and-full-year-2025-results>
- Resonac JOINT3: <https://eu.resonac.com/0309_25/>
- Uyemura advanced plating chemistries: <https://uyemura.com/>
- Uyemura product research: <https://www.uyemura.co.jp/en/development/product/>
- Okuno products: <https://www.okuno.co.jp/en/product/>
- Chemleader Cu etchant: <https://en.chemleader.com.tw/autopage_detail/6/cu-etchant>
- Technic Elevate Cu 6370: <https://www.semi.org/en/press/technic-announces-commercial-release-high-performance-copper-plating>
- Anji Microelectronics solutions: <https://www.anjimicro.com/en/jiejuefangan.html>
- Shanghai Sinyang: <https://www.sinyang.com.cn/en/>
- PhiChem semiconductor materials: <https://www.phichem.com/products/semiconductor-materials/>
- ASMPT NEXX deposition/plating: <https://semi.asmpt.com/en/products/ap/nexx/>
- RENA electroplating tools: <https://www.rena.com/en/products/semiconductor/electro-plating>

### 论坛、行业报告与市场数据

- TECHCET / TechInsights semiconductor materials intelligence: <https://www.techinsights.com/semiconductor-materials-intelligence>
- TECHCET Metal Chemicals public summary, 2025-11: <https://techcet.com/2025/11/24/rising-copper-plating-demand-in-semiconductors-driven-by-advanced-packaging-and-fe-interconnects/>
- Semiconductor Digest reprint of TECHCET metal chemicals: <https://www.semiconductor-digest.com/rising-copper-demand-in-semiconductors-drives-plating-chemicals-for-advanced-packaging-and-interconnects/>
- SEMI Global Semiconductor Packaging Materials Outlook: <https://www.semi.org/en/news-media-press-releases/semi-press-releases/global-semiconductor-packaging-materials-market-to-near-%2430-billion-by-2027>
- IMAPS Device Packaging Conference 2026: <https://imaps.org/page/device-packaging-conference>
- IMAPS DPC 2026 PDCs: <https://imaps.org/page/DPC-26-PDCs>
- Advanced Energy SEMICON Korea 2026 trends: <https://www.advancedenergy.com/en-us/about/news/blog/trends-from-semicon%C2%AE-korea-2026/>
- Merck KGaA Annual Report 2025, Electronics/Semiconductor Solutions: <https://reports.emdgroup.com/en/annualreport/2025/>
- Korea IT Times, Merck SEMICON Korea 2026: <https://www.koreaittimes.com/news/articleView.html?idxno=150838>

## 11. 风险提示

1. AI capex 因电力、ROI、机房交付或政策因素递延，导致 advanced packaging 化学品订单低于极度乐观情景。
2. CoWoS/HBM4/hybrid bonding 良率低于预期，新技术材料收入延后。
3. 客户多源认证加速，专有配方毛利率被压缩。
4. 贵金属价格波动、PFAS/氰化物/溶剂法规、危化物流限制影响供应和利润。
5. 本文对未公开的单位化学品消耗、客户份额和自用 ASIC 封装规模做了大胆乐观估算，不能与公司公开营收简单相加。
# 行业调研：【先进逻辑晶圆代工和封装】

报告日期：2026-05-08  
研究对象：先进逻辑晶圆代工、2.5D/3D 先进封装、CoWoS/SoIC/EMIB/Foveros/I-Cube、AI XPU 封装基板、HBM 逻辑集成、晶圆级/封装级测试，以及直接约束这些环节的设备、材料、EDA/IP。  
资料边界：已参考本项目 `v5` 根目录和 `conference_update` 里的 AI 芯片、GTC 2026、ISSCC 2026、Chiplet Summit 2026、DATE 2026、DesignCon 2026 等资料；未使用 `行业调研_*` 四个行业调研文件夹里的既有报告内容。外部资料优先使用公司公告、投资者材料、技术论坛、官方博客和行业机构公开摘要。  
核心假设：对 2026 年 AI 基础设施建设采取乐观到极度乐观假设；对直接数据缺失的环节，用 AI 芯片出货、GW 电力、HBM stack、CoWoS 片数、晶圆收入和封装产能做交叉推算。

## 0. 一页结论

**最重要判断：2026 年先进逻辑代工和先进封装的投资主线不是“AI 芯片需求强”，而是 AI 数据中心把最稀缺的制造资源锁定为三件东西：TSMC N4/N3/N2 类先进逻辑 wafer、CoWoS/SoIC 类封装产能、HBM/基板/测试良率。** 在这个链条里，长期最高 ROIC 层最可能是 TSMC 的 leading-edge + 3DFabric 组合、HBM 头部供应商、EDA/IP 与关键设备材料；传统 OSAT 和基板厂也高弹性，但长期定价权弱于 TSMC/HBM/EDA/设备龙头。

2026 年最可能放量的技术路径：

| 排名 | 2026 最确定路径 | 对代工/封装的含义 |
|---:|---|---|
| 1 | NVIDIA B300/GB300、B200/GB200：TSMC 4NP/N4 系列 + CoWoS-L/S + HBM3E + 大尺寸 ABF | 2026 收入最大、良率成熟、瓶颈在 CoWoS/HBM/基板/系统测试；Rubin 前的绝对主线 |
| 2 | Google TPU Ironwood、AWS Trainium2/3、Microsoft Maia 200、Meta/OpenAI/Broadcom XPU：3nm/4nm 级 ASIC + HBM/2.5D 封装 | Hyperscaler ASIC 从“补充 GPU”转为独立产能池，拉动 TSMC/三星/封装/test 的第二需求曲线 |
| 3 | AMD MI350/MI400、NVIDIA Rubin：3nm/2nm + HBM3E/HBM4 + 更大封装 + 全液冷 rack | 2026 H2 小批量，2027 量产主线；HBM4 验证和高级封装良率决定斜率 |
| 4 | 中国 Ascend/Cambricon/T-Head/Kunlun：SMIC DUV 多重曝光 + 国产 2.5D/封测/HBM 替代 | 全球收入占比不高，但中国本土设备、材料、封测和测试确定性强 |
| 5 | CPO/硅光/photonic interposer、UCIe 3.0、SoIC/hybrid bonding、CoPoS/玻璃基板 | 2026 多为设计导入/样机/小批量，2027 出现早期收入，2028-2029 才是大规模兑现 |

**市场规模粗估：**

| 口径 | 未来 3 个月 | 未来 1 年 | 未来 2 年 | 备注 |
|---|---:|---:|---:|---|
| 全球 AI/HPC 先进逻辑代工 wafer 收入 | $28-40B | $125-180B | $175-280B | 以 TSMC HPC/先进节点收入为锚，含部分 Samsung/Intel/SMIC |
| AI 相关先进封装/CoWoS/SoIC/EMIB/Foveros/I-Cube 收入 | $6-10B | $28-48B | $50-90B | 不含 HBM 存储芯片本体，含封装服务、interposer、RDL、substrate、assembly/test |
| HBM + AI 高带宽存储本体 | $15-22B | $60-90B | $95-150B | Yole/会议材料口径给 2026 HBM 约 $60B、2027 约 $80B；极乐观可更高 |
| AI 封装基板/ABF/interposer/RDL 关键材料 | $4-7B | $18-32B | $32-58B | 大尺寸基板、ABF、underfill、临时键合材料、TSV/RDL 化学品 |
| AI package probe / ATE / burn-in / system-level test | $1.8-3.2B | $8-14B | $15-26B | HBM KGD、CoWoS package、NVLink/SerDes、rack burn-in 时间变长 |

**三档总情景：**

| 情景 | 2026 核心假设 | 2027 核心假设 | 投资结论 |
|---|---|---|---|
| 基准 | Blackwell Ultra、Ironwood、Trainium2/3、MI350 放量；Rubin/MI400/TPU8 试量；CoWoS/HBM4 有 1-2 季度摩擦 | Rubin/HBM4/MI400 开始规模化，但电力和封装仍限制出货 | TSMC/HBM/CoWoS/test 稳健高增，OSAT/基板弹性中高 |
| 乐观 | CoWoS 年底 11.5-14 万片/月区间兑现，HBM4 多供应商验证顺利，ASIC 订单提前锁产能 | Rubin、MI400、OpenAI/Meta/Broadcom XPU 同步 ramp，AI ASIC 不挤出 GPU | 高端封装和先进节点持续供不应求，TSMC 与 HBM 供应商利润率维持高位 |
| 极度乐观 | AI 推理 token 爆发，客户把 2027 需求前置；CoWoS/HBM/基板/test 供应“被预定但可交付” | 1GW AI factory 成为采购单位；N2/N3/SoIC/CoWoS 大客户排产到 2028 | 先进逻辑 + 先进封装进入 2026-2027 超级周期，定价权上移到稀缺制程/封装/test 资源 |

## 1. AI 计算中心建设给行业带来的机遇与挑战

### 1.1 需求锚：AI 芯片路线图已经足够支撑 2026-2027 先进制造景气

本项目已有 AI 芯片路线图给出的 2026 全球 AI 计算芯片/模块产能释放金额为：基准约 **$300-360B**，乐观 **$390-470B**，极度乐观 **$520-650B**；2027 为 **$430-520B / $590-720B / $850-1,050B**。对应最大共同瓶颈明确是 **HBM3E/HBM4、CoWoS/先进封装、液冷/供电、客户机房上电节奏**。

2026-2027 年初出货量和价值权重最大的 AI 芯片/平台，对晶圆代工和封装的拉动如下：

| 芯片/平台 | 2026 金额情景，基准/乐观/极乐观 | 主要技术路径 | 对晶圆制造与封装的直接需求 |
|---|---:|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | $90B / $130B / $180B | TSMC 4NP/N4；HBM3E；CoWoS-L/S；NVL72 rack | 2026 最大 CoWoS、ABF、HBM KGD、封装 test 消耗者 |
| AWS Trainium2 | $15B / $25B / $40B | 先进逻辑 ASIC + HBM + NeuronLink；大规模自用 | ASIC 代工、HBM 集成、系统级 burn-in；内部转移价低于 GPU 但数量大 |
| Google TPU v7 Ironwood | $18B / $32B / $55B | Broadcom/Google ASIC；192GB HBM、7.37TB/s；2.5D 封装 | 3nm/先进节点、HBM3E、2.5D 封装、云端 pod 级测试 |
| NVIDIA B200/GB200 | $25B / $45B / $70B | TSMC 4NP；双 die Blackwell；HBM3E；CoWoS | 既有订单延续，推高 CoWoS 利用率 |
| Huawei Ascend 910C/950 | $12B / $23B / $42B | SMIC N+2/N+3 DUV 多重曝光；国产 2.5D/HBM | 中国本土设备、材料、封测、探针/ATE 替代 |
| Cambricon MLU590/690 | $3B / $6B / $11.5B | SMIC N+2/N+3；HBM；OAM 模块 | 国产先进逻辑良率、HBM 封装和测试瓶颈 |
| AMD MI350 | $12B / $22B / $36B | CDNA4，ISSCC 公开为 3D-stacked 3nm XCD + 6nm IOD；HBM3E | 3D chiplet、先进封装、HBM3E KGD 和 UBB/OAM 测试 |
| AWS Trainium3 | $6B / $12B / $24B | AWS 称 3nm；144-chip UltraServer | 3nm ASIC、大规模封装/test、HBM/Neuron fabric 测试 |
| Meta MTIA 300/400/450/500 | $2.5B / $7B / $16B | Broadcom XPU 平台；先进节点；GenAI 推理 | 2026-2027 ASIC 多代迭代，拉动定制 NRE 和封装锁产能 |
| Microsoft Maia 200 | $4B / $8B / $15B | TSMC 3nm、216GB HBM3E、7TB/s、272MB SRAM | 3nm AI ASIC + HBM3E + 液冷 rack 级验证 |
| AMD MI400/MI455X Helios | $2B / $8B / $18B | 2nm/3nm 组合可能性；HBM4；72 GPU rack | 2026 H2 起步，2027 对 N2/HBM4/CoWoS-L 的弹性最大 |
| OpenAI/Broadcom accelerator | $0.5B / $2B / $5B | 官方 10GW 合作，2026 H2 开始部署 | 2026 先锁设计与产能，2027 进入 >1GW 级别消耗 |

### 1.2 当前已被使用的核心技术

| 技术层 | 2026 正在使用的主流技术 | 2026-2027 变化 |
|---|---|---|
| 先进逻辑节点 | TSMC N4/N4P/4NP、N5/N5P、N3E/N3P；Samsung SF4/SF3/SF2 设计导入；Intel 18A/14A 设计推进；SMIC N+2/N+3 DUV | 2026 大量收入仍在 N4/N5/N3；N2/N2P/A16 从 2026-2027 设计/早期 ramp，AI 大量收入偏 2027+ |
| 2.5D 封装 | CoWoS-S、CoWoS-L、I-Cube、EMIB、InFO-oS、RDL interposer | AI GPU/ASIC 默认 2.5D + HBM；封装尺寸从 3.3x reticle 向 5.5x、未来 14x reticle 迁移 |
| 3D 封装 | SoIC、hybrid bonding、Foveros Direct、X-Cube、HBM TSV stack | 逻辑-on-逻辑和 HBM base die 进入更深耦合，2027-2029 影响更大 |
| 内存集成 | HBM3E 主力；HBM4 验证；GDDR7 中端推理；LPDDR6 端侧 | 2026 HBM3E 仍最赚钱，HBM4 决定 Rubin/MI400/TPU8 斜率 |
| D2D/chiplet | 私有 die-to-die、Infinity Fabric、NVLink-C2C、UCIe 早期 | UCIe 3.0 48/64GT/s 进入 2026 设计导入，RoT/管理/测试比速率本身更关键 |
| 测试 | HBM known-good-die、wafer probe、package test、burn-in、SerDes/NVLink/PCIe/UALink 测试 | 测试从成本项变成瓶颈项；AI package test 时间和 probe card 复杂度显著提升 |
| 封装材料 | ABF、高阶 BT/RDL、silicon interposer、underfill、temporary bonding、molding、thermal interface | 大尺寸 package 的 warpage、CTE、翘曲、良率成为定价来源 |

### 1.3 新技术成熟和放量时间

| 技术 | 2026 基准 | 2026 乐观 | 2026 极乐观 | 2027 基准/乐观/极乐观 | 关键判断 |
|---|---|---|---|---|---|
| N4/N5 + CoWoS + HBM3E | 已成熟，全年主力 | GB300/B300 更快切换 | 客户加价抢产能 | 仍是存量大头，但增长让位 Rubin/N3/N2 | 2026 最确定收入池 |
| N3/N3E/N3P AI ASIC | Google/AWS/Microsoft/AMD 部分放量 | Hyperscaler ASIC 加速 | Broadcom/Marvell 订单前置 | 2027 成为 ASIC 与 MI350/部分 GPU 主力 | TSMC Q1 2026 3nm 已占 wafer revenue 25%，说明节点商业化成熟 |
| N2/N2P/A16 | 设计导入/早期产品，不宜按大规模收入定价 | MI400/TPU8/部分 ASIC 小量切入 | 2026 H2 有高价小批量 | 2027 放量，2028 A14 继续接棒 | AI 大芯片的 N2 ramp 通常慢于手机 SoC，但 ASP 和锁产能能力更强 |
| HBM4 | 2026 Q2-Q3 验证，H2 小量 | Rubin/MI400 首批顺利 | 多供应商认证超预期 | 2027 主力化；极乐观下成为最大瓶颈利润池 | HBM4 是 2027 advanced packaging 的共同阀门 |
| CoWoS-L / 5.5x reticle | 2026 已放量 | 年底产能接近 11.5-14 万片/月区间 | 客户预付锁产能 | 2027 约 17 万片/月规划兑现则 GPU/ASIC 出货上修 | CoWoS 仍是最稀缺封装资源 |
| SoIC / hybrid bonding | 先进产品小规模 | 2.5D + 3D 组合设计增多 | 高端 ASIC 采用前置 | 2027-2028 规模扩大，2029 A14-on-A14 更重要 | 比 CoWoS 更难、认证更长、毛利更高 |
| CPO/COUPE/photonic interposer | 交换芯片/光引擎试点 | Spectrum-6、硅光生态拉动 | 设计 win 在 2026 提前确认 | 2027 早期收入，2028 后规模化 | 2026 收入小但架构权重要 |
| CoPoS/FOPLP/玻璃基板 | 样机/中试 | 大客户验证提前 | 小批量工程线 | 2028-2029 大规模可能性高 | 2027 前更像期权，不应替代 CoWoS 主线 |

## 2. 已开始放量的关键产品：规模、渗透率、利润率

### 2.1 AI/HPC 先进逻辑晶圆代工

| 指标 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| 未来 3 个月市场规模 | $28-34B | $34-40B | $40-46B |
| 未来 1 年市场规模 | $125-150B | $150-180B | $180-220B |
| 未来 2 年市场规模 | $175-220B | $220-280B | $280-360B |
| AI/HPC 中 TSMC 份额 | 80-88% | 82-90% | 85-92% |
| Samsung/Intel/SMIC 合计份额 | 8-15% | 10-18% | 12-22% |
| 毛利率/利润率 | TSMC 65-70%，Samsung Foundry 低个位数到亏损改善，SMIC 15-25% | TSMC 68-74%，Samsung 高端订单改善 | TSMC 72-78%，先进节点与封装打包溢价扩大 |

依据和解释：

- TSMC 1Q26 revenue 为 **$35.94B**，gross margin **66.2%**，operating margin **56.8%**；3nm/5nm/7nm 分别占 wafer revenue **25%/36%/13%**，advanced nodes 合计 **74%**，HPC 平台占 **61%**。这意味着仅 TSMC 单季 HPC/先进节点已是数百亿美元级收入池。
- TSMC 指引 2Q26 revenue **$39.2-40.4B**，gross margin **58-60%**。短期毛利被汇率、海外 fab、N2 ramp 和折旧影响，但 AI/HPC 稼动率极强。
- Gartner 预计 2026 全球半导体收入 **$1.32T**，2027 **$1.5545T**；AI 半导体约占 2026 半导体总收入 **30%**，对应约 **$396B**。这给先进逻辑 + HBM + 封装的上限提供校验。

### 2.2 CoWoS / 2.5D advanced packaging

| 指标 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| 未来 3 个月市场规模 | $5.5-7.5B | $7.5-9.5B | $9.5-12B |
| 未来 1 年市场规模 | $24-34B | $34-48B | $48-65B |
| 未来 2 年市场规模 | $45-65B | $65-90B | $90-125B |
| AI 高端 GPU/ASIC 封装渗透率 | 80-90% | 88-95% | 95%+ |
| TSMC 高端 AI 2.5D 份额 | 65-80% | 70-85% | 75-88% |
| 毛利率 | TSMC 高端封装 38-50%，OSAT 20-32% | TSMC 45-55%，OSAT 25-35% | TSMC 50-60%，少数稀缺 OSAT/基板也可 30-40% |

依据和解释：

- TrendForce 公开估计 TSMC CoWoS 月产能到 2026 年底约 **11.5-14 万片/月**，2027 年约 **17 万片/月**。
- TSMC 2026 技术论坛资料显示：CoWoS 可在 2026 年量产 **5.5x reticle** 级别，2028 年走向 **14x reticle**，2029 年 **>14x reticle**；System-on-Wafer 路线到 2029 年可到 **40 reticle** 级别。
- AI XPU 单颗封装价值显著高于手机/PC SoC 封装，且客户无法轻易切换，因为 package design、thermal、HBM KGD、substrate、test recipe 都和芯片设计强绑定。

### 2.3 HBM 逻辑集成、HBM KGD 和高带宽存储封装链

| 指标 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| HBM 本体未来 1 年市场规模 | $60-75B | $75-90B | $90-110B |
| HBM 本体未来 2 年市场规模 | $80-110B | $110-140B | $140-180B |
| HBM 封装/test/集成服务未来 1 年 | $10-16B | $16-24B | $24-35B |
| HBM 封装/test/集成服务未来 2 年 | $18-30B | $30-48B | $48-70B |
| HBM 在高端 AI accelerator 渗透率 | 90%+ | 95%+ | 95%+ 且每颗 stack 数上升 |
| 毛利率 | HBM 供应商 50-60%；test/probe 45-65% | HBM 55-65%；test 55-70% | HBM 60-70%；稀缺 test/probe 可 65-75% |

依据和解释：

- Chiplet Summit 2026 会议材料引用 Yole 口径：HBM 收入 2025 约 **$35B**，2026 约 **$60B**，2027 约 **$80B**，2031 约 **$170B**。
- HBM4 从 2026 H2 起进入 Rubin/MI400/TPU8 相关验证和小批量；若多供应商验证顺利，2027 对先进封装良率、探针卡、ATE 和 burn-in 的拉动会强于普通 DRAM。

### 2.4 ABF/高阶基板、interposer、RDL、封装材料

| 指标 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| 未来 3 个月市场规模 | $4-5.5B | $5.5-7B | $7-9B |
| 未来 1 年市场规模 | $18-25B | $25-32B | $32-42B |
| 未来 2 年市场规模 | $32-45B | $45-58B | $58-78B |
| 大尺寸 AI package 中 ABF/高阶基板渗透率 | 80%+ | 90%+ | 95%+ |
| 毛利率 | 基板厂 20-30%，关键材料 35-55% | 基板 25-35%，材料 45-60% | 基板 30-40%，ABF/underfill/临时键合材料 50-65% |

关键事实：

- AI package 尺寸扩大导致 ABF 层数、面积、翘曲控制、阻抗控制和热膨胀匹配难度上升。
- 大尺寸 CoWoS-L 与 HBM4 的组合会把封装良率从单纯 interposer 产能转向 **substrate warpage + underfill + assembly test** 的综合良率。

### 2.5 探针卡、ATE、封装/系统级测试

| 指标 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| 未来 3 个月市场规模 | $1.8-2.4B | $2.4-3.2B | $3.2-4.2B |
| 未来 1 年市场规模 | $8-11B | $11-14B | $14-18B |
| 未来 2 年市场规模 | $15-20B | $20-26B | $26-35B |
| AI package probe/test attach rate | 持续提高 | HBM4 和 CPO 增加测试时间 | 测试时间成为交付瓶颈之一 |
| 毛利率 | ATE/probe 45-60%，OSAT test 20-35% | ATE/probe 55-68% | 稀缺高端 probe/ATE 60-75% |

关键事实：

- FormFactor 1Q26 revenue **$226.1M**，公司称受 AI/advanced packaging/HBM 需求驱动，non-GAAP gross margin **42.4%**。
- AI package 的测试不是单颗 die 功能测试，而是 HBM KGD、interposer continuity、NVLink/SerDes、thermal cycling、burn-in、rack-level/system-level test 的串联。

## 3. 在研关键产品和未来高增长技术

### 3.1 N2/N2P/A16/A14 与 backside power

| 时间 | 基准 | 乐观 | 极度乐观 |
|---|---|---|---|
| 未来 3 个月 | 设计导入、PDK/EDA signoff、少量 tape-out | 头部 AI ASIC 锁定 2027 N2 产能 | 客户预付 N2/A16 产能和 CoWoS 组合套餐 |
| 未来 1 年 | N2/N2P 在 mobile/部分 AI 开始收入；AI 大芯片更多是工程批 | AMD/Google/Broadcom/NVIDIA 后续平台提前 | AI ASIC 从 N3 快速跨到 N2，抬高晶圆 ASP |
| 未来 2 年 | N2/N2P/A16 成为高端 AI ASIC/GPU 主力之一 | A16 backside power 被高功耗 AI 采用 | N2/A16 + SoIC/CoWoS 打包成为 TSMC 新护城河 |
| 毛利率 | 55-65% ramp 期受折旧拖累 | 65-75% | 75%+，若供不应求并与封装打包 |

TSMC 2026 技术论坛给出的后续路线包括 A14、N2U、A14-on-A14 SoIC 等；对投资的关键不是单节点命名，而是 **front-end 节点、backside power、SoIC、CoWoS 和系统热/电协同**被打包销售。

### 3.2 SoIC / hybrid bonding / logic-on-logic

| 口径 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| 未来 1 年收入 | $2-5B | $5-8B | $8-12B |
| 未来 2 年收入 | $8-15B | $15-25B | $25-40B |
| 渗透率 | 高端 AI/CPU/GPU 少数旗舰 | XPU chiplet 和 HBM base die 更广泛采用 | 逻辑 3D stacking 进入 AI 主流架构 |
| 毛利率 | 45-60% | 55-70% | 65-80% |

SoIC/hybrid bonding 的定价能力来自三点：第一，pitch、平坦度、污染和良率窗口极窄；第二，设计必须从架构期嵌入；第三，一旦通过客户认证，切换成本远高于传统封装。

### 3.3 CPO、COUPE、silicon photonics 与 photonic interposer

| 口径 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| 未来 1 年 CPO/光 chiplet 收入 | $0.2-0.5B | $0.5-0.9B | $0.9-1.5B |
| 未来 2 年收入 | $0.8-1.8B | $1.8-4B | $4-8B |
| 渗透率 | 交换芯片/部分高端 AI fabric pilot | 2027 早期 AI scale-up/scale-out 导入 | 224G/448G 电互连压力提前触顶，光封装快速前置 |
| 毛利率 | 20-40%，研发/良率吃利润 | 35-55% | 光引擎/IP/激光源 50-70%，模块端分化 |

2026 收入小，但它决定 2028 以后架构权。NVIDIA GTC 2026 提到 Spectrum-6/CPO；TSMC 2026 技术论坛资料中 COUPE/光电封装也进入路线图。短线更确定的是 CPO 相关的光引擎、光电测试、silicon photonics process、laser source、packaging thermal。

### 3.4 CoPoS、panel-level packaging、玻璃基板/TGV

| 口径 | 基准 | 乐观 | 极度乐观 |
|---|---:|---:|---:|
| 未来 1 年收入 | <$1B | $1-2B | $2-3B |
| 未来 2 年收入 | $2-5B | $5-10B | $10-18B |
| 成熟时间 | 2028-2029 | 2027 late 小量 | 大客户提前工程线 |
| 毛利率 | 初期低或不稳定 | 30-45% | 若形成稀缺产能可 45-60% |

这类技术是 CoWoS 后的成本曲线期权。2026-2027 不应按主收入池估值，但一旦 AI package 继续向 10x reticle 以上扩张，panel-level 和玻璃/TGV 会成为 CoWoS 的下一代成本解法。

## 4. 供给侧：产能结构、瓶颈、成本和价格传导

### 4.1 主要产能分布

| 地区/公司 | 关键产能 | 工艺/封装 | 投资含义 |
|---|---|---|---|
| 台湾 TSMC | 新竹/台中/台南/高雄先进逻辑，竹南/台中/台南先进封装 | N4/N3/N2、CoWoS、SoIC、InFO、3DFabric | 全球 AI 高端逻辑与封装核心瓶颈，定价权最强 |
| 美国 TSMC Arizona | N4/N3/N2 分阶段 | 先进逻辑为主 | 成本高、折旧高，但客户愿为供应链韧性付费 |
| 韩国 Samsung | 华城/平泽/未来 Taylor；Foundry + HBM + AVP | SF4/SF3/SF2、I-Cube/X-Cube、HBM | 垂直整合优势，但先进逻辑良率和客户信任仍需验证 |
| 美国/全球 Intel Foundry | Oregon/Arizona/New Mexico/Ireland/Israel/Malaysia 等 | Intel 18A/14A、EMIB、Foveros、Foveros Direct | 先进封装强，代工客户生态仍在重建；若 AI ASIC 拿单则高弹性 |
| 中国大陆 SMIC/华虹/封测链 | 上海/北京/深圳/无锡/苏州等 | DUV 多重曝光 N+2/N+3、国产 2.5D/OSAT | 中国 AI 替代需求强，但受设备、HBM、良率、EDA 约束 |
| OSAT：ASE/Amkor/JCET/TFME/PTI/KYEC/华天 | 台湾、中国、马来西亚、韩国、美国等 | Assembly、test、fan-out、SiP、部分 2.5D | 受益于 TSMC 外包和非 TSMC ASIC，但长期定价权不及前段 |
| 基板：Ibiden/Shinko/Unimicron/Kinsus/AT&S/Nanya/SEMCO 等 | 日本、台湾、韩国、奥地利、中国 | ABF/BT/高阶 package substrate | 大尺寸 AI package 扩产周期长，弹性高 |

### 4.2 供给瓶颈，至少 10 条

1. **CoWoS/2.5D 封装产能。** 不是单台设备问题，而是 silicon interposer、RDL、TSV、bonding、substrate、underfill、test、良率的系统产能。
2. **HBM4 KGD 和 base die。** HBM4 需要内存厂、逻辑 base die、封装厂和 GPU/ASIC 客户共同验证；任何一环拖慢都会限制 Rubin/MI400/TPU8。
3. **ABF/大尺寸基板。** AI package 面积和层数上升导致翘曲、阻抗、热膨胀和良率成为硬瓶颈。
4. **EUV/High-NA EUV 与先进 litho 工艺窗口。** N2/A16/A14 时代，ASML scanner、光罩、OPC、resist、metrology 和 overlay 都是瓶颈。
5. **先进封装测试时间。** HBM KGD、interposer continuity、SerDes/NVLink/PCIe/UALink、burn-in、thermal cycling 使 test hour per package 上升。
6. **探针卡和高并行测试接触技术。** HBM 和大 die 高针数、高频、高温测试对 probe card 寿命和一致性要求更高。
7. **临时键合/解键合、CMP、清洗、湿化学和 underfill 材料。** 这些材料单价不如芯片高，但失效会造成整颗高价 package 报废。
8. **EDA/IP/PDK 和 package-aware signoff。** 先进封装必须同时看 thermal、IR drop、EM、SI/PI、warpage；工具链不成熟会拉长 tape-out。
9. **工程人才和客户认证。** AI XPU 项目一次封装/节点切换动辄 12-24 个月，客户认证是隐性瓶颈。
10. **地缘、出口管制和供应链冗余。** 中国先进逻辑受 DUV 多重曝光、EDA 和 HBM 限制；美国/欧洲本土产能成本高但战略价值高。
11. **厂务、电力、水和洁净室交付。** 先进 fab 和 advanced backend 都是高耗能、高用水、高洁净度设施，建设周期限制扩产速度。
12. **良率学习周期。** 大 die + HBM + interposer + substrate 的系统良率是乘法，不是单 die 良率。

### 4.3 成本构成与毛利决定因素

| 环节 | 成本构成 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| 先进逻辑 wafer | 折旧 35-45%、材料/化学品/光罩 15-25%、人工/厂务/能源 10-15%、研发/工程/良率 10-20% | 节点良率、稼动率、客户 mix、折旧曲线、NRE | wafer price、mask/NRE、long-term capacity agreement、预付款 |
| CoWoS/2.5D | interposer/RDL、ABF substrate、bonding、underfill、assembly、test、良率损失 | 封装尺寸、HBM stack 数、substrate 良率、test 时间、客户认证 | capacity reservation、package ASP、turnkey pricing、稀缺产能加价 |
| HBM 集成 | HBM die/stack、base die、TSV、KGD test、thermal、package integration | HBM4 良率、stack 高度、客户锁单、DRAM 价格周期 | 长约、预付款、take-or-pay、优先供货溢价 |
| 基板/材料 | ABF、铜箔、树脂、玻璃布、underfill、清洗/电镀/蚀刻化学品 | 大尺寸良率、材料认证、客户集中 | 年度议价 + 稀缺料溢价；客户二供认证慢 |
| ATE/probe/test | ATE 设备折旧、probe card、socket、handler、工程时间、burn-in 能源 | 测试复杂度、并行度、良率反馈价值、客户停线成本 | test time 收费、设备租赁/购买、probe card 定制费 |

## 5. 竞争格局与壁垒

### 5.1 市场结构

| 领域 | 头部集中度 | 说明 |
|---|---|---|
| 先进逻辑代工 | 极高，TSMC 在 3nm/5nm/AI HPC 中事实垄断 | Samsung/Intel 是战略二供，但 2026 收入和良率可信度仍与 TSMC 有差距 |
| CoWoS/高端 2.5D | 极高，TSMC 主导 NVIDIA/AMD/Broadcom/Google 等核心平台 | ASE/Amkor/Intel/Samsung 可承接部分，但最高端 turnkey 仍看 TSMC |
| HBM | 三强，SK hynix/Samsung/Micron | 2026 HBM3E/4 供给紧，客户锁单强 |
| 基板 | 日本/台湾/韩国头部集中，Ibiden/Shinko/Unimicron/Kinsus/SEMCO 等 | AI package 对大尺寸良率要求高，扩产慢 |
| 前道设备 | ASML/AMAT/Lam/TEL/KLA 等高集中 | 工具不可替代，毛利和 ROIC 稳定 |
| EDA/IP | Synopsys/Cadence/Siemens 三强 | 先进节点和 3DIC signoff 越复杂，粘性越强 |
| 测试 | Advantest/Teradyne/FormFactor/Technoprobe/MPI 等 | HBM/AI package 提高高端 test attach rate |

### 5.2 壁垒清单：为什么能定价

| 壁垒 | 为什么能定价 |
|---|---|
| 技术/良率壁垒 | 客户买的不是工艺名，而是可量产良率。大 die + HBM + interposer 的系统良率无法靠短期资本复制 |
| 规模壁垒 | N2/N3 fab、CoWoS 线、HBM test 需要数十亿到数百亿美元 capex；稼动率决定毛利 |
| 客户 co-design 锁定 | AI XPU 从架构期就锁 PDK、封装、HBM、thermal、test recipe，切换要重做系统验证 |
| 认证标准 | Hyperscaler/NVIDIA/AMD/汽车/主权 AI 客户认证周期长，二供导入慢 |
| 切换成本 | AI 大芯片 mask/NRE、验证、软件栈和 rack 级认证可达数亿美元，重流片风险极高 |
| 供应链控制 | TSMC 能协调 wafer、CoWoS、HBM partner、substrate、test；单点供应商很难提供 turnkey certainty |
| 数据和经验 | 良率学习、失效分析、DFM/DFT 数据沉淀不可购买；越先进节点越明显 |

### 5.3 长期高 ROIC 层

最可能长期高 ROIC 的层级排序：

1. **TSMC leading-edge + 3DFabric。** 同时控制先进节点和先进封装，是 AI XPU 的共同生产平台；客户难以绕开。
2. **HBM 头部供应商。** SK hynix/Samsung/Micron 在 2026-2027 供不应求，HBM4 认证成功者有准垄断溢价。
3. **EDA/IP 和 D2D/3DIC 工具链。** 毛利率高、粘性强、随设计复杂度提高而价值上升。
4. **前道/后道关键设备和量测。** ASML、AMAT、Lam、TEL、KLA、BESI、DISCO、EVG、SUSS、Advantest、Teradyne、FormFactor 等，受益于扩产和工艺复杂化。
5. **高端基板/关键材料。** ABF、underfill、temporary bonding、silicon interposer 材料、光刻胶/掩模/硅片，短中期强弹性；长期要看产能纪律。
6. **OSAT。** 量增很强，但如果不掌握最高端封装 IP 和客户 co-design，长期毛利率通常低于 TSMC/EDA/HBM。

## 6. 2026 关键变化：三个拐点和最可能放量方向

### 拐点 1：Blackwell Ultra/GB300 把 CoWoS 从瓶颈变成定价资产

2026 年 B300/GB300 是最大收入单品。它对 TSMC 4NP、CoWoS-L/S、HBM3E、ABF、探针/test、系统 burn-in 的需求同步放大。最可能放量方向是：

- CoWoS-L/S 和 5.5x reticle 级封装；
- HBM3E KGD + package test；
- 高阶 ABF、大尺寸 substrate；
- 高速 SerDes/NVLink/PCIe test；
- advanced packaging 设备：bonding、CMP、RDL、inspection、dicing、temporary bonding。

### 拐点 2：Hyperscaler ASIC 成为独立产能池

Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA、OpenAI/Broadcom XPU 的共同点是：不再只是 NVIDIA GPU 的替代选项，而是云厂把推理 TCO、供应链议价和自有 workload 优化变成资本开支主轴。最可能放量方向：

- TSMC N3/N4 AI ASIC wafer；
- Broadcom/Marvell custom silicon + advanced packaging；
- ASIC 专属 package test、D2D IP、HBM 集成；
- 非 NVIDIA 生态的 UCIe/以太网/PCIe 互连封装。

### 拐点 3：HBM4/Rubin/MI400 把 2027 订单提前到 2026

即使 Rubin/MI400 2026 收入不如 Blackwell，客户会在 2026 锁 HBM4、CoWoS、N2/N3 wafer、基板和测试产能。最可能放量方向：

- HBM4 probe/test、base die、stack 验证；
- N2/N3 大芯片 tape-out 支持；
- SoIC/hybrid bonding 早期设计；
- 先进封装热/电/机械仿真和 EDA signoff。

## 7. 2027 关键变化：三个拐点和最可能放量方向

### 拐点 1：Rubin/MI400/TPU8/OpenAI ASIC 进入 HBM4 + 更大封装时代

2027 先进封装的焦点从“CoWoS 产能够不够”升级为“HBM4、CoWoS-L、SoIC、基板、test、液冷能否系统良率达标”。最可能放量方向：

- HBM4/HBM4E；
- N2/N3 AI ASIC/GPU；
- CoWoS-L、SoIC、hybrid bonding；
- 更大 reticle-size package 与高阶 ABF；
- 高端 ATE/probe card。

### 拐点 2：CPO/光电封装从样机转向订单

2027 不是 CPO 全面替代 pluggable 的年份，但会是高端 AI fabric 设计 win 的年份。最可能放量方向：

- CPO optical engine、外置激光源、硅光 PIC；
- 光电共封装热管理和光电测试；
- 224G/448G SerDes、retimer、connector 与 package SI/PI；
- COUPE/photonic interposer 早期客户验证。

### 拐点 3：开放 chiplet/UCIe 从论文进入受控生态

2027 真正发生的不是通用 chiplet marketplace 大爆发，而是 hyperscaler/大厂内部受控生态里出现可复用 chiplet。最可能放量方向：

- UCIe 3.0 PHY/IP/VIP/compliance；
- RoT/Management Director/security chiplet；
- DFT/SLM/KGD；
- 3DIC digital twin、thermal/IR/EM-aware EDA；
- advanced package test responsibility 和供应链规则。

## 8. 头部公司与细分公司清单

### 8.1 先进逻辑代工与先进封装平台

| 细分 | 公司 |
|---|---|
| 先进逻辑 foundry | TSMC、Samsung Foundry、Intel Foundry、SMIC、Rapidus、GlobalFoundries、UMC、Tower、华虹 |
| AI 高端先进封装 | TSMC 3DFabric/CoWoS/SoIC/InFO、Intel EMIB/Foveros/Foveros Direct、Samsung AVP/I-Cube/X-Cube/H-Cube、ASE、Amkor、JCET、Tongfu Microelectronics、Powertech/PTI、KYEC、Tianshui Huatian、Nepes、LB Semicon、Hana Micron |
| AI ASIC/custom silicon | NVIDIA、Broadcom、AMD、Marvell、Google、Amazon Annapurna、Microsoft、Meta、OpenAI、Qualcomm、MediaTek、Tesla、Huawei HiSilicon、Cambricon、Alibaba T-Head、Baidu Kunlun、Biren、Iluvatar、Moore Threads、Enflame、MetaX |
| HBM/存储 | SK hynix、Samsung、Micron、Rambus、Cadence/Synopsys HBM IP、Kioxia/Western Digital/Seagate 用于 AI storage |

### 8.2 基板、材料、设备、测试

| 细分 | 公司 |
|---|---|
| ABF/封装基板 | Ibiden、Shinko Electric、Unimicron、Kinsus、Nan Ya PCB、AT&S、Samsung Electro-Mechanics、LG Innotek、Daeduck、Shennan Circuits、Simmtech、Zhuhai Access、欣兴、景硕、南电 |
| ABF/树脂/封装材料 | Ajinomoto、Resonac、Namics、Henkel、DuPont、Merck/EMD、Entegris、JSR、TOK、Shin-Etsu Chemical、Fujifilm、Sumitomo Chemical、Hitachi Chemical、Soulbrain、Dongjin |
| 硅片/前道材料 | Shin-Etsu Handotai、SUMCO、GlobalWafers、Siltronic、SK Siltron、Okmetic、Soitec、JX Metals、Mitsui Chemicals、Air Liquide、Linde |
| 前道设备 | ASML、Applied Materials、Lam Research、Tokyo Electron、KLA、ASM International、Hitachi High-Tech、SCREEN、Nikon、Canon、Lasertec、Onto Innovation、Nova、Veeco、Axcelis |
| 后道/先进封装设备 | BESI、ASMPT、Kulicke & Soffa、DISCO、EV Group、SUSS MicroTec、Tokyo Electron、Applied Materials、Lam、KLA、Onto、Camtek、Rudolph/Onto、Accretech |
| ATE/probe/test | Advantest、Teradyne、FormFactor、Technoprobe、MPI、Cohu、Chroma、Keysight、Rohde & Schwarz、Anritsu、Teledyne LeCroy、Viavi、Onto、Camtek |
| EDA/IP/3DIC | Synopsys、Cadence、Siemens EDA、Ansys、Keysight EDA、Alphawave Semi、Rambus、Arteris、Arm、Imec、UCIe Consortium、OCP、Open Compute silicon ecosystem |
| 硅光/CPO | Broadcom、NVIDIA、Marvell、Coherent、Lumentum、Intel Silicon Photonics、Cisco/Acacia、Ayar Labs、Lightmatter、Ranovus、OpenLight、GlobalFoundries silicon photonics、TSMC COUPE ecosystem |

## 9. 投资结论

### 9.1 最强主线

1. **TSMC leading-edge + 3DFabric 是 2026-2027 最强确定性资产。** 先进节点、CoWoS、SoIC、HBM 集成、客户 co-design 一体化，使其比单纯 wafer foundry 更有定价权。
2. **HBM 与先进封装是同一条投资线。** 2026 看 HBM3E + CoWoS，2027 看 HBM4 + N2/N3 + SoIC/CoWoS-L。
3. **测试、探针卡和封装良率管理会被重估。** AI package 单价极高，测试不是低附加值环节，而是降低整颗 package 报废概率的保险。
4. **OSAT/基板/材料是高弹性中游。** 订单弹性强，但要区分是否掌握大尺寸 AI package、HBM/2.5D 认证和客户绑定。
5. **CPO/玻璃基板/CoPoS 是 2027 订单、2028+ 收入的期权。** 适合作为二线弹性，不应替代 2026 CoWoS/HBM 主线。

### 9.2 最大风险

| 风险 | 影响 |
|---|---|
| Hyperscaler AI capex 因 ROI 或融资压力放缓 | wafer/封装锁单仍有支撑，但极乐观情景下修 |
| HBM4 良率和认证不及预期 | Rubin/MI400/TPU8 推迟，2027 先进封装收入后移 |
| CoWoS 扩产或外包良率不及预期 | GPU/ASIC 出货被封装卡住，客户转向更多 ASIC/多供应商 |
| Samsung/Intel 二供进展快于预期 | TSMC 垄断溢价被部分压缩，但整个市场扩大 |
| 地缘与出口管制升级 | 中国国产链受益，全球设备材料和高端代工不确定性上升 |
| 先进封装价格战 | OSAT/基板毛利先受压，TSMC/HBM/EDA/设备仍较稳 |

## 10. 主要资料来源

| 来源 | 关键用途 |
|---|---|
| [TSMC 1Q26 Quarterly Results](https://investor.tsmc.com/english/quarterly-results/2026/q1) | 1Q26 revenue、gross margin、HPC/advanced nodes mix、2Q26 guidance |
| [TSMC 1Q26 Earnings Transcript PDF](https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf) | AI/HPC 需求、capex、advanced packaging、N2/N3 管理层口径 |
| [TSMC 2026 Technology Symposium PDF](https://pr.tsmc.com/system/files/newspdf/attachment/36a83a1c01678afe9df8e589f352fdfb6b11bc1d/2026%20Tech%20Symposium%20%28C%29_final_wmn.pdf) | A14、N2U、CoWoS 5.5x/14x reticle、SoIC、COUPE、System-on-Wafer 路线 |
| [TrendForce: TSMC CoWoS capacity and CoPoS](https://www.trendforce.com/news/2026/04/16/news-tsmc-says-cowos-offers-industrys-largest-reticle-size-packaging-amid-intel-emib-rivalry-copos-advances/) | CoWoS 2026/2027 产能估计和 advanced packaging 竞争 |
| [Gartner semiconductor revenue forecast 2026](https://www.gartner.com/en/newsroom/press-releases/2026-04-08-gartner-forecasts-worldwide-semiconductor-revenue-to-exceed-us-dollars-one-point-3-trillion-in-2026) | 全球半导体、AI 半导体、memory 市场上限校验 |
| [NVIDIA Vera Rubin official release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | Rubin、Vera、Spectrum-6、CPO、LPX、2026 H2 availability |
| [OpenAI/Broadcom strategic collaboration](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/) | 10GW custom accelerator、2026 H2 开始部署 |
| [Samsung 1Q26 earnings presentation PDF](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2026_1Q_conference_eng.pdf) | Samsung Foundry/HBM/advanced packaging 口径 |
| [Samsung GTC 2026 HBM4E and NVIDIA partnership](https://news.samsung.com/global/samsung-unveils-hbm4e-showcasing-comprehensive-ai-solutions-nvidia-partnership-and-vision-at-nvidia-gtc-2026) | HBM4E、AI semiconductor vertical integration |
| [ASML Q1 2026 results](https://www.asml.com/en/investors/financial-results/q1-2026) | EUV/High-NA、logic/memory demand、equipment backlog |
| [FormFactor 1Q26 results](https://investors.formfactor.com/news-releases/news-release-details/formfactor-inc-reports-2026-first-quarter-results) | AI/HBM/advanced packaging probe card demand |
| 本项目 `ai_chip_research_2026_2027.md` | 2026/2027 AI 芯片出货路径、金额情景、技术拆解 |
| 本项目 `conference_update/nvidia_gtc_2026_research.md` | GTC 2026 一手信息整理、Rubin/LPX/STX/DSX 路线 |
| 本项目 `conference_update/isscc_2026_ai_ic_soc_research.md` | HBM4、UCIe、CPO、供电、CIM、AI SoC 技术指标 |
| 本项目 `conference_update/chiplet_summit_2026_update.md` | HBM 市场、UCIe 3.0、advanced packaging、photonic interposer |
| 本项目 `conference_update/date_2026_conference_research.md` | Agentic EDA、3DIC、chiplet、thermal/IR/EM-aware design |
| 本项目 `conference_update/designcon_2026_conference_update.md` | 224G/448G、PCIe 7/8、CPO/OIO、AI rack power/thermal |

---

非投资建议。本报告用于产业链研究和情景分析；所有市场规模为基于公开信息和 AI 芯片路线图的推算区间，实际结果会受客户 capex、良率、封装产能、HBM 供应、地缘政策和融资环境影响。
