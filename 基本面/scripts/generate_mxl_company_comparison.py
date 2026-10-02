from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "MXL"
TARGET_NAME = "MaxLinear"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MXL_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_HIGH_SPEED_PEERS = {
    "ALAB",
    "AVGO",
    "CRDO",
    "MRVL",
    "MTSI",
    "SMTC",
}

OPTICAL_AND_COPPER_CHAIN = {
    "AAOI",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CSCO",
    "FN",
    "GLW",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "TEL",
    "VIAV",
    "VISN",
}

PLATFORM_AND_CUSTOMER_CHAIN = {
    "AMD",
    "AMZN",
    "APLD",
    "ARM",
    "BABA",
    "CRWV",
    "DELL",
    "FLEX",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "META",
    "MSFT",
    "NBIS",
    "NVDA",
    "ORCL",
    "PENG",
    "SANM",
    "SMCI",
}

ANALOG_AND_CONNECTIVITY_ADJACENT = {
    "ADI",
    "AOSL",
    "DIOD",
    "IFNNY",
    "MCHP",
    "MPWR",
    "ON",
    "POWI",
    "QCOM",
    "RMBS",
    "SIMO",
    "STM",
    "TXN",
    "VICR",
    "VSH",
}

SEMI_SUPPLY_CHAIN = {
    "ACLS",
    "ACMR",
    "AEHR",
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
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "SNPS",
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
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

    # MXL calibration: 2026Q1 Infrastructure +136%, Q2 guide $160M-$170M,
    # optical DSP/TIA ramp and 224G retimer options make growth and short-term
    # attack strong. The offset is very high IV, negative TTM EPS, high P/S,
    # severe SOXX stress-window drawdown and still-undisclosed customer orders.
    mxl = companies[TARGET]
    overrides = {
        "NTM兑现优先": 81.0,
        "右尾弹性优先": 94.0,
        "风险调整收益": 48.0,
        "下行保护优先": 31.0,
        "估值消化优先": 46.0,
        "近端催化优先": 82.0,
        "价格确认/动量": 70.0,
        "激进短线": 100.0,
    }
    for strategy, score in overrides.items():
        mxl["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_HIGH_SPEED_PEERS:
        return "直接同业"
    if ticker in OPTICAL_AND_COPPER_CHAIN or ticker in PLATFORM_AND_CUSTOMER_CHAIN or ticker in SEMI_SUPPLY_CHAIN:
        return "上下游"
    if ticker in ANALOG_AND_CONNECTIVITY_ADJACENT:
        return "相邻替代"
    if category in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC"}:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的Q2指引和optical ramp更直接",
            "右尾弹性优先": "A小基数叠加DSP/TIA/retimer右尾",
            "风险调整收益": "A上行足以补偿部分估值风险",
            "下行保护优先": "B反证更重且A有转正路径",
            "估值消化优先": "A高增速可部分压低远期P/S",
            "近端催化优先": "A有Q2/Q3、Rushmore/Washington验证",
            "价格确认/动量": "A近月重估仍有价格确认",
            "激进短线": "A高IV叠加光互联叙事更适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO/利润兑现更硬",
            "右尾弹性优先": "B右尾规模或份额证据更强",
            "风险调整收益": "B上行下行组合优于A",
            "下行保护优先": "B现金流/估值/压力期更稳",
            "估值消化优先": "B估值消化压力低于A",
            "近端催化优先": "B近端订单或财报催化更清楚",
            "价格确认/动量": "B价格趋势确认强于A",
            "激进短线": "B短线事件弹性或关注度更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "估值消化优先", "下行保护优先"}:
        return "成长与估值/防守互抵"
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
    a_count, b_count, _ = direction_counts(cells)
    if a_count > b_count:
        return "A"
    if b_count > a_count:
        return "B"
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
            return "MXL 的光DSP/TIA、1.6T和224G retimer小基数右尾更大。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "MXL 的Q2指引、optical data center目标和Rushmore/Washington验证更近。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "MXL 的Infrastructure收入和H2 optical ramp更能支撑未来12个月兑现。"
        return "MXL 的增长右尾和近端验证足以压过B的部分防守或估值优势。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、估值或压力期韧性明显好于高波动的 MXL。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化压力低于 MXL，MXL 已资本化较多乐观路径。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/利润兑现证据更硬。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入、份额或规模右尾更强。"
    return f"{b['ticker']} 在多数投资思路下比 MXL 更符合项目内资金配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output: list[dict[str, object]] = []
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
                "summary": base.grade_diff_summary(a, b),
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


def ttm_pe_text(fin: dict[str, object]) -> str:
    if fin.get("ttm_pe") is not None:
        return fmt_num(fin.get("ttm_pe"))
    notes = str(fin.get("notes", ""))
    return "不适用(TTM EPS为负)" if "TTM PE不适用" in notes else "缺失"


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
            x["b"]["scores"]["下行保护优先"] - a["scores"]["下行保护优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["右尾弹性优先"] - x["b"]["scores"]["右尾弹性优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:60]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:60]  # type: ignore[operator]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"] or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {ttm_pe_text(fin)}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    support = {
        "NTM兑现优先": (
            "2026Q1收入137.2M、Infrastructure 62.8M同比+136%、Q2指引160M-170M，NTM基准720M-780M",
            "backlog/RPO和客户项目金额未披露，Rushmore/Washington仍需客户认证",
        ),
        "右尾弹性优先": (
            "800G Keystone、1.6T Rushmore、Washington TIA和224G Annapurna在小收入基数上有非线性上修空间",
            "极度乐观需要多个hyperscaler/模块厂同时采用，当前仍是低可信上限",
        ),
        "风险调整收益": (
            "基准收入相对TTM约+42%-53%，乐观/极度乐观可带来明显经营杠杆和FCF转正",
            "2026-06-22 P/S 16.97、Forward PE 51.43、Call IV 112.4%，且TTM EPS为负",
        ),
        "下行保护优先": (
            "Broadband/Connectivity和Industrial仍有现金流底座，基准FCF方向转正",
            "SOXX三段压力窗口累计-74.70%，高IV和高估值使其不适合防守优先",
        ),
        "估值消化优先": (
            "若NTM收入到720M-780M并进入15%-20% non-GAAP OM，当前市值有一部分业绩消化路径",
            "当前倍数已经要求optical DC持续上修，若Q3不增长或GM低于60%会迅速反证",
        ),
        "近端催化优先": (
            "Q2实际收入/Q3指引、Infrastructure占比、2026 optical DC目标、Washington/Rushmore资格认证均在1-2季可验证",
            "缺少客户/BOM/订单金额披露时，产品demo容易被市场当作已兑现",
        ),
        "价格确认/动量": (
            "2026-06-03过去一月+18.41%，2026-06-22价格96.44美元仍高于6月3日收盘91.39美元",
            "过去两周-5.56%，5月大涨后波动高，价格确认不如持续趋势型强股",
        ),
        "激进短线": (
            "Call IV 112.4%、小市值、光DSP/TIA/1.6T/224G retimer叙事和近端财报验证具备高进攻性",
            "高IV意味着利好预期拥挤，客户认证或收入不及预期会放大回撤",
        ),
    }

    opposition_text = (
        f"{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在低估值、防守、已披露RPO/订单、"
        "更大直接AI收入规模或更稳价格趋势上压过 MXL。"
        if strong_b_rows
        else "无达到“B胜出至少5列且净胜3列”的显著强反方；MXL主要输在防守、估值和少数大型AI主线公司的兑现规模。"
    )

    out: list[str] = []
    out += [
        "# MXL 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：MXL / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 MXL vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MXL 的优势集中在右尾弹性、激进短线、近端催化和NTM兑现；核心是Q2指引、optical data center DSP/TIA收入进入表内、1.6T Rushmore/Washington TIA和224G Annapurna小基数右尾。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是Forward PE `51.43`、P/S `16.97`、Call IV `112.4%`、TTM EPS为负和SOXX压力窗口累计 `-74.70%`，因此不适合下行保护和估值消化优先。",
        "- A 最适合的投资者画像：愿意承受高IV和高估值、下注光DSP/TIA第二来源、1.6T模块BOM、224G retimer/AEC和财报指引上修的成长进攻型资金。",
        "- A 最不适合的投资者画像：优先买低波动、低估值、强现金流、客户订单/backlog已完全披露，或在SOXX压力期要求较小回撤的稳健资金。",
        f"- 多数思路下最强反方公司：{opposition_text}",
        "- 如果只追求更高增长、更好公司，A 的总体位置：MXL 是项目内高弹性光互联芯片进攻票，增长右尾靠前，但风险调整、估值消化和下行保护明显弱于成熟现金流/大型AI平台/部分同业龙头；它更像进攻仓而不是核心防守仓。",
        "- 后续最重要跟踪数据：2026Q2实际收入和Q3指引、Infrastructure收入及占比、2026 optical data center目标是否上修、non-GAAP GM是否维持60%左右、库存和prepaid assets、客户集中变化、Rushmore/Washington客户BOM、Annapurna design win、Panther商业采购与Broadcom/Marvell/Cisco/Acacia/Credo/Astera竞争进展。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", TARGET]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$720M-$780M"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "能否把800G已出货基础、1.6T Rushmore客户认证、Washington TIA attach和Annapurna 224G AEC/retimer从产品展示/评估转成NTM可确认收入。"]),
        base.row(["最大反证", "未披露可直接相加backlog/RPO；客户项目timing、1.6T认证、竞品锁定socket、库存/预付款错配和Broadband/Connectivity抵消都可能削弱兑现。"]),
        base.row(["近端催化剂", "Q2实际收入、Q3指引、Infrastructure占比、optical data center目标上修、Rushmore/Washington BOM/qualification、Annapurna design win、Panther商业采购。"]),
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
        base.row(["直接同业", "同属高速光互联DSP/TIA、retimer/AEC、serdes、网络/数据中心高速模拟或相邻BOM竞争，优先比较客户认证、socket份额、收入兑现、毛利率和同业估值。", "MRVL、AVGO、CRDO、ALAB、MTSI、SMTC", "同业证据权重最高；若一方在客户、订单、份额或利润质量上明显更硬，结论力度可上调。"]),
        base.row(["相邻替代", "同属AI半导体、连接、模拟、宽带/网络或数据中心基础设施资金篮子，但产品不直接竞争。", "QCOM、ADI、MPWR、ON、RMBS、ANET、COHR、ETN、VRT", "回答资金只能买一个时，谁的增长质量、估值消化和近端催化更好。"]),
        base.row(["上下游", "一方是MXL客户、模块/系统/云平台/服务器/晶圆制造/测试供应链，另一方是MXL所在芯片环节。", "NVDA、MSFT、AMZN、DELL、FN、TSM、ASML、KLAC、CIEN", "强调利润池和议价权，不把下游收入规模或上游瓶颈自动等同胜出。"]),
        base.row(["跨赛道", "电力、机电、工业、化工、公用事业、软件等与MXL业务差异大但可作为项目内资金配置替代。", "CEG、VST、LIN、TMO、CAT、ADBE", "默认降低结论力度；若证据互有强弱，优先中性或微倾向。"]),
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
        need = "需要 MXL 披露更明确的optical DC客户订单、Rushmore/Washington BOM、Annapurna design win、GM和FCF改善，并证明高估值可被NTM利润消化。"
        if comparison["rel"] == "直接同业":
            need = "需要 MXL 在同业中证明更强客户份额、1.6T DSP/TIA/224G出货、毛利率和可确认订单。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 MXL 用更强收入兑现和现金流改善抵消跨赛道标的的低估值或防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]
    if not strong_b_rows:
        out.append(base.row([1, "无显著强反方", "无", "按 B 胜出至少5列且净胜3列的口径，没有公司在多数思路下明显强于 MXL。", "继续跟踪MXL估值、订单、客户和毛利率；若这些弱化，低估值防守股和更大AI右尾股会成为更强反方。"]))

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬NTM订单/利润兑现、同等AI主线右尾，或明显更好的估值消化和价格确认。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要 B 把防守优势转化为更高增长或明确催化，否则难以压过MXL的光互联右尾和短线弹性。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少可用价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI计算芯片_EDA_IP_custom_ASIC/MXL_MaxLinear_公司调研_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_光DSP、TIA与CDR芯片_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_LPO_LRO线性光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AEC、DAC与高速铜缆_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_宽带接入、PON、DOCSIS 4.0与Wi-Fi 7_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_mxl_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+42%-53%` 做同号区间修正后建档；未读取下游量化目录、备份、临时目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 MXL 正式评估文件")
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
                "mxl_tiers": companies[TARGET]["tiers"],
                "mxl_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
                "mxl_ranks": companies[TARGET]["ranks"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
