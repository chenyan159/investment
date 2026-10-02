from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base
import generate_camt_company_comparison as range_fix


TARGET = "FORM"
TARGET_NAME = "FormFactor"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "FORM_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_TEST_PEERS = {
    "AEHR",
    "ATEYY",
    "CAMT",
    "COHU",
    "KEYS",
    "KLAC",
    "NVMI",
    "ONTO",
    "TER",
    "TMO",
}
PACKAGING_TEST_ADJACENT = {
    "AMKR",
    "ASMVY",
    "ASX",
    "BESIY",
    "DSCSY",
    "IMOS",
    "KLIC",
    "MICLF",
    "PLAB",
    "TDY",
}
AI_MEMORY_LOGIC_CUSTOMERS = {
    "ALAB",
    "AMD",
    "ARM",
    "AVGO",
    "CDNS",
    "GFS",
    "GOOGL",
    "INTC",
    "META",
    "MRVL",
    "MSFT",
    "MU",
    "NVDA",
    "QCOM",
    "RMBS",
    "SNDK",
    "SNPS",
    "STX",
    "TSEM",
    "TSM",
    "UMC",
    "WDC",
}
AI_NETWORK_SYSTEMS = {
    "AAOI",
    "ANET",
    "APH",
    "CIEN",
    "COHR",
    "CRDO",
    "DELL",
    "FN",
    "HPE",
    "LITE",
    "SMCI",
}
SEMICAP_ADJACENT = {
    "ACLS",
    "ACMR",
    "AEIS",
    "AMAT",
    "ASMIY",
    "ASML",
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


def post_june3_momentum(company: dict[str, object]) -> float | None:
    fin = company["fin"]  # type: ignore[assignment]
    mom2 = company["mom2"]  # type: ignore[assignment]
    price = fin.get("price") if fin else None
    base_close = mom2.get("latest_close") if mom2 else None
    if not price or not base_close:
        return None
    return (float(price) / float(base_close) - 1.0) * 100.0


def add_current_momentum_adjustment(companies: dict[str, dict[str, object]]) -> None:
    values = [post_june3_momentum(c) for c in companies.values()]
    for company in companies.values():
        post = post_june3_momentum(company)
        company["post_june3_mom"] = post
        post_rank = base.pct_rank(post, values)
        old_momentum = company["scores"]["价格确认/动量"]  # type: ignore[index]
        company["scores"]["价格确认/动量"] = base.clamp(old_momentum * 0.65 + post_rank * 0.35)  # type: ignore[index,operator]
        old_aggressive = company["scores"]["激进短线"]  # type: ignore[index]
        company["scores"]["激进短线"] = base.clamp(old_aggressive * 0.85 + post_rank * 0.15)  # type: ignore[index,operator]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    range_fix.fix_growth_ranges(companies)
    base.TARGET = "ALLE"
    base.score_companies(companies)
    add_current_momentum_adjustment(companies)

    a = companies[TARGET]
    overrides = {
        # FORM formal evaluation calibration:
        # strong HBM/DRAM and Foundry & Logic probe-card evidence, Q2 guide,
        # SK hynix/NVIDIA customer proof, positive FCF and net-cash balance
        # sheet. Caps reflect no formal backlog/bookings, Systems/CPO small
        # NTM contribution, rich valuation, high IV and mixed pressure history.
        "NTM兑现优先": 82.0,
        "右尾弹性优先": 88.0,
        "风险调整收益": 54.0,
        "下行保护优先": 63.0,
        "估值消化优先": 51.0,
        "近端催化优先": 78.0,
        "价格确认/动量": 70.0,
        "激进短线": 92.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]
    range_fix.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_TEST_PEERS:
        return "直接同业"
    if ticker in AI_MEMORY_LOGIC_CUSTOMERS or ticker in AI_NETWORK_SYSTEMS:
        return "上下游"
    if ticker in PACKAGING_TEST_ADJACENT or ticker in SEMICAP_ADJACENT or ticker in SEMI_MATERIALS:
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
            "NTM兑现优先": "A的HBM/F&L探针卡兑现更清楚",
            "右尾弹性优先": "A的HBM4/CPO探针卡右尾更直接",
            "风险调整收益": "A增长证据可抵部分高估值",
            "下行保护优先": "A净现金和FCF提供一定缓冲",
            "估值消化优先": "A收入高增可部分消化倍数",
            "近端催化优先": "A的Q2/HBM客户验证更近",
            "价格确认/动量": "A自6月初反弹确认更强",
            "激进短线": "A高IV叠加HBM测试叙事更进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入或利润兑现路径更稳",
            "右尾弹性优先": "B右尾规模或平台弹性更大",
            "风险调整收益": "B估值现金流组合更均衡",
            "下行保护优先": "B低波动和估值缓冲更强",
            "估值消化优先": "B利润和倍数更易消化",
            "近端催化优先": "B近端订单或财报催化更确定",
            "价格确认/动量": "B趋势更强或回吐更少",
            "激进短线": "B短线关注度或爆发力更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if rel == "直接同业":
        return "同业证据接近需等订单和份额验证"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
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


def final_choice(a: dict[str, object], b: dict[str, object], cells: list[str], rel: str) -> str:
    a_count, b_count, neutral = direction_counts(cells)
    if a_count > b_count:
        return TARGET
    if b_count > a_count:
        return str(b["ticker"])
    weighted = (
        a["scores"]["NTM兑现优先"] * 1.1
        + a["scores"]["右尾弹性优先"] * 0.9
        + a["scores"]["风险调整收益"] * 1.0
        + a["scores"]["估值消化优先"] * 0.9
        + a["scores"]["近端催化优先"] * 0.8
        + a["scores"]["下行保护优先"] * 0.6
        - b["scores"]["NTM兑现优先"] * 1.1
        - b["scores"]["右尾弹性优先"] * 0.9
        - b["scores"]["风险调整收益"] * 1.0
        - b["scores"]["估值消化优先"] * 0.9
        - b["scores"]["近端催化优先"] * 0.8
        - b["scores"]["下行保护优先"] * 0.6
    )
    if rel == "跨赛道" and abs(weighted) < 8 and neutral >= 2:
        return "风格中性"
    return TARGET if weighted >= 0 else str(b["ticker"])


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == TARGET:
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "FORM 的Q2指引、HBM/DRAM和F&L probe-card收入证据更硬。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "FORM 在HBM4、AI logic和CPO/SiPh wafer test上的右尾更直接。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "FORM 的Q2、客户占比和DRAM/F&L分市场验证窗口更近。"
        return "FORM 的高端探针卡兑现和客户证据略胜，但需承受高估值。"
    if final == "风格中性":
        return "两家公司风格差异明显，需按右尾进攻或防守兑现取舍。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、估值缓冲或压力期韧性明显优于 FORM。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 更容易用未来业绩消化估值，FORM 倍数已较高。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的风险调整收益比 FORM 更均衡。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和资金偏好强于 FORM。"
    return f"{b['ticker']} 在多数投资思路下比 FORM 更适合当前配置目标。"


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
        final = final_choice(a, b, cells, rel)
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
            x["b"]["scores"]["风险调整收益"]
            + x["b"]["scores"]["估值消化优先"]
            + x["b"]["scores"]["下行保护优先"]
            - a["scores"]["风险调整收益"]
            - a["scores"]["估值消化优先"]
            - a["scores"]["下行保护优先"],
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
            - x["b"]["scores"]["NTM兑现优先"]
            - x["b"]["scores"]["右尾弹性优先"]
            - x["b"]["scores"]["近端催化优先"],
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
    post = a.get("post_june3_mom")
    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-22 相对 2026-06-03 收盘价约 {fmt_pct(post)}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )
    product_names = [str(product[0]).split(" | ")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "FY2026Q1收入$226.1M、Q2指引$240M、DRAM/F&L双主线强，SK hynix 29.5%和NVIDIA 10.2%给客户锚",
            "FORM不披露formal backlog/bookings，季度收入仍依赖当季订单和交付",
        ),
        "右尾弹性优先": (
            "HBM4/HBM3E、AI logic/networking probe-card、TRITON/SiPh/CPO和FICT供应链带来非线性上限",
            "CPO和FICT在NTM内仍是小比例或使能项，不能替代HBM/F&L主收入",
        ),
        "风险调整收益": (
            "Q1 OCF $45.0M、FCF $30.7M，现金与有价证券$303M，净债务压力低",
            "2026-06-22 Forward PE 56.13、P/S 14.54、IV约86%-89%，上行容错率有限",
        ),
        "下行保护优先": (
            "净现金、流动性、Probe Cards客户认证壁垒和FCF为正提供基本缓冲",
            "高beta半导体设备属性明显，SOXX压力窗口累计-49.53%，估值不低",
        ),
        "估值消化优先": (
            "NTM基准收入$1.0B-$1.08B、non-GAAP经营利润率20%-24%，若连续兑现可消化部分高倍数",
            "当前倍数已要求乐观增长，若Q3/Q4收入放缓，估值会先受压",
        ),
        "近端催化优先": (
            "Q2实际收入/GM/EPS、DRAM/F&L分市场、SK hynix/NVIDIA客户占比和Farmers Branch节点都是1-2季验证点",
            "缺少标准订单披露，催化需要财报和客户收入继续证实，而非只靠叙事",
        ),
        "价格确认/动量": (
            "2026-06-22价格较2026-06-03收盘约+24%，显示财报后AI/HBM测试重估仍在继续",
            "2026-06-03过去一月仍为-8.26%，此前趋势并不连续，短期高IV显示拥挤",
        ),
        "激进短线": (
            "高IV、AI/HBM probe-card稀缺叙事、Q2验证窗口和CPO远期期权适合进攻资金",
            "短线弹性依赖高波动和连续上修，任何客户/毛利/订单反证都会放大回撤",
        ),
    }

    out: list[str] = []
    out += [
        "# FORM 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：FORM / FormFactor",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；两周/一月涨跌为 2026-06-03；SOXX压力窗口为 2026-06-04",
        "资料边界：使用公司评估、公司调研、行业调研和金融资料；未读取、引用或继承 `特征量化/`、`公司排序/`、`简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/`。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。FORM 的优势集中在 HBM/DRAM 与 Foundry & Logic probe-card 兑现、HBM4/CPO右尾、近端财报验证和高波动进攻弹性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 Forward PE 56.13、P/S 14.54、IV接近90%、formal backlog缺失和SOXX压力窗口回撤不低。",
        "- A 最适合的投资者画像：愿意承受高估值半导体测试链波动，押注 HBM3E/HBM4、AI logic/networking wafer sort、probe-card高端化和客户认证壁垒继续兑现的进攻型配置者。",
        "- A 最不适合的投资者画像：优先要低估值、低IV、稳定现金流防守、标准backlog可见度或跨周期低回撤的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在估值消化、风险调整收益、下行保护或更大平台右尾上压过 FORM。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：FORM 是项目内测试/探针卡链的高质量进攻资产，经营证据强于普通题材股，但全项目并非最优综合资产；在 NTM、右尾和近端催化上有竞争力，在估值和防守维度容易输给现金流平台或低倍数公司。",
        "- 后续最重要跟踪数据：FY2026Q2实际 revenue、non-GAAP GM和EPS；DRAM/F&L/Systems/Flash分市场收入；SK hynix、NVIDIA、Samsung、Micron、TSMC等客户占比；inventory/deferred revenue/FCF；Farmers Branch投产；TRITON/CPO production revenue；重组和tariff对GAAP/non-GAAP bridge的影响。",
        "- 自动化覆盖限制：公司评估全集 189 家；日度金融快照解析到 181 家，其中 180 家有可用价格/估值；缺少当日可用价格/估值的公司在估值、动量和激进短线列中按保守口径处理。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "FORM"]),
        base.row(["公司名称", "FormFactor"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "10.0亿-10.8亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "HBM4/HBM3E test intensity、HBM客户认证、F&L HPC/networking probe-card复购、Farmers Branch扩产与加州制造整合能否转化为可交付高端probe-card产能。"]),
        base.row(["最大反证", "formal backlog/bookings缺失；CPO在NTM内仍小；Systems Q1 YoY下滑；高估值要求Q2后DRAM/F&L连续兑现。"]),
        base.row(["近端催化剂", "FY2026Q2实际 revenue、non-GAAP GM/EPS、DRAM/F&L收入、SK hynix/NVIDIA客户占比、deferred revenue/inventory、Farmers Branch和CPO/TRITON收入信号。"]),
        base.row(["最新日度快照", daily_snapshot]),
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
        base.row(["直接同业", "同属半导体测试、探针卡、ATE、检测量测或系统级测试资金池，优先比较订单、收入兑现、客户认证、产品代际、毛利率和同业估值。", "TER、ATEYY、COHU、CAMT、ONTO、NVMI、AEHR", "同档时用客户/订单/分市场证据给微倾向；两档以上且同业反证清楚时可给建议或强烈建议。"]),
        base.row(["相邻替代", "同属半导体资本开支、先进封装、封装设备、OSAT或材料资金篮子，但产品不直接竞争。", "AMAT、ASML、LRCX、ENTG、KLIC、AMKR、ASX、PLAB", "强调资金二选一时谁的增长质量、估值消化和近端催化更好，避免只比终端赛道热度。"]),
        base.row(["上下游", "B 是FORM需求链中的AI芯片、HBM、foundry、OSAT、网络、服务器或云资本开支端。", "NVDA、MU、TSM、AMD、AVGO、ALAB、ANET、DELL、SMCI", "区分需求规模和利润捕获；下游更大不必然更优，上游瓶颈也不必然胜出。"]),
        base.row(["跨赛道", "云软件、电力、冷却、工业和材料以外业务差异较大，但作为项目内资金替代仍比较。", "MSFT、AMZN、VRT、ETN、CEG、TT、GEV", "默认降低结论力度；只有增长质量、估值消化、下行保护或价格确认明显拉开才给建议/强烈建议。"]),
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
        need = "需要 FORM 证明Q2后DRAM/F&L连续放量、non-GAAP GM维持49%+、订单/客户能见度提升，并降低高估值和高IV反证。"
        if "下行保护优先" in wins or "估值消化优先" in wins:
            need = "需要 FORM 让基准收入和利润而非乐观情景就能覆盖当前倍数，并证明压力窗口回撤可控。"
        if "风险调整收益" in wins:
            need = "需要 FORM 把客户集中、backlog缺失、Systems过渡和重组成本的不确定性进一步降下来。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 拿出同等强度的订单/backlog、客户项目、收入增速、利润杠杆或近端重定价证据。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要 B 在保持下行保护的同时补足HBM/AI测试级别的增长右尾和近端催化。"
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
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/封测_检测_计量_光罩/FORM_FormFactor_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_探针卡、ATE与系统级测试_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_form_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 FORM 的 HBM/DRAM、F&L probe-card、Q2指引、客户占比、现金流、CPO小基数、高估值、高IV和压力窗口表现做人工校准后建档；未读取下游量化目录或现成排序结论。",
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
                "form_tiers": companies[TARGET]["tiers"],
                "form_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
