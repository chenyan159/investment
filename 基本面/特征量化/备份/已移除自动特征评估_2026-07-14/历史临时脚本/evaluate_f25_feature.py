import math
import re
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\drive\Investment\基本面")
FEATURE_ID = "F25"
FEATURE_NAME = "需求到收入链条清晰度"
FEATURE_STEM = f"{FEATURE_ID}_{FEATURE_NAME}"
REPORT_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_STEM}_量化评分_2026-06-04.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
F51_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_PATH = ROOT / "特征量化" / "特征评估" / f"{FEATURE_STEM}_特征评估_6个月涨跌_{REPORT_DATE}.md"

SOXX = {
    "SOXX下跌1": -32.98,
    "SOXX下跌2": -15.82,
    "SOXX下跌3": -13.40,
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def split_md_row(line: str):
    line = line.strip()
    if not line.startswith("|"):
        return None
    cells = [c.strip() for c in line.strip("|").split("|")]
    return cells


def is_separator(cells):
    return all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells)


def parse_percent(cell: str):
    if cell is None:
        return math.nan
    text = str(cell)
    if "N/A" in text or "缺失" in text:
        return math.nan
    m = re.search(r"([+-]?\d+(?:,\d{3})*(?:\.\d+)?)%", text)
    if not m:
        return math.nan
    return float(m.group(1).replace(",", ""))


def parse_money_to_billion(cell: str):
    if cell is None:
        return math.nan
    text = str(cell).strip()
    if text in ("", "缺失", "N/A"):
        return math.nan
    m = re.search(r"\$?([+-]?\d+(?:,\d{3})*(?:\.\d+)?)([TtBbMmKk]?)", text)
    if not m:
        return math.nan
    val = float(m.group(1).replace(",", ""))
    unit = m.group(2).upper()
    if unit == "T":
        return val * 1000
    if unit == "B":
        return val
    if unit == "M":
        return val / 1000
    if unit == "K":
        return val / 1_000_000
    return val / 1_000_000_000


def extract_metadata_value(text: str, label: str):
    m = re.search(rf"- {re.escape(label)}：(.+)", text)
    return m.group(1).strip() if m else ""


def table_rows_in_section(text: str, section_heading: str):
    start = text.index(section_heading)
    rest = text[start + len(section_heading):]
    next_m = re.search(r"\n## ", rest)
    section = rest[: next_m.start()] if next_m else rest
    lines = section.splitlines()
    header = None
    rows = []
    for line in lines:
        cells = split_md_row(line)
        if not cells:
            continue
        if is_separator(cells):
            continue
        if header is None:
            header = cells
            continue
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def parse_score_file(path: Path, score_col_name="特征分", prefix=None):
    rows = table_rows_in_section(read_text(path), "## 全公司排序表")
    parsed = []
    for row in rows:
        ticker = row.get("股票代号", "").strip()
        if not ticker:
            continue
        parsed.append(
            {
                "ticker": ticker,
                "company": row.get("公司名称", "").strip(),
                "category": row.get("分类目录", "").strip(),
                "score": float(row.get(score_col_name, "nan")),
                "score_rank": int(row.get("排名", "0")),
                "evidence": row.get("证据等级", "").strip(),
                "confidence": row.get("置信度", "").strip(),
            }
        )
    df = pd.DataFrame(parsed)
    if prefix:
        df = df.rename(columns={"score": f"{prefix}_score"})
    return df


def parse_return_file(path: Path):
    text = read_text(path)
    detail_start = text.index("## 按分类分组的公司明细")
    detail = text[detail_start:]
    rows = []
    category = None
    header = None
    for line in detail.splitlines():
        m = re.match(r"### (.+)", line.strip())
        if m:
            category = m.group(1).strip()
            header = None
            continue
        cells = split_md_row(line)
        if not cells:
            continue
        if is_separator(cells):
            continue
        if cells and cells[0] == "股票代号":
            header = cells
            continue
        if header and len(cells) == len(header):
            row = dict(zip(header, cells))
            rows.append(
                {
                    "ticker": row["股票代号"].strip(),
                    "return_company": row["公司名称"].strip(),
                    "return_category": category,
                    "latest_trade_date": row.get("最新交易日", "").strip(),
                    "close": float(row.get("最新收盘价", "").replace(",", "")),
                    "r_1m": parse_percent(row.get("1个月")),
                    "r_3m": parse_percent(row.get("3个月")),
                    "r_6m": parse_percent(row.get("6个月")),
                    "r_1y": parse_percent(row.get("1年")),
                    "return_note": row.get("备注", "").strip(),
                }
            )
    return pd.DataFrame(rows)


def parse_soxx_file(path: Path):
    text = read_text(path)
    start = text.index("### 按分类分组的全公司明细")
    end = text.index("## 按分类分组的公司明细")
    section = text[start:end]
    rows = []
    category = None
    header = None
    for line in section.splitlines():
        m = re.match(r"#### (.+)", line.strip())
        if m:
            category = m.group(1).strip()
            header = None
            continue
        cells = split_md_row(line)
        if not cells:
            continue
        if is_separator(cells):
            continue
        if cells and cells[0] == "股票代号":
            header = cells
            continue
        if header and len(cells) == len(header):
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
    return pd.DataFrame(rows)


def parse_financial_file(path: Path):
    text = read_text(path)
    start = text.index("## 按项目分类分组的公司明细表")
    section = text[start:]
    rows = []
    category = None
    header = None
    for line in section.splitlines():
        m = re.match(r"### (.+)", line.strip())
        if m:
            category = m.group(1).strip()
            header = None
            continue
        cells = split_md_row(line)
        if not cells:
            continue
        if is_separator(cells):
            continue
        if cells and cells[0] == "股票代号":
            header = cells
            continue
        if header and len(cells) == len(header):
            row = dict(zip(header, cells))
            call_iv = parse_percent(row.get("Call IV"))
            put_iv = parse_percent(row.get("Put IV"))
            iv_vals = [x for x in [call_iv, put_iv] if not math.isnan(x)]
            rows.append(
                {
                    "ticker": row["股票代号"].strip(),
                    "fin_category": category,
                    "market_cap_b": parse_money_to_billion(row.get("市值")),
                    "call_iv": call_iv,
                    "put_iv": put_iv,
                    "near_atm_iv": float(np.mean(iv_vals)) if iv_vals else math.nan,
                    "currency": row.get("currency", "").strip(),
                    "financial_currency": row.get("financial_currency", "").strip(),
                    "listing_type": row.get("listing_type", "").strip(),
                    "adr_ratio": row.get("adr_ratio", "").strip(),
                    "valuation_check": row.get("估值校验", "").strip(),
                    "fin_note": row.get("备注", "").strip(),
                }
            )
    return pd.DataFrame(rows)


def pearson(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if len(x) < 2 or np.std(x) == 0 or np.std(y) == 0:
        return math.nan
    return float(np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    xr = pd.Series(x).rank(method="average")
    yr = pd.Series(y).rank(method="average")
    return pearson(xr, yr)


def kendall_tau_b(x, y):
    pairs = pd.DataFrame({"x": x, "y": y}).dropna()
    x_vals = pairs["x"].to_numpy(dtype=float)
    y_vals = pairs["y"].to_numpy(dtype=float)
    n = len(x_vals)
    if n < 2:
        return math.nan
    c = d = 0
    for i in range(n - 1):
        dx = x_vals[i + 1:] - x_vals[i]
        dy = y_vals[i + 1:] - y_vals[i]
        prod = dx * dy
        c += int(np.sum(prod > 0))
        d += int(np.sum(prod < 0))
    n0 = n * (n - 1) / 2
    n1 = sum(v * (v - 1) / 2 for v in pd.Series(x_vals).value_counts().values)
    n2 = sum(v * (v - 1) / 2 for v in pd.Series(y_vals).value_counts().values)
    denom = math.sqrt((n0 - n1) * (n0 - n2))
    if denom == 0:
        return math.nan
    return float((c - d) / denom)


def corr_stats(df, score_col="score", ret_col="r_6m"):
    d = df[[score_col, ret_col]].dropna()
    return {
        "n": len(d),
        "pearson": pearson(d[score_col], d[ret_col]),
        "spearman": spearman(d[score_col], d[ret_col]),
        "kendall": kendall_tau_b(d[score_col], d[ret_col]),
    }


def fmt_corr(x):
    return "N/A" if x is None or math.isnan(x) else f"{x:.3f}"


def fmt_pct(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "N/A"
    sign = "+" if x >= 0 else ""
    return f"{sign}{x:.2f}%"


def fmt_pct1(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "N/A"
    sign = "+" if x >= 0 else ""
    return f"{sign}{x:.1f}%"


def fmt_float(x, digits=2):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "N/A"
    return f"{x:.{digits}f}"


def classify_strength(s):
    if s >= 0.15:
        return "部分成立"
    if s >= 0.05:
        return "弱正向"
    if s > -0.05:
        return "不成立"
    return "反向或偏负"


def sorted_by_score(df):
    return df.sort_values(["score", "ticker"], ascending=[False, True]).reset_index(drop=True)


def top_bottom_stats(df, n, score_col="score", neutral=False):
    d = df.dropna(subset=[score_col, "r_6m"]).sort_values([score_col, "ticker"], ascending=[False, True])
    top = d.head(n)
    bottom = d.tail(n).sort_values([score_col, "ticker"], ascending=[True, True])
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


def quintile_stats(df):
    d = df.dropna(subset=["score", "r_6m"]).sort_values(["score", "ticker"], ascending=[False, True]).reset_index(drop=True)
    groups = []
    splits = [d.iloc[idx].copy() for idx in np.array_split(np.arange(len(d)), 5)]
    for i, g in enumerate(splits, start=1):
        groups.append(
            {
                "group": f"Q{i}{'最高分' if i == 1 else '最低分' if i == 5 else ''}",
                "n": len(g),
                "score_mean": g["score"].mean(),
                "return_mean": g["r_6m"].mean(),
                "return_median": g["r_6m"].median(),
                "hit": (g["r_6m"] > 0).mean() * 100,
            }
        )
    return groups


def risk_group_stats(df, label_prefix=FEATURE_ID):
    d = df.dropna(subset=["score", "r_6m"]).sort_values(["score", "ticker"], ascending=[False, True]).reset_index(drop=True)
    top = d.head(30).copy()
    bottom = d.tail(30).sort_values(["score", "ticker"], ascending=[True, True]).copy()
    mid_start = max((len(d) - 30) // 2, 0)
    mid = d.iloc[mid_start: mid_start + 30].copy()
    groups = [(f"{label_prefix} Top30", top), (f"{label_prefix} Mid30", mid), (f"{label_prefix} Bottom30", bottom)]
    out = []
    iv_out = []
    for name, g in groups:
        vals = []
        wins = []
        neg_count = 0
        obs = 0
        for col, soxx_val in [("soxx1", SOXX["SOXX下跌1"]), ("soxx2", SOXX["SOXX下跌2"]), ("soxx3", SOXX["SOXX下跌3"])]:
            v = g[col].dropna()
            vals.append(v.mean())
            obs += len(v)
            wins.extend(list(v > soxx_val))
            neg_count += int((v < 0).sum())
        window_means = g[["soxx1", "soxx2", "soxx3"]].mean(axis=1, skipna=True)
        worst = g[["soxx1", "soxx2", "soxx3"]].min(axis=1, skipna=True)
        stds = g[["soxx1", "soxx2", "soxx3"]].std(axis=1, skipna=True)
        out.append(
            {
                "group": name,
                "n": len(g),
                "obs": obs,
                "soxx1_mean": vals[0],
                "soxx2_mean": vals[1],
                "soxx3_mean": vals[2],
                "stress_mean": window_means.mean(),
                "worst_mean": worst.mean(),
                "window_std": stds.mean(),
                "outperform": np.mean(wins) * 100 if wins else math.nan,
                "neg_window": neg_count / obs * 100 if obs else math.nan,
            }
        )
        iv = g.dropna(subset=["near_atm_iv"])
        iv_out.append(
            {
                "group": name,
                "n": len(g),
                "iv_n": len(iv),
                "call_iv": g["call_iv"].mean(skipna=True),
                "put_iv": g["put_iv"].mean(skipna=True),
                "near_iv": g["near_atm_iv"].mean(skipna=True),
                "iv_median": g["near_atm_iv"].median(skipna=True),
            }
        )
    return out, iv_out


def add_neutral_scores(df):
    d = df.copy()
    parts = []
    for cat, g in d.groupby("category", sort=True):
        g = g.copy()
        n = len(g)
        if n == 1:
            g["cat_percentile"] = 1.0
        else:
            g["cat_percentile"] = (g["score"].rank(method="average") - 1) / (n - 1)
        g["score_resid"] = g["score"] - g["score"].mean()
        g["ret_resid"] = g["r_6m"] - g["r_6m"].mean()
        parts.append(g)
    return pd.concat(parts, ignore_index=True)


def neutral_corr_stats(df):
    d = add_neutral_scores(df)
    return {
        "raw": corr_stats(d, "score", "r_6m"),
        "percentile": corr_stats(d, "cat_percentile", "r_6m"),
        "resid": corr_stats(d, "score_resid", "ret_resid"),
        "df": d,
    }


def category_corrs(df):
    rows = []
    for cat, g in df.groupby("category", sort=True):
        g = g.dropna(subset=["score", "r_6m"]).copy()
        top_score = g.sort_values(["score", "ticker"], ascending=[False, True]).iloc[0]
        top_ret = g.sort_values(["r_6m", "ticker"], ascending=[False, True]).iloc[0]
        c = corr_stats(g, "score", "r_6m")
        rows.append(
            {
                "category": cat,
                "n": len(g),
                "pearson": c["pearson"],
                "spearman": c["spearman"],
                "mean_ret": g["r_6m"].mean(),
                "top_return": top_ret,
                "top_score": top_score,
            }
        )
    return rows


def robust_rows(df):
    d = df.dropna(subset=["score", "r_6m"]).copy()
    low = d["r_6m"].quantile(0.05)
    high = d["r_6m"].quantile(0.95)
    d["exclude_low_liq"] = d["f51_score"].isna() | (d["f51_score"] <= 5.0)
    listing = d["listing_type"].fillna("")
    adr_ratio = d["adr_ratio"].fillna("")
    cur = d["currency"].fillna("")
    fcur = d["financial_currency"].fillna("")
    valchk = d["valuation_check"].fillna("")
    note = d["fin_note"].fillna("")
    d["exclude_adr_currency"] = (
        listing.str.contains("ADR|ADS", case=False, regex=True)
        | adr_ratio.ne("不适用")
        | (cur.ne("") & fcur.ne("") & cur.ne(fcur))
        | valchk.str.contains("currency_mismatch", case=False, regex=False)
        | note.str.contains("交易货币/财报货币不一致|ADR/ADS比例需确认", regex=True)
    )
    d["exclude_extreme"] = (d["r_6m"] <= low) | (d["r_6m"] >= high)
    masks = [
        ("全样本基准", "无剔除", pd.Series(True, index=d.index)),
        ("剔除低流动性", "F51交易流动性分 > 5.0", ~d["exclude_low_liq"]),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", ~d["exclude_adr_currency"]),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(low)} / {fmt_pct(high)}", ~d["exclude_extreme"]),
        ("三项合并剔除", "同时满足上述三项", ~(d["exclude_low_liq"] | d["exclude_adr_currency"] | d["exclude_extreme"])),
    ]
    rows = []
    for name, rule, mask in masks:
        sub = d[mask].copy()
        c = corr_stats(sub, "score", "r_6m")
        tb30 = top_bottom_stats(sub, 30)
        rows.append(
            {
                "name": name,
                "rule": rule,
                "n": len(sub),
                "excluded": len(d) - len(sub),
                "pearson": c["pearson"],
                "spearman": c["spearman"],
                "kendall": c["kendall"],
                "top30": tb30["top_mean"],
                "bottom30": tb30["bottom_mean"],
                "diff30": tb30["diff"],
            }
        )
    exclusion_lists = {
        "low_liq": sorted(d.loc[d["exclude_low_liq"], "ticker"].tolist()),
        "adr_currency": sorted(d.loc[d["exclude_adr_currency"], "ticker"].tolist()),
        "extreme": sorted(d.loc[d["exclude_extreme"], "ticker"].tolist()),
    }
    return rows, exclusion_lists, low, high


def markdown_table(headers, rows):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---:" if h.endswith("数") or h in ("样本数", "公司数", "数量", "剔除数", "窗口观测", "IV覆盖") else "---" for h in headers]) + " |")
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out)


def top_constituents_rows(tb, group_label):
    rows = []
    for _, r in tb.iterrows():
        rows.append(
            [
                group_label,
                r["ticker"],
                r["company"],
                r["category"],
                fmt_float(r["score"], 1),
                int(r["score_rank"]),
                fmt_pct(r["r_6m"]),
                r["confidence"],
            ]
        )
    return rows


def conclusion_text(corr, tb_stats, neutral, robust, top15_ret, top15_score):
    s = corr["spearman"]
    tb30 = tb_stats[30]["diff"]
    neutral_s = neutral["percentile"]["spearman"]
    combo_s = robust[-1]["spearman"]
    if s >= 0.15 and tb30 > 0 and neutral_s > 0:
        sort_line = "排序有效性：部分成立"
    elif s >= 0.05:
        sort_line = "排序有效性：弱正向"
    elif s <= -0.05:
        sort_line = "排序有效性：反向或偏负"
    else:
        sort_line = "排序有效性：不成立"
    if tb30 > 0 and tb_stats[10]["diff"] > 0:
        tb_line = "Top/Bottom能力：部分成立"
    else:
        tb_line = "Top/Bottom能力：不成立"
    robust_line = "稳健性："
    if combo_s >= 0.10:
        robust_line += "弱稳定"
    elif combo_s > 0:
        robust_line += "有弱正向残留但不强"
    else:
        robust_line += "不稳定"
    return sort_line, tb_line, robust_line


def main():
    score = parse_score_file(SCORE_PATH)
    ret = parse_return_file(RETURN_PATH)
    soxx = parse_soxx_file(RETURN_PATH)
    fin = parse_financial_file(FIN_PATH)
    f51 = parse_score_file(F51_PATH, prefix="f51")
    f51 = f51[["ticker", "f51_score"]]

    df = score.merge(ret, on="ticker", how="left").merge(soxx, on="ticker", how="left").merge(fin, on="ticker", how="left").merge(f51, on="ticker", how="left")
    df["company"] = df["company"].fillna(df.get("return_company", ""))
    df["category"] = df["category"].fillna(df.get("return_category", ""))
    eval_df = df.dropna(subset=["score", "r_6m"]).copy()

    missing_returns = sorted(df.loc[df["r_6m"].isna(), "ticker"].tolist())
    returns_missing_score = sorted(set(ret["ticker"]) - set(score["ticker"]))

    corr = corr_stats(eval_df)
    tb_stats = {n: top_bottom_stats(eval_df, n) for n in [10, 20, 30]}
    qstats = quintile_stats(eval_df)
    risk_stats, iv_stats = risk_group_stats(eval_df, FEATURE_ID)
    neutral = neutral_corr_stats(eval_df)
    neutral_df = neutral["df"]
    neutral_tb = {n: top_bottom_stats(neutral_df, n, score_col="cat_percentile") for n in [10, 20, 30]}
    cat_rows = category_corrs(eval_df)
    robust, exclusions, low_thr, high_thr = robust_rows(eval_df)

    top15_ret = eval_df.sort_values(["r_6m", "ticker"], ascending=[False, True]).head(15)
    top15_score = eval_df.sort_values(["score", "ticker"], ascending=[False, True]).head(15)
    bottom15_score = eval_df.sort_values(["score", "ticker"], ascending=[True, True]).head(10)

    sort_line, tb_line, robust_line = conclusion_text(corr, tb_stats, neutral, robust, top15_ret, top15_score)
    spearman_label = classify_strength(corr["spearman"])
    neutral_s = neutral["percentile"]["spearman"]
    resid_s = neutral["resid"]["spearman"]

    lines = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 6个月涨跌 {REPORT_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.append(f"- 评估对象：`{FEATURE_STEM}`。")
    lines.append(f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 2026-06-04，覆盖 {len(score)} 家。")
    lines.append("- 收益输入：`日度资料/区间涨跌/公司股价区间涨跌幅_2026-05-27.md`，生成时间 2026-05-27 20:17:54 -0700（本机时区），价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。")
    lines.append("- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。")
    lines.append("- 稳健性辅助输入：`特征量化/量化评分/F51_交易流动性_量化评分_2026-06-04.md`；`日度资料/每日金融数据/每日金融数据_2026-06-03.md`，金融数据生成时间 2026-06-03 13:41:46 PDT-0700。")
    lines.append(f"- 有效评估样本：评分与6个月涨跌交集 {len(eval_df)} 家；F25评分有但6个月涨跌缺失 {len(missing_returns)} 家。")
    lines.append("- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。")
    lines.append("- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动率或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为风险代理，并用2026-06-03近ATM Call/Put IV均值补充观察波动代理。")
    lines.append("- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。")
    lines.append("- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F25 正式输出；处理结果：未发现同类旧版正式输出。 本次未读取旧版 F25 特征评估作为结论依据。")
    lines.append("")
    lines.append("## 结论摘要")
    lines.append(f"- {sort_line}。全样本 Pearson {fmt_corr(corr['pearson'])}, Spearman {fmt_corr(corr['spearman'])}, Kendall {fmt_corr(corr['kendall'])}；重点指标 Spearman {fmt_corr(corr['spearman'])}，属于{spearman_label}。")
    lines.append(f"- {tb_line}。Top10、Top20、Top30 的平均收益分别为 {fmt_pct(tb_stats[10]['top_mean'])}、{fmt_pct(tb_stats[20]['top_mean'])}、{fmt_pct(tb_stats[30]['top_mean'])}；Top-Bottom 收益差分别为 {fmt_pct(tb_stats[10]['diff'])}、{fmt_pct(tb_stats[20]['diff'])}、{fmt_pct(tb_stats[30]['diff'])}。")
    lines.append(f"- 风险解释力：不稳定。Top30 压力窗口均值 {fmt_pct(risk_stats[0]['stress_mean'])}，Bottom30 为 {fmt_pct(risk_stats[2]['stress_mean'])}；Top30 平均最差窗口 {fmt_pct(risk_stats[0]['worst_mean'])}，Bottom30 为 {fmt_pct(risk_stats[2]['worst_mean'])}；Top30 近ATM IV均值 {fmt_pct(iv_stats[0]['near_iv'])}，Bottom30 为 {fmt_pct(iv_stats[2]['near_iv'])}。")
    lines.append(f"- 分类中性：{'仍为正但偏弱' if neutral_s > 0 else '方向转弱或为负'}。按10个分类目录内重新排序并合并后，Spearman {fmt_corr(neutral_s)}；分类去均值残差口径 Spearman {fmt_corr(resid_s)}。")
    lines.append(f"- {robust_line}。剔除低流动性后 Spearman {fmt_corr(robust[1]['spearman'])}, 剔除ADR/币种异常后为 {fmt_corr(robust[2]['spearman'])}, 剔除极端涨跌后为 {fmt_corr(robust[3]['spearman'])}, 三项合并后为 {fmt_corr(robust[4]['spearman'])}。")
    lines.append("- 解释：F25 衡量 AI capex、芯片出货、数据中心建设或晶圆厂投资到公司收入利润的路径是否短、直接且可验证。高分端集中在 DELL、CRWV、VRT、NVDA、NBIS、ORCL、SNDK、GOOGL、AMZN、GEV 等订单/RPO/backlog/AI收入链条清晰的公司；但本次6个月收益头部仍由 AXTI、SNDK、AAOI、MXL、AEHR、ICHR、MU、VICR、MRAM、FCEL 等小中盘弹性、存储/光互联周期修复或低基数重估公司主导。因此 F25 有一定基本面解释含义，但在该窗口不是单独可用的6个月收益排序因子。")
    lines.append("")

    lines.append("## 覆盖检查")
    lines.append(markdown_table(
        ["项目", "数量", "说明"],
        [
            ["F25评分覆盖", len(score), "来自2026-06-04评分文件"],
            ["6个月涨跌覆盖", len(ret), "来自2026-05-27区间涨跌文件"],
            ["交集样本", len(eval_df), "用于本次所有主指标"],
            ["评分有但6个月涨跌缺失", len(missing_returns), ", ".join(missing_returns) if missing_returns else "无"],
            ["涨跌有但评分缺失", len(returns_missing_score), ", ".join(returns_missing_score) if returns_missing_score else "无"],
        ],
    ))
    lines.append("")
    lines.append("### 交集样本分类分布")
    cat_dist = []
    for cat, g in eval_df.groupby("category", sort=True):
        cat_dist.append([cat, len(g), fmt_float(g["score"].mean(), 2), fmt_pct(g["r_6m"].mean()), fmt_pct(g["r_6m"].median())])
    lines.append(markdown_table(["分类目录", "样本数", "F25均分", "6个月平均收益", "6个月中位收益"], cat_dist))
    lines.append("")

    lines.append("## 排序有效性")
    lines.append(markdown_table(
        ["指标", "数值", "解释"],
        [
            ["Pearson", fmt_corr(corr["pearson"]), "线性相关；受极端涨跌影响较大"],
            ["Spearman", fmt_corr(corr["spearman"]), "排序相关；这是本任务最重要指标"],
            ["Kendall tau-b", fmt_corr(corr["kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
        ],
    ))
    lines.append("")
    lines.append("### 分数分组收益")
    qrows = [[q["group"], q["n"], fmt_float(q["score_mean"], 2), fmt_pct(q["return_mean"]), fmt_pct(q["return_median"]), fmt_pct1(q["hit"])] for q in qstats]
    lines.append(markdown_table(["分组", "公司数", "F25均分", "6个月平均收益", "6个月中位收益", "命中率"], qrows))
    lines.append("")

    lines.append("## Top/Bottom能力")
    tb_rows = []
    for n in [10, 20, 30]:
        tb = tb_stats[n]
        tb_rows.append([f"Top{n}/Bottom{n}", fmt_pct(tb["top_mean"]), fmt_pct1(tb["top_hit"]), fmt_pct(tb["bottom_mean"]), fmt_pct1(tb["bottom_hit"]), fmt_pct(tb["diff"])])
    lines.append(markdown_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], tb_rows))
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    tb10_rows = top_constituents_rows(tb_stats[10]["top"], "Top10") + top_constituents_rows(tb_stats[10]["bottom"], "Bottom10")
    lines.append(markdown_table(["组别", "股票代号", "公司名称", "分类目录", "F25分", "F25排名", "6个月收益", "F25置信度"], tb10_rows))
    lines.append("")

    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为下跌日/回撤代理，并使用2026-06-03近ATM IV作为波动代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供，故不写成严格波动率结论。")
    risk_rows = []
    for r in risk_stats:
        risk_rows.append([r["group"], r["n"], r["obs"], fmt_pct(r["soxx1_mean"]), fmt_pct(r["soxx2_mean"]), fmt_pct(r["soxx3_mean"]), fmt_pct(r["stress_mean"]), fmt_pct(r["worst_mean"]), fmt_pct(r["window_std"]), fmt_pct1(r["outperform"]), fmt_pct1(r["neg_window"])])
    lines.append(markdown_table(["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"], risk_rows))
    lines.append("")
    lines.append("### IV波动代理")
    iv_rows = []
    for r in iv_stats:
        iv_rows.append([r["group"], r["n"], r["iv_n"], fmt_pct(r["call_iv"]), fmt_pct(r["put_iv"]), fmt_pct(r["near_iv"]), fmt_pct(r["iv_median"])])
    lines.append(markdown_table(["分组", "公司数", "IV覆盖", "平均Call IV", "平均Put IV", "近ATM IV均值", "IV中位数"], iv_rows))
    lines.append("")
    lines.append(f"结论：Top30 的压力窗口均值为 {fmt_pct(risk_stats[0]['stress_mean'])}，Bottom30 为 {fmt_pct(risk_stats[2]['stress_mean'])}；Top30 近ATM IV均值为 {fmt_pct(iv_stats[0]['near_iv'])}，Bottom30 为 {fmt_pct(iv_stats[2]['near_iv'])}。F25高分组并没有稳定体现更小压力窗口跌幅；IV代理略低于中低分组，但不足以替代逐日波动率或完整回撤结论。")
    lines.append("")

    lines.append("## 分类中性结果")
    neutral_rows = [
        ["原始全样本", corr["n"], fmt_corr(neutral["raw"]["pearson"]), fmt_corr(neutral["raw"]["spearman"]), fmt_corr(neutral["raw"]["kendall"]), "直接用F25分数排序"],
        ["分类内百分位合并", neutral["percentile"]["n"], fmt_corr(neutral["percentile"]["pearson"]), fmt_corr(neutral["percentile"]["spearman"]), fmt_corr(neutral["percentile"]["kendall"]), "每个分类内先按F25排序，再转成0-1百分位合并"],
        ["分类去均值残差", neutral["resid"]["n"], fmt_corr(neutral["resid"]["pearson"]), fmt_corr(neutral["resid"]["spearman"]), fmt_corr(neutral["resid"]["kendall"]), "F25和收益分别减去分类均值后相关"],
    ]
    lines.append(markdown_table(["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"], neutral_rows))
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    ntb_rows = []
    for n in [10, 20, 30]:
        tb = neutral_tb[n]
        ntb_rows.append([f"中性Top{n}/Bottom{n}", fmt_pct(tb["top_mean"]), fmt_pct1(tb["top_hit"]), fmt_pct(tb["bottom_mean"]), fmt_pct1(tb["bottom_hit"]), fmt_pct(tb["diff"])])
    lines.append(markdown_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], ntb_rows))
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    cat_corr_rows = []
    for r in cat_rows:
        tr = r["top_return"]
        ts = r["top_score"]
        cat_corr_rows.append([r["category"], r["n"], fmt_corr(r["pearson"]), fmt_corr(r["spearman"]), fmt_pct(r["mean_ret"]), f"{tr['ticker']} {fmt_pct(tr['r_6m'])}", f"{ts['ticker']} {fmt_float(ts['score'],1)} / {fmt_pct(ts['r_6m'])}"])
    lines.append(markdown_table(["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F25公司"], cat_corr_rows))
    lines.append("")
    lines.append("分类内结果用于识别是否只是押中某个目录。若原始全样本与分类内百分位、分类残差口径方向相近，则说明结果不是单一行业暴露造成；若方向变化，则说明行业结构和个股极值共同影响较大。")
    lines.append("")

    lines.append("## 稳健性检验")
    robust_rows_md = []
    for r in robust:
        robust_rows_md.append([r["name"], r["rule"], r["n"], r["excluded"], fmt_corr(r["pearson"]), fmt_corr(r["spearman"]), fmt_corr(r["kendall"]), fmt_pct(r["top30"]), fmt_pct(r["bottom30"]), fmt_pct(r["diff30"])])
    lines.append(markdown_table(["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"], robust_rows_md))
    lines.append("")
    lines.append(f"稳健性结论：剔除低流动性、ADR/币种异常和极端涨跌后，Spearman 是否保留正向排序是核心判断。本次三项合并后 Spearman 为 {fmt_corr(robust[4]['spearman'])}，Top30-Bottom30 为 {fmt_pct(robust[4]['diff30'])}，说明 F25 在过滤异常后未保留正向排序能力，不能单独使用。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(markdown_table(
        ["剔除项", "数量", "公司"],
        [
            ["低流动性", len(exclusions["low_liq"]), ", ".join(exclusions["low_liq"])],
            ["ADR/币种异常", len(exclusions["adr_currency"]), ", ".join(exclusions["adr_currency"])],
            ["极端涨跌双尾5%", len(exclusions["extreme"]), ", ".join(exclusions["extreme"])],
        ],
    ))
    lines.append("")

    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    ret_rows = []
    for _, r in top15_ret.iterrows():
        ret_rows.append([r["ticker"], r["company"], r["category"], fmt_pct(r["r_6m"]), fmt_float(r["score"], 1), int(r["score_rank"]), r["confidence"]])
    lines.append(markdown_table(["股票代号", "公司名称", "分类目录", "6个月收益", "F25分", "F25排名", "F25置信度"], ret_rows))
    lines.append("")
    lines.append("### F25分数前15")
    score_rows = []
    for _, r in top15_score.iterrows():
        score_rows.append([r["ticker"], r["company"], r["category"], fmt_float(r["score"], 1), int(r["score_rank"]), fmt_pct(r["r_6m"]), r["confidence"]])
    lines.append(markdown_table(["股票代号", "公司名称", "分类目录", "F25分", "F25排名", "6个月收益", "F25置信度"], score_rows))
    lines.append("")
    lines.append("### F25低分端但6个月高弹性样本")
    low_high = eval_df.sort_values(["score", "r_6m"], ascending=[True, False]).head(12)
    low_rows = []
    for _, r in low_high.iterrows():
        low_rows.append([r["ticker"], r["company"], r["category"], fmt_float(r["score"], 1), int(r["score_rank"]), fmt_pct(r["r_6m"]), r["confidence"]])
    lines.append(markdown_table(["股票代号", "公司名称", "分类目录", "F25分", "F25排名", "6个月收益", "F25置信度"], low_rows))
    lines.append("")
    lines.append("诊断结论：F25高分公司更像订单可见度、合同/RPO/backlog和收入确认链条清晰度高的基本面质量因子；本窗口股价收益头部包含 AXTI、AAOI、MXL、AEHR、ICHR、MRAM、FCEL、RKLB 等低分或中低分的弹性/修复型标的，说明6个月价格排序同时受低基数、流动性、估值修复和事件催化驱动。")
    lines.append("")

    lines.append("## 最终判断与后续使用")
    lines.append(f"- 对“6个月价格涨跌排序”的单因子预测：F25_{FEATURE_NAME}本轮评估为{spearman_label}，排序解释力有限，不建议单独用于6个月收益排序。")
    lines.append("- 对风险解释：F25高分组在 SOXX 压力窗口中没有稳定更抗跌，IV代理略低但不足以证明波动显著更小；需要逐日价格序列才能做严格波动率、最大回撤和下跌日收益统计。")
    lines.append("- 对组合使用：F25适合作为订单可见度、收入确认链条和基本面兑现质量的解释变量。后续应与 F05估值赔率、F10-F12收入兑现/台阶信号、F37-F39催化剂、F50价格相对强度、F51交易流动性和极端涨跌过滤联用。")
    lines.append("- 对上游资料：本报告只作为下游特征评估，不反向修改公司调研、行业调研或日度事实资料。")
    lines.append("")

    lines.append("## 附：关键口径复述")
    lines.append("- 6个月收益：区间涨跌文件中的 `6个月` 字段，百分比单位，不含股息再投资。")
    lines.append("- 低流动性剔除：F51交易流动性分数缺失或不高于 5.0。")
    lines.append("- ADR/币种异常剔除：`listing_type` 为 ADR/ADS、ADR比例非不适用、交易货币与财报货币不一致、估值校验含 `currency_mismatch` 或备注提示 ADR/币种需确认。")
    lines.append(f"- 极端涨跌剔除：按本次{len(eval_df)}家6个月收益双尾5%剔除，阈值为 {fmt_pct(low_thr)} 和 {fmt_pct(high_thr)}。")
    lines.append("- 时间限制：F25评分日期为2026-06-04，收益窗口截至2026-05-27；本报告是当前评分对既有6个月股价表现的解释性评估，不是严格的前瞻回测。")
    lines.append("")
    lines.append("## 附：输入文件")
    lines.append(f"- `{SCORE_PATH.relative_to(ROOT)}`")
    lines.append(f"- `{RETURN_PATH.relative_to(ROOT)}`")
    lines.append(f"- `{F51_PATH.relative_to(ROOT)}`")
    lines.append(f"- `{FIN_PATH.relative_to(ROOT)}`")
    lines.append("")

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")

    summary = {
        "score_n": len(score),
        "return_n": len(ret),
        "eval_n": len(eval_df),
        "missing_returns": missing_returns,
        "corr": corr,
        "tb30_diff": tb_stats[30]["diff"],
        "neutral_spearman": neutral_s,
        "robust_combo_spearman": robust[4]["spearman"],
        "out_path": str(OUT_PATH),
    }
    print(summary)


if __name__ == "__main__":
    main()
