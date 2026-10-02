# Organization Notes

Current canonical panels:

- `features/common_research_daily_panel.csv`: base daily panel.
- `features/common_research_daily_panel_enriched.csv`: base panel plus breadth, concentration, FOMC, NFP, and ZQ policy proxy features.
- `features/common_research_daily_panel_full.csv`: enriched panel plus policy uncertainty and geopolitical risk features.

Legacy data moved out of the top-level `data` folder:

- Inflation backtest summaries moved to `data/legacy/inflation_event_backtest`.
- Older monthly Yahoo market files moved to `data/legacy/market_monthly_yahoo`.
- Older monetary-policy-uncertainty research data moved to `data/legacy/mpu_uncertainty`.
- The inflation raw event file used by the current panel is now `data/common_daily/raw/inflation_events_raw.csv`.
