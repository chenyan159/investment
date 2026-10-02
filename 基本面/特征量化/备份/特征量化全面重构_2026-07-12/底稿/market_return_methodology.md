# 特征量化样本外行情口径与质量核验

## 结论摘要

- 52 个正式量化评分文件的文件名日期均为 `2026-06-04`，本机落地时间为 `2026-06-04 00:47:51` 至 `04:07:37`（America/Los_Angeles），都早于当日美股 `06:30` 开盘。因此主样本外口径采用 `2026-06-04 调整后开盘价 -> 2026-07-10 调整后收盘价`。
- 180 个研究股票代码全部取得有效行情；180 个代码的入口日均为 `2026-06-04`，最后可得交易日均为 `2026-07-10`，没有仍需剔除的缺失或停牌样本。
- 主口径全样本均值 `-5.59%`、中位数 `-3.40%`、上涨比例 `37.78%`。65/180 跑赢 SPY，76/180 跑赢 QQQ，74/180 跑赢 SOXX。
- 同期主口径基准：SPY `+0.64%`、QQQ `-1.25%`、SOXX `-1.03%`。辅助收盘到收盘口径分别为 SPY `-0.03%`、QQQ `-1.93%`、SOXX `-3.50%`。
- 主口径最好为 ICHR `+44.31%`，最差为 NVTS `-53.11%`。这些只是全池描述，不应代替按特征分组、分位数组合和连续分数相关性检验。

## 收益公式

Yahoo Finance 的 `Close` 已经对拆股做历史调整，但不包含现金分红；`Adj Close` 同时反映拆股和股息/资本分配。因此本次把调整后收益作为主口径，避免 KLAC、CRWD 等拆股造成伪暴跌。

```text
调整后开盘价 = 当日 Open * 当日 Adj Close / 当日 Close
主收益 = 2026-07-10 Adj Close / 2026-06-04 调整后开盘价 - 1
辅助收益 = 2026-07-10 Adj Close / 2026-06-04 Adj Close - 1
不含分配的收盘收益 = 2026-07-10 Close / 2026-06-04 Close - 1
```

主口径对应评分在开盘前已经可知、并按当天开盘执行；辅助口径用于排除 6 月 4 日盘内波动的影响。Yahoo 对调整后收盘价的定义见：

- https://uk.help.yahoo.com/kb/finance/adjusted-close-sln28256.html
- https://in.help.yahoo.com/kb/finance/download-historical-data-yahoo-finance-sln2311.html

每个股票和基准的实际 JSON 请求 URL 已写入明细 CSV 的 `source_url` 列。

## Corporate actions 与代码变更

- `CRWD`：`2026-07-02 4:1` 拆股；调整后主收益 `+11.07%`、辅助收益 `+4.12%`。
- `KLAC`：`2026-06-12 10:1` 拆股；调整后主收益 `+12.72%`、辅助收益 `+8.64%`。
- `PSTG`：不是停牌或退市。Everpure 官方公告显示，公司自 `2026-04-17` 起把 NYSE 代码从 `PSTG` 改为 `P`，CUSIP 不变。本次以 `P` 的连续行情计算：主收益 `+0.08%`、辅助收益 `+1.04%`。旧 `PSTG` 数据源已经失效或呈现残留冻结值，不得用于回测。官方公告：https://www.everpuredata.com/company/newsroom/press-releases/everpure-to-change-ticker-symbol.html

拆股事件详见 `split_action_checks.csv`；代码变更和质量说明详见 `data_quality_issues.csv`。

## 海外 ADR 与 OTC

- 15 个 OTC 报价代码全部取得 `2026-06-04` 至 `2026-07-10` 的 USD 行情：`ABBNY, AJNMY, ASGLY, ASMIY, ASMVY, ATEYY, BESIY, DSCSY, HOCPY, IFNNY, MICLF, MIELY, RYCEY, SHECY, SOMMY`。
- 它们使用美国 OTC 报价而非母国本币普通股，收益同时包含 ADR/OTC 相对母股的汇率、流动性和价差效应。后续正式模型应增加“主上市地复核”和最低成交额筛选，不能把 OTC 异常价差误判成基本面特征收益。
- 全部 180 个最终使用序列的币种元数据均为 USD，最后交易日均为 7 月 10 日。

## 输出文件

- `company_returns_2026-06-04_to_latest.csv`：180 家公司主收益、辅助收益、三基准超额收益、拆股/分红、交易所、币种、代码变更和逐行数据 URL。
- `benchmark_returns_2026-06-04_to_latest.csv`：SPY、QQQ、SOXX 两种收益口径。
- `price_history_daily.csv`：180 家公司加 3 个基准的 5,124 行逐日底稿。
- `split_action_checks.csv`：拆股影响专项检查。
- `data_quality_issues.csv`：PSTG 到 P 的代码变更及处理。
- `return_run_summary.csv`：覆盖数、总体分布和基准摘要。
- `universe_audit.csv`：每个股票在 52 个正式结果中的覆盖、文件日期和落地时间。
- `download_feature_returns.ps1`：下载、计算和全部 CSV 生成脚本。

## 适用边界

- Yahoo Finance 是公开可复核的延迟行情源，不是交易所官方成交审计源；本结果适合研究重构和样本外方向性评估，不应用作成交价或交易损益对账。
- 目前样本外仅约 25 个交易日，统计功效有限，而且覆盖财报、拆股、代码变更和高波动阶段。评价特征时必须同时报告秩相关、分位数组合、行业/规模中性结果、置信区间及多个未来窗口，不能只看一次短期涨跌。
