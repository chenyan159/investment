from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "BWXT"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "BWXT_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_NUCLEAR = {"RYCEY"}
NUCLEAR_AND_POWER_ADJACENT = {
    "BE",
    "FCEL",
    "GEV",
    "GNRC",
    "HTHIY",
    "OKLO",
    "PSIX",
    "SMR",
    "CMI",
    "ENS",
    "ENPH",
    "FLNC",
    "AMPX",
}
UTILITY_OR_ENERGY_CHAIN = {"AEP", "CEG", "DTE", "ET", "ETR", "VST"}
ENGINEERING_AND_GRID = {
    "PWR",
    "EME",
    "FIX",
    "MYRG",
    "IESC",
    "ETN",
    "POWL",
    "HUBB",
    "NVT",
    "ABBNY",
    "VRT",
    "TT",
    "AAON",
    "CARR",
    "JCI",
    "MOD",
    "DOV",
}
DOWNSTREAM_POWER_BUYERS = {
    "AMZN",
    "MSFT",
    "GOOGL",
    "META",
    "ORCL",
    "BABA",
    "IBM",
    "EQIX",
    "DLR",
    "CRWV",
    "APLD",
    "IREN",
    "NBIS",
    "NTNX",
    "DELL",
    "SMCI",
    "HPE",
    "JBL",
    "PENG",
    "FLEX",
    "FN",
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

    values: list[float] = []
    for match in re.finditer(r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text):
        values.append((-1 if match.group(1) == "-" else 1) * float(match.group(2)))
    return sum(values) / len(values) if values else None


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

    # BWXT calibration: formal evaluation supports hard NTM/backlog evidence
    # and better-than-average downside protection. The same evidence does not
    # justify treating long-duration nuclear/AI electricity optionality as NTM
    # hyper-growth, and current valuation plus stale interval momentum remain
    # clear limits.
    target = companies[TARGET]
    overrides = {
        "NTM兑现优先": 84.0,
        "右尾弹性优先": 72.0,
        "风险调整收益": 65.0,
        "下行保护优先": 88.0,
        "估值消化优先": 60.0,
        "近端催化优先": 72.0,
        "价格确认/动量": 45.0,
        "激进短线": 76.0,
    }
    for strategy, score in overrides.items():
        target["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_NUCLEAR:
        return "直接同业"
    if ticker in UTILITY_OR_ENERGY_CHAIN or ticker in DOWNSTREAM_POWER_BUYERS:
        return "上下游"
    if ticker in NUCLEAR_AND_POWER_ADJACENT or ticker in ENGINEERING_AND_GRID or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有backlog、海军合同和FCF锚",
            "右尾弹性优先": "A核能/PCG/TRISO期权更好",
            "风险调整收益": "A政府订单和现金流缓冲更强",
            "下行保护优先": "A政府核合同防守性更强",
            "估值消化优先": "A业绩可见度支撑高倍数",
            "近端催化优先": "A订单转化和PCG节点更近",
            "价格确认/动量": "A价格已从6月初低位修复",
            "激进短线": "A核能主题和IV提供进攻性",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/利润兑现更快",
            "右尾弹性优先": "B右尾更短链且更大",
            "风险调整收益": "B上行/估值组合更优",
            "下行保护优先": "B估值或现金流安全垫更厚",
            "估值消化优先": "B估值消化压力更低",
            "近端催化优先": "B近端重定价事件更强",
            "价格确认/动量": "B趋势确认更强",
            "激进短线": "B高beta更适合短线进攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "安全边际和兑现证据接近"
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
        a["scores"]["NTM兑现优先"] * 1.0
        + a["scores"]["风险调整收益"] * 1.1
        + a["scores"]["下行保护优先"] * 0.8
        + a["scores"]["估值消化优先"] * 0.9
        + a["scores"]["右尾弹性优先"] * 0.7
        + a["scores"]["近端催化优先"] * 0.6
        - b["scores"]["NTM兑现优先"] * 1.0
        - b["scores"]["风险调整收益"] * 1.1
        - b["scores"]["下行保护优先"] * 0.8
        - b["scores"]["估值消化优先"] * 0.9
        - b["scores"]["右尾弹性优先"] * 0.7
        - b["scores"]["近端催化优先"] * 0.6
    )
    return "A" if weighted >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
            return "BWXT 的政府核合同、backlog和FCF让防守质量明显更好。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "BWXT 的FY2026指引、Q1收入和订单/backlog使NTM兑现更硬。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:  # type: ignore[index,operator]
            return "BWXT 的核级制造稀缺性和现金流缓冲优于B的风险组合。"
        return "BWXT 以可见订单、现金流和核能稀缺性略胜，但估值仍需业绩兑现。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        ticker = str(b["ticker"])
        category = str(b["category"])
        if category in HIGH_GROWTH_CATS:
            return f"{ticker} 的AI主链、存储/光互联或云算力右尾更短链且更大。"
        if ticker in UTILITY_OR_ENERGY_CHAIN or category == "电力_发电_能源_储能":
            return f"{ticker} 的电力负荷、核电/能源利润池或项目右尾比BWXT更直接。"
        if category in INFRA_CATS:
            return f"{ticker} 的AI基础设施订单和短线重定价弹性强于BWXT。"
        return f"{ticker} 的小基数或周期右尾显著大于BWXT。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 更容易用NTM业绩消化估值，BWXT倍数已不便宜。"
    if b["scores"]["近端催化优先"] - a["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的近端订单、产品或价格催化更明确。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和资金偏好强于BWXT。"
    return f"{b['ticker']} 在多数投资思路下比BWXT更符合当前配置目标。"


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
            x["b"]["scores"]["右尾弹性优先"] + x["b"]["scores"]["估值消化优先"] - a["scores"]["右尾弹性优先"] - a["scores"]["估值消化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["NTM兑现优先"] + a["scores"]["下行保护优先"] + a["scores"]["风险调整收益"] - x["b"]["scores"]["NTM兑现优先"] - x["b"]["scores"]["下行保护优先"] - x["b"]["scores"]["风险调整收益"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] > x["ac"] and x["bc"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
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
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )
    product_names = [str(product[0]).split("，")[0].split("；")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入8.602亿美元、同比+26%，backlog 86.51亿美元、bookings 22.50亿美元、book-to-bill 2.62x，FY2026收入>37.5亿美元、EBITDA 6.50-6.65亿美元、FCF 3.15-3.30亿美元",
            "backlog转收入仍受核级制造、质量验收、政府拨款和交付节奏约束，不能把长期核能主题直接并入NTM基准",
        ),
        "右尾弹性优先": (
            "乐观收入42.5-46.0亿美元、极度乐观48.0-53.0亿美元；PCG、TRISO、HALEU、SMR和核电重启给远期期权",
            "极度乐观可信度低到中，AI数据中心核能需求大多在NTM之后，短期右尾不如AI芯片、光互联和高beta电力设备",
        ),
        "风险调整收益": (
            "政府核海军合同、Commercial backlog、FCF指引和核级制造稀缺性给出较好风险缓冲",
            "2026-06-22 Forward PE 40.43、P/S 5.70、EV/EBITDA 43.74，不是低估值防守；PCG和先进燃料仍需执行验证",
        ),
        "下行保护优先": (
            "Government Operations、长周期国防/核材料需求、backlog和FCF使其在压力期比多数高beta AI链更稳",
            "估值已抬升，Commercial利润率、营运资本和并购整合会削弱纯防守属性",
        ),
        "估值消化优先": (
            "NTM基准收入38.5-41.0亿美元、EBITDA 6.70-7.25亿美元，业绩锚比纯远期核能公司清楚",
            "当前倍数需要持续高质量交付，基准情景只能部分消化估值，不能只靠TRISO/HALEU/AI核能叙事",
        ),
        "近端催化优先": (
            "Q2-Q4收入run-rate、Government/Commercial backlog分拆、海军/NNSA/DOE合同、PCG 2026H2关闭和分部利润率是1-2季可验证节点",
            "催化更多是稳步验证和合同转化，不如AI主链新订单、产品代际或客户认证那样容易快速重定价",
        ),
        "价格确认/动量": (
            "2026-06-22价格已回到210美元，较2026-06-03的184.72美元明显修复，且IV不算极端",
            "正式区间文件截至2026-06-03仍显示两周-8.85%、一月-14.60%，趋势确认弱于强动量AI硬件链",
        ),
        "激进短线": (
            "Call IV 51.5%、核能主题、政府合同和PCG/TRISO事件能提供中等进攻性",
            "BWXT不是小基数亏损转盈利或AI主链订单爆发型标的，短线弹性弱于高IV高关注度公司",
        ),
    }

    out: list[str] = []
    out += [
        "# BWXT 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：BWXT / BWX Technologies",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 BWXT vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。BWXT 的优势来自政府核项目和核海军长周期 backlog、明确 FY2026 指引、FCF 指引和核级制造稀缺性；它更像高质量核能/国防制造配置，而不是纯 AI 右尾小盘。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 2026-06-22 估值已不便宜、6月初正式区间动量偏弱、TRISO/HALEU/SMR/AI核能大多是远期或乐观以上情景。",
        "- A 最适合的投资者画像：愿意用中高估值买高可信订单、国防核制造、核电生命周期和长期核能期权，同时更重视兑现和下行保护而非最高短线弹性的资金。",
        "- A 最不适合的投资者画像：只追求最高增速、最强AI主链订单、极端高IV短线爆发或低估值深度价值的投资者。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在AI主链右尾、估值消化、近端催化或价格确认上比BWXT更强。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：BWXT 在全项目属于高质量核能/能源安全稀缺资产，NTM兑现和防守性强于多数高beta公司；但总体增长和短线爆发不如AI芯片、光互联、NeoCloud、现场电力和部分电网设备龙头。",
        "- 后续最重要跟踪数据：2026Q2-Q4收入run-rate、book-to-bill、Government/Commercial backlog分拆、海军/NNSA/DOE新合同、分部利润率、FCF与营运资本、PCG关闭和并表收入、Kinectrics同店增长、TRISO/HALEU/advanced reactor订单金额。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "BWXT"]),
        base.row(["公司名称", "BWX Technologies"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "3.85-4.10 十亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "能否把已披露政府和商用核 backlog 按核级制造质量、交期、验收、预算拨款和里程碑回款节奏转为可确认收入。"]),
        base.row(["最大反证", "AI数据中心核能、SMR、TRISO和HALEU大多缺少NTM内大额可确认收入；估值已经要求持续高质量交付。"]),
        base.row(["近端催化剂", "海军/NNSA/DOE合同、Q2-Q4收入run-rate、backlog和book-to-bill、Government/Commercial分部利润率、PCG 2026H2关闭、FCF与营运资本改善。"]),
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
        base.row(["直接同业", "项目内没有完全一一对应的核级制造同业；仅把核动力/国防核和先进核业务高度重叠的公司按直接同业处理。", "RYCEY", "优先看核级制造、订单/backlog、收入兑现、利润质量和估值；同业证据强时可以放大力度。"]),
        base.row(["相邻替代", "同属核能、能源安全、AI数据中心电力、储能、发电设备、电网设备或工程服务配置篮子，但产品不直接相同。", "SMR、OKLO、GEV、BE、PWR、ETN、VRT、POWL、HTHIY", "回答资金只能买一个时谁的增长质量、订单兑现、估值消化和风险调整后收益更好。"]),
        base.row(["上下游", "B 是核电/电力需求端、公用事业、能源供给、云/IDC电力买方或AI算力负荷端，影响长期核能需求但不必然形成BWXT短期收入。", "CEG、VST、AEP、ETR、ET、MSFT、AMZN、ORCL、EQIX、CRWV", "不把下游收入规模直接等同于BWXT机会，重点看利润池捕获、合同路径和NTM可确认收入。"]),
        base.row(["跨赛道", "半导体、设备、材料、软件、工业和消费平台等与BWXT业务差异大，但作为项目内资金配置替代仍可比较。", "NVDA、AVGO、TSM、ASML、MU、CDNS、BABA", "默认降低结论力度；只有增长质量、估值消化、下行保护或价格确认明显拉开时才给建议/强烈建议。"]),
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
        need = "需要BWXT把PCG、TRISO、HALEU或Commercial核服务从远期期权转成NTM订单和利润，并改善价格确认。"
        if "估值消化优先" in wins or "风险调整收益" in wins:
            need = "需要BWXT用基准而非乐观情景消化当前估值，并维持FCF/分部利润率不下滑。"
        if "右尾弹性优先" in wins or "激进短线" in wins:
            need = "需要BWXT出现更明确的高增速订单、客户项目或先进燃料商业化金额，证明右尾不只是长期主题。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B拿出同等强度的订单/backlog、收入兑现、FCF和下行保护证据。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入/利润，并降低估值和波动反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/电力_发电_能源_储能/BWXT_BWX_Technologies_公司调研_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_bwxt_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对BWXT的政府核backlog、海军合同、FCF指引、PCG/TRISO/HALEU远期期权、高估值和价格动量限制做人工校准后建档；未读取下游量化目录或现成排序结论。",
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
                "bwxt_tiers": companies[TARGET]["tiers"],
                "bwxt_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
