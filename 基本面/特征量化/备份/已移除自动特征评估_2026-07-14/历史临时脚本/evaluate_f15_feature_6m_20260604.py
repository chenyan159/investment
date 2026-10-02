from __future__ import annotations

import math
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from statistics import mean, median, stdev


ROOT = Path(r"D:\drive\Investment\基本面")
FEATURE_ID = "F15"
FEATURE_NAME = "6-12月利润台阶信号"
FEATURE_SUBJECT = f"{FEATURE_ID}_{FEATURE_NAME}"
RUN_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_SUBJECT}_量化评分_{RUN_DATE}.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
LIQUIDITY_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
FINANCIAL_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUT_DIR / "备份"
OUT_PATH = OUT_DIR / f"{FEATURE_SUBJECT}_特征评估_6个月涨跌_{RUN_DATE}.md"

SOXX_RETURNS = {
    "SOXX下跌1": -32.98,
    "SOXX下跌2": -15.82,
    "SOXX下跌3": -13.40,
}


@dataclass
class ScoreRow:
    rank: int
    ticker: str
    name: str
    category: str
    score: float
    evidence: str
    confidence: str


@dataclass
class ReturnRow:
    ticker: str
    name: str
    category: str
    latest_date: str
    close: str
    ret_1m: float | None
    ret_3m: float | None
    ret_6m: float | None
    ret_1y: float | None
    note: str


@dataclass
class JoinedRow:
    ticker: str
    name: str
    category: str
    score: float
    score_rank: int
    evidence: str
    confidence: str
    ret_6m: float
    risk_windows: dict[str, float | None]
    liquidity_score: float | None
    adr_or_currency_abnormal: bool


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def parse_percent(cell: str) -> float | None:
    if not cell or "N/A" in cell:
        return None
    match = re.search(r"([+-]?\d+(?:\.\d+)?)%", cell.replace(",", ""))
    if not match:
        return None
    return float(match.group(1))


def parse_number(text: str) -> float | None:
    if not text or "N/A" in text or "不适用" in text or "缺失" in text:
        return None
    cleaned = re.sub(r"[,$]", "", text.strip())
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_score_table(path: Path) -> dict[str, ScoreRow]:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_table = False
    rows: dict[str, ScoreRow] = {}
    for line in lines:
        if line.startswith("## 全公司排序表"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|"):
            continue
        cells = split_md_row(line)
        if not cells or cells[0] == "排名" or is_separator(cells):
            continue
        if len(cells) < 7:
            continue
        try:
            row = ScoreRow(
                rank=int(cells[0]),
                ticker=cells[1],
                name=cells[2],
                category=cells[3],
                score=float(cells[4]),
                evidence=cells[5],
                confidence=cells[6],
            )
        except ValueError:
            continue
        rows[row.ticker] = row
    return rows


def parse_return_tables(path: Path) -> dict[str, ReturnRow]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: dict[str, ReturnRow] = {}
    in_section = False
    current_category = ""
    header: list[str] | None = None
    for line in lines:
        if line.startswith("## 按分类分组的公司明细"):
            in_section = True
            header = None
            continue
        if not in_section:
            continue
        if line.startswith("### "):
            current_category = line[4:].strip()
            header = None
            continue
        if not line.startswith("|"):
            continue
        cells = split_md_row(line)
        if cells and cells[0] == "股票代号":
            header = cells
            continue
        if not header or is_separator(cells):
            continue
        if len(cells) < len(header) or not current_category:
            continue
        by_col = dict(zip(header, cells))
        if "6个月" not in by_col:
            continue
        ret_6m = parse_percent(by_col.get("6个月", ""))
        if ret_6m is None:
            continue
        rows[by_col["股票代号"]] = ReturnRow(
            ticker=by_col["股票代号"],
            name=by_col.get("公司名称", ""),
            category=current_category,
            latest_date=by_col.get("最新交易日", ""),
            close=by_col.get("最新收盘价", ""),
            ret_1m=parse_percent(by_col.get("1个月", "")),
            ret_3m=parse_percent(by_col.get("3个月", "")),
            ret_6m=ret_6m,
            ret_1y=parse_percent(by_col.get("1年", "")),
            note=by_col.get("备注", ""),
        )
    return rows


def parse_risk_windows(path: Path) -> dict[str, dict[str, float | None]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: dict[str, dict[str, float | None]] = {}
    in_section = False
    in_risk_detail = False
    header: list[str] | None = None
    for line in lines:
        if line.startswith("## SOXX最大下跌窗口全公司涨跌幅"):
            in_section = True
            continue
        if in_section and line.startswith("### 按分类分组的全公司明细"):
            in_risk_detail = True
            header = None
            continue
        if in_risk_detail and line.startswith("## 按分类分组的公司明细"):
            break
        if not in_risk_detail or not line.startswith("|"):
            continue
        cells = split_md_row(line)
        if cells and cells[0] == "股票代号":
            header = cells
            continue
        if not header or is_separator(cells) or len(cells) < len(header):
            continue
        by_col = dict(zip(header, cells))
        ticker = by_col.get("股票代号", "")
        if not ticker:
            continue
        rows[ticker] = {
            "SOXX下跌1": parse_percent(by_col.get("SOXX下跌1 2025-02-20至2025-04-08", "")),
            "SOXX下跌2": parse_percent(by_col.get("SOXX下跌2 2026-02-25至2026-03-30", "")),
            "SOXX下跌3": parse_percent(by_col.get("SOXX下跌3 2025-10-29至2025-11-20", "")),
        }
    return rows


def parse_daily_financial(path: Path) -> dict[str, dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: dict[str, dict[str, str]] = {}
    in_section = False
    header: list[str] | None = None
    for line in lines:
        if line.startswith("## 按项目分类分组的公司明细表"):
            in_section = True
            header = None
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = split_md_row(line)
        if cells and cells[0] == "股票代号":
            header = cells
            continue
        if not header or is_separator(cells) or len(cells) < len(header):
            continue
        by_col = dict(zip(header, cells))
        ticker = by_col.get("股票代号", "")
        if ticker:
            rows[ticker] = by_col
    return rows


def adr_currency_abnormal(row: dict[str, str] | None) -> bool:
    if not row:
        return True
    listing_type = row.get("listing_type", "")
    adr_ratio = row.get("adr_ratio", "")
    currency = row.get("currency", "")
    financial_currency = row.get("financial_currency", "")
    valuation_check = row.get("估值校验", "")
    note = row.get("备注", "")
    if "ADR" in listing_type or "ADS" in listing_type:
        return True
    if adr_ratio and adr_ratio != "不适用":
        return True
    if currency and financial_currency and currency != financial_currency:
        return True
    if "currency_mismatch" in valuation_check:
        return True
    if "ADR" in note or "ADS" in note or "currency_mismatch" in note or "交易货币" in note:
        return True
    return False


def rankdata(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2
        for k in range(i, j):
            ranks[indexed[k][0]] = avg_rank
        i = j
    return ranks


def pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return float("nan")
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return float("nan")
    return num / (den_x * den_y)


def spearman(xs: list[float], ys: list[float]) -> float:
    return pearson(rankdata(xs), rankdata(ys))


def kendall_tau_b(xs: list[float], ys: list[float]) -> float:
    c = d = tx = ty = 0
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            dx = (xs[i] > xs[j]) - (xs[i] < xs[j])
            dy = (ys[i] > ys[j]) - (ys[i] < ys[j])
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                tx += 1
            elif dy == 0:
                ty += 1
            elif dx == dy:
                c += 1
            else:
                d += 1
    denom = math.sqrt((c + d + tx) * (c + d + ty))
    if denom == 0:
        return float("nan")
    return (c - d) / denom


def correlations(rows: list[JoinedRow], score_attr: str = "score", ret_attr: str = "ret_6m") -> dict[str, float]:
    xs = [getattr(row, score_attr) for row in rows]
    ys = [getattr(row, ret_attr) for row in rows]
    return {
        "pearson": pearson(xs, ys),
        "spearman": spearman(xs, ys),
        "kendall": kendall_tau_b(xs, ys),
    }


def fmt_num(value: float | None, digits: int = 3) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    return f"{value:.{digits}f}"


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{digits}f}%"


def group_stats(rows: list[JoinedRow]) -> dict[str, float]:
    returns = [row.ret_6m for row in rows]
    scores = [row.score for row in rows]
    return {
        "n": len(rows),
        "score_mean": mean(scores) if scores else float("nan"),
        "ret_mean": mean(returns) if returns else float("nan"),
        "ret_median": median(returns) if returns else float("nan"),
        "hit_rate": sum(1 for value in returns if value > 0) / len(returns) * 100 if returns else float("nan"),
    }


def top_bottom(rows: list[JoinedRow], n: int, key=lambda row: row.score) -> dict[str, float]:
    ordered = sorted(rows, key=lambda row: (key(row), -row.score_rank), reverse=True)
    top = ordered[:n]
    bottom = ordered[-n:]
    top_s = group_stats(top)
    bottom_s = group_stats(bottom)
    return {
        "top_mean": top_s["ret_mean"],
        "top_hit": top_s["hit_rate"],
        "bottom_mean": bottom_s["ret_mean"],
        "bottom_hit": bottom_s["hit_rate"],
        "spread": top_s["ret_mean"] - bottom_s["ret_mean"],
    }


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return float("nan")
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * p / 100
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - pos) + ordered[hi] * (pos - lo)


def neutral_percentiles(rows: list[JoinedRow]) -> dict[str, float]:
    by_cat: dict[str, list[JoinedRow]] = defaultdict(list)
    for row in rows:
        by_cat[row.category].append(row)
    result: dict[str, float] = {}
    for cat_rows in by_cat.values():
        scores = [row.score for row in cat_rows]
        ranks = rankdata(scores)
        denom = len(cat_rows) - 1
        for row, rank in zip(cat_rows, ranks):
            result[row.ticker] = 0.5 if denom == 0 else (rank - 1) / denom
    return result


def category_residual_rows(rows: list[JoinedRow]) -> tuple[list[float], list[float]]:
    by_cat: dict[str, list[JoinedRow]] = defaultdict(list)
    for row in rows:
        by_cat[row.category].append(row)
    xs: list[float] = []
    ys: list[float] = []
    for cat_rows in by_cat.values():
        score_avg = mean(row.score for row in cat_rows)
        ret_avg = mean(row.ret_6m for row in cat_rows)
        for row in cat_rows:
            xs.append(row.score - score_avg)
            ys.append(row.ret_6m - ret_avg)
    return xs, ys


def risk_group_stats(rows: list[JoinedRow]) -> dict[str, float | int]:
    observations: list[float] = []
    per_window: dict[str, list[float]] = {key: [] for key in SOXX_RETURNS}
    worst_by_company: list[float] = []
    beat_soxx = 0
    negative = 0
    for row in rows:
        company_values: list[float] = []
        for key, soxx_ret in SOXX_RETURNS.items():
            value = row.risk_windows.get(key)
            if value is None:
                continue
            observations.append(value)
            per_window[key].append(value)
            company_values.append(value)
            if value > soxx_ret:
                beat_soxx += 1
            if value < 0:
                negative += 1
        if company_values:
            worst_by_company.append(min(company_values))
    return {
        "n": len(rows),
        "obs": len(observations),
        "soxx1": mean(per_window["SOXX下跌1"]) if per_window["SOXX下跌1"] else float("nan"),
        "soxx2": mean(per_window["SOXX下跌2"]) if per_window["SOXX下跌2"] else float("nan"),
        "soxx3": mean(per_window["SOXX下跌3"]) if per_window["SOXX下跌3"] else float("nan"),
        "pressure_mean": mean(observations) if observations else float("nan"),
        "avg_worst": mean(worst_by_company) if worst_by_company else float("nan"),
        "dispersion": stdev(observations) if len(observations) > 1 else 0.0,
        "beat_soxx": beat_soxx / len(observations) * 100 if observations else float("nan"),
        "negative": negative / len(observations) * 100 if observations else float("nan"),
    }


def md_table(headers: list[str], rows: list[list[str]], aligns: list[str] | None = None) -> str:
    aligns = aligns or ["---"] * len(headers)
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join(aligns) + " |"]
    output.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(output)


def top_bottom_rows(rows: list[JoinedRow], n: int) -> list[list[str]]:
    ordered = sorted(rows, key=lambda row: (row.score, -row.score_rank), reverse=True)
    output: list[list[str]] = []
    for label, part in [("Top10", ordered[:n]), ("Bottom10", ordered[-n:])]:
        for row in part:
            output.append([
                label,
                row.ticker,
                row.name,
                row.category,
                f"{row.score:.1f}",
                str(row.score_rank),
                fmt_pct(row.ret_6m),
            ])
    return output


def describe_validity(spearman_value: float) -> str:
    if abs(spearman_value) < 0.05:
        return "接近0；排序分核心指标不支持有效"
    if spearman_value >= 0.20:
        return "为正且有一定排序解释力"
    if spearman_value > 0:
        return "小幅为正，但强度偏弱"
    if spearman_value <= -0.20:
        return "明显为负，方向与预期相反"
    return "小幅为负，排序解释力偏弱"


def make_report() -> str:
    scores = parse_score_table(SCORE_PATH)
    returns = parse_return_tables(RETURN_PATH)
    risk = parse_risk_windows(RETURN_PATH)
    liquidity = parse_score_table(LIQUIDITY_PATH)
    financial = parse_daily_financial(FINANCIAL_PATH)

    joined: list[JoinedRow] = []
    for ticker, score in scores.items():
        ret = returns.get(ticker)
        if ret is None:
            continue
        joined.append(
            JoinedRow(
                ticker=ticker,
                name=score.name,
                category=score.category,
                score=score.score,
                score_rank=score.rank,
                evidence=score.evidence,
                confidence=score.confidence,
                ret_6m=ret.ret_6m,
                risk_windows=risk.get(ticker, {}),
                liquidity_score=liquidity[ticker].score if ticker in liquidity else None,
                adr_or_currency_abnormal=adr_currency_abnormal(financial.get(ticker)),
            )
        )

    joined = sorted(joined, key=lambda row: (row.score, -row.score_rank), reverse=True)
    score_missing_return = sorted(set(scores) - set(returns))
    return_missing_score = sorted(set(returns) - set(scores))
    corr = correlations(joined)

    by_cat: dict[str, list[JoinedRow]] = defaultdict(list)
    for row in joined:
        by_cat[row.category].append(row)

    cat_rows = []
    for category, cat_items in sorted(by_cat.items()):
        stats = group_stats(cat_items)
        cat_rows.append([
            category,
            str(stats["n"]),
            f"{stats['score_mean']:.2f}",
            fmt_pct(stats["ret_mean"]),
            fmt_pct(stats["ret_median"]),
        ])

    ordered_by_score = sorted(joined, key=lambda row: (row.score, -row.score_rank), reverse=True)
    # Similar to prior reports, use five score bands after sorting. This is diagnostic only.
    quintile_sizes = [len(joined) // 5, len(joined) // 5, len(joined) // 5 + 1, len(joined) // 5, len(joined) - (4 * (len(joined) // 5) + 1)]
    quintile_rows = []
    cursor = 0
    for label, size in zip(["Q1最高分", "Q2", "Q3", "Q4", "Q5"], quintile_sizes):
        part = ordered_by_score[cursor: cursor + size]
        cursor += size
        stats = group_stats(part)
        quintile_rows.append([
            label,
            str(stats["n"]),
            f"{stats['score_mean']:.2f}",
            fmt_pct(stats["ret_mean"]),
            fmt_pct(stats["ret_median"]),
            fmt_pct(stats["hit_rate"], 1),
        ])

    tb_rows = []
    tb_metrics_by_n = {}
    for n in [10, 20, 30]:
        tb = top_bottom(joined, n)
        tb_metrics_by_n[n] = tb
        tb_rows.append([
            f"Top{n}/Bottom{n}",
            fmt_pct(tb["top_mean"]),
            fmt_pct(tb["top_hit"], 1),
            fmt_pct(tb["bottom_mean"]),
            fmt_pct(tb["bottom_hit"], 1),
            fmt_pct(tb["spread"]),
        ])

    top30 = ordered_by_score[:30]
    bottom30 = ordered_by_score[-30:]
    mid_start = max(0, (len(ordered_by_score) - 30) // 2)
    mid30 = ordered_by_score[mid_start: mid_start + 30]
    risk_rows = []
    risk_stats_by_label = {}
    for label, part in [("F15 Top30", top30), ("F15 Mid30", mid30), ("F15 Bottom30", bottom30)]:
        stats = risk_group_stats(part)
        risk_stats_by_label[label] = stats
        risk_rows.append([
            label,
            str(stats["n"]),
            str(stats["obs"]),
            fmt_pct(stats["soxx1"]),
            fmt_pct(stats["soxx2"]),
            fmt_pct(stats["soxx3"]),
            fmt_pct(stats["pressure_mean"]),
            fmt_pct(stats["avg_worst"]),
            fmt_pct(stats["dispersion"]),
            fmt_pct(stats["beat_soxx"], 1),
            fmt_pct(stats["negative"], 1),
        ])

    neutral_pct = neutral_percentiles(joined)
    neutral_score_rows = []
    for row in joined:
        setattr(row, "neutral_pct", neutral_pct[row.ticker])
    neutral_x = [neutral_pct[row.ticker] for row in joined]
    neutral_y = [row.ret_6m for row in joined]
    residual_x, residual_y = category_residual_rows(joined)
    neutral_corr = {
        "raw": corr,
        "pct": {
            "pearson": pearson(neutral_x, neutral_y),
            "spearman": spearman(neutral_x, neutral_y),
            "kendall": kendall_tau_b(neutral_x, neutral_y),
        },
        "resid": {
            "pearson": pearson(residual_x, residual_y),
            "spearman": spearman(residual_x, residual_y),
            "kendall": kendall_tau_b(residual_x, residual_y),
        },
    }
    neutral_rows = [
        ["原始全样本", str(len(joined)), fmt_num(corr["pearson"]), fmt_num(corr["spearman"]), fmt_num(corr["kendall"]), "直接用F15分数排序"],
        ["分类内百分位合并", str(len(joined)), fmt_num(neutral_corr["pct"]["pearson"]), fmt_num(neutral_corr["pct"]["spearman"]), fmt_num(neutral_corr["pct"]["kendall"]), "每个分类内先按F15排序，再转成0-1百分位合并"],
        ["分类去均值残差", str(len(joined)), fmt_num(neutral_corr["resid"]["pearson"]), fmt_num(neutral_corr["resid"]["spearman"]), fmt_num(neutral_corr["resid"]["kendall"]), "F15和收益分别减去分类均值后相关"],
    ]

    neutral_tb_rows = []
    neutral_ordered = sorted(joined, key=lambda row: neutral_pct[row.ticker], reverse=True)
    for n in [10, 20, 30]:
        top = neutral_ordered[:n]
        bottom = neutral_ordered[-n:]
        top_s = group_stats(top)
        bottom_s = group_stats(bottom)
        neutral_tb_rows.append([
            f"中性Top{n}/Bottom{n}",
            fmt_pct(top_s["ret_mean"]),
            fmt_pct(top_s["hit_rate"], 1),
            fmt_pct(bottom_s["ret_mean"]),
            fmt_pct(bottom_s["hit_rate"], 1),
            fmt_pct(top_s["ret_mean"] - bottom_s["ret_mean"]),
        ])

    cat_corr_rows = []
    for category, cat_items in sorted(by_cat.items()):
        cat_corr = correlations(cat_items)
        highest_ret = max(cat_items, key=lambda row: row.ret_6m)
        highest_score = max(cat_items, key=lambda row: (row.score, -row.score_rank))
        cat_corr_rows.append([
            category,
            str(len(cat_items)),
            fmt_num(cat_corr["pearson"]),
            fmt_num(cat_corr["spearman"]),
            fmt_pct(mean(row.ret_6m for row in cat_items)),
            f"{highest_ret.ticker} {fmt_pct(highest_ret.ret_6m)}",
            f"{highest_score.ticker} {highest_score.score:.1f} / {fmt_pct(highest_score.ret_6m)}",
        ])

    all_returns = [row.ret_6m for row in joined]
    low_cut = percentile(all_returns, 5)
    high_cut = percentile(all_returns, 95)
    low_liquidity = sorted([row.ticker for row in joined if row.liquidity_score is None or row.liquidity_score <= 5.0])
    adr_abnormal = sorted([row.ticker for row in joined if row.adr_or_currency_abnormal])
    extreme = sorted([row.ticker for row in joined if row.ret_6m <= low_cut or row.ret_6m >= high_cut])

    robustness_specs = [
        ("全样本基准", "无剔除", joined),
        ("剔除低流动性", "F51交易流动性分 > 5.0", [row for row in joined if row.ticker not in set(low_liquidity)]),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", [row for row in joined if row.ticker not in set(adr_abnormal)]),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(low_cut)} / {fmt_pct(high_cut)}", [row for row in joined if row.ticker not in set(extreme)]),
        ("三项合并剔除", "同时满足上述三项", [row for row in joined if row.ticker not in set(low_liquidity) and row.ticker not in set(adr_abnormal) and row.ticker not in set(extreme)]),
    ]
    robustness_rows = []
    for label, rule, part in robustness_specs:
        part_corr = correlations(part) if len(part) >= 3 else {"pearson": float("nan"), "spearman": float("nan"), "kendall": float("nan")}
        n_top = min(30, len(part) // 2)
        tb = top_bottom(part, n_top) if n_top else {"top_mean": float("nan"), "bottom_mean": float("nan"), "spread": float("nan")}
        robustness_rows.append([
            label,
            rule,
            str(len(part)),
            str(len(joined) - len(part)),
            fmt_num(part_corr["pearson"]),
            fmt_num(part_corr["spearman"]),
            fmt_num(part_corr["kendall"]),
            fmt_pct(tb["top_mean"]),
            fmt_pct(tb["bottom_mean"]),
            fmt_pct(tb["spread"]),
        ])

    top_ret15 = sorted(joined, key=lambda row: row.ret_6m, reverse=True)[:15]
    top_score15 = ordered_by_score[:15]
    top_ret_rows = [[row.ticker, row.name, row.category, fmt_pct(row.ret_6m), f"{row.score:.1f}", str(row.score_rank), row.confidence] for row in top_ret15]
    top_score_rows = [[row.ticker, row.name, row.category, f"{row.score:.1f}", str(row.score_rank), fmt_pct(row.ret_6m), row.confidence] for row in top_score15]

    score_top_names = ", ".join(row.ticker for row in top_score15[:8])
    ret_top_names = ", ".join(row.ticker for row in top_ret15[:8])
    spearman_text = describe_validity(corr["spearman"])
    tb30 = tb_metrics_by_n[30]
    risk_top = risk_stats_by_label["F15 Top30"]
    risk_bottom = risk_stats_by_label["F15 Bottom30"]
    robust_combined_spearman = float(robustness_rows[-1][5])

    if corr["spearman"] >= 0.05:
        sorting_conclusion = "部分成立" if corr["spearman"] < 0.20 else "成立"
    elif corr["spearman"] <= -0.05:
        sorting_conclusion = "不成立，且方向略负"
    else:
        sorting_conclusion = "不成立"

    if tb30["spread"] > 0 and tb_metrics_by_n[10]["spread"] > 0:
        top_bottom_conclusion = "部分成立"
    else:
        top_bottom_conclusion = "不成立"

    risk_conclusion = (
        "部分成立但不是完整保护性结论"
        if risk_top["pressure_mean"] > risk_bottom["pressure_mean"] or risk_top["avg_worst"] > risk_bottom["avg_worst"]
        else "不成立"
    )

    neutral_spearman = neutral_corr["pct"]["spearman"]
    neutral_conclusion = "仍有弱正向" if neutral_spearman > 0.05 else ("方向转弱或为负" if neutral_spearman < 0 else "接近0")

    robust_text = "不稳定"
    robustness_spearmans = [float(row[5]) for row in robustness_rows]
    if min(robustness_spearmans) >= 0.05 and corr["spearman"] >= 0.05:
        robust_text = "弱稳定"
    elif robust_combined_spearman >= 0.05 and corr["spearman"] >= 0.05:
        robust_text = "不稳定，但合并剔除后保留弱正"

    report_lines: list[str] = []
    report_lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 6个月涨跌 {RUN_DATE}")
    report_lines.append("")
    report_lines.append("## 运行元信息")
    report_lines.extend([
        f"- 评估对象：{FEATURE_SUBJECT}。",
        f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 {RUN_DATE}，覆盖 {len(scores)} 家。",
        f"- 收益输入：`日度资料/区间涨跌/{RETURN_PATH.name}`，生成时间 2026-05-27 20:17:54 -0700，价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。",
        "- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。",
        f"- 稳健性辅助输入：`特征量化/量化评分/{LIQUIDITY_PATH.name}`；`日度资料/每日金融数据/{FINANCIAL_PATH.name}`。",
        f"- 有效评估样本：评分与6个月涨跌交集 {len(joined)} 家；F15评分有但6个月涨跌缺失 {len(score_missing_return)} 家。",
        "- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。",
        "- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为风险代理。",
        "- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。",
        "- 旧版处理：写入前已检查 `特征量化/特征评估/` 根目录同类 F15 正式输出；若有残留会移动到 `特征量化/特征评估/备份/`。本次未读取旧版 F15 特征评估作为结论依据。",
    ])
    report_lines.append("")
    report_lines.append("## 结论摘要")
    report_lines.extend([
        f"- 排序有效性：{sorting_conclusion}。全样本 Pearson {fmt_num(corr['pearson'])}, Spearman {fmt_num(corr['spearman'])}, Kendall {fmt_num(corr['kendall'])}；最重要的 Spearman {spearman_text}。",
        f"- Top/Bottom能力：{top_bottom_conclusion}。Top10、Top20、Top30 的平均收益分别为 {fmt_pct(tb_metrics_by_n[10]['top_mean'])}、{fmt_pct(tb_metrics_by_n[20]['top_mean'])}、{fmt_pct(tb_metrics_by_n[30]['top_mean'])}；Top-Bottom 收益差分别为 {fmt_pct(tb_metrics_by_n[10]['spread'])}、{fmt_pct(tb_metrics_by_n[20]['spread'])}、{fmt_pct(tb_metrics_by_n[30]['spread'])}。",
        f"- 风险解释力：{risk_conclusion}。Top30 压力窗口均值 {fmt_pct(risk_top['pressure_mean'])}，Bottom30 为 {fmt_pct(risk_bottom['pressure_mean'])}；Top30 平均最差窗口 {fmt_pct(risk_top['avg_worst'])}，Bottom30 为 {fmt_pct(risk_bottom['avg_worst'])}；Top30 窗口离散度 {fmt_pct(risk_top['dispersion'])}，Bottom30 为 {fmt_pct(risk_bottom['dispersion'])}。",
        f"- 分类中性：{neutral_conclusion}。按10个分类目录内重新排序并合并后，Spearman {fmt_num(neutral_spearman)}；分类去均值残差口径 Spearman {fmt_num(neutral_corr['resid']['spearman'])}。",
        f"- 稳健性：{robust_text}。剔除低流动性后 Spearman {robustness_rows[1][5]}, 剔除ADR/币种异常后为 {robustness_rows[2][5]}, 剔除极端涨跌后为 {robustness_rows[3][5]}, 三项合并后为 {robustness_rows[4][5]}。",
        f"- 解释：F15 衡量未来 6-12 个月利润额、利润率、EPS或FCF是否存在公司级台阶，理论上更适合捕捉收入向毛利、经营杠杆、现金流和每股收益兑现的中期质量；但本次6个月收益由 {ret_top_names} 等高弹性、修复型或价格重估标的主导，F15高分的 {score_top_names} 多数是利润台阶可见度强的主线公司，未必等同于最高价格弹性。",
    ])
    report_lines.append("")
    report_lines.append("## 覆盖检查")
    report_lines.append(md_table(
        ["项目", "数量", "说明"],
        [
            ["F15评分覆盖", str(len(scores)), "来自2026-06-04评分文件"],
            ["6个月涨跌覆盖", str(len(returns)), "来自2026-05-27区间涨跌文件"],
            ["交集样本", str(len(joined)), "用于本次所有主指标"],
            ["评分有但6个月涨跌缺失", str(len(score_missing_return)), ", ".join(score_missing_return) if score_missing_return else "无"],
            ["涨跌有但评分缺失", str(len(return_missing_score)), ", ".join(return_missing_score) if return_missing_score else "无"],
        ],
        ["---", "---:", "---"],
    ))
    report_lines.append("")
    report_lines.append("### 交集样本分类分布")
    report_lines.append(md_table(["分类目录", "样本数", "F15均分", "6个月平均收益", "6个月中位收益"], cat_rows, ["---", "---:", "---:", "---:", "---:"]))
    report_lines.append("")
    report_lines.append("## 排序有效性")
    report_lines.append(md_table(
        ["指标", "数值", "解释"],
        [
            ["Pearson", fmt_num(corr["pearson"]), "线性相关；受极端涨跌影响较大"],
            ["Spearman", fmt_num(corr["spearman"]), spearman_text],
            ["Kendall tau-b", fmt_num(corr["kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
        ],
        ["---", "---:", "---"],
    ))
    report_lines.append("")
    report_lines.append("### 分数分组收益")
    report_lines.append(md_table(["分组", "公司数", "F15均分", "6个月平均收益", "6个月中位收益", "命中率"], quintile_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    report_lines.append("")
    report_lines.append("## Top/Bottom能力")
    report_lines.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], tb_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    report_lines.append("")
    report_lines.append("### Top10与Bottom10构成")
    report_lines.append(md_table(["组别", "股票代号", "公司名称", "分类目录", "F15分", "F15排名", "6个月收益"], top_bottom_rows(joined, 10), ["---", "---", "---", "---", "---:", "---:", "---:"]))
    report_lines.append("")
    report_lines.append("## 风险解释力")
    report_lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为压力测试代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供，故不写成严格波动率结论。")
    report_lines.append(md_table(
        ["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"],
        risk_rows,
        ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
    ))
    report_lines.append("")
    report_lines.append(f"结论：Top30 的压力窗口均值为 {fmt_pct(risk_top['pressure_mean'])}，与 Bottom30 的 {fmt_pct(risk_bottom['pressure_mean'])} 比较后，F15高分组是否更抗跌需要谨慎解释；这只能说明在三段 SOXX 压力窗口内的相对表现，不能替代逐日波动率或最大回撤。")
    report_lines.append("")
    report_lines.append("## 分类中性结果")
    report_lines.append(md_table(["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"], neutral_rows, ["---", "---:", "---:", "---:", "---:", "---"]))
    report_lines.append("")
    report_lines.append("### 分类中性Top/Bottom")
    report_lines.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], neutral_tb_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    report_lines.append("")
    report_lines.append("### 10个分类目录内相关性")
    report_lines.append(md_table(
        ["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F15公司"],
        cat_corr_rows,
        ["---", "---:", "---:", "---:", "---:", "---", "---"],
    ))
    report_lines.append("")
    report_lines.append("分类内结果用于识别是否只是押中某个目录。若原始全样本与分类内百分位、分类残差口径方向相近，则说明结果不是单一行业暴露造成；若方向变化，则说明行业结构和个股极值共同影响较大。")
    report_lines.append("")
    report_lines.append("## 稳健性检验")
    report_lines.append(md_table(
        ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"],
        robustness_rows,
        ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
    ))
    report_lines.append("")
    report_lines.append(f"稳健性结论：剔除低流动性、ADR/币种异常和极端涨跌后，Spearman 是否保留正向排序是核心判断。本次三项合并后 Spearman 为 {robustness_rows[4][5]}，因此 F15 对6个月收益的独立排序解释力不能单独使用，需要和估值、动量、流动性、催化剂等特征联用。")
    report_lines.append("")
    report_lines.append("### 剔除清单")
    report_lines.append(md_table(
        ["剔除项", "数量", "公司"],
        [
            ["低流动性", str(len(low_liquidity)), ", ".join(low_liquidity)],
            ["ADR/币种异常", str(len(adr_abnormal)), ", ".join(adr_abnormal)],
            ["极端涨跌双尾5%", str(len(extreme)), ", ".join(extreme)],
        ],
        ["---", "---:", "---"],
    ))
    report_lines.append("")
    report_lines.append("## 诊断：收益由哪些公司主导")
    report_lines.append("### 6个月涨幅前15")
    report_lines.append(md_table(["股票代号", "公司名称", "分类目录", "6个月收益", "F15分", "F15排名", "F15置信度"], top_ret_rows, ["---", "---", "---", "---:", "---:", "---:", "---"]))
    report_lines.append("")
    report_lines.append("### F15分数前15")
    report_lines.append(md_table(["股票代号", "公司名称", "分类目录", "F15分", "F15排名", "6个月收益", "F15置信度"], top_score_rows, ["---", "---", "---", "---:", "---:", "---:", "---"]))
    report_lines.append("")
    report_lines.append("诊断结论：F15高分公司体现未来利润台阶、毛利率和经营杠杆的可见度，但本窗口股价收益的头部更多来自存储、光互联、小中盘修复和低基数弹性。F15可以解释一部分“利润兑现质量”，但不能直接替代短中期价格弹性、估值修复或事件催化因子。")
    report_lines.append("")
    report_lines.append("## 最终判断与后续使用")
    report_lines.extend([
        f"- 对“6个月价格涨跌排序”的单因子预测：{FEATURE_SUBJECT}本轮评估为{sorting_conclusion}，不建议单独用于6个月收益排序。",
        "- 对风险解释：F15高分组是否更抗跌只能在SOXX压力窗口代理下观察；本次没有逐日价格序列，不能给出严格波动率、最大回撤或下跌日收益结论。",
        "- 对组合使用：F15更像利润台阶、利润率改善、EPS/FCF兑现和中期质量因子。后续应与F05估值赔率、F37-F39催化剂、F50价格相对强度、F51交易流动性、极端涨跌过滤联用。",
        "- 对上游资料：本报告只作为下游特征评估，不反向修改公司调研、行业调研或日度事实资料。",
    ])
    report_lines.append("")
    report_lines.append("## 附：关键口径复述")
    report_lines.extend([
        "- 6个月收益：区间涨跌文件中的 `6个月` 字段，百分比单位，不含股息再投资。",
        "- 低流动性剔除：F51交易流动性分数缺失或不高于 5.0。",
        "- ADR/币种异常剔除：`listing_type` 为 ADR/ADS、ADR比例非不适用、交易货币与财报货币不一致、估值校验含 `currency_mismatch` 或备注提示 ADR/币种需确认。",
        f"- 极端涨跌剔除：按本次{len(joined)}家6个月收益双尾5%剔除，阈值为 {fmt_pct(low_cut)} 和 {fmt_pct(high_cut)}。",
    ])
    report_lines.append("")
    return "\n".join(report_lines)


def backup_old_outputs() -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    old_files = sorted(OUT_DIR.glob(f"{FEATURE_SUBJECT}_特征评估_6个月涨跌_*.md"))
    moved: list[Path] = []
    if not old_files:
        return moved
    tz = timezone(timedelta(hours=-7))
    stamp = datetime.now(tz).strftime("%Y-%m-%dT%H_%M_%S-07_00")
    target_dir = BACKUP_DIR / f"{FEATURE_SUBJECT}_6个月涨跌_{stamp}"
    target_dir.mkdir(parents=True, exist_ok=True)
    for old_file in old_files:
        destination = target_dir / old_file.name
        shutil.move(str(old_file), str(destination))
        moved.append(destination)
    return moved


def main() -> None:
    for path in [SCORE_PATH, RETURN_PATH, LIQUIDITY_PATH, FINANCIAL_PATH]:
        if not path.exists():
            raise FileNotFoundError(path)
    report = make_report()
    moved = backup_old_outputs()
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(f"wrote={OUT_PATH}")
    print(f"bytes={OUT_PATH.stat().st_size}")
    print(f"backed_up={len(moved)}")
    for path in moved:
        print(f"backup={path}")


if __name__ == "__main__":
    main()

