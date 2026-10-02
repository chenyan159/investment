from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


ROOT = Path(r"D:\investment\基本面")
TARGET = "VISN"
TARGET_NAME = "Vistance Networks"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "VISN_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH
base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"
base.MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
base.MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
base.SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


# VISN is not an AI data-center fabric company. Direct comparability is limited
# to networking/broadband/campus-network peers and the RUCKUS/Belden transaction
# context. AI-network names are usually capital-allocation alternatives, not
# product substitutes.
DIRECT_PEERS = {"BDC", "CSCO", "NOK"}
ACCESS_WIFI_SUPPLY_CHAIN = {
    "AAOI",
    "ANET",
    "APH",
    "AVGO",
    "CIEN",
    "COHR",
    "CRDO",
    "GLW",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "MXL",
    "POET",
    "QCOM",
    "SMTC",
    "TEL",
    "VIAV",
}
AI_INFRA_CAPITAL_ALTERNATIVES = {
    "ADBE",
    "ALAB",
    "AMD",
    "AMZN",
    "APLD",
    "ARM",
    "BABA",
    "CDNS",
    "CLS",
    "CRWD",
    "CRWV",
    "DELL",
    "DLR",
    "EQIX",
    "FN",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "META",
    "MSFT",
    "NBIS",
    "NTAP",
    "NTNX",
    "NVDA",
    "ORCL",
    "PENG",
    "PSTG",
    "SANM",
    "SMCI",
}
CORE_AI_NTM_PEERS = {
    "ALAB",
    "AMD",
    "ANET",
    "AVGO",
    "CRDO",
    "GOOGL",
    "MRVL",
    "MSFT",
    "MU",
    "NVDA",
    "SMCI",
}
CORE_AI_RIGHT_TAIL_PEERS = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "APLD",
    "AVGO",
    "COHR",
    "CRDO",
    "CRWV",
    "IREN",
    "MRVL",
    "MU",
    "NBIS",
    "NVDA",
    "SMCI",
    "SMTC",
    "VRT",
}
CORE_AI_AGGRESSIVE_PEERS = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "APLD",
    "AVGO",
    "COHR",
    "CRDO",
    "CRWV",
    "GLW",
    "IREN",
    "MRVL",
    "MU",
    "NBIS",
    "NVDA",
    "SMCI",
    "SMTC",
    "VRT",
}

VISN_SCORES = {
    "NTM兑现优先": 64.0,
    "右尾弹性优先": 58.0,
    "风险调整收益": 63.0,
    "下行保护优先": 62.0,
    "估值消化优先": 88.0,
    "近端催化优先": 76.0,
    "价格确认/动量": 52.0,
    "激进短线": 70.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for company in companies.values():
        company["tiers"] = {}
        company["ranks"] = {}

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
            company["tiers"][strategy] = tier  # type: ignore[index]
            company["ranks"][strategy] = rank  # type: ignore[index]

    for company in companies.values():
        if not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company["tiers"][strategy] = "资料不足"  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    base.score_companies(companies)
    a = companies[TARGET]
    for strategy, score in VISN_SCORES.items():
        a["scores"][strategy] = score  # type: ignore[index]
    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in ACCESS_WIFI_SUPPLY_CHAIN:
        return "上下游"
    if ticker in AI_INFRA_CAPITAL_ALTERNATIVES:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    short_names = {
        "NTM兑现优先": "NTM",
        "右尾弹性优先": "右尾",
        "风险调整收益": "风险收益",
        "下行保护优先": "下行",
        "估值消化优先": "估值",
        "近端催化优先": "催化",
        "价格确认/动量": "动量",
        "激进短线": "短线",
    }
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strategy in STRATS:
        diff = tier_value(a["tiers"][strategy]) - tier_value(b["tiers"][strategy])  # type: ignore[index]
        label = short_names[strategy]
        if diff >= 1:
            a_strong.append(label)
        elif diff <= -1:
            b_strong.append(label)
        else:
            close.append(label)

    def joined(items: list[str]) -> str:
        if not items:
            return "无"
        return "、".join(items[:4]) + ("等" if len(items) > 4 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


def decision_summary(cells: list[str]) -> str:
    short_names = {
        "NTM兑现优先": "NTM",
        "右尾弹性优先": "右尾",
        "风险调整收益": "风险收益",
        "下行保护优先": "下行",
        "估值消化优先": "估值",
        "近端催化优先": "催化",
        "价格确认/动量": "动量",
        "激进短线": "短线",
    }
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strategy, cell in zip(STRATS, cells):
        label = short_names[strategy]
        tag = base.tag_in_cell(cell) or ""
        if tag.endswith("投A"):
            a_strong.append(label)
        elif tag.endswith("投B"):
            b_strong.append(label)
        else:
            close.append(label)

    def joined(items: list[str]) -> str:
        if not items:
            return "无"
        return "、".join(items[:4]) + ("等" if len(items) > 4 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


def reason_for(strategy: str, tag: str, company: dict[str, object], rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if tag == "中性":
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"

    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "Aurora指引、Q1增速与RUCKUS桥接更清楚",
            "右尾弹性优先": "DOCSIS第二波和RUCKUS交易期权仍有弹性",
            "风险调整收益": "低估值和现金返还抵消部分增长短板",
            "下行保护优先": "RUCKUS proceeds和低倍数提供一定底线",
            "估值消化优先": "Forward PE、P/S和EV/EBITDA更低",
            "近端催化优先": "RUCKUS H2交割和60天分配窗口更近",
            "价格确认/动量": "近期小幅上行且事件溢价仍在",
            "激进短线": "小市值、高IV和交易事件适合短线进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}网络收入、客户或订单兑现更稳",
            "右尾弹性优先": f"{ticker}全栈网络或企业渠道右尾更大",
            "风险调整收益": f"{ticker}增长质量和组合韧性更好",
            "下行保护优先": f"{ticker}客户分散或现金流更稳",
            "估值消化优先": f"{ticker}持续经营收入更能解释估值",
            "近端催化优先": f"{ticker}产品/订单节点更清楚",
            "价格确认/动量": f"{ticker}趋势确认强于VISN",
            "激进短线": f"{ticker}短线资金关注更强",
        }[strategy]

    if category in HIGH_GROWTH_CATS or ticker in AI_INFRA_CAPITAL_ALTERNATIVES:
        return {
            "NTM兑现优先": f"{ticker} AI主链收入兑现更直接",
            "右尾弹性优先": f"{ticker}数据中心右尾大于VISN接入网周期",
            "风险调整收益": f"{ticker}增长质量更能覆盖风险",
            "下行保护优先": f"{ticker}现金流、需求能见度或压力表现更好",
            "估值消化优先": f"{ticker}高增长更能消化当前估值",
            "近端催化优先": f"{ticker}订单/产品催化更密集",
            "价格确认/动量": f"{ticker}价格确认更强",
            "激进短线": f"{ticker} AI beta和叙事更适合进攻",
        }[strategy]

    if category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}订单/backlog或交付更清楚",
            "右尾弹性优先": f"{ticker}AI电力/设备利润池更直接",
            "风险调整收益": f"{ticker}增长与估值组合更优",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}业绩更能消化当前估值",
            "近端催化优先": f"{ticker}近端订单或产能催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker}未来12个月兑现证据更硬",
        "右尾弹性优先": f"{ticker}极端情景上行更大",
        "风险调整收益": f"{ticker}风险调整赔率更好",
        "下行保护优先": f"{ticker}资产质量或估值更安全",
        "估值消化优先": f"{ticker}当前估值更容易消化",
        "近端催化优先": f"{ticker}未来两个季度催化更明确",
        "价格确认/动量": f"{ticker}价格行为更强",
        "激进短线": f"{ticker}短线关注度和波动更强",
    }[strategy]


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    tier_diff = tier_value(at) - tier_value(bt)
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
    ticker = str(b.get("ticker", ""))
    if ticker in CORE_AI_NTM_PEERS and strategy == "NTM兑现优先":
        tag = "建议投B" if tag != "强烈建议投B" else tag
    if ticker in CORE_AI_RIGHT_TAIL_PEERS and strategy == "右尾弹性优先":
        tag = "强烈建议投B" if ticker in {"ALAB", "AVGO", "CRDO", "MU", "NVDA", "SMCI"} else "建议投B"
    if ticker in CORE_AI_AGGRESSIVE_PEERS and strategy == "激进短线":
        tag = "强烈建议投B" if ticker in {"ALAB", "AVGO", "CRDO", "MU", "SMCI"} else "建议投B"
    return tag


def cell_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    tag = label_for(a, b, strategy, rel)
    return f"{tag}：{reason_for(strategy, tag, b, rel)}"


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
    ticker = str(b.get("ticker", ""))
    labels = {strategy: base.tag_in_cell(cell) or "" for strategy, cell in zip(STRATS, cells)}
    if (
        ticker in CORE_AI_RIGHT_TAIL_PEERS
        and labels["右尾弹性优先"].endswith("投B")
        and labels["激进短线"].endswith("投B")
        and (labels["NTM兑现优先"].endswith("投B") or labels["价格确认/动量"].endswith("投B"))
    ):
        return "B"
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
            return "VISN胜在低倍数、RUCKUS现金返还和估值消化，B的成长优势不足以抵消。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "VISN的RUCKUS交割、特别分配和Aurora季度验证节点更集中。"
        return "VISN的事件驱动和估值缓冲略优，B的右尾证据不足以形成压倒优势。"

    category = str(b.get("category", ""))
    ticker = str(b.get("ticker", ""))
    if ticker in CORE_AI_RIGHT_TAIL_PEERS:
        return f"{b['ticker']}直接吃到AI主链或高增长需求，右尾明显强于VISN的接入网周期。"
    if category in HIGH_GROWTH_CATS and b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']}直接吃到AI主链或高增长需求，右尾明显强于VISN的接入网周期。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']}的NTM收入、订单或指引兑现证据更硬。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']}的现金流、压力表现或资产质量更适合防守。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']}价格趋势和资金确认强于VISN。"
    return f"{b['ticker']}在多数投资思路下比VISN更符合项目内资金配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    rows: list[dict[str, object]] = []
    rel_order = {"直接同业": 0, "上下游": 1, "相邻替代": 2, "跨赛道": 3}
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        ac, bc, nc = direction_counts(cells)
        final = final_choice(a, b, cells)
        rows.append(
            {
                "ticker": ticker,
                "b": b,
                "rel": rel,
                "cells": cells,
                "ac": ac,
                "bc": bc,
                "nc": nc,
                "final": final,
                "summary": decision_summary(cells),
                "reason": key_reason(a, b, final),
            }
        )
    rows.sort(key=lambda row: (rel_order[str(row["rel"])], base.category_short(str(row["b"]["category"])), str(row["ticker"])))  # type: ignore[index]
    return rows


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
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["估值消化优先"] - x["b"]["scores"]["估值消化优先"]),  # type: ignore[index,operator]
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
    daily_snapshot = (
        f"2026-06-23 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1 Aurora收入$298.4M、同比+32.6%，Aurora FY2026 adjusted EBITDA指引$225M-$250M，RUCKUS交割前仍有桥接收入",
            "Aurora基准收入只约-2%至+12%，公司不披露backlog/bookings，RUCKUS交割会截断报告收入",
        ),
        "右尾弹性优先": (
            "小市值、DOCSIS 4.0第二波MSO、vCCAP/software attach和RUCKUS交易失败/延迟构成上限情景",
            "已售CCS和AI后端网络不归VISN，极度乐观需非Comcast订单、软件收入和利润率同时兑现",
        ),
        "风险调整收益": (
            "Forward PE 8.87、P/S 1.39、EV/EBITDA 1.22，RUCKUS税后proceeds约$1.7B对市值有保护",
            "SOXX压力窗口累计-32.95%，Aurora留存后业务更单一，客户集中和价格压力仍重",
        ),
        "下行保护优先": (
            "RUCKUS现金交易、低估值和去杠杆后资产负债表改善给下行边界",
            "三段SOXX压力累计-32.95%，Call IV 62.7%，并非低波动防御资产",
        ),
        "估值消化优先": (
            "低Forward PE、低P/S、低EV/EBITDA和Aurora EBITDA指引使估值消化在项目内靠前",
            "报告收入受RUCKUS交割扭曲，若Aurora margin低于指引，低倍数可能是价值陷阱",
        ),
        "近端催化优先": (
            "RUCKUS预计2026H2交割、excess cash 60天内分配计划、Aurora Q2/Q3收入和EBITDA验证",
            "催化依赖交易审批、交割时点和资本返还安排，非Comcast订单仍缺金额披露",
        ),
        "价格确认/动量": (
            "2026-06-23过去两周+2.72%、过去一月+1.38%，价格没有完全破位",
            "相对项目内AI主链动量偏弱，SOXX压力期回撤较深",
        ),
        "激进短线": (
            "Call IV 62.7%、小市值、RUCKUS交割/分配和DOCSIS 4.0事件驱动适合短线观察",
            "不是AI数据中心核心网络股，短线右尾弱于800G/1.6T、GPU、HBM和NeoCloud主链",
        ),
    }

    out: list[str] = []
    out += [
        "# VISN 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：VISN / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV、过去两周、过去1个月和SOXX三段压力窗口均为 2026-06-23",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 VISN vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。VISN 的优势不是AI数据中心核心网络，而是低倍数、RUCKUS现金事件和近端资本返还窗口。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是Aurora持续核心增长不够高、AI主链右尾不足、SOXX压力期表现弱。",
        "- A 最适合的投资者画像：事件驱动、低估值重估、愿意跟踪RUCKUS交割/特别分配并接受Aurora单一业务风险的投资者。",
        "- A 最不适合的投资者画像：只买AI数据中心核心网络、800G/1.6T、GPU/ASIC、NeoCloud或高速光互联高beta右尾的进攻资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]]) if strong_b_rows else '无明显集中反方'}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：VISN 在估值消化和近端事件上靠前，但在增长右尾、价格确认和AI主链质量上偏中后；它更像事件驱动价值重估，而不是项目内长期高增长核心仓。",
        "- 后续最重要跟踪数据：RUCKUS监管审批/交割日期、税后proceeds和特别分配金额；Aurora季度收入、standalone adjusted EBITDA是否达到$225M-$250M；非Comcast MSO订单、vCCAP/software attach、lower pricing和库存/应收/FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "VISN"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"]]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准利润：{a['base_profit']}；现金流：{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "非Comcast MSO订单、unified node/amplifier认证和量产、vCCAP/software attach、lower pricing、现场施工/验收以及RUCKUS交割时间。"]),
        base.row(["最大反证", "VISN不卖AI后端800G/1.6T、GPU互联、CPO或光模块；已售CCS不再归属VISN，RUCKUS交割后也不再贡献持续经营收入。"]),
        base.row(["近端催化剂", "RUCKUS 2026H2交割、交割后60天内excess cash分配、Aurora Q2/Q3收入和EBITDA、非Comcast MSO项目/订单披露。"]),
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
        base.row(["直接同业", "网络设备、宽带接入、企业/园区网络或RUCKUS交易口径相近，优先比较收入兑现、客户分散度、产品代际、现金流和估值。", "BDC、CSCO、NOK", "直接同业若一方在客户、订单、利润质量或估值上明显胜出，可提高到建议/强烈建议。"]),
        base.row(["上下游", "宽带接入、PON/DOCSIS/Wi-Fi silicon、光/铜连接、测试、网络设备或企业网络相关链条。", "AVGO、QCOM、MXL、VIAV、APH、TEL、CIEN、ANET", "不把上游瓶颈或下游收入规模自动等同于胜出，重点看利润捕获和收入确认。"]),
        base.row(["相邻替代", "同属AI基础设施或网络资金篮子，但VISN并不直接参与AI后端fabric，重点比较增长质量、赔率、估值消化和催化。", "NVDA、MRVL、CRDO、SMTC、VRT、ETN、GEV、SMCI", "默认按全项目档位判断；若对方AI收入更直接且档位高，VISN只能靠估值/事件驱动反击。"]),
        base.row(["跨赛道", "业务差异大但作为项目内资金配置替代仍可比较风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、DHR、CAT、RKLB、TSLA", "默认降低结论力度；证据互有强弱时优先使用中性或微倾向。"]),
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

    out += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "VISN需要看到非Comcast MSO订单、Aurora收入/EBITDA上修、RUCKUS顺利交割并明确大额现金分配，才能抵消B的增长或风险收益优势。"
        if str(b.get("category", "")) in HIGH_GROWTH_CATS:
            need = "VISN需要证明DOCSIS 4.0/Aurora的收入和利润上修足以接近AI主链右尾，同时兑现RUCKUS现金返还。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "B需要提高NTM兑现、现金流质量、估值消化或近端催化确定性，才能反超VISN的低倍数和事件驱动优势。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "B需要把右尾叙事转成可确认收入/利润，并降低估值、波动或现金流反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        f"- 日度金融数据覆盖：2026-06-23 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- VISN 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI网络_光互联_连接器/VISN_Vistance_Networks_公司调研_2026-06-11.md`、`行业调研/行业索引.md`、`行业调研/AI网络_光互联_铜互联/行业调研_宽带接入、PON、DOCSIS 4.0与Wi-Fi 7_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 VISN 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8", newline="\n")
    a = companies[TARGET]
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "visn_tiers": {strategy: a["tiers"][strategy] for strategy in STRATS},  # type: ignore[index]
        "visn_ranks": {strategy: a["ranks"][strategy] for strategy in STRATS},  # type: ignore[index]
        "visn_scores": {strategy: round(a["scores"][strategy], 2) for strategy in STRATS},  # type: ignore[index]
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
