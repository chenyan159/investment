from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_etn_company_comparison as etn_calibrated
import generate_jci_company_comparison as jci_calibrated
import generate_mod_company_comparison as mod_calibrated
import generate_tt_company_comparison as tt_calibrated


TARGET = "VST"
TARGET_NAME = "Vistra Corp"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "VST_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
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

DIRECT_PEERS = {"AEP", "CEG", "DTE", "ETR"}

POWER_AND_INFRA_ADJACENT = {
    "ABBNY",
    "AEIS",
    "AAON",
    "AMPX",
    "ATKR",
    "BE",
    "BWXT",
    "CARR",
    "CAT",
    "CMI",
    "DOV",
    "EME",
    "ENS",
    "ET",
    "ETN",
    "FCEL",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "IFNNY",
    "JCI",
    "LFUS",
    "MIELY",
    "MOD",
    "MRAAY",
    "MYRG",
    "NVT",
    "OKLO",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "ST",
    "TT",
    "TTDKY",
    "VRT",
    "VICR",
    "VSH",
}

DATA_CENTER_CUSTOMERS_AND_OPERATORS = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
    "DLR",
    "EQIX",
    "GOOGL",
    "IBM",
    "IREN",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
}

SERVER_NETWORK_AND_AI_CHAIN = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "APH",
    "ARM",
    "AVGO",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CSCO",
    "DELL",
    "FLEX",
    "FN",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "MU",
    "NOK",
    "NTAP",
    "NVDA",
    "PENG",
    "POET",
    "PSTG",
    "QCOM",
    "RMBS",
    "SANM",
    "SIMO",
    "SITM",
    "SMCI",
    "SMTC",
    "SNDK",
    "STX",
    "TEL",
    "TSLA",
    "VIAV",
    "VISN",
    "WDC",
}

SEMI_AND_MATERIAL_CROSS = {
    "ACLS",
    "ACMR",
    "AMAT",
    "AMKR",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "AXTI",
    "BESIY",
    "CAMT",
    "CDNS",
    "CC",
    "COHU",
    "DIOD",
    "DSCSY",
    "ENTG",
    "FORM",
    "GFS",
    "HOCPY",
    "ICHR",
    "IMOS",
    "INTC",
    "KEYS",
    "KLAC",
    "KLIC",
    "LIN",
    "LRCX",
    "MCHP",
    "MICLF",
    "MKSI",
    "MPWR",
    "MRAM",
    "MTRN",
    "MXL",
    "NVMI",
    "NVTS",
    "ON",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SOMMY",
    "STM",
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "TXN",
    "UCTT",
    "UMC",
    "VECO",
    "WOLF",
}

VST_SCORES = {
    "NTM兑现优先": 82.0,
    "右尾弹性优先": 78.0,
    "风险调整收益": 72.0,
    "下行保护优先": 70.0,
    "估值消化优先": 82.0,
    "近端催化优先": 76.0,
    "价格确认/动量": 76.0,
    "激进短线": 82.0,
}


def row(cells: list[object]) -> str:
    return base.row(cells)


def short_name(company: dict[str, object]) -> str:
    return base.short_name(company)


def category_short(category: str) -> str:
    return base.category_short(category)


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def fmt_num(value: object) -> str:
    if value is None:
        return "缺失"
    return f"{float(value):.2f}"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    return f"${float(value):.2f}B"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    return f"{float(value):+.2f}%"


def apply_floors(companies: dict[str, dict[str, object]], floors: dict[str, dict[str, float]]) -> None:
    for ticker, score_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in score_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(current, floor)  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    if hasattr(calibrated, "fix_growth_ranges"):
        calibrated.fix_growth_ranges(companies)

    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    apply_floors(companies, getattr(calibrated, "SCORE_FLOORS", {}))
    apply_floors(companies, getattr(etn_calibrated, "LOCAL_SCORE_FLOORS", {}))
    if "ETN" in companies and hasattr(etn_calibrated, "ETN_SCORES"):
        for strategy, score in etn_calibrated.ETN_SCORES.items():
            companies["ETN"].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    apply_floors(companies, getattr(jci_calibrated, "ADDITIONAL_SCORE_FLOORS", {}))
    if "JCI" in companies and hasattr(jci_calibrated, "JCI_SCORES"):
        for strategy, score in jci_calibrated.JCI_SCORES.items():
            companies["JCI"].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    apply_floors(companies, getattr(mod_calibrated, "LOCAL_SCORE_FLOORS", {}))
    if "MOD" in companies and hasattr(mod_calibrated, "MOD_SCORES"):
        for strategy, score in mod_calibrated.MOD_SCORES.items():
            companies["MOD"].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    if "TT" in companies and hasattr(tt_calibrated, "TT_SCORES"):
        for strategy, score in tt_calibrated.TT_SCORES.items():
            companies["TT"].setdefault("scores", {})[strategy] = score  # type: ignore[index]

    target = companies[TARGET]
    for strategy, score in VST_SCORES.items():
        target.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    mod_calibrated.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in POWER_AND_INFRA_ADJACENT:
        return "相邻替代"
    if ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_NETWORK_AND_AI_CHAIN or category in HIGH_GROWTH_CATS:
        return "上下游"
    if ticker in SEMI_AND_MATERIAL_CROSS:
        return "跨赛道"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


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


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A EBITDA/FCF指引更硬",
            "右尾弹性优先": "A核电PPA和气电右尾更大",
            "风险调整收益": "A估值和现金流赔率更均衡",
            "下行保护优先": "A套保与FCF底盘更稳",
            "估值消化优先": "A低估值更易被业绩消化",
            "近端催化优先": "A PPA/并购/电价催化更近",
            "价格确认/动量": "A近期价格确认更强",
            "激进短线": "A电力AI叙事和波动更适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或订单兑现更强",
            "右尾弹性优先": "B右尾更大或估值未透支",
            "风险调整收益": "B上行下行组合更均衡",
            "下行保护优先": "B现金流或压力韧性更强",
            "估值消化优先": "B估值更易由业绩消化",
            "近端催化优先": "B近端催化更硬",
            "价格确认/动量": "B价格趋势更好",
            "激进短线": "B短线弹性或爆发力更高",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"下行保护优先", "估值消化优先"}:
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
        tag = tag_in_cell(cell) or ""
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
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    ticker = str(b["ticker"])
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "VST 的2026 EBITDA/FCFbG指引、套保比例和已披露PPA让NTM利润兑现更清楚。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "VST 的PJM核电、Meta operating PPA、Cogentrix和AI电力短缺共同提供更大右尾。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "VST 的Meta交付、Cogentrix交割、PJM/ERCOT容量和财报指引催化更可验证。"
        if a["scores"]["激进短线"] - b["scores"]["激进短线"] > 14:  # type: ignore[index,operator]
            return "VST 的AI电力、核电PPA和可调度发电叙事更适合短线进攻。"
        return "VST 的利润兑现、估值消化和AI电力暴露略优于对手。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker} 的现金流、估值支撑或压力窗口韧性明显强于 VST。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{ticker} 的估值更容易被NTM业绩消化，而VST仍需PJM/ERCOT和PPA兑现支撑。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{ticker} 的上行/下行组合比VST更均衡。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker} 的右尾弹性或主链收入杠杆明显高于 VST。"
    return f"{ticker} 在多数投资思路下比 VST 更符合该资金配置口径。"


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
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return output


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
            stats[strategy][tag_in_cell(cell)] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = sorted(
        comparisons,
        key=lambda x: (
            x["bc"] - x["ac"],  # type: ignore[operator]
            x["b"]["scores"]["风险调整收益"] - a["scores"]["风险调整收益"],  # type: ignore[index,operator]
            x["b"]["scores"]["估值消化优先"] - a["scores"]["估值消化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],  # type: ignore[operator]
            a["scores"]["NTM兑现优先"] - x["b"]["scores"]["NTM兑现优先"],  # type: ignore[index,operator]
            a["scores"]["近端催化优先"] - x["b"]["scores"]["近端催化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    final_a = sum(1 for item in comparisons if item["final"] == "A")
    final_b = sum(1 for item in comparisons if item["final"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"]]
    missing_price = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"].get("price")  # type: ignore[index,union-attr]
    ]
    missing_call_iv = [
        ticker
        for ticker in sorted(companies)
        if companies[ticker]["fin"].get("call_iv") is None  # type: ignore[index,union-attr]
    ]
    missing_price_text = "无" if not missing_price else "、".join(missing_price)
    missing_call_iv_text = "无" if not missing_call_iv else "、".join(missing_call_iv)

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]

    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})
    price_line = (
        f"2026-06-23 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"过去两周 {fmt_pct(mom2.get('mom2w'))}，过去1个月 {fmt_pct(mom1.get('mom1m'))}，"
        f"三段SOXX压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    support = {
        "NTM兑现优先": (
            "2026Q1收入56.40亿美元、Ongoing Adj. EBITDA 14.94亿美元；公司重申2026 Ongoing Adj. EBITDA 68-76亿美元、FCFbG 39.25-47.25亿美元，且2026/2027发电量套保约98%/89%",
            "收入无正式指引，Meta operating PPA只在late-2026/2027小比例进入NTM，Cogentrix仍待H2 2026交割且被正式指引排除",
        ),
        "右尾弹性优先": (
            "基准收入195-215亿美元，乐观215-240亿美元，极度乐观240-270亿美元；Meta 2176MW operating PPA、Cogentrix 5.5GW、PJM/ERCOT容量紧张和Helix优先供电权构成右尾",
            "AWS Comanche Peak、433MW核电uprate和Helix项目大多偏远期；没有价格、项目和收入确认路径时不能把主题全部进NTM",
        ),
        "风险调整收益": (
            "2026-06-23 Forward PE 14.75、P/S 2.81、EV/EBITDA 11.51，叠加高FCFbG指引和AI电力稀缺，风险收益优于多数纯题材公司",
            "三段SOXX压力窗口累计-66.07%、Call IV 57.0%，且PJM/FERC规则、核电/气电可用率、衍生品抵押品和Asset Closure仍会放大下行",
        ),
        "下行保护优先": (
            "零售电力与发电组合提供天然套保，2026 FCFbG指引接近39.25-47.25亿美元，现金流和盈利底盘强于多数亏损高β电力题材",
            "相对AEP/DTE/ETR等受监管公用事业，VST压力窗口回撤更深，且电价、套保、collateral、并购和Moss Landing/Asset Closure会冲击现金流",
        ),
        "估值消化优先": (
            "Forward PE 14.75、P/S 2.81、EV/EBITDA 11.51，对应基准Ongoing Adj. EBITDA 70-76亿美元和FCFbG 39-46亿美元，估值消化路径清楚",
            "市场已经给AI电力和核电PPA溢价；若Meta/Cogentrix/PJM/ERCOT不能兑现增量，估值会回到普通IPP/公用事业口径",
        ),
        "近端催化优先": (
            "未来1-2季可跟踪Q2/Q3分部Adj. EBITDA、PJM容量/电价、Meta late-2026交付准备、Cogentrix监管和交割、Helix项目级PPA、Retail天气正常化",
            "催化多为事件和时间表，不等于已确认收入；PPA价格、交付规则、并购审批和电厂检修均可能把重定价推后",
        ),
        "价格确认/动量": (
            "2026-06-23口径过去两周+10.98%、过去1个月+3.84%，价格已重新确认AI电力和核电PPA主线",
            "三段SOXX压力窗口累计-66.07%，说明VST并非防御型动量；若电力链资金降温，回撤弹性仍大",
        ),
        "激进短线": (
            "Call IV 57.0%、AI电力稀缺、核电PPA、Cogentrix、Helix和近期价格反弹使VST适合进攻型仓位",
            "短线爆发力仍低于OKLO/SMR/APLD/CRWV等纯右尾高β标的；若PPA或并购时间推迟，叙事兑现会被打折",
        ),
    }

    out: list[str] = []
    out += [
        "# VST 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：VST / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格、估值、IV、过去两周涨跌、过去1个月涨跌、SOXX压力窗口均为 2026-06-23 文件口径",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 VST vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。VST 的强项集中在2026 EBITDA/FCF指引、低于高成长硬件链的估值倍数、AI电力稀缺、核电PPA和可调度发电资产。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。核心短板是压力期回撤深、仍有PJM/FERC和交付规则不确定性，且右尾虽大但不像纯AI芯片、NeoCloud或小堆题材那样极端。",
        "- A 最适合的投资者画像：想押注AI数据中心电力短缺、核电/CFE PPA、可调度气电和现金流兑现，同时不愿承受纯亏损小盘电力题材极端波动的成长型资金。",
        "- A 最不适合的投资者画像：只追求传统公用事业防御性、低回撤和监管资产确定性的资金；也不适合只追最高收入增速、最高IV和最极端右尾的短线进攻资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在直接AI主链收入、极端右尾、压力期韧性或更稳的风险调整收益上压过 VST。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：VST 是项目内AI电力/发电利润捕获的一线标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它比传统公用事业更有成长和右尾，比亏损电力题材更有现金流，但面对NVDA、AVGO、MU、VRT、ETN、GEV等核心AI主链/电力设备公司仍需按思路分开选择。",
        "- 后续最重要跟踪数据：2026Q2/Q3 Ongoing Adj. EBITDA和FCFbG、East/PJM与Texas/ERCOT分部利润、Meta operating PPA delivery commencement、Cogentrix审批和close date、PJM capacity auction、ERCOT reserve margin、2026/2027套保比例、Helix项目级PPA、AWS Comanche Peak里程碑、Moss Landing/Asset Closure成本和保险回收。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        row(["项目", "内容"]),
        row(["---", "---"]),
        row(["股票代号", "VST"]),
        row(["公司名称", TARGET_NAME]),
        row(["产业链分类", a["category"]]),
        row(["重要产品/业务线", "；".join(product_names)]),
        row(["NTM 基准收入", a["base_rev"] or "$19.5-21.5B"]),
        row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/EBITDA：{a['base_profit']}；现金流：{a['base_cash']}"]),
        row(["最大传导瓶颈", "AI用电需求需要通过客户合同、PPA/容量价格、PJM/ERCOT/ISO规则、核电/气电可用率、Cogentrix交割和收入确认才能转成NTM收入与利润。"]),
        row(["最大反证", "Helix、AWS和核电uprate主要是远期期权；收入没有正式指引；Moss Landing/Asset Closure、collateral、核电/气电检修和监管规则可能吞噬现金流。"]),
        row(["近端催化剂", "Q2/Q3分部Adj. EBITDA、2026指引修正、Meta late-2026 delivery准备、Cogentrix H2 2026 close、PJM/ERCOT容量与电价、Helix项目级PPA、Asset Closure风险出清。"]),
        row(["日度价格/估值/IV", price_line]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        out.append(row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        row(["---", "---", "---", "---"]),
        row(["直接同业", "与VST在北美电力供给、核电/气电/零售电力、容量市场、PPA和数据中心电力需求池高度重叠，优先比较发电组合、套保、PPA、容量价格、FCF、监管风险和同业估值。", "CEG、AEP、DTE、ETR", "同业证据权重最高；CEG更像直接AI核电替代，AEP/DTE/ETR更偏受监管防御替代。"]),
        row(["相邻替代", "同属AI电力、能源基础设施、配电、发电设备、工程、储能或数据中心物理基础设施资金篮子，但利润池位置不同。", "GEV、PWR、ETN、VRT、BE、OKLO、SMR、POWL、HUBB、NVT、TT", "重点回答资金只能买一个时，谁在增长质量、收入/利润兑现、估值消化、风险调整收益和近端催化上更值得配置。"]),
        row(["上下游", "B位于VST需求链上游或下游，如云厂、NeoCloud、IDC、AI芯片、服务器、网络和AI软件平台。", "NVDA、AVGO、MSFT、AMZN、META、GOOGL、CRWV、DLR、EQIX、DELL、SMCI", "不把客户CapEx直接等同于VST收入；核心看VST能否从AI算力建设中捕获更稳定且可合同化的电力利润。"]),
        row(["跨赛道", "半导体设备、材料、软件或其他业务差异很大的标的，只作为资金配置替代比较。", "ASML、TSM、AMAT、LIN、DHR、TMO", "默认降低结论力度；除非增长质量、估值消化或风险收益明显拉开，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    out.append(row(headers))
    out.append(row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        out.append(
            row(
                [
                    index,
                    short_name(b),  # type: ignore[arg-type]
                    category_short(str(b["category"])),  # type: ignore[index]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(comparison["ac"], comparison["bc"], comparison["nc"]),  # type: ignore[arg-type]
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要VST证明Meta/Cogentrix/PJM/ERCOT能高质量转为利润和FCF，且估值、回撤和监管风险继续可控。"
        if comparison["rel"] == "直接同业":
            need = "需要VST在同业中证明核电/气电/容量利润、FCF转换和PPA质量强于B，同时压力期回撤不过度放大。"
        elif comparison["rel"] == "上下游":
            need = "需要VST证明能从云厂和AI算力CapEx中捕获更高质量的电力利润，而不只是跟随电力主题估值重定价。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高NTM收入/利润兑现可信度、近端催化和AI需求捕获能力，或用更好估值/现金流抵消VST的PPA与FCF优势。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要B把下行保护优势延伸到更高增长或更强近端催化，否则难以在多数成长思路下反超VST。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/VST_Vistra_Corp_公司调研_2026-06-11.md`。",
        "- 公司 A 主要行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`；`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`。",
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        f"- 日度金融数据覆盖：2026-06-23 金融数据文件有记录 {n - len(missing_fin)}/{n} 家；缺少整行金融数据的公司为 {('、'.join(missing_fin) if missing_fin else '无')}；缺少当日价格的公司为 {missing_price_text}；缺少 Call IV 的公司为 {missing_call_iv_text}。若个别估值、价格或 IV 字段缺失，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{price_line}",
        "- 外部官方核验来源：Vistra 2026Q1 results（https://investor.vistracorp.com/2026-05-07-Vistra-Reports-First-Quarter-2026-Results）；Vistra FY2025/Q4 results（https://investor.vistracorp.com/2026-02-26-Vistra-Reports-Fourth-Quarter-and-Full-Year-2025-Results）；Vistra 2026Q1 Form 10-Q（https://www.sec.gov/Archives/edgar/data/1692819/000169281926000014/vistra-20260331.htm）；Vistra/Meta PPA release（https://investor.vistracorp.com/2026-01-09-Vistra-and-Meta-Announce-Agreements-to-Support-Nuclear-Plants-in-PJM-and-Add-New-Nuclear-Generation-to-the-Grid）；KKR Helix announcement（https://www.businesswire.com/news/home/20260610500794/en/KKR-Launches-Helix-Digital-Infrastructure-a-New-Company-to-Finance-and-Deliver-the-Next-Generation-of-AI-Infrastructure）。",
        "- 自动化脚本：`scripts/generate_vst_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对VST的2026 EBITDA/FCFbG指引、Meta PPA、Cogentrix、PJM/ERCOT、Helix、估值、IV、价格确认、SOXX压力窗口和现金流反证做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比结果。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    if not OUT_PATH.parent.exists():
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 VST 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "vst_tiers": companies[TARGET]["tiers"],
        "vst_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
