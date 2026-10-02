# Scripts

当前共享研究数据的运行顺序：

1. `01_build_common_daily_data.py` builds the base daily asset, macro, valuation proxy, and inflation-event panel.
2. `02_build_public_supplement_data.py` adds current-constituent breadth proxies, current-holdings concentration proxies, FOMC flags, NFP flags, and ZQ policy-move proxies.
3. `03_build_policy_geopolitical_risk_data.py` adds AI-GPR, daily EPU, and FRED EPU category features, then writes the full panel.
4. `04_refresh_workspace_inventory.py` refreshes file inventories under `data` and `scripts`.

旧的一次性研究脚本已移入 `../备份/重构前_2026-07-14/scripts/legacy/`，不作为当前因子研究入口。`02_build_public_supplement_data.py` 中依赖缺失临时 CSV 的 ZQ 代理不能视为完整有效特征；运行前必须复核其输入和生成列。
