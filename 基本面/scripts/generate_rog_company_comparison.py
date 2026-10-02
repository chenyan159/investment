from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_nvt_company_comparison as framework


TARGET = "ROG"
TARGET_NAME = "Rogers Corporation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ROG_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_MATERIALS_EXTRA = {
    "GLW",
    "MMM",
    "MTRN",
    "Q",
}

SEMI_AND_PACKAGE_CHAIN = {
    "ACLS",
    "ACMR",
    "AEHR",
    "AMAT",
    "AMKR",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
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
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "SNPS",
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

AI_NETWORK_SERVER_CHAIN = {
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
    "MRAM",
    "MRVL",
    "MTSI",
    "MU",
    "MXL",
    "NOK",
    "NTAP",
    "NTNX",
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
    "VIAV",
    "VISN",
    "WDC",
}

POWER_ELECTRONICS_CHAIN = {
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
    "ON",
    "POWI",
    "ST",
    "STM",
    "TTDKY",
    "TXN",
    "VICR",
    "VSH",
    "WOLF",
}

DATA_CENTER_CUSTOMERS = {
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
    "ORCL",
}

AI_INFRA_ADJACENT = {
    "AAON",
    "ABBNY",
    "AEIS",
    "AEP",
    "ATKR",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "CMI",
    "DKILY",
    "DTE",
    "EME",
    "ENPH",
    "ENS",
    "ET",
    "ETN",
    "ETR",
    "FCEL",
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
    "PNR",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "TT",
    "VRT",
    "VST",
}

INDUSTRIAL_CROSS = {
    "ALLE",
    "AMPX",
    "CAT",
    "DCI",
    "DHR",
    "DOV",
    "ECL",
    "FTV",
    "IESC",
    "MSI",
    "NDSN",
    "PH",
    "RKLB",
    "TDY",
    "TMO",
    "TSLA",
}

ROG_SCORES = {
    "NTM兑现优先": 64.0,
    "右尾弹性优先": 65.0,
    "风险调整收益": 43.5,
    "下行保护优先": 58.0,
    "估值消化优先": 50.0,
    "近端催化优先": 62.5,
    "价格确认/动量": 67.0,
    "激进短线": 84.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    framework.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in ROG_SCORES.items():
        target.setdefault("scores", {})[strategy] = score
    framework.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if category == "半导体材料_化学品_基板" or ticker in DIRECT_MATERIALS_EXTRA:
        return "直接同业"
    if ticker in SEMI_AND_PACKAGE_CHAIN or ticker in AI_NETWORK_SERVER_CHAIN or ticker in POWER_ELECTRONICS_CHAIN:
        return "上下游"
    if ticker in DATA_CENTER_CUSTOMERS:
        return "上下游"
    if ticker in AI_INFRA_ADJACENT or category in INFRA_CATS:
        return "相邻替代"
    if category in {
        "AI计算芯片_EDA_IP_custom_ASIC",
        "AI网络_光互联_连接器",
        "AI服务器_存储_EMS",
        "云算力_IDC_AI软件平台",
        "晶圆制造_前道设备",
        "封测_检测_计量_光罩",
        "配电_电源_功率器件",
    }:
        return "上下游"
    if ticker in INDUSTRIAL_CROSS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "直接同业":
            return "材料同业证据互有强弱"
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近且收入链条差异大"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "ROG有Q2指引、分部收入和成本削减锚",
            "右尾弹性优先": "ROG高频板材、ADAS、curamik和热材料期权多",
            "风险调整收益": "ROG小市值、P/S较低且利润修复有弹性",
            "下行保护优先": "ROG低杠杆、正FCF和EMS现金流支撑",
            "估值消化优先": "ROG估值可由EBITDA和FCF修复消化",
            "近端催化优先": "ROG Q2/Q3、E&C、curamik和ADAS验证更近",
            "价格确认/动量": "ROG 6月价格确认和IV关注度较强",
            "激进短线": "ROG小市值叠加AI材料和高频板材期权",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}材料收入、客户或订单证据更硬",
            "右尾弹性优先": f"{ticker}材料右尾或AI份额更直接",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业业绩更能覆盖估值",
            "近端催化优先": f"{ticker}同业订单/认证催化更近",
            "价格确认/动量": f"{ticker}同业价格趋势更强",
            "激进短线": f"{ticker}同业主题beta或波动更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}收入/RPO或交付确认链更短",
            "右尾弹性优先": f"{ticker}AI主链或瓶颈利润池更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流、规模或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}AI关注度和高beta更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}订单/backlog或交付更清楚",
            "右尾弹性优先": f"{ticker}AI设施利润池更直接",
            "风险调整收益": f"{ticker}增长与估值组合更优",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}订单兑现更能消化估值",
            "近端催化优先": f"{ticker}近端订单或产能催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}AI链收入兑现证据更硬",
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
        return "ROG的材料期权与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "ROG有Q2收入/毛利/EBITDA指引、分部run-rate和成本削减支撑NTM温和兑现。"
        if diffs["右尾弹性优先"] > 12:
            return "ROG小市值叠加高速板材、AI热材料、curamik电力材料和ADAS高频材料多条期权。"
        if diffs["估值消化优先"] > 10:
            return "ROG的P/S约3.6倍、市值约30亿美元，若EBITDA和FCF修复兑现更容易消化。"
        if diffs["下行保护优先"] > 10:
            return "ROG低杠杆、正FCF和EMS高毛利底盘比对手更能承受需求波动。"
        if diffs["价格确认/动量"] > 12:
            return "ROG 6月价格确认和58% Call IV显示资金已开始交易材料修复和AI期权。"
        return "ROG在可验证修复、小市值右尾、估值和近端验证之间的组合略优。"

    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或收入兑现比ROG更硬。"
    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于ROG。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于ROG。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或压力期表现比ROG更安全。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或估值组合比ROG更容易消化。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比ROG更直接。"
    if diffs["激进短线"] < -12:
        return f"{ticker}短线高beta、AI叙事或价格爆发力强于ROG。"
    return f"{ticker}在多数投资思路下比ROG更符合项目内资金配置目标。"


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
    call_iv_text = f"{fmt_num(fin.get('call_iv'), 1)}%" if fin.get("call_iv") is not None else "缺失"
    put_iv_text = f"{fmt_num(fin.get('put_iv'), 1)}%" if fin.get("put_iv") is not None else "缺失"
    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {call_iv_text}，"
        f"Put IV {put_iv_text}；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
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
            "2026Q1收入200.5M、同比+5.2%；Q2指引210M-220M，中点215M；NTM基准865M-910M，毛利率32.5%-34.0%，Adj. EBITDA 145M-165M",
            "不披露正式backlog/bookings，多数收入来自短PO，客户可重排/取消；基准增长只有+5%-11%，不是全项目高兑现顶档",
        ),
        "右尾弹性优先": (
            "乐观/极度乐观收入940M-1.02B/1.08B-1.22B；高速/RF低损耗板材、ADAS radar、curamik/ROLINX/cooling、EMS热/密封材料同时有AI、EV和工业期权",
            "直接AI data center基准收入只按20M-50M处理，缺少LTA、客户名、订单金额、BOM份额和交付窗口",
        ),
        "风险调整收益": (
            "2026-06-22市值约2.97B、P/S 3.62，若EBITDA和FCF修复兑现，小市值有弹性；EMS毛利率和成本削减提供利润杠杆",
            "Forward PE 38.13、TTM EPS为负、SOXX压力窗口累计-48.20%，且无backlog降低风险调整后的确定性",
        ),
        "下行保护优先": (
            "资产负债表和正FCF方向较好，基准FCF45M-80M、CapEx30M-40M可承受，EMS高毛利业务为现金流底盘",
            "SOXX压力窗口回撤大，TTM EPS为负；短PO、curamik impairment后续、汽车/中国本土替代和PFAS/原料风险削弱防守性",
        ),
        "估值消化优先": (
            "P/S 3.62、EV/EBITDA 23.04；若NTM Adj. EBITDA 145M-165M和净利润45M-70M兑现，估值有一部分可消化",
            "Forward PE 38.13对应的收入增速只有中个位数到低双位数，AI data center未单列，估值消化依赖连续毛利修复",
        ),
        "近端催化优先": (
            "Q2/Q3收入、GM、Adj. EBITDA、E&C占比、curamik China qualification、RO4830 Plus/RO3003G2 design win、EMS热材料项目均有近端验证价值",
            "催化多为验证修复而非已披露大订单；AI高频板材、热材料和电力材料仍缺客户项目金额",
        ),
        "价格确认/动量": (
            "2026-06-03两周+11.28%、一月+10.09%，2026-06-22收盘较2026-06-03再上涨约12.51%，Call IV 58.0%显示资金关注度提升",
            "上涨来自修复和AI材料期权重估，若Q2/Q3没有订单/指引跟进，动量可能快速回吐",
        ),
        "激进短线": (
            "市值约2.97B、Call IV 58.0%，高速低损耗材料、AI thermal、curamik电力材料和ADAS radar可形成短线故事密度",
            "关注度和订单强度仍弱于光互联、AI芯片、NeoCloud、核电和电力设备高beta标的，且Put IV缺失降低期权读数完整性",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "高速/RF/低损耗电路材料",
            "ADAS/mmWave radar材料",
            "curamik ceramic substrates / ROLINX / cooling",
            "EMS高性能弹性/热/密封/减振材料",
            "Other/低权重传统业务",
        ]

    lines: list[str] = [
        "# ROG 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：ROG / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 ROG vs 公司 B 的二选一判断。未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 作为决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ROG 的相对优势主要在右尾弹性、NTM温和兑现和价格确认：市值小，6月价格已有确认，且高速/RF低损耗材料、ADAS radar、curamik电力材料和EMS热/密封材料同时具备AI、汽车与工业修复期权。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板集中在风险调整、下行保护和估值消化：2026-06-22 Forward PE 38.13、TTM EPS为负、SOXX压力窗口累计-48.20%，而NTM基准收入仅865M-910M且公司不披露backlog/bookings。",
        "- A 最适合的投资者画像：愿意买小市值材料修复和AI/ADAS/电力材料期权、接受订单披露不足和较高估值、重点跟踪Q2/Q3毛利与E&C/curamik/EMS验证的成长/事件型资金。",
        "- A 最不适合的投资者画像：只买最硬订单/RPO/backlog、最高NTM收入增速、最强AI主链或强防守现金流的资金；这些资金通常会更偏向AI芯片/光互联/服务器、数据中心电力设备、成熟现金流工业或公用事业公司。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在订单硬度、AI主链收入、利润池位置、估值消化、下行保护或更高短线beta上压过ROG。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：ROG 是项目内中游偏主题弹性的材料修复标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它能压过部分低成长、缺动量或估值更难消化的公司，但面对AI主链、电力设备、存储/网络和高现金流防守公司时经常要让位。",
        "- 后续最重要跟踪数据：Q2/Q3 2026收入、GM、Adj. EBITDA、E&C占比；是否披露wired infrastructure/data center客户、LTA或订单金额；RO4830 Plus/RO3003G2 design win；curamik China qualification；EMS optical module/rack thermal项目；PFAS/原料供应、中国本土替代、短PO取消/重排和营运资本。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ROG"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or a["scenarios"]["base"].get("NTM 公司收入", "缺失")]),
        base.row(["乐观/极度乐观收入", f"{a.get('bull_rev') or a['scenarios']['bull'].get('NTM 公司收入', '缺失')} / {a.get('extreme_rev') or a['scenarios']['extreme'].get('NTM 公司收入', '缺失')}"]),
        base.row(["利润和现金流结论", f"{a.get('base_profit', '')}；{a.get('base_cash', '')}"]),
        base.row(["最大传导瓶颈", "不披露正式backlog/bookings，短PO可取消或重排；行业AI高速互联、TIM、800VDC和数据中心capex必须先通过客户认证、设计导入和收入确认，不能直接映射为ROG收入。"]),
        base.row(["最大反证", "2026-06-22 Forward PE 38.13、TTM EPS为负、SOXX压力窗口累计-48.20%；2025 curamik impairment、AI data center未单列、客户/LTA/订单金额缺失。"]),
        base.row(["近端催化剂", "Q2/Q3收入、GM、Adj. EBITDA；E&C/wired infrastructure恢复；curamik China qualification；RO4830 Plus/RO3003G2 design win；EMS optical/rack thermal项目；是否披露data center材料客户。"]),
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
        rank_text = f"第 {rank}/{total}，{a['tiers'][strategy]} 档" if rank else f"{a['tiers'][strategy]} 档"
        lines.append(base.row([strategy, a["tiers"][strategy], rank_text, support[strategy][0], support[strategy][1]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "同属半导体材料、化学品、基板、功能材料、高频/低损耗板材、陶瓷/热/特种材料资金池；优先比较客户认证、份额、材料粘性、利润率、估值和收入兑现。", "Q、DD、SHECY、ASGLY、AJNMY、MTRN、GLW、MMM", "同业证据更硬时允许建议或强烈建议；不能只因ROG有AI材料期权就压过已披露收入/订单更硬的材料公司。"]),
        base.row(["相邻替代", "数据中心电力、配电、冷却、工程和工业AI基础设施等资金替代篮子；比较增长质量、订单/backlog、估值消化和近端催化。", "ETN、VRT、NVT、POWL、PWR、MOD、JCI、CEG", "默认降低结论力度；只有订单、估值或右尾明显拉开才使用建议以上标签。"]),
        base.row(["上下游", "AI芯片、服务器、光互联、封测/前道设备、晶圆制造、云/IDC客户和功率半导体等需求链/供应链关系；重点看利润池位置、议价权和收入确认链条。", "NVDA、AVGO、AMD、MU、ANET、COHR、SMCI、TSM、AMAT、MSFT", "不把下游AI capex或上游设备订单直接等同于ROG收入；若B的订单/RPO/收入链条更短，通常优先B。"]),
        base.row(["跨赛道", "业务差异大，但作为项目资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "TMO、DHR、CAT、RKLB、TSLA、MSI", "默认使用中性或微倾向；只有档位差明显时才升级。"]),
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
                    "ROG" if row_obj["final_choice"] == "A" else row_obj["ticker"] if row_obj["final_choice"] == "B" else "中性",
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
        need = "ROG需要披露更硬的data center/ADAS/curamik/EMS客户订单、收入拆分、毛利率和交付窗口，并证明估值、现金流和短PO风险可控。"
        if row_obj["relationship"] == "直接同业":
            need = "ROG需要在材料同业中证明低损耗板材、ADAS radar、curamik或EMS热材料的客户份额、订单金额、毛利和收入增速强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "ROG需要证明AI高速互联、电力和热材料需求会落到自身BOM和收入，而不是主要被B所在的芯片、网络、服务器、设备或云客户环节捕获。"
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
        need = "B需要拿出更硬订单/RPO、更强NTM收入利润兑现，或证明估值、现金流和执行反证低于ROG。"
        if b.get("scores", {}).get("右尾弹性优先", 0) > a.get("scores", {}).get("右尾弹性优先", 0):
            need = "B需要把右尾叙事转成可确认收入/利润，并证明估值、现金流和执行反证可控。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/ROG_Rogers_Corporation_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未使用备份、临时结果、现成排序或下游量化结论。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；价格缺失或不可用公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AEC、DAC与高速铜缆_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_高速连接器、背板与结构化布线_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_先进封装材料与热界面材料_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_硅光材料、光子材料与电光聚合物_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- ROG 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_rog_company_comparison.py`。脚本读取正式公司评估与金融资料，基于全项目统一档位阈值建档；对ROG按2026Q1/Q2指引、NTM收入区间、利润/FCF修复、无backlog、AI材料收入未单列、估值、IV、区间涨跌和SOXX压力窗口做目标公司校准；未读取 `特征量化/`。",
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
        raise SystemExit("缺少 ROG 正式评估文件")
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
                "rog_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "rog_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "rog_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
