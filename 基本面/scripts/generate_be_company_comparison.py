from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "BE"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "BE_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_ONSITE_POWER = {"FCEL", "GNRC", "PSIX"}
UPSTREAM_FUEL_OR_POWER = {"AEP", "DTE", "ET", "ETR", "CEG", "VST", "LIN", "APD"}
DOWNSTREAM_AI_LOAD = {
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
ADJACENT_POWER_INFRA = {
    "GEV",
    "RYCEY",
    "SMR",
    "OKLO",
    "CMI",
    "FLNC",
    "ENS",
    "POWL",
    "PWR",
    "ETN",
    "VRT",
    "HUBB",
    "NVT",
    "AEIS",
    "POWI",
    "VICR",
    "MOD",
    "AAON",
    "TT",
    "CARR",
    "JCI",
    "FIX",
    "EME",
    "MYRG",
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

    # Bloom calibration: formal company evaluation supports top-tier NTM,
    # right-tail and near-term catalyst evidence. Daily valuation/IV data
    # shows the opposite for downside protection and valuation digestion.
    target = companies[TARGET]
    overrides = {
        "NTM兑现优先": 94.0,
        "右尾弹性优先": 100.0,
        "风险调整收益": 48.0,
        "下行保护优先": 33.0,
        "估值消化优先": 42.0,
        "近端催化优先": 86.0,
        "价格确认/动量": 64.0,
        "激进短线": 100.0,
    }
    for strategy, score in overrides.items():
        target["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_ONSITE_POWER:
        return "直接同业"
    if ticker in DOWNSTREAM_AI_LOAD or category in {"云算力_IDC_AI软件平台", "AI服务器_存储_EMS"}:
        return "上下游"
    if ticker in UPSTREAM_FUEL_OR_POWER:
        return "上下游"
    if ticker in ADJACENT_POWER_INFRA or category in INFRA_CATS or category == "电力_发电_能源_储能":
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有指引、backlog和客户项目硬锚",
            "右尾弹性优先": "A是AI onsite power高右尾",
            "风险调整收益": "A上行可覆盖部分执行风险",
            "下行保护优先": "B现金流或反证更弱",
            "估值消化优先": "A高增速可部分消化高倍数",
            "近端催化优先": "A客户/产能节点更近",
            "价格确认/动量": "A最新价格和高IV确认关注",
            "激进短线": "A高IV叠加AI电力叙事更强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入或利润兑现更稳",
            "右尾弹性优先": "B右尾更直接或更大",
            "风险调整收益": "B估值现金流组合更好",
            "下行保护优先": "B估值和现金流缓冲更强",
            "估值消化优先": "B估值消化压力低于A",
            "近端催化优先": "B近端催化更确定",
            "价格确认/动量": "B趋势更强或更不拥挤",
            "激进短线": "B短线爆发力更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "估值和安全边际接近"
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
        a["scores"]["NTM兑现优先"] * 0.9
        + a["scores"]["右尾弹性优先"] * 0.8
        + a["scores"]["风险调整收益"] * 1.1
        + a["scores"]["估值消化优先"]
        + a["scores"]["近端催化优先"] * 0.6
        + a["scores"]["下行保护优先"] * 0.5
        - b["scores"]["NTM兑现优先"] * 0.9
        - b["scores"]["右尾弹性优先"] * 0.8
        - b["scores"]["风险调整收益"] * 1.1
        - b["scores"]["估值消化优先"]
        - b["scores"]["近端催化优先"] * 0.6
        - b["scores"]["下行保护优先"] * 0.5
    )
    return "A" if weighted >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
            return "BE 的指引、backlog和客户项目使 NTM 兑现证据更硬。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
            return "BE 的 AI 数据中心 onsite power 右尾明显更大。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 14:  # type: ignore[index,operator]
            return "BE 的 Oracle/Nebius/AEP/产能节点更可能近端重定价。"
        return "BE 以高增长和高催化压过 B，但需要承受高估值和高波动。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、估值缓冲和压力期韧性明显优于 BE。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 更容易用业绩消化估值，BE 已要求乐观执行。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的风险调整收益更均衡。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和资金偏好强于 BE。"
    return f"{b['ticker']} 在多数投资思路下比 BE 更适合当前配置目标。"


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
    product_names = [str(product[0]).split(" / ")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入$751.1M、FY2026收入指引$3.4-3.8B、current product backlog约$6B，Oracle初始1.2GW、Nebius 328MW和AEP路径提供硬锚",
            "NTP、permit、gas、switchgear/transformer、commissioning、验收和回款任一环节延迟都会打断收入确认",
        ),
        "右尾弹性优先": (
            "NTM基准收入$4.5-5.4B，极度乐观$7.6-9.1B；Oracle最高2.8GW、Project Jupiter最高2.45GW、Brookfield $5B框架提供非线性上限",
            "极度乐观要求2GW+有效产能、Product GM 36%+、Service GM上行、低质量事故和现金转换同时成立",
        ),
        "风险调整收益": (
            "增长已进入收入表，Product GM 34.3%，基准Adjusted EBITDA $0.85-1.20B，右尾上行真实",
            "2026-06-22 P/S 40.17、Forward PE 79.26、EV/EBITDA 406.08、Call IV 109.8%，且SOXX压力窗口累计-96.29%",
        ),
        "下行保护优先": (
            "backlog、客户项目和Q1 OCF为正给出一定底部支撑",
            "高估值、高IV、客户集中、营运资本和历史压力窗口跌幅使其不适合防守口径",
        ),
        "估值消化优先": (
            "若NTM收入接近乐观且EBITDA/FCF兑现，估值可被部分消化",
            "当前市值和P/S已要求乐观甚至极度乐观执行，基准收入不足以轻松消化",
        ),
        "近端催化优先": (
            "Oracle/Nebius/AEP部署、2GW产能爬坡、Product GM、Service GM、Brookfield项目落地都能在1-2季持续验证",
            "催化强但也集中在交付链，任何许可/燃气/验收或毛利反证都会被迅速重定价",
        ),
        "价格确认/动量": (
            "2026-06-22价格显著高于6月初区间文件锚点，高IV显示资金关注度强",
            "正式区间涨跌文件截至2026-06-03仍只显示两周+1.77%、一月-1.10%，且压力窗口回撤很深",
        ),
        "激进短线": (
            "Call IV 109.8%、AI数据中心电力瓶颈、GW级客户项目和高右尾叙事都适合短线进攻",
            "短线不是低风险交易，估值、回撤和执行反证会放大波动",
        ),
    }

    out: list[str] = []
    out += [
        "# BE 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：BE / Bloom Energy",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 BE vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。BE 的优势集中在 NTM 兑现、AI 数据中心 onsite power 右尾、近端客户/产能催化和激进短线进攻，不是传统防守或低估值标的。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 2026-06-22 估值和 IV 已极高，且 SOXX 压力窗口累计跌幅深，基准业绩难以轻松消化当前市值。",
        "- A 最适合的投资者画像：愿意为 AI 数据中心电力瓶颈、GW 级客户项目、订单/backlog 和 2026-2027 收入非线性增长承担高估值、高波动和执行风险的进攻型资金。",
        "- A 最不适合的投资者画像：优先要低波动、低估值、现金流防守、压力期韧性或已经被财务报表充分消化的稳健配置者。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在下行保护、估值消化、风险调整收益、现金流质量或更稳健价格确认上压过 BE。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：BE 是项目内增长/右尾/催化顶档，但不是综合质量无短板；它的总体吸引力取决于投资者是否愿意把高估值和高回撤视为换取非线性收入上修的成本。",
        "- 后续最重要跟踪数据：Product revenue、Product GM、Service GM、Installation GM、Non-GAAP operating income、OCF/FCF、存货/应收、Oracle/Nebius/AEP/Brookfield 的 PO/NTP/设备到场/上电/验收、2GW 产能良率、current product backlog、Project Jupiter permit/gas/water/air-quality 进度。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "BE"]),
        base.row(["公司名称", "Bloom Energy"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$4.5-5.4B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "订单到收入的执行链：客户NTP、许可、燃气运输、switchgear/transformer、制造slot、现场commissioning、验收和现金回收。"]),
        base.row(["最大反证", "高估值和高IV已经把乐观执行前置定价；若Product GM低于30%、Installation继续亏损、项目延迟或营运资本吞噬OCF，右尾会被快速重估。"]),
        base.row(["近端催化剂", "Oracle初始1.2GW部署、Nebius 328MW、AEP采购路径、Brookfield项目融资、Project Jupiter、2GW产能爬坡、Product/Service GM和OCF/FCF连续验证。"]),
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
        base.row(["直接同业", "与 BE 在 onsite generation、燃料电池、数据中心自备电源或燃气/柴油替代供电方案上直接争夺同一需求池。", "FCEL、GNRC、PSIX", "优先看订单/backlog、MW交付、Product GM、服务成本、可靠性和估值；同业强证据可放大判断力度。"]),
        base.row(["相邻替代", "同属 AI 数据中心电力、储能、配电、冷却、工程或能源供给资金篮子，但产品不直接相同。", "GEV、SMR、OKLO、ETN、VRT、PWR、POWL、FLNC、TT、AAON", "回答资金只能买一个时谁的增长质量、利润捕获、估值消化和近端催化更好。"]),
        base.row(["上下游", "B 是 BE 项目的燃料/utility/电力供应链，或是 AI 数据中心和云算力需求端，决定 BE 订单的最终负荷和上电需求。", "AEP、ET、CEG、MSFT、AMZN、ORCL、CRWV、APLD、IREN、EQIX、DLR", "不把下游收入规模直接等同于更好，重点看 BE 能否捕获利润池与B自身现金流/估值质量。"]),
        base.row(["跨赛道", "半导体、设备、材料、软件、工业和消费平台等与 BE 业务差异大，但作为项目内资金配置替代仍可比较。", "NVDA、AVGO、TSM、ASML、MU、CDNS、BABA", "默认降低结论力度；只有增长质量、估值消化、下行保护或价格确认明显拉开时才给建议/强烈建议。"]),
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
        need = "需要 BE 证明高增长能转为Product GM、OCF/FCF和可持续backlog，并降低高估值/高IV反证。"
        if "下行保护优先" in wins or "估值消化优先" in wins:
            need = "需要 BE 让基准业绩而非乐观业绩就能消化估值，并证明压力期回撤不再失控。"
        if "风险调整收益" in wins:
            need = "需要 BE 把Oracle/Nebius/AEP交付、毛利和现金流同步兑现，压低执行风险。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 拿出同等强度的订单/backlog、客户项目、收入增速或近端重定价证据。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要 B 在保持下行保护的同时补足增长右尾、近端催化和收入兑现速度。"
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
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/电力_发电_能源_储能/BE_Bloom_Energy_公司调研_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_动态UPS、飞轮与超级电容_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_be_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 BE 的订单/backlog、AI 数据中心 onsite power 右尾、高估值、高IV、压力窗口回撤和执行风险做人工校准后建档；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
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
                "be_tiers": companies[TARGET]["tiers"],
                "be_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
