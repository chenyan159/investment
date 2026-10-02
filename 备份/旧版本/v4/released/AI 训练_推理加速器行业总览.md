截至 **2026-04-24**，下面按“数据中心 AI 训练/推理加速器”为主口径整理；AI PC、手机、车载、机器人端侧 NPU 也列入全景，但不放进 12 大数据中心芯片技术深表。

**“产能释放量（美元）”口径**：不是云服务收入，也不等于厂商确认营收；我按“可被数据中心部署的加速器硬件等效价值”估算，含 GPU/ASIC/XPU 模组、HBM、先进封装、必要的板卡/机架级互联与液冷份额。云厂商自研 TPU/Trainium/MTIA/Maia 这类不对外销售的芯片，按“可替代的同等算力硬件价值 \+ 自研系统 BOM 溢价”估算。低置信度项标注为“推测/未检验”。

## **1\. 总体判断**

2026 年还是 **Blackwell / Blackwell Ultra、AWS Trainium2/3、Google TPU Ironwood/TPU 8、华为 Ascend 910C/950、AMD MI350/MI450 初期** 的共同放量年；2027 年会更明显切到 **NVIDIA Rubin、AMD Helios/MI450、TPU 8、Trainium3/4、Meta MTIA 450/500、华为 Ascend 960**。NVIDIA 仍是最大供给方：其 FY2026 数据中心收入为 **1937 亿美元**，并给出 FY2027 Q1 **780 亿美元**收入展望；NVIDIA 在 GTC 2026 上还称 2025–2027 年至少看见 **1 万亿美元**收入机会。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026))

供应链瓶颈不是单一晶圆，而是 **HBM、CoWoS/先进封装、ABF/高层基板、光模块/PCB、液冷与供电** 叠加。TSMC 2026 年资本开支被上调到 **520–560 亿美元**高端区间，并称 AI 相关 3nm/先进产能仍紧；ASE 预计先进封装业务 2026 年翻倍；SK hynix 称未来 3 年客户需求超过其 HBM 产能，且 2026 年 HBM 基本售罄。([Reuters](https://www.reuters.com/world/asia-pacific/tsmc-set-post-50-quarterly-profit-jump-extend-record-earnings-on-insatiable-ai-2026-04-16/))

### **全球 AI 芯片/加速器产能释放量预测**

| 口径 | 2026 年预测区间 | 2027 年预测区间 | 交叉验证 |
| ----- | ----- | ----- | ----- |
| 数据中心 AI 加速器“可部署硬件价值” | **5200–8500 亿美元** | **8500 亿–1.55 万亿美元** | NVIDIA 自身 FY2026 数据中心收入已接近 2000 亿美元，FY2027 Q1 指引年化超过 3000 亿美元；Broadcom AI 半导体收入 Q1 FY2026 为 84 亿美元、Q2 指引 107 亿美元，且 Reuters 报道其 2027 AI 芯片收入展望可超 1000 亿美元。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026)) |
| 只算“芯片/封装模组”半导体价值，不含完整机架、存储、供电、土建 | **3000–5700 亿美元** | **5200 亿–1.05 万亿美元** | HBM3E/HBM4、CoWoS、晶圆与先进封装是主限制；Samsung 已宣布 HBM4 商业量产，AMD 也确认 Samsung HBM4 将供给 MI455X/Helios。([Samsung Semiconductor Global](https://semiconductor.samsung.com/news-events/news/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing/)) |
| 端侧 AI SoC/NPU：手机、AI PC、车载、机器人 | **450–900 亿美元** | **600–1300 亿美元** | 单价远低于数据中心 GPU/ASIC，但出货量大；例如 Apple M4 Neural Engine 38 TOPS，Intel Lunar Lake NPU 最高 48 TOPS，NVIDIA Jetson Thor 最高 2070 FP4 TFLOPS、128GB 内存。([Apple](https://www.apple.com/newsroom/2024/05/apple-introduces-m4-chip/)) |

---

## **2\. 全行业 AI 芯片全景：当前代、下一代、设计中**

表内金额为“该芯片/平台对应的年度产能释放价值”，同一生态内部分范围有替代关系，不应机械相加。

| 公司/生态 | 芯片/平台 | 类型 | 2026-04 阶段 | 2026 产能释放 | 2027 产能释放 | 依据与置信度 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| NVIDIA | H100/H200/H20、Hopper 尾部 | GPU | 大规模存量；H20 受出口政策与中国替代影响 | 150–350 亿美元 | 30–150 亿美元 | 存量与兼容生态仍强；但主供给转 Blackwell。中 |
| NVIDIA | **B200 / GB200 Blackwell** | GPU/Grace-GPU 超芯片 | 大规模量产 | 900–1500 亿美元 | 400–900 亿美元 | Blackwell 为 TSMC 4NP，两颗近光罩极限 die，以 10TB/s chip-to-chip 互联；NVIDIA 称 Blackwell 已 full production。([NVIDIA](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/)) 高 |
| NVIDIA | **B300 / GB300 Blackwell Ultra** | GPU/机架级 NVL72 | 大规模量产/可购 | 1400–2400 亿美元 | 700–1400 亿美元 | DGX B300 已 available now；B300 288GB HBM3e+、8TB/s 带宽，GB300 NVL72 为 72 GPU \+ NVLink fabric。([NVIDIA](https://www.nvidia.com/en-us/data-center/dgx-b300/)) 高 |
| NVIDIA | **Vera Rubin / Rubin GPU / Rubin NVL72** | 下一代 GPU \+ CPU \+ 网络 | 初期生产/部署，2026 roll-out | 200–700 亿美元 | 2200–4200 亿美元 | Rubin GPU 官方规格：50 PFLOPS NVFP4 inference、22TB/s HBM4、3.6TB/s NVLink/GPU、336B 晶体管；平台含 36 Vera CPU \+ 72 Rubin GPU。([NVIDIA](https://www.nvidia.com/en-us/data-center/technologies/rubin/)) 高 |
| NVIDIA | Rubin Ultra / Feynman | 下一代/后下一代 | Rubin Ultra 2027 下半年推测；Feynman 2028 | 0–50 亿美元 | 400–1300 亿美元 | Rubin Ultra 公开细节少，多为路线图与供应链推测；Feynman 官方仅称为 Rubin 之后架构，含 Rosa CPU、LP40、CPO/光互联方向。([NVIDIA Blog](https://blogs.nvidia.com/blog/gtc-2026-news/)) 中/低 |
| NVIDIA \+ Groq | **Groq 3 LPX / LPU** | 低延迟推理 LPU | 2026 下半年可用 | 10–60 亿美元 | 100–350 亿美元 | 每 rack 256 个 LPU、128GB SRAM、12TB DDR5、40PB/s SRAM 带宽、640TB/s scale-up。([NVIDIA](https://www.nvidia.com/en-us/data-center/lpx/)) 中 |
| AMD | MI300X / MI325X | GPU | 量产尾部 | 20–80 亿美元 | 10–50 亿美元 | 被 MI350/MI450 替代。中 |
| AMD | **MI350X / MI355X** | GPU | 量产放量 | 150–350 亿美元 | 80–250 亿美元 | CDNA4；288GB HBM3E、8TB/s；最高 4x 代际 AI compute、35x inference。([AMD](https://www.amd.com/en/blogs/2025/amd-instinct-mi350-series-and-beyond-accelerating-the-future-of-ai-and-hpc.html)) 高 |
| AMD | MI430X | HPC/AI GPU | 超算专项、小规模 | 10–50 亿美元 | 50–150 亿美元 | 432GB HBM4、19.6TB/s，面向 Alice Recoque 超算。([AMD](https://www.amd.com/en/newsroom/press-releases/2025-11-18-amd-and-eviden-to-power-europe-s-new-exascale-supe.html)) 中 |
| AMD | **MI450 / MI455X / Helios** | 下一代 rack-scale GPU | 2026 H2 客户启动 | 80–250 亿美元 | 600–1500 亿美元 | Helios：72 GPU/rack、432GB HBM4/GPU、19.6TB/s；Oracle 首批 5 万颗 2026 Q3 起，Meta 与 AMD 达成 6GW，多代部署，首个 1GW 2026 H2 启动。([AMD](https://www.amd.com/en/blogs/2025/amd-helios-ai-rack-built-on-metas-2025-ocp-design.html)) 高 |
| Intel | Gaudi 3 | AI 加速器 | 小规模量产 | 5–40 亿美元 | 2–20 亿美元 | Gaudi 3 PCIe 已 shipping，采用标准 Ethernet；但份额小。([Intel](https://www.intel.com/content/www/us/en/products/details/processors/ai-accelerators/gaudi.html)) 中 |
| Intel | Crescent Island / Jaguar Shores | 推理 GPU / 未来 rack AI | Crescent Island 2026 H2 sampling；Jaguar Shores 2027+ | 0–10 亿美元 | 10–100 亿美元 | Crescent Island 被报道为 160GB LPDDR5X 推理卡；Jaguar Shores 仍为 reported/未充分公开，可能用 HBM4 与硅光互联。([Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/intel-chip-roadmap-2026-2028)) 低 |
| Google \+ Broadcom | TPU v6e / v5p 尾部 | ASIC | 量产尾部 | 40–120 亿美元 | 10–50 亿美元 | 被 Ironwood/TPU 8 替代。中 |
| Google \+ Broadcom | **TPU v7 Ironwood / TPU7x** | ASIC | GA/大规模部署 | 250–600 亿美元 | 200–700 亿美元 | Ironwood 最高 9216 liquid-cooled chips/pod；TPU7x 单芯 192GiB HBM、7380GiB/s、FP8 4614 TFLOPS。([blog.google](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/ironwood-tpu-age-of-inference/)) 高 |
| Google \+ Broadcom | **TPU 8i / TPU 8t** | ASIC | 2026 发布，soon/ramp | 80–350 亿美元 | 700–1700 亿美元 | TPU 8t：216GB HBM、128MB SRAM、12.6 PFLOPS FP4；TPU 8i：288GB HBM、384MB SRAM、10.1 PFLOPS FP4。([blog.google](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/tpus-8t-8i-cloud-next/)) 高 |
| Broadcom \+ Google | 下一代 TPU/机架 ASIC | Custom ASIC | 设计/长期供给协议 | 0–50 亿美元 | 150–600 亿美元 | Broadcom 与 Google 签至 2031 的长期供给协议；Anthropic 2027 起约 3.5GW Google TPU 容量。([Reuters](https://www.reuters.com/business/broadcom-signs-long-term-deal-develop-googles-custom-ai-chips-2026-04-06/)) 中 |
| AWS | **Trainium2** | ASIC | 大规模量产 | 250–700 亿美元 | 150–450 亿美元 | Project Rainier 近 50 万 Trainium2；Anthropic 已用超 100 万颗 Trainium2，2026 年底 Trainium2/3 近 1GW。([Amazon News](https://www.aboutamazon.com/news/aws/aws-project-rainier-ai-trainium-chips-compute-cluster)) 高 |
| AWS | **Trainium3** | 3nm ASIC | GA，2026 放量 | 150–600 亿美元 | 700–1600 亿美元 | Trainium3 为 AWS 首款 3nm AI 芯片，144GB HBM3e、4.9TB/s、2.52 PFLOPS FP8；144 chips/UltraServer。([Amazon Web Services, Inc.](https://aws.amazon.com/ai/machine-learning/trainium/)) 高 |
| AWS | Trainium4 | 下一代 ASIC | 设计中 | 0 | 50–450 亿美元 | AWS 称 Trainium4 至少 6x FP4、3x FP8、4x memory bandwidth。([Amazon News](https://www.aboutamazon.com/news/aws/trainium-3-ultraserver-faster-ai-training-lower-cost)) 中 |
| Microsoft | Maia 100 | ASIC | 小规模部署 | 10–40 亿美元 | 0–20 亿美元 | 第一代，内部使用。([Microsoft Azure](https://azure.microsoft.com/en-us/blog/azure-maia-for-the-era-of-ai-from-silicon-to-software-to-systems/)) 中 |
| Microsoft | **Maia 200** | 3nm ASIC | 早期部署 | 30–150 亿美元 | 150–500 亿美元 | TSMC 3nm、216GB HBM3e、7TB/s、272MB SRAM、\>10 PFLOPS FP4、750W，部署于 US Central 等区域。([The Official Microsoft Blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)) 高 |
| Meta \+ Broadcom | MTIA 300 | ASIC | 生产/推荐训练 | 30–120 亿美元 | 50–200 亿美元 | Meta 称 MTIA 300 用于 ranking/recommendation training，已有数十万 MTIA 部署推理。([About Facebook](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)) 中 |
| Meta \+ Broadcom | **MTIA 400 / 450 / 500** | GenAI 推理 ASIC | 2026–2027 切入 | 10–100 亿美元 | 250–900 亿美元 | Meta 称未来两年四代 MTIA；Broadcom 合作，初始 commitment 超 1GW；泄露/媒体规格称 MTIA 400/450 为 288GB HBM，500 到 384–512GB HBM。([About Facebook](https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/)) 中 |
| Broadcom \+ OpenAI | OpenAI 自研 AI ASIC | Custom ASIC | 设计/流片前后；2027 初放量 | 0–30 亿美元 | 250–1000 亿美元 | Reuters 报道 OpenAI 正与 Broadcom 做自研 AI 芯片，且 AMD/OpenAI 交易文本中也提到 OpenAI 自研硅片计划；Broadcom 2027 AI 收入展望超 1000 亿美元。([Reuters](https://www.reuters.com/business/amd-signs-ai-chip-supply-deal-with-openai-gives-it-option-take-10-stake-2025-10-06/)) 中 |
| Qualcomm | Cloud AI 100 Ultra / AI200 / AI250 | 推理 NPU/卡/机架 | AI100 已商用；AI200 2026；AI250 2027 | 10–70 亿美元 | 50–300 亿美元 | AI200 每卡 768GB LPDDR、160kW/rack、DLC；AI250 early 2027，近存计算，\>10x effective bandwidth。([Qualcomm](https://www.qualcomm.com/artificial-intelligence/data-center)) 中 |
| 华为 | Ascend 910B / 910C | AI 加速器 | 910C 量产/出货 | 80–250 亿美元 | 30–150 亿美元 | Reuters 称 910C 由两个 910B 级处理器组合，性能接近 H100，2025 起出货。([Reuters](https://www.reuters.com/world/china/huawei-readies-new-ai-chip-mass-shipment-china-seeks-nvidia-alternatives-sources-2025-04-21/)) 中 |
| 华为 | **Ascend 950PR / 950DT \+ Atlas 950** | 下一代国产 AI 加速器 | 样品/量产启动 | 150–450 亿美元 | 450–1100 亿美元 | Reuters 称 950PR 计划 2026 年约 75 万颗，样品已给 ByteDance/Alibaba，2026 H2 大量出货；950DT/Atlas 950 SuperPod 2026 Q4。([Reuters](https://www.reuters.com/world/china/huaweis-new-ai-chip-find-favour-with-bytedance-alibaba-which-plan-place-orders-2026-03-27/)) 中 |
| 华为 | Ascend 960 / 970 \+ Atlas 960 | 下一代/后下一代 | 设计 | 0–30 亿美元 | 80–400 亿美元 | 路线图：960 在 2027，970 在 2028；Atlas 960 Q4 2027。([Reuters](https://www.reuters.com/business/media-telecom/chinas-huawei-hypes-up-chip-computing-power-plans-fresh-challenge-nvidia-2025-09-18/)) 中/低 |
| 阿里 T-Head | Zhenwu 810E；XuanTie C950 | AI 加速器/服务器 CPU | 810E 大规模；C950 设计/发布 | 70–200 亿美元 | 120–350 亿美元 | TrendForce 称 T-Head 芯片截至 2026-02 已交付 47 万颗、年化收入超 100 亿元人民币；Reuters 称 C950 为 5nm RISC-V server chip，面向 agentic AI。([TrendForce](https://www.trendforce.com/news/2026/03/20/news-alibabas-t-head-reportedly-hits-470k-chip-shipments-expands-amid-unclear-ipo-timeline/)) 中 |
| 百度 Kunlunxin | P800 / 下一代 | AI 加速器 | 量产部署 | 30–120 亿美元 | 80–250 亿美元 | Reuters 称 Kunlunxin 获中国移动超 10 亿元订单，百度有 3 万颗 P800 集群用于训练。([Reuters](https://www.reuters.com/technology/baidu-chip-design-unit-kunlunxin-wins-over-139-million-orders-china-mobile-2025-08-22/)) 中 |
| 寒武纪 | Siyuan 590 / 690 | AI 加速器 | 扩大量产 | 40–150 亿美元 | 80–300 亿美元 | 多家媒体/供应链称 2026 目标约 50 万颗，其中 590/690 约 30 万颗；信息未完全验证。([TrendForce](https://www.trendforce.com/news/2025/12/15/insights-cambricon-remains-chinas-top-ai-chip-startup-rumored-2026-triple-output-faces-smic-limits/)) 低/中 |
| 字节跳动 | SeedChip | 推理 ASIC | sampling/设计 | 10–80 亿美元 | 50–250 亿美元 | Reuters 称字节 2026 目标至少 10 万颗推理芯片，后续增至 35 万颗，与 Samsung 接触。([Reuters](https://www.reuters.com/world/asia-pacific/bytedance-developing-ai-chip-manufacturing-talks-with-samsung-sources-say-2026-02-11/)) 中 |
| 其他中国厂商 | 海光 DCU、壁仞、沐曦、燧原 S60、天数智芯、摩尔线程等 | GPU/ASIC | 小中规模量产/国产替代 | 30–150 亿美元 | 80–350 亿美元 | 2025 年中国 AI accelerator server 市场约 400 万张卡，国产约 165 万张；华为、T-Head、昆仑芯、寒武纪领先。([Reuters](https://www.reuters.com/world/china/chinese-chipmakers-claim-nearly-half-of-local-market-nvidias-lead-shrinks-idc-2026-04-01/)) 中 |
| Cerebras | WSE-3 / CS-3 | 晶圆级 AI | 小规模生产/超大推理训练 | 10–80 亿美元 | 40–300 亿美元 | WSE-3：5nm、4 万亿晶体管、90 万核心、44GB 片上 SRAM、125PF；CS-3 已出货。([Cerebras](https://www.cerebras.ai/press-release/cerebras-announces-third-generation-wafer-scale-engine)) 中 |
| d-Matrix | Corsair | SRAM/DIMC 推理 ASIC | early production/sampling | 5–50 亿美元 | 30–200 亿美元 | Corsair 双卡：4GB performance memory、300TB/s、最高 19.2PF MXINT4；rack 可到 128GB performance memory、9.6PB/s。([d-Matrix](https://www.d-matrix.ai/product/)) 中 |
| Etched | Sohu | Transformer 专用 ASIC | 设计/试产 | 0–30 亿美元 | 20–200 亿美元 | Sohu 为 TSMC 4nm transformer ASIC，宣称单服务器替代 160 H100；未大规模验证。([TechCrunch](https://techcrunch.com/2024/06/25/etched-is-building-an-ai-chip-that-only-runs-transformer-models/)) 低 |
| Tenstorrent / SambaNova / Qualcomm AI100 | Blackhole/Galaxy、SN40L、Cloud AI100 | 推理/开发/边缘数据中心 | 小规模商用 | 5–40 亿美元 | 20–150 亿美元 | Tenstorrent Blackhole 120 Tensix cores、32GB GDDR6；Galaxy 32 颗 Blackhole；SambaNova SN40L 为 SRAM+HBM+DDR 三层内存；Qualcomm AI100 Ultra 150W、128GB LPDDR。([Tenstorrent Documentation](https://docs.tenstorrent.com/aibs/blackhole/specifications.html)) 中/低 |
| Tesla / xAI / SpaceX | AI5 / AI6 / Dojo / Terafab | 车载/机器人/未来训练 | AI5 流片；Terafab 规划 | 0–30 亿美元 | 30–200 亿美元 | Reuters 称 Tesla 计划在 Terafab 使用 Intel 14A，细节与时间线仍不清；近期主要是车载和机器人，不是主流云训练芯片。([Reuters](https://www.reuters.com/business/autos-transportation/tesla-ceo-musk-says-company-plans-use-intels-14a-process-terafab-2026-04-22/)) 低/中 |

---

## **3\. 多角度校验这些美元预测**

| 校验角度 | 看到的信号 | 对预测的约束 |
| ----- | ----- | ----- |
| 厂商营收 | NVIDIA FY2026 数据中心 1937 亿美元，FY2027 Q1 指引 780 亿美元，年化接近/超过 3000 亿美元；Broadcom FY2026 Q1 AI 收入 84 亿美元、Q2 指引 107 亿美元，2027 AI 芯片收入被报道可超 1000 亿美元。([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026)) | 仅 NVIDIA \+ Broadcom custom 就支撑 2026 年数千亿美元级别；2027 年若 Rubin、TPU/MTIA/OpenAI ASIC 成熟，1 万亿美元级别不是离谱上限。 |
| GW 级订单 | AWS/Anthropic 2026 年底 Trainium2/3 接近 1GW；AMD 与 Meta 达成最高 6GW，首个 1GW 从 2026 H2 开始；AMD/OpenAI 交易也从 2026 H2 的 1GW MI450 开始。([anthropic.com](https://www.anthropic.com/news/anthropic-amazon-compute)) | 1GW AI 硬件按 300–800 亿美元部署价值估算，单个 hyperscaler 多 GW 订单足以推高 2027 区间。 |
| HBM | Blackwell Ultra 288GB HBM3e+，MI350 288GB HBM3E，MI450 432GB HBM4，TPU 8i 288GB HBM，Maia 200 216GB HBM3e。HBM 是硬约束。([NVIDIA](https://www.nvidia.com/en-us/data-center/dgx-b300/)) | HBM 供给若偏紧，2026 高端区间会被压低；HBM4 在 2026 验证/量产顺利，2027 高端区间才成立。 |
| 封装/基板 | TSMC 称 CoWoS 可到 5.5-reticle size，2028 到 14-reticle；ASE 先进封装 2026 翻倍；Broadcom 称 TSMC 产能与 lasers/PCB 都是 2026 瓶颈。([TSMC](https://pr.tsmc.com/english/news/3302)) | 2026 年不可能无限放量，Rubin/MI450/TPU 8 的部分需求会顺延到 2027。 |
| 中国市场 | IDC/Reuters 称 2025 年中国 AI 加速卡约 400 万张，其中国内厂商约 165 万张；华为约 81.2 万、T-Head 约 26.5 万、昆仑芯和寒武纪各约 11.6 万。([Reuters](https://www.reuters.com/world/china/chinese-chipmakers-claim-nearly-half-of-local-market-nvidias-lead-shrinks-idc-2026-04-01/)) | 国产芯片“颗数”很大，但 ASP/系统价值低于 NVIDIA 高端 GPU；美元价值仍会显著增长。 |

---

## **4\. 2026–2027 年初预计放量最大的 12 类芯片：技术拆解**

下面 12 类按 **2026–2027 年初“等效美元出货价值 \+ 放量确定性”** 选出。若只按“颗数”，华为/阿里/寒武纪/Trainium/TPU 会更靠前，NVIDIA/AMD 高端 GPU 则按价值更靠前。

### **4.1 架构、工艺、存储、互联、散热**

| \# | 芯片/芯片族 | 光刻掩膜/制程 | AI 芯片外部存储 | AI 芯片内部存储 | 计算芯片基板/先进封装 | 光互联/光电共封装 | 芯片级供电与散热 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 1 | **NVIDIA GB200 / B200 Blackwell** | TSMC 4NP；两颗 reticle-limited die；掩膜数未公开，按 N4-class EUV 全掩膜套推测约 60–90 张（推测） | HBM3e，GB200/B200 级别通常 192GB 左右（公开 SKU 差异） | 大 L2/SRAM；第二代 Transformer Engine；NVFP4/FP4 路径 | CoWoS-L/2.5D interposer \+ 大 ABF 基板；双 GPU die 10TB/s chip-to-chip | 芯片内无 CPO；机架/集群用 NVLink、InfiniBand/Ethernet \+ 800G 光模块 | 48V rack → 板级多相 VRM/POL；液冷在 NVL 系统中成为主流；B200/B300 高电流电源完整细节未公开（推测） |
| 2 | **NVIDIA GB300 / B300 Blackwell Ultra** | TSMC 4NP；Blackwell Ultra 同工艺族（官方未给全部掩膜细节） | 288GB HBM3e+、8TB/s/GPU | 更强 FP4/attention；大 SRAM/L2 未完全公开 | 更大 CoWoS/ABF 载板压力；NVL72 级高密度机架 | NVLink Switch fabric；外部仍以可插拔 800G 光模块为主，CPO 未成为 GPU 包内默认 | GB300 NVL72 需要 DLC/冷板；供电为高电流 48V 机架级架构（推测） |
| 3 | **NVIDIA Rubin / Vera Rubin / Rubin Ultra** | 制程未正式公开；行业普遍推测 TSMC N3P/N2 转进，Rubin Ultra 可能更高阶（推测） | Rubin GPU 官方 22TB/s HBM4；Rubin Ultra 可能 HBM4E/更高堆叠（推测） | 336B 晶体管、224 SM、第五代 Tensor Cores；片上 SRAM 未公开 | 2.5D/多 die advanced packaging；Rubin Ultra 可能更多 chiplet（推测） | NVLink 6 3.6TB/s/GPU；NVIDIA GTC 2026 对后续 Feynman 提到 Kyber、CPO scale-up 与 optical scale-out | HBM4 与高功耗 GPU 使 direct liquid cooling 成默认；背面供电不是 2026 主流，可能 2028+（推测） |
| 4 | **AMD MI350X / MI355X** | 制程官方未明示，CDNA4；推测 TSMC N3/N4 \+ 先进封装（推测） | 288GB HBM3E、8TB/s，Samsung/Micron 供给 | CDNA4 矩阵核心；on-die cache/SRAM 未完全公开 | 2.5D chiplet \+ HBM；OAM/UBB；ABF \+ interposer | Infinity Fabric \+ Ethernet/NIC；无包内 CPO | 支持风冷与 direct liquid-cooled；高电流 VRM/POL |
| 5 | **AMD MI450 / MI455X / MI430X / Helios** | MI450 制程未完全公开，推测 TSMC 3nm-class；MI430/450 HBM4 | MI450/MI430：432GB HBM4、19.6TB/s | CDNA-next；片上 SRAM 未公开 | Helios 72 GPU/rack；OCP ORW；大 interposer/ABF；HBM4 base die 复杂 | UALink/UALoE、Ethernet；每 GPU 可配多 800G NIC；无确定包内 CPO | 160kW+ rack 级别推测；DLC/温水液冷；OCP rack 电源 |
| 6 | **Google TPU v7 Ironwood / TPU7x** | Google 未公开制程；Broadcom physical design \+ TSMC 代工可能性高（推测） | TPU7x：192GiB HBM，7380GiB/s | VMEM/SRAM；官方表列 VMEM SRAM | 自研 board/pod；液冷 pod，9216 chips/pod | ICI 互联；pod/数据中心网络含大规模光模块；CPO 未公开 | 液冷；9,216-chip pod 接近 10MW；供电/VRM 细节未公开 |
| 7 | **Google TPU 8i / TPU 8t** | 未公开；推测先进 TSMC/Broadcom ASIC 流程 | TPU 8t：216GB HBM；TPU 8i：288GB HBM | TPU 8t 128MB SRAM；TPU 8i 384MB SRAM | 机架/board 级 ASIC \+ HBM；具体封装未公开 | TPU 8t 3D Torus；TPU 8i Boardfly；Virgo Network 大规模连接 | 液冷概率高；AI 数据中心级 48V/高压配电（推测） |
| 8 | **AWS Trainium2** | 制程未公开；AWS/Annapurna 自研 ASIC | HBM，公开容量未如 T3 细；64 chips/UltraServer | NeuronCore \+ SRAM/片上缓存未全公开 | UltraServer；NeuronLinks scale-up；定制板卡 | EFA/以太网 scale-out；无 CPO | Trainium2 数据中心采用 AWS 自有机架/供电/液冷或高效风冷组合（推测） |
| 9 | **AWS Trainium3 / Trainium4** | Trainium3 官方称 AWS 首款 3nm AI chip；Trainium4 设计中 | Trainium3：144GB HBM3e、4.9TB/s；Trainium4 4x memory bandwidth | NeuronCore v3；片上 SRAM 未完全公开 | 144 chips/Trn3 UltraServer，20.7TB HBM3e，总 706TB/s memory bandwidth | UltraCluster 3.0 可到百万芯片；EFA/网络光模块；无 CPO | 5x output tokens/MW vs Trn2；电源/散热细节未公开，推测液冷占比上升 |
| 10 | **Meta MTIA 300 / 400 / 450 / 500** | Broadcom 设计协作，TSMC 代工；节点未公开，推测 N5/N3 过渡 | 泄露/媒体：MTIA400/450 288GB HBM；MTIA500 384–512GB HBM（未检验） | RISC-V 控制 \+ chiplet；片上 SRAM 未公开 | Broadcom advanced packaging \+ OCP rack；72 MTIA400 scale-up rack（媒体/推测） | Ethernet-first；Meta/Broadcom 强调 networking；CPO 未公开 | 初始 1GW commitment；液冷与 OCP power shelf 概率高（推测） |
| 11 | **华为 Ascend 910C / 950PR / 950DT** | 无法用 TSMC 先进节点；910C/950 推测 SMIC 7nm/N+2 类；掩膜/EUV 信息不公开（推测） | 950PR：HiBL 1.0 128GB、1.6TB/s；950DT：HiZQ2.0 144GB、4TB/s | Da Vinci/NPU 内部 SRAM 未公开；国产 HBM/堆叠良率是关键 | 双 die/多芯片封装；国产 interposer/基板能力是瓶颈 | SuperPod 内部华为自有互联；光模块/光电协同可能有自研路线，但 CPO 未公开 | Atlas 950/960 SuperPod 高密度液冷；供电细节未公开 |
| 12 | **国产非华为：阿里 Zhenwu 810E、百度 P800、寒武纪 590/690** | 阿里/百度节点未充分公开；寒武纪 590/690 被称 SMIC N+2/7nm 类（未检验） | 多数为 HBM 或 GDDR/DDR 混合；公开容量少 | 片上 SRAM/NoC 未公开；软件兼容 CUDA/PyTorch 是关键 | 国产先进封装、ABF/BT 基板、2.5D 能力逐步爬坡 | 主要走以太网/厂商自有互联；CPO 不公开 | 风冷到液冷混合；高密度集群会转液冷，供电/检测能力仍是瓶颈（推测） |

主要公开规格来源：NVIDIA Blackwell/Rubin 官方资料、AMD MI350/MI450 官方资料、Google TPU7/8 官方资料、AWS Trainium 官方资料、Meta/Broadcom 公开路线、Reuters 对华为/中国芯片链报道。([NVIDIA](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/))

### **4.2 制造设备、检测、内部存储检测、CPO、储能**

| \# | 芯片/芯片族 | AI 芯片制造设备 | AI 芯片检测 | AI 芯片内部存储检测 | 内部存储制造设备 | 光电共封装/CPO | 超级电容器与飞轮储能 |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 1 | GB200/B200 | ASML EUV/DUV；Applied/Lam/TEL 薄膜沉积/刻蚀；KLA 量测；TSMC CoWoS 线 | 晶圆 probe、KGD、HBM stack test、SerDes/NVLink 高速测试；ATE 以 Advantest/Teradyne 类设备为主（推测） | SRAM MBIST、ECC、冗余修复；HBM PHY training/BIST | SRAM 为逻辑制程内嵌；HBM TSV/DRAM 由 SK hynix/Samsung/Micron 设备链 | 无包内 CPO；外部 800G/1.6T 光模块 | 非芯片级；数据中心 UPS/BESS 可能用超级电容/飞轮做瞬态支撑，未公开 |
| 2 | GB300/B300 | 同 GB200，但 CoWoS、HBM3e+、基板良率压力更高 | B300 HBM3e+ 与 NVL72 系统级 burn-in 更复杂 | 同上，需更强 HBM margin test | HBM3e+ 供应链 \+ logic base die | 仍以可插拔 optics 为主 | GB300 高密度 rack 可能更依赖 flywheel/BESS 削峰（推测） |
| 3 | Rubin/Rubin Ultra | N3/N2 类 EUV、更多先进封装设备；HBM4 逻辑基底 4nm-class 设备链 | HBM4 KGD、chiplet interconnect、NVLink 6/SerDes ATE | HBM4 PHY/BIST、SRAM ECC/repair；更高带宽导致眼图/时序 margin 更难 | HBM4：DRAM 1c/先进 TSV \+ logic base die；Samsung HBM4 用 4nm logic base die | NVIDIA 后续 Feynman 官方提到 Kyber \+ CPO scale-up/optical scale-out；Rubin 是否用 CPO 未公开 | GW 级 Rubin 数据中心需要机房级储能，芯片不集成超级电容/飞轮 |
| 4 | MI350 | TSMC/OSAT 先进封装；HBM3E 测试与堆叠 | OAM 模组、Infinity Fabric、HBM3E KGD | SRAM MBIST；HBM ECC/repair | HBM3E DRAM/TSV；Samsung/Micron/SK hynix 设备链 | 无明确 CPO | DLC rack 可结合 UPS/BESS；飞轮未公开 |
| 5 | MI450/Helios | HBM4 封装、OCP ORW 机架制造；UALink/以太网 NIC 测试 | 72 GPU rack 级测试，NIC/SerDes 与 UALink 互操作测试 | HBM4 BIST/PHY training；SRAM MBIST | HBM4 供应与先进封装是核心 | 以 800G NIC/UALink/以太网为主，CPO 未确认 | 1GW 级部署可能需要站点级 BESS/飞轮削峰（推测） |
| 6 | TPU Ironwood | Broadcom/TSMC custom ASIC 设备链（推测）；液冷 pod 系统制造 | 9216-chip pod 级系统 test；ICI/网络一致性测试 | SRAM/VMEM BIST；HBM test | HBM \+ SRAM 逻辑嵌入 | Google 未公开 CPO；大规模光网络是确定需求 | Google 数据中心侧储能未映射到芯片，按站点级处理 |
| 7 | TPU 8i/8t | 同 TPU7，但 HBM/SRAM 容量更高 | Boardfly/3D Torus 大规模测试 | 8i 384MB SRAM，SRAM yield/repair 更重要 | 大 SRAM 宏 \+ HBM 设备链 | Virgo Network 连接规模极大；CPO 未公开 | GW/百万 TPU 级调度需要电网级储能，未公开 |
| 8 | Trainium2 | AWS/Annapurna custom ASIC 设备链；封装未全公开 | UltraServer/UltraCluster 级 burn-in；NeuronLink test | NeuronCore SRAM/缓存 BIST | 嵌入式 SRAM，HBM/外存测试 | 无 CPO 公开 | AWS 站点级 UPS/BESS，芯片层无 |
| 9 | Trainium3/4 | 3nm EUV；HBM3e；144-chip UltraServer 制造 | MXFP8/MXFP4 运算路径、HBM3e、EFA 网络测试 | SRAM MBIST \+ HBM ECC/PHY | HBM3e 设备链，Trainium4 带宽翻倍更依赖 HBM/封装 | 无 CPO 公开 | 5x tokens/MW 指标降低储能压力，但 GW 级仍需要电力缓冲 |
| 10 | Meta MTIA | Broadcom ASIC \+ TSMC \+ OSAT；先进封装/网络芯片协同 | PyTorch/vLLM/Triton 负载下系统 test；Ethernet scale-up | SRAM MBIST；HBM KGD（若 HBM 规格属实） | HBM/逻辑 SRAM | Broadcom 强在网络/CPO switch，但 MTIA 包内 CPO 未公开 | Meta 1GW+ 建设很可能配套 BESS/UPS，未公开 |
| 11 | 华为 Ascend | SMIC 先进 DUV 多重图形化（推测）；国产刻蚀/沉积/量测替代；HBM 国产化 | 国产 ATE、高速互联、HBM-like stack test；软件兼容测试 | Da Vinci SRAM MBIST；HiBL/HiZQ BIST | 国产 DRAM/HBM、TSV、先进封装设备链仍爬坡 | 华为有光通信能力，但 Ascend CPO 未公开 | 国产 AI 集群可能使用站点级储能，芯片级无 |
| 12 | 国产非华为 | SMIC/国内晶圆厂 \+ OSAT；部分设计曾受 TSMC/出口限制影响 | ATE、HBM/GDDR、国产互联测试；良率与一致性是主风险 | SRAM MBIST；GDDR/HBM ECC | 国产 SRAM/DRAM/封装设备；HBM 供给偏紧 | 多数没有 CPO；以以太网/PCIe/私有互联为主 | 大型集群用 UPS/BESS；飞轮/超级电容未见芯片级公开 |

---

## **5\. 哪些技术最可能决定 2026–2027 胜负**

| 技术环节 | 2026–2027 关键变化 | 受益/受限芯片 |
| ----- | ----- | ----- |
| **HBM3E → HBM4** | 2026 是 HBM3E 高峰与 HBM4 验证/初量产，2027 HBM4 成为高端 GPU/ASIC 主流。Samsung 已称 HBM4 商业量产，AMD Helios/MI455X 使用 Samsung HBM4。([Samsung Semiconductor Global](https://semiconductor.samsung.com/news-events/news/samsung-ships-industry-first-commercial-hbm4-with-ultimate-performance-for-ai-computing/)) | Rubin、MI450/MI430、TPU 8、MTIA 500、Ascend 950/960 |
| **先进封装/CoWoS** | Blackwell/MI450/TPU/MTIA 都依赖 2.5D/CoWoS 类封装；TSMC 提到 CoWoS 尺寸从 5.5 reticle 到 2028 的 14 reticle，ASE 2026 先进封装翻倍。([TSMC](https://pr.tsmc.com/english/news/3302)) | NVIDIA、AMD、Google TPU、Meta MTIA、Broadcom custom |
| **机架级互联** | 训练从单卡性能转向 NVL72、Helios、TPU pod、Trainium UltraCluster。NVIDIA Rubin NVLink 6 到 3.6TB/s/GPU；AMD Helios scale-up 260TB/s；Google TPU pod 到数千/万芯片。([NVIDIA Developer](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/)) | Rubin、GB300、MI450、TPU 8、Trainium3 |
| **光互联/CPO** | 2026 主流仍是可插拔 800G/1.6T 光模块；CPO 先在交换/互联侧落地。TSMC COUPE 2026 生产，NVIDIA Feynman 路线提到 CPO scale-up。([TSMC](https://pr.tsmc.com/english/news/3302)) | Broadcom/Marvell 网络、NVIDIA 后续、超大 TPU/MTIA/Trainium 集群 |
| **供电与散热** | 100kW–200kW/rack 变常态，DLC 从“高端选项”变成“默认”。Qualcomm AI200 也做到 160kW/rack、DLC，说明推理机架同样高功率。([Qualcomm](https://www.qualcomm.com/news/releases/2025/10/qualcomm-unveils-ai200-and-ai250-redefining-rack-scale-data-cent)) | GB300、Rubin、MI450、TPU 8、Trainium3、Qualcomm AI200 |
| **国产替代** | 中国市场 2025 已有约 400 万 AI 加速卡，国产份额约 41%；华为、阿里、寒武纪、昆仑芯继续放量，但高端 HBM/先进封装/软件生态仍是限制。([Reuters](https://www.reuters.com/world/china/chinese-chipmakers-claim-nearly-half-of-local-market-nvidias-lead-shrinks-idc-2026-04-01/)) | Ascend 950/960、Zhenwu 810E、P800、Siyuan 590/690 |

**最保守结论**：2026 年 AI 芯片行业不是“Rubin 一代全面替代 Blackwell”，而是 **Blackwell Ultra \+ TPU/Trainium/国产 ASIC 多线放量**；2027 年才是 **Rubin、MI450/Helios、TPU 8、Trainium3/4、MTIA 450/500、Ascend 960** 真正拉开下一代供给曲线的年份。

