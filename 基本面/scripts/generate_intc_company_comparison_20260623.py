from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
TARGET = "INTC"
TARGET_NAME = "Intel Corporation 英特尔"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "INTC_逐家公司投资思路对比_2026-06-23.md"

EVAL_DIR = ROOT.parent / "分析报告" / "公司评估" / "结果"
INDEX_PATH = ROOT / "公司调研" / "公司索引.md"
FINANCE_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-22.md"
RET_1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-03.md"
RET_2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-03.md"
SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md"

STRATEGIES = [
    "NTM兑现优先",
    "右尾弹性优先",
    "风险调整收益",
    "下行保护优先",
    "估值消化优先",
    "近端催化优先",
    "价格确认/动量",
    "激进短线",
]

LABEL_ORDER = [
    "强烈建议投A",
    "建议投A",
    "微倾向投A",
    "中性",
    "微倾向投B",
    "建议投B",
    "强烈建议投B",
]

GRADE_VALUE = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "资料不足": 0}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r", " ").replace("\n", "<br>")
    text = text.replace("|", "／")
    return text.strip()


def strip_code(text: str) -> str:
    return text.replace("`", "").replace("<br>", " ")


def split_md_row(line: str) -> Optional[list[str]]:
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        return None
    cells = [c.strip() for c in line.strip("|").split("|")]
    if not cells:
        return None
    if all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in cells):
        return None
    return cells


def is_separator(line: str) -> bool:
    cells = line.strip().strip("|").split("|")
    return bool(cells) and all(re.fullmatch(r"\s*:?-{2,}:?\s*", c) for c in cells)


def iter_tables(text: str):
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        header = split_md_row(lines[i])
        if header and is_separator(lines[i + 1]):
            rows: list[dict[str, str]] = []
            i += 2
            while i < len(lines):
                row = split_md_row(lines[i])
                if row is None:
                    break
                if len(row) < len(header):
                    row += [""] * (len(header) - len(row))
                rows.append(dict(zip(header, row)))
                i += 1
            yield header, rows
        i += 1


def parse_percent(text: str) -> Optional[float]:
    if not text or "N/A" in text or "缺失" in text:
        return None
    cleaned = strip_code(text).replace(",", "")
    # Prefer an explicitly signed percentage close to words like up/down.
    matches = re.findall(r"([+-]?\d+(?:\.\d+)?)\s*%", cleaned)
    if not matches:
        return None
    nums = [float(x) for x in matches]
    if "下跌" in cleaned and all(n >= 0 for n in nums):
        nums = [-n for n in nums]
    return sum(nums) / len(nums)


def parse_percent_range(text: str) -> Optional[float]:
    if not text:
        return None
    cleaned = strip_code(text).replace(",", "")
    # Capture signed ranges first: +27%-35%, -5%-+10%, 15%-22%.
    ranges = re.findall(r"([+-]?\d+(?:\.\d+)?)\s*%\s*[-至到]\s*([+-]?\d+(?:\.\d+)?)\s*%", cleaned)
    if ranges:
        a, b = ranges[-1]
        av = float(a)
        bv = float(b)
        if av >= 0 and bv >= 0 and "下跌" in cleaned and "增长" not in cleaned:
            av, bv = -av, -bv
        return (av + bv) / 2
    return parse_percent(cleaned)


def parse_float(text: str) -> Optional[float]:
    if not text or "缺失" in text or "不适用" in text or "N/A" in text:
        return None
    cleaned = strip_code(text).replace(",", "")
    m = re.search(r"[-+]?\d+(?:\.\d+)?", cleaned)
    return float(m.group(0)) if m else None


def parse_money_b(text: str) -> Optional[float]:
    if not text or "缺失" in text:
        return None
    cleaned = strip_code(text).replace(",", "").replace("$", "")
    m = re.search(r"([-+]?\d+(?:\.\d+)?)\s*[-至到]?\s*([-+]?\d+(?:\.\d+)?)?", cleaned)
    if not m:
        return None
    a = float(m.group(1))
    b = float(m.group(2)) if m.group(2) else a
    value = (a + b) / 2
    if "T" in cleaned:
        value *= 1000
    elif "M" in cleaned:
        value /= 1000
    elif "亿" in cleaned:
        value *= 0.1
    return value


def score_confidence(text: str) -> float:
    text = strip_code(text or "")
    if any(x in text for x in ["中高", "高到中高"]):
        return 0.78
    if "高" in text and "低" not in text:
        return 0.88
    if any(x in text for x in ["中低", "低到中低"]):
        return 0.35
    if "低" in text:
        return 0.22
    if "中" in text:
        return 0.56
    return 0.50


def clamp(value: Optional[float], lo: float = 0.0, hi: float = 1.0) -> Optional[float]:
    if value is None or math.isnan(value):
        return None
    return max(lo, min(hi, value))


def section_between(text: str, title: str) -> str:
    m = re.search(rf"^##\s+{re.escape(title)}\s*$", text, flags=re.M)
    if not m:
        return ""
    start = m.end()
    n = re.search(r"^##\s+", text[start:], flags=re.M)
    end = start + n.start() if n else len(text)
    return text[start:end].strip()


def bullet_after(text: str, label: str) -> str:
    m = re.search(rf"[-*]\s*{re.escape(label)}[:：]\s*(.+)", text)
    return m.group(1).strip() if m else ""


def short_phrase(text: str, max_len: int = 80) -> str:
    text = strip_code(text)
    text = re.sub(r"\s+", " ", text).strip(" ：:;；。")
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def normalize_series(items: dict[str, Optional[float]], higher_better: bool = True) -> dict[str, Optional[float]]:
    vals = [(k, v) for k, v in items.items() if v is not None and not math.isnan(v)]
    if not vals:
        return {k: None for k in items}
    sorted_vals = sorted(vals, key=lambda kv: kv[1])
    n = len(sorted_vals)
    ranks: dict[str, float] = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and sorted_vals[j + 1][1] == sorted_vals[i][1]:
            j += 1
        rank = ((i + j) / 2) / (n - 1) if n > 1 else 0.5
        for k, _ in sorted_vals[i : j + 1]:
            ranks[k] = rank
        i = j + 1
    if higher_better:
        return {k: ranks.get(k) for k in items}
    return {k: (None if k not in ranks else 1 - ranks[k]) for k in items}


def mean_present(values: list[Optional[float]], default: Optional[float] = None) -> Optional[float]:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    if not vals:
        return default
    return sum(vals) / len(vals)


def weighted(items: list[tuple[Optional[float], float]], default: Optional[float] = None) -> Optional[float]:
    total = 0.0
    weight = 0.0
    for value, w in items:
        if value is not None and not math.isnan(value):
            total += value * w
            weight += w
    if weight == 0:
        return default
    return total / weight


@dataclass
class Company:
    ticker: str
    name: str
    eval_date: str
    eval_path: Path
    text: str
    category: str = "未分类"
    finance: dict[str, str] = field(default_factory=dict)
    returns: dict[str, Optional[float]] = field(default_factory=dict)
    scenarios: dict[str, dict[str, str]] = field(default_factory=dict)
    metrics: dict[str, Optional[float]] = field(default_factory=dict)
    features: dict[str, float] = field(default_factory=dict)
    scores: dict[str, Optional[float]] = field(default_factory=dict)
    grades: dict[str, str] = field(default_factory=dict)
    ranks: dict[str, Optional[int]] = field(default_factory=dict)
    rank_counts: dict[str, int] = field(default_factory=dict)


def load_latest_reports() -> dict[str, Company]:
    latest: dict[str, tuple[str, Path, str]] = {}
    pattern = re.compile(r"(?P<ticker>[^_]+)_(?P<name>.+)_收入传导估值评估_(?P<date>\d{4}-\d{2}-\d{2})\.md$")
    for path in EVAL_DIR.glob("*_收入传导估值评估_*.md"):
        if not path.is_file():
            continue
        m = pattern.match(path.name)
        if not m:
            continue
        ticker = m.group("ticker")
        date = m.group("date")
        name = m.group("name").replace("_", " ")
        if ticker not in latest or date > latest[ticker][0]:
            latest[ticker] = (date, path, name)
    companies: dict[str, Company] = {}
    for ticker, (date, path, name) in latest.items():
        companies[ticker] = Company(
            ticker=ticker,
            name=name,
            eval_date=date,
            eval_path=path,
            text=read_text(path),
        )
    return dict(sorted(companies.items()))


def load_index_categories() -> dict[str, tuple[str, str]]:
    text = read_text(INDEX_PATH)
    mapping: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        row = split_md_row(line)
        if not row or len(row) < 3 or row[0] == "股票代号":
            continue
        ticker = row[0].strip()
        name = row[1].strip()
        cat = row[2].strip().strip("`").strip("/")
        if re.fullmatch(r"[A-Z0-9.]+", ticker):
            mapping[ticker] = (name, cat)
    return mapping


def load_finance() -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    text = read_text(FINANCE_PATH)
    meta = {
        "finance_file": FINANCE_PATH.relative_to(ROOT).as_posix(),
        "finance_title_date": "2026-06-22",
        "generated": "",
        "price_date": "2026-06-22",
        "source_timestamp": "",
    }
    m = re.search(r"生成时间[:：]\s*([^\n]+)", text)
    if m:
        meta["generated"] = m.group(1).strip()
    m = re.search(r"价格数据日期[:：][^\n]*最新\s*`?(\d{4}-\d{2}-\d{2})`?", text)
    if m:
        meta["price_date"] = m.group(1)
    finance: dict[str, dict[str, str]] = {}
    for header, rows in iter_tables(text):
        if "股票代号" not in header or "最新价格" not in header:
            continue
        for row in rows:
            ticker = row.get("股票代号", "").strip()
            if re.fullmatch(r"[A-Z0-9.]+", ticker):
                finance[ticker] = row
                if not meta["source_timestamp"] and row.get("source_timestamp"):
                    meta["source_timestamp"] = row.get("source_timestamp", "")
    return finance, meta


def load_return_table(path: Path, column_hint: str) -> dict[str, Optional[float]]:
    text = read_text(path)
    out: dict[str, Optional[float]] = {}
    for header, rows in iter_tables(text):
        if "股票代号" not in header:
            continue
        col = None
        for h in header:
            if column_hint in h:
                col = h
                break
        if col is None:
            continue
        for row in rows:
            ticker = row.get("股票代号", "").strip()
            if re.fullmatch(r"[A-Z0-9.]+", ticker):
                out[ticker] = parse_percent(row.get(col, ""))
    return out


def extract_scenarios(text: str) -> dict[str, dict[str, str]]:
    best: dict[str, dict[str, str]] = {}
    for header, rows in iter_tables(text):
        is_company_scenario = (
            "情景" in header
            and any(h == "NTM 公司收入" or h == "NTM收入" for h in header)
            and "绝对增速" in header
        )
        if not is_company_scenario:
            continue
        for row in rows:
            raw_key = strip_code(row.get("情景", "")).strip()
            key = ""
            if "悲观" in raw_key:
                key = "悲观"
            elif "基准" in raw_key:
                key = "基准"
            elif "极度乐观" in raw_key:
                key = "极度乐观"
            elif "乐观" in raw_key:
                key = "乐观"
            if key:
                best[key] = row
        if "基准" in best:
            break
    return best


def count_terms(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(t.lower()) for t in terms)


def build_metrics(companies: dict[str, Company]) -> None:
    for c in companies.values():
        c.scenarios = extract_scenarios(c.text)
        base = c.scenarios.get("基准", {})
        optimistic = c.scenarios.get("乐观", {})
        extreme = c.scenarios.get("极度乐观", {})
        c.metrics["base_growth"] = parse_percent_range(base.get("绝对增速", ""))
        c.metrics["optimistic_growth"] = parse_percent_range(optimistic.get("绝对增速", ""))
        c.metrics["extreme_growth"] = parse_percent_range(extreme.get("绝对增速", ""))
        c.metrics["base_revenue_b"] = parse_money_b(base.get("NTM 公司收入", "") or base.get("NTM收入", ""))
        c.metrics["op_margin"] = parse_percent_range(base.get("经营利润率", ""))
        c.metrics["gross_margin"] = parse_percent_range(base.get("毛利率", ""))
        c.metrics["confidence"] = score_confidence(base.get("可信度", ""))
        c.metrics["extreme_confidence"] = score_confidence(extreme.get("可信度", ""))

        finance = c.finance
        c.metrics["market_cap_b"] = parse_money_b(finance.get("市值", ""))
        c.metrics["price"] = parse_float(finance.get("最新价格", ""))
        c.metrics["forward_pe"] = parse_float(finance.get("Forward PE", ""))
        c.metrics["ttm_pe"] = parse_float(finance.get("TTM PE", ""))
        ps_text = finance.get("P/S", "")
        if "P/S:bad" in finance.get("估值校验", ""):
            c.metrics["ps"] = None
        else:
            c.metrics["ps"] = parse_float(ps_text)
        c.metrics["ev_ebitda"] = parse_float(finance.get("EV/EBITDA", ""))
        c.metrics["ttm_revenue_b"] = parse_money_b(finance.get("ttm_revenue", ""))
        c.metrics["call_iv"] = parse_percent(finance.get("Call IV", ""))
        c.metrics["put_iv"] = parse_percent(finance.get("Put IV", ""))
        c.metrics["iv"] = mean_present([c.metrics["call_iv"], c.metrics["put_iv"]])
        c.metrics["ret_1m"] = c.returns.get("1m")
        c.metrics["ret_2w"] = c.returns.get("2w")
        c.metrics["soxx_pressure"] = c.returns.get("soxx")

        cash_text = " ".join([
            base.get("自由现金流方向", ""),
            bullet_after(section_between(c.text, "8. 结论"), "利润/现金流结论"),
            c.text[:3500],
        ])
        cash_score = 0.45
        if any(x in cash_text for x in ["FCF 正", "自由现金流 `", "自由现金流正", "FCF 仍为正", "现金流强", "现金流稳定", "free cash flow"]):
            cash_score += 0.25
        if any(x in cash_text for x in ["净现金", "资产负债表", "现金储备", "低杠杆"]):
            cash_score += 0.10
        if any(x in cash_text for x in ["现金流为负", "烧钱", "融资", "高杠杆", "working capital 吞噬", "库存和应收"]):
            cash_score -= 0.18
        c.metrics["cash_score"] = clamp(cash_score)

        text = c.text
        c.features["order_visibility"] = clamp(count_terms(text, ["backlog", "RPO", "订单", "合同", "指引", "客户项目", "交付", "预订", "bookings"]) / 34)
        c.features["tail_terms"] = clamp(count_terms(text, ["极度乐观", "非线性", "AI", "hyperscaler", "CPO", "1.6T", "800G", "Blackwell", "Rubin", "HBM", "CoWoS", "液冷", "电力瓶颈", "scale", "右尾"]) / 70)
        c.features["catalyst_terms"] = clamp(count_terms(text, ["Q3", "Q4", "未来 1-2", "未来 12", "财报", "订单", "客户认证", "发布", "量产", "产能", "交付", "指引上修", "backlog", "ramp"]) / 55)
        risk_count = count_terms(text, ["低可信", "未披露", "反证", "客户集中", "ASP 下行", "价格战", "供应链", "认证慢", "现金流为负", "融资", "亏损", "高杠杆", "延迟", "取消"])
        c.features["risk_terms"] = clamp(risk_count / 80)
        c.features["recent_eval"] = 1.0 if c.eval_date >= "2026-06-20" else 0.6 if c.eval_date >= "2026-06-12" else 0.4
        c.features["has_finance"] = 1.0 if finance else 0.0


def assign_scores(companies: dict[str, Company]) -> None:
    raw = defaultdict(dict)
    for t, c in companies.items():
        for key in [
            "base_growth",
            "optimistic_growth",
            "extreme_growth",
            "op_margin",
            "gross_margin",
            "confidence",
            "market_cap_b",
            "forward_pe",
            "ttm_pe",
            "ps",
            "ev_ebitda",
            "iv",
            "ret_1m",
            "ret_2w",
            "soxx_pressure",
            "cash_score",
        ]:
            raw[key][t] = c.metrics.get(key)

    norm = {
        "base_growth": normalize_series(raw["base_growth"], True),
        "optimistic_growth": normalize_series(raw["optimistic_growth"], True),
        "extreme_growth": normalize_series(raw["extreme_growth"], True),
        "op_margin": normalize_series(raw["op_margin"], True),
        "gross_margin": normalize_series(raw["gross_margin"], True),
        "confidence": normalize_series(raw["confidence"], True),
        "market_cap": normalize_series(raw["market_cap_b"], True),
        "small_cap": normalize_series(raw["market_cap_b"], False),
        "fwdpe_low": normalize_series(raw["forward_pe"], False),
        "ttmpe_low": normalize_series(raw["ttm_pe"], False),
        "ps_low": normalize_series(raw["ps"], False),
        "ev_low": normalize_series(raw["ev_ebitda"], False),
        "iv_low": normalize_series(raw["iv"], False),
        "iv_high": normalize_series(raw["iv"], True),
        "ret_1m": normalize_series(raw["ret_1m"], True),
        "ret_2w": normalize_series(raw["ret_2w"], True),
        "soxx": normalize_series(raw["soxx_pressure"], True),
        "cash": normalize_series(raw["cash_score"], True),
    }

    for t, c in companies.items():
        valuation = weighted(
            [
                (norm["fwdpe_low"].get(t), 0.36),
                (norm["ps_low"].get(t), 0.34),
                (norm["ev_low"].get(t), 0.20),
                (norm["ttmpe_low"].get(t), 0.10),
            ],
            default=None,
        )
        if valuation is not None:
            pe = c.metrics.get("forward_pe")
            ps = c.metrics.get("ps")
            ev = c.metrics.get("ev_ebitda")
            if pe is not None and pe > 80:
                valuation -= 0.08
            if ps is not None and ps > 35:
                valuation -= 0.08
            if ev is not None and ev > 100:
                valuation -= 0.04
            valuation = clamp(valuation)
        c.metrics["valuation_rank"] = valuation

        growth_base = norm["base_growth"].get(t)
        optimistic = norm["optimistic_growth"].get(t)
        extreme = norm["extreme_growth"].get(t)
        evidence = weighted([(norm["confidence"].get(t), 0.55), (c.features["order_visibility"], 0.45)], default=0.45)
        profit = weighted([(norm["op_margin"].get(t), 0.65), (norm["gross_margin"].get(t), 0.35)], default=0.45)
        cash = weighted([(norm["cash"].get(t), 0.7), (c.metrics["cash_score"], 0.3)], default=0.45)
        risk_penalty = c.features["risk_terms"] * 0.16

        ntm = weighted(
            [
                (growth_base, 0.34),
                (evidence, 0.26),
                (c.features["order_visibility"], 0.15),
                (profit, 0.12),
                (cash, 0.13),
            ],
            default=None,
        )
        c.scores["NTM兑现优先"] = clamp(None if ntm is None else ntm - risk_penalty)

        tail = weighted(
            [
                (extreme, 0.30),
                (optimistic, 0.23),
                (c.features["tail_terms"], 0.18),
                (norm["iv_high"].get(t), 0.10),
                (norm["small_cap"].get(t), 0.08),
                (c.features["catalyst_terms"], 0.11),
            ],
            default=None,
        )
        if tail is not None:
            tail -= max(0, 0.55 - c.metrics.get("extreme_confidence", 0.5)) * 0.07
        c.scores["右尾弹性优先"] = clamp(tail)

        downside = weighted(
            [
                (norm["soxx"].get(t), 0.28),
                (norm["market_cap"].get(t), 0.18),
                (norm["iv_low"].get(t), 0.20),
                (cash, 0.17),
                (valuation, 0.11),
                (profit, 0.06),
            ],
            default=None,
        )
        if c.features["has_finance"] == 0:
            downside = None
        c.scores["下行保护优先"] = clamp(None if downside is None else downside - c.features["risk_terms"] * 0.12)

        valuation_digest = weighted(
            [
                (valuation, 0.35),
                (growth_base, 0.24),
                (profit, 0.18),
                (cash, 0.11),
                (evidence, 0.12),
            ],
            default=None,
        )
        if c.features["has_finance"] == 0 or valuation is None:
            valuation_digest = None
        c.scores["估值消化优先"] = clamp(None if valuation_digest is None else valuation_digest - c.features["risk_terms"] * 0.08)

        risk_adj = weighted(
            [
                (c.scores["NTM兑现优先"], 0.28),
                (valuation_digest, 0.25),
                (c.scores["下行保护优先"], 0.25),
                (c.scores["右尾弹性优先"], 0.12),
                (cash, 0.10),
            ],
            default=None,
        )
        c.scores["风险调整收益"] = clamp(None if risk_adj is None else risk_adj - c.features["risk_terms"] * 0.06)

        catalyst = weighted(
            [
                (c.features["catalyst_terms"], 0.34),
                (c.features["order_visibility"], 0.22),
                (c.features["recent_eval"], 0.13),
                (growth_base, 0.14),
                (norm["ret_2w"].get(t), 0.10),
                (evidence, 0.07),
            ],
            default=None,
        )
        c.scores["近端催化优先"] = clamp(None if catalyst is None else catalyst - c.features["risk_terms"] * 0.06)

        momentum = weighted(
            [
                (norm["ret_2w"].get(t), 0.43),
                (norm["ret_1m"].get(t), 0.34),
                (evidence, 0.10),
                (norm["iv_low"].get(t), 0.05),
                (c.features["order_visibility"], 0.08),
            ],
            default=None,
        )
        if c.features["has_finance"] == 0 or c.metrics.get("ret_1m") is None or c.metrics.get("ret_2w") is None:
            momentum = None
        if momentum is not None:
            ret_1m = c.metrics.get("ret_1m")
            if ret_1m is not None and ret_1m > 90:
                momentum -= 0.06
        c.scores["价格确认/动量"] = clamp(momentum)

        aggressive = weighted(
            [
                (c.scores["右尾弹性优先"], 0.30),
                (norm["iv_high"].get(t), 0.22),
                (norm["ret_2w"].get(t), 0.18),
                (c.features["catalyst_terms"], 0.16),
                (norm["small_cap"].get(t), 0.09),
                (norm["ret_1m"].get(t), 0.05),
            ],
            default=None,
        )
        if c.features["has_finance"] == 0:
            aggressive = None
        c.scores["激进短线"] = clamp(None if aggressive is None else aggressive - c.features["risk_terms"] * 0.05)


def assign_grades(companies: dict[str, Company]) -> None:
    for strat in STRATEGIES:
        valid = [(t, c.scores.get(strat)) for t, c in companies.items() if c.scores.get(strat) is not None]
        valid.sort(key=lambda kv: kv[1], reverse=True)
        n = len(valid)
        for rank, (t, score) in enumerate(valid, start=1):
            pct = (rank - 1) / max(1, n - 1)
            if pct < 0.08:
                grade = "S"
            elif pct < 0.25:
                grade = "A"
            elif pct < 0.50:
                grade = "B"
            elif pct < 0.80:
                grade = "C"
            else:
                grade = "D"
            companies[t].grades[strat] = grade
            companies[t].ranks[strat] = rank
            companies[t].rank_counts[strat] = n
        for t, c in companies.items():
            if strat not in c.grades:
                c.grades[strat] = "资料不足"
                c.ranks[strat] = None
                c.rank_counts[strat] = n


def relation_for(b: Company) -> str:
    cat = b.category
    if cat == "AI计算芯片_EDA_IP_custom_ASIC":
        if b.ticker in {"AMD", "ARM", "AVGO", "MRVL", "NVDA", "QCOM"}:
            return "直接同业"
        if b.ticker in {"CDNS", "SNPS"}:
            return "上下游"
        return "相邻替代"
    if cat == "晶圆制造_前道设备":
        if b.ticker in {"TSM", "GFS", "UMC", "TSEM"}:
            return "直接同业"
        return "上下游"
    if cat == "AI服务器_存储_EMS":
        return "上下游"
    if cat == "AI网络_光互联_连接器":
        if b.ticker in {"ANET", "CSCO", "NOK", "VISN"}:
            return "相邻替代"
        return "上下游"
    if cat == "云算力_IDC_AI软件平台":
        return "上下游"
    if cat in {"配电_电源_功率器件", "电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    return "跨赛道"


def strength_label(side: str, diff: int, score_diff: float, relation: str, missing: bool) -> str:
    if missing:
        if abs(score_diff) < 0.08:
            return "中性"
        return f"微倾向投{side}"
    if diff >= 3:
        label = f"强烈建议投{side}"
    elif diff == 2:
        label = f"建议投{side}"
    elif diff == 1:
        label = f"微倾向投{side}"
    else:
        if abs(score_diff) >= 0.12:
            label = f"微倾向投{side}"
        else:
            return "中性"
    if relation == "跨赛道":
        if label.startswith("强烈"):
            label = f"建议投{side}"
        elif label.startswith("建议") and diff <= 2:
            label = f"微倾向投{side}"
    if relation == "直接同业" and label.startswith("微倾向") and abs(score_diff) >= 0.16:
        label = f"建议投{side}"
    return label


def reason_for(strat: str, label: str, b: Company, relation: str) -> str:
    if label == "中性":
        if relation == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"
    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "INTC CCG/DCAI和Q2指引兑现更清楚",
            "右尾弹性优先": "INTC 18A、IPU和AI host CPU仍有右尾",
            "风险调整收益": "INTC估值低且复苏赔率更均衡",
            "下行保护优先": "INTC规模、战略资产和现金流底盘更稳",
            "估值消化优先": "INTC低P/S和利润修复更能消化估值",
            "近端催化优先": "INTC Q2/Q3 DCAI和18A进展更近",
            "价格确认/动量": "INTC价格确认较强但需防过热",
            "激进短线": "INTC高IV、转型叙事和政策关注可交易",
        }[strat]
    return {
        "NTM兑现优先": f"{b.ticker} NTM兑现证据更强",
        "右尾弹性优先": f"{b.ticker}右尾空间或小基数弹性更大",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}当前估值更易被业绩消化",
        "近端催化优先": f"{b.ticker}近端事件重定价概率更高",
        "价格确认/动量": f"{b.ticker}价格趋势确认更强",
        "激进短线": f"{b.ticker}短线波动和资金关注更强",
    }[strat]


def decision_for(a: Company, b: Company, strat: str, relation: str) -> str:
    ga = a.grades[strat]
    gb = b.grades[strat]
    sa = a.scores.get(strat)
    sb = b.scores.get(strat)
    missing = ga == "资料不足" or gb == "资料不足"
    score_diff = (sa if sa is not None else 0.5) - (sb if sb is not None else 0.5)
    diff = GRADE_VALUE.get(ga, 0) - GRADE_VALUE.get(gb, 0)
    if diff > 0 or (diff == 0 and score_diff > 0.04):
        label = strength_label("A", diff, score_diff, relation, missing)
    elif diff < 0 or (diff == 0 and score_diff < -0.04):
        label = strength_label("B", -diff, score_diff, relation, missing)
    else:
        label = "中性"
    return f"{label}：{reason_for(strat, label, b, relation)}"


def label_side(cell: str) -> str:
    label = cell.split("：", 1)[0]
    if label.endswith("投A"):
        return "A"
    if label.endswith("投B"):
        return "B"
    return "N"


def grade_summary(a: Company, b: Company) -> str:
    a_strong = []
    b_strong = []
    near = []
    short_names = {
        "NTM兑现优先": "NTM",
        "右尾弹性优先": "右尾",
        "风险调整收益": "风险收益",
        "下行保护优先": "下行",
        "估值消化优先": "估值",
        "近端催化优先": "催化",
        "价格确认/动量": "动量",
        "激进短线": "短线",
    }
    for strat in STRATEGIES:
        diff = GRADE_VALUE[a.grades[strat]] - GRADE_VALUE[b.grades[strat]]
        if diff >= 1:
            a_strong.append(short_names[strat])
        elif diff <= -1:
            b_strong.append(short_names[strat])
        else:
            near.append(short_names[strat])
    parts = []
    if a_strong:
        parts.append("A强：" + "、".join(a_strong[:4]))
    if b_strong:
        parts.append("B强：" + "、".join(b_strong[:4]))
    if near:
        parts.append("接近：" + "、".join(near[:3]))
    return "；".join(parts)


def final_choice(decisions: dict[str, str], b: Company) -> tuple[str, str, str]:
    counts = Counter(label_side(v) for v in decisions.values())
    a_count, b_count, n_count = counts["A"], counts["B"], counts["N"]
    if a_count > b_count:
        final = TARGET
        reason = "INTC在多数思路下更均衡，尤其估值消化、近端催化或复苏弹性不弱。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，INTC需要更强DCAI收入、Foundry亏损收窄或现金流证据。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = TARGET
            reason = "多数思路打平时，风险调整收益更支持INTC。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = TARGET
                reason = "多数思路打平，INTC复苏赔率和估值消化略更清楚。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def format_grade_position(c: Company, strat: str) -> str:
    rank = c.ranks.get(strat)
    n = c.rank_counts.get(strat, 0)
    if rank is None:
        return "资料不足"
    pct = rank / max(1, n)
    if pct <= 0.08:
        loc = "全项目顶层"
    elif pct <= 0.25:
        loc = "全项目强势层"
    elif pct <= 0.50:
        loc = "全项目中上层"
    elif pct <= 0.80:
        loc = "全项目中性层"
    else:
        loc = "全项目弱势层"
    return f"{loc}，第 {rank}/{n}"


def grade_support_limit(strat: str, c: Company) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "Q2收入指引、CCG底盘、DCAI double-digit q/q和Google/IPU客户路径",
        "右尾弹性优先": "18A/14A、external Foundry、custom IPU、Xeon AI host CPU和rackscale inference期权",
        "风险调整收益": "低P/S、复苏弹性、战略资产和DCAI/CCG利润底盘提供赔率",
        "下行保护优先": "大规模收入、PC/CPU底盘、政策战略属性和低P/S提供部分支撑",
        "估值消化优先": "P/S约6.36、NTM 57-60B基准收入和non-GAAP利润修复可消化部分估值",
        "近端催化优先": "Q2/Q3收入毛利、DCAI server CPU、other DCAI、18A yield和external Foundry revenue",
        "价格确认/动量": "1个月涨幅为正，2026-06-22价格较6月初继续上行",
        "激进短线": "高IV、Intel转型、18A/Foundry和AI host CPU叙事带来短线进攻性",
    }[strat]
    limit = {
        "NTM兑现优先": "供给约束贯穿2026，18A early ramp和input cost压制毛利",
        "右尾弹性优先": "Gaudi/future accelerator、18A外部大单和先进封装NTM收入证据仍不足",
        "风险调整收益": "Foundry亏损、GAAP扰动、负EPS和高IV会放大执行风险",
        "下行保护优先": "SOXX压力窗口累计跌幅大，FCF和Foundry亏损尚未真正稳定",
        "估值消化优先": "forward PE约91倍且TTM EPS为负，利润修复必须兑现",
        "近端催化优先": "若Q2/Q3毛利或DCAI供给低于预期，催化会迅速转成反证",
        "价格确认/动量": "两周区间曾下跌，价格/IV需要用后续行情刷新避免追高",
        "激进短线": "高IV同时意味着回撤风险，且相对小基数AI链爆发倍数有限",
    }[strat]
    return support, limit


def make_report(companies: dict[str, Company]) -> str:
    a = companies[TARGET]
    rows = []
    stats: dict[str, Counter] = {s: Counter() for s in STRATEGIES}
    b_rank_rows = []
    a_rank_rows = []
    decisions_by_b: dict[str, dict[str, str]] = {}

    sorted_bs = [c for t, c in companies.items() if t != TARGET]
    sorted_bs.sort(key=lambda c: (c.category, c.ticker))

    for idx, b in enumerate(sorted_bs, start=1):
        relation = relation_for(b)
        decisions = {s: decision_for(a, b, s, relation) for s in STRATEGIES}
        decisions_by_b[b.ticker] = decisions
        for s, cell in decisions.items():
            stats[s][cell.split("：", 1)[0]] += 1
        majority, final, final_reason = final_choice(decisions, b)
        counts = Counter(label_side(v) for v in decisions.values())
        row = [
            str(idx),
            f"{b.ticker} / {b.name}",
            b.category,
            relation,
            grade_summary(a, b),
            *[decisions[s] for s in STRATEGIES],
            majority,
            final,
            final_reason,
        ]
        rows.append(row)
        diff = counts["B"] - counts["A"]
        if diff >= 3:
            b_rank_rows.append((diff, counts["B"], b, decisions))
        if -diff >= 3:
            a_rank_rows.append((-diff, counts["A"], b, decisions))

    a_majority_wins = sum(1 for b, ds in decisions_by_b.items() if final_choice(ds, companies[b])[1] == TARGET)
    b_majority_wins = len(sorted_bs) - a_majority_wins

    by_strategy_a = {s: stats[s]["强烈建议投A"] + stats[s]["建议投A"] + stats[s]["微倾向投A"] for s in STRATEGIES}
    by_strategy_b = {s: stats[s]["强烈建议投B"] + stats[s]["建议投B"] + stats[s]["微倾向投B"] for s in STRATEGIES}
    a_best = max(STRATEGIES, key=lambda s: by_strategy_a[s])
    a_worst = max(STRATEGIES, key=lambda s: by_strategy_b[s])
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:8]
    strongest_b_names = "、".join(f"{b.ticker}" for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])

    one_page = [
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；核心来自低P/S、DCAI/CCG复苏、18A/Foundry期权和高波动带来的重定价空间。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；主要输给现金流更稳、AI增速更确定、订单更硬或压力期更抗跌的公司。",
        "- A 最适合的投资者画像：愿意承受高波动，押注 Intel 从PC/CPU周期修复、DCAI增长、18A良率和Foundry亏损收窄中获得再定价的投资者。",
        "- A 最不适合的投资者画像：只追求低回撤、确定性现金流、已验证AI加速器收入或不愿承担Foundry执行风险的人。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：INTC 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后，属于高争议复苏/右尾标的；赔率来自低基数和转型，质量与确定性明显弱于AI链顶级赢家。",
        "- 后续最重要跟踪数据：Q2/Q3收入和毛利、DCAI revenue/server ASP与volume、other DCAI product revenue、Google/IPU项目、18A yield/throughput、external Foundry revenue、Foundry OPM、adjusted FCF、客户deposits和供应商预付款。",
    ]

    a_intro = section_between(a.text, "1. 一页结论")
    conclusion = section_between(a.text, "8. 结论")
    products = bullet_after(a_intro, "重要产品/业务线")
    ntm = a.scenarios.get("基准", {}).get("NTM 公司收入", "")
    optimistic = " / ".join(
        filter(
            None,
            [
                a.scenarios.get("乐观", {}).get("NTM 公司收入", ""),
                a.scenarios.get("极度乐观", {}).get("NTM 公司收入", ""),
            ],
        )
    )
    profit_cash = bullet_after(conclusion, "利润/现金流结论") or bullet_after(a_intro, "利润或 EBITDA 四情景")
    bottleneck = bullet_after(conclusion, "主要传导瓶颈") or bullet_after(a_intro, "最大传导瓶颈")
    bear = bullet_after(conclusion, "悲观情景触发条件") or "PC TAM弱化、DCAI供给或ASP失速、18A拉低毛利、Foundry亏损不收窄是主要反证入口。"
    catalysts = bullet_after(conclusion, "乐观情景成立条件") or bullet_after(conclusion, "后续跟踪数据")

    lines = []
    lines.append("# INTC 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：INTC / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、`金融资料/每日金融数据/每日金融数据_2026-06-22.md` 和 `金融资料/区间涨跌/` 三个正式行情文件。未读取、引用或继承 `特征量化/`、Signals、回归、模型比较或 `公司排序/` 的现成排序结果；`备份/` 与 `tmp/` 不作为决策输入。")
    if missing_finance:
        lines.append(f"> 金融资料覆盖差异：正式评估公司 {len(companies)} 家，最新金融快照覆盖 {len(companies) - len(missing_finance)} 家；缺少日度金融明细的公司为 {', '.join(missing_finance)}，价格/估值/IV/动量相关档位按资料不足或低置信处理。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.extend(one_page)
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append(f"| 股票代号 | INTC |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {md_escape(short_phrase(products, 240))} |")
    lines.append(f"| NTM 基准收入 | {md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {md_escape(short_phrase(profit_cash, 220))} |")
    lines.append(f"| 最大传导瓶颈 | {md_escape(short_phrase(bottleneck, 220))} |")
    lines.append(f"| 最大反证 | {md_escape(short_phrase(bear, 220))} |")
    lines.append(f"| 近端催化剂 | {md_escape(short_phrase(catalysts, 220))} |")
    lines.append("")

    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in STRATEGIES:
        sup, lim = grade_support_limit(strat, a)
        lines.append(f"| {strat} | {a.grades[strat]} | {format_grade_position(a, strat)} | {md_escape(sup)} | {md_escape(lim)} |")
    lines.append("")

    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 与 INTC 在CPU、AI加速/主机CPU、custom ASIC/IPU、晶圆代工或数据中心芯片资金池中直接争夺客户、份额或配置权重 | AMD、NVDA、ARM、AVGO、MRVL、QCOM、TSM、GFS、UMC、TSEM | 同档或相邻档必须复核份额、产品代际、客户项目、利润质量和同业估值，直接证据可放大到建议级别 |")
    lines.append("| 相邻替代 | 同属AI基础设施或半导体资金篮子，但产品不直接竞争，重点比较增长质量、兑现确定性和赔率 | ALAB、CRDO、ANET、DELL、VRT、ETN、GEV | 默认按档位判断，除非增长、估值或催化显著拉开，否则少用强烈建议 |")
    lines.append("| 上下游 | EDA、设备、材料、云厂、服务器和网络供应商与 INTC 处于制造、芯片、系统或客户需求链上下游 | CDNS、SNPS、ASML、AMAT、AMZN、MSFT、GOOGL、SMCI | 强调利润池和议价权，不把云厂收入规模、设备瓶颈或Intel战略属性自动等同为胜出 |")
    lines.append("| 跨赛道 | 电力、冷却、工业、化工、医疗工具等与 INTC 业务差异大，但仍可作为资金配置替代 | CEG、VST、LIN、ECL、TMO、DHR | 默认降低结论力度；若证据互有强弱，优先微倾向或中性 |")
    lines.append("")

    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    headers = [
        "序号",
        "公司B",
        "公司B分类",
        "可比关系",
        "档位差摘要",
        *STRATEGIES,
        "多数思路方向",
        "最终更值得投",
        "最关键理由",
    ]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---:" if h == "序号" else "---" for h in headers]) + " |")
    for row in rows:
        lines.append("| " + " | ".join(md_escape(x) for x in row) + " |")
    lines.append("")

    lines.append("## 6. 投资思路统计")
    lines.append("")
    stat_headers = ["投资思路", *LABEL_ORDER, "A侧合计", "B侧合计"]
    lines.append("| " + " | ".join(stat_headers) + " |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strat in STRATEGIES:
        counter = stats[strat]
        a_total = counter["强烈建议投A"] + counter["建议投A"] + counter["微倾向投A"]
        b_total = counter["强烈建议投B"] + counter["建议投B"] + counter["微倾向投B"]
        vals = [str(counter[label]) for label in LABEL_ORDER]
        lines.append(f"| {strat} | " + " | ".join(vals) + f" | {a_total} | {b_total} |")
    lines.append("")

    def winning_strats(decisions: dict[str, str], side: str) -> str:
        out = [s for s, cell in decisions.items() if label_side(cell) == side]
        return "、".join(out) if out else "无"

    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于INTC，且多数思路下增长、兑现、下行保护、估值消化或价格证据更强。 | INTC需要DCAI连续兑现、18A良率改善、Foundry亏损明显收窄、FCF转正并刷新价格确认。 |"
        )
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过INTC | 继续跟踪DCAI、18A、Foundry亏损和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'A')} | INTC相对{b.ticker}的估值消化、转型右尾、近端催化或交易弹性更清楚。 | {b.ticker}需要更硬的NTM订单/利润兑现、估值消化证据和价格确认。 |"
        )
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | INTC没有在多数思路下明显压过其他公司 | 需等待DCAI、18A、Foundry和现金流进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md` 用于公司名称和分类；INTC 评估报告内已列出的公司调研、行业调研和官方财报/IR来源用于 A 侧业务证据。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    companies = load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("INTC not found in formal company evaluation universe")

    index = load_index_categories()
    finance, _ = load_finance()
    ret_1m = load_return_table(RET_1M_PATH, "过去1个月涨跌幅")
    ret_2w = load_return_table(RET_2W_PATH, "过去两周涨跌幅")
    soxx = load_return_table(SOXX_PATH, "三段累计涨跌幅")

    for ticker, c in companies.items():
        if ticker in index:
            idx_name, cat = index[ticker]
            c.category = cat
            if c.name.replace(" ", "") == ticker:
                c.name = idx_name
        c.finance = finance.get(ticker, {})
        c.returns = {"1m": ret_1m.get(ticker), "2w": ret_2w.get(ticker), "soxx": soxx.get(ticker)}

    build_metrics(companies)
    assign_scores(companies)
    assign_grades(companies)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={OUT_PATH.stat().st_size}")
    print("INTC grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})


if __name__ == "__main__":
    main()

