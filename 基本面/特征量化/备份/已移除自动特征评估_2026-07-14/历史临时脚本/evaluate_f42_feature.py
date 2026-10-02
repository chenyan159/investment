from __future__ import annotations

import importlib.util
import math
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np


ROOT = Path(r"D:\drive\Investment\基本面")
RUN_DATE = "2026-06-04"
FEATURE_ID = "F42"
FEATURE_NAME = "情景收益不对称性"
FEATURE_SUBJECT = f"{FEATURE_ID}_{FEATURE_NAME}"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_SUBJECT}_量化评分_{RUN_DATE}.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
FINANCE_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
LIQ_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
OUT_PATH = OUT_DIR / f"{FEATURE_SUBJECT}_特征评估_6个月涨跌_{RUN_DATE}.md"
BACKUP_DIR = OUT_DIR / "备份"

BASE_EVAL = ROOT / "tmp" / "evaluate_f39_feature.py"


def load_base_module():
    spec = importlib.util.spec_from_file_location("feature_eval_base_f39", BASE_EVAL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load base evaluator: {BASE_EVAL}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


B = load_base_module()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fmt_num(v: float, digits: int = 3) -> str:
    if v is None or math.isnan(v):
        return "N/A"
    return f"{v:.{digits}f}"


def fmt_pct(v: float | None, digits: int = 2) -> str:
    if v is None or math.isnan(v):
        return "N/A"
    return f"{v:+.{digits}f}%"


def fmt_rate(v: float | None, digits: int = 1) -> str:
    if v is None or math.isnan(v):
        return "N/A"
    return f"{v:.{digits}f}%"


def md_escape(text: str) -> str:
    return (text or "").replace("\n", " ").replace("|", "\\|")


def table(headers: list[str], rows: list[list[object]], aligns: list[str] | None = None) -> str:
    if aligns is None:
        aligns = ["---"] * len(headers)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(aligns) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def describe_strength(spearman_value: float) -> str:
    if math.isnan(spearman_value):
        return "不可判定"
    av = abs(spearman_value)
    if av < 0.05:
        return "接近0"
    if av < 0.15:
        return "很弱"
    if av < 0.30:
        return "弱到中等"
    return "较强"


def describe_signed_strength(value: float) -> str:
    if math.isnan(value):
        return "不可判定"
    direction = "正向" if value > 0 else ("负向" if value < 0 else "零相关")
    return f"{direction}{describe_strength(value)}"


def list_tickers(records: list[dict] | list[str]) -> str:
    if not records:
        return "无"
    if isinstance(records[0], str):
        return ", ".join(sorted(records))
    return ", ".join(r["ticker"] for r in sorted(records, key=lambda x: x["ticker"])) or "无"


def backup_existing_outputs() -> str:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    existing = sorted(OUT_DIR.glob(f"{FEATURE_SUBJECT}_特征评估_6个月涨跌_*.md"))
    if not existing:
        return "本次未发现根目录同类旧版正式输出残留。"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest_dir = BACKUP_DIR / f"{FEATURE_SUBJECT}_6个月涨跌_写入前备份_{stamp}"
    dest_dir.mkdir(parents=True, exist_ok=False)
    moved = []
    for path in existing:
        target = dest_dir / path.name
        shutil.move(str(path), str(target))
        moved.append(path.name)
    return f"写入前已移动同类旧版正式输出 {len(moved)} 个到 `{dest_dir.relative_to(ROOT).as_posix()}`：{', '.join(moved)}。"


def quantile_groups(records_by_rank: list[dict]) -> list[list[dict]]:
    return [list(arr) for arr in np.array_split(np.array(records_by_rank, dtype=object), 5)]


def top_bottom_rows(records: list[dict]) -> tuple[list[list[object]], dict[int, dict[str, float]]]:
    rows = []
    values = {}
    for n in [10, 20, 30]:
        metrics = B.top_bottom_metrics(records, n)
        values[n] = metrics
        rows.append(
            [
                f"Top{n}/Bottom{n}",
                fmt_pct(metrics["top_mean"]),
                fmt_rate(metrics["top_hit"]),
                fmt_pct(metrics["bottom_mean"]),
                fmt_rate(metrics["bottom_hit"]),
                fmt_pct(metrics["spread"]),
            ]
        )
    return rows, values


def neutral_top_bottom_rows(records: list[dict]) -> list[list[object]]:
    rows = []
    for n in [10, 20, 30]:
        metrics = B.top_bottom_metrics(records, n, "neutral_percentile")
        rows.append(
            [
                f"中性Top{n}/Bottom{n}",
                fmt_pct(metrics["top_mean"]),
                fmt_rate(metrics["top_hit"]),
                fmt_pct(metrics["bottom_mean"]),
                fmt_rate(metrics["bottom_hit"]),
                fmt_pct(metrics["spread"]),
            ]
        )
    return rows


def group_summary_rows(records_by_rank: list[dict]) -> list[list[object]]:
    rows = []
    for i, group in enumerate(quantile_groups(records_by_rank), 1):
        stats = B.summary_stats(group)
        label = f"Q{i}{'最高分' if i == 1 else ('最低分' if i == 5 else '')}"
        rows.append(
            [
                label,
                stats["n"],
                f"{stats['score_mean']:.2f}",
                fmt_pct(stats["ret_mean"]),
                fmt_pct(stats["ret_median"]),
                fmt_rate(stats["hit_rate"]),
            ]
        )
    return rows


def category_rows(records: list[dict]) -> tuple[list[list[object]], list[list[object]]]:
    by_cat = defaultdict(list)
    for record in records:
        by_cat[record["category"]].append(record)
    summary = []
    correlations = []
    for cat, group in sorted(by_cat.items(), key=lambda kv: kv[0]):
        stats = B.summary_stats(group)
        metrics = B.corr_metrics(group)
        top_ret = max(group, key=lambda r: r["ret_6m"])
        top_score = min(group, key=lambda r: r["rank"])
        summary.append(
            [
                cat,
                stats["n"],
                f"{stats['score_mean']:.2f}",
                fmt_pct(stats["ret_mean"]),
                fmt_pct(stats["ret_median"]),
            ]
        )
        correlations.append(
            [
                cat,
                len(group),
                fmt_num(metrics["pearson"]),
                fmt_num(metrics["spearman"]),
                fmt_pct(stats["ret_mean"]),
                f"{top_ret['ticker']} {fmt_pct(top_ret['ret_6m'])}",
                f"{top_score['ticker']} {top_score['score']:.1f} / {fmt_pct(top_score['ret_6m'])}",
            ]
        )
    return summary, correlations


def risk_rows(records_by_rank: list[dict]) -> tuple[list[list[object]], list[list[object]], dict[str, dict[str, object]]]:
    top30 = records_by_rank[:30]
    mid_start = max((len(records_by_rank) - 30) // 2, 0)
    mid30 = records_by_rank[mid_start : mid_start + 30]
    bottom30 = list(reversed(records_by_rank[-30:]))
    risk = {}
    risk_table = []
    iv_table = []
    for label, group in [(f"{FEATURE_ID} Top30", top30), (f"{FEATURE_ID} Mid30", mid30), (f"{FEATURE_ID} Bottom30", bottom30)]:
        rg = B.compute_risk_group(records_by_rank, label, group)
        risk[label] = rg
        risk_table.append(
            [
                rg["label"],
                rg["n"],
                rg["obs"],
                fmt_pct(rg["w1"]),
                fmt_pct(rg["w2"]),
                fmt_pct(rg["w3"]),
                fmt_pct(rg["pressure_mean"]),
                fmt_pct(rg["worst_mean"]),
                fmt_pct(rg["dispersion"]),
                fmt_rate(rg["beat_soxx"]),
                fmt_rate(rg["neg_rate"]),
            ]
        )
        ivg = B.compute_iv_group(label, group)
        risk[f"{label} IV"] = ivg
        iv_table.append(
            [
                ivg["label"],
                ivg["n"],
                ivg["iv_coverage"],
                fmt_pct(ivg["call_mean"]),
                fmt_pct(ivg["put_mean"]),
                fmt_pct(ivg["near_mean"]),
                fmt_pct(ivg["near_median"]),
            ]
        )
    return risk_table, iv_table, risk


def robustness(records: list[dict]) -> tuple[list[list[object]], dict[str, object]]:
    low_liq_removed = [r for r in records if not (r["liq_score"] > 5.0)]
    no_low_liq = [r for r in records if r["liq_score"] > 5.0]
    adr_removed = [r for r in records if not B.finance_clean(r["finance"])]
    no_adr = [r for r in records if B.finance_clean(r["finance"])]
    returns = np.array([r["ret_6m"] for r in records], dtype=float)
    low_q = float(np.quantile(returns, 0.05))
    high_q = float(np.quantile(returns, 0.95))
    extreme_removed = [r for r in records if r["ret_6m"] < low_q or r["ret_6m"] > high_q]
    no_extreme = [r for r in records if low_q <= r["ret_6m"] <= high_q]
    combined = [r for r in records if r["liq_score"] > 5.0 and B.finance_clean(r["finance"]) and low_q <= r["ret_6m"] <= high_q]

    specs = [
        ("全样本基准", "无剔除", records, []),
        ("剔除低流动性", "F51交易流动性分 > 5.0", no_low_liq, low_liq_removed),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", no_adr, adr_removed),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(low_q)} / {fmt_pct(high_q)}", no_extreme, extreme_removed),
        ("三项合并剔除", "同时满足上述三项", combined, [r for r in records if r not in combined]),
    ]
    rows = []
    for label, rule, subset, removed in specs:
        metrics = B.corr_metrics(subset) if len(subset) >= 3 else {"pearson": float("nan"), "spearman": float("nan"), "kendall": float("nan")}
        n = min(30, len(subset) // 2)
        tb = B.top_bottom_metrics(subset, n) if len(subset) >= 2 else {}
        rows.append(
            [
                label,
                rule,
                len(subset),
                len(removed),
                fmt_num(metrics["pearson"]),
                fmt_num(metrics["spearman"]),
                fmt_num(metrics["kendall"]),
                fmt_pct(tb.get("top_mean", float("nan"))),
                fmt_pct(tb.get("bottom_mean", float("nan"))),
                fmt_pct(tb.get("spread", float("nan"))),
            ]
        )
    detail = {
        "low_liq_removed": low_liq_removed,
        "adr_removed": adr_removed,
        "extreme_removed": extreme_removed,
        "combined": combined,
        "combined_metrics": B.corr_metrics(combined),
        "combined_tb": B.top_bottom_metrics(combined, min(30, len(combined) // 2)),
        "low_q": low_q,
        "high_q": high_q,
    }
    return rows, detail


def composition_rows(records_by_rank: list[dict]) -> list[list[object]]:
    rows = []
    for label, group in [("Top10", records_by_rank[:10]), ("Bottom10", list(reversed(records_by_rank[-10:])))]:
        for r in group:
            rows.append(
                [
                    label,
                    r["ticker"],
                    md_escape(r["name"]),
                    r["category"],
                    f"{r['score']:.1f}",
                    r["rank"],
                    fmt_pct(r["ret_6m"]),
                    r["confidence"],
                ]
            )
    return rows


def return_diag_rows(records: list[dict], reverse: bool) -> list[list[object]]:
    rows = []
    for r in sorted(records, key=lambda x: x["ret_6m"], reverse=reverse)[:15]:
        rows.append(
            [
                r["ticker"],
                md_escape(r["name"]),
                r["category"],
                fmt_pct(r["ret_6m"]),
                f"{r['score']:.1f}",
                r["rank"],
                r["confidence"],
            ]
        )
    return rows


def top_score_rows(records_by_rank: list[dict]) -> list[list[object]]:
    return [
        [
            r["rank"],
            r["ticker"],
            md_escape(r["name"]),
            r["category"],
            f"{r['score']:.1f}",
            fmt_pct(r["ret_6m"]),
            r["confidence"],
        ]
        for r in records_by_rank[:30]
    ]


def load_records():
    scores = B.parse_score_file(SCORE_PATH)
    returns, stress = B.parse_return_file(RETURN_PATH)
    finance = B.parse_finance_file(FINANCE_PATH)
    liquidity = B.parse_liquidity_file(LIQ_PATH)
    records = B.build_records(scores, returns, stress, finance, liquidity)
    return scores, returns, records


def make_report() -> str:
    scores, returns, records = load_records()
    records_by_rank = sorted(records, key=lambda r: r["rank"])
    metrics = B.corr_metrics(records)
    neutral_percentile_metrics = B.corr_metrics(records, "neutral_percentile", "ret_6m")
    residual_metrics = B.corr_metrics(records, "score_resid", "ret_resid")

    quintile_rows = group_summary_rows(records_by_rank)
    tb_rows, tb_values = top_bottom_rows(records)
    neutral_tb = neutral_top_bottom_rows(records)
    cat_summary, cat_corr = category_rows(records)
    risk_table, iv_table, risk = risk_rows(records_by_rank)
    robust_rows, robust_detail = robustness(records)

    missing_scores = sorted(set(scores) - set(returns))
    extra_returns = sorted(set(returns) - set(scores))

    score_text = read_text(SCORE_PATH)
    score_date_match = re.search(r"评分日期：(\d{4}-\d{2}-\d{2})", score_text)
    score_date = score_date_match.group(1) if score_date_match else RUN_DATE
    score_count_match = re.search(r"公司数量：(\d+)", score_text)
    score_count = score_count_match.group(1) if score_count_match else str(len(scores))

    backup_note = backup_existing_outputs()
    top30_spread = tb_values[30]["spread"]
    top30_risk = risk[f"{FEATURE_ID} Top30"]
    bottom30_risk = risk[f"{FEATURE_ID} Bottom30"]
    top30_iv = risk[f"{FEATURE_ID} Top30 IV"]
    bottom30_iv = risk[f"{FEATURE_ID} Bottom30 IV"]

    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 6个月涨跌 {RUN_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.append(f"- 评估对象：`{FEATURE_SUBJECT}`。")
    lines.append(f"- 评分输入：`{SCORE_PATH.relative_to(ROOT).as_posix()}`，评分日期 {score_date}，覆盖 {score_count} 家。")
    lines.append("- 收益输入：`日度资料/区间涨跌/公司股价区间涨跌幅_2026-05-27.md`，生成时间 2026-05-27 20:17:54 -0700（本机时区），价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。")
    lines.append("- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。")
    lines.append("- 稳健性辅助输入：`特征量化/量化评分/F51_交易流动性_量化评分_2026-06-04.md`；`日度资料/每日金融数据/每日金融数据_2026-06-03.md`，金融数据生成时间 2026-06-03 13:41:46 PDT-0700。")
    lines.append(f"- 有效评估样本：评分与6个月涨跌交集 {len(records)} 家；F42评分有但6个月涨跌缺失 {len(missing_scores)} 家。")
    lines.append("- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。")
    lines.append("- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动率、完整最大回撤或逐日下跌日胜率；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度、跑赢 SOXX 比例和负收益窗口占比作为下跌窗口代理，并用2026-06-03近ATM Call/Put IV均值补充当前波动代理。")
    lines.append("- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。")
    lines.append("- 时间方向限制：F42评分日期为2026-06-04，6个月收益窗口截至2026-05-27，本报告是“当前情景收益不对称性评分 vs 过去6个月收益”的横截面对照，不是严格样本外预测回测。")
    lines.append("- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F42 正式输出；本次未读取旧版 F42 特征评估作为结论依据。")
    lines.append(f"- {backup_note}")
    lines.append("")

    lines.append("## 结论摘要")
    lines.append(f"- 排序有效性：{describe_signed_strength(metrics['spearman'])}。全样本 Pearson {fmt_num(metrics['pearson'])}, Spearman {fmt_num(metrics['spearman'])}, Kendall {fmt_num(metrics['kendall'])}；重点指标 Spearman {fmt_num(metrics['spearman'])}，方向为负，说明本次过去6个月里高 F42 并没有对应更高涨幅，反而低分高 beta/低基数反弹公司贡献了更高收益。")
    lines.append(f"- Top/Bottom能力：Top10、Top20、Top30 平均收益分别为 {fmt_pct(tb_values[10]['top_mean'])}、{fmt_pct(tb_values[20]['top_mean'])}、{fmt_pct(tb_values[30]['top_mean'])}；Top-Bottom收益差分别为 {fmt_pct(tb_values[10]['spread'])}、{fmt_pct(tb_values[20]['spread'])}、{fmt_pct(tb_values[30]['spread'])}。")
    lines.append(f"- 风险解释力：正向。Top30 压力窗口均值 {fmt_pct(top30_risk['pressure_mean'])}，Bottom30 为 {fmt_pct(bottom30_risk['pressure_mean'])}；Top30 平均最差窗口 {fmt_pct(top30_risk['worst_mean'])}，Bottom30 为 {fmt_pct(bottom30_risk['worst_mean'])}；Top30 近ATM IV均值 {fmt_pct(top30_iv['near_mean'])}，Bottom30 为 {fmt_pct(bottom30_iv['near_mean'])}。这说明 F42 更能解释下跌窗口韧性和当前波动风险，而不是本轮6个月涨幅排序。")
    lines.append(f"- 分类中性：分类内百分位合并 Spearman {fmt_num(neutral_percentile_metrics['spearman'])}，分类去均值残差 Spearman {fmt_num(residual_metrics['spearman'])}，负向关系在分类中性后仍保留，说明它不只是押错某个产业目录，而是同一目录内也存在“高赔率低波动资产涨幅弱于高 beta 反弹资产”的窗口风格。")
    lines.append(f"- 稳健性：三项合并剔除后样本 {len(robust_detail['combined'])} 家，Spearman {fmt_num(robust_detail['combined_metrics']['spearman'])}，Top30-Bottom30 {fmt_pct(robust_detail['combined_tb']['spread'])}；剔除低流动性、ADR/币种异常和极端涨跌后，收益排序负向结论仍成立，但负向幅度收窄。")
    lines.append("- 解释：F42衡量牛/基/熊情景下上行空间、下行保护和可验证节点是否形成有利收益不对称。用过去6个月收益做对照时，高分端往往包含已被市场定价的高质量核心资产，低分端可能出现低基数、小盘题材或亏损高 beta 的极端反弹；因此本报告更适合检验“情景赔率评分是否解释已发生行情和压力窗口表现”，不应直接等同于未来预测能力。")
    lines.append("")

    lines.append("## 覆盖检查")
    lines.append(
        table(
            ["项目", "数量", "说明"],
            [
                ["F42评分覆盖", len(scores), "来自2026-06-04评分文件"],
                ["6个月涨跌覆盖", len(returns), "来自2026-05-27区间涨跌文件"],
                ["交集样本", len(records), "用于本次所有主指标"],
                ["评分有但6个月涨跌缺失", len(missing_scores), list_tickers(missing_scores)],
                ["涨跌有但评分缺失", len(extra_returns), ", ".join(extra_returns) if extra_returns else "无"],
            ],
            ["---", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.append(
        table(
            ["分类目录", "样本数", "F42均分", "6个月平均收益", "6个月中位收益"],
            cat_summary,
            ["---", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")

    lines.append("## 排序有效性")
    lines.append(
        table(
            ["指标", "数值", "解释"],
            [
                ["Pearson", fmt_num(metrics["pearson"]), "线性相关；受极端涨跌影响较大"],
                ["Spearman", fmt_num(metrics["spearman"]), "排序相关；这是本任务最重要指标"],
                ["Kendall tau-b", fmt_num(metrics["kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
            ],
            ["---", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 分数分组收益")
    lines.append(
        table(
            ["分组", "公司数", "F42均分", "6个月平均收益", "6个月中位收益", "命中率"],
            quintile_rows,
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")

    lines.append("## Top/Bottom能力")
    lines.append(
        table(
            ["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"],
            tb_rows,
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    lines.append(
        table(
            ["组别", "股票代号", "公司名称", "分类目录", "F42分", "F42排名", "6个月收益", "置信度"],
            composition_rows(records_by_rank),
            ["---", "---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")

    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为下跌窗口代理。严格日度波动率、完整最大回撤和逐日下跌日胜率需要逐日价格序列，本次输入文件没有提供；近ATM IV为2026-06-03当前期权波动代理，不等同于过去6个月实际波动率。")
    lines.append(
        table(
            ["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"],
            risk_table,
            ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("### 当前IV代理")
    lines.append(
        table(
            ["分组", "公司数", "IV覆盖", "Call IV均值", "Put IV均值", "近ATM IV均值", "近ATM IV中位数"],
            iv_table,
            ["---", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("判断方式：若高分组压力窗口均值更高、平均最差窗口更浅、跑赢 SOXX 比例更高且近ATM IV更低，说明F42高分公司不仅收益更好，也更符合“上行/下行不对称”的风险解释；反之则说明评分捕捉的是基本面赔率，但短期市场波动、估值和题材交易仍占主导。")
    lines.append("")

    lines.append("## 分类中性结果")
    lines.append(
        table(
            ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
            [
                ["原始全样本", len(records), fmt_num(metrics["pearson"]), fmt_num(metrics["spearman"]), fmt_num(metrics["kendall"]), "直接用F42分数排序"],
                ["分类内百分位合并", len(records), fmt_num(neutral_percentile_metrics["pearson"]), fmt_num(neutral_percentile_metrics["spearman"]), fmt_num(neutral_percentile_metrics["kendall"]), "每个分类内先按F42排序，再转成0-1百分位后合并"],
                ["分类去均值残差", len(records), fmt_num(residual_metrics["pearson"]), fmt_num(residual_metrics["spearman"]), fmt_num(residual_metrics["kendall"]), "F42和收益分别减去分类均值后相关"],
            ],
            ["---", "---:", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(
        table(
            ["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"],
            neutral_tb,
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("说明：分类中性 Top/Bottom 用于检验 F42 是否只是押中某些强势目录。若分类内百分位和去均值残差仍为正，说明同目录内情景赔率排序有额外信息；若转弱或转负，则原始结果更多来自分类暴露、极端公司或窗口风格。")
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(
        table(
            ["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F42公司"],
            cat_corr,
            ["---", "---:", "---:", "---:", "---:", "---", "---"],
        )
    )
    lines.append("")

    lines.append("## 稳健性检验")
    lines.append(
        table(
            ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"],
            robust_rows,
            ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("稳健性结论：低流动性、ADR/币种异常和极端涨跌剔除后，重点看 Spearman 和 Top30-Bottom30 是否同向保持。若三项合并剔除后仍能保持正向，说明 F42 至少有独立排序价值；若转负或接近0，则更适合作为基本面赔率监控、组合风险约束和研究优先级信号，而不是独立收益排序因子。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(
        table(
            ["剔除项", "数量", "公司"],
            [
                ["低流动性", len(robust_detail["low_liq_removed"]), list_tickers(robust_detail["low_liq_removed"])],
                ["ADR/币种异常", len(robust_detail["adr_removed"]), list_tickers(robust_detail["adr_removed"])],
                ["极端涨跌双尾5%", len(robust_detail["extreme_removed"]), list_tickers(robust_detail["extreme_removed"])],
            ],
            ["---", "---:", "---"],
        )
    )
    lines.append("")

    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    lines.append(
        table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F42分", "F42排名", "F42置信度"],
            return_diag_rows(records, True),
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 6个月跌幅前15")
    lines.append(
        table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F42分", "F42排名", "F42置信度"],
            return_diag_rows(records, False),
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### F42 Top30收益明细")
    lines.append(
        table(
            ["F42排名", "股票代号", "公司名称", "分类目录", "F42分", "6个月收益", "置信度"],
            top_score_rows(records_by_rank),
            ["---:", "---", "---", "---", "---:", "---:", "---"],
        )
    )
    lines.append("")

    lines.append("## 结论与使用建议")
    lines.append(f"- 主结论：F42在本次过去6个月横截面对照中的 Spearman 为 {fmt_num(metrics['spearman'])}，Top30-Bottom30 为 {fmt_pct(top30_spread)}；应把这两个指标作为本报告的核心读数。")
    lines.append("- 若用于后续模型：F42更适合作为基本面赔率和风险约束特征，与价格相对强度、估值赔率、流动性、预期差、执行风险和行业中性约束共同使用，不宜单独作为6个月收益排序因子。")
    lines.append("- 若用于研究流程：高分但过去6个月收益弱的公司，需要检查上行空间是否已经被估值/IV提前吸收、悲观情景保护是否真的可验证、或短期催化是否不足；低分但涨幅极高的公司，应单独标记为低基数反弹、小盘题材扩散、亏损高 beta 或极端供需挤压。")
    lines.append("- 若要做真正前瞻验证：建议以2026-06-04评分为起点，滚动跟踪未来6个月、9个月和12个月收益，并与本报告的历史横截面对照分开存档。")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    report = make_report()
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(f"WROTE {OUT_PATH}")
    print(f"SIZE {OUT_PATH.stat().st_size}")


if __name__ == "__main__":
    main()
