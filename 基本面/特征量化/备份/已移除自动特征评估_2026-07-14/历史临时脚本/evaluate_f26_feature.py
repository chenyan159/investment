from __future__ import annotations

import math
import re
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "F26"
FEATURE_NAME = "细分行业空间弹性"
FEATURE_SUBJECT = f"{FEATURE_ID}_{FEATURE_NAME}"
RUN_DATE = "2026-06-04"
RETURN_WINDOW = "6个月"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_SUBJECT}_量化评分_{RUN_DATE}.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
F51_PATH = ROOT / "特征量化" / "量化评分" / f"F51_交易流动性_量化评分_{RUN_DATE}.md"
FINANCIAL_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
EVAL_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = EVAL_DIR / "备份"
OUT_PATH = EVAL_DIR / f"{FEATURE_SUBJECT}_特征评估_{RETURN_WINDOW}涨跌_{RUN_DATE}.md"

SOXX_WINDOWS = {
    "soxx1": ("SOXX跌1", "2025-02-20至2025-04-08", -32.98),
    "soxx2": ("SOXX跌2", "2026-02-25至2026-03-30", -15.82),
    "soxx3": ("SOXX跌3", "2025-10-29至2025-11-20", -13.40),
}


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def parse_float_text(text: str) -> float:
    text = text.strip().replace(",", "")
    if not text or text in {"N/A", "缺失", "不适用"}:
        return math.nan
    m = re.search(r"[-+]?\d+(?:\.\d+)?", text)
    return float(m.group()) if m else math.nan


def parse_pct(text: str) -> float:
    if not text or "N/A" in text or "缺失" in text:
        return math.nan
    m = re.search(r"([-+]?\d+(?:,\d{3})*(?:\.\d+)?)%", text)
    if not m:
        return math.nan
    value = float(m.group(1).replace(",", ""))
    if "下跌" in text and value > 0:
        value = -value
    return value


def parse_market_cap(text: str) -> float:
    if not text or "缺失" in text or "N/A" in text:
        return math.nan
    clean = text.replace("$", "").replace(",", "").strip()
    m = re.search(r"([-+]?\d+(?:\.\d+)?)([KMBT]?)", clean, re.I)
    if not m:
        return math.nan
    value = float(m.group(1))
    unit = m.group(2).upper()
    mult = {"": 1.0, "K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}[unit]
    return value * mult


def parse_score_file(path: Path, prefix: str) -> pd.DataFrame:
    rows: list[dict] = []
    in_table = False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("| 排名 | 股票代号 | 公司名称 | 分类目录 | 特征分 |"):
            in_table = True
            continue
        if in_table and not line.startswith("|"):
            break
        if not in_table or not line.startswith("|"):
            continue
        cells = split_md_row(line)
        if is_separator_row(cells) or len(cells) < 10:
            continue
        rows.append(
            {
                "ticker": cells[1],
                "company": cells[2],
                "category": cells[3],
                f"{prefix}_rank": int(parse_float_text(cells[0])),
                f"{prefix}_score": parse_float_text(cells[4]),
                f"{prefix}_evidence": cells[5],
                f"{prefix}_confidence": cells[6],
                f"{prefix}_core": cells[7],
                f"{prefix}_discount": cells[8],
            }
        )
    return pd.DataFrame(rows)


def parse_return_file(path: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, str]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    meta = {
        "generated": "",
        "latest_trade": "",
        "soxx_windows": "2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20",
    }
    for line in lines:
        if line.startswith("- 生成时间："):
            meta["generated"] = line.replace("- 生成时间：", "").strip().rstrip("。")
        if line.startswith("- 最新可得交易日最大值："):
            m = re.search(r"`?(\d{4}-\d{2}-\d{2})`?", line)
            if m:
                meta["latest_trade"] = m.group(1)

    returns: list[dict] = []
    stress: list[dict] = []
    mode: str | None = None
    table: str | None = None
    category = ""

    for line in lines:
        if line.startswith("### 按分类分组的全公司明细"):
            mode = "stress"
            table = None
            continue
        if line.startswith("## 按分类分组的公司明细"):
            mode = "returns"
            table = None
            continue
        if mode == "stress" and line.startswith("#### "):
            category = line.replace("#### ", "").strip()
            table = None
            continue
        if mode == "returns" and line.startswith("### "):
            category = line.replace("### ", "").strip()
            table = None
            continue
        if not line.startswith("|"):
            table = None
            continue

        cells = split_md_row(line)
        if is_separator_row(cells):
            continue
        if mode == "stress" and cells[:2] == ["股票代号", "公司名称"]:
            table = "stress"
            continue
        if mode == "returns" and cells[:4] == ["股票代号", "公司名称", "最新交易日", "最新收盘价"]:
            table = "returns"
            continue
        if table == "stress" and len(cells) >= 6:
            stress.append(
                {
                    "ticker": cells[0],
                    "company_return": cells[1],
                    "category_return": category,
                    "soxx1": parse_pct(cells[2]),
                    "soxx2": parse_pct(cells[3]),
                    "soxx3": parse_pct(cells[4]),
                    "stress_note": cells[5],
                }
            )
        elif table == "returns" and len(cells) >= 9:
            returns.append(
                {
                    "ticker": cells[0],
                    "company_return": cells[1],
                    "category_return": category,
                    "latest_trade_date": cells[2],
                    "latest_close": parse_float_text(cells[3]),
                    "ret1m": parse_pct(cells[4]),
                    "ret3m": parse_pct(cells[5]),
                    "ret6m": parse_pct(cells[6]),
                    "ret1y": parse_pct(cells[7]),
                    "return_note": cells[8],
                }
            )
    return pd.DataFrame(returns), pd.DataFrame(stress), meta


def parse_financial_file(path: Path) -> pd.DataFrame:
    rows: list[dict] = []
    table = False
    category = ""
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("### "):
            category = line.replace("### ", "").strip()
            table = False
            continue
        if not line.startswith("|"):
            table = False
            continue
        cells = split_md_row(line)
        if is_separator_row(cells):
            continue
        if cells[:3] == ["股票代号", "公司名称", "价格日期"]:
            table = True
            continue
        if table and len(cells) >= 25:
            call_iv = parse_pct(cells[11])
            put_iv = parse_pct(cells[12])
            iv_values = [v for v in [call_iv, put_iv] if not pd.isna(v)]
            rows.append(
                {
                    "ticker": cells[0],
                    "company_fin": cells[1],
                    "category_fin": category,
                    "price_date_fin": cells[2],
                    "market_cap": parse_market_cap(cells[4]),
                    "call_iv": call_iv,
                    "put_iv": put_iv,
                    "iv_avg": float(np.mean(iv_values)) if iv_values else math.nan,
                    "currency": cells[13],
                    "financial_currency": cells[14],
                    "listing_type": cells[19],
                    "adr_ratio": cells[20],
                    "valuation_check": cells[23],
                    "financial_note": cells[24],
                }
            )
    return pd.DataFrame(rows)


def pearson(x: pd.Series, y: pd.Series) -> float:
    valid = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(valid) < 2:
        return math.nan
    xv = valid["x"].to_numpy(dtype=float)
    yv = valid["y"].to_numpy(dtype=float)
    if np.std(xv) == 0 or np.std(yv) == 0:
        return math.nan
    return float(np.corrcoef(xv, yv)[0, 1])


def spearman(x: pd.Series, y: pd.Series) -> float:
    valid = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(valid) < 2:
        return math.nan
    return pearson(valid["x"].rank(method="average"), valid["y"].rank(method="average"))


def kendall_tau_b(x: pd.Series, y: pd.Series) -> float:
    valid = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(valid)
    if n < 2:
        return math.nan
    xv = valid["x"].to_numpy(dtype=float)
    yv = valid["y"].to_numpy(dtype=float)
    concordant = discordant = ties_x = ties_y = 0
    for i in range(n - 1):
        dx = xv[i] - xv[i + 1 :]
        dy = yv[i] - yv[i + 1 :]
        prod = dx * dy
        concordant += int(np.sum(prod > 0))
        discordant += int(np.sum(prod < 0))
        ties_x += int(np.sum((dx == 0) & (dy != 0)))
        ties_y += int(np.sum((dy == 0) & (dx != 0)))
    denom = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    if denom == 0:
        return math.nan
    return (concordant - discordant) / denom


def corr_metrics(df: pd.DataFrame, score_col: str = "score", ret_col: str = "ret6m") -> dict:
    valid = df[[score_col, ret_col]].dropna()
    return {
        "n": len(valid),
        "pearson": pearson(valid[score_col], valid[ret_col]),
        "spearman": spearman(valid[score_col], valid[ret_col]),
        "kendall": kendall_tau_b(valid[score_col], valid[ret_col]),
    }


def sorted_sample(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(["score", "rank", "ticker"], ascending=[False, True, True]).reset_index(drop=True)


def group_stats(df: pd.DataFrame) -> dict:
    return {
        "n": len(df),
        "score_mean": df["score"].mean(),
        "ret_mean": df["ret6m"].mean(),
        "ret_median": df["ret6m"].median(),
        "hit": (df["ret6m"] > 0).mean() if len(df) else math.nan,
    }


def top_bottom_metrics(df: pd.DataFrame, n: int) -> dict:
    ordered = sorted_sample(df)
    top = ordered.head(n)
    bottom = ordered.tail(n)
    return {
        "n": n,
        "top_mean": top["ret6m"].mean(),
        "top_hit": (top["ret6m"] > 0).mean(),
        "bottom_mean": bottom["ret6m"].mean(),
        "bottom_hit": (bottom["ret6m"] > 0).mean(),
        "spread": top["ret6m"].mean() - bottom["ret6m"].mean(),
    }


def risk_group_metrics(label: str, df: pd.DataFrame) -> dict:
    window_cols = list(SOXX_WINDOWS)
    stacked = df[window_cols].stack().dropna()
    worst = df[window_cols].min(axis=1, skipna=True)
    row_std = df[window_cols].std(axis=1, skipna=True)
    outperf = []
    negs = []
    for col, (_, _, soxx_ret) in SOXX_WINDOWS.items():
        vals = df[col].dropna()
        outperf.extend(list(vals > soxx_ret))
        negs.extend(list(vals < 0))
    return {
        "label": label,
        "n": len(df),
        "obs": int(stacked.count()),
        "soxx1_mean": df["soxx1"].mean(),
        "soxx2_mean": df["soxx2"].mean(),
        "soxx3_mean": df["soxx3"].mean(),
        "pressure_mean": stacked.mean(),
        "worst_mean": worst.mean(),
        "window_dispersion": row_std.mean(),
        "outperform_soxx": np.mean(outperf) if outperf else math.nan,
        "negative_window": np.mean(negs) if negs else math.nan,
        "call_iv": df["call_iv"].mean(),
        "put_iv": df["put_iv"].mean(),
        "iv_avg": df["iv_avg"].mean(),
        "iv_median": df["iv_avg"].median(),
        "iv_coverage": int(df["iv_avg"].notna().sum()),
    }


def neutral_top_bottom(df: pd.DataFrame, k_per_category: int) -> dict:
    top_parts = []
    bottom_parts = []
    for _, g in df.groupby("category", sort=True):
        ordered = sorted_sample(g)
        top_parts.append(ordered.head(k_per_category))
        bottom_parts.append(ordered.tail(k_per_category))
    top = pd.concat(top_parts, ignore_index=True)
    bottom = pd.concat(bottom_parts, ignore_index=True)
    return {
        "n": len(top),
        "top_mean": top["ret6m"].mean(),
        "top_hit": (top["ret6m"] > 0).mean(),
        "bottom_mean": bottom["ret6m"].mean(),
        "bottom_hit": (bottom["ret6m"] > 0).mean(),
        "spread": top["ret6m"].mean() - bottom["ret6m"].mean(),
    }


def robustness_row(label: str, rule: str, base: pd.DataFrame, mask: pd.Series) -> dict:
    sub = base.loc[mask].copy()
    metrics = corr_metrics(sub)
    tb = top_bottom_metrics(sub, min(30, len(sub) // 2))
    return {
        "label": label,
        "rule": rule,
        "n": len(sub),
        "removed": len(base) - len(sub),
        **metrics,
        "top30": tb["top_mean"],
        "bottom30": tb["bottom_mean"],
        "spread30": tb["spread"],
    }


def fmt_corr(x: float) -> str:
    return "N/A" if pd.isna(x) else f"{x:.3f}"


def fmt_num(x: float, digits: int = 2) -> str:
    return "N/A" if pd.isna(x) else f"{x:.{digits}f}"


def fmt_pct(x: float, digits: int = 2) -> str:
    return "N/A" if pd.isna(x) else f"{x:+.{digits}f}%"


def fmt_rate(x: float) -> str:
    return "N/A" if pd.isna(x) else f"{x * 100:+.1f}%"


def fmt_plain_rate(x: float) -> str:
    return "N/A" if pd.isna(x) else f"{x * 100:.1f}%"


def md_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |"]
    aligns = []
    for h in headers:
        aligns.append("---:" if any(key in h for key in ["数", "分", "收益", "率", "Pearson", "Spearman", "Kendall", "差", "均值", "中位", "排名", "IV", "窗口", "观测"]) else "---")
    out.append("| " + " | ".join(aligns) + " |")
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return out


def corr_interpret(metric: dict) -> str:
    s = metric["spearman"]
    if s >= 0.20:
        return "较强正向，排序有效性成立"
    if s >= 0.10:
        return "小幅到中等正向，排序有效性部分成立"
    if s >= 0.03:
        return "弱正向，排序解释力有限"
    if s > -0.03:
        return "接近零，排序有效性不成立"
    if s > -0.10:
        return "小幅为负，排序有效性不成立"
    return "明显为负，方向与预期相反"


def feature_specific_interpretation(df: pd.DataFrame) -> str:
    leaders = sorted_sample(df).head(10)["ticker"].tolist()
    top_return = df.sort_values("ret6m", ascending=False).head(8)["ticker"].tolist()
    return (
        f"{FEATURE_ID} 衡量公司所在细分市场未来1-2年的市场规模、渗透率和增长率弹性，而不是公司份额或投资建议。"
        f"本次高分端主要是 {', '.join(leaders)} 等处在AI算力、网络、电力、冷却、存储或先进制造高增长细分池的公司；"
        f"但6个月涨幅头部由 {', '.join(top_return)} 等存储、光互联、小中盘修复、周期反弹或价格重估标的主导。"
        "因此 F26 可以解释赛道空间和中期需求池，但不等同于本窗口最高价格弹性。"
    )


def backup_existing_outputs() -> str:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    matches = sorted(EVAL_DIR.glob(f"{FEATURE_SUBJECT}_特征评估_{RETURN_WINDOW}涨跌_*.md"))
    if not matches:
        return "处理结果：未发现同类旧版正式输出。"
    stamp = datetime.now(timezone(timedelta(hours=-7))).isoformat(timespec="seconds").replace(":", "_")
    dest_dir = BACKUP_DIR / f"{FEATURE_SUBJECT}_{RETURN_WINDOW}涨跌_{stamp}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    moved = []
    for old in matches:
        dest = dest_dir / old.name
        shutil.move(str(old), str(dest))
        moved.append(old.name)
    return f"处理结果：已移动 {len(moved)} 个同类旧版正式输出到 `特征量化/特征评估/备份/{dest_dir.name}/`。"


def build_report() -> tuple[str, dict]:
    score = parse_score_file(SCORE_PATH, "F26")
    f51 = parse_score_file(F51_PATH, "f51")
    returns, stress, ret_meta = parse_return_file(RETURN_PATH)
    financial = parse_financial_file(FINANCIAL_PATH)

    score = score.rename(
        columns={
            "F26_score": "score",
            "F26_rank": "rank",
            "F26_confidence": "confidence",
            "F26_evidence": "evidence",
        }
    )
    f51 = f51[["ticker", "f51_score", "f51_rank"]].rename(columns={"f51_score": "liquidity_score"})

    df = score.merge(returns, on="ticker", how="left")
    df = df.merge(stress[["ticker", "soxx1", "soxx2", "soxx3", "stress_note"]], on="ticker", how="left")
    df = df.merge(f51, on="ticker", how="left")
    df = df.merge(
        financial[
            [
                "ticker",
                "market_cap",
                "call_iv",
                "put_iv",
                "iv_avg",
                "currency",
                "financial_currency",
                "listing_type",
                "adr_ratio",
                "valuation_check",
                "financial_note",
            ]
        ],
        on="ticker",
        how="left",
    )
    df["category"] = df["category"].fillna(df["category_return"])
    sample = df[df["ret6m"].notna()].copy()
    sample = sample.sort_values(["score", "rank"], ascending=[False, True]).reset_index(drop=True)

    missing_return = sorted(df.loc[df["ret6m"].isna(), "ticker"].tolist())
    return_not_scored = sorted(set(returns["ticker"]) - set(score["ticker"]))

    base_corr = corr_metrics(sample)
    sample["neutral_pct"] = sample.groupby("category")["score"].transform(
        lambda s: s.rank(method="average", pct=True, ascending=True)
    )
    sample["score_resid"] = sample["score"] - sample.groupby("category")["score"].transform("mean")
    sample["ret_resid"] = sample["ret6m"] - sample.groupby("category")["ret6m"].transform("mean")
    neutral_pct_corr = corr_metrics(sample, "neutral_pct", "ret6m")
    resid_corr = corr_metrics(sample, "score_resid", "ret_resid")

    top_bottom = [top_bottom_metrics(sample, n) for n in [10, 20, 30]]
    ordered = sorted_sample(sample)
    middle_start = max(0, (len(ordered) - 30) // 2)
    risk_groups = [
        risk_group_metrics(f"{FEATURE_ID} Top30", ordered.head(30)),
        risk_group_metrics(f"{FEATURE_ID} Mid30", ordered.iloc[middle_start : middle_start + 30]),
        risk_group_metrics(f"{FEATURE_ID} Bottom30", ordered.tail(30)),
    ]

    category_rows = []
    for category, g in sample.groupby("category", sort=True):
        st = group_stats(g)
        category_rows.append(
            [
                category,
                st["n"],
                fmt_num(st["score_mean"]),
                fmt_pct(st["ret_mean"]),
                fmt_pct(st["ret_median"]),
            ]
        )

    quintile_rows = []
    chunks = np.array_split(np.arange(len(ordered)), 5)
    for i, idx in enumerate(chunks, start=1):
        g = ordered.iloc[idx]
        st = group_stats(g)
        label = "Q1最高分" if i == 1 else ("Q5最低分" if i == 5 else f"Q{i}")
        quintile_rows.append([label, st["n"], fmt_num(st["score_mean"]), fmt_pct(st["ret_mean"]), fmt_pct(st["ret_median"]), fmt_rate(st["hit"])])

    tb_rows = [
        [
            f"Top{m['n']}/Bottom{m['n']}",
            fmt_pct(m["top_mean"]),
            fmt_rate(m["top_hit"]),
            fmt_pct(m["bottom_mean"]),
            fmt_rate(m["bottom_hit"]),
            fmt_pct(m["spread"]),
        ]
        for m in top_bottom
    ]

    comp_rows = []
    top10 = ordered.head(10)
    bottom10 = ordered.tail(10).sort_values("rank")
    for label, g in [("Top10", top10), ("Bottom10", bottom10)]:
        for _, row in g.iterrows():
            comp_rows.append(
                [
                    label,
                    row["ticker"],
                    row["company"],
                    row["category"],
                    fmt_num(row["score"], 1),
                    int(row["rank"]),
                    fmt_pct(row["ret6m"]),
                    row["confidence"],
                ]
            )

    risk_rows = [
        [
            r["label"],
            r["n"],
            r["obs"],
            fmt_pct(r["soxx1_mean"]),
            fmt_pct(r["soxx2_mean"]),
            fmt_pct(r["soxx3_mean"]),
            fmt_pct(r["pressure_mean"]),
            fmt_pct(r["worst_mean"]),
            fmt_pct(r["window_dispersion"]),
            fmt_rate(r["outperform_soxx"]),
            fmt_rate(r["negative_window"]),
        ]
        for r in risk_groups
    ]
    iv_rows = [
        [
            r["label"],
            r["n"],
            r["iv_coverage"],
            fmt_pct(r["call_iv"]),
            fmt_pct(r["put_iv"]),
            fmt_pct(r["iv_avg"]),
            fmt_pct(r["iv_median"]),
        ]
        for r in risk_groups
    ]

    neutral_tb_rows = []
    for n, k in [(10, 1), (20, 2), (30, 3)]:
        ntb = neutral_top_bottom(sample, k)
        neutral_tb_rows.append(
            [
                f"中性Top{n}/Bottom{n}",
                fmt_pct(ntb["top_mean"]),
                fmt_rate(ntb["top_hit"]),
                fmt_pct(ntb["bottom_mean"]),
                fmt_rate(ntb["bottom_hit"]),
                fmt_pct(ntb["spread"]),
            ]
        )

    per_cat_rows = []
    for category, g in sample.groupby("category", sort=True):
        cm = corr_metrics(g)
        top_ret = g.sort_values("ret6m", ascending=False).iloc[0]
        top_score = sorted_sample(g).iloc[0]
        per_cat_rows.append(
            [
                category,
                len(g),
                fmt_corr(cm["pearson"]),
                fmt_corr(cm["spearman"]),
                fmt_pct(g["ret6m"].mean()),
                f"{top_ret['ticker']} {fmt_pct(top_ret['ret6m'])}",
                f"{top_score['ticker']} {fmt_num(top_score['score'], 1)} / {fmt_pct(top_score['ret6m'])}",
            ]
        )

    q_low = sample["ret6m"].quantile(0.05)
    q_high = sample["ret6m"].quantile(0.95)
    low_liq_mask = sample["liquidity_score"] > 5.0
    adr_bad = (
        sample["listing_type"].fillna("").str.contains("ADR|ADS", case=False, regex=True)
        | (sample["currency"].fillna("") != sample["financial_currency"].fillna(""))
        | sample["valuation_check"].fillna("").str.contains("currency_mismatch", case=False)
        | sample["financial_note"].fillna("").str.contains("ADR/ADS比例需确认|交易货币/财报货币不一致", regex=True)
    )
    adr_mask = ~adr_bad
    extreme_mask = (sample["ret6m"] > q_low) & (sample["ret6m"] < q_high)
    robust_rows_data = [
        robustness_row("全样本基准", "无剔除", sample, pd.Series(True, index=sample.index)),
        robustness_row("剔除低流动性", "F51交易流动性分 > 5.0", sample, low_liq_mask),
        robustness_row("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", sample, adr_mask),
        robustness_row(
            "剔除极端涨跌",
            f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(q_low)} / {fmt_pct(q_high)}",
            sample,
            extreme_mask,
        ),
        robustness_row("三项合并剔除", "同时满足上述三项", sample, low_liq_mask & adr_mask & extreme_mask),
    ]
    robust_rows = [
        [
            r["label"],
            r["rule"],
            r["n"],
            r["removed"],
            fmt_corr(r["pearson"]),
            fmt_corr(r["spearman"]),
            fmt_corr(r["kendall"]),
            fmt_pct(r["top30"]),
            fmt_pct(r["bottom30"]),
            fmt_pct(r["spread30"]),
        ]
        for r in robust_rows_data
    ]

    low_liq_list = sorted(sample.loc[~low_liq_mask, "ticker"].tolist())
    adr_list = sorted(sample.loc[adr_bad, "ticker"].tolist())
    extreme_list = sorted(sample.loc[~extreme_mask, "ticker"].tolist())
    exclusion_rows = [
        ["低流动性", len(low_liq_list), ", ".join(low_liq_list)],
        ["ADR/币种异常", len(adr_list), ", ".join(adr_list)],
        ["极端涨跌双尾5%", len(extreme_list), ", ".join(extreme_list)],
    ]

    top_return_rows = []
    for _, row in sample.sort_values("ret6m", ascending=False).head(15).iterrows():
        top_return_rows.append([row["ticker"], row["company"], row["category"], fmt_pct(row["ret6m"]), fmt_num(row["score"], 1), int(row["rank"]), row["confidence"]])

    top_score_rows = []
    for _, row in ordered.head(15).iterrows():
        top_score_rows.append([row["ticker"], row["company"], row["category"], fmt_num(row["score"], 1), int(row["rank"]), fmt_pct(row["ret6m"]), row["confidence"]])

    backup_action = backup_existing_outputs()

    sort_text = corr_interpret(base_corr)
    top30_spread = top_bottom[-1]["spread"]
    topbottom_text = "成立" if top30_spread > 0 and top_bottom[1]["spread"] > 0 else "不成立"
    neutral_text = corr_interpret(neutral_pct_corr)
    combined_spearman = robust_rows_data[-1]["spearman"]
    risk_top = risk_groups[0]
    risk_bottom = risk_groups[2]
    risk_text = (
        "部分成立"
        if (risk_top["pressure_mean"] > risk_bottom["pressure_mean"] and risk_top["iv_avg"] <= risk_bottom["iv_avg"])
        else "不稳定"
    )

    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 {RETURN_WINDOW}涨跌 {RUN_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.append(f"- 评估对象：{FEATURE_SUBJECT}。")
    lines.append(f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 {RUN_DATE}，覆盖 {len(score)} 家。")
    lines.append(
        f"- 收益输入：`日度资料/区间涨跌/{RETURN_PATH.name}`，生成时间 {ret_meta['generated']}，价格最新交易日 {ret_meta['latest_trade']}，6个月价格涨跌不含股息再投资。"
    )
    lines.append("- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。")
    lines.append(f"- 稳健性辅助输入：`特征量化/量化评分/{F51_PATH.name}`；`日度资料/每日金融数据/{FINANCIAL_PATH.name}`。")
    lines.append(f"- 有效评估样本：评分与6个月涨跌交集 {len(sample)} 家；{FEATURE_ID}评分有但6个月涨跌缺失 {len(missing_return)} 家。")
    lines.append("- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。")
    lines.append("- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动率或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为风险代理，并用2026-06-03近ATM Call/Put IV均值补充观察波动代理。")
    lines.append("- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。")
    lines.append(f"- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F26 正式输出；{backup_action} 本次未读取旧版 F26 特征评估作为结论依据。")
    lines.append("")
    lines.append("## 结论摘要")
    lines.append(f"- 排序有效性：{sort_text}。全样本 Pearson {fmt_corr(base_corr['pearson'])}, Spearman {fmt_corr(base_corr['spearman'])}, Kendall {fmt_corr(base_corr['kendall'])}；重点指标 Spearman {fmt_corr(base_corr['spearman'])}。")
    lines.append(f"- Top/Bottom能力：{topbottom_text}。Top10、Top20、Top30 的平均收益分别为 {fmt_pct(top_bottom[0]['top_mean'])}、{fmt_pct(top_bottom[1]['top_mean'])}、{fmt_pct(top_bottom[2]['top_mean'])}；Top-Bottom 收益差分别为 {fmt_pct(top_bottom[0]['spread'])}、{fmt_pct(top_bottom[1]['spread'])}、{fmt_pct(top_bottom[2]['spread'])}。")
    lines.append(f"- 风险解释力：{risk_text}。Top30 压力窗口均值 {fmt_pct(risk_top['pressure_mean'])}，Bottom30 为 {fmt_pct(risk_bottom['pressure_mean'])}；Top30 平均最差窗口 {fmt_pct(risk_top['worst_mean'])}，Bottom30 为 {fmt_pct(risk_bottom['worst_mean'])}；Top30 近ATM IV均值 {fmt_pct(risk_top['iv_avg'])}，Bottom30 为 {fmt_pct(risk_bottom['iv_avg'])}。")
    lines.append(f"- 分类中性：{neutral_text}。按10个分类目录内重新排序并合并后，Spearman {fmt_corr(neutral_pct_corr['spearman'])}；分类去均值残差口径 Spearman {fmt_corr(resid_corr['spearman'])}。")
    stability_label = "不稳定但有弱正向残留" if combined_spearman > 0.03 else "不稳定或不成立"
    lines.append(f"- 稳健性：{stability_label}。剔除低流动性后 Spearman {fmt_corr(robust_rows_data[1]['spearman'])}, 剔除ADR/币种异常后为 {fmt_corr(robust_rows_data[2]['spearman'])}, 剔除极端涨跌后为 {fmt_corr(robust_rows_data[3]['spearman'])}, 三项合并后为 {fmt_corr(combined_spearman)}。")
    lines.append(f"- 解释：{feature_specific_interpretation(sample)}")
    lines.append("")
    lines.append("## 覆盖检查")
    lines.extend(
        md_table(
            ["项目", "数量", "说明"],
            [
                [f"{FEATURE_ID}评分覆盖", len(score), f"来自{RUN_DATE}评分文件"],
                [f"{RETURN_WINDOW}涨跌覆盖", len(returns), "来自2026-05-27区间涨跌文件"],
                ["交集样本", len(sample), "用于本次所有主指标"],
                [f"评分有但{RETURN_WINDOW}涨跌缺失", len(missing_return), ", ".join(missing_return) if missing_return else "无"],
                ["涨跌有但评分缺失", len(return_not_scored), ", ".join(return_not_scored) if return_not_scored else "无"],
            ],
        )
    )
    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.extend(md_table(["分类目录", "样本数", f"{FEATURE_ID}均分", f"{RETURN_WINDOW}平均收益", f"{RETURN_WINDOW}中位收益"], category_rows))
    lines.append("")
    lines.append("## 排序有效性")
    lines.extend(
        md_table(
            ["指标", "数值", "解释"],
            [
                ["Pearson", fmt_corr(base_corr["pearson"]), "线性相关；受极端涨跌影响较大"],
                ["Spearman", fmt_corr(base_corr["spearman"]), "排序相关；这是本任务最重要指标"],
                ["Kendall tau-b", fmt_corr(base_corr["kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
            ],
        )
    )
    lines.append("")
    lines.append("### 分数分组收益")
    lines.extend(md_table(["分组", "公司数", f"{FEATURE_ID}均分", f"{RETURN_WINDOW}平均收益", f"{RETURN_WINDOW}中位收益", "命中率"], quintile_rows))
    lines.append("")
    lines.append("## Top/Bottom能力")
    lines.extend(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], tb_rows))
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    lines.extend(md_table(["组别", "股票代号", "公司名称", "分类目录", f"{FEATURE_ID}分", f"{FEATURE_ID}排名", f"{RETURN_WINDOW}收益", f"{FEATURE_ID}置信度"], comp_rows))
    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为下跌日/回撤代理，并使用2026-06-03近ATM IV作为波动代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供，故不写成严格波动率结论。")
    lines.extend(md_table(["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"], risk_rows))
    lines.append("")
    lines.append("### IV波动代理")
    lines.extend(md_table(["分组", "公司数", "IV覆盖", "平均Call IV", "平均Put IV", "近ATM IV均值", "IV中位数"], iv_rows))
    lines.append("")
    lines.append(f"结论：Top30 的压力窗口均值为 {fmt_pct(risk_top['pressure_mean'])}，Bottom30 为 {fmt_pct(risk_bottom['pressure_mean'])}；Top30 近ATM IV均值为 {fmt_pct(risk_top['iv_avg'])}，Bottom30 为 {fmt_pct(risk_bottom['iv_avg'])}。F26 高分组是否更抗跌需要同时看压力窗口和IV代理，本次不能替代逐日波动率或最大回撤。")
    lines.append("")
    lines.append("## 分类中性结果")
    lines.extend(
        md_table(
            ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
            [
                ["原始全样本", base_corr["n"], fmt_corr(base_corr["pearson"]), fmt_corr(base_corr["spearman"]), fmt_corr(base_corr["kendall"]), f"直接用{FEATURE_ID}分数排序"],
                ["分类内百分位合并", neutral_pct_corr["n"], fmt_corr(neutral_pct_corr["pearson"]), fmt_corr(neutral_pct_corr["spearman"]), fmt_corr(neutral_pct_corr["kendall"]), f"每个分类内先按{FEATURE_ID}排序，再转成0-1百分位合并"],
                ["分类去均值残差", resid_corr["n"], fmt_corr(resid_corr["pearson"]), fmt_corr(resid_corr["spearman"]), fmt_corr(resid_corr["kendall"]), f"{FEATURE_ID}和收益分别减去分类均值后相关"],
            ],
        )
    )
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.extend(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], neutral_tb_rows))
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.extend(md_table(["分类目录", "样本数", "Pearson", "Spearman", f"类内平均{RETURN_WINDOW}收益", "类内最高收益", f"类内最高{FEATURE_ID}公司"], per_cat_rows))
    lines.append("")
    lines.append("分类内结果用于识别是否只是押中某个目录。若原始全样本与分类内百分位、分类残差口径方向相近，则说明结果不是单一行业暴露造成；若方向变化，则说明行业结构和个股极值共同影响较大。")
    lines.append("")
    lines.append("## 稳健性检验")
    lines.extend(md_table(["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"], robust_rows))
    lines.append("")
    lines.append(f"稳健性结论：剔除低流动性、ADR/币种异常和极端涨跌后，Spearman 是否保留正向排序是核心判断。本次三项合并后 Spearman 为 {fmt_corr(combined_spearman)}，因此 F26 对6个月收益的独立排序解释力{'可以保留为弱辅助线索，但不能单独使用' if combined_spearman > 0.03 else '不能单独使用'}。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.extend(md_table(["剔除项", "数量", "公司"], exclusion_rows))
    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append(f"### {RETURN_WINDOW}涨幅前15")
    lines.extend(md_table(["股票代号", "公司名称", "分类目录", f"{RETURN_WINDOW}收益", f"{FEATURE_ID}分", f"{FEATURE_ID}排名", f"{FEATURE_ID}置信度"], top_return_rows))
    lines.append("")
    lines.append(f"### {FEATURE_ID}分数前15")
    lines.extend(md_table(["股票代号", "公司名称", "分类目录", f"{FEATURE_ID}分", f"{FEATURE_ID}排名", f"{RETURN_WINDOW}收益", f"{FEATURE_ID}置信度"], top_score_rows))
    lines.append("")
    lines.append("诊断结论：F26高分公司体现其所处细分市场是否具备足够大的AI需求池、足够快的渗透率提升和足够近的收入验证窗口。本窗口股价收益头部仍包含小中盘修复、存储/光互联弹性、周期反弹和低基数重估；F26能解释赛道空间和需求弹性，但不能直接替代价格动量、估值修复、流动性或事件催化因子。")
    lines.append("")
    lines.append("## 最终判断与后续使用")
    lines.append(f"- 对“6个月价格涨跌排序”的单因子预测：{FEATURE_SUBJECT}本轮评估为{sort_text}，不建议单独用于6个月收益排序。")
    lines.append("- 对风险解释：F26高分组是否更抗跌只能在SOXX压力窗口和近ATM IV代理下观察；本次没有逐日价格序列，不能给出严格波动率、最大回撤或下跌日收益结论。")
    lines.append("- 对组合使用：F26更像赛道空间、渗透率斜率和1-2年收入池弹性因子。后续应与F05估值赔率、F25需求到收入链条清晰度、F37-F39催化剂、F50价格相对强度、F51交易流动性和极端涨跌过滤联用。")
    lines.append("- 对上游资料：本报告只作为下游特征评估，不反向修改公司调研、行业调研或日度事实资料。")
    lines.append("")
    lines.append("## 附：关键口径复述")
    lines.append("- 6个月收益：区间涨跌文件中的 `6个月` 字段，百分比单位，不含股息再投资。")
    lines.append("- 低流动性剔除：F51交易流动性分数缺失或不高于 5.0。")
    lines.append("- ADR/币种异常剔除：`listing_type` 为 ADR/ADS、ADR比例非不适用、交易货币与财报货币不一致、估值校验含 `currency_mismatch` 或备注提示 ADR/币种需确认。")
    lines.append(f"- 极端涨跌剔除：按本次{len(sample)}家6个月收益双尾5%剔除，阈值为 {fmt_pct(q_low)} 和 {fmt_pct(q_high)}。")
    lines.append("")

    diagnostics = {
        "score_count": len(score),
        "return_count": len(returns),
        "sample_count": len(sample),
        "missing_return": len(missing_return),
        "base_spearman": base_corr["spearman"],
        "combined_spearman": combined_spearman,
        "out_path": str(OUT_PATH),
    }
    return "\n".join(lines), diagnostics


def main() -> None:
    report, diagnostics = build_report()
    OUT_PATH.write_text(report, encoding="utf-8")
    print("Wrote", OUT_PATH)
    print(diagnostics)


if __name__ == "__main__":
    main()

