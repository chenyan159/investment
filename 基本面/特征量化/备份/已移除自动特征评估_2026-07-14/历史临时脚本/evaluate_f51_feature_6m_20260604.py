from __future__ import annotations

import importlib.util
import math
import shutil
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
BASE_SCRIPT = ROOT / "tmp" / "evaluate_F30_feature_2026_06_04.py"
FEATURE_ID = "F51"
FEATURE_NAME = "交易流动性"
FEATURE_STEM = f"{FEATURE_ID}_{FEATURE_NAME}"
WINDOW = "6个月"
REPORT_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_STEM}_量化评分_{REPORT_DATE}.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUT_DIR / "备份"
OUT_PATH = OUT_DIR / f"{FEATURE_STEM}_特征评估_{WINDOW}涨跌_{REPORT_DATE}.md"


def load_base_module():
    spec = importlib.util.spec_from_file_location("feature_eval_base_f30", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load base evaluator from {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.FEATURE_ID = FEATURE_ID
    module.FEATURE_NAME = FEATURE_NAME
    module.FEATURE_STEM = FEATURE_STEM
    module.WINDOW = WINDOW
    module.REPORT_DATE = REPORT_DATE
    module.SCORE_PATH = SCORE_PATH
    module.RETURN_PATH = RETURN_PATH
    module.F51_PATH = SCORE_PATH
    module.FIN_PATH = FIN_PATH
    module.OUT_DIR = OUT_DIR
    module.BACKUP_DIR = BACKUP_DIR
    module.OUT_PATH = OUT_PATH
    return module


base = load_base_module()


def tickers(values: list[str]) -> str:
    return ", ".join(values) if values else "无"


def fmt_sign(value: float) -> str:
    if value >= 0.15:
        return "正向"
    if value >= 0.05:
        return "弱正向"
    if value > -0.05:
        return "接近零"
    if value > -0.15:
        return "弱负向"
    return "明显负向"


def mean_pressure(row: pd.Series) -> float:
    return pd.Series([row["soxx1"], row["soxx2"], row["soxx3"]]).dropna().mean()


def backup_existing() -> list[str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    existing = [p for p in OUT_DIR.glob(f"{FEATURE_STEM}_特征评估_{WINDOW}涨跌_*.md") if p.is_file()]
    if not existing:
        return []
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_target = BACKUP_DIR / f"{FEATURE_STEM}_{WINDOW}涨跌_{REPORT_DATE}_写入前备份_{stamp}"
    backup_target.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    for path in existing:
        destination = backup_target / path.name
        shutil.move(str(path), str(destination))
        moved.append(str(destination.relative_to(ROOT)))
    return moved


def build_dataset() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    score = base.parse_score_file(SCORE_PATH)
    returns = base.parse_return_file(RETURN_PATH)
    soxx = base.parse_soxx_file(RETURN_PATH)
    financial = base.parse_financial_file(FIN_PATH)
    df = (
        score.merge(returns, on="ticker", how="left")
        .merge(soxx[["ticker", "soxx1", "soxx2", "soxx3", "soxx_note"]], on="ticker", how="left")
        .merge(
            financial[
                [
                    "ticker",
                    "call_iv",
                    "put_iv",
                    "near_atm_iv",
                    "currency",
                    "financial_currency",
                    "listing_type",
                    "adr_ratio",
                    "valuation_check",
                    "fin_note",
                ]
            ],
            on="ticker",
            how="left",
        )
    )
    df["liquidity_score"] = df["score"]
    return score, returns, soxx, financial, df


def make_report() -> tuple[str, dict[str, object]]:
    score, returns, _soxx, _financial, df = build_dataset()
    eval_df = df.dropna(subset=["score", "r_6m"]).copy()
    neutral_df = base.add_neutral_scores(eval_df)

    missing_returns = sorted(df.loc[df["r_6m"].isna(), "ticker"].tolist())
    return_missing_score = sorted(set(returns["ticker"]) - set(score["ticker"]))

    corr = base.corr_stats(eval_df)
    tb = {n: base.top_bottom_stats(eval_df, n) for n in (10, 20, 30)}
    qstats = base.quintile_stats(eval_df)
    pressure_stats, iv_stats = base.risk_group_stats(eval_df)
    neutral_raw = base.corr_stats(neutral_df, "score", "r_6m")
    neutral_pct = base.corr_stats(neutral_df, "cat_percentile", "r_6m")
    neutral_resid = base.corr_stats(neutral_df, "score_resid", "ret_resid")
    neutral_tb = {n: base.top_bottom_stats(neutral_df, n, "cat_percentile") for n in (10, 20, 30)}
    cat_corr = base.category_corrs(eval_df)
    robust, exclusions, low_tail, high_tail = base.robust_rows(eval_df)

    top_sorted = base.sorted_by_score(eval_df)
    bottom_sorted = base.sorted_by_score(eval_df, ascending=True)
    top10 = top_sorted.head(10)
    bottom10 = bottom_sorted.head(10)
    winners15 = eval_df.sort_values(["r_6m", "ticker"], ascending=[False, True]).head(15)
    losers15 = eval_df.sort_values(["r_6m", "ticker"], ascending=[True, True]).head(15)
    top20_score = top_sorted.head(20)
    bottom20_score = bottom_sorted.head(20)

    score["score_bucket"] = score["score"].map(base.score_bucket)
    bucket_counts = (
        score["score_bucket"]
        .value_counts()
        .reindex(["9.0-10.0", "8.0-8.9", "7.0-7.9", "5.0-6.9", "3.0-4.9", "1.0-2.9"], fill_value=0)
    )

    top30 = tb[30]["top"]
    bottom30 = tb[30]["bottom"]
    top30_low_return = top30.sort_values(["r_6m", "ticker"], ascending=[True, True]).head(8)
    bottom30_high_return = bottom30.sort_values(["r_6m", "ticker"], ascending=[False, True]).head(8)

    risk_top = pressure_stats[0]
    risk_bottom = pressure_stats[2]
    iv_top = iv_stats[0]
    iv_bottom = iv_stats[2]
    spearman_value = float(corr["spearman"])
    top30_diff = float(tb[30]["diff"])
    robust_final = robust[-1]
    moved = backup_existing()

    top_names = "、".join(top_sorted["ticker"].head(10).tolist())
    winner_names = "、".join(winners15["ticker"].head(10).tolist())
    bottom_winner_names = "、".join(
        winners15.loc[winners15["score"] <= eval_df["score"].median(), "ticker"].head(8).tolist()
    )
    if not bottom_winner_names:
        bottom_winner_names = "无明显低分赢家"

    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 {WINDOW}涨跌 {REPORT_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.extend(
        [
            f"- 评估对象：`{FEATURE_STEM}`。",
            f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 2026-06-04，覆盖 {len(score)} 家。",
            "- 收益输入：`日度资料/区间涨跌/公司股价区间涨跌幅_2026-05-27.md`，生成时间 2026-05-27 20:17:54 -0700（本机时区），价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。",
            "- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。",
            "- 金融数据辅助输入：`日度资料/每日金融数据/每日金融数据_2026-06-03.md`，生成时间 2026-06-03 13:41:46 PDT-0700；用于读取 listing_type、ADR/ADS、币种、估值校验和近 ATM IV。",
            f"- 有效评估样本：评分与6个月涨跌交集 {len(eval_df)} 家；F51评分有但6个月涨跌缺失 {len(missing_returns)} 家。",
            "- F51口径限制：原评分文件明确说明日度金融数据未提供逐家公司成交额、成交量、30日均成交额或买卖价差，因此本次评测对象是“交易流动性代理评分”，不是完整 ADV/换手率/价差流动性排序。",
            "- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。",
            "- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动率、完整最大回撤或逐日下跌日胜率；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度、跑赢 SOXX 比例和负收益窗口占比作为下跌窗口代理，并用2026-06-03近ATM IV补充当前波动代理。",
            "- 稳健性口径限制：因为 F51 本身就是交易流动性评分，“剔除低流动性”使用 F51<=5.0 的低分尾部作为自过滤敏感性检验，不是独立流动性数据验证；独立验证需要补充 ADV、成交额、换手和买卖价差。",
            "- 时间方向限制：F51评分日期为2026-06-04，6个月收益窗口截至2026-05-27；本报告是当前交易流动性代理评分与过去6个月价格表现的横截面对照，不是严格样本外预测回测。",
            "- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F51 正式输出；本次未读取旧版 F51 特征评估作为结论依据。",
        ]
    )
    if moved:
        lines.append(f"- 本次移动旧版文件：{'; '.join(moved)}。")
    else:
        lines.append("- 本次未发现根目录同类旧版正式输出残留。")

    lines.append("")
    lines.append("## 结论摘要")
    lines.extend(
        [
            f"- 排序有效性：{fmt_sign(spearman_value)}。全样本 Pearson {base.fmt_corr(corr['pearson'])}, Spearman {base.fmt_corr(corr['spearman'])}, Kendall {base.fmt_corr(corr['kendall'])}；重点指标 Spearman {base.fmt_corr(corr['spearman'])}，说明 F51 对本次过去6个月涨幅排序不是正向收益因子。",
            f"- Top/Bottom能力：收益排序不成立。Top10、Top20、Top30 平均收益分别为 {base.fmt_pct(tb[10]['top_mean'])}、{base.fmt_pct(tb[20]['top_mean'])}、{base.fmt_pct(tb[30]['top_mean'])}；Top-Bottom收益差分别为 {base.fmt_pct(tb[10]['diff'])}、{base.fmt_pct(tb[20]['diff'])}、{base.fmt_pct(tb[30]['diff'])}。若目标是抓6个月涨幅，低流动性/小市值尾部在本窗口反而贡献更高收益。",
            f"- 风险解释力：部分成立。Top30 压力窗口均值 {base.fmt_pct(risk_top['stress_mean'])}，Bottom30 为 {base.fmt_pct(risk_bottom['stress_mean'])}；Top30 平均最差窗口 {base.fmt_pct(risk_top['worst_mean'])}，Bottom30 为 {base.fmt_pct(risk_bottom['worst_mean'])}；Top30 近ATM IV均值 {base.fmt_pct(iv_top['near_iv'])}，Bottom30 为 {base.fmt_pct(iv_bottom['near_iv'])}。F51高分更像风险/可交易性过滤器，而不是收益弹性因子。",
            f"- 分类中性：负向仍保留。分类内百分位合并 Spearman {base.fmt_corr(neutral_pct['spearman'])}，分类去均值残差 Spearman {base.fmt_corr(neutral_resid['spearman'])}；说明结果不是单纯押中了某个分类目录，而是在不少分类内部也呈“低流动性代理分、高反弹收益”的结构。",
            f"- 稳健性：三项合并剔除后样本 {robust_final['n']} 家，Spearman {base.fmt_corr(robust_final['spearman'])}，Top30-Bottom30 {base.fmt_pct(robust_final['diff30'])}。剔除低流动性尾部、ADR/币种异常和极端涨跌后，负向收益关系通常收窄，但没有转成稳定正向。",
            f"- 解释：F51高分端集中在 {top_names} 等大市值、期权链覆盖较好、普通股/数据完整度较高的公司；本窗口涨幅头部为 {winner_names}，其中低分或中低分赢家包括 {bottom_winner_names}。过去6个月收益主要由小盘、低基数、存储/光互联/设备周期、融资或事件驱动反弹贡献；这些样本流动性代理分更低、IV更高、压力窗口更差。因此 F51 更适合做容量、成交摩擦和回撤风险约束，不适合单独追求6个月收益最大化。",
        ]
    )

    lines.append("")
    lines.append("## 覆盖检查")
    lines.append(
        base.md_table(
            ["项目", "数量", "说明"],
            [
                ["F51评分覆盖", len(score), "来自2026-06-04评分文件"],
                ["6个月涨跌覆盖", len(returns), "来自2026-05-27区间涨跌文件"],
                ["交集样本", len(eval_df), "用于本次所有主指标"],
                ["评分有但6个月涨跌缺失", len(missing_returns), tickers(missing_returns)],
                ["涨跌有但评分缺失", len(return_missing_score), tickers(return_missing_score)],
                ["分类目录不一致", int((eval_df["category"] != eval_df["return_category"]).sum()), "按评分文件分类为主，收益文件分类用于交叉校验"],
            ],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 交集样本分类分布")
    category_rows: list[list[object]] = []
    for category, group in eval_df.groupby("category", sort=True):
        category_rows.append(
            [
                category,
                len(group),
                base.fmt_float(group["score"].mean()),
                base.fmt_pct(group["r_6m"].mean()),
                base.fmt_pct(group["r_6m"].median()),
                base.fmt_pct(group["near_atm_iv"].mean(skipna=True)),
            ]
        )
    lines.append(
        base.md_table(
            ["分类目录", "样本数", "F51均分", "6个月平均收益", "6个月中位收益", "近ATM IV均值"],
            category_rows,
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## 排序有效性")
    lines.append(
        base.md_table(
            ["指标", "数值", "解释"],
            [
                ["Pearson", base.fmt_corr(corr["pearson"]), "线性相关；受AXTI、SNDK、AAOI、MXL等极端涨幅影响较大"],
                ["Spearman", base.fmt_corr(corr["spearman"]), "排序相关；这是本任务最重要指标"],
                ["Kendall tau-b", base.fmt_corr(corr["kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
            ],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 分数分组收益")
    lines.append(
        base.md_table(
            ["分组", "公司数", "F51均分", "6个月平均收益", "6个月中位收益", "命中率"],
            [
                [
                    item["group"],
                    item["n"],
                    base.fmt_float(item["score_mean"]),
                    base.fmt_pct(item["return_mean"]),
                    base.fmt_pct(item["return_median"]),
                    base.fmt_rate(item["hit"]),
                ]
                for item in qstats
            ],
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## Top/Bottom能力")
    lines.append(
        base.md_table(
            ["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"],
            [
                [
                    f"Top{n}/Bottom{n}",
                    base.fmt_pct(tb[n]["top_mean"]),
                    base.fmt_rate(tb[n]["top_hit"]),
                    base.fmt_pct(tb[n]["bottom_mean"]),
                    base.fmt_rate(tb[n]["bottom_hit"]),
                    base.fmt_pct(tb[n]["diff"]),
                ]
                for n in (10, 20, 30)
            ],
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("### Top10与Bottom10构成")
    top_bottom_rows: list[list[object]] = []
    for label, group in [("Top10", top10), ("Bottom10", bottom10)]:
        for _, row in group.iterrows():
            top_bottom_rows.append(
                [
                    label,
                    row["ticker"],
                    row["company"],
                    row["category"],
                    base.fmt_float(row["score"], 1),
                    int(row["score_rank"]),
                    base.fmt_pct(row["r_6m"]),
                    row["confidence"],
                ]
            )
    lines.append(
        base.md_table(
            ["组别", "股票代号", "公司名称", "分类目录", "F51分", "F51排名", "6个月收益", "置信度"],
            top_bottom_rows,
            ["---", "---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### Top30中的低收益样本与Bottom30中的高收益样本")
    contrast_rows: list[list[object]] = []
    for label, group in [("Top30低收益", top30_low_return), ("Bottom30高收益", bottom30_high_return)]:
        for _, row in group.iterrows():
            contrast_rows.append(
                [
                    label,
                    row["ticker"],
                    row["company"],
                    row["category"],
                    base.fmt_float(row["score"], 1),
                    int(row["score_rank"]),
                    base.fmt_pct(row["r_6m"]),
                    base.fmt_pct(mean_pressure(row)),
                    base.fmt_pct(row["near_atm_iv"]),
                ]
            )
    lines.append(
        base.md_table(
            ["组别", "股票代号", "公司名称", "分类目录", "F51分", "排名", "6个月收益", "压力窗口均值", "近ATM IV"],
            contrast_rows,
            ["---", "---", "---", "---", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为下跌日/回撤代理，并使用2026-06-03近ATM IV作为当前波动代理。严格日度波动率、最大回撤和逐日下跌日表现需要逐日价格序列，本次输入文件没有提供。")
    lines.append(
        base.md_table(
            ["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"],
            [
                [
                    row["group"],
                    row["n"],
                    row["obs"],
                    base.fmt_pct(row["soxx1_mean"]),
                    base.fmt_pct(row["soxx2_mean"]),
                    base.fmt_pct(row["soxx3_mean"]),
                    base.fmt_pct(row["stress_mean"]),
                    base.fmt_pct(row["worst_mean"]),
                    base.fmt_pct(row["window_std"]),
                    base.fmt_rate(row["beat_soxx"]),
                    base.fmt_rate(row["negative_rate"]),
                ]
                for row in pressure_stats
            ],
            ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("### 当前IV代理")
    lines.append(
        base.md_table(
            ["分组", "公司数", "IV覆盖", "Call IV均值", "Put IV均值", "近ATM IV均值", "近ATM IV中位数"],
            [
                [
                    row["group"],
                    row["n"],
                    row["iv_n"],
                    base.fmt_pct(row["call_iv"]),
                    base.fmt_pct(row["put_iv"]),
                    base.fmt_pct(row["near_iv"]),
                    base.fmt_pct(row["near_iv_median"]),
                ]
                for row in iv_stats
            ],
            ["---", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append(
        f"结论：Top30 压力窗口均值比 Bottom30 {'更浅' if risk_top['stress_mean'] > risk_bottom['stress_mean'] else '更深'}，"
        f"近ATM IV均值比 Bottom30 {'更低' if iv_top['near_iv'] < iv_bottom['near_iv'] else '更高'}。"
        "这支持 F51 作为交易可执行性、组合容量和风险过滤变量，但不支持把它当成进攻型收益排序因子。"
    )

    lines.append("")
    lines.append("## 分类中性结果")
    lines.append(
        base.md_table(
            ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
            [
                ["原始全样本", neutral_raw["n"], base.fmt_corr(neutral_raw["pearson"]), base.fmt_corr(neutral_raw["spearman"]), base.fmt_corr(neutral_raw["kendall"]), "直接用F51分数排序"],
                ["分类内百分位合并", neutral_pct["n"], base.fmt_corr(neutral_pct["pearson"]), base.fmt_corr(neutral_pct["spearman"]), base.fmt_corr(neutral_pct["kendall"]), "每个分类内先按F51排序，再转成0-1百分位后合并"],
                ["分类去均值残差", neutral_resid["n"], base.fmt_corr(neutral_resid["pearson"]), base.fmt_corr(neutral_resid["spearman"]), base.fmt_corr(neutral_resid["kendall"]), "F51和收益分别减去分类均值后相关"],
            ],
            ["---", "---:", "---:", "---:", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(
        base.md_table(
            ["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"],
            [
                [
                    f"中性Top{n}/Bottom{n}",
                    base.fmt_pct(neutral_tb[n]["top_mean"]),
                    base.fmt_rate(neutral_tb[n]["top_hit"]),
                    base.fmt_pct(neutral_tb[n]["bottom_mean"]),
                    base.fmt_rate(neutral_tb[n]["bottom_hit"]),
                    base.fmt_pct(neutral_tb[n]["diff"]),
                ]
                for n in (10, 20, 30)
            ],
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("说明：分类中性结果用于排除“只是押中了某个行业”的解释。本次分类内百分位和分类残差仍为负，说明 F51 与6个月涨幅的反向关系不是纯粹来自云算力、大盘半导体或电力目录配置，而是多个目录内部都有低流动性高弹性反弹。")

    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(
        base.md_table(
            ["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F51公司"],
            [
                [
                    row["category"],
                    row["n"],
                    base.fmt_corr(row["pearson"]),
                    base.fmt_corr(row["spearman"]),
                    base.fmt_pct(row["mean_ret"]),
                    f"{row['top_return']['ticker']} {base.fmt_pct(row['top_return']['r_6m'])}",
                    f"{row['top_score']['ticker']} {base.fmt_float(row['top_score']['score'], 1)} / {base.fmt_pct(row['top_score']['r_6m'])}",
                ]
                for row in cat_corr
            ],
            ["---", "---:", "---:", "---:", "---:", "---", "---"],
        )
    )

    lines.append("")
    lines.append("## 稳健性检验")
    lines.append(
        base.md_table(
            ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"],
            [
                [
                    row["name"],
                    row["rule"],
                    row["n"],
                    row["excluded"],
                    base.fmt_corr(row["pearson"]),
                    base.fmt_corr(row["spearman"]),
                    base.fmt_corr(row["kendall"]),
                    base.fmt_pct(row["top30"]),
                    base.fmt_pct(row["bottom30"]),
                    base.fmt_pct(row["diff30"]),
                ]
                for row in robust
            ],
            ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append(
        "稳健性结论：低流动性剔除在本报告里是 F51 自过滤，即移除 F51<=5.0 的尾部高弹性/高噪声样本。若剔除后 Spearman 与 Top30-Bottom30 仍没有稳定转正，说明 F51 本身不应被解释为收益增强因子。ADR/币种异常和极端涨跌剔除后负向幅度通常收窄，说明一部分反向收益来自高风险尾部，但不是唯一来源。"
    )

    lines.append("")
    lines.append("### 剔除清单")
    lines.append(
        base.md_table(
            ["剔除项", "数量", "公司"],
            [[name, len(values), tickers(values)] for name, values in exclusions.items()],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    lines.append(
        base.md_table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F51分", "F51排名", "F51置信度", "近ATM IV"],
            [
                [
                    row["ticker"],
                    row["company"],
                    row["category"],
                    base.fmt_pct(row["r_6m"]),
                    base.fmt_float(row["score"], 1),
                    int(row["score_rank"]),
                    row["confidence"],
                    base.fmt_pct(row["near_atm_iv"]),
                ]
                for _, row in winners15.iterrows()
            ],
            ["---", "---", "---", "---:", "---:", "---:", "---", "---:"],
        )
    )

    lines.append("")
    lines.append("### 6个月跌幅前15")
    lines.append(
        base.md_table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F51分", "F51排名", "F51置信度", "近ATM IV"],
            [
                [
                    row["ticker"],
                    row["company"],
                    row["category"],
                    base.fmt_pct(row["r_6m"]),
                    base.fmt_float(row["score"], 1),
                    int(row["score_rank"]),
                    row["confidence"],
                    base.fmt_pct(row["near_atm_iv"]),
                ]
                for _, row in losers15.iterrows()
            ],
            ["---", "---", "---", "---:", "---:", "---:", "---", "---:"],
        )
    )

    lines.append("")
    lines.append("### F51高分前20")
    lines.append(
        base.md_table(
            ["排名", "股票代号", "公司名称", "分类目录", "F51分", "6个月收益", "压力窗口均值", "近ATM IV"],
            [
                [
                    int(row["score_rank"]),
                    row["ticker"],
                    row["company"],
                    row["category"],
                    base.fmt_float(row["score"], 1),
                    base.fmt_pct(row["r_6m"]),
                    base.fmt_pct(mean_pressure(row)),
                    base.fmt_pct(row["near_atm_iv"]),
                ]
                for _, row in top20_score.iterrows()
            ],
            ["---:", "---", "---", "---", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("### F51低分前20")
    lines.append(
        base.md_table(
            ["排名", "股票代号", "公司名称", "分类目录", "F51分", "6个月收益", "压力窗口均值", "近ATM IV"],
            [
                [
                    int(row["score_rank"]),
                    row["ticker"],
                    row["company"],
                    row["category"],
                    base.fmt_float(row["score"], 1),
                    base.fmt_pct(row["r_6m"]),
                    base.fmt_pct(mean_pressure(row)),
                    base.fmt_pct(row["near_atm_iv"]),
                ]
                for _, row in bottom20_score.iterrows()
            ],
            ["---:", "---", "---", "---", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## 分数分布与解释")
    lines.append(
        base.md_table(
            ["分数段", "公司数", "占评分样本"],
            [[bucket, count, base.fmt_rate(count / len(score) * 100)] for bucket, count in bucket_counts.items()],
            ["---", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append(
        "F51 本次最高分受限于9.2，因为日度金融数据没有真实成交额/ADV/买卖价差。高分主要来自大市值、普通股覆盖、期权链双侧覆盖和估值字段完整；低分主要来自小市值、ADR/ADS比例需确认、foreign ordinary、无期权链、币种错配或金融字段缺失。这个结构天然偏向大盘可交易性，而过去6个月收益窗口偏向小盘高弹性反弹，所以收益排序出现负向并不意外。"
    )

    lines.append("")
    lines.append("## 使用建议")
    lines.extend(
        [
            "- 不建议把 F51 单独作为6个月收益排序因子；本轮主结果、分类中性结果和稳健性结果均不支持高流动性代理分带来更高6个月涨幅。",
            "- 建议把 F51 用作组合容量、交易摩擦和风险过滤变量：同等基本面弹性、催化剂、估值赔率和价格强度下，F51高分公司更适合放大仓位、降低冲击成本和减少执行风险。",
            "- F51 与 F44上行弹性、F50价格相对强度、F37/F38/F39催化剂、F05估值赔率联用更有价值：F51 回答“能不能以足够容量交易”，不回答“涨幅弹性最大在哪里”。",
            "- 对低分但涨幅极高公司，应单独复核真实 ADV、成交额、可融券/借券、买卖价差、场外/ADR交易深度和事件驱动持续性；低分赢家可能能贡献收益，但仓位容量和回撤风险不能按收益排序直接外推。",
            "- 下一轮应补抓真实成交量、美元成交额、30/60日 ADV、换手率、bid-ask spread、期权 OI/成交量和交易所/ADR主上市地成交额；这些数据可把 F51 从代理分升级为更接近交易可执行性的实证因子。",
        ]
    )

    lines.append("")
    lines.append("## 数据与方法限制")
    lines.extend(
        [
            "- 收益文件使用 Yahoo Finance 免费历史行情的 Close 价格，`auto_adjust=False`，不含股息再投资，不是总回报率。",
            "- 6个月收益窗口的最新价格日为 2026-05-27；评分日期为 2026-06-04，日度金融数据日期为 2026-06-03，结论更接近“当前流动性代理评分 vs 过去6个月表现”的解释性检验，不是严格前瞻回测。",
            "- 风险部分没有逐日收益序列，因此不能给出严格日波动率、完整最大回撤或真实下跌日胜率；本报告用三个 SOXX 下跌窗口和当前 IV 作为代理。",
            "- 低流动性剔除使用 F51 自身分数阈值 F51<=5.0，不是独立 ADV 口径；ADR/币种异常剔除依据日度金融数据中的 listing_type、adr_ratio、currency、financial_currency、估值校验和备注。",
            "- 极端涨跌剔除使用交集样本6个月收益的双尾5%分位，阈值为 " + f"{base.fmt_pct(low_tail)} / {base.fmt_pct(high_tail)}。",
        ]
    )

    metadata = {
        "score_rows": len(score),
        "return_rows": len(returns),
        "eval_rows": len(eval_df),
        "spearman": corr["spearman"],
        "top30_diff": top30_diff,
        "out_path": str(OUT_PATH),
        "moved": moved,
    }
    return "\n".join(lines) + "\n", metadata


def main() -> None:
    report, metadata = make_report()
    OUT_PATH.write_text(report, encoding="utf-8")
    print(
        f"wrote={metadata['out_path']}\n"
        f"score_rows={metadata['score_rows']} return_rows={metadata['return_rows']} eval_rows={metadata['eval_rows']}\n"
        f"spearman={float(metadata['spearman']):.6f} top30_diff={float(metadata['top30_diff']):.6f}\n"
        f"moved={metadata['moved']}"
    )


if __name__ == "__main__":
    main()
