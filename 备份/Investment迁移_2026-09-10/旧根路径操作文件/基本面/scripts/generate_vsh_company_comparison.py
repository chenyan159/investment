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
import generate_ifnny_company_comparison as ifnny_calibration
import generate_mraay_company_comparison as mraay_calibration
import generate_ttdky_company_comparison as ttdky_calibration


TARGET = "VSH"
TARGET_NAME = "Vishay Intertechnology"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "VSH_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"
base.MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
base.MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
base.SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"


DIRECT_COMPONENT_PEERS = {
    "ADI",
    "AOSL",
    "BELFB",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MCHP",
    "MIELY",
    "MPWR",
    "MRAAY",
    "NVTS",
    "ON",
    "POWI",
    "ST",
    "STM",
    "TTDKY",
    "TXN",
    "VICR",
    "WOLF",
}

AI_POWER_AND_ELECTRICAL_ALTS = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "ETN",
    "GEV",
    "HUBB",
    "NVT",
    "POWL",
    "VRT",
}

BOARD_POWER_CONNECTIVITY_ALTS = {
    "ALAB",
    "APH",
    "BDC",
    "CRDO",
    "GLW",
    "MTSI",
    "RMBS",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
}

DOWNSTREAM_AI_AND_CLOUD = {
    "AAOI",
    "AMD",
    "AMZN",
    "ANET",
    "APLD",
    "ARM",
    "AVGO",
    "BABA",
    "CIEN",
    "CLS",
    "COHR",
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
    "QCOM",
    "SANM",
    "SIMO",
    "SMCI",
    "SNDK",
    "STX",
    "WDC",
}

POWER_AND_INFRA_CUSTOMERS = {
    "AEP",
    "BE",
    "BWXT",
    "CARR",
    "CAT",
    "CEG",
    "CMI",
    "DTE",
    "EME",
    "ENS",
    "ENPH",
    "ET",
    "ETR",
    "FCEL",
    "FIX",
    "FLNC",
    "GNRC",
    "HTHIY",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "OKLO",
    "PWR",
    "RYCEY",
    "SMR",
    "TT",
    "VST",
}

SEMI_EQUIPMENT_AND_MATERIALS = {
    "ACLS",
    "ACMR",
    "AEHR",
    "AJNMY",
    "AMAT",
    "AMKR",
    "APD",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "AXTI",
    "BESIY",
    "CAMT",
    "CC",
    "CDNS",
    "COHU",
    "DD",
    "DHR",
    "DKILY",
    "DSCSY",
    "ECL",
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
    "MMM",
    "MTRN",
    "NDSN",
    "NVMI",
    "ONTO",
    "PH",
    "PLAB",
    "PNR",
    "Q",
    "ROG",
    "SHECY",
    "SOMMY",
    "TDY",
    "TER",
    "TMO",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

# Formal VSH evaluation anchor:
# Q1 2026 revenue +17.3% YoY, Q2 guide $875-$905M, backlog $1.592B,
# B2B 1.34, base NTM revenue +16%-22%, but MOSFET OPM only 0.8%,
# 2026 capex $400-$440M and FCF still tight. AI/DC exposure is real but
# mostly components and indirect power-chain sockets, not disclosed customer
# revenue.
VSH_SCORES = {
    "NTM兑现优先": 67.0,
    "右尾弹性优先": 61.0,
    "风险调整收益": 43.0,
    "下行保护优先": 48.0,
    "估值消化优先": 58.0,
    "近端催化优先": 68.0,
    "价格确认/动量": 70.0,
    "激进短线": 84.0,
}

DIOD_SCORES = {
    "NTM兑现优先": 74.0,
    "右尾弹性优先": 80.0,
    "风险调整收益": 56.0,
    "下行保护优先": 64.0,
    "估值消化优先": 70.0,
    "近端催化优先": 68.0,
    "价格确认/动量": 74.0,
    "激进短线": 86.0,
}


def apply_daily_path_overrides() -> None:
    base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"
    base.MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
    base.MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
    base.SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1].get("scores", {}).get(strategy, -999),  # type: ignore[union-attr]
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
            company.setdefault("rank_total", {})[strategy] = total  # type: ignore[index]

    for company in companies.values():
        if not company.get("fin", {}).get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"  # type: ignore[index]
                company.setdefault("ranks", {})[strategy] = None  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    apply_daily_path_overrides()
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    floors: dict[str, dict[str, float]] = {}
    floors.update(getattr(project_calibration, "SCORE_FLOORS", {}))
    floors.update(getattr(etn_calibration, "LOCAL_SCORE_FLOORS", {}))
    floors["ETN"] = getattr(etn_calibration, "ETN_SCORES", {})
    floors["HUBB"] = getattr(hubb_calibration, "HUBB_SCORES", {})
    floors["MRAAY"] = getattr(mraay_calibration, "MRAAY_SCORES", {})
    floors["TTDKY"] = getattr(ttdky_calibration, "TTDKY_SCORES", {})
    floors["IFNNY"] = getattr(ifnny_calibration, "IFNNY_SCORES", {})
    floors["DIOD"] = DIOD_SCORES

    for ticker, strategy_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in strategy_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[union-attr]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    for strategy, score in VSH_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_COMPONENT_PEERS:
        return "直接同业"
    if ticker in AI_POWER_AND_ELECTRICAL_ALTS or ticker in BOARD_POWER_CONNECTIVITY_ALTS:
        return "相邻替代"
    if ticker in DOWNSTREAM_AI_AND_CLOUD or ticker in POWER_AND_INFRA_CUSTOMERS:
        return "上下游"
    if ticker in SEMI_EQUIPMENT_AND_MATERIALS:
        return "跨赛道"
    if category in {"配电_电源_功率器件", "AI网络_光互联_连接器", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台", "电力_发电_能源_储能"}:
        return "上下游"
    return "跨赛道"


def label_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
    bt = b.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))  # type: ignore[union-attr]
    tier_gap = tier_value(str(at)) - tier_value(str(bt))
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 29, 14, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 25, 11, 4
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


def reason_for(strategy: str, label: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    if label == "中性":
        if rel == "跨赛道":
            return "业务差异大且证据接近"
        return "档位接近且证据互有强弱"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "A有Q1 backlog/B2B和Q2指引",
            "右尾弹性优先": "A的AI电源和800V器件期权更直接",
            "风险调整收益": "A低P/S和恢复弹性抵部分风险",
            "下行保护优先": "A多元被动件和分立器件底盘更稳",
            "估值消化优先": "A低P/S配合收入恢复更易消化",
            "近端催化优先": "A Q2/Q3订单转收入验证更近",
            "价格确认/动量": "A一月涨幅已确认恢复交易",
            "激进短线": "A高IV叠加AI电源短线弹性",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单或收入锚更硬",
            "右尾弹性优先": f"{ticker}同业AI电源/元件右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或波动更安全",
            "估值消化优先": f"{ticker}同业估值更易被业绩消化",
            "近端催化优先": f"{ticker}同业产品/客户催化更明确",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}订单/RPO或收入兑现更短链",
            "右尾弹性优先": f"{ticker}AI主链或需求端右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS or category in HIGH_GROWTH_CATS:
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


def cell_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    return f"{label}：{reason_for(strategy, label, b, rel)}"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


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
    weights = {
        "NTM兑现优先": 1.15,
        "右尾弹性优先": 0.95,
        "风险调整收益": 1.15,
        "下行保护优先": 0.85,
        "估值消化优先": 1.05,
        "近端催化优先": 0.90,
        "价格确认/动量": 0.50,
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
    for strategy, cell in zip(STRATS, cells):
        score += weights[strategy] * label_score.get(tag_in_cell(cell) or "中性", 0.0)
    if score > 0.05:
        return "A"
    if score < -0.05:
        return "B"
    a_quality = (
        float(a["scores"]["NTM兑现优先"])  # type: ignore[index]
        + float(a["scores"]["风险调整收益"])  # type: ignore[index]
        + float(a["scores"]["估值消化优先"])  # type: ignore[index]
    )
    b_quality = (
        float(b["scores"]["NTM兑现优先"])  # type: ignore[index]
        + float(b["scores"]["风险调整收益"])  # type: ignore[index]
        + float(b["scores"]["估值消化优先"])  # type: ignore[index]
    )
    return "A" if a_quality >= b_quality else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    diffs = {
        strategy: float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
        for strategy in STRATS
    }
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    if final == "A":
        if diffs["NTM兑现优先"] > 8:
            return "VSH有Q1 backlog、book-to-bill和Q2指引，NTM收入恢复比对手更清楚。"
        if diffs["估值消化优先"] > 8:
            return "VSH的P/S低且收入恢复可见，估值消化压力小于对手。"
        if diffs["近端催化优先"] > 8:
            return "VSH未来两个季度有订单转收入、毛利率和MOSFET修复验证。"
        if diffs["价格确认/动量"] > 10:
            return "VSH一月涨幅和高IV显示市场已开始交易恢复和AI电源期权。"
        return "VSH在收入恢复、低P/S和AI电源可选性之间略优，对手证据不足以压过。"

    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比VSH更硬。"
    if diffs["右尾弹性优先"] < -14 and category in HIGH_GROWTH_CATS:
        return f"{ticker}的AI主链、小基数或核心利润池右尾明显强于VSH。"
    if diffs["右尾弹性优先"] < -14:
        return f"{ticker}的产品/订单右尾比VSH的间接AI电源期权更强。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长、估值和下行组合优于VSH。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、资产质量或压力期表现明显优于VSH。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}更容易用NTM业绩消化估值，VSH仍受利润率和FCF约束。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker}价格确认和资金偏好强于VSH。"
    return f"{ticker}在多数投资思路下比VSH更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        av = tier_value(a.get("tiers", {}).get(strategy))  # type: ignore[union-attr]
        bv = tier_value(b.get("tiers", {}).get(strategy))  # type: ignore[union-attr]
        label = strategy.replace("优先", "").replace("/动量", "动量")
        if av > bv:
            a_strong.append(label)
        elif av < bv:
            b_strong.append(label)
        else:
            close.append(label)

    def joined(items: list[str]) -> str:
        if not items:
            return "无"
        return "、".join(items[:3]) + ("等" if len(items) > 3 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


def comparison_sort_key(row_obj: dict[str, object]) -> tuple[int, str, str]:
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    b = row_obj["b"]
    return (rel_order.get(str(row_obj["rel"]), 9), str(b["category"]), str(row_obj["ticker"]))  # type: ignore[index]


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    rows: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(strategy, a, b, rel) for strategy in STRATS]
        ac, bc, nc = direction_counts(cells)
        rows.append(
            {
                "ticker": ticker,
                "b": b,
                "rel": rel,
                "cells": cells,
                "ac": ac,
                "bc": bc,
                "nc": nc,
                "final": final_choice(a, b, cells),
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final_choice(a, b, cells)),
            }
        )
    return sorted(rows, key=comparison_sort_key)


def fmt_num(value: object, decimals: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return "缺失"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return "缺失"


def fmt_pct(value: object, signed: bool = True) -> str:
    if value is None:
        return "缺失"
    try:
        sign = "+" if signed else ""
        return f"{float(value):{sign}.2f}%"
    except Exception:
        return "缺失"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def top_majority(comparisons: list[dict[str, object]], final: str, limit: int = 45) -> list[dict[str, object]]:
    selected = [row_obj for row_obj in comparisons if row_obj["final"] == final]
    if final == "B":
        selected.sort(key=lambda row_obj: (row_obj["bc"] - row_obj["ac"], row_obj["bc"], -row_obj["nc"]), reverse=True)  # type: ignore[operator]
    else:
        selected.sort(key=lambda row_obj: (row_obj["ac"] - row_obj["bc"], row_obj["ac"], -row_obj["nc"]), reverse=True)  # type: ignore[operator]
    return selected[:limit]


def daily_snapshot_text(a: dict[str, object]) -> str:
    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})
    return (
        f"2026-06-23 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'), signed=False)}，Put IV {fmt_pct(fin.get('put_iv'), signed=False)}；"
        f"过去两周 {fmt_pct(mom2.get('mom2w'))}，过去1个月 {fmt_pct(mom1.get('mom1m'))}；"
        f"三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = sorted(str(company["date"]) for company in companies.values())
    date_range = f"{company_dates[0]} 至 {company_dates[-1]}"
    missing_fin = sorted(ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price"))  # type: ignore[union-attr]

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][tag_in_cell(cell)] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy])[:3]
    strong_b = top_majority(comparisons, "B")
    strong_a = top_majority(comparisons, "A")
    final_a = sum(1 for comparison in comparisons if comparison["final"] == "A")
    final_b = sum(1 for comparison in comparisons if comparison["final"] == "B")

    product_names = [str(product[0]).split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]  # type: ignore[index]
    if not product_names:
        product_names = [
            "MOSFET / MaxSiC",
            "Diodes / TVS / protection",
            "Resistors / current sense",
            "Inductors / magnetics",
            "Capacitors / MLCC / DC-link",
            "Optoelectronics / isolation",
        ]

    support = {
        "NTM兑现优先": (
            "第 {rank}/{total}，{tier} 档",
            "2026Q1收入8.392亿美元、同比+17.3%，Q2指引8.75-9.05亿美元，backlog 15.923亿美元、B2B 1.34，基准NTM收入35.5-37.5亿美元",
            "订单中有分销补库成分，能否转成OEM/EMS可确认出货仍需Q2-Q3验证",
        ),
        "右尾弹性优先": (
            "第 {rank}/{total}，{tier} 档",
            "乐观收入38.5-41.0亿美元、极度乐观42.0-45.5亿美元；AI PSU、48V/54V、UPS/BBU、800VDC、MaxSiC和高端电容/电感/current sense提供右尾",
            "VSH不是AI控制器、GPU/HBM、PSU系统商或高端MLCC绝对龙头，客户级AI收入和设计赢金额未披露",
        ),
        "风险调整收益": (
            "第 {rank}/{total}，{tier} 档",
            "P/S 2.50x、收入恢复和多产品分散度给出一定赔率，若MOSFET/被动件mix修复可上修利润",
            "Forward PE 38.05x、TTM EPS接近零、FCF受2026 capex 4.00-4.40亿美元压制，SOXX压力窗口累计-93.85%",
        ),
        "下行保护优先": (
            "第 {rank}/{total}，{tier} 档",
            "被动件/分立器件多元终端、backlog和低P/S提供部分底盘",
            "MOSFET分部OPM仅0.8%、FCF偏紧、Call IV 115.0%、历史压力窗口表现弱，不适合作为防守核心",
        ),
        "估值消化优先": (
            "第 {rank}/{total}，{tier} 档",
            "P/S 2.50x且基准收入相对2025增长约+16%-22%，若毛利率修复可部分消化估值",
            "Forward PE 38.05x已经要求利润恢复，若MOSFET ASP和Newport固定成本不改善，估值消化会停留在收入层面",
        ),
        "近端催化优先": (
            "第 {rank}/{total}，{tier} 档",
            "Q2收入/毛利率指引、B2B、backlog turns、分销/OEM结构、MOSFET OPM、Capacitors/Inductors B2B可在1-2季验证",
            "缺少单一大客户订单或AI revenue量化，催化强度弱于已有RPO/长约/明确产能放量标的",
        ),
        "价格确认/动量": (
            "第 {rank}/{total}，{tier} 档",
            "过去1个月+24.53%，说明市场已开始交易周期恢复和AI电源可选性",
            "过去两周仅+0.44%，不是持续最强趋势；高IV意味着动量也可能快速反转",
        ),
        "激进短线": (
            "第 {rank}/{total}，{tier} 档",
            "Call IV 115.0%、Put IV 115.2%、1个月+24.53%，叠加AI电源、800VDC和周期修复，短线进攻属性较强",
            "不是最高关注度AI主链，且若Q2/Q3不能证明订单质量，短线高IV会反噬",
        ),
    }

    def position(strategy: str) -> str:
        return support[strategy][0].format(
            rank=a.get("ranks", {}).get(strategy),  # type: ignore[union-attr]
            total=a.get("rank_total", {}).get(strategy, n),  # type: ignore[union-attr]
            tier=a.get("tiers", {}).get(strategy),  # type: ignore[union-attr]
        )

    lines: list[str] = [
        "# VSH 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：VSH / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV、过去两周/过去1个月区间涨跌、SOXX三段压力窗口均为 2026-06-23 本地快照。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 VSH vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。VSH的优势集中在低P/S、订单恢复、Q2指引、1个月价格确认和高IV短线弹性；它是AI电源链和被动/分立器件的周期恢复标的，而不是全项目最高质量AI主链公司。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是SOXX压力窗口累计-93.85%、FCF受2026 capex压制、MOSFET利润率仍低、AI数据中心客户级收入未披露。",
        "- A 最适合的投资者画像：愿意押注半导体/工业/汽车去库存结束、分销订单转真实出货、被动件和分立器件利润率修复，并接受高波动来换取AI电源链可选性的资金。",
        "- A 最不适合的投资者画像：追求最强AI主链、硬RPO/长约、强现金流防守、低IV、或估值已经被高利润质量充分支撑的稳健资金。",
        f"- 多数思路下最强反方公司：{'、'.join(str(row['ticker']) for row in strong_b[:12])}。这些公司通常在AI主链收入、订单/RPO、利润质量、下行保护、估值消化或更强价格确认上压过VSH。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：VSH是项目内中游偏进攻的恢复+AI电源可选性标的，最终选择为A的对比 {final_a} 家、B的对比 {final_b} 家；它强于部分低增速、资料不足或远期反证更重的公司，但面对顶级AI计算、存储、云、强电气设备和优质同业时多数思路落后。",
        "- 后续最重要跟踪数据：Q2/Q3 revenue、gross margin、segment book-to-bill、backlog月数、分销/OEM/EMS结构、MOSFET segment OPM、Newport/12英寸扩产拖累、capex和库存、FCF、Capacitors/Inductors B2B、高端AI power product的design win/production quantity/lead time、MaxSiC/1200V模块客户进展。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "VSH"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "配电_电源_功率器件")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "35.5-37.5 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '38.5-41.0 亿美元'}；极度乐观：{a.get('extreme_rev') or '42.0-45.5 亿美元'}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a.get('base_margin') or '3.5%-5.5%'}；利润/现金流：{a.get('base_profit') or 'EBITDA 3.3-4.3 亿美元；净利润 0.6-1.2 亿美元'}；{a.get('base_cash') or 'FCF -1.0 亿美元至小幅转正'}"]),
        base.row(["最大传导瓶颈", "Q1高book-to-bill中分销补库存和安全库存成分较高，需求能否转成OEM/EMS可确认出货仍需Q2-Q3验证。"]),
        base.row(["最大反证", "VSH不披露AI数据中心单独收入或hyperscaler/NVIDIA/AMD/OCP平台design win金额；MOSFET分部Q1 OPM仅0.8%，2026 capex 4.00-4.40亿美元压制FCF。"]),
        base.row(["近端催化剂", "Q2/Q3收入和毛利率、backlog转化、B2B续航、分销/OEM结构、MOSFET OPM、Inductors/Capacitors高利润mix、MaxSiC/AI power客户线索。"]),
        base.row(["日度市场数据", daily_snapshot_text(a)]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        lines.append(base.row([strategy, a.get("tiers", {}).get(strategy, "资料不足"), position(strategy), support[strategy][1], support[strategy][2]]))  # type: ignore[union-attr]

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与VSH在分立半导体、功率器件、被动元件、保护器件、current sense、电感/电容和板级电源完整性需求池重叠；优先看订单、收入兑现、毛利率、产品代际、客户认证和估值。", "MRAAY、TTDKY、IFNNY、DIOD、LFUS、MPWR、POWI、NVTS、WOLF、ON、TXN", "判断力度最高；若同业在AI电源、高端MLCC/GaN/SiC、利润率、净现金或价格确认上明显更强，可在对应列压过VSH。"]),
        base.row(["相邻替代", "同属AI电源、板级供电、连接器、电气设备、数据中心配电或物理基础设施资金篮子，但产品不完全竞争。", "ETN、HUBB、NVT、POWL、VRT、APH、CRDO、GLW、SITM、SMTC", "重点回答资金只能买一个时谁的订单硬度、增长质量、利润捕获、估值消化和近端催化更好。"]),
        base.row(["上下游", "B是AI芯片/服务器/云/IDC需求端，或电力/工程/储能/公用事业客户与项目链；VSH可能从其capex中获得器件收入，但下游规模不自动等同VSH利润。", "NVDA、AVGO、MU、SMCI、DELL、MSFT、AMZN、GOOGL、CRWV、CEG、PWR、VST", "区分系统/平台利润池与VSH低中ASP元件利润池；核心看议价权、订单硬度和收入确认链条。"]),
        base.row(["跨赛道", "半导体设备、材料、工业、医疗、软件等业务差异大但作为项目内资金配置替代仍可比较。", "ASML、AMAT、LRCX、TSM、LIN、TMO、DHR、ADBE、RKLB", "默认降低结论力度；除非增长质量、估值、风险调整收益或动量明显拉开，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    lines.append(base.row(headers))
    lines.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        lines.append(
            base.row(
                [
                    index,
                    base.short_name(b),  # type: ignore[arg-type]
                    base.category_short(str(b.get("category", ""))),  # type: ignore[union-attr]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(comparison["ac"], comparison["bc"], comparison["nc"]),  # type: ignore[arg-type]
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

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
    for index, comparison in enumerate(strong_b, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        catchup = "VSH需要披露更清晰的AI/data-center客户、订单金额、design win和收入确认节奏，并证明MOSFET/被动件利润率和FCF随收入恢复同步改善。"
        if comparison["rel"] == "直接同业":
            catchup = "VSH需要在同业中证明AI电源、MaxSiC、高端电容/电感/current sense的订单、毛利率和客户认证强于B。"
        elif comparison["rel"] == "上下游":
            catchup = "VSH需要证明下游AI capex能持续落到其元件收入和利润，而不是只停留在行业TAM映射。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins[:6]), comparison["reason"], catchup]))  # type: ignore[arg-type]

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_a, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        catchup = "B需要拿出更硬的NTM收入/利润兑现、现金流质量、估值消化或明确订单/客户证据。"
        if float(b.get("scores", {}).get("右尾弹性优先", 0)) > float(a.get("scores", {}).get("右尾弹性优先", 0)):  # type: ignore[union-attr]
            catchup = "B需要把右尾叙事转成可确认收入、利润和现金流，并降低估值、融资或执行反证。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins[:6]), comparison["reason"], catchup]))  # type: ignore[arg-type]

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/配电_电源_功率器件/VSH_Vishay Intertechnology_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`；`行业调研/AI服务器_存储_芯片/行业调研_MLCC与高端陶瓷电容_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。日度金融数据可用价格覆盖 {n - len(missing_fin)}/{n} 家；缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}。",
        f"- 公司 A 日度数据摘录：{daily_snapshot_text(a)}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_vsh_company_comparison.py`。脚本复用项目内正式评估与2026-06-23金融资料解析函数，对VSH的Q1收入、Q2指引、backlog、book-to-bill、AI电源链可选性、MOSFET利润率、capex/FCF、估值和价格动量做目标公司校准后建档；未读取下游量化目录或现成排序结论作为决策依据。",
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
    apply_daily_path_overrides()
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 VSH 正式评估文件")
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
                "vsh_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "vsh_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "vsh_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
