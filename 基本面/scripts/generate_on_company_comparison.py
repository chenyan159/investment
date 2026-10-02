from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_etn_company_comparison as etn_calibration
import generate_hubb_company_comparison as hubb_calibration
import generate_nvt_company_comparison as framework


TARGET = "ON"
TARGET_NAME = "onsemi"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ON_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_POWER_ANALOG_PEERS = {
    "ADI",
    "AOSL",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MCHP",
    "MIELY",
    "MPWR",
    "MRAAY",
    "NVTS",
    "POWI",
    "ST",
    "STM",
    "TTDKY",
    "TXN",
    "VICR",
    "VSH",
    "WOLF",
}

AI_COMPUTE_ADJACENT = {
    "ALAB",
    "AMD",
    "ARM",
    "AVGO",
    "CDNS",
    "INTC",
    "MRVL",
    "MTSI",
    "MXL",
    "NVDA",
    "QCOM",
    "RMBS",
    "SIMO",
    "SITM",
    "SMTC",
    "SNPS",
}

AI_POWER_ELECTRICAL_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "BE",
    "ENS",
    "ENPH",
    "ETN",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "NVT",
    "POWL",
    "PSIX",
    "VRT",
}

DATA_CENTER_AND_SERVER_CHAIN = {
    "AAOI",
    "ADBE",
    "AMZN",
    "ANET",
    "APH",
    "APLD",
    "BABA",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CRWD",
    "CRWV",
    "CSCO",
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
    "LITE",
    "LWLG",
    "META",
    "MSFT",
    "MU",
    "NBIS",
    "NOK",
    "NTAP",
    "NTNX",
    "ORCL",
    "PENG",
    "POET",
    "PSTG",
    "SANM",
    "SMCI",
    "SNDK",
    "STX",
    "TEL",
    "VIAV",
    "VISN",
    "WDC",
}

FABS_EQUIPMENT_AND_MATERIALS = {
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
    "COHU",
    "DSCSY",
    "ENTG",
    "FORM",
    "GFS",
    "HOCPY",
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LIN",
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

UTILITY_AND_CAMPUS_POWER = {
    "AEP",
    "BWXT",
    "CEG",
    "CMI",
    "DTE",
    "ET",
    "ETR",
    "FCEL",
    "HTHIY",
    "OKLO",
    "PWR",
    "RYCEY",
    "SMR",
    "VST",
}

INDUSTRIAL_CROSS_OR_ADJACENT = {
    "AAON",
    "ALLE",
    "APD",
    "CARR",
    "CAT",
    "CC",
    "DCI",
    "DD",
    "DHR",
    "DKILY",
    "DOV",
    "ECL",
    "EME",
    "FIX",
    "FTV",
    "IESC",
    "JCI",
    "MOD",
    "MMM",
    "MSI",
    "MTRN",
    "MYRG",
    "NDSN",
    "PH",
    "PNR",
    "TDY",
    "TMO",
    "TT",
}

ON_SCORES = {
    "NTM兑现优先": 67.5,
    "右尾弹性优先": 72.0,
    "风险调整收益": 49.0,
    "下行保护优先": 60.0,
    "估值消化优先": 55.0,
    "近端催化优先": 68.0,
    "价格确认/动量": 83.0,
    "激进短线": 86.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    framework.score_companies(companies)
    base.TARGET = old_target

    if "ETN" in companies:
        companies["ETN"].setdefault("scores", {}).update(etn_calibration.ETN_SCORES)
    if "HUBB" in companies:
        companies["HUBB"].setdefault("scores", {}).update(hubb_calibration.HUBB_SCORES)

    for strategy, score in ON_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    framework.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_POWER_ANALOG_PEERS:
        return "直接同业"
    if ticker in AI_COMPUTE_ADJACENT:
        return "相邻替代"
    if ticker in AI_POWER_ELECTRICAL_ADJACENT or ticker in INDUSTRIAL_CROSS_OR_ADJACENT:
        return "相邻替代"
    if ticker in DATA_CENTER_AND_SERVER_CHAIN or ticker in FABS_EQUIPMENT_AND_MATERIALS or ticker in UTILITY_AND_CAMPUS_POWER:
        return "上下游"
    if category == "配电_电源_功率器件":
        return "直接同业"
    if category in {"电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器", "云算力_IDC_AI软件平台", "晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category == "AI计算芯片_EDA_IP_custom_ASIC":
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "直接同业":
            return "同业证据接近，需等订单和毛利验证"
        if rel == "跨赛道":
            return "业务差异大且证据互抵"
        return "档位接近，证据互有强弱"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "ON有Q2指引、RPO/LTSA和三分部收入锚",
            "右尾弹性优先": "ON有AI电源、SiC/GaN和800VDC期权",
            "风险调整收益": "ON正FCF和恢复路径抵消部分估值压力",
            "下行保护优先": "ON已有现金流和车工底盘支撑",
            "估值消化优先": "ON基准恢复可部分消化估值",
            "近端催化优先": "ON有Q2、AI power tree和客户项目验证",
            "价格确认/动量": "ON近期价格确认明显强于对手",
            "激进短线": "ON高IV、AI电源和800V叙事更适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入/订单兑现更硬",
            "右尾弹性优先": f"{ticker}同业小基数或平台右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业业绩更能覆盖估值",
            "近端催化优先": f"{ticker}同业订单/产品催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业beta和波动更适合短线",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}收入/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker}AI主链或需求端右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流、规模或资产质量更防守",
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
        strong_cut, suggest_cut, micro_cut = 29, 14, 4
    elif rel == "直接同业":
        strong_cut, suggest_cut, micro_cut = 19, 9, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 22, 10, 4

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
    ac, bc, _nc = direction_counts(row_obj)
    if ac > bc:
        return "A"
    if bc > ac:
        return "B"

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
        return "ON的AI电源和车工恢复与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 9:
            return "ON有2026Q2指引、PSG/AMG/ISG分部收入和RPO/LTSA支撑NTM恢复。"
        if diffs["近端催化优先"] > 10:
            return "ON的AI power tree采用、Q2指引、汽车/工业恢复和800VDC合作节点更近。"
        if diffs["价格确认/动量"] > 12:
            return "ON近期价格确认和高IV资金偏好强于对手。"
        if diffs["右尾弹性优先"] > 10:
            return "ON的AI电源、SiC/GaN、Treo和800VDC组合给右尾留下空间。"
        return "ON在收入恢复、AI电源期权和短线动量之间的组合略好。"

    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或压力期表现比ON更安全。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于ON。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或估值组合比ON更容易消化。"
    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于ON。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比ON更硬。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比ON更直接。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和短线资金偏好明显强于ON。"
    return f"{ticker}在多数投资思路下比ON更符合项目内资金配置目标。"


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
    if final == "B":
        selected = [row for row in rows if row["bc"] >= 5 and row["bc"] - row["ac"] >= 3]
    elif final == "A":
        selected = [row for row in rows if row["ac"] >= 5 and row["ac"] - row["bc"] >= 3]
    else:
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
    missing_price = sorted([ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price")])
    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})

    price_from_0603 = None
    if fin.get("price") and m2w.get("latest_close"):
        price_from_0603 = ((fin.get("price") / m2w.get("latest_close")) - 1) * 100
    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去一月 {fmt_pct(m1m.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}；"
        f"2026-06-22收盘较2026-06-03收盘 {fmt_pct(price_from_0603)}。"
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
            "中上档",
            "2026Q1收入15.133亿美元、2026Q2指引中点15.85亿美元；PSG/AMG/ISG三分部披露清楚；LTSAs/RPO约65亿美元且约35%预计12个月内确认",
            "NTM基准64.5-68.5亿美元只比TTM约+6%-+13%；汽车/工业和PSG利用率仍是主要约束",
        ),
        "右尾弹性优先": (
            "中上档",
            "乐观/极度乐观收入70-76/78-85亿美元；AI数据中心收入同比超过2倍、环比超过30%，叠加SiC、GaNEXUS/vGaN、Treo和800VDC期权",
            "AI数据中心、SiC、GaN和Treo单项金额未披露，800VDC更偏2027+，右尾可信度低于AI主链和小基数标的",
        ),
        "风险调整收益": (
            "中上偏中性",
            "基准毛利率38.5%-40.5%、经营利润率16%-19%，自由现金流约8-12亿美元方向；公司仍有正FCF和订单可见度",
            "2026-06-22 Forward PE 30.49、P/S 8.44、Call IV 80.4%，且库存和PSG毛利率修复不确定",
        ),
        "下行保护优先": (
            "中性偏弱",
            "Q1经营现金流2.391亿美元、自由现金流约2.172亿美元；AMG毛利率较高，汽车/工业客户生命周期较长",
            "三段SOXX压力窗口累计-75.45%，近月IV约80%，汽车/工业周期、SiC价格和库存会放大回撤",
        ),
        "估值消化优先": (
            "中上偏弱",
            "若基准收入64.5-68.5亿美元、经营利润率16%-19%兑现，Forward PE 30.49可被恢复性利润部分消化",
            "P/S 8.44已不低；若AI电源绝对金额、PSG毛利率或库存周转不验证，估值消化会降档",
        ),
        "近端催化优先": (
            "强势档",
            "Q2实际/后续指引、AI power tree采用、NVIDIA 800VDC合作、Geely/NIO/Xiaomi/Sineng项目和库存周转均是1-2季度验证点",
            "催化需要转成绝对收入、毛利率和FCF；产品发布或design-in不能直接替代订单确认",
        ),
        "价格确认/动量": (
            "强势档",
            "2026-06-03过去两周+21.52%、过去一月+29.99%，2026-06-22仍接近6月初高位，市场已经交易AI电源和周期修复",
            "6/22较6/03回落约1.78%，高IV意味着动量若无业绩确认容易反噬",
        ),
        "激进短线": (
            "中上偏进攻",
            "Call IV 80.4%、Put IV 82.1%，AI电源、800VDC、SiC/GaN、汽车高压和近期价格确认提供事件弹性",
            "市值约511.5亿美元且基准增长不极端，短线爆发力弱于小基数光互联、NeoCloud、核电和亏损转盈利高beta",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "PSG智能功率",
            "AMG模拟与混合信号",
            "ISG智能感知",
            "AI数据中心供电链",
            "EliteSiC与汽车高压平台",
            "GaNEXUS/vGaN与Treo",
        ]

    lines: list[str] = [
        "# ON 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：ON / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 ON vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ON 最强的是近期价格确认、AI数据中心供电链和800VDC/GaN/SiC/Treo等近端事件叙事；它不是全项目最高确定性经营兑现公司，但短线和催化层面有明显存在感。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是汽车/工业周期仍在恢复、PSG毛利率和库存周转需要验证，AI数据中心绝对收入未披露，且80%左右IV和-75.45%的SOXX压力窗口表现削弱下行保护。",
        "- A 最适合的投资者画像：想在成熟车规/工业功率半导体里叠加AI数据中心供电、SiC/GaN、800VDC和近期价格确认的进攻型资金；更适合催化/动量/右尾思路，而不是纯防守或低估值价值配置。",
        "- A 最不适合的投资者画像：只要求最高NTM兑现、最强AI主链收入、最厚现金流安全垫或最低估值消化压力的资金；这些资金通常会转向NVDA/AVGO/MRVL/ALAB/MU、VRT/ETN/POWL/HUBB或公用事业/云平台现金流标的。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在直接AI收入、订单/RPO、利润池位置、估值消化、下行保护或小基数短线弹性上压过ON。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：ON 是项目内中上但不顶尖的功率/模拟半导体恢复与AI电源期权标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它强于多数低成长、低动量或缺收入锚公司，但面对AI主链、顶级电力/冷却设备和低估值高FCF防守资产时必须按思路拆分。",
        "- 后续最重要跟踪数据：Q2实际收入和Q3指引；PSG/AMG/ISG收入与毛利率；AI数据中心绝对收入或订单披露；LTSAs/RPO十二个月确认比例；汽车/工业end market环比；库存和产能利用率；SiC ASP/良率；GaNEXUS/vGaN量化订单；Treo车型平台；NVIDIA 800VDC/HV IBC客户验证和2027 ramp指引。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ON"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["scenarios"]["base"].get("NTM 公司收入", "缺失")]),
        base.row(["乐观/极度乐观收入", f"{a['scenarios']['bull'].get('NTM 公司收入', '缺失')} / {a['scenarios']['extreme'].get('NTM 公司收入', '缺失')}"]),
        base.row(["利润和现金流结论", f"{a['scenarios']['base'].get('EBITDA/净利润', '')}；{a['scenarios']['base'].get('自由现金流方向', '')}"]),
        base.row(["最大传导瓶颈", "AI数据中心、SiC、GaN、Treo等关键产品单项收入未披露，从design-in和客户采用传到NTM收入仍需要SKU、交付量、份额、ASP和毛利率验证。"]),
        base.row(["最大反证", "Q2之后季度run-rate低于15.5-16.0亿美元；AI数据中心绝对收入不披露或增长放缓；PSG毛利率无法修复；汽车/工业客户继续去库存或价格重谈；库存和制造调整吞噬FCF。"]),
        base.row(["近端催化剂", "Q2实际与Q3指引、AI power tree出货或订单、NVIDIA 800VDC合作进展、SiC/Geely/NIO/Xiaomi平台、Sineng储能/逆变器项目、GaNEXUS/vGaN和Treo量化订单。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        rank = a.get("ranks", {}).get(strategy)
        total = a.get("rank_total", {}).get(strategy) or len(companies)
        lines.append(base.row([strategy, a["tiers"][strategy], f"第 {rank}/{total}，{a['tiers'][strategy]} 档", support[strategy][1], support[strategy][2]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与ON在功率半导体、模拟/电源管理、车规/工业半导体、SiC/GaN、AI PSU/BBU/保护/驱动或传感器需求池中重叠。", "ADI、TXN、MCHP、IFNNY、STM、MPWR、AOSL、DIOD、NVTS、POWI、WOLF、VICR", "优先比较同业订单、收入表、客户认证、产品代际、毛利率、SiC/GaN进展和估值消化。"]),
        base.row(["相邻替代", "同属AI半导体、AI电源、数据中心电气或车工周期修复资金篮子，但产品不直接替代；资金可能在ON与AI主链/电力设备之间二选一。", "NVDA、AVGO、MRVL、ALAB、ETN、VRT、HUBB、NVT、POWL、GEV", "默认按档位判断；只有增长质量、订单可见度、估值消化或风险收益明显拉开时才给建议级结论。"]),
        base.row(["上下游", "云厂、服务器、网络、存储、晶圆制造、封测、材料、设备、公用事业和数据中心运营商处在ON需求或供给链上下游。", "MSFT、AMZN、GOOGL、DELL、SMCI、ANET、TSM、ASML、AMAT、TER、CEG", "不把下游AI capex或上游设备订单直接等同于ON收入，重点看利润池位置、议价权、订单/RPO和收入确认链条。"]),
        base.row(["跨赛道", "软件、材料、医疗工具、普通工业、化工和业务差异较大的公司，仍作为项目资金配置替代比较。", "ADBE、TMO、DHR、ECL、LIN、CAT、RKLB", "默认降低结论力度；若证据互有强弱，优先中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
        base.row(["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATS, "多数思路方向", "最终更值得投", "最关键理由"]),
        base.row(["---:", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(comparisons, start=1):
        lines.append(
            base.row(
                [
                    index,
                    f"{row_obj['ticker']} / {row_obj['name']}",
                    row_obj["classification"],
                    row_obj["relationship"],
                    row_obj["grade_diff"],
                    *[row_obj[strategy] for strategy in STRATS],
                    row_obj["majority"],
                    "ON" if row_obj["final_choice"] == "A" else row_obj["ticker"] if row_obj["final_choice"] == "B" else "中性",
                    row_obj["key_reason"],
                ]
            )
        )

    lines += [
        "",
        "## 6. 投资思路统计",
        "",
        base.row(["投资思路", *TAG_ORDER, "A侧合计", "B侧合计"]),
        base.row(["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]),
    ]
    for strategy in STRATS:
        lines.append(base.row([strategy, *[stats[strategy][tag] for tag in TAG_ORDER], a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_b, start=1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        need = "ON需要披露更清晰的AI数据中心绝对收入/订单、PSG/AMG毛利率修复、库存周转和FCF，并证明估值与高IV不是透支。"
        if row_obj["relationship"] == "直接同业":
            need = "ON需要在功率/模拟同业中证明AI电源、SiC/GaN、汽车高压或AMG控制产品的份额、毛利和订单强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "ON需要证明下游AI capex和高密机柜供电能持续落到自己的器件/控制/驱动收入，而不是只停留在行业TAM。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_a, start=1):
        b = companies[row_obj["ticker"]]
        wins = [strategy for strategy in STRATS if "投A" in row_obj[strategy]]
        need = "B需要拿出更硬订单/RPO、更强NTM收入利润兑现，或证明估值、现金流和执行反证低于ON。"
        if b.get("scores", {}).get("右尾弹性优先", 0) > a.get("scores", {}).get("右尾弹性优先", 0):
            need = "B需要把右尾叙事转成可确认收入/利润，并证明估值、现金流和执行反证可控。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/AI计算芯片_EDA_IP_custom_ASIC/ON_onsemi_公司调研_2026-06-12.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/`、`特征量化/` 或既有公司对比成品。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；价格缺失或不可用公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_服务器BMC、MCU与嵌入式控制_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_商用AI加速芯片_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- ON 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_on_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的使用既有正式脚本中的最低分校准，对ON的Q1/Q2收入表、RPO/LTSA、AI数据中心增长、SiC/GaN/Treo/800VDC期权、PSG毛利/库存反证、估值、IV、区间涨跌和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
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
        raise SystemExit("缺少 ON 正式评估文件")
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
                "on_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "on_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "on_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
