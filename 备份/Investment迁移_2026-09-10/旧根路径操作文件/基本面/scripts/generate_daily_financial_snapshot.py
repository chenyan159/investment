from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

try:
    import yfinance as yf
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: yfinance") from exc


LA_TZ = ZoneInfo("America/Los_Angeles")
NY_TZ = ZoneInfo("America/New_York")

ROOT = Path(r"D:\drive\Investment\基本面")
DEFAULT_INDEX = ROOT / "公司调研" / "公司索引.md"
DEFAULT_OUT_DIR = ROOT.parent / "金融资料" / "每日金融数据"

SOURCE_BASE = "Yahoo Finance/yfinance"
NASDAQ_SOURCE = "Nasdaq free quote API"

ADR_RATIO_OVERRIDES = {
    "SIMO": "1 ADS = 4 ordinary shares",
    "ASML": "1 ADS = 1 ordinary share",
    "BABA": "1 ADS = 8 ordinary shares",
    "NOK": "1 ADS = 1 ordinary share",
    "TSM": "1 ADR = 5 ordinary shares",
    "UMC": "1 ADS = 5 ordinary shares",
}

KNOWN_ADR_OR_ADS = {
    "ABBNY",
    "AJNMY",
    "ARM",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "BABA",
    "BESIY",
    "DSCSY",
    "HOCPY",
    "IFNNY",
    "IMOS",
    "MIELY",
    "NOK",
    "RYCEY",
    "SHECY",
    "SIMO",
    "SOMMY",
    "TSM",
    "UMC",
}

US_EQUITY_EXCHANGES = {
    "ASE",
    "BTS",
    "NGM",
    "NMS",
    "NCM",
    "NYQ",
    "PCX",
}

OTC_EXCHANGES = {"OTC", "PNK", "PNQ", "PINX", "GREY"}


@dataclass(frozen=True)
class Company:
    ticker: str
    company: str
    category: str


@dataclass
class OptionPick:
    display: str = "缺失"
    success: bool = False
    note: str = ""


@dataclass
class SnapshotRow:
    category: str
    ticker: str
    company: str
    price_date: str = "缺失"
    price: float | None = None
    market_cap: float | None = None
    trailing_pe: float | None = None
    forward_pe: float | None = None
    ps: float | None = None
    pb: float | None = None
    ev_ebitda: float | None = None
    eps: float | None = None
    call_iv: str = "缺失"
    put_iv: str = "缺失"
    currency: str = "缺失/需确认"
    financial_currency: str = "缺失/需确认"
    shares_outstanding: float | None = None
    ttm_revenue: float | None = None
    ttm_eps: float | None = None
    forward_eps: float | None = None
    data_source: str = SOURCE_BASE
    source_timestamp: str = ""
    listing_type: str = "other/unknown"
    adr_ratio: str = "不适用"
    valuation_check: str = "市值:missing; PE:missing; FwdPE:missing; P/S:missing"
    notes: list[str] = field(default_factory=list)
    price_source: str = "缺失"
    option_chain_available: bool = False
    option_chain_read: bool = False
    clean_source_iv: bool = False
    valuation_statuses: dict[str, str] = field(default_factory=dict)
    recalcs: dict[str, float | None] = field(default_factory=dict)
    fetch_error: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate daily free-source financial snapshot from 公司索引.md."
    )
    parser.add_argument("--index", default=str(DEFAULT_INDEX), help="Path to 公司索引.md.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUT_DIR), help="Output directory.")
    parser.add_argument("--date", help="LA local run date, YYYY-MM-DD. Defaults to today.")
    parser.add_argument("--workers", type=int, default=6, help="Concurrent ticker workers.")
    parser.add_argument("--skip-options", action="store_true", help="Skip option chain reads.")
    parser.add_argument("--limit", type=int, default=0, help="Debug row limit.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing output file.")
    return parser.parse_args()


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(result):
        return None
    return result


def positive(value: float | None) -> bool:
    return value is not None and math.isfinite(value) and value > 0


def fmt_price(value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return "缺失"
    if abs(value) < 1:
        return f"{value:.4f}"
    return f"{value:.2f}"


def fmt_ratio(value: float | None, digits: int = 2) -> str:
    if value is None or not math.isfinite(value):
        return "缺失"
    if 0 < abs(value) < 0.01:
        return f"{value:.4f}"
    return f"{value:.{digits}f}"


def fmt_scaled(value: float | None, digits: int = 2, prefix: str = "") -> str:
    if value is None or not math.isfinite(value):
        return "缺失"
    abs_value = abs(value)
    if abs_value >= 1e12:
        return f"{prefix}{value / 1e12:.{digits}f}T"
    if abs_value >= 1e9:
        return f"{prefix}{value / 1e9:.{digits}f}B"
    if abs_value >= 1e6:
        return f"{prefix}{value / 1e6:.{digits}f}M"
    if abs_value >= 1e3:
        return f"{prefix}{value / 1e3:.{digits}f}K"
    return f"{prefix}{value:.{digits}f}"


def md_cell(value: Any) -> str:
    text = str(value)
    text = text.replace("\n", " ").replace("\r", " ")
    text = text.replace("|", "/")
    return text.strip()


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_index(path: Path) -> tuple[list[Company], int | None]:
    text = path.read_text(encoding="utf-8")
    declared = None
    title_match = re.search(r"#\s*(\d+)\s*家公司", text)
    if title_match:
        declared = int(title_match.group(1))

    companies: list[Company] = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("| 股票代号 |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = split_md_row(line)
        if len(cells) < 3:
            continue
        ticker = cells[0].strip().strip("`").upper()
        company = cells[1].strip()
        category = cells[2].strip().strip("`").strip().rstrip("/")
        if ticker and ticker != "股票代号":
            companies.append(Company(ticker=ticker, company=company, category=category))
    return companies, declared


def fast_get(fast_info: Any, key: str) -> Any:
    if fast_info is None:
        return None
    try:
        value = getattr(fast_info, key)
        if value is not None:
            return value
    except Exception:
        pass
    try:
        return fast_info[key]
    except Exception:
        return None


def get_info(info: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = info.get(key)
        if value not in (None, ""):
            return value
    return None


def date_from_history_index(index_value: Any) -> date | None:
    try:
        if hasattr(index_value, "to_pydatetime"):
            return index_value.to_pydatetime().date()
        if isinstance(index_value, datetime):
            return index_value.date()
    except Exception:
        return None
    return None


def date_from_market_time(value: Any) -> date | None:
    ts = as_float(value)
    if ts is None or ts <= 0:
        return None
    try:
        return datetime.fromtimestamp(ts, timezone.utc).astimezone(NY_TZ).date()
    except Exception:
        return None


def parse_money_text(value: Any) -> float | None:
    if value in (None, ""):
        return None
    cleaned = re.sub(r"[^0-9.\-]", "", str(value))
    if cleaned in {"", "-", "."}:
        return None
    return as_float(cleaned)


def date_from_nasdaq_timestamp(value: Any) -> date | None:
    if not value:
        return None
    text = str(value).strip()
    for pattern in ("%b %d, %Y %I:%M %p ET", "%B %d, %Y %I:%M %p ET"):
        try:
            parsed = datetime.strptime(text, pattern).replace(tzinfo=NY_TZ)
            return parsed.date()
        except ValueError:
            continue
    return None


def fetch_nasdaq_price(ticker: str) -> tuple[float | None, str, str | None]:
    symbol = urllib.parse.quote(ticker.upper())
    url = f"https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.nasdaq.com",
            "Referer": "https://www.nasdaq.com/",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return None, "缺失", f"Nasdaq价格回退读取失败: {exc!r}"

    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        status = payload.get("status") if isinstance(payload, dict) else None
        return None, "缺失", f"Nasdaq价格回退无覆盖: {status!r}"

    primary = data.get("primaryData")
    if not isinstance(primary, dict):
        return None, "缺失", "Nasdaq价格回退缺失primaryData"

    price = parse_money_text(primary.get("lastSalePrice"))
    price_date = date_from_nasdaq_timestamp(primary.get("lastTradeTimestamp"))
    if price is None:
        return None, "缺失", "Nasdaq价格回退缺失lastSalePrice"
    return price, price_date.isoformat() if price_date else "缺失", None


def detect_listing_type(ticker: str, info: dict[str, Any]) -> str:
    ticker_upper = ticker.upper()
    quote_type = str(info.get("quoteType") or "").upper()
    exchange = str(info.get("exchange") or "").upper()

    if quote_type in {"ETF", "MUTUALFUND", "FUND"}:
        return "fund/ETF"
    if ticker_upper in KNOWN_ADR_OR_ADS:
        return "ADR/ADS"
    if ticker_upper.endswith("Y") and (exchange in OTC_EXCHANGES or exchange == ""):
        return "ADR/ADS"
    if ticker_upper.endswith("F") and (exchange in OTC_EXCHANGES or exchange == ""):
        return "foreign_ordinary"
    if exchange in OTC_EXCHANGES:
        return "OTC"
    if quote_type == "EQUITY" and exchange in US_EQUITY_EXCHANGES:
        return "common/equity"
    if quote_type == "EQUITY":
        return "common/equity"
    return "other/unknown"


def adr_ratio_for(ticker: str, listing_type: str) -> str:
    ticker_upper = ticker.upper()
    if ticker_upper in ADR_RATIO_OVERRIDES:
        return ADR_RATIO_OVERRIDES[ticker_upper]
    if listing_type == "ADR/ADS":
        return "需确认"
    return "不适用"


def choose_price(
    run_date: date,
    info: dict[str, Any],
    fast_info: Any,
    history: Any,
) -> tuple[float | None, str, str, list[str]]:
    notes: list[str] = []
    hist_price = None
    hist_date = None
    if history is not None and not getattr(history, "empty", True):
        try:
            hist_price = as_float(history["Close"].iloc[-1])
            hist_date = date_from_history_index(history.index[-1])
        except Exception as exc:
            notes.append(f"history收盘价解析失败: {exc!r}")

    quote_price = as_float(
        get_info(info, "regularMarketPrice", "currentPrice")
    )
    if quote_price is None:
        quote_price = as_float(fast_get(fast_info, "last_price"))
    quote_date = date_from_market_time(info.get("regularMarketTime"))

    if quote_price is not None and quote_date is not None:
        if hist_date is None or quote_date >= hist_date:
            return quote_price, quote_date.isoformat(), "Yahoo Finance/yfinance quote.info", notes

    if (
        quote_price is not None
        and quote_date is None
        and hist_date is not None
        and hist_date < run_date
        and any(info.get(k) is not None for k in ("regularMarketDayHigh", "regularMarketDayLow", "regularMarketOpen"))
    ):
        notes.append(
            f"价格来自quote.currentPrice；regularMarketTime缺失；history最后日线={hist_date.isoformat()}"
        )
        return quote_price, run_date.isoformat(), "Yahoo Finance/yfinance quote.info", notes

    if hist_price is not None and hist_date is not None:
        if quote_price is not None and quote_date is None and abs(quote_price - hist_price) > max(0.01, abs(hist_price) * 0.02):
            notes.append("quote.currentPrice与history收盘价差异较大但无quote时间戳，保留history价格")
        return hist_price, hist_date.isoformat(), "Yahoo Finance/yfinance history", notes

    if quote_price is not None:
        date_text = quote_date.isoformat() if quote_date else run_date.isoformat()
        if quote_date is None:
            notes.append("价格来自quote.currentPrice；quote时间戳缺失")
        return quote_price, date_text, "Yahoo Finance/yfinance quote.info", notes

    return None, "缺失", "缺失", notes


def choose_expiry(expiries: tuple[str, ...] | list[str], run_date: date) -> tuple[str | None, str]:
    parsed: list[tuple[date, str]] = []
    for item in expiries:
        try:
            parsed.append((datetime.strptime(item, "%Y-%m-%d").date(), item))
        except ValueError:
            continue
    future = [(d, s) for d, s in parsed if d > run_date]
    if not future:
        return None, "无未来到期日"
    target = run_date + timedelta(days=30)
    window = [(d, s) for d, s in future if 14 <= (d - run_date).days <= 60]
    candidates = window if window else future
    selected = min(candidates, key=lambda x: (abs((x[0] - target).days), x[0]))
    note = "" if window else "无14-60天到期日，改用最近未来到期日"
    return selected[1], note


def parse_option_trade_date(value: Any) -> date | None:
    if value is None:
        return None
    try:
        if hasattr(value, "to_pydatetime"):
            return value.to_pydatetime().date()
        if isinstance(value, datetime):
            return value.date()
    except Exception:
        return None
    return None


def pick_option_iv(df: Any, price: float | None, expiry: str, run_date: date, side: str) -> OptionPick:
    if price is None or price <= 0:
        return OptionPick(note="价格缺失，无法筛选近ATM合约")
    if df is None or getattr(df, "empty", True):
        return OptionPick(note="期权链为空")

    best: tuple[float, dict[str, Any], float] | None = None
    scanned = 0
    for record in df.to_dict("records"):
        scanned += 1
        strike = as_float(record.get("strike"))
        bid = as_float(record.get("bid"))
        ask = as_float(record.get("ask"))
        iv = as_float(record.get("impliedVolatility"))
        volume = as_float(record.get("volume")) or 0.0
        open_interest = as_float(record.get("openInterest")) or 0.0
        if strike is None or strike <= 0 or iv is None:
            continue
        if iv < 0.01 or iv > 3.0:
            continue
        dist = abs(strike - price) / price
        if dist > 0.20:
            continue
        if bid is None or ask is None or bid <= 0 or ask <= 0 or ask < bid:
            continue
        mid = (bid + ask) / 2.0
        rel_spread = (ask - bid) / mid if mid > 0 else math.inf
        if rel_spread > 0.80:
            continue
        if volume + open_interest < 1:
            continue
        last_trade_date = parse_option_trade_date(record.get("lastTradeDate"))
        if last_trade_date is not None and last_trade_date < run_date - timedelta(days=30):
            continue

        liquidity_bonus = min(volume, 1000) / 10000 + min(open_interest, 5000) / 50000
        score = dist * 100 + rel_spread * 0.25 - liquidity_bonus
        if best is None or score < best[0]:
            best = (score, record, rel_spread)

    if best is None:
        return OptionPick(note=f"{side}: 无干净近ATM合约")

    record = best[1]
    strike = as_float(record.get("strike"))
    iv = as_float(record.get("impliedVolatility"))
    display = f"{iv * 100:.1f}% ({expiry}, K={fmt_strike(strike)}, source)"
    return OptionPick(display=display, success=True)


def fmt_strike(value: float | None) -> str:
    if value is None:
        return "缺失"
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def fetch_options(ticker_obj: Any, run_date: date, price: float | None) -> tuple[OptionPick, OptionPick, bool, bool, bool, list[str]]:
    notes: list[str] = []
    try:
        expiries = ticker_obj.options or ()
    except Exception as exc:
        return (
            OptionPick(note="call: 期权链读取失败"),
            OptionPick(note="put: 期权链读取失败"),
            False,
            False,
            False,
            [f"期权链读取失败: {exc!r}"],
        )

    if not expiries:
        return (
            OptionPick(note="call: 无期权链或数据源无覆盖"),
            OptionPick(note="put: 无期权链或数据源无覆盖"),
            False,
            False,
            False,
            [],
        )

    expiry, expiry_note = choose_expiry(expiries, run_date)
    if expiry is None:
        return (
            OptionPick(note="call: 无未来到期日"),
            OptionPick(note="put: 无未来到期日"),
            True,
            False,
            False,
            [expiry_note],
        )
    if expiry_note:
        notes.append(expiry_note)

    try:
        chain = ticker_obj.option_chain(expiry)
    except Exception as exc:
        return (
            OptionPick(note="call: 期权链读取失败"),
            OptionPick(note="put: 期权链读取失败"),
            True,
            False,
            False,
            [f"期权链读取失败({expiry}): {exc!r}"],
        )

    call_pick = pick_option_iv(chain.calls, price, expiry, run_date, "call")
    put_pick = pick_option_iv(chain.puts, price, expiry, run_date, "put")
    clean = call_pick.success or put_pick.success
    return call_pick, put_pick, True, True, clean, notes


def source_pe_value(source: float | None, calc: float | None, eps: float | None, label: str) -> tuple[float | None, str | None]:
    if eps is not None and eps <= 0:
        return None, f"{label}不适用：EPS为负或为零"
    if positive(source):
        return source, None
    if positive(calc):
        return calc, f"{label}源字段缺失，使用价格/EPS重算"
    return None, f"{label}缺失：源字段或EPS缺失"


def pct_diff(source: float | None, calc: float | None) -> float | None:
    if source is None or calc is None or not math.isfinite(source) or not math.isfinite(calc):
        return None
    denom = max(abs(source), 1e-9)
    return abs(calc - source) / denom


def check_status(
    source: float | None,
    calc: float | None,
    *,
    forced: str | None = None,
) -> str:
    if forced:
        return forced
    diff = pct_diff(source, calc)
    if diff is None:
        return "missing"
    if diff > 0.50:
        return f"bad({diff:.0%})"
    if diff > 0.15:
        return f"warn({diff:.0%})"
    return "ok"


def add_missing_note(row: SnapshotRow, field_name: str, reason: str) -> None:
    row.notes.append(f"{field_name}缺失: {reason}")


def fetch_company(company: Company, run_date: date, source_timestamp: str, skip_options: bool = False) -> SnapshotRow:
    row = SnapshotRow(
        category=company.category,
        ticker=company.ticker,
        company=company.company,
        source_timestamp=source_timestamp,
    )
    ticker_obj = yf.Ticker(company.ticker)
    info: dict[str, Any] = {}
    fast_info = None
    history = None

    try:
        history = ticker_obj.history(period="10d", auto_adjust=False)
    except Exception as exc:
        row.notes.append(f"history读取失败: {exc!r}")

    try:
        fast_info = ticker_obj.fast_info
    except Exception as exc:
        row.notes.append(f"fast_info读取失败: {exc!r}")

    try:
        info = ticker_obj.info or {}
    except Exception as exc:
        row.fetch_error = repr(exc)
        row.notes.append(f"quote.info读取失败: {exc!r}")
        info = {}

    price, price_date, price_source, price_notes = choose_price(run_date, info, fast_info, history)
    nasdaq_fallback_attempted = False
    if price is None:
        nasdaq_fallback_attempted = True
        nasdaq_price, nasdaq_price_date, nasdaq_note = fetch_nasdaq_price(company.ticker)
        if nasdaq_price is not None:
            price = nasdaq_price
            price_date = nasdaq_price_date if nasdaq_price_date != "缺失" else run_date.isoformat()
            price_source = NASDAQ_SOURCE
            price_notes.append("Yahoo价格缺失，使用Nasdaq免费quote回退")
            if nasdaq_price_date == "缺失":
                price_notes.append("Nasdaq价格回退时间戳缺失，价格日期按运行日标记")
        elif nasdaq_note:
            price_notes.append(nasdaq_note)
    row.price = price
    row.price_date = price_date
    row.price_source = price_source
    row.notes.extend(price_notes)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", price_date) and price_date < run_date.isoformat():
        row.notes.append(
            f"价格日期滞后：最新可得 {price_date}，洛杉矶运行日 {run_date.isoformat()}"
        )

    source_name = get_info(info, "longName", "shortName", "displayName")
    if source_name:
        row.notes.append(f"源名称: {source_name}")

    quote_currency = get_info(info, "currency") or fast_get(fast_info, "currency")
    financial_currency = get_info(info, "financialCurrency")
    row.currency = str(quote_currency) if quote_currency else "缺失/需确认"
    row.financial_currency = str(financial_currency) if financial_currency else "缺失/需确认"

    row.market_cap = as_float(get_info(info, "marketCap")) or as_float(fast_get(fast_info, "market_cap"))
    row.shares_outstanding = (
        as_float(get_info(info, "sharesOutstanding"))
        or as_float(get_info(info, "impliedSharesOutstanding"))
        or as_float(fast_get(fast_info, "shares"))
    )
    row.ttm_revenue = as_float(get_info(info, "totalRevenue"))
    row.ttm_eps = as_float(get_info(info, "trailingEps"))
    row.forward_eps = as_float(get_info(info, "forwardEps"))
    row.eps = row.ttm_eps
    row.pb = as_float(get_info(info, "priceToBook"))
    row.ev_ebitda = as_float(get_info(info, "enterpriseToEbitda"))

    source_trailing_pe = as_float(get_info(info, "trailingPE"))
    source_forward_pe = as_float(get_info(info, "forwardPE"))
    source_ps = as_float(get_info(info, "priceToSalesTrailing12Months"))

    market_cap_calc = row.price * row.shares_outstanding if row.price is not None and row.shares_outstanding else None
    pe_calc = row.price / row.ttm_eps if row.price is not None and row.ttm_eps and row.ttm_eps > 0 else None
    forward_pe_calc = (
        row.price / row.forward_eps if row.price is not None and row.forward_eps and row.forward_eps > 0 else None
    )
    currency_mismatch = (
        row.currency not in {"", "缺失/需确认"}
        and row.financial_currency not in {"", "缺失/需确认"}
        and row.currency != row.financial_currency
    )
    ps_calc = None
    if not currency_mismatch and row.market_cap is not None and row.ttm_revenue and row.ttm_revenue > 0:
        ps_calc = row.market_cap / row.ttm_revenue

    row.trailing_pe, pe_note = source_pe_value(source_trailing_pe, pe_calc, row.ttm_eps, "TTM PE")
    row.forward_pe, fwd_note = source_pe_value(source_forward_pe, forward_pe_calc, row.forward_eps, "Forward PE")
    if positive(source_ps):
        row.ps = source_ps
    elif ps_calc is not None:
        row.ps = ps_calc
        row.notes.append("P/S源字段缺失，使用市值/TTM收入重算")
    else:
        row.ps = None

    if pe_note:
        row.notes.append(pe_note)
    if fwd_note:
        row.notes.append(fwd_note)
    if row.price is None:
        price_reason = (
            "Yahoo history/quote 与 Nasdaq quote 回退均无可用价格"
            if nasdaq_fallback_attempted
            else "history和quote均无可用价格"
        )
        add_missing_note(row, "价格", price_reason)
    if row.market_cap is None:
        add_missing_note(row, "市值", "marketCap/fast_info.market_cap缺失")
    if row.ps is None:
        add_missing_note(row, "P/S", "源字段缺失或收入/币种口径无法校验")
    if row.pb is None:
        add_missing_note(row, "P/B", "源字段缺失")
    if row.ev_ebitda is None:
        add_missing_note(row, "EV/EBITDA", "源字段缺失")
    if row.eps is None:
        add_missing_note(row, "EPS", "trailingEps缺失")
    if row.currency == "缺失/需确认":
        row.notes.append("currency缺失/需确认")
    if row.financial_currency == "缺失/需确认":
        row.notes.append("financial_currency缺失/需确认")
    if row.shares_outstanding is None:
        add_missing_note(row, "shares_outstanding", "源字段缺失")
    if row.ttm_revenue is None:
        add_missing_note(row, "ttm_revenue", "totalRevenue缺失")
    if row.ttm_eps is None:
        add_missing_note(row, "ttm_eps", "trailingEps缺失")
    if row.forward_eps is None:
        add_missing_note(row, "forward_eps", "forwardEps缺失")
    if currency_mismatch:
        row.notes.append(f"交易货币/财报货币不一致: {row.currency}/{row.financial_currency}")

    row.listing_type = detect_listing_type(company.ticker, info)
    row.adr_ratio = adr_ratio_for(company.ticker, row.listing_type)
    if row.adr_ratio == "需确认":
        row.notes.append("ADR/ADS比例需确认")

    if row.pb is not None and row.pb < 0:
        row.notes.append(f"异常: P/B为负({row.pb:.2f})")
    if row.ev_ebitda is not None and row.ev_ebitda < 0:
        row.notes.append(f"异常: 负EV/EBITDA({row.ev_ebitda:.2f})")
    if row.trailing_pe is not None and row.trailing_pe > 300:
        row.notes.append(f"异常: TTM PE过高({row.trailing_pe:.2f})")
    if row.ev_ebitda is not None and row.ev_ebitda > 150:
        row.notes.append(f"异常: EV/EBITDA过高({row.ev_ebitda:.2f})")

    ps_forced = "bad(currency_mismatch)" if currency_mismatch else None
    if row.ttm_eps is not None and row.ttm_eps <= 0:
        pe_forced = "missing"
    else:
        pe_forced = None
    if row.forward_eps is not None and row.forward_eps <= 0:
        fwd_forced = "missing"
    else:
        fwd_forced = None

    statuses = {
        "market_cap": check_status(row.market_cap, market_cap_calc),
        "pe": check_status(source_trailing_pe, pe_calc, forced=pe_forced),
        "forward_pe": check_status(source_forward_pe, forward_pe_calc, forced=fwd_forced),
        "ps": check_status(source_ps, ps_calc, forced=ps_forced),
    }
    row.valuation_statuses = statuses
    row.recalcs = {
        "market_cap": market_cap_calc,
        "pe": pe_calc,
        "forward_pe": forward_pe_calc,
        "ps": ps_calc,
    }
    row.valuation_check = (
        f"市值:{statuses['market_cap']}; PE:{statuses['pe']}; "
        f"FwdPE:{statuses['forward_pe']}; P/S:{statuses['ps']}"
    )
    warn_bad = [name for name, status in statuses.items() if status.startswith(("warn", "bad"))]
    if warn_bad:
        row.notes.append("估值重算warn/bad: " + ",".join(warn_bad))

    source_parts: list[str] = []
    if row.price_source == NASDAQ_SOURCE:
        source_parts.append(f"{NASDAQ_SOURCE} price_fallback")
    elif "history" in row.price_source:
        source_parts.append("Yahoo Finance/yfinance history")
    elif "quote.info" in row.price_source:
        source_parts.append("Yahoo Finance/yfinance quote.info")
    else:
        source_parts.append("Yahoo Finance/yfinance quote.info")
    source_parts.append("Yahoo Finance/yfinance quote.info")
    if any("Nasdaq价格回退" in note or "Nasdaq免费quote回退" in note for note in row.notes):
        source_parts.append(f"{NASDAQ_SOURCE} fallback_attempt")
    if not skip_options:
        call_pick, put_pick, has_options, chain_read, clean_iv, option_notes = fetch_options(ticker_obj, run_date, row.price)
        row.call_iv = call_pick.display
        row.put_iv = put_pick.display
        row.option_chain_available = has_options
        row.option_chain_read = chain_read
        row.clean_source_iv = clean_iv
        row.notes.extend(option_notes)
        if call_pick.note:
            row.notes.append(call_pick.note)
        if put_pick.note:
            row.notes.append(put_pick.note)
        if has_options:
            source_parts.append("Yahoo Finance/yfinance options")
    else:
        row.notes.append("期权IV跳过: --skip-options")

    row.data_source = "; ".join(dict.fromkeys(source_parts))
    return row


def status_bucket(status: str) -> str:
    if status.startswith("ok"):
        return "ok"
    if status.startswith("warn"):
        return "warn"
    if status.startswith("bad"):
        return "bad"
    return "missing"


def has_missing_or_na(row: SnapshotRow) -> bool:
    required_values = [
        row.price,
        row.market_cap,
        row.trailing_pe,
        row.forward_pe,
        row.ps,
        row.pb,
        row.ev_ebitda,
        row.eps,
        row.shares_outstanding,
        row.ttm_revenue,
        row.ttm_eps,
        row.forward_eps,
    ]
    if any(value is None for value in required_values):
        return True
    if row.currency == "缺失/需确认" or row.financial_currency == "缺失/需确认":
        return True
    if row.call_iv == "缺失":
        return True
    return False


def note_text(row: SnapshotRow) -> str:
    if not row.notes:
        return ""
    deduped: list[str] = []
    seen = set()
    for note in row.notes:
        note = str(note).strip()
        if not note or note in seen:
            continue
        deduped.append(note)
        seen.add(note)
    return "<br>".join(md_cell(note) for note in deduped)


def build_report(
    rows: list[SnapshotRow],
    companies: list[Company],
    declared_total: int | None,
    run_date: date,
    generated_at: datetime,
    output_path: Path,
) -> str:
    source_timestamp = generated_at.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    total = len(rows)
    price_dates = [row.price_date for row in rows if re.fullmatch(r"\d{4}-\d{2}-\d{2}", row.price_date)]
    price_counter = Counter(price_dates)
    latest_price_date = max(price_dates) if price_dates else "缺失"
    common_price_date = price_counter.most_common(1)[0][0] if price_counter else "缺失"
    latest_price_count = price_counter.get(latest_price_date, 0)
    stale_count = sum(1 for row in rows if row.price_date != latest_price_date)
    run_date_text = run_date.isoformat()
    if latest_price_date == run_date_text and latest_price_count >= max(1, total // 2):
        top_note = f"主要价格数据已覆盖洛杉矶运行日 {run_date_text}；个别股票如滞后或quote无时间戳已在备注标记。"
    elif common_price_date != run_date_text and latest_price_date == run_date_text:
        top_note = (
            f"洛杉矶运行日为 {run_date_text}，但只有 {latest_price_count} 家公司的价格日期等于运行日；"
            f"最常见价格日期为 {common_price_date}。当天可能为非交易日、数据源尚未普遍更新或部分标的源覆盖不足。"
        )
    else:
        top_note = (
            f"洛杉矶运行日为 {run_date_text}，但可取得的最新价格日期为 {latest_price_date}；"
            "可能为非交易日、数据源尚未更新或部分标的源覆盖不足。"
        )

    coverage = {
        "price": sum(row.price is not None for row in rows),
        "market_cap": sum(row.market_cap is not None for row in rows),
        "ttm_pe": sum(row.trailing_pe is not None for row in rows),
        "forward_pe": sum(row.forward_pe is not None for row in rows),
        "ps": sum(row.ps is not None for row in rows),
        "pb": sum(row.pb is not None for row in rows),
        "ev_ebitda": sum(row.ev_ebitda is not None for row in rows),
        "eps": sum(row.eps is not None for row in rows),
    }
    missing_any = sum(has_missing_or_na(row) for row in rows)
    needs_confirm = sum(
        any(marker in note_text(row) for marker in ("需确认", "异常", "缺失", "读取失败", "不一致"))
        for row in rows
    )

    added = {
        "currency": sum(row.currency != "缺失/需确认" for row in rows),
        "financial_currency": sum(row.financial_currency != "缺失/需确认" for row in rows),
        "shares": sum(row.shares_outstanding is not None for row in rows),
        "revenue": sum(row.ttm_revenue is not None for row in rows),
        "ttm_eps": sum(row.ttm_eps is not None for row in rows),
        "forward_eps": sum(row.forward_eps is not None for row in rows),
        "data_source": sum(bool(row.data_source) for row in rows),
        "source_timestamp": sum(bool(row.source_timestamp) for row in rows),
        "listing_type": sum(row.listing_type != "other/unknown" for row in rows),
        "adr_known": sum(row.listing_type == "ADR/ADS" and row.adr_ratio != "需确认" for row in rows),
        "adr_confirm": sum(row.listing_type == "ADR/ADS" and row.adr_ratio == "需确认" for row in rows),
        "adr_na": sum(row.listing_type != "ADR/ADS" and row.adr_ratio == "不适用" for row in rows),
        "currency_mismatch": sum(
            row.currency not in {"", "缺失/需确认"}
            and row.financial_currency not in {"", "缺失/需确认"}
            and row.currency != row.financial_currency
            for row in rows
        ),
    }

    iv_stats = {
        "options_available": sum(row.option_chain_available for row in rows),
        "chain_read": sum(row.option_chain_read for row in rows),
        "call": sum(row.call_iv != "缺失" for row in rows),
        "put": sum(row.put_iv != "缺失" for row in rows),
        "both": sum(row.call_iv != "缺失" and row.put_iv != "缺失" for row in rows),
        "clean_source": sum(row.clean_source_iv for row in rows),
    }
    iv_stats["missing"] = total - iv_stats["call"]

    valuation_counts: dict[str, Counter[str]] = defaultdict(Counter)
    valuation_recalc = Counter()
    for row in rows:
        for metric, status in row.valuation_statuses.items():
            valuation_counts[metric][status_bucket(status)] += 1
            if row.recalcs.get(metric) is not None:
                valuation_recalc[metric] += 1

    price_source_counts = Counter(row.price_source for row in rows)
    category_counts = Counter(company.category for company in companies)
    rows_by_category: dict[str, list[SnapshotRow]] = defaultdict(list)
    for row in rows:
        rows_by_category[row.category].append(row)

    lines = [
        f"# 每日金融数据快照 {run_date_text}",
        "",
        f"> {top_note}",
        "",
        "## 生成与数据日期",
        "",
        f"- 生成时间：{source_timestamp}",
        f"- 价格数据日期：最新 `{latest_price_date}`；最常见 `{common_price_date}`；滞后于最新日期的公司 `{stale_count}` 家；每家公司详见明细表。",
        "- 估值数据日期：Yahoo Finance quote/info 于生成时间采集；TTM/forward 字段底层财报期或一致预期日期由数据源维护，源接口不提供逐字段 as-of date。",
        "- 使用的数据源说明：本次主源为 Yahoo Finance 免费匿名数据，经 `yfinance` 读取历史价格、quote/info 估值字段和期权链；价格缺口先回退到 quote.currentPrice/fast_info，仍缺失时再尝试 Nasdaq 免费 quote API。脚本不写入 provider 凭据，不要求付费 API key。字段缺失、源覆盖不足、期权链不干净或 ADR 比例需确认时，均写入公司明细备注列。",
        "- IV 口径：本次使用期权链 `impliedVolatility` 源字段并做合约筛选；未使用付费 IV provider，未用 0 代替缺失 IV。",
        f"- 公司数量校验：索引声明 `{declared_total if declared_total is not None else '未声明'}` 家；本次解析 `{len(companies)}` 家；写入 `{total}` 家。",
        "",
        "## 覆盖统计",
        "",
        "| 项目 | 数量 |",
        "|---|---:|",
        f"| 公司总数 | {total} |",
        f"| 价格成功 | {coverage['price']} |",
        f"| 价格缺失 | {total - coverage['price']} |",
        f"| 市值成功 | {coverage['market_cap']} |",
        f"| TTM PE成功 | {coverage['ttm_pe']} |",
        f"| Forward PE成功 | {coverage['forward_pe']} |",
        f"| P/S成功 | {coverage['ps']} |",
        f"| P/B成功 | {coverage['pb']} |",
        f"| EV/EBITDA成功 | {coverage['ev_ebitda']} |",
        f"| EPS成功 | {coverage['eps']} |",
        f"| 存在缺失/不适用字段的公司 | {missing_any} |",
        f"| 存在异常/需确认标记的公司 | {needs_confirm} |",
        "",
        "## 新增字段覆盖统计",
        "",
        "| 字段/项目 | 数量 |",
        "|---|---:|",
        f"| currency 成功 | {added['currency']} |",
        f"| currency 缺失/需确认 | {total - added['currency']} |",
        f"| financial_currency 成功 | {added['financial_currency']} |",
        f"| financial_currency 缺失/需确认 | {total - added['financial_currency']} |",
        f"| shares_outstanding 成功 | {added['shares']} |",
        f"| shares_outstanding 缺失 | {total - added['shares']} |",
        f"| ttm_revenue 成功 | {added['revenue']} |",
        f"| ttm_revenue 缺失 | {total - added['revenue']} |",
        f"| ttm_eps 成功 | {added['ttm_eps']} |",
        f"| ttm_eps 缺失 | {total - added['ttm_eps']} |",
        f"| forward_eps 成功 | {added['forward_eps']} |",
        f"| forward_eps 缺失 | {total - added['forward_eps']} |",
        f"| data_source 成功 | {added['data_source']} |",
        f"| source_timestamp 成功 | {added['source_timestamp']} |",
        f"| listing_type 成功 | {added['listing_type']} |",
        f"| ADR/ADS 比例已写明 | {added['adr_known']} |",
        f"| ADR/ADS 比例需确认 | {added['adr_confirm']} |",
        f"| 非 ADR/ADS adr_ratio 不适用 | {added['adr_na']} |",
        f"| 交易货币/财报货币不一致 | {added['currency_mismatch']} |",
        "",
        "## 估值重算/校验统计",
        "",
        "| 项目 | 数量 |",
        "|---|---:|",
    ]

    valuation_labels = [
        ("market_cap", "市值"),
        ("pe", "TTM PE"),
        ("forward_pe", "Forward PE"),
        ("ps", "P/S"),
    ]
    for key, label in valuation_labels:
        counts = valuation_counts[key]
        lines.extend(
            [
                f"| {label} 可重算 | {valuation_recalc[key]} |",
                f"| {label} 校验 ok | {counts['ok']} |",
                f"| {label} 校验 warn | {counts['warn']} |",
                f"| {label} 校验 bad | {counts['bad']} |",
                f"| {label} 校验 missing | {counts['missing']} |",
            ]
        )

    lines.extend(
        [
            "",
            "## 期权 IV 覆盖统计",
            "",
            "| 项目 | 数量 |",
            "|---|---:|",
            f"| 数据源返回期权链 | {iv_stats['options_available']} |",
            f"| 期权链成功读取 | {iv_stats['chain_read']} |",
            f"| Call IV成功 | {iv_stats['call']} |",
            f"| Put IV成功 | {iv_stats['put']} |",
            f"| Call/Put IV均成功 | {iv_stats['both']} |",
            f"| 使用干净bid/ask源IV的公司 | {iv_stats['clean_source']} |",
            "| 使用last trade估算IV的公司 | 0 |",
            f"| 无期权链或无干净Call IV | {iv_stats['missing']} |",
            "",
            "### 期权 IV 口径",
            "",
            "- 到期日：优先选择距离运行日 14-60 天内、最接近 30 天的到期日；没有该窗口时选择最近未来可用到期日并在备注标注。",
            "- 合约筛选：接近平值（strike 距离价格不超过 20%）、source IV 在 1%-300%；要求 bid/ask 均为正、ask >= bid、价差不过宽、成交量+持仓至少 1，且最近成交不过度陈旧。",
            "- 缺失处理：无期权链、无干净近 ATM 合约、零报价、异常 IV、流动性过低或价格缺失时均写入明细表备注，不以 0 代替。",
            "",
            "## 价格源统计",
            "",
            "| 价格源 | 公司数 |",
            "|---|---:|",
        ]
    )
    for source, count in sorted(price_source_counts.items()):
        lines.append(f"| {source} | {count} |")

    lines.extend(["", "## 分类统计", "", "| 分类 | 公司数 |", "|---|---:|"])
    for category, count in category_counts.items():
        lines.append(f"| {category} | {count} |")

    lines.extend(["", "## 按项目分类分组的公司明细表", ""])
    table_header = (
        "| 股票代号 | 公司名称 | 价格日期 | 最新价格 | 市值 | TTM PE | Forward PE | P/S | P/B | "
        "EV/EBITDA | EPS | Call IV | Put IV | currency | financial_currency | shares_outstanding | "
        "ttm_revenue | ttm_eps | forward_eps | listing_type | adr_ratio | data_source | "
        "source_timestamp | 估值校验 | 备注 |"
    )
    table_sep = (
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|---:|---:|---:|---|---|---|---|---|---|"
    )
    for category in category_counts:
        lines.extend([f"### {category}", "", table_header, table_sep])
        for row in rows_by_category.get(category, []):
            pe_text = "不适用(TTM EPS为负)" if row.ttm_eps is not None and row.ttm_eps <= 0 else fmt_ratio(row.trailing_pe)
            fwd_text = (
                "不适用(Forward EPS为负)"
                if row.forward_eps is not None and row.forward_eps <= 0
                else fmt_ratio(row.forward_pe)
            )
            cells = [
                row.ticker,
                row.company,
                row.price_date,
                fmt_price(row.price),
                fmt_scaled(row.market_cap, prefix="$"),
                pe_text,
                fwd_text,
                fmt_ratio(row.ps),
                fmt_ratio(row.pb),
                fmt_ratio(row.ev_ebitda),
                fmt_ratio(row.eps),
                row.call_iv,
                row.put_iv,
                row.currency,
                row.financial_currency,
                fmt_scaled(row.shares_outstanding),
                fmt_scaled(row.ttm_revenue),
                fmt_ratio(row.ttm_eps),
                fmt_ratio(row.forward_eps),
                row.listing_type,
                row.adr_ratio,
                row.data_source,
                row.source_timestamp,
                row.valuation_check,
                note_text(row),
            ]
            lines.append("| " + " | ".join(md_cell(cell) for cell in cells) + " |")
        lines.append("")

    lines.append(f"> 输出文件：`{output_path}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    index_path = Path(args.index)
    out_dir = Path(args.output_dir)
    run_date = datetime.now(LA_TZ).date() if not args.date else datetime.strptime(args.date, "%Y-%m-%d").date()
    generated_at = datetime.now(LA_TZ)
    source_timestamp = generated_at.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    output_path = out_dir / f"每日金融数据_{run_date.isoformat()}.md"

    companies, declared_total = parse_index(index_path)
    if args.limit > 0:
        companies = companies[: args.limit]
    if not companies:
        raise SystemExit(f"No companies parsed from {index_path}")
    if output_path.exists() and args.limit == 0 and not args.overwrite:
        raise SystemExit(f"Output already exists, not overwriting: {output_path}")

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Generating {len(companies)} rows -> {output_path}", flush=True)

    rows_by_ticker: dict[str, SnapshotRow] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(fetch_company, company, run_date, source_timestamp, args.skip_options): company
            for company in companies
        }
        for index, future in enumerate(as_completed(futures), start=1):
            company = futures[future]
            try:
                row = future.result()
            except Exception as exc:
                row = SnapshotRow(
                    category=company.category,
                    ticker=company.ticker,
                    company=company.company,
                    source_timestamp=source_timestamp,
                    fetch_error=repr(exc),
                    notes=[f"抓取失败: {exc!r}"],
                )
            rows_by_ticker[company.ticker] = row
            if index % 10 == 0 or index == len(companies):
                print(f"Fetched {index}/{len(companies)}", flush=True)

    rows = [rows_by_ticker[company.ticker] for company in companies]
    report = build_report(rows, companies, declared_total, run_date, generated_at, output_path)
    output_path.write_text(report, encoding="utf-8", newline="\n")
    print(f"Wrote {output_path} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
