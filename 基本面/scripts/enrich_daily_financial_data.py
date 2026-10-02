from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    import yfinance as yf
except ImportError as exc:  # pragma: no cover - runtime dependency check
    raise SystemExit("Missing dependency: yfinance") from exc


MISSING = {"", "缺失", "不适用", "不适用(TTM EPS为负)"}
SOURCE_NAME = "Yahoo Finance/yfinance quote.info"
LA_TZ = ZoneInfo("America/Los_Angeles")

ADR_RATIO_OVERRIDES = {
    "TSM": "1 ADR = 5 ordinary shares",
    "ASML": "1 ADS = 1 ordinary share",
    "BABA": "1 ADS = 8 ordinary shares",
}

KNOWN_ADR_OR_ADS = {
    "ABBNY",
    "AJNMY",
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
    "MIELY",
    "RYCEY",
    "SHECY",
    "SOMMY",
    "TSM",
    "UMC",
}


@dataclass
class DailyRow:
    category: str
    ticker: str
    company: str
    price_date: str
    price: float | None
    market_cap: float | None
    pe: float | None
    forward_pe: float | None
    ps: float | None
    notes: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add validation-oriented fields to a daily financial data Markdown file."
    )
    parser.add_argument("--input", required=True, help="Input daily financial data Markdown file.")
    parser.add_argument("--output", help="Output Markdown file. Defaults to *_补充字段校验.md.")
    parser.add_argument("--limit", type=int, default=0, help="Optional row limit for debugging.")
    return parser.parse_args()


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_money(value: str) -> float | None:
    text = clean_cell(value)
    if text in MISSING:
        return None
    multiplier = 1.0
    if text.startswith("$"):
        text = text[1:]
    if text.endswith("T"):
        multiplier = 1e12
        text = text[:-1]
    elif text.endswith("B"):
        multiplier = 1e9
        text = text[:-1]
    elif text.endswith("M"):
        multiplier = 1e6
        text = text[:-1]
    elif text.endswith("K"):
        multiplier = 1e3
        text = text[:-1]
    return parse_number(text, multiplier)


def clean_cell(value: str) -> str:
    return re.sub(r"<br\s*/?>", "; ", str(value), flags=re.I).strip()


def parse_number(value: str, multiplier: float = 1.0) -> float | None:
    text = clean_cell(value).replace(",", "").strip()
    if text in MISSING:
        return None
    if text.startswith("<"):
        text = text[1:]
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    try:
        return float(match.group(0)) * multiplier
    except ValueError:
        return None


def fmt_num(value: float | int | None, digits: int = 2) -> str:
    if value is None or not math.isfinite(float(value)):
        return "缺失"
    value = float(value)
    abs_value = abs(value)
    if abs_value >= 1e12:
        return f"${value / 1e12:.{digits}f}T"
    if abs_value >= 1e9:
        return f"${value / 1e9:.{digits}f}B"
    if abs_value >= 1e6:
        return f"${value / 1e6:.{digits}f}M"
    if abs_value >= 1e3:
        return f"${value / 1e3:.{digits}f}K"
    return f"{value:.{digits}f}"


def fmt_plain(value: float | int | None, digits: int = 2) -> str:
    if value is None or not math.isfinite(float(value)):
        return "缺失"
    return f"{float(value):.{digits}f}"


def pct_diff(source: float | None, calc: float | None) -> float | None:
    if source is None or calc is None:
        return None
    if not math.isfinite(source) or not math.isfinite(calc):
        return None
    denom = max(abs(source), 1e-9)
    return abs(calc - source) / denom


def check_status(source: float | None, calc: float | None, *, extra_flag: str | None = None) -> str:
    if extra_flag:
        return extra_flag
    diff = pct_diff(source, calc)
    if diff is None:
        return "missing"
    if diff > 0.50:
        return f"bad({diff:.0%})"
    if diff > 0.15:
        return f"warn({diff:.0%})"
    return "ok"


def detect_listing_type(ticker: str, info: dict) -> str:
    exchange = str(info.get("exchange") or "")
    quote_type = str(info.get("quoteType") or "")
    ticker_upper = ticker.upper()
    if ticker_upper in KNOWN_ADR_OR_ADS:
        return "ADR/ADS"
    if ticker_upper.endswith("Y"):
        return "OTC_ADR"
    if ticker_upper.endswith("F"):
        return "OTC_foreign_ordinary"
    if "." in ticker_upper:
        return "foreign_local"
    if exchange in {"NMS", "NGM", "NCM", "NYQ", "ASE", "PCX"} and quote_type == "EQUITY":
        return "US_listed_equity"
    return quote_type or exchange or "unknown"


def adr_ratio(ticker: str, listing_type: str) -> str:
    ticker_upper = ticker.upper()
    if ticker_upper in ADR_RATIO_OVERRIDES:
        return ADR_RATIO_OVERRIDES[ticker_upper]
    if "ADR" in listing_type or "ADS" in listing_type:
        return "需确认"
    return "不适用"


def parse_daily_rows(path: Path) -> list[DailyRow]:
    rows: list[DailyRow] = []
    category = ""
    lines = path.read_text(encoding="utf-8").splitlines()
    table_header = [
        "股票代号",
        "公司名称",
        "价格日期",
        "最新价格",
        "市值",
        "TTM PE",
        "Forward PE",
        "P/S",
        "P/B",
        "EV/EBITDA",
        "EPS(TTM)",
        "Call IV",
        "Put IV",
        "备注",
    ]
    in_table = False
    for line in lines:
        if line.startswith("### "):
            category = line[4:].strip()
            in_table = False
            continue
        if line.startswith("| 股票代号 |"):
            in_table = split_md_row(line) == table_header
            continue
        if in_table:
            if not line.startswith("|") or line.startswith("|---"):
                continue
            cells = split_md_row(line)
            if len(cells) != len(table_header):
                continue
            rows.append(
                DailyRow(
                    category=category,
                    ticker=cells[0],
                    company=cells[1],
                    price_date=cells[2],
                    price=parse_number(cells[3]),
                    market_cap=parse_money(cells[4]),
                    pe=parse_number(cells[5]),
                    forward_pe=parse_number(cells[6]),
                    ps=parse_number(cells[7]),
                    notes=clean_cell(cells[13]),
                )
            )
    return rows


def fetch_info(ticker: str) -> dict:
    try:
        info = yf.Ticker(ticker).info or {}
    except Exception as exc:  # pragma: no cover - network/data source failure
        return {"_fetch_error": repr(exc)}
    return info


def as_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(result):
        return None
    return result


def build_report(rows: list[DailyRow], source_path: Path, output_path: Path) -> str:
    source_timestamp = datetime.now(LA_TZ).strftime("%Y-%m-%d %H:%M:%S %Z%z")
    enriched = []
    counts = {
        "rows": 0,
        "currency": 0,
        "shares": 0,
        "revenue": 0,
        "ttm_eps": 0,
        "forward_eps": 0,
        "market_cap_bad": 0,
        "pe_bad": 0,
        "forward_pe_bad": 0,
        "ps_bad": 0,
        "currency_mismatch": 0,
        "fetch_error": 0,
    }

    for row in rows:
        info = fetch_info(row.ticker)
        fetch_error = info.get("_fetch_error")
        currency = info.get("currency") or ""
        financial_currency = info.get("financialCurrency") or currency or ""
        shares = as_float(info.get("sharesOutstanding") or info.get("impliedSharesOutstanding"))
        ttm_revenue = as_float(info.get("totalRevenue"))
        ttm_eps = as_float(info.get("trailingEps"))
        forward_eps = as_float(info.get("forwardEps"))
        listing = detect_listing_type(row.ticker, info)
        ratio = adr_ratio(row.ticker, listing)

        market_cap_calc = row.price * shares if row.price is not None and shares else None
        pe_calc = row.price / ttm_eps if row.price is not None and ttm_eps and ttm_eps > 0 else None
        forward_pe_calc = (
            row.price / forward_eps if row.price is not None and forward_eps and forward_eps > 0 else None
        )
        currency_mismatch = bool(currency and financial_currency and currency != financial_currency)
        ps_calc = None
        ps_extra_flag = None
        if currency_mismatch:
            ps_extra_flag = "bad(currency_mismatch)"
        elif row.market_cap is not None and ttm_revenue and ttm_revenue > 0:
            ps_calc = row.market_cap / ttm_revenue

        market_cap_status = check_status(row.market_cap, market_cap_calc)
        pe_status = check_status(row.pe, pe_calc)
        forward_pe_status = check_status(row.forward_pe, forward_pe_calc)
        ps_status = check_status(row.ps, ps_calc, extra_flag=ps_extra_flag)

        bad_fields = [
            name
            for name, status in [
                ("market_cap", market_cap_status),
                ("pe", pe_status),
                ("forward_pe", forward_pe_status),
                ("ps", ps_status),
            ]
            if status.startswith("bad")
        ]
        notes = []
        if fetch_error:
            notes.append(f"fetch_error: {fetch_error}")
        if currency_mismatch:
            notes.append(f"currency mismatch: price={currency}, financial={financial_currency}")
        if bad_fields:
            notes.append("bad_fields=" + ",".join(bad_fields))
        if "源名称" in row.notes:
            source_name = row.notes.split(";")[0].replace("源名称:", "").strip()
        else:
            source_name = ""

        counts["rows"] += 1
        counts["currency"] += bool(currency)
        counts["shares"] += bool(shares)
        counts["revenue"] += bool(ttm_revenue)
        counts["ttm_eps"] += bool(ttm_eps)
        counts["forward_eps"] += bool(forward_eps)
        counts["market_cap_bad"] += market_cap_status.startswith("bad")
        counts["pe_bad"] += pe_status.startswith("bad")
        counts["forward_pe_bad"] += forward_pe_status.startswith("bad")
        counts["ps_bad"] += ps_status.startswith("bad")
        counts["currency_mismatch"] += currency_mismatch
        counts["fetch_error"] += bool(fetch_error)

        enriched.append(
            {
                "category": row.category,
                "ticker": row.ticker,
                "company": row.company,
                "price_date": row.price_date,
                "price": row.price,
                "source_market_cap": row.market_cap,
                "currency": currency or "缺失",
                "financial_currency": financial_currency or "缺失",
                "shares": shares,
                "ttm_revenue": ttm_revenue,
                "ttm_eps": ttm_eps,
                "forward_eps": forward_eps,
                "listing_type": listing,
                "adr_ratio": ratio,
                "data_source": SOURCE_NAME,
                "source_timestamp": source_timestamp,
                "market_cap_calc": market_cap_calc,
                "pe_calc": pe_calc,
                "forward_pe_calc": forward_pe_calc,
                "ps_calc": ps_calc,
                "market_cap_status": market_cap_status,
                "pe_status": pe_status,
                "forward_pe_status": forward_pe_status,
                "ps_status": ps_status,
                "source_name": source_name,
                "notes": "; ".join(notes) if notes else "",
            }
        )

    lines = [
        f"# 每日金融数据补充字段与校验 {source_path.stem.replace('每日金融数据_', '')}",
        "",
        f"> 来源文件：`{source_path.as_posix()}`",
        f"> 生成时间：{source_timestamp}",
        "",
        "## 字段口径",
        "",
        "| 字段 | 用途 |",
        "|---|---|",
        "| currency | 交易/报价货币，用于识别美元、台币、日元和 ADR 口径混用 |",
        "| financial_currency | 财报货币；若与 currency 不同，P/S 等收入类估值必须先做汇率或 ADR 口径处理 |",
        "| shares_outstanding | 用于用 `price * shares` 交叉校验市值 |",
        "| ttm_revenue | 用于重新计算 P/S；币种以 financial_currency 为准 |",
        "| ttm_eps | 用于重新计算 TTM PE |",
        "| forward_eps | 用于重新计算 Forward PE |",
        "| data_source | 字段来源 |",
        "| source_timestamp | 本次采集时间 |",
        "| adr_ratio / listing_type | 识别 ADR/ADS、OTC ADR、普通美股或外股本地上市口径 |",
        "",
        "## 覆盖与异常统计",
        "",
        "| 项目 | 数量 |",
        "|---|---:|",
        f"| 公司总数 | {counts['rows']} |",
        f"| currency 成功 | {counts['currency']} |",
        f"| shares_outstanding 成功 | {counts['shares']} |",
        f"| ttm_revenue 成功 | {counts['revenue']} |",
        f"| ttm_eps 成功 | {counts['ttm_eps']} |",
        f"| forward_eps 成功 | {counts['forward_eps']} |",
        f"| 交易货币/财报货币不一致 | {counts['currency_mismatch']} |",
        f"| 市值校验 bad | {counts['market_cap_bad']} |",
        f"| PE 校验 bad | {counts['pe_bad']} |",
        f"| Forward PE 校验 bad | {counts['forward_pe_bad']} |",
        f"| P/S 校验 bad | {counts['ps_bad']} |",
        f"| yfinance info 抓取失败 | {counts['fetch_error']} |",
        "",
        "## 明细表",
        "",
        "| 股票代号 | 公司名称 | 分类 | 价格日期 | 最新价格 | 源市值 | currency | financial_currency | shares_outstanding | ttm_revenue | ttm_eps | forward_eps | listing_type | adr_ratio | 市值重算 | PE重算 | Fwd PE重算 | P/S重算 | 市值校验 | PE校验 | Fwd PE校验 | P/S校验 | data_source | source_timestamp | 备注 |",
        "|---|---|---|---|---:|---:|---|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---|---|---|---|---|---|---|",
    ]

    for item in enriched:
        lines.append(
            "| "
            + " | ".join(
                [
                    item["ticker"],
                    item["company"],
                    item["category"],
                    item["price_date"],
                    fmt_plain(item["price"]),
                    fmt_num(item["source_market_cap"]),
                    item["currency"],
                    item["financial_currency"],
                    fmt_num(item["shares"], 2),
                    fmt_num(item["ttm_revenue"], 2),
                    fmt_plain(item["ttm_eps"]),
                    fmt_plain(item["forward_eps"]),
                    item["listing_type"],
                    item["adr_ratio"],
                    fmt_num(item["market_cap_calc"]),
                    fmt_plain(item["pe_calc"]),
                    fmt_plain(item["forward_pe_calc"]),
                    fmt_plain(item["ps_calc"]),
                    item["market_cap_status"],
                    item["pe_status"],
                    item["forward_pe_status"],
                    item["ps_status"],
                    item["data_source"],
                    item["source_timestamp"],
                    item["notes"] or item["source_name"],
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    output_path = Path(args.output) if args.output else input_path.with_name(input_path.stem + "_补充字段校验.md")
    rows = parse_daily_rows(input_path)
    if args.limit and args.limit > 0:
        rows = rows[: args.limit]
    if not rows:
        raise SystemExit("No daily financial data rows parsed.")
    report = build_report(rows, input_path, output_path)
    output_path.write_text(report, encoding="utf-8", newline="\n")
    print(f"Wrote {output_path} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
