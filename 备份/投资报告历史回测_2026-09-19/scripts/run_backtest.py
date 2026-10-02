from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(r"D:\investment")
OUT = ROOT / "备份" / "投资报告历史回测_2026-09-19"
END_DATE = pd.Timestamp("2026-09-18")
FETCH_START = "2026-09-04"
FETCH_END_EXCLUSIVE = "2026-09-20"
RECENT_PRICE_CACHE = OUT / "tmp" / "近期行情下载.csv"

OLD_RANK_PATH = (
    ROOT
    / "分析报告"
    / "公司排序"
    / "90_有效性评估"
    / "2026-07-12_全版本生成后评估"
    / "02_全版本全部公司股价变动明细.csv"
)
OLD_MANIFEST_PATH = OLD_RANK_PATH.with_name("03_版本与生成日期清单.csv")
JULY_RANK_PATH = ROOT / "备份" / "项目反思_2026-09-04" / "data" / "historical_rankings.csv"
SCENARIO_PATH = ROOT / "备份" / "项目反思_2026-09-04" / "data" / "decisions_historical.csv"
SCENARIO_REPORTS_PATH = OUT / "agent_scenario_reports.csv"
SCENARIO_SNAPSHOTS_PATH = OUT / "agent_scenario_snapshots.csv"
META_PATH = ROOT / "备份" / "项目反思_2026-09-04" / "data" / "company_review_joined.csv"
COMPARE_RANK_PATH = ROOT / "备份" / "company-comparison专项回测_2026-09-05" / "data" / "derived_rankings.csv"
COMPARE_JUNE_PATH = ROOT / "分析报告" / "tmp" / "公司对比信号前3个月6个月价格及后续验证_2026-07-12.csv"
LOCAL_PRICE_PATH = ROOT / "备份" / "项目反思_2026-09-04" / "data" / "daily_prices.csv"

EXTRA_RANKINGS = [
    {
        "id": "B15",
        "date": "2026-05-29",
        "name": "情景收入利润股价区间",
        "csv": ROOT / "分析报告" / "备份" / "排序清理_2026-06-11" / "旧排序结果" / "简单排序" / "15_情景收入利润股价区间_评分卡_2026-05-27.csv",
        "report": ROOT / "分析报告" / "备份" / "排序清理_2026-06-11" / "旧排序结果" / "简单排序" / "15_情景收入利润股价区间_全公司排序_2026-05-27.md",
        "columns": {"排名": "rank", "股票代号": "ticker", "公司名称": "company", "公司分类": "category", "总分": "score"},
        "dependency_note": "独立旧路线；与61版最大Top30重合11/30",
    },
    {
        "id": "B16",
        "date": "2026-05-29",
        "name": "情景收入可能下行股价区间",
        "csv": ROOT / "分析报告" / "备份" / "排序清理_2026-06-11" / "旧排序结果" / "简单排序" / "16_情景收入可能下行股价区间_评分卡_2026-05-27.csv",
        "report": ROOT / "分析报告" / "备份" / "排序清理_2026-06-11" / "旧排序结果" / "简单排序" / "16_情景收入可能下行股价区间_全公司排序_2026-05-27.md",
        "columns": {"排名": "rank", "股票代号": "ticker", "公司名称": "company", "公司分类": "category", "总分": "score"},
        "dependency_note": "与旧07路线部分相关，但不是副本",
    },
    {
        "id": "B17",
        "date": "2026-06-01",
        "name": "179家公司投资排序_公司评估",
        "csv": ROOT / "分析报告" / "备份" / "排序清理_2026-06-11" / "旧排序结果" / "简单排序" / "17_179家公司投资排序_公司评估_评分卡_2026-06-01.csv",
        "report": ROOT / "分析报告" / "备份" / "排序清理_2026-06-11" / "旧排序结果" / "简单排序" / "17_179家公司投资排序_公司评估_全公司排序_2026-06-01.md",
        "columns": {"排名": "rank", "股票代号": "ticker", "公司名称": "company", "公司分类": "category", "总分": "score"},
        "dependency_note": "被排除的旧08/公司评估179家路线；非61版副本",
    },
    {
        "id": "BAGG",
        "date": "2026-06-02",
        "name": "激进投资排序",
        "csv": ROOT / "分析报告" / "备份" / "排序清理_2026-06-11" / "旧排序结果" / "投资排序" / "激进投资排序_2026-06-02.csv",
        "report": ROOT / "分析报告" / "备份" / "排序清理_2026-06-11" / "旧排序结果" / "投资排序" / "激进投资排序_2026-06-02.md",
        "columns": {"rank": "rank", "ticker": "ticker", "name": "company", "category": "category", "score": "score"},
        "dependency_note": "与61版12/2026-06-02高度相关（全榜Spearman 0.78、Top30重合22/30），不作独立票",
    },
]

BENCHMARKS = ["SPY", "QQQ", "SOXX"]
PRICE_SYMBOL_MAP = {
    "PSTG": "P",  # 2026 年历史代码已失效；项目冻结数据使用 P 承接连续序列。
}
AGGREGATE_EXCLUSIONS = {
    "MICLF": "OTC 极低流动性且 2026-09-18 报价与此前长期陈旧报价冲突",
}
RATING_SCORE = {
    "强烈建议投资": 6,
    "建议投资": 5,
    "谨慎建议投资": 4,
    "中性/等待": 3,
    "不建议投资": 2,
    "强烈不建议投资": 1,
}


def normalize_rating(value: object) -> str:
    return str(value).replace(" ", "").strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_float(value: object) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return float("nan")
    return x if math.isfinite(x) else float("nan")


def pct(value: object, digits: int = 2) -> str:
    x = safe_float(value)
    return "NA" if not math.isfinite(x) else f"{x * 100:.{digits}f}%"


def num(value: object, digits: int = 3) -> str:
    x = safe_float(value)
    return "NA" if not math.isfinite(x) else f"{x:.{digits}f}"


def download_recent(symbols: list[str]) -> pd.DataFrame:
    """Fetch only the post-freeze tail; the frozen local cache remains the historical base."""
    symbols = sorted(set(symbols))
    RECENT_PRICE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    if RECENT_PRICE_CACHE.exists():
        cached = pd.read_csv(RECENT_PRICE_CACHE)
        cached["date"] = pd.to_datetime(cached["date"])
        if set(symbols).issubset(set(cached["symbol"].astype(str))):
            print(f"Using cached recent prices for {len(symbols)} symbols ...", flush=True)
            return cached[cached["symbol"].isin(symbols)].copy()
    print(f"Downloading recent prices for {len(symbols)} symbols ...", flush=True)
    raw = yf.download(
        tickers=symbols,
        start=FETCH_START,
        end=FETCH_END_EXCLUSIVE,
        auto_adjust=False,
        actions=False,
        group_by="ticker",
        threads=True,
        progress=False,
        timeout=30,
    )
    rows: list[dict[str, object]] = []
    if not isinstance(raw.columns, pd.MultiIndex):
        raw.columns = pd.MultiIndex.from_product([[symbols[0]], raw.columns])
    level0 = set(str(x) for x in raw.columns.get_level_values(0))
    # yfinance may return either (ticker, field) or (field, ticker).
    ticker_first = bool(set(symbols) & level0)
    for symbol in symbols:
        try:
            frame = raw[symbol] if ticker_first else raw.xs(symbol, level=1, axis=1)
        except (KeyError, ValueError):
            continue
        frame = frame.copy()
        frame.index = pd.to_datetime(frame.index).tz_localize(None)
        for dt, r in frame.iterrows():
            close = safe_float(r.get("Close"))
            if not math.isfinite(close):
                continue
            rows.append(
                {
                    "symbol": symbol,
                    "date": pd.Timestamp(dt).normalize(),
                    "open": safe_float(r.get("Open")),
                    "high": safe_float(r.get("High")),
                    "low": safe_float(r.get("Low")),
                    "close": close,
                    "volume": safe_float(r.get("Volume")),
                    "adj_close": safe_float(r.get("Adj Close", close)),
                    "price_source": "Yahoo Finance via yfinance 1.3.0; refreshed 2026-09-19",
                }
            )
    out = pd.DataFrame(rows)
    if not out.empty:
        out.to_csv(RECENT_PRICE_CACHE, index=False, encoding="utf-8-sig")
    return out


def load_prices(symbols: list[str]) -> pd.DataFrame:
    base = pd.read_csv(LOCAL_PRICE_PATH)
    base["date"] = pd.to_datetime(base["date"])
    base["price_source"] = "frozen Yahoo chart cache collected 2026-09-04"
    recent = download_recent(symbols)
    combined = pd.concat([base, recent], ignore_index=True, sort=False)
    combined = combined[combined["symbol"].isin(symbols)].copy()
    combined = combined[combined["date"] <= END_DATE].copy()
    combined.sort_values(["symbol", "date", "price_source"], inplace=True)
    # The refreshed tail wins on overlapping dates.
    combined.drop_duplicates(["symbol", "date"], keep="last", inplace=True)
    combined.sort_values(["symbol", "date"], inplace=True)
    combined.reset_index(drop=True, inplace=True)
    return combined


@dataclass
class PriceObservation:
    ticker: str
    pricing_symbol: str
    intended_start_date: pd.Timestamp
    start_date: pd.Timestamp | None
    start_open: float
    start_adj_open: float
    end_date: pd.Timestamp | None
    end_close: float
    end_adj_close: float
    total_return: float
    price_return: float
    zero_volume_days: int
    data_status: str
    aggregate_eligible: bool
    exclusion_reason: str


class PriceBook:
    def __init__(self, prices: pd.DataFrame):
        self.prices = prices.copy()
        self.by_symbol = {
            str(symbol): frame.sort_values("date").reset_index(drop=True)
            for symbol, frame in self.prices.groupby("symbol", sort=False)
        }

    def next_us_session(self, report_date: pd.Timestamp) -> pd.Timestamp | None:
        spy = self.by_symbol.get("SPY")
        if spy is None:
            return None
        rows = spy[spy["date"] > report_date]
        if rows.empty:
            return None
        return pd.Timestamp(rows.iloc[0]["date"])

    def observe(self, ticker: str, report_date: pd.Timestamp) -> PriceObservation:
        pricing_symbol = PRICE_SYMBOL_MAP.get(ticker, ticker)
        intended = self.next_us_session(report_date)
        empty = PriceObservation(
            ticker=ticker,
            pricing_symbol=pricing_symbol,
            intended_start_date=intended if intended is not None else pd.NaT,
            start_date=None,
            start_open=float("nan"),
            start_adj_open=float("nan"),
            end_date=None,
            end_close=float("nan"),
            end_adj_close=float("nan"),
            total_return=float("nan"),
            price_return=float("nan"),
            zero_volume_days=0,
            data_status="missing",
            aggregate_eligible=False,
            exclusion_reason="无行情序列",
        )
        frame = self.by_symbol.get(pricing_symbol)
        if frame is None or frame.empty or intended is None:
            return empty
        start = frame[frame["date"] == intended]
        end_exact = frame[frame["date"] == END_DATE]
        end_any = frame[frame["date"] <= END_DATE]
        if start.empty:
            last = end_any.iloc[-1] if not end_any.empty else None
            empty.end_date = pd.Timestamp(last["date"]) if last is not None else None
            empty.end_close = safe_float(last["close"]) if last is not None else float("nan")
            empty.end_adj_close = safe_float(last["adj_close"]) if last is not None else float("nan")
            empty.data_status = "missing_intended_entry_session"
            empty.exclusion_reason = "报告日后首个美股交易日没有该证券可成交报价"
            return empty
        s = start.iloc[0]
        e = end_exact.iloc[-1] if not end_exact.empty else (end_any.iloc[-1] if not end_any.empty else None)
        open_price = safe_float(s["open"])
        close_at_start = safe_float(s["close"])
        adj_at_start = safe_float(s["adj_close"])
        adj_open = (
            open_price * adj_at_start / close_at_start
            if all(math.isfinite(x) and x != 0 for x in [open_price, close_at_start, adj_at_start])
            else float("nan")
        )
        end_close = safe_float(e["close"]) if e is not None else float("nan")
        end_adj = safe_float(e["adj_close"]) if e is not None else float("nan")
        total_return = end_adj / adj_open - 1 if math.isfinite(adj_open) and adj_open != 0 and math.isfinite(end_adj) else float("nan")
        price_return = end_close / open_price - 1 if math.isfinite(open_price) and open_price != 0 and math.isfinite(end_close) else float("nan")
        period = frame[(frame["date"] >= intended) & (frame["date"] <= END_DATE)]
        zero_days = int((pd.to_numeric(period["volume"], errors="coerce").fillna(0) == 0).sum())
        reasons: list[str] = []
        eligible = True
        end_date = pd.Timestamp(e["date"]) if e is not None else None
        if end_date != END_DATE:
            eligible = False
            reasons.append(f"终点无 2026-09-18 报价，最近为 {end_date.date() if end_date is not None else 'NA'}")
        if ticker in AGGREGATE_EXCLUSIONS:
            eligible = False
            reasons.append(AGGREGATE_EXCLUSIONS[ticker])
        if not math.isfinite(total_return):
            eligible = False
            reasons.append("收益无法计算")
        if zero_days > max(5, int(len(period) * 0.5)):
            reasons.append(f"区间内零成交日 {zero_days} 天")
        status = "ok" if eligible else "excluded_from_aggregate"
        if reasons and eligible:
            status = "ok_with_liquidity_flag"
        return PriceObservation(
            ticker=ticker,
            pricing_symbol=pricing_symbol,
            intended_start_date=intended,
            start_date=pd.Timestamp(s["date"]),
            start_open=open_price,
            start_adj_open=adj_open,
            end_date=end_date,
            end_close=end_close,
            end_adj_close=end_adj,
            total_return=total_return,
            price_return=price_return,
            zero_volume_days=zero_days,
            data_status=status,
            aggregate_eligible=eligible,
            exclusion_reason="；".join(reasons),
        )

    def portfolio_mdd(self, tickers: list[str], report_date: pd.Timestamp) -> float:
        start_date = self.next_us_session(report_date)
        if start_date is None:
            return float("nan")
        series: list[pd.Series] = []
        for ticker in tickers:
            obs = self.observe(ticker, report_date)
            if not obs.aggregate_eligible or not math.isfinite(obs.start_adj_open):
                continue
            frame = self.by_symbol[obs.pricing_symbol]
            sub = frame[(frame["date"] >= start_date) & (frame["date"] <= END_DATE)][["date", "adj_close"]].copy()
            if sub.empty:
                continue
            s = sub.set_index("date")["adj_close"].astype(float) / obs.start_adj_open
            s.loc[start_date - pd.Timedelta(microseconds=1)] = 1.0
            series.append(s.sort_index().rename(ticker))
        if not series:
            return float("nan")
        panel = pd.concat(series, axis=1).sort_index().ffill()
        panel = panel.dropna(how="all")
        portfolio = panel.mean(axis=1, skipna=True)
        drawdown = portfolio / portfolio.cummax() - 1
        return float(drawdown.min())


def load_metadata() -> pd.DataFrame:
    meta = pd.read_csv(META_PATH, usecols=["ticker", "company", "category"])
    meta.drop_duplicates("ticker", inplace=True)
    alias = meta[meta["ticker"] == "P"].copy()
    if not alias.empty:
        alias["ticker"] = "PSTG"
        meta = pd.concat([meta, alias], ignore_index=True)
    return meta


def load_reports(meta: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return normalized full ranking rows and a report manifest."""
    report_frames: list[pd.DataFrame] = []
    report_manifest: list[dict[str, object]] = []

    old = pd.read_csv(OLD_RANK_PATH)
    old["report_date"] = pd.to_datetime(old["generation_date"])
    old["report_key"] = (
        "retained61::"
        + old["scheme_id"].astype(str).str.zfill(2)
        + "::"
        + old["version"].astype(str)
        + "::"
        + old["generation_date"].astype(str)
    )
    old["report_family"] = "排序-历史保留61版"
    old["report_type"] = "原始全榜"
    old["report_name"] = old["scheme"].astype(str) + "｜" + old["version"].astype(str)
    old["method_or_dimension"] = old["scheme_id"].astype(str).str.zfill(2)
    old["is_derived"] = False
    old["cohort"] = "2026-05-25至2026-06-22"
    old["source_path"] = old["source"].map(lambda x: str(ROOT / "分析报告" / "公司排序" / str(x)))
    old["score"] = pd.to_numeric(old["score"], errors="coerce")
    old["rank"] = pd.to_numeric(old["rank"], errors="coerce")
    old["full_universe_available"] = True

    manifest = pd.read_csv(OLD_MANIFEST_PATH)
    manifest["generation_date"] = pd.to_datetime(manifest["generation_date"])
    manifest["source_last_write_time"] = pd.to_datetime(manifest["source_last_write_time"], errors="coerce", utc=True)
    manifest.sort_values(["scheme_id", "generation_date", "source_last_write_time", "version"], inplace=True)
    latest = manifest.groupby("scheme_id", as_index=False).tail(1)
    latest_keys = set(
        "retained61::"
        + latest["scheme_id"].astype(str).str.zfill(2)
        + "::"
        + latest["version"].astype(str)
        + "::"
        + latest["generation_date"].dt.strftime("%Y-%m-%d")
    )
    old["is_latest_within_scheme"] = old["report_key"].isin(latest_keys)
    report_frames.append(old)

    july = pd.read_csv(JULY_RANK_PATH)
    july["report_date"] = pd.to_datetime(july["run_date"])
    july["report_key"] = "july28::" + july["list_id"].astype(str)
    july["report_family"] = "排序-2026-07-13正式28榜"
    july["report_type"] = "原始全榜"
    july["report_name"] = july["list_name"].astype(str)
    july["method_or_dimension"] = july["list_id"].astype(str)
    july["is_derived"] = False
    july["cohort"] = "2026-07-13"
    july["source_path"] = july["source_path"].astype(str).str.replace(r"D:\drive\Investment", str(ROOT), regex=False)
    july["score"] = pd.to_numeric(july["score"], errors="coerce")
    july["rank"] = pd.to_numeric(july["rank"], errors="coerce")
    july["full_universe_available"] = True
    july["is_latest_within_scheme"] = True
    report_frames.append(july)

    for spec in EXTRA_RANKINGS:
        extra = pd.read_csv(spec["csv"]).rename(columns=spec["columns"])
        extra["report_date"] = pd.Timestamp(spec["date"])
        extra["report_key"] = "backup4::" + spec["id"]
        extra["report_family"] = "排序-备份完整旧榜4份"
        extra["report_type"] = "原始全榜（备份）"
        extra["report_name"] = spec["name"]
        extra["method_or_dimension"] = spec["id"]
        extra["is_derived"] = False
        extra["cohort"] = spec["date"]
        extra["source_path"] = str(spec["report"])
        extra["rank"] = pd.to_numeric(extra["rank"], errors="coerce")
        extra["score"] = pd.to_numeric(extra["score"], errors="coerce")
        extra["full_universe_available"] = True
        extra["is_latest_within_scheme"] = True
        extra["dependency_note"] = spec["dependency_note"]
        report_frames.append(extra)

    june_compare = pd.read_csv(COMPARE_JUNE_PATH)
    june_compare["report_date"] = pd.to_datetime(june_compare["report_date"])
    june_compare["report_key"] = "comparison::2026-06-23::overall"
    june_compare["report_family"] = "对比-2026-06-23原报告派生榜"
    june_compare["report_type"] = "派生全榜（按逐公司报告净胜场重建）"
    june_compare["report_name"] = "2026-06-23逐公司对比｜overall"
    june_compare["method_or_dimension"] = "overall"
    june_compare["is_derived"] = True
    june_compare["cohort"] = "2026-06-23"
    june_compare["source_path"] = str(COMPARE_JUNE_PATH)
    june_compare["rank"] = pd.to_numeric(june_compare["original_rank"], errors="coerce")
    june_compare["score"] = pd.to_numeric(june_compare["net_wins"], errors="coerce")
    june_compare["full_universe_available"] = True
    june_compare["is_latest_within_scheme"] = True
    june_compare["dependency_note"] = "基于189份逐公司对比报告的净胜场重建；不是原报告发布的官方总榜"
    report_frames.append(june_compare)

    comparison = pd.read_csv(COMPARE_RANK_PATH)
    comparison = comparison[(comparison["variant"] == "both")].copy()
    comparison["report_date"] = pd.to_datetime(comparison["cohort"].map({"original_0714": "2026-07-14", "latest_0718": "2026-07-18"}))
    comparison["report_key"] = "comparison::" + comparison["cohort"].astype(str) + "::" + comparison["dimension"].astype(str)
    comparison["report_family"] = "对比-原报告派生全局榜"
    comparison["report_type"] = "派生全榜（原报告未发布全局Top30）"
    comparison["report_name"] = comparison["cohort"].astype(str) + "｜" + comparison["dimension"].astype(str) + "｜both"
    comparison["method_or_dimension"] = comparison["dimension"].astype(str)
    comparison["is_derived"] = True
    comparison["source_path"] = str(COMPARE_RANK_PATH)
    comparison["score"] = pd.to_numeric(comparison["points"], errors="coerce")
    comparison["rank"] = pd.to_numeric(comparison["rank"], errors="coerce")
    comparison["full_universe_available"] = True
    comparison["is_latest_within_scheme"] = comparison["cohort"].eq("latest_0718")
    report_frames.append(comparison)

    snapshots = pd.read_csv(SCENARIO_SNAPSHOTS_PATH)
    snapshots["underlying_report_date"] = snapshots["report_date"]
    snapshots["underlying_source_path"] = snapshots["source_path"]
    snapshots["snapshot_date"] = pd.to_datetime(snapshots["snapshot_date"])
    snapshots["report_date"] = snapshots["snapshot_date"]
    snapshots["rating_normalized"] = snapshots["rating"].map(normalize_rating)
    snapshots["rating_score"] = snapshots["rating_normalized"].map(RATING_SCORE)
    snapshots["predicted_midpoint_pct"] = (
        pd.to_numeric(snapshots["return_low"], errors="coerce")
        + pd.to_numeric(snapshots["return_high"], errors="coerce")
    ) / 2
    for snapshot_date, scenario in snapshots.groupby("snapshot_date", sort=True):
        scenario = scenario.copy()
        scenario.sort_values(["rating_score", "predicted_midpoint_pct", "ticker"], ascending=[False, False, True], inplace=True)
        scenario["rank"] = np.arange(1, len(scenario) + 1)
        scenario["score"] = scenario["rating_score"] * 1000 + scenario["predicted_midpoint_pct"].fillna(-999)
        date_text = pd.Timestamp(snapshot_date).strftime("%Y-%m-%d")
        scenario["report_key"] = f"scenario::{date_text}::latest_asof_rating_midpoint"
        scenario["report_family"] = "情景-最新可用评级机械榜"
        scenario["report_type"] = "派生全榜（截至该日最新报告；评级优先、目标回报区间中点破同分）"
        scenario["report_name"] = f"{date_text}情景决策latest-as-of机械榜"
        scenario["method_or_dimension"] = "rating_then_midpoint"
        scenario["is_derived"] = True
        scenario["cohort"] = date_text
        scenario["source_path"] = str(SCENARIO_SNAPSHOTS_PATH)
        scenario["full_universe_available"] = True
        scenario["is_latest_within_scheme"] = date_text == "2026-09-05"
        scenario["dependency_note"] = "192家公司latest-as-of快照；并非原报告发布的全局Top30"
        report_frames.append(scenario)

    keep = [
        "report_key",
        "report_family",
        "report_type",
        "report_name",
        "method_or_dimension",
        "cohort",
        "report_date",
        "source_path",
        "is_derived",
        "full_universe_available",
        "is_latest_within_scheme",
        "rank",
        "ticker",
        "score",
    ]
    optional = ["scheme_id", "scheme", "family", "version", "list_id", "list_name", "dimension", "variant", "rating_normalized", "rating_score", "predicted_midpoint_pct", "dependency_note", "underlying_report_date", "underlying_source_path"]
    normalized: list[pd.DataFrame] = []
    for frame in report_frames:
        f = frame.copy()
        for col in optional:
            if col not in f.columns:
                f[col] = np.nan
        normalized.append(f[keep + optional])
    reports = pd.concat(normalized, ignore_index=True, sort=False)
    reports["ticker"] = reports["ticker"].astype(str).str.strip()
    reports = reports.merge(meta, how="left", on="ticker")
    # One row per report manifest, preserving declared population size.
    for key, g in reports.groupby("report_key", sort=False):
        first = g.iloc[0]
        report_manifest.append(
            {
                "report_key": key,
                "report_family": first["report_family"],
                "report_type": first["report_type"],
                "report_name": first["report_name"],
                "method_or_dimension": first["method_or_dimension"],
                "cohort": first["cohort"],
                "report_date": first["report_date"],
                "source_path": first["source_path"],
                "is_derived": bool(first["is_derived"]),
                "is_latest_within_scheme": bool(first["is_latest_within_scheme"]),
                "declared_rows": int(len(g)),
                "unique_tickers": int(g["ticker"].nunique()),
                "unique_ranks": int(g["rank"].nunique()),
            }
        )
    return reports, pd.DataFrame(report_manifest)


def add_price_observations(reports: pd.DataFrame, book: PriceBook) -> pd.DataFrame:
    cache: dict[tuple[str, pd.Timestamp], PriceObservation] = {}
    benchmark_cache: dict[tuple[str, pd.Timestamp], PriceObservation] = {}
    out_rows: list[dict[str, object]] = []
    for row in reports.itertuples(index=False):
        report_date = pd.Timestamp(row.report_date)
        key = (str(row.ticker), report_date)
        obs = cache.setdefault(key, book.observe(str(row.ticker), report_date))
        result = row._asdict()
        result.update(
            {
                "pricing_symbol": obs.pricing_symbol,
                "intended_start_date": obs.intended_start_date,
                "start_trade_date": obs.start_date,
                "start_open": obs.start_open,
                "start_adj_open": obs.start_adj_open,
                "end_trade_date": obs.end_date,
                "end_close": obs.end_close,
                "end_adj_close": obs.end_adj_close,
                "total_return": obs.total_return,
                "price_return": obs.price_return,
                "zero_volume_days": obs.zero_volume_days,
                "data_status": obs.data_status,
                "aggregate_eligible": obs.aggregate_eligible,
                "exclusion_reason": obs.exclusion_reason,
            }
        )
        for benchmark in BENCHMARKS:
            bkey = (benchmark, report_date)
            b = benchmark_cache.setdefault(bkey, book.observe(benchmark, report_date))
            result[f"{benchmark.lower()}_return"] = b.total_return
            result[f"excess_{benchmark.lower()}"] = obs.total_return - b.total_return if math.isfinite(obs.total_return) and math.isfinite(b.total_return) else float("nan")
        out_rows.append(result)
    out = pd.DataFrame(out_rows)
    out["rank"] = pd.to_numeric(out["rank"], errors="coerce")
    return out


def spearman(x: pd.Series, y: pd.Series) -> float:
    good = pd.DataFrame({"x": pd.to_numeric(x, errors="coerce"), "y": pd.to_numeric(y, errors="coerce")}).dropna()
    if len(good) < 5 or good["x"].nunique() < 2 or good["y"].nunique() < 2:
        return float("nan")
    return float(good["x"].rank(method="average").corr(good["y"].rank(method="average"), method="pearson"))


def report_metrics(enriched: pd.DataFrame, manifest: pd.DataFrame, book: PriceBook) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for report_key, g0 in enriched.groupby("report_key", sort=False):
        g = g0[g0["aggregate_eligible"]].copy()
        top = g[g["rank"] <= 30].copy()
        bottom = g.nlargest(30, "rank").copy() if not g.empty else g.copy()
        first = g0.iloc[0]
        universe_ret = float(g["total_return"].mean()) if not g.empty else float("nan")
        top_ret = float(top["total_return"].mean()) if not top.empty else float("nan")
        bottom_ret = float(bottom["total_return"].mean()) if not bottom.empty else float("nan")
        residual = g["total_return"] - g.groupby("category", dropna=False)["total_return"].transform("mean") if not g.empty else pd.Series(dtype=float)
        rank_ic = spearman(-g["rank"], g["total_return"]) if not g.empty else float("nan")
        cat_ic = spearman(-g["rank"], residual) if not g.empty else float("nan")
        mdd = book.portfolio_mdd(top["ticker"].tolist(), pd.Timestamp(first["report_date"])) if not top.empty else float("nan")
        benchmark_values = {b: float(top[f"{b.lower()}_return"].iloc[0]) if not top.empty else float("nan") for b in BENCHMARKS}
        rows.append(
            {
                "report_key": report_key,
                "report_family": first["report_family"],
                "report_type": first["report_type"],
                "report_name": first["report_name"],
                "method_or_dimension": first["method_or_dimension"],
                "cohort": first["cohort"],
                "report_date": pd.Timestamp(first["report_date"]).date(),
                "start_trade_date": top["start_trade_date"].dropna().min().date() if not top["start_trade_date"].dropna().empty else None,
                "end_trade_date": END_DATE.date(),
                "source_path": first["source_path"],
                "is_derived": bool(first["is_derived"]),
                "is_latest_within_scheme": bool(first["is_latest_within_scheme"]),
                "n_declared": int(len(g0)),
                "n_eligible": int(len(g)),
                "top30_n_eligible": int(len(top)),
                "top30_return": top_ret,
                "top30_median_return": float(top["total_return"].median()) if not top.empty else float("nan"),
                "top30_positive_rate": float((top["total_return"] > 0).mean()) if not top.empty else float("nan"),
                "top30_mdd": mdd,
                "universe_return": universe_ret,
                "bottom30_return": bottom_ret,
                "top30_minus_universe": top_ret - universe_ret,
                "top30_minus_bottom30": top_ret - bottom_ret,
                "spy_return": benchmark_values["SPY"],
                "qqq_return": benchmark_values["QQQ"],
                "soxx_return": benchmark_values["SOXX"],
                "top30_excess_spy": top_ret - benchmark_values["SPY"],
                "top30_excess_qqq": top_ret - benchmark_values["QQQ"],
                "top30_excess_soxx": top_ret - benchmark_values["SOXX"],
                "rank_ic": rank_ic,
                "category_neutral_rank_ic": cat_ic,
                "top30_tickers": ",".join(top.sort_values("rank")["ticker"].tolist()),
                "excluded_tickers": ",".join(sorted(set(g0.loc[~g0["aggregate_eligible"], "ticker"].astype(str)))),
            }
        )
    metrics = pd.DataFrame(rows)
    return manifest.merge(metrics, how="left", on=[
        "report_key",
        "report_family",
        "report_type",
        "report_name",
        "method_or_dimension",
        "cohort",
        "report_date",
        "source_path",
        "is_derived",
        "is_latest_within_scheme",
    ]) if False else metrics


def family_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for family, g in metrics.groupby("report_family", sort=False):
        rows.append(
            {
                "report_family": family,
                "report_count": int(len(g)),
                "original_report_count": int((~g["is_derived"]).sum()),
                "derived_report_count": int(g["is_derived"].sum()),
                "median_top30_return": float(g["top30_return"].median()),
                "median_top30_excess_spy": float(g["top30_excess_spy"].median()),
                "median_top30_excess_qqq": float(g["top30_excess_qqq"].median()),
                "median_top30_minus_universe": float(g["top30_minus_universe"].median()),
                "median_top30_minus_bottom30": float(g["top30_minus_bottom30"].median()),
                "median_rank_ic": float(g["rank_ic"].median()),
                "share_top30_positive": float((g["top30_return"] > 0).mean()),
                "share_beating_spy": float((g["top30_excess_spy"] > 0).mean()),
                "share_beating_qqq": float((g["top30_excess_qqq"] > 0).mean()),
                "share_beating_universe": float((g["top30_minus_universe"] > 0).mean()),
                "share_positive_ic": float((g["rank_ic"] > 0).mean()),
                "best_report": g.loc[g["top30_excess_spy"].idxmax(), "report_name"] if g["top30_excess_spy"].notna().any() else "",
                "best_excess_spy": float(g["top30_excess_spy"].max()),
                "worst_report": g.loc[g["top30_excess_spy"].idxmin(), "report_name"] if g["top30_excess_spy"].notna().any() else "",
                "worst_excess_spy": float(g["top30_excess_spy"].min()),
            }
        )
    return pd.DataFrame(rows)


def scenario_group_metrics(enriched: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    scenarios = enriched[enriched["report_family"].eq("情景-最新可用评级机械榜")].copy()
    for cohort, snapshot0 in scenarios.groupby("cohort", sort=True):
        snapshot = snapshot0[snapshot0["aggregate_eligible"]].copy()
        for rating, g in snapshot.groupby("rating_normalized", sort=False):
            rows.append(
                {
                    "snapshot_date": cohort,
                    "rating": rating,
                    "rating_score": int(g["rating_score"].iloc[0]),
                    "n": int(len(g)),
                    "mean_return": float(g["total_return"].mean()),
                    "median_return": float(g["total_return"].median()),
                    "positive_rate": float((g["total_return"] > 0).mean()),
                    "mean_excess_spy": float(g["excess_spy"].mean()),
                    "mean_excess_qqq": float(g["excess_qqq"].mean()),
                    "mean_predicted_midpoint_pct": float(g["predicted_midpoint_pct"].mean()),
                    "rating_return_spearman": np.nan,
                    "midpoint_return_spearman": np.nan,
                }
            )
        rows.append(
            {
                "snapshot_date": cohort,
                "rating": "全体序数检验",
                "rating_score": np.nan,
                "n": int(len(snapshot)),
                "mean_return": float(snapshot["total_return"].mean()),
                "median_return": float(snapshot["total_return"].median()),
                "positive_rate": float((snapshot["total_return"] > 0).mean()),
                "mean_excess_spy": float(snapshot["excess_spy"].mean()),
                "mean_excess_qqq": float(snapshot["excess_qqq"].mean()),
                "mean_predicted_midpoint_pct": float(snapshot["predicted_midpoint_pct"].mean()),
                "rating_return_spearman": spearman(snapshot["rating_score"], snapshot["total_return"]),
                "midpoint_return_spearman": spearman(snapshot["predicted_midpoint_pct"], snapshot["total_return"]),
            }
        )
    return pd.DataFrame(rows).sort_values(["snapshot_date", "rating_score"], ascending=[True, False], na_position="last")


def scenario_report_backtest(book: PriceBook, meta: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Backtest all 440 de-duplicated dated scenario calls without pretending partial dates are full rankings."""
    calls = pd.read_csv(SCENARIO_REPORTS_PATH)
    calls["report_date"] = pd.to_datetime(calls["report_date"])
    calls["rating_normalized"] = calls["rating"].map(normalize_rating)
    calls["rating_score"] = calls["rating_normalized"].map(RATING_SCORE)
    calls["predicted_midpoint_pct"] = (
        pd.to_numeric(calls["return_low"], errors="coerce")
        + pd.to_numeric(calls["return_high"], errors="coerce")
    ) / 2
    calls = calls.merge(meta, how="left", on="ticker")
    rows: list[dict[str, object]] = []
    obs_cache: dict[tuple[str, pd.Timestamp], PriceObservation] = {}
    benchmark_cache: dict[tuple[str, pd.Timestamp], PriceObservation] = {}
    for row in calls.itertuples(index=False):
        dt = pd.Timestamp(row.report_date)
        key = (str(row.ticker), dt)
        obs = obs_cache.setdefault(key, book.observe(str(row.ticker), dt))
        result = row._asdict()
        result.update(
            {
                "pricing_symbol": obs.pricing_symbol,
                "intended_start_date": obs.intended_start_date,
                "start_trade_date": obs.start_date,
                "start_open": obs.start_open,
                "start_adj_open": obs.start_adj_open,
                "end_trade_date": obs.end_date,
                "end_close": obs.end_close,
                "end_adj_close": obs.end_adj_close,
                "total_return": obs.total_return,
                "price_return": obs.price_return,
                "zero_volume_days": obs.zero_volume_days,
                "data_status": obs.data_status,
                "aggregate_eligible": obs.aggregate_eligible,
                "exclusion_reason": obs.exclusion_reason,
            }
        )
        for benchmark in BENCHMARKS:
            b = benchmark_cache.setdefault((benchmark, dt), book.observe(benchmark, dt))
            result[f"{benchmark.lower()}_return"] = b.total_return
            result[f"excess_{benchmark.lower()}"] = obs.total_return - b.total_return if math.isfinite(obs.total_return) and math.isfinite(b.total_return) else np.nan
        rows.append(result)
    details = pd.DataFrame(rows)
    summary_rows: list[dict[str, object]] = []
    expected_counts = {"2026-07-13": 91, "2026-07-14": 114, "2026-07-15": 192, "2026-07-18": 16, "2026-08-19": 24, "2026-09-05": 3}
    for dt, date0 in details.groupby("report_date", sort=True):
        date_text = pd.Timestamp(dt).strftime("%Y-%m-%d")
        date_group = date0[date0["aggregate_eligible"]].copy()
        for rating, g in date_group.groupby("rating_normalized", sort=False):
            summary_rows.append(
                {
                    "report_date": date_text,
                    "scope": "完整192横截面" if date_text == "2026-07-15" else "当日新增/更新，非完整横截面",
                    "rating": rating,
                    "rating_score": int(g["rating_score"].iloc[0]),
                    "n": int(len(g)),
                    "date_declared_calls": expected_counts.get(date_text, int(len(date0))),
                    "mean_return": float(g["total_return"].mean()),
                    "median_return": float(g["total_return"].median()),
                    "positive_rate": float((g["total_return"] > 0).mean()),
                    "mean_excess_spy": float(g["excess_spy"].mean()),
                    "mean_excess_qqq": float(g["excess_qqq"].mean()),
                    "rating_return_spearman": np.nan,
                    "midpoint_return_spearman": np.nan,
                }
            )
        summary_rows.append(
            {
                "report_date": date_text,
                "scope": "完整192横截面" if date_text == "2026-07-15" else "当日新增/更新，非完整横截面",
                "rating": "当日全体序数检验",
                "rating_score": np.nan,
                "n": int(len(date_group)),
                "date_declared_calls": expected_counts.get(date_text, int(len(date0))),
                "mean_return": float(date_group["total_return"].mean()),
                "median_return": float(date_group["total_return"].median()),
                "positive_rate": float((date_group["total_return"] > 0).mean()),
                "mean_excess_spy": float(date_group["excess_spy"].mean()),
                "mean_excess_qqq": float(date_group["excess_qqq"].mean()),
                "rating_return_spearman": spearman(date_group["rating_score"], date_group["total_return"]),
                "midpoint_return_spearman": spearman(date_group["predicted_midpoint_pct"], date_group["total_return"]),
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values(["report_date", "rating_score"], ascending=[True, False], na_position="last")
    details.sort_values(["report_date", "ticker"], inplace=True)
    return details, summary


def company_consensus(top30: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    all_tickers = sorted(top30["ticker"].unique())
    family_denoms = {
        "retained_latest": top30.loc[(top30["report_family"] == "排序-历史保留61版") & top30["is_latest_within_scheme"], "report_key"].nunique(),
        "july28": top30.loc[top30["report_family"] == "排序-2026-07-13正式28榜", "report_key"].nunique(),
        "comparison_latest": top30.loc[(top30["report_family"] == "对比-原报告派生全局榜") & (top30["cohort"] == "latest_0718"), "report_key"].nunique(),
        "scenario": top30.loc[(top30["report_family"] == "情景-最新可用评级机械榜") & (top30["cohort"] == "2026-09-05"), "report_key"].nunique(),
    }
    for ticker in all_tickers:
        g = top30[top30["ticker"] == ticker]
        subset_defs = {
            "retained_latest": (g["report_family"] == "排序-历史保留61版") & g["is_latest_within_scheme"],
            "july28": g["report_family"] == "排序-2026-07-13正式28榜",
            "comparison_latest": (g["report_family"] == "对比-原报告派生全局榜") & (g["cohort"] == "latest_0718"),
            "scenario": (g["report_family"] == "情景-最新可用评级机械榜") & (g["cohort"] == "2026-09-05"),
        }
        shares = {}
        counts = {}
        for name, mask in subset_defs.items():
            counts[name] = int(g.loc[mask, "report_key"].nunique())
            shares[name] = counts[name] / family_denoms[name] if family_denoms[name] else np.nan
        valid_shares = [x for x in shares.values() if math.isfinite(x)]
        first = g.iloc[0]
        rows.append(
            {
                "ticker": ticker,
                "company": first.get("company", np.nan),
                "category": first.get("category", np.nan),
                "raw_top30_appearances": int(g["report_key"].nunique()),
                "retained61_appearances": int(g.loc[g["report_family"] == "排序-历史保留61版", "report_key"].nunique()),
                "retained_latest_appearances": counts["retained_latest"],
                "retained_latest_share": shares["retained_latest"],
                "july28_appearances": counts["july28"],
                "july28_share": shares["july28"],
                "comparison_latest_dimensions": counts["comparison_latest"],
                "comparison_latest_share": shares["comparison_latest"],
                "scenario_top30": counts["scenario"],
                "family_balanced_presence": float(np.mean(valid_shares)) if valid_shares else np.nan,
                "mean_realized_return_across_entries": float(g["total_return"].mean()),
                "median_realized_return_across_entries": float(g["total_return"].median()),
                "mean_excess_spy_across_entries": float(g["excess_spy"].mean()),
                "best_realized_return": float(g["total_return"].max()),
                "worst_realized_return": float(g["total_return"].min()),
            }
        )
    return pd.DataFrame(rows).sort_values(["family_balanced_presence", "raw_top30_appearances", "ticker"], ascending=[False, False, True])


def build_summary_json(metrics: pd.DataFrame, families: pd.DataFrame, scenario_groups: pd.DataFrame, consensus: pd.DataFrame, enriched: pd.DataFrame, prices: pd.DataFrame) -> dict[str, object]:
    retained = metrics[metrics["report_family"] == "排序-历史保留61版"]
    retained_latest = retained[retained["is_latest_within_scheme"]]
    july = metrics[metrics["report_family"] == "排序-2026-07-13正式28榜"]
    comparison = metrics[metrics["report_family"] == "对比-原报告派生全局榜"]
    scenario_metrics = metrics[metrics["report_family"] == "情景-最新可用评级机械榜"]
    top30 = enriched[(enriched["rank"] <= 30) & enriched["aggregate_eligible"]]

    def compact(g: pd.DataFrame) -> dict[str, object]:
        return {
            "report_count": int(len(g)),
            "median_top30_return": float(g["top30_return"].median()),
            "median_top30_excess_spy": float(g["top30_excess_spy"].median()),
            "median_top30_excess_qqq": float(g["top30_excess_qqq"].median()),
            "share_beating_spy": float((g["top30_excess_spy"] > 0).mean()),
            "share_beating_qqq": float((g["top30_excess_qqq"] > 0).mean()),
            "share_beating_universe": float((g["top30_minus_universe"] > 0).mean()),
            "median_rank_ic": float(g["rank_ic"].median()),
        }

    scenario_summary: dict[str, object] = {}
    for row in scenario_metrics.itertuples(index=False):
        cohort = str(row.cohort)
        overall = scenario_groups[(scenario_groups["snapshot_date"].astype(str) == cohort) & (scenario_groups["rating"] == "全体序数检验")]
        scenario_summary[cohort] = {
            key: (getattr(row, key).item() if hasattr(getattr(row, key), "item") else getattr(row, key))
            for key in ["top30_return", "top30_excess_spy", "top30_excess_qqq", "top30_minus_universe", "top30_minus_bottom30", "rank_ic", "top30_positive_rate", "top30_mdd", "top30_tickers"]
        }
        if not overall.empty:
            scenario_summary[cohort]["rating_return_spearman"] = float(overall["rating_return_spearman"].iloc[0])
            scenario_summary[cohort]["midpoint_return_spearman"] = float(overall["midpoint_return_spearman"].iloc[0])

    return {
        "as_of": str(END_DATE.date()),
        "price_rows": int(len(prices)),
        "price_symbols": int(prices["symbol"].nunique()),
        "report_count": int(metrics["report_key"].nunique()),
        "top30_detail_rows": int(len(top30)),
        "retained_all_61": compact(retained),
        "retained_latest_by_scheme": compact(retained_latest),
        "july_28": compact(july),
        "comparison_14_derived": compact(comparison),
        "scenario_mechanical_by_snapshot": scenario_summary,
        "best_reports_by_excess_spy": metrics.nlargest(10, "top30_excess_spy")[["report_key", "report_family", "report_name", "report_date", "top30_return", "top30_excess_spy", "rank_ic"]].to_dict("records"),
        "worst_reports_by_excess_spy": metrics.nsmallest(10, "top30_excess_spy")[["report_key", "report_family", "report_name", "report_date", "top30_return", "top30_excess_spy", "rank_ic"]].to_dict("records"),
        "family_balanced_top30": consensus.head(30).to_dict("records"),
        "input_hashes": {
            str(path): sha256_file(path)
            for path in [OLD_RANK_PATH, OLD_MANIFEST_PATH, JULY_RANK_PATH, SCENARIO_PATH, SCENARIO_REPORTS_PATH, SCENARIO_SNAPSHOTS_PATH, META_PATH, COMPARE_RANK_PATH, COMPARE_JUNE_PATH, LOCAL_PRICE_PATH, *[x["csv"] for x in EXTRA_RANKINGS]]
        },
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = load_metadata()
    reports, manifest = load_reports(meta)
    all_symbols = sorted(set(reports["ticker"].map(lambda x: PRICE_SYMBOL_MAP.get(str(x), str(x)))) | set(BENCHMARKS))
    prices = load_prices(all_symbols)
    book = PriceBook(prices)
    enriched = add_price_observations(reports, book)
    metrics = report_metrics(enriched, manifest, book)
    families = family_summary(metrics)
    scenario_groups = scenario_group_metrics(enriched)
    scenario_calls, scenario_call_summary = scenario_report_backtest(book, meta)
    top30 = enriched[enriched["rank"] <= 30].copy()
    consensus = company_consensus(top30[top30["aggregate_eligible"]])
    summary = build_summary_json(metrics, families, scenario_groups, consensus, enriched, prices)

    # Stable output order for auditability.
    metrics.sort_values(["report_family", "report_date", "report_key"], inplace=True)
    top30.sort_values(["report_family", "report_date", "report_key", "rank"], inplace=True)
    manifest.sort_values(["report_family", "report_date", "report_key"], inplace=True)
    prices.sort_values(["symbol", "date"], inplace=True)

    manifest.to_csv(OUT / "01_样本清单.csv", index=False, encoding="utf-8-sig")
    metrics.to_csv(OUT / "02_全部报告回测指标.csv", index=False, encoding="utf-8-sig")
    top30.to_csv(OUT / "03_所有报告Top30逐股明细.csv", index=False, encoding="utf-8-sig")
    consensus.to_csv(OUT / "04_Top30跨报告共识.csv", index=False, encoding="utf-8-sig")
    scenario_groups.to_csv(OUT / "05_情景评级分组回测.csv", index=False, encoding="utf-8-sig")
    families.to_csv(OUT / "06_报告家族汇总.csv", index=False, encoding="utf-8-sig")
    prices.to_csv(OUT / "07_行情缓存_截至2026-09-18.csv", index=False, encoding="utf-8-sig")
    (OUT / "08_机器可读摘要.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    scenario_calls.to_csv(OUT / "09_情景逐报告回测明细.csv", index=False, encoding="utf-8-sig")
    scenario_call_summary.to_csv(OUT / "10_情景逐报告日期评级汇总.csv", index=False, encoding="utf-8-sig")

    print(json.dumps({"outputs": str(OUT), "reports": len(metrics), "top30_rows": len(top30), "price_symbols": prices["symbol"].nunique()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
