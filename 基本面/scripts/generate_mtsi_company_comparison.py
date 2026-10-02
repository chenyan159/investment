from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "MTSI"
TARGET_NAME = "MACOM Technology Solutions"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MTSI_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {"COHR", "LITE", "AAOI", "POET", "LWLG"}
OPTICAL_VALUE_CHAIN = {
    "ALAB",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "CRDO",
    "CSCO",
    "FN",
    "GLW",
    "MRVL",
    "NOK",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}
CUSTOMER_OR_PLATFORM = {
    "NVDA",
    "AMD",
    "AMZN",
    "MSFT",
    "GOOGL",
    "META",
    "ORCL",
    "BABA",
    "IBM",
    "CRWV",
    "APLD",
    "IREN",
    "NBIS",
    "DELL",
    "HPE",
    "SMCI",
    "CLS",
    "FLEX",
    "JBL",
    "SANM",
}
RF_ANALOG_ADJACENT = {
    "ADI",
    "MCHP",
    "MXL",
    "MPWR",
    "ON",
    "QCOM",
    "RMBS",
    "TXN",
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

    # MTSI calibration: Q2 revenue, Q3 guide, 1.5x book-to-bill and record
    # backlog make NTM and near-term catalyst strong. The counterweights are
    # high valuation, high IV, limited product/customer/backlog disclosure,
    # and weak SOXX stress-window behavior.
    mtsi = companies[TARGET]
    overrides = {
        "NTM兑现优先": 84.0,
        "右尾弹性优先": 91.0,
        "风险调整收益": 51.0,
        "下行保护优先": 58.0,
        "估值消化优先": 55.0,
        "近端催化优先": 78.0,
        "价格确认/动量": 80.0,
        "激进短线": 100.0,
    }
    for strategy, score in overrides.items():
        mtsi["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in OPTICAL_VALUE_CHAIN or ticker in CUSTOMER_OR_PLATFORM:
        return "上下游"
    if ticker in RF_ANALOG_ADJACENT:
        return "相邻替代"
    if category in {"AI网络_光互联_连接器"}:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的Q3指引和订单转收入更硬",
            "右尾弹性优先": "A的1.6T/ACC/3.2T期权更直接",
            "风险调整收益": "A增长和防务底座可覆盖部分估值",
            "下行保护优先": "B更弱且A有I&D/Telecom底座",
            "估值消化优先": "A高增速可部分消化高倍数",
            "近端催化优先": "A有Q3、backlog和1.6T验证",
            "价格确认/动量": "A近月价格确认更强",
            "激进短线": "A高IV叠加光互联叙事更适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或利润兑现更硬",
            "右尾弹性优先": "B右尾更大或小基数更弹",
            "风险调整收益": "B估值与下行组合更好",
            "下行保护优先": "B现金流/估值/压力期更稳",
            "估值消化优先": "B估值消化压力更低",
            "近端催化优先": "B近端订单/财报催化更直接",
            "价格确认/动量": "B价格趋势或确认更强",
            "激进短线": "B短线事件弹性更强",
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
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "MTSI 的 Q3 指引、1.5x book-to-bill、record backlog 和 1.6T/ACC 验证更近。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
            return "MTSI 的 800G/1.6T optical analog、LPO/LRO/ACC、3.2T/448G 和 I&D/GaN 右尾更直接。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "MTSI 的 Q3 run-rate 和 Data Center/I&D 收入桥更能支持未来 12 个月兑现。"
        return "MTSI 的增长质量、近端验证和光互联稀缺性足以压过 B 的部分估值或防守优势。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、估值或压力期韧性明显好于高估值的 MTSI。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化压力低于 MTSI，MTSI 已资本化较多乐观路径。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/利润兑现证据更硬。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的小基数、直接 AI 收入或利润杠杆右尾更大。"
    return f"{b['ticker']} 在多数投资思路下比 MTSI 更符合项目内资金配置目标。"


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
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    support = {
        "NTM兑现优先": (
            "FY2026Q2收入2.89亿美元、Q3指引3.31-3.39亿美元、book-to-bill 1.5x和record backlog支撑NTM 14.3-15.5亿美元",
            "产品级客户、backlog绝对金额和Data Center内部800G/1.6T拆分未披露",
        ),
        "右尾弹性优先": (
            "1.6T optical analog、LPO/LRO/ACC、448G/400G-per-lane、CW laser/InP、I&D/GaN/SATCOM形成多条右尾",
            "3.2T/448G、CPO/ELS和IQE供给增强多属低到中可信，不能全部提前进NTM",
        ),
        "风险调整收益": (
            "基准收入+33%-44%、non-GAAP OM 28%-30.5%、FCF 3.2-4.3亿美元，增长和利润质量较好",
            "2026-06-22 Forward PE 57.89、P/S 28.15、EV/EBITDA 126.01、Call IV 73.2%",
        ),
        "下行保护优先": (
            "I&D、Telecom、防务/GaN和正FCF提供非AI收入底座，业务质量强于纯概念小票",
            "SOXX压力窗口累计-44.86%，高估值和高IV使其不是防守资产",
        ),
        "估值消化优先": (
            "若Q3 run-rate延续且GM向60%靠近，NTM利润可部分消化当前倍数",
            "当前价格已要求Data Center、1.6T、I&D/GaN多线兑现，单季达指引不足以支持高倍数",
        ),
        "近端催化优先": (
            "Q3实际收入/GM、Q4指引、record backlog转收入、1.6T production volume、MACD-41804客户平台和IQE交易均可在1-2季验证",
            "若管理层仍不披露客户、订单金额或产品级收入，催化会被估值透支抵消",
        ),
        "价格确认/动量": (
            "2026-06-03过去一月+37.36%，2026-06-22价格396.26美元高于6月3日收盘390.34美元",
            "两周仅+3.89%，高IV和大涨后估值拥挤提示过热风险",
        ),
        "激进短线": (
            "Call IV 73.2%、AI光互联/1.6T/ACC/3.2T多叙事和强近端验证，适合进攻资金",
            "高IV意味着利好预期拥挤，任何ASP、客户认证或backlog质量反证都会放大回撤",
        ),
    }

    opposition_text = (
        f"{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在低估值、现金流/防守、"
        "更硬RPO/订单或更大直接AI收入规模上压过 MTSI。"
        if strong_b_rows
        else "无达到“B胜出至少5列且净胜3列”的显著强反方；MTSI的劣势主要集中在估值、防守和少数同业右尾单列。"
    )

    out: list[str] = []
    out += [
        "# MTSI 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：MTSI / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 MTSI vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MTSI 的优势集中在近端催化、NTM兑现、右尾弹性、价格确认和激进短线；Q3 指引、record backlog、1.5x book-to-bill、Data Center高速模拟/光互联和I&D/GaN底座让它明显强于普通周期半导体。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 Forward PE `57.89`、P/S `28.15`、EV/EBITDA `126.01`、Call IV `73.2%`，以及 SOXX 压力窗口累计 `-44.86%`。",
        "- A 最适合的投资者画像：愿意为 AI 光互联模拟芯片、1.6T/ACC、3.2T/448G、CW laser/InP 和防务/GaN 的多线兑现付高估值的成长进攻型资金。",
        "- A 最不适合的投资者画像：优先买低估值、低波动、强防守回撤、或要求产品级客户/订单/backlog 完全披露后才进场的稳健资金。",
        f"- 多数思路下最强反方公司：{opposition_text}",
        "- 如果只追求更高增长、更好公司，A 的总体位置：MTSI 是项目内 AI 光互联/高速模拟链条中靠前的进攻配置，NTM和近端验证强于多数公司，但风险调整、估值消化和下行保护不是项目最优。",
        "- 后续最重要跟踪数据：FY2026Q3实际收入和GM、Q4/FY2027Q1指引、Data Center收入、I&D收入、book-to-bill、turns orders、record backlog质量、inventory/WIP、1.6T production volume、MACD-41804客户平台、448G driver qualification、IQE交易进展和SATCOM/LEO production program。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "MTSI"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "14.3-15.5亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "可收入化而不是需求池本身：需要证明 Q2 1.5x book-to-bill 和 record backlog 能在 Q3/Q4 转为收入，且 Data Center 增长不是低毛利 pass-through 或单客户拉货。"]),
        base.row(["最大反证", "产品级客户、订单、backlog金额、Data Center内部800G/1.6T/ACC/laser拆分未披露；若ASP连续下行、客户库存上升或Q4/FY2027H1指引保守，估值容错会快速下降。"]),
        base.row(["近端催化剂", "FY2026Q3实际与Q4指引、Data Center收入、book-to-bill与turns、1.6T production volume、MACD-41804客户平台、448G qualification、IQE交易和I&D/GaN项目进展。"]),
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
        base.row(["直接同业", "同属高速光模块/光器件、光模拟IC、InP/laser、线性光/铜互联或下一代3.2T链条，优先比较订单、客户认证、BOM份额、ASP、利润率和同业估值。", "COHR、LITE、AAOI、POET、LWLG", "同业证据权重最高；若一方在客户/订单/利润质量上明显更硬，结论力度可上调。"]),
        base.row(["相邻替代", "同处AI网络、高速互联、模拟/RF半导体、AI芯片、服务器或数据中心基础设施资金篮子，但产品不是直接替代。", "ALAB、CRDO、MRVL、AVGO、ADI、MXL、SMTC、ETN、VRT", "回答资金只能买一个时，谁的增长质量、估值消化和催化更好。"]),
        base.row(["上下游", "一方是MTSI客户、平台、DSP/交换芯片、连接器/测试/网络系统、服务器或云/AI集群需求端。", "NVDA、ANET、CIEN、CSCO、APH、TEL、MSFT、AMZN、DELL、SMCI", "强调利润捕获和议价权，不把下游收入规模或上游瓶颈自动等同胜出。"]),
        base.row(["跨赛道", "半导体材料、前道设备、封测、工业、化工、公用事业等与MTSI业务差异大，但作为项目内资金配置替代仍可比较。", "ASML、LIN、TMO、AEP、CAT、DHR", "默认降低结论力度；若成长、估值或防守证据互有强弱，优先中性或微倾向。"]),
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
        need = "需要 MTSI 披露更明确的1.6T/ACC/3.2T客户金额、backlog、ASP、产品级毛利和FCF改善，并证明高估值可被NTM利润消化。"
        if comparison["rel"] == "直接同业":
            need = "需要 MTSI 在同业中证明更强客户份额、1.6T/ACC出货、laser/InP供应、毛利率和可确认订单。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 MTSI 用更强收入兑现和现金流改善抵消跨赛道标的的低估值或防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]
    if not strong_b_rows:
        out.append(base.row([1, "无显著强反方", "无", "按 B 胜出至少5列且净胜3列的口径，没有公司在多数思路下明显强于 MTSI。", "继续跟踪MTSI估值、订单、客户和毛利率；若这些弱化，低估值防守股和更大AI右尾股会成为更强反方。"]))

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬NTM订单/利润兑现、同等AI主线右尾，或明显更好的估值消化和价格确认。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要 B 把防守优势转化为更高增长或明确催化，否则难以压过MTSI的AI光互联右尾和近端验证。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI网络_光互联_连接器/MTSI_MACOM_Technology_Solutions_公司调研_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_光DSP、TIA与CDR芯片_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_LPO_LRO线性光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_激光器、EML与光器件_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AEC、DAC与高速铜缆_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_OCS光路交换_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_mtsi_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+33%-44%` 做同号区间修正后建档；未读取下游量化目录、备份、临时目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 MTSI 正式评估文件")
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
                "mtsi_tiers": companies[TARGET]["tiers"],
                "mtsi_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
                "mtsi_ranks": companies[TARGET]["ranks"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
