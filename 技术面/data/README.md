# Data Layout

- `common_daily/`：当前可复用的日频研究数据。
- `common_daily/features/common_research_daily_panel_full.csv`：现有覆盖最广的日频面板。
- `common_daily/raw/`：下载或采集的源数据快照。
- `common_daily/features/`：对齐后的特征文件与合并面板。

旧项目数据、重复历史输出和迁移前清单已移入 `../备份/重构前_2026-07-14/`，不作为当前因子研究的默认输入。

主面板使用 SPX 交易日历。期货、周末新闻和宏观事件可能落在非股票交易日；任何研究都必须按真实公开时间映射到下一个可交易时点。现有估值、宏观修订值、当前成分股宽度和集中度代理仍有 point-in-time 限制，使用前须阅读 `common_daily/README.md` 与 unresolved data requirements。
