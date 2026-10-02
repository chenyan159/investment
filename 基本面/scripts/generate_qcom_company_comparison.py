from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_nvt_company_comparison as framework


TARGET = "QCOM"
TARGET_NAME = "Qualcomm"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "QCOM_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_AI_COMPUTE_PEERS = {
    "AMD",
    "AVGO",
    "INTC",
    "MRVL",
    "NVDA",
}

ADJACENT_AI_SEMI_PEERS = {
    "ADI",
    "ALAB",
    "ARM",
    "CDNS",
    "MCHP",
    "MTSI",
    "MXL",
    "ON",
    "RMBS",
    "SIMO",
    "SITM",
    "SMTC",
    "SNPS",
    "STM",
    "TXN",
}

EDGE_AUTO_POWER_ADJACENT = {
    "AOSL",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MIELY",
    "MPWR",
    "MRAAY",
    "NVTS",
    "POWI",
    "ST",
    "TTDKY",
    "VICR",
    "VSH",
    "WOLF",
}

NETWORK_CONNECTIVITY_ADJACENT = {
    "AAOI",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "HPE",
    "LITE",
    "LWLG",
    "NOK",
    "POET",
    "TEL",
    "VIAV",
    "VISN",
}

CLOUD_AND_AI_CUSTOMERS = {
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

SERVER_STORAGE_CHAIN = {
    "CLS",
    "DELL",
    "FLEX",
    "FN",
    "JBL",
    "MRAM",
    "MU",
    "NTAP",
    "PENG",
    "PSTG",
    "SANM",
    "SMCI",
    "SNDK",
    "STX",
    "WDC",
}

FOUNDRY_EQUIPMENT_MATERIALS_CHAIN = {
    "ACLS",
    "ACMR",
    "AEHR",
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
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

DATA_CENTER_INFRA_ADJACENT = {
    "AAON",
    "ABBNY",
    "AEIS",
    "APD",
    "ATKR",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "CMI",
    "DKILY",
    "EME",
    "ENS",
    "ETN",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "JCI",
    "MOD",
    "MYRG",
    "NVT",
    "OKLO",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "TT",
    "VRT",
    "VST",
}

INDUSTRIAL_CROSS = {
    "AJNMY",
    "ALLE",
    "AMPX",
    "APD",
    "CAT",
    "CC",
    "DCI",
    "DD",
    "DHR",
    "DOV",
    "DTE",
    "ECL",
    "ET",
    "ETR",
    "FCEL",
    "FTV",
    "IESC",
    "MMM",
    "MSI",
    "MTRN",
    "NDSN",
    "PH",
    "PNR",
    "RKLB",
    "TDY",
    "TMO",
    "TSLA",
}

QCOM_SCORES = {
    "NTM兑现优先": 66.5,
    "右尾弹性优先": 72.5,
    "风险调整收益": 58.5,
    "下行保护优先": 64.0,
    "估值消化优先": 67.0,
    "近端催化优先": 74.0,
    "价格确认/动量": 82.0,
    "激进短线": 83.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    framework.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in QCOM_SCORES.items():
        target.setdefault("scores", {})[strategy] = score
    framework.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_AI_COMPUTE_PEERS:
        return "直接同业"
    if ticker in ADJACENT_AI_SEMI_PEERS or ticker in EDGE_AUTO_POWER_ADJACENT or ticker in NETWORK_CONNECTIVITY_ADJACENT:
        return "相邻替代"
    if ticker in CLOUD_AND_AI_CUSTOMERS or ticker in SERVER_STORAGE_CHAIN or ticker in FOUNDRY_EQUIPMENT_MATERIALS_CHAIN:
        return "上下游"
    if ticker in DATA_CENTER_INFRA_ADJACENT:
        return "相邻替代"
    if ticker in INDUSTRIAL_CROSS:
        return "跨赛道"
    if category == "AI计算芯片_EDA_IP_custom_ASIC":
        return "相邻替代"
    if category in {"AI网络_光互联_连接器", "AI服务器_存储_EMS", "云算力_IDC_AI软件平台", "晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in {"配电_电源_功率器件", "电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "直接同业":
            return "同业证据互有强弱，需看AI收入确认"
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，增长与估值互抵"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "QCOM有手机/QTL/汽车/IoT和Q3指引硬锚",
            "右尾弹性优先": "QCOM有AI200、HUMAIN、Alphawave和汽车右尾",
            "风险调整收益": "QCOM估值低于AI主链且QTL现金流缓冲",
            "下行保护优先": "QCOM QTL高利润和资产负债表更稳",
            "估值消化优先": "QCOM Forward PE约20.8倍更易消化",
            "近端催化优先": "QCOM有Q3财报、AI200和Dragonwing节点",
            "价格确认/动量": "QCOM近月价格确认明显强于对手",
            "激进短线": "QCOM高IV叠加数据中心推理期权",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}的AI芯片收入或订单兑现更硬",
            "右尾弹性优先": f"{ticker}的AI主链或ASIC右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或生态护城河更强",
            "估值消化优先": f"{ticker}收入增速更能覆盖估值",
            "近端催化优先": f"{ticker}的AI产品/客户催化更近",
            "价格确认/动量": f"{ticker}同业价格趋势更强",
            "激进短线": f"{ticker}的AI beta和关注度更适合短攻",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}订单/RPO或收入确认链更短",
            "右尾弹性优先": f"{ticker}的AI需求端或瓶颈利润池更大",
            "风险调整收益": f"{ticker}上行与下行组合更优",
            "下行保护优先": f"{ticker}现金流、规模或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}收入、订单或交付可见度更强",
            "右尾弹性优先": f"{ticker}右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker}增长与估值组合更好",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}订单兑现更能消化估值",
            "近端催化优先": f"{ticker}近端订单或产品催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}的AI链兑现证据更硬",
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
        strong_cut, suggest_cut, micro_cut = 20, 9, 4
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
        return "QCOM的现金流/汽车/边缘AI与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["估值消化优先"] > 10:
            return "QCOM的Forward PE约20.8倍、P/S约5.3倍和QTL现金流使估值消化更容易。"
        if diffs["下行保护优先"] > 10:
            return "QCOM有QTL高利润、健康资产负债表和成熟QCT现金流托底。"
        if diffs["近端催化优先"] > 10:
            return "QCOM的FY26Q3财报、AI200/HUMAIN、Alphawave和Dragonwing节点更密集。"
        if diffs["价格确认/动量"] > 12:
            return "QCOM近月价格确认和高IV关注度强于对手。"
        if diffs["右尾弹性优先"] > 10:
            return "QCOM的AI200、汽车Digital Chassis和Alphawave给右尾留下空间。"
        return "QCOM在成熟现金流、汽车增长、AI推理期权和估值之间的组合略优。"

    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或AI收入兑现比QCOM更硬。"
    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于QCOM。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于QCOM。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或压力期表现比QCOM更安全。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或估值组合比QCOM更容易消化。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比QCOM更直接。"
    if diffs["激进短线"] < -12:
        return f"{ticker}短线高beta、AI叙事或价格爆发力强于QCOM。"
    return f"{ticker}在多数投资思路下比QCOM更符合项目内资金配置目标。"


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
    rows: list[dict] = []
    for ticker in sorted(ticker for ticker in companies if ticker != TARGET):
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


def majority_rows(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
    if final == "B":
        selected = [row for row in rows if row["bc"] >= 5 and row["bc"] - row["ac"] >= 3]
        selected.sort(key=lambda row: (row["bc"] - row["ac"], row["bc"], -row["nc"]), reverse=True)
    elif final == "A":
        selected = [row for row in rows if row["ac"] >= 5 and row["ac"] - row["bc"] >= 3]
        selected.sort(key=lambda row: (row["ac"] - row["bc"], row["ac"], -row["nc"]), reverse=True)
    else:
        selected = [row for row in rows if row["final_choice"] == final]
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
    a_best = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy])[:3]
    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) or "无"

    support = {
        "NTM兑现优先": (
            "FY26Q2总收入105.99亿美元，FY26Q3指引92-100亿美元；Handsets/QTL/Automotive/IoT都有正式收入表，汽车FY26Q2同比+38%，QTL为高利润稳定器",
            "NTM基准收入430-480亿美元只相对最近四季约-3%至+8%，手机仍受内存/渠道库存和Android竞争约束，AI200不应大额进基准",
        ),
        "右尾弹性优先": (
            "乐观/极度乐观收入490-570/580-700亿美元；AI200/AI250、HUMAIN 200MW、Alphawave custom silicon、Dragonwing和汽车Digital Chassis构成多点期权",
            "AI200/HUMAIN未披露订单金额、ASP、rack数和验收；Alphawave收入确认滞后，右尾可信度低于NVDA/AVGO/MRVL/ALAB等AI主链",
        ),
        "风险调整收益": (
            "2026-06-22 Forward PE 20.79、P/S 5.26显著低于许多AI高beta标的；QTL与成熟QCT支撑现金流，汽车增长提供结构性改善",
            "Call IV 86.2%、SOXX压力窗口累计-51.77%，手机周期、Apple/MediaTek/华为竞争和AI200执行不确定削弱赔率",
        ),
        "下行保护优先": (
            "QTL授权EBT margin高，资本开支轻；公司资产负债表健康，成熟手机/IoT/QTL现金流能为新业务提供缓冲",
            "高IV、6月初以后价格回撤、手机最大收入池下行和AI数据中心未确认收入意味着下行保护不是全项目顶档",
        ),
        "估值消化优先": (
            "Forward PE约20.79倍、P/S约5.26倍；若基准430-480亿美元收入和96-125亿美元non-GAAP净利兑现，估值可由成熟现金流消化",
            "收入增长不极端，若手机不修复、AI200只停留PoC或Alphawave并表低于预期，估值难显著上修",
        ),
        "近端催化优先": (
            "FY26Q3财报与FY26Q4指引、手机Q3后是否触底、汽车季度收入、AI200/HUMAIN出货线索、AI250、Alphawave初始出货、Dragonwing 2026-09可用均是近端验证",
            "多数催化仍需从合作/产品发布变成订单、收入、毛利和现金流，不能只按AI数据中心标题定价",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+23.46%、过去一月+41.24%，市场已明显交易数据中心推理和估值修复",
            "2026-06-22收盘较6月3日收盘回落约11%，高IV下若财报不兑现，动量容易反噬",
        ),
        "激进短线": (
            "Call IV 86.2%、Put IV 81.8%，AI200/HUMAIN、Alphawave和汽车/边缘AI提供短线故事密度，价格也已有高关注度",
            "QCOM市值约2340亿美元且手机/QTL底盘成熟，爆发倍数不如小盘光互联、NeoCloud、核电、电力设备或亏损转盈利高beta",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "Handsets移动SoC/Modem-RF",
            "Automotive Snapdragon Digital Chassis",
            "IoT/Edge AI/AI PC/Networking",
            "QTL授权",
            "AI200/AI250数据中心推理",
            "Alphawave高速连接/IP/custom silicon",
        ]

    lines: list[str] = [
        "# QCOM 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：QCOM / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 QCOM vs 公司 B 的二选一判断。未使用下游量化资料、现成排序结论、临时结果、备份结论或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。QCOM 的高胜率主要来自近端催化、风险调整和估值消化：市场已经开始交易 AI200/HUMAIN、Alphawave 和汽车/边缘AI期权，同时当前估值还没有达到AI主链极端倍数；价格确认也强，但会被部分高beta对手分流。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 NTM 收入增速不够高、手机仍是最大收入池、数据中心AI收入未规模披露；面对NVDA/AVGO/MRVL/ALAB/MU/VRT/ETN/POWL等高增长或订单硬标的时，QCOM经常只能胜在估值和现金流，不胜在绝对增长。",
        "- A 最适合的投资者画像：希望持有一个成熟半导体现金流底盘，同时拿汽车、边缘AI、AI200/AI250数据中心推理和Alphawave custom silicon期权的资金；更适合风险调整、估值消化、催化和动量组合，而不是纯AI主链最高增长配置。",
        "- A 最不适合的投资者画像：只追求最高NTM收入增速、最硬AI服务器订单、最高右尾弹性或最强短线小盘爆发力的资金；这些资金通常会转向NVDA/AVGO/MRVL/ALAB/CRDO/AAOI、VRT/ETN/POWL/HUBB或NeoCloud/核电等高beta标的。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在AI主链收入、订单/RPO/backlog、利润池位置、估值消化、下行保护或小基数短线弹性上压过QCOM。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：QCOM 是项目内中上但非顶尖的成熟半导体+AI推理期权标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它明显强于多数弱增长、缺现金流或缺动量公司，但面对AI主链、HBM/网络、数据中心电力设备和部分低估值高FCF公司时需要按投资思路拆分。",
        "- 后续最重要跟踪数据：2026-07-29附近FY26Q3财报与FY26Q4指引；Handsets中国客户收入是否触底回升；QCT margin是否从低谷修复；汽车季度收入与450亿美元design-win pipeline转收入；AI200/HUMAIN是否披露订单金额、rack数、交付窗口、验收和毛利；AI250客户评估；Alphawave/custom silicon初始出货和客户保留；Dragonwing IQ10 2026-09可用后的模块SKU和客户；QTL续约/监管线索。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "QCOM"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or a["scenarios"]["base"].get("NTM 公司收入", "缺失")]),
        base.row(["乐观/极度乐观收入", f"{a.get('bull_rev') or a['scenarios']['bull'].get('NTM 公司收入', '缺失')} / {a.get('extreme_rev') or a['scenarios']['extreme'].get('NTM 公司收入', '缺失')}"]),
        base.row(["利润和现金流结论", f"{a.get('base_profit', '')}；{a.get('base_cash', '')}"]),
        base.row(["最大传导瓶颈", "手机仍是最大收入池，短期受内存供应、成本上涨、中国渠道库存和Android OEM build plan影响；AI200/HUMAIN从战略合作到可确认收入仍缺订单金额、价格、交付和验收证据。"]),
        base.row(["最大反证", "FY26Q3后手机不修复、QCT margin无法回升；AI200停留PoC或HUMAIN交付推迟；Alphawave整合/客户出货滞后；汽车SOP推迟；QTL续约或监管压力升温。"]),
        base.row(["近端催化剂", "FY26Q3财报与FY26Q4指引、AI200/HUMAIN订单或出货披露、AI250客户评估、Alphawave/custom silicon初始出货、Dragonwing IQ10 2026-09可用、汽车收入创新高。"]),
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
        lines.append(base.row([strategy, a["tiers"][strategy], f"第 {rank}/{total}，{a['tiers'][strategy]} 档", support[strategy][0], support[strategy][1]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与QCOM在AI加速器、数据中心推理、custom silicon、Android/边缘AI计算或高端半导体资金池中高度重叠。", "NVDA、AMD、AVGO、MRVL、INTC", "优先比较AI收入兑现、客户锁定、产品代际、生态、毛利率、订单/RPO和同业估值；同业证据差距明显时结论力度上调。"]),
        base.row(["相邻替代", "同属AI半导体、EDA/IP、网络连接、汽车/工业半导体、AI电力或数据中心设备资金篮子，但产品不直接一一替代。", "ARM、ALAB、CDNS、SNPS、ON、TXN、ADI、CRDO、ANET、ETN、VRT、POWL", "回答资金只能买一个时，谁的增长质量、右尾、估值消化、近端催化和风险调整收益更好。"]),
        base.row(["上下游", "B 是QCOM的云客户、服务器/网络/存储链、代工封测、EDA/IP、材料设备或数据中心运营链条伙伴/约束。", "MSFT、GOOGL、META、AMZN、TSM、ASML、AMAT、MU、SMCI、DELL、COHR", "不把云capex、上游设备订单或下游需求直接等同于QCOM收入，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。"]),
        base.row(["跨赛道", "业务差异大，但作为项目资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、DHR、CAT、RKLB、ECL、MSI", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
                    "QCOM" if row_obj["final_choice"] == "A" else row_obj["ticker"] if row_obj["final_choice"] == "B" else "中性",
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
        need = "QCOM需要披露更清晰的AI200/AI250订单、收入、毛利率和多客户复制，同时证明手机恢复、QCT margin和Alphawave收入可兑现。"
        if row_obj["relationship"] == "直接同业":
            need = "QCOM需要在AI推理/custom silicon同业中证明AI200/AI250、Alphawave和汽车/边缘AI收入增速、生态和客户质量强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "QCOM需要证明云厂AI capex、数据中心推理和高速互连需求会落到自己的芯片/IP收入，而不是只停留在下游或上游利润池。"
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
        need = "B需要拿出更硬订单/RPO、更强NTM收入利润兑现，或证明估值、现金流和执行反证低于QCOM。"
        if b.get("scores", {}).get("右尾弹性优先", 0) > a.get("scores", {}).get("右尾弹性优先", 0):
            need = "B需要把右尾叙事转成可确认收入/利润，并证明估值、现金流和执行反证可控。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/AI计算芯片_EDA_IP_custom_ASIC/QCOM_Qualcomm_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未使用备份、临时结果、现成排序或下游量化结论。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；价格缺失或不可用公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI服务器_存储_芯片/行业调研_商用AI加速芯片_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI边缘推理芯片_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_宽带接入、PON、DOCSIS 4.0与Wi-Fi 7_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_EDA工具、接口IP与Chiplet IP_2026-06-11.md`、`行业调研/产业背景/行业调研_头部AI芯片全景与产能释放_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- QCOM 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_qcom_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的使用既有正式脚本的最低分校准，对QCOM的FY26Q2/Q3收入锚、手机/QTL/汽车/IoT底盘、AI200/HUMAIN、AI250、Alphawave、Dragonwing、估值、IV、区间涨跌和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论、临时结果、备份结论或既有公司对比成品。",
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
        raise SystemExit("缺少 QCOM 正式评估文件")
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
                "qcom_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "qcom_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "qcom_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
