from __future__ import annotations

import math
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median


ROOT = Path(r"D:\drive\Investment\基本面")
FEATURE_ID = "F47"
FEATURE_NAME = "客户集中风险可控性"
FEATURE_KEY = f"{FEATURE_ID}_{FEATURE_NAME}"
DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_KEY}_量化评分_{DATE}.md"
LIQ_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
OUT_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = OUT_DIR / "备份"
OUT_PATH = OUT_DIR / f"{FEATURE_KEY}_特征评估_6个月涨跌_{DATE}.md"

SOXX_WINDOWS = {
    "SOXX跌1": -32.98,
    "SOXX跌2": -15.82,
    "SOXX跌3": -13.40,
}


def split_md_row(line: str) -> list[str] | None:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    return [part.strip() for part in s.strip("|").split("|")]


def is_sep_row(parts: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", p.strip()) for p in parts if p.strip())


def clean_cell(value: object) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def parse_percent(cell: str) -> float | None:
    if not cell or "N/A" in cell or "缺失" in cell:
        return None
    m = re.search(r"([+-]?\d+(?:\.\d+)?)%", cell)
    if not m:
        return None
    return float(m.group(1))


def parse_float(cell: str) -> float | None:
    s = clean_cell(cell).replace(",", "")
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
    if value is None:
        return "N/A"
    return f"{value:.1f}"


def md_escape(value: object) -> str:
    s = clean_cell(value)
    return s.replace("|", "\\|")


def rankdata(values: list[float]) -> list[float]:
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
    n = len(x)
    for i in range(n - 1):
        for j in range(i + 1, n):
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
    if denom == 0:
        return None
    return (c - d) / denom


def correlations(rows: list[dict]) -> dict[str, float | None]:
    x = [r["score"] for r in rows]
    y = [r["ret6"] for r in rows]
    return {
        "pearson": pearson(x, y),
        "spearman": spearman(x, y),
        "kendall": kendall_tau_b(x, y),
    }


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


def parse_returns(path: Path) -> tuple[dict[str, dict], dict[str, dict], dict[str, str]]:
    interval_rows: dict[str, dict] = {}
    risk_rows: dict[str, dict] = {}
    meta: dict[str, str] = {}
    current_category = ""
    mode: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("- 生成时间："):
            meta["generated"] = s.replace("- 生成时间：", "").strip()
        if "最新可得交易日最大值" in s:
            meta["latest"] = s
        if s.startswith("### "):
            current_category = s[4:].strip()
            mode = None
            continue
        parts = split_md_row(line)
        if parts and parts[:9] == ["股票代号", "公司名称", "最新交易日", "最新收盘价", "1个月", "3个月", "6个月", "1年", "备注"]:
            mode = "interval"
            continue
        if parts and len(parts) >= 6 and parts[:2] == ["股票代号", "公司名称"] and "SOXX下跌1" in parts[2]:
            mode = "risk"
            continue
        if mode is None:
            continue
        if parts is None:
            mode = None
            continue
        if is_sep_row(parts):
            continue
        if mode == "interval" and len(parts) >= 9:
            ret6 = parse_percent(parts[6])
            if ret6 is None:
                continue
            ticker = parts[0]
            interval_rows[ticker] = {
                "ticker": ticker,
                "name": parts[1],
                "category": current_category,
                "latest_trade_date": parts[2],
                "latest_close": parse_float(parts[3]),
                "ret1": parse_percent(parts[4]),
                "ret3": parse_percent(parts[5]),
                "ret6": ret6,
                "ret1y": parse_percent(parts[7]),
                "note": parts[8],
            }
        elif mode == "risk" and len(parts) >= 6:
            ticker = parts[0]
            risk_rows[ticker] = {
                "ticker": ticker,
                "w1": parse_percent(parts[2]),
                "w2": parse_percent(parts[3]),
                "w3": parse_percent(parts[4]),
                "note": parts[5],
            }
    return interval_rows, risk_rows, meta


def parse_financial(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    current_category = ""
    header: list[str] | None = None
    idx: dict[str, int] = {}
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("### "):
            current_category = s[4:].strip()
            in_table = False
            header = None
            idx = {}
            continue
        parts = split_md_row(line)
        if parts and len(parts) > 10 and parts[:3] == ["股票代号", "公司名称", "价格日期"] and "Call IV" in parts:
            header = parts
            idx = {name: i for i, name in enumerate(header)}
            in_table = True
            continue
        if not in_table:
            continue
        if parts is None:
            in_table = False
            header = None
            idx = {}
            continue
        if is_sep_row(parts):
            continue
        if not header or len(parts) < len(header):
            continue
        ticker = parts[idx["股票代号"]]
        rows[ticker] = {
            "ticker": ticker,
            "name": parts[idx["公司名称"]],
            "category": current_category,
            "price_date": parts[idx["价格日期"]],
            "call_iv": parse_percent(parts[idx["Call IV"]]),
            "put_iv": parse_percent(parts[idx["Put IV"]]),
            "currency": parts[idx["currency"]],
            "financial_currency": parts[idx["financial_currency"]],
            "listing_type": parts[idx["listing_type"]],
            "valuation_check": parts[idx["估值校验"]],
            "note": parts[idx["备注"]],
        }
    return rows


def top_bottom_metrics(rows: list[dict], n: int, key: str = "score") -> dict[str, float]:
    ordered = sorted(rows, key=lambda r: (-r[key], r["rank"], r["ticker"]))
    top = ordered[:n]
    bottom = ordered[-n:]
    top_avg = mean(r["ret6"] for r in top)
    bottom_avg = mean(r["ret6"] for r in bottom)
    return {
        "top_avg": top_avg,
        "top_hit": mean(1.0 if r["ret6"] > 0 else 0.0 for r in top) * 100,
        "bottom_avg": bottom_avg,
        "bottom_hit": mean(1.0 if r["ret6"] > 0 else 0.0 for r in bottom) * 100,
        "diff": top_avg - bottom_avg,
    }


def split_quintiles(rows: list[dict]) -> list[list[dict]]:
    ordered = sorted(rows, key=lambda r: (-r["score"], r["rank"], r["ticker"]))
    n = len(ordered)
    groups = []
    base = n // 5
    extra = n % 5
    start = 0
    for i in range(5):
        size = base + (1 if i < extra else 0)
        end = start + size
        groups.append(ordered[start:end])
        start = end
    return groups


def risk_group_metrics(group: list[dict]) -> dict[str, float | int | None]:
    window_values = {"w1": [], "w2": [], "w3": []}
    obs = 0
    beat = 0
    neg = 0
    worsts = []
    within_stds = []
    for r in group:
        vals = []
        for key, soxx in zip(["w1", "w2", "w3"], SOXX_WINDOWS.values()):
            val = r.get(key)
            if val is None:
                continue
            window_values[key].append(val)
            vals.append(val)
            obs += 1
            if val > soxx:
                beat += 1
            if val < 0:
                neg += 1
        if vals:
            worsts.append(min(vals))
            if len(vals) > 1:
                m = mean(vals)
                within_stds.append(math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals)))
            else:
                within_stds.append(0.0)
    w_means = {k: (mean(v) if v else None) for k, v in window_values.items()}
    pressure_vals = [v for v in w_means.values() if v is not None]
    return {
        "n": len(group),
        "obs": obs,
        "w1": w_means["w1"],
        "w2": w_means["w2"],
        "w3": w_means["w3"],
        "pressure": mean(pressure_vals) if pressure_vals else None,
        "worst": mean(worsts) if worsts else None,
        "dispersion": mean(within_stds) if within_stds else None,
        "beat": beat / obs * 100 if obs else None,
        "negative": neg / obs * 100 if obs else None,
    }


def iv_metrics(group: list[dict]) -> dict[str, float | int | None]:
    call = [r["call_iv"] for r in group if r.get("call_iv") is not None]
    put = [r["put_iv"] for r in group if r.get("put_iv") is not None]
    both = [(r["call_iv"] + r["put_iv"]) / 2 for r in group if r.get("call_iv") is not None and r.get("put_iv") is not None]
    return {
        "n": len(group),
        "coverage": len(both),
        "call_avg": mean(call) if call else None,
        "put_avg": mean(put) if put else None,
        "near_avg": mean(both) if both else None,
        "near_med": median(both) if both else None,
    }


def subset_eval(rows: list[dict], keep_func) -> tuple[list[dict], dict[str, float | None], dict[str, float]]:
    sub = [r for r in rows if keep_func(r)]
    return sub, correlations(sub), top_bottom_metrics(sub, min(30, len(sub) // 2))


def percentile_by_category(rows: list[dict]) -> None:
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)
    for group in by_cat.values():
        scores = [r["score"] for r in group]
        ranks = rankdata(scores)
        if len(group) == 1:
            pct = [1.0]
        else:
            pct = [(rk - 1) / (len(group) - 1) for rk in ranks]
        score_mean = mean(scores)
        ret_mean = mean(r["ret6"] for r in group)
        for r, p in zip(group, pct):
            r["cat_pct"] = p
            r["score_resid"] = r["score"] - score_mean
            r["ret_resid"] = r["ret6"] - ret_mean


def corr_for_keys(rows: list[dict], x_key: str, y_key: str) -> dict[str, float | None]:
    x = [r[x_key] for r in rows]
    y = [r[y_key] for r in rows]
    return {
        "pearson": pearson(x, y),
        "spearman": spearman(x, y),
        "kendall": kendall_tau_b(x, y),
    }


def md_table(headers: list[str], rows: list[list[object]], aligns: list[str] | None = None) -> str:
    if aligns is None:
        aligns = ["---"] * len(headers)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(aligns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(v) for v in row) + " |")
    return "\n".join(lines)


def company_list(items: list[str], max_len: int = 1200) -> str:
    text = ", ".join(items)
    if len(text) <= max_len:
        return text
    clipped = []
    total = 0
    for item in items:
        if total + len(item) + 2 > max_len:
            break
        clipped.append(item)
        total += len(item) + 2
    return ", ".join(clipped) + f" 等{len(items)}家"


def make_report() -> tuple[str, dict]:
    score = parse_score_file(SCORE_PATH)
    liquidity = parse_score_file(LIQ_PATH)
    returns, risk, ret_meta = parse_returns(RETURN_PATH)
    financial = parse_financial(FIN_PATH)

    all_rows: list[dict] = []
    for ticker, s in score.items():
        if ticker not in returns or returns[ticker].get("ret6") is None:
            continue
        row = dict(s)
        row.update({
            "ret6": returns[ticker]["ret6"],
            "return_name": returns[ticker]["name"],
            "return_category": returns[ticker]["category"],
        })
        row.update(risk.get(ticker, {"w1": None, "w2": None, "w3": None}))
        fin = financial.get(ticker, {})
        row.update({
            "call_iv": fin.get("call_iv"),
            "put_iv": fin.get("put_iv"),
            "currency": fin.get("currency"),
            "financial_currency": fin.get("financial_currency"),
            "listing_type": fin.get("listing_type"),
            "valuation_check": fin.get("valuation_check"),
        })
        row["liq_score"] = liquidity.get(ticker, {}).get("score")
        all_rows.append(row)

    all_rows.sort(key=lambda r: (-r["score"], r["rank"], r["ticker"]))
    percentile_by_category(all_rows)

    score_missing_returns = sorted(set(score) - set(returns))
    returns_missing_score = sorted(set(returns) - set(score))
    base_corr = correlations(all_rows)
    tb = {n: top_bottom_metrics(all_rows, n) for n in [10, 20, 30]}

    quintile_rows = []
    for i, group in enumerate(split_quintiles(all_rows), start=1):
        label = "Q1最高分" if i == 1 else ("Q5最低分" if i == 5 else f"Q{i}")
        quintile_rows.append([
            label,
            len(group),
            fmt_score(mean(r["score"] for r in group)),
            fmt_pct(mean(r["ret6"] for r in group)),
            fmt_pct(median(r["ret6"] for r in group)),
            fmt_pct(mean(1.0 if r["ret6"] > 0 else 0.0 for r in group) * 100, 1),
        ])

    ordered = all_rows
    mid_start = max(0, len(ordered) // 2 - 15)
    groups = {
        "F47 Top30": ordered[:30],
        "F47 Mid30": ordered[mid_start:mid_start + 30],
        "F47 Bottom30": ordered[-30:],
    }
    risk_metrics = {name: risk_group_metrics(group) for name, group in groups.items()}
    iv_group_metrics = {name: iv_metrics(group) for name, group in groups.items()}

    by_cat: dict[str, list[dict]] = defaultdict(list)
    for r in all_rows:
        by_cat[r["category"]].append(r)
    category_distribution = []
    cat_corr_rows = []
    for cat in sorted(by_cat):
        group = by_cat[cat]
        c = correlations(group)
        top_ret = max(group, key=lambda r: r["ret6"])
        top_score = sorted(group, key=lambda r: (-r["score"], r["rank"], r["ticker"]))[0]
        category_distribution.append([
            cat,
            len(group),
            fmt_score(mean(r["score"] for r in group)),
            fmt_pct(mean(r["ret6"] for r in group)),
            fmt_pct(median(r["ret6"] for r in group)),
        ])
        cat_corr_rows.append([
            cat,
            len(group),
            fmt_num(c["pearson"]),
            fmt_num(c["spearman"]),
            fmt_pct(mean(r["ret6"] for r in group)),
            f"{top_ret['ticker']} {fmt_pct(top_ret['ret6'])}",
            f"{top_score['ticker']} {fmt_score(top_score['score'])} / {fmt_pct(top_score['ret6'])}",
        ])

    neutral_pct_corr = corr_for_keys(all_rows, "cat_pct", "ret6")
    neutral_resid_corr = corr_for_keys(all_rows, "score_resid", "ret_resid")
    neutral_ordered = sorted(all_rows, key=lambda r: (-r["cat_pct"], r["rank"], r["ticker"]))
    neutral_rows = []
    for n in [10, 20, 30]:
        top = neutral_ordered[:n]
        bottom = neutral_ordered[-n:]
        top_avg = mean(r["ret6"] for r in top)
        bottom_avg = mean(r["ret6"] for r in bottom)
        neutral_rows.append([
            f"中性Top{n}/Bottom{n}",
            fmt_pct(top_avg),
            fmt_pct(mean(1.0 if r["ret6"] > 0 else 0.0 for r in top) * 100, 1),
            fmt_pct(bottom_avg),
            fmt_pct(mean(1.0 if r["ret6"] > 0 else 0.0 for r in bottom) * 100, 1),
            fmt_pct(top_avg - bottom_avg),
        ])

    rets = sorted(r["ret6"] for r in all_rows)
    # NumPy's default linear quantile is reproduced to keep the threshold stable without a dependency.
    def quantile(vals: list[float], q: float) -> float:
        pos = (len(vals) - 1) * q
        lo = math.floor(pos)
        hi = math.ceil(pos)
        if lo == hi:
            return vals[lo]
        return vals[lo] * (hi - pos) + vals[hi] * (pos - lo)

    low_q = quantile(rets, 0.05)
    high_q = quantile(rets, 0.95)

    low_liq_names = sorted(r["ticker"] for r in all_rows if r.get("liq_score") is not None and r["liq_score"] <= 5.0)

    def is_currency_clean(r: dict) -> bool:
        listing = clean_cell(r.get("listing_type"))
        cur = clean_cell(r.get("currency"))
        fcur = clean_cell(r.get("financial_currency"))
        check = clean_cell(r.get("valuation_check"))
        if "ADR/ADS" in listing:
            return False
        if cur and fcur and cur != fcur:
            return False
        if "currency_mismatch" in check:
            return False
        return True

    adr_names = sorted(r["ticker"] for r in all_rows if not is_currency_clean(r))
    extreme_names = sorted(r["ticker"] for r in all_rows if r["ret6"] < low_q or r["ret6"] > high_q)

    robustness_specs = [
        ("全样本基准", "无剔除", lambda r: True),
        ("剔除低流动性", "F51交易流动性分 > 5.0", lambda r: r.get("liq_score") is None or r["liq_score"] > 5.0),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", is_currency_clean),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(low_q)} / {fmt_pct(high_q)}", lambda r: low_q <= r["ret6"] <= high_q),
        ("三项合并剔除", "同时满足上述三项", lambda r: (r.get("liq_score") is None or r["liq_score"] > 5.0) and is_currency_clean(r) and low_q <= r["ret6"] <= high_q),
    ]
    robustness_rows = []
    robustness_detail = {}
    for name, rule, func in robustness_specs:
        sub, c, tb30 = subset_eval(all_rows, func)
        robustness_detail[name] = (sub, c, tb30)
        robustness_rows.append([
            name,
            rule,
            len(sub),
            len(all_rows) - len(sub),
            fmt_num(c["pearson"]),
            fmt_num(c["spearman"]),
            fmt_num(c["kendall"]),
            fmt_pct(tb30["top_avg"]),
            fmt_pct(tb30["bottom_avg"]),
            fmt_pct(tb30["diff"]),
        ])

    top_ret15 = sorted(all_rows, key=lambda r: r["ret6"], reverse=True)[:15]
    bottom_ret10 = sorted(all_rows, key=lambda r: r["ret6"])[:10]
    top_score15 = ordered[:15]
    bottom_score15 = ordered[-15:]

    def top_bottom_company_rows(top: list[dict], group_name: str, score_label: str = "F47分") -> list[list[object]]:
        return [[
            group_name,
            r["ticker"],
            r["name"],
            r["category"],
            fmt_score(r["score"]),
            r["rank"],
            fmt_pct(r["ret6"]),
            r["confidence"],
        ] for r in top]

    tb_company_rows = top_bottom_company_rows(ordered[:10], "Top10") + top_bottom_company_rows(ordered[-10:], "Bottom10")

    def pressure_avg(r: dict) -> float | None:
        vals = [r.get(k) for k in ["w1", "w2", "w3"] if r.get(k) is not None]
        return mean(vals) if vals else None

    def near_iv(r: dict) -> float | None:
        if r.get("call_iv") is not None and r.get("put_iv") is not None:
            return (r["call_iv"] + r["put_iv"]) / 2
        return None

    top_score_rows = []
    for r in top_score15:
        top_score_rows.append([
            r["rank"], r["ticker"], r["name"], r["category"], fmt_score(r["score"]),
            fmt_pct(r["ret6"]), fmt_pct(pressure_avg(r)), fmt_pct(near_iv(r))
        ])
    bottom_score_rows = []
    for r in reversed(bottom_score15):
        bottom_score_rows.append([
            r["rank"], r["ticker"], r["name"], r["category"], fmt_score(r["score"]),
            fmt_pct(r["ret6"]), fmt_pct(pressure_avg(r)), fmt_pct(near_iv(r))
        ])

    def ret_diag_rows(rows: list[dict]) -> list[list[object]]:
        return [[
            r["ticker"], r["name"], r["category"], fmt_pct(r["ret6"]),
            fmt_score(r["score"]), r["rank"], r["confidence"],
        ] for r in rows]

    dist_counter = Counter()
    for r in score.values():
        s = r["score"]
        if s >= 9:
            dist_counter["9.0-10.0"] += 1
        elif s >= 8:
            dist_counter["8.0-8.9"] += 1
        elif s >= 7:
            dist_counter["7.0-7.9"] += 1
        elif s >= 5:
            dist_counter["5.0-6.9"] += 1
        elif s >= 3:
            dist_counter["3.0-4.9"] += 1
        else:
            dist_counter["1.0-2.9"] += 1
    dist_rows = [[k, dist_counter[k]] for k in ["9.0-10.0", "8.0-8.9", "7.0-7.9", "5.0-6.9", "3.0-4.9", "1.0-2.9"]]

    conclusion_strength = "不成立"
    if base_corr["spearman"] is not None:
        if base_corr["spearman"] >= 0.3:
            conclusion_strength = "成立，且强度中等以上"
        elif base_corr["spearman"] >= 0.1:
            conclusion_strength = "弱成立"
        elif base_corr["spearman"] > -0.1:
            conclusion_strength = "接近无效"
        else:
            conclusion_strength = "反向"

    tb30 = tb[30]
    risk_top = risk_metrics["F47 Top30"]
    risk_bottom = risk_metrics["F47 Bottom30"]
    iv_top = iv_group_metrics["F47 Top30"]
    iv_bottom = iv_group_metrics["F47 Bottom30"]
    combined_c = robustness_detail["三项合并剔除"][1]
    combined_tb = robustness_detail["三项合并剔除"][2]

    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 6个月涨跌 {DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.extend([
        f"- 评估对象：`{FEATURE_KEY}`。",
        f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 {DATE}，覆盖 {len(score)} 家。",
        f"- 收益输入：`日度资料/区间涨跌/{RETURN_PATH.name}`，生成时间 {ret_meta.get('generated', 'N/A').rstrip('。')}，价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。",
        "- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。",
        "- 稳健性辅助输入：`特征量化/量化评分/F51_交易流动性_量化评分_2026-06-04.md`；`日度资料/每日金融数据/每日金融数据_2026-06-03.md`，金融数据生成时间 2026-06-03 13:41:46 PDT-0700。",
        f"- 有效评估样本：评分与6个月涨跌交集 {len(all_rows)} 家；F47评分有但6个月涨跌缺失 {len(score_missing_returns)} 家。",
        "- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。",
        "- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动率或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为下跌窗口代理，并用2026-06-03近ATM Call/Put IV均值补充当前波动代理。",
        "- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。",
        "- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F47 正式输出；本次未读取旧版 F47 特征评估作为结论依据。",
        "- 时间限制：F47评分日期为2026-06-04，收益窗口截至2026-05-27；本报告是当前评分对既有6个月股价表现的解释性评估，不是严格前瞻回测。",
    ])
    lines.append("")
    lines.append("## 结论摘要")
    lines.extend([
        f"- 排序有效性：{conclusion_strength}。全样本 Pearson {fmt_num(base_corr['pearson'])}, Spearman {fmt_num(base_corr['spearman'])}, Kendall {fmt_num(base_corr['kendall'])}；重点指标 Spearman {fmt_num(base_corr['spearman'])}。",
        f"- Top/Bottom能力：Top10、Top20、Top30 平均收益分别为 {fmt_pct(tb[10]['top_avg'])}、{fmt_pct(tb[20]['top_avg'])}、{fmt_pct(tb[30]['top_avg'])}；Top-Bottom收益差分别为 {fmt_pct(tb[10]['diff'])}、{fmt_pct(tb[20]['diff'])}、{fmt_pct(tb[30]['diff'])}。",
        f"- 风险解释力：Top30 压力窗口均值 {fmt_pct(risk_top['pressure'])}，Bottom30 为 {fmt_pct(risk_bottom['pressure'])}；Top30 平均最差窗口 {fmt_pct(risk_top['worst'])}，Bottom30 为 {fmt_pct(risk_bottom['worst'])}；Top30 近ATM IV均值 {fmt_pct(iv_top['near_avg'])}，Bottom30 为 {fmt_pct(iv_bottom['near_avg'])}。",
        f"- 分类中性：分类内百分位合并 Spearman {fmt_num(neutral_pct_corr['spearman'])}，分类去均值残差 Spearman {fmt_num(neutral_resid_corr['spearman'])}；中性Top30-Bottom30 {neutral_rows[2][-1]}。",
        f"- 稳健性：三项合并剔除后样本 {len(robustness_detail['三项合并剔除'][0])} 家，Spearman {fmt_num(combined_c['spearman'])}，Top30-Bottom30 {fmt_pct(combined_tb['diff'])}。",
        "- 解释：F47 衡量客户集中风险是否可控，高分端偏向客户分散、RPO/backlog/长期合同、受监管负荷或客户认证较强的公司；低分端偏向单一客户、单一项目、NeoCloud/预商业化项目、可取消 PO 或平台/融资/监管节点高度集中的公司。若高分组合收益不强但压力窗口和 IV 更稳，F47 更适合作为质量/风险过滤；若收益排序也为正，则可作为风险调整收益因子加入组合。",
    ])
    lines.append("")
    lines.append("## 覆盖检查")
    lines.append(md_table(
        ["项目", "数量", "说明"],
        [
            ["F47评分覆盖", len(score), "来自2026-06-04评分文件"],
            ["6个月涨跌覆盖", len(returns), "来自2026-05-27区间涨跌文件"],
            ["交集样本", len(all_rows), "用于本次所有主指标"],
            ["评分有但6个月涨跌缺失", len(score_missing_returns), company_list(score_missing_returns) if score_missing_returns else "无"],
            ["涨跌有但评分缺失", len(returns_missing_score), company_list(returns_missing_score) if returns_missing_score else "无"],
        ],
        ["---", "---:", "---"],
    ))
    lines.append("")
    lines.append("### 交集样本分类分布")
    lines.append(md_table(["分类目录", "样本数", "F47均分", "6个月平均收益", "6个月中位收益"], category_distribution, ["---", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## 排序有效性")
    lines.append(md_table(
        ["指标", "数值", "解释"],
        [
            ["Pearson", fmt_num(base_corr["pearson"]), "线性相关；受极端涨跌影响较大"],
            ["Spearman", fmt_num(base_corr["spearman"]), "排序相关；这是本任务最重要指标"],
            ["Kendall tau-b", fmt_num(base_corr["kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
        ],
        ["---", "---:", "---"],
    ))
    lines.append("")
    lines.append("### 分数分组收益")
    lines.append(md_table(["分组", "公司数", "F47均分", "6个月平均收益", "6个月中位收益", "命中率"], quintile_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## Top/Bottom能力")
    lines.append(md_table(
        ["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"],
        [[f"Top{n}/Bottom{n}", fmt_pct(tb[n]["top_avg"]), fmt_pct(tb[n]["top_hit"], 1), fmt_pct(tb[n]["bottom_avg"]), fmt_pct(tb[n]["bottom_hit"], 1), fmt_pct(tb[n]["diff"])] for n in [10, 20, 30]],
        ["---", "---:", "---:", "---:", "---:", "---:"],
    ))
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    lines.append(md_table(["组别", "股票代号", "公司名称", "分类目录", "F47分", "F47排名", "6个月收益", "置信度"], tb_company_rows, ["---", "---", "---", "---", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为下跌窗口代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供；近ATM IV为2026-06-03当前期权波动代理，不等同于过去6个月实际波动率。")
    lines.append(md_table(
        ["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"],
        [[name, m["n"], m["obs"], fmt_pct(m["w1"]), fmt_pct(m["w2"]), fmt_pct(m["w3"]), fmt_pct(m["pressure"]), fmt_pct(m["worst"]), fmt_pct(m["dispersion"]), fmt_pct(m["beat"], 1), fmt_pct(m["negative"], 1)] for name, m in risk_metrics.items()],
        ["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
    ))
    lines.append("")
    lines.append("### 当前IV代理")
    lines.append(md_table(
        ["分组", "公司数", "IV覆盖", "Call IV均值", "Put IV均值", "近ATM IV均值", "近ATM IV中位数"],
        [[name, m["n"], m["coverage"], fmt_pct(m["call_avg"]), fmt_pct(m["put_avg"]), fmt_pct(m["near_avg"]), fmt_pct(m["near_med"])] for name, m in iv_group_metrics.items()],
        ["---", "---:", "---:", "---:", "---:", "---:", "---:"],
    ))
    lines.append("")
    lines.append("结论：如果高分组压力窗口均值、平均最差窗口和近ATM IV低于低分组，说明 F47 的风险可控性含义得到价格侧支持；如果收益排序为负但风险代理改善，则该特征应作为风险过滤而非单独收益排序。")
    lines.append("")
    lines.append("## 分类中性结果")
    lines.append(md_table(
        ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
        [
            ["原始全样本", len(all_rows), fmt_num(base_corr["pearson"]), fmt_num(base_corr["spearman"]), fmt_num(base_corr["kendall"]), "直接用F47分数排序"],
            ["分类内百分位合并", len(all_rows), fmt_num(neutral_pct_corr["pearson"]), fmt_num(neutral_pct_corr["spearman"]), fmt_num(neutral_pct_corr["kendall"]), "每个分类内先按F47排序，再转成0-1百分位后合并"],
            ["分类去均值残差", len(all_rows), fmt_num(neutral_resid_corr["pearson"]), fmt_num(neutral_resid_corr["spearman"]), fmt_num(neutral_resid_corr["kendall"]), "F47和收益分别减去分类均值后相关"],
        ],
        ["---", "---:", "---:", "---:", "---:", "---"],
    ))
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    lines.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], neutral_rows, ["---", "---:", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    lines.append(md_table(["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F47公司"], cat_corr_rows, ["---", "---:", "---:", "---:", "---:", "---", "---"]))
    lines.append("")
    lines.append("分类内结果用于检验是否只是押中某个分类目录。若分类内 Spearman 多数为负或中性化Top/Bottom转弱，说明该特征更偏跨行业质量/防守，不适合单独承担6个月收益排序。")
    lines.append("")
    lines.append("## 稳健性检验")
    lines.append(md_table(
        ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"],
        robustness_rows,
        ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"],
    ))
    lines.append("")
    lines.append("稳健性结论：若三项合并剔除后 Spearman 和 Top30-Bottom30仍维持同向，说明结果不主要依赖低流动性、ADR/币种口径或极端涨跌样本；若方向反转，应降低 F47 在收益排序中的权重，只保留风险约束用途。")
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(md_table(
        ["剔除项", "数量", "公司"],
        [
            ["低流动性", len(low_liq_names), company_list(low_liq_names)],
            ["ADR/币种异常", len(adr_names), company_list(adr_names)],
            ["极端涨跌双尾5%", len(extreme_names), company_list(extreme_names)],
        ],
        ["---", "---:", "---"],
    ))
    lines.append("")
    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "6个月收益", "F47分", "F47排名", "F47置信度"], ret_diag_rows(top_ret15), ["---", "---", "---", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### 6个月跌幅前10")
    lines.append(md_table(["股票代号", "公司名称", "分类目录", "6个月收益", "F47分", "F47排名", "F47置信度"], ret_diag_rows(bottom_ret10), ["---", "---", "---", "---:", "---:", "---:", "---"]))
    lines.append("")
    lines.append("### F47高分前15")
    lines.append(md_table(["排名", "股票代号", "公司名称", "分类目录", "F47分", "6个月收益", "压力窗口均值", "近ATM IV"], top_score_rows, ["---:", "---", "---", "---", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("### F47低分前15")
    lines.append(md_table(["排名", "股票代号", "公司名称", "分类目录", "F47分", "6个月收益", "压力窗口均值", "近ATM IV"], bottom_score_rows, ["---:", "---", "---", "---", "---:", "---:", "---:", "---:"]))
    lines.append("")
    lines.append("## 分数分布与解释")
    lines.append(md_table(["分数段", "公司数"], dist_rows, ["---", "---:"]))
    lines.append("")
    lines.append("F47 的高分多来自客户分散、长期合同/RPO/backlog、监管机制、客户认证和切换成本；低分多来自单一客户/项目、PO或forecast可取消、融资/监管/许可节点未落地、pre-commercial pipeline 或平台依赖。该信息天然偏风险质量，不保证在6个月窗口中跑赢高弹性、低基数、题材驱动或困境反转公司。")
    lines.append("")
    lines.append("## 使用建议")
    if base_corr["spearman"] is not None and base_corr["spearman"] > 0.1 and combined_c["spearman"] is not None and combined_c["spearman"] > 0.1:
        lines.extend([
            "- 可以把 F47 作为弱到中等权重的风险调整收益因子；全样本和稳健性样本均保留正向排序时，说明客户集中风险可控性不仅是防守标签，也对6个月收益有一定解释。",
            "- 更稳妥的组合用法是与上行弹性、估值赔率、催化剂强度和交易流动性联用：优先选择高 F47 且同时具备上修空间的公司，避免只买低波动成熟公司。",
            "- 对低分但涨幅极高公司，应复核是否是低基数困境反转、融资/客户新增或题材重估；这些公司可以贡献收益，但需要额外止损和事件核验。",
        ])
    elif base_corr["spearman"] is not None and base_corr["spearman"] < -0.1:
        lines.extend([
            "- 不建议把 F47 单独用作6个月收益排序因子；本窗口高客户集中风险样本反而更容易获得高弹性收益。",
            "- 更合理的用途是风险过滤：在上行弹性或催化剂筛选后，用 F47 排除客户/项目/融资高度集中的公司，或要求更高估值折扣。",
            "- 若高分组压力窗口和IV显著更稳，F47仍可作为防守型质量因子；但收益目标需要依赖其他进攻因子补足。",
        ])
    else:
        lines.extend([
            "- 不建议赋予 F47 单因子过高收益排序权重；当前 Spearman 接近中性或仅弱信号，说明客户集中风险可控性不是本窗口的主导涨跌变量。",
            "- 更合理的用途是组合风险约束：在高弹性、高催化剂或低估值公司中，优先保留 F47 较高、客户/项目取消风险更可控的标的。",
            "- 对 F47 低分但涨幅靠前的公司，应单独跟踪客户占比、binding合同、预付款、融资条件和验收节点，因为收益弹性通常伴随更高尾部回撤和更高IV。",
        ])
    lines.append("")
    lines.append("## 数据与方法限制")
    lines.extend([
        "- 收益文件使用 Yahoo Finance 免费历史行情的 Close 价格，`auto_adjust=False`，不含股息再投资，不是总回报率。",
        "- 6个月收益窗口的最新价格日为 2026-05-27；评分日期为 2026-06-04，存在评分信息相对收益窗口滞后的偏差，结论更接近“截至评分时的特征与过去6个月收益关系”，不是严格前瞻回测。",
        "- 风险部分没有逐日收益序列，因此不能给出严格日波动率、最大回撤或下跌日胜率；本报告以三个 SOXX 下跌窗口和 2026-06-03 当前 IV 作为代理。",
        "- 流动性剔除依赖 F51 代理评分，不等同于真实成交额/ADV；ADR/币种异常剔除依据日度金融数据中的 listing_type、currency、financial_currency 和估值校验备注。",
        f"- 极端涨跌剔除使用交集样本6个月收益的双尾5%分位，阈值为 {fmt_pct(low_q)} / {fmt_pct(high_q)}。",
    ])
    lines.append("")

    summary = {
        "score_count": len(score),
        "return_count": len(returns),
        "intersection": len(all_rows),
        "missing_returns": score_missing_returns,
        "base_corr": base_corr,
        "top30": tb[30],
        "risk_top": risk_top,
        "risk_bottom": risk_bottom,
        "iv_top": iv_top,
        "iv_bottom": iv_bottom,
        "combined_corr": combined_c,
        "combined_tb": combined_tb,
        "low_liq_count": len(low_liq_names),
        "adr_count": len(adr_names),
        "extreme_count": len(extreme_names),
        "low_q": low_q,
        "high_q": high_q,
    }
    return "\n".join(lines), summary


def backup_existing() -> list[str]:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    for path in OUT_DIR.glob(f"{FEATURE_KEY}_特征评估_6个月涨跌_*.md"):
        if path.is_file():
            dest_dir = BACKUP_DIR / f"{FEATURE_KEY}_6个月涨跌_写入前备份_{stamp}"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / path.name
            shutil.move(str(path), str(dest))
            moved.append(str(dest.relative_to(ROOT)))
    return moved


def main() -> None:
    report, summary = make_report()
    moved = backup_existing()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(f"wrote={OUT_PATH}")
    print(f"backup_moved={len(moved)}")
    for item in moved:
        print(f"backup={item}")
    print(f"score_count={summary['score_count']} return_count={summary['return_count']} intersection={summary['intersection']}")
    print(f"missing_returns={','.join(summary['missing_returns'])}")
    print("base_corr=" + ",".join(f"{k}:{fmt_num(v)}" for k, v in summary["base_corr"].items()))
    print("top30=" + ",".join(f"{k}:{fmt_pct(v) if 'avg' in k or k == 'diff' else fmt_pct(v, 1)}" for k, v in summary["top30"].items()))
    print(f"risk_top_pressure={fmt_pct(summary['risk_top']['pressure'])} risk_bottom_pressure={fmt_pct(summary['risk_bottom']['pressure'])}")
    print(f"iv_top={fmt_pct(summary['iv_top']['near_avg'])} iv_bottom={fmt_pct(summary['iv_bottom']['near_avg'])}")
    print("combined_corr=" + ",".join(f"{k}:{fmt_num(v)}" for k, v in summary["combined_corr"].items()))
    print(f"combined_top30_diff={fmt_pct(summary['combined_tb']['diff'])}")
    print(f"robust_counts low_liq={summary['low_liq_count']} adr={summary['adr_count']} extreme={summary['extreme_count']} thresholds={fmt_pct(summary['low_q'])}/{fmt_pct(summary['high_q'])}")


if __name__ == "__main__":
    main()
