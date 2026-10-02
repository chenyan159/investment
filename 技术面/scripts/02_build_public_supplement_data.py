from __future__ import annotations

import csv
import math
import re
import time
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
COMMON_DIR = ROOT / "data" / "common_daily"
RAW_DIR = COMMON_DIR / "raw"
FEATURE_DIR = COMMON_DIR / "features"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; common-daily-supplement/1.0)"}
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
WIKI_SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
IVV_HOLDINGS_URL = (
    "https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/"
    "1467271812596.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund"
)
FED_CURRENT_CALENDAR_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FED_HISTORICAL_YEAR_URL = "https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm"

START_DATE = "2010-01-01"
MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
MONTH_NUM = {name: idx + 1 for idx, name in enumerate(MONTHS)}
MONTH_ALIASES = {name: name for name in MONTHS}
MONTH_ALIASES.update(
    {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Sept": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December",
    }
)
MAG7_HOLDING_TICKERS = {"AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "NVDA", "TSLA"}


def ensure_dirs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)


def request_text(url: str, attempts: int = 4) -> str:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=60)
            response.raise_for_status()
            return response.text
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"GET failed after {attempts} attempts: {url}") from last_error


def request_bytes(url: str, attempts: int = 4) -> bytes:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=60)
            response.raise_for_status()
            return response.content
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"GET failed after {attempts} attempts: {url}") from last_error


def yahoo_symbol(symbol: str) -> str:
    clean = str(symbol).strip()
    special = {"BRKB": "BRK-B", "BFB": "BF-B", "BRK.B": "BRK-B", "BF.B": "BF-B"}
    return special.get(clean, clean.replace(".", "-"))


def parse_number(value: object) -> float:
    if value is None or pd.isna(value):
        return math.nan
    text = str(value).strip().replace(",", "").replace("%", "")
    if text in {"", "-", "nan"}:
        return math.nan
    return float(text)


def scrape_wikipedia_sp500_constituents() -> pd.DataFrame:
    soup = BeautifulSoup(request_text(WIKI_SP500_URL), "html.parser")
    table = soup.find("table", {"id": "constituents"})
    if table is None:
        raise RuntimeError("Could not find Wikipedia S&P 500 constituents table")
    headers = [th.get_text(" ", strip=True) for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(cells) != len(headers):
            continue
        row = dict(zip(headers, cells, strict=True))
        row["yahoo_symbol"] = yahoo_symbol(row["Symbol"])
        row["source_url"] = WIKI_SP500_URL
        row["source"] = "Wikipedia current S&P 500 constituents"
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(RAW_DIR / "sp500_current_constituents_wikipedia.csv", index=False)
    return df


def download_ivv_holdings() -> tuple[pd.DataFrame, pd.Timestamp]:
    text = request_bytes(IVV_HOLDINGS_URL).decode("utf-8-sig", errors="replace")
    rows = list(csv.reader(StringIO(text)))
    as_of = pd.NaT
    for row in rows[:10]:
        if row and row[0].strip().lower() == "fund holdings as of" and len(row) > 1:
            as_of = pd.to_datetime(row[1], errors="coerce")
            break
    header_idx = next(i for i, row in enumerate(rows) if row and row[0] == "Ticker")
    df = pd.DataFrame(rows[header_idx + 1 :], columns=rows[header_idx])
    df = df[df["Ticker"].notna() & df["Asset Class"].eq("Equity")].copy()
    df = df[df["Ticker"].astype(str).str.strip().ne("-")]
    df["Ticker"] = df["Ticker"].astype(str).str.strip()
    df["yahoo_symbol"] = df["Ticker"].map(yahoo_symbol)
    for col in ["Market Value", "Weight (%)", "Notional Value", "Quantity", "Price", "FX Rate"]:
        if col in df:
            df[col] = df[col].map(parse_number)
    df["holdings_as_of"] = as_of
    df["source_url"] = IVV_HOLDINGS_URL
    df["source"] = "iShares IVV holdings"
    df.to_csv(RAW_DIR / "ivv_current_holdings.csv", index=False)

    top = df.sort_values("Weight (%)", ascending=False).head(25).copy()
    top.to_csv(FEATURE_DIR / "ivv_current_top25_holdings.csv", index=False)
    return df, as_of


def download_close_history(symbols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames: list[pd.DataFrame] = []
    failures: list[dict] = []
    unique_symbols = sorted({symbol for symbol in symbols if symbol and symbol != "-"})
    chunk_size = 80
    for start in range(0, len(unique_symbols), chunk_size):
        chunk = unique_symbols[start : start + chunk_size]
        data = yf.download(
            chunk,
            start=START_DATE,
            auto_adjust=False,
            progress=False,
            threads=True,
            group_by="column",
        )
        if data.empty:
            for symbol in chunk:
                failures.append({"yahoo_symbol": symbol, "reason": "empty chunk result"})
            continue
        if isinstance(data.columns, pd.MultiIndex):
            if "Close" in data.columns.get_level_values(0):
                close = data["Close"].copy()
            elif "Adj Close" in data.columns.get_level_values(0):
                close = data["Adj Close"].copy()
            else:
                failures.extend({"yahoo_symbol": symbol, "reason": "no close column"} for symbol in chunk)
                continue
        else:
            close = data[["Close"]].rename(columns={"Close": chunk[0]})
        close.index = pd.to_datetime(close.index).tz_localize(None).normalize()
        close = close.loc[:, ~close.columns.duplicated()]
        frames.append(close)
        for symbol in chunk:
            if symbol not in close.columns or close[symbol].dropna().empty:
                failures.append({"yahoo_symbol": symbol, "reason": "no price history"})
        time.sleep(0.5)

    if frames:
        close_all = pd.concat(frames, axis=1)
        close_all = close_all.loc[:, ~close_all.columns.duplicated()].sort_index()
        close_all.index.name = "date"
    else:
        close_all = pd.DataFrame()
    failures_df = pd.DataFrame(failures).drop_duplicates() if failures else pd.DataFrame(columns=["yahoo_symbol", "reason"])
    close_all.reset_index().to_csv(RAW_DIR / "sp500_current_constituents_close_2010.csv", index=False)
    failures_df.to_csv(RAW_DIR / "sp500_current_constituents_price_failures.csv", index=False)
    return close_all, failures_df


def compute_breadth(close: pd.DataFrame) -> pd.DataFrame:
    returns = close.pct_change(fill_method=None)
    available = close.notna().sum(axis=1)
    out = pd.DataFrame(index=close.index)
    out["current_constituent_price_count"] = available
    for window in [20, 50, 200]:
        ma = close.rolling(window, min_periods=window).mean()
        valid = close.notna() & ma.notna()
        out[f"pct_above_{window}dma_current_constituents"] = ((close > ma) & valid).sum(axis=1) / valid.sum(axis=1)
        out[f"count_above_{window}dma_current_constituents"] = ((close > ma) & valid).sum(axis=1)
        out[f"count_valid_{window}dma_current_constituents"] = valid.sum(axis=1)
    out["advance_count_current_constituents"] = (returns > 0).sum(axis=1)
    out["decline_count_current_constituents"] = (returns < 0).sum(axis=1)
    out["unchanged_count_current_constituents"] = (returns == 0).sum(axis=1)
    out["advance_minus_decline_current_constituents"] = (
        out["advance_count_current_constituents"] - out["decline_count_current_constituents"]
    )
    out["advance_minus_decline_pct_current_constituents"] = out["advance_minus_decline_current_constituents"] / available
    out["advance_decline_ratio_current_constituents"] = (
        out["advance_count_current_constituents"] / out["decline_count_current_constituents"].replace(0, np.nan)
    )
    out["advance_decline_line_current_constituents"] = out["advance_minus_decline_current_constituents"].cumsum()
    out["equal_weight_return_current_constituents"] = returns.mean(axis=1, skipna=True)
    out["median_return_current_constituents"] = returns.median(axis=1, skipna=True)
    out["pct_positive_return_current_constituents"] = (returns > 0).sum(axis=1) / returns.notna().sum(axis=1)
    out.index.name = "date"
    out = out.reset_index()
    out.to_csv(FEATURE_DIR / "sp500_current_constituents_breadth_proxy.csv", index=False)
    return out


def compute_concentration_proxy(close: pd.DataFrame, holdings: pd.DataFrame) -> pd.DataFrame:
    clean = holdings.dropna(subset=["Quantity", "Weight (%)"]).copy()
    clean = clean[clean["yahoo_symbol"].isin(close.columns)].copy()
    quantities = clean.drop_duplicates("yahoo_symbol").set_index("yahoo_symbol")["Quantity"]
    aligned = close[quantities.index].copy()
    values = aligned.multiply(quantities, axis=1)
    weights = values.divide(values.sum(axis=1), axis=0)

    out = pd.DataFrame(index=close.index)
    out["top10_weight_proxy_current_holdings"] = weights.apply(lambda row: row.nlargest(10).sum(), axis=1)
    out["top5_weight_proxy_current_holdings"] = weights.apply(lambda row: row.nlargest(5).sum(), axis=1)
    out["top25_weight_proxy_current_holdings"] = weights.apply(lambda row: row.nlargest(25).sum(), axis=1)
    out["hhi_proxy_current_holdings"] = (weights**2).sum(axis=1)
    mag7_cols = [symbol for symbol in MAG7_HOLDING_TICKERS if symbol in weights.columns]
    out["mag7_weight_proxy_current_holdings"] = weights[mag7_cols].sum(axis=1) if mag7_cols else np.nan
    out["holdings_price_coverage_count"] = values.notna().sum(axis=1)
    out["holdings_weight_coverage_proxy"] = values.notna().multiply(
        clean.drop_duplicates("yahoo_symbol").set_index("yahoo_symbol")["Weight (%)"] / 100.0,
        axis=1,
    ).sum(axis=1)
    out.index.name = "date"
    out = out.reset_index()
    out.to_csv(FEATURE_DIR / "sp500_current_holdings_concentration_proxy.csv", index=False)

    current_summary = pd.DataFrame(
        [
            {
                "holdings_as_of": holdings["holdings_as_of"].dropna().max(),
                "top10_weight_current_ivv": holdings.sort_values("Weight (%)", ascending=False).head(10)["Weight (%)"].sum()
                / 100.0,
                "top5_weight_current_ivv": holdings.sort_values("Weight (%)", ascending=False).head(5)["Weight (%)"].sum()
                / 100.0,
                "top25_weight_current_ivv": holdings.sort_values("Weight (%)", ascending=False).head(25)["Weight (%)"].sum()
                / 100.0,
                "mag7_weight_current_ivv": holdings.loc[holdings["Ticker"].isin(MAG7_HOLDING_TICKERS), "Weight (%)"].sum()
                / 100.0,
                "equity_holding_count": len(holdings),
                "source": "iShares IVV holdings",
                "source_url": IVV_HOLDINGS_URL,
            }
        ]
    )
    current_summary.to_csv(FEATURE_DIR / "ivv_current_concentration_summary.csv", index=False)
    return out


def parse_historical_fomc_year(year: int) -> list[dict]:
    soup = BeautifulSoup(request_text(FED_HISTORICAL_YEAR_URL.format(year=year)), "html.parser")
    records = []
    pattern = re.compile(
        r"(?P<month1>[A-Za-z]+(?:/[A-Za-z]+)?) (?P<day1>\d{1,2})"
        r"(?:-(?:(?P<month2>[A-Za-z]+) )?(?P<day2>\d{1,2}))?"
        rf"(?P<extra>.*?) - (?P<year>\d{{4}})"
    )
    for heading in soup.find_all(["h4", "h5"]):
        title = heading.get_text(" ", strip=True)
        match = pattern.search(title)
        if not match:
            continue
        month_token = match.group("month2") or match.group("month1").split("/")[-1]
        event_month = MONTH_ALIASES.get(month_token)
        if event_month is None:
            continue
        event_day = int(match.group("day2") or match.group("day1"))
        event_date = pd.Timestamp(year=int(match.group("year")), month=MONTH_NUM[event_month], day=event_day)
        lower = title.lower()
        records.append(
            {
                "event_date": event_date,
                "year": int(match.group("year")),
                "meeting_title": title,
                "meeting_type": "conference_call"
                if "conference call" in lower
                else "notation_vote"
                if "notation vote" in lower
                else "meeting",
                "is_unscheduled": int("unscheduled" in lower or "conference call" in lower or "notation vote" in lower),
                "is_cancelled": int("cancelled" in lower),
                "has_sep": np.nan,
                "source_url": FED_HISTORICAL_YEAR_URL.format(year=year),
                "source": "Federal Reserve historical FOMC materials",
            }
        )
    return records


def parse_current_fomc_calendar() -> list[dict]:
    soup = BeautifulSoup(request_text(FED_CURRENT_CALENDAR_URL), "html.parser")
    records = []
    for panel in soup.select(".panel.panel-default"):
        heading = panel.select_one(".panel-heading")
        heading_text = heading.get_text(" ", strip=True) if heading else ""
        year_match = re.search(r"(20\d{2}) FOMC Meetings", heading_text)
        if not year_match:
            continue
        year = int(year_match.group(1))
        if year < 2021 or year > 2026:
            continue
        lines = [line.strip() for line in panel.get_text("\n", strip=True).split("\n") if line.strip()]
        for idx, line in enumerate(lines[:-1]):
            date_line = lines[idx + 1].replace("*", "")
            month_token = line.split("/")[-1] if "/" in line else line
            month_name = MONTH_ALIASES.get(month_token)
            if month_name not in MONTHS or not re.match(r"^\d{1,2}(?:-\d{1,2})?$", date_line):
                continue
            day = int(date_line.split("-")[-1])
            event_date = pd.Timestamp(year=year, month=MONTH_NUM[month_name], day=day)
            records.append(
                {
                    "event_date": event_date,
                    "year": year,
                    "meeting_title": f"{line} {lines[idx + 1]} FOMC meeting - {year}",
                    "meeting_type": "meeting",
                    "is_unscheduled": 0,
                    "is_cancelled": 0,
                    "has_sep": int("*" in lines[idx + 1]),
                    "source_url": FED_CURRENT_CALENDAR_URL,
                    "source": "Federal Reserve FOMC calendars",
                }
            )
    return records


def download_fred(series_id: str, start: str = "1990-01-01") -> pd.DataFrame:
    text = request_text(f"{FRED_CSV_URL}?id={series_id}&cosd={start}")
    df = pd.read_csv(StringIO(text))
    value_col = df.columns[1]
    df = df.rename(columns={df.columns[0]: "date", value_col: series_id})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df[series_id] = pd.to_numeric(df[series_id].replace(".", np.nan), errors="coerce")
    return df.dropna(subset=["date"]).sort_values("date")


def add_target_rate_changes(fomc: pd.DataFrame) -> pd.DataFrame:
    frames = [download_fred(series) for series in ["DFEDTAR", "DFEDTARU", "DFEDTARL"]]
    target = frames[0]
    for frame in frames[1:]:
        target = target.merge(frame, on="date", how="outer")
    target = target.sort_values("date").set_index("date").ffill()
    target["target_mid"] = np.where(
        target[["DFEDTARU", "DFEDTARL"]].notna().all(axis=1),
        (target["DFEDTARU"] + target["DFEDTARL"]) / 2.0,
        target["DFEDTAR"],
    )
    target["target_mid_change_bp"] = target["target_mid"].diff() * 100.0
    target.reset_index().to_csv(RAW_DIR / "fed_policy_target_daily.csv", index=False)

    target_reset = target.reset_index()
    event_target = pd.merge_asof(
        fomc.sort_values("event_date"),
        target_reset.rename(columns={"date": "event_date"}).sort_values("event_date"),
        on="event_date",
        direction="backward",
    )
    before_lookup = target_reset[["date", "target_mid"]].rename(
        columns={"date": "target_before_lookup_date", "target_mid": "target_mid_before_decision"}
    )
    after_lookup = target_reset[["date", "target_mid"]].rename(
        columns={"date": "target_after_lookup_date", "target_mid": "target_mid_after_decision"}
    )
    event_target["target_before_lookup_date"] = event_target["event_date"] - pd.Timedelta(days=1)
    event_target["target_after_lookup_date"] = event_target["event_date"] + pd.Timedelta(days=1)
    event_target = pd.merge_asof(
        event_target.sort_values("target_before_lookup_date"),
        before_lookup.sort_values("target_before_lookup_date"),
        on="target_before_lookup_date",
        direction="backward",
    ).sort_values("event_date")
    event_target = pd.merge_asof(
        event_target.sort_values("target_after_lookup_date"),
        after_lookup.sort_values("target_after_lookup_date"),
        on="target_after_lookup_date",
        direction="backward",
    ).sort_values("event_date")
    event_target["target_decision_change_bp"] = (
        event_target["target_mid_after_decision"] - event_target["target_mid_before_decision"]
    ) * 100.0
    return event_target


def build_fomc_calendar(market_dates: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    records: list[dict] = []
    for year in range(1990, 2021):
        records.extend(parse_historical_fomc_year(year))
        time.sleep(0.1)
    records.extend(parse_current_fomc_calendar())
    fomc = pd.DataFrame(records).drop_duplicates(["event_date", "meeting_title"]).sort_values("event_date")
    fomc = add_target_rate_changes(fomc)

    zq_path = ROOT / "tmp" / "market_history_policy_surprise.csv"
    if zq_path.exists():
        zq = pd.read_csv(zq_path, parse_dates=["Date"]).rename(columns={"Date": "date"})
        if "ZQ=F" in zq:
            zq = zq.sort_values("date")
            zq["zq_implied_rate_pct"] = 100.0 - zq["ZQ=F"]
            zq["zq_5d_implied_rate_change_bp"] = zq["zq_implied_rate_pct"].diff(5) * 100.0
            fomc = pd.merge_asof(
                fomc.sort_values("event_date"),
                zq[["date", "zq_implied_rate_pct", "zq_5d_implied_rate_change_bp"]].rename(
                    columns={"date": "event_date"}
                ),
                on="event_date",
                direction="backward",
                tolerance=pd.Timedelta(days=5),
            )
    if "zq_5d_implied_rate_change_bp" not in fomc.columns:
        # ZQ futures are an optional public proxy; keep the FOMC calendar usable
        # when the local market-history file is absent or lacks ZQ prices.
        fomc["zq_5d_implied_rate_change_bp"] = np.nan

    fomc["market_date"] = align_to_market_dates(fomc["event_date"], market_dates)
    fomc.to_csv(RAW_DIR / "fomc_calendar_fed.csv", index=False)

    active = fomc[fomc["is_cancelled"].ne(1) & fomc["market_date"].notna()].copy()
    flags = active.groupby("market_date").agg(
        fomc_event_count=("event_date", "size"),
        fomc_unscheduled_count=("is_unscheduled", "sum"),
        fomc_sep_count=("has_sep", "sum"),
        fomc_target_mid_change_bp=("target_decision_change_bp", "sum"),
        fomc_zq_5d_implied_rate_change_bp=("zq_5d_implied_rate_change_bp", "last"),
    )
    flags["has_fomc_event"] = 1
    result = pd.DataFrame({"date": market_dates})
    result = result.merge(flags.reset_index().rename(columns={"market_date": "date"}), on="date", how="left")
    fill_zero = ["fomc_event_count", "fomc_unscheduled_count", "fomc_sep_count", "has_fomc_event"]
    for col in fill_zero:
        result[col] = result[col].fillna(0).astype(int)
    result.to_csv(FEATURE_DIR / "fomc_event_flags_daily.csv", index=False)
    return fomc, result


def align_to_market_dates(dates: pd.Series, market_dates: pd.Series) -> pd.Series:
    calendar = pd.DatetimeIndex(pd.to_datetime(market_dates).sort_values())
    aligned = []
    for value in pd.to_datetime(dates):
        if pd.isna(value):
            aligned.append(pd.NaT)
            continue
        idx = calendar.searchsorted(value)
        aligned.append(calendar[idx] if idx < len(calendar) else pd.NaT)
    return pd.Series(aligned, index=dates.index)


def first_jobs_report_friday(year: int, month: int) -> pd.Timestamp:
    first = pd.Timestamp(year=year, month=month, day=1)
    candidate = first
    while candidate.weekday() != 4 or candidate.day < 3:
        candidate += pd.Timedelta(days=1)
    return candidate


def build_nfp_calendar(market_dates: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    payems = download_fred("PAYEMS", START_DATE)
    unrate = download_fred("UNRATE", START_DATE)
    df = payems.merge(unrate, on="date", how="left")
    df["reference_month"] = df["date"]
    df["payems_mom_chg_k_current_revised"] = df["PAYEMS"].diff()
    df["release_month"] = df["reference_month"] + pd.offsets.MonthBegin(1)
    df["release_date"] = df["release_month"].map(lambda x: first_jobs_report_friday(x.year, x.month))
    df["market_date"] = align_to_market_dates(df["release_date"], market_dates)
    df["calendar_method"] = "first_friday_on_or_after_3rd_day_approx"
    df["source"] = "FRED PAYEMS/UNRATE with approximate BLS Employment Situation release rule"
    df["source_url"] = "https://fred.stlouisfed.org/series/PAYEMS"
    nfp = df[
        [
            "reference_month",
            "release_date",
            "market_date",
            "PAYEMS",
            "payems_mom_chg_k_current_revised",
            "UNRATE",
            "calendar_method",
            "source",
            "source_url",
        ]
    ].copy()
    nfp.to_csv(RAW_DIR / "nfp_release_calendar_approx.csv", index=False)

    flags = nfp[nfp["market_date"].notna()].groupby("market_date").agg(
        nfp_release_count=("reference_month", "size"),
        nfp_payems_mom_chg_k_current_revised=("payems_mom_chg_k_current_revised", "last"),
        nfp_unrate_current_revised=("UNRATE", "last"),
    )
    flags["has_nfp_release"] = 1
    result = pd.DataFrame({"date": market_dates})
    result = result.merge(flags.reset_index().rename(columns={"market_date": "date"}), on="date", how="left")
    result["has_nfp_release"] = result["has_nfp_release"].fillna(0).astype(int)
    result["nfp_release_count"] = result["nfp_release_count"].fillna(0).astype(int)
    result.to_csv(FEATURE_DIR / "nfp_event_flags_daily.csv", index=False)
    return nfp, result


def formalize_policy_surprise_proxy(market_dates: pd.Series) -> pd.DataFrame:
    path = ROOT / "tmp" / "policy_surprise_events.csv"
    result = pd.DataFrame({"date": market_dates})
    if not path.exists():
        result.to_csv(FEATURE_DIR / "zq_policy_surprise_proxy_flags_daily.csv", index=False)
        return result
    events = pd.read_csv(path, parse_dates=["date"])
    events["market_date"] = align_to_market_dates(events["date"], market_dates)
    events["source"] = "Existing tmp/policy_surprise_events.csv; ZQ 5-trading-day implied rate move proxy"
    events.to_csv(RAW_DIR / "zq_policy_surprise_proxy_events.csv", index=False)
    grouped = events.dropna(subset=["market_date"]).groupby("market_date").agg(
        zq_large_policy_move_count=("date", "size"),
        zq_large_policy_move_bp=("zq_5d_implied_rate_change_bp", "last"),
        zq_large_policy_move_type=("type", "last"),
    )
    grouped["has_zq_large_policy_move"] = 1
    result = result.merge(grouped.reset_index().rename(columns={"market_date": "date"}), on="date", how="left")
    result["has_zq_large_policy_move"] = result["has_zq_large_policy_move"].fillna(0).astype(int)
    result["zq_large_policy_move_count"] = result["zq_large_policy_move_count"].fillna(0).astype(int)
    result.to_csv(FEATURE_DIR / "zq_policy_surprise_proxy_flags_daily.csv", index=False)
    return result


def build_enriched_panel(extra_frames: list[pd.DataFrame]) -> pd.DataFrame:
    base_path = FEATURE_DIR / "common_research_daily_panel.csv"
    base = pd.read_csv(base_path, parse_dates=["date"])
    panel = base.copy()
    for frame in extra_frames:
        panel = panel.merge(frame, on="date", how="left")
    panel.to_csv(FEATURE_DIR / "common_research_daily_panel_enriched.csv", index=False)
    return panel


def write_unresolved_after_supplement() -> None:
    rows = [
        {
            "variable_group": "valuation",
            "variable": "forward PE",
            "status": "not_done",
            "available_proxy": "trailing PE and earnings yield from Multpl; current Yahoo ETF trailingPE snapshot can be queried but is not historical forward PE",
            "remaining_gap": "Needs licensed point-in-time consensus forward EPS/price history.",
            "likely_source": "FactSet, IBES, Bloomberg, LSEG, S&P Capital IQ",
        },
        {
            "variable_group": "valuation",
            "variable": "EV/Sales",
            "status": "not_done",
            "available_proxy": "S&P 500 P/S from Multpl with conservative lag.",
            "remaining_gap": "Historical index-level EV/Sales is not available from the public sources used here.",
            "likely_source": "FactSet, Bloomberg, S&P Capital IQ",
        },
        {
            "variable_group": "earnings",
            "variable": "forward EPS / EPS revision / earnings growth expectation",
            "status": "not_done",
            "available_proxy": "None suitable for point-in-time modeling.",
            "remaining_gap": "Needs analyst estimate history with publication timestamps.",
            "likely_source": "FactSet, IBES, Bloomberg, LSEG",
        },
        {
            "variable_group": "earnings",
            "variable": "Mag 7 EPS contribution",
            "status": "not_done",
            "available_proxy": "Mag 7 price return and IVV current holdings weight proxies are available.",
            "remaining_gap": "Needs point-in-time EPS contribution or constituent-level EPS estimates and index weights.",
            "likely_source": "FactSet, Bloomberg, S&P Capital IQ",
        },
        {
            "variable_group": "credit",
            "variable": "CDX",
            "status": "not_done",
            "available_proxy": "HY_OAS, IG_OAS, BBB_OAS, HYG/LQD and HYG/Treasury ETF spread proxies.",
            "remaining_gap": "CDX index history is not available from the public sources used here.",
            "likely_source": "Markit/IHS, Bloomberg, LSEG",
        },
        {
            "variable_group": "market breadth",
            "variable": "advance-decline",
            "status": "proxy_done",
            "available_proxy": "advance/decline counts and A-D line using current IVV/S&P 500 holdings from 2010 onward.",
            "remaining_gap": "True exchange breadth or point-in-time S&P 500 membership breadth still requires vendor data.",
            "likely_source": "NYSE/Nasdaq data, Bloomberg, Refinitiv, CRSP/Compustat, Norgate",
        },
        {
            "variable_group": "market breadth",
            "variable": "% above 20/50/200dma for S&P 500 members",
            "status": "proxy_done",
            "available_proxy": "current-constituent % above 20/50/200dma from 2010 onward.",
            "remaining_gap": "Point-in-time constituent membership version still requires vendor data.",
            "likely_source": "CRSP/Compustat, Bloomberg, FactSet, Norgate",
        },
        {
            "variable_group": "concentration",
            "variable": "Top 10 weight",
            "status": "proxy_done",
            "available_proxy": "Current IVV top-10/top-25/Mag7 weights and current-holdings backcast proxy from 2010 onward.",
            "remaining_gap": "True historical S&P 500 point-in-time top-10 weights require historical index constituents and shares/float weights.",
            "likely_source": "S&P Dow Jones Indices, FactSet, Bloomberg",
        },
        {
            "variable_group": "macro events",
            "variable": "NFP release surprise calendar",
            "status": "partial_done",
            "available_proxy": "Approximate NFP release calendar plus current-revised PAYEMS/UNRATE values.",
            "remaining_gap": "Survey forecast surprise and exact historical release-date exceptions need an economic calendar or ALFRED/BLS access.",
            "likely_source": "Bloomberg ECO, Econoday, Investing.com, Refinitiv, ALFRED release dates",
        },
        {
            "variable_group": "macro events",
            "variable": "FOMC policy surprise calendar",
            "status": "partial_done",
            "available_proxy": "Fed FOMC calendar, target-rate changes, and ZQ 5-day implied-rate-change proxy from 2018 onward where available.",
            "remaining_gap": "True high-frequency policy surprise requires futures/OIS ticks around statement release.",
            "likely_source": "Fed, CME FedWatch, Bloomberg, high-frequency Fed funds futures/OIS data",
        },
        {
            "variable_group": "macro events",
            "variable": "fiscal/tariff/geopolitical event labels",
            "status": "not_done",
            "available_proxy": "Policy uncertainty indexes already exist in the project.",
            "remaining_gap": "Needs a curated taxonomy or news/event database to avoid arbitrary hand labels.",
            "likely_source": "GDELT, RavenPack, Bloomberg News, manual event file",
        },
    ]
    df = pd.DataFrame(rows)
    df.to_csv(COMMON_DIR / "unresolved_data_requirements.csv", index=False)
    df.to_csv(COMMON_DIR / "unresolved_data_requirements_after_public_supplement.csv", index=False)


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
    date_col = "date" if "date" in df.columns else "event_date" if "event_date" in df.columns else None
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
        "data/common_daily/features/common_research_daily_panel_enriched.csv": "Joined panel plus public supplements: breadth proxy, concentration proxy, FOMC/NFP/ZQ event flags.",
        "data/common_daily/features/sp500_current_constituents_breadth_proxy.csv": "Survivorship-biased current-constituent breadth proxy from IVV holdings.",
        "data/common_daily/features/sp500_current_holdings_concentration_proxy.csv": "Current IVV holdings backcast concentration proxy; not true historical index weights.",
        "data/common_daily/raw/fomc_calendar_fed.csv": "FOMC event calendar scraped from Federal Reserve pages plus target-rate changes.",
        "data/common_daily/raw/nfp_release_calendar_approx.csv": "Approximate NFP release dates plus current-revised PAYEMS/UNRATE values.",
        "data/common_daily/raw/ivv_current_holdings.csv": "Current IVV holdings from iShares.",
        "data/common_daily/raw/sp500_current_constituents_wikipedia.csv": "Current S&P 500 constituent table from Wikipedia.",
    }
    rows = []
    for path in sorted(COMMON_DIR.rglob("*.csv")):
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        rows.append(inventory_csv(path, notes.get(rel, "")))
    pd.DataFrame(rows).to_csv(COMMON_DIR / "data_inventory.csv", index=False)


def update_readme() -> None:
    readme = COMMON_DIR / "README.md"
    existing = readme.read_text(encoding="utf-8") if readme.exists() else "# Common Daily Research Data\n"
    marker = "## Public Supplement\n"
    supplement = f"""{marker}
Generated at: {datetime.now(timezone.utc).isoformat()}

Additional files:
- raw/sp500_current_constituents_wikipedia.csv: current S&P 500 constituent list from Wikipedia.
- raw/ivv_current_holdings.csv: current IVV holdings from iShares.
- raw/sp500_current_constituents_close_2010.csv: Yahoo close prices for current IVV equity holdings, starting 2010.
- features/sp500_current_constituents_breadth_proxy.csv: current-constituent advance/decline and % above 20/50/200dma proxy.
- features/sp500_current_holdings_concentration_proxy.csv: top-5/top-10/top-25/Mag7 concentration proxy using current IVV quantities backcast through prices.
- raw/fomc_calendar_fed.csv and features/fomc_event_flags_daily.csv: FOMC calendar, target-rate changes, and ZQ 5-day implied-rate proxy where available.
- raw/nfp_release_calendar_approx.csv and features/nfp_event_flags_daily.csv: approximate NFP release calendar with current-revised PAYEMS/UNRATE values.
- features/common_research_daily_panel_enriched.csv: joined panel with the public supplements.

Supplement caveats:
- Breadth and concentration supplements use the current IVV/S&P 500 membership and therefore have survivorship bias.
- The concentration backcast is a proxy based on current IVV share quantities, not historical S&P Dow Jones point-in-time weights.
- NFP release dates are rule-based approximations; forecast surprises are not included.
- FOMC ZQ-based values are policy-surprise proxies, not true high-frequency policy surprises.
"""
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + "\n\n" + supplement
    else:
        existing = existing.rstrip() + "\n\n" + supplement
    readme.write_text(existing, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    base = pd.read_csv(FEATURE_DIR / "common_research_daily_panel.csv", parse_dates=["date"])
    market_dates = base["date"]

    scrape_wikipedia_sp500_constituents()
    holdings, _ = download_ivv_holdings()
    close, failures = download_close_history(holdings["yahoo_symbol"].dropna().tolist())
    if close.empty:
        raise RuntimeError("No current-constituent price data downloaded")

    breadth = compute_breadth(close)
    concentration = compute_concentration_proxy(close, holdings)
    _, fomc_flags = build_fomc_calendar(market_dates)
    _, nfp_flags = build_nfp_calendar(market_dates)
    zq_flags = formalize_policy_surprise_proxy(market_dates)

    build_enriched_panel([breadth, concentration, fomc_flags, nfp_flags, zq_flags])
    write_unresolved_after_supplement()
    write_inventory()
    update_readme()

    print(f"IVV equity holdings: {len(holdings):,}")
    print(f"Downloaded close columns: {len(close.columns):,}")
    print(f"Price failures: {len(failures):,}")
    print(f"Wrote enriched panel to {FEATURE_DIR / 'common_research_daily_panel_enriched.csv'}")


if __name__ == "__main__":
    main()
