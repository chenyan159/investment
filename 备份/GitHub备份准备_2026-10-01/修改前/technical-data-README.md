# Common Daily Research Data

本目录是技术面研究的标准日频数据集。最完整面板为 `features/common_research_daily_panel_full.csv`，以 SPX 交易日历对齐。

## 核心文件

- `raw/yahoo_ohlcv_daily.csv`、`raw/yahoo_adjclose_wide.csv`：市场价格和复权价格。
- `raw/fred_series_long.csv`：宏观、利率、信用、波动率、商品和流动性数据。
- `features/market_momentum_features.csv`：收益率、实现波动率、回撤和价格位置特征。
- `features/macro_daily_features.csv`：对齐市场日期的宏观特征。
- `features/valuation_daily_lagged_proxy.csv`：保守滞后的公开估值代理。
- `features/macro_event_flags_daily.csv`、`features/fomc_event_flags_daily.csv`、`features/nfp_event_flags_daily.csv`：宏观事件标记。
- `features/sp500_current_constituents_breadth_proxy.csv`：基于当前成分股的市场宽度代理。
- `features/sp500_current_holdings_concentration_proxy.csv`：基于当前持仓的集中度代理。
- `features/policy_geopolitical_risk_features.csv`：EPU 与 GPR 风险特征。
- `data_inventory.csv`、`unresolved_data_requirements.csv`：数据范围和未满足需求。

## 数据来源

主要使用 Yahoo、FRED、公开估值表、Wikipedia、iShares、AI-GPR 和 PolicyUncertainty 等公开数据。公开数据适合研究准备和可复跑验证，不等同于授权的点时交易数据库。

## 关键限制

- 当前成分股宽度和当前持仓集中度回推存在 survivorship bias，不是历史点时成分或权重。
- 估值代理采用保守滞后，但不具备精确历史发布时间。
- NFP 日期为规则近似，FOMC 期货字段是政策变化代理，不是真正的高频政策意外。
- Daily 新闻指标滞后一个日历日；月度分类指标在月末七天后才进入面板。
- Forward EPS、EPS revisions、CDX、真实历史宽度和指数集中度仍需要授权或人工整理的数据。

生成日期、行数和覆盖范围以 `data_inventory.csv` 及各文件内容为准，不在 README 重复维护。
