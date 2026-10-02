# 利率对标普500与纳斯达克100影响研究：第一阶段数据准备

生成时间：2026-06-24T06:15:00.530349+00:00 UTC
请求起始日期：1990-01-01
下载结束参数：2026-06-25

## 数据源

- 市场价格：Yahoo Finance chart API，覆盖 `^GSPC`（SPX）和 `^NDX`（NDX）；同时保留 `SPY`、`QQQ` 作为可交易 ETF/复权价格代理，但 ETF 历史不都满足 30 年。
- 利率与利差：FRED fredgraph CSV，覆盖政策利率、货币市场利率、国债曲线、TIPS 实际利率、盈亏平衡通胀、企业债收益率/OAS、按揭利率、Prime rate、金融条件指数。
- 元数据：`data/metadata/source_map.csv` 记录每个字段的来源、FRED/Yahoo ID、类别和历史长度预期。

## 核心文件

- `data/raw/yahoo_index_ohlcv_daily.csv`：Yahoo 原始日频 OHLCV。
- `data/raw/fred_interest_daily_long.csv`：FRED 原始日频/周频/月频长表。
- `data/weekly/index_prices_weekly.csv`：周五口径市场价格与 1/4/13/52 周收益率。
- `data/weekly/interest_rates_weekly.csv`：对齐到市场周历的利率水平；低频系列在首次观测后按频率限制向前填充。
- `data/weekly/interest_rates_weekly_data_age.csv`：每个利率字段距离真实观测值的周数，用于识别陈旧填充值。
- `data/weekly/rate_features_weekly.csv`：利率水平、期限利差、信用利差、倒挂标记、1/4/13/52 周 bp 变化。
- `data/weekly/market_rates_weekly_panel.csv`：主研究面板，按 `week_end` 合并市场价格和利率特征。
- `data/metadata/series_coverage.csv`：每个系列的起止日期、观测数、历史年限和是否超过 30 年。
- `data/data_inventory.csv`：本目录 CSV 文件清单与日期范围。

## 周频口径

- 市场价格按 `W-FRI` 聚合：周内第一笔 open、最高 high、最低 low、最后 close/adjclose、成交量求和。
- 周频研究文件只保留已经完成的市场周；原始日频文件仍保留下载时能拿到的最新交易日。
- 利率按 `W-FRI` 取周内最后一个可用观测值；合并面板为便于建模，对每个利率系列在首次观测后 forward-fill 到市场周历，但 daily/weekly/monthly 分别限制为 2/2/8 周，避免把长时间停发误当连续数据。
- FRED 的月频系列如 `AAA`、`BAA` 只适合做中低频背景变量；若做严格事件研究，需要再加入真实发布时间/修订时间约束。

## 注意事项

- 本阶段是研究数据准备，不是正式回归结论。
- `SPX`、`NDX` 和多数核心政策/国债/按揭/Prime/FRED 月频信用收益率系列具备 30 年以上历史；`SOFR`、TIPS 实际利率、breakeven、部分 OAS 系列起始较晚，不能强行当作完整 30 年样本。
- Yahoo 与 FRED 公共接口适合研究准备和可复跑验证；若后续用于交易级验证，应替换为授权行情和点时间宏观数据库。
- 无下载失败。

## 复跑

```powershell
python "D:\drive\Investment\技术面\利息\scripts\build_interest_weekly_data.py"
```
