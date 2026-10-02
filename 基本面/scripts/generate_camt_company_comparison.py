from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "CAMT"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CAMT_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_INSPECTION_METROLOGY = {"KLAC", "NVMI", "ONTO"}
PACKAGING_TEST_ADJACENT = {
    "AEHR",
    "ATEYY",
    "ASMVY",
    "BESIY",
    "COHU",
    "FORM",
    "KEYS",
    "KLIC",
    "MICLF",
    "PLAB",
    "TDY",
    "TER",
    "TMO",
}
OSAT_MEMORY_FOUNDRY_CUSTOMERS = {
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
AI_DEMAND_CHAIN = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "ARM",
    "AVGO",
    "COHR",
    "CRDO",
    "DELL",
    "FN",
    "HPE",
    "LITE",
    "META",
    "MRVL",
    "MSFT",
    "NVDA",
    "ORCL",
    "QCOM",
    "SMCI",
}
SEMICAP_ADJACENT = {
    "ACLS",
    "ACMR",
    "AEIS",
    "AMAT",
    "ASMIY",
    "ASML",
    "DSCSY",
    "ICHR",
    "LRCX",
    "MKSI",
    "TOELY",
    "UCTT",
    "VECO",
}
SEMI_MATERIALS = {
    "AJNMY",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "ENTG",
    "HOCPY",
    "LIN",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}
SEMI_RELATED_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "半导体材料_化学品_基板",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
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
    old_target = base.TARGET
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    # CAMT calibration. Generic extraction captures the base growth path, but
    # it underweights disclosed 2026 OSAT/IDM orders, the 2027 HBM/OSAT order
    # bridge, Hawk/Eagle mix, and the high-visibility Q2/H2 validation window.
    # It also needs explicit caps for very high PE/P-S, high IV, and deep SOXX
    # pressure-window drawdowns.
    target = companies[TARGET]
    overrides = {
        "NTM兑现优先": 88.0,
        "右尾弹性优先": 90.0,
        "风险调整收益": 55.0,
        "下行保护优先": 49.0,
        "估值消化优先": 50.0,
        "近端催化优先": 86.0,
        "价格确认/动量": 74.0,
        "激进短线": 92.0,
    }
    for strategy, score in overrides.items():
        target["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_INSPECTION_METROLOGY:
        return "直接同业"
    if ticker in OSAT_MEMORY_FOUNDRY_CUSTOMERS or ticker in AI_DEMAND_CHAIN:
        return "上下游"
    if ticker in PACKAGING_TEST_ADJACENT or ticker in SEMICAP_ADJACENT:
        return "相邻替代"
    if ticker in SEMI_MATERIALS:
        return "相邻替代"
    if category == "封测_检测_计量_光罩":
        return "相邻替代"
    if category in SEMI_RELATED_CATS:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的Q2指引/H2 ramp和订单锚更硬",
            "右尾弹性优先": "A有HBM/CoWoS/Hawk高端工具右尾",
            "风险调整收益": "A增长和现金流可抵部分估值压力",
            "下行保护优先": "A盈利现金流和净现金略稳",
            "估值消化优先": "A高端设备增长可部分消化高倍数",
            "近端催化优先": "A的Q2/H2/2027订单验证更近",
            "价格确认/动量": "A两周涨幅和高IV确认重估",
            "激进短线": "A高IV叠加先进封装叙事更强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入或利润兑现路径更稳",
            "右尾弹性优先": "B右尾规模或平台弹性更大",
            "风险调整收益": "B估值现金流组合更均衡",
            "下行保护优先": "B低波动和估值缓冲更强",
            "估值消化优先": "B估值消化压力低于A",
            "近端催化优先": "B近端订单或财报催化更确定",
            "价格确认/动量": "B趋势更强或回吐更少",
            "激进短线": "B短线关注度或爆发力更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if rel == "直接同业":
        return "同业证据接近需等订单和份额验证"
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
        a["scores"]["NTM兑现优先"] * 1.0
        + a["scores"]["右尾弹性优先"] * 0.8
        + a["scores"]["风险调整收益"] * 1.1
        + a["scores"]["估值消化优先"] * 0.9
        + a["scores"]["近端催化优先"] * 0.7
        + a["scores"]["下行保护优先"] * 0.6
        - b["scores"]["NTM兑现优先"] * 1.0
        - b["scores"]["右尾弹性优先"] * 0.8
        - b["scores"]["风险调整收益"] * 1.1
        - b["scores"]["估值消化优先"] * 0.9
        - b["scores"]["近端催化优先"] * 0.7
        - b["scores"]["下行保护优先"] * 0.6
    )
    return "A" if weighted >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "CAMT 的Q2指引、H2 ramp、OSAT/HBM/Hawk订单让NTM兑现证据更硬。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 15:  # type: ignore[index,operator]
            return "CAMT 在HBM/CoWoS-like/先进封装检测量测上的右尾更直接。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "CAMT 的Q2/H2交付和2027订单节奏更可能近端重定价。"
        return "CAMT 的先进封装增长和订单可见度略胜，但仍需承受高估值。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、估值缓冲和压力期韧性明显优于 CAMT。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 更容易用未来业绩消化估值，CAMT 倍数已不便宜。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的风险调整收益更均衡。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和资金偏好强于 CAMT。"
    return f"{b['ticker']} 在多数投资思路下比 CAMT 更适合当前配置目标。"


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
            "2026Q2指引$129M-$131M、H2收入预计较H1增长25%+，2026 OSAT/IDM Hawk订单和2027 HBM/OSAT订单给出交付锚",
            "公司不披露标准backlog，2027订单未给季度节奏，客户验收和交付节奏仍是收入确认瓶颈",
        ),
        "右尾弹性优先": (
            "Hawk、Eagle G5、MicroProf/FRT覆盖HBM、CoWoS-like、chiplet、hybrid bonding和先进封装量测，极度乐观收入上限$800M-$900M",
            "极度乐观要求多客户POR、HBM4E/16Hi、OSAT二供和高端mix同时兑现，证据还不足以进基准",
        ),
        "风险调整收益": (
            "2025 OCF $142.6M，non-GAAP经营利润率基准27%-30%，高毛利设备属性优于多数亏损右尾标的",
            "2026-06-22 TTM PE 199.71、Forward PE 43.25、P/S 18.06、EV/EBITDA 63.55、Call IV 84.5%，赔率被高估值压缩",
        ),
        "下行保护优先": (
            "公司盈利、现金/存款/有价证券充足，服务和成熟应用提供收入底盘",
            "三段SOXX压力窗口累计-75.31%，高IV和高倍数使其仍不是防守标的",
        ),
        "估值消化优先": (
            "NTM基准收入$610M-$650M、乐观$680M-$760M，若Hawk/Eagle mix推动利润率上修，可部分消化倍数",
            "当前P/S和PE已经要求乐观执行，若只落在基准下沿，估值消化压力仍大",
        ),
        "近端催化优先": (
            "Q2实际收入、Q3/Q4指引、H2 +25%兑现、Hawk追加订单、2027订单交付节奏和Visual Layer商业化都在1-2季可验证",
            "催化集中在订单/交付/验收链，任何push-out或毛利未上修都会快速伤害定价",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+15.11%，2026-06-22价格高于6月初锚点，高IV显示资金关注",
            "过去一月仍为-1.70%，压力窗口深回撤，价格确认强但并非无透支",
        ),
        "激进短线": (
            "Call IV 84.5%、先进封装/HBM/CoWoS叙事、Q2/H2订单验证和小市值高端设备弹性适合进攻",
            "短线收益依赖高波动和叙事延续，高估值下任何反证都会放大回撤",
        ),
    }

    out: list[str] = []
    out += [
        "# CAMT 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：CAMT / Camtek",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 CAMT vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。CAMT 的优势集中在先进封装/HBM检测量测、Q2/H2收入兑现、2026/2027订单桥和激进短线右尾，不是低估值防守仓。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。核心短板是 2026-06-22 估值、IV 和历史压力窗口回撤都偏高，风险调整收益和估值消化不能只看收入高增。",
        "- A 最适合的投资者画像：愿意押注 HBM/CoWoS-like/chiplet/hybrid bonding 资本开支继续转化为高端 inspection/metrology 订单，并能承受高估值和高波动的进攻型半导体设备投资者。",
        "- A 最不适合的投资者画像：优先要低倍数、低回撤、现金流防守、压力期韧性或成熟股息/现金流型配置者。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在下行保护、估值消化、风险调整收益、现金流质量或更大平台右尾上压过 CAMT。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：CAMT 是项目内半导体设备链里增长/催化/右尾很靠前的标的，但不是综合质量无短板；它更像高端检测量测的进攻型核心，而非所有风格下的最优配置。",
        "- 后续最重要跟踪数据：2026Q2实际收入、Q3/Q4指引、H2较H1 +25%是否兑现、Hawk追加订单、2027 >$105M订单季度交付节奏、Hawk/Eagle G5 mix、non-GAAP GM、库存/应收/OCF、Visual Layer是否形成可收费软件收入。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "CAMT"]),
        base.row(["公司名称", "Camtek"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$610M-$650M"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI芯片需求需经HBM/CoWoS-like/OSAT capex、高端inspection/metrology PO、交付、客户验收后才能确认收入。"]),
        base.row(["最大反证", "不披露标准backlog和分产品收入；若H2 ramp、Hawk追加订单、客户验收或毛利率上修不达预期，高估值会快速重估。"]),
        base.row(["近端催化剂", "2026Q2实际和Q3指引、H2 +25%兑现、OSAT/HBM/Hawk追加订单、2027订单节奏、Hawk/Eagle G5 mix、Visual Layer整合。"]),
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
        base.row(["直接同业", "与 CAMT 在半导体高端 inspection/metrology、先进封装/HBM/wafer级量测需求池高度重叠。", "ONTO、NVMI、KLAC", "优先看客户份额、工具代际、订单/验收、毛利率、估值和同业压力窗口表现；同业强证据可放大判断力度。"]),
        base.row(["相邻替代", "同属封测/检测/先进封装/半导体设备或材料资金篮子，但产品不直接相同。", "ATEYY、FORM、COHU、TER、ASMVY、BESIY、AMAT、ASML、LRCX、ENTG", "回答资金只能买一个时谁的增长质量、订单兑现、估值消化和近端催化更好。"]),
        base.row(["上下游", "B 是 OSAT、foundry、memory、AI芯片或AI服务器/云需求端，决定 CAMT 工具需求的最终资本开支。", "TSM、ASX、AMKR、MU、NVDA、AMD、AVGO、SMCI、DELL、MSFT", "不把下游收入规模等同于更好，重点看 CAMT 能否捕获利润池与B自身现金流/估值质量。"]),
        base.row(["跨赛道", "电力、冷却、云软件、工业和消费平台等与 CAMT 业务差异大，但作为项目内资金配置替代仍可比较。", "BE、VRT、ETN、ORCL、BABA、CRWD、GEV", "默认降低结论力度；只有增长质量、估值消化、下行保护或价格确认明显拉开时才给建议/强烈建议。"]),
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
        need = "需要 CAMT 证明H2 ramp、Hawk订单、毛利率和OCF同步兑现，并降低高估值/高IV反证。"
        if "下行保护优先" in wins or "估值消化优先" in wins:
            need = "需要 CAMT 让基准收入和利润而非乐观情景就能消化估值，并证明压力期回撤不再失控。"
        if "风险调整收益" in wins:
            need = "需要 CAMT 把高端设备订单、利润率和现金流连续兑现，压低客户集中和验收风险。"
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
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/封测_检测_计量_光罩/CAMT_Camtek_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体检测量测设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_camt_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 CAMT 的 HBM/CoWoS/Hawk/Eagle 订单、Q2/H2兑现、高估值、高IV、压力窗口回撤和执行风险做人工校准后建档；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
    base.REPORT_DATE = REPORT_DATE
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
                "camt_tiers": companies[TARGET]["tiers"],
                "camt_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
