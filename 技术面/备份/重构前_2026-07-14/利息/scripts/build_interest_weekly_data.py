from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

import numpy as np
import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
TECH_ROOT = ROOT.parents[0]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
WEEKLY_DIR = DATA_DIR / "weekly"
META_DIR = DATA_DIR / "metadata"

START_DATE = "1990-01-01"
NY_TZ = "America/New_York"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; investment-interest-weekly/1.0)"}

YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"


@dataclass(frozen=True)
class YahooSpec:
    symbol: str
    alias: str
    group: str
    description: str


@dataclass(frozen=True)
class FredSpec:
    series_id: str
    alias: str
    group: str
    description: str
    native_frequency: str
    expected_history: str


YAHOO_SPECS = [
    YahooSpec("^GSPC", "SPX", "market_index", "S&P 500 price index"),
    YahooSpec("^NDX", "NDX", "market_index", "Nasdaq-100 price index"),
    YahooSpec("SPY", "SPY", "etf_proxy", "SPDR S&P 500 ETF adjusted-price proxy"),
    YahooSpec("QQQ", "QQQ", "etf_proxy", "Invesco QQQ ETF adjusted-price proxy"),
]


FRED_SPECS = [
    FredSpec("DFF", "DFF", "policy_money_market", "Effective federal funds rate", "daily", "30y_plus"),
    FredSpec("FEDFUNDS", "FEDFUNDS", "policy_money_market", "Effective federal funds rate, monthly average", "monthly", "30y_plus"),
    FredSpec("DPRIME", "DPRIME", "policy_money_market", "Bank prime loan rate", "daily", "30y_plus"),
    FredSpec("SOFR", "SOFR", "policy_money_market", "Secured overnight financing rate", "daily", "short_history"),
    FredSpec("DTB3", "DTB3", "policy_money_market", "3-month Treasury bill secondary market rate, discount basis", "daily", "30y_plus"),
    FredSpec("DGS1MO", "DGS1MO", "treasury_curve", "1-month Treasury constant maturity", "daily", "short_history"),
    FredSpec("DGS3MO", "DGS3MO", "treasury_curve", "3-month Treasury constant maturity", "daily", "30y_plus"),
    FredSpec("DGS6MO", "DGS6MO", "treasury_curve", "6-month Treasury constant maturity", "daily", "30y_plus"),
    FredSpec("DGS1", "DGS1", "treasury_curve", "1-year Treasury constant maturity", "daily", "30y_plus"),
    FredSpec("DGS2", "DGS2", "treasury_curve", "2-year Treasury constant maturity", "daily", "30y_plus"),
    FredSpec("DGS3", "DGS3", "treasury_curve", "3-year Treasury constant maturity", "daily", "30y_plus"),
    FredSpec("DGS5", "DGS5", "treasury_curve", "5-year Treasury constant maturity", "daily", "30y_plus"),
    FredSpec("DGS7", "DGS7", "treasury_curve", "7-year Treasury constant maturity", "daily", "30y_plus"),
    FredSpec("DGS10", "DGS10", "treasury_curve", "10-year Treasury constant maturity", "daily", "30y_plus"),
    FredSpec("DGS20", "DGS20", "treasury_curve", "20-year Treasury constant maturity", "daily", "partial_30y"),
    FredSpec("DGS30", "DGS30", "treasury_curve", "30-year Treasury constant maturity", "daily", "30y_plus_with_gap"),
    FredSpec("DFII5", "DFII5", "real_rates_inflation", "5-year TIPS real yield", "daily", "short_history"),
    FredSpec("DFII10", "DFII10", "real_rates_inflation", "10-year TIPS real yield", "daily", "short_history"),
    FredSpec("DFII30", "DFII30", "real_rates_inflation", "30-year TIPS real yield", "daily", "short_history"),
    FredSpec("T5YIE", "T5YIE", "real_rates_inflation", "5-year breakeven inflation rate", "daily", "short_history"),
    FredSpec("T10YIE", "T10YIE", "real_rates_inflation", "10-year breakeven inflation rate", "daily", "short_history"),
    FredSpec("T5YIFR", "T5YIFR", "real_rates_inflation", "5-year, 5-year forward inflation expectation rate", "daily", "short_history"),
    FredSpec("AAA", "AAA", "credit_rates_spreads", "Moody's seasoned Aaa corporate bond yield", "monthly", "30y_plus"),
    FredSpec("BAA", "BAA", "credit_rates_spreads", "Moody's seasoned Baa corporate bond yield", "monthly", "30y_plus"),
    FredSpec("BAMLH0A0HYM2", "HY_OAS", "credit_rates_spreads", "ICE BofA US high yield option-adjusted spread", "daily", "partial_30y"),
    FredSpec("BAMLC0A0CM", "IG_OAS", "credit_rates_spreads", "ICE BofA US corporate option-adjusted spread", "daily", "partial_30y"),
    FredSpec("BAMLC0A4CBBB", "BBB_OAS", "credit_rates_spreads", "ICE BofA BBB US corporate option-adjusted spread", "daily", "partial_30y"),
    FredSpec("MORTGAGE30US", "MORTGAGE30US", "mortgage_rates", "30-year fixed rate mortgage average in the United States", "weekly", "30y_plus"),
    FredSpec("MORTGAGE15US", "MORTGAGE15US", "mortgage_rates", "15-year fixed rate mortgage average in the United States", "weekly", "30y_plus"),
    FredSpec("NFCI", "NFCI", "financial_conditions", "Chicago Fed National Financial Conditions Index", "weekly", "30y_plus"),
    FredSpec("ANFCI", "ANFCI", "financial_conditions", "Adjusted National Financial Conditions Index", "weekly", "30y_plus"),
]


DERIVED_SPREADS = [
    ("yc_10y_2y_pct", "DGS10", "DGS2", "10-year minus 2-year Treasury yield"),
    ("yc_10y_3mo_pct", "DGS10", "DGS3MO", "10-year minus 3-month Treasury yield"),
    ("yc_30y_10y_pct", "DGS30", "DGS10", "30-year minus 10-year Treasury yield"),
    ("yc_5y_2y_pct", "DGS5", "DGS2", "5-year minus 2-year Treasury yield"),
    ("fed_gap_2y_dff_pct", "DGS2", "DFF", "2-year Treasury yield minus effective fed funds rate"),
    ("fed_gap_10y_dff_pct", "DGS10", "DFF", "10-year Treasury yield minus effective fed funds rate"),
    ("bill_gap_3mo_dff_pct", "DGS3MO", "DFF", "3-month Treasury yield minus effective fed funds rate"),
    ("real_10y_nominal_minus_breakeven_pct", "DGS10", "T10YIE", "10-year nominal yield minus 10-year breakeven"),
    ("real_5y_nominal_minus_breakeven_pct", "DGS5", "T5YIE", "5-year nominal yield minus 5-year breakeven"),
    ("credit_baa_aaa_pct", "BAA", "AAA", "Moody Baa minus Aaa corporate yield"),
    ("mortgage30_10y_spread_pct", "MORTGAGE30US", "DGS10", "30-year mortgage rate minus 10-year Treasury yield"),
]

RATE_CHANGE_ALIASES = [
    "DFF",
    "FEDFUNDS",
    "DPRIME",
    "SOFR",
    "DTB3",
    "DGS3MO",
    "DGS2",
    "DGS5",
    "DGS10",
    "DGS30",
    "DFII10",
    "T10YIE",
    "AAA",
    "BAA",
    "HY_OAS",
    "IG_OAS",
    "BBB_OAS",
    "MORTGAGE30US",
]


def ensure_dirs() -> None:
    for path in [RAW_DIR, WEEKLY_DIR, META_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def current_end_date() -> str:
    today = pd.Timestamp.now(tz="America/Los_Angeles").normalize()
    return (today + pd.Timedelta(days=2)).strftime("%Y-%m-%d")


def timestamp_seconds(date_text: str) -> int:
    return int(pd.Timestamp(date_text, tz="UTC").timestamp())


def request_with_retry(url: str, *, params: dict | None = None, attempts: int = 5, timeout: int = 120) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"GET failed after {attempts} attempts: {url}") from last_error


def download_yahoo_symbol(spec: YahooSpec, start: str, end: str) -> pd.DataFrame:
    params = {
        "period1": timestamp_seconds(start),
        "period2": timestamp_seconds(end),
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    url = YAHOO_CHART_URL.format(symbol=quote(spec.symbol, safe=""))
    response = request_with_retry(url, params=params)
    payload = response.json()
    chart = payload.get("chart", {})
    if chart.get("error"):
        raise RuntimeError(f"Yahoo error for {spec.symbol}: {chart['error']}")
    result = (chart.get("result") or [None])[0]
    if not result or not result.get("timestamp"):
        raise RuntimeError(f"No Yahoo data for {spec.symbol}")

    quote_block = result["indicators"]["quote"][0]
    adjclose = result["indicators"].get("adjclose", [{}])[0].get("adjclose") or quote_block.get("close")
    dates = pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_convert(NY_TZ)
    df = pd.DataFrame(
        {
            "date": dates.tz_localize(None).normalize(),
            "symbol": spec.symbol,
            "alias": spec.alias,
            "group": spec.group,
            "description": spec.description,
            "open": quote_block.get("open"),
            "high": quote_block.get("high"),
            "low": quote_block.get("low"),
            "close": quote_block.get("close"),
            "adjclose": adjclose,
            "volume": quote_block.get("volume"),
            "source": "Yahoo Finance chart API",
        }
    )
    return df.dropna(subset=["adjclose"]).drop_duplicates(["date", "alias"]).sort_values("date")


def load_yahoo_from_common_daily(spec: YahooSpec) -> pd.DataFrame:
    path = TECH_ROOT / "data" / "common_daily" / "raw" / "yahoo_ohlcv_daily.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, parse_dates=["date"])
    df = df[df["alias"] == spec.alias].copy()
    if df.empty:
        return df
    df["description"] = spec.description
    df["source"] = df["source"].astype(str) + " via common_daily fallback"
    return df


def download_yahoo_all(start: str, end: str) -> tuple[pd.DataFrame, list[dict]]:
    frames: list[pd.DataFrame] = []
    failures: list[dict] = []
    for spec in YAHOO_SPECS:
        try:
            frames.append(download_yahoo_symbol(spec, start, end))
        except Exception as exc:  # noqa: BLE001
            fallback = load_yahoo_from_common_daily(spec)
            if not fallback.empty:
                frames.append(fallback)
                failures.append(
                    {
                        "source": "yahoo",
                        "id": spec.symbol,
                        "alias": spec.alias,
                        "status": "used_common_daily_fallback",
                        "error": str(exc),
                    }
                )
            else:
                failures.append(
                    {
                        "source": "yahoo",
                        "id": spec.symbol,
                        "alias": spec.alias,
                        "status": "failed",
                        "error": str(exc),
                    }
                )
    if not frames:
        return pd.DataFrame(), failures
    return pd.concat(frames, ignore_index=True).sort_values(["alias", "date"]), failures


def download_fred_series(spec: FredSpec, start: str) -> pd.DataFrame:
    response = request_with_retry(FRED_CSV_URL, params={"id": spec.series_id, "cosd": start})
    df = pd.read_csv(StringIO(response.text))
    if len(df.columns) < 2:
        raise RuntimeError(f"Unexpected FRED CSV for {spec.series_id}")
    date_col = df.columns[0]
    value_col = df.columns[1]
    out = pd.DataFrame(
        {
            "date": pd.to_datetime(df[date_col], errors="coerce"),
            "series_id": spec.series_id,
            "alias": spec.alias,
            "group": spec.group,
            "description": spec.description,
            "native_frequency": spec.native_frequency,
            "expected_history": spec.expected_history,
            "value": pd.to_numeric(df[value_col].replace(".", np.nan), errors="coerce"),
            "source": "FRED fredgraph CSV",
        }
    )
    return out.dropna(subset=["date", "value"]).drop_duplicates(["date", "alias"]).sort_values("date")


def load_fred_from_common_daily(spec: FredSpec) -> pd.DataFrame:
    path = TECH_ROOT / "data" / "common_daily" / "raw" / "fred_series_long.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, parse_dates=["date"])
    df = df[df["alias"] == spec.alias].copy()
    if df.empty:
        return df
    for column, value in {
        "series_id": spec.series_id,
        "group": spec.group,
        "description": spec.description,
        "native_frequency": spec.native_frequency,
        "expected_history": spec.expected_history,
    }.items():
        df[column] = value
    df["source"] = df["source"].astype(str) + " via common_daily fallback"
    return df[["date", "series_id", "alias", "group", "description", "native_frequency", "expected_history", "value", "source"]]


def download_fred_all(start: str) -> tuple[pd.DataFrame, list[dict]]:
    frames: list[pd.DataFrame] = []
    failures: list[dict] = []
    for spec in FRED_SPECS:
        try:
            frames.append(download_fred_series(spec, start))
        except Exception as exc:  # noqa: BLE001
            fallback = load_fred_from_common_daily(spec)
            if not fallback.empty:
                frames.append(fallback)
                failures.append(
                    {
                        "source": "fred",
                        "id": spec.series_id,
                        "alias": spec.alias,
                        "status": "used_common_daily_fallback",
                        "error": str(exc),
                    }
                )
            else:
                failures.append(
                    {
                        "source": "fred",
                        "id": spec.series_id,
                        "alias": spec.alias,
                        "status": "failed",
                        "error": str(exc),
                    }
                )
    if not frames:
        return pd.DataFrame(), failures
    return pd.concat(frames, ignore_index=True).sort_values(["alias", "date"]), failures


def build_market_weekly(yahoo: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if yahoo.empty:
        return pd.DataFrame(), pd.DataFrame()
    rows: list[pd.DataFrame] = []
    for alias, group in yahoo.groupby("alias"):
        group = group.sort_values("date").set_index("date")
        weekly = group.resample("W-FRI").agg(
            {
                "symbol": "last",
                "group": "last",
                "description": "last",
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "adjclose": "last",
                "volume": "sum",
                "source": "last",
            }
        )
        weekly = weekly.dropna(subset=["adjclose"]).reset_index().rename(columns={"date": "week_end"})
        weekly["alias"] = alias
        weekly["return_1w"] = weekly["adjclose"].pct_change(1)
        weekly["return_4w"] = weekly["adjclose"].pct_change(4)
        weekly["return_13w"] = weekly["adjclose"].pct_change(13)
        weekly["return_52w"] = weekly["adjclose"].pct_change(52)
        weekly["log_return_1w"] = np.log(weekly["adjclose"] / weekly["adjclose"].shift(1))
        rows.append(weekly)
    long = pd.concat(rows, ignore_index=True).sort_values(["alias", "week_end"])
    metrics = ["close", "adjclose", "return_1w", "return_4w", "return_13w", "return_52w", "log_return_1w", "volume"]
    wide = long.pivot_table(index="week_end", columns="alias", values=metrics, aggfunc="last")
    wide.columns = [f"{alias}_{metric}" for metric, alias in wide.columns]
    wide = wide.reset_index().sort_values("week_end")
    return long, wide


def latest_completed_friday(max_date: pd.Timestamp) -> pd.Timestamp:
    max_date = pd.Timestamp(max_date).normalize()
    days_since_friday = (max_date.weekday() - 4) % 7
    return max_date - pd.Timedelta(days=days_since_friday)


def ffill_limit_for_frequency(native_frequency: str) -> int:
    limits = {
        "daily": 2,
        "weekly": 2,
        "monthly": 8,
    }
    return limits.get(str(native_frequency).lower(), 4)


def build_rates_weekly(fred: pd.DataFrame, week_index: pd.DatetimeIndex) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if fred.empty:
        return pd.DataFrame(), pd.DataFrame({"week_end": week_index}), pd.DataFrame({"week_end": week_index})
    rows: list[pd.DataFrame] = []
    for alias, group in fred.groupby("alias"):
        group = group.sort_values("date").set_index("date")
        group["last_observation_date"] = group.index
        weekly = group.resample("W-FRI").agg(
            {
                "series_id": "last",
                "group": "last",
                "description": "last",
                "native_frequency": "last",
                "expected_history": "last",
                "value": "last",
                "last_observation_date": "last",
                "source": "last",
            }
        )
        weekly = weekly.dropna(subset=["value"]).reset_index().rename(columns={"date": "week_end"})
        weekly["alias"] = alias
        rows.append(weekly)
    observed = pd.concat(rows, ignore_index=True).sort_values(["alias", "week_end"])

    if len(week_index) == 0:
        week_index = pd.DatetimeIndex(sorted(observed["week_end"].dropna().unique()))

    level_series: dict[str, pd.Series] = {}
    age_series: dict[str, pd.Series] = {}
    for alias, group in observed.groupby("alias"):
        group = group.sort_values("week_end")
        native_frequency = str(group["native_frequency"].dropna().iloc[-1]) if group["native_frequency"].notna().any() else ""
        limit = ffill_limit_for_frequency(native_frequency)
        values = group.set_index("week_end")["value"].sort_index()
        values = values[~values.index.duplicated(keep="last")]
        levels = values.reindex(week_index).ffill(limit=limit)

        obs_week = pd.Series(values.index, index=values.index)
        last_obs_week = obs_week.reindex(week_index).ffill(limit=limit)
        week_as_series = pd.Series(week_index, index=week_index)
        age_weeks = (week_as_series - pd.to_datetime(last_obs_week)).dt.days / 7.0
        age_weeks = age_weeks.where(levels.notna())

        level_series[alias] = levels
        age_series[f"{alias}_age_weeks"] = age_weeks

    wide = pd.DataFrame(level_series, index=week_index).reset_index().rename(columns={"index": "week_end"})
    freshness = pd.DataFrame(age_series, index=week_index).reset_index().rename(columns={"index": "week_end"})
    return observed, wide, freshness


def build_rate_features(rates_wide: pd.DataFrame) -> pd.DataFrame:
    if rates_wide.empty:
        return rates_wide
    features = rates_wide.copy().sort_values("week_end")
    numeric_cols = [col for col in features.columns if col != "week_end"]
    features = features[["week_end"] + numeric_cols]

    for name, left, right, _description in DERIVED_SPREADS:
        if left in features.columns and right in features.columns:
            features[name] = features[left] - features[right]
            features[name.replace("_pct", "_bp")] = features[name] * 100.0

    for spread in ["yc_10y_2y_pct", "yc_10y_3mo_pct"]:
        if spread in features.columns:
            features[spread.replace("_pct", "_inverted_flag")] = (features[spread] < 0).astype("Int64")

    for alias in RATE_CHANGE_ALIASES:
        if alias not in features.columns:
            continue
        for window in [1, 4, 13, 52]:
            features[f"{alias}_chg_bp_{window}w"] = (features[alias] - features[alias].shift(window)) * 100.0
    return features


def write_source_map() -> None:
    rows: list[dict] = []
    for spec in YAHOO_SPECS:
        rows.append(
            {
                "source": "Yahoo Finance chart API",
                "source_id": spec.symbol,
                "alias": spec.alias,
                "group": spec.group,
                "description": spec.description,
                "native_frequency": "daily",
                "expected_history": "primary_30y" if spec.alias in {"SPX", "NDX"} else "proxy_shorter_history",
            }
        )
    for spec in FRED_SPECS:
        rows.append(
            {
                "source": "FRED",
                "source_id": spec.series_id,
                "alias": spec.alias,
                "group": spec.group,
                "description": spec.description,
                "native_frequency": spec.native_frequency,
                "expected_history": spec.expected_history,
            }
        )
    for name, left, right, description in DERIVED_SPREADS:
        rows.append(
            {
                "source": "derived",
                "source_id": f"{left}-{right}",
                "alias": name,
                "group": "derived_spread",
                "description": description,
                "native_frequency": "weekly",
                "expected_history": "depends_on_components",
            }
        )
    pd.DataFrame(rows).to_csv(META_DIR / "source_map.csv", index=False)


def coverage_from_long(df: pd.DataFrame, date_col: str, key_col: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    grouped = df.groupby(key_col, dropna=False)[date_col].agg(["min", "max", "count"]).reset_index()
    grouped["history_years"] = (pd.to_datetime(grouped["max"]) - pd.to_datetime(grouped["min"])).dt.days / 365.25
    return grouped.rename(columns={key_col: "alias", "min": "first_date", "max": "last_date", "count": "observations"})


def write_coverage(yahoo: pd.DataFrame, fred: pd.DataFrame, market_weekly: pd.DataFrame, rates_weekly: pd.DataFrame) -> None:
    market_daily = coverage_from_long(yahoo, "date", "alias")
    if not market_daily.empty:
        market_daily["dataset"] = "market_daily_raw"
    rates_daily = coverage_from_long(fred, "date", "alias")
    if not rates_daily.empty:
        rates_daily["dataset"] = "fred_daily_raw"
    market_week = coverage_from_long(market_weekly, "week_end", "alias")
    if not market_week.empty:
        market_week["dataset"] = "market_weekly"
    rate_week = coverage_from_long(rates_weekly, "week_end", "alias")
    if not rate_week.empty:
        rate_week["dataset"] = "rates_weekly_observed"
    out = pd.concat([market_daily, rates_daily, market_week, rate_week], ignore_index=True)
    source_map = pd.read_csv(META_DIR / "source_map.csv")
    out = out.merge(source_map[["alias", "source_id", "group", "description", "native_frequency", "expected_history"]], on="alias", how="left")
    out["has_30y_history"] = out["history_years"] >= 30.0
    out.to_csv(META_DIR / "series_coverage.csv", index=False)


def inventory_csv(path: Path, note: str = "") -> dict:
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001
        return {
            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "rows": math.nan,
            "columns": math.nan,
            "min_date": "",
            "max_date": "",
            "note": f"read failed: {exc}",
        }
    date_col = next((col for col in ["week_end", "date", "last_observation_date", "first_date"] if col in df.columns), None)
    min_date = ""
    max_date = ""
    if {"first_date", "last_date"}.issubset(df.columns):
        first_dates = pd.to_datetime(df["first_date"], errors="coerce")
        last_dates = pd.to_datetime(df["last_date"], errors="coerce")
        if first_dates.notna().any():
            min_date = first_dates.min().date().isoformat()
        if last_dates.notna().any():
            max_date = last_dates.max().date().isoformat()
    elif date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        if dates.notna().any():
            min_date = dates.min().date().isoformat()
            max_date = dates.max().date().isoformat()
    return {
        "file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "rows": len(df),
        "columns": len(df.columns),
        "min_date": min_date,
        "max_date": max_date,
        "note": note,
    }


def write_inventory() -> None:
    notes = {
        "data/raw/yahoo_index_ohlcv_daily.csv": "Raw daily OHLCV for SPX, NDX, and ETF proxies from Yahoo Finance chart API.",
        "data/raw/fred_interest_daily_long.csv": "Raw FRED interest-rate and rate-adjacent series in long form.",
        "data/weekly/index_prices_weekly_long.csv": "Weekly Friday market bars and returns in long form.",
        "data/weekly/index_prices_weekly.csv": "Weekly market prices and returns in wide form.",
        "data/weekly/interest_rates_weekly_observed.csv": "Weekly last observed value per FRED series, before panel forward-fill.",
        "data/weekly/interest_rates_weekly.csv": "Weekly FRED levels aligned to market week calendar and forward-filled with frequency-specific stale-data limits.",
        "data/weekly/interest_rates_weekly_data_age.csv": "Weeks since each rate series' last real observation after limited forward-fill.",
        "data/weekly/rate_features_weekly.csv": "Weekly rate levels, spreads, inversion flags, and rate-change features.",
        "data/weekly/market_rates_weekly_panel.csv": "Main modeling panel: weekly market data joined to rate features.",
        "data/metadata/source_map.csv": "Data source, IDs, descriptions, and expected-history metadata.",
        "data/metadata/series_coverage.csv": "Observed date coverage and 30-year-history checks.",
        "data/metadata/download_failures.csv": "Download failures and fallback usage, if any.",
    }
    rows = []
    for path in sorted(DATA_DIR.rglob("*.csv")):
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        rows.append(inventory_csv(path, notes.get(rel, "")))
    pd.DataFrame(rows).to_csv(DATA_DIR / "data_inventory.csv", index=False)


def write_readme(end_date: str, failures: list[dict]) -> None:
    failure_note = "无下载失败。"
    if failures:
        failure_note = f"共有 {len(failures)} 条下载失败或回退记录，详见 `data/metadata/download_failures.csv`。"

    text = f"""# 利率对标普500与纳斯达克100影响研究：第一阶段数据准备

生成时间：{datetime.now(timezone.utc).isoformat()} UTC
请求起始日期：{START_DATE}
下载结束参数：{end_date}

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
- {failure_note}

## 复跑

```powershell
python "D:\\drive\\Investment\\技术面\\利息\\scripts\\build_interest_weekly_data.py"
```
"""
    (ROOT / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    end_date = current_end_date()

    yahoo, yahoo_failures = download_yahoo_all(START_DATE, end_date)
    fred, fred_failures = download_fred_all(START_DATE)
    failures = yahoo_failures + fred_failures

    if not yahoo.empty:
        yahoo.to_csv(RAW_DIR / "yahoo_index_ohlcv_daily.csv", index=False)
    if not fred.empty:
        fred.to_csv(RAW_DIR / "fred_interest_daily_long.csv", index=False)

    market_weekly_long, market_weekly_wide = build_market_weekly(yahoo)
    if not market_weekly_wide.empty:
        primary_market = yahoo[yahoo["alias"].isin(["SPX", "NDX"])]
        if not primary_market.empty:
            latest_primary_date = primary_market.groupby("alias")["date"].max().min()
            completed_cutoff = latest_completed_friday(pd.Timestamp(latest_primary_date))
            market_weekly_long = market_weekly_long[market_weekly_long["week_end"] <= completed_cutoff].copy()
            market_weekly_wide = market_weekly_wide[market_weekly_wide["week_end"] <= completed_cutoff].copy()
    market_weekly_long.to_csv(WEEKLY_DIR / "index_prices_weekly_long.csv", index=False)
    market_weekly_wide.to_csv(WEEKLY_DIR / "index_prices_weekly.csv", index=False)

    market_week_index = pd.DatetimeIndex(pd.to_datetime(market_weekly_wide["week_end"])) if not market_weekly_wide.empty else pd.date_range(START_DATE, end_date, freq="W-FRI")
    rates_weekly_observed, rates_weekly_wide, rates_weekly_age = build_rates_weekly(fred, market_week_index)
    rates_weekly_observed.to_csv(WEEKLY_DIR / "interest_rates_weekly_observed.csv", index=False)
    rates_weekly_wide.to_csv(WEEKLY_DIR / "interest_rates_weekly.csv", index=False)
    rates_weekly_age.to_csv(WEEKLY_DIR / "interest_rates_weekly_data_age.csv", index=False)

    rate_features = build_rate_features(rates_weekly_wide)
    rate_features.to_csv(WEEKLY_DIR / "rate_features_weekly.csv", index=False)

    panel = market_weekly_wide.merge(rate_features, on="week_end", how="left")
    panel.to_csv(WEEKLY_DIR / "market_rates_weekly_panel.csv", index=False)

    write_source_map()
    if failures:
        pd.DataFrame(failures).to_csv(META_DIR / "download_failures.csv", index=False)
    else:
        pd.DataFrame(columns=["source", "id", "alias", "status", "error"]).to_csv(META_DIR / "download_failures.csv", index=False)
    write_coverage(yahoo, fred, market_weekly_long, rates_weekly_observed)
    write_inventory()
    write_readme(end_date, failures)

    print(f"Wrote interest weekly data to {ROOT}")
    print(f"Yahoo daily rows: {len(yahoo):,}")
    print(f"FRED rows: {len(fred):,}")
    print(f"Weekly panel rows: {len(panel):,}")
    print(f"Failures/fallbacks: {len(failures):,}")


if __name__ == "__main__":
    main()
