from __future__ import annotations

import math
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median, stdev


ROOT = Path.cwd()
FEATURE_ID = "F14"
FEATURE_NAME = "3-6月利润率改善信号"
RUN_DATE = "2026-06-04"

SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_ID}_{FEATURE_NAME}_量化评分_{RUN_DATE}.md"
RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
LIQUIDITY_PATH = ROOT / "特征量化" / "量化评分" / "F51_交易流动性_量化评分_2026-06-04.md"
FINANCIAL_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
EVAL_DIR = ROOT / "特征量化" / "特征评估"
BACKUP_DIR = EVAL_DIR / "备份"
OUTPUT_PATH = EVAL_DIR / f"{FEATURE_ID}_{FEATURE_NAME}_特征评估_6个月涨跌_{RUN_DATE}.md"


@dataclass
class ScoreRow:
    ticker: str
    company: str
    category: str
    score: float
    rank: int
    evidence: str
    confidence: str


@dataclass
class ReturnRow:
    ticker: str
    company: str
    category: str
    latest_date: str
    return_6m: float | None
    soxx1: float | None = None
    soxx2: float | None = None
    soxx3: float | None = None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def md_cells(line: str) -> list[str] | None:
    if not line.startswith("|"):
        return None
    parts = [part.strip() for part in line.strip().strip("|").split("|")]
    if not parts:
        return None
    if all(set(part) <= set("-: ") for part in parts):
        return None
    return parts


def parse_pct(cell: str) -> float | None:
    if not cell or "N/A" in cell:
        return None
    match = re.search(r"([+-]?\d+(?:,\d{3})*(?:\.\d+)?)%", cell)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def clean_cell(cell: str) -> str:
    return re.sub(r"<br\s*/?>", "；", cell).strip()


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None or math.isnan(value):
        return "N/A"
    return f"{value:+.{digits}f}%"


def fmt_num(value: float | None, digits: int = 3) -> str:
    if value is None or math.isnan(value):
        return "N/A"
    return f"{value:.{digits}f}"


def parse_score_table(path: Path) -> dict[str, ScoreRow]:
    text = read_text(path)
    rows: dict[str, ScoreRow] = {}
    in_table = False
    for line in text.splitlines():
        if line.startswith("## 全公司排序表"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table:
            continue
        cells = md_cells(line)
        if not cells or len(cells) < 7 or not cells[0].isdigit():
            continue
        rank = int(cells[0])
        ticker = cells[1]
        rows[ticker] = ScoreRow(
            ticker=ticker,
            company=cells[2],
            category=cells[3],
            score=float(cells[4]),
            rank=rank,
            evidence=cells[5],
            confidence=cells[6],
        )
    return rows


def parse_returns(path: Path) -> tuple[dict[str, ReturnRow], dict[str, float], dict[str, str]]:
    text = read_text(path)
    rows: dict[str, ReturnRow] = {}
    meta: dict[str, str] = {}

    gen_match = re.search(r"- 生成时间：(.+)", text)
    if gen_match:
        meta["生成时间"] = gen_match.group(1).strip()
    latest_match = re.search(r"- 最新可得交易日最大值：`([^`]+)`", text)
    if latest_match:
        meta["价格最新交易日"] = latest_match.group(1)

    soxx_returns: dict[str, float] = {}
    for line in text.splitlines():
        cells = md_cells(line)
        if not cells or not cells[0].startswith("SOXX下跌"):
            continue
        if len(cells) >= 6:
            label = cells[0].split("：", 1)[0]
            pct = parse_pct(cells[5])
            if pct is not None:
                soxx_returns[label] = pct

    # Stress windows.
    in_risk = False
    current_category = ""
    for line in text.splitlines():
        if line.startswith("### 按分类分组的全公司明细"):
            in_risk = True
            continue
        if in_risk and line.startswith("## 按分类分组的公司明细"):
            break
        if not in_risk:
            continue
        if line.startswith("#### "):
            current_category = line.removeprefix("#### ").strip()
            continue
        cells = md_cells(line)
        if not cells or len(cells) < 6 or cells[0] == "股票代号":
            continue
        ticker = cells[0]
        row = rows.get(ticker)
        if row is None:
            row = ReturnRow(ticker=ticker, company=cells[1], category=current_category, latest_date="", return_6m=None)
            rows[ticker] = row
        row.soxx1 = parse_pct(cells[2])
        row.soxx2 = parse_pct(cells[3])
        row.soxx3 = parse_pct(cells[4])

    # Main interval returns.
    in_returns = False
    current_category = ""
    for line in text.splitlines():
        if line.startswith("## 按分类分组的公司明细"):
            in_returns = True
            continue
        if not in_returns:
            continue
        if line.startswith("### "):
            current_category = line.removeprefix("### ").strip()
            continue
        cells = md_cells(line)
        if not cells or len(cells) < 9 or cells[0] == "股票代号":
            continue
        ticker = cells[0]
        row = rows.get(ticker)
        if row is None:
            row = ReturnRow(ticker=ticker, company=cells[1], category=current_category, latest_date=cells[2], return_6m=None)
            rows[ticker] = row
        row.company = cells[1]
        row.category = current_category
        row.latest_date = cells[2]
        row.return_6m = parse_pct(cells[6])
    return rows, soxx_returns, meta


def parse_financial_flags(path: Path) -> dict[str, dict[str, str | bool]]:
    text = read_text(path)
    data: dict[str, dict[str, str | bool]] = {}
    header: list[str] | None = None
    current_category = ""
    for line in text.splitlines():
        if line.startswith("### "):
            current_category = line.removeprefix("### ").strip()
            header = None
            continue
        cells = md_cells(line)
        if not cells:
            continue
        if cells[0] == "股票代号" and "listing_type" in cells:
            header = cells
            continue
        if header is None or len(cells) < len(header) or cells[0] == "股票代号":
            continue
        item = {name: cells[i] for i, name in enumerate(header)}
        ticker = item["股票代号"]
        listing = item.get("listing_type", "")
        adr_ratio = item.get("adr_ratio", "")
        currency = item.get("currency", "")
        financial_currency = item.get("financial_currency", "")
        valuation = item.get("估值校验", "")
        note = item.get("备注", "")
        abnormal = (
            listing != "common/equity"
            or adr_ratio != "不适用"
            or currency != financial_currency
            or "currency_mismatch" in valuation
            or "交易货币/财报货币不一致" in note
            or "ADR/ADS比例需确认" in note
        )
        data[ticker] = {
            "category": current_category,
            "listing_type": listing,
            "adr_ratio": adr_ratio,
            "currency": currency,
            "financial_currency": financial_currency,
            "valuation": valuation,
            "note": clean_cell(note),
            "adr_currency_abnormal": abnormal,
        }
    return data


def average(values: list[float]) -> float | None:
    values = [v for v in values if v is not None and not math.isnan(v)]
    if not values:
        return None
    return mean(values)


def hit_rate(values: list[float]) -> float | None:
    values = [v for v in values if v is not None and not math.isnan(v)]
    if not values:
        return None
    return 100.0 * sum(1 for v in values if v > 0) / len(values)


def rank_values(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        rank = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            ranks[indexed[k][0]] = rank
        i = j + 1
    return ranks


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    mx = mean(xs)
    my = mean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / math.sqrt(vx * vy)


def spearman(xs: list[float], ys: list[float]) -> float | None:
    return pearson(rank_values(xs), rank_values(ys))


def kendall_tau_b(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 2:
        return None
    concordant = discordant = 0
    ties_x = ties_y = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            dx = (xs[i] > xs[j]) - (xs[i] < xs[j])
            dy = (ys[i] > ys[j]) - (ys[i] < ys[j])
            if dx == 0:
                ties_x += 1
            if dy == 0:
                ties_y += 1
            if dx == 0 or dy == 0:
                continue
            if dx == dy:
                concordant += 1
            else:
                discordant += 1
    n0 = n * (n - 1) / 2
    denom = math.sqrt((n0 - ties_x) * (n0 - ties_y))
    if denom == 0:
        return None
    return (concordant - discordant) / denom


def correlations(records: list[dict]) -> dict[str, float | None]:
    xs = [r["score"] for r in records]
    ys = [r["return_6m"] for r in records]
    return {
        "pearson": pearson(xs, ys),
        "spearman": spearman(xs, ys),
        "kendall": kendall_tau_b(xs, ys),
    }


def percentile(values: list[float], p: float) -> float:
    values = sorted(values)
    if not values:
        raise ValueError("empty percentile input")
    if len(values) == 1:
        return values[0]
    pos = p * (len(values) - 1)
    low = math.floor(pos)
    high = math.ceil(pos)
    if low == high:
        return values[low]
    return values[low] + (values[high] - values[low]) * (pos - low)


def sorted_records(records: list[dict]) -> list[dict]:
    return sorted(records, key=lambda r: (-r["score"], r["score_rank"], r["ticker"]))


def top_bottom(records: list[dict], n: int) -> dict[str, float | list[dict]]:
    ordered = sorted_records(records)
    top = ordered[:n]
    bottom = ordered[-n:]
    return {
        "top": top,
        "bottom": bottom,
        "top_avg": average([r["return_6m"] for r in top]),
        "bottom_avg": average([r["return_6m"] for r in bottom]),
        "top_hit": hit_rate([r["return_6m"] for r in top]),
        "bottom_hit": hit_rate([r["return_6m"] for r in bottom]),
    }


def quintile_groups(records: list[dict], groups: int = 5) -> list[list[dict]]:
    ordered = sorted_records(records)
    n = len(ordered)
    return [ordered[math.floor(i * n / groups) : math.floor((i + 1) * n / groups)] for i in range(groups)]


def category_neutral_records(records: list[dict]) -> list[dict]:
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_cat[record["category"]].append(record)
    out: list[dict] = []
    for cat_records in by_cat.values():
        ordered = sorted_records(cat_records)
        n = len(ordered)
        for i, record in enumerate(ordered):
            clone = dict(record)
            clone["category_percentile"] = 1.0 if n == 1 else 1.0 - i / (n - 1)
            out.append(clone)
    return out


def residual_records(records: list[dict]) -> list[dict]:
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_cat[record["category"]].append(record)
    out: list[dict] = []
    for cat_records in by_cat.values():
        score_mean = mean(r["score"] for r in cat_records)
        return_mean = mean(r["return_6m"] for r in cat_records)
        for record in cat_records:
            clone = dict(record)
            clone["score_residual"] = record["score"] - score_mean
            clone["return_residual"] = record["return_6m"] - return_mean
            out.append(clone)
    return out


def risk_stats(group: list[dict], soxx_returns: dict[str, float]) -> dict[str, float | int | None]:
    keys = ["soxx1", "soxx2", "soxx3"]
    soxx_keys = ["SOXX下跌1", "SOXX下跌2", "SOXX下跌3"]
    per_window = {}
    all_values = []
    worst_values = []
    dispersions = []
    beats = 0
    beat_obs = 0
    negative = 0
    for idx, key in enumerate(keys):
        vals = [r[key] for r in group if r.get(key) is not None]
        per_window[key] = average(vals)
    for record in group:
        vals = [record.get(key) for key in keys if record.get(key) is not None]
        all_values.extend(vals)
        if vals:
            worst_values.append(min(vals))
        if len(vals) >= 2:
            dispersions.append(stdev(vals))
        for idx, key in enumerate(keys):
            value = record.get(key)
            if value is None:
                continue
            soxx = soxx_returns.get(soxx_keys[idx])
            if soxx is not None:
                beat_obs += 1
                if value > soxx:
                    beats += 1
            if value < 0:
                negative += 1
    return {
        "count": len(group),
        "obs": len(all_values),
        "soxx1_avg": per_window["soxx1"],
        "soxx2_avg": per_window["soxx2"],
        "soxx3_avg": per_window["soxx3"],
        "pressure_avg": average(all_values),
        "worst_avg": average(worst_values),
        "dispersion": average(dispersions),
        "beat_soxx": None if beat_obs == 0 else 100.0 * beats / beat_obs,
        "negative_share": None if not all_values else 100.0 * negative / len(all_values),
    }


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def metric_sentence(spearman_value: float | None) -> str:
    if spearman_value is None:
        return "样本不足。"
    if spearman_value >= 0.20:
        return "正向有效。"
    if spearman_value >= 0.08:
        return "弱正向有效。"
    if spearman_value > -0.08:
        return "接近0，排序有效性不足。"
    return "负向或反向，排序有效性不成立。"


def move_old_outputs() -> list[str]:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    moved: list[str] = []
    pattern = f"{FEATURE_ID}_{FEATURE_NAME}_特征评估_6个月涨跌_*.md"
    for path in EVAL_DIR.glob(pattern):
        if path.resolve() == OUTPUT_PATH.resolve():
            continue
        backup_name = path.stem + f"_备份于{RUN_DATE}" + path.suffix
        backup_path = BACKUP_DIR / backup_name
        suffix = 1
        while backup_path.exists():
            backup_path = BACKUP_DIR / f"{path.stem}_备份于{RUN_DATE}_{suffix}{path.suffix}"
            suffix += 1
        path.replace(backup_path)
        moved.append(f"{path.name} -> 备份/{backup_path.name}")
    if OUTPUT_PATH.exists():
        backup_path = BACKUP_DIR / (OUTPUT_PATH.stem + f"_覆盖前备份于{RUN_DATE}" + OUTPUT_PATH.suffix)
        suffix = 1
        while backup_path.exists():
            backup_path = BACKUP_DIR / f"{OUTPUT_PATH.stem}_覆盖前备份于{RUN_DATE}_{suffix}{OUTPUT_PATH.suffix}"
            suffix += 1
        OUTPUT_PATH.replace(backup_path)
        moved.append(f"{OUTPUT_PATH.name} -> 备份/{backup_path.name}")
    return moved


def main() -> None:
    scores = parse_score_table(SCORE_PATH)
    liquidity_scores = parse_score_table(LIQUIDITY_PATH)
    returns, soxx_returns, return_meta = parse_returns(RETURN_PATH)
    financial = parse_financial_flags(FINANCIAL_PATH)

    records: list[dict] = []
    for ticker, score in scores.items():
        ret = returns.get(ticker)
        if ret is None or ret.return_6m is None:
            continue
        f51 = liquidity_scores.get(ticker)
        fin = financial.get(ticker, {})
        records.append(
            {
                "ticker": ticker,
                "company": score.company,
                "category": score.category,
                "score": score.score,
                "score_rank": score.rank,
                "evidence": score.evidence,
                "confidence": score.confidence,
                "return_6m": ret.return_6m,
                "latest_date": ret.latest_date,
                "soxx1": ret.soxx1,
                "soxx2": ret.soxx2,
                "soxx3": ret.soxx3,
                "liquidity_score": None if f51 is None else f51.score,
                "adr_currency_abnormal": bool(fin.get("adr_currency_abnormal", False)),
                "listing_type": str(fin.get("listing_type", "")),
                "currency": str(fin.get("currency", "")),
                "financial_currency": str(fin.get("financial_currency", "")),
            }
        )

    corr = correlations(records)
    ordered = sorted_records(records)
    missing_returns = sorted(set(scores) - {r["ticker"] for r in records}, key=lambda t: scores[t].rank)
    missing_scores = sorted(set(returns) - set(scores))

    by_cat: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_cat[record["category"]].append(record)

    quintiles = quintile_groups(records)
    tb = {n: top_bottom(records, n) for n in [10, 20, 30]}

    neutral = category_neutral_records(records)
    neutral_corr = {
        "pearson": pearson([r["category_percentile"] for r in neutral], [r["return_6m"] for r in neutral]),
        "spearman": spearman([r["category_percentile"] for r in neutral], [r["return_6m"] for r in neutral]),
        "kendall": kendall_tau_b([r["category_percentile"] for r in neutral], [r["return_6m"] for r in neutral]),
    }
    residual = residual_records(records)
    residual_corr = {
        "pearson": pearson([r["score_residual"] for r in residual], [r["return_residual"] for r in residual]),
        "spearman": spearman([r["score_residual"] for r in residual], [r["return_residual"] for r in residual]),
        "kendall": kendall_tau_b([r["score_residual"] for r in residual], [r["return_residual"] for r in residual]),
    }
    neutral_ordered = sorted(neutral, key=lambda r: (-r["category_percentile"], -r["score"], r["score_rank"], r["ticker"]))
    neutral_tb = {}
    for n in [10, 20, 30]:
        top = neutral_ordered[:n]
        bottom = neutral_ordered[-n:]
        neutral_tb[n] = {
            "top_avg": average([r["return_6m"] for r in top]),
            "top_hit": hit_rate([r["return_6m"] for r in top]),
            "bottom_avg": average([r["return_6m"] for r in bottom]),
            "bottom_hit": hit_rate([r["return_6m"] for r in bottom]),
        }

    top30 = ordered[:30]
    bottom30 = ordered[-30:]
    mid_start = (len(ordered) - 30) // 2
    mid30 = ordered[mid_start : mid_start + 30]
    risk = {
        f"{FEATURE_ID} Top30": risk_stats(top30, soxx_returns),
        f"{FEATURE_ID} Mid30": risk_stats(mid30, soxx_returns),
        f"{FEATURE_ID} Bottom30": risk_stats(bottom30, soxx_returns),
    }

    all_returns = [r["return_6m"] for r in records]
    low_q = percentile(all_returns, 0.05)
    high_q = percentile(all_returns, 0.95)
    low_liq = {r["ticker"] for r in records if r["liquidity_score"] is None or r["liquidity_score"] <= 5.0}
    adr_bad = {r["ticker"] for r in records if r["adr_currency_abnormal"]}
    extreme = {r["ticker"] for r in records if r["return_6m"] < low_q or r["return_6m"] > high_q}

    robustness_specs = [
        ("全样本基准", "无剔除", set()),
        ("剔除低流动性", "F51交易流动性分 > 5.0", low_liq),
        ("剔除ADR/币种异常", "非ADR/ADS且交易货币=财报货币，估值校验无currency_mismatch", adr_bad),
        ("剔除极端涨跌", f"剔除6个月涨跌双尾5%；阈值 {fmt_pct(low_q)} / {fmt_pct(high_q)}", extreme),
        ("三项合并剔除", "同时满足上述三项", low_liq | adr_bad | extreme),
    ]
    robustness_rows = []
    for label, rule, excluded in robustness_specs:
        subset = [r for r in records if r["ticker"] not in excluded]
        c = correlations(subset)
        tb30 = top_bottom(subset, 30)
        robustness_rows.append(
            {
                "label": label,
                "rule": rule,
                "sample": len(subset),
                "excluded": len(records) - len(subset),
                "pearson": c["pearson"],
                "spearman": c["spearman"],
                "kendall": c["kendall"],
                "top30": tb30["top_avg"],
                "bottom30": tb30["bottom_avg"],
                "diff": None if tb30["top_avg"] is None or tb30["bottom_avg"] is None else tb30["top_avg"] - tb30["bottom_avg"],
            }
        )

    moved = move_old_outputs()

    # Report tables.
    lines: list[str] = []
    lines.append(f"# {FEATURE_ID} {FEATURE_NAME} 特征评估 6个月涨跌 {RUN_DATE}")
    lines.append("")
    lines.append("## 运行元信息")
    lines.append(f"- 评估对象：{FEATURE_ID}_{FEATURE_NAME}。")
    lines.append(f"- 评分输入：`特征量化/量化评分/{SCORE_PATH.name}`，评分日期 {RUN_DATE}，覆盖 {len(scores)} 家。")
    generated_time = return_meta.get("生成时间", "N/A").rstrip("。")
    lines.append(
        f"- 收益输入：`日度资料/区间涨跌/{RETURN_PATH.name}`，生成时间 {generated_time}，价格最新交易日 {return_meta.get('价格最新交易日', 'N/A')}，6个月价格涨跌不含股息再投资。"
    )
    lines.append("- 风险窗口输入：同一收益文件中的三个 SOXX 最大下跌窗口，分别为 2025-02-20至2025-04-08、2026-02-25至2026-03-30、2025-10-29至2025-11-20。")
    lines.append("- 稳健性辅助输入：`特征量化/量化评分/F51_交易流动性_量化评分_2026-06-04.md`；`日度资料/每日金融数据/每日金融数据_2026-06-03.md`。")
    lines.append(f"- 有效评估样本：评分与6个月涨跌交集 {len(records)} 家；F14评分有但6个月涨跌缺失 {len(missing_returns)} 家。")
    lines.append("- 命中率口径：6个月涨跌幅大于 0 记为命中。Top-Bottom收益差=高分组合平均6个月收益 - 低分组合平均6个月收益。")
    lines.append("- 风险口径限制：本次区间涨跌文件没有逐日收益序列，因此不把结果写成严格日度波动或完整最大回撤；报告使用三个 SOXX 压力窗口的均值、最差窗口、窗口收益离散度和跑赢 SOXX 比例作为风险代理。")
    lines.append("- 稳健性口径限制：F51 是交易流动性代理评分，日度金融数据未提供真实 ADV、成交额或买卖价差；本报告把 F51<=5.0 作为低流动性剔除代理。")
    old_note = "；".join(moved) if moved else "写入前已检查根目录，无同类旧版 F14 正式输出残留。"
    lines.append(f"- 旧版处理：{old_note} 本次未读取旧版 F14 特征评估作为结论依据。")
    lines.append("")

    f14_top = tb[30]["top_avg"]
    f14_bottom = tb[30]["bottom_avg"]
    f14_diff = None if f14_top is None or f14_bottom is None else f14_top - f14_bottom
    risk_top = risk[f"{FEATURE_ID} Top30"]
    risk_bottom = risk[f"{FEATURE_ID} Bottom30"]
    combined_spearman = robustness_rows[-1]["spearman"]

    lines.append("## 结论摘要")
    lines.append(
        f"- 排序有效性：{metric_sentence(corr['spearman'])}全样本 Pearson {fmt_num(corr['pearson'])}, Spearman {fmt_num(corr['spearman'])}, Kendall {fmt_num(corr['kendall'])}；重点指标 Spearman 用于判断排序分是否能解释6个月收益。"
    )
    lines.append(
        f"- Top/Bottom能力：Top10、Top20、Top30 的平均收益分别为 {fmt_pct(tb[10]['top_avg'])}、{fmt_pct(tb[20]['top_avg'])}、{fmt_pct(tb[30]['top_avg'])}；Top-Bottom 收益差分别为 {fmt_pct(tb[10]['top_avg'] - tb[10]['bottom_avg'])}、{fmt_pct(tb[20]['top_avg'] - tb[20]['bottom_avg'])}、{fmt_pct(f14_diff)}。"
    )
    lines.append(
        f"- 风险解释力：Top30 压力窗口均值 {fmt_pct(risk_top['pressure_avg'])}，Bottom30 为 {fmt_pct(risk_bottom['pressure_avg'])}；Top30 平均最差窗口 {fmt_pct(risk_top['worst_avg'])}，Bottom30 为 {fmt_pct(risk_bottom['worst_avg'])}；Top30 窗口离散度 {fmt_pct(risk_top['dispersion'])}，Bottom30 为 {fmt_pct(risk_bottom['dispersion'])}。"
    )
    lines.append(
        f"- 分类中性：分类内百分位合并后 Spearman {fmt_num(neutral_corr['spearman'])}；分类去均值残差口径 Spearman {fmt_num(residual_corr['spearman'])}。"
    )
    lines.append(
        f"- 稳健性：剔除低流动性后 Spearman {fmt_num(robustness_rows[1]['spearman'])}, 剔除ADR/币种异常后为 {fmt_num(robustness_rows[2]['spearman'])}, 剔除极端涨跌后为 {fmt_num(robustness_rows[3]['spearman'])}, 三项合并后为 {fmt_num(combined_spearman)}。"
    )
    top_return_names = ", ".join(f"{r['ticker']} {fmt_pct(r['return_6m'])}" for r in sorted(records, key=lambda r: -r["return_6m"])[:6])
    top_score_names = ", ".join(f"{r['ticker']} {r['score']:.1f}/{fmt_pct(r['return_6m'])}" for r in ordered[:6])
    lines.append(
        f"- 解释：6个月收益头部由 {top_return_names} 等高弹性或修复型标的主导；F14高分头部为 {top_score_names}，更偏利润率改善机制和订单/产品mix兑现质量，未必等同于最高价格弹性。"
    )
    lines.append("")

    lines.append("## 覆盖检查")
    lines.append(
        table(
            ["项目", "数量", "说明"],
            [
                ["F14评分覆盖", str(len(scores)), "来自2026-06-04评分文件"],
                ["6个月涨跌覆盖", str(sum(1 for r in returns.values() if r.return_6m is not None)), "来自2026-05-27区间涨跌文件"],
                ["交集样本", str(len(records)), "用于本次所有主指标"],
                ["评分有但6个月涨跌缺失", str(len(missing_returns)), ", ".join(missing_returns) if missing_returns else "无"],
                ["涨跌有但评分缺失", str(len(missing_scores)), ", ".join(missing_scores) if missing_scores else "无"],
            ],
        )
    )
    lines.append("")
    lines.append("### 交集样本分类分布")
    cat_rows = []
    for category, cat_records in sorted(by_cat.items(), key=lambda item: (-len(item[1]), item[0])):
        cat_rows.append(
            [
                category,
                str(len(cat_records)),
                f"{mean(r['score'] for r in cat_records):.2f}",
                fmt_pct(mean(r["return_6m"] for r in cat_records)),
                fmt_pct(median(r["return_6m"] for r in cat_records)),
            ]
        )
    lines.append(table(["分类目录", "样本数", "F14均分", "6个月平均收益", "6个月中位收益"], cat_rows))
    lines.append("")

    lines.append("## 排序有效性")
    lines.append(
        table(
            ["指标", "数值", "解释"],
            [
                ["Pearson", fmt_num(corr["pearson"]), "线性相关；受极端涨跌影响较大"],
                ["Spearman", fmt_num(corr["spearman"]), "排序相关；本任务最重要指标"],
                ["Kendall tau-b", fmt_num(corr["kendall"]), "成对排序一致性指标；对并列分数做tie修正"],
            ],
        )
    )
    lines.append("")
    lines.append("### 分数分组收益")
    q_rows = []
    for i, group in enumerate(quintiles, start=1):
        q_rows.append(
            [
                "Q1最高分" if i == 1 else f"Q{i}",
                str(len(group)),
                f"{mean(r['score'] for r in group):.2f}",
                fmt_pct(mean(r["return_6m"] for r in group)),
                fmt_pct(median(r["return_6m"] for r in group)),
                fmt_pct(hit_rate([r["return_6m"] for r in group]), 1),
            ]
        )
    lines.append(table(["分组", "公司数", "F14均分", "6个月平均收益", "6个月中位收益", "命中率"], q_rows))
    lines.append("")

    lines.append("## Top/Bottom能力")
    tb_rows = []
    for n in [10, 20, 30]:
        diff = tb[n]["top_avg"] - tb[n]["bottom_avg"]
        tb_rows.append([f"Top{n}/Bottom{n}", fmt_pct(tb[n]["top_avg"]), fmt_pct(tb[n]["top_hit"], 1), fmt_pct(tb[n]["bottom_avg"]), fmt_pct(tb[n]["bottom_hit"], 1), fmt_pct(diff)])
    lines.append(table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], tb_rows))
    lines.append("")
    lines.append("### Top10与Bottom10构成")
    comp_rows = []
    for label, group in [("Top10", tb[10]["top"]), ("Bottom10", tb[10]["bottom"])]:
        for r in group:
            comp_rows.append([label, r["ticker"], r["company"], r["category"], f"{r['score']:.1f}", str(r["score_rank"]), fmt_pct(r["return_6m"])])
    lines.append(table(["组别", "股票代号", "公司名称", "分类目录", "F14分", "F14排名", "6个月收益"], comp_rows))
    lines.append("")

    lines.append("## 风险解释力")
    lines.append("本节只使用本地收益文件中的三个 SOXX 最大下跌窗口作为压力测试代理。严格日度波动率和完整最大回撤需要逐日价格序列，本次输入文件没有提供，故不写成严格波动率结论。")
    risk_rows = []
    for label, stats in risk.items():
        risk_rows.append(
            [
                label,
                str(stats["count"]),
                str(stats["obs"]),
                fmt_pct(stats["soxx1_avg"]),
                fmt_pct(stats["soxx2_avg"]),
                fmt_pct(stats["soxx3_avg"]),
                fmt_pct(stats["pressure_avg"]),
                fmt_pct(stats["worst_avg"]),
                fmt_pct(stats["dispersion"]),
                fmt_pct(stats["beat_soxx"], 1),
                fmt_pct(stats["negative_share"], 1),
            ]
        )
    lines.append(
        table(
            ["分组", "公司数", "窗口观测", "SOXX跌1均值", "SOXX跌2均值", "SOXX跌3均值", "压力窗口均值", "平均最差窗口", "窗口离散度", "跑赢SOXX比例", "负收益窗口占比"],
            risk_rows,
        )
    )
    lines.append("")
    lines.append(
        f"结论：Top30 的压力窗口均值为 {fmt_pct(risk_top['pressure_avg'])}，Bottom30 为 {fmt_pct(risk_bottom['pressure_avg'])}；Top30 平均最差窗口为 {fmt_pct(risk_top['worst_avg'])}，Bottom30 为 {fmt_pct(risk_bottom['worst_avg'])}。这只能说明三段 SOXX 压力窗口内的相对表现，不能替代逐日波动率或最大回撤。"
    )
    lines.append("")

    lines.append("## 分类中性结果")
    lines.append(
        table(
            ["口径", "样本数", "Pearson", "Spearman", "Kendall", "说明"],
            [
                ["原始全样本", str(len(records)), fmt_num(corr["pearson"]), fmt_num(corr["spearman"]), fmt_num(corr["kendall"]), "直接用F14分数排序"],
                ["分类内百分位合并", str(len(neutral)), fmt_num(neutral_corr["pearson"]), fmt_num(neutral_corr["spearman"]), fmt_num(neutral_corr["kendall"]), "每个分类内先按F14排序，再转成0-1百分位合并"],
                ["分类去均值残差", str(len(residual)), fmt_num(residual_corr["pearson"]), fmt_num(residual_corr["spearman"]), fmt_num(residual_corr["kendall"]), "F14和收益分别减去分类均值后相关"],
            ],
        )
    )
    lines.append("")
    lines.append("### 分类中性Top/Bottom")
    neutral_rows = []
    for n in [10, 20, 30]:
        diff = neutral_tb[n]["top_avg"] - neutral_tb[n]["bottom_avg"]
        neutral_rows.append([f"中性Top{n}/Bottom{n}", fmt_pct(neutral_tb[n]["top_avg"]), fmt_pct(neutral_tb[n]["top_hit"], 1), fmt_pct(neutral_tb[n]["bottom_avg"]), fmt_pct(neutral_tb[n]["bottom_hit"], 1), fmt_pct(diff)])
    lines.append(table(["组合", "Top平均收益", "Top命中率", "Bottom平均收益", "Bottom命中率", "Top-Bottom收益差"], neutral_rows))
    lines.append("")
    lines.append("### 10个分类目录内相关性")
    cat_corr_rows = []
    for category, cat_records in sorted(by_cat.items()):
        c = correlations(cat_records)
        top_return = max(cat_records, key=lambda r: r["return_6m"])
        top_score = sorted_records(cat_records)[0]
        cat_corr_rows.append(
            [
                category,
                str(len(cat_records)),
                fmt_num(c["pearson"]),
                fmt_num(c["spearman"]),
                fmt_pct(mean(r["return_6m"] for r in cat_records)),
                f"{top_return['ticker']} {fmt_pct(top_return['return_6m'])}",
                f"{top_score['ticker']} {top_score['score']:.1f} / {fmt_pct(top_score['return_6m'])}",
            ]
        )
    lines.append(table(["分类目录", "样本数", "Pearson", "Spearman", "类内平均6个月收益", "类内最高收益", "类内最高F14公司"], cat_corr_rows))
    lines.append("")
    lines.append("分类内结果用于识别是否只是押中某个目录。若原始全样本与分类内百分位、分类残差口径方向相近，说明结果不是单一行业暴露造成；若方向变化，则说明行业结构和个股极值共同影响较大。")
    lines.append("")

    lines.append("## 稳健性检验")
    robustness_table_rows = []
    for row in robustness_rows:
        robustness_table_rows.append(
            [
                row["label"],
                row["rule"],
                str(row["sample"]),
                str(row["excluded"]),
                fmt_num(row["pearson"]),
                fmt_num(row["spearman"]),
                fmt_num(row["kendall"]),
                fmt_pct(row["top30"]),
                fmt_pct(row["bottom30"]),
                fmt_pct(row["diff"]),
            ]
        )
    lines.append(
        table(
            ["口径", "剔除规则", "样本数", "剔除数", "Pearson", "Spearman", "Kendall", "Top30均值", "Bottom30均值", "Top30-Bottom30"],
            robustness_table_rows,
        )
    )
    lines.append("")
    lines.append(
        f"稳健性结论：剔除低流动性、ADR/币种异常和极端涨跌后，Spearman 是否保留正向排序是核心判断。本次三项合并后 Spearman 为 {fmt_num(combined_spearman)}，说明 F14 对6个月收益的独立排序解释力需要结合估值、价格动量、流动性、催化剂和极端涨跌过滤共同使用。"
    )
    lines.append("")
    lines.append("### 剔除清单")
    lines.append(
        table(
            ["剔除项", "数量", "公司"],
            [
                ["低流动性", str(len(low_liq)), ", ".join(sorted(low_liq))],
                ["ADR/币种异常", str(len(adr_bad)), ", ".join(sorted(adr_bad))],
                ["极端涨跌双尾5%", str(len(extreme)), ", ".join(sorted(extreme))],
            ],
        )
    )
    lines.append("")

    lines.append("## 诊断：收益由哪些公司主导")
    lines.append("### 6个月涨幅前15")
    top_return_rows = []
    for r in sorted(records, key=lambda x: -x["return_6m"])[:15]:
        top_return_rows.append([r["ticker"], r["company"], r["category"], fmt_pct(r["return_6m"]), f"{r['score']:.1f}", str(r["score_rank"]), r["confidence"]])
    lines.append(table(["股票代号", "公司名称", "分类目录", "6个月收益", "F14分", "F14排名", "F14置信度"], top_return_rows))
    lines.append("")
    lines.append(f"### {FEATURE_ID}分数前15")
    top_score_rows = []
    for r in ordered[:15]:
        top_score_rows.append([r["ticker"], r["company"], r["category"], f"{r['score']:.1f}", str(r["score_rank"]), fmt_pct(r["return_6m"]), r["confidence"]])
    lines.append(table(["股票代号", "公司名称", "分类目录", "F14分", "F14排名", "6个月收益", "F14置信度"], top_score_rows))
    lines.append("")
    lines.append("诊断结论：F14高分公司体现未来3-6个月毛利率、经营利润率、EBITDA或EPS margin改善概率，但本窗口股价涨幅前列还包含大量低基数修复、小市值高波动、存储/光互联周期弹性和极端重估标的。F14可以解释一部分利润率改善质量，但不能单独替代价格动量、估值修复或事件催化因子。")
    lines.append("")

    lines.append("## 最终判断与后续使用")
    lines.append(f"- 对“6个月价格涨跌排序”的单因子预测：{FEATURE_ID}_{FEATURE_NAME}本轮评估为{metric_sentence(corr['spearman']).rstrip('。')}，不建议单独用于6个月收益排序。")
    lines.append("- 对风险解释：F14高分组是否更抗跌只能在SOXX压力窗口代理下观察；本次没有逐日价格序列，不能给出严格波动率、最大回撤或下跌日收益结论。")
    lines.append("- 对组合使用：F14更像利润率改善、产品mix、利用率、价格传导和费用杠杆因子。后续应与F05估值赔率、F37-F39催化剂、F50价格相对强度、F51交易流动性、极端涨跌过滤联用。")
    lines.append("- 对上游资料：本报告只作为下游特征评估，不反向修改公司调研、行业调研或日度事实资料。")
    lines.append("")
    lines.append("## 附：关键口径复述")
    lines.append("- 6个月收益：区间涨跌文件中的 `6个月` 字段，百分比单位，不含股息再投资。")
    lines.append("- 低流动性剔除：F51交易流动性分数缺失或不高于 5.0。")
    lines.append("- ADR/币种异常剔除：`listing_type` 非 `common/equity`、ADR比例非不适用、交易货币与财报货币不一致、估值校验含 `currency_mismatch` 或备注提示 ADR/币种需确认。")
    lines.append(f"- 极端涨跌剔除：按本次{len(records)}家6个月收益双尾5%剔除，阈值为 {fmt_pct(low_q)} 和 {fmt_pct(high_q)}。")

    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote={OUTPUT_PATH}")
    print(f"records={len(records)} scores={len(scores)} missing_returns={len(missing_returns)}")
    print(f"pearson={fmt_num(corr['pearson'])} spearman={fmt_num(corr['spearman'])} kendall={fmt_num(corr['kendall'])}")
    print(f"top30={fmt_pct(tb[30]['top_avg'])} bottom30={fmt_pct(tb[30]['bottom_avg'])} diff={fmt_pct(f14_diff)}")
    print(f"combined_spearman={fmt_num(combined_spearman)}")


if __name__ == "__main__":
    main()
