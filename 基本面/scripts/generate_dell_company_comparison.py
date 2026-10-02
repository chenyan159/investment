from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_cls_company_comparison as cls_calibrated


TARGET = "DELL"
TARGET_NAME = "Dell Technologies"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "DELL_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "HPE",
    "SMCI",
    "PENG",
    "JBL",
    "FLEX",
    "SANM",
    "CLS",
    "FN",
}
SERVER_STORAGE_ADJACENT = {
    "NTAP",
    "PSTG",
    "STX",
    "WDC",
    "SNDK",
    "RMBS",
    "SIMO",
    "MRAM",
    "MU",
}
UPSTREAM_CHIP_NETWORK = {
    "NVDA",
    "AMD",
    "AVGO",
    "MRVL",
    "INTC",
    "ARM",
    "QCOM",
    "ANET",
    "CSCO",
    "CIEN",
    "ALAB",
    "CRDO",
    "COHR",
    "LITE",
    "AAOI",
    "APH",
    "BDC",
    "BELFB",
    "MTSI",
    "SMTC",
    "TEL",
    "VIAV",
}
DOWNSTREAM_CLOUD = {
    "AMZN",
    "MSFT",
    "GOOGL",
    "META",
    "ORCL",
    "BABA",
    "IBM",
    "EQIX",
    "DLR",
    "CRWV",
    "APLD",
    "IREN",
    "NBIS",
    "NTNX",
    "ADBE",
    "CRWD",
}
POWER_COOLING_CHAIN = {
    "VRT",
    "ETN",
    "GEV",
    "CEG",
    "VST",
    "AEP",
    "DTE",
    "ETR",
    "PWR",
    "EME",
    "FIX",
    "IESC",
    "MYRG",
    "AAON",
    "TT",
    "MOD",
    "CARR",
    "JCI",
    "DKILY",
    "POWL",
    "HUBB",
    "NVT",
    "ABBNY",
    "AEIS",
    "POWI",
    "VICR",
}

EXTRA_SCORE_FLOORS = {
    **calibrated.SCORE_FLOORS,
    **cls_calibrated.EXTRA_SCORE_FLOORS,
    "CLS": cls_calibrated.CLS_SCORE_OVERRIDES,
    # CRWV's formal report needs explicit calibration: very high backlog/RPO
    # and short-term optionality, but weak downside/FCF quality.
    "CRWV": {
        "NTM兑现优先": 92,
        "右尾弹性优先": 100,
        "风险调整收益": 56,
        "下行保护优先": 35,
        "估值消化优先": 63,
        "近端催化优先": 86,
        "价格确认/动量": 60,
        "激进短线": 100,
    },
    "CSCO": {
        "NTM兑现优先": 72,
        "右尾弹性优先": 55,
        "风险调整收益": 82,
        "下行保护优先": 90,
        "估值消化优先": 64,
        "近端催化优先": 70,
        "价格确认/动量": 76,
        "激进短线": 66,
    },
    "CIEN": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 78,
        "风险调整收益": 64,
        "下行保护优先": 58,
        "估值消化优先": 68,
        "近端催化优先": 84,
        "价格确认/动量": 74,
        "激进短线": 80,
    },
}

DELL_OVERRIDES = {
    "NTM兑现优先": 86.0,
    "右尾弹性优先": 78.0,
    "风险调整收益": 68.0,
    "下行保护优先": 74.0,
    "估值消化优先": 82.0,
    "近端催化优先": 84.0,
    "价格确认/动量": 96.0,
    "激进短线": 88.0,
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    calibrated.fix_growth_ranges(companies)
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in EXTRA_SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    for strategy, score in DELL_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    calibrated.recompute_tiers(companies)


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in SERVER_STORAGE_ADJACENT or category == "AI服务器_存储_EMS":
        return "相邻替代"
    if ticker in UPSTREAM_CHIP_NETWORK or ticker in DOWNSTREAM_CLOUD or ticker in POWER_COOLING_CHAIN:
        return "上下游"
    if category in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in INFRA_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, winner: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有AI订单、backlog和FY2027指引硬锚",
            "右尾弹性优先": "A的AI服务器和整柜收入右尾更大",
            "风险调整收益": "A增长、估值和现金流组合更均衡",
            "下行保护优先": "A低P/S、正现金流和客户底盘更稳",
            "估值消化优先": "A用高收入增速消化约20x远期PE",
            "近端催化优先": "A有AI订单、Q2指引和交付催化",
            "价格确认/动量": "A近月涨幅已强确认AI兑现",
            "激进短线": "A高IV叠加AI服务器主线更进攻",
        }[strategy]
    if winner == "B":
        if ticker in DIRECT_PEERS or category == "AI服务器_存储_EMS":
            return {
                "NTM兑现优先": "B同业订单或利润兑现更直接",
                "右尾弹性优先": "B同业小基数或利润弹性更大",
                "风险调整收益": "B同业估值/现金流组合更优",
                "下行保护优先": "B同业波动或压力期更稳",
                "估值消化优先": "B同业倍数更易被业绩消化",
                "近端催化优先": "B同业订单/财报催化更近",
                "价格确认/动量": "B同业价格趋势更强",
                "激进短线": "B同业短线弹性更高",
            }[strategy]
        if ticker in UPSTREAM_CHIP_NETWORK or category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链兑现或利润留存更强",
                "右尾弹性优先": "B上游瓶颈利润池右尾更大",
                "风险调整收益": "B上行更能覆盖执行风险",
                "下行保护优先": "B现金流/资产质量或波动更好",
                "估值消化优先": "B利润弹性更能消化估值",
                "近端催化优先": "B产品/订单催化更密集",
                "价格确认/动量": "B价格趋势和资金偏好更强",
                "激进短线": "B高beta叙事更适合进攻",
            }[strategy]
        if ticker in DOWNSTREAM_CLOUD:
            return {
                "NTM兑现优先": "B云/软件收入确认更稳",
                "右尾弹性优先": "B平台扩张或AI云右尾更大",
                "风险调整收益": "B盈利质量和资本结构更好",
                "下行保护优先": "B现金流、客户粘性或规模更稳",
                "估值消化优先": "B利润留存更能支撑估值",
                "近端催化优先": "B云订单或AI产品催化更近",
                "价格确认/动量": "B价格确认更强",
                "激进短线": "B市场关注或波动更集中",
            }[strategy]
        if ticker in POWER_COOLING_CHAIN or category in INFRA_CATS:
            return {
                "NTM兑现优先": "B电力/机电backlog兑现更清楚",
                "右尾弹性优先": "B设施瓶颈右尾更直接",
                "风险调整收益": "B订单和现金流赔率更好",
                "下行保护优先": "B防御现金流或订单粘性更强",
                "估值消化优先": "B用订单兑现消化估值更容易",
                "近端催化优先": "B订单/产能/财报催化更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化交易弹性更高",
            }[strategy]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景上行更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量或估值缓冲更好",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线波动和关注度更适合进攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "增长与估值/防守互抵"
    return "档位接近需再验证"


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    score_diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
    tier_diff = tier_value(str(at)) - tier_value(str(bt))
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
        if tag == "强烈建议投A" and abs(score_diff) < 38 and abs(tier_diff) < 4:
            tag = "建议投A"
        elif tag == "强烈建议投B" and abs(score_diff) < 38 and abs(tier_diff) < 4:
            tag = "建议投B"
        elif tag == "建议投A" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投A"
        elif tag == "建议投B" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投B"
    if rel == "直接同业" and abs(score_diff) >= 20 and tag.startswith("建议"):
        tag = "强烈" + tag
    return tag


def cell_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    tag = label_for(a, b, strategy, rel)
    winner = "A" if tag.endswith("投A") else "B" if tag.endswith("投B") else "N"
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
    a_count, b_count, _ = direction_counts(cells)
    if a_count > b_count:
        return "A"
    if b_count > a_count:
        return "B"
    key = (
        float(a["scores"]["NTM兑现优先"])
        + float(a["scores"]["右尾弹性优先"])
        + float(a["scores"]["风险调整收益"])
        + float(a["scores"]["估值消化优先"])
        + float(a["scores"]["近端催化优先"])
        - float(b["scores"]["NTM兑现优先"])
        - float(b["scores"]["右尾弹性优先"])
        - float(b["scores"]["风险调整收益"])
        - float(b["scores"]["估值消化优先"])
        - float(b["scores"]["近端催化优先"])
    )
    return "A" if key >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    ticker = str(b["ticker"])
    if final == "A":
        if float(a["scores"]["NTM兑现优先"]) - float(b["scores"]["NTM兑现优先"]) > 12:
            return "DELL 的AI订单、backlog和FY2027收入指引让NTM兑现更硬。"
        if float(a["scores"]["估值消化优先"]) - float(b["scores"]["估值消化优先"]) > 12:
            return "DELL 的低P/S、约20x远期PE和高收入增速使估值消化更顺。"
        if float(a["scores"]["价格确认/动量"]) - float(b["scores"]["价格确认/动量"]) > 12:
            return "DELL 的6月价格确认和AI服务器主线资金偏好更强。"
        return "DELL 在收入兑现、估值消化、近端催化和动量组合上更均衡。"
    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 12:
        return f"{ticker} 的右尾或瓶颈利润池弹性明显大于 DELL。"
    if float(b["scores"]["下行保护优先"]) - float(a["scores"]["下行保护优先"]) > 12:
        return f"{ticker} 的现金流、估值缓冲或压力期防守强于 DELL。"
    if float(b["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"]) > 10:
        return f"{ticker} 的上行/下行组合比 DELL 的低毛利AI服务器模式更好。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 10:
        return f"{ticker} 的NTM订单/收入兑现证据强于 DELL。"
    return f"{ticker} 在多数投资思路下比 DELL 更符合当前配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    short = {
        "NTM兑现优先": "NTM",
        "右尾弹性优先": "右尾",
        "风险调整收益": "风险收益",
        "下行保护优先": "下行",
        "估值消化优先": "估值",
        "近端催化优先": "催化",
        "价格确认/动量": "动量",
        "激进短线": "短线",
    }
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
        if diff >= 8:
            a_strong.append(short[strategy])
        elif diff <= -8:
            b_strong.append(short[strategy])
        else:
            close.append(short[strategy])

    def joined(items: list[str]) -> str:
        if not items:
            return "无"
        return "、".join(items[:4]) + ("等" if len(items) > 4 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    rows: list[dict[str, object]] = []
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    for ticker in sorted(t for t in companies if t != TARGET):
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
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
                "rel_order": rel_order.get(rel, 9),
            }
        )
    return sorted(rows, key=lambda item: (item["rel_order"], str(item["ticker"])))


def fmt_num(value: object, digits: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return str(value)


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    return f"${float(value):.2f}B"


def fmt_pct(value: object, signed: bool = False) -> str:
    if value is None:
        return "缺失"
    if signed:
        return f"{float(value):+.2f}%"
    return f"{float(value):.2f}%"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def win_strategies(comparison: dict[str, object], side: str) -> list[str]:
    cells = comparison["cells"]  # type: ignore[assignment]
    out = []
    for strategy, cell in zip(STRATS, cells):
        tag = base.tag_in_cell(str(cell)) or ""
        if side == "A" and tag.endswith("投A"):
            out.append(strategy)
        elif side == "B" and tag.endswith("投B"):
            out.append(strategy)
    return out


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    date_range = f"{min(str(c['date']) for c in companies.values())} 至 {max(str(c['date']) for c in companies.values())}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(str(cell))] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]

    strong_b = sorted(
        [c for c in comparisons if c["final"] == "B"],
        key=lambda x: (int(x["bc"]) - int(x["ac"]), int(x["bc"]), float(x["b"]["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"])),  # type: ignore[index]
        reverse=True,
    )[:45]
    strong_a = sorted(
        [c for c in comparisons if c["final"] == "A"],
        key=lambda x: (int(x["ac"]) - int(x["bc"]), int(x["ac"]), float(a["scores"]["NTM兑现优先"]) + float(a["scores"]["估值消化优先"]) - float(x["b"]["scores"]["NTM兑现优先"]) - float(x["b"]["scores"]["估值消化优先"])),  # type: ignore[index]
        reverse=True,
    )[:45]
    final_a = sum(1 for c in comparisons if c["final"] == "A")
    final_b = sum(1 for c in comparisons if c["final"] == "B")
    missing_fin = sorted(
        ticker
        for ticker, company in companies.items()
        if not company.get("fin") or not company["fin"].get("price")  # type: ignore[union-attr]
    )
    file_list = "；".join(f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies))  # type: ignore[union-attr]

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'), True)}、过去一月 {fmt_pct(mom1.get('mom1m'), True)}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'), True)}。"
    )
    products = [str(p[0]).split("：")[0] for p in a["products"][:7]]  # type: ignore[index]
    rank_text = {
        strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]
        for strategy in STRATS
    }
    support = {
        "NTM兑现优先": (
            "FY2027 Q1收入438.42亿美元、FY2027收入指引1650-1690亿美元、AI server收入指引约600亿美元、AI订单244亿美元、AI backlog 513亿美元",
            "收入兑现依赖GPU/HBM/DRAM/NAND allocation、客户数据中心ready、液冷/电力验收和营运资本周转",
        ),
        "右尾弹性优先": (
            "乐观收入1850-2050亿美元、极度乐观2150-2400亿美元；整柜AI、PowerRack/PowerCool、GB300/B300/Rubin和AI storage attach提供上限",
            "大基数、GPU pass-through和低毛利属性限制市值弹性，极度乐观需要订单和交付多季度重复",
        ),
        "风险调整收益": (
            "2026-06-22 P/S 2.02、Forward PE 19.61，配合25%-33%基准收入增速，赔率优于多数高倍数AI链公司",
            "AI server mix压毛利率，库存/应收/供应链融资放大，客户/NeoCloud融资和交付延期是主要反证",
        ),
        "下行保护优先": (
            "CSG商用PC、storage、services和正现金流提供底盘，SOXX压力窗口累计-34.34%好于多数高beta硬件链",
            "Call IV 74.3%、P/B为负、AI大单营运资本波动和硬件低毛利使其不是低波动防守资产",
        ),
        "估值消化优先": (
            "低P/S、约20x Forward PE、FY2027 AI server收入约600亿美元和净利润115-135亿美元基准能支撑消化",
            "若AI server只是低毛利pass-through或库存/应收扩大，利润和FCF无法同步消化股价",
        ),
        "近端催化优先": (
            "未来1-2季可跟踪AI orders、AI server revenue、backlog、FY2027 Q2指引、storage增长、ISG margin和客户数据中心验收",
            "催化从订单到收入仍要经过组件供应、整柜测试、通电、液冷和客户验收，任何延迟都会推后确认",
        ),
        "价格确认/动量": (
            "截至2026-06-03过去两周+73.33%、过去1个月+100.35%，2026-06-22价格仍接近6月初高位",
            "涨幅已大，后续必须由订单/backlog、margin和FCF继续确认，不能只靠主题交易延续",
        ),
        "激进短线": (
            "高IV、强动量、AI server主线、GB300/NVL72/PowerRack和大客户项目形成短线事件弹性",
            "大市值和低毛利硬件属性使爆发力不如小基数光互联、NeoCloud或存储周期弹性股",
        ),
    }

    out: list[str] = [
        "# DELL 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：DELL / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 DELL vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。DELL 的优势来自 AI server 订单/backlog、FY2027 指引、低P/S/合理Forward PE、近月价格强确认和可跟踪的Q2/Q3收入催化。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 AI server pass-through 低毛利、营运资本/库存/应收放大、客户数据中心ready和融资约束，以及大基数限制极端右尾。",
        "- A 最适合的投资者画像：希望买到 AI server 与整柜交付主线、同时不愿支付纯芯片/光互联高倍数的中高风险配置型资金。",
        "- A 最不适合的投资者画像：只追求小市值极端右尾、上游瓶颈利润率，或要求低IV、低回撤、公用事业式防守的资金。",
        f"- 多数思路下最强反方公司：{'、'.join(str(x['ticker']) for x in strong_b[:12])}。这些公司通常在芯片/存储/光互联瓶颈利润、右尾、下行保护或短线高beta上压过 DELL。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：DELL 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；属于全项目 AI 基础设施兑现和估值消化强势档，但不是全项目最稀缺利润池或最强短线小基数弹性。",
        "- 后续最重要跟踪数据：AI server orders、AI server revenue、AI backlog、FY2027 Q2/Q3 revenue guide、ISG operating margin、gross margin、storage growth、services attach、inventory/accounts receivable/accounts payable、operating cash flow/free cash flow、GPU/HBM/DRAM/NAND allocation、客户通电/验收和NeoCloud融资。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "DELL"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(products)]),
        base.row(["NTM 基准收入", a["base_rev"] or "1680-1780亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；净利润/EBITDA：{a['base_profit']}；现金流：{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI server backlog 转收入的瓶颈不是需求本身，而是 GPU/HBM/DRAM/NAND、客户数据中心 ready、液冷/电力/验收、订单融资和营运资本周转。"]),
        base.row(["最大反证", "AI mix 拉低毛利率、库存/应收扩大、客户项目延期、NeoCloud融资或利用率恶化、ISG margin跌破关键区间。"]),
        base.row(["近端催化剂", "AI server orders/revenue/backlog、FY2027 Q2-Q3指引、GB300/NVL72/PowerRack客户交付、storage/services attach、ISG margin和FCF。"]),
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
        base.row(["直接同业", "与 DELL 在 AI server、rack-scale AI、服务器/存储系统、EMS/OEM/ODM 或系统交付收入池高度重叠，优先比较订单、backlog、收入确认、毛利率、客户质量和估值。", "HPE、SMCI、PENG、JBL、FLEX、SANM、CLS、FN", "同业证据权重最高；若对手在收入兑现或利润质量明显胜出，可给建议或强烈建议。"]),
        base.row(["相邻替代", "同属 AI server、enterprise storage、存储周期或AI基础设施硬件配置篮子，但产品/利润池不完全重叠。", "NTAP、PSTG、STX、WDC、SNDK、RMBS、SIMO、MU", "重点看资金只能买一个时，谁的增长质量、估值消化和风险调整后收益更好。"]),
        base.row(["上下游", "B 是 DELL 的GPU/ASIC/网络/光互联/电力/液冷/云客户/IDC链条上下游，重点区分系统收入、上游瓶颈利润和下游资本开支。", "NVDA、AMD、AVGO、MRVL、ANET、MSFT、AMZN、CRWV、VRT、ETN、CEG", "不把云capex或上游供给稀缺直接等同于DELL收入；比较利润捕获、议价权和交付风险。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、估值消化、下行保护和催化可见度。", "半导体材料、前道设备、封测、工业与化学品公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
                    majority(int(comparison["ac"]), int(comparison["bc"]), int(comparison["nc"])),
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b, start=1):
        b = comparison["b"]
        wins = win_strategies(comparison, "B")
        need = "DELL 需要证明AI订单持续高于收入、backlog稳定、ISG margin/FCF不被低毛利硬件和营运资本吞噬。"
        if "右尾弹性优先" in wins:
            need = "DELL 需要把GB300/Rubin、整柜液冷、storage/services attach转成更高毛利的可重复订单，而不是只扩大低毛利收入。"
        if "下行保护优先" in wins:
            need = "DELL 需要降低IV和压力窗口回撤，证明营运资本、库存和客户融资没有放大下行。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a, start=1):
        b = comparison["b"]
        wins = win_strategies(comparison, "A")
        need = "B 需要拿出更硬的NTM订单/RPO、利润率、FCF和价格确认，或证明其右尾不只是叙事。"
        if "下行保护优先" in wins and "估值消化优先" in wins:
            need = "B 需要同时改善估值消化和下行保护，才能抵消DELL的低倍数、高收入能见度和价格确认。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 公司索引来源：`公司调研/公司索引.md`，用于公司名称和分类目录校验。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖情况见金融资料；本次公司全集中缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/AI服务器_存储_EMS/DELL_Dell Technologies_公司调研_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI服务器整机与机架集成_2026-06-10.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI-native存储与KV Cache基础设施_2026-06-10.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 外部 sanity check：运行中查看了 Dell Investor Relations 最新新闻/季度结果页面和公开行情页面，仅用于确认本地评估所引用的 Q1 FY2027 披露与最新市场语境仍匹配；主表不使用外部网页排序、券商评级或目标价。参考页：Dell IR <https://investors.delltechnologies.com/>；Dell quarterly results <https://investors.delltechnologies.com/financial-information/quarterly-results>；Yahoo Finance DELL quote <https://finance.yahoo.com/quote/DELL/>；Robinhood DELL quote <https://robinhood.com/us/en/stocks/DELL/>。",
        "- 自动化脚本：`scripts/generate_dell_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 DELL 的 AI server orders/backlog、FY2027指引、低估值、低毛利pass-through、营运资本、强动量和高IV做人工校准后建档；未读取下游量化目录、备份、临时目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit(f"缺少目标公司正式评估：{TARGET}")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "dell_tiers": companies[TARGET]["tiers"],
                "dell_ranks": companies[TARGET]["ranks"],
                "dell_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
