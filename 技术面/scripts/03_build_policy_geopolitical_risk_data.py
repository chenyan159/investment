from __future__ import annotations

from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
import time

import numpy as np
import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
COMMON_DIR = ROOT / "data" / "common_daily"
RAW_DIR = COMMON_DIR / "raw"
FEATURE_DIR = COMMON_DIR / "features"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; common-daily-risk-data/1.0)"}
AI_GPR_DAILY_URL = "https://www.matteoiacoviello.com/ai_gpr_files/ai_gpr_data_daily.csv"
AI_GPR_MONTHLY_URL = "https://www.matteoiacoviello.com/ai_gpr_files/ai_gpr_data_monthly.csv"
AI_GPR_EVENTTYPE_URL = "https://www.matteoiacoviello.com/ai_gpr_files/ai_gpr_eventtype_monthly.csv"
EPU_DAILY_URL = "https://www.policyuncertainty.com/media/All_Daily_Policy_Data.csv"
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"

FRED_EPU_SERIES = {
    "USEPUINDXD": "us_epu_daily_fred",
    "USEPUINDXM": "us_epu_monthly_fred",
    "GEPUCURRENT": "global_epu_monthly_current_price",
    "EPUMONETARY": "us_epu_monetary_policy",
    "EPUTRADE": "us_epu_trade_policy",
    "EPUFISCAL": "us_epu_fiscal_policy",
    "EPUHEALTHCARE": "us_epu_healthcare_policy",
}


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)


def get_csv(url: str) -> pd.DataFrame:
    last_error: Exception | None = None
    for attempt in range(1, 5):
        try:
            response = requests.get(url, headers=HEADERS, timeout=60)
            response.raise_for_status()
            return pd.read_csv(StringIO(response.text.lstrip("\ufeff")))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt < 4:
                time.sleep(1.5 * attempt)
    raise RuntimeError(f"GET failed after retries: {url}") from last_error


def download_fred(series_id: str, alias: str) -> pd.DataFrame:
    last_error: Exception | None = None
    response = None
    for attempt in range(1, 5):
        try:
            response = requests.get(FRED_CSV_URL, params={"id": series_id}, headers=HEADERS, timeout=60)
            response.raise_for_status()
            break
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt < 4:
                time.sleep(1.5 * attempt)
    if response is None:
        raise RuntimeError(f"FRED download failed after retries: {series_id}") from last_error
    df = pd.read_csv(StringIO(response.text))
    value_col = df.columns[1]
    df = df.rename(columns={df.columns[0]: "date", value_col: "value"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"].replace(".", np.nan), errors="coerce")
    df = df.dropna(subset=["date", "value"]).sort_values("date")
    df["series_id"] = series_id
    df["alias"] = alias
    df["source"] = "FRED"
    df["source_url"] = f"https://fred.stlouisfed.org/series/{series_id}"
    return df[["date", "series_id", "alias", "value", "source", "source_url"]]


def daily_lagged_features(df: pd.DataFrame, date_col: str, prefix: str, value_cols: list[str], market_dates: pd.Series) -> pd.DataFrame:
    daily_index = pd.date_range(pd.to_datetime(market_dates).min(), pd.to_datetime(market_dates).max(), freq="D")
    values = df.copy()
    values[date_col] = pd.to_datetime(values[date_col], errors="coerce")
    values = values.dropna(subset=[date_col]).set_index(date_col).sort_index()
    values = values.reindex(daily_index)

    out = pd.DataFrame(index=daily_index)
    for col in value_cols:
        if col not in values:
            continue
        series = pd.to_numeric(values[col], errors="coerce")
        lagged = series.shift(1)
        name = f"{prefix}_{col.lower()}_lag1"
        out[name] = lagged
        out[f"{name}_7d_ma"] = lagged.rolling(7, min_periods=3).mean()
        out[f"{name}_21d_ma"] = lagged.rolling(21, min_periods=10).mean()
        out[f"{name}_21d_chg"] = lagged - lagged.shift(21)
        out[f"{name}_252d_z"] = (lagged - lagged.rolling(252, min_periods=120).mean()) / lagged.rolling(
            252, min_periods=120
        ).std()
    out.index.name = "date"
    return out.reindex(pd.to_datetime(market_dates)).reset_index()


def monthly_lagged_features(
    df: pd.DataFrame,
    date_col: str,
    prefix: str,
    value_cols: list[str],
    market_dates: pd.Series,
    lag_days_after_month_end: int = 7,
) -> pd.DataFrame:
    values = df.copy()
    values[date_col] = pd.to_datetime(values[date_col], errors="coerce")
    values = values.dropna(subset=[date_col]).sort_values(date_col)
    values["available_date"] = values[date_col] + pd.offsets.MonthEnd(0) + pd.Timedelta(days=lag_days_after_month_end)
    wide = values.set_index("available_date")[value_cols].apply(pd.to_numeric, errors="coerce").sort_index()
    wide = wide[~wide.index.duplicated(keep="last")]
    out = wide.reindex(pd.to_datetime(market_dates)).ffill()
    out = out.rename(columns={col: f"{prefix}_{col.lower()}_lagged_monthly" for col in out.columns})
    out.index.name = "date"
    return out.reset_index()


def build_policy_geopolitical_features() -> pd.DataFrame:
    panel_path = FEATURE_DIR / "common_research_daily_panel_enriched.csv"
    if not panel_path.exists():
        panel_path = FEATURE_DIR / "common_research_daily_panel.csv"
    base = pd.read_csv(panel_path, parse_dates=["date"], low_memory=False)
    market_dates = base["date"]

    gpr_daily = get_csv(AI_GPR_DAILY_URL)
    gpr_monthly = get_csv(AI_GPR_MONTHLY_URL)
    gpr_eventtype = get_csv(AI_GPR_EVENTTYPE_URL)
    epu_daily = get_csv(EPU_DAILY_URL)

    gpr_daily.to_csv(RAW_DIR / "ai_gpr_daily.csv", index=False)
    gpr_monthly.to_csv(RAW_DIR / "ai_gpr_monthly.csv", index=False)
    gpr_eventtype.to_csv(RAW_DIR / "ai_gpr_eventtype_monthly.csv", index=False)
    epu_daily.to_csv(RAW_DIR / "epu_daily_policyuncertainty.csv", index=False)

    epu_daily["date"] = pd.to_datetime(
        {
            "year": epu_daily["year"],
            "month": epu_daily["month"],
            "day": epu_daily["day"],
        },
        errors="coerce",
    )
    epu_daily = epu_daily.rename(columns={"daily_policy_index": "us_daily_epu"})

    fred_epu = pd.concat(
        [download_fred(series_id, alias) for series_id, alias in FRED_EPU_SERIES.items()],
        ignore_index=True,
    )
    fred_epu.to_csv(RAW_DIR / "fred_epu_policy_uncertainty_long.csv", index=False)
    fred_wide = fred_epu.pivot_table(index="date", columns="alias", values="value", aggfunc="last").reset_index()

    features = pd.DataFrame({"date": market_dates})
    daily_epu_features = daily_lagged_features(epu_daily, "date", "epu", ["us_daily_epu"], market_dates)
    daily_gpr_features = daily_lagged_features(
        gpr_daily,
        "Date",
        "ai_gpr",
        [
            "GPR_AI",
            "GPR_AER",
            "GPR_OIL",
            "GPR_NONOIL",
            "GPR_OIL_MiddleEast",
            "GPR_OIL_Russia",
            "GPR_OIL_USA",
            "GPR_OIL_Venezuela",
        ],
        market_dates,
    )
    gpr_event_features = monthly_lagged_features(
        gpr_eventtype,
        "Date",
        "ai_gpr_event",
        [
            "military_conflict",
            "diplomatic_tension",
            "terrorism",
            "civil_war",
            "nuclear_threat",
            "coup",
            "sanctions",
            "other",
        ],
        market_dates,
    )
    fred_monthly_cols = [
        "us_epu_monthly_fred",
        "global_epu_monthly_current_price",
        "us_epu_monetary_policy",
        "us_epu_trade_policy",
        "us_epu_fiscal_policy",
        "us_epu_healthcare_policy",
    ]
    fred_monthly_features = monthly_lagged_features(
        fred_wide,
        "date",
        "fred_epu",
        [col for col in fred_monthly_cols if col in fred_wide],
        market_dates,
    )
    fred_daily_features = daily_lagged_features(
        fred_wide,
        "date",
        "fred_epu",
        ["us_epu_daily_fred"] if "us_epu_daily_fred" in fred_wide else [],
        market_dates,
    )

    for frame in [daily_epu_features, daily_gpr_features, gpr_event_features, fred_monthly_features, fred_daily_features]:
        features = features.merge(frame, on="date", how="left")

    if "fred_epu_us_epu_trade_policy_lagged_monthly" in features:
        features["trade_policy_uncertainty_high_90p"] = (
            features["fred_epu_us_epu_trade_policy_lagged_monthly"]
            > features["fred_epu_us_epu_trade_policy_lagged_monthly"].rolling(252 * 5, min_periods=252).quantile(0.9)
        ).astype("Int64")
    if "ai_gpr_gpr_ai_lag1_252d_z" in features:
        features["ai_gpr_stress_z_gt_2"] = (features["ai_gpr_gpr_ai_lag1_252d_z"] > 2.0).astype("Int64")

    features.to_csv(FEATURE_DIR / "policy_geopolitical_risk_features.csv", index=False)
    full = base.merge(features, on="date", how="left")
    full.to_csv(FEATURE_DIR / "common_research_daily_panel_full.csv", index=False)
    return features


def update_unresolved() -> None:
    path = COMMON_DIR / "unresolved_data_requirements.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    mask = df["variable"].astype(str).str.contains("fiscal/tariff/geopolitical", case=False, na=False)
    if mask.any():
        df.loc[mask, "status"] = "partial_done"
        df.loc[
            mask,
            "available_proxy",
        ] = "Daily AI-GPR, GPR event-type monthly, daily US EPU, monthly trade/fiscal/monetary/healthcare EPU indexes."
        df.loc[
            mask,
            "remaining_gap",
        ] = "Still needs hand-vetted event labels for specific tariff, fiscal, and geopolitical shocks if causal event studies require exact announcement timestamps."
    df.to_csv(path, index=False)


def update_inventory() -> None:
    rows = []
    for path in sorted(COMMON_DIR.rglob("*.csv")):
        try:
            df = pd.read_csv(path, nrows=5)
            full_rows = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore")) - 1
            date_col = "date" if "date" in df.columns else "Date" if "Date" in df.columns else "event_date" if "event_date" in df.columns else None
            if date_col:
                full = pd.read_csv(path, usecols=[date_col])
                dates = pd.to_datetime(full[date_col], errors="coerce")
                min_date = dates.min()
                max_date = dates.max()
            else:
                min_date = pd.NaT
                max_date = pd.NaT
            rows.append(
                {
                    "file": str(path.relative_to(ROOT)),
                    "rows": max(full_rows, 0),
                    "columns": len(df.columns),
                    "min_date": "" if pd.isna(min_date) else min_date.strftime("%Y-%m-%d"),
                    "max_date": "" if pd.isna(max_date) else max_date.strftime("%Y-%m-%d"),
                }
            )
        except Exception as exc:  # noqa: BLE001
            rows.append({"file": str(path.relative_to(ROOT)), "rows": "", "columns": "", "min_date": "", "max_date": "", "note": str(exc)})
    pd.DataFrame(rows).to_csv(COMMON_DIR / "data_inventory.csv", index=False)


def update_readme() -> None:
    readme = COMMON_DIR / "README.md"
    existing = readme.read_text(encoding="utf-8") if readme.exists() else "# Common Daily Research Data\n"
    marker = "## Policy And Geopolitical Risk Supplement\n"
    supplement = f"""{marker}
Generated at: {datetime.now(timezone.utc).isoformat()}

Additional files:
- raw/ai_gpr_daily.csv: AI-GPR daily geopolitical risk indexes, 1960-present.
- raw/ai_gpr_eventtype_monthly.csv: AI-GPR monthly event-type decomposition.
- raw/epu_daily_policyuncertainty.csv: daily US Economic Policy Uncertainty index.
- raw/fred_epu_policy_uncertainty_long.csv: FRED EPU category indexes, including trade, fiscal, monetary, healthcare, US monthly, US daily, and global monthly EPU.
- features/policy_geopolitical_risk_features.csv: lagged daily/monthly EPU and GPR features aligned to the SPX trading calendar.
- features/common_research_daily_panel_full.csv: enriched panel plus policy/geopolitical risk features.

Point-in-time rule:
- Daily news indexes are lagged one calendar day before joining to market dates.
- Monthly category indexes are made available seven calendar days after month end, then forward-filled.
"""
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + "\n\n" + supplement
    else:
        existing = existing.rstrip() + "\n\n" + supplement
    readme.write_text(existing, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    features = build_policy_geopolitical_features()
    update_unresolved()
    update_inventory()
    update_readme()
    print(f"Wrote policy/geopolitical features: {FEATURE_DIR / 'policy_geopolitical_risk_features.csv'}")
    print(f"Rows: {len(features):,}; columns: {len(features.columns):,}")
    print(f"Wrote full panel: {FEATURE_DIR / 'common_research_daily_panel_full.csv'}")


if __name__ == "__main__":
    main()
