# Data Layout

- `common_daily/`: current canonical research data. Use `common_daily/features/common_research_daily_panel_full.csv` as the broadest daily panel.
- `common_daily/raw/`: downloaded or scraped source data.
- `common_daily/features/`: aligned daily feature files and joined panels.
- `legacy/`: older project-specific datasets and duplicate historical outputs retained for reproducibility.
- `_file_inventory.csv`: generated inventory of files under `data`.

The main panel uses the SPX trading calendar. Some raw data, especially futures and daily news indexes, can have calendar dates that do not appear in the equity-market panel.
