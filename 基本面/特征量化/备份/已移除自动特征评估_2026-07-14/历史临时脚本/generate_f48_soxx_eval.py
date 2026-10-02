from __future__ import annotations

import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path.cwd()
FEATURE_ID = "F48"
FEATURE_NAME = "非AI业务拖累可控性"
FEATURE_SUBJECT = f"{FEATURE_ID}_{FEATURE_NAME}"
RUN_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_SUBJECT}_量化评分_{RUN_DATE}.md"
F51_PATH = ROOT / "特征量化" / "量化评分" / f"F51_交易流动性_量化评分_{RUN_DATE}.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md"
DAILY_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUTPUT_PATH = ROOT / "特征量化" / "特征评估" / f"{FEATURE_SUBJECT}_特征评估_三段SOXX下跌区间涨跌_{RUN_DATE}.md"


def split_md_row(line: str) -> list[str] | None:
    s = line.strip()
    if not s.startswith("|") or "|" not in s[1:]:
        return None
    parts = [p.strip() for p in s.strip("|").split("|")]
    if not parts:
        return None
    if parts[0].startswith("---") or parts[0] in {"排名", "股票代号", "项目", "窗口", "方向", "分类", "分组", "组合", "口径", "指标", "目标收益", "剔除项", "分数区间"}:
        return None
    if all(set(p) <= {"-", ":", " "} for p in parts):
        return None
    return parts


def clean_cell(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "；", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def md(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()


def parse_pct(value: str) -> float | None:
    if value is None:
        return None
    if "N/A" in value or "缺失" == value.strip():
        return None
    m = re.search(r"([+-]?\d+(?:\.\d+)?)\s*%", value)
    if not m:
        return None
    return float(m.group(1))


def parse_score_file(path: Path) -> dict[str, dict]:
    scores: dict[str, dict] = {}
    in_table = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        if line.startswith("## 全公司排序表"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table:
            continue
        parts = split_md_row(line)
        if not parts or len(parts) < 7:
            continue
        if not parts[0].isdigit():
            continue
        ticker = parts[1]
        scores[ticker] = {
            "rank": int(parts[0]),
            "ticker": ticker,
            "name": parts[2],
            "category": parts[3],
            "score": float(parts[4]),
            "evidence": parts[5],
            "confidence": parts[6],
            "core": clean_cell(parts[7]) if len(parts) > 7 else "",
            "penalty": clean_cell(parts[8]) if len(parts) > 8 else "",
            "follow": clean_cell(parts[9]) if len(parts) > 9 else "",
        }
    return scores


def parse_return_file(path: Path) -> tuple[dict[str, dict], list[dict], float, str]:
    returns: dict[str, dict] = {}
    window_defs: list[dict] = []
    soxx_cum = math.nan
    generated_time = ""
    in_detail = False
    current_category = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        if "生成时间：" in line and not generated_time:
            generated_time = line.split("生成时间：", 1)[1].strip().strip("。")
        if "SOXX三段累计涨跌幅" in line:
            val = parse_pct(line)
            if val is not None:
                soxx_cum = val
        parts = split_md_row(line)
        if parts and parts[0].startswith("SOXX下跌") and len(parts) >= 6:
            label = parts[0]
            pct = parse_pct(parts[5])
            m = re.search(r"SOXX下跌(\d+)", label)
            window_defs.append(
                {
                    "idx": int(m.group(1)) if m else len(window_defs) + 1,
                    "label": label,
                    "start": parts[1],
                    "start_close": parts[2],
                    "end": parts[3],
                    "end_close": parts[4],
                    "return": pct,
                }
            )
        if line.startswith("## 全公司明细"):
            in_detail = True
            continue
        if not in_detail:
            continue
        if line.startswith("### "):
            current_category = line[4:].strip()
            continue
        parts = split_md_row(line)
        if not parts or len(parts) < 7:
            continue
        ticker = parts[0]
        if not re.match(r"^[A-Z0-9.\-]+$", ticker):
            continue
        returns[ticker] = {
            "ticker": ticker,
            "name": parts[1],
            "category": current_category or parts[0],
            "r1": parse_pct(parts[2]),
            "r2": parse_pct(parts[3]),
            "r3": parse_pct(parts[4]),
            "cum": parse_pct(parts[5]),
            "note": clean_cell(parts[6]) if len(parts) > 6 else "",
        }
    window_defs.sort(key=lambda x: x["idx"])
    return returns, window_defs, soxx_cum, generated_time


def parse_daily_file(path: Path) -> tuple[dict[str, dict], str]:
    daily: dict[str, dict] = {}
    generated_time = ""
    current_category = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        if line.startswith("- 生成时间：") and not generated_time:
            generated_time = line.split("：", 1)[1].strip()
        if line.startswith("### "):
            current_category = line[4:].strip()
            continue
        parts = split_md_row(line)
        if not parts or len(parts) < 24:
            continue
        ticker = parts[0]
        if not re.match(r"^[A-Z0-9.\-]+$", ticker):
            continue
        call_iv = parse_pct(parts[11])
        put_iv = parse_pct(parts[12])
        iv_values = [v for v in [call_iv, put_iv] if v is not None]
        daily[ticker] = {
            "ticker": ticker,
            "name": parts[1],
            "category": current_category,
            "price_date": parts[2],
            "call_iv": call_iv,
            "put_iv": put_iv,
            "iv": mean(iv_values),
            "currency": parts[13],
            "financial_currency": parts[14],
            "listing_type": parts[19],
            "adr_ratio": parts[20],
            "valuation_check": parts[23],
            "note": clean_cell(parts[24]) if len(parts) > 24 else "",
        }
    return daily, generated_time


def mean(values: list[float] | tuple[float, ...]) -> float | None:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    if not vals:
        return None
    return sum(vals) / len(vals)


def median(values: list[float]) -> float | None:
    vals = sorted(v for v in values if v is not None and not math.isnan(v))
    if not vals:
        return None
    return statistics.median(vals)


def sample_std(values: list[float]) -> float | None:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    if len(vals) < 2:
        return None
    return statistics.stdev(vals)


def avg_rank(values: list[float]) -> list[float]:
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i + 1
        while j < n and values[order[j]] == values[order[i]]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = avg
        i = j
    return ranks


def pearson(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None and not math.isnan(x) and not math.isnan(y)]
    if len(pairs) < 2:
        return None
    xvals = [p[0] for p in pairs]
    yvals = [p[1] for p in pairs]
    mx = sum(xvals) / len(xvals)
    my = sum(yvals) / len(yvals)
    num = sum((x - mx) * (y - my) for x, y in pairs)
    denx = math.sqrt(sum((x - mx) ** 2 for x in xvals))
    deny = math.sqrt(sum((y - my) ** 2 for y in yvals))
    if denx == 0 or deny == 0:
        return None
    return num / (denx * deny)


def spearman(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None and not math.isnan(x) and not math.isnan(y)]
    if len(pairs) < 2:
        return None
    return pearson(avg_rank([p[0] for p in pairs]), avg_rank([p[1] for p in pairs]))


def kendall_tau_b(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None and not math.isnan(x) and not math.isnan(y)]
    n = len(pairs)
    if n < 2:
        return None
    concordant = discordant = ties_x = ties_y = 0
    for i in range(n - 1):
        xi, yi = pairs[i]
        for j in range(i + 1, n):
            xj, yj = pairs[j]
            dx = (xi > xj) - (xi < xj)
            dy = (yi > yj) - (yi < yj)
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
    den = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    if den == 0:
        return None
    return (concordant - discordant) / den


def corr_pack(records: list[dict], target: str = "cum", score_field: str = "score") -> dict:
    xs = [r[score_field] for r in records]
    ys = [r[target] for r in records]
    return {
        "n": len(records),
        "pearson": pearson(xs, ys),
        "spearman": spearman(xs, ys),
        "kendall": kendall_tau_b(xs, ys),
    }


def quantile(values: list[float], q: float) -> float:
    vals = sorted(values)
    if not vals:
        return math.nan
    if len(vals) == 1:
        return vals[0]
    pos = (len(vals) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return vals[lo]
    return vals[lo] * (hi - pos) + vals[hi] * (pos - lo)


def fmt_num(value: float | None, digits: int = 3) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    return f"{value:.{digits}f}"


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    return f"{value:+.{digits}f}%"


def fmt_rate(value: float | None, digits: int = 1) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    return f"{value:+.{digits}f}%"


def fmt_score(value: float | None) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"
    return f"{value:.1f}"


def top_bottom(records: list[dict], n: int, soxx_cum: float) -> dict:
    ordered = sorted(records, key=lambda r: r["rank"])
    top = ordered[:n]
    bottom = ordered[-n:]
    def pack(group: list[dict]) -> dict:
        vals = [r["cum"] for r in group]
        return {
            "mean": mean(vals),
            "median": median(vals),
            "hit": 100 * sum(1 for v in vals if v > soxx_cum) / len(vals) if vals else None,
            "positive": 100 * sum(1 for v in vals if v > 0) / len(vals) if vals else None,
        }
    tp = pack(top)
    bp = pack(bottom)
    return {
        "n": n,
        "top": top,
        "bottom": list(reversed(bottom)),
        "top_stats": tp,
        "bottom_stats": bp,
        "spread": None if tp["mean"] is None or bp["mean"] is None else tp["mean"] - bp["mean"],
        "hit_spread": None if tp["hit"] is None or bp["hit"] is None else tp["hit"] - bp["hit"],
    }


def quintiles(records: list[dict], soxx_cum: float) -> list[dict]:
    ordered = sorted(records, key=lambda r: r["rank"])
    n = len(ordered)
    groups = []
    for i in range(5):
        start = round(i * n / 5)
        end = round((i + 1) * n / 5)
        group = ordered[start:end]
        vals = [r["cum"] for r in group]
        groups.append(
            {
                "name": ["Q1最高分", "Q2", "Q3", "Q4", "Q5最低分"][i],
                "records": group,
                "n": len(group),
                "score_mean": mean([r["score"] for r in group]),
                "cum_mean": mean(vals),
                "cum_median": median(vals),
                "hit": 100 * sum(1 for v in vals if v > soxx_cum) / len(vals) if vals else None,
                "worst_mean": mean([min(r["r1"], r["r2"], r["r3"]) for r in group]),
                "iv_mean": mean([r.get("iv") for r in group]),
                "iv_n": sum(1 for r in group if r.get("iv") is not None),
            }
        )
    return groups


def risk_pack(label: str, group: list[dict], window_defs: list[dict], soxx_cum: float) -> dict:
    windows = ["r1", "r2", "r3"]
    all_window_values = []
    beat_count = 0
    neg_count = 0
    obs = 0
    for r in group:
        for idx, w in enumerate(windows):
            value = r[w]
            if value is None:
                continue
            obs += 1
            all_window_values.append(value)
            if window_defs and idx < len(window_defs) and value > window_defs[idx]["return"]:
                beat_count += 1
            if value < 0:
                neg_count += 1
    return {
        "label": label,
        "n": len(group),
        "obs": obs,
        "r1_mean": mean([r["r1"] for r in group]),
        "r2_mean": mean([r["r2"] for r in group]),
        "r3_mean": mean([r["r3"] for r in group]),
        "cum_mean": mean([r["cum"] for r in group]),
        "stress_mean": mean(all_window_values),
        "worst_mean": mean([min(r["r1"], r["r2"], r["r3"]) for r in group]),
        "dispersion": mean([sample_std([r["r1"], r["r2"], r["r3"]]) for r in group]),
        "beat_window": 100 * beat_count / obs if obs else None,
        "beat_cum": 100 * sum(1 for r in group if r["cum"] > soxx_cum) / len(group) if group else None,
        "negative_window": 100 * neg_count / obs if obs else None,
        "call_iv": mean([r.get("call_iv") for r in group]),
        "put_iv": mean([r.get("put_iv") for r in group]),
        "iv": mean([r.get("iv") for r in group]),
        "iv_median": median([r.get("iv") for r in group if r.get("iv") is not None]),
        "iv_n": sum(1 for r in group if r.get("iv") is not None),
    }


def category_percentiles(records: list[dict]) -> list[dict]:
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_cat[r["category"]].append(r)
    out = []
    for group in by_cat.values():
        vals = [r["score"] for r in group]
        ranks = avg_rank(vals)
        denom = max(len(group) - 1, 1)
        for r, rank in zip(group, ranks):
            nr = dict(r)
            nr["score_pct"] = (rank - 1) / denom if len(group) > 1 else 0.5
            nr["score_resid"] = r["score"] - mean(vals)
            nr["cum_resid"] = r["cum"] - mean([x["cum"] for x in group])
            out.append(nr)
    return out


def category_stats(records: list[dict]) -> list[dict]:
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_cat[r["category"]].append(r)
    rows = []
    for cat in sorted(by_cat):
        group = by_cat[cat]
        cp = corr_pack(group)
        best = max(group, key=lambda r: r["cum"])
        worst = min(group, key=lambda r: r["cum"])
        highest = sorted(group, key=lambda r: r["rank"])[0]
        rows.append(
            {
                "category": cat,
                "n": len(group),
                "score_mean": mean([r["score"] for r in group]),
                "cum_mean": mean([r["cum"] for r in group]),
                "cum_median": median([r["cum"] for r in group]),
                "hit": 100 * sum(1 for r in group if r["cum"] > SOXX_CUM) / len(group),
                "pearson": cp["pearson"],
                "spearman": cp["spearman"],
                "kendall": cp["kendall"],
                "best": best,
                "worst": worst,
                "highest": highest,
            }
        )
    return rows


def robust_row(label: str, rule: str, subset: list[dict], base_n: int, soxx_cum: float) -> dict:
    cp = corr_pack(subset)
    tb = top_bottom(subset, 30, soxx_cum) if len(subset) >= 60 else None
    return {
        "label": label,
        "rule": rule,
        "n": len(subset),
        "excluded": base_n - len(subset),
        "pearson": cp["pearson"],
        "spearman": cp["spearman"],
        "kendall": cp["kendall"],
        "top_mean": tb["top_stats"]["mean"] if tb else None,
        "bottom_mean": tb["bottom_stats"]["mean"] if tb else None,
        "spread": tb["spread"] if tb else None,
        "hit_spread": tb["hit_spread"] if tb else None,
    }


def effect_label(x: float | None) -> str:
    if x is None:
        return "无法判断"
    if x >= 0.25:
        return "中等正向"
    if x >= 0.10:
        return "弱正向"
    if x <= -0.25:
        return "明显反向"
    if x <= -0.10:
        return "反向"
    return "不明显"


def spread_label(x: float | None) -> str:
    if x is None:
        return "无法判断"
    if x >= 20:
        return "成立"
    if x >= 5:
        return "弱成立"
    if x <= -20:
        return "明显反向"
    if x <= -5:
        return "反向"
    return "不明显"


def top_bottom_lines(tb: dict) -> list[str]:
    t = tb["top_stats"]
    b = tb["bottom_stats"]
    return [
        f"| Top{tb['n']}/Bottom{tb['n']} | {fmt_pct(t['mean'])} | {fmt_pct(t['median'])} | {fmt_rate(t['hit'])} | {fmt_rate(t['positive'])} | {fmt_pct(b['mean'])} | {fmt_pct(b['median'])} | {fmt_rate(b['hit'])} | {fmt_rate(b['positive'])} | {fmt_pct(tb['spread'])} |"
    ]


def record_row(group: str, r: dict) -> str:
    return (
        f"| {group} | {md(r['ticker'])} | {md(r['name'])} | {md(r['category'])} | "
        f"{fmt_pct(r['cum'])} | {fmt_pct(r['r1'])} | {fmt_pct(r['r2'])} | {fmt_pct(r['r3'])} | "
        f"{fmt_score(r['score'])} | {r['rank']} | {md(r['confidence'])} |"
    )


scores = parse_score_file(SCORE_PATH)
f51_scores = parse_score_file(F51_PATH)
returns, window_defs, SOXX_CUM, return_generated_time = parse_return_file(RETURN_PATH)
daily, daily_generated_time = parse_daily_file(DAILY_PATH)

records: list[dict] = []
missing_return = []
for ticker, sc in scores.items():
    rt = returns.get(ticker)
    if not rt or rt["cum"] is None:
        missing_return.append(ticker)
        continue
    dy = daily.get(ticker, {})
    f51 = f51_scores.get(ticker)
    rec = {
        **sc,
        "return_name": rt["name"],
        "return_category": rt["category"],
        "r1": rt["r1"],
        "r2": rt["r2"],
        "r3": rt["r3"],
        "cum": rt["cum"],
        "return_note": rt["note"],
        "f51": f51["score"] if f51 else None,
        "call_iv": dy.get("call_iv"),
        "put_iv": dy.get("put_iv"),
        "iv": dy.get("iv"),
        "listing_type": dy.get("listing_type", ""),
        "adr_ratio": dy.get("adr_ratio", ""),
        "currency": dy.get("currency", ""),
        "financial_currency": dy.get("financial_currency", ""),
        "valuation_check": dy.get("valuation_check", ""),
    }
    records.append(rec)

records.sort(key=lambda r: r["rank"])
return_missing_with_score = sorted(set(scores) - {r["ticker"] for r in records})
return_only = sorted(set(returns) - set(scores))
cat_mismatch = sorted(r["ticker"] for r in records if r["category"] != r["return_category"])

main_corr = corr_pack(records)
window_corrs = {
    "r1": corr_pack(records, "r1"),
    "r2": corr_pack(records, "r2"),
    "r3": corr_pack(records, "r3"),
}

q_rows = quintiles(records, SOXX_CUM)
tb10 = top_bottom(records, 10, SOXX_CUM)
tb20 = top_bottom(records, 20, SOXX_CUM)
tb30 = top_bottom(records, 30, SOXX_CUM)

ordered = sorted(records, key=lambda r: r["rank"])
mid_start = (len(ordered) - 30) // 2
top30 = ordered[:30]
mid30 = ordered[mid_start : mid_start + 30]
bottom30 = ordered[-30:]
risk_rows = [
    risk_pack(f"{FEATURE_ID} Top30", top30, window_defs, SOXX_CUM),
    risk_pack(f"{FEATURE_ID} Mid30", mid30, window_defs, SOXX_CUM),
    risk_pack(f"{FEATURE_ID} Bottom30", bottom30, window_defs, SOXX_CUM),
]

neutral_records = category_percentiles(records)
neutral_pct_corr = {
    "n": len(neutral_records),
    "pearson": pearson([r["score_pct"] for r in neutral_records], [r["cum"] for r in neutral_records]),
    "spearman": spearman([r["score_pct"] for r in neutral_records], [r["cum"] for r in neutral_records]),
    "kendall": kendall_tau_b([r["score_pct"] for r in neutral_records], [r["cum"] for r in neutral_records]),
}
neutral_resid_corr = {
    "n": len(neutral_records),
    "pearson": pearson([r["score_resid"] for r in neutral_records], [r["cum_resid"] for r in neutral_records]),
    "spearman": spearman([r["score_resid"] for r in neutral_records], [r["cum_resid"] for r in neutral_records]),
    "kendall": kendall_tau_b([r["score_resid"] for r in neutral_records], [r["cum_resid"] for r in neutral_records]),
}
neutral_order = sorted(neutral_records, key=lambda r: (-r["score_pct"], r["rank"]))
neutral_records_for_tb = [dict(r, rank=i + 1) for i, r in enumerate(neutral_order)]
ntb10 = top_bottom(neutral_records_for_tb, 10, SOXX_CUM)
ntb20 = top_bottom(neutral_records_for_tb, 20, SOXX_CUM)
ntb30 = top_bottom(neutral_records_for_tb, 30, SOXX_CUM)

cat_rows = category_stats(records)

low_liq_excluded = sorted(r["ticker"] for r in records if r.get("f51") is None or r.get("f51") <= 5.0)
adr_excluded = sorted(
    r["ticker"]
    for r in records
    if r.get("listing_type") != "common/equity"
    or r.get("adr_ratio") != "不适用"
    or r.get("currency") != r.get("financial_currency")
    or "currency_mismatch" in r.get("valuation_check", "")
)
cum_values = [r["cum"] for r in records]
q05 = quantile(cum_values, 0.05)
q95 = quantile(cum_values, 0.95)
extreme_excluded = sorted(r["ticker"] for r in records if r["cum"] <= q05 or r["cum"] >= q95)

low_liq_set = set(low_liq_excluded)
adr_set = set(adr_excluded)
extreme_set = set(extreme_excluded)

robust_rows = [
    robust_row("全样本基准", "无剔除", records, len(records), SOXX_CUM),
    robust_row("剔除低流动性", "F51交易流动性分 > 5.0", [r for r in records if r["ticker"] not in low_liq_set], len(records), SOXX_CUM),
    robust_row(
        "剔除ADR/币种异常",
        "listing_type=common/equity、ADR比例不适用、交易/财报货币一致、估值校验无currency_mismatch",
        [r for r in records if r["ticker"] not in adr_set],
        len(records),
        SOXX_CUM,
    ),
    robust_row(
        "剔除极端涨跌",
        f"剔除三段累计涨跌双尾5%；阈值 {fmt_pct(q05)} / {fmt_pct(q95)}",
        [r for r in records if r["ticker"] not in extreme_set],
        len(records),
        SOXX_CUM,
    ),
    robust_row(
        "三项合并剔除",
        "同时满足上述三项",
        [r for r in records if r["ticker"] not in low_liq_set | adr_set | extreme_set],
        len(records),
        SOXX_CUM,
    ),
]

best15 = sorted(records, key=lambda r: r["cum"], reverse=True)[:15]
worst15 = sorted(records, key=lambda r: r["cum"])[:15]
high15 = ordered[:15]
low15 = list(reversed(ordered[-15:]))
high_drag = [r for r in ordered[:60] if r["cum"] < SOXX_CUM][:10]
low_beat = [r for r in reversed(ordered[-80:]) if r["cum"] > SOXX_CUM][:12]

score_dist = Counter()
for r in records:
    s = r["score"]
    if s >= 9.0:
        score_dist["9.0-10.0"] += 1
    elif s >= 7.0:
        score_dist["7.0-8.9"] += 1
    elif s >= 5.0:
        score_dist["5.0-6.9"] += 1
    elif s >= 3.0:
        score_dist["3.0-4.9"] += 1
    else:
        score_dist["1.0-2.9"] += 1

spearman_judgement = effect_label(main_corr["spearman"])
top_judgement = spread_label(tb30["spread"])
risk_judgement = "成立" if (risk_rows[0]["cum_mean"] > risk_rows[2]["cum_mean"] and risk_rows[0]["worst_mean"] > risk_rows[2]["worst_mean"] and (risk_rows[0]["iv"] or 999) < (risk_rows[2]["iv"] or -999)) else "不充分"
neutral_judgement = effect_label(neutral_pct_corr["spearman"])
combined = robust_rows[-1]
if combined["spearman"] is not None and combined["spearman"] > 0 and combined["spread"] is not None and combined["spread"] > 0:
    robust_judgement = "弱成立" if combined["spearman"] < 0.25 or combined["spread"] < 20 else "成立"
else:
    robust_judgement = "不稳定/不成立"

lines: list[str] = []
lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 三段SOXX下跌区间涨跌 {RUN_DATE}")
lines.append("")
lines.append("## 运行元信息")
lines.append(f"- 评估对象：`{FEATURE_SUBJECT}`。")
lines.append(f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 {RUN_DATE}，覆盖 {len(scores)} 家。")
lines.append(f"- 收益输入：`日度资料/区间涨跌/{RETURN_PATH.name}`，生成时间 {return_generated_time}；价格口径为 Yahoo Finance `Close`，`auto_adjust=False`，不含股息再投资。")
if len(window_defs) >= 3:
    lines.append(
        "- SOXX压力窗口："
        f"{window_defs[0]['start']}至{window_defs[0]['end']} {fmt_pct(window_defs[0]['return'])}；"
        f"{window_defs[1]['start']}至{window_defs[1]['end']} {fmt_pct(window_defs[1]['return'])}；"
        f"{window_defs[2]['start']}至{window_defs[2]['end']} {fmt_pct(window_defs[2]['return'])}。"
        f"SOXX三段累计涨跌幅为 {fmt_pct(SOXX_CUM)}。"
    )
lines.append(f"- 稳健性辅助输入：`特征量化/量化评分/{F51_PATH.name}`；`日度资料/每日金融数据/{DAILY_PATH.name}`，金融数据生成时间 {daily_generated_time}。")
lines.append(f"- 有效评估样本：评分与三段累计涨跌幅交集 {len(records)} 家；F48评分有但累计涨跌缺失 {len(return_missing_with_score)} 家：{', '.join(return_missing_with_score) if return_missing_with_score else '无'}。")
lines.append("- 收益方向口径：三段累计涨跌幅越高越好；在压力窗口中，跌幅更小、或上涨，均视为更优表现。")
lines.append(f"- 命中率口径：三段累计涨跌幅大于 SOXX 三段累计涨跌幅 `{fmt_pct(SOXX_CUM)}` 记为压力命中；Top-Bottom收益差=高分组合平均三段累计收益 - 低分组合平均三段累计收益。")
lines.append("- 风险口径限制：本次输入是三个固定压力区间收益，不是逐日收益序列；因此本报告不写成严格日度波动率、完整最大回撤或真实下跌日胜率结论，而使用三个SOXX下跌窗口均值、平均最差窗口、窗口离散度、跑赢SOXX比例、负收益窗口占比，并用 2026-06-03 近ATM Call/Put IV均值补充当前波动代理。")
lines.append("- 稳健性口径：低流动性使用 `F51<=5.0` 或F51缺失作为剔除代理；ADR/币种异常使用每日金融数据中的 `listing_type`、ADR比例、交易/财报货币和 `currency_mismatch` 标记；极端涨跌按本次三段累计收益双尾5%剔除。")
lines.append("- 旧版处理：本次未读取或继承旧版F48三段SOXX特征评估；直接写入指定正式路径。")
lines.append("- 本报告是下游特征评估，只读取 `特征量化/量化评分/`、`特征量化/特征评估/`、`日度资料/区间涨跌/` 和必要日度金融字段，不把结论反向写入上游资料。")
lines.append("")

lines.append("## 结论摘要")
lines.append(f"- 排序有效性：{spearman_judgement}。全样本 Pearson {fmt_num(main_corr['pearson'])}，Spearman {fmt_num(main_corr['spearman'])}，Kendall {fmt_num(main_corr['kendall'])}；重点指标 Spearman 用于判断 F48 高分是否对应三段SOXX压力期少跌。")
lines.append(f"- 分窗口观察：SOXX下跌1/2/3 的 Spearman 分别为 {fmt_num(window_corrs['r1']['spearman'])}、{fmt_num(window_corrs['r2']['spearman'])}、{fmt_num(window_corrs['r3']['spearman'])}。如果某一段明显偏离，应结合行业beta、估值、流动性和个股事件解释。")
lines.append(f"- Top/Bottom能力：{top_judgement}。Top10/Top20/Top30 平均累计收益分别为 {fmt_pct(tb10['top_stats']['mean'])}、{fmt_pct(tb20['top_stats']['mean'])}、{fmt_pct(tb30['top_stats']['mean'])}；对应Top-Bottom收益差为 {fmt_pct(tb10['spread'])}、{fmt_pct(tb20['spread'])}、{fmt_pct(tb30['spread'])}。")
lines.append(f"- 风险解释力：{risk_judgement}。F48 Top30 三段累计均值 {fmt_pct(risk_rows[0]['cum_mean'])}、平均最差窗口 {fmt_pct(risk_rows[0]['worst_mean'])}、跑赢SOXX窗口比例 {fmt_rate(risk_rows[0]['beat_window'])}、当前IV均值 {fmt_pct(risk_rows[0]['iv'])}；Bottom30 对应为 {fmt_pct(risk_rows[2]['cum_mean'])}、{fmt_pct(risk_rows[2]['worst_mean'])}、{fmt_rate(risk_rows[2]['beat_window'])}、{fmt_pct(risk_rows[2]['iv'])}。")
lines.append(f"- 分类中性：{neutral_judgement}。分类内百分位合并 Spearman {fmt_num(neutral_pct_corr['spearman'])}，分类去均值残差 Spearman {fmt_num(neutral_resid_corr['spearman'])}；中性Top30-Bottom30收益差 {fmt_pct(ntb30['spread'])}。")
lines.append(f"- 稳健性：{robust_judgement}。剔除低流动性后 Spearman {fmt_num(robust_rows[1]['spearman'])}，剔除ADR/币种异常后 {fmt_num(robust_rows[2]['spearman'])}，剔除极端涨跌后 {fmt_num(robust_rows[3]['spearman'])}，三项合并后 {fmt_num(robust_rows[4]['spearman'])}；三项合并后Top30-Bottom30为 {fmt_pct(robust_rows[4]['spread'])}。")
lines.append("- 解释：F48衡量“非AI/传统业务包袱是否会抵消AI增长、利润、现金流或估值重估”。在SOXX下跌窗口中，这个特征更接近质量/防守因子：若高分端少跌且IV更低，说明传统业务拖累可控能改善下行韧性；若收益排序不强，则提示F48不应单独替代价格相对强度、估值、流动性或事件风险因子。")
lines.append("")

lines.append("## 覆盖检查")
lines.append("| 项目 | 数量 | 说明 |")
lines.append("| --- | ---: | --- |")
lines.append(f"| F48评分覆盖 | {len(scores)} | 来自2026-06-04评分文件 |")
lines.append(f"| 三段累计涨跌覆盖 | {sum(1 for v in returns.values() if v['cum'] is not None)} | 来自2026-06-04三段SOXX下跌区间涨跌文件 |")
lines.append(f"| 交集有效样本 | {len(records)} | 用于本报告主指标 |")
lines.append(f"| 评分有但累计涨跌缺失 | {len(return_missing_with_score)} | {', '.join(return_missing_with_score) if return_missing_with_score else '无'} |")
lines.append(f"| 涨跌有但评分缺失 | {len(return_only)} | {', '.join(return_only) if return_only else '无'} |")
lines.append(f"| 分类目录不一致 | {len(cat_mismatch)} | {', '.join(cat_mismatch) if cat_mismatch else '无'} |")
lines.append("")

lines.append("### 交集样本分类分布")
lines.append("| 分类目录 | 样本数 | F48均分 | 三段累计平均 | 三段累计中位数 | 跑赢SOXX累计率 |")
lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
for row in cat_rows:
    lines.append(f"| {md(row['category'])} | {row['n']} | {fmt_score(row['score_mean'])} | {fmt_pct(row['cum_mean'])} | {fmt_pct(row['cum_median'])} | {fmt_rate(row['hit'])} |")
lines.append("")

lines.append("## 排序有效性")
lines.append("| 目标收益 | 样本数 | Pearson | Spearman | Kendall tau-b | 解释 |")
lines.append("| --- | ---: | ---: | ---: | ---: | --- |")
lines.append(f"| 三段累计涨跌幅 | {main_corr['n']} | {fmt_num(main_corr['pearson'])} | {fmt_num(main_corr['spearman'])} | {fmt_num(main_corr['kendall'])} | 核心目标；三个SOXX下跌区间百分比简单相加，越高越好 |")
for i, key in enumerate(["r1", "r2", "r3"]):
    wc = window_corrs[key]
    wd = window_defs[i]
    lines.append(f"| SOXX下跌{i+1}：{wd['start']}至{wd['end']} | {wc['n']} | {fmt_num(wc['pearson'])} | {fmt_num(wc['spearman'])} | {fmt_num(wc['kendall'])} | 单个压力窗口，SOXX {fmt_pct(wd['return'])} |")
lines.append("")

lines.append("### F48分数分组收益")
lines.append("| 分组 | 公司数 | F48均分 | 三段累计平均 | 三段累计中位数 | 跑赢SOXX累计率 | 平均最差窗口 | 当前IV均值 | IV样本 |")
lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
for row in q_rows:
    lines.append(f"| {row['name']} | {row['n']} | {fmt_score(row['score_mean'])} | {fmt_pct(row['cum_mean'])} | {fmt_pct(row['cum_median'])} | {fmt_rate(row['hit'])} | {fmt_pct(row['worst_mean'])} | {fmt_pct(row['iv_mean'])} | {row['iv_n']} |")
lines.append("")
lines.append("分组读数应区分“非AI业务拖累可控性”和“压力期beta”。F48最高分五分位主要包含非AI业务稳定、现金流/RPO/backlog/订单底座更强、传统业务不明显抵消AI主线的公司；若这些公司在压力窗口少跌并且当前IV更低，说明F48具备下行风险解释力。")
lines.append("")

lines.append("## Top/Bottom能力")
lines.append("| 组合 | Top平均累计 | Top中位累计 | Top压力命中率 | Top正收益率 | Bottom平均累计 | Bottom中位累计 | Bottom压力命中率 | Bottom正收益率 | Top-Bottom收益差 |")
lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
for tb in [tb10, tb20, tb30]:
    lines.extend(top_bottom_lines(tb))
lines.append("")

lines.append("### Top10与Bottom10构成")
lines.append("| 组别 | 股票代号 | 公司名称 | 分类目录 | 三段累计 | SOXX跌1 | SOXX跌2 | SOXX跌3 | F48分 | F48排名 | 置信度 |")
lines.append("| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
for r in tb10["top"]:
    lines.append(record_row("Top10", r))
for r in tb10["bottom"]:
    lines.append(record_row("Bottom10", r))
lines.append("")

lines.append("## 风险解释力")
lines.append("本节只使用三个固定SOXX下跌区间作为压力测试代理。严格日度波动率、完整最大回撤、真实下跌日收益稳定性需要逐日价格序列；当前IV均值仅是 2026-06-03 近ATM期权波动代理，不等同于历史实际波动率。")
lines.append("")
lines.append("| 分组 | 公司数 | 窗口观测 | SOXX跌1均值 | SOXX跌2均值 | SOXX跌3均值 | 三段累计均值 | 压力窗口均值 | 平均最差窗口 | 窗口离散度 | 跑赢SOXX窗口比例 | 跑赢SOXX累计率 | 负收益窗口占比 | 平均Call IV | 平均Put IV | 当前IV均值 | IV中位数 | IV样本 |")
lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
for row in risk_rows:
    lines.append(
        f"| {row['label']} | {row['n']} | {row['obs']} | {fmt_pct(row['r1_mean'])} | {fmt_pct(row['r2_mean'])} | {fmt_pct(row['r3_mean'])} | "
        f"{fmt_pct(row['cum_mean'])} | {fmt_pct(row['stress_mean'])} | {fmt_pct(row['worst_mean'])} | {fmt_pct(row['dispersion'])} | "
        f"{fmt_rate(row['beat_window'])} | {fmt_rate(row['beat_cum'])} | {fmt_rate(row['negative_window'])} | "
        f"{fmt_pct(row['call_iv'])} | {fmt_pct(row['put_iv'])} | {fmt_pct(row['iv'])} | {fmt_pct(row['iv_median'])} | {row['iv_n']} |"
    )
lines.append("")
lines.append(f"结论：F48 Top30 相比 Bottom30，三段累计差值为 {fmt_pct(risk_rows[0]['cum_mean'] - risk_rows[2]['cum_mean']) if risk_rows[0]['cum_mean'] is not None and risk_rows[2]['cum_mean'] is not None else 'N/A'}，平均最差窗口差值为 {fmt_pct(risk_rows[0]['worst_mean'] - risk_rows[2]['worst_mean']) if risk_rows[0]['worst_mean'] is not None and risk_rows[2]['worst_mean'] is not None else 'N/A'}，跑赢SOXX窗口比例差值为 {fmt_rate(risk_rows[0]['beat_window'] - risk_rows[2]['beat_window']) if risk_rows[0]['beat_window'] is not None and risk_rows[2]['beat_window'] is not None else 'N/A'}，当前IV均值差值为 {fmt_pct(risk_rows[0]['iv'] - risk_rows[2]['iv']) if risk_rows[0]['iv'] is not None and risk_rows[2]['iv'] is not None else 'N/A'}。这些指标用于判断“高F48是否回撤更小、波动更低、下跌窗口更稳”。")
lines.append("")

lines.append("## 分类中性结果")
lines.append("| 口径 | 样本数 | Pearson | Spearman | Kendall | 说明 |")
lines.append("| --- | ---: | ---: | ---: | ---: | --- |")
lines.append(f"| 原始全样本 | {len(records)} | {fmt_num(main_corr['pearson'])} | {fmt_num(main_corr['spearman'])} | {fmt_num(main_corr['kendall'])} | 直接用F48原始分数排序 |")
lines.append(f"| 分类内百分位合并 | {neutral_pct_corr['n']} | {fmt_num(neutral_pct_corr['pearson'])} | {fmt_num(neutral_pct_corr['spearman'])} | {fmt_num(neutral_pct_corr['kendall'])} | 每个分类内先按F48排序，再转为0-1百分位合并 |")
lines.append(f"| 分类去均值残差 | {neutral_resid_corr['n']} | {fmt_num(neutral_resid_corr['pearson'])} | {fmt_num(neutral_resid_corr['spearman'])} | {fmt_num(neutral_resid_corr['kendall'])} | F48和累计收益分别减去分类均值后相关 |")
lines.append("")

lines.append("### 分类中性Top/Bottom")
lines.append("| 组合 | Top平均累计 | Top压力命中率 | Bottom平均累计 | Bottom压力命中率 | Top-Bottom收益差 |")
lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
for tb in [ntb10, ntb20, ntb30]:
    lines.append(f"| 中性Top{tb['n']}/Bottom{tb['n']} | {fmt_pct(tb['top_stats']['mean'])} | {fmt_rate(tb['top_stats']['hit'])} | {fmt_pct(tb['bottom_stats']['mean'])} | {fmt_rate(tb['bottom_stats']['hit'])} | {fmt_pct(tb['spread'])} |")
lines.append("")

lines.append("### 10个分类目录内相关性")
lines.append("| 分类目录 | 样本数 | Pearson | Spearman | Kendall | 类内累计均值 | 类内命中率 | 类内最好 | 类内最差 | 类内最高F48公司 |")
lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |")
for row in cat_rows:
    best = row["best"]
    worst = row["worst"]
    highest = row["highest"]
    lines.append(
        f"| {md(row['category'])} | {row['n']} | {fmt_num(row['pearson'])} | {fmt_num(row['spearman'])} | {fmt_num(row['kendall'])} | "
        f"{fmt_pct(row['cum_mean'])} | {fmt_rate(row['hit'])} | {best['ticker']} {fmt_pct(best['cum'])} | {worst['ticker']} {fmt_pct(worst['cum'])} | "
        f"{highest['ticker']} {fmt_score(highest['score'])} / {fmt_pct(highest['cum'])} |"
    )
lines.append("")
lines.append("分类内结果用于检验 F48 是否只是押中了某个分类目录。若分类内百分位合并和分类去均值残差仍有效，说明同一产业目录内“非AI业务拖累更可控”也能解释压力窗口少跌；若转弱，则原始读数可能主要来自行业配置或大盘质量风格。")
lines.append("")

lines.append("## 稳健性检验")
lines.append("| 口径 | 剔除规则 | 样本数 | 剔除数 | Pearson | Spearman | Kendall | Top30均值 | Bottom30均值 | Top30-Bottom30 | Top-Bottom命中率差 |")
lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
for row in robust_rows:
    lines.append(f"| {row['label']} | {row['rule']} | {row['n']} | {row['excluded']} | {fmt_num(row['pearson'])} | {fmt_num(row['spearman'])} | {fmt_num(row['kendall'])} | {fmt_pct(row['top_mean'])} | {fmt_pct(row['bottom_mean'])} | {fmt_pct(row['spread'])} | {fmt_rate(row['hit_spread'])} |")
lines.append("")
lines.append("稳健性结论：低流动性、ADR/币种异常和极端涨跌剔除后，重点看 Spearman 与 Top30-Bottom30是否仍同向为正，同时风险窗口和IV代理是否仍改善。若过滤后排序转弱但Top/Bottom风险代理保持改善，则F48应保留为防守/质量过滤变量，而不是单独收益排序因子。")
lines.append("")

lines.append("### 剔除清单")
lines.append("| 剔除项 | 数量 | 公司 |")
lines.append("| --- | ---: | --- |")
lines.append(f"| 低流动性 | {len(low_liq_excluded)} | {', '.join(low_liq_excluded) if low_liq_excluded else '无'} |")
lines.append(f"| ADR/币种异常 | {len(adr_excluded)} | {', '.join(adr_excluded) if adr_excluded else '无'} |")
lines.append(f"| 极端涨跌双尾5% | {len(extreme_excluded)} | {', '.join(extreme_excluded) if extreme_excluded else '无'} |")
lines.append("")

lines.append("## 诊断：收益由哪些公司主导")
lines.append("### 三段累计表现最好15")
lines.append("| 股票代号 | 公司名称 | 分类目录 | 三段累计 | SOXX跌1 | SOXX跌2 | SOXX跌3 | F48分 | F48排名 | 置信度 |")
lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
for r in best15:
    lines.append(f"| {r['ticker']} | {md(r['name'])} | {md(r['category'])} | {fmt_pct(r['cum'])} | {fmt_pct(r['r1'])} | {fmt_pct(r['r2'])} | {fmt_pct(r['r3'])} | {fmt_score(r['score'])} | {r['rank']} | {md(r['confidence'])} |")
lines.append("")

lines.append("### 三段累计表现最差15")
lines.append("| 股票代号 | 公司名称 | 分类目录 | 三段累计 | SOXX跌1 | SOXX跌2 | SOXX跌3 | F48分 | F48排名 | 置信度 |")
lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
for r in worst15:
    lines.append(f"| {r['ticker']} | {md(r['name'])} | {md(r['category'])} | {fmt_pct(r['cum'])} | {fmt_pct(r['r1'])} | {fmt_pct(r['r2'])} | {fmt_pct(r['r3'])} | {fmt_score(r['score'])} | {r['rank']} | {md(r['confidence'])} |")
lines.append("")

lines.append("### F48高分前15")
lines.append("| 股票代号 | 公司名称 | 分类目录 | 三段累计 | SOXX跌1 | SOXX跌2 | SOXX跌3 | F48分 | F48排名 | 置信度 |")
lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
for r in high15:
    lines.append(f"| {r['ticker']} | {md(r['name'])} | {md(r['category'])} | {fmt_pct(r['cum'])} | {fmt_pct(r['r1'])} | {fmt_pct(r['r2'])} | {fmt_pct(r['r3'])} | {fmt_score(r['score'])} | {r['rank']} | {md(r['confidence'])} |")
lines.append("")

lines.append("### F48低分前15")
lines.append("| 股票代号 | 公司名称 | 分类目录 | 三段累计 | SOXX跌1 | SOXX跌2 | SOXX跌3 | F48分 | F48排名 | 置信度 |")
lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
for r in low15:
    lines.append(f"| {r['ticker']} | {md(r['name'])} | {md(r['category'])} | {fmt_pct(r['cum'])} | {fmt_pct(r['r1'])} | {fmt_pct(r['r2'])} | {fmt_pct(r['r3'])} | {fmt_score(r['score'])} | {r['rank']} | {md(r['confidence'])} |")
lines.append("")

lines.append("### 高F48但压力窗口显著拖累")
lines.append("| 股票代号 | 公司名称 | 分类目录 | F48分 | F48排名 | 三段累计 | 主要提示 |")
lines.append("| --- | --- | --- | ---: | ---: | ---: | --- |")
for r in high_drag:
    lines.append(f"| {r['ticker']} | {md(r['name'])} | {md(r['category'])} | {fmt_score(r['score'])} | {r['rank']} | {fmt_pct(r['cum'])} | 非AI拖累可控不等于压力期低beta；需叠加估值、价格相对强度、客户集中、流动性和个股事件过滤。 |")
if not high_drag:
    lines.append("| 无 | 无 | 无 | N/A | N/A | N/A | 高F48前60中没有跌破SOXX累计的样本。 |")
lines.append("")

lines.append("### 低F48但跑赢SOXX累计")
lines.append("| 股票代号 | 公司名称 | 分类目录 | F48分 | F48排名 | 三段累计 | 主要提示 |")
lines.append("| --- | --- | --- | ---: | ---: | ---: | --- |")
for r in low_beat:
    lines.append(f"| {r['ticker']} | {md(r['name'])} | {md(r['category'])} | {fmt_score(r['score'])} | {r['rank']} | {fmt_pct(r['cum'])} | F48低分说明非AI业务包袱或商业化/亏损/周期拖累更明显，但压力期表现仍可能来自低beta、特殊事件、低流动性反弹、估值修复或非AI防守属性。 |")
if not low_beat:
    lines.append("| 无 | 无 | 无 | N/A | N/A | N/A | 低F48样本均未跑赢SOXX累计。 |")
lines.append("")

lines.append("## 分数分布")
lines.append("| 分数区间 | 有效样本公司数 |")
lines.append("| --- | ---: |")
for band in ["9.0-10.0", "7.0-8.9", "5.0-6.9", "3.0-4.9", "1.0-2.9"]:
    lines.append(f"| {band} | {score_dist[band]} |")
lines.append("")

lines.append("## 方法说明与限制")
lines.append("- Pearson/Spearman/Kendall 均在 F48评分与三段累计涨跌交集样本上计算；Spearman 使用并列分数平均秩，Kendall 使用 tau-b tie 修正。")
lines.append("- 分类中性百分位：在每个正式分类目录内按 F48 分数转为0-1百分位后合并；分类去均值残差：F48分数和三段累计收益分别减去本分类均值后再计算相关。")
lines.append("- 三段累计涨跌幅来自本地收益文件的三个SOXX压力窗口简单相加；这不是复利收益，也不是总回报率。")
lines.append("- 风险解释力只代表三个固定SOXX下跌窗口和 2026-06-03 当前IV代理，不能替代逐日最大回撤、真实波动率或完整样本外回测。")
lines.append("- 本次F48评分日期与收益窗口存在时间方向限制：这是当前评分对既有压力窗口表现的解释性评估，不是严格前瞻预测。")
lines.append("")

lines.append("## 最终判断")
lines.append(f"- 对“三段SOXX下跌区间累计涨跌幅”这一目标，F48的核心 Spearman 为 {fmt_num(main_corr['spearman'])}，Top30-Bottom30 为 {fmt_pct(tb30['spread'])}，分类中性 Spearman 为 {fmt_num(neutral_pct_corr['spearman'])}。")
lines.append(f"- 风险端，F48 Top30 相比 Bottom30 的平均最差窗口差值为 {fmt_pct(risk_rows[0]['worst_mean'] - risk_rows[2]['worst_mean']) if risk_rows[0]['worst_mean'] is not None and risk_rows[2]['worst_mean'] is not None else 'N/A'}，当前IV均值差值为 {fmt_pct(risk_rows[0]['iv'] - risk_rows[2]['iv']) if risk_rows[0]['iv'] is not None and risk_rows[2]['iv'] is not None else 'N/A'}。")
lines.append("- 因此，F48更适合作为“压力期质量/防守/非AI包袱过滤”特征使用；若要把它用于收益排序，应与F50价格相对强度、F51交易流动性、估值赔率、财务承压、客户集中和执行风险共同建模，而不宜单因子正向筛选。")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"wrote={OUTPUT_PATH}")
print(f"score_count={len(scores)}")
print(f"return_count={len(returns)}")
print(f"valid_records={len(records)}")
print(f"missing_returns={','.join(return_missing_with_score)}")
print(f"pearson={fmt_num(main_corr['pearson'])} spearman={fmt_num(main_corr['spearman'])} kendall={fmt_num(main_corr['kendall'])}")
print(f"top30={fmt_pct(tb30['top_stats']['mean'])} bottom30={fmt_pct(tb30['bottom_stats']['mean'])} spread={fmt_pct(tb30['spread'])}")
print(f"neutral_spearman={fmt_num(neutral_pct_corr['spearman'])} combined_spearman={fmt_num(robust_rows[-1]['spearman'])}")
