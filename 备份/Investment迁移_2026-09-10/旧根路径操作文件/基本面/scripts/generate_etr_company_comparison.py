from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "ETR"
TARGET_NAME = "Entergy Corporation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ETR_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_POWER_PEERS = {"AEP", "CEG", "DTE", "VST"}

POWER_ADJACENT = {
    "BE",
    "BWXT",
    "CMI",
    "ENS",
    "ENPH",
    "ET",
    "FCEL",
    "FLNC",
    "GEV",
    "GNRC",
    "HTHIY",
    "OKLO",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "AMPX",
}

ELECTRICAL_AND_INFRA_ALTS = {
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
    "ST",
    "TTDKY",
    "VICR",
    "VRT",
    "VSH",
    "WOLF",
    "AAON",
    "ALLE",
    "CARR",
    "CAT",
    "DCI",
    "DOV",
    "EME",
    "FIX",
    "FTV",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "PH",
    "PNR",
    "TT",
}

DOWNSTREAM_AI_LOAD = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
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
    "META",
    "MSFT",
    "NBIS",
    "NTAP",
    "NTNX",
    "ORCL",
    "PENG",
    "PSTG",
    "SANM",
    "SMCI",
}

AI_HARDWARE_DEMAND_CHAIN = {
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
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "MU",
    "NOK",
    "NVDA",
    "POET",
    "RMBS",
    "SIMO",
    "SITM",
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
    "VST": {
        "NTM兑现优先": 78.0,
        "右尾弹性优先": 80.0,
        "风险调整收益": 70.0,
        "下行保护优先": 72.0,
        "估值消化优先": 74.0,
        "近端催化优先": 74.0,
        "价格确认/动量": 55.0,
        "激进短线": 84.0,
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
    "ET": {
        "NTM兑现优先": 74.0,
        "右尾弹性优先": 62.0,
        "风险调整收益": 70.0,
        "下行保护优先": 84.0,
        "估值消化优先": 84.0,
        "近端催化优先": 68.0,
        "价格确认/动量": 35.0,
        "激进短线": 58.0,
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
}

ETR_SCORES = {
    "NTM兑现优先": 64.0,
    "右尾弹性优先": 52.0,
    "风险调整收益": 58.0,
    "下行保护优先": 88.0,
    "估值消化优先": 62.0,
    "近端催化优先": 62.0,
    "价格确认/动量": 42.0,
    "激进短线": 60.0,
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

    for strategy, score in ETR_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_POWER_PEERS:
        return "直接同业"
    if ticker in POWER_ADJACENT or ticker in ELECTRICAL_AND_INFRA_ALTS:
        return "相邻替代"
    if ticker in DOWNSTREAM_AI_LOAD or ticker in AI_HARDWARE_DEMAND_CHAIN:
        return "上下游"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str, company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if tag == "中性":
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "证据互有强弱且档位接近"

    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "ETR受监管收入、EPS指引和ESA路径更稳",
            "右尾弹性优先": "ETR 7-12GW管线和rate base右尾更清楚",
            "风险调整收益": "ETR受监管底盘叠加数据中心期权更均衡",
            "下行保护优先": "ETR低IV、公用事业现金流和压力期更稳",
            "估值消化优先": "ETR估值由EPS指引和rate base增长支撑",
            "近端催化优先": "ETR有Meta/Google审批和Investor Day节点",
            "价格确认/动量": "ETR价格修复和低波动略优",
            "激进短线": "ETR AI电力重估仍有事件弹性",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入/利润兑现证据更硬",
            "右尾弹性优先": f"{ticker}核电、容量或发电右尾更直接",
            "风险调整收益": f"{ticker}同业上行与下行组合更优",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}盈利倍数更容易消化",
            "近端催化优先": f"{ticker} PPA/容量或监管催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}电力主题beta更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}订单/backlog或交付路径更清楚",
            "右尾弹性优先": f"{ticker}设备或能源利润池右尾更直接",
            "风险调整收益": f"{ticker}增长和估值组合更优",
            "下行保护优先": f"{ticker}现金流或订单粘性更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}近端订单或产能催化更强",
            "价格确认/动量": f"{ticker}价格趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if rel == "上下游" or category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}AI主链收入/RPO兑现更短链",
            "右尾弹性优先": f"{ticker}AI主链或小基数右尾更大",
            "风险调整收益": f"{ticker}增长赔率更能覆盖执行风险",
            "下行保护优先": f"{ticker}需求能见度或现金流韧性更好",
            "估值消化优先": f"{ticker}高速增长更能消化估值",
            "近端催化优先": f"{ticker}产品/订单催化更密集",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合进攻",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker}未来12个月兑现证据更直接",
        "右尾弹性优先": f"{ticker}极端情景上行更大",
        "风险调整收益": f"{ticker}风险调整赔率更好",
        "下行保护优先": f"{ticker}资产质量或估值缓冲更好",
        "估值消化优先": f"{ticker}当前估值更容易消化",
        "近端催化优先": f"{ticker}未来两个季度催化更明确",
        "价格确认/动量": f"{ticker}价格行为更强",
        "激进短线": f"{ticker}短线波动和关注度更强",
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
    tag = label_for(strategy, a, b, rel)
    return f"{tag}：{reason_for(strategy, tag, rel, b)}"


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
        "估值消化优先": 1.05,
        "下行保护优先": 1.05,
        "右尾弹性优先": 0.85,
        "近端催化优先": 0.80,
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
    a_count = int(row_obj.get("ac", 0))
    b_count = int(row_obj.get("bc", 0))
    if a_count >= b_count + 2:
        return "A"
    if b_count >= a_count + 2:
        return "B"
    if a_count > b_count:
        return "B" if score < -1.0 else "A"
    if b_count > a_count:
        return "A" if score > 1.0 else "B"
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, choice: str, row_obj: dict | None = None) -> str:
    ticker = str(b["ticker"])
    if choice == "中性":
        return "ETR的受监管电力底盘与对手增长/估值证据互有强弱，当前不能可靠二选一。"
    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["下行保护优先"] > 12:
            return "ETR的低IV、受监管utility属性和压力窗口表现提供更好下行保护。"
        if diffs["风险调整收益"] > 10:
            return "ETR在受监管现金流、数据中心负荷期权和估值消化之间更均衡。"
        if diffs["NTM兑现优先"] > 10:
            return "ETR有2026 EPS指引、LTM收入和已签/推进ESA支撑NTM兑现。"
        if diffs["近端催化优先"] > 10:
            return "ETR的Meta/Google、rate base、Investor Day和监管节点更适合近端验证。"
        return "ETR的公用事业底盘、rate base增长和数据中心供电期权比对手更均衡。"

    if ticker == "CEG":
        return "CEG的Calpine并表、核电/PPA、清洁电力长约和数据中心站点供电，使NTM兑现与右尾强于ETR。"
    if ticker == "VST":
        return "VST的核电/气电资产、Meta PPA、Cogentrix敏感性和FCF锚，使进攻性和估值消化强于ETR。"
    if ticker == "AEP":
        return "AEP的下行保护和公用事业防守性略强，ETR的数据中心右尾还需要更多可确认ESA和rate base证据。"
    if ticker == "DTE":
        return "DTE的低IV、Oracle/Google负荷路径和受监管防守属性在该权重组合下更占优。"
    if row_obj and int(row_obj.get("bc", 0)) <= int(row_obj.get("ac", 0)):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        if wins:
            return f"{ticker}在{'、'.join(wins[:2])}等高权重口径压过ETR，其余列差距有限。"
    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的小基数、AI主链或核电/设备利润池右尾明显大于ETR。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比ETR更硬。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或当前估值更容易消化，ETR已包含公用事业AI电力溢价。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和资金偏好明显强于ETR。"
    if diffs["激进短线"] < -14:
        return f"{ticker}的短线高beta和主题关注度比ETR更适合进攻。"
    return f"{ticker}在多数投资思路下比ETR更符合项目内资金配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [
        strategy
        for strategy in STRATS
        if tier_value(a.get("tiers", {}).get(strategy)) > tier_value(b.get("tiers", {}).get(strategy))
    ]
    b_strong = [
        strategy
        for strategy in STRATS
        if tier_value(a.get("tiers", {}).get(strategy)) < tier_value(b.get("tiers", {}).get(strategy))
    ]
    close = [
        strategy
        for strategy in STRATS
        if tier_value(a.get("tiers", {}).get(strategy)) == tier_value(b.get("tiers", {}).get(strategy))
    ]
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts) if parts else "档位接近"


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
        choice = final_choice(row_obj)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, choice, row_obj)
        rows.append(row_obj)

    def sort_key(item: dict) -> tuple[int, str, str]:
        rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
        return (rel_order.get(item["relationship"], 9), item["classification"], item["ticker"])

    return sorted(rows, key=sort_key)


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
    dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{dates[0]} 至 {dates[-1]}" if dates else "缺失"
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
            "B",
            "中上档",
            "1Q26 operating revenue 31.88亿美元、LTM operating revenue 132.87亿美元、2026 adjusted EPS指引4.25-4.45美元，传统受监管售电和早期ESA收入支撑基准兑现",
            "NTM收入增长主要仍是公用事业底盘+少量大负荷，7-12GW管线不能直接进入12个月收入",
        ),
        "右尾弹性优先": (
            "B",
            "中上档",
            "7-12GW数据中心管线、Meta/Google/Amazon线索、2026-2030约670亿美元capex和rate base从460亿美元到970亿美元提供长期右尾",
            "受监管收益非线性弱于设备/核电/NeoCloud小基数，且燃机、变压器、500kV和监管审批限制NTM速度",
        ),
        "风险调整收益": (
            "B",
            "强势档",
            "regulated utility底盘、低IV、长期ESA和rate-base化路径降低需求兑现风险",
            "Forward PE 22.16、P/S 3.87已反映AI电力溢价，570-670亿美元级capex和外部融资压低赔率",
        ),
        "下行保护优先": (
            "A",
            "强势档",
            "Call IV 26.9%、Put IV 25.1%，SOXX三段压力窗口累计-5.67%，受监管客户、费率机制和电力刚需提供防守属性",
            "建设期FCF持续为负，高债务、飓风、利率、燃料/购电和监管成本分摊仍会冲击安全边际",
        ),
        "估值消化优先": (
            "B",
            "中上档",
            "2026 EPS指引和rate base增长可部分消化22倍远期PE，估值压力低于许多高P/S高IV AI链标的",
            "对传统utility并不便宜，必须依赖负荷增长、rate base和监管顺利证明溢价合理",
        ),
        "近端催化优先": (
            "B",
            "中上档",
            "Meta Louisiana、Google special rate、Investor Day资本计划、LPSC/APSC/MPSC/PUCT docket和Q2/Q3 industrial sales均是近端验证点",
            "多数发电/输电资产COD偏2028以后，近端更多是审批和进度，不是利润爆发",
        ),
        "价格确认/动量": (
            "C",
            "中性偏弱",
            "2026-06-22价格112.20美元，较2026-06-03的108.66美元有修复且IV低",
            "正式区间涨跌文件截至2026-06-03显示过去两周-2.92%、过去一月-6.67%，动量弱于AI主链和高beta电力设备",
        ),
        "激进短线": (
            "B",
            "弱势档",
            "AI电力供给瓶颈、Meta/Google新闻流和监管节点可触发事件交易，且低IV使期权成本较低",
            "公用事业属性和大基数限制短线爆发，弱于OKLO/SMR、光互联、NeoCloud、VRT/GEV/POWL等高beta标的",
        ),
    }

    product_names = [str(product[0]).split("：")[0] for product in a.get("products", [])[:8]]

    lines: list[str] = [
        "# ETR 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：ETR / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 ETR vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司排序不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ETR 的优势集中在受监管utility底盘、低IV、SOXX压力窗口韧性、Meta/Google数据中心负荷与rate base长期路径。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是NTM直接AI收入占比仍低、建设期FCF为负、估值已高于传统utility，右尾非线性弱于AI主链/核能开发/电气设备高beta标的。",
        "- A 最适合的投资者画像：希望配置AI数据中心电力供给瓶颈，但更看重受监管现金流、低波动、客户成本分担和长期rate base增长的中期资金。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大右尾、小基数利润杠杆、强价格动量或激进短线波动的资金。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常拥有更直接AI主链收入、订单/RPO、核电/发电/PPA现金流、设备订单或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：ETR 是项目内偏防守的AI电力负荷+rate base期权标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。它相对多数高估值、低现金流或证据不足公司更稳，但通常不如NVDA/AVGO/MU/ALAB/CRDO、CEG/VST、GEV/VRT/POWL、OKLO/SMR这类高右尾或高动量标的适合进攻。",
        "- 后续最重要跟踪数据：signed/advanced ESA MW、actual energization MW、industrial sales GWh、Meta Louisiana LPSC docket、Google special rate与上电时间、customer contribution/CIAC、500kV线路和变电NTP/COD、燃机/变压器交付、rate base roll-forward、O&M per MWh、FFO/debt、equity/forward issuance、OCF vs capex。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ETR"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "电力_发电_能源_储能")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "`$14.0-14.8B`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev')}；极度乐观：{a.get('extreme_rev')}"]),
        base.row(["利润和现金流结论", "基准 adjusted EPS `$4.25-4.45`，净利润约 `$2.0-2.1B`；建设期OCF为正但FCF明显为负，现金流质量取决于客户出资、债务/权益融资和监管回收速度。"]),
        base.row(["最大传导瓶颈", "ESA/特殊费率能否获批，客户是否承担 full cost of service，燃机/大型变压器/开关设备/500kV线路能否按期交付并转入rate base。"]),
        base.row(["最大反证", "7-12GW数据中心管线多数未在NTM内完全签约/通电；燃料和购电pass-through会放大收入但不等同利润；高capex、债务和潜在股权融资可能摊薄EPS。"]),
        base.row(["近端催化剂", "Meta Louisiana、Google Arkansas special rate、Amazon/Mississippi线索、2026 Investor Day后续、LPSC/APSC/MPSC/PUCT docket、Q2/Q3 industrial sales、rate base roll-forward和融资计划。"]),
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
        base.row(["直接同业", "与ETR同属电力公用事业、竞争性发电或AI电力供给篮子，优先比较受监管/merchant收入兑现、长约/PPA、rate base、发电资产、现金流、估值和压力期表现。", "AEP、DTE、CEG、VST", "判断力度最高；若同业在核电/PPA、FCF、监管兑现或下行保护上明显更强，可给建议或强烈建议。"]),
        base.row(["相邻替代", "同属AI数据中心电力、燃气发电、储能、电气设备、工程、冷却和工业基础设施资金篮子，但利润池不同；比较资金只能买一个时谁的增长质量、估值消化和催化更好。", "ET、GEV、BE、SMR、OKLO、ETN、VRT、POWL、PWR、EME、TT", "中等力度；赛道热度不能自动胜出，必须有订单、backlog、现金流、估值或催化证据。"]),
        base.row(["上下游", "云厂、IDC、NeoCloud、服务器、网络和AI芯片是ETR数据中心负荷的需求链来源；比较时区分下游收入规模、ETR可捕获的受监管回报和各自承担的capex/估值压力。", "MSFT、META、AMZN、GOOGL、ORCL、EQIX、DLR、CRWV、NVDA、DELL、ANET", "不把下游客户规模直接等同ETR利润池；若对方拥有更直接RPO/订单或价格确认，可在右尾/催化/动量列胜出。"]),
        base.row(["跨赛道", "半导体设备、材料、封测、化学品、软件和部分工业公司与ETR业务差异大，但作为组合资金替代仍比较增长质量、风险调整收益、估值消化和下行保护。", "ASML、AMAT、LRCX、LIN、TMO、ADBE、RKLB", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        catchup = "ETR需要把7-12GW管线更多转成已签ESA、已获批rate base和可确认EPS/OCF，并重新获得价格确认。"
        if row_obj["relationship"] == "直接同业":
            catchup = "ETR需要证明数据中心负荷、监管成本回收、EPS增长和估值消化优于电力直接同业。"
        elif row_obj["relationship"] == "上下游":
            catchup = "ETR需要证明自己能从下游AI负荷中捕获高质量受监管回报，而不只是承担capex和融资压力。"
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
        "- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/ETR_Entergy Corporation_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- ETR 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_etr_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对ETR的2026 adjusted EPS指引、7-12GW数据中心管线、Meta/Google/Investor Day、rate base路径、低IV、估值溢价、建设期负FCF和capex/融资/监管约束做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 ETR 正式评估文件")
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
                "size": OUT_PATH.stat().st_size,
                "etr_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "etr_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "etr_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
