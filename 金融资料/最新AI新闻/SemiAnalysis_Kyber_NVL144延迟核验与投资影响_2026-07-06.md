# SemiAnalysis Kyber NVL144 延迟传闻核验与投资影响

报告日期：2026-07-06  
事件口径：SemiAnalysis 在 X 上发布的 Kyber / Rubin Ultra 相关爆料，以及华尔街见闻中文转述。本文不使用实时股价和盘前价格，只评估事实可靠性、产业链传导和项目内投资机会。  
项目内引用范围：只读取 `公司调研/`、`行业调研/`、`分析报告/公司评估/` 与 `日度资料/` 相关资料；未使用 `特征量化/`。

## 一句话结论

这篇文章“作为 SemiAnalysis 爆料的转述”基本可靠，但“Kyber NVL144 已被英伟达正式延迟 12 个月以上、且主因确定为 PCB 中板制造困难”仍不是官方确认事实，当前应按中等可信的供应链传闻处理。

投资上，最重要的变化不是 2026 年英伟达 Blackwell / GB300 主线崩塌，而是 2027-2028 年 Rubin Ultra / Kyber 的极度乐观情景下修。相应地，第二供给、更多 NVL72 / GB300 / Rubin NVL72 机架、铜互联和 AEC、高密供电、液冷、机架集成、HBM3E/4 供应链的确定性权重上升；纯 Kyber 中板 PCB、短期 CPO 放量和 800VDC 立即量产叙事的权重要下调。

## 可靠性核验

### 已确认事实

1. **SemiAnalysis 爆料本身存在**  
   可检索到 SemiAnalysis 在 X 上的帖子链接，标题片段包括 “MASSIVE DELAY” 和 “Kyber NVL144 rack architecture has been delayed to 2028”。未登录环境无法完整读取 X 正文，因此本文把它作为“可检索到的原始爆料”，不把全文细节当作独立可审计来源。

2. **中文文章确实是在转述 SemiAnalysis 的系列推文**  
   华尔街见闻文章称 SemiAnalysis 连发六条推文，核心说法是 Kyber NVL144 延迟超过 12 个月，可能推迟到 2028 年，主要瓶颈是 PCB 中板制造。文章还转述了 NVL576 / CPO、Rubin Ultra 四计算芯片版本取消、AMD / Google / PCB / CCL / ODM 影响等观点。

3. **Kyber / NVL144 是英伟达官方路线图中的真实架构选项**  
   NVIDIA 2026-03-16 官方技术博客确认：Vera Rubin NVL72 计划在 2026 年下半年出货；Rubin Ultra NVL576 由 8 个 72-GPU MGX NVL 机架组成；Kyber 会把单机架 NVLink 域从 72 GPU 提升到 144 GPU，并作为 Vera Rubin Ultra 的独立 NVL144 选项出现。官方同时说明相关规格仍可能变更。

4. **相邻约束已有独立交叉印证**  
   TrendForce 2026-04-08 报道称 Rubin 放量有延期压力，涉及 HBM4 验证、CX8 到 CX9 网络转换、更高功耗和液冷优化，Blackwell 仍会贡献 2026 年高端 GPU 出货大头。TrendForce 2026-04-01 和 Tom's Hardware 2026-06-30 也都报道过 Rubin Ultra 从四计算芯片转向双计算芯片的传闻，理由集中在先进封装和制造执行难度。

5. **CPO / 光互联长期重要，但短期不等于大规模可收入化**  
   NVIDIA 2026 年已分别与 Coherent、Lumentum 达成战略合作，各投资 20 亿美元，并包含多年采购承诺和产能访问权。这支持“光互联是长期路线”的判断，但不能证明 NVL576 / Kyber CPO 在 2026-2027 已经顺利量产。

### 可信度分层

| 文章说法 | 可信度 | 核验结论 | 投资处理 |
|---|---:|---|---|
| SemiAnalysis 确实发布 Kyber 延迟爆料 | 高 | 可检索到原始 X 链接，中文文章转述链条清楚 | 可作为事件来源 |
| Kyber NVL144 推迟超过 12 个月、到 2028 | 中 | 逻辑上与官方路线、工程难度和第三方 Rubin 延迟信息一致，但无 NVIDIA 官方确认 | 下调 2027-2028 极度乐观情景，不直接砍 2026 基准 |
| 主因是 PCB 中板制造困难 | 中 | 官方确认 Rubin / MGX 强调 PCB midplane / cable-free 方向；文章给出细节，但未见供应商或官方验证 | 对 Kyber 专用超高难度中板谨慎；普通高阶 PCB 不能一并看空 |
| 78 层 PCB、M9 CCL、石英布、PTFE、25um 线宽线距等细节 | 中低 | 技术上可解释，但来源仍主要是 SemiAnalysis / 转述文章 | 不作为单一供应商订单判断依据 |
| NVL72x2 back-to-back 方案取消 | 中低 | 只有文章转述，缺少官方或客户侧确认 | 作为“需求端不接受复杂替代方案”的风险信号 |
| NVL576 / CPO 大规模化后移 | 中 | 官方确认 NVL576 依赖铜和直接光连接；NVIDIA 投资光器件说明路线重要；但具体延迟无官方确认 | 下调短期 CPO 量产权重，保留 2027-2028 期权 |
| 四计算芯片 Rubin Ultra 取消、双计算芯片保留 | 中高 | 已有 TrendForce 与 Tom's Hardware 独立报道，且与封装约束一致 | 下调单颗封装极限叙事，上调“更多系统/更多机架”叙事 |

## 我的可靠性结论

这条新闻的可用级别是：**中等可信、不可当作官方事实、足以调整情景权重**。

不能做的动作：

- 不能因为这篇文章就认定 NVIDIA 2026 年主线崩塌。
- 不能把 “PCB 中板制造困难” 简化成单一 PCB 供应商出问题。
- 不能把所有 PCB / CCL / 连接器一概看空。
- 不能把 AMD / Google / Broadcom 受益直接等同为可确认收入。

应该做的动作：

- 把 Kyber / Rubin Ultra / NVL144 从 2027 年较高权重的乐观项，下调为 2027-2028 低到中可信期权。
- 把 Blackwell / GB300 / Rubin NVL72 / 更多机架数量 / 第二供给 / 铜互联 / 电力液冷 / 机架集成作为更现实的 2026-2027 传导链。
- 对短期 CPO、800VDC、超高层 Kyber 中板 PCB 主题做证据折扣。

## 投资点变化

### 1. NVIDIA：近端基准不动，远端极度乐观下修

项目内 `NVDA_NVIDIA_收入传导估值评估_2026-06-20.md` 的主线本来就是 Blackwell / GB300、networking attach、Rubin 小比例贡献；Rubin / Kyber 没有被放进 2026 基准大项。

这次事件后的调整：

| 维度 | 原判断 | 事件后调整 |
|---|---|---|
| 2026 收入主线 | Blackwell、GB300、NVL72、networking attach | 基本不变 |
| Rubin NVL72 | 2026H2 开始贡献，仍需看客户接受与供应链 | 不因 Kyber 传闻直接否定 |
| Rubin Ultra / Kyber | 2027+ 上限项 | 极度乐观权重下修，推迟到 2028 的概率上升 |
| 估值叙事 | CUDA + GPU + NVLink + networking + rack-scale moat | 护城河仍在，但“每代密度跃迁无摩擦”的叙事打折 |
| 反证指标 | rack acceptance、HBM4、CoWoS、liquid/power、networking | 增加 PCB midplane / CPO / hyperscaler topology acceptance |

操作含义：如果市场把这条新闻理解成“2026 NVIDIA 订单崩塌”，那是过度解读；如果市场此前给了 Kyber / Rubin Ultra 过高的 2027-2028 确定性溢价，则需要下修。

### 2. AMD：第二机架生态窗口上升，但仍要折扣

项目内 AMD 报告已经把 MI450 / Helios 放在 H2 2026 之后逐步确认，并强调 HBM4、机架良率、ROCm、UALink / Ultra Ethernet、客户验收是核心约束。

这次事件给 AMD 的边际变化是正向的，但不是无条件利好：

- 正向：如果 Kyber / NVL144 延后，hyperscaler 对第二供给和开放机架生态的议价需求会上升。
- 正向：Helios / MI450 / 后续 MI500 的战略价值上升，尤其是在客户不愿完全绑定 NVIDIA rack-scale 路线时。
- 约束：AMD 仍要证明 ROCm 迁移、HBM4 供应、整机良率、开放网络、客户验收和收入确认。
- 结论：上调 AMD 乐观情景的可参与需求池，不把它直接搬进基准收入。

更适合跟踪的不是“AMD 概念受益”，而是：

- Oracle / Meta / OpenAI 等客户的 MI450 / Helios 交付与验收时间。
- HPE / Juniper / Broadcom 开放 scale-up 网络是否进入实际集群。
- AMD 是否披露更多 Instinct backlog、AI accelerator 收入或 rack-level 订单。

### 3. Broadcom / Google / 云厂 ASIC：第二供给价值上升

项目内 `行业调研_云厂自研AI ASIC_2026-06-10.md` 已经把 2026-2027 年云厂 ASIC 作为 GPU 之外的强需求池，核心逻辑是：当 GPU / HBM / 封装 / 机架交付存在不确定性时，云厂更愿意用自研 ASIC 分散供给、TCO 和架构风险。

这次事件强化了这个判断：

- Google TPU / Broadcom XPU 的相对战略权重上升。
- Broadcom 的 custom XPU、AI Ethernet / Fabric、SerDes / 光电 I/O 价值上升。
- AWS Trainium、Meta MTIA、Microsoft Maia 等也因“非 NVIDIA 单一路线”而获得更高配置权重。

但需要保持边界：ASIC 不是免费替代，仍受 HBM、先进封装、软件栈、互联、液冷、电力和客户工作负载绑定约束。

### 4. PCB / CCL：不能一刀切，Kyber 专用中板下修，广义高阶 PCB 分化

文章最容易被误读的地方是把“Kyber PCB 中板困难”扩大成“AI PCB 全线利空”。

更合理的拆分：

| 子方向 | 事件影响 | 解释 |
|---|---|---|
| Kyber NVL144 专用超高层 midplane | 负面 | 如果 2027 出货后移，相关中板 / 高端 CCL 订单确认延后 |
| 普通高端 GPU / switch / server PCB | 中性到小正 | 更多 GB300 / NVL72 / Oberon / Rubin NVL72 机架可能增加系统数量 |
| M9 / M10 CCL、PTFE、石英布等高端材料 | 分化 | Kyber 专案延迟负面，但高速网络与高端 switch 材料升级仍在 |
| ODM / JDM 机架集成 PCB | 中性到小正 | 如果从单架 144 GPU 回到更多 72 GPU 机架，系统数量和测试集成工作量可能增加 |

项目内行业资料对 PCB / 连接器已经有类似边界：普通 PCB、低端线束和传统连接器不是最优暴露；更值得看的是高速连接器、cabled backplane、AEC / DAC、retimer / SerDes、高端 PCB / CCL 中真正绑定 AI rack 认证的供应商。

### 5. 铜互联 / AEC / 连接器：边际上修

如果 Kyber 的 PCB midplane 走不顺，且 CPO / NVL576 也后移，那么短中期更可能出现的是：

- 更多 NVL72 / GB300 / Rubin NVL72 机架。
- 更多短距铜缆、AEC / DAC、连接器、cabled backplane、retimer / SerDes。
- 更多机架内、机架间的布线、测试、诊断和现场维护需求。

项目内 CRDO 和 ALAB 相关公司评估对这个方向已经有高权重：

- CRDO：800G / 400G AEC 是已收入化主线，1.6T / 224G AEC、Optical DSP、PCIe / CXL retimer、Blue Heron scale-up retimer是上修项。
- ALAB：Aries / Scorpio / Taurus、PCIe / CXL、AEC / smart cable、NVLink Fusion / UALink / optical 相关机会主要在 2027-2028。

事件后更合理的配置是：上调 AEC / DAC / retimer / SerDes / 高速连接器的二阶弹性；但不要把所有线缆厂都当作高毛利 AI 受益股。

### 6. CPO / 光器件：短期降温，长期不变

这次事件对 CPO 的影响是“双向”的：

- 短期负面：如果 NVL576 / scale-up CPO 因交换芯片、外部光源、封装、散热、可维护性或客户接受度后移，2026-2027 年的 CPO 大规模收入要折扣。
- 长期正面：NVIDIA 对 Coherent、Lumentum 的投资和采购承诺说明光互联不是伪需求，而是高密度 AI 系统继续扩展的必要路线。

对应公司：

- LITE：EML / InP 激光、800G / 1.6T、OCS、UHP / ELS 是主线；scale-up CPO late CY27 后的机会不能提前计入 2026 基准。
- COHR：1.6T、InP / EML / CW laser、OCS、CPO / ELS 是中长期主线；产品级收入和客户确认仍要折扣。

配置含义：不要用“Kyber 延迟”否定所有光器件；但要把“2026 就靠 CPO 大规模放量”的激进假设下修。

### 7. HBM / DRAM：总需求不一定下降，结构和时间点变化

文章提到四计算芯片 Rubin Ultra 取消、双计算芯片保留，这可能降低单包极限 HBM4 配置，但如果 NVIDIA 改卖更多 Oberon / Rubin / Rubin Ultra 机架，总 HBM 需求未必一比一下降。

更重要的变化：

- HBM4 / HBM4E 的时间点更重要，2027 高端需求可能后移或更分散。
- HBM3E 与 Blackwell / GB300 延续更有支撑。
- 若 AMD / Google / Broadcom / AWS 等第二供给占比提高，HBM 需求从 NVIDIA 单一路线分散到更多客户。

项目内 HBM 研究的原判断不变：SK hynix、Micron、Samsung 仍是核心供给；CXL / SOCAMM / eSSD 等不是 HBM 替代，而是内存墙分层补充。

### 8. ODM / EMS / 机架集成：数量逻辑可能上修，利润要筛选

Kyber 延迟并不一定减少 AI 机架数量。相反，如果单机架 144 GPU 密度跃迁推迟，客户可能用更多 72 GPU 机架和更多 GB300 / Rubin NVL72 系统补足算力。

受益方向：

- SMCI / Dell / HPE / Lenovo 等整机与机架集成商：订单数量和复杂度可能上升，但毛利取决于客户、GPU / 网络透传比例、验收和现金流。
- Flex / Jabil / Celestica：更适合看电力、液冷、系统集成、测试和高附加值制造，而不是低毛利普通 assembly。
- HPE：如果 AMD Helios / Juniper / Open Ethernet 第二生态增强，HPE 的相对弹性高于普通服务器厂。

项目内 SMCI 报告已经强调：AI rack 收入强，但 GPU / 网络 / 液冷组件采购、客户验收、营收确认、库存与应收是关键风险。这次事件并没有消除这些风险。

### 9. 电力 / 液冷：更确定，不更弱

Kyber 延迟对电力液冷不是明显利空。原因是客户仍要上算力，如果密度跃迁放慢，可能用更多机架、更多 CDU、更多配电、更多现场工程来弥补。

项目内电力液冷研究已经把 2026 主线放在：

- 48 / 54V 高功率 rack power。
- UPS、switchgear、busway、PDU、power shelf。
- Direct-to-chip liquid cooling、CDU、manifold、RDHx、heat rejection。
- 预制化电力 / 冷却模块和现场 commissioning。

事件后调整：

- VRT / ETN / Schneider / nVent / Modine / Flex 等电力液冷链条主线不变。
- 800VDC / PowerDirect 5000 / HVDC sidecar 这种与 Rubin Ultra / Kyber 高密度架构强绑定的远期期权要下调近端权重。
- Flex 的 Power / Cloud & Cooling、Vertiv 的高密 AC 电力链 / 液冷 / OneCore 更值得看可确认订单和 backlog 转化。

## 项目内机会排序

### A. 基准机会：不靠 Kyber 也能成立

| 方向 | 代表公司或资产 | 逻辑 | 关键反证 |
|---|---|---|---|
| NVIDIA 近端主线 | NVDA | Blackwell / GB300 / NVL72 / networking attach 仍是 2026 核心 | GB300 / Rubin NVL72 验收延迟、毛利下行、capex 放缓 |
| 云厂 ASIC / AI fabric | AVGO、Google TPU 产业链、AWS Trainium 相关 | 第二供给、TCO、定制 ASIC 和以太网 fabric 权重上升 | HBM / CoWoS / 软件栈 / 客户项目延期 |
| 高密电力液冷 | VRT、ETN、Schneider、FLEX、MOD | 更多机架和更复杂现场交付仍需要电力与冷却 | 电网接入、site readiness、液冷验收、营运资本 |
| HBM / 高端 DRAM | MU、SK hynix、Samsung | HBM3E / HBM4 和 server DRAM 仍是上游瓶颈 | HBM4 资格推迟、客户库存、DRAM 价格反转 |

### B. 上修机会：这条事件提高二阶弹性

| 方向 | 代表公司或资产 | 为什么上修 | 进入基准的条件 |
|---|---|---|---|
| AEC / DAC / active copper | CRDO、Amphenol、TE、Molex、Samtec、Luxshare 等 | 如果 CPO / Kyber 后移，短距铜和 cabled backplane 继续承担主流连接 | 1.6T / 224G 客户量产订单、毛利不被多供压低 |
| Retimer / SerDes / PCIe-CXL | ALAB、CRDO、MRVL、AVGO | 更多机架和更复杂 IO 提高信号完整性价值 | 产品从 design-in 转收入、客户平台明确 |
| 开放机架生态 | AMD、HPE / Juniper、Broadcom | Kyber 延迟提高非 NVIDIA 第二生态战略价值 | Helios / MI450 / Open Ethernet 客户验收 |
| ODM / EMS 高附加值集成 | HPE、FLEX、JBL、CLS、SMCI | 更多 NVL72 / GB300 / ASIC rack 可能增加系统集成、测试和 commissioning | 订单转收入、毛利率不被 pass-through 吞噬 |

### C. 下修或等待确认

| 方向 | 调整 | 原因 |
|---|---|---|
| Kyber 专用超高层 PCB midplane | 下修近端权重 | 如果传闻属实，2027 出货和订单确认后移 |
| 短期 CPO 大规模收入 | 下修 2026-2027 权重 | NVIDIA 战略投入不等于 scale-up CPO 马上量产 |
| 800VDC 立即量产 | 下修近端权重 | 与 Rubin Ultra / Kyber 高密 rack 绑定较强，项目内也只作为 2027+ 设计导入 |
| 单纯低端 PCB / 线束 / 组装 | 不上修 | 价值量和利润率不等于 AI rack 技术瓶颈 |

## 情景重估

| 情景 | 概率方向 | 组合含义 |
|---|---|---|
| 传闻被 NVIDIA / ODM 间接证实，Kyber 到 2028 | 概率上升 | 下调 NVDA 远期密度跃迁溢价；上调 AMD / AVGO / AEC / 电力液冷 / 机架集成 |
| 只是 Kyber 小幅延期，NVL576 / Rubin Ultra 仍按节奏推进 | 概率下降但保留 | CPO / 高端 PCB / 800VDC 恢复部分权重；NVDA 远期溢价修复 |
| NVIDIA 用更多 NVL72 / Oberon / GB300 / Rubin NVL72 替代 | 概率上升 | 对 GPU 数量、HBM、系统集成、电力液冷、铜互联更友好；对单机架极限中板不友好 |
| AMD / Google / Broadcom 第二生态超预期 | 概率小幅上升 | AVGO / AMD / HPE / CRDO / ALAB 等弹性上升，但必须看到订单和验收 |
| 整个 AI capex 放缓 | 不是本文主线 | 如果同时出现云厂 capex 下修、GPU 租赁利用率下行、数据中心延迟，则所有链条都要下修 |

## 后续跟踪清单

### 需要看官方或硬证据

- NVIDIA 后续财报电话会是否提到 Rubin Ultra、NVL144、NVL576、Kyber、CPO、midplane、rack acceptance。
- NVIDIA / ODM / cloud partner 对 Vera Rubin NVL72 的 H2 2026 出货节奏是否变化。
- Dell / HPE / Supermicro / Quanta / Wiwynn 等是否出现 Rubin / Kyber 订单或认证延后表述。
- PCB / CCL 厂商是否披露高层数 AI backplane 订单推迟、重新设计或良率问题。
- Coherent / Lumentum 是否把 CPO / ELS / UHP 的收入确认从 2026-2027 后移。
- AMD / HPE / Broadcom 是否出现 Helios / Open Ethernet / MI450 真实量产客户。

### 可交易观察点

- 若 NVDA 因 Kyber 传闻大跌，但 Blackwell / GB300 / NVL72 指引不变，可能是近端主线错杀。
- 若 CPO 纯概念和 Kyber 专用 PCB 继续维持高溢价，而没有客户 / 订单 / 量产证据，应降低暴露。
- 若 CRDO / ALAB / 连接器 / power / cooling 公司在订单与指引中确认更多 AI rack 需求，二阶机会比“单纯抢 NVIDIA 份额”的逻辑更稳。
- 若 AMD / AVGO / HPE 的客户部署披露变实，第二生态机会从期权上移到基准。

## 结论

这篇文章值得重视，但不能按标题直接交易。它真正改变的是远期权重，而不是当季基本面：

1. **NVDA 2026 基准主线不应因 Kyber 传闻直接下修**，但 Rubin Ultra / Kyber 的 2027-2028 极度乐观假设要降权。
2. **AMD / AVGO / Google TPU / 云厂 ASIC 的战略权重上升**，但收入确认仍需客户、HBM、封装、软件和验收闭环。
3. **铜互联、AEC、retimer、连接器、高密电力、液冷、机架集成更受益于“更多机架、更复杂系统”的路径**。
4. **短期 CPO、Kyber 专用 PCB 中板、800VDC 立即量产要更谨慎**，这些方向应从基准收入退回到设计导入或远期期权。
5. **项目内原有框架基本被验证**：Blackwell / GB300 / NVL72、HBM、networking、电力液冷和第二供给是现实主线；Rubin Ultra / Kyber / CPO / 800VDC 是高弹性但低确定性的后续观察项。

## 外部核验源

- 华尔街见闻，2026-07-06，SemiAnalysis 转述文章：https://wallstreetcn.com/articles/3776238
- NVIDIA Developer Blog，2026-03-16，Vera Rubin POD / NVL72 / NVL576 / Kyber 路线：https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/
- NVIDIA Newsroom，2026-03-16，Rubin 平台和云厂 / OEM 合作：https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer
- NVIDIA NVLink 官方页面，Vera Rubin NVL72 / NVLink 6 规格说明：https://www.nvidia.com/en-us/data-center/nvlink/
- TrendForce / I-Connect007，2026-04-08，Rubin 延迟与 Blackwell 2026 高端 GPU 份额：https://iconnect007.com/article/149537/rubin-faces-delays-blackwell-to-drive-70-of-nvidia-highend-gpu-shipments-in-2026/149534/design
- TrendForce，2026-04-01，Rubin Ultra 双 die / 封装约束：https://www.trendforce.com/news/2026/04/01/news-nvidias-rubin-ultra-seen-sticking-to-dual-die-design-on-packaging-constraints-tsmc-3nm-demand-intact/
- Tom's Hardware，2026-06-30，Rubin Ultra 四 die 取消传闻：https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-reportedly-cancels-quad-die-rubin-ultra-gpu-in-favor-of-dual-gpu-design-report-claims-complex-design-purportedly-scrapped-over-manufacturing-execution-concerns
- NVIDIA / Coherent 战略合作，2026-03-02：https://nvidianews.nvidia.com/news/nvidia-and-coherent-announce-strategic-partnership-to-develop-optics-technology-to-scale-next-generation-data-center-architecture
- NVIDIA / Lumentum 战略合作，2026-03-03：https://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology
- AMD Helios 官方资料：https://www.amd.com/en/blogs/2025/amd-helios-ai-rack-built-on-metas-2025-ocp-design.html

## 项目内引用

- `分析报告/公司评估/NVDA_NVIDIA_收入传导估值评估_2026-06-20.md`
- `分析报告/公司评估/AMD_Advanced_Micro_Devices_收入传导估值评估_2026-06-20.md`
- `分析报告/公司评估/AVGO_Broadcom_收入传导估值评估_2026-06-20.md`
- `分析报告/公司评估/HPE_惠普企业_收入传导估值评估_2026-06-20.md`
- `分析报告/公司评估/CRDO_Credo_Technology_Group_收入传导估值评估_2026-06-12.md`
- `分析报告/公司评估/ALAB_AsteraLabs_收入传导估值评估_2026-06-12.md`
- `分析报告/公司评估/LITE_Lumentum_收入传导估值评估_2026-06-12.md`
- `分析报告/公司评估/COHR_Coherent_收入传导估值评估_2026-06-20.md`
- `分析报告/公司评估/VRT_Vertiv_收入传导估值评估_2026-06-20.md`
- `分析报告/公司评估/FLEX_Flex_Ltd_收入传导估值评估_2026-06-12.md`
- `行业调研/产业背景/行业调研_头部AI芯片全景与产能释放_2026-06-10.md`
- `行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`
- `行业调研/AI网络_光互联_铜互联/行业调研_高速连接器、背板与结构化布线_2026-06-11.md`
- `行业调研/AI网络_光互联_铜互联/行业调研_AEC、DAC与高速铜缆_2026-06-11.md`
- `行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`
- `行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`
- `行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`
- `行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`
