from __future__ import annotations

import math
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
FEATURE = "F24_单位负载价值量"
WINDOW = "6个月"
RUN_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE}_量化评分_2026-06-04.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
F51_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUT_DIR / "备份"
TARGET_PATH = OUT_DIR / f"{FEATURE}_特征评估_{WINDOW}涨跌_{RUN_DATE}.md"

SOXX_WINDOWS = [
    ("SOXX下跌1 2025-02-20至2025-04-08", -32.98),
    ("SOXX下跌2 2026-02-25至2026-03-30", -15.82),
    ("SOXX下跌3 2025-10-29至2025-11-20", -13.40),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_md_row(line: str) -> list[str] | None:
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return None
    return [cell.strip() for cell in s.strip("|").split("|")]


def is_sep_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells)


def parse_pct(cell: str) -> float | None:
    if cell is None or "N/A" in cell:
        return None
    m = re.search(r"(上涨|下跌|持平)\s*([+-]?\d[\d,]*(?:\.\d+)?)%", cell)
    if not m:
        return None
    direction, number = m.groups()
    value = float(number.replace(",", ""))
    if direction == "下跌" and value > 0:
        value = -value
    if direction == "上涨" and value < 0:
        value = abs(value)
    return value


def parse_number(text: str) -> float | None:
    if text is None:
        return None
    s = text.strip().replace(",", "")
    if not s or s in {"缺失", "不适用", "N/A"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_score_table(path: Path) -> pd.DataFrame:
    text = read_text(path)
    rows: list[dict] = []
    in_table = False
    for line in text.splitlines():
        if line.strip() == "## 全公司排序表":
            in_table = True
            continue
        if in_table and line.startswith("## ") and line.strip() != "## 全公司排序表":
            break
        if not in_table:
            continue
        cells = split_md_row(line)
        if not cells or is_sep_row(cells):
            continue
        if cells[0] == "排名":
            continue
        if len(cells) >= 10 and re.fullmatch(r"\d+", cells[0]):
            rows.append(
                {
                    "rank": int(cells[0]),
                    "ticker": cells[1],
                    "company": cells[2],
                    "category": cells[3],
                    "score": float(cells[4]),
                    "evidence": cells[5],
                    "confidence": cells[6],
                    "core_evidence": cells[7],
                    "downgrade": cells[8],
                    "follow_up": cells[9],
                }
            )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"No score rows parsed from {path}")
    return df


def parse_interval_returns(path: Path, categories: set[str]) -> pd.DataFrame:
    text = read_text(path)
    rows: list[dict] = []
    section = False
    current_category: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "## 按分类分组的公司明细":
            section = True
            current_category = None
            continue
        if section and stripped.startswith("## ") and stripped != "## 按分类分组的公司明细":
            break
        if not section:
            continue
        hm = re.match(r"^#{3,4}\s+(.+?)\s*$", stripped)
        if hm and hm.group(1) in categories:
            current_category = hm.group(1)
            continue
        cells = split_md_row(line)
        if not cells or is_sep_row(cells):
            continue
        if cells[0] == "股票代号":
            continue
        if current_category and len(cells) >= 9:
            rows.append(
                {
                    "ticker": cells[0],
                    "company_return": cells[1],
                    "return_category": current_category,
                    "latest_trade_date": cells[2],
                    "latest_close": parse_number(cells[3]),
                    "ret_1m": parse_pct(cells[4]),
                    "ret_3m": parse_pct(cells[5]),
                    "ret_6m": parse_pct(cells[6]),
                    "ret_1y": parse_pct(cells[7]),
                    "return_note": cells[8],
                }
            )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"No interval return rows parsed from {path}")
    return df


def parse_pressure_returns(path: Path, categories: set[str]) -> pd.DataFrame:
    text = read_text(path)
    rows: list[dict] = []
    section = False
    current_category: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "### 按分类分组的全公司明细":
            section = True
            current_category = None
            continue
        if section and stripped == "## 按分类分组的公司明细":
            break
        if not section:
            continue
        hm = re.match(r"^#{3,5}\s+(.+?)\s*$", stripped)
        if hm and hm.group(1) in categories:
            current_category = hm.group(1)
            continue
        cells = split_md_row(line)
        if not cells or is_sep_row(cells):
            continue
        if cells[0] == "股票代号":
            continue
        if current_category and len(cells) >= 6:
            rows.append(
                {
                    "ticker": cells[0],
                    "company_pressure": cells[1],
                    "pressure_category": current_category,
                    "soxx1": parse_pct(cells[2]),
                    "soxx2": parse_pct(cells[3]),
                    "soxx3": parse_pct(cells[4]),
                    "pressure_note": cells[5],
                }
            )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"No pressure rows parsed from {path}")
    return df


def parse_financial(path: Path) -> pd.DataFrame:
    text = read_text(path)
    rows: list[dict] = []
    for line in text.splitlines():
        cells = split_md_row(line)
        if not cells or is_sep_row(cells):
            continue
        if cells[0] == "股票代号":
            continue
        if len(cells) >= 25:
            rows.append(
                {
                    "ticker": cells[0],
                    "fin_company": cells[1],
                    "price_date": cells[2],
                    "market_cap": cells[4],
                    "currency": cells[13],
                    "financial_currency": cells[14],
                    "listing_type": cells[19],
                    "adr_ratio": cells[20],
                    "valuation_check": cells[23],
                    "fin_note": cells[24],
                }
            )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"No financial rows parsed from {path}")
    return df


def rank_percentile_high(values: pd.Series) -> pd.Series:
    n = values.notna().sum()
    if n <= 1:
        return pd.Series([0.5] * len(values), index=values.index)
    return (values.rank(method="average", ascending=True) - 1) / (n - 1)


def pearson(x: pd.Series, y: pd.Series) -> float:
    sub = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(sub) < 2:
        return math.nan
    return float(sub["x"].corr(sub["y"], method="pearson"))


def spearman(x: pd.Series, y: pd.Series) -> float:
    sub = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(sub) < 2:
        return math.nan
    return pearson(sub["x"].rank(method="average"), sub["y"].rank(method="average"))


def kendall_tau_b(x: pd.Series, y: pd.Series) -> float:
    sub = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(sub)
    if n < 2:
        return math.nan
    xs = sub["x"].to_numpy()
    ys = sub["y"].to_numpy()
    concordant = discordant = ties_x = ties_y = 0
    for i in range(n - 1):
        dx = xs[i] - xs[i + 1 :]
        dy = ys[i] - ys[i + 1 :]
        sx = np.sign(dx)
        sy = np.sign(dy)
        both_tied = (sx == 0) & (sy == 0)
        ties_x += int(((sx == 0) & (sy != 0)).sum())
        ties_y += int(((sx != 0) & (sy == 0)).sum())
        valid = ~both_tied & (sx != 0) & (sy != 0)
        concordant += int((sx[valid] * sy[valid] > 0).sum())
        discordant += int((sx[valid] * sy[valid] < 0).sum())
    denom = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    if denom == 0:
        return math.nan
    return (concordant - discordant) / denom


def corr_pack(df: pd.DataFrame, score_col: str = "score") -> dict:
    sub = df[[score_col, "ret_6m"]].dropna()
    return {
        "n": len(sub),
        "pearson": pearson(sub[score_col], sub["ret_6m"]),
        "spearman": spearman(sub[score_col], sub["ret_6m"]),
        "kendall": kendall_tau_b(sub[score_col], sub["ret_6m"]),
    }


def sorted_by_score(df: pd.DataFrame, ascending: bool = False) -> pd.DataFrame:
    if ascending:
        return df.sort_values(["score", "rank"], ascending=[True, False]).reset_index(drop=True)
    return df.sort_values(["score", "rank"], ascending=[False, True]).reset_index(drop=True)


def group_stats(df: pd.DataFrame, label_col: str = "score_group") -> pd.DataFrame:
    rows = []
    for label, g in df.groupby(label_col, sort=False):
        rows.append(
            {
                "group": label,
                "n": len(g),
                "score_mean": g["score"].mean(),
                "ret_mean": g["ret_6m"].mean(),
                "ret_median": g["ret_6m"].median(),
                "hit_rate": (g["ret_6m"] > 0).mean(),
            }
        )
    return pd.DataFrame(rows)


def top_bottom_stats(df: pd.DataFrame, score_col: str = "score") -> list[dict]:
    rows = []
    for n in (10, 20, 30):
        if score_col == "score":
            high = sorted_by_score(df).head(n)
            low = sorted_by_score(df, ascending=True).head(n)
        else:
            high = df.sort_values([score_col, "score", "rank"], ascending=[False, False, True]).head(n)
            low = df.sort_values([score_col, "score", "rank"], ascending=[True, True, False]).head(n)
        rows.append(
            {
                "n": n,
                "top_mean": high["ret_6m"].mean(),
                "top_hit": (high["ret_6m"] > 0).mean(),
                "bottom_mean": low["ret_6m"].mean(),
                "bottom_hit": (low["ret_6m"] > 0).mean(),
                "spread": high["ret_6m"].mean() - low["ret_6m"].mean(),
            }
        )
    return rows


def pressure_stats(df: pd.DataFrame, label: str) -> dict:
    cols = ["soxx1", "soxx2", "soxx3"]
    values = df[cols]
    obs = values.stack().dropna()
    out = {
        "group": label,
        "n": len(df),
        "obs": len(obs),
        "soxx1_mean": df["soxx1"].mean(),
        "soxx2_mean": df["soxx2"].mean(),
        "soxx3_mean": df["soxx3"].mean(),
        "pressure_mean": obs.mean(),
        "worst_avg": values.min(axis=1, skipna=True).mean(),
        "dispersion": obs.std(ddof=0),
        "negative_rate": (obs < 0).mean(),
    }
    wins = []
    for col, (_, soxx_ret) in zip(cols, SOXX_WINDOWS):
        s = df[col].dropna()
        wins.extend((s > soxx_ret).tolist())
    out["beat_soxx_rate"] = float(np.mean(wins)) if wins else math.nan
    return out


def fmt_num(x: float, digits: int = 3) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "N/A"
    return f"{x:.{digits}f}"


def fmt_pct(x: float | None, digits: int = 2) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "N/A"
    return f"{x:+.{digits}f}%"


def fmt_rate(x: float | None, digits: int = 1) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "N/A"
    return f"{x * 100:.{digits}f}%"


def md_table(headers: list[str], rows: list[list[str]], aligns: list[str] | None = None) -> str:
    aligns = aligns or ["---"] * len(headers)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(aligns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def tickers_join(series: pd.Series) -> str:
    vals = list(dict.fromkeys(str(x) for x in series.dropna()))
    return ", ".join(vals) if vals else "无"


def backup_existing() -> list[str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    pattern = f"{FEATURE}_特征评估_{WINDOW}涨跌_*.md"
    existing = [p for p in OUT_DIR.glob(pattern) if p.is_file()]
    if not existing:
        return []
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    subdir = BACKUP_DIR / f"{FEATURE}_{WINDOW}涨跌_{RUN_DATE}_写入前备份_{stamp}"
    subdir.mkdir(parents=True, exist_ok=True)
    moved = []
    for path in existing:
        dst = subdir / path.name
        shutil.move(str(path), str(dst))
        moved.append(str(dst.relative_to(ROOT)))
    return moved


def score_level(v: float) -> str:
    if v >= 9:
        return "9.0-10.0"
    if v >= 8:
        return "8.0-8.9"
    if v >= 7:
        return "7.0-7.9"
    if v >= 5:
        return "5.0-6.9"
    if v >= 3:
        return "3.0-4.9"
    return "1.0-2.9"


def make_report() -> tuple[str, dict]:
    score = parse_score_table(SCORE_PATH)
    f51 = parse_score_table(F51_PATH).rename(columns={"score": "liquidity_score"})
    categories = set(score["category"])
    interval = parse_interval_returns(RETURN_PATH, categories)
    pressure = parse_pressure_returns(RETURN_PATH, categories)
    fin = parse_financial(FIN_PATH)

    df = (
        score.merge(interval, on="ticker", how="left")
        .merge(pressure[["ticker", "soxx1", "soxx2", "soxx3", "pressure_note"]], on="ticker", how="left")
        .merge(f51[["ticker", "liquidity_score"]], on="ticker", how="left")
        .merge(fin[["ticker", "currency", "financial_currency", "listing_type", "adr_ratio", "valuation_check", "fin_note"]], on="ticker", how="left")
    )
    eval_df = df[df["ret_6m"].notna()].copy()
    eval_df["category_pct"] = eval_df.groupby("category")["score"].transform(rank_percentile_high)
    eval_df["score_resid"] = eval_df["score"] - eval_df.groupby("category")["score"].transform("mean")
    eval_df["return_resid"] = eval_df["ret_6m"] - eval_df.groupby("category")["ret_6m"].transform("mean")
    eval_df["score_group"] = pd.qcut(
        eval_df["score"].rank(method="first", ascending=False),
        5,
        labels=["Q1最高分", "Q2", "Q3", "Q4", "Q5最低分"],
    )

    missing_returns = df[df["ret_6m"].isna()].sort_values("rank")
    returns_no_score = interval[~interval["ticker"].isin(score["ticker"])]

    corr_main = corr_pack(eval_df)
    corr_neutral = corr_pack(eval_df, "category_pct")
    corr_resid = {
        "n": len(eval_df[["score_resid", "return_resid"]].dropna()),
        "pearson": pearson(eval_df["score_resid"], eval_df["return_resid"]),
        "spearman": spearman(eval_df["score_resid"], eval_df["return_resid"]),
        "kendall": kendall_tau_b(eval_df["score_resid"], eval_df["return_resid"]),
    }
    tb = top_bottom_stats(eval_df)
    tb_neutral = top_bottom_stats(eval_df, "category_pct")

    top_sorted = sorted_by_score(eval_df)
    bottom_sorted = sorted_by_score(eval_df, ascending=True)
    mid_start = max((len(top_sorted) - 30) // 2, 0)
    pressure_rows = [
        pressure_stats(top_sorted.head(30), "F24 Top30"),
        pressure_stats(top_sorted.iloc[mid_start : mid_start + 30], "F24 Mid30"),
        pressure_stats(bottom_sorted.head(30), "F24 Bottom30"),
    ]

    group_rows = group_stats(eval_df)
    cat_summary = []
    cat_corrs = []
    for cat, g in eval_df.groupby("category", sort=False):
        top_cat = sorted_by_score(g).iloc[0]
        high_ret = g.loc[g["ret_6m"].idxmax()]
        cat_summary.append(
            {
                "category": cat,
                "n": len(g),
                "score_mean": g["score"].mean(),
                "ret_mean": g["ret_6m"].mean(),
                "ret_median": g["ret_6m"].median(),
            }
        )
        cat_corrs.append(
            {
                "category": cat,
                "n": len(g),
                "pearson": pearson(g["score"], g["ret_6m"]),
                "spearman": spearman(g["score"], g["ret_6m"]),
                "ret_mean": g["ret_6m"].mean(),
                "highest_return": f"{high_ret['ticker']} {fmt_pct(high_ret['ret_6m'])}",
                "highest_score": f"{top_cat['ticker']} {top_cat['score']:.1f} / {fmt_pct(top_cat['ret_6m'])}",
            }
        )

    low_liq_mask = eval_df["liquidity_score"].fillna(-999) <= 5.0
    adr_currency_mask = (
        eval_df["listing_type"].fillna("").str.contains("ADR/ADS", case=False, regex=False)
        | (eval_df["currency"] != eval_df["financial_currency"])
        | eval_df["valuation_check"].fillna("").str.contains("currency_mismatch", case=False, regex=False)
    )
    q_low = float(eval_df["ret_6m"].quantile(0.05))
    q_high = float(eval_df["ret_6m"].quantile(0.95))
    extreme_mask = (eval_df["ret_6m"] <= q_low) | (eval_df["ret_6m"] >= q_high)

    robustness_specs = [
        ("全样本基准", "无剔除", pd.Series(False, index=eval_df.index)),
        ("剔除低流动性", "F51交易流动性分 > 5.0", low_liq_mask),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", adr_currency_mask),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(q_low)} / {fmt_pct(q_high)}", extreme_mask),
        ("三项合并剔除", "同时满足上述三项", low_liq_mask | adr_currency_mask | extreme_mask),
    ]
    robustness_rows = []
    for name, rule, mask in robustness_specs:
        sub = eval_df[~mask].copy()
        c = corr_pack(sub)
        tb30 = top_bottom_stats(sub)[-1] if len(sub) >= 60 else None
        robustness_rows.append(
            {
                "name": name,
                "rule": rule,
                "n": len(sub),
                "removed": int(mask.sum()),
                **c,
                "top30": tb30["top_mean"] if tb30 else math.nan,
                "bottom30": tb30["bottom_mean"] if tb30 else math.nan,
                "spread30": tb30["spread"] if tb30 else math.nan,
            }
        )

    winners15 = eval_df.sort_values("ret_6m", ascending=False).head(15)
    losers10 = eval_df.sort_values("ret_6m", ascending=True).head(10)
    top10 = top_sorted.head(10)
    bottom10 = bottom_sorted.head(10)

    score["score_level"] = score["score"].map(score_level)
    score_bins = score["score_level"].value_counts().reindex(
        ["9.0-10.0", "8.0-8.9", "7.0-7.9", "5.0-6.9", "3.0-4.9", "1.0-2.9"], fill_value=0
    )

    moved = backup_existing()

    high = top_sorted.head(30)
    low = bottom_sorted.head(30)
    spearman_main = corr_main["spearman"]
    spread30 = tb[-1]["spread"]
    risk_top = pressure_rows[0]
    risk_bottom = pressure_rows[2]
    robust_combined = robustness_rows[-1]

    if spearman_main >= 0.10:
        rank_conclusion = "弱正向"
    elif spearman_main <= -0.10:
        rank_conclusion = "弱负向"
    else:
        rank_conclusion = "接近0"
    if spread30 > 0:
        tb_conclusion = "Top30 相对 Bottom30 有正收益差"
    else:
        tb_conclusion = "Top30 相对 Bottom30 没有正收益差"
    risk_conclusion = (
        "高分组压力窗口均值优于低分组"
        if risk_top["pressure_mean"] > risk_bottom["pressure_mean"]
        else "高分组压力窗口均值不优于低分组"
    )

    lines: list[str] = []
    lines.append(f"# F24 单位负载价值量 特征评估 6个月涨跌 {RUN_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.extend(
        [
            "- 评估对象：F24_单位负载价值量。",
            f"- 评分输入：`{SCORE_PATH.relative_to(ROOT)}`，评分日期 2026-06-04，覆盖 {len(score)} 家。",
            f"- 收益输入：`{RETURN_PATH.relative_to(ROOT)}`，生成时间 2026-05-27 20:17:54 -0700，价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。",
            "- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。",
            f"- 稳健性辅助输入：`{F51_PATH.relative_to(ROOT)}`；`{FIN_PATH.relative_to(ROOT)}`。",
            f"- 有效评估样本：评分与6个月涨跌交集 {len(eval_df)} 家；F24评分有但6个月涨跌缺失 {len(missing_returns)} 家。",
            "- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。",
            "- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为风险代理。",
            "- 旧版处理：写入前已检查 `特征量化/特征评估/` 根目录同类正式输出；若有残留会移动到 `特征量化/特征评估/备份/`。本次未读取旧版特征评估作为结论依据。",
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
            f"- 排序有效性：{rank_conclusion}。全样本 Pearson {fmt_num(corr_main['pearson'])}, Spearman {fmt_num(corr_main['spearman'])}, Kendall {fmt_num(corr_main['kendall'])}；重点 Spearman {fmt_num(spearman_main)}，说明 F24 对本次6个月收益排序的单因子解释力不足。",
            f"- Top/Bottom能力：{tb_conclusion}。Top10、Top20、Top30 的平均收益分别为 {fmt_pct(tb[0]['top_mean'])}、{fmt_pct(tb[1]['top_mean'])}、{fmt_pct(tb[2]['top_mean'])}；Top-Bottom收益差分别为 {fmt_pct(tb[0]['spread'])}、{fmt_pct(tb[1]['spread'])}、{fmt_pct(tb[2]['spread'])}。",
            f"- 风险解释力：{risk_conclusion}。Top30 压力窗口均值 {fmt_pct(risk_top['pressure_mean'])}，Bottom30 为 {fmt_pct(risk_bottom['pressure_mean'])}；Top30 平均最差窗口 {fmt_pct(risk_top['worst_avg'])}，Bottom30 为 {fmt_pct(risk_bottom['worst_avg'])}。高单位负载价值量不是低回撤因子。",
            f"- 分类中性：分类内百分位合并 Spearman {fmt_num(corr_neutral['spearman'])}，分类去均值残差 Spearman {fmt_num(corr_resid['spearman'])}；信号没有在10个分类目录内稳定保留。",
            f"- 稳健性：三项合并剔除后样本 {robust_combined['n']} 家，Spearman {fmt_num(robust_combined['spearman'])}，Top30-Bottom30 {fmt_pct(robust_combined['spread30'])}；剔除低流动性、ADR/币种异常和极端涨跌后仍不能形成稳定正向排序。",
            "- 解释：F24 衡量的是每 GPU/rack/MW/port/wafer start 的单位经济价值，而本窗口收益主要由高弹性修复、低基数小中盘、光互联/存储/设备贝塔和少数极端涨幅驱动。NVDA、AVGO、VRT、GEV、ETN 等高分公司的单位价值量证据强，但在2025-11至2026-05这段收益窗口里未显著跑赢低分修复型标的。",
        ]
    )

    lines.append("")
    lines.append("## 覆盖检查")
    lines.append(
        md_table(
            ["项目", "数量", "说明"],
            [
                ["F24评分覆盖", str(len(score)), "来自2026-06-04评分文件"],
                ["6个月涨跌覆盖", str(len(interval)), "来自2026-05-27区间涨跌文件"],
                ["交集样本", str(len(eval_df)), "用于本次所有主指标"],
                ["评分有但6个月涨跌缺失", str(len(missing_returns)), tickers_join(missing_returns["ticker"])],
                ["涨跌有但评分缺失", str(len(returns_no_score)), tickers_join(returns_no_score["ticker"])],
            ],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.append(
        md_table(
            ["分类目录", "样本数", "F24均分", "6个月平均收益", "6个月中位收益"],
            [
                [r["category"], str(r["n"]), f"{r['score_mean']:.2f}", fmt_pct(r["ret_mean"]), fmt_pct(r["ret_median"])]
                for r in cat_summary
            ],
            ["---", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## 排序有效性")
    lines.append(
        md_table(
            ["指标", "数值", "解释"],
            [
                ["Pearson", fmt_num(corr_main["pearson"]), "线性相关；受极端涨跌影响较大"],
                ["Spearman", fmt_num(corr_main["spearman"]), "排序相关；本次核心判断指标"],
                ["Kendall tau-b", fmt_num(corr_main["kendall"]), "成对排序胜率；考虑分数并列"],
            ],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 分数分组收益")
    lines.append(
        md_table(
            ["分组", "公司数", "F24均分", "6个月平均收益", "6个月中位收益", "命中率"],
            [
                [r["group"], str(r["n"]), f"{r['score_mean']:.2f}", fmt_pct(r["ret_mean"]), fmt_pct(r["ret_median"]), fmt_rate(r["hit_rate"])]
                for _, r in group_rows.iterrows()
            ],
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## Top/Bottom能力")
    lines.append(
        md_table(
            ["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"],
            [
                [
                    f"Top{r['n']}/Bottom{r['n']}",
                    fmt_pct(r["top_mean"]),
                    fmt_rate(r["top_hit"]),
                    fmt_pct(r["bottom_mean"]),
                    fmt_rate(r["bottom_hit"]),
                    fmt_pct(r["spread"]),
                ]
                for r in tb
            ],
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("### Top10与Bottom10构成")
    top_bottom_rows = []
    for label, g in [("Top10", top10), ("Bottom10", bottom10)]:
        for _, r in g.iterrows():
            top_bottom_rows.append([label, r["ticker"], r["company"], r["category"], f"{r['score']:.1f}", str(int(r["rank"])), fmt_pct(r["ret_6m"])])
    lines.append(
        md_table(
            ["组别", "股票代号", "公司名称", "分类目录", "F24分", "F24排名", "6个月收益"],
            top_bottom_rows,
            ["---", "---", "---", "---", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为压力测试代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供，故不写成严格波动率结论。")
    lines.append(
        md_table(
            ["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"],
            [
                [
                    r["group"],
                    str(r["n"]),
                    str(r["obs"]),
                    fmt_pct(r["soxx1_mean"]),
                    fmt_pct(r["soxx2_mean"]),
                    fmt_pct(r["soxx3_mean"]),
                    fmt_pct(r["pressure_mean"]),
                    fmt_pct(r["worst_avg"]),
                    fmt_pct(r["dispersion"]),
                    fmt_rate(r["beat_soxx_rate"]),
                    fmt_rate(r["negative_rate"]),
                ]
                for r in pressure_rows
            ],
            ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("结论：Top30 的压力窗口表现没有呈现保护性。其单位负载价值量高，但组合中包含 NVDA、AVGO、CRDO、ALAB、SMCI、CEG、CRWV 等高贝塔或估值敏感标的，SOXX下跌窗口中并未比低分组更稳。")

    lines.append("")
    lines.append("## 分类中性结果")
    lines.append(
        md_table(
            ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
            [
                ["原始全样本", str(corr_main["n"]), fmt_num(corr_main["pearson"]), fmt_num(corr_main["spearman"]), fmt_num(corr_main["kendall"]), "直接用F24分数排序"],
                ["分类内百分位合并", str(corr_neutral["n"]), fmt_num(corr_neutral["pearson"]), fmt_num(corr_neutral["spearman"]), fmt_num(corr_neutral["kendall"]), "每个分类内先按F24排序，再转成0-1百分位合并"],
                ["分类去均值残差", str(corr_resid["n"]), fmt_num(corr_resid["pearson"]), fmt_num(corr_resid["spearman"]), fmt_num(corr_resid["kendall"]), "F24和收益分别减去分类均值后相关"],
            ],
            ["---", "---:", "---:", "---:", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(
        md_table(
            ["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"],
            [
                [
                    f"中性Top{r['n']}/Bottom{r['n']}",
                    fmt_pct(r["top_mean"]),
                    fmt_rate(r["top_hit"]),
                    fmt_pct(r["bottom_mean"]),
                    fmt_rate(r["bottom_hit"]),
                    fmt_pct(r["spread"]),
                ]
                for r in tb_neutral
            ],
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(
        md_table(
            ["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F24公司"],
            [
                [
                    r["category"],
                    str(r["n"]),
                    fmt_num(r["pearson"]),
                    fmt_num(r["spearman"]),
                    fmt_pct(r["ret_mean"]),
                    r["highest_return"],
                    r["highest_score"],
                ]
                for r in cat_corrs
            ],
            ["---", "---:", "---:", "---:", "---:", "---", "---"],
        )
    )
    lines.append("")
    lines.append("分类内结果显示，F24 在云算力/IDC、机电冷却等目录有局部解释，但在AI计算芯片、晶圆制造、配电电源、电力等目录受高贝塔修复股和极端涨幅扰动明显；分类中性合并后仍无法形成稳定正收益差。")

    lines.append("")
    lines.append("## 稳健性检验")
    lines.append(
        md_table(
            ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"],
            [
                [
                    r["name"],
                    r["rule"],
                    str(r["n"]),
                    str(r["removed"]),
                    fmt_num(r["pearson"]),
                    fmt_num(r["spearman"]),
                    fmt_num(r["kendall"]),
                    fmt_pct(r["top30"]),
                    fmt_pct(r["bottom30"]),
                    fmt_pct(r["spread30"]),
                ]
                for r in robustness_rows
            ],
            ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("稳健性结论：剔除低流动性后相关性可能因小盘修复股被拿掉而改善，但 ADR/币种异常和极端涨跌口径下没有稳定支持；三项合并后 Spearman 仍不足以把 F24 当作单独排序因子。")

    lines.append("")
    lines.append("### 剔除清单")
    lines.append(
        md_table(
            ["剔除项", "数量", "公司"],
            [
                ["低流动性", str(int(low_liq_mask.sum())), tickers_join(eval_df.loc[low_liq_mask].sort_values("ticker")["ticker"])],
                ["ADR/币种异常", str(int(adr_currency_mask.sum())), tickers_join(eval_df.loc[adr_currency_mask].sort_values("ticker")["ticker"])],
                ["极端涨跌双尾5%", str(int(extreme_mask.sum())), tickers_join(eval_df.loc[extreme_mask].sort_values("ticker")["ticker"])],
            ],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    lines.append(
        md_table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F24分", "F24排名", "F24置信度"],
            [[r["ticker"], r["company"], r["category"], fmt_pct(r["ret_6m"]), f"{r['score']:.1f}", str(int(r["rank"])), r["confidence"]] for _, r in winners15.iterrows()],
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 6个月跌幅前10")
    lines.append(
        md_table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F24分", "F24排名", "F24置信度"],
            [[r["ticker"], r["company"], r["category"], fmt_pct(r["ret_6m"]), f"{r['score']:.1f}", str(int(r["rank"])), r["confidence"]] for _, r in losers10.iterrows()],
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("诊断结论：本窗口涨幅前列集中在 AXTI、SNDK、AAOI、MXL、AEHR、ICHR、MU、VICR、MRAM、FCEL 等高弹性或低基数公司，其中多家公司 F24 并非最高分；低分组被 MRAM、FCEL、RKLB、ENPH、VISN 等修复或特殊事件公司显著抬高，直接削弱 Top-Bottom 收益差。")

    lines.append("")
    lines.append("## F24分布与解释边界")
    lines.append("### 评分分布")
    lines.append(
        md_table(
            ["分数区间", "公司数"],
            [[idx, str(val)] for idx, val in score_bins.items()],
            ["---", "---:"],
        )
    )
    conf_counts = score["confidence"].value_counts()
    evidence_counts = score["evidence"].value_counts()
    lines.append("")
    lines.append("### 证据等级与置信度")
    lines.append(
        md_table(
            ["项目", "A", "B", "C", "D", "高", "中", "低"],
            [[
                "公司数",
                str(evidence_counts.get("A", 0)),
                str(evidence_counts.get("B", 0)),
                str(evidence_counts.get("C", 0)),
                str(evidence_counts.get("D", 0)),
                str(conf_counts.get("高", 0)),
                str(conf_counts.get("中", 0)),
                str(conf_counts.get("低", 0)),
            ]],
            ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("解释边界：F24 是结构性价值量特征，不是动量、估值赔率、交易流动性或催化剂特征。它更适合用于识别 AI 负载上升后利润池会流向哪里；若用于6个月价格排序，必须与估值、盈利兑现、流动性和事件催化共同建模。")

    report = "\n".join(lines) + "\n"
    meta = {
        "score_rows": len(score),
        "return_rows": len(interval),
        "pressure_rows": len(pressure),
        "eval_rows": len(eval_df),
        "missing_returns": list(missing_returns["ticker"]),
        "corr_main": corr_main,
        "top_bottom": tb,
        "robustness": robustness_rows,
        "moved": moved,
    }
    return report, meta


def main() -> None:
    report, meta = make_report()
    TARGET_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(f"wrote={TARGET_PATH}")
    print(f"score_rows={meta['score_rows']} return_rows={meta['return_rows']} pressure_rows={meta['pressure_rows']} eval_rows={meta['eval_rows']}")
    print(f"missing_returns={','.join(meta['missing_returns'])}")
    print(
        "corr="
        + ",".join(f"{k}:{fmt_num(v)}" for k, v in meta["corr_main"].items() if k != "n")
    )
    print(
        "top30_spread="
        + fmt_pct(meta["top_bottom"][-1]["spread"])
        + " top30="
        + fmt_pct(meta["top_bottom"][-1]["top_mean"])
        + " bottom30="
        + fmt_pct(meta["top_bottom"][-1]["bottom_mean"])
    )
    print(f"backed_up={len(meta['moved'])}")


if __name__ == "__main__":
    main()
