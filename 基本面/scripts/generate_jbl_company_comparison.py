from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_cls_company_comparison as cls_calibrated


TARGET = "JBL"
TARGET_NAME = "Jabil Inc"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "JBL_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_EMS_PEERS = {"DELL", "HPE", "CLS", "FLEX", "SANM", "SMCI", "PENG", "FN"}
SERVER_STORAGE_ADJACENT = {"MRAM", "NTAP", "PSTG", "RMBS", "SIMO", "SNDK", "STX", "WDC", "MU"}
AI_NETWORK_UPDOWN = {
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
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}
AI_COMPUTE_UPSTREAM = {
    "ADI",
    "AMD",
    "ARM",
    "CDNS",
    "INTC",
    "MCHP",
    "MXL",
    "NVDA",
    "ON",
    "QCOM",
    "SNPS",
    "STM",
    "TXN",
}
DOWNSTREAM_CLOUD = {
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
POWER_COOLING_ADJACENT = {
    "AAON",
    "ABBNY",
    "AEIS",
    "AEP",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "CMI",
    "DKILY",
    "DLR",
    "DTE",
    "EME",
    "ENS",
    "ENPH",
    "ET",
    "ETN",
    "ETR",
    "FIX",
    "FLNC",
    "FCEL",
    "GEV",
    "GNRC",
    "HUBB",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "NVT",
    "OKLO",
    "POWL",
    "POWI",
    "PSIX",
    "PWR",
    "SMR",
    "TT",
    "VICR",
    "VRT",
    "VST",
}

EXTRA_SCORE_FLOORS = {
    **calibrated.SCORE_FLOORS,
    **cls_calibrated.EXTRA_SCORE_FLOORS,
    "CLS": cls_calibrated.CLS_SCORE_OVERRIDES,
    "CRWV": {
        "NTM兑现优先": 92,
        "右尾弹性优先": 100,
        "风险调整收益": 56,
        "下行保护优先": 35,
        "估值消化优先": 63,
        "近端催化优先": 86,
        "价格确认/动量": 60,
        "激进短线": 100,
    },
    "CSCO": {
        "NTM兑现优先": 72,
        "右尾弹性优先": 55,
        "风险调整收益": 82,
        "下行保护优先": 90,
        "估值消化优先": 64,
        "近端催化优先": 70,
        "价格确认/动量": 76,
        "激进短线": 66,
    },
    "CIEN": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 78,
        "风险调整收益": 64,
        "下行保护优先": 58,
        "估值消化优先": 68,
        "近端催化优先": 84,
        "价格确认/动量": 74,
        "激进短线": 80,
    },
    "DELL": {
        "NTM兑现优先": 86,
        "右尾弹性优先": 78,
        "风险调整收益": 68,
        "下行保护优先": 52,
        "估值消化优先": 72,
        "近端催化优先": 82,
        "价格确认/动量": 76,
        "激进短线": 76,
    },
    "FLEX": {
        "NTM兑现优先": 70,
        "右尾弹性优先": 64,
        "风险调整收益": 66,
        "下行保护优先": 56,
        "估值消化优先": 74,
        "近端催化优先": 68,
        "价格确认/动量": 72,
        "激进短线": 68,
    },
    "SANM": {
        "NTM兑现优先": 66,
        "右尾弹性优先": 56,
        "风险调整收益": 64,
        "下行保护优先": 62,
        "估值消化优先": 72,
        "近端催化优先": 62,
        "价格确认/动量": 62,
        "激进短线": 60,
    },
    "SMCI": {
        "NTM兑现优先": 76,
        "右尾弹性优先": 80,
        "风险调整收益": 55,
        "下行保护优先": 35,
        "估值消化优先": 84,
        "近端催化优先": 78,
        "价格确认/动量": 72,
        "激进短线": 84,
    },
    "HPE": {
        "NTM兑现优先": 76,
        "右尾弹性优先": 70,
        "风险调整收益": 64,
        "下行保护优先": 58,
        "估值消化优先": 72,
        "近端催化优先": 76,
        "价格确认/动量": 72,
        "激进短线": 70,
    },
}

JBL_SCORE_OVERRIDES = {
    "NTM兑现优先": 82.0,
    "右尾弹性优先": 76.0,
    "风险调整收益": 78.0,
    "下行保护优先": 62.0,
    "估值消化优先": 84.0,
    "近端催化优先": 80.0,
    "价格确认/动量": 62.0,
    "激进短线": 70.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    calibrated.fix_growth_ranges(companies)
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in EXTRA_SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strat, floor in floors.items():
            current = company.setdefault("scores", {}).get(strat, 0)
            company["scores"][strat] = max(current, floor)

    for strat, score in JBL_SCORE_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strat] = score
    calibrated.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = company["ticker"]
    category = company.get("category", "")
    if ticker in DIRECT_EMS_PEERS:
        return "直接同业"
    if ticker in SERVER_STORAGE_ADJACENT or ticker in POWER_COOLING_ADJACENT:
        return "相邻替代"
    if ticker in AI_NETWORK_UPDOWN or ticker in AI_COMPUTE_UPSTREAM or ticker in DOWNSTREAM_CLOUD:
        return "上下游"
    if category in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict) -> str:
    ticker = company["ticker"]
    category = company.get("category", "")
    if winner == "A":
        return {
            "NTM兑现优先": "JBL指引与AI收入已进入收入表",
            "右尾弹性优先": "JBL AI rack与power/thermal有收入化路径",
            "风险调整收益": "JBL估值、FCF和AI增长更均衡",
            "下行保护优先": "JBL有FCF和非AI业务底座",
            "估值消化优先": "JBL低P/S和core EPS更易消化",
            "近端催化优先": "FY2027指引和Hanley/AI客户可催化",
            "价格确认/动量": "JBL价格已确认但不过度过热",
            "激进短线": "JBL AI制造叙事仍有短线弹性",
        }[strat]
    if winner == "B":
        if ticker in DIRECT_EMS_PEERS:
            return {
                "NTM兑现优先": "B同业订单或AI服务器兑现更直接",
                "右尾弹性优先": "B同业小基数或客户项目弹性更大",
                "风险调整收益": "B同业上行下行组合更优",
                "下行保护优先": "B同业波动或资产质量更稳",
                "估值消化优先": "B同业估值更易被业绩消化",
                "近端催化优先": "B同业订单/财报催化更近",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线爆发力更强",
            }[strat]
        if ticker in POWER_COOLING_ADJACENT or category in INFRA_CATS:
            return {
                "NTM兑现优先": "B电力/冷却订单兑现更短链",
                "右尾弹性优先": "B电力瓶颈右尾更直接",
                "风险调整收益": "B增长质量或订单可见度更优",
                "下行保护优先": "B现金流或长约/公用属性更稳",
                "估值消化优先": "B订单利润更能消化估值",
                "近端催化优先": "B订单/产能/电力重定价更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化交易弹性更高",
            }[strat]
        if category in HIGH_GROWTH_CATS or ticker in AI_NETWORK_UPDOWN or ticker in AI_COMPUTE_UPSTREAM or ticker in DOWNSTREAM_CLOUD:
            return {
                "NTM兑现优先": "B AI主链订单/RPO兑现更短链",
                "右尾弹性优先": "B AI主链利润池或小基数更大",
                "风险调整收益": "B上行更能覆盖执行风险",
                "下行保护优先": "B规模、现金流或估值缓冲更好",
                "估值消化优先": "B业绩弹性更能消化估值",
                "近端催化优先": "B近端产品/订单催化更密集",
                "价格确认/动量": "B价格趋势和资金偏好更强",
                "激进短线": "B高beta和关注度更适合进攻",
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
        strong_cut, suggest_cut, micro_cut = 24, 12, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 22, 10, 4
    else:
        strong_cut, suggest_cut, micro_cut = 18, 9, 4
    if diff > 0:
        if tier_gap >= 2 and abs_diff >= strong_cut:
            return "强烈建议投A"
        if tier_gap >= 1 or abs_diff >= suggest_cut:
            return "建议投A"
        if abs_diff >= micro_cut:
            return "微倾向投A"
    if diff < 0:
        if tier_gap <= -2 and abs_diff >= strong_cut:
            return "强烈建议投B"
        if tier_gap <= -1 or abs_diff >= suggest_cut:
            return "建议投B"
        if abs_diff >= micro_cut:
            return "微倾向投B"
    return "中性"


def cell_for(strat: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strat, a, b, rel)
    winner = "A" if label.endswith("投A") else "B" if label.endswith("投B") else "N"
    return f"{label}：{reason_for(strat, winner, b)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = b_count = neutral = 0
    for strat in STRATS:
        label = base.tag_in_cell(row_obj[strat]) or ""
        if label.endswith("投A"):
            a_count += 1
        elif label.endswith("投B"):
            b_count += 1
        else:
            neutral += 1
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
    ac, bc, _ = row_obj["ac"], row_obj["bc"], row_obj["nc"]
    if ac > bc:
        return "A"
    if bc > ac:
        return "B"
    risk_label = base.tag_in_cell(row_obj["风险调整收益"]) or ""
    if risk_label.endswith("投B"):
        return "B"
    return "A"


def key_reason(a: dict, b: dict, choice: str) -> str:
    if choice == "A":
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:
            return "JBL的AI收入兑现和低P/S估值消化更有吸引力。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:
            return "JBL在AI增长、FCF和估值压力之间的组合更均衡。"
        return "JBL在多数投资思路下比该公司更兼具兑现、估值和催化。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 12:
        return f"{b['ticker']}的右尾或小基数弹性明显强于JBL。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 12:
        return f"{b['ticker']}的现金流、波动或压力期防御明显优于JBL。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 10:
        return f"{b['ticker']}的NTM订单/收入兑现证据更强。"
    return f"{b['ticker']}在多数投资思路下比JBL更符合该资金目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
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
    a_strong, b_strong, close = [], [], []
    for strat in STRATS:
        gap = tier_value(a.get("tiers", {}).get(strat)) - tier_value(b.get("tiers", {}).get(strat))
        if gap >= 1:
            a_strong.append(short[strat])
        elif gap <= -1:
            b_strong.append(short[strat])
        else:
            close.append(short[strat])
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
    rows: list[dict] = []
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
        row_obj["ac"], row_obj["bc"], row_obj["nc"] = ac, bc, nc
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        choice = final_choice(row_obj)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, choice)
        rows.append(row_obj)

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda item: (rel_order.get(item["relationship"], 9), item["ticker"]))


def fmt_num(value, decimals: int = 1) -> str:
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
    selected = [r for r in rows if r["final_choice"] == final]
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
    final_a = sum(1 for r in comparisons if r["final_choice"] == "A")
    final_b = sum(1 for r in comparisons if r["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    a_side = {s: stats[s]["强烈建议投A"] + stats[s]["建议投A"] + stats[s]["微倾向投A"] for s in STRATS}
    b_side = {s: stats[s]["微倾向投B"] + stats[s]["建议投B"] + stats[s]["强烈建议投B"] for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:2]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:2]

    support = {
        "NTM兑现优先": ("强势档", "FY2026收入指引350亿美元、AI-related revenue 136亿美元、Q4 revenue guide 92-100亿美元，收入基准可信度中高", "不披露backlog/bookings/RPO，FY2027正式指引未出"),
        "右尾弹性优先": ("中上到强势", "AI rack、第三hyperscaler、Networking、Hanley power/thermal、Adani/India平台给出远期右尾", "EMS不捕获GPU/HBM/IP高毛利，极度乐观需要客户/订单/交付路径"),
        "风险调整收益": ("强势档", "Forward PE 22.53、P/S 1.18、FY2026 adjusted FCF 14亿美元以上，AI增长与估值较平衡", "客户多供、材料穿透、营运资本和低毛利率会压制利润弹性"),
        "下行保护优先": ("中性偏弱", "正FCF、回购、非AI业务底座和FY2026指引上修提供支撑", "SOXX压力窗口累计-51.81%，制造链库存/应收对需求下修敏感"),
        "估值消化优先": ("强势档", "低P/S、Forward PE约22.5与core EPS 12.70美元指引相对AI收入增长并不极端", "若AI收入只带来材料穿透而非margin扩张，估值消化会变慢"),
        "近端催化优先": ("强势档", "FY2027 AI-related revenue指引、第三hyperscaler、Hanley订单、Intelligent Infrastructure margin和Adani框架均可在1-2季重定价", "很多催化仍需正式订单/客户/收入拆分披露"),
        "价格确认/动量": ("中性到中上", "过去一月+10.68%，2026-06-22价格仍接近财报后高位，基本面已被价格确认", "动量弱于高beta光互联、NeoCloud、电气化小盘，且不是低波动资产"),
        "激进短线": ("弱势档", "Call IV 56.4%、AI制造+power/thermal叙事可支持事件交易", "相对全项目高beta右尾标的，短线爆发力和资金拥挤度明显不足"),
    }

    lines: list[str] = []
    lines.append("# JBL 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：JBL / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(comparisons)}")
    lines.append(f"公司评估文件日期范围：{date_range}")
    lines.append("日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 压力窗口")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、JBL公司调研、相关行业调研和 `金融资料/` 金融及区间涨跌文件；未读取、引用或继承 `特征量化/`、Signals、回归、模型比较、`公司排序/`、`简单排序/`、备份目录或临时结果。每一行是 JBL 与一家项目内公司 B 的二选一判断。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append(f"- A 最占优的投资思路：`{'`、`'.join(a_best)}`。JBL 最强的是 AI-related revenue 已经进入收入表、FY2026 指引和 FCF 有硬锚，并且估值仍低于多数 AI 主链高成长公司。")
    lines.append(f"- A 最吃亏的投资思路：`{'`、`'.join(a_worst)}`。主要短板是 EMS 模式不捕获芯片/IP毛利、backlog不披露、价格动量不如高beta右尾标的，压力期防守也不是全项目顶层。")
    lines.append("- A 最适合的投资者画像：想买 AI 数据中心硬件加速的收入兑现和估值消化，但不想承受纯芯片/光互联小盘极端估值的风险调整型资金。")
    lines.append("- A 最不适合的投资者画像：只追求最大右尾、最高短线波动或最强下行保护的资金；JBL是高质量AI制造平台，不是高毛利芯片垄断或公用事业防御资产。")
    lines.append("- 多数思路下最强反方公司：" + "、".join([f"{r['ticker']}（{r['name']}）" for r in strong_b[:8]]) + "。")
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：JBL 属于全项目中上到强势的 AI 硬件制造兑现标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。")
    lines.append("- 后续最重要跟踪数据：FY2027 revenue / AI-related revenue / core margin / FCF 指引；Intelligent Infrastructure revenue 和 core margin；Cloud & Data Center、Networking & Communications、Capital Equipment 三个端市场；Hanley订单或客户披露；第三hyperscaler贡献；inventory days、contract assets、operating cash flow、capex；GB300/Rubin/ASIC rack、1.6T optical、液冷/CDU、48/50V power shelf、BBU和800VDC design-in进度。")
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | JBL |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.get('category', 'AI服务器_存储_EMS')} |")
    lines.append("| 重要产品/业务线 | Cloud & Data Center Infrastructure / AI硬件制造与机架集成；Networking & Communications / 光互联与高速互联制造；Capital Equipment；Hanley与Jabil power/thermal；Regulated Industries与Connected Living/Digital Commerce非AI底座 |")
    lines.append("| NTM 基准收入 | 390-410亿美元；基准含义是Q4 FY26指引兑现、FY27 AI-related revenue继续增长但不把全部远期pipeline提前确认 |")
    lines.append("| 乐观/极度乐观收入 | 乐观430-460亿美元；极度乐观480-520亿美元，但极度情景需多个客户、平台、power/thermal和供应链同时突破 |")
    lines.append("| 利润和现金流结论 | 基准core operating margin 5.9%-6.2%，core EBITDA约31-34亿美元，core earnings约15-17亿美元，adjusted FCF方向12-16亿美元 |")
    lines.append("| 最大传导瓶颈 | 客户PO/forecast、GPU/ASIC/HBM/CoWoS供给、AI rack验收、液冷/电力/网络联调、区域产能爬坡和营运资本承受能力 |")
    lines.append("| 最大反证 | FY2027 AI-related revenue低于150亿美元或持平；Q4 FY26交付不达指引；core margin回落到5.3%-5.6%；库存/应收/合同资产显著上升但revenue未兑现；客户转向ODM/其他EMS |")
    lines.append("| 近端催化剂 | FY2027正式revenue/AI-related revenue/core margin/FCF指引；第三hyperscaler；Hanley订单/客户；Adani框架；Intelligent Infrastructure端市场和margin |")
    lines.append("| 日度数据 | " + daily_snapshot + " |")
    lines.append("")
    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in STRATS:
        tier = a.get("tiers", {}).get(strat, "资料不足")
        position = f"{support[strat][0]}；评分排名 {a.get('ranks', {}).get(strat)}/{a.get('rank_total', {}).get(strat)}"
        lines.append(f"| {strat} | {tier} | {position} | {support[strat][1]} | {support[strat][2]} |")
    lines.append("")
    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | AI服务器/存储/EMS、ODM/OEM、平台硬件和复杂系统制造同池比较，优先看客户订单、收入兑现、毛利率、交付能力、capex和估值消化 | CLS、DELL、HPE、FLEX、SANM、SMCI、PENG、FN | 判断力度最高；同业中若一方订单、margin或估值明显更硬，可以给建议或强烈建议 |")
    lines.append("| 相邻替代 | 同属AI基础设施资金篮子，但不是JBL直接制造对手，重点比较增长质量、兑现确定性、估值、催化和资金偏好 | MU、STX、WDC、PSTG、VRT、ETN、GEV、PWR、POWL、MOD | 保持中等力度；赛道更热不能自动胜出，必须有订单或收入传导证据 |")
    lines.append("| 上下游 | JBL 的芯片、交换ASIC、光/铜互联、连接器、电源或云客户链条上下游，重点看利润池、议价权和谁捕获瓶颈价值 | NVDA、AVGO、AMD、MRVL、ANET、CIEN、CRDO、COHR、MSFT、AMZN、GOOGL、META | 不把下游收入规模或上游瓶颈自动等同于胜出；强调利润捕获和反证 |")
    lines.append("| 跨赛道 | 半导体材料、前道设备、封测、工业/化工等与JBL业务差异大但可作为资金配置替代 | ASML、AMAT、LIN、ECL、TMO、DHR、CAT | 默认降低结论力度；除非增长质量、估值消化或下行保护明显拉开 |")
    lines.append("")
    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATS, "多数思路方向", "最终更值得投", "最关键理由"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---:" if h == "序号" else "---" for h in headers]) + " |")
    for idx, row_obj in enumerate(comparisons, 1):
        cells = [
            str(idx),
            f"{row_obj['ticker']} / {row_obj['name']}",
            row_obj["classification"],
            row_obj["relationship"],
            row_obj["grade_diff"],
            *[row_obj[strat] for strat in STRATS],
            row_obj["majority"],
            row_obj["final_choice"],
            row_obj["key_reason"],
        ]
        lines.append("| " + " | ".join(base.md(cell) for cell in cells) + " |")
    lines.append("")
    lines.append("## 6. 投资思路统计")
    lines.append("")
    lines.append("| 投资思路 | 强烈建议投A | 建议投A | 微倾向投A | 中性 | 微倾向投B | 建议投B | 强烈建议投B | A侧合计 | B侧合计 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strat in STRATS:
        counter = stats[strat]
        a_total = counter["强烈建议投A"] + counter["建议投A"] + counter["微倾向投A"]
        b_total = counter["微倾向投B"] + counter["建议投B"] + counter["强烈建议投B"]
        lines.append(
            f"| {strat} | {counter['强烈建议投A']} | {counter['建议投A']} | {counter['微倾向投A']} | {counter['中性']} | "
            f"{counter['微倾向投B']} | {counter['建议投B']} | {counter['强烈建议投B']} | {a_total} | {b_total} |"
        )
    lines.append("")
    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_b, 1):
        wins = [strat for strat in STRATS if "投B" in row_obj[strat]]
        need = "JBL需要披露更明确的FY2027 AI收入、客户/订单/backlog、Hanley订单和更高core margin，同时证明AI增长不会吞噬FCF。"
        lines.append(f"| {idx} | {base.md(row_obj['ticker'] + ' / ' + row_obj['name'])} | {'、'.join(wins[:5])} | {base.md(row_obj['key_reason'])} | {need} |")
    lines.append("")
    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strat for strat in STRATS if "投A" in row_obj[strat]]
        need = "B需要拿出更硬的NTM收入/利润兑现、客户订单、估值消化证据或价格确认，才能抵消JBL的AI制造兑现和估值优势。"
        lines.append(f"| {idx} | {base.md(row_obj['ticker'] + ' / ' + row_obj['name'])} | {'、'.join(wins[:5])} | {base.md(row_obj['key_reason'])} | {need} |")
    lines.append("")
    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。")
    lines.append(f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告，同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}。")
    lines.append(f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。")
    lines.append("- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。")
    lines.append("- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI服务器_存储_EMS/JBL_Jabil Inc_公司调研_2026-06-20.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI服务器整机与机架集成_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`。")
    lines.append(f"- JBL 日度数据快照：{daily_snapshot}")
    lines.append("- 生成脚本：`scripts/generate_jbl_company_comparison.py`。")
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
    print(json.dumps({
        "target": TARGET,
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "jbl_tiers": {strat: a.get("tiers", {}).get(strat) for strat in STRATS},
        "jbl_ranks": {strat: a.get("ranks", {}).get(strat) for strat in STRATS},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
