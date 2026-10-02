# Scripts

Run order for the shared research dataset:

1. `01_build_common_daily_data.py` builds the base daily asset, macro, valuation proxy, and inflation-event panel.
2. `02_build_public_supplement_data.py` adds current-constituent breadth proxies, current-holdings concentration proxies, FOMC flags, NFP flags, and ZQ policy-move proxies.
3. `03_build_policy_geopolitical_risk_data.py` adds AI-GPR, daily EPU, and FRED EPU category features, then writes the full panel.
4. `04_refresh_workspace_inventory.py` refreshes file inventories under `data`, `outputs`, and `scripts`.

Legacy one-off research scripts are under `scripts/legacy`.
