# **行业调研：交换机与 AI fabric 网络芯片**

截至 2026-04-09

这份报告优先用最近半年、尤其 2026 年的官方发布、财报、联盟规范、论坛材料，再用 Dell’Oro、TrendForce、LightCounting、Cignal 做交叉验证；关于 2026–2027 年最大装机 AI 芯片家族与 NVIDIA 2026 路线图，我直接结合项目内材料。整体假设采用**偏乐观**的 2026 AI 基建情景。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

## **核心判断**

1. **2026 年最可能的主路径，不是 CPO 全面替代 pluggable，而是“102.4T 交换芯片 \+ 800G 规模出货 \+ 1.6T 开始爬坡 \+ SuperNIC/DPU 高 attach \+ 封闭 scale-up 仍主导”。** Dell’Oro 判断 AI back-end 交换机支出到 2030 年将超过 1000 亿美元，并认为长期看以太网会在 scale-up 与 scale-out 都成为赢家；到 3Q25，以太网已占 AI back-end 交换机销售额的三分之二以上。Broadcom 已把 102.4T TH6 推向多项、总规模超过 10 万 XPU 的部署；Cisco 也在推 102.4T 的 Silicon One G300。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))  
2. **2026 是 AI 网络从“交换机升级年”变成“体系结构定型年”的拐点。** 一边是 NVIDIA Rubin 平台把 Spectrum‑6、ConnectX‑9、BlueField‑4 和 photonics 拉成整套 AI factory；另一边是 UEC 1.0/1.0.2、UALink 2.0、OCP 的 ESUN/SUE 把开放标准从口号推到实现阶段。([Ultra Ethernet Consortium](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/))  
3. **最确定的放量方向是 Ethernet scale-out；最性感但没那么快的是 CPO；最值得埋伏的是开放 scale-up 与 memory-fabric。** LightCounting/Cignal/TrendForce 的方向高度一致：800G 在 2025–2026 是主力，1.6T 随后接棒；Google Ironwood 这类 OCS 架构会把 800G/1.6T 光需求再往上推；CPO 进入实质验证，但高量产仍晚于 pluggable。([LightCounting](https://www.lightcounting.com/storage/LC_Optical_Brochure.pdf))  
4. **投资上，长期高 ROIC/高毛利最可能留在“交换/互连主芯片 \+ SuperNIC/DPU \+ 光 DSP/控制芯片 \+ NOS/遥测软件”这一层。** 例子很直观：Credo 最新季度 GAAP 毛利率 68.5%，Arista 最新季度 non-GAAP 毛利率 63.4%；Cisco 则已把 hyperscaler AI 基础设施订单做到单季 21 亿美元。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

---

## **最近半年最值得盯的论坛、联盟与报告**

* **GTC 2026（3 月 16–19 日）**：Rubin、Spectrum‑6、BlueField‑4 STX、Spectrum‑X Photonics、Cisco × NVIDIA AI Factory。([NVIDIA](https://www.nvidia.com/gtc/conference-schedule/))  
* **OFC 2026（3 月 15–19 日）**：Broadcom TH6/TH6‑Davisson CPO、Marvell+Lumentum OCS、Arista XPO、Credo 1.6T AEC、Coherent/Ciena/Lumentum 的 400G/lane 与 CPO。([\*\*\*\*TODO optica \*\*\*\*](https://www.ofcconference.org/))  
* **UEC Member Summit 2026（4 月 27–29 日）**：已经从规范讨论进入 deployment / implementation planning。([Ultra Ethernet Consortium](https://ultraethernet.org/event/ultra-ethernet-consortium-member-summit-2026/))  
* **UALink 2.0（2026-04-07）**：新增 in-network compute、chiplet、manageability；白皮书明确写到**评估硬件预计在 2026 年晚些时候出现**。([Business Wire](https://www.businesswire.com/news/home/20260407620696/en/Ultra-Accelerator-Link-UALink-Consortium-Publishes-Four-Specifications-Defining-In-Network-Compute-Chiplets-Manageability-and-200G-Performance))  
* **OCP：ESUN/SUE / OCS / SONiC**：OCP Networking 项目页在 2026 年已把 ESUN、SUE-T、OCS 都列进主工作流。([Open Compute Project](https://www.opencompute.org/wiki/Networking?utm_source=chatgpt.com))  
* **第三方报告，建议并看**：Dell’Oro《AI Back-end Networks》、TrendForce 的 Google/Ironwood 互连与 AI 芯片跟踪、LightCounting《Optics for AI Clusters》、Cignal AI 的 OFC 与 datacom optics 报告。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

---

## **最近半年最重要的一手信号**

* **Broadcom**：TH6 是单芯片 102.4Tbps，官方说已规划多项部署，合计超过 10 万 XPU；TH6‑Davisson CPO 已出货。公司 FY26 Q1 AI 收入 84 亿美元，同比增长 106%，Q2 指引 AI 半导体收入 107 亿美元。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-ships-tomahawk-6-worlds-first-1024-tbps-switch))  
* **Cisco**：Silicon One G300 是 102.4Tbps，目标是 gigawatt-scale AI cluster；Cisco 还说 hyperscaler AI infrastructure orders 在 FY26 Q2 达到 21 亿美元。Cisco 与 NVIDIA 的 Secure AI Factory 里，Cisco 可以用 NVIDIA Spectrum-X 交换硅配 Cisco OS。([Cisco Newsroom](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m02/cisco-announces-new-silicon-one-g300.html?utm_source=chatgpt.com))  
* **Arista**：Meta 已部署 Arista 7700R4 DES 做以太网 AI 集群；Arista 2025 全年收入 90.06 亿美元，同比增长 28.6%；3 月又发布 XPO，单模块 12.8Tbps，面向 scale-up / scale-out / scale-across。([Arista Networks Blog](https://blogs.arista.com/blog/topic/martin-hull))  
* **Credo**：OFC 2026 现场演示 1.6T ZeroFlap AEC，直接对准 Vera Rubin NVL144 / Kyber Ultra NVL576；最新季度收入 4.07 亿美元，同比增长 201.5%。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-to-Showcase-Optical-Solutions-for-AI-Scale-Out-Fabrics-at-OFC-2026/default.aspx?utm_source=chatgpt.com))  
* **Astera Labs**：Scorpio X 系列把 in-network computing 做进 fabric switch；公司 2025 年收入 8.525 亿美元，同比增长 115%，并已开始某个 lead platform 的 Scorpio X 量产爬坡；同时和 Amazon 有交易/权证安排。([Astera Labs](https://ir.asteralabs.com/news-releases/news-release-details/astera-labs-broadens-scorpio-x-series-smart-fabric-switch?utm_source=chatgpt.com))  
* **NVIDIA 光互连链条**：NVIDIA 2026 年明确把 Spectrum‑X Ethernet Photonics 推到 2026；并与 Lumentum 签了多年度、含未来产能权利的战略协议，还向 Lumentum 投资 20 亿美元；与 Coherent 也签了多年度战略协议。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-spectrum-x-co-packaged-optics-networking-switches-ai-factories))  
* **Marvell**：已完成对 Celestial AI 的收购，又完成 XConn 收购，直接补强 Photonic Fabric、PCIe/CXL switch 和 UALink scale-up 团队；3 月还加入 NVIDIA NVLink Fusion，提供 custom XPU 和兼容 NVLink Fusion 的 scale-up 网络。([Marvell Technology](https://www.marvell.com/company/newsroom/marvell-completes-acquisition-of-celestial-ai.html))

---

## **A. 2026 年的机遇、挑战、已用技术与未来路径**

### **1）在 AI 计算中心大建设的 2026 年，这个行业的机会是什么**

项目内资料显示，2026–2027 年最大装机的 AI 芯片家族——Blackwell/Blackwell Ultra、Rubin、MI350/MI450、Trillium/Ironwood、Trainium2/3、Maia 200、MTIA、Ascend——都在向更大 pod、更高每 GPU 对外带宽、更重液冷/高压直流、更深 memory hierarchy 走。网络不再是“配件”，而是决定 token economics 的主变量。

机会主要有四个。第一，**AI back-end 网络从可选项变成集群成败项**：Cisco 甚至把网络改进和 job completion time 直接挂钩，称 G300 可把作业完成时间改善 28%；Broadcom TH6 则已经面向 10 万 XPU 级别部署。第二，**以太网主线越来越清晰**：Dell’Oro 认为长期看以太网会赢下 scale-up 和 scale-out；2025 年 3Q 的 AI back-end 交换机销售里，以太网已超过三分之二。第三，**光互连价值密度快速上升**：1.6T、400G/lane、XPO、CPO、OCS 都在 2026 同时推进。第四，**长期上下文 / agentic inference 让 memory-fabric 和 SuperNIC 变成新附加层**。([Cisco Newsroom](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m02/cisco-announces-new-silicon-one-g300.html?utm_source=chatgpt.com))

### **2）挑战是什么**

挑战也很集中。第一，**CPO 还没到“闭着眼上量”的阶段**：LightCounting 认为第一批 CPO 更可能先出现在愿意冒风险的小集群，高量产要等头部云厂真正点头；Arista 自己也明确说 OSFP 在 2026 仍会继续是最高量 form factor。第二，**多厂商 Ethernet AI fabric 的拥塞控制、故障域和运维复杂度，还没有像单厂封闭方案那样“傻瓜化”**。第三，**电力、液冷和 time-to-power 正在反过来决定网络形态**：OCP 2026 的 LVDC 白皮书就是为 AI 高密度机架准备的。([LightCounting](https://www.lightcounting.com/research-note/january-2026-cpo-waiting-for-green-light-from-customers-439))

### **3）2026 年现在真正在用的技术**

现在已经在生产环境里跑的，基本是四组：

* **Scale-out 主网**：RoCEv2/以太网 AI fabric 快速扩张，核心平台包括 Broadcom TH/Jericho、Cisco Silicon One、Arista Etherlink、NVIDIA Spectrum‑X；InfiniBand 仍在 NVIDIA 强势集群和 HPC 场景有很强黏性。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-ships-tomahawk-6-worlds-first-1024-tbps-switch))  
* **Scale-up**：2026 量产主流仍是**专有 scale-up**，即 NVLink/NVSwitch 一类；开放阵营则是 UALink 和 OCP 的 ESUN/SUE，但还处于规范成型、样机与设计导入阶段。([UALink Consortium](https://ualinkconsortium.org/wp-content/uploads/2026/01/UALink_White_Paper_Publication_Candidate_FINAL_VERSION.pdf))  
* **主机侧互连**：ConnectX‑9 / BlueField‑4、AMD Pollara / Vulcano、Cornelis CN6000、Enfabrica ACF‑S、Astera Scorpio 都在争抢 GPU/加速器旁边的高 attach 插槽。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-unveils-rubin-cpx-a-new-class-of-gpu-designed-for-massive-context-inference))  
* **光互连**：2026 仍以 800G pluggable/AEC 为主力，1.6T 进入实质 ramp，CPO/SiPh/OCS 从 demo 进入早期商用。([LightCounting](https://www.lightcounting.com/storage/LC_Optical_Brochure.pdf))

### **4）在 2026–2027 最大装机 AI 芯片背景下，我对新技术成熟/放量时间的判断**

下面是我的判断，不是公司指引：

| 技术 | 2026 状态 | 技术成熟时间 | 明显放量时间 | 我对其判断 |
| ----- | ----- | ----- | ----- | ----- |
| 102.4T AI 交换芯片 | 已量产/设计定型 | 已成熟 | 2026–2027 | 这是最确定主线 |
| 800G NIC / SuperNIC / DPU | 已量产 | 已成熟 | 2026–2027 | attach 率继续升 |
| 1.6T optics / 400G-lane DSP | 小批量到爬坡 | 2026H2 | 2027 | 2026 先在头部客户导入 |
| 液冷 pluggable / XPO | 工程样机到早期系统 | 2026–2027 | 2027 | 比 CPO 更容易先大规模商用 |
| CPO scale-out 交换 | 早期商用/有限出货 | 2026–2027 | 2027–2028 | 先小集群、后头部云 |
| 开放 scale-up：ESUN/SUE | 规范期 | 2027 | 2028 | 2026 是设计导入，不是放量年 |
| UALink 2.0 | 规范已出 | late‑2026 eval hardware | 2027–2028 | 2027 才开始看真系统 |
| CXL / AI memory fabric | 试点期 | 2026–2027 | 2027 | agent / 长上下文会推它加速 |

这个节奏的依据很直接：UALink 白皮书写到评估硬件预计 2026 年晚些时候出现；CPO 方面，LightCounting 认为高量产要等头部云给绿灯；而 Arista 又明确表示 2026 OSFP 仍会是最高量 form factor。([UALink Consortium](https://ualinkconsortium.org/wp-content/uploads/2026/01/UALink_White_Paper_Publication_Candidate_FINAL_VERSION.pdf))

### **5）这个行业 2026 年最可能的技术路径是什么**

**我给出的主判断是：**

**“以太网 scale-out \+ 封闭 scale-up \+ 800G 主放量 \+ 1.6T 起量 \+ CPO 试商用 \+ SuperNIC/DPU 高 attach”**

更细一点说：

* **大多数新增 AI 集群**：会走 102.4T Ethernet leaf/spine/AI back-end fabric，配 800G 光模块/AEC，逐步把 1.6T 插进去。  
* **单厂高端 scale-up 域**：2026 仍主要是 NVLink/NVSwitch 一类封闭方案；开放 scale-up 要到 2027 才有真正上量概率。  
* **光互连**：2026 先看 1.6T pluggable、XPO、AEC、LPO/linear；CPO 是 2027–2028 的更大弹性。  
* **推理新方向**：memory-fabric / SuperNIC / CXL attached memory 会先在长上下文、expert-parallel、agentic inference 里起量。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-ships-tomahawk-6-worlds-first-1024-tbps-switch))

---

## **B1. 关键产品分类，以及 2026–2027 市场规模与渗透率路径**

单位：**十亿美元（USD bn）**。这是**分层价值池**，**不能简单加总**。

这些数字是我的模型估算，校准锚点是：Dell’Oro 对 AI back-end switch 的长期支出轨迹、Broadcom AI networking 加速、Cisco hyperscaler AI 订单、Arista/Astera/Credo 的增长，以及项目内对 2026–2027 AI 芯片和资本开支的乐观主线。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

1. **AI 以太网 back-end 交换系统/芯片**  
   2026E：**16 / 24 / 32**  
   2027E：**23 / 35 / 48**  
   新增 AI back-end 渗透率 2026→2027：**62%→68% / 68%→76% / 74%→82%**  
   2026→2027 增长：**44% / 46% / 50%**  
   判断：最确定的大赛道，Broadcom/Cisco/Arista/NVIDIA 都会吃到。  
2. **InfiniBand 交换系统/芯片**  
   2026E：**9 / 12 / 15**  
   2027E：**10 / 13 / 17**  
   新增 AI back-end 渗透率 2026→2027：**26%→22% / 24%→20% / 22%→18%**  
   2026→2027 增长：**11% / 8% / 13%**  
   判断：绝对值仍增，但份额让给以太网。  
3. **NIC / SuperNIC / DPU / SmartNIC**  
   2026E：**11 / 17 / 24**  
   2027E：**17 / 27 / 38**  
   AI 服务器 attach 率 2026→2027：**68%→78% / 76%→86% / 82%→92%**  
   2026→2027 增长：**55% / 59% / 58%**  
   判断：这是 2026–2027 弹性最好的层之一。  
4. **光 DSP / AEC / retimer / gearbox**  
   2026E：**5 / 8 / 12**  
   2027E：**8 / 13 / 19**  
   新增 AI 光链路中 800G+ 占比 2026→2027：**58%→70% / 66%→80% / 72%→88%**  
   2026→2027 增长：**60% / 63% / 58%**  
   判断：Credo/Marvell/Broadcom 这一层利润率最好看。  
5. **Scale-up fabric / bridge / memory-fabric 芯片**  
   2026E：**1 / 3 / 5**  
   2027E：**2 / 5 / 8**  
   高端 AI rack 渗透率 2026→2027：**3%→6% / 6%→12% / 10%→18%**  
   2026→2027 增长：**100% / 67% / 60%**  
   判断：小池子，但很可能是 2027–2028 的大赔率方向。  
6. **CPO / silicon photonics / OCS 引擎**  
   2026E：**0.7 / 1.6 / 3.0**  
   2027E：**1.8 / 4.0 / 8.0**  
   AI switch port 渗透率 2026→2027：**0.5%→2% / 1.5%→5% / 3%→9%**  
   2026→2027 增长：**157% / 150% / 167%**  
   判断：2026 不是最大池子，但最容易被重新定价。

---

## **B2. 主流与新技术的市场规模与渗透率**

同样是**重叠口径，不能相加**。

1. **RoCEv2 / UEC 风格的 Ethernet scale-out fabric**  
   2026E：**20 / 30 / 40**；2027E：**30 / 45 / 60**  
   新增 AI pod 渗透率：**65%→72% / 72%→80% / 78%→85%**  
   这是 2026 的主干。  
2. **InfiniBand fabric**  
   2026E：**9 / 12 / 15**；2027E：**10 / 13 / 16**  
   新增 AI pod 渗透率：**20%→17% / 24%→20% / 23%→18%**  
   强但更集中于 NVIDIA 生态和少数极致训练/HPC 需求。  
3. **UALink 开放 scale-up**  
   2026E：**0.2 / 0.7 / 1.5**；2027E：**1.0 / 2.5 / 4.5**  
   新增高端 AI pod 渗透率：**0.5%→3% / 2%→7% / 4%→12%**  
   2026 更像“定标准和验硬件”，2027 才会看订单。  
4. **ESUN / SUE（开放 Ethernet scale-up）**  
   2026E：**0.3 / 0.9 / 1.8**；2027E：**1.2 / 3.0 / 5.0**  
   新增高端 AI pod 渗透率：**1%→4% / 3%→8% / 5%→12%**  
   中长期有潜力，但 2026 不是营收大年。  
5. **1.6T / 400G-lane 光互连**  
   2026E：**3 / 6 / 9**；2027E：**8 / 13 / 20**  
   新增 AI optical ports 渗透率：**8%→25% / 15%→40% / 22%→55%**  
   这是 2027 最明确的升级线。  
6. **CPO / NPO**  
   2026E：**0.8 / 1.8 / 3.2**；2027E：**2 / 5 / 8**  
   AI switch port 渗透率：**0.5%→2% / 1.5%→5% / 3%→9%**  
   叙事最强，但节奏慢于资本市场情绪。  
7. **CXL \+ RDMA AI memory fabric**  
   2026E：**0.5 / 1.2 / 2.2**；2027E：**1.5 / 3.5 / 6.0**  
   长上下文/agent inference rack 渗透率：**2%→8% / 5%→15% / 8%→22%**  
   这是被低估的“推理成本下降器”。

---

## **C. 供给侧：产能结构、瓶颈、成本与毛利**

### **1）产能结构：集中在哪里**

* **交换/网卡/retimer 主芯片**：设计能力集中在美国 fabless 与系统厂商——Broadcom、NVIDIA、Cisco、Marvell、AMD/Pensando、Astera、Credo；工艺正往 102.4T、224G SerDes、3nm/先进封装走，量产依赖极少数先进代工与封装生态。Broadcom 已公开 3nm 400G/lane DSP，Cisco 已公开 102.4T G300，Credo 1.6T AEC 也明确基于 3nm DSP。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next))  
* **光子与激光**：能力集中在 Lumentum、Coherent、Ciena/Nubis、Marvell/Celestial、Ayar、Lightmatter 这类少数玩家；NVIDIA 已用真金白银锁激光与光子产能。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/NVIDIA-Announces-Strategic-Partnership-With-Lumentum-to-Develop-State-of-the-Art-Optics-Technology/default.aspx))  
* **光模块/光封装/精密制造**：更多集中在东南亚/台湾链条，Fabrinet 这类先进光封装和精密制造平台的战略地位上升。([Fabrinet](https://investor.fabrinet.com/press-releases))  
* **系统集成**：Arista、Cisco、NVIDIA 以及 OCP/UEC 生态伙伴，决定了系统级交付和 NOS/遥测层。([Cisco Newsroom](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m03/cisco-secure-ai-factory-with-nvidia-GTC-2026.html?utm_source=chatgpt.com))

### **2）供给瓶颈：我认为至少有 8 个**

1. **200G/400G-lane SerDes 和 SI/PI 难度**：1.6T 与 204.8T 级别网络，把高速信号完整性推到新上限。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next))  
2. **高功率激光器/ELS/EML/VCSEL 供给**：NVIDIA 对 Lumentum/Coherent 的长期协议，本身就是“核心部件不够宽松”的证明。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/NVIDIA-Announces-Strategic-Partnership-With-Lumentum-to-Develop-State-of-the-Art-Optics-Technology/default.aspx))  
3. **CPO 封装良率与可维护性**：OFC 2026 讨论重心就是 CPO/ELSFP/OCS，说明量产问题还没彻底解决。([Cignal AI](https://cignal.ai/2026/03/ofc-2026-show-report/))  
4. **液冷光模块与交换机的可靠性认证**：XPO 和液冷交换机意味着新的冷板、密封、可换修标准。([Arista Networks](https://www.arista.com/en/company/news/press-release/23697-pr-20260311))  
5. **多厂商互操作与合规程序**：UEC 仍在实现/合规推进中；UALink 也才到下一版规范并计划后续互通测试。([Ultra Ethernet Consortium](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/))  
6. **AI fabric 软件与调优人才**：真正决定集群效率的，不只是带宽，而是 CLB、遥测、作业感知、失败恢复。Arista 甚至把 CLB 与 CV UNO 作为核心卖点。([Arista Networks](https://investors.arista.com/Communications/Press-Releases-and-Events/Press-Release-Detail/2026/Arista-Networks-Inc--Reports-Fourth-Quarter-and-Year-End-2025-Financial-Results/default.aspx))  
7. **站点电力/液冷/time-to-power**：OCP 2026 的 LVDC 白皮书就是为 AI 高密度机架准备的。([Open Compute Project](https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1?utm_source=chatgpt.com))  
8. **客户验证周期**：头部云厂不会轻易切掉主网，尤其是 scale-up；所以开放标准虽然热，但订单兑现会慢半拍。([UALink Consortium](https://ualinkconsortium.org/wp-content/uploads/2026/01/UALink_White_Paper_Publication_Candidate_FINAL_VERSION.pdf))

### **3）成本构成（我的估算）**

**102.4T AI 交换系统 BOM**，我给出一个可操作的估算框架：

* 交换芯片/主控硅：**22%–28%**  
* 光模块/AEC/电缆：**40%–55%**  
* PCB/背板/连接器：**6%–10%**  
* 电源/散热/液冷：**8%–14%**  
* 控制板/DDR/CPU/NOS 软件/装测：**10%–18%**

**800G SuperNIC / DPU 卡 BOM**：

* 主 ASIC：**35%–50%**  
* I/O 与 retimer/optics：**20%–35%**  
* PCB/供电/DDR：**15%–25%**  
* 软件/NRE/安全与管理 amortization：**10%–20%**

核心变化是：**越往 1.6T、CPO、液冷走，光和封装的价值占比越高；越往 job-aware fabric 走，软件和 SDK 的隐性 BOM 越高。** 这也是为什么 Cisco、Arista、NVIDIA 都在把网络写成“作业完成时间”和“AI factory”的一部分，而不只是 box。([Cisco Newsroom](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m02/cisco-announces-new-silicon-one-g300.html?utm_source=chatgpt.com))

### **4）毛利决定因素与价格传导**

* **高毛利决定因素**：SerDes/IP 难度、NOS/SDK、客户认证、系统可观测性、与 GPU/AI factory 的捆绑程度。Credo 68.5% GAAP 毛利率、Arista 63.4% non-GAAP 毛利率，说明真正高利润不在“铁盒子”，而在芯片 \+ 软件 \+ 认证。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))  
* **价格传导机制**：短期最容易传导的是 optics/laser；中期最有定价权的是 switch/NIC 主芯片；长期最稳的是 NOS/遥测/管理面软件。  
* **为什么能定价**：因为 10 万 GPU/XPU 集群里，网络效率掉 1% 的损失，往往远大于一台交换机贵 10% 的损失。Cisco 直接把 G300 与 28% 的 job completion 改善挂钩，本质就是在告诉客户：网络不是成本中心，而是算力释放器。([Cisco Newsroom](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m02/cisco-announces-new-silicon-one-g300.html?utm_source=chatgpt.com))

---

## **D. 竞争格局与壁垒**

### **1）市场结构：我给出的量化判断**

按公开部署、设计赢单和订单可见度，我的估算是：

* **AI Ethernet back-end 交换硅/系统**：CR3 大致 **75%–85%**，主导者是 **Broadcom \+ NVIDIA/Cisco \+ Arista/Marvell** 这一层。Dell’Oro 已经确认以太网在 AI back-end 销售里占比超过三分之二。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-networks-continue-their-shift-to-ethernet-now-accounting-for-over-two-thirds-of-3q-2025-switch-sales-in-ai-clusters/))  
* **InfiniBand / 封闭 scale-up**：接近 **NVIDIA 单极主导**。Rubin 平台把 NVLink 6、ConnectX‑9、Spectrum‑6 都放进整平台。  
* **光 DSP / AEC / 高速互连控制硅**：CR3 很高，我估算 **80%+**，前排是 **Credo / Broadcom / Marvell**。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))  
* **开放 scale-up**：还早，竞争分散，但 2026 的话语权集中在 **AMD、Astera、Marvell/XConn、Broadcom、Meta、Microsoft、OpenAI、Google** 这些共同参与规格的人手里。([Business Wire](https://www.businesswire.com/news/home/20260407620696/en/Ultra-Accelerator-Link-UALink-Consortium-Publishes-Four-Specifications-Defining-In-Network-Compute-Chiplets-Manageability-and-200G-Performance))

### **2）壁垒清单：为什么能定价**

* **技术壁垒**：102.4T/224G SerDes、拥塞控制、VOQ、公平调度、失败恢复都很难，且会直接影响训练效率。([Cisco Newsroom](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m02/cisco-announces-new-silicon-one-g300.html?utm_source=chatgpt.com))  
* **规模壁垒**：Broadcom 官方已经谈到 10 万 XPU 级部署；这不是小厂靠 PPT 就能切进来的。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-ships-tomahawk-6-worlds-first-1024-tbps-switch))  
* **渠道/客户锁定**：Meta 已用 Arista DES，Meta 和 Oracle 用 Spectrum‑X，Cisco 与 NVIDIA 合作 Secure AI Factory。客户一旦上车，下一代通常沿同栈扩。([Arista Networks Blog](https://blogs.arista.com/blog/topic/martin-hull))  
* **认证与标准壁垒**：UEC、UALink、OCP ESUN/SUE 的主导者，会天然提前获得实现经验和生态位置。([Ultra Ethernet Consortium](https://ultraethernet.org/ultra-ethernet-consortium-uec-launches-specification-1-0-transforming-ethernet-for-ai-and-hpc-at-scale/))  
* **切换成本**：网络 OS、collective tuning、布线、光模块、故障模型、运维工具全要改；对大集群来说，切换成本远高于单点 ASP 差异。

### **3）价值捕获：哪一层最可能长期高 ROIC / 高毛利**

我最看好三层：

1. **Merchant switch / SuperNIC / DPU 主芯片层**：最容易获得长期高 ROIC，因为它既吃速度代际升级，又吃软件/认证壁垒。  
2. **光 DSP / 控制芯片 / photonic engine**：如果 1.6T 和 CPO 持续兑现，这一层会拿到稀缺性溢价。  
3. **NOS / 遥测 / fabric 软件层**：最稳定，黏性最高，最不容易被 commodity 化。

相对不那么优的是：**纯白盒整机、低差异化模块装配、通用线缆**。它们会赚钱，但长期定价权较弱。

---

## **E. 2026 年最可能发生的 3 个拐点**

### **拐点 1：以太网正式坐实 AI back-end 主流**

我认为 2026 年最大的确定性变化，就是\*\*“以太网不再是挑战者，而是新增大集群的默认主网”\*\*。Dell’Oro 已经给出数据基础；Broadcom、Cisco、Arista、NVIDIA 都在把产品推进到 102.4T \+ 800G/1.6T 的组合。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-networks-continue-their-shift-to-ethernet-now-accounting-for-over-two-thirds-of-3q-2025-switch-sales-in-ai-clusters/))

### **拐点 2：1.6T / XPO / CPO 从“展台技术”变成“项目技术”**

2026 年不会是 CPO 全面放量年，但会是**1.6T 和新型光互连正式进入项目定版年**。Arista 的 XPO、Broadcom TH6‑Davisson、Marvell+Lumentum OCS、Credo 1.6T AEC、Ciena 6.4T CPX 光引擎，都说明这件事已经从讲故事走到工程样机。([Arista Networks](https://www.arista.com/en/company/news/press-release/23697-pr-20260311))

### **拐点 3：开放 scale-up 和 memory-fabric 从规范转向 eval hardware**

UALink 白皮书和 2.0 规范最关键的信号不是“更开放”，而是**硬件真的要出来了**；Enfabrica 的 EMFASYS、Astera 的 Scorpio X 说明“网络 \+ 内存”已经开始专门为长上下文/agent inference 做系统层优化。这个方向 2026 营收还小，但 2027 很可能快速放大。([UALink Consortium](https://ualinkconsortium.org/wp-content/uploads/2026/01/UALink_White_Paper_Publication_Candidate_FINAL_VERSION.pdf))

**2026 最可能放量的子方向，我排序是：**

1. **102.4T Ethernet AI back-end switches**  
2. **800G/1.6T optics \+ AEC/DSP**  
3. **SuperNIC / DPU / 智能主机侧互连**

---

## **F. 头部与代表性公司清单：上市状态、交易所、是否可在美股买到**

下面按“代表性 \+ 最近半年有公开技术/订单/论坛曝光”来列。上市/交易状态按公司 IR、官方交易信息和官方交易/收购公告核对。NVIDIA、Broadcom、Cisco、AMD、Arista、Astera、Credo、Lumentum、Coherent、Ciena、Fabrinet 目前都能在美股市场买到；Alphawave 已在 2025-12-19 从伦交所退市；Celestial AI 已于 2026-02 被 Marvell 完成收购；Enfabrica 在 2025-09 与 NVIDIA 完成交易。([NVIDIA Investor Relations](https://investor.nvidia.com/stock-info/stock-quote-and-chart/default.aspx))

### **1）交换芯片 / AI fabric / NIC / DPU / scale-up**

| 细分 | 公司 | 代表产品/技术 | 上市状态 | 交易所/代码 | 美股可买 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| AI Ethernet/Scale-out | Broadcom | Tomahawk 6、Jericho4、TH6-Davisson CPO、Thor Ultra AI NIC | 已上市 | Nasdaq / AVGO | 是 |
| AI Ethernet/InfiniBand/系统 | NVIDIA | Spectrum‑X、Spectrum‑6、Quantum、ConnectX‑9、BlueField‑4 | 已上市 | Nasdaq / NVDA | 是 |
| AI Ethernet/系统 | Cisco | Silicon One G300、Secure AI Factory with NVIDIA | 已上市 | Nasdaq / CSCO | 是 |
| AI Ethernet/定制互连 | Marvell | Teralynx、optical DSP、NVLink Fusion-compatible scale-up | 已上市 | Nasdaq / MRVL | 是 |
| AI 交换系统/NOS | Arista | Etherlink、7700R4 DES、XPO、EOS/CloudVision | 已上市 | NYSE / ANET | 是 |
| AI NIC/DPU | AMD（Pensando） | Pollara、Vulcano、开放 rack-scale AI networking | 已上市 | Nasdaq / AMD | 是 |
| Scale-up fabric / PCIe/CXL | Astera Labs | Scorpio P/X、Ares、Taurus | 已上市 | Nasdaq / ALAB | 是 |
| SuperNIC / memory fabric | Enfabrica | ACF‑S、EMFASYS | 私有/已与 NVIDIA 完成交易 | — | 否 |
| AI/HPC fabric | Cornelis Networks | CN5000、CN6000 SuperNIC | 私有 | — | 否 |

### **2）光互连 / AEC / DSP / CPO / 光器件**

| 细分 | 公司 | 代表产品/技术 | 上市状态 | 交易所/代码 | 美股可买 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| AEC / optical DSP | Credo | 1.6T ZeroFlap AEC、Cardinal/Robin DSP | 已上市 | Nasdaq / CRDO | 是 |
| DSP / optics / OCS | Marvell | Ara/Aquila 1.6T DSP、OCS、Celestial Photonic Fabric | 已上市 | Nasdaq / MRVL | 是 |
| 激光器 / 光器件 | Lumentum | 400G/lane 激光、1.6T DR4、CPO laser source | 已上市 | Nasdaq / LITE | 是 |
| 光器件 / CPO / 400G-lane | Coherent | 6.4T socketed CPO、1.6T/3.2T、InP-on-silicon | 已上市 | NYSE / COHR | 是 |
| 光引擎 / photonics / DCI | Ciena | Vesta 200 6.4T CPX、Hyper-Rail、Nubis | 已上市 | NYSE / CIEN | 是 |
| 光封装/精密制造 | Fabrinet | 先进光封装与 EMS | 已上市 | NYSE / FN | 是 |
| CPO / optical I/O | Ayar Labs | TeraPHY、AI scale-up CPO | 私有 | — | 否 |
| Photonic interconnect | Lightmatter | Passage、Guide、CPO/NPO/3D interposer 路线 | 私有 | — | 否 |
| Photonic Fabric | Celestial AI | Photonic Fabric | 已被 Marvell 收购 | — | 否（间接通过 MRVL） |
| 高速互连 IP / DSP | Alphawave Semi | 800G/1.6T UALink/UEC IP、DSP | 已退市 | 原 LSE / AWE | 否（已被 Qualcomm 收购） |

---

## **最后的投资判断**

**我对这个行业的结论偏多头，而且是结构性多头。**

最确定的是：  
**2026–2027 不会只有“GPU 更贵”这一条主线，而会同时出现“网络更值钱、光互连更值钱、SuperNIC/DPU 更值钱”的三条并行主线。**

在产业链里，我会把优先级排成：

* **确定性最高**：102.4T 交换芯片、AI Ethernet back-end fabric、800G host interconnect  
* **弹性最高**：1.6T DSP/AEC、液冷 optics、CPO 相关控制与光子引擎  
* **中长期赔率最高**：开放 scale-up、CXL/AI memory fabric、OCS/scale-across

一句话收束：

**2026 年最可能赚到大钱的，不是“讲 CPO 故事最多”的公司，而是“先把 102.4T Ethernet \+ 800G/1.6T \+ SuperNIC/DPU 这三件事真做成量”的公司；CPO 和开放 scale-up 更像 2027–2028 的第二波。**

下一步最自然的工作，是把这张产业链直接压成一版“美股可买标的池 \+ 未来 12 个月催化剂日历”。

According to a document from (2026-04-09).

# **行业调研：OCS（光路交换）**

下面把公开一手材料放在前面，把市场规模、渗透率、毛利和份额放在后面；后者是我在“2026–2027 AI 计算中心建设非常乐观”的前提下做的模型推演，不是公司指引。项目内材料已经把 2026–2027 的主流 AI 芯片/机架路线梳理得很清楚：Blackwell/GB300 仍是 2026 主出货平台，Rubin/Ultra 更像 2027 的方向定义者；2026 仍是 **HBM3E \+ 电互联 \+ 液冷大机架** 之年，2027 才更像 **HBM4/HBM4E \+ 更多自研 ASIC \+ 部分光化**。这直接决定了 OCS 在 2026 的最佳切入点是 **pod / spine / scale-out / scale-across 的外挂式可重构光层**，而不是 GPU 封装内标配。

## **先给总判断**

**第一，OCS 在 2026 已经不是“概念验证”，而是“头部客户架构定案 \+ 商用品开始兑现”的早期放量阶段。** Google 已把 OCS 明确写进 Ironwood TPU 的公开系统架构：多个 cube 通过 OCS 连接成 pod / superpod，故障时由 OCS fabric manager 绕过异常 cube 和链路；TPU7x 在 2026-03-31 GA，官方文档还把 OCS between cubes 的容错写成默认能力之一。与此同时，OCP 已成立 OCS 子项目，目标直指 open specs、SDN、telemetry、互操作和 AI 集群优化；OFC 2026 也把 OCS 放进 AI 数据中心专场 workshop 和 AI scale-up 专题里。([Google Cloud](https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack))

**第二，2026 最强的一手商业信号不是“论文更热”，而是订单、backlog、产能和生产部署。** Lumentum 在 2026-02-03 财报中披露 OCS backlog 已“well beyond $400 million”；Coherent 在 OFC 2026 投资者材料里写明 OCS 已有 **10+ customer engagements** 且 **shipping into production deployments**，并给出 2030 年 **$4B OCS SAM** 的口径；DiCon 说 2026 年单年计划交付 **3000+ matrix switch units**；HUBER+SUHNER/POLATIS 在 2025 年拿到 hyperscaler 多年大单，并在波兰新厂规划 **两年内至少 5 倍**产能提升。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

**第三，2026 最可能放量的不是“封装内光交换”，而是“高 radix 外置 OCS \+ OCS-aware 软件控制”。** OFC 官方专题明确写到：当前 AI scale-up 架构仍高度依赖高阶 PAM4 SerDes 和铜互连，真正的光化会先发生在超出单机架后的 scale-up / scale-out 域；而项目内材料同样判断 2026 主流仍是电互联，2027 才明显更光化。这意味着 2026 最现实的 OCS 技术路径，是 **Google 式 cube/pod/superpod 重构**、**spine replacement**、**AI cluster reconfiguration**，以及少量 rack-level / torus 试点，而不是全面替代 GPU 机架内部电互连。([\*\*\*\*TODO optica \*\*\*\*](https://www.ofcconference.org/program/special-events/symposia-next-generation-interconnects-for-ai-scale-up-systems/))

**第四，2027 会比 2026 更像 OCS 的“真正加速年”。** 原因不是 OCS 自身突然成熟，而是它周边的 1.6T / 3.2T 光模块、400G/lane DSP、NPO/CPO、以及更深层的 AI 工厂光网络会在 2026–2027 一起成熟。Broadcom 已发布 3nm 400G/lane optical DSP，为 1.6T 和后续 3.2T / 204.8T 网络铺路；NVIDIA 也把 Spectrum-X Ethernet Photonics 放到 2026 下半年商用窗口。OCS 不是 CPO 的替代品，而是更高层的 **topology reconfiguration layer**，两者大概率是互补关系。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next))

## **近半年最有信息增量的一手信号**

1. **2026-03-31，Google TPU7x GA**：公开确认 OCS 在 Ironwood superpod 中承担大规模重构和容错。([Google Cloud Documentation](https://docs.cloud.google.com/tpu/docs/release-notes))  
2. **2026-02-03，Lumentum Q2 FY26**：管理层披露 OCS backlog 超过 **$4 亿**。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))  
3. **2026-03-17，Coherent OFC 2026 briefing**：OCS 已进入生产部署，且客户拓展到 scale-up / scale-out / spine / scale-across。([Coherent Inc](https://www.coherent.com/content/dam/coherent/site/en/documents/investors/investor-presentations/2026/march-17/OFC-2026-Investor%20event-deck-vf.pdf))  
4. **2026-03-11，DiCon OFC 2026 发布**：宣布 300x300 / 64x64 新品，2026 计划交付 **3000+** 台矩阵交换设备，2027 上 **1024x1024**。([DiCon Fiberoptics](https://diconfiberoptics.com/news/news_2026_0311.php))  
5. **2026-03-16\~17，Molex / Accelink / Eoptolink / Marvell-Lumentum**：高 radix OCS、320x320 OCS、NX200/NX300、rack-level OCS demo 同时出现，说明 merchant 生态开始成形。([Molex](https://www.molex.com/en-us/products/optical-solutions/optical-circuit-switch))  
6. **2026-03-10\~03-12，iPronics / Salience / Oriole / Keysight / Tower**：SiPh OCS、32-port all-optical switch、nanosecond full-photonic fabric、专用测试环境和代工合作同时落地，说明新路线已从论文走向工程样机。([iPronics](https://ipronics.com/ipronics-to-showcase-programmable-photonics-leadership-at-ofc-2026/))

---

## **A. 2026–2027 的机遇、挑战、当前技术，以及最可能路径**

### **1）机遇**

OCS 的最大机遇来自三个共振。第一，AI 集群规模从“单 rack 很强”变成“跨 rack / 跨 pod / 跨 superpod 的大规模确定性流量”，Google 已公开证明 OCS 可以在这种环境里做重构、切片和容错。第二，OCP 与 OFC 的讨论焦点已经从“要不要 OCS”转向“如何标准化、如何做 SDN/telemetry、如何在 AI cluster 里用起来”。第三，头部厂商已经开始把 OCS 卖成 **提高 xPU 利用率、提高 availability、减少 OEO 与交换层级** 的系统收益，而不是单个 box。([Google Cloud](https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack))

### **2）挑战**

2026 的 OCS 也有四个硬约束。第一，**它不适合替换所有网络层**，更适合大象流、可预编排流、可切片训练/推理域。第二，**控制面比硬件更难**：Google 有 OCS fabric manager，OCP 也把 SDN、telemetry、互操作单独列成标准化范围。第三，**测试验证体系还不成熟**，这也是 Salience 和 Keysight 要专门做 OCS testing environment 的原因。第四，**CPO/NPO/1.6T/3.2T 演进太快**，OCS 供应商必须跟着更高带宽光层节奏一起爬坡。([Open Compute Project](https://www.opencompute.org/projects/optical-circuit-switching))

### **3）当前在用/在推的技术**

2026 公开材料里最清晰的技术分类，来自 Accelink：**MEMS、液晶/LCoS、压电/beam-steering、硅光 SiPh** 四条路线，其中它明确说 **MEMS 目前是主流**，原因是商业成熟度、插损和端口扩展性最好。成熟商用层里，Lumentum 用 MEMS 做 R300/R64；Molex 是 MEMS 高 radix 平台；DiCon 也是 3D MEMS；Calient 是 3D MEMS；POLATIS/HUBER+SUHNER 属于 beam-steering/DirectLight 路线；Coherent 则公开强调其 **liquid crystal** 路线“无运动部件、无高压器件”；新技术层里，iPronics、Salience、Oriole 则分别代表 SiPh OCS、all-optical SiPh switch、以及更激进的 full-photonic / passive-core 路线。([Accelink](https://www.accelink.com/en/lighting_your_dreams/2033420083430191105.html))

### **4）在“2026–2027 出货/装机最大的 AI 芯片家族”背景下，OCS 新技术的成熟与放量时间**

按项目内材料，2026–2027 的主流 AI 加速器家族大致仍是 **Blackwell / Blackwell Ultra、Rubin、AMD MI350 / MI450、TPU Trillium / Ironwood、Trainium2 / 3、Maia 200、MTIA 300→500、Ascend 910C / 950**。这些路线共同指向一个结论：**2026 最大量的互连矛盾仍发生在 rack 之外，而不是 rack 之内**。所以我的判断是：  
**MEMS / beam-steering 大 radix OCS：已经成熟，2026 有生产部署，2027 扩面放量；液晶 OCS：2026–2027 持续在特定账户渗透；SiPh OCS：2026 是样机/试商用/小规模 design-in，2027 才是更明显的收入爬坡；full-photonic / passive-core：2026–2027 仍以 PoC 和先行客户为主，真正量产更偏 2028+。** ([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

### **5）我认为 2026 最可能的技术路径**

**答案很明确：大型外置 MEMS / beam-steering OCS \+ SONiC/SDN 控制 \+ 800G/1.6T pluggables / NPO，先切 pod / spine / scale-out / scale-across。**  
不是封装内 OCS，不是全硅光一统天下，也不是所有 GPU 集群 2026 都全面上 OCS。真正最像 2026 主线的是：**Google 式 OCS fabric；Lumentum / Molex / POLATIS / DiCon / Accelink / Eoptolink 这类 merchant 设备；以及围绕它的 SONiC、gNMI、fabric manager、optical budgeting、spares/bypass 体系。** SiPh 是 2027–2028 的最强弹性方向，但 2026 的最大收入不会先落在它身上。([Google Cloud](https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack))

---

## **B1. 关键产品与 2026–2027 市场规模/渗透率**

公开口径里并没有统一的 audited 2026 OCS 市场数字，所以我用四个锚做模型：  
一是 Accelink 官方引用 Cignal AI，称 **2025 全球 OCS 约 $4 亿、2029 超过 $25 亿**；二是 Cignal 自己也把 **external OCS** 的 2029 预测提到 **\>$25 亿**，并提到 Google 已部署数万 OCS 端口；三是 Coherent 在 OFC 2026 给出 **2030 年 $40 亿 OCS SAM**；四是 LightCounting 估算 **AI cluster optics 2026 为 $260 亿**。再叠加 Google 公开落地、Lumentum backlog、Coherent production deployments、DiCon 3000+ units 等信号，我把 2026–2027 设成偏乐观情景。([Accelink](https://www.accelink.com/en/lighting_your_dreams/2033420083430191105.html))

口径定义：**渗透率 \= 新增大型 AI 集群（数千 xPU 级）中，至少部署一层 OCS 的占比。**  
下表是 **core OCS 市场**，不含广义全部 AI 光模块/CPO/NPO。

| 产品类别 | 2026 市场规模（保守 / 基准 / 乐观） | 2027 市场规模（保守 / 基准 / 乐观） | 基准渗透率路径 |
| ----- | ----- | ----- | ----- |
| 大 radix 外置 OCS（256x256–600x600+） | 2.8–3.6 / 4.0–5.8 / 5.5–7.5 亿美元 | 4.0–5.5 / 6.0–8.5 / 9.0–12.5 亿美元 | 2026：20–30% → 2027：35–50% |
| 中小 radix / rack-pod OCS（32x32–128x128） | 0.8–1.2 / 1.2–1.8 / 1.5–2.5 亿美元 | 1.0–1.6 / 1.8–2.8 / 2.8–4.0 亿美元 | 2026：8–15% → 2027：18–28% |
| OCS 控制软件 / NOS / telemetry | 0.2–0.3 / 0.4–0.6 / 0.5–0.8 亿美元 | 0.3–0.5 / 0.6–0.9 / 1.0–1.5 亿美元 | attach rate：70–85% → 85–95% |
| 关键器件（MEMS mirror / FAU / driver / PIC） | 0.7–1.0 / 1.0–1.6 / 1.4–2.2 亿美元 | 1.0–1.5 / 1.4–2.0 / 1.8–2.8 亿美元 | 基本随系统同步放量 |

这些产品映射到当下最有代表性的商用品，分别是：**Lumentum R300 / R64、Molex 544x544（roadmap 到 1000+）、POLATIS 384x384、Coherent 320x320、Calient S320、DiCon 300x300 / 64x64 / 600x600 / 1024x1024 roadmap、Accelink 320x320、Eoptolink NX200/NX300**；软件控制层则是 **Google OCS fabric manager、Lumentum/Molex 的 SONiC-based 控制、OCP OCS-SDN**。([Lumentum](https://www.lumentum.com/en/products/data-center/optical-circuit-switches))

---

## **B2. 主流技术与新技术的 2026–2027 市场规模/渗透率**

下面按**技术路线**拆，和上表不是严格相加口径。

| 技术路线 | 2026 市场规模（保守 / 基准 / 乐观） | 2027 市场规模（保守 / 基准 / 乐观） | 我的判断 |
| ----- | ----- | ----- | ----- |
| MEMS OCS | 2.5–3.5 / 3.8–5.5 / 5.5–8.0 亿美元 | 3.5–5.0 / 5.5–8.5 / 9.0–13.0 亿美元 | 2026 主流；2027 仍是最大收入池 |
| 压电 / beam-steering OCS | 0.5–0.8 / 0.8–1.2 / 1.0–1.8 亿美元 | 0.7–1.0 / 1.0–1.6 / 1.5–2.5 亿美元 | 成熟、可靠、客户集中，增速中高 |
| 液晶 / LCoS OCS | 0.4–0.7 / 0.6–1.0 / 0.8–1.4 亿美元 | 0.5–0.8 / 0.8–1.2 / 1.2–2.0 亿美元 | 可靠性叙事强，但客户更精选 |
| SiPh OCS | 0.2–0.5 / 0.4–0.8 / 0.8–1.5 亿美元 | 0.5–1.0 / 1.2–2.5 / 2.5–5.0 亿美元 | 2026 是验证/试商用；2027 弹性最大 |
| Full-photonic / passive-core / nanosecond fabrics | \<0.3 / 0.1–0.3 / 0.3–0.8 亿美元 | 0.2–0.5 / 0.5–1.0 / 1.0–2.0 亿美元 | 2026–2027 仍偏 PoC，长赔率方向 |

**技术渗透路径**我判断是：  
2026 新增 merchant OCS 装机里，MEMS 大约 **55–70%**，beam-steering **10–15%**，液晶 **8–12%**，SiPh **5–10%**；到 2027，MEMS 仍最大，但 SiPh 有望升到 **12–20%** 的 mix。这个判断的核心依据，是 Accelink 对 MEMS“当前主流”的官方表态、Coherent 对液晶路线的差异化定位、以及 iPronics / Salience / Oriole 在 2026 已经把 SiPh / full-photonic 从论文推进到 commercial showcase。([Accelink](https://www.accelink.com/en/lighting_your_dreams/2033420083430191105.html))

---

## **C. 供给侧：产能结构、瓶颈、成本与毛利**

### **1）产能结构**

如果只看 **成熟 merchant OCS**，产能和客户认证现在主要集中在 **美国 \+ 欧洲**：Lumentum、Coherent、Molex、DiCon、Calient、HUBER+SUHNER/POLATIS 是最可见的一层；**中国** 则在用垂直整合做追赶，Accelink 明确强调 MEMS mirror array \+ FAU 自研与高 volume 平台制造，Eoptolink 则把 OCS 与 NPO 一起推进；**SiPh OCS** 的制造重心更多依赖 Tower 这类 foundry 能力以及 Salience / Oriole / iPronics 这类新创。([Lumentum](https://www.lumentum.com/en/products/data-center/optical-circuit-switches))

### **2）我认为最关键的 8 个供给瓶颈**

第一是 **MEMS mirror array 芯片良率和一致性**；第二是 **FAU / microlens / 高密度耦合对准**；第三是 **高 radix 系统的自动校准、driver card、hot-swap serviceability**；第四是 **SiPh OCS 的测试验证环境**；第五是 **多厂商控制面/telemetry/SDN 互通**；第六是 **插损预算与长距离光功率余量**；第七是 **客户 qualification 周期**；第八是 **出货规模化能力**。这 8 个点都已经在公开材料里露头：Accelink 把 MEMS mirror 和 FAU 点名为两大核心器件；Molex 把 16 个 hot-swappable driver cards 和 SONiC-based NOS 当成卖点；OCP 专门把接口、SDN、telemetry、互操作列为标准化范围；Keysight/Salience 之所以要做首个 OCS testing environment，本身就说明测试还是短板。([Accelink](https://www.accelink.com/en/lighting_your_dreams/2033420083430191105.html))

### **3）成本、毛利和价格传导**

下面这组 BOM 是我的工程化估算，不是公司披露：**大 radix OCS 系统**里，光学核心（MEMS / beam-steering / LC / PIC）约占 **28–35%**，FAU / microlens / alignment **12–18%**，driver / control electronics **10–15%**，高密度 fiber / connector **8–12%**，机箱/电源/热设计 **8–10%**，校准/测试/老化 **8–12%**，软件/支持/质保 **8–12%**。这个拆分背后的逻辑，是公开产品页面都在强调 **光学核心、对准、driver cards、NOS、自动校准、低插损和 serviceability**，而不是钣金。([Molex](https://www.molex.com/en-us/products/optical-solutions/optical-circuit-switch))

毛利上，我偏向这样看：**成熟 merchant OCS 龙头**在放量后做到 **45–60% 毛利**是合理区间；**SiPh 新创**前两年更可能是 **20–40%**，等良率、测试和 qualification 打通以后，才有机会向 **40–55%** 靠拢。OCS 能定价，不是因为“端口贵”，而是因为它卖的是 **少一层电交换、少一轮 OEO、少一部分功耗和热、以及更高的 xPU 利用率和 uptime**。Coherent 已经直接把 OCS 的价值表述成 “software-defined topology reconfiguration to improve xPU utilization and availability”；Google 则公开把 OCS 用于 fault tolerance 和 slicing。([Coherent Inc](https://www.coherent.com/content/dam/coherent/site/en/documents/investors/investor-presentations/2026/march-17/OFC-2026-Investor%20event-deck-vf.pdf))

---

## **D. 竞争格局与壁垒**

### **1）市场结构**

如果只看 **merchant OCS 市场**，2026 我认为已经具备明显寡头特征：真正同时拥有 **公开产品、公开客户信号、公开规模化表态、公开控制栈** 的公司并不多。按公开 backlog / 订单 / 产能 / 已披露部署强度推，我估 **top3 约占 60–75%，top5 约占 80–90%**；Google 仍是最大的公开架构定义者，但它是 end-user / in-house route-setter，而不是 merchant box vendor。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

### **2）壁垒清单，以及“为什么能定价”**

**技术壁垒**：高 radix、低插损、可重复校准、可大规模部署，不是简单拼端口数。  
**规模壁垒**：Lumentum backlog、Huber 5x 扩产、DiCon 3000+ units，说明“会做”和“做得出来”差别很大。  
**客户锁定**：一旦接入 fabric manager、SONiC、gNMI、spares policy、scheduler，换供应商就不是换个 box，而是重做一层网络控制。  
**标准壁垒**：OCP 正在把 OCS-SDN、telemetry、互操作做成共同语义层；谁先通过这一层，谁更容易变成默认选项。  
**切换成本**：线缆、光预算、故障域、旁路策略、运维脚本、测试工具，全都和 OCS 供应商绑定。  
所以 OCS 能定价，不是“卖硬件单价”，而是“卖 AI fabric 的确定性收益”。([Open Compute Project](https://www.opencompute.org/projects/optical-circuit-switching))

### **3）价值链里谁最可能拿到长期高 ROIC / 高毛利**

我最看好的长期价值捕获层，不是最外层机箱，而是三块：  
**第一，光学交换核心**（MEMS / beam-steering / LC / PIC）；  
**第二，FAU / alignment / 校准 / 可靠性工艺**；  
**第三，控制软件与 telemetry**。  
原因很简单：这三层最难替代、最难认证、最能形成“越用越锁定”。相反，纯集成装配和通用机箱更容易被压价。([Molex](https://www.molex.com/en-us/products/optical-solutions/optical-circuit-switch))

---

## **E. 2026 最可能发生的 3 个拐点，以及最可能放量的子方向**

**拐点一：Google 把 OCS 从“内部黑箱”变成“公开架构范式”。**  
一旦 Google 公开 GA、公开 OCS superpod 拓扑、公开 fabric manager 与 fault bypass 逻辑，整个产业讨论就从“OCS 行不行”变成“别人什么时候学”。([Google Cloud](https://cloud.google.com/blog/products/compute/inside-the-ironwood-tpu-codesigned-ai-stack))

**拐点二：merchant 市场开始出现可见订单簿，而不是只有 demo。**  
Lumentum backlog \>$4 亿、Coherent 生产部署、DiCon 3000+ units、Huber 多年订单和扩产，说明 2026 不是“没人买”，而是“谁先交付、谁先吃份额”。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

**拐点三：SiPh OCS 从实验室走向早期商用。**  
iPronics 的 commercial SiPh OCS、Salience 的 32-port、Tower 的 at-scale 代工合作、Oriole 的 nanosecond full-photonic fabric，意味着 2026 已经是新路线的工程年；只是收入重心还不在这里。([iPronics](https://ipronics.com/ipronics-to-showcase-programmable-photonics-leadership-at-ofc-2026/))

**2026 最可能先放量的子方向**：  
我押注 **大型外置 OCS（spine replacement / scale-out / scale-across）**。  
**2026 增速最快但收入还不最大的子方向**：**32–64 port SiPh OCS / rack-level OCS 试点**。

---

## **F. 代表公司、上市情况、是否能在美股买到**

### **1）成熟 merchant OCS / 系统层**

**Lumentum**：NASDAQ: **LITE**，美股可直接买。  
**Coherent**：NYSE: **COHR**，美股可直接买。  
**HUBER+SUHNER / POLATIS**：瑞士 SIX: **HUBN**；美股主板没有对应主上市，公开行情站点显示存在 **OTC: HSSKF** 痕迹，但流动性和券商可得性要单独核对。  
**Molex**：未上市，2013 年被 Koch 收购。  
**DiCon Fiberoptics**：当前按未上市处理；SEC 旧文件显示其曾注销证券注册。  
**CALIENT**：官网未披露交易代码，按未上市处理。([Lumentum Investor Relations](https://investor.lumentum.com/overview/default.aspx))

### **2）中国 OCS / 器件与系统层**

**Accelink**：官方材料写明 **Stock Code: 002281**，深交所上市；不是美股主板标的，普通美股账户通常不能直接买。  
**Eoptolink**：官方 IR 写明 **SZSE: 300502**，深交所上市；同样不是美股主板标的。([Accelink](https://www.accelink.com/en/lighting_your_dreams/1740676786057711639.html))

### **3）SiPh / all-optical / 新技术层**

**iPronics**：官网未披露交易代码，按未上市处理。  
**Salience Labs**：官网未披露交易代码，按未上市处理。  
**Oriole Networks**：官网未披露交易代码，按未上市处理。([iPronics](https://ipronics.com/))

### **4）Foundry / test / 邻接可交易标的**

**Tower Semiconductor**：NASDAQ/TASE: **TSEM**，美股可直接买。  
**Keysight**：美股 **KEYS**，可直接买；它不是 OCS box 厂，但在 OCS testing environment 上是关键验证方。  
**Marvell**（MRVL）、**Broadcom**（AVGO）、**NVIDIA**（NVDA）、**Alphabet/Google**（GOOGL）、**Amazon**（AMZN）、**Microsoft**（MSFT）、**Meta**（META）都能在美股买到，但它们更像 **OCS 生态代理标的/架构定义方**，不是纯 OCS 收入公司。([Tower Semiconductor](https://towersemi.com/))

---

## **最后的投资判断**

如果你让我把 2026 的 OCS 投资逻辑压缩成一句话，我会说：

**OCS 不是 2026 AI 基建里最大的收入池，但很可能是最容易从“可选技术”变成“系统标配层”的小而快赛道之一。**  
2026 最值得押的是 **成熟 merchant OCS 龙头 \+ 光学核心/FAU/对准工艺 \+ 控制软件**；2027 开始再把更多赔率押给 **SiPh OCS / full-photonic fabric**。在非常乐观的 AI 基建情景下，我对 **core OCS 市场** 的基准判断是：**2026 年 6.6–9.8 亿美元，2027 年 9.8–14.2 亿美元**；乐观情景下，2027 可以看到 **14.6–20.8 亿美元**。真正决定上沿的，不是需求，而是 **交付、认证、控制面和测试体系**。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

According to a document from (2026-04-09)，结合项目内 AI 芯片/AI 工厂材料与最近半年公司公告、OFC 2026、OIF/IEEE 资料，我的核心判断是：\*\*2026 是 1.6T 可插拔光模块真正进入商业放量的第一年，但放量主角仍是 8×200G 电口、DSP 型 full‑retimed pluggable（FRO），以 OSFP 的 DR8、2×DR4、2×FR4 为主；TRO/LRO 会在 2026H2 开始吃份额，LPO 仍以局部场景和特定系统为主，400G/lane 属于 2026 的 demo/sampling 主线，真正大规模放量更偏 2027–2028。\*\*项目内材料已经把 2026–2027 的 AI 基础设施主线定义为 rack/pod/factory 化，并明确判断高阶光互连正在进入设计定案期，这与外部一手信息高度一致。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

如果站在投资角度，我偏乐观，但**更看好“上游差异化器件/DSP/激光和垂直一体化龙头”，而不是纯组装**。NVIDIA 在 2026 年直接给 Lumentum 和 Coherent 各投 20 亿美元，并绑定多亿美元级采购承诺，本质上已经说明：这个行业最稀缺的不是模组装配，而是 **InP 激光、CW 光源、200G/400G‑lane 光电器件与 224G/400G 信号链能力**。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology))

# **行业调研：1.6T 可插拔光模块（retimed）**

## **一、研究框架与最近半年高信号来源**

我把材料分成三层：**一手**看公司公告、官网、OFC 2026、OIF/IEEE；**二手**只拿来校验区间，主要看 Dell’Oro、Cignal AI、TrendForce、LightCounting；**模型推演**则在你要求的“对 2026 AI 基建偏乐观”前提下，给出保守/基准/乐观三情景。最近半年最值得看的公开来源，不是泛泛券商图表，而是 OFC 2026 的厂商发布、OIF 的 224G/RTLR 互操作、Cisco Live EMEA 2026 的 102.4T/1.6T 系统发布，以及 GTC 2026/Google Ironwood 把 photonics 和 OCS 提升到 AI factory 一层。二手校验里，我最重视 Dell’Oro（2027 年 AI back-end 端口以 1.6T 为主）、Cignal AI（2026 年 1.6T 模块超 500 万只）、TrendForce（Google 2026 年 800G+ 模块需求超 600 万只）和 LightCounting（2026 年产能可再翻倍、短缺缓和但可能出现阶段性错配）。([OIForum](https://www.oiforum.com/oif-demonstrates-industry-wide-interoperability-at-scale-at-ofc-2026-advancing-energy-efficiency-performance-and-capacity-for-ai-era-data-center-networks/))

最近半年最关键的一手/高信号消息，我认为有 9 条：

1. **AOI** 3 月 9 日拿到首个 1.6T 数据中心收发器量产订单，初始订单金额 **超过 2 亿美元**，计划 **2026Q3 开始出货、Q4 完成**；管理层还说到 2026 年底其全球 800G+1.6T 合并产能将超过 **50 万只/月**。这是真正意义上的量产信号。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))  
2. **Broadcom** 3 月 11 日发布 **Taurus BCM83640**，号称首个 **3nm 400G/lane optical PAM4 DSP**，直接把 1.6T pluggable 和后续 3.2T/204.8T 交换时代连起来。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next))  
3. **Marvell** 3 月 12 日明确表示 **Ara** 已经“**mass volume**”出货，同时推出首个 **8×200G TRO DSP（Ara T）**，Q1 2026 开始 sampling。说明半 retimed 不是 PPT，而是进入客户验证。([Marvell Technology, Inc.](https://investor.marvell.com/news-events/press-releases/detail/1013/marvell-ushers-in-the-1-6t-era-with-expanded-optical-dsp-platform-portfolio-redefining-ai-data-center-end-to-end-connectivity))  
4. **Cisco** 2 月 10 日把 **102.4T G300 系统、1.6T OSFP optics、800G LPO** 一起发布，直接把 1.6T optics 放进系统 BOM；Cisco 还明确声称 LPO 相比 retimed optics 可把模块功耗降约 **50%**。这既是机会，也是对 retimed 的定价压力。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx))  
5. **NVIDIA** 3 月 2 日与 **Lumentum / Coherent** 分别签多年的非独家战略合作，均包含 **multibillion purchase commitment** 和 **20 亿美元投资**；这说明上游激光/光源已经被当作战略产能来锁。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology))  
6. **Lumentum** 3 月 26 日宣布在北卡 Greensboro 建 **24 万平方英尺**新厂，做 InP 光器件，**mid‑2028** 爬坡；短期看不到新增产能释放，但这恰恰说明 2026–2027 的上游仍紧。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-New-U-S--Manufacturing-Facility-to-Produce-Advanced-Lasers-for-the-Worlds-Largest-AI-Data-Centers/default.aspx))  
7. **Source Photonics \+ Delta** 3 月 17 日在 OFC 现场做 **64×1.6T / 102.4T** live demo，Delta 交换机支持 **30W OSFP**，并支持 **LRO/LPO**。这是真正的系统级验证。([Source Photonics](https://www.sourcephotonics.com/news/source-photonics-and-delta-electronics-join-force-to-demo-1-6t-transceiver-and-switch-products-at-ofc26/))  
8. **Eoptolink** 3 月 12 日演示 **IMDD 400G/λ 的 1.6T DR4 OSFP**，3 月 13 日又发布 **6.4T NPO**。这说明 400G/lane 和 NPO 已经进入明确 roadmap，而不是空谈。([Eoptolink](https://www.eoptolink.com/news))  
9. **OIF** 在 2025 年 11 月已发布 **112G RTLR**，并在 OFC 2026 扩大展示 retimed、half-retimed、linear 的多厂互通；同时 **CEI‑224G‑Linear** 持续推进。说明半 retimed / linear 正在补标准和互操作，不再是散点方案。([OIForum](https://www.oiforum.com/oif-publishes-implementation-agreement-for-112-gb-s-retimed-transmitter-linear-receiver-rtlr-electrical-and-optical-interface-advancing-energy-efficiency/))

---

## **A. 2026 年的机遇、挑战、正在使用的技术，以及未来技术成熟/放量判断**

### **1）2026 年的机遇**

\*\*第一，AI 芯片从“单卡时代”进入“AI 工厂时代”，互连被提升为一级瓶颈。\*\*项目内材料已经把 2026–2027 的主线定义为 Blackwell/GB300→Rubin、Ironwood、Trainium、Maia、MTIA、MI350/450、Ascend 等系统级扩容，并明确指出 2026 是高阶光互连的设计定案年，而不是 CPO 全面爆发年。外部一手信息也一致：NVIDIA Rubin 把 Spectrum‑6/photonics 纳入 AI factory；Google Ironwood 通过 OCS 让系统从 9,216 芯片 pod 继续扩展到更大的光网络域。**这意味着 1.6T retimed 不是“锦上添花”，而是第一代大规模可交付的通用光层。**([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform))

\*\*第二，102.4T 交换机一上来，1.6T 就成了最自然的端口速度。\*\*Dell’Oro 明确说 AI back-end 网络中，端口已经大规模转向 800G，并预计 **2027 年以 1.6T 为主**；Cisco 的 G300、Delta 的 64×1.6T、Broadcom Taurus 都是在给 102.4T / 1RU 或 1 台固定系统时代做准备。也就是说，**1.6T retimed 的大行情不是因为模块厂“想卖更贵”，而是因为交换芯片/系统平台升级把它变成了默认档位。**([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

\*\*第三，retimed 仍是 2026 年采购最安全的路线。\*\*原因很简单：224G/1.6T 是第一波真实大规模部署，系统商和 hyperscaler 最先关心的是 bring‑up、BER、遥测、兼容性和维护，而不是把最后几瓦都省掉。Marvell 的 Ara 已经 mass volume，AOI 已经拿到量产订单，Broadcom Taurus 也进入 sampling；相比之下，LPO/linear 的确更省电，但把更多 SI/PI 和 FEC 风险转移给 host ASIC、板级材料和系统验证。**在“先把网络点亮”这个优先级下，retimed 最像 2026 年的主流。**([Marvell Technology, Inc.](https://investor.marvell.com/news-events/press-releases/detail/1013/marvell-ushers-in-the-1-6t-era-with-expanded-optical-dsp-platform-portfolio-redefining-ai-data-center-end-to-end-connectivity))

\*\*第四，上游战略锁产能让 1.6T 放量确定性提升。\*\*NVIDIA 同时绑定 Lumentum 和 Coherent，并且 TrendForce 明确说供给链关注点正从模块装配转向 **InP 激光和高功率 CW 光源**。这等于告诉市场：2026 的真正“交付约束”被识别出来了，而且头部买家已经开始出手解决。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology))

### **2）2026 年的挑战**

\*\*第一，224G/1.6T 的标准与互操作仍在“收口”，不是完全尘埃落定。\*\*OIF 的 112G RTLR 已经发布，但 224G linear 仍在持续推进；Cisco 在 2026 年的材料里写到 IEEE 802.3dj 正在 public ballot 进程中，并预计 **2026 年 9 月**批准，而 2025 年 IEEE 文件曾给出 **2026 年 8 月**送 ratification 的目标。换句话说，**标准方向很清晰，但 2026 仍是工程化、验证和生态收口之年。**([OIForum](https://www.oiforum.com/oif-publishes-implementation-agreement-for-112-gb-s-retimed-transmitter-linear-receiver-rtlr-electrical-and-optical-interface-advancing-energy-efficiency/))

\*\*第二，功耗/热设计会压缩 retimed 的份额和毛利。\*\*Lumentum 的 1.6T TRO 2×DR4 模块给到 **16W** 这个非常有吸引力的数字；Cisco 则直接说 LPO 比 retimed 模块可省约 **50% 模块功耗**、约 **30% switch power**。这意味着 2026 年 retimed 会继续拿量，但从 2027 年开始，它的 ASP 和份额都会受到 TRO/LRO/LPO 的双重压力。([Lumentum](https://www.lumentum.com/en/products/16t-2dr4-tro-osfp-transceiver-module))

\*\*第三，上游瓶颈不在模组产线，而在激光、PIC、MEMS 和 224G 信号链。\*\*TrendForce 认为 2026–2028 的紧张和盈利，主要取决于 **lasers 与 MEMS 的可用产能和良率**；Lumentum、Coherent、Source 等都在 OFC 2026 把 200G/400G 的激光、EML、CW 光源放在核心展示位。([TrendForce](https://img.trendforce.com/Report/2026/03/20260316_141005_RP260226OS_preview.pdf))

**第四，价格风险比 2024–2025 更大。LightCounting 在 2026 年 3 月已经提示：以太网光模块短缺在缓解，行业“有能力在 2026 年把销售再翻一倍”，但产能也可能超过客户真实需要。对投资人来说，这意味着量会涨，但 generic assembly 的 ASP/毛利不一定同步涨。**([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382?utm_source=chatgpt.com))

### **3）2026 年实际在用的技术**

今天真正被使用的不是单一路线，而是一个分层栈：\*\*800G retimed OSFP/QSFP‑DD 仍是大底座；1.6T full‑retimed（DR8、2×DR4、2×FR4、2×LR4）开始进入量产/早期部署；TRO/LRO/RTLR 在客户验证；LPO 在特定系统推进；AEC/ACC/AOC 继续吃很短距离；Google 这类架构在 inter‑rack 层已经把 OCS 作为现实方案。\*\*form factor 上，OSFP 和 QSFP‑DD1600 都存在，但 2026 年与 AI scale‑out 最相关的高信号发布明显更偏 OSFP；OSFP MSA 本身也强调 8 lane 到 1.6T、1U 可做到 36 ports。([OSFPmsa](https://osfpmsa.org/))

一个很重要但常被忽略的现实是：\*\*1.6T 光模块不会和 AI 芯片出货量 1:1 线性增长。\*\*在 OCS 架构里，短距仍会大量用铜或 AEC/ACC，TrendForce 对 Google 的判断就是“短距靠高速铜，机架间靠全光网络”；MACOM 在 OFC 2026 的 live demo 也把 retimed optics、low‑power ACC 和 LPO 一起摆进 102.4T switch 生态。**所以，真正吃到最多钱的是“需要 reach \+ 需要低 BER \+ 需要快速 bring‑up”的那部分 1.6T 端口。**([TrendForce](https://www.trendforce.com/presscenter/news/20260210-12919.html))

### **4）新技术成熟时间、放量时间：我的判断**

| 技术路径 | 2026 状态 | 成熟时间 | 放量时间 | 我的判断 |
| ----- | ----- | ----- | ----- | ----- |
| 200G/lane FRO（full-retimed） | 商业化爬坡 | 已成熟 | 2026H2–2027 | **2026 主线** |
| 200G/lane TRO/LRO/RTLR | 客户验证/小批 | 2026H2 | 2027 | **2027 最快增量** |
| 200G/lane LPO / full linear | 小批导入 | 2027 | 2027–2028 | 2026 仍非主流 |
| 400G/lane IMDD（1.6T DR4/未来 3.2T） | demo/sampling | 2027 | 2027–2028 | 是“下一代确定方向” |
| OCS（scale-across） | 头部客户落地 | 2026 | 2027 | 与 1.6T pluggable 共振，不是替代 |
| NPO/CPO/XPO | 设计定案/样机 | 2027 | 2028+ | 2026 不是它的量产年 |

这个时间表的约束条件很明确：Broadcom 2026 还是在 sample 400G/lane Taurus；Marvell 的 Ara 已经量产但 Ara T/X 仍是 2026 Q1 sampling；OIF 的 224G Linear 还在推进；Cisco、Semtech、Lumentum 都在 2026 把 linear/TRO 推到产品化，但 Source 和 Eoptolink 同时又在现场展示 400G/λ 与 NPO/XPO，说明行业并不是“一个方向赢、其他都死”，而是**2026 以 FRO 放量、2027 以 half‑retimed/linear 加速、2028+ 再看 NPO/CPO/XPO 真正吞吐**。([Marvell Technology, Inc.](https://investor.marvell.com/news-events/press-releases/detail/1013/marvell-ushers-in-the-1-6t-era-with-expanded-optical-dsp-platform-portfolio-redefining-ai-data-center-end-to-end-connectivity))

### **5）A 的结论：2026 最可能的技术路径是什么？**

\*\*最可能的路径就是：102.4T switch \+ 8×200G electrical \+ OSFP 1.6T full‑retimed optics（以 2×DR4、2×FR4、DR8 为主）+ 短距 copper/AEC 补充 \+ 少量 OCS 做 scale‑across。\*\*我不认为 2026 会是 CPO 或全线 LPO 的年份；我认为 2026 是 **retimed 拿量、half‑retimed/linear 开始进入客户预算、400G/lane 抢先卡位** 的年份。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

---

## **B1. 按产品类别拆分：2026–2027 市场规模与渗透率路径**

**单位：亿美元；以下是我的模型估算，不是公司指引。**

| 产品类别 | 2026E（保守/基准/乐观） | 2027E（保守/基准/乐观） | 基准份额路径 | 备注 |
| ----- | ----- | ----- | ----- | ----- |
| 1.6T DR8 / SR8 / 2VR4 | 10 / 18 / 26 | 15 / 26 / 38 | 24% → 24% | 近距、机架内/邻近机架、AOC/VCSEL/短单模补位 |
| 1.6T 2×DR4 | 18 / 30 / 46 | 26 / 42 / 64 | 41% → 39% | **2026 最主流 SKU** |
| 1.6T 2×FR4 | 12 / 22 / 34 | 20 / 33 / 52 | 30% → 31% | 行/列/房间级互连最吃香 |
| 1.6T 2×LR4 / 更长距单模 | 2 / 4 / 8 | 3 / 6 / 12 | 5% → 6% | 小而稳，更多偏 scale-across / DCI 邻近场景 |
| **纯 1.6T 光模块合计** | **42 / 74 / 114** | **64 / 107 / 166** | — | 行业主市场 |

这张表的底层约束是四个事实：Cignal AI 预计 **2026 年 1.6T 模块超过 500 万只**；Dell’Oro 预计 **2027 年 AI back-end 端口以 1.6T 为主**；TrendForce 预计 Google 2026 年 **800G+ 模块需求超 600 万只**；LightCounting 则提示 2026 年行业产能可继续放大但短缺趋缓。换成投资语言：**需求已经足够大，问题只在 2026 是不是全部兑现。**([Cignal AI](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/))

我的基准判断是：\*\*2×DR4 和 2×FR4 是 2026–2027 最值得盯的两个 SKU 方向。\*\*DR8/2VR4 更像“近距/过渡层”，2×LR4 是小众但利润不差。若按基准情形看，**纯 1.6T 光模块市场 2027 年相对 2026 年大约还能再长 40%–50%**。这是在 ASP 下行的情况下仍能成立的增长。

---

## **B2. 按技术路径拆分：2026–2027 市场规模与渗透率路径**

**这一表与上表有重叠，不能横向相加。单位：亿美元。**

| 技术路径 | 2026E（保守/基准/乐观） | 2027E（保守/基准/乐观） | 基准渗透路径 | 备注 |
| ----- | ----- | ----- | ----- | ----- |
| 200G/lane FRO（full-retimed） | 30 / 58 / 82 | 35 / 68 / 96 | 78% → 64% | **2026 主流**，2027 仍是最大池子 |
| 200G/lane TRO/LRO/RTLR | 4 / 10 / 18 | 10 / 24 / 40 | 14% → 22% | **2027 最快成长** |
| 200G/lane LPO / full linear | 1 / 6 / 14 | 6 / 15 / 30 | 8% → 14% | 受 host/system 能力限制 |
| 400G/lane IMDD | 1 / 3 / 7 | 5 / 15 / 32 | 4% → 14% | 2026 样机/小样，2027 快增 |
| OCS（相关系统与光交换） | 3 / 8 / 15 | 7 / 16 / 28 | 20% → 35%\* | \*指新建 hyperscale AI superpod 采用率 |
| NPO/CPO/XPO | 1 / 2 / 5 | 3 / 8 / 15 | 3% → 8%\* | \*指新建 102.4T+ 高密度平台采用率 |

这张表的约束来自几条非常明确的产业路径：Marvell 的 **Ara 已量产、Ara T 开始 sampling**；Broadcom 的 **400G/lane Taurus** 已 sampling；OIF 的 **RTLR/224G Linear** 正在补 interoperable 生态；Cisco 正在把 **LPO** 放进实际系统；Lumentum 已有 **16W TRO 1.6T 2×DR4** 产品；Source/Eoptolink 则把 **400G/λ、NPO/XPO** 摆上 OFC。**所以 2026 的技术判断不是“线性会不会来”，而是“线性会先吃掉多少份额”。**([Marvell Technology, Inc.](https://investor.marvell.com/news-events/press-releases/detail/1013/marvell-ushers-in-the-1-6t-era-with-expanded-optical-dsp-platform-portfolio-redefining-ai-data-center-end-to-end-connectivity))

我的基准情形里，\*\*2026→2027：FRO 仍增长，但份额下滑；TRO/LRO 翻倍以上；LPO 翻倍以上；400G/lane 从“技术概念”进入“客户真预算”。\*\*这也是为什么我认为 2026–2027 最好的投资，不是去赌“retimed 永远不被替代”，而是去赌 **retimed 龙头能否平滑切到 half‑retimed/400G‑lane 新周期**。

---

## **C. 供给侧：产能结构、瓶颈、成本与毛利**

### **1）产能结构：主要集中在哪些地区/公司/工艺**

\*\*模块装配主产能仍然集中在中国大陆 \+ 东南亚（尤其泰国）+ 台湾，少量高附加值/战略产能向美国回流。\*\*InnoLight 公开写到其生产基地在 **苏州、台湾、泰国**；AOI 的工程和制造布局在 **德州 Sugar Land、台北、宁波**；Eoptolink 官网给出 **成都总部 \+ 泰国基地 \+ 美国销售**；Lumentum 则在美国新建 InP 产线。换句话说，**模组量产在亚洲，关键光源和一部分战略器件在美国补链**。([Tower Semiconductor](https://towersemi.com/2023/09/07/09072323/))

\*\*工艺上，2026 的关键不是“谁会装模块”，而是谁能把 224G/200G-lane 信号链、EML/SiPh/PIC、激光器、热管理和 burn‑in 一起做成量产品。\*\*Broadcom 和 Marvell 负责高端 DSP/gearbox；Coherent/Lumentum/Source/Eoptolink/MACOM/Semtech 在 EML、CW laser、PIC、TIA/driver 上形成核心分工；Cisco、Delta、Google、NVIDIA 则把这些器件拉进 102.4T 系统和 OCS/AI factory 架构。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next))

### **2）我认为 2026–2027 最关键的 8 个供给瓶颈**

1. \*\*InP 激光与高功率 CW 光源产能。\*\*NVIDIA 对 Lumentum/Coherent 的投资，TrendForce 对 InP/CW 的点名，已经说明这是最硬瓶颈。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology))  
2. \*\*200G/lane DSP / 224G SI/PI 良率与互操作。\*\*Taurus 还在 sampling，Ara T/X 也只是 2026 Q1 sampling。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next))  
3. \*\*MEMS/OCS 良率和供给。\*\*TrendForce 明说 2026–2028 的 tightness/profitability 很大程度由 lasers 和 MEMS 决定。([TrendForce](https://img.trendforce.com/Report/2026/03/20260316_141005_RP260226OS_preview.pdf))  
4. \*\*热设计与模块功耗。\*\*Delta 的 102.4T 交换机把 OSFP 上限做到 **30W**，已经说明 1.6T optics 进入高热密度区。([Source Photonics](https://www.sourcephotonics.com/news/source-photonics-and-delta-electronics-join-force-to-demo-1-6t-transceiver-and-switch-products-at-ofc26/))  
5. \*\*板级材料/超低损耗 PCB/连接器。\*\*224G 时代把 host‑to‑module trace 和板材从“配件”变成成败因素；Cisco、Delta、OIF 都在强调 advanced materials / VSR/LR objective。([Source Photonics](https://www.sourcephotonics.com/news/source-photonics-and-delta-electronics-join-force-to-demo-1-6t-transceiver-and-switch-products-at-ofc26/))  
6. \*\*标准/认证/客户资格周期。\*\*802.3dj、RTLR、224G Linear 虽已明确，但 2026 仍在收口。([ciscolive.com](https://www.ciscolive.com/c/dam/r/ciscolive/emea/docs/2026/pdf/CISCOU-2238.pdf))  
7. \*\*测试与 burn‑in。\*\*1.6T/224G 让测试复杂度上升，Keysight 在 OFC 2026 专门把“1.6T 可靠性验证”单独拎出来。([Keysight United States](https://www.keysight.com/us/en/cmp/optical-networking-innovations.html))  
8. \*\*交付节奏与第二来源认证。\*\*LightCounting 已提示 2026 的风险从“没有货”部分转向“供给结构与真实需求是否匹配”。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382?utm_source=chatgpt.com))

### **3）成本构成、毛利决定因素、价格传导**

\*\*典型 1.6T retimed 模块的 BOM，我更愿意把它看成六块：\*\*DSP/gearbox（约 20–28%）、光器件与光引擎（EML/SiPh/PIC/TIA/driver/PD，约 35–45%）、封装/对准/耦合（10–15%）、外壳/散热/电源管理（8–12%）、测试与 burn‑in（8–12%）、制造损耗与良率折损（5–10%）。\*\*TRO/LRO 的本质，是拿掉一部分 DSP 成本和功耗；LPO 则进一步拿掉 DSP，但把代价转移到 host ASIC、板材、验证和系统调优。\*\*Lumentum 的 16W TRO、Cisco 对 LPO 的功耗表述，都在证明“功耗/热/验证”已成为 BOM 分配器。([Lumentum](https://www.lumentum.com/en/products/16t-2dr4-tro-osfp-transceiver-module))

\*\*毛利最受四个因素决定：\*\*第一是上游器件自给率，尤其激光/PIC/TIA/driver；第二是 hyperscaler qualification 的深度；第三是良率与返修率；第四是 SKU mix（2×DR4/2×FR4 通常比通用短距更有议价）。\*\*价格传导机制通常是“上游稀缺先涨价、模块后提价；一旦二供通过，模块 ASP 先掉，上游差异化器件掉得慢”。\*\*因此长期看，纯 assembly 的毛利波动最大，垂直一体化和关键器件层更稳。

---

## **D. 竞争格局与壁垒（可量化）**

\*\*我的估算：2026 年全球 1.6T AI 数据中心光模块市场，CR3 大约在 55%–70%，CR5 大约在 75%–85%；到 2027 年集中度会略降，但仍将显著高于传统低速光模块。\*\*理由不是神秘，而是 hyperscaler 资格认证、DSP/laser 供给和系统互操作都让“二供”很难一夜之间补齐。Cignal AI 也已在 800G 维度看到 Innolight、Eoptolink、Coherent 等龙头领先，而 TrendForce 对 Google 的判断甚至给出 Innolight \+ Eoptolink 接近 **80%** 的 800G+ 订单份额。**1.6T 不会完全复制 800G，但集中度只会更高，不会更低。**([Cignal AI](https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/))

**这个行业真正的壁垒，不是“会不会做光模块”，而是以下 6 条：**

1. \*\*224G/200G‑lane 信号完整性壁垒。\*\*224G 一旦 BER、FEC、latency 不稳定，损失的是整簇 GPU 利用率，不是一个模块返修费。  
2. \*\*客户资格壁垒。\*\*AI back-end 网络容错成本极高，一旦某家模块通过验证，客户不愿轻易更换。  
3. \*\*上游器件壁垒。\*\*InP 激光、CW 光源、EML/PIC、DSP 才是真正稀缺层。  
4. \*\*规模制造壁垒。\*\*烧机、老化、批次一致性、返修数据库都需要时间积累。  
5. \*\*系统/遥测/CMIS 壁垒。\*\*AI 网络越来越需要可观测、可调优的 optics，不是“能亮就行”。  
6. \*\*切换成本壁垒。\*\*模块一旦和特定 switch/NIC/板材/线缆/FEC 组合绑定，替换成本高于表面模块价差。

这些壁垒共同解释了**为什么能定价**：因为 AI back-end 网络里，**宕机和 tail latency 的代价远高于每只模块多花的几十到几百美元**。这也是 retimed 在 2026 仍能拿到高份额的根本原因。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

\*\*长期高 ROIC/高毛利最可能落在两层：\*\*一层是 **上游差异化器件/DSP/激光**；另一层是 **具备激光/PIC/封装垂直一体化的模块龙头**。相对而言，**纯 assembly** 最容易在 2026–2027 的 ASP 下行里被挤压。NVIDIA 直接投资 Lumentum 和 Coherent，就是对这一价值分配最直白的投票。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology))

---

## **E. 2026 年最可能发生的 3 个拐点，以及最可能放量的子方向**

\*\*拐点 1：1.6T 从“演示样机”变成“可确认收入的量产 SKU”。\*\*AOI 的 \>2 亿美元订单、Marvell Ara mass volume、Cisco/Delta 的 102.4T 系统一起出现，说明 2026 年不是只开发布会，而是订单开始进利润表。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

\*\*拐点 2：供给瓶颈正式上移到激光/CW 光源/关键器件。\*\*NVIDIA 对 Lumentum/Coherent 的打法，外加 TrendForce 对 InP lasers / MEMS 的强调，意味着 2026 年开始，行业的关键变量不再是“哪家模组厂扩了几条线”，而是“哪家拿到了上游战略器件配额”。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology))

\*\*拐点 3：half‑retimed/linear 从概念进入客户预算。\*\*OIF 的 RTLR/224G Linear、Marvell Ara T、Lumentum TRO、Cisco LPO、Semtech 的 224G linear 器件，已经把这条路线从“实验室可用”推进到“客户可评估”。2026 还不会改写全行业，但会显著影响 2027 年的份额与估值。([OIForum](https://www.oiforum.com/oif-publishes-implementation-agreement-for-112-gb-s-retimed-transmitter-linear-receiver-rtlr-electrical-and-optical-interface-advancing-energy-efficiency/))

\*\*2026 年最可能放量的子方向：\*\*我押 **1.6T OSFP retimed 的 2×DR4 / 2×FR4**，其次是 **DR8**。这三条是 2026 最“工程上稳、客户敢下单、系统能交付”的路径。

---

## **F. 代表公司地图：头部公司、是否上市、在哪上市、能否在美股买到**

### **1）模块/整机/光引擎层**

* **可直接在美股买到**：AOI（**NASDAQ: AAOI**）、Lumentum（**NASDAQ: LITE**）、Coherent（**NYSE: COHR**）、Fabrinet（**NYSE: FN**）、Cisco（**NASDAQ: CSCO**）、Arista（**NYSE: ANET**）、Nokia ADR（**NYSE: NOK**）。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))  
* **非美股主板上市，不能作为标准美股主板标的直接买**：中际旭创/Innolight（**SZSE: 300308**）、新易盛/Eoptolink（**SZSE: 300502**）、光迅科技/Accelink（**SZSE: 002281**）、台达电子/Delta（**TWSE: 2308**）。([Reuters](https://www.reuters.com/markets/companies/300308.SZ/all-listings/?utm_source=chatgpt.com))  
* **未见公开主要交易所代码/按未上市或未公开代码处理**：Source Photonics、TeraHop。([Source Photonics](https://www.sourcephotonics.com/))

### **2）DSP / gearbox / 224G 模拟前端**

* **可直接在美股买到**：Broadcom（**NASDAQ: AVGO**）、Marvell（**NASDAQ: MRVL**）、Semtech（**NASDAQ: SMTC**）、MACOM（**NASDAQ: MTSI**）、Credo（**NASDAQ: CRDO**）。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next))

### **3）SiPh / CPO / OCS / 下一代高密度互连**

* **可直接在美股买到**：NVIDIA（**NASDAQ: NVDA**）、Alphabet/Google（**NASDAQ: GOOGL**）、Tower Semiconductor（**NASDAQ: TSEM**）。([Reuters](https://www.reuters.com/markets/companies/NVDA.O/))  
* **未见公开主要交易所代码/私募为主**：Ayar Labs、Lightmatter、iPronics。Ayar Labs 2026 年 3 月还在做 **Series E**，这本身就说明它仍是私募阶段。([Ayar Labs](https://ayarlabs.com/news/ayar-labs-closes-500m-series-e-accelerates-volume-production-of-co-packaged-optics/))

### **4）我建议重点跟踪的代表公司名单（按细分）**

* **1.6T retimed 模块龙头**：Innolight、中易?（这里按公开高信号我更看 Innolight / Eoptolink / AOI / Source / Coherent / Lumentum / Accelink）  
* **TRO/LRO/LPO 路线**：Marvell、Cisco、Lumentum、Semtech、MACOM、Source  
* **400G/lane 下一代**：Broadcom、Eoptolink、Source、Coherent、Lumentum  
* **上游激光/CW/PIC**：Coherent、Lumentum、MACOM、Semtech、Tower  
* **OCS/NPO/CPO/XPO**：Google、NVIDIA、Cisco、Delta、Ayar Labs、Lightmatter、iPronics、TeraHop、Eoptolink、Source

---

## **最后的投资结论**

**我对 1.6T 可插拔光模块（retimed）行业在 2026–2027 的投资价值给出“偏强乐观”判断。**  
但我会把价值捕获顺序排成这样：

**第一梯队**：InP 激光 / 高功率 CW 光源 / EML / SiPh PIC / DSP / gearbox。  
**第二梯队**：具备垂直一体化、已经通过 hyperscaler 资格的模块龙头。  
**第三梯队**：系统与 OCS/CPO optionality 公司。  
**第四梯队**：纯 assembly、缺器件能力、缺客户绑定的模组厂。

最核心的原因只有一句话：\*\*2026 年这个行业不是“有没有需求”的问题，而是“谁能在 224G、1.6T、102.4T 和 AI 工厂交付节奏下，把可靠性、功耗、上游器件和产能一起交出来”的问题。\*\*在这个框架下，retimed 仍是 2026 的主胜负手；而真正能穿越 2027–2028 的，是那些已经在向 TRO/LRO、400G/lane、NPO/CPO 预埋筹码的公司。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

如果你接下来要把这份研究转成“个股清单 \+ 估值框架 \+ 跟踪指标”，我建议下一步直接按 **模块龙头 / DSP-器件 / 激光-PIC / OCS-CPO** 四条线展开。

# **行业调研：铜互联（DAC / AEC / 连接器）**

## **2026 年 AI 数据中心建设中的机遇、挑战与投资价值**

基于截至 **2026-04-09** 的公开材料，以及项目内两份资料，我的核心判断先给出来：

**2026 不是“铜被光替代”的年份，而是“铜按距离、功耗、可靠性、可维护性重新分层”的年份。**  
最可能落地的路径不是“所有链路继续堆被动铜”，而是：**机内铜、出柜光、近芯片线缆化、短距主动化（AEC/ACC）、长距光化**。在项目内 AI 芯片/机架路线里，2026 大出货仍主要由 **Blackwell/GB300、MI350、Trillium、Trainium2、Inferentia2、Maia 200、MTIA 300** 等已量产体系驱动；**Rubin、MI450/455X、Ironwood、Trainium3、Ascend 950** 的真正放量更偏 **2H26–2027**。这意味着 **2026 最大量的铜互联不是 448G 铜，也不是全面 CPO，而是 112G AEC \+ 短距 DAC \+ 224G-ready 连接器/线缆背板**。

我这版尽量不用单一“行业报告数字”当锚，而是用四类材料交叉验证：  
一是 **GTC 2026 / OFC 2026 / DesignCon 2026 / OCP Global Summit 2025 / Ethernet Alliance Plugfest / OIF CEI-224G** 等会议与标准活动；二是 **TE、Amphenol、Credo、Astera、MaxLinear、Marvell、Semtech、Molex、Samtec、FIT、立讯** 的公告、财报、展会 demo 和客户部署；三是项目内 AI 芯片与 AI 基建资料；四是少量二级研究作方向验证，例如 **650 Group 跟踪 AEC、Dell’Oro 跟踪 1.6T 交换部署、Omdia 跟踪 AI infrastructure build super cycle**。([Amphenol](https://www.amphenol-cs.com/events/designcon))

---

## **一、近半年最重要的一手与半一手信号**

一手信号已经非常密集。**TE** 在 FY26 Q1 做到 **$4.7B 收入、$5.1B record orders**，管理层直接把 AI 带来的 **data and power connectivity** 作为增长来源；**Amphenol** FY2025 收入 **$23.1B**、Q4 收入 **$6.4B**，并在 2026 年 1 月完成对 **CommScope CCS** 的收购，预期后者 2026 销售约 **$4.1B**；**Credo** FY26 Q3 收入 **$407M**、GM **68.5%**，管理层明确说增长来自 **AECs 和 ICs**；**Astera** 已把 AI rack-scale connectivity 作为主航道，并围绕 hyperscaler 推进下一代 scale-up networking。

更关键的是客户部署。**TensorWave** 已宣布在下一代 **AMD AI clusters** 中部署 **Credo ZeroFlap AECs**，Credo 同时称其 AEC 已在大规模 AI 网络中部署 **millions** 级别，并强调更快的 **time to first token**、更高利用率和更低 link flap 风险。**Marvell** 在 2025 年 12 月还专门发起了 **Golden Cable** 计划，加速 AEC 生态和 hyp([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/TensorWave-Partners-with-Credo-to-Power-Next-Generation-AMD-Based-AI-Clusters/default.aspx))

会议与标准侧也高度一致。**DesignCon 2026** 上，Amphenol 直接把议题推到 **“448G – Is Copper Still a Viable Solution for In-Chassis Connections?”**；**Semtech \+ TE** 联合讨论 “400G Channels for AI Applications: Passive & Active Copper Cable Assemblies”；**OFC 2026** 上 Semtech 做了 **1.6T ACC** 和 **3.2T 448G ACC** live demo；**Ethernet Alliance** 到 2025 年 12 月 plugfest 已完成 **192** 项互操作测试，其中 **100** 项基于 **224G**；**OIF** 已经把 **CEI-224G** 的 XSR / VSR / MR / LR 项目全部推起来。换句话说，\*\*2026 不是“224G 能不能做”的问题，而是“224G 先在哪里做、做到多远、用什([Amphenol](https://www.amphenol-cs.com/events/designcon))

---

## **二、A. 2026 年的机遇、挑战与最可能技术路径**

### **1）机遇**

**第一，AI 机架密度和端口数继续爆发，铜互联的单位机架价值在上升。**  
项目内资料表明，2026–2027 的 AI 工厂仍高景气，Blackwell/GB300 是 2026 主力，Rubin 在 2H26–2027 拉动更高带宽、更高功率、更复杂的机架拓扑；而 TE、Amphenol、FIT、立讯都在把 224G、1.6T、448G 前研、([TE Connectivity](https://www.te.com/en/industries/data-centers-ai.html))

**第二，价值从 PCB 走线转移到“线缆化背板 / near-chip / co-packaged copper”。**  
TE 的 **AdrenaLINE 224G**、Molex 的 **Impress Co-Packaged Copper**、Samtec 的 **Si-Fly HD**、Amphenol 的 **Paladin HD2**，本质都在把长而损耗高的 PCB path 缩短，把损耗预算改到 twinax / cabled backplane / near-package 这一层。谁能把铜从“板上传输”改造成“短距高密度、可替换、可维护”的系统件，谁就更容易拿到高毛利。([TE Connectivity](https://www.te.com/en/industries/data-centers-ai.html?utm_source=chatgpt.com))

**第三，AEC 变成了“可靠性产品”，不再只是“多一点 reach 的线”。**  
Credo 的 ZeroFlap 之所以重要，不是因为它只是 AEC，而是它把 **link stability / uptime / utilization / time-to-first-token** 变成了可量化价值，这种东西是可以定价的。对超大 AI cluster 来说，少一次训练或推理集群 flap，价值([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/TensorWave-Partners-with-Credo-to-Power-Next-Generation-AMD-Based-AI-Clusters/default.aspx))

**第四，PCIe 6 / CXL / memory disaggregation 给铜增加了新场景。**  
Astera 的 **Aries Smart Cable Modules** 把 **PCIe 6.x / CXL 3.x** 的主动铜拉到 **7m**，并明确指出 64GT/s 下被动 DAC 大约只有 **3m** 左右的舒适区；Credo 的 **Toucan** 也在把 PCIe 6 retimer 变成 AI rack-scale 和 multi-rack archite([ASTERA LABS, INC.](https://www.asteralabs.com/enabling-multi-rack-ai-clusters-with-aries-smart-cable-modules-for-pcie-6/))

### **2）挑战**

**第一，铜的物理极限没有消失，只是被工程化延后。**  
Keysight 把今天的现实边界说得很清楚：**DAC** 大约适合 **1m** 级，**ACC** 大约到 **3m**，**AEC** 大约到 **7–9m**；OIF 的 **CEI-224G-MR** 预算只有 **500mm PCB \+ 1 connector**，**LR** 也只是 **1000mm backplane \+ 2 connectors**。224G/448G 下，插损、串扰、连接器过孔、温([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0319_pr26-056-keysight-expands-1-6t-interconnect-validation-technology-to-include-passive-copper-and-low-power-optics.html))

**第二，液冷时代的机械与热设计变难了。**  
被动 DAC 越粗越难布线，容易挡风和压缩维护空间；TE 已经在做连接器与液冷桥接方案，Astera 也直接把“更薄、更柔的主动电缆”作为卖点。未来能不能在液冷、高密、可维护三者之间平([TE Connectivity](https://www.te.com/en/about-te/events/ofc-2025.html))

**第三，标准尚未完全收口，互操作仍是门槛。**  
224G 生态虽然已经非常热闹，但 **IEEE 802.3dj** 在 2025 年 12 月 plugfest 时还未最终定稿；ACC 甚至是到 **2026 年 2 月** 才成立 **ACC-MSA** 来推进线性主动铜的设备/线缆互通。对投资来说，这意味着 2026 会是“design win 和小批量量产”之年，真正全面标([Keysight United States](https://www.keysight.com/blogs/en/inds/ai/ethernet-alliance-800g-1-6t-plugfest-2025-december-blog))

**第四，专利和认证不是小事。**  
2026 年 3 月 Credo 分别与 **Molex**、**TE** 达成 AEC 相关专利争议和解/交叉授权，这反过来说明 AEC 绝不是一条完全 com([Credo](https://credosemi.com/news/credo-and-molex-reach-settlement-in-active-electrical-cable-patent-infringement-disputes/))

### **3）当前正在被使用的主流技术**

当前主流技术可以非常清楚地按 reach 分层：

* **Passive DAC**：机架内、超短距、最低([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0319_pr26-056-keysight-expands-1-6t-interconnect-validation-technology-to-include-passive-copper-and-low-power-optics.html))  
* **ACC（线性主动铜）**：用 redriver / linear EQ 拉长到约 2–3m，强调([ACC-MSA](https://www.acc-msa.org/))  
* **AEC（带 retimer / CDR 的主动电缆）**：给到 7–9m，适合 AI 集群里对稳定性([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0319_pr26-056-keysight-expands-1-6t-interconnect-validation-technology-to-include-passive-copper-and-low-power-optics.html))  
* **Cabled backplane / flyover / internal cabled I/O / near-chip connector**：用 twinax 或近封装连接器绕开长 PCB path，支撑 224G。([TE Connectivity](https://www.te.com/en/industries/data-centers-ai.html?utm_source=chatgpt.com))  
* **PCIe 6 / CXL 主动铜**：服务 GPU-to-GPU、GPU-to-memory([ASTERA LABS, INC.](https://www.asteralabs.com/enabling-multi-rack-ai-clusters-with-aries-smart-cable-modules-for-pcie-6/))  
* **更长距离与机架外 scale-out**：越来越光化，Broadcom/NVIDIA/项目内资料都指向 2027 之后光学继续向 A([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-delivers-industrys-first-400glane-optical-dsp-next))

### **4）在“前十大 AI 芯片家族”背景下，铜互联新技术的成熟与放量时间**

我用项目内出货/装机最大的十类家族作为背景：**Blackwell/GB300、Rubin、MI350、MI450/455X、TPU Trillium/Ironwood、Trainium2/3、Inferentia2、Maia 200、MTIA 300/400/500、Ascend 910C/950**。项目内资料的关键信息是：\*\*2026 主量仍在已量产电互联体系，Rubin/MI450/Ironwood/Trainium3 真正推高 200G/lane 与 224G 压力的窗口是 2

因此我的时间判断是：

| 技术 | 成熟时间 | 放量时间 | 判断 |
| ----- | ----- | ----- | ----- |
| 112G DAC | 已成熟 | 2026 继续大批量 | 仍是极短距基本盘 |
| 112G AEC | 已成熟 | 2026 最大量 | 2026 最有可能的量产赢家 |
| 200G/lane ACC | 2026 进入工程可用 | 2027 放量 | 先吃 1–3m、低功耗短链路 |
| 224G retimed electrical / cabled backplane | 2026 资格认证、样机、design-in | 2027 放量 | 先在 switch/near-chip/线缆背板落地 |
| PCIe 6 / CXL 主动铜 | 2026 早期部署 | 2027 放量 | 跟随 rack disaggregation |
| 224G near-package / co-packaged copper | 2026 小批量 | 2027–2028 放量 | 会先进入顶级机架/交换芯片 |
| 448G 铜 | 2026 demo / 前研 | 2028 以后 | 2026–2027 仍不是量产主线 |

这个判断的支撑来自：Semtech 已在 OFC 2026 做 224G/448G ACC demo；Credo 和 MaxLinear 都在推 224G retimer；TE、Molex、Samtec、Amphenol 都在把 224G 做成 near-chip / cabled backplane / high-density connector；([Semtech](https://www.semtech.com/company/press/showcases-ai-interconnect-leadership-with-live-1.6t-demos-ofc-2026))

### **5）2026 最可能的技术路径**

一句话概括：**“机内铜、出柜光；短距 DAC 保底，中距 AEC 主导，ACC 开始切入；224G 先从 near-chip / cabled backplane / retimer 化落地。”**  
我认为 **2026 最可能的大量部署路径** 是：

* **0–1m**：DAC 继续占优。  
* **1–7m**：AEC 成为 AI cluster 的最强主线。  
* **2–3m 的 200G/lane 新链路**：ACC 开始占一部分新增份额。  
* **224G**：先在线缆背板、近芯片连接器、retimer 化铜链路落地，而不是大面积“长板走线裸奔”。  
* **出柜/跨柜/行级**：光模块和后续更近([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0319_pr26-056-keysight-expands-1-6t-interconnect-validation-technology-to-include-passive-copper-and-low-power-optics.html))

---

## **三、B. 关键产品拆分与 2026–2027 市场规模（我的偏乐观工程模型）**

**口径说明**：只算 **AI 数据中心信号铜互联**，不把光模块、交换 ASIC、供电母排/母线、液冷设备计入。  
我把 2026 总体 AI 铜互联 TAM 估成 **$6.0B / $8.6B / $11.8B**（保守 / 基准 / 乐观），2027 估成 **$8.8B / $13.4B / $18.9B**。这个区间建立在项目内 AI 芯片与 AI 工厂高景气假设之上，且 delib

| 产品类别 | 2026 TAM（保/基/乐，$bn） | 2027 TAM（保/基/乐，$bn） | 基准渗透路径 | 2026→2027 基准增速 |
| ----- | ----- | ----- | ----- | ----- |
| Passive DAC | 1.1 / 1.4 / 1.8 | 1.2 / 1.5 / 2.0 | 适用短链路中，2026 约 68%，2027 约 60% | \+7% |
| ACC | 0.2 / 0.6 / 1.1 | 0.5 / 1.2 / 2.2 | 1–3m、200G/lane 新链路中，2026 约 8%，2027 约 20% | \+100% |
| AEC | 1.7 / 2.7 / 3.8 | 2.8 / 4.2 / 6.0 | \>1m 高速电链路中，2026 约 45%，2027 约 60% | \+56% |
| Internal cabled I/O / flyover / cabled backplane | 0.7 / 1.2 / 1.8 | 1.2 / 2.0 / 3.0 | 新一代 224G-ready 板卡中，2026 约 18%，2027 约 35% | \+67% |
| 高速连接器系统（front panel / board-to-board / near-chip） | 1.8 / 2.2 / 2.8 | 2.6 / 3.2 / 4.3 | 新 AI 机架/交换板连接器 BOM 中，2026 约 30%，2027 约 52% 为 224G-ready | \+45% |
| PCIe 6 / CXL 智能铜缆 / SCM / cable-retimer content | 0.5 / 0.5 / 0.5 | 0.5 / 1.3 / 1.4 | 多机架 GPU/内存解耦链路中，2026 约 9%，2027 约 22% | \+160% |

**我最看好的不是 DAC，而是三层：AEC、224G 连接器/线缆背板、PCIe/CXL 主动铜。** DAC 会继续有量，但会逐步从“成长股”变成“存量工具”；真正享受 AI 溢价的，是把 SI、热、诊断、可靠性一起卖出去的产品。这个判断与 Credo、Astera、TE、Molex、Samtec、Amphe([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

---

## **四、B（第二问）. 主要技术与新技术的 2026–2027 规模、渗透率路径**

**注意：下面是技术口径，彼此有重叠，不能相加。**

| 技术 | 2026 TAM（保/基/乐，$bn） | 2027 TAM（保/基/乐，$bn） | 基准渗透路径 |
| ----- | ----- | ----- | ----- |
| 112G DAC | 1.1 / 1.4 / 1.8 | 1.2 / 1.5 / 2.0 | 适用极短距链路中：68% → 60% |
| 112G AEC | 1.7 / 2.5 / 3.5 | 2.5 / 3.8 / 5.4 | 适用中短距高速链路中：45% → 60% |
| 200G/lane ACC | 0.2 / 0.6 / 1.1 | 0.5 / 1.4 / 2.5 | 新 200G/lane 短距链路：8% → 20% |
| 224G retimed electrical / cabled backplane | 0.4 / 1.0 / 1.8 | 1.2 / 2.4 / 4.1 | 新 scale-up fabric：12% → 32% |
| PCIe 6 / CXL 3.x 主动铜 | 0.2 / 0.5 / 0.8 | 0.5 / 1.2 / 2.0 | 多机架 GPU/内存互连：9% → 22% |
| 224G near-package / CPC | 0.1 / 0.3 / 0.6 | 0.4 / 0.8 / 1.5 | 顶级 switch/XPU 平台：3% → 10% |
| 448G 铜 | 0 / 0.05 / 0.1 | 0.05 / 0.2 / 0.5 | 2026 几乎只 demo，2027 才开始 pilot |

---

## **五、C. 供给侧：产能结构、瓶颈、成本与毛利**

### **1）产能结构**

* **连接器/线缆总装**：量产重心在 **中国、东南亚、墨西哥**，但设计/IP 与高端客户导入主要被 **Amphenol、TE、Molex、Samtec** 等掌握；中国链条里 **FIT、立讯、BizLink** 的存在感显著上升。Amphenol 在约 **40 个国家**有设施，Samtec 有 **40+ locations / 14+ plants**，FIT 和立讯都在把 AI([Amphenol Investors](https://investors.amphenol.com/news-and-events/news-details/2026/Amphenol-Reports-Record-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx))  
* **主动端芯片（AEC/ACC/retimer/SCM）**：高度集中在美国 fabless —— **Credo、Astera、MaxLinear、Semtech、Marvell、Broadcom、MACOM**。这层技术壁垒最高，([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))  
* **近芯片/共封装铜连接器**：仍由 **Molex、Samtec、TE、Amphenol** 这类老牌连接器公司主导，Molex 甚至披露其 NearStack OTS 已累计交付 \*\*100([Molex](https://www.molex.com/en-us/news/molex-launches-impress-co-packaged-copper-solutions-scaling-near-asic-connectivity-innovations-to-meet-next-gen-data-rate-demands))

### **2）供给瓶颈（至少 5 条）**

1. **224G/448G SI 预算极紧**：OIF 的 MR/LR 定义本身就在告诉([OIForum](https://www.oiforum.com/technical-work/hot-topics/common-electrical-i-o-cei-224g/))  
2. **主动端芯片与调参复杂度高**：Keysight 明说 assembled interconnect 的验证和调优更复杂，且新 DSP / retimer / linear amp 正([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0319_pr26-056-keysight-expands-1-6t-interconnect-validation-technology-to-include-passive-copper-and-low-power-optics.html))  
3. **标准与互操作未完全统一**：IEEE 802.3dj 未 final、ACC-MSA 刚成立、([Keysight United States](https://www.keysight.com/blogs/en/inds/ai/ethernet-alliance-800g-1-6t-plugfest-2025-december-blog))  
4. **液冷时代的布线与维护**：粗 DAC/AEC 的 routing、弯折半径([TE Connectivity](https://www.te.com/en/about-te/events/ofc-2025.html))  
5. **认证与客户导入周期长**：PCI-SIG、OIF、Ethernet Alliance、各 hyperscaler 自身认([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credos-Toucan-PCIe-Retimer-Achieves-PCISIG-Compliance/default.aspx))  
6. **专利/IP 风险**：2026 年的 Credo-Molex / Credo-TE 纠([Credo](https://credosemi.com/news/credo-and-molex-reach-settlement-in-active-electrical-cable-patent-infringement-disputes/))  
7. **224G/1.6T 测试人才和设备**：测试设备和互操([Semtech](https://www.semtech.com/company/press/showcases-ai-interconnect-leadership-with-live-1.6t-demos-ofc-2026))

### **3）成本与毛利（我的工程化拆分）**

这部分我没有找到公开、可核验、可横比的统一 BOM，所以给 **工程化估算**：

* **Passive DAC**：双轴线缆 **35–50%**，连接器/笼子 **25–35%**，小 PCB/EEPROM **3–8%**，组装测试 **10–20%**。  
* **ACC**：线缆 **25–35%**，连接器 **20–30%**，线性 EQ / redriver **10–20%**，小 PCB/固件 **5–10%**，组装测试 **15–20%**。  
* **AEC**：线缆 **15–25%**，连接器 **15–25%**，DSP/retimer/CDR **25–40%**，PCB/固件/诊断 **5–10%**，组装测试/老化 **15–20%**。  
* **224G 高速连接器系统**：精密冲压/电镀/塑封 **40–55%**，良率与精密治具 **10–20%**，验证测试 **10–15%**，IP/设计摊销 **10–15%**，客户导入支持 **10–15%**。

毛利决定因素里，**铜价不是第一变量**；真正决定毛利的是 **能否满足 loss budget、功耗、稳定性、可运维性和认证要求**。因此 **AEC / SCM / retimer** 的长期毛利明显高于纯线缆装配；Credo 的 **68.5% GM**、Astera 的高毛利，已经说明([ACC-MSA](https://www.acc-msa.org/))

---

## **六、D. 竞争格局与壁垒（可量化）**

### **1）市场结构**

我**没有找到可信公开口径的精确 CR4 / CR8**，所以给工程化估计：

* 在 **高端 AI 连接器 / near-chip / cabled backplane** 里，**Amphenol、TE、Molex、Samtec** 四家大概率覆盖了 **70–85%** 的主流平台导入。  
* 在 **merchant active copper silicon** 里，**Credo、Astera、Marvell、Semtech、MaxLinear、Broadcom** 六家占据绝大部分设计话语权。  
* 在 **线缆组装与中国性价比供给** 里，**FIT、立讯、BizLink** 的份额弹性最大。

这是我根据财务规模、展会能见度、主流 demo 覆盖率和 hyperscaler 可见导入面做的判断。规模上，Amphenol FY2025 **$23.1B**、TE 单季 **$4.7B** 且 orders 创新高、Credo 单季 **$407M / 68.5% GM**，([Amphenol Investors](https://investors.amphenol.com/news-and-events/news-details/2026/Amphenol-Reports-Record-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx))

### **2）壁垒清单：为什么能定价**

1. **信号完整性壁垒**：224G/448G 不是“把铜做粗一点”就行，需要 channel modeling、材料、连接器 geometry、cable skew、retimer tuning([OIForum](https://www.oiforum.com/technical-work/hot-topics/common-electrical-i-o-cei-224g/))  
2. **设计导入/切换成本壁垒**：一旦某个 connector/cable family 被写进 switch、NIC、GPU tray、背板和机柜图纸，更换就意味着重新认证和 re-l([The Samtec Blog](https://blog.samtec.com/post/samtec-inks-second-source-agreement-with-molex-on-224-gbps-si-fly-hd/))  
3. **可靠性和软件/诊断壁垒**：AEC 已经有 telemetry、link recovery、ZeroFlap 之类“软硬一体”特性，这不是 comm([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/TensorWave-Partners-with-Credo-to-Power-Next-Generation-AMD-Based-AI-Clusters/default.aspx))  
4. **标准/认证壁垒**：OIF、PCI-SIG、Ethernet Alliance、ACC-MSA 不([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credos-Toucan-PCIe-Retimer-Achieves-PCISIG-Compliance/default.aspx))  
5. **制造规模和全球交付壁垒**：超大客户需要多厂区、跨区域、可追溯和快速二供，所以 Amphenol/TE/Samtec/Mo([Amphenol Investors](https://investors.amphenol.com/news-and-events/news-details/2026/Amphenol-Reports-Record-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx))  
6. **IP 壁垒**：AEC 专利和解事件已经证明，([Credo](https://credosemi.com/news/credo-and-molex-reach-settlement-in-active-electrical-cable-patent-infringement-disputes/))

### **3）长期高 ROIC / 高毛利最可能在哪一层**

**最可能长期高 ROIC / 高毛利的三层**：

* **第一层：主动铜 silicon（AEC DSP / retimer / redriver / smart cable module）**  
  这是我最看好的价值捕获层。原因是它同时吃到了 **带宽升级、可靠性、软件诊断、标准认证、客户锁定**。Credo、As([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))  
* **第二层：224G premium connector / near-chip / cabled backplane 平台**  
  这层不是普通连接器，而是“替代长 PCB 的系统解决方案”。被 desig([TE Connectivity](https://www.te.com/en/about-te/events/ofc-2025.html))  
* **第三层：整合式信号+电力+热管理供应商**  
  TE、Amphenol、FIT、立讯在这个方向都有动作；未来最吃香的是能把 connector、cable、thermal、甚至 power interf([TE Connectivity](https://www.te.com/en/industries/data-centers-ai.html))

**最弱的一层**反而是纯 commodity 化的 passive cable assembly。

---

## **七、E. 2026 年最可能发生的 3 个拐点**

**拐点 1：AEC 从“替代 DAC 的选项”变成 AI 机架里的默认中短距方案。**  
Credo 的 millions deployed、TensorWave 的 cluster 采用、Marvell 的 Golden Cab([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/TensorWave-Partners-with-Credo-to-Power-Next-Generation-AMD-Based-AI-Clusters/default.aspx))

**拐点 2：224G 铜从展台走向 design-in。**  
TE、Molex、Samtec、Amphenol、MaxLinear、Credo、FIT、立讯都已经把 224G 做到具体产品级；2026 最重要的不是出货多少，而是谁先拿到下一代 switch / XPU ([TE Connectivity](https://www.te.com/en/about-te/events/ofc-2025.html))

**拐点 3：ACC 和 PCIe/CXL 主动铜从“概念补充”变成真实新增市场。**  
ACC-MSA 的成立、Semtech 的 live demo、Astera/Credo 的 PCIe/CXL 方案，意味着 2026 年开始出现新的子方向。2027 年看，这两([GlobeNewswire](https://www.globenewswire.com/news-release/2026/02/23/3242613/19814/en/Thirteen-Industry-Leaders-Unite-to-Define-Active-Copper-Cable-Standards.html?utm_source=chatgpt.com))

---

## **八、F. 代表性公司清单：按产品/技术分层列示**

下面尽量覆盖公开资料里**最有代表性**的公司。私营长尾线束厂、区域代工厂无法完全穷尽。

### **1）DAC / ACC / AEC / 线缆组件**

* **Credo**：AEC / retimer / 1.6T AEC，\*\*NASDAQ: CR([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))  
* **Amphenol**：连接器、线缆、背板、224G 平台，\*\*NYSE: A([Amphenol Investors](https://investors.amphenol.com/news-and-events/news-details/2026/Amphenol-Reports-Record-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx))  
* **TE Connectivity**：224G connector / cabled backplane / internal cable，\*\*NYSE: T([TE Connectivity](https://www.te.com/en/about-te/news-center/corporate-news/2026/2026-01-21-te-connectivity-announces-first-quarter-results-for-fiscal-year-2026.html))  
* **Molex**：CPC / NearStack / data center connectivity，\*\*私有（Koch 旗下([Molex](https://www.molex.com/en-us/news/molex-incorporated-agrees-to-be-acquired-by-koch-industries-inc))  
* **Samtec**：Si-Fly HD / FireFly / high-speed connectors，\*\*私([Samtec](https://www.samtec.com/about/))  
* **FIT Hon Teng / Foxconn Interconnect**：224G CPC、448G CHIPLINK、AI interconnect，\*\*HKEX: 60([Fit Foxconn](https://www.fit-foxconn.com/mainssl/modules/MySpace/index.php?pg=ZC4355&sn=fit))  
* **立讯精密 Luxshare**：224G small-scale mass production、448G 预研，\*\*SZSE: 0024([Luxshare ICT](https://www.luxshare-ict.com/en/investors.html))  
* **BizLink**：线缆与互连方案，\*\*TWSE: 36([BizLink](https://www.bizlinktech.com/financial-information))  
* **Infraeo**：小而活跃的 AEC/ACC/AOC([Infraeo](https://www.infraeo.com/?utm_source=chatgpt.com))

### **2）224G/448G 连接器、背板、near-chip / CPC**

* \*\*Amphenol、TE、Molex、Samtec、FIT([TE Connectivity](https://www.te.com/en/about-te/events/ofc-2025.html))  
* **JAE**：通用连接器强厂，**TSE: 6807**([JAE](https://www.jae.com/en/ir/))  
* **Yamaichi Electronics**：高速连接器/测试 socket 能力强，**TSE: 6941**([Yamaichi Electronics](https://www.yamaichi.co.jp/en/ir/))

### **3）主动铜硅片 / retimer / redriver / SCM / 验证**

* **Astera Labs**：PCIe/CXL SCM、rack-scale connectivity，\*\*NASDAQ: AL([Astera Labs](https://asteralabs.gcs-web.com/))  
* **MaxLinear**：224G scale-up retimer，\*\*NASDAQ: M([MaxLinear](https://www.maxlinear.com/news/press-releases/2026/maxlinear-unveils-annapurna-224g-scale-up-retimer-to-extend-copper-connectivity-in-ai-data-centers))  
* **Semtech**：224G/448G ACC 相关器件，**NASDAQ: SMTC**，可直接买美股。([Semtech](https://www.semtech.com/company/press/showcases-ai-interconnect-leadership-with-live-1.6t-demos-ofc-2026?utm_source=chatgpt.com))  
* **Marvell**：ACC/AEC/OCS/CXL/AI interconnect 平台，\*\*NASDAQ: MR([Marvell Technology, Inc.](https://investor.marvell.com/))  
* **Broadcom**：224G/400G-lane、switch/NIC/custom XPU 生态，\*\*NASDAQ: AV([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial))  
* **MACOM**：200G/lane 数据中心互连相关器件，\*\*NASDAQ: MT([MACOM](https://ir.macom.com/financial-information/))  
* **Keysight**：验证与互操作测试，\*\*NYSE: KE([Keysight Investor Relations](https://investor.keysight.com/stock-information/stock-data-and-chart/default.aspx?utm_source=chatgpt.com))  
* **MultiLane**：1.6T 测试与互操作([Multilane](https://multilaneinc.com/?utm_source=chatgpt.com))

---

## **最后的投资判断**

如果只选一句结论，我会写：

**2026 年铜互联最值得投的不是“铜价”，而是“让铜在 AI 机架里继续有生命力的工程能力”。**  
这体现在三类资产上：

1. **AEC / active copper silicon**：最容易拿到高毛利和高 ROIC。  
2. **224G premium connector \+ near-chip/cabled backplane**：最容易拿到 design-in 和长期锁定。  
3. **中国高弹性制造链（FIT / 立讯 / BizLink）**：最容易吃到平台切换期的份额增量。

相对不那么性感的，是纯 commodity 化的被动 DAC 总装。  
所以，这个行业在 2026 年真正的主线不是“铜对抗光”，而是：

**“把铜从廉价材料，升级成 AI 机架里的可靠性、布线、功耗和可维护性解决方案。”**

如果你后面要把这份报告继续压缩成 **“投资备忘录版（2页）”** 或 **“上市公司映射版（按美股/港股/A股分组）”**，我建议下一步直接做。

# **行业调研：【网卡 / DPU / SmartNIC / 高速 I/O】**

本报告把范围锁定在 **AI 计算中心中的网卡 / DPU / SmartNIC / 高速 I/O 全栈**，优先采用 **近半年、尤其 2026 年**的官方发布会、IR、产品规格、联盟规范和客户采用公告；二手验证只用 Reuters、Dell’Oro 和少量技术媒体。重点材料包括 **NVIDIA GTC 2026、OFC 2026、OCP ESUN 1.0、UEC 1.0.2、UALink 2.0**，并结合项目内两份底稿对 2026–2027 AI 芯片主线和 Rubin/AI Factory 技术栈做交叉映射。([NVIDIA Investor Relations](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx))

## **先给结论**

**1）2026 年这个行业的主线已经不是“普通网卡升级”，而是 AI 工厂的网络/存储/内存层系统重构。**  
最强信号是：Dell’Oro 指出 **以太网在 2025 年已经超过 InfiniBand，成为 AI back-end scale-out 的主导 fabric**，且 800G 已占绝大多数，1600G 将于 2026 年下半年开始出货；Dell’Oro 还预计 AI back-end 交换机市场到 2030 年将超过 1000 亿美元，并判断 **以太网最终会同时主导 scale-out 和 scale-up**。NVIDIA 在 Rubin 平台中已经把 **ConnectX-9 SuperNIC、BlueField-4 DPU、Spectrum-6、STX 存储架构**放进同一个 AI Factory 平台里。([Dell'Oro Group](https://www.delloro.com/news/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025/))

**2）2026 最可能的技术路径不是“DPU 取代一切”，而是“AI NIC / SuperNIC 负责后端大规模集合通信，DPU/SmartNIC 负责前端、多租户、存储、安全与 AI-native context/KV offload”。**  
NVIDIA BlueField-4 STX 明确把 DPU 推向 **context memory storage / 数据摄取 / AI-native storage tier**，官方声称可提升 **最高 5 倍 token throughput、4 倍能效**，并已有 CoreWeave、Crusoe、IREN、Lambda、Mistral、Nebius、OCI、Vultr 等首批采用者。AMD 则用 **Pollara 400** 切入 UEC-ready AI NIC，用 **Vulcano 800** 切入 2026 年的 AI scale-out。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption))

**3）2026 是 800G 大年，1.6T 的“验证 \+ 小批量导入”年；真正的大放量更像 2027。**  
Broadcom 的 **Tomahawk 6 102.4T** 已经量产出货，**Thor Ultra 800G AI NIC** 在送样；Marvell 已经把 **1.6T 光 DSP、1.6T ZR/ZR+、UEC-ready 交换、CXL 共享内存**摆上 OFC 2026；Arista 则推出 **12.8T 液冷 XPO 模块**。但 Dell’Oro 也明确把 **1600G volume shipping** 放在 2026 年后半段，并把 CPO 加速采用放到更长一点的窗口。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-introduces-industrys-first-800g-ai-ethernet-nic))

**4）投资上，长期最有可能拿到高 ROIC / 高毛利的，不是“普通板卡组装”，而是三层：交换芯片+fabric 软件、光 DSP/AEC/retimer/CXL 控制器、以及绑定存储/安全的软件化 DPU 平台。**  
证据很直接：Astera Labs 2025 年收入同比增 **115%**、GAAP 毛利率 **75.7%**；Credo 2026 财年 Q3 收入同比增 **201.5%**、GAAP 毛利率 **68.5%**；Arista 2025 全年 GAAP 毛利率 **64.1%**；Broadcom 2026 财年 Q1 AI 收入 **84 亿美元**，并指引 Q2 AI 半导体收入 **107 亿美元**，驱动项就是 **custom AI accelerators \+ AI networking**。([Astera Labs](https://ir.asteralabs.com/node/8671/pdf))

**5）在你要求的“乐观 AI 基建”前提下，我的基准情景偏乐观：2026–2027 这个赛道不是景气衰退，而是价值外溢。**  
项目内芯片底稿显示，2026–2027 出货/装机最大的主线芯片家族正在向 **Blackwell/GB300、Rubin、MI350/MI450、TPU Trillium/Ironwood、Trainium2/3、Maia 200、MTIA、Ascend 910C/950**集中，其共同特征是 **更高 HBM、更大机架功率、更重液冷、更强 scale-up/scale-out**，这会把 NIC / DPU / 高速 I/O 从“服务器配件”抬升为“系统瓶颈层”。

---

## **近半年最关键的一手信号**

**NVIDIA：** Rubin 平台已把 **七颗核心芯片**放进统一 AI Factory 叙事，官方写明其中包括 **ConnectX-9 SuperNIC、BlueField-4 DPU、Spectrum-6**，并称这些 Rubin-based 产品将于 **2026 年下半年**由 AWS、Google Cloud、Azure、OCI、CoreWeave 等提供。BlueField-4 STX 则把 AI 存储/KV/context 问题正式产品化。([NVIDIA Investor Relations](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx))

**AMD：** Pollara 400 是官方口径里的 **“首个 UEC-ready AI NIC”**，400Gbps、OCP 3.0 形态；Vulcano 是 2026 年的下一代 **800G AI NIC**，支持 PCIe 和 UALink 接口，并将随 Helios/MI455X 平台推进。Oracle 将在 **2026 年 Q3** 提供首个公开的 **5 万颗 MI450 GPU** 超级集群。([AMD](https://www.amd.com/en/solutions/data-center/networking.html?utm_source=chatgpt.com))

**Broadcom：** 2026 财年 Q1 AI 收入 **84 亿美元**、同比翻倍，Q2 AI 半导体收入指引 **107 亿美元**；产品侧，**Tomahawk 6 102.4T** 已经量产，**Thor Ultra 800G AI NIC** 已送样，OFC 2026 又把 **102.4T CPO 交换、400G/lane DSP、PCIe Gen6 switch/retimer** 全部摆上台面。([Broadcom Inc.](https://investors.broadcom.com/node/63976/pdf))

**Marvell：** OFC 2026 的主题已经不是单个器件，而是“connectivity is the primary bottleneck”。其公开了 **1.6T PAM4 DSP**、**1.6T ZR/ZR+**、**UEC-ready Teralynx**、**Structera CXL memory fabric**、以及与 NVIDIA 的 **NVLink Fusion / 硅光合作**。财务上，Marvell 2026 财年收入 **81.95 亿美元**创新高。([Marvell Technology, Inc.](https://investor.marvell.com/news-events/press-releases/detail/1013/marvell-ushers-in-the-1-6t-era-with-expanded-optical-dsp-platform-portfolio-redefining-ai-data-center-end-to-end-connectivity))

**Astera / Credo / Arista / Cisco：** Astera 的 **Scorpio X-Series** 已进入初始量产 ramp，并把 **Leo CXL Smart Memory** 部署到 Azure M-series，成为首个已宣布的 CXL-attached memory 云部署；Credo Q3 FY2026 收入同比增 **201.5%**，明确增长来自 **AECs 和 ICs**；Arista 的 **XPO 12.8T 液冷光模块**代表“高密 pluggable optics”路线；Cisco 的 **Silicon One G300 102.4T** 和 **P200 51.2T** 则瞄准 gigawatt-scale AI clusters 的 scale-out 与 scale-across。([Astera Labs](https://ir.asteralabs.com/node/8671/pdf))

**标准/联盟：** UEC 已发布 **1.0.2** 规范；OCP 已在 2026 年 3 月发布 **ESUN 1.0**，明确要让 Ethernet 进入 GPU scale-up；UALink 刚在 2026 年 4 月发布 **2.0**，加入 in-network compute、chiplet、manageability 和 200G 物理层。OFC 2026 上，Keysight 与 Broadcom 还公开演示了 **UEC LLR \+ CBFC 在 800GE 全线速互通**。([Ultra Ethernet Consortium](https://ultraethernet.org/wp-content/uploads/sites/20/2026/01/UE-Specification-1.0.2-1.pdf))

---

## **A. 2026 年的机遇、挑战、现用技术，以及未来成熟/放量判断**

### **1）机遇**

2026 年最大的机遇是：**AI 集群规模继续变大，而网络和 I/O 已经成为 GPU 利用率的直接约束项**。Dell’Oro 已确认 Amazon、Microsoft、Meta、Oracle、xAI 都在采用以太网 AI back-end，且 800G 已成主流；Rubin、Helios、Ironwood、Trainium、Maia 这类平台都在把集群组织形式推向 rack-scale / pod-scale。对 NIC / DPU / 高速 I/O 行业来说，这意味着 **端口速率升级、交换容量升级、AOC/AEC/光模块升级、PCIe/CXL 升级、DPU/存储卸载升级**会被同步拉动。([Dell'Oro Group](https://www.delloro.com/news/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025/))

### **2）挑战**

真正的挑战不在“有没有需求”，而在 **能否把系统按期交付**。Broadcom 已公开提示 2026 年的瓶颈不只在 TSMC 产能，还包括 **laser、PCB、光模块相关部件**；Reuters 还报道了内存大厂对 3–5 年长期合同的推动，以及 HBM/DRAM 紧张状态延续；Solidigm 也警告 AI 数据增长可能拉紧 SSD/存储供应。项目内对 Rubin 的梳理也把 **HBM4、先进封装、CPO 良率、液冷装配、HVDC 改造**列为未来两年执行风险。([Reuters](https://www.reuters.com/world/asia-pacific/broadcom-flags-supply-constraints-says-tsmc-capacity-bottleneck-2026-03-24/))

### **3）2026 年正在被使用的主流技术**

今天真正已经在用、并且会继续放量的，是以下几条：  
一是 **400/800G AI NIC / SuperNIC \+ RoCE/可编程拥塞控制**，代表是 NVIDIA ConnectX-8/9、AMD Pollara、Broadcom Thor Ultra；二是 **102.4T 交换芯片 \+ 200G/lane SerDes**，代表是 Spectrum-6、Tomahawk 6、Cisco G300；三是 **800G pluggable optics / AEC / AOC**；四是 **PCIe Gen6 主机 I/O** 开始进入新平台，Astera 已推出把 PCIe 6.0 主机桥接到既有 Gen5 NIC 的 Aries 6；五是 **CXL 内存扩展**开始从概念变成云侧真实部署；六是 **DPU/IPU** 持续承担虚拟化、存储、安全与前端网络卸载，而 BlueField-4 STX 这类产品正在把 DPU 推到 AI-native storage / context tier。([NVIDIA](https://www.nvidia.com/en-us/networking/products/ethernet/supernic/))

同时也要承认，**InfiniBand 和封闭 scale-up fabric 并没有在 2026 年消失**。Dell’Oro 的结论是“以太网在 AI back-end 的 scale-out 已经超过 InfiniBand，并且长期看会压向 scale-up”，但 NVIDIA 仍在同时推进 ConnectX/Quantum-X800/NVLink 体系。更准确的判断是：**2026 年新增大集群的主流增长在 Ethernet，极致性能和部分既有生态继续留给 InfiniBand / 封闭 scale-up。**([Dell'Oro Group](https://www.delloro.com/news/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025/))

### **4）结合 2026–2027 主流 AI 芯片技术路径，我对新技术成熟/放量时间的判断**

结合项目底稿中的 2026–2027 主流芯片家族路径，我更看重的是它们的共同需求：**更高 HBM、更高每机架功率、更强集群并行、更重长上下文/推理流量**。这会决定网络与 I/O 技术并不是同步成熟，而是分层成熟。

| 新技术 | 2026 成熟判断 | 放量时间 | 我的结论 |
| ----- | ----- | ----- | ----- |
| 800G AI NIC / SuperNIC | 已成熟 | 2026 全年 | 主流量产层 |
| 1.6T 交换 / 光模块 / DSP | 小批量导入 | 2027 | 2026 验证、2027 放量 |
| PCIe Gen6 NIC / retimer / gearbox | 成熟导入 | 2026H2–2027 | 新平台标配化 |
| CXL 内存扩展 / pooling | 早期商用 | 2027 | 先在推理/RAG/KV 场景走量 |
| UEC-ready 端到端栈 | 规范成熟 | 2026H2–2027 | 先由头部集群采用 |
| ESUN（以太网 scale-up） | 规范成熟、产品初代 | 2027–2028 | 2026 主要是生态定型 |
| UALink | 规范先行 | 2027 以后 | 2026 更像设计与评估年 |
| CPO / XPO / 液冷超高密 optics | 样机与设计导入 | 2027 | 2026 不是大规模收入年 |
| DPU-based STX / context storage | 2026H2 起量 | 2027 | 这是最容易低估的新层 |

### **5）我认为 2026 年最可能的技术路径**

**最可能的主线路径是：**  
**“以太网优先的 AI scale-out \+ 800G AI NIC/SuperNIC \+ 102.4T 交换芯片 \+ 800G optics/AEC \+ PCIe Gen6 主机 I/O \+ DPU 向 AI-native storage/context/security 收缩并升维”。**  
换句话说，2026 年最可能放量的不是“CPO 全面替代 pluggables”，也不是“UALink 立即大规模商用”，而是 **Ethernet-first 的 800G 主流化，1.6T 的验证导入，DPU 从通用卸载转向 AI 存储/上下文层，CXL 从概念进入局部真部署**。([Dell'Oro Group](https://www.delloro.com/news/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025/))

---

## **B1. 关键产品拆分，以及 2026–2027 市场规模/渗透率三情景**

**说明：** 下表是我基于官方发布、客户采用、Dell’Oro 框架和行业财报做的 **偏乐观推演**；口径为**相关产品年化市场规模**，**彼此有重叠，不能横向相加**。锚点主要来自：Dell’Oro 预计 **AI back-end switch 市场 2030 年超 1000 亿美元**、Ethernet Adapter & Smart NIC 市场 **2028 年超 160 亿美元**，以及 2026 年 800G/1.6T 的产品节奏。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

| 产品类别 | 代表产品 | 2026E（保守 / 基准 / 乐观） | 2027E（保守 / 基准 / 乐观） | 渗透率路径（我的定义） |
| ----- | ----- | ----- | ----- | ----- |
| AI 后端 NIC / SuperNIC | ConnectX-8/9、Pollara、Thor Ultra、Vulcano | 50–70 / 70–100 / 100–130 亿美元 | 80–110 / 110–150 / 150–200 亿美元 | 新增 AI 后端端口中，400/800G 专用 AI NIC 渗透率：2026 65%/75%/85%，2027 80%/88%/93% |
| DPU / IPU / SmartNIC | BlueField、Pensando、Intel IPU、OCTEON | 18–25 / 25–35 / 35–50 | 28–40 / 40–55 / 55–75 | 新增 AI front-end / storage / control 节点 attach：2026 20%/30%/35%，2027 30%/40%/45% |
| AI back-end 交换机 / 系统 | Spectrum-6、Tomahawk 6、G300、Teralynx、Scorpio | 120–160 / 160–220 / 220–280 | 180–250 / 250–350 / 350–450 | 102.4T 级别在新增 AI back-end 交换容量中的占比：2026 45%/60%/70%，2027 70%/80%/90% |
| Optics / AEC / AOC / DSP / 液冷光互连 | 800G pluggables、AEC、1.6T DSP、XPO、CPO | 90–120 / 120–170 / 170–230 | 150–220 / 220–300 / 300–400 | 1.6T 在新增高端 AI 光互连中的占比：2026 3%/7%/10%，2027 15%/25%/35% |
| PCIe / CXL 连接芯片 | PCIe Gen6 switch/retimer/gearbox、CXL controller/switch | 15–25 / 25–40 / 40–60 | 30–50 / 50–80 / 80–120 | PCIe 6.0 在新增 AI 服务器主机 I/O 中占比：2026 20%/35%/45%，2027 50%/65%/75% |
| AI-native storage / context offload | BlueField-4 STX、CXL memory pool、KV tier | 3–8 / 8–15 / 15–25 | 10–20 / 20–35 / 35–60 | 新增超大推理集群采用 context/KV 独立层：2026 2%/5%/8%，2027 10%/18%/25% |

---

## **B2. 主流技术与高增长新技术：2026–2027 市场规模/渗透率三情景**

**说明：** 这里按“技术价值池”估算，同样有重叠。核心不是算绝对精确值，而是判断 **哪条曲线最陡、何时拐点最清晰**。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

| 技术路径 | 2026E（保守 / 基准 / 乐观） | 2027E（保守 / 基准 / 乐观） | 渗透率路径判断 |
| ----- | ----- | ----- | ----- |
| AI 后端以太网（UEC/ESUN \+ RoCE/拥塞控制） | 250–350 / 350–450 / 450–600 亿美元 | 400–550 / 550–750 / 750–950 | 2026 已成主流，2027 继续挤压 InfiniBand |
| InfiniBand / 封闭 scale-up fabric | 60–100 / 80–120 / 120–150 | 50–90 / 70–110 / 100–130 | 绝对值未必掉，**相对份额**下降 |
| 1.6T / 200G-lane optics & DSP | 10–30 / 30–50 / 50–80 | 50–100 / 100–160 / 160–240 | 2026 以 design-in 为主，2027 进入量产曲线 |
| CPO / XPO / 液冷超高密 optics | 2–6 / 6–12 / 12–20 | 10–20 / 20–40 / 40–70 | 2026 试点，2027 开始可见收入 |
| PCIe 6.0 \+ CXL memory expansion/pooling | 5–10 / 10–20 / 20–35 | 15–30 / 30–50 / 50–80 | 先从推理/RAG/KV 扩展切入，再向训练侧渗透 |
| UALink / 开放 scale-up | 1–3 / 3–6 / 6–10 | 5–10 / 10–20 / 20–35 | 2026 规范先行，2027 才能看产品化 |
| DPU-based context/KV/storage offload | 3–8 / 8–15 / 15–25 | 10–20 / 20–35 / 35–60 | 这是 2026–2027 最容易被低估的新附加层 |

---

## **C. 供给侧：产能结构、瓶颈、成本与毛利**

### **1）产能结构**

从公开披露看，这条链的 **设计主权**主要集中在美国/以色列，**先进制造/封装**高度集中在台湾，**系统整机与板卡**集中在台湾/北美 ODM/OEM，**光模块/AEC/部分封装组装**则更分散到中国和东南亚。公开能确认的代表工艺包括：AMD **Vulcano 800 AI NIC 为 3nm**，Marvell **1.6T PAM4 DSP 为 3nm**，Marvell **OCTEON 10 DPU 为 5nm**；NVIDIA 的系统/OEM 伙伴名单则覆盖 Dell、HPE、Lenovo、Supermicro、Foxconn、Inventec、Pegatron、QCT、Wistron、Wiwynn 等。([AMD](https://www.amd.com/content/dam/amd/en/documents/corporate/events/advancing-ai-2025-distribution-deck.pdf))

### **2）至少 5 条关键瓶颈**

第一，**200G/lane SerDes 与模拟混合信号人才**稀缺，这是 800G/1.6T、PCIe6/CXL、光 DSP、AEC/retimer 的共用瓶颈。第二，**laser、光器件与高端 PCB lead time** 已经被 Broadcom 点名。第三，**HBM/先进封装/液冷/机架功率**会反向拖慢整个网络层交付，因为 AI 集群是系统工程。第四，**UEC/ESUN/PCIe6/CXL 的互通与认证**很慢，Keysight/Broadcom 公开做 800GE UEC 互通演示，本身就说明生态仍在磨合。第五，**存储与 SSD 供应**也会被 AI 数据量拉紧。第六，**超大客户资格认证周期长**，一旦进入设计定点，后续 2–4 年更换供应商并不容易。([Reuters](https://www.reuters.com/world/asia-pacific/broadcom-flags-supply-constraints-says-tsmc-capacity-bottleneck-2026-03-24/))

### **3）成本与毛利：我的经验拆分**

这部分公开精确数据很少，我给经验模型：  
**AI NIC / SuperNIC 板卡**中，控制器/PHY/SerDes 大致占 **30%–45%**，PCB/连接器/电源/散热 **10%–15%**，若含绑定光模块/AEC，则连接介质可再占 **20%–35%**；  
**DPU 板卡**中，DPU SoC 常占 **35%–50%**，板上 DRAM **10%–20%**，NIC PHY/SerDes **10%–15%**；  
**102.4T 级交换系统**中，交换 ASIC **25%–35%**，光模块/线缆/CPO **25%–40%**，机箱/电源/散热 **10%–15%**，retimer/PCB/连接器 **10%–20%**。  
毛利的决定因素不是纯 BOM，而是 **误码率/功耗/拥塞控制/遥测/软件栈/验证能力**。所以板卡通常利润最低，**控制器与系统软件最高**。

### **4）价格传导机制**

这条链的价格不是简单 cost-plus，而是 **“GPU 集群停机成本倒逼溢价”**。如果一个 1% 的网络效率改善能换来更高 GPU 利用率、缩短 job completion time，客户愿意为更稳定的 NIC/交换/光互连支付显著溢价；相反，泛用 NIC、低速前端卡和缺乏软件绑定的白牌产品会更快被压价。Astera、Credo、Arista 的高毛利，已经说明 **高端连接芯片 \+ 软件/验证能力**能拿到定价权。([Astera Labs](https://ir.asteralabs.com/node/8671/pdf?utm_source=chatgpt.com))

---

## **D. 竞争格局与壁垒（可量化）**

### **1）市场结构**

**交换侧最清楚。** Dell’Oro 说 2025 年 AI back-end Ethernet 交换市场里，**Celestica \+ NVIDIA 合计接近 50% 份额**，Arista 第三，Cisco 开始加速，HPE/Juniper 也拿到新账户。这个市场仍然高度集中，但已经不是“一家独大”的静态格局。([Dell'Oro Group](https://www.delloro.com/news/ethernet-more-than-doubles-size-of-infiniband-as-the-leading-fabric-for-ai-scale-out-networks-in-2025/))

**NIC / SmartNIC / DPU 侧更像“高集中 \+ 内部自研并存”。** 独立第三方统计没有像交换机那样透明，但从公开产品看，商业供给主要被 **NVIDIA、Broadcom、AMD、Intel、Marvell、Astera**掌控，而 AWS Nitro、Azure Boost 这类 **内部 DPU** 则进一步压缩了外部供应商的前端市场空间。([Amazon Web Services, Inc.](https://aws.amazon.com/ec2/nitro/))

### **2）壁垒清单：为什么这些环节能定价**

**技术壁垒。** 200G/lane SerDes、低功耗 DSP、CXL/PCIe6 时序完整性、800GE/1.6T BER 控制，不是普通数字芯片公司能快速补齐的。  
**规模壁垒。** 需要持续做互通、验证、参考设计和现场支持，客户越大，供应商越少。  
**渠道/客户锁定。** AI 集群一旦定型，NIC/交换/光模块/软件常常跟着机架与运维体系一起绑定。  
**认证标准壁垒。** UEC、ESUN、OCP 3.0、PCIe/CXL、Azure CXL deployment 等都需要长验证周期。  
**切换成本。** 更换端点或 fabric 不是换一块卡，而是改动驱动、遥测、拥塞算法、运维 SOP，代价很高。  
这就是为什么高端连接层能定价：**它卖的不是器件，而是 GPU 集群不掉速。**([Ultra Ethernet Consortium](https://ultraethernet.org/))

### **3）价值捕获：哪一层最可能长期高 ROIC / 高毛利**

我最看好三层。  
第一层是 **交换芯片 \+ fabric 软件/遥测**，因为它直接决定大集群吞吐和作业完成时间；  
第二层是 **光 DSP / AEC / retimer / CXL controller**，因为这是最硬的模拟/互通/功耗门槛；  
第三层是 **绑定存储/安全/上下文的软件化 DPU 平台**，前提是能真正进入 AI-native storage 或安全控制面。  
我最不看好的是“纯板卡组装 \+ 无软件附着”的泛化网卡，因为那一层更容易被价格竞争吞掉。

---

## **E. 2026 年最可能发生的 3 个拐点**

**拐点一：Ethernet 在 AI back-end 的“胜负手”基本坐实，并开始从 scale-out 走向 scale-up。**  
UEC 1.0.2、ESUN 1.0、Dell’Oro 对 Ethernet 统治 scale-up/scale-out 的判断，都说明 2026 已不是“以太网能不能做 AI back-end”的问题，而是“哪种以太网栈先成主流”。([Ultra Ethernet Consortium](https://ultraethernet.org/wp-content/uploads/sites/20/2026/01/UE-Specification-1.0.2-1.pdf))

**拐点二：1.6T \+ PCIe6/CXL 让“高速 I/O”从板级问题上升为机架级架构问题。**  
Tomahawk 6 已量产，1.6T DSP/光模块在 OFC 2026 集体亮相，Aries 6 已开始解决“Gen6 host 对接既有 NIC”的过渡痛点，CXL 4.0 则把带宽翻到 128GT/s。2026 下半年，架构团队讨论的将不只是“换更快的卡”，而是“机架内部和机架之间怎么重构 I/O 预算”。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-now-shipping-worlds-first-1024-tbps-switch-production))

**拐点三：DPU 从通用云卸载，转向 AI-native storage / context / KV 层。**  
BlueField-4 STX 是 2026 年最值得盯的拐点型产品之一；Marvell 的 CXL 共享内存和 Astera 的 Azure CXL 部署也在证明，未来网络和内存/存储会一起重构。DPU 不会消失，但它的高增长方向会从“泛云 offload”转向“AI 数据与上下文层”。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption))

---

## **F. 公司全景图：按产品/技术分类列出代表公司、上市情况、是否可在美股买到**

下面按主干链条覆盖头部与细分代表公司。

**AI NIC / SuperNIC / AI endpoint NIC**  
NVIDIA（ConnectX-8/9，**NASDAQ: NVDA**，可直接买）；AMD（Pollara / Vulcano，**NASDAQ: AMD**，可）；Broadcom（Thor Ultra，**NASDAQ: AVGO**，可）；Intel（以太网适配器/IPU，**NASDAQ: INTC**，可）；Marvell（定制 NIC / connectivity，**NASDAQ: MRVL**，可）；AWS Nitro 与 Azure Boost 属于内部自研，不单独上市，分别通过 **AMZN** 和 **MSFT** 获得经济暴露。([NVIDIA Investor Relations](https://investor.nvidia.com/home/default.aspx))

**DPU / IPU / SmartNIC / 基础设施卸载**  
NVIDIA BlueField（NVDA）；AMD Pensando（AMD）；Intel IPU（INTC）；Marvell OCTEON 10 DPU（MRVL）；AWS Nitro（AMZN 体系内）；Azure Boost（MSFT 体系内）；HPE Aruba CX10000 通过 Pensando 获得 DPU 交换机敞口（**NYSE: HPE**，可）。([AMD](https://www.amd.com/en/products/data-processing-units/pensando.html))

**AI back-end 交换 / fabric / scale-up & scale-out**  
NVIDIA Spectrum / Quantum（NVDA）；Broadcom Tomahawk / Jericho / Thor（AVGO）；Cisco Silicon One（**NASDAQ: CSCO**，可）；Arista（**NYSE: ANET**，可）；Marvell Teralynx / Structera（MRVL）；Astera Labs Scorpio（**NASDAQ: ALAB**，可）；Celestica（交换系统/OEM，**NYSE/TSX: CLS**，可在美股买）。([Cisco Investor Relations](https://investor.cisco.com/overview/default.aspx))

**Optics / AEC / AOC / CPO / XPO / 光互连**  
Credo（AEC/retimer/optics，**NASDAQ: CRDO**，可）；Coherent（激光/光器件，**NYSE: COHR**，可）；Lumentum（激光/光器件，**NASDAQ: LITE**，可）；Fabrinet（光模块代工，**NYSE: FN**，可）；Broadcom（DSP/CPO，AVGO）；Marvell（DSP/ZR/ZR+，MRVL）；Arista（XPO，ANET）；中际旭创（**深交所 300308**，无美股主板代码）；新易盛（**深交所 300502**，无美股主板代码）；天孚通信（**深交所 300394**，无美股主板代码）。([Credo Technology Group](https://investors.credosemi.com/resources/investor-faqs/default.aspx))

**PCIe / CXL / retimer / gearbox / 内存互连**  
Astera Labs（Leo / Aries / Scorpio，ALAB）；Broadcom（PCIe Gen6 switch/retimer，AVGO）；Marvell（Structera / 1.6T / CXL，MRVL）；Qualcomm（通过收购 Alphawave 获取高速连接资产，**NASDAQ: QCOM**，可）；Montage 澜起科技（CXL/内存连接，**上交所科创板 688008；港交所 6809**，不能直接在美股主板买）。Alphawave 已于 2025 年 12 月从伦敦交易所退市。([Astera Labs](https://ir.asteralabs.com/node/8671/pdf))

**AI-native storage / context / KV offload 生态**  
NVIDIA（BlueField-4 STX，NVDA）；Cloudian、DDN、VAST、WEKA、MinIO（多为未上市/私有）；NetApp（**NASDAQ: NTAP**，可）；Nutanix（**NASDAQ: NTNX**，可）；Dell（**NYSE: DELL**，可）；HPE（NYSE: HPE，可）；IBM（**NYSE: IBM**，可）。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-launches-bluefield-4-stx-storage-architecture-with-broad-industry-adoption))

---

## **最后一句判断**

如果把 2026 年当作 AI 计算中心的大建设年，我对这个行业的判断是：

**最值得下注的不是“普通网卡数量增加”，而是“AI back-end 以太网化 \+ 800G 向 1.6T 迁移 \+ DPU 向 context/storage/security 升维 \+ PCIe6/CXL 打开新的内存层 \+ 光互连提前定型”。**  
最有弹性的投资抓手，是 **交换芯片与系统、光 DSP/AEC/retimer、CXL/PCIe 连接控制器、以及 AI-native storage/context 层**；最大风险仍是 **供给链与交付链**，不是需求链。([Dell'Oro Group](https://www.delloro.com/news/ai-back-end-switch-market-will-push-past-100-billion-by-2030/))

**高价值继续跟踪的论坛/材料**：GTC 2026、OFC 2026、OCP ESUN 1.0、UEC 1.0.2、UALink 2.0、Dell’Oro 的 AI back-end switch / Ethernet Adapter & Smart NIC 报告。([NVIDIA Investor Relations](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Opens-Agentic-AI-Frontier/default.aspx))

如果你下一步要把这份报告继续压成 **“投资清单 \+ 关键公司对比表 \+ 上市公司优先级排序”**，我建议直接按 **交换 / 光互连 / 连接芯片 / DPU 软件层** 四条线展开。

# **行业调研：光互联（光模块/光器件）**

**时间窗口：2025-10-09 至 2026-04-09**  
\*\*口径说明：\*\*我优先用了近半年的一手材料：OFC 2026 官方议程与展会新闻、OIF/OCP/OCI/Open CPX/XPO 等标准与联盟材料、头部公司公告/IR/订单/高管口径；行业报告只作为校准层，主要用了 TrendForce、LightCounting、Cignal AI、Yole 的公开摘要。AI 芯片背景层直接采用项目内两份资料：NVIDIA GTC 2026 技术栈与 AI 芯片全景。 ([\*\*\*\*TODO optica \*\*\*\*](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-show-floor-programs-deliver-essential-insights-on-market-direction-and-breakthrough-technol/))

最近半年的“底座材料”里，最值得反复看的其实只有八类：OFC 2026（把 1.6T、AI cluster interconnect、CPO/OCS/NPO、224G SerDes 可靠性直接摆上主舞台）、OIF @ OFC 2026 的 40 家公司互通演示、OCP 2025 Global Summit 的 AI scale-up/短距光互联议程、OCP 新建的 OCS 项目、NVIDIA GTC 2026 Rubin/Spectrum-6 路线、TrendForce 的 800G+ 渗透判断、LightCounting 的 2026–2031 光互联展望、以及 Cignal/Yole 对 OCS/CPO 的中长期曲线。([\*\*\*\*TODO optica \*\*\*\*](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-show-floor-programs-deliver-essential-insights-on-market-direction-and-breakthrough-technol/))

## **先给结论**

1. **2026 最可能的主路径不是“全行业立刻切到 CPO”，而是“800G 继续做绝对出货主力，1.6T 开始形成真实订单与量产坡道，AEC 继续统治超短距，LRO/LPO 在部分新架构渗透，OCS 和 switch-side CPO 进入设计定型年”。** AOI 已拿到首个 1.6T 量产订单，金额超 2 亿美元；Marvell 明确表示 Ara 1.6T DSP 已向全球客户批量供货；Tower 已与 NVIDIA 围绕 1.6T SiPh 模块合作。与此同时，800G 仍在继续加单，AOI 4 月又拿到 7100 万美元 800G 新订单。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))  
2. **2026–2027 这轮不是单纯“速率升级”，而是“AI 工厂光化率提升”。** LightCounting 认为，AI scale-out 网络里单颗 GPU 未来最多会带动 6 只光收发器，而 scale-up 网络带宽需求又大约是 scale-out 的 10 倍；TrendForce 则判断 800G 及以上光模块的全球出货占比会在 2026 年超过 60%。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382))  
3. **2026 是“开放标准元年”，不是“最终形态落地年”。** 3 月 OFC 前后，OCI、Open CPX、XPO 三个联盟几乎同时成形：OCI 试图把 AI scale-up 从“模块中心”转成“硅中心”；Open CPX 试图定义 near-package/co-packaged 光引擎的插座、热、管理和电光接口；XPO 则把液冷高密度可插拔直接推到 12.8T。这个节奏本身就说明：compute-side optics 还没到 2026 全面放量，正处在标准锁定期。([OCI MSA](https://oci-msa.org/))  
4. **投资上，2026–2027 最有弹性的不是“普通模块组装产能”本身，而是三层：DSP/SerDes、稀缺激光器/外置光源/SiPh 平台、以及拿到头部客户 design-win 的 1.6T 模块龙头。** Coherent 明确说 FY26 下半年到 FY27 的 datacenter & communications 需求仍强；Lumentum为 AI 数据中心新增美国 InP 产能，且 NVIDIA 是该新厂客户；Credo 的 Q3 FY26 非 GAAP 毛利率达到 68.6%，说明上游高壁垒 IC/互连层的盈利能力显著强于普通硬件组装。([Coherent Inc](https://www.coherent.com/news/press-releases/second-quarter-fiscal-year-2026-results))  
5. **最大的风险不是需求，而是执行。** LightCounting 判断 2026 光模块产能并不是绝对不够，真正限制增长的是 XPU 和 switch ASIC 供应；Keysight 则在 OFC 2026 直接指出，接近 80% 的失效发生在互连环节；Aehr 拿到面向 SiPh 收发器与 optical I/O 的工程验证 \+ 高量产 burn-in 订单，也说明测试、可靠性和量产认证已成为新的硬瓶颈。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382))

---

## **A. 2026 年在 AI 计算中心大建设下，光互联行业的机遇、挑战、现用技术与主路径判断**

### **1）机遇**

**第一，带宽/算力比持续上升，光器件内容量会继续抬升。**  
项目内 AI 芯片资料显示，2026 仍由 Blackwell/Blackwell Ultra、MI350、Trainium2、Trillium 等延续型平台支撑大规模装机，2027 才更明显切向 Rubin、MI450、Ironwood、Trainium3、Ascend 950 等新一代平台；这意味着 2026 会同时出现两股需求：一股是 800G 对既有大规模 AI 集群的延续扩容，另一股是 1.6T 对 200G/lane 新平台的资格验证与前置备货。Rubin 还把 Spectrum-6 102.4T/200G CPO 交换层拉进官方平台，说明“光”已不只是网络配件，而是 AI 工厂 token/watt 的一部分。 ([NVIDIA Developer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/))

**第二，1.6T 已从“展示品”变成“订单品”。**  
AOI 3 月拿到首个 1.6T 量产订单，预计 Q3 开始发货、Q4 完成，且管理层判断 1.6T 会成为 hyperscaler 的下一步；Marvell 则称 Ara 已向全球客户批量供货；Cisco 发布了 1.6T OSFP 产品；InnoLight、Eoptolink、Accelink、Source 也都公开了 1.6T 产品或演示。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

**第三，OCS 把“光”从端口速率升级，推向网络架构升级。**  
Google 已公开表示，其在 Jupiter/AI 网络和 TPU 系统里广泛使用 Project Apollo 的 OCS；TrendForce 进一步推演，Ironwood \+ Apollo OCS 架构会让 800G+ 模块在 2026 成为 AI 数据中心标准件，并使 Google 一家在 2026 的 800G+ 需求超过 600 万只；Cignal 则认为 OCS 市场保守看 2029 年也会到 25 亿美元。([Open Compute Project](https://www.opencompute.org/blog/the-open-compute-project-announces-new-optical-circuit-switching-ocs-project))

**第四，光纤/连接器/激光器从“辅料”升级为战略采购。**  
Meta 与 Corning 签了最高 60 亿美元的多年度光纤光缆协议；Lumentum 为全球最大 AI 数据中心建设新的美国 InP 激光器产能；Broadcom、Lumentum、Ciena、Arista 都在 2026 年把外置激光源、CPO/NPO、XPO、液冷可插拔等推到公开路线图。([About Facebook](https://about.fb.com/news/2026/01/meta-6-billion-agreement-corning-support-us-manufacturing/))

### **2）挑战**

**第一，2026 最大瓶颈已经从“会不会做 1.6T”转成“能不能把 224G/200G-lane 可靠地做成量产系统”。**  
OIF 在 OFC 2026 把 CEI-224G、CEI-448G、Co-Packaging、CMIS 作为 40 家公司互通演示重点；Semtech 则在 OFC 2026 推出 224G 线性 TIA/driver，直接覆盖 LPO/LRO/XPO/NPO/CPO；Keysight 则明确指出 1.6T/224G 时代的失效大头在互连。([OIForum](https://www.oiforum.com/meetings-events/oif-ofc-2026/))

**第二，2026 的真正卡点不是模块组装，而是 DSP、激光器、SiPh 封装、测试与认证。**  
LightCounting 判断 2026 光模块需求增长会被 XPU 与 switch ASIC 短缺压住，只能增长约 60%；Lumentum 在扩 InP，Aehr 在扩 SiPh burn-in，说明上游器件与测试比简单装配更紧。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382))

**第三，标准在加快，但也在分叉。**  
2026 同时出现 OCI、Open CPX、XPO、OCP OCS、OIF 224G/448G 等多条标准线，这对产业是好事，但对中小厂是坏事：谁不在标准桌上，谁未来就只能做被动配套。([OCI MSA](https://oci-msa.org/))

### **3）目前实际在用的技术**

下表按 **scale-up / scale-out / scale-across / reconfiguration** 四层来归纳 2026 真正在用或已进入客户验证的主技术路径。归纳依据主要来自 OFC 2026、OIF、OCP、GTC 2026 和头部厂商 1.6T/CPO/OCS 公告。([\*\*\*\*TODO optica \*\*\*\*](https://www.ofcconference.org/news-media/news-releases/2026/ofc-2026-show-floor-programs-deliver-essential-insights-on-market-direction-and-breakthrough-technol/))

| 层级 | 2026 主流方案 | 代表技术/公司 |
| ----- | ----- | ----- |
| 机柜内、邻柜短距 scale-up | **DAC/AEC 仍是主力**，AOC 次之；光 scale-up 仍以 pilot/标准化为主 | Credo AEC/ALC、Broadcom 200G/lane AEC、OCI、Lumentum VCSEL optical scale-up |
| 机架间 scale-out | **800G 可插拔仍是绝对主力**；**1.6T 可插拔开始导入**；FRO 为主，LRO/LPO 开始渗透 | AOI、Marvell、Cisco、InnoLight、Eoptolink、Accelink、Source |
| 园区/跨楼 scale-across | 800ZR/ZR+、1.6T coherent、coherent-lite、多轨 DCI | Ciena、Cisco/Acacia、Marvell |
| 网络重构/大规模调度 | **OCS** 开始从 Google 专有走向开放生态 | Google Apollo/OCP OCS、Lumentum、Marvell、Accelink |
| switch-edge 光集成 | **switch-side CPO/NPO** 已进入产品/演示期；compute-side 仍偏早 | NVIDIA、Broadcom、Ciena CPX、Open CPX、XPO |

### **4）结合 2026–2027 AI 芯片主族群，预测光互联新技术的成熟与放量**

按项目内 AI 芯片全景，2026–2027 的大装机主族群大致分成两拨：  
**第一拨**是 Blackwell/Blackwell Ultra、MI350、Trainium2、Trillium、Maia 200、MTIA 300、Ascend 910C 这类“继续放量”的平台；它们决定了 **800G \+ AEC \+ 局部 LPO/LRO** 在 2026 的绝对量。  
**第二拨**是 Rubin、MI450、Ironwood、Trainium3、Ascend 950 这类“定义下一代”的平台；它们决定了 **1.6T、OCS、switch-side CPO、optical scale-up 标准** 的定型节奏。

| 技术 | 2026 状态 | 成熟时间判断 | 放量时间判断 | 我的判断 |
| ----- | ----- | ----- | ----- | ----- |
| 800G FRO 可插拔 | 已成熟、仍在大量追加订单 | 已成熟 | **2026 继续大放量** | 仍是 2026 出货王 |
| 1.6T FRO / LRO 可插拔 | 从 sample 进入真实订单与批量供货 | **2026H2** | **2027** | 2027 成为最大增量 |
| LPO / LRO / TRO | 224G 芯片与客户验证加快 | **2026–2027** | **2027** | 先在高功耗机柜与新架构放量 |
| AEC / ALC / 有源铜 | 已成熟，短距仍最经济 | 已成熟 | **2026–2027 持续放量** | 2026 不会被光立刻替代 |
| OCS | 头部客户已实用，开放标准刚成形 | **2026** | **2027–2028** | Google 之后会外溢到更多云厂 |
| switch-side CPO / NPO | 已有商用交换机/演示 | **2026–2027** | **2027** | 先从 switch，不先从 compute |
| compute-side optics（OCI/CPX/XPO） | 联盟成立、产品演示密集 | **2027** | **2028+** | 2026 还是“标准年” |
| 400G/lambda、3.2T 可插拔 | 处于样机/器件验证期 | **2027** | **2028–2029** | 不是 2026 主线 |
| 相干-lite / 1.6T ZR/ZR+ | 进入 AI campus/metro 讨论与样机阶段 | **2026–2027** | **2027** | AI scale-across 会打开新口袋 |

上表的核心判断很明确：**2026 最可能的技术主路径 \= 800G 可插拔继续冲量 \+ 1.6T 可插拔开始上量 \+ AEC 守住短距 \+ OCS 在头部客户扩张 \+ switch-side CPO 开始商用；compute-side optical scale-up 仍处于生态定型期。** 这个节奏，与 2026 仍由现有大规模平台贡献绝对装机、2027 才更明显转向 Rubin/Ironwood/MI450 的芯片路线是匹配的。 ([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

---

## **B1. 关键产品分类，以及 2026–2027 市场规模区间与渗透路径**

\*\*口径：\*\*只统计 **AI 数据中心直接相关** 的光互联产品价值池，不含传统电信与普通企业网；下表为 **本文测算**，我把基准情景设得偏乐观。锚定边界主要来自：TrendForce 的 800G+ 渗透与 Google 800G+/OCS 需求、LightCounting 的 2026 增长判断、Cignal 的 OCS 曲线、Yole 的 CPO 路线。([TrendForce](https://www.trendforce.com/presscenter/news/20260210-12919.html))

**我给的总量判断：**  
\*\*2026E：\*\*保守 **$17–26B**，基准 **$25–37B**，乐观 **$33–48B**  
\*\*2027E：\*\*保守 **$21–32B**，基准 **$32–50B**，乐观 **$45–71B**  
这里的基准已经偏乐观：默认 1.6T 认证快于传统以太网升级节奏、头部云厂继续高强度扩 AI fabric、Google/Meta/微软风格的开放光 scale-up 方案在 2027 开始转收入。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382))

| 产品类别 | 2026E（保/基/乐，$bn） | 2027E（保/基/乐，$bn） | 渗透率路径（对应适用场景新增端口） | 2026→2027 增长判断 |
| ----- | ----- | ----- | ----- | ----- |
| **800G 可插拔模块** | 10–13 / 13–16 / 16–20 | 9–12 / 12–16 / 15–22 | 2026 新建 AI scale-out 光端口 **50–70%**；2027 **30–50%** | **\-10% \~ \+20%**，收入平稳，绝对出货仍最大 |
| **1.6T 可插拔模块** | 2–4 / 4–7 / 6–10 | 4–8 / 8–14 / 12–20 | 2026 **10–20%**；2027 **30–50%** | **\+80% \~ \+180%**，全行业最强弹性 |
| **AEC / AOC / DAC** | 2–3 / 3–5 / 4–6 | 3–4 / 4–7 / 6–9 | 2026 新建短距 scale-up/邻柜链路 **65–80%**；2027 **55–70%** | **\+20% \~ \+60%** |
| **OCS** | 0.3–0.5 / 0.5–0.8 / 0.8–1.2 | 0.5–0.8 / 0.8–1.3 / 1.2–2.0 | 2026 顶级 hyperscaler 新 superpod 采用率 **15–25%**；2027 **25–40%** | **\+50% \~ \+150%** |
| **CPO / NPO / XPO / CPX 光引擎与液冷高密模块** | 0.15–0.3 / 0.3–0.8 / 0.6–1.5 | 0.4–0.8 / 0.8–2.0 / 1.5–4.0 | 2026 新 switch/XPU 光边缘端口 **1–3%**；2027 **5–12%** | **\+120% \~ \+300%**，但基数很低 |
| **AI campus DCI 相干/相干-lite** | 1.5–2.5 / 2.0–3.5 / 3.0–5.0 | 2.0–3.0 / 3.0–5.0 / 4.5–7.0 | 2026 AI scale-across 新链路 **15–25%**；2027 **25–40%** | **\+30% \~ \+80%** |
| **高密度光纤/连接器/配线** | 1.5–2.5 / 2.0–3.5 / 3.0–4.5 | 2.0–3.0 / 3.0–5.0 / 4.5–6.5 | 2026 在新建超大集群里已成前置规划项，预装率 **\>80%**；2027 **\>90%** | **\+25% \~ \+70%** |

---

## **B2. 主流技术与高增长新技术的 2026–2027 市场规模与渗透路径**

\*\*注意：\*\*这一张按“技术路径”拆，和产品表 **重叠、不可相加**。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382))

| 技术路径 | 2026E（保/基/乐，$bn） | 2027E（保/基/乐，$bn） | 渗透路径 | 结论 |
| ----- | ----- | ----- | ----- | ----- |
| **DSP 全重定时 FRO** | 12–15 / 14–18 / 17–22 | 10–14 / 13–18 / 16–22 | 2026 新 AI 光模块 **65–75%**；2027 **45–60%** | 仍是 2026 主流，但 2027 占比被 1.6T 线性系分流 |
| **LPO / LRO / TRO / 线性光** | 1.5–2.5 / 2.5–4.0 / 4.0–6.0 | 3.0–5.0 / 5.0–9.0 / 8.0–13.0 | 2026 **8–15%**；2027 **18–30%** | 2026 不是主流，2027 是最快份额提升路径 |
| **AEC / 有源铜** | 2–3 / 3–5 / 4–6 | 3–4 / 4–7 / 6–9 | 2026 短距链路 **65–80%**；2027 **55–70%** | 会被光侵蚀，但不是立刻出局 |
| **OCS** | 0.3–0.5 / 0.5–0.8 / 0.8–1.2 | 0.5–0.8 / 0.8–1.3 / 1.2–2.0 | 2026 头部 superpod **15–25%**；2027 **25–40%** | 低基数高增长，2026 是架构定型年 |
| **CPO / NPO / OCI / CPX / XPO** | 0.15–0.3 / 0.3–0.8 / 0.6–1.5 | 0.4–0.8 / 0.8–2.0 / 1.5–4.0 | 2026 **1–3%**；2027 **3–8%** | 2028 以后才可能接棒成主逻辑 |
| **相干-lite / ZR / ZR+** | 1.5–2.5 / 2.0–3.5 / 3.0–5.0 | 2.0–3.0 / 3.0–5.0 / 4.5–7.0 | 2026 **15–25%**；2027 **25–40%** | AI campus/metro 是很容易被低估的新口袋 |

---

## **C. 供给侧：产能结构、瓶颈、成本与毛利**

### **1）产能结构：地区 / 公司 / 工艺**

**模块装配与垂直集成能力，仍然明显集中在中国与台湾。**  
TrendForce 甚至判断，在 Google 的 800G+ 订单里，Innolight 与 Eoptolink 合计可拿到接近 80%；中国厂商这几年已不只是做封装，而是在 1.6T、LPO/LRO、NPO/OCS 上同步推进。InnoLight、Eoptolink、Accelink、Source 都有 1.6T / NPO / OCS / 400G/lambda 相关公开产品或演示。([TrendForce](https://www.trendforce.com/presscenter/news/20260210-12919.html))

**北美的强项不在低成本装配，而在高价值器件、系统、光纤与测试。**  
Meta 与 Corning 的最高 60 亿美元光缆协议、Lumentum 新建美国 InP 工厂、Coherent 对 FY26H2–FY27 的 datacenter 强需求判断、以及 Aehr 面向 SiPh WLBI 的新订单，说明北美正把价值链重心放在光纤/激光器/系统平台/测试上。([About Facebook](https://about.fb.com/news/2026/01/meta-6-billion-agreement-corning-support-us-manufacturing/))

**工艺上，2026 不是单一技术路线，而是“三条并行”：**  
1）**InP/EML/UHP laser/ELS**：仍是 800G/1.6T 直检和 CPO 外置光源的关键利润池；  
2）**SiPh/PIC**：用于 1.6T、NPO、CPO、光引擎，Tower-NVIDIA、Ciena CPX、Source TFLN/SiPh、Eoptolink NPO 都说明 SiPh 已经深入下一代；  
3）**MEMS/FAU/精密耦合**：主要对应 OCS，与 Accelink 的 320×320 OCS 和 Google Apollo 路线一致。([Tower Semiconductor](https://towersemi.com/2026/02/05/02052026/))

### **2）至少 5 个供给瓶颈**

**瓶颈 1：224G/200G-lane 的电接口与信号完整性。**  
这是 1.6T 的真实物理门槛。OIF 在 OFC 2026 把 CEI-224G/448G 互通摆到核心位置；Semtech 的 224G 线性芯片直接覆盖 LPO/LRO/XPO/NPO/CPO。([OIForum](https://www.oiforum.com/meetings-events/oif-ofc-2026/))

**瓶颈 2：激光器，尤其是 InP、EML、UHP laser 与外置光源。**  
Lumentum 的新厂明确瞄准 InP；其 OFC 2026 还公开了 1W SHP laser 和 16 通道 DWDM UHP laser/ELSFP；Broadcom 也把 400G EML/PD 作为 1.6T/3.2T 的基础。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-New-U-S--Manufacturing-Facility-to-Produce-Advanced-Lasers-for-the-Worlds-Largest-AI-Data-Centers/default.aspx))

**瓶颈 3：DSP / SerDes / switch ASIC 与 XPU 的同步供给。**  
LightCounting 明确说 2026 光模块增长不会被模块产能限制，而会被 XPU 与 switch ASIC 短缺限制。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382))

**瓶颈 4：SiPh 封装、fiber attach、光引擎热管理与测试。**  
Aehr 拿到工程验证 \+ HVM 的 SiPh WLBI 订单，说明量产瓶颈已经往测试和可靠性迁移；Keysight 也强调 1.6T 的验证难度主要在互连。([Aehr Test Systems](https://www.aehr.com/2026/03/aehr-wins-major-new-silicon-photonics-customer-with-high-power-fox-xp-wafer-level-burn-in-system-for-hyperscale-data-center-optical-interconnect-market/))

**瓶颈 5：OCS / CPO 的可靠性与可维护性。**  
Cignal 认为 OCS 的首要指标是可靠性；Ciena 的 CPX 之所以强调“外置光源 \+ 开放生态”，就是为了绕开传统 CPO 难维护的痛点。([Cignal AI](https://cignal.ai/2025/12/the-optical-circuit-switching-market-4q25/))

**瓶颈 6：液冷、散热与模块功耗预算。**  
Cisco 称 800G LPO 可把模块功耗降 50%；Ciena 的 6.4T CPX 号称较传统重定时方案省电 70%；Arista 的 XPO 甚至把单模块冷却能力直接拉到 400W。说明功耗预算已经反过来决定技术路线。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx))

**瓶颈 7：认证与平台切换成本。**  
AOI 的 1.6T/800G 订单都要经过客户 qualification；Semtech 和 Credo 都在把 telemetry、link monitoring、ZeroFlap 当卖点，本质上就是因为大规模 AI 集群对“链路抖动”的容忍度极低。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

### **3）成本构成、毛利决定因素、价格传导机制**

**以 800G/1.6T 单模可插拔为例，我的 BOM 拆分大致如下（本文测算）：**

| 模块类型 | DSP/Retimer | 光引擎/激光器/PIC | Driver/TIA | PCB/连接器/壳体 | 热设计 | 组装校准测试 | 良率/保固 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 800G FRO | 22–28% | 25–35% | 8–12% | 8–12% | 5–8% | 12–18% | 5–10% |
| 1.6T FRO/LRO | 25–32% | 28–38% | 8–12% | 8–12% | 6–10% | 12–18% | 5–10% |
| CPO/NPO/光引擎 | 10–18% | 35–50% | 10–15% | 3–6% | 8–15% | 12–20% | 5–10% |

**毛利最强的，不是最重资产的一层，而是最稀缺的一层。**  
上游 DSP/SerDes 和稀缺激光器/SiPh/ELS 往往有更高结构性毛利：例如 Credo 的 Q3 FY26 非 GAAP 毛利率为 68.6%，Coherent 的 Q2 FY26 非 GAAP 毛利率为 39.0%，且 datacenter demand 仍强。相比之下，模块组装层在高景气期利润也很好，但长期更容易受 ASP 下行和客户压价影响。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

**价格传导机制：**  
上游紧缺时，价格先在 **激光器 / DSP / SiPh / 测试** 处稳定，再向模块传导；下游 hyperscaler 在 800G 成熟期更容易压模块 ASP，但在 1.6T 首轮导入、OCS/CPX/XPO 新形态、或带 telemetry/低 flap 的高可靠版本里，供应商仍有溢价权。Cisco、Ciena、Credo、Semtech 都在把“降功耗、降 flap、提升可维护性”直接变成卖点，本质就是定价依据。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx))

---

## **D. 竞争格局与壁垒（可量化）**

### **1）市场结构**

**我的判断：2026 的 AI 光互联市场会呈现“模块相对分散、DSP/激光器高度集中、OCS/CPO 极度早期集中”的结构。**

* \*\*高速模块层：\*\*按本文建模，**Top 5** 大概率拿走 **65–75%** 的 AI 800G/1.6T 价值量；其中中国龙头最强。仅 Google 一家，TrendForce 就预计 Innolight \+ Eoptolink 可能拿到接近 80% 的 800G+ 订单。([TrendForce](https://www.trendforce.com/presscenter/news/20260210-12919.html))  
* \*\*DSP/PHY/AEC 层：\*\*Broadcom、Marvell、Credo 三家形成主框架，按本文估算 **Top 3 \>85%**。Broadcom 在 400G/lane、TH6/CPO、retimer/AEC 全覆盖；Marvell 的 Ara 已批量供货；Credo 在 AEC、LRO、ZeroFlap 形成特色。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai))  
* \*\*激光器 / ELS / SiPh 核心器件：\*\*Coherent、Lumentum、AOI、Tower/SiPh 平台的集中度高，按本文估算 **Top 4 约 70–85%**。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-New-U-S--Manufacturing-Facility-to-Produce-Advanced-Lasers-for-the-Worlds-Largest-AI-Data-Centers/default.aspx))  
* \*\*OCS / CPO / CPX / XPO：\*\*市场还早，但标准与产品门槛极高，按本文估算 **Top 3/4 \>70%**。Cignal 说 OCS 供应商已达 20 家，但收入高度集中在少数先发方案上。([Cignal AI](https://cignal.ai/2025/12/the-optical-circuit-switching-market-4q25/))

### **2）壁垒清单：为什么能定价**

**壁垒 1：224G/200G-lane 的器件物理与量产良率。**  
能把 1.6T/3.2T 做成高良率，不是“会设计”就够，而是器件、封装、热、测试一起过关。Broadcom 400G/lane DSP+EML/PD、Lumentum 400G differential EML、Semtech 224G linear、Ciena 200G/lane CPX 都说明这层技术极少数厂商能做。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai))

**壁垒 2：垂直整合。**  
Eoptolink、Accelink、Source 都强调 optical engine 或芯片到模块的垂直能力；垂直整合带来更低功耗、更稳定交期、更快 debug，这就是定价基础。([Eoptolink](https://www.eoptolink.com/))

**壁垒 3：标准席位。**  
能进入 OCI、Open CPX、XPO、OIF、OCP OCS 的厂商，不只是跟标准，而是在塑造接口、热设计、管理面和生态。谁定义接口，谁就更容易拿平台租。([OCI MSA](https://oci-msa.org/))

**壁垒 4：客户 qualification 与平台绑定。**  
一旦进了头部 hyperscaler / AI lab 的平台，替换成本很高，因为要重做功耗、信号、可靠性、软件与供应链验证。AOI 的订单都明确写了 qualification 节点；Meta-Corning 则直接把光缆做成多年战略协议。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

**壁垒 5：可靠性与运维软件化。**  
AI 集群最怕 link flap 和瞬时故障，所以 telemetry、事件日志、远程诊断都能变成溢价。Credo 的 ZeroFlap、Semtech 的 link monitoring 都是典型例子。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Launches-800G-ZeroFlap-Optical-Transceivers-Engineered-for-AI-Networks/default.aspx))

**壁垒 6：测试与 burn-in 能力。**  
Aehr 这类 SiPh burn-in 设备厂能吃到很高壁垒红利，因为 2026 的核心不是会不会 demo，而是能不能稳定 HVM。([Aehr Test Systems](https://www.aehr.com/2026/03/aehr-wins-major-new-silicon-photonics-customer-with-high-power-fox-xp-wafer-level-burn-in-system-for-hyperscale-data-center-optical-interconnect-market/))

### **3）长期谁最可能拥有高 ROIC / 高毛利？**

**我给的排序是：**

**第一层：DSP / SerDes / AEC / 关键 PHY。**  
原因：IP、算法、系统兼容、客户锁定强，且资本开支相对模块装配更轻，ROIC 最漂亮。

**第二层：激光器 / ELS / SiPh 平台 / 光引擎。**  
原因：物理壁垒高、供给稀缺、可切入 CPO/NPO/OCS/400G-lambda，长期比纯模块装配更稳。

**第三层：CPO / OCS / scale-up optical 平台型公司。**  
原因：2026–2027 还早，但一旦生态形成，平台租会很厚。

**第四层：头部模块龙头。**  
原因：在 800G/1.6T 上仍能赚大钱，尤其拿到 hyperscaler 大单时；但长期毛利与 ROIC 的稳定性仍弱于上游 IC/器件层。

---

## **E. 2026 最可能发生的 3 个拐点**

### **拐点 1：1.6T 从“验证年”跨到“订单年”**

这已经发生了一半：AOI 拿到首个 1.6T volume order，Marvell 的 1.6T Ara 已在 global customers 批量供货，Tower-NVIDIA 明确把 1.6T SiPh 模块推到 NVIDIA networking 协议体系里。**我的判断是 2026H2 起 1.6T 会从“技术主题”变成“收入主题”。** ([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

### **拐点 2：optical scale-up 从“概念”跨到“联盟与接口锁定”**

2026 年 3 月的关键不是某一家公司又 demo 了什么，而是 OCI、Open CPX、XPO 三条线同时成形。**这通常意味着 2027–2028 的主赛道已经开始画框。** ([OCI MSA](https://oci-msa.org/))

### **拐点 3：OCS 从 Google/少数客户的架构优势，走向更开放的产业外溢**

OCP 单独为 OCS 建项目，Google 公开说自己已在 Jupiter/AI 网络广泛使用 Apollo OCS，Marvell-Lumentum 和 Accelink 也都在 OFC 2026 做 OCS 演示。**我判断 2026 是 OCS 从“客户私有优势”走向“开放产业机会”的元年。** ([Open Compute Project](https://www.opencompute.org/blog/the-open-compute-project-announces-new-optical-circuit-switching-ocs-project))

---

## **F. 头部公司全景图：按细分产品/技术尽量全覆盖**

\*\*说明：\*\*下面按当前公开材料做尽量全覆盖的代表性清单；“美股可买”指能否在美股主板/纳斯达克直接买到。技术参与度主要依据近半年公开产品、订单、联盟或会议材料。([InnoLight](https://www.innolight.com/data-center-networking/1.6t-osfp224))

### **1）高速可插拔光模块 / 光引擎**

* **中际旭创 / InnoLight**：已上市，**深交所创业板**；**美股主板否**  
* **新易盛 / Eoptolink**：已上市，**深交所创业板**；**美股主板否**  
* **光迅科技 / Accelink**：已上市，**深交所主板**；**美股主板否**  
* **AOI / Applied Optoelectronics**：已上市，**NASDAQ**；**是**  
* **Source Photonics**：**未上市**；**否**  
* **O-Net**：已上市，**港交所**；**美股主板通常否**  
* **华工正源 / 华工科技体系**：母公司已上市，**深交所主板**；**美股主板否**  
* **Cisco（模块/平台）**：已上市，**NASDAQ**；**是**  
* **Ciena（光引擎/相干/CPX）**：已上市，**NYSE**；**是**  
* **Arista（XPO 平台）**：已上市，**NYSE**；**是**

### **2）DSP / PHY / Retimer / AEC / 线性光芯片**

* **Broadcom**：已上市，**NASDAQ**；**是**  
* **Marvell**：已上市，**NASDAQ**；**是**  
* **Credo**：已上市，**NASDAQ**；**是**  
* **Semtech**：已上市，**NASDAQ**；**是**  
* **MaxLinear**：已上市，**NASDAQ**；**是**  
* **MACOM**：已上市，**NASDAQ**；**是**

### **3）CPO / NPO / CPX / XPO / optical scale-up**

* **NVIDIA**：已上市，**NASDAQ**；**是**  
* **Broadcom**：已上市，**NASDAQ**；**是**  
* **Marvell**：已上市，**NASDAQ**；**是**  
* **Ciena / Nubis 体系**：已上市，**NYSE**；**是**  
* **Arista**：已上市，**NYSE**；**是**  
* **Cisco**：已上市，**NASDAQ**；**是**  
* **Tower Semiconductor（SiPh）**：已上市，**NASDAQ / TASE**；**是**  
* **Eoptolink / Accelink / Source**：分别为 **深交所创业板 / 深交所主板 / 未上市**；**美股主板否**  
* **TeraHop**：**未上市**  
* **Ranovus**：**未上市**  
* **Ayar Labs**：**未上市**  
* **Celestial AI**：**未上市**  
* **Lightmatter**：**未上市**  
* **OpenLight**：**未上市**  
* **Xscape Photonics**：**未上市**

### **4）OCS（光路交换）**

* **Lumentum**：已上市，**NASDAQ**；**是**  
* **HUBER+SUHNER / Polatis 体系**：已上市，**瑞士证券交易所**；**美股主板通常否**  
* **Accelink**：已上市，**深交所主板**；**美股主板否**  
* **Marvell（互连配套）**：已上市，**NASDAQ**；**是**  
* **iPronics**：**未上市**  
* **Lumotive**：**未上市**  
* **Oriole Networks**：**未上市**  
* **Google（自用架构方，不是卖硬件的独立 OCS 上市公司）**：母公司 **NASDAQ**；**是**

### **5）激光器 / EML / VCSEL / 外置光源 / PIC**

* **Coherent**：已上市，**NYSE**；**是**  
* **Lumentum**：已上市，**NASDAQ**；**是**  
* **AOI**：已上市，**NASDAQ**；**是**  
* **Tower Semiconductor（SiPh foundry）**：已上市，**NASDAQ / TASE**；**是**  
* **OpenLight**：**未上市**  
* **Source Photonics**：**未上市**  
* **Sumitomo Electric**：已上市，**东京证券交易所**；**美股主板通常否**  
* **Furukawa Electric**：已上市，**东京证券交易所**；**美股主板通常否**  
* **Fujikura**：已上市，**东京证券交易所**；**美股主板通常否**

### **6）相干 / ZR / ZR+ / scale-across**

* **Ciena**：已上市，**NYSE**；**是**  
* **Cisco / Acacia 体系**：已上市，**NASDAQ**；**是**  
* **Marvell / Inphi 体系**：已上市，**NASDAQ**；**是**  
* **Nokia**：已上市，**NYSE / 赫尔辛基**；**是**  
* **Eoptolink**：已上市，**深交所创业板**；**美股主板否**

### **7）光纤 / 光缆 / 连接器 / 配线**

* **Corning**：已上市，**NYSE**；**是**  
* **Amphenol**：已上市，**NYSE**；**是**  
* **TE Connectivity**：已上市，**NYSE**；**是**  
* **CommScope**：已上市，**NASDAQ**；**是**  
* **Molex**：**未上市**  
* **Samtec**：**未上市**  
* **US Conec**：**未上市**  
* **SENKO**：**未上市**  
* **Sumitomo / Furukawa / Fujikura**：已上市，**东京证券交易所**；**美股主板通常否**

### **8）测试 / 认证 / burn-in / 量测**

* **Aehr**：已上市，**NASDAQ**；**是**  
* **Keysight**：已上市，**NYSE**；**是**  
* **Anritsu**：已上市，**东京证券交易所**；**美股主板通常否**  
* **EXFO**：**未上市**  
* **MultiLane**：**未上市**  
* **VeEX**：**未上市**  
* **Wilder Technologies**：**未上市**

---

## **最后的投资价值判断**

我对这个行业的判断是 **明确偏乐观**：

**第一，2026 不是光互联周期的尾声，而是“第二阶段的开端”。**  
第一阶段是 800G scale-out 大扩容；第二阶段是 1.6T \+ OCS \+ optical scale-up 标准化与导入。这个行业的增长逻辑，已经不只是“换代提速”，而是 **单颗 AI 加速器配套的光价值量在上升**。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382))

**第二，2026–2027 最值得押注的不是“所有光模块公司”，而是：**  
**1）拿到头部客户 design-win 的 1.6T 模块龙头；**  
**2）DSP/SerDes/AEC 龙头；**  
**3）激光器/ELS/SiPh/测试平台；**  
**4）OCS/CPO/OCI/XPO 的先发生态位。**  
其中第 1 类吃业绩弹性，第 2/3 类吃长期壁垒，第 4 类吃未来平台溢价。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

**第三，2026 最可能的错杀点，是市场把“CPO 还没全面放量”误解成“光互联见顶”。**  
真实情况恰好相反：**2026 的收入主线仍然是 800G/1.6T 可插拔与 AEC，CPO/OCS/optical scale-up 是下一波估值期权。** 这对投资更友好，因为你既有当期业绩，又有下一代架构溢价。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

**第四，最大的风险不是需求塌陷，而是 2027 可能出现的供给错配与库存波动。**  
LightCounting 明说 2027–2028 可能出现 soft landing 或 bumpy ride；所以最好的标的是那些 **既有当期订单、又在下一代架构里占生态位** 的公司，而不是只靠短期模块 ASP 的公司。([LightCounting](https://www.lightcounting.com/newsletter/en/march-2026-ethernet-optics-382))

如果只用一句话收尾：**2026 年光互联行业最可能的主路径，是“800G 继续冲量、1.6T 开始加速、AEC 守短距、OCS/CPO 锁未来”，而投资价值最高的环节，是能同时吃到“现在的量”和“下一代的接口定义权”的公司。**

According to documents from 2026-03-16 and 2026-04-09，结合过去半年尤其 2026Q1 的官方公告、OFC/OIF 技术材料、财报与订单信息，我对【1.6T LPO / LRO / 低功耗线性可插拔】行业的核心判断是：**2026 年不是 1.6T LPO 全面普及年，而是 1.6T 可插拔从 demo / qualification 迈向首批订单与量产爬坡年；最现实的主线不是一步跳到全 LPO，而是 1.6T FRO 先上量，LRO/RTLR 成为功耗与可运维性之间的最优过渡，LPO 先在头部 AI 集群短距链路局部导入，真正全面放量更大概率在 2027 年。** ([OIForum](https://www.oiforum.com/wp-content/uploads/01-LHUF-OIF-400G-Workshop.pdf?utm_source=chatgpt.com))

# **行业调研：1.6T LPO / LRO / 低功耗线性可插拔**

## **一、先给投资结论**

按项目内资料，2026–2027 的 AI 基础设施主背景仍是 **Blackwell / Blackwell Ultra 向 Rubin 过渡**，并行叠加 **Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA、Huawei Ascend** 等多条 ASIC/GPU 路线；而 NVIDIA 在 GTC 2026 已经把重点从“单芯片”切到 **AI factory、Spectrum-6/CPO、STX/CMX、液冷与 800VDC**。这决定了 800G 向 1.6T 的升级不是概念题，而是 AI scale-out 的现实题。

**我对这个行业的排序是：**

1. **2026 最确定的商业路径**：**224G SerDes \+ 1.6T OSFP/OSFP-RHS FRO 模块**，配合部分 **LRO/RTLR**；  
2. **2026 最值得加仓的弹性方向**：**224G DSP/retimer、224G 线性模拟前端、400G/lambda 光引擎/EML/UHP laser、1.6T 验证测试**；  
3. **2027 最可能的斜率变化**：**LRO 从验证走向放量，LPO 从局部 design-in 走向可见营收，XPO/CPO/NPO 对传统 pluggable 形成路线压力**。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Introduces-Cardinal-A-LowPower-1-6T-Optical-DSP-Family-Engineered-for-MassiveScale-AI-Fabrics/default.aspx))

一句话概括投资逻辑：**2026 是“1.6T可插拔商业化元年”，但真正高赔率的不是纯模块代工，而是“平台硅 \+ 关键光器件 \+ 验证 \+ 已拿到 hyperscaler 资格的模块龙头”。** ([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

---

## **二、过去半年最该看的正式材料与论坛**

最有信息密度的正式材料，不是泛行业报告，而是下面几类一手资料：

**1）OFC 2026**：几乎所有关键公司都把 1.6T/LPO/LRO 的真实路线端上桌面了。Cisco 发布了 **1.6T OSFP optic** 与 **800G LPO**；Arista 做了 **1.6T LPO/LRO/FRO 互通 demo** 并发布 **XPO**；Broadcom、Marvell、Semtech、Credo、Coherent、Lumentum、AOI、Source、Eoptolink 都在 OFC 上给出 224G/1.6T 的具体器件或模块路线。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

**2）OIF @ OFC 2026**：这是判断“技术是不是会从 demo 变成行业共识”的关键场子。OIF 当前工作已覆盖 **CEI-224G VSR/MR/LR** 与 **CEI-448G VSR/LR**；224G VSR 明确就是面向 **200/400/800/1600G 低功耗接口**；2026 OFC 期间 OIF 还在做 **CEI-224G/448G、EEI、co-packaging 的多厂互通演示**。此外，OIF 的 **RTLR**（Retimed Tx, Linear Rx）项目明确瞄准功耗、成本、时延下降，同时尽量保留 plug-and-play。([OIForum](https://www.oiforum.com/technical-work/hot-topics/common-electrical-i-o-cei-224g/?utm_source=chatgpt.com))

**3）NVIDIA GTC 2026**：这不是在直接卖 LPO/LRO，但它给出的是未来两年最重要的上层约束：Rubin、Spectrum-6、CPO、STX/CMX、AI factory、800VDC。换句话说，它定义了“为什么 1.6T 会成为必选项，以及为什么 1.6T 之后一定会被更高密度路线继续推着走”。 ([NVIDIA Developer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/))

**4）Cisco Live / Cisco 官方 AI 数据中心材料**：Cisco 公开给出 **800G LPO 功耗可比传统 retimed optics 低 50%**、整体交换系统功耗可降约 30%，并引用 Dell’Oro 的判断：**AI back-end 网络中多数交换端口将在 2027 年达到 1600G。** 这对节奏判断很关键。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

**5）Keysight / VIAVI 测试路线**：如果你想判断一个赛道是不是“真开始商用”，测试设备厂的动作很灵。Keysight 在 2026 年 3 月连续发布了 **224G/1.6T 验证平台、1.6T AI workload emulation、低功耗光互连验证**；VIAVI 也推出了面向 1.6T OSFP/AI fabric 的测试平台。([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0310_pr26-044-keysight-debuts-purpose-built-1-6t-ethernet-ai-workload-emulation-platform-to-validate-next-generation-ai-fabrics.html))

---

## **A. 2026 年的机遇、挑战、现用技术、成熟时间与最可能路径**

### **A1. 2026 年的机遇**

**机遇一：AI 后端网络端口速率切换，直接把 1.6T 从“可选升级”变成“结构性需求”。**  
224G/lane 已经从标准和器件层走到系统层。OIF 的 224G/448G 标准路线、Cisco 的 102.4T G300、Arista 的 1.6T 互通 demo、Broadcom/Marvell/Credo/Semtech 的 224G 器件发布，说明 1.6T 不是“还早”，而是已经进入 deployment 前夜。([OIForum](https://www.oiforum.com/technical-work/hot-topics/common-electrical-i-o-cei-224g/?utm_source=chatgpt.com))

**机遇二：低功耗路线正在从“实验室最优”转成“数据中心 TCO 最优”。**  
LPO 去掉模块内 DSP，LRO/RTLR 则保留发端 retiming、接收端线性化，是更温和的折中方案。Cisco 和 Lumentum都给过相对传统 DSP 光模块约 **50% 量级功耗改善** 的口径；Eoptolink 对 LRO 的口径是 **模块功耗约降 30%**。这在 AI 集群里不是小优化，而是会影响每柜功率预算、交换密度、散热和可布线性。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

**机遇三：AI 芯片路线越多，跨平台 Ethernet 互连价值越高。**  
项目内资料已经说明，2026–2027 的 AI 芯片不再是单一 NVIDIA 模式，而是 Blackwell/Rubin、TPU、Trainium、Maia、MTIA、Ascend 等多路线并行；在这种格局下，基于以太网的 800G/1.6T 光互连比单一封闭 fabric 更有扩散力。

### **A2. 2026 年的挑战**

**挑战一：LPO 的技术最优，不等于 2026 的商业最优。**  
LPO 要求 host ASIC、PCB、connector、module、FEC、CMIS/管理面共同收敛；Keysight 已把 224G 下的信号完整性、抖动、噪声、crosstalk、误码和验证效率列为 1.6T 的核心难点。LPO 能做到最低功耗，但也最依赖系统级共设计。([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0319_pr26-056-keysight-expands-1-6t-interconnect-validation-technology-to-include-passive-copper-and-low-power-optics.html))

**挑战二：OSFP 正在接近设计边界。**  
Arista 公开说 OSFP 仍会是未来几年最高量 form factor，但 AI 数据中心的带宽需求已经在密度、散热和可靠性上逼近 OSFP 设计包线，因此才推出 XPO，直接给出 **相对 1600G OSFP 约 4 倍前面板密度**。这说明 1.6T pluggable 不是终局，而是过渡高地。([Arista Networks Blog](https://blogs.arista.com/blog/ai-datacenters-are-reshaping-the-optics-industry?utm_source=chatgpt.com))

**挑战三：未来路线存在“被 CPO/XPO 提前截流”的风险。**  
NVIDIA 已公开把 Spectrum-X / Spectrum-6 的 photonics / CPO 放进 AI factory 叙事，并给出 **1.6T 端口 5 倍级网络功耗效率改善** 的方向性口径；Broadcom 也把 102.4T CPO 交换机推向出货；Arista 则用 XPO 提前卡位。也就是说，1.6T 低功耗 pluggable 赛道要在 2026–2027 快速兑现，否则 2028 后很可能被更高密度形态分流。([NVIDIA Developer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/))

### **A3. 目前真正被使用的技术**

现在真正“在用”而不是“在讲”的，按成熟度排序是：

**第一层：800G FRO 仍是主流，800G LPO 已经进入真实系统。**  
Cisco 已把 **800G LPO** 和 1.6T optic 一起放进正式产品公告；Arista 交换系统支持 LPO。2026 年实际出货量最大的“低功耗线性可插拔”大概率仍是 800G LPO，而不是 1.6T LPO。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

**第二层：1.6T FRO 已进入量产前夜，甚至已经出现首批收入/订单。**  
Coherent 在 2025 年就已披露 **1.6T datacom transceiver 首次收入**；AOI 在 2026 年 3 月拿到来自 major hyperscale customer 的 **首个 1.6T datacenter transceiver volume order，金额超过 2 亿美元**，计划 Q3 开始发货、Q4 完成。([Coherent Inc](https://www.coherent.com/content/dam/coherent/site/en/documents/investors/financial-releases/2025/august-13/earnings-release-fy25-q4.pdf))

**第三层：1.6T LRO/RTLR 正处于 sample/qualification 向 design win 过渡。**  
Omdia 在 2025 年公开判断是 **2025/2026 有 some deployment，真正 acceleration 从 2027 开始**；Arista、Semtech、Source、Eoptolink 在 OFC 2026 都把 LRO/RTLR 拉进 live demo 或量产组合。([OIForum](https://www.oiforum.com/wp-content/uploads/01-LHUF-OIF-400G-Workshop.pdf?utm_source=chatgpt.com))

**第四层：XPO/NPO/CPO 是下一代路线，但 2026 还不是主流出货形态。**  
这一点项目内资料和外部材料是一致的：2026 的主流仍是电 scale-up \+ 可插拔光；CPO/XPO 更像 2027 后的路线压力。 ([Arista Networks](https://www.arista.com/en/company/news/press-release/23697-pr-20260311?utm_source=chatgpt.com))

### **A4. 在“2026–2027 出货/装机最大的 AI 芯片”背景下，我对成熟时间和放量时间的判断**

按项目内资料，2026–2027 的主背景仍是 **Blackwell/Blackwell Ultra → Rubin**，外加 **TPU Trillium/Ironwood、Trainium2/3、MI350/MI450、Maia、MTIA、Ascend** 等多路线并行；共同特征是：**224G/200G-lane、液冷、功耗与 scale-out 压力同时抬升。**

基于这个背景，我的判断是：

* **1.6T FRO**：2026H2 商用品质基本成熟，**2027 全年放量**。  
* **1.6T LRO / RTLR / TRO**：2026 是 qualification 与首批 design-in 年，**2027 才是规模放量年**。  
* **1.6T LPO**：2026 在头部 AI 集群短距链路、tight host co-design 环境中局部导入，**更广泛放量更可能在 2027H2–2028**。  
* **XPO / NPO / CPO**：2026–2027 完成架构定案和少量试点，**2028 左右才会更系统性蚕食 pluggable**。([OIForum](https://www.oiforum.com/wp-content/uploads/01-LHUF-OIF-400G-Workshop.pdf?utm_source=chatgpt.com))

### **A5. 2026 年最可能的技术路径**

**如果只能选一条 2026 最可能的路径，我的答案是：**  
**224G SerDes 交换/网卡/ASIC \+ 1.6T OSFP/OSFP-RHS FRO 为主，LRO/RTLR 作为节能升级路径，LPO 只在少数头部 AI cluster 短距场景率先导入。**

换成更投资化的话说：  
**2026 真正最有把握赚钱的不是“赌 LPO 全面替代”，而是“赌 1.6T pluggable 上量 \+ LRO 快速渗透 \+ 224G 配套硅/光器件先挣钱”。** ([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

---

## **B1. 关键产品拆分与 2026–2027 市场规模区间（美元）**

下面所有数字，**都是我基于 Omdia / Cignal AI / Dell’Oro 公开判断、OIF 标准推进、以及 AOI 等一手订单自己建模的区间**；口径只统计 **AI 数据中心短中距高速互连相关产品**，**不含长距相干、不含整机交换机/服务器收入**，且不同层之间有重叠，**不能横向相加**。基准情景已经是偏乐观的。([OIForum](https://www.oiforum.com/wp-content/uploads/01-LHUF-OIF-400G-Workshop.pdf?utm_source=chatgpt.com))

**1）1.6T FRO 模块**  
2026E：保守 **$2.5B–$4.0B**；基准 **$4.5B–$6.5B**；乐观 **$6.5B–$9.0B**。  
2027E：保守 **$6B–$9B**；基准 **$9B–$13B**；乐观 **$13B–$18B**。  
份额路径（在 1.6T pluggables 内）：2026 大致 **75% / 60% / 50%**，2027 大致 **55% / 40% / 25%**。  
这是 2026 最确定的收入池。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

**2）1.6T LRO / RTLR 模块**  
2026E：保守 **$0.4B–$0.9B**；基准 **$0.9B–$1.8B**；乐观 **$1.8B–$3.0B**。  
2027E：保守 **$1.8B–$3.0B**；基准 **$3.0B–$5.2B**；乐观 **$5.2B–$7.5B**。  
份额路径（在 1.6T pluggables 内）：2026 大致 **15% / 22% / 20%**，2027 大致 **25% / 32% / 30%**。  
这是我认为 **2027 斜率最大、风险收益比最好** 的细分产品。([OIForum](https://www.oiforum.com/technical-work/hot-topics/energy-efficient-interfaces/))

**3）1.6T LPO 模块**  
2026E：保守 **$0.2B–$0.5B**；基准 **$0.5B–$1.2B**；乐观 **$1.2B–$2.2B**。  
2027E：保守 **$1.0B–$2.0B**；基准 **$2.0B–$4.0B**；乐观 **$4.0B–$6.5B**。  
份额路径（在 1.6T pluggables 内）：2026 大致 **5% / 12% / 25%**，2027 大致 **15% / 23% / 40%**。  
LPO 的上限最高，但 2026 的确定性不如 LRO。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

**4）1.6T Optical DSP / Retimer 芯片**  
2026E：保守 **$0.8B–$1.2B**；基准 **$1.2B–$1.8B**；乐观 **$1.8B–$2.5B**。  
2027E：保守 **$1.8B–$2.8B**；基准 **$2.8B–$4.0B**；乐观 **$4.0B–$5.5B**。  
这层是最有可能拿长期高毛利的层。([Broadcom](https://www.broadcom.com/company/news/product-releases/64036?utm_source=chatgpt.com))

**5）224G 线性模拟前端（TIA / Driver / Linear EQ）**  
2026E：保守 **$0.4B–$0.7B**；基准 **$0.7B–$1.1B**；乐观 **$1.1B–$1.6B**。  
2027E：保守 **$1.0B–$1.6B**；基准 **$1.6B–$2.4B**；乐观 **$2.4B–$3.2B**。  
这一层往往被低估，但在 LRO/LPO 扩散时弹性很大。([Semtech](https://www.semtech.com/company/press/semtech-launches-224-gbps-ic-family-for-linear-optics-era?utm_source=chatgpt.com))

**6）400G/lambda 光引擎、EML、UHP laser、SiPh light engine**  
2026E：保守 **$1.2B–$2.0B**；基准 **$2.0B–$3.0B**；乐观 **$3.0B–$4.2B**。  
2027E：保守 **$2.8B–$4.2B**；基准 **$4.2B–$6.0B**；乐观 **$6.0B–$8.5B**。  
真正拉长景气的，不只是模块，而是 400G/lambda 器件和光引擎。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx))

**7）AEC / ACC / HiWire 等超短距替代产品**  
2026E：保守 **$0.7B–$1.2B**；基准 **$1.2B–$1.8B**；乐观 **$1.8B–$2.6B**。  
2027E：保守 **$1.5B–$2.5B**；基准 **$2.5B–$3.8B**；乐观 **$3.8B–$5.2B**。  
对光模块是替代，但对“低功耗高速互连”是同主题受益。([Credo](https://credosemi.com/news/credo-announces-1-6tbps-osfp-xd-hiwire-aecs-targeting-hyperscaler-spine-switching/))

---

## **B2. 主流技术与新技术的 2026–2027 市场区间与渗透率路径**

这里的“渗透率”口径，指 **新建 AI 后端高速互连端口中的技术份额**，不是整个以太网市场。以下仍是我的建模。([OIForum](https://www.oiforum.com/wp-content/uploads/01-LHUF-OIF-400G-Workshop.pdf?utm_source=chatgpt.com))

**FRO（全 retimed optics）**  
2026E 市场：**$3.5B–$6.5B**；2027E：**$8B–$14B**。  
渗透率：2026 保守/基准/乐观约 **70% / 60% / 50%**；2027 约 **50% / 40% / 30%**。  
它是 2026 的现金牛，但不是终局。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

**LRO / RTLR / TRO（半 retimed）**  
2026E 市场：**$0.8B–$2.2B**；2027E：**$3B–$6B**。  
渗透率：2026 约 **10% / 20% / 25%**；2027 约 **20% / 30% / 35%**。  
这是我认为最有可能先成为“准主流”的低功耗路线。([OIForum](https://www.oiforum.com/technical-work/hot-topics/energy-efficient-interfaces/))

**LPO（全线性可插拔）**  
2026E 市场：**$0.5B–$1.5B**；2027E：**$2B–$5B**。  
渗透率：2026 约 **5% / 10% / 20%**；2027 约 **10% / 25% / 40%**。  
天花板最高，但 2026 不是大面积普及期。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

**XPO / NPO**  
2026E 市场：**\<$0.3B–$0.8B**；2027E：**$0.5B–$1.8B**。  
渗透率：2026 约 **0% / 2% / 4%**；2027 约 **2% / 7% / 12%**。  
它们不是 2026 营收主角，却是 2027–2028 估值主角。([Arista Networks](https://www.arista.com/en/company/news/press-release/23697-pr-20260311?utm_source=chatgpt.com))

**CPO（共封装光学）**  
2026E 市场：**\<$0.5B**；2027E：**$0.8B–$2.5B**。  
渗透率：2026 约 **0% / 1% / 3%**；2027 约 **2% / 5% / 10%**。  
2026 主要是架构定案和少量试点，不是大规模收入年。([NVIDIA Developer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/))

**AEC / ACC**  
2026E 市场：**$1.2B–$2.6B**；2027E：**$2.5B–$5.2B**。  
在超短距场景，它会持续挤压一部分光模块需求。([Credo](https://credosemi.com/news/credo-announces-1-6tbps-osfp-xd-hiwire-aecs-targeting-hyperscaler-spine-switching/))

---

## **C. 供给侧：产能结构、瓶颈、成本、毛利与价格传导**

### **C1. 产能结构：主要集中在哪些地区/公司/工艺**

**设计与平台硅** 主要在美国：Broadcom、Marvell、Credo、Semtech、Cisco、NVIDIA；工艺节点以 **3nm/5nm 级 DSP/SerDes \+ 更成熟节点的模拟/电源/管理芯片** 为主。Credo 已公开 3nm 224G optical DSP；Broadcom、Marvell 也都把 3nm / 224G / 1.6T 放到 2026 正式产品线上。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Introduces-Cardinal-A-LowPower-1-6T-Optical-DSP-Family-Engineered-for-MassiveScale-AI-Fabrics/default.aspx))

**晶圆制造与先进封装** 仍高度依赖台湾，尤其是 TSMC 及其先进封装能力；项目内资料也把 **HBM、先进封装、液冷、机架供电** 列为 2026–2027 上限约束。虽然 1.6T 模块不是 HBM 产品，但同一批 AI 基础设施资本开支会争抢相同的先进制造资源。

**光器件与模块装配** 则是 **中国大陆 \+ 东南亚 \+ 美国局部回流** 的格局：Eoptolink、InnoLight、Accelink、Source 等在中国端更强；Lumentum、Coherent、AOI 在美国端强化激光、器件和部分制造；AOI 正在扩建得州工厂，Lumentum 则新建美国 Greensboro 设施并明确 NVIDIA 为客户。([Eoptolink](https://www.eoptolink.com/about-us))

**电源/液冷/机柜集成** 的重心在台湾与北美：Delta 已明确 AI 数据中心液冷方案获 leading global CSPs/ODMs 认可并进入生产阶段。([\- Delta](https://www.deltaww.com/en-US/investors/chairman-statement))

### **C2. 至少 5 个关键供给瓶颈**

**1）224G 电通道与 PCB 材料。**  
真正卡住 LPO/LRO 的第一关，不是光，而是 host electrical channel。Source 与 Delta 的 demo 都强调了 **next-gen ultra-lossless PCB materials**；Keysight 则直接把 224G 下的 SI/jitter/noise 作为核心难点。([Source Photonics](https://www.sourcephotonics.com/news/source-photonics-and-delta-electronics-join-force-to-demo-1-6t-transceiver-and-switch-products-at-ofc26/?utm_source=chatgpt.com))

**2）400G/lambda 器件与封装良率。**  
1.6T 的底层不是“把 800G 简单翻倍”，而是进入 400G/lambda 的器件、EML、SiPh light engine、UHP laser、封装与热管理新阶段。Lumentum、Coherent、Marvell 都在推这一层。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx))

**3）热设计与 OSFP/OSFP-RHS 功耗包线。**  
Source 的 102.4T switch demo 已经写到 **支持最高 30W OSFP** 且双 **4.5kW PSU**；Arista 更直接承认 OSFP 已接近设计包线。([Source Photonics](https://www.sourcephotonics.com/news/source-photonics-and-delta-electronics-join-force-to-demo-1-6t-transceiver-and-switch-products-at-ofc26/?utm_source=chatgpt.com))

**4）多厂互通与认证。**  
OIF、Arista、Semtech、VIAVI、Keysight 在 2026 都把“互通”和“验证”放在前台，说明 1.6T 的瓶颈不只是谁能做出来，而是谁能在多家 switch/NIC/ASIC/OS 组合下 first-time-right。([OIForum](https://www.oiforum.com/meetings-events/oif-ofc-2026/?utm_source=chatgpt.com))

**5）外部激光与高端光源供给。**  
Lumentum新厂直接对准 AI 和 NVIDIA，Coherent 与 NVIDIA 签多年的先进光学合作，说明光源/光引擎不是充裕环节。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-New-U-S--Manufacturing-Facility-to-Produce-Advanced-Lasers-for-the-Worlds-Largest-AI-Data-Centers/default.aspx))

**6）验证测试产能。**  
当 Keysight 和 VIAVI 都在强调 1.6T/224G 测试平台时，意味着很多项目不是输在设计，而是输在“实验室吞吐率”。([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0310_pr26-044-keysight-debuts-purpose-built-1-6t-ethernet-ai-workload-emulation-platform-to-validate-next-generation-ai-fabrics.html))

**7）服务性与可维护性。**  
LPO/CPO 的理论功耗更好，但现场运维、热插拔、模块替换、故障定位并没有 pluggable/FRO/LRO 那么友好，所以 2026 先跑出来的仍是可插拔体系。([NVIDIA Developer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/))

### **C3. 成本与毛利：BOM、决定因素、价格传导**

下面的 BOM 是**按 1.6T FRO 模块做的建模估算**，不是某一家公司的官方成本表：

* 光引擎/laser/PD/PIC：**35%–40%**  
* DSP/retimer：**15%–22%**  
* TIA/driver/equalizer 等模拟前端：**8%–12%**  
* 封装/装配/测试/老炼：**12%–18%**  
* 散热件/壳体/连接器：**8%–12%**  
* 电源管理/MCU/EEPROM/PCB：**6%–10%**  
* 良率损耗/保固/物流：**5%–8%**

LRO 相对 FRO，**模块 BOM 大致可降 8%–15%**，功耗可降 **20%–35%**；LPO 相对 FRO，**模块 BOM 大致可降 15%–25%**，功耗可降 **30%–50%**，但会把部分成本转移到 host ASIC、PCB、connector、验证与系统软件上。这个迁移非常关键：**LPO 不是“凭空降本”，而是“把成本从模块侧转到系统侧”。** ([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

毛利的真正决定因素，不是“是不是 1.6T”，而是四件事：  
**一是是否有 hyperscaler qualification；二是是否垂直整合到 laser/PIC/light engine；三是 field failure / RMA 能否压住；四是能否把产品做进 switch/NIC/firmware 的整体验证矩阵。** Source 强调其垂直整合与已累计 **2,000 万颗以上高速 53GBd EML** 出货，就是典型的规模与良率护城河。([Source Photonics](https://www.sourcephotonics.com/news/source-photonics-to-spotlight-its-latest-optical-innovations-announce-to-receive-two-industry-awards-for-two-product-families-during-ofc26/))

价格传导机制也不是传统通信设备那种线性链条。它通常是：  
**上游器件/激光/DSP 紧缺 → 模块 lead time 拉长 → 先在 frame agreement 和季度议价中体现 → 当 multi-vendor interop 成熟后 ASP 迅速下滑。** 所以这个行业会同时出现“早期高毛利”和“后期快速价格竞争”。这也解释了为什么最稳的长期价值不一定在纯模块装配端。

---

## **D. 竞争格局与壁垒：谁能定价，谁能长期高 ROIC**

### **D1. 市场结构**

**1）224G DSP / retimer / SerDes 层：高度集中。**  
公开活跃、能真正打到 1.6T 主战场的主力就是 **Broadcom、Marvell、Credo、Semtech**，再加上 Cisco / NVIDIA 的系统级路线。我的估算是，**这一层的公开设计赢面 CR4 大概率超过 80%**。([Broadcom](https://www.broadcom.com/company/news/product-releases/64036?utm_source=chatgpt.com))

**2）1.6T 模块层：寡头但没到极端垄断。**  
公开活跃玩家大致是 **InnoLight、Eoptolink、Accelink、AOI、Source、Coherent、Lumentum** 等 7–8 家。我的估算是，**CR5 大致在 60%–75%**，但客户结构和区域分布差异很大。([CNINFO](https://static.cninfo.com.cn/finalpage/2025-08-27/1224585973.PDF))

**3）光引擎 / 激光 / UHP laser / SiPh 层：比模块更集中。**  
因为这层真正考验 IP、工艺和制造良率，所以长期更容易出现高毛利。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-New-U-S--Manufacturing-Facility-to-Produce-Advanced-Lasers-for-the-Worlds-Largest-AI-Data-Centers/default.aspx))

### **D2. 壁垒清单：为什么能定价**

**技术壁垒。**  
224G 时代不是“把速率翻倍”这么简单，而是电通道、封装、FEC、热、误码率一起上升；能跑通 1.6T live traffic 的公司天然更少，所以能定价。([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0319_pr26-056-keysight-expands-1-6t-interconnect-validation-technology-to-include-passive-copper-and-low-power-optics.html))

**规模壁垒。**  
Source 强调垂直整合和累计 EML 出货，AOI 拿到 \>$200M 订单，Lumentum/Coherent 则在扩产与 NVIDIA 绑定。规模意味着良率学习、交付能力和客户放心程度，所以能定价。([Source Photonics](https://www.sourcephotonics.com/news/source-photonics-to-spotlight-its-latest-optical-innovations-announce-to-receive-two-industry-awards-for-two-product-families-during-ofc26/))

**渠道与客户锁定。**  
能进 hyperscaler，不只是卖模块，而是卖进其资格名单、备用件体系、监控体系和 firmware matrix。一旦进了，切换成本非常高，所以能定价。

**认证标准壁垒。**  
OIF CEI-224G/448G、RTLR、CMIS、互通测试，并不是降低壁垒，而是把市场压缩到“真正能过认证的少数玩家”。过标准的人少，所以能定价。([OIForum](https://www.oiforum.com/technical-work/hot-topics/common-electrical-i-o-cei-224g/?utm_source=chatgpt.com))

**系统切换成本。**  
LPO/LRO/FRO 不是独立零件，而是和 ASIC、PCB、switch OS、遥测、故障处理耦合的。切换一个模块厂商，常常意味着整套 recertification，所以能定价。

### **D3. 哪一层最可能长期高 ROIC / 高毛利**

**我最看好三层：**

**第一层：merchant switch / optical DSP / SerDes 平台层。**  
Broadcom、Marvell、Credo 这类公司最容易长期高 ROIC，因为它们控制的是系统瓶颈与标准节奏，而不是单个模块 BOM。Credo FY26Q3 non-GAAP gross margin 已到 **68.6%**；Marvell FY26Q4 non-GAAP gross margin **59.0%**。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-Third-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

**第二层：差异化光器件 / 光引擎 / 激光。**  
Lumentum 和 Coherent 正在把 AI datacenter optics 从“通信零件”升级为“AI 关键部件”，并且已经与 NVIDIA 形成更深绑定。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-New-U-S--Manufacturing-Facility-to-Produce-Advanced-Lasers-for-the-Worlds-Largest-AI-Data-Centers/default.aspx))

**第三层：测试验证。**  
Keysight 和 VIAVI 本质上是“向复杂度收费”，而 1.6T/224G 时代最不缺的就是复杂度。([Keysight United States](https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0310_pr26-044-keysight-debuts-purpose-built-1-6t-ethernet-ai-workload-emulation-platform-to-validate-next-generation-ai-fabrics.html))

**相对没那么稳的层：纯模块装配。**  
它会在供给紧缺和客户认证稀缺时拿到阶段性高毛利，但一旦多家互通跑通，ASP 压力会来得很快。除非它同时拥有 laser/PIC/light engine 或 hyperscaler 绑定，否则长期不如平台硅和关键器件。

---

## **E. 2026 年最关键的 3 个变化与最可能放量的子方向**

### **拐点 1：1.6T 从“有样品”变成“有大单”**

AOI 在 2026 年 3 月拿到 **超过 2 亿美元** 的首个 1.6T volume order，并计划 Q3 开始发货、Q4 完成，这是一条非常强的一手验证：**1.6T 已不是纯演示，而是开始进 frame contract。** ([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))

### **拐点 2：LRO / RTLR 从概念变成最现实的过渡路线**

OIF RTLR、Semtech 的多厂 demo、Arista 的 1.6T LRO/LPO/FRO 互通，说明 2026 年行业在形成一种共识：  
**如果 LPO 太激进，那先上 LRO。**  
我认为这就是 2026 年最大的结构性变化。([OIForum](https://www.oiforum.com/technical-work/hot-topics/energy-efficient-interfaces/))

### **拐点 3：后 OSFP 路线提前浮出水面**

Arista 正式推 XPO，NVIDIA 把 CPO/photonics 写进 AI factory，Cisco 也在 silicon photonics 上推进 1.6T/800G LPO，这意味着市场不再把 1.6T OSFP 当终局。**2026 年最重要的不是 CPO 大放量，而是 2027–2028 的路线权已经开始分配。** ([Arista Networks](https://www.arista.com/en/company/news/press-release/23697-pr-20260311?utm_source=chatgpt.com))

### **2026 最可能放量的子方向**

如果只看 **1.6T**，最可能先放量的是：  
**1.6T FRO 模块、1.6T LRO 模块、224G DSP/retimer、224G 线性模拟前端、400G/lambda 光引擎/EML。**

如果看整个“低功耗线性可插拔家族”，2026 实际最先兑现营收的很可能是：  
**800G LPO \+ 1.6T FRO/LRO。** ([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx?utm_source=chatgpt.com))

---

## **F. 头部公司清单：按产品/技术分类，含是否上市、交易所、能否在美股买到**

下面按**公开活跃玩家**分层列示，优先列近半年在 OFC/OIF/公告/订单里有实质动作的公司。

### **1）交换芯片 / DSP / SerDes / 系统平台**

**Broadcom**（NASDAQ: AVGO，美股可买）、**Marvell**（NASDAQ: MRVL，美股可买）、**Credo**（NASDAQ: CRDO，美股可买）、**Semtech**（NASDAQ: SMTC，美股可买）、**Cisco**（NASDAQ: CSCO，美股可买）、**Arista**（NYSE: ANET，美股可买）、**NVIDIA**（NASDAQ: NVDA，美股可买）。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial))

这组公司里，**Broadcom / Marvell / Credo / Semtech** 更偏“卖关键硅”，**Cisco / Arista / NVIDIA** 更偏“卖系统级路线和平台”。

### **2）1.6T 模块 / LRO / LPO / 数据中心光模块**

**AOI / Applied Optoelectronics**（NASDAQ: AAOI，美股可买）、**Lumentum**（NASDAQ: LITE，美股可买）、**Coherent**（NYSE: COHR，美股可买）、**Eoptolink / 新易盛**（SZSE: 300502，A股，非美股主板直接交易）、**Zhongji InnoLight / 中际旭创**（SZSE: 300308，A股，非美股主板直接交易）、**Accelink / 光迅科技**（A股 002281，深市，非美股主板直接交易）、**Source Photonics**（未见公开上市代码，至少我未检到可在美股直接交易的公开证券）。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-events/press-releases))

其中：

* **AOI**：订单验证最强，2026 已有 \>$200M 的 1.6T hyperscaler 大单。([Applied Optoelectronics, Inc.](https://investors.ao-inc.com/news-releases/news-release-details/aoi-receives-first-volume-order-16t-data-center-transceivers))  
* **Coherent / Lumentum**：不仅卖模块，也卖器件/光源/平台，长期护城河更深。([Coherent Inc](https://www.coherent.com/news/press-releases/coherent-demonstrates-next-gen-pluggable-transceiver-ofc-2026))  
* **Eoptolink / 中际旭创 / 光迅 / Source**：是中国与全球 hyperscaler datacom 光模块链里最不能忽视的一组。

### **3）光器件 / 光引擎 / 激光 / Silicon Photonics**

**Lumentum**（NASDAQ: LITE）、**Coherent**（NYSE: COHR）、**AOI**（NASDAQ: AAOI）、**Marvell**（NASDAQ: MRVL）、**Broadcom**（NASDAQ: AVGO）、**Source Photonics**（未见公开上市代码）、**Eoptolink**（SZSE: 300502）。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-to-Join-the-SP-500-Index/default.aspx))

这层里我尤其看重 **Lumentum / Coherent / Marvell**，因为它们更直接站在 400G/lambda、UHP laser、SiPh light engine、未来 CPO/NPO 的节点上。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Demonstrates-Industry-Leading-Technologies-and-Products-for-Scale-Out-Scale-Up-and-Scale-Across-AI-Infrastructure-at-OFC-2026/default.aspx))

### **4）连接器 / AEC / ACC / 机柜互连 / 热管理**

**TE Connectivity**（NYSE: TEL，美股可买）、**Amphenol**（NYSE: APH，美股可买）、**Molex**（Koch 子公司，未上市，不能直接在美股买到）、**Delta Electronics**（TWSE: 2308，台股，非美股主板直接交易）、**Credo**（NASDAQ: CRDO，美股可买，AEC/HiWire 方向）。([TE Connectivity](https://investors.te.com/shareholder-info/default.aspx))

### **5）测试验证**

**Keysight**（NYSE: KEYS，美股可买）、**VIAVI**（NASDAQ: VIAV，美股可买）。([Keysight Investor Relations](https://investor.keysight.com/stock-information/stock-data-and-chart/default.aspx))

这一层虽然不是最“性感”的主题，但在 224G / 1.6T 阶段往往是最稳的卖铲子标的。

---

## **最后的判断**

**对 2026–2027，我是偏乐观的。**  
但我的乐观不是基于“LPO 立刻一统天下”，而是基于这条更现实的链条：

**AI 芯片与 AI 工厂继续上量 → 800G 向 1.6T 的端口升级确定性很高 → FRO 先吃收入，LRO 先吃渗透，LPO 先吃预期，XPO/CPO 先拿路线权。**

因此，这个行业最值得盯住的，不是一个抽象名词“LPO”，而是三类可兑现资产：

**第一类**，224G merchant DSP / retimer / analog front-end；  
**第二类**，400G/lambda 光引擎、EML、UHP laser、SiPh light engine；  
**第三类**，已经拿到 hyperscaler 资格且能跨 FRO/LRO/LPO 三种形态切换的模块龙头。([Credo Technology Group](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Introduces-Cardinal-A-LowPower-1-6T-Optical-DSP-Family-Engineered-for-MassiveScale-AI-Fabrics/default.aspx))

最需要警惕的是：**纯粹靠装配、没有 photonics/IP、又没有头部客户绑定的模块厂，2026 也许会很赚钱，但 2027 以后会同时面对 LRO/LPO 价格战和 XPO/CPO 路线挤压。**

如果要用一句最简洁的话做结论：  
**2026 年最可能的赢家不是“最激进的 LPO 叙事”，而是“能从 1.6T FRO 吃到当前收入、又能顺滑切到 LRO/LPO 的平台型公司”。**

根据 2026-03-16 与 2026-04-09 的项目文档，再结合 2026 年 1–4 月 OFC / GTC / 公司公告，我的核心判断是：**Package optical I/O / optical chiplets 已经从“技术验证题材”进入“AI 数据中心瓶颈层的工程化赛跑”，但 2026 年最先兑现收入的不会是 GPU 主封装全面光化，而是交换机侧 CPO、NPO/OBO、外置激光/光源和 SiPh foundry+先进封装测试；XPU 级 optical chiplet 的真正财务放量更像 2027–2028。** 项目内 AI 芯片主航道也支持这个判断：2026 的主流系统仍以 HBM3E+电互连+液冷大机架为主，2027 才更像 HBM4+更多光化，Rubin Ultra 的 direct optical connections 更像方向信号而不是 2026 全面现实。 ([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

# **行业调研：Package optical I/O / optical chiplets（2026）**

## **先给结论**

这是一个**非常值得提前布局、但要把时间轴看对**的方向。若你对 2026 AI 基础设施建设抱极乐观预期，我的结论是：

1. **2026 是订单/标准/验证拐点年，不是全面包内光化年。**  
2. **2027 才是第一轮真正财务放量年；2028 更可能是 XPU/package optical I/O 的放量年。**  
3. **最确定受益的层，不是“所有 GPU 都立刻上光I/O”，而是：交换机侧 CPO、ELS/高功率激光、SiPh foundry、先进封装与测试。**  
4. **弹性最大的层，是 optical chiplets / photonic fabric / UCIe optical，但执行风险也最大。** ([LightCounting](https://www.lightcounting.com/research-note/january-2026-cpo-waiting-for-green-light-from-customers-439))

第三方判断并不完全一致。**Yole/MGSSI 偏乐观**，认为 CPO 已到 adoption / inflection 点，2026 会进入实用化阶段；**LightCounting 更谨慎**，认为大规模部署仍要等至少一家 Top 5 cloud 给出采购绿灯。我的判断在两者中间：**2026 是“工程与采购拐点”，2027 是“收入与利润拐点”。** ([Optics](https://optics.org/news/photonics-packaging-market-to-triple-in-value-by-2031))

## **最近半年最值得看的正式与半正式材料**

**最值得盯的论坛/会议**，我按重要性排是：  
**OFC 2026**：这次不是普通光通信会，而是 AI 光互连的主战场。官方专门设置了 *Advanced Packaging and Co-Packaging for Efficient Optical Systems*，台上直接有 NVIDIA、AMD、Google、Nubis/Cisco，主题已经从 CPO 扩到 optical chiplets、AI fabrics 和 mixed-media socket。([\*\*\*\*TODO optica \*\*\*\*](https://www.ofcconference.org/program/special-events/advanced-packaging-and-co-packaging-for-efficient-optical-systems/))

**Photonics West 2026 / PIC Summit USA**：这是判断“产业有没有真的准备好量产”的最好风向标。LightCounting 会后给出的核心结论很关键：**客户接受度仍是最大障碍**，第一批部署更可能发生在愿意承担风险的小型 AI 集群，而不是一上来就全行业铺开。([LightCounting](https://www.lightcounting.com/research-note/january-2026-cpo-waiting-for-green-light-from-customers-439))

**GTC 2026**：这不是讲 optics 的会议，但它给了最强的需求侧信号。项目文档里已经很清楚：NVIDIA 在卖的是 AI Factory，而不是单 GPU；Rubin Ultra 对 direct optical connections 的表述，说明“网络先光化、XPU 后光化”是官方路线的一部分。

**Yole 2026 / Lam 联合议题**：Yole 认为 photonics packaging 市场会从当前约 **45 亿美元**增长到 2031 年 **144 亿美元**，其中 **CPO 相关需求到 2031 年约 50 亿美元**，几乎从零起步；这给了这个赛道很好的中长期上沿。([Optics](https://optics.org/news/photonics-packaging-market-to-triple-in-value-by-2031))

---

## **A. 2026 年的机遇、挑战、现有技术与未来成熟时间**

### **1）2026 年为什么会有大机会**

AI 集群已经把**电互连的三个天花板**同时顶出来了：**功耗、带宽、距离**。Siemens 的总结很到位：当节点带宽超过 100Tb/s、集群需要数百万条高速链路时，铜互连在带宽/瓦、重定时开销和信号完整性上都开始失效；GF 也直接说数据中心正逼近电互连极限，silicon photonics 已经成为可扩展路径。([Siemens Blog Network](https://blogs.sw.siemens.com/semiconductor-packaging/2026/02/05/five-key-trends-of-co-packaged-optics-cpo-in-2026/))

而且需求不是空想。NVIDIA 已把 Spectrum‑X / Quantum‑X photonics 推到产品层，Broadcom 已把 **102.4T CPO switch、400G/lane optical DSP、3.5D XDSiP XPU** 推到量产/展示层；Anthropic 则与 Google/Broadcom 签下了从 2027 年开始的**multiple gigawatts TPU capacity** 协议。换句话说，**AI 基础设施不是在讨论要不要更强光互连，而是在抢谁先把它工程化。** ([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

### **2）2026 年的核心挑战**

真正的难点不是“光能不能传”，而是五件事一起成立：**热、可维护性、测试、标准、客户绿灯**。  
LightCounting 认为客户接受度仍是最大阻碍；MGSSI 明确写到 ELS 已成为主流思路，因为热敏感的激光器不适合直接靠近高热 ASIC；Siemens 认为 CPO 真正的主瓶颈是 production-scale optical/electrical test 与 KGD；Lightmatter 推出的 vClick，本质上是在解决“可拆光纤阵列 \+ known-good optical engine \+ serviceability”这组现实问题。([LightCounting](https://www.lightcounting.com/research-note/january-2026-cpo-waiting-for-green-light-from-customers-439))

### **3）目前已经在用、或已进入工程化的技术**

我把这个赛道按 2026 的真实成熟度分三层：

**第一层：已经在大规模使用的桥接技术。**  
800G / 1.6T pluggable optics 仍是主流，且 silicon photonics 在 2026 年会占到**超过一半的光模块销量**；短距仍大量依赖 ACC/AEC/copper。也就是说，2026 的现实不是“直接一步到 package optical I/O”，而是**先把 SiPh 模块、1.6T 交换和液冷/高压直流配套吃透**。([LightCounting](https://www.lightcounting.com/research-note/november-2025-the-year-of-silicon-photonics-2026-436))

**第二层：2026 年开始兑现收入的近端技术。**  
这层是 **switch-side CPO \+ NPO/OBO \+ ELS/ELSFP**。NVIDIA 的 Spectrum‑X Ethernet Photonics 明确写到 **2H26 可用**；Broadcom 的 Tomahawk 6–Davisson CPO、102.4T Tomahawk 6 已是 production volume；Lightmatter 的 Passage L20 把 **NPO/OBO** 做成 224G PAM4、6.4Tbps each direction 的“drop-in bridge”，预计 **late 2026 sampling**。([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

**第三层：最性感、但更偏 2027–2028 的新技术。**  
这里才是 **optical I/O chiplets / photonic fabric / UCIe optical / package-to-package optical**。Ayar 的 TeraPHY 是 UCIe 兼容的 optical I/O chiplet；Marvell/Celestial 的 Photonic Fabric chiplet 直接打到 **16Tbps/单芯粒**，但 Marvell 自己给的节奏是 **2H FY2028 才开始 meaningful revenue**；这说明技术方向很对，但财务放量不会像 PPT 那么早。([Ayar Labs](https://ayarlabs.com/teraphy/))

### **4）在项目内“2026–2027 出货最大的 AI 芯片路径”背景下，我的成熟时间判断**

结合项目文件里 Blackwell/GB300、Rubin、MI350/MI450、Trillium/Ironwood、Trainium2/3、Maia 200、MTIA、Ascend 等主线可以看出：**公开资料里，2026–2027 的大出货 AI 芯片绝大多数仍是电互连主导，光先进入网络/交换与部分 custom XPU scale-up，而不是先进入主流 GPU 主封装。**

我的时间判断是：

* **交换机侧 CPO**：2026 成熟，**2H26–2027 放量**。  
* **NPO/OBO**：2026 工程成熟，**2027 放量**。  
* **ELS / 高功率 DWDM light source**：2026 小批量，**2027 放量**。  
* **XPU optical I/O chiplets**：2026–2027 完成头部客户 qualification，**2027 小批量、2028 基准放量**。  
* **光学 scale-up fabric / package-to-package optical**：2026–2027 做 design-in，**2028 起放量**更合理。([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

### **5）这个行业在 2026 年最可能的技术路径**

我给一个很明确的判断：**2026 年最可能的路径是“先交换机、后 XPU；先机架/板级、后封装内；先 ELS/NPO/OBO、后真正 UCIe optical chiplet”。**

再说白一点，就是：

**2026 主路径 \= 1.6T/3.2T 过渡 \+ switch-side CPO \+ NPO/OBO bridge \+ ELSFP remote light sources \+ OCS 试点；**  
**2027 主路径 \= custom XPU optical scale-up \+ first package optical I/O deployments；**  
**2028 才更像真正的 package optical I/O 扩散。** ([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

---

## **B. 产品与技术的 2026–2027 市场规模、渗透率与增长路径**

下面这些数**不是第三方现成口径**，而是我基于以下锚点做的**偏乐观 bottom-up 模型**：  
Yole 对 photonics packaging / CPO 的 2031 规模，Dell’Oro 对 1.6T 交换首年放量判断，Lumentum 的 OCS backlog 和 CPO 订单，Marvell/Celestial 的 revenue 时点，Ayar/Lightmatter 的量产与 sampling 节奏，以及项目里对 2026–2027 AI 基建的乐观假设。渗透率分母统一定义为：**当年新增部署的高端 AI scale-up / scale-out 链路或相关 XPU package**，不是全行业所有光模块。([Optics](https://optics.org/news/photonics-packaging-market-to-triple-in-value-by-2031))

### **B1. 按产品拆分**

**1）交换机侧 CPO / CPO 光引擎 / CPO 交换机**  
2026：**$0.3–0.5B / $0.6–0.9B / $1.2–1.6B**（保守/基准/乐观）  
2027：**$0.8–1.2B / $1.5–2.2B / $3.0–4.0B**  
渗透率：2026 **2–4% / 5–10% / 10–18%**；2027 **8–12% / 15–25% / 25–40%**。  
这是 2026 最先兑现的收入池，因为 NVIDIA 与 Broadcom 的产品节奏最清晰。([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

**2）NPO / OBO 光引擎（作为过渡桥接）**  
2026：**$0.15–0.3B / $0.3–0.5B / $0.7–1.0B**  
2027：**$0.35–0.6B / $0.7–1.2B / $1.5–2.2B**  
渗透率：2026 **4–8% / 8–15% / 15–25%**；2027 **10–18% / 18–30% / 30–45%**。  
这是我最看好的“2026 桥接路线”，因为它最容易嵌入现有 XPU / switch PCB 与 224G PAM4 设计。([Lightmatter®](https://lightmatter.co/press-release/lightmatter-expands-photonic-interconnect-roadmap-with-passage-l20-unified-optical-engine-for-npo-and-obo-applications/))

**3）XPU 侧 optical I/O chiplets / photonic fabric chiplets**  
2026：**$0.05–0.1B / $0.1–0.2B / $0.25–0.4B**  
2027：**$0.15–0.3B / $0.4–0.8B / $1.2–1.8B**  
渗透率（分母=新增 custom XPU scale-up packages）：2026 **0.2–0.5% / 0.5–1.5% / 1.5–3%**；2027 **1–3% / 3–8% / 8–15%**。  
这是最有想象力的部分，但要尊重 Marvell 自己给出的收入时点，别把放量想得太早。([Ayar Labs](https://ayarlabs.com/teraphy/))

**4）ELS / ELSFP / DWDM laser source / 高功率光源**  
2026：**$0.2–0.35B / $0.35–0.55B / $0.7–1.0B**  
2027：**$0.45–0.7B / $0.8–1.2B / $1.5–2.0B**  
这层是我认为最容易超预期的细分，因为几乎所有 CPO/NPO 路线最后都要落到光源的功率密度、波长稳定和可维护性上，Lumentum 已经给出 backlog/订单，Lightmatter 和 Tower/Scintil 也都在打这条线。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

**5）SiPh foundry \+ advanced packaging / test（窄口径，只算 package optics 相关）**  
2026：**$0.3–0.5B / $0.5–0.8B / $1.0–1.4B**  
2027：**$0.6–0.9B / $1.0–1.5B / $2.0–2.8B**  
这层最像“卖铲子”，确定性高于光I/O芯粒本体。TSMC、GF、Tower 都在给 very specific 的 production 信号。([TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_connectivity))

**我给这个赛道的窄口径总盘子：**  
2026：**$1.0–1.5B / $1.8–2.8B / $3.5–5.0B**  
2027：**$2.2–3.5B / $4.5–6.5B / $8.0–11.0B**。  
如果你把 OCS、相关 SiPh 模块和更宽口径 packaging services 算进去，2027 的乐观值还能更高。([Optics](https://optics.org/news/photonics-packaging-market-to-triple-in-value-by-2031))

### **B2. 按技术路线拆分**

**主流技术（2026 真正在用）**：  
**SiPh pluggables \+ 电互连 \+ 短距铜**仍是主流底座；LightCounting 预计 2026 超过一半光模块销量会基于 SiPho modulators。这个“旧技术”其实仍然是 2026 的大收入池。([LightCounting](https://www.lightcounting.com/research-note/november-2025-the-year-of-silicon-photonics-2026-436))

**未来两年增长最快的新技术**：  
增长斜率我排序为：**switch-side CPO \> ELS/light source \> NPO/OBO \> optical chiplets \> OCS in scale-up fabrics**。  
原因很简单：越靠近现有交换与机架架构，越容易先吃到订单；越深进 XPU 封装，越受制于热、测试、良率和客户 risk tolerance。([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

---

## **C. 供给侧：产能结构、瓶颈、成本与毛利**

### **1）产能结构：地区 / 公司 / 工艺**

**台湾**是最关键的制造与系统集成重心。  
TSMC 已公开 65nm silicon photonics 量产，并在做 3D stacked CPO；ASE/SPIL 是封装能力核心；Wiwynn、Foxconn、LITEON 等则掌握机架、系统集成和模块落地。([TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_connectivity))

**美国**最强在系统架构、交换芯片、光引擎、激光与设计平台。  
NVIDIA、Broadcom、Marvell、Ayar Labs、Lightmatter、Lumentum、Coherent、GF 都是这一层的核心。([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

**以色列 / 日本 / 美国 / 新加坡**是 SiPh foundry 的重要补充。  
Tower 的产线分布在以色列、美国、日本；GF 通过 AMF 把新加坡纳入版图，并强调自己是唯一高量产 300mm CMOS SiPh pure-play foundry。([Tower Semiconductor](https://towersemi.com/2026/02/05/02052026/))

### **2）至少 8 个现实瓶颈**

**瓶颈 1：热管理与波长漂移。**  
光器件离多千瓦 XPU 太近，热耦合、波长漂移、激光效率衰减都会立刻放大，所以 ELS 方案在 2026 事实上成了主流折中。([Siemens Blog Network](https://blogs.sw.siemens.com/semiconductor-packaging/2026/02/05/five-key-trends-of-co-packaged-optics-cpo-in-2026/))

**瓶颈 2：可维护性。**  
传统 CPO 如果内部光器件坏掉，可能拖累整个高价值 package 报废。Lightmatter 的 vClick 就是在解决 detachable fiber \+ field serviceability。([Lightmatter®](https://lightmatter.co/press-release/lightmatter-unveils-vclick-optics-industry-first-detachable-fiber-array-unit-for-cpo-advanced-packaging-and-high-volume-production/))

**瓶颈 3：Known-Good Optical Engine / KGD 测试。**  
Siemens 直接点名 production-scale optical/electrical test 是主瓶颈；Lightmatter 也强调要在 final integration 前验证 known-good optical engines。([Siemens Blog Network](https://blogs.sw.siemens.com/semiconductor-packaging/2026/02/05/five-key-trends-of-co-packaged-optics-cpo-in-2026/))

**瓶颈 4：光纤耦合与装配良率。**  
微米级偏差就会带来明显损耗，且不同 PIC / laser / package 组合的敏感性都不同。([Siemens Blog Network](https://blogs.sw.siemens.com/semiconductor-packaging/2026/02/05/five-key-trends-of-co-packaged-optics-cpo-in-2026/))

**瓶颈 5：光源功率密度与可靠性。**  
Lightmatter 明确指出传统离散 InP 激光 \+ ELSFP 方案会碰到 front-panel 空间、热损伤和波长控制问题；Lumentum/Coherent/Tower/Scintil 都在围绕这个 choke point 发力。([Lightmatter®](https://lightmatter.co/press-release/lightmatter-introduces-guide-light-engine-for-ai-featuring-vlsp-technology/))

**瓶颈 6：标准仍在形成。**  
OCI MSA、XPO MSA、OIF 都在推进，但机械接口、热规格、optical attach、qualification flows 还没像 pluggables 那样成熟。([Broadcom Inc.](https://investors.broadcom.com/node/64036/pdf))

**瓶颈 7：PIC foundry 与先进封装能力。**  
TSMC、GF、Tower 都在强调 volume/3D/2.5D/co-packaging 能力，反过来说明这仍是稀缺资源。([TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_connectivity))

**瓶颈 8：客户绿灯。**  
LightCounting 说得很直接：高 volume deployment 要等至少一家 Top 5 cloud 真正给出绿灯。([LightCounting](https://www.lightcounting.com/research-note/january-2026-cpo-waiting-for-green-light-from-customers-439))

### **3）成本与毛利：我给的可制造 BOM 框架**

公开市场几乎没有可直接引用的完整 BOM，我给一个**工程上合理的建模**：

**交换机侧 CPO / NPO 光学子系统 BOM**，大致可以看成：  
PIC/EIC/driver/DSP **25–35%**；激光/光源 **15–25%**；封装、fiber attach、测试 **20–30%**；热管理、socket/connector、控制与冗余 **15–25%**。

**XPU 侧 optical chiplet 子系统 BOM**，大致是：  
optical chiplet die / photonic fabric die **20–30%**；光源 **15–25%**；先进封装 / interposer / co-packaging **25–35%**；fiber attach \+ test **15–25%**；控制/固件/IP **10–15%**。

我的结论是：**真正决定毛利的不是材料成本，而是良率、测试、可维护性和客户锁定。** 一旦 optical engine / light source 被锁进某一代 XPU 或 switch package，它的价格锚就不是“一个光模块值多少钱”，而是“每 bit 功耗省多少、front-panel 和 retimer 少多少、能否把更多 HBM / die edge 释放出来”。Marvell/Celestial 明说 optical fabric 可以释放 die edge，转而容纳更多 HBM，这就是最典型的“为什么能定价”。([SEC](https://www.sec.gov/Archives/edgar/data/1835632/000119312525305289/d34367dex991.htm))

---

## **D. 竞争格局与壁垒：谁最可能长期高 ROIC / 高毛利**

### **1）市场结构：今天很窄，明天很大**

**交换机侧 CPO** 目前是明显的寡头起跑。公开能看到 production-class 节奏的，核心就是 **NVIDIA \+ Broadcom**，Marvell 更偏 custom XPU / scale-up 侧。我自己的估计是：**Top 2 在 2026 年公开可见的 production-grade CPO design-in 价值池里，大概率占到 70% 以上。** 这不是审计口径，是基于已公开量产、availability 和生态 breadth 的推断。([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

**optical chiplets / photonic fabric** 这边则是“3 家半”格局：**Ayar Labs、Marvell/Celestial、Lightmatter** 是最强的公开管线；Intel/AMD 更像有路线但尚未公开大规模商用品。这里我会判断 **Top 3 占 visible pipeline 80%+**。([Ayar Labs](https://ayarlabs.com/news/ayar-labs-closes-500m-series-e-accelerates-volume-production-of-co-packaged-optics/))

### **2）壁垒清单：为什么能定价**

**技术壁垒**：不是单一 PIC，而是**电\-光-热-封装-测试联合优化**。这决定了后来者即便能做出器件，也不一定能做出可量产系统。([Siemens Blog Network](https://blogs.sw.siemens.com/semiconductor-packaging/2026/02/05/five-key-trends-of-co-packaged-optics-cpo-in-2026/))

**规模壁垒**：foundry、OSAT、laser、fiber attach、system integration 要一起爬坡；Ayar 融 5 亿美元去扩 volume production and test，本身就说明规模门槛有多高。([Ayar Labs](https://ayarlabs.com/news/ayar-labs-closes-500m-series-e-accelerates-volume-production-of-co-packaged-optics/))

**渠道/客户锁定**：一旦被锁进 hyperscaler 的 XPU/switch/rack 路线，替换供应商会牵动 package、冷却、测试、布线、协议，切换成本非常高。([Ayar Labs](https://ayarlabs.com/news/ayar-labs-and-wiwynn-partner-to-bring-co-packaged-optics-to-rack-scale-ai-systems/))

**标准与认证壁垒**：OCI MSA、XPO MSA、OIF 等标准仍在形成，先入局者更容易定义接口、测试与资格。([Broadcom Inc.](https://investors.broadcom.com/node/64036/pdf))

**切换成本**：CPO/NPO 不像换一颗 pluggable。它是换整个 package / board / rack 物理架构，所以能够形成更强的议价权。([Lightmatter®](https://lightmatter.co/press-release/lightmatter-unveils-vclick-optics-industry-first-detachable-fiber-array-unit-for-cpo-advanced-packaging-and-high-volume-production/))

### **3）价值链里谁最可能长期高 ROIC / 高毛利**

我给的排序是：

**第一层：平台型 CPO / optical engine / photonic fabric 供应商。**  
因为它们拿的是“体系结构席位”，而不是零件席位。Broadcom、NVIDIA、Ayar、Lightmatter、Marvell/Celestial 都在这个层。([Broadcom Inc.](https://investors.broadcom.com/node/64036/pdf))

**第二层：高功率 laser / ELS / DWDM light source。**  
这层是最容易从“配角”变成瓶颈的。Lumentum、Coherent、Scintil/Tower、Lightmatter Guide 都说明这一层在往上游抬价。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

**第三层：SiPh foundry \+ advanced packaging/test。**  
不一定毛利最高，但**ROIC 很可能很高**，因为它是稀缺产能 \+ 量产 know-how。TSMC、GF、Tower、ASE/Amkor 都值得高看一眼。([TSMC](https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_connectivity))

**相对不那么理想的层**：纯 commodity transceiver / cable / generic assembly。它们也会受益，但长期更容易被 price-down。

---

## **E. 2026 年最可能发生的 3 个关键拐点**

**拐点 1：交换机侧 CPO 从“看展会”走向“真正部署”。**  
NVIDIA 的 Spectrum‑X Photonics 已明确写到 **2H26**；Broadcom 的 Tomahawk 6 CPO / 102.4T 已是 production volume。2026 很可能是“CPO 终于不只是 demo”的第一年。([NVIDIA](https://www.nvidia.com/en-us/networking/products/silicon-photonics/))

**拐点 2：标准开始进入采购清单，而不只是论坛清单。**  
OCI MSA 和 XPO MSA 的意义非常大：它们把光互连从“某家厂商 proprietary trick”往“hyperscaler 可采购的多供应商规范”推进。([OCI MSA](https://oci-msa.org/))

**拐点 3：光源、serviceability、test 这三个 choke point 被头部客户验证。**  
Lumentum 已给出 **OCS backlog 超过 $400M** 和 **1H27 交付的 multi-hundred-million-dollar CPO order**；Lightmatter 用 vClick 解决 detachable fiber / KGOE；Ayar/Wiwynn 已经把 reference rack 做出来。谁先把这三件事闭环，谁就先拿到 hyperscaler 绿灯。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Second-Quarter-of-Fiscal-Year-2026-Financial-Results/default.aspx))

---

## **F. 公司全景图：头部公司、上市状态、交易所、是否能在美股买到**

我按“能否直接映射到这个赛道的收入”来分层。

### **1）交换机 / CPO 平台 / AI fabric**

* **NVIDIA**：上市；NASDAQ：**NVDA**；**美股可直接买**  
* **Broadcom**：上市；NASDAQ：**AVGO**；**美股可直接买**  
* **Marvell**：上市；NASDAQ：**MRVL**；**美股可直接买**  
* **Cisco**：上市；NASDAQ：**CSCO**；**美股可直接买**  
* **Arista**：上市；NYSE：**ANET**；**美股可直接买**  
* **AMD**：上市；NASDAQ：**AMD**；**美股可直接买**  
* **Intel**：上市；NASDAQ：**INTC**；**美股可直接买**

### **2）optical I/O chiplets / photonic fabric / CPO 创新平台**

* **Ayar Labs**：未上市；**美股不可直接买**  
* **Lightmatter**：未上市；**美股不可直接买**  
* **Celestial AI**：**已被 Marvell 收购**；不可单独交易  
* **Ranovus**：未上市  
* **Scintil Photonics**：未上市  
* **POET Technologies**：上市；NASDAQ：**POET**；**美股可直接买**  
* **AMD / Enosemi**：Enosemi 已并入 AMD，间接通过 **AMD** 参与  
* **Intel Silicon Photonics / Optical I/O 路线**：通过 **INTC** 间接参与 ([Ayar Labs](https://ayarlabs.com/news/ayar-labs-closes-500m-series-e-accelerates-volume-production-of-co-packaged-optics/))

### **3）laser / ELS / InP / VCSEL / 光源**

* **Coherent**：上市；NYSE：**COHR**；**美股可直接买**  
* **Lumentum**：上市；NASDAQ：**LITE**；**美股可直接买**  
* **POET**：上市；NASDAQ：**POET**；**美股可直接买**  
* **Sumitomo Electric**：上市；东京证券交易所：**5802**；**不是美股主板直买**  
* **LITEON**：上市；台湾证券交易所：**2301**；**不是美股主板直买**  
* **Scintil Photonics**：未上市

### **4）SiPh foundry / 封装测试 / 系统集成**

* **TSMC**：上市；TWSE：**2330**；NYSE ADR：**TSM**；**美股可通过 ADR 买**  
* **GlobalFoundries**：上市；NASDAQ：**GFS**；**美股可直接买**  
* **Tower Semiconductor**：上市；NASDAQ / TASE：**TSEM**；**美股可直接买**  
* **ASE Technology**：上市；NYSE ADR：**ASX**；**美股可直接买**  
* **Amkor**：上市；NASDAQ：**AMKR**；**美股可直接买**  
* **Fabrinet**：上市；NYSE：**FN**；**美股可直接买**  
* **Wiwynn**：上市；台湾证券交易所：**6669**；**不是美股主板直买**  
* **Hon Hai / Foxconn**：上市；台湾证券交易所：**2317**；**不是美股主板直买**

---

## **最后的投资判断**

如果你的前提是**2026 AI 计算中心建设非常强**，那我会把这个行业的投资价值分成两段看：

**第一段，2026 就可能兑现的确定性收益**：  
**NVIDIA / Broadcom / Marvell** 这类平台层；**Coherent / Lumentum** 这类光源层；**TSMC / GF / Tower / ASE / Amkor** 这类 foundry/封装测试层。

**第二段，2027–2028 才会爆发的高弹性收益**：  
**Ayar Labs、Lightmatter、Marvell/Celestial 这类 optical chiplet / photonic fabric 平台。**

真正需要避免的误判只有一个：**把 2026 误判成“GPU 主封装全面光化年”。** 更准确的说法是：**2026 是“交换机先光化、机架先光化、标准先成形”的一年；2027 才是 chiplet/package 光I/O 开始有像样收入的第一年。** ([LightCounting](https://www.lightcounting.com/research-note/january-2026-cpo-waiting-for-green-light-from-customers-439))

如果你后面要继续推进，我建议下一步直接做一个\*\*“美股可交易标的 \+ 私有公司观察名单 \+ 2026/2027 事件触发器”\*\*版本。

According to a document from 2026-04-09，结合项目内两份底稿和近半年一手资料，我的核心结论是：\*\*2026 年这个赛道的主线不是“CPO 立刻全面替代可插拔”，而是 AI 集群把交换侧光互连从“可选优化”升级成“系统上限”；最可能路径是“1.6T 可插拔/LPO 先放量，VCSEL-based NPO 先导入，交换侧 SiPh CPO \+ 外置激光在头部集群小批量爬坡”，真正更明显的放量点在 2027 年。\*\*项目内资料也指向这一点：2026 主量仍是 Blackwell/GB300、MI350/450、Trainium、Ironwood、Maia、MTIA、Ascend 等，Rubin 在 2H26 导入、2027 才进入主线，这决定了 2026 的网络光学仍以“先解决密度、功耗、可维护性”而非“全面上封装光” 为主。 ([TrendForce](https://www.trendforce.com/presscenter/news/20260311-12962.html))

# **行业调研：【CPO / NPO 交换侧光引擎 \+ 外置激光】**

## **一、先给结论**

**最值得下注的不是“CPO 一词”，而是三件事：**  
第一，**交换侧光引擎从模块级走向系统级**，它会跟着 102.4T/204.8T 交换机、1.6T/3.2T 端口密度一起放量。第二，**外置激光几乎会成为交换侧 CPO 真正商用的默认方案**，因为热、失效点和可维护性都逼着激光从热封装里移出来。第三，**2026 年最有现实订单弹性的路线其实是 NPO/XPO/LPO \+ 少量 CPO**；到 2027 年，随着 Rubin/Spectrum‑6、Broadcom Davisson、Ciena CPX、更多 ELSFP/ DWDM laser source 进入客户验证和采购，CPO 才会从“样机/验证”进入“收入能看见”的阶段。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai))

近半年最该看的正式场合和材料，按重要性排序是：**GTC 2026、OFC 2026、OCP Global Summit 2025、SC25**。其中 OFC 2026 官方 IEEE panel 已把 **CPO/NPO/xPO 的系统影响、可靠性、可维护性、200G PAM4/PCIe/UCIe、标准/MSA 与供应链多样性**列成核心议题；OCP 2025 已经出现 AI xPU scale-up 光互连和 AI cluster optical interconnect 的正式 session；GTC 2026 则把 NVIDIA 的 Spectrum‑X Ethernet Photonics、STX/CMX、800VDC 和 Rubin 放在一个 AI factory 框架里讲，说明这不是单点器件问题，而是整机房问题。([\*\*\*\*TODO optica \*\*\*\*](https://www.ofcconference.org/))

---

## **A. 2026 年的机遇、挑战、当前在用技术、成熟时间与最可能路径**

### **1）2026 的机遇**

AI 集群的建设强度，已经足以把交换侧光引擎从“提高效率”变成“解决上限”。LightCounting 估算 **AI Ethernet optical transceivers \+ CPO 市场 2025 年约 165 亿美元、2026 年到 260 亿美元**；Dell’Oro 认为 2026 年 AI back-end networking 仍将强增长，**1.6T 交换机开始 volume deployment，CPO 在以太网与 InfiniBand 上出现初始量产爬坡**；Broadcom Q1 FY26 **AI 收入 84 亿美元，同比增长 106%，Q2 AI 半导体收入指引 107 亿美元**，说明交换、定制 ASIC、光互连并不是配角；Anthropic/Google/Broadcom 的多 GW TPU 协议、AMD/Meta 的首个 GW 级 2H26 部署，也把 2027 的算力需求可见度向前锁定了。([LightCounting](https://www.lightcounting.com/newsletter/en/january-2026-optics-for-ai-clusters-366))

对这个赛道最直接的利好是：**交换机带宽代际、前面板密度、机柜热设计、铜互连物理极限**同时逼近。Cisco 已把 **102.4T Silicon One G300 \+ 1.6T optics \+ 100% 液冷系统**推向市场；Broadcom 公开了 **102.4T Davisson CPO switch、400G/lane DSP、3.2T VCSEL-based NPO**；NVIDIA 公开表示 Spectrum‑X Ethernet Photonics 采用**集成硅光 \+ 外置激光阵列**；Arista 则用 **12.8T liquid-cooled XPO** 直接挑战“必须全 CPO 才能提高密度”的叙事。换句话说，**2026 年不是“要不要上光”的问题，而是“上哪种光、上到什么层级、是否还能维护”的问题。**([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx))

### **2）2026 的挑战**

最大挑战不是需求，而是**工程化**。TrendForce 认为 **2026 年 CPO 在 AI 数据中心光模块中的占比仅约 0.5%**，而且首先会出现在 **Rubin 世代的 scale-out 跨机架传输**；同一机构又在 4 月提示 Rubin 受 **HBM4 验证、CX8→CX9 过渡、更高功耗和更先进液冷**影响，Blackwell 在 2026 高端 GPU 出货占比反而会超过 70%。这说明 2026 年行业还在“边验证、边量产、边补 supply chain”。([TrendForce](https://www.trendforce.com/presscenter/news/20260311-12962.html))

具体到交换侧 CPO/NPO+外置激光，至少有七个硬瓶颈：

1. **高功率 CW / DWDM / InP 激光供给与可靠性**；  
2. **光引擎与交换 ASIC 的热耦合**，需要冷板、液冷、激光远置；  
3. **fiber attach / blind-mate / 连接器 / 纤缆管理** 良率与装配节拍；  
4. **package \+ optical engine \+ switch ASIC 的联合测试**，不是单芯片测试；  
5. **102.4T/204.8T 交换 ASIC 与 200G/lane SerDes 节奏**；  
6. **客户认证周期**，尤其是失效率、serviceability、field replacement；  
7. **工程人才**，懂 SerDes、SiPh、封装、热、系统软件的人太少。Coherent 已明确说 InP 需求“前所未有”，其 **6 英寸 InP 线已量产，2026 和 2027 产出继续翻倍**；Furukawa 正在日本和泰国扩 DFB 激光产能；Tower 也在加 SiPh 产能，这本身就是瓶颈的反证。([Coherent Inc](https://www.coherent.com/content/dam/coherent/site/en/documents/investors/investor-presentations/2026/march-17/OFC-2026-Investor%20event-deck-vf.pdf))

### **3）2026 年正在被使用的技术**

**现在真正大规模被使用的，仍然是 800G/1.6T 可插拔、AEC、LPO/线性可插拔。** Cisco 的 102.4T G300 系统和 Broadcom 的 400G/lane DSP 都是围绕 1.6T pluggables 展开的；Arista 的 XPO 本质上是用更大、更高密度、液冷化的 pluggable optics 去抢“全 CPO”之前的工程窗口。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx))

**NPO 是 2026 最现实的增量路线。** Broadcom在 OFC 2026 直接把 **VCSEL-based 3.2T NPO** 定义为“高性能、可靠、成本有效”的 AI 路线；Lightmatter 发布了 **Passage L20**，把 **NPO/OBO** 直接做成统一光引擎；Ciena 的 **Vesta 200 6.4T CPX** 则提供了“可插拔 CPO/近封装光引擎”的折中方案。也就是说，2026 年市场并不是只有“pluggable vs CPO”两极，而是存在 **LPO/XPO → NPO/OBO/CPX → CPO** 的一整条中间带。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai))

**交换侧 CPO \+ 外置激光已经不是 PPT，而是进入 pilot/initial ramp。** NVIDIA 已公开表示 Spectrum‑X Ethernet Photonics 用的是 **integrated silicon photonics \+ external laser arrays**；Marvell 的 CPO switch 参考设计把 **16 个激光模块放到 faceplate**，明确追求 serviceability 和 cooler lasers；Lumentum、OE Solutions、AOI 都在推 **ELSFP/UHP external laser source**；OIF 2025 的 **ELSFP IA** 也已经把“field-replaceable blind-mate external lasers”写成标准化接口。**这说明：只要是交换侧 CPO，外置激光几乎就是 2026–2027 的默认商业形态。**([NVIDIA Developer](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/))

### **4）结合项目内前十大 AI 芯片背景，预测成熟时间与放量时间**

项目内资料给出的结论很清楚：\*\*2026 出货主量仍是 Blackwell/Blackwell Ultra，Rubin 2H26 导入、2027 主线化；AMD MI450 也是 2H26 开始首批 GW 级部署；Google Ironwood 2026-03-31 GA；Trainium/Inferentia、Maia、MTIA、Ascend 都在并行上量。\*\*这意味着 2026 的主流机架仍以“电 scale-up \+ 光 scale-out”为主，真正把光推进到交换芯片封装边缘，是从 Rubin / Spectrum‑6 / Davisson / CPO switch 这一波开始。 ([Google Cloud Documentation](https://docs.cloud.google.com/tpu/docs/release-notes))

**我的判断：**

* **1.6T 可插拔/LPO**：已成熟，2026 全年放量；  
* **VCSEL-based NPO / XPO / OBO**：2026 客户验证+小批导入，2027 明显上量；  
* **交换侧 SiPh CPO \+ ELS**：2026H2 初始量产/试商用，2027 才进入“收入可见”的 ramp；  
* **CPX / pluggable CPO engine**：2026 sample \+ early qualification，2027 小规模商用；  
* **跨多机架 scale-up optical fabric / OCS / xPU 侧更深层 CPO**：2026–2027 仍偏 pilot，2028 更像放量点。Cignal 在 OFC 2026 后的判断也指向 **NVIDIA \+ Lumentum 的 scale-up CPO 在 2028**。 ([TrendForce](https://www.trendforce.com/presscenter/news/20260311-12962.html))

### **5）2026 最可能的技术路径**

**一句话：`102.4T 交换机 + 1.6T 可插拔/LPO 做主量，VCSEL-based NPO/XPO 做高密度短距增强，交换侧 SiPh CPO + 外置激光在顶级集群的 scale-out 先行。`**

这条路最符合 2026 的现实：  
一方面，Cisco/Broadcom/Arista 都在把 **1.6T、液冷、front-panel density** 推向量产；另一方面，TrendForce 明说 **2026 年 CPO 仅约 0.5%**，但 Dell’Oro 又认为 2026 会出现 **CPO 的初始 volume ramp**。这两件事并不矛盾——说明 **2026 的 CPO 是“高端项目放量”，不是“全行业替代”**。而外置激光之所以最可能，是因为它同时满足热、服务、可靠性三件事。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx))

---

## **B. 关键产品拆分，以及 2026–2027 市场规模区间与渗透率路径**

**口径说明：下面是我对“交换侧 CPO/NPO \+ 外置激光”组件/子系统价值池的测算，存在上下游重复，不可横向直接加总；分母统一按“AI 数据中心新增交换/光互连价值池”理解。锚点主要来自：LightCounting 2026 AI optics+CPO 约 260 亿美元、TrendForce 2026 CPO 渗透约 0.5%、Dell’Oro 2026 初始量产爬坡，以及 NVIDIA/Broadcom/Cisco/Arista/Ciena/Lumentum 的产品节奏。**([LightCounting](https://www.lightcounting.com/newsletter/en/january-2026-optics-for-ai-clusters-366))

| 产品类别 | 2026 保守 | 2026 基准 | 2026 乐观 | 2027 保守 | 2027 基准 | 2027 乐观 | 2026→2027 增长判断 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| NPO/XPO 光模块/光引擎 | $4–6 亿 | $7–10 亿 | $11–15 亿 | $10–15 亿 | $18–25 亿 | $28–40 亿 | 高增长，核心受益于 102.4T/204.8T 密度升级 |
| 交换侧 CPO 子系统（含 switch-side optical assembly） | $1.5–2.5 亿 | $3.5–5.5 亿 | $6–9 亿 | $5–8 亿 | $12–18 亿 | $20–30 亿 | 2027 才进入明显放量 |
| 外置激光模块（ELSFP / RLM / DWDM laser source） | $1.2–1.8 亿 | $2–3 亿 | $3.5–5 亿 | $3.5–5.5 亿 | $6.5–9.5 亿 | $11–16 亿 | 增长快于 CPO 本体，因为几乎所有新 CPO 都要先解决激光 |
| CPX / 可插拔式 CPO 光引擎 | $0.5–1 亿 | $1.5–2.5 亿 | $3–4.5 亿 | $2–4 亿 | $5–9 亿 | $10–16 亿 | 是 2026–2027 的“折中路线”期权 |
| 封装/测试/冷板/共设服务 | $2–3 亿 | $3.5–5 亿 | $5–7 亿 | $4.5–7 亿 | $7.5–11 亿 | $11–14 亿 | 供给偏紧、议价偏强 |

**渗透率路径（基准）**：

* NPO/XPO：**2026 约 4%–7% → 2027 约 9%–13%**  
* 交换侧 CPO：**2026 约 0.4%–0.8% → 2027 约 2.5%–4.5%**  
* 外置激光：**在新部署的交换侧 CPO 项目中 attach rate 接近 100%，在整个新增 AI 光互连价值池里 2026 约 1% 左右，2027 提升到 2%–3%**  
* CPX：**2026 小于 1%，2027 约 1%–2%**

---

## **B（技术口径）. 主流技术与快增长新技术的 2026–2027 规模与渗透率**

**这里按技术路线，不按产品。**

| 技术路线 | 2026 状态 | 2026E 市场规模 | 2027E 市场规模 | 2026 渗透率 | 2027 渗透率 | 我的判断 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Retimed 可插拔 800G/1.6T | 主流成熟 | $180–260 亿 | $220–360 亿 | 88%–95% | 72%–85% | 2026 仍是绝对主量 |
| LPO / 线性可插拔 | 快速放量 | $15–30 亿 | $30–60 亿 | 5%–10% | 10%–18% | 是 2026 最现实的过渡技术 |
| VCSEL-based NPO / XPO / OBO | 早期导入 | $3–15 亿 | $10–40 亿 | 1%–6% | 4%–15% | 2027 进入明显上量区 |
| SiPh CPO \+ 外置激光 | 初始量产 | $2–8 亿 | $8–30 亿 | \~0.5%–1.5% | 2%–8% | 2026 先在头部项目吃到订单 |
| OCS / Photonic Fabric / 多机架 scale-up optics | Pilot | $1–4 亿 | $5–18 亿 | \<1% | 1%–6% | 2028 更像大拐点 |

**最快的不是“最大的”，而是“从小基数跃迁最快”的路线：**  
**ELS/CPO、NPO/XPO、OCS** 的 2026→2027 增速，我给 **100%–300%** 区间；  
而 **可插拔/LPO** 虽然增速没那么夸张，但因为基数大，2026–2027 仍是最大的收入池。([LightCounting](https://www.lightcounting.com/newsletter/en/january-2026-optics-for-ai-clusters-366))

---

## **C. 供给侧：产能、瓶颈、成本、毛利**

### **1）产能结构**

* **交换芯片/系统定义**：美国公司主导（NVIDIA、Broadcom、Cisco、Arista、Marvell、Ciena），但核心硅与先进封装高度依赖台湾。([NVIDIA Investor Relations](https://investor.nvidia.com/home/default.aspx))  
* **SiPh / PIC / foundry**：台湾 **TSMC COUPE/CoWoS** 路线最关键；以色列 **Tower** 在 SiPh/heterogeneous laser 上很活跃。([TSMC](https://pr.tsmc.com/english/news/3136))  
* **外置激光 / InP / DFB / CW / DWDM**：美国（Coherent、Lumentum、AAOI）、日本（Furukawa、Sumitomo Electric、Fujikura）、韩国（OE Solutions）、法国/以色列（Scintil/Tower）是主要重镇。([Coherent Inc](https://www.coherent.com/content/dam/coherent/site/en/documents/investors/investor-presentations/2026/march-17/OFC-2026-Investor%20event-deck-vf.pdf))  
* **封装/连接器/热管理/集成**：台湾/中国大陆/东南亚/Japan 供应链密集，Jabil、FIT、Senko、Mikros、ASE 等会持续受益。([Marvell Technology](https://www.marvell.com/blogs/co-packaged-optics-for-next-wave-ai-data-centers.html))

### **2）至少 5 条供给瓶颈**

1. **高功率 CW/DFB/DWDM 激光器**：不是普通模块激光，而是长期高功率、低漂移、可 blind-mate 的 light source。  
2. **SiPh \+ laser 的异质集成与良率**：尤其是 DWDM、微环、耦合与热管理。  
3. **fiber attach / 连接器 / blind-mate / 光纤管理**：102.4T/204.8T 下是系统工程难点。  
4. **封装+热设计**：交换 ASIC、光引擎、冷板、机箱风/液冷必须一起设计。  
5. **系统级测试与 field service**：客户买的是整台 fabric，不是单个器件。  
6. **200G/lane SerDes / 102.4T→204.8T 节奏**：上游交换硅速度决定光引擎放量窗口。  
7. **人才与软件联调**：光、电、热、封装、网络 OS、telemetry 必须一起通。([Marvell Technology](https://www.marvell.com/blogs/co-packaged-optics-for-next-wave-ai-data-centers.html))

### **3）成本与毛利**

**我的 BOM 模型（102.4T 交换侧 CPO+ELS，含 optics 子系统，不含整台机柜总成本）：**

* 光引擎/PIC/driver/TIA/PD：**25%–35%**  
* 外置激光模块/laser array：**15%–25%**  
* fiber attach/连接器/FAU/光纤：**10%–15%**  
* package/substrate/assembly/test：**15%–20%**  
* 冷板/热管理：**10%–15%**  
* 良率损耗/返工/burn-in：**5%–10%**

**若按整台 102.4T 交换系统看**，交换 ASIC \+ board \+ power 大致仍占 **40%–50%**，optics 子系统 **30%–40%**，其余是热、装配和软件。这个赛道毛利不是单靠“器件贵”，而是靠 **良率、可靠性认证、系统级替代成本、以及能否在 102.4T/204.8T 时点拿到 design-in**。  
**最能提毛利的三件事**：

1. 激光共享与外置化，把失效率和维护成本从 package 里挪出来；  
2. 去掉 retimer / pluggable cage，直接减少功耗和部件数；  
3. 绑定头部云厂/交换 ASIC 厂的 next-gen fabric 设计。  
   价格传导通常是 **bandwidth generation 升级 → front-panel density / 铜缆极限触发 → optics 升级为必要项 → 紧缺器件和封装把价格向上游传导**。([NVIDIA Developer](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/))

---

## **D. 竞争格局、壁垒、价值捕获**

### **1）市场结构（我的估算）**

* **交换侧 CPO/NPO 系统层**：CR3 大概率 **75%–85%**，基本围绕 **NVIDIA / Broadcom / Cisco（加 Arista 作为 XPO 路线）**。  
* **外置激光/InP 层**：CR3 约 **55%–70%**，核心看 **Coherent / Lumentum / 日本大厂（Furukawa、Sumitomo、Fujikura）**。  
* **光引擎 / CPO-NPO 平台层**：CR5 约 **60%–75%**，但仍在快速洗牌，**Marvell、Ciena/Nubis、Lightmatter、Ayar、Coherent、POET、Scintil** 都有机会。

### **2）壁垒清单，以及“为什么能定价”**

**技术壁垒**：  
不是做出一个 PIC 就够，而是要把 **SerDes、PIC、laser、package、冷板、network OS、telemetry** 一起跑通，所以能做系统共设计的人天然稀缺。

**规模壁垒**：  
2026–2027 先吃到量的公司，能更快把良率、失效率、热设计和 field data 做成壁垒，后进者要重新踩坑。

**渠道/客户锁定**：  
CPO/NPO 不是买一个器件，而是进 hyperscaler 的 rack 与 fabric。进一次 design-in，通常绑定至少一代交换 ASIC 和一轮机房资本开支。

**认证与标准壁垒**：  
ELSFP、blind-mate、MSA、Reliability、serviceability 都要过。OFC 2026 官方 panel 已经把这些列成核心讨论项。

**切换成本**：  
客户切换时不是换一个模块，而是重新验证 **交换芯片、光引擎、激光源、热、线缆、运维流程**，所以一旦通过认证就有定价权。([\*\*\*\*TODO optica \*\*\*\*](https://www.ofcconference.org/program/special-events/the-network-and-system-implications/))

### **3）哪一层最可能长期高 ROIC / 高毛利**

**我最看好两层：**

1. **交换 ASIC \+ 系统定义者**：NVIDIA、Broadcom、Cisco/Arista 这类公司可以把 optics 变成 attach revenue，而不是被动采购项；  
2. **高功率外置激光 \+ InP / PIC 关键器件**：只要 CPO 要求更高带宽密度、更低功耗和更好可维护性，laser / PIC 会从“部件”变成“瓶颈”。

**相对没那么看好的层**是纯组装型模块厂，除非它同时掌握 **光引擎、热管理、连接器或系统验证**。长期 ROIC 不会均匀分布，最有价值的是**控制标准和控制系统边界的人**。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-announces-tomahawkr-6-davisson-industrys-first-1024))

---

## **E. 2026 最可能发生的 3 个拐点**

**拐点 1：102.4T / 1.6T 量产，把“铜还能撑多久”从技术讨论变成采购问题。**  
Cisco、Broadcom、Arista 都把答案推到了 2026 年。交换侧光学不再是锦上添花，而是前面板密度和能耗的硬解。([Cisco Investor Relations](https://investor.cisco.com/news/news-details/2026/Cisco-Announces-New-Silicon-One-G300-Advanced-Systems-and-Optics-to-Power-and-Scale-AI-Data-Centers-for-the-Agentic-Era/default.aspx))

**拐点 2：外置激光从“CPO 的辅助件”变成“CPO 能否商用的前提件”。**  
OIF 的 ELSFP、Lumentum 的 16-channel DWDM ELSFP、OE Solutions 23dBm、AOI 25dBm、Marvell 的 faceplate laser，都说明产业共识已形成：**要商用，先把激光拿出来。**([OIForum](https://www.oiforum.com/wp-content/uploads/OIF-ELSFP-02.0.pdf))

**拐点 3：2026 是 design-in 年，2027 才是收入 ramp 年。**  
TrendForce 给出 2026 CPO 仅 \~0.5%，Dell’Oro 说 2026 初始量产爬坡，Cignal 则把更深层的 scale-up CPO 指到 2028。我的理解是：**2026 是“客户开始下正式验证预算”，2027 才是“财务报表里看到更明显的新增收入”。**([TrendForce](https://www.trendforce.com/presscenter/news/20260311-12962.html))

---

## **F. 头部公司地图：谁在做、是否上市、哪里上市、能否在美股买到**

### **1）交换芯片 / CPO-NPO 系统层**

**NVIDIA（NASDAQ: NVDA，能直接在美股买）**、**Broadcom（NASDAQ: AVGO，能直接买）**、**Cisco（NASDAQ: CSCO，能直接买）**、**Arista（NYSE: ANET，能直接买）**、**Marvell（NASDAQ: MRVL，能直接买）**、**Ciena（NYSE: CIEN，能直接买）**。这一层是系统定义权最强的一层。([NVIDIA Investor Relations](https://investor.nvidia.com/home/default.aspx))

### **2）光引擎 / CPO-NPO 平台层**

**Ciena/Nubis（CIEN，美股可买）**、**Marvell/Celestial AI（MRVL，美股可买）**、**Coherent（NYSE: COHR，美股可买）**、**POET Technologies（NASDAQ: POET，美股可买）**、**Tower Semiconductor（NASDAQ/TASE: TSEM，美股可买）**、**Lightmatter（未见公开上市代码，仍处融资/私有阶段）**、**Ayar Labs（Series E，未见公开上市代码）**、**Ranovus（官网未见公开上市代码）**、**Scintil Photonics（Series B，未见公开上市代码）**。([Ciena Corporation](https://investor.ciena.com/news-releases/news-release-details/ciena-unveils-industrys-highest-density-lowest-power-pluggable/))

### **3）外置激光 / InP / ELSFP / DWDM laser source 层**

**Lumentum（NASDAQ: LITE，美股可买）**、**Coherent（NYSE: COHR，美股可买）**、**Applied Optoelectronics / AAOI（NASDAQ: AAOI，美股可买）**、**Tower \+ Scintil（TSEM \+ private，美股可买的是 Tower）**、**Furukawa Electric（东证 5801，非美股主板）**、**Sumitomo Electric（东京 5802，非美股主板）**、**Fujikura（东证 5803，非美股主板）**、**FIT Hon Teng（HKEX: 06088，非美股主板）**、**OE Solutions（KOSDAQ: 138080，非美股主板）**。这层里，**能在美股直接买的主要是 LITE / COHR / AAOI / TSEM**；日本、韩国、香港名字通常需要对应海外市场权限。([Lumentum Investor Relations](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-to-Join-the-SP-500-Index/default.aspx))

### **4）Foundry / 封装 / 连接器 / 热管理 / 集成**

**TSMC（NYSE: TSM ADR，美股可买）**、**ASE（NYSE: ASX，美股可买）**、**Jabil（NYSE: JBL，美股可买）**、**Amphenol（NYSE: APH，美股可买）**、**Senko/SENKO Advanced Components（官网未见公开美股代码）**、**Mikros Technologies（Jabil 子公司）**。如果你看的是“谁给这个赛道卡脖子”，这一层的重要性会越来越高。([TSMC](https://investor.tsmc.com/english/dividends/2q25))

---

## **最后给投资结论**

**我对这个赛道在 2026–2027 的结论是偏强乐观。**  
不是因为我觉得 CPO 会立刻无脑爆发，而是因为：  
**AI 集群建设已经把交换侧互连推到了“功耗、密度、可维护性”的硬约束；而 NPO/XPO/LPO/CPO+ELS 恰好是解决这组硬约束的产品集合。** 2026 年最容易兑现的是 **NPO/XPO/LPO、外置激光、SiPh/封装/冷板验证订单**；2027 年更容易兑现的是 **交换侧 CPO 子系统收入**。如果只选一句话：**2026 投“先导入、先验证、先 attach”的环节；2027 才开始收“真正放量”的钱。** ([TrendForce](https://www.trendforce.com/presscenter/news/20260311-12962.html))

如果你愿意，我下一步可以把这份报告再压缩成一版**投资备忘录格式**，直接给出“最值得跟踪的 15 家公司 \+ 关键观察指标 \+ 触发条件”。

