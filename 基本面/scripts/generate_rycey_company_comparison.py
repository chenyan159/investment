from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_nvt_company_comparison as nvt_ref


TARGET = "RYCEY"
TARGET_NAME = "Rolls-Royce Holdings"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "RYCEY_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_POWER_SYSTEMS_PEERS = {
    "BE",
    "CAT",
    "CMI",
    "GEV",
    "GNRC",
    "PSIX",
}

NUCLEAR_DEFENSE_AND_AEROSPACE_ADJACENT = {
    "BWXT",
    "CEG",
    "OKLO",
    "RKLB",
    "SMR",
    "TDY",
    "VST",
}

POWER_ELECTRICAL_ADJACENT = (
    set(getattr(nvt_ref, "POWER_ELECTRICAL_INFRA", set()))
    | set(getattr(nvt_ref, "INDUSTRIAL_AND_ENGINEERING_INFRA", set()))
    | {
        "AAON",
        "ABBNY",
        "AEIS",
        "ATKR",
        "CARR",
        "DKILY",
        "DOV",
        "EME",
        "ENS",
        "ENPH",
        "ETN",
        "FCEL",
        "FIX",
        "FLNC",
        "FTV",
        "HTHIY",
        "HUBB",
        "IESC",
        "JCI",
        "MIELY",
        "MOD",
        "MRAAY",
        "MYRG",
        "NVT",
        "PH",
        "PNR",
        "POWL",
        "PWR",
        "TT",
        "TTDKY",
        "VRT",
    }
) - {TARGET}

UTILITY_AND_POWER_CUSTOMERS = set(getattr(nvt_ref, "UTILITY_AND_POWER_CUSTOMERS", set())) | {
    "AEP",
    "DTE",
    "ET",
    "ETR",
}
DATA_CENTER_CUSTOMERS_AND_OPERATORS = set(getattr(nvt_ref, "DATA_CENTER_CUSTOMERS_AND_OPERATORS", set()))
SERVER_NETWORK_AND_AI_DEMAND_CHAIN = set(getattr(nvt_ref, "SERVER_NETWORK_AND_AI_DEMAND_CHAIN", set()))
SEMI_CHAIN = set(getattr(nvt_ref, "SEMI_CHAIN", set()))

DEMAND_CHAIN_CATS = {
    "AI服务器_存储_EMS",
    "AI网络_光互联_连接器",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "云算力_IDC_AI软件平台",
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
}

RYCEY_SCORES = {
    "NTM兑现优先": 84.0,
    "右尾弹性优先": 73.0,
    "风险调整收益": 70.0,
    "下行保护优先": 76.0,
    "估值消化优先": 57.0,
    "近端催化优先": 78.0,
    "价格确认/动量": 82.0,
    "激进短线": 64.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    nvt_ref.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in RYCEY_SCORES.items():
        target.setdefault("scores", {})[strategy] = score
    nvt_ref.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_POWER_SYSTEMS_PEERS:
        return "直接同业"
    if ticker in POWER_ELECTRICAL_ADJACENT or ticker in NUCLEAR_DEFENSE_AND_AEROSPACE_ADJACENT:
        return "相邻替代"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if ticker in UTILITY_AND_POWER_CUSTOMERS or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_NETWORK_AND_AI_DEMAND_CHAIN or ticker in SEMI_CHAIN:
        return "上下游"
    if category in DEMAND_CHAIN_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        return "业务差异大且档位接近" if rel == "跨赛道" else "证据互有强弱且档位接近"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "RYCEY有FY2026 UOP/FCF指引和backlog",
            "右尾弹性优先": "mtu数据中心电力/快启燃气/SMR仍有右尾",
            "风险调整收益": "Civil现金流、Defence backlog和净现金更均衡",
            "下行保护优先": "净现金、FCF和Civil/Defence底盘更抗压",
            "估值消化优先": "FY2026/2027利润与FCF可部分消化估值",
            "近端催化优先": "H1财报和Power Systems订单/backlog更近",
            "价格确认/动量": "6月价格继续上行且趋势确认更强",
            "激进短线": "AI电力、SMR和动量仍有进攻性",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}发电设备订单或交付更短链",
            "右尾弹性优先": f"{ticker}同业小基数或电力设备beta更高",
            "风险调整收益": f"{ticker}同业估值或利润捕获更优",
            "下行保护优先": f"{ticker}现金流、估值或压力期表现更稳",
            "估值消化优先": f"{ticker}设备收入更能覆盖估值",
            "近端催化优先": f"{ticker}订单/产能/客户催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}AI主链/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker}AI计算或客户侧利润池右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}产品、订单或财报催化更近",
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


def final_choice(row_obj: dict, a: dict, b: dict) -> str:
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
    if score > 0.15:
        return "A"
    if score < -0.15:
        return "B"

    tie_break = (
        (a.get("scores", {}).get("风险调整收益", 0) - b.get("scores", {}).get("风险调整收益", 0)) * 1.20
        + (a.get("scores", {}).get("NTM兑现优先", 0) - b.get("scores", {}).get("NTM兑现优先", 0)) * 0.90
        + (a.get("scores", {}).get("估值消化优先", 0) - b.get("scores", {}).get("估值消化优先", 0)) * 0.75
        + (a.get("scores", {}).get("下行保护优先", 0) - b.get("scores", {}).get("下行保护优先", 0)) * 0.55
    )
    return "A" if tie_break >= 0 else "B"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    rel = str(row_obj["relationship"])
    category = str(b.get("category", ""))
    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}

    if choice == "中性":
        return "RYCEY的兑现、现金流和动量优势与对手的增长、估值或右尾优势未拉开强判差距。"

    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "RYCEY有FY2026 UOP £4.0-4.2bn、FCF £3.6-3.8bn、NTM收入约£23.6-24.3bn和Civil/Defence/Power Systems多引擎支撑。"
        if diffs["下行保护优先"] > 10:
            return "RYCEY净现金、自由现金流、Civil售后服务和Defence backlog让下行保护优于对手。"
        if diffs["风险调整收益"] > 10:
            return "RYCEY的航空售后现金流、Defence backlog和数据中心电力增长构成更均衡赔率。"
        if diffs["价格确认/动量"] > 10:
            return "RYCEY从2026-06-03至2026-06-22继续上涨约11%，价格确认强于对手。"
        if diffs["近端催化优先"] > 10:
            return "RYCEY的H1 2026财报、Civil EFH/shop visits和Power Systems订单/backlog是更近端可验证催化。"
        return "RYCEY在兑现、现金流、订单能见度和价格确认上的综合证据足以压过B。"

    if rel == "上下游" or category in HIGH_GROWTH_CATS or category in DEMAND_CHAIN_CATS:
        if diffs["右尾弹性优先"] < -12:
            return f"{ticker}拥有更直接AI数据中心收入/利润池，RYCEY的AI暴露主要是电力设备和电源方案而非计算主链。"
        if diffs["NTM兑现优先"] < -12:
            return f"{ticker}的AI主链订单、RPO、客户兑现或收入确认比RYCEY更短链。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}用未来业绩消化当前估值的难度低于RYCEY。"
    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的小基数、AI主链或设备利润池右尾明显大于RYCEY。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和短线资金偏好明显强于RYCEY。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比RYCEY更直接。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或防御属性明显强于RYCEY。"
    return f"{ticker}在多数投资思路下比RYCEY更符合项目内资金配置目标。"


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
        row_obj["final_choice"] = final_choice(row_obj, a, b)
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


def fmt_iv(value) -> str:
    if value is None:
        return "缺失"
    return f"{fmt_num(value, 1)}%"


def majority_rows(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
    selected = [row for row in rows if row["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda x: (x["bc"] - x["ac"], x["bc"], -x["nc"]), reverse=True)
    else:
        selected.sort(key=lambda x: (x["ac"] - x["bc"], x["ac"], -x["nc"]), reverse=True)
    return selected[:limit]


def target_daily_snapshot(a: dict) -> str:
    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})
    price = fin.get("price")
    latest_close = m2w.get("latest_close")
    after_m2w = None
    if price and latest_close:
        after_m2w = (float(price) / float(latest_close) - 1.0) * 100
    return (
        f"2026-06-22 收盘价 {fmt_num(price, 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_iv(fin.get('call_iv'))}，"
        f"Put IV {fmt_iv(fin.get('put_iv'))}；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去一月 {fmt_pct(m1m.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}；"
        f"2026-06-22较2026-06-03收盘 {fmt_pct(after_m2w)}。"
    )


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin")])
    daily_snapshot = target_daily_snapshot(a)

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
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) or "无"

    support = {
        "NTM兑现优先": (
            "强势兑现档",
            "FY2026 underlying operating profit 指引 £4.0-4.2bn、FCF £3.6-3.8bn；NTM基准收入约£23.6-24.3bn，Civil services、Defence backlog和Power Systems共同支撑",
            "Power Systems订单到收入、Civil供应链/MRO/shop visits和客户验收仍决定兑现速度",
        ),
        "右尾弹性优先": (
            "中上右尾档",
            "mtu柴油/燃气发电机、20V4000 L64快启燃气、BESS/DRUPS/Kinetic PowerPack、SMR早期工作和数据中心time-to-power需求提供右尾",
            "RYCEY不是GPU、网络、内存、UPS或变压器主链；SMR/DRUPS不是NTM大收入贡献，基数也不小",
        ),
        "风险调整收益": (
            "中上到强势档",
            "净现金、强FCF、Civil售后服务、Defence backlog和Power Systems增长让上行与下行组合较均衡",
            "估值已反映较多转型和AI电力预期，且Power Systems data-center收入拆分不足",
        ),
        "下行保护优先": (
            "中上防守档",
            "FY2025净现金£1.895bn、FCF £3.270bn，FY2026 FCF指引£3.6-3.8bn；Civil/Defence现金流底盘较厚",
            "航空周期、发动机供应链、售后shop visit节奏和估值收缩仍会放大回撤",
        ),
        "估值消化优先": (
            "中档偏强",
            "FY2026/2027共识利润和FCF继续上行，能部分支撑Forward PE和EV/EBITDA",
            f"2026-06-22 Forward PE {fmt_num(a.get('fin', {}).get('forward_pe'), 2)}、P/S {fmt_num(a.get('fin', {}).get('ps'), 2)}、EV/EBITDA {fmt_num(a.get('fin', {}).get('ev_ebitda'), 2)}，估值已不便宜且ADR/币种口径需留意",
        ),
        "近端催化优先": (
            "强势近端档",
            "H1 2026 results在2026-07-30；Power Systems order intake/book-to-bill/backlog、20V4000 L64客户、Civil EFH/shop visits和Defence milestones可验证",
            "若数据中心订单只停留在pipeline、或Civil/Defence margin没有继续兑现，催化会被估值吸收",
        ),
        "价格确认/动量": (
            "强势动量档",
            f"2026-06-22收盘较2026-06-03收盘 {fmt_pct((a.get('fin', {}).get('price') / a.get('mom2', {}).get('latest_close') - 1) * 100 if a.get('fin', {}).get('price') and a.get('mom2', {}).get('latest_close') else None)}，6月价格继续确认转型和AI电力主题",
            f"2026-06-04三段SOXX压力窗口累计 {fmt_pct(a.get('soxx', {}).get('soxx_cum'))}，历史压力窗口不算顶级防守；上涨后更易受估值收缩影响",
        ),
        "激进短线": (
            "弱势短线档",
            "AI电力、自备发电、快启燃气、SMR和价格动量给短线进攻性",
            "Call/Put IV缺失，且大市值工业/航空属性让短线爆发力弱于光互联、核能开发、小盘电力设备和AI芯片链",
        ),
    }

    product_names = [
        "Civil Aerospace services/LTSA与OE",
        "Power Systems mtu柴油/燃气发电机和数据中心电力",
        "20V4000 L64 fast-start gas genset",
        "Defence航空、海军和陆用动力",
        "BESS/DRUPS/Kinetic PowerPack",
        "SMR早期开发与政府项目",
    ]

    lines: list[str] = [
        "# RYCEY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：RYCEY / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 RYCEY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。RYCEY 的优势集中在FY2026利润/FCF指引、Civil售后服务现金流、Defence backlog、Power Systems数据中心电力订单线索和6月价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值已较充分、不是AI计算主链或电气设备纯主链、SMR/DRUPS等右尾在NTM收入中还不能给高权重，且期权IV缺失降低短线定价信息。",
        "- A 最适合的投资者画像：想要配置AI数据中心电力与航空/国防高质量现金流交集、但不想完全承担芯片/光互联/小盘核能高beta的中期成长质量资金。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大右尾、小基数非线性、短线高波动或AI计算主链直接弹性的资金；这类资金通常会偏向NVDA、AVGO、MU、ALAB、CRDO、VRT、POWL、OKLO、SMR等。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常拥有更直接AI主链收入、更高设备利润池、更大右尾弹性、更强近端产品/订单催化或更低估值消化难度。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：RYCEY 是项目内偏强的工业/航空/国防/AI电力复合标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它明显强于许多低兑现、弱现金流或价格未确认公司，但面对顶级AI主链、电气设备OEM、小盘核能/电力高beta和部分平台龙头时必须按投资思路拆分。",
        "- 后续最重要跟踪数据：2026-07-30 H1业绩、Civil EFH/shop visits/LTSA margin、Power Systems order intake/book-to-bill/backlog/data-center revenue、20V4000 L64客户、BESS/DRUPS/Kinetic PowerPack订单、Defence milestones、SMR政府项目进度、FCF/net cash和估值倍数。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "RYCEY"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "电力_发电_能源_储能")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", "约£23.6-24.3bn；正式评估锚为NTM约£23.9bn"]),
        base.row(["乐观/极度乐观收入", "乐观：£24.6-25.8bn；极度乐观：£26.0-27.5bn"]),
        base.row(["利润和现金流结论", "FY2026 UOP指引£4.0-4.2bn、FCF £3.6-3.8bn；NTM基准UOP/EBIT约£4.35-4.60bn、FCF约£4.09bn；FY2025净现金£1.895bn。"]),
        base.row(["最大传导瓶颈", "Power Systems订单到收入转换、数据中心客户NTP/许可/燃气连接/commissioning、Civil供应链/MRO/shop visits和客户多供应商策略。"]),
        base.row(["最大反证", "估值已高，RYCEY不是纯AI主链；Power Systems data-center收入拆分不足，SMR/DRUPS不是NTM大收入贡献，Civil和Defence仍有执行/供应链风险。"]),
        base.row(["近端催化剂", "2026-07-30 H1财报；Power Systems order intake/book-to-bill/backlog/data-center revenue；20V4000 L64客户；Civil EFH/shop visits/AOG/LTSA；Defence milestones；BESS/SMR早期进展。"]),
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
        base.row(["直接同业", "与RYCEY在数据中心自备电力、发电设备、燃气/柴油机组、分布式发电或电力设备需求池上直接重叠；优先比较订单、backlog、交付、利润率、服务收入和同业估值。", "BE、CAT、CMI、GEV、GNRC、PSIX", "判断力度最高；同档或相邻档时必须复核谁真正把同一time-to-power需求转成收入和FCF。"]),
        base.row(["相邻替代", "同属AI园区电力、冷却、核能、储能、工程交付、国防/航天或工业基础设施资金篮子，但产品或收入模式不完全相同。", "ETN、HUBB、NVT、POWL、VRT、MOD、JCI、BWXT、CEG、OKLO、SMR、PWR", "回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好；不因赛道更热自动胜出。"]),
        base.row(["上下游", "B是RYCEY数据中心电力需求的云厂/IDC/服务器/芯片/网络客户链、半导体供给链或公用事业/能源需求端。", "MSFT、AMZN、GOOGL、META、ORCL、NVDA、AVGO、DELL、ANET、AEP、ETR", "不把客户capex直接等同RYCEY利润，也不把芯片/服务器高增速直接等同RYCEY机会；核心看利润捕获、订单硬度和传导链长度。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "材料、化学品、软件、生命科学、消费电子和部分平台公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        catchup = "RYCEY需要证明Power Systems数据中心订单、Civil利润率、Defence backlog和FCF可以继续超预期，并降低估值透支风险。"
        if row_obj["relationship"] == "直接同业":
            catchup = "RYCEY需要在直接发电/电力设备同业中证明订单、backlog、data-center revenue、margin和服务现金流明显强于B。"
        elif row_obj["relationship"] == "上下游":
            catchup = "RYCEY需要证明云厂/AI主链capex会持续落到其发电机组、BESS/DRUPS和Power Systems收入利润，而不只是行业TAM。"
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
        "- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/RYCEY_Rolls-Royce_Holdings_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_动态UPS、飞轮与超级电容_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- RYCEY 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_rycey_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的使用既有正式脚本的最低分校准，对RYCEY的FY2026 UOP/FCF指引、Civil/Defence/Power Systems、数据中心电力、20V4000 L64、SMR/BESS/DRUPS、估值、IV缺失、价格确认和非纯AI主链限制做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
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
        raise SystemExit("缺少 RYCEY 正式评估文件")
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
                "rycey_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "rycey_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "rycey_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
