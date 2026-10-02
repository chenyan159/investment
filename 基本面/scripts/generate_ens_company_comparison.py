from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "ENS"
TARGET_NAME = "EnerSys"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ENS_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_BATTERY_STORAGE = {
    "AMPX",
    "ENPH",
    "FLNC",
    "GNRC",
    "PSIX",
}

POWER_ELECTRICAL_ADJACENT = {
    "AEP",
    "ABBNY",
    "AEIS",
    "ATKR",
    "BE",
    "BWXT",
    "CEG",
    "CMI",
    "DTE",
    "ET",
    "ETN",
    "ETR",
    "FCEL",
    "GEV",
    "HUBB",
    "HTHIY",
    "IFNNY",
    "LFUS",
    "MIELY",
    "MPWR",
    "MRAAY",
    "NVT",
    "NVTS",
    "OKLO",
    "POWI",
    "POWL",
    "PWR",
    "RYCEY",
    "SMR",
    "ST",
    "TTDKY",
    "VICR",
    "VRT",
    "VSH",
    "VST",
    "WOLF",
}

INDUSTRIAL_ADJACENT = {
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

DATA_CENTER_UPSTREAM_DOWNSTREAM = {
    "AAOI",
    "ADBE",
    "ALAB",
    "AMD",
    "AMZN",
    "ANET",
    "APH",
    "APLD",
    "ARM",
    "AVGO",
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
    "MRVL",
    "MSFT",
    "MTSI",
    "MU",
    "NBIS",
    "NOK",
    "NTAP",
    "NTNX",
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
    "TSLA",
    "VIAV",
    "VISN",
    "WDC",
}

LOCAL_SCORE_FLOORS = {
    # CEG's own target overrides are not part of calibrated.SCORE_FLOORS.
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
    # Keep major already-calibrated power/engineering comparables from being
    # understated by generic percentage parsing.
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

ENS_SCORES = {
    "NTM兑现优先": 68.0,
    "右尾弹性优先": 59.0,
    "风险调整收益": 63.0,
    "下行保护优先": 83.0,
    "估值消化优先": 71.0,
    "近端催化优先": 67.0,
    "价格确认/动量": 67.0,
    "激进短线": 76.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in {**calibrated.SCORE_FLOORS, **LOCAL_SCORE_FLOORS}.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strat, floor in floors.items():
            current = company.setdefault("scores", {}).get(strat, 0)
            company["scores"][strat] = max(current, floor)

    for strat, score in ENS_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strat] = score

    recompute_tiers(companies)


def recompute_tiers(companies: dict[str, dict]) -> None:
    for strat in STRATS:
        scored = [
            company.get("scores", {}).get(strat)
            for company in companies.values()
            if company.get("scores", {}).get(strat) is not None
        ]
        scored.sort(reverse=True)
        total = len(scored)
        if not total:
            continue
        cuts = {
            "S": scored[max(0, int(total * 0.08) - 1)],
            "A": scored[max(0, int(total * 0.25) - 1)],
            "B": scored[max(0, int(total * 0.55) - 1)],
            "C": scored[max(0, int(total * 0.80) - 1)],
        }
        for company in companies.values():
            score = company.get("scores", {}).get(strat)
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
            company.setdefault("tiers", {})[strat] = tier
            company.setdefault("ranks", {})[strat] = rank
            company.setdefault("rank_total", {})[strat] = total

    for company in companies.values():
        if not company.get("fin", {}).get("price"):
            for strat in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strat] = "资料不足"
                company.setdefault("ranks", {})[strat] = None


def relationship(company: dict) -> str:
    ticker = company["ticker"]
    category = company.get("category", "")
    if ticker in DIRECT_BATTERY_STORAGE:
        return "直接同业"
    if ticker in POWER_ELECTRICAL_ADJACENT or ticker in INDUSTRIAL_ADJACENT:
        return "相邻替代"
    if ticker in DATA_CENTER_UPSTREAM_DOWNSTREAM:
        return "上下游"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {
        "AI服务器_存储_EMS",
        "AI网络_光互联_连接器",
        "AI计算芯片_EDA_IP_custom_ASIC",
        "云算力_IDC_AI软件平台",
    }:
        return "上下游"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict) -> str:
    ticker = company["ticker"]
    category = company.get("category", "")
    rel = relationship(company)
    if winner == "A":
        return {
            "NTM兑现优先": "A有Q1指引、NIS/PPS订单和FCF支撑",
            "右尾弹性优先": "A有DataSafe Noir与PPS可验证右尾",
            "风险调整收益": "A低估值、强FCF和订单证据更均衡",
            "下行保护优先": "A低P/S、FCF和压力窗口更稳",
            "估值消化优先": "A约17x远期PE和2.3x P/S更易消化",
            "近端催化优先": "A有新品、FYQ1和PPS订单节点",
            "价格确认/动量": "A两周/一月价格已确认",
            "激进短线": "A高IV叠加新品和国防订单催化",
        }[strat]
    if winner == "B":
        if rel == "直接同业":
            return {
                "NTM兑现优先": "B同类储能/电源兑现链条更清楚",
                "右尾弹性优先": "B同类小基数或储能右尾更大",
                "风险调整收益": "B同业上行和风险组合更优",
                "下行保护优先": "B同业现金流或估值缓冲更好",
                "估值消化优先": "B同业增长更能消化估值",
                "近端催化优先": "B同业订单或认证催化更近",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业波动和主题beta更强",
            }[strat]
        if category in HIGH_GROWTH_CATS or ticker in DATA_CENTER_UPSTREAM_DOWNSTREAM:
            return {
                "NTM兑现优先": "B AI主链订单/RPO兑现更短链",
                "右尾弹性优先": "B AI主链右尾和收入弹性更大",
                "风险调整收益": "B上行空间更能覆盖执行风险",
                "下行保护优先": "B需求能见度或现金流韧性更好",
                "估值消化优先": "B高速增长更能消化高倍数",
                "近端催化优先": "B产品/订单/财报催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta和AI关注度更适合进攻",
            }[strat]
        if category in INFRA_CATS or rel == "相邻替代":
            return {
                "NTM兑现优先": "B订单、backlog或交付路径更清楚",
                "右尾弹性优先": "B电力/设备/工程右尾更直接",
                "风险调整收益": "B增长和估值组合更优",
                "下行保护优先": "B现金流、防御性或压力表现更好",
                "估值消化优先": "B用订单兑现消化估值更容易",
                "近端催化优先": "B订单/产能/财报催化更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化或AI设施交易弹性更强",
            }[strat]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景上行更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量或估值缓冲更好",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线波动和关注度更适合进攻",
        }[strat]
    return {
        "NTM兑现优先": "NTM证据接近",
        "右尾弹性优先": "右尾证据互有强弱",
        "风险调整收益": "赔率和风险接近",
        "下行保护优先": "防守证据接近",
        "估值消化优先": "估值消化差距不大",
        "近端催化优先": "近端催化强度接近",
        "价格确认/动量": "价格确认差距有限",
        "激进短线": "短线弹性差距有限",
    }[strat]


def label_for(strat: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strat, "资料不足")
    bt = b.get("tiers", {}).get(strat, "资料不足")
    if "资料不足" in (at, bt):
        return "中性"

    diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"
    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 25, 12, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 22, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 19, 9, 4

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


def cell_for(strat: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strat, a, b, rel)
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strat, winner, b)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strat in STRATS if "投A" in row_obj[strat])
    b_count = sum(1 for strat in STRATS if "投B" in row_obj[strat])
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.15,
        "估值消化优先": 1.05,
        "下行保护优先": 0.95,
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
    for strat in STRATS:
        label = base.tag_in_cell(row_obj[strat])
        score += weights[strat] * label_score.get(label, 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = b["ticker"]
    if choice == "中性":
        return "两家公司风格差异较大，ENS的低估值/现金流与对手的增长或催化证据未拉开强判差距。"

    diffs = {strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0) for strat in STRATS}
    if choice == "A":
        if diffs["下行保护优先"] > 12:
            return "ENS 的低P/S、强自由现金流和SOXX压力窗口韧性提供更好下行保护。"
        if diffs["估值消化优先"] > 12:
            return "ENS 的约17x远期PE、2.3x P/S和中高可信度基准收入更容易消化估值。"
        if diffs["风险调整收益"] > 10:
            return "ENS 在数据中心UPS/PPS订单、现金流和估值之间的风险调整组合更均衡。"
        if diffs["NTM兑现优先"] > 10:
            return "ENS 的FY2027 Q1指引、NIS/PPS订单和分部收入底盘使NTM兑现更清楚。"
        return "ENS 的DataSafe Noir、PPS高可靠电源、低估值和FCF底盘比对手更适合该口径。"

    if diffs["右尾弹性优先"] < -18:
        return f"{ticker} 的AI主链、核电/电气设备或小基数右尾明显大于ENS。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker} 的订单、RPO、backlog或收入确认证据比ENS更硬。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker} 未来1-2个季度的订单、产品或财报催化更直接。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker} 当前估值更容易被未来业绩消化，ENS仍需证明新品和PPS放量。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker} 的价格确认和资金偏好明显强于ENS。"
    return f"{ticker} 在增长质量、催化或资金偏好上更符合项目内配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) > tier_value(b.get("tiers", {}).get(s))]
    b_strong = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) < tier_value(b.get("tiers", {}).get(s))]
    close = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) == tier_value(b.get("tiers", {}).get(s))]
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
            "classification": base.category_short(b.get("category", "")),
            "relationship": rel,
            "grade_diff": grade_diff_summary(a, b),
        }
        for strat in STRATS:
            row_obj[strat] = cell_for(strat, a, b, rel)
        ac, bc, nc = direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        choice = final_choice(row_obj)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, row_obj, choice)
        rows.append(row_obj)

    def sort_key(item: dict) -> tuple[int, str]:
        rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
        return (rel_order.get(item["relationship"], 9), item["ticker"])

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


def majority(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
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

    stats: dict[str, Counter] = {strat: Counter() for strat in STRATS}
    for row_obj in comparisons:
        for strat in STRATS:
            stats[strat][base.tag_in_cell(row_obj[strat])] += 1

    strong_b = majority(comparisons, "B", 45)
    strong_a = majority(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b

    lines: list[str] = []
    lines.append("# ENS 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append("公司 A：ENS / EnerSys")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(comparisons)}")
    lines.append(f"公司评估文件日期范围：{date_range}")
    lines.append("日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 压力窗口")
    lines.append("")
    lines.append("> 口径说明：正式生成脚本只使用公司评估、公司调研、行业调研和金融资料等上游资料；未将 `特征量化/`、公司排序结果、备份目录或临时结果作为资料来源，也未引用或继承其结论。每一行是 ENS 与一家项目内公司 B 的二选一判断。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append("- A 最占优的投资思路：`下行保护优先`、`估值消化优先` 和 `风险调整收益`。ENS 有 FY2026 FCF 4.68 亿美元、Forward PE 17.34、P/S 2.27、SOXX 压力窗口累计 -18.82% 和 FY2027 Q1 指引作底盘。")
    lines.append("- A 最吃亏的投资思路：`右尾弹性优先` 和 `激进短线`。DataSafe Noir、PPS 军工电源和数据中心 UPS 有右尾，但 NTM 内仍受客户验证、项目交付、IMS 周期和 FY2028 后放量节奏约束。")
    lines.append("- A 最适合的投资者画像：想配置 AI 数据中心供电/电池环节，但更重视估值、现金流、订单证据和下行保护的中等进攻型资金。")
    lines.append("- A 最不适合的投资者画像：只追求最高 AI 主链 beta、最快收入翻倍、核电/NeoCloud/光互联极端弹性或纯动量交易的资金。")
    lines.append("- 多数思路下最强反方公司：" + "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:8]]) + "。")
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：ENS 是项目内中上偏强的低估值现金流型 AI 电力/电池配套标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。")
    lines.append("- 后续最重要跟踪数据：FY2027 Q1/Q2 revenue、NIS revenue 与 margin、data center orders、DataSafe Noir 客户/OEM/hyperscaler 认证、PPS book-to-bill、liquid reserve/thermal batteries 收入、IMS order/revenue/mix、45X benefit、ex-45X adjusted EPS、经营现金流、库存/应收、capex 和 Greenville 工厂进展。")
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | ENS |")
    lines.append("| 公司名称 | EnerSys |")
    lines.append(f"| 产业链分类 | {a.get('category', '电力_发电_能源_储能')} |")
    lines.append("| 重要产品/业务线 | NIS 数据中心 UPS/TPPL/DataSafe/DataSafe Noir、通信/工业后备电源；IMS 物料搬运和交通动力电池；PPS 国防/航天/弹药/士兵电源；仓储/工业 BESS 作为小额期权 |")
    lines.append("| NTM 基准收入 | 评估文件基准情景 `$3.85-4.05B`，相当于 FY2026 `$3.751B` 上低到中个位数增长 |")
    lines.append("| 乐观/极度乐观收入 | 乐观 `$4.10-4.35B`；极度乐观 `$4.45-4.80B`，需要 DataSafe Noir、传统数据中心、PPS 与 IMS 周期修复同时成立 |")
    lines.append("| 利润和现金流结论 | 基准调整后 EBITDA `$610-690M`、净利润 `$310-390M`、FCF `$350-480M`；FY2026 FCF `$468M` 和 159% 转换率不能机械外推，但正常化后仍强 |")
    lines.append("| 最大传导瓶颈 | 数据中心订单 `+36% YoY` 不能直接等同收入，仍受 UPS/OEM handoff、客户验证、通信接口、site commissioning、项目交付和电力建设节奏约束 |")
    lines.append("| 最大反证 | DataSafe Noir meaningful revenue lift 更偏 FY2028；DataSafe Noir/BESS 缺量化客户和收入指引；IMS 依赖工业/仓储 capex，45X 抬高利润但非经营需求本身 |")
    lines.append("| 近端催化剂 | FY2027 Q1/Q2 revenue、NIS margin、data center orders、DataSafe Noir 认证/客户披露、PPS book-to-bill/liquid reserve/thermal battery 收入、IMS 订单修复和 45X/ex-45X EPS |")
    lines.append("| 日度数据 | " + daily_snapshot + " |")
    lines.append("")
    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    support = {
        "NTM兑现优先": ("A", "中上偏强", "FY2027 Q1 收入 `$915-955M`、FY2026 收入 `$3.751B`、NIS/PPS订单和FCF提供硬锚", "公司未给FY2027全年收入指引，数据中心订单到收入仍需项目交付"),
        "右尾弹性优先": ("B", "中上但非顶级", "DataSafe Noir、PPS高可靠电源、数据中心UPS和Greenville锂电工厂提供期权", "极度乐观需多环节同时成立，DataSafe Noir大规模收入更偏FY2028"),
        "风险调整收益": ("A", "强势档", "低估值、强FCF、PPS/NIS订单和SOXX压力窗口韧性组合较均衡", "45X质量折扣、IMS周期和项目制营运资本会压低赔率"),
        "下行保护优先": ("A", "强势档", "FY2026 FCF `$468M`、Forward PE 17.34、P/S 2.27、SOXX三段累计仅 -18.82%", "Call IV 48.6%并不低，普通工业需求和项目制交付仍有波动"),
        "估值消化优先": ("A", "强势档", "约17x远期PE、2.27x P/S、基准EBITDA `$610-690M` 和FCF可支撑估值", "若DataSafe/PPS不能放量，估值重估空间有限"),
        "近端催化优先": ("A", "偏强", "DataSafe Noir发布、FY2027 Q1/Q2、PPS book-to-bill和NIS订单均有1-2季度跟踪点", "新品认证和客户披露可能慢，重大收入更依赖后续季度"),
        "价格确认/动量": ("B", "中上", "2026-06-03两周 +11.92%、一月 +13.07%，价格已对新品/电力主题作出确认", "截至2026-06-22较6月初回落，动量弱于高beta AI主链"),
        "激进短线": ("C", "偏弱到中性", "Call IV 48.6%、DataSafe Noir和国防电源新闻流可支持事件交易", "市值和业务底盘较成熟，短线爆发力弱于NeoCloud、核能开发和光互联高beta"),
    }
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in STRATS:
        tier = a.get("tiers", {}).get(strat, "资料不足")
        position = f"{support[strat][1]}；评分排名 {a.get('ranks', {}).get(strat)}/{a.get('rank_total', {}).get(strat)}"
        lines.append(f"| {strat} | {tier} | {position} | {support[strat][2]} | {support[strat][3]} |")
    lines.append("")
    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 作为电池、储能、后备电源和分布式能源设备比较，优先看订单、收入确认、客户验证、毛利率、现金流和估值 | AMPX、ENPH、FLNC、GNRC、PSIX | 判断力度较高；若一方订单或收入转化明显更硬，可以给建议或强烈建议 |")
    lines.append("| 相邻替代 | 作为AI电力、配电、电源、冷却、工程、电气设备和工业设施资金篮子二选一，重点比较增长质量、订单、估值和催化 | VRT、ETN、POWL、HUBB、GEV、PWR、AAON、TT、EME | 保持中等力度；赛道更热不能自动胜出，必须有订单、backlog、现金流或价格确认支撑 |")
    lines.append("| 上下游 | 作为数据中心客户、算力、服务器、网络和云平台需求链比较，区分谁捕获利润、谁承担capex和谁的估值更容易消化 | AMZN、MSFT、GOOGL、META、ORCL、EQIX、DLR、NVDA、AVGO、ANET、DELL、SMCI | 降低业务指标硬比，强调资金只能买一个时的增长质量、确定性和赔率 |")
    lines.append("| 跨赛道 | 作为组合资金替代比较，重点看增长质量、风险调整收益、估值消化、下行保护和催化可见度 | 半导体设备、材料、封测、工业和软件中与ENS需求链较远的公司 | 默认降低结论力度；除非增长质量、估值消化或右尾弹性明显拉开 |")
    lines.append("")
    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    lines.append("| 序号 | 公司B | 公司B分类 | 可比关系 | 档位差摘要 | NTM兑现优先 | 右尾弹性优先 | 风险调整收益 | 下行保护优先 | 估值消化优先 | 近端催化优先 | 价格确认/动量 | 激进短线 | 多数思路方向 | 最终更值得投 | 最关键理由 |")
    lines.append("| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(comparisons, 1):
        b_label = f"{row_obj['ticker']} / {row_obj['name']}"
        cells = [
            str(idx),
            b_label,
            row_obj["classification"],
            row_obj["relationship"],
            row_obj["grade_diff"],
        ] + [row_obj[strat] for strat in STRATS] + [
            row_obj["majority"],
            row_obj["final_choice"],
            row_obj["key_reason"],
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## 6. 投资思路统计")
    lines.append("")
    lines.append("| 投资思路 | 强烈建议投A | 建议投A | 微倾向投A | 中性 | 微倾向投B | 建议投B | 强烈建议投B | A侧合计 | B侧合计 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strat in STRATS:
        c = stats[strat]
        a_side = c["强烈建议投A"] + c["建议投A"] + c["微倾向投A"]
        b_side = c["微倾向投B"] + c["建议投B"] + c["强烈建议投B"]
        lines.append(
            f"| {strat} | {c['强烈建议投A']} | {c['建议投A']} | {c['微倾向投A']} | {c['中性']} | "
            f"{c['微倾向投B']} | {c['建议投B']} | {c['强烈建议投B']} | {a_side} | {b_side} |"
        )
    lines.append("")
    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_b, 1):
        wins = [strat for strat in STRATS if "投B" in row_obj[strat]]
        catchup = "ENS 需要看到DataSafe Noir可量化客户/OEM认证、data center orders继续转收入、PPS订单放量、ex-45X利润和FCF继续上修，并重新获得价格确认。"
        lines.append(f"| {idx} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:5])} | {row_obj['key_reason']} | {catchup} |")
    lines.append("")
    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strat for strat in STRATS if "投A" in row_obj[strat]]
        catchup = "B 需要拿出更清晰的NTM收入/利润兑现、订单或客户合同，并证明估值、现金流和压力窗口能承受波动。"
        lines.append(f"| {idx} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:5])} | {row_obj['key_reason']} | {catchup} |")
    lines.append("")
    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。")
    lines.append(f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告，同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}。")
    lines.append(f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。")
    lines.append("- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。")
    lines.append("- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`、`公司调研/电力_发电_能源_储能/ENS_EnerSys_公司调研_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`。")
    lines.append(f"- ENS 日度数据快照：{daily_snapshot}")
    lines.append("- 生成脚本：`scripts/generate_ens_company_comparison.py`。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    report = render_report(companies, comparisons)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8")
    a = companies[TARGET]
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "ens_tiers": {strat: a.get("tiers", {}).get(strat) for strat in STRATS},
                "ens_ranks": {strat: a.get("ranks", {}).get(strat) for strat in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
