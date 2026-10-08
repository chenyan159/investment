# 行业调研上游探索：开源软件、标准、工程验证与硬件拆解

核查日：2026-10-08（用户时区 America/Los_Angeles）。本文件是一次性探索片段，不修改正式研究方案、报告或索引。已阅读根目录、基本面和行业调研 AGENTS.md；91 主题索引用于主题映射。本文的频率与工作量是建议/估算，并非已运行系统的实测值。

## 核心判断

这些来源应该进入行业调研上游，但应按“证据对象及状态”分类，不能都塞进会议调研。最优先的是公开代码/发布、公开标准贡献和工程验证；会议只是发现原始条目的一个入口。公开浏览、机器可读取、允许正文进入 AI、可复现、能证明商业采用，是五个不同条件。

尤其有三项实际发现：

- DeepSeek 不能以一个仓库概括。当前公开 API 抽样：DeepEP 最近 README 提交为 2026-09-30T01:09:46Z，核心 V2.5 提交为 2026-09-29T05:22:15Z；DeepGEMM 最近发布提交为 2026-09-30T01:48:05Z；DeepSeek-V3 最近提交仍为 2025-08-28T03:24:26Z。模型展示/参考推理仓库与持续工程库需用不同监测频率，不能把 V3 PR 数量当作 DeepSeek 全部技术进展。[DeepEP](https://github.com/deepseek-ai/DeepEP)、[DeepGEMM](https://github.com/deepseek-ai/DeepGEMM)、[V3](https://github.com/deepseek-ai/DeepSeek-V3)。
- SGLang PR #43008 很好地展示了标题与真实收益的区别：一个微内核样本从 13.5μs 到 5.2μs，端到端输出 tok/s 在并发 1/2/4/8/16 时分别变化 +3.1%/+3.5%/+5.4%/+6.0%/-2.0%；KV 池从 2,284,032 降到 2,078,208 tokens。作者注明先跑开启组，未在关闭组后再跑开启组，不能排除时间漂移。API 核实仍 open、merged_at=null；不能写成已发布且全面提升 2.6 倍。[原始 PR](https://github.com/sgl-project/sglang/pull/43008)。
- CXL 官方规格下载页有明确 AI 条款。2026-02-12 的 Evaluation Copy Agreement 第 3 节，未经董事会事先书面同意禁止 AI 处理规格；短原文为 “using any AI Systems to Process any CXL Specification”。本次未申请或获取规格正文。Research runner 不应默认导入该规格；公开目录/新闻监测与受限规格正文需分开。[CXL 官方下载及条款](https://computeexpresslink.org/cxl-specification/)。

## 已实际打开的来源与可接入性

| 来源 | 公开程度和机器读取 | 本次验证的时效/原始条目 | 能证明什么；主要限制 | 建议分类与优先级 |
|---|---|---|---|---|
| [vLLM](https://github.com/vllm-project/vllm/pulls) | 仓库、PR、diff、issues、release 公开；GitHub REST 可匿名 JSON，官方限额 60 请求/小时/IP | 10/08 UTC 有大量新增 PR；[#60514](https://github.com/vllm-project/vllm/pull/60514) 修复无 nvcc 时 DeepGEMM/FlashInfer 选择，API 核实 open、4 文件、+114/-2 | 可见支持什么 GPU/模型、软件瓶颈、量化/KV/网络传导；open PR 只是提案，CI通过不等于生产可用，也不能推设备销量 | 开源软件与工程进展；P0；每日元数据扫描、每周精选 |
| [SGLang](https://github.com/sgl-project/sglang/pulls) | 同上；可读 benchmark 参数与 PR 作者限制说明 | #43008 10/07 UTC 创建，8 文件、+622/-11，仍未合并 | 在给定模型、GPU、batch、精度下的声明/证据；单内核与端到端收益分开；贡献者不一定代表所属雇主采购 | 开源软件与工程进展；P0 |
| DeepSeek 工程库 | [DeepEP](https://github.com/deepseek-ai/DeepEP) / [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) / [V3](https://github.com/deepseek-ai/DeepSeek-V3) 均公开，MIT/模型许可需逐仓分开；API已实测 | API日期见上；DeepEP README 明确 EP dispatch/combine 占用 SM，Bucket/Engram/PP 为 experimental | 模型架构、通信方式、GPU/网络约束和实现进展；公开库不代表内部代码完整公开；社区 fork、官方分支与第三方适配必须标识 | 工程库 P0；模型展示仓 P1，发布触发 |
| [OCP Contribution Database](https://www.opencompute.org/contributions/) | 公共目录有 contributor、family、project、release year；PDF和部分设计文件可直读；未验证稳定公开查询API | [SST v0.3 PDF](https://www.opencompute.org/documents/ocp-sst-design-specification-v0-3-final-pdf) 24 页，effective 6/22/2026，5/20 首稿；[液冷项目](https://www.opencompute.org/projects/cooling-environments/) 列 BMQC、UQD、Deschutes、冷却液及冷板测试贡献 | Operator requirements、接口和资格要求、材料/组件设计条件；accepted contribution、whitepaper、draft规格、marketplace产品不能合并为“行业标准已量产”；同站有旧wiki和TBD，不能以首页最后更新时间替代条目日期 | 标准与接口/公开工程要求；P0；每周目录差分，更新时精读 |
| [IEEE 802.3dj 公共区](https://www.ieee802.org/3/dj/public/) | 静态HTML索引、公开贡献PDF、minutes、motions、comments、reflector；另有 private area，不能假设草案正文全公开 | [9月材料](https://www.ieee802.org/3/dj/public/26_09/index.html) 最后更新9/30；可直接打开 [NVIDIA Bin16贡献](https://www.ieee802.org/3/dj/public/26_09/rubin_3dj_01_2609.pdf) 22页及 [47页议程](https://www.ieee802.org/3/dj/public/26_09/agenda_3dj_b_2609.pdf)；议程考虑D3.2评论、生成D3.3 | 可证明哪种物理限制/测试方法在讨论、支持方/反对方、投票阶段；不能把作者提案当已采纳标准；会议禁止观察者自行录制，采集已发布PDF/纪要即可 | 标准草案与技术争议；P0；每周扫描、会后增量 |
| [UALink](https://ualinkconsortium.org/specification/) | 目录公开；Common 2.0下载是姓名/公司/email/EULA表单，不是匿名直链；正文只供内部评估、不可转授 | 当前目录含200G 1.0、Common2.0、128G DL/PL1.0、200G DL/PL2.0、Chiplet1.01、Manageability1.0；[Common2.0条款](https://ualinkconsortium.org/specification/ualink-common-2-0-specification/) 已读 | 标准发布范围/分层、管理接口方向；会员名单不证明量产采用；免费评估不等于可公开再分发，也不等于已获AI使用许可 | 目录/公开资源 P0；受限规格正文需单独使用权状态 |
| [Ultra Ethernet](https://ultraethernet.org/specification-history/) | 公开版本历史、release notes PDF；最新规格下载入口在本次web工具报内部错误，未把正文读取记为成功 | 明确 v1.0.3 于7/16/2026；[2页 release notes](https://ultraethernet.org/wp-content/uploads/sites/20/2026/07/UE-Specification-1.0.3-release-notes-.pdf) 已打开；1.0/1.0.1/1.0.2历史可定位 | 版本变更和协议要求，不代表交换机/NIC全功能已经交付；不能仅关注首次发布而漏勘误 | 标准与接口 P0；每周元数据和勘误扫描 |
| [UCIe](https://www.uciexpress.org/specifications) | 目录公开；[3.0申请](https://www.uciexpress.org/3-0-spec-download) 需公司/教育email和身份字段、条款；页面称最多7个工作日；许可为非商业内部评估 | 当前目录 3.0 含48/64GT/s；并有CTA/CSSC/TRoCS ECN | 可证明规范路线/发布，不能直接证明 chiplet互通和交付良率；规范正文不可默认灌入统一公共语料 | 标准与接口；目录P1，正文受限 |
| [OpenConfig public](https://github.com/openconfig/public) | Apache2.0、公开YANG模型/发布文档/issue；GitHub机器读取 | 此仓用途为operators group 发布模型，不必然是开放接受所有PR的开发仓 | 电信/云运营商管理和遥测需求、可支持的字段；模型存在不证明供应商功能已实现或客户购买；用YANG版本而不是star | 软件接口/运维遥测；P1；周扫 |
| [SONiC](https://github.com/sonic-net/SONiC) | 总仓是文档/协调/网站，公开MoM/HLD；真正代码需进组件仓，如 [sonic-buildimage](https://github.com/sonic-net/sonic-buildimage/pulls)、SAI/orchagent等 | 已打开总仓和buildimage PR列表 | Feature/HLD → merge → release → supported platform → tests需串起来；总仓提交量不是NOS开发速度；平台“支持”不代表每特性可用 | 开源网络工程；P1 |
| [MLCommons Inference Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) | 公共results、raw .xlsx、supplemental PDF、[v6.1提交仓](https://github.com/mlcommons/inference_results_v6.1) summary.csv/各提交代码日志；无付费门槛 | 当前 v6.1，官方9/16/2026宣布；results页注明结果可能修改/失效，有change log | 规定模型/精度/场景下性能，区分Closed/Open、Available/Preview/RDI、Server/Offline/Interactive、加速卡数/系统功耗；不能用单分数推平均客户利用率或采购规模 | 工程验证与可复现benchmark；P0；发布时+勘误周扫 |
| [IETF Datatracker](https://datatracker.ietf.org/api/) | 正文TXT/HTML、版本、状态、邮件/会议；只读JSON/XML API、单文档doc.json无需密钥，已实际HTTP200 | [RFC9843 doc.json](https://datatracker.ietf.org/doc/rfc9843/doc.json) 返回 name/rev/group/state/rev_history/authors 等17字段；[活动草案](https://datatracker.ietf.org/doc/active/) 可筛WG | 个体draft、WG adopted、last call、RFC、Standards Track与Informational区分；任何人提草案不代表行业共识。适合QUIC/路由/Security/REST/数据中心拥塞议题 | 标准草案与协议；P0，可自动化程度高 |
| [arXiv](https://arxiv.org/abs/2412.19437) | 版本化HTML/PDF/TeX及 [API文档](https://info.arxiv.org/help/api/index.html)；逐论文license | V3报告 v1 2024-12-27、v2 2025-02-18，链接官方代码/权重 | 研究者声明、方法和技术路线；预印本不是同行评审，成本样本不是训练全成本；新论文可低时滞，但需论文→实现→benchmark链 | 论文/方法与技术验证；P1；日元数据+周精选 |
| [Hugging Face官方V3模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V3) | model card、文件、community公开；只采README/config/tokenizer/commit元数据，不下载巨量weights；官方组织/社区量化版分开 | 卡可连接arXiv、模型配置和官方repo；有部署支持说明及不同许可文件 | 可证明实际公开权重/架构与配置；模型卡是作者披露，不能证明商用需求；下载计数不等于独立开发者或推理调用；网页自动生成用法和卡内手写旧说明可能不同步 | 模型/数据发布；P1；commit/version触发 |
| [iFixit](https://www.ifixit.com/Teardown) | 公共拆解与API；[API说明](https://www.ifixit.com/api-docs)明确 BY-NC-SA、商业用需另议、禁止LLM训练；[Guides API](https://www.ifixit.com/api/2.0/doc/Guides)支持filter=teardown/modifiedSince | 公开GET一条样本HTTP200：guide240330，Lasko5390 heater拆解，modified_date1790822636 | 可见一个实物的PCB/元器件/装配和维修性；样本BOM不代表全部批次、供应商份额或工厂产能；以消费设备为主，对AI服务器覆盖弱 | 实物拆解/样本设计；P2；按产品触发，需保留许可状态 |
| [ServeTheHome](https://www.servethehome.com/this-is-the-nvidia-dgx-gb200-nvl72/) | 页面/照片公开，可RSS候选但本次未验证feed；没有验证开放内容API | 已读2024-03-19 GTC现场GB200文章，作者明确show floor拍照，不是量产实测 | 实物布局、busbar/blind-mate液冷/NVLink与前面板；厂商说省20kW是转述，不能标独立测量；每篇区分展示、review、拆机、benchmark、赞助 | 实物观察与独立测试；P1/P2；按新平台触发 |
| [TechInsights](https://www.techinsights.com/solutions/market-solutions/vehicle-transportation) | 公开产品说明/博客摘要，平台深度reports/images/design-wins/BOM需订阅；无已验证公开report API | 官方页明示subscription-based，包含板/芯片图和BOM；只读公开介绍，未登录/取付费正文 | 原始reverse engineering价值高，但cost model是估计，实物design win仅限样本；公开摘要不能替代付费证据 | 付费受限拆解索引P2；取得授权才正文接入 |

## 仅候选或验证不足

- OIF：官方搜索索引可定位 [CEI-224G framework](https://www.oiforum.com/wp-content/uploads/OIF-FD-CEI-224G-01.0.pdf)，但本次直接打开PDF/IA目录失败，未验证正文。应继续核查IA、framework、interop demo三种文档及不同版本，不能把framework等同正式IA；优先级P1。
- Yole/System Plus：主站返回403；发现其官方Yole Group账号推广GH200/BlueField3/HBM逆向研究，但未验证主站报告目录/价格/许可。本次不把其视作可持续自动采集来源，不用Slideshare/Scribd转存付费全文补缺。待人工确认购买/摘要权益。
- OpenReview：[官方API v2文档](https://docs.openreview.net/reference/api-v2)已打开；未抽样具体paper/review线程，因此只列候选。需分public note和private review；conference接收结论、review意见、代码复现均分别存。与arXiv使用DOI/arXiv ID/OpenReview forum关联去重。
- 其他复用GitHub适配器的候选：PyTorch、Triton、FlashInfer、NCCL、UCX/UCCL、LMCache、Ray/KubeRay/Kueue、Dynamo、TensorRT-LLM、SGLang ROCm/Ascend适配、Linux RDMA、SPDK/io_uring；由主题明确瓶颈后纳入，不做整个平台全量监控。
- 91主题可继续映射 DMTF Redfish、SNIA/NVMe、JEDEC公开新闻/规范目录（正文访问需另查）、Khronos/OpenXR、NIST/OWASP/CSA、W3C。机器人ROS/MoveIt及航天监管由其他研究片段覆盖。

## 采集和研究如何划分工作量

估算口径：一个已有HTTP/JSON、PDF抽取、归档与runner基础的工程人员；一个主题理解合格的分析人员。首轮量以5个GitHub仓、OCP/IEEE/UEC三个标准入口、MLPerf和IETF为试点；不含付费采购、复杂登录和大规模跑benchmark。

| 来源家族 | 首轮理解/注册 | 可复用采集适配器估算 | 持续分析工作量估算 |
|---|---|---|---|
| GitHub 5个精选仓 | 4–8小时：定位维护仓、发布语义、标签/path和硬件映射 | 1–3人日：条件GET/分页、checkpoint、PR更新追踪、commit/release关联；无需为每仓造一个完整research任务 | 每周2–4小时：对10–30个预筛事件进行技术判断；所有PR都读会失控 |
| OCP/IEEE/UEC | 1–2人日：定位权威项目和版本，梳理公开/受限边界 | 2–4人日：HTML/PDF目录差分、内容hash、同版本重传、附件识别；PDF图表解释需要review | 正常每周2–4小时；有会议/新版时每源2–6小时 |
| MLPerf | 4–8小时：理解closed/open、场景、精度和availability | 1–2人日：summary.csv/xlsx/schema、系统与硬件名归一、勘误修订 | 发布一轮4–8小时；日常0.5–1小时/周 |
| IETF | 4–8小时：筛WG和状态 | 0.5–1.5人日：JSON/版本、草案状态、关联RFC与邮件 | 每周1–2小时，按重大状态变更触发 |
| 论文/模型卡 | 4–8小时：关键词/机构/问题清单 | 1–2人日：元数据/版本、论文→代码→权重链接、license | 每周2–4小时精选，全文精读另算每篇1–3小时 |
| 拆解/样本测试 | 每家2–4小时明确领域覆盖、许可、证据颗粒度 | 公开标题索引0.5–1人日/家；正文非统一API，受限来源暂不建适配器 | 每篇0.5–2小时；复杂芯片逆向或精读测试数小时至数日 |

这些区间不是交付报价。最容易低估的是语义判断：同样一个“support”可能只是PR、合并、CI、release、实机验证、商用采用中的不同阶段；解析器下载成功并不完成研究。

## 建议的证据分类与runner输入

1. **发布/实现证据**：commit、merged PR、release、模型文件版本；状态为 proposed→merged→released→tested，不允许自动跳到deployed。
2. **规范/架构证据**：individual proposal、working-group draft、accepted contribution、ratified/发布规格、errata；注明组织、作者、公司affiliation、投票/采纳状态、替代版本。
3. **测试/验证证据**：benchmark、interop/compliance、公开测试方法、实物拆解；保存sample/设备SKU/硬件数量/软件SHA/模型版本/精度/数据集/负载/功耗边界/误差和限制。
4. **研究解释**：论文、作者说明、独立review；推断独立于原始证据，不把评论者观点写成库事实。

建议每条source registry字段：source_id、组织/域名、权威入口、source_family、topics多对多、company实体、access_level（public/form/member/paid）、machine_route（API/HTML/PDF）、rights_status（尤其AI正文）、source_published_at、source_updated_at、observed_at、version/hash、evidence_state、cadence、fetch_status、review_effort。事件库使用稳定ID（repo+PR、specID+version、benchmark resultID、paperID+version）；抓取批次共享，不按91主题各自再抓。

两阶段适合runner：先低成本deterministic采集/差分去重，再把高价值变更送研究任务。changed_files/path、硬件标签、merge/release、bench/accuracy结果可预筛；docs/typo/build noise要降级。Research任务围绕“某瓶颈/采用状态是否改变”关联三条证据链，不给每个PR写完整行业报告。

最有价值的跨来源链示例：MoE通信论文/DeepEP发布→vLLM/SGLang适配→对应GPU/网络benchmark→标准接口与operator requirements→OEM实物/最终客户披露。前四层已经能及时识别需求结构改变，但商业规模仍需订单、部署、收入等独立证据。

## 公开API只读实测记录

普通沙箱网络对api.github.com发生DNS失败；使用授权的require_escalated公开GET后成功，未使用token或登录。不应把工具网络限制误判为平台不可采集。

- GitHub commits endpoint：`https://api.github.com/repos/{owner}/{repo}/commits?per_page=1`；repo分别DeepEP/DeepGEMM/V3，HTTP JSON成功。初始响应rate remaining59，后续58/57，与匿名60/hour政策一致。[官方限额](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)。
- DeepEP V2.5：SHA `def865146e95aa9ea223e277c0a8a4c6b81e5ac7`；DeepGEMM 9/30发布：SHA `057ca5964aae0879ff2e0eb71ee05a3cb0ba3df7`；V3：SHA `9b4e9788e4a3a731f7567338ed15d3ec549ce03b`。
- GitHub PR endpoints：vLLM60514 created_at2026-10-08T01:22:08Z，updated_at01:22:46Z；SGLang43008 created_at2026-10-07T18:21:25Z，updated_at18:29:58Z；state均open/merged_at均null。本地LA换日不能丢失UTC。
- IETF `https://datatracker.ietf.org/doc/rfc9843/doc.json`：HTTP200，JSON含版本历史/状态/组织等。
- iFixit `https://www.ifixit.com/api/2.0/guides?filter=teardown&order=DESC&limit=1`：HTTP200，guide240330标题/类型/链接/修改时间可读。这里只验证GET通路；未来正文使用仍受其许可约束。

GitHub web搜索抓取的DeepEP/DeepGEMM commit列表曾只到8月/7月（页面标3周前crawl）；实时REST已发现9月提交。因此初步exploration可用网页搜索，正式持续采集不能仅以搜索索引“最新”结果为checkpoint。
