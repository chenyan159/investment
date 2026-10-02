# 24 家公司综合排名、情景决策与配置

先完整读取同目录 `00_通用规范.md`。然后读取本批次已经完成的四份组别报告：

1. `01_半导体计算与制造_综合评估_2026-08-19.md`
2. `02_网络互连与连接器_综合评估_2026-08-19.md`
3. `03_云算力服务器与存储_综合评估_2026-08-19.md`
4. `04_电力冷却与工业基础设施_综合评估_2026-08-19.md`

分析前必须确认四份文件全部存在、非空、日期为 2026-08-19 且 `status=complete`，并严格匹配：01=`group_id=01_semiconductor_compute_manufacturing` 与 `AVGO,AMKR,NVDA,TSM,MKSI,MU,ALAB`；02=`group_id=02_network_interconnect_connectors` 与 `TEL,CRDO,LITE,ANET`；03=`group_id=03_cloud_compute_servers_storage` 与 `HPE,META,STX,WDC,NBIS,CRWV`；04=`group_id=04_power_cooling_industrial_infrastructure` 与 `CMI,CARR,EME,POWL,NVT,GEV,BE`。四集合并集必须恰好是 24 个 ticker 且无重复、遗漏或额外公司；四份的 `valuation_target_date`、`model_anchor_path`、`market_snapshot_id`、`price_snapshot_path`、`price_snapshot_sha256`、`price_snapshot_generated_at` 和 `price_as_of` 必须完全一致。任一检查失败则硬停且不写 master，不得用直接上游重建或替代缺失组。

四份文件位于本批次目录根层。还必须读取共享市场快照，以及唯一固定的 `金融资料/每日金融数据/每日金融数据_2026-08-19.md`（SHA-256 `266EB51FAACC64888C2FA02F4984275B4C7CC53F51FA13D653226197A795DFE6`）；不得改读运行时更晚日期或联网行情。对四份组别报告中的决定性结论，抽查相应 2026-08-19 公司评估、投资决策和情绪原文。不得读取旧排序、旧对比或旧版报告。

本次全集必须且只能是：`TEL、CMI、AVGO、AMKR、CARR、HPE、NVDA、TSM、META、EME、POWL、MKSI、NVT、MU、ALAB、CRDO、LITE、ANET、GEV、BE、STX、WDC、NBIS、CRWV`。

## 必须输出

1. **执行摘要**：直接回答当前最值得投入新资金的是谁、哪些只适合等待价格/证据、哪些只适合小仓位投机、哪些当前不值得承担风险；每项都要有条件和失效点。
2. **24 家统一总表**：统一价格/日期、业务质量、经营动量、盈利与 FCF、资产负债表、估值、当前经营定位、主/相邻市场状态下基准价值区间、悲观下行、乐观上行、reverse-DCF 隐含要求、最强催化、最大风险、传闻等级、当前条件立场、强/一般安全边际价格区。
3. **六种投资哲学分别排序**：近端兑现、长期复利质量、价格赔率、防守资本保全、爆发增长与产业突破、市场定价错位。每种都必须完整列出 1–24 名并解释决定性变量；不得用同一总分换权重伪装成六种方法。
4. **总体现阶段分层**：用 `核心候选 / 分批候选 / 等待回撤或证据 / 仅投机小仓位 / 暂不投入新资金` 五层覆盖全部 24 家。总层级基于 8–16 个月风险调整判断，不用六维多数票。
5. **多情景视图**：共享主状态、相邻状态、有序风险收缩、信用压力下，哪些排名最稳定，哪些会大幅反转；列出经营情景与市场状态之间最重要的联动。
6. **价格与证据触发器**：每家公司给现价距离、强/一般安全边际区、下一项最可能改变判断的财报/订单/产能/融资/客户证据、最早日期、失效条件。对 8 月 18 日决策锚与固定 8 月 19 日收盘叠加价格之间的变化，重新计算回报距离但不擅自改内在价值假设。
7. **传闻叠加账本**：只列足以改变情景的 B+/B/C/D 线索，说明确认/否认时先改变哪个变量和哪一经营行；传闻不能改变事实基准。列出没有高价值传闻的公司，避免为了形式制造消息。
8. **组合与相关性**：给防守、均衡、进攻三种示例组合思路，说明同一 AI capex、HBM、光互连、电力/冷却、GPU 云融资风险下的重复暴露、单股上限和为何不应把高度相关公司误当分散。组合仅用于比较研究，不假定用户的资金规模或风险承受力。
9. **逐公司短结论**：24 家每家至少一段，包含“为什么现在值得/不值得”“什么价格或证据会改变判断”“最容易错在哪里”。
10. **数据质量与限制**：列明价格时点、TSM 币种、CRWV 市值重算、负 FCF/负 EPS、不适用倍数、非 GAAP 与一次性项目、来源缺口。

结论要直截了当，但必须是条件化、可验证、可复盘的研究判断。不要写成确定收益承诺，不要用免责声明取代回答。

输出只写入 runner 指定的唯一文件 `05_24家公司综合排名与配置_2026-08-19.md`，不修改任何上游。报告开头必须按一行一个 `key=value` 的机器可读格式逐项写明：`batch_id=24_company_investment_value_20260819`、`tickers=TEL,CMI,AVGO,AMKR,CARR,HPE,NVDA,TSM,META,EME,POWL,MKSI,NVT,MU,ALAB,CRDO,LITE,ANET,GEV,BE,STX,WDC,NBIS,CRWV`、`report_date=2026-08-19`、`valuation_target_date=2027-08-19`、`model_anchor_path=金融资料/每日金融数据/每日金融数据_2026-08-18.md`、`market_snapshot_id=US-EQ-USD-20260818-CLOSE-5B-v1.0`、`price_snapshot_path=金融资料/每日金融数据/每日金融数据_2026-08-19.md`、`price_snapshot_sha256=266EB51FAACC64888C2FA02F4984275B4C7CC53F51FA13D653226197A795DFE6`、`price_snapshot_generated_at=2026-08-19 13:01:58 PDT-0700`、`price_as_of=2026-08-19_CLOSE`、`status=complete`。
