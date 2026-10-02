from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "TER"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "TER_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_TEST_PEERS = {"ATEYY", "COHU", "AEHR"}
TEST_ADJACENT = {
    "ASMVY",
    "BESIY",
    "CAMT",
    "FORM",
    "KEYS",
    "KLIC",
    "MICLF",
    "ONTO",
    "PLAB",
    "TDY",
    "TMO",
    "VIAV",
}
AI_SOC_MEMORY_CUSTOMERS = {
    "ADI",
    "ALAB",
    "AMD",
    "AMKR",
    "ARM",
    "ASX",
    "AVGO",
    "CDNS",
    "CRDO",
    "DELL",
    "GFS",
    "GOOGL",
    "HPE",
    "IMOS",
    "INTC",
    "JBL",
    "META",
    "MRVL",
    "MSFT",
    "MU",
    "NVDA",
    "ORCL",
    "QCOM",
    "RMBS",
    "SANM",
    "SIMO",
    "SMCI",
    "SNDK",
    "SNPS",
    "STX",
    "TSM",
    "UMC",
    "WDC",
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
SEMI_CHAIN_CATS = {
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

    # Direct peer calibration from the same formal company-evaluation layer.
    # This avoids treating ATEYY as a generic B when it is TER's closest ATE peer.
    peer_overrides = {
        "ATEYY": {
            "NTM兑现优先": 88.0,
            "右尾弹性优先": 86.0,
            "风险调整收益": 61.0,
            "下行保护优先": 49.0,
            "估值消化优先": 55.0,
            "近端催化优先": 75.0,
            "价格确认/动量": 71.0,
            "激进短线": 78.0,
        },
    }
    for ticker, scores in peer_overrides.items():
        if ticker in companies:
            companies[ticker]["scores"].update(scores)  # type: ignore[index,union-attr]

    # TER target calibration: high-quality AI/HBM tester exposure, but high valuation and weak pressure-window defense.
    companies[TARGET]["scores"] = {  # type: ignore[index]
        "NTM兑现优先": 84.0,
        "右尾弹性优先": 91.0,
        "风险调整收益": 52.0,
        "下行保护优先": 43.0,
        "估值消化优先": 55.0,
        "近端催化优先": 72.0,
        "价格确认/动量": 88.0,
        "激进短线": 95.0,
    }
    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_TEST_PEERS:
        return "直接同业"
    if ticker in AI_SOC_MEMORY_CUSTOMERS:
        return "上下游"
    if ticker in TEST_ADJACENT or ticker in SEMICAP_ADJACENT or category == "封测_检测_计量_光罩":
        return "相邻替代"
    if category in SEMI_CHAIN_CATS:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A SoC/HBM收入锚和Q2指引更硬",
            "右尾弹性优先": "A AI测试内容右尾更直接",
            "风险调整收益": "A上行能覆盖部分高估值",
            "下行保护优先": "A盈利质量略胜但非防守",
            "估值消化优先": "A高增可部分消化估值",
            "近端催化优先": "A SoC/HBM/KGD节点更近",
            "价格确认/动量": "A价格确认和资金强度更高",
            "激进短线": "A高IV和AI tester题材更利进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现更硬",
            "右尾弹性优先": "B右尾或市值弹性更大",
            "风险调整收益": "B风险调整赔率更好",
            "下行保护优先": "B现金流或压力期更稳",
            "估值消化优先": "B估值更容易消化",
            "近端催化优先": "B近端订单/产品节点更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B短线beta或题材更强",
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
        + a["scores"]["右尾弹性优先"] * 0.75
        + a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"] * 0.45
        + a["scores"]["近端催化优先"] * 0.65
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["右尾弹性优先"] * 0.75
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"] * 0.45
        - b["scores"]["近端催化优先"] * 0.65
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "TER 的 SoC/HBM 测试收入锚、Q2指引和高毛利 mix 更硬。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "TER 的 AI SoC/HBM/KGD/光电测试内容上修空间更直接。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
            return "TER 的六月价格确认和高波动进攻属性更强。"
        return "TER 在 AI 测试兑现、右尾和近端催化上略胜，但估值和回撤仍需折扣。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、估值或压力期韧性明显好于 TER。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化难度明显低于 TER。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的风险调整收益优于 TER。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据强于 TER。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的右尾收入弹性或市值弹性强于 TER。"
    return f"{b['ticker']} 在多数投资思路下比 TER 更符合当前项目内配置目标。"


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
            x["b"]["scores"]["下行保护优先"]
            + x["b"]["scores"]["估值消化优先"]
            - a["scores"]["下行保护优先"]
            - a["scores"]["估值消化优先"],
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["NTM兑现优先"]
            + a["scores"]["右尾弹性优先"]
            + a["scores"]["近端催化优先"]
            + a["scores"]["价格确认/动量"] * 0.5
            - x["b"]["scores"]["NTM兑现优先"]
            - x["b"]["scores"]["右尾弹性优先"]
            - x["b"]["scores"]["近端催化优先"]
            - x["b"]["scores"]["价格确认/动量"] * 0.5,
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

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:8]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 金融快照生成；TER价格日期 {fin.get('price_date', '缺失')}，价格 {fmt_num(fin.get('price'))} 美元，"
        f"市值 {fmt_b(fin.get('market_cap_b'))}，TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    support = {
        "NTM兑现优先": (
            "2026Q1收入12.825亿美元、同比+87%，2026Q2收入指引中点12.0亿美元；NTM基准收入48.5-53.0亿美元、经营利润率34%-38%",
            "不披露完整 bookings/backlog；官方RPO仅覆盖原始期限超过一年的合同，不能直接外推需求池",
        ),
        "右尾弹性优先": (
            "乐观/极度乐观收入55.5-61.5/63.5-71.0亿美元；AI SoC/GPU/ASIC、HBM、KGD/SLT、高速I/O和光电测试内容均有上修路径",
            "市值已经不小，极度乐观需要多条测试链路同时量产且客户加单，不能只靠AI capex叙事",
        ),
        "风险调整收益": (
            "高毛利Semi Test mix、基准现金流为正，若SoC/HBM持续强可抵部分高估值压力",
            "2026-06-22 Forward PE 48.09、P/S 18.89、EV/EBITDA 58.88、IV约83%，风险调整收益被估值和波动显著扣分",
        ),
        "下行保护优先": (
            "盈利为正、现金流为正，高端测试客户粘性和产品替代门槛提供一定底座",
            "SOXX三段压力窗口累计-72.43%，高IV和高估值说明行业压力期防守属性弱",
        ),
        "估值消化优先": (
            "NTM基准收入较最近四个季度约+28%-40%，经营利润率显著上行，业绩高增可部分消化估值",
            "当前估值已明显要求乐观兑现，若SoC/HBM收入从Q1高位回落，消化难度会快速上升",
        ),
        "近端催化优先": (
            "Q2指引、SoC/Memory分部连续披露、HBM4/KGD/SLT、TEL Prexa SDP集成方案、Photon 100/1.6T光电测试均有未来1-2季验证点",
            "催化多依赖客户订单、交付和验收，若公司不披露订单口径，市场只能用收入和指引后验确认",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+18.97%、一月+18.60%，6月22日收盘457.00美元继续高于区间涨跌表的409.67美元",
            "上涨伴随高IV和高估值，动量强但也容易在预期反转时放大回撤",
        ),
        "激进短线": (
            "AI tester、HBM4、KGD/SLT、CPO/光电测试叙事集中，期权IV高且价格强，适合更激进的短期进攻",
            "短线已经拥挤，若Q2/Q3指引未继续上修或同业订单更强，回撤会很快",
        ),
    }

    out: list[str] = []
    out += [
        "# TER 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：TER / Teradyne",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22金融快照；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 TER vs 公司 B 的二选一判断；未读取、引用或继承 `特征量化/`、现成排序、备份、tmp 或既有公司对比成品作为决策输入。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。TER 的优势集中在 AI SoC/HBM 测试收入锚、极度乐观测试内容上修、近端产品/客户验证和价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是高估值、高 IV、SOXX 压力窗口回撤深，以及没有完整 bookings/backlog 口径。",
        "- A 最适合的投资者画像：能承受高波动和高估值，愿意押注未来 1-2 季 AI SoC、HBM、KGD/SLT 和高速光电测试继续收入化的进攻型中期资金。",
        "- A 最不适合的投资者画像：要求低估值、强下行保护、低 IV 或在半导体压力期有防守属性的稳健配置者。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在估值消化、下行保护、风险调整收益或更硬订单/backlog 上压过 TER。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：TER 是项目内靠前的 AI 半导体测试瓶颈资产，但不是全风格最优；它更适合进攻仓位，不适合作为防守或低估值核心仓位。",
        "- 后续最重要跟踪数据：TER 季度 SoC/Memory/Product Test/Robotics 收入、Q3/Q4 指引、AI相关收入比例、毛利率和经营利润率、经营现金流与库存/应收、是否新增完整订单或 backlog 口径、Magnum 7H/HBM4、TEL Prexa SDP/KGD、Photon 100/1.6T光电客户，以及 Advantest/FormFactor/Cohu/Aehr 同业订单和交期。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "TER"]),
        base.row(["公司名称", "Teradyne"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "48.5-53.0 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI芯片/HBM/先进封装测试需求很强，但公司不披露完整backlog/bookings；NTM只能用已确认收入、Q2指引、产品线收入和客户量产节奏折扣收入化。"]),
        base.row(["最大反证", "当前估值已经反映大量乐观预期；客户集中、多供压价、测试产能消化、传统测试周期和Robotics利润质量都可能抵消AI测试增量。"]),
        base.row(["近端催化剂", "Q2/Q3指引、SoC和Memory分部收入、HBM4验证、Magnum 7H、TEL Prexa SDP/KGD方案、Photon 100/1.6T光电测试、同业ATE/SLT订单。"]),
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
        base.row(["直接同业", "与 TER 在 ATE、AI SoC/HBM测试、SLT/burn-in 或测试cell需求池高度重叠，优先比较份额、订单、收入兑现、毛利率、产品代际、客户质量和同业估值。", "ATEYY、COHU、AEHR", "同业证据权重最高；若对手在订单、毛利率或估值消化上明显更硬，会直接压低 TER 结论。"]),
        base.row(["相邻替代", "同属半导体设备、后道封装测试、探针卡/检测量测或AI基础设施资金篮子，但产品不完全竞争；回答资金只能买一个时谁的增长质量和赔率更好。", "FORM、CAMT、ONTO、KEYS、ASML、AMAT、KLAC、VRT、ETN", "默认看订单兑现、右尾、估值消化和近端催化；不因设备赛道更热自动胜出。"]),
        base.row(["上下游", "B 是 TER 设备需求端、客户链、供应链或利润池相邻环节，重点看谁捕获利润池、议价权、订单和估值。", "TSM、MU、NVDA、AMD、AVGO、MRVL、AMKR、ASX、GFS、MSFT、META", "不把下游AI收入规模直接等同 TER 机会，重点比较利润捕获、客户集中、订单和估值消化。"]),
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
        need = "需要 TER 用连续分部收入/利润上修、订单或book-to-bill和现金流转换证明高估值可持续。"
        if comparison["rel"] == "直接同业":
            need = "需要 TER 在SoC/HBM tester份额、订单、毛利率和估值消化上拿出强于直接同业的新增证据。"
        elif "下行保护优先" in wins or "风险调整收益" in wins:
            need = "需要 TER 证明高估值下仍有足够下行边界，并改善压力期回撤和高IV反证。"
        elif "估值消化优先" in wins:
            need = "需要 TER 用FY2026/FY2027收入和利润连续上修来压低Forward PE和P/S。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/backlog、收入和利润上修、或更直接AI需求收入化证据。"
        if b["scores"]["估值消化优先"] > a["scores"]["估值消化优先"]:  # type: ignore[index,operator]
            need = "需要 B 把估值优势转化成更强增长兑现，否则TER的测试瓶颈、近端催化和价格确认仍更有吸引力。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取、引用或继承 `特征量化/`、`分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/` 或既有公司对比成品。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家，本次公司评估全集为 {n} 家；缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/封测_检测_计量_光罩/TER_Teradyne_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_探针卡、ATE与系统级测试_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体检测量测设备_2026-06-11.md`、`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_ter_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对TER的Q1/Q2收入锚、SoC/HBM/KGD/SLT/光电测试机会、缺backlog、Forward PE/P/S/IV、区间涨跌和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
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
                "ter_tiers": companies[TARGET]["tiers"],
                "ter_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
