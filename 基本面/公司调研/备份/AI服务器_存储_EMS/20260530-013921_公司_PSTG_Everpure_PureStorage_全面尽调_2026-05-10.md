# 公司：PSTG/P - Everpure（原 Pure Storage）全面尽调

> 截至日期：2026-05-10（美国市场最近一个完整交易日为 2026-05-08）。  
> 口径：美元；公司 fiscal year 以 1 月底/2 月初结束，FY2026 截至 2026-02-01。  
> 重要说明：Pure Storage 在 2026 年更名为 Everpure。公司 2026-02-23 公告称 2026-03-05 起以 Everpure 名义交易且当时仍保留 `PSTG`；后续行情页和交易所资料显示新 ticker 使用 `P`。本报告沿用用户给定 `PSTG`，并在行情处列示 `P`。

## 0. 高浓度结论

1. **这不是传统企业存储股的旧故事，而是“全闪存平台 + 订阅化 + hyperscaler DirectFlash 授权 + AI 数据平台”的再定价故事。** FY2026 收入 $3.663B、同比 +15.6%；Q4 FY2026 首次单季超过 $1B，收入 $1.059B、同比 +20.4%。订阅服务收入 FY2026 $1.691B、占收入 46.2%，ARR $1.9B，RPO $3.7B、同比 +40%。
2. **最强边际变化是 hyperscaler。** 公司 Q4 电话会明确：hyperscaler 收入不进 RPO、以 product revenue 确认；FY2027 多数 hyperscaler 收入预计在 Q3/Q4；新模式下 hyperscaler 自行采购 NAND，Everpure 采购部分非 NAND 组件，hyperscaler 收入毛利预计 **75%-85%**，高于普通 product gross margin。
3. **AI 产品线已经从“认证/样机”进入“可卖产品”。** FlashBlade//EXA 在 Q4 FY2026 已拿到第一批销售；2026-03 又推出 Evergreen//One for FlashBlade//EXA 与 Data Stream beta。官方资料称 FlashBlade//EXA 单命名空间 read performance 可达 10+ TB/s，并披露 1-10 chassis、每 chassis 10 blades、每 blade 1-4 个 37.5TB DFM、16×400GbE uplinks 的规格。
4. **估值贵，但财务质量强。** 最近可得行情：`P` 2026-05-08 工具报价 $78.16；StockAnalysis 2026-05-07 口径 market cap $25.13B、TTM P/E 135.3x、forward P/E 32.2x。用 FY2026 收入 $3.663B 计算，P/S 约 6.9x-7.4x（取决于市值口径）。FY2026 GAAP gross margin 70.4%、net margin 5.1%、free cash flow $616M，现金和有价证券 $1.55B、无流动债务。
5. **核心风险不是需求，而是 NAND/组件供给、hyperscaler 项目节奏和 AI 存储价值捕获口径。** 公司已提示 NAND、memory、CPU 等组件价格快速上涨，可能导致长交期和 shipment delays；但同一供需失衡也迫使 hyperscaler 加速验证新供应源，对 Everpure 是双刃剑。

## 1. 公司整体业务、资本市场认知与产业链位置

### 1.1 公司做什么

Everpure/Pure Storage 是全闪存企业级数据存储与数据管理平台厂商。核心不是自制 NAND，而是用自研 DirectFlash Module、Purity 操作环境、Pure Fusion/Pure1 控制面、FlashArray/FlashBlade 硬件平台和 Evergreen 订阅服务，把企业的 block/file/object、云原生、AI/HPC、备份恢复、Kubernetes 数据服务统一起来。

| 层级 | 产品/能力 | 主要用途 | 投资含义 |
|---|---|---|---|
| 存储系统 | FlashArray//X、//C、//E、//XL、//ST | 数据库、虚拟化、VMware 替代、性能/容量/归档层 | FY2026 product revenue $1.972B 的主体，毛利 67.0% GAAP |
| AI/HPC 文件/对象 | FlashBlade//S、FlashBlade//EXA | 训练数据湖、checkpoint、RAG、GPU direct、HPC/AI 并行文件 | EXA 是 AI 叙事核心，当前收入小但增速高 |
| 订阅/消费模式 | Evergreen//One、Evergreen//Flex、Evergreen//Forever | Storage-as-a-Service、容量/性能 SLA、无中断升级 | FY2026 subscription services $1.691B，ARR $1.9B |
| 云原生 | Portworx、KubeVirt/Red Hat OpenShift Virtualization | Kubernetes 持久化、容器/VM 数据管理 | 高毛利软件，推动平台化 |
| 控制面/数据平台 | Pure Fusion、Pure1、Enterprise Data Cloud、1touch | 跨 on-prem/cloud/edge 的数据治理、分类、AI-ready context | 从“管存储”升级到“管数据”的战略焦点 |
| Hyperscaler 授权 | DirectFlash/软件+硬件 IP | 用 flash 替代部分 hyperscale HDD/SSD 环境 | FY2027 最关键的非线性收入源，毛利 75%-85% 预期 |

### 1.2 投资人心中的公司画像

过去 Pure Storage 在投资人眼中是 **“高毛利、全闪存、份额持续提升但仍受企业 IT 周期影响的存储硬件+订阅服务公司”**。2025-2026 年叙事发生三层变化：

1. **从硬件供应商变成平台商。** 2025 Pure Accelerate 推出 Enterprise Data Cloud，目标是把分散存储池抽象为统一数据云；FY2026 财报强调 Fusion、Purity、Pure1 统一控制面。
2. **从企业客户扩展到 hyperscaler。** 传统存储厂商很难进入 hyperscaler 自研存储堆栈；Pure 的 DirectFlash 技术被定位为能在 hyperscale 场景用 flash 挑战 disk 的空间/功耗/TCO。
3. **从“AI 受益概念”变成“AI 数据路径产品”。** FlashBlade//EXA、NVIDIA-Certified Storage、Evergreen//One for AI、Data Stream、1touch 都围绕 AI 数据准备、训练/推理吞吐、RAG、数据治理和上下文管理。

### 1.3 最近 3 年重大业务变化、转型和收购

| 时间 | 事件 | 影响 |
|---|---|---|
| 2020 | 收购 Portworx，交易额约 $370M | 进入 Kubernetes/cloud-native 数据服务，补软件栈 |
| 2024-2025 | DirectFlash hyperscaler design win、150TB DFM 路线、hyperscale 替代 disk 叙事 | 打开传统企业存储之外的超大客户市场 |
| 2025-03 | FlashBlade 集成 NVIDIA AI Data Platform；获 NVIDIA HPS/NVCS 相关认证 | 进入 NVIDIA AI factory reference architecture 采购语言 |
| 2025-06/09 | Enterprise Data Cloud、FlashArray//ST、FlashBlade//S 更新，Pure//Accelerate 强化平台战略 | 产品线从单阵列升级为统一数据云 |
| 2026-02 | Pure Storage 宣布更名 Everpure，并拟收购 1touch | 从 storage 品牌转为 data intelligence/data management 品牌；1touch 提供数据发现、分类、治理、DSPM 和 AI context |
| 2026-03 | Evergreen//One for FlashBlade//EXA、Data Stream beta | AI 项目从 pilot 到 production 的消费模式和数据管道 |

### 1.4 产业链位置

Everpure 不在 NAND wafer 或 SSD controller 的最上游，也不是服务器 OEM。它位于 **“AI/企业数据平台系统层”**：上游采购 NAND/DRAM/CPU/NIC/电源/机箱/代工，下游卖给企业、政府、neocloud、hyperscaler。其价值捕获来自三点：软件/控制面、数据迁移与运营锁定、以及 DirectFlash 对容量/功耗/TCO 的系统优化。

在 AI 基建技术栈中，它不是 GPU/HBM 那种必选件，但在以下场景成为高优先级：训练 checkpoint、RAG/embedding、长上下文推理的数据准备、KV/cache warm tier、GPU 利用率提升、数据治理/安全合规。

## 2. 最新股价、估值和资产负债表健康度

### 2.1 股价与估值

| 指标 | 最新数据 | 日期/口径 | 备注 |
|---|---:|---|---|
| 股价 | $78.16 | 2026-05-08，finance 工具，`P` | 周末无交易，属最近交易日 |
| 市值 | $25.1B-$27.0B | 2026-05-07/05-08，多数据源 | 股数约 330.46M，供应商口径略有差异 |
| TTM P/E | 约 135x-142x | 2026-05-07/05-08，按 FY26 EPS $0.55 近似 | finance 工具给出 PE 200x，可能使用不同 TTM EPS |
| Forward P/E | 32.2x-32.9x | StockAnalysis 2026-05-07 | 以 sell-side forward EPS 估算 |
| P/S | 约 6.9x-7.4x | 市值 / FY2026 revenue $3.663B | 若用 $25.13B 为 6.86x；用 $27.0B 为 7.37x |
| 收入增速 | FY2026 +15.6%；Q4 +20.4% | FY2026/Q4 FY2026 | Q4 增速明显加速 |
| GAAP 毛利率 | FY2026 70.4%；Q4 69.9% | 公司财报 | 非 GAAP FY2026 72.1% |
| GAAP 净利率 | FY2026 5.1%；Q4 9.5% | 净利 $188.2M / 收入 $3.663B | SBC 仍压低 GAAP 净利 |
| FCF margin | FY2026 16.8% | FCF $616M / 收入 $3.663B | 现金转化强 |

### 2.2 财务健康度

| 指标 | FY2026 末 | 判断 |
|---|---:|---|
| 现金+有价证券 | $1.547B | 现金充足 |
| 总资产 | $4.674B | 轻资产平台型硬件公司 |
| 总负债 | $3.229B | 主要为递延收入和经营负债 |
| 股东权益 | $1.446B | 正权益，累计赤字缩小至 $1.181B |
| 流动资产 | $3.063B | 现金、A/R、预付增加 |
| 流动负债 | $1.910B | current deferred revenue $1.181B |
| 流动比率 | 1.60x | 健康 |
| 债务 | 流动债务 0；FY2025 末有 $100M current debt | 资本结构低杠杆 |
| FY2026 operating cash flow | $880M | 强 |
| FY2026 FCF | $616M | 强 |
| FY2026 回购 | $343M | 有资本回报能力 |

资产负债表总体健康。最需要盯的不是偿债，而是 **A/R、库存、组件预付款和供应链承诺**：Q4 FY2026 A/R $944.8M、库存 $75.9M，均较 FY2025 末上升；这与 Q4 大单、hyperscaler/enterprise 项目确认和组件供给紧张有关。公司 10-K 风险因素也提示，hyperscaler 若降低需求，公司可能承担 NAND flash purchase commitments；不过 Q4 电话会又表示 FY2027 hyperscaler 模式中 hyperscaler 自行采购 NAND，这会降低 Everpure 对 NAND 库存风险的暴露。

## 3. 最新及最近四次财报：五个季度高密度表

> 注：公司不直接披露 backlog/bookings/cancel rate、AI 数据中心收入占比。本表将 RPO 作为服务合同 backlog，TCV sales 作为 Storage-as-a-Service bookings，hyperscaler shipment/revenue 用管理层披露和毛利变化推断。

| 财报季度 | 收入与增速 | 收入结构 | 毛利/利润 | ARR/RPO/Bookings | 订单、交期、取消率推断 | AI/hyperscaler 信息 |
|---|---:|---|---|---|---|---|
| Q4 FY2026，end 2026-02-01 | $1,058.9M，+20.4% YoY | Product $618.5M，+25.0%；Subscription $440.4M，+14.4% | GAAP GM 69.9%；non-GAAP GM 71.4%；non-GAAP OI $225.7M，margin 21.3%；GAAP net income $100.3M | ARR $1.9B，+16%；RPO $3.7B，+40%；Storage-as-a-Service TCV $179M，+28%；FY26 TCV $520M，+32% | RPO sequential +约 $0.8B，但管理层称 hyperscaler 不计入 RPO；组件短缺可能拉长 lead time；取消率未披露，RPO增长显示服务端取消压力低 | FlashBlade//EXA first sales；hyperscaler FY26 超预期；FY27 hyperscaler 多数收入 Q3/Q4，毛利 75%-85% 预期 |
| Q3 FY2026，end 2025-11-02 | $964.5M，+16% | Product 约 $534.8M，+18%；Subscription $429.7M，+14% | GAAP GM 72.3%；non-GAAP GM 74.1%；Product non-GAAP GM 72.9%；non-GAAP OI $196.2M，margin 20.3% | ARR $1.8B，+17%；RPO $2.9B，+24%；Storage-as-a-Service TCV $120M，+25% | 产品收入和毛利受 hyperscaler royalty/Portworx term license 正面拉动；交期未披露 | Q3 YTD hyperscaler shipments 已超过全年 1-2EB/2EB 初始预测，Q4 继续出货 |
| Q2 FY2026，end 2025-08-03 | $861.0M，+13% | Product $446.3M，+10.9%；Subscription $414.7M，+14.8% | GAAP GM 70.2%；non-GAAP GM 72.1%；Product non-GAAP GM 68.0%；non-GAAP OI $130.0M，margin 15.1% | ARR $1.8B，+18%；RPO $2.8B，+22%；Storage-as-a-Service TCV +24% | 上调 FY26 指引；TCV 和 RPO 说明订阅订单稳定；未披露取消率 | EDC 架构发布，FlashArray//XL、FlashArray//ST、FlashBlade//S 扩展；hyperscale/AI 被列入前瞻重点 |
| Q1 FY2026，end 2025-05-04 | $778.5M，+12% | Product 约 $372.2M，+约7%；Subscription $406.3M，+17% | GAAP GM 68.9%；non-GAAP GM 70.9%；Product non-GAAP GM 64.0%；non-GAAP OI $82.7M，margin 10.6% | ARR $1.7B，+18%；RPO $2.7B，+17%；Storage-as-a-Service TCV +70% | Q1 通常季节性较弱但现金流强；TCV 高增说明消费模式订单动能好 | FlashBlade//EXA 发布/推进；Portworx Enterprise 3.3；获得 NVIDIA Foundation/Enterprise 相关认证 |
| Q4 FY2025，end 2025-02-02 | $879.8M，+11.4% | Product $494.8M，+7.4%；Subscription $385.1M，+17.1% | GAAP GM 67.5%；non-GAAP GM 69.2%；Product non-GAAP GM 62.9%；non-GAAP OI $153.1M，margin 17.4% | ARR $1.7B，+21%；RPO $2.6B，+14% | FY2025 基准：产品毛利较低，hyperscaler 尚未明显贡献 | hyperscale/AI 仍主要是机会叙事，后续 FY26 开始兑现 |

### 3.1 最新指引

Q4 FY2026 给出的 FY2027 指引：

| 指引项 | Q1 FY2027 | FY2027 |
|---|---:|---:|
| 收入 | $990M-$1.01B | $4.3B-$4.4B |
| 收入同比增速 | +27% 至 +30% | +17% 至 +20% |
| Non-GAAP operating income | $125M-$135M | $780M-$820M |
| 隐含 non-GAAP OI margin | 约 12.6%-13.4% | 约 18.1%-18.6% |

管理层同时提示：FY2027 hyperscaler 收入不线性，多数在 Q3/Q4；行业会遇到 NAND、memory、CPU 价格上涨和组件短缺；2026-02-09 公司已对产品线涨价，Q1 product gross margin（不含 hyperscaler）可能在典型 65%-70% 区间低端，但全年会恢复。

## 4. 业务收入占比、产品线和重点/跳过项

### 4.1 FY2026 业务占比

| 业务 | FY2026 收入 | 占比 | 增速 | GAAP 毛利 | 判断 |
|---|---:|---:|---:|---:|---|
| Product | $1.972B | 53.8% | +16.0% | 67.0% | FlashArray/FlashBlade/DirectFlash/hyperscaler/部分 Portworx term license；FY27 弹性最大 |
| Subscription services | $1.691B | 46.2% | +15.2% | 74.4% | Evergreen、support、消费订阅；收入可见度强 |
| 合计 | $3.663B | 100% | +15.6% | 70.4% | 典型高毛利硬件+软件混合模型 |

### 4.2 产品对应关系

| 业务/产品 | 对应型号/模块 | AI 重要性 | 当前收入可见度 |
|---|---|---:|---|
| FlashArray | //X、//C、//E、//XL、//ST；DirectFlash Modules | 中-高：企业数据库、虚拟化、AI 数据准备和高性能 block | 高；Product revenue 主体 |
| FlashBlade//S | S200/S500 等 | 高：企业 AI、RAG、文件/对象、NVIDIA 认证 | 中高；已成熟出货 |
| FlashBlade//EXA | EXA metadata/data 架构，37.5TB DFM，400GbE fabric | 极高：AI/HPC、GPU 利用率、checkpoint/RAG/并行文件 | 早期；Q4 FY26 first sales |
| Evergreen//One | for block/file/object；2026 扩展到 FlashBlade//EXA | 高：消费模式降低 AI 项目 capex 和容量规划风险 | 高；FY26 TCV $520M |
| Portworx | Enterprise 3.3、KubeVirt、OpenShift Virtualization | 中高：K8s/VM 数据持久化、云原生 AI 平台 | 中；不单独披露 |
| Enterprise Data Cloud/Fusion/Pure1 | 统一数据平面和控制面 | 高：把数据从孤岛变成 AI-ready operational data | 主要拉动硬件和订阅，不单独披露 |
| Data Stream beta | 2026 later beta | 高潜力：自动数据管道从 ingest 到 inference | 期权；暂无收入 |
| 1touch | 数据发现、分类、治理、DSPM、数据主权/context | 高潜力：让数据 self-describing、AI-ready | 预计 Q2 FY27 关闭；FY27 对 OI 约 1.5% 稀释 |
| Hyperscaler DirectFlash/IP | DirectFlash 硬件/软件授权，NAND 由客户供应链采购 | 极高：flash 替代 hyperscale disk/SSD 层，省空间/电力 | FY27 关键弹性；不进 RPO |

### 4.3 可跳过的低增速/非核心业务

- 传统 support renewal 中非扩容部分：现金流好，但不是 AI 弹性来源。
- 普通 SMB/商业客户存储替换：稳定但增速低于 hyperscaler/AI。
- 非 AI 的 Cloud Block Store/迁云项目：有战略价值，但不是未来 12 个月最大弹性。
- 纯备份/归档低性能容量层：FlashArray//E 有 TCO 价值，但若不绑定 AI 数据湖和高密度机房，估值弹性弱。
- 非 AI 的政府/教育周期项目：可贡献收入，但订单节奏受预算周期影响。

## 5. 高增长/关键产品当前贡献与 AI 基建评分

> 评分 1-5：5 = 极强。收入贡献为估算时明确标注，不代表公司披露。

| 关键产品/业务 | FY2026 当前收入贡献 | 收入增速 | AI 技术栈重要性 | 时间紧急性 | 供需紧张 | 垄断/溢价能力 | 依据 |
|---|---:|---:|---:|---:|---:|---:|---|
| Hyperscaler DirectFlash/IP | 估算 $100M-$200M，约 3%-5% 收入；公司未披露 | >100%，低基数 | 5 | 5 | 5 | 4 | Q3 YTD shipments 超过 1-2EB/2EB 初始目标；FY27 收入 Q3/Q4 集中；GM 75%-85% |
| FlashBlade//EXA AI/HPC | 估算 FY26 <$50M-$100M；Q4 first sales | 新品，>100% | 5 | 4 | 4 | 4 | 10+TB/s、NVIDIA path、SPEC/MLPerf 叙事 |
| FlashBlade//S AI-ready/NVIDIA certified | 估算 $200M-$350M AI-adjacent；未披露 | +20%-40% | 4 | 4 | 3 | 3 | FlashBlade//S500 获 NVIDIA Foundation/Enterprise/NCP/DGX 相关认证 |
| Evergreen//One / Storage-as-a-Service | FY26 TCV bookings $520M，+32%；subscription revenue 总计 $1.691B | TCV +32% | 4 | 4 | 3 | 4 | 保证性能/容量、减少 AI 试点到生产的 capex 摩擦 |
| FlashArray//ST/DirectFlash enterprise | Product revenue 主体，估算 >$1.2B | +中双位数 | 3 | 3 | 4 | 3 | 全闪存替代、VMware/数据库/企业数据准备 |
| Portworx/Kubernetes | 估算 $100M-$200M；未披露 | +20%-40% | 3 | 3 | 2 | 3 | K8s、KubeVirt、OpenShift VM，云原生 AI 数据服务 |
| EDC/Fusion/1touch/Data Stream | FY26 直接收入小；主要拉动平台销售 | 新品/早期 | 4 | 4 | 2 | 3 | 数据治理、classification、AI context 是企业 AI 落地瓶颈 |

## 6. 一年后收入贡献三情景预测

| 产品/业务 | 基准：未来一年 | 乐观：未来一年 | 极度乐观：未来一年 |
|---|---|---|---|
| Hyperscaler DirectFlash/IP | FY27 $300M-$450M；占收入 7%-10%；增长 2-3x；重要性 5、紧急性 5、供需 4、溢价 4 | $500M-$750M；第二 hyperscaler 初始出货；占 11%-16%；供需 5 | $900M-$1.2B；多家 hyperscaler 加速 flash 替代 disk；占 18%-23%；溢价 5，但项目集中风险高 |
| FlashBlade//EXA | $150M-$250M；从 first sales 到 selected production；增长 2x+ | $300M-$500M；neocloud/enterprise AI 采购放量；NCP 认证推进 | $700M+；成为高端 AI/HPC storage 默认 shortlist，GPU idle 成本推动快速采购 |
| FlashBlade//S AI-ready | $280M-$450M AI-adjacent；NVIDIA-certified attach 提升 | $500M-$700M；企业 RAG/AI 工厂标准化 | $900M+；AI storage share 从 2%-3% 上修到 5%+，Pure 抢占份额 |
| Evergreen//One | FY27 TCV $650M-$750M；subscription revenue $1.9B-$2.05B | TCV $800M-$950M；EG1 for AI 拉动高性能 SLA | TCV $1.1B+；AI 客户偏好消费模式，RPO/ARR 再加速 |
| Portworx/EDC/1touch/Data Stream | $150M-$250M 直接/可识别软件收入；1touch 稀释 OI 约 1.5% | $250M-$400M；数据治理和 AI-ready context 变成 AI 项目预算项 | $500M+；Data Stream 与 1touch 嵌入企业数据平面，估值从硬件转软件 |
| Core FlashArray enterprise | Product total ex-hyperscaler $2.0B-$2.2B；价格抵消成本 | $2.3B-$2.5B；VMware 替代、全闪存替代 HDD 加速 | $2.7B+；NAND 成本可传导且客户为能耗/TCO 迁移 |

公司层面 FY2027 收入三情景：

| 情景 | FY2027 收入 | 同比 | Non-GAAP OI | 核心假设 |
|---|---:|---:|---:|---|
| 基准/公司指引 | $4.3B-$4.4B | +17%-20% | $780M-$820M | hyperscaler 后半财年确认；订阅稳定；组件成本逐步传导 |
| 乐观 | $4.55B-$4.75B | +24%-30% | $850M-$950M | EXA/EG1 for AI 超预期；产品涨价顺利；第二 hyperscaler 有贡献 |
| 极度乐观 | $5.0B-$5.3B | +37%-45% | $1.05B+ | hyperscaler flash 替代提前、多个 AI/neocloud 项目批量部署；供应链没有大延误 |

## 7. BOM、内容量、价格传导、产能与认证

### 7.1 FlashBlade//EXA：AI/HPC 关键产品

| 项目 | 内容 |
|---|---|
| 官方规格锚点 | 1-10 chassis；每 chassis 10 blades；每 blade 1-4 个 37.5TB DFM；2 个 XFM；16×400GbE uplinks；metadata chassis 5U、2600W nominal；每 XFM 1U、310W nominal |
| 容量 | 0.375PB-1.5PB raw/chassis；10 chassis 最高 3.75PB-15PB raw，取决于每 blade DFM 数 |
| 网络内容量 | 400GbE port 理论 50GB/s；16×400G = 6.4Tb/s = 800GB/s raw line rate；若 10 chassis 线性扩展为 160×400G，raw line rate 约 8TB/s |
| 性能 | 官方称单命名空间 read performance 10+TB/s；write speeds 可扩到 read 的 50%；SPEC AI_Image 可支持 6,300 simultaneous AI jobs；MLPerf 叙事称大型 NVIDIA Hopper 集群 GPU 利用率 >90% |
| 每 rack | 官方称 less than half rack 可支撑大规模 AI 性能；按 5U chassis + XFM 估算，容量/功耗随 chassis 数变化 |
| 每 MW | AI storage 一般占 IT power 2%-5%；每 1MW AI 负载可配 20-50kW 存储。按 3.2kW/EXA chassis+XFM 口径，约 6-15 个单元级配置，raw flash 约 9PB-22PB 上限；实际受网络/冗余/数据保护影响 |
| 每 GPU | 训练/RAG 热数据层常见 20-100TB effective/GPU；EXA 若按 512 GPU 集群，可对应约 10PB-50PB effective hot tier；若按 NVIDIA NCP 10,000 GPU 认证框架，单一 15PB raw 配置只是 1.5TB/GPU 的最低共享层，不代表生产最佳实践 |
| BOM 粗拆 | DFM/flash 35%-55%；CPU/metadata/controller/DRAM 10%-20%；NIC/XFM/switch/cabling 10%-25%；chassis/power/cooling 10%-20%；软件/支持 10%-25% |
| 毛利判断 | 系统毛利 55%-70%，若以 Evergreen//One SLA 与软件价值销售，综合毛利可更接近订阅服务的 75%+；早期项目有验证/服务成本 |
| 价格传导 | NAND/DRAM/NIC 涨价先压 product GM；但 AI 客户以 GPU idle time 评估 TCO，若 EXA 能减少 GPU 等待，可按系统价值定价 |
| 当前产能能力 | 不是晶圆产能，而是系统集成/DFM/NIC/供应链交付能力；FY2026 product revenue $1.97B，Q4 run-rate product revenue $2.47B，显示硬件交付能力可支持数十亿年化 |
| 采纳/认证 | FlashBlade//EXA 已在 NVIDIA certified storage list 中显示 Foundation；官方称路径指向 NCP 级别；FlashBlade//S500 已覆盖 Foundation/Enterprise/NCP/DGX SuperPOD 相关验证 |

### 7.2 Hyperscaler DirectFlash/IP

| 项目 | 内容 |
|---|---|
| 真实内容量 | 公司披露 Q3 FY2026 YTD hyperscaler shipments 已超过 1-2EB/2EB 初始预测；这是 exabyte 级交付，不是普通企业阵列规模 |
| BOM | Hyperscaler 自行采购 NAND；Everpure 提供 DirectFlash 相关硬件/软件/IP、部分非 NAND 组件、工程支持 |
| 每 TB 收入推断 | 公司未披露。若 FY26 hyperscaler revenue $100M-$200M、shipment 2EB+，隐含 $50/TB-$100/TB 以下量级；若只看 royalty 软件，则可能更低。该估算高度不确定 |
| 毛利 | 管理层给出 FY27 hyperscaler gross margin 75%-85% |
| 每 MW/rack | Hyperscale storage rack 通常按 PB/rack、W/TB、空间/TB 衡量；Pure 的卖点是用 flash 减少空间、功耗和冷却，而非每 GPU 固定 attach |
| 价格传导 | NAND 不由 Pure 承担，有利于毛利；非 NAND 组件涨价可通过产品价格/合同传导 |
| 当前产能 | FY26 已交付 2EB+；FY27 产能取决于 hyperscaler 数据中心 buildout schedule 和非 NAND 组件供应 |
| 认证阶段 | 已进入至少一个 hyperscaler 的生产/交付阶段；第二 hyperscaler 处于初始/早期信号，未量化 |

### 7.3 Evergreen//One / Storage-as-a-Service

| 项目 | 内容 |
|---|---|
| 内容量 | 不按固定硬件卖，而是按容量、性能和 SLA 消费；公司提供基础设施并保证 outcomes |
| FY26 bookings | Storage-as-a-Service TCV $520M，+32%；Q4 $179M，+28% |
| BOM | 底层 FlashArray/FlashBlade + 运维软件 + Pure1/Fusion + 支持服务 + 折旧/融资成本 |
| 毛利 | 订阅服务 GAAP GM FY26 74.4%，non-GAAP 76.6%；高于 product |
| 每 rack/MW | 客户不用先买满 rack；适合 AI 项目从 pilot 扩到 production，降低过度采购和容量误配 |
| 价格传导 | 通过 SLA/容量/性能等级续约和扩容传导；NAND 上涨滞后反映到新合同 |
| 采纳 | ARR $1.9B，RPO $3.7B，说明客户锁定和收入可见度强 |

### 7.4 Portworx / EDC / 1touch / Data Stream

| 项目 | 内容 |
|---|---|
| BOM | 主要是软件研发、云/支持、FAE；硬件 BOM 很低 |
| 毛利 | 成熟软件可达 75%-90%；1touch 目前未盈利，FY27 对 OI 预计 1.5% 稀释 |
| 每 GPU/rack | 不按物理单位销售；价值来自数据发现、分类、context、Kubernetes/VM 数据移动、AI pipeline |
| 采纳 | Portworx 已产品化；Data Stream 2026 later beta；1touch 预计 Q2 FY27 closing |
| 认证/生态 | Kubernetes、Red Hat/OpenShift、VM migration、data governance/DSPM；未来关键是与 NVIDIA/AI runtime/RAG 平台打通 |

## 8. 一年后产能与认证三情景

| 产品/业务 | 基准 | 乐观 | 极度乐观 |
|---|---|---|---|
| FlashBlade//EXA | FY27 可支持 $150M-$250M 收入；Foundation 认证转更多客户 PoC；NCP 路径推进 | $300M-$500M；NCP/Cloud Partner 参考架构推进，多 neocloud 采用 | $700M+；成为高端 AI storage shortlist，供应链主要约束在 NIC/DFM/集成 |
| Hyperscaler DirectFlash/IP | $300M-$450M 产能/收入能力；单一主客户为主；Q3/Q4 确认 | $500M-$750M；第二客户初步贡献；非 NAND 组件供应可控 | $900M-$1.2B；多客户 exabyte 级扩展，工程支持/供应链成为瓶颈 |
| Evergreen//One | TCV $650M-$750M；RPO 保持 20%+ 增长 | TCV $800M-$950M；AI SLA 和 EXA 消费模式加速 | TCV $1.1B+；大量企业绕过 capex，以 consumption 采购 AI data platform |
| EDC/1touch/Data Stream | 1touch 关闭后整合，FY27 小规模 revenue；OI 稀释 1.5% | 1touch 数据分类/治理嵌入 Pure1/Fusion，带动大单 | 成为 AI-ready data control plane，软件 attach 改变估值 |

## 9. 基于订单积压和供给的未来一年增速推断

### 9.1 真实 backlog / bookings 的可见部分

| 项目 | 数字 | 对未来一年含义 |
|---|---:|---|
| RPO | $3.7B，+40% YoY | 服务合同 backlog 强；但不含 hyperscaler product revenue |
| ARR | $1.9B，+16% YoY | 订阅收入 FY27 有高可见度 |
| Storage-as-a-Service TCV | FY26 $520M，+32% | Evergreen//One 扩张速度快于总收入 |
| Hyperscaler shipment | Q3 FY26 YTD 已超过 1-2EB/2EB 初始目标；Q4 继续 | FY27 product revenue 弹性来自数据中心建设 schedule，不体现在 RPO |
| >$5M 大单 | Q4 deals over $5M +80% YoY | enterprise strategic platform deal 增多 |
| 组件供给 | NAND/memory/CPU 价格上涨、短缺、可能 lead time 延长 | 短期 shipment delay 风险；中期价格传导和新供应源验证利好 |

### 9.2 增速推断

| 情景 | 未来一年收入增速 | 订单/供给解释 |
|---|---:|---|
| 基准 | +17%-20% | 公司指引；RPO 提供订阅底盘，hyperscaler 后半财年确认；供应链有扰动但不致命 |
| 乐观 | +24%-30% | RPO 高增长转收入，EXA/EG1 for AI 高于预期，产品涨价被接受；第二 hyperscaler 初步贡献 |
| 极度乐观 | +37%-45% | Hyperscaler exabyte 级 flash 替代提前，多家 AI/neocloud 采购 EXA；AI storage share 从当前低位上修 |

取消率：公司未披露。基于 RPO +40%、deferred revenue 上升、TCV +32%，订阅取消风险低；hyperscaler 侧取消/延迟风险中等，因为收入取决于客户数据中心建设节奏，且公司 10-K 提示单客户机会需要大量资源投入、存在需求下降风险。

## 10. 竞争格局、替代方案与切换成本

### 10.1 主要竞争对手

| 市场 | 竞争者 | Everpure 相对位置 |
|---|---|---|
| 企业全闪存阵列 | Dell PowerStore/PowerMax/PowerScale、NetApp AFF/AFX、HPE Alletra/GreenLake、IBM FlashSystem、Hitachi Vantara、Nutanix | Pure 在简单性、Evergreen、NPS、全闪存 TCO、订阅化上强；Dell/NetApp 在大客户覆盖和组合销售更强 |
| AI/HPC 文件/对象 | DDN AI400X、VAST Data、WEKA、IBM Storage Scale、Dell PowerScale、HPE ClusterStor、NetApp、MinIO/Cloudian | FlashBlade//EXA 性能和 NVIDIA 认证是新卖点；VAST/WEKA/DDN 在 AI-native/KV/context 叙事强 |
| Hyperscaler 存储 | Hyperscaler 自研系统、HDD/SSD 厂商、对象存储内部平台 | Pure 的机会是 DirectFlash/IP 嵌入客户自研体系，而不是卖传统阵列 |
| Kubernetes 数据服务 | Portworx、Red Hat OpenShift Data Foundation/Ceph、NetApp Trident/Astra、Dell/VMware、Longhorn 等 | Portworx 是强品牌，但开源和平台内置方案压价 |
| 数据治理/DSPM/AI-ready data | BigID、Varonis、Wiz/云安全、Rubrik/Commvault 数据安全、Snowflake/Databricks data governance | 1touch 带来语义/分类/context，但整合仍早期 |

### 10.2 新技术会是主流吗

- **全闪存替代部分 HDD：会成为高密度 AI 和 hyperscaler warm/hot tier 的主流之一，但不会全面替代 cold HDD。** AI 数据湖有读多写少、空间/能耗受限、交付确定性要求，高容量 QLC/DirectFlash 有优势；冷归档仍由 HDD/object storage 占优。
- **FlashBlade//EXA/AI parallel file：有机会成为企业/neo-cloud AI 的主流 shortlist，但竞争激烈。** DDN、VAST、WEKA 已经在 NVIDIA STX/CMX、KV/context memory 叙事中很活跃。
- **Enterprise Data Cloud：方向正确，但货币化需要时间。** 企业 AI 难点从模型转向数据准备、治理和实时 access；不过 Snowflake/Databricks/安全厂商/备份厂商都会争夺同一数据控制面。
- **Evergreen consumption：大概率继续成为主流采购方式之一。** AI 项目容量波动大，消费模式比一次性 capex 更适配，但融资/折旧和服务交付成本要被良好管理。

### 10.3 风险与替代

| 风险 | 影响 | 替代/缓释 |
|---|---|---|
| NAND/DRAM/CPU 继续涨价 | Product GM 短期承压、交期延长 | 涨价、Evergreen SLA 定价、hyperscaler 自采 NAND |
| Hyperscaler 项目非线性 | FY27 Q3/Q4 revenue 若延后，股价波动大 | RPO/ARR enterprise 底盘；多客户扩张 |
| AI storage attach 慢于预期 | EXA、Data Stream、1touch 估值叙事降温 | 传统 enterprise refresh 和 VMware 替代支撑 |
| 竞争者抢 NVIDIA/KV 生态 | VAST/WEKA/DDN 在 STX/CMX 中强势 | Pure 的优势是安装基数、Evergreen、FlashBlade//S500 认证和一体化 |
| 开源/云厂自研压价 | Portworx/EDC 软件定价受限 | 与硬件/SLA/数据治理打包，降低单点可替代性 |
| 数据迁移复杂 | 客户采用周期长 | Pure 的迁移工具、订阅模式和高 NPS 缓解 |

### 10.4 客户替换成本

存储是高切换成本资产。企业客户迁移 PB/EB 级数据、数据库、VM、Kubernetes volume、权限、备份链路和审计 lineage，需要长时间验证；AI 客户还要验证 GPU 利用率、checkpoint 恢复、RAG tail latency、metadata ops 和安全隔离。一旦 Everpure 进入客户的 data plane/control plane，替换成本高于普通服务器或 SSD 单品。

## 11. 投资跟踪清单

1. Q1 FY2027（预计 2026-05-27）是否继续确认 +27%-30% 收入增速，且 product GM 是否仅短期跌到 65%-70% 低端。
2. FY2027 Q3/Q4 hyperscaler 收入确认节奏、是否出现第二/第三 hyperscaler。
3. FlashBlade//EXA 是否从 first sales 变为可量化 backlog，是否获得更高 NVIDIA certification/NCP。
4. Storage-as-a-Service TCV 是否保持 25%-35% 增长，ARR 是否重新加速。
5. RPO 中 current/next-12-month recognition 比例；Q4 $3.7B 的增量能否转收入。
6. 1touch 是否按 Q2 FY27 关闭，整合后是否提高 EDC 软件 attach。
7. NAND/DRAM/CPU 成本和交期；公司涨价能否完整传导。
8. 与 VAST/WEKA/DDN/NetApp/Dell 在 NVIDIA AI storage 认证和 neocloud 客户中的 win/loss。

## 12. 主要信息源

- Everpure Q4 FY2026 earnings press release: https://s21.q4cdn.com/687136699/files/doc_financials/2026/q4/Everpure-Q4FY2026-Earnings-Press-Release.pdf
- Everpure Q4 FY2026 prepared remarks: https://s21.q4cdn.com/687136699/files/doc_financials/2026/q4/Q4FY26-Everpure-Prepared-Remarks.pdf
- Everpure FY2026 Form 10-K: https://www.sec.gov/Archives/edgar/data/1474432/000147443226000043/a10kfy2026.pdf
- Q3 FY2026 results: https://www.purestorage.com/content/dam/pdf/en/quarter-report/q3-2026.pdf
- Q2 FY2026 results: https://www.sec.gov/Archives/edgar/data/1474432/000147443225000038/pstg-ex991q2fy2026xpressre.htm
- Q1 FY2026 results: https://www.purestorage.com/content/dam/pdf/en/quarter-report/q1-2026.pdf
- Q4 FY2025 results: https://www.sec.gov/Archives/edgar/data/1474432/000162828025008136/pstg-ex991q4fy2025.htm
- Rebrand and 1touch announcement: https://investor.everpuredata.com/news-and-events/press-releases/press-release-details/2026/Pure-Storage-Becomes-Everpure-Announces-Intent-to-Acquire-1touch/default.aspx
- Evergreen//One for AI and Data Stream beta: https://www.everpuredata.com/company/newsroom/press-releases/everpure-simplifies-enterprise-ai-with-evergreen-one.html
- NVIDIA AI Data Platform / FlashBlade certification announcement: https://www.purestorage.com/company/newsroom/press-releases/pure-storage-integrates-nvidia-ai-data-platform-into-flashblade.html
- NVIDIA-Certified Storage systems list: https://docs.nvidia.com/certification-programs/certified-storage/latest/systems-list.html
- FlashBlade//EXA product/spec page: https://www.pure.ai/flashblade-exa.html
- StockAnalysis `P` statistics/valuation: https://stockanalysis.com/stocks/p/statistics/
- Everpure investor stock info: https://investor.everpuredata.com/stock-information/default.aspx
- 项目内行业资料（未读取 `公司调研` 目录）：`行业调研_AI服务器_存储_芯片/行业调研_AI-native存储与KV Cache基础设施_2026-05-08.md`、`行业调研_AI服务器_存储_芯片/行业调研_企业级SSD与高速存储控制器_2026-05-08.md`、`行业调研/AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`、`conference_update/xcelerated_compute_show_2026_report.md`

