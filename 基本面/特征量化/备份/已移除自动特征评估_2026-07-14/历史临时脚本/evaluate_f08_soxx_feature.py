from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path
from statistics import mean, median, pstdev


ROOT = Path(r"D:\drive\Investment\基本面")
DATE = "2026-06-04"
FEATURE_ID = "F08"
FEATURE_NAME = "财务承压可控性"
FEATURE_KEY = f"{FEATURE_ID}_{FEATURE_NAME}"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_KEY}_量化评分_{DATE}.md"
LIQ_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md"
FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_PATH = ROOT / "特征量化" / "特征评估" / f"{FEATURE_KEY}_特征评估_三段SOXX下跌区间涨跌_{DATE}.md"

SOXX_CUMULATIVE = -62.20
SOXX_WINDOWS = {
    "w1": ("SOXX下跌1：2025-02-20至2025-04-08", -32.98),
    "w2": ("SOXX下跌2：2026-02-25至2026-03-30", -15.82),
    "w3": ("SOXX下跌3：2025-10-29至2025-11-20", -13.40),
}


def split_md_row(line: str) -> list[str] | None:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    return [part.strip() for part in s.strip("|").split("|")]


def is_sep_row(parts: list[str]) -> bool:
    return bool(parts) and all(re.fullmatch(r":?-{3,}:?", p.strip()) for p in parts if p.strip())


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).replace("<br>", " / ")).strip()


def md_escape(value: object) -> str:
    return clean(value).replace("|", "\\|")


def parse_pct(cell: str) -> float | None:
    if not cell or "N/A" in cell or "缺失" in cell or "不适用" in cell:
        return None
    m = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%", cell.replace(",", ""))
    return float(m.group(1)) if m else None


def parse_float(cell: str) -> float | None:
    s = clean(cell).replace(",", "")
    if not s or s in {"N/A", "缺失", "不适用"}:
        return None
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{digits}f}%"


def fmt_num(value: float | None, digits: int = 3) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    return f"{value:.{digits}f}"


def fmt_score(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.1f}"


def md_table(headers: list[str], rows: list[list[object]], aligns: list[str] | None = None) -> str:
    if aligns is None:
        aligns = ["---"] * len(headers)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(aligns) + " |"]
    for row in rows:
        out.append("| " + " | ".join(md_escape(v) for v in row) + " |")
    return "\n".join(out)


def rankdata(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda x: x[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = avg
        i = j
    return ranks


def pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) < 2:
        return None
    mx, my = mean(x), mean(y)
    sx = math.sqrt(sum((v - mx) ** 2 for v in x))
    sy = math.sqrt(sum((v - my) ** 2 for v in y))
    if sx == 0 or sy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def spearman(x: list[float], y: list[float]) -> float | None:
    return pearson(rankdata(x), rankdata(y))


def kendall_tau_b(x: list[float], y: list[float]) -> float | None:
    if len(x) < 2:
        return None
    c = d = tx = ty = 0
    for i in range(len(x) - 1):
        for j in range(i + 1, len(x)):
            dx = (x[i] > x[j]) - (x[i] < x[j])
            dy = (y[i] > y[j]) - (y[i] < y[j])
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
    return None if denom == 0 else (c - d) / denom


def corr(rows: list[dict], target: str = "cum", score_key: str = "score") -> dict[str, float | None]:
    valid = [r for r in rows if r.get(score_key) is not None and r.get(target) is not None]
    x = [float(r[score_key]) for r in valid]
    y = [float(r[target]) for r in valid]
    return {"pearson": pearson(x, y), "spearman": spearman(x, y), "kendall": kendall_tau_b(x, y)}


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("empty quantile input")
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def parse_score_file(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = split_md_row(line)
        if parts and parts[:7] == ["排名", "股票代号", "公司名称", "分类目录", "特征分", "证据等级", "置信度"]:
            in_table = True
            continue
        if not in_table:
            continue
        if parts is None:
            if rows:
                break
            continue
        if is_sep_row(parts):
            continue
        if len(parts) < 7 or not re.fullmatch(r"\d+", parts[0]):
            continue
        ticker = parts[1]
        rows[ticker] = {
            "rank": int(parts[0]),
            "ticker": ticker,
            "name": parts[2],
            "category": parts[3],
            "score": float(parts[4]),
            "evidence": parts[5],
            "confidence": parts[6],
        }
    return rows


def parse_soxx_returns(path: Path) -> tuple[dict[str, dict], dict[str, str]]:
    rows: dict[str, dict] = {}
    meta: dict[str, str] = {}
    in_details = False
    current_category = ""
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("- 生成时间："):
            meta["generated"] = s.replace("- 生成时间：", "").strip().rstrip("。")
        if s.startswith("- 价格口径："):
            meta["price_basis"] = s.replace("- 价格口径：", "").strip().rstrip("。")
        if s.startswith("- 累计计算："):
            meta["cum_basis"] = s.replace("- 累计计算：", "").strip().rstrip("。")
        if s == "## 全公司明细":
            in_details = True
            continue
        if in_details and s.startswith("## "):
            break
        if not in_details:
            continue
        if s.startswith("### "):
            current_category = s[4:].strip()
            in_table = False
            continue
        parts = split_md_row(line)
        if parts and parts[:2] == ["股票代号", "公司名称"] and "SOXX下跌1" in parts[2]:
            in_table = True
            continue
        if not in_table:
            continue
        if parts is None:
            in_table = False
            continue
        if is_sep_row(parts):
            continue
        if len(parts) < 7:
            continue
        rows[parts[0]] = {
            "ticker": parts[0],
            "name": parts[1],
            "category": current_category,
            "w1": parse_pct(parts[2]),
            "w2": parse_pct(parts[3]),
            "w3": parse_pct(parts[4]),
            "cum": parse_pct(parts[5]),
            "note": clean(parts[6]),
        }
    return rows, meta


def parse_financial(path: Path) -> tuple[dict[str, dict], str]:
    rows: dict[str, dict] = {}
    generated = ""
    current_category = ""
    header: list[str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("- 生成时间：") and not generated:
            generated = s.replace("- 生成时间：", "").strip()
        if s.startswith("### "):
            current_category = s[4:].strip()
            header = None
            continue
        parts = split_md_row(line)
        if parts is None:
            continue
        if is_sep_row(parts):
            continue
        if parts and parts[0] == "股票代号":
            header = parts
            continue
        if not header or len(parts) != len(header):
            continue
        row = dict(zip(header, parts))
        ticker = row.get("股票代号", "")
        if not ticker:
            continue
        rows[ticker] = {
            "ticker": ticker,
            "financial_category": current_category,
            "price_date": row.get("价格日期", ""),
            "currency": row.get("currency", ""),
            "financial_currency": row.get("financial_currency", ""),
            "listing_type": row.get("listing_type", ""),
            "adr_ratio": row.get("adr_ratio", ""),
            "valuation_check": row.get("估值校验", ""),
            "note": row.get("备注", ""),
            "call_iv": parse_pct(row.get("Call IV", "")),
            "put_iv": parse_pct(row.get("Put IV", "")),
        }
    return rows, generated


def build_rows(score: dict[str, dict], returns: dict[str, dict], liq: dict[str, dict], fin: dict[str, dict]) -> list[dict]:
    rows: list[dict] = []
    for ticker, s in score.items():
        r = returns.get(ticker)
        if not r or r.get("cum") is None:
            continue
        f = fin.get(ticker, {})
        l = liq.get(ticker, {})
        call_iv = f.get("call_iv")
        put_iv = f.get("put_iv")
        near_iv = mean([v for v in [call_iv, put_iv] if v is not None]) if call_iv is not None or put_iv is not None else None
        rows.append(
            {
                **s,
                "return_name": r["name"],
                "return_category": r["category"],
                "w1": r["w1"],
                "w2": r["w2"],
                "w3": r["w3"],
                "cum": r["cum"],
                "return_note": r["note"],
                "liquidity_score": l.get("score"),
                "call_iv": call_iv,
                "put_iv": put_iv,
                "near_iv": near_iv,
                "listing_type": f.get("listing_type", ""),
                "adr_ratio": f.get("adr_ratio", ""),
                "currency": f.get("currency", ""),
                "financial_currency": f.get("financial_currency", ""),
                "valuation_check": f.get("valuation_check", ""),
                "financial_note": f.get("note", ""),
            }
        )
    return rows


def ordered_rows(rows: list[dict], neutral: bool = False) -> list[dict]:
    key = "neutral_pct" if neutral else "score"
    return sorted(rows, key=lambda r: (-float(r[key]), int(r["rank"])))


def top_bottom(rows: list[dict], n: int, neutral: bool = False) -> dict[str, float | list[dict]]:
    ordered = ordered_rows(rows, neutral=neutral)
    top = ordered[:n]
    bottom = ordered[-n:]
    return {
        "top_rows": top,
        "bottom_rows": bottom,
        "top_avg": mean(r["cum"] for r in top),
        "top_med": median(r["cum"] for r in top),
        "top_hit": mean(1.0 if r["cum"] > SOXX_CUMULATIVE else 0.0 for r in top) * 100,
        "top_pos": mean(1.0 if r["cum"] > 0 else 0.0 for r in top) * 100,
        "bottom_avg": mean(r["cum"] for r in bottom),
        "bottom_med": median(r["cum"] for r in bottom),
        "bottom_hit": mean(1.0 if r["cum"] > SOXX_CUMULATIVE else 0.0 for r in bottom) * 100,
        "bottom_pos": mean(1.0 if r["cum"] > 0 else 0.0 for r in bottom) * 100,
        "diff": mean(r["cum"] for r in top) - mean(r["cum"] for r in bottom),
        "hit_diff": (mean(1.0 if r["cum"] > SOXX_CUMULATIVE else 0.0 for r in top) - mean(1.0 if r["cum"] > SOXX_CUMULATIVE else 0.0 for r in bottom)) * 100,
    }


def group_risk(name: str, group_rows: list[dict]) -> dict[str, object]:
    obs = []
    worst = []
    dispersion = []
    beat_count = 0
    neg_count = 0
    total_windows = 0
    for r in group_rows:
        vals = [r.get("w1"), r.get("w2"), r.get("w3")]
        pairs = [(key, val) for key, val in zip(["w1", "w2", "w3"], vals) if val is not None]
        if not pairs:
            continue
        only_vals = [val for _, val in pairs]
        obs.extend(only_vals)
        worst.append(min(only_vals))
        dispersion.append(pstdev(only_vals) if len(only_vals) > 1 else 0.0)
        for key, val in pairs:
            total_windows += 1
            if val > SOXX_WINDOWS[key][1]:
                beat_count += 1
            if val < 0:
                neg_count += 1
    return {
        "name": name,
        "n": len(group_rows),
        "obs": len(obs),
        "w1": mean([r["w1"] for r in group_rows if r.get("w1") is not None]),
        "w2": mean([r["w2"] for r in group_rows if r.get("w2") is not None]),
        "w3": mean([r["w3"] for r in group_rows if r.get("w3") is not None]),
        "cum": mean(r["cum"] for r in group_rows),
        "pressure": mean(obs),
        "worst": mean(worst),
        "dispersion": mean(dispersion),
        "beat_windows": beat_count / total_windows * 100 if total_windows else None,
        "beat_cum": mean(1.0 if r["cum"] > SOXX_CUMULATIVE else 0.0 for r in group_rows) * 100,
        "negative": neg_count / total_windows * 100 if total_windows else None,
        "iv_avg": mean([r["near_iv"] for r in group_rows if r.get("near_iv") is not None]) if any(r.get("near_iv") is not None for r in group_rows) else None,
        "iv_med": median([r["near_iv"] for r in group_rows if r.get("near_iv") is not None]) if any(r.get("near_iv") is not None for r in group_rows) else None,
        "iv_n": len([r for r in group_rows if r.get("near_iv") is not None]),
    }


def add_neutral_fields(rows: list[dict]) -> None:
    by_cat: dict[str, list[dict]] = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)
    for group in by_cat.values():
        score_ranks = rankdata([r["score"] for r in group])
        denom = len(group) - 1
        for r, rk in zip(group, score_ranks):
            r["neutral_pct"] = 1.0 if denom <= 0 else (rk - 1) / denom
            r["score_resid"] = r["score"] - mean(x["score"] for x in group)
            r["cum_resid"] = r["cum"] - mean(x["cum"] for x in group)


def category_rows(rows: list[dict]) -> list[list[object]]:
    out = []
    categories = []
    seen = set()
    for r in rows:
        if r["category"] not in seen:
            categories.append(r["category"])
            seen.add(r["category"])
    for cat in categories:
        g = [r for r in rows if r["category"] == cat]
        out.append([
            cat,
            len(g),
            fmt_score(mean(r["score"] for r in g)),
            fmt_pct(mean(r["cum"] for r in g)),
            fmt_pct(median(r["cum"] for r in g)),
            fmt_pct(mean(1.0 if r["cum"] > SOXX_CUMULATIVE else 0.0 for r in g) * 100, 1),
        ])
    return out


def quintile_rows(rows: list[dict]) -> list[list[object]]:
    ordered = ordered_rows(rows)
    groups = []
    n = len(ordered)
    labels = ["Q1最高分", "Q2", "Q3", "Q4", "Q5最低分"]
    for i, label in enumerate(labels):
        start = round(i * n / 5)
        end = round((i + 1) * n / 5)
        g = ordered[start:end]
        groups.append([
            label,
            len(g),
            fmt_score(mean(r["score"] for r in g)),
            fmt_pct(mean(r["cum"] for r in g)),
            fmt_pct(median(r["cum"] for r in g)),
            fmt_pct(mean(1.0 if r["cum"] > SOXX_CUMULATIVE else 0.0 for r in g) * 100, 1),
            fmt_pct(mean(min(r["w1"], r["w2"], r["w3"]) for r in g if None not in [r["w1"], r["w2"], r["w3"]])),
            fmt_pct(mean([r["near_iv"] for r in g if r.get("near_iv") is not None]) if any(r.get("near_iv") is not None for r in g) else None),
        ])
    return groups


def category_corr_rows(rows: list[dict]) -> list[list[object]]:
    out = []
    categories = []
    seen = set()
    for r in rows:
        if r["category"] not in seen:
            categories.append(r["category"])
            seen.add(r["category"])
    for cat in categories:
        g = [r for r in rows if r["category"] == cat]
        c = corr(g)
        best = sorted(g, key=lambda r: r["cum"], reverse=True)[0]
        worst = sorted(g, key=lambda r: r["cum"])[0]
        top_score = ordered_rows(g)[0]
        out.append([
            cat,
            len(g),
            fmt_num(c["pearson"]),
            fmt_num(c["spearman"]),
            fmt_num(c["kendall"]),
            fmt_pct(mean(r["cum"] for r in g)),
            fmt_pct(mean(1.0 if r["cum"] > SOXX_CUMULATIVE else 0.0 for r in g) * 100, 1),
            f"{best['ticker']} {fmt_pct(best['cum'])}",
            f"{worst['ticker']} {fmt_pct(worst['cum'])}",
            f"{top_score['ticker']} {fmt_score(top_score['score'])} / {fmt_pct(top_score['cum'])}",
        ])
    return out


def sample_robustness(label: str, rule: str, rows: list[dict], keep_mask: list[bool]) -> dict[str, object]:
    kept = [r for r, keep in zip(rows, keep_mask) if keep]
    c = corr(kept)
    tb = top_bottom(kept, 30)
    return {
        "label": label,
        "rule": rule,
        "n": len(kept),
        "excluded": len(rows) - len(kept),
        "corr": c,
        "tb": tb,
    }


def company_list(rows: list[dict] | list[str]) -> str:
    if not rows:
        return "无"
    if isinstance(rows[0], str):
        return ", ".join(sorted(rows))
    return ", ".join(sorted(r["ticker"] for r in rows))


def row_diag(r: dict, score_label: str = "F08分") -> list[object]:
    return [r["ticker"], r["name"], r["category"], fmt_pct(r["cum"]), fmt_pct(r["w1"]), fmt_pct(r["w2"]), fmt_pct(r["w3"]), fmt_score(r["score"]), r["rank"], r["confidence"]]


def make_report() -> tuple[str, dict[str, object]]:
    score = parse_score_file(SCORE_PATH)
    liq = parse_score_file(LIQ_PATH)
    returns, ret_meta = parse_soxx_returns(RETURN_PATH)
    fin, fin_generated = parse_financial(FIN_PATH)
    rows = build_rows(score, returns, liq, fin)
    add_neutral_fields(rows)
    rows = ordered_rows(rows)

    missing_returns = sorted([t for t in score if t not in returns or returns[t].get("cum") is None])
    missing_scores = sorted([t for t in returns if returns[t].get("cum") is not None and t not in score])

    base_corr = corr(rows)
    window_corrs = {key: corr(rows, key) for key in ["w1", "w2", "w3"]}
    target_corr_rows = [
        ["三段累计涨跌幅", len(rows), fmt_num(base_corr["pearson"]), fmt_num(base_corr["spearman"]), fmt_num(base_corr["kendall"]), "核心目标；三个SOXX下跌区间百分比简单相加"],
        [SOXX_WINDOWS["w1"][0], len([r for r in rows if r["w1"] is not None]), fmt_num(window_corrs["w1"]["pearson"]), fmt_num(window_corrs["w1"]["spearman"]), fmt_num(window_corrs["w1"]["kendall"]), "最大压力窗口，SOXX -32.98%"],
        [SOXX_WINDOWS["w2"][0], len([r for r in rows if r["w2"] is not None]), fmt_num(window_corrs["w2"]["pearson"]), fmt_num(window_corrs["w2"]["spearman"]), fmt_num(window_corrs["w2"]["kendall"]), "第二段压力窗口，SOXX -15.82%"],
        [SOXX_WINDOWS["w3"][0], len([r for r in rows if r["w3"] is not None]), fmt_num(window_corrs["w3"]["pearson"]), fmt_num(window_corrs["w3"]["spearman"]), fmt_num(window_corrs["w3"]["kendall"]), "第三段压力窗口，SOXX -13.40%"],
    ]

    tb = {n: top_bottom(rows, n) for n in [10, 20, 30]}
    tb_rows = [
        [f"Top{n}/Bottom{n}", fmt_pct(tb[n]["top_avg"]), fmt_pct(tb[n]["top_med"]), fmt_pct(tb[n]["top_hit"], 1), fmt_pct(tb[n]["top_pos"], 1), fmt_pct(tb[n]["bottom_avg"]), fmt_pct(tb[n]["bottom_med"]), fmt_pct(tb[n]["bottom_hit"], 1), fmt_pct(tb[n]["bottom_pos"], 1), fmt_pct(tb[n]["diff"])]
        for n in [10, 20, 30]
    ]
    tb_company_rows = []
    for r in tb[10]["top_rows"]:
        tb_company_rows.append(["Top10", *row_diag(r)])
    for r in tb[10]["bottom_rows"]:
        tb_company_rows.append(["Bottom10", *row_diag(r)])

    ordered = ordered_rows(rows)
    mid_start = (len(ordered) - 30) // 2
    risk_groups = {
        "F08 Top30": ordered[:30],
        "F08 Mid30": ordered[mid_start:mid_start + 30],
        "F08 Bottom30": ordered[-30:],
    }
    risk = {name: group_risk(name, group) for name, group in risk_groups.items()}
    risk_rows = [
        [
            name,
            m["n"],
            m["obs"],
            fmt_pct(m["w1"]),
            fmt_pct(m["w2"]),
            fmt_pct(m["w3"]),
            fmt_pct(m["cum"]),
            fmt_pct(m["pressure"]),
            fmt_pct(m["worst"]),
            fmt_pct(m["dispersion"]),
            fmt_pct(m["beat_windows"], 1),
            fmt_pct(m["beat_cum"], 1),
            fmt_pct(m["negative"], 1),
            fmt_pct(m["iv_avg"]),
            m["iv_n"],
        ]
        for name, m in risk.items()
    ]

    neutral_pct_corr = corr(rows, "cum", "neutral_pct")
    neutral_resid_corr = corr(rows, "cum_resid", "score_resid")
    neutral_tb = {n: top_bottom(rows, n, neutral=True) for n in [10, 20, 30]}
    neutral_rows = [
        [f"中性Top{n}/Bottom{n}", fmt_pct(neutral_tb[n]["top_avg"]), fmt_pct(neutral_tb[n]["top_hit"], 1), fmt_pct(neutral_tb[n]["bottom_avg"]), fmt_pct(neutral_tb[n]["bottom_hit"], 1), fmt_pct(neutral_tb[n]["diff"])]
        for n in [10, 20, 30]
    ]

    low_liq_mask = [(r.get("liquidity_score") is None or r.get("liquidity_score") <= 5.0) for r in rows]
    adr_mask = [
        (
            r.get("listing_type", "") != "common/equity"
            or r.get("adr_ratio", "") not in {"", "不适用"}
            or (r.get("currency", "") != r.get("financial_currency", ""))
            or "currency_mismatch" in r.get("valuation_check", "")
            or "ADR/ADS比例需确认" in r.get("financial_note", "")
        )
        for r in rows
    ]
    cum_values = [r["cum"] for r in rows]
    low_q = quantile(cum_values, 0.05)
    high_q = quantile(cum_values, 0.95)
    extreme_mask = [(r["cum"] < low_q or r["cum"] > high_q) for r in rows]
    all_mask = [True] * len(rows)
    robustness = [
        sample_robustness("全样本基准", "无剔除", rows, all_mask),
        sample_robustness("剔除低流动性", "F51交易流动性分 > 5.0", rows, [not x for x in low_liq_mask]),
        sample_robustness("剔除ADR/币种异常", "listing_type=common/equity、ADR比例不适用、交易/财报货币一致、估值校验无currency_mismatch", rows, [not x for x in adr_mask]),
        sample_robustness("剔除极端涨跌", f"剔除三段累计涨跌双尾5%；阈值 {fmt_pct(low_q)} / {fmt_pct(high_q)}", rows, [not x for x in extreme_mask]),
        sample_robustness("三项合并剔除", "同时满足上述三项", rows, [not (a or b or c) for a, b, c in zip(low_liq_mask, adr_mask, extreme_mask)]),
    ]
    robustness_rows = [
        [
            r["label"],
            r["rule"],
            r["n"],
            r["excluded"],
            fmt_num(r["corr"]["pearson"]),
            fmt_num(r["corr"]["spearman"]),
            fmt_num(r["corr"]["kendall"]),
            fmt_pct(r["tb"]["top_avg"]),
            fmt_pct(r["tb"]["bottom_avg"]),
            fmt_pct(r["tb"]["diff"]),
            fmt_pct(r["tb"]["hit_diff"], 1),
        ]
        for r in robustness
    ]

    winners = sorted(rows, key=lambda r: r["cum"], reverse=True)[:15]
    losers = sorted(rows, key=lambda r: r["cum"])[:15]
    top_score15 = ordered[:15]
    bottom_score15 = ordered[-15:]

    high_score_bad = [r for r in ordered[:45] if r["cum"] <= SOXX_CUMULATIVE]
    low_score_good = [r for r in ordered[-45:] if r["cum"] > SOXX_CUMULATIVE]
    high_bad_rows = [[r["ticker"], r["name"], r["category"], fmt_score(r["score"]), r["rank"], fmt_pct(r["cum"]), "高F08代表财务约束可控，但本窗口仍受估值压缩、AI beta、客户/订单节奏或个股事件影响。"] for r in high_score_bad[:12]]
    low_good_rows = [[r["ticker"], r["name"], r["category"], fmt_score(r["score"]), r["rank"], fmt_pct(r["cum"]), "低F08通常代表融资/现金流/营运资本压力，但本窗口可能受公用事业防守、特殊事件、反弹或低beta属性支撑。"] for r in low_score_good[:12]]

    dist_counter: Counter[str] = Counter()
    for r in rows:
        s = r["score"]
        if s >= 9:
            dist_counter["9.0-10.0"] += 1
        elif s >= 7:
            dist_counter["7.0-8.9"] += 1
        elif s >= 5:
            dist_counter["5.0-6.9"] += 1
        elif s >= 3:
            dist_counter["3.0-4.9"] += 1
        else:
            dist_counter["1.0-2.9"] += 1
    dist_rows = [[k, dist_counter[k]] for k in ["9.0-10.0", "7.0-8.9", "5.0-6.9", "3.0-4.9", "1.0-2.9"]]

    spearman_main = base_corr["spearman"]
    if spearman_main is not None and spearman_main >= 0.20:
        sort_eval = "成立，且有中等排序强度"
    elif spearman_main is not None and spearman_main >= 0.10:
        sort_eval = "弱成立"
    elif spearman_main is not None and spearman_main > -0.10:
        sort_eval = "接近无效"
    else:
        sort_eval = "反向或不成立"

    tb_eval = "成立" if tb[30]["diff"] > 5 else ("弱成立" if tb[30]["diff"] > 0 else "不成立")
    risk_eval = "成立" if risk["F08 Top30"]["cum"] > risk["F08 Bottom30"]["cum"] and risk["F08 Top30"]["worst"] > risk["F08 Bottom30"]["worst"] else "不成立"
    neutral_eval = "成立" if neutral_pct_corr["spearman"] is not None and neutral_pct_corr["spearman"] > 0 and neutral_tb[30]["diff"] > 0 else "不成立"
    robust_combined = robustness[-1]
    robust_eval = "成立" if robust_combined["corr"]["spearman"] is not None and robust_combined["corr"]["spearman"] > 0 and robust_combined["tb"]["diff"] > 0 else "不成立"

    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 三段SOXX下跌区间涨跌 {DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.extend([
        f"- 评估对象：`{FEATURE_KEY}`。",
        f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 {DATE}，覆盖 {len(score)} 家。",
        f"- 收益输入：`日度资料/区间涨跌/{RETURN_PATH.name}`，生成时间 {ret_meta.get('generated', 'N/A')}；价格口径为 Yahoo Finance `Close`，`auto_adjust=False`，不含股息再投资。",
        "- SOXX压力窗口：2025-02-20至2025-04-08 下跌 -32.98%；2026-02-25至2026-03-30 下跌 -15.82%；2025-10-29至2025-11-20 下跌 -13.40%。SOXX三段累计涨跌幅为 -62.20%。",
        f"- 稳健性辅助输入：`特征量化/量化评分/{LIQ_PATH.name}`；`日度资料/每日金融数据/{FIN_PATH.name}`，金融数据生成时间 {fin_generated}。",
        f"- 有效评估样本：评分与三段累计涨跌幅交集 {len(rows)} 家；F08评分有但累计涨跌缺失 {len(missing_returns)} 家：{company_list(missing_returns)}。",
        "- 收益方向口径：三段累计涨跌幅越高越好；在压力窗口中，跌幅更小、或上涨，均视为更优表现。",
        "- 命中率口径：三段累计涨跌幅大于 SOXX 三段累计涨跌幅 `-62.20%` 记为压力命中；Top-Bottom收益差=高分组合平均三段累计收益 - 低分组合平均三段累计收益。",
        "- 风险口径限制：本次输入是三个固定压力区间收益，不是逐日收益序列；因此本报告不写成严格日度波动率、完整最大回撤或真实下跌日胜率，而使用三个SOXX下跌窗口均值、平均最差窗口、窗口离散度、跑赢SOXX比例、负收益窗口占比，并用 2026-06-03 近ATM Call/Put IV均值补充当前波动代理。",
        "- 稳健性口径：低流动性使用 `F51<=5.0` 或F51缺失作为剔除代理；ADR/币种异常使用每日金融数据中的 `listing_type`、ADR比例、交易/财报货币和 `currency_mismatch` 标记；极端涨跌按本次三段累计收益双尾5%剔除。",
        "- 本报告是下游特征评估，只读取 `量化评分/`、`特征评估/`、`日度资料/区间涨跌/` 和必要日度金融字段，不把结论反向写入上游资料。",
    ])
    lines.append("")
    lines.append("## 结论摘要")
    lines.extend([
        f"- 排序有效性：{sort_eval}。全样本 Pearson {fmt_num(base_corr['pearson'])}，Spearman {fmt_num(base_corr['spearman'])}，Kendall {fmt_num(base_corr['kendall'])}；重点指标 Spearman 为 {fmt_num(base_corr['spearman'])}。",
        f"- 分窗口观察：SOXX下跌1/2/3 的 Spearman 分别为 {fmt_num(window_corrs['w1']['spearman'])}、{fmt_num(window_corrs['w2']['spearman'])}、{fmt_num(window_corrs['w3']['spearman'])}。若三段方向不一致，应把F08理解为组合风险约束，而不是机械下跌保护因子。",
        f"- Top/Bottom能力：{tb_eval}。Top10/Top20/Top30 平均累计收益分别为 {fmt_pct(tb[10]['top_avg'])}、{fmt_pct(tb[20]['top_avg'])}、{fmt_pct(tb[30]['top_avg'])}；对应Top-Bottom收益差为 {fmt_pct(tb[10]['diff'])}、{fmt_pct(tb[20]['diff'])}、{fmt_pct(tb[30]['diff'])}。",
        f"- 风险解释力：{risk_eval}。F08 Top30 三段累计均值 {fmt_pct(risk['F08 Top30']['cum'])}、平均最差窗口 {fmt_pct(risk['F08 Top30']['worst'])}、跑赢SOXX窗口比例 {fmt_pct(risk['F08 Top30']['beat_windows'], 1)}；Bottom30 对应为 {fmt_pct(risk['F08 Bottom30']['cum'])}、{fmt_pct(risk['F08 Bottom30']['worst'])}、{fmt_pct(risk['F08 Bottom30']['beat_windows'], 1)}。",
        f"- 分类中性：{neutral_eval}。分类内百分位合并 Spearman {fmt_num(neutral_pct_corr['spearman'])}，分类去均值残差 Spearman {fmt_num(neutral_resid_corr['spearman'])}；中性Top30-Bottom30收益差 {fmt_pct(neutral_tb[30]['diff'])}。",
        f"- 稳健性：{robust_eval}。剔除低流动性后 Spearman {fmt_num(robustness[1]['corr']['spearman'])}，剔除ADR/币种异常后 {fmt_num(robustness[2]['corr']['spearman'])}，剔除极端涨跌后 {fmt_num(robustness[3]['corr']['spearman'])}，三项合并后 {fmt_num(robust_combined['corr']['spearman'])}；三项合并后Top30-Bottom30为 {fmt_pct(robust_combined['tb']['diff'])}。",
        "- 解释：F08 衡量现金、债务、FCF、库存和融资压力是否可控。这个特征天然偏“抗融资踩雷/经营韧性”，但三段SOXX下跌窗口仍会受到行业beta、低流动性反弹、ADR口径和极端个股事件干扰；因此最终使用应看排序相关、Top/Bottom和风险代理是否共同同向。",
    ])
    lines.append("")
    lines.append("## 覆盖检查")
    lines.append(md_table(
        ["项目", "数量", "说明"],
        [
            ["F08评分覆盖", len(score), "来自2026-06-04评分文件"],
            ["三段累计涨跌覆盖", len([r for r in returns.values() if r.get("cum") is not None]), "来自2026-06-04三段SOXX下跌区间涨跌文件"],
            ["交集有效样本", len(rows), "用于本报告主指标"],
            ["评分有但累计涨跌缺失", len(missing_returns), company_list(missing_returns)],
            ["涨跌有但评分缺失", len(missing_scores), company_list(missing_scores)],
        ],
        ["---", "---:", "---"],
    ))
    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.append(md_table(["分类目录", "样本数", "F08均分", "三段累计平均", "三段累计中位数", "跑赢SOXX累计率"], category_rows(rows), ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## 排序有效性")
    lines.append(md_table(["目标收益", "样本数", "Pearson", "Spearman", "Kendall tau-b", "解释"], target_corr_rows, ["---", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### F08分数分组收益")
    lines.append(md_table(["分组", "公司数", "F08均分", "三段累计平均", "三段累计中位数", "跑赢SOXX累计率", "平均最差窗口", "当前IV均值"], quintile_rows(rows), ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## Top/Bottom能力")
    lines.append(md_table(["组合", "Top平均累计", "Top中位累计", "Top压力命中率", "Top正收益率", "Bottom平均累计", "Bottom中位累计", "Bottom压力命中率", "Bottom正收益率", "Top-Bottom收益差"], tb_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    lines.append(md_table(["组别", "股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F08分", "F08排名", "置信度"], tb_company_rows, ["---", "---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用三个固定SOXX下跌区间作为压力测试代理。严格日度波动率、完整最大回撤、真实下跌日收益稳定性需要逐日价格序列；当前IV均值仅是 2026-06-03 近ATM期权波动代理，不等同于历史实际波动率。")
    lines.append("")
    lines.append(md_table(["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "三段累计均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX窗口比例", "跑赢SOXX累计率", "负收益窗口占比", "当前IV均值", "IV样本"], risk_rows, ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append(f"结论：F08 Top30 的三段累计均值比 Bottom30 高 {fmt_pct(risk['F08 Top30']['cum'] - risk['F08 Bottom30']['cum'])}，平均最差窗口差值为 {fmt_pct(risk['F08 Top30']['worst'] - risk['F08 Bottom30']['worst'])}，跑赢SOXX窗口比例差值为 {fmt_pct(risk['F08 Top30']['beat_windows'] - risk['F08 Bottom30']['beat_windows'], 1)}。若这些指标同向改善，说明F08确有压力窗口防守含义；若只在少数指标改善，则只能作为风控辅助。")
    lines.append("")
    lines.append("## 分类中性结果")
    lines.append(md_table(
        ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
        [
            ["原始全样本", len(rows), fmt_num(base_corr["pearson"]), fmt_num(base_corr["spearman"]), fmt_num(base_corr["kendall"]), "直接用F08原始分数排序"],
            ["分类内百分位合并", len(rows), fmt_num(neutral_pct_corr["pearson"]), fmt_num(neutral_pct_corr["spearman"]), fmt_num(neutral_pct_corr["kendall"]), "每个分类内先按F08排序，再转为0-1百分位合并"],
            ["分类去均值残差", len(rows), fmt_num(neutral_resid_corr["pearson"]), fmt_num(neutral_resid_corr["spearman"]), fmt_num(neutral_resid_corr["kendall"]), "F08和累计收益分别减去分类均值后相关"],
        ],
        ["---", "---:", "---:", "---:", "---:", "---"],
    ))
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(md_table(["组合", "Top平均累计", "Top压力命中率", "Bottom平均累计", "Bottom压力命中率", "Top-Bottom收益差"], neutral_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(md_table(["分类目录", "样本数", "Pearson", "Spearman", "Kendall", "类内累计均值", "类内命中率", "类内最好", "类内最差", "类内最高F08公司"], category_corr_rows(rows), ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---", "---", "---"]))
    lines.append("")
    lines.append("分类内结果用于检验 F08 是否只是押中了某个分类目录。若分类内百分位合并和分类去均值残差仍为正，说明同一产业目录内财务承压可控性也有额外排序信息；若转弱或转负，则原始读数更可能来自行业配置、beta或极端样本。")
    lines.append("")
    lines.append("## 稳健性检验")
    lines.append(md_table(["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30", "Top-Bottom命中率差"], robustness_rows, ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("稳健性结论：若三项合并剔除后 Spearman 和 Top30-Bottom30仍同向为正，说明 F08 的压力窗口有效性不主要依赖低流动性、ADR/币种口径或极端涨跌；若方向反转，则应降低单因子权重，仅保留风险约束用途。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(md_table(
        ["剔除项", "数量", "公司"],
        [
            ["低流动性", sum(low_liq_mask), company_list([r for r, flag in zip(rows, low_liq_mask) if flag])],
            ["ADR/币种异常", sum(adr_mask), company_list([r for r, flag in zip(rows, adr_mask) if flag])],
            ["极端涨跌双尾5%", sum(extreme_mask), company_list([r for r, flag in zip(rows, extreme_mask) if flag])],
        ],
        ["---", "---:", "---"],
    ))
    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 三段累计表现最好15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F08分", "F08排名", "置信度"], [row_diag(r) for r in winners], ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 三段累计表现最差15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F08分", "F08排名", "置信度"], [row_diag(r) for r in losers], ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### F08高分前15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F08分", "F08排名", "置信度"], [row_diag(r) for r in top_score15], ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### F08低分前15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "三段累计", "SOXX跌1", "SOXX跌2", "SOXX跌3", "F08分", "F08排名", "置信度"], [row_diag(r) for r in bottom_score15], ["---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    lines.append("")
    if high_bad_rows:
        lines.append("### 高F08但压力窗口显著拖累")
        lines.append(md_table(["股票代号", "公司名称", "分类目录", "F08分", "F08排名", "三段累计", "主要提示"], high_bad_rows, ["---", "---", "---", "---:", "---:", "---:", "---"]))
        lines.append("")
    if low_good_rows:
        lines.append("### 低F08但跑赢SOXX累计")
        lines.append(md_table(["股票代号", "公司名称", "分类目录", "F08分", "F08排名", "三段累计", "主要提示"], low_good_rows, ["---", "---", "---", "---:", "---:", "---:", "---"]))
        lines.append("")
    lines.append("## 分数分布")
    lines.append(md_table(["分数区间", "有效样本公司数"], dist_rows, ["---", "---:"]))
    lines.append("")
    lines.append("## 评估结论与使用建议")
    if sort_eval.startswith("成立") and tb_eval == "成立" and robust_eval == "成立":
        lines.extend([
            "- 对“三段SOXX下跌区间累计涨跌幅”这一目标，F08_财务承压可控性可以作为正向压力窗口排序因子；核心 Spearman、Top/Bottom、分类中性和稳健性均支持高分更抗跌。",
            "- 组合使用上，F08 可作为下跌窗口防守权重或融资风险过滤器；它不替代 F50价格相对强度、估值赔率、订单确认性和催化剂强度，但可以降低高融资压力标的在SOXX压力期的尾部回撤。",
            "- 对低F08但短期抗跌的公司，应单独确认是否来自公用事业低beta、特殊事件、低流动性价格缺口或短挤压；不能把价格抗跌直接反写为财务质量改善。",
        ])
    elif base_corr["spearman"] is not None and base_corr["spearman"] > 0 and tb[30]["diff"] > 0:
        lines.extend([
            "- 对“三段SOXX下跌区间累计涨跌幅”这一目标，F08_财务承压可控性有正向但不充分的压力窗口信息；核心 Spearman 或稳健性尚不足以支持单独高权重使用。",
            "- 更稳妥的用法是把 F08 放在风控层：在高AI暴露、高订单弹性或高催化剂标的中，优先保留现金流、杠杆和营运资本更可控的公司。",
            "- 若后续逐日价格序列可用，应补做真实最大回撤、下跌日收益和历史波动率，验证本次固定三窗口代理是否一致。",
        ])
    else:
        lines.extend([
            "- 对“三段SOXX下跌区间累计涨跌幅”这一目标，F08_财务承压可控性不能作为独立正向排序因子；至少不能机械地解释为高分必然抗跌。",
            "- 它仍有基本面风控价值：低F08公司在融资窗口、库存/应收、债务到期和现金消耗上的尾部风险更高，但价格表现还会受行业beta、公用事业防守属性、短期反弹和估值位置影响。",
            "- 后续使用建议是与 F50价格相对强度、F51交易流动性、估值隐含增长压力、订单下修风险可控性和客户集中风险可控性联用；单独使用 F08 容易把“财务健康”误当作“压力期一定少跌”。",
        ])
    lines.append("- 本报告只作为下游特征评估，不反向修改 `公司调研/`、`行业调研/` 或 `日度资料/`。")
    lines.append("")
    lines.append("## 方法说明")
    lines.extend([
        "- Pearson 使用原始F08分数与收益百分比。",
        "- Spearman 使用平均秩处理并列分数；本报告重点看Spearman，因为F08本质是排序评分。",
        "- Kendall 使用tau-b口径，对F08分数并列进行tie修正。",
        "- Top/Bottom按F08评分文件原始排名取样；如公司三段累计收益缺失，则不插补，向后顺延取有效样本。",
        "- 分类中性百分位中，同一分类内高F08分对应更高百分位，然后合并全样本重新排序。",
        f"- 极端涨跌双尾5%阈值按本次{len(rows)}家有效样本三段累计收益计算，低端阈值为 `{fmt_pct(low_q)}`，高端阈值为 `{fmt_pct(high_q)}`。",
        "- 所有收益均为区间Close价格变动，不含股息再投资，不等于总回报。",
    ])
    lines.append("")

    summary = {
        "score_count": len(score),
        "return_count": len([r for r in returns.values() if r.get("cum") is not None]),
        "intersection": len(rows),
        "missing_returns": missing_returns,
        "base_corr": base_corr,
        "window_corrs": window_corrs,
        "tb30": tb[30],
        "risk_top": risk["F08 Top30"],
        "risk_bottom": risk["F08 Bottom30"],
        "neutral_pct_corr": neutral_pct_corr,
        "robust_combined": robust_combined,
        "low_liq_count": sum(low_liq_mask),
        "adr_count": sum(adr_mask),
        "extreme_count": sum(extreme_mask),
        "low_q": low_q,
        "high_q": high_q,
    }
    return "\n".join(lines), summary


def main() -> None:
    report, summary = make_report()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(f"wrote={OUT_PATH}")
    print(f"score_count={summary['score_count']} return_count={summary['return_count']} intersection={summary['intersection']}")
    print(f"missing_returns={','.join(summary['missing_returns'])}")
    print("base_corr=" + ",".join(f"{k}:{fmt_num(v)}" for k, v in summary["base_corr"].items()))
    print("window_spearman=" + ",".join(f"{k}:{fmt_num(v['spearman'])}" for k, v in summary["window_corrs"].items()))
    print("top30=" + ",".join(f"{k}:{fmt_pct(v) if 'avg' in k or k in {'diff', 'top_med', 'bottom_med'} else fmt_pct(v, 1)}" for k, v in summary["tb30"].items() if k not in {"top_rows", "bottom_rows"}))
    print(f"risk_top_cum={fmt_pct(summary['risk_top']['cum'])} risk_bottom_cum={fmt_pct(summary['risk_bottom']['cum'])}")
    print(f"risk_top_worst={fmt_pct(summary['risk_top']['worst'])} risk_bottom_worst={fmt_pct(summary['risk_bottom']['worst'])}")
    print("neutral_pct_corr=" + ",".join(f"{k}:{fmt_num(v)}" for k, v in summary["neutral_pct_corr"].items()))
    print("combined_corr=" + ",".join(f"{k}:{fmt_num(v)}" for k, v in summary["robust_combined"]["corr"].items()))
    print(f"combined_top30_diff={fmt_pct(summary['robust_combined']['tb']['diff'])}")
    print(f"robust_counts low_liq={summary['low_liq_count']} adr={summary['adr_count']} extreme={summary['extreme_count']} thresholds={fmt_pct(summary['low_q'])}/{fmt_pct(summary['high_q'])}")


if __name__ == "__main__":
    main()
