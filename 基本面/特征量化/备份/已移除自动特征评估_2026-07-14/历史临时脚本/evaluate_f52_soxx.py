# -*- coding: utf-8 -*-
from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
F52_PATH = ROOT / "特征量化" / "量化评分" / "F52_监管地缘风险_量化评分_2026-06-04.md"
F51_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
RET_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md"
FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_PATH = ROOT / "特征量化" / "特征评估" / "F52_监管地缘风险_特征评估_三段SOXX下跌区间涨跌_2026-06-04.md"

SOXX_WINDOWS = {
    "w1": ("SOXX下跌1：2025-02-20至2025-04-08", -32.98),
    "w2": ("SOXX下跌2：2026-02-25至2026-03-30", -15.82),
    "w3": ("SOXX下跌3：2025-10-29至2025-11-20", -13.40),
}
SOXX_CUM = -62.20


def split_md_row(line: str) -> list[str] | None:
    if not line.lstrip().startswith("|"):
        return None
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: Iterable[str]) -> bool:
    cells = list(cells)
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in cells)


def parse_percent(text: str) -> float:
    if text is None:
        return math.nan
    if "N/A" in text:
        return math.nan
    match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%", text)
    if not match:
        return math.nan
    return float(match.group(1))


def parse_float(text: str) -> float:
    try:
        return float(str(text).replace(",", "").strip())
    except Exception:
        return math.nan


def parse_int(text: str) -> int:
    try:
        return int(str(text).strip())
    except Exception:
        return -1


def parse_score_file(path: Path, prefix: str) -> pd.DataFrame:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == "## 全公司排序表")
    header = None
    rows: list[dict[str, object]] = []
    in_table = False
    for line in lines[start + 1 :]:
        if in_table and line.startswith("## "):
            break
        cells = split_md_row(line)
        if cells is None:
            continue
        if is_separator(cells):
            continue
        if header is None:
            header = cells
            in_table = True
            continue
        if len(cells) < len(header):
            cells += [""] * (len(header) - len(cells))
        rec = dict(zip(header, cells))
        ticker = rec.get("股票代号", "").strip()
        if not ticker or ticker == "股票代号":
            continue
        rank = parse_int(rec.get("排名", ""))
        score = parse_float(rec.get("特征分", ""))
        if rank < 0 or math.isnan(score):
            continue
        rows.append(
            {
                "ticker": ticker,
                "name": rec.get("公司名称", "").strip(),
                "category": rec.get("分类目录", "").strip(),
                f"{prefix}_rank": rank,
                f"{prefix}_score": score,
                f"{prefix}_evidence": rec.get("证据等级", "").strip(),
                f"{prefix}_confidence": rec.get("置信度", "").strip(),
                f"{prefix}_evidence_text": rec.get("核心证据", "").strip(),
                f"{prefix}_discount": rec.get("缺失/降权", "").strip(),
            }
        )
    return pd.DataFrame(rows)


def parse_returns(path: Path) -> pd.DataFrame:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, object]] = []
    in_detail = False
    current_category = ""
    header = None
    w1_col = w2_col = w3_col = cum_col = None

    for line in lines:
        stripped = line.strip()
        if stripped == "## 全公司明细":
            in_detail = True
            continue
        if in_detail and stripped.startswith("## ") and stripped != "## 全公司明细":
            break
        if not in_detail:
            continue
        if stripped.startswith("### "):
            current_category = stripped.replace("### ", "", 1).strip()
            header = None
            continue
        cells = split_md_row(line)
        if cells is None:
            continue
        if is_separator(cells):
            continue
        if cells and cells[0] == "股票代号" and "三段累计涨跌幅" in cells:
            header = cells
            w1_col = next(h for h in header if h.startswith("SOXX下跌1"))
            w2_col = next(h for h in header if h.startswith("SOXX下跌2"))
            w3_col = next(h for h in header if h.startswith("SOXX下跌3"))
            cum_col = "三段累计涨跌幅"
            continue
        if header is None or len(cells) < len(header):
            continue
        rec = dict(zip(header, cells))
        ticker = rec.get("股票代号", "").strip()
        if not ticker or ticker == "股票代号":
            continue
        rows.append(
            {
                "ticker": ticker,
                "ret_name": rec.get("公司名称", "").strip(),
                "ret_category": current_category,
                "w1": parse_percent(rec.get(w1_col, "")),
                "w2": parse_percent(rec.get(w2_col, "")),
                "w3": parse_percent(rec.get(w3_col, "")),
                "cum_ret": parse_percent(rec.get(cum_col, "")),
                "ret_note": rec.get("备注", "").strip(),
            }
        )
    return pd.DataFrame(rows).drop_duplicates("ticker", keep="first")


def parse_financial(path: Path) -> pd.DataFrame:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, object]] = []
    in_detail = False
    current_category = ""
    header = None
    for line in lines:
        stripped = line.strip()
        if stripped == "## 按项目分类分组的公司明细表":
            in_detail = True
            continue
        if not in_detail:
            continue
        if stripped.startswith("### "):
            current_category = stripped.replace("### ", "", 1).strip()
            header = None
            continue
        cells = split_md_row(line)
        if cells is None:
            continue
        if is_separator(cells):
            continue
        if cells and cells[0] == "股票代号" and "Call IV" in cells and "listing_type" in cells:
            header = cells
            continue
        if header is None or len(cells) < len(header):
            continue
        rec = dict(zip(header, cells))
        ticker = rec.get("股票代号", "").strip()
        if not ticker or ticker == "股票代号":
            continue
        call_iv = parse_percent(rec.get("Call IV", ""))
        put_iv = parse_percent(rec.get("Put IV", ""))
        vals = [v for v in [call_iv, put_iv] if not math.isnan(v)]
        rows.append(
            {
                "ticker": ticker,
                "fin_category": current_category,
                "call_iv": call_iv,
                "put_iv": put_iv,
                "iv_avg": float(np.mean(vals)) if vals else math.nan,
                "currency": rec.get("currency", "").strip(),
                "financial_currency": rec.get("financial_currency", "").strip(),
                "listing_type": rec.get("listing_type", "").strip(),
                "adr_ratio": rec.get("adr_ratio", "").strip(),
                "valuation_check": rec.get("估值校验", "").strip(),
                "fin_note": rec.get("备注", "").strip(),
            }
        )
    return pd.DataFrame(rows).drop_duplicates("ticker", keep="first")


def pearson_corr(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) < 2:
        return math.nan
    if np.nanstd(x) == 0 or np.nanstd(y) == 0:
        return math.nan
    return float(np.corrcoef(x, y)[0, 1])


def kendall_tau_b(x: np.ndarray, y: np.ndarray) -> float:
    n = len(x)
    if n < 2:
        return math.nan
    concordant = discordant = tie_x = tie_y = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            dx = 0 if x[i] == x[j] else (1 if x[i] > x[j] else -1)
            dy = 0 if y[i] == y[j] else (1 if y[i] > y[j] else -1)
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                tie_x += 1
            elif dy == 0:
                tie_y += 1
            elif dx == dy:
                concordant += 1
            else:
                discordant += 1
    denom = math.sqrt((concordant + discordant + tie_x) * (concordant + discordant + tie_y))
    if denom == 0:
        return math.nan
    return (concordant - discordant) / denom


def corr_stats(df: pd.DataFrame, score_col: str, ret_col: str) -> dict[str, float | int]:
    sub = df[[score_col, ret_col]].dropna()
    x = sub[score_col].astype(float).to_numpy()
    y = sub[ret_col].astype(float).to_numpy()
    if len(sub) < 2:
        return {"n": len(sub), "pearson": math.nan, "spearman": math.nan, "kendall": math.nan}
    rx = pd.Series(x).rank(method="average").to_numpy()
    ry = pd.Series(y).rank(method="average").to_numpy()
    return {
        "n": len(sub),
        "pearson": pearson_corr(x, y),
        "spearman": pearson_corr(rx, ry),
        "kendall": kendall_tau_b(x, y),
    }


def sort_by_score(df: pd.DataFrame, score_col: str = "f52_score", high: bool = True) -> pd.DataFrame:
    if high:
        return df.sort_values([score_col, "f52_rank", "ticker"], ascending=[False, True, True], kind="mergesort")
    return df.sort_values([score_col, "f52_rank", "ticker"], ascending=[True, False, True], kind="mergesort")


def top_bottom_stats(df: pd.DataFrame, n: int, score_col: str = "f52_score") -> dict[str, float | int]:
    top = sort_by_score(df, score_col=score_col, high=True).head(n)
    bottom = sort_by_score(df, score_col=score_col, high=False).head(n)
    return {
        "n": n,
        "top_mean": top["cum_ret"].mean(),
        "top_median": top["cum_ret"].median(),
        "top_hit": (top["cum_ret"] > SOXX_CUM).mean(),
        "top_positive": (top["cum_ret"] > 0).mean(),
        "bottom_mean": bottom["cum_ret"].mean(),
        "bottom_median": bottom["cum_ret"].median(),
        "bottom_hit": (bottom["cum_ret"] > SOXX_CUM).mean(),
        "bottom_positive": (bottom["cum_ret"] > 0).mean(),
        "diff": top["cum_ret"].mean() - bottom["cum_ret"].mean(),
        "hit_diff": (top["cum_ret"] > SOXX_CUM).mean() - (bottom["cum_ret"] > SOXX_CUM).mean(),
    }


def group_risk_stats(df: pd.DataFrame, label: str) -> dict[str, float | int | str]:
    windows = ["w1", "w2", "w3"]
    window_values = df[windows].to_numpy(dtype=float)
    flat = window_values[~np.isnan(window_values)]
    soxx_values = np.array([SOXX_WINDOWS["w1"][1], SOXX_WINDOWS["w2"][1], SOXX_WINDOWS["w3"][1]], dtype=float)
    valid_matrix = ~np.isnan(window_values)
    beat_matrix = (window_values > soxx_values) & valid_matrix
    company_worst = np.nanmin(window_values, axis=1)
    company_std = np.nanstd(window_values, axis=1)
    return {
        "label": label,
        "n": len(df),
        "obs": int(valid_matrix.sum()),
        "w1_mean": df["w1"].mean(),
        "w2_mean": df["w2"].mean(),
        "w3_mean": df["w3"].mean(),
        "cum_mean": df["cum_ret"].mean(),
        "pressure_mean": float(np.nanmean(flat)) if len(flat) else math.nan,
        "avg_worst": float(np.nanmean(company_worst)) if len(company_worst) else math.nan,
        "window_dispersion": float(np.nanmean(company_std)) if len(company_std) else math.nan,
        "beat_window": float(beat_matrix.sum() / valid_matrix.sum()) if valid_matrix.sum() else math.nan,
        "beat_cum": (df["cum_ret"] > SOXX_CUM).mean(),
        "neg_window": float(((window_values < 0) & valid_matrix).sum() / valid_matrix.sum()) if valid_matrix.sum() else math.nan,
        "call_iv_mean": df["call_iv"].mean(),
        "put_iv_mean": df["put_iv"].mean(),
        "iv_mean": df["iv_avg"].mean(),
        "iv_median": df["iv_avg"].median(),
        "iv_n": int(df["iv_avg"].notna().sum()),
    }


def risk_groups(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    sorted_high = sort_by_score(df, high=True)
    top = sorted_high.head(30)
    bottom = sort_by_score(df, high=False).head(30)
    start = max((len(sorted_high) - 30) // 2, 0)
    mid = sorted_high.iloc[start : start + 30]
    stats = [
        group_risk_stats(top, "F52 Top30"),
        group_risk_stats(mid, "F52 Mid30"),
        group_risk_stats(bottom, "F52 Bottom30"),
    ]
    return top, mid, bottom, stats


def fmt_corr(value: float) -> str:
    if value is None or math.isnan(float(value)):
        return "N/A"
    return f"{float(value):.3f}"


def fmt_pct(value: float, digits: int = 2) -> str:
    if value is None or math.isnan(float(value)):
        return "N/A"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{digits}f}%"


def fmt_rate(value: float, digits: int = 1) -> str:
    if value is None or math.isnan(float(value)):
        return "N/A"
    return f"{value * 100:.{digits}f}%"


def fmt_score(value: float) -> str:
    if value is None or math.isnan(float(value)):
        return "N/A"
    return f"{value:.1f}"


def tickers_text(tickers: Iterable[str]) -> str:
    values = sorted(str(t) for t in tickers if str(t))
    return ", ".join(values) if values else "无"


def md_table(headers: list[str], rows: list[list[object]], aligns: list[str] | None = None) -> list[str]:
    if aligns is None:
        aligns = ["---"] * len(headers)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(aligns) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return out


def best_label(row: pd.Series) -> str:
    return f"{row['ticker']} {fmt_pct(row['cum_ret'])}"


def high_score_label(row: pd.Series) -> str:
    return f"{row['ticker']} {fmt_score(row['f52_score'])} / {fmt_pct(row['cum_ret'])}"


def current_iv(row: pd.Series) -> str:
    return fmt_pct(row["iv_avg"]) if not pd.isna(row["iv_avg"]) else "N/A"


def main() -> None:
    target_existed_before = OUT_PATH.exists()

    f52 = parse_score_file(F52_PATH, "f52")
    f51 = parse_score_file(F51_PATH, "f51")[["ticker", "f51_score", "f51_rank", "f51_confidence"]]
    returns = parse_returns(RET_PATH)
    finance = parse_financial(FIN_PATH)

    df = (
        f52.merge(returns, on="ticker", how="left")
        .merge(f51, on="ticker", how="left")
        .merge(finance, on="ticker", how="left")
    )
    df["category_mismatch"] = df["ret_category"].notna() & (df["ret_category"] != "") & (df["category"] != df["ret_category"])
    df["low_liquidity"] = df["f51_score"].isna() | (df["f51_score"] <= 5.0)
    df["adr_currency_abnormal"] = (
        df["listing_type"].isna()
        | (df["listing_type"] != "common/equity")
        | (df["adr_ratio"] != "不适用")
        | (df["currency"] != df["financial_currency"])
        | df["valuation_check"].fillna("").str.contains("currency_mismatch", regex=False)
    )

    main_df = df[df["cum_ret"].notna()].copy()
    q_low = float(main_df["cum_ret"].quantile(0.05, interpolation="linear"))
    q_high = float(main_df["cum_ret"].quantile(0.95, interpolation="linear"))
    main_df["extreme_return"] = (main_df["cum_ret"] <= q_low) | (main_df["cum_ret"] >= q_high)

    main_df["category_pct"] = main_df.groupby("category")["f52_score"].rank(method="average", pct=True)
    main_df["score_resid"] = main_df["f52_score"] - main_df.groupby("category")["f52_score"].transform("mean")
    main_df["ret_resid"] = main_df["cum_ret"] - main_df.groupby("category")["cum_ret"].transform("mean")

    missing_return = df[df["cum_ret"].isna()]["ticker"].tolist()
    returns_no_score = sorted(set(returns[returns["cum_ret"].notna()]["ticker"]) - set(f52["ticker"]))

    main_corr = corr_stats(main_df, "f52_score", "cum_ret")
    window_corrs = {
        "cum_ret": main_corr,
        "w1": corr_stats(main_df, "f52_score", "w1"),
        "w2": corr_stats(main_df, "f52_score", "w2"),
        "w3": corr_stats(main_df, "f52_score", "w3"),
    }

    sorted_high = sort_by_score(main_df, high=True)
    positions = pd.Series(np.arange(len(sorted_high)), index=sorted_high.index)
    sorted_high = sorted_high.assign(quintile=pd.qcut(positions, 5, labels=False, duplicates="drop").astype(int))
    quintile_rows = []
    quintile_names = {
        0: "Q1最高分",
        1: "Q2",
        2: "Q3",
        3: "Q4",
        4: "Q5最低分",
    }
    for q in sorted(sorted_high["quintile"].unique()):
        part = sorted_high[sorted_high["quintile"] == q]
        quintile_rows.append(
            [
                quintile_names.get(int(q), f"Q{int(q) + 1}"),
                len(part),
                fmt_score(part["f52_score"].mean()),
                fmt_pct(part["cum_ret"].mean()),
                fmt_pct(part["cum_ret"].median()),
                fmt_rate((part["cum_ret"] > SOXX_CUM).mean()),
                fmt_pct(np.nanmean(np.nanmin(part[["w1", "w2", "w3"]].to_numpy(dtype=float), axis=1))),
                fmt_pct(part["iv_avg"].mean()),
                int(part["iv_avg"].notna().sum()),
            ]
        )

    combo_stats = [top_bottom_stats(main_df, n) for n in [10, 20, 30]]
    top30, mid30, bottom30, risk_stats = risk_groups(main_df)

    neutral_corr_pct = corr_stats(main_df, "category_pct", "cum_ret")
    neutral_corr_resid = corr_stats(main_df, "score_resid", "ret_resid")
    neutral_combo = [top_bottom_stats(main_df, n, score_col="category_pct") for n in [10, 20, 30]]

    category_rows = []
    for category, part in main_df.groupby("category", sort=True):
        stats = corr_stats(part, "f52_score", "cum_ret")
        best = part.sort_values("cum_ret", ascending=False).iloc[0]
        worst = part.sort_values("cum_ret", ascending=True).iloc[0]
        high = sort_by_score(part, high=True).iloc[0]
        category_rows.append(
            [
                category,
                len(part),
                fmt_corr(stats["pearson"]),
                fmt_corr(stats["spearman"]),
                fmt_corr(stats["kendall"]),
                fmt_pct(part["cum_ret"].mean()),
                fmt_rate((part["cum_ret"] > SOXX_CUM).mean()),
                best_label(best),
                best_label(worst),
                high_score_label(high),
            ]
        )

    category_dist_rows = []
    for category, part in main_df.groupby("category", sort=True):
        category_dist_rows.append(
            [
                category,
                len(part),
                fmt_score(part["f52_score"].mean()),
                fmt_pct(part["cum_ret"].mean()),
                fmt_pct(part["cum_ret"].median()),
                fmt_rate((part["cum_ret"] > SOXX_CUM).mean()),
            ]
        )

    masks = {
        "全样本基准": pd.Series(True, index=main_df.index),
        "剔除低流动性": ~main_df["low_liquidity"],
        "剔除ADR/币种异常": ~main_df["adr_currency_abnormal"],
        "剔除极端涨跌": ~main_df["extreme_return"],
        "三项合并剔除": ~(main_df["low_liquidity"] | main_df["adr_currency_abnormal"] | main_df["extreme_return"]),
    }
    rules = {
        "全样本基准": "无剔除",
        "剔除低流动性": "F51交易流动性分 > 5.0",
        "剔除ADR/币种异常": "listing_type=common/equity、adr_ratio=不适用、交易/财报货币一致、估值校验无currency_mismatch",
        "剔除极端涨跌": f"剔除三段累计涨跌双尾5%；阈值 {fmt_pct(q_low)} / {fmt_pct(q_high)}",
        "三项合并剔除": "同时满足上述三项",
    }
    robust_rows = []
    robust_values: dict[str, dict[str, object]] = {}
    for name, mask in masks.items():
        part = main_df[mask].copy()
        stats = corr_stats(part, "f52_score", "cum_ret")
        combo = top_bottom_stats(part, 30)
        robust_values[name] = {"part": part, "stats": stats, "combo": combo}
        robust_rows.append(
            [
                name,
                rules[name],
                len(part),
                len(main_df) - len(part),
                fmt_corr(stats["pearson"]),
                fmt_corr(stats["spearman"]),
                fmt_corr(stats["kendall"]),
                fmt_pct(combo["top_mean"]),
                fmt_pct(combo["bottom_mean"]),
                fmt_pct(combo["diff"]),
                fmt_rate(combo["hit_diff"]),
            ]
        )

    def constituent_rows() -> list[list[object]]:
        rows: list[list[object]] = []
        top10 = sort_by_score(main_df, high=True).head(10)
        bottom10 = sort_by_score(main_df, high=False).head(10)
        for label, part in [("Top10", top10), ("Bottom10", bottom10)]:
            for _, row in part.iterrows():
                rows.append(
                    [
                        label,
                        row["ticker"],
                        row["name"],
                        row["category"],
                        fmt_pct(row["cum_ret"]),
                        fmt_pct(row["w1"]),
                        fmt_pct(row["w2"]),
                        fmt_pct(row["w3"]),
                        fmt_score(row["f52_score"]),
                        int(row["f52_rank"]),
                        row["f52_confidence"],
                    ]
                )
        return rows

    def stock_table(part: pd.DataFrame, include_rank_label: str = "F52排名") -> list[list[object]]:
        rows = []
        for _, row in part.iterrows():
            rows.append(
                [
                    row["ticker"],
                    row["name"],
                    row["category"],
                    fmt_pct(row["cum_ret"]),
                    fmt_pct(row["w1"]),
                    fmt_pct(row["w2"]),
                    fmt_pct(row["w3"]),
                    fmt_score(row["f52_score"]),
                    int(row["f52_rank"]),
                    row["f52_confidence"],
                ]
            )
        return rows

    def score_extreme_table(part: pd.DataFrame) -> list[list[object]]:
        rows = []
        for _, row in part.iterrows():
            rows.append(
                [
                    int(row["f52_rank"]),
                    row["ticker"],
                    row["name"],
                    row["category"],
                    fmt_score(row["f52_score"]),
                    fmt_pct(row["cum_ret"]),
                    fmt_pct(np.nanmean([row["w1"], row["w2"], row["w3"]])),
                    current_iv(row),
                    row["f52_confidence"],
                ]
            )
        return rows

    risk_rows = []
    for stat in risk_stats:
        risk_rows.append(
            [
                stat["label"],
                stat["n"],
                stat["obs"],
                fmt_pct(stat["w1_mean"]),
                fmt_pct(stat["w2_mean"]),
                fmt_pct(stat["w3_mean"]),
                fmt_pct(stat["cum_mean"]),
                fmt_pct(stat["pressure_mean"]),
                fmt_pct(stat["avg_worst"]),
                fmt_pct(stat["window_dispersion"]),
                fmt_rate(stat["beat_window"]),
                fmt_rate(stat["beat_cum"]),
                fmt_rate(stat["neg_window"]),
                fmt_pct(stat["call_iv_mean"]),
                fmt_pct(stat["put_iv_mean"]),
                fmt_pct(stat["iv_mean"]),
                fmt_pct(stat["iv_median"]),
                stat["iv_n"],
            ]
        )

    corr_summary_rows = [
        [
            "三段累计涨跌幅",
            window_corrs["cum_ret"]["n"],
            fmt_corr(window_corrs["cum_ret"]["pearson"]),
            fmt_corr(window_corrs["cum_ret"]["spearman"]),
            fmt_corr(window_corrs["cum_ret"]["kendall"]),
            "核心目标；三个SOXX下跌区间百分比简单相加，越高越好",
        ],
        [
            "SOXX下跌1：2025-02-20至2025-04-08",
            window_corrs["w1"]["n"],
            fmt_corr(window_corrs["w1"]["pearson"]),
            fmt_corr(window_corrs["w1"]["spearman"]),
            fmt_corr(window_corrs["w1"]["kendall"]),
            "SOXX -32.98%",
        ],
        [
            "SOXX下跌2：2026-02-25至2026-03-30",
            window_corrs["w2"]["n"],
            fmt_corr(window_corrs["w2"]["pearson"]),
            fmt_corr(window_corrs["w2"]["spearman"]),
            fmt_corr(window_corrs["w2"]["kendall"]),
            "SOXX -15.82%",
        ],
        [
            "SOXX下跌3：2025-10-29至2025-11-20",
            window_corrs["w3"]["n"],
            fmt_corr(window_corrs["w3"]["pearson"]),
            fmt_corr(window_corrs["w3"]["spearman"]),
            fmt_corr(window_corrs["w3"]["kendall"]),
            "SOXX -13.40%",
        ],
    ]

    top30_stats = next(s for s in risk_stats if s["label"] == "F52 Top30")
    bottom30_stats = next(s for s in risk_stats if s["label"] == "F52 Bottom30")
    top_bottom_30 = combo_stats[-1]
    combined = robust_values["三项合并剔除"]

    spearman = float(main_corr["spearman"])
    if spearman >= 0.30:
        direction_text = "中等正向成立"
    elif spearman >= 0.10:
        direction_text = "弱到中等正向成立"
    elif spearman > -0.10:
        direction_text = "接近无效"
    else:
        direction_text = "负向或失效"

    neutral_s = float(neutral_corr_pct["spearman"])
    neutral_direction = "仍为正向" if neutral_s > 0 else "转为负向"
    robust_s = float(combined["stats"]["spearman"])
    robust_direction = "仍成立" if robust_s > 0.1 else ("边际有效" if robust_s > 0 else "不成立")

    report: list[str] = []
    report.append("# F52 监管地缘风险 特征评估 三段SOXX下跌区间涨跌 2026-06-04")
    report.append("")
    report.append("## 运行元信息")
    report.append("- 评估对象：`F52_监管地缘风险`。")
    report.append(f"- 评分输入：`特征量化/量化评分/{F52_PATH.name}`，评分日期 2026-06-04，覆盖 {len(f52)} 家。")
    report.append(f"- 收益输入：`日度资料/区间涨跌/{RET_PATH.name}`，生成时间 2026-06-04 10:57:48 -0700（America/Los_Angeles，本机时区）；价格口径为 Yahoo Finance `Close`，`auto_adjust=False`，不含股息再投资。")
    report.append("- SOXX压力窗口：2025-02-20至2025-04-08 下跌 -32.98%；2026-02-25至2026-03-30 下跌 -15.82%；2025-10-29至2025-11-20 下跌 -13.40%。SOXX三段累计涨跌幅为 -62.20%。")
    report.append(f"- 稳健性辅助输入：`特征量化/量化评分/{F51_PATH.name}`；`日度资料/每日金融数据/{FIN_PATH.name}`，金融数据生成时间 2026-06-03 13:41:46 PDT-0700。")
    report.append(f"- 有效评估样本：评分与三段累计涨跌幅交集 {len(main_df)} 家；F52评分有但累计涨跌缺失 {len(missing_return)} 家：{tickers_text(missing_return)}。")
    report.append("- 收益方向口径：三段累计涨跌幅越高越好；在压力窗口中，跌幅更小、或上涨，均视为更优表现。")
    report.append(f"- 命中率口径：三段累计涨跌幅大于 SOXX 三段累计涨跌幅 `{fmt_pct(SOXX_CUM)}` 记为压力命中；Top-Bottom收益差=高分组合平均三段累计收益 - 低分组合平均三段累计收益。")
    report.append("- 风险口径限制：本次输入是三个固定压力区间收益，不是逐日收益序列；因此本报告不写成严格日度波动率、完整最大回撤或真实下跌日表现结论，而使用三个SOXX下跌窗口均值、平均最差窗口、窗口离散度、跑赢SOXX窗口比例、负收益窗口占比，并用 2026-06-03 近ATM Call/Put IV均值补充当前波动代理。")
    report.append("- 稳健性口径：低流动性使用 `F51<=5.0` 或F51缺失作为剔除代理；ADR/币种异常使用每日金融数据中的 `listing_type`、ADR比例、交易/财报货币和 `currency_mismatch` 标记；极端涨跌按本次三段累计收益双尾5%剔除。")
    report.append(f"- 旧版处理：目标正式输出文件写入前{'已存在，本次按用户指定正式文件名覆盖重算结果' if target_existed_before else '不存在，无需备份'}；本次查看同目录既有评估报告仅作为格式与口径参照，三段SOXX指标均重新计算，不继承6个月评估结论。")
    report.append("- 时间限制：F52评分日期为2026-06-04，三个收益窗口发生在2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20；本报告是当前评分对既有压力窗口表现的解释性评估，不是严格前瞻回测。")
    report.append("- 本报告是下游特征评估，只读取 `特征量化/量化评分/`、`特征量化/特征评估/`、`日度资料/区间涨跌/` 和必要日度金融字段，不把结论反向写入上游资料。")
    report.append("")
    report.append("## 结论摘要")
    report.append(f"- 排序有效性：{direction_text}。全样本 Pearson {fmt_corr(main_corr['pearson'])}，Spearman {fmt_corr(main_corr['spearman'])}，Kendall {fmt_corr(main_corr['kendall'])}；重点指标 Spearman 为 {fmt_corr(main_corr['spearman'])}。")
    report.append(f"- 分窗口观察：SOXX下跌1/2/3 的 Spearman 分别为 {fmt_corr(window_corrs['w1']['spearman'])}、{fmt_corr(window_corrs['w2']['spearman'])}、{fmt_corr(window_corrs['w3']['spearman'])}。")
    report.append(f"- Top/Bottom能力：Top10/Top20/Top30 平均累计收益分别为 {fmt_pct(combo_stats[0]['top_mean'])}、{fmt_pct(combo_stats[1]['top_mean'])}、{fmt_pct(combo_stats[2]['top_mean'])}；对应Top-Bottom收益差为 {fmt_pct(combo_stats[0]['diff'])}、{fmt_pct(combo_stats[1]['diff'])}、{fmt_pct(combo_stats[2]['diff'])}。")
    report.append(f"- 风险解释力：F52 Top30 三段累计均值 {fmt_pct(top30_stats['cum_mean'])}，平均最差窗口 {fmt_pct(top30_stats['avg_worst'])}，跑赢SOXX窗口比例 {fmt_rate(top30_stats['beat_window'])}，当前IV均值 {fmt_pct(top30_stats['iv_mean'])}；Bottom30 对应为 {fmt_pct(bottom30_stats['cum_mean'])}、{fmt_pct(bottom30_stats['avg_worst'])}、{fmt_rate(bottom30_stats['beat_window'])}、{fmt_pct(bottom30_stats['iv_mean'])}。")
    report.append(f"- 分类中性：{neutral_direction}。分类内百分位合并 Spearman {fmt_corr(neutral_corr_pct['spearman'])}，分类去均值残差 Spearman {fmt_corr(neutral_corr_resid['spearman'])}；中性Top30-Bottom30收益差 {fmt_pct(neutral_combo[2]['diff'])}。")
    report.append(f"- 稳健性：{robust_direction}。剔除低流动性后 Spearman {fmt_corr(robust_values['剔除低流动性']['stats']['spearman'])}，剔除ADR/币种异常后 {fmt_corr(robust_values['剔除ADR/币种异常']['stats']['spearman'])}，剔除极端涨跌后 {fmt_corr(robust_values['剔除极端涨跌']['stats']['spearman'])}，三项合并后 {fmt_corr(combined['stats']['spearman'])}；三项合并后 Top30-Bottom30 为 {fmt_pct(combined['combo']['diff'])}。")
    report.append("-.解释：F52 衡量的是“监管、地缘、出口许可、关税、并网/环保、数据安全、反垄断、制裁或区域政策冲击是否可控”。三段SOXX压力窗口里，高F52公司更集中在电力配电、机电施工、公用事业、工业气体和分散型设施链，通常有受监管回收、长期合同、多区域供给或本土化交付支撑；低F52公司更多暴露在先进半导体出口管制、台湾/中国地缘、核许可、GPU/电力融资和小盘政策敏感资产中。因此F52在本次压力窗口更像防守质量和尾部风险约束因子，而不是单独的进攻型收益因子。")
    report[-1] = report[-1].replace("-.解释", "- 解释")
    report.append("")
    report.append("## 覆盖检查")
    report.extend(
        md_table(
            ["项目", "数量", "说明"],
            [
                ["F52评分覆盖", len(f52), "来自2026-06-04评分文件"],
                ["三段累计涨跌覆盖", int(returns["cum_ret"].notna().sum()), "来自2026-06-04三段SOXX下跌区间涨跌文件"],
                ["交集有效样本", len(main_df), "用于本报告主指标"],
                ["评分有但累计涨跌缺失", len(missing_return), tickers_text(missing_return)],
                ["涨跌有但评分缺失", len(returns_no_score), tickers_text(returns_no_score)],
                ["分类目录不一致", int(df["category_mismatch"].sum()), tickers_text(df.loc[df["category_mismatch"], "ticker"])],
            ],
        )
    )
    report.append("")
    report.append("### 交集样本分类分布")
    report.extend(
        md_table(
            ["分类目录", "样本数", "F52均分", "三段累计平均", "三段累计中位数", "跑赢SOXX累计率"],
            category_dist_rows,
        )
    )
    report.append("")
    report.append("## 排序有效性")
    report.extend(
        md_table(
            ["目标收益", "样本数", "Pearson", "Spearman", "Kendall tau-b", "解释"],
            corr_summary_rows,
        )
    )
    report.append("")
    report.append("### F52分数分组收益")
    report.extend(
        md_table(
            ["分组", "公司数", "F52均分", "三段累计平均", "三段累计中位数", "跑赢SOXX累计率", "平均最差窗口", "当前IV均值", "IV样本"],
            quintile_rows,
        )
    )
    report.append("")
    report.append("分组读数用于观察单调性。若F52是有效压力期防守分，最高分五分位应比最低分五分位累计跌幅更浅、跑赢SOXX比例更高、最差窗口更小；若只有Top端有效而中间不单调，则应把F52当作尾部过滤器而非线性alpha。")
    report.append("")
    report.append("## Top/Bottom能力")
    report.extend(
        md_table(
            ["组合", "Top平均累计", "Top中位累计", "Top压力命中率", "Top正收益率", "Bottom平均累计", "Bottom中位累计", "Bottom压力命中率", "Bottom正收益率", "Top-Bottom收益差"],
            [
                [
                    f"Top{s['n']}/Bottom{s['n']}",
                    fmt_pct(s["top_mean"]),
                    fmt_pct(s["top_median"]),
                    fmt_rate(s["top_hit"]),
                    fmt_rate(s["top_positive"]),
                    fmt_pct(s["bottom_mean"]),
                    fmt_pct(s["bottom_median"]),
                    fmt_rate(s["bottom_hit"]),
                    fmt_rate(s["bottom_positive"]),
                    fmt_pct(s["diff"]),
                ]
                for s in combo_stats
            ],
        )
    )
    report.append("")
    report.append("### Top10与Bottom10构成")
    report.extend(
        md_table(
            ["组别", "股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F52分", "F52排名", "置信度"],
            constituent_rows(),
        )
    )
    report.append("")
    report.append("Top端不是无风险资产：配电、工程、公用事业和成熟工业公司仍会承受估值和项目周期压力；Bottom端也会出现单段反弹或事件驱动少跌的个例。因此更应看Top30/Bottom30均值、命中率和最差窗口，而不是只看单一股票。")
    report.append("")
    report.append("## 风险解释力")
    report.append("本节只使用三个固定SOXX下跌区间作为压力测试代理。严格日度波动率、完整最大回撤、真实下跌日收益稳定性需要逐日价格序列；当前IV均值仅是 2026-06-03 近ATM期权波动代理，不等同于历史实际波动率。")
    report.append("")
    report.extend(
        md_table(
            [
                "分组",
                "公司数",
                "窗口观测",
                "SOXX跌1均值",
                "SOXX跌2均值",
                "SOXX跌3均值",
                "三段累计均值",
                "压力窗口均值",
                "平均最差窗口",
                "窗口离散度",
                "跑赢SOXX窗口比例",
                "跑赢SOXX累计率",
                "负收益窗口占比",
                "平均Call IV",
                "平均Put IV",
                "当前IV均值",
                "IV中位数",
                "IV样本",
            ],
            risk_rows,
        )
    )
    report.append("")
    report.append(
        f"结论：F52 Top30 相比 Bottom30，三段累计均值差值为 {fmt_pct(top30_stats['cum_mean'] - bottom30_stats['cum_mean'])}，平均最差窗口差值为 {fmt_pct(top30_stats['avg_worst'] - bottom30_stats['avg_worst'])}，当前近ATM IV均值差值为 {fmt_pct(top30_stats['iv_mean'] - bottom30_stats['iv_mean'])}。若差值分别表现为累计更高、最差窗口更浅、IV更低，则说明F52能解释压力期回撤与波动质量。"
    )
    report.append("")
    report.append("## 分类中性结果")
    report.extend(
        md_table(
            ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
            [
                [
                    "原始全样本",
                    main_corr["n"],
                    fmt_corr(main_corr["pearson"]),
                    fmt_corr(main_corr["spearman"]),
                    fmt_corr(main_corr["kendall"]),
                    "直接用F52原始分数排序",
                ],
                [
                    "分类内百分位合并",
                    neutral_corr_pct["n"],
                    fmt_corr(neutral_corr_pct["pearson"]),
                    fmt_corr(neutral_corr_pct["spearman"]),
                    fmt_corr(neutral_corr_pct["kendall"]),
                    "每个分类内先按F52排序，再转为0-1百分位后合并",
                ],
                [
                    "分类去均值残差",
                    neutral_corr_resid["n"],
                    fmt_corr(neutral_corr_resid["pearson"]),
                    fmt_corr(neutral_corr_resid["spearman"]),
                    fmt_corr(neutral_corr_resid["kendall"]),
                    "F52和累计收益分别减去分类均值后相关",
                ],
            ],
        )
    )
    report.append("")
    report.append("### 分类中性Top/Bottom")
    report.extend(
        md_table(
            ["组合", "Top平均累计", "Top压力命中率", "Bottom平均累计", "Bottom压力命中率", "Top-Bottom收益差"],
            [
                [
                    f"中性Top{s['n']}/Bottom{s['n']}",
                    fmt_pct(s["top_mean"]),
                    fmt_rate(s["top_hit"]),
                    fmt_pct(s["bottom_mean"]),
                    fmt_rate(s["bottom_hit"]),
                    fmt_pct(s["diff"]),
                ]
                for s in neutral_combo
            ],
        )
    )
    report.append("")
    report.append("### 10个分类目录内相关性")
    report.extend(
        md_table(
            ["分类目录", "样本数", "Pearson", "Spearman", "Kendall", "类内累计均值", "类内命中率", "类内最好", "类内最差", "类内最高F52公司"],
            category_rows,
        )
    )
    report.append("")
    report.append("分类内结果用于检验F52是否只是押中了某些防御目录。若分类内百分位和残差相关仍为正，说明同目录内“监管地缘风险可控性”排序也有额外压力期信息；若部分目录为负，则这些目录需要与价格强度、估值和流动性因子联用。")
    report.append("")
    report.append("## 稳健性检验")
    report.extend(
        md_table(
            ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30", "Top-Bottom命中率差"],
            robust_rows,
        )
    )
    report.append("")
    report.append(
        f"稳健性结论：剔除低流动性、ADR/币种异常和极端涨跌公司后，重点看 Spearman 与 Top30-Bottom30 是否同向保持。三项合并剔除后样本 {len(combined['part'])} 家，Spearman {fmt_corr(combined['stats']['spearman'])}，Top30-Bottom30 {fmt_pct(combined['combo']['diff'])}；这说明F52的压力期有效性{'不是完全由异常样本机械驱动' if robust_s > 0 else '在严格样本中不足，需要谨慎使用'}。"
    )
    report.append("")
    report.append("### 剔除清单")
    report.extend(
        md_table(
            ["剔除项", "数量", "公司"],
            [
                ["低流动性", int(main_df["low_liquidity"].sum()), tickers_text(main_df.loc[main_df["low_liquidity"], "ticker"])],
                ["ADR/币种异常", int(main_df["adr_currency_abnormal"].sum()), tickers_text(main_df.loc[main_df["adr_currency_abnormal"], "ticker"])],
                ["极端涨跌双尾5%", int(main_df["extreme_return"].sum()), tickers_text(main_df.loc[main_df["extreme_return"], "ticker"])],
            ],
        )
    )
    report.append("")
    report.append("## 诊断：收益由哪些公司主导")
    report.append("### 三段累计表现最好15")
    report.extend(
        md_table(
            ["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F52分", "F52排名", "置信度"],
            stock_table(main_df.sort_values("cum_ret", ascending=False).head(15)),
        )
    )
    report.append("")
    report.append("### 三段累计表现最差15")
    report.extend(
        md_table(
            ["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F52分", "F52排名", "置信度"],
            stock_table(main_df.sort_values("cum_ret", ascending=True).head(15)),
        )
    )
    report.append("")
    report.append("### F52高分前15")
    report.extend(
        md_table(
            ["排名", "股票代号", "公司名称", "分类目录", "F52分", "三段累计", "压力窗口均值", "近ATM IV", "置信度"],
            score_extreme_table(sort_by_score(main_df, high=True).head(15)),
        )
    )
    report.append("")
    report.append("### F52低分前15")
    report.extend(
        md_table(
            ["排名", "股票代号", "公司名称", "分类目录", "F52分", "三段累计", "压力窗口均值", "近ATM IV", "置信度"],
            score_extreme_table(sort_by_score(main_df, high=False).head(15)),
        )
    )
    report.append("")
    report.append("## 使用建议")
    if spearman > 0.1:
        report.append("- 可以把 F52 作为 SOXX压力期防守质量、监管/地缘尾部风险过滤和仓位上限因子：全样本、分类中性和稳健剔除后的排序方向若保持正向，说明高F52公司在压力窗口里通常少跌、最差窗口更浅。")
    else:
        report.append("- 不建议单独把 F52 当作本次三段SOXX压力窗口的正向排序因子：若全样本和稳健样本 Spearman 偏弱或为负，应把它定位为风险解释和复核标签。")
    report.append("- 不建议把 F52 单独替代收益因子：监管地缘风险可控性高的公司往往更偏成熟、防御或受监管资产，进攻弹性可能弱于低分高波动资产。")
    report.append("- 组合使用上，F52适合与F50价格相对强度、F51交易流动性、F41负向预期差风险、F45执行风险、估值赔率和订单下修风险联用；高F52但价格弱的公司可能只是抗跌，低F52但动量强的公司需要额外催化剂和仓位折扣。")
    report.append("- 复核重点应放在两个尾部：一是低F52且压力窗口大跌的核许可、融资、电力并网、小盘或出口管制敏感公司；二是低F52但压力期少跌的单段反弹公司，判断是否为数据口径、事件驱动还是风险折价已释放。")
    report.append("- 后续若要做严格因子回测，需要用评分形成日前的历史评分快照，对之后的1/3/6个月收益做前瞻检验，并补充逐日价格序列计算真实波动率、最大回撤和SOXX下跌日alpha。")
    report.append("")
    report.append("## 方法说明")
    report.append("- 相关性：Pearson 使用原始 F52 分数与三段累计收益；Spearman 使用并列平均秩；Kendall 使用 tau-b，并对 F52 分数并列做 tie 修正。")
    report.append("- Top/Bottom：按 F52 分数从高到低排序，同分时沿用评分文件原排名顺序；Bottom 为低分端。")
    report.append("- 分类中性：先在每个分类目录内计算 F52 分数百分位，再合并全样本；残差口径为 F52 分数和三段累计收益分别减去所在分类均值。")
    report.append("- 风险窗口：三段 SOXX 下跌窗口来自 `日度资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`；公司收益均为窗口起止价变动，不含股息再投资。")
    report.append(f"- 稳健性：低流动性剔除使用 F51<=5.0 代理；ADR/币种异常来自每日金融数据的 listing_type、adr_ratio、currency/financial_currency 和 currency_mismatch 标记；极端涨跌剔除使用三段累计收益双尾5%线性分位阈值 {fmt_pct(q_low)} / {fmt_pct(q_high)}。")

    OUT_PATH.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"wrote={OUT_PATH}")
    print(f"rows_f52={len(f52)} rows_returns={len(returns)} main={len(main_df)}")
    print(f"main_corr pearson={fmt_corr(main_corr['pearson'])} spearman={fmt_corr(main_corr['spearman'])} kendall={fmt_corr(main_corr['kendall'])}")
    print(f"top30={fmt_pct(top_bottom_30['top_mean'])} bottom30={fmt_pct(top_bottom_30['bottom_mean'])} diff={fmt_pct(top_bottom_30['diff'])}")
    print(f"robust_combined_n={len(combined['part'])} spearman={fmt_corr(combined['stats']['spearman'])} diff={fmt_pct(combined['combo']['diff'])}")


if __name__ == "__main__":
    main()
