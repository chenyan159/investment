from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "ECL"
TARGET_NAME = "Ecolab"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ECL_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "DD",
    "PNR",
    "DCI",
}

WATER_CHEM_ADJACENT = {
    "APD",
    "LIN",
    "DHR",
    "TMO",
    "NDSN",
    "MMM",
    "CC",
    "Q",
    "SHECY",
    "SOMMY",
    "ASGLY",
    "AJNMY",
    "ENTG",
    "MTRN",
    "ROG",
    "HOCPY",
    "DKILY",
}

COOLING_INFRA_ADJACENT = {
    "AAON",
    "CARR",
    "DOV",
    "JCI",
    "MOD",
    "TT",
    "VRT",
    "PH",
    "FTV",
    "ALLE",
    "EME",
    "FIX",
    "IESC",
    "MYRG",
}

SEMICONDUCTOR_DOWNSTREAM_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
}

DATA_CENTER_DOWNSTREAM_CATS = {
    "云算力_IDC_AI软件平台",
    "电力_发电_能源_储能",
    "配电_电源_功率器件",
}


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1].setdefault("scores", {}).get(strategy, 0),  # type: ignore[union-attr]
            reverse=True,
        )
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
        if not company.get("fin", {}).get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"  # type: ignore[index]
                company.setdefault("ranks", {})[strategy] = None  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    calibrated.fix_growth_ranges(companies)  # type: ignore[arg-type]

    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in calibrated.SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    ecl = companies[TARGET]
    overrides = {
        # ECL has a real FY2026/Ovivo/Water anchor and stable services, but CoolIT is
        # only partial NTM revenue until close.
        "NTM兑现优先": 72.0,
        # Global High-Tech/CoolIT creates a right tail, but it is smaller and less
        # immediate than chips, memory, optical, servers and pure liquid-cooling plays.
        "右尾弹性优先": 62.0,
        # Quality and cash flow are strong; 28x forward PE and higher pro-forma
        # leverage keep this below the best risk-adjusted names.
        "风险调整收益": 61.0,
        "下行保护优先": 76.0,
        "估值消化优先": 55.0,
        "近端催化优先": 65.0,
        "价格确认/动量": 50.0,
        "激进短线": 54.0,
    }
    for strategy, score in overrides.items():
        ecl.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in WATER_CHEM_ADJACENT or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if ticker in COOLING_INFRA_ADJACENT or category == "机电_冷却_工程_水处理_边缘工业AI":
        return "相邻替代"
    if category in SEMICONDUCTOR_DOWNSTREAM_CATS or category in DATA_CENTER_DOWNSTREAM_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, winner: str, b: dict[str, object], rel: str, diff: float) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))

    if winner == "A":
        return {
            "NTM兑现优先": "A有FY2026指引、Ovivo和服务底盘",
            "右尾弹性优先": "A有CoolIT/High-Tech水冷期权",
            "风险调整收益": "A质量现金流和上行更均衡",
            "下行保护优先": "A低IV、服务粘性和压力期韧性更好",
            "估值消化优先": "A中速收入和利润兑现更可见",
            "近端催化优先": "A有Q2/H2提速和CoolIT close节点",
            "价格确认/动量": "A价格确认较稳且未明显过热",
            "激进短线": "A液冷收购叙事仍有事件弹性",
        }[strategy]

    if winner == "B":
        if ticker in DIRECT_PEERS:
            return {
                "NTM兑现优先": "B同业收入/利润兑现更直接",
                "右尾弹性优先": "B同业小基数或材料右尾更大",
                "风险调整收益": "B同业估值或上行组合更优",
                "下行保护优先": "B同业估值/现金流缓冲更强",
                "估值消化优先": "B同业增长与估值更匹配",
                "近端催化优先": "B同业订单或周期催化更明确",
                "价格确认/动量": "B同业价格趋势更强",
                "激进短线": "B同业短线beta更高",
            }[strategy]
        if category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链收入兑现更短链",
                "右尾弹性优先": "B直接AI右尾和小基数更大",
                "风险调整收益": "B上行空间更能覆盖风险",
                "下行保护优先": "B需求能见度或现金流更强",
                "估值消化优先": "B高速增长更能消化估值",
                "近端催化优先": "B产品/订单催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta和AI叙事更适合进攻",
            }[strategy]
        if category in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单/backlog或项目确认更硬",
                "右尾弹性优先": "B AI电力/机电右尾更直接",
                "风险调整收益": "B上行与订单确定性组合更优",
                "下行保护优先": "B资产质量或受监管现金流更稳",
                "估值消化优先": "B backlog兑现更能覆盖估值",
                "近端催化优先": "B项目/FID/产能催化更明确",
                "价格确认/动量": "B价格趋势和确认度更强",
                "激进短线": "B高关注度和事件弹性更强",
            }[strategy]
        return {
            "NTM兑现优先": "B收入兑现证据更强",
            "右尾弹性优先": "B右尾空间更大",
            "风险调整收益": "B风险收益组合更优",
            "下行保护优先": "B下行缓冲更强",
            "估值消化优先": "B增长更能消化估值",
            "近端催化优先": "B近端催化更明确",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B短线弹性更强",
        }[strategy]

    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "质量、估值和兑现接近"
    return "档位接近需再验证"


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    tier_diff = tier_value(str(at)) - tier_value(str(bt))
    score_diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
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
    winner = "A" if tag.endswith("投A") else "B" if tag.endswith("投B") else "中性"
    diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
    return f"{tag}：{reason_for(strategy, winner, b, rel, diff)}"


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
    quality_weight = (
        float(a["scores"]["风险调整收益"])
        + float(a["scores"]["NTM兑现优先"]) * 0.8
        + float(a["scores"]["下行保护优先"]) * 0.7
        + float(a["scores"]["估值消化优先"]) * 0.6
        - float(b["scores"]["风险调整收益"])
        - float(b["scores"]["NTM兑现优先"]) * 0.8
        - float(b["scores"]["下行保护优先"]) * 0.7
        - float(b["scores"]["估值消化优先"]) * 0.6
    )
    return "A" if quality_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if float(a["scores"]["下行保护优先"]) - float(b["scores"]["下行保护优先"]) > 12:
            return "ECL的服务/耗材底盘、低IV和SOXX压力窗口表现比B更适合防守配置。"
        if float(a["scores"]["NTM兑现优先"]) - float(b["scores"]["NTM兑现优先"]) > 10:
            return "ECL有FY2026指引、Ovivo并表和Water/I&S/Pest/Life底盘，B的NTM证据较弱。"
        if float(a["scores"]["近端催化优先"]) - float(b["scores"]["近端催化优先"]) > 10:
            return "ECL的H2 organic提速、High-Tech验证和CoolIT close节点比B更近。"
        return "ECL在质量、防守和可兑现增长上略胜，B的右尾或动量不足以覆盖反证。"

    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于ECL。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 14:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比ECL更硬。"
    if float(b["scores"]["价格确认/动量"]) - float(a["scores"]["价格确认/动量"]) > 12:
        return f"{b['ticker']}的价格确认和资金偏好明显强于ECL。"
    if float(b["scores"]["估值消化优先"]) - float(a["scores"]["估值消化优先"]) > 12:
        return f"{b['ticker']}的增长和估值匹配度优于ECL。"
    return f"{b['ticker']}在多数投资思路下比ECL更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
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
    rows: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        a_count, b_count, neutral = direction_counts(cells)
        final = final_choice(a, b, cells)
        rows.append(
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

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda item: (rel_order.get(str(item["rel"]), 9), str(item["ticker"])))


def fmt_num(value: object, precision: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{precision}f}"
    except Exception:
        return "缺失"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return "缺失"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "缺失"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = sorted(str(company["date"]) for company in companies.values())
    date_range = f"{company_dates[0]} 至 {company_dates[-1]}"

    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]

    strong_b = sorted(
        comparisons,
        key=lambda row: (
            int(row["bc"]) - int(row["ac"]),
            float(row["b"]["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda row: (
            int(row["ac"]) - int(row["bc"]),
            float(a["scores"]["下行保护优先"]) - float(row["b"]["scores"]["下行保护优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_b_rows = [row for row in strong_b if int(row["bc"]) >= 5 and int(row["bc"]) - int(row["ac"]) >= 3][:45]
    strong_a_rows = [row for row in strong_a if int(row["ac"]) >= 5 and int(row["ac"]) - int(row["bc"]) >= 3][:45]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker].get("fin", {}).get("price")  # type: ignore[union-attr]
    ]

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {
        strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]
        for strategy in STRATS
    }

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22收盘价 `{fmt_num(fin.get('price'))}`，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"P/S `{fmt_num(fin.get('ps'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`，Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03过去两周 `{fmt_pct(mom2.get('mom2w'))}`，过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04三段SOXX压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    product_names = []
    for product in a["products"]:  # type: ignore[index]
        product_name = str(product[0]).split("：")[0]
        product_names.append(product_name)
        if len(product_names) >= 8:
            break

    support = {
        "NTM兑现优先": (
            "2026 reported sales指引+9%-+11%，NTM基准`181-188亿美元`，Ovivo并表、Water/I&S/Pest/Life底盘和H2 organic提速提供硬锚",
            "CoolIT尚未close，NTM只能纳入Q3 close后partial revenue；H2 surcharge和High-Tech项目确认仍需兑现",
        ),
        "右尾弹性优先": (
            "CoolIT NTM sales约`5.5亿美元`、Global High-Tech pro forma约`15亿美元`、D2C液冷和半导体UPW构成AI水/流体右尾",
            "右尾占公司体量仍小，CaaS/3D TRASAR standalone订单、attach rate和客户合同未披露，低于AI芯片/光互联主链",
        ),
        "风险调整收益": (
            "传统服务/耗材现金流、I&S/Pest/Life高质量增长和Low-IV属性降低下行；AI水冷提供一定上行",
            "Forward PE约`28.05x`、P/S约`4.61x`，CoolIT高价交易后pro forma leverage约`3x`，赔率不是全项目最优",
        ),
        "下行保护优先": (
            "Call IV仅`30.4%`，三段SOXX压力窗口累计`-28.29%`，明显优于SOXX和多数高beta AI主链；服务/耗材粘性强",
            "工业Water/Heavy Water/Paper、commodity cost、并购融资和整合仍会在压力期放大估值惩罚",
        ),
        "估值消化优先": (
            "NTM收入双位数增长、adjusted OI margin向`19%`附近改善，现金流为正，能部分消化估值",
            "估值已包含高质量溢价，若CoolIT只partial并表且CaaS订单不披露，28x Forward PE不算便宜",
        ),
        "近端催化优先": (
            "2026Q2/H2 organic提速、Global High-Tech>20%读数延续、CoolIT预计2026Q3 close、Ovivo全年贡献均在1-2季可验证",
            "缺少已披露CoolIT backlog、hyperscaler客户名单、CaaS合同和High-Tech细分订单金额，催化强度弱于纯AI硬件链",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周`+2.83%`，6月22日价格高于6月3日收盘，防守型动量较稳",
            "过去一月`-1.48%`，不属于全项目强动量；低IV也意味着爆发力有限",
        ),
        "激进短线": (
            "CoolIT close、液冷并购和AI水处理新闻可触发再定价，且IV不高时事件赔率有一定吸引力",
            "ECL体量大、传统业务占比高，短线beta和资金拥挤度弱于AI芯片、光模块、NeoCloud和高压电气链",
        ),
    }

    lines: list[str] = []
    lines += [
        "# ECL 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：ECL / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV为2026-06-22；两周/一月区间涨跌为2026-06-03；SOXX压力窗口为2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 ECL vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；ECL 的 CoolIT 只按 pending close 后 partial NTM 并表处理，不把 full-year run-rate 直接并入基准。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ECL 的相对强项是风险调整、NTM兑现，以及相对传统工业/材料公司的AI水冷右尾；核心来自水/卫生/生命科学服务底盘、Ovivo并表、H2 organic提速、低IV和SOXX压力窗口韧性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是右尾收入化只占公司小部分、CoolIT尚未close、CaaS/3D TRASAR缺少standalone合同，短线beta和动量弱于AI主链。",
        "- A 最适合的投资者画像：希望买高质量服务/耗材现金流，同时保留AI数据中心液冷和半导体UPW上修期权，但不愿承受纯AI硬件高波动的中长期配置者。",
        "- A 最不适合的投资者画像：只追求高增长大右尾、强价格动量、高IV进攻、直接AI芯片/光互联订单或短期爆发力的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(row['ticker']) for row in strong_b_rows[:10]])}。这些公司通常有更直接的AI收入化、订单/RPO/backlog、更高NTM增速或更强价格确认。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：ECL 是全项目中偏上质量型、非顶级高增长标的；面对传统材料/水处理和弱证据公司具备优势，但面对AI芯片、内存、光互联、前道设备、AI电力机电和NeoCloud强标的，多数进攻型思路会落后。",
        "- 后续最重要跟踪数据：2026Q2 sales/organic growth/gross margin、H2 surcharge覆盖、Global High-Tech细分收入、Ovivo订单/项目确认、CoolIT close日期与并表收入、CoolIT orders/backlog和毛利、CaaS/3D TRASAR attach rate、pro forma leverage、FCF conversion和One Ecolab重组现金支出。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ECL"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "181-188 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "CoolIT交易尚未close；NTM只能纳入Q3 2026 close后的partial revenue，不能把CoolIT未来12个月销售全额并入。"]),
        base.row(["最大反证", "CaaS/3D TRASAR standalone收入、attach rate和客户合同未披露；CoolIT硬件可能被多供压价，交易后杠杆和整合风险抬升。"]),
        base.row(["近端催化剂", "2026Q2/H2 organic提速、Global High-Tech>20%延续、Ovivo项目确认、CoolIT 2026Q3 close、CaaS/3D TRASAR客户披露。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        lines.append(base.row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与ECL在水处理、过滤、膜/流体服务、工业/生命科学水和客户运营结果上高度重叠，优先比较收入兑现、利润率、客户粘性、估值和现金流。", "DD、PNR、DCI", "同业证据权重最高；若B的水处理/过滤增长或估值明显更优，可覆盖ECL质量优势。"]),
        base.row(["相邻替代", "同属材料/化学品/水处理/冷却/HVAC/机电基础设施资金篮子，但产品不完全竞争，比较增长质量、订单、估值消化和风险收益。", "APD、LIN、DHR、TMO、VRT、TT、CARR、MOD、DOV", "允许在ECL防守质量和B的AI设备/冷却订单之间做风格切换，默认不因赛道更热直接胜出。"]),
        base.row(["上下游", "B处于ECL可服务的半导体制造、AI芯片、服务器、云/IDC、电力或数据中心资本开支链条。", "NVDA、TSM、ASML、AMAT、MSFT、AMZN、EQIX、DLR、ETN", "不把下游AI capex自动映射为ECL收入；只在B的利润捕获、订单或估值消化明显更好时提高结论力度。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "RKLB、TSLA、CRWD、CAT、MSI", "默认降低结论力度；除非档位差明显，否则优先微倾向或中性。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]

    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    lines.append(base.row(headers))
    lines.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        lines.append(
            base.row(
                [
                    index,
                    base.short_name(b),  # type: ignore[arg-type]
                    base.category_short(str(b.get("category", ""))),  # type: ignore[union-attr]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(int(comparison["ac"]), int(comparison["bc"]), int(comparison["nc"])),
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    lines += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        lines.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    lines += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要ECL披露CoolIT orders/backlog、客户/平台design-in、CaaS/3D TRASAR attach rate，并把High-Tech增长转成可确认收入和利润。"
        if comparison["rel"] == "直接同业":
            need = "需要ECL在水处理/过滤同业中证明更高organic、margin和现金流，同时降低CoolIT高价并购和杠杆反证。"
        elif comparison["rel"] == "上下游":
            need = "需要ECL证明能实际捕获下游AI芯片/数据中心利润池，而不是只有小额间接受益。"
        elif comparison["rel"] == "跨赛道":
            need = "需要ECL用更硬的订单、客户合同或利润上修抵消跨赛道公司的高增长和强动量。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    lines += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高NTM收入确认、利润/现金流质量或估值消化能力，或给出明确订单/指引上修。"
        if float(b["scores"]["右尾弹性优先"]) > float(a["scores"]["右尾弹性优先"]):  # type: ignore[index]
            need = "需要B把右尾叙事转成可确认收入和利润，并降低估值、波动或资产负债表反证。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/ECL_Ecolab_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_冷却液、水处理、过滤与制冷剂_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心风冷、冷水机组与HVAC_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体高纯水、气体与化学流体系统_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV或正式金融行的公司为 {('、'.join(missing_fin) if missing_fin else '无')}。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_ecl_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对百分比区间做同号区间修正，并对ECL的CoolIT partial并表、Global High-Tech水处理期权、估值/杠杆和日度价格数据做人工校准后建档。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 ECL 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    a = companies[TARGET]
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "ecl_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "ecl_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "ecl_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
