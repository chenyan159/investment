from __future__ import annotations

import math
import os
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np


ROOT = Path(r"D:\drive\Investment\基本面")
FEATURE_ID = "F39"
FEATURE_NAME = "6-12月催化剂强度"
FEATURE_SUBJECT = f"{FEATURE_ID}_{FEATURE_NAME}"
RUN_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_SUBJECT}_量化评分_{RUN_DATE}.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
FINANCE_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
LIQ_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
OUT_PATH = OUT_DIR / f"{FEATURE_SUBJECT}_特征评估_6个月涨跌_{RUN_DATE}.md"
BACKUP_DIR = OUT_DIR / "备份"

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
    evidence_grade: str
    confidence: str
    evidence: str
    missing: str
    followup: str


@dataclass
class ReturnRow:
    ticker: str
    name: str
    category: str
    latest_date: str
    latest_close: str
    ret_6m: float
    base_date_6m: str
    note: str


@dataclass
class FinanceRow:
    ticker: str
    name: str
    category: str
    call_iv: float | None
    put_iv: float | None
    currency: str
    financial_currency: str
    listing_type: str
    adr_ratio: str
    valuation_check: str
    note: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_md_row(line: str) -> list[str]:
    line = line.strip()
    if not (line.startswith("|") and line.endswith("|")):
        return []
    return [cell.strip() for cell in line.strip("|").split("|")]


def is_separator(line: str) -> bool:
    if not line.strip().startswith("|"):
        return False
    cells = split_md_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells)


def parse_percent_cell(cell: str) -> float | None:
    if not cell or "N/A" in cell or "缺失" in cell:
        return None
    m = re.search(r"([+-]?\d+(?:\.\d+)?)%", cell)
    if not m:
        return None
    val = float(m.group(1))
    if val == 0:
        return 0.0
    if "下跌" in cell and val > 0:
        val = -val
    return val


def parse_base_date(cell: str) -> str:
    m = re.search(r"基准\s+(\d{4}-\d{2}-\d{2})", cell)
    return m.group(1) if m else ""


def parse_iv(cell: str) -> float | None:
    return parse_percent_cell(cell)


def parse_score_file(path: Path) -> dict[str, ScoreRow]:
    rows: dict[str, ScoreRow] = {}
    lines = read_text(path).splitlines()
    in_table = False
    headers: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("| 排名 | 股票代号 | 公司名称 | 分类目录 | 特征分 |"):
            headers = split_md_row(line)
            in_table = True
            continue
        if in_table:
            if is_separator(line):
                continue
            if not line.strip().startswith("|"):
                break
            cells = split_md_row(line)
            if len(cells) != len(headers):
                raise ValueError(f"score row has {len(cells)} cells at line {i+1}: {line[:120]}")
            d = dict(zip(headers, cells))
            ticker = d["股票代号"]
            rows[ticker] = ScoreRow(
                rank=int(d["排名"]),
                ticker=ticker,
                name=d["公司名称"],
                category=d["分类目录"],
                score=float(d["特征分"]),
                evidence_grade=d["证据等级"],
                confidence=d["置信度"],
                evidence=d["核心证据"],
                missing=d["缺失/降权"],
                followup=d["后续核验"],
            )
    if not rows:
        raise ValueError(f"no score rows parsed from {path}")
    return rows


def parse_return_file(path: Path) -> tuple[dict[str, ReturnRow], dict[str, dict[str, float | None]]]:
    lines = read_text(path).splitlines()
    returns: dict[str, ReturnRow] = {}
    stress: dict[str, dict[str, float | None]] = defaultdict(dict)

    section = None
    category = None
    headers: list[str] = []
    mode: str | None = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## 按分类分组的公司明细"):
            section = "returns"
            category = None
            headers = []
            mode = None
            continue
        if stripped.startswith("### 按分类分组的全公司明细"):
            section = "stress"
            category = None
            headers = []
            mode = None
            continue
        if stripped.startswith("## ") and section in {"returns", "stress"}:
            section = None
            category = None
            headers = []
            mode = None
            continue
        if section in {"returns", "stress"} and stripped.startswith("#### "):
            category = stripped[5:].strip()
            headers = []
            mode = None
            continue
        if section == "returns" and stripped.startswith("### "):
            category = stripped[4:].strip()
            headers = []
            mode = None
            continue
        if not section:
            continue

        if stripped.startswith("| 股票代号 | 公司名称 |"):
            headers = split_md_row(line)
            mode = section
            continue
        if mode and is_separator(line):
            continue
        if mode and stripped.startswith("|"):
            cells = split_md_row(line)
            if len(cells) != len(headers):
                raise ValueError(f"{mode} row has {len(cells)} cells at line {i+1}: {line[:120]}")
            d = dict(zip(headers, cells))
            ticker = d["股票代号"]
            if mode == "returns":
                ret = parse_percent_cell(d["6个月"])
                if ret is None:
                    continue
                returns[ticker] = ReturnRow(
                    ticker=ticker,
                    name=d["公司名称"],
                    category=category or "",
                    latest_date=d["最新交易日"],
                    latest_close=d["最新收盘价"],
                    ret_6m=ret,
                    base_date_6m=parse_base_date(d["6个月"]),
                    note=d.get("备注", ""),
                )
            elif mode == "stress":
                for col in headers:
                    if col.startswith("SOXX下跌1"):
                        stress[ticker]["SOXX下跌1"] = parse_percent_cell(d[col])
                    elif col.startswith("SOXX下跌2"):
                        stress[ticker]["SOXX下跌2"] = parse_percent_cell(d[col])
                    elif col.startswith("SOXX下跌3"):
                        stress[ticker]["SOXX下跌3"] = parse_percent_cell(d[col])
    if not returns:
        raise ValueError(f"no return rows parsed from {path}")
    return returns, stress


def parse_finance_file(path: Path) -> dict[str, FinanceRow]:
    lines = read_text(path).splitlines()
    rows: dict[str, FinanceRow] = {}
    in_section = False
    category = None
    headers: list[str] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## 按项目分类分组的公司明细表"):
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if not in_section:
            continue
        if stripped.startswith("### "):
            category = stripped[4:].strip()
            headers = []
            continue
        if stripped.startswith("| 股票代号 | 公司名称 | 价格日期 |"):
            headers = split_md_row(line)
            continue
        if headers and is_separator(line):
            continue
        if headers and stripped.startswith("|"):
            cells = split_md_row(line)
            if len(cells) != len(headers):
                raise ValueError(f"finance row has {len(cells)} cells at line {i+1}: {line[:120]}")
            d = dict(zip(headers, cells))
            rows[d["股票代号"]] = FinanceRow(
                ticker=d["股票代号"],
                name=d["公司名称"],
                category=category or "",
                call_iv=parse_iv(d.get("Call IV", "")),
                put_iv=parse_iv(d.get("Put IV", "")),
                currency=d.get("currency", ""),
                financial_currency=d.get("financial_currency", ""),
                listing_type=d.get("listing_type", ""),
                adr_ratio=d.get("adr_ratio", ""),
                valuation_check=d.get("估值校验", ""),
                note=d.get("备注", ""),
            )
    if not rows:
        raise ValueError(f"no finance rows parsed from {path}")
    return rows


def parse_liquidity_file(path: Path) -> dict[str, ScoreRow]:
    return parse_score_file(path)


def rankdata_average(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda x: x[1])
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


def pearson(x: list[float], y: list[float]) -> float:
    if len(x) < 2:
        return float("nan")
    xa = np.array(x, dtype=float)
    ya = np.array(y, dtype=float)
    if np.std(xa) == 0 or np.std(ya) == 0:
        return float("nan")
    return float(np.corrcoef(xa, ya)[0, 1])


def spearman(x: list[float], y: list[float]) -> float:
    return pearson(rankdata_average(x), rankdata_average(y))


def kendall_tau_b(x: list[float], y: list[float]) -> float:
    n = len(x)
    if n < 2:
        return float("nan")
    c = d = tx = ty = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            sx = 0 if x[i] == x[j] else (1 if x[i] > x[j] else -1)
            sy = 0 if y[i] == y[j] else (1 if y[i] > y[j] else -1)
            if sx == 0 and sy == 0:
                continue
            if sx == 0:
                tx += 1
            elif sy == 0:
                ty += 1
            elif sx == sy:
                c += 1
            else:
                d += 1
    denom = math.sqrt((c + d + tx) * (c + d + ty))
    return (c - d) / denom if denom else float("nan")


def corr_metrics(records: list[dict], score_key: str = "score", return_key: str = "ret_6m") -> dict[str, float]:
    x = [float(r[score_key]) for r in records]
    y = [float(r[return_key]) for r in records]
    return {
        "pearson": pearson(x, y),
        "spearman": spearman(x, y),
        "kendall": kendall_tau_b(x, y),
    }


def mean(values: list[float | None]) -> float:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    return float(np.mean(vals)) if vals else float("nan")


def median(values: list[float | None]) -> float:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    return float(np.median(vals)) if vals else float("nan")


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


def summary_stats(records: list[dict]) -> dict[str, float]:
    return {
        "n": len(records),
        "score_mean": mean([r["score"] for r in records]),
        "ret_mean": mean([r["ret_6m"] for r in records]),
        "ret_median": median([r["ret_6m"] for r in records]),
        "hit_rate": 100.0 * sum(1 for r in records if r["ret_6m"] > 0) / len(records) if records else float("nan"),
    }


def top_bottom_metrics(sorted_records: list[dict], n: int, sort_key: str = "rank") -> dict[str, float]:
    if sort_key == "neutral_percentile":
        ordered = sorted(sorted_records, key=lambda r: (-r["neutral_percentile"], r["rank"]))
        bottom_ordered = sorted(sorted_records, key=lambda r: (r["neutral_percentile"], -r["rank"]))
    else:
        ordered = sorted(sorted_records, key=lambda r: r["rank"])
        bottom_ordered = sorted(sorted_records, key=lambda r: -r["rank"])
    top = ordered[:n]
    bottom = bottom_ordered[:n]
    top_mean = mean([r["ret_6m"] for r in top])
    bottom_mean = mean([r["ret_6m"] for r in bottom])
    top_hit = 100.0 * sum(1 for r in top if r["ret_6m"] > 0) / len(top) if top else float("nan")
    bottom_hit = 100.0 * sum(1 for r in bottom if r["ret_6m"] > 0) / len(bottom) if bottom else float("nan")
    return {
        "top_mean": top_mean,
        "top_hit": top_hit,
        "bottom_mean": bottom_mean,
        "bottom_hit": bottom_hit,
        "spread": top_mean - bottom_mean,
    }


def add_neutral_fields(records: list[dict]) -> None:
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_cat[r["category"]].append(r)
    for cat, group in by_cat.items():
        scores = [r["score"] for r in group]
        ranks = rankdata_average(scores)
        denom = max(len(group) - 1, 1)
        for r, rk in zip(group, ranks):
            r["neutral_percentile"] = (rk - 1) / denom
        score_mean = mean(scores)
        ret_mean = mean([r["ret_6m"] for r in group])
        for r in group:
            r["score_resid"] = r["score"] - score_mean
            r["ret_resid"] = r["ret_6m"] - ret_mean


def compute_risk_group(records: list[dict], label: str, group: list[dict]) -> dict[str, object]:
    window_means = {}
    observations = []
    worst_by_company = []
    dispersion_by_company = []
    beat = 0
    beat_total = 0
    neg = 0
    for r in group:
        vals = []
        for win in ["SOXX下跌1", "SOXX下跌2", "SOXX下跌3"]:
            v = r["stress"].get(win)
            if v is None or math.isnan(v):
                continue
            vals.append(v)
            observations.append(v)
            if v > SOXX_RETURNS[win]:
                beat += 1
            beat_total += 1
            if v < 0:
                neg += 1
        if vals:
            worst_by_company.append(min(vals))
            if len(vals) >= 2:
                dispersion_by_company.append(float(np.std(vals, ddof=0)))
    for win in ["SOXX下跌1", "SOXX下跌2", "SOXX下跌3"]:
        window_means[win] = mean([r["stress"].get(win) for r in group])
    return {
        "label": label,
        "n": len(group),
        "obs": beat_total,
        "w1": window_means["SOXX下跌1"],
        "w2": window_means["SOXX下跌2"],
        "w3": window_means["SOXX下跌3"],
        "pressure_mean": mean(observations),
        "worst_mean": mean(worst_by_company),
        "dispersion": mean(dispersion_by_company),
        "beat_soxx": 100.0 * beat / beat_total if beat_total else float("nan"),
        "neg_rate": 100.0 * neg / beat_total if beat_total else float("nan"),
    }


def compute_iv_group(label: str, group: list[dict]) -> dict[str, object]:
    call_vals = [r["finance"].call_iv for r in group if r["finance"] and r["finance"].call_iv is not None]
    put_vals = [r["finance"].put_iv for r in group if r["finance"] and r["finance"].put_iv is not None]
    near_vals = []
    for r in group:
        f = r["finance"]
        if not f:
            continue
        vals = [v for v in [f.call_iv, f.put_iv] if v is not None]
        if vals:
            near_vals.append(float(np.mean(vals)))
    return {
        "label": label,
        "n": len(group),
        "iv_coverage": len(near_vals),
        "call_mean": mean(call_vals),
        "put_mean": mean(put_vals),
        "near_mean": mean(near_vals),
        "near_median": median(near_vals),
    }


def finance_clean(f: FinanceRow | None) -> bool:
    if f is None:
        return False
    is_adr = "ADR" in f.listing_type.upper() or "ADS" in f.listing_type.upper()
    same_currency = f.currency and f.financial_currency and f.currency == f.financial_currency
    no_currency_mismatch = "currency_mismatch" not in f.valuation_check and "交易货币/财报货币不一致" not in f.note
    return (not is_adr) and same_currency and no_currency_mismatch


def build_records(
    scores: dict[str, ScoreRow],
    returns: dict[str, ReturnRow],
    stress: dict[str, dict[str, float | None]],
    finance: dict[str, FinanceRow],
    liquidity: dict[str, ScoreRow],
) -> list[dict]:
    records = []
    for ticker, s in scores.items():
        if ticker not in returns:
            continue
        rr = returns[ticker]
        records.append(
            {
                "ticker": ticker,
                "name": s.name,
                "category": s.category,
                "score": s.score,
                "rank": s.rank,
                "evidence_grade": s.evidence_grade,
                "confidence": s.confidence,
                "ret_6m": rr.ret_6m,
                "base_date_6m": rr.base_date_6m,
                "stress": stress.get(ticker, {}),
                "finance": finance.get(ticker),
                "liq_score": liquidity[ticker].score if ticker in liquidity else float("nan"),
            }
        )
    add_neutral_fields(records)
    return records


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


def list_tickers(records: list[dict]) -> str:
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
    for p in existing:
        target = dest_dir / p.name
        shutil.move(str(p), str(target))
        moved.append(p.name)
    return f"写入前已移动同类旧版正式输出 {len(moved)} 个到 `{dest_dir.relative_to(ROOT)}`：{', '.join(moved)}。"


def make_report() -> str:
    scores = parse_score_file(SCORE_PATH)
    returns, stress = parse_return_file(RETURN_PATH)
    finance = parse_finance_file(FINANCE_PATH)
    liquidity = parse_liquidity_file(LIQ_PATH)
    records = build_records(scores, returns, stress, finance, liquidity)
    records_by_rank = sorted(records, key=lambda r: r["rank"])
    records_by_return = sorted(records, key=lambda r: r["ret_6m"], reverse=True)

    metrics = corr_metrics(records)
    neutral_percentile_metrics = corr_metrics(records, "neutral_percentile", "ret_6m")
    residual_metrics = corr_metrics(records, "score_resid", "ret_resid")

    q_groups = np.array_split(np.array(records_by_rank, dtype=object), 5)
    quintile_rows = []
    for i, arr in enumerate(q_groups, 1):
        group = list(arr)
        label = f"Q{i}{'最高分' if i == 1 else ('最低分' if i == 5 else '')}"
        st = summary_stats(group)
        quintile_rows.append(
            [
                label,
                st["n"],
                f"{st['score_mean']:.2f}",
                fmt_pct(st["ret_mean"]),
                fmt_pct(st["ret_median"]),
                fmt_rate(st["hit_rate"]),
            ]
        )

    tb_rows = []
    tb_values = {}
    for n in [10, 20, 30]:
        m = top_bottom_metrics(records, n)
        tb_values[n] = m
        tb_rows.append(
            [
                f"Top{n}/Bottom{n}",
                fmt_pct(m["top_mean"]),
                fmt_rate(m["top_hit"]),
                fmt_pct(m["bottom_mean"]),
                fmt_rate(m["bottom_hit"]),
                fmt_pct(m["spread"]),
            ]
        )

    neutral_tb_rows = []
    for n in [10, 20, 30]:
        m = top_bottom_metrics(records, n, "neutral_percentile")
        neutral_tb_rows.append(
            [
                f"中性Top{n}/Bottom{n}",
                fmt_pct(m["top_mean"]),
                fmt_rate(m["top_hit"]),
                fmt_pct(m["bottom_mean"]),
                fmt_rate(m["bottom_hit"]),
                fmt_pct(m["spread"]),
            ]
        )

    top30 = records_by_rank[:30]
    mid_start = max((len(records_by_rank) - 30) // 2, 0)
    mid30 = records_by_rank[mid_start : mid_start + 30]
    bottom30 = list(reversed(records_by_rank[-30:]))
    risk_rows = []
    iv_rows = []
    for label, group in [(f"{FEATURE_ID} Top30", top30), (f"{FEATURE_ID} Mid30", mid30), (f"{FEATURE_ID} Bottom30", bottom30)]:
        rg = compute_risk_group(records, label, group)
        risk_rows.append(
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
        ivg = compute_iv_group(label, group)
        iv_rows.append(
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

    cat_rows = []
    cat_corr_rows = []
    by_cat = defaultdict(list)
    for r in records:
        by_cat[r["category"]].append(r)
    for cat, group in sorted(by_cat.items(), key=lambda kv: kv[0]):
        st = summary_stats(group)
        cm = corr_metrics(group)
        top_ret = max(group, key=lambda r: r["ret_6m"])
        top_score = min(group, key=lambda r: r["rank"])
        cat_rows.append(
            [
                cat,
                st["n"],
                f"{st['score_mean']:.2f}",
                fmt_pct(st["ret_mean"]),
                fmt_pct(st["ret_median"]),
            ]
        )
        cat_corr_rows.append(
            [
                cat,
                len(group),
                fmt_num(cm["pearson"]),
                fmt_num(cm["spearman"]),
                fmt_pct(st["ret_mean"]),
                f"{top_ret['ticker']} {fmt_pct(top_ret['ret_6m'])}",
                f"{top_score['ticker']} {top_score['score']:.1f} / {fmt_pct(top_score['ret_6m'])}",
            ]
        )

    low_liq_removed = [r for r in records if not (r["liq_score"] > 5.0)]
    no_low_liq = [r for r in records if r["liq_score"] > 5.0]
    adr_removed = [r for r in records if not finance_clean(r["finance"])]
    no_adr = [r for r in records if finance_clean(r["finance"])]
    rets = np.array([r["ret_6m"] for r in records], dtype=float)
    low_q = float(np.quantile(rets, 0.05))
    high_q = float(np.quantile(rets, 0.95))
    extreme_removed = [r for r in records if r["ret_6m"] < low_q or r["ret_6m"] > high_q]
    no_extreme = [r for r in records if low_q <= r["ret_6m"] <= high_q]
    combined = [r for r in records if r["liq_score"] > 5.0 and finance_clean(r["finance"]) and low_q <= r["ret_6m"] <= high_q]

    robust_specs = [
        ("全样本基准", "无剔除", records, []),
        ("剔除低流动性", "F51交易流动性分 > 5.0", no_low_liq, low_liq_removed),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", no_adr, adr_removed),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(low_q)} / {fmt_pct(high_q)}", no_extreme, extreme_removed),
        ("三项合并剔除", "同时满足上述三项", combined, [r for r in records if r not in combined]),
    ]
    robust_rows = []
    for label, rule, subset, removed in robust_specs:
        cm = corr_metrics(subset) if len(subset) >= 3 else {"pearson": float("nan"), "spearman": float("nan"), "kendall": float("nan")}
        tb = top_bottom_metrics(subset, min(30, len(subset) // 2)) if len(subset) >= 2 else {}
        robust_rows.append(
            [
                label,
                rule,
                len(subset),
                len(removed),
                fmt_num(cm["pearson"]),
                fmt_num(cm["spearman"]),
                fmt_num(cm["kendall"]),
                fmt_pct(tb.get("top_mean", float("nan"))),
                fmt_pct(tb.get("bottom_mean", float("nan"))),
                fmt_pct(tb.get("spread", float("nan"))),
            ]
        )

    missing_scores = sorted(set(scores) - set(returns))
    extra_returns = sorted(set(returns) - set(scores))

    top10 = records_by_rank[:10]
    bottom10 = list(reversed(records_by_rank[-10:]))
    top_bottom_comp_rows = []
    for label, group in [("Top10", top10), ("Bottom10", bottom10)]:
        for r in group:
            top_bottom_comp_rows.append(
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

    return_diag_rows = []
    for r in records_by_return[:15]:
        return_diag_rows.append(
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
    bottom_return_diag_rows = []
    for r in sorted(records, key=lambda r: r["ret_6m"])[:15]:
        bottom_return_diag_rows.append(
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

    top_score_rows = []
    for r in top30:
        top_score_rows.append(
            [
                r["rank"],
                r["ticker"],
                md_escape(r["name"]),
                r["category"],
                f"{r['score']:.1f}",
                fmt_pct(r["ret_6m"]),
                r["confidence"],
            ]
        )

    backup_note = backup_existing_outputs()

    score_date_match = re.search(r"评分日期：(\d{4}-\d{2}-\d{2})", read_text(SCORE_PATH))
    score_date = score_date_match.group(1) if score_date_match else RUN_DATE
    score_count_match = re.search(r"公司数量：(\d+)", read_text(SCORE_PATH))
    score_count = score_count_match.group(1) if score_count_match else str(len(scores))

    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 6个月涨跌 {RUN_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.append(f"- 评估对象：`{FEATURE_SUBJECT}`。")
    score_rel = SCORE_PATH.relative_to(ROOT).as_posix()
    lines.append(f"- 评分输入：`{score_rel}`，评分日期 {score_date}，覆盖 {score_count} 家。")
    lines.append("- 收益输入：`日度资料/区间涨跌/公司股价区间涨跌幅_2026-05-27.md`，生成时间 2026-05-27 20:17:54 -0700（本机时区），价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。")
    lines.append("- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。")
    lines.append("- 稳健性辅助输入：`特征量化/量化评分/F51_交易流动性_量化评分_2026-06-04.md`；`日度资料/每日金融数据/每日金融数据_2026-06-03.md`，金融数据生成时间 2026-06-03 13:41:46 PDT-0700。")
    lines.append(f"- 有效评估样本：评分与6个月涨跌交集 {len(records)} 家；F39评分有但6个月涨跌缺失 {len(missing_scores)} 家。")
    lines.append("- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。")
    lines.append("- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动率或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为下跌窗口代理，并用2026-06-03近ATM Call/Put IV均值补充当前波动代理。")
    lines.append("- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。")
    lines.append("- 时间方向限制：F39评分日期为2026-06-04，6个月收益窗口截至2026-05-27，本报告是“当前催化剂评分 vs 过去6个月收益”的横截面对照，不是严格样本外预测回测。")
    lines.append("- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F39 正式输出；本次未读取旧版 F39 特征评估作为结论依据。")
    lines.append(f"- {backup_note}")
    lines.append("")

    top30_spread = tb_values[30]["spread"]
    lines.append("## 结论摘要")
    lines.append(f"- 排序有效性：{describe_strength(metrics['spearman'])}。全样本 Pearson {fmt_num(metrics['pearson'])}, Spearman {fmt_num(metrics['spearman'])}, Kendall {fmt_num(metrics['kendall'])}；重点指标 Spearman {fmt_num(metrics['spearman'])}，说明 F39 对本次过去6个月收益排序的单因子解释力{describe_strength(metrics['spearman'])}。")
    lines.append(f"- Top/Bottom能力：Top10、Top20、Top30 平均收益分别为 {fmt_pct(tb_values[10]['top_mean'])}、{fmt_pct(tb_values[20]['top_mean'])}、{fmt_pct(tb_values[30]['top_mean'])}；Top-Bottom收益差分别为 {fmt_pct(tb_values[10]['spread'])}、{fmt_pct(tb_values[20]['spread'])}、{fmt_pct(tb_values[30]['spread'])}。")
    lines.append(f"- 风险解释力：Top30 压力窗口均值 {fmt_pct(compute_risk_group(records, 'tmp', top30)['pressure_mean'])}，Bottom30 为 {fmt_pct(compute_risk_group(records, 'tmp', bottom30)['pressure_mean'])}；Top30 平均最差窗口 {fmt_pct(compute_risk_group(records, 'tmp', top30)['worst_mean'])}，Bottom30 为 {fmt_pct(compute_risk_group(records, 'tmp', bottom30)['worst_mean'])}；Top30 近ATM IV均值 {fmt_pct(compute_iv_group('tmp', top30)['near_mean'])}，Bottom30 为 {fmt_pct(compute_iv_group('tmp', bottom30)['near_mean'])}。")
    lines.append(f"- 分类中性：分类内百分位合并 Spearman {fmt_num(neutral_percentile_metrics['spearman'])}，分类去均值残差 Spearman {fmt_num(residual_metrics['spearman'])}；若分类中性后仍弱或转负，说明 F39 当前更像行业/风格暴露和中期催化提前定价的混合指标，而不是稳定跨行业收益排序因子。")
    lines.append(f"- 稳健性：三项合并剔除后样本 {len(combined)} 家，Spearman {fmt_num(corr_metrics(combined)['spearman'])}，Top30-Bottom30 {fmt_pct(top_bottom_metrics(combined, min(30, len(combined)//2))['spread'])}；剔除低流动性、ADR/币种异常和极端涨跌后，结论以该行作为稳健性主判断。")
    lines.append("- 解释：F39衡量未来6-12个月规模量产、run-rate上移、利润率扩张、AI占比提升或估值框架重写催化的强度。用过去6个月收益做对照时，高分端会同时包含已经被市场提前交易的强催化公司和仍未兑现的高预期公司；低分端则可能包含低基数反弹、小盘题材扩散和周期修复公司。因此本报告更适合检验“中期催化剂强度是否与已发生行情共振”，不宜直接等同于未来6-12个月预测能力。")
    lines.append("")

    lines.append("## 覆盖检查")
    lines.append(
        table(
            ["项目", "数量", "说明"],
            [
                ["F39评分覆盖", len(scores), "来自2026-06-04评分文件"],
                ["6个月涨跌覆盖", len(returns), "来自2026-05-27区间涨跌文件"],
                ["交集样本", len(records), "用于本次所有主指标"],
                ["评分有但6个月涨跌缺失", len(missing_scores), list_tickers([{"ticker": t} for t in missing_scores])],
                ["涨跌有但评分缺失", len(extra_returns), ", ".join(extra_returns) if extra_returns else "无"],
            ],
            ["---", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.append(
        table(
            ["分类目录", "样本数", "F39均分", "6个月平均收益", "6个月中位收益"],
            cat_rows,
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
            ["分组", "公司数", "F39均分", "6个月平均收益", "6个月中位收益", "命中率"],
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
            ["组别", "股票代号", "公司名称", "分类目录", "F39分", "F39排名", "6个月收益", "置信度"],
            top_bottom_comp_rows,
            ["---", "---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")

    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为下跌窗口代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供；近ATM IV为2026-06-03当前期权波动代理，不等同于过去6个月实际波动率。")
    lines.append(
        table(
            ["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"],
            risk_rows,
            ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("### 当前IV代理")
    lines.append(
        table(
            ["分组", "公司数", "IV覆盖", "Call IV均值", "Put IV均值", "近ATM IV均值", "近ATM IV中位数"],
            iv_rows,
            ["---", "---:", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("结论：若高分组压力窗口均值更高、最差窗口更浅且IV更低，说明F39高分公司在回撤期更稳；若高分组IV更高或压力窗口更差，则说明中期催化剂往往伴随提前定价、高估值或项目执行波动，不能自然视为防守特征。")
    lines.append("")

    lines.append("## 分类中性结果")
    lines.append(
        table(
            ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
            [
                ["原始全样本", len(records), fmt_num(metrics["pearson"]), fmt_num(metrics["spearman"]), fmt_num(metrics["kendall"]), "直接用F39分数排序"],
                ["分类内百分位合并", len(records), fmt_num(neutral_percentile_metrics["pearson"]), fmt_num(neutral_percentile_metrics["spearman"]), fmt_num(neutral_percentile_metrics["kendall"]), "每个分类内先按F39排序，再转成0-1百分位后合并"],
                ["分类去均值残差", len(records), fmt_num(residual_metrics["pearson"]), fmt_num(residual_metrics["spearman"]), fmt_num(residual_metrics["kendall"]), "F39和收益分别减去分类均值后相关"],
            ],
            ["---", "---:", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(
        table(
            ["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"],
            neutral_tb_rows,
            ["---", "---:", "---:", "---:", "---:", "---:"],
        )
    )
    lines.append("")
    lines.append("说明：分类中性 Top/Bottom 用于检验 F39 是否只是押中某些强势目录。若分类内百分位和去均值残差仍为正，说明同目录内催化剂排序有额外信息；若转弱或转负，则原始结果更多来自分类暴露、极端公司或窗口风格。")
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(
        table(
            ["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F39公司"],
            cat_corr_rows,
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
    lines.append("稳健性结论：低流动性、ADR/币种异常和极端涨跌剔除后，重点看 Spearman 和 Top30-Bottom30 是否同向保持。若三项合并剔除后仍能保持正向，说明 F39 至少有弱排序价值；若转负或接近0，则更适合作为中期催化监控/组合约束，而不是独立收益排序因子。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(
        table(
            ["剔除项", "数量", "公司"],
            [
                ["低流动性", len(low_liq_removed), list_tickers(low_liq_removed)],
                ["ADR/币种异常", len(adr_removed), list_tickers(adr_removed)],
                ["极端涨跌双尾5%", len(extreme_removed), list_tickers(extreme_removed)],
            ],
            ["---", "---:", "---"],
        )
    )
    lines.append("")

    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    lines.append(
        table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F39分", "F39排名", "F39置信度"],
            return_diag_rows,
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### 6个月跌幅前15")
    lines.append(
        table(
            ["股票代号", "公司名称", "分类目录", "6个月收益", "F39分", "F39排名", "F39置信度"],
            bottom_return_diag_rows,
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
    )
    lines.append("")
    lines.append("### F39 Top30收益明细")
    lines.append(
        table(
            ["F39排名", "股票代号", "公司名称", "分类目录", "F39分", "6个月收益", "置信度"],
            top_score_rows,
            ["---:", "---", "---", "---", "---:", "---:", "---"],
        )
    )
    lines.append("")

    lines.append("## 结论与使用建议")
    lines.append(f"- 主结论：F39在本次过去6个月横截面对照中的 Spearman 为 {fmt_num(metrics['spearman'])}，Top30-Bottom30 为 {fmt_pct(top30_spread)}；应把这两个指标作为本报告的核心读数。")
    lines.append("- 若用于后续模型：F39更适合作为中期催化剂排序特征，与价格相对强度、估值赔率、流动性、预期差和行业中性约束共同使用，不宜单独作为6个月收益排序因子。")
    lines.append("- 若用于研究流程：高分但过去6个月收益弱的公司，需要检查催化剂是否尚未兑现、是否被估值/IV提前反映、或是否存在执行/监管/融资风险；低分但涨幅极高的公司，则应单独标记为低基数反弹、题材扩散或小盘高贝塔。")
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

