from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(r"D:\drive\Investment")
RANK_ROOT = ROOT / "基本面" / "分析报告" / "公司排序"
INDEX_FILE = ROOT / "基本面" / "公司调研" / "公司索引.md"
OUT = RANK_ROOT / "tmp" / "2026-07-13_26方案3m6m评估"

PRICE_END = pd.Timestamp("2026-07-10")
DOWNLOAD_START = "2025-12-15"
DOWNLOAD_END_EXCLUSIVE = "2026-07-11"
BENCHMARKS = ["SPY", "QQQ", "SOXX"]
ACTIVE_CONTAINERS = {
    "01_暂时有效_核心",
    "02_暂时有效_辅助",
    "03_观察_待更新",
    "04_冻结_待重构",
    "05_退出与历史备份",
    "06_候选新方案_待验证",
    "07_输入扩展对照方案_待验证",
}


# Each selector is (H2 prefix, optional H3 prefix).  Method 06 intentionally
# emits three complete rankings and is handled separately below.
SELECTORS: dict[str, list[tuple[str, str | None]]] = {
    "01": [("六、完整连续排名", None)],
    "02": [("七、完整连续排名", None)],
    "03": [("八、全样本连续排名", None)],
    "04": [("六、全样本连续排名", None)],
    "05": [("六、完整连续排名", None)],
    "07": [("全样本连续排名", None)],
    "08": [("七、完整连续排名", None)],
    "09": [("五、全样本连续排名", None)],
    "10": [("六、全样本连续排名", None)],
    "11": [("Top20", None), ("完整连续排名", None), ("Bottom20", None)],
    "12": [("七、全样本连续排名", None)],
    "13": [("八、完整连续排名", None)],
    "14": [("六、完整连续排名", None)],
    "15": [("五、全样本连续排名", None)],
    "16": [("全样本连续排名", None)],
    "17": [("6. 全样本连续排名", None)],
    "N01": [("六、完整连续排名", None)],
    "N02": [("完整连续排名", None)],
    "N03": [("六、完整连续排名", None)],
    "N04": [("五、完整连续排名", None)],
    "N05": [("七、完整排名", None)],
    "N06": [("六、完整排名", None)],
    "E01": [("4. 横截面排序", "4.4 完整连续排名")],
    "E02": [("八、完整连续排名", None)],
    "E03": [("七、完整排名", None)],
}

METHOD06_LISTS = {
    "06F": "五、基本面性价比完整排名",
    "06G": "六、激进成长完整排名",
    "06E": "七、财报事件与右尾弹性完整排名",
}


def split_md_row(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [part.replace(r"\|", "|").strip() for part in re.split(r"(?<!\\)\|", raw)]


def norm_header(value: str) -> str:
    return re.sub(r"[\s*`_：:/（）()\-—]", "", value)


def clean_cell(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"[*`_]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells)


def selector_match(h2: str, h3: str, selectors: list[tuple[str, str | None]]) -> bool:
    return any(h2.startswith(want_h2) and (want_h3 is None or h3.startswith(want_h3)) for want_h2, want_h3 in selectors)


def read_index() -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
        cells = split_md_row(line) if line.lstrip().startswith("|") else []
        if len(cells) >= 3 and re.fullmatch(r"[A-Z][A-Z0-9.]{0,9}", cells[0].strip()):
            rows.append({"ticker": cells[0].strip(), "company": clean_cell(cells[1]), "category": clean_cell(cells[2]).strip("`")})
    frame = pd.DataFrame(rows).drop_duplicates("ticker")
    if len(frame) != 192:
        raise RuntimeError(f"company index expected 192 tickers, got {len(frame)}")
    return frame


def result_files() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for path in RANK_ROOT.rglob("02_排序结果.md"):
        if "2026-07-12_独立自洽版" not in str(path):
            continue
        # Root-level legacy compatibility links/directories can expose some of
        # the same runs a second time.  The 26 canonical jobs live only inside
        # the seven active lifecycle containers.
        if path.parents[3].name not in ACTIVE_CONTAINERS:
            continue
        method_dir = path.parents[2]
        method_id = method_dir.name.split("_", 1)[0]
        if method_id in found:
            raise RuntimeError(f"duplicate standalone result for {method_id}: {path} and {found[method_id]}")
        found[method_id] = path
    return dict(sorted(found.items()))


def parse_rank_rows(path: Path, selectors: list[tuple[str, str | None]]) -> tuple[pd.DataFrame, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    h2 = ""
    h3 = ""
    active_header: list[str] | None = None
    active_rank_col: int | None = None
    active_ticker_col: int | None = None
    active_score_col: int | None = None
    rows: list[dict[str, object]] = []
    parsing_notes: list[str] = []

    for idx, line in enumerate(lines):
        if line.startswith("## "):
            h2 = line[3:].strip()
            h3 = ""
            active_header = None
        elif line.startswith("### "):
            h3 = line[4:].strip()
            active_header = None

        if not selector_match(h2, h3, selectors) or not line.lstrip().startswith("|"):
            continue

        cells = split_md_row(line)
        next_cells = split_md_row(lines[idx + 1]) if idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith("|") else []
        if next_cells and is_separator(next_cells):
            active_header = cells
            normalized = [norm_header(c) for c in cells]
            rank_candidates = [
                i for i, c in enumerate(normalized)
                if c in {"排名", "名次", "最终排名", "样本排名"}
                or (c.endswith("排名") and "原始" not in c)
            ]
            ticker_candidates = [i for i, c in enumerate(normalized) if "代码" in c or "股票代号" in c]
            score_candidates = [i for i, c in enumerate(normalized) if c in {"综合分", "总分", "生存分", "最终分", "分数", "可投资价值分"}]
            active_rank_col = rank_candidates[0] if rank_candidates else None
            active_ticker_col = ticker_candidates[0] if ticker_candidates else None
            active_score_col = score_candidates[0] if score_candidates else None
            continue
        if is_separator(cells) or active_header is None or active_rank_col is None or active_ticker_col is None:
            continue
        if len(cells) <= max(active_rank_col, active_ticker_col):
            continue

        rank_cell = clean_cell(cells[active_rank_col])
        rank_match = re.match(r"^(\d{1,3})(?:\D|$)", rank_cell)
        ticker_cell = clean_cell(cells[active_ticker_col]).upper()
        ticker_match = re.match(r"^([A-Z][A-Z0-9.]{0,9})(?:\b|\s|/|·|$)", ticker_cell)
        if not rank_match or not ticker_match:
            continue
        rank = int(rank_match.group(1))
        if not 1 <= rank <= 192:
            continue
        score = np.nan
        if active_score_col is not None and active_score_col < len(cells):
            number = re.search(r"[-+]?\d+(?:\.\d+)?", clean_cell(cells[active_score_col]).replace(",", ""))
            if number:
                score = float(number.group())
        rows.append({"rank": rank, "ticker": ticker_match.group(1), "score": score, "h2": h2, "h3": h3, "line": idx + 1})

    raw = pd.DataFrame(rows)
    if raw.empty:
        return raw, ["no ranking rows parsed"]
    conflicts = []
    for rank, group in raw.groupby("rank"):
        if group["ticker"].nunique() > 1:
            conflicts.append(f"rank {rank}: {','.join(sorted(group['ticker'].unique()))}")
    for ticker, group in raw.groupby("ticker"):
        if group["rank"].nunique() > 1:
            conflicts.append(f"ticker {ticker}: {','.join(map(str, sorted(group['rank'].unique())))}")
    if conflicts:
        parsing_notes.extend(conflicts)

    # Exact repeats from Top/Bottom excerpts are harmless.  Any conflicting row
    # remains visible in parsing_notes and the first source row is retained.
    result = raw.sort_values(["rank", "line"]).drop_duplicates("rank", keep="first")
    result = result.drop_duplicates("ticker", keep="first").sort_values("rank").reset_index(drop=True)
    return result, parsing_notes


def ranking_audit_row(method_id: str, list_id: str, method_name: str, path: Path, rank: pd.DataFrame, notes: list[str], index_tickers: set[str]) -> dict[str, object]:
    ranks = set(rank["rank"].astype(int)) if not rank.empty else set()
    tickers = set(rank["ticker"].astype(str)) if not rank.empty else set()
    return {
        "method_id": method_id,
        "list_id": list_id,
        "method_name": method_name,
        "result_path": str(path),
        "result_bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "row_count": len(rank),
        "unique_ranks": len(ranks),
        "unique_tickers": len(tickers),
        "min_rank": min(ranks) if ranks else np.nan,
        "max_rank": max(ranks) if ranks else np.nan,
        "missing_ranks": ",".join(map(str, sorted(set(range(1, 193)) - ranks))),
        "missing_tickers": ",".join(sorted(index_tickers - tickers)),
        "unexpected_tickers": ",".join(sorted(tickers - index_tickers)),
        "parse_conflicts": " | ".join(notes),
        "structurally_valid": len(rank) == 192 and ranks == set(range(1, 193)) and tickers == index_tickers and not notes,
    }


def fetch_histories(symbols: list[str]) -> tuple[dict[str, pd.DataFrame], dict[str, str]]:
    histories: dict[str, pd.DataFrame] = {}
    failures: dict[str, str] = {}

    def extract(data: pd.DataFrame, symbol: str) -> pd.DataFrame | None:
        try:
            if isinstance(data.columns, pd.MultiIndex):
                if ("Adj Close", symbol) in data.columns:
                    frame = data.loc[:, [("Adj Close", symbol), ("Close", symbol)]].copy()
                    frame.columns = ["adj_close", "close"]
                elif (symbol, "Adj Close") in data.columns:
                    frame = data.loc[:, [(symbol, "Adj Close"), (symbol, "Close")]].copy()
                    frame.columns = ["adj_close", "close"]
                else:
                    return None
            else:
                frame = data[["Adj Close", "Close"]].copy()
                frame.columns = ["adj_close", "close"]
            frame = frame.dropna(subset=["adj_close"])
            frame.index = pd.to_datetime(frame.index).tz_localize(None)
            return frame.sort_index() if not frame.empty else None
        except Exception:
            return None

    for start in range(0, len(symbols), 28):
        chunk = symbols[start : start + 28]
        try:
            data = yf.download(chunk, start=DOWNLOAD_START, end=DOWNLOAD_END_EXCLUSIVE, auto_adjust=False, actions=False, progress=False, threads=True, timeout=30)
            for symbol in chunk:
                frame = extract(data, symbol)
                if frame is not None:
                    histories[symbol] = frame
        except Exception as exc:
            for symbol in chunk:
                failures[symbol] = f"batch: {type(exc).__name__}: {exc}"
        time.sleep(0.15)

    missing = [s for s in symbols if s not in histories]
    for symbol in missing:
        try:
            data = yf.download(symbol, start=DOWNLOAD_START, end=DOWNLOAD_END_EXCLUSIVE, auto_adjust=False, actions=False, progress=False, threads=False, timeout=30)
            frame = extract(data, symbol)
            if frame is not None:
                histories[symbol] = frame
                failures.pop(symbol, None)
            else:
                failures[symbol] = "no adjusted-close observations"
        except Exception as exc:
            failures[symbol] = f"single: {type(exc).__name__}: {exc}"
        time.sleep(0.08)
    return histories, failures


def trailing_return(frame: pd.DataFrame, months: int) -> dict[str, object]:
    hist = frame[frame.index <= PRICE_END].dropna(subset=["adj_close"])
    target = PRICE_END - pd.DateOffset(months=months)
    end_hist = hist[hist.index <= PRICE_END]
    start_hist = hist[hist.index <= target]
    if end_hist.empty or start_hist.empty:
        return {"return": np.nan, "start_date": "", "end_date": "", "start_gap_days": np.nan, "end_gap_days": np.nan, "status": "insufficient_history"}
    end_date = end_hist.index[-1]
    start_date = start_hist.index[-1]
    start_gap = int((target - start_date).days)
    end_gap = int((PRICE_END - end_date).days)
    if start_gap > 14 or end_gap > 14:
        return {"return": np.nan, "start_date": start_date.date().isoformat(), "end_date": end_date.date().isoformat(), "start_gap_days": start_gap, "end_gap_days": end_gap, "status": "stale_price"}
    ret = float(end_hist.iloc[-1]["adj_close"] / start_hist.iloc[-1]["adj_close"] - 1)
    return {"return": ret, "start_date": start_date.date().isoformat(), "end_date": end_date.date().isoformat(), "start_gap_days": start_gap, "end_gap_days": end_gap, "status": "ok"}


def build_price_table(index: pd.DataFrame, histories: dict[str, pd.DataFrame], failures: dict[str, str]) -> pd.DataFrame:
    rows = []
    for src in index.itertuples(index=False):
        row = {"ticker": src.ticker, "company": src.company, "category": src.category, "vendor_symbol": src.ticker}
        frame = histories.get(src.ticker)
        if frame is None:
            row.update({"ret_3m": np.nan, "ret_6m": np.nan, "price_status": failures.get(src.ticker, "missing")})
        else:
            r3 = trailing_return(frame, 3)
            r6 = trailing_return(frame, 6)
            row.update({
                "ret_3m": r3["return"], "ret_3m_start": r3["start_date"], "ret_3m_end": r3["end_date"], "ret_3m_status": r3["status"],
                "ret_6m": r6["return"], "ret_6m_start": r6["start_date"], "ret_6m_end": r6["end_date"], "ret_6m_status": r6["status"],
                "price_status": "ok" if r3["status"] == "ok" or r6["status"] == "ok" else f"3m={r3['status']};6m={r6['status']}",
                "end_adj_close": float(frame[frame.index <= PRICE_END].iloc[-1]["adj_close"]),
            })
        rows.append(row)
    result = pd.DataFrame(rows)
    for horizon in ["3m", "6m"]:
        result[f"ret_{horizon}_winsor"] = result[f"ret_{horizon}"].clip(result[f"ret_{horizon}"].quantile(0.05), result[f"ret_{horizon}"].quantile(0.95))
        result[f"actual_rank_{horizon}"] = result[f"ret_{horizon}"].rank(ascending=False, method="average")
        # These two fields separate company selection from the very large
        # category return differences in this universe.
        result[f"category_median_{horizon}"] = result.groupby("category")[f"ret_{horizon}"].transform("median")
        result[f"category_excess_{horizon}"] = result[f"ret_{horizon}"] - result[f"category_median_{horizon}"]
        result[f"category_percentile_{horizon}"] = result.groupby("category")[f"ret_{horizon}"].rank(pct=True)
    return result


def corr_spearman_desirability(rank: pd.Series, returns: pd.Series) -> float:
    frame = pd.concat([rank, returns], axis=1).dropna()
    if len(frame) < 3:
        return np.nan
    return float((-frame.iloc[:, 0]).rank().corr(frame.iloc[:, 1].rank()))


def metric_row(list_id: str, method_id: str, name: str, rank: pd.DataFrame, prices: pd.DataFrame, synthetic: bool = False) -> dict[str, object]:
    data = rank[["rank", "ticker"]].merge(prices, on="ticker", how="left")
    out: dict[str, object] = {"list_id": list_id, "method_id": method_id, "name": name, "synthetic": synthetic, "ranked_n": len(rank)}
    for horizon in ["3m", "6m"]:
        col = f"ret_{horizon}"
        wcol = f"ret_{horizon}_winsor"
        ecol = f"category_excess_{horizon}"
        pcol = f"category_percentile_{horizon}"
        valid = data.dropna(subset=[col])
        top10 = valid[valid["rank"] <= 10]
        top20 = valid[valid["rank"] <= 20]
        bottom20 = valid[valid["rank"] >= 173]
        q1 = valid[valid["rank"] <= 48]
        q4 = valid[valid["rank"] >= 145]
        universe_median = valid[col].median()
        actual_top20 = set(valid.nsmallest(20, f"actual_rank_{horizon}")["ticker"])
        out.update({
            f"valid_n_{horizon}": len(valid),
            f"universe_mean_{horizon}": valid[col].mean(),
            f"universe_median_{horizon}": universe_median,
            f"top10_mean_{horizon}": top10[col].mean(),
            f"top10_median_{horizon}": top10[col].median(),
            f"top20_mean_{horizon}": top20[col].mean(),
            f"top20_median_{horizon}": top20[col].median(),
            f"top20_winsor_mean_{horizon}": top20[wcol].mean(),
            f"bottom20_mean_{horizon}": bottom20[col].mean(),
            f"bottom20_median_{horizon}": bottom20[col].median(),
            f"top20_bottom20_spread_{horizon}": top20[col].mean() - bottom20[col].mean(),
            f"q1_q4_spread_{horizon}": q1[col].mean() - q4[col].mean(),
            f"rank_ic_{horizon}": corr_spearman_desirability(valid["rank"], valid[col]),
            f"category_neutral_rank_ic_{horizon}": corr_spearman_desirability(valid["rank"], valid[pcol]),
            f"top20_category_excess_mean_{horizon}": top20[ecol].mean(),
            f"top20_category_excess_median_{horizon}": top20[ecol].median(),
            f"top20_bottom20_category_excess_spread_{horizon}": top20[ecol].mean() - bottom20[ecol].mean(),
            f"top20_positive_rate_{horizon}": (top20[col] > 0).mean(),
            f"top20_above_universe_median_{horizon}": (top20[col] > universe_median).mean(),
            f"top20_actual_top20_overlap_{horizon}": len(set(top20["ticker"]) & actual_top20),
            f"top20_tickers_{horizon}": ",".join(top20.sort_values("rank")["ticker"]),
        })
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    index = read_index()
    index_tickers = set(index["ticker"])
    files = result_files()
    if len(files) != 26:
        raise RuntimeError(f"expected 26 standalone result files, got {len(files)}: {list(files)}")

    audits = []
    rankings: dict[str, pd.DataFrame] = {}
    method_names: dict[str, str] = {}
    member_rows = []
    for method_id, path in files.items():
        method_name = path.parents[2].name.split("_", 1)[1]
        method_names[method_id] = method_name
        if method_id == "06":
            for list_id, h2 in METHOD06_LISTS.items():
                rank, notes = parse_rank_rows(path, [(h2, None)])
                rankings[list_id] = rank
                audits.append(ranking_audit_row(method_id, list_id, method_name, path, rank, notes, index_tickers))
                for row in rank.itertuples(index=False):
                    member_rows.append({"method_id": method_id, "list_id": list_id, "rank": row.rank, "ticker": row.ticker, "score": row.score})
        else:
            rank, notes = parse_rank_rows(path, SELECTORS[method_id])
            rankings[method_id] = rank
            audits.append(ranking_audit_row(method_id, method_id, method_name, path, rank, notes, index_tickers))
            for row in rank.itertuples(index=False):
                member_rows.append({"method_id": method_id, "list_id": method_id, "rank": row.rank, "ticker": row.ticker, "score": row.score})

    audit = pd.DataFrame(audits)
    audit.to_csv(OUT / "01_28张完整榜结构审计.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(member_rows).to_csv(OUT / "02_28张榜全部名次.csv", index=False, encoding="utf-8-sig")
    if not audit["structurally_valid"].all():
        bad = audit.loc[~audit["structurally_valid"], ["list_id", "row_count", "missing_ranks", "missing_tickers", "unexpected_tickers", "parse_conflicts"]]
        raise RuntimeError("ranking structure audit failed:\n" + bad.to_string(index=False))

    symbols = sorted(index_tickers | set(BENCHMARKS))
    histories, failures = fetch_histories(symbols)
    prices = build_price_table(index, histories, failures)
    prices.to_csv(OUT / "03_192家公司独立复权价3月6月收益.csv", index=False, encoding="utf-8-sig")

    benchmark_rows = []
    for symbol in BENCHMARKS:
        frame = histories.get(symbol)
        if frame is None:
            benchmark_rows.append({"symbol": symbol, "ret_3m": np.nan, "ret_6m": np.nan, "status": failures.get(symbol, "missing")})
        else:
            r3 = trailing_return(frame, 3)
            r6 = trailing_return(frame, 6)
            benchmark_rows.append({"symbol": symbol, "ret_3m": r3["return"], "ret_6m": r6["return"], "start_3m": r3["start_date"], "start_6m": r6["start_date"], "end": r3["end_date"], "status": f"3m={r3['status']};6m={r6['status']}"})
    pd.DataFrame(benchmark_rows).to_csv(OUT / "04_基准3月6月收益.csv", index=False, encoding="utf-8-sig")

    # A method-level synthetic consensus for method 06 is used only to keep the
    # 26-plan comparison at 26 rows.  Its three actual lists remain separately
    # reported and are never counted as three independent votes.
    m06 = pd.concat([rankings[k][["ticker", "rank"]].rename(columns={"rank": k}) for k in METHOD06_LISTS], axis=0, ignore_index=True)
    m06 = m06.groupby("ticker", as_index=False).agg({k: "first" for k in METHOD06_LISTS})
    m06["mean_rank"] = m06[list(METHOD06_LISTS)].mean(axis=1)
    m06["rank"] = m06["mean_rank"].rank(method="first").astype(int)
    m06 = m06.sort_values("rank")[["rank", "ticker"]]
    rankings["06"] = m06

    list_metrics = []
    for list_id, rank in rankings.items():
        method_id = "06" if list_id in {"06", *METHOD06_LISTS.keys()} else list_id
        label = {
            "06F": "双源三视图-基本面性价比",
            "06G": "双源三视图-激进成长",
            "06E": "双源三视图-财报事件与右尾弹性",
            "06": "双源三视图-三榜等权综合（派生）",
        }.get(list_id, method_names[method_id])
        list_metrics.append(metric_row(list_id, method_id, label, rank, prices, synthetic=list_id == "06"))
    metrics = pd.DataFrame(list_metrics)
    metrics.to_csv(OUT / "05_28张实际榜及06派生综合_3月6月评估.csv", index=False, encoding="utf-8-sig")
    plan_metrics = metrics[(metrics["list_id"].isin(files.keys()))].copy()
    plan_metrics.to_csv(OUT / "06_26方案3月6月有限评估.csv", index=False, encoding="utf-8-sig")

    # Consensus views.  Exclude E-pairs from the independent-vote view because
    # they are input-expansion paired experiments, and exclude 10-17 from the
    # current-priority view because those methods are frozen or exited.
    plan_members = []
    for method_id in files:
        rank = rankings[method_id]
        for row in rank.itertuples(index=False):
            plan_members.append({"method_id": method_id, "ticker": row.ticker, "rank": int(row.rank), "percentile": 1 - (int(row.rank) - 1) / 191})
    pm = pd.DataFrame(plan_members)

    def consensus_for(method_set: set[str], prefix: str) -> pd.DataFrame:
        group = pm[pm["method_id"].isin(method_set)].groupby("ticker")
        result = group.agg(**{
            f"{prefix}_method_n": ("method_id", "nunique"),
            f"{prefix}_mean_rank": ("rank", "mean"),
            f"{prefix}_median_rank": ("rank", "median"),
            f"{prefix}_mean_percentile": ("percentile", "mean"),
            f"{prefix}_top10_count": ("rank", lambda s: int((s <= 10).sum())),
            f"{prefix}_top20_count": ("rank", lambda s: int((s <= 20).sum())),
            f"{prefix}_top48_count": ("rank", lambda s: int((s <= 48).sum())),
        }).reset_index()
        return result

    all_ids = set(files)
    independent_ids = all_ids - {"E01", "E02", "E03"}
    priority_ids = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "N01", "N02", "N03", "N04", "N05", "N06"}
    core_aux_ids = {"01", "02", "03", "04", "05", "06", "07", "08"}
    consensus = index.copy()
    for method_set, prefix in [(all_ids, "all26"), (independent_ids, "independent23"), (priority_ids, "priority15"), (core_aux_ids, "core_aux8")]:
        consensus = consensus.merge(consensus_for(method_set, prefix), on="ticker", how="left")
    consensus = consensus.merge(prices.drop(columns=["company", "category"]), on="ticker", how="left")
    consensus = consensus.sort_values(["priority15_mean_percentile", "core_aux8_mean_percentile"], ascending=False)
    consensus.to_csv(OUT / "07_公司跨方案共识.csv", index=False, encoding="utf-8-sig")

    # Pair diagnostics for the three expanded-input methods.
    pair_rows = []
    for base, ext in [("01", "E01"), ("02", "E02"), ("N06", "E03")]:
        merged = rankings[base][["ticker", "rank"]].merge(rankings[ext][["ticker", "rank"]], on="ticker", suffixes=("_base", "_extended"))
        pair_rows.append({
            "base": base, "extended": ext,
            # Both inputs are already complete ordinal ranks, so Pearson on
            # these columns is exactly their Spearman rank correlation.
            "spearman_rank_similarity": merged["rank_base"].corr(merged["rank_extended"]),
            "top10_overlap": len(set(merged.nsmallest(10, "rank_base")["ticker"]) & set(merged.nsmallest(10, "rank_extended")["ticker"])),
            "top20_overlap": len(set(merged.nsmallest(20, "rank_base")["ticker"]) & set(merged.nsmallest(20, "rank_extended")["ticker"])),
            "mean_abs_rank_change": (merged["rank_base"] - merged["rank_extended"]).abs().mean(),
        })
    pd.DataFrame(pair_rows).to_csv(OUT / "08_输入扩展配对排名变化.csv", index=False, encoding="utf-8-sig")

    metadata = {
        "created_at": pd.Timestamp.now(tz="America/Los_Angeles").isoformat(),
        "price_end": PRICE_END.date().isoformat(),
        "return_definition": "Yahoo Finance Adjusted Close total return; closest valid close on or before exact 3/6 calendar-month target, max 14-day staleness",
        "result_file_count": len(files),
        "actual_complete_list_count": len(audit),
        "structurally_valid_list_count": int(audit["structurally_valid"].sum()),
        "price_3m_valid_count": int(prices["ret_3m"].notna().sum()),
        "price_6m_valid_count": int(prices["ret_6m"].notna().sum()),
        "download_failures": failures,
    }
    (OUT / "09_运行元数据.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    print("\nTop plan metrics by 3m IC")
    print(plan_metrics.sort_values("rank_ic_3m", ascending=False)[["list_id", "name", "rank_ic_3m", "top20_bottom20_spread_3m", "top20_mean_3m", "top20_median_3m"]].head(12).to_string(index=False))
    print("\nTop plan metrics by 6m IC")
    print(plan_metrics.sort_values("rank_ic_6m", ascending=False)[["list_id", "name", "rank_ic_6m", "top20_bottom20_spread_6m", "top20_mean_6m", "top20_median_6m"]].head(12).to_string(index=False))
    print("\nConsensus top 30")
    print(consensus[["ticker", "company", "priority15_mean_rank", "priority15_top20_count", "core_aux8_mean_rank", "core_aux8_top20_count", "ret_3m", "ret_6m"]].head(30).to_string(index=False))


if __name__ == "__main__":
    main()
