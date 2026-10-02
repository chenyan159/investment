# 行业调研：【InfiniBand与专有Scale-up互联】

截至日期：2026-05-08  
研究口径：本报告聚焦 AI 计算中心里连接加速器的高性能互联系统，重点覆盖 InfiniBand、NVIDIA NVLink/NVSwitch、NVIDIA Spectrum-X/Quantum-X、Broadcom 以太网 scale-up/scale-out、UALink/UEC、Google TPU ICI/Apollo OCS、AWS NeuronLink/EFA、AMD Infinity Fabric/UALoE、华为/寒武纪等超节点互联，以及配套的 NIC/DPU/SuperNIC、交换芯片、交换机系统、铜缆/DAC/AEC/LACC、CPO/硅光/ELS、测试认证和 fabric 管理软件。美元口径为名义收入或订单规模估算，`B`=十亿美元，`M`=百万美元。对于自用 ASIC 和内部互联，采用“等效外部采购/内部转移价值”估算。

## 0. 一页结论

1. **2026 年最确定的技术路径仍是“NVIDIA rack 内 NVLink/NVSwitch + rack 间 InfiniBand 或 Spectrum-X”。** GB200/GB300 已经把 NVLink fabric 变成每个 NVL72 rack 的默认 BOM，Vera Rubin NVL72 在 2026H2 接棒，NVLink 6 提升到每 GPU 3.6TB/s、单 rack 260TB/s。NVIDIA FY2026 Q4 数据中心 networking revenue 已达 $11.0B，同比 +263%，全年 networking $31.4B，同比 +142%，说明网络已经不是配角。
2. **InfiniBand 仍是 NVIDIA 大训练集群的“性能保险”，但市场份额压力来自 Ethernet。** Quantum-X800 已到 800G、144 ports/switch，并具备 SHARP v4、adaptive routing、telemetry congestion control。挑战是 Dell'Oro 已判断 Ethernet 在 AI back-end switch 中反超，2025 年 Ethernet AI back-end switch sales 超过 InfiniBand 两倍以上，且预计 AI back-end switch market 2030 年超过 $100B。
3. **专有 scale-up 的核心战场从“谁的链路最快”变为“谁能把 72-1,024 个 accelerator 当作可运营资产”。** NVLink 的壁垒是 GPU 原生集成、SHARP collective、CUDA/Dynamo/Mission Control 软件闭环；Broadcom/Meta/OpenAI 的路线是用 Ethernet scale-up/scale-out/across 做更开放、更可采购的 rack 级 fabric；UALink 则试图把 accelerator pod 内部互联标准化。
4. **2026 年的最大拐点是 Ethernet 开始侵入 scale-up，而不是只赢 scale-out。** Broadcom Tomahawk 6 已 production volume shipping，102.4T、512×200G/1024×100G SerDes，单芯片可连接 512 XPUs 做单跳 all-to-all；Tomahawk Ultra 主打 250ns latency；Jericho 4 面向 1M+ XPU lossless fabric。Meta >1GW MTIA 和 OpenAI 10GW Broadcom 均明确采用 Ethernet scale-up/scale-out。
5. **UALink 2026 仍是 early ramp，2027 才是商业放量窗口。** UALink 1.0 是 200G per lane、最多 1,024 accelerators/pod；2.0 计划 2026Q2 引入 in-network compute；3.0 目标 2027 面向更高带宽、跨 rack/row reach 和更强可靠性。2026 的收入主要来自 IP、switch silicon、验证、early rack；2027 才可能被 AMD Helios、Meta/Open Rack、部分云厂自研 ASIC 拉动。
6. **光互联和铜互联不是互斥，而是距离和功耗分层。** 2026 rack 内/短距 scale-up 仍大量依赖 NVLink 铜缆、LACC、DAC/AEC、高速 backplane 和 CPO 前的电连接；rack 间与 scale-out 继续由 800G/1.6T 光模块承接；CPO/CPX/NPO/OCI 是 2027-2028 的高端 switch 和 optical scale-up 方向。
7. **价值捕获排序：NVIDIA 全栈 proprietary fabric > switch/NIC/DPU silicon > 高端 CPO/1.6T 光器件/DSP > fabric 软件与认证 > 交换机白盒/线缆组装。** 但 2026-2027 的高 beta 来自 1.6T Ethernet、Broadcom/Marvell/ASIC 互联、UALink IP/switch、CPO/ELS、铜缆/AEC/retimer 和测试设备。

## 1. 行业定义：Scale-up、Scale-out、Scale-across

### 1.1 三层网络

| 层级 | 典型距离 | 目标 | 代表技术 | 2026 关键变化 |
|---|---:|---|---|---|
| Scale-up | 同机箱、同 rack、少数 rack | 把多个 GPU/XPU 变成一个近似共享内存/统一 accelerator domain | NVLink/NVSwitch、UALink、Broadcom Ethernet scale-up、Google ICI、AWS NeuronLink、AMD Infinity Fabric/UALoE、华为 UB/HCCS 类互联 | 从 NVIDIA proprietary 主导，进入 Ethernet/UALink 竞争窗口 |
| Scale-out | rack 间、pod 内、机房内 | 连接多台 accelerator server/rack，做分布式训练和推理 | InfiniBand、Spectrum-X/RoCE、UEC Ethernet、Arista/Cisco/HPE Ethernet、Google/AWS 自研网络 | 800G 主流化，1.6T 开始导入，Ethernet 份额扩大 |
| Scale-across | 楼宇、campus、metro、regional | 跨数据中心或跨园区把多个 AI factory 连接为容量池 | Spectrum-XGS、coherent pluggables、1600ZR/ZR+、Ciena/Nokia line system、OCS | 2026 从传统 DCI 升级为 AI regional fabric |

### 1.2 为什么 InfiniBand 与专有 Scale-up 仍值得单独研究

AI 网络不是普通数据中心 leaf-spine。训练和 agentic inference 的成本函数是 `GPU利用率 x tail latency x collective效率 x 故障恢复 x 每瓦 token`。因此互联能定价的原因不是端口数，而是它能否让一台价值数百万美元的 rack 多跑 1-5% 的有效 token 或缩短数周训练周期。

2026 年主要矛盾是：

- **性能极限：** NVLink/InfiniBand 仍有低延迟、collective offload、GPU 生态协同优势。
- **可采购性：** Ethernet/UEC/UALink 的多供应商、开放标准和运维熟悉度吸引 hyperscaler。
- **电力约束：** CPO、OCS、低功耗 copper、retimerless/LPO 都在争夺同一目标：用更低 bit/W 保持 accelerator 利用率。
- **客户锁定：** NVIDIA 把 GPU、NVLink、InfiniBand/Spectrum、DPU、软件、MGX rack 和 DSX 打包；Broadcom/Meta/OpenAI 则把 XPU、Ethernet、PCIe、optics、SerDes、retimer 打包成开放但高度定制的供应链。

## 2. 公开事实锚点

| 类别 | 关键数字/事实 | 产业含义 |
|---|---|---|
| NVIDIA networking | FY2026 Q4 Data Center Networking revenue $11.0B，同比 +263%，环比 +34%；FY2026 networking $31.4B，同比 +142%。 | NVLink、InfiniBand、Ethernet 已经成为 NVIDIA 数据中心收入的独立高增长引擎。 |
| NVIDIA NVLink 6 | 每 GPU 3.6TB/s，72 GPU all-to-all，单 Vera Rubin NVL72 rack 260TB/s。 | 2026H2 Rubin 后，rack 内 scale-up 价值继续上移。 |
| NVIDIA Quantum-X800 | 800Gb/s 端到端 InfiniBand；Quantum-X800 switch 144×800G；ConnectX SuperNIC up to 1.6Tb/s per GPU。 | 2026 大训练集群继续有 InfiniBand 高确定需求。 |
| NVIDIA Vera Rubin | 七类芯片 full production：Vera CPU、Rubin GPU、NVLink 6、ConnectX-9、BlueField-4、Spectrum-6、Groq 3 LPU；2026H2 伙伴供货。 | NVIDIA 从 GPU 出货转为 rack/POD/GW 级系统出货。 |
| Broadcom Tomahawk 6 | 102.4Tbps switch，production volume shipping；单芯片支持 512×200G 或 1024×100G SerDes；可连接 512 XPUs 做 scale-up。 | Ethernet 的 scale-up 可信度大幅上升。 |
| Broadcom OFC 2026 | 3.5D XPU production、102.4T CPO switch、400G/lane optical DSP、Thor Ultra 800G NIC、Agera 3 retimer、PCIe Gen6。 | Broadcom 提供 XPU + Ethernet + PCIe + optics + SerDes 的完整非 NVIDIA 互联栈。 |
| UALink 1.0 | 200G per lane、最多 1,024 accelerators/pod；93% effective peak bandwidth；成员超过 85 家。 | 开放 scale-up 标准进入 productization 阶段。 |
| UALink roadmap | 2.0 计划 2026Q2，加入 INC；Management/Chiplet spec 同步；3.0 目标 2027。 | 2026 是验证年，2027 是第一代商用 ramp。 |
| UEC | 1.0 规范发布，目标是完整 Ethernet AI/HPC communications stack。 | Ethernet 不只是 RoCE 微调，而是针对 AI/HPC 重构 transport/flow/control。 |
| IDC Ethernet switch | 2025 Ethernet switch revenue $55.1B，+31.5%；data center segment $32.5B，+53.5%；4Q25 data center $9.9B，+63%；NVIDIA 4Q25 data center Ethernet share 15.2%。 | AI 正把 Ethernet switch TAM 重新抬高，NVIDIA 也在 Ethernet 中拿份额。 |
| Dell'Oro AI back-end | 2030 AI back-end switch spending 超过 $100B；800G 已占 AI back-end 主流，2027 预计转向 1.6T，2030 走向 3.2T。 | 2026-2027 网络升级斜率可能高于服务器出货斜率。 |

## 3. 2026 机遇、挑战与正在使用的技术

### 3.1 机遇

| 机遇 | 量化判断 | 最受益方向 |
|---|---:|---|
| AI rack 从 8 GPU server 转向 72+ GPU rack-scale | GB200/GB300/Rubin/Helios/Trainium3 都在提高 rack 内 accelerator 数量 | NVSwitch/NVLink、UALink switch、Broadcom TH6/Tomahawk Ultra、铜缆/AEC/retimer |
| Back-end 网络从 400G/800G 转向 1.6T | OFC 2026 资料指向 2026 1.6T pluggable >500 万只，2027 进入大规模部署 | 1.6T optics、200G/400G SerDes、switch ASIC、NIC/DPU |
| Hyperscaler 自研 ASIC 拉动非 NVIDIA 互联 | OpenAI 10GW Broadcom、Meta >1GW MTIA、Google TPU、AWS Trainium | Broadcom、Marvell、AMD Pensando、UALink/UEC、PCIe/CXL/optics IP |
| Agentic inference 提高 tail-latency 和 KV cache 要求 | 长上下文、多轮 agent、test-time compute 让网络和存储成为 token cost 关键 | NVLink 6、LPX direct links、BlueField-4 STX、CPO、OCS |
| 电力紧缺放大 bit/W 价值 | CPO 5x optical power efficiency、OCS 功耗降低 90%+ 的故事进入采购讨论 | CPO/CPX/NPO、LPO/LACC、ELS、OCS、低功耗 SerDes |

### 3.2 挑战

1. **Ethernet 对 InfiniBand 的份额挤压。** InfiniBand 性能仍强，但 hyperscaler 对多供应商、SONiC/EOS/自研 NOS、成本和供应链弹性更敏感。
2. **Scale-up 标准碎片化。** NVLink、UALink、UALoE、Broadcom proprietary Ethernet extensions、Google ICI、AWS NeuronLink、华为超节点互联并存，软件与测试复杂度上升。
3. **铜互联物理极限。** 224G/448G PAM4、机架内高密布线、损耗、弯折半径、散热、连接器可靠性和可维护性成为真实瓶颈。
4. **CPO 的可维护性与良率。** CPO 能降功耗，但 field replace、ELS 冗余、热漂移、封装良率、测试时间会延迟规模化。
5. **客户认证周期长。** 一套 AI fabric 不是换交换机就行，需要训练框架、collective library、容错、调度、观测、运维 SOP 全栈验证。
6. **高端人才稀缺。** 224G/448G SerDes、switch ASIC、IB/RoCE congestion control、collective offload、硅光封装和大规模 fabric debug 都是小圈子人才。

### 3.3 2026 正在使用的技术全景

| 技术 | 已部署场景 | 2026 状态 | 投资判断 |
|---|---|---|---|
| NVLink 5 / NVSwitch | GB200/GB300 NVL72 rack | 大规模量产，绑定 NVIDIA rack | 2026 最确定、毛利最强，但纯 NVIDIA 暴露 |
| NVLink 6 | Vera Rubin NVL72 | full production，2026H2 伙伴供货 | 2027 大放量核心 |
| Quantum-X800 InfiniBand | NVIDIA 大规模训练/超级计算/neo cloud | 800G，144 ports/switch，ConnectX-8/9 | 高端训练稳，但份额受 Ethernet 压力 |
| Spectrum-X Ethernet | NVIDIA Ethernet scale-out/AI cloud | Spectrum-X800 到 Spectrum-6/SPX，CPO 路线明确 | NVIDIA 在 Ethernet 份额扩张的主线 |
| Broadcom Ethernet scale-up/out/across | Meta MTIA、OpenAI custom ASIC、非 NVIDIA XPU clusters | TH6 production，Tomahawk Ultra/Jericho 4/Thor Ultra | 非 NVIDIA AI fabric 最核心底座 |
| UALink / UALoE | AMD Helios、开放 accelerator pod | 1.0 产品化、2.0/management/chiplet spec 2026 | 2026 小，2027 弹性大 |
| UEC Ethernet | AI/HPC Ethernet transport | 1.0/1.0.2 规范，interop 演示推进 | 打开多厂商后端网络采购 |
| Google ICI / OCS | TPU pod/Ironwood | 内部成熟，OCS 方向强化 | 外部投资映射在 optics/OCS/line system |
| AWS NeuronLink/EFA | Trainium/Inferentia | 内部成熟，Trainium3/4 扩展 | 自研 ASIC 规模验证开放标准压力 |
| 华为 UB/HCCS/CloudMatrix 类互联 | Ascend 超节点/Cluster | 中国市场高确定需求 | 国产供应链替代和软件适配是关键 |

## 4. 2026-2027 头部 AI 芯片技术路径背景下的互联预测

以下表格使用项目内已有 AI 芯片路线图作为背景，不再外部重新搜索芯片出货量。

| 2026-2027 头部芯片/平台 | 互联路径 | 对 InfiniBand/Scale-up 行业的含义 |
|---|---|---|
| NVIDIA B300/GB300 Blackwell Ultra | Rack 内 NVLink 5/NVSwitch，rack 间 Quantum-X800 或 Spectrum-X，scale-out 800G/1.6T optics | 2026 收入主力。每个 NVL72 rack 自带高价值 scale-up fabric，拉动 NVSwitch、铜缆、ConnectX、BlueField、IB/Ethernet switch。 |
| AWS Trainium2 | Rack 内 NeuronLink，scale-out EFA/Ethernet | AWS 自研路线证明 proprietary scale-up 可以在封闭云内部大规模跑通；外部受益在 Ethernet、光模块、交换机、测试。 |
| Google TPU v7 Ironwood | TPU ICI、自研 pod fabric、短距铜 + rack 间光/OCS | Google 的 Apollo OCS 和 TPU 网络会提高光交换、800G/1.6T 模块和线路系统价值。 |
| NVIDIA B200/GB200 Blackwell | NVLink 5 + Quantum/Spectrum | 存量和延续订单继续贡献 NVLink/IB revenue。 |
| Huawei Ascend 910C/950 | 自研超节点互联 + 国产交换/光模块 | 中国市场绕开 NVIDIA，拉动国产以太网/光模块/连接器/交换芯片，但软件和 HBM 限制真实效率。 |
| Cambricon MLU 590/690 | MLU-Link/OAM + Ethernet/optics | 国产 AI 集群扩大后，标准 Ethernet 与国产 fabric 管理软件需求上升。 |
| AMD MI350/MI355 | 8-GPU UBB/Infinity Fabric + Ethernet scale-out | 2026 企业与云端第二供给源，但 scale-up domain 小于 NVL72。 |
| AWS Trainium3 | 144-chip UltraServer，NeuronSwitch/Neuron Fabric + EFA | 自研 ASIC scale-up domain 变大，验证非 NVIDIA fabric 的经济性。 |
| Meta MTIA 300/400/450/500 | Broadcom XPU + Ethernet scale-up/out/across | 2026-2029 多 GW 级部署，是 Broadcom Ethernet scale-up 的最强样板。 |
| Microsoft Maia 200 | Azure 自研后端网络 + 内部 scale-up | 对外少卖设备，但拉动 Azure 数据中心 Ethernet/optics/液冷/时钟/同步。 |
| OpenAI/Broadcom custom accelerator | Broadcom Ethernet + PCIe + optics，2026H2 起 10GW | 非 NVIDIA AI fabric 订单能见度最高的长期项目之一。 |
| AMD MI400/MI455X Helios | 72 GPU rack，UALink/UALoE scale-up + UEC/Ethernet scale-out | 2027 UALink/UALoE 商业化最重要载体。 |

### 4.1 新技术成熟和放量时间：三情景

| 技术 | 2026-05 成熟度 | 基准成熟/放量 | 乐观成熟/放量 | 极度超预期乐观 |
|---|---|---|---|---|
| NVLink 5/NVSwitch | 成熟量产 | 2026 全年随 GB200/GB300 出货，2027 让位但仍高量 | GB300 需求延续至 2027H1 | 2026H2-2027H1 供应持续短缺，NVSwitch 溢价维持 |
| NVLink 6 | full production，2026H2 partner availability | 2026H2 小批，2027 主力 | 2026Q4 明显收入化，2027 快速接棒 GB300 | Rubin ramp 接近 Blackwell，2027 成为高端 AI rack 默认 |
| Quantum-X800 InfiniBand | 800G 产品化 | 2026-2027 在 NVIDIA 训练集群保持增长，份额被 Ethernet 稀释 | Blackwell/Rubin 大训练需求强，绝对收入继续扩张 | CPO Quantum-X 加速落地，InfiniBand 高端份额稳住 |
| Spectrum-X / Spectrum-6 Ethernet | 800G 放量，102.4T/CPO 路线明确 | 2026 放量，2027 1.6T/CPO 增速加快 | 成为 neocloud 和云厂新增 NVIDIA cluster 默认 scale-out | NVIDIA 在 Ethernet DC share 从 15% 级继续上行 |
| Broadcom Tomahawk 6 / Ultra / Jericho 4 | TH6 已量产，Ultra/Jericho 进入 AI 方案 | 2026 随 Meta/OpenAI/ASIC early rack 增长，2027 放大 | 2027 成为非 NVIDIA AI fabric 主导 silicon | scale-up Ethernet 被证明可替代部分 NVLink/IB 高端场景 |
| UALink 1.0/2.0 | 1.0 已公开，2.0 2026Q2 | 2026 IP/测试/样机，2027 first-gen switch/rack | 2027 被 AMD Helios/部分 hyperscaler ASIC 大量采用 | 2027 形成 $10B+ 直接产品市场，成为采购清单项 |
| UEC Ethernet 1.0/1.1 | 1.0/1.0.2 发布，interop 推进 | 2026 产品验证，2027 进入更多 AI fabric | 2027 成为多厂商 AI Ethernet 的事实规范 | 与 UALink/ESUN 共同压缩 InfiniBand 份额 |
| CPO/CPX/NPO/OCI | 多厂商样品/早期客户 | 2026 pilot，2027 高端 switch 小规模 | 2027 socketed CPO/CPX 被多个 AI cluster 采用 | 2027 高端 AI switch 默认 CPO/CPX，ELS/optical engine 供不应求 |
| 3.2T/400G-per-lane | DSP/EML/PIC 样品 | 2026 样品，2027 live demo/qual，2028 规模 | 2027H2 小批收入 | 2027 形成数十亿美元早期市场 |

### 4.2 2026 最可能的技术路径

1. **NVIDIA 新增 GPU rack：** NVLink 5/6 scale-up + Quantum-X800 InfiniBand 或 Spectrum-X Ethernet scale-out。基准情景中，InfiniBand 用于最高端训练和 supercomputer，Spectrum-X 用于 hyperscaler/cloud AI Ethernet。
2. **非 NVIDIA custom ASIC rack：** Broadcom Ethernet scale-up/out + PCIe/CXL/retimer/optics，典型客户是 Meta MTIA 和 OpenAI custom accelerator。
3. **AMD Helios/开放 rack：** 2026H2 以 UALoE/UALink early 方案出现，2027 才明显放量。
4. **自研云厂内部 fabric：** AWS NeuronLink/EFA、Google TPU ICI/OCS、Microsoft Maia/Azure fabric 继续扩张，对外部供应链映射在交换芯片、光模块、光交换、DPU/NIC、测试。

## 5. 已开始放量的关键产品：市场规模、渗透率和利润率

说明：下表把“产品市场规模”定义为相应产品或方案的年度化收入/订单池，不等同公司收入。渗透率为该产品在对应 AI back-end/scale-up 细分中的采用率估算。

### 5.1 市场规模与渗透率路径

| 已放量产品/细分 | 2026 当前状态 | 未来 3 个月市场规模 | 未来 1 年市场规模 | 未来 2 年市场规模 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| NVIDIA NVLink 5/NVSwitch rack fabric | GB200/GB300 NVL72 主力 | 基准 $5-8B；乐观 $8-12B；极乐观 $12-16B | 基准 $22-35B；乐观 $35-50B；极乐观 $50-70B | 基准 $30-50B；乐观 $55-80B；极乐观 $80-110B | NVIDIA rack-scale GPU 内部 attach 接近 100%；全球高端 AI rack scale-up 价值占比 45-60% |
| NVIDIA Quantum-X800 InfiniBand + ConnectX | 800G 高端训练/AI supercomputer | $4-7B / $6-9B / $8-12B | $18-30B / $26-42B / $38-58B | $24-40B / $38-65B / $55-85B | NVIDIA 大训练集群中 40-60%，全 AI back-end switch 份额 20-35% 但绝对额增长 |
| NVIDIA Spectrum-X/Spectrum-6 Ethernet | AI Ethernet scale-out，高速增长 | $3-6B / $5-8B / $8-11B | $18-32B / $30-48B / $45-65B | $40-70B / $65-105B / $95-145B | NVIDIA AI Ethernet data center switch share 已到 15% 级；2027 高速端口份额继续上行 |
| Broadcom Tomahawk/Jericho/Thor/Agera AI Ethernet silicon | TH6 volume shipping，Meta/OpenAI 拉动 | $4-8B / $7-11B / $10-15B | $22-40B / $36-60B / $55-85B | $50-90B / $85-135B / $125-190B | Merchant/specialized AI Ethernet silicon 在非 NVIDIA fabric 中 50-75%；scale-up Ethernet 2027 加速 |
| 800G AI Ethernet/IB switch systems | 800G 已成为 AI back-end 主流 | $8-14B / $12-18B / $16-24B | $38-60B / $55-85B / $80-120B | $45-75B / $70-110B / $95-150B | 800G 2026 为主流，2027 被 1.6T 稀释但仍大出货 |
| 1.6T pluggable optics for AI fabric | 2026 放量前夜，>500 万只年出货预期 | $2-4B / $3-6B / $5-8B | $9-16B / $15-28B / $25-40B | $22-40B / $40-70B / $70-110B | 2026 高端新增集群 10-20%；2027 新增 AI fabric 25-45%；极乐观 50%+ |
| DAC/AEC/LACC/高速铜缆与连接器 | Rack 内/短距继续刚需 | $2-4B / $3-5B / $4-7B | $10-18B / $15-25B / $22-35B | $16-30B / $25-45B / $40-65B | Rack 内短距 attach 70%+，但中长距逐步被光替代；AEC/retimer attach 上升 |
| NIC/DPU/SuperNIC | ConnectX、BlueField、Thor Ultra、Pensando、Marvell | $4-7B / $6-10B / $9-14B | $22-38B / $35-55B / $50-78B | $45-75B / $70-110B / $105-160B | 高端 AI server attach 近 100%；DPU/SmartNIC attach 从 35-55% 向 60-80% |

### 5.2 增长和毛利率预测

| 产品 | 基准增长 | 乐观增长 | 极度超预期增长 | 当前/未来毛利率判断 |
|---|---:|---:|---:|---|
| NVLink/NVSwitch rack fabric | 未来一年 +35-55%，两年 CAGR +25-40% | +60-85% | +100%+ | NVIDIA 系统级毛利参考 71-75%；NVLink 作为专有附加价值，估计 70-85%，极度短缺时更高。 |
| Quantum-X800 InfiniBand | +25-45% | +50-70% | +90% | Switch/NIC silicon 和系统综合 55-75%；高端训练客户愿付性能保险溢价。 |
| Spectrum-X Ethernet | +55-85% | +90-130% | +160%+ | NVIDIA Ethernet 高端 mix 毛利 60-75%；CPO/软件 attach 后上行。 |
| Broadcom AI Ethernet silicon | +60-90% | +100-140% | +180%+ | Switch/NIC/retimer/DSP silicon 60-75%；公司 adjusted EBITDA 高 60% 级说明议价强。 |
| 800G switch systems | +40-60% | +70-90% | +110% | Box 25-45%；使用自有 silicon/软件/客户认证的 Arista/NVIDIA/Cisco/HPE 更高。 |
| 1.6T optics | +80-120% | +150-220% | +300% | 早期高端模块 35-45%，上游 EML/SiPh/laser/DSP 可 45-65%；2027 多供后 ASP 压力。 |
| 高速铜缆/AEC/连接器 | +35-55% | +60-85% | +120% | 普通 DAC/connector 25-40%，AEC/retimer/高密连接 40-65%。 |
| NIC/DPU/SuperNIC | +45-70% | +80-110% | +150% | NIC/SuperNIC 55-70%，DPU/软件安全/存储 offload 可 60-75%。 |

## 6. 在研和快速增长产品：市场规模、渗透率和毛利率

### 6.1 产品路线与市场规模

| 在研/快速增长技术 | 2026 当前状态 | 未来 3 个月 | 未来 1 年 | 未来 2 年 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| UALink switch/IP/management/chiplet | 1.0 公开，2.0 计划 Q2，商业 early | $100-300M / $250-600M / $500M-1.2B | $1-3B / $3-7B / $7-14B | $6-15B / $15-35B / $35-70B | 2026 <5%；2027 在开放 XPU/AMD Helios 中 10-25%；极乐观 30%+ |
| UALoE / Ethernet scale-up rack | AMD Helios/Celestica/HPE 生态推进 | $200-600M / $500M-1.5B / $1-3B | $2-6B / $6-14B / $14-28B | $12-30B / $30-65B / $65-120B | 2027 开放 GPU/XPU rack 中 15-35%；极乐观成非 NVIDIA 默认 |
| NVLink Fusion | NVIDIA 半定制开放，AWS Trainium4/Marvell 等生态 | $200-500M / $500M-1B / $1-2B | $2-5B / $5-12B / $12-25B | $10-25B / $25-55B / $55-100B | Custom ASIC 接入 NVIDIA rack 的桥；2027 从少数客户扩大 |
| Spectrum-6/Quantum-X CPO switch | Spectrum-6 102.4T CPO，Quantum CPO 方向 | $100-400M / $300-900M / $800M-2B | $1-4B / $4-10B / $10-22B | $8-20B / $20-45B / $45-85B | 2026 pilot，2027 高端 switch 5-15%，极乐观 25%+ |
| Broadcom TH6-Davisson CPO / NPO | TH6-Davisson sampling，third-gen CPO | $100-300M / $300-800M / $800M-1.8B | $1-3B / $3-8B / $8-18B | $7-18B / $18-40B / $40-75B | 高端 AI Ethernet switch 中逐步替代部分 pluggable |
| OCI optical compute interconnect | MSA 成立，协议无关 optical scale-up | <$100M / $100-300M / $300-800M | $300M-1B / $1-3B / $3-8B | $2-8B / $8-25B / $25-60B | 2026 标准/样机，2027 pilot，2028 后规模化 |
| CPX/XPO 12.8T liquid-cooled pluggable | Arista XPO MSA，多家演示 | <$100M / $100-300M / $300-600M | $300M-1B / $1-4B / $4-10B | $3-10B / $10-25B / $25-50B | 作为 CPO 之外高密 pluggable 路线，2027 高端导入 |
| OCS optical circuit switching | Google Apollo 体系化采用讨论 | $100-300M / $300-800M / $800M-1.5B | $1-3B / $3-7B / $7-15B | $5-15B / $15-35B / $35-70B | TPU-like cluster 先行；GPU Ethernet fabric 若采用则放大 |
| 3.2T/400G-lane optics/DSP | Broadcom Taurus、OpenLight/Coherent 样品 | <$200M / $200-500M / $500M-1B | $0.5-2B / $2-6B / $6-12B | $8-20B / $20-45B / $45-85B | 2027 仍早期；2028 才更主流 |
| Fabric management / observability / congestion software | UFM、Mission Control、EOS、SONiC、Apstra 等升级 | $300-800M / $600M-1.5B / $1-3B | $2-5B / $5-10B / $10-18B | $6-15B / $15-30B / $30-60B | 高端 AI fabric attach 从 30-50% 到 60-80%，软件毛利高 |

### 6.2 毛利率预测

| 在研/快速增长技术 | 基准毛利率 | 乐观毛利率 | 极度乐观毛利率 | 为什么能有溢价 |
|---|---:|---:|---:|---|
| UALink IP/switch silicon | 55-70% | 65-78% | 75-85% | 标准初期 IP/验证/互操作稀缺，客户避免 NVIDIA 锁定愿意付设计导入费。 |
| UALoE rack system | 25-45% | 35-55% | 45-65% | 系统集成毛利较低，但低延迟验证、液冷 rack、fabric tuning 可溢价。 |
| NVLink Fusion | 65-80% | 75-85% | 80-90% | 本质是 NVIDIA 把专有 scale-up 收费边界扩到第三方 XPU。 |
| CPO/CPX optical engine/ELS | 35-55% | 50-70% | 65-80% | 早期良率和可靠性难，ELS 冗余、封装、测试、客户认证形成壁垒。 |
| Broadcom CPO/NPO switch silicon | 60-75% | 70-80% | 75-85% | TH6/Tomahawk/Jericho 生态、SerDes、DSP、optics 全栈掌控。 |
| OCI optical scale-up | 35-60% | 55-75% | 70-85% | 标准初期，optical PHY、connector、WDM、测试工具短缺。 |
| OCS | 35-50% | 45-60% | 60-75% | 如果从 Google 扩散到更多 AI fabric，MEMS/控制软件/运维集成变稀缺。 |
| 3.2T optics/DSP | 40-60% | 55-70% | 65-80% | 400G/lane 器件、DSP、测试和良率是少数厂商能力。 |
| Fabric 软件 | 70-85% | 80-90% | 85-95% | 软件直接影响 GPU 利用率，客户切换成本和运维依赖高。 |

## 7. 供给侧：产能结构、瓶颈、成本与毛利

### 7.1 产能结构

| 环节 | 主要地区 | 主要公司/资产 | 关键工艺/能力 |
|---|---|---|---|
| InfiniBand/NVLink/Spectrum silicon | 美国、以色列、台湾代工 | NVIDIA/Mellanox、TSMC、封测 OSAT | 先进 switch ASIC、NVSwitch、ConnectX/BlueField、224G SerDes、CoWoS/高阶封装 |
| Ethernet switch/NIC/retimer silicon | 美国、台湾、新加坡/马来西亚封测 | Broadcom、Marvell、Cisco Silicon One、AMD Pensando、Astera、Credo、MACOM、MaxLinear | 102.4T switch、200G/400G lane DSP、PCIe Gen6、retimer/AEC |
| 交换机系统/白盒 | 台湾、美国、墨西哥、泰国、东欧 | Arista、Cisco、HPE/Juniper、Celestica、Accton/Edgecore、Quanta、Wiwynn、Foxconn、Dell、Supermicro | 高密交换机主板、散热、液冷、SONiC/EOS/NOS 集成、客户 burn-in |
| 光模块/光器件 | 中国、泰国、马来西亚、美国、日本、台湾 | Coherent、Lumentum、Fabrinet、Innolight/中际旭创、Eoptolink/新易盛、AOI、光迅科技、华工科技、天孚通信、海信宽带、Marvell、Broadcom optics | 800G/1.6T OSFP/QSFP、EML/VCSEL/SiPh、DSP、TRO/LPO/LRO、CPO optical engine |
| 铜缆/连接器/AEC | 中国、台湾、美国、墨西哥、越南 | Amphenol、TE、Molex、Samtec、Luxshare、BizLink、Credo、Astera、Spectra7、Semtech、MACOM | DAC/AEC/LACC、high-density connector、224G channel、retimer/linear equalization |
| 测试认证 | 美国、日本、欧洲、中国 | Keysight、VIAVI、Spirent、Anritsu、Tektronix、Teradyne、Advantest | 800G/1.6T/3.2T、LLR/CBFC、SerDes eye、FEC、interop、thermal/reliability |
| 软件/fabric management | 美国、以色列、欧洲 | NVIDIA UFM/DOCA/Mission Control、Arista EOS、Cisco、Juniper Apstra、SONiC 社区、HPE Slingshot、Cornelis | 拥塞控制、telemetry、job-aware routing、collective library、fault isolation |

### 7.2 至少 10 个供给瓶颈

1. **224G/448G SerDes 设计与良率。** 102.4T/204.8T switch 和 1.6T/3.2T optics 都依赖超高良率高速 I/O，任何 jitter/BER 问题都会拖慢客户认证。
2. **高阶 switch ASIC 封装和基板。** 大 die switch、CPO、多 chiplet/optical engine 对 ABF、substrate warpage、供电和散热要求极高。
3. **CPO optical engine 与 ELS。** Laser source、field replaceable ELSFP、耦合、热漂移和冗余机制决定 CPO 能否从 demo 走到量产。
4. **1.6T 光模块关键器件。** 200G/400G EML/EAM/MZM、SiPh PIC、InP laser/PD、isolator/filter、DSP 仍是短缺点。
5. **铜缆和连接器 SI/热管理。** NVLink copper spine、LACC、DAC/AEC 的布线、插拔、弯折半径、散热和现场维护限制 rack 设计。
6. **UEC/UALink/ESUN 互操作认证。** 标准有了不等于可采购，客户需要跨 switch、NIC、accelerator、cable、NOS、framework 的完整 compliance。
7. **Fabric debug 人才。** 大规模训练失败可能由单个 flap、tail latency、PFC storm、ECN 配置、collective imbalance 引发，排障人才稀缺。
8. **DPU/NIC firmware 与安全认证。** SuperNIC/DPU 需要和 hypervisor、container、storage、RDMA、PTP、安全策略深度耦合。
9. **液冷交换机/光模块热设计。** 高端 switch 和 XPO/CPO 都在突破传统风冷面板密度，冷板、泵、快接、漏液检测成为网络设备的一部分。
10. **长交期测试设备。** 1.6T MAC/FEC、224G SerDes、LLR/CBFC、CPO optical test 需要高端仪器，测试时间本身会成为产能。
11. **客户集中导致产能锁定。** NVIDIA、Meta、OpenAI、Google、AWS、Microsoft 可以预定产能，二线 neocloud 或企业客户拿货成本上升。
12. **地缘和出口管制。** 中国 AI 集群需求强，但高端 switch ASIC、NIC、DPU、HBM、光器件和EDA/IP可得性受限，国产替代难度高。

### 7.3 成本结构与价格传导

| 产品 | BOM/单位成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| NVLink/NVSwitch tray | NVSwitch ASIC 35-50%，高速 PCB/连接器/铜缆 20-30%，散热/电源 10-20%，测试/软件 10-20%。 | 是否随 GPU rack 打包、NVLink domain 大小、软件/collective 效率、缺货程度。 | 不是按单独端口定价，而是嵌入 NVL72 rack ASP，以 GPU 利用率和系统性能转嫁。 |
| InfiniBand switch/NIC | Switch ASIC/NIC ASIC 35-50%，光/铜端口 20-35%，系统板/电源/风扇 10-20%，UFM/软件/支持 5-15%。 | 端口速率、SHARP、拥塞控制、认证拓扑、NVIDIA GPU 绑定。 | 高端训练客户按 job completion time 和 uptime 支付溢价。 |
| Ethernet AI switch | Merchant switch ASIC 25-45%，optics/cages/connectors 25-40%，system/thermal 15-25%，NOS/支持 5-15%。 | 102.4T/204.8T silicon、radix、latency、PFC/ECN/UEC、CPO。 | Hyperscaler 用多供应商压价，但高端 silicon 和认证软件仍能溢价。 |
| SuperNIC/DPU | ASIC 30-45%，SerDes/PHY/PCB 15-25%，DRAM/flash 10-20%，software/security/offload 15-30%。 | RDMA 性能、storage/KV offload、安全、DOCA/SDK、firmware 可靠性。 | 随 AI server attach；DPU 能提升 GPU 利用率和安全隔离则可独立定价。 |
| 1.6T 光模块 | DSP/driver/TIA 25-40%，laser/modulator/PD/PIC 25-40%，封装/光学件 10-20%，测试 10-20%。 | DSP vs LPO/TRO、EML/SiPh 良率、温度、客户认证、短缺程度。 | 2026 短缺可涨价，2027 多供后 ASP 下行，价值向器件/DSP/测试集中。 |
| DAC/AEC/LACC | 铜线/连接器 30-50%，retimer/linear EQ 0-40%，组装 10-20%，测试 10-20%。 | 距离、速率、热、插拔可靠性、是否需要 retimer。 | 与 rack design 绑定，认证后切换成本高；普通 DAC 更易价格竞争。 |
| CPO/CPX/ELS | Switch ASIC/光引擎 40-60%，ELS/laser 10-20%，封装/连接器/散热 15-25%，测试/服务 10-20%。 | 光引擎良率、现场可维护、ELS 冗余、link stability、客户 field data。 | 用节能、可靠性、端口密度换溢价；若标准化多供，毛利回落。 |

## 8. 竞争格局与壁垒

### 8.1 市场结构

| 细分 | 头部集中度 | 主要公司 | 判断 |
|---|---|---|---|
| InfiniBand AI fabric | 极高，NVIDIA/Mellanox 近乎唯一高端供应 | NVIDIA | 绝对高壁垒，但 TAM 被 Ethernet 分流。 |
| NVLink/NVSwitch | 极高，NVIDIA 独占 | NVIDIA | 和 GPU、CUDA、MGX rack 绑定，最强定价权。 |
| AI Ethernet switch silicon | 高，Broadcom 第一梯队，NVIDIA/Cisco/Marvell 等竞争 | Broadcom、NVIDIA、Cisco、Marvell | 高端 102.4T/204.8T silicon 壁垒强，客户也希望多供。 |
| Ethernet switch systems | 中高，Arista/Cisco/NVIDIA/HPE/Celestica/Accton | Arista、Cisco、NVIDIA、HPE/Juniper、Celestica、Accton | 软件/NOS 和客户关系决定毛利，白盒竞争会压价格。 |
| 800G/1.6T 光模块 | 中，头部集中但多厂商竞争 | Coherent、Lumentum、Innolight、Eoptolink、AOI、Fabrinet 等 | 需求强但 ASP 下行风险高，上游器件更稳。 |
| UALink/开放 scale-up | 早期，格局未定 | AMD、Broadcom、Astera、Synopsys、Cisco、Intel、HPE、Meta、Microsoft、Google、AWS 等 | 2027 以后可能出现新 oligopoly。 |
| 高速铜/AEC/retimer | 中，连接器和芯片分层 | Amphenol、TE、Molex、Samtec、Credo、Astera、MACOM | 连接器规模壁垒 + retimer 芯片壁垒并存。 |

### 8.2 壁垒清单：为什么能定价

| 壁垒 | 具体解释 | 定价逻辑 |
|---|---|---|
| 协议和 collective offload | SHARP、NVLink all-to-all、UEC/UALink INC、RDMA congestion control 直接影响训练效率。 | 能把 GPU 利用率提高 1% 就对应数亿美元级客户价值。 |
| GPU/XPU 原生集成 | NVLink 与 NVIDIA GPU package/rack/软件深耦合；Broadcom XPU 与 Ethernet/PCIe/optics 协同设计。 | 客户买的是可工作的 rack，不是单个端口。 |
| 高速 SerDes 和 SI | 224G/448G PAM4 的 BER、jitter、loss budget、connector/backplane 都是硬门槛。 | 高速端口稀缺时，switch ASIC、retimer、测试工具有高毛利。 |
| 软件与可观测性 | UFM、DOCA、Mission Control、EOS、Apstra、SONiC tuning、job-aware routing。 | 大规模 AI fabric 的故障成本极高，运维软件可形成持续收入。 |
| 客户认证 | Hyperscaler 一个 fabric 认证周期通常跨 silicon、box、cable、NOS、framework、facility。 | 认证后切换成本高，供应商可维持 multi-year 价格。 |
| 规模与供给锁定 | NVIDIA/Broadcom/头部模块厂能提前锁 TSMC、封测、光器件、连接器产能。 | 二线客户需要为交期付溢价。 |
| 生态锁定 | CUDA/NCCL/NVLink/UFM 与 ROCm/UALink/UEC、Google/AWS internal stack 互不完全兼容。 | 性能和开发生态锁定比硬件价差更重要。 |
| 现场可靠性 | Link flap、thermal drift、connector failure、PFC storm 直接导致训练中断。 | 高可靠设备和支持服务可按 uptime 定价。 |

### 8.3 长期高 ROIC/高毛利层

长期最可能拥有高 ROIC 的层级：

1. **NVIDIA proprietary rack-scale fabric。** NVLink/NVSwitch/Quantum/Spectrum/ConnectX/BlueField/Mission Control 与 GPU 销售打包，客户很难拆分采购。
2. **Broadcom 类 AI fabric silicon 平台。** Tomahawk/Jericho/Thor/Agera/Sian/PCIe/optics + XPU 定制，把非 NVIDIA ASIC 生态的关键 I/O 抓在手里。
3. **高端 SerDes/DSP/retimer/IP。** 224G/448G 和 1.6T/3.2T 需要长期研发积累，客户认证强，毛利可高。
4. **CPO/ELS/optical engine。** 如果可维护性跑通，能从模块价格竞争中上移到封装和光引擎控制点。
5. **Fabric 管理软件与诊断工具。** 毛利最高，但需要依附硬件 installed base。

毛利较容易被压缩的层级：

- 普通白盒交换机 assembly。
- 标准 DAC/低端铜缆。
- 多供应商充分后的 800G/1.6T 通用光模块。
- 无软件/认证能力的单一硬件 OEM。

## 9. 2026 关键变化：3 个最可能拐点

### 拐点 1：Ethernet 反超从 scale-out 延伸到 scale-up

2025-2026 的核心变化不是“Ethernet 比 InfiniBand 便宜”，而是 Broadcom TH6/Ultra、UALink、UEC、ESUN/OCI 等把 Ethernet 或 Ethernet-like 技术推向 accelerator pod 内部。基准情景下，2026 仍是 NVLink 主导 scale-up，但非 NVIDIA ASIC 新增 rack 会更倾向 Ethernet scale-up。

最可能放量子方向：Broadcom Tomahawk/Jericho/Thor、UEC Ethernet、800G switch、1.6T optics、AEC/retimer。

### 拐点 2：Vera Rubin 让 NVLink 6 和 CPO 进入新一代 AI rack 采购

Rubin 2026H2 partner availability 将把 NVLink 6、ConnectX-9、BlueField-4、Spectrum-6/CPO 放进同一 rack/POD 产品。2026 不是 Rubin 大量收入年，但会决定 2027 供应链谁进入 reference design。

最可能放量子方向：NVSwitch 6、ConnectX-9、BlueField-4、Spectrum-6/SPX、CPO/ELS、液冷高密交换机。

### 拐点 3：开放标准进入产品化和合规验证

UALink 1.0、2.0、UEC 1.0/1.0.2 的意义在于从“paper spec”进入 IP、switch silicon、test、compliance、reference rack。2026 年直接收入小，但设计导入决定 2027-2028 份额。

最可能放量子方向：UALink IP、switch silicon、测试设备、fabric management、AMD Helios/Celestica/HPE 生态。

## 10. 2027 关键变化：3 个最可能拐点

### 拐点 1：1.6T 成为新增 AI fabric 主流，800G 开始价格竞争

2027 年新增 AI rack 若继续高速增长，1.6T 会从 high-end option 变成主流采购项。800G 仍大出货，但 ASP 与毛利压力上升。

最可能放量子方向：1.6T OSFP、200G/400G EML/SiPh、switch ASIC 200G lane、coherent campus DCI。

### 拐点 2：UALink/UALoE 与 Broadcom Ethernet scale-up 开始规模化

AMD Helios、Meta MTIA、OpenAI/Broadcom、其他 XPU 订单若按计划推进，2027 会出现第一批真正大规模非 NVIDIA scale-up fabric。它不一定打败 NVLink，但会改变采购基准。

最可能放量子方向：UALink switch/IP、Broadcom Ethernet scale-up、PCIe Gen6/CXL、retimer/AEC、fabric compliance。

### 拐点 3：CPO/CPX/XPO 从 pilot 走向高端 switch 量产

如果 2026 的 CPO/ELS 可靠性验证顺利，2027 高端 102.4T/204.8T switch 会将 CPO、CPX、NPO、XPO 作为节能和密度工具。若进展慢，pluggable 继续主流，但 XPO 会延长可插拔路线寿命。

最可能放量子方向：CPO optical engine、ELSFP laser、high-density connector、liquid-cooled pluggable、CPO test。

## 11. 头部公司清单

### 11.1 全栈与专有互联平台

| 方向 | 头部公司 |
|---|---|
| NVIDIA proprietary fabric | NVIDIA/Mellanox：NVLink/NVSwitch、Quantum InfiniBand、Spectrum-X、ConnectX、BlueField、LinkX、UFM/DOCA/Mission Control。 |
| Broadcom custom XPU + Ethernet | Broadcom：XPU、Tomahawk、Jericho、Thor、Agera、Sian DSP、CPO、PCIe switch/retimer。 |
| AMD open rack | AMD：Infinity Fabric、Pensando/Vulcano NIC、Helios、MI400/MI455X、UALink/UEC 生态。 |
| Google TPU fabric | Google：TPU ICI、Apollo OCS、Jupiter/Aquila 类数据中心网络、TPU pod。 |
| AWS fabric | AWS/Annapurna：NeuronLink、NeuronSwitch、EFA、Trainium/Inferentia。 |
| Microsoft Azure fabric | Microsoft：Maia/Cobalt/Azure 内部 AI fabric。 |
| Meta MTIA fabric | Meta + Broadcom：MTIA、Open Rack Wide、Ethernet scale-up/out/across。 |
| OpenAI custom accelerator | OpenAI + Broadcom：10GW custom accelerator/network systems。 |
| 中国超节点 | Huawei、Cambricon、Alibaba T-Head、Baidu Kunlunxin、Biren、Moore Threads、Enflame、Iluvatar、MetaX。 |

### 11.2 Switch/NIC/DPU/Retimer/SerDes/IP

| 细分 | 公司 |
|---|---|
| Switch ASIC | NVIDIA, Broadcom, Cisco Silicon One, Marvell, Intel, HPE/Juniper, Huawei, Innovium legacy/Marvell。 |
| NIC/SuperNIC/DPU | NVIDIA ConnectX/BlueField, Broadcom Thor/NetXtreme, Marvell, AMD Pensando, Intel Ethernet/IPU, Cisco, Napatech, Xilinx/AMD Alveo legacy。 |
| PCIe/CXL/Retimer/AEC | Astera Labs, Broadcom, Credo, Parade, Montage/LXT, Microchip, Diodes, Semtech, MACOM, Spectra7。 |
| SerDes/IP/EDA | Synopsys, Cadence, Alphawave Semi, Rambus, Marvell, Broadcom, MediaTek, GUC, Alchip。 |
| UALink/UEC/标准生态 | AMD, Apple, AWS, Cisco, Google, HPE, Intel, Meta, Microsoft, Synopsys, Alibaba, Astera Labs, Broadcom, Arista, NVIDIA, Dell, Lenovo 等。 |

### 11.3 交换机系统、OEM/ODM、NOS

| 细分 | 公司 |
|---|---|
| 高端品牌交换机 | Arista, Cisco, NVIDIA, HPE/Juniper, Dell, Huawei, Nokia, Ciena。 |
| 白盒/ODM/系统集成 | Celestica, Accton/Edgecore, Quanta, Wiwynn, Foxconn, Inventec, Wistron, Pegatron, QCT, Supermicro, Lenovo, Jabil, Flex。 |
| NOS/fabric 软件 | Arista EOS, NVIDIA UFM/DOCA/Mission Control, Cisco NX-OS/SONiC, Juniper Apstra, SONiC community, HPE Slingshot, Cornelis Omni-Path, Broadcom SDK。 |

### 11.4 光互联、CPO、硅光、激光器

| 细分 | 公司 |
|---|---|
| 光模块/收发器 | Coherent, Lumentum, Fabrinet, Innolight/中际旭创, Eoptolink/新易盛, Applied Optoelectronics, Accelink/光迅科技, 华工科技, Hisense Broadband, Source Photonics, Linktel/联特科技, Cambridge Industries, HG Genuine。 |
| 光芯片/激光器/器件 | Coherent, Lumentum, Broadcom, Marvell, Cisco/Acacia, MACOM, Semtech, MaxLinear, OpenLight, Ayar Labs, Ranovus, Celestial AI, Avicena, Lightmatter, POET, 天孚通信, 仕佳光子。 |
| CPO/CPX/NPO/OCI | NVIDIA, Broadcom, Coherent, Lumentum, Marvell, Ciena, Molex, Samtec, TeraHop, OpenLight, Ayar Labs, Ranovus, Celestial AI。 |
| Coherent/scale-across | Ciena, Nokia, Cisco/Acacia, Marvell, Infinera/Nokia, Lumentum, Coherent, Fujitsu。 |
| OCS/光交换 | Google Apollo ecosystem, Calient, Polatis/HUBER+SUHNER, Coherent, MEMS/optical switch suppliers, Ciena/Nokia line systems。 |

### 11.5 铜互联、连接器、线缆和热管理

| 细分 | 公司 |
|---|---|
| 连接器/高速线缆 | Amphenol, TE Connectivity, Molex, Samtec, Luxshare, BizLink, Foxconn Interconnect, JAE, Hirose, Rosenberger。 |
| DAC/AEC/LACC 芯片 | Credo, Astera Labs, Broadcom, MACOM, Semtech, Spectra7, Parade, MaxLinear。 |
| 高密光纤管理 | Corning, Senko, US Conec, AFL, CommScope, Panduit, Legrand, nVent。 |
| 液冷网络设备配套 | Vertiv, CoolIT, Boyd, Delta, Auras, Schneider, Eaton, nVent, Modine。 |

### 11.6 测试、认证与生产设备

| 细分 | 公司 |
|---|---|
| 高速网络测试 | Keysight, VIAVI, Spirent, Anritsu, Tektronix, EXFO。 |
| 半导体/封装测试 | Advantest, Teradyne, FormFactor, Chroma, Cohu, MPI。 |
| 光电测试/生产 | Coherent, Keysight, VIAVI, Luna, Santec, Yokogawa, Newport/MKS。 |
| 合规/互操作 | UALink Consortium, UEC, Ethernet Alliance, OCP, OIF, IEEE, PCI-SIG。 |

## 12. 投资排序与跟踪指标

### 12.1 未来 12 个月最确定

1. **NVIDIA networking stack：** NVLink/NVSwitch、Quantum-X800、Spectrum-X、ConnectX/BlueField，受益于 GB300 和 Rubin。
2. **Broadcom AI fabric silicon：** Tomahawk 6/Ultra、Jericho、Thor、Agera、Sian DSP、PCIe/retimer，受益于 Meta/OpenAI/custom XPU。
3. **1.6T 光模块与上游器件：** 2026 导入、2027 放量，器件/DSP/测试优于普通组装。
4. **高速铜/AEC/连接器：** rack 内 density 提升，NVL72/Helios/Trainium3 都需要更复杂铜互联。
5. **测试认证：** UEC/UALink/CPO/3.2T 的复杂度放大测试设备和服务价值。

### 12.2 未来 12-24 个月赔率最高

1. **UALink/UALoE switch/IP。** 小基数，若 AMD Helios 和非 NVIDIA XPU 规模化，弹性很大。
2. **CPO/CPX/NPO/OCI。** 若 field service 和 ELS 可靠性跑通，会从 pilot 变成高端 switch 默认选项。
3. **OCS/光交换。** 若从 Google TPU 扩散到通用 AI fabric，会重写部分电交换价值分配。
4. **Fabric software。** GPU 利用率和故障隔离直接影响 token revenue，软件价值会从“免费工具”变为 SLA 工具。

### 12.3 关键跟踪指标

- NVIDIA networking revenue 是否继续高于 Data Center compute 增速。
- Quantum-X800 与 Spectrum-X 在新建集群中的 mix。
- Broadcom Tomahawk 6/Ultra/Jericho 设计赢单数量，以及 Meta/OpenAI 项目实际 rack 出货。
- UALink 2.0 规范和合规计划是否按 2026Q2/Q3 落地。
- AMD Helios/Celestica/HPE 是否在 2026H2 交付 early customer rack。
- 1.6T 光模块出货是否从 2026 的 >500 万只走向 2027 的 1,500-2,500 万只。
- CPO/CPX/XPO 是否有真实 field deployment 和故障率数据。
- Ethernet AI back-end switch sales 是否继续超过 InfiniBand 两倍以上。
- OpenAI/Meta/Google/AWS/Microsoft capex 是否继续上修，以及是否前置 2027 需求。

## 13. 主要来源

| 来源 | 关键信息 |
|---|---|
| [NVIDIA Quantum-X800 InfiniBand Platform](https://www.nvidia.com/en-us/networking/products/infiniband/quantum-x800/) | 800G InfiniBand、144 ports、ConnectX SuperNIC、SHARP v4、CPO 方向。 |
| [NVIDIA NVLink and NVLink Switch](https://www.nvidia.com/en-us/data-center/nvlink/) | NVLink 6 每 GPU 3.6TB/s、NVL72 260TB/s、NVLink Fusion。 |
| [NVIDIA Vera Rubin Opens Agentic AI Frontier](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx) | 七类芯片 full production、NVL72、LPX、STX、SPX、DSX、2026H2 供货。 |
| [NVIDIA Vera Rubin POD 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) | 40 racks、1,152 GPUs、60 exaflops、10PB/s scale-up、MGX copper spines、Spectrum-6 102.4T CPO。 |
| [NVIDIA NVLink Fusion](https://www.nvidia.com/en-us/data-center/nvlink-fusion/) | 第三方 CPU/XPU 接入 NVLink rack-scale architecture，72 XPUs all-to-all。 |
| [NVIDIA FY2026 Q4 CFO Commentary](https://s201.q4cdn.com/141608511/files/doc_financials/2026/Q426/Q4FY26-CFO-Commentary.pdf) | Q4 networking $11.0B、FY2026 networking $31.4B、毛利率与收入。 |
| [Broadcom OFC 2026 AI infrastructure release](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai) | 3.5D XPU、102.4T CPO、400G/lane DSP、Thor Ultra、Agera、PCIe Gen6、OCI MSA。 |
| [Broadcom Tomahawk 6 production volume](https://investors.broadcom.com/news-releases/news-release-details/broadcom-now-shipping-worlds-first-1024-tbps-switch-production) | 102.4T switch production、512 XPU single-hop scale-up、128K XPU two-tier scale-out。 |
| [Broadcom TH6-Davisson CPO](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-tomahawkr-6-davisson-industrys-first-1024) | 第三代 CPO、102.4Tbps、70% optical interconnect power reduction、512 XPU scale-up。 |
| [Broadcom-Meta MTIA partnership](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-extended-partnership-meta-deploy-technology) | Meta >1GW 首期、多 GW rollout、Ethernet scale-up/out/across。 |
| [OpenAI-Broadcom 10GW collaboration](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-announce-strategic-collaboration-deploy-10) | OpenAI 自研 accelerator + Broadcom Ethernet，2026H2 起部署，2029 完成。 |
| [UALink 200G 1.0 Specification PR](https://ualinkconsortium.org/wp-content/uploads/2025/04/UALink-1.0-Specification-PR_FINAL.pdf) | 200G per lane、1,024 accelerators/pod、93% effective peak bandwidth、成员和董事会。 |
| [UALink roadmap 2026](https://ualinkconsortium.org/blog/ualink-roadmap-insights-accelerating-open-scalable-ai-networking-1296/) | 2.0 计划 2026Q2、INC、management/chiplet spec、3.0 目标 2027。 |
| [Ultra Ethernet Consortium 1.0](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/) | UEC 1.0 specification、AI/HPC Ethernet stack、compliance/interop。 |
| [Ultra Ethernet Consortium FAQ](https://ultraethernet.org/) | UEC 目标、AI scale-out network、Ethernet interoperability。 |
| [Dell'Oro AI back-end switch forecast](https://www.prnewswire.com/news-releases/ai-back-end-switch-market-will-push-past-100-billion-by-2030-according-to-delloro-group-302678344.html) | AI back-end switch 2030 >$100B、Ethernet 预计在 scale-up/out 主导、800G/1.6T/3.2T。 |
| [Dell'Oro 2Q25 InfiniBand/Ethernet](https://www.prnewswire.com/news-releases/infiniband-switch-sales-surged-in-2q-2025-while-ethernet-maintains-market-lead-in-ai-back-end-networks-according-to-delloro-group-302546136.html) | InfiniBand 2Q25 增长但 Ethernet 领先，Celestica/NVIDIA/Arista 领先 Ethernet segment。 |
| [IDC Ethernet switch market 4Q25](https://www.idc.com/resource-center/blog/ethernet-switch-market-size-and-growth-datacenter-segment-surges-60-in-q4-as-ai-workloads-expand/) | 2025 Ethernet switch $55.1B、data center $32.5B、NVIDIA data center Ethernet share 15.2%。 |
| [AMD-Celestica Helios](https://www.amd.com/en/newsroom/press-releases/2026-3-16-amd-and-celestica-announce-collaboration-to-a.html) | Helios scale-up switch 使用 UALoE，Celestica R&D/design/manufacturing。 |
| [AMD Helios OCP Open Rack](https://ir.amd.com/news-events/press-releases/detail/1261/amd-showcases-helios-rack-scale-platform-built-on-the-open-compute-project-open-rack-for-ai-introduced-by-meta) | Helios 使用 OCP、UALink、UEC，AMD Instinct/EPYC/Pensando。 |
| [HPE AMD Helios](https://www.hpe.com/us/en/newsroom/press-release/2025/12/hpe-accelerates-ai-deployments-with-first-amd-helios-ai-rack-scale-architecture-with-open-scale-up-networking-built-with-broadcom.html) | HPE 2026 提供 AMD Helios，open scale-up Ethernet networking with Broadcom。 |
| [OFC 2026 本地报告](../conference_update/ofc_2026_conference_update.md) | 1.6T、3.2T、CPO、XPO、coherent、OCS 和市场估算。 |
| [NVIDIA GTC 2026 本地报告](../conference_update/nvidia_gtc_2026_research.md) | Rubin、NVLink、Spectrum-X、LPX、STX、DSX 与财务/市场口径。 |
| [AI 芯片路线图本地报告](../ai_chip_research_2026_2027.md) | 2026-2027 头部 AI 芯片与平台的出货/技术路径背景。 |
| [Xcelerated Compute Show 2026 本地报告](../conference_update/xcelerated_compute_show_2026_report.md) | 开放互联、UEC/UALink、AI backend networking、memory wall、neocloud 信号。 |

## 14. 读数注意事项

1. 本报告把 NVLink/NVSwitch 等随 rack 出货的互联价值拆出估算，但现实收入中大量价值会被计入 NVIDIA GPU/rack 系统 ASP。
2. Broadcom 的 AI revenue 同时包含 custom XPU、networking、PCIe、optics 等，不应和本报告所有子项简单相加。
3. InfiniBand 和 Ethernet 的份额取决于口径：端口数、switch revenue、AI back-end switch revenue、完整 fabric revenue 可能给出不同结论。
4. 未来 3 个月数字偏订单/出货 run-rate；未来 1 年和 2 年数字是本报告在乐观 AI 基建假设下的市场池预测，不是保证收入。
5. 本报告有意采用偏乐观 AI 基建情景：假设 2026-2027 agentic inference、长上下文、多模态、主权 AI 和自研 ASIC 均继续推高算力需求。
