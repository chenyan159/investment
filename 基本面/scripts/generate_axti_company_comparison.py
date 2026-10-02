from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "AXTI"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "AXTI_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_MATERIAL_PEERS = {
    "AJNMY",
    "ASGLY",
    "CC",
    "DD",
    "DKILY",
    "ENTG",
    "HOCPY",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}
OPTICAL_DOWNSTREAM = {
    "AAOI",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "FN",
    "GLW",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "MXL",
    "NOK",
    "POET",
    "SMTC",
    "TEL",
    "VIAV",
}
SEMI_CHAIN_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
    "云算力_IDC_AI软件平台",
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
    old_target = base.TARGET
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 94.0,
        "右尾弹性优先": 98.0,
        "风险调整收益": 38.0,
        "下行保护优先": 56.0,
        "估值消化优先": 34.0,
        "近端催化优先": 90.0,
        "价格确认/动量": 62.0,
        "激进短线": 100.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_MATERIAL_PEERS:
        return "直接同业"
    if ticker in OPTICAL_DOWNSTREAM or category in SEMI_CHAIN_CATS:
        return "上下游"
    if category == "半导体材料_化学品_基板" or category in INFRA_CATS or category in HIGH_GROWTH_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的InP backlog和Q2收入锚更硬",
            "右尾弹性优先": "A小基数InP/CPO右尾更大",
            "风险调整收益": "A上行弹性可覆盖部分风险",
            "下行保护优先": "A增发后现金和压力窗口较好",
            "估值消化优先": "A收入倍增可部分消化估值",
            "近端催化优先": "A的Q2许可/InP验证更近",
            "价格确认/动量": "A价格和IV确认InP重估",
            "激进短线": "A高IV叠加光互联叙事更强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单或利润兑现更稳",
            "右尾弹性优先": "B平台或直接AI右尾更大",
            "风险调整收益": "B估值现金流组合更好",
            "下行保护优先": "B低波动和现金流更防守",
            "估值消化优先": "B估值消化压力低于A",
            "近端催化优先": "B近端订单或财报催化更确定",
            "价格确认/动量": "B价格趋势更强或回吐更少",
            "激进短线": "B短线关注度或爆发力更强",
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
    key_weight = (
        a["scores"]["NTM兑现优先"]
        + a["scores"]["右尾弹性优先"] * 0.8
        + a["scores"]["近端催化优先"] * 0.6
        + a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"]
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["右尾弹性优先"] * 0.8
        - b["scores"]["近端催化优先"] * 0.6
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "AXTI 的InP backlog、Q2收入锚和年底产能路径让NTM兑现更强。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "AXTI 的小基数InP、6英寸和CPO/ELS期权提供更大右尾。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "AXTI 的Q2/Q3收入、出口许可、backlog和LTA验证窗口更近。"
        if a["scores"]["激进短线"] - b["scores"]["激进短线"] > 12:  # type: ignore[index,operator]
            return "AXTI 的高IV、高关注度和AI光互联上游叙事更适合短线进攻。"
        return "AXTI 在InP收入化和近端验证上略胜，尽管估值反证仍重。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值、现金流和反证组合明显好于 AXTI。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化压力显著低于 AXTI。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、低波动或压力期表现更安全。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入或平台型右尾强于 AXTI。"
    return f"{b['ticker']} 在多数投资思路下比 AXTI 更符合项目内资金配置目标。"


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
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return output


def fmt_num(value: object, suffix: str = "", precision: int = 2) -> str:
    if value is None:
        return "缺失"
    if isinstance(value, float):
        return f"{value:.{precision}f}{suffix}"
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
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["风险调整收益"] - a["scores"]["风险调整收益"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["NTM兑现优先"] - x["b"]["scores"]["NTM兑现优先"]),  # type: ignore[index,operator]
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
        f"2026-06-22 金融快照：AXTI价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE 不适用，Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，"
        f"P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}；"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("，")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入2692万美元、InP收入1360万美元；Q2约3400万美元收入可确认或无需许可，InP backlog超过1亿美元",
            "出口许可、客户验收和合格产能仍是收入确认阀门，TTM仍亏损",
        ),
        "右尾弹性优先": (
            "NTM基准收入1.75-2.20亿美元，乐观2.40-3.10亿美元，极度乐观3.30-4.20亿美元；小基数+InP扩产+6英寸/CPO提供非线性",
            "衬底在模块BOM中价值占比小，AXTI不控制DSP/模块/交换机平台，客户多供会限制定价权",
        ),
        "风险调整收益": (
            "增发后资金安全垫强，SOXX压力窗口累计+20%，需求与backlog不是空叙事",
            "2026-06-22 P/S 63.07、Forward PE 122.93、Call IV 140%，任何许可或良率失误都会被放大",
        ),
        "下行保护优先": (
            "4月大额股权融资缓解扩产资金，三段SOXX压力窗口历史表现较强",
            "高IV、高P/S、仍亏损、库存和政策许可风险使它不是安全资产",
        ),
        "估值消化优先": (
            "若收入从不足1亿美元TTM提升到2-4亿美元区间，估值分母会快速变大",
            "当前市值已提前定价多年InP扩产和利润率改善，基准情景也难轻松消化63x TTM P/S",
        ),
        "近端催化优先": (
            "Q2总收入、InP收入、出口许可、Q3指引、backlog续补、LTA和4/6英寸qualification都在1-2季内验证",
            "催化高度集中在许可和执行，若Q2/Q3没有连续上修会快速反噬",
        ),
        "价格确认/动量": (
            "一月+11.15%，2026-06-22价格92.44美元且IV极高，市场已确认InP稀缺叙事",
            "过去两周仅+2.00%，较2026-06-03的106.70美元已有回吐，动量质量不如强趋势AI主线",
        ),
        "激进短线": (
            "140% Call IV、小盘高关注、InP backlog、AI光互联/CPO/ELS叙事和Q2验证窗口适合短线进攻",
            "估值和拥挤度极高，短线容错低，负面许可或毛利率信号会引发剧烈回撤",
        ),
    }

    out: list[str] = []
    out += [
        "# AXTI 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：AXTI / AXT Inc",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 AXTI vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。AXTI 的优势集中在InP backlog、Q2收入确认、年底产能爬坡、6英寸/4英寸高规格InP和AI光互联上游稀缺性，不是稳健低估值资产。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。核心短板是估值已极度前置、IV很高、TTM仍亏损、出口许可和良率会决定收入是否真的入表。",
        "- A 最适合的投资者画像：愿意为AI光互联上游瓶颈付高估值、重点押注未来1-2季收入验证、能承受高波动和政策/许可风险的进攻型资金。",
        "- A 最不适合的投资者画像：以估值消化、现金流、低波动、资产负债表稳定性或公用事业式下行保护为首要目标的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在平台定价权、现金流、防守属性或估值消化上明显压过 AXTI。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：AXTI 是项目内最极端的高弹性小基数InP上游标的之一；在兑现、右尾、近端和短线列可以击败大量传统公司，但若投资思路要求风险调整和估值消化，它会输给很多质量更稳的AI主链、设备、云和基础设施公司。",
        "- 后续最重要跟踪数据：2026Q2总收入是否达到约3400万美元、InP收入是否超过1700万美元并继续向2500-3500万美元/季度爬坡、InP backlog是否维持1亿美元以上、出口许可节奏、GAAP/non-GAAP毛利率是否走向35%-40%、LTA/预付款、4英寸/6英寸qualification、库存和应收周转、800G/1.6T模块ASP和客户库存。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "AXTI"]),
        base.row(["公司名称", "AXT Inc"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`1.75-2.20 亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "InP出口许可、合格wafer交付、客户验收和收入确认节奏；backlog只有转成出货、验收和现金流才算兑现。"]),
        base.row(["最大反证", "2026-06-22 P/S 63.07、Forward PE 122.93、Call IV 140%，TTM仍亏损；市场已把InP扩产、价格和长协提前资本化。"]),
        base.row(["近端催化剂", "2026Q2/Q3收入和EPS、InP收入、出口许可、backlog续补、LTA/预付款、4英寸/6英寸InP qualification、毛利率和库存周转。"]),
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
        base.row(["直接同业", "同属半导体材料、化合物半导体衬底、电子化学品、光学/基板材料或关键上游材料，优先比较客户认证、订单/backlog、良率、产能和同业估值。", "SMTOY、MTRN、HOCPY、ENTG、SHECY、ASGLY、DD", "同业证据权重最高；若对方利润质量和估值更稳，会直接压低AXTI的风险调整和估值消化列。"]),
        base.row(["相邻替代", "同属AI材料、工业材料、AI基础设施或高弹性小盘资金篮子，但产品不直接竞争；回答资金只能买一个时谁的赔率更好。", "APD、LIN、ECL、ETN、VRT、POWL、GEV", "重点看增长质量、估值消化、下行保护和近端催化，不因AXTI叙事更热自动胜出。"]),
        base.row(["上下游", "B处在AXTI所服务的光模块、激光器、SiPh、AI网络、云、服务器、封测、晶圆制造或设备链条。", "COHR、LITE、AAOI、AVGO、MRVL、ANET、NVDA、TSM、AMAT、ASML", "不把下游AI收入规模直接等同AXTI机会，也不把上游材料稀缺自动等同更好；核心看利润捕获、估值和反证。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化。", "CAT、DHR、TMO、MSI、RKLB、TSLA", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 AXTI 把InP backlog连续转成收入、毛利率和现金流，并证明高估值不会被执行风险反噬。"
        if comparison["rel"] == "直接同业":
            need = "需要 AXTI 在同业中证明InP订单、良率、客户认证和利润率显著强于B，同时估值不过度透支。"
        elif comparison["rel"] == "上下游":
            need = "需要 AXTI 证明上游衬底利润捕获能接近下游平台、光模块、芯片或设备公司的成长斜率和确定性。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 AXTI 用更强收入兑现和现金流改善抵消跨赛道标的的防守、估值或质量优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提高收入确认速度、右尾弹性或近端催化强度，或拿出更明确订单/backlog。"
        if b["scores"]["风险调整收益"] > a["scores"]["风险调整收益"]:  # type: ignore[index,operator]
            need = "需要 B 把风险调整优势之外的增长和催化补强，否则难压过AXTI的InP小基数弹性。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/半导体材料_化学品_基板/AXTI_AXT_Inc_公司调研_2026-06-22.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_激光器、EML与光器件_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_硅光材料、光子材料与电光聚合物_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_axti_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+83%-129%` 做同号区间修正；对AXTI的InP backlog、Q2收入锚、高估值、高IV、许可和扩产风险做人工校准后建档。",
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
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "axti_tiers": companies[TARGET]["tiers"],
        "axti_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
