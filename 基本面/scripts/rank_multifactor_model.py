from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from single_factor_test import (
    DATA_DIR,
    METRICS_FILE,
    OUT_PREFIX,
    PRICE_FILE,
    TARGET_COLS,
    fmt_corr,
    fmt_pct,
    fmt_return,
    grouped_return_stats,
    kendall_tau_b,
    load_table,
    markdown_table,
    normalize_ticker,
    parse_number,
    pearson_corr,
    spearman_corr,
    top_hit_rate,
)


SINGLE_FILE = OUT_PREFIX.with_name(f"{OUT_PREFIX.name}_full_results.csv")
OUT_FILE = DATA_DIR / "百分位Rank多因子模型_14_30_90_180_365天_2026-05-11.md"

POS_JUDGES = {"正向较强", "正向有效"}
NEG_JUDGES = {"反向较强", "反向有效"}


def pct_rank_score(series: pd.Series, direction: int) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    if values.notna().sum() == 0:
        return pd.Series(np.nan, index=series.index)

    filled = values.fillna(values.median())
    if direction == 1:
        return filled.rank(method="average", ascending=True, pct=True) * 100.0
    return filled.rank(method="average", ascending=False, pct=True) * 100.0


def judge_model(spearman: float, top20_hit: float, top_bottom: float) -> str:
    if not np.isfinite(spearman) or not np.isfinite(top_bottom):
        return "无效"
    if spearman >= 0.45 and top20_hit >= 0.40 and top_bottom > 0:
        return "强有效，能识别高涨幅"
    if spearman >= 0.30 and top20_hit >= 0.30 and top_bottom > 0:
        return "有效，排序和识别均较好"
    if spearman >= 0.15 and top_bottom > 0:
        return "边际有效"
    if spearman <= -0.15 or top_bottom < 0:
        return "方向相反或失效"
    return "弱相关/失效"


def fmt_score(value: float) -> str:
    if not np.isfinite(value):
        return ""
    return f"{value:.2f}"


def build_report() -> tuple[Path, pd.DataFrame]:
    single = pd.read_csv(SINGLE_FILE, encoding="utf-8-sig")
    numeric_cols = [
        "Pearson",
        "Spearman",
        "Kendall",
        "Top10命中率",
        "Top20命中率",
        "Top30命中率",
        "Top20平均涨幅",
        "Bottom20平均涨幅",
        "Top-Bottom差",
        "综合得分",
        "排名",
    ]
    for col in numeric_cols:
        if col in single.columns:
            single[col] = pd.to_numeric(single[col], errors="coerce")

    price = load_table(PRICE_FILE, required_cols={"股票代码", *TARGET_COLS}, min_cols=8).copy()
    metrics = load_table(METRICS_FILE, required_cols={"股票代号"}, min_cols=20).copy()
    price["_ticker"] = price["股票代码"].map(normalize_ticker)
    metrics["_ticker"] = metrics["股票代号"].map(normalize_ticker)

    for col in TARGET_COLS:
        price[col] = price[col].map(parse_number)

    factor_names = sorted(set(single["指标"]))
    for col in factor_names:
        if col in metrics.columns:
            metrics[col] = metrics[col].map(parse_number)

    factor_cols = [col for col in factor_names if col in metrics.columns]
    merged = metrics[["_ticker", "股票代号", "公司名", *factor_cols]].merge(
        price[["_ticker", "股票代码", "公司", *TARGET_COLS]],
        on="_ticker",
        how="inner",
    )
    if merged.empty:
        raise RuntimeError("No matched tickers between metrics and price tables.")

    summary_rows: list[dict[str, object]] = []
    window_tables: dict[str, list[dict[str, object]]] = {}
    candidate_lines: list[str] = []

    for window in TARGET_COLS:
        subset = single[single["窗口"] == window].copy()
        candidates: list[tuple[str, int]] = []

        for _, row in subset.sort_values("排名").iterrows():
            factor = row["指标"]
            if factor not in merged.columns:
                continue

            judge = str(row["判断"])
            if judge in POS_JUDGES:
                direction = 1
            elif judge in NEG_JUDGES:
                direction = -1
            else:
                continue

            spearman = row.get("Spearman", np.nan)
            top_bottom = row.get("Top-Bottom差", np.nan)
            if direction == 1 and not (spearman > 0 and top_bottom > 0):
                continue
            if direction == -1 and not (spearman < 0 and top_bottom < 0):
                continue

            candidates.append((factor, direction))

        model = merged[["_ticker", "股票代码", "公司", "公司名", window]].dropna(subset=[window]).copy()
        score_cols: list[str] = []
        for factor, direction in candidates:
            score_col = f"__score__{factor}"
            model[score_col] = pct_rank_score(merged.loc[model.index, factor], direction)
            score_cols.append(score_col)

        model["模型分数"] = model[score_cols].mean(axis=1) if score_cols else np.nan

        y = model[window].to_numpy(dtype=float)
        x = model["模型分数"].to_numpy(dtype=float)
        pearson = pearson_corr(x, y)
        spearman = spearman_corr(x, y)
        kendall = kendall_tau_b(x, y)

        scored = model.rename(columns={"模型分数": "_score"})
        top10 = top_hit_rate(scored, "_score", window, 10)
        top20 = top_hit_rate(scored, "_score", window, 20)
        top30 = top_hit_rate(scored, "_score", window, 30)
        top20_avg, bottom20_avg, tb_diff = grouped_return_stats(scored, "_score", window, 20)

        pos_count = sum(1 for _, direction in candidates if direction == 1)
        neg_count = sum(1 for _, direction in candidates if direction == -1)
        summary_rows.append(
            {
                "窗口": window,
                "方法说明": f"方向调整后百分位Rank等权均值（正向{pos_count}，反向{neg_count}）",
                "候选指标数量": len(candidates),
                "Pearson": fmt_corr(pearson),
                "Spearman": fmt_corr(spearman),
                "Kendall": fmt_corr(kendall),
                "Top20命中率": fmt_pct(top20),
                "Top-Bottom差": fmt_return(tb_diff),
                "判断": judge_model(spearman, top20, tb_diff),
                "_top10": top10,
                "_top20": top20,
                "_top30": top30,
                "_top20avg": top20_avg,
                "_bottom20avg": bottom20_avg,
                "_tbdiff": tb_diff,
                "_pearson": pearson,
                "_spearman": spearman,
                "_kendall": kendall,
            }
        )

        candidate_text = "、".join(("+" if direction == 1 else "-") + factor for factor, direction in candidates)
        candidate_lines.append(f"- {window}：{len(candidates)}个（+为正序，-为倒序）：{candidate_text}")

        ranked = model.sort_values(["模型分数", "_ticker"], ascending=[False, True]).reset_index(drop=True)
        rows: list[dict[str, object]] = []
        for rank, row in ranked.iterrows():
            rows.append(
                {
                    "排名": rank + 1,
                    "公司": row.get("公司") or row.get("公司名") or "",
                    "代码": row["股票代码"],
                    f"{window}涨跌幅": fmt_return(row[window]),
                    "模型分数": fmt_score(row["模型分数"]),
                }
            )
        window_tables[window] = rows

    summary_df = pd.DataFrame(summary_rows)
    best_sort = summary_df.sort_values("_spearman", ascending=False).iloc[0]
    best_identify = summary_df.sort_values("_top20", ascending=False).iloc[0]
    not_suitable = summary_df[(summary_df["_spearman"] < 0.15) | (summary_df["_tbdiff"] <= 0)]["窗口"].tolist()

    short_score = summary_df[summary_df["窗口"].isin(["14天", "30天"])]["_spearman"].mean()
    mid_score = summary_df[summary_df["窗口"].isin(["90天", "180天"])]["_spearman"].mean()
    long_score = summary_df[summary_df["窗口"].eq("365天")]["_spearman"].mean()
    if short_score >= mid_score and short_score >= long_score:
        horizon = "短线"
    elif mid_score >= long_score:
        horizon = "中期"
    else:
        horizon = "长期"

    lines: list[str] = []
    lines.append("# 百分位 Rank 多因子模型检验（14/30/90/180/365天）")
    lines.append("")
    lines.append("生成日期：2026-05-11。")
    lines.append("")
    lines.append("## 方法")
    lines.append("")
    lines.append(
        "每个窗口直接使用对应窗口的单因子检验结果，不重新做单因子。候选指标取单因子判断为“正向有效/正向较强”或“反向有效/反向较强”的指标；"
        "正向指标按原始分数做横截面百分位排名，反向指标按倒序百分位排名，所有候选指标等权求均值得到 0-100 的模型分数。"
        "该模型重点检验排序和选股能力，不用于拟合涨跌幅绝对数值。"
        "样本数沿用单因子检验口径：14/30/90/180天为170家公司，365天因有效365天涨跌幅缺失为168家公司。"
    )
    lines.append("")
    lines.append("## 五个窗口效果汇总")
    lines.append("")

    summary_display_cols = [
        "窗口",
        "方法说明",
        "候选指标数量",
        "Pearson",
        "Spearman",
        "Kendall",
        "Top20命中率",
        "Top-Bottom差",
        "判断",
    ]
    lines.append(
        markdown_table(
            [{col: row[col] for col in summary_display_cols} for row in summary_rows],
            summary_display_cols,
            ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 分组和命中率补充")
    lines.append("")

    supplement_cols = [
        "窗口",
        "Top10命中率",
        "Top20命中率",
        "Top30命中率",
        "Top20平均涨幅",
        "Bottom20平均涨幅",
        "Top-Bottom差",
    ]
    supplement_rows = []
    for row in summary_rows:
        supplement_rows.append(
            {
                "窗口": row["窗口"],
                "Top10命中率": fmt_pct(row["_top10"]),
                "Top20命中率": fmt_pct(row["_top20"]),
                "Top30命中率": fmt_pct(row["_top30"]),
                "Top20平均涨幅": fmt_return(row["_top20avg"]),
                "Bottom20平均涨幅": fmt_return(row["_bottom20avg"]),
                "Top-Bottom差": fmt_return(row["_tbdiff"]),
            }
        )
    lines.append(markdown_table(supplement_rows, supplement_cols, ["---", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### 候选指标")
    lines.append("")
    lines.extend(candidate_lines)
    lines.append("")
    lines.append("## 各窗口排序表")

    for window in TARGET_COLS:
        lines.append("")
        lines.append(f"### {window}")
        lines.append("")
        cols = ["排名", "公司", "代码", f"{window}涨跌幅", "模型分数"]
        lines.append(markdown_table(window_tables[window], cols, ["---:", "---", "---", "---:", "---:"]))

    invalid_text = "、".join(not_suitable) if not_suitable else "无明显不适合窗口"
    lines.append("")
    lines.append("## 总结")
    lines.append("")
    lines.append(
        f"这个多因子思路整体更适合{horizon}；排序能力最强的是{best_sort['窗口']}（Spearman {best_sort['_spearman']:.3f}），"
        f"高涨幅公司识别最好的是{best_identify['窗口']}（Top20命中率 {best_identify['_top20']:.1%}）。"
        f"不适合或需要谨慎使用的窗口：{invalid_text}。"
    )
    lines.append("")

    OUT_FILE.write_text("\n".join(lines), encoding="utf-8-sig")
    return OUT_FILE, summary_df[summary_display_cols]


def main() -> None:
    out_file, summary = build_report()
    print(f"output={out_file}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
