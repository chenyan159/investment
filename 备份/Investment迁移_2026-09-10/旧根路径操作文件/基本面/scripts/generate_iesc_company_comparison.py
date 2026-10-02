from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as project_calibration
import generate_etn_company_comparison as etn_calibration


TARGET = "IESC"
TARGET_NAME = "IES Holdings"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "IESC_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_IESC_PEERS = {
    "EME",
    "FIX",
    "MYRG",
    "PWR",
    "POWL",
    "ATKR",
}

ADJACENT_POWER_MEP_COOLING = {
    "AAON",
    "ABBNY",
    "ALLE",
    "BE",
    "BWXT",
    "CARR",
    "CAT",
    "CMI",
    "DCI",
    "DD",
    "DHR",
    "DKILY",
    "DOV",
    "ECL",
    "ENS",
    "ETN",
    "FCEL",
    "FLNC",
    "FTV",
    "GEV",
    "GNRC",
    "HTHIY",
    "HUBB",
    "IFNNY",
    "JCI",
    "LFUS",
    "MIELY",
    "MOD",
    "MPWR",
    "MRAAY",
    "MSI",
    "NDSN",
    "NVT",
    "NVTS",
    "PH",
    "PNR",
    "POWI",
    "PSIX",
    "RYCEY",
    "SMR",
    "ST",
    "TDY",
    "TMO",
    "TT",
    "TTDKY",
    "VICR",
    "VRT",
    "VSH",
    "WOLF",
}

UTILITY_AND_POWER_DEPENDENCIES = {
    "AEP",
    "CEG",
    "DTE",
    "ET",
    "ETR",
    "VST",
    "APD",
    "LIN",
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

SERVER_NETWORK_COMPUTE_CHAIN = {
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

IESC_SCORES = {
    "NTM兑现优先": 81.0,
    "右尾弹性优先": 78.0,
    "风险调整收益": 58.0,
    "下行保护优先": 70.0,
    "估值消化优先": 67.5,
    "近端催化优先": 79.0,
    "价格确认/动量": 70.0,
    "激进短线": 78.0,
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
        fin = company.get("fin", {})
        if not fin or not fin.get("price"):
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"
                company.setdefault("ranks", {})[strategy] = None


def score_companies(companies: dict[str, dict]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    floors: dict[str, dict[str, float]] = {}
    floors.update(getattr(project_calibration, "SCORE_FLOORS", {}))
    floors.update(getattr(etn_calibration, "LOCAL_SCORE_FLOORS", {}))
    floors["ETN"] = getattr(etn_calibration, "ETN_SCORES", {})

    for ticker, strategy_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in strategy_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)
            company["scores"][strategy] = max(current, floor)

    for strategy, score in IESC_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_IESC_PEERS:
        return "直接同业"
    if ticker in ADJACENT_POWER_MEP_COOLING:
        return "相邻替代"
    if ticker in UTILITY_AND_POWER_DEPENDENCIES or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_NETWORK_COMPUTE_CHAIN:
        return "上下游"
    if category in {"机电_冷却_工程_水处理_边缘工业AI", "配电_电源_功率器件", "电力_发电_能源_储能"}:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
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
            "NTM兑现优先": "IESC backlog/RPO与6-12个月转收入更清楚",
            "右尾弹性优先": "IESC C&I和custom power可非线性放量",
            "风险调整收益": "IESC增长、利润和估值组合更均衡",
            "下行保护优先": "IESC盈利底盘和订单可见度更稳",
            "估值消化优先": "IESC NTM增长更能消化当前估值",
            "近端催化优先": "IESC Q3/Q4 backlog兑现催化更近",
            "价格确认/动量": "IESC近期价格已确认基本面",
            "激进短线": "IESC数据中心电力/MEP题材弹性更高",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单/backlog兑现更硬",
            "右尾弹性优先": f"{ticker}同业右尾或利润池更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业业绩更能覆盖估值",
            "近端催化优先": f"{ticker}同业订单/产能催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
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

    if rel == "上下游" or category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}AI主链兑现证据更硬",
            "右尾弹性优先": f"{ticker}AI主链或需求端右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}产品/订单催化更密集",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
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
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 25, 12, 4
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
        "NTM兑现优先": 1.18,
        "风险调整收益": 1.18,
        "估值消化优先": 1.12,
        "下行保护优先": 1.02,
        "近端催化优先": 0.90,
        "右尾弹性优先": 0.82,
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
        return "IESC的backlog兑现与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "IESC有RPO/backlog、非住宅三分部高增长和C&I未来6-12个月转收入支撑。"
        if diffs["近端催化优先"] > 10:
            return "IESC的Q3/Q4收入确认、Infrastructure产能和C&I backlog兑现更容易近端验证。"
        if diffs["估值消化优先"] > 10:
            return "IESC的NTM收入和EBITDA增长更能覆盖当前P/S与TTM PE压力。"
        if diffs["右尾弹性优先"] > 12:
            return "IESC在AI数据中心MEP、custom power和低压通信上的可收入化右尾更直接。"
        return "IESC在项目执行、订单可见度和数据中心物理基础设施暴露上更适合该思路。"

    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于IESC。"
    if diffs["下行保护优先"] < -16:
        return f"{ticker}的现金流、资产质量、IV或压力窗口安全性强于IESC。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和资金偏好明显强于IESC。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比IESC更硬。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值和下行组合优于IESC。"
    return f"{ticker}在多数投资思路下比IESC更符合项目内资金配置目标。"


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
        selected = [row for row in rows if row["final_choice"] == final and row["bc"] >= 5 and row["bc"] - row["ac"] >= 2]
        selected.sort(key=lambda x: (x["bc"] - x["ac"], x["bc"], -x["nc"]), reverse=True)
    else:
        selected = [row for row in rows if row["final_choice"] == final and row["ac"] >= 5 and row["ac"] - row["bc"] >= 2]
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
            "FY2026 Q2收入9.742亿美元、FY2026前6个月18.452亿美元；RPO 23.471亿美元、backlog 38.621亿美元，非住宅三分部约87.5% backlog",
            "公司不提供传统全年收入/EPS指引；backlog中15.150亿美元为不可强制执行协议/LOI，C&I Q2收入尚未加速",
        ),
        "右尾弹性优先": (
            "强势档",
            "基准收入44-48亿美元、乐观51-57亿美元、极度乐观62-70亿美元；C&I、Infrastructure custom power和Communications均可被AI园区建设放大",
            "客户名、AI数据中心收入、标准化power island订单和取消率未披露，极度乐观可信度低到中",
        ),
        "风险调整收益": (
            "强势档",
            "收入增速、EBITDA弹性、P/S 4.14和已盈利经营底盘优于多数纯期权标的",
            "TTM PE 40.12、EV/EBITDA 29.26、Call IV 70.8%，项目制收入和营运资本会抬高下行风险",
        ),
        "下行保护优先": (
            "中性偏弱",
            "RPO/backlog、分部利润、住宅以外的非住宅需求和现金流为压力期提供经营支撑",
            "不是低波动防守股；2026-06-22 Call IV 70.8%，三段SOXX压力窗口累计-43.85%，固定价/人工/材料风险仍高",
        ),
        "估值消化优先": (
            "强势档",
            "NTM基准收入相对TTM约+21%-32%，基准EBITDA 5.2-6.4亿美元，收入和利润增长可部分消化估值",
            "Forward PE缺失，市场可能已给较高数据中心施工/电力稀缺预期；FCF conversion受AR、contract assets和capex影响",
        ),
        "近端催化优先": (
            "全项目顶档",
            "未来1-2个季度可验证C&I backlog转收入、Infrastructure新增产能、Communications持续高增和Q3/Q4分部margin",
            "近端催化依赖执行节奏，不是单一产品发布；现场readiness和关键电气设备到货可能推迟收入确认",
        ),
        "价格确认/动量": (
            "中上档",
            "2026-06-03过去两周+10.45%、过去一月+10.50%，2026-06-22价格754.74仍延续强趋势",
            "价格已包含部分AI园区电力/MEP叙事，若Q3/Q4收入未兑现容易回撤",
        ),
        "激进短线": (
            "中性偏弱",
            "高IV、近期动量、AI数据中心电力/MEP瓶颈和C&I backlog burn使短线进攻弹性较高",
            "短线弹性仍低于小基数亏损转盈利、光互联/AI芯片订单爆发和NeoCloud高beta标的",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "Communications低压/光纤/技术基础设施",
            "Infrastructure custom power/generator enclosure/bus duct",
            "Commercial & Industrial数据中心电气/MEP",
            "Residential住宅电气/HVAC/管道",
        ]

    lines: list[str] = [
        "# IESC 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：IESC / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 IESC vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。IESC 的优势集中在 FY2026 Q2 已经进入收入表的 Communications/Infrastructure 高增长、38.621 亿美元 backlog、23.471 亿美元 RPO、C&I 未来 6-12 个月执行窗口，以及数据中心电力/低压/MEP 需求可收入化。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 AI 数据中心收入和客户名未披露、backlog中含不可强制执行协议/LOI、住宅业务低利润抵消、固定价合同/人工/材料/工作资本风险，以及 2026-06-22 Call IV 70.8% 不具备低波动防守属性。",
        "- A 最适合的投资者画像：想投 AI 数据中心物理建设、低压通信、MEP 和 custom power，但仍要求已有收入、backlog/RPO、分部利润和近端财报验证的进攻型基本面资金。",
        "- A 最不适合的投资者画像：只买极致高毛利芯片/软件平台、低 IV 防守股，或不愿承担施工项目收入确认、固定价合同、营运资本和并购整合风险的资金。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在AI主链右尾、芯片/光互联/电力设备订单、平台现金流、低IV防守或价格确认上强于IESC。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：IESC 是项目内偏强的 AI 数据中心物理基础设施/MEP 标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它明显强于多数传统材料、低增长工业和纯远期期权，但面对 NVDA/AVGO/MU/ALAB/CRDO/ANET、ETN/VRT/POWL/GEV 以及部分云算力/IDC 高beta标的时需要按投资思路拆分。",
        "- 后续最重要跟踪数据：FY2026 Q3/Q4 segment revenue、C&I backlog burn、Infrastructure Gulf Island/Greiner contribution、Communications data center growth、分部margin、RPO/backlog强制性比例、AR/contract assets与OCF/FCF、capex、客户项目或框架协议、Residential margin、关键电气设备和现场readiness。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "IESC"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "机电_冷却_工程_水处理_边缘工业AI")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "44.0-48.0 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '51.0-57.0 亿美元'}；极度乐观：{a.get('extreme_rev') or '62.0-70.0 亿美元'}"]),
        base.row(["利润和现金流结论", "基准调整后EBITDA 5.2-6.4亿美元、调整后净利润3.4-4.5亿美元；FCF基准应为正，但高增长情景可能被应收、合同资产、capex和收购整合投资吞掉。"]),
        base.row(["最大传导瓶颈", "RPO/backlog -> 客户NTP/现场readiness -> 关键电气设备和材料到货 -> 工厂/现场产能 -> FAT/SAT/commissioning -> percentage-of-completion收入确认。"]),
        base.row(["最大反证", "不披露AI data center revenue、客户名、取消率和lead time；C&I Q2收入仅+1%；backlog中15.150亿美元为不可强制执行协议/LOI；住宅业务低利润拖累。"]),
        base.row(["近端催化剂", "FY2026 Q3/Q4 revenue by segment、C&I backlog转收入、Infrastructure Gulf Island/Greiner并表和产能爬坡、Communications 30%+增速延续、OCF/FCF conversion。"]),
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
        base.row(["直接同业", "同属电气/MEP工程、数据中心施工、工业电气项目、custom power或电气材料需求池；优先比较backlog/RPO、收入确认、项目margin、现金流、客户质量和估值。", "EME、FIX、MYRG、PWR、POWL、ATKR", "判断力度最高；直接同业在订单、margin、backlog burn或估值消化上显著更强时可压过IESC。"]),
        base.row(["相邻替代", "同属AI园区电力、冷却、MEP、发电、储能、配电、功率器件、工业基础设施或楼宇系统资金篮子，但产品或收入模式不完全重叠。", "ETN、VRT、HUBB、NVT、GEV、TT、MOD、CARR、AAON、JCI、BE、GNRC", "中等力度；赛道更热不能自动胜出，必须落实到订单、backlog、利润率、FCF和估值消化。"]),
        base.row(["上下游", "云厂、IDC、NeoCloud、AI服务器、网络、芯片、发电/公用事业是IESC需求链上下游；比较时区分客户capex规模、IESC可捕获工程利润和各自估值/融资风险。", "MSFT、AMZN、GOOGL、META、EQIX、DLR、CRWV、NVDA、DELL、ANET、AEP、CEG、VST", "不把客户capex直接等同IESC收入；若对方拥有更直接AI收入、RPO或价格确认，可在右尾、催化和动量列胜出。"]),
        base.row(["跨赛道", "半导体设备、材料、封测、软件和部分工业公司与IESC业务差异大，但作为组合资金替代仍比较增长质量、风险调整收益、估值消化和催化可见度。", "ASML、AMAT、LRCX、LIN、TMO、ADBE、RKLB", "默认降低结论力度；除非增长质量、估值消化或右尾弹性明显拉开，否则用中性或微倾向。"]),
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
        catchup = "IESC需要披露更清晰的数据中心收入、客户PO、C&I backlog burn、Infrastructure标准化power block订单、分部margin和FCF conversion，并证明不可强制backlog能转为正式合同。"
        if row_obj["relationship"] == "上下游":
            catchup = "IESC需要证明云厂/IDC/AI主链capex能持续落到其低压通信、MEP和custom power订单，而不是只停留在行业TAM。"
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
        "- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/IESC_IES Holdings_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心开关设备与变压器_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心低压配电、PDU与母线槽_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_导管、桥架与线缆管理_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- IESC 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_iesc_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用正式评估最低分校准，对IESC的RPO/backlog、非住宅三分部、C&I 6-12个月转收入、Infrastructure custom power、Communications、住宅抵消、固定价项目和工作资本风险做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 IESC 正式评估文件")
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
                "iesc_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "iesc_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "iesc_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
