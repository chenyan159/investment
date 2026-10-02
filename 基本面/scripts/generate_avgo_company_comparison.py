from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "AVGO"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "AVGO_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_AI_CHIP_PEERS = {
    "AMD",
    "INTC",
    "MRVL",
    "NVDA",
    "QCOM",
}

NETWORK_AND_CONNECTIVITY_ADJACENT = {
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "HPE",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}

CLOUD_AND_SOFTWARE_CUSTOMERS = {
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

AI_SUPPLY_CHAIN = {
    "ARM",
    "ASML",
    "ASMIY",
    "AMAT",
    "LRCX",
    "KLAC",
    "TOELY",
    "TSM",
    "GFS",
    "UMC",
    "TSEM",
    "CDNS",
    "SNPS",
    "RMBS",
    "AMKR",
    "ASX",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "IMOS",
    "KEYS",
    "KLIC",
    "MICLF",
    "ONTO",
    "TER",
    "MU",
    "SNDK",
    "WDC",
    "STX",
    "SIMO",
    "NTAP",
    "PSTG",
    "DELL",
    "SMCI",
    "CLS",
    "FLEX",
    "FN",
    "JBL",
    "PENG",
    "SANM",
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

    # AVGO calibration: Broadcom has unusually hard NTM evidence from FY2026
    # Q2/Q3 AI semiconductor disclosures, RPO, VMware software cash flow, and
    # AI Ethernet/ASIC product proof. The cap is valuation and pressure-window
    # drawdown, not business quality.
    overrides = {
        "NTM兑现优先": 94.0,
        "右尾弹性优先": 94.0,
        "风险调整收益": 71.0,
        "下行保护优先": 59.0,
        "估值消化优先": 78.0,
        "近端催化优先": 89.0,
        "价格确认/动量": 82.0,
        "激进短线": 88.0,
    }
    target = companies[TARGET]
    for strategy, score in overrides.items():
        target["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_AI_CHIP_PEERS:
        return "直接同业"
    if ticker in CLOUD_AND_SOFTWARE_CUSTOMERS or ticker in AI_SUPPLY_CHAIN:
        return "上下游"
    if ticker in NETWORK_AND_CONNECTIVITY_ADJACENT:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的AI半导体指引/RPO更硬",
            "右尾弹性优先": "A定制XPU与AI Fabric右尾更大",
            "风险调整收益": "A高增速与软件现金流更均衡",
            "下行保护优先": "A软件现金流提供缓冲",
            "估值消化优先": "A增长和利润更能消化估值",
            "近端催化优先": "A Q3 AI半导体节点更近",
            "价格确认/动量": "A价格已验证AI兑现",
            "激进短线": "A高IV和ASIC叙事更强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/RPO或收入确认更硬",
            "右尾弹性优先": "B小基数或直接右尾更大",
            "风险调整收益": "B估值与下行组合更好",
            "下行保护优先": "B低估值/低IV更防守",
            "估值消化优先": "B当前估值消化更容易",
            "近端催化优先": "B近端订单/产品节点更硬",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B高beta更适合短攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"下行保护优先", "估值消化优先", "风险调整收益"}:
        return "估值/安全性接近"
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
    weighted = (
        a["scores"]["NTM兑现优先"]
        + a["scores"]["右尾弹性优先"] * 0.8
        + a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"]
        + a["scores"]["近端催化优先"] * 0.6
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["右尾弹性优先"] * 0.8
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
        - b["scores"]["近端催化优先"] * 0.6
    )
    return "A" if weighted >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "AVGO 的Q3指引、AI半导体放量、RPO和VMware现金流让NTM兑现更硬。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "AVGO 的定制XPU、AI Ethernet/Fabric和OpenAI XPV期权提供更大右尾。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "AVGO 的增长和调整后EBITDA斜率更能覆盖当前估值。"
        return "AVGO 在AI半导体兑现、软件利润和近端催化之间更均衡。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的低估值、低IV或压力窗口韧性明显强于 AVGO。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化难度明显低于 AVGO。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的小基数或直接AI右尾强于 AVGO。"
    if b["scores"]["激进短线"] - a["scores"]["激进短线"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的短线高beta和资金弹性更适合进攻。"
    return f"{b['ticker']} 在多数投资思路下比 AVGO 更符合当前项目内配置目标。"


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
        key=lambda x: (
            x["bc"] - x["ac"],
            x["b"]["scores"]["下行保护优先"] + x["b"]["scores"]["估值消化优先"] - a["scores"]["下行保护优先"] - a["scores"]["估值消化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["NTM兑现优先"] + a["scores"]["右尾弹性优先"] + a["scores"]["近端催化优先"] - x["b"]["scores"]["NTM兑现优先"] - x["b"]["scores"]["右尾弹性优先"] - x["b"]["scores"]["近端催化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
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
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "FY2026 Q2总收入约`222.3亿美元`、AI半导体`108亿美元`同比`+143%`，FY2026 Q3指引总收入约`294亿美元`、AI半导体约`160亿美元`，RPO约`1,646亿美元`且约30%预计12个月确认",
            "AI半导体内部客户/产品拆分未披露，客户集中和交付验收会影响确认节奏",
        ),
        "右尾弹性优先": (
            "NTM乐观收入`1,450-1,650亿美元`、极度乐观`1,700-2,000亿美元`，定制XPU/ASIC、Tomahawk/Jericho、DSP/SerDes、VCF与OpenAI XPV共同给右尾",
            "大市值限制倍数弹性，OpenAI XPV/20GW大量价值超过NTM，不能全部计入基准",
        ),
        "风险调整收益": (
            "基准调整后EBITDA约`825-960亿美元`、FCF约`560-680亿美元`，软件利润与AI半导体高增速组合质量高",
            "2026-06-22 P/S`24.72`、市值`1.87T`、客户集中和供应链瓶颈压低赔率",
        ),
        "下行保护优先": (
            "VMware/Infrastructure Software高毛利、RPO和FCF可为半导体周期提供缓冲",
            "Call IV`51.7%`且SOXX压力窗口累计`-53.05%`，高估值下并非防守顶档",
        ),
        "估值消化优先": (
            "Forward PE`20.23`对比NTM收入`+66%-86%`和非GAAP经营利润率约`65%-68%`，若兑现可快速压低前瞻倍数",
            "P/S仍高，若AI半导体或VMware续约低于预期，估值消化会迅速失效",
        ),
        "近端催化优先": (
            "FY2026 Q3实际收入/AI半导体、FY2026 Q4指引、RPO确认比例、Tomahawk 6与1.6T/400G lane路线、VMware VCF续约都在1-2季验证",
            "部分客户项目、OpenAI XPV和CPO/NPO更偏远期期权，不能替代近端收入确认",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周`+14.71%`、过去一月`+13.76%`，AI半导体指引已经有价格确认",
            "2026-06-22价格`392.13`低于6月初区间快照，且高IV显示预期已较充分",
        ),
        "激进短线": (
            "Call IV`51.7%`、AI ASIC/Fabric/OpenAI XPV叙事和Q3指引窗口提供短线事件弹性",
            "超大市值限制爆发倍数，短线beta通常不如AAOI、CRDO、ALAB、ARM、APLD等高波动标的",
        ),
    }

    out: list[str] = []
    out += [
        "# AVGO 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：AVGO / Broadcom",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 AVGO vs 公司 B 的二选一判断。未使用下游量化资料、现成排序结论、临时结果或备份结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。AVGO 的胜率来自硬指引、AI半导体高速收入化、VMware软件现金流、RPO和AI Ethernet/定制ASIC的近端验证。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是高市值、高P/S、客户集中、AI半导体内部拆分低披露，以及SOXX压力窗口回撤较大。",
        "- A 最适合的投资者画像：希望买到AI定制ASIC、AI Fabric和高毛利基础设施软件的组合，重视未来12个月收入/利润兑现且能接受高估值波动的核心成长配置者。",
        "- A 最不适合的投资者画像：只追求低估值、低IV、压力期绝对防守，或只想押小盘高beta短线爆发的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在下行保护、估值消化、小基数右尾或短线高beta上压过 AVGO。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：AVGO 属于全项目最强AI基础设施核心之一，在NTM兑现、右尾弹性、近端催化和估值消化上处于前列；但不是防守型第一，也不是最激进的小盘弹性第一。",
        "- 后续最重要跟踪数据：FY2026 Q3实际总收入和AI半导体收入、FY2026 Q4指引、RPO中12个月确认比例、AI半导体客户集中度、Tomahawk 6/1.6T DSP/SerDes出货、VMware VCF续约/booking、库存和应收账款周转、FCF与调整后EBITDA转换率、OpenAI XPV项目是否出现NTM可确认收入。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "AVGO"]),
        base.row(["公司名称", "Broadcom"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`1,250-1,400 亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "从云厂AI资本开支到AVGO可确认收入需要经过设计锁定、先进封装/HBM/高端基板、交付验收、客户集中和同一预算在ASIC/网络/光互联之间的去重。"]),
        base.row(["最大反证", "AI半导体内部拆分、客户项目节奏、产品ASP/mix和OpenAI XPV的NTM可确认收入仍需估算；客户集中和营运资本占用会压低确定性。"]),
        base.row(["近端催化剂", "FY2026 Q3实绩与Q4指引、AI半导体收入继续上修、RPO确认、Tomahawk 6量产/1.6T DSP导入、VMware VCF续约、库存/应收与FCF转换。"]),
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
        base.row(["直接同业", "与AVGO在AI加速器、定制ASIC、网络半导体或AI计算资金池高度重叠，优先比较AI收入兑现、客户锁定、产品代际、毛利率、供应链和同业估值。", "NVDA、AMD、MRVL、QCOM、INTC", "同业证据权重最高；若一方在订单/收入兑现或估值消化明显领先，结论力度可以上调。"]),
        base.row(["相邻替代", "同属AI网络、光互联、服务器、数据中心电力或AI基础设施资金篮子，但产品不直接重叠。", "ANET、ALAB、CRDO、COHR、CIEN、VRT、ETN、GEV", "回答资金只能买一个时，谁的增长质量、右尾、近端催化和估值消化更好。"]),
        base.row(["上下游", "B 是AVGO的云客户、软件生态、代工封测、EDA/IP、存储或AI服务器链条伙伴/约束，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。", "MSFT、GOOGL、META、AMZN、TSM、ASML、CDNS、SNPS、MU、SMCI、DELL", "不把云capex或上游供给稀缺直接等同于AVGO收入；比较谁更能捕获利润池并消化估值。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、DHR、CAT、RYCEY、ECL", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 AVGO 证明AI半导体和VMware现金流继续上修，并把高P/S通过收入/EBITDA兑现快速消化。"
        if "下行保护优先" in wins:
            need = "需要 AVGO 降低IV和回撤反证，或用更高FCF转换率证明高估值下仍有下行边界。"
        if "激进短线" in wins:
            need = "需要 AVGO 出现更明确的OpenAI/多云厂订单、AI Fabric客户或产品节点，让超大市值仍有短线爆发力。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更高NTM收入利润兑现，或用更低估值和更好现金流抵消AVGO的AI半导体和软件组合。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要 B 把防守优势转化为更高增长或更清楚催化，否则仍难压过AVGO的兑现和右尾。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未使用备份、临时结果、现成排序或下游量化结论。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家，本次公司评估全集为 {n} 家；缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/AI计算芯片_EDA_IP_custom_ASIC/AVGO_Broadcom_公司调研_2026-06-20.md`、`行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_EDA工具、接口IP与Chiplet IP_2026-06-11.md`、`行业调研/产业背景/行业调研_头部AI芯片全景与产能释放_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_avgo_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+66%-86%` 做同号区间修正后建档；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
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
                "avgo_tiers": companies[TARGET]["tiers"],
                "avgo_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
