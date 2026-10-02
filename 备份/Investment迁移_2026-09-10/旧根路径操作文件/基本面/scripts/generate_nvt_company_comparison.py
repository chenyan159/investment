from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as project_calibration
import generate_etn_company_comparison as etn_calibration
import generate_hubb_company_comparison as hubb_calibration
import generate_jci_company_comparison as jci_calibration
import generate_mod_company_comparison as mod_calibration


TARGET = "NVT"
TARGET_NAME = "nVent Electric"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "NVT_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_ELECTRICAL_PEERS = {
    "ABBNY",
    "ATKR",
    "ETN",
    "HUBB",
    "MIELY",
    "POWL",
}

DIRECT_COOLING_RACK_PEERS = {
    "AAON",
    "CARR",
    "DKILY",
    "JCI",
    "MOD",
    "TT",
    "VRT",
}

POWER_ELECTRICAL_INFRA = {
    "AEIS",
    "BE",
    "BWXT",
    "CMI",
    "ENS",
    "ENPH",
    "FCEL",
    "FLNC",
    "GEV",
    "GNRC",
    "HTHIY",
    "IFNNY",
    "LFUS",
    "MPWR",
    "MRAAY",
    "NVTS",
    "OKLO",
    "POWI",
    "PSIX",
    "RYCEY",
    "SMR",
    "ST",
    "TTDKY",
    "VICR",
    "VSH",
    "WOLF",
    "AMPX",
}

INDUSTRIAL_AND_ENGINEERING_INFRA = {
    "ALLE",
    "CAT",
    "DCI",
    "DD",
    "DHR",
    "DOV",
    "ECL",
    "EME",
    "FIX",
    "FTV",
    "IESC",
    "MMM",
    "MSI",
    "MYRG",
    "NDSN",
    "PH",
    "PNR",
    "PWR",
    "TDY",
    "TMO",
}

UTILITY_AND_POWER_CUSTOMERS = {"AEP", "CEG", "DTE", "ET", "ETR", "VST"}

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

SERVER_NETWORK_AND_AI_DEMAND_CHAIN = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "APH",
    "ARM",
    "AVGO",
    "BDC",
    "BELFB",
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

SEMI_CHAIN = {
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
    "COHU",
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
    "MRAM",
    "MXL",
    "NVMI",
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
}

NVT_SCORES = {
    "NTM兑现优先": 83.0,
    "右尾弹性优先": 82.0,
    "风险调整收益": 60.0,
    "下行保护优先": 68.0,
    "估值消化优先": 59.0,
    "近端催化优先": 80.0,
    "价格确认/动量": 78.0,
    "激进短线": 80.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def apply_floors(companies: dict[str, dict], floors: dict[str, dict[str, float]]) -> None:
    for ticker, score_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in score_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)
            company["scores"][strategy] = max(current, floor)


def recompute_tiers(companies: dict[str, dict]) -> None:
    for strategy in STRATS:
        scored = [
            company.get("scores", {}).get(strategy)
            for company in companies.values()
            if company.get("scores", {}).get(strategy) is not None
        ]
        scored.sort(reverse=True)
        total = len(scored)
        if not total:
            continue
        cuts = {
            "S": scored[max(0, int(total * 0.07) - 1)],
            "A": scored[max(0, int(total * 0.25) - 1)],
            "B": scored[max(0, int(total * 0.55) - 1)],
            "C": scored[max(0, int(total * 0.85) - 1)],
        }
        for company in companies.values():
            score = company.get("scores", {}).get(strategy)
            if score is None:
                tier = "资料不足"
                rank = None
            elif score >= cuts["S"]:
                tier = "S"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["A"]:
                tier = "A"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["B"]:
                tier = "B"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["C"]:
                tier = "C"
                rank = sum(1 for value in scored if value > score) + 1
            else:
                tier = "D"
                rank = sum(1 for value in scored if value > score) + 1
            company.setdefault("tiers", {})[strategy] = tier
            company.setdefault("ranks", {})[strategy] = rank
            company.setdefault("rank_total", {})[strategy] = total

    for company in companies.values():
        if not company.get("fin", {}).get("price"):
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"
                company.setdefault("ranks", {})[strategy] = None


def score_companies(companies: dict[str, dict]) -> None:
    if hasattr(project_calibration, "fix_growth_ranges"):
        project_calibration.fix_growth_ranges(companies)

    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    apply_floors(companies, getattr(project_calibration, "SCORE_FLOORS", {}))
    apply_floors(companies, getattr(etn_calibration, "LOCAL_SCORE_FLOORS", {}))
    apply_floors(companies, getattr(jci_calibration, "ADDITIONAL_SCORE_FLOORS", {}))
    apply_floors(companies, getattr(mod_calibration, "LOCAL_SCORE_FLOORS", {}))

    for ticker, score_map in [
        ("ETN", getattr(etn_calibration, "ETN_SCORES", {})),
        ("HUBB", getattr(hubb_calibration, "HUBB_SCORES", {})),
        ("JCI", getattr(jci_calibration, "JCI_SCORES", {})),
        ("MOD", getattr(mod_calibration, "MOD_SCORES", {})),
    ]:
        if ticker in companies:
            for strategy, score in score_map.items():
                companies[ticker].setdefault("scores", {})[strategy] = score

    for strategy, score in NVT_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_ELECTRICAL_PEERS or ticker in DIRECT_COOLING_RACK_PEERS:
        return "直接同业"
    if ticker in POWER_ELECTRICAL_INFRA or ticker in INDUSTRIAL_AND_ENGINEERING_INFRA:
        return "相邻替代"
    if ticker in UTILITY_AND_POWER_CUSTOMERS or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_NETWORK_AND_AI_DEMAND_CHAIN or ticker in SEMI_CHAIN:
        return "上下游"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {
        "AI服务器_存储_EMS",
        "AI网络_光互联_连接器",
        "AI计算芯片_EDA_IP_custom_ASIC",
        "云算力_IDC_AI软件平台",
        "晶圆制造_前道设备",
        "封测_检测_计量_光罩",
    }:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        return "业务差异大且档位接近" if rel == "跨赛道" else "证据互有强弱且档位接近"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "NVT订单/backlog和2026指引更硬",
            "右尾弹性优先": "NVT液冷/机柜/PDU右尾更直接",
            "风险调整收益": "NVT增长、FCF和AI设施暴露更均衡",
            "下行保护优先": "NVT现金流和净杠杆底盘更稳",
            "估值消化优先": "NVT收入高增更能消化估值",
            "近端催化优先": "NVT Q2订单/margin/液冷验证更近",
            "价格确认/动量": "NVT价格确认和资金偏好更强",
            "激进短线": "NVT液冷AI题材和波动更适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单或backlog更硬",
            "右尾弹性优先": f"{ticker}同业右尾或利润池更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业业绩更能覆盖估值",
            "近端催化优先": f"{ticker}同业订单/产能催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}收入/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker}AI主链或客户侧右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}订单/backlog或交付更清楚",
            "右尾弹性优先": f"{ticker}右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker}增长与估值组合更优",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}订单兑现更能消化估值",
            "近端催化优先": f"{ticker}近端订单或产能催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}AI主链兑现证据更硬",
            "右尾弹性优先": f"{ticker}小基数或AI收入弹性更大",
            "风险调整收益": f"{ticker}增长赔率更能覆盖风险",
            "下行保护优先": f"{ticker}需求能见度或现金流更好",
            "估值消化优先": f"{ticker}高增速更能消化估值",
            "近端催化优先": f"{ticker}产品/订单催化更密集",
            "价格确认/动量": f"{ticker}价格趋势更强",
            "激进短线": f"{ticker}高波动更适合短线进攻",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker}未来12个月兑现证据更直接",
        "右尾弹性优先": f"{ticker}极端情景上行更大",
        "风险调整收益": f"{ticker}风险调整赔率更好",
        "下行保护优先": f"{ticker}估值或资产质量更安全",
        "估值消化优先": f"{ticker}当前估值更易消化",
        "近端催化优先": f"{ticker}未来两个季度催化更明确",
        "价格确认/动量": f"{ticker}价格行为更强",
        "激进短线": f"{ticker}短线关注度和波动更强",
    }[strategy]


def label_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")
    bt = b.get("tiers", {}).get(strategy, "资料不足")
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0)
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 28, 13, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 21, 10, 4

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


def cell_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    return f"{label}：{reason_for(strategy, label, b, rel)}"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.20,
        "估值消化优先": 1.15,
        "下行保护优先": 1.05,
        "近端催化优先": 0.85,
        "右尾弹性优先": 0.80,
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
    for strategy in STRATS:
        score += weights[strategy] * label_score.get(tag_in_cell(row_obj[strategy]) or "中性", 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    if choice == "中性":
        return "NVT的液冷/配电右尾与对手增长、估值或现金流优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "NVT有2026高增指引、Q1有机订单约40%、26亿美元backlog和数据中心收入锚支撑NTM兑现。"
        if diffs["右尾弹性优先"] > 12:
            return "NVT的液冷、机柜/PDU、灰空间电气建筑和连接件组合更直接受益于高密AI机柜。"
        if diffs["价格确认/动量"] > 12:
            return "NVT的价格确认、AI液冷关注度和近端订单验证更适合该口径。"
        if diffs["下行保护优先"] > 10:
            return "NVT的FCF、净杠杆和工业/商住底盘比对手更能承受需求波动。"
        return "NVT在收入兑现、AI设施右尾、现金流和近端催化之间的组合更均衡。"

    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于NVT。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或防御属性明显强于NVT。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或估值组合比NVT更容易消化。"
    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于NVT。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比NVT更直接。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和短线资金偏好明显强于NVT。"
    return f"{ticker}在多数投资思路下比NVT更符合项目内资金配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) > tier_value(b.get("tiers", {}).get(strategy))]
    b_strong = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) < tier_value(b.get("tiers", {}).get(strategy))]
    close = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) == tier_value(b.get("tiers", {}).get(strategy))]
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts) if parts else "档位接近"


def comparison_sort_key(row_obj: dict) -> tuple[int, str, str]:
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return (rel_order.get(row_obj["relationship"], 9), row_obj["classification"], row_obj["ticker"])


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj = {
            "ticker": ticker,
            "name": b["name"],
            "classification": base.category_short(str(b.get("category", ""))),
            "relationship": rel,
            "grade_diff": grade_diff_summary(a, b),
        }
        for strategy in STRATS:
            row_obj[strategy] = cell_for(strategy, a, b, rel)
        ac, bc, nc = direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        row_obj["final_choice"] = final_choice(row_obj)
        row_obj["key_reason"] = key_reason(a, b, row_obj, row_obj["final_choice"])
        rows.append(row_obj)
    return sorted(rows, key=comparison_sort_key)


def fmt_num(value, decimals: int = 2) -> str:
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


def majority_rows(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
    selected = [row for row in rows if row["final_choice"] == final]
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

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][tag_in_cell(row_obj[strategy])] += 1

    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]])

    support = {
        "NTM兑现优先": (
            "强势档",
            "2026Q1销售12.42亿美元、同比+53%、有机+34%，2026全年销售指引+26%-28%、有机+21%-23%，有机订单约+40%、backlog 26亿美元",
            "高增长需要backlog顺利转收入；液冷客户认证、现场调试、灰空间工程交付和外部电力设备仍是约束",
        ),
        "右尾弹性优先": (
            "全项目强档",
            "2025数据中心收入超过10亿美元，液冷、机柜/围护、PDU/配电、灰空间电气建筑和连接件共同受益于高功率AI rack",
            "公司不是GPU/光模块小基数主链；800VDC、1MW rack和telemetry等更偏2027+期权，产品级收入仍需估算",
        ),
        "风险调整收益": (
            "中上档",
            "NTM基准收入50.5-52.5亿美元、adjusted EBITDA 12.3-13.4亿美元、FCF 6.8-7.8亿美元，净杠杆约1.5x",
            "2026-06-22 Forward PE 32.71、P/S 6.89、EV/EBITDA 32.61，估值要求数据中心/电力公用事业持续兑现",
        ),
        "下行保护优先": (
            "中性偏弱",
            "2025 FCF约102% adjusted net income conversion，Q1仍正FCF，工业/商住基础业务和Electrical Connections利润率提供底盘",
            "三段SOXX压力窗口累计-43.93%，高估值和营运资金占用会削弱防守性",
        ),
        "估值消化优先": (
            "中上档",
            "FY2026高增指引、NTM基准收入+30%-35%和adjusted EPS/EBITDA增长能部分消化估值",
            "估值已反映大量AI液冷和电气建筑预期；若毛利率不能从Q1 35.9%修复或EC ROS继续承压，消化速度会变慢",
        ),
        "近端催化优先": (
            "全项目顶档",
            "Q2 organic +23%-25%指引、orders/backlog、液冷产能、Systems Protection ROS、EC ROS和数据中心收入可在1-2季度验证",
            "催化主要是持续验证和margin修复，若订单环比降速或客户验收推迟，市场会快速重估",
        ),
        "价格确认/动量": (
            "强势档",
            "2026-06-03过去两周+8.98%、过去一月+10.99%，2026-06-22收盘184.34高于6月初176.39，资金继续确认AI液冷/电力链",
            "上涨后估值更贵，若Q2订单、毛利率或FCF不匹配，价格确认可能变成透支",
        ),
        "激进短线": (
            "中性偏进攻",
            "Call IV 54.3%、Put IV 51.2%，液冷、NVIDIA reference、数据中心white/gray space和高密rack题材具备短线进攻性",
            "市值已近300亿美元，不如NeoCloud、核能开发、小盘光互联或亏损转盈利标的那样高beta",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "液冷系统与液冷小组件/服务",
            "高密度机柜、围护、白空间PDU",
            "灰空间工程化电气建筑和预制电力模块",
            "Electrical Connections基础设施",
            "工业、商业/住宅和非AI基础业务",
        ]

    lines: list[str] = [
        "# NVT 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：NVT / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 NVT vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。NVT 的优势集中在2026高增指引、Q1 organic orders约+40%、26亿美元backlog、数据中心收入超过10亿美元、液冷/机柜/PDU/灰空间电气建筑的组合收入化，以及近期价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值已经不便宜、毛利率与Electrical Connections ROS仍需修复、产品级客户/订单拆分不足，且市值已不小使短线非线性弱于更高beta的AI主链或小盘电力标的。",
        "- A 最适合的投资者画像：想配置AI数据中心facility layer，尤其看重液冷、机柜/围护、PDU、工程化电气建筑和连接件能在2026-2027持续转收入，同时愿意承受高估值验证压力的成长型资金。",
        "- A 最不适合的投资者画像：只追求最大AI芯片/内存/光互联右尾、最低估值安全垫、纯公用事业防守或极端短线高beta的资金；这些资金通常会转向NVDA/MU/AVGO/ALAB/VRT/POWL/OKLO/SMR等。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常拥有更直接AI主链收入、更大右尾弹性、更强风险调整收益、更便宜估值消化或更高短线爆发力。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：NVT 是项目内偏强的AI液冷/电气基础设施公司，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；相对多数传统工业、材料、低成长电气件和弱现金流标的更值得配置，但面对顶级AI主链、VRT/POWL/ETN/HUBB等直接电气/冷却替代时必须按思路拆分。",
        "- 后续最重要跟踪数据：Q2/Q3 organic orders、backlog和book-to-bill；data center revenue是否继续披露或可估算；liquid cooling订单/产能/现场服务；Systems Protection ROS；Electrical Connections ROS；毛利率、tariff offset和mix；working capital、inventory、receivables和FCF conversion；GB300/Rubin/800VDC相关客户认证与量产时间。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "NVT"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "配电_电源_功率器件")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "50.5-52.5 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '54.0-57.5 亿美元'}；极度乐观：{a.get('extreme_rev') or '59.0-63.5 亿美元'}"]),
        base.row(["利润和现金流结论", "基准 adjusted operating margin 20.0%-20.8%、adjusted EBITDA 12.3-13.4亿美元、adjusted net income 7.5-8.2亿美元、FCF 6.8-7.8亿美元；关键看毛利率和EC ROS能否从Q1压力中修复。"]),
        base.row(["最大传导瓶颈", "backlog转收入需要液冷/CDU/manifold客户认证、现场调试、灰空间工程交付、外部switchgear/变压器/并网节奏和客户架构稳定共同配合。"]),
        base.row(["最大反证", "产品级收入、客户名单、液冷/机柜/PDU/灰空间细分订单和800VDC/1MW rack收入未完全披露；估值已经要求2026-2027持续高增长和利润率修复。"]),
        base.row(["近端催化剂", "2026Q2/Q3 organic orders、backlog、data center revenue、liquid cooling record orders/产能、Systems Protection ROS、Electrical Connections ROS、tariff offset、working capital和FCF conversion。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]

    for strategy in STRATS:
        tier = a.get("tiers", {}).get(strategy, "资料不足")
        position = f"{support[strategy][0]}；评分排名 {a.get('ranks', {}).get(strategy)}/{a.get('rank_total', {}).get(strategy)}"
        lines.append(base.row([strategy, tier, position, support[strategy][1], support[strategy][2]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与NVT在液冷、机柜/围护、PDU、低压配电、连接/接地/线缆管理、工程化电气建筑或关键设施电气设备需求池重叠；优先比较订单/backlog、产品代际、客户认证、毛利率和同业估值。", "ETN、HUBB、POWL、ABBNY、ATKR、VRT、MOD、JCI、TT、CARR", "判断力度最高；若对手在订单、利润率、估值或价格确认上明显更强，可压过NVT的高增长指引。"]),
        base.row(["相邻替代", "同属AI园区电力、冷却、MEP、发电、储能、核能、工程建设或工业基础设施资金篮子，但产品不完全重叠。", "GEV、PWR、EME、FIX、IESC、BE、GNRC、ENS、CMI、AAON", "重点回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好。"]),
        base.row(["上下游", "B位于NVT需求链上下游，如云厂、IDC、NeoCloud、服务器、芯片、网络、发电、公用事业和半导体设备材料。", "MSFT、AMZN、GOOGL、META、ORCL、EQIX、DLR、CRWV、NVDA、DELL、ANET、TSM、ASML", "不把下游capex直接等同NVT收入；若对方拥有更直接AI收入、RPO或价格确认，可在右尾、催化和动量列胜出。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "部分材料、化学品、软件、生命科学和航天公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]

    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    lines.append(base.row(headers))
    lines.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for idx, row_obj in enumerate(comparisons, 1):
        cells = [
            idx,
            f"{row_obj['ticker']} / {row_obj['name']}",
            row_obj["classification"],
            row_obj["relationship"],
            row_obj["grade_diff"],
        ] + [row_obj[strategy] for strategy in STRATS] + [
            row_obj["majority"],
            row_obj["final_choice"],
            row_obj["key_reason"],
        ]
        lines.append(base.row(cells))

    lines += [
        "",
        "## 6. 投资思路统计",
        "",
        base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]),
        base.row(["---"] + ["---:"] * 9),
    ]
    for strategy in STRATS:
        c = stats[strategy]
        lines.append(base.row([strategy] + [c[tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_b, 1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        catchup = "NVT需要继续证明data center收入、液冷订单、backlog转收入、毛利率修复和FCF能同步兑现，并降低估值透支风险。"
        if row_obj["relationship"] == "直接同业":
            catchup = "NVT需要在直接同业中证明液冷/机柜/PDU/灰空间订单、利润率和客户认证强于B，且估值没有过度透支。"
        elif row_obj["relationship"] == "上下游":
            catchup = "NVT需要证明云厂/AI主链capex能持续落到其设施侧产品和利润，而不是只停留在行业TAM。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strategy for strategy in STRATS if "投A" in row_obj[strategy]]
        catchup = "B需要拿出更清晰的NTM收入/利润兑现、订单或客户合同，并证明估值、现金流和压力窗口能承受波动。"
        if "右尾弹性优先" in wins and row_obj["final_choice"] == "A":
            catchup = "B需要把右尾叙事转成可确认收入、利润和现金流，并降低估值或融资反证。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/配电_电源_功率器件/NVT_nVent_Electric_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心低压配电、PDU与母线槽_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 外部官方校验来源：SEC 8-K/Exhibit 99.1 Q1 2026 press release `https://www.sec.gov/Archives/edgar/data/1720635/000162828026029098/q12026nvtpressrelease.htm`；nVent 2026 Investor Day press release `https://investors.nvent.com/press-releases/press-release-details/2026/nVent-Highlights-Portfolio-Transformation-and-Growth-Priorities-at-2026-Investor-Day/default.aspx`；nVent 2026 Investor Day event page `https://investors.nvent.com/events-and-presentations/event-details/2026/2026-Investor-Day-2026-ACxKq2G1aI/default.aspx`。",
        f"- NVT 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_nvt_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的使用既有正式脚本的最低分校准，对NVT的2026指引、Q1 organic orders/backlog、数据中心收入、液冷/机柜/PDU/灰空间暴露、估值、IV、价格确认和利润率修复风险做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        lines.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{Path(company['path']).name}`"]))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 NVT 正式评估文件")
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
                "nvt_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "nvt_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "nvt_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
