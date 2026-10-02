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


TARGET = "VRT"
TARGET_NAME = "Vertiv"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "VRT_逐家公司投资思路对比_2026-06-23.md"

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

DIRECT_PEERS = {"AAON", "CARR", "DKILY", "ETN", "JCI", "MOD", "TT"}

FACILITY_INFRA_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ALLE",
    "ATKR",
    "BE",
    "BDC",
    "BELFB",
    "BWXT",
    "CAT",
    "CMI",
    "DCI",
    "DD",
    "DHR",
    "DOV",
    "ECL",
    "EME",
    "ENS",
    "FCEL",
    "FIX",
    "FLNC",
    "FTV",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "IFNNY",
    "LFUS",
    "MIELY",
    "MMM",
    "MRAAY",
    "MSI",
    "MYRG",
    "NDSN",
    "NVT",
    "PH",
    "PNR",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "ST",
    "TDY",
    "TMO",
    "TTDKY",
    "VICR",
    "VSH",
}

POWER_AND_UTILITY_CHAIN = {
    "AEP",
    "CEG",
    "DTE",
    "ET",
    "ETR",
    "OKLO",
    "SMR",
    "VST",
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

VRT_SCORES = {
    "NTM兑现优先": 86.0,
    "右尾弹性优先": 84.0,
    "风险调整收益": 60.0,
    "下行保护优先": 58.0,
    "估值消化优先": 54.0,
    "近端催化优先": 84.0,
    "价格确认/动量": 70.0,
    "激进短线": 88.0,
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
    for strategy, score in VRT_SCORES.items():
        target.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    mod_calibrated.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in FACILITY_INFRA_ADJACENT:
        return "相邻替代"
    if ticker in POWER_AND_UTILITY_CHAIN or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
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
            "NTM兑现优先": "A backlog和FY2026指引更硬",
            "右尾弹性优先": "A液冷/电力链右尾更大",
            "风险调整收益": "A增长赔率仍优于风险",
            "下行保护优先": "A服务收入和订单底盘较强",
            "估值消化优先": "A收入利润增速更能消化估值",
            "近端催化优先": "A订单转收入和产品催化更近",
            "价格确认/动量": "A短期价格确认更强",
            "激进短线": "A高关注度和高IV更适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或订单兑现更强",
            "右尾弹性优先": "B右尾更大或估值未透支",
            "风险调整收益": "B上行下行组合更均衡",
            "下行保护优先": "B现金流和估值缓冲更强",
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
            return "VRT 的FY2026指引、$15B backlog和book-to-bill让NTM收入兑现更清楚。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "VRT 在高密度电力、液冷、OneCore、800VDC和BESS上的右尾更大。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "VRT 近端订单转收入、液冷/热排放和产品路线催化更可验证。"
        if a["scores"]["激进短线"] - b["scores"]["激进短线"] > 14:  # type: ignore[index,operator]
            return "VRT 的高IV、高关注度和AI电力/冷却叙事更适合短线进攻。"
        return "VRT 的收入兑现、AI物理基础设施暴露和近端催化略优于对手。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker} 的现金流、估值支撑或压力窗口韧性明显强于 VRT。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{ticker} 的估值更容易被NTM业绩消化，而VRT当前倍数要求继续高兑现。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{ticker} 的上行/下行组合比VRT更均衡。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker} 的右尾弹性或主链收入杠杆明显高于 VRT。"
    return f"{ticker} 在多数投资思路下比 VRT 更符合该资金配置口径。"


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
            "2026Q1收入26.50亿美元同比+30.1%，FY2026收入指引135-140亿美元，2025Q4 backlog 150亿美元、book-to-bill 2.9x",
            "Q1 run-rate低于全年指引，NTM兑现仍取决于客户场地、电网接入、验收和营运资本",
        ),
        "右尾弹性优先": (
            "基准收入160-173亿美元，乐观185-205亿美元，极度乐观220-250亿美元；高密度电力、液冷、OneCore、800VDC和MV BESS共同提供上限",
            "800VDC、MV BESS/UPS和软件平台化仍是C/D级证据，不能把远期期权全部放入NTM基准",
        ),
        "风险调整收益": (
            "AI物理基础设施需求和订单可见度强，服务/液冷/热排放mix有利润率上修空间",
            "2026-06-23 Forward PE 35.89、P/S 11.25、EV/EBITDA 58.02且Call IV 76.7%，估值和波动压低风险调整赔率",
        ),
        "下行保护优先": (
            "服务和备件、装机维护、客户粘性以及大额backlog提供经营底盘",
            "2026Q1 FCF为负；三段SOXX压力窗口累计-70.57%，高估值和高IV导致压力期保护较弱",
        ),
        "估值消化优先": (
            "NTM收入和调整后经营利润仍有高增，基准经营利润37-41亿美元可为估值提供部分消化路径",
            "当前价格已要求backlog快速转收入和margin改善；若液冷/预制化利润率或FCF慢于收入，倍数压力很大",
        ),
        "近端催化优先": (
            "Q2/Q3订单、book-to-bill、backlog转收入、FY2026/FY2027指引、液冷/热排放和OneCore客户项目都可在1-2季验证",
            "近端催化大多需要交付确认；若客户项目或电网/场地延迟，订单强度不能立刻变收入",
        ),
        "价格确认/动量": (
            "过去两周+10.04%，高beta反弹已显示资金仍愿意买AI电力/冷却主线",
            "过去1个月-2.71%，压力窗口累计回撤深，动量不是无瑕疵趋势",
        ),
        "激进短线": (
            "高IV、高关注度、高密度电力/液冷叙事、订单强度和短期反弹使VRT适合进攻型仓位",
            "短线已拥挤且波动大；一旦订单转收入或FCF低于预期，估值杀伤也更大",
        ),
    }

    out: list[str] = []
    out += [
        "# VRT 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：VRT / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格、估值、IV、过去两周涨跌、过去1个月涨跌、SOXX压力窗口均为 2026-06-23 文件口径",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 VRT vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。VRT 的强项集中在订单/backlog、AI数据中心电力和液冷收入化、以及未来1-2季可验证催化。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。核心短板是估值已经很高、Call IV高、压力窗口回撤深、Q1 FCF为负且营运资本仍吃现金。",
        "- A 最适合的投资者画像：想押注AI数据中心物理基础设施紧缺，能够承受高波动，并把订单、backlog和液冷/电力链交付视作主要胜负手的成长型资金。",
        "- A 最不适合的投资者画像：优先追求低估值、低IV、压力期韧性、稳定FCF和分散经营底盘的防御型资金；这类资金通常会偏向TT、ETN、PWR、公用事业或成熟大盘平台。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在风险调整收益、估值消化、下行保护或更直接AI主链收入上压过 VRT。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：VRT 是项目内AI电力/冷却物理基础设施的核心高增长标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它不是最安全或最便宜的公司，但在NTM兑现、右尾和近端催化上处于前列。",
        "- 后续最重要跟踪数据：季度订单、book-to-bill、backlog余额和交付周期、FY2026/FY2027指引、产品/服务收入split、Americas/APAC/EMEA增长和利润率、液冷/热排放订单、OneCore/SmartRun项目、800VDC design win到订单转化、MV BESS/UPS试点到合同、库存和自由现金流。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        row(["项目", "内容"]),
        row(["---", "---"]),
        row(["股票代号", "VRT"]),
        row(["公司名称", TARGET_NAME]),
        row(["产业链分类", a["category"]]),
        row(["重要产品/业务线", "；".join(product_names)]),
        row(["NTM 基准收入", a["base_rev"] or "$16.0-17.3B"]),
        row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/EBITDA：{a['base_profit']}；现金流：{a['base_cash']}"]),
        row(["最大传导瓶颈", "backlog和订单能否在NTM内转为可确认收入，取决于客户场地就绪、电网接入、GPU机群节奏、液冷调试、预制化产能、交付验收和营运资本。"]),
        row(["最大反证", "2026Q1自由现金流为负、EMEA同比下滑、高估值和高IV；800VDC、MV BESS/UPS和软件平台化仍缺少NTM大额收入确认。"]),
        row(["近端催化剂", "Q2/Q3订单和book-to-bill、backlog转收入、FY2026/FY2027指引、液冷/热排放订单、OneCore/SmartRun客户项目、PurgeRite服务attach、800VDC客户认证。"]),
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
        row(["直接同业", "与VRT在AI数据中心电力链、UPS/PDU/busway、热管理、液冷、模块化基础设施、服务或关键设施需求池直接重叠，优先比较订单/backlog、收入兑现、产品代际、利润率、客户质量和同业估值。", "ETN、TT、MOD、JCI、CARR、AAON、DKILY", "同业证据权重最高；如果对手在现金流、估值或压力期韧性明显更强，可在风险调整和下行保护列压过VRT。"]),
        row(["相邻替代", "同属AI数据中心物理基础设施、配电、电力、冷却、工程、储能或工业基础设施资金篮子，但产品不完全直接竞争。", "GEV、PWR、EME、FIX、POWL、HUBB、NVT、BE", "重点回答资金只能买一个时谁的增长质量、订单兑现、估值消化和风险收益更好。"]),
        row(["上下游", "B位于VRT需求链上游或下游，如云厂、NeoCloud、IDC、AI芯片、服务器、网络、发电和公用事业。", "NVDA、AVGO、MSFT、AMZN、DELL、SMCI、EQIX、DLR、CEG", "不把客户CapEx直接等同于VRT收入；核心看VRT能否从下游建设中捕获高质量利润。"]),
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
        need = "需要VRT证明backlog能高质量转收入、FCF随收入释放、估值压力下降，并在价格确认上重新领先。"
        if comparison["rel"] == "直接同业":
            need = "需要VRT在同业中证明订单增长、液冷/电力链利润率和FCF转换强于B，同时估值不过度透支。"
        elif comparison["rel"] == "上下游":
            need = "需要VRT证明能从下游AI算力/云厂CapEx中捕获更高利润，而不只是设施侧跟随。"
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
        need = "需要B提高收入确认可信度、近端订单催化和AI物理基础设施暴露，或用更好估值/现金流抵消增长差距。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要B把下行保护优势延伸到更高增长或更强近端催化，否则难以在多数成长思路下反超VRT。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/VRT_Vertiv_公司调研_2026-06-20.md`。",
        "- 公司 A 主要行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心低压配电、PDU与母线槽_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        f"- 日度金融数据覆盖：2026-06-23 金融数据文件有记录 {n - len(missing_fin)}/{n} 家；缺少整行金融数据的公司为 {('、'.join(missing_fin) if missing_fin else '无')}；缺少当日价格的公司为 {missing_price_text}；缺少 Call IV 的公司为 {missing_call_iv_text}。若个别估值、价格或 IV 字段缺失，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{price_line}",
        "- 外部官方核验来源：Vertiv 2026Q1 results（https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-First-Quarter-with-Diluted-EPS-Growth-of-136-Adjusted-Diluted-EPS-Growth-of-83-Raises-Full-Year-Guidance/default.aspx）；Vertiv 2026Q1 Form 10-Q（https://www.sec.gov/Archives/edgar/data/1674101/000162828026026556/vrt-20260331.htm）；Vertiv 2025Q4/FY2025 results（https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Fourth-Quarter-and-Full-Year-Results-with-Record-Backlog-Raises-Organic-Growth-Target/default.aspx）；Vertiv 2026 Investor Conference（https://investors.vertiv.com/events-presentations/2026-investor-conference/default.aspx）。",
        "- 自动化脚本：`scripts/generate_vrt_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对VRT的FY2026指引、backlog/book-to-bill、液冷/热排放、OneCore/SmartRun、800VDC/MV BESS、估值、IV、价格确认和FCF反证做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比结果。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    if not OUT_PATH.parent.exists():
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 VRT 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "vrt_tiers": companies[TARGET]["tiers"],
        "vrt_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
