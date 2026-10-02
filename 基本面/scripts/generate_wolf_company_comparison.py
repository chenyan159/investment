from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as project_calibration
import generate_etn_company_comparison as etn_calibration
import generate_hubb_company_comparison as hubb_calibration
import generate_ifnny_company_comparison as ifnny_calibration
import generate_mraay_company_comparison as mraay_calibration
import generate_nvt_company_comparison as nvt_calibration
import generate_on_company_comparison as on_calibration
import generate_ttdky_company_comparison as ttdky_calibration
import generate_vrt_company_comparison as vrt_calibration

TARGET = "WOLF"
TARGET_NAME = "Wolfspeed"
REPORT_DATE = "2026-06-23"

OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / f"{TARGET}_逐家公司投资思路对比_{REPORT_DATE}.md"

EVAL_DIR = ROOT.parent / "分析报告" / "公司评估" / "结果"
FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"
MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_SIC_POWER_PEERS = {
    "ADI",
    "AOSL",
    "COHR",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MCHP",
    "MIELY",
    "MPWR",
    "MRAAY",
    "NVTS",
    "ON",
    "POWI",
    "ST",
    "STM",
    "TTDKY",
    "TXN",
    "VICR",
    "VSH",
}

AI_POWER_ELECTRICAL_ALTS = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "BDC",
    "BELFB",
    "BE",
    "CMI",
    "EME",
    "ENS",
    "ETN",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "ITRI",
    "LEU",
    "NVT",
    "POWL",
    "PSIX",
    "RYCEY",
    "VRT",
}

AI_COMPUTE_AND_NETWORK = {
    "AAPL",
    "AAOI",
    "ACMR",
    "AMD",
    "AMKR",
    "APP",
    "ARISTA",
    "ARQQ",
    "ARM",
    "AVGO",
    "BABA",
    "BIDU",
    "CAMT",
    "CARR",
    "CEG",
    "CLS",
    "COHU",
    "CRDO",
    "CRWV",
    "DELL",
    "FN",
    "FSLR",
    "GOOG",
    "HPE",
    "INTC",
    "IONQ",
    "KLAC",
    "META",
    "MRVL",
    "MSFT",
    "MU",
    "NBIS",
    "NVDA",
    "NXPI",
    "ORCL",
    "PLTR",
    "QCOM",
    "QUBT",
    "RGTI",
    "RIVN",
    "SHOP",
    "TSLA",
    "TSM",
    "UBER",
}

SEMI_CAPEX_MATERIALS = {
    "ACLs".upper(),
    "AMAT",
    "ASML",
    "AXTI",
    "ENTG",
    "FORM",
    "LRCX",
    "MKSI",
    "MU",
    "NVMI",
    "ONTO",
    "TER",
    "UCTT",
}

HIGH_GROWTH_AI_SOFTWARE = {
    "APP",
    "BIDU",
    "GOOG",
    "META",
    "MSFT",
    "NOW",
    "ORCL",
    "PLTR",
    "SHOP",
    "UBER",
}

WOLF_SCORES = {
    "NTM兑现优先": 38.0,
    "右尾弹性优先": 66.0,
    "风险调整收益": 28.0,
    "下行保护优先": 20.0,
    "估值消化优先": 34.0,
    "近端催化优先": 58.0,
    "价格确认/动量": 22.0,
    "激进短线": 76.0,
}

SCORE_FLOORS = {
    "ABBNY": {"NTM兑现优先": 68, "风险调整收益": 68, "下行保护优先": 72, "估值消化优先": 63},
    "AEIS": {"近端催化优先": 62, "激进短线": 61},
    "AMKR": {"NTM兑现优先": 62, "估值消化优先": 61, "下行保护优先": 58},
    "ARM": {"右尾弹性优先": 86, "风险调整收益": 58, "激进短线": 80},
    "AVGO": {"NTM兑现优先": 86, "右尾弹性优先": 82, "风险调整收益": 76, "估值消化优先": 74},
    "CEG": {"NTM兑现优先": 78, "风险调整收益": 75, "下行保护优先": 80, "估值消化优先": 72},
    "CRDO": {"右尾弹性优先": 84, "近端催化优先": 80, "价格确认/动量": 82, "激进短线": 84},
    "DELL": {"NTM兑现优先": 76, "估值消化优先": 73, "近端催化优先": 70},
    "EME": {"NTM兑现优先": 76, "风险调整收益": 74, "下行保护优先": 70, "估值消化优先": 70},
    "GEV": {"NTM兑现优先": 76, "右尾弹性优先": 74, "风险调整收益": 74, "下行保护优先": 74},
    "HPE": {"估值消化优先": 70, "下行保护优先": 68},
    "IFNNY": {"NTM兑现优先": 70, "风险调整收益": 72, "下行保护优先": 74, "估值消化优先": 70},
    "KLAC": {"NTM兑现优先": 74, "风险调整收益": 72, "下行保护优先": 73, "估值消化优先": 70},
    "MPWR": {"NTM兑现优先": 72, "右尾弹性优先": 74, "风险调整收益": 68, "近端催化优先": 70},
    "MRVL": {"右尾弹性优先": 78, "近端催化优先": 76, "激进短线": 76},
    "MU": {"右尾弹性优先": 80, "近端催化优先": 78, "价格确认/动量": 76, "激进短线": 78},
    "NVDA": {"NTM兑现优先": 92, "右尾弹性优先": 92, "风险调整收益": 82, "近端催化优先": 86, "价格确认/动量": 84},
    "ON": {"NTM兑现优先": 66, "风险调整收益": 64, "下行保护优先": 62, "估值消化优先": 64},
    "POWL": {"NTM兑现优先": 76, "右尾弹性优先": 76, "风险调整收益": 68, "近端催化优先": 74},
    "TSM": {"NTM兑现优先": 88, "右尾弹性优先": 82, "风险调整收益": 80, "下行保护优先": 78, "估值消化优先": 76},
    "VRT": {"NTM兑现优先": 84, "右尾弹性优先": 82, "风险调整收益": 76, "估值消化优先": 74, "近端催化优先": 82},
}


def apply_daily_path_overrides() -> None:
    base.ROOT = ROOT
    base.EVAL_DIR = EVAL_DIR
    base.OUT_DIR = OUT_PATH.parent
    base.FIN_PATH = FIN_PATH
    base.MOM2W_PATH = MOM2W_PATH
    base.MOM1M_PATH = MOM1M_PATH
    base.SOXX_PATH = SOXX_PATH
    base.TARGET = TARGET
    base.REPORT_DATE = REPORT_DATE


def tier_value(tier: str) -> int | None:
    return TIER_VAL.get(tier)


def collect_score_floors() -> dict[str, dict[str, float]]:
    floors: dict[str, dict[str, float]] = {ticker: values.copy() for ticker, values in SCORE_FLOORS.items()}
    modules = [
        project_calibration,
        etn_calibration,
        hubb_calibration,
        ifnny_calibration,
        mraay_calibration,
        nvt_calibration,
        on_calibration,
        ttdky_calibration,
        vrt_calibration,
    ]
    for module in modules:
        for attr in ("SCORE_FLOORS", "LOCAL_SCORE_FLOORS"):
            for ticker, score_map in getattr(module, attr, {}).items():
                current = floors.setdefault(ticker, {})
                for strat, score in score_map.items():
                    current[strat] = max(current.get(strat, -999), score)
        for attr in (
            "ETN_SCORES",
            "HUBB_SCORES",
            "IFNNY_SCORES",
            "MRAAY_SCORES",
            "NVT_SCORES",
            "ON_SCORES",
            "TTDKY_SCORES",
            "VRT_SCORES",
        ):
            if hasattr(module, attr):
                ticker = attr.removesuffix("_SCORES")
                current = floors.setdefault(ticker, {})
                for strat, score in getattr(module, attr).items():
                    current[strat] = max(current.get(strat, -999), score)
    floors[TARGET] = WOLF_SCORES.copy()
    return floors


def recompute_tiers(companies: dict[str, dict]) -> None:
    for strat in STRATS:
        vals: list[tuple[str, float]] = []
        for ticker, c in companies.items():
            if c["scores"].get(strat) is not None:
                vals.append((ticker, float(c["scores"][strat])))
        vals.sort(key=lambda item: item[1], reverse=True)
        n = len(vals)
        if n == 0:
            continue
        for rank, (ticker, _score) in enumerate(vals, 1):
            pct = rank / n
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
            companies[ticker]["tiers"][strat] = tier


def score_companies(companies: dict[str, dict]) -> None:
    base.TARGET = TARGET
    base.score_companies(companies)
    if hasattr(project_calibration, "fix_growth_ranges"):
        project_calibration.fix_growth_ranges(companies)
    if hasattr(project_calibration, "apply_score_floors"):
        project_calibration.apply_score_floors(companies)
    floors = collect_score_floors()
    for ticker, score_map in floors.items():
        if ticker not in companies:
            continue
        for strat, score in score_map.items():
            current = companies[ticker]["scores"].get(strat)
            companies[ticker]["scores"][strat] = score if current is None else max(float(current), score)
    for strat, score in WOLF_SCORES.items():
        companies[TARGET]["scores"][strat] = score
    recompute_tiers(companies)


def relationship(b: dict) -> str:
    ticker = b["ticker"]
    category = b.get("category", "")
    if ticker in DIRECT_SIC_POWER_PEERS:
        return "直接同业"
    if ticker in AI_POWER_ELECTRICAL_ALTS:
        return "相邻替代"
    if ticker in SEMI_CAPEX_MATERIALS:
        return "上下游"
    if ticker in AI_COMPUTE_AND_NETWORK:
        return "上下游"
    if any(key in category for key in ("配电_电源_功率器件", "电力_发电_能源_储能", "机电_冷却", "光模块_网络设备", "半导体设备_制造_材料")):
        return "相邻替代"
    if any(key in category for key in ("AI芯片", "AI软件", "云厂商", "服务器_OEM")):
        return "上下游"
    return "跨赛道"


def relation_strength(rel: str) -> float:
    return {"直接同业": 1.12, "相邻替代": 1.0, "上下游": 0.92, "跨赛道": 0.76}[rel]


def category_short(c: dict) -> str:
    category = c.get("category") or ""
    if category:
        return category
    return base.category_short(c)


def short_name(c: dict) -> str:
    return base.short_name(c)


def label_for(a: dict, b: dict, strat: str, rel: str) -> str:
    av = tier_value(a["tiers"][strat])
    bv = tier_value(b["tiers"][strat])
    ascore = a["scores"].get(strat)
    bscore = b["scores"].get(strat)
    if av is None or bv is None or ascore is None or bscore is None:
        return "中性"
    diff = (float(ascore) - float(bscore)) * relation_strength(rel)
    tier_diff = av - bv

    if abs(diff) < 4.5 and abs(tier_diff) == 0:
        return "中性"

    if diff >= 24 or tier_diff >= 3:
        return "强烈建议投A"
    if diff >= 11 or tier_diff >= 2:
        return "建议投A"
    if diff >= 4.5 or tier_diff == 1:
        return "微倾向投A"
    if diff <= -24 or tier_diff <= -3:
        return "强烈建议投B"
    if diff <= -11 or tier_diff <= -2:
        return "建议投B"
    if diff <= -4.5 or tier_diff == -1:
        return "微倾向投B"
    return "中性"


def reason_for(label: str, strat: str, b: dict, rel: str) -> str:
    bname = b["ticker"]
    if label == "中性":
        if rel == "跨赛道":
            return "业务差异大且证据未拉开"
        if strat in ("风险调整收益", "下行保护优先"):
            return "赔率与风险相互抵消"
        return "同档或相邻档差距有限"

    choose_a = label.endswith("投A")
    if choose_a:
        if strat == "NTM兑现优先":
            return "A有Q4指引和SiC底部验证"
        if strat == "右尾弹性优先":
            return "A的SiC高压和AI电力右尾更大"
        if strat == "风险调整收益":
            return "A低市值反转赔率略优"
        if strat == "下行保护优先":
            return "A现金缓冲强于对手短板"
        if strat == "估值消化优先":
            return "A低基数反转可消化估值"
        if strat == "近端催化优先":
            return "A有FYQ4和Gen5验证窗口"
        if strat == "价格确认/动量":
            return "A超跌后反弹弹性更高"
        if strat == "激进短线":
            return "A高IV叠加SiC转向叙事"

    if strat == "NTM兑现优先":
        if rel == "直接同业":
            return f"{bname}订单/利润兑现更清楚"
        if rel == "相邻替代":
            return f"{bname}收入路径和 backlog 更硬"
        return f"{bname}近12个月收入质量更高"
    if strat == "右尾弹性优先":
        if bname in {"NVDA", "AVGO", "CRDO", "VRT", "MU", "MRVL", "ARM", "POWL"}:
            return f"{bname}AI主线右尾更确定"
        return f"{bname}上行情景证据更硬"
    if strat == "风险调整收益":
        return f"{bname}上行下行组合优于A"
    if strat == "下行保护优先":
        return f"{bname}现金流/资产质量更稳"
    if strat == "估值消化优先":
        return f"{bname}更能用业绩消化估值"
    if strat == "近端催化优先":
        return f"{bname}近两季重定价事件更明确"
    if strat == "价格确认/动量":
        return f"{bname}价格趋势强于A破位"
    if strat == "激进短线":
        return f"{bname}短线关注度和趋势更强"
    return f"{bname}证据强于A"


def cell_for(a: dict, b: dict, strat: str, rel: str) -> str:
    label = label_for(a, b, strat, rel)
    return f"{label}：{reason_for(label, strat, b, rel)}"


def tag_in_cell(cell: str) -> str:
    return cell.split("：", 1)[0]


def direction_counts(cells: dict[str, str]) -> tuple[int, int, int]:
    a_side = sum(1 for v in cells.values() if tag_in_cell(v).endswith("投A"))
    b_side = sum(1 for v in cells.values() if tag_in_cell(v).endswith("投B"))
    neutral = sum(1 for v in cells.values() if tag_in_cell(v) == "中性")
    return a_side, b_side, neutral


def final_choice(a: dict, b: dict, cells: dict[str, str], rel: str) -> str:
    weights = {
        "NTM兑现优先": 1.35,
        "右尾弹性优先": 1.0,
        "风险调整收益": 1.45,
        "下行保护优先": 1.2,
        "估值消化优先": 1.35,
        "近端催化优先": 1.0,
        "价格确认/动量": 0.85,
        "激进短线": 0.75,
    }
    label_weight = {
        "强烈建议投A": 2.0,
        "建议投A": 1.25,
        "微倾向投A": 0.45,
        "中性": 0.0,
        "微倾向投B": -0.45,
        "建议投B": -1.25,
        "强烈建议投B": -2.0,
    }
    net = 0.0
    for strat, cell in cells.items():
        net += weights[strat] * label_weight[tag_in_cell(cell)]
    if rel == "跨赛道" and abs(net) < 1.0:
        return "中性"
    if net > 0.6:
        return TARGET
    if net < -0.6:
        return b["ticker"]
    return "中性"


def key_reason(a: dict, b: dict, cells: dict[str, str], rel: str, choice: str) -> str:
    bname = b["ticker"]
    if choice == "中性":
        return "两家公司投资风格差异大，核心证据未形成稳定二选一优势"
    if choice == TARGET:
        if tag_in_cell(cells["激进短线"]).endswith("投A") and tag_in_cell(cells["右尾弹性优先"]).endswith("投A"):
            return "WOLF胜在SiC高压、AI电力和重组反转弹性，但只适合作为高风险仓位"
        if tag_in_cell(cells["近端催化优先"]).endswith("投A"):
            return "WOLF近端FYQ4、Gen5和高压产品验证比对手更能改变预期"
        return "WOLF在该对比中主要靠低基数反转和SiC右尾压过对手"
    if tag_in_cell(cells["NTM兑现优先"]).endswith("投B") and tag_in_cell(cells["估值消化优先"]).endswith("投B"):
        return f"{bname}收入/利润兑现和估值消化强于WOLF，WOLF仍需证明订单与毛利修复"
    if tag_in_cell(cells["下行保护优先"]).endswith("投B") and tag_in_cell(cells["风险调整收益"]).endswith("投B"):
        return f"{bname}现金流、资产质量或风险调整赔率更稳，WOLF负毛利和高IV拖累配置价值"
    if tag_in_cell(cells["价格确认/动量"]).endswith("投B"):
        return f"{bname}价格已经更好确认基本面，WOLF一个月大幅回撤尚未修复"
    if tag_in_cell(cells["右尾弹性优先"]).endswith("投B"):
        return f"{bname}右尾和近端AI主线证据强于WOLF的未量化SiC可选项"
    return f"{bname}综合证据强于WOLF，WOLF需要收入、毛利和订单三项同步转正"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strat in STRATS:
        av = tier_value(a["tiers"][strat])
        bv = tier_value(b["tiers"][strat])
        if av is None or bv is None:
            close.append(strat)
        elif av - bv >= 1:
            a_strong.append(strat)
        elif bv - av >= 1:
            b_strong.append(strat)
        else:
            close.append(strat)
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts)


def comparison_sort_key(item: dict) -> tuple:
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return (rel_order[item["rel"]], category_short(item["b"]), item["b"]["ticker"])


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows: list[dict] = []
    for ticker, b in companies.items():
        if ticker == TARGET:
            continue
        rel = relationship(b)
        cells = {strat: cell_for(a, b, strat, rel) for strat in STRATS}
        a_count, b_count, neutral_count = direction_counts(cells)
        choice = final_choice(a, b, cells, rel)
        rows.append(
            {
                "b": b,
                "rel": rel,
                "cells": cells,
                "a_count": a_count,
                "b_count": b_count,
                "neutral_count": neutral_count,
                "choice": choice,
                "key_reason": key_reason(a, b, cells, rel, choice),
                "grade_summary": grade_diff_summary(a, b),
            }
        )
    rows.sort(key=comparison_sort_key)
    return rows


def fmt_num(value, digits: int = 2, na: str = "缺失") -> str:
    if value is None:
        return na
    try:
        return f"{float(value):,.{digits}f}"
    except (TypeError, ValueError):
        return na


def fmt_b(value, na: str = "缺失") -> str:
    if value is None:
        return na
    try:
        v = float(value)
    except (TypeError, ValueError):
        return na
    return f"{v:,.2f}B"


def fmt_pct(value, digits: int = 1, signed: bool = False, na: str = "缺失") -> str:
    if value is None:
        return na
    try:
        v = float(value)
    except (TypeError, ValueError):
        return na
    sign = "+" if signed and v > 0 else ""
    return f"{sign}{v:.{digits}f}%"


def daily_snapshot_text(a: dict) -> str:
    fin = a.get("fin", {})
    mom2w = a.get("mom2", {})
    mom1m = a.get("mom1", {})
    soxx = a.get("soxx", {})
    return (
        f"价格 {fmt_num(fin.get('price'))}（{fin.get('price_date') or REPORT_DATE}），"
        f"市值 {fmt_b(fin.get('market_cap_b'))}，P/S {fmt_num(fin.get('ps'))}，"
        f"Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}，"
        f"两周 {fmt_pct(mom2w.get('mom2w'), signed=True)}，一月 {fmt_pct(mom1m.get('mom1m'), signed=True)}，"
        f"SOXX压力累计 {fmt_pct(soxx.get('soxx_cum'), signed=True, na='缺失/不可比')}。"
    )


def winner_str(r: dict) -> str:
    return f"A {r['a_count']} / B {r['b_count']} / 中性 {r['neutral_count']}"


def top_majority(rows: list[dict], side: str, limit: int = 30) -> list[dict]:
    if side == "B":
        selected = [r for r in rows if r["b_count"] >= 5 and r["b_count"] - r["a_count"] >= 2]
        selected.sort(key=lambda r: (r["b_count"] - r["a_count"], r["b_count"], r["b"]["scores"].get("风险调整收益") or 0), reverse=True)
    else:
        selected = [r for r in rows if r["a_count"] >= 5 and r["a_count"] - r["b_count"] >= 2]
        selected.sort(key=lambda r: (r["a_count"] - r["b_count"], r["a_count"]), reverse=True)
    return selected[:limit]


def majority_side(rows: list[dict]) -> Counter:
    c: Counter = Counter()
    for r in rows:
        if r["choice"] == TARGET:
            c["A"] += 1
        elif r["choice"] == "中性":
            c["中性"] += 1
        else:
            c["B"] += 1
    return c


def source_file_list(companies: dict[str, dict]) -> str:
    lines = []
    for ticker in sorted(companies):
        c = companies[ticker]
        lines.append(f"- {ticker}: `{Path(c['path']).name}`")
    return "\n".join(lines)


def render_report(companies: dict[str, dict], rows: list[dict], eval_dates: list[str]) -> str:
    a = companies[TARGET]
    fin = a.get("fin", {})
    mom2w = a.get("mom2", {})
    mom1m = a.get("mom1", {})
    soxx = a.get("soxx", {})
    date_range = f"{min(eval_dates)} 至 {max(eval_dates)}"
    eval_count = len(companies)
    b_count = eval_count - 1
    final_stats = majority_side(rows)

    strat_stats: dict[str, Counter] = {}
    for strat in STRATS:
        counter: Counter = Counter()
        for r in rows:
            counter[tag_in_cell(r["cells"][strat])] += 1
        strat_stats[strat] = counter

    table_rows = []
    for idx, r in enumerate(rows, 1):
        b = r["b"]
        cells = r["cells"]
        cell_values = " | ".join(cells[strat] for strat in STRATS)
        table_rows.append(
            f"| {idx} | {short_name(b)} | {category_short(b)} | {r['rel']} | {r['grade_summary']} | "
            f"{cell_values} | {winner_str(r)} | {r['choice']} | {r['key_reason']} |"
        )

    stat_rows = []
    for strat in STRATS:
        counter = strat_stats[strat]
        a_side = counter["强烈建议投A"] + counter["建议投A"] + counter["微倾向投A"]
        b_side = counter["微倾向投B"] + counter["建议投B"] + counter["强烈建议投B"]
        stat_rows.append(
            f"| {strat} | {counter['强烈建议投A']} | {counter['建议投A']} | {counter['微倾向投A']} | "
            f"{counter['中性']} | {counter['微倾向投B']} | {counter['建议投B']} | {counter['强烈建议投B']} | {a_side} | {b_side} |"
        )

    b_major_rows = []
    for idx, r in enumerate(top_majority(rows, "B"), 1):
        win_strats = [strat for strat in STRATS if tag_in_cell(r["cells"][strat]).endswith("投B")]
        b_major_rows.append(
            f"| {idx} | {short_name(r['b'])} | {'、'.join(win_strats[:5])} | {r['key_reason']} | "
            f"WOLF需要看到大客户订单、Power/Materials收入恢复、非GAAP毛利率转正和FCF压力下降 |"
        )

    a_major_rows = []
    for idx, r in enumerate(top_majority(rows, "A"), 1):
        win_strats = [strat for strat in STRATS if tag_in_cell(r["cells"][strat]).endswith("投A")]
        a_major_rows.append(
            f"| {idx} | {short_name(r['b'])} | {'、'.join(win_strats[:5])} | {r['key_reason']} | "
            f"B需要证明近端收入、利润或催化强于WOLF的SiC反转弹性 |"
        )

    if not b_major_rows:
        b_major_rows.append("| 1 | 无 | 无 | 未出现多数思路下明显强于WOLF的公司 | 无 |")
    if not a_major_rows:
        a_major_rows.append("| 1 | 无 | 无 | WOLF没有在多数思路下明显压过项目内其他公司 | 无 |")

    a_tiers = {
        "NTM兑现优先": ("D", "全项目后段", "FY2026 Q3收入150.2M、Q4指引140-160M提供基准锚", "基准收入仍接近低位，非GAAP毛利和EBITDA为负"),
        "右尾弹性优先": ("B", "中上但未达顶档", "SiC材料、Gen5、3.3kV/10kV和AI电力架构有非线性可选项", "未披露AI数据中心收入、backlog或超大客户量产订单"),
        "风险调整收益": ("D", "全项目后段", "市值小、P/S约3.62、现金和重组给反转赔率", "负毛利、负EBITDA、负FCF和高IV使下行风险很重"),
        "下行保护优先": ("D", "全项目后段", "现金及短期投资约11.65亿美元提供时间缓冲", "一月下跌约28.72%，SOXX压力窗口部分数据很弱"),
        "估值消化优先": ("D", "全项目后段", "低收入基数若恢复，P/S消化速度可放大", "Forward EPS为负，EV/EBITDA为负，当前业绩无法支撑质量估值"),
        "近端催化优先": ("D", "全项目后段但有观察窗口", "FYQ4/FY27指引、Gen5、3.3kV/10kV和设计导入有验证窗口", "缺少已公告订单金额和客户放量时间表"),
        "价格确认/动量": ("D", "全项目后段", "高IV使反弹敏感度高", "价格趋势破位，一月区间表现落后多数公司"),
        "激进短线": ("C", "全项目中游的高波动进攻档", "Call IV约142.5%，SiC/800V/AI电力叙事和低市值反转弹性集中", "IV昂贵且基本面尚未确认，容易变成高波动下跌"),
    }

    tier_rows = [
        f"| {strat} | {a['tiers'][strat]} | {pos} | {support} | {limit} |"
        for strat, (_manual_tier, pos, support, limit) in a_tiers.items()
    ]

    report = f"""# {TARGET} 逐家公司投资思路对比

生成日期：{REPORT_DATE}
公司 A：{TARGET} / {TARGET_NAME}
公司全集来源：分析报告/公司评估/结果/
项目内公司总数：{eval_count}
被比较公司 B 数量：{b_count}
公司评估文件日期范围：{date_range}
日度数据日期：价格/估值/IV为 2026-06-23；两周涨跌为 2026-06-23；一月涨跌为 2026-06-23；SOXX压力窗口为 2026-06-23。

## 1. 一页结论

- A 最占优的投资思路：右尾弹性优先，其次是少数高风险对比中的激进短线。WOLF 的优势不是当前兑现质量，而是 SiC 高压、Gen5、3.3kV/10kV、AI电力架构和重组后低市值反转的组合弹性。
- A 最吃亏的投资思路：下行保护、风险调整收益、估值消化和价格确认/动量。WOLF 当前仍是负毛利、负EBITDA、负FCF，且 2026-06-23 的一月股价区间表现为 {fmt_pct(mom1m.get('mom1m'), signed=True)}。
- A 最适合的投资者画像：能承受高波动、愿意用小仓位押注 SiC 周期见底、AI电力高压化和重组后经营修复的激进投资者。
- A 最不适合的投资者画像：需要未来12个月收入利润兑现、稳定现金流、低回撤和估值可快速消化的核心配置投资者。
- 多数思路下最强反方公司：NVDA、TSM、AVGO、VRT、CEG、GEV、ETN、POWL、CRDO、MU、MRVL 等公司在兑现、订单、现金流、价格确认或AI主线位置上明显强于 WOLF。
- 如果只追求更高增长、更好公司，A 的总体位置：WOLF 不是项目内高质量核心资产，而是后段质量 + 中上右尾 + 高波动短线可选项；按最终二选一结果，A 胜出 {final_stats['A']} 家，B 胜出 {final_stats['B']} 家，中性 {final_stats['中性']} 家。
- 后续最重要跟踪数据：Power Products 与 Materials 收入是否连续恢复，非GAAP毛利率何时转正，Mohawk Valley/材料利用率，大客户设计导入是否转化为订单金额，Gen5/3.3kV/10kV实际收入，现金消耗和债务利息压力。

## 2. 公司 A 基准画像

| 项目 | 内容 |
| --- | --- |
| 股票代号 | {TARGET} |
| 公司名称 | {TARGET_NAME} |
| 产业链分类 | {category_short(a)} |
| 重要产品/业务线 | SiC材料与外延、650/750/1200V SiC MOSFET/裸片/分立器件/模块、Gen5、TOLT顶面冷却、3.3kV SiC模块、10kV MOSFET die、AI PSU/UPS/BESS/中压直流潜在应用 |
| NTM 基准收入 | 610-720百万美元；FY2026 Q3收入150.2百万美元，FY2026 Q4公司指引140-160百万美元 |
| 乐观/极度乐观收入 | 乐观750-900百万美元；极度乐观1.0-1.2十亿美元 |
| 利润和现金流结论 | 基准情景调整EBITDA约-260至-150百万美元，GAAP利润大概率仍为负；现金流核心取决于收入恢复、库存下降、capex控制和重组后利息负担 |
| 最大传导瓶颈 | 不是AI电力叙事本身，而是客户BOM/订单/backlog、Mohawk Valley和材料端利用率、负毛利转正 |
| 最大反证 | FY2026 Q3 Power收入同比-6.9%、Materials同比-35.7%，非GAAP毛利率仍为负，未披露AI数据中心收入或超大客户批量订单 |
| 近端催化剂 | FY2026 Q4/FY2027 Q1业绩与指引、Gen5导入、3.3kV/10kV高压产品进展、数据中心电力设计导入、重组后现金消耗下降 |

日度快照：{daily_snapshot_text(a)}

## 3. 公司 A 全项目相对档位

| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |
| --- | --- | --- | --- | --- |
{chr(10).join(tier_rows)}

## 4. 可比关系使用说明

| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |
| --- | --- | --- | --- |
| 直接同业 | 优先比较SiC/GaN/功率器件/模拟电源的收入恢复、订单、毛利率、产品代际和同业估值 | ON、IFNNY、STM、NVTS、POWI、MPWR、VSH、COHR | 证据权重最高；同业中若B有利润和订单优势，WOLF不能靠叙事直接胜出 |
| 相邻替代 | 比较AI电力、配电、储能、电气设备和资金配置篮子的增长质量、backlog、估值消化与近端催化 | VRT、ETN、HUBB、NVT、POWL、GEV、ABBNY、AEIS | 重点看谁更值得作为AI电力/电气化仓位；不强行比较产品细节 |
| 上下游 | 比较AI计算、云、服务器、半导体设备材料、电源需求链和SiC供需链中的利润池位置与议价权 | NVDA、AVGO、TSM、AMAT、ASML、CRDO、MRVL、DELL | 由于利润池不同，默认降低极端结论力度，但若B订单/现金流明显更强仍可建议投B |
| 跨赛道 | 业务差异较大，只作为资金配置替代比较风险调整收益、估值消化、下行保护和催化可见度 | 软件、消费互联网、非AI工业与其他异质资产 | 默认使用中性或微倾向；只有证据差距显著才给建议或强烈建议 |

## 5. 全项目逐行投资思路决策表

| 序号 | 公司B | 公司B分类 | 可比关系 | 档位差摘要 | NTM兑现优先 | 右尾弹性优先 | 风险调整收益 | 下行保护优先 | 估值消化优先 | 近端催化优先 | 价格确认/动量 | 激进短线 | 多数思路方向 | 最终更值得投 | 最关键理由 |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(table_rows)}

## 6. 投资思路统计

| 投资思路 | 强烈建议投A | 建议投A | 微倾向投A | 中性 | 微倾向投B | 建议投B | 强烈建议投B | A侧合计 | B侧合计 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(stat_rows)}

## 7. 多数思路下 B 明显强于 A 的公司

| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |
| ---: | --- | --- | --- | --- |
{chr(10).join(b_major_rows)}

## 8. 多数思路下 A 明显强于 B 的公司

| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |
| ---: | --- | --- | --- | --- |
{chr(10).join(a_major_rows)}

## 9. 来源

- 公司 A 评估文件：`{Path(a['path']).name}`。
- 公司 A 公司调研：`公司调研/配电_电源_功率器件/WOLF_Wolfspeed_公司调研_2026-06-12.md`。
- 行业调研：`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`。
- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告，同一Ticker只保留文件名日期最新的一份；未使用 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/` 或 `特征量化/`。
- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。
- 其他主要来源：每家公司最新正式收入传导估值评估中的收入表、乐观/极度乐观收入、利润现金流、催化、反证和瓶颈字段；公司调研与行业调研仅用于校准业务、订单、客户、产品和产业链关系。

### 公司全集最新正式评估文件清单

{source_file_list(companies)}
"""
    return report


def main() -> None:
    apply_daily_path_overrides()
    files = base.latest_eval_files()
    if TARGET not in files:
        raise SystemExit(f"缺少目标公司正式评估：{TARGET}")
    eval_dates = [str(item["date"]) for item in files.values()]
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit(f"目标公司未进入项目公司全集：{TARGET}")
    score_companies(companies)
    rows = build_comparisons(companies)
    report = render_report(companies, rows, eval_dates)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8")
    print(f"wrote {OUT_PATH}")
    print(f"companies={len(companies)} comparisons={len(rows)} date_range={min(eval_dates)}..{max(eval_dates)}")


if __name__ == "__main__":
    main()
