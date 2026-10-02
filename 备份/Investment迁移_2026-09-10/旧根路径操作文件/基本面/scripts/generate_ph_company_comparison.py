from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base


TARGET = "PH"
TARGET_NAME = "Parker-Hannifin"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "PH_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

# base.score_companies was originally written for ALLE and applies a final
# ALLE-specific adjustment.  This script uses the same parser and generic
# scoring engine, then reverses that target adjustment before applying PH
# calibration.
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

PH_SCORES = {
    "NTM兑现优先": 77.2,
    "右尾弹性优先": 58.0,
    "风险调整收益": 56.5,
    "下行保护优先": 91.0,
    "估值消化优先": 59.0,
    "近端催化优先": 62.5,
    "价格确认/动量": 36.0,
    "激进短线": 66.5,
}

SCORE_FLOORS = {
    "AAOI": {"NTM兑现优先": 72.0, "右尾弹性优先": 86.0, "近端催化优先": 76.0, "价格确认/动量": 82.0, "激进短线": 90.0},
    "ALAB": {"NTM兑现优先": 82.0, "右尾弹性优先": 92.0, "风险调整收益": 62.0, "估值消化优先": 68.0, "近端催化优先": 86.0, "价格确认/动量": 86.0, "激进短线": 94.0},
    "AMD": {"NTM兑现优先": 72.0, "右尾弹性优先": 82.0, "风险调整收益": 55.0, "估值消化优先": 58.0, "近端催化优先": 72.0, "价格确认/动量": 60.0, "激进短线": 82.0},
    "AMZN": {"NTM兑现优先": 80.0, "右尾弹性优先": 72.0, "风险调整收益": 68.0, "下行保护优先": 75.0, "估值消化优先": 72.0, "近端催化优先": 70.0, "激进短线": 66.0},
    "ANET": {"NTM兑现优先": 82.0, "右尾弹性优先": 86.0, "风险调整收益": 68.0, "下行保护优先": 72.0, "估值消化优先": 70.0, "近端催化优先": 82.0, "价格确认/动量": 80.0, "激进短线": 88.0},
    "APH": {"NTM兑现优先": 78.0, "右尾弹性优先": 74.0, "风险调整收益": 66.0, "下行保护优先": 78.0, "估值消化优先": 66.0, "近端催化优先": 72.0, "价格确认/动量": 72.0, "激进短线": 76.0},
    "ARM": {"NTM兑现优先": 78.0, "右尾弹性优先": 92.0, "风险调整收益": 58.0, "估值消化优先": 58.0, "近端催化优先": 80.0, "价格确认/动量": 72.0, "激进短线": 90.0},
    "ASML": {"NTM兑现优先": 76.0, "右尾弹性优先": 72.0, "风险调整收益": 64.0, "下行保护优先": 78.0, "估值消化优先": 62.0, "近端催化优先": 70.0, "激进短线": 66.0},
    "AVGO": {"NTM兑现优先": 94.0, "右尾弹性优先": 96.0, "风险调整收益": 74.0, "估值消化优先": 84.0, "近端催化优先": 82.0, "价格确认/动量": 70.0, "激进短线": 94.0},
    "BE": {"NTM兑现优先": 82.0, "右尾弹性优先": 88.0, "风险调整收益": 55.0, "估值消化优先": 64.0, "近端催化优先": 84.0, "价格确认/动量": 82.0, "激进短线": 92.0},
    "CLS": {"NTM兑现优先": 82.0, "右尾弹性优先": 78.0, "风险调整收益": 62.0, "估值消化优先": 72.0, "近端催化优先": 78.0, "价格确认/动量": 78.0, "激进短线": 84.0},
    "COHR": {"NTM兑现优先": 76.0, "右尾弹性优先": 86.0, "风险调整收益": 58.0, "估值消化优先": 62.0, "近端催化优先": 78.0, "价格确认/动量": 82.0, "激进短线": 90.0},
    "CRDO": {"NTM兑现优先": 78.0, "右尾弹性优先": 90.0, "风险调整收益": 58.0, "估值消化优先": 64.0, "近端催化优先": 82.0, "价格确认/动量": 84.0, "激进短线": 92.0},
    "CRWV": {"NTM兑现优先": 90.0, "右尾弹性优先": 96.0, "风险调整收益": 45.0, "估值消化优先": 50.0, "近端催化优先": 92.0, "价格确认/动量": 95.0, "激进短线": 100.0},
    "DELL": {"NTM兑现优先": 78.0, "右尾弹性优先": 76.0, "风险调整收益": 60.0, "估值消化优先": 72.0, "近端催化优先": 78.0, "价格确认/动量": 65.0, "激进短线": 78.0},
    "ETN": {"NTM兑现优先": 78.0, "右尾弹性优先": 70.0, "风险调整收益": 68.0, "下行保护优先": 84.0, "估值消化优先": 66.0, "近端催化优先": 74.0, "价格确认/动量": 62.0, "激进短线": 72.0},
    "FIX": {"NTM兑现优先": 74.0, "右尾弹性优先": 66.0, "风险调整收益": 60.0, "下行保护优先": 65.0, "估值消化优先": 66.0, "近端催化优先": 74.0, "价格确认/动量": 82.0, "激进短线": 84.0},
    "FN": {"NTM兑现优先": 80.0, "右尾弹性优先": 82.0, "风险调整收益": 64.0, "估值消化优先": 72.0, "近端催化优先": 80.0, "价格确认/动量": 84.0, "激进短线": 88.0},
    "GEV": {"NTM兑现优先": 78.0, "右尾弹性优先": 82.0, "风险调整收益": 62.0, "下行保护优先": 68.0, "估值消化优先": 65.0, "近端催化优先": 78.0, "价格确认/动量": 75.0, "激进短线": 86.0},
    "GOOGL": {"NTM兑现优先": 78.0, "右尾弹性优先": 68.0, "风险调整收益": 70.0, "下行保护优先": 82.0, "估值消化优先": 74.0, "近端催化优先": 68.0, "激进短线": 62.0},
    "HUBB": {"NTM兑现优先": 76.0, "右尾弹性优先": 70.0, "风险调整收益": 66.0, "下行保护优先": 82.0, "估值消化优先": 64.0, "近端催化优先": 72.0, "价格确认/动量": 60.0, "激进短线": 70.0},
    "IESC": {"NTM兑现优先": 72.0, "右尾弹性优先": 68.0, "风险调整收益": 58.0, "下行保护优先": 60.0, "估值消化优先": 65.0, "近端催化优先": 72.0, "价格确认/动量": 86.0, "激进短线": 86.0},
    "IREN": {"NTM兑现优先": 78.0, "右尾弹性优先": 90.0, "风险调整收益": 48.0, "估值消化优先": 60.0, "近端催化优先": 82.0, "价格确认/动量": 88.0, "激进短线": 95.0},
    "JBL": {"NTM兑现优先": 78.0, "右尾弹性优先": 72.0, "风险调整收益": 60.0, "估值消化优先": 70.0, "近端催化优先": 76.0, "价格确认/动量": 72.0, "激进短线": 78.0},
    "LITE": {"NTM兑现优先": 72.0, "右尾弹性优先": 84.0, "风险调整收益": 52.0, "估值消化优先": 56.0, "近端催化优先": 76.0, "价格确认/动量": 78.0, "激进短线": 88.0},
    "META": {"NTM兑现优先": 82.0, "右尾弹性优先": 78.0, "风险调整收益": 68.0, "下行保护优先": 70.0, "估值消化优先": 80.0, "近端催化优先": 74.0, "价格确认/动量": 50.0, "激进短线": 75.0},
    "MOD": {"NTM兑现优先": 76.0, "右尾弹性优先": 80.0, "风险调整收益": 56.0, "下行保护优先": 62.0, "估值消化优先": 58.0, "近端催化优先": 78.0, "价格确认/动量": 82.0, "激进短线": 86.0},
    "MRVL": {"NTM兑现优先": 76.0, "右尾弹性优先": 86.0, "风险调整收益": 56.0, "估值消化优先": 60.0, "近端催化优先": 80.0, "价格确认/动量": 70.0, "激进短线": 86.0},
    "MSFT": {"NTM兑现优先": 84.0, "右尾弹性优先": 72.0, "风险调整收益": 74.0, "下行保护优先": 80.0, "估值消化优先": 82.0, "近端催化优先": 74.0, "价格确认/动量": 42.0, "激进短线": 66.0},
    "MU": {"NTM兑现优先": 94.0, "右尾弹性优先": 96.0, "风险调整收益": 70.0, "估值消化优先": 90.0, "近端催化优先": 84.0, "价格确认/动量": 92.0, "激进短线": 96.0},
    "NBIS": {"NTM兑现优先": 86.0, "右尾弹性优先": 95.0, "风险调整收益": 46.0, "估值消化优先": 50.0, "近端催化优先": 90.0, "价格确认/动量": 90.0, "激进短线": 98.0},
    "NVDA": {"NTM兑现优先": 90.0, "右尾弹性优先": 96.0, "风险调整收益": 72.0, "下行保护优先": 65.0, "估值消化优先": 76.0, "近端催化优先": 88.0, "价格确认/动量": 75.0, "激进短线": 92.0},
    "NVT": {"NTM兑现优先": 83.0, "右尾弹性优先": 82.0, "风险调整收益": 60.0, "下行保护优先": 68.0, "估值消化优先": 59.0, "近端催化优先": 80.0, "价格确认/动量": 78.0, "激进短线": 80.0},
    "ORCL": {"NTM兑现优先": 82.0, "右尾弹性优先": 74.0, "风险调整收益": 62.0, "下行保护优先": 68.0, "估值消化优先": 70.0, "近端催化优先": 78.0, "价格确认/动量": 60.0, "激进短线": 78.0},
    "POWL": {"NTM兑现优先": 80.0, "右尾弹性优先": 82.0, "风险调整收益": 58.0, "下行保护优先": 62.0, "估值消化优先": 62.0, "近端催化优先": 80.0, "价格确认/动量": 76.0, "激进短线": 88.0},
    "PWR": {"NTM兑现优先": 78.0, "右尾弹性优先": 70.0, "风险调整收益": 66.0, "下行保护优先": 74.0, "估值消化优先": 68.0, "近端催化优先": 76.0, "价格确认/动量": 70.0, "激进短线": 74.0},
    "SMCI": {"NTM兑现优先": 82.0, "右尾弹性优先": 86.0, "风险调整收益": 52.0, "估值消化优先": 68.0, "近端催化优先": 82.0, "价格确认/动量": 72.0, "激进短线": 90.0},
    "TSM": {"NTM兑现优先": 84.0, "右尾弹性优先": 78.0, "风险调整收益": 70.0, "下行保护优先": 82.0, "估值消化优先": 70.0, "近端催化优先": 74.0, "价格确认/动量": 65.0, "激进短线": 74.0},
    "VRT": {"NTM兑现优先": 84.0, "右尾弹性优先": 88.0, "风险调整收益": 62.0, "下行保护优先": 55.0, "估值消化优先": 58.0, "近端催化优先": 82.0, "价格确认/动量": 72.0, "激进短线": 88.0},
}

DIRECT_FLUID_COOLING_AND_FILTRATION = {
    "AAON",
    "CARR",
    "DCI",
    "DHR",
    "DKILY",
    "DOV",
    "ECL",
    "FTV",
    "JCI",
    "MMM",
    "MOD",
    "NDSN",
    "PNR",
    "TT",
    "VRT",
}

ADJACENT_INDUSTRIAL_INFRA = {
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
    "TMO",
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
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    if "ALLE" in companies:
        for strategy, adjustment in ALLE_TARGET_ADJUSTMENTS.items():
            current = companies["ALLE"].setdefault("scores", {}).get(strategy, 0)
            companies["ALLE"]["scores"][strategy] = base.clamp(current - adjustment)

    for ticker, floors in SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)
            company["scores"][strategy] = max(current, floor)

    for strategy, score in PH_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_FLUID_COOLING_AND_FILTRATION:
        return "直接同业"
    if ticker in ADJACENT_INDUSTRIAL_INFRA:
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
            "NTM兑现优先": "PH航空backlog和订单兑现更硬",
            "右尾弹性优先": "PH液冷/过滤期权更可收入化",
            "风险调整收益": "PH现金流质量和估值风险更均衡",
            "下行保护优先": "PH现金流、航空aftermarket和低IV更稳",
            "估值消化优先": "PH利润兑现更能覆盖估值",
            "近端催化优先": "PH FY2027指引和并购验证更近",
            "价格确认/动量": "PH压力期韧性更好",
            "激进短线": "PH事件确定性高于对手",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单或交付节奏更强",
            "右尾弹性优先": f"{ticker}同业AI冷却/设施右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业业绩更能消化估值",
            "近端催化优先": f"{ticker}同业订单或产品催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker} 订单/backlog或收入兑现更强",
            "右尾弹性优先": f"{ticker} AI设施右尾更直接",
            "风险调整收益": f"{ticker} 增长与估值组合更优",
            "下行保护优先": f"{ticker} 现金流或压力期表现更安全",
            "估值消化优先": f"{ticker} 业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker} 近端订单/产能催化更强",
            "价格确认/动量": f"{ticker} 趋势和资金偏好更强",
            "激进短线": f"{ticker} 波动和主题热度更适合进攻",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker} 收入/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker} AI主链或需求端右尾更大",
            "风险调整收益": f"{ticker} 上行赔率和下行组合更优",
            "下行保护优先": f"{ticker} 现金流或资产质量更防守",
            "估值消化优先": f"{ticker} 高增速更能消化估值",
            "近端催化优先": f"{ticker} 财报、订单或产品催化更近",
            "价格确认/动量": f"{ticker} 价格确认和资金偏好更强",
            "激进短线": f"{ticker} 高beta和AI关注度更高",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker} AI主链兑现证据更硬",
            "右尾弹性优先": f"{ticker} 小基数或AI收入弹性更大",
            "风险调整收益": f"{ticker} 增长赔率更能覆盖风险",
            "下行保护优先": f"{ticker} 需求能见度或现金流更好",
            "估值消化优先": f"{ticker} 高增速更能消化估值",
            "近端催化优先": f"{ticker} 产品/订单催化更密集",
            "价格确认/动量": f"{ticker} 价格趋势更强",
            "激进短线": f"{ticker} 高波动更适合短线进攻",
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
        strong_cut, suggest_cut, micro_cut = 30, 14, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 25, 11, 4
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


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    neutral = len(STRATS) - a_count - b_count
    return a_count, b_count, neutral


def final_choice(a: dict, b: dict, row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.20,
        "风险调整收益": 1.20,
        "估值消化优先": 1.10,
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
    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["下行保护优先"] > 12:
            return "PH的现金流、航空aftermarket、低IV和经营质量更能承受压力窗口。"
        if diffs["NTM兑现优先"] > 10:
            return "PH有FY2026指引、订单+9%、125亿美元backlog和航空12-18个月可见度支撑。"
        if diffs["风险调整收益"] > 8:
            return "PH增长不极端，但收入兑现、现金流和估值压力的组合更均衡。"
        if diffs["估值消化优先"] > 8:
            return "PH的利润率和现金流更容易把当前估值消化掉。"
        return "PH在质量、现金流和NTM兑现上更适合稳健配置。"

    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于PH。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和短线资金偏好明显强于PH。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的收入/RPO/order/backlog兑现证据强于PH。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比PH更直接。"
    if diffs["估值消化优先"] < -10:
        return f"{ticker}的业绩增速或估值组合比PH更容易消化。"
    if diffs["下行保护优先"] < -10:
        return f"{ticker}的现金流、估值缓冲或资产质量比PH更防守。"
    return f"{ticker}在多数投资思路下比PH更符合项目内资金配置目标。"


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
    missing_price = sorted(
        [ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price")]
    )
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
            "强势档",
            "FY2026 Q3销售54.86亿美元、同比+10.6%、有机+6.5%，订单+9%，总backlog约125亿美元；航空backlog 84.13亿美元且转化周期12-18个月",
            "工业backlog约3个月；AI数据中心收入和液冷backlog未披露，NTM增速仍主要是高质量中个位数到低双位数",
        ),
        "右尾弹性优先": (
            "中上档",
            "UQD/UQDB、ORV BMQC、Parflex管路、阀、密封、过滤、TIM/EMI和燃气轮机空气过滤是真实AI数据中心小部件期权",
            "直接AI数据中心收入估计仅`$0.1-0.3B`年化，宽口径`$0.2-0.5B`；PH不是GPU、CDU主机或整柜系统商",
        ),
        "风险调整收益": (
            "强势档",
            "基准stand-alone收入`$22.4-23.6B`、调整分部经营利润60-66亿美元，现金流强且航空/工业组合质量高",
            "2026-06-22 Forward PE 28.23、P/S 5.78、EV/EBITDA 23.60，估值不是便宜资产；Filtration Group会抬升债务",
        ),
        "下行保护优先": (
            "强势档",
            "FY2026前三季度经营现金流26.28亿美元、capex 2.86亿美元；航空aftermarket、分散工业客户和较低IV提供防守底座",
            "SOXX三段压力窗口累计-33.58%，仍有工业周期、材料成本、并购杠杆和高质量工业股估值回撤风险",
        ),
        "估值消化优先": (
            "中上档",
            "FY2026指引和NTM基准利润率26.8%-27.8%支持用EPS/FCF消化估值，Forward PE低于多数高beta AI主链",
            "估值已反映航空强劲、Win Strategy和并购增厚；若工业或AI小部件没有上修，估值消化速度有限",
        ),
        "近端催化优先": (
            "中上档",
            "FY2026 Q4/FY2027初始指引、orders/book-to-bill、航空backlog、Filtration Group交割、首个data center收入披露都可验证",
            "近端催化更多是质量验证而非爆发式订单；缺少已披露hyperscaler液冷大单和产品级backlog",
        ),
        "价格确认/动量": (
            "弱势档",
            "2026-06-22价格高于6月初日度区间价格，说明财报后并未完全失去资金关注",
            "2026-06-03过去两周-1.01%、过去一月-3.57%，价格确认弱于多数AI主链和高beta设施链",
        ),
        "激进短线": (
            "弱势档",
            "Call IV 31.4%、Put IV 28.5%，事件风险可控，若披露液冷客户或并购超预期会有重定价",
            "低波动、低披露、小AI收入占比和千亿美元市值使PH不适合作为极端短线进攻标的",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "Aerospace Systems",
            "Diversified Industrial",
            "AI数据中心液冷连接与流体控制",
            "数据中心coolant filtration/fluid management",
            "燃气轮机空气过滤",
            "Curtis electrification controls",
            "Filtration Group并购补充",
        ]

    lines: list[str] = [
        "# PH 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：PH / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 PH vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。PH 的核心优势不是最高AI beta，而是FY2026指引、订单+9%、125亿美元backlog、航空12-18个月可见度、强现金流和高质量工业/航空组合。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是AI数据中心直接收入和液冷backlog未披露，PH只供应关键小部件而非GPU/CDU/整柜系统，且近期价格动量弱于AI主链和高beta设施链。",
        "- A 最适合的投资者画像：希望用一只质量工业/航空复合股参与部分AI液冷、过滤和电力可靠性期权，同时重视现金流、利润率、订单和下行韧性的中长期配置者。",
        "- A 最不适合的投资者画像：只追求最高增长、最大右尾、强动量和短线爆发的资金；这类资金更容易选择AI芯片、内存、光互联、NeoCloud、VRT/MOD/NVT/POWL等高beta链条。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常有更直接AI收入、更高小基数弹性、更密集近端催化或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：PH 是项目内高质量、低右尾、中高兑现的工业/航空复合标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家。它能压过多数低质量、低现金流或估值难消化公司，但在右尾弹性、动量和激进短线列明显输给AI主链与高beta设施链。",
        "- 后续最重要跟踪数据：FY2026 Q4/FY2027初始指引；orders、book-to-bill和backlog；Aerospace commercial OEM/aftermarket增长；工业backlog是否超过3个月；公司是否首次量化data center/liquid cooling/thermal management revenue；UQD/BMQC/Parflex客户认证；Texas燃气过滤项目是否复制；Filtration Group交割、融资成本、协同和净杠杆路径。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "PH"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "机电_冷却_工程_水处理_边缘工业AI")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "stand-alone $22.4-23.6B；Filtration Group若在NTM内交割另作报表补充"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or 'stand-alone $24.0-25.8B'}；极度乐观：{a.get('extreme_rev') or 'reported $26.0-29.0B'}"]),
        base.row(["利润和现金流结论", "基准调整分部经营利润约60-66亿美元、调整分部经营利润率26.8%-27.8%；FY2026前三季度经营现金流26.28亿美元、capex 2.86亿美元，但Filtration Group 92.5亿美元现金收购会提高债务和利息成本。"]),
        base.row(["最大传导瓶颈", "PH不是GPU、CDU主机或整柜系统商；AI数据中心需求必须经过客户AVL、OCP/UQD/ORV标准、CDU/冷板/rack manifold设计导入、交付、验收和收入确认。"]),
        base.row(["最大反证", "公司未披露data center/liquid cooling revenue或backlog；AI液冷直接收入估计仍只是数亿美元级小部件，不能把行业液冷TAM直接映射到PH收入。"]),
        base.row(["近端催化剂", "FY2026 Q4/FY2027指引、orders与book-to-bill、航空backlog、首次data center/liquid cooling收入披露、Texas燃气过滤项目复制、Filtration Group交割和协同路径。"]),
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
        base.row(["直接同业", "与PH在液冷流体连接、过滤、HVAC/冷却、工业流体控制、工程材料或高可靠工业部件需求池重叠；优先比较订单、backlog、产品认证、客户质量、利润率和同业估值。", "DOV、DCI、PNR、ECL、DHR、CARR、JCI、MOD、TT、VRT、AAON", "判断力度最高；若对手有更直接AI液冷系统收入、订单或价格确认，可在右尾、催化和动量列压过PH。"]),
        base.row(["相邻替代", "同属AI园区电力/冷却/MEP/工业基础设施/航空与高质量工业资金篮子，但产品不完全重叠。", "ETN、HUBB、NVT、POWL、GEV、CAT、CMI、PWR、EME、FIX、IESC", "重点回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好。"]),
        base.row(["上下游", "B位于PH需求链上下游，如云厂、IDC、NeoCloud、服务器、芯片、网络、发电、公用事业和半导体设备材料。", "MSFT、AMZN、GOOGL、META、ORCL、EQIX、DLR、NVDA、DELL、ANET、TSM、ASML", "不把下游capex直接等同PH收入；若对方拥有更直接AI收入、RPO或价格确认，可在右尾、催化和动量列胜出。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "部分材料、软件、生命科学、航天和非AI工业公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        catchup = "PH需要把液冷/过滤/燃气过滤从产品期权变成可披露收入、订单、客户和backlog，并证明估值没有透支。"
        if row_obj["relationship"] == "直接同业":
            catchup = "PH需要在同业中证明其液冷接头、管路、过滤和工业订单质量强于B，且AI小部件不是低毛利标准件。"
        elif row_obj["relationship"] == "上下游":
            catchup = "PH需要证明AI主链capex能持续落到其fluid path、过滤和燃气发电过滤产品，而不是只停留在行业TAM。"
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
        "- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/PH_Parker-Hannifin_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；缺少价格字段的公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        f"- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；缺少两周和一月动量的公司为：{('、'.join(missing_mom) if missing_mom else '无')}。",
        f"- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`；缺少SOXX压力窗口数据的公司为：{('、'.join(missing_soxx) if missing_soxx else '无')}。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_冷却液、水处理、过滤与制冷剂_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心风冷、冷水机组与HVAC_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 外部官方校验来源：Parker FY2026 Q3 results press release `https://investors.parker.com/news-events/press-releases/detail/506/parker-reports-fiscal-2026-third-quarter-results`；Parker FY2026 Q3 10-Q `https://investors.parker.com/sec-filings/all-sec-filings/content/0000076334-26-000073/ph-20260331.htm`；Parker Filtration Group acquisition release `https://investors.parker.com/news-events/press-releases/detail/496/parker-to-acquire-filtration-group-corporation`；Parker data center cooling product page `https://www.parker.com/us/en/additional-information/data-center-cooling.html`；OCP Parker UQDB page `https://www.opencompute.org/ai-marketplace/products/662/parker-universal-quick-disconnect-blindmate-couplings-for-liquid-cooling`。",
        f"- PH 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_ph_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对PH的FY2026 Q3销售、订单、backlog、Aerospace可见度、AI液冷/过滤小部件期权、Filtration Group债务与协同、估值、IV、区间涨跌和SOXX压力窗口做目标公司校准；同时对正式评估中明显处于AI主链、云平台、电力冷却设施链的核心标的设置保守最低分校准，防止通用文本解析低估强对手；未读取下游量化目录、现成排序结论或既有公司对比成品。",
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
        raise SystemExit("缺少 PH 正式评估文件")
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
                "ph_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "ph_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "ph_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
