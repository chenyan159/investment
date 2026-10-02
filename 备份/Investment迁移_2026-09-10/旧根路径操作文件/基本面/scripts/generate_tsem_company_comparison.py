from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "TSEM"
TARGET_NAME = "Tower Semiconductor"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "TSEM_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH
base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_FOUNDRY_PEERS = {"TSM", "GFS", "UMC", "INTC"}
SPECIALTY_ANALOG_IDM = {
    "ADI",
    "AOSL",
    "DIOD",
    "IFNNY",
    "MCHP",
    "MPWR",
    "ON",
    "POWI",
    "STM",
    "TXN",
    "VICR",
}
OPTICAL_NETWORK_CHAIN = {
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "NOK",
    "POET",
    "RMBS",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}
AI_COMPUTE_CUSTOMERS = {
    "AMD",
    "ARM",
    "BABA",
    "CDNS",
    "DELL",
    "GOOGL",
    "HPE",
    "IBM",
    "META",
    "MSFT",
    "NVDA",
    "ORCL",
    "QCOM",
    "SNPS",
    "SMCI",
}
WFE_SUPPLY_CHAIN = {
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
MATERIALS_SUPPLY_CHAIN = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "ENTG",
    "HOCPY",
    "LIN",
    "MTRN",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SOMMY",
}
PACKAGING_TEST_CHAIN = {
    "AEHR",
    "AMKR",
    "ASMVY",
    "ASX",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "IMOS",
    "KEYS",
    "KLIC",
    "MICLF",
    "ONTO",
    "TER",
}
SEMI_ADJACENT_CATS = {
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "半导体材料_化学品_基板",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
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

    peer_overrides = {
        "TSM": {
            "NTM兑现优先": 94.0,
            "右尾弹性优先": 84.0,
            "风险调整收益": 74.0,
            "下行保护优先": 70.0,
            "估值消化优先": 62.0,
            "近端催化优先": 76.0,
            "价格确认/动量": 84.0,
            "激进短线": 78.0,
        },
        "GFS": {
            "NTM兑现优先": 65.0,
            "右尾弹性优先": 65.0,
            "风险调整收益": 48.0,
            "下行保护优先": 48.0,
            "估值消化优先": 48.0,
            "近端催化优先": 62.0,
            "价格确认/动量": 84.0,
            "激进短线": 84.0,
        },
        "UMC": {
            "NTM兑现优先": 52.0,
            "右尾弹性优先": 36.0,
            "风险调整收益": 54.0,
            "下行保护优先": 63.0,
            "估值消化优先": 66.0,
            "近端催化优先": 40.0,
            "价格确认/动量": 45.0,
            "激进短线": 32.0,
        },
        "INTC": {
            "NTM兑现优先": 42.0,
            "右尾弹性优先": 56.0,
            "风险调整收益": 31.0,
            "下行保护优先": 33.0,
            "估值消化优先": 30.0,
            "近端催化优先": 50.0,
            "价格确认/动量": 46.0,
            "激进短线": 58.0,
        },
    }
    for ticker, scores in peer_overrides.items():
        if ticker in companies:
            companies[ticker]["scores"].update(scores)  # type: ignore[index,union-attr]

    companies[TARGET]["scores"] = {  # type: ignore[index]
        "NTM兑现优先": 86.0,
        "右尾弹性优先": 92.0,
        "风险调整收益": 57.0,
        "下行保护优先": 58.0,
        "估值消化优先": 47.0,
        "近端催化优先": 81.0,
        "价格确认/动量": 82.0,
        "激进短线": 95.0,
    }
    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_FOUNDRY_PEERS:
        return "直接同业"
    if ticker in WFE_SUPPLY_CHAIN or ticker in MATERIALS_SUPPLY_CHAIN:
        return "上下游"
    if ticker in AI_COMPUTE_CUSTOMERS or ticker in OPTICAL_NETWORK_CHAIN:
        return "上下游"
    if ticker in PACKAGING_TEST_CHAIN or ticker in SPECIALTY_ANALOG_IDM:
        return "相邻替代"
    if category == "晶圆制造_前道设备":
        return "直接同业"
    if category in {"半导体材料_化学品_基板", "封测_检测_计量_光罩"}:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有Q1/Q2指引、预付款和SiPho合同",
            "右尾弹性优先": "A硅光/1.6T/CPO右尾更直接",
            "风险调整收益": "A增长证据可抵部分估值风险",
            "下行保护优先": "A压力窗口表现和现金锚更好",
            "估值消化优先": "A收入利润上修可部分消化估值",
            "近端催化优先": "A Q2和客户合同验证更近",
            "价格确认/动量": "A一月涨幅和趋势确认更强",
            "激进短线": "A高IV叠加硅光重定价弹性",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO/订单兑现更硬",
            "右尾弹性优先": "B利润池或小基数右尾更大",
            "风险调整收益": "B估值/现金流/上行组合更好",
            "下行保护优先": "B低IV或现金流防守更稳",
            "估值消化优先": "B当前估值更容易消化",
            "近端催化优先": "B近端订单/产品事件更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B短线资金弹性更强",
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
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "TSEM 的SiPho/1.6T/CPO合同右尾比B更直接。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "TSEM 有Q2指引、客户预付款和2027 SiPho合同支撑NTM兑现。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 10:  # type: ignore[index,operator]
            return "TSEM 近月价格确认更强，且硅光催化仍未完全验证。"
        return "TSEM 的硅光收入化和近端催化略优，B 的反证不足以压过。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的当前估值和现金流更容易被NTM业绩消化。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的低波动、现金流或防守属性强于 TSEM。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的收入/RPO/订单兑现证据比 TSEM 更硬。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI利润池或小基数右尾大于 TSEM。"
    return f"{b['ticker']} 在多数投资思路下比 TSEM 更符合项目内资金配置目标。"


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
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["估值消化优先"] - a["scores"]["估值消化优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["右尾弹性优先"] - x["b"]["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
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
    latest_vs_june3 = ""
    try:
        latest_vs_june3 = f"，且6/23价格较6/3收盘约{(float(fin.get('price')) / float(mom2.get('latest_close')) - 1) * 100:+.2f}%"
    except Exception:
        latest_vs_june3 = ""
    daily_snapshot = (
        f"2026-06-23 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}{latest_vs_june3}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入4.136亿美元、Q2指引4.55亿美元±5%、RF Infrastructure占38%、客户预付款2.90亿美元和2027 SiPho合同13亿美元共同支撑",
            "收入确认仍受SiPho产能、良率、wafer-level optical test、客户验收和非AI底座抵消影响",
        ),
        "右尾弹性优先": (
            "SiPho PIC、SiGe/high-speed analog、1.6T、CPO/NPO/OCS、Gen3 BCD和2028收入/净利模型构成非线性上限",
            "极度乐观要求需求、客户捕获、产能、良率和利润率同时成立，NTM证据低于2027-2028远期锚",
        ),
        "风险调整收益": (
            "基准收入20.0-22.0亿美元、净利润3.8-5.0亿美元，预付款改善现金流质量，SOXX压力窗口相对强",
            "2026-06-23 P/S 20.48、Forward PE 48.65、Call IV 108.4%，且客户集中和履约义务会放大下行",
        ),
        "下行保护优先": (
            "客户预付款、传统成熟节点现金底座和2026-06-04三段SOXX压力窗口累计+1.94%提供相对缓冲",
            "高IV、高估值、SiPho交付义务和非AI底座周期使其不是低波动防守资产",
        ),
        "估值消化优先": (
            "若基准收入20.0-22.0亿美元、毛利率30%-34%、净利润3.8-5.0亿美元兑现，可部分解释高估值",
            "P/S 20.48和Forward PE 48.65已经要求乐观兑现，估值消化明显弱于低倍数现金流公司",
        ),
        "近端催化优先": (
            "Q2/Q3收入和毛利率、RF Infrastructure占比、客户advances、SiPho合同上修、Marvell 5M+ PIC、IQE InP和Gen3 BCD均可近端验证",
            "缺少逐客户订单和CPO/NPO repeat order披露，若Q2后环比增长或毛利率未跟上，催化会反向",
        ),
        "价格确认/动量": (
            "2026-06-03过去一月+22.89%，2026-06-23价格较6/3约继续上行，硅光合同后价格已确认主题",
            "过去两周仅+1.30%，高IV说明价格已包含较多右尾，后续需要基本面继续验证",
        ),
        "激进短线": (
            "Call IV 108.4%、Put IV 95.1%、SiPho/1.6T/CPO叙事、客户预付款和近端财报验证带来高进攻弹性",
            "短线进攻同时暴露于估值透支、合约兑现延迟、客户集中和光模块库存/ASP反证",
        ),
    }

    out: list[str] = []
    out += [
        "# TSEM 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：TSEM / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-23；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 TSEM vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/`、项目根 `tmp/` 或既有公司对比成品作为决策输入。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。TSEM 的相对优势集中在 SiPho/1.6T/CPO 右尾、Q1/Q2收入锚、客户预付款、2027 SiPho合同、近端财报/合同验证和高IV短线弹性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 2026-06-23 P/S 20.48、Forward PE 48.65、Call IV 108.4%，以及SiPho产能/良率/客户验收、2027合同折扣确认和传统成熟节点抵消风险。",
        "- A 最适合的投资者画像：愿意用高波动承接硅光特种代工重定价、看重1.6T/CPO/SiGe/BCD收入化、并能跟踪季度交付和客户预付款变化的进攻型成长资金。",
        "- A 最不适合的投资者画像：只要求低估值、低IV、强自由现金流防守、广泛客户分散，或不愿承担SiPho履约和光互联需求周期风险的稳健资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在AI主链利润池、RPO/backlog、低估值现金流、防守属性或更强价格确认上压过 TSEM。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：TSEM 对 {sum(1 for x in comparisons if x['final'] == 'A')}/{n - 1} 家公司多数思路占优，对 {sum(1 for x in comparisons if x['final'] == 'B')}/{n - 1} 家公司多数思路落后；它是项目内“硅光特种代工高右尾进攻资产”，但不是估值消化或低波动防守资产。",
        "- 后续最重要跟踪数据：2026Q2/Q3收入和毛利率；RF Infrastructure占比；客户advances/deferred revenue；SiPho合同是否上修；Fab 7/300mm/SiPho产能和工具安装；Marvell/NVIDIA/IQE/Scintil/OpenLight量产线索；Gen3 BCD design-in/LTA；1.6T出货、ASP、库存和客户验收周期。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "TSEM"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$2.00-2.20B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI optical demand 需转成 Tower SiPho/SiGe 客户订单、capacity reservation/prepayment、Fab/工具/良率/测试/封装、客户验收和收入确认；最窄环节是产能、良率、wafer-level optical test 和客户验收。"]),
        base.row(["最大反证", "2026H2收入停止环比增长、SiPho预付款转回或合同延期、1.6T出货低于300-500万只、光模块库存超过一季度需求、Power segment无法从Gen3 BCD转设计赢单。"]),
        base.row(["近端催化剂", "Q2/Q3收入和毛利率、RF Infrastructure占比、客户advances、SiPho合同上修、Marvell 5M+ coherent PIC、IQE InP供货、Gen3 BCD AI power design-in、1.6T/CPO客户验证。"]),
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
        base.row(["直接同业", "同属晶圆代工、特种工艺、成熟节点或IDM制造资金池，优先比较收入兑现、客户质量、产品mix、毛利率、capex、利用率、估值和AI相关收入真实占比。", "TSM、GFS、UMC、INTC、部分晶圆制造公司", "同业证据权重最高；若对手在先进制程、利用率、现金流或估值消化上明显更强，TSEM的硅光右尾不能自动胜出。"]),
        base.row(["相邻替代", "同属模拟/功率/特种工艺、封测测试或半导体制造投资篮子，但产品和利润池不完全重叠。", "ADI、ON、STM、TXN、IFNNY、AMKR、ATEYY、TER、CAMT", "回答资金只能买一个时，谁的增长质量、利润留存、估值消化和近端催化更好。"]),
        base.row(["上下游", "B 位于TSEM的设备/材料/封测供应链、AI芯片/光互联客户链或云/服务器终端需求端。", "ASML、AMAT、ENTG、MRVL、AVGO、COHR、LITE、AAOI、NVDA、MSFT、GOOGL", "不把下游AI capex或上游稀缺自动等同TSEM收入；重点看谁真正捕获利润池、议价权和可确认收入。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、DHR、CAT、RYCEY、公用事业和工业公司", "默认降低结论力度；除非增长质量、估值消化或下行保护明显拉开，否则使用中性或微倾向。"]),
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
        need = "需要 TSEM 证明SiPho/SiGe/BCD订单能在NTM内转收入和利润，同时用毛利率、FCF或回调后的估值降低高P/S和高IV反证。"
        if comparison["rel"] == "直接同业":
            need = "需要 TSEM 在同业中证明硅光/特种工艺收入化、毛利率和现金流强于B，并且当前估值没有透支。"
        elif comparison["rel"] == "上下游":
            need = "需要 TSEM 证明比该上下游公司更能捕获AI光互联利润池，而不是只承接制造环节执行风险。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 TSEM 用更强兑现或估值消化抵消跨赛道标的的现金流、防守或低波动优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更高NTM收入利润兑现、更强价格确认，或以更低估值和更好现金流抵消TSEM的硅光右尾。"
        if b["scores"]["估值消化优先"] > a["scores"]["估值消化优先"]:  # type: ignore[index,operator]
            need = "需要 B 把估值和现金流优势转成可见上修，并证明增长不会被周期或执行反证抵消。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/`、`特征量化/`、项目根 `tmp/` 或既有公司对比成品。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-23 金融快照写入 189 家；本次公司评估全集为 {n} 家，缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}；涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/TSEM_Tower Semiconductor_公司调研_2026-06-20.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_特种晶圆代工_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_硅光材料、光子材料与电光聚合物_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_tsem_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对TSEM的2026Q1/Q2收入锚、RF Infrastructure、SiPho预付款、2027 SiPho合同、Marvell coherent PIC、IQE InP、Gen3 BCD、CPO/NPO、估值、高IV、SOXX压力窗口和价格确认做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
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
                "tsem_tiers": companies[TARGET]["tiers"],
                "tsem_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
