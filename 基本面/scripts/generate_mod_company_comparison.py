from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_etn_company_comparison as etn_calibrated
import generate_jci_company_comparison as jci_calibrated


TARGET = "MOD"
TARGET_NAME = "Modine Manufacturing"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MOD_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_COOLING_PEERS = {
    "AAON",
    "CARR",
    "DKILY",
    "DOV",
    "JCI",
    "TT",
    "VRT",
}

FACILITY_INFRA_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ALLE",
    "ATKR",
    "BE",
    "BWXT",
    "CAT",
    "CMI",
    "DCI",
    "DD",
    "DHR",
    "ECL",
    "EME",
    "ENS",
    "ETN",
    "FIX",
    "FLNC",
    "FTV",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "IFNNY",
    "LFUS",
    "MIELY",
    "MMM",
    "MRAAY",
    "MSI",
    "MYRG",
    "NDSN",
    "NVT",
    "PH",
    "PNR",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "ST",
    "TDY",
    "TMO",
    "TTDKY",
    "VICR",
    "VSH",
}

UTILITY_AND_POWER_CHAIN = {
    "AEP",
    "CEG",
    "DTE",
    "ET",
    "ETR",
    "VST",
    "OKLO",
    "SMR",
    "FCEL",
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

LOCAL_SCORE_FLOORS = {
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
    "JCI": {
        "NTM兑现优先": 76.0,
        "右尾弹性优先": 68.0,
        "风险调整收益": 62.0,
        "下行保护优先": 82.0,
        "估值消化优先": 62.0,
        "近端催化优先": 74.0,
        "价格确认/动量": 58.0,
        "激进短线": 62.0,
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

MOD_SCORES = {
    "NTM兑现优先": 78.0,
    "右尾弹性优先": 80.0,
    "风险调整收益": 58.0,
    "下行保护优先": 58.0,
    "估值消化优先": 68.0,
    "近端催化优先": 80.0,
    "价格确认/动量": 82.0,
    "激进短线": 88.0,
}


def row(cells: list[object]) -> str:
    return base.row(cells)


def short_name(company: dict[str, object]) -> str:
    return base.short_name(company)


def category_short(category: str) -> str:
    return base.category_short(category)


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def pct_text(value: object, suffix: str = "%") -> str:
    if value is None:
        return "缺失"
    return f"{float(value):.2f}{suffix}"


def num_text(value: object, suffix: str = "") -> str:
    if value is None:
        return "缺失"
    return f"{float(value):.2f}{suffix}"


def money_text(value: object) -> str:
    if value is None:
        return "缺失"
    return f"${float(value):.2f}B"


def apply_floors(companies: dict[str, dict[str, object]], floors: dict[str, dict[str, float]]) -> None:
    for ticker, score_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in score_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(current, floor)  # type: ignore[index]


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for company in companies.values():
        company["tiers"] = {}
        company["ranks"] = {}
        company["rank_total"] = {}

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
            company["tiers"][strategy] = tier  # type: ignore[index]
            company["ranks"][strategy] = rank  # type: ignore[index]
            company["rank_total"][strategy] = total  # type: ignore[index]

    for company in companies.values():
        if not company.get("fin", {}).get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company["tiers"][strategy] = "资料不足"  # type: ignore[index]
                company["ranks"][strategy] = None  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    if hasattr(calibrated, "fix_growth_ranges"):
        calibrated.fix_growth_ranges(companies)

    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    apply_floors(companies, getattr(calibrated, "SCORE_FLOORS", {}))
    apply_floors(companies, getattr(etn_calibrated, "LOCAL_SCORE_FLOORS", {}))
    if hasattr(etn_calibrated, "ETN_SCORES") and "ETN" in companies:
        for strategy, score in etn_calibrated.ETN_SCORES.items():
            companies["ETN"].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    apply_floors(companies, getattr(jci_calibrated, "ADDITIONAL_SCORE_FLOORS", {}))
    apply_floors(companies, LOCAL_SCORE_FLOORS)

    mod = companies[TARGET]
    for strategy, score in MOD_SCORES.items():
        mod.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_COOLING_PEERS:
        return "直接同业"
    if ticker in FACILITY_INFRA_ADJACENT:
        return "相邻替代"
    if ticker in UTILITY_AND_POWER_CHAIN or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_NETWORK_AND_AI_DEMAND_CHAIN or ticker in SEMI_CHAIN:
        return "上下游"
    if category in {"机电_冷却_工程_水处理_边缘工业AI"}:
        return "直接同业"
    if category in {"配电_电源_功率器件", "电力_发电_能源_储能"}:
        return "相邻替代"
    if category in {
        "AI服务器_存储_EMS",
        "AI网络_光互联_连接器",
        "AI计算芯片_EDA_IP_custom_ASIC",
        "云算力_IDC_AI软件平台",
        "晶圆制造_前道设备",
        "封测_检测_计量_光罩",
        "半导体材料_化学品_基板",
    }:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str, company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    if tag == "中性":
        return "业务差异大且档位接近" if rel == "跨赛道" else "档位接近需继续验证"

    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "MOD FY2027指引和Airedale长协更硬",
            "右尾弹性优先": "MOD冷却长协和液冷接口右尾更大",
            "风险调整收益": "MOD增长/估值组合更好",
            "下行保护优先": "MOD有正FCF和客户预付款缓冲",
            "估值消化优先": "MOD增速更能消化当前估值",
            "近端催化优先": "MOD Q1/Q2交付和LTA验证更近",
            "价格确认/动量": "MOD价格确认和资金偏好更强",
            "激进短线": "MOD高IV叠加AI冷却更适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker} 同业订单或收入兑现更硬",
            "右尾弹性优先": f"{ticker} 冷却/热管理右尾更优",
            "风险调整收益": f"{ticker} 增长、估值和现金流组合更优",
            "下行保护优先": f"{ticker} 现金流或压力期更安全",
            "估值消化优先": f"{ticker} 利润和估值消化更轻",
            "近端催化优先": f"{ticker} 订单或产能催化更明确",
            "价格确认/动量": f"{ticker} 价格趋势和资金偏好更强",
            "激进短线": f"{ticker} 高beta或事件弹性更强",
        }[strategy]

    if rel == "相邻替代":
        return {
            "NTM兑现优先": f"{ticker} 订单/backlog或兑现更清楚",
            "右尾弹性优先": f"{ticker} 右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker} 上行和下行组合更优",
            "下行保护优先": f"{ticker} 现金流或防御属性更强",
            "估值消化优先": f"{ticker} 增长质量更能覆盖估值",
            "近端催化优先": f"{ticker} 近端事件催化更强",
            "价格确认/动量": f"{ticker} 价格确认更强",
            "激进短线": f"{ticker} 主题beta和波动更强",
        }[strategy]

    if rel == "上下游" or str(company.get("category", "")) in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker} AI主链兑现证据更硬",
            "右尾弹性优先": f"{ticker} AI收入或小基数右尾更大",
            "风险调整收益": f"{ticker} 风险调整赔率更好",
            "下行保护优先": f"{ticker} 现金流或需求能见度更好",
            "估值消化优先": f"{ticker} 高增速更能覆盖估值",
            "近端催化优先": f"{ticker} 订单/产品催化更密集",
            "价格确认/动量": f"{ticker} 价格行为更强",
            "激进短线": f"{ticker} 高波动更适合进攻",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker} 未来12个月兑现证据更直接",
        "右尾弹性优先": f"{ticker} 极端情景上行更大",
        "风险调整收益": f"{ticker} 风险调整赔率更好",
        "下行保护优先": f"{ticker} 估值或资产质量更安全",
        "估值消化优先": f"{ticker} 当前估值更易消化",
        "近端催化优先": f"{ticker} 未来两个季度催化更明确",
        "价格确认/动量": f"{ticker} 价格行为更强",
        "激进短线": f"{ticker} 短线关注度和波动更强",
    }[strategy]


def label_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

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


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
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


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    ticker = str(b["ticker"])
    if final == "中性":
        return "MOD的冷却长协/动量与对手的增长、估值或防守优势未拉开强判差距。"
    if final == "A":
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "MOD的FY2027交付、Airedale长协和产能爬坡更可能在近端验证。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "MOD有FY2027收入+20%-35%指引、Data Centers高增和40亿美元长协锚定NTM兑现。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "MOD的数据中心冷源、空气侧、CDU/RDHx和服务组合右尾更直接。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
            return "MOD近期价格确认和高IV资金偏好更强。"
        return "MOD在AI冷却收入化、订单可见度和短线关注度上更适合该口径。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的现金流、低波动或压力期表现明显优于MOD。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的估值、现金流和下行组合比MOD更均衡。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于MOD。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的订单/RPO/backlog或收入确认证据比MOD更硬。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}更容易用近端利润兑现消化估值。"
    return f"{ticker}在多数投资思路下比MOD更符合项目内资金配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output: list[dict[str, object]] = []
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(strategy, a, b, rel) for strategy in STRATS]
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


def rank_position(a: dict[str, object], strategy: str, n: int) -> str:
    rank = a["ranks"].get(strategy)  # type: ignore[union-attr]
    if rank is None:
        return f"资料不足，{a['tiers'][strategy]} 档"  # type: ignore[index]
    return f"第 {rank}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]


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
    strong_b = sorted(
        comparisons,
        key=lambda x: (
            x["bc"] - x["ac"],  # type: ignore[operator]
            x["b"]["scores"]["风险调整收益"] - a["scores"]["风险调整收益"],  # type: ignore[index,operator]
            x["b"]["scores"]["下行保护优先"] - a["scores"]["下行保护优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],  # type: ignore[operator]
            a["scores"]["近端催化优先"] - x["b"]["scores"]["近端催化优先"],  # type: ignore[index,operator]
            a["scores"]["激进短线"] - x["b"]["scores"]["激进短线"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3]  # type: ignore[operator]
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker].get("fin")]
    missing_price = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker].get("fin", {}).get("price")  # type: ignore[union-attr]
    ]

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join(
        [f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)]  # type: ignore[union-attr]
    )
    rank_text = {s: rank_position(a, s, n) for s in STRATS}
    final_a = sum(1 for c in comparisons if c["final"] == "A")
    final_b = sum(1 for c in comparisons if c["final"] == "B")
    final_neutral = sum(1 for c in comparisons if c["final"] == "中性")

    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})
    price_line = (
        f"2026-06-22 收盘价 `{num_text(fin.get('price'))}`，市值 `{money_text(fin.get('market_cap_b'))}`，"
        f"TTM PE `{num_text(fin.get('ttm_pe'))}`，Forward PE `{num_text(fin.get('forward_pe'))}`，"
        f"P/S `{num_text(fin.get('ps'))}`，EV/EBITDA `{num_text(fin.get('ev_ebitda'))}`，"
        f"Call IV `{pct_text(fin.get('call_iv'))}`，Put IV `{pct_text(fin.get('put_iv'))}`；"
        f"2026-06-03 过去两周 `{pct_text(mom2.get('mom2w'))}`、过去一月 `{pct_text(mom1.get('mom1m'))}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{pct_text(soxx.get('soxx_cum'))}`。"
    )

    support = {
        "NTM兑现优先": ("FY2027收入+20%-35%指引，Data Centers约35%收入、Q4 +158%，40亿美元LTA和1.65亿美元预付款", "没有标准backlog/book-to-bill披露，LTA三年总额不能全额进入NTM"),
        "右尾弹性优先": ("Airedale冷水机组、热排放、空气侧、CDU/RDHx、模块化/服务共同绑定AI冷却瓶颈", "CDU/RDHx和服务收入未单列，极度乐观依赖多客户认证和产能同步突破"),
        "风险调整收益": ("基准收入38.5-41.5亿美元、EBITDA 6.50-6.80亿美元，P/S 4.91仍低于许多AI高beta", "TTM PE 130.79、Forward PE 26.01、IV 77.6%，利润率和FCF质量仍需恢复"),
        "下行保护优先": ("FY2026 CFO 2.487亿美元、FCF 1.054亿美元，客户预付款改善扩产资金压力", "SOXX压力窗口累计-46.31%、高IV、客户集中和扩产低效限制防守属性"),
        "估值消化优先": ("FY2027高收入增速和EBITDA指引可支撑估值消化，P/S 4.91不算极端", "估值已要求Data Centers继续高增且毛利率修复，若交付或成本拖累会快速反噬"),
        "近端催化优先": ("FY2027 Q1/Q2 Data Centers收入、LTA早期转收入、产能爬坡、Performance分拆和毛利率修复均在近端验证", "若关键组件、FAT/SAT或客户上电窗口推迟，强订单会变成递延反证"),
        "价格确认/动量": ("截至2026-06-03两周+17.37%、一月+13.19%，2026-06-22价格仍处高位", "价格已提前反映大量乐观预期，高IV使回撤风险放大"),
        "激进短线": ("Call IV 77.6%、AI冷却长协、短期财报/交付/扩产验证和强动量适合进攻", "短线容错低，若margin/FCF或交付不达预期会被高估值放大"),
    }

    out: list[str] = [
        "# MOD 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：MOD / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去1个月/过去两周区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 MOD vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MOD 的优势集中在 Airedale 数据中心冷却长协、FY2027 高增指引、近期价格确认和高 IV 带来的短线进攻弹性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是高 TTM PE/高 IV、SOXX 压力期累计回撤较大、Data Centers 扩产毛利率和 FCF 质量还没有完全兑现。",
        "- A 最适合的投资者画像：愿意承担较高波动，核心押注 AI 数据中心冷源/热排放/空气侧/液冷接口订单在 FY2027 转收入，并接受用近端财报验证仓位的成长进攻型资金。",
        "- A 最不适合的投资者画像：优先要求低回撤、低估值、稳定现金流、低 IV 或不希望承担客户集中和产能爬坡风险的防守型配置者。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在现金流安全、下行保护、估值消化或AI主链收入确定性上比MOD更稳或更强。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：MOD 是 {n} 家正式评估公司中偏进攻的AI冷却高弹性标的；本报告最终更值得投 MOD 的对比为 {final_a} 家，更值得投 B 的对比为 {final_b} 家，中性 {final_neutral} 家。它不是全项目最安全公司，但在近端催化、动量和激进短线下处于前列。",
        "- 后续最重要跟踪数据：FY2027 Q1/Q2 Data Centers收入增速、Climate/Data Centers gross margin、adjusted EBITDA margin、LTA早期转收入与客户预付款使用、Airedale产能/关键组件lead time、FAT/SAT和现场验收、CDU/RDHx公开客户、非LTA客户是否被挤出、FCF/库存/应收、Performance Technologies分拆完成时点。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        row(["项目", "内容"]),
        row(["---", "---"]),
        row(["股票代号", "MOD"]),
        row(["公司名称", TARGET_NAME]),
        row(["产业链分类", a["category"]]),
        row(["重要产品/业务线", "；".join(product_names)]),
        row(["NTM 基准收入", a["base_rev"] or "38.5-41.5 亿美元"]),
        row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        row(["最大传导瓶颈", "Airedale 数据中心订单从锁产能、排产、关键零部件、FAT/SAT、现场交付到收入确认的链条；三年LTA不是NTM全额收入。"]),
        row(["最大反证", "FY2026/Q4毛利率下滑、Climate gross margin受扩产低效压制、FCF低于上一年、客户集中和关键组件短缺可能使收入上修不能留下利润。"]),
        row(["近端催化剂", "FY2027 Q1/Q2 Data Centers继续高增、LTA相关扩产按计划推进、毛利率恢复、CDU/RDHx/模块化出现公开订单或客户、Performance分拆更新remaining MOD指引。"]),
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
        "说明：本节档位基于同一批 189 家正式评估公司建立，先用每家公司最新收入传导估值评估抽取 NTM/乐观/极度乐观、利润、现金流、证据和反证，再叠加日度价格、估值、IV、区间涨跌和 SOXX 压力窗口。它不是公司排序结果，也没有读取 `特征量化/`。",
        "",
        "## 4. 可比关系使用说明",
        "",
        row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        row(["---", "---", "---", "---"]),
        row(["直接同业", "数据中心冷却、HVAC、冷水机组、空气侧、CDU/RDHx、热管理或楼宇控制需求池直接重叠，优先看订单/backlog、收入兑现、产品代际、毛利率和同业估值。", "AAON、CARR、JCI、TT、VRT、DKILY、DOV", "同档或相邻档时必须复核订单、收入拆分和利润质量；同业证据强时允许更明确建议。"]),
        row(["相邻替代", "同属AI数据中心物理基础设施、配电、电力、工程或工业基础设施篮子，但产品不直接替代。", "ETN、HUBB、POWL、NVT、EME、FIX、PWR、GEV", "回答资金只能买一个时谁的增长质量、兑现确定性和估值消化更好，不硬比产品细节。"]),
        row(["上下游", "B是云/IDC/服务器/AI芯片/网络/电力等需求链或供应链环节，MOD是设施侧热管理供应商。", "MSFT、AMZN、NVDA、SMCI、ANET、CEG、AEP", "不把下游收入规模直接等同于MOD机会，重点看利润池、议价权、CapEx压力和客户集中度。"]),
        row(["跨赛道", "软件、材料、医疗工业等与MOD业务差异大，但资金配置上仍可替代。", "ADBE、CRWD、LIN、TMO、DHR", "默认降低结论力度；只有增长质量、估值消化或风险收益明显拉开时才给建议/强烈建议。"]),
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
        need = "需要MOD证明FY2027收入高增能同步转成毛利率、EBITDA和FCF修复，并披露更清楚的Data Centers backlog/客户/产品拆分。"
        if comparison["rel"] == "跨赛道":
            need = "需要MOD用更高收入兑现和利润质量抵消该跨赛道标的的现金流、估值或防御优势。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高收入确认可信度、订单/backlog透明度和近端价格确认，或显著改善估值/现金流反证。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要B在保留防守优势的同时，拿出足够右尾和近端催化，否则难压过MOD的AI冷却弹性。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件有金融数据行 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 或价格为缺失的公司为 {('、'.join(missing_price) if missing_price else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{price_line}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/机电_冷却_工程_水处理_边缘工业AI/MOD_Modine_Manufacturing_公司调研_2026-06-11.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心风冷、冷水机组与HVAC_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各公司正式评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "mod_tiers": companies[TARGET]["tiers"],
        "mod_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
