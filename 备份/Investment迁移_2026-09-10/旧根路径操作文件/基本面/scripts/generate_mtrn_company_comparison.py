from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base


TARGET = "MTRN"
TARGET_NAME = "Materion"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MTRN_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_MATERIAL_PEERS = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "DKILY",
    "ENTG",
    "HOCPY",
    "LIN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}

SPECIALTY_ADJACENT = {
    "DHR",
    "ECL",
    "MMM",
    "NDSN",
    "TMO",
    "MRAAY",
    "TTDKY",
    "VSH",
    "LFUS",
    "BELFB",
    "APH",
    "TEL",
    "VIAV",
    "GLW",
    "COHR",
    "LITE",
}

SEMICON_DOWNSTREAM = {
    "ADI",
    "AMD",
    "ARM",
    "AVGO",
    "CDNS",
    "INTC",
    "MCHP",
    "MRVL",
    "NVDA",
    "ON",
    "QCOM",
    "STM",
    "TXN",
    "ALAB",
    "SNPS",
    "MXL",
    "TSM",
    "ASML",
    "AMAT",
    "LRCX",
    "KLAC",
    "TOELY",
    "ASMIY",
    "ACMR",
    "ACLS",
    "GFS",
    "TSEM",
    "UMC",
    "NVMI",
    "VECO",
    "UCTT",
    "ICHR",
    "MKSI",
    "DSCSY",
    "AMKR",
    "ASX",
    "ATEYY",
    "BESIY",
    "ASMVY",
    "CAMT",
    "FORM",
    "TER",
    "COHU",
    "AEHR",
    "KLIC",
    "KEYS",
    "ONTO",
    "PLAB",
    "IMOS",
    "MICLF",
}

AI_AND_DATA_CENTER_BASKET = {
    "AAOI",
    "ANET",
    "BDC",
    "CIEN",
    "CRDO",
    "CSCO",
    "LWLG",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "DELL",
    "FN",
    "HPE",
    "JBL",
    "MRAM",
    "NTAP",
    "PENG",
    "SANM",
    "SMCI",
    "STX",
    "WDC",
    "CLS",
    "FLEX",
    "MU",
    "PSTG",
    "RMBS",
    "SIMO",
    "SNDK",
    "ADBE",
    "AMZN",
    "APLD",
    "CRWD",
    "CRWV",
    "DLR",
    "GOOGL",
    "IBM",
    "IREN",
    "META",
    "MSFT",
    "NTNX",
    "ORCL",
    "BABA",
    "EQIX",
    "NBIS",
}

INFRA_AND_DEFENSE_BASKET = {
    "AEP",
    "BE",
    "BWXT",
    "CMI",
    "DTE",
    "ENS",
    "ENPH",
    "ET",
    "ETR",
    "FCEL",
    "GEV",
    "GNRC",
    "OKLO",
    "PSIX",
    "PWR",
    "RYCEY",
    "VST",
    "CEG",
    "FLNC",
    "SMR",
    "AMPX",
    "HTHIY",
    "ALLE",
    "CARR",
    "CAT",
    "DCI",
    "FIX",
    "FTV",
    "MSI",
    "PH",
    "PNR",
    "RKLB",
    "TSLA",
    "TT",
    "VRT",
    "DOV",
    "JCI",
    "MOD",
    "AAON",
    "IESC",
    "EME",
    "MYRG",
    "ABBNY",
    "AOSL",
    "ATKR",
    "DIOD",
    "HUBB",
    "MIELY",
    "MPWR",
    "POWI",
    "POWL",
    "ST",
    "VICR",
    "WOLF",
    "ETN",
    "IFNNY",
    "NVT",
    "NVTS",
}


def patch_percent_parser() -> None:
    def pct_values(value: str) -> list[float]:
        text = base.clean(value).replace("−", "-")
        text = re.sub(r"(?<=%)\s*[-–—~]\s*(?=\d)", "至", text)
        text = re.sub(r"(?<=\d)\s*[-–—~]\s*(?=\d+(?:\.\d+)?\s*%)", "至", text)
        return [float(match.group(1)) for match in re.finditer(r"([+-]?\d+(?:\.\d+)?)\s*%", text)]

    base.pct_values = pct_values
    base.pct_mid = lambda value: (sum(pct_values(value)) / len(pct_values(value)) if pct_values(value) else None)
    base.parse_pct_text = lambda value: (pct_values(value)[0] if pct_values(value) else None)


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    soxx_vals = [c["soxx"].get("soxx_cum") for c in companies.values()]  # type: ignore[union-attr]
    mom2_vals = [c["mom2"].get("mom2w") for c in companies.values()]  # type: ignore[union-attr]
    mom1_vals = [c["mom1"].get("mom1m") for c in companies.values()]  # type: ignore[union-attr]

    for company in companies.values():
        text = f"{company['one']}\n{company['conclusion']}\n{company['calibration']}"
        base_growth = company["base_growth"] if company["base_growth"] is not None else 0
        bull_growth = company["bull_growth"] if company["bull_growth"] is not None else base_growth
        extreme_growth = company["extreme_growth"] if company["extreme_growth"] is not None else bull_growth
        conf = base.conf_score(str(company["base_conf"]))
        extreme_conf = base.conf_score(str(company["extreme_conf"]))
        val = base.valuation_score(company)
        safe = base.iv_safe(company)
        ag_iv = base.iv_aggressive(company)
        soxxp = base.pct_rank(company["soxx"].get("soxx_cum"), soxx_vals)  # type: ignore[union-attr]
        mom2p = base.pct_rank(company["mom2"].get("mom2w"), mom2_vals)  # type: ignore[union-attr]
        mom1p = base.pct_rank(company["mom1"].get("mom1m"), mom1_vals)  # type: ignore[union-attr]
        category = str(company["category"])

        evidence = base.keyword_count(text, ["backlog", "RPO", "订单", "指引", "已披露", "收入表", "book-to-bill", "客户", "合同", "认证", "产能"])
        risk_words = base.keyword_count(text, ["未披露", "缺少", "无法可靠", "低可信", "下移", "不进入基准", "不确定", "风险", "延迟", "瓶颈"])
        cash_words = base.keyword_count(text, ["FCF", "自由现金流", "现金流", "cash flow", "available cash flow", "现金转化", "资产负债表"])
        catalyst = base.keyword_count(text, ["Q2", "Q3", "Q4", "未来 1", "未来1", "1-2 个季度", "订单", "backlog", "RPO", "认证", "产能", "产品发布", "收购", "指引", "财报", "客户", "交付", "Investor Conference"])
        direct_ai = base.has_any(text, ["AI 数据中心", "AI data center", "Blackwell", "Rubin", "GB300", "液冷", "800V", "HBM", "CoWoS", "NeoCloud", "hyperscale", "AI campus", "data center"])
        mature_cash = base.has_any(text, ["现金流强", "FCF 强", "available cash flow", "高利润", "recurring", "服务", "稳定", "公用事业", "regulated"])
        negative_profit = base.has_any(text, ["FCF 为负", "自由现金流为负", "净亏损", "亏损", "负毛利", "破产", "going concern"])
        category_bonus = 4 if category in base.HIGH_GROWTH_CATS else (2 if category in base.INFRA_CATS else 0)

        ntm = 45 + min(max(base_growth, -10), 80) * 0.45 + conf * 0.80 + min(evidence, 10) * 0.80 - min(risk_words, 12) * 0.30 + (3 if mature_cash else 0)
        right = 34 + min(max(extreme_growth, -10), 150) * 0.42 + min(max(extreme_growth - base_growth, 0), 90) * 0.23 + category_bonus + (6 if direct_ai else 0) + ag_iv * 0.07 - max(-extreme_conf, 0) * 0.20
        riskadj = 30 + min(max(base_growth, -10), 80) * 0.22 + min(max(extreme_growth, -10), 140) * 0.14 + conf * 0.55 + (val - 50) * 0.22 + (safe - 50) * 0.12 + soxxp * 0.08 + min(cash_words, 8) * 0.70 - (8 if negative_profit else 0) - min(risk_words, 10) * 0.18
        downside = 28 + safe * 0.22 + soxxp * 0.28 + val * 0.12 + conf * 0.45 + min(cash_words, 8) * 0.80 + (5 if mature_cash else 0) - (12 if negative_profit else 0)
        digestion = 32 + val * 0.35 + min(max(base_growth, -10), 80) * 0.35 + min(max(extreme_growth, -10), 140) * 0.10 + conf * 0.30
        if company["fin"].get("ps") is not None and company["fin"].get("ps") < 3 and base_growth > 5:  # type: ignore[union-attr,operator]
            digestion += 5
        if company["fin"].get("ps") is not None and company["fin"].get("ps") > 20 and base_growth < 50:  # type: ignore[union-attr,operator]
            digestion -= 8
        near = 34 + min(catalyst, 18) * 0.95 + min(max(base_growth, -10), 80) * 0.20 + conf * 0.30 + (6 if direct_ai else 0) + (3 if category in base.INFRA_CATS else 0)
        momentum = 22 + mom2p * 0.42 + mom1p * 0.30 + min(max(company["mom2"].get("mom2w") or 0, -20), 70) * 0.18 + ag_iv * 0.04  # type: ignore[union-attr]
        aggressive = 28 + right * 0.45 + momentum * 0.25 + ag_iv * 0.18 + min(catalyst, 15) * 0.55 - (10 if negative_profit and conf < 0 else 0)

        company["scores"] = {
            "NTM兑现优先": base.clamp(ntm),
            "右尾弹性优先": base.clamp(right),
            "风险调整收益": base.clamp(riskadj),
            "下行保护优先": base.clamp(downside),
            "估值消化优先": base.clamp(digestion),
            "近端催化优先": base.clamp(near),
            "价格确认/动量": base.clamp(momentum),
            "激进短线": base.clamp(aggressive),
        }

    mtrn = companies[TARGET]
    adjustments = {
        "NTM兑现优先": 3,
        "右尾弹性优先": -5,
        "风险调整收益": -3,
        "下行保护优先": 2,
        "估值消化优先": -5,
        "近端催化优先": 0,
        "价格确认/动量": 0,
        "激进短线": -2,
    }
    for strategy, adjustment in adjustments.items():
        mtrn["scores"][strategy] = base.clamp(mtrn["scores"][strategy] + adjustment)  # type: ignore[index,operator]

    for strategy in STRATS:
        ordered = sorted(companies.items(), key=lambda item: item[1]["scores"][strategy], reverse=True)  # type: ignore[index]
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
        if not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company["tiers"][strategy] = "资料不足"  # type: ignore[index]


def fmt_num(value: object, suffix: str = "") -> str:
    if value is None:
        return "缺失"
    return f"{value}{suffix}"


def fmt_money_b(value: object) -> str:
    if value is None:
        return "缺失"
    return f"${float(value):.2f}B"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    return f"{float(value):.2f}%"


def rank_text(company: dict[str, object], strategy: str, total: int) -> str:
    return f"全项目第 {company['ranks'][strategy]}/{total}，{company['tiers'][strategy]} 档"  # type: ignore[index]


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_MATERIAL_PEERS:
        return "直接同业"
    if ticker in SPECIALTY_ADJACENT:
        return "相邻替代"
    if ticker in SEMICON_DOWNSTREAM or category in {"AI计算芯片_EDA_IP_custom_ASIC", "晶圆制造_前道设备", "封测_检测_计量_光罩"}:
        return "上下游"
    if ticker in AI_AND_DATA_CENTER_BASKET or ticker in INFRA_AND_DEFENSE_BASKET or category in {"AI网络_光互联_连接器", "AI服务器_存储_EMS", "云算力_IDC_AI软件平台", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI", "电力_发电_能源_储能"}:
        return "相邻替代"
    return "跨赛道"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    labels = {
        "NTM兑现优先": "NTM",
        "右尾弹性优先": "右尾",
        "风险调整收益": "风调",
        "下行保护优先": "防御",
        "估值消化优先": "估值",
        "近端催化优先": "催化",
        "价格确认/动量": "动量",
        "激进短线": "短线",
    }
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        at = a["tiers"][strategy]  # type: ignore[index]
        bt = b["tiers"][strategy]  # type: ignore[index]
        if at == "资料不足" or bt == "资料不足":
            close.append(labels[strategy])
            continue
        gap = TIER_VAL[at] - TIER_VAL[bt]  # type: ignore[index,operator]
        if gap > 0:
            a_strong.append(labels[strategy])
        elif gap < 0:
            b_strong.append(labels[strategy])
        else:
            close.append(labels[strategy])

    def joined(items: list[str]) -> str:
        return "无" if not items else "/".join(items[:5]) + ("等" if len(items) > 5 else "")

    return f"A强:{joined(a_strong)}；B强:{joined(b_strong)}；接近:{joined(close)}"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的backlog和VA收入更可兑现",
            "右尾弹性优先": "A有ALD/PVD和国防铍右尾",
            "风险调整收益": "A订单质量和下行组合更均衡",
            "下行保护优先": "A材料壁垒和国防订单更稳",
            "估值消化优先": "A用低双位数增长可消化估值",
            "近端催化优先": "A的EM和国防订单验证更近",
            "价格确认/动量": "A价格确认更强",
            "激进短线": "A有材料小盘重定价弹性",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现更清楚",
            "右尾弹性优先": "B高增长右尾更大",
            "风险调整收益": "B赔率或现金流组合更优",
            "下行保护优先": "B估值/现金流安全性更强",
            "估值消化优先": "B倍数更容易被业绩消化",
            "近端催化优先": "B近端订单/产品催化更硬",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B短线爆发力更高",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"下行保护优先", "估值消化优先"}:
        return "估值与安全边际接近"
    return "档位接近需继续验证"


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == bt:
            tag = "中性"
        else:
            tag = "微倾向投B" if at == "资料不足" else "微倾向投A"
        return f"{tag}：关键资料不足"

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
    return f"{tag}：{reason_for(strategy, tag, rel)}"


def direction_counts(cells: list[str]) -> tuple[int, int, int]:
    a_count = b_count = neutral = 0
    for cell in cells:
        tag = base.tag_in_cell(cell) or ""
        if tag.endswith("投A"):
            a_count += 1
        elif tag.endswith("投B"):
            b_count += 1
        else:
            neutral += 1
    return a_count, b_count, neutral


def final_choice(a: dict[str, object], b: dict[str, object], cells: list[str]) -> str:
    a_count, b_count, _neutral = direction_counts(cells)
    if a_count > b_count:
        return "A"
    if b_count > a_count:
        return "B"
    key_weight = (
        a["scores"]["NTM兑现优先"]
        + a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"]
        + a["scores"]["下行保护优先"] * 0.5
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
        - b["scores"]["下行保护优先"] * 0.5
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
            return "MTRN的材料壁垒、国防铍订单和压力期韧性更适合配置。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "MTRN的record backlog、EM VA和A&D订单兑现路径更清楚。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "MTRN的P/S和VA收入基数比高估值AI股更容易消化。"
        return "MTRN在防守、材料壁垒或NTM兑现上略胜，B的右尾不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']}的增长右尾和重定价弹性明显强于MTRN。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']}的未来12个月收入/利润兑现证据强于MTRN。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']}的估值消化或赔率优于MTRN。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']}的价格确认和短线资金偏好更强。"
    return f"{b['ticker']}在多数投资思路下比MTRN更符合当前配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    comparisons: list[dict[str, object]] = []
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [label_for(a, b, strategy, rel) for strategy in STRATS]
        ac, bc, nc = direction_counts(cells)
        final = final_choice(a, b, cells)
        comparisons.append(
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
    return comparisons


def short_name(company: dict[str, object]) -> str:
    return f"{company['ticker']} / {company['name']}"


def category_short(category: str) -> str:
    return category.replace("_", "/") if category else "未分类"


def majority(ac: int, bc: int, nc: int) -> str:
    return f"A {ac} / B {bc} / 中性 {nc}"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    total = len(companies)
    dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(dates)} 至 {max(dates)}"

    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell) or "中性"] += 1

    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: b_side[s] - a_side[s], reverse=True)[:3]
    strong_b = sorted(comparisons, key=lambda x: (x["bc"] - x["ac"], x["bc"], x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]), reverse=True)  # type: ignore[index,operator]
    strong_a = sorted(comparisons, key=lambda x: (x["ac"] - x["bc"], x["ac"], a["scores"]["下行保护优先"] - x["b"]["scores"]["下行保护优先"]), reverse=True)  # type: ignore[index,operator]
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"]]

    product_names = []
    for product in a["products"][:6]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])
    products_text = "；".join(product_names) if product_names else "Electronic Materials；Performance Materials；Precision Optics"

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_line = (
        f"2026-06-22 收盘价 `{fmt_num(fin.get('price'))}`，市值 `{fmt_money_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，P/S `{fmt_num(fin.get('ps'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`，Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03 过去两周 `{fmt_pct(mom2.get('mom2w'))}`、过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    support = {
        "NTM兑现优先": ("Q1 record backlog YoY +20%+、年初以来 +15%，EM VA +17.7%，A&D orders +50%，FY2026 top-line 低双位数", "绝对backlog、分产品订单、取消率未披露，PM/PCS仍拖累"),
        "右尾弹性优先": ("PVD targets、ALD/new metal precursors、国防铍、PO修复都有上行路径", "不是GPU/光模块/液冷主链，AI每rack内容量小，极度乐观可信度低"),
        "风险调整收益": ("材料认证壁垒和国防订单支撑基本面，下行保护强于高beta AI链", "2026-06-22 Forward PE 37.32、TTM PE 75.87，估值已计入乐观"),
        "下行保护优先": ("国防铍、半导体材料客户认证、P/S 3.01和压力窗口韧性提供底座", "现金只有$16M量级，净债务约2.1x EBITDA，营运资本会吞噬FCF"),
        "估值消化优先": ("VA sales基准+7%-15%、EBITDA $245-$275M，P/S低于多数高成长AI硬件", "forward PE仍高，必须看到EM和A&D订单兑现"),
        "近端催化优先": ("Q2/Q3 EM VA、A&D RFQ转PO、PM质量费用消退和PO修复均可验证", "缺少客户级ALD/CPO订单或明确book-to-bill披露"),
        "价格确认/动量": ("截至2026-06-22价格已上行到277.68，动量较多传统材料股更强", "价格上涨也提高估值压力，需基本面同步上修"),
        "激进短线": ("小盘材料、AI半导体材料和国防铍叙事可触发短线重定价", "IV约55%，弹性低于纯AI芯片/光互联/Neocloud高beta标的"),
    }

    opponents = "、".join([f"{x['ticker']}" for x in strong_b_rows[:10]]) or "无"

    out: list[str] = [
        "# MTRN 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：MTRN / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{total}",
        f"被比较公司 B 数量：{total - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04",
        "资料边界：本报告未读取、引用或继承 `特征量化/`；未把 `公司排序/` 的现成排序结果作为决策依据；未读取 `分析报告/公司对比/结果/` 的既有对比报告作为输入。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MTRN 最强的是下行保护与部分NTM兑现：材料认证壁垒、国防铍订单、EM VA增长和record backlog给出真实经营锚。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要问题是右尾不如核心AI硬件/云/光互联，且Forward PE `37.32`、TTM PE `75.87` 已反映较多乐观预期。",
        "- A 最适合的投资者画像：想买小型先进材料平台、接受中等成长、重视半导体材料复苏和国防订单兑现，同时不想承担纯AI高beta波动的配置者。",
        "- A 最不适合的投资者画像：只追求GPU、HBM、CPO、Neocloud、液冷和电力主链高右尾，以及短线高波动爆发的进攻型资金。",
        f"- 多数思路下最强反方公司：{opponents}。这些公司通常在NTM收入弹性、AI主链右尾、近端催化或估值消化上明显强于MTRN。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：MTRN不是全项目顶级成长股，更像半导体材料/国防材料的中上质量、小盘材料重估标的；多数核心AI链公司增长更强，MTRN胜在材料壁垒、订单可见度和下行保护。",
        "- 后续最重要跟踪数据：EM VA与EBITDA/VA、semiconductor order rate、backlog绝对值或book-to-bill、A&D RFQ转PO、$65M defense prime扩产节点、ALD/new-metal客户/产能、PO VA/margin、PM质量费用、经营现金流和营运资本。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "MTRN"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", products_text]),
        base.row(["NTM 基准收入", a["base_rev"]]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润：{a['base_profit']}；现金流：{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "未披露绝对backlog、产品级订单、客户、交付时间和取消率；贵金属pass-through使net sales不能直接当作利润增长。"]),
        base.row(["最大反证", "AI/DC收入不是直接设备收入，PM product quality和precision clad strip仍是抵消项，估值需要EM与国防订单兑现。"]),
        base.row(["近端催化剂", "Q2/Q3 EM VA与margin、A&D RFQ转PO、PM质量费用消退、PO持续修复、ALD/new-metal或CPO客户披露、backlog金额/book-to-bill。"]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        out.append(base.row([strategy, a["tiers"][strategy], rank_text(a, strategy, total), support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "半导体材料、靶材、前驱体、特种化学品、先进基板/材料或高可靠材料需求池重叠，优先看客户认证、订单、利润率和估值。", "ENTG、ROG、Q、AXTI、DD、SHECY、ASGLY、HOCPY、AJNMY", "同业内允许用EM VA、订单、产品代际和估值差给出更明确建议。"]),
        base.row(["相邻替代", "同属AI材料、连接器、光学、电子元件、数据中心基础设施或防御/工业资金篮子，但产品不直接竞争。", "MRAAY、TTDKY、APH、TEL、VRT、ETN、GEV、CEG", "重点比较增长质量、估值消化、近端催化和风险调整收益；默认低于直接同业力度。"]),
        base.row(["上下游", "MTRN是半导体/先进材料上游，B是晶圆制造、设备、封测、芯片、服务器或AI客户需求链。", "TSM、ASML、AMAT、NVDA、MU、AVGO、AMKR、TER", "不把下游收入规模等同MTRN机会，重点看利润池位置、供应瓶颈和订单传导。"]),
        base.row(["跨赛道", "与MTRN业务差异大，只作为项目资金配置替代。", "软件、传统工业、非材料型平台公司", "默认降低结论力度，除非增长、估值消化或下行保护明显拉开。"]),
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

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    if not strong_b_rows:
        out.append(base.row([1, "无", "无", "没有多数思路明显压过MTRN的公司。", "继续跟踪MTRN订单和EM兑现。"]))
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "MTRN需要披露backlog金额、EM持续15%+增长、A&D RFQ转PO、ALD/new-metal客户或PO/CPO订单，并证明估值能被利润消化。"
        if comparison["rel"] == "直接同业":
            need = "MTRN需要在EM VA增速、订单/客户认证、利润率和估值消化上超过该材料同业。"
        out.append(base.row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    if not strong_a_rows:
        out.append(base.row([1, "无", "无", "MTRN没有在多数思路下明显压过足够多公司。", "B侧若补足现金流、订单和估值消化即可保持优势。"]))
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "B需要把收入/利润兑现、现金流和估值消化补强，或拿出明确订单/客户认证来抵消MTRN的材料壁垒。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "B需要把右尾叙事转化为可确认收入/利润，并降低估值和波动反证。"
        out.append(base.row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {total} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {total - len(missing_fin)}/{total} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_line}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- MTRN 公司与行业主要来源：`公司调研/半导体材料_化学品_基板/MTRN_Materion_公司调研_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_硅片、光刻胶与前道材料_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_先进封装材料与热界面材料_2026-06-10.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_硅光材料、光子材料与电光聚合物_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`；`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`。",
        "- 研究方案来源：`分析报告/公司对比/研究方案.md`，未新建或改写方案文件。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    patch_percent_parser()
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 MTRN 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "mtrn_tiers": companies[TARGET]["tiers"],
                "mtrn_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
                "mtrn_ranks": companies[TARGET]["ranks"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
