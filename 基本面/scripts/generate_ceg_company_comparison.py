from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base


TARGET = "CEG"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CEG_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_POWER_PEERS = {"VST", "AEP", "DTE", "ETR"}
ADJACENT_POWER_ALTS = {
    "BE",
    "FCEL",
    "OKLO",
    "SMR",
    "GEV",
    "GNRC",
    "PSIX",
    "BWXT",
    "RYCEY",
    "FLNC",
    "AMPX",
    "CMI",
    "ENS",
    "HTHIY",
    "PWR",
    "ETN",
    "VRT",
    "POWL",
    "HUBB",
    "NVT",
    "ABBNY",
    "AEIS",
    "POWI",
    "VICR",
    "TT",
    "AAON",
    "CARR",
    "JCI",
    "MOD",
    "EME",
    "FIX",
    "IESC",
    "MYRG",
    "DKILY",
    "DOV",
    "PH",
    "TTDKY",
    "MRAAY",
}
UPSTREAM_DOWNSTREAM = {
    "MSFT",
    "META",
    "AMZN",
    "GOOGL",
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
    "DELL",
    "SMCI",
    "HPE",
    "JBL",
    "FLEX",
    "PENG",
    "SANM",
    "FN",
    "ET",
    "LIN",
    "APD",
}

SCORE_FLOORS = {
    # Core AI compute and semiconductor leaders whose eval files often use
    # absolute revenue ranges rather than explicit growth percentages.
    "NVDA": {
        "NTM兑现优先": 90,
        "右尾弹性优先": 92,
        "风险调整收益": 72,
        "下行保护优先": 82,
        "估值消化优先": 74,
        "近端催化优先": 88,
        "价格确认/动量": 65,
        "激进短线": 88,
    },
    "AVGO": {
        "NTM兑现优先": 92,
        "右尾弹性优先": 94,
        "风险调整收益": 72,
        "估值消化优先": 82,
        "近端催化优先": 82,
        "激进短线": 88,
    },
    "AMD": {
        "NTM兑现优先": 76,
        "右尾弹性优先": 86,
        "风险调整收益": 58,
        "估值消化优先": 58,
        "近端催化优先": 78,
        "价格确认/动量": 60,
        "激进短线": 84,
    },
    "MU": {
        "NTM兑现优先": 90,
        "右尾弹性优先": 92,
        "风险调整收益": 68,
        "估值消化优先": 84,
        "近端催化优先": 84,
        "价格确认/动量": 86,
        "激进短线": 90,
    },
    "TSM": {
        "NTM兑现优先": 86,
        "右尾弹性优先": 78,
        "风险调整收益": 70,
        "下行保护优先": 84,
        "估值消化优先": 74,
        "近端催化优先": 75,
        "价格确认/动量": 62,
        "激进短线": 72,
    },
    "ASML": {
        "NTM兑现优先": 80,
        "右尾弹性优先": 78,
        "风险调整收益": 62,
        "下行保护优先": 76,
        "估值消化优先": 60,
        "近端催化优先": 78,
        "价格确认/动量": 70,
        "激进短线": 80,
    },
    # Hyperscalers and AI platform companies.
    "MSFT": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 68,
        "风险调整收益": 74,
        "下行保护优先": 92,
        "估值消化优先": 70,
        "近端催化优先": 72,
        "价格确认/动量": 55,
        "激进短线": 60,
    },
    "AMZN": {
        "NTM兑现优先": 84,
        "右尾弹性优先": 76,
        "风险调整收益": 70,
        "下行保护优先": 82,
        "估值消化优先": 68,
        "近端催化优先": 76,
        "价格确认/动量": 60,
        "激进短线": 68,
    },
    "GOOGL": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 72,
        "风险调整收益": 72,
        "下行保护优先": 86,
        "估值消化优先": 72,
        "近端催化优先": 72,
        "价格确认/动量": 58,
        "激进短线": 64,
    },
    "META": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 74,
        "风险调整收益": 70,
        "下行保护优先": 82,
        "估值消化优先": 72,
        "近端催化优先": 74,
        "价格确认/动量": 62,
        "激进短线": 70,
    },
    "ORCL": {
        "NTM兑现优先": 80,
        "右尾弹性优先": 78,
        "风险调整收益": 62,
        "下行保护优先": 66,
        "估值消化优先": 62,
        "近端催化优先": 80,
        "价格确认/动量": 70,
        "激进短线": 78,
    },
    # AI power, electrical infrastructure and data-center equipment leaders.
    "VRT": {
        "NTM兑现优先": 86,
        "右尾弹性优先": 82,
        "风险调整收益": 58,
        "下行保护优先": 60,
        "估值消化优先": 54,
        "近端催化优先": 82,
        "价格确认/动量": 70,
        "激进短线": 84,
    },
    "ETN": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 74,
        "风险调整收益": 66,
        "下行保护优先": 84,
        "估值消化优先": 58,
        "近端催化优先": 78,
        "价格确认/动量": 70,
        "激进短线": 74,
    },
    "POWL": {
        "NTM兑现优先": 80,
        "右尾弹性优先": 80,
        "风险调整收益": 62,
        "估值消化优先": 66,
        "近端催化优先": 78,
        "价格确认/动量": 78,
        "激进短线": 86,
    },
    "HUBB": {
        "NTM兑现优先": 76,
        "右尾弹性优先": 68,
        "风险调整收益": 62,
        "下行保护优先": 78,
        "估值消化优先": 58,
        "近端催化优先": 72,
        "价格确认/动量": 68,
        "激进短线": 68,
    },
    "GEV": {
        "NTM兑现优先": 80,
        "右尾弹性优先": 80,
        "风险调整收益": 64,
        "下行保护优先": 70,
        "估值消化优先": 60,
        "近端催化优先": 80,
        "价格确认/动量": 70,
        "激进短线": 84,
    },
    "ANET": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 82,
        "风险调整收益": 66,
        "估值消化优先": 64,
        "近端催化优先": 80,
        "价格确认/动量": 70,
        "激进短线": 82,
    },
    # Nuclear development names have weaker NTM certainty than CEG, but their
    # right-tail and short-term beta should not be suppressed by no-revenue parsing.
    "OKLO": {
        "右尾弹性优先": 88,
        "近端催化优先": 70,
        "价格确认/动量": 78,
        "激进短线": 92,
    },
    "SMR": {
        "右尾弹性优先": 92,
        "近端催化优先": 74,
        "价格确认/动量": 78,
        "激进短线": 92,
    },
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def mid_growth(company: dict) -> float | None:
    if company.get("base_mid") is None or company.get("bear_mid") is None:
        return None
    try:
        if company["bear_mid"] <= 0:
            return None
        return (company["base_mid"] - company["bear_mid"]) / company["bear_mid"]
    except Exception:
        return None


def fix_growth_ranges(companies: dict[str, dict]) -> None:
    """Repair a few parser misses where Chinese punctuation or units hide ranges."""
    for company in companies.values():
        if company.get("base_mid") is not None and company.get("bull_mid") is not None:
            continue
        text = company.get("text", "")
        ranges: dict[str, tuple[float, float]] = {}
        for label, key in [
            ("悲观", "bear"),
            ("基准", "base"),
            ("乐观", "bull"),
            ("极度乐观", "extreme"),
        ]:
            m = re.search(rf"{label}[^0-9$￥\-]{{0,80}}(?:\$|￥)?\s*([0-9]+(?:\.[0-9]+)?)\s*[-~—至]\s*(?:\$|￥)?\s*([0-9]+(?:\.[0-9]+)?)", text)
            if m:
                ranges[key] = (float(m.group(1)), float(m.group(2)))
        for key, pair in ranges.items():
            company[f"{key}_range"] = pair
            company[f"{key}_mid"] = sum(pair) / 2


def recompute_tiers(companies: dict[str, dict]) -> None:
    for strat in STRATS:
        scored = [
            company.get("scores", {}).get(strat)
            for company in companies.values()
            if company.get("scores", {}).get(strat) is not None
        ]
        scored.sort(reverse=True)
        n = len(scored)
        if not n:
            continue
        cuts = {
            "S": scored[max(0, int(n * 0.08) - 1)],
            "A": scored[max(0, int(n * 0.25) - 1)],
            "B": scored[max(0, int(n * 0.55) - 1)],
            "C": scored[max(0, int(n * 0.80) - 1)],
        }
        for company in companies.values():
            score = company.get("scores", {}).get(strat)
            if score is None:
                tier = "资料不足"
            elif score >= cuts["S"]:
                tier = "S"
            elif score >= cuts["A"]:
                tier = "A"
            elif score >= cuts["B"]:
                tier = "B"
            elif score >= cuts["C"]:
                tier = "C"
            else:
                tier = "D"
            company.setdefault("tiers", {})[strat] = tier
            company.setdefault("ranks", {})[strat] = sum(1 for s in scored if s > score) + 1 if score is not None else None
            company.setdefault("rank_total", {})[strat] = n

    for company in companies.values():
        if not company.get("fin", {}).get("price"):
            for strat in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strat] = "资料不足"
                company.setdefault("ranks", {})[strat] = None


def score_companies(companies: dict[str, dict]) -> None:
    fix_growth_ranges(companies)
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strat, floor in floors.items():
            current = company.setdefault("scores", {}).get(strat, 0)
            company["scores"][strat] = max(current, floor)

    # CEG calibration: Constellation is a high-quality AI power and nuclear scarcity
    # compounder, with strong NTM anchors but weaker recent price confirmation.
    overrides = {
        "NTM兑现优先": 86.0,
        "右尾弹性优先": 76.0,
        "风险调整收益": 55.5,
        "下行保护优先": 64.0,
        "估值消化优先": 65.0,
        "近端催化优先": 68.0,
        "价格确认/动量": 39.0,
        "激进短线": 75.0,
    }
    for strat, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strat] = score
    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = company["ticker"]
    category = company.get("category", "")
    if ticker in DIRECT_POWER_PEERS:
        return "直接同业"
    if ticker in UPSTREAM_DOWNSTREAM:
        return "上下游"
    if ticker in ADJACENT_POWER_ALTS or category == "电力_发电_能源_储能":
        return "相邻替代"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict, diff: float) -> str:
    cat = company.get("category", "")
    ticker = company["ticker"]
    if winner == "A":
        return {
            "NTM兑现优先": "A有Q1收入/EPS指引和Calpine并表硬锚",
            "右尾弹性优先": "A核电长约与站点供电右尾稀缺",
            "风险调整收益": "A清洁电力资产和现金流赔率更均衡",
            "下行保护优先": "A核电/PTC/长约和发电底盘更稳",
            "估值消化优先": "A用FY2026 EPS更能消化估值",
            "近端催化优先": "A有Calpine整合和PPA审批节点",
            "价格确认/动量": "A核电重估线索强于对手弱势走势",
            "激进短线": "A核电AI电力叙事和IV仍有进攻性",
        }[strat]
    if winner == "B":
        if ticker in DIRECT_POWER_PEERS:
            peer = {
                "NTM兑现优先": "B同业现金流或2026兑现更短链",
                "右尾弹性优先": "B同业核电/容量重估弹性更直接",
                "风险调整收益": "B同业估值和FCF组合更优",
                "下行保护优先": "B同业现金流或估值缓冲更好",
                "估值消化优先": "B同业盈利倍数更容易消化",
                "近端催化优先": "B同业PPA/容量催化更直接",
                "价格确认/动量": "B同业价格确认强于CEG",
                "激进短线": "B同业短线弹性和资金关注更强",
            }
            return peer[strat]
        if cat in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链订单/RPO兑现更短链",
                "右尾弹性优先": "B AI主链右尾和小基数弹性更大",
                "风险调整收益": "B上行空间更能覆盖执行风险",
                "下行保护优先": "B需求能见度或现金流韧性更好",
                "估值消化优先": "B高速增长更能消化高倍数",
                "近端催化优先": "B近端产品/订单催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta和AI关注度更适合进攻",
            }[strat]
        if cat in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单 backlog 和交付路径更清楚",
                "右尾弹性优先": "B电气设备放量右尾更直接",
                "风险调整收益": "B增长和估值组合更优",
                "下行保护优先": "B订单粘性和利润稳定性更强",
                "估值消化优先": "B用订单兑现消化估值更容易",
                "近端催化优先": "B订单/产能/财报催化更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化交易弹性更强",
            }[strat]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景上行更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量或估值缓冲更好",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线波动和关注度更适合进攻",
        }[strat]
    return {
        "NTM兑现优先": "NTM证据接近",
        "右尾弹性优先": "右尾证据互有强弱",
        "风险调整收益": "赔率和风险接近",
        "下行保护优先": "防守证据接近",
        "估值消化优先": "估值消化差距不大",
        "近端催化优先": "近端催化强度接近",
        "价格确认/动量": "价格确认差距有限",
        "激进短线": "短线弹性差距有限",
    }[strat]


def label_for(strat: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strat, "资料不足")
    bt = b.get("tiers", {}).get(strat, "资料不足")
    if "资料不足" in (at, bt):
        return "中性"
    diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)

    if abs_diff < 4:
        return "中性"
    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 24, 12, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 22, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 19, 9, 4

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


def cell_for(strat: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strat, a, b, rel)
    diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strat, winner, b, diff)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strat in STRATS if "投A" in row_obj[strat])
    b_count = sum(1 for strat in STRATS if "投B" in row_obj[strat])
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
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
    for strat in STRATS:
        label = base.tag_in_cell(row_obj[strat])
        score += weights[strat] * label_score.get(label, 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    if choice == "中性":
        return "两家公司风格差异较大，CEG的AI电力稀缺性与对手的增长/估值证据未拉开可强判差距。"
    diffs = {strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0) for strat in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 12:
            return "CEG 的Q1收入、FY2026 EPS指引、Calpine全年并表和核电可用性使NTM兑现更硬。"
        if diffs["近端催化优先"] > 12:
            return "CEG 的Calpine整合、Freestone/Clinton/Crane审批和PPA节点更可能带来近端验证。"
        if diffs["下行保护优先"] > 12:
            return "CEG 的核电/PTC、长约和发电现金流底盘更适合防守。"
        if diffs["风险调整收益"] > 10:
            return "CEG 的清洁电力稀缺性、现金流和估值消化组合更均衡。"
        return "CEG 在可见现金流、核电/气电资产和AI电力期权之间更均衡。"

    if diffs["右尾弹性优先"] < -18 and b.get("category") in HIGH_GROWTH_CATS:
        return f"{b['ticker']} 的AI主链右尾或小基数弹性明显大于CEG的中期电力传导。"
    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']} 的NTM订单、收入或利润兑现链条比CEG更短。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']} 当前估值更容易被未来业绩消化，CEG已包含一定AI电力重估。"
    if diffs["下行保护优先"] < -12:
        return f"{b['ticker']} 的现金流、估值或压力期韧性强于CEG。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']} 的价格确认和资金偏好明显强于CEG。"
    return f"{b['ticker']} 在该资金配置口径下的增长质量、催化或估值组合更优。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) > tier_value(b.get("tiers", {}).get(s))]
    b_strong = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) < tier_value(b.get("tiers", {}).get(s))]
    close = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) == tier_value(b.get("tiers", {}).get(s))]
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts) if parts else "档位接近"


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj = {
            "ticker": ticker,
            "name": b["name"],
            "classification": base.category_short(b.get("category", "")),
            "relationship": rel,
            "grade_diff": grade_diff_summary(a, b),
        }
        for strat in STRATS:
            row_obj[strat] = cell_for(strat, a, b, rel)
        ac, bc, nc = direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        choice = final_choice(row_obj)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, row_obj, choice)
        rows.append(row_obj)

    def sort_key(item: dict) -> tuple[int, str]:
        rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
        return (rel_order.get(item["relationship"], 9), item["ticker"])

    return sorted(rows, key=sort_key)


def fmt_num(value, decimals: int = 1) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return "缺失"


def fmt_b(value) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return "缺失"


def fmt_pct(value) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):+.2f}%"
    except Exception:
        return "缺失"


def majority(rows: list[dict], final: str, limit: int = 40) -> list[dict]:
    selected = [r for r in rows if r["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda x: (x["bc"] - x["ac"], x["bc"], -x["nc"]), reverse=True)
    else:
        selected.sort(key=lambda x: (x["ac"] - x["bc"], x["ac"], -x["nc"]), reverse=True)
    return selected[:limit]


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin")])
    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})

    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去一月 {fmt_pct(m1m.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    stats: dict[str, Counter] = {strat: Counter() for strat in STRATS}
    for row_obj in comparisons:
        for strat in STRATS:
            stats[strat][base.tag_in_cell(row_obj[strat])] += 1

    lines: list[str] = []
    lines.append("# CEG 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：CEG / Constellation Energy")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(comparisons)}")
    lines.append(f"公司评估文件日期范围：{date_range}")
    lines.append("日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 压力窗口")
    lines.append("")
    lines.append("> 口径说明：正式生成脚本只使用公司评估、公司调研、行业调研和金融资料等上游资料；未将 `特征量化/`、公司排序结果、备份目录或临时结果作为资料来源，也未引用或继承其结论。每一行是 CEG 与一家项目内公司 B 的二选一判断。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append("- A 最占优的投资思路：`NTM兑现优先` 和 `近端催化优先`。CEG 有 2026Q1 收入、FY2026 调整后 EPS 指引、Calpine 全年并表、核电可用性和电力长约/站点供电节点作为硬锚。")
    lines.append("- A 最吃亏的投资思路：`价格确认/动量` 和 `激进短线`。CEG 的 AI 电力叙事强，但近期价格确认和高 beta 弹性弱于一批 AI 主链、核能开发、算力和电气设备公司。")
    lines.append("- A 最适合的投资者画像：希望买 AI 用电/核电稀缺性，同时要求 NTM 收入与利润有真实资产、指引和现金流支撑的中长期配置资金。")
    lines.append("- A 最不适合的投资者画像：只追求最高短期 beta、最快收入翻倍或最强价格动量的进攻型资金。")
    strong_b = majority(comparisons, "B", 12)
    strong_a = majority(comparisons, "A", 12)
    lines.append("- 多数思路下最强反方公司：" + "、".join([f"{r['ticker']}（{r['name']}）" for r in strong_b[:8]]) + "。")
    final_a = sum(1 for r in comparisons if r["final_choice"] == "A")
    final_b = sum(1 for r in comparisons if r["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：CEG 是全项目偏强但非最高 beta 的 AI 电力/核电稀缺资产；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。")
    lines.append("- 后续最重要跟踪数据：Calpine 并表后季度收入与调整后 EPS、核电可用性和停堆天数、Freestone/Thad Hill/Clinton/Crane 里程碑、PPA 定价和成本分摊、净债务/抵押品/成长 capex、以及股价能否重新获得相对 SOXX 的确认。")
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | CEG |")
    lines.append("| 公司名称 | Constellation Energy |")
    lines.append(f"| 产业链分类 | {a.get('category', '电力_发电_能源_储能')} |")
    lines.append("| 重要产品/业务线 | 核电清洁基荷电力、Calpine 气电/容量/抽蓄资产、C&I/零售清洁电力合同、数据中心站点供电、Crane/Clinton 等核电长约和重启/延寿项目 |")
    lines.append("| NTM 基准收入 | 评估文件基准情景约 $43.5-$48.5B；2026Q1 收入 $11.122B，同比 +63.8%，主要来自 Calpine 2026-01-07 并表、市场条件和业务组合 |")
    lines.append("| 乐观/极度乐观收入 | 乐观情景约 $48.5-$54.5B；极度乐观情景约 $54.5-$60.0B |")
    lines.append("| 利润和现金流结论 | FY2026 调整后经营 EPS 指引 $11.00-$12.00；基准调整后经营收益约 $4.00-$4.45B，现金流受 Calpine 债务、成长 capex、抵押品和客户预付款/成本分摊影响 |")
    lines.append("| 最大传导瓶颈 | AI/data center 电力需求到收入确认链条长，需要客户签约、PUCT/PJM/ERCOT/NRC/FERC/DOJ 条件、站点基础设施、互联/净计量、资产可用率和结算同步兑现 |")
    lines.append("| 最大反证 | NTM 直接 AI 数据中心收入仍有限；Crane 和多个站点供电项目主要在 2027H2-2029 以后，若审批、互联、停堆或 capex 超支会削弱右尾 |")
    lines.append("| 近端催化剂 | Calpine 整合与资产剥离、季度 EPS/毛利指引、Freestone/Thad Hill 站点供电进展、Clinton-Meta 2027 年启动准备、Crane NRC/DOE 节点、Geysers/储能进展 |")
    lines.append("| 日度数据 | " + daily_snapshot + " |")
    lines.append("")
    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    support = {
        "NTM兑现优先": ("A", "全项目前列", "Q1收入 $11.122B、FY2026 EPS $11-$12、Calpine全年并表和核电发电量提供硬锚", "收入高增有并购基数因素，AI电力直接收入在NTM仍少"),
        "右尾弹性优先": ("A", "强但非最激进", "147M MWh 长约库存、Freestone/Thad Hill >1.1GW、Crane 835MW/Microsoft、Clinton 1,121MW/Meta", "多数右尾项目落在2027H2-2029以后，非纯小基数翻倍标的"),
        "风险调整收益": ("A", "偏强", "核电/PTC/长约/Calpine形成资产底盘，估值仍可由FY2026 EPS部分消化", "电力价格、停堆、capex、净债务和AI电力重估溢价会压低赔率"),
        "下行保护优先": ("B", "中上", "核电基荷、PTC、长期合同和发电资产提供基本面支撑", "SOXX压力窗口累计 -62.45%，股性更像竞争性发电商而非低波动公用事业"),
        "估值消化优先": ("A", "偏强", "Forward PE 20.34、EV/EBITDA 15.20 与FY2026 EPS指引相比尚可解释", "市场已计入部分AI电力稀缺性，极端情景需要多项目兑现"),
        "近端催化优先": ("A", "强势档", "Calpine并表、Freestone/Thad Hill、Clinton/Meta、Crane审批和季度指引都有可跟踪节点", "重大收入贡献时间滞后，审批节奏可能推迟"),
        "价格确认/动量": ("C", "偏弱", "主题关注度与IV不低，若PPA/审批再验证可重新获得趋势", "近期相对动量和压力窗口表现不强，价格尚未充分确认基本面改善"),
        "激进短线": ("C", "偏弱", "Call IV 52.5%、核电AI电力叙事、站点供电新闻流仍可用于事件交易", "短线爆发力弱于AI算力链、核能开发小票和高动量电气设备"),
    }
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in STRATS:
        tier = a.get("tiers", {}).get(strat, "资料不足")
        position = f"{support[strat][1]}；评分排名 {a.get('ranks', {}).get(strat)}/{a.get('rank_total', {}).get(strat)}"
        lines.append(f"| {strat} | {tier} | {position} | {support[strat][2]} | {support[strat][3]} |")
    lines.append("")
    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 作为电力生产、公用事业或核电/容量/PPA资产比较，优先看发电资产、长约、容量收入、现金流、停堆、估值和PPA兑现 | VST、AEP、DTE、ETR | 判断力度最高；同业中若一方FCF/估值/合同更硬，可以给建议或强烈建议 |")
    lines.append("| 相邻替代 | 作为AI电力、核能、电气设备、机电和电网建设资金篮子二选一，重点比较增长质量、订单、估值和催化 | BE、GEV、SMR、OKLO、BWXT、ETN、VRT、PWR、POWL | 保持中等力度；赛道更热不能自动胜出，必须有订单或业绩传导证据 |")
    lines.append("| 上下游 | 作为AI负载客户、数据中心、服务器/ODM、燃料/气体或电力需求链上下游比较，区分收入规模、利润捕获和议价权 | MSFT、META、AMZN、GOOGL、ORCL、EQIX、DLR、CRWV、ET、LIN、APD | 降低业务指标硬比，强调谁更能捕获利润池和谁的估值风险更低 |")
    lines.append("| 跨赛道 | 作为组合资金替代比较，重点看增长质量、风险调整收益、估值消化、下行保护和催化可见度 | NVDA、AVGO、TSM、ASML、MU、CDNS 等 | 默认降低结论力度；除非增长质量、估值消化或右尾弹性明显拉开 |")
    lines.append("")
    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    lines.append("| 序号 | 公司B | 公司B分类 | 可比关系 | 档位差摘要 | NTM兑现优先 | 右尾弹性优先 | 风险调整收益 | 下行保护优先 | 估值消化优先 | 近端催化优先 | 价格确认/动量 | 激进短线 | 多数思路方向 | 最终更值得投 | 最关键理由 |")
    lines.append("| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(comparisons, 1):
        b_label = f"{row_obj['ticker']} / {row_obj['name']}"
        cells = [
            str(idx),
            b_label,
            row_obj["classification"],
            row_obj["relationship"],
            row_obj["grade_diff"],
        ] + [row_obj[strat] for strat in STRATS] + [
            row_obj["majority"],
            row_obj["final_choice"],
            row_obj["key_reason"],
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## 6. 投资思路统计")
    lines.append("")
    lines.append("| 投资思路 | 强烈建议投A | 建议投A | 微倾向投A | 中性 | 微倾向投B | 建议投B | 强烈建议投B | A侧合计 | B侧合计 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strat in STRATS:
        c = stats[strat]
        a_side = c["强烈建议投A"] + c["建议投A"] + c["微倾向投A"]
        b_side = c["微倾向投B"] + c["建议投B"] + c["强烈建议投B"]
        lines.append(
            f"| {strat} | {c['强烈建议投A']} | {c['建议投A']} | {c['微倾向投A']} | {c['中性']} | "
            f"{c['微倾向投B']} | {c['建议投B']} | {c['强烈建议投B']} | {a_side} | {b_side} |"
        )
    lines.append("")
    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_b[:45], 1):
        wins = [strat for strat in STRATS if "投B" in row_obj[strat]]
        catchup = "CEG 需要看到AI电力长约更快转收入、Calpine整合超预期、EPS/FCF上修和股价相对SOXX重新确认。"
        lines.append(f"| {idx} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:5])} | {row_obj['key_reason']} | {catchup} |")
    lines.append("")
    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_a[:45], 1):
        wins = [strat for strat in STRATS if "投A" in row_obj[strat]]
        catchup = "B 需要拿出更清晰的NTM收入/利润兑现、订单或客户合同，并证明估值和现金流能承受压力窗口。"
        lines.append(f"| {idx} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:5])} | {row_obj['key_reason']} | {catchup} |")
    lines.append("")
    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。")
    lines.append(f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告，同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}。")
    lines.append(f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。")
    lines.append("- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。")
    lines.append("- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`、`公司调研/电力_发电_能源_储能/CEG_Constellation_Energy_公司调研_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`。")
    lines.append(f"- CEG 日度数据快照：{daily_snapshot}")
    lines.append("- 生成脚本：`scripts/generate_ceg_company_comparison.py`。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    report = render_report(companies, comparisons)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8")
    a = companies[TARGET]
    print(json.dumps({
        "target": TARGET,
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "ceg_tiers": {strat: a.get("tiers", {}).get(strat) for strat in STRATS},
        "ceg_ranks": {strat: a.get("ranks", {}).get(strat) for strat in STRATS},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
