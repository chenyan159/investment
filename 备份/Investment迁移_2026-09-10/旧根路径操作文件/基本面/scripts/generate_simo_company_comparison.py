from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_nvt_company_comparison as framework


TARGET = "SIMO"
TARGET_NAME = "Silicon Motion Technology"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "SIMO_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_STORAGE_SILICON_PEERS = {
    "RMBS",
    "MRAM",
    "MXL",
}

STORAGE_MEMORY_VALUE_CHAIN = {
    "CLS",
    "DELL",
    "FLEX",
    "FN",
    "HPE",
    "JBL",
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

AI_COMPUTE_AND_CLOUD_CHAIN = {
    "ADBE",
    "AMD",
    "AMZN",
    "APLD",
    "ARM",
    "AVGO",
    "BABA",
    "CRWD",
    "CRWV",
    "DLR",
    "EQIX",
    "GOOGL",
    "IBM",
    "INTC",
    "IREN",
    "META",
    "MRVL",
    "MSFT",
    "NBIS",
    "NTNX",
    "NVDA",
    "ORCL",
    "QCOM",
}

AI_NETWORK_AND_IO_ADJACENT = {
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}

SEMI_MANUFACTURING_CHAIN = {
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
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SOMMY",
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

AI_INFRA_ADJACENT = {
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

ANALOG_EDGE_ADJACENT = {
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

INDUSTRIAL_CROSS = {
    "AJNMY",
    "ALLE",
    "CAT",
    "CC",
    "DCI",
    "DD",
    "DHR",
    "DOV",
    "DTE",
    "ECL",
    "ENPH",
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

SIMO_SCORES = {
    "NTM兑现优先": 86.0,
    "右尾弹性优先": 96.0,
    "风险调整收益": 57.0,
    "下行保护优先": 37.0,
    "估值消化优先": 62.0,
    "近端催化优先": 88.0,
    "价格确认/动量": 91.0,
    "激进短线": 97.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    framework.score_companies(companies)
    if TARGET not in companies:
        raise SystemExit("缺少 SIMO 正式评估文件")

    for strategy, score in SIMO_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    framework.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_STORAGE_SILICON_PEERS:
        return "直接同业"
    if ticker in STORAGE_MEMORY_VALUE_CHAIN or ticker in AI_COMPUTE_AND_CLOUD_CHAIN or ticker in SEMI_MANUFACTURING_CHAIN:
        return "上下游"
    if ticker in AI_NETWORK_AND_IO_ADJACENT or ticker in AI_INFRA_ADJACENT or ticker in ANALOG_EDGE_ADJACENT:
        return "相邻替代"
    if category == "AI服务器_存储_EMS":
        return "上下游"
    if category in {"AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器"}:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    if ticker in INDUSTRIAL_CROSS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "直接同业":
            return "存储硅片证据互有强弱"
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "增长、估值和防守互抵"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "SIMO有Q1/Q2指引和H2 CSP ramp硬锚",
            "右尾弹性优先": "SIMO有MonTitan/SM8008/ICMS小基数右尾",
            "风险调整收益": "SIMO高增速可补偿部分估值风险",
            "下行保护优先": "SIMO净现金且B防守反证更重",
            "估值消化优先": "SIMO收入高增和利润杠杆更能消化估值",
            "近端催化优先": "SIMO有Q2/Q3和5家CSP ramp验证",
            "价格确认/动量": "SIMO近月价格确认明显更强",
            "激进短线": "SIMO高IV叠加AI存储右尾更适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入或订单兑现更硬",
            "右尾弹性优先": f"{ticker}同业右尾或规模更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业估值消化压力更低",
            "近端催化优先": f"{ticker}同业产品或订单催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业短线关注度更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}收入、RPO或供应链兑现更短链",
            "右尾弹性优先": f"{ticker}AI存储/算力利润池更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流、规模或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速或倍数组合更易消化",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}AI beta或事件弹性更适合短攻",
        }[strategy]

    if rel == "相邻替代" or category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}订单或收入兑现证据更清楚",
            "右尾弹性优先": f"{ticker}右尾规模或份额弹性更直接",
            "风险调整收益": f"{ticker}增长和估值组合更好",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}未来业绩更能覆盖估值",
            "近端催化优先": f"{ticker}近端订单或产品节点更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
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
        return "SIMO的AI存储右尾与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["右尾弹性优先"] > 12:
            return "SIMO的MonTitan、SM8008、ICMS/CMX和小基数收入上修弹性更大。"
        if diffs["NTM兑现优先"] > 10:
            return "SIMO有2026Q1/Q2高run-rate、Q2量产和H2五家CSP ramp支撑NTM兑现。"
        if diffs["近端催化优先"] > 10:
            return "SIMO未来1-2个季度的Q2实绩、Q3指引和CSP/SKU披露节点更密集。"
        if diffs["价格确认/动量"] > 12:
            return "SIMO近期价格确认和AI存储重估动能明显更强。"
        if diffs["估值消化优先"] > 10:
            return "SIMO的收入高增和利润率上行路径比对手更能消化估值。"
        return "SIMO在AI存储右尾、近端验证和收入兑现之间的组合更适合进攻配置。"

    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或压力期韧性明显强于高波动的SIMO。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于SIMO。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或当前倍数比SIMO更容易消化。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或收入确认比SIMO更硬。"
    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的AI主链、小基数或利润池右尾大于SIMO。"
    if diffs["激进短线"] < -12:
        return f"{ticker}短线高beta、价格确认或事件弹性强于SIMO。"
    return f"{ticker}在多数投资思路下比SIMO更符合项目内资金配置目标。"


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
        selected.sort(key=lambda row: (row["bc"] - row["ac"], row["bc"], -row["nc"]), reverse=True)
    elif final == "A":
        selected.sort(key=lambda row: (row["ac"] - row["bc"], row["ac"], -row["nc"]), reverse=True)
    return selected[:limit]


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy in STRATS:
            stats[strategy][tag_in_cell(comparison[strategy])] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b_rows = majority_rows(comparisons, "B", 55)
    strong_a_rows = majority_rows(comparisons, "A", 55)
    strong_b_rows = [row for row in strong_b_rows if row["bc"] >= 5 and row["bc"] - row["ac"] >= 3]
    strong_a_rows = [row for row in strong_a_rows if row["ac"] >= 5 and row["ac"] - row["bc"] >= 3]
    fin_rows = sum(1 for company in companies.values() if company.get("fin"))
    missing_price = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker]["fin"].get("price")
    ]

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}

    fin = a["fin"]
    mom2 = a["mom2"]
    mom1 = a["mom1"]
    soxx = a["soxx"]
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    support = {
        "NTM兑现优先": (
            "2026Q1收入342.1M、同比+105%；Q2指引393M-411M、同比+98%-107%；H1已约为2025全年84%",
            "MonTitan/boot客户和美元backlog未披露，库存与客户验收仍是兑现瓶颈",
        ),
        "右尾弹性优先": (
            "MonTitan、SM8008 boot drive、SM8466 Gen6、ICMS/CMX和AI KV cache让小基数收入有非线性上修",
            "极度乐观必须等客户/SKU/收入确认，不能只靠产品展示或生态叙事",
        ),
        "风险调整收益": (
            "基准NTM收入1.75B-2.10B、利润率20%-24%，若H2 ramp兑现有利润杠杆",
            "2026-06-22 P/S 10.76、Forward PE 33.84、Call IV 105.2%，SOXX压力窗口累计-81.31%",
        ),
        "下行保护优先": (
            "净现金、轻资产、控制器/firmware壁垒和股息提供一定底座",
            "Q1库存515.3M、OCF -31.2M，高IV和高回撤使其不适合防守优先",
        ),
        "估值消化优先": (
            "若NTM收入接近2B且GAAP OPM 20%-24%，当前估值可被部分业绩消化",
            "当前市值已反映AI存储重估，若Q3 sequential growth停滞则倍数压力大",
        ),
        "近端催化优先": (
            "Q2实际、Q3指引、MonTitan Q2 volume、H2五家tier-one CSP ramp、SM8008客户扩散均在1-2季可验证",
            "客户、SKU、订单金额和分产品收入披露不足会限制催化强度",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+18.82%、过去一月+30.72%，2026-06-22价格继续升至336.90美元",
            "上涨已较多，若基本面披露跟不上，价格确认会迅速变成透支反证",
        ),
        "激进短线": (
            "Call IV 105.2%、AI存储/KV cache/boot drive叙事、近端财报和小市值属性适合进攻",
            "高IV代表预期拥挤，客户ramp或现金流不及预期会放大回撤",
        ),
    }

    opposition_text = (
        f"{'、'.join(row['ticker'] for row in strong_b_rows[:12])}。这些公司通常在现金流、防守、估值消化、已披露RPO/订单、"
        "更大AI主链收入规模或更稳价格趋势上压过 SIMO。"
        if strong_b_rows
        else "无达到“B胜出至少5列且净胜3列”的显著强反方；SIMO主要输在防守、估值和少数更大AI主链公司的兑现规模。"
    )

    out: list[str] = []
    out += [
        "# SIMO 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：SIMO / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 SIMO vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。SIMO 的优势集中在右尾弹性、激进短线、近端催化、价格确认和NTM兑现；核心是Q1/Q2高run-rate、MonTitan Q2量产、H2五家tier-one CSP ramp、SM8008 boot drive和AI-native存储/KV cache重估。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是Forward PE `33.84`、P/S `10.76`、Call IV `105.2%`、Q1 OCF `-$31.2M`、库存 `$515.3M` 和SOXX压力窗口累计 `-81.31%`，因此不适合下行保护优先。",
        "- A 最适合的投资者画像：愿意承担高IV和高估值、押注企业级SSD控制器/boot storage从设计赢单转为云厂量产、并重视近端财报指引验证的成长进攻型资金。",
        "- A 最不适合的投资者画像：优先买低波动、低估值、强现金流、订单/backlog充分披露，或在SOXX压力期要求回撤可控的稳健资金。",
        f"- 多数思路下最强反方公司：{opposition_text}",
        "- 如果只追求更高增长、更好公司，A 的总体位置：SIMO 是项目内AI存储小基数高弹性标的，增长右尾和近端催化靠前，但风险调整、估值消化和下行保护明显弱于成熟现金流公司、部分大型AI平台和部分已披露订单更硬的主链公司；它更像进攻仓，而不是低波动核心仓。",
        "- 后续最重要跟踪数据：2026Q2实际收入和Q3指引、产品线QoQ/YoY、MonTitan客户/SKU/量产披露、boot drive客户扩散、Ferri/boot与MonTitan拆分、inventory turns、OCF、GAAP GM、enterprise SSD ASP、NAND allocation、Gen6/ICMS/CMX客户验证。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", TARGET]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$1.75-$2.10B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "MonTitan/boot drive 从 design win、客户 ramp 和产品展示变成可确认收入的速度；企业级 SSD 控制器需通过 NAND 兼容、OCP/NVMe、安全、firmware 和云厂 AVL 验证。"]),
        base.row(["最大反证", "Q1 inventory 已升至 515.3M 且 OCF 为 -31.2M；MonTitan/5家CSP未披露美元backlog，手机/PC需求和NAND成本仍会拖累低端控制器。"]),
        base.row(["近端催化剂", "Q2实际收入、Q3指引、MonTitan量产客户/SKU披露、SM8008客户扩散、Ferri/boot拆分线索、inventory turns和OCF转正。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        out.append(base.row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "同属存储/内存控制器、firmware/IP或相邻存储硅片价值层，优先比较客户认证、socket份额、收入兑现、毛利率和同业估值。", "RMBS、MRAM、MXL", "同业证据权重最高；若一方在客户、订单、份额或利润质量上明显更硬，结论力度可上调。"]),
        base.row(["相邻替代", "同属AI半导体、网络、边缘控制、功率或AI基础设施资金篮子，但产品不直接竞争。", "QCOM、ADI、ALAB、CRDO、ANET、VRT、ETN、NVT", "回答资金只能买一个时，谁的增长质量、估值消化和近端催化更好。"]),
        base.row(["上下游", "一方是SIMO的NAND/eSSD/服务器/云客户、供应链或制造生态，另一方是SIMO控制器/firmware环节。", "MU、SNDK、WDC、STX、DELL、HPE、NVDA、TSM、ASML", "强调利润池和议价权，不把下游收入规模或上游瓶颈自动等同胜出。"]),
        base.row(["跨赛道", "电力、机电、工业、化工、公用事业、软件等与SIMO业务差异大但可作为项目内资金配置替代。", "CEG、VST、LIN、TMO、CAT、ADBE", "默认降低结论力度；若证据互有强弱，优先中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    out.append(base.row(headers))
    out.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        out.append(
            base.row(
                [
                    index,
                    f"{comparison['ticker']} / {comparison['name']}",
                    comparison["classification"],
                    comparison["relationship"],
                    comparison["grade_diff"],
                    *[comparison[strategy] for strategy in STRATS],
                    comparison["majority"],
                    comparison["final_choice"],
                    comparison["key_reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        wins = [strategy for strategy in STRATS if (tag_in_cell(comparison[strategy]) or "").endswith("投B")]
        need = "需要 SIMO 披露更明确的MonTitan/SM8008客户订单、SKU、美元backlog、GM和OCF改善，并证明高估值可被NTM利润消化。"
        if comparison["relationship"] == "直接同业":
            need = "需要 SIMO 在同业中证明更强客户份额、企业级SSD控制器socket、boot drive出货、毛利率和可确认订单。"
        elif comparison["relationship"] == "跨赛道":
            need = "需要 SIMO 用更强收入兑现和现金流改善抵消跨赛道标的的低估值或防守优势。"
        out.append(base.row([index, f"{comparison['ticker']} / {comparison['name']}", "、".join(wins), comparison["key_reason"], need]))
    if not strong_b_rows:
        out.append(base.row([1, "无显著强反方", "无", "按 B 胜出至少5列且净胜3列的口径，没有公司在多数思路下明显强于 SIMO。", "继续跟踪SIMO估值、订单、客户和现金流；若这些弱化，低估值防守股和更大AI右尾股会成为更强反方。"]))

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        wins = [strategy for strategy in STRATS if (tag_in_cell(comparison[strategy]) or "").endswith("投A")]
        need = "需要 B 提供更硬NTM订单/利润兑现、同等AI存储右尾，或明显更好的估值消化和价格确认。"
        b = companies[comparison["ticker"]]
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:
            need = "需要 B 把防守优势转化为更高增长或明确催化，否则难以压过SIMO的AI存储右尾和短线弹性。"
        out.append(base.row([index, f"{comparison['ticker']} / {comparison['name']}", "、".join(wins), comparison["key_reason"], need]))

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照有明细行 {fin_rows}/{n} 家，可用价格/估值/IV 口径覆盖 {n - len(missing_price)}/{n} 家；缺少可用价格/估值/IV 的公司为 {('、'.join(missing_price) if missing_price else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI服务器_存储_EMS/SIMO_Silicon Motion Technology_公司调研_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_企业级SSD与高速存储控制器_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI-native存储与KV Cache基础设施_2026-06-10.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_存储晶圆制造_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_simo_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 SIMO 的 `+65%-98%` 等增长区间做专属投资思路校准后建档；未读取下游量化目录、备份、临时目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 SIMO 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    print(
        json.dumps(
            {
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "simo_tiers": companies[TARGET]["tiers"],
                "simo_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
                "simo_ranks": companies[TARGET]["ranks"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
