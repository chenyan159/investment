from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "CLS"
TARGET_NAME = "Celestica Inc"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CLS_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_EMS_PEERS = {"DELL", "HPE", "JBL", "FLEX", "SANM", "SMCI", "PENG", "FN"}
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
DOWNSTREAM_CLOUD = {"ADBE", "AMZN", "APLD", "BABA", "CRWD", "CRWV", "DLR", "EQIX", "GOOGL", "IBM", "IREN", "META", "MSFT", "NBIS", "NTNX", "ORCL"}

EXTRA_SCORE_FLOORS = {
    "ALAB": {"NTM兑现优先": 78, "右尾弹性优先": 92, "近端催化优先": 86, "价格确认/动量": 88, "激进短线": 94},
    "CRDO": {"NTM兑现优先": 80, "右尾弹性优先": 90, "近端催化优先": 84, "价格确认/动量": 84, "激进短线": 92},
    "MRVL": {"NTM兑现优先": 78, "右尾弹性优先": 86, "近端催化优先": 82, "激进短线": 86},
    "CIEN": {"NTM兑现优先": 80, "右尾弹性优先": 78, "风险调整收益": 62, "估值消化优先": 58, "近端催化优先": 80, "价格确认/动量": 74, "激进短线": 80},
    "COHR": {"NTM兑现优先": 76, "右尾弹性优先": 82, "近端催化优先": 80, "价格确认/动量": 80, "激进短线": 84},
    "FN": {"NTM兑现优先": 78, "右尾弹性优先": 82, "风险调整收益": 58, "近端催化优先": 78, "价格确认/动量": 82, "激进短线": 84},
    "DELL": {"NTM兑现优先": 84, "右尾弹性优先": 72, "风险调整收益": 62, "估值消化优先": 68, "近端催化优先": 78, "激进短线": 72},
    "SMCI": {"NTM兑现优先": 76, "右尾弹性优先": 76, "风险调整收益": 55, "估值消化优先": 82, "近端催化优先": 74, "激进短线": 78},
    "JBL": {"NTM兑现优先": 78, "右尾弹性优先": 70, "风险调整收益": 64, "估值消化优先": 68, "近端催化优先": 72, "价格确认/动量": 78, "激进短线": 76},
    "HPE": {"NTM兑现优先": 76, "右尾弹性优先": 68, "风险调整收益": 62, "估值消化优先": 72, "近端催化优先": 76, "激进短线": 70},
    "FLEX": {"NTM兑现优先": 70, "右尾弹性优先": 64, "风险调整收益": 62, "估值消化优先": 72, "近端催化优先": 68},
    "CRWV": {"右尾弹性优先": 86, "近端催化优先": 78, "激进短线": 88},
    "NBIS": {"右尾弹性优先": 88, "近端催化优先": 78, "价格确认/动量": 82, "激进短线": 90},
    "APLD": {"右尾弹性优先": 84, "近端催化优先": 76, "激进短线": 88},
    "IREN": {"右尾弹性优先": 82, "价格确认/动量": 80, "激进短线": 86},
    "POET": {"右尾弹性优先": 88, "价格确认/动量": 78, "激进短线": 92},
    "LWLG": {"右尾弹性优先": 86, "激进短线": 88},
}

CLS_SCORE_OVERRIDES = {
    "NTM兑现优先": 84.0,
    "右尾弹性优先": 81.0,
    "风险调整收益": 60.0,
    "下行保护优先": 44.0,
    "估值消化优先": 72.0,
    "近端催化优先": 84.0,
    "价格确认/动量": 76.0,
    "激进短线": 82.0,
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

    for ticker, floors in {**calibrated.SCORE_FLOORS, **EXTRA_SCORE_FLOORS}.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strat, floor in floors.items():
            current = company.setdefault("scores", {}).get(strat, 0)
            company["scores"][strat] = max(current, floor)

    for strat, score in CLS_SCORE_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strat] = score
    calibrated.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = company["ticker"]
    category = company.get("category", "")
    if ticker in DIRECT_EMS_PEERS:
        return "直接同业"
    if ticker in SERVER_STORAGE_ADJACENT:
        return "相邻替代"
    if ticker in AI_NETWORK_UPDOWN or ticker in AI_COMPUTE_UPSTREAM or ticker in DOWNSTREAM_CLOUD:
        return "上下游"
    if category in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict, diff: float) -> str:
    ticker = company["ticker"]
    cat = company.get("category", "")
    if winner == "A":
        return {
            "NTM兑现优先": "A有190亿美元FY2026指引和HPS/CCS硬锚",
            "右尾弹性优先": "A的800G/1.6T与AI compute右尾可收入化",
            "风险调整收益": "A增长、估值和现金流组合更均衡",
            "下行保护优先": "A现金流为正且资产负债表仍健康",
            "估值消化优先": "A用高增长和约3.1x P/S消化估值",
            "近端催化优先": "A有Q2指引、1.6T H2和AI/ML ramp",
            "价格确认/动量": "A两周涨幅强，价格已确认兑现",
            "激进短线": "A高IV叠加AI网络/1.6T叙事",
        }[strat]
    if winner == "B":
        if ticker in DIRECT_EMS_PEERS:
            return {
                "NTM兑现优先": "B同业订单或AI服务器兑现更直接",
                "右尾弹性优先": "B同业右尾或客户项目弹性更大",
                "风险调整收益": "B同业估值/现金流组合更优",
                "下行保护优先": "B同业波动、估值或压力期更稳",
                "估值消化优先": "B同业倍数更易被业绩消化",
                "近端催化优先": "B同业订单/财报催化更近",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线弹性更强",
            }[strat]
        if cat in HIGH_GROWTH_CATS or ticker in AI_NETWORK_UPDOWN or ticker in AI_COMPUTE_UPSTREAM or ticker in DOWNSTREAM_CLOUD:
            return {
                "NTM兑现优先": "B AI主链订单/RPO兑现更短链",
                "右尾弹性优先": "B AI主链右尾或小基数更大",
                "风险调整收益": "B上行更能覆盖执行风险",
                "下行保护优先": "B现金流、规模或估值缓冲更好",
                "估值消化优先": "B业绩弹性更能消化估值",
                "近端催化优先": "B近端产品/订单催化更密集",
                "价格确认/动量": "B价格趋势和资金偏好更强",
                "激进短线": "B高beta和关注度更适合进攻",
            }[strat]
        if cat in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单backlog和交付链更清楚",
                "右尾弹性优先": "B电力/冷却瓶颈右尾更直接",
                "风险调整收益": "B增长和估值组合更优",
                "下行保护优先": "B订单粘性或利润稳定性更强",
                "估值消化优先": "B用订单兑现消化估值更容易",
                "近端催化优先": "B订单/产能/财报催化更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化交易弹性更强",
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
    diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)
    return f"{label}：{reason_for(strat, winner, b, diff)}"


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


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    if choice == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:
            return "CLS的HPS/CCS收入兑现、FY2026指引和1.6T时间表更清楚。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:
            return "CLS当前估值能被高增长和利润扩张更好消化。"
        return "CLS在多数投资思路下增长、催化和价格确认更均衡。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 12:
        return f"{b['ticker']}的右尾或小基数弹性明显强于CLS。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 12:
        return f"{b['ticker']}的现金流、波动或压力期防御明显优于CLS。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 10:
        return f"{b['ticker']}的NTM订单/收入兑现证据更强。"
    return f"{b['ticker']}在多数投资思路下比CLS更符合该资金目标。"


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
        row_obj["key_reason"] = key_reason(a, b, row_obj, choice)
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
        "NTM兑现优先": ("S", "全项目顶层", "2026Q1收入40.47亿美元同比+53%，FY2026收入指引上调至190亿美元，CCS/HPS已有收入硬锚", "H2 implied run-rate、客户验收、switch ASIC/optics和营运资本仍是执行瓶颈"),
        "右尾弹性优先": ("A", "强势档", "800G仍放量，DS6000/DS6001 1.6T两家hyperscaler H2启动，AI/ML compute与rack integration提供右尾", "不是芯片垄断利润池，极度乐观需要多个客户和供应链同时兑现"),
        "风险调整收益": ("A", "强势档但非防御", "高增长、正FCF、净债务较低和估值倍数仍可被业绩消化", "客户集中、毛利率低于芯片/软件商、capex和工作资本放大下行"),
        "下行保护优先": ("C", "中性偏弱", "Q1 FCF为正、ATS提供稳定器，净债务不高", "Call IV约78.8%、SOXX压力窗口累计-73.85%，高增长硬件链不是防御资产"),
        "估值消化优先": ("A", "强势档", "Forward PE约25.19、P/S约3.14，对应NTM收入210-228亿美元和利润扩张仍可解释", "若800G ASP下行或HPS mix变差，估值消化速度会快速恶化"),
        "近端催化优先": ("S", "全项目顶层", "Q2指引41.5-44.5亿美元、FY2026上修、1.6T program 2026H2启动、AI/ML compute ramp", "客户/订单量未完全披露，催化若推迟会从2026H2滑到2027"),
        "价格确认/动量": ("B", "中上档", "过去两周+32.23%，市场已经开始确认AI网络与平台制造兑现", "区间涨跌文件截至2026-06-03，且高IV意味着反向波动也大"),
        "激进短线": ("B", "中上档", "高IV、强动量、1.6T/AI Ethernet/AI compute叙事兼具，适合事件进攻", "短线爆发力弱于ALAB、CRDO、POET、NBIS等更小基数或更高beta标的"),
    }

    lines: list[str] = []
    lines.append("# CLS 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：CLS / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(comparisons)}")
    lines.append(f"公司评估文件日期范围：{date_range}")
    lines.append("日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 压力窗口")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、CLS 公司调研、相关行业调研和 `金融资料/` 金融及区间涨跌文件；未读取、引用或继承 `特征量化/`、Signals、回归、模型比较、`公司排序/`、`简单排序/`、备份目录或临时结果。每一行是 CLS 与一家项目内公司 B 的二选一判断。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append(f"- A 最占优的投资思路：`{'`、`'.join(a_best)}`。CLS 的强项是 FY2026 指引上修、HPS/CCS 已经进收入表、1.6T/AI compute/rack integration 有明确时间表，以及价格已经给出确认。")
    lines.append(f"- A 最吃亏的投资思路：`{'`、`'.join(a_worst)}`。主要短板是客户集中、制造型毛利率、2026 capex/营运资本压力，以及高 IV 和 SOXX 压力窗口回撤暴露。")
    lines.append("- A 最适合的投资者画像：愿意买 AI 数据中心网络、平台硬件和复杂系统制造兑现，同时接受高波动和客户集中风险的中期进攻型资金。")
    lines.append("- A 最不适合的投资者画像：要求公用事业式下行保护、低波动现金流，或只追求芯片/软件垄断利润率的资金。")
    lines.append("- 多数思路下最强反方公司：" + "、".join([f"{r['ticker']}（{r['name']}）" for r in strong_b[:8]]) + "。")
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：CLS 是全项目强势 AI 基础设施兑现标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。")
    lines.append("- 后续最重要跟踪数据：Q2/Q3收入和EPS、HPS revenue、CCS segment margin、1.6T客户量产、AI/ML compute program、rack integration收入/毛利、2026 capex投产、inventory/AR/AP/customer cash deposits、800G/1.6T optics ASP和客户多供压价。")
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | CLS |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.get('category', 'AI服务器_存储_EMS')} |")
    lines.append("| 重要产品/业务线 | CCS/HPS 800G AI网络交换与高性能networking；DS6000/DS6001 1.6T switch；AI/ML compute与Enterprise server/storage program；rack integration、testing、software configuration和lifecycle service；HPS storage；ATS稳定型业务 |")
    lines.append("| NTM 基准收入 | 210-228亿美元；基准高于FY2026 190亿美元指引，因为NTM含2027Q1且公司披露2027需求可见度和新program wins增强 |")
    lines.append("| 乐观/极度乐观收入 | 乐观235-258亿美元；极度乐观260-290亿美元 |")
    lines.append("| 利润和现金流结论 | 基准adjusted operating margin 8.0%-8.6%，调整后净利润约12.8-15.0亿美元；FCF约6-9亿美元但受capex、AR和inventory约束 |")
    lines.append("| 最大传导瓶颈 | HPS/CCS高速ramp能否按客户认证、switch ASIC/optics/测试产能、工作资本和新产能投产节奏转为可确认收入 |")
    lines.append("| 最大反证 | 客户集中、800G ASP下行、1.6T qualification推迟、客户转向Arista/NVIDIA/Cisco或台系ODM、多供压价、capex和工作资本吞噬现金流 |")
    lines.append("| 近端催化剂 | Q2 2026 revenue/EPS、FY2026继续上修、两家hyperscaler 1.6T program 2026H2启动、AI/ML compute ramp、HPS/CCS margin和2027 visibility |")
    lines.append("| 日度数据 | " + daily_snapshot + " |")
    lines.append("")
    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
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
    lines.append("| 直接同业 | AI服务器/存储/EMS、ODM/OEM、平台硬件和复杂系统制造同池比较，优先看客户订单、收入兑现、毛利率、交付能力、capex和估值消化 | DELL、HPE、JBL、FLEX、SANM、SMCI、PENG、FN | 判断力度最高；同业中若一方订单、margin或估值明显更硬，可以给建议或强烈建议 |")
    lines.append("| 相邻替代 | 同属AI基础设施资金篮子，但不是直接制造/平台对手，重点比较增长质量、兑现确定性、估值、催化和资金偏好 | MU、STX、WDC、PSTG、VRT、ETN、GEV、PWR、POWL、MOD | 保持中等力度；赛道更热不能自动胜出，必须有订单或收入传导证据 |")
    lines.append("| 上下游 | CLS 的芯片、交换ASIC、光/铜互联、连接器、电源或云客户链条上下游，重点看利润池、议价权和谁捕获瓶颈价值 | NVDA、AVGO、AMD、MRVL、ANET、CIEN、CRDO、COHR、MSFT、AMZN、GOOGL、META | 不把下游收入规模或上游瓶颈自动等同于胜出；强调利润捕获和反证 |")
    lines.append("| 跨赛道 | 半导体材料、前道设备、封测、工业/化工等与CLS业务差异大但可作为资金配置替代 | ASML、AMAT、LIN、ECL、TMO、DHR、CAT | 默认降低结论力度；除非增长质量、估值消化或下行保护明显拉开 |")
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
        need = "CLS需要把1.6T、AI/ML compute和rack integration转成更明确的订单/收入披露，同时维持CCS/HPS margin并改善压力窗口表现。"
        lines.append(f"| {idx} | {base.md(row_obj['ticker'] + ' / ' + row_obj['name'])} | {'、'.join(wins[:5])} | {base.md(row_obj['key_reason'])} | {need} |")
    lines.append("")
    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strat for strat in STRATS if "投A" in row_obj[strat]]
        need = "B需要拿出更硬的NTM收入/利润兑现、客户订单、估值消化证据或价格确认，才能抵消CLS的AI网络兑现优势。"
        lines.append(f"| {idx} | {base.md(row_obj['ticker'] + ' / ' + row_obj['name'])} | {'、'.join(wins[:5])} | {base.md(row_obj['key_reason'])} | {need} |")
    lines.append("")
    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。")
    lines.append(f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告，同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}。")
    lines.append(f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。")
    lines.append("- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。")
    lines.append("- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI服务器_存储_EMS/CLS_Celestica Inc_公司调研_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI服务器整机与机架集成_2026-06-10.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`。")
    lines.append(f"- CLS 日度数据快照：{daily_snapshot}")
    lines.append("- 生成脚本：`scripts/generate_cls_company_comparison.py`。")
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
        "cls_tiers": {strat: a.get("tiers", {}).get(strat) for strat in STRATS},
        "cls_ranks": {strat: a.get("ranks", {}).get(strat) for strat in STRATS},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
