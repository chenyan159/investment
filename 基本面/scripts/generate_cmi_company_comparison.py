from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base

try:
    import generate_ceg_company_comparison as score_floor_source
except Exception:  # pragma: no cover - fallback only if the helper is removed later.
    score_floor_source = None


TARGET = "CMI"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CMI_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS
SCORE_FLOORS = getattr(score_floor_source, "SCORE_FLOORS", {}) if score_floor_source else {}


DIRECT_POWER_PEERS = {"CAT", "GEV", "GNRC", "PSIX", "RYCEY"}
ONSITE_POWER_SUBSTITUTES = {"BE", "FCEL", "SMR", "OKLO", "CEG", "VST"}
POWER_INFRA_ADJACENT = {
    "AEP",
    "ABBNY",
    "AEIS",
    "AMPX",
    "CARR",
    "DKILY",
    "DOV",
    "DTE",
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
UPSTREAM_FUEL_GRID = {"APD", "ET", "LIN"}
INDUSTRIAL_ADJACENT = {"DCI", "FTV", "MMM", "NDSN", "PNR", "TDY", "TMO", "DHR", "ECL"}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1]["scores"][strategy],  # type: ignore[index]
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
            company.setdefault("rank_total", {})[strategy] = total  # type: ignore[index]

    for company in companies.values():
        if not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"  # type: ignore[index]
                company.setdefault("ranks", {})[strategy] = None  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[union-attr]
            company["scores"][strategy] = max(current, floor)  # type: ignore[index]

    # CMI calibration from its formal assessment: strong FY2026 guidance and
    # Power Systems/Distribution power-generation revenue anchors, but lower
    # right-tail beta than CAT/GEV/BE and no disclosed data-center backlog.
    overrides = {
        "NTM兑现优先": 76.5,
        "右尾弹性优先": 63.0,
        "风险调整收益": 53.0,
        "下行保护优先": 76.0,
        "估值消化优先": 68.0,
        "近端催化优先": 64.0,
        "价格确认/动量": 60.5,
        "激进短线": 72.0,
    }
    for strategy, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_POWER_PEERS:
        return "直接同业"
    if ticker in DOWNSTREAM_AI_LOAD or ticker in UPSTREAM_FUEL_GRID:
        return "上下游"
    if ticker in ONSITE_POWER_SUBSTITUTES or ticker in POWER_INFRA_ADJACENT:
        return "相邻替代"
    if category in {"电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI", "配电_电源_功率器件"}:
        return "相邻替代"
    if ticker in INDUSTRIAL_ADJACENT:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, winner: str, company: dict[str, object], _diff: float) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if winner == "A":
        return {
            "NTM兑现优先": "A有FY2026指引和发电收入锚",
            "右尾弹性优先": "A数据中心发电期权更可收入化",
            "风险调整收益": "A估值现金流组合更均衡",
            "下行保护优先": "A成熟盈利和服务底盘更稳",
            "估值消化优先": "A低P/S和NTM业绩更易消化",
            "近端催化优先": "A发电收入和指引节点更近",
            "价格确认/动量": "A价格仍高于六月初锚点",
            "激进短线": "A电力叙事叠加IV仍可进攻",
        }[strategy]

    if winner == "B":
        if ticker in DIRECT_POWER_PEERS:
            return {
                "NTM兑现优先": "B同业订单/backlog兑现更硬",
                "右尾弹性优先": "B同业GW或设备右尾更大",
                "风险调整收益": "B同业赔率或估值更优",
                "下行保护优先": "B同业现金流或估值缓冲更厚",
                "估值消化优先": "B同业业绩更能覆盖估值",
                "近端催化优先": "B同业订单/交付节点更密集",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线弹性更高",
            }[strategy]
        if ticker in ONSITE_POWER_SUBSTITUTES or category == "电力_发电_能源_储能":
            return {
                "NTM兑现优先": "B电力资产或订单兑现更直接",
                "右尾弹性优先": "B电力右尾和重估弹性更大",
                "风险调整收益": "B上行和下行组合更好",
                "下行保护优先": "B现金流或电力资产更抗压",
                "估值消化优先": "B估值更容易被业绩消化",
                "近端催化优先": "B电力项目催化更明确",
                "价格确认/动量": "B价格确认更强",
                "激进短线": "B电力主题beta更高",
            }[strategy]
        if category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链订单兑现更短链",
                "右尾弹性优先": "B AI主链右尾更大",
                "风险调整收益": "B上行空间更能覆盖风险",
                "下行保护优先": "B需求能见度或现金流更强",
                "估值消化优先": "B高增长更能消化估值",
                "近端催化优先": "B产品/订单催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta更适合短线进攻",
            }[strategy]
        if category in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单和交付路径更清楚",
                "右尾弹性优先": "B电气设备右尾更直接",
                "风险调整收益": "B增长估值组合更优",
                "下行保护优先": "B订单粘性或利润更稳",
                "估值消化优先": "B订单兑现更能消化估值",
                "近端催化优先": "B订单/产能催化更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化交易弹性更强",
            }[strategy]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景上行更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量或估值缓冲更好",
            "估值消化优先": "B当前估值更易消化",
            "近端催化优先": "B近端催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线关注度更高",
        }[strategy]

    if strategy in {"价格确认/动量", "激进短线"}:
        return "动量或短线证据差距有限"
    if strategy in {"风险调整收益", "估值消化优先", "下行保护优先"}:
        return "估值安全边际互有强弱"
    return "档位接近需继续验证"


def label_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a["tiers"].get(strategy, "资料不足")  # type: ignore[union-attr]
    bt = b["tiers"].get(strategy, "资料不足")  # type: ignore[union-attr]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
    tier_gap = tier_value(str(at)) - tier_value(str(bt))
    abs_diff = abs(float(diff))
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 26, 13, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 23, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 20, 9, 4

    if diff > 0:
        if tier_gap >= 2 and abs_diff >= strong_cut:
            return "强烈建议投A"
        if tier_gap >= 1 and abs_diff >= suggest_cut:
            return "建议投A"
        if abs_diff >= micro_cut:
            return "微倾向投A"
    else:
        if tier_gap <= -2 and abs_diff >= strong_cut:
            return "强烈建议投B"
        if tier_gap <= -1 and abs_diff >= suggest_cut:
            return "建议投B"
        if abs_diff >= micro_cut:
            return "微倾向投B"
    return "中性"


def cell_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strategy, winner, b, float(diff))}"


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
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.15,
        "估值消化优先": 1.05,
        "下行保护优先": 0.95,
        "右尾弹性优先": 0.85,
        "近端催化优先": 0.80,
        "价格确认/动量": 0.45,
        "激进短线": 0.45,
    }
    label_score = {
        "强烈建议投A": 2.0,
        "建议投A": 1.35,
        "微倾向投A": 0.55,
        "中性": 0.0,
        "微倾向投B": -0.55,
        "建议投B": -1.35,
        "强烈建议投B": -2.0,
    }
    score = 0.0
    for strategy, cell in zip(STRATS, cells):
        score += weights[strategy] * label_score.get(base.tag_in_cell(cell) or "中性", 0.0)
    if score > 0.05:
        return "A"
    if score < -0.05:
        return "B"
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    diffs = {strategy: a["scores"][strategy] - b["scores"][strategy] for strategy in STRATS}  # type: ignore[index,operator]
    ticker = str(b["ticker"])
    category = str(b["category"])
    if final == "A":
        if diffs["NTM兑现优先"] > 12:
            return "CMI 的FY2026指引、Power Systems/Distribution发电收入和服务网络使NTM兑现更硬。"
        if diffs["估值消化优先"] > 10:
            return "CMI 的P/S、Forward PE和基准业绩路径比对手更容易消化当前估值。"
        if diffs["下行保护优先"] > 10:
            return "CMI 的成熟盈利、售后服务和多业务底盘提供更好的压力期缓冲。"
        if diffs["近端催化优先"] > 10:
            return "CMI 的发电收入、指引复核和Accelera减亏更可能在近端被验证。"
        return "CMI 在可见收入、现金流和估值消化之间更均衡，对手右尾证据不足以压过。"

    if diffs["右尾弹性优先"] < -16 and category in HIGH_GROWTH_CATS:
        return f"{ticker} 的AI主链右尾和小基数弹性明显强于CMI的电力设备传导。"
    if diffs["右尾弹性优先"] < -16 and (category in INFRA_CATS or ticker in ONSITE_POWER_SUBSTITUTES):
        return f"{ticker} 的AI电力/基础设施右尾或订单重定价弹性强于CMI。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker} 的NTM订单、收入或利润兑现链条比CMI更短。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker} 的上行/估值/现金流组合比CMI更优。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker} 的价格确认和短线资金偏好强于CMI。"
    return f"{ticker} 在多数投资思路下比CMI更符合当前项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        av = tier_value(a["tiers"].get(strategy))  # type: ignore[union-attr]
        bv = tier_value(b["tiers"].get(strategy))  # type: ignore[union-attr]
        label = strategy.replace("优先", "").replace("/动量", "动量")
        if av > bv:
            a_strong.append(label)
        elif av < bv:
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
        cells = [cell_for(strategy, a, b, rel) for strategy in STRATS]
        ac, bc, nc = direction_counts(cells)
        final = final_choice(a, b, cells)
        output.append(
            {
                "ticker": ticker,
                "b": b,
                "rel": rel,
                "cells": cells,
                "ac": ac,
                "bc": bc,
                "nc": nc,
                "final": final,
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(output, key=lambda item: (rel_order.get(str(item["rel"]), 9), str(item["ticker"])))


def fmt_num(value: object, decimals: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
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
        return f"{float(value):+.2f}%"
    except Exception:
        return "缺失"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def top_majority(comparisons: list[dict[str, object]], final: str, limit: int = 45) -> list[dict[str, object]]:
    rows = [row_obj for row_obj in comparisons if row_obj["final"] == final]
    if final == "B":
        rows.sort(key=lambda row_obj: (row_obj["bc"] - row_obj["ac"], row_obj["bc"], -row_obj["nc"]), reverse=True)  # type: ignore[operator]
    else:
        rows.sort(key=lambda row_obj: (row_obj["ac"] - row_obj["bc"], row_obj["ac"], -row_obj["nc"]), reverse=True)  # type: ignore[operator]
    return rows[:limit]


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"

    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy])[:3]
    strong_b_rows = top_majority(comparisons, "B")
    strong_a_rows = top_majority(comparisons, "A")
    final_a = sum(1 for comparison in comparisons if comparison["final"] == "A")
    final_b = sum(1 for comparison in comparisons if comparison["final"] == "B")
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
        f"Call IV {fmt_num(fin.get('call_iv'), 1)}%，Put IV {fmt_num(fin.get('put_iv'), 1)}%；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )
    product_names = [str(product[0]).split("，")[0].split("；")[0] for product in a["products"][:7]]  # type: ignore[index]
    rank_text = {strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档" for strategy in STRATS}  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]

    support = {
        "NTM兑现优先": (
            "FY2026收入指引+8%-+11%、EBITDA margin 17.75%-18.50%，NTM基准收入约$37.5-$38.5B；Power Systems与Distribution发电收入已在报表体现",
            "CMI未披露数据中心收入/backlog/book-to-bill，Engine/Components仍受truck cycle影响",
        ),
        "右尾弹性优先": (
            "乐观收入约$39.2-$40.8B、极度乐观$41.8-$43.5B；大型数据中心genset、天然气prime power、Distribution服务和Accelera减亏提供右尾",
            "公司基数大，客户/MW/backlog证据少于CAT/GEV/BE等更高beta电力标的",
        ),
        "风险调整收益": (
            "Forward PE 21.37、P/S 2.95，基准EBITDA约$6.8-$7.2B，成熟盈利和服务网络给出基本赔率",
            "2026-06-04压力窗口累计-39.00%，P/B 8.10且股价已重估，关税/材料/产能爬坡会侵蚀利润",
        ),
        "下行保护优先": (
            "Engine、Components、Distribution、Power Systems和售后服务形成多业务底盘，自由现金流方向为正",
            "周期制造属性仍强，SOXX压力窗口回撤较深，Accelera亏损和大项目营运资本会压低防御性",
        ),
        "估值消化优先": (
            "NTM基准收入+11%-+14%、EBITDA约18%上下，与Forward PE 21.37和P/S 2.95相比仍有消化路径",
            "当前价格已反映AI电力和Power Generation强势，若发电增速回落或truck恢复慢，倍数消化会变慢",
        ),
        "近端催化优先": (
            "未来1-2季可跟踪Power Systems power generation、Distribution power generation/service、FY2026指引复核、S17/large genset、天然气数据中心订单和Accelera减亏",
            "缺少已披露大型客户PO或数据中心backlog，天然气prime和BESS项目多数仍需客户/许可验证",
        ),
        "价格确认/动量": (
            "区间文件显示两周+1.86%、一月+3.79%，2026-06-22收盘价724.93高于6月3日682.33，价格继续确认电力链重估",
            "动量不如AI服务器、光互联、内存和部分电气设备，压力窗口历史回撤仍重",
        ),
        "激进短线": (
            "Call IV 42.2%、AI数据中心电力/自备发电叙事、发电机组供给瓶颈和近端财报节点给出事件交易弹性",
            "CMI是$100B级成熟工业股，短线爆发力低于小基数电力、核能开发、AI芯片和光互联高beta标的",
        ),
    }

    out: list[str] = [
        "# CMI 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：CMI / Cummins Inc",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 CMI vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。CMI 最适合用来买 AI 数据中心电力瓶颈里已经进入收入表的发电机组、Distribution 发电服务和成熟工业现金流，而不是买最高 beta 的AI主链右尾。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是未披露数据中心收入/backlog/客户清单，天然气 prime power 和 BESS 仍需订单验证，且成熟大市值制造公司的短线弹性天然低于高波动AI链。",
        "- A 最适合的投资者画像：希望配置 AI 电力/自备发电需求，但要求有FY2026指引、已确认收入、利润和现金流底座，同时不愿承担纯项目型小票或亏损型能源科技风险的资金。",
        "- A 最不适合的投资者画像：只追求最高增长、最强右尾、最快价格爆发或纯半导体/云算力主链弹性的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(row_obj['ticker']) for row_obj in strong_b_rows[:12]])}。这些公司通常在AI主链右尾、小基数电力弹性、订单backlog、估值消化或价格动量上压过CMI。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：CMI 是项目内中上偏强的AI电力硬件/工业现金流标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家。",
        "- 后续最重要跟踪数据：Power Systems power generation、Distribution power generation和service、Power Systems EBITDA margin、large genset lead time、数据中心客户/订单/backlog、天然气prime power项目、ATS/switchgear联动瓶颈、Engine/Components truck recovery、Accelera亏损、capex、营运资本和FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "CMI"]),
        base.row(["公司名称", "Cummins Inc"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "约 $37.5-$38.5B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "数据中心电力需求到CMI收入确认需要design-in、排产、工厂测试、ATS/并机、现场许可、燃气或柴油方案、施工和客户验收同步兑现。"]),
        base.row(["最大反证", "CMI未披露数据中心revenue、backlog、book-to-bill或客户清单；Engine/Components周期和Accelera亏损可能稀释Power Systems强势。"]),
        base.row(["近端催化剂", "Q2/Q3 Power Systems power generation、Distribution服务attach、FY2026指引复核、large genset交期、天然气prime power订单、S17系列、Accelera减亏和FCF。"]),
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
        base.row(["直接同业", "与 CMI 在数据中心 genset、备用/prime power、燃机/发动机、现场发电或全球服务网络上争夺相近需求池。", "CAT、GEV、GNRC、PSIX、RYCEY", "优先看订单/backlog、MW/GW项目、交付窗口、服务网络、利润率、估值和现金流；同业证据强时提高判断力度。"]),
        base.row(["相邻替代", "同属 AI 数据中心电力、配电、储能、核能、公用事业、冷却、工程或工业基础设施资金篮子，但产品不完全重叠。", "BE、CEG、VST、SMR、OKLO、ETN、VRT、PWR、POWL、AAON、TT、JCI", "回答资金只能买一个时谁的增长质量、利润捕获、估值消化和近端催化更好。"]),
        base.row(["上下游", "B 是AI负荷端、云/IDC资本开支端、服务器/ODM、燃气/工业气体/电网供给端，影响 CMI 订单但不等同于 CMI 收入。", "MSFT、AMZN、GOOGL、META、ORCL、EQIX、CRWV、DELL、SMCI、ET、LIN、APD", "区分下游收入规模和上游设备利润捕获，重点看议价权、收入确认链条和现金流质量。"]),
        base.row(["跨赛道", "半导体、设备、材料、软件、工业和消费平台等与 CMI 业务差异大，但作为项目内资金配置替代仍可比较。", "NVDA、AVGO、TSM、ASML、MU、CDNS、BABA", "默认降低结论力度；只有增长质量、估值消化、下行保护或价格确认明显拉开时才给建议/强烈建议。"]),
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
        need = "需要CMI披露更清晰的数据中心收入、客户PO、backlog/book-to-bill、large genset交付节奏和Power Systems margin持续性。"
        if "右尾弹性优先" in wins or "激进短线" in wins:
            need = "需要CMI把数据中心genset、天然气prime power和BESS/微电网从叙事转成可验证订单与利润上修。"
        if "估值消化优先" in wins or "风险调整收益" in wins:
            need = "需要CMI用FY2026后续指引、FCF和Accelera减亏证明当前股价不是只靠AI电力乐观情景支撑。"
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
        need = "需要B拿出同等强度的NTM收入/利润兑现、订单或客户合同，并证明估值和现金流能承受压力窗口。"
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
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/电力_发电_能源_储能/CMI_Cummins_Inc_公司调研_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_动态UPS、飞轮与超级电容_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 外部校验来源：Cummins 2026Q1 earnings release（FY2026收入+8%-+11%、EBITDA margin 17.75%-18.50%，https://investor.cummins.com/news/detail/694/cummins-delivered-strong-operating-results-and-returned）；Cummins 2026 Analyst Day / 2030 financial targets and large-engine capacity investment（https://investor.cummins.com/AnalystDay；https://investor.cummins.com/news/detail/696/cummins-raises-2030-financial-targets-announces）。",
        "- 自动化脚本：`scripts/generate_cmi_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对CMI的FY2026指引、Power Systems/Distribution发电收入、数据中心发电期权、估值、价格确认、truck cycle、Accelera亏损和未披露backlog限制做人工校准后建档；未读取下游量化目录或现成排序结论。",
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
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "cmi_tiers": {strategy: companies[TARGET]["tiers"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
                "cmi_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},  # type: ignore[index]
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
