from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base

try:
    import generate_ceg_company_comparison as floor_source
except Exception:  # pragma: no cover - only used if helper is later removed.
    floor_source = None


TARGET = "DIOD"
TARGET_NAME = "Diodes Incorporated"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "DIOD_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS
SCORE_FLOORS = getattr(floor_source, "SCORE_FLOORS", {}) if floor_source else {}


DIRECT_ANALOG_POWER_PEERS = {
    "ADI",
    "AOSL",
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
    "VSH",
    "WOLF",
}

TIMING_CONNECTIVITY_ADJACENT = {
    "ALAB",
    "CRDO",
    "MTSI",
    "MXL",
    "RMBS",
    "SITM",
    "SMTC",
}

AI_SERVER_NETWORK_DOWNSTREAM = {
    "AAOI",
    "ANET",
    "APH",
    "AVGO",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CSCO",
    "DELL",
    "FN",
    "FLEX",
    "GLW",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "MRVL",
    "NVDA",
    "PENG",
    "POET",
    "SANM",
    "SMCI",
    "TEL",
    "VIAV",
}

AI_LOAD_OR_CUSTOMERS = {
    "AMZN",
    "APLD",
    "BABA",
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

POWER_INFRA_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "BE",
    "ETN",
    "GEV",
    "HUBB",
    "NVT",
    "POWL",
    "VRT",
}

SEMI_MANUFACTURING_CHAIN = {
    "ACLS",
    "ACMR",
    "AMAT",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "DSCSY",
    "FORM",
    "GFS",
    "ICHR",
    "IMOS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MKSI",
    "NVMI",
    "ONTO",
    "TER",
    "TOELY",
    "TSM",
    "TSEM",
    "UCTT",
    "UMC",
    "VECO",
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


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

    values: list[float] = []
    for match in re.finditer(r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text):
        values.append((-1 if match.group(1) == "-" else 1) * float(match.group(2)))
    return sum(values) / len(values) if values else None


def fix_growth_ranges(companies: dict[str, dict[str, object]]) -> None:
    for company in companies.values():
        scenarios = company.get("scenarios", {})
        if not isinstance(scenarios, dict):
            continue
        for scenario, field in [
            ("bear", "bear_growth"),
            ("base", "base_growth"),
            ("bull", "bull_growth"),
            ("extreme", "extreme_growth"),
        ]:
            record = scenarios.get(scenario, {})
            if not isinstance(record, dict):
                continue
            for key, value in record.items():
                if "增速" in str(key) or "绝对" in str(key):
                    parsed = mid_growth(value)
                    if parsed is not None:
                        company[field] = parsed
                    break


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1]["scores"][strategy],  # type: ignore[index]
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
        if not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"  # type: ignore[index]
                company.setdefault("ranks", {})[strategy] = None  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    fix_growth_ranges(companies)
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[union-attr]
            company["scores"][strategy] = max(current, floor)  # type: ignore[index]

    # DIOD calibration from its formal assessment and daily data:
    # clear Q1/Q2 recovery, net cash and AI-adjacent timing/power sockets, but
    # no backlog/bookings/AI revenue disclosure and weak pressure-window drawdown.
    overrides = {
        "NTM兑现优先": 74.0,
        "右尾弹性优先": 80.0,
        "风险调整收益": 56.0,
        "下行保护优先": 64.0,
        "估值消化优先": 70.0,
        "近端催化优先": 68.0,
        "价格确认/动量": 74.0,
        "激进短线": 86.0,
    }
    for strategy, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_ANALOG_POWER_PEERS:
        return "直接同业"
    if ticker in TIMING_CONNECTIVITY_ADJACENT or ticker in POWER_INFRA_ADJACENT:
        return "相邻替代"
    if ticker in AI_SERVER_NETWORK_DOWNSTREAM or ticker in AI_LOAD_OR_CUSTOMERS:
        return "上下游"
    if ticker in SEMI_MANUFACTURING_CHAIN:
        return "上下游"
    if category in {"配电_电源_功率器件", "AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "晶圆制造_前道设备", "封测_检测_计量_光罩", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, winner: str, company: dict[str, object], _diff: float) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if winner == "A":
        return {
            "NTM兑现优先": "A有Q2指引、POS和库存改善锚",
            "右尾弹性优先": "A小芯片AI socket仍有放大空间",
            "风险调整收益": "A净现金和估值增速组合较均衡",
            "下行保护优先": "A净现金和正FCF提供底盘",
            "估值消化优先": "A约25x远期PE可由恢复消化",
            "近端催化优先": "A有Q2/Q3指引与PCIe7验证",
            "价格确认/动量": "A近两周价格已明显确认",
            "激进短线": "A高IV叠加AI电源/时钟叙事",
        }[strategy]

    if winner == "B":
        if ticker in DIRECT_ANALOG_POWER_PEERS:
            return {
                "NTM兑现优先": "B同业订单或收入锚更硬",
                "右尾弹性优先": "B同业AI电源或模拟右尾更大",
                "风险调整收益": "B同业赔率或质量更优",
                "下行保护优先": "B同业现金流或波动更安全",
                "估值消化优先": "B同业业绩更能消化估值",
                "近端催化优先": "B同业产品/客户催化更明确",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线弹性更高",
            }[strategy]
        if ticker in AI_SERVER_NETWORK_DOWNSTREAM or category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链订单兑现更直接",
                "右尾弹性优先": "B核心AI利润池右尾更大",
                "风险调整收益": "B上行更能覆盖执行风险",
                "下行保护优先": "B需求能见度或质量更强",
                "估值消化优先": "B高增长更能消化估值",
                "近端催化优先": "B订单/产品催化更密集",
                "价格确认/动量": "B价格趋势和资金偏好更强",
                "激进短线": "B高beta更适合短线进攻",
            }[strategy]
        if ticker in POWER_INFRA_ADJACENT or category in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单/交付路径更清楚",
                "右尾弹性优先": "B电气化或电力右尾更直接",
                "风险调整收益": "B增长估值组合更优",
                "下行保护优先": "B订单粘性或资产质量更稳",
                "估值消化优先": "B业绩兑现更能覆盖倍数",
                "近端催化优先": "B订单或产能催化更近",
                "价格确认/动量": "B价格确认更强",
                "激进短线": "B主题beta更高",
            }[strategy]
        if ticker in SEMI_MANUFACTURING_CHAIN or category in {"晶圆制造_前道设备", "封测_检测_计量_光罩"}:
            return {
                "NTM兑现优先": "B设备/制造兑现证据更硬",
                "右尾弹性优先": "B半导体周期右尾更大",
                "风险调整收益": "B利润池或护城河更好",
                "下行保护优先": "B规模质量或现金流更稳",
                "估值消化优先": "B景气兑现更能消化估值",
                "近端催化优先": "B订单/制程节点更明确",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B半导体beta更适合进攻",
            }[strategy]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景上行更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B现金流或估值缓冲更好",
            "估值消化优先": "B当前估值更易消化",
            "近端催化优先": "B近端催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线关注度更高",
        }[strategy]

    if strategy in {"价格确认/动量", "激进短线"}:
        return "动量或短线证据差距有限"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "估值安全边际互有强弱"
    return "档位接近需继续验证"


def label_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a["tiers"].get(strategy, "资料不足")  # type: ignore[union-attr]
    bt = b["tiers"].get(strategy, "资料不足")  # type: ignore[union-attr]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
    tier_gap = tier_value(str(at)) - tier_value(str(bt))
    abs_diff = abs(float(diff))
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 28, 14, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 21, 9, 4

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


def cell_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strategy, winner, b, float(diff))}"


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
    weights = {
        "NTM兑现优先": 1.15,
        "右尾弹性优先": 1.00,
        "风险调整收益": 1.10,
        "下行保护优先": 0.75,
        "估值消化优先": 1.00,
        "近端催化优先": 0.85,
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
    for strategy, cell in zip(STRATS, cells):
        score += weights[strategy] * label_score.get(base.tag_in_cell(cell) or "中性", 0.0)
    if score > 0.05:
        return "A"
    if score < -0.05:
        return "B"
    quality_a = a["scores"]["NTM兑现优先"] + a["scores"]["风险调整收益"] + a["scores"]["估值消化优先"]  # type: ignore[index,operator]
    quality_b = b["scores"]["NTM兑现优先"] + b["scores"]["风险调整收益"] + b["scores"]["估值消化优先"]  # type: ignore[index,operator]
    return "A" if quality_a >= quality_b else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    diffs = {strategy: a["scores"][strategy] - b["scores"][strategy] for strategy in STRATS}  # type: ignore[index,operator]
    ticker = str(b["ticker"])
    category = str(b["category"])
    if final == "A":
        if diffs["NTM兑现优先"] > 10:
            return "DIOD的Q2指引、POS改善和汽车/工业恢复让NTM兑现更清楚。"
        if diffs["估值消化优先"] > 8:
            return "DIOD的P/S、远期PE和收入恢复路径比对手更容易消化。"
        if diffs["近端催化优先"] > 8:
            return "DIOD有Q2/Q3收入、毛利率、PCIe7和AI socket验证节点。"
        if diffs["价格确认/动量"] > 10:
            return "DIOD近两周价格确认更强，市场已开始交易恢复和AI-adjacent弹性。"
        return "DIOD在收入恢复、净现金和估值消化之间更均衡，对手证据不足以压过。"

    if diffs["右尾弹性优先"] < -14 and category in HIGH_GROWTH_CATS:
        return f"{ticker}的核心AI收入、订单或小基数右尾明显强于DIOD的小芯片socket。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比DIOD更硬。"
    if diffs["风险调整收益"] < -10:
        return f"{ticker}的增长、估值和下行组合优于DIOD。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、防御性或压力期表现明显优于DIOD。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker}的价格确认和资金偏好强于DIOD。"
    return f"{ticker}在多数投资思路下比DIOD更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        av = tier_value(a["tiers"].get(strategy))  # type: ignore[union-attr]
        bv = tier_value(b["tiers"].get(strategy))  # type: ignore[union-attr]
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

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(output, key=lambda item: (rel_order.get(str(item["rel"]), 9), str(item["ticker"])))


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


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):+.2f}%"
    except Exception:
        return "缺失"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def top_majority(comparisons: list[dict[str, object]], final: str, limit: int = 45) -> list[dict[str, object]]:
    rows = [row_obj for row_obj in comparisons if row_obj["final"] == final]
    if final == "B":
        rows.sort(key=lambda row_obj: (row_obj["bc"] - row_obj["ac"], row_obj["bc"], -row_obj["nc"]), reverse=True)  # type: ignore[operator]
    else:
        rows.sort(key=lambda row_obj: (row_obj["ac"] - row_obj["bc"], row_obj["ac"], -row_obj["nc"]), reverse=True)  # type: ignore[operator]
    return rows[:limit]


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"

    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy])[:3]
    strong_b_rows = top_majority(comparisons, "B")
    strong_a_rows = top_majority(comparisons, "A")
    final_a = sum(1 for comparison in comparisons if comparison["final"] == "A")
    final_b = sum(1 for comparison in comparisons if comparison["final"] == "B")
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"] or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_num(fin.get('call_iv'), 1)}%，Put IV {fmt_num(fin.get('put_iv'), 1)}%；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )
    product_names = [str(product[0]).split("：")[0].split("；")[0] for product in a["products"][:7]]  # type: ignore[index]
    rank_text = {strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档" for strategy in STRATS}  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]

    support = {
        "NTM兑现优先": (
            "2026Q1收入同比+22.1%、Q2指引中位数4.35亿美元且同比+18.8%，POS改善、渠道库存降至正常低端，NTM基准收入18.0-19.5亿美元",
            "公司不披露backlog、bookings、book-to-bill、客户级AI收入，NTM证据强于普通周期件但弱于订单/RPO硬锚公司",
        ),
        "右尾弹性优先": (
            "AI data-center socket overlay基准2.5-3.6亿美元、乐观4.2-6.0亿美元，PCIe timing、redriver、power/protection可随AI服务器和网络放量",
            "DIOD不是GPU/HBM/CPO/retimer主链，单颗ASP低，极度乐观需平台AVL、价格、份额和产能同时成立",
        ),
        "风险调整收益": (
            "P/S 3.63、Forward PE 24.60、净现金、正FCF和基准收入+16%-25%形成中等偏好的赔率",
            "TTM PE 66.36、Call IV 81.5%、SOXX压力窗口累计-70.87%，高波动和压力期回撤削弱风险调整收益",
        ),
        "下行保护优先": (
            "截至2026Q1现金+短投约4.087亿美元、总债务约0.55亿美元，Q1经营现金流和FCF为正，汽车/工业认证客户提供底盘",
            "库存仍高、毛利率只有31.8%、高IV和SOXX压力窗口大回撤说明它不是防守型资产",
        ),
        "估值消化优先": (
            "基准NTM收入18.0-19.5亿美元、EBITDA 2.4-3.1亿美元、净利润1.0-1.5亿美元，可支撑约25x Forward PE逐步消化",
            "若毛利率不能上穿33%-34%、库存天数不降或AI socket不能量化，估值消化会停留在周期修复层面",
        ),
        "近端催化优先": (
            "Q2/Q3收入和毛利率、computing/communications占比、汽车/工业恢复、PCIe 7 clock、AI server/networking/power设计线索可在1-2季验证",
            "缺少大客户、订单金额、backlog或AI revenue量化，催化强度弱于已有订单/RPO或产能放量的AI主链公司",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+19.63%、过去一月+7.37%，2026-06-22收盘价122.76高于6月初116.22，价格已确认复苏交易",
            "涨幅不如AI服务器、光互联、存储、NeoCloud和电力高beta，后续需要Q2/Q3业绩继续确认",
        ),
        "激进短线": (
            "Call IV 81.5%、AI电源/保护/timing叙事、PCIe 7新品和小市值半导体属性给出事件弹性",
            "短线爆发力受非核心AI主链、低/中ASP、无订单披露和压力窗口回撤限制",
        ),
    }

    out: list[str] = [
        "# DIOD 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：DIOD / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 DIOD vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。DIOD 的优势来自Q2指引、POS/渠道库存改善、汽车/工业恢复、净现金、PCIe timing和AI power/protection小芯片socket，以及近期价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是没有backlog/bookings/AI revenue披露，AI收入只是AI-adjacent而非主链，SOXX压力窗口累计-70.87%、Call IV 81.5%，下行保护和激进短线都不算全项目强项。",
        "- A 最适合的投资者画像：希望买半导体周期修复叠加AI服务器电源/保护/时钟边缘受益，同时不想支付纯AI芯片、光互联或NeoCloud极端高倍数的中高风险配置资金。",
        "- A 最不适合的投资者画像：只追求最高增长、最大右尾、订单/RPO硬锚、低波动防守，或要求短期爆发力强于AI主链高beta标的的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(row_obj['ticker']) for row_obj in strong_b_rows[:12]])}。这些公司通常拥有更直接AI收入、订单/RPO/backlog、核心利润池、估值消化或更强价格动量。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：DIOD 是项目内中游偏上的AI-adjacent模拟/分立/时钟标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家。它强于大量缺订单、缺现金流或高反证公司，但面对AI计算、存储、光互联、电气设备和部分强现金流平台时通常落后。",
        "- 后续最重要跟踪数据：2026Q2/Q3收入和毛利率、computing+communications占比、汽车+工业占比、渠道库存周数和POS、库存天数、管理层是否量化AI/data-center revenue、PCIe 7 clock平台/客户线索、AI PSU/BBU/48V/800V power protection design win、capex和FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "DIOD"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "18.0-19.5 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "DIOD不披露backlog、bookings、book-to-bill、客户级订单或AI data-center revenue；AI需求只能通过Q2指引、POS、渠道库存、终端mix和design-win线索折扣校准。"]),
        base.row(["最大反证", "毛利率仍在31.8%左右、库存天数157天仍高，AI socket多为低/中ASP小芯片且高端retimer/核心power模块利润可能由竞品捕获。"]),
        base.row(["近端催化剂", "Q2/Q3收入和毛利率、computing+communications占比、汽车/工业恢复、PCIe 7.0 clock generator平台线索、AI server/networking/optical/power supply设计赢和库存天数下降。"]),
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
        base.row(["直接同业", "与DIOD在analog、power management、discrete、protection、timing、MCU/混合信号或功率器件需求池高度重叠，优先比较收入兑现、毛利率、客户认证、产品代际、库存和估值。", "ADI、TXN、MCHP、ON、STM、IFNNY、MPWR、LFUS、VSH、POWI", "同业证据权重最高；若对手在AI电源、车规/工业、timing或利润质量上明显胜出，可给建议或强烈建议。"]),
        base.row(["相邻替代", "同属AI电源、时钟/连接、配电、电气化、光互联或半导体边缘小芯片配置篮子，但产品不完全竞争。", "ALAB、SITM、CRDO、MTSI、VRT、ETN、POWL、HUBB、BE", "重点回答资金只能买一个时，谁的增长质量、利润捕获、估值消化和近端催化更好。"]),
        base.row(["上下游", "B 是DIOD产品进入的AI服务器、网络、光模块、云/IDC、晶圆制造、前道设备或封测链条；下游收入规模不自动等同DIOD收入。", "NVDA、AVGO、MRVL、ANET、DELL、SMCI、MSFT、TSM、ASML、AMAT、TER", "区分系统/芯片/设备利润池与DIOD低中ASP socket；核心看议价权、订单硬度和收入确认链条。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "材料、化学品、公用事业、工业、软件和航天类公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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

    out += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要DIOD披露AI/data-center收入、客户、订单金额、backlog或book-to-bill，并证明毛利率和FCF随收入同步上行。"
        if comparison["rel"] == "直接同业":
            need = "需要DIOD在同业中证明timing/power/protection的份额、毛利率、客户认证和收入兑现强于B。"
        elif comparison["rel"] == "上下游":
            need = "需要DIOD证明自己能从下游AI系统/芯片/设备利润池中捕获可观收入，而非只获得低ASP边缘器件。"
        elif "右尾弹性优先" in wins or "激进短线" in wins:
            need = "需要DIOD把PCIe7、AI power/protection和800V/48V机会转成客户/订单/收入，而不是只停留在产品映射。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B拿出更硬的NTM收入/利润兑现、现金流质量、估值消化或明确订单/客户证据。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入和利润，并降低估值、现金流或执行反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/配电_电源_功率器件/DIOD_Diodes_Incorporated_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`；`行业调研/AI服务器_存储_芯片/行业调研_精密时钟与同步芯片_2026-06-10.md`；`行业调研/AI网络_光互联_铜互联/行业调研_PCIe_CXL高速IO交换与Retimer_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_diod_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对DIOD的Q2指引、POS/库存、PCIe timing、AI power/protection、净现金、估值、SOXX压力窗口和缺少订单/AI收入披露做人工校准后建档；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = "ALLE"
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 DIOD 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "diod_tiers": {strategy: companies[TARGET]["tiers"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
                "diod_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},  # type: ignore[index]
                "diod_ranks": {strategy: companies[TARGET]["ranks"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
