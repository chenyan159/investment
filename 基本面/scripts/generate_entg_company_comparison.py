from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_dd_company_comparison as growth_fix


TARGET = "ENTG"
TARGET_NAME = "Entegris"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ENTG_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "AJNMY",
    "ASGLY",
    "AXTI",
    "DKILY",
    "HOCPY",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}
MATERIAL_ADJACENT = {
    "APD",
    "CC",
    "DD",
    "DHR",
    "ECL",
    "LIN",
    "MMM",
    "NDSN",
    "TMO",
}
SEMI_DOWNSTREAM_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
}
REMOTE_DEMAND_CATS = {
    "云算力_IDC_AI软件平台",
}


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: float(item[1].setdefault("scores", {}).get(strategy, 0)),  # type: ignore[union-attr]
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
    growth_fix.fix_growth_ranges(companies)  # repairs +7%-11% style ranges

    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in calibrated.SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    entg = companies[TARGET]
    overrides = {
        # Q2 guide, Q3 visibility, APS/MS segment profit and FCF support a solid,
        # but not top-quartile, NTM setup.
        "NTM兑现优先": 74.0,
        # Advanced purity, deposition precursors, CMP/clean and advanced packaging
        # give real AI manufacturing optionality, but the right tail is smaller
        # and less direct than chips, memory, optical and server/rack names.
        "右尾弹性优先": 69.0,
        # High valuation, high IV, debt/leverage and weak SOXX-stress behavior
        # offset good product quality and FCF.
        "风险调整收益": 49.0,
        "下行保护优先": 50.0,
        "估值消化优先": 57.0,
        "近端催化优先": 64.0,
        # 6/22 price is far above the 6/3 interval close, but the official
        # interval file stops at 6/3 and IV is already high, so this is strong
        # confirmation but not a top-tier momentum score.
        "价格确认/动量": 76.0,
        "激进短线": 86.0,
    }
    for strategy, score in overrides.items():
        entg.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in MATERIAL_ADJACENT or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if category in SEMI_DOWNSTREAM_CATS:
        return "上下游"
    if category in REMOTE_DEMAND_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, winner: str, b: dict[str, object], rel: str) -> str:
    category = str(b.get("category", ""))
    ticker = str(b.get("ticker", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有Q2/Q3指引和材料耗材锚",
            "右尾弹性优先": "A先进节点材料右尾更清楚",
            "风险调整收益": "A利润质量/FCF相对更均衡",
            "下行保护优先": "A耗材POR粘性提供底盘",
            "估值消化优先": "A利润兑现更能吸收估值",
            "近端催化优先": "A有过滤/FOUP/MS高端验证",
            "价格确认/动量": "A价格已确认材料重估",
            "激进短线": "A高IV和先进材料题材更活跃",
        }[strategy]

    if winner == "B":
        if ticker in DIRECT_PEERS or rel == "直接同业":
            return {
                "NTM兑现优先": "B同业订单或收入路径更硬",
                "右尾弹性优先": "B同业小基数/材料右尾更大",
                "风险调整收益": "B同业估值和反证组合更优",
                "下行保护优先": "B同业现金流或估值缓冲更强",
                "估值消化优先": "B同业增长更能消化倍数",
                "近端催化优先": "B同业客户/产能节点更明确",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线弹性更高",
            }[strategy]
        if category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链收入确认更短链",
                "右尾弹性优先": "B直接AI右尾和小基数更大",
                "风险调整收益": "B上行空间更能覆盖风险",
                "下行保护优先": "B现金流/需求能见度更强",
                "估值消化优先": "B高增长更能消化估值",
                "近端催化优先": "B订单/产品催化更密集",
                "价格确认/动量": "B价格和资金确认更强",
                "激进短线": "B高beta叙事更适合进攻",
            }[strategy]
        if category in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单/backlog兑现更清楚",
                "右尾弹性优先": "B AI电力/机电右尾更直接",
                "风险调整收益": "B订单与估值组合更优",
                "下行保护优先": "B现金流或防御属性更强",
                "估值消化优先": "B backlog兑现更能覆盖估值",
                "近端催化优先": "B项目/FID/产能催化更近",
                "价格确认/动量": "B价格趋势确认更强",
                "激进短线": "B事件弹性和关注度更高",
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
    at = str(a["tiers"][strategy])  # type: ignore[index]
    bt = str(b["tiers"][strategy])  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    score_diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
    tier_diff = tier_value(at) - tier_value(bt)
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
    return f"{tag}：{reason_for(strategy, winner, b, rel)}"


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
        float(a["scores"]["NTM兑现优先"]) * 0.9
        + float(a["scores"]["风险调整收益"]) * 0.8
        + float(a["scores"]["估值消化优先"]) * 0.7
        + float(a["scores"]["近端催化优先"]) * 0.5
        - float(b["scores"]["NTM兑现优先"]) * 0.9
        - float(b["scores"]["风险调整收益"]) * 0.8
        - float(b["scores"]["估值消化优先"]) * 0.7
        - float(b["scores"]["近端催化优先"]) * 0.5
    )
    return "A" if quality_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if float(a["scores"]["NTM兑现优先"]) - float(b["scores"]["NTM兑现优先"]) > 10:
            return "ENTG有Q2/Q3收入可见度、APS/MS高端材料和FCF路径，B的NTM兑现更弱。"
        if float(a["scores"]["价格确认/动量"]) - float(b["scores"]["价格确认/动量"]) > 12:
            return "ENTG近期价格已明显确认先进材料重估，B的价格证据不足。"
        if float(a["scores"]["近端催化优先"]) - float(b["scores"]["近端催化优先"]) > 8:
            return "ENTG的液体过滤、FOUP、advanced deposition/CMP和Q2/Q3节点更可验证。"
        return "ENTG在先进节点材料兑现、价格确认或利润质量上略胜，B的右尾证据不足以覆盖反证。"

    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于ENTG。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 12:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比ENTG更硬。"
    if float(b["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"]) > 10:
        return f"{b['ticker']}的估值、现金流或下行风险组合优于ENTG。"
    if float(b["scores"]["价格确认/动量"]) - float(a["scores"]["价格确认/动量"]) > 12:
        return f"{b['ticker']}的价格确认和短线资金偏好明显强于ENTG。"
    return f"{b['ticker']}在多数投资思路下比ENTG更符合项目内资金配置目标。"


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
            float(a["scores"]["NTM兑现优先"]) - float(row["b"]["scores"]["NTM兑现优先"]),  # type: ignore[index]
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
    price = fin.get("price")
    close_0603 = mom2.get("latest_close")
    post_interval = "缺失"
    if price is not None and close_0603:
        post_interval = fmt_pct((float(price) / float(close_0603) - 1) * 100)
    daily_snapshot = (
        f"2026-06-22收盘价 `{fmt_num(fin.get('price'))}`，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"P/S `{fmt_num(fin.get('ps'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`，Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03过去两周 `{fmt_pct(mom2.get('mom2w'))}`，过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04三段SOXX压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`；"
        f"从2026-06-03收盘到2026-06-22收盘约 `{post_interval}`。"
    )

    product_names = []
    for product in a["products"]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])
        if len(product_names) >= 8:
            break

    support = {
        "NTM兑现优先": (
            "2026Q1净销售`8.119亿美元`、Q2指引中点`8.30亿美元`、Q3可见度约再环比`+5%`，基准收入`34.5-36.0亿美元`",
            "产品线拆分缺少完整披露，capex-driven收入和客户POR确认仍可能滞后",
        ),
        "右尾弹性优先": (
            "液体/气体过滤、FOUP、高纯fluid handling、advanced deposition、CMP/clean和advanced packaging都受益先进节点/HBM/封装",
            "极度乐观仍需WFE、先进逻辑、DRAM/HBM、客户POR、制造利用率和价格/mix同步成立，MOR/EUV不进基准",
        ),
        "风险调整收益": (
            "APS/MS高端mix、segment profit和FCF支撑经营质量，Q1 FCF约`1.42-1.44亿美元`",
            "2026-06-22 Forward PE约`39.8x`、P/S约`8.66x`、Call IV约`82.9%`，净杠杆约`3.6x`压制赔率",
        ),
        "下行保护优先": (
            "高纯材料耗材、客户认证和POR粘性比一次性项目收入更稳定",
            "三段SOXX压力窗口累计`-89.47%`弱于SOXX，IV高且债务/working capital会放大压力期波动",
        ),
        "估值消化优先": (
            "基准EBITDA`9.5-10.2亿美元`、FCF`4.8-6.0亿美元`，若Q2/Q3兑现可支撑部分高估值",
            "当前价格已抬升至高倍数，基准增速`+7%-11%`不足以无压力消化估值，需乐观情景继续兑现",
        ),
        "近端催化优先": (
            "Q2实际、Q3收入节奏、liquid filtration record、FOUP三年高点、advanced deposition/selective etch/CMP评论可在1-2季验证",
            "缺少明确backlog/RPO和产品线订单金额，MOR/EUV及Colorado/KSP更多是后续跟踪",
        ),
        "价格确认/动量": (
            "2026-06-22收盘`184.00`较2026-06-03收盘`140.33`约上涨`31.12%`，价格已明显确认材料重估",
            "正式区间涨跌文件仍停在2026-06-03；高IV和估值抬升意味着动量可能已有透支",
        ),
        "激进短线": (
            "高IV、6月以来价格爆发、先进材料/HBM/先进封装/MOR题材让短线进攻性高于普通材料股",
            "公司体量和收入增速仍低于小基数AI主链，强波动下容易受估值回撤和SOXX压力拖累",
        ),
    }

    lines: list[str] = []
    lines += [
        "# ENTG 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：ENTG / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV为2026-06-22；两周/一月区间涨跌为2026-06-03；SOXX压力窗口为2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 ENTG vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；ENTG 的 MOR/EUV、advanced packaging 和高端材料只按评估文件中可收入化口径处理，不把AI芯片/先进封装行业总需求直接并入公司收入。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ENTG 相对最强的是 NTM兑现、价格确认/动量和先进材料右尾：公司有Q2/Q3可见度、APS/MS高端材料收入锚，且6月价格已经大幅确认先进材料重估。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是风险调整、下行保护和估值消化：估值/IV已经很高，SOXX压力窗口表现弱，净杠杆和working capital使压力期缓冲有限。",
        "- A 最适合的投资者画像：想买半导体上游高纯材料、过滤、前驱体、CMP/clean和先进封装耗材的中期兑现，同时接受高估值和高波动的制造链配置者。",
        "- A 最不适合的投资者画像：只追求最低回撤、低IV、低估值现金流，或只愿意买直接AI芯片/光模块/服务器订单的高右尾进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(row['ticker']) for row in strong_b_rows[:10]])}。这些公司通常有更直接AI收入化、更大右尾、更强风险收益组合或更硬订单/RPO/backlog。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：ENTG 是项目内半导体材料链中有质量和近端兑现的一档，但不是全项目最强右尾或最安全标的；面对材料/弱证据公司可胜出，面对NVDA/AVGO/MU/TSM/光互联/NeoCloud/强电力机电等直接AI主链和强订单公司通常落后。",
        "- 后续最重要跟踪数据：Q2实际收入和GM、Q3收入是否接近约`8.7亿美元`节奏、APS/MS segment profit margin、liquid filtration、FOUP、gas filtration、advanced deposition、CMP/selective etch、advanced packaging run-rate、capex-driven revenue、FCF/working capital、净杠杆、MOR/EUV客户验证是否从license变成pilot revenue。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ENTG"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`34.5-36.0 亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI芯片需求必须先变成先进逻辑/DRAM/HBM/NAND/先进封装真实wafer starts、工具安装、客户POR/qualification和材料收入确认，才能进入ENTG收入。"]),
        base.row(["最大反证", "GPU/HBM/CoWoS总需求不能直接映射为ENTG收入；MOR/EUV和full-scale hybrid bonding仍属远期期权；高估值、高IV和SOXX压力期弱表现构成市场反证。"]),
        base.row(["近端催化剂", "Q2实际收入/GM、Q3收入节奏、液体过滤是否继续record、FOUP/fluid handling恢复、advanced deposition/selective etch/CMP评论、advanced packaging run-rate、FCF和净杠杆。"]),
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
        base.row(["直接同业", "同属半导体材料、电子化学品、高纯材料、基板/光罩/晶圆/特种材料，优先比较客户POR、收入兑现、产品代际、利润率和估值。", "Q、SHECY、SOMMY、ASGLY、HOCPY、AJNMY、AXTI", "同业证据权重最高；若B在先进节点材料、订单或估值消化上明显更强，可直接压过ENTG。"]),
        base.row(["相邻替代", "同属材料、工业气体、水处理、生命科学/工业材料或半导体供应链资金篮子，但产品不完全竞争。", "APD、LIN、DD、ECL、DHR、TMO、NDSN、MMM", "重点比较增长质量、现金流、估值消化和可见催化，不因材料属性相近就忽略AI收入链差异。"]),
        base.row(["上下游", "B处于ENTG材料需求链的晶圆制造、前道设备、封测、AI芯片、光互联、服务器或云算力下游。", "TSM、ASML、AMAT、LRCX、NVDA、AVGO、MU、SMCI、MSFT", "不把下游AI capex自动映射为ENTG收入；若B直接捕获利润池和订单，结论力度可更强。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "VRT、ETN、CEG、RKLB、TSLA、CRWD", "默认降低结论力度；除非档位差明显，否则优先微倾向或中性。"]),
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
        need = "需要ENTG把先进节点材料、过滤/CMP/clean或advanced packaging从趋势评论转成更高收入增速、订单金额、客户POR和利润率上修。"
        if comparison["rel"] == "直接同业":
            need = "需要ENTG在直接材料同业中证明更高客户POR份额、更强产品代际、利润率和更低估值反证。"
        elif comparison["rel"] == "上下游":
            need = "需要ENTG证明能实际捕获下游AI芯片/晶圆制造利润池，而不是只有间接受益和小额overlay。"
        elif comparison["rel"] == "跨赛道":
            need = "需要ENTG用更硬的订单、价格持续性和现金流去抵消跨赛道公司的高增长或强防守属性。"
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
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/ENTG_Entegris_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装湿化学与表面处理材料_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体高纯水、气体与化学流体系统_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_AI芯片前道制造设备_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV或正式金融行的公司为 {('、'.join(missing_fin) if missing_fin else '无')}。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_entg_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对同号百分比区间做修正，应用项目已有强公司校准，并对ENTG的Q2/Q3可见度、APS/MS高端材料、估值/IV、SOXX压力窗口和6月价格确认做人工校准后建档。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    base.TARGET = "ALLE"
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 ENTG 正式评估文件")
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
                "entg_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "entg_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "entg_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
