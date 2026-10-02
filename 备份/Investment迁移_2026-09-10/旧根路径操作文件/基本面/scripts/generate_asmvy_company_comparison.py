from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "ASMVY"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ASMVY_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_BACKEND_PEERS = {
    "BESIY",
    "KLIC",
    "MICLF",
}
BACKEND_TEST_ADJACENT = {
    "AEHR",
    "ATEYY",
    "CAMT",
    "COHU",
    "FORM",
    "KEYS",
    "ONTO",
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
    "KLAC",
    "LRCX",
    "MKSI",
    "NVMI",
    "TOELY",
    "UCTT",
    "VECO",
}
SEMI_MATERIAL_CHAIN_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "半导体材料_化学品_基板",
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

    # ASMVY-specific calibration. The generic parser underweights the same-sign
    # revenue ranges such as +33%-45%, and it cannot fully capture the quality of
    # disclosed TCB/C2W/HBM4/1.6T orders. We lift NTM/catalyst evidence, but cap
    # valuation, risk-adjusted and downside scores for high PE, ADR/currency
    # warnings, missing forward PE/IV, and weak SOXX pressure-window behavior.
    target = companies[TARGET]
    overrides = {
        "NTM兑现优先": 82.0,
        "右尾弹性优先": 78.0,
        "风险调整收益": 52.0,
        "下行保护优先": 56.0,
        "估值消化优先": 50.0,
        "近端催化优先": 77.0,
        "价格确认/动量": 66.0,
        "激进短线": 86.0,
    }
    for strategy, score in overrides.items():
        target["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_BACKEND_PEERS:
        return "直接同业"
    if ticker in OSAT_MEMORY_FOUNDRY_CUSTOMERS or ticker in AI_DEMAND_CHAIN:
        return "上下游"
    if ticker in BACKEND_TEST_ADJACENT or ticker in SEMICAP_ADJACENT:
        return "相邻替代"
    if category == "封测_检测_计量_光罩":
        return "相邻替代"
    if category in SEMI_MATERIAL_CHAIN_CATS:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A订单/B2B/Q2指引更硬",
            "右尾弹性优先": "A有TCB和1.6T设备右尾",
            "风险调整收益": "A增长弹性可抵部分估值压力",
            "下行保护优先": "A净现金和低杠杆略胜",
            "估值消化优先": "A高增长可部分消化高PE",
            "近端催化优先": "A有Q2订单和TCB验证窗口",
            "价格确认/动量": "A近月价格确认更强",
            "激进短线": "A先进封装事件弹性更高",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现更硬",
            "右尾弹性优先": "B右尾更大或小基数更弹",
            "风险调整收益": "B估值和下行组合更好",
            "下行保护优先": "B现金流或压力期更稳",
            "估值消化优先": "B当前估值更易消化",
            "近端催化优先": "B近端订单/产品节点更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B高beta和资金关注更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "估值、安全和兑现证据接近"
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
        + a["scores"]["右尾弹性优先"] * 0.7
        + a["scores"]["风险调整收益"]
        + a["scores"]["近端催化优先"] * 0.7
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["右尾弹性优先"] * 0.7
        - b["scores"]["风险调整收益"]
        - b["scores"]["近端催化优先"] * 0.7
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "ASMVY 的Q2指引、B2B、C2W/HBM4/1.6T订单验证更近。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "ASMVY 的订单池和先进封装收入兑现路径更硬。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 10:  # type: ignore[index,operator]
            return "ASMVY 的TCB、photonics和SMT AI server右尾更清楚。"
        return "ASMVY 在订单兑现和近端先进封装催化上略胜，但估值仍需持续验证。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化难度明显低于 ASMVY。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的风险调整收益优于 ASMVY。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、估值或压力期韧性更好。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的右尾收入弹性或市值弹性强于 ASMVY。"
    return f"{b['ticker']} 在多数投资思路下比 ASMVY 更符合当前项目内配置目标。"


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


def fmt_num(value: object, precision: int = 2) -> str:
    if value is None:
        return "缺失"
    if isinstance(value, float):
        return f"{value:.{precision}f}"
    return str(value)


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
            x["b"]["scores"]["风险调整收益"] + x["b"]["scores"]["估值消化优先"] - a["scores"]["风险调整收益"] - a["scores"]["估值消化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["近端催化优先"] + a["scores"]["NTM兑现优先"] - x["b"]["scores"]["近端催化优先"] - x["b"]["scores"]["NTM兑现优先"],  # type: ignore[index,operator]
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
        f"2026-06-22 金融快照生成；ASMVY价格日期 {fin.get('price_date', '缺失')}，价格 {fmt_num(fin.get('price'))} 美元，"
        f"市值 {fmt_b(fin.get('market_cap_b'))}，TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"源字段P/S {fmt_num(fin.get('ps'))}（交易货币/财报货币不一致，P/S重算标记bad；公司调研2026-06-11口径约5.5x），"
        f"P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = []
    for product in a["products"][:8]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "FY2025继续经营收入`US$1.762bn`、2026Q1收入`US$507.9m`、订单`US$727.0m`、B2B`1.43`，Q2收入指引`US$540m-600m`",
            "高端设备仍需安装、客户验收和营运资本配合；Q1期末正式backlog未披露",
        ),
        "右尾弹性优先": (
            "TCB FY2025约`+146%`，C2S/C2W/AOR/HBM4订单可数，1.6T photonics收入约5倍，极度乐观收入可到`US$3.30-3.80bn`",
            "CPO/NPO、HBM4 16H和hybrid bonding大规模仍是远期期权，客户多供和竞争限制独占右尾",
        ),
        "风险调整收益": (
            "基准收入`US$2.35-2.55bn`、毛利率`40%-42%`，SEMI mix改善带来利润杠杆，资产负债表净现金",
            "2026-06-22 TTM PE约`79.93`、Forward PE缺失，ADR/币种警示和压力窗口回撤削弱赔率",
        ),
        "下行保护优先": (
            "2025年末现金及银行存款约`HK$5.676bn`、净现金约`HK$3.28bn`、流动比率约`3.58x`",
            "设备周期、高估值和SOXX三段压力窗口累计约`-62.14%`说明市场压力期不防守",
        ),
        "估值消化优先": (
            "若Q2/Q3订单继续高于收入且SEMI GM维持mid-40s，NTM业绩可以部分吸收估值",
            "当前估值已反映AI先进封装预期，Forward PE/IV缺失且P/S存在ADR币种错配警示",
        ),
        "近端催化优先": (
            "Q2实际收入/订单、C2W 8台repeat order、HBM4 16H/AOR qualification、1.6T photonics、SMT战略选项均在1-2季内可验证",
            "若Q2低于指引、H2 B2B低于1或SMT订单无法转收入，催化会反向释放",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周`+3.06%`、过去一月`+11.84%`，2026-06-22价格`79.93`较6月初继续上行",
            "正式区间涨跌口径停在2026-06-03，且相对AI主链高动量公司并非顶档",
        ),
        "激进短线": (
            "先进封装、HBM4、C2W、1.6T和SMT价值释放具备高事件弹性，短线容易被订单新闻重新定价",
            "ASMVY为OTC ADR且期权链/IV缺失，流动性和风险控制弱于美股主线高beta标的",
        ),
    }

    out: list[str] = []
    out += [
        "# ASMVY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：ASMVY / ASMPT",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22金融快照；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 ASMVY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ASMVY 的相对优势集中在订单兑现和近端催化：2026Q1 B2B 1.43、Q2指引、C2W/HBM4/AOR/1.6T 订单链条使它不是纯主题映射。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值消化、下行保护和风险调整收益：当前价格已经提前反映 AI 先进封装预期，且 ADR/币种、Forward PE、IV 和压力窗口数据均需折扣。",
        "- A 最适合的投资者画像：愿意承受半导体设备周期和估值波动、重点押注先进封装/HBM/1.6T 光子封装订单兑现和未来1-2季财报验证的进攻型中期资金。",
        "- A 最不适合的投资者画像：要求低估值、强现金流防守、低波动、或希望在SOXX压力期有明确下行保护的稳健配置者。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在估值消化、风险调整、下行保护或更大AI主线右尾上压过 ASMVY。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：ASMVY 是项目内靠前的先进封装设备弹性标的，但不是全风格最优；在NTM兑现和近端事件上强，在估值/下行保护上弱。",
        "- 后续最重要跟踪数据：Q2 2026 实际收入和订单、Q2/Q3 B2B、SEMI/SMT收入与GM、TCB台数和客户类型、HBM4 16H/AOR qualification、1.6T photonics收入、SMT战略选项、backlog、存货、应收和自由现金流。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ASMVY"]),
        base.row(["公司名称", "ASMPT"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`US$2.35bn-2.55bn`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "高端TCB精密部件、AOR/plasma模块、客户厂务安装、客户验收、光子贴装良率、SMT战略评估期间交付稳定性和营运资本周转。"]),
        base.row(["最大反证", "当前估值已经反映AI先进封装重估；产品级backlog/取消率未披露，SMT毛利率低，2025Q3有非核心订单取消样本，SOXX压力窗口累计回撤大。"]),
        base.row(["近端催化剂", "2026Q2实际收入/订单、Q2/Q3 B2B、C2W/HBM4/AOR/1.6T订单继续披露、SEMI GM维持mid-40s、SMT战略选项公告。"]),
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
        base.row(["直接同业", "与ASMVY在后道封装、TCB/die attach、hybrid bonding、SMT或先进封装设备需求池重叠，优先比较订单、份额、产品代际、客户认证、毛利率和估值。", "BESIY、KLIC、MICLF", "同业证据权重最高；若对方在TCB/HB、订单或估值消化上明显更强，会直接压低ASMVY结论。"]),
        base.row(["相邻替代", "同属半导体设备、测试、封测、AI基础设施或高beta设备资金篮子，但产品不完全竞争；回答资金只能买一个时谁的增长质量和赔率更好。", "ATEYY、TER、CAMT、ONTO、AMAT、ASML、KLAC、LRCX、VRT、ETN", "默认看订单兑现、右尾、估值消化和近端催化；不因设备赛道更热自动胜出。"]),
        base.row(["上下游", "B 是ASMVY设备服务的OSAT、foundry、IDM、HBM/存储、AI芯片、光模块、服务器或云需求端，重点看谁捕获利润池和谁的收入确认更硬。", "AMKR、ASX、TSM、MU、NVDA、AVGO、CRDO、SMCI、MSFT", "不把下游AI收入规模直接等同ASMVY机会，重点比较利润捕获、议价权、订单和估值。"]),
        base.row(["跨赛道", "业务差异较大，只作为项目内资金配置替代比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、CAT、RYCEY、RKLB", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 ASMVY 把TCB/HBM4/1.6T订单连续转成收入、利润和现金流，并让估值倍数随业绩兑现下行。"
        if comparison["rel"] == "直接同业":
            need = "需要 ASMVY 在TCB/HB/SMT关键客户、份额和利润率上拿出强于直接同业的新增证据。"
        elif "下行保护优先" in wins or "风险调整收益" in wins:
            need = "需要 ASMVY 证明高估值下仍有足够下行边界，并改善压力期回撤和营运资本反证。"
        elif "估值消化优先" in wins:
            need = "需要 ASMVY 用连续收入/利润上修和Forward PE修复来消化当前AI设备预期。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/backlog、近端催化或价格确认，并降低收入兑现与估值反证。"
        if b["scores"]["估值消化优先"] > a["scores"]["估值消化优先"]:  # type: ignore[index,operator]
            need = "需要 B 把估值优势转化成更强增长兑现，否则ASMVY的近端订单弹性仍更有吸引力。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家，本次公司评估全集为 {n} 家；缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/封测_检测_计量_光罩/ASMVY_ASMPT_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_asmvy_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对ASMVY的同号百分比区间、TCB/C2W/HBM4/1.6T订单证据、ADR/币种警示、Forward PE/IV缺失和压力窗口回撤做人工校准后建档。",
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
                "asmvy_tiers": companies[TARGET]["tiers"],
                "asmvy_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
