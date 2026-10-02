from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_nvt_company_comparison as framework


TARGET = "SITM"
TARGET_NAME = "SiTime Corporation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "SITM_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_TIMING_PEERS = {
    "ADI",
    "DIOD",
    "IFNNY",
    "MCHP",
    "STM",
    "TXN",
}

AI_NETWORK_ADJACENT = {
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
    "AVGO",
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
    "MRVL",
    "MTSI",
    "MXL",
    "NOK",
    "POET",
    "RMBS",
    "SIMO",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}

AI_COMPUTE_AND_CLOUD_CHAIN = {
    "ADBE",
    "AMD",
    "AMZN",
    "APLD",
    "ARM",
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
    "NVDA",
    "ORCL",
    "PENG",
    "QCOM",
    "SMCI",
    "TSLA",
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
    "PSTG",
    "SANM",
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
    "CDNS",
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
    "MRAAY",
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
    "TTDKY",
    "UCTT",
    "UMC",
    "VECO",
}

DATA_CENTER_INFRA_ADJACENT = {
    "AAON",
    "ABBNY",
    "AEIS",
    "AEP",
    "AMPX",
    "APD",
    "ATKR",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "CMI",
    "DKILY",
    "DTE",
    "EME",
    "ENS",
    "ET",
    "ETN",
    "ETR",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "NVT",
    "OKLO",
    "PH",
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
    "AOSL",
    "APD",
    "CAT",
    "CC",
    "DCI",
    "DD",
    "DHR",
    "DOV",
    "ECL",
    "ENPH",
    "FCEL",
    "FTV",
    "LFUS",
    "MIELY",
    "MMM",
    "MPWR",
    "MSI",
    "MTRN",
    "NDSN",
    "NVTS",
    "ON",
    "PNR",
    "POWI",
    "RKLB",
    "ST",
    "TDY",
    "TMO",
    "VICR",
    "VSH",
    "WOLF",
}

SITM_SCORES = {
    # Manual calibration fixes the generic parser's inability to treat Chinese
    # "亿美元" revenue ranges as USD hundreds of millions. The target score is
    # anchored to SITM's formal evaluation and daily market files, not to ranking
    # outputs or downstream quant folders.
    "NTM兑现优先": 78.0,
    "右尾弹性优先": 86.0,
    "风险调整收益": 38.0,
    "下行保护优先": 42.0,
    "估值消化优先": 35.0,
    "近端催化优先": 77.0,
    "价格确认/动量": 75.0,
    "激进短线": 88.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    framework.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in SITM_SCORES.items():
        target.setdefault("scores", {})[strategy] = score  # type: ignore[index]
    framework.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_TIMING_PEERS:
        return "直接同业"
    if ticker in AI_NETWORK_ADJACENT:
        return "相邻替代"
    if ticker in AI_COMPUTE_AND_CLOUD_CHAIN or ticker in SERVER_STORAGE_CHAIN or ticker in FOUNDRY_EQUIPMENT_MATERIALS_CHAIN:
        return "上下游"
    if ticker in DATA_CENTER_INFRA_ADJACENT or category in INFRA_CATS:
        return "相邻替代"
    if category in {"AI网络_光互联_连接器"}:
        return "相邻替代"
    if category in {"AI计算芯片_EDA_IP_custom_ASIC", "AI服务器_存储_EMS", "云算力_IDC_AI软件平台", "晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if ticker in INDUSTRIAL_CROSS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict[str, object], rel: str) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "直接同业":
            return "timing证据互有强弱"
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，增长和估值互抵"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "SITM Q1/Q2指引和CED高增更硬",
            "右尾弹性优先": "AI timing、Elite 2和Renesas右尾更纯",
            "风险调整收益": "SITM成长弹性可覆盖部分高估值",
            "下行保护优先": "SITM现金和高毛利略优于高风险B",
            "估值消化优先": "SITM高增速相对B更能消化",
            "近端催化优先": "Q2/Q3、Elite 2和Renesas节点更近",
            "价格确认/动量": "SITM近月价格确认更强",
            "激进短线": "SITM高IV和AI timing叙事更适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单/分部收入更硬",
            "右尾弹性优先": f"{ticker}同业产品池或客户右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流和估值缓冲更厚",
            "估值消化优先": f"{ticker}同业估值更易被业绩消化",
            "近端催化优先": f"{ticker}同业产品/财报催化更明确",
            "价格确认/动量": f"{ticker}同业价格趋势更强",
            "激进短线": f"{ticker}同业短线资金偏好更强",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}订单/RPO或收入确认链更硬",
            "右尾弹性优先": f"{ticker}AI主链美元右尾更大",
            "风险调整收益": f"{ticker}上行下行组合更优",
            "下行保护优先": f"{ticker}现金流或规模护城河更稳",
            "估值消化优先": f"{ticker}业绩规模更能覆盖估值",
            "近端催化优先": f"{ticker}订单/产品/财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}AI beta和流动性更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}收入、订单或交付更清楚",
            "右尾弹性优先": f"{ticker}右尾利润池更直接",
            "风险调整收益": f"{ticker}增长与估值组合更优",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}订单兑现更能消化估值",
            "近端催化优先": f"{ticker}近端订单或产品催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}AI链兑现证据更硬",
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


def label_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
    bt = b.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))  # type: ignore[union-attr]
    tier_gap = tier_value(str(at)) - tier_value(str(bt))
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


def cell_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    return f"{label}：{reason_for(strategy, label, b, rel)}"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def direction_counts(row_obj: dict[str, object]) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in str(row_obj[strategy]))
    b_count = sum(1 for strategy in STRATS if "投B" in str(row_obj[strategy]))
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict[str, object]) -> str:
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
        score += weights[strategy] * label_score.get(tag_in_cell(str(row_obj[strategy])) or "中性", 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict[str, object], b: dict[str, object], row_obj: dict[str, object], choice: str) -> str:
    ticker = str(b["ticker"])
    if choice == "中性":
        return "SITM的AI timing高弹性与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {
        strategy: float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))  # type: ignore[union-attr]
        for strategy in STRATS
    }
    if choice == "A":
        if diffs["右尾弹性优先"] > 13:
            return "SITM的AI精密时钟、Elite 2/TimeFabric和Renesas并购带来更纯右尾。"
        if diffs["NTM兑现优先"] > 10:
            return "SITM有Q1/Q2指引、CED高增和FY2026 standalone至少+80%的收入锚。"
        if diffs["近端催化优先"] > 10:
            return "SITM未来两个季度有Q2/Q3、Elite 2量产和Renesas交割进展验证。"
        if diffs["激进短线"] > 10:
            return "SITM高IV、高AI timing关注度和短期事件密度更适合进攻。"
        return "SITM在AI timing成长、催化和短线弹性上的组合略优。"

    if diffs["估值消化优先"] < -12:
        return f"{ticker}的当前估值更容易被NTM业绩覆盖，SITM估值压力更重。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、资产质量或压力期表现比SITM更安全。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的上行和下行组合优于高估值高波动的SITM。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或收入确认比SITM更硬。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker}价格确认和资金趋势强于SITM。"
    if diffs["激进短线"] < -12:
        return f"{ticker}短线爆发力或AI资金偏好强于SITM。"
    return f"{ticker}在多数投资思路下比SITM更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong = []
    b_strong = []
    close = []
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
    for strategy in STRATS:
        at = a.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
        bt = b.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
        diff = tier_value(str(at)) - tier_value(str(bt))
        if diff >= 1:
            a_strong.append(short[strategy])
        elif diff <= -1:
            b_strong.append(short[strategy])
        else:
            close.append(short[strategy])
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:4]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:4]))
    if close:
        parts.append("接近:" + "、".join(close[:3]))
    return "；".join(parts) if parts else "档位接近"


def comparison_sort_key(row_obj: dict[str, object]) -> tuple[int, str, str]:
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return (rel_order.get(str(row_obj["relationship"]), 9), str(row_obj["classification"]), str(row_obj["ticker"]))


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    rows: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj: dict[str, object] = {
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
        row_obj["key_reason"] = key_reason(a, b, row_obj, str(row_obj["final_choice"]))
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


def majority_rows(rows: list[dict[str, object]], final: str, limit: int = 45) -> list[dict[str, object]]:
    if final == "B":
        selected = [row for row in rows if int(row["bc"]) >= 5 and int(row["bc"]) - int(row["ac"]) >= 3]
        selected.sort(key=lambda row: (int(row["bc"]) - int(row["ac"]), int(row["bc"]), -int(row["nc"])), reverse=True)
    elif final == "A":
        selected = [row for row in rows if int(row["ac"]) >= 5 and int(row["ac"]) - int(row["bc"]) >= 3]
        selected.sort(key=lambda row: (int(row["ac"]) - int(row["bc"]), int(row["ac"]), -int(row["nc"])), reverse=True)
    else:
        selected = [row for row in rows if row["final_choice"] == final]
    return selected[:limit]


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({str(company["date"]) for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin")])
    missing_price = sorted([ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price")])  # type: ignore[union-attr]
    fin = a.get("fin", {})  # type: ignore[assignment]
    m2w = a.get("mom2", {})  # type: ignore[assignment]
    m1m = a.get("mom1", {})  # type: ignore[assignment]
    soxx = a.get("soxx", {})  # type: ignore[assignment]

    price_from_0603 = None
    if fin.get("price") and m2w.get("latest_close"):
        price_from_0603 = ((float(fin.get("price")) / float(m2w.get("latest_close"))) - 1) * 100
    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE 不适用，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去一月 {fmt_pct(m1m.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}；"
        f"2026-06-22收盘较2026-06-03收盘 {fmt_pct(price_from_0603)}。"
    )

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][tag_in_cell(str(row_obj[strategy]))] += 1

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
            "2026Q1收入1.136亿美元、同比+88.3%；Q2收入指引1.40-1.50亿美元；管理层称2026 standalone至少同比+80%，NTM主窗口收入锚约6.5-7.2亿美元",
            "公司缺少按产品披露的backlog/RPO/客户订单；Q3库存pause、客户拉货节奏和产品拆分不透明会限制强判",
        ),
        "右尾弹性优先": (
            "CED精密时钟、AI网络/800G/1.6T/PCIe timing、Elite 2/TimeFabric和Renesas timing business共同提供高毛利小BOM右尾",
            "AI timing价值量小且可能被NIC/switch/ASIC内化；Renesas未交割，Elite 2仍需从样品和Q3商业生产转成收入",
        ),
        "风险调整收益": (
            "收入增速、non-GAAP毛利率、交易前现金和AI timing纯度支撑上行，且2026-06-22价格仍较2026-06-03收盘高约5.66%",
            "2026-06-22 P/S 52.33、Forward PE 69.64、Call IV 84.4%，SOXX压力窗口累计-69.69%，高估值高波动显著压低风险调整收益",
        ),
        "下行保护优先": (
            "交易前现金和短投充足，Q1经营现金流/自由现金流为正，高端timing毛利率较强",
            "股价对AI timing平台成功定价很满，压力期历史回撤大；Renesas现金对价、可转债、客户集中和GAAP亏损削弱防守性",
        ),
        "估值消化优先": (
            "若NTM standalone收入6.5-7.2亿美元、non-GAAP经营利润率30%-34%兑现，估值压力可部分消化",
            "当前市值约198.8亿美元，对NTM基准收入仍约28-31倍销售额，任何CED放缓、Elite 2延迟或Renesas整合噪音都会放大估值反噬",
        ),
        "近端催化优先": (
            "2026Q2实际收入与Q3指引、CED end-market收入、Elite 2 2026Q3商业生产、TimeFabric商业化线索和Renesas交割进度均在1-2个季度内可验证",
            "多数催化要转成订单、客户、收入和毛利；仅有产品发布或交易公告不足以支撑基准强上修",
        ),
        "价格确认/动量": (
            "2026-06-03过去一月+27.59%，2026-06-22收盘753.12美元较6月3日仍上涨约5.66%，AI timing叙事有价格确认",
            "过去两周至6月3日仅+2.26%，IV超过80%，且高估值下任何订单/指引失望都会导致趋势快速反转",
        ),
        "激进短线": (
            "高IV、高关注度、AI timing纯标的、Elite 2/Q2Q3/Renesas事件密度使SITM适合更激进进攻",
            "短线赔率被高估值和高IV挤压，若市场转向防守或AI硬件拥挤交易降温，SITM会比现金流稳定资产更脆弱",
        ),
    }

    lines: list[str] = [
        "# SITM 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：SITM / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 SITM vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`；未使用现成排序结论、临时结果、备份结论或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。SITM 最强的是右尾、近端催化和激进短线：它是AI数据中心精密时钟纯度最高的项目内标的之一，Q2/Q3、Elite 2/TimeFabric和Renesas交易提供清晰事件密度。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是高估值、高IV、压力期回撤和产品级订单/RPO披露不足；面对低估值现金流、硬订单电力设备、AI主链龙头和大型平台公司时，风险调整、下行保护和估值消化经常输。",
        "- A 最适合的投资者画像：愿意用高波动承接AI timing小BOM高系统杠杆、Elite 2/TimeFabric从0到1和Renesas并表右尾的进攻型资金。",
        "- A 最不适合的投资者画像：要求估值已经便宜、现金流防守强、订单/backlog完全透明或只买最大AI美元收入池的资金。",
        f"- 多数思路下最强反方公司：{strong_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：SITM 对 {final_a}/{len(comparisons)} 家公司多数思路占优，对 {final_b}/{len(comparisons)} 家公司多数思路落后，中性 {final_neutral} 家；它不是全项目综合最稳配置，但在AI网络精密时钟右尾和短线催化画像中有清晰稀缺性。",
        "- 后续最重要跟踪数据：2026Q2实际收入和Q3指引；CED收入、客户集中度、订单可见度和book-to-bill；Elite 2商业生产和首批客户收入；TimeFabric是否独立收费或进入参考设计；Renesas交割时间、客户留存、毛利率和整合成本；非GAAP毛利率、GAAP利润、库存、应收、经营现金流、自由现金流和可转债稀释。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "SITM"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "")]),
        base.row(["重要产品/业务线", "CED精密时钟；AI网络/800G/1.6T/PCIe低抖动timing；Elite 2 Super-TCXO；TimeFabric/集群同步；AIA高可靠timing；Mobile/IoT/Consumer timing；Renesas timing business待交割补充口径"]),
        base.row(["NTM 基准收入", a.get("base_rev") or "6.5-7.2 亿美元"]),
        base.row(["乐观/极度乐观收入", f"{a.get('bull_rev') or '7.6-8.6 亿美元'} / {a.get('extreme_rev') or '8.5-10.5 亿美元'}"]),
        base.row(["利润和现金流结论", "基准下非GAAP毛利率约63%-66%，经营利润率约30%-34%，非GAAP净利润约2.1-2.6亿美元；自由现金流正向但受库存、应收、Renesas现金支出和整合营运资本影响。"]),
        base.row(["最大传导瓶颈", "AI集群同步、PCIe/SerDes、800G/1.6T和光互联低抖动需求不等于SITM可确认收入；公司缺少按产品披露的backlog/RPO/客户订单。"]),
        base.row(["最大反证", "CED增长低于Q2/H2隐含路径、Q3库存pause、Elite 2只停留样品、Renesas交割或客户迁移延迟、客户或ASIC/NIC/switch厂商内化timing功能。"]),
        base.row(["近端催化剂", "2026Q2实际收入与Q3指引、CED end-market收入、Elite 2 2026Q3商业生产、TimeFabric商业化线索、Renesas交割和整合成本披露。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        rank = a.get("ranks", {}).get(strategy)  # type: ignore[union-attr]
        total = a.get("rank_total", {}).get(strategy) or len(companies)  # type: ignore[union-attr]
        lines.append(base.row([strategy, a.get("tiers", {}).get(strategy), f"第 {rank}/{total}，{a.get('tiers', {}).get(strategy)} 档", support[strategy][0], support[strategy][1]]))  # type: ignore[union-attr]

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与SITM在clock/timing、DPLL、network synchronizer、低抖动参考时钟、MEMS/模拟混合信号或服务器/数据中心timing socket上高度重叠。", "MCHP、TXN、ADI、STM、DIOD、IFNNY", "优先比较产品级收入、订单/客户、毛利率、socket粘性和同业估值；同业证据差距明显时结论力度上调。"]),
        base.row(["相邻替代", "同属AI网络、光互联、连接、retimer/DSP、AI fabric或数据中心电力/冷却资金篮子，但产品不直接一一替代。", "ALAB、CRDO、MRVL、MTSI、MXL、SMTC、COHR、ANET、VRT、ETN、POWL", "回答资金只能买一个时，谁的增长质量、右尾、估值消化、近端催化和风险调整收益更好。"]),
        base.row(["上下游", "B是SITM的AI算力需求端、服务器/网络/存储链、代工封测、EDA/IP、设备材料或云平台客户/约束。", "NVDA、AMD、MSFT、GOOGL、META、TSM、ASML、AMAT、MU、SMCI", "不把AI capex或上游设备订单直接等同于SITM收入，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。"]),
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
                    "SITM" if row_obj["final_choice"] == "A" else row_obj["ticker"] if row_obj["final_choice"] == "B" else "中性",
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
        wins = [strategy for strategy in STRATS if "投B" in str(row_obj[strategy])]
        need = "SITM需要披露更清晰的AI timing客户、订单/backlog、Elite 2收入、Renesas交割和毛利/现金流证据，同时证明高估值可由业绩消化。"
        if row_obj["relationship"] == "直接同业":
            need = "SITM需要在timing同业中证明CED/Elite 2/TimeFabric/Renesas收入、客户质量和毛利率强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "SITM需要证明AI capex、服务器、网络和云厂架构升级会落到自己的外部timing socket，而不是被下游系统或上游芯片内化。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_a, start=1):
        wins = [strategy for strategy in STRATS if "投A" in str(row_obj[strategy])]
        need = "B需要拿出更硬订单/RPO、更强NTM收入利润兑现，或证明估值、现金流和执行反证低于SITM。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(str(a['path'])).name}`。",
        "- 公司 A 公司调研文件：`公司调研/AI网络_光互联_连接器/SITM_SiTime Corporation_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取、引用或继承 `特征量化/`，未使用备份、临时结果或现成排序结论。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；价格缺失或不可用公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI服务器_存储_芯片/行业调研_精密时钟与同步芯片_2026-06-10.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_PCIe_CXL高速IO交换与Retimer_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- SITM 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_sitm_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的使用既有正式脚本的最低分校准，对SITM的Q1/Q2收入锚、CED高增、FY2026 standalone至少+80%、Elite 2/TimeFabric、Renesas交易、估值、IV、区间涨跌和SOXX压力窗口做目标公司校准后建档；未读取、引用或继承 `特征量化/`，未使用现成排序结论、临时结果、备份结论或既有公司对比成品。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        lines.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{Path(str(company['path'])).name}`"]))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 SITM 正式评估文件")
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
                "sitm_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
                "sitm_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},  # type: ignore[union-attr]
                "sitm_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
