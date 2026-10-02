from __future__ import annotations

import math
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
FEATURE_ID = "F32"
FEATURE_NAME = "订单下修风险可控性"
FEATURE_SUBJECT = f"{FEATURE_ID}_{FEATURE_NAME}"
RUN_DATE = "2026-06-04"
WINDOW_NAME = "6个月"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_SUBJECT}_量化评分_{RUN_DATE}.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
LIQUIDITY_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
FINANCIAL_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUTPUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUTPUT_DIR / "备份"
OUTPUT_PATH = OUTPUT_DIR / f"{FEATURE_SUBJECT}_特征评估_{WINDOW_NAME}涨跌_{RUN_DATE}.md"

SOXX_BENCHMARKS = {
    "SOXX下跌1 2025-02-20至2025-04-08": -0.3298,
    "SOXX下跌2 2026-02-25至2026-03-30": -0.1582,
    "SOXX下跌3 2025-10-29至2025-11-20": -0.1340,
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells)


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def normalize_cells(cells: list[str], header: list[str]) -> list[str]:
    if len(cells) == len(header):
        return cells
    if len(cells) < len(header):
        return cells + [""] * (len(header) - len(cells))

    # Scoring tables can contain stray pipes in long evidence cells. Keep the
    # fixed leading columns and trailing action columns stable.
    if header[:5] == ["排名", "股票代号", "公司名称", "分类目录", "特征分"] and len(header) == 10:
        return cells[:7] + [" / ".join(cells[7 : len(cells) - 2])] + cells[-2:]

    # Other tables should not contain pipes, but if they do, preserve all excess
    # text in the last column rather than shifting numeric fields.
    return cells[: len(header) - 1] + [" / ".join(cells[len(header) - 1 :])]


def parse_single_table_after_heading(text: str, heading: str) -> pd.DataFrame:
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    in_table = False

    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## ") and in_table:
            break
        if not stripped.startswith("|"):
            if in_table and rows:
                break
            continue

        cells = split_md_row(stripped)
        if is_separator(cells):
            continue
        if header is None:
            header = cells
            in_table = True
            continue
        cells = normalize_cells(cells, header)
        rows.append(dict(zip(header, cells)))

    return pd.DataFrame(rows)


def extract_section(text: str, start_heading: str, end_heading: str | None = None) -> str:
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == start_heading)
    if end_heading is None:
        end = len(lines)
    else:
        matches = [i for i, line in enumerate(lines[start + 1 :], start + 1) if line.strip() == end_heading]
        end = matches[0] if matches else len(lines)
    return "\n".join(lines[start:end])


def parse_grouped_tables(section_text: str, subheading_prefix: str) -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    current_group: str | None = None
    header: list[str] | None = None
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(subheading_prefix + " "):
            current_group = stripped[len(subheading_prefix) :].strip()
            header = None
            continue
        if not stripped.startswith("|"):
            continue
        cells = split_md_row(stripped)
        if is_separator(cells):
            continue
        if header is None:
            header = cells
            continue
        cells = normalize_cells(cells, header)
        row = dict(zip(header, cells))
        if "分类目录" not in row:
            row["分类目录"] = current_group or ""
        rows.append(row)
    return pd.DataFrame(rows)


def parse_percent_cell(value: object) -> float:
    if value is None:
        return math.nan
    text = str(value).replace(",", "")
    if "N/A" in text or "缺失" in text or "不适用" in text:
        return math.nan
    match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%", text)
    if not match:
        return math.nan
    return float(match.group(1)) / 100.0


def parse_number(value: object) -> float:
    if value is None:
        return math.nan
    text = str(value).replace(",", "").strip()
    if not text or any(x in text for x in ["N/A", "缺失", "不适用"]):
        return math.nan
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else math.nan


def rank_average(values: np.ndarray) -> np.ndarray:
    series = pd.Series(values)
    return series.rank(method="average").to_numpy(dtype=float)


def corr_pearson(x: pd.Series, y: pd.Series) -> float:
    xx = pd.to_numeric(x, errors="coerce").to_numpy(dtype=float)
    yy = pd.to_numeric(y, errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(xx) & np.isfinite(yy)
    xx = xx[mask]
    yy = yy[mask]
    if len(xx) < 2 or np.std(xx) == 0 or np.std(yy) == 0:
        return math.nan
    return float(np.corrcoef(xx, yy)[0, 1])


def corr_spearman(x: pd.Series, y: pd.Series) -> float:
    xx = pd.to_numeric(x, errors="coerce").to_numpy(dtype=float)
    yy = pd.to_numeric(y, errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(xx) & np.isfinite(yy)
    xx = xx[mask]
    yy = yy[mask]
    if len(xx) < 2:
        return math.nan
    return corr_pearson(pd.Series(rank_average(xx)), pd.Series(rank_average(yy)))


def corr_kendall_tau_b(x: pd.Series, y: pd.Series) -> float:
    xx = pd.to_numeric(x, errors="coerce").to_numpy(dtype=float)
    yy = pd.to_numeric(y, errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(xx) & np.isfinite(yy)
    xx = xx[mask]
    yy = yy[mask]
    n = len(xx)
    if n < 2:
        return math.nan
    concordant = discordant = ties_x = ties_y = 0
    for i in range(n - 1):
        dx = np.sign(xx[i] - xx[i + 1 :])
        dy = np.sign(yy[i] - yy[i + 1 :])
        both_tied = (dx == 0) & (dy == 0)
        only_x = (dx == 0) & (dy != 0)
        only_y = (dx != 0) & (dy == 0)
        comparable = (dx != 0) & (dy != 0)
        ties_x += int(only_x.sum())
        ties_y += int(only_y.sum())
        concordant += int(((dx == dy) & comparable).sum())
        discordant += int(((dx != dy) & comparable).sum())
        # both_tied intentionally excluded from tau-b denominator.
        _ = both_tied
    denom = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    return math.nan if denom == 0 else (concordant - discordant) / denom


def correlations(df: pd.DataFrame, score_col: str = "score", ret_col: str = "ret_6m") -> dict[str, float]:
    return {
        "Pearson": corr_pearson(df[score_col], df[ret_col]),
        "Spearman": corr_spearman(df[score_col], df[ret_col]),
        "Kendall": corr_kendall_tau_b(df[score_col], df[ret_col]),
    }


def fmt_num(value: float, digits: int = 3) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value:.{digits}f}"


def fmt_score(value: float) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value:.1f}"


def fmt_pct(value: float, digits: int = 2) -> str:
    if value is None or not math.isfinite(value):
        return "N/A"
    return f"{value * 100:+.{digits}f}%"


def md_escape(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\n", "<br>").replace("|", "\\|")
    return text


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("| " + " | ".join(["---" for _ in headers]) + " |")
    for row in rows:
        out.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")
    return "\n".join(out)


def sorted_by_score(df: pd.DataFrame, score_col: str = "score") -> pd.DataFrame:
    working = df.reset_index(drop=True)
    rank_col = "rank" if "rank" in df.columns else None
    if rank_col:
        return working.sort_values([score_col, rank_col, "ticker"], ascending=[False, True, True]).reset_index(drop=True)
    return working.sort_values([score_col, "ticker"], ascending=[False, True]).reset_index(drop=True)


def top_bottom_stats(df: pd.DataFrame, score_col: str = "score", sizes: tuple[int, ...] = (10, 20, 30)) -> list[dict[str, float]]:
    ordered = sorted_by_score(df, score_col)
    results = []
    for n in sizes:
        top = ordered.head(n)
        bottom = ordered.tail(n)
        results.append(
            {
                "n": n,
                "top_mean": float(top["ret_6m"].mean()),
                "top_hit": float((top["ret_6m"] > 0).mean()),
                "bottom_mean": float(bottom["ret_6m"].mean()),
                "bottom_hit": float((bottom["ret_6m"] > 0).mean()),
                "diff": float(top["ret_6m"].mean() - bottom["ret_6m"].mean()),
            }
        )
    return results


def quintile_rows(df: pd.DataFrame) -> list[list[object]]:
    ordered = sorted_by_score(df)
    groups = [ordered.iloc[idx] for idx in np.array_split(np.arange(len(ordered)), 5)]
    rows = []
    names = ["Q1最高分", "Q2", "Q3", "Q4", "Q5最低分"]
    for name, group in zip(names, groups):
        rows.append(
            [
                name,
                len(group),
                fmt_score(group["score"].mean()),
                fmt_pct(group["ret_6m"].mean()),
                fmt_pct(group["ret_6m"].median()),
                fmt_pct((group["ret_6m"] > 0).mean()),
            ]
        )
    return rows


def top_bottom_constituents(df: pd.DataFrame, n: int = 10) -> list[list[object]]:
    ordered = sorted_by_score(df)
    top = ordered.head(n).copy()
    bottom = ordered.tail(n).sort_values("rank").copy()
    rows = []
    for label, group in [("Top10", top), ("Bottom10", bottom)]:
        for _, row in group.iterrows():
            rows.append(
                [
                    label,
                    row["ticker"],
                    row["company"],
                    row["category"],
                    fmt_score(row["score"]),
                    int(row["rank"]),
                    fmt_pct(row["ret_6m"]),
                    row["confidence"],
                ]
            )
    return rows


def stress_metrics(df: pd.DataFrame, label: str, indices: pd.Index) -> list[object]:
    group = df.loc[indices]
    cols = list(SOXX_BENCHMARKS.keys())
    values = group[cols]
    per_company_worst = values.min(axis=1, skipna=True)
    per_company_std = values.std(axis=1, skipna=True, ddof=0)
    observations = int(values.count().sum())
    outperform = []
    negatives = []
    for col, bench in SOXX_BENCHMARKS.items():
        col_values = values[col].dropna()
        outperform.extend(list(col_values > bench))
        negatives.extend(list(col_values < 0))
    return [
        label,
        len(group),
        observations,
        fmt_pct(values[cols[0]].mean()),
        fmt_pct(values[cols[1]].mean()),
        fmt_pct(values[cols[2]].mean()),
        fmt_pct(values.stack().mean()),
        fmt_pct(per_company_worst.mean()),
        fmt_pct(per_company_std.mean()),
        fmt_pct(float(np.mean(outperform)) if outperform else math.nan),
        fmt_pct(float(np.mean(negatives)) if negatives else math.nan),
    ]


def group_indices_for_risk(df: pd.DataFrame) -> dict[str, pd.Index]:
    ordered = sorted_by_score(df)
    n = len(ordered)
    mid_start = max((n - 30) // 2, 0)
    return {
        f"{FEATURE_ID} Top30": ordered.head(30).set_index("ticker").index,
        f"{FEATURE_ID} Mid30": ordered.iloc[mid_start : mid_start + 30].set_index("ticker").index,
        f"{FEATURE_ID} Bottom30": ordered.tail(30).set_index("ticker").index,
    }


def iv_group_rows(df: pd.DataFrame, indices_by_label: dict[str, pd.Index]) -> list[list[object]]:
    rows = []
    for label, idx in indices_by_label.items():
        group = df.loc[idx]
        rows.append(
            [
                label,
                len(group),
                int(group["near_iv"].notna().sum()),
                fmt_pct(group["call_iv"].mean()),
                fmt_pct(group["put_iv"].mean()),
                fmt_pct(group["near_iv"].mean()),
                fmt_pct(group["near_iv"].median()),
            ]
        )
    return rows


def category_neutral_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["category_percentile"] = out.groupby("category")["score"].rank(method="average", pct=True)
    out["score_residual"] = out["score"] - out.groupby("category")["score"].transform("mean")
    out["ret_residual"] = out["ret_6m"] - out.groupby("category")["ret_6m"].transform("mean")
    return out


def robustness_row(label: str, rule: str, baseline: pd.DataFrame, subset: pd.DataFrame) -> list[object]:
    corr = correlations(subset)
    tb = top_bottom_stats(subset, sizes=(30,))[0]
    return [
        label,
        rule,
        len(subset),
        len(baseline) - len(subset),
        fmt_num(corr["Pearson"]),
        fmt_num(corr["Spearman"]),
        fmt_num(corr["Kendall"]),
        fmt_pct(tb["top_mean"]),
        fmt_pct(tb["bottom_mean"]),
        fmt_pct(tb["diff"]),
    ]


def corr_direction(value: float) -> str:
    if not math.isfinite(value):
        return "无法判断"
    if value >= 0.20:
        return "正向有效"
    if value >= 0.10:
        return "弱正向"
    if value > -0.05:
        return "接近零"
    if value > -0.15:
        return "偏负"
    return "明显负向"


def top_bottom_judgement(diff30: float) -> str:
    if diff30 >= 0.20:
        return "成立，Top30 明显跑赢 Bottom30"
    if diff30 >= 0.05:
        return "弱成立，Top30 小幅跑赢 Bottom30"
    if diff30 > -0.05:
        return "接近持平"
    return "不成立，Top30 跑输 Bottom30"


def list_tickers(series: pd.Series) -> str:
    items = [str(x) for x in series.dropna().tolist()]
    return ", ".join(items) if items else "无"


def prepare_data() -> tuple[pd.DataFrame, dict[str, object]]:
    score_raw = parse_single_table_after_heading(read_text(SCORE_PATH), "## 全公司排序表")
    score = score_raw.rename(
        columns={
            "股票代号": "ticker",
            "公司名称": "company",
            "分类目录": "category",
            "特征分": "score",
            "排名": "rank",
            "置信度": "confidence",
            "证据等级": "evidence_level",
        }
    )
    score["score"] = score["score"].map(parse_number)
    score["rank"] = score["rank"].map(parse_number).astype(int)
    score = score[["ticker", "company", "category", "score", "rank", "confidence", "evidence_level"]]

    ret_section = extract_section(read_text(RETURN_PATH), "## 按分类分组的公司明细")
    ret_raw = parse_grouped_tables(ret_section, "###")
    ret = ret_raw.rename(
        columns={
            "股票代号": "ticker",
            "公司名称": "return_company",
            "分类目录": "return_category",
            "6个月": "ret_6m_cell",
            "最新交易日": "latest_trade_date",
        }
    )
    ret["ret_6m"] = ret["ret_6m_cell"].map(parse_percent_cell)
    ret = ret[["ticker", "return_company", "return_category", "latest_trade_date", "ret_6m"]]

    soxx_section = extract_section(read_text(RETURN_PATH), "### 按分类分组的全公司明细", "## 按分类分组的公司明细")
    soxx_raw = parse_grouped_tables(soxx_section, "####")
    soxx = soxx_raw.rename(columns={"股票代号": "ticker", "公司名称": "stress_company"})
    for col in SOXX_BENCHMARKS:
        if col in soxx.columns:
            soxx[col] = soxx[col].map(parse_percent_cell)
    soxx = soxx[["ticker"] + list(SOXX_BENCHMARKS.keys())]

    liq_raw = parse_single_table_after_heading(read_text(LIQUIDITY_PATH), "## 全公司排序表")
    liq = liq_raw.rename(columns={"股票代号": "ticker", "特征分": "liquidity_score"})
    liq["liquidity_score"] = liq["liquidity_score"].map(parse_number)
    liq = liq[["ticker", "liquidity_score"]]

    fin_section = extract_section(read_text(FINANCIAL_PATH), "## 按项目分类分组的公司明细表")
    fin_raw = parse_grouped_tables(fin_section, "###")
    fin = fin_raw.rename(
        columns={
            "股票代号": "ticker",
            "Call IV": "call_iv_cell",
            "Put IV": "put_iv_cell",
            "currency": "currency",
            "financial_currency": "financial_currency",
            "listing_type": "listing_type",
            "估值校验": "valuation_check",
        }
    )
    fin["call_iv"] = fin["call_iv_cell"].map(parse_percent_cell)
    fin["put_iv"] = fin["put_iv_cell"].map(parse_percent_cell)
    fin["near_iv"] = fin[["call_iv", "put_iv"]].mean(axis=1, skipna=True)
    fin = fin[["ticker", "call_iv", "put_iv", "near_iv", "currency", "financial_currency", "listing_type", "valuation_check"]]

    merged = (
        score.merge(ret, on="ticker", how="left")
        .merge(soxx, on="ticker", how="left")
        .merge(liq, on="ticker", how="left")
        .merge(fin, on="ticker", how="left")
    )
    merged = merged.set_index("ticker", drop=False)

    eval_df = merged[merged["ret_6m"].notna()].copy()

    metadata = {
        "score_count": len(score),
        "return_count": int(ret["ret_6m"].notna().sum()),
        "intersection_count": len(eval_df),
        "missing_returns": sorted(merged.loc[merged["ret_6m"].isna(), "ticker"].tolist()),
        "returns_no_score": sorted(set(ret["ticker"]) - set(score["ticker"])),
    }
    return eval_df, metadata


def build_report(df: pd.DataFrame, metadata: dict[str, object], moved_files: list[Path]) -> str:
    base_corr = correlations(df)
    tb_stats = top_bottom_stats(df)
    tb30 = tb_stats[-1]
    qrows = quintile_rows(df)
    constituents = top_bottom_constituents(df)

    risk_idx = group_indices_for_risk(df)
    risk_rows = [stress_metrics(df, label, idx) for label, idx in risk_idx.items()]
    iv_rows = iv_group_rows(df, risk_idx)
    top30_label = f"{FEATURE_ID} Top30"
    bottom30_label = f"{FEATURE_ID} Bottom30"
    risk_lookup = {row[0]: row for row in risk_rows}
    iv_lookup = {row[0]: row for row in iv_rows}

    neutral = category_neutral_scores(df)
    pct_corr = correlations(neutral, score_col="category_percentile")
    residual_corr = {
        "Pearson": corr_pearson(neutral["score_residual"], neutral["ret_residual"]),
        "Spearman": corr_spearman(neutral["score_residual"], neutral["ret_residual"]),
        "Kendall": corr_kendall_tau_b(neutral["score_residual"], neutral["ret_residual"]),
    }
    neutral_tb = top_bottom_stats(neutral.rename(columns={"category_percentile": "neutral_score"}), score_col="neutral_score")

    category_rows = []
    for category, group in df.groupby("category", sort=False):
        c = correlations(group)
        high_ret = group.sort_values("ret_6m", ascending=False).iloc[0]
        high_score = sorted_by_score(group).iloc[0]
        category_rows.append(
            [
                category,
                len(group),
                fmt_num(c["Pearson"]),
                fmt_num(c["Spearman"]),
                fmt_pct(group["ret_6m"].mean()),
                f"{high_ret['ticker']} {fmt_pct(high_ret['ret_6m'])}",
                f"{high_score['ticker']} {fmt_score(high_score['score'])} / {fmt_pct(high_score['ret_6m'])}",
            ]
        )
    category_rows = sorted(category_rows, key=lambda row: row[0])

    low_liq_mask = df["liquidity_score"].fillna(-math.inf) <= 5.0
    adr_bad_mask = (
        df["listing_type"].fillna("").str.contains("ADR/ADS", case=False, regex=False)
        | (df["currency"].fillna("") != df["financial_currency"].fillna(""))
        | df["valuation_check"].fillna("").str.contains("currency_mismatch", case=False, regex=False)
    )
    q_low = df["ret_6m"].quantile(0.05)
    q_high = df["ret_6m"].quantile(0.95)
    extreme_mask = (df["ret_6m"] < q_low) | (df["ret_6m"] > q_high)

    robust_rows = [
        robustness_row("全样本基准", "无剔除", df, df),
        robustness_row("剔除低流动性", "F51交易流动性分 > 5.0", df, df[~low_liq_mask]),
        robustness_row("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", df, df[~adr_bad_mask]),
        robustness_row("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(q_low)} / {fmt_pct(q_high)}", df, df[~extreme_mask]),
        robustness_row("三项合并剔除", "同时满足上述三项", df, df[~low_liq_mask & ~adr_bad_mask & ~extreme_mask]),
    ]

    high_return = df.sort_values("ret_6m", ascending=False).head(15)
    low_return = df.sort_values("ret_6m", ascending=True).head(10)
    high_score = sorted_by_score(df).head(15)
    low_score = sorted_by_score(df).tail(15).sort_values("rank")

    stress_avg = df[list(SOXX_BENCHMARKS.keys())].mean(axis=1, skipna=True)
    df = df.copy()
    df["stress_avg"] = stress_avg

    def diag_return_rows(group: pd.DataFrame) -> list[list[object]]:
        rows = []
        for _, row in group.iterrows():
            rows.append(
                [
                    row["ticker"],
                    row["company"],
                    row["category"],
                    fmt_pct(row["ret_6m"]),
                    fmt_score(row["score"]),
                    int(row["rank"]),
                    row["confidence"],
                ]
            )
        return rows

    def diag_score_rows(group: pd.DataFrame) -> list[list[object]]:
        rows = []
        for _, row in group.iterrows():
            t = row["ticker"]
            rows.append(
                [
                    int(row["rank"]),
                    t,
                    row["company"],
                    row["category"],
                    fmt_score(row["score"]),
                    fmt_pct(row["ret_6m"]),
                    fmt_pct(df.loc[t, "stress_avg"]),
                    fmt_pct(df.loc[t, "near_iv"]),
                ]
            )
        return rows

    category_dist_rows = []
    for category, group in df.groupby("category", sort=False):
        category_dist_rows.append(
            [
                category,
                len(group),
                fmt_score(group["score"].mean()),
                fmt_pct(group["ret_6m"].mean()),
                fmt_pct(group["ret_6m"].median()),
            ]
        )
    category_dist_rows = sorted(category_dist_rows, key=lambda row: row[0])

    neutral_corr_rows = [
        [
            "原始全样本",
            len(df),
            fmt_num(base_corr["Pearson"]),
            fmt_num(base_corr["Spearman"]),
            fmt_num(base_corr["Kendall"]),
            f"直接用{FEATURE_ID}分数排序",
        ],
        [
            "分类内百分位合并",
            len(df),
            fmt_num(pct_corr["Pearson"]),
            fmt_num(pct_corr["Spearman"]),
            fmt_num(pct_corr["Kendall"]),
            f"每个分类内先按{FEATURE_ID}排序，再转成0-1百分位后合并",
        ],
        [
            "分类去均值残差",
            len(df),
            fmt_num(residual_corr["Pearson"]),
            fmt_num(residual_corr["Spearman"]),
            fmt_num(residual_corr["Kendall"]),
            f"{FEATURE_ID}和收益分别减去分类均值后相关",
        ],
    ]

    neutral_tb_rows = [
        [
            f"中性Top{s['n']}/Bottom{s['n']}",
            fmt_pct(s["top_mean"]),
            fmt_pct(s["top_hit"]),
            fmt_pct(s["bottom_mean"]),
            fmt_pct(s["bottom_hit"]),
            fmt_pct(s["diff"]),
        ]
        for s in neutral_tb
    ]

    tb_rows = [
        [
            f"Top{s['n']}/Bottom{s['n']}",
            fmt_pct(s["top_mean"]),
            fmt_pct(s["top_hit"]),
            fmt_pct(s["bottom_mean"]),
            fmt_pct(s["bottom_hit"]),
            fmt_pct(s["diff"]),
        ]
        for s in tb_stats
    ]

    moved_desc = "无"
    if moved_files:
        moved_desc = "；".join(str(path.relative_to(ROOT)) for path in moved_files)

    top_tickers = ", ".join(sorted_by_score(df).head(10)["ticker"].tolist())
    sixm_leaders = ", ".join(df.sort_values("ret_6m", ascending=False).head(10)["ticker"].tolist())
    combined_subset = df[~low_liq_mask & ~adr_bad_mask & ~extreme_mask]
    combined_corr = correlations(combined_subset)
    combined_tb = top_bottom_stats(combined_subset, sizes=(30,))[0]

    report: list[str] = []
    report.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 {WINDOW_NAME}涨跌 {RUN_DATE}")
    report.append("")
    report.append("## 运行元信息")
    report.append(f"- 评估对象：`{FEATURE_SUBJECT}`。")
    report.append(f"- 评分输入：`{SCORE_PATH.relative_to(ROOT)}`，评分日期 {RUN_DATE}，覆盖 {metadata['score_count']} 家。")
    report.append("- 收益输入：`日度资料/区间涨跌/公司股价区间涨跌幅_2026-05-27.md`，生成时间 2026-05-27 20:17:54 -0700（本机时区），价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。")
    report.append("- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。")
    report.append("- 稳健性辅助输入：`特征量化/量化评分/F51_交易流动性_量化评分_2026-06-04.md`；`日度资料/每日金融数据/每日金融数据_2026-06-03.md`，金融数据生成时间 2026-06-03 13:41:46 PDT-0700。")
    report.append(f"- 有效评估样本：评分与6个月涨跌交集 {metadata['intersection_count']} 家；{FEATURE_ID}评分有但6个月涨跌缺失 {len(metadata['missing_returns'])} 家。")
    report.append("- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。")
    report.append("- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动率或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为下跌窗口代理，并用2026-06-03近ATM Call/Put IV均值补充当前波动代理。")
    report.append("- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。")
    report.append(f"- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 {FEATURE_ID} 正式输出；本次移动旧版文件：{moved_desc}。本次未读取旧版 {FEATURE_ID} 特征评估作为结论依据。")
    report.append(f"- 时间限制：{FEATURE_ID}评分日期为2026-06-04，收益窗口截至2026-05-27；本报告是当前评分对既有6个月股价表现的解释性评估，不是严格前瞻回测。")
    report.append("")
    report.append("## 结论摘要")
    report.append(f"- 排序有效性：{corr_direction(base_corr['Spearman'])}。全样本 Pearson {fmt_num(base_corr['Pearson'])}, Spearman {fmt_num(base_corr['Spearman'])}, Kendall {fmt_num(base_corr['Kendall'])}；重点指标 Spearman {fmt_num(base_corr['Spearman'])}。")
    report.append(f"- Top/Bottom能力：{top_bottom_judgement(tb30['diff'])}。Top10、Top20、Top30 平均收益分别为 {fmt_pct(tb_stats[0]['top_mean'])}、{fmt_pct(tb_stats[1]['top_mean'])}、{fmt_pct(tb_stats[2]['top_mean'])}；Top-Bottom收益差分别为 {fmt_pct(tb_stats[0]['diff'])}、{fmt_pct(tb_stats[1]['diff'])}、{fmt_pct(tb_stats[2]['diff'])}。")
    report.append(f"- 风险解释力：Top30 压力窗口均值 {risk_lookup[top30_label][6]}，Bottom30 为 {risk_lookup[bottom30_label][6]}；Top30 平均最差窗口 {risk_lookup[top30_label][7]}，Bottom30 为 {risk_lookup[bottom30_label][7]}；Top30 近ATM IV均值 {iv_lookup[top30_label][5]}，Bottom30 为 {iv_lookup[bottom30_label][5]}。")
    report.append(f"- 分类中性：分类内百分位合并 Spearman {fmt_num(pct_corr['Spearman'])}，分类去均值残差 Spearman {fmt_num(residual_corr['Spearman'])}；若中性化后仍接近零或为负，说明结果不只是押中某个分类目录。")
    report.append(f"- 稳健性：三项合并剔除后样本 {len(combined_subset)} 家，Spearman {fmt_num(combined_corr['Spearman'])}，Top30-Bottom30 {fmt_pct(combined_tb['diff'])}。")
    report.append(f"- 解释：{FEATURE_ID} 衡量订单被取消、延期、重定价、客户融资受阻、政策/许可打断或无法转收入的风险是否可控，高分代表订单下修风险低。高分端主要是 {top_tickers}；但本窗口 6 个月涨幅头部是 {sixm_leaders}。因此本评估要同时区分“下修风险可控”与“股价弹性”：若高分组合收益不强，但压力窗口、最差窗口或 IV 更稳，说明该特征更偏风险质量；若收益和风险代理同时不占优，则不能单独作为6个月收益排序因子。")
    report.append("")
    report.append("## 覆盖检查")
    report.append(
        md_table(
            ["项目", "数量", "说明"],
            [
                [f"{FEATURE_ID}评分覆盖", metadata["score_count"], f"来自{RUN_DATE}评分文件"],
                [f"{WINDOW_NAME}涨跌覆盖", metadata["return_count"], "来自2026-05-27区间涨跌文件"],
                ["交集样本", metadata["intersection_count"], "用于本次所有主指标"],
                ["评分有但6个月涨跌缺失", len(metadata["missing_returns"]), list_tickers(pd.Series(metadata["missing_returns"]))],
                ["涨跌有但评分缺失", len(metadata["returns_no_score"]), list_tickers(pd.Series(metadata["returns_no_score"]))],
            ],
        )
    )
    report.append("")
    report.append("### 交集样本分类分布")
    report.append(md_table(["分类目录", "样本数", f"{FEATURE_ID}均分", "6个月平均收益", "6个月中位收益"], category_dist_rows))
    report.append("")
    report.append("## 排序有效性")
    report.append(
        md_table(
            ["指标", "数值", "解释"],
            [
                ["Pearson", fmt_num(base_corr["Pearson"]), "线性相关；受极端涨跌影响较大"],
                ["Spearman", fmt_num(base_corr["Spearman"]), "排序相关；这是本任务最重要指标"],
                ["Kendall tau-b", fmt_num(base_corr["Kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
            ],
        )
    )
    report.append("")
    report.append("### 分数分组收益")
    report.append(md_table(["分组", "公司数", f"{FEATURE_ID}均分", "6个月平均收益", "6个月中位收益", "命中率"], qrows))
    report.append("")
    report.append("## Top/Bottom能力")
    report.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], tb_rows))
    report.append("")
    report.append("### Top10与Bottom10构成")
    report.append(md_table(["组别", "股票代号", "公司名称", "分类目录", f"{FEATURE_ID}分", f"{FEATURE_ID}排名", "6个月收益", f"{FEATURE_ID}置信度"], constituents))
    report.append("")
    report.append("## 风险解释力")
    report.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为下跌日/回撤代理，并使用2026-06-03近ATM IV作为波动代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供，故不写成严格波动率结论。")
    report.append(md_table(["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"], risk_rows))
    report.append("")
    report.append("### 当前IV代理")
    report.append(md_table(["分组", "公司数", "IV覆盖", "Call IV均值", "Put IV均值", "近ATM IV均值", "近ATM IV中位数"], iv_rows))
    report.append("")
    report.append(f"结论：高分组是否更稳，主要看 Top30 与 Bottom30 的压力窗口均值、平均最差窗口和近ATM IV。{FEATURE_ID} 的经济含义是风险可控性，不等同于更高收益弹性；因此风险代理若改善但收益排序弱，应把它用于下修风险约束，而不是单独排序。")
    report.append("")
    report.append("## 分类中性结果")
    report.append(md_table(["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"], neutral_corr_rows))
    report.append("")
    report.append("### 分类中性Top/Bottom")
    report.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], neutral_tb_rows))
    report.append("")
    report.append("### 10个分类目录内相关性")
    report.append(md_table(["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", f"类内最高{FEATURE_ID}公司"], category_rows))
    report.append("")
    report.append("分类内结果用于检验是否只是押中某个行业。若同一分类内 Spearman 多数为负或分散，说明该特征在本窗口更像质量/风险约束，而不是短期收益弹性排序。")
    report.append("")
    report.append("## 稳健性检验")
    report.append(md_table(["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"], robust_rows))
    report.append("")
    report.append(f"稳健性结论：如果三项合并剔除后 Spearman 和 Top30-Bottom30 仍不能稳定为正，则 {FEATURE_ID} 暂不适合直接作为6个月收益排序因子；若风险窗口和 IV 仍改善，则更适合作为订单质量与下修风险的过滤变量。")
    report.append("")
    report.append("### 剔除清单")
    report.append(
        md_table(
            ["剔除项", "数量", "公司"],
            [
                ["低流动性", int(low_liq_mask.sum()), list_tickers(df.loc[low_liq_mask, "ticker"].sort_values())],
                ["ADR/币种异常", int(adr_bad_mask.sum()), list_tickers(df.loc[adr_bad_mask, "ticker"].sort_values())],
                ["极端涨跌双尾5%", int(extreme_mask.sum()), list_tickers(df.loc[extreme_mask, "ticker"].sort_values())],
            ],
        )
    )
    report.append("")
    report.append("## 诊断：收益由哪些公司主导")
    report.append("### 6个月涨幅前15")
    report.append(md_table(["股票代号", "公司名称", "分类目录", "6个月收益", f"{FEATURE_ID}分", f"{FEATURE_ID}排名", f"{FEATURE_ID}置信度"], diag_return_rows(high_return)))
    report.append("")
    report.append("### 6个月跌幅前10")
    report.append(md_table(["股票代号", "公司名称", "分类目录", "6个月收益", f"{FEATURE_ID}分", f"{FEATURE_ID}排名", f"{FEATURE_ID}置信度"], diag_return_rows(low_return)))
    report.append("")
    report.append(f"### {FEATURE_ID}高分前15")
    report.append(md_table(["排名", "股票代号", "公司名称", "分类目录", f"{FEATURE_ID}分", "6个月收益", "压力窗口均值", "近ATM IV"], diag_score_rows(high_score)))
    report.append("")
    report.append(f"### {FEATURE_ID}低分前15")
    report.append(md_table(["排名", "股票代号", "公司名称", "分类目录", f"{FEATURE_ID}分", "6个月收益", "压力窗口均值", "近ATM IV"], diag_score_rows(low_score)))
    report.append("")
    report.append("## 使用建议")
    report.append(f"- 不把 {FEATURE_ID} 单独用作6个月收益排序，除非后续多窗口或前瞻回测显示 Spearman 稳定转正。")
    report.append(f"- 更合理的用途是作为订单质量和下修风险约束：在高弹性因子筛选后，剔除客户融资、非约束订单、许可政策或交付瓶颈导致的下修风险不可控公司。")
    report.append("- 若要升级评估，需要补入逐日价格序列，直接计算6个月最大回撤、下跌日 beta、日度波动率和压力窗口相对收益，而不是只使用当前区间汇总表。")
    report.append("")

    return "\n".join(report)


def backup_existing_outputs() -> list[Path]:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    moved: list[Path] = []
    pattern = f"{FEATURE_SUBJECT}_特征评估_{WINDOW_NAME}涨跌_*.md"
    existing = [path for path in OUTPUT_DIR.glob(pattern) if path.is_file() and path.resolve() != OUTPUT_PATH.resolve()]
    if OUTPUT_PATH.exists():
        existing.append(OUTPUT_PATH)
    if not existing:
        return moved

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target_dir = BACKUP_DIR / f"{FEATURE_SUBJECT}_{WINDOW_NAME}涨跌_写入前备份_{stamp}"
    target_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(set(existing)):
        target = target_dir / path.name
        shutil.move(str(path), str(target))
        moved.append(target)
    return moved


def main() -> None:
    df, metadata = prepare_data()
    moved = backup_existing_outputs()
    report = build_report(df, metadata, moved)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(f"wrote={OUTPUT_PATH}")
    print(f"score_count={metadata['score_count']} return_count={metadata['return_count']} intersection={metadata['intersection_count']}")
    base = correlations(df)
    print(f"pearson={base['Pearson']:.6f} spearman={base['Spearman']:.6f} kendall={base['Kendall']:.6f}")
    print(f"moved={len(moved)}")


if __name__ == "__main__":
    main()
