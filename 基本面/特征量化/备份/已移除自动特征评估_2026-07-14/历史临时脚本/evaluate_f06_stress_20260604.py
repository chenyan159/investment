from __future__ import annotations

import math
import re
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
FEATURE_ID = "F06"
FEATURE_NAME = "同业历史估值分位"
FEATURE_SUBJECT = f"{FEATURE_ID}_{FEATURE_NAME}"
RUN_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_SUBJECT}_量化评分_{RUN_DATE}.md"
STRESS_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md"
LIQUIDITY_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
FINANCIAL_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUT_DIR / "备份"
OUT_PATH = OUT_DIR / f"{FEATURE_SUBJECT}_特征评估_三段SOXX下跌区间涨跌_{RUN_DATE}.md"

SOXX_CUM = -62.20
SOXX_WINDOWS = {
    "stress1": ("SOXX下跌1：2025-02-20至2025-04-08", -32.98),
    "stress2": ("SOXX下跌2：2026-02-25至2026-03-30", -15.82),
    "stress3": ("SOXX下跌3：2025-10-29至2025-11-20", -13.40),
}
CATEGORY_ORDER = [
    "AI服务器_存储_EMS",
    "AI网络_光互联_连接器",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "云算力_IDC_AI软件平台",
    "半导体材料_化学品_基板",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
    "机电_冷却_工程_水处理_边缘工业AI",
    "电力_发电_能源_储能",
    "配电_电源_功率器件",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def parse_percent(cell: str) -> float | None:
    if not cell or "N/A" in cell or "缺失" in cell:
        return None
    match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%", cell.replace(",", ""))
    return float(match.group(1)) if match else None


def clean(cell: str) -> str:
    return re.sub(r"\s+", " ", str(cell).replace("<br>", " / ")).strip()


def parse_score_table(path: Path) -> pd.DataFrame:
    rows: list[dict] = []
    in_table = False
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if stripped == "## 全公司排序表":
            in_table = True
            continue
        if in_table and stripped.startswith("## "):
            break
        if not in_table or not stripped.startswith("|"):
            continue
        cells = split_md_row(stripped)
        if is_separator(cells) or not cells or cells[0] == "排名" or len(cells) < 10 or not cells[0].isdigit():
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
                "deduction": clean(cells[8]),
                "follow_up": clean(cells[9]),
            }
        )
    return pd.DataFrame(rows)


def parse_stress_returns(path: Path) -> pd.DataFrame:
    rows: list[dict] = []
    in_section = False
    category: str | None = None
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if stripped == "## 全公司明细":
            in_section = True
            continue
        if not in_section:
            continue
        if stripped.startswith("## ") and stripped != "## 全公司明细":
            break
        if stripped.startswith("### "):
            category = stripped[4:].strip()
            continue
        if not stripped.startswith("|") or category is None:
            continue
        cells = split_md_row(stripped)
        if is_separator(cells) or not cells or cells[0] == "股票代号" or len(cells) < 7:
            continue
        rows.append(
            {
                "ticker": cells[0],
                "return_company": cells[1],
                "return_category": category,
                "stress1": parse_percent(cells[2]),
                "stress2": parse_percent(cells[3]),
                "stress3": parse_percent(cells[4]),
                "cum_return": parse_percent(cells[5]),
                "return_note": clean(cells[6]),
            }
        )
    return pd.DataFrame(rows)


def parse_financial_details(path: Path) -> pd.DataFrame:
    rows: list[dict] = []
    in_section = False
    category: str | None = None
    header: list[str] | None = None
    for line in read_text(path).splitlines():
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
        call_iv = parse_percent(row.get("Call IV", ""))
        put_iv = parse_percent(row.get("Put IV", ""))
        iv_values = [value for value in [call_iv, put_iv] if value is not None]
        rows.append(
            {
                "ticker": row.get("股票代号", ""),
                "financial_category": category,
                "currency": row.get("currency", ""),
                "financial_currency": row.get("financial_currency", ""),
                "listing_type": row.get("listing_type", ""),
                "adr_ratio": row.get("adr_ratio", ""),
                "valuation_check": row.get("估值校验", ""),
                "financial_note": clean(row.get("备注", "")),
                "iv_avg": sum(iv_values) / len(iv_values) if iv_values else None,
            }
        )
    return pd.DataFrame(rows)


def rank_average(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
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
    x_values, y_values = zip(*pairs)
    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in pairs)
    x_den = math.sqrt(sum((x - x_mean) ** 2 for x in x_values))
    y_den = math.sqrt(sum((y - y_mean) ** 2 for y in y_values))
    return numerator / (x_den * y_den) if x_den and y_den else float("nan")


def spearman(xs: list[float], ys: list[float]) -> float:
    pairs = [(float(x), float(y)) for x, y in zip(xs, ys) if pd.notna(x) and pd.notna(y)]
    if len(pairs) < 2:
        return float("nan")
    x_values, y_values = zip(*pairs)
    return pearson(rank_average(list(x_values)), rank_average(list(y_values)))


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
    denominator = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    return (concordant - discordant) / denominator if denominator else float("nan")


def correlations(df: pd.DataFrame, score_col: str, return_col: str) -> dict[str, float]:
    sub = df[[score_col, return_col]].dropna()
    xs = sub[score_col].astype(float).tolist()
    ys = sub[return_col].astype(float).tolist()
    return {
        "n": len(sub),
        "pearson": pearson(xs, ys),
        "spearman": spearman(xs, ys),
        "kendall": kendall_tau_b(xs, ys),
    }


def pct(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:+.2f}%"


def rate(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.1f}%"


def one_decimal(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.1f}"


def num(value: float | None, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.{digits}f}"


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def md_table(headers: list[str], rows: list[list[object]], aligns: list[str] | None = None) -> str:
    aligns = aligns or ["---"] * len(headers)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(aligns) + " |"]
    out.extend("| " + " | ".join(md_escape(cell) for cell in row) + " |" for row in rows)
    return "\n".join(out)


def top_bottom_stats(df: pd.DataFrame, n: int, neutral: bool = False) -> dict[str, float]:
    if neutral:
        top = df.sort_values(["cat_score_pct", "score_rank"], ascending=[False, True]).head(n)
        bottom = df.sort_values(["cat_score_pct", "score_rank"], ascending=[True, False]).head(n)
    else:
        top = df.sort_values("score_rank", ascending=True).head(n)
        bottom = df.sort_values("score_rank", ascending=False).head(n)
    return {
        "top_mean": top["cum_return"].mean(),
        "top_median": top["cum_return"].median(),
        "top_hit": (top["cum_return"] > SOXX_CUM).mean() * 100,
        "top_positive": (top["cum_return"] > 0).mean() * 100,
        "bottom_mean": bottom["cum_return"].mean(),
        "bottom_median": bottom["cum_return"].median(),
        "bottom_hit": (bottom["cum_return"] > SOXX_CUM).mean() * 100,
        "bottom_positive": (bottom["cum_return"] > 0).mean() * 100,
        "spread": top["cum_return"].mean() - bottom["cum_return"].mean(),
    }


def split_score_quintiles(df: pd.DataFrame) -> list[tuple[str, pd.DataFrame]]:
    ordered = df.sort_values("score_rank", ascending=True).reset_index(drop=True)
    n = len(ordered)
    base = n // 5
    remainder = n % 5
    sizes = [base + (1 if i < remainder else 0) for i in range(5)]
    labels = ["Q1最高分", "Q2", "Q3", "Q4", "Q5最低分"]
    groups: list[tuple[str, pd.DataFrame]] = []
    start = 0
    for label, size in zip(labels, sizes):
        groups.append((label, ordered.iloc[start : start + size].copy()))
        start += size
    return groups


def category_percentiles(df: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    for _, group in df.groupby("category", sort=False):
        group = group.copy()
        n = len(group)
        if n == 1:
            group["cat_score_pct"] = 1.0
        else:
            ranks = rank_average((-group["score"]).astype(float).tolist())
            group["cat_score_pct"] = [(n - rank) / (n - 1) for rank in ranks]
        group["score_resid_cat"] = group["score"] - group["score"].mean()
        group["return_resid_cat"] = group["cum_return"] - group["cum_return"].mean()
        pieces.append(group)
    return pd.concat(pieces, ignore_index=True)


def stress_group_stats(df: pd.DataFrame, label: str) -> dict[str, float | str]:
    all_values: list[float] = []
    worst_values: list[float] = []
    per_company_std: list[float] = []
    outperf = total = negative = 0
    for _, row in df.iterrows():
        company_values = []
        for key, (_, soxx_return) in SOXX_WINDOWS.items():
            value = row.get(key)
            if pd.notna(value):
                value = float(value)
                company_values.append(value)
                all_values.append(value)
                total += 1
                outperf += value > soxx_return
                negative += value < 0
        if company_values:
            worst_values.append(min(company_values))
            if len(company_values) >= 2:
                mean_value = sum(company_values) / len(company_values)
                per_company_std.append(math.sqrt(sum((v - mean_value) ** 2 for v in company_values) / (len(company_values) - 1)))
    return {
        "label": label,
        "n": len(df),
        "obs": total,
        "stress1_mean": df["stress1"].dropna().mean(),
        "stress2_mean": df["stress2"].dropna().mean(),
        "stress3_mean": df["stress3"].dropna().mean(),
        "cum_mean": df["cum_return"].dropna().mean(),
        "window_mean": sum(all_values) / len(all_values) if all_values else float("nan"),
        "worst_mean": sum(worst_values) / len(worst_values) if worst_values else float("nan"),
        "dispersion": sum(per_company_std) / len(per_company_std) if per_company_std else float("nan"),
        "outperform_window": outperf / total * 100 if total else float("nan"),
        "outperform_cum": (df["cum_return"] > SOXX_CUM).mean() * 100,
        "negative_window": negative / total * 100 if total else float("nan"),
        "iv_mean": df["iv_avg"].dropna().mean(),
        "iv_n": int(df["iv_avg"].notna().sum()),
    }


def sample_robustness(df: pd.DataFrame, label: str, rule: str, mask: pd.Series) -> dict[str, float | str]:
    sample = df[mask].copy().sort_values("score_rank")
    c = correlations(sample, "score", "cum_return")
    top = sample.head(min(30, len(sample)))
    bottom = sample.tail(min(30, len(sample)))
    return {
        "label": label,
        "rule": rule,
        "n": len(sample),
        "excluded": len(df) - len(sample),
        "pearson": c["pearson"],
        "spearman": c["spearman"],
        "kendall": c["kendall"],
        "top30": top["cum_return"].mean(),
        "bottom30": bottom["cum_return"].mean(),
        "spread": top["cum_return"].mean() - bottom["cum_return"].mean(),
        "hit_spread": (top["cum_return"] > SOXX_CUM).mean() * 100 - (bottom["cum_return"] > SOXX_CUM).mean() * 100,
    }


def extract_meta(text: str, pattern: str, default: str = "未解析") -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else default


def row_company(row: pd.Series) -> list[object]:
    return [
        row["ticker"],
        row["company"],
        row["category"],
        pct(row["cum_return"]),
        pct(row["stress1"]),
        pct(row["stress2"]),
        pct(row["stress3"]),
        one_decimal(row["score"]),
        str(int(row["score_rank"])),
        row["confidence"],
    ]


def backup_existing_output() -> list[str]:
    if not OUT_PATH.exists():
        return []
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target_dir = BACKUP_DIR / f"F06_同业历史估值分位_三段SOXX下跌区间涨跌_写入前备份_{stamp}"
    target_dir.mkdir(parents=True, exist_ok=True)
    dst = target_dir / OUT_PATH.name
    shutil.copy2(OUT_PATH, dst)
    return [str(dst.relative_to(ROOT))]


def build_report() -> tuple[str, dict[str, object]]:
    score_df = parse_score_table(SCORE_PATH)
    stress_df = parse_stress_returns(STRESS_PATH)
    liquidity_df = parse_score_table(LIQUIDITY_PATH)[["ticker", "score"]].rename(columns={"score": "liquidity_score"})
    financial_df = parse_financial_details(FINANCIAL_PATH)

    joined = (
        score_df.merge(stress_df, on="ticker", how="left")
        .merge(liquidity_df, on="ticker", how="left")
        .merge(financial_df, on="ticker", how="left")
    )
    valid = joined[joined["cum_return"].notna()].copy().sort_values("score_rank").reset_index(drop=True)
    valid["category"] = pd.Categorical(valid["category"], categories=CATEGORY_ORDER, ordered=True)
    valid = valid.sort_values("score_rank").reset_index(drop=True)
    neutral = category_percentiles(valid)

    missing_returns = sorted(set(score_df["ticker"]) - set(valid["ticker"]))
    missing_scores = sorted(set(valid["ticker"]) - set(score_df["ticker"]))

    stress_generation = extract_meta(read_text(STRESS_PATH), r"生成时间：([^。]+)。")
    financial_generation = extract_meta(read_text(FINANCIAL_PATH), r"生成时间：([^\n]+)")

    main_corr = correlations(valid, "score", "cum_return")
    window_corrs = {key: correlations(valid, "score", key) for key in ["stress1", "stress2", "stress3"]}
    neutral_raw = correlations(neutral, "score", "cum_return")
    neutral_pct = correlations(neutral, "cat_score_pct", "cum_return")
    neutral_resid = correlations(neutral, "score_resid_cat", "return_resid_cat")

    tb_stats = {n: top_bottom_stats(valid, n) for n in [10, 20, 30]}
    neutral_tb_stats = {n: top_bottom_stats(neutral, n, neutral=True) for n in [10, 20, 30]}
    ordered = valid.sort_values("score_rank", ascending=True).reset_index(drop=True)
    mid_start = max(0, (len(ordered) - 30) // 2)
    risk_groups = [
        stress_group_stats(ordered.head(30), "F06 Top30"),
        stress_group_stats(ordered.iloc[mid_start : mid_start + 30], "F06 Mid30"),
        stress_group_stats(ordered.tail(30), "F06 Bottom30"),
    ]

    category_rows = []
    category_corr_rows = []
    for category in CATEGORY_ORDER:
        group = valid[valid["category"] == category]
        if group.empty:
            continue
        c = correlations(group, "score", "cum_return")
        winner = group.sort_values("cum_return", ascending=False).iloc[0]
        loser = group.sort_values("cum_return", ascending=True).iloc[0]
        top_score = group.sort_values("score_rank", ascending=True).iloc[0]
        category_rows.append(
            [
                category,
                str(len(group)),
                one_decimal(group["score"].mean()),
                pct(group["cum_return"].mean()),
                pct(group["cum_return"].median()),
                rate((group["cum_return"] > SOXX_CUM).mean() * 100),
            ]
        )
        category_corr_rows.append(
            [
                category,
                str(len(group)),
                num(c["pearson"], 3),
                num(c["spearman"], 3),
                num(c["kendall"], 3),
                pct(group["cum_return"].mean()),
                rate((group["cum_return"] > SOXX_CUM).mean() * 100),
                f"{winner['ticker']} {pct(winner['cum_return'])}",
                f"{loser['ticker']} {pct(loser['cum_return'])}",
                f"{top_score['ticker']} {one_decimal(top_score['score'])} / {pct(top_score['cum_return'])}",
            ]
        )

    corr_rows = [
        ["三段累计涨跌幅", str(main_corr["n"]), num(main_corr["pearson"], 3), num(main_corr["spearman"], 3), num(main_corr["kendall"], 3), "核心目标；三段百分比简单相加，越高越好"],
    ]
    for key, (label, soxx_return) in SOXX_WINDOWS.items():
        c = window_corrs[key]
        corr_rows.append([label, str(c["n"]), num(c["pearson"], 3), num(c["spearman"], 3), num(c["kendall"], 3), f"单个压力窗口，SOXX {pct(soxx_return)}"])

    quintile_rows = []
    for label, group in split_score_quintiles(valid):
        worst_window = group[["stress1", "stress2", "stress3"]].min(axis=1, skipna=True)
        quintile_rows.append(
            [
                label,
                str(len(group)),
                one_decimal(group["score"].mean()),
                pct(group["cum_return"].mean()),
                pct(group["cum_return"].median()),
                rate((group["cum_return"] > SOXX_CUM).mean() * 100),
                pct(worst_window.mean()),
                pct(group["iv_avg"].dropna().mean()),
                str(int(group["iv_avg"].notna().sum())),
            ]
        )

    tb_rows = []
    for n, stats in tb_stats.items():
        tb_rows.append(
            [
                f"Top{n}/Bottom{n}",
                pct(stats["top_mean"]),
                pct(stats["top_median"]),
                rate(stats["top_hit"]),
                rate(stats["top_positive"]),
                pct(stats["bottom_mean"]),
                pct(stats["bottom_median"]),
                rate(stats["bottom_hit"]),
                rate(stats["bottom_positive"]),
                pct(stats["spread"]),
            ]
        )

    tb_detail_rows = []
    for label, sub in [("Top10", ordered.head(10)), ("Bottom10", ordered.tail(10).sort_values("score_rank", ascending=False))]:
        for _, row in sub.iterrows():
            tb_detail_rows.append(
                [
                    label,
                    row["ticker"],
                    row["company"],
                    row["category"],
                    one_decimal(row["score"]),
                    str(int(row["score_rank"])),
                    pct(row["cum_return"]),
                    pct(row["stress1"]),
                    pct(row["stress2"]),
                    pct(row["stress3"]),
                    row["confidence"],
                ]
            )

    risk_rows = []
    for row in risk_groups:
        risk_rows.append(
            [
                row["label"],
                str(row["n"]),
                str(row["obs"]),
                pct(row["stress1_mean"]),
                pct(row["stress2_mean"]),
                pct(row["stress3_mean"]),
                pct(row["cum_mean"]),
                pct(row["window_mean"]),
                pct(row["worst_mean"]),
                pct(row["dispersion"]),
                rate(row["outperform_window"]),
                rate(row["outperform_cum"]),
                rate(row["negative_window"]),
                pct(row["iv_mean"]),
                str(row["iv_n"]),
            ]
        )

    neutral_corr_rows = [
        ["原始全样本", str(neutral_raw["n"]), num(neutral_raw["pearson"], 3), num(neutral_raw["spearman"], 3), num(neutral_raw["kendall"], 3), "直接用F06原始分数排序"],
        ["分类内百分位合并", str(neutral_pct["n"]), num(neutral_pct["pearson"], 3), num(neutral_pct["spearman"], 3), num(neutral_pct["kendall"], 3), "每个分类内先按F06排序，再转为0-1百分位后合并"],
        ["分类去均值残差", str(neutral_resid["n"]), num(neutral_resid["pearson"], 3), num(neutral_resid["spearman"], 3), num(neutral_resid["kendall"], 3), "F06和累计收益分别减去分类均值后相关"],
    ]
    neutral_tb_rows = []
    for n, stats in neutral_tb_stats.items():
        neutral_tb_rows.append([f"中性Top{n}/Bottom{n}", pct(stats["top_mean"]), rate(stats["top_hit"]), pct(stats["bottom_mean"]), rate(stats["bottom_hit"]), pct(stats["spread"])])

    valid["low_liquidity"] = valid["liquidity_score"].fillna(-999) <= 5.0
    valid["adr_currency_abnormal"] = (
        (valid["listing_type"].fillna("") != "common/equity")
        | (valid["adr_ratio"].fillna("") != "不适用")
        | (valid["currency"].fillna("") != valid["financial_currency"].fillna(""))
        | valid["valuation_check"].fillna("").str.contains("currency_mismatch", regex=False)
    )
    low_q = valid["cum_return"].quantile(0.05)
    high_q = valid["cum_return"].quantile(0.95)
    valid["extreme_return"] = (valid["cum_return"] < low_q) | (valid["cum_return"] > high_q)

    robustness_data = [
        sample_robustness(valid, "全样本基准", "无剔除", pd.Series([True] * len(valid), index=valid.index)),
        sample_robustness(valid, "剔除低流动性", "F51交易流动性分 > 5.0", ~valid["low_liquidity"]),
        sample_robustness(valid, "剔除ADR/币种异常", "listing_type=common/equity、ADR比例不适用、交易/财报货币一致、估值校验无currency_mismatch", ~valid["adr_currency_abnormal"]),
        sample_robustness(valid, "剔除极端涨跌", f"剔除三段累计涨跌双尾5%；阈值 {pct(low_q)} / {pct(high_q)}", ~valid["extreme_return"]),
        sample_robustness(valid, "三项合并剔除", "同时满足上述三项", ~(valid["low_liquidity"] | valid["adr_currency_abnormal"] | valid["extreme_return"])),
    ]
    robustness_rows = []
    for row in robustness_data:
        robustness_rows.append(
            [
                row["label"],
                row["rule"],
                str(row["n"]),
                str(row["excluded"]),
                num(row["pearson"], 3),
                num(row["spearman"], 3),
                num(row["kendall"], 3),
                pct(row["top30"]),
                pct(row["bottom30"]),
                pct(row["spread"]),
                pct(row["hit_spread"]),
            ]
        )

    exclusion_rows = []
    for label, column in [("低流动性", "low_liquidity"), ("ADR/币种异常", "adr_currency_abnormal"), ("极端涨跌双尾5%", "extreme_return")]:
        tickers = sorted(valid.loc[valid[column], "ticker"].tolist())
        exclusion_rows.append([label, str(len(tickers)), ", ".join(tickers) if tickers else "无"])

    best_rows = [row_company(row) for _, row in valid.sort_values("cum_return", ascending=False).head(15).iterrows()]
    worst_rows = [row_company(row) for _, row in valid.sort_values("cum_return", ascending=True).head(15).iterrows()]
    high_bad_rows = [
        row_company(row)
        for _, row in valid[(valid["score"] >= 7.0) & (valid["cum_return"] < SOXX_CUM)]
        .sort_values("cum_return", ascending=True)
        .head(12)
        .iterrows()
    ]
    high_good_rows = [
        row_company(row)
        for _, row in valid[(valid["score"] >= 7.0) & (valid["cum_return"] > SOXX_CUM)]
        .sort_values("cum_return", ascending=False)
        .head(12)
        .iterrows()
    ]
    low_good_rows = [
        row_company(row)
        for _, row in valid[(valid["score"] <= 3.0) & (valid["cum_return"] > SOXX_CUM)]
        .sort_values("cum_return", ascending=False)
        .head(12)
        .iterrows()
    ]

    moved_backups = backup_existing_output()
    old_output_note = "未发现同名旧版正式输出。" if not moved_backups else "写入前已复制备份：" + "；".join(f"`{p}`" for p in moved_backups)

    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 三段SOXX下跌区间涨跌 {RUN_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.append(f"- 评估对象：`{FEATURE_SUBJECT}`。")
    lines.append(f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 2026-06-04，覆盖 {len(score_df)} 家。")
    lines.append(f"- 收益输入：`日度资料/区间涨跌/{STRESS_PATH.name}`，生成时间 {stress_generation}；价格口径为 Yahoo Finance `Close`，不含股息再投资。")
    lines.append("- SOXX压力窗口：2025-02-20至2025-04-08 下跌 -32.98%；2026-02-25至2026-03-30 下跌 -15.82%；2025-10-29至2025-11-20 下跌 -13.40%。SOXX三段累计涨跌幅为 -62.20%。")
    lines.append(f"- 稳健性辅助输入：`特征量化/量化评分/{LIQUIDITY_PATH.name}`；`日度资料/每日金融数据/{FINANCIAL_PATH.name}`，金融数据生成时间 {financial_generation}。")
    lines.append(f"- 有效评估样本：评分与三段累计涨跌幅交集 {len(valid)} 家；{FEATURE_ID}评分有但累计涨跌缺失 {len(missing_returns)} 家：{', '.join(missing_returns) if missing_returns else '无'}。")
    lines.append("- 收益方向口径：三段累计涨跌幅越高越好；在压力窗口中，跌幅更小、或上涨，均视为更优表现。")
    lines.append("- 命中率口径：三段累计涨跌幅大于 SOXX 三段累计涨跌幅 `-62.20%` 记为压力命中；Top-Bottom收益差=高分组合平均三段累计收益 - 低分组合平均三段累计收益。")
    lines.append("- 风险口径限制：本次输入是三个固定压力区间收益，不是逐日收益序列；因此本报告不写成严格日度波动率、完整最大回撤或真实下跌日收益稳定性结论，而使用三个SOXX下跌窗口均值、平均最差窗口、窗口离散度、跑赢SOXX比例、负收益窗口占比，并用 2026-06-03 近ATM Call/Put IV均值补充当前波动代理。")
    lines.append("- 稳健性口径：低流动性使用 `F51<=5.0` 或F51缺失作为剔除代理；ADR/币种异常使用每日金融数据中的 `listing_type`、ADR比例、交易/财报货币和 `currency_mismatch` 标记；极端涨跌按本次三段累计收益双尾5%剔除。")
    lines.append(f"- 旧版处理：{old_output_note}")
    lines.append("")
    lines.append("## 结论摘要")
    lines.append(f"- 排序有效性：弱到中等正向。全样本 Pearson {num(main_corr['pearson'], 3)}，Spearman {num(main_corr['spearman'], 3)}，Kendall {num(main_corr['kendall'], 3)}；重点指标 Spearman 为正，但绝对值低于 0.3，说明 F06 对压力期收益有排序信息，但不是强单因子。")
    lines.append(f"- 分窗口观察：SOXX下跌1/2/3 的 Spearman 分别为 {num(window_corrs['stress1']['spearman'], 3)}、{num(window_corrs['stress2']['spearman'], 3)}、{num(window_corrs['stress3']['spearman'], 3)}；第二段较弱，第一段和第三段更能体现估值缓冲。")
    lines.append(f"- Top/Bottom能力：成立但强度不均。Top10、Top20、Top30 平均累计收益分别为 {pct(tb_stats[10]['top_mean'])}、{pct(tb_stats[20]['top_mean'])}、{pct(tb_stats[30]['top_mean'])}；对应Top-Bottom收益差为 {pct(tb_stats[10]['spread'])}、{pct(tb_stats[20]['spread'])}、{pct(tb_stats[30]['spread'])}。Top20差距收窄，主要因为高分端混入 PSIX、SMCI 等压力期大跌样本。")
    lines.append(f"- 风险解释力：较明确。F06 Top30 三段累计均值 {pct(risk_groups[0]['cum_mean'])}、平均最差窗口 {pct(risk_groups[0]['worst_mean'])}、窗口离散度 {pct(risk_groups[0]['dispersion'])}、当前IV均值 {pct(risk_groups[0]['iv_mean'])}；Bottom30 对应为 {pct(risk_groups[2]['cum_mean'])}、{pct(risk_groups[2]['worst_mean'])}、{pct(risk_groups[2]['dispersion'])}、{pct(risk_groups[2]['iv_mean'])}。高分组在固定压力窗口中更抗跌、当前波动代理也更低。")
    lines.append(f"- 分类中性：仍有效。分类内百分位合并 Spearman {num(neutral_pct['spearman'], 3)}，分类去均值残差 Spearman {num(neutral_resid['spearman'], 3)}；中性Top30-Bottom30收益差 {pct(neutral_tb_stats[30]['spread'])}。这说明结果不是单纯押中某个分类目录。")
    lines.append(f"- 稳健性：结论保持。剔除低流动性后 Spearman {num(robustness_data[1]['spearman'], 3)}，剔除ADR/币种异常后 {num(robustness_data[2]['spearman'], 3)}，剔除极端涨跌后 {num(robustness_data[3]['spearman'], 3)}，三项合并后 {num(robustness_data[4]['spearman'], 3)}；三项合并后 Top30-Bottom30仍为 {pct(robustness_data[4]['spread'])}。")
    lines.append("- 解释：F06 高分代表相对同业/可得历史证据更便宜，压力期往往对应更低估值压缩和更低当前IV；但它无法自动排除价值陷阱、财务/会计/个股事件和高beta周期修复。PSIX、SMCI、UCTT 是高分端的主要反例；AXTI、TSEM、LWLG、IMOS 等低分端跑赢样本提示事件驱动、低流动性和单窗口反弹仍会干扰单因子。")
    lines.append("- 使用建议：F06 可以作为 SOXX 压力窗口中的估值缓冲和风险预算因子使用，适合与 F08财务承压可控性、F41负向预期差风险可控性、F45执行风险可控性、F50价格相对强度和F51交易流动性联用；不宜独立作为买入排序或替代完整基本面判断。")
    lines.append("")
    lines.append("## 覆盖检查")
    lines.append(md_table(["项目", "数量", "说明"], [
        ["F06评分覆盖", str(len(score_df)), "来自2026-06-04评分文件"],
        ["三段累计涨跌覆盖", str(int(stress_df["cum_return"].notna().sum())), "来自2026-06-04三段SOXX下跌区间涨跌文件"],
        ["交集有效样本", str(len(valid)), "用于本报告主指标"],
        ["评分有但累计涨跌缺失", str(len(missing_returns)), ", ".join(missing_returns) if missing_returns else "无"],
        ["涨跌有但评分缺失", str(len(missing_scores)), ", ".join(missing_scores) if missing_scores else "无"],
    ], ["---", "---:", "---"]))
    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.append(md_table(["分类目录", "样本数", "F06均分", "三段累计平均", "三段累计中位数", "跑赢SOXX累计率"], category_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## 排序有效性")
    lines.append(md_table(["目标收益", "样本数", "Pearson", "Spearman", "Kendall tau-b", "解释"], corr_rows, ["---", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### F06分数分组收益")
    lines.append(md_table(["分组", "公司数", "F06均分", "三段累计平均", "三段累计中位数", "跑赢SOXX累计率", "平均最差窗口", "当前IV均值", "IV样本"], quintile_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("分组结果呈现较清楚的防守梯度：最高分五分位累计均值 -46.12%，最低分五分位 -63.36%；当前IV均值也从最高分组约 52.17% 上升到最低分组约 97.95%。这支持 F06 的风险缓冲含义。但 Q1 与 Q2 接近，且 Q1 内部仍有 PSIX、SMCI 等大跌样本，因此不能把它写成线性强因子。")
    lines.append("")
    lines.append("## Top/Bottom能力")
    lines.append(md_table(["组合", "Top平均累计", "Top中位累计", "Top压力命中率", "Top正收益率", "Bottom平均累计", "Bottom中位累计", "Bottom压力命中率", "Bottom正收益率", "Top-Bottom收益差"], tb_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    lines.append(md_table(["组别", "股票代号", "公司名称", "分类目录", "F06分", "F06排名", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "置信度"], tb_detail_rows, ["---", "---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("Top10 的压力命中率达到 90%，但 PSIX 单只大跌把 Top10 均值拉低；Top20 扩大后又纳入 SMCI、VST、META、UCTT 等高分但高beta或个股风险样本，导致收益差收窄。Bottom端则包含 NBIS、NVTS、SMR、RKLB 等高波动低估值容错公司，整体压力命中率明显更低。")
    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用三个固定SOXX下跌区间作为压力测试代理。严格日度波动率、完整最大回撤、真实下跌日收益稳定性需要逐日价格序列；当前IV均值仅是 2026-06-03 近ATM期权波动代理，不等同于历史实际波动率。")
    lines.append("")
    lines.append(md_table(["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "三段累计均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX窗口比例", "跑赢SOXX累计率", "负收益窗口占比", "当前IV均值", "IV样本"], risk_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("结论：F06 Top30 相比 Bottom30，三段累计少跌 15.78 个百分点，平均最差窗口少跌 11.53 个百分点，跑赢SOXX窗口比例高 30.0 个百分点，当前IV均值低约 48.60 个百分点。负收益窗口占比同为 86.7%，说明高分组并不是不跌，而是在下跌窗口中跌幅更浅、波动代理更低、窗口间表现更稳定。")
    lines.append("")
    lines.append("## 分类中性结果")
    lines.append(md_table(["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"], neutral_corr_rows, ["---", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(md_table(["组合", "Top平均累计", "Top压力命中率", "Bottom平均累计", "Bottom压力命中率", "Top-Bottom收益差"], neutral_tb_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(md_table(["分类目录", "样本数", "Pearson", "Spearman", "Kendall", "类内累计均值", "类内命中率", "类内最好", "类内最差", "类内最高F06公司"], category_corr_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---", "---", "---"]))
    lines.append("")
    lines.append("分类内结果显示，10个目录中除晶圆制造为弱负外，多数目录的 Spearman 为正；机电冷却、AI服务器、封测、电力、配电目录内相关性更明显。分类内百分位和分类残差口径仍保持正相关，因此 F06 的压力期有效性不是简单来自行业配置，而是同目录内便宜/贵的排序本身也带有信息。")
    lines.append("")
    lines.append("## 稳健性检验")
    lines.append(md_table(["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30", "命中率差"], robustness_rows, ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("稳健性结论：低流动性、ADR/币种异常、极端涨跌三类剔除都没有破坏正向排序；三项合并后样本剩 115 家，Spearman 反而升至 +0.344，Top30-Bottom30 仍为 +18.10%。因此，本次 F06 对三段SOXX压力窗口的解释不是由低流动性、跨币种异常或少数极端涨跌单独驱动。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(md_table(["剔除项", "数量", "公司"], exclusion_rows, ["---", "---:", "---"]))
    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 三段累计表现最好15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F06分", "F06排名", "置信度"], best_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 三段累计表现最差15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F06分", "F06排名", "置信度"], worst_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 高F06但压力窗口显著拖累")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F06分", "F06排名", "置信度"], high_bad_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("这些公司说明 F06 的反证条件很重要：估值便宜可能来自周期下行、财务口径异常、会计/订单风险、融资压力或高beta业务暴露。PSIX、SMCI、UCTT、ON、DIOD 等不是因为 F06 方向错，而是说明便宜分不能替代财务承压、执行风险、价格趋势和个股事件过滤。")
    lines.append("")
    lines.append("### 高F06且跑赢SOXX累计的防守样本")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F06分", "F06排名", "置信度"], high_good_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("这组样本体现 F06 最有效的使用场景：低倍数、成熟业务、盈利或现金流可支撑、当前IV不高，且在至少一个 SOXX 压力窗口里能明显跑赢指数。电力公用事业、成熟工业、部分软件/网络和材料公司是主要贡献。")
    lines.append("")
    lines.append("### 低F06但压力期较稳的反例")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F06分", "F06排名", "置信度"], low_good_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("低F06反例主要来自事件驱动、低流动性或单窗口强反弹，例如 AXTI、TSEM、LWLG、IMOS。它们提示：在固定压力窗口里，个股事件和交易结构可以压过估值分位；后续若要做更严格回测，需要用逐日收益、成交额、真实ADV和事件标签进一步拆解。")
    lines.append("")
    lines.append("## 评估结论与使用建议")
    lines.append("- F06 在本次三段SOXX下跌区间中可以作为压力期防守/估值缓冲因子使用：全样本排序、Top/Bottom、风险代理、分类中性和稳健性均给出正向证据。")
    lines.append("- 该因子强度不是高alpha型：核心 Spearman 只有 +0.272，第二段压力窗口 Spearman 仅 +0.129，说明 F06 更适合控制下行和波动，而不是单独捕捉所有压力窗口赢家。")
    lines.append("- 组合层面建议把 F06 作为防守侧约束：高F06可以提高组合估值容错率，但需要叠加 F08财务承压、F41负向预期差、F45执行风险、F50价格相对强度和F51交易流动性，过滤 PSIX、SMCI、UCTT 这类“便宜但压力期仍大跌”的价值陷阱或高beta样本。")
    lines.append("- 对低F06高表现样本不要简单上调 F06 解释力，应另用事件、催化剂、价格动量、空头回补、低流动性和行业轮动因子解释；否则会把估值因子误写成万能防守因子。")
    lines.append("- 后续验证建议：用 2026-06-04 之后的未来压力窗口做前瞻检验，并补充逐日收益序列、真实成交额/ADV和最大回撤，验证 F06 是否仍能解释日度波动率、下跌日收益和组合尾部风险。")
    lines.append("")
    lines.append("## 数据来源路径")
    lines.append(f"- `特征量化/量化评分/{SCORE_PATH.name}`")
    lines.append(f"- `日度资料/区间涨跌/{STRESS_PATH.name}`")
    lines.append(f"- `特征量化/量化评分/{LIQUIDITY_PATH.name}`")
    lines.append(f"- `日度资料/每日金融数据/{FINANCIAL_PATH.name}`")
    lines.append("")

    summary = {
        "score_n": len(score_df),
        "stress_n": len(stress_df),
        "valid_n": len(valid),
        "missing_returns": missing_returns,
        "main_spearman": main_corr["spearman"],
        "top30_spread": tb_stats[30]["spread"],
        "combined_spearman": robustness_data[4]["spearman"],
    }
    return "\n".join(lines), summary


def main() -> None:
    report, summary = build_report()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8")
    print(f"wrote={OUT_PATH}")
    print(
        " ".join(
            [
                f"score_n={summary['score_n']}",
                f"stress_n={summary['stress_n']}",
                f"valid_n={summary['valid_n']}",
                f"missing={','.join(summary['missing_returns'])}",
                f"main_spearman={summary['main_spearman']:.6f}",
                f"top30_spread={summary['top30_spread']:.6f}",
                f"combined_spearman={summary['combined_spearman']:.6f}",
            ]
        )
    )


if __name__ == "__main__":
    main()
