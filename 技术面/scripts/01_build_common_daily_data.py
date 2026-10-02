from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "common_daily"
RAW_DIR = DATA_DIR / "raw"
FEATURE_DIR = DATA_DIR / "features"

START_DATE = "1990-01-01"
NY_TZ = "America/New_York"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; common-daily-data/1.0)"}

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
    release_lag_days: int = 0


YAHOO_SPECS = [
    YahooSpec("^GSPC", "SPX", "asset", "S&P 500 price index"),
    YahooSpec("SPY", "SPY", "asset", "SPDR S&P 500 ETF"),
    YahooSpec("^NDX", "NDX", "asset", "Nasdaq-100 price index"),
    YahooSpec("QQQ", "QQQ", "asset", "Invesco QQQ ETF"),
    YahooSpec("^SOX", "SOX", "asset", "PHLX Semiconductor index"),
    YahooSpec("SMH", "SMH", "asset", "VanEck Semiconductor ETF"),
    YahooSpec("SOXX", "SOXX", "asset", "iShares Semiconductor ETF"),
    YahooSpec("RSP", "RSP", "asset", "Invesco S&P 500 Equal Weight ETF"),
    YahooSpec("HYG", "HYG", "asset", "iShares High Yield Corporate Bond ETF"),
    YahooSpec("LQD", "LQD", "asset", "iShares Investment Grade Corporate Bond ETF"),
    YahooSpec("TLT", "TLT", "asset", "iShares 20+ Year Treasury Bond ETF"),
    YahooSpec("IEF", "IEF", "asset", "iShares 7-10 Year Treasury Bond ETF"),
    YahooSpec("SHY", "SHY", "asset", "iShares 1-3 Year Treasury Bond ETF"),
    YahooSpec("CL=F", "WTI_FUT", "commodity", "NYMEX WTI crude oil futures"),
    YahooSpec("BZ=F", "BRENT_FUT", "commodity", "ICE Brent crude oil futures"),
    YahooSpec("RB=F", "RBOB_GASOLINE_FUT", "commodity", "NYMEX RBOB gasoline futures"),
    YahooSpec("USO", "USO", "commodity", "United States Oil Fund"),
    YahooSpec("BNO", "BNO", "commodity", "United States Brent Oil Fund"),
    YahooSpec("UGA", "UGA", "commodity", "United States Gasoline Fund"),
    YahooSpec("^VIX", "VIX", "volatility", "CBOE VIX index"),
    YahooSpec("^VIX9D", "VIX9D", "volatility", "CBOE 9-day volatility index"),
    YahooSpec("^VIX3M", "VIX3M", "volatility", "CBOE 3-month volatility index"),
    YahooSpec("^VVIX", "VVIX", "volatility", "CBOE VVIX index"),
    YahooSpec("^SKEW", "SKEW", "volatility", "CBOE SKEW index"),
    YahooSpec("AAPL", "AAPL", "mag7", "Apple"),
    YahooSpec("MSFT", "MSFT", "mag7", "Microsoft"),
    YahooSpec("AMZN", "AMZN", "mag7", "Amazon"),
    YahooSpec("GOOGL", "GOOGL", "mag7", "Alphabet Class A"),
    YahooSpec("META", "META", "mag7", "Meta Platforms"),
    YahooSpec("NVDA", "NVDA", "mag7", "Nvidia"),
    YahooSpec("TSLA", "TSLA", "mag7", "Tesla"),
]


FRED_SPECS = [
    FredSpec("SP500", "FRED_SP500", "asset", "S&P 500 index from FRED"),
    FredSpec("DGS10", "DGS10", "rates", "10-year Treasury constant maturity"),
    FredSpec("DGS2", "DGS2", "rates", "2-year Treasury constant maturity"),
    FredSpec("DGS3MO", "DGS3MO", "rates", "3-month Treasury constant maturity"),
    FredSpec("DFII10", "DFII10", "rates", "10-year TIPS real yield"),
    FredSpec("T10YIE", "T10YIE", "rates", "10-year breakeven inflation rate"),
    FredSpec("T10Y2Y", "T10Y2Y", "rates", "10-year minus 2-year Treasury spread"),
    FredSpec("T10Y3M", "T10Y3M", "rates", "10-year minus 3-month Treasury spread"),
    FredSpec("DFF", "DFF", "rates", "Effective federal funds rate"),
    FredSpec("SOFR", "SOFR", "rates", "Secured overnight financing rate"),
    FredSpec("VIXCLS", "FRED_VIX", "volatility", "CBOE VIX from FRED"),
    FredSpec("VXVCLS", "FRED_VIX3M", "volatility", "CBOE 3-month volatility from FRED"),
    FredSpec("BAMLH0A0HYM2", "HY_OAS", "credit", "ICE BofA US high yield OAS"),
    FredSpec("BAMLC0A0CM", "IG_OAS", "credit", "ICE BofA US corporate OAS"),
    FredSpec("BAMLC0A4CBBB", "BBB_OAS", "credit", "ICE BofA BBB US corporate OAS"),
    FredSpec("DCOILWTICO", "WTI_SPOT", "commodity", "WTI crude oil spot price"),
    FredSpec("DCOILBRENTEU", "BRENT_SPOT", "commodity", "Brent crude oil spot price"),
    FredSpec("GASREGW", "US_REG_GASOLINE", "commodity", "US regular gasoline retail price", 7),
    FredSpec("WALCL", "FED_BALANCE_SHEET", "liquidity", "Federal Reserve total assets", 2),
    FredSpec("WTREGEN", "TGA", "liquidity", "Treasury General Account", 2),
    FredSpec("RRPONTSYD", "RRP", "liquidity", "Overnight reverse repo agreements"),
    FredSpec("NFCI", "NFCI", "liquidity", "Chicago Fed National Financial Conditions Index", 5),
    FredSpec("ANFCI", "ANFCI", "liquidity", "Adjusted National Financial Conditions Index", 5),
    FredSpec("CPIAUCSL", "CPI", "macro", "Consumer price index", 45),
    FredSpec("PCEPI", "PCE_PRICE_INDEX", "macro", "PCE price index", 60),
    FredSpec("PAYEMS", "NONFARM_PAYROLLS", "macro", "Total nonfarm payrolls", 35),
    FredSpec("UNRATE", "UNRATE", "macro", "Unemployment rate", 35),
]


MULTPL_SPECS = [
    {
        "metric": "sp500_trailing_pe",
        "url": "https://www.multpl.com/s-p-500-pe-ratio/table/by-month",
        "frequency": "monthly",
        "lag_days": 45,
    },
    {
        "metric": "sp500_earnings_yield",
        "url": "https://www.multpl.com/s-p-500-earnings-yield/table/by-month",
        "frequency": "monthly",
        "lag_days": 45,
    },
    {
        "metric": "sp500_shiller_pe",
        "url": "https://www.multpl.com/shiller-pe/table/by-month",
        "frequency": "monthly",
        "lag_days": 45,
    },
    {
        "metric": "sp500_price_to_sales",
        "url": "https://www.multpl.com/s-p-500-price-to-sales/table/by-quarter",
        "frequency": "quarterly",
        "lag_days": 60,
    },
]


def ensure_dirs() -> None:
    for path in [DATA_DIR, RAW_DIR, FEATURE_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def request_with_retry(url: str, *, params: dict | None = None, attempts: int = 4) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=60)
            response.raise_for_status()
            return response
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"GET failed after {attempts} attempts: {url}") from last_error


def timestamp_seconds(date_text: str) -> int:
    return int(pd.Timestamp(date_text, tz="UTC").timestamp())


def current_end_date() -> str:
    today = pd.Timestamp.now(tz="America/Los_Angeles").normalize()
    return (today + pd.Timedelta(days=2)).strftime("%Y-%m-%d")


def download_yahoo_symbol(spec: YahooSpec, start: str, end: str) -> pd.DataFrame:
    params = {
        "period1": timestamp_seconds(start),
        "period2": timestamp_seconds(end),
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    response = request_with_retry(YAHOO_CHART_URL.format(symbol=spec.symbol), params=params)
    payload = response.json()
    chart = payload.get("chart", {})
    if chart.get("error"):
        raise RuntimeError(f"Yahoo error for {spec.symbol}: {chart['error']}")
    result = (chart.get("result") or [None])[0]
    if not result or not result.get("timestamp"):
        raise RuntimeError(f"No Yahoo data for {spec.symbol}")

    quote = result["indicators"]["quote"][0]
    adjclose = result["indicators"].get("adjclose", [{}])[0].get("adjclose") or quote["close"]
    dates = pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_convert(NY_TZ)
    df = pd.DataFrame(
        {
            "date": dates.tz_localize(None).normalize(),
            "symbol": spec.symbol,
            "alias": spec.alias,
            "group": spec.group,
            "open": quote.get("open"),
            "high": quote.get("high"),
            "low": quote.get("low"),
            "close": quote.get("close"),
            "adjclose": adjclose,
            "volume": quote.get("volume"),
            "source": "Yahoo Finance chart API",
        }
    )
    return df.dropna(subset=["adjclose"]).drop_duplicates(["date", "alias"]).sort_values("date")


def download_yahoo_all(start: str, end: str) -> tuple[pd.DataFrame, list[dict]]:
    frames: list[pd.DataFrame] = []
    failures: list[dict] = []
    for spec in YAHOO_SPECS:
        try:
            frames.append(download_yahoo_symbol(spec, start, end))
        except Exception as exc:  # noqa: BLE001
            failures.append(
                {
                    "source": "yahoo",
                    "id": spec.symbol,
                    "alias": spec.alias,
                    "reason": str(exc),
                }
            )
        time.sleep(0.2)
    if not frames:
        return pd.DataFrame(), failures
    return pd.concat(frames, ignore_index=True), failures


def download_fred_series(spec: FredSpec, start: str) -> pd.DataFrame:
    response = request_with_retry(FRED_CSV_URL, params={"id": spec.series_id, "cosd": start})
    df = pd.read_csv(StringIO(response.text))
    if len(df.columns) < 2:
        raise RuntimeError(f"Unexpected FRED CSV for {spec.series_id}")
    value_col = df.columns[1]
    df = df.rename(columns={df.columns[0]: "date", value_col: "value"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"].replace(".", np.nan), errors="coerce")
    df = df.dropna(subset=["date", "value"]).sort_values("date")
    df["series_id"] = spec.series_id
    df["alias"] = spec.alias
    df["group"] = spec.group
    df["description"] = spec.description
    df["release_lag_days"] = spec.release_lag_days
    df["source"] = "FRED"
    return df[["date", "series_id", "alias", "group", "description", "release_lag_days", "value", "source"]]


def download_fred_all(start: str) -> tuple[pd.DataFrame, list[dict]]:
    frames: list[pd.DataFrame] = []
    failures: list[dict] = []
    for spec in FRED_SPECS:
        try:
            frames.append(download_fred_series(spec, start))
        except Exception as exc:  # noqa: BLE001
            failures.append(
                {
                    "source": "fred",
                    "id": spec.series_id,
                    "alias": spec.alias,
                    "reason": str(exc),
                }
            )
        time.sleep(0.2)
    if not frames:
        return pd.DataFrame(), failures
    return pd.concat(frames, ignore_index=True), failures


def parse_float(text: str) -> float:
    cleaned = re.sub(r"[^0-9.\-]", "", text)
    if cleaned in {"", ".", "-", "-."}:
        return math.nan
    return float(cleaned)


def scrape_multpl_table(spec: dict) -> pd.DataFrame:
    response = request_with_retry(spec["url"])
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table is None:
        raise RuntimeError(f"No table found at {spec['url']}")

    rows: list[dict] = []
    for tr in table.find_all("tr"):
        cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["td", "th"])]
        if len(cells) < 2 or cells[0].lower() == "date":
            continue
        date_value = pd.to_datetime(cells[0], errors="coerce")
        value = parse_float(cells[1])
        if pd.notna(date_value) and pd.notna(value):
            rows.append(
                {
                    "date": date_value.normalize(),
                    "metric": spec["metric"],
                    "value": value,
                    "frequency": spec["frequency"],
                    "availability_lag_days": spec["lag_days"],
                    "available_date": (date_value + pd.Timedelta(days=spec["lag_days"])).normalize(),
                    "source_url": spec["url"],
                    "source": "Multpl",
                    "lag_note": "Conservative lag from table date; use licensed point-in-time data for production.",
                }
            )
    return pd.DataFrame(rows).sort_values(["metric", "date"])


def scrape_multpl_all() -> tuple[pd.DataFrame, list[dict]]:
    frames: list[pd.DataFrame] = []
    failures: list[dict] = []
    for spec in MULTPL_SPECS:
        try:
            frames.append(scrape_multpl_table(spec))
        except Exception as exc:  # noqa: BLE001
            failures.append(
                {
                    "source": "multpl",
                    "id": spec["metric"],
                    "alias": spec["metric"],
                    "reason": str(exc),
                }
            )
        time.sleep(0.3)
    if not frames:
        return pd.DataFrame(), failures
    return pd.concat(frames, ignore_index=True), failures


def rolling_days_since_low(series: pd.Series, window: int = 252) -> pd.Series:
    values = series.to_numpy(dtype=float)
    result = np.full(len(values), np.nan)
    for idx in range(len(values)):
        start = max(0, idx - window + 1)
        sample = values[start : idx + 1]
        valid = np.where(~np.isnan(sample))[0]
        if valid.size == 0:
            continue
        local = valid[np.nanargmin(sample[valid])]
        result[idx] = idx - (start + local)
    return pd.Series(result, index=series.index)


def build_market_features(yahoo: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    adjclose = (
        yahoo.pivot_table(index="date", columns="alias", values="adjclose", aggfunc="last")
        .sort_index()
        .rename_axis(None, axis=1)
    )
    if "SPX" in adjclose.columns:
        adjclose = adjclose.loc[adjclose["SPX"].notna()]
    elif "SPY" in adjclose.columns:
        adjclose = adjclose.loc[adjclose["SPY"].notna()]

    horizons = [1, 5, 21, 63, 126, 252]
    feature_cols: dict[str, pd.Series] = {}
    for alias in adjclose.columns:
        series = adjclose[alias]
        feature_cols[f"{alias}_adjclose"] = series
        for horizon in horizons:
            feature_cols[f"{alias}_ret_{horizon}d"] = series.pct_change(horizon)
        daily_return = series.pct_change()
        feature_cols[f"{alias}_rv_21d_ann"] = daily_return.rolling(21).std() * math.sqrt(252)
        feature_cols[f"{alias}_rv_63d_ann"] = daily_return.rolling(63).std() * math.sqrt(252)
        rolling_high = series.rolling(252, min_periods=20).max()
        rolling_low = series.rolling(252, min_periods=20).min()
        feature_cols[f"{alias}_dd_from_252d_high"] = series / rolling_high - 1.0
        feature_cols[f"{alias}_rebound_from_252d_low"] = series / rolling_low - 1.0
        feature_cols[f"{alias}_days_since_252d_low"] = rolling_days_since_low(series, 252)
        feature_cols[f"{alias}_dd_from_ath"] = series / series.cummax() - 1.0

    ratio_specs = {
        "RSP_SPY_ratio": ("RSP", "SPY"),
        "QQQ_RSP_ratio": ("QQQ", "RSP"),
        "NDX_SPX_ratio": ("NDX", "SPX"),
        "SOX_SPX_ratio": ("SOX", "SPX"),
        "SMH_SPY_ratio": ("SMH", "SPY"),
        "SOXX_SPY_ratio": ("SOXX", "SPY"),
        "HYG_LQD_ratio": ("HYG", "LQD"),
        "HYG_IEF_ratio": ("HYG", "IEF"),
        "HYG_TLT_ratio": ("HYG", "TLT"),
        "TLT_SPY_ratio": ("TLT", "SPY"),
        "WTI_BRENT_ratio": ("WTI_FUT", "BRENT_FUT"),
    }
    for name, (left, right) in ratio_specs.items():
        if left in adjclose.columns and right in adjclose.columns:
            ratio = adjclose[left] / adjclose[right]
            feature_cols[name] = ratio
            feature_cols[f"{name}_ret_21d"] = ratio.pct_change(21)
            feature_cols[f"{name}_ret_63d"] = ratio.pct_change(63)

    mag7 = [alias for alias in ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "TSLA"] if alias in adjclose]
    if mag7:
        mag7_returns = adjclose[mag7].pct_change()
        eq_return = mag7_returns.mean(axis=1, skipna=True)
        feature_cols["MAG7_equal_weight_ret_1d"] = eq_return
        feature_cols["MAG7_equal_weight_index"] = (1.0 + eq_return.fillna(0.0)).cumprod() * 100.0
        if "SPY" in adjclose:
            mag7_index = feature_cols["MAG7_equal_weight_index"]
            feature_cols["MAG7_equal_weight_minus_SPY_ret_21d"] = mag7_index.pct_change(21) - adjclose["SPY"].pct_change(21)

    features = pd.DataFrame(feature_cols, index=adjclose.index)
    return adjclose, features.reset_index().rename(columns={"index": "date"})


def build_macro_features(fred: pd.DataFrame, market_dates: pd.DatetimeIndex) -> pd.DataFrame:
    if fred.empty:
        return pd.DataFrame({"date": market_dates})

    lagged = fred.copy()
    lagged["available_date"] = lagged["date"] + pd.to_timedelta(lagged["release_lag_days"], unit="D")
    lagged["available_date"] = pd.to_datetime(lagged["available_date"]).dt.normalize()
    wide = lagged.pivot_table(index="available_date", columns="alias", values="value", aggfunc="last").sort_index()
    wide = wide.reindex(market_dates).ffill()

    features = pd.DataFrame(index=market_dates)
    for col in wide.columns:
        features[col] = wide[col]

    if {"DGS10", "DGS2"}.issubset(wide.columns):
        features["yield_curve_10y_2y_calc"] = wide["DGS10"] - wide["DGS2"]
    if {"DGS10", "DGS3MO"}.issubset(wide.columns):
        features["yield_curve_10y_3m_calc"] = wide["DGS10"] - wide["DGS3MO"]
    for col in ["DGS10", "DGS2", "DFII10", "T10YIE"]:
        if col in wide.columns:
            features[f"{col}_chg_5d"] = wide[col] - wide[col].shift(5)
            features[f"{col}_chg_21d"] = wide[col] - wide[col].shift(21)
    if {"HY_OAS", "IG_OAS"}.issubset(wide.columns):
        features["HY_minus_IG_OAS"] = wide["HY_OAS"] - wide["IG_OAS"]
    if {"HY_OAS", "BBB_OAS"}.issubset(wide.columns):
        features["HY_minus_BBB_OAS"] = wide["HY_OAS"] - wide["BBB_OAS"]
    if {"WTI_SPOT", "BRENT_SPOT"}.issubset(wide.columns):
        features["WTI_BRENT_spot_ratio"] = wide["WTI_SPOT"] / wide["BRENT_SPOT"]
    if {"sp500_earnings_yield", "DGS10"}.issubset(wide.columns):
        features["ERP_trailing_proxy"] = wide["sp500_earnings_yield"] - wide["DGS10"]

    return features.reset_index().rename(columns={"index": "date"})


def build_valuation_daily(multpl: pd.DataFrame, market_dates: pd.DatetimeIndex) -> pd.DataFrame:
    if multpl.empty:
        return pd.DataFrame({"date": market_dates})
    df = multpl.copy()
    wide = df.pivot_table(index="available_date", columns="metric", values="value", aggfunc="last").sort_index()
    daily = wide.reindex(market_dates).ffill()
    if "sp500_earnings_yield" in daily.columns:
        # Multpl stores percent values as percent points.
        daily["sp500_earnings_yield_pct"] = daily["sp500_earnings_yield"] / 100.0
    return daily.reset_index().rename(columns={"index": "date"})


def build_event_flags(market_dates: pd.DatetimeIndex) -> pd.DataFrame:
    path = ROOT / "data" / "common_daily" / "raw" / "inflation_events_raw.csv"
    if not path.exists():
        path = ROOT / "data" / "legacy" / "inflation_event_backtest" / "inflation_events_raw.csv"
    flags = pd.DataFrame({"date": market_dates})
    if not path.exists():
        return flags

    events = pd.read_csv(path)
    if "release_date" not in events:
        return flags
    events["date"] = pd.to_datetime(events["release_date"], errors="coerce")
    events = events.dropna(subset=["date"])
    events["date"] = events["date"].dt.normalize()
    events["indicator_lower"] = events["indicator"].astype(str).str.lower()
    events["is_cpi"] = events["indicator_lower"].str.contains("cpi")
    events["is_pce"] = events["indicator_lower"].str.contains("pce")
    events["is_hot"] = events["surprise_bucket"].astype(str).str.lower().eq("hot")
    events["is_cool"] = events["surprise_bucket"].astype(str).str.lower().eq("cool")

    grouped = events.groupby("date").agg(
        inflation_event_count=("indicator", "size"),
        cpi_event_count=("is_cpi", "sum"),
        pce_event_count=("is_pce", "sum"),
        hot_surprise_count=("is_hot", "sum"),
        cool_surprise_count=("is_cool", "sum"),
        mean_surprise_pp=("surprise_pp", "mean"),
        max_abs_surprise_pp=("surprise_pp", lambda x: pd.to_numeric(x, errors="coerce").abs().max()),
    )
    grouped["has_inflation_event"] = 1
    result = flags.merge(grouped.reset_index(), on="date", how="left")
    count_cols = [
        "inflation_event_count",
        "cpi_event_count",
        "pce_event_count",
        "hot_surprise_count",
        "cool_surprise_count",
        "has_inflation_event",
    ]
    for col in count_cols:
        result[col] = result[col].fillna(0).astype(int)
    return result


def write_symbol_map() -> None:
    rows = [
        {
            "source": "Yahoo Finance",
            "source_id": spec.symbol,
            "alias": spec.alias,
            "group": spec.group,
            "description": spec.description,
        }
        for spec in YAHOO_SPECS
    ]
    rows.extend(
        {
            "source": "FRED",
            "source_id": spec.series_id,
            "alias": spec.alias,
            "group": spec.group,
            "description": spec.description,
        }
        for spec in FRED_SPECS
    )
    pd.DataFrame(rows).to_csv(DATA_DIR / "source_symbol_map.csv", index=False)


def write_unresolved_requirements(failures: list[dict]) -> None:
    rows = [
        {
            "variable_group": "valuation",
            "variable": "forward PE",
            "status": "not_done",
            "reason": "Requires licensed point-in-time consensus data.",
            "likely_source": "FactSet, IBES, Bloomberg, LSEG, S&P Capital IQ",
        },
        {
            "variable_group": "valuation",
            "variable": "EV/Sales",
            "status": "not_done",
            "reason": "Historical index-level EV/Sales is not available from the public sources used here.",
            "likely_source": "FactSet, Bloomberg, S&P Capital IQ",
        },
        {
            "variable_group": "earnings",
            "variable": "forward EPS",
            "status": "not_done",
            "reason": "Requires point-in-time consensus EPS history.",
            "likely_source": "FactSet, IBES, Bloomberg, LSEG",
        },
        {
            "variable_group": "earnings",
            "variable": "EPS revision",
            "status": "not_done",
            "reason": "Requires analyst estimate history and point-in-time revision stamps.",
            "likely_source": "FactSet, IBES, Bloomberg, LSEG",
        },
        {
            "variable_group": "earnings",
            "variable": "earnings growth expectation",
            "status": "not_done",
            "reason": "Requires point-in-time consensus growth expectations.",
            "likely_source": "FactSet, IBES, Bloomberg, LSEG",
        },
        {
            "variable_group": "earnings",
            "variable": "Mag 7 EPS contribution",
            "status": "not_done",
            "reason": "Requires point-in-time index EPS contribution or constituent-level estimates and weights.",
            "likely_source": "FactSet, Bloomberg, S&P Capital IQ",
        },
        {
            "variable_group": "credit",
            "variable": "CDX",
            "status": "not_done",
            "reason": "CDX history is not available from the public sources used here.",
            "likely_source": "Markit/IHS, Bloomberg, LSEG",
        },
        {
            "variable_group": "market breadth",
            "variable": "advance-decline",
            "status": "not_done",
            "reason": "Requires exchange breadth feed or vendor breadth history.",
            "likely_source": "NYSE/Nasdaq data, Bloomberg, Refinitiv, StockCharts",
        },
        {
            "variable_group": "market breadth",
            "variable": "% above 20/50/200dma for S&P 500 members",
            "status": "not_done",
            "reason": "Requires point-in-time constituent membership and constituent price histories.",
            "likely_source": "CRSP/Compustat, Bloomberg, FactSet, Norgate",
        },
        {
            "variable_group": "concentration",
            "variable": "Top 10 weight",
            "status": "not_done",
            "reason": "Requires point-in-time S&P 500 constituent weights.",
            "likely_source": "S&P Dow Jones Indices, FactSet, Bloomberg",
        },
        {
            "variable_group": "macro events",
            "variable": "NFP release surprise calendar",
            "status": "not_done",
            "reason": "Release dates and survey surprises need an economic-calendar vendor feed.",
            "likely_source": "Bloomberg ECO, Econoday, Investing.com, Refinitiv",
        },
        {
            "variable_group": "macro events",
            "variable": "FOMC policy surprise calendar",
            "status": "not_done",
            "reason": "Meeting dates are public, but surprise needs futures/OIS-implied expectations.",
            "likely_source": "Fed, CME FedWatch, Bloomberg, high-frequency futures data",
        },
        {
            "variable_group": "macro events",
            "variable": "fiscal/tariff/geopolitical event labels",
            "status": "not_done",
            "reason": "Requires manual taxonomy or a curated news/event database.",
            "likely_source": "GDELT, RavenPack, Bloomberg News, manual event file",
        },
    ]
    for failure in failures:
        rows.append(
            {
                "variable_group": f"download_failure:{failure.get('source')}",
                "variable": failure.get("id"),
                "status": "failed",
                "reason": failure.get("reason"),
                "likely_source": failure.get("source"),
            }
        )
    pd.DataFrame(rows).to_csv(DATA_DIR / "unresolved_data_requirements.csv", index=False)


def inventory_csv(path: Path, note: str = "") -> dict:
    try:
        df = pd.read_csv(path)
    except Exception as exc:  # noqa: BLE001
        return {
            "file": str(path.relative_to(ROOT)),
            "rows": np.nan,
            "columns": np.nan,
            "min_date": "",
            "max_date": "",
            "note": f"Could not read: {exc}",
        }
    date_col = "date" if "date" in df.columns else None
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        min_date = dates.min()
        max_date = dates.max()
    else:
        min_date = pd.NaT
        max_date = pd.NaT
    return {
        "file": str(path.relative_to(ROOT)),
        "rows": len(df),
        "columns": len(df.columns),
        "min_date": "" if pd.isna(min_date) else min_date.strftime("%Y-%m-%d"),
        "max_date": "" if pd.isna(max_date) else max_date.strftime("%Y-%m-%d"),
        "note": note,
    }


def write_inventory() -> None:
    notes = {
        "data/common_daily/raw/yahoo_ohlcv_daily.csv": "Raw daily OHLCV from Yahoo Finance chart API.",
        "data/common_daily/raw/yahoo_adjclose_wide.csv": "Wide adjusted close matrix by alias.",
        "data/common_daily/raw/fred_series_long.csv": "Raw FRED observations. Weekly/monthly series are not point-in-time unless lagged in features.",
        "data/common_daily/raw/multpl_valuation_raw.csv": "Public valuation proxy scraped from Multpl; use licensed data for production point-in-time tests.",
        "data/common_daily/features/market_momentum_features.csv": "Daily returns, realized vol, drawdown/rebound, ratios, Mag7 equal-weight proxy.",
        "data/common_daily/features/macro_daily_features.csv": "FRED features aligned to market dates with release lag rules where specified.",
        "data/common_daily/features/valuation_daily_lagged_proxy.csv": "Conservatively lagged public valuation proxy, not a licensed point-in-time feed.",
        "data/common_daily/features/macro_event_flags_daily.csv": "Daily CPI/PCE flags from existing inflation_events_raw.csv.",
        "data/common_daily/features/common_research_daily_panel.csv": "Joined common panel from market, macro, valuation proxy, and event flags.",
    }
    rows = []
    for path in sorted(DATA_DIR.rglob("*.csv")):
        rows.append(inventory_csv(path, notes.get(str(path.relative_to(ROOT)).replace("\\", "/"), "")))
    pd.DataFrame(rows).to_csv(DATA_DIR / "data_inventory.csv", index=False)


def write_readme(end_date: str) -> None:
    text = f"""# Common Daily Research Data

Generated at: {datetime.now(timezone.utc).isoformat()}
Requested start date: {START_DATE}
Download end parameter: {end_date}

Core files:
- raw/yahoo_ohlcv_daily.csv: daily OHLCV and adjusted close for the shared asset pool, volatility indexes, commodities, and Mag 7 names.
- raw/yahoo_adjclose_wide.csv: adjusted close matrix.
- raw/fred_series_long.csv: FRED macro, rates, credit, volatility, commodity, and liquidity series.
- raw/multpl_valuation_raw.csv: public S&P 500 valuation proxies from Multpl.
- features/market_momentum_features.csv: 1/5/21/63/126/252-day returns, realized volatility, drawdown/rebound location, key ratios, and Mag 7 equal-weight return proxy.
- features/macro_daily_features.csv: FRED features aligned to market dates.
- features/valuation_daily_lagged_proxy.csv: lagged valuation proxy. This is not a replacement for point-in-time FactSet/IBES/Bloomberg/LSEG data.
- features/macro_event_flags_daily.csv: CPI/PCE event flags and surprise summaries from the existing inflation event file.
- features/common_research_daily_panel.csv: joined common daily panel.
- data_inventory.csv: row counts and date ranges.
- unresolved_data_requirements.csv: fields that still need licensed data or manual event work.

Important caveats:
- Yahoo and FRED public feeds are suitable for initial research staging, not vendor-grade point-in-time validation.
- Multpl valuation data is lagged conservatively from table dates to reduce look-ahead risk, but exact historical publication timestamps are not available here.
- Forward EPS, forward PE, EPS revisions, CDX, top-10 index weights, and true S&P 500 breadth require licensed or curated datasets.
"""
    (DATA_DIR / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    end_date = current_end_date()
    failures: list[dict] = []

    yahoo, yahoo_failures = download_yahoo_all(START_DATE, end_date)
    failures.extend(yahoo_failures)
    if not yahoo.empty:
        yahoo.to_csv(RAW_DIR / "yahoo_ohlcv_daily.csv", index=False)
        adjclose, market_features = build_market_features(yahoo)
        adjclose.reset_index().to_csv(RAW_DIR / "yahoo_adjclose_wide.csv", index=False)
        market_features.to_csv(FEATURE_DIR / "market_momentum_features.csv", index=False)
        market_dates = pd.DatetimeIndex(adjclose.index)
    else:
        market_dates = pd.bdate_range(START_DATE, pd.Timestamp(end_date))
        market_features = pd.DataFrame({"date": market_dates})

    fred, fred_failures = download_fred_all(START_DATE)
    failures.extend(fred_failures)
    if not fred.empty:
        fred.to_csv(RAW_DIR / "fred_series_long.csv", index=False)
    macro_features = build_macro_features(fred, market_dates)
    macro_features.to_csv(FEATURE_DIR / "macro_daily_features.csv", index=False)

    multpl, multpl_failures = scrape_multpl_all()
    failures.extend(multpl_failures)
    if not multpl.empty:
        multpl.to_csv(RAW_DIR / "multpl_valuation_raw.csv", index=False)
    valuation_daily = build_valuation_daily(multpl, market_dates)
    valuation_daily.to_csv(FEATURE_DIR / "valuation_daily_lagged_proxy.csv", index=False)

    event_flags = build_event_flags(market_dates)
    event_flags.to_csv(FEATURE_DIR / "macro_event_flags_daily.csv", index=False)

    panel = market_features.merge(macro_features, on="date", how="left")
    panel = panel.merge(valuation_daily, on="date", how="left", suffixes=("", "_valuation"))
    panel = panel.merge(event_flags, on="date", how="left", suffixes=("", "_event"))
    if {"sp500_earnings_yield_pct", "DGS10"}.issubset(panel.columns):
        panel["ERP_trailing_proxy"] = panel["sp500_earnings_yield_pct"] - panel["DGS10"] / 100.0
    panel.to_csv(FEATURE_DIR / "common_research_daily_panel.csv", index=False)

    write_symbol_map()
    write_unresolved_requirements(failures)
    write_readme(end_date)
    write_inventory()

    print(f"Wrote data to {DATA_DIR}")
    print(f"Yahoo rows: {len(yahoo):,}")
    print(f"FRED rows: {len(fred):,}")
    print(f"Multpl rows: {len(multpl):,}")
    print(f"Failures: {len(failures)}")


if __name__ == "__main__":
    main()
