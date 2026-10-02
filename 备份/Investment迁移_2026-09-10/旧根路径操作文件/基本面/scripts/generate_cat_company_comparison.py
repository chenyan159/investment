from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "CAT"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CAT_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_POWER_PEERS = {"CMI", "GEV", "GNRC", "PSIX", "RYCEY"}
ONSITE_POWER_SUBSTITUTES = {"BE", "FCEL", "SMR", "OKLO", "VST", "CEG"}
POWER_INFRA_ADJACENT = {
    "ABBNY",
    "AEIS",
    "AEP",
    "AMPX",
    "CARR",
    "DKILY",
    "DOV",
    "EME",
    "ENS",
    "ENPH",
    "ETN",
    "ETR",
    "FIX",
    "FLNC",
    "HUBB",
    "HTHIY",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "NVT",
    "PH",
    "POWI",
    "POWL",
    "PWR",
    "TT",
    "VICR",
    "VRT",
}
DOWNSTREAM_AI_LOAD = {
    "AMZN",
    "APLD",
    "BABA",
    "CRWV",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
    "PENG",
    "SANM",
    "SMCI",
}
UPSTREAM_FUEL_AND_GRID = {"APD", "DTE", "ET", "LIN"}
INDUSTRIAL_ADJACENT = {"DCI", "FTV", "MMM", "NDSN", "TDY", "TMO", "DHR", "ECL"}


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
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    # CAT calibration: formal evaluation gives unusually hard NTM evidence
    # through Q1 revenue, FY2026 guidance, $63B backlog, PG +41%, AIP 2GW,
    # and strong FCF. The caps are high current valuation, cyclicality in CI/RI,
    # and the fact that direct AI data center revenue is not separately disclosed.
    target = companies[TARGET]
    overrides = {
        "NTM兑现优先": 86.0,
        "右尾弹性优先": 78.0,
        "风险调整收益": 62.0,
        "下行保护优先": 71.0,
        "估值消化优先": 57.0,
        "近端催化优先": 76.0,
        "价格确认/动量": 76.0,
        "激进短线": 77.0,
    }
    for strategy, score in overrides.items():
        target["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_POWER_PEERS:
        return "直接同业"
    if ticker in ONSITE_POWER_SUBSTITUTES or ticker in POWER_INFRA_ADJACENT:
        return "相邻替代"
    if ticker in DOWNSTREAM_AI_LOAD or ticker in UPSTREAM_FUEL_AND_GRID:
        return "上下游"
    if category in {"电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI", "配电_电源_功率器件"}:
        return "相邻替代"
    if ticker in INDUSTRIAL_ADJACENT:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有$63B backlog和PG收入锚",
            "右尾弹性优先": "A自备电GW订单右尾更实",
            "风险调整收益": "A现金流和订单抵部分估值",
            "下行保护优先": "A盈利FCF和服务网络更稳",
            "估值消化优先": "A增长和现金流可部分消化估值",
            "近端催化优先": "AIP交付和PG订单节点更近",
            "价格确认/动量": "A两周和一月趋势已确认",
            "激进短线": "A AI电力叙事叠加IV更强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入或利润兑现更短链",
            "右尾弹性优先": "B右尾规模或小基数更大",
            "风险调整收益": "B估值现金流组合更均衡",
            "下行保护优先": "B估值或现金流缓冲更厚",
            "估值消化优先": "B当前估值消化压力更低",
            "近端催化优先": "B近端订单或产品节点更硬",
            "价格确认/动量": "B价格确认和资金偏好更强",
            "激进短线": "B高beta短线弹性更强",
        }[strategy]
    if rel == "直接同业":
        return "同业订单和估值接近"
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
        a["scores"]["NTM兑现优先"] * 1.0
        + a["scores"]["风险调整收益"] * 1.1
        + a["scores"]["估值消化优先"] * 0.9
        + a["scores"]["右尾弹性优先"] * 0.8
        + a["scores"]["近端催化优先"] * 0.7
        + a["scores"]["下行保护优先"] * 0.7
        - b["scores"]["NTM兑现优先"] * 1.0
        - b["scores"]["风险调整收益"] * 1.1
        - b["scores"]["估值消化优先"] * 0.9
        - b["scores"]["右尾弹性优先"] * 0.8
        - b["scores"]["近端催化优先"] * 0.7
        - b["scores"]["下行保护优先"] * 0.7
    )
    return "A" if weighted >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "CAT 的Q1收入、$63B backlog、PG高增和AIP 2GW让NTM兑现更硬。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "CAT 的AIP交付、PG订单和FY2026上修更可能在近端验证。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
            return "CAT 的盈利、FCF、经销商网络和服务收入提供更强防守底座。"
        return "CAT 以可见订单、现金流和AI电力需求捕获略胜，但估值仍需兑现。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 16:  # type: ignore[index,operator]
        ticker = str(b["ticker"])
        category = str(b["category"])
        if category in HIGH_GROWTH_CATS:
            return f"{ticker} 的AI主链、光互联、芯片或云算力右尾比CAT更短链。"
        if category in INFRA_CATS or ticker in ONSITE_POWER_SUBSTITUTES:
            return f"{ticker} 的小基数电力/基础设施右尾和重定价弹性强于CAT。"
        return f"{ticker} 的非线性增长右尾明显大于CAT。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 更容易用NTM业绩消化估值，CAT已要求强执行。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的上行/估值/现金流组合比CAT更均衡。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和短线资金偏好强于CAT。"
    return f"{b['ticker']} 在多数投资思路下比CAT更符合当前配置目标。"


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
            a["scores"]["NTM兑现优先"] + a["scores"]["近端催化优先"] + a["scores"]["下行保护优先"] - x["b"]["scores"]["NTM兑现优先"] - x["b"]["scores"]["近端催化优先"] - x["b"]["scores"]["下行保护优先"],  # type: ignore[index,operator]
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
    product_names = [str(product[0]).split("，")[0].split("；")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入$17.415B同比+22%，FY2026低双位数增长指引，backlog约$63B同比+79%，Power Generation外部销售$2.817B同比+41%",
            "AI数据中心收入未单列，NTM仍受许可、燃气、BESS/开关设备、经销商commissioning和验收约束",
        ),
        "右尾弹性优先": (
            "AIP 2GW、PROPWR多年框架、六个1GW+ prime power协议和2030 Power Generation >3x目标提供AI电力右尾",
            "公司基数大，Monarch/PROPWR/2030目标多数不是NTM收入，极度乐观需要CI/RI不拖累",
        ),
        "风险调整收益": (
            "基准收入$76-80B、调整后经营利润$14.0-15.6B，MP&E FCF方向高于2025，需求和现金流都可见",
            "2026-06-22 Forward PE 33.95、P/S 6.65、EV/EBITDA 33.93，关税$2.2-2.4B和周期风险压低赔率",
        ),
        "下行保护优先": (
            "盈利、服务/后市场、Cat Financial、全球经销商网络和订单backlog给出比高beta AI链更好的防守底座",
            "压力窗口累计-41.20%，估值已抬升，CI库存和RI利润率仍有周期反证",
        ),
        "估值消化优先": (
            "若PG高增和FCF高于2025兑现，NTM利润能部分消化高倍数",
            "当前估值已要求强执行，基准增长+12%-18%不足以像低估值工业股那样轻松消化",
        ),
        "近端催化优先": (
            "2026H2 AIP交付窗口、PG收入/零售、backlog、FY2026上修、关税转嫁和P&E margin都是1-2季可验证节点",
            "催化依赖交付链，任何permit/gas/commissioning延迟都会削弱重定价",
        ),
        "价格确认/动量": (
            "正式区间文件显示两周+6.15%、一月+4.10%，2026-06-22价格继续高于6月初锚点，资金已确认AI电力重估",
            "不是最高动量标的，强势价格也提高了估值透支风险",
        ),
        "激进短线": (
            "Call IV 42.4%、AI数据中心自备电、GW级订单和工业龙头重估提供短线进攻性",
            "短线爆发力低于BE、PSIX、VRT、AI芯片/光互联等更高beta标的",
        ),
    }

    out: list[str] = []
    out += [
        "# CAT 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：CAT / Caterpillar Inc",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 CAT vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。CAT 的优势集中在 NTM 兑现、近端催化、价格确认和较好的下行保护：它不是 AI 芯片公司，但已经用 Power Generation 收入、backlog 和 AIP 2GW 把 AI 电力瓶颈转成可收入化证据。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是公司体量大、当前估值已经重估、直接 AI 数据中心收入未单列，且 Construction/Resource 仍有周期和利润率反证。",
        "- A 最适合的投资者画像：希望配置 AI 数据中心电力瓶颈，但不想只买亏损小盘或纯远期主题，愿意用中高估值买真实收入表、backlog、FCF和全球服务网络的资金。",
        "- A 最不适合的投资者画像：只追求最高右尾、最强短线 beta、最低估值或纯半导体/云算力主链弹性的投资者。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在AI主链右尾、小基数弹性、估值消化、软件/半导体利润率或短线动量上比CAT更强。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：CAT 属于项目内高质量 AI 物理电力供应链龙头，NTM 兑现强于多数公司，右尾和短线进攻低于高beta AI主链；总体是强配置但不是全项目最高弹性标的。",
        "- 后续最重要跟踪数据：Power Generation外部销售、P&E零售统计、P&E margin、backlog/订单、AIP交付/commissioning、PROPWR滚动订单、large recip capacity扩产、MP&E FCF、关税成本、CI终端销售、RI利润率、Cat Financial past dues和数据中心客户PO。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "CAT"]),
        base.row(["公司名称", "Caterpillar Inc"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$76-80B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "从GW级客户需求到CAT NTM可确认收入：空气许可、燃气接入、BESS/开关设备/变压器、经销商commissioning、融资、验收和交付节奏。"]),
        base.row(["最大反证", "CAT未单列AI数据中心收入，Power Generation高增不能全部归因于AI；关税成本、CI库存建设、RI利润率和周期需求会抵消部分上行。"]),
        base.row(["近端催化剂", "2026H2 AIP交付启动、Power Generation外部销售/零售继续高增、backlog和订单延续、P&E margin、FY2026指引、FCF和关税转嫁。"]),
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
        base.row(["直接同业", "与 CAT 在数据中心 genset、prime/bridge power、燃机/发动机、工业动力或全球服务网络上争夺同一需求池。", "CMI、GEV、GNRC、PSIX、RYCEY", "优先看MW/GW订单、backlog、交付窗口、服务网络、利润率和估值；同业证据强时可以放大判断力度。"]),
        base.row(["相邻替代", "同属 AI 数据中心电力、配电、储能、冷却、工程、能源安全或工业基础设施资金篮子，但产品不完全重叠。", "BE、FCEL、ETN、VRT、PWR、POWL、TT、AAON、CARR、JCI、SMR、OKLO", "回答资金只能买一个时谁的增长质量、利润捕获、估值消化和近端催化更好。"]),
        base.row(["上下游", "B 是AI负荷端、云/IDC资本开支端、公用事业、燃气/工业气体/电网供给端，影响 CAT 电力订单但不等同于 CAT 收入。", "MSFT、AMZN、GOOGL、META、ORCL、EQIX、CRWV、AEP、ET、LIN、APD", "区分下游收入规模和上游设备利润捕获，重点看议价权、项目路径和现金流质量。"]),
        base.row(["跨赛道", "半导体、设备、材料、软件、工业和消费平台等与 CAT 业务差异大，但作为项目内资金配置替代仍可比较。", "NVDA、AVGO、TSM、ASML、MU、CDNS、BABA", "默认降低结论力度；只有增长质量、估值消化、下行保护或价格确认明显拉开时才给建议/强烈建议。"]),
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
        need = "需要CAT披露更多可确认AI数据中心收入、客户PO、交付节奏和利润率，并证明高估值可由基准业绩消化。"
        if "右尾弹性优先" in wins or "激进短线" in wins:
            need = "需要CAT把AIP/PROPWR/1GW+协议转成更密集的NTM收入和利润上修，否则右尾仍弱于高beta标的。"
        if "估值消化优先" in wins or "风险调整收益" in wins:
            need = "需要CAT用PG增长、FCF和关税转嫁证明当前倍数不是只靠乐观情景支撑。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B拿出同等强度的订单/backlog、收入兑现、FCF和近端催化证据。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入/利润，并降低估值、现金流或执行反证。"
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
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/机电_冷却_工程_水处理_边缘工业AI/CAT_Caterpillar_Inc_公司调研_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_动态UPS、飞轮与超级电容_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_cat_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对CAT的Q1收入、$63B backlog、Power Generation高增、AIP 2GW、FCF、估值、周期风险和AI收入未单列限制做人工校准后建档；未读取下游量化目录或现成排序结论。",
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
                "cat_tiers": companies[TARGET]["tiers"],
                "cat_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
