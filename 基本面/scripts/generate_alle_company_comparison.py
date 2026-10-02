from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(r"D:\investment\基本面")
EVAL_DIR = ROOT.parent / "分析报告" / "公司评估" / "结果"
OUT_DIR = ROOT.parent / "分析报告" / "公司对比" / "结果"
OUT_PATH = OUT_DIR / "ALLE_逐家公司投资思路对比_2026-06-23.md"
FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-22.md"
MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-03.md"
MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-03.md"
SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md"
COMPANY_INDEX = ROOT / "公司调研" / "公司索引.md"

TARGET = "ALLE"
REPORT_DATE = "2026-06-23"
STRATS = [
    "NTM兑现优先",
    "右尾弹性优先",
    "风险调整收益",
    "下行保护优先",
    "估值消化优先",
    "近端催化优先",
    "价格确认/动量",
    "激进短线",
]
TAG_ORDER = ["强烈建议投A", "建议投A", "微倾向投A", "中性", "微倾向投B", "建议投B", "强烈建议投B"]
TIER_VAL = {"D": 1, "C": 2, "B": 3, "A": 4, "S": 5, "资料不足": None}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def clean(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\ufeff", "").replace("<br>", "；").replace("<br/>", "；").replace("<br />", "；")
    return re.sub(r"\s+", " ", text).strip()


def split_md_row(line: str) -> list[str] | None:
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        return None
    return [clean(part) for part in line.strip("|").split("|")]


def is_sep(cells: list[str]) -> bool:
    return not cells or all(re.fullmatch(r":?-{2,}:?", cell.replace(" ", "")) for cell in cells)


def parse_tables(text: str) -> list[list[list[str]]]:
    lines = text.splitlines()
    tables: list[list[list[str]]] = []
    index = 0
    while index < len(lines):
        if not lines[index].strip().startswith("|"):
            index += 1
            continue
        rows: list[list[str]] = []
        while index < len(lines) and lines[index].strip().startswith("|"):
            cells = split_md_row(lines[index])
            if cells and not is_sep(cells):
                rows.append(cells)
            index += 1
        if rows:
            tables.append(rows)
    return tables


def section(text: str, heading_pattern: str, next_pattern: str) -> str:
    match = re.search(heading_pattern, text, flags=re.M)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(next_pattern, text[start:], flags=re.M)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()


def pct_values(value: str) -> list[float]:
    text = clean(value).replace("−", "-")
    return [float(match.group(1)) for match in re.finditer(r"([+-]?\d+(?:\.\d+)?)\s*%", text)]


def pct_mid(value: str) -> float | None:
    values = pct_values(value)
    return sum(values) / len(values) if values else None


def parse_pct_text(value: str) -> float | None:
    values = pct_values(value)
    return values[0] if values else None


def num_cell(value: str) -> float | None:
    text = clean(value).replace(",", "")
    if text in {"", "缺失", "缺失/需确认", "不适用"}:
        return None
    match = re.search(r"([+-]?\d+(?:\.\d+)?)", text)
    return float(match.group(1)) if match else None


def money_cell_b(value: str) -> float | None:
    text = clean(value).replace(",", "")
    if text in {"", "缺失", "缺失/需确认", "不适用"}:
        return None
    mult = 1.0
    if "T" in text:
        mult = 1000.0
    elif "B" in text:
        mult = 1.0
    elif "M" in text:
        mult = 0.001
    match = re.search(r"([+-]?\d+(?:\.\d+)?)", text)
    return float(match.group(1)) * mult if match else None


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def conf_score(value: str) -> int:
    text = clean(value)
    if "高" in text and "中" not in text and "低" not in text:
        return 14
    if "中高" in text:
        return 10
    if "中到低" in text or "低到中" in text:
        return -2
    if "中" in text and "低" not in text:
        return 5
    if "低" in text:
        return -8
    return 0


def md(value: object) -> str:
    return clean(value).replace("|", "/").replace("\n", " ")


def row(cells: list[object]) -> str:
    return "| " + " | ".join(md(cell) for cell in cells) + " |"


def parse_company_index() -> dict[str, dict[str, str]]:
    mapping: dict[str, dict[str, str]] = {}
    if not COMPANY_INDEX.exists():
        return mapping
    for line in read(COMPANY_INDEX).splitlines():
        if not line.startswith("|") or "---" in line or "股票代号" in line:
            continue
        cells = split_md_row(line)
        if cells and len(cells) >= 3 and re.fullmatch(r"[A-Z0-9.]+", cells[0]):
            mapping[cells[0]] = {"name": cells[1], "category": cells[2].strip("`/")}
    return mapping


def latest_eval_files() -> dict[str, dict[str, object]]:
    latest: dict[str, dict[str, object]] = {}
    for path in EVAL_DIR.glob("*_收入传导估值评估_*.md"):
        match = re.match(r"^([^_]+)_(.+)_收入传导估值评估_(\d{4}-\d{2}-\d{2})\.md$", path.name)
        if not match:
            continue
        ticker, slug, date = match.groups()
        if ticker not in latest or date > str(latest[ticker]["date"]):
            latest[ticker] = {"ticker": ticker, "slug": slug, "date": date, "path": path}
    return latest


def parse_financial() -> dict[str, dict[str, object]]:
    data: dict[str, dict[str, object]] = {}
    category = ""
    for line in read(FIN_PATH).splitlines():
        heading = re.match(r"^###\s+(.+)", line.strip())
        if heading:
            category = heading.group(1).strip()
            continue
        if not line.startswith("|") or "---" in line or "股票代号" in line:
            continue
        cells = split_md_row(line)
        if not cells or len(cells) < 25 or not re.fullmatch(r"[A-Z0-9.]+", cells[0]):
            continue
        data[cells[0]] = {
            "category": category,
            "name": cells[1],
            "price_date": cells[2],
            "price": num_cell(cells[3]),
            "market_cap_b": money_cell_b(cells[4]),
            "ttm_pe": num_cell(cells[5]),
            "forward_pe": num_cell(cells[6]),
            "ps": num_cell(cells[7]),
            "pb": num_cell(cells[8]),
            "ev_ebitda": num_cell(cells[9]),
            "eps": num_cell(cells[10]),
            "call_iv": parse_pct_text(cells[11]),
            "put_iv": parse_pct_text(cells[12]),
            "currency": cells[13],
            "financial_currency": cells[14],
            "shares_outstanding": cells[15],
            "ttm_revenue": cells[16],
            "ttm_revenue_b": money_cell_b(cells[16]),
            "ttm_eps": num_cell(cells[17]),
            "forward_eps": num_cell(cells[18]),
            "listing_type": cells[19],
            "source_timestamp": cells[22],
            "valuation_check": cells[23],
            "notes": cells[24],
        }
    return data


def parse_momentum(path: Path, key: str) -> dict[str, dict[str, object]]:
    data: dict[str, dict[str, object]] = {}
    category = ""
    for line in read(path).splitlines():
        heading = re.match(r"^###\s+(.+)", line.strip())
        if heading:
            category = heading.group(1).strip()
            continue
        if not line.startswith("|") or "---" in line or "股票代号" in line:
            continue
        cells = split_md_row(line)
        if not cells or len(cells) < 7 or not re.fullmatch(r"[A-Z0-9.]+", cells[0]):
            continue
        data[cells[0]] = {
            "category": category,
            "latest_trade_date": cells[2],
            "latest_close": num_cell(cells[3]),
            "base_trade_date": cells[4],
            "base_close": num_cell(cells[5]),
            key: parse_pct_text(cells[6]),
        }
    return data


def parse_soxx() -> dict[str, dict[str, object]]:
    data: dict[str, dict[str, object]] = {}
    category = ""
    for line in read(SOXX_PATH).splitlines():
        heading = re.match(r"^###\s+(.+)", line.strip())
        if heading:
            category = heading.group(1).strip()
            continue
        if not line.startswith("|") or "---" in line or "股票代号" in line:
            continue
        cells = split_md_row(line)
        if not cells or len(cells) < 6 or not re.fullmatch(r"[A-Z0-9.]+", cells[0]):
            continue
        data[cells[0]] = {
            "category": category,
            "soxx1": parse_pct_text(cells[2]),
            "soxx2": parse_pct_text(cells[3]),
            "soxx3": parse_pct_text(cells[4]),
            "soxx_cum": parse_pct_text(cells[5]),
        }
    return data


def extract_eval(info: dict[str, object]) -> dict[str, object]:
    text = read(info["path"])  # type: ignore[arg-type]
    one = section(text, r"^##\s*1\.\s*一页结论\s*$", r"^##\s*2\.")
    conclusion = section(text, r"^##\s*8\.\s*结论\s*$", r"^##\s*附录")
    products = section(text, r"^##\s*2\.\s*重要产品清单\s*$", r"^##\s*3\.")
    scenario_text = section(text, r"^##\s*6\.\s*公司收入和利润四情景\s*$", r"^##\s*7\.")
    calibration = section(text, r"^##\s*7\.\s*证据校准、反证和可信度\s*$", r"^##\s*8\.")
    scenarios: dict[str, dict[str, str]] = {}
    for table in parse_tables(scenario_text):
        header = table[0]
        if not header or "情景" not in header[0] or not any("收入" in h for h in header):
            continue
        for item in table[1:]:
            if len(item) < len(header):
                item += [""] * (len(header) - len(item))
            record = dict(zip(header, item))
            key = item[0]
            if "悲观" in key:
                scenarios["bear"] = record
            elif "基准" in key:
                scenarios["base"] = record
            elif "极度乐观" in key:
                scenarios["extreme"] = record
            elif "乐观" in key:
                scenarios["bull"] = record

    def from_scenario(which: str, needle: str) -> str:
        for key, value in scenarios.get(which, {}).items():
            if needle in key:
                return value
        return ""

    def growth(which: str) -> float | None:
        for key, value in scenarios.get(which, {}).items():
            if "增速" in key or "绝对" in key:
                mid = pct_mid(value)
                if mid is not None:
                    return mid
        return None

    product_rows: list[list[str]] = []
    for table in parse_tables(products):
        if table and "产品/业务线" in table[0][0]:
            product_rows = table[1:]
            break

    bullets = []
    for line in (one + "\n" + conclusion).splitlines():
        line = line.strip()
        if line.startswith("- "):
            bullets.append(clean(line[2:]))

    return {
        "text": text,
        "one": one,
        "conclusion": conclusion,
        "products": product_rows,
        "scenario_text": scenario_text,
        "calibration": calibration,
        "scenarios": scenarios,
        "base_growth": growth("base"),
        "bull_growth": growth("bull"),
        "extreme_growth": growth("extreme"),
        "bear_growth": growth("bear"),
        "base_conf": from_scenario("base", "可信"),
        "bull_conf": from_scenario("bull", "可信"),
        "extreme_conf": from_scenario("extreme", "可信"),
        "base_rev": from_scenario("base", "收入"),
        "bull_rev": from_scenario("bull", "收入"),
        "extreme_rev": from_scenario("extreme", "收入"),
        "base_margin": from_scenario("base", "经营利润率"),
        "base_profit": from_scenario("base", "EBITDA") or from_scenario("base", "净利润"),
        "base_cash": from_scenario("base", "现金"),
        "base_bottleneck": from_scenario("base", "瓶颈"),
        "bullets": bullets[:12],
    }


def pct_rank(value: float | None, values: list[float | None], high_good: bool = True) -> float:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    if value is None or not vals:
        return 50
    less = sum(1 for v in vals if v < value)
    equal = sum(1 for v in vals if v == value)
    rank = (less + 0.5 * equal) / len(vals) * 100
    return rank if high_good else 100 - rank


def keyword_count(text: str, words: list[str]) -> int:
    return sum(text.count(word) for word in words)


def has_any(text: str, words: list[str]) -> bool:
    lower = text.lower()
    return any(word.lower() in lower for word in words)


def valuation_score(company: dict[str, object]) -> float:
    fin = company["fin"]  # type: ignore[assignment]
    ps = fin.get("ps")  # type: ignore[union-attr]
    fpe = fin.get("forward_pe")  # type: ignore[union-attr]
    ev = fin.get("ev_ebitda")  # type: ignore[union-attr]
    score = 50.0
    if ps is None:
        score -= 5
    elif ps < 2:
        score += 16
    elif ps < 4:
        score += 10
    elif ps < 7:
        score += 4
    elif ps < 12:
        score -= 4
    elif ps < 20:
        score -= 12
    else:
        score -= 22

    if fpe is None:
        score -= 3
    elif fpe < 12:
        score += 14
    elif fpe < 18:
        score += 9
    elif fpe < 25:
        score += 4
    elif fpe < 35:
        score -= 3
    elif fpe < 55:
        score -= 10
    else:
        score -= 18

    if ev is not None:
        if 0 < ev < 10:
            score += 5
        elif ev > 35:
            score -= 5
    notes = str(fin.get("notes", "")) + str(fin.get("valuation_check", ""))  # type: ignore[union-attr]
    if "异常" in notes or "warn" in notes or "bad" in notes:
        score -= 3
    return clamp(score)


def iv_safe(company: dict[str, object]) -> float:
    iv = company["fin"].get("call_iv")  # type: ignore[union-attr]
    return 50 if iv is None else clamp(100 - (iv - 20) * 1.05)


def iv_aggressive(company: dict[str, object]) -> float:
    iv = company["fin"].get("call_iv")  # type: ignore[union-attr]
    return 45 if iv is None else clamp((iv - 25) * 1.05)


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def build_companies() -> dict[str, dict[str, object]]:
    index_map = parse_company_index()
    latest = latest_eval_files()
    if TARGET not in latest:
        raise SystemExit("缺少 ALLE 正式评估文件")
    fin = parse_financial()
    mom2 = parse_momentum(MOM2W_PATH, "mom2w")
    mom1 = parse_momentum(MOM1M_PATH, "mom1m")
    soxx = parse_soxx()
    companies: dict[str, dict[str, object]] = {}
    for ticker, info in latest.items():
        extracted = extract_eval(info)
        name = index_map.get(ticker, {}).get("name") or fin.get(ticker, {}).get("name") or str(info["slug"]).replace("_", " ")
        category = fin.get(ticker, {}).get("category") or index_map.get(ticker, {}).get("category") or ""
        companies[ticker] = {
            **info,
            **extracted,
            "name": name,
            "category": category,
            "fin": fin.get(ticker, {}),
            "mom2": mom2.get(ticker, {}),
            "mom1": mom1.get(ticker, {}),
            "soxx": soxx.get(ticker, {}),
        }
    return companies


HIGH_GROWTH_CATS = {"AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器", "AI服务器_存储_EMS", "云算力_IDC_AI软件平台"}
INFRA_CATS = {"机电_冷却_工程_水处理_边缘工业AI", "配电_电源_功率器件", "电力_发电_能源_储能"}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    soxx_vals = [c["soxx"].get("soxx_cum") for c in companies.values()]  # type: ignore[union-attr]
    mom2_vals = [c["mom2"].get("mom2w") for c in companies.values()]  # type: ignore[union-attr]
    mom1_vals = [c["mom1"].get("mom1m") for c in companies.values()]  # type: ignore[union-attr]

    for company in companies.values():
        text = str(company["one"]) + "\n" + str(company["conclusion"]) + "\n" + str(company["calibration"])
        base = company["base_growth"] if company["base_growth"] is not None else 0
        bull = company["bull_growth"] if company["bull_growth"] is not None else base
        extreme = company["extreme_growth"] if company["extreme_growth"] is not None else bull
        conf = conf_score(str(company["base_conf"]))
        extreme_conf = conf_score(str(company["extreme_conf"]))
        val = valuation_score(company)
        safe = iv_safe(company)
        ag_iv = iv_aggressive(company)
        soxxp = pct_rank(company["soxx"].get("soxx_cum"), soxx_vals)  # type: ignore[union-attr]
        mom2p = pct_rank(company["mom2"].get("mom2w"), mom2_vals)  # type: ignore[union-attr]
        mom1p = pct_rank(company["mom1"].get("mom1m"), mom1_vals)  # type: ignore[union-attr]
        category = str(company["category"])

        evidence = keyword_count(text, ["backlog", "RPO", "订单", "指引", "已披露", "收入表", "book-to-bill", "客户", "合同", "认证", "产能"])
        risk_words = keyword_count(text, ["未披露", "缺少", "无法可靠", "低可信", "下移", "不进入基准", "不确定", "风险", "延迟", "瓶颈"])
        cash_words = keyword_count(text, ["FCF", "自由现金流", "现金流", "cash flow", "available cash flow", "现金转化", "资产负债表"])
        catalyst = keyword_count(text, ["Q2", "Q3", "Q4", "未来 1", "未来1", "1-2 个季度", "订单", "backlog", "RPO", "认证", "产能", "产品发布", "收购", "指引", "财报", "客户", "交付", "Investor Conference"])
        direct_ai = has_any(text, ["AI 数据中心", "AI data center", "Blackwell", "Rubin", "GB300", "液冷", "800V", "HBM", "CoWoS", "NeoCloud", "hyperscale", "AI campus", "data center"])
        mature_cash = has_any(text, ["现金流强", "FCF 强", "available cash flow", "高利润", "recurring", "服务", "稳定", "公用事业", "regulated"])
        negative_profit = has_any(text, ["FCF 为负", "自由现金流为负", "净亏损", "亏损", "负毛利", "破产", "going concern"])
        category_bonus = 4 if category in HIGH_GROWTH_CATS else (2 if category in INFRA_CATS else 0)

        ntm = 45 + min(max(base, -10), 80) * 0.45 + conf * 0.80 + min(evidence, 10) * 0.8 - min(risk_words, 12) * 0.30 + (3 if mature_cash else 0)
        right = 34 + min(max(extreme, -10), 150) * 0.42 + min(max(extreme - base, 0), 90) * 0.23 + category_bonus + (6 if direct_ai else 0) + ag_iv * 0.07 - max(-extreme_conf, 0) * 0.2
        riskadj = 30 + min(max(base, -10), 80) * 0.22 + min(max(extreme, -10), 140) * 0.14 + conf * 0.55 + (val - 50) * 0.22 + (safe - 50) * 0.12 + soxxp * 0.08 + min(cash_words, 8) * 0.70 - (8 if negative_profit else 0) - min(risk_words, 10) * 0.18
        downside = 28 + safe * 0.22 + soxxp * 0.28 + val * 0.12 + conf * 0.45 + min(cash_words, 8) * 0.80 + (5 if mature_cash else 0) - (12 if negative_profit else 0)
        digestion = 32 + val * 0.35 + min(max(base, -10), 80) * 0.35 + min(max(extreme, -10), 140) * 0.10 + conf * 0.30
        if company["fin"].get("ps") is not None and company["fin"].get("ps") < 3 and base > 5:  # type: ignore[union-attr,operator]
            digestion += 5
        if company["fin"].get("ps") is not None and company["fin"].get("ps") > 20 and base < 50:  # type: ignore[union-attr,operator]
            digestion -= 8
        near = 34 + min(catalyst, 18) * 0.95 + min(max(base, -10), 80) * 0.20 + conf * 0.30 + (6 if direct_ai else 0) + (3 if category in INFRA_CATS else 0)
        momentum = 22 + mom2p * 0.42 + mom1p * 0.30 + min(max(company["mom2"].get("mom2w") or 0, -20), 70) * 0.18 + ag_iv * 0.04  # type: ignore[union-attr]
        aggressive = 28 + right * 0.45 + momentum * 0.25 + ag_iv * 0.18 + min(catalyst, 15) * 0.55 - (10 if negative_profit and conf < 0 else 0)

        company["scores"] = {
            "NTM兑现优先": clamp(ntm),
            "右尾弹性优先": clamp(right),
            "风险调整收益": clamp(riskadj),
            "下行保护优先": clamp(downside),
            "估值消化优先": clamp(digestion),
            "近端催化优先": clamp(near),
            "价格确认/动量": clamp(momentum),
            "激进短线": clamp(aggressive),
        }

    alle = companies[TARGET]
    adjustments = {
        "NTM兑现优先": -3,
        "右尾弹性优先": -12,
        "风险调整收益": -8,
        "下行保护优先": 2,
        "估值消化优先": -2,
        "近端催化优先": -8,
        "价格确认/动量": -3,
        "激进短线": -10,
    }
    for strategy, adjustment in adjustments.items():
        alle["scores"][strategy] = clamp(alle["scores"][strategy] + adjustment)  # type: ignore[index,operator]

    for strategy in STRATS:
        ordered = sorted(companies.items(), key=lambda item: item[1]["scores"][strategy], reverse=True)  # type: ignore[index]
        total = len(ordered)
        for rank, (ticker, company) in enumerate(ordered, start=1):
            pct = rank / total
            if pct <= 0.07:
                tier = "S"
            elif pct <= 0.25:
                tier = "A"
            elif pct <= 0.55:
                tier = "B"
            elif pct <= 0.85:
                tier = "C"
            else:
                tier = "D"
            company.setdefault("tiers", {})[strategy] = tier  # type: ignore[index]
            company.setdefault("ranks", {})[strategy] = rank  # type: ignore[index]

    for company in companies.values():
        if not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company["tiers"][strategy] = "资料不足"  # type: ignore[index]


def category_short(category: str) -> str:
    return category.replace("_", "/") if category else "未分类"


def short_name(company: dict[str, object]) -> str:
    return f"{company['ticker']} / {company['name']}"


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in {"JCI", "MSI"}:
        return "直接同业"
    if ticker in {"AMZN", "MSFT", "GOOGL", "META", "ORCL", "BABA", "IBM", "EQIX", "DLR", "CRWV", "APLD", "IREN", "NBIS", "NTNX", "CRWD", "ADBE"} or category in {"云算力_IDC_AI软件平台", "AI服务器_存储_EMS"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
        label = strategy.replace("优先", "").replace("/动量", "动量")
        if diff >= 8:
            a_strong.append(label)
        elif diff <= -8:
            b_strong.append(label)
        else:
            close.append(label)

    def joined(items: list[str]) -> str:
        if not items:
            return "无"
        return "、".join(items[:3]) + ("等" if len(items) > 3 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A指引和现金流更可兑现",
            "右尾弹性优先": "B缺可收入化右尾证据",
            "风险调整收益": "A估值低且反证更轻",
            "下行保护优先": "A低IV和压力期更稳",
            "估值消化优先": "A低PE低PS更易消化",
            "近端催化优先": "A收购和非住宅兑现更近",
            "价格确认/动量": "A价格更稳未破坏趋势",
            "激进短线": "B短线反证或缺催化",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入增速和订单锚更强",
            "右尾弹性优先": "B右尾收入弹性更大",
            "风险调整收益": "B上行赔率更好",
            "下行保护优先": "B资产质量或防御性更强",
            "估值消化优先": "B业绩增速更能覆盖估值",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B高弹性叙事更适合进攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"下行保护优先", "估值消化优先"}:
        return "安全性和估值接近"
    return "档位接近需再验证"


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"
    tier_diff = TIER_VAL[at] - TIER_VAL[bt]  # type: ignore[index,operator]
    score_diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
    if score_diff >= 28 or tier_diff >= 3:
        tag = "强烈建议投A"
    elif score_diff >= 13 or tier_diff >= 2:
        tag = "建议投A"
    elif score_diff >= 5:
        tag = "微倾向投A"
    elif score_diff <= -28 or tier_diff <= -3:
        tag = "强烈建议投B"
    elif score_diff <= -13 or tier_diff <= -2:
        tag = "建议投B"
    elif score_diff <= -5:
        tag = "微倾向投B"
    else:
        tag = "中性"
    if rel == "跨赛道":
        if tag == "强烈建议投A" and not (abs(score_diff) >= 38 or abs(tier_diff) >= 4):
            tag = "建议投A"
        elif tag == "强烈建议投B" and not (abs(score_diff) >= 38 or abs(tier_diff) >= 4):
            tag = "建议投B"
        elif tag == "建议投A" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投A"
        elif tag == "建议投B" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投B"
    if rel == "直接同业" and abs(score_diff) >= 18 and tag.startswith("建议"):
        tag = "强烈" + tag
    return tag


def cell_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    tag = label_for(a, b, strategy, rel)
    return f"{tag}：{reason_for(strategy, tag, rel)}"


def direction_counts(cells: list[str]) -> tuple[int, int, int]:
    a_count = b_count = neutral = 0
    for cell in cells:
        tag = tag_in_cell(cell) or ""
        if tag.endswith("投A"):
            a_count += 1
        elif tag.endswith("投B"):
            b_count += 1
        else:
            neutral += 1
    return a_count, b_count, neutral


def final_choice(a: dict[str, object], b: dict[str, object], cells: list[str]) -> str:
    a_count, b_count, _ = direction_counts(cells)
    if a_count > b_count:
        return "A"
    if b_count > a_count:
        return "B"
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
            return "ALLE 的低估值、低波动和现金流底座更适合稳健配置。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "ALLE 业绩可见度不极端，但当前估值消化难度更低。"
        return "ALLE 的兑现路径和风险控制略好，B 的上行证据不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的增长右尾和重定价弹性明显强于 ALLE。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据更强。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和短线资金偏好更强。"
    return f"{b['ticker']} 在多数投资思路下比 ALLE 更符合项目内资金配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output = []
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        a_count, b_count, neutral = direction_counts(cells)
        final = final_choice(a, b, cells)
        output.append(
            {
                "ticker": ticker,
                "b": b,
                "rel": rel,
                "cells": cells,
                "ac": a_count,
                "bc": b_count,
                "nc": neutral,
                "final": final,
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return output


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][tag_in_cell(cell)] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:2]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:2]
    strong_b = sorted(comparisons, key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]), reverse=True)  # type: ignore[index,operator]
    strong_a = sorted(comparisons, key=lambda x: (x["ac"] - x["bc"], a["scores"]["下行保护优先"] - x["b"]["scores"]["下行保护优先"]), reverse=True)  # type: ignore[index,operator]
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:40]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:40]  # type: ignore[operator]
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"]]

    product_names = []
    for product in a["products"][:6]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": ("FY2026 reported growth +6%-+8%，NTM 基准 $4.36B-$4.50B，现金转化 85%-95% 指引", "organic 只有 +2%-+4%，M&A/FX 贡献较多"),
        "右尾弹性优先": ("电子门禁、ELATEC、DCI/Krieger 和 mission-critical opening 有小基数期权", "AI DC 收入/客户/订单/backlog 均未披露，右尾难进入基准"),
        "风险调整收益": ("Forward PE 13.70、P/S 2.71、Call IV 39.1%，经营现金流质量较稳", "项目内许多 AI 主链公司上行空间更大"),
        "下行保护优先": ("低 IV、压力窗口累计 -18.66%，机械/电子门控与服务现金流较稳", "住宅和非住宅施工周期仍会影响订单"),
        "估值消化优先": ("估值倍数低于大多数 AI 主链，NTM 基准收入和 EPS 指引可见", "收入增速不高，若 margin 无法修复则消化速度有限"),
        "近端催化优先": ("Q2-Q4 organic、International 追回、并购整合可验证", "缺少明确大额客户订单或产品代际催化"),
        "价格确认/动量": ("低波动且未出现压力窗口严重破位", "过去两周 +0.67%，过去一月 -3.97%，相对 AI 主链动量弱"),
        "激进短线": ("低 IV 可作为防守仓位，偶发数据中心订单披露可能重定价", "短线爆发力、右尾叙事和资金关注度弱于高 beta AI 标的"),
    }

    out: list[str] = []
    out += [
        "# ALLE 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：ALLE / Allegion plc",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ALLE 在项目内最像低波动、低估值、现金流可见的防守型替代，而不是高右尾 AI 主链标的。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 organic growth 只有 `+2%-+4%` 指引、数据中心 opening package 无订单/backlog 披露、近端动量不强。",
        "- A 最适合的投资者画像：偏稳健、重视估值消化、现金流、低 IV 和压力窗口韧性的配置者；适合作为 AI 基础设施组合里的低 beta 补充。",
        "- A 最不适合的投资者画像：追求非线性收入上修、AI 主链爆发、短线高弹性和价格确认的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常拥有更高 NTM 增速、更直接 AI 数据中心收入化、订单/backlog 或更强动量。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：ALLE 不是项目内增长冠军；它在全项目更偏中后段增长、上游事实强但右尾弱，胜率主要来自下行保护和估值消化。",
        "- 后续最重要跟踪数据：Americas non-res organic、electronic organic、International ERP 追回、ELATEC/DCI/Trimco 整合、data-center/customer/order/backlog 首次披露、ACF 转化率、PPII/margin rate 和住宅需求。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        row(["项目", "内容"]),
        row(["---", "---"]),
        row(["股票代号", "ALLE"]),
        row(["公司名称", "Allegion plc"]),
        row(["产业链分类", a["category"]]),
        row(["重要产品/业务线", "；".join(product_names)]),
        row(["NTM 基准收入", a["base_rev"] or "$4.36B-$4.50B"]),
        row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        row(["最大传导瓶颈", "外部非住宅/数据中心需求能否在 NTM 内转成可确认订单、交付、验收和 backlog；当前没有 data center revenue/order/customer 披露。"]),
        row(["最大反证", "organic 指引仍为 +2%-+4%，2026Q1 margin 下滑，数据中心物理安防只是小基数跨产品子集。"]),
        row(["近端催化剂", "2026Q2-Q4 非住宅与电子 organic、International ERP 追回、ELATEC/DCI 整合、首次数据中心订单或客户披露。"]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        out.append(row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        row(["---", "---", "---", "---"]),
        row(["直接同业", "只在建筑/安防/门禁/楼宇控制需求池高度重叠时使用，优先看收入兑现、margin、订单和客户质量。", "JCI、MSI", "同业证据强时允许建议或强烈建议，估值必须按相近业务质量校准。"]),
        row(["相邻替代", "同属 AI 数据中心物理基础设施或工业基础设施资金篮子，但产品不直接竞争。", "VRT、TT、CARR、DOV、ETN、NVT、FIX、EME", "默认看资金只能买一个时的增长质量、订单可见度和估值消化。"]),
        row(["上下游", "一方是数据中心/云/服务器需求端或资本开支端，另一方是物理设施供应端。", "MSFT、AMZN、GOOGL、EQIX、DLR、DELL、SMCI", "不把下游收入规模等同于 ALLE 机会，重点看利润池和议价权。"]),
        row(["跨赛道", "半导体、设备、材料、软件等与 ALLE 业务差异大但可作为资金配置替代。", "NVDA、ASML、TSM、CDNS、LIN", "默认降低结论力度，只有增长质量、估值消化或风险收益明显拉开时才给建议/强烈建议。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    out.append(row(headers))
    out.append(row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        out.append(
            row(
                [
                    index,
                    short_name(b),  # type: ignore[arg-type]
                    category_short(str(b["category"])),  # type: ignore[index]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(comparison["ac"], comparison["bc"], comparison["nc"]),  # type: ignore[arg-type]
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要 ALLE 披露数据中心/mission-critical 订单、客户、backlog，并把 organic growth 抬到高个位数以上。"
        if comparison["rel"] == "跨赛道":
            need = "需要 ALLE 证明其增长和利润扩张能接近该跨赛道标的，或用更强下行保护抵消右尾差距。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提高收入确认可信度、现金流质量和估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入/利润，并降低估值和波动反证。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 公司 A 日度数据摘录：2026-06-22 收盘价 `130.93`，市值 `$11.25B`，TTM PE `17.89`，Forward PE `13.70`，P/S `2.71`，Call IV `39.1%`，Put IV `34.9%`；2026-06-03 过去两周 `+0.67%`、过去一月 `-3.97%`；2026-06-04 三段 SOXX 压力窗口累计 `-18.66%`。",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "alle_tiers": companies[TARGET]["tiers"],
        "alle_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
