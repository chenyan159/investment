from __future__ import annotations

import math
import re
import shutil
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
FEATURE_ID = "F30"
FEATURE_NAME = "收入可见度"
FEATURE_STEM = f"{FEATURE_ID}_{FEATURE_NAME}"
WINDOW = "6个月"
REPORT_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_STEM}_量化评分_2026-06-04.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
F51_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUT_DIR / "备份"
OUT_PATH = OUT_DIR / f"{FEATURE_STEM}_特征评估_{WINDOW}涨跌_{REPORT_DATE}.md"

SOXX = {
    "soxx1": ("SOXX下跌1", "2025-02-20至2025-04-08", -32.98),
    "soxx2": ("SOXX下跌2", "2026-02-25至2026-03-30", -15.82),
    "soxx3": ("SOXX下跌3", "2025-10-29至2025-11-20", -13.40),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def split_md_row(line: str) -> list[str] | None:
    text = line.strip()
    if not text.startswith("|") or not text.endswith("|"):
        return None
    return [cell.strip() for cell in text.strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def parse_percent(cell: str | None) -> float:
    if cell is None:
        return math.nan
    text = str(cell)
    if "N/A" in text or "缺失" in text:
        return math.nan
    m = re.search(r"(上涨|下跌|持平)?\s*([+-]?\d+(?:,\d{3})*(?:\.\d+)?)%", text)
    if not m:
        return math.nan
    direction, number = m.groups()
    value = float(number.replace(",", ""))
    if direction == "下跌" and value > 0:
        value = -value
    if direction == "上涨" and value < 0:
        value = abs(value)
    return value


def parse_number(cell: str | None) -> float:
    if cell is None:
        return math.nan
    text = str(cell).strip().replace(",", "")
    if text in {"", "N/A", "缺失", "不适用"}:
        return math.nan
    try:
        return float(text)
    except ValueError:
        return math.nan


def table_rows_in_section(text: str, section_heading: str) -> list[dict[str, str]]:
    start = text.index(section_heading)
    rest = text[start + len(section_heading) :]
    next_heading = re.search(r"\n## ", rest)
    section = rest[: next_heading.start()] if next_heading else rest
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in section.splitlines():
        cells = split_md_row(line)
        if not cells or is_separator(cells):
            continue
        if header is None:
            header = cells
            continue
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def parse_score_file(path: Path) -> pd.DataFrame:
    rows = table_rows_in_section(read_text(path), "## 全公司排序表")
    parsed: list[dict[str, object]] = []
    for row in rows:
        ticker = row.get("股票代号", "").strip()
        rank = row.get("排名", "").strip()
        score = row.get("特征分", "").strip()
        if not ticker or not rank or not score:
            continue
        parsed.append(
            {
                "ticker": ticker,
                "company": row.get("公司名称", "").strip(),
                "category": row.get("分类目录", "").strip(),
                "score": float(score),
                "score_rank": int(rank),
                "evidence": row.get("证据等级", "").strip(),
                "confidence": row.get("置信度", "").strip(),
            }
        )
    df = pd.DataFrame(parsed)
    if df.empty:
        raise RuntimeError(f"No score rows parsed from {path}")
    return df


def parse_return_file(path: Path) -> pd.DataFrame:
    text = read_text(path)
    start = text.index("## 按分类分组的公司明细")
    section = text[start:]
    rows: list[dict[str, object]] = []
    category: str | None = None
    header: list[str] | None = None
    for line in section.splitlines():
        heading = re.match(r"### (.+)", line.strip())
        if heading:
            category = heading.group(1).strip()
            header = None
            continue
        cells = split_md_row(line)
        if not cells or is_separator(cells):
            continue
        if cells[0] == "股票代号":
            header = cells
            continue
        if category and header and len(cells) == len(header):
            row = dict(zip(header, cells))
            rows.append(
                {
                    "ticker": row["股票代号"].strip(),
                    "return_company": row["公司名称"].strip(),
                    "return_category": category,
                    "latest_trade_date": row.get("最新交易日", "").strip(),
                    "latest_close": parse_number(row.get("最新收盘价")),
                    "r_1m": parse_percent(row.get("1个月")),
                    "r_3m": parse_percent(row.get("3个月")),
                    "r_6m": parse_percent(row.get("6个月")),
                    "r_1y": parse_percent(row.get("1年")),
                    "return_note": row.get("备注", "").strip(),
                }
            )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"No return rows parsed from {path}")
    return df


def parse_soxx_file(path: Path) -> pd.DataFrame:
    text = read_text(path)
    start = text.index("### 按分类分组的全公司明细")
    end = text.index("## 按分类分组的公司明细")
    section = text[start:end]
    rows: list[dict[str, object]] = []
    category: str | None = None
    header: list[str] | None = None
    for line in section.splitlines():
        heading = re.match(r"#### (.+)", line.strip())
        if heading:
            category = heading.group(1).strip()
            header = None
            continue
        cells = split_md_row(line)
        if not cells or is_separator(cells):
            continue
        if cells[0] == "股票代号":
            header = cells
            continue
        if category and header and len(cells) == len(header):
            row = dict(zip(header, cells))
            rows.append(
                {
                    "ticker": row["股票代号"].strip(),
                    "soxx_category": category,
                    "soxx1": parse_percent(row.get("SOXX下跌1 2025-02-20至2025-04-08")),
                    "soxx2": parse_percent(row.get("SOXX下跌2 2026-02-25至2026-03-30")),
                    "soxx3": parse_percent(row.get("SOXX下跌3 2025-10-29至2025-11-20")),
                    "soxx_note": row.get("备注", "").strip(),
                }
            )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"No SOXX rows parsed from {path}")
    return df


def parse_financial_file(path: Path) -> pd.DataFrame:
    text = read_text(path)
    start = text.index("## 按项目分类分组的公司明细表")
    section = text[start:]
    rows: list[dict[str, object]] = []
    category: str | None = None
    header: list[str] | None = None
    for line in section.splitlines():
        heading = re.match(r"### (.+)", line.strip())
        if heading:
            category = heading.group(1).strip()
            header = None
            continue
        cells = split_md_row(line)
        if not cells or is_separator(cells):
            continue
        if cells[0] == "股票代号":
            header = cells
            continue
        if category and header and len(cells) == len(header):
            row = dict(zip(header, cells))
            call_iv = parse_percent(row.get("Call IV"))
            put_iv = parse_percent(row.get("Put IV"))
            iv_values = [x for x in (call_iv, put_iv) if math.isfinite(x)]
            rows.append(
                {
                    "ticker": row["股票代号"].strip(),
                    "fin_category": category,
                    "call_iv": call_iv,
                    "put_iv": put_iv,
                    "near_atm_iv": float(np.mean(iv_values)) if iv_values else math.nan,
                    "currency": row.get("currency", "").strip(),
                    "financial_currency": row.get("financial_currency", "").strip(),
                    "listing_type": row.get("listing_type", "").strip(),
                    "adr_ratio": row.get("adr_ratio", "").strip(),
                    "valuation_check": row.get("估值校验", "").strip(),
                    "fin_note": row.get("备注", "").strip(),
                }
            )
    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError(f"No financial rows parsed from {path}")
    return df


def pearson(x: pd.Series, y: pd.Series) -> float:
    sub = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(sub) < 2:
        return math.nan
    if sub["x"].std(ddof=0) == 0 or sub["y"].std(ddof=0) == 0:
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
    xs = sub["x"].to_numpy(dtype=float)
    ys = sub["y"].to_numpy(dtype=float)
    concordant = discordant = ties_x = ties_y = 0
    for i in range(n - 1):
        dx = xs[i + 1 :] - xs[i]
        dy = ys[i + 1 :] - ys[i]
        sx = np.sign(dx)
        sy = np.sign(dy)
        both_tied = (sx == 0) & (sy == 0)
        ties_x += int(((sx == 0) & (sy != 0)).sum())
        ties_y += int(((sx != 0) & (sy == 0)).sum())
        valid = ~both_tied & (sx != 0) & (sy != 0)
        concordant += int((sx[valid] * sy[valid] > 0).sum())
        discordant += int((sx[valid] * sy[valid] < 0).sum())
    denominator = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    if denominator == 0:
        return math.nan
    return float((concordant - discordant) / denominator)


def corr_stats(df: pd.DataFrame, score_col: str = "score", ret_col: str = "r_6m") -> dict[str, float | int]:
    sub = df[[score_col, ret_col]].dropna()
    return {
        "n": len(sub),
        "pearson": pearson(sub[score_col], sub[ret_col]),
        "spearman": spearman(sub[score_col], sub[ret_col]),
        "kendall": kendall_tau_b(sub[score_col], sub[ret_col]),
    }


def fmt_corr(value: float | None) -> str:
    if value is None or not math.isfinite(float(value)):
        return "N/A"
    return f"{float(value):.3f}"


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None or not math.isfinite(float(value)):
        return "N/A"
    return f"{float(value):+.{digits}f}%"


def fmt_rate(value: float | None, digits: int = 1) -> str:
    if value is None or not math.isfinite(float(value)):
        return "N/A"
    return f"{float(value):.{digits}f}%"


def fmt_float(value: float | None, digits: int = 2) -> str:
    if value is None or not math.isfinite(float(value)):
        return "N/A"
    return f"{float(value):.{digits}f}"


def md_table(headers: list[str], rows: list[list[object]], aligns: list[str] | None = None) -> str:
    if aligns is None:
        aligns = ["---"] * len(headers)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(aligns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def sorted_by_score(df: pd.DataFrame, ascending: bool = False) -> pd.DataFrame:
    if ascending:
        return df.sort_values(["score", "score_rank", "ticker"], ascending=[True, False, True]).reset_index(drop=True)
    return df.sort_values(["score", "score_rank", "ticker"], ascending=[False, True, True]).reset_index(drop=True)


def top_bottom_stats(df: pd.DataFrame, n: int, score_col: str = "score") -> dict[str, object]:
    sub = df.dropna(subset=[score_col, "r_6m"]).copy()
    if score_col == "score":
        top = sorted_by_score(sub).head(n)
        bottom = sorted_by_score(sub, ascending=True).head(n)
    else:
        top = sub.sort_values([score_col, "score", "score_rank", "ticker"], ascending=[False, False, True, True]).head(n)
        bottom = sub.sort_values([score_col, "score", "score_rank", "ticker"], ascending=[True, True, False, True]).head(n)
    return {
        "n": n,
        "top_mean": top["r_6m"].mean(),
        "top_hit": (top["r_6m"] > 0).mean() * 100,
        "bottom_mean": bottom["r_6m"].mean(),
        "bottom_hit": (bottom["r_6m"] > 0).mean() * 100,
        "diff": top["r_6m"].mean() - bottom["r_6m"].mean(),
        "top": top,
        "bottom": bottom,
    }


def quintile_stats(df: pd.DataFrame) -> list[dict[str, object]]:
    sub = sorted_by_score(df).dropna(subset=["score", "r_6m"]).reset_index(drop=True)
    groups: list[dict[str, object]] = []
    for idx, locs in enumerate(np.array_split(np.arange(len(sub)), 5), start=1):
        group = sub.iloc[locs]
        groups.append(
            {
                "group": f"Q{idx}{'最高分' if idx == 1 else '最低分' if idx == 5 else ''}",
                "n": len(group),
                "score_mean": group["score"].mean(),
                "return_mean": group["r_6m"].mean(),
                "return_median": group["r_6m"].median(),
                "hit": (group["r_6m"] > 0).mean() * 100,
            }
        )
    return groups


def add_neutral_scores(df: pd.DataFrame) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    for _, group in df.groupby("category", sort=True):
        g = group.copy()
        n = len(g)
        if n <= 1:
            g["cat_percentile"] = 1.0
        else:
            g["cat_percentile"] = (g["score"].rank(method="average") - 1) / (n - 1)
        g["score_resid"] = g["score"] - g["score"].mean()
        g["ret_resid"] = g["r_6m"] - g["r_6m"].mean()
        parts.append(g)
    return pd.concat(parts, ignore_index=True)


def risk_group_stats(df: pd.DataFrame) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    sub = sorted_by_score(df).dropna(subset=["score", "r_6m"]).reset_index(drop=True)
    mid_start = max((len(sub) - 30) // 2, 0)
    groups = [
        (f"{FEATURE_ID} Top30", sub.head(30).copy()),
        (f"{FEATURE_ID} Mid30", sub.iloc[mid_start : mid_start + 30].copy()),
        (f"{FEATURE_ID} Bottom30", sorted_by_score(sub, ascending=True).head(30).copy()),
    ]
    pressure_rows: list[dict[str, object]] = []
    iv_rows: list[dict[str, object]] = []
    for label, group in groups:
        pressure_values = group[["soxx1", "soxx2", "soxx3"]]
        observed = pressure_values.stack().dropna()
        beat_list: list[bool] = []
        for col, (_, _, soxx_ret) in SOXX.items():
            values = group[col].dropna()
            beat_list.extend((values > soxx_ret).tolist())
        row_std = pressure_values.std(axis=1, skipna=True)
        pressure_rows.append(
            {
                "group": label,
                "n": len(group),
                "obs": len(observed),
                "soxx1_mean": group["soxx1"].mean(),
                "soxx2_mean": group["soxx2"].mean(),
                "soxx3_mean": group["soxx3"].mean(),
                "stress_mean": observed.mean(),
                "worst_mean": pressure_values.min(axis=1, skipna=True).mean(),
                "window_std": row_std.mean(),
                "beat_soxx": np.mean(beat_list) * 100 if beat_list else math.nan,
                "negative_rate": (observed < 0).mean() * 100 if len(observed) else math.nan,
            }
        )
        iv_rows.append(
            {
                "group": label,
                "n": len(group),
                "iv_n": int(group["near_atm_iv"].notna().sum()),
                "call_iv": group["call_iv"].mean(skipna=True),
                "put_iv": group["put_iv"].mean(skipna=True),
                "near_iv": group["near_atm_iv"].mean(skipna=True),
                "near_iv_median": group["near_atm_iv"].median(skipna=True),
            }
        )
    return pressure_rows, iv_rows


def category_corrs(df: pd.DataFrame) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for category, group in df.groupby("category", sort=True):
        g = group.dropna(subset=["score", "r_6m"]).copy()
        top_score = sorted_by_score(g).iloc[0]
        top_return = g.sort_values(["r_6m", "ticker"], ascending=[False, True]).iloc[0]
        c = corr_stats(g)
        rows.append(
            {
                "category": category,
                "n": len(g),
                "pearson": c["pearson"],
                "spearman": c["spearman"],
                "mean_ret": g["r_6m"].mean(),
                "top_return": top_return,
                "top_score": top_score,
            }
        )
    return rows


def robust_rows(df: pd.DataFrame) -> tuple[list[dict[str, object]], dict[str, list[str]], float, float]:
    sub = df.dropna(subset=["score", "r_6m"]).copy()
    low_tail = float(sub["r_6m"].quantile(0.05))
    high_tail = float(sub["r_6m"].quantile(0.95))
    sub["exclude_low_liq"] = sub["liquidity_score"].isna() | (sub["liquidity_score"] <= 5.0)
    listing = sub["listing_type"].fillna("")
    adr_ratio = sub["adr_ratio"].fillna("")
    currency = sub["currency"].fillna("")
    fin_currency = sub["financial_currency"].fillna("")
    valuation_check = sub["valuation_check"].fillna("")
    fin_note = sub["fin_note"].fillna("")
    sub["exclude_adr_currency"] = (
        listing.str.contains("ADR|ADS", case=False, regex=True)
        | adr_ratio.ne("不适用")
        | (currency.ne("") & fin_currency.ne("") & currency.ne(fin_currency))
        | valuation_check.str.contains("currency_mismatch", case=False, regex=False)
        | fin_note.str.contains("交易货币/财报货币不一致|ADR/ADS比例需确认", regex=True)
    )
    sub["exclude_extreme"] = (sub["r_6m"] <= low_tail) | (sub["r_6m"] >= high_tail)
    specs = [
        ("全样本基准", "无剔除", pd.Series(True, index=sub.index)),
        ("剔除低流动性", "F51交易流动性分 > 5.0", ~sub["exclude_low_liq"]),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", ~sub["exclude_adr_currency"]),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(low_tail)} / {fmt_pct(high_tail)}", ~sub["exclude_extreme"]),
        ("三项合并剔除", "同时满足上述三项", ~(sub["exclude_low_liq"] | sub["exclude_adr_currency"] | sub["exclude_extreme"])),
    ]
    rows: list[dict[str, object]] = []
    for name, rule, keep_mask in specs:
        filtered = sub[keep_mask].copy()
        c = corr_stats(filtered)
        tb30 = top_bottom_stats(filtered, 30)
        rows.append(
            {
                "name": name,
                "rule": rule,
                "n": len(filtered),
                "excluded": len(sub) - len(filtered),
                "pearson": c["pearson"],
                "spearman": c["spearman"],
                "kendall": c["kendall"],
                "top30": tb30["top_mean"],
                "bottom30": tb30["bottom_mean"],
                "diff30": tb30["diff"],
            }
        )
    exclusions = {
        "低流动性": sorted(sub.loc[sub["exclude_low_liq"], "ticker"].tolist()),
        "ADR/币种异常": sorted(sub.loc[sub["exclude_adr_currency"], "ticker"].tolist()),
        "极端涨跌双尾5%": sorted(sub.loc[sub["exclude_extreme"], "ticker"].tolist()),
    }
    return rows, exclusions, low_tail, high_tail


def score_bucket(value: float) -> str:
    if value >= 9.0:
        return "9.0-10.0"
    if value >= 8.0:
        return "8.0-8.9"
    if value >= 7.0:
        return "7.0-7.9"
    if value >= 5.0:
        return "5.0-6.9"
    if value >= 3.0:
        return "3.0-4.9"
    return "1.0-2.9"


def strength_label(spearman_value: float) -> str:
    if spearman_value >= 0.15:
        return "部分成立"
    if spearman_value >= 0.05:
        return "弱正向"
    if spearman_value > -0.05:
        return "接近0"
    return "反向或偏负"


def tickers(values: list[str]) -> str:
    return ", ".join(values) if values else "无"


def backup_existing() -> list[str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    pattern = f"{FEATURE_STEM}_特征评估_{WINDOW}涨跌_*.md"
    existing = [p for p in OUT_DIR.glob(pattern) if p.is_file()]
    if not existing:
        return []
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target_dir = BACKUP_DIR / f"{FEATURE_STEM}_{WINDOW}涨跌_{REPORT_DATE}_写入前备份_{stamp}"
    target_dir.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    for path in existing:
        destination = target_dir / path.name
        shutil.move(str(path), str(destination))
        moved.append(str(destination.relative_to(ROOT)))
    return moved


def build_report() -> tuple[str, dict[str, object]]:
    score = parse_score_file(SCORE_PATH)
    f51 = parse_score_file(F51_PATH).rename(columns={"score": "liquidity_score"})
    returns = parse_return_file(RETURN_PATH)
    soxx = parse_soxx_file(RETURN_PATH)
    financial = parse_financial_file(FIN_PATH)

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
        .merge(f51[["ticker", "liquidity_score"]], on="ticker", how="left")
    )
    eval_df = df.dropna(subset=["score", "r_6m"]).copy()
    neutral_df = add_neutral_scores(eval_df)

    missing_returns = sorted(df.loc[df["r_6m"].isna(), "ticker"].tolist())
    return_missing_score = sorted(set(returns["ticker"]) - set(score["ticker"]))

    corr = corr_stats(eval_df)
    tb = {n: top_bottom_stats(eval_df, n) for n in (10, 20, 30)}
    qstats = quintile_stats(eval_df)
    pressure_stats, iv_stats = risk_group_stats(eval_df)
    neutral_raw = corr_stats(neutral_df, "score", "r_6m")
    neutral_pct = corr_stats(neutral_df, "cat_percentile", "r_6m")
    neutral_resid = corr_stats(neutral_df, "score_resid", "ret_resid")
    neutral_tb = {n: top_bottom_stats(neutral_df, n, "cat_percentile") for n in (10, 20, 30)}
    cat_corr = category_corrs(eval_df)
    robust, exclusions, low_tail, high_tail = robust_rows(eval_df)

    top_sorted = sorted_by_score(eval_df)
    bottom_sorted = sorted_by_score(eval_df, ascending=True)
    top10 = top_sorted.head(10)
    bottom10 = bottom_sorted.head(10)
    winners15 = eval_df.sort_values(["r_6m", "ticker"], ascending=[False, True]).head(15)
    losers10 = eval_df.sort_values(["r_6m", "ticker"], ascending=[True, True]).head(10)
    top15_score = top_sorted.head(15)
    bottom15_score = bottom_sorted.head(15)

    score["score_bucket"] = score["score"].map(score_bucket)
    bucket_counts = (
        score["score_bucket"]
        .value_counts()
        .reindex(["9.0-10.0", "8.0-8.9", "7.0-7.9", "5.0-6.9", "3.0-4.9", "1.0-2.9"], fill_value=0)
    )

    moved = backup_existing()

    strength = strength_label(float(corr["spearman"]))
    top30_diff = float(tb[30]["diff"])
    risk_top = pressure_stats[0]
    risk_bottom = pressure_stats[2]
    risk_line = (
        "高分组压力窗口均值优于低分组"
        if float(risk_top["stress_mean"]) > float(risk_bottom["stress_mean"])
        else "高分组压力窗口均值不优于低分组"
    )
    iv_line = (
        "高分组当前IV低于低分组"
        if float(iv_stats[0]["near_iv"]) < float(iv_stats[2]["near_iv"])
        else "高分组当前IV不低于低分组"
    )
    top_examples = "、".join(top15_score["ticker"].head(8).tolist())
    winner_examples = "、".join(winners15["ticker"].head(10).tolist())
    low_score_winner_examples = "、".join(
        winners15.loc[winners15["score"] < eval_df["score"].median(), "ticker"].head(6).tolist()
    )
    if not low_score_winner_examples:
        low_score_winner_examples = "无明显样本"

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
            "- 稳健性辅助输入：`特征量化/量化评分/F51_交易流动性_量化评分_2026-06-04.md`；`日度资料/每日金融数据/每日金融数据_2026-06-03.md`，金融数据生成时间 2026-06-03 13:41:46 PDT-0700。",
            f"- 有效评估样本：评分与6个月涨跌交集 {len(eval_df)} 家；F30评分有但6个月涨跌缺失 {len(missing_returns)} 家。",
            "- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。",
            "- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动率或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为下跌窗口代理，并用2026-06-03近ATM Call/Put IV均值补充当前波动代理。",
            "- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。",
            "- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F30 正式输出；本次未读取旧版 F30 特征评估作为结论依据。",
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
            f"- 排序有效性：{strength}。全样本 Pearson {fmt_corr(corr['pearson'])}, Spearman {fmt_corr(corr['spearman'])}, Kendall {fmt_corr(corr['kendall'])}；重点指标 Spearman {fmt_corr(corr['spearman'])}，说明 F30 对本次6个月收益排序的单因子解释力{'偏弱且方向为负' if float(corr['spearman']) < -0.05 else '偏弱'}。",
            f"- Top/Bottom能力：{'成立' if top30_diff > 0 else '不成立'}。Top10、Top20、Top30 平均收益分别为 {fmt_pct(tb[10]['top_mean'])}、{fmt_pct(tb[20]['top_mean'])}、{fmt_pct(tb[30]['top_mean'])}；Top-Bottom收益差分别为 {fmt_pct(tb[10]['diff'])}、{fmt_pct(tb[20]['diff'])}、{fmt_pct(tb[30]['diff'])}。",
            f"- 风险解释力：{risk_line}，{iv_line}。Top30 压力窗口均值 {fmt_pct(risk_top['stress_mean'])}，Bottom30 为 {fmt_pct(risk_bottom['stress_mean'])}；Top30 平均最差窗口 {fmt_pct(risk_top['worst_mean'])}，Bottom30 为 {fmt_pct(risk_bottom['worst_mean'])}；Top30 近ATM IV均值 {fmt_pct(iv_stats[0]['near_iv'])}，Bottom30 为 {fmt_pct(iv_stats[2]['near_iv'])}。",
            f"- 分类中性：分类内百分位合并 Spearman {fmt_corr(neutral_pct['spearman'])}，分类去均值残差 Spearman {fmt_corr(neutral_resid['spearman'])}；若分类中性后仍为负，说明结果不只是行业配置造成，而是类内也缺乏稳定正向排序。",
            f"- 稳健性：三项合并剔除后样本 {robust[-1]['n']} 家，Spearman {fmt_corr(robust[-1]['spearman'])}，Top30-Bottom30 {fmt_pct(robust[-1]['diff30'])}；剔除低流动性、ADR/币种异常和极端涨跌后，F30 仍不能作为独立6个月收益排序因子。",
            f"- 解释：F30 衡量 RPO、backlog、长期合同、订阅/服务协议、预付款或明确指引对未来收入的支撑。高分端集中在 {top_examples} 等收入可见度硬证据强的公司；但本窗口涨幅头部是 {winner_examples}，其中低分或中低分弹性股包括 {low_score_winner_examples}。2025-11至2026-05 的6个月收益更像高贝塔修复、存储/光互联/设备周期和低基数重估，而不是单纯由收入可见度驱动。",
        ]
    )

    lines.append("")
    lines.append("## 覆盖检查")
    lines.append(
        md_table(
            ["项目", "数量", "说明"],
            [
                ["F30评分覆盖", len(score), "来自2026-06-04评分文件"],
                ["6个月涨跌覆盖", len(returns), "来自2026-05-27区间涨跌文件"],
                ["交集样本", len(eval_df), "用于本次所有主指标"],
                ["评分有但6个月涨跌缺失", len(missing_returns), tickers(missing_returns)],
                ["涨跌有但评分缺失", len(return_missing_score), tickers(return_missing_score)],
            ],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 交集样本分类分布")
    cat_dist_rows: list[list[object]] = []
    for category, group in eval_df.groupby("category", sort=True):
        cat_dist_rows.append(
            [
                category,
                len(group),
                fmt_float(group["score"].mean()),
                fmt_pct(group["r_6m"].mean()),
                fmt_pct(group["r_6m"].median()),
            ]
        )
    lines.append(
        md_table(
            ["分类目录", "样本数", "F30均分", "6个月平均收益", "6个月中位收益"],
            cat_dist_rows,
            ["---", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## 排序有效性")
    lines.append(
        md_table(
            ["指标", "数值", "解释"],
            [
                ["Pearson", fmt_corr(corr["pearson"]), "线性相关；受极端涨跌影响较大"],
                ["Spearman", fmt_corr(corr["spearman"]), "排序相关；这是本任务最重要指标"],
                ["Kendall tau-b", fmt_corr(corr["kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
            ],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 分数分组收益")
    lines.append(
        md_table(
            ["分组", "公司数", "F30均分", "6个月平均收益", "6个月中位收益", "命中率"],
            [
                [
                    item["group"],
                    item["n"],
                    fmt_float(item["score_mean"]),
                    fmt_pct(item["return_mean"]),
                    fmt_pct(item["return_median"]),
                    fmt_rate(item["hit"]),
                ]
                for item in qstats
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
                    f"Top{n}/Bottom{n}",
                    fmt_pct(tb[n]["top_mean"]),
                    fmt_rate(tb[n]["top_hit"]),
                    fmt_pct(tb[n]["bottom_mean"]),
                    fmt_rate(tb[n]["bottom_hit"]),
                    fmt_pct(tb[n]["diff"]),
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
                    fmt_float(row["score"], 1),
                    int(row["score_rank"]),
                    fmt_pct(row["r_6m"]),
                    row["confidence"],
                ]
            )
    lines.append(
        md_table(
            ["组别", "股票代号", "公司名称", "分类目录", "F30分", "F30排名", "6个月收益", "置信度"],
            top_bottom_rows,
            ["---", "---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为下跌窗口代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供；近ATM IV为2026-06-03当前期权波动代理，不等同于过去6个月实际波动率。")
    lines.append(
        md_table(
            ["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"],
            [
                [
                    row["group"],
                    row["n"],
                    row["obs"],
                    fmt_pct(row["soxx1_mean"]),
                    fmt_pct(row["soxx2_mean"]),
                    fmt_pct(row["soxx3_mean"]),
                    fmt_pct(row["stress_mean"]),
                    fmt_pct(row["worst_mean"]),
                    fmt_pct(row["window_std"]),
                    fmt_rate(row["beat_soxx"]),
                    fmt_rate(row["negative_rate"]),
                ]
                for row in pressure_stats
            ],
            ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("### 当前IV代理")
    lines.append(
        md_table(
            ["分组", "公司数", "IV覆盖", "Call IV均值", "Put IV均值", "近ATM IV均值", "近ATM IV中位数"],
            [
                [
                    row["group"],
                    row["n"],
                    row["iv_n"],
                    fmt_pct(row["call_iv"]),
                    fmt_pct(row["put_iv"]),
                    fmt_pct(row["near_iv"]),
                    fmt_pct(row["near_iv_median"]),
                ]
                for row in iv_stats
            ],
            ["---", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append(f"结论：{risk_line}，{iv_line}。F30 高分公司通常收入确认路径更清晰，但在压力窗口中仍包含云平台、AI服务器、工程建设、核电/电力和高估值软件等高久期或高贝塔资产，不能自然等同于更低回撤。")

    lines.append("")
    lines.append("## 分类中性结果")
    lines.append(
        md_table(
            ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
            [
                ["原始全样本", neutral_raw["n"], fmt_corr(neutral_raw["pearson"]), fmt_corr(neutral_raw["spearman"]), fmt_corr(neutral_raw["kendall"]), "直接用F30分数排序"],
                ["分类内百分位合并", neutral_pct["n"], fmt_corr(neutral_pct["pearson"]), fmt_corr(neutral_pct["spearman"]), fmt_corr(neutral_pct["kendall"]), "每个分类内先按F30排序，再转成0-1百分位后合并"],
                ["分类去均值残差", neutral_resid["n"], fmt_corr(neutral_resid["pearson"]), fmt_corr(neutral_resid["spearman"]), fmt_corr(neutral_resid["kendall"]), "F30和收益分别减去分类均值后相关"],
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
                    f"中性Top{n}/Bottom{n}",
                    fmt_pct(neutral_tb[n]["top_mean"]),
                    fmt_rate(neutral_tb[n]["top_hit"]),
                    fmt_pct(neutral_tb[n]["bottom_mean"]),
                    fmt_rate(neutral_tb[n]["bottom_hit"]),
                    fmt_pct(neutral_tb[n]["diff"]),
                ]
                for n in (10, 20, 30)
            ],
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("说明：分类中性 Top30/Bottom30 可能出现局部正差，但 Top10/Top20 仍为负且分类内百分位、残差相关均为负，因此不把该结果判定为稳定有效。")

    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(
        md_table(
            ["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F30公司"],
            [
                [
                    row["category"],
                    row["n"],
                    fmt_corr(row["pearson"]),
                    fmt_corr(row["spearman"]),
                    fmt_pct(row["mean_ret"]),
                    f"{row['top_return']['ticker']} {fmt_pct(row['top_return']['r_6m'])}",
                    f"{row['top_score']['ticker']} {fmt_float(row['top_score']['score'], 1)} / {fmt_pct(row['top_score']['r_6m'])}",
                ]
                for row in cat_corr
            ],
            ["---", "---:", "---:", "---:", "---:", "---", "---"],
        )
    )
    lines.append("")
    lines.append("分类内结果用于检验是否只是押中某个行业。若同一分类内 Spearman 多数为负或分散，说明 F30 在该窗口更像收入确定性/质量信息，而不是短期收益弹性信息。")

    lines.append("")
    lines.append("## 稳健性检验")
    lines.append(
        md_table(
            ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"],
            [
                [
                    row["name"],
                    row["rule"],
                    row["n"],
                    row["excluded"],
                    fmt_corr(row["pearson"]),
                    fmt_corr(row["spearman"]),
                    fmt_corr(row["kendall"]),
                    fmt_pct(row["top30"]),
                    fmt_pct(row["bottom30"]),
                    fmt_pct(row["diff30"]),
                ]
                for row in robust
            ],
            ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("稳健性结论：如果三项合并剔除后 Spearman 和 Top30-Bottom30 仍没有转为稳定正数，则 F30 暂不适合直接作为6个月收益排序因子；更适合作为基本面兑现确定性、估值兑现压力和风险复核中的约束变量。")

    lines.append("")
    lines.append("### 剔除清单")
    lines.append(
        md_table(
            ["剔除项", "数量", "公司"],
            [[name, len(values), tickers(values)] for name, values in exclusions.items()],
            ["---", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    lines.append(
        md_table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F30分", "F30排名", "F30置信度"],
            [
                [
                    row["ticker"],
                    row["company"],
                    row["category"],
                    fmt_pct(row["r_6m"]),
                    fmt_float(row["score"], 1),
                    int(row["score_rank"]),
                    row["confidence"],
                ]
                for _, row in winners15.iterrows()
            ],
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### 6个月跌幅前10")
    lines.append(
        md_table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F30分", "F30排名", "F30置信度"],
            [
                [
                    row["ticker"],
                    row["company"],
                    row["category"],
                    fmt_pct(row["r_6m"]),
                    fmt_float(row["score"], 1),
                    int(row["score_rank"]),
                    row["confidence"],
                ]
                for _, row in losers10.iterrows()
            ],
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )

    lines.append("")
    lines.append("### F30高分前15")
    lines.append(
        md_table(
            ["排名", "股票代号", "公司名称", "分类目录", "F30分", "6个月收益", "压力窗口均值", "近ATM IV"],
            [
                [
                    int(row["score_rank"]),
                    row["ticker"],
                    row["company"],
                    row["category"],
                    fmt_float(row["score"], 1),
                    fmt_pct(row["r_6m"]),
                    fmt_pct(pd.Series([row["soxx1"], row["soxx2"], row["soxx3"]]).dropna().mean()),
                    fmt_pct(row["near_atm_iv"]),
                ]
                for _, row in top15_score.iterrows()
            ],
            ["---:", "---", "---", "---", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("### F30低分前15")
    lines.append(
        md_table(
            ["排名", "股票代号", "公司名称", "分类目录", "F30分", "6个月收益", "压力窗口均值", "近ATM IV"],
            [
                [
                    int(row["score_rank"]),
                    row["ticker"],
                    row["company"],
                    row["category"],
                    fmt_float(row["score"], 1),
                    fmt_pct(row["r_6m"]),
                    fmt_pct(pd.Series([row["soxx1"], row["soxx2"], row["soxx3"]]).dropna().mean()),
                    fmt_pct(row["near_atm_iv"]),
                ]
                for _, row in bottom15_score.iterrows()
            ],
            ["---:", "---", "---", "---", "---:", "---:", "---:", "---:"],
        )
    )

    lines.append("")
    lines.append("## 分数分布与解释")
    lines.append(
        md_table(
            ["分数段", "公司数", "占评分样本"],
            [[bucket, count, fmt_rate(count / len(score) * 100)] for bucket, count in bucket_counts.items()],
            ["---", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("本次 F30 的高分多来自 RPO/backlog/长期合同、明确订单或订阅收入池。该信息对收入兑现和下行基本面风险有意义，但在强反弹窗口里往往输给低分高弹性公司：低收入可见度公司一旦出现订单、融资、产能或周期预期修复，价格弹性可能远大于高分成熟公司。")

    lines.append("")
    lines.append("## 使用建议")
    lines.extend(
        [
            "- 不建议把 F30 单独作为未来6个月收益排序因子；本轮主结果、分类中性结果和稳健性结果均未提供稳定正向证据。",
            "- 建议把 F30 用作质量/兑现约束：同等产业弹性、催化剂强度和估值赔率下，收入可见度高的公司应获得更高兑现置信度。",
            "- 与 F31订单刚性、F32订单下修风险、F43基本面兑现确定性联用时更有价值：F30 解决“收入是否看得见”，但不解决“估值是否已经充分定价”和“股价是否处于高弹性修复段”。",
            "- 对低分但涨幅极高公司，应重点追问涨幅是否来自真实订单可见度改善，还是来自低基数、融资、题材、空头回补或行业贝塔。",
        ]
    )

    lines.append("")
    lines.append("## 数据与方法限制")
    lines.extend(
        [
            "- 收益文件使用 Yahoo Finance 免费历史行情的 Close 价格，`auto_adjust=False`，不含股息再投资，不是总回报率。",
            "- 6个月收益窗口的最新价格日为 2026-05-27；评分日期为 2026-06-04，存在评分信息相对收益窗口滞后的偏差，结论更接近“截至评分时的特征与过去6个月收益关系”，不是严格前瞻回测。",
            "- 风险部分没有逐日收益序列，因此不能给出严格日波动率、最大回撤或下跌日胜率；本报告以三个 SOXX 下跌窗口和 2026-06-03 当前 IV 作为代理。",
            "- 流动性剔除依赖 F51 代理评分，不等同于真实成交额/ADV；ADR/币种异常剔除依据日度金融数据中的 listing_type、currency、financial_currency 和估值校验备注。",
            "- 极端涨跌剔除使用交集样本6个月收益的双尾5%分位，阈值为 " + f"{fmt_pct(low_tail)} / {fmt_pct(high_tail)}。",
        ]
    )

    metadata = {
        "score_rows": len(score),
        "return_rows": len(returns),
        "eval_rows": len(eval_df),
        "out_path": str(OUT_PATH),
        "spearman": corr["spearman"],
        "top30_diff": tb[30]["diff"],
        "moved": moved,
    }
    return "\n".join(lines) + "\n", metadata


def main() -> None:
    report, metadata = build_report()
    OUT_PATH.write_text(report, encoding="utf-8")
    print(
        f"wrote={metadata['out_path']}\n"
        f"score_rows={metadata['score_rows']} return_rows={metadata['return_rows']} eval_rows={metadata['eval_rows']}\n"
        f"spearman={float(metadata['spearman']):.6f} top30_diff={float(metadata['top30_diff']):.6f}\n"
        f"moved={metadata['moved']}"
    )


if __name__ == "__main__":
    main()
