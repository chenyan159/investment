from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as project_calibration


TARGET = "PNR"
TARGET_NAME = "Pentair plc"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "PNR_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

# base.score_companies was first written for ALLE and applies one final
# ALLE-specific target adjustment.  Call it with ALLE as target, reverse that
# adjustment, then apply PNR-specific calibration.
ALLE_TARGET_ADJUSTMENTS = {
    "NTM兑现优先": -3,
    "右尾弹性优先": -12,
    "风险调整收益": -8,
    "下行保护优先": 2,
    "估值消化优先": -2,
    "近端催化优先": -8,
    "价格确认/动量": -3,
    "激进短线": -10,
}

PNR_SCORES = {
    # PNR has unusually clear FY2026 guidance and segment evidence, but growth
    # is low-to-mid single digit and Pool/Water volume remains a constraint.
    "NTM兑现优先": 61.0,
    # Aurora pump and water treatment are real capabilities, but there are no
    # disclosed data-center customers, orders, backlog or revenue splits.
    "右尾弹性优先": 40.0,
    # Low valuation and cash generation help, while weak growth and pressure
    # window drawdowns prevent a top-tier risk-adjusted grade.
    "风险调整收益": 62.0,
    "下行保护优先": 66.0,
    "估值消化优先": 72.0,
    "近端催化优先": 55.0,
    "价格确认/动量": 31.0,
    "激进短线": 34.0,
}

DIRECT_WATER_FLOW_FILTRATION_PEERS = {
    "DCI",
    "DOV",
    "ECL",
    "PH",
}

COOLING_MEP_ADJACENT = {
    "AAON",
    "CARR",
    "DKILY",
    "JCI",
    "MOD",
    "TT",
    "VRT",
    "FTV",
    "NDSN",
    "DHR",
    "TMO",
    "MMM",
}

WATER_MATERIALS_ADJACENT = {
    "APD",
    "LIN",
    "DD",
    "CC",
    "Q",
    "ASGLY",
    "AJNMY",
    "SHECY",
    "SOMMY",
    "ENTG",
    "HOCPY",
    "MTRN",
    "ROG",
}

INDUSTRIAL_INFRA_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ALLE",
    "ATKR",
    "BE",
    "BWXT",
    "CAT",
    "CMI",
    "EME",
    "ENS",
    "ETN",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "IFNNY",
    "LFUS",
    "MIELY",
    "MRAAY",
    "MSI",
    "MYRG",
    "NVT",
    "OKLO",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "ST",
    "TDY",
    "TTDKY",
    "VICR",
    "VSH",
}

UTILITY_AND_POWER_CUSTOMERS = {"AEP", "CEG", "DTE", "ET", "ETR", "VST"}

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

SERVER_NETWORK_AND_AI_DEMAND_CHAIN = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "APH",
    "ARM",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CSCO",
    "DELL",
    "FLEX",
    "FN",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "MU",
    "NOK",
    "NTAP",
    "NVDA",
    "PENG",
    "POET",
    "PSTG",
    "QCOM",
    "RMBS",
    "SANM",
    "SIMO",
    "SITM",
    "SMCI",
    "SMTC",
    "SNDK",
    "STX",
    "TEL",
    "TSLA",
    "VIAV",
    "VISN",
    "WDC",
}

SEMI_CHAIN = {
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
    "DSCSY",
    "FORM",
    "GFS",
    "HOCPY",
    "ICHR",
    "IMOS",
    "INTC",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MCHP",
    "MICLF",
    "MKSI",
    "MPWR",
    "MRAM",
    "MXL",
    "NVMI",
    "NVTS",
    "ON",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SOMMY",
    "STM",
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "TXN",
    "UCTT",
    "UMC",
    "VECO",
    "WOLF",
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def apply_score_floors(companies: dict[str, dict]) -> None:
    for ticker, floors in getattr(project_calibration, "SCORE_FLOORS", {}).items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)
            company["scores"][strategy] = max(float(current), float(floor))


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
            else:
                if score >= cuts["S"]:
                    tier = "S"
                elif score >= cuts["A"]:
                    tier = "A"
                elif score >= cuts["B"]:
                    tier = "B"
                elif score >= cuts["C"]:
                    tier = "C"
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
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    if "ALLE" in companies:
        for strategy, adjustment in ALLE_TARGET_ADJUSTMENTS.items():
            current = companies["ALLE"].setdefault("scores", {}).get(strategy, 0)
            companies["ALLE"]["scores"][strategy] = base.clamp(float(current) - adjustment)

    apply_score_floors(companies)

    for strategy, score in PNR_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def apply_company_index_metadata(companies: dict[str, dict]) -> None:
    index_map = base.parse_company_index()
    for ticker, meta in index_map.items():
        company = companies.get(ticker)
        if not company:
            continue
        if meta.get("name"):
            company["name"] = meta["name"]
        if meta.get("category"):
            company["category"] = meta["category"]


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_WATER_FLOW_FILTRATION_PEERS:
        return "直接同业"
    if ticker in COOLING_MEP_ADJACENT or ticker in WATER_MATERIALS_ADJACENT or ticker in INDUSTRIAL_INFRA_ADJACENT:
        return "相邻替代"
    if ticker in UTILITY_AND_POWER_CUSTOMERS or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_NETWORK_AND_AI_DEMAND_CHAIN or ticker in SEMI_CHAIN:
        return "上下游"
    if category in {"机电_冷却_工程_水处理_边缘工业AI", "配电_电源_功率器件", "电力_发电_能源_储能"}:
        return "相邻替代"
    if category in {
        "AI服务器_存储_EMS",
        "AI网络_光互联_连接器",
        "AI计算芯片_EDA_IP_custom_ASIC",
        "云算力_IDC_AI软件平台",
        "晶圆制造_前道设备",
        "封测_检测_计量_光罩",
    }:
        return "上下游"
    return "跨赛道"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        return "业务差异大且证据互抵" if rel == "跨赛道" else "档位接近需继续验证"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "PNR指引、分部收入和现金流路径更清楚",
            "右尾弹性优先": "PNR仍有水处理/泵包低估期权",
            "风险调整收益": "PNR低估值和现金流缓冲更均衡",
            "下行保护优先": "PNR高利润率和低IV更防守",
            "估值消化优先": "PNR低PE/P/S更易由业绩消化",
            "近端催化优先": "PNR旺季、Hydra-Stop和Flow验证更近",
            "价格确认/动量": "PNR价格修复胜过弱趋势对手",
            "激进短线": "PNR事件风险低且仍有设施侧题材",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入或订单兑现更硬",
            "右尾弹性优先": f"{ticker}同业AI冷却/过滤右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业增长更能消化估值",
            "近端催化优先": f"{ticker}同业订单或产品催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}订单/backlog或收入兑现更强",
            "右尾弹性优先": f"{ticker} AI设施右尾更直接",
            "风险调整收益": f"{ticker}增长与估值组合更优",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}近端订单/产能催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}波动和主题热度更适合进攻",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}收入/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker} AI主链或需求端右尾更大",
            "风险调整收益": f"{ticker}上行赔率和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}高增速更能消化估值",
            "近端催化优先": f"{ticker}财报、订单或产品催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更高",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker} AI主链兑现证据更硬",
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

    diff = float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 31, 15, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 26, 12, 4
    else:
        strong_cut, suggest_cut, micro_cut = 22, 10, 4

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


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    neutral = len(STRATS) - a_count - b_count
    return a_count, b_count, neutral


def final_choice(a: dict, b: dict, row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.20,
        "风险调整收益": 1.20,
        "估值消化优先": 1.15,
        "下行保护优先": 1.05,
        "近端催化优先": 0.85,
        "右尾弹性优先": 0.75,
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
    if score > 0.05:
        return "A"
    if score < -0.05:
        return "B"
    a_anchor = (
        a.get("scores", {}).get("风险调整收益", 0)
        + a.get("scores", {}).get("NTM兑现优先", 0)
        + a.get("scores", {}).get("估值消化优先", 0)
    )
    b_anchor = (
        b.get("scores", {}).get("风险调整收益", 0)
        + b.get("scores", {}).get("NTM兑现优先", 0)
        + b.get("scores", {}).get("估值消化优先", 0)
    )
    return "A" if a_anchor >= b_anchor else "B"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    diffs = {strategy: float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0)) for strategy in STRATS}
    if choice == "A":
        if diffs["估值消化优先"] > 12:
            return "PNR的Forward PE、P/S和现金流更容易被低个位数增长消化。"
        if diffs["下行保护优先"] > 10:
            return "PNR有Pool高ROS、Water/Flow现金流和低IV，防守质量优于B。"
        if diffs["风险调整收益"] > 8:
            return "PNR增长不高，但估值、利润率和现金流组合更均衡。"
        if diffs["NTM兑现优先"] > 8:
            return "PNR有FY2026指引、分部收入和Hydra-Stop并表锚，NTM路径更清楚。"
        return "PNR在估值消化和经营可见度上略胜，B的右尾或动量不足以覆盖反证。"

    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于PNR。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和短线资金偏好明显强于PNR。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的收入/RPO/order/backlog兑现证据强于PNR。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比PNR更直接。"
    if diffs["风险调整收益"] < -10:
        return f"{ticker}的增长质量和风险调整赔率比PNR更好。"
    if diffs["下行保护优先"] < -10:
        return f"{ticker}的现金流、估值缓冲或资产质量比PNR更防守。"
    return f"{ticker}在多数投资思路下比PNR更符合项目内资金配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [
        strategy
        for strategy in STRATS
        if tier_value(a.get("tiers", {}).get(strategy)) > tier_value(b.get("tiers", {}).get(strategy))
    ]
    b_strong = [
        strategy
        for strategy in STRATS
        if tier_value(a.get("tiers", {}).get(strategy)) < tier_value(b.get("tiers", {}).get(strategy))
    ]
    close = [
        strategy
        for strategy in STRATS
        if tier_value(a.get("tiers", {}).get(strategy)) == tier_value(b.get("tiers", {}).get(strategy))
    ]
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
        row_obj["final_choice"] = final_choice(a, b, row_obj)
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
    missing_price = sorted([ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price")])
    missing_mom = sorted(
        [
            ticker
            for ticker, company in companies.items()
            if not company.get("mom2", {}).get("mom2w") and not company.get("mom1", {}).get("mom1m")
        ]
    )
    missing_soxx = sorted([ticker for ticker, company in companies.items() if not company.get("soxx", {})])

    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})
    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去一月 {fmt_pct(m1m.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
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
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]])

    support = {
        "NTM兑现优先": (
            "中上档",
            "FY2026销售指引同比+2%-+4%，NTM基准收入$4.30B-$4.42B；Q1 2026销售$1.0367B，Pool/Water/Flow三分部收入与ROS证据完整",
            "Pool volume -5.8%、Water volume -4.5%、Flow core仅+2.5%；收入增速不高，更多靠price/productivity和并购补充",
        ),
        "右尾弹性优先": (
            "偏弱档",
            "Aurora数据中心泵包、水处理/过滤、Hydra-Stop和Pool connected ecosystem提供长期可选项",
            "未披露数据中心客户、订单、backlog或收入；PNR不是GPU、CDU、冷板、UQD或主电力设备供应商",
        ),
        "风险调整收益": (
            "强势档",
            "2026-06-22 Forward PE 12.74、P/S 2.85、EV/EBITDA 12.74；基准FCF约$0.75B-$0.90B，高ROS业务提供缓冲",
            "上行主要是低到中个位数增长和利润率执行；若Pool旺季弱或数据中心无订单，重定价弹性有限",
        ),
        "下行保护优先": (
            "中性偏弱档",
            "Pool 30%+ ROS、Water/Flow利润率较高，FY2025 FCF $748.4M，Call IV 32.2%较低",
            "三段SOXX压力窗口累计-42.43%，住宅泳池/Water volume周期性和项目延迟会削弱防御性",
        ),
        "估值消化优先": (
            "强势档",
            "Forward PE 12.74、P/S 2.85、调整后EPS指引$5.30-$5.40，低增长也能较容易消化当前估值",
            "估值消化靠利润率和现金流，不靠收入爆发；若price/productivity失效，低估值优势会收窄",
        ),
        "近端催化优先": (
            "弱势档",
            "Q2/Q3 Pool旺季、Hydra-Stop全年并表、Flow市政/商业项目和FY2026指引兑现可在未来1-2季度验证",
            "公司Q2销售指引仅约+1%；缺少可披露数据中心大单、客户认证或backlog上修节点",
        ),
        "价格确认/动量": (
            "弱势档",
            "2026-06-22价格74.03高于2026-06-03收盘71.45，说明6月初后有修复",
            "截至2026-06-03过去两周-3.69%、过去一月-9.67%，相对AI主链和强设施链动量弱",
        ),
        "激进短线": (
            "弱势档",
            "低IV和数据中心设施侧题材可提供小幅事件弹性，若披露Aurora泵包/水处理客户会重估",
            "短线爆发力、市场关注度和右尾叙事远弱于芯片、光互联、NeoCloud、液冷系统和高beta电力设备",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "Pool设备与connected ecosystem",
            "Water Solutions水处理/过滤",
            "Flow商业/工业/市政泵",
            "Hydra-Stop插入阀/line stop",
            "数据中心Aurora泵包",
            "数据中心水处理/过滤",
        ]

    lines: list[str] = [
        "# PNR 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：PNR / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立8个投资思路全项目相对档位，再逐行做PNR vs 公司B的二选一判断。未读取、引用或继承`特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/`或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。PNR的核心优势是估值消化、现金流和经营可见度：Forward PE 12.74、P/S 2.85、Pool 30%+ ROS、FY2026销售+2%-+4%指引和FCF底盘让它比许多高估值或亏损标的更容易守住基本面。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是右尾弹性、价格确认和激进短线：数据中心泵/水处理只有产品能力证据，没有客户、订单、backlog或收入拆分；截至2026-06-03过去一月跌幅也偏弱。",
        "- A 最适合的投资者画像：重视低估值、高利润率、现金流和防守型工业水处理/泳池设备配置，同时愿意把数据中心设施侧泵包与水处理只当作远期期权的中长期资金。",
        "- A 最不适合的投资者画像：只追求最高AI收入弹性、短线爆发、强价格确认、订单密集上修或小基数非线性增长的进攻型资金。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常有更直接AI收入、更高小基数弹性、更密集近端催化或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：PNR是项目内偏价值/质量/现金流的中游配置，不是高增长核心；综合最终选择为A的对比 {final_a} 家、B的对比 {final_b} 家。它能压过部分估值难消化、现金流弱或资料不足公司，但会系统性输给AI主链、液冷/电力高beta和订单更硬的设施链公司。",
        "- 后续最重要跟踪数据：Q2 2026销售是否超过约+1%指引；Pool旺季sell-through、渠道库存和volume/price拆分；Water Solutions volume能否转正；Flow core growth与backlog；Hydra-Stop收入和ROS；Aurora data center pump或水处理客户/订单/backlog/交期；adjusted ROS、gross margin、FCF conversion、应收库存和回购/杠杆。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "PNR"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "机电_冷却_工程_水处理_边缘工业AI")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "$4.30B-$4.42B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '$4.45B-$4.65B'}；极度乐观：{a.get('extreme_rev') or '$4.70B-$4.95B'}"]),
        base.row(["利润和现金流结论", "基准调整后经营利润约$1.13B-$1.20B、调整后净利润约$0.87B-$0.93B，FCF基准约$0.75B-$0.90B；利润质量高于收入增速。"]),
        base.row(["最大传导瓶颈", "数据中心设施侧需求必须经过MEP/泵包/水处理规格、指定或中标、交付验收和收入确认；当前只有产品页和brochure，不足以进入大额基准。"]),
        base.row(["最大反证", "Pool和Water volume为负，Flow reported增长有收购/FX/价格贡献；数据中心无客户、订单、backlog或收入拆分。"]),
        base.row(["近端催化剂", "Q2-Q3 Pool旺季、Water volume改善、Flow/Hydra-Stop项目转收入、Aurora数据中心泵包或水处理客户/订单首次披露、Q2/Q3 FCF释放。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]

    for strategy in STRATS:
        tier = a.get("tiers", {}).get(strategy, "资料不足")
        position = f"{support[strategy][0]}；评分排名 {a.get('ranks', {}).get(strategy)}/{a.get('rank_total', {}).get(strategy)}"
        lines.append(base.row([strategy, tier, position, support[strategy][1], support[strategy][2]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与PNR在水处理、过滤、工业/市政泵、流体处理、设施侧水管理或相近客户预算上高度重叠，优先比较收入兑现、订单/backlog、margin、现金流、估值和数据中心收入证据。", "ECL、DOV、DCI、PH", "同业证据权重最高；若B有更直接数据中心订单、液冷/过滤收入或更强估值消化，可在对应列压过PNR。"]),
        base.row(["相邻替代", "同属AI园区冷却、MEP、工业基础设施、水/材料/过滤或电力设备资金篮子，但产品不完全竞争。", "VRT、CARR、TT、AAON、MOD、JCI、ETN、NVT、POWL、EME、FIX", "重点回答资金只能买一个时，谁的增长质量、订单可见度、估值消化和近端催化更好。"]),
        base.row(["上下游", "B位于PNR需求链上下游，如云厂、IDC、NeoCloud、服务器、芯片、网络、发电、公用事业和半导体设备材料。", "MSFT、AMZN、GOOGL、META、ORCL、EQIX、DLR、NVDA、DELL、ANET、TSM、ASML", "不把下游capex直接等同PNR收入；若对方拥有更直接AI收入、RPO或价格确认，可在右尾、催化和动量列胜出。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "部分软件、生命科学、材料和非AI工业公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        counter = stats[strategy]
        lines.append(base.row([strategy] + [counter[tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_b, 1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        catchup = "PNR需要把数据中心泵包/水处理从产品能力变成可披露收入、订单、客户和backlog，并证明Pool/Water volume转正。"
        if row_obj["relationship"] == "直接同业":
            catchup = "PNR需要在同业中证明其泵/水处理/过滤订单、margin和估值消化优于B，并拿出数据中心设施侧订单。"
        elif row_obj["relationship"] == "上下游":
            catchup = "PNR需要证明AI主链capex能持续落到Aurora泵包、水处理和Flow/Water订单，而不是只停留在行业TAM。"
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
        catchup = "B需要拿出更清晰的NTM收入/利润兑现、现金流质量、估值消化和压力窗口韧性，或出现明确订单/指引上修。"
        if "右尾弹性优先" in wins and row_obj["final_choice"] == "A":
            catchup = "B需要把右尾叙事转成可确认收入、利润和现金流，并降低估值、融资或执行反证。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/PNR_Pentair plc_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；缺少价格字段的公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        f"- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；缺少两周和一月动量的公司为：{('、'.join(missing_mom) if missing_mom else '无')}。",
        f"- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`；缺少SOXX压力窗口数据的公司为：{('、'.join(missing_soxx) if missing_soxx else '无')}。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_冷却液、水处理、过滤与制冷剂_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心风冷、冷水机组与HVAC_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 外部官方校验来源：Pentair Q1 2026 earnings release / SEC Exhibit 99.1；Pentair Q1 2026 Form 10-Q；Pentair FY2025 Form 10-K；Pentair Aurora data center pump solutions；Pentair Aurora data center pump solutions brochure；Hydra-Stop acquisition announcement；这些链接已在公司A正式评估文件附录列明。",
        f"- PNR 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_pnr_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对PNR的FY2026指引、Pool/Water/Flow分部、Hydra-Stop、数据中心设施侧证据边界、估值、IV、区间涨跌和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
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
        raise SystemExit("缺少 PNR 正式评估文件")
    apply_company_index_metadata(companies)
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
                "pnr_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "pnr_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "pnr_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
