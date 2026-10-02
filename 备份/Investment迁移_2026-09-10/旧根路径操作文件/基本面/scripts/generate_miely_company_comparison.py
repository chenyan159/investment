from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as project_calibration
import generate_etn_company_comparison as etn_calibration
import generate_hubb_company_comparison as hubb_calibration


TARGET = "MIELY"
TARGET_NAME = "三菱电机 Mitsubishi Electric"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MIELY_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_ELECTRICAL_PEERS = {
    "ABBNY",
    "ETN",
    "HUBB",
    "HTHIY",
    "IFNNY",
    "NVT",
    "POWL",
    "POWI",
    "ST",
    "TTDKY",
    "VSH",
}

OPTICAL_AND_DEVICE_PEERS = {
    "AVGO",
    "COHR",
    "LITE",
    "MTSI",
    "SMTC",
    "SMTOY",
    "BELFB",
    "CRDO",
    "AAOI",
    "POET",
    "LWLG",
    "MRAAY",
    "MPWR",
    "NVTS",
    "VICR",
    "WOLF",
    "AOSL",
    "DIOD",
    "LFUS",
}

MEP_COOLING_AND_POWER_ALTS = {
    "AAON",
    "AEIS",
    "ATKR",
    "BE",
    "CARR",
    "CAT",
    "CEG",
    "CMI",
    "DKILY",
    "DOV",
    "EME",
    "ENS",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "PH",
    "PNR",
    "PWR",
    "RYCEY",
    "TT",
    "VRT",
    "VST",
}

UTILITY_AND_POWER_CUSTOMERS = {
    "AEP",
    "DTE",
    "ET",
    "ETR",
}

DATA_CENTER_CUSTOMERS_AND_OPERATORS = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
    "DLR",
    "EQIX",
    "GOOGL",
    "IBM",
    "IREN",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
}

SERVER_AND_NETWORK_DEMAND_CHAIN = {
    "ANET",
    "APH",
    "ARM",
    "BDC",
    "CIEN",
    "CLS",
    "CSCO",
    "DELL",
    "FLEX",
    "FN",
    "HPE",
    "JBL",
    "MRVL",
    "MU",
    "NOK",
    "NTAP",
    "NVDA",
    "PENG",
    "PSTG",
    "RMBS",
    "SANM",
    "SIMO",
    "SITM",
    "SMCI",
    "SNDK",
    "STX",
    "TEL",
    "VIAV",
    "VISN",
    "WDC",
}

SEMICONDUCTOR_EQUIPMENT_AND_MATERIALS = {
    "ACLS",
    "ACMR",
    "AMAT",
    "AMKR",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "AXTI",
    "BESIY",
    "CAMT",
    "CDNS",
    "COHU",
    "DD",
    "DHR",
    "DSCSY",
    "ENTG",
    "FORM",
    "GFS",
    "HOCPY",
    "ICHR",
    "IMOS",
    "INTC",
    "KEYS",
    "KLAC",
    "KLIC",
    "LIN",
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ON",
    "ONTO",
    "PLAB",
    "Q",
    "QCOM",
    "SHECY",
    "SOMMY",
    "STM",
    "TER",
    "TMO",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

MIELY_SCORES = {
    "NTM兑现优先": 72.0,
    "右尾弹性优先": 67.0,
    "风险调整收益": 60.0,
    "下行保护优先": 86.0,
    "估值消化优先": 58.0,
    "近端催化优先": 68.0,
    "价格确认/动量": 58.0,
    "激进短线": 64.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict]) -> None:
    for strategy in STRATS:
        scored = [
            company.get("scores", {}).get(strategy)
            for company in companies.values()
            if company.get("scores", {}).get(strategy) is not None
        ]
        scored.sort(reverse=True)
        total = len(scored)
        if not total:
            continue
        cuts = {
            "S": scored[max(0, int(total * 0.07) - 1)],
            "A": scored[max(0, int(total * 0.25) - 1)],
            "B": scored[max(0, int(total * 0.55) - 1)],
            "C": scored[max(0, int(total * 0.85) - 1)],
        }
        for company in companies.values():
            score = company.get("scores", {}).get(strategy)
            if score is None:
                tier = "资料不足"
                rank = None
            elif score >= cuts["S"]:
                tier = "S"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["A"]:
                tier = "A"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["B"]:
                tier = "B"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["C"]:
                tier = "C"
                rank = sum(1 for value in scored if value > score) + 1
            else:
                tier = "D"
                rank = sum(1 for value in scored if value > score) + 1
            company.setdefault("tiers", {})[strategy] = tier
            company.setdefault("ranks", {})[strategy] = rank
            company.setdefault("rank_total", {})[strategy] = total

    for company in companies.values():
        if not company.get("fin", {}).get("price"):
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"
                company.setdefault("ranks", {})[strategy] = None


def score_companies(companies: dict[str, dict]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    floors: dict[str, dict[str, float]] = {}
    floors.update(getattr(project_calibration, "SCORE_FLOORS", {}))
    floors.update(getattr(etn_calibration, "LOCAL_SCORE_FLOORS", {}))
    floors["ETN"] = getattr(etn_calibration, "ETN_SCORES", {})
    floors["HUBB"] = getattr(hubb_calibration, "HUBB_SCORES", {})

    for ticker, strategy_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in strategy_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)
            company["scores"][strategy] = max(current, floor)

    for strategy, score in MIELY_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_ELECTRICAL_PEERS:
        return "直接同业"
    if ticker in OPTICAL_AND_DEVICE_PEERS or ticker in MEP_COOLING_AND_POWER_ALTS:
        return "相邻替代"
    if ticker in UTILITY_AND_POWER_CUSTOMERS or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_AND_NETWORK_DEMAND_CHAIN:
        return "上下游"
    if ticker in SEMICONDUCTOR_EQUIPMENT_AND_MATERIALS:
        return "跨赛道"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI", "AI网络_光互联_连接器"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "证据互有强弱且档位接近"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "MIELY FY2027指引和多业务兑现更清楚",
            "右尾弹性优先": "MIELY电源/冷却/EML右尾更可收入化",
            "风险调整收益": "MIELY分散底盘和现金流更均衡",
            "下行保护优先": "MIELY现金流、低波动和资产底盘更稳",
            "估值消化优先": "MIELY利润改善更能消化估值",
            "近端催化优先": "MIELY H1数据中心/EML验证更近",
            "价格确认/动量": "MIELY价格趋势和长周期确认更稳",
            "激进短线": "MIELY兼具EML/800VDC事件弹性",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单/backlog兑现更硬",
            "右尾弹性优先": f"{ticker}同业右尾或利润池更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业业绩更能覆盖估值",
            "近端催化优先": f"{ticker}同业订单/产能催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}收入/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker}AI主链或需求端右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS or category == "AI网络_光互联_连接器":
        return {
            "NTM兑现优先": f"{ticker}订单/backlog或交付更清楚",
            "右尾弹性优先": f"{ticker}右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker}增长与估值组合更优",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}订单兑现更能消化估值",
            "近端催化优先": f"{ticker}近端订单或产能催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}AI主链兑现证据更硬",
            "右尾弹性优先": f"{ticker}小基数或AI收入弹性更大",
            "风险调整收益": f"{ticker}增长赔率更能覆盖风险",
            "下行保护优先": f"{ticker}需求能见度或现金流更好",
            "估值消化优先": f"{ticker}高增速更能消化估值",
            "近端催化优先": f"{ticker}产品/订单催化更密集",
            "价格确认/动量": f"{ticker}价格趋势更强",
            "激进短线": f"{ticker}高波动更适合短线进攻",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker}未来12个月兑现证据更直接",
        "右尾弹性优先": f"{ticker}极端情景上行更大",
        "风险调整收益": f"{ticker}风险调整赔率更好",
        "下行保护优先": f"{ticker}估值或资产质量更安全",
        "估值消化优先": f"{ticker}当前估值更易消化",
        "近端催化优先": f"{ticker}未来两个季度催化更明确",
        "价格确认/动量": f"{ticker}价格行为更强",
        "激进短线": f"{ticker}短线关注度和波动更强",
    }[strategy]


def label_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")
    bt = b.get("tiers", {}).get(strategy, "资料不足")
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0)
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 28, 13, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 21, 10, 4

    if diff > 0:
        if tier_gap >= 2 and abs_diff >= strong_cut:
            return "强烈建议投A"
        if tier_gap >= 1 and abs_diff >= suggest_cut:
            return "建议投A"
        if abs_diff >= micro_cut:
            return "微倾向投A"
    else:
        if tier_gap <= -2 and abs_diff >= strong_cut:
            return "强烈建议投B"
        if tier_gap <= -1 and abs_diff >= suggest_cut:
            return "建议投B"
        if abs_diff >= micro_cut:
            return "微倾向投B"
    return "中性"


def cell_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    return f"{label}：{reason_for(strategy, label, b, rel)}"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.20,
        "估值消化优先": 1.15,
        "下行保护优先": 1.05,
        "近端催化优先": 0.85,
        "右尾弹性优先": 0.80,
        "价格确认/动量": 0.45,
        "激进短线": 0.45,
    }
    label_score = {
        "强烈建议投A": 2.0,
        "建议投A": 1.35,
        "微倾向投A": 0.55,
        "中性": 0.0,
        "微倾向投B": -0.55,
        "建议投B": -1.35,
        "强烈建议投B": -2.0,
    }
    score = 0.0
    for strategy in STRATS:
        score += weights[strategy] * label_score.get(tag_in_cell(row_obj[strategy]) or "中性", 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    if choice == "中性":
        return "MIELY的稳健兑现/防守与对手增长、估值或催化优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["下行保护优先"] > 12:
            return "MIELY的多元业务、正FCF、压力窗口韧性和低波动提供更好下行保护。"
        if diffs["NTM兑现优先"] > 10:
            return "MIELY有FY2027收入/利润指引和数据中心电源、IT cooling、EML分项支撑NTM兑现。"
        if diffs["风险调整收益"] > 10:
            return "MIELY在电力、冷却、光器件和工业底盘之间的风险调整组合更均衡。"
        if diffs["估值消化优先"] > 10:
            return "MIELY的FY2027利润改善和多元收入底盘更能支撑估值消化。"
        return "MIELY的经营锚、现金流和多元AI基础设施敞口更适合该口径。"

    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于MIELY。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比MIELY更直接。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和资金偏好明显强于MIELY。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比MIELY更硬。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量和风险调整收益组合优于MIELY。"
    return f"{ticker}在多数投资思路下比MIELY更符合项目内资金配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) > tier_value(b.get("tiers", {}).get(strategy))]
    b_strong = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) < tier_value(b.get("tiers", {}).get(strategy))]
    close = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) == tier_value(b.get("tiers", {}).get(strategy))]
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts) if parts else "档位接近"


def comparison_sort_key(row_obj: dict) -> tuple[int, str, str]:
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return (rel_order.get(row_obj["relationship"], 9), row_obj["classification"], row_obj["ticker"])


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj = {
            "ticker": ticker,
            "name": b["name"],
            "classification": base.category_short(str(b.get("category", ""))),
            "relationship": rel,
            "grade_diff": grade_diff_summary(a, b),
        }
        for strategy in STRATS:
            row_obj[strategy] = cell_for(strategy, a, b, rel)
        ac, bc, nc = direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        row_obj["final_choice"] = final_choice(row_obj)
        row_obj["key_reason"] = key_reason(a, b, row_obj, row_obj["final_choice"])
        rows.append(row_obj)
    return sorted(rows, key=comparison_sort_key)


def fmt_num(value, decimals: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return "缺失"


def fmt_b(value) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return "缺失"


def fmt_pct(value) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):+.2f}%"
    except Exception:
        return "缺失"


def majority_rows(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
    selected = [row for row in rows if row["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda x: (x["bc"] - x["ac"], x["bc"], -x["nc"]), reverse=True)
    else:
        selected.sort(key=lambda x: (x["ac"] - x["bc"], x["ac"], -x["nc"]), reverse=True)
    return selected[:limit]


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin")])
    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})

    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}（ADR/财报币种错配，估值消化不采用该字段），P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}（币种/口径异常，保守处理），Call IV 缺失，Put IV 缺失；"
        f"2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，过去一月 {fmt_pct(m1m.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][tag_in_cell(row_obj[strategy])] += 1

    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]])

    support = {
        "NTM兑现优先": (
            "A",
            "强势档",
            "FY2027公司指引收入6.2万亿日元、调整后经营利润5,900亿日元；数据中心电源、IT cooling、EML分项进入基准",
            "数据中心专属backlog、客户项目、订单金额和交付窗口未披露，总收入增速仍主要是中个位数",
        ),
        "右尾弹性优先": (
            "B",
            "中上档",
            "EML、IT cooling、电源系统、800VDC/SST、Nozomi/OT security提供长期右尾，光器件和冷却小基数较清楚",
            "公司体量大，数据中心FY2026仅约3%收入；FY2031/FY2036目标不能提前计入NTM",
        ),
        "风险调整收益": (
            "B",
            "强势档",
            "Life、Infrastructure、FA、光器件和电源/冷却组合分散，FY2026 FCF为正，FY2027利润改善有官方锚",
            "汽车设备拖累、S&D折旧/价格压力、ADR估值字段异常和数据中心订单缺口限制赔率",
        ),
        "下行保护优先": (
            "A",
            "强势档",
            "大盘工业综合体、正自由现金流、低波动、SOXX压力窗口累计-17.06%，传统HVAC/Infrastructure/FA提供底盘",
            "若日元、汽车设备、项目验收或半导体折旧同时恶化，防守性会下降",
        ),
        "估值消化优先": (
            "B",
            "中上档",
            "FY2027调整后OP由FY2026的5,012亿日元向5,900亿日元改善，利润增长比收入增长更能消化估值",
            "2026-06-22 Forward PE缺失，P/S和EV/EBITDA因ADR/币种错配异常，不能用0.01倍P/S当低估依据",
        ),
        "近端催化优先": (
            "A",
            "强势档",
            "FY2027 H1数据中心分项更新、EML/光器件、IT cooling、Nozomi并表、功率半导体数据服务和IR Day路径可验证",
            "催化偏持续验证，不如AI芯片/内存/光模块订单那样容易快速重定价",
        ),
        "价格确认/动量": (
            "B",
            "中性档",
            "2025-05-27至2026-05-27曾上涨88.11%，2026-06-22价格77.64高于6月初75.41，趋势未坏",
            "2026-06-03过去两周仅+1.51%、过去一月-2.72%，短期动量弱于AI服务器、内存和高beta电力设备",
        ),
        "激进短线": (
            "C",
            "弱势档",
            "EML/1.6T、800VDC、IT cooling、Nozomi和数据中心电源可形成事件交易入口",
            "ADR无干净期权IV，业务分散且数据中心占比小，短线爆发力弱于小盘AI主链和高IV标的",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "数据中心电源系统",
            "IT cooling systems",
            "EML光器件",
            "Monitoring/control/FA/OT security",
            "AI/DC功率半导体",
            "Infrastructure",
            "Life空调/楼宇",
            "Factory Automation",
        ]

    lines: list[str] = [
        "# MIELY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：MIELY / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 MIELY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MIELY 的强项是FY2027收入/利润指引、数据中心电源/IT cooling/EML的真实收入分项、多元工业底盘、正FCF和压力窗口韧性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是数据中心占总收入仍小、专属backlog/客户/订单未披露、Forward PE缺失且ADR估值字段异常、短线beta和资金关注度弱于AI主链。",
        "- A 最适合的投资者画像：想配置AI数据中心电力、冷却、EML光器件和工业控制，但更重视可兑现收入、现金流、下行保护和长期复合，而不是追求最高短线弹性的资金。",
        "- A 最不适合的投资者画像：只追求高增速、小基数、强订单催化、高IV和价格爆发的激进资金；这类资金通常更偏向NVDA/AVGO/MU/ALAB/CRDO/AAOI/VRT/POWL/BE/OKLO/SMR等。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在AI主链右尾、近端订单催化、价格确认或更直接电气/光互联利润池上强于MIELY。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：MIELY 是项目内偏稳健的AI基础设施综合表达，最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它相对多数弱现金流、纯远期和传统慢增长标的更值得配置，但面对ETN/HUBB/VRT/POWL以及AI芯片、内存、云算力、光互联顶级标的时需要按投资思路拆分。",
        "- 后续最重要跟踪数据：FY2027 H1数据中心相关收入和分项；电源系统订单/backlog/交付窗口；IT cooling北美/欧洲客户和液冷平台资格；EML 1.6T/200G lane资格、ASP、产能利用率；Power Device中UPS/BESS/SST/SiC design-in；Nozomi并表收入/ARR和交叉销售；FY2027 capex、库存、FCF和汽车设备重组拖累。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "MIELY"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "配电_电源_功率器件")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "约6.20万亿日元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '6.30-6.40万亿日元'}；极度乐观：{a.get('extreme_rev') or '6.50-6.70万亿日元'}"]),
        base.row(["利润和现金流结论", "基准调整后经营利润约5,900亿日元、净利润约4,750亿日元；FY2026 FCF为正，但电源/冷却/半导体扩产和项目验收会带来营运资本波动。"]),
        base.row(["最大传导瓶颈", "无数据中心专属backlog、客户项目、订单金额、取消率或交付窗口；电源/冷却硬件收入不自动转化为高利润。"]),
        base.row(["最大反证", "数据中心相关FY2026收入1,763亿日元仅约合并收入3.0%；Automotive Equipment下滑、S&D折旧/价格压力和项目验收节奏可能抵消AI增量。"]),
        base.row(["近端催化剂", "FY2027 H1数据中心分项更新、EML/1.6T订单与产能利用率、IT cooling客户突破、电源系统订单、Nozomi并表收入、功率半导体design-in和FCF。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        tier = a.get("tiers", {}).get(strategy, "资料不足")
        position = f"{support[strategy][1]}；评分排名 {a.get('ranks', {}).get(strategy)}/{a.get('rank_total', {}).get(strategy)}"
        lines.append(base.row([strategy, tier, position, support[strategy][2], support[strategy][3]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "同属电气设备、配电、开关设备、UPS/电源系统、功率器件、工业电气渠道或高可靠电力电子供应商；优先比较orders/backlog、收入兑现、margin、客户质量、产品代际和估值。", "ETN、ABBNY、HUBB、NVT、POWL、HTHIY、IFNNY、TTDKY", "判断力度最高；若直接同业在订单、margin、估值或价格确认上显著更强，可压过MIELY的多元底盘和防守优势。"]),
        base.row(["相邻替代", "同属AI园区电力、冷却、光器件、功率器件、发电、储能、工程建设或工业基础设施资金篮子，但产品不完全重叠。", "VRT、TT、DKILY、COHR、LITE、SMTOY、GEV、PWR、EME、FIX、BE、GNRC", "中等力度；赛道更热不能自动胜出，必须落实到订单、backlog、利润率、FCF和估值消化。"]),
        base.row(["上下游", "云厂、IDC、NeoCloud、服务器、网络、芯片和公用事业是MIELY电源/冷却/EML/控制业务的需求链上下游；比较时区分客户收入规模、MIELY可捕获利润和各自capex/估值风险。", "MSFT、AMZN、GOOGL、META、ORCL、EQIX、DLR、CRWV、NVDA、DELL、ANET、AEP、CEG、VST", "不把客户capex直接等同MIELY收入；若对方拥有更直接AI收入、RPO或价格确认，可在右尾、催化和动量列胜出。"]),
        base.row(["跨赛道", "半导体设备、材料、封测、软件和部分工业公司与MIELY业务差异大，但作为组合资金替代仍比较增长质量、风险调整收益、估值消化和催化可见度。", "ASML、AMAT、LRCX、LIN、TMO、ADBE、RKLB", "默认降低结论力度；除非增长质量、估值消化或右尾弹性明显拉开，否则用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    lines.append(base.row(headers))
    lines.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for idx, row_obj in enumerate(comparisons, 1):
        cells = [
            idx,
            f"{row_obj['ticker']} / {row_obj['name']}",
            row_obj["classification"],
            row_obj["relationship"],
            row_obj["grade_diff"],
        ] + [row_obj[strategy] for strategy in STRATS] + [
            row_obj["majority"],
            row_obj["final_choice"],
            row_obj["key_reason"],
        ]
        lines.append(base.row(cells))

    lines += [
        "",
        "## 6. 投资思路统计",
        "",
        base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]),
        base.row(["---"] + ["---:"] * 9),
    ]
    for strategy in STRATS:
        c = stats[strategy]
        lines.append(base.row([strategy] + [c[tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_b, 1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        catchup = "MIELY需要披露更清晰的数据中心电源/IT cooling/EML订单、客户、backlog、交付窗口，并证明利润率和FCF能随收入同步改善。"
        if row_obj["relationship"] == "上下游":
            catchup = "MIELY需要证明云厂/AI主链capex能持续落到其电源、冷却、EML和控制系统收入，而不是只停留在行业TAM。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strategy for strategy in STRATS if "投A" in row_obj[strategy]]
        catchup = "B需要拿出更清晰的NTM收入/利润兑现、订单或客户合同，并证明估值、现金流和压力窗口能承受波动。"
        if "右尾弹性优先" in wins and row_obj["final_choice"] == "A":
            catchup = "B需要把右尾叙事转成可确认收入、利润和现金流，并降低估值或融资反证。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/配电_电源_功率器件/MIELY_三菱电机_Mitsubishi_Electric_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；补充历史区间摘录来自 `金融资料/区间涨跌/公司股价区间涨跌幅_2026-05-27.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 外部行情交叉检查：MarketWatch `https://www.marketwatch.com/investing/stock/miely` 显示 2026-06-23 9:55 a.m. EDT 延时报价约 `$75.11`、较前收 `$77.64` 下跌约 `3.26%`；Investing.com `https://www.investing.com/equities/mitsubishi-electric-corp` 显示 2026-06-23 延时报价约 `$75.61`、前收 `$77.64`。本报告主表仍以项目内最新正式日度文件 `2026-06-22` 建档，6/23 盘中报价仅作价格变动提示，不重算全表。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心开关设备与变压器_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心风冷、冷水机组与HVAC_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_激光器、EML与光器件_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- MIELY 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_miely_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用正式评估最低分校准，对MIELY的FY2027指引、数据中心电源/IT cooling/EML分项、正FCF、压力窗口表现、ADR估值字段异常、短线IV缺失和未披露backlog/RPO限制做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        lines.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{Path(company['path']).name}`"]))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 MIELY 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    a = companies[TARGET]
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "miely_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "miely_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "miely_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
