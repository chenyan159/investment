from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_etn_company_comparison as etn_calibration


TARGET = "ICHR"
TARGET_NAME = "Ichor Holdings"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ICHR_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_SUBSYSTEM_PEERS = {"AEIS", "MKSI", "UCTT"}
WFE_OEMS_AND_CLOSE_EQUIPMENT = {
    "ACLS",
    "ACMR",
    "AMAT",
    "ASMIY",
    "ASML",
    "DSCSY",
    "KLAC",
    "LRCX",
    "NVMI",
    "TOELY",
    "VECO",
}
FOUNDRY_MEMORY_OSAT = {
    "AMKR",
    "ASX",
    "GFS",
    "IMOS",
    "INTC",
    "MU",
    "SNDK",
    "STX",
    "TSEM",
    "TSM",
    "UMC",
    "WDC",
}
AI_COMPUTE_AND_CLOUD_DEMAND = {
    "ADBE",
    "ALAB",
    "AMD",
    "AMZN",
    "ANET",
    "ARM",
    "AVGO",
    "BABA",
    "CDNS",
    "CIEN",
    "COHR",
    "CRDO",
    "CRWD",
    "CRWV",
    "DELL",
    "FN",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "META",
    "MRVL",
    "MSFT",
    "NBIS",
    "NVDA",
    "NTNX",
    "ORCL",
    "QCOM",
    "RMBS",
    "SMCI",
    "SNPS",
}
SEMI_MATERIAL_TEST_ADJACENT = {
    "AJNMY",
    "AMKR",
    "ASGLY",
    "ASMVY",
    "ATEYY",
    "AXTI",
    "BESIY",
    "CAMT",
    "COHU",
    "ENTG",
    "FORM",
    "HOCPY",
    "KEYS",
    "KLIC",
    "MICLF",
    "MTRN",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
    "TER",
}

ICHR_SCORES = {
    "NTM兑现优先": 74.0,
    "右尾弹性优先": 78.0,
    "风险调整收益": 43.0,
    "下行保护优先": 39.0,
    "估值消化优先": 61.0,
    "近端催化优先": 66.0,
    "价格确认/动量": 82.0,
    "激进短线": 93.0,
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


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
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
        fin = company.get("fin", {})
        if not fin or not fin.get("price"):
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"
                company.setdefault("ranks", {})[strategy] = None


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    fix_growth_ranges(companies)

    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    floors: dict[str, dict[str, float]] = {}
    floors.update(getattr(calibrated, "SCORE_FLOORS", {}))
    floors.update(getattr(etn_calibration, "LOCAL_SCORE_FLOORS", {}))
    floors["ETN"] = getattr(etn_calibration, "ETN_SCORES", {})
    for ticker, strategy_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in strategy_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    for strategy, score in ICHR_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_SUBSYSTEM_PEERS:
        return "直接同业"
    if ticker in WFE_OEMS_AND_CLOSE_EQUIPMENT or ticker in FOUNDRY_MEMORY_OSAT or ticker in AI_COMPUTE_AND_CLOUD_DEMAND:
        return "上下游"
    if ticker in SEMI_MATERIAL_TEST_ADJACENT:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict[str, object], rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "证据互有强弱且档位接近"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "ICHR有Q2指引和WFE修复收入锚",
            "右尾弹性优先": "ICHR小盘WFE子系统利润弹性更大",
            "风险调整收益": "ICHR上行能覆盖部分高IV反证",
            "下行保护优先": "ICHR估值或业务反证相对更轻",
            "估值消化优先": "ICHR收入修复可部分消化估值",
            "近端催化优先": "ICHR有Q2/Q3和GM现金流验证",
            "价格确认/动量": "ICHR六月价格确认更强",
            "激进短线": "ICHR高IV与WFE/HBM beta更强",
        }[strategy]

    if ticker in DIRECT_SUBSYSTEM_PEERS or rel == "直接同业":
        return {
            "NTM兑现优先": "B同业订单或客户结构更硬",
            "右尾弹性优先": "B同业产品/利润右尾更大",
            "风险调整收益": "B同业现金流和估值组合更好",
            "下行保护优先": "B同业现金流或回撤缓冲更强",
            "估值消化优先": "B同业估值消化压力更低",
            "近端催化优先": "B同业订单或毛利节点更近",
            "价格确认/动量": "B同业价格确认更强",
            "激进短线": "B同业短线弹性更高",
        }[strategy]
    if category in HIGH_GROWTH_CATS or ticker in AI_COMPUTE_AND_CLOUD_DEMAND:
        return {
            "NTM兑现优先": "B直接AI收入/RPO更短链",
            "右尾弹性优先": "B直接AI右尾或小基数更大",
            "风险调整收益": "B上行质量更能覆盖风险",
            "下行保护优先": "B现金流或需求能见度更强",
            "估值消化优先": "B增长更能消化估值",
            "近端催化优先": "B产品/订单催化更密集",
            "价格确认/动量": "B价格和资金确认更强",
            "激进短线": "B高beta叙事更适合进攻",
        }[strategy]
    if category in INFRA_CATS:
        return {
            "NTM兑现优先": "B订单/backlog兑现更清楚",
            "右尾弹性优先": "B AI电力/机电右尾更直接",
            "风险调整收益": "B订单与估值组合更优",
            "下行保护优先": "B现金流或防御属性更强",
            "估值消化优先": "B backlog兑现更能覆盖估值",
            "近端催化优先": "B项目/FID/产能催化更近",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B事件弹性和关注度更高",
        }[strategy]
    if rel == "上下游":
        return {
            "NTM兑现优先": "B收入/订单兑现链条更硬",
            "右尾弹性优先": "B利润池位置和右尾更优",
            "风险调整收益": "B增长质量和下行组合更好",
            "下行保护优先": "B规模/现金流缓冲更强",
            "估值消化优先": "B盈利兑现更能消化估值",
            "近端催化优先": "B客户/产品节点更明确",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B短线资金偏好更强",
        }[strategy]
    return {
        "NTM兑现优先": "B收入兑现证据更强",
        "右尾弹性优先": "B右尾空间更大",
        "风险调整收益": "B风险收益组合更优",
        "下行保护优先": "B下行缓冲更强",
        "估值消化优先": "B增长更能消化估值",
        "近端催化优先": "B近端催化更明确",
        "价格确认/动量": "B价格确认更强",
        "激进短线": "B短线弹性更强",
    }[strategy]


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = str(a["tiers"][strategy])  # type: ignore[index]
    bt = str(b["tiers"][strategy])  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    score_diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
    tier_diff = tier_value(at) - tier_value(bt)
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
    quality_weight = (
        float(a["scores"]["NTM兑现优先"]) * 0.9
        + float(a["scores"]["风险调整收益"]) * 0.9
        + float(a["scores"]["估值消化优先"]) * 0.7
        + float(a["scores"]["近端催化优先"]) * 0.5
        - float(b["scores"]["NTM兑现优先"]) * 0.9
        - float(b["scores"]["风险调整收益"]) * 0.9
        - float(b["scores"]["估值消化优先"]) * 0.7
        - float(b["scores"]["近端催化优先"]) * 0.5
    )
    return "A" if quality_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if float(a["scores"]["价格确认/动量"]) - float(b["scores"]["价格确认/动量"]) > 12:
            return "ICHR近期价格确认强，WFE/HBM修复已被资金验证，B的价格证据不足。"
        if float(a["scores"]["激进短线"]) - float(b["scores"]["激进短线"]) > 12:
            return "ICHR高IV、小盘WFE子系统和Q2/Q3验证窗口更适合进攻。"
        if float(a["scores"]["NTM兑现优先"]) - float(b["scores"]["NTM兑现优先"]) > 10:
            return "ICHR的Q2收入指引、WFE修复和gas/chemical delivery收入锚更清楚。"
        return "ICHR在WFE修复、价格确认或短线弹性上略胜，B的证据不足以覆盖反证。"

    if float(b["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"]) > 12:
        return f"{b['ticker']}的估值、现金流或下行风险组合明显优于ICHR。"
    if float(b["scores"]["下行保护优先"]) - float(a["scores"]["下行保护优先"]) > 14:
        return f"{b['ticker']}的现金流、防御属性或压力期表现强于ICHR。"
    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 14:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于ICHR。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 12:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比ICHR更硬。"
    return f"{b['ticker']}在多数投资思路下比ICHR更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
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
    rows: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        a_count, b_count, neutral = direction_counts(cells)
        final = final_choice(a, b, cells)
        rows.append(
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
    rel_order = {"直接同业": 0, "上下游": 1, "相邻替代": 2, "跨赛道": 3}
    return sorted(rows, key=lambda item: (rel_order.get(str(item["rel"]), 9), str(item["ticker"])))


def fmt_num(value: object, precision: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{precision}f}"
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
        return f"{float(value):.2f}%"
    except Exception:
        return "缺失"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = sorted(str(company["date"]) for company in companies.values())
    date_range = f"{company_dates[0]} 至 {company_dates[-1]}"

    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]

    strong_b = sorted(
        comparisons,
        key=lambda row: (
            int(row["bc"]) - int(row["ac"]),
            float(row["b"]["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"]),  # type: ignore[index]
            float(row["b"]["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda row: (
            int(row["ac"]) - int(row["bc"]),
            float(a["scores"]["价格确认/动量"]) - float(row["b"]["scores"]["价格确认/动量"]),  # type: ignore[index]
            float(a["scores"]["激进短线"]) - float(row["b"]["scores"]["激进短线"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_b_rows = [row for row in strong_b if int(row["bc"]) >= 5 and int(row["bc"]) - int(row["ac"]) >= 3][:45]
    strong_a_rows = [row for row in strong_a if int(row["ac"]) >= 5 and int(row["ac"]) - int(row["bc"]) >= 3][:45]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker].get("fin", {}).get("price")  # type: ignore[union-attr]
    ]

    final_a = sum(1 for row in comparisons if row["final"] == "A")
    final_b = sum(1 for row in comparisons if row["final"] == "B")
    final_neutral = len(comparisons) - final_a - final_b

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    price = fin.get("price")
    close_0603 = mom2.get("latest_close")
    post_interval = "缺失"
    if price is not None and close_0603:
        post_interval = fmt_pct((float(price) / float(close_0603) - 1) * 100)
    daily_snapshot = (
        f"2026-06-22收盘价 `{fmt_num(fin.get('price'))}`，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `不适用/TTM EPS为负`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"P/S `{fmt_num(fin.get('ps'))}`，P/B `{fmt_num(fin.get('pb'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`，Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03过去两周 `{fmt_pct(mom2.get('mom2w'))}`，过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04三段SOXX压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`；"
        f"从2026-06-03收盘到2026-06-22收盘约 `{post_interval}`。"
    )

    product_names = []
    for product in a["products"]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])
        if len(product_names) >= 7:
            break

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {
        strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]
        for strategy in STRATS
    }

    support = {
        "NTM兑现优先": (
            "2026Q1收入`2.56068亿美元`、Q2官方指引`2.90-3.10亿美元`，NTM基准收入`12.5-13.5亿美元`，较TTM约`+30%-41%`",
            "不披露backlog/bookings/RPO和产品线收入，Q2以后需要Q3指引、客户订单和库存转收入验证",
        ),
        "右尾弹性优先": (
            "gas delivery、chemical delivery、advanced packaging/HBM、3D DRAM/GAA工具复杂度和Ichor-branded content带来小盘利润弹性",
            "极度乐观`17.0-19.0亿美元`缺少客户锁单、产品线订单和proprietary product量产证据",
        ),
        "风险调整收益": (
            "若毛利率从12.8%修复到15%-16%并且FCF转正，利润弹性会明显大于收入弹性",
            "2026-06-22 Forward PE`38.12`、EV/EBITDA`129.00`、Call IV`91.0%`，TTM EPS为负且Q1 FCF约`-998万美元`",
        ),
        "下行保护优先": (
            "WFE修复有Q2指引支撑，客户工具平台design-in能提供一定粘性",
            "三段SOXX压力窗口累计`-110.87%`、高IV、客户集中、低毛利BOM pass-through和库存占用使下行保护弱",
        ),
        "估值消化优先": (
            "基准收入`12.5-13.5亿美元`、基准EBITDA`1.05-1.40亿美元`，若Q3/Q4顺季增长可开始消化估值",
            "当前价格已从6月初快速抬升，Forward PE仍高，收入达标但GM不升会使估值消化失败",
        ),
        "近端催化优先": (
            "Q2实际收入、Q3指引、non-GAAP GM进入13%-14%并向14.5%-15%推进、库存转收入和OCF转正都在1-2季可验证",
            "缺少正式订单/backlog和产品线量产收入披露，催化更多是验证式而非确定订单式",
        ),
        "价格确认/动量": (
            "2026-06-03两周`+10.17%`、一月`+12.47%`，2026-06-22收盘`99.61`较2026-06-03收盘约`+37.49%`",
            "高IV和快速涨幅意味着价格确认可能已透支一部分Q2/Q3改善",
        ),
        "激进短线": (
            "小市值、Call IV`91.0%`、WFE/HBM/advanced packaging上修和Q2/Q3验证窗口提供短线进攻性",
            "高波动、现金流反证和无backlog披露使短线交易必须承受财报落空回撤",
        ),
    }

    lines: list[str] = []
    lines += [
        "# ICHR 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：ICHR / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV为2026-06-22；两周/一月区间涨跌为2026-06-03；SOXX压力窗口为2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 ICHR vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；ICHR 的 AI/HBM 传导只按 WFE OEM 工具订单、gas/chemical delivery 收入和毛利率修复路径处理，不把云厂CapEx或AI数据中心BOM直接并入公司收入。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ICHR 的优势集中在小盘WFE子系统beta、6月价格确认、高IV进攻性、Q2收入指引和毛利率修复验证窗口。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是不披露backlog/bookings/RPO和产品线收入，Q1 FCF为负，SOXX压力窗口回撤大，且当前Forward PE/EV-EBITDA和IV都不低。",
        "- A 最适合的投资者画像：愿意用高波动押注WFE/HBM/advanced packaging上游订单修复、Q2/Q3指引延续和毛利率经营杠杆的进攻型资金。",
        "- A 最不适合的投资者画像：要求订单/RPO硬证据、现金流防守、低回撤、低IV或直接AI收入确认的稳健资金；这类资金通常更偏向NVDA/AVGO/MU/ASML/ETN/VRT/CEG/TSM等。",
        f"- 多数思路下最强反方公司：{'、'.join([str(row['ticker']) for row in strong_b_rows[:10]])}。这些公司通常在直接AI收入、订单/RPO/backlog、平台右尾、现金流、防守属性或估值消化上强于ICHR。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：ICHR 是项目内偏进攻的WFE子系统修复标的，最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它更适合价格/动量和激进短线列，不适合下行保护和风险调整收益列。",
        "- 后续最重要跟踪数据：Ichor Q2实际收入、Q3指引、non-GAAP GM是否进入13%-14%并继续上行、OCF/FCF是否转正、inventory turns/DSO、客户Lam/Applied/TEL在etch/deposition、memory/HBM和advanced packaging上的订单评论、是否披露backlog替代线索、proprietary product量产收入和Ichor-branded content占比。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ICHR"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "12.5-13.5 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "不披露backlog/bookings/book-to-bill和产品线收入；Q2以后必须用Q3指引、客户WFE订单、毛利率和库存转收入验证。"]),
        base.row(["最大反证", "Q1 operating cash flow为-290万美元、FCF约-998万美元且库存增加；若GM停在13%附近或收入来自低毛利BOM pass-through，经营价值传导会被下修。"]),
        base.row(["近端催化剂", "Q2实际收入、Q3指引、non-GAAP GM、OCF/FCF、库存周转、Lam/Applied/TEL订单评论、gas panel pull-in、proprietary product和Ichor-branded content线索。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        lines.append(base.row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "同属半导体设备子系统、关键电源/RF/真空/流体/精密制造供应商；优先比较客户份额、订单/交付、毛利率、现金流、组件自有度和同业估值。", "UCTT、MKSI、AEIS", "判断力度最高；若对手订单、现金流或组件利润质量明显更强，可直接压过ICHR的价格动量。"]),
        base.row(["上下游", "WFE设备OEM、晶圆厂/存储/封测客户、AI芯片和云厂是ICHR需求链；比较时区分客户收入规模、WFE订单转化、利润池位置和ICHR可捕获份额。", "AMAT、LRCX、ASML、TOELY、TSM、MU、NVDA、MSFT", "不把下游AI收入直接等同ICHR收入；若对方拥有更硬订单/RPO或更高利润池，可在NTM、右尾和风险收益列胜出。"]),
        base.row(["相邻替代", "同属半导体制造材料、封测、检测计量或周边设备资金篮子，但产品/客户模式不完全重叠；比较增长质量、估值消化和催化。", "ENTG、ATEYY、TER、CAMT、FORM、COHU、SHECY", "中等力度；赛道更热不能自动胜出，必须落实到收入兑现、利润率、现金流和估值。"]),
        base.row(["跨赛道", "电力、冷却、工程、工业、软件等与ICHR业务差异大，但作为项目内资金替代仍比较风险调整收益、估值消化、下行保护和近端催化。", "ETN、VRT、CEG、GEV、PWR、TMO、ADBE", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
                    base.category_short(str(b["category"])),  # type: ignore[index]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(int(comparison["ac"]), int(comparison["bc"]), int(comparison["nc"])),
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
        lines.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要ICHR披露更硬订单/backlog替代指标、Q3/Q4连续上修、GM进入15%-16%且OCF/FCF转正。"
        if comparison["rel"] == "跨赛道":
            need = "需要ICHR证明WFE子系统弹性足以覆盖跨赛道标的的现金流、订单或防守优势。"
        if "右尾弹性优先" in wins:
            need = "需要ICHR把HBM/advanced packaging叙事转成可量化订单、收入和proprietary product量产。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高近端收入确认、价格确认或短线催化强度，并证明估值和现金流反证可控。"
        if float(b["scores"]["风险调整收益"]) > float(a["scores"]["风险调整收益"]):  # type: ignore[index]
            need = "需要B把风险收益优势转化为更强价格确认或更明确近端催化。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    target = companies[TARGET]
    print(
        json.dumps(
            {
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "ichr_scores": {strategy: round(target.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "ichr_tiers": {strategy: target.get("tiers", {}).get(strategy) for strategy in STRATS},
                "ichr_ranks": {strategy: target.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
