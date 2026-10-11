# 行业调研：【宽带接入、PON、DOCSIS 4.0与Wi-Fi 7】

> 版本日期：2026-05-08  
> 研究口径：本报告聚焦固定宽带接入设备、PON、DOCSIS 4.0、家庭/企业 Wi-Fi 7、运营商网关与接入侧软件平台。美元区间主要为设备、软件、CPE、运营商采购订单或可归因收入池，不等同于运营商宽带服务总收入。  
> 投资假设：对 2026-2027 AI 计算中心建设、推理流量、AI PC/手机、企业 AI 应用和边缘 AI 采用极度乐观的上行情景；对没有直接披露的数据，采用“公开锚点 + 单位出货/ASP + 运营商节奏”的乐观推导。

## 0. 一句话结论

宽带接入不是 AI 数据中心硬件的最直接上游，但在 2026 会被三股力量同时推高：第一，AI 数据中心和云推理把骨干、城域、企业园区和边缘节点的流量基线抬高；第二，家庭与企业端的 AI PC、4K/8K 视频、实时协作、云游戏、视频生成和安全摄像头，使“上行、低时延、室内覆盖和稳定性”从可选卖点变成续约/留存工具；第三，运营商在 fiber overbuild、BEAD、DOCSIS 4.0、Wi-Fi 7 CPE 和托管 Wi-Fi 上开始重新进入资本开支周期。

最现实的 2026 主线是 **XGS-PON + Wi-Fi 7 + DOCSIS 3.1 high-split/DAA + Comcast 型 DOCSIS 4.0 FDX 扩围**。50G PON、25GS-PON、DOCSIS 4.0 ESD 大规模化、6GHz 标准功率 AFC、AI-native gateway 是 2027 预期差。极度超预期情景下，2027 年 50G PON 与 DOCSIS 4.0 会从“高端试点”变成“运营商防御 fiber overbuild 的战略采购”，Wi-Fi 7 则会成为新装家庭网关和企业 AP 的默认配置。

最值得跟踪的投资层级不是低毛利 CPE 组装，而是：**PON/DOCSIS/Wi-Fi 芯片与参考设计、25G/50G PON 光器件、DOCSIS 4.0 放大器/节点/RPD/vCMTS、云管 Wi-Fi/AIOps 平台、运营商深度认证网关、BEAD/FTTH 被动光网络材料和施工交付**。

## 1. 资料锚点与校验

| 公开锚点 | 数字/事实 | 对本报告的含义 |
|---|---:|---|
| Dell'Oro 2026-03 宽带接入报告 | 2025Q4 全球 broadband access equipment 收入 $4.8B，QoQ +7%、YoY +2%；报告覆盖 cable、DSL、PON 设备的收入、ASP、端口/单位出货。来源：[Dell'Oro/PRNewswire](https://www.prnewswire.com/news-releases/broadband-access-equipment-to-return-to-growth-in-2026-according-to-delloro-group-302709983.html) | 2026 接入设备从三年压制周期回到增长，全球年化设备池约 $18B-$21B，是 PON/DOCSIS 设备预测的总锚。 |
| Dell'Oro 2026 预测摘录 | 宽带接入设备 2025-2030 CAGR 约 0.3%，2028 收入峰值约 $18.8B；PON 设备 2025-2030 CAGR 约 1.9%；PON ONT 2025 全球出货 158M。来源：[Electronics Weekly](https://www.electronicsweekly.com/news/business/0-3-growth-2025-30-for-broadband-access-equipment-market-2026-01/)、[Advanced Television](https://www.advanced-television.com/2026/03/12/forecast-broadband-access-equipment-return-to-growth-in-2026/) | 总市场不是爆炸式，但结构性爆点在 XGS-PON、Wi-Fi 7、DOCSIS 4.0、FWA CPE 和高端网关。 |
| 美国 FTTH | 2025 年美国新增 FTTH passings 11.8M，总 passings 98.3M；2026 100% bonus depreciation 可能推动 FTTH CapEx +5%-15%。来源：[Fiber Broadband Association](https://fiberbroadband.org/2025/12/16/fiber-broadband-association-reports-historic-fiber-deployment-highs/) | 美国 fiber build 继续强，XGS-PON、ONT、光缆、分光器、施工和 Wi-Fi 7 网关受益。 |
| BEAD 进度 | 截至 2026-05-04，56 个州/地区已全部提交 Final Proposal，54 个获 NTIA 批准，52 个获 NIST 批准可用资金，50 个完成 award agreement。来源：[NTIA BEAD dashboard](https://www.ntia.gov/funding-programs/internet-all/broadband-equity-access-and-deployment-bead-program/progress-dashboard) | BEAD 从规划进入采购/施工，2026 H2 开始有订单，2027 放量更明显。 |
| CableLabs DOCSIS 2026 | 截至 2024-12，美国 cable HFC 住宅位置中 98% 可获得 1Gbps+ 下行；100Mbps+ 上行从约 1% 升到 32%，1Gbps+ 上行升到 9%；DOCSIS 4.0 已展示 10G-class 下行、3Gbps/5.5Gbps 上行，正在研究 3GHz 和 6GHz HFC 扩展。来源：[CableLabs](https://www.cablelabs.com/blog/docsis-technology-whats-changed-in-the-past-year-and-why-it-matters) | Cable 短期主线是 high-split、DAA、vCMTS、DOCSIS 3.1+，DOCSIS 4.0 是 2026-2027 高弹性增量。 |
| DOCSIS 4.0 互通 | 2026-03 CableLabs 第 16 次 DOCSIS 4.0 Interop·Labs 验证了多厂商安全、认证和加密机制，2026-05 继续互通测试。来源：[CableLabs](https://www.cablelabs.com/blog/authentication-and-privacy-docsis-4-0-interop-focuses-on-security) | 认证/互通仍是节奏阀门，但 D4.0 已从实验室速度转向部署可信度。 |
| Comcast/CommScope | Comcast 2023 推出全球首个 DOCSIS 4.0 商用；2024 已扩至 6 个市场、100 万+ homes；CommScope 2025 称下一代 unified FDX/ESD RPD、amps 支持 1.8GHz ESD 与 FDX。来源：[Comcast](https://corporate.comcast.com/press/releases/comcast-commscope-notch-milestone-next-generation-connectivity-millions-across-us)、[CommScope](https://commscopeholdingcompanyinc.gcs-web.com/news-releases/news-release-details/commscope-and-comcast-accelerate-rollout-docsis-40-amplifiers) | Comcast 是 D4.0 FDX 第一条实战曲线；FDX amps、nodes、RPD、网关是 2026 最明确 D4.0 订单。 |
| Charter | 2026Q1 Charter 有 29.6M Internet customers，Q1 CapEx $2.9B，FY2026 CapEx 预期约 $11.4B；10-K 称当前把频谱扩到 1.2GHz、high split 与 DAA，之后部署 DOCSIS 4.0 并扩至 1.8GHz。来源：[Charter Q1 2026](https://ir.charter.com/static-files/8f4715b9-1c59-4a03-8829-05e75fdbb368)、[Charter 10-K](https://www.sec.gov/Archives/edgar/data/0001091667/000109166726000017/chtr-20251231.htm) | Charter 2026 更像“D3.1 high-split + DAA 的大采购年”，D4.0 收入更偏 2027。 |
| Wi-Fi 7 | WBA 预计 Wi-Fi 7 AP 出货从 2024 年 26.3M、2025 年 66.5M 增至 2026 年 117.9M；WBA 调研中 38% 受访者计划 2026 部署 Wi-Fi 7，32% 计划 AI/Cognitive networks。来源：[WBA 2026 predictions](https://wballiance.com/wireless-broadband-alliance-reveals-its-wi-fi-predictions-for-2026-and-beyond/)、[WBA Industry Report](https://wballiance.com/wba-industry-report-2026-finds-62-of-survey-respondents-more-confident-to-invest-in-wi-fi-than-12-months-ago/) | Wi-Fi 7 是 2026 最确定的 CPE/AP 量产升级；AI AIOps 是软件毛利来源。 |
| Wi-Fi 7 企业 WLAN | IDC 4Q25 显示企业 WLAN 增长由 Wi-Fi 7 带动，全球企业 WLAN 支出 60% 已流向 Wi-Fi 6E/7。来源：[IDC](https://www.idc.com/resource-center/blog/worldwide-enterprise-wlan-grew-13-9-driven-by-wi-fi-7-deployments/) | 企业端 2026 是 Wi-Fi 7 ROI 验证年，AFC、6GHz、MLO、AIOps 决定溢价。 |
| Nokia PON | Nokia 50G/25G PON 可在现有 Lightspan MF / Quillion line card 上支持 GPON、XGS、25G、50G 和未来光模块；2026Q1 Fixed Networks 收入 -13%，但公司称转向高毛利产品。来源：[Nokia 50G PON](https://www.nokia.com/newsroom/nokia-unveils-worlds-first-50g-pon-solution-for-post-quantum-enterprise-connectivity/)、[Nokia Q1 2026](https://www.nokia.com/newsroom/nokia-corporation-interim-report-for-q1-2026/) | 25G/50G PON 不是完全替换 XGS-PON，而是在同一平台上卖高端端口、企业 SLA 和投资保护。 |
| 中国 50G PON | ZTE 与中国移动江苏 2025-06 推出 50G PON FMC 社区，三代五模 Combo，支持对称 50Gbps 和 50G FTTR。来源：[ZTE](https://www.zte.com.cn/global/about/news/china-mobile-and-zte-take-the-lead-in-launching-a-50G-PON-based-FMC-residential-community-in-China.html) | 中国会是 50G PON 初期最大示范市场，但 2026 仍以 10G/XGS 与 FTTR 为主。 |
| PON 互通 | Broadband Forum 2025 Plugfest 测试 50G PON、25GS-PON、XGS-PON，参加者包括 Airoha、Calix、Nokia、Sagemcom、Evolution Digital、Hitron、MT2。来源：[Broadband Forum](https://www.broadband-forum.org/news/record-vendor-turnout-powers-high-speed-fiber-device-compatibility/) | 25G/50G PON 生态已进入多厂商互通阶段，2026 是认证和小批部署窗口。 |
| Calix | 2025 全年收入 $1B、非 GAAP 毛利率 58%；2026Q1 收入 $280M、YoY +27%、非 GAAP 毛利率 57.2%。来源：[Calix Q4 2025](https://investor-relations.calix.com/sec-filings/all-sec-filings/content/0001406666-26-000004/ex992stockholderletter25q4.htm)、[Calix Q1 2026](https://www.stocktitan.net/sec-filings/CALX/8-k-calix-inc-reports-material-event-2c5a13d94a83.html) | 平台化/云管/托管 Wi-Fi 比纯硬件更能定价，区域宽带商升级周期恢复。 |
| Qualcomm Wi-Fi 7/Edge AI | Wi-Fi 7 平台支持 320MHz、4K QAM、MLO，平台容量最高 33Gbps；Networking Pro A7 Elite 把 Wi-Fi 7 与 edge AI 整合。来源：[Qualcomm Wi-Fi 7](https://www.qualcomm.com/wi-fi/wi-fi-7)、[Qualcomm A7 Elite](https://www.qualcomm.com/news/releases/2024/10/qualcomm-unveils-the-networking-pro-a7-elite-platform--the-first) | AI gateway 不是概念题，芯片平台已把 NPU/AIOps/网关融合成产品方向。 |
| Broadcom/Comcast DOCSIS AI chipset | Broadcom/Comcast 统一 DOCSIS 4.0 芯片支持 FDX、ESD 或两者同时运行，并在 node、amp、modem 中嵌入 AI/ML。来源：[Comcast/Broadcom](https://corporate.comcast.com/press/releases/comcast-broadcom-develop-ai-powered-access-network-pioneering-new-chipset) | D4.0 芯片的核心价值是统一 FDX/ESD 生态、降低库存碎片，并把 telemetry/AI 变成运营商网络能力。 |
| 内存成本 | TrendForce 预计 AI server 需求推动 2026Q2 DRAM/NAND 合约价继续上涨，2026 供应短缺明显，实质扩产要到 2027 年末或 2028。来源：[TrendForce](https://www.trendforce.com/presscenter/news/20260331-12995.html) | AI 数据中心会反向挤压路由器、网关、ONT 的 DRAM/NAND 成本，是 2026 CPE 毛利最大不确定性。 |

## 2. 2026 AI 计算中心建设下的机遇、挑战与技术路径

### 2.1 这个行业为什么会被 AI 拉动

1. **上行与低时延从小众需求变成留存工具。** AI 视频会议、云桌面、代码/设计协作、家庭安全摄像头、边缘 NAS、云备份和实时生成式应用都提高上行与低抖动需求。DOCSIS high-split、D4.0 FDX、XGS-PON、25G/50G PON 的共同卖点都是“更高上行 + 更低延迟 + 更高稳定性”。
2. **企业 AI 与 AI PC 让企业 WLAN 进入更新周期。** 2026 年 Wi-Fi 7 的价值不是理论峰值，而是 6GHz、MLO、QoS、AIOps、AP cloud telemetry、智能漫游和高密会议室/工厂/学校场景。
3. **AI 数据中心挤占城域光纤、施工、光器件和电力交付资源。** 这对接入行业既是机会也是挑战：有数据中心/企业园区资源的运营商会升级城域与接入，纯住宅 overbuild 项目则可能被光缆、施工和融资成本挤压。
4. **运营商 CPE 从“成本中心”变成“家庭入口”。** Qualcomm、Broadcom、Calix、Plume、Charter 等方向都指向一个现实：网关/AP 将承担安全、家宽体验、设备画像、AI AIOps、家庭边缘推理和移动融合。
5. **AI 带来存储/内存成本传导。** 高端网关需要更多 DRAM/NAND、10G/2.5G LAN、Wi-Fi 7 RF FEM 和更强 CPU/NPU。AI 数据中心抢内存会压缩低端 CPE 毛利，利好有价格传导能力和平台收入的厂商。

### 2.2 当前正在使用的主流技术

| 技术 | 2026 状态 | 典型用途 | 投资含义 |
|---|---|---|---|
| GPON / EPON | 存量巨大，新增主要在低 ARPU 和海外新建市场 | 1Gbps 以下/低成本 FTTH | 收入稳定但 ASP 低，替换周期会给低价 ONT 和兼容 OLT 带来量。 |
| XGS-PON / 10G EPON | 全球 FTTH 新建主力，北美、欧洲、中东、拉美继续扩张 | 1-10Gbps residential/SMB，BEAD，fiber overbuild | 2026 最确定 PON 设备收入池；ONT 量大、OLT 端口和 combo card 利润更好。 |
| 25GS-PON | Nokia 生态领先，Google Fiber、Frontier、enterprise/wholesale/MDU 场景试点 | 10Gbps+ premium broadband、企业接入、mobile xHaul | 2026 小批高毛利，2027 随 10G 套餐竞争和企业 SLA 放量。 |
| 50G PON / HS-PON | 中国、Nokia/ZTE/Huawei/Calix/Airoha 等进入互通和示范 | enterprise、campus、FTTR、premium residential、切片 | 2026 仍是 trial/flagship，2027 是商业化预期差；ONU optics 成本决定节奏。 |
| DOCSIS 3.1 high-split / mid-split | Cable 主流升级；Charter 2026 核心 | 提升上行到 100Mbps-1Gbps+，延长 HFC 资产寿命 | 2026 cable 采购大头在 amps、taps、RPD、vCMTS、3.1+ modem。 |
| DOCSIS 4.0 FDX | Comcast 领先，FDX amps/nodes/gateway 扩围 | 对称 multi-gig over existing HFC | 2026 最明确 D4.0 订单来自 Comcast 生态；后续看 unified chips。 |
| DOCSIS 4.0 ESD/FDD | Charter/Cox/欧洲 cable 更偏该方向，但大规模节奏慢于 high-split | 1.8GHz 扩频、5-10Gbps 下行、上行增强 | 2026-2027 高弹性，但受 1.8GHz plant、passives、CPE 认证约束。 |
| DAA / Remote PHY / Remote MACPHY / vCMTS | Comcast、Charter、Cox、Liberty 等长期方向 | 分布式接入、降低 headend、软件化 capacity | Harmonic、CommScope、Vecima、Cisco/legacy 受益；软件和 RPD 价值更高。 |
| Wi-Fi 6E / Wi-Fi 7 | 2026 Wi-Fi 7 进入运营商网关和企业 AP 主流 | 6GHz、MLO、320MHz、4K QAM、低时延 | 2026 最确定 CPE/AP 升级；芯片、RF、cloud-managed Wi-Fi 价值上移。 |
| Standard Power 6GHz / AFC | 美国/加拿大进展快，2026 大型场馆、教育、工业加速 | 室外/大空间 6GHz Wi-Fi 7 覆盖 | 使 enterprise Wi-Fi 7 从“近距离峰值”走向可规划覆盖。 |

### 2.3 项目内 AI 芯片路线对本行业的映射

项目内 AI 芯片资料显示，2026-2027 价值和出货权重最高的平台大致是 NVIDIA GB300/B300、GB200/B200、Vera Rubin、AWS Trainium2/3、Google TPU Ironwood/TPU8、AMD MI350/MI400、Microsoft Maia 200、Meta MTIA、OpenAI/Broadcom custom accelerator、中国 Ascend/Cambricon 等。它们对本行业的影响不是直接消耗 PON/DOCSIS/Wi-Fi 芯片，而是通过 **流量、企业园区、边缘节点、运营商城域网和客户体验指标** 传导。

| AI 芯片/平台 | 2026-2027 技术背景 | 对宽带接入行业的拉动 |
|---|---|---|
| NVIDIA GB300/B300、GB200 | 2026 主力，AI 数据中心网络以 800G/1.6T、NVLink/InfiniBand/Ethernet 为核心 | 拉动城域光纤和运营商企业专线；住宅端主要通过 AI 应用提高上行和低时延要求。 |
| NVIDIA Rubin / Rubin Ultra | 2026 H2 起步、2027 放量，HBM4/液冷/高密集群 | 若推理多模态爆发，运营商会加速 fiber backhaul、edge cloud 和企业 Wi-Fi 7。 |
| Google TPU Ironwood/TPU8 | 推理优先、TPU8 训练/推理分化，Google/Anthropic 多云 | Google Fiber/云边协同更可能验证 25G/50G PON、OCS/光网络和 AI home use cases。 |
| AWS Trainium2/3/4 | Rainier/Anthropic GW 级，云端推理成本下降 | 推理价格下降会扩大端侧用户调用频率，增加家庭/SMB 上行、Wi-Fi 与 CDN/edge 需求。 |
| AMD MI350/MI400 Helios | 2026 H2-2027 机架级竞争增强 | 多供应商 GPU 降低 AI 服务成本，间接推高 AI 应用流量。 |
| Microsoft Maia 200 | Azure/Copilot 推理，自研芯片 + HBM/SRAM | 企业 Copilot/AI PC 使用强度提升，企业 WLAN/Wi-Fi 7 和 SD-Branch 升级受益。 |
| Meta MTIA / OpenAI-Broadcom | 自研 ASIC 从 2026 H2 起步，2027 可能 GW 级 | 社交/视频/agentic 推理爆发会提升消费者宽带流量；Broadcom 同时在接入/DOCSIS/Wi-Fi 芯片有生态协同。 |
| 中国 Ascend/Cambricon | 国产 AI 云与政企推理集群放量 | 中国 10G/50G PON、FTTR、Wi-Fi 7/7+、政企园区网升级更快。 |

### 2.4 技术成熟与放量时间：三情景

| 子方向 | 2026 基准 | 2026 乐观 | 2026 极度超预期 | 2027 基准 | 2027 乐观 | 2027 极度超预期 |
|---|---|---|---|---|---|---|
| XGS-PON | FTTH 新建默认技术，北美/欧洲/拉美/中东继续扩张 | BEAD 订单 H2 明显落地 | 运营商因 cable 竞争加速把 2G/5G 套餐推为主流 | 继续主导 PON 收入 | XGS-PON + Wi-Fi 7 网关成新装标配 | XGS-PON ONT 量价齐升，50G 推迟但 XGS 赚满 |
| 25GS-PON | 企业、MDU、Google Fiber/Nokia 生态小批 | 高端住宅 10G+ 套餐驱动 | 若 50G optics 成本高，25G 成为过渡主线 | 小规模商用放量 | 北美/澳洲/欧洲多运营商采用 | 25G 成为 premium PON 默认路线之一 |
| 50G PON | 中国/企业示范，Nokia/ZTE/Huawei/Calix 试点 | 中国运营商加速 50G PON + FTTR | 50G Combo optics 成本快速下降，新增端口超预期 | 企业/园区/高端住宅商用初期 | 50G 端口收入进入 $2B-$6B 池 | 中国 + 中东 + 北美高端客户形成 $8B-$12B 订单池 |
| DOCSIS 3.1 high-split/DAA | Charter、Cox、欧洲 cable 主线，RPD/vCMTS/amps 订单 | Cable 面对 fiber 抢客加速高上行升级 | 供应商交付顺利，high-split 覆盖率跃升 | 继续放量但逐步让位 D4 | 高上行套餐显著降低 churn | D3.1+ 与 D4 混合网络快速覆盖大多数 cable homes |
| DOCSIS 4.0 FDX | Comcast 扩围，FDX amps/gateway 供货 | Comcast 从百万 homes 级迈向多百万 homes | FDX unified chipset 多 ODM 供货，市场感知加速 | Comcast 规模化、其他 FDX operator 跟进 | D4.0 FDX 对称 2G/5G 套餐常态化 | D4 FDX 成 cable 防御 FTTH 的关键叙事 |
| DOCSIS 4.0 ESD/FDD | 认证/设备准备，Charter 仍以 1.2GHz/high split 为主 | Charter/Cox 1.8GHz 采购提前 | Cox/Charter 合并后统一路线加速 | 2027 开始规模部署 | ESD/FDD 进入大规模 HFC upgrade | D4.0 ESD + DAA 在北美/欧洲形成 $5B+ 年订单 |
| Wi-Fi 7 residential CPE | 新装高端网关/路由器主流 | 运营商把 Wi-Fi 7 作为降 churn 工具 | AI PC/手机换机拉动用户主动升级 | 中高端网关默认 Wi-Fi 7 | 低端双频 Wi-Fi 7 下沉 | Wi-Fi 7 CPE 收入峰值提前到 2027 |
| Enterprise Wi-Fi 7 | 高密办公室、教育、医疗、酒店、工厂升级 | 6GHz/AFC 与 AI AIOps 形成 ROI | 企业 AI app + AI PC 让 Wi-Fi 7 预算前置 | Wi-Fi 7 成 enterprise AP 新主流 | SP 6GHz/AFC 大规模化 | Wi-Fi 7 + AI/Cognitive WLAN 支出超过 Wi-Fi 6/6E |
| AI-native gateway / AIOps | Qualcomm/Broadcom/Calix/Plume 平台化 | 运营商开始把安全、诊断、边缘 AI 打包收费 | 网关 NPU/AI service 形成 ARPU 增量 | 托管 Wi-Fi 软件 attach 上升 | 家庭 AI agent、安全、能耗管理成为套餐 | 网关从低毛利硬件变成高毛利 platform endpoint |

### 2.5 2026 最可能赚钱的技术路径

1. **XGS-PON OLT/ONT + Wi-Fi 7 HGS 网关。** 这是最大量、最少争议的路线，适配 FTTH 新建、overbuild、BEAD、MDU 和 2G/5G 家宽套餐。
2. **DOCSIS high-split/DAA/vCMTS + DOCSIS 4.0 FDX 扩围。** 2026 cable 不会等待 D4.0 全面完美化，会先买 1.2GHz、high-split、RPD、amps、vCMTS 和 D3.1+ CPE；Comcast 型 FDX 是 D4.0 第一条实战曲线。
3. **Wi-Fi 7 AP/CPE + cloud-managed Wi-Fi/AIOps。** 运营商把 Wi-Fi 体验作为留存和 upsell 入口，企业把 Wi-Fi 7 当作 AI PC/IoT/视频协作的底座。
4. **PON/DOCSIS/Wi-Fi 芯片和高端光器件。** 50G PON、D4.0 unified chipset、Wi-Fi 7/8、10G LAN、2.5G/10G switch PHY、FEM、burst-mode optics 属于小体量高壁垒。

## 3. 已经开始放量的关键产品：规模、渗透率与利润率

> 口径说明：以下“3个月/1年/2年市场规模”为从 2026-05-08 起的全球累计设备/软件/订单收入池估算；不是运营商宽带服务收入。渗透率为该子技术在对应新增采购或装机升级中的占比。

### 3.1 已放量产品市场规模与渗透率

| 已放量产品/技术 | 当前放量证据 | 未来3个月：基准/乐观/极超 | 未来1年：基准/乐观/极超 | 未来2年：基准/乐观/极超 | 渗透率路径：基准/乐观/极超 |
|---|---|---:|---:|---:|---|
| XGS-PON OLT/ONT/Combo PON | Dell'Oro 称 XGS-PON 仍主导，FBA 美国 2025 新增 FTTH passings 11.8M | $2.4-3.2B / $3.2-4.0B / $4.0-5.0B | $9-13B / $13-17B / $17-22B | $19-28B / $28-38B / $38-52B | 新增 FTTH PON 端口 45%-60% -> 55%-70% -> 65%-80%；极超 2027 新装高端区域 85%+ |
| GPON/EPON 低成本 ONT 与替换 | 158M PON ONT 年出货中仍大量为 GPON/EPON | $1.2-1.8B / $1.8-2.2B / $2.2-2.8B | $4.5-6.5B / $6.5-8.5B / $8.5-11B | $8-12B / $12-16B / $16-21B | 新增低 ARPU PON 仍 30%-45%，两年后降至 20%-35%；极超因新兴市场维持 40% |
| FTTR / 室内光网络 / 高端家庭网关 | 中国运营商 FTTR 推动，50G PON 社区把 FTTR 作为示范 | $0.5-1.0B / $1.0-1.6B / $1.6-2.5B | $2.5-5B / $5-8B / $8-13B | $6-12B / $12-22B / $22-35B | 中国新装中高端 FTTH 15%-25% -> 25%-40%；海外仍 <5%-10%；极超海外 MDU 采用 |
| DOCSIS 3.1 high-split / 1.2GHz upgrade | Charter 10-K 明确 1.2GHz/high split/DAA，CableLabs 显示上行覆盖快速提升 | $0.8-1.3B / $1.3-1.8B / $1.8-2.5B | $3.5-5.5B / $5.5-8B / $8-11B | $7-11B / $11-17B / $17-25B | Cable 新增升级节点 35%-50% -> 50%-65% -> 60%-75%；极超大 MSO 加速 |
| DAA/RPD/vCMTS/Remote PHY | Comcast 100k digital nodes 历史基础，Charter/CableLabs DAA 主线 | $0.7-1.2B / $1.2-1.8B / $1.8-2.6B | $3-5B / $5-8B / $8-12B | $7-12B / $12-20B / $20-30B | 大型 cable upgrade 中 40%-55% -> 55%-70%；极超 DAA 成所有新增 D4 项目前置 |
| DOCSIS 4.0 FDX amps/nodes/gateways | Comcast 商用领先，CommScope 推 FDX/unified amps 和 RPD | $0.3-0.8B / $0.8-1.5B / $1.5-2.5B | $1.5-3.5B / $3.5-6.5B / $6.5-10B | $4-9B / $9-16B / $16-28B | 北美 cable homes D4.0 active availability 低个位数 -> 8%-15%；极超 2027 达 20%-30% |
| DOCSIS 3.1+/4.0 CPE 与 Wi-Fi 7 cable gateway | XB10、Hitron CODA6021、Vantiva/Sercomm/CommScope/Hitron 供应链 | $0.4-0.9B / $0.9-1.4B / $1.4-2.2B | $2-4B / $4-7B / $7-11B | $5-10B / $10-18B / $18-30B | Cable 新发高端 CPE 中 Wi-Fi 7 25%-40% -> 50%-70%；D4 modem <5% -> 10%-25% |
| Residential Wi-Fi 7 router/AP/mesh | WBA/ABI 预计 Wi-Fi 7 AP 2026 出货 117.9M | $1.8-2.8B / $2.8-4.0B / $4.0-5.5B | $8-12B / $12-17B / $17-24B | $18-28B / $28-42B / $42-60B | 新发中高端住宅 CPE 25%-40% -> 45%-65% -> 65%-80%；极超 2027 低端下沉 |
| Enterprise Wi-Fi 7 AP + WLAN controller/cloud | IDC：企业 WLAN 支出 60% 流向 Wi-Fi 6E/7；WBA：Wi-Fi 7 为 2026 最可能部署技术 | $1.2-2.0B / $2.0-2.8B / $2.8-4.0B | $6-9B / $9-13B / $13-18B | $14-22B / $22-32B / $32-45B | 企业 AP 新采购 Wi-Fi 7 20%-35% -> 40%-60% -> 60%-75%；极超高密场景 80%+ |
| Cloud-managed Wi-Fi / AIOps / home security services | Calix 57%+ GM，Plume/Charter、Juniper Mist、Cisco/Meraki 等 | $0.5-0.9B / $0.9-1.4B / $1.4-2.2B | $2.5-4.5B / $4.5-7B / $7-11B | $6-11B / $11-18B / $18-30B | 新装运营商 CPE software attach 35%-50% -> 50%-70%；极超 80%+ |
| BEAD/FTTH 被动光网络材料：光缆、分路器、closures、cabinets | NTIA 资金释放，Corning 称 BEAD 从规划转采购 | $2-4B / $4-6B / $6-9B | $10-18B / $18-28B / $28-42B | $25-45B / $45-70B / $70-100B | 美国未覆盖区域 fiber 项目 2026 H2 起动，2027 是主放量；极超取决于劳动力和 BABA 供应 |

### 3.2 已放量产品增长与利润率

| 已放量产品/技术 | 未来1年收入增速：基准/乐观/极超 | 当前毛利率区间 | 1年毛利率：基准/乐观/极超 | 2年毛利率：基准/乐观/极超 | 主要毛利决定因素 |
|---|---:|---:|---:|---:|---|
| XGS-PON OLT/ONT/Combo | +8%-18% / +18%-30% / +30%-45% | OLT 35%-50%，ONT 15%-28%，平台厂 blended 35%-58% | 35%-52% / 40%-55% / 45%-60% | 34%-50% / 40%-55% / 45%-62% | OLT 端口密度、combo optics、运营商认证、软件管理、ONT 价格竞争。 |
| GPON/EPON 低成本 | -5%-+5% / +5%-12% / +12%-20% | 10%-22% | 9%-20% / 12%-22% / 15%-25% | 8%-18% / 10%-20% / 12%-24% | 低端 ASP、内存涨价、ODM 规模、国家补贴项目。 |
| FTTR / 室内光网络 | +25%-45% / +45%-70% / +80%+ | 25%-45% | 28%-48% / 35%-55% / 45%-65% | 25%-45% / 35%-55% / 45%-65% | 套餐绑定、室内施工能力、光模块/分光器成本、运营商补贴。 |
| DOCSIS high-split/1.2GHz | +20%-35% / +35%-55% / +60%+ | 25%-40% | 28%-42% / 32%-46% / 38%-52% | 25%-40% / 30%-45% / 35%-50% | 放大器/节点短缺、field hardened 认证、MSO 长单价格。 |
| DAA/RPD/vCMTS | +25%-45% / +45%-70% / +80%+ | 硬件 30%-45%，软件 55%-75% | 35%-50% / 40%-55% / 50%-65% | 35%-50% / 45%-60% / 55%-70% | vCMTS 软件占比、RPD 认证、operator lock-in。 |
| DOCSIS 4.0 FDX/ESD ecosystem | +80%-150% / +150%-250% / +300%+ | 早期硬件 35%-50%，芯片 55%-70% | 38%-55% / 45%-60% / 55%-70% | 35%-50% / 42%-58% / 50%-68% | 供不应求、统一芯片、多运营商认证、现场返修率。 |
| DOCSIS/Wi-Fi 7 cable gateway | +50%-100% / +100%-180% / +200%+ | ODM 10%-18%，品牌/CPE 平台 20%-35%，芯片 55%-70% | 12%-25% / 20%-35% / 30%-45% | 10%-22% / 18%-32% / 25%-42% | DRAM/NAND、Wi-Fi 7 RF、10G PHY、运营商租赁模式。 |
| Residential Wi-Fi 7 | +60%-100% / +100%-160% / +180%+ | 芯片 50%-65%，品牌 25%-40%，ODM 8%-15% | 25%-38% / 30%-42% / 35%-48% | 22%-35% / 28%-40% / 32%-45% | 初期价格低、内存涨价、6GHz/tri-band 配置、渠道竞争。 |
| Enterprise Wi-Fi 7 | +35%-55% / +55%-80% / +100%+ | 品牌 AP 45%-65%，cloud 70%-85% | 45%-65% / 50%-68% / 55%-72% | 42%-62% / 48%-68% / 55%-75% | AIOps/cloud license、AFC、PoE/switch attachment、客户认证。 |
| Cloud-managed Wi-Fi/AIOps | +25%-45% / +45%-70% / +90%+ | 65%-90% | 68%-88% / 72%-90% / 78%-92% | 68%-88% / 75%-90% / 80%-93% | 软件 attach、数据规模、运营商 churn reduction、AI 模型成本。 |
| BEAD/FTTH passive | +15%-30% / +30%-50% / +70%+ | 光纤/线缆 20%-35%，连接器/closures 25%-45% | 22%-38% / 28%-45% / 35%-55% | 20%-35% / 25%-42% / 30%-50% | BABA 约束、光纤预制化、施工节奏、原材料和运费。 |

## 4. 在研关键产品与细分技术：规模、渗透率与利润率

### 4.1 未来快速增长技术清单

| 在研/早期商业化技术 | 当前状态 | 未来3个月：基准/乐观/极超 | 未来1年：基准/乐观/极超 | 未来2年：基准/乐观/极超 | 渗透率路径 |
|---|---|---:|---:|---:|---|
| 50G PON OLT/ONU/Combo optics | Nokia/ZTE/Huawei/Calix/Airoha 等互通与示范，中国已有 50G 社区 | $0.08-0.20B / $0.20-0.45B / $0.45-0.80B | $0.6-1.5B / $1.5-3B / $3-6B | $2-6B / $6-12B / $12-22B | PON 新增端口 <1% -> 2%-5% -> 5%-12%；极超 2027 中国/中东高端端口 15%-20% |
| 25GS-PON mass-market CPE | Nokia 生态较成熟，Google Fiber/Frontier/altafiber/enterprise 方向 | $0.10-0.25B / $0.25-0.50B / $0.50-0.90B | $0.8-1.8B / $1.8-3.5B / $3.5-6B | $2.5-6B / $6-10B / $10-16B | 高端 FTTH/企业 PON 2%-4% -> 5%-10% -> 10%-20% |
| PON slicing / deterministic PON / enterprise SLA | BBF/Omdia 讨论 50G PON slicing，运营商企业专线化 | $0.03-0.10B / $0.10-0.25B / $0.25-0.50B | $0.3-0.8B / $0.8-1.8B / $1.8-3.5B | $1-3B / $3-7B / $7-12B | 新增企业 PON 5%-10% -> 15%-30%；极超 50% |
| Remote OLT / distributed PON | Vecima R-OLT 领先，适合 cable-to-fiber、rural、MDU | $0.15-0.30B / $0.30-0.55B / $0.55-0.90B | $0.8-1.6B / $1.6-2.8B / $2.8-4.5B | $2-5B / $5-9B / $9-15B | 新增 fiber access nodes 5%-10% -> 12%-20% -> 20%-35% |
| DOCSIS 4.0 unified FDX/ESD SoC | Broadcom/Comcast 已发布方向，MaxLinear Puma 8 生态 | $0.05-0.15B / $0.15-0.35B / $0.35-0.70B | $0.6-1.2B / $1.2-2.5B / $2.5-4.5B | $2-5B / $5-9B / $9-15B | 新发 DOCSIS modem SoC 中 D4.0 <5% -> 10%-25% -> 25%-45% |
| DOCSIS 3GHz / 6GHz HFC extension | CableLabs 研究和 PoC，规格未规模化 | <$0.03B / $0.03-0.08B / $0.08-0.15B | $0.1-0.4B / $0.4-0.8B / $0.8-1.5B | $0.5-2B / $2-5B / $5-10B | 2027 仍偏 PoC/field trial；极超为 3GHz taps/amps 预采购 |
| Low Latency DOCSIS / app-aware QoE | LLD 已进入 D3.1/D4.0，Comcast 等部署 | $0.05-0.15B / $0.15-0.35B / $0.35-0.70B | $0.4-1B / $1-2B / $2-4B | $1.5-4B / $4-8B / $8-14B | Cable broadband premium tiers 5%-15% -> 20%-40%；极超 60% |
| Standard Power 6GHz / AFC Wi-Fi 7 | 美国 AFC 运营成熟，Cisco 等支持；FCC GVP 扩展 | $0.20-0.50B / $0.50-0.90B / $0.90-1.5B | $1.5-3B / $3-6B / $6-10B | $5-10B / $10-18B / $18-30B | 企业/场馆 Wi-Fi 7 中 AFC 10%-20% -> 30%-50%；极超 70% |
| Wi-Fi 8 / 802.11bn prototype | Broadcom/Qualcomm 2026 推早期芯片/样机，标准未最终 | <$0.03B / $0.03-0.08B / $0.08-0.20B | $0.1-0.4B / $0.4-0.9B / $0.9-1.8B | $1-3B / $3-7B / $7-12B | 2027 仍 <5% 企业新 AP；极超为高端预标准 AP |
| AI-native gateway / router NPU | Qualcomm A7 Elite、Broadcom AI access chipset、Calix One | $0.10-0.30B / $0.30-0.70B / $0.70-1.2B | $0.8-2B / $2-4B / $4-8B | $3-8B / $8-16B / $16-30B | 高端网关 NPU attach 5%-10% -> 15%-30% -> 30%-50%；极超 70% |
| Wi-Fi HaLow / IoT access | WBA 预计 2026 继续加速，适合低功耗远距 IoT | $0.05-0.15B / $0.15-0.35B / $0.35-0.60B | $0.4-0.9B / $0.9-1.8B / $1.8-3B | $1.5-4B / $4-8B / $8-14B | 工业/智慧城市 IoT 低个位数 -> 5%-10%；极超 15% |
| OpenRoaming / Wi-Fi offload platform | WBA 推动，移动运营商需要降低 cellular traffic cost | $0.05-0.15B / $0.15-0.35B / $0.35-0.70B | $0.4-1B / $1-2.5B / $2.5-5B | $1.5-4B / $4-9B / $9-16B | 公共 Wi-Fi/城市/venue 10%-20% -> 25%-45%；极超 60% |

### 4.2 在研技术利润率预测

| 技术 | 当前/早期毛利率 | 未来1年：基准/乐观/极超 | 未来2年：基准/乐观/极超 | 为什么能高溢价 |
|---|---:|---:|---:|---|
| 50G PON optics/line cards | 35%-60% | 35%-55% / 45%-65% / 55%-75% | 32%-50% / 40%-60% / 50%-70% | Burst-mode 50G optics、combo coexistence、PON timing、认证难；早期客户买的是未来 proofing。 |
| 25GS-PON | 35%-55% | 35%-55% / 42%-60% / 50%-68% | 32%-50% / 38%-58% / 45%-65% | 25G 与 XGS/GPON 共纤，CPE 少但高端用户愿付费，Nokia 生态领先。 |
| PON slicing/deterministic PON | 60%-85% 软件/功能毛利 | 65%-85% / 70%-88% / 75%-90% | 65%-85% / 72%-90% / 78%-92% | SLA、切片、QoE、OSS/BSS 集成是软件和控制面，不是低价硬件。 |
| Remote OLT | 35%-55% | 35%-55% / 40%-60% / 48%-65% | 35%-52% / 40%-58% / 45%-62% | Cable-to-fiber 和 rural 场景节省机房/馈线成本，设备认证和远端运维壁垒高。 |
| D4.0 unified SoC | 55%-70% | 58%-72% / 62%-75% / 68%-80% | 55%-70% / 60%-75% / 65%-80% | FDX/ESD 双路线统一、AI telemetry、CableLabs 认证、多年 operator design-in。 |
| DOCSIS 3GHz/6GHz | 早期 NRE/试验，毛利不可比 | 40%-60% / 50%-70% / 60%-80% | 35%-55% / 45%-65% / 55%-75% | 新 passives/amps/taps/measurement 工具，规格制定参与方可优先卡位。 |
| LLD/QoE software | 65%-90% | 68%-88% / 72%-90% / 78%-92% | 68%-88% / 75%-90% / 80%-93% | 降低延迟和投诉，可按 premium tier、gaming、business SLA 收费。 |
| SP 6GHz/AFC | AP 硬件 45%-65%，AFC service 70%-90% | 45%-65% / 55%-72% / 65%-85% | 42%-62% / 50%-70% / 60%-82% | 监管数据库、场景规划、enterprise validation、Cisco/Meraki/venue 锁定。 |
| Wi-Fi 8 early AP/chip | 芯片 55%-70%，AP 50%-65% | 50%-68% / 58%-72% / 65%-80% | 45%-65% / 55%-70% / 60%-75% | 预标准高端客户为了 reliability/AIOps 提前付费；但量产后 ASP 会降。 |
| AI-native gateway | 芯片 55%-70%，平台软件 70%-90% | 55%-75% / 65%-85% / 75%-90% | 55%-75% / 68%-88% / 78%-92% | 运营商买“少上门、少投诉、少 churn、增 ARPU”，可按软件/安全/AI 服务收费。 |
| Wi-Fi HaLow | 芯片 45%-60%，模块 25%-45% | 35%-55% / 45%-65% / 55%-75% | 32%-52% / 42%-62% / 50%-70% | 低功耗远距 IoT 替代专网，工业/公用事业认证周期形成锁定。 |
| OpenRoaming/offload | 平台 70%-90% | 70%-88% / 75%-90% / 80%-92% | 70%-88% / 75%-90% / 80%-93% | 运营商 offload 成本下降、漫游身份、SIM/eSIM/Passpoint 集成。 |

## 5. 供给侧：产能结构、瓶颈、成本与价格传导

### 5.1 产能结构

| 环节 | 主要产能地区 | 主要公司/生态 | 工艺/能力 |
|---|---|---|---|
| PON OLT/ONT 系统 | 中国、越南、泰国、台湾、墨西哥、东欧、美国少量 final assembly | Huawei、ZTE、FiberHome、Nokia、Calix、Adtran、DZS、Ubiquiti、Ciena/Cisco 部分，ODM Sercomm/Arcadyan/Sagemcom/Hitron | OLT line card、PON MAC/PHY、burst-mode optics、combo PON、ONT/HGS。 |
| 25G/50G PON optics | 中国、台湾、日本、韩国、东南亚 | Hisense Broadband、Accelink、Source Photonics、Lumentum、Coherent、Innolight、Eoptolink、Broadex、AIO Core optics 生态 | 25G/50G burst-mode laser/APD/TIA、BOSA、symmetric/asymmetric optics。 |
| DOCSIS nodes/amps/RPD/vCMTS | 北美、墨西哥、中国、台湾、欧洲 | CommScope/Vistance、Harmonic、Vecima、Cisco、Casa legacy、Teleste、ATX、Technetix | 1.2/1.8GHz amps、RPD/RMD、vCMTS software、field-hardened RF。 |
| DOCSIS/PON/Wi-Fi SoC | 台积电/三星/成熟逻辑代工，封测在台湾/中国/东南亚 | Broadcom、MaxLinear、Qualcomm、MediaTek、Airoha、Realtek、Intel/MaxLinear legacy、Celeno/Imagination 等 | 6-16nm 级 cable/fiber SoC，Wi-Fi 7 RF/baseband，10G/2.5G Ethernet PHY。 |
| Wi-Fi 7 AP/CPE | 中国、台湾、越南、泰国、马来西亚、墨西哥 | TP-Link、Netgear、Ubiquiti、Cisco/Meraki、HPE Aruba、Huawei、Juniper Mist、Extreme、CommScope Ruckus、Zyxel、Vantiva、Sercomm、Arcadyan | Tri-band RF、FEM、antenna tuning、PoE/2.5G/10G LAN、cloud firmware。 |
| 光纤/线缆/被动件 | 美国、中国、欧洲、日本、印度、东南亚 | Corning、Prysmian、CommScope、AFL、YOFC、Furukawa、Fujikura、Sumitomo、Hengtong、FiberHome、Clearfield、Belden、Panduit | 光纤预制、MPO/LC/SC/APC、closures、splitters、cabinets、BABA 合规。 |
| 测试认证 | 美国、欧洲、中国台湾、中国、日本 | CableLabs、Broadband Forum/UNH-IOL、Wi-Fi Alliance、Keysight、VIAVI、R&S、Anritsu、EXFO | DOCSIS 4.0 security/interop、PON plugfest、Wi-Fi 7/6GHz/AFC、field meters。 |

### 5.2 供给瓶颈

1. **DRAM/NAND/eMMC/LPDDR。** AI 数据中心把 DRAM/NAND/HBM 价格和产能吸走，高端 Wi-Fi 7 网关、DOCSIS 4.0 gateway、企业 AP 的内存成本 2026 最难控。
2. **25G/50G PON burst-mode optics。** OLT 侧连续发送容易，ONU 侧 burst-mode 高速上行、定时、温漂、功率预算和低成本量产更难，是 50G PON 放量阀门。
3. **DOCSIS 4.0 field hardware。** 1.8GHz/FDX amps、taps、passives、RPD、nodes 需要现场可靠性、温度、供电、噪声和长级联验证；实验室速度不等于可规模施工。
4. **认证与互通。** CableLabs、Broadband Forum、Wi-Fi Alliance、AFC、运营商自有测试周期会把芯片样片到收入确认拉长 6-18 个月。
5. **施工与许可。** FTTH trenching、make-ready、pole attachment、splicing technicians、MDU access、municipal permits 会比 OLT/ONT 更慢。
6. **BEAD/BABA 合规供应。** 美国 BEAD 项目对国产化和合规链条要求高，可能造成“有资金但缺合规光缆/closures/人力”的局面。
7. **Wi-Fi 7 客户端生态和 6GHz 监管。** 没有 6GHz 客户端、AFC 或标准功率覆盖，Wi-Fi 7 的 MLO/320MHz 价值会被削弱。
8. **运营商库存与预算周期。** 2021-2022 供应链紧张后运营商曾过度备货，2023-2025 去库存压制采购；2026 复苏仍会呈季度波动。
9. **中国设备地缘政治。** Huawei/ZTE 在欧洲/美国受限，利好 Nokia/Calix/Adtran/Cisco/Juniper/HPE，但也减少低价供给、提高项目成本。
10. **10G LAN/PoE/家庭布线短板。** 10G PON 或 D4.0 网关若家内只有 1G/2.5G LAN，用户感知不足，会延迟高端套餐渗透。

### 5.3 BOM 与单位成本拆分

| 产品 | 典型 BOM/成本拆分 | 毛利决定因素 | 价格传导机制 |
|---|---|---|---|
| XGS-PON OLT line card/port | PON MAC/ASIC 20%-30%，optics 25%-35%，PCB/电源/散热 10%-15%，chassis allocation 10%-20%，软件/许可 10%-20%，测试 5%-10% | 端口密度、combo optics、平台锁定、OSS/BSS 集成 | 大运营商年度框架价；高端 combo/25G/50G 可按端口溢价。 |
| XGS-PON ONT/HGS | PON SoC 15%-25%，Wi-Fi/CPU/RF 20%-35%，DRAM/NAND 10%-20%，optics 10%-18%，LAN PHY/ports 5%-10%，电源/外壳/天线 15%-25%，软件 5%-10% | Wi-Fi 7 配置、内存价格、运营商定制、远程管理 | CPE 租赁/补贴可转嫁给用户月费；硬件厂常需接受年度降价。 |
| 50G PON ONU/OLT optics | Laser/APD/TIA/driver 30%-45%，PON SoC/PHY 20%-30%，thermal/calibration 10%-15%，封装/测试 15%-25% | 良率、burst-mode timing、功率预算、温度等级 | 初期按 high-end enterprise SLA 定价，量产后向 XGS-PON 靠拢。 |
| DOCSIS 4.0 gateway | Cable SoC 20%-30%，RF tuner/FEM/amps 15%-25%，Wi-Fi 7 20%-30%，DRAM/NAND 10%-15%，10G/2.5G ports 5%-10%，电源/热/外壳 10%-15%，软件 5%-10% | Broadcom/MaxLinear 芯片供应、Wi-Fi 7 tri-band、运营商认证、返修率 | 运营商租赁网关月费和高端套餐吸收；ODM 毛利低，芯片/品牌毛利高。 |
| DOCSIS amps/nodes/RPD | RF components 20%-30%，RPD/SoC 20%-30%，power/hardened enclosure 20%-30%，thermal/sealing 10%-15%，测试/认证 10%-15% | 1.8GHz/FDX 性能、级联噪声、现场可靠性、安装效率 | MSO 项目制采购，供不应求时按交期和服务能力溢价。 |
| Enterprise Wi-Fi 7 AP | Wi-Fi SoC/RF/FEM 35%-50%，CPU/switch/PoE 10%-20%，DRAM/NAND 8%-15%，antenna/mechanics 10%-20%，cloud license/support 5%-15% | Cloud AIOps、AFC、security license、PoE switch attachment | 硬件可低溢价，软件订阅和 support contract 保毛利。 |
| Cloud-managed Wi-Fi/AIOps | 云 infra 10%-20%，R&D/AI model 25%-40%，support/CS 15%-25%，sales/channel 20%-35% | 数据规模、运营商集成、降低 truck roll/churn 的 ROI | 按 subscriber、AP、site、feature tier 收费；最容易提价。 |
| FTTH passive/BABA | 光纤/线缆 35%-50%，closures/cabinets 15%-30%，连接器/分路器 10%-20%，物流 5%-10%，施工辅材 10%-20% | 合规产能、项目批量、预制化、施工效率 | BEAD 和运营商项目可做 escalation clause，短缺时交期溢价。 |

## 6. 竞争格局与壁垒

### 6.1 市场结构与头部集中度

| 细分市场 | 头部结构 | 集中度判断 | 说明 |
|---|---|---|---|
| 全球 PON OLT | Huawei、ZTE、Nokia、FiberHome、Calix、Adtran、DZS | 全球 top 4 约 65%-80%；排除中国后 Nokia/Calix/Adtran 份额更高 | 中国设备商强在规模和成本；北美/欧洲受地缘政治影响，Nokia/Calix/Adtran 受益。 |
| ONT/HGS/CPE | Sercomm、Arcadyan、Vantiva、Sagemcom、Hitron、ZTE、Huawei、Nokia、Calix/Adtran 生态 | 分散但运营商项目高度锁定 | ODM 毛利低，平台/云管/运营商认证决定粘性。 |
| 25G/50G PON | Nokia、ZTE、Huawei、Calix、Adtran、Airoha、Sagemcom/Hitron 等 | 早期集中度高 | Nokia 25G/50G 同卡演进有先发；中国 50G 由 Huawei/ZTE/FiberHome 牵引。 |
| DOCSIS network equipment | CommScope/Vistance、Harmonic、Vecima、Cisco legacy、Teleste、ATX/Technetix | 北美高度集中 | Field-proven amps/nodes/RPD/vCMTS 认证壁垒高，新进入者难。 |
| DOCSIS silicon | Broadcom、MaxLinear | 接近双寡头 | D4.0 unified chipset 和 Puma 8 等决定 modem/node 生态。 |
| Wi-Fi 7 chipset | Broadcom、Qualcomm、MediaTek/Airoha、MaxLinear、Realtek | 高集中，三强主导高端 | Tri-band、RF FEM、MLO、power、reference design 是壁垒。 |
| Enterprise WLAN | Cisco/Meraki、HPE Aruba、Huawei、Ubiquiti、Juniper Mist、Extreme、CommScope Ruckus、TP-Link Omada | 中高集中，区域差异大 | 北美企业偏 Cisco/HPE/Juniper/Ubiquiti；中国 Huawei 强；SMB TP-Link/Ubiquiti 强。 |
| Managed Wi-Fi/AIOps | Calix、Plume、Cisco/Meraki、Juniper Mist、HPE Aruba Central、ExtremeCloud、CommScope、TP-Link Omada | 平台 lock-in 明显 | 一旦接入 OSS/BSS、app、support 和数据湖，切换成本高。 |
| FTTH passive | Corning、Prysmian、CommScope、AFL、Clearfield、YOFC、Fujikura、Sumitomo、Hengtong | 区域性集中 | 美国 BEAD 合规和产能可形成局部稀缺。 |

### 6.2 壁垒清单：为什么能定价

| 壁垒 | 体现 | 为什么能定价 |
|---|---|---|
| 标准与认证 | CableLabs D4.0、BBF PON Plugfest、Wi-Fi CERTIFIED 7、AFC、operator lab | 认证失败会延迟运营商上线，客户愿意为“已验证、可互通、少返修”付费。 |
| 运营商切换成本 | OSS/BSS、TR-069/TR-369 USP、OpenSync/prpl/RDK-B、远程诊断、app、库存 | 替换 CPE/OLT 平台会影响客服、truck roll、库存和固件安全，成本远高于硬件差价。 |
| 规模与供应链 | 大客户需要百万级 ONT/AP、长期 firmware、全球 RMA | 交期、质量和售后是运营商 KPI，规模厂可在短缺时优先拿料。 |
| 高速模拟/RF/光器件 | DOCSIS 1.8GHz RF、50G burst-mode optics、Wi-Fi 7 6GHz FEM | 这是工程良率壁垒，不是简单软件复制；调试周期长。 |
| 平台数据 | AIOps 需要大量 AP/网关 telemetry、故障标签、家庭拓扑 | 数据越多，模型越准，能减少投诉和上门，形成正反馈。 |
| 监管/地缘政治 | BEAD BABA、美国/欧洲对 Huawei/ZTE 限制、6GHz AFC | 合规供应商池缩小后，剩余厂商议价提升。 |
| 渠道与客户锁定 | Cisco/HPE/Juniper/Calix/Plume 与企业/运营商销售体系 | 采购不是只买 AP，而是买安全、support、controller、cloud 和 SLA。 |
| 现场施工能力 | FTTH splicing、pole attachment、HFC amps/taps 施工 | 有设备也要能施工和验收，EPC/材料一体化能力可溢价。 |

### 6.3 价值捕获排序

| 排名 | 价值链层级 | 长期 ROIC/毛利判断 | 原因 |
|---:|---|---|---|
| 1 | Cloud-managed Wi-Fi/AIOps/运营商体验平台 | 最高，毛利 70%-90% | 直接降低 churn、truck roll、客服成本，可按 subscriber/site 收费。 |
| 2 | PON/DOCSIS/Wi-Fi 高端芯片与参考设计 | 很高，毛利 55%-75% | 认证周期长、客户 design-in 长、FDX/ESD/MLO/6GHz/50G PHY 壁垒高。 |
| 3 | DOCSIS 4.0 amps/nodes/RPD/vCMTS | 高，毛利 35%-60% | MSO 采购集中、现场可靠性要求高、供应商少。 |
| 4 | 25G/50G PON optics/OLT line cards | 高，毛利 35%-65% | 高端 optics 和 combo 端口早期稀缺，企业 SLA 支撑溢价。 |
| 5 | Enterprise Wi-Fi 7 AP + cloud license | 高，毛利 45%-70% | 硬件竞争激烈但 cloud/security/AIOps 抬高 blended margin。 |
| 6 | FTTH passive + 合规材料 | 中高，毛利 20%-45% | 周期性强，但 BEAD/BABA/光缆短缺会形成局部高价。 |
| 7 | 低端 ONT/CPE ODM | 低，毛利 8%-18% | 客户强势、竞争充分、内存涨价难完全传导。 |

## 7. 2026 关键变化：3 个最可能拐点

### 拐点一：Wi-Fi 7 从高端消费电子进入运营商默认 CPE

WBA/ABI 对 2026 Wi-Fi 7 AP 117.9M 出货的预测，叠加 Charter 2026 推 Invincible WiFi、Comcast XB10、Hitron/Vantiva/Sagemcom/Sercomm 的 Wi-Fi 7 gateway，使 Wi-Fi 7 从零售路由器故事变成运营商 CPE 采购故事。AI PC、手机和 XR 设备换机一旦增加 6GHz/MLO 客户端，运营商会更愿意把 Wi-Fi 7 用于高端套餐留存。

**最可能放量子方向：** residential Wi-Fi 7 HGS、enterprise tri-band AP、cloud-managed Wi-Fi、AIOps、安全订阅。

### 拐点二：Cable 升级从“等待 DOCSIS 4.0”转为“high-split + DAA + D4.0 并行”

Charter 2026 的主线仍是 1.2GHz/high-split/DAA；Comcast 的 FDX 证明 D4.0 可以商用；CableLabs 互通从速度转向安全和多厂商。结果是 cable 运营商不再二选一，而是按 plant 条件分层采购：D3.1+ 和 high-split 负责大范围上行，D4.0 FDX/ESD 负责 premium 区域。

**最可能放量子方向：** RPD/RMD、vCMTS、1.2GHz/1.8GHz amps、FDX amps、D4.0 gateway、LLD/QoE software。

### 拐点三：BEAD 与 FTTH overbuild 进入采购，但瓶颈从 OLT 转向合规材料和施工

NTIA 数据显示 BEAD 已从审批推进到资金可用和 award agreement，2026 H2 会产生更多真实订单。但短期瓶颈不是 PON 芯片，而是 BABA 光缆、closures、cabinets、施工队、pole attachment、许可和项目融资。

**最可能放量子方向：** XGS-PON、remote OLT、预制光缆组件、closures/cabinets、施工软件、Calix/Adtran/Nokia 平台。

## 8. 2027 关键变化：3 个最可能拐点

### 拐点一：50G PON 从示范走向高价值商业化

2026 的 50G PON 更像“技术可信度建立年”，2027 才是商业化分水岭。若中国运营商、中东高端园区、Google Fiber/Nokia 生态和企业 SLA 同时推进，50G PON 可能提前形成 $6B-$12B 级两年订单池。若成本下降慢，则 25GS-PON 会吃掉一部分过渡需求。

**最可能放量子方向：** 50G OLT line card、50G ONU optics、50G FTTR、enterprise PON slicing、25G/50G combo card。

### 拐点二：DOCSIS 4.0 ESD/FDX 进入多运营商规模部署

Comcast FDX 扩围、Charter/Cox 交易后网络路线收敛、欧洲 cable operator 面对 fiber overbuild，将共同推动 D4.0 从“单一领先运营商”走向多运营商采购。2027 年 D4.0 的最大弹性不在 modem 数量，而在 amps、nodes、RPD、vCMTS、field meter 和认证服务。

**最可能放量子方向：** unified FDX/ESD chipset、1.8GHz ESD amps/taps、D4.0 RPD、vCMTS capacity license、D4.0 Wi-Fi 7/8 gateways。

### 拐点三：Wi-Fi 7 主流化与 Wi-Fi 8 预标准并行

2027 Wi-Fi 7 将成为 enterprise 和高端 residential 的默认采购，SP 6GHz/AFC 在场馆、教育和工业中更常见；同时 Wi-Fi 8 预标准样机开始进入高端试点。Wi-Fi 8 的投资点不是更高峰值，而是可靠性、漫游、mesh、拥塞环境和 AI QoE。

**最可能放量子方向：** Wi-Fi 7 AFC AP、AI/Cognitive WLAN、OpenRoaming/offload、Wi-Fi 8 early silicon、gateway NPU。

## 9. 头部公司与细分技术清单

### 9.1 PON / FTTH / 光接入

- **全球 OLT/PON 系统**：Huawei、ZTE、Nokia、FiberHome、Calix、Adtran、DZS、Ciena、Cisco、Ubiquiti、Tibit/Coherent PON transceiver ecosystem。
- **25G/50G PON**：Nokia、ZTE、Huawei、FiberHome、Calix、Adtran、Airoha、Sagemcom、Hitron、Evolution Digital、MT2、Broadcom/MaxLinear/Realtek/Airoha chipset ecosystem。
- **Remote OLT / distributed access fiber**：Vecima Entra、Harmonic、Adtran、Nokia、Calix、Casa legacy、Tibit/Coherent pluggable OLT。
- **ONT/HGS/CPE ODM**：Sercomm、Arcadyan、Vantiva、Sagemcom、Hitron、Technicolor/Vantiva、Gemtek、Zyxel、CIG、Foxconn/Accton ecosystem、TP-Link。
- **PON optics / BOSA / burst-mode components**：Hisense Broadband、Accelink、Lumentum、Coherent、Source Photonics、Innolight、中际旭创、新易盛、Eoptolink、Broadex、AOI、Fujitsu Optical Components、Sumitomo Electric、Furukawa。
- **FTTH passive / 光缆与连接**：Corning、Prysmian、CommScope、AFL、Clearfield、Belden、Panduit、YOFC、Hengtong、FiberHome、Fujikura、Sumitomo、Furukawa、Senko、US Conec、Huber+Suhner。

### 9.2 DOCSIS / Cable access

- **DOCSIS DAA / nodes / amps / RPD / vCCAP**：CommScope/Vistance Networks、Harmonic、Vecima、Cisco、Casa Systems legacy、Teleste、ATX Networks、Technetix、Gainspeed/Nokia legacy。
- **DOCSIS 4.0 chipset**：Broadcom、MaxLinear。
- **DOCSIS CPE / gateways**：Comcast XB10 ecosystem、Vantiva、Sercomm、Hitron、CommScope/Home Networks、Sagemcom、Ubee、Netgear、Arris legacy。
- **Cable software / vCMTS / orchestration**：Harmonic cOS、CommScope vCCAP、Vecima Entra vCMTS、CableLabs FMA/DAA ecosystem、OpenSync/RDK-B/prpl。
- **Cable test and field tools**：VIAVI、Keysight、Rohde & Schwarz、Anritsu、EXFO、VeEX、SCTE/CableLabs labs。

### 9.3 Wi-Fi 7 / Wi-Fi 8 / WLAN

- **Wi-Fi silicon**：Broadcom、Qualcomm、MediaTek、Airoha、MaxLinear、Realtek、NXP、Infineon、Synaptics、Celeno/Intel legacy。
- **Consumer/SMB Wi-Fi 7 routers/mesh**：TP-Link、Netgear、ASUS、Eero/Amazon、Ubiquiti、Linksys、Zyxel、D-Link、Xiaomi、Huawei、Honor。
- **Enterprise WLAN**：Cisco/Meraki、HPE Aruba、Huawei、Juniper Mist、Ubiquiti UniFi、Extreme Networks、CommScope Ruckus、TP-Link Omada、Fortinet、Cambium、Zyxel、EnGenius。
- **运营商托管 Wi-Fi / home platform**：Calix、Plume、Airties、OpenSync ecosystem、CommScope HomeVantage、Vantiva、Sagemcom、Assia/DZS CloudCheck、RouteThis、Cujo AI。
- **AFC / 6GHz / OpenRoaming**：Wi-Fi Alliance Services、Wireless Broadband Alliance、Federated Wireless、Comsearch/CommScope、Qualcomm AFC、Cisco/Meraki AFC、Broadcom ecosystem。

### 9.4 AI-native gateway / edge intelligence

- **AI gateway silicon/platform**：Qualcomm Networking Pro A7 Elite / Dragonwing、Broadcom AI access chipset、MediaTek Filogic/Airoha、MaxLinear Wi-Fi 7/Puma ecosystem。
- **运营商 AI/AIOps 平台**：Calix One、Plume、Juniper Mist AI、Cisco/Meraki AI、HPE Aruba Central、ExtremeCloud IQ、Huawei iMaster NCE、ZTE AI network solutions。
- **安全与家庭服务**：Cujo AI、F-Secure/Sense、Bitdefender BOX/operator security、Allot、Akamai/Guardicore、Cloudflare for families/zero trust edge。

## 10. 投资排序与风险

### 10.1 优先级排序

| 优先级 | 子方向 | 2026 确定性 | 2027 弹性 | 结论 |
|---:|---|---|---|---|
| 1 | Wi-Fi 7 enterprise/residential + cloud-managed Wi-Fi | 极高 | 高 | 已进入规模出货，AI/AIOps 提升软件毛利。 |
| 2 | XGS-PON + HGS 网关 | 极高 | 中高 | FTTH/BEAD/overbuild 主力，量大但硬件 ASP 有压力。 |
| 3 | DOCSIS high-split/DAA/vCMTS | 高 | 高 | Cable 运营商 2026 必做，D4.0 前置投资。 |
| 4 | DOCSIS 4.0 FDX/ESD ecosystem | 中高 | 极高 | 2026 Comcast 明确，2027 多运营商放量可能带来估值弹性。 |
| 5 | 25G/50G PON optics/line cards | 中 | 极高 | 2026 小批高毛利，2027 预期差大。 |
| 6 | AI-native gateway / AIOps platform | 中 | 极高 | 若运营商能把 AI 服务打包进 ARPU，是最高 ROIC 方向。 |
| 7 | BEAD passive materials/施工 | 中高 | 高 | 项目可见度上升，但受劳动力、合规和许可约束。 |

### 10.2 主要风险

1. **AI 流量不兑现为消费者/企业付费升级。** AI 数据中心 CapEx 很强，但家庭宽带 ARPU 不一定同步上行。
2. **内存涨价压缩 CPE 毛利。** DRAM/NAND 若继续紧张，低端网关/ONT/路由器最受伤。
3. **DOCSIS 4.0 认证与现场复杂度。** FDX/ESD 两路线、1.8GHz plant、legacy QAM、taps、amps、modem certification 会拖慢收入确认。
4. **50G PON 过早资本化。** 50G PON 技术成立，但 XGS-PON 已足够满足大多数家庭，50G 放量必须靠企业/园区/高端差异化。
5. **Wi-Fi 7 价格战。** Dell'Oro 已提示 Wi-Fi 7 初期价格异常低；若内存成本不能传导，AP 厂商毛利可能受压。
6. **BEAD 延迟。** 资金获批不等于施工开始，pole attachment、NEPA、BABA、州级合同和劳动力会把收入推到 2027。
7. **中国设备地缘限制。** 可能利好非中国厂商，但也会抬高成本、延长交期。

## 11. 可跟踪的 2026-2027 高频指标

1. Comcast DOCSIS 4.0 FDX availability 从百万 homes 到多百万 homes 的披露，以及 XB10/FDX gateway 供应。
2. Charter network evolution 的 quarterly CapEx 中 network evolution spending、1.2GHz/high-split 完成比例、1.8GHz/D4 采购信号。
3. CableLabs D4.0 Interop、Cable-Tec Expo 2026 中 FDX/ESD unified modem、RPD、vCMTS 认证数量。
4. Nokia、Calix、Adtran、Vecima 的 book-to-bill、BEAD 订单、gross margin 和 25G/50G PON 客户披露。
5. Wi-Fi 7 AP 出货、6GHz 客户端 attach、AFC 标准功率部署、enterprise WLAN 中 Wi-Fi 7 收入占比。
6. DRAM/NAND 合约价和 CPE 厂商 memory surcharge 是否被运营商接受。
7. 50G PON optics ASP、ONU 量产良率、BBF Plugfest 参与厂商和运营商试商用名单。
8. BEAD 项目 award agreement 后的采购公告、BABA 合规光缆交期、splicing crew 单价。

## 12. 来源索引

- Dell'Oro / PRNewswire, Broadband Access Equipment to Return to Growth in 2026: <https://www.prnewswire.com/news-releases/broadband-access-equipment-to-return-to-growth-in-2026-according-to-delloro-group-302709983.html>
- Electronics Weekly, broadband access forecast 2025-2030: <https://www.electronicsweekly.com/news/business/0-3-growth-2025-30-for-broadband-access-equipment-market-2026-01/>
- Fiber Broadband Association, 2025 FTTH deployment highs: <https://fiberbroadband.org/2025/12/16/fiber-broadband-association-reports-historic-fiber-deployment-highs/>
- NTIA BEAD Progress Dashboard: <https://www.ntia.gov/funding-programs/internet-all/broadband-equity-access-and-deployment-bead-program/progress-dashboard>
- CableLabs, DOCSIS technology 2026 update: <https://www.cablelabs.com/blog/docsis-technology-whats-changed-in-the-past-year-and-why-it-matters>
- CableLabs, DOCSIS 4.0 Interop security: <https://www.cablelabs.com/blog/authentication-and-privacy-docsis-4-0-interop-focuses-on-security>
- Comcast + Broadcom AI-powered access network / unified DOCSIS 4.0 chipset: <https://corporate.comcast.com/press/releases/comcast-broadcom-develop-ai-powered-access-network-pioneering-new-chipset>
- Comcast + CommScope DOCSIS 4.0 rollout milestone: <https://corporate.comcast.com/press/releases/comcast-commscope-notch-milestone-next-generation-connectivity-millions-across-us>
- CommScope DOCSIS 4.0 amplifiers: <https://commscopeholdingcompanyinc.gcs-web.com/news-releases/news-release-details/commscope-and-comcast-accelerate-rollout-docsis-40-amplifiers>
- Charter Q1 2026 results: <https://ir.charter.com/static-files/8f4715b9-1c59-4a03-8829-05e75fdbb368>
- Charter 2025 10-K: <https://www.sec.gov/Archives/edgar/data/0001091667/000109166726000017/chtr-20251231.htm>
- Wireless Broadband Alliance 2026 predictions: <https://wballiance.com/wireless-broadband-alliance-reveals-its-wi-fi-predictions-for-2026-and-beyond/>
- WBA Industry Report 2026 findings: <https://wballiance.com/wba-industry-report-2026-finds-62-of-survey-respondents-more-confident-to-invest-in-wi-fi-than-12-months-ago/>
- IDC enterprise WLAN Wi-Fi 7 blog: <https://www.idc.com/resource-center/blog/worldwide-enterprise-wlan-grew-13-9-driven-by-wi-fi-7-deployments/>
- Qualcomm Wi-Fi 7: <https://www.qualcomm.com/wi-fi/wi-fi-7>
- Qualcomm Networking Pro A7 Elite: <https://www.qualcomm.com/news/releases/2024/10/qualcomm-unveils-the-networking-pro-a7-elite-platform--the-first>
- Nokia 50G PON solution: <https://www.nokia.com/newsroom/nokia-unveils-worlds-first-50g-pon-solution-for-post-quantum-enterprise-connectivity/>
- Nokia Q1 2026 interim report: <https://www.nokia.com/newsroom/nokia-corporation-interim-report-for-q1-2026/>
- Nokia selected by altafiber: <https://www.nokia.com/about-us/news/releases/2026/01/19/nokia-selected-by-altafiber-for-fiber-network-expansion-across-ohio-and-hawaii/>
- ZTE + China Mobile 50G PON FMC community: <https://www.zte.com.cn/global/about/news/china-mobile-and-zte-take-the-lead-in-launching-a-50G-PON-based-FMC-residential-community-in-China.html>
- Broadband Forum PON Plugfest: <https://www.broadband-forum.org/news/record-vendor-turnout-powers-high-speed-fiber-device-compatibility/>
- Broadband Forum State of PON 2026: <https://www.broadband-forum.org/events/state-of-pon-2026-industry-reality-check-vbase-webinar/>
- Calix Q4 2025 shareholder letter: <https://investor-relations.calix.com/sec-filings/all-sec-filings/content/0001406666-26-000004/ex992stockholderletter25q4.htm>
- Calix Q1 2026 results: <https://www.stocktitan.net/sec-filings/CALX/8-k-calix-inc-reports-material-event-2c5a13d94a83.html>
- MaxLinear Wi-Fi 7 / Puma / broadband access demos: <https://www.maxlinear.com/news/press-releases/2024/maxlinear-highlights-leading-end-to-end-broadband-access-and-connectivity-solutions-with-low-power>
- TrendForce memory contract price pressure from AI servers: <https://www.trendforce.com/presscenter/news/20260331-12995.html>

---

非投资建议。本报告用于产业链研究和情景分析。关键不确定性包括 AI 应用流量兑现、运营商资本开支周期、CPE 内存成本、DOCSIS/PON 认证节奏、BEAD 施工延迟、地缘政治和设备价格竞争。
