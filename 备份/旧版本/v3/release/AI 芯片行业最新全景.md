我先给结论：到 **2026 年 4 月**，真正决定 AI 芯片行业节奏的，已经不是“单一 GPU 型号”，而是三条并行主线：  
**NVIDIA 从 Blackwell/Blackwell Ultra 过渡到 Rubin；云厂商自研 ASIC（Google TPU、AWS Trainium、Microsoft Maia、Meta MTIA）快速上量；中国侧由 Huawei Ascend 910C/950 带动替代链。** 过去一个月里，Google TPU7x Ironwood 在 **2026-03-31** GA，Meta 在 **2026-04-02** 再次确认 MTIA 300→500 路线，NVIDIA 在 **2026-03-30** 公布 800VDC AI factory 配电，**2026-04-06** 又出现 Broadcom/Google/Anthropic 的新长期供给消息，这些都把 2027 的重心推向“更多自研 ASIC \+ HBM4 \+ 先进封装 \+ 液冷 \+ 更高电压直流配电”。 ([Google Cloud Documentation](https://docs.cloud.google.com/tpu/docs/release-notes))

下面我聚焦的是 **数据中心 / 云 / 主权 AI 训练与推理加速器**。手机、PC、车载、边缘 NPU 不逐一展开，否则范围会失控。

---

## **1）2026–2027 AI 加速器全景：谁在做、做到哪一阶段了**

状态口径：  
**大规模量产** \= 已 GA / 正式出货且有公开规模部署；  
**规模导入** \= 已发布并开始部署，但还未完全铺开；  
**试产/送样** \= 小批或客户样品；  
**实验/内部验证** \= 内部测试；  
**设计** \= 路线图阶段。

| 公司 / 家族 | 2026-04 状态 | 2027 前后后续 | 公开关键信息 | 依据 |
| ----- | ----- | ----- | ----- | ----- |
| **NVIDIA Blackwell 家族（B200 / GB200 / HGX B200）** | **大规模量产** | 2026 仍是主力之一，被 Blackwell Ultra / Rubin 逐步接棒 | Blackwell 公开为 **TSMC 4NP、2080 亿晶体管、双 reticle die、10TB/s die-to-die**。 | 官方。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives-to-power-a-new-era-of-computing?utm_source=chatgpt.com)) |
| **NVIDIA Blackwell Ultra（B300 / GB300 / GB300 NVL72）** | **大规模量产 / 快速爬坡** | 2026 主力大系统 | **GB300 NVL72** 为 72 GPU \+ 36 Grace CPU，官方称 **fully liquid-cooled**；Blackwell Ultra 每 GPU 公布 **288GB HBM3e**。 | 官方。([NVIDIA](https://www.nvidia.com/en-us/data-center/gb300-nvl72/?utm_source=chatgpt.com)) |
| **NVIDIA Rubin / Vera Rubin / Rubin Ultra** | **Rubin 已宣布 full production，2H26 导入** | 2027 主线；Rubin Ultra 往更大规模机架推进 | Rubin 官方称 **HBM4、NVLink 6、七颗新芯片 full production**；DGX SuperPOD with Vera Rubin / Rubin NVL8 计划 **2026 下半年**。Rubin Ultra NVL576 已公开采用 **direct optical connections**。 | 官方。([NVIDIA](https://www.nvidia.com/en-us/data-center/technologies/rubin/)) |
| **AMD Instinct MI350（MI350X / MI355X）** | **大规模量产** | 2026 与 MI450 并行 | 官方公布 **TSMC 3nm/6nm、1850 亿晶体管、288GB HBM3E、8TB/s、256MB LLC、1400W**。 | 官方。([AMD](https://www.amd.com/en/products/accelerators/instinct/mi350/mi355x.html)) |
| **AMD Instinct MI430X / MI440X** | **小规模量产 / 规模导入** | 面向主权 AI / HPC 的并行分支 | MI430X 公布 **432GB HBM4、19.6TB/s**；MI440X 在 2026 年初继续推进，面向 sovereign AI / HPC。 | 官方。([AMD](https://www.amd.com/en/blogs/2025/amd-instinct-mi430x-powering-the-next-wave-of-ai.html)) |
| **AMD Instinct MI450 / MI455X \+ Helios** | **2026H2 爬坡** | 2027 放量 | AMD/OCI 公布 MI450 系列每 GPU **最高 432GB HBM4、约 20TB/s**；Helios 72 GPU 机架 **Q3 2026** 可用；AMD 与 OpenAI / Meta 的 **1GW 首批部署**都指向 **2H26**。 | 官方。([AMD](https://www.amd.com/en/blogs/2025/amd-helios-ai-rack-built-on-metas-2025-ocp-design.html)) |
| **AMD MI500** | **设计 / 路线图** | 2027 | AMD 已预告 **2nm \+ HBM4E** 的 MI500 系列。 | 官方。([AMD](https://www.amd.com/en/newsroom/press-releases/2026-1-5-amd-and-its-partners-share-their-vision-for-ai-ev.html)) |
| **Google TPU Trillium（v6e）** | **GA / 大规模部署** | 与 Ironwood 并行 | Google 公布 Trillium 每芯片 **32GB HBM、1638GiB/s HBM 带宽、800GB/s ICI**；Jupiter fabric 可到 **100,000 chips**。 | 官方。([Google Cloud Documentation](https://docs.cloud.google.com/tpu/docs/v6e)) |
| **Google TPU Ironwood（TPU7x）** | **GA（2026-03-31）** | 2026–2027 快速上量 | Google Cloud 公开 TPU7x / Ironwood **192GB HBM、约 7.37TB/s、1200GB/s ICI、最多 9216 芯片 Pod、双 chiplet**。 | 官方。([Google Cloud Documentation](https://docs.cloud.google.com/tpu/docs/tpu7x)) |
| **AWS Trainium2** | **GA / 大规模量产** | 与 Trainium3 并行 | Trn2 UltraServer 为 **64 Trainium2**；单芯片公开 **96GB HBM、2.9TB/s、1TB/s NeuronLink**。 | 官方。([Amazon Web Services, Inc.](https://aws.amazon.com/ec2/instance-types/trn2/)) |
| **AWS Trainium3** | **GA / 快速爬坡** | 2027 继续放量 | AWS 公布单芯片 **144GB HBM3e、4.9TB/s、2.52 PFLOPS FP8**；Trn3 UltraServers 2025 末已正式推出。 | 官方。([Amazon Web Services, Inc.](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-ec2-trn3-ultraservers/)) |
| **AWS Inferentia2** | **大规模量产** | 下一代未公开 | 官方公开单芯片 **32GB HBM**，Inference 为主。 | 官方。([Amazon Web Services, Inc.](https://aws.amazon.com/ai/machine-learning/inferentia/)) |
| **Microsoft Maia 200** | **规模导入 / 量产部署** | 后续 Maia 未公开 | 官方公布 **TSMC 3nm、216GB HBM3e、7TB/s、272MB on-chip SRAM、750W、2.8TB/s scale-up、闭环液冷**。 | 官方。([The Official Microsoft Blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)) |
| **Meta MTIA 300 → 500** | **MTIA 300 已量产；400/450/500 设计/导入** | 2027 前继续出 4 个世代 | Meta 官方称：**两年内开发/部署 4 代**，整体已部署 **hundreds of thousands of MTIA chips**；MTIA 300 已用于排序/推荐训练，400/450/500 面向更广泛工作负载和 GenAI inference。 | 官方。([About Facebook](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)) |
| **Intel Gaudi 3 / Crescent Island / Jaguar Shores** | **Gaudi 3 量产；Crescent 送样；Jaguar 设计** | 2027 取决于路线是否稳定 | Gaudi 3 已量产；Intel 公布 **Crescent Island** 为 future inference GPU。关于 Falcon Shores 转内部测试、Jaguar Shores 延续，主要来自二手报道，需保留不确定性。 | 官方 \+ 二手。([Newsroom](https://newsroom.intel.com/client-computing/computex-intel-unveils-new-gpus-ai-workstations)) |
| **OpenAI custom accelerator（与 Broadcom）** | **设计 / 试产** | 2027 更可能进入放量窗口 | OpenAI 与 Broadcom 官方宣布 **10GW custom accelerators，时间窗 2H26–2029**；首颗芯片更具体时间点主要来自二手报道。 | 官方 \+ 二手。([OpenAI](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)) |
| **Huawei Ascend 910C / 950PR / 950DT / 960** | **910C 量产；950PR 2026 ramp；950DT Q4’26；960 Q4’27** | 2027 中国主线之一 | 华为官方 Atlas 950 SuperPoD 为 **64 NPU/柜，最多 8192 NPU，全光互联**；950/960 时间窗有官方与路透两条线。910C 的大规模出货最早由路透报道。 | 官方 \+ 路透。([huawei](https://www.huawei.com/en/news/2026/3/mwc-superpod-ai)) |
| **Baidu Kunlunxin（P800 / M100 / M300）** | **P800 在用；M100 2026；M300 2027** | 2027 继续追赶 | Kunlun 路线主要由路透披露：P800 已用于超节点，M100 面向 2026，M300 面向 2027。 | 二手。([Reuters](https://www.reuters.com/world/china/baidus-kunlunxin-valued-close-3-billion-eyes-hong-kong-ipo-sources-say-2025-12-05/)) |
| **Alibaba T-Head proprietary GPU** | **官方称已 scaled production** | 后续公开细节很少 | 阿里云官方博客已明确：T-Head 的自研 GPU 已进入 **scaled production**，支持 **training / fine-tuning / inference**。公开命名和规格仍少。 | 官方。([Alibaba Cloud](https://www.alibabacloud.com/blog/602958)) |
| **Cambricon Siyuan 370 / MLU370** | **已上市/量产** | 后续公开路线图较少 | 寒武纪公开仍以 **MLU370 / Siyuan 370** 为主，采用 chiplet 路线。 | 官方。([Cambricon](https://www.cambricon.com/)) |
| **Cerebras WSE-3 / CS-3** | **已部署** | 下一代未公开 | WSE-3 仍是标志性大晶圆芯片；AWS 已宣布在数据中心部署 Cerebras CS-3。 | 官方。([Cerebras](https://www.cerebras.ai/chip)) |
| **SambaNova SN50** | **2026H2 shipping** | 面向 agentic inference | 官方称 SN50 为 **agentic inference** 设计，计划 **2026 下半年出货**。 | 官方。([SambaNova](https://sambanova.ai/blog/introducing-the-sn50-rdu-purpose-built-for-agentic-inference)) |
| **Tenstorrent Blackhole / next Samsung chiplet** | **Blackhole 已销售；下一代设计中** | 2027 看 Samsung chiplet | Blackhole 已上架，公开规格含 **120 Tensix cores、180MB SRAM、最多 32GB GDDR6**；下一代 chiplet 与 Samsung Foundry 合作。 | 官方。([Tenstorrent](https://tenstorrent.com/)) |
| **Groq 3 LPX / LP30** | **2026 导入** | 更偏超低时延 inference | NVIDIA 官方技术文中给出 Groq 3 LPX：**256 chips、128GB SRAM、40PB/s SRAM bandwidth**。 | 官方。([NVIDIA Developer](https://developer.nvidia.com/blog/inside-nvidia-groq-3-lpx-the-low-latency-inference-accelerator-for-the-nvidia-vera-rubin-platform/?utm_source=chatgpt.com)) |

两点要单独说明。第一，**Broadcom、Marvell 更像“定制 XPU 的平台与设计/封装/互联供应商”而不是单一公开型号所有者**，但它们在 2026–2027 的重要性非常高：Broadcom 已宣布 **首个 2nm custom compute SoC shipping**，3.5D XDSiP 平台进入生产；Marvell 则公开了 **custom HBM、CPO、2nm custom SRAM、先进封装**平台。 ([Broadcom Inc.](https://investors.broadcom.com/node/63946/pdf))

第二，**很多“下一代”并没有完全公开命名与规格**。像 Google 后继 TPU、AWS 下一代 Inferentia/Trainium、下一代 Maia、部分中国厂商新芯片，公开信息都还不完整；下面我会把未公开部分尽量补足，但会明确标注“推测 / 未检验”。

---

## **2）我对 2026 / 2027 AI 加速器“产能释放量（美元口径）”的估计**

口径说明：这里的“产能释放量”是 **当年可交付、可装入服务器/机架并形成可部署算力的 AI 加速器硅价值**。  
自研芯片（Google TPU、Trainium、Maia、MTIA 等）按 **内部转移价等价值**估算；**不**把服务器机箱、交换机、楼宇、电力土建和供应商收入重复加总。

| 家族 | 2026E 产能释放（$B） | 2027E 产能释放（$B） | 置信度 | 我为什么这样估 |
| ----- | ----- | ----- | ----- | ----- |
| **NVIDIA Blackwell \+ Blackwell Ultra** | **90–135** | **45–85** | 中 | 2026 仍是行业主力，GB300/GB200 都在上量；但 2027 会被 Rubin 部分替代。核心上限受 HBM 与封装约束。([NVIDIA](https://www.nvidia.com/en-us/data-center/gb300-nvl72/?utm_source=chatgpt.com)) |
| **NVIDIA Rubin / Vera Rubin** | **5–15** | **40–80** | 低-中 | 2026 更像导入年，官方已称 full production，2H26 交付；2027 才进入大规模贡献窗口。Rubin 还叠加 HBM4 供应爬坡。([NVIDIA](https://www.nvidia.com/en-us/data-center/technologies/rubin/)) |
| **AMD MI350** | **4–10** | **2–6** | 中 | MI350 已量产，但 2027 会被 MI450/455X 逐步替代。([AMD](https://www.amd.com/en/products/accelerators/instinct/mi350/mi355x.html)) |
| **AMD MI450 / MI455X** | **4–12** | **18–40** | 低-中 | 2H26 才是首批 1GW 级部署开始，2027 才更像放量年；OpenAI、Meta、OCI 都是关键验证。([AMD](https://www.amd.com/en/newsroom/press-releases/2026-2-24-amd-and-meta-announce-expanded-strategic-partnersh.html)) |
| **Google TPU（Trillium \+ Ironwood）** | **15–30** | **25–55** | 低-中 | Google 自用口径最难估，但 Trillium 已是 100K-chip 级 fabric，Ironwood 已 GA，且 Broadcom/Google/Anthropic 长单提高 2027 上沿。([Google Cloud](https://cloud.google.com/blog/products/compute/trillium-tpu-is-ga)) |
| **AWS Trainium / Inferentia** | **10–20** | **18–40** | 低-中 | Trainium2/3 与 Inferentia2 都在正式供给期，Trainium3 单芯片规格显著拉高价值密度。([Amazon Web Services, Inc.](https://aws.amazon.com/ec2/instance-types/trn2/)) |
| **Microsoft Maia** | **2–6** | **6–15** | 低 | Maia 200 刚进入部署期，规格高，但公开部署范围仍少于 Google/AWS/NVIDIA。([The Official Microsoft Blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)) |
| **Meta MTIA** | **2–6** | **5–15** | 低 | 官方已说整体部署到“hundreds of thousands of MTIA chips”，但代际与单片价值不透明。([About Facebook](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)) |
| **Huawei Ascend（910C / 950）** | **8–18** | **15–35** | 低-中 | 中国需求强，950 PR/DT 进入 2026，且有官方 8192-NPU SuperPoD 路线；但供应链与价格体系透明度低。路透甚至给出 2026 年约 75 万片计划的说法。 |
| **Baidu / Alibaba / Cambricon 等中国其他 AI 芯片** | **2–8** | **6–18** | 低 | 三家都有推进，但公开规格/价格/交付节奏都更不透明。([Reuters](https://www.reuters.com/world/china/baidus-kunlunxin-valued-close-3-billion-eyes-hong-kong-ipo-sources-say-2025-12-05/)) |
| **OpenAI custom accelerator** | **0–2** | **5–15** | 低 | 2026 更像试产 / 小批，2027 才有可能实质放量。([OpenAI](https://openai.com/index/openai-and-broadcom-announce-strategic-collaboration/)) |
| **Intel \+ Cerebras \+ Groq \+ SambaNova \+ Tenstorrent 等其他** | **2–6** | **4–12** | 低 | 技术亮点多，但总量大概率仍小于前述几大阵营。([Intel](https://www.intel.com/content/www/us/en/products/details/processors/ai-accelerators/gaudi.html)) |
| **行业合计** | **160–260** | **240–380** | 低-中 | 由超大买家 CapEx、HBM TAM、TSMC 封装瓶颈、具体 GW 级采购承诺共同约束。([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx)) |

### **这组数字为什么大致站得住**

**第一重验证：需求侧预算。**  
Alphabet 给出 **2026 CapEx $175B–$185B**，Amazon 预计 **$200B**，Meta 预计 **$115B–$135B**，Oracle 预计 **$45B–$50B**；Microsoft 单季 CapEx 已到 **$37.5B**，并明确其中约 **2/3 是短寿命资产，主要是 GPU 和 CPU**。按中点再把 Microsoft 以当前 run-rate 粗略年化，五家合计已经到 **约 $705B** 的级别。即使只有 25%–35% 最终沉淀到 AI 加速器相关硅价值，也能支撑我给出的行业总区间。 ([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

**第二重验证：HBM 倒推。**  
Micron 已表示 **2026 全年 HBM 的价格和数量协议已经签完**，并给出 HBM TAM 从 **2025 年约 $35B 到 2028 年约 $100B** 的路径；Samsung 与 Micron 都已在 2026 年启动 **HBM4** 量产/出货，且都直接点名面向 Rubin。若把 2026–2027 的 HBM 市场粗看成 **$55B–$70B** 量级、HBM 占高端 AI 加速器 BOM 的 **约 25%**，倒推的 AI 加速器硅价值大约是 **$220B–$280B**，与我给的行业总区间基本一致。 ([Micron Technology](https://investors.micron.com/static-files/088991c5-a249-4f66-a0a6-258d9b66f3f9))

**第三重验证：供给侧天花板。**  
TSMC 2026 资本开支为 **$52B–$56B**，而 Broadcom 在 2026 年又明确提示了 **TSMC 产能瓶颈**，且该约束会延伸到 2027；与此同时，HBM4 仍是刚进入量产阶段。这意味着 2026–2027 的上沿不能无限抬，最终还是会被 **HBM、先进封装、液冷、机架供电**共同卡住。 ([TSMC](https://investor.tsmc.com/chinese/encrypt/files/encrypt_file/reports/2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf))

---

## **3）我挑出的 2026–2027 初“综合出货/装机规模最大”的 12 个芯片家族**

这里不是按“裸片片数”死排名，而是按 **综合装机规模 \+ 交付价值 \+ 公开部署迹象** 选 12 个家族。  
边界上非常接近、但我没放进这 12 个的有：**Intel Gaudi 3、OpenAI custom、Baidu P800/M100、Alibaba 自研 GPU**。

| 家族 | 规模判断 | 掩膜 / 工艺 | 外部存储 | 内部存储 | 互联 / 光学 | 供电 / 散热 | 封装 / 基板 / CPO | 公开度与补充 | 依据 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **NVIDIA Blackwell / Blackwell Ultra** | **极高** | **TSMC 4NP**；双 reticle die；具体掩膜层数未公开 | **HBM3E**；Ultra 公布 **288GB/GPU** | 片上 cache/SRAM 细节未完整公开 | **NVLink** 电互联为主；公开资料里未见 package-level CPO | GB300 NVL72 **全液冷**；NVIDIA 正推 **800VDC** AI factory 架构 | CoWoS 类先进封装 \+ 大型 interposer / 基板（具体 S/L/R 未公开，**推测**） | 2026 主力；CPO 还不是 Blackwell 主体卖点 | ([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-blackwell-platform-arrives-to-power-a-new-era-of-computing?utm_source=chatgpt.com)) |
| **NVIDIA Rubin / Vera Rubin** | **高** | 节点未公开；已 official **full production** | **HBM4**；系统级官方给出 NVL72 **最高 20.7TB HBM4** | 片上存储细节未完整公开 | **NVLink 6**；Rubin Ultra 已公开 **direct optical connections** | 继续沿液冷 \+ 更高压直流机房配电 | CoWoS 类路线几乎确定，但具体封装形态未公开（**推测**） | 2026 是导入年，2027 才是主放量窗口 | ([NVIDIA](https://www.nvidia.com/en-us/data-center/technologies/rubin/)) |
| **AMD MI350** | **高** | **TSMC 3nm/6nm** | **288GB HBM3E，8TB/s** | **256MB LLC** | 公开重点仍是电互联 / 节点互联，未见 package-level 光学 | **1400W**；支持风冷与直液冷 | 先进 chiplet/封装路线明确，但细节未完全公开 | 2026 AMD 主量产训练芯片 | ([AMD](https://www.amd.com/en/products/accelerators/instinct/mi350/mi355x.html)) |
| **AMD MI450 / MI455X** | **中高** | 节点未公开 | **432GB HBM4，约 19.6–20TB/s** | 片上存储细节未公开 | **UALoE \+ Ethernet**；公开未见 package-level CPO | Helios 为 **72 GPU 液冷机架** | AMD 明确提到 **3.5D packaging、12x HBM4 stacks** | 2027 比 2026 更重要 | ([AMD](https://www.amd.com/en/blogs/2025/amd-helios-ai-rack-built-on-metas-2025-ocp-design.html)) |
| **Google TPU Trillium（v6e）** | **高** | 工艺节点未公开 | **32GB HBM/chip，1638GiB/s** | 片上 SRAM 细节未公开 | **800GB/s ICI，2D torus**；公开未见 CPO | Google TPU Pods 已长期液冷；Google 公开 **±400VDC / 1MW racks** | 封装细节未公开；Google/Broadcom 协作广为流传，但官方不细说 | 内部转移价最难估，但部署规模极大 | ([Google Cloud Documentation](https://docs.cloud.google.com/tpu/docs/v6e)) |
| **Google TPU Ironwood（TPU7x）** | **高** | 工艺节点未公开 | **192GB HBM/chip，约 7.37TB/s** | 双 chiplet 架构已公开；更细片上缓存未公开 | **1200GB/s ICI，最多 9216 芯片 Pod** | Google 同样以 **液冷 \+ ±400VDC** 路线推进 | 双 chiplet \+ HBM；具体封装未公开 | 2026-03-31 GA，是最近一个月最重要的新点之一 | ([Google Cloud Documentation](https://docs.cloud.google.com/tpu/docs/tpu7x)) |
| **AWS Trainium2** | **高** | 工艺节点未公开 | **96GB HBM，2.9TB/s** | 片上存储细节未公开 | **1TB/s NeuronLink，2D torus** | 机架级供电/散热公开少于 Google/NVIDIA | 封装细节未公开 | AWS 训练主力之一 | ([Amazon Web Services, Inc.](https://aws.amazon.com/blogs/aws/amazon-ec2-trn2-instances-and-trn2-ultraservers-for-aiml-training-and-inference-is-now-available/)) |
| **AWS Trainium3** | **中高** | 工艺节点未公开 | **144GB HBM3e，4.9TB/s** | 片上存储细节未公开 | UltraServer 路线继续加强 scale-up | AWS 公开强调 **tokens/MW** 提升 | 封装细节未公开 | 价值密度明显高于 Trn2 | ([Amazon Web Services, Inc.](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-ec2-trn3-ultraservers/)) |
| **AWS Inferentia2** | **中高** | 工艺节点未公开 | **32GB HBM/chip** | 片上存储细节未公开 | 以 inference 实例形态出现，互联细节公开少 | 散热/供电细节公开不多 | 封装细节未公开 | 绝对片数可能不低，但单片价值低于训练芯片 | ([Amazon Web Services, Inc.](https://aws.amazon.com/ai/machine-learning/inferentia/)) |
| **Microsoft Maia 200** | **中高** | **TSMC 3nm** | **216GB HBM3e，7TB/s** | **272MB on-chip SRAM** | **2.8TB/s bidirectional scale-up**；Cluster 到 **6144 accelerators** | **750W**；**closed-loop liquid cooling** | HBM 大封装路线明确，具体封装名未公开 | 公开规格相当完整 | ([The Official Microsoft Blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)) |
| **Meta MTIA 300 / 400 / 450 / 500** | **高** | 工艺/掩膜基本未公开 | 官方未公开具体 HBM/外存规格 | 官方只说 memory bandwidth / numeric types 持续增强 | 基于 OCP 标准，互联细节仍 sparse | MTIA 400 引入液冷主要来自路透，**未完全证实** | Broadcom+TSMC 合作也主要来自路透，**未完全证实** | 这是“信息最不透明但部署量很大”的一条线 | ([About Facebook](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)) |
| **Huawei Ascend 910C / 950** | **高** | 工艺/掩膜未公开 | 高带宽内存大概率存在，但具体容量公开不全；部分高端 HBM 说法来自路透，**未检验** | 片上存储未公开 | **Atlas 950 SuperPoD 全光互联**，官方给出 **16PB/s** | 电源/散热公开少；大系统层面很可能重液冷（**推测**） | 先进封装是必然，但细节未公开 | 中国替代链主心骨，透明度低于美系 | ([huawei](https://www.huawei.com/en/news/2026/3/mwc-superpod-ai)) |

---

## **4）把你关心的技术环节单独拉平：掩膜、光互联、供电、HBM、检测、制造设备、散热、CPO、储能**

这一张不是按芯片分，而是按 **前 12 家族共同依赖的技术环节** 分。这样更适合回答你列出的那些“横向技术问题”。

| 环节 | 2026–2027 主流技术 / 趋势 | 典型公司 / 设备 | 对前 12 家族的影响 | 依据 |
| ----- | ----- | ----- | ----- | ----- |
| **光刻掩膜** | 主流仍是 **EUV \+ computational lithography**；**2nm / 高 NA EUV**开始进入 HVM；但**每颗 AI 芯片的准确 mask count 没有厂商公开** | ASML、TSMC mask ecosystem、Hoya EUV mask blanks | Blackwell/MI350/Maia 200 已在 4NP/3nm；Rubin、Broadcom 2nm custom、AMD MI500 更受 2nm / high-NA 影响 | ([ASML](https://www.asml.com/products/euv-lithography-systems)) |
| **AI 芯片级供电** | 两条线并行：**芯片侧**更重 backside power / 更短 PDN / on-package regulator；**机架侧**转向 **±400VDC / 800VDC** | Applied（backside power）、Marvell（PIVR / on-package regulator 概念）、Google、NVIDIA、OCP | 芯片级供电本身不是单一器件，而是“die → package → board → rack”一整条链；2026 的真实拐点其实在机架高压直流 | ([Applied Materials](https://ir.appliedmaterials.com/static-files/50913916-d1d0-4eff-bb18-67c4886343d0)) |
| **AI 芯片外部存储** | **HBM3E → HBM4 → HBM4E** 是主线；2026 开始从 HBM3E 大规模切向 HBM4 | Samsung、Micron、SK hynix | Blackwell/MI350 以 HBM3E 为主；Rubin、MI450/455X、未来 MI500 转向 HBM4/HBM4E；HBM 是 2026–2027 最大共同瓶颈之一 | ([Samsung Global Newsroom](https://news.samsung.com/global/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing)) |
| **AI 芯片内部存储** | 片上 **SRAM / L2 / scratchpad / custom SRAM** 重要性继续上升；推理芯片尤其强调片上 SRAM | Microsoft Maia 200、Groq、Marvell custom SRAM | Maia 200 已公开 **272MB SRAM**；Groq LPX 机架级总 **128GB SRAM**；Marvell 已公开 **2nm custom SRAM** 平台 | ([The Official Microsoft Blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)) |
| **AI 芯片制造设备** | AI 逻辑与先进封装的关键设备继续集中在 **ASML EUV、Applied、Lam、TEL、Besi** | ASML、Applied Materials、Lam、TEL、Besi | 对 3nm/4NP/2nm 逻辑、HBM TSV、hybrid bonding、CoWoS / 3.5D 都是刚需 | ([Applied Materials](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-next-gen-chipmaking-products/)) |
| **AI 芯片检测** | 重点从单纯 wafer test 延伸到 **先进封装 / interposer / substrate / 3D IC defect** | KLA、Advantest、Teradyne | 多 die \+ HBM \+ 大基板时代，检测已不是“后道补丁”，而是良率核心 | ([KLA](https://www.kla.com/products/packaging-manufacturing/wafer-inspection-and-metrology-for-advanced-packaging)) |
| **AI 芯片内部存储检测（HBM / KGD / stack test）** | HBM4 转换使 **Known Good Die、stack-level test、memory tester** 更关键 | Advantest、Teradyne | Advantest 明说 HBM4 带动 memory tester 需求；Teradyne 直接推出 **Magnum 7H** 面向 HBM | ([株式会社アドバンテスト](https://www.advantest.com/document/en/investors/ir-library/result/E_BIZ_250729_QA.pdf)) |
| **AI 芯片内部存储制造设备** | HBM 关键仍是 **TSV etch、铜沉积、die stack、hybrid bonding** | Lam、Applied、TEL、Besi | 几乎所有高端训练芯片都受这条链影响；HBM 供给弹性决定 2026–2027 上限 | ([Lam Research Newsroom](https://newsroom.lamresearch.com/inside-the-chip-advanced-packaging)) |
| **散热** | **直液冷** 已从“高端可选”变成“旗舰系统默认项”；机架与光模块也开始液冷化 | NVIDIA、Google、Microsoft、Marvell/XPO | GB300 NVL72 是 fully liquid-cooled；Maia 200 为闭环液冷；Google TPU Pods 长期液冷；XPO 模块把液冷推进到光模块级 | ([NVIDIA](https://www.nvidia.com/en-us/data-center/gb300-nvl72/?utm_source=chatgpt.com)) |
| **计算芯片基板** | 更大的 **interposer \+ IC substrate \+ RDL / glass / panel** 继续演进 | TSMC、KLA、Marvell、Broadcom | 大型多 die \+ HBM 设计使“基板”从配角变成性能与良率关键件 | ([KLA](https://www.kla.com/advance/innovation/advancing-connectivity-with-kla-new-ic-substrate-product-portfolio)) |
| **光互联 / 光电共封装（CPO）** | 2026 主流仍是**电 scale-up \+ 可插拔光**；真正公开把光学拉近到封装/近封装的，更多是 **Broadcom / Marvell custom XPU**，以及 Rubin Ultra 的 **direct optical** | Broadcom、Marvell、NVIDIA Rubin Ultra | **CPO 现在还不是主流 GPU 本体的标准 BOM**；更像 2027 之后逐步扩大 | ([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai)) |
| **超级电容器与飞轮储能** | 目前主要还是**机房/UPS/列级配电层**，不是芯片本体标准件 | Panasonic、Active Power、Schneider 等 | 这是 AI 工厂级基础设施，不是 GPU 封装级通用组件；主要用于应对 AI 负载毫秒级突增、削峰和短时支撑 | ([Panasonic Industrial](https://na.industrial.panasonic.com/whats-new/coming-soon-supercapacitors-next-gen-telecom-ai-datacenters)) |
| **先进封装** | 主线是 **CoWoS-S / L / R、3.5D XDSiP、hybrid bonding**，并继续向更大面积和更多 HBM 堆叠推进 | TSMC、Broadcom、AMD、Marvell、Applied、Besi | Blackwell / Rubin / MI450 / Maia / custom XPU 全都深度依赖先进封装；这也是 2026–2027 最硬的共性瓶颈之一 | ([3DFabric](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)) |

---

## **5）我最重要的几个判断**

**1\. 2026 仍然是 “HBM3E \+ 电互联 \+ 液冷大机架” 的一年，2027 才更像 “HBM4 / HBM4E \+ 更多自研 ASIC \+ 部分光化” 的一年。**  
这从 Rubin、MI450/455X、Ironwood、Broadcom 2nm custom XPU、HBM4 的量产节奏基本都能看出来。 ([NVIDIA](https://www.nvidia.com/en-us/data-center/technologies/rubin/))

**2\. 真正会卡住行业的，不是“算力需求”，而是 HBM、先进封装、液冷、电源分配。**  
需求侧预算已经足够大，约束反而更偏供给侧。 ([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

**3\. CPO 很重要，但 2026 还不是大多数主流训练 GPU 的标准卖点。**  
真正公开把光拉得更近的，是 Broadcom / Marvell 的 custom XPU 架构，以及 Rubin Ultra 的 direct optical；主流 GPU/TPU/Trainium 公开资料里仍以电互联 \+ 外部光模块为主。 ([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-showcases-industry-leading-solutions-scaling-ai))

**4\. “超级电容器与飞轮储能”是 AI factory 级问题，不是 GPU die 级问题。**  
它们重要，但多数情况下在 UPS / 列级 / 机房配电层，不在芯片本体 BOM 里。 ([Panasonic Industrial](https://na.industrial.panasonic.com/whats-new/coming-soon-supercapacitors-next-gen-telecom-ai-datacenters))

**5\. 对未公开信息，我最有把握的推测只有两类：**  
一类是 **节点 / 封装 / HBM 方向**，因为可由供应链公开信息反推；  
另一类是 **出货节奏**，因为可由 CapEx、GW 合同、HBM 供给和 TSMC 封装瓶颈交叉约束。  
但像 **单片 ASP、准确 mask count、真实良率、具体客户分配**，公开面仍然不够，我只能给区间，不能假装精确。

# **过去3个月AI基础设施与使用量脉冲报告**

## **截至 2026-04-09，重点观察 2026-03-09 至 2026-04-09**

## **一、先说结论**

过去3个月、尤其过去1个月，AI行业最重要的变化不是“需求见顶”，而是**需求继续强于供给，但瓶颈的位置在快速迁移**：从“有没有GPU”，转向“有没有电力、机房、HBM/先进封装、网络、液冷、变压器，以及能否按期交付”。这件事几乎被云厂商、芯片厂、存储厂、模型公司同时验证了。微软说需求仍超过供给；Google Cloud说在紧张供给环境下需求仍强；Oracle明确说AI训练与推理需求增长快于供给；Meta则说其计算需求增速快于自身供给，直到 2026 年后段自建设施上线前都将受限。([Microsoft](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2))

第二个核心结论是：**行业的容量单位正在从“几万/几十万张卡”升级到“GW级园区、长期容量协议、预付款锁算力”**。微软单季新增接近 1GW 容量；Meta 与 AMD 签下最高 6GW 多年代际部署协议；Anthropic 4 月 6 日披露，已与 Google/Broadcom 签下 2027 年起“multiple gigawatts”的下一代 TPU 容量协议；OpenAI 过去披露的 Stargate 规划也已走到多 GW 路线。这个尺度，明显比市场在 2025 年初普遍预想的更激进。([Microsoft](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2))

第三个结论是：**行业的核心KPI正在从“训练 FLOPS”转向“token economics”**，也就是每瓦、每美元、每单位延迟能产出多少高质量 token。微软明确说自己在优化“tokens per watt per dollar”；Google 在 4 月给 Gemini API 上线了 Flex/Priority 推理档位，直接把“便宜”和“高可靠高优先级”产品化；Micron 说快速增长的 AI inference 正在驱动围绕 token economics 的新架构；NVIDIA 与微软新一代平台都在强调更低 cost per token。([Microsoft](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2))

第四个结论是：**真正超预期的，不只是模型更强，而是使用量、会话长度、企业付费速度、预付锁产能的速度都在变快**。OpenAI 在 3 月 31 日自披露 API 已处理超过 15B tokens/min，ChatGPT 周活超过 9 亿，Codex 周活 200 万、3个月增长 5 倍；Google 说 Gemini 第一方模型已处理超过 10B tokens/min，AI Mode 查询长度是传统搜索 3 倍；Anthropic 则披露最重度 Claude Code 会话的 99.9 分位 turn duration 已从不到 25 分钟拉长到超过 45 分钟，且 \>$1M 年化客户数在几周内从 500+ 翻到 1000+。这说明“代理式长会话 \+ coding \+ 企业自动化”正在把 token 消耗和算力需求推向新台阶。([OpenAI](https://openai.com/index/accelerating-the-next-phase-ai/))

---

## **二、过去3个月，尤其过去1个月，最重要的正式与非正式消息**

## **1\) AI芯片与系统**

**3月16日，NVIDIA 发布 Vera Rubin 平台，且称 7 款新芯片已进入 full production。** 这不是普通的“下一代GPU发布”，而是从预训练、后训练、test-time scaling 到实时 agentic inference 的整栈设计。NVIDIA称 Rubin NVL72 在大模型训练上可用更少 GPU 完成大型 MoE 训练；在推理上可做到更高 throughput per watt 和更低 cost per token；其 BlueField-4 存储机架还把 KV cache 处理独立出来，号称可把推理吞吐提升到 5 倍量级。这里最值得注意的不是某个单点性能数字，而是**架构已经围绕推理、KV cache、agent workload、单位 token 成本做了重构**。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform))

**3月6日，Broadcom 披露 Q1 AI revenue 84 亿美元，同比增长 106%，并指引 Q2 AI semiconductor revenue 到 107 亿美元。** Broadcom 的 AI 收入主要来自 custom AI accelerators 和 AI networking，这说明**ASIC/TPU/定制芯片并不是边角料，而是在非常快速地做大**。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial))

**4月6日，Anthropic 公布与 Google/Broadcom 新协议：2027年起获得 multiple gigawatts 的下一代 TPU 容量。** Reuters 同日报道，这一安排对应的 Anthropic 算力接入大约在 3.5GW 量级；Broadcom 的 SEC 文件也证实了其与 Google 的长期 TPU 代际合作延续到 2031 年。交叉看下来，**Google TPU 体系正从“Google内部利器”升级为“外部头部模型公司可锁定的长期工业级算力平台”**。([Anthropic](https://www.anthropic.com/news/google-broadcom-partnership-compute))

**2月24日，AMD 与 Meta 公布多年代际部署协议，规模最高 6GW，首个 1GW 级部署将在 2026 年下半年开始。** 这说明 Meta 已不是“买卡”逻辑，而是**按GW规划长期算力供给，并主动做供应链多元化**。([AMD](https://www.amd.com/en/newsroom/press-releases/2026-2-24-amd-and-meta-announce-expanded-strategic-partnersh.html))

**1月26日，微软发布 Maia 200，并明确说这是为 inference economics 设计的。** 其官方说法是相对自家现有最新硬件可带来 30% performance per dollar 改善，并已服务 GPT-5.2、Microsoft Foundry 与 Copilot，还用于合成数据和强化学习。微软自己下场做芯片，且宣传口径直接对准 token economics，也再次验证“推理主导设计”的拐点。([The Official Microsoft Blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/))

**非正式但重要的消息**：Reuters 3月11日报道 Meta 展示了四款新的自研 AI 芯片路线；2月26日 Reuters 引述 The Information 报道 Meta 与 Google 达成多亿美元到数十亿美元级 TPU 租用安排，用于模型开发，不过这一点未见双方正式确认。我的判断是：哪怕这条单独消息未完全坐实，**其方向与 Meta-AMD 的 6GW 协议、Meta 的高 capex 指引、以及“供给约束到 2026 年大部分时间”这几个正式信息是同向的**。([Reuters](https://www.reuters.com/world/asia-pacific/meta-unveils-plans-batch-in-house-ai-chips-2026-03-11/))

---

## **2\) AI数据中心与云容量**

**Google 的扩张节奏最激进。** Alphabet 在 2 月初财报会上给出 2026 年 capex 指引 1750亿到1850亿美元，Q4 capex 已达 279 亿美元，且“约 60% 用于服务器、40% 用于数据中心和网络”；Google Cloud backlog 在 2025 年底达到 2400 亿美元，季度环比增 55%、同比翻倍以上。更关键的是，Google 说 2026 年其 ML 计算里“略高于一半”将投向 Cloud 业务。含义很直接：Google 不是只给自己训练，而是在把大量最优算力转为外部云供给。([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

**微软的扩容速度同样惊人。** 1 月底财报会披露，单季资本开支 375 亿美元，约三分之二投向短生命周期资产，主要是 GPU 和 CPU；该季度还新增了“接近 1GW”容量，但 Nadella 同时强调需求仍超过供给。也就是说，**即便以这种级别的投入，仍然不够填满前台需求**。([Microsoft](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2))

**Meta 明确把 2026 capex 提到 1150亿到1350亿美元。** 管理层直说 Q4 的 capex 主要由数据中心、服务器和网络驱动，并明确表示 2026 年大部分时间仍将受容量限制，直到年底前部分自建设施上线。([Q4 Capital](https://s21.q4cdn.com/399680738/files/doc_financials/2025/q4/META-Q4-2025-Earnings-Call-Transcript.pdf))

**Amazon 也把 2026 capex 提到约 2000 亿美元。** Reuters 在 2 月引述 Amazon 管理层称，AWS 需求强劲但仍有容量约束，同时 S\&P Global Visible Alpha 口径显示四大云厂商 2026 年合计 capex 预计超过 6300 亿美元。官方与外部测算放在一起看，**超大厂的 AI 基建军备竞赛在 2026 年并没有停下，反而继续加速**。([Reuters](https://www.reuters.com/business/retail-consumer/amazon-projects-200-billion-capital-spending-this-year-2026-02-05/))

**Oracle 是本轮最能说明“需求如何被锁定”的公司。** 其 3 月财报披露 RPO 达 5530 亿美元，同比增长 325%，并明确说当季 RPO 的大部分增加来自大规模 AI 合同，且这些合同里设备常由客户预付款资助，甚至由客户自己提供 GPU。Oracle 还说为了支撑需求计划融资 500 亿美元，且其中 300 亿美元几天内就被超额认购。这个信号非常强：**客户不仅愿意买云，而且愿意提前出钱把产能锁住**。([Oracle Investor Relations](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Fiscal-Year-2026-Third-Quarter-Financial-Results/default.aspx))

**CoreWeave 则提供了新型云厂商视角。** 公司 4 月 1 日的官方材料说，行业已进入“inference 成为关键焦点”的阶段，且 inference 需求增长快于底层硬件部署速度；其截至 2025 年末的 revenue backlog 达 668 亿美元，较年初增长超过四倍。说明即便是“纯AI云”玩家，也不是担心卖不掉，而是担心机器上得不够快。([CoreWeave](https://www.coreweave.com/news/coreweave-delivers-leading-inference-performance-in-mlperf-r-benchmark))

---

## **3\) Token 使用量、推理量、会话复杂度**

**OpenAI 给了最激进的一组自披露数据。** 3 月 31 日公告称，ChatGPT 周活已超 9 亿、订阅用户超 5000 万，API 每分钟处理超过 150 亿 tokens；Codex 周活超 200 万，3 个月增长 5 倍，且使用量月增速仍高于 70%；企业收入占比已超 40%，并预计年底接近与消费业务持平。就算把这些数字打一点保守折扣，它也足以说明：**token 的工业化吞吐已经进入“每分钟十亿级以上”的时代，且 coding/agent 正在成为非常强的增量来源。** ([OpenAI](https://openai.com/index/accelerating-the-next-phase-ai/))

**Google 也给出直接 token 数据。** Alphabet 管理层说，其第一方 Gemini 模型现在通过客户直接 API 调用已处理超过 100 亿 tokens/min，高于上一季度的 70 亿；Google AI Studio 3 月新增了 spend cap、RPM/TPM/RPD dashboard、自动升档 usage tier，4 月又把 Flex/Priority inference tier 上线。把这些连起来看，说明 **Google 看到的不是“偶发峰值”，而是必须用配额、分层服务、可靠性等级来管理的持续高流量市场。** ([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

**Anthropic 的数据最能说明“工作负载在变长、变自动化、变企业化”。** 2 月的官方研究称，最长运行的 Claude Code 会话里，99.9 分位单回合持续时间从 2025 年 10 月不到 25 分钟提高到 2026 年 1 月超过 45 分钟，且内部挑战任务成功率翻倍、人工干预下降；3 月 24 日的 Economic Index 进一步说，Claude.ai 流量的 top 10 任务占比已从 2025 年 11 月的 24% 降到 2026 年 2 月的 19%，任务分布更分散，而 coding 正从网页端“辅助式使用”迁移到更自动化的一方 API 流量中，销售外联自动化、自动交易与市场运营等业务流在 3 个月内至少翻倍。也就是说，**AI 不只是更多人用了，而是更多机器在“更长、更自主地用”**。([Anthropic](https://www.anthropic.com/research/measuring-agent-autonomy))

**Google Search/AI Mode 的数据说明，搜索型 AI 正在显著抬升每次查询的 token 强度。** Google 说美国用户 AI Mode 的单用户日查询量较上线时翻倍，且 AI Mode 查询平均长度是传统搜索的 3 倍，很多会继续追问，且近六分之一查询是非文本。这个变化很关键，因为它意味着**即便查询次数不暴增，单次查询的 token、上下文和推理成本也在上升**。([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

---

## **4\) 模型训练量：直接数据少，但代理变量非常强**

模型公司很少公开训练 FLOPs、总训练 token、有效 GPU 小时，所以**过去3个月最有用的办法不是盯“FLOPs官方数”，而是盯训练/后训练/推理一体化的容量承诺与交付节奏**。从这个角度看，NVIDIA Rubin 明确覆盖 pretraining、post-training、test-time scaling；Anthropic 锁定 multiple GW TPU；Meta-AMD 协议上到 6GW；微软单季加近 1GW；OpenAI、Oracle、CoreWeave 都在往多园区、大规模预留/预付模式走。**这说明 frontier 训练与后训练规模仍在继续抬升，而且 test-time compute 已经成为新增训练预算之外的第二大吞吐黑洞。** ([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform))

---

## **三、交叉验证后，我认为最重要的“最新进展”和“超预期发现”**

### **1\. 超预期发现：算力采购从“采购设备”变成“采购发电侧可兑现的长期容量”**

Anthropic/Google/Broadcom、Meta/AMD、微软单季扩容、OpenAI/Oracle/Stargate 这些信号放在一起，意味着头部玩家争夺的已经不是单点芯片，而是**可持续供电、可交付机房、可扩展网络、长期锁定的 GW 级 token 工厂**。这是比“多买一点 GPU”更重资产、更长周期、更不容易反转的需求形态。([Anthropic](https://www.anthropic.com/news/google-broadcom-partnership-compute))

### **2\. 超预期发现：推理与 agent 并没有把训练替代掉，而是在训练之外又加了一层巨大的算力需求**

NVIDIA、Google、微软、Micron、CoreWeave 的官方口径都在转向 inference economics，但同时没有任何一家说预训练结束了。相反，行业在讲 pretraining、post-training、test-time scaling、real-time agentic inference 的全链路。也就是说，**不是“训练见顶、转推理”，而是“训练还在，推理又爆了”**。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform))

### **3\. 超预期发现：存储与内存的重要性被严重低估**

Micron 3 月直接说，2026 年数据中心 DRAM+NAND bit TAM 将首次超过行业总 TAM 的 50%，而且 AI 与传统服务器需求都受到 DRAM/NAND 供应不足约束；NAND 需求在可预见时期内显著强于供给；HBM4 已经开始量产出货并对准 Rubin，三星也已为 AMD MI455X/Helios 提供 HBM4。再结合 NVIDIA 对 KV cache、Micron 对向量数据库与 KV cache offload 的表述，说明**下一阶段的价值池和瓶颈不只在算力芯片，还在 HBM、DDR、SSD、内存层级设计和数据搬运。** ([Micron Technology](https://investors.micron.com/static-files/9c0becf5-df56-4eec-bd67-453dda68b273))

### **4\. 超预期发现：企业付费速度和高端客户密度提升很快**

Anthropic 说年化支出超 100 万美元的客户数从 2 月融资时的 500+ 到 4 月 6 日已超 1000；OpenAI 说企业收入已超 40%；Oracle 的 AI 合同甚至出现客户预付款、客户自带 GPU；Google Cloud backlog 短时间跃升到 2400 亿。说明这轮基础设施扩张背后，**不是纯粹的“故事驱动”，而是已有大额合同和企业预算在前面拉着跑。** ([Anthropic](https://www.anthropic.com/news/google-broadcom-partnership-compute))

### **5\. 超预期发现：软件使用形态正迅速朝“更长上下文、更强自主、更高QoS差异化”演进**

Google 推 Flex/Priority，OpenAI API 15B TPM，Anthropic 最长会话 45 分钟以上，AI Mode 查询更长且跟进问答更多。这意味着未来 1–2 年里，**不是所有 token 都一样值钱**：低延迟、可靠性、长期会话、带工具调用的推理，会形成更明显的价格层和硬件分层。([blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-flex-and-priority-inference/))

---

## **四、未来1–2年评估AI发展的框架**

我建议用下面这套框架看 2026–2027，而不是只看模型榜单。

## **A. 硬件需求端：看“要多少算力”，更要看“哪种算力”**

重点看六个指标：

1. 预训练需求是否继续抬升；  
2. 后训练/强化学习/合成数据需求是否扩容；  
3. test-time scaling 是否变成主流；  
4. agent/coding/搜索/多模态是否抬升单位请求 token；  
5. 单位 workload 的内存、KV cache、存储吞吐需求；  
6. 用户愿意为低延迟、高可用、多轮长会话付多少钱。  
   过去3个月的数据表明，这六项里至少前五项都在走强。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-vera-rubin-platform))

## **B. 硬件生产端：看“能造多少”，更要看“能按期交付多少”**

不能只盯晶圆厂。真正要看的链条是：先进逻辑制程、先进封装、HBM、DDR/NAND、交换芯片/NIC/光模块、整机柜、液冷、变压器、并网、电力接入、机房施工、软件栈可移植性。IEA 2026 报告说，全球数据中心投资 2024 年已接近 5000 亿美元；大型 AI 数据中心用电可达普通 AI 数据中心的 20 倍；大约 20% 的规划项目可能因电网约束延误，输电线建设往往需要 4–8 年，变压器和电缆等待时间在过去3年翻倍。这是未来 1–2 年最硬的约束。([IEA](https://www.iea.org/reports/energy-and-ai/executive-summary))

## **C. 云服务需求端：看“云厂商敢不敢继续投”**

这里看四个指标：capex 指引、RPO/backlog、预付款/保底协议、单位 token 的毛利改善。过去3个月，Google 给出 1750–1850 亿 capex，Meta 给 1150–1350 亿，Amazon 约 2000 亿，微软单季 capex 375 亿且继续供不应求，Oracle RPO 5530 亿且 AI 合同大量预付，CoreWeave backlog 668 亿。这个组合告诉我：**云供给侧未来1–2年继续扩产的意愿非常强，而且已有合同做支撑。** ([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

## **D. 云服务消费端：看“谁真的把 token 变成收入”**

这里看五个指标：周活/月活、TPM、企业客户数与大客户密度、代理/编码/搜索等高价值场景渗透、以及收费层级的形成。OpenAI、Google、Anthropic 过去1个月给出的数字说明，**消费端不只是聊天机器人，而是在往搜索、编码、企业流程自动化、多模态助手和长会话代理渗透**。([OpenAI](https://openai.com/index/accelerating-the-next-phase-ai/))

## **E. 横向总指标：用“每度电能换多少高毛利 token”统一衡量**

未来 1–2 年最好的总指标，不是单纯训练 FLOPs，也不是单纯用户数，而是：  
**每瓦/每美元/每机架/每站点，能否持续产出可收费的高价值 token，并维持较高利用率。**  
这也是为什么微软讲 tokens per watt per dollar、Google把推理QoS分层、NVIDIA和Micron都在重构围绕推理与内存的系统。([Microsoft](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2))

---

## **五、用这套框架评估未来1–2年：我的基准偏乐观判断**

## **1\) 硬件需求端：高景气，且 2027 大概率强于 2026**

我偏乐观。理由不是“模型会更神”，而是**需求结构更厚了**：预训练还在，后训练和 RL 在扩，test-time scaling 变贵，agent/coding 把会话拉长，搜索和多模态把 token/请求抬高。OpenAI、Google、Anthropic 过去一个月给出的使用与会话数据，已经足够说明 2026 年不是“试验年”，而是“工业流量年”。([OpenAI](https://openai.com/index/accelerating-the-next-phase-ai/))

## **2\) 硬件生产端：能扩，但扩得没有需求快**

芯片本身会继续扩，尤其是 NVIDIA、Broadcom/Google TPU、AMD、微软自研、AWS Trainium 等多路线并行；但 HBM、先进封装、机房通电、液冷、并网、变压器仍是慢变量。Micron 和 IEA 的信息几乎把这件事说透了：**真正限制 2026–2027 的，不是“会不会下单”，而是“能不能把订单变成可运行的系统”**。([Broadcom Inc.](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial))

## **3\) 云服务需求端：继续加杠杆扩产，且合同可见度提升**

从 Google Cloud backlog、Oracle RPO、CoreWeave backlog、Microsoft 的商业合同储备、Amazon/Meta/Alphabet capex 指引看，云供给侧未来1–2年的策略仍是**抢地、抢电、抢芯片、抢大客户锁单**，而不是收缩。这里最大的风险不是需求塌陷，而是交付不及预期导致收入确认滞后。([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

## **4\) 云服务消费端：从“聊天”升级到“工作流”**

未来 1–2 年里，最强的付费方向大概率不是纯聊天，而是四类：  
**编码代理、企业自动化、搜索/检索增强、多模态工作流。**  
证据已经出现：OpenAI 的 Codex、Anthropic 的 Claude Code 和 API 自动化流量、Google AI Mode/Antigravity 都在朝这个方向走。([OpenAI](https://openai.com/index/accelerating-the-next-phase-ai/))

## **5\) 总判断**

我的基准偏乐观判断是：**2026–2027 年 AI 行业更像“电力与工程学约束下的高成长基础设施行业”，而不是“靠情绪支撑的题材行业”。** 需求大概率继续增长，最可能压制增长斜率的因素是供给链、并网、电力和交付，而不是客户突然不想用了。([Oracle Investor Relations](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Fiscal-Year-2026-Third-Quarter-Financial-Results/default.aspx))

---

## **六、需求与生产的不匹配，主要在哪**

## **1\. 最大的不匹配：算力需求按季度爆发，电力与机房供给按年度/多年爬坡**

芯片和服务器加单可以很快，但电网接入、变压器、输电线、土地审批、机房施工、冷却系统部署都更慢。IEA 给出的 4–8 年输电线建设周期和关键设备等待期拉长，是最硬的现实约束。([IEA](https://www.iea.org/reports/energy-and-ai/executive-summary))

## **2\. 第二个不匹配：GPU/ASIC 在扩，HBM/内存/存储与封装跟不上同样速度**

Micron 说 DRAM/NAND 都偏紧，NAND 需求显著超过供给，HBM4 已开始量产但 HBM4E 还要到 2027。意味着未来 1–2 年里，**“有芯片不代表有完整系统”**。([Micron Technology](https://investors.micron.com/static-files/9c0becf5-df56-4eec-bd67-453dda68b273))

## **3\. 第三个不匹配：云厂商签单速度快于可兑现容量交付速度**

Oracle 的预付款合同、Google/Anthropic 的多 GW 容量协议、Meta/AMD 的 6GW 协议都表明需求方愿意先签、先付，但实际收入确认要看设备、机房和电力何时到位。([Oracle Investor Relations](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Fiscal-Year-2026-Third-Quarter-Financial-Results/default.aspx))

## **4\. 第四个不匹配：软件生态多元化速度慢于硬件多元化速度**

芯片供给正在从单一 NVIDIA 走向 TPU、Trainium、Maia、AMD、定制 ASIC 并存，但高效的软件可移植性、调度、兼容层还在追赶。OpenAI 已公开说其基础设施与硅栈跨 Microsoft、Oracle、AWS、CoreWeave、Google Cloud，以及 NVIDIA、AMD、Trainium、Cerebras 和自研芯片，这本身就是对“必须多元化”的承认。([OpenAI](https://openai.com/index/accelerating-the-next-phase-ai/))

---

## **七、最应该优先解决什么**

### **第一优先：电力优先，而不是芯片优先**

未来 1–2 年最重要的不是“多拿一点卡”，而是**先拿到电、变电站、并网时隙、液冷、施工资源**。谁把“功率可兑现”先锁住，谁就更可能把 capex 变成收入。IEA 的结论对这件事是决定性的。([IEA](https://www.iea.org/reports/energy-and-ai/executive-summary))

### **第二优先：提前锁 HBM、封装、交换与存储**

Micron、Samsung、NVIDIA 的信息共同表明，HBM4、KV cache、内存层级与高速互连是未来系统瓶颈。要解决不匹配，必须把采购和设计从“GPU中心主义”改成“整机架/整系统中心主义”。([Micron Technology](https://investors.micron.com/static-files/9c0becf5-df56-4eec-bd67-453dda68b273))

### **第三优先：把 workload 分层，按 token 价值路由到不同硬件**

Google 的 Flex/Priority、微软的 token economics、NVIDIA Rubin 对不同阶段 workload 的分层设计，说明未来最有效率的做法不是“一种芯片跑所有东西”，而是**把高可靠低延迟 agent、长上下文、批处理推理、训练、后训练分开调度**。([blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-flex-and-priority-inference/))

### **第四优先：通过预付款、保底采购、容量市场化降低建设风险**

Oracle 已经示范了客户预付与客户自带 GPU；Google/Anthropic、Meta/AMD 的长期容量协议也指向同一方向。未来 1–2 年，融资结构和合同结构本身就是竞争力。([Oracle Investor Relations](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Fiscal-Year-2026-Third-Quarter-Financial-Results/default.aspx))

---

## **八、市场规模预测（美元，基于上面披露与交叉验证后的基准偏乐观估算）**

下面这些不是公司指引，而是我基于过去3个月披露的 capex、backlog/RPO、token 吞吐、HBM 路线图、电力约束做的区间推演。它们更适合拿来判断“方向和斜率”，不适合当成精确点估值。

## **1\) 数据中心 AI 加速器 \+ 紧耦合网络/系统收入池**

**2026E：3000亿–3800亿美元**  
**2027E：4200亿–5500亿美元**

理由：NVIDIA 单季数据中心收入已达 623 亿美元；Broadcom 单季 AI 收入 84 亿、下一季 AI 半导体指引 107 亿；再加上 AMD、云厂自研 TPU/Trainium/Maia、以及高端网络/机柜系统，2026 的“AI算力硬件收入池”已经很难再用 1000 多亿美元去理解。这里我故意用“加速器+紧耦合系统”而不是“纯 GPU 芯片”，因为各家披露口径差异很大。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026))

## **2\) HBM 市场**

**2026E：450亿–550亿美元**  
**2027E：600亿–750亿美元**

理由：Micron 在 2025 年底给出的官方判断是 HBM TAM 从 2025 年约 350 亿美元，以约 40% CAGR 增长到 2028 年约 1000 亿美元；3 月又进一步披露 HBM4 已开始量产出货，且 HBM4E 将在 2027 年爬坡。用这个路径推，2026–2027 的区间大致在上述范围。([Micron Technology](https://investors.micron.com/static-files/530bd7ed-a8c8-4687-af4a-8c129f740e09))

## **3\) 广义 AI 数据中心 CapEx（超大云 \+ 新型AI云 \+ 关键园区建设）**

**2026E：6500亿–7500亿美元**  
**2027E：8000亿–9500亿美元**

理由：Alphabet 官方指引 1750–1850 亿，Meta 1150–1350 亿，Amazon 约 2000 亿，微软单季 capex 375 亿、按当前节奏年化已超过 1500 亿；Reuters/S\&P 估算四大云厂 2026 年合计已在 6300 多亿级。再加上 Oracle、CoreWeave 等外延投入，2026 年广义 AI 基建 capex 看到 6500–7500 亿美元并不激进。2027 年能否冲到 8000 亿以上，关键看电力和交付。([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

## **4\) AI 云算力收入（IaaS/PaaS 中可归因于AI工作负载的部分）**

**2026E：1800亿–2400亿美元**  
**2027E：2600亿–3400亿美元**

理由：Google Cloud backlog、Oracle RPO、CoreWeave backlog、微软与 AWS 的强劲需求都说明 AI 云不是小池子了。但这个口径最难精确，因为会与通用云收入重叠。我给出的是“可归因于训练、后训练、推理、agent 运行的云收入池”估算，而不是全部云收入。([Alphabet Investor Relations](https://abc.xyz/investor/events/event-details/2026/2025-Q4-Earnings-Call-2026-Dr_C033hS6/default.aspx))

## **5\) 大模型 API / 订阅 / 企业代理软件收入池（不含底层云）**

**2026E：700亿–1100亿美元**  
**2027E：1200亿–1800亿美元**

理由：仅 OpenAI 3 月底自披露已在 20 多亿美元/月收入量级，Anthropic 4 月初自披露 revenue run-rate 已超 300 亿美元，且大客户数快速上升；再加上 Google、微软 Copilot、其他 API 与企业代理层软件，这个池子 2026 年看到数百亿美元中高位是有依据的。这里的不确定性主要来自是否把某些嵌入式 AI 功能单独拆出来计价。([OpenAI](https://openai.com/index/accelerating-the-next-phase-ai/))

下面直接贴正文，保留原始编号索引；文末附材料清单，对应文中的 `[P] / [R] / [M]`。

# **2026年4月AI硬件前瞻报告**

## **从“抢GPU”到“拼系统”：近两个月半导体与AI芯片产业的新方向、瓶颈与机会**

**时间范围**：以 2026 年 2 月 9 日—2026 年 4 月 9 日的公开材料为主，少量 1 月中下旬材料仅作为趋势背景，不作为核心结论的唯一证据。  
**材料范围**：本报告交叉整理了 **50+ 条**官方公告、财报电话会、路透社报道、TrendForce、TechInsights、Counterpoint、Omdia、The Next Platform、SemiWiki、The Information 等材料。  
**方法说明**：

1. 优先使用官方公告、财报电话会、公司新闻稿、公开技术材料；  
2. 以 Reuters 作为高质量二次确认；  
3. 将 TrendForce / TechInsights / Counterpoint / Omdia / The Next Platform / SemiWiki 作为产业链与技术结构的“解释层”；  
4. 将 The Information、供应链口径、论坛型文章列为“高信号但未完全官方确认”的非正式线索；  
5. 报告中把信息分为三类：**已确认事实**、**高概率信号**、**推演判断**。

---

# **一、执行摘要：先给结论**

过去两个月，半导体，尤其是 AI 芯片产业，最重要的变化不是“又有一颗更快的 GPU 出来”，而是产业的竞争中心明显从**单颗计算芯片**转向了**完整 AI 系统栈**。这条系统栈至少包括六层：  
**计算芯片（GPU/ASIC/CPU）—高带宽内存（HBM）—先进封装—机架内/机架间互连（NVLink/以太网/光互连/CXL）—供电与散热—软件栈与可移植性**。  
过去两个月几乎所有头部厂商的重要动作，都能放进这六层框架里理解。

如果只用一句话概括：  
**AI 硬件产业正在从“算力器件之争”进入“系统工程之争”，而且系统工程中的第一瓶颈已经从 GPU 算力本身，转向 HBM、封装、互连、供电和软件兼容性。**

更具体地说，我认为有十个最关键的判断：

### **1\. NVIDIA 仍是中心，但它自己也不再把竞争定义为“卖GPU”**

过去外界对 NVIDIA 的理解还是“更快一代 GPU \+ 更紧的 CUDA 生态”。但 2026 年 3 月 GTC 之后，NVIDIA 对外释放的信号非常清楚：它卖的不是一颗芯片，而是一个**由七颗核心芯片和多种机架组成的 AI 工厂平台**。Rubin 平台的官方表述就是“七颗新芯片已进入全面生产”，而且把 GPU、CPU、LPU、DPU、网卡、交换芯片、存储层都定义成一个整体。\[P01\]  
这说明即便是最强的 GPU 厂商，也已经把核心竞争力重新定义为**系统级协同设计**，而不是单芯片绝对性能。

### **2\. 未来 12—18 个月，HBM 仍是最硬的物理瓶颈**

Micron 已宣布面向 Rubin 的 HBM4 36GB 12H 量产，单堆栈带宽超过 2.8TB/s；Samsung 宣布商用 HBM4，标称 11.7Gbps、可进一步拉到 13Gbps；SK hynix 则强调其 HBM4 具备 2048 I/O、2.54 倍上代带宽、40% 以上能效改善。\[P07\]\[P08\]\[P09\]  
表面上看，三大厂都在“冲 HBM4”，但越是同时冲，越说明系统正在被 HBM、TSV、堆叠、测试、封装、逻辑基底与 cleanroom 扩张所绑定。Micron 自己在电话会上也已明说，AI 与传统服务器需求都同时受到 DRAM/NAND 供给不足约束。\[P07\]\[M09\]

### **3\. 先进封装已经上升为与工艺节点同等级的战略变量**

TSMC 2026 技术研讨会不再只是讲 3nm / 2nm / A16 / A14，而是把 3DFabric、SoIC、InFO、CoWoS、SoW 一并放到技术核心位置。\[P10\]  
Broadcom 公开说 TSMC 已经“打到产能极限”，并且这件事在 2026 年已经成了 choke point；ASML 也公开表示要往先进封装工具拓展；ASE 直接在高雄追加 178 亿新台币建设新厂，明确点名为了 AI 芯片需求。\[R02\]\[R08\]\[P17\]  
这意味着：**先进节点不再自动等于先进产品，先进封装能力决定谁能把先进节点真正变成大规模可交付的 AI 系统。**

### **4\. 推理（Inference）正在从“GPU 的一个场景”分化成独立硬件赛道**

过去几年训练主导了市场叙事，所以很多人默认“训练强 \= 推理强”。这个逻辑在过去两个月被大幅修正。  
NVIDIA 自己在 GTC 上把 2027 年前的 AI 芯片收入机会从 5000 亿美元上调到 1 万亿美元，其中一个核心逻辑就是推理的爆发；同时其官方平台已经公开采用“Rubin 负责 prefill、Groq 3 LPU 负责 decode”的思路。\[R10\]\[P01\]  
AWS 与 Cerebras 的新服务也采用了几乎相同的分工：Trainium3 负责 prefill，Cerebras 负责 decode。\[R13\]  
这不是偶然，而是在说明：**推理已经开始出现与训练不同的瓶颈函数、不同的最优芯片结构、不同的内存结构与不同的软件调度方式。**

### **5\. CPU 在 AI 基础设施中的战略地位正在反弹**

2023—2025 的主流叙事是“GPU 吃掉一切”，CPU 只是辅助器件。但现在 CPU 的角色正在重估。  
NVIDIA 的 Vera CPU 被单独拉出来做机架；Arm 甚至第一次从 IP 公司正式迈入完整生产级芯片，推出 Arm AGI CPU，并明确把 agentic AI 带来的协调、数据移动、推理编排作为 CPU 需求再扩张的理由。\[P01\]\[P16\]\[R10\]  
这背后反映的是：**AI 正从大批量矩阵计算，转向包含调度、环境仿真、agent coordination、KV 管理、存储调用、工具调用的复合系统。** 在这个系统里，CPU 不再只是“喂 GPU 的小弟”，而是 AI 工厂的编排层。

### **6\. Hyperscaler 自研 ASIC 已经从“对冲方案”变成“基础配置”**

Google 的 TPU7x / Ironwood、AWS 的 Trainium3/4、Meta 的 MTIA 300/400/450/500、Microsoft 的 Maia 200，已经不再是“showcase 项目”，而是在真实上线、真实服务、真实采购、真实绑定模型路线。\[P02\]\[P03\]\[P04\]\[P05\]\[P06\]  
Meta 官方甚至明确说，未来两年将连续开发并部署四代 MTIA，并把产品节奏压到每六个月或更快；Google 的 Ironwood 直接以最高 9216 芯片 Pod 和 Optical Circuit Switch 作为系统定义；Microsoft 把 Maia 200 放进 Copilot、Foundry 和 synthetic data generation 流程；AWS 则已经把 Trainium3/4 作为与 OpenAI 战略合作的一部分。\[P02\]\[P03\]\[P04\]\[P06\]  
这说明：**自研 ASIC 已不再是可选项，而是云厂商控制成本、锁定模型迭代节奏、摆脱单供应商依赖的必选项。**

### **7\. 光互连、CXL、光交换，从“远期概念”走进采购与架构设计周期**

Broadcom 发布 400G/lane 光 DSP，直接为 1.6T 与后续 3.2T 光模块和 204.8T 交换体系打地基；Marvell 与 Lumentum 做面向 AI scale-up 基础设施的 OCS 演示，同时推出面向“AI memory wall”的 CXL switch；Google 的 Ironwood Pod 也明确写进了 OCS；NVIDIA 则在 Rubin 上强调 photonics 与更高能效互连。\[P12\]\[P13\]\[P14\]\[P03\]\[P01\]  
这意味着一件事：**AI 集群的下一个数量级，不可能靠全铜缆和传统机架内互连硬堆出来。**  
2026 年也许还不是大规模封装级光互连爆发年，但它几乎肯定是**设计定案年、客户验证年、生态绑定年**。

### **8\. 供电与 time-to-power，已成为仅次于 HBM 的第二大硬约束**

TrendForce 明确给出一个非常强的框架：全球数据中心电力容量从 2023 年的 84GW、2024 年的 98GW、2025 年的 120GW，上到 2026 年预计 152GW；其中 AI 服务器到 2026 年将消耗 55GW、同比增长 74%，占全部服务器电力容量的 52%，并且超过 50% 的 AI 服务器热管理方案会采用液冷。\[M01\]  
Microsoft 在单季度新增近 1GW 容量；NVIDIA 甚至把“固定功率数据中心里多塞 30% AI 基础设施”和“释放 100GW stranded grid power”写进官方表述。\[P06\]\[P01\]  
这说明：**AI 数据中心建设正在从“抢芯片”升级为“抢电、抢变压器、抢液冷、抢施工周期”。**

### **9\. 中国 AI 芯片栈的关键变量，不再只是“性能追没追上”，而是“软件是否更容易迁移”**

路透社援引供应链与客户测试信息称，Huawei 新一代 950PR 更受 ByteDance、Alibaba 等大客户欢迎，其中最关键的改变之一是它比上一代更兼容 CUDA 软件迁移；Reuters 之后又援引 The Information 报道 DeepSeek V4 将运行在 Huawei 芯片上。\[R03\]\[R04\]  
这说明一个重要变化：  
**中国国产 AI 芯片的竞争门槛，正从“先证明理论峰值算力”，转向“先解决模型迁移、部署稳定性、生态摩擦、供应可得性”。**  
一旦软件迁移成本显著下降，国产替代会从政策驱动的被动采购，变成真实可用的工程选择。

### **10\. 未来 12 个月，AI 硬件产业的最大增量收益，未必来自“卖最多 GPU 的公司”**

GPU 仍会是最大单点价值捕获者，但从边际增量看，更有弹性的环节可能来自：  
**HBM / 高端 DRAM、先进封装、OSAT、ABF/PCB、光 DSP / 光模块 / 激光器、CXL / 内存扩展、液冷、电力分配、rack-level integration、ASIC 设计服务与 semi-custom 平台。**  
换句话说，市场会越来越像 2024 年以后的“AI 工厂产业链”，而不是 2023 年那种“只看 GPU”的单点行情。

---

# **二、研究框架：为什么这次结论和以往不一样**

为了避免“把最新新闻堆一遍”而得出误判，这次我把过去两个月的信号按六条主线做交叉验证：

1. **计算芯片主线**：NVIDIA / AMD / Arm / AWS / Google / Meta / Microsoft / Huawei  
2. **存储与 HBM 主线**：Samsung / SK hynix / Micron / Counterpoint / TechInsights  
3. **封装与制造主线**：TSMC / ASE / Applied / ASML / Besi / SemiWiki  
4. **网络与光互连主线**：Broadcom / Marvell / Lumentum / Google / NVIDIA  
5. **电力与散热主线**：TrendForce / Microsoft / NVIDIA / Reuters  
6. **中国与地缘主线**：Huawei / DeepSeek / Reuters / TrendForce / 出口管制材料

结论之所以和一年前不同，不是因为某一家厂商突然“更强了”，而是因为过去两个月这些主线同时指向了同一个新中心：  
**AI 系统的边界条件已经从单芯片算力，转移到系统耦合效率。**

这意味着后面的所有判断都要换一套提问方式。  
旧问题是：“谁的 FLOPS 更高？”  
新问题是：“谁能在给定功率、给定 HBM、给定封装、给定网络、给定软件迁移成本下，交付更多有效 tokens 和更低单位成本？”

---

# **三、过去两个月最重要的“方向变化”**

## **3.1 从“GPU 路线图”变成“AI 工厂路线图”**

过去谈 NVIDIA，行业习惯问的是：B100 到 B200，再到 Rubin，性能怎么提升？  
但官方现在给出的答案，已经不是“某颗 GPU 提升多少”，而是**Vera Rubin 平台作为一个多芯片系统整体怎么服务 AI 工厂**。\[P01\]

Rubin 官方新闻稿里的几个细节值得特别重视：

* 官方直接使用“Seven New Chips in Full Production”表述，而不是单 GPU 量产。\[P01\]  
* 组件里除了 Rubin GPU、Vera CPU，还包括 NVLink 6、ConnectX-9、BlueField-4、Spectrum-6，以及 Groq 3 LPU。\[P01\]  
* 官方写明系统覆盖 pretraining、post-training、test-time scaling 与 agentic inference 全周期。\[P01\]  
* NVIDIA 明确说 AI 基础设施正从离散芯片和单机服务器，演进到 rack-scale、pod-scale、AI factory。\[P01\]  
* 在电力侧，Rubin 绑定了 DSX 平台、DSX Max-Q、DSX Flex，并把 power provisioning 写成核心卖点。\[P01\]

这个变化意味着两件事。  
第一，NVIDIA 不再满足于“作为一个 accelerator vendor 获利”，而是要把自己变成 AI factory 定义者。  
第二，整个行业后续的资本开支，不会只围绕“买多少 GPU”，而会围绕“买什么样的完整 rack / POD / fabric / storage tier / power stack”。

对比去年，最大的认知偏差在于：  
**外界还在用“芯片公司”的眼光看龙头，但龙头已经在用“数据中心系统公司”的方式定义市场。**

---

## **3.2 从“训练主导”转向“训练 \+ 推理 \+ agentic”的复合需求**

NVIDIA 在 GTC 上将到 2027 年的 AI 芯片收入机会从 5000 亿美元上调至 1 万亿美元，同时明确强调推理拐点已到来；Reuters 对其发布会的解读也把“inference inflection”放在标题级位置。\[R10\]  
这背后不是情绪，而是 workload 结构变了。

过去训练是王，因为：

* 一次训练吃掉巨量算力；  
* 大模型迭代速度快；  
* GPU 的通用性可以覆盖大部分工作。

但现在推理端正在出现三个新变量：

### **变量一：长上下文、Agent、工具调用、RAG，把“token 成本”推到战略层**

长上下文和 agent 让“生成一次答案”的硬件消耗不再是简单的一次前向计算，而是包含大量 KV cache 管理、工具调用、分支推理、环境交互、上下文保存与检索。这使得推理开始拥有不同于训练的成本函数。

### **变量二：推理被拆成 prefill 和 decode 两个物理特性不同的阶段**

Reuters 明确写到，NVIDIA 的 Rubin 芯片负责 prefill，而 Groq 3 新芯片负责 decode；AWS 与 Cerebras 的合作也几乎完全采用同一思路：Trainium3 处理 prefill，Cerebras 处理 decode。\[R10\]\[R13\]  
这意味着推理并不一定要由一颗“全能芯片”解决，而会出现**分阶段最优化**。

### **变量三：HBM 不再是唯一解**

TechInsights 对 NVIDIA 新 inference 芯片的解读非常有启发意义：Groq 3 LPU 代表了一种 **SRAM-dominant、HBM-free** 的 decode 架构方向，这会改变未来推理负载对 HBM 的消费方式。\[M10\]\[M11\]  
Omdia 对 LPU/LPX 的分析也指出，其价值在于提高 decode 阶段效率、减少不必要的 HBM 访问。\[M12\]

我的判断是：  
**2026—2027 年 AI 推理市场最关键的变化，不是 GPU 会被替代，而是推理将被分层，GPU 只是其中一层。**  
未来最有价值的系统，很可能不是“全由 GPU 构成”，而是“GPU \+ 专用 decode 芯片 \+ CPU \+ 扩展内存 \+ 更聪明的网络/存储层”的混合架构。

---

## **3.3 从“通用 GPU 主导”转向“云厂商自研 \+ semi-custom 常态化”**

过去，自研 ASIC 更多被看作巨头控制成本的对冲方案。  
但过去两个月的信号说明：它已经成为云厂商和头部 AI 公司基础设施策略的主轴之一。

### **Google：TPU7x / Ironwood 把“Google 自研芯片”正式变成外部可消费算力产品**

Google 官方技术博客强调，Ironwood 是围绕 9216 芯片级 Pod 去定义的，其系统是 ICI \+ OCS \+ DCN \+ 聚合 HBM 的整体。\[P03\]  
这不是一个“实验芯片”，而是具有完整网络与调度结构的超大规模 AI 基础设施。  
Google Cloud 文档还给出 future reservations / calendar mode 等资源预定能力，这意味着 TPU 不再只是内部资源，而是逐渐向外部用户提供更成熟的容量计划接口。\[P23\]

### **AWS：Trainium 不再是“能不能用”，而是“和谁深度绑定”**

AWS 与 OpenAI 的战略合作明确横跨 Trainium3 和 Trainium4，且直接写入更高 FP4 性能、更大带宽、更高 HBM 容量等下一代指标。\[P04\]  
与此同时，AWS 让 Uber 开始 pilot Trainium3，并在 AWS 数据中心中与 Cerebras 做 prefill/decode 协同。\[P05\]\[R13\]  
这表明 Trainium 已经进入“既自用又对外卖、既训练又协同推理”的阶段。

### **Meta：MTIA 节奏压到每六个月**

Meta 官方材料最重要的不是 MTIA 本身，而是两个组织能力信号：

1. 未来两年开发并部署四代新芯片；  
2. 通过模块化设计，把发布节奏压到六个月或更快。\[P02\]  
   这说明 Meta 不只是做一颗芯片，而是在建立一套能快速迭代 silicon 与 rack 的内部方法论。  
   Meta 同时强调其会继续采用多家外部 silicon 供应商，而自研 MTIA 作为中心。\[P02\]

### **Microsoft：Maia 200 已经进实际业务栈**

Microsoft 在 FY26 Q2 电话会上说得很直接：Maia 200 已上线，10+ PFLOPS FP4、30% 以上 TCO 改善，先用于 superintelligence team 的推理与 synthetic data generation，也会用于 Copilot 和 Foundry。\[P06\]  
这比单纯“下一代会更强”更重要，因为这意味着微软已经在用自研芯片改写内部成本结构。

### **Arm：从 IP 授权商变成生产级芯片提供方**

Arm 推出 AGI CPU，是这个周期里最容易被低估的事件之一。  
它的象征意义不在“Arm 做了一颗 CPU”，而在于：  
**过去最坚持中立平台定位的公司，也开始认为单纯卖 IP 不够了，必须更直接地介入生产级系统芯片。**  
Arm 的官方表述直接把它定位为面向 agentic AI 数据中心工作负载的 CPU；Reuters 则进一步指出，Arm 预计该产品五年后可带来约 150 亿美元年收入。\[P16\]\[R15\]

### **Broadcom：从“做网通和定制芯片”升级到 hyperscaler AI 定制主舞台**

Reuters 报道 Broadcom 与 Google 签订到 2031 年的长期协议，共同开发并供应未来多代定制 AI 芯片与 next-gen AI racks 相关部件；同时 Anthropic 将从 2027 年起获得约 3.5GW 的 Google AI 处理器算力。\[R01\]  
这很重要，因为它说明：

* Custom ASIC 的采购周期在拉长；  
* 与 rack / power / cloud capacity 绑定得更紧；  
* TPU 已不再只是“Google 自己用”，而是变成可作为第三方算力基础的供应源。

综合来看，**自研 ASIC 已经不是“GPU 不够买时的备胎”，而是未来 AI 基础设施的标准组成部分。**  
谁没有自研或 semi-custom 路线，谁未来就会在成本、供货、节奏和谈判权上持续处于被动。

---

# **四、GPU 仍然强，但它已经不是唯一主角**

这一段必须讲清楚，因为市场很容易在两个极端之间摇摆：  
一个极端是“GPU 永远无敌，其他都没戏”；  
另一个极端是“ASIC、LPU、CPU 一起出来，GPU 很快完蛋”。  
这两个判断都过于粗糙。

## **4.1 为什么 GPU 仍是 AI 系统的中心层**

即便在推理分化、自研 ASIC 普及的背景下，GPU 仍有三个难以取代的优势：

### **第一，灵活性**

训练算法、后训练、MoE、multimodal、agentic workflow 还在快速变化。  
GPU 的通用性意味着它能覆盖更多形态变化，这种“可错配但不至于完全失效”的灵活性，在今天仍然极具价值。

### **第二，生态粘性**

这不只是 CUDA 本身，而是完整的软件、编译器、开发者、模型优化、调试、部署链条。  
Huawei 950PR 新一代更受欢迎，很大原因恰恰是因为它更容易让开发者从 CUDA 环境迁移过去。\[R03\]  
也就是说，其他厂商的突破点，并不是“证明自己芯片性能更强”，而是“降低从 GPU 生态迁移出去的摩擦成本”。

### **第三，系统级整合速度**

NVIDIA 现在已经不是只在卖 GPU die，而是在卖整套 rack、fabric、CPU、DPU、NIC、switch、甚至存储层。  
当一家厂商能把计算、网络、功耗、软件一起打包卖时，它的竞争优势会比“单芯片快 15%”更难撼动。\[P01\]

## **4.2 但 GPU 的角色正在重新被定义**

GPU 不会被消灭，但它会被“重新安放”。  
未来 12—18 个月，它最可能承担的角色是：

* 训练主力与大部分通用后训练主力；  
* prefill 主力；  
* 需要灵活编程与高兼容性的复杂推理工作负载主力；  
* 混合系统中的中心层，而不是全部。

这也是为什么我认为未来最大的变化，不是“GPU 被谁取代”，而是：  
**GPU 将从“一切算力的统一平台”，变成“异构 AI 系统中的中心计算层”。**

这对 NVIDIA 并不一定是坏事。相反，如果它能持续主导系统集成，它仍然可能是最大赢家。  
但对产业链其他公司来说，这意味着机会窗口打开了：  
只要能够在 GPU 不擅长或性价比不优的层面补上能力，就有机会切进 AI 工厂价值链。

---

# **五、HBM：不是“重要组件”，而是 AI 时代的核心战略资源**

## **5.1 三大原厂同时冲向 HBM4，意味着什么**

从公开材料看，HBM 正在进入比 HBM3E 更剧烈的“产业争夺期”。

### **Micron**

Micron 在 GTC 期间宣布：其面向 NVIDIA Vera Rubin 的 HBM4 36GB 12H 已进入高量产，带宽超过 2.8TB/s，能效比 HBM3E 提升 20% 以上；同时还展示了 HBM4 48GB 16H 样品。\[P07\]

### **Samsung**

Samsung 2 月宣布商用 HBM4，强调持续 11.7Gbps 传输速率，超过 8Gbps 行业标准约 46%，并称可进一步拉高到 13Gbps；3 月又在 GTC 上继续强化 HBM4E 与 NVIDIA 合作信号。\[P08\]\[R20\]

### **SK hynix**

SK hynix 在 MWC 2026 上强调 HBM4 面向下一代 AI 数据中心平台，2,048 I/O、2.54 倍前代带宽、40% 以上能效改进。\[P09\]

仅从这些材料看，好像是“HBM 供给很充足，大家都在上新”。  
但真正需要读懂的是反面：  
**如果供给已经宽松，这些厂商不会同时把 HBM4、封装、长期合同、客户绑定放在这么前的位置。**

## **5.2 供给约束不是简单的 DRAM 片数量问题**

HBM 的供给约束至少来自五层：

1. DRAM wafer 能力；  
2. TSV、减薄、堆叠、热处理与测试；  
3. 逻辑基底与先进封装协同；  
4. cleanroom 和设备扩产速度；  
5. 客户的长期绑定协议。

Samsung 高层已公开推动与大客户签 3—5 年长期合同，并直言内存短缺还会持续驱动需求；Reuters 同时报道本季度 DRAM 价格预计上涨 50% 以上。\[R07\]\[R06\]  
Micron 则在财报口径中承认，AI 与传统服务器需求同时受 DRAM/NAND 供应不足限制。\[P07\]  
Counterpoint 还给出一个很能说明问题的趋势性判断：**面向 AI server compute ASIC 的 HBM 需求到 2028 年将增长 35 倍。**\[M06\]  
TechInsights 进一步将其概括为：DRAM 正面临“几年花钱都补不上的供给缺口”。\[M09\]

这告诉我们：  
HBM 的真实瓶颈，不是“有没有人会做 HBM”，而是**有多少 HBM 能在正确的时间、正确的封装能力、正确的客户协议下，变成系统可交付量。**

## **5.3 HBM 的产业影响：谁受益，谁受压**

### **受益方**

* HBM 原厂（Samsung / SK hynix / Micron）  
* 与 HBM 深度耦合的设备与材料供应商  
* 有能力处理更高层堆叠、更高热密度的封装与测试环节  
* 提前锁定长期合同的 hyperscaler / AI lab

### **承压方**

* 依赖 spot 市场或短单采购的二线云与 AI 公司  
* 只解决 compute die、不解决内存与封装协同的芯片设计公司  
* 下游终端（PC、手机、消费电子），因为传统 DRAM/NAND 资源会被 AI 服务器挤压

从这个角度看，我认为未来 12 个月行业里最重要的一条分化线，不是“有没有 AI 芯片”，而是：  
**有没有稳定拿到高端内存与配套封装的资格。**

---

# **六、先进封装：2026 年真正被重新定价的环节**

## **6.1 TSMC 的技术叙事已经发生结构性变化**

TSMC 2026 技术研讨会的公开页面，把先进逻辑节点与 3DFabric/SoIC/InFO/CoWoS/SoW 并列展示。\[P10\]  
这是一个非常清晰的信号：  
**先进封装不是附属项，而是先进制程路线图的必要部分。**

过去市场会把“节点领先”看作最关键竞争力。  
但在 AI 芯片时代，单颗 die 已经接近 reticle limit，多 die 拼接、2.5D/3D 堆叠、HBM 集成、chiplet 一体化越来越成为默认解法。  
所以先进节点必须通过先进封装才能变成真正的产品能力。

## **6.2 Broadcom 公开承认：TSMC 的容量限制已经卡住 2026 供应链**

Reuters 援引 Broadcom 高管称，TSMC 已经打到产能极限，而且这个限制在 2026 年已经成为 bottleneck，甚至“choked the supply chain”；并且短缺不只在芯片，还扩展到激光器和光模块相关 PCB，后者交期从约六周拉长到六个月。\[R02\]  
这段信息非常重要，因为它说明供应链瓶颈正在外溢：

* 不再只是前道产能紧张；  
* 已经同时牵动光器件、PCB、封装与测试；  
* 说明 AI 产业建设已进入“多瓶颈并行”的阶段。

## **6.3 OSAT 与封装厂开始显性扩产，不再只是被动接单**

ASE 于 3 月宣布在高雄开建两栋新楼，总投资 178 亿新台币，明确指出是为了满足 AI 芯片需求。\[P17\]  
这类动作的意义在于：  
**封装厂开始从跟随型扩张变成前置型投资。**  
这通常意味着客户已经给出较高可见度的中期订单预期，否则 OSAT 不会轻易做这么重的资本承诺。

## **6.4 ASML 进入先进封装工具，说明封装已从“制造末端”回到“工艺前台”**

Reuters 对 ASML CTO 的采访最有价值的一点是：ASML 不只谈 EUV，而是明确说要进入帮助“glue and connect multiple specialized chips”的先进封装工具市场，并把它视作 AI 芯片及其先进内存的关键构件。\[R08\]  
这等于从设备巨头视角再次确认：  
**先进封装已不再是低毛利后段业务，而是决定未来 AI 芯片上限的前沿制造领域。**

## **6.5 Hybrid bonding 的战略地位继续上升**

Reuters 对 Besi 的报道提到，先进封装已经成为行业关键瓶颈，而 hybrid bonding 被认为是支持下一代 AI 与 HPC 芯片的重要技术；其铜对铜直接连接可带来更快数据传输与更低功耗。\[R09\]  
虽然行业内部对 HBM 下一代究竟多快全面切到 hybrid bonding 仍有争议，但有一点基本可以确定：  
**未来几代 AI 芯片若要继续提升 die-to-die、logic-to-memory、memory-to-memory 的连接效率，bonding 技术一定是核心战场。**

## **6.6 我对先进封装的核心判断**

过去投资人喜欢把封装看成“受益环节”，但对未来 18 个月我更愿意把它定义为：  
**AI 芯片时代的生产率决定层。**

为什么这么说？因为前道工艺再先进，如果不能以足够良率、足够功耗、足够热设计、足够成本把多个计算 die 与多个 HBM 堆叠集成为可交付系统，那前道能力就无法有效转化为收入与市场份额。

所以，先进封装不是上游“锦上添花”，而是把先进工艺变成商业产品的最后一道门槛。  
谁掌握这道门槛，谁就掌握了 2026—2027 AI 硬件出货节奏的真实控制权。

---

# **七、光互连、光交换、CXL：AI 系统下一阶段的“隐藏主线”**

## **7.1 过去两个月，网络与互连层的信号强得不正常**

如果把过去两个月的 AI 芯片新闻按热度排序，很多人会先看到 Rubin、HBM4、Trainium、TPU。  
但如果按“对未来系统边界影响程度”排序，光互连和 CXL 很可能比大家意识到的更重要。

### **Broadcom：400G/lane 把 1.6T / 3.2T 时代提前铺路**

Broadcom 3 月 11 日宣布 3nm 400G/lane 光 DSP Taurus，面向 1.6T 模块，并明确表示这会为未来 3.2T 模块与 204.8T 交换容量打地基。\[P12\]  
这说明 AI 网络带宽的演进速度，并不是“慢慢跟着 GPU 需求走”，而是正在主动前置。

### **Marvell：光交换 \+ CXL 双线并进**

Marvell 与 Lumentum 演示面向下一代 AI scale-up 架构的 OCS；同时 Marvell 发布面向 “AI memory wall” 的新一代 CXL Switch，给出 4TB/s 聚合带宽，并把 composable memory、shared memory pool、sub-microsecond access 作为卖点。\[P13\]\[P14\]  
这表明 Marvell 押注的不是“某个单一 protocol”，而是一个更大的判断：  
**未来 AI 数据中心最缺的不是算力绝对值，而是算力与内存、内存与节点、节点与节点之间的低摩擦连接方式。**

### **Google：OCS 不再只是论文概念**

Google 的 Ironwood 技术博客把 OCS 直接写入 Pod 级系统定义，这几乎等于官方承认：  
在足够大规模的 AI 超级集群里，电交换与固定拓扑并不是最优解，至少不是唯一解。\[P03\]

### **NVIDIA：网络与 photonics 直接进入平台级叙事**

Rubin 平台把 Spectrum-6 SPX 与 photonics 写进官方表述，甚至给出“5 倍光功耗效率、10 倍韧性”的官方宣传口径。\[P01\]  
这也意味着 NVIDIA 认为互连层已经足够重要，值得与计算芯片并列叙述。

## **7.2 为什么互连现在比以前更重要**

原因有三：

### **第一，模型规模与上下文长度增加，数据移动的重要性高于过去**

训练时代，大家更关注每秒能做多少矩阵乘。  
但 agentic / reasoning / long context 时代，很多瓶颈会体现在：

* KV cache 搬运；  
* 多节点共享上下文；  
* 模型切片与重组；  
* 存储与内存之间的层级调度；  
* 多芯片、多机架之间的带宽与延迟匹配。

### **第二，封装与 HBM 已经逼近单封装内的边界**

当一颗封装里塞进更多 die 和更多 HBM 后，继续往上堆的成本和热设计都会急剧上升。  
这时如果能把更多内存和更多计算通过 CXL、OCS、光互连在更大范围内变成“近似共享”的资源池，系统边界就能继续扩展。

### **第三，功耗压力迫使行业降低电互连比重**

当带宽上到 1.6T、3.2T、甚至更高量级，全电互连的功耗和空间成本都会变得难以接受。  
所以无论是 Broadcom 的光 DSP、Marvell 的光交换，还是 NVIDIA 的 photonics 表述，本质都在回答同一个问题：  
**如何让 AI 集群继续扩张，而不会被铜线、功耗和机柜密度拖垮。**

## **7.3 我的判断：2026 是“光互连设计定案年”，不是“全面放量年”**

这里需要区分时间尺度。  
我不认为 2026 年就会出现大规模封装级光互连全面爆发。  
但是我认为 2026 年会出现三个更重要的变化：

1. 头部 hyperscaler 和 AI infra 厂商完成未来两代系统的互连路线定案；  
2. OCS / CPO / 更高阶光模块开始在设计与验证层面深度绑定客户；  
3. 市场开始把光器件、DSP、激光器、光交换、相关 PCB/基板，纳入“AI 核心受益链条”而不是“通信附属链条”。

这意味着未来 12 个月，在资本市场与产业订单层面，光互连相关公司的 re-rating 可能持续强于很多人预期。

---

# **八、内存墙与“推理内存重构”：CXL、近存算、KV 层级，将变成新主战场**

## **8.1 “内存墙”为什么在 2026 年突然被高频提起**

以前大家讲内存墙，多是学术概念。  
但今年不一样，因为大模型推理已经把它变成真实商业问题：

* 模型更大；  
* 上下文更长；  
* KV cache 爆炸；  
* decode 阶段对内存访问模式极其敏感；  
* HBM 又贵又紧缺。

在这种环境下，单纯“给更多 HBM”并不是无限可扩展的方案。  
于是出现了三条路：

### **路线一：继续增加 HBM 层数和带宽**

这是最直接也最贵的路线。  
Micron 的 HBM4 48GB 16H 样品、Samsung / SK hynix 的 HBM4 提速，本质都属于这条路。\[P07\]\[P08\]\[P09\]

### **路线二：把部分推理阶段改成 SRAM / HBM-free 优化**

TechInsights 对 Groq 3 LPU 的分析，正是这一方向的代表：在 decode 阶段减少对 HBM 的依赖，用 SRAM-dominant 架构提高能效和吞吐。\[M10\]\[M11\]

### **路线三：在系统层重新组织内存**

这条路线包括：

* CXL memory pooling；  
* near-memory acceleration；  
* 更智能的 KV cache storage tier；  
* SOCAMM / 其他新型服务器内存形态；  
* 把一部分原本必须塞进 HBM 的数据，转移到更低层级的共享内存或高速存储层。

Rubin 上的 BlueField-4 STX 和 DOCA Memos，官方就直接强调了 KV cache 的存储层扩展价值。\[P01\]  
Marvell 则把 CXL switch 定位成突破 memory wall 的关键组件。\[P14\]  
Micron 也把 SOCAMM2 直接与 Vera Rubin 系统绑定。\[P07\]

## **8.2 为什么这件事会决定未来推理市场份额**

训练时代，市场看重单次峰值吞吐。  
推理时代，更重要的是：

* tokens per watt；  
* tokens per dollar；  
* 长上下文成本；  
* 多轮对话保持成本；  
* agent memory 的保存、检索、扩展成本；  
* 系统利用率。

谁能用更便宜、更可扩展的方式处理 KV、共享上下文和多阶段推理，谁就会在推理业务中获得结构性优势。  
所以我认为未来最有潜力的不是某个“更快 5% 的 GPU”，而是那些能把 **HBM—CXL—SOCAMM—KV storage tier—decode accelerator** 整体打通的系统方案。

---

# **九、CPU 的复兴：AI 越智能，CPU 反而越重要**

这个结论很多人会本能反感，因为过去两年“GPU 吃掉一切”的叙事太强了。  
但从过去两个月的材料看，CPU 的战略权重确实在回升。

## **9.1 NVIDIA 自己就在强化 CPU 机架的重要性**

Rubin 平台中，Vera CPU 不是配角，而是单独成 rack，并被用于强化大规模 agentic AI 与 reinforcement learning 场景下的 CPU-based environments。\[P01\]  
这说明在 NVIDIA 眼里，AI 工厂不是单纯的 GPU farm，而是一个需要大量 CPU 环境去做测试、验证、协调与数据移动的复合系统。

## **9.2 Arm 的 AGI CPU 把“agentic AI 需要更多 CPU”说得非常直白**

Arm 的官方新闻稿写得很清楚：随着 AI 从训练转向持续运行的 agent，系统需要更多 CPU 去承担 reasoning coordination 和 data movement。\[P16\]  
这其实击中了 AI 产业一个容易被忽略的现实：  
**越接近真实业务系统，越不是纯矩阵乘。**

真实 agent 工作流包含：

* 任务编排；  
* I/O 管理；  
* 工具调用；  
* 多进程/多线程调度；  
* 服务拼装；  
* 外部 API 与数据库交互；  
* 多阶段安全和策略控制。

这些事情并不会天然被 GPU 吞掉，很多恰恰更适合 CPU 做。  
所以 Arm 的动作不是“逆风做 CPU”，而是顺着 AI 工作负载复杂化趋势去吃回一部分价值。

## **9.3 未来 CPU 会在哪些地方受益**

1. 大规模推理集群的 orchestration  
2. agent / RL / simulation 环境  
3. 数据预处理与后处理  
4. 存储、网络、控制平面  
5. GPU / ASIC 外围的计算密集型服务  
6. 低延迟、高度并发的部分在线推理业务

我对未来 12 个月的判断是：  
**AI 数据中心中 CPU 的 BOM 占比和战略话语权都会上升，不是因为 GPU 变弱，而是因为系统变复杂。**

---

# **十、地缘与中国：新的竞争点不只是“有没有 3nm”，而是“能不能形成可用栈”**

## **10.1 Huawei 950PR 的真正意义：软件迁移门槛降低**

Reuters 对 Huawei 950PR 的独家报道里有三个细节特别关键：

* ByteDance、Alibaba 等大客户客户测试反馈较好，并计划下单；  
* 新芯片更兼容 CUDA 软件系统，迁移更容易；  
* 今年计划出货约 75 万张，DDR 版本约 5 万元人民币，HBM 版本约 7 万元人民币。\[R03\]

这几条合在一起，比“峰值性能到底比 H20 强多少”更重要。  
因为真正决定中国市场国产 AI 芯片扩散速度的，不是理论跑分，而是：

* 是否容易部署；  
* 是否容易把既有模型迁过去；  
* 是否供应更稳定；  
* 是否总拥有成本更可控；  
* 是否在政策环境下更可持续。

## **10.2 DeepSeek 与 Huawei 的绑定，可能是中国 AI 栈的标志性事件**

Reuters 援引 The Information 报道称，DeepSeek 的 V4 模型将运行在 Huawei 芯片上，而且 DeepSeek 提前向国内供应商开放了新模型进行优化。\[R04\]  
这条消息的分量不只是“DeepSeek 用了华为”，而是如果它被后续更多证据坐实，意味着：

* 中国最具影响力的模型厂之一，开始围绕国产芯片做系统协同；  
* 国产硬件与国产模型不再是松散配对，而是更前置的联合优化；  
* 中国 AI 产业可能从“用不到最先进美国芯片的替代方案”，走向“围绕国内硬件约束反向优化模型与系统”的新阶段。

## **10.3 出口管制会继续推高“可替代生态”的价值**

美国关于 ASML 及其他设备对华限制的新提案、MATCH Act 的思路、以及 imec 拿到全球不到十台级别的 High NA EUV，都说明先进制造设备的地缘化还在升级。\[R14\]\[R15\]  
这会带来两个后果：

### **后果一**

中国在前沿工艺节点上的追赶会继续受阻，短期很难在“最先进制程 \+ 最先进设备”上正面追平。

### **后果二**

中国企业反而会更强烈地推动：

* 软件可移植层；  
* 更适合国内工艺/供应链条件的架构；  
* 通过系统级优化弥补单点器件差距；  
* 本土存储、本土互连、本土整机集成。

因此，未来评估中国 AI 芯片竞争力，不能只看“单卡 benchmark”，而要看**可用栈的成熟度**。

---

# **十一、供电、液冷与 time-to-power：AI 工厂的终极边界开始暴露**

## **11.1 为什么说 power 是“第二 HBM”**

TrendForce 的数据已经足够说明问题：2026 年 AI 服务器将消耗 55GW 电力、同比增长 74%，占全服务器总电力容量的 52%；超过 50% 的 AI 服务器热管理将使用液冷。\[M01\]  
Microsoft 单季度新增近 1GW 容量，说明 hyperscaler 已经在用极其激进的建设速度扩张基础设施。\[P06\]  
NVIDIA 也把 DSX Max-Q 和 DSX Flex 当作 Rubin 平台的重要组成，甚至强调在固定供电的数据中心里多塞 30% AI 基础设施，以及把 AI 工厂变成更灵活的电网资产。\[P01\]

这些都说明一个现实：  
**AI 硬件的上限，越来越不是由“能不能设计出来”决定，而是由“有没有电、能不能冷却、多久能建成”决定。**

## **11.2 供电瓶颈为何会深刻改变硬件路线**

当电力成为关键变量时，芯片设计与系统采购逻辑会同时改变：

### **设计侧**

* 更关注 tokens per watt 而非峰值 TOPS/FLOPS；  
* 更重视按 workload 动态调度的系统；  
* 更重视 prefill/decode 分拆；  
* 更重视光互连与低功耗内存体系；  
* 更重视 CPU/GPU/ASIC 混合部署。

### **采购侧**

* 更倾向整 rack / POD / turnkey delivery；  
* 更早锁定冷却、电力分配、变压器与施工资源；  
* 更看重 time-to-power 而不是单卡发布日；  
* 更愿意采用自研 ASIC 与混合架构来降低单位功耗成本。

## **11.3 我对供电主线的判断**

未来 12 个月，AI 基础设施里最容易被资本市场低估的不是某颗芯片，而是：

* 液冷系统；  
* 高压直流与配电；  
* 数据中心级 power management 软件；  
* 能源接入、微电网与储能协同；  
* “在给定电力预算下如何提升 AI 有效输出”的系统级设计。

从这个角度看，AI 硬件产业已经开始和能源基础设施产业部分融合。  
这也是为什么我认为未来“AI 工厂”会成为比“AI 服务器”更准确的产业语言。

---

# **十二、现在最值得关注的八个“新瓶颈”**

下面这部分是这份报告最重要的实战段落。  
如果你想判断未来 6—18 个月谁会胜出，重点不是看谁发布会最热闹，而是看谁能跨过下面这八个瓶颈。

## **12.1 瓶颈一：HBM 供给与长期绑定**

**严重程度：极高**  
**时间跨度：现在到 2027 年大概率持续**  
**领先指标：HBM4 design win、长期合约、价格、封装与测试扩产节奏**

HBM 已经不是一项部件采购问题，而是系统资格问题。  
有 HBM 配额的人，才有可能真正拿到 AI 系统出货资格。  
没有 HBM 配额，即便算力 die 做出来，也可能因为内存与封装无法匹配而失去商机。

## **12.2 瓶颈二：先进封装与 CoWoS / bonding / OSAT 能力**

**严重程度：极高**  
**时间跨度：2026—2027 持续**  
**领先指标：TSMC CoWoS / 3DFabric 扩产、ASE 投资、设备订单、hybrid bonding 采用进度**

先进封装已经从支持层变成主导层。  
谁掌握封装，谁掌握 AI 系统真正的出货速度。

## **12.3 瓶颈三：光互连相关器件与高端 PCB / 基板**

**严重程度：高**  
**时间跨度：2026 年开始显性化**  
**领先指标：光 DSP、激光器、模块、PCB lead time、CPO / OCS 验证进度**

Broadcom 公开提到激光器和 PCB 交期拉长，说明互连扩容已不只是交换芯片问题，而是整个光电链条联动问题。\[R02\]

## **12.4 瓶颈四：供电、液冷与站点建设**

**严重程度：极高**  
**时间跨度：2026—2028 都会是核心问题**  
**领先指标：数据中心 MW/GW 级扩建、变压器/液冷订单、site commissioning 进度**

未来很多 AI 集群的延迟，不会发生在 tape-out，而会发生在电力接入和冷却落地。

## **12.5 瓶颈五：推理内存墙与 KV cache 成本**

**严重程度：高**  
**时间跨度：随着 context window 增长而更严重**  
**领先指标：CXL 部署、KV cache 存储层方案、decode 专用芯片采用、SOCAMM 等新形态落地**

谁能更便宜地管理长上下文和 agent memory，谁会吃到推理市场的大头。

## **12.6 瓶颈六：软件可移植性**

**严重程度：高**  
**时间跨度：长期**  
**领先指标：框架支持、编译器成熟度、客户迁移案例、模型适配速度**

Huawei 950PR 被大客户更积极测试，背后关键变量之一就是更容易从 CUDA 迁移。\[R03\]  
所以软件不是配套，而是市场进入门槛。

## **12.7 瓶颈七：系统级编排能力**

**严重程度：中高**  
**时间跨度：agentic AI 扩张后快速提升**  
**领先指标：CPU 需求、调度软件、训练/推理混部效率、资源池化能力**

当 AI 进入多阶段、多模型、多工具调用场景，系统编排能力会成为效率决定项。

## **12.8 瓶颈八：政策与供应链地缘化**

**严重程度：高**  
**时间跨度：长期**  
**领先指标：出口管制、新法案、设备可得性、客户区域化采购策略**

地缘限制不是背景噪音，而是供给结构的一部分。  
尤其对中国市场，它会直接重塑芯片架构、软件层和客户采购逻辑。

---

# **十三、正在形成的六大新机会**

如果上面讲的是“约束条件”，那么下面讲的是“价值外溢”。

## **13.1 机会一：自研 ASIC 与 semi-custom 平台服务**

Broadcom、Marvell、Arm 的共同方向说明，未来最值钱的不只是“做一颗自有芯片”，而是提供能够快速贴合客户 workload 的半定制平台。  
原因很简单：  
真正有海量 AI 需求的公司，不满足于标准货；  
但也不是每家都愿意从零做芯片。  
这就给“平台化定制”留下巨大空间。

## **13.2 机会二：推理专用架构**

包括但不限于：

* decode 加速器；  
* SRAM-dominant 架构；  
* near-memory inference；  
* 更适合 agent / coding / long context 的专用系统。

这类公司未必会取代 GPU，但只要能接住推理成本优化这一刀，就有机会成为 AI 基础设施中的独立层。

## **13.3 机会三：HBM 之外的内存分层与扩展**

HBM4 会继续涨，但不是所有问题都该用 HBM4 解决。  
CXL、SOCAMM、KV cache 存储层、内存池化、近存算，都会成为下一轮创新焦点。  
因为真正有竞争力的系统，不是“全都最贵”，而是“把贵资源用在最该用的地方”。

## **13.4 机会四：先进封装与相关材料/设备**

过去“封装受益”是一个很宽泛的说法。  
现在要具体到：

* interposer / substrate；  
* bonding；  
* TSV；  
* 测试；  
* 热管理材料；  
* 更大封装尺寸相关设备；  
* 与 HBM / chiplet 适配的流程优化。

这个环节未来会持续被重新估值。

## **13.5 机会五：光互连与数据中心互联升级**

Broadcom、Marvell、NVIDIA、Google 都在指向同一个方向：  
未来 AI 集群不能没有更高阶光互连。  
所以从 1.6T / 3.2T 模块、光 DSP、激光器，到 OCS/CPO，都是持续追踪的重点。

## **13.6 机会六：电力、液冷、机柜级系统集成**

这是很多半导体投资者最容易忽略的机会。  
当 AI 产业进入“固定电力预算下追求更多有效 token”的阶段，  
那些能解决 **功率分配、液冷、机柜集成、site-level deployment** 的公司，可能比某些二线芯片公司更容易拿到超额收益。

---

# **十四、接下来 6—18 个月的核心预测**

下面这部分属于**推演判断**，不是已发生事实。我会尽量把每条预测都建立在前述已确认材料之上。

## **14.1 预测一：未来主流 AI 产品不会再按“单卡”采购，而会按 rack / POD / system 采购**

依据：NVIDIA Rubin 平台就是按 rack / AI factory 定义；Google Ironwood 是 Pod 级；微软、AWS 也都强调 fleet / rack / cloud service，而不是单芯片。\[P01\]\[P03\]\[P06\]\[P04\]  
判断：**到 2026 年下半年，采购语言会更系统化。**  
投资上，真正有议价权的公司也会从单点器件向整系统交付公司倾斜。

## **14.2 预测二：2026 年下半年到 2027 年，Blackwell 仍会是更广泛出货平台，但 Rubin 代表未来系统方向**

TrendForce 已提示，由于地缘与供应链因素，Rubin 在高端 GPU 出货中的占比会低于一些乐观预期，而 Blackwell 的占比会上升。\[M03\]  
我的判断是：

* **Blackwell / GB300 会是大规模商业出货主力；**  
* **Rubin 会是方向定义者和下一代设计基线。**

也就是说，市场短期收入可能更多兑现于 Blackwell，但产业路线图会越来越向 Rubin 的“七芯片系统”靠拢。

## **14.3 预测三：HBM 紧缺至少持续到 2027 年，且会强化长期合同化**

依据：Samsung 主推 3—5 年合约；Micron 说 DRAM/NAND 供应不足；Counterpoint、TechInsights 都强调 HBM / DRAM 供给缺口长期化。\[R06\]\[P07\]\[M06\]\[M09\]  
判断：**HBM 会从高景气周期商品，变成中期战略配额资源。**

## **14.4 预测四：推理市场会快速异构化，且“prefill / decode 分治”会扩散**

依据：NVIDIA \+ Groq、AWS \+ Cerebras、TechInsights 对 decode bottleneck 的分析、Omdia 对 LPX/LPU 的判断。\[R10\]\[R13\]\[M10\]\[M11\]\[M12\]  
判断：  
未来推理最有竞争力的方案，不会是“一种芯片跑所有阶段”，而会是“按阶段、按上下文、按延迟和功耗要求拆分”。

## **14.5 预测五：CPU 在 AI 数据中心中的战略地位将继续提升**

依据：NVIDIA Vera CPU rack、Arm AGI CPU、微软强调 CPU side progress、agentic AI 带来 coordination/data movement 需求。\[P01\]\[P16\]\[P06\]  
判断：  
市场会逐渐意识到 AI 时代的 CPU 不是退场，而是在重新定位。

## **14.6 预测六：先进封装的战略权重会在市场上超过前道工艺“纯节点新闻”**

依据：TSMC、ASML、ASE、Besi、Applied 都在强化封装和 bonding。\[P10\]\[R08\]\[P17\]\[R09\]\[P18\]\[P19\]  
判断：  
未来一年，任何只谈节点不谈封装的 AI 芯片分析，都会明显失真。

## **14.7 预测七：中国市场会更快转向“可用替代栈”而不是“最佳单点性能”**

依据：Huawei 950PR 的兼容性改善、DeepSeek/Huawei、国内客户测试与下单、TrendForce 对 Ascend 后续路线的跟踪。\[R03\]\[R04\]\[M02\]  
判断：  
中国 AI 硬件生态会越来越围绕“迁移成本最低 \+ 供应最稳定 \+ 整体栈最可用”的原则来演进。

## **14.8 预测八：电力与液冷会成为未来 12 个月 AI 基础设施项目最常见的延误源**

依据：TrendForce 电力数据、微软近 1GW 扩建、NVIDIA DSX、Reuters 对 power / labor / turbine / transformer 约束的报道。\[M01\]\[P06\]\[P01\]\[R23\]\[R24\]  
判断：  
“有钱买不到足够快上线的 AI 产能”会成为很多公司 2026 年下半年的真实痛点。

## **14.9 预测九：光互连将在 2026 年完成更多设计绑定，并在 2027 年迎来更实质的放量节点**

依据：Broadcom 400G/lane、Marvell OCS、Google OCS、NVIDIA photonics、The Next Platform 对 photonic fabric 的持续关注。\[P12\]\[P13\]\[P03\]\[P01\]\[M18\]  
判断：  
2026 是验证和 design-in 年，2027 才更可能是商业放量加速年。

## **14.10 预测十：AI 硬件的价值分配会更加分散，但龙头平台效应不会立刻瓦解**

依据：GPU 仍具生态和系统集成优势，但自研 ASIC、HBM、封装、互连、电力都在独立增值。\[P01\]\[P02\]\[P03\]\[P04\]\[P07\]\[P10\]\[P12\]  
判断：  
未来一年，市场结构更像“多层受益、多层瓶颈”，而不是“一家公司吃掉全部超额收益”。  
但只要龙头继续主导系统整合，它仍然可能在总价值捕获上维持第一。

---

# **十五、如果只盯住一个变量，你最容易看错什么**

这一段专门写给需要做产业判断的人。

## **15.1 只盯 GPU，会低估 HBM 和封装**

你会看到一堆芯片发布，却看不到为什么真正能大规模交付的系统很少。  
因为不是所有算力 die 都能变成量产机柜。

## **15.2 只盯 HBM，会低估推理架构变化**

你会把所有未来增长都线性外推到 HBM 上，但实际上 decode 阶段可能出现 HBM-free 或 HBM-light 路线。  
HBM 仍会很强，但它不是唯一答案。

## **15.3 只盯 ASIC，会低估软件生态与灵活性**

很多 ASIC 的理论效率很高，但客户真正用不用，取决于迁移成本、编译器、框架支持、运维复杂度。  
软件摩擦有时比晶体管更重要。

## **15.4 只盯训练，会低估推理分层**

未来很多商业价值来自推理，尤其是 agent、coding、search、enterprise workflow。  
而推理的最优硬件结构，未必和训练一致。

## **15.5 只盯芯片，会低估电力与 time-to-power**

未来一年，很多 AI 订单的真实节拍，不在 tape-out，而在 site readiness。

---

# **十六、对不同参与者的建议**

## **16.1 对芯片设计公司**

不要只做“更像 NVIDIA 的 GPU”。  
更现实的机会在：

* 推理专用阶段优化；  
* 内存扩展与池化；  
* 与某个 hyperscaler 或大模型厂深度共设计；  
* 在软件迁移层做最小摩擦方案；  
* 把芯片、板卡、机柜与系统软件一起卖。

## **16.2 对内存与封装企业**

未来最值钱的不只是扩产，而是：

* 和客户一起做 roadmap 锁定；  
* 提前绑定下一代封装与 bonding 工艺；  
* 把供货从“部件交付”升级到“系统适配交付”。

## **16.3 对云厂商**

继续扩大混合舰队是最优解：

* 标准 GPU 保持灵活性；  
* 自研 ASIC 降成本、提 supply control；  
* 在推理侧引入更细粒度异构；  
* 强化 power-aware scheduling 与 rack-level 设计。

## **16.4 对中国厂商**

最核心的不是先去追“峰值参数”，而是先做：

* 更低迁移摩擦的软件栈；  
* 更稳定的供应交付；  
* 与模型厂的联合优化；  
* 更适配国内供电、机柜和算力预算的整机系统。

## **16.5 对投资与战略团队**

未来一年最应该看的是：

1. HBM 合同与供货节奏  
2. CoWoS / OSAT / bonding 产能  
3. 光互连 design-in  
4. 电力与液冷项目落地  
5. Hyperscaler 自研芯片上线范围  
6. 推理系统是否开始从“单平台”变“多层异构”

---

# **十七、未来 90 天最值得追踪的观察点**

1. Rubin / GB300 的真实出货与客户部署节奏  
2. HBM4 / HBM4E 的 design win 和量产坡度  
3. Samsung / SK hynix / Micron 的长期协议与扩产口径  
4. Google TPU 与外部客户绑定的更多证据  
5. AWS Trainium3 生产级工作负载是否增多  
6. Microsoft Maia 200 的更多商业化场景  
7. Arm AGI CPU 客户名单与 tape-out / 量产进度  
8. Huawei 950PR 的真正大规模交付情况  
9. CXL 与 OCS 是否从“发布会概念”进入更实际的采购与部署  
10. 数据中心 power / cooling 项目是否成为新的交付瓶颈

---

# **十八、最后的总判断：AI 硬件产业已经跨过拐点**

如果让我对未来一年给出一句最浓缩的结论，我会写成这样：

**AI 硬件产业已经从“以 GPU 为核心的加速器时代”，进入“以内存、封装、互连、供电和软件协同为核心的系统时代”。**

GPU 依然重要，甚至可能仍然是最大单点赢家；  
但未来真正定义行业格局的，不再是“谁有更强 GPU”，而是：

* 谁能拿到足够 HBM；  
* 谁能把先进封装变成稳定产能；  
* 谁能在推理时代有效管理 memory wall；  
* 谁能在给定电力预算内交付更多有效 token；  
* 谁能在软件生态层面把客户迁移摩擦压到最低；  
* 谁能把这些东西整成一个可交付的 AI 工厂。

也因此，未来 12—18 个月半导体产业最重要的新瓶颈，不是“没有新芯片”，而是**系统复杂度急剧上升后，产业链每一层都开始变成上限约束**。  
与之对应，最大的机会也不是“下注下一颗明星芯片”，而是**下注那些正在成为 AI 工厂必需层的环节**。

* 

