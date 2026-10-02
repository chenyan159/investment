from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base


TARGET = "TSLA"
TARGET_NAME = "Tesla"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "TSLA_逐家公司投资思路对比_2026-06-23.md"
FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_ENERGY_STORAGE = {"FLNC", "ENPH"}
ENERGY_POWER_ADJACENT = {
    "AEP",
    "AMPX",
    "BE",
    "BWXT",
    "CEG",
    "CMI",
    "DTE",
    "ENS",
    "ET",
    "ETR",
    "FCEL",
    "GEV",
    "GNRC",
    "OKLO",
    "PSIX",
    "RYCEY",
    "SMR",
    "VST",
}
AI_FACILITY_ADJACENT = {
    "AAON",
    "ALLE",
    "CARR",
    "CAT",
    "DCI",
    "DOV",
    "EME",
    "FIX",
    "FTV",
    "JCI",
    "MOD",
    "MSI",
    "MYRG",
    "PH",
    "PNR",
    "PWR",
    "RKLB",
    "TT",
    "VRT",
}
DATA_CENTER_CUSTOMERS = {
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
SERVER_AND_NETWORK_CHAIN = {
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
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
    "GLW",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "PENG",
    "POET",
    "SANM",
    "SMCI",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}
SEMI_AI_SUPPLY_CHAIN = {
    "ACLS",
    "ACMR",
    "ADI",
    "AEHR",
    "AEIS",
    "AMAT",
    "AMD",
    "AMKR",
    "ARM",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "AVGO",
    "BESIY",
    "CAMT",
    "CDNS",
    "COHU",
    "DSCSY",
    "FORM",
    "GFS",
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
    "MRVL",
    "MTSI",
    "MU",
    "MXL",
    "NVDA",
    "NVMI",
    "NVTS",
    "ON",
    "ONTO",
    "PLAB",
    "POWI",
    "QCOM",
    "RMBS",
    "SIMO",
    "SITM",
    "SNPS",
    "STM",
    "TER",
    "TOELY",
    "TSM",
    "TXN",
    "UCTT",
    "UMC",
    "VECO",
    "VICR",
    "WDC",
    "WOLF",
}
MATERIAL_AND_INDUSTRIAL_SUPPLY = {
    "ABBNY",
    "AJNMY",
    "AOSL",
    "APD",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "DHR",
    "DKILY",
    "ECL",
    "ENTG",
    "HOCPY",
    "HTHIY",
    "HUBB",
    "IFNNY",
    "LFUS",
    "LIN",
    "MIELY",
    "MMM",
    "MRAAY",
    "MTRN",
    "NDSN",
    "NVT",
    "PH",
    "POWL",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
    "ST",
    "TDY",
    "TMO",
    "TTDKY",
    "VSH",
}


def mid_growth(value: object) -> float | None:
    text = str(value).replace("−", "-").replace("～", "-").replace("—", "-").replace("–", "-")
    ranged = re.search(
        r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%\s*(?:至|到|-)\s*([+-]?)\s*(\d+(?:\.\d+)?)\s*%",
        text,
    )
    if not ranged:
        ranged = re.search(r"([+-])\s*(\d+(?:\.\d+)?)\s*-\s*([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text)
    if ranged:
        sign1, num1, sign2, num2 = ranged.groups()
        signed1 = -1 if sign1 == "-" else 1
        signed2 = -1 if sign2 == "-" else signed1 if sign2 == "" else 1
        return (signed1 * float(num1) + signed2 * float(num2)) / 2
    vals: list[float] = []
    for match in re.finditer(r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text):
        vals.append((-1 if match.group(1) == "-" else 1) * float(match.group(2)))
    return sum(vals) / len(vals) if vals else None


def fix_growth_ranges(companies: dict[str, dict[str, object]]) -> None:
    for company in companies.values():
        for scenario, field in [
            ("bear", "bear_growth"),
            ("base", "base_growth"),
            ("bull", "bull_growth"),
            ("extreme", "extreme_growth"),
        ]:
            record = company.get("scenarios", {}).get(scenario, {})  # type: ignore[union-attr]
            for key, value in record.items():
                if "增速" in key or "绝对" in key:
                    parsed = mid_growth(value)
                    if parsed is not None:
                        company[field] = parsed
                    break


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
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


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    fix_growth_ranges(companies)
    base.score_companies(companies)

    # TSLA has very large optionality, but the latest formal evaluation and
    # 2026-06-23 market data both argue against treating it as a top-tier
    # NTM/valuation/downside name: base growth is mid-single to low-teens,
    # FCF is negative in the base case, and forward PE/P-S are high.
    tsla_scores = {
        "NTM兑现优先": 68.0,
        "右尾弹性优先": 84.0,
        "风险调整收益": 39.0,
        "下行保护优先": 30.0,
        "估值消化优先": 28.0,
        "近端催化优先": 76.0,
        "价格确认/动量": 44.0,
        "激进短线": 82.0,
    }
    companies[TARGET]["scores"] = tsla_scores  # type: ignore[index]
    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_ENERGY_STORAGE:
        return "直接同业"
    if ticker in DATA_CENTER_CUSTOMERS or ticker in SERVER_AND_NETWORK_CHAIN or ticker in SEMI_AI_SUPPLY_CHAIN:
        return "上下游"
    if ticker in ENERGY_POWER_ADJACENT or ticker in AI_FACILITY_ADJACENT:
        return "相邻替代"
    if ticker in MATERIAL_AND_INDUSTRIAL_SUPPLY:
        return "上下游"
    if category in INFRA_CATS or category == "电力_发电_能源_储能":
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    if tag == "中性":
        return "业务差异大且证据互抵" if rel == "跨赛道" else "档位接近且证据互有强弱"

    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "TSLA汽车/储能/服务底盘更大",
            "右尾弹性优先": "Megapack、Robotaxi和Optimus右尾更大",
            "风险调整收益": "TSLA右尾可部分抵消估值反证",
            "下行保护优先": "TSLA现金余额和规模略有缓冲",
            "估值消化优先": "Energy和高毛利服务若兑现可消化部分估值",
            "近端催化优先": "Robotaxi、FSD和Energy节点更近",
            "价格确认/动量": "TSLA仍有高关注度和交易流动性",
            "激进短线": "Robotaxi/Optimus叙事更适合短线进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}储能/能源收入兑现更短链",
            "右尾弹性优先": f"{ticker}小基数或储能弹性更大",
            "风险调整收益": f"{ticker}估值和反证组合更好",
            "下行保护优先": f"{ticker}压力期或估值缓冲更强",
            "估值消化优先": f"{ticker}业绩更容易覆盖当前估值",
            "近端催化优先": f"{ticker}订单/项目催化更明确",
            "价格确认/动量": f"{ticker}价格趋势确认更强",
            "激进短线": f"{ticker}短线beta或事件弹性更强",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}订单/RPO或利润兑现更硬",
            "右尾弹性优先": f"{ticker} AI主链或供应瓶颈右尾更直接",
            "风险调整收益": f"{ticker}增长、现金流和估值组合更优",
            "下行保护优先": f"{ticker}现金流、估值或压力期表现更稳",
            "估值消化优先": f"{ticker}当前倍数更能被业绩消化",
            "近端催化优先": f"{ticker}产品、订单或财报节点更清楚",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker} 高beta或AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS or category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}未来12个月兑现证据更直接",
            "右尾弹性优先": f"{ticker}小基数或AI收入弹性更大",
            "风险调整收益": f"{ticker}风险调整赔率更好",
            "下行保护优先": f"{ticker}估值或现金流安全边际更强",
            "估值消化优先": f"{ticker}估值消化压力低于TSLA",
            "近端催化优先": f"{ticker}近端订单/产能催化更明确",
            "价格确认/动量": f"{ticker}价格行为验证更充分",
            "激进短线": f"{ticker}短线爆发力或资金偏好更强",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker}经营兑现更清楚",
        "右尾弹性优先": f"{ticker}右尾质量或可信度更好",
        "风险调整收益": f"{ticker}估值和反证组合更优",
        "下行保护优先": f"{ticker}防守性和现金流更好",
        "估值消化优先": f"{ticker}当前估值更易消化",
        "近端催化优先": f"{ticker}近端事件更确定",
        "价格确认/动量": f"{ticker}价格趋势更强",
        "激进短线": f"{ticker}短线弹性更强",
    }[strategy]


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
    return f"{tag}：{reason_for(strategy, tag, b, rel)}"


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
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    ticker = str(b["ticker"])
    if final == "A":
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
            return "TSLA 的 Megapack、Robotaxi、FSD/Optimus 右尾明显更大。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "TSLA 近端 Robotaxi/FSD/Energy 节点更容易触发重定价。"
        return "TSLA 主要靠远期期权和短线关注度胜出，非估值防守型选择。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{ticker} 的 NTM 收入、订单或利润兑现证据更硬。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker} 的当前估值更容易被未来业绩消化。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker} 的现金流、估值或压力期韧性明显强于 TSLA。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 16:  # type: ignore[index,operator]
        return f"{ticker} 的价格确认和资金偏好更强。"
    return f"{ticker} 在多数投资思路下比 TSLA 更符合当前配置目标。"


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


def fmt_num(value: object, suffix: str = "") -> str:
    if value is None:
        return "缺失"
    if isinstance(value, float):
        return f"{value:.2f}{suffix}"
    return f"{value}{suffix}"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    return f"${float(value):.2f}B"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    return f"{float(value):.2f}%"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def current_vs_momentum(fin: dict[str, object], mom: dict[str, object]) -> str:
    current = fin.get("price")
    prior = mom.get("latest_close")
    if current is None or prior is None:
        return "缺失"
    change = (float(current) / float(prior) - 1) * 100
    return f"{change:+.2f}%"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = sorted(
        comparisons,
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["右尾弹性优先"] - x["b"]["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:55]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"] or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    vs_jun3 = current_vs_momentum(fin, mom1)
    daily_snapshot = (
        f"2026-06-23 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}；2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、"
        f"过去一月 {fmt_pct(mom1.get('mom1m'))}，2026-06-23 相对 2026-06-03 收盘约 {vs_jun3}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = []
    for product in a["products"][:8]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "NTM基准收入 `1040-1120亿美元`、基准可信度中高；汽车、Energy、Services均有分部收入锚",
            "基准增速仅约 `+6%-+14%`，汽车需求/ASP和Energy项目确认仍是瓶颈，基准FCF为负",
        ),
        "右尾弹性优先": (
            "Megapack/Megablock、FSD/Robotaxi、Cybercab、Optimus和AI5形成多条远期期权",
            "极度乐观收入 `1450-1650亿美元` 可信度低，需需求、监管、量产、利润率和CapEx同时成立",
        ),
        "风险调整收益": (
            "TSLA有大市值流动性、现金余额、Energy高增长和Robotaxi/FSD可选上行",
            "Forward PE `152.24`、P/S `14.61`、EV/EBITDA `134.59`，NTM FCF基准 `-30至-80亿美元`",
        ),
        "下行保护优先": (
            "现金余额和多业务底盘提供一定缓冲，Energy/Services比纯汽车更分散",
            "Call IV `50.2%`、三段SOXX压力窗口累计 `-66.64%`，估值高且汽车端有价格反证",
        ),
        "估值消化优先": (
            "若Energy收入和高毛利服务同步上修，可部分缓解估值压力",
            "当前估值已经要求Robotaxi/FSD/Energy较强兑现，基准收入和利润难单独支撑高倍数",
        ),
        "近端催化优先": (
            "季度交付、Energy GWh/RPO、Robotaxi城市扩张、FSD海外审批、Cybercab/Semi节点均可跟踪",
            "大部分催化仍需披露收入、毛利、车队经济性或外部订单，不宜直接当作已兑现利润",
        ),
        "价格确认/动量": (
            "2026-06-03过去一月 `+8.41%`，TSLA流动性和关注度仍高",
            "2026-06-23价格较2026-06-03约 `-10.17%`，且高估值下价格确认不如硬订单链公司",
        ),
        "激进短线": (
            "Robotaxi、FSD、Optimus和Megapack叙事叠加 `50.2%` Call IV，适合高风险事件交易",
            "短线进攻可以容忍风险，但不能忽视汽车需求、监管、FCF和估值反证",
        ),
    }

    out: list[str] = []
    out += [
        "# TSLA 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：TSLA / Tesla",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-23；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 TSLA vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、项目根 `tmp/`、`分析报告/备份/` 或既有公司对比成品作为决策输入。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。TSLA 在项目内主要靠 Robotaxi/FSD、Megapack/Megablock、Optimus 和高关注度短线叙事取得相对优势。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。核心短板是 Forward PE `152.24`、P/S `14.61`、基准 FCF 为负、SOXX压力窗口回撤深，导致估值消化和下行保护明显弱。",
        "- A 最适合的投资者画像：愿意用较高估值和现金流波动换 Robotaxi/FSD、Energy、Optimus 右尾的进攻型或事件驱动资金；更像高波动长期期权，而不是低风险基本面复利仓位。",
        "- A 最不适合的投资者画像：优先追求 NTM 硬订单兑现、低倍数估值消化、现金流防守、压力期稳定和可验证利润质量的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:15]])}。这些公司通常在订单/RPO、AI主链收入、现金流、估值消化或价格确认上压过 TSLA。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：TSLA 是右尾和短线强、估值和下行保护弱的中高波动标的；在全项目里不是最均衡的配置选择，只有在投资思路明确偏向非线性右尾或事件交易时胜率更高。",
        "- 后续最重要跟踪数据：季度交付/生产/库存天数、Automotive ex-credit GM、Energy revenue/GWh/RPO/GM、Megapack 3/Megablock进度、FSD付费订阅、Robotaxi城市数/paid miles/fleet size/事故率/单车收入、Cybercab/Semi产量、Optimus外部订单和ASP、CapEx/OCF/FCF、现金余额。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "TSLA"]),
        base.row(["公司名称", "Tesla"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`1040-1120 亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "汽车需求和ASP、Energy项目确认与BESS价格竞争、Robotaxi监管/安全/车队运营、Optimus量产和外部付费验证、AI5/Cortex/Research Fab高CapEx。"]),
        base.row(["最大反证", "NTM基准FCF仍为负；Robotaxi/Optimus收入未形成硬披露；汽车库存、价格竞争和高估值共同压制风险调整收益。"]),
        base.row(["近端催化剂", "季度交付和库存、Energy部署/RPO/GM、Robotaxi城市扩张和paid miles、FSD订阅/海外审批、Cybercab/Semi进度、Optimus订单或内部部署数据、CapEx和FCF。"]),
        base.row(["日度市场数据", daily_snapshot]),
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
        base.row(["直接同业", "与 TSLA Energy 在储能/能源系统需求池有明显重叠，优先看储能项目、订单、收入确认、毛利率和估值。", "FLNC、ENPH", "同业证据权重较高；若对手储能订单更硬或估值压力更低，可在NTM/估值列压过TSLA。"]),
        base.row(["相邻替代", "同属AI电力、能源、机电、工业AI或高右尾成长资金篮子，但产品不完全竞争。", "BE、VRT、TT、PWR、GEV、CEG、RKLB、OKLO", "重点比较增长质量、兑现确定性、估值消化、下行保护和近端催化。"]),
        base.row(["上下游", "B 是 TSLA 的AI芯片/半导体/电力电子/材料/云算力/数据中心客户或供应链相关公司。", "NVDA、AMD、TSM、AVGO、MU、MSFT、AMZN、GOOGL、SMCI、ETN", "不把TSLA下游规模或上游稀缺直接等同胜出；看利润捕获、硬订单和估值消化。"]),
        base.row(["跨赛道", "业务差异大，仅作为资金配置替代比较。", "TMO、DHR、LIN、APD、部分材料/工业公司", "默认降低结论力度；只有增长质量、估值消化或风险调整明显拉开时才给建议/强烈建议。"]),
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
                    base.category_short(str(b["category"])),  # type: ignore[index]
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
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要 TSLA 把 Robotaxi/FSD/Energy 叙事转成可确认收入、毛利和FCF，并降低估值消化压力。"
        if "NTM兑现优先" in wins:
            need = "需要 TSLA 提供更硬的季度交付、Energy订单/RPO、Robotaxi收入或FSD订阅增长证据。"
        if "下行保护优先" in wins or "估值消化优先" in wins:
            need = "需要 TSLA 证明基准利润和FCF足以支撑当前估值，并改善压力窗口回撤表现。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更大或更高可信的右尾收入、近端催化和短线资金确认。"
        if b["scores"]["风险调整收益"] > a["scores"]["风险调整收益"]:  # type: ignore[index,operator]
            need = "需要 B 保持风险调整优势，同时补足右尾弹性或事件催化，否则容易输给 TSLA 的期权价值。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、项目根 `tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`特征量化/` 或既有公司对比成品。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-23 金融快照覆盖情况见对应金融资料；本次公司全集中缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/机电_冷却_工程_水处理_边缘工业AI/TSLA_Tesla_公司调研_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI边缘推理芯片_2026-06-11.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研、IR、SEC、产品公告和财报来源。",
        "- 自动化脚本：`scripts/generate_tsla_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 TSLA 的汽车/Energy/FSD/Robotaxi/Optimus/AI5、Forward PE/P-S/IV、区间涨跌和 SOXX 压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论、备份/tmp或既有公司对比成品作为决策输入。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
    base.REPORT_DATE = REPORT_DATE
    base.FIN_PATH = FIN_PATH
    base.OUT_PATH = OUT_PATH
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    print(
        json.dumps(
            {
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "tsla_tiers": companies[TARGET]["tiers"],
                "tsla_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
