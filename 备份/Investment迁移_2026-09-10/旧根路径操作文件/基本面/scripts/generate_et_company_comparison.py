from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "ET"
TARGET_NAME = "Energy Transfer LP"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ET_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

UTILITY_AND_POWER_DOWNSTREAM = {
    "AEP",
    "CEG",
    "DTE",
    "ETR",
    "VST",
}

GAS_POWER_ADJACENT = {
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
    "OKLO",
    "PSIX",
    "RYCEY",
    "SMR",
    "AMPX",
}

POWER_ELECTRICAL_INFRA = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "ETN",
    "HUBB",
    "IFNNY",
    "LFUS",
    "MIELY",
    "MPWR",
    "MRAAY",
    "NVT",
    "NVTS",
    "POWI",
    "POWL",
    "PWR",
    "ST",
    "TTDKY",
    "VICR",
    "VRT",
    "VSH",
    "WOLF",
}

INDUSTRIAL_INFRA = {
    "AAON",
    "ALLE",
    "CARR",
    "CAT",
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
    "MYRG",
    "NDSN",
    "PH",
    "PNR",
    "TDY",
    "TMO",
    "TT",
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

SERVER_AND_NETWORK_DEMAND_CHAIN = {
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

LOCAL_SCORE_FLOORS = {
    "CEG": {
        "NTM兑现优先": 86.0,
        "右尾弹性优先": 76.0,
        "风险调整收益": 55.5,
        "下行保护优先": 64.0,
        "估值消化优先": 65.0,
        "近端催化优先": 68.0,
        "价格确认/动量": 39.0,
        "激进短线": 75.0,
    },
    "DTE": {
        "NTM兑现优先": 63.0,
        "右尾弹性优先": 45.0,
        "风险调整收益": 54.0,
        "下行保护优先": 91.0,
        "估值消化优先": 61.0,
        "近端催化优先": 63.0,
        "价格确认/动量": 38.0,
        "激进短线": 60.0,
    },
    "ENS": {
        "NTM兑现优先": 68.0,
        "右尾弹性优先": 59.0,
        "风险调整收益": 63.0,
        "下行保护优先": 83.0,
        "估值消化优先": 71.0,
        "近端催化优先": 67.0,
        "价格确认/动量": 67.0,
        "激进短线": 76.0,
    },
    "EME": {
        "NTM兑现优先": 74.0,
        "右尾弹性优先": 60.0,
        "风险调整收益": 62.0,
        "下行保护优先": 76.0,
        "估值消化优先": 68.0,
        "近端催化优先": 70.0,
        "价格确认/动量": 34.0,
        "激进短线": 68.0,
    },
    "AEP": {
        "NTM兑现优先": 62.0,
        "右尾弹性优先": 47.0,
        "风险调整收益": 56.0,
        "下行保护优先": 90.0,
        "估值消化优先": 60.0,
        "近端催化优先": 58.0,
        "价格确认/动量": 40.0,
        "激进短线": 54.0,
    },
    "ETR": {
        "NTM兑现优先": 64.0,
        "右尾弹性优先": 52.0,
        "风险调整收益": 58.0,
        "下行保护优先": 88.0,
        "估值消化优先": 62.0,
        "近端催化优先": 62.0,
        "价格确认/动量": 42.0,
        "激进短线": 60.0,
    },
}

ET_SCORES = {
    "NTM兑现优先": 74.0,
    "右尾弹性优先": 62.0,
    "风险调整收益": 70.0,
    "下行保护优先": 84.0,
    "估值消化优先": 84.0,
    "近端催化优先": 68.0,
    "价格确认/动量": 35.0,
    "激进短线": 58.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


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
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in {**calibrated.SCORE_FLOORS, **LOCAL_SCORE_FLOORS}.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)
            company["scores"][strategy] = max(current, floor)

    for strategy, score in ET_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in UTILITY_AND_POWER_DOWNSTREAM or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in GAS_POWER_ADJACENT or ticker in POWER_ELECTRICAL_INFRA or ticker in INDUSTRIAL_INFRA:
        return "相邻替代"
    if ticker in SERVER_AND_NETWORK_DEMAND_CHAIN:
        return "上下游"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "证据互有强弱且档位接近"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "ET有2026 EBITDA指引和项目投运硬锚",
            "右尾弹性优先": "ET气管网backlog提供长周期右尾",
            "风险调整收益": "ET低估值、DCF和长约现金流更均衡",
            "下行保护优先": "ET低估值、分配覆盖和压力期表现更稳",
            "估值消化优先": "ET低P/S和低远期PE更易消化",
            "近端催化优先": "ET有Hugh Brinson和NGL投运节点",
            "价格确认/动量": "ET价格弱但对手更缺确认",
            "激进短线": "ET气电叙事与低估值仍有事件弹性",
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
            "右尾弹性优先": f"{ticker}电力设备或能源右尾更直接",
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
        return "中性"

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
        return "ET的现金流/估值优势与对手增长或催化优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["估值消化优先"] > 12:
            return "ET的0.70x P/S、12.37x远期PE和18B美元级EBITDA更容易消化估值。"
        if diffs["下行保护优先"] > 12:
            return "ET的长约fee cash flow、分配覆盖和SOXX压力窗口表现提供更好下行保护。"
        if diffs["风险调整收益"] > 10:
            return "ET在低估值、DCF、长约项目和可见现金流之间的风险调整组合更均衡。"
        if diffs["NTM兑现优先"] > 10:
            return "ET有2026 EBITDA指引、Q1分部数据和Hugh Brinson/Mustang Draw/NGL投运支撑NTM兑现。"
        return "ET的中游现金流、低估值和天然气长约项目比对手更适合该口径。"

    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或电力设备右尾明显大于ET。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和资金偏好明显强于ET，ET近期价格仍偏弱。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比ET更直接。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比ET更硬。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量和风险调整收益组合优于ET。"
    return f"{ticker}在多数投资思路下比ET更符合项目内资金配置目标。"


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
            "A",
            "强势档",
            "2026E Adjusted EBITDA 18.2-18.6B、Q1 2026 EBITDA 4.937B、DCF 2.704B、Hugh Brinson/Mustang Draw/NGL扩容均有时间表",
            "收入受Sunoco和商品通过性放大，项目级tariff和partial-year确认仍需估算",
        ),
        "右尾弹性优先": (
            "B",
            "中上档",
            "6+Bcf/d签约容量、18年加权期、25B+ firm transportation fees和AI上电燃气路径提供长周期右尾",
            "公司基数太大，AI直接收入当前仍低于1%，极度乐观依赖多个项目同时提前",
        ),
        "风险调整收益": (
            "A",
            "强势档",
            "0.70x P/S、12.37x远期PE、9.78x EV/EBITDA、长约fee现金流和分配覆盖构成低估值现金流赔率",
            "长债约69B、growth capex 5.5-5.9B、MLP/K-1和项目许可/融资仍是折扣项",
        ),
        "下行保护优先": (
            "A",
            "强势档",
            "SOXX三段压力窗口累计-17.84%、低估值、fee-based EBITDA和DCF覆盖使防守性强于多数高beta AI链",
            "能源/MLP仍受利率、债务、监管许可、商品价差和资本市场窗口影响",
        ),
        "估值消化优先": (
            "S",
            "全项目顶档",
            "低P/S、低远期PE和18B美元级EBITDA指引使当前估值不需要极度乐观AI情景才能消化",
            "consolidated revenue质量被Sunoco和商品价格稀释，需用EBITDA/DCF而非收入倍数单独判断",
        ),
        "近端催化优先": (
            "A",
            "偏强",
            "Q2/Q3分部EBITDA、Oracle/Nexus/Oklahoma、Hugh Brinson Q4 2026/Q1 2027、Mustang Draw I/II和NGL项目均有跟踪点",
            "多数AI气电项目的完整收入化偏2027-2029，1-2季度更像进度验证而非爆发式重估",
        ),
        "价格确认/动量": (
            "C",
            "偏弱",
            "低波动和高分配收益提供支撑，SOXX压力窗口表现好于高beta链",
            "2026-06-22价格18.89低于6月初19.55，过去两周-3.03%、一月-1.96%，趋势未确认",
        ),
        "激进短线": (
            "D",
            "弱势档",
            "Call IV 31.4%、AI上电燃气叙事和低估值可支持事件交易",
            "MLP属性和大基数限制短线爆发力，弱于NeoCloud、核能开发、光互联和高beta电力设备",
        ),
    }

    product_names = [str(product[0]).split("：")[0] for product in a.get("products", [])[:8]]

    lines: list[str] = []
    lines += [
        "# ET 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：ET / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 ET vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ET 的优势集中在低估值、DCF/分配覆盖、fee-based中游现金流、2026 EBITDA指引和SOXX压力窗口韧性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是AI直接收入当前仍小、公司基数大、右尾非线性弱于AI主链，且2026-06-22价格较6月初走弱。",
        "- A 最适合的投资者画像：希望用低估值现金流和高分配收益获取AI数据中心燃气供给长期期权，同时不愿承担纯高beta AI链估值压力的风险调整型资金。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大短线爆发、核能/NeoCloud/光互联/AI芯片小基数右尾或强动量价格确认的进攻型资金。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常拥有更直接AI主链收入、订单/RPO、数据中心设备利润池、核电/电力主题右尾或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：ET 是项目内偏强的低估值现金流+AI上电燃气期权标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。它在估值消化、下行保护和风险调整收益上显著强于很多高估值/低现金流公司，但面对NVDA/AVGO/MU/ALAB/CRDO/CEG/GEV/VRT/POWL/OKLO/SMR等AI主链或电力高beta右尾标的，右尾和短线通常不占优。",
        "- 后续最重要跟踪数据：每季度Intrastate/Interstate/Midstream/NGL/Crude/SUN/USAC segment EBITDA、contracted MMcf/d转in-service MMcf/d、Hugh Brinson实际投运、Oracle/Nexus/Oklahoma/Entergy/Fermi/AR项目状态、Mustang Draw I/II利用率、NGL exports/fractionation volumes、growth capex、DCF attributable to partners、debt/EBITDA、Sunoco/Parkland整合成本和分配覆盖。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ET"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "电力_发电_能源_储能")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "`$103-110B`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev')}；极度乐观：{a.get('extreme_rev')}"]),
        base.row(["利润和现金流结论", "基准 Adjusted EBITDA `$18.6-19.6B`，归属合伙人净利 `$4.7-5.4B`；DCF可覆盖分配并支持大部分维护/增长资金，growth capex后接近中性到小幅正。"]),
        base.row(["最大传导瓶颈", "已签天然气容量和项目backlog能否在NTM内从可参与需求转成in-service、billable firm transportation / processing / storage revenue，尤其是Hugh Brinson、Oracle/Nexus/Oklahoma、Mustang Draw和NGL项目。"]),
        base.row(["最大反证", "AI直接收入当前仍小，Sunoco/Parkland和NGL/原油商品通过性会放大收入但不等同高质量利润；长债、capex、许可和项目费率未披露限制右尾兑现。"]),
        base.row(["近端催化剂", "Q2/Q3 segment EBITDA、Oracle/Nexus/Oklahoma流气进度、Hugh Brinson施工/投运、Mustang Draw I/II、NGL export/fractionation/storage项目、DCF覆盖、debt/EBITDA和Sunoco/Parkland协同。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        tier = a.get("tiers", {}).get(strategy, "资料不足")
        position = f"{support[strategy][1]}；评分排名 {a.get('ranks', {}).get(strategy)}/{a.get('rank_total', {}).get(strategy)}"
        lines.append(base.row([strategy, tier, position, support[strategy][2], support[strategy][3]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "项目内没有KMI/WMB/EPD/ONEOK这类纯中游天然气管网同业，因此不强行把电力公司或设备公司列为直接同业；若未来加入中游管网公司，应优先比较费率、管网位置、contracted capacity、DCF和杠杆。", "本次无纯直接同业", "本报告主表基本不使用直接同业放大规则；避免把下游utility或电力设备误判为ET同业。"]),
        base.row(["相邻替代", "同属AI数据中心电力、燃气发电、储能、发电设备、配电、工程、冷却和工业基础设施资金篮子，但利润池不同；重点回答资金只能买一个时谁的增长质量、估值消化和风险调整收益更好。", "BE、GEV、GNRC、PSIX、RYCEY、ENS、VRT、ETN、POWL、PWR、EME、TT", "中等力度；赛道更热不能自动胜出，必须有订单、backlog、现金流、估值或催化证据。"]),
        base.row(["上下游", "公用事业、发电商、云厂、IDC、NeoCloud、服务器和网络平台是ET天然气供给需求链的下游或需求来源；比较时区分客户收入规模、ET可捕获fee revenue和各自承担的capex/估值压力。", "AEP、DTE、ETR、CEG、VST、ORCL、GOOGL、MSFT、AMZN、META、DLR、EQIX、NVDA、DELL、ANET", "不把下游客户规模直接等同ET利润机会；若对方拥有更直接AI收入、RPO或价格确认，可在右尾/催化/动量列胜出。"]),
        base.row(["跨赛道", "半导体设备、材料、封测、化学品、软件和部分工业公司与ET业务差异大，但作为组合资金替代仍比较增长质量、估值消化、下行保护和催化可见度。", "ASML、AMAT、LRCX、LIN、TMO、ADBE、RKLB", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        catchup = "ET需要把6+Bcf/d签约容量更多转成in-service fee revenue，披露更清晰项目费率/EBITDA贡献，并重新获得价格确认。"
        if row_obj["relationship"] == "上下游":
            catchup = "ET需要证明自己能从下游AI负荷中捕获高质量长约现金流，而不是只承担管网capex和项目许可风险。"
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
        "- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/ET_Energy Transfer LP_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- ET 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_et_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对ET的2026 EBITDA指引、6+Bcf/d签约容量、25B+ firm fees、Hugh Brinson/Mustang Draw/NGL项目、低估值、DCF、分配覆盖、弱价格动量和MLP/债务/capex约束做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 ET 正式评估文件")
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
                "et_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "et_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "et_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
