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


TARGET = "IFNNY"
TARGET_NAME = "Infineon Technologies AG 英飞凌科技"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "IFNNY_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_POWER_SEMI_PEERS = {
    "ADI",
    "AOSL",
    "DIOD",
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

ADJACENT_POWER_AND_ELECTRICAL = {
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

AI_POWER_DEMAND_CHAIN = {
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
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GOOGL",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "META",
    "MRVL",
    "MTSI",
    "MU",
    "NBIS",
    "NOK",
    "NTAP",
    "NVDA",
    "ORCL",
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
    "CDNS",
    "COHU",
    "DSCSY",
    "ENTG",
    "FORM",
    "GFS",
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "SHECY",
    "SNPS",
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
    "APLD",
    "BWXT",
    "CEG",
    "CMI",
    "CRWV",
    "DTE",
    "ET",
    "ETR",
    "FCEL",
    "HTHIY",
    "IREN",
    "OKLO",
    "PWR",
    "RYCEY",
    "SMR",
    "VST",
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

# The generic parser reads ranges such as "+11-16%" as a negative value.
# These scores anchor IFNNY to the formal evaluation: AI power has hard
# FY2026/FY2027 revenue targets and PSS proof, while automotive/industrial
# cyclicality, valuation and missing option-chain data cap the top-down score.
IFNNY_SCORES = {
    "NTM兑现优先": 73.0,
    "右尾弹性优先": 73.5,
    "风险调整收益": 57.0,
    "下行保护优先": 68.0,
    "估值消化优先": 55.0,
    "近端催化优先": 70.0,
    "价格确认/动量": 84.0,
    "激进短线": 82.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for floorset in (project_calibration.SCORE_FLOORS, etn_calibration.LOCAL_SCORE_FLOORS):
        for ticker, floors in floorset.items():
            company = companies.get(ticker)
            if not company:
                continue
            for strategy, floor in floors.items():
                current = company.setdefault("scores", {}).get(strategy, 0)
                company["scores"][strategy] = max(current, floor)

    if "ETN" in companies:
        companies["ETN"].setdefault("scores", {}).update(etn_calibration.ETN_SCORES)
    if "HUBB" in companies:
        companies["HUBB"].setdefault("scores", {}).update(hubb_calibration.HUBB_SCORES)

    for strategy, score in IFNNY_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    etn_calibration.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_POWER_SEMI_PEERS:
        return "直接同业"
    if ticker in ADJACENT_POWER_AND_ELECTRICAL or ticker in INDUSTRIAL_INFRA:
        return "相邻替代"
    if ticker in AI_POWER_DEMAND_CHAIN or ticker in UTILITY_AND_CAMPUS_POWER or ticker in FABS_EQUIPMENT_AND_MATERIALS:
        return "上下游"
    if category in {"配电_电源_功率器件"}:
        return "直接同业"
    if category in {"电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "跨赛道":
            return "业务差异大且证据互抵"
        if rel == "直接同业":
            return "同业证据接近需等订单和利润验证"
        return "证据互有强弱且档位接近"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "IFNNY有AI power目标、PSS增长和EUR25B backlog",
            "右尾弹性优先": "IFNNY的800V/BBU/TLVR右尾可收入化",
            "风险调整收益": "IFNNY增长锚、现金流和反证更均衡",
            "下行保护优先": "IFNNY多元车规/功率底盘和FCF更稳",
            "估值消化优先": "IFNNY可用AI power和利润恢复消化估值",
            "近端催化优先": "IFNNY有Q3、PSS、30kW PSU和800V验证",
            "价格确认/动量": "IFNNY六月价格确认显著强于对手",
            "激进短线": "IFNNY AI power叙事和价格弹性更适合进攻",
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
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
    elif rel == "直接同业":
        strong_cut, suggest_cut, micro_cut = 19, 9, 4
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
        return "IFNNY的AI power收入锚与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "IFNNY有FY2026/FY2027 AI power目标、PSS高增和集团backlog支撑NTM兑现。"
        if diffs["近端催化优先"] > 10:
            return "IFNNY的PSS收入、Q3指引、30kW PSU、800V/HV IBC和BBU验证更近。"
        if diffs["价格确认/动量"] > 12:
            return "IFNNY 6月价格确认强，市场已经开始验证AI power重估逻辑。"
        if diffs["风险调整收益"] > 10:
            return "IFNNY在AI power增长、现金流和汽车/工业反证之间的风险调整组合更均衡。"
        return "IFNNY的功率半导体平台、AI power目标和现金流底盘比对手更适合该口径。"

    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于IFNNY。"
    if diffs["下行保护优先"] < -14:
        return f"{ticker}的现金流、资产质量或压力期表现比IFNNY更安全。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或估值消化空间优于IFNNY。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比IFNNY更硬。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比IFNNY更直接。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和资金偏好明显强于IFNNY。"
    return f"{ticker}在多数投资思路下比IFNNY更符合项目内资金配置目标。"


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
    missing_price = sorted([ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price")])
    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})

    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去一月 {fmt_pct(m1m.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}；"
        f"2026-06-22收盘较2026-06-03收盘 {fmt_pct(((fin.get('price') or 0) / (m2w.get('latest_close') or 1) - 1) * 100 if fin.get('price') and m2w.get('latest_close') else None)}。"
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
            "FY2026 AI power目标约EUR1.5B、FY2027约EUR2.5B，FY2026 Q2 PSS收入EUR1.260B且同比+26%，集团backlog约EUR25B",
            "ATV仍接近半数收入且EV高压业务/工业周期拖累；AI客户、产品级backlog和份额未披露",
        ),
        "右尾弹性优先": (
            "A",
            "强势档",
            "800VDC/HV IBC、48/50V VR/TLVR/PoL、eFuse/hot-swap、BBU/energy shelf、30kW PSU和CoolGaN/CoolSiC构成AI power非线性右尾",
            "公司基数大且不是纯AI公司；800VDC大规模量产更偏2027以后，NTM内不能把长期TAM提前收入化",
        ),
        "风险调整收益": (
            "A",
            "中上档",
            "AI power已有收入目标、PSS利润率改善、集团FCF指引约EUR1.25B/调整后EUR1.65B，业务不是纯题材",
            "2026-06-22 Forward PE 32.17、P/S 8.52且P/S受USD/EUR口径标记bad；汽车/工业反证会抵消AI上行",
        ),
        "下行保护优先": (
            "C",
            "中性偏弱档",
            "车规功率、工业功率、PSS和CSS多元化，净债务/权益约33%，不是融资困境公司",
            "SOXX压力窗口累计-66.26%，估值已给AI power溢价，且OTC无干净IV数据；防守性弱于公用事业/软件现金流龙头",
        ),
        "估值消化优先": (
            "B",
            "中上档",
            "NTM基准收入EUR16.8-17.6B、Segment Result Margin 18-21%，若AI power按FY2027目标推进可消化部分估值",
            "TTM PE 104.35、Forward PE 32.17、EV/EBITDA 32.34，估值已经要求PSS和利润率持续兑现",
        ),
        "近端催化优先": (
            "A",
            "强势档",
            "FY2026 Q3指引、FY2026H2 AI power目标、PSS收入/margin、30kW PSU、HV IBC、XDPP1188、eFuse/BBU客户验证均可在1-2个季度内跟踪",
            "公司不披露产品级AI订单，近端催化更可能是目标维持/上修和PSS继续高增，而非单个大客户订单",
        ),
        "价格确认/动量": (
            "A",
            "强势档",
            "2026-06-03过去两周+27.32%、过去一月+51.27%，2026-06-22收盘99.13仅较6月初101.73回落约2.56%",
            "动量数据来自6月初区间，6/22之后仍需确认；OTC ADR无干净期权链，短线资金工具受限",
        ),
        "激进短线": (
            "B",
            "中上档",
            "AI power、800VDC、30kW PSU、BBU、机器人安全MCU/传感器和强价格确认提供进攻入口",
            "缺少Call IV，且大盘欧洲功率半导体龙头短线爆发力弱于小基数NeoCloud、光互联、内存和核能开发标的",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "Automotive/ATV",
            "PSS AI power",
            "AI PSU/PFC/power shelf",
            "48/50V DC/DC、VR/TLVR/PoL、eFuse",
            "BBU/energy shelf",
            "800VDC/HV IBC/CoolGaN",
            "GIP工业/能源功率",
        ]

    lines: list[str] = [
        "# IFNNY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：IFNNY / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 IFNNY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。IFNNY 的增速区间因通用解析器会误读 `+11-16%` 一类区间，已按正式评估中的 FY2026/FY2027 AI power、PSS、backlog、估值和动量证据做目标公司校准。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。IFNNY 的优势集中在 FY2026/FY2027 AI power 明确收入目标、PSS 高增、800VDC/HV IBC、VR/TLVR/eFuse、BBU、30kW PSU 以及 6 月价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是汽车/工业周期仍拖累集团利润，AI客户和产品级backlog未披露，估值已经给AI power较高溢价，SOXX压力窗口表现偏弱且OTC期权IV缺失。",
        "- A 最适合的投资者画像：想配置 AI 数据中心电源半导体和控制层，但又不想买纯亏损小盘或系统设备高 beta 的资金；适合作为 AI power / 功率半导体平台型仓位，而不是纯防守仓位。",
        "- A 最不适合的投资者画像：只追求最高短线爆发、最强右尾或最厚下行保护的资金。前者通常更偏 NVDA/MU/AVGO/ALAB/CRDO/NBIS/CRWV/OKLO/SMR，后者通常更偏 MSFT/AMZN/公用事业或低IV现金流资产。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常拥有更直接AI主链收入、更硬订单/RPO/backlog、更低估值消化压力或更强下行保护。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：IFNNY 是项目内偏强的AI power半导体受益者，但不是全项目顶级强者；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。它明显强于许多周期弱、现金流差或AI收入不清晰的标的，但面对NVDA/AVGO/MU/TSM/ORCL/ETN/VRT/POWL/GEV等顶级AI主链或电力设备标的时，需要按投资思路拆分。",
        "- 后续最重要跟踪数据：FY2026 Q3/Q4 PSS收入和margin、FY2026 AI power EUR1.5B与FY2027 EUR2.5B目标是否维持或上修、30kW PSU与HV IBC客户量产、TLVR/eFuse/BBU attach、800VDC定点、集团backlog结构、ATV margin、GIP恢复、库存周转、capex与FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "IFNNY"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "配电_电源_功率器件")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "`EUR16.8-17.6B`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or 'EUR18.2-19.2B'}；极度乐观：{a.get('extreme_rev') or 'EUR20.0-22.0B'}"]),
        base.row(["利润和现金流结论", f"基准利润：{a.get('base_profit') or '净利润约EUR1.6-2.1B'}；基准利润率：{a.get('base_margin') or 'Segment Result Margin 18-21%'}；现金流：{a.get('base_cash') or 'FCF约EUR1.2-1.7B，调整后FCF接近或略高于FY2026指引'}。"]),
        base.row(["最大传导瓶颈", "公司只披露AI power年度目标和PSS分部数据，不披露AI客户、产品级backlog、设计份额或每类产品收入；同时ATV汽车半导体仍接近半数收入。"]),
        base.row(["最大反证", "ATV高压e-mobility价格/库存、工业周期、800VDC/BBU客户认证延迟、AI客户透明度不足、FY2026 capex EUR2.7B和FCF兑现压力。"]),
        base.row(["近端催化剂", "FY2026 Q3/Q4 PSS收入和margin、AI power目标维持或上修、30kW PSU/18kW PSU、HV IBC、XDPP1188、TLVR/eFuse/BBU客户验证、Siemens SiC断路器商业化。"]),
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
        base.row(["直接同业", "同属功率半导体、模拟/电源管理、车规/工业功率、GaN/SiC/MOSFET、VR/PoL、eFuse、MCU/传感或高压保护供应商；优先比较PSS/功率收入、design win、产品代际、毛利率、估值和客户认证。", "ON、STM、TXN、ADI、MPWR、POWI、NVTS、WOLF、VICR、MRAAY、TTDKY、DIOD", "判断力度最高；若同业在AI PSU、VR/TLVR、GaN/SiC、客户定点或估值消化上明显胜出，相关列可以压过IFNNY。"]),
        base.row(["相邻替代", "同属AI电力、配电、电源、UPS/BBU、数据中心电气设备、工业电气或冷却/工程资金篮子，但一方卖系统/工程、一方卖半导体。", "ETN、HUBB、POWL、VRT、GEV、ABBNY、NVT、BE、ENS、FLNC、AAON、TT", "中等力度；不能把系统商订单直接等同为IFNNY收入，也不能把半导体小器件稀缺直接等同为更好，需看利润捕获和估值。"]),
        base.row(["上下游", "AI芯片、服务器、网络、云厂、IDC、公用事业、晶圆制造/设备/材料均处在IFNNY需求链或供给链附近；比较利润池位置、客户预算、议价权、订单/RPO和资本开支风险。", "NVDA、AVGO、MU、DELL、HPE、SMCI、CRWV、MSFT、ORCL、TSM、ASML、AMAT、CEG、AEP", "上游或下游不能机械胜出；若对方拥有更直接AI收入或更硬RPO/backlog，会在NTM、右尾、近端催化和价格确认列胜出。"]),
        base.row(["跨赛道", "软件、材料、医疗仪器、普通工业、化工和其他与IFNNY业务差异大的项目内配置替代。", "ADBE、TMO、ECL、DHR、CAT、RKLB、LIN", "默认降低结论力度；除非增长、估值、防守或动量明显拉开，否则用中性或微倾向。"]),
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
        catchup = "IFNNY需要披露更清晰的AI power客户/产品级backlog、PSS收入和margin上修、800V/HV IBC或BBU量产定点，并让ATV/GIP反证消退。"
        if row_obj["relationship"] == "直接同业":
            catchup = "IFNNY需要证明其AI PSU、VR/TLVR、eFuse、GaN/SiC和800V方案在同业中拿到更高份额、毛利或客户认证。"
        elif row_obj["relationship"] == "上下游":
            catchup = "IFNNY需要证明下游AI capex能持续转成自己的功率半导体收入，而不是只停留在系统或客户预算层。"
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
        catchup = "B需要拿出更硬的NTM收入/利润兑现、订单或客户合同，并证明估值、现金流和压力窗口能承受波动。"
        if row_obj["relationship"] == "直接同业":
            catchup = "B需要在AI PSU、VR/TLVR、GaN/SiC、eFuse或800V客户认证中显示强于IFNNY的份额和利润证据。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/配电_电源_功率器件/IFNNY_Infineon_Technologies_AG_英飞凌科技_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；有明细行公司 {len(companies) - len(missing_fin)}/{len(companies)} 家，价格缺失或无明细的公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 外部官方核验来源：Infineon FY2026 Q2 press release and financial tables（https://www.infineon.com/assets/row/public/documents/corporate/press/2026/infxx202605-082e.pdf）；Infineon FY2026 Q2 analyst call presentation（https://www.infineon.com/content/dam/infineon/row/public/documents/corporate/investors/presentations/2026/2026-05-05-q2-fy26-analyst-call-v01-00-en.pdf）；Infineon data center power solutions（https://www.infineon.com/applications/ai-data-center/data-center-power-solutions）；Infineon We Power AI（https://www.infineon.com/technology/ai/we-power-ai）；Infineon 800VDC/HV IBC reference designs（2026-03-17，https://www.infineon.com/technology-news/2026/infpss202603-067）；Infineon XDPP1188-200C controller（2026-03-17，https://www.infineon.com/market-news/2026/infpss202603-068）；Infineon 18kW/30kW AI data center PSU solutions（2026-06-02，https://www.infineon.com/market-news/2026/infpss202606-094）。",
        f"- IFNNY 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_ifnny_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用正式评估最低分校准，并对IFNNY的AI power官方收入目标、PSS增长、800V/BBU/VR产品证据、估值、压力窗口和IV缺失做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 IFNNY 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8", newline="\n")
    a = companies[TARGET]
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "ifnny_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "ifnny_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "ifnny_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
