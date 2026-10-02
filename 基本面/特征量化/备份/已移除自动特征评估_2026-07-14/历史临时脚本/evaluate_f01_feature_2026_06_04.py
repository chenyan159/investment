from __future__ import annotations

import math
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
SCORE_PATH = ROOT / "特征量化" / "量化评分" / "F01_AI收益暴露纯度_量化评分_2026-06-04.md"
RETURNS_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
LIQUIDITY_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
FINANCIAL_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUT_DIR / "备份"
OUT_PATH = OUT_DIR / "F01_AI收益暴露纯度_特征评估_6个月涨跌_2026-06-04.md"

SOXX_WINDOWS = {
    "stress1": ("SOXX下跌1", "2025-02-20至2025-04-08", -32.98),
    "stress2": ("SOXX下跌2", "2026-02-25至2026-03-30", -15.82),
    "stress3": ("SOXX下跌3", "2025-10-29至2025-11-20", -13.40),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_md_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells)


def parse_pct(cell: str) -> float | None:
    if not cell or "N/A" in cell or "缺失" in cell:
        return None
    text = cell.replace(",", "")
    match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%", text)
    if not match:
        return None
    return float(match.group(1))


def parse_float(text: str) -> float | None:
    if text is None:
        return None
    s = str(text).replace(",", "").strip()
    if not s or s in {"N/A", "缺失"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", str(s).replace("<br>", " / ")).strip()


def parse_score_table(path: Path) -> pd.DataFrame:
    text = read_text(path)
    rows: list[dict] = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## 全公司排序表":
            in_table = True
            continue
        if in_table and stripped.startswith("## "):
            break
        if not in_table or not stripped.startswith("|"):
            continue
        cells = split_md_row(stripped)
        if is_separator(cells) or not cells or cells[0] == "排名":
            continue
        if len(cells) < 10 or not cells[0].isdigit():
            continue
        rows.append(
            {
                "score_rank": int(cells[0]),
                "ticker": cells[1],
                "company": cells[2],
                "category": cells[3],
                "score": float(cells[4]),
                "evidence": cells[5],
                "confidence": cells[6],
                "core_evidence": clean(cells[7]),
                "score_deduction": clean(cells[8]),
                "follow_up": clean(cells[9]),
            }
        )
    return pd.DataFrame(rows)


def parse_return_details(path: Path) -> pd.DataFrame:
    text = read_text(path)
    rows: list[dict] = []
    in_section = False
    category: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## 按分类分组的公司明细":
            in_section = True
            continue
        if not in_section:
            continue
        if stripped.startswith("### "):
            category = stripped[4:].strip()
            continue
        if not stripped.startswith("|") or category is None:
            continue
        cells = split_md_row(stripped)
        if is_separator(cells) or not cells or cells[0] == "股票代号":
            continue
        if len(cells) < 9:
            continue
        rows.append(
            {
                "ticker": cells[0],
                "return_company": cells[1],
                "return_category": category,
                "latest_trade_date": cells[2],
                "last_close": parse_float(cells[3]),
                "return_1m": parse_pct(cells[4]),
                "return_3m": parse_pct(cells[5]),
                "return_6m": parse_pct(cells[6]),
                "return_1y": parse_pct(cells[7]),
                "return_note": clean(cells[8]),
            }
        )
    return pd.DataFrame(rows)


def parse_stress_details(path: Path) -> pd.DataFrame:
    text = read_text(path)
    rows: list[dict] = []
    in_section = False
    category: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "### 按分类分组的全公司明细":
            in_section = True
            continue
        if in_section and stripped == "## 按分类分组的公司明细":
            break
        if not in_section:
            continue
        if stripped.startswith("#### "):
            category = stripped[5:].strip()
            continue
        if not stripped.startswith("|") or category is None:
            continue
        cells = split_md_row(stripped)
        if is_separator(cells) or not cells or cells[0] == "股票代号":
            continue
        if len(cells) < 6:
            continue
        rows.append(
            {
                "ticker": cells[0],
                "stress_company": cells[1],
                "stress_category": category,
                "stress1": parse_pct(cells[2]),
                "stress2": parse_pct(cells[3]),
                "stress3": parse_pct(cells[4]),
                "stress_note": clean(cells[5]),
            }
        )
    return pd.DataFrame(rows)


def parse_financial_details(path: Path) -> pd.DataFrame:
    text = read_text(path)
    rows: list[dict] = []
    in_section = False
    category: str | None = None
    header: list[str] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## 按项目分类分组的公司明细表":
            in_section = True
            continue
        if not in_section:
            continue
        if stripped.startswith("### "):
            category = stripped[4:].strip()
            header = None
            continue
        if not stripped.startswith("|") or category is None:
            continue
        cells = split_md_row(stripped)
        if is_separator(cells):
            continue
        if cells and cells[0] == "股票代号":
            header = cells
            continue
        if not header or len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        rows.append(
            {
                "ticker": row.get("股票代号", ""),
                "financial_category": category,
                "price_date": row.get("价格日期", ""),
                "currency": row.get("currency", ""),
                "financial_currency": row.get("financial_currency", ""),
                "listing_type": row.get("listing_type", ""),
                "adr_ratio": row.get("adr_ratio", ""),
                "valuation_check": row.get("估值校验", ""),
                "financial_note": clean(row.get("备注", "")),
            }
        )
    return pd.DataFrame(rows)


def rank_average(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = avg_rank
        i = j
    return ranks


def pearson(xs: list[float], ys: list[float]) -> float:
    pairs = [(float(x), float(y)) for x, y in zip(xs, ys) if pd.notna(x) and pd.notna(y)]
    if len(pairs) < 2:
        return float("nan")
    x_vals, y_vals = zip(*pairs)
    mx = sum(x_vals) / len(x_vals)
    my = sum(y_vals) / len(y_vals)
    num = sum((x - mx) * (y - my) for x, y in pairs)
    den_x = math.sqrt(sum((x - mx) ** 2 for x in x_vals))
    den_y = math.sqrt(sum((y - my) ** 2 for y in y_vals))
    if den_x == 0 or den_y == 0:
        return float("nan")
    return num / (den_x * den_y)


def spearman(xs: list[float], ys: list[float]) -> float:
    pairs = [(float(x), float(y)) for x, y in zip(xs, ys) if pd.notna(x) and pd.notna(y)]
    if len(pairs) < 2:
        return float("nan")
    x_vals, y_vals = zip(*pairs)
    return pearson(rank_average(list(x_vals)), rank_average(list(y_vals)))


def kendall_tau_b(xs: list[float], ys: list[float]) -> float:
    pairs = [(float(x), float(y)) for x, y in zip(xs, ys) if pd.notna(x) and pd.notna(y)]
    n = len(pairs)
    if n < 2:
        return float("nan")
    concordant = discordant = ties_x = ties_y = 0
    for i in range(n - 1):
        x1, y1 = pairs[i]
        for j in range(i + 1, n):
            x2, y2 = pairs[j]
            dx = (x1 > x2) - (x1 < x2)
            dy = (y1 > y2) - (y1 < y2)
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                ties_x += 1
            elif dy == 0:
                ties_y += 1
            elif dx == dy:
                concordant += 1
            else:
                discordant += 1
    denom = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    if denom == 0:
        return float("nan")
    return (concordant - discordant) / denom


def correlations(df: pd.DataFrame, score_col: str = "score", return_col: str = "return_6m") -> dict[str, float]:
    sub = df[[score_col, return_col]].dropna()
    x = sub[score_col].astype(float).tolist()
    y = sub[return_col].astype(float).tolist()
    return {
        "n": len(sub),
        "pearson": pearson(x, y),
        "spearman": spearman(x, y),
        "kendall": kendall_tau_b(x, y),
    }


def pct(v: float | None) -> str:
    if v is None or pd.isna(v):
        return "N/A"
    return f"{v:+.2f}%"


def num(v: float | None, digits: int = 3) -> str:
    if v is None or pd.isna(v):
        return "N/A"
    return f"{v:.{digits}f}"


def one_decimal(v: float | None) -> str:
    if v is None or pd.isna(v):
        return "N/A"
    return f"{v:.1f}"


def rate(v: float | None) -> str:
    if v is None or pd.isna(v):
        return "N/A"
    return f"{v:.1f}%"


def summarize_group(df: pd.DataFrame) -> dict[str, float]:
    returns = df["return_6m"].dropna().astype(float)
    scores = df["score"].dropna().astype(float)
    if returns.empty:
        return {"n": len(df), "score_mean": float("nan"), "mean": float("nan"), "median": float("nan"), "hit": float("nan")}
    return {
        "n": len(df),
        "score_mean": scores.mean() if not scores.empty else float("nan"),
        "mean": returns.mean(),
        "median": returns.median(),
        "hit": (returns > 0).mean() * 100,
    }


def top_bottom_stats(df: pd.DataFrame, n: int, neutral: bool = False) -> dict[str, float]:
    if neutral:
        ordered = df.sort_values(["cat_score_pct", "score_rank"], ascending=[False, True])
        bottom_ordered = df.sort_values(["cat_score_pct", "score_rank"], ascending=[True, False])
    else:
        ordered = df.sort_values(["score_rank"], ascending=True)
        bottom_ordered = df.sort_values(["score_rank"], ascending=False)
    top = ordered.head(n)
    bottom = bottom_ordered.head(n)
    top_summary = summarize_group(top)
    bottom_summary = summarize_group(bottom)
    return {
        "n": n,
        "top_mean": top_summary["mean"],
        "top_hit": top_summary["hit"],
        "bottom_mean": bottom_summary["mean"],
        "bottom_hit": bottom_summary["hit"],
        "spread": top_summary["mean"] - bottom_summary["mean"],
    }


def split_score_quintiles(df: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    ordered = df.sort_values("score_rank", ascending=True).reset_index(drop=True)
    n = len(ordered)
    base = n // 5
    rem = n % 5
    sizes = [base + (1 if i < rem else 0) for i in range(5)]
    groups = []
    start = 0
    labels = ["Q1最高分", "Q2", "Q3", "Q4", "Q5最低分"]
    for label, size in zip(labels, sizes):
        groups.append((label, ordered.iloc[start : start + size].copy()))
        start += size
    return groups


def category_percentiles(df: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    for _, g in df.groupby("category", sort=False):
        g = g.copy()
        n = len(g)
        if n == 1:
            g["cat_score_pct"] = 1.0
        else:
            # Higher score should mean higher percentile. Ties receive average rank.
            ranks = rank_average((-g["score"]).astype(float).tolist())
            g["cat_score_pct"] = [(n - r) / (n - 1) for r in ranks]
        g["score_resid_cat"] = g["score"] - g["score"].mean()
        g["return_resid_cat"] = g["return_6m"] - g["return_6m"].mean()
        pieces.append(g)
    return pd.concat(pieces, ignore_index=True)


def stress_group_stats(df: pd.DataFrame, label: str) -> dict[str, object]:
    window_means: dict[str, float] = {}
    all_values: list[float] = []
    worst_values: list[float] = []
    outperf = total = negative = 0
    per_company_std: list[float] = []
    for _, row in df.iterrows():
        company_values = []
        for key, (_, _, soxx_ret) in SOXX_WINDOWS.items():
            val = row.get(key)
            if pd.notna(val):
                company_values.append(float(val))
                all_values.append(float(val))
                total += 1
                if float(val) > soxx_ret:
                    outperf += 1
                if float(val) < 0:
                    negative += 1
        if company_values:
            worst_values.append(min(company_values))
            if len(company_values) >= 2:
                avg = sum(company_values) / len(company_values)
                per_company_std.append(math.sqrt(sum((v - avg) ** 2 for v in company_values) / (len(company_values) - 1)))
    for key in SOXX_WINDOWS:
        vals = [float(v) for v in df[key].dropna().tolist()]
        window_means[key] = sum(vals) / len(vals) if vals else float("nan")
    return {
        "label": label,
        "n": len(df),
        "obs": total,
        "stress1_mean": window_means["stress1"],
        "stress2_mean": window_means["stress2"],
        "stress3_mean": window_means["stress3"],
        "pressure_mean": sum(all_values) / len(all_values) if all_values else float("nan"),
        "avg_worst": sum(worst_values) / len(worst_values) if worst_values else float("nan"),
        "dispersion": sum(per_company_std) / len(per_company_std) if per_company_std else float("nan"),
        "outperform_soxx": outperf / total * 100 if total else float("nan"),
        "negative_ratio": negative / total * 100 if total else float("nan"),
    }


def sample_robustness(df: pd.DataFrame, label: str, rule: str, mask: pd.Series) -> dict[str, object]:
    sub = df[mask].copy()
    c = correlations(sub)
    tb = top_bottom_stats(sub, min(30, max(1, len(sub) // 2)))
    return {
        "label": label,
        "rule": rule,
        "n": len(sub),
        "excluded": len(df) - len(sub),
        "pearson": c["pearson"],
        "spearman": c["spearman"],
        "kendall": c["kendall"],
        "top30": tb["top_mean"],
        "bottom30": tb["bottom_mean"],
        "spread": tb["spread"],
    }


def md_table(headers: list[str], rows: list[list[str]], aligns: list[str] | None = None) -> str:
    aligns = aligns or ["---"] * len(headers)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(aligns) + " |"]
    out += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(out)


def extract_meta(text: str, pattern: str, default: str = "未解析") -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else default


def backup_existing_outputs() -> list[str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    candidates = sorted(OUT_DIR.glob("F01_AI收益暴露纯度_特征评估_6个月涨跌_*.md"))
    if not candidates:
        return moved
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_backup_dir = BACKUP_DIR / f"F01_AI收益暴露纯度_6个月涨跌_运行前备份_{stamp}"
    run_backup_dir.mkdir(parents=True, exist_ok=True)
    for src in candidates:
        if src.resolve() == OUT_PATH.resolve():
            # Treat an existing target as an old formal output for this rerun.
            pass
        dst = run_backup_dir / src.name
        shutil.move(str(src), str(dst))
        moved.append(str(dst.relative_to(ROOT)))
    return moved


def build_report() -> tuple[str, dict[str, object]]:
    score_df = parse_score_table(SCORE_PATH)
    returns_df = parse_return_details(RETURNS_PATH)
    stress_df = parse_stress_details(RETURNS_PATH)
    liquidity_df = parse_score_table(LIQUIDITY_PATH).rename(
        columns={"score": "liquidity_score", "score_rank": "liquidity_rank"}
    )[["ticker", "liquidity_score", "liquidity_rank"]]
    financial_df = parse_financial_details(FINANCIAL_PATH)

    df = score_df.merge(returns_df, on="ticker", how="inner")
    df = df.merge(stress_df[["ticker", "stress1", "stress2", "stress3"]], on="ticker", how="left")
    df = df.merge(liquidity_df, on="ticker", how="left")
    df = df.merge(financial_df, on="ticker", how="left")
    df = category_percentiles(df)

    c_main = correlations(df)
    score_only = set(score_df["ticker"])
    returns_only = set(returns_df["ticker"])
    missing_returns = sorted(score_only - returns_only)
    missing_scores = sorted(returns_only - score_only)

    category_rows = []
    for category, g in df.groupby("category", sort=False):
        category_rows.append(
            [
                category,
                str(len(g)),
                one_decimal(g["score"].mean()),
                pct(g["return_6m"].mean()),
                pct(g["return_6m"].median()),
            ]
        )

    corr_table_rows = [
        ["Pearson", num(c_main["pearson"], 3), "线性相关；容易受极端涨跌影响"],
        ["Spearman", num(c_main["spearman"], 3), "排序相关；本特征评估的主指标"],
        ["Kendall tau-b", num(c_main["kendall"], 3), "成对排序胜率；已处理分数并列"],
    ]

    quintile_rows = []
    for label, g in split_score_quintiles(df):
        s = summarize_group(g)
        quintile_rows.append([label, str(s["n"]), one_decimal(s["score_mean"]), pct(s["mean"]), pct(s["median"]), rate(s["hit"])])

    tb_rows = []
    tb_values = {}
    for n in [10, 20, 30]:
        stats = top_bottom_stats(df, n)
        tb_values[n] = stats
        tb_rows.append([f"Top{n}/Bottom{n}", pct(stats["top_mean"]), rate(stats["top_hit"]), pct(stats["bottom_mean"]), rate(stats["bottom_hit"]), pct(stats["spread"])])

    top10 = df.sort_values("score_rank", ascending=True).head(10)
    bottom10 = df.sort_values("score_rank", ascending=False).head(10)
    tb_detail_rows = []
    for group_label, sub in [("Top10", top10), ("Bottom10", bottom10)]:
        sort_sub = sub.sort_values("score_rank", ascending=True if group_label == "Top10" else False)
        for _, row in sort_sub.iterrows():
            tb_detail_rows.append(
                [
                    group_label,
                    row["ticker"],
                    row["company"],
                    row["category"],
                    one_decimal(row["score"]),
                    str(int(row["score_rank"])),
                    pct(row["return_6m"]),
                ]
            )

    ordered = df.sort_values("score_rank", ascending=True).reset_index(drop=True)
    top30 = ordered.head(30)
    mid_start = max(0, (len(ordered) - 30) // 2)
    mid30 = ordered.iloc[mid_start : mid_start + 30]
    bottom30 = ordered.tail(30)
    risk_stats = [
        stress_group_stats(top30, "F01 Top30"),
        stress_group_stats(mid30, "F01 Mid30"),
        stress_group_stats(bottom30, "F01 Bottom30"),
    ]
    risk_rows = []
    for s in risk_stats:
        risk_rows.append(
            [
                str(s["label"]),
                str(s["n"]),
                str(s["obs"]),
                pct(s["stress1_mean"]),
                pct(s["stress2_mean"]),
                pct(s["stress3_mean"]),
                pct(s["pressure_mean"]),
                pct(s["avg_worst"]),
                pct(s["dispersion"]),
                rate(s["outperform_soxx"]),
                rate(s["negative_ratio"]),
            ]
        )

    c_neutral_pct = correlations(df, "cat_score_pct", "return_6m")
    c_resid = correlations(df, "score_resid_cat", "return_resid_cat")
    neutral_corr_rows = [
        ["原始全样本", str(c_main["n"]), num(c_main["pearson"], 3), num(c_main["spearman"], 3), num(c_main["kendall"], 3), "直接用F01分数排序"],
        ["分类内百分位合并", str(c_neutral_pct["n"]), num(c_neutral_pct["pearson"], 3), num(c_neutral_pct["spearman"], 3), num(c_neutral_pct["kendall"], 3), "每个分类内先按F01排序，再转成0-1百分位合并"],
        ["分类去均值残差", str(c_resid["n"]), num(c_resid["pearson"], 3), num(c_resid["spearman"], 3), num(c_resid["kendall"], 3), "F01和收益分别减去分类均值后相关"],
    ]

    neutral_tb_rows = []
    neutral_tb_values = {}
    for n in [10, 20, 30]:
        stats = top_bottom_stats(df, n, neutral=True)
        neutral_tb_values[n] = stats
        neutral_tb_rows.append([f"中性Top{n}/Bottom{n}", pct(stats["top_mean"]), rate(stats["top_hit"]), pct(stats["bottom_mean"]), rate(stats["bottom_hit"]), pct(stats["spread"])])

    category_corr_rows = []
    for category, g in df.groupby("category", sort=False):
        c = correlations(g)
        winner = g.sort_values("return_6m", ascending=False).iloc[0]
        top_score = g.sort_values(["score", "score_rank"], ascending=[False, True]).iloc[0]
        category_corr_rows.append(
            [
                category,
                str(len(g)),
                num(c["pearson"], 3),
                num(c["spearman"], 3),
                pct(g["return_6m"].mean()),
                f"{winner['ticker']} {pct(winner['return_6m'])}",
                f"{top_score['ticker']} {one_decimal(top_score['score'])} / {pct(top_score['return_6m'])}",
            ]
        )

    low_liquidity_mask = df["liquidity_score"].fillna(-999) <= 5.0
    adr_currency_anomaly_mask = (
        (df["listing_type"].fillna("") != "common/equity")
        | (df["currency"].fillna("") != df["financial_currency"].fillna(""))
        | df["valuation_check"].fillna("").str.contains("currency_mismatch", regex=False)
    )
    low_q = df["return_6m"].quantile(0.05)
    high_q = df["return_6m"].quantile(0.95)
    extreme_mask = (df["return_6m"] < low_q) | (df["return_6m"] > high_q)
    robust_rows_data = [
        sample_robustness(df, "全样本基准", "无剔除", pd.Series([True] * len(df), index=df.index)),
        sample_robustness(df, "剔除低流动性", "F51交易流动性分 > 5.0", ~low_liquidity_mask),
        sample_robustness(df, "剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", ~adr_currency_anomaly_mask),
        sample_robustness(df, "剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {pct(low_q)} / {pct(high_q)}", ~extreme_mask),
        sample_robustness(df, "三项合并剔除", "同时满足上述三项", ~(low_liquidity_mask | adr_currency_anomaly_mask | extreme_mask)),
    ]
    robust_rows = [
        [
            str(r["label"]),
            str(r["rule"]),
            str(r["n"]),
            str(r["excluded"]),
            num(r["pearson"], 3),
            num(r["spearman"], 3),
            num(r["kendall"], 3),
            pct(r["top30"]),
            pct(r["bottom30"]),
            pct(r["spread"]),
        ]
        for r in robust_rows_data
    ]

    exclusions_rows = [
        ["低流动性", str(int(low_liquidity_mask.sum())), ", ".join(df.loc[low_liquidity_mask, "ticker"].sort_values().tolist()) or "无"],
        ["ADR/币种异常", str(int(adr_currency_anomaly_mask.sum())), ", ".join(df.loc[adr_currency_anomaly_mask, "ticker"].sort_values().tolist()) or "无"],
        ["极端涨跌双尾5%", str(int(extreme_mask.sum())), ", ".join(df.loc[extreme_mask, "ticker"].sort_values().tolist()) or "无"],
    ]

    winners = df.sort_values("return_6m", ascending=False).head(15)
    losers = df.sort_values("return_6m", ascending=True).head(15)
    winners_rows = [
        [row["ticker"], row["company"], row["category"], pct(row["return_6m"]), one_decimal(row["score"]), str(int(row["score_rank"])), row["confidence"]]
        for _, row in winners.iterrows()
    ]
    losers_rows = [
        [row["ticker"], row["company"], row["category"], pct(row["return_6m"]), one_decimal(row["score"]), str(int(row["score_rank"])), row["confidence"]]
        for _, row in losers.iterrows()
    ]

    # Lightweight attribution by score decile extremes.
    top30_mean = tb_values[30]["top_mean"]
    bottom30_mean = tb_values[30]["bottom_mean"]
    top30_spread = tb_values[30]["spread"]
    neutral_spread = neutral_tb_values[30]["spread"]
    combined_spearman = robust_rows_data[-1]["spearman"]

    sort_eval = "成立" if c_main["spearman"] >= 0.20 else ("弱成立" if c_main["spearman"] >= 0.08 else "不成立")
    tb_eval = "成立" if top30_spread > 15 else ("弱成立" if top30_spread > 0 else "不成立")
    neutral_eval = "成立" if c_neutral_pct["spearman"] >= 0.15 and neutral_spread > 0 else ("弱成立" if c_neutral_pct["spearman"] > 0 and neutral_spread > 0 else "不成立")
    robust_eval = "稳定" if combined_spearman >= 0.10 and robust_rows_data[-1]["spread"] > 0 else "不稳定"

    risk_eval = "更稳" if risk_stats[0]["pressure_mean"] > risk_stats[2]["pressure_mean"] and risk_stats[0]["avg_worst"] > risk_stats[2]["avg_worst"] else "没有更稳"

    returns_text = read_text(RETURNS_PATH)
    score_text = read_text(SCORE_PATH)
    financial_text = read_text(FINANCIAL_PATH)
    generated_time = extract_meta(returns_text, r"生成时间：(.+?)（")
    latest_trade = extract_meta(returns_text, r"最新可得交易日最大值：`([^`]+)`")
    common_trade = extract_meta(returns_text, r"最常见价格日期：`([^`]+)`")
    financial_generated = extract_meta(financial_text, r"生成时间：(.+)")

    lines: list[str] = []
    lines.append("# F01 AI收益暴露纯度 特征评估 6个月涨跌 2026-06-04")
    lines.append("")
    lines.append("## 运行元信息")
    lines.append("- 评估对象：F01_AI收益暴露纯度。")
    lines.append(f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 2026-06-04，覆盖 {len(score_df)} 家。")
    lines.append(f"- 收益输入：`日度资料/区间涨跌/{RETURNS_PATH.name}`，生成时间 {generated_time}，价格最新交易日 {latest_trade}，最常见价格日期 {common_trade}；6个月价格涨跌不含股息再投资。")
    lines.append("- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。")
    lines.append(f"- 稳健性辅助输入：`特征量化/量化评分/{LIQUIDITY_PATH.name}`；`日度资料/每日金融数据/{FINANCIAL_PATH.name}`，金融数据生成时间 {financial_generated}。")
    lines.append(f"- 有效评估样本：评分与6个月涨跌交集 {len(df)} 家；F01评分有但6个月涨跌缺失 {len(missing_returns)} 家。")
    lines.append("- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。")
    lines.append("- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为风险代理。")
    lines.append("- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。")
    lines.append("- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F01 正式输出；若有残留先移动到 `特征量化/特征评估/备份/`。本次未读取旧版 F01 特征评估作为结论依据。")
    lines.append("")
    lines.append("## 结论摘要")
    lines.append(f"- 排序有效性：{sort_eval}。全样本 Pearson {num(c_main['pearson'], 3)}, Spearman {num(c_main['spearman'], 3)}, Kendall {num(c_main['kendall'], 3)}；核心 Spearman {num(c_main['spearman'], 3)}，说明 F01 对本次6个月收益排序的单因子解释力{'较强' if c_main['spearman'] >= 0.20 else '有限' if c_main['spearman'] >= 0.08 else '接近0或方向不足'}。")
    lines.append(f"- Top/Bottom能力：{tb_eval}。Top10、Top20、Top30 的平均收益分别为 {pct(tb_values[10]['top_mean'])}、{pct(tb_values[20]['top_mean'])}、{pct(tb_values[30]['top_mean'])}；Top-Bottom 收益差分别为 {pct(tb_values[10]['spread'])}、{pct(tb_values[20]['spread'])}、{pct(tb_values[30]['spread'])}。")
    lines.append(f"- 风险解释力：{risk_eval}。Top30 压力窗口均值 {pct(risk_stats[0]['pressure_mean'])}，平均最差窗口 {pct(risk_stats[0]['avg_worst'])}，跑赢 SOXX 比例 {rate(risk_stats[0]['outperform_soxx'])}；Bottom30 对应为 {pct(risk_stats[2]['pressure_mean'])}、{pct(risk_stats[2]['avg_worst'])}、{rate(risk_stats[2]['outperform_soxx'])}。")
    lines.append(f"- 分类中性：{neutral_eval}。分类内百分位合并后 Spearman {num(c_neutral_pct['spearman'], 3)}，中性 Top30-Bottom30 收益差 {pct(neutral_spread)}；分类去均值残差 Spearman {num(c_resid['spearman'], 3)}。")
    lines.append(f"- 稳健性：{robust_eval}。剔除低流动性后 Spearman {num(robust_rows_data[1]['spearman'], 3)}，剔除 ADR/币种异常后 {num(robust_rows_data[2]['spearman'], 3)}，剔除极端涨跌后 {num(robust_rows_data[3]['spearman'], 3)}，三项合并后 {num(combined_spearman, 3)}。")
    lines.append(f"- 解释：F01 衡量 AI 收入暴露纯度，能识别 NVDA、CRWV、NBIS、AVGO、VRT 等 AI 主线资产，但 2025-11至2026-05 的6个月收益被 AXTI、SNDK、AAOI、MXL、AEHR、ICHR、MRAM、FCEL 等高弹性/修复型标的显著拉动；因此若 Spearman 和 Top-Bottom 差距不足，问题不在于 AI 暴露没有经济意义，而在于该窗口的股价排序同时受小盘弹性、估值修复、事件催化和流动性影响。")
    lines.append("")
    lines.append("## 覆盖检查")
    lines.append(
        md_table(
            ["项目", "数量", "说明"],
            [
                ["F01评分覆盖", str(len(score_df)), "来自2026-06-04评分文件"],
                ["6个月涨跌覆盖", str(len(returns_df)), "来自2026-05-27区间涨跌文件"],
                ["交集样本", str(len(df)), "用于本次所有主指标"],
                ["评分有但6个月涨跌缺失", str(len(missing_returns)), ", ".join(missing_returns) if missing_returns else "无"],
                ["涨跌有但评分缺失", str(len(missing_scores)), ", ".join(missing_scores) if missing_scores else "无"],
            ],
            ["---", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.append(md_table(["分类目录", "样本数", "F01均分", "6个月平均收益", "6个月中位收益"], category_rows, ["---", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## 排序有效性")
    lines.append(md_table(["指标", "数值", "解释"], corr_table_rows, ["---", "---:", "---"]))
    lines.append("")
    lines.append("### 分数分组收益")
    lines.append(md_table(["分组", "公司数", "F01均分", "6个月平均收益", "6个月中位收益", "命中率"], quintile_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## Top/Bottom能力")
    lines.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], tb_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    lines.append(md_table(["组别", "股票代号", "公司名称", "分类目录", "F01分", "F01排名", "6个月收益"], tb_detail_rows, ["---", "---", "---", "---", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为压力测试代理。严格日度波动率、完整最大回撤和真实下跌日收益稳定性需要逐日收益序列，本次输入文件没有提供，故不写成严格日度波动结论。")
    lines.append(md_table(["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"], risk_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("结论：若 Top30 的压力窗口均值、平均最差窗口和跑赢 SOXX 比例没有同步优于 Bottom30，则不能把 F01 写成下跌保护因子；若仅窗口离散度较低，只能说明高分组在压力期表现更一致，不能等同于回撤更小。")
    lines.append("")
    lines.append("## 分类中性结果")
    lines.append(md_table(["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"], neutral_corr_rows, ["---", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], neutral_tb_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(md_table(["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F01公司"], category_corr_rows, ["---", "---:", "---:", "---:", "---:", "---", "---"]))
    lines.append("")
    lines.append("分类内结果用于判断 F01 是否只是押中了某个目录。若分类内百分位和去均值残差仍为正，说明同目录内排序仍有信息；若转弱或转负，说明原始结果主要来自行业/分类暴露或个别极端公司。")
    lines.append("")
    lines.append("## 稳健性检验")
    lines.append(md_table(["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"], robust_rows, ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("稳健性结论：低流动性、ADR/币种异常和极端涨跌剔除后，重点看 Spearman 方向和 Top30-Bottom30 差值是否共同保持。若三项合并后只剩接近0的 Spearman 或负收益差，则 F01 不能作为独立6个月收益排序因子，只适合作为多因子基本面暴露维度。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(md_table(["剔除项", "数量", "公司"], exclusions_rows, ["---", "---:", "---"]))
    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "6个月收益", "F01分", "F01排名", "F01置信度"], winners_rows, ["---", "---", "---", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 6个月跌幅前15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "6个月收益", "F01分", "F01排名", "F01置信度"], losers_rows, ["---", "---", "---", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("## 可用性判断")
    if sort_eval in {"成立", "弱成立"} and tb_eval in {"成立", "弱成立"} and robust_eval == "稳定":
        final_judgment = "可作为6个月收益排序的候选单因子，但仍需与估值、动量、流动性和催化剂组合验证。"
    elif c_main["spearman"] > 0 and tb_values[30]["spread"] > 0:
        final_judgment = "有方向性信息，但单因子强度不足；适合作为多因子中的基本面纯度维度，不适合独立排序买卖。"
    else:
        final_judgment = "本窗口不支持把 F01 作为独立6个月收益排序因子；更适合作为解释公司 AI 主线暴露和风险分层的基础变量，需与 F05估值、F37-F39催化剂、F50价格相对强度和F51流动性联合使用。"
    lines.append(f"- 结论：{final_judgment}")
    lines.append("- 最应复核的不是高分公司基本面是否真实，而是股价窗口是否被极端小盘修复、分拆/上市时间、期权化交易和行业轮动主导。")
    lines.append("- 后续验证建议：把 F01 与估值压力、价格相对强度、1-3月/3-6月催化剂、交易流动性做二元或多元分层；同时使用 1个月、3个月、1年和 SOXX压力窗口分开回测，避免单一6个月窗口过拟合。")
    lines.append("")
    lines.append("## 数据来源路径")
    lines.append(f"- `特征量化/量化评分/{SCORE_PATH.name}`")
    lines.append(f"- `日度资料/区间涨跌/{RETURNS_PATH.name}`")
    lines.append(f"- `特征量化/量化评分/{LIQUIDITY_PATH.name}`")
    lines.append(f"- `日度资料/每日金融数据/{FINANCIAL_PATH.name}`")
    lines.append("")
    report = "\n".join(lines)
    summary = {
        "score_n": len(score_df),
        "returns_n": len(returns_df),
        "joined_n": len(df),
        "pearson": c_main["pearson"],
        "spearman": c_main["spearman"],
        "kendall": c_main["kendall"],
        "top30": top30_mean,
        "bottom30": bottom30_mean,
        "spread30": top30_spread,
        "neutral_spearman": c_neutral_pct["spearman"],
        "combined_spearman": combined_spearman,
        "low_q": low_q,
        "high_q": high_q,
        "sort_eval": sort_eval,
        "tb_eval": tb_eval,
        "neutral_eval": neutral_eval,
        "robust_eval": robust_eval,
    }
    return report, summary


def main() -> None:
    moved = backup_existing_outputs()
    report, summary = build_report()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(f"wrote={OUT_PATH}")
    print(f"backup_count={len(moved)}")
    for item in moved:
        print(f"backup={item}")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}={value:.6f}")
        else:
            print(f"{key}={value}")


if __name__ == "__main__":
    main()
