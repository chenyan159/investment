from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_etn_company_comparison as etn_calibrated


TARGET = "JCI"
TARGET_NAME = "Johnson Controls"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "JCI_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {"AAON", "CARR", "DKILY", "MOD", "TT", "VRT"}
BUILDING_SECURITY_ADJACENT = {"ALLE", "MSI", "DOV", "DCI", "PNR", "ECL", "NDSN", "FTV", "PH", "DHR", "TMO"}
POWER_COOLING_ADJACENT = {
    "ABBNY",
    "AEIS",
    "AEP",
    "ATKR",
    "BE",
    "BWXT",
    "CEG",
    "CMI",
    "DTE",
    "EME",
    "ENS",
    "ET",
    "ETN",
    "ETR",
    "FCEL",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "MRAAY",
    "MYRG",
    "NVT",
    "OKLO",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "TTDKY",
    "VST",
}
AI_DOWNSTREAM_OR_CUSTOMERS = {
    "AAOI",
    "ADBE",
    "ALAB",
    "AMD",
    "AMZN",
    "ANET",
    "APH",
    "APLD",
    "ARM",
    "AVGO",
    "BABA",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CRWD",
    "CRWV",
    "CSCO",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "LITE",
    "LWLG",
    "META",
    "MRVL",
    "MSFT",
    "MTSI",
    "MU",
    "NBIS",
    "NOK",
    "NTAP",
    "NTNX",
    "NVDA",
    "ORCL",
    "PENG",
    "POET",
    "PSTG",
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
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "BESIY",
    "CAMT",
    "CDNS",
    "COHU",
    "DSCSY",
    "FORM",
    "GFS",
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "SNPS",
    "TER",
    "TOELY",
    "TSM",
    "TSEM",
    "UCTT",
    "UMC",
    "VECO",
}

ADDITIONAL_SCORE_FLOORS = {
    "AAON": {
        "NTM兑现优先": 66.0,
        "右尾弹性优先": 72.0,
        "风险调整收益": 52.0,
        "下行保护优先": 56.0,
        "估值消化优先": 54.0,
        "近端催化优先": 68.0,
        "价格确认/动量": 80.0,
        "激进短线": 82.0,
    },
    "CARR": {
        "NTM兑现优先": 62.0,
        "右尾弹性优先": 47.0,
        "风险调整收益": 55.0,
        "下行保护优先": 84.0,
        "估值消化优先": 61.0,
        "近端催化优先": 66.0,
        "价格确认/动量": 50.0,
        "激进短线": 74.0,
    },
    "DOV": {
        "NTM兑现优先": 67.0,
        "右尾弹性优先": 58.0,
        "风险调整收益": 70.0,
        "下行保护优先": 80.0,
        "估值消化优先": 66.0,
        "近端催化优先": 63.0,
        "价格确认/动量": 50.0,
        "激进短线": 43.0,
    },
    "DKILY": {
        "NTM兑现优先": 68.0,
        "右尾弹性优先": 60.0,
        "风险调整收益": 60.0,
        "下行保护优先": 68.0,
        "估值消化优先": 58.0,
        "近端催化优先": 65.0,
    },
    "MOD": {
        "NTM兑现优先": 78.0,
        "右尾弹性优先": 80.0,
        "风险调整收益": 58.0,
        "下行保护优先": 58.0,
        "估值消化优先": 68.0,
        "近端催化优先": 80.0,
        "价格确认/动量": 82.0,
        "激进短线": 88.0,
    },
    "TT": {
        "NTM兑现优先": 80.0,
        "右尾弹性优先": 68.0,
        "风险调整收益": 74.0,
        "下行保护优先": 88.0,
        "估值消化优先": 68.0,
        "近端催化优先": 78.0,
        "价格确认/动量": 45.0,
        "激进短线": 64.0,
    },
}

JCI_SCORES = {
    "NTM兑现优先": 76.0,
    "右尾弹性优先": 68.0,
    "风险调整收益": 62.0,
    "下行保护优先": 82.0,
    "估值消化优先": 62.0,
    "近端催化优先": 74.0,
    "价格确认/动量": 58.0,
    "激进短线": 62.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def apply_floors(companies: dict[str, dict[str, object]], floors: dict[str, dict[str, float]]) -> None:
    for ticker, score_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in score_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(current, floor)  # type: ignore[index]


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1].setdefault("scores", {}).get(strategy, 0),  # type: ignore[union-attr]
            reverse=True,
        )
        total = len(ordered)
        for rank, (_ticker, company) in enumerate(ordered, start=1):
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
        if not company.get("fin", {}).get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    if hasattr(calibrated, "fix_growth_ranges"):
        calibrated.fix_growth_ranges(companies)

    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    apply_floors(companies, calibrated.SCORE_FLOORS)
    apply_floors(companies, getattr(etn_calibrated, "LOCAL_SCORE_FLOORS", {}))
    if hasattr(etn_calibrated, "ETN_SCORES") and "ETN" in companies:
        for strategy, score in etn_calibrated.ETN_SCORES.items():
            companies["ETN"].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    apply_floors(companies, ADDITIONAL_SCORE_FLOORS)

    jci = companies[TARGET]
    for strategy, score in JCI_SCORES.items():
        jci.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in BUILDING_SECURITY_ADJACENT or ticker in POWER_COOLING_ADJACENT:
        return "相邻替代"
    if ticker in AI_DOWNSTREAM_OR_CUSTOMERS or ticker in SEMI_CHAIN:
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


def reason_for(strategy: str, tag: str, rel: str, company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    if tag == "中性":
        return "业务差异大且档位接近" if rel == "跨赛道" else "档位接近需继续验证"

    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "JCI订单/backlog/RPO锚更硬",
            "右尾弹性优先": "JCI冷却+CDU+Alloy右尾更完整",
            "风险调整收益": "JCI订单、FCF和估值组合更均衡",
            "下行保护优先": "JCI服务/楼宇底盘和低IV更稳",
            "估值消化优先": "JCI约26x FwdPE可由订单兑现消化",
            "近端催化优先": "JCI Q3/Q4订单和出货验证更近",
            "价格确认/动量": "JCI价格确认温和更稳",
            "激进短线": "JCI冷却叙事仍有事件弹性",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单或收入兑现更硬",
            "右尾弹性优先": f"{ticker}AI冷却纯度或小基数更大",
            "风险调整收益": f"{ticker}增长/估值组合更优",
            "下行保护优先": f"{ticker}现金流或压力期更安全",
            "估值消化优先": f"{ticker}业绩更能覆盖估值",
            "近端催化优先": f"{ticker}订单或产能催化更强",
            "价格确认/动量": f"{ticker}价格趋势和资金偏好更强",
            "激进短线": f"{ticker}高beta更适合短线进攻",
        }[strategy]

    if rel == "相邻替代":
        return {
            "NTM兑现优先": f"{ticker}订单/backlog或兑现更清楚",
            "右尾弹性优先": f"{ticker}右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或防御属性更强",
            "估值消化优先": f"{ticker}增长更能消化估值",
            "近端催化优先": f"{ticker}近端事件催化更强",
            "价格确认/动量": f"{ticker}价格确认更强",
            "激进短线": f"{ticker}主题beta和波动更强",
        }[strategy]

    if rel == "上下游" or str(company.get("category", "")) in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}AI主链兑现证据更硬",
            "右尾弹性优先": f"{ticker}AI收入或小基数右尾更大",
            "风险调整收益": f"{ticker}增长赔率更优",
            "下行保护优先": f"{ticker}现金流或需求能见度更好",
            "估值消化优先": f"{ticker}高增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单/产品催化更密集",
            "价格确认/动量": f"{ticker}价格行为更强",
            "激进短线": f"{ticker}高波动更适合进攻",
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


def label_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        return "中性"

    tier_gap = tier_value(str(at)) - tier_value(str(bt))
    diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
    if diff >= 28 or tier_gap >= 3:
        tag = "强烈建议投A"
    elif diff >= 13 or tier_gap >= 2:
        tag = "建议投A"
    elif diff >= 5:
        tag = "微倾向投A"
    elif diff <= -28 or tier_gap <= -3:
        tag = "强烈建议投B"
    elif diff <= -13 or tier_gap <= -2:
        tag = "建议投B"
    elif diff <= -5:
        tag = "微倾向投B"
    else:
        tag = "中性"

    if rel == "跨赛道":
        if tag == "强烈建议投A" and not (diff >= 38 or tier_gap >= 4):
            tag = "建议投A"
        elif tag == "强烈建议投B" and not (diff <= -38 or tier_gap <= -4):
            tag = "建议投B"
        elif tag == "建议投A" and abs(diff) < 18 and abs(tier_gap) < 2:
            tag = "微倾向投A"
        elif tag == "建议投B" and abs(diff) < 18 and abs(tier_gap) < 2:
            tag = "微倾向投B"

    if rel == "直接同业" and tag.startswith("建议") and abs(diff) >= 18:
        tag = "强烈" + tag
    return tag


def cell_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    tag = label_for(strategy, a, b, rel)
    return f"{tag}：{reason_for(strategy, tag, rel, b)}"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def direction_counts(cells: list[str]) -> tuple[int, int, int]:
    a_count = sum(1 for cell in cells if (tag_in_cell(cell) or "").endswith("投A"))
    b_count = sum(1 for cell in cells if (tag_in_cell(cell) or "").endswith("投B"))
    return a_count, b_count, 8 - a_count - b_count


def final_choice(a: dict[str, object], b: dict[str, object], cells: list[str]) -> str:
    a_count, b_count, _neutral = direction_counts(cells)
    if a_count >= b_count + 2:
        return "A"
    if b_count >= a_count + 2:
        return "B"
    risk_diff = a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"]  # type: ignore[index,operator]
    if abs(risk_diff) >= 4:
        return "A" if risk_diff > 0 else "B"
    digestion_diff = a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"]  # type: ignore[index,operator]
    if abs(digestion_diff) >= 4:
        return "A" if digestion_diff > 0 else "B"
    return "中性"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    ticker = str(b["ticker"])
    if final == "中性":
        return "JCI的订单/服务底盘与对手增长、估值或催化优势未拉开强判差距。"
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "JCI有$20B backlog、$26.3B RPO和FY2026指引支撑NTM兑现。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
            return "JCI的楼宇服务、商业HVAC底盘、低IV和FCF指引提供更好下行保护。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:  # type: ignore[index,operator]
            return "JCI在订单确定性、现金流、估值和AI冷却右尾之间更均衡。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "JCI的Q3/Q4 orders、backlog转收入和高密冷却出货验证更近。"
        return "JCI的AI设施冷却证据和成熟服务现金流质量更适合该口径。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于JCI。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的订单/RPO/backlog或收入确认证据比JCI更硬。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的价格确认和短线资金偏好强于JCI。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的增长或估值组合比JCI更容易消化。"
    return f"{ticker}在多数投资思路下比JCI更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strategy in STRATS:
        diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
        short = strategy.replace("/", "")
        if diff >= 8:
            a_strong.append(short)
        elif diff <= -8:
            b_strong.append(short)
        else:
            close.append(short)
    return f"A强：{'、'.join(a_strong[:3]) or '无'}；B强：{'、'.join(b_strong[:3]) or '无'}；接近：{'、'.join(close[:3]) or '无'}"


def comparison_order(item: dict[str, object]) -> tuple[int, str, str]:
    rel_rank = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    b = item["b"]
    return (rel_rank.get(str(item["rel"]), 9), str(b["category"]), str(b["ticker"]))  # type: ignore[index]


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output: list[dict[str, object]] = []
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(strategy, a, b, rel) for strategy in STRATS]
        ac, bc, nc = direction_counts(cells)
        final = final_choice(a, b, cells)
        output.append(
            {
                "ticker": ticker,
                "b": b,
                "rel": rel,
                "cells": cells,
                "ac": ac,
                "bc": bc,
                "nc": nc,
                "final": final,
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return sorted(output, key=comparison_order)


def fmt_num(value: object, decimals: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return str(value)


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return str(value)


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):+.2f}%"
    except Exception:
        return str(value)


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def top_majority(comparisons: list[dict[str, object]], final: str, limit: int = 40) -> list[dict[str, object]]:
    if final == "B":
        rows = [c for c in comparisons if c["bc"] >= 5 and c["bc"] - c["ac"] >= 3]  # type: ignore[operator]
        return sorted(rows, key=lambda c: (c["bc"] - c["ac"], c["b"]["scores"]["右尾弹性优先"]), reverse=True)[:limit]  # type: ignore[index,operator]
    rows = [c for c in comparisons if c["ac"] >= 5 and c["ac"] - c["bc"] >= 3]  # type: ignore[operator]
    return sorted(rows, key=lambda c: (c["ac"] - c["bc"], c["b"]["scores"]["下行保护优先"]), reverse=True)[:limit]  # type: ignore[index,operator]


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
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b_rows = top_majority(comparisons, "B")
    strong_a_rows = top_majority(comparisons, "A")
    final_a = sum(1 for c in comparisons if c["final"] == "A")
    final_b = sum(1 for c in comparisons if c["final"] == "B")
    final_neutral = sum(1 for c in comparisons if c["final"] == "中性")
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"]]

    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    product_names = [str(product[0]).split("：")[0] for product in a["products"][:8]]  # type: ignore[index]

    support = {
        "NTM兑现优先": (
            "FY2026 Q2 sales $6.142B、organic +6%，orders +30%，backlog $20.0B，RPO $26.3B且67%两年内确认",
            "backlog不等于12个月收入，数据中心项目受site readiness、MEP和验收节奏约束",
        ),
        "右尾弹性优先": (
            "YORK高密chiller、Silent-Aire CDU、OpenBlue/Metasys、Alloy/Accelsius形成chip-to-ambient期权",
            "公司体量大且AI/DC分项未披露，Alloy/Accelsius NTM证据低于纯液冷/光互联/算力公司",
        ),
        "风险调整收益": (
            "约26x Forward PE、P/S 3.70、FCF conversion约100%、服务和楼宇底盘降低单一AI项目风险",
            "估值已明显反映数据中心冷却预期，若项目毛利和现金流滞后，上行会被折价",
        ),
        "下行保护优先": (
            "服务收入占31.6%、低IV、楼宇维护粘性、成熟商业HVAC和消防安防底盘提供防守",
            "SOXX压力窗口累计-32.62%，防守性弱于部分公用事业/净现金软件/低估值工业",
        ),
        "估值消化优先": (
            "基准NTM收入$26.0-26.8B、调整后净利润$3.0-3.2B，若backlog按期转化可消化估值",
            "P/S 3.70和约26x FwdPE不低，估值消化依赖订单转收入和margin同步兑现",
        ),
        "近端催化优先": (
            "FY2026 Q3/Q4 orders、book-to-bill、Americas Products & Systems、YDAM/Silent-Aire出货可连续验证",
            "大型项目可能跨季度确认，缺少客户名单/CDU订单量会压低催化确定性",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+6.69%、过去一月+1.30%，2026-06-22收盘148.21高于6月初",
            "动量不如AI主链、液冷小基数和高beta电力/算力公司，涨幅也可能已部分透支",
        ),
        "激进短线": (
            "33.7% Call IV叠加AI冷却订单、Alloy/Accelsius和reference design事件仍有短线弹性",
            "低IV和大市值使爆发力弱于VRT、MOD、AAON、光互联、NeoCloud和核能开发高beta",
        ),
    }

    out: list[str] = [
        "# JCI 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：JCI / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 JCI vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。JCI 的优势来自订单和 backlog 已经很硬、数据中心冷却进入收入传导、同时仍有商业楼宇服务和消防安防现金流底盘。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是公司体量较大、AI/DC分项收入仍为模型估算、Alloy/Accelsius更多是2027+期权，短线弹性弱于高beta AI主链。",
        "- A 最适合的投资者画像：希望买AI数据中心facility layer，但更重视订单兑现、服务现金流、下行控制和估值可消化性的稳健成长型资金。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大右尾、极强价格动量、短线爆发或纯AI硬件/算力beta的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常有更直接AI主链收入、RPO/backlog、光互联/芯片/存储/电力核心利润池或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：JCI 是项目内中上游的AI冷却稳健兑现型标的，不是全项目右尾冠军；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。",
        "- 后续最重要跟踪数据：FY2026 Q3/Q4 orders、backlog、book-to-bill；Americas Products & Systems和Services增速；APAC Applied HVAC data center延续性；Silent-Aire CDU、YDAM、YK-HT出货和客户案例；Alloy design-in；RPO两年内确认比例；deferred revenue、accounts receivable、inventory、FCF conversion。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "JCI"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$26.0-26.8B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "从订单/backlog到收入确认的现场交付节奏，包括电力接入、客户site readiness、液冷/冷水侧联调、FAT/SAT、MEP工程资源和客户验收。"]),
        base.row(["最大反证", "AI/DC收入仍未单列披露，CDU客户/订单量和Alloy/Accelsius量产证据不足；若大项目压价、扩产成本和营运资本吞噬利润，收入上修不一定留下来。"]),
        base.row(["近端催化剂", "FY2026 Q3/Q4 orders、backlog、Americas Products & Systems转收入、YDAM/Silent-Aire出货、Armada框架转订单、Alloy认证和FCF conversion。"]),
        base.row([
            "日度市场数据",
            f"2026-06-22 收盘价 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。",
        ]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        out.append(base.row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与JCI在HVAC、数据中心冷却、CDU/液冷、楼宇控制、服务或关键设施需求池直接重叠，优先比较订单/backlog、产品代际、客户质量、毛利率和同业估值。", "TT、CARR、VRT、MOD、AAON、DKILY", "同业证据权重最高；若对手在AI冷却纯度、订单或价格确认上明显胜出，可给建议或强烈建议。"]),
        base.row(["相邻替代", "同属AI数据中心物理基础设施、电力、工程、楼宇安全、工业服务或高质量工业资金篮子，但产品不完全竞争。", "ETN、GEV、CEG、NVT、POWL、DOV、ALLE、MSI、EME、FIX", "重点回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好。"]),
        base.row(["上下游", "B位于JCI热管理、楼宇控制、数据中心建设需求链的上游/下游，如芯片、服务器、云厂、光互联、半导体设备和制造链。", "NVDA、AVGO、MSFT、AMZN、DELL、SMCI、TSM、ASML、ANET", "不把下游规模直接等同JCI利润池，核心看议价权、订单硬度、收入确认和利润捕获。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "材料、化学品、软件、航天和部分平台公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    out.append(base.row(headers))
    out.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        out.append(
            base.row(
                [
                    index,
                    base.short_name(b),  # type: ignore[arg-type]
                    base.category_short(str(b["category"])),
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(comparison["ac"], comparison["bc"], comparison["nc"]),  # type: ignore[arg-type]
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要JCI把orders/backlog更快转成收入和margin，并披露数据中心产品收入、CDU客户、Alloy design-in或更高AI/DC收入占比。"
        if comparison["rel"] == "直接同业":
            need = "需要JCI在冷却同业中证明YORK/Silent-Aire订单、交付、利润率和服务attach强于B。"
        elif comparison["rel"] == "上下游":
            need = "需要JCI证明自己能从下游AI系统/云厂CapEx中捕获更高利润，而不只是设施侧跟随。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高收入确认可信度、现金流质量和估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入/利润，并降低估值、现金流或波动反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/JCI_Johnson_Controls_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心风冷、冷水机组与HVAC_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_DCIM、能控与AI工厂数字孪生_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_jci_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对JCI的backlog/RPO、YORK/Silent-Aire/OpenBlue/Alloy证据、估值、IV、价格确认和产品拆分缺失反证做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        out.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{company['path'].name}`"]))  # type: ignore[index,union-attr]

    out.append("")
    return "\n".join(out)


def main() -> None:
    base.TARGET = "ALLE"
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 JCI 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "jci_tiers": {strategy: companies[TARGET]["tiers"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
        "jci_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},  # type: ignore[index]
        "jci_ranks": {strategy: companies[TARGET]["ranks"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
