from __future__ import annotations

import math
import re
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
FEATURE_ID = "F22"
FEATURE_NAME = "技术稀缺与复制难度"
FEATURE_SUBJECT = f"{FEATURE_ID}_{FEATURE_NAME}"
RUN_DATE = "2026-06-04"
RETURN_WINDOW = "6个月"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_SUBJECT}_量化评分_{RUN_DATE}.md"
F51_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
EVAL_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = EVAL_DIR / "备份"
OUTPUT_PATH = EVAL_DIR / f"{FEATURE_SUBJECT}_特征评估_{RETURN_WINDOW}涨跌_{RUN_DATE}.md"

SOXX_WINDOWS = {
    "SOXX下跌1": -32.98,
    "SOXX下跌2": -15.82,
    "SOXX下跌3": -13.40,
}


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def split_md_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    if stripped.endswith("|"):
        stripped = stripped[1:-1]
    else:
        stripped = stripped[1:]
    return [cell.strip() for cell in stripped.split("|")]


def is_separator(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def parse_float(text: str) -> float | None:
    text = text.strip()
    if not text or text in {"N/A", "NA", "缺失", "不适用"}:
        return None
    text = text.replace(",", "")
    m = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(m.group(0)) if m else None


def parse_return_percent(cell: str) -> float | None:
    if not cell or "N/A" in cell:
        return None
    m = re.search(r"([+-]?\d+(?:\.\d+)?)%", cell.replace(",", ""))
    return float(m.group(1)) if m else None


def clean_cell(cell: str) -> str:
    return cell.replace("<br>", "；").strip()


def parse_score_table(path: Path) -> list[dict]:
    headers = [
        "排名",
        "股票代号",
        "公司名称",
        "分类目录",
        "特征分",
        "证据等级",
        "置信度",
        "核心证据",
        "缺失/降权",
        "后续核验",
    ]
    rows: list[dict] = []
    in_table = False
    for line in read_lines(path):
        cells = split_md_row(line)
        if cells and cells[: len(headers)] == headers:
            in_table = True
            continue
        if not in_table:
            continue
        if cells is None:
            break
        if is_separator(cells):
            continue
        if len(cells) < len(headers):
            continue
        row = dict(zip(headers, cells[: len(headers)]))
        rank = parse_float(row["排名"])
        score = parse_float(row["特征分"])
        if rank is None or score is None:
            continue
        rows.append(
            {
                "ticker": row["股票代号"],
                "name": row["公司名称"],
                "category": row["分类目录"],
                "score": score,
                "rank": int(rank),
                "evidence": row["证据等级"],
                "confidence": row["置信度"],
                "core": row["核心证据"],
                "downgrade": row["缺失/降权"],
                "verify": row["后续核验"],
            }
        )
    return rows


def parse_price_file(path: Path) -> tuple[dict[str, dict], dict[str, dict]]:
    returns: dict[str, dict] = {}
    stress: dict[str, dict] = {}
    mode: str | None = None
    category: str | None = None
    headers: list[str] | None = None

    for line in read_lines(path):
        if line.startswith("### 按分类分组的全公司明细"):
            mode = "stress"
            category = None
            headers = None
            continue
        if line.startswith("## 按分类分组的公司明细"):
            mode = "returns"
            category = None
            headers = None
            continue
        if mode == "stress" and line.startswith("## ") and not line.startswith("### "):
            headers = None
        if mode == "stress" and line.startswith("#### "):
            category = line.replace("#### ", "").strip()
            headers = None
            continue
        if mode == "returns" and line.startswith("### "):
            category = line.replace("### ", "").strip()
            headers = None
            continue

        cells = split_md_row(line)
        if cells is None:
            headers = None
            continue
        if is_separator(cells):
            continue
        if cells and cells[0] == "股票代号":
            headers = cells
            continue
        if not headers or not category or len(cells) < len(headers):
            continue
        row = dict(zip(headers, cells[: len(headers)]))
        ticker = row.get("股票代号", "").strip()
        if not ticker:
            continue
        if mode == "returns" and "6个月" in row:
            returns[ticker] = {
                "ticker": ticker,
                "name_return": row.get("公司名称", ""),
                "category_return": category,
                "latest_trade_date": row.get("最新交易日", ""),
                "ret_1m": parse_return_percent(row.get("1个月", "")),
                "ret_3m": parse_return_percent(row.get("3个月", "")),
                "ret_6m": parse_return_percent(row.get("6个月", "")),
                "ret_1y": parse_return_percent(row.get("1年", "")),
                "return_note": clean_cell(row.get("备注", "")),
            }
        elif mode == "stress":
            stress[ticker] = {
                "ticker": ticker,
                "name_stress": row.get("公司名称", ""),
                "category_stress": category,
                "soxx1": parse_return_percent(row.get("SOXX下跌1 2025-02-20至2025-04-08", "")),
                "soxx2": parse_return_percent(row.get("SOXX下跌2 2026-02-25至2026-03-30", "")),
                "soxx3": parse_return_percent(row.get("SOXX下跌3 2025-10-29至2025-11-20", "")),
                "stress_note": clean_cell(row.get("备注", "")),
            }
    return returns, stress


def parse_financial_file(path: Path) -> dict[str, dict]:
    financial: dict[str, dict] = {}
    in_details = False
    category: str | None = None
    headers: list[str] | None = None
    for line in read_lines(path):
        if line.startswith("## 按项目分类分组的公司明细表"):
            in_details = True
            headers = None
            continue
        if not in_details:
            continue
        if line.startswith("### "):
            category = line.replace("### ", "").strip()
            headers = None
            continue
        cells = split_md_row(line)
        if cells is None:
            headers = None
            continue
        if is_separator(cells):
            continue
        if cells and cells[0] == "股票代号" and "listing_type" in cells:
            headers = cells
            continue
        if not headers or not category or len(cells) < len(headers):
            continue
        row = dict(zip(headers, cells[: len(headers)]))
        ticker = row.get("股票代号", "").strip()
        if not ticker:
            continue
        financial[ticker] = {
            "ticker": ticker,
            "name_fin": row.get("公司名称", ""),
            "category_fin": category,
            "listing_type": row.get("listing_type", ""),
            "adr_ratio": row.get("adr_ratio", ""),
            "currency": row.get("currency", ""),
            "financial_currency": row.get("financial_currency", ""),
            "valuation_check": row.get("估值校验", ""),
            "fin_note": clean_cell(row.get("备注", "")),
        }
    return financial


def mean(values: list[float]) -> float:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    return sum(vals) / len(vals) if vals else math.nan


def median(values: list[float]) -> float:
    vals = sorted(v for v in values if v is not None and not math.isnan(v))
    if not vals:
        return math.nan
    n = len(vals)
    mid = n // 2
    if n % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2


def std_sample(values: list[float]) -> float:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    if len(vals) < 2:
        return math.nan
    m = mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


def ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    out = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            out[indexed[k][0]] = avg_rank
        i = j
    return out


def pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        return math.nan
    mx = mean(x)
    my = mean(y)
    sx = math.sqrt(sum((v - mx) ** 2 for v in x))
    sy = math.sqrt(sum((v - my) ** 2 for v in y))
    if sx == 0 or sy == 0:
        return math.nan
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def spearman(x: list[float], y: list[float]) -> float:
    return pearson(ranks(x), ranks(y))


def kendall_tau_b(x: list[float], y: list[float]) -> float:
    c = d = tx = ty = 0
    n = len(x)
    for i in range(n):
        for j in range(i + 1, n):
            dx = 0 if x[i] == x[j] else (1 if x[i] > x[j] else -1)
            dy = 0 if y[i] == y[j] else (1 if y[i] > y[j] else -1)
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
    return (c - d) / denom if denom else math.nan


def corr_metrics(rows: list[dict], x_key: str = "score", y_key: str = "ret_6m") -> dict[str, float]:
    pairs = [(r[x_key], r[y_key]) for r in rows if r.get(x_key) is not None and r.get(y_key) is not None]
    x = [p[0] for p in pairs]
    y = [p[1] for p in pairs]
    return {
        "n": len(pairs),
        "pearson": pearson(x, y),
        "spearman": spearman(x, y),
        "kendall": kendall_tau_b(x, y),
    }


def sort_top(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: (r["rank"], -r["score"], r["ticker"]))


def sort_bottom(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: (-r["rank"], r["score"], r["ticker"]))


def hit_rate(rows: list[dict]) -> float:
    valid = [r for r in rows if r.get("ret_6m") is not None]
    return sum(1 for r in valid if r["ret_6m"] > 0) / len(valid) * 100 if valid else math.nan


def portfolio_stats(top_rows: list[dict], bottom_rows: list[dict]) -> dict[str, float]:
    top_mean = mean([r["ret_6m"] for r in top_rows])
    bottom_mean = mean([r["ret_6m"] for r in bottom_rows])
    return {
        "top_mean": top_mean,
        "top_hit": hit_rate(top_rows),
        "bottom_mean": bottom_mean,
        "bottom_hit": hit_rate(bottom_rows),
        "diff": top_mean - bottom_mean,
    }


def top_bottom_table(rows: list[dict], key: str = "rank") -> dict[int, dict[str, float]]:
    if key == "neutral_pct":
        ordered_top = sorted(rows, key=lambda r: (-r["neutral_pct"], r["rank"], r["ticker"]))
        ordered_bottom = sorted(rows, key=lambda r: (r["neutral_pct"], -r["rank"], r["ticker"]))
    else:
        ordered_top = sort_top(rows)
        ordered_bottom = sort_bottom(rows)
    out: dict[int, dict[str, float]] = {}
    for n in (10, 20, 30):
        out[n] = portfolio_stats(ordered_top[:n], ordered_bottom[:n])
    return out


def array_chunks(values: list[dict], k: int) -> list[list[dict]]:
    n = len(values)
    chunks = []
    start = 0
    for i in range(k):
        end = round((i + 1) * n / k)
        chunks.append(values[start:end])
        start = end
    return chunks


def percentile_by_category(rows: list[dict]) -> None:
    by_cat: dict[str, list[dict]] = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)
    for cat_rows in by_cat.values():
        vals = [r["score"] for r in cat_rows]
        rs = ranks(vals)
        n = len(cat_rows)
        for r, rank_val in zip(cat_rows, rs):
            r["neutral_pct"] = rank_val / n if n else math.nan
        score_mean = mean(vals)
        ret_mean = mean([r["ret_6m"] for r in cat_rows])
        for r in cat_rows:
            r["score_resid"] = r["score"] - score_mean
            r["return_resid"] = r["ret_6m"] - ret_mean


def risk_stats(label: str, rows: list[dict]) -> dict:
    windows = ["soxx1", "soxx2", "soxx3"]
    window_means = {w: mean([r[w] for r in rows if r.get(w) is not None]) for w in windows}
    all_obs = []
    outperform = 0
    obs = 0
    neg = 0
    worst_by_company = []
    for r in rows:
        vals = []
        for w, soxx_label in zip(windows, SOXX_WINDOWS.keys()):
            v = r.get(w)
            if v is None:
                continue
            vals.append(v)
            all_obs.append(v)
            obs += 1
            if v > SOXX_WINDOWS[soxx_label]:
                outperform += 1
            if v < 0:
                neg += 1
        if vals:
            worst_by_company.append(min(vals))
    return {
        "group": label,
        "count": len(rows),
        "obs": obs,
        "soxx1": window_means["soxx1"],
        "soxx2": window_means["soxx2"],
        "soxx3": window_means["soxx3"],
        "stress_mean": mean(all_obs),
        "avg_worst": mean(worst_by_company),
        "dispersion": std_sample(all_obs),
        "outperform": outperform / obs * 100 if obs else math.nan,
        "neg_ratio": neg / obs * 100 if obs else math.nan,
    }


def is_adr_or_currency_abnormal(row: dict) -> bool:
    listing = (row.get("listing_type") or "").upper()
    adr_ratio = (row.get("adr_ratio") or "").upper()
    currency = row.get("currency") or ""
    financial_currency = row.get("financial_currency") or ""
    check = row.get("valuation_check") or ""
    note = row.get("fin_note") or ""
    is_adr = "ADR" in listing or "ADS" in listing or ("ADR" in adr_ratio and "不适用" not in adr_ratio)
    mismatch = bool(currency and financial_currency and currency != financial_currency)
    mismatch = mismatch or "currency_mismatch" in check or "交易货币/财报货币不一致" in note
    return is_adr or mismatch


def quantile(values: list[float], q: float) -> float:
    vals = sorted(values)
    if not vals:
        return math.nan
    pos = (len(vals) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return vals[int(pos)]
    return vals[lo] + (vals[hi] - vals[lo]) * (pos - lo)


def fmt_corr(value: float) -> str:
    return "N/A" if value is None or math.isnan(value) else f"{value:.3f}"


def fmt_pct(value: float) -> str:
    if value is None or math.isnan(value):
        return "N/A"
    return f"{value:+.2f}%"


def fmt_num(value: float) -> str:
    return "N/A" if value is None or math.isnan(value) else f"{value:.2f}"


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    aligns = []
    for h in headers:
        if h in {"数量", "样本数", "剔除数", "公司数", "窗口观测", "F22排名"} or "收益" in h or "均值" in h or "命中率" in h or h in {"Pearson", "Spearman", "Kendall", "F22分", "F22均分", "特征分", "Top30-Bottom30", "Top-Bottom收益差", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"}:
            aligns.append("---:")
        else:
            aligns.append("---")
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(aligns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def describe_sorting(corr: dict) -> str:
    sp = corr["spearman"]
    if sp >= 0.15:
        return "部分成立"
    if sp >= 0.05:
        return "弱成立"
    if sp > -0.05:
        return "不成立，接近0"
    return "不成立，方向偏负"


def describe_top_bottom(tb: dict[int, dict]) -> str:
    diff30 = tb[30]["diff"]
    if diff30 > 20:
        return "成立"
    if diff30 > 0:
        return "弱成立"
    return "不成立"


def make_company_list(tickers: list[str], max_len: int = 40) -> str:
    if not tickers:
        return "无"
    shown = tickers[:max_len]
    suffix = "" if len(tickers) <= max_len else f" 等{len(tickers)}家"
    return "、".join(shown) + suffix


def backup_existing_outputs() -> list[str]:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    existing = [
        p
        for p in EVAL_DIR.glob(f"{FEATURE_SUBJECT}_特征评估_{RETURN_WINDOW}涨跌_*.md")
        if p.is_file()
    ]
    if not existing:
        return []
    stamp = datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    dest_dir = BACKUP_DIR / f"{FEATURE_SUBJECT}_{RETURN_WINDOW}涨跌_{stamp}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    moved = []
    for src in existing:
        dest = dest_dir / src.name
        shutil.move(str(src), str(dest))
        moved.append(str(dest.relative_to(ROOT)))
    return moved


def main() -> None:
    score_rows = parse_score_table(SCORE_PATH)
    f51_rows = parse_score_table(F51_PATH)
    returns, stress = parse_price_file(RETURN_PATH)
    financial = parse_financial_file(FIN_PATH)
    f51_by_ticker = {r["ticker"]: r for r in f51_rows}

    merged: list[dict] = []
    for row in score_rows:
        ticker = row["ticker"]
        if ticker not in returns or returns[ticker].get("ret_6m") is None:
            continue
        item = dict(row)
        item.update(returns[ticker])
        item.update(stress.get(ticker, {}))
        item.update(financial.get(ticker, {}))
        liq = f51_by_ticker.get(ticker)
        item["liquidity_score"] = liq["score"] if liq else None
        item["adr_currency_abnormal"] = is_adr_or_currency_abnormal(item)
        merged.append(item)

    percentile_by_category(merged)

    score_tickers = {r["ticker"] for r in score_rows}
    return_tickers = {t for t, r in returns.items() if r.get("ret_6m") is not None}
    missing_returns = sorted(score_tickers - return_tickers)
    missing_scores = sorted(return_tickers - score_tickers)

    full_corr = corr_metrics(merged)
    tb = top_bottom_table(merged)
    ordered = sort_top(merged)
    bottom_ordered = sort_bottom(merged)

    quintile_rows = []
    for i, chunk in enumerate(array_chunks(ordered, 5), start=1):
        label = "Q1最高分" if i == 1 else ("Q5最低分" if i == 5 else f"Q{i}")
        quintile_rows.append(
            [
                label,
                str(len(chunk)),
                fmt_num(mean([r["score"] for r in chunk])),
                fmt_pct(mean([r["ret_6m"] for r in chunk])),
                fmt_pct(median([r["ret_6m"] for r in chunk])),
                fmt_pct(hit_rate(chunk)),
            ]
        )

    top10_bottom10_rows = []
    for label, rows in (("Top10", ordered[:10]), ("Bottom10", bottom_ordered[:10])):
        for r in rows:
            top10_bottom10_rows.append(
                [
                    label,
                    r["ticker"],
                    r["name"],
                    r["category"],
                    fmt_num(r["score"]),
                    str(r["rank"]),
                    fmt_pct(r["ret_6m"]),
                ]
            )

    n = len(ordered)
    mid_start = max(0, (n - 30) // 2)
    risk_groups = [
        risk_stats(f"{FEATURE_ID} Top30", ordered[:30]),
        risk_stats(f"{FEATURE_ID} Mid30", ordered[mid_start : mid_start + 30]),
        risk_stats(f"{FEATURE_ID} Bottom30", bottom_ordered[:30]),
    ]

    neutral_corr = corr_metrics(merged, "neutral_pct", "ret_6m")
    resid_corr = corr_metrics(merged, "score_resid", "return_resid")
    neutral_tb = top_bottom_table(merged, key="neutral_pct")

    category_rows = []
    categories = sorted({r["category"] for r in merged})
    for cat in categories:
        rows = [r for r in merged if r["category"] == cat]
        cc = corr_metrics(rows)
        top_return = max(rows, key=lambda r: r["ret_6m"])
        top_score = min(rows, key=lambda r: r["rank"])
        category_rows.append(
            [
                cat,
                str(len(rows)),
                fmt_corr(cc["pearson"]),
                fmt_corr(cc["spearman"]),
                fmt_pct(mean([r["ret_6m"] for r in rows])),
                f"{top_return['ticker']} {fmt_pct(top_return['ret_6m'])}",
                f"{top_score['ticker']} {fmt_num(top_score['score'])} / {fmt_pct(top_score['ret_6m'])}",
            ]
        )

    low_liq_excluded = sorted(
        [r["ticker"] for r in merged if r.get("liquidity_score") is None or r["liquidity_score"] <= 5.0]
    )
    adr_excluded = sorted([r["ticker"] for r in merged if r.get("adr_currency_abnormal")])
    returns_values = [r["ret_6m"] for r in merged]
    q05 = quantile(returns_values, 0.05)
    q95 = quantile(returns_values, 0.95)
    extreme_excluded = sorted([r["ticker"] for r in merged if r["ret_6m"] < q05 or r["ret_6m"] > q95])

    def subset_rows(rule: str) -> list[dict]:
        if rule == "all":
            return list(merged)
        if rule == "liq":
            return [r for r in merged if r.get("liquidity_score") is not None and r["liquidity_score"] > 5.0]
        if rule == "adr":
            return [r for r in merged if not r.get("adr_currency_abnormal")]
        if rule == "extreme":
            return [r for r in merged if q05 <= r["ret_6m"] <= q95]
        if rule == "combined":
            return [
                r
                for r in merged
                if r.get("liquidity_score") is not None
                and r["liquidity_score"] > 5.0
                and not r.get("adr_currency_abnormal")
                and q05 <= r["ret_6m"] <= q95
            ]
        raise ValueError(rule)

    robust_specs = [
        ("全样本基准", "无剔除", "all"),
        ("剔除低流动性", "F51交易流动性分 > 5.0", "liq"),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", "adr"),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(q05)} / {fmt_pct(q95)}", "extreme"),
        ("三项合并剔除", "同时满足上述三项", "combined"),
    ]
    robust_rows = []
    robust_summary: dict[str, dict] = {}
    for label, rule_text, rule in robust_specs:
        rows = subset_rows(rule)
        cc = corr_metrics(rows)
        tbs = top_bottom_table(rows)
        robust_summary[rule] = {"rows": rows, "corr": cc, "tb": tbs}
        robust_rows.append(
            [
                label,
                rule_text,
                str(len(rows)),
                str(len(merged) - len(rows)),
                fmt_corr(cc["pearson"]),
                fmt_corr(cc["spearman"]),
                fmt_corr(cc["kendall"]),
                fmt_pct(tbs[30]["top_mean"]),
                fmt_pct(tbs[30]["bottom_mean"]),
                fmt_pct(tbs[30]["diff"]),
            ]
        )

    top_return_rows = []
    for r in sorted(merged, key=lambda x: x["ret_6m"], reverse=True)[:15]:
        top_return_rows.append(
            [
                r["ticker"],
                r["name"],
                r["category"],
                fmt_pct(r["ret_6m"]),
                fmt_num(r["score"]),
                str(r["rank"]),
                r["confidence"],
            ]
        )

    laggard_rows = []
    for r in [x for x in ordered[:50] if x["ret_6m"] < 20][:15]:
        laggard_rows.append(
            [
                r["ticker"],
                r["name"],
                r["category"],
                fmt_num(r["score"]),
                str(r["rank"]),
                fmt_pct(r["ret_6m"]),
            ]
        )

    moved = backup_existing_outputs()
    old_text = "未发现同类旧版正式输出" if not moved else "已移动：" + "；".join(moved)

    report_lines: list[str] = []
    report_lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 {RETURN_WINDOW}涨跌 {RUN_DATE}")
    report_lines.append("")
    report_lines.append("## 运行元信息")
    report_lines.extend(
        [
            f"- 评估对象：{FEATURE_SUBJECT}。",
            f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 {RUN_DATE}，覆盖 {len(score_rows)} 家。",
            f"- 收益输入：`日度资料/区间涨跌/{RETURN_PATH.name}`，生成时间 2026-05-27 20:17:54 -0700，价格最新交易日 2026-05-27，6个月价格涨跌不含股息再投资。",
            "- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。",
            f"- 稳健性辅助输入：`特征量化/量化评分/{F51_PATH.name}`；`日度资料/每日金融数据/{FIN_PATH.name}`。",
            f"- 有效评估样本：评分与6个月涨跌交集 {len(merged)} 家；F22评分有但6个月涨跌缺失 {len(missing_returns)} 家。",
            "- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。",
            "- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为风险代理。",
            f"- 旧版处理：写入前检查 `特征量化/特征评估/` 根目录同类 F22 正式输出；处理结果：{old_text}。本次未读取旧版 F22 特征评估作为结论依据。",
        ]
    )

    report_lines.append("")
    report_lines.append("## 结论摘要")
    sorting_desc = describe_sorting(full_corr)
    tb_desc = describe_top_bottom(tb)
    neutral_desc = "仍为正" if neutral_corr["spearman"] > 0.05 else ("接近0" if neutral_corr["spearman"] > -0.05 else "转负")
    combined_corr = robust_summary["combined"]["corr"]
    risk_top = risk_groups[0]
    risk_bottom = risk_groups[2]
    risk_sentence = (
        "部分成立"
        if risk_top["stress_mean"] > risk_bottom["stress_mean"] and risk_top["avg_worst"] > risk_bottom["avg_worst"]
        else "不成立"
    )
    report_lines.extend(
        [
            f"- 排序有效性：{sorting_desc}。全样本 Pearson {fmt_corr(full_corr['pearson'])}, Spearman {fmt_corr(full_corr['spearman'])}, Kendall {fmt_corr(full_corr['kendall'])}；重点指标 Spearman 显示 F22 对本次6个月收益排序的单因子解释力偏弱。",
            f"- Top/Bottom能力：{tb_desc}。Top10、Top20、Top30 的平均收益分别为 {fmt_pct(tb[10]['top_mean'])}、{fmt_pct(tb[20]['top_mean'])}、{fmt_pct(tb[30]['top_mean'])}；Top-Bottom 收益差分别为 {fmt_pct(tb[10]['diff'])}、{fmt_pct(tb[20]['diff'])}、{fmt_pct(tb[30]['diff'])}。",
            f"- 风险解释力：{risk_sentence}。Top30 压力窗口均值 {fmt_pct(risk_top['stress_mean'])}，Bottom30 为 {fmt_pct(risk_bottom['stress_mean'])}；Top30 平均最差窗口 {fmt_pct(risk_top['avg_worst'])}，Bottom30 为 {fmt_pct(risk_bottom['avg_worst'])}。",
            f"- 分类中性：{neutral_desc}。分类内百分位合并后 Spearman {fmt_corr(neutral_corr['spearman'])}，分类去均值残差 Spearman {fmt_corr(resid_corr['spearman'])}；这用于检验结果是否只是押中某个分类目录。",
            f"- 稳健性：不稳定。剔除低流动性后 Spearman {fmt_corr(robust_summary['liq']['corr']['spearman'])}，剔除ADR/币种异常后 {fmt_corr(robust_summary['adr']['corr']['spearman'])}，剔除极端涨跌后 {fmt_corr(robust_summary['extreme']['corr']['spearman'])}，三项合并后 {fmt_corr(combined_corr['spearman'])}。",
            "- 解释：F22 衡量长期复制周期、客户迁移成本、工艺/认证/软件生态壁垒；但 2025-11至2026-05 的6个月收益大量由 AXTI、SNDK、AAOI、MXL、AEHR、ICHR、MRAM、FCEL 等高弹性或修复型标的主导。高技术稀缺公司具备长期护城河，但在这个窗口并没有稳定转化为更高的6个月价格排序收益。",
        ]
    )

    report_lines.append("")
    report_lines.append("## 覆盖检查")
    coverage_rows = [
        ["F22评分覆盖", str(len(score_rows)), f"来自{RUN_DATE}评分文件"],
        ["6个月涨跌覆盖", str(len(return_tickers)), "来自2026-05-27区间涨跌文件"],
        ["交集样本", str(len(merged)), "用于本次所有主指标"],
        ["评分有但6个月涨跌缺失", str(len(missing_returns)), make_company_list(missing_returns)],
        ["涨跌有但评分缺失", str(len(missing_scores)), make_company_list(missing_scores)],
    ]
    report_lines.append(md_table(["项目", "数量", "说明"], coverage_rows))

    report_lines.append("")
    report_lines.append("### 交集样本分类分布")
    class_dist_rows = []
    for cat in categories:
        rows = [r for r in merged if r["category"] == cat]
        class_dist_rows.append(
            [
                cat,
                str(len(rows)),
                fmt_num(mean([r["score"] for r in rows])),
                fmt_pct(mean([r["ret_6m"] for r in rows])),
                fmt_pct(median([r["ret_6m"] for r in rows])),
            ]
        )
    report_lines.append(md_table(["分类目录", "样本数", "F22均分", "6个月平均收益", "6个月中位收益"], class_dist_rows))

    report_lines.append("")
    report_lines.append("## 排序有效性")
    report_lines.append(
        md_table(
            ["指标", "数值", "解释"],
            [
                ["Pearson", fmt_corr(full_corr["pearson"]), "线性相关；容易受极端涨跌影响"],
                ["Spearman", fmt_corr(full_corr["spearman"]), "排序相关；本特征评估的主指标"],
                ["Kendall tau-b", fmt_corr(full_corr["kendall"]), "成对排序一致性；已处理分数并列"],
            ],
        )
    )
    report_lines.append("")
    report_lines.append("### 分数分组收益")
    report_lines.append(md_table(["分组", "公司数", "F22均分", "6个月平均收益", "6个月中位收益", "命中率"], quintile_rows))

    report_lines.append("")
    report_lines.append("## Top/Bottom能力")
    tb_rows = []
    for n_top, stats in tb.items():
        tb_rows.append(
            [
                f"Top{n_top}/Bottom{n_top}",
                fmt_pct(stats["top_mean"]),
                fmt_pct(stats["top_hit"]),
                fmt_pct(stats["bottom_mean"]),
                fmt_pct(stats["bottom_hit"]),
                fmt_pct(stats["diff"]),
            ]
        )
    report_lines.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], tb_rows))
    report_lines.append("")
    report_lines.append("### Top10与Bottom10构成")
    report_lines.append(md_table(["组别", "股票代号", "公司名称", "分类目录", "F22分", "F22排名", "6个月收益"], top10_bottom10_rows))

    report_lines.append("")
    report_lines.append("## 风险解释力")
    report_lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为压力测试代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供，故不写成严格波动率结论。")
    risk_rows = []
    for r in risk_groups:
        risk_rows.append(
            [
                r["group"],
                str(r["count"]),
                str(r["obs"]),
                fmt_pct(r["soxx1"]),
                fmt_pct(r["soxx2"]),
                fmt_pct(r["soxx3"]),
                fmt_pct(r["stress_mean"]),
                fmt_pct(r["avg_worst"]),
                fmt_pct(r["dispersion"]),
                fmt_pct(r["outperform"]),
                fmt_pct(r["neg_ratio"]),
            ]
        )
    report_lines.append(
        md_table(
            [
                "分组",
                "公司数",
                "窗口观测",
                "SOXX跌1均值",
                "SOXX跌2均值",
                "SOXX跌3均值",
                "压力窗口均值",
                "平均最差窗口",
                "窗口离散度",
                "跑赢SOXX比例",
                "负收益窗口占比",
            ],
            risk_rows,
        )
    )
    report_lines.append("")
    report_lines.append(
        f"结论：Top30 压力窗口均值 {fmt_pct(risk_top['stress_mean'])} 与 Bottom30 {fmt_pct(risk_bottom['stress_mean'])} 相比没有形成稳定保护；若仅看窗口离散度，Top30 为 {fmt_pct(risk_top['dispersion'])}，Bottom30 为 {fmt_pct(risk_bottom['dispersion'])}，但这不足以证明高F22组合回撤更小或下跌日更稳。"
    )

    report_lines.append("")
    report_lines.append("## 分类中性结果")
    neutral_rows = [
        ["原始全样本", str(len(merged)), fmt_corr(full_corr["pearson"]), fmt_corr(full_corr["spearman"]), fmt_corr(full_corr["kendall"]), "直接用F22分数排序"],
        ["分类内百分位合并", str(len(merged)), fmt_corr(neutral_corr["pearson"]), fmt_corr(neutral_corr["spearman"]), fmt_corr(neutral_corr["kendall"]), "每个分类内先按F22排序，再转成0-1百分位合并"],
        ["分类去均值残差", str(len(merged)), fmt_corr(resid_corr["pearson"]), fmt_corr(resid_corr["spearman"]), fmt_corr(resid_corr["kendall"]), "F22和收益分别减去分类均值后相关"],
    ]
    report_lines.append(md_table(["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"], neutral_rows))
    report_lines.append("")
    report_lines.append("### 分类中性Top/Bottom")
    ntb_rows = []
    for n_top, stats in neutral_tb.items():
        ntb_rows.append(
            [
                f"中性Top{n_top}/Bottom{n_top}",
                fmt_pct(stats["top_mean"]),
                fmt_pct(stats["top_hit"]),
                fmt_pct(stats["bottom_mean"]),
                fmt_pct(stats["bottom_hit"]),
                fmt_pct(stats["diff"]),
            ]
        )
    report_lines.append(md_table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], ntb_rows))
    report_lines.append("")
    report_lines.append("### 10个分类目录内相关性")
    report_lines.append(md_table(["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F22公司"], category_rows))
    report_lines.append("")
    report_lines.append("分类内结果显示，F22在少数目录可能有局部正相关，但多个高收益目录由中低分高弹性公司拉动。分类中性后仍不足以证明 F22 是独立6个月收益排序因子。")

    report_lines.append("")
    report_lines.append("## 稳健性检验")
    report_lines.append(
        md_table(
            ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"],
            robust_rows,
        )
    )
    report_lines.append("")
    report_lines.append(
        f"稳健性结论：剔除低流动性、ADR/币种异常和极端涨跌后，Spearman 是否保留正向排序是核心判断。本次三项合并后 Spearman 为 {fmt_corr(combined_corr['spearman'])}，Top30-Bottom30 为 {fmt_pct(robust_summary['combined']['tb'][30]['diff'])}，因此 F22 对6个月收益的独立排序解释力不能单独使用。"
    )

    report_lines.append("")
    report_lines.append("### 剔除清单")
    removal_rows = [
        ["低流动性", str(len(low_liq_excluded)), make_company_list(low_liq_excluded, 80)],
        ["ADR/币种异常", str(len(adr_excluded)), make_company_list(adr_excluded, 80)],
        ["极端涨跌双尾5%", str(len(extreme_excluded)), make_company_list(extreme_excluded, 80)],
    ]
    report_lines.append(md_table(["剔除项", "数量", "公司"], removal_rows))

    report_lines.append("")
    report_lines.append("## 诊断：收益由哪些公司主导")
    report_lines.append("### 6个月涨幅前15")
    report_lines.append(md_table(["股票代号", "公司名称", "分类目录", "6个月收益", "F22分", "F22排名", "F22置信度"], top_return_rows))

    report_lines.append("")
    report_lines.append("### 高F22但6个月收益偏弱样本")
    if laggard_rows:
        report_lines.append(md_table(["股票代号", "公司名称", "分类目录", "F22分", "F22排名", "6个月收益"], laggard_rows))
    else:
        report_lines.append("无。")

    report_lines.append("")
    report_lines.append("## 使用建议")
    report_lines.extend(
        [
            f"- 对“6个月价格涨跌排序”的单因子预测：{FEATURE_SUBJECT}本轮评估为偏弱或无效，不建议单独用于6个月收益排序。",
            "- 对风险解释：F22可以解释长期技术护城河、复制周期和客户迁移成本，但本轮压力窗口没有证明高分组合更抗跌；需要与估值压力、价格相对强度、交易流动性和催化剂强度联用。",
            "- 对多因子模型：F22更适合作为长期质量/护城河维度，降低短周期高弹性收益因子对组合的过度支配，而不是直接替代动量、估值或事件催化。",
            "- 对上游资料：本报告只作为下游特征评估，不反向修改公司调研、行业调研或日度事实资料。",
        ]
    )

    report_lines.append("")
    report_lines.append("## 方法附录")
    report_lines.extend(
        [
            "- Pearson：用 F22 原始分与6个月涨跌百分比计算线性相关。",
            "- Spearman：用 F22 分数排序与6个月涨跌排序计算相关，是本次主指标。",
            "- Kendall tau-b：用成对排序一致性计算，处理 F22 分数并列。",
            "- 分类中性：在10个分类目录内分别按F22排序并转百分位，再合并计算相关性和Top/Bottom表现；另用分类去均值残差复核。",
            "- 低流动性剔除：使用 F51 交易流动性评分，保留 F51 > 5.0 的公司。",
            "- ADR/币种异常剔除：剔除 ADR/ADS、交易货币与财报货币不一致、估值校验存在 currency_mismatch 的公司。",
            "- 极端涨跌剔除：按交集样本6个月涨跌双尾5%阈值剔除。",
        ]
    )

    OUTPUT_PATH.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"score_rows={len(score_rows)}")
    print(f"return_rows={len(return_tickers)}")
    print(f"merged={len(merged)}")
    print(f"missing_returns={len(missing_returns)} {','.join(missing_returns)}")
    print(f"full_spearman={fmt_corr(full_corr['spearman'])}")
    print(f"top30_diff={fmt_pct(tb[30]['diff'])}")
    print(f"combined_spearman={fmt_corr(combined_corr['spearman'])}")
    print(f"output={OUTPUT_PATH}")


if __name__ == "__main__":
    main()
