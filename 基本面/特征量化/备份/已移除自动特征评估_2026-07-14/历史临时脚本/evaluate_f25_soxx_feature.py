from __future__ import annotations

import math
import re
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
RUN_DATE = "2026-06-04"
FEATURE_ID = "F25"
FEATURE_NAME = "需求到收入链条清晰度"
FEATURE_KEY = f"{FEATURE_ID}_{FEATURE_NAME}"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_KEY}_量化评分_{RUN_DATE}.md"
STRESS_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md"
LIQUIDITY_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
FINANCIAL_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUT_DIR / "备份"
OUT_PATH = OUT_DIR / f"{FEATURE_KEY}_特征评估_三段SOXX下跌区间涨跌_{RUN_DATE}.md"

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
    return path.read_text(encoding="utf-8-sig")


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def clean(cell: object) -> str:
    return re.sub(r"\s+", " ", str(cell).replace("<br>", " / ")).strip()


def md_escape(value: object) -> str:
    return clean(value).replace("|", "\\|").replace("\n", " ")


def parse_percent(cell: str) -> float | None:
    if not cell or "N/A" in cell or "缺失" in cell or "不适用" in cell:
        return None
    match = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%", cell.replace(",", ""))
    return float(match.group(1)) if match else None


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:+.{digits}f}%"


def fmt_rate(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.1f}%"


def fmt_num(value: float | None, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.{digits}f}"


def fmt_score(value: float | None) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:.1f}"


def md_table(headers: list[str], rows: list[list[object]], aligns: list[str] | None = None) -> str:
    aligns = aligns or ["---"] * len(headers)
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(aligns) + " |",
    ]
    out.extend("| " + " | ".join(md_escape(cell) for cell in row) + " |" for row in rows)
    return "\n".join(out)


def extract_meta(text: str, pattern: str, default: str = "未解析") -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else default


def parse_score_table(path: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
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
        if is_separator(cells) or not cells or cells[0] == "排名" or len(cells) < 7:
            continue
        if not cells[0].isdigit():
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
            }
        )
    return pd.DataFrame(rows)


def parse_stress_returns(path: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    in_details = False
    category: str | None = None
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if stripped == "## 全公司明细":
            in_details = True
            continue
        if in_details and stripped.startswith("## "):
            break
        if not in_details:
            continue
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
    rows: list[dict[str, object]] = []
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
                "call_iv": call_iv,
                "put_iv": put_iv,
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


def top_bottom_stats(df: pd.DataFrame, n: int, neutral: bool = False) -> dict[str, float | pd.DataFrame]:
    if neutral:
        ordered = df.sort_values(["cat_score_pct", "score_rank"], ascending=[False, True])
        reverse = df.sort_values(["cat_score_pct", "score_rank"], ascending=[True, False])
    else:
        ordered = df.sort_values("score_rank", ascending=True)
        reverse = df.sort_values("score_rank", ascending=False)
    top = ordered.head(min(n, len(ordered)))
    bottom = reverse.head(min(n, len(reverse)))
    return {
        "top_rows": top,
        "bottom_rows": bottom,
        "top_mean": top["cum_return"].mean(),
        "top_median": top["cum_return"].median(),
        "top_hit": (top["cum_return"] > SOXX_CUM).mean() * 100,
        "top_positive": (top["cum_return"] > 0).mean() * 100,
        "bottom_mean": bottom["cum_return"].mean(),
        "bottom_median": bottom["cum_return"].median(),
        "bottom_hit": (bottom["cum_return"] > SOXX_CUM).mean() * 100,
        "bottom_positive": (bottom["cum_return"] > 0).mean() * 100,
        "spread": top["cum_return"].mean() - bottom["cum_return"].mean(),
        "hit_spread": (top["cum_return"] > SOXX_CUM).mean() * 100 - (bottom["cum_return"] > SOXX_CUM).mean() * 100,
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
    for _, group in df.groupby("category", sort=False, observed=False):
        group = group.copy()
        n = len(group)
        if n == 1:
            group["cat_score_pct"] = 1.0
        else:
            ranks = rank_average(group["score"].astype(float).tolist())
            group["cat_score_pct"] = [(rank - 1) / (n - 1) for rank in ranks]
        group["score_resid_cat"] = group["score"] - group["score"].mean()
        group["return_resid_cat"] = group["cum_return"] - group["cum_return"].mean()
        pieces.append(group)
    return pd.concat(pieces, ignore_index=True)


def stress_group_stats(df: pd.DataFrame, label: str) -> dict[str, float | int | str]:
    all_values: list[float] = []
    worst_values: list[float] = []
    dispersion_values: list[float] = []
    outperf = total = negative = 0
    for _, row in df.iterrows():
        company_values: list[float] = []
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
                avg = sum(company_values) / len(company_values)
                dispersion_values.append(math.sqrt(sum((v - avg) ** 2 for v in company_values) / (len(company_values) - 1)))
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
        "dispersion": sum(dispersion_values) / len(dispersion_values) if dispersion_values else float("nan"),
        "outperform_window": outperf / total * 100 if total else float("nan"),
        "outperform_cum": (df["cum_return"] > SOXX_CUM).mean() * 100,
        "negative_window": negative / total * 100 if total else float("nan"),
        "call_iv_mean": df["call_iv"].dropna().mean(),
        "put_iv_mean": df["put_iv"].dropna().mean(),
        "iv_mean": df["iv_avg"].dropna().mean(),
        "iv_median": df["iv_avg"].dropna().median(),
        "iv_n": int(df["iv_avg"].notna().sum()),
    }


def sample_robustness(df: pd.DataFrame, label: str, rule: str, mask: pd.Series) -> dict[str, float | str]:
    sample = df[mask].copy().sort_values("score_rank")
    c = correlations(sample, "score", "cum_return")
    tb = top_bottom_stats(sample, 30)
    return {
        "label": label,
        "rule": rule,
        "n": len(sample),
        "excluded": len(df) - len(sample),
        "pearson": c["pearson"],
        "spearman": c["spearman"],
        "kendall": c["kendall"],
        "top30": tb["top_mean"],
        "bottom30": tb["bottom_mean"],
        "spread": tb["spread"],
        "hit_spread": tb["hit_spread"],
    }


def row_company(row: pd.Series) -> list[object]:
    return [
        row["ticker"],
        row["company"],
        row["category"],
        fmt_pct(row["cum_return"]),
        fmt_pct(row["stress1"]),
        fmt_pct(row["stress2"]),
        fmt_pct(row["stress3"]),
        fmt_score(row["score"]),
        str(int(row["score_rank"])),
        row["confidence"],
    ]


def backup_existing_output() -> list[str]:
    if not OUT_PATH.exists():
        return []
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target_dir = BACKUP_DIR / f"{FEATURE_KEY}_三段SOXX下跌区间涨跌_写入前备份_{stamp}"
    target_dir.mkdir(parents=True, exist_ok=True)
    dst = target_dir / OUT_PATH.name
    shutil.copy2(OUT_PATH, dst)
    return [str(dst.relative_to(ROOT))]


def classify_sort(spearman_value: float, spread30: float) -> str:
    if pd.isna(spearman_value):
        return "无法判断"
    if spearman_value >= 0.15 and spread30 > 0:
        return "部分成立"
    if spearman_value >= 0.05:
        return "弱正向但不足"
    if spearman_value > -0.05:
        return "不成立"
    return "反向或偏负"


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
    missing_scores = sorted(set(stress_df.loc[stress_df["cum_return"].notna(), "ticker"]) - set(score_df["ticker"]))

    stress_text = read_text(STRESS_PATH)
    fin_text = read_text(FINANCIAL_PATH)
    stress_generation = extract_meta(stress_text, r"生成时间：([^。]+)。")
    financial_generation = extract_meta(fin_text, r"生成时间：([^\n]+)")

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
        stress_group_stats(ordered.head(30), f"{FEATURE_ID} Top30"),
        stress_group_stats(ordered.iloc[mid_start : mid_start + 30], f"{FEATURE_ID} Mid30"),
        stress_group_stats(ordered.tail(30), f"{FEATURE_ID} Bottom30"),
    ]

    category_rows: list[list[object]] = []
    category_corr_rows: list[list[object]] = []
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
                fmt_score(group["score"].mean()),
                fmt_pct(group["cum_return"].mean()),
                fmt_pct(group["cum_return"].median()),
                fmt_rate((group["cum_return"] > SOXX_CUM).mean() * 100),
            ]
        )
        category_corr_rows.append(
            [
                category,
                str(len(group)),
                fmt_num(c["pearson"]),
                fmt_num(c["spearman"]),
                fmt_num(c["kendall"]),
                fmt_pct(group["cum_return"].mean()),
                fmt_rate((group["cum_return"] > SOXX_CUM).mean() * 100),
                f"{winner['ticker']} {fmt_pct(winner['cum_return'])}",
                f"{loser['ticker']} {fmt_pct(loser['cum_return'])}",
                f"{top_score['ticker']} {fmt_score(top_score['score'])} / {fmt_pct(top_score['cum_return'])}",
            ]
        )

    corr_rows = [
        ["三段累计涨跌幅", str(main_corr["n"]), fmt_num(main_corr["pearson"]), fmt_num(main_corr["spearman"]), fmt_num(main_corr["kendall"]), "核心目标；三个SOXX下跌区间百分比简单相加，越高越好"],
    ]
    for key, (label, soxx_return) in SOXX_WINDOWS.items():
        c = window_corrs[key]
        corr_rows.append([label, str(c["n"]), fmt_num(c["pearson"]), fmt_num(c["spearman"]), fmt_num(c["kendall"]), f"单个压力窗口，SOXX {fmt_pct(soxx_return)}"])

    quintile_rows: list[list[object]] = []
    for label, group in split_score_quintiles(valid):
        worst = group[["stress1", "stress2", "stress3"]].min(axis=1, skipna=True)
        quintile_rows.append(
            [
                label,
                str(len(group)),
                fmt_score(group["score"].mean()),
                fmt_pct(group["cum_return"].mean()),
                fmt_pct(group["cum_return"].median()),
                fmt_rate((group["cum_return"] > SOXX_CUM).mean() * 100),
                fmt_pct(worst.mean()),
                fmt_pct(group["iv_avg"].mean()),
                str(int(group["iv_avg"].notna().sum())),
            ]
        )

    tb_rows: list[list[object]] = []
    for n in [10, 20, 30]:
        tb = tb_stats[n]
        tb_rows.append(
            [
                f"Top{n}/Bottom{n}",
                fmt_pct(tb["top_mean"]),
                fmt_pct(tb["top_median"]),
                fmt_rate(tb["top_hit"]),
                fmt_rate(tb["top_positive"]),
                fmt_pct(tb["bottom_mean"]),
                fmt_pct(tb["bottom_median"]),
                fmt_rate(tb["bottom_hit"]),
                fmt_rate(tb["bottom_positive"]),
                fmt_pct(tb["spread"]),
            ]
        )

    tb_detail_rows: list[list[object]] = []
    for _, row in tb_stats[10]["top_rows"].iterrows():
        tb_detail_rows.append(["Top10", *row_company(row)])
    for _, row in tb_stats[10]["bottom_rows"].sort_values("score_rank", ascending=False).iterrows():
        tb_detail_rows.append(["Bottom10", *row_company(row)])

    risk_rows: list[list[object]] = []
    for group in risk_groups:
        risk_rows.append(
            [
                group["label"],
                str(group["n"]),
                str(group["obs"]),
                fmt_pct(group["stress1_mean"]),
                fmt_pct(group["stress2_mean"]),
                fmt_pct(group["stress3_mean"]),
                fmt_pct(group["cum_mean"]),
                fmt_pct(group["window_mean"]),
                fmt_pct(group["worst_mean"]),
                fmt_pct(group["dispersion"]),
                fmt_rate(group["outperform_window"]),
                fmt_rate(group["outperform_cum"]),
                fmt_rate(group["negative_window"]),
                fmt_pct(group["call_iv_mean"]),
                fmt_pct(group["put_iv_mean"]),
                fmt_pct(group["iv_mean"]),
                fmt_pct(group["iv_median"]),
                str(group["iv_n"]),
            ]
        )

    neutral_corr_rows = [
        ["原始全样本", str(len(valid)), fmt_num(neutral_raw["pearson"]), fmt_num(neutral_raw["spearman"]), fmt_num(neutral_raw["kendall"]), "直接用F25原始分数排序"],
        ["分类内百分位合并", str(len(neutral)), fmt_num(neutral_pct["pearson"]), fmt_num(neutral_pct["spearman"]), fmt_num(neutral_pct["kendall"]), "每个分类内先按F25排序，再转为0-1百分位合并"],
        ["分类去均值残差", str(len(neutral)), fmt_num(neutral_resid["pearson"]), fmt_num(neutral_resid["spearman"]), fmt_num(neutral_resid["kendall"]), "F25和累计收益分别减去分类均值后相关"],
    ]
    neutral_tb_rows: list[list[object]] = []
    for n in [10, 20, 30]:
        tb = neutral_tb_stats[n]
        neutral_tb_rows.append([f"中性Top{n}/Bottom{n}", fmt_pct(tb["top_mean"]), fmt_rate(tb["top_hit"]), fmt_pct(tb["bottom_mean"]), fmt_rate(tb["bottom_hit"]), fmt_pct(tb["spread"])])

    low_q = valid["cum_return"].quantile(0.05)
    high_q = valid["cum_return"].quantile(0.95)
    valid["low_liquidity"] = valid["liquidity_score"].isna() | (valid["liquidity_score"] <= 5.0)
    valid["adr_currency_abnormal"] = (
        valid["listing_type"].fillna("").str.contains("ADR|ADS", case=False, regex=True)
        | valid["adr_ratio"].fillna("").ne("不适用")
        | (
            valid["currency"].fillna("").ne("")
            & valid["financial_currency"].fillna("").ne("")
            & valid["currency"].fillna("").ne(valid["financial_currency"].fillna(""))
        )
        | valid["valuation_check"].fillna("").str.contains("currency_mismatch", case=False, regex=False)
        | valid["financial_note"].fillna("").str.contains("交易货币/财报货币不一致|ADR/ADS比例需确认", regex=True)
    )
    valid["extreme_return"] = (valid["cum_return"] <= low_q) | (valid["cum_return"] >= high_q)

    robustness_data = [
        sample_robustness(valid, "全样本基准", "无剔除", pd.Series(True, index=valid.index)),
        sample_robustness(valid, "剔除低流动性", "F51交易流动性分 > 5.0", ~valid["low_liquidity"]),
        sample_robustness(valid, "剔除ADR/币种异常", "listing_type=common/equity、ADR比例不适用、交易/财报货币一致、估值校验无currency_mismatch", ~valid["adr_currency_abnormal"]),
        sample_robustness(valid, "剔除极端涨跌", f"剔除三段累计涨跌双尾5%；阈值 {fmt_pct(low_q)} / {fmt_pct(high_q)}", ~valid["extreme_return"]),
        sample_robustness(valid, "三项合并剔除", "同时满足上述三项", ~(valid["low_liquidity"] | valid["adr_currency_abnormal"] | valid["extreme_return"])),
    ]
    robustness_rows: list[list[object]] = []
    for row in robustness_data:
        robustness_rows.append(
            [
                row["label"],
                row["rule"],
                str(row["n"]),
                str(row["excluded"]),
                fmt_num(row["pearson"]),
                fmt_num(row["spearman"]),
                fmt_num(row["kendall"]),
                fmt_pct(row["top30"]),
                fmt_pct(row["bottom30"]),
                fmt_pct(row["spread"]),
                fmt_pct(row["hit_spread"]),
            ]
        )

    exclusion_rows = []
    for label, column in [("低流动性", "low_liquidity"), ("ADR/币种异常", "adr_currency_abnormal"), ("极端涨跌双尾5%", "extreme_return")]:
        tickers = sorted(valid.loc[valid[column], "ticker"].tolist())
        exclusion_rows.append([label, str(len(tickers)), ", ".join(tickers) if tickers else "无"])

    best_rows = [row_company(row) for _, row in valid.sort_values("cum_return", ascending=False).head(15).iterrows()]
    worst_rows = [row_company(row) for _, row in valid.sort_values("cum_return", ascending=True).head(15).iterrows()]
    top_score_rows = [row_company(row) for _, row in valid.sort_values("score_rank", ascending=True).head(15).iterrows()]
    bottom_score_rows = [row_company(row) for _, row in valid.sort_values("score_rank", ascending=False).head(15).iterrows()]
    high_bad_rows = [
        [
            row["ticker"],
            row["company"],
            row["category"],
            fmt_score(row["score"]),
            str(int(row["score_rank"])),
            fmt_pct(row["cum_return"]),
            "链条清晰不等于压力期低beta；需叠加估值、价格相对强度、客户集中、融资/建设或个股事件过滤。",
        ]
        for _, row in valid[(valid["score"] >= 8.0) & (valid["cum_return"] < SOXX_CUM)]
        .sort_values("cum_return", ascending=True)
        .head(12)
        .iterrows()
    ]
    low_good_rows = [
        [
            row["ticker"],
            row["company"],
            row["category"],
            fmt_score(row["score"]),
            str(int(row["score_rank"])),
            fmt_pct(row["cum_return"]),
            "F25低分说明需求到收入链条不清晰，但压力期表现可能来自低beta、特殊事件、低流动性反弹或非AI业务防守。",
        ]
        for _, row in valid[(valid["score"] <= 5.5) & (valid["cum_return"] > SOXX_CUM)]
        .sort_values("cum_return", ascending=False)
        .head(12)
        .iterrows()
    ]

    dist_rows: list[list[object]] = []
    buckets = [
        ("9.0-10.0", valid[(valid["score"] >= 9.0) & (valid["score"] <= 10.0)]),
        ("7.0-8.9", valid[(valid["score"] >= 7.0) & (valid["score"] < 9.0)]),
        ("5.0-6.9", valid[(valid["score"] >= 5.0) & (valid["score"] < 7.0)]),
        ("3.0-4.9", valid[(valid["score"] >= 3.0) & (valid["score"] < 5.0)]),
        ("1.0-2.9", valid[(valid["score"] >= 1.0) & (valid["score"] < 3.0)]),
    ]
    for label, group in buckets:
        dist_rows.append([label, str(len(group))])

    moved_backups = backup_existing_output()
    old_output_note = "未发现同名旧版正式输出。" if not moved_backups else "写入前已复制备份：" + "；".join(f"`{p}`" for p in moved_backups)

    sort_eval = classify_sort(main_corr["spearman"], tb_stats[30]["spread"])
    tb_eval = "成立" if tb_stats[30]["spread"] > 5 else ("弱成立" if tb_stats[30]["spread"] > 0 else "不成立")
    risk_top = risk_groups[0]
    risk_bottom = risk_groups[2]
    risk_eval = "成立" if risk_top["cum_mean"] > risk_bottom["cum_mean"] and risk_top["worst_mean"] > risk_bottom["worst_mean"] else "不成立"
    neutral_eval = "成立" if neutral_pct["spearman"] > 0 and neutral_tb_stats[30]["spread"] > 0 else "不成立"
    robust_eval = "成立" if robustness_data[-1]["spearman"] > 0 and robustness_data[-1]["spread"] > 0 else "不成立"

    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 三段SOXX下跌区间涨跌 {RUN_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.extend(
        [
            f"- 评估对象：`{FEATURE_KEY}`。",
            f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 {RUN_DATE}，覆盖 {len(score_df)} 家。",
            f"- 收益输入：`日度资料/区间涨跌/{STRESS_PATH.name}`，生成时间 {stress_generation}；价格口径为 Yahoo Finance `Close`，`auto_adjust=False`，不含股息再投资。",
            "- SOXX压力窗口：2025-02-20至2025-04-08 下跌 -32.98%；2026-02-25至2026-03-30 下跌 -15.82%；2025-10-29至2025-11-20 下跌 -13.40%。SOXX三段累计涨跌幅为 -62.20%。",
            f"- 稳健性辅助输入：`特征量化/量化评分/{LIQUIDITY_PATH.name}`；`日度资料/每日金融数据/{FINANCIAL_PATH.name}`，金融数据生成时间 {financial_generation}。",
            f"- 有效评估样本：评分与三段累计涨跌幅交集 {len(valid)} 家；F25评分有但累计涨跌缺失 {len(missing_returns)} 家：{', '.join(missing_returns) if missing_returns else '无'}。",
            "- 收益方向口径：三段累计涨跌幅越高越好；在压力窗口中，跌幅更小、或上涨，均视为更优表现。",
            "- 命中率口径：三段累计涨跌幅大于 SOXX 三段累计涨跌幅 `-62.20%` 记为压力命中；Top-Bottom收益差=高分组合平均三段累计收益 - 低分组合平均三段累计收益。",
            "- 风险口径限制：本次输入是三个固定压力区间收益，不是逐日收益序列；因此本报告不写成严格日度波动率、完整最大回撤或真实下跌日表现结论，而使用三个SOXX下跌窗口均值、平均最差窗口、窗口离散度、跑赢SOXX比例、负收益窗口占比，并用 2026-06-03 近ATM Call/Put IV均值补充当前波动代理。",
            "- 稳健性口径：低流动性使用 `F51<=5.0` 或F51缺失作为剔除代理；ADR/币种异常使用每日金融数据中的 `listing_type`、ADR比例、交易/财报货币和 `currency_mismatch` 标记；极端涨跌按本次三段累计收益双尾5%剔除。",
            f"- 旧版处理：{old_output_note}",
            "- 本报告是下游特征评估，只读取 `特征量化/量化评分/`、`特征量化/特征评估/`、`日度资料/区间涨跌/` 和必要日度金融字段，不把结论反向写入上游资料。",
        ]
    )
    lines.append("")
    lines.append("## 结论摘要")
    lines.extend(
        [
            f"- 排序有效性：{sort_eval}。全样本 Pearson {fmt_num(main_corr['pearson'])}，Spearman {fmt_num(main_corr['spearman'])}，Kendall {fmt_num(main_corr['kendall'])}；重点指标 Spearman 为 {fmt_num(main_corr['spearman'])}。",
            f"- 分窗口观察：SOXX下跌1/2/3 的 Spearman 分别为 {fmt_num(window_corrs['stress1']['spearman'])}、{fmt_num(window_corrs['stress2']['spearman'])}、{fmt_num(window_corrs['stress3']['spearman'])}。三个窗口均不强，说明F25不能稳定解释压力窗口抗跌排序。",
            f"- Top/Bottom能力：{tb_eval}。Top10/Top20/Top30 平均累计收益分别为 {fmt_pct(tb_stats[10]['top_mean'])}、{fmt_pct(tb_stats[20]['top_mean'])}、{fmt_pct(tb_stats[30]['top_mean'])}；对应Top-Bottom收益差为 {fmt_pct(tb_stats[10]['spread'])}、{fmt_pct(tb_stats[20]['spread'])}、{fmt_pct(tb_stats[30]['spread'])}。",
            f"- 风险解释力：{risk_eval}。F25 Top30 三段累计均值 {fmt_pct(risk_top['cum_mean'])}、平均最差窗口 {fmt_pct(risk_top['worst_mean'])}、跑赢SOXX窗口比例 {fmt_rate(risk_top['outperform_window'])}、当前IV均值 {fmt_pct(risk_top['iv_mean'])}；Bottom30 对应为 {fmt_pct(risk_bottom['cum_mean'])}、{fmt_pct(risk_bottom['worst_mean'])}、{fmt_rate(risk_bottom['outperform_window'])}、{fmt_pct(risk_bottom['iv_mean'])}。",
            f"- 分类中性：{neutral_eval}。分类内百分位合并 Spearman {fmt_num(neutral_pct['spearman'])}，分类去均值残差 Spearman {fmt_num(neutral_resid['spearman'])}；中性Top30-Bottom30收益差 {fmt_pct(neutral_tb_stats[30]['spread'])}。",
            f"- 稳健性：{robust_eval}。剔除低流动性后 Spearman {fmt_num(robustness_data[1]['spearman'])}，剔除ADR/币种异常后 {fmt_num(robustness_data[2]['spearman'])}，剔除极端涨跌后 {fmt_num(robustness_data[3]['spearman'])}，三项合并后 {fmt_num(robustness_data[4]['spearman'])}；三项合并后 Top30-Bottom30为 {fmt_pct(robustness_data[4]['spread'])}。",
            "- 解释：F25 衡量需求源、订单、RPO、backlog、合同、客户认证或收入指引到公司收入利润的链条是否短且可验证。这个特征有基本面兑现价值，但在三段 SOXX 下跌窗口中，高分端同时暴露于 AI 硬件/IDC/电力建设高beta、估值压缩、客户集中、融资和建设进度风险；低分或中低分端则可能因公用事业低beta、传统工业、特殊事件或低流动性反弹而少跌。因此 F25 不宜单独解释为压力窗口防守因子。",
        ]
    )
    lines.append("")
    lines.append("## 覆盖检查")
    lines.append(
        md_table(
            ["项目", "数量", "说明"],
            [
                ["F25评分覆盖", str(len(score_df)), "来自2026-06-04评分文件"],
                ["三段累计涨跌覆盖", str(int(stress_df["cum_return"].notna().sum())), "来自2026-06-04三段SOXX下跌区间涨跌文件"],
                ["交集有效样本", str(len(valid)), "用于本报告主指标"],
                ["评分有但累计涨跌缺失", str(len(missing_returns)), ", ".join(missing_returns) if missing_returns else "无"],
                ["涨跌有但评分缺失", str(len(missing_scores)), ", ".join(missing_scores) if missing_scores else "无"],
            ],
            ["---", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.append(md_table(["分类目录", "样本数", "F25均分", "三段累计平均", "三段累计中位数", "跑赢SOXX累计率"], category_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## 排序有效性")
    lines.append(md_table(["目标收益", "样本数", "Pearson", "Spearman", "Kendall tau-b", "解释"], corr_rows, ["---", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### F25分数分组收益")
    lines.append(md_table(["分组", "公司数", "F25均分", "三段累计平均", "三段累计中位数", "跑赢SOXX累计率", "平均最差窗口", "当前IV均值", "IV样本"], quintile_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("分组读数没有形成稳定的高分少跌梯度。F25最高分五分位包含 DELL、VRT、NVDA、NBIS、ORCL、SNDK、GOOGL、AMZN、GEV、HPE、MSFT、PWR 等链条清晰公司，其中部分确实明显跑赢SOXX，但也混入 NBIS、VRT、SMCI、IREN、APLD 等高beta或建设/融资风险样本。")
    lines.append("")
    lines.append("## Top/Bottom能力")
    lines.append(md_table(["组合", "Top平均累计", "Top中位累计", "Top压力命中率", "Top正收益率", "Bottom平均累计", "Bottom中位累计", "Bottom压力命中率", "Bottom正收益率", "Top-Bottom收益差"], tb_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    lines.append(md_table(["组别", "股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F25分", "F25排名", "置信度"], tb_detail_rows, ["---", "---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用三个固定SOXX下跌区间作为压力测试代理。严格日度波动率、完整最大回撤、真实下跌日收益稳定性需要逐日价格序列；当前IV均值仅是 2026-06-03 近ATM期权波动代理，不等同于历史实际波动率。")
    lines.append("")
    lines.append(md_table(["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "三段累计均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX窗口比例", "跑赢SOXX累计率", "负收益窗口占比", "平均Call IV", "平均Put IV", "当前IV均值", "IV中位数", "IV样本"], risk_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append(f"结论：F25 Top30 相比 Bottom30，三段累计差值为 {fmt_pct(risk_top['cum_mean'] - risk_bottom['cum_mean'])}，平均最差窗口差值为 {fmt_pct(risk_top['worst_mean'] - risk_bottom['worst_mean'])}，跑赢SOXX窗口比例差值为 {fmt_pct(risk_top['outperform_window'] - risk_bottom['outperform_window'], 1)}，当前IV均值差值为 {fmt_pct(risk_top['iv_mean'] - risk_bottom['iv_mean'])}。这些指标没有共同支持“高F25回撤更小、波动更低、下跌窗口更稳”。")
    lines.append("")
    lines.append("## 分类中性结果")
    lines.append(md_table(["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"], neutral_corr_rows, ["---", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(md_table(["组合", "Top平均累计", "Top压力命中率", "Bottom平均累计", "Bottom压力命中率", "Top-Bottom收益差"], neutral_tb_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(md_table(["分类目录", "样本数", "Pearson", "Spearman", "Kendall", "类内累计均值", "类内命中率", "类内最好", "类内最差", "类内最高F25公司"], category_corr_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---", "---", "---"]))
    lines.append("")
    lines.append("分类内结果用于检验 F25 是否只是押中了某个分类目录。分类内百分位合并和分类去均值残差若仍不强，说明即便在同一产业目录内，需求到收入链条更清晰也没有稳定转化为压力窗口少跌。")
    lines.append("")
    lines.append("## 稳健性检验")
    lines.append(md_table(["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30", "Top-Bottom命中率差"], robustness_rows, ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("稳健性结论：核心观察是三项合并剔除后 Spearman 与 Top30-Bottom30是否同向为正。本次低流动性、ADR/币种异常、极端涨跌过滤后均未给出强正向结果，因此 F25 的压力窗口有效性不能被稳健性检验支持。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(md_table(["剔除项", "数量", "公司"], exclusion_rows, ["---", "---:", "---"]))
    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 三段累计表现最好15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F25分", "F25排名", "置信度"], best_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 三段累计表现最差15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F25分", "F25排名", "置信度"], worst_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### F25高分前15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F25分", "F25排名", "置信度"], top_score_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### F25低分前15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F25分", "F25排名", "置信度"], bottom_score_rows, ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    if high_bad_rows:
        lines.append("### 高F25但压力窗口显著拖累")
        lines.append(md_table(["股票代号", "公司名称", "分类目录", "F25分", "F25排名", "三段累计", "主要提示"], high_bad_rows, ["---", "---", "---", "---:", "---:", "---:", "---"]))
        lines.append("")
    if low_good_rows:
        lines.append("### 低F25但跑赢SOXX累计")
        lines.append(md_table(["股票代号", "公司名称", "分类目录", "F25分", "F25排名", "三段累计", "主要提示"], low_good_rows, ["---", "---", "---", "---:", "---:", "---:", "---"]))
        lines.append("")
    lines.append("## 分数分布")
    lines.append(md_table(["分数区间", "有效样本公司数"], dist_rows, ["---", "---:"]))
    lines.append("")
    lines.append("## 评估结论与使用建议")
    if sort_eval.startswith("部分") and tb_eval in {"成立", "弱成立"} and robust_eval == "成立":
        lines.extend(
            [
                "- 对“三段SOXX下跌区间累计涨跌幅”这一目标，F25 可以作为弱正向辅助因子，但不能单独高权重使用。",
                "- 更稳妥的用法是把F25作为收入确认链条质量和订单可见度变量，再叠加估值、交易流动性、价格相对强度和负向预期差风险过滤。",
            ]
        )
    else:
        lines.extend(
            [
                "- 对“三段SOXX下跌区间累计涨跌幅”这一目标，F25_需求到收入链条清晰度不能作为独立正向压力窗口排序因子；至少不能把“链条清晰”机械解释成“SOXX下跌时更抗跌”。",
                "- F25 仍有重要基本面价值：它适合识别订单、RPO、backlog、合同、客户认证、收入指引和收入确认路径更清楚的公司，用于解释收入兑现确定性和基本面跟踪优先级。",
                "- 组合使用时，F25高分必须叠加 F05估值赔率、F06估值分位、F08财务承压、F31订单刚性、F32订单下修风险、F41负向预期差风险、F50价格相对强度和F51交易流动性。尤其是高F25但高IV、高估值、高融资依赖、建设周期长或客户集中公司，压力窗口中应降低单因子权重。",
                "- 若目标是下跌窗口防守，应优先验证估值缓冲、财务韧性、价格相对强度、流动性和执行风险，而不是单独依赖需求到收入链条清晰度。",
            ]
        )
    lines.append("- 本报告只作为下游特征评估，不反向修改 `公司调研/`、`行业调研/`、`日度资料/` 或 `特征量化/量化评分/`。")
    lines.append("")
    lines.append("## 方法说明")
    lines.extend(
        [
            "- Pearson 使用原始F25分数与收益百分比。",
            "- Spearman 使用平均秩处理并列分数；本报告重点看Spearman，因为F25本质是排序评分。",
            "- Kendall 使用tau-b口径，对F25分数和收益中的并列值做tie修正。",
            "- Top/Bottom按F25评分文件原始排名取样；如公司三段累计收益缺失，则不插补，向后顺延取有效样本。",
            "- 分类中性百分位中，同一分类内高F25分对应更高百分位，然后合并全样本重新排序。",
            f"- 极端涨跌双尾5%阈值按本次{len(valid)}家有效样本三段累计收益计算，低端阈值为 `{fmt_pct(low_q)}`，高端阈值为 `{fmt_pct(high_q)}`。",
            "- 所有收益均为区间Close价格变动，不含股息再投资，不等于总回报。",
        ]
    )
    lines.append("")
    lines.append("## 数据来源路径")
    lines.extend(
        [
            f"- `特征量化/量化评分/{SCORE_PATH.name}`",
            f"- `日度资料/区间涨跌/{STRESS_PATH.name}`",
            f"- `特征量化/量化评分/{LIQUIDITY_PATH.name}`",
            f"- `日度资料/每日金融数据/{FINANCIAL_PATH.name}`",
        ]
    )
    lines.append("")

    summary = {
        "score_n": len(score_df),
        "stress_n": int(stress_df["cum_return"].notna().sum()),
        "valid_n": len(valid),
        "missing_returns": missing_returns,
        "main_corr": main_corr,
        "window_corrs": window_corrs,
        "tb30": tb_stats[30],
        "risk_top": risk_top,
        "risk_bottom": risk_bottom,
        "neutral_pct": neutral_pct,
        "robust_combined": robustness_data[-1],
        "low_liq_count": int(valid["low_liquidity"].sum()),
        "adr_count": int(valid["adr_currency_abnormal"].sum()),
        "extreme_count": int(valid["extreme_return"].sum()),
        "low_q": low_q,
        "high_q": high_q,
    }
    return "\n".join(lines), summary


def main() -> None:
    report, summary = build_report()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(f"wrote={OUT_PATH}")
    print(
        " ".join(
            [
                f"score_n={summary['score_n']}",
                f"stress_n={summary['stress_n']}",
                f"valid_n={summary['valid_n']}",
                f"missing={','.join(summary['missing_returns'])}",
                f"main_spearman={summary['main_corr']['spearman']:.6f}",
                f"main_pearson={summary['main_corr']['pearson']:.6f}",
                f"main_kendall={summary['main_corr']['kendall']:.6f}",
                f"top30_spread={summary['tb30']['spread']:.6f}",
                f"combined_spearman={summary['robust_combined']['spearman']:.6f}",
                f"combined_spread={summary['robust_combined']['spread']:.6f}",
            ]
        )
    )
    print("window_spearman=" + ",".join(f"{key}:{value['spearman']:.6f}" for key, value in summary["window_corrs"].items()))
    print(f"risk_top_cum={fmt_pct(summary['risk_top']['cum_mean'])} risk_bottom_cum={fmt_pct(summary['risk_bottom']['cum_mean'])}")
    print(f"risk_top_worst={fmt_pct(summary['risk_top']['worst_mean'])} risk_bottom_worst={fmt_pct(summary['risk_bottom']['worst_mean'])}")
    print(f"neutral_spearman={summary['neutral_pct']['spearman']:.6f}")
    print(
        f"robust_counts low_liq={summary['low_liq_count']} adr={summary['adr_count']} "
        f"extreme={summary['extreme_count']} thresholds={fmt_pct(summary['low_q'])}/{fmt_pct(summary['high_q'])}"
    )


if __name__ == "__main__":
    main()
